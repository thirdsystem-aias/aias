#!/usr/bin/env python3
"""
v0.16 C_P Retrofit Acquisition
==============================
Re-run Phase A Recognition probes for the v0.16 kitchen-knives panel against
the 6-model reference panel introduced in v1.4+, to produce per-brand C_P on
the 0-6 integer scale used by v0.19/v0.20/v0.21.

Why
---
v0.16 was scored under methodology v1.2 (Google Trends + high-N LLM probes
summarized as percentages ai_t1_pct / ai_t2_pct over ai_t1_n=160 probes per
brand). The 6-model panel C_P (0-6 integer count of recognition across a
fixed reference panel) was introduced in v1.4. For v0.26 cross-substrate BSR
predictive validity, v0.16 brands need a v1.4+ C_P to be metric-comparable
with v0.19/v0.20/v0.21. This retrofit produces that data.

This is documented as a deviation; see DEVIATIONS.md Entry 0 for the v0.26
substrate pre-screen and the v0.16 retrofit rationale.

Convention
----------
Probe template structurally mirrors v0.19 verbatim (osf/v19/thresholds_v0_19.json
phase_a.probe_template), with the substrate descriptor substituted:

    "Is the brand [BRAND_NAME] commonly recognized as a brand of
     kitchen knives? Answer yes or no."

Yes/no parsing follows v0.19 regex verbatim (osf/v19/acquire_v0_19.py:247-248).
Provider calls go through the canonical protocol.providers module — same code
path used by v0.20+ acquisition runners.

Outputs
-------
    osf/v26/data/v16_cp_retrofit_responses.jsonl   raw per-probe responses (provenance)
    osf/v26/data/v16_cp_retrofit.csv               brand, model, recognition_yes (0/1)
    osf/v26/data/v16_cp_retrofit_aggregated.csv    brand, cp, n_models (derived)

Usage
-----
    # Inspect what would be queried (no API calls, no env vars needed):
    python3 scripts/acquire_v16_cp_retrofit.py --dry-run

    # Live run (requires ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY):
    python3 scripts/acquire_v16_cp_retrofit.py

    # Resume an interrupted run (skips (brand, model) combos already in CSV):
    python3 scripts/acquire_v16_cp_retrofit.py --resume

Estimated cost: ~156 probes (26 brands × 6 models), short prompts and short
responses. At ~$0.001-0.005 per call across the provider mix, total ~$0.20-1.00.
Wall time at --delay 2.0: ~5-10 minutes.
"""

import argparse
import csv
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Make protocol/ importable
AIAS_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AIAS_ROOT))
from protocol.providers import call_anthropic, call_openai, call_google  # noqa: E402

# -----------------------------------------------------------------------------
# Locked constants
# -----------------------------------------------------------------------------

SUBSTRATE_DESCRIPTOR = "kitchen knives"

# Structurally identical to v0.19 phase_a.probe_template; only the substrate
# descriptor changes. [BRAND_NAME] follows v0.19's placeholder convention.
PROBE_TEMPLATE = (
    "Is the brand [BRAND_NAME] commonly recognized as a brand of "
    "[SUBSTRATE_DESCRIPTOR]? Answer yes or no."
)

PANEL_REGISTRY = AIAS_ROOT / "registries" / "brands_kitchen_knives_v0.16.json"

# Include both panel-role and activated-alternate-role entries (Au Nain, Hengtai)
# to match the 26 brands actually queried in the v0.16 Phase A panel.
INCLUDE_ROLES = {"panel", "alternate"}

PANEL_MODELS = [
    "claude-opus-4-5",
    "claude-sonnet-4-5",
    "gpt-4o",
    "gpt-4o-mini",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
]

OUT_DIR = AIAS_ROOT / "osf" / "v26" / "data"
RESPONSES_JSONL = OUT_DIR / "v16_cp_retrofit_responses.jsonl"
RESULTS_CSV = OUT_DIR / "v16_cp_retrofit.csv"
AGGREGATED_CSV = OUT_DIR / "v16_cp_retrofit_aggregated.csv"

