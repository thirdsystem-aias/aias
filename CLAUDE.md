# AIAS™ Measurement Program — Project Context for Claude Code

This file gives Claude Code persistent context for the AIAS™ Presence Measurement Protocol research program. Loaded at session start.

---

## Identity & affiliation

**Author:** Pablo Ulpiano González Castro (accent on the á)

**Primary academic affiliation:** School of Visual Arts, MPS Branding Program, New York, NY
**Secondary research entity:** Third System™ (research entity; data archive and methodology venue)
**Employment:** Samsung Electronics America (Director, Corporate Brand Creative & Governance)

### Samsung COI rule — non-negotiable

Samsung is disclosed **only in Declarations §COI** of formal papers. **Never** in author blocks, affiliations, or front-matter. Pre-acquisition COI screen per phase is documented as DEVIATIONS Entry 0 (confirming no brand in the panel is Samsung-affiliated).

### Standard SSRN/paper author block

```
Pablo Ulpiano González Castro
School of Visual Arts, MPS Branding Program, New York, NY (primary academic affiliation)
Third System™ (research entity; data archive and methodology venue)
Correspondence: pablou@pablou.com · pablou.com
ORCID: 0009-0003-8968-9990 (linked: https://orcid.org/0009-0003-8968-9990)
```

### Trademark convention

Place ™ superscript after **"Third System"** and **"AIAS"** on first prominent mention in formal documents, papers, proposals, applications, and websites. Subsequent mentions in the same document are unmarked. Do not use ™ in casual conversation, internal notes, or after the first marked use within the same document.

---

## Repo layout

```
~/aias/
├── scripts/             # acquisition runners, scorers, osf_upload.py
├── papers/v0_NN/        # SSRN academic papers per phase
├── papers/methodology/  # v1.N methodology papers (paths TBD per increment)
├── reports/             # Third System brand-format managerial PDFs
├── reports/figs/v21/    # chart PDFs per phase
├── osf/v21/             # OSF staging tree (Phase A, Phase B, verdicts, registries)
├── brand/               # third_system_brand.json (Indigo #37237B primary)
└── methodology/v1_N/    # methodology paper drafts + outlines
```

Build outputs land under their respective subdirs. Never write to `/Users/pablou/Downloads`.

---

## Current state (May 2026)

- **Latest phase shipped:** v0.21 cosmetics (SSRN 6815378, May 2026)
  - 5-substrate-family anchor base now complete (kitchenware, fragrance, audio, skincare, cosmetics)
  - Type 2 quadrant cleared EMERGED threshold for first time
  - Phantom Brand Persistence reached strongest demonstration (Glossier 6/6 q6)
- **Latest methodology paper shipped:** v1.6 (SSRN 6816340, May 2026)
  - Three increments: substrate-level Recognition pre-screen, independent moderator pathway (`H_IdentityLoad_Direct`), Phantom Brand Persistence Phase B extension
  - Retrospective scoring against v0.16–v0.21 corpus; v0.21 returned CONFIRMED for both `H_IdentityLoad_Direct` and `H_PhantomBrandPersistence` (Glossier validity anchor passed at R_phantom = 12)
  - Pre-reg tag `v1.6-prereg-r1` (commit `f10616a`); OSF deposit at `osf.io/ec6wh/methodology/v1_6/`
- **Active next deliverable:** AIAS™ 1.0 synthesis paper consolidating the 5-family anchor base under locked v1.6 methodology

---

## Pre-registration discipline — non-negotiable

Every phase follows this ship sequence:

1. **Pre-registration** at git commit, tag `v0.NN-prereg-rN`. Locks panel, hypotheses, decision rules, verdict matrices, probe wording. Nothing else proceeds until this is in.
2. **Acquisition** (Phase A 144 probes + Phase B 36 queries against locked panel). Tag `v0.NN-acquisition-locked` after acquisition is complete.
3. **Canonical scoring + hypothesis verdict resolution** via `score_vNN.py`. Verdicts JSON to `~/aias/osf/vNN/`.
4. **Third System brand-format report PDF** (managerial register; ReportLab + Akkurat Pro).
5. **SSRN academic paper** (academic register; pandoc + xelatex + Carlito).
6. **OSF deposit** at `osf.io/ec6wh/vNN/` via `~/aias/scripts/osf_upload.py`.
7. **SSRN webform submission** → returns abstract ID (1–3 business days).
8. **Cross-citation backfill** in dependent papers (Tri-System MSI WP, Routledge monograph).

