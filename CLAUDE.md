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
├── papers/aias_1_0/     # AIAS™ 1.0 synthesis paper (five-substrate foundational construct claim)
├── papers/tri_system/   # Tri-System™ MSI WP (foundational architectural paper, in-repo since AIAS 1.0 cycle)
├── reports/             # Third System™ brand-format managerial PDFs
├── reports/figs/vNN/    # per-phase chart PDFs
├── reports/figs/aias_1_0/ # synthesis-paper chart PDFs
├── osf/vNN/             # per-phase OSF staging tree (Phase A, Phase B, verdicts, reports)
├── osf/aias_1_0/        # synthesis-paper OSF staging tree
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
- **Latest methodology paper shipped:** v1.7 CPC Consistency (SSRN 6878818, June 2026) — pre-registered **negative result**
  - CV-based Consistency (CPC = 1/(1+CV) of cross-model recall) is **not independent of Presence**: pooled |ρ| = 0.77 > 0.50 ceiling, per-substrate +0.94/+0.85/+0.64; mechanical CV ≈ 1/√mean coupling at recall counts r∈0–6. Instrument **not adopted**; redefinition escalated to v1.8. H_CPC_PhantomNull confirmed; H_CPC_Defined falsified (57% defined-rate, recognition–recall gap).
  - Anchored set v0.20–v0.22 (two-channel canonical trio); tags `v1.7-prereg-r1/r2/r3` (r2 scope-narrow, r3 falsification record); OSF deposit at `osf.io/ec6wh/methodology/v1_7/`
- **Prior methodology paper:** v1.6 (SSRN 6816340, May 2026)
  - Three increments: substrate-level Recognition pre-screen, independent moderator pathway (`H_IdentityLoad_Direct`), Phantom Brand Persistence Phase B extension
  - Retrospective scoring against v0.16–v0.21 corpus; v0.21 returned CONFIRMED for both `H_IdentityLoad_Direct` and `H_PhantomBrandPersistence` (Glossier validity anchor passed at R_phantom = 12)
  - Pre-reg tag `v1.6-prereg-r1` (commit `f10616a`); OSF deposit at `osf.io/ec6wh/methodology/v1_6/`
- **Latest synthesis paper shipped:** AIAS™ 1.0 (SSRN 6817841, May 2026) — *AI Availability as a Third Measurable Layer of Brand Availability: Five-Substrate Empirical Anchoring of the AIAS™ Presence Measurement Protocol*
  - Consolidates the 5-family anchor base (v0.16–v0.21) under locked v1.6 methodology
  - Seven-layer construct claim L1–L7; L7 carries the Presence-only-with-multi-year-composite-roadmap positioning
  - Cross-phase synthesis-layer contribution: La Mer (v0.20 Cell A) + e.l.f. Cosmetics (v0.21 Cell C) establish out-of-cell Type 2 as a recurrent feature of the dissociation framework
  - Lock tags `aias-1-0-outline-locked` (36918dc) / `aias-1-0-data-locked` (7298411) / `aias-1-0-charts-locked` (5f6bf70) / `aias-1-0-paper-locked` (bdae263); OSF deposit at `osf.io/ec6wh/aias_1_0/`
- **Latest brand-format report shipped:** AIAS 1.0 Third System brand-format synthesis report (May 2026, 22 pages)
  - Three lock revisions: r1 (`aias-1-0-report-locked`, a199b93 — broken layout, preserved for pre-reg lineage); r2 (`aias-1-0-report-locked-r2`, ccfb7fe — partial layout fixes, preserved for lineage); r3 (`aias-1-0-report-locked-r3`, fd89ee6 — chart-caption gap + P2/P4 orphan resolution; **shipping version**)
  - r3 resolved both remaining defects via a single root-cause fix to the report builder's ChartReservation pre-compute (see Build pipelines below). Deferred to future cycle: font glyph fallback for δ and ✓ in chart builder (cross-cuts SSRN paper); P5 vertical rhythm on the finding-tail page.
- **Active next deliverable:** JAR submission of AIAS™ 1.0 synthesis paper (2–3 sessions, async). After JAR ships, v0.22 prospective phase under v1.6 methodology lock.

### AIAS™ 1.0 ship state milestones

- Five-substrate empirical anchor base complete (kitchenware, fragrance, audio, skincare, cosmetics)
- Six phase papers shipped (v0.16 → v0.21)
- Five methodology papers shipped (v1.2 → v1.6)
- Foundational construct claim staked under pre-registration discipline
- Construct validity + behavioral correlate held as Phase 3 future work
- Version-numbering discipline: AIAS™ 1.0 → 6.0 binds to measurement surface, not architectural ambition

### AIAS™ 1.0 cycle-close lock-tag inventory