# v0.19 canonical yes/no regex (osf/v19/acquire_v0_19.py:247-248)
YES_RE = re.compile(r"\b(yes|yeah|yep|correct|affirmative|indeed)\b", re.I)
NO_RE = re.compile(r"\b(no|nope|not\s+(?:commonly\s+)?recognized|incorrect|negative)\b", re.I)


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def load_brands() -> list[str]:
    with open(PANEL_REGISTRY) as f:
        data = json.load(f)
    return [
        entry["display_name"]
        for entry in data["panel"]
        if entry.get("role", "panel") in INCLUDE_ROLES
    ]


def parse_yes_no(text: str) -> int | None:
    """Return 1 (yes), 0 (no), or None (ambiguous). v0.19 convention:
    first signal wins; if both present, earlier-in-string wins."""
    y = YES_RE.search(text)
    n = NO_RE.search(text)
    if y and n:
        return 1 if y.start() < n.start() else 0
    if y:
        return 1
    if n:
        return 0
    return None


def dispatch(model: str, prompt: str):
    if model.startswith("claude"):
        return call_anthropic(model, prompt)
    if model.startswith("gpt"):
        return call_openai(model, prompt)
    if model.startswith("gemini"):
        return call_google(model, prompt)
    raise ValueError(f"Unknown model: {model}")


def load_completed(path: Path) -> set[tuple[str, str]]:
    if not path.exists():
        return set()
    done = set()
    with open(path) as f:
        for row in csv.DictReader(f):
            done.add((row["brand"], row["model"]))
    return done


