# AIAS™ Presence Measurement Protocol — v0.18 Indie Fragrance / IL-Gradient

**Phase tag:** `v0.18-prereg-r1` at commit `183386c` (revised through r4 at `1195cb8`) on branch `v0.18-il-gradient`
**Methodology base:** AIAS™ Presence Measurement Protocol v1.4 (SSRN 6799479)
**SSRN paper:** *forthcoming*
**Date:** May 2026
**Author:** Pablo Ulpiano González Castro · pablou@pablou.com · ORCID 0009-0003-8968-9990

---

## Phase summary

v0.18 tests two pre-registered hypotheses orthogonally on a single substrate:

1. **The three-leg joint Identity-Load moderator hypothesis** closing the AMBIGUOUS verdict left by v0.16 PARTIAL (SSRN 6791999) and v0.17 FALSIFIED on panel inadequacy (SSRN 6802261).
2. **The first generalization test of the Recognition × Recall multi-component construct** (v1.4) from its original cross-cultural Iwachu anchor (v0.17 Japanese cell) to a same-language IL-gradient substrate.

**Substrate.** Indie fragrance, 24 brands across three Identity-Load-stratified cells (8 brands per cell, worldwide n = 24 pre-floor). English-language anchored throughout. The locked six-slot reference panel from v0.17 is carried forward.

| Cell | Identity-Load tier | Mean Phase A C_P | Pivot outcome |
|---|---|---|---|
| Cell A — Designer-niche | medium-high IL | 5.88 / 6 | Anchored at Maison Francis Kurkdjian (first cascade step) |
| Cell B — Indie / Artisan | high IL | 5.00 / 6 | Anchored at D.S. & Durga (first cascade step) |
| Cell C — Mass-prestige | medium IL | 0.25 / 6 | Cascade exhausted (DEVIATIONS Entry 1) |

---

## Three orthogonal verdicts

| Hypothesis | Verdict | Resolution |
|---|---|---|
| H_Regime4_indie_fragrance (within-phase substantive) | **PARTIAL** | Resolved at C3 (ranking coherence). C1 panel adequacy and both C2 conditions clear; C3 fails at 1 of 3 cells clearing per-cell ρ ≥ 0.50 |
| H_IdentityLoad_moderator (three-leg joint) | **PARTIAL** | v0.16 PARTIAL × v0.17 FALSIFIED × v0.18 PARTIAL → joint PARTIAL (moderator operates with substrate-specific qualifications) |
| H_Recognition_Recall_dissociation_generalization (methodological) | **DISSOCIATION_PARTIAL** | 9 Iwachu-pattern cases identified across 2 of 3 cells (Cell A: 3; Cell B: 6; Cell C: 0 by Recognition-floor design) |

**Methodological headline.** The v1.4 multi-component construct generalizes from its original cross-cultural anchor (one case on a Japanese-cell substrate) to a same-language IL-gradient substrate (nine cases across two cells, concentrated in the highest-IL cell at 75% prevalence). The dissociation is not a cross-cultural artifact; it is a measurable mechanism of AI-mediated retrieval.

---

## Per-cell diagnostics

Phase B observations are out of 18 (3 query frames × 6 reference panel models).

| Cell | n | Top-2 mention share | Spearman ρ (C_P × mentions) |
|---|---|---|---|
| Cell A — Designer-niche | 8 | 0.446 | 0.247 |
| Cell B — Indie / Artisan | 8 | 1.000 | 0.434 |
| Cell C — Mass-prestige | 8 | 0.688 | 0.615 |

- **C1 panel adequacy:** worldwide n = 24 ≥ 12 floor ✓
- **C2 within-cell** (top-2 ≥ 0.50): Cells B and C clear ✓
- **C2 IL-gradient separation** (Cell B − Cell C ≥ 0.10): 1.000 − 0.688 = 0.3125 ≥ 0.10 ✓
- **C3 within-cell ρ ≥ 0.50** in ≥ 2 of 3 cells: only Cell C clears (1 of 3) ✗

---

## Pre-registration discipline

The v0.18 pre-registration was iteratively refined through revisions r1 → r4 before any data acquisition. Each revision is preserved in git history:

- **r1** at commit `183386c` — initial lock (panel, hypotheses, decision-rule structure)
- **r2** — panel composition refinement
- **r3** — frame battery specification
- **r4** at commit `1195cb8` — numerical lock of C2/C3 thresholds for the v1.4 framework (the first phase to exercise v1.4 C2/C3, since v0.17 FALSIFIED at C1)

One deviation was opened during acquisition:

- **DEVIATIONS Entry 1** (2026-05-20, pre-Phase-B): Cell C pivot cascade exhausted at the "niche fragrance" Recognition probe. No Cell C brand achieved C_P = 6/6. Treated as substantive empirical finding (the IL-gradient operating on Recognition itself), not as panel construction error. Cell C alternates explicitly NOT invoked. Pre-registered panel of 24 brands unchanged. Full text at `DEVIATIONS.md`.

