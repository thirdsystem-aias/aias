#!/usr/bin/env python3
"""
aias_new_phase.py — Scaffold a new AIAS phase by cloning the prior phase.

One command bootstraps the entire build pipeline for a new phase from the
prior phase's files, with version strings swapped throughout. Eliminates the
build-pipeline-drift class of errors that cost time in v0.22 (improvised
scripts, divergent paper builders, missing parent dirs, etc.).

What gets scaffolded:

  scripts/build_charts_vNN.py        ← copy from prior phase, version-swapped
  scripts/build_paper_v0_NN.py       ← copy, version-swapped
  reports/build_report_vNN.py        ← copy, version-swapped
  reports/vNN_<substrate>_content.py ← skeleton (11-attr structure preserved)
  prereg/v0_NN_<substrate>_content.py← skeleton (TBD fields marked)
  prereg/v0_NN_mega_prompt.md        ← boilerplate sections
  papers/v0_NN/v0_NN_ssrn_paper_draft.md ← canonical template
                                          (YAML + titlepage + sections)
  osf/vNN/                           ← directory tree (data/, prereg/, reports/,
                                       figures/, scripts/, registries/, README)
  reports/figs/vNN/                  ← chart output directory

What does NOT get scaffolded (operator-authored):

  - Pre-registration content (hypotheses, registry, thresholds, predictions)
  - Mega-prompt design rationale
  - Acquisition CSVs (these come from Phase A/B runs)
  - Verdict JSON (comes from scoring)

The intent: after running this, the operator has a working build pipeline
that compiles cleanly with stub data. They then fill in the pre-registration
content, run acquisition, populate verdicts.json, and the pipeline renders
the phase end-to-end without further intervention.

Usage:
    python3 scripts/aias_new_phase.py \\
        --from v0.22 --to v0.23 \\
        --substrate "luxury watches" \\
        [--substrate-slug luxury_watches] \\
        [--dry-run]

Examples:
    # Scaffold v0.23 luxury watches from v0.22 automotive
    python3 scripts/aias_new_phase.py --from v0.22 --to v0.23 --substrate "luxury watches"

    # Preview without writing anything
    python3 scripts/aias_new_phase.py --from v0.22 --to v0.23 --substrate "premium spirits" --dry-run
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

AIAS_ROOT = Path.home() / "aias"

# Canonical SSRN ID registry — update when each phase ships.
# Used to generate upstream-phases citation reference for new phases.
PHASE_SSRN_REGISTRY = {
    "v0.16": ("Kitchen knives", 6791999),
    "v0.17": ("Premium kitchenware", 6802261),
    "v0.18": ("Indie fragrance", 6806558),
    "v0.19": ("Audiophile headphones", 6809182),
    "v0.20": ("Skincare", 6811441),
    "v0.21": ("Cosmetics", 6815378),
    "v0.22": ("Automotive", 6829118),
    "v0.23": ("Premium spirits", 6834298),
    "v0.24": ("B2B SaaS", 6838802),
    # v0.25–v0.29 are construct-validity studies (not substrate-presence papers), so each
    # sets its real title. v0.25/v0.26 use the canonical registry short-form (their in-repo
    # paper drafts carry a stale clone title); v0.27 has no draft yet. v0.31 is intentionally
    # absent (WITHDRAWN on SSRN; lineage carried via substrate phases + v1.7, per v0.34).
    "v0.25": {"substrate": "B2B SaaS Construct Validity", "ssrn_id": 6842138,
              "title": "B2B SaaS Construct Validity"},
    "v0.26": {"substrate": "Amazon BSR Discriminant Validity", "ssrn_id": 6847678,
              "title": "Amazon BSR Discriminant Validity"},
    "v0.27": {"substrate": "B2B SaaS Convergent Validity", "ssrn_id": 6854758,
              "title": "B2B SaaS Convergent Validity"},
    "v0.28": {"substrate": "Tech BRAND Discriminant Validity (CV.04)", "ssrn_id": 6865478,
              "title": "AI Availability is Not Reducible to Recognition Memory --- "
                       "and is Underpowered Against Familiarity at n = 24"},
    "v0.29": {"substrate": "Presence Construct-Validity Baseline (CV.05)", "ssrn_id": 6870778,
              "title": "The Presence Component Is Construct-Valid"},
    # Entry schema: a value is either the legacy 2-tuple (substrate, ssrn_id) OR a
    # dict carrying an optional `title` (or `short_title`) that overrides the
    # "AI Presence in {substrate}" descriptor in generate_upstream_phases().
    # v0.30 is an instrument pilot, not a substrate paper, so it sets its real title.
    "v0.30": {
        "substrate": "Consistency component (CPC.01)",
        "ssrn_id": 6875319,
        "title": 'Recognition Saturates, Consistency Doesn\'t — '
                 'An Instrument-Specification Pilot of the AIAS Consistency Component (CPC)',
    },
    # v0.31 intentionally omitted (WITHDRAWN). CPC re-analysis phases below set real titles.
    "v0.32": {"substrate": "CPC Version-Snapshot Stability", "ssrn_id": 6898581,
              "title": "Version-Snapshot Stability of an AI-Presence Consistency Score"},
    "v0.33": {"substrate": "Provider-Asymmetric CPC (CPC.02)", "ssrn_id": 6909019,
              "title": "Provider-Asymmetric Consistency in AI Brand Availability"},
    "v0.34": {"substrate": "CPC Longitudinal t1->t2 Stability (CPC.03)", "ssrn_id": 6915458,
              "title": "Two-Wave Temporal Stability of an AI Brand-Recall Consistency Quantity"},
}

METHODOLOGY_SSRN_REGISTRY = {
    "v1.2": ("Construct Validity and Four-Regime Taxonomy", 6761698),
    "v1.3": ("Phase A Pivot-Validation Specification", 6797679),
    "v1.4": ("Recognition × Recall Decomposition", 6799479),
    "v1.5": ("Multi-Statistic C2 and Two-Channel Recall", 6810758),
    "v1.6": ("Substrate Pre-Screening, Independent Moderator, Phantom Extension", 6816340),
    "v1.7": ("CPC Consistency --- Pre-Registered Negative Result "
             "(CV not independent of Presence)", 6878818),
}

SYNTHESIS_SSRN_REGISTRY = {
    "AIAS 1.0": ("Five-Substrate Foundational Construct Claim", 6817841),
}

FOUNDATIONAL_SSRN = ("Tri-System Brand Growth", 6659000)


def parse_version(v: str) -> tuple[str, str, str, str]:
    """Parse 'v0.22' or 'v0_22' or '0.22' → ('v0.22', 'v0_22', 'v22', '0_22').

    Returns (display, snake_full, snake_short, snake_no_v) for use in different contexts:
      display     'v0.22'  — for prose, logs, comments
      snake_full  'v0_22'  — for filenames like 'build_paper_v0_22.py', 'osf/v22/' paths
      snake_short 'v22'    — for filenames like 'build_charts_v22.py', 'reports/figs/v22/'
      snake_no_v  '0_22'   — rare, for some internal var names
    """
    v = v.strip().lstrip("v").replace("_", ".")
    if "." not in v:
        raise ValueError(f"Unrecognized version: {v!r}; expected like 'v0.22' or '0.22'")
    major, minor = v.split(".", 1)
    display = f"v{major}.{minor}"
    snake_full = f"v{major}_{minor}"
    # snake_short drops the major when major=='0' (so v0.22 → v22), keeps it otherwise
    snake_short = f"v{minor}" if major == "0" else f"v{major}_{minor}"
    snake_no_v = f"{major}_{minor}"
    return display, snake_full, snake_short, snake_no_v


def slugify(s: str) -> str:
    """'luxury watches' → 'luxury_watches'; 'Premium Spirits' → 'premium_spirits'."""
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def version_swap(text: str, *,
                 from_display: str, to_display: str,
                 from_snake_full: str, to_snake_full: str,
                 from_snake_short: str, to_snake_short: str,
                 from_substrate_slug: str = "",
                 to_substrate_slug: str = "") -> str:
    """Replace version strings and substrate slug in `text`.

    Order matters: longer patterns first so 'v0.22' doesn't get partially matched
    when looking for 'v22'.
    """
    replacements = [
        (from_display, to_display),
        (from_snake_full, to_snake_full),
        (from_snake_short, to_snake_short),
    ]
    if from_substrate_slug and to_substrate_slug and from_substrate_slug != to_substrate_slug:
        replacements.append((from_substrate_slug, to_substrate_slug))
    # Sort by length of source string DESCENDING so 'v0.22' (5 chars) replaces
    # before 'v22' (3 chars).
    replacements.sort(key=lambda r: -len(r[0]))
    for src, dst in replacements:
        text = text.replace(src, dst)
    return text


def clone_file(src_path: Path, dst_path: Path,
               version_args: dict, *, root: Path,
               dry_run: bool = False) -> None:
    """Copy file with version strings swapped throughout content."""
    if not src_path.exists():
        print(f"  [skip] {src_path} not found", file=sys.stderr)
        return
    text = src_path.read_text(encoding="utf-8")
    new_text = version_swap(text, **version_args)
    if dry_run:
        try:
            rel = dst_path.relative_to(root)
        except ValueError:
            rel = dst_path
        print(f"  [dry-run] would write: {rel}  ({len(new_text):,} chars)")
        return
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    dst_path.write_text(new_text, encoding="utf-8")
    try:
        rel = dst_path.relative_to(root)
    except ValueError:
        rel = dst_path
    print(f"  [write] {rel}")


def ensure_dir(path: Path, *, root: Path, dry_run: bool = False) -> None:
    try:
        rel = path.relative_to(root)
    except ValueError:
        rel = path
    if dry_run:
        print(f"  [dry-run] would mkdir: {rel}/")
        return
    path.mkdir(parents=True, exist_ok=True)
    print(f"  [mkdir] {rel}/")


def generate_upstream_phases(to_display: str) -> str:
    """Generate a markdown reference file listing all prior phases, methodology,
    and synthesis papers with SSRN IDs for bibliography cross-citation."""
    lines = [
        f"# Upstream Phases — citation reference for {to_display}",
        "",
        "Copy these into the paper bibliography. Every phase paper cites all prior phases",
        "plus the full methodology chain.",
        "",
        "## Phase papers",
        "",
    ]
    for phase, entry in PHASE_SSRN_REGISTRY.items():
        if phase >= to_display:
            break
        # Entry is a legacy 2-tuple (substrate, ssrn_id) or a dict with an optional
        # title/short_title. A title, when present, replaces the legacy
        # "AI Presence in {substrate}" descriptor; otherwise the template renders
        # (so v0.16–v0.29 are unaffected).
        if isinstance(entry, dict):
            substrate = entry.get("substrate", "")
            ssrn_id = entry["ssrn_id"]
            descriptor = (entry.get("title") or entry.get("short_title")
                          or f"AI Presence in {substrate}")
        else:
            substrate, ssrn_id = entry
            descriptor = f"AI Presence in {substrate}"
        lines.append(
            f"- González Castro, P. U. (2026). *{descriptor}: "
            f"AIAS {phase}*. Working Paper. SSRN {ssrn_id}. "
            f"https://ssrn.com/abstract={ssrn_id}"
        )
    lines += ["", "## Methodology papers", ""]
    for ver, (title, ssrn_id) in METHODOLOGY_SSRN_REGISTRY.items():
        lines.append(
            f"- González Castro, P. U. (2026). *{title}*. "
            f"AIAS Protocol {ver}. SSRN {ssrn_id}. "
            f"https://ssrn.com/abstract={ssrn_id}"
        )
    lines += ["", "## Synthesis papers", ""]
    for ver, (title, ssrn_id) in SYNTHESIS_SSRN_REGISTRY.items():
        lines.append(
            f"- González Castro, P. U. (2026). *{title}*. "
            f"{ver}. SSRN {ssrn_id}. "
            f"https://ssrn.com/abstract={ssrn_id}"
        )
    lines += ["", "## Foundational", ""]
    title, ssrn_id = FOUNDATIONAL_SSRN
    lines.append(
        f"- González Castro, P. U. (2025). *{title}*. "
        f"SSRN {ssrn_id}. https://ssrn.com/abstract={ssrn_id}"
    )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold a new AIAS phase by cloning the prior phase's build pipeline."
    )
    parser.add_argument("--from", dest="from_v", required=True,
                        help="Prior phase version, e.g. 'v0.22'")
    parser.add_argument("--to", dest="to_v", required=True,
                        help="New phase version, e.g. 'v0.23'")
    parser.add_argument("--substrate", required=True,
                        help="Substrate name, e.g. 'luxury watches' or 'premium spirits'")
    parser.add_argument("--substrate-slug", default=None,
                        help="Filename-safe slug. Default: derived from --substrate.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be written without writing.")
    parser.add_argument("--root", default=str(AIAS_ROOT),
                        help=f"AIAS project root. Default: {AIAS_ROOT}")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.exists():
        print(f"ERROR: AIAS root not found: {root}", file=sys.stderr)
        return 2

    from_display, from_snake_full, from_snake_short, _ = parse_version(args.from_v)
    to_display, to_snake_full, to_snake_short, _ = parse_version(args.to_v)
    substrate_slug = args.substrate_slug or slugify(args.substrate)

    # Detect prior substrate slug from existing content module filename.
    # e.g. reports/v23_premium_spirits_content.py → "premium_spirits"
    prior_content_files = list((root / "reports").glob(
        f"{from_snake_short}_*_content.py"))
    prior_content_files = [p for p in prior_content_files
                           if not p.name.startswith("_")]
    from_substrate_slug = ""
    if prior_content_files:
        # Extract slug: strip version prefix and _content.py suffix
        fname = prior_content_files[0].stem  # e.g. "v23_premium_spirits_content"
        prefix = from_snake_short + "_"      # e.g. "v23_"
        suffix = "_content"
        if fname.startswith(prefix) and fname.endswith(suffix):
            from_substrate_slug = fname[len(prefix):-len(suffix)]

    version_args = dict(
        from_display=from_display, to_display=to_display,
        from_snake_full=from_snake_full, to_snake_full=to_snake_full,
        from_snake_short=from_snake_short, to_snake_short=to_snake_short,
        from_substrate_slug=from_substrate_slug,
        to_substrate_slug=substrate_slug,
    )

    print(f"[aias_new_phase] scaffolding {to_display} from {from_display}")
    print(f"  substrate: {args.substrate!r}  (slug: {substrate_slug!r})")
    if from_substrate_slug:
        print(f"  prior substrate slug: {from_substrate_slug!r} → {substrate_slug!r}")
    print(f"  root: {root}")
    print(f"  version map: {from_display}→{to_display}, "
          f"{from_snake_full}→{to_snake_full}, "
          f"{from_snake_short}→{to_snake_short}")
    print()

    # ----- Discover prior-phase content files (already found above) -----
    prior_substrate_content = prior_content_files
    prior_substrate_prereg = list((root / "prereg").glob(
        f"{from_snake_full}_*_content.py"))

    # ----- Clone build pipeline files (version strings swapped) -----
    print("[1/6] Cloning build pipeline scripts...")
    pipeline_files = [
        (root / "scripts" / f"build_charts_{from_snake_short}.py",
         root / "scripts" / f"build_charts_{to_snake_short}.py"),
        (root / "scripts" / f"build_paper_{from_snake_full}.py",
         root / "scripts" / f"build_paper_{to_snake_full}.py"),
        (root / "reports" / f"build_report_{from_snake_short}.py",
         root / "reports" / f"build_report_{to_snake_short}.py"),
    ]
    for src, dst in pipeline_files:
        clone_file(src, dst, version_args, root=root, dry_run=args.dry_run)

    # ----- Clone content modules with substrate rename -----
    print("\n[2/6] Cloning content modules...")
    if prior_substrate_content:
        src = prior_substrate_content[0]
        dst = root / "reports" / f"{to_snake_short}_{substrate_slug}_content.py"
        clone_file(src, dst, version_args, root=root, dry_run=args.dry_run)
        if not args.dry_run:
            # Annotate: this is a clone, fill in NEW content
            content = dst.read_text(encoding="utf-8")
            banner = (f"# NOTE: cloned from {src.name} on phase scaffold.\n"
                      f"# All COVER, STANDFIRST, LEAD_DECK, EXEC_SUMMARY, PATTERNS,\n"
                      f"# LIMITATIONS, WHATS_NEXT, HYPOTHESIS_DETAILS, CLOSING text\n"
                      f"# must be re-written for the {to_display} {args.substrate}\n"
                      f"# substrate. Do not ship this file as-is.\n\n")
            dst.write_text(banner + content, encoding="utf-8")
    else:
        print(f"  [skip] no prior content module found for {from_snake_short}")

    if prior_substrate_prereg:
        src = prior_substrate_prereg[0]
        dst = root / "prereg" / f"{to_snake_full}_{substrate_slug}_content.py"
        clone_file(src, dst, version_args, root=root, dry_run=args.dry_run)

    # ----- Clone mega-prompt -----
    print("\n[3/6] Cloning mega-prompt...")
    mp_src = root / "prereg" / f"{from_snake_full}_mega_prompt.md"
    mp_dst = root / "prereg" / f"{to_snake_full}_mega_prompt.md"
    clone_file(mp_src, mp_dst, version_args, root=root, dry_run=args.dry_run)

    # ----- Clone SSRN paper draft and submission packet (templates) -----
    print("\n[4/6] Cloning SSRN paper draft + submission packet templates...")
    paper_src = root / "papers" / from_snake_full / f"{from_snake_full}_ssrn_paper_draft.md"
    paper_dst = root / "papers" / to_snake_full / f"{to_snake_full}_ssrn_paper_draft.md"
    clone_file(paper_src, paper_dst, version_args, root=root, dry_run=args.dry_run)

    packet_src = root / "papers" / from_snake_full / f"ssrn_submission_packet_{from_snake_full}.md"
    packet_dst = root / "papers" / to_snake_full / f"ssrn_submission_packet_{to_snake_full}.md"
    clone_file(packet_src, packet_dst, version_args, root=root, dry_run=args.dry_run)

    # ----- Generate upstream-phases citation reference -----
    upstream_path = root / "papers" / to_snake_full / "_upstream_phases.md"
    upstream_content = generate_upstream_phases(to_display)
    if args.dry_run:
        print(f"  [dry-run] would write: papers/{to_snake_full}/_upstream_phases.md  "
              f"({len(upstream_content):,} chars)")
    else:
        upstream_path.parent.mkdir(parents=True, exist_ok=True)
        upstream_path.write_text(upstream_content, encoding="utf-8")
        print(f"  [write] papers/{to_snake_full}/_upstream_phases.md")

    # ----- Create directory tree for new phase -----
    print("\n[5/6] Creating directory tree...")
    dirs_to_create = [
        root / "papers" / to_snake_full,
        root / "reports" / "figs" / to_snake_short,
        root / "osf" / to_snake_short,
        root / "osf" / to_snake_short / "data",
        root / "osf" / to_snake_short / "prereg",
        root / "osf" / to_snake_short / "reports",
        root / "osf" / to_snake_short / "figures",
        root / "osf" / to_snake_short / "scripts",
        root / "osf" / to_snake_short / "registries",
    ]
    for d in dirs_to_create:
        ensure_dir(d, root=root, dry_run=args.dry_run)

    # ----- Write OSF README placeholder -----
    print("\n[6/6] Writing OSF README placeholder...")
    osf_readme = root / "osf" / to_snake_short / "README.md"
    readme_content = (
        f"# AIAS {to_display} — {args.substrate.title()}\n\n"
        f"OSF deposit for AIAS™ Presence Measurement Protocol, {to_display}.\n\n"
        f"**Status:** scaffolded by `aias_new_phase.py` on phase kickoff. "
        f"Pre-registration not yet locked; acquisition not yet run.\n\n"
        f"## Tree\n\n"
        f"- `data/` — Phase A and Phase B acquisition CSVs\n"
        f"- `prereg/` — locked pre-registration artifacts (content module + mega-prompt)\n"
        f"- `reports/` — brand-format report PDF\n"
        f"- `figures/` — chart PDFs (chart_01..04)\n"
        f"- `scripts/` — scoring code\n"
        f"- `registries/` — locked 24-brand registry\n\n"
        f"## Pipeline\n\n"
        f"1. Author pre-registration in `prereg/{to_snake_full}_{substrate_slug}_content.py`\n"
        f"2. Lock at git tag `{to_display}-prereg-r1`\n"
        f"3. Run acquisition: `python3 scripts/run_acquisition_{to_snake_short}.py`\n"
        f"4. Score: `python3 scripts/score_{to_snake_short}.py`\n"
        f"5. Build report: `python3 reports/build_report_{to_snake_short}.py`\n"
        f"6. Build SSRN paper: `python3 scripts/build_paper_{to_snake_full}.py`\n"
        f"7. Submit per `papers/{to_snake_full}/ssrn_submission_packet_{to_snake_full}.md`\n"
        f"8. Final OSF deposit: `python3 ~/aias/scripts/osf_upload.py "
        f"~/aias/osf/{to_snake_short} {to_snake_short}`\n"
    )
    if args.dry_run:
        print(f"  [dry-run] would write README at {osf_readme}")
    else:
        osf_readme.write_text(readme_content, encoding="utf-8")
        print(f"  [write] osf/{to_snake_short}/README.md")

    # ----- Summary + next steps -----
    print()
    print(f"[aias_new_phase] ✓ {to_display} scaffold "
          f"{'WOULD BE ' if args.dry_run else ''}complete.")
    print()
    print("Next steps:")
    print(f"  1. Author pre-registration:")
    print(f"     $ $EDITOR prereg/{to_snake_full}_{substrate_slug}_content.py")
    print(f"     $ $EDITOR prereg/{to_snake_full}_mega_prompt.md")
    print(f"  2. Lock at git tag:")
    print(f"     $ git add prereg/ && git commit -m '{to_display} pre-reg r1'")
    print(f"     $ git tag {to_display}-prereg-r1")
    print(f"  3. Run acquisition (manual step, populates Phase A/B CSVs)")
    print(f"  4. Score → verdicts → report → paper, fully automated downstream")

    return 0


if __name__ == "__main__":
    sys.exit(main())