For methodology papers (v1.N): no new acquisition; retrospective scoring against existing phase corpus. Same pre-reg discipline at git tag `v1.N-prereg-rN`.

---

## Two-register discipline — non-negotiable

The same phase findings are written in **two intentionally divergent registers**:

- **Academic register** (SSRN papers): formal H1/H2 hypothesis framing, ex-ante verdict matrices, methodology lineage, full citation chain. Standard scholarly voice.
- **Managerial register** (Third System brand-format reports): P1–P5 propositional framing, executive-readable, brand-strategy framing. No academic hypothesis labels.

These are **not inconsistent**. They are different registers for different audiences. Do not collapse them into a single artifact, and do not let academic-paper voice leak into report content (or vice versa).

---

## Build pipelines

### Report build (ReportLab + pypdf two-pass)

Per-phase three-file set in `~/aias/reports/`:

- `build_report_vNN.py` — main builder; Pass 1 layouts body with chart slot reservations; Pass 2 overlays chart PDFs at locked figsize
- `vNN_<topic>_content.py` — content module (STANDFIRST, EXEC_SUMMARY, PATTERNS, HYPOTHESIS_DETAILS, LIMITATIONS, WHATS_NEXT)
- `build_charts_vNN.py` — matplotlib chart builder; outputs chart_NN.pdf to `~/aias/reports/figs/vNN/`

**Font:** Akkurat Pro from `~/.fonts/Akkurat` and `~/Library/Fonts`, auto-detected. Register via `matplotlib.font_manager.fontManager.addfont()` at module top for charts; set `plt.rcParams['font.family']=['Akkurat Pro','sans-serif']`.

**Brand tokens:** `~/aias/brand/third_system_brand.json`. Primary: Indigo #37237B.

**Typography (Akkurat lacks subscript glyphs ₁/₂):** Subscripts via `<sub size='6'>1</sub>` markup (body) or `<sub size='10'>1</sub>` (cover/18pt). Do **not** add `rise='-N'` — default sub position is correct. Wrap arrow connectors with `\u00a0` (NBSP) to prevent line-splits.

### SSRN paper build (pandoc + xelatex + Carlito)

Per-phase two-file set in `~/aias/papers/v0_NN/`:

- `build_paper_vNN.py` — thin pandoc wrapper; applies defensive Unicode→LaTeX substitutions for Carlito glyph gaps; outputs PDF
- `v0_NN_ssrn_paper_draft.md` — paper body with YAML preamble