---

## Deposit layout

```
osf/v18/
├── README.md                              ← this file
├── MANIFEST.md                            ← annotated file inventory
├── PRE_REGISTRATION_v0_18.md              ← locked pre-reg (r1–r4 history in Appendix A)
├── DEVIATIONS.md                          ← deviations log (Entry 1)
├── data/
│   ├── phase_a_results.json               ← Phase A C_P scores per brand × model
│   ├── phase_b_results.json               ← Phase B mention rates per brand × frame × model
│   └── verdicts/
│       ├── v0_18_verdict.json             ← machine-readable verdict structure
│       └── v0_18_verdict.md               ← human-readable verdict with diagnostics
├── figures/
│   ├── chart_01_mention_rate_distribution.pdf
│   ├── chart_02_cell_attrition.pdf
│   └── chart_03_dissociation_scatter.pdf
├── scripts/
│   ├── _path.py                           ← protocol/ sys.path bootstrap
│   ├── acquire_phase_a_v18.py             ← Phase A acquisition driver
│   ├── acquire_phase_b_v18.py             ← Phase B acquisition driver
│   ├── score_v18.py                       ← C1/C2/C3 verdict logic + emission
│   ├── build_charts_v18.py                ← three brand-format chart renderers
│   └── protocol/                          ← canonical AIAS v1.4 implementation
│       ├── __init__.py
│       ├── thresholds.py                  ← locked numerical thresholds (pre-reg r4)
│       ├── providers.py                   ← Anthropic / OpenAI / Google SDK dispatch
│       ├── probe.py                       ← probe_brand (C_P) + probe_frame
│       └── parse.py                       ← v1.4 brand-mention detection rules
└── reports/
    ├── v18_indie_fragrance.pdf            ← brand-format report
    ├── build_report_v18.py                ← two-pass ReportLab + pypdf typesetter
    └── v18_indie_fragrance_content.py     ← content module (sections, tables, prose)
```

---

## Reproduction instructions

The full v0.18 pipeline reproduces from a clean clone of the program repo at the v0.18-prereg-r1 tag.

**Dependencies:**

```bash
python -m pip install anthropic openai google-generativeai python-dotenv \
    matplotlib reportlab pypdf scipy
```

**API credentials:** create a `.env` file at the project root with real keys for the three providers (Anthropic, OpenAI, Google AI Studio). See `.env.example` in the program repo for the template.

**Pipeline:**

```bash
python scripts/acquire_phase_a_v18.py    # ~10–20 min (288 API calls with cascade early-termination)
python scripts/acquire_phase_b_v18.py    # ~5 min (18 calls)
python scripts/score_v18.py              # seconds (local computation)
python scripts/build_charts_v18.py       # seconds (matplotlib + pypdf)
python reports/build_report_v18.py       # seconds (ReportLab + pypdf two-pass)
```

**Expected outputs match the files in this deposit.** LLM responses are not deterministic; minor variation in mention counts is expected across runs against the same locked panel. Substantive verdicts (PARTIAL × 3) should replicate.

---

## Citation chain

- González Castro, P. U. (2026). *AI Availability — A Third System in Brand Availability Theory.* SSRN 6659000.
- González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol: Methodological Notes (v1.2).* SSRN 6761698.
- González Castro, P. U. (2026). *AIAS Protocol v1.3 — Phase A Pivot-Validation Specification.* SSRN 6797679.
- González Castro, P. U. (2026). *AIAS Protocol v1.4 — Recognition × Recall Decomposition.* SSRN 6799479.
- González Castro, P. U. (2026). *v0.16 — Regime 4 Boundary and Discourse-Language Carryforward (Kitchen Knives).* SSRN 6791999.
- González Castro, P. U. (2026). *v0.17 — Panel Inadequacy and Recognition × Recall Dissociation (Premium Kitchenware).* SSRN 6802261.
- González Castro, P. U. (2026). *v0.18 — Identity-Load Moderator Test and Recognition × Recall Dissociation Generalization (Indie Fragrance).* SSRN *forthcoming*.

---

## Declarations

**Declaration of interest.** The author is employed by Samsung Electronics America (Director, Corporate Brand Creative and Governance). The AIAS™ Presence Measurement Protocol and the work reported here are independent academic research, conducted outside the scope of employment, in the author's role as faculty at the School of Visual Arts MPS Branding Program and founder of Third System™. Samsung had no role in the design, execution, analysis, or interpretation of this work.

**Funder.** Self-funded.

**Ethics.** Not applicable; no human subjects. The research uses publicly accessible LLM APIs queried with non-personal, category-anchored prompts.

**Trademark notice.** AIAS™ and Third System™ are trademarks of the research program.

---

*Correspondence:* Pablo Ulpiano González Castro · pablou@pablou.com · pablou.com · thirdsystem.ai · ORCID 0009-0003-8968-9990