| Tag | Commit | Status |
|---|---|---|
| `aias-1-0-outline-locked` | 36918dc | Outline lock |
| `aias-1-0-data-locked` | 7298411 | Synthesis data lock |
| `aias-1-0-charts-locked` | 5f6bf70 | Six figures lock |
| `aias-1-0-paper-locked` | bdae263 | Synthesis paper lock (SSRN 6817841) |
| `aias-1-0-report-locked` | a199b93 | Report r1 (original; broken layout, preserved for pre-reg lineage) |
| `aias-1-0-report-locked-r2` | ccfb7fe | Report r2 (partial fixes, preserved for lineage) |
| `aias-1-0-report-locked-r3` | fd89ee6 | Report r3 — **shipping version** |

All seven tags pushed to origin. r1 and r2 are preserved (not retagged or deleted) so the lineage from broken-layout to shipping is auditable; r3 is the canonical reference for any downstream citation of the brand-format report.

---

## Pre-flight discipline — non-negotiable

Every brand-format report render requires a page-by-page visual layout inspection of the rendered PDF before commit, tag, or OSF deposit. Numerical pre-flight (word counts, voice scans, citation completeness) catches content issues; visual pre-flight catches layout issues — orphan content, frame-iteration cascades, chart overflow, chart-caption gap. Both are required.

Established under the AIAS™ 1.0 brand-format report r1→r2→r3 cycle: r1 shipped with four layout defects that the numerical pre-flight passed cleanly. The r3 ChartReservation root-cause fix only became possible after page-by-page visual inspection surfaced the pattern across all four chart pages simultaneously.

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

**Figure sets may diverge by register (deliberate).** The report (managerial) is not bound to the paper's pre-registered confirmatory figure set; it may carry an extra *descriptive* figure that visualizes an already-locked tertiary/exploratory verdict, provided the framing stays deflationary and the styling stays neutral (non-green). Example: v0.33 ships 3 figures in the paper (the pre-registered confirmatory set) but 4 in the report — the 4th visualizes the descriptive H_Provider_Phantom verdict ("obscurity is mechanical, not a signature"). Nothing post-hoc or confirmatory is smuggled into the report by doing this.

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

**ChartReservation pre-compute pattern (locked at AIAS™ 1.0 r3):** Pass 1 reserves chart slots at known dimensions; Pass 2 overlays chart PDFs into those slots. `ChartReservation` must pre-compute the final chart-rendered footprint (width and height) by reading the chart PDF mediabox and applying the fit-to-clamps proportional scale *before* slot allocation. Clamps: `CHART_RESERVATION_WIDTH_CLAMP_PT = CONTENT_W`, `CHART_RESERVATION_HEIGHT_CLAMP_PT = 600.0` for synthesis-scale (v21 phase-scale used 500.0). Chart-overlay scale = 1.0 (slot is already sized to the chart; no padding correction needed). Eliminates chart-caption gap and chart-page heading orphans simultaneously — the two defects that drove the AIAS™ 1.0 r1→r2→r3 lineage.

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

**Local OSF staging convention.** The per-phase and synthesis-cycle OSF staging directories (`~/aias/osf/vNN/`, `~/aias/osf/aias_1_0/`) hold the upload-source files for OSF deposit, not a complete mirror of the deposit tree. Authoritative OSF state lives at `osf.io/ec6wh` — local staging may carry only the files newest to a given upload batch, not every file already in the deposit. To inspect OSF deposit completeness, query OSF directly (web UI or a read-only API call against `https://api.osf.io/v2/nodes/ec6wh/files/osfstorage/`). `osf_upload.py` is upload-only; it has no list/status mode. Source files (paper drafts, build scripts, content modules, chart builders) live at their canonical repo paths (`papers/`, `reports/`, `scripts/`) and are upload-sourced from there into staging at deposit time, not duplicated into local staging trees as authoritative copies.

---

## Methodology citation chain (canonical)

Cite **all five** methodology papers in every phase paper's bibliography:

- v1.2 — *The AIAS™ Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy*. SSRN 6761698.
- v1.3 — *The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification (v1.3)*. SSRN 6797679.
- v1.4 — *The AIAS Presence Measurement Protocol v1.4: Recognition × Recall Decomposition and Multi-Component AI Availability*. SSRN 6799479.
- v1.5 — *The AIAS™ Presence Measurement Protocol: Multi-Statistic C2 Specification and Two-Channel Recall Decomposition*. SSRN 6810758.
- v1.6 — *Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension*. SSRN 6816340.