**YAML preamble standard:** `mainfont: Carlito`, `fontsize: 11pt`, `geometry: [letterpaper, margin=1in]` (added v0.21+), `\setstretch{1.36}`, `\parskip 8pt`, `\parindent 0pt`, float/caption/titlesec packages, `\renewcommand{\maketitle}{}` (suppresses pandoc's auto-maketitle).

**Titlepage block:** custom `\begin{titlepage}...\end{titlepage}` at body start. Always add `\setstretch{1.0}` AND `\setlength{\parskip}{0pt}` locally inside the block to override global preamble — without these the titlepage inflates ~35% and bleeds to page 2.

**Figure references:** `![cap](../../reports/figs/vNN/chart_NN.pdf){#fig:label width=100%}`. Pandoc needs `--resource-path=papers/v0_NN` flag.

**Carlito glyph-gap substitution dict** (canonical, in build_paper_vNN.py):

| Char | LaTeX |
|---|---|
| ₜ U+209C | `$_{t}$` |
| ∈ U+2208 | `$\in$` |
| ∧ U+2227 | `$\wedge$` |
| ∶ U+2236 | `$:$` |
| ⊆ U+2286 | `$\subseteq$` |
| ✓ U+2713 | `\checkmark` |
| ✗ U+2717 | `$\times$` |
| ▶ U+25B6 | `$\blacktriangleright$` |
| ⁻ U+207B | `-` (rewrite compounds like `10⁻⁴` to decimal in source) |
| ⁰¹²³⁴⁵⁶⁷⁸⁹ | `$^{N}$` |

Add to dict on every new gap surfaced by xelatex `Missing character` warnings.

### Acquisition runner

`~/aias/scripts/run_acquisition_vNN.py` — calls the 6-LLM panel (Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o-mini, Gemini 2.5 Flash, Gemini 2.5 Flash Lite) for both phases. Probe template + Phase B frames read dynamically from registry JSON. Outputs `phase_a_results.csv` (144 rows) and `phase_b_results.csv` (36 rows). Note: `google.generativeai` package deprecated; migrate to `google.genai` at v0.22.

### Scorer

`~/aias/scripts/score_vNN.py` — applies locked methodology version (currently v1.5; v1.6 in development). Outputs `vNN_verdicts.json` with the four hypothesis verdicts and supporting statistics.

### OSF upload (patched v0.21 for nested paths)

`~/aias/scripts/osf_upload.py` — recursive uploader against WaterButler API. Project ID `ec6wh` hardcoded. Requires `OSF_TOKEN` env var with `osf.full_write` scope. Supports nested destination paths (e.g. `v21/figures`); each path component is created in sequence since WaterButler 500s on nested PUT.

Usage: `python ~/aias/scripts/osf_upload.py <local_dir> <remote_path>`. Standard deposit pattern per phase: `vNN/figures`, `vNN/paper`, `vNN/report`, `vNN/scoring`.

---

## Methodology citation chain (canonical)

Cite **all five** methodology papers in every phase paper's bibliography:

- v1.2 — *Methodological Notes on Construct Validity and the Four-Regime Taxonomy*. SSRN 6761698.
- v1.3 — *Phase A Pivot-Validation Specification*. SSRN 6797679.
- v1.4 — *Recognition × Recall Decomposition and Multi-Component AI Availability*. SSRN 6799479.
- v1.5 — *Multi-Statistic C2 and Two-Channel Recall Decomposition*. SSRN 6810758.
- v1.6 — *Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension*. SSRN 6816340.

Foundational: *Tri-System Brand Growth* (SSRN 6659000).

---

## Phase SSRN ID registry

| Phase | Substrate | SSRN ID |
|---|---|---|
| v0.16 | Kitchen knives | 6791999 |
| v0.17 | Premium kitchenware | 6802261 |
| v0.18 | Indie fragrance | 6806558 |
| v0.19 | Audiophile headphones | 6809182 |
| v0.20 | Skincare | 6811441 |
| v0.21 | Cosmetics | 6815378 |
| — methodology papers — | | |
| v1.6 | Three increments (Recognition regime, IL Direct, Phantom) | 6816340 |

URL pattern: `https://ssrn.com/abstract={ID}`. New phase papers cite **all prior phases** plus the methodology chain.

---

## SSRN submission packet template (Step 3 metadata)

- **Keywords:** semicolon-separated. Always include: `AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass`. Add 5–7 phase-specific keywords.
- **JEL primary:** M31. Secondary: L86, L15, D83, M37.
- **eJournals (up to 7):** Marketing; Marketing Strategy; Consumer Behavior; Advertising & Marketing Communications; Information Systems & eBusiness; Artificial Intelligence; Decision-Making Under Risk & Uncertainty.
- **Funder:** Self-funded.
- **Ethics:** Not applicable; no human subjects.

---

## Chart conventions (matplotlib)

Editorial layout per `build_charts_vNN.py`:

- Title: **bold top-left**
- Subtitle: gray below title
- Thin Indigo (#37237B) horizontal separator rule
- Source line: *italic gray* at bottom, citing upstream SSRN IDs and pre-reg tag
- Akkurat Pro font registered at module top

Cell color convention (cumulative across phases):

- Cell A: Indigo (#37237B), prestige/heritage tier
- Cell B: Purple/violet, celebrity-DTC/cult tier (high IL)
- Cell C: Cyan/light blue, drugstore/mass tier (low IL)

---

## Working preferences

- **Single unified build pipelines, no toggles.** Strong preference across all deliverables.
- **Surgical precision over broad rewrites.** Edits scoped tightly. Always verify scope before executing major changes.
- **Phase copy pattern:** copy prior build files with new version prefix, new registry, pre-reg locked at git commit before measurement. Prior phases left untouched.
- **No emojis, no excessive bolding, no breathless tone** in deliverables. Direct, declarative voice. Reports are managerial; papers are academic; neither is salesy.

---

## When in doubt

- The v1.6 outline (`~/aias/methodology/v1_6/aias_v1_6_outline.md`) is the active planning artifact for the next paper. Read it first when working on v1.6.
- Prior phase deliverables (`~/aias/papers/v0_21/`, `~/aias/reports/v21_*`) are the structural template for new phase work.
- The 5 decisions in the v1.6 outline gate drafting. Resolve those before producing draft prose.

---

*This file is the AIAS program's constitution for Claude Code sessions. Update when conventions change, when new phases ship (extend the SSRN registry), or when build pipelines evolve.*