def write_aggregated(results_csv: Path, out_csv: Path) -> list[tuple[str, int, int]]:
    """Aggregate: C_P = sum(recognition_yes) per brand across panel models."""
    by_brand: dict[str, list[int]] = {}
    with open(results_csv) as f:
        for row in csv.DictReader(f):
            by_brand.setdefault(row["brand"], []).append(int(row["recognition_yes"]))
    rows = [(brand, sum(vals), len(vals)) for brand, vals in by_brand.items()]
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["brand", "cp", "n_models"])
        for r in rows:
            w.writerow(r)
    return rows


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="v0.16 C_P retrofit acquisition (v1.4+ panel)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print probes that would be issued; make no API calls")
    parser.add_argument("--resume", action="store_true",
                        help="Skip (brand, model) combos already present in results CSV")
    parser.add_argument("--delay", type=float, default=2.0,
                        help="Seconds between API calls (default 2.0)")
    parser.add_argument("--substrate-descriptor", default=SUBSTRATE_DESCRIPTOR,
                        help=f"Substrate phrase inserted into probe (default {SUBSTRATE_DESCRIPTOR!r})")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    brands = load_brands()
    probe_template = PROBE_TEMPLATE.replace("[SUBSTRATE_DESCRIPTOR]", args.substrate_descriptor)
    total_probes = len(brands) * len(PANEL_MODELS)

    print("v0.16 C_P retrofit acquisition")
    print(f"  panel registry:      {PANEL_REGISTRY.relative_to(AIAS_ROOT)}")
    print(f"  brands (incl. alts): {len(brands)}")
    print(f"  panel models:        {len(PANEL_MODELS)}  ({', '.join(PANEL_MODELS)})")
    print(f"  total probes:        {total_probes}")
    print(f"  probe template:      {probe_template!r}")
    print(f"  results CSV:         {RESULTS_CSV.relative_to(AIAS_ROOT)}")
    print(f"  responses JSONL:     {RESPONSES_JSONL.relative_to(AIAS_ROOT)}")
    print(f"  dry-run:             {args.dry_run}")
    print(f"  resume:              {args.resume}")
    print()

    completed = load_completed(RESULTS_CSV) if args.resume else set()
    if completed:
        print(f"  resume: {len(completed)} combos already in CSV; skipping those")
        print()

    if args.dry_run:
        print("--- DRY RUN: probes that would be issued ---")
        for b in brands:
            print(f"  {probe_template.replace('[BRAND_NAME]', b)!r}")
        print(f"\n  ({len(brands)} brands × {len(PANEL_MODELS)} models = {total_probes} total probes)")
        return

    # CSV header on first creation
    is_new_csv = not RESULTS_CSV.exists()
    csv_mode = "w" if is_new_csv else "a"
    jsonl_mode = "w" if not RESPONSES_JSONL.exists() else "a"

    n_done = 0
    n_skip = 0
    n_fail = 0
    n_ambiguous = 0

    with open(RESULTS_CSV, csv_mode, newline="") as cf, open(RESPONSES_JSONL, jsonl_mode) as jf:
        writer = csv.writer(cf)
        if is_new_csv:
            writer.writerow(["brand", "model", "recognition_yes"])

        for brand in brands:
            for model in PANEL_MODELS:
                if (brand, model) in completed:
                    n_skip += 1
                    continue

                probe = probe_template.replace("[BRAND_NAME]", brand)
                query_id = f"phase_a__{slug(brand)}__{model}"
                idx = n_done + 1
                print(f"  [{idx:3d}/{total_probes - n_skip}] {brand:30s} × {model:25s} … ", end="", flush=True)

                t0 = time.monotonic()
                try:
                    resp = dispatch(model, probe)
                    response_text = resp["raw_response"]
                    tokens_in = resp.get("tokens_in")
                    tokens_out = resp.get("tokens_out")
                    latency_ms = resp.get("latency_ms")
                except Exception as e:
                    latency_ms = int((time.monotonic() - t0) * 1000)
                    print(f"FAIL  ({type(e).__name__}: {e})")
                    n_fail += 1
                    jf.write(json.dumps({
                        "query_id": query_id,
                        "phase": "A",
                        "panel_model": model,
                        "brand": brand,
                        "probe": probe,
                        "response": "",
                        "error": f"{type(e).__name__}: {e}",
                        "latency_ms": latency_ms,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }) + "\n")
                    jf.flush()
                    time.sleep(args.delay)
                    continue

                recognition_yes = parse_yes_no(response_text or "")

                # Provenance: write raw to JSONL
                jf.write(json.dumps({
                    "query_id": query_id,
                    "phase": "A",
                    "panel_model": model,
                    "brand": brand,
                    "probe": probe,
                    "response": response_text,
                    "recognition_yes": recognition_yes,
                    "latency_ms": latency_ms,
                    "tokens_in": tokens_in,
                    "tokens_out": tokens_out,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }) + "\n")
                jf.flush()

                # Parsed result: write 0/1 to CSV. Ambiguous treated as 0 with a
                # stdout flag; the raw response is preserved in JSONL for audit.
                if recognition_yes is None:
                    n_ambiguous += 1
                    print(f"AMBIG (parsed→0); resp={response_text[:60]!r}")
                    writer.writerow([brand, model, 0])
                else:
                    label = "YES" if recognition_yes else "NO "
                    print(f"{label}  ({latency_ms} ms)")
                    writer.writerow([brand, model, recognition_yes])
                cf.flush()

                n_done += 1
                time.sleep(args.delay)

    print()
    print(f"  done: {n_done}   skipped (resume): {n_skip}   failed: {n_fail}   ambiguous (→0): {n_ambiguous}")

    # Aggregate
    rows = write_aggregated(RESULTS_CSV, AGGREGATED_CSV)
    print(f"\n  aggregated C_P per brand → {AGGREGATED_CSV.relative_to(AIAS_ROOT)}")
    print(f"\n  brand C_P summary:")
    for brand, cp, n in sorted(rows, key=lambda r: (-r[1], r[0])):
        print(f"    {brand:30s}  C_P = {cp} / {n}")

    if n_ambiguous:
        print(f"\n  ⚠  {n_ambiguous} ambiguous response(s) coded as 0 (no recognition).")
        print(f"     Review raw responses in {RESPONSES_JSONL.relative_to(AIAS_ROOT)}")
        print(f"     and reclassify manually if non-trivial.")


if __name__ == "__main__":
    main()