Foundational: *AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval* (SSRN 6659000).

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
| v0.22 | Automotive | 6829118 |
| v0.23 | Premium spirits | 6834298 |
| v0.24 | B2B SaaS | 6838802 |
| v0.25 | B2B SaaS Construct Validity | 6842138 |
| v0.26 | Amazon BSR Discriminant Validity | 6847678 |
| v0.27 | B2B SaaS Convergent Validity | 6854758 |
| v0.28 | Tech BRAND Discriminant Validity (CV.04) | 6865478 |
| v0.29 | Presence Construct-Validity Baseline (CV.05) | 6870778 |
| v0.30 | Consistency Component Instrument Pilot (CPC.01) | 6875319 |
| v0.31 | CPC Cross-Category Baseline — 5-substrate omnibus, channel-agnostic generalization | 6880959 — WITHDRAWN (inactive on SSRN; inputs archived at OSF) |
| v0.32 | CPC Version-Snapshot Stability — two-arm cross-generation test (CPC version-robustness) | 6898581 |
| — methodology papers — | | |
| v1.6 | Three increments (Recognition regime, IL Direct, Phantom) | 6816340 |
| v1.7 | CPC Consistency — pre-registered negative result (CV not independent of Presence; redefinition escalated to v1.8) | 6878818 |
| — synthesis paper — | | |
| AIAS™ 1.0 | Five-Substrate Foundational Construct Claim | 6817841 |

URL pattern: `https://ssrn.com/abstract={ID}`. New phase papers cite **all prior phases** plus the methodology chain.

v0.27 B2B SaaS Convergent Validity — SSRN 6854758. H_CV3_Primary FALSIFIED (rho=0.29); recognition null CONFIRMED; exploratory PQ 0.80 / BR 0.75 (convergence is rank-alignment, not range restriction — corrected pre-deposit).

v0.28 Tech BRAND Discriminant Validity (CV.04) — SSRN 6865478. Discriminant test of AIAS Presence vs the BRAND human-norm database (familiarity 1–7, recognition d′) on a frozen 24-brand Technology panel (seed 280400). H_Disc_Recognition CONFIRMED (rho=0.379, |rho|<0.50, BCa CI upper 0.714 excludes the 0.74 reducibility threshold); H_Disc_Familiarity UNDETERMINED (rho=0.593, BCa CI [0.18, 0.83] spans all three bands at n=24); H_Dissociation FULL (descriptive). Presence pinned to v0.25 presence_composite at v1.6-canonical /18 recall (r2 Entry 2). Blind acquisition; one-shot scoring. Tags v0.28-prereg-r1/r2, -acquisition-locked, -results-locked.

v0.29 Presence Construct-Validity Baseline (CV.05) — SSRN 6870778. Synthesis (no acquisition): assembles the v0.25 convergent leg (Presence × Google Trends, rho=0.7411, p=3.4e-05, n=24) and the v0.26 discriminant leg (Presence × Amazon BSR, rho=−0.0002, p=0.998, n=88) into a single Campbell–Fiske MTMM frame. C3 = |rho_conv| − |rho_disc| = 0.7409 > 0 with significance asymmetry intact; H_CV_Baseline CONFIRMED. Predictive validity NOT claimed (DEVIATIONS Entry 0 — needs a longitudinal t1→t2 criterion, gated to a later wave). Prereg-only tag v0.29-prereg-r1 (no scoring-locked tag — deterministic synthesis, CV-family precedent). OSF osf.io/ec6wh/v29.

---

## SSRN submission packet template (Step 3 metadata)

- **Keywords:** semicolon-separated. Always include: `AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass`. Add 5–7 phase-specific keywords.
- **JEL primary:** M31. Secondary: L86, L15, D83, M37.
- **JEL label (paper body):** the inline bold label MUST read exactly `**JEL codes:**` — the `generate_ssrn_packet.py` extraction key. Never author `JEL:` or `JEL classification:` (the generator silently misses them).
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

- For program-level synthesis context, the AIAS™ 1.0 synthesis paper (`~/aias/papers/aias_1_0/aias_1_0_synthesis_paper_draft.md`) is the canonical statement of the five-substrate foundational construct claim and the L1–L7 seven-layer model.
- For architectural framing context, the Tri-System™ MSI WP (`~/aias/papers/tri_system/jar_tri_system_v0_2_draft.md`, with JAR double-anonymous variant alongside) is the foundational architectural paper.
- For new phase work, the v1.6 methodology paper (`~/aias/papers/v1_6/v1_6_ssrn_paper_draft.md`) is the active methodology lock.
- Structural templates: `~/aias/papers/v0_21/` and `~/aias/reports/build_report_v21.py` / `~/aias/reports/v21_cosmetics_content.py` for phase work; `~/aias/papers/aias_1_0/` and `~/aias/reports/build_report_aias_1_0.py` / `~/aias/reports/aias_1_0_content.py` for synthesis work.

---

*This file is the AIAS program's constitution for Claude Code sessions. Update when conventions change, when new phases ship (extend the SSRN registry), or when build pipelines evolve.*

## v0.29 (CV.05) — tag convention (DECIDED, not open)
v0.29 is prereg-only. No post-scoring lifecycle tag (no v0.29-scoring-locked).
Rationale: a synthesis with a deterministic verdict has no analytic degrees of
freedom past the prereg lock, and the CV-family precedent (v0.25, v0.26) is
prereg-tag-only. This is settled; do not re-surface it as an open item.
