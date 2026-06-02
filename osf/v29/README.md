# AIAS v0.29 (CV.05) — The Presence Component Is Construct-Valid

**Subtitle:** A Convergent–Discriminant (Campbell–Fiske) Baseline for AI Availability
**Design class:** Synthesis (no acquisition; assembly of two locked component verdicts)
**Protocol:** v1.6 (SSRN 6816340)
**Pre-registration:** locked at git tag `v0.29-prereg-r1` (commit `a66c8d8`). Synthesis phase — no acquisition tag (settled program convention; CV-family precedent v0.25/v0.26 is prereg-tag-only).
**Date:** June 2026
**Author:** Pablo Ulpiano González Castro
**Affiliation:** School of Visual Arts, MPS Branding Program, New York, NY (primary academic affiliation); Third System™ (research entity)
**ORCID:** 0009-0003-8968-9990
**Correspondence:** pablou@pablou.com

## Study design

This is a **synthesis**. It performs no new acquisition, runs no probes, and reads no
acquisition CSVs. It assembles two already-locked component verdicts into a single
multitrait–multimethod (MTMM) frame and evaluates the joint Campbell–Fiske condition
that defines a construct-validity baseline for the Presence component (C_P) of AIAS.

- **Convergent leg** (inherited from v0.25, SSRN 6842138, pre-reg `v0.25-prereg-r1`):
  AIAS Presence × Google Trends search interest across a 24-brand B2B SaaS panel.
  Search interest is a *related* salience signal, so a valid Presence measure should
  track it. Locked verdict H_CV_Primary CONFIRMED at ρ = 0.7411, p = 3.4×10⁻⁵, n = 24.
- **Discriminant leg** (inherited from v0.26, SSRN 6847678, pre-reg `v0.26-prereg-r2`):
  AIAS Presence × Amazon Best Sellers Rank, pooled n = 88. Sales rank is an *unrelated*
  criterion, so a valid Presence measure should not track it. Pooled ρ = −0.0002,
  p = 0.998 — statistically indistinguishable from zero.

The single computed quantity is the **Campbell–Fiske gap**
C₃ = |ρ_convergent| − |ρ_discriminant| = |0.7411| − |−0.0002| = **0.7409**.

## Hypothesis verdict

The pre-registered rule (`H_CV_Baseline`) is conjunctive and CONFIRMED iff three
conditions hold jointly:

| Condition | Test | Result | Pass |
|---|---|---|---|
| **C1** convergent | leg positive and significant | ρ = 0.7411, p = 3.4×10⁻⁵, n = 24 | ✓ |
| **C2** discriminant | \|ρ\| < 0.20 and non-significant | ρ = −0.0002, p = 0.998, n = 88 | ✓ |
| **C3** gap | \|ρ_conv\| − \|ρ_disc\| > 0 | 0.7409 > 0 | ✓ |
| **H_CV_Baseline** | C1 ∧ C2 ∧ C3, significance asymmetry intact | — | **CONFIRMED** |

The verdict is FALSIFIED if C₃ ≤ 0 (a Campbell–Fiske inversion) and PARTIAL if the
gap is positive but a leg drifts. The pre-registered point forecast for C₃ was ≈ 0.55,
anchored to the upper edge of the |ρ| < 0.20 discriminant band; the realized gap
(0.7409) exceeds it because the inherited discriminant coefficient came in near zero
rather than near the band ceiling. The forecast was non-binding; the verdict rule
depends on sign and significance, not on the point value. The pre-registration lock is
untouched — forecast-versus-realization only.

## What this establishes (bounded)

The finding is about the **measure**: the Presence component is construct-valid —
anchored to a related salience signal (search) and distinct from a commercial-outcome
criterion (retail sales rank). The program proposes AI Availability as a third system
alongside Mental and Physical Availability; that validity is the precondition the
proposal depends on, but the proposal is the frame, not a result of this study. The
predictive leg (whether Presence forecasts a downstream behavioral outcome) is not
claimed here and is gated to a subsequent wave.

## Contents

```
osf/v29/
├── README.md                                  (this file)
├── v29_verdicts.json                          canonical synthesis verdict (C1/C2/C3/H_CV_Baseline) + provenance
├── prereg/
│   ├── v0_29_cv_baseline_content.py           pre-registration content module (design, hypotheses, thresholds)
│   └── v0_29_mega_prompt.md                    pre-registration spec (synthesis assembly, no acquisition)
├── scripts/
│   ├── score_v29.py                           synthesis scorer (reads the two inherited verdict files; computes C₃)
│   └── build_charts_v29.py                     CV.05 figure builder (MTMM gap + convergent scatter)
├── papers/
│   ├── v0_29_ssrn_paper.pdf                    SSRN paper (academic register)
│   └── v0_29_ssrn_paper_draft.md              paper source (Markdown + YAML)
├── reports/
│   └── v29_cv_baseline_report.pdf              Third System brand-format report (managerial register)
└── figures/
    ├── chart_29_mtmm_gap.pdf                   Figure 1 — the construct-validity gap (referenced by paper + report)
    └── chart_29_convergent_scatter.pdf         Figure 2 — the convergent leg (v0.25 Presence × Trends)
```

The SSRN submission packet (`papers/v0_29/ssrn_submission_packet_v0_29.md`) is an
internal Step-3 metadata worksheet and is intentionally kept in-repo only, not
deposited here.

## Reproduction

This synthesis is deterministic: given the two inherited verdict files, the verdict is
exact and byte-reproducible.

```bash
# Verdict (reads osf/v25/v25_verdicts.json + osf/v26/v26_verdicts.json -> osf/v29/v29_verdicts.json)
python3 scripts/score_v29.py

# Figures
python3 scripts/build_charts_v29.py

# PDFs
python3 scripts/build_paper_v0_29.py
python3 reports/build_report_v29.py
```

The inherited data and per-point analyses live with their component studies:
convergent at osf.io/ec6wh/v25 (SSRN 6842138); discriminant at osf.io/ec6wh/v26
(SSRN 6847678). This node deposits the synthesis assembly, not a re-derivation of the
components.

## Methodology citation chain

- v1.2 — *Methodological Notes on Construct Validity and the Four-Regime Taxonomy*. SSRN 6761698.
- v1.3 — *Phase A Pivot-Validation Specification*. SSRN 6797679.
- v1.4 — *Recognition × Recall Decomposition and Multi-Component AI Availability*. SSRN 6799479.
- v1.5 — *Multi-Statistic C2 and Two-Channel Recall Decomposition*. SSRN 6810758.
- v1.6 — *Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension*. SSRN 6816340.

Foundational: *Tri-System Brand Growth* (SSRN 6659000).
Synthesis: *AIAS™ 1.0* (SSRN 6817841).
Inherited component studies: v0.25 convergent (SSRN 6842138); v0.26 discriminant (SSRN 6847678).

## Declarations

**Conflict of Interest:** The author is employed by Samsung Electronics America in a
corporate brand role. That employment played no part in the design, conduct, analysis,
or reporting of this research, which was carried out independently under the Third
System research entity. No commercial relationship exists between any brand examined in
the inherited component studies and the author or his employer that bears on the findings.

**Data and Code Availability:** The synthesis assembly, scoring code, figures, and
pre-registration are deposited at this OSF node (osf.io/ec6wh/v29). Inherited data and
verdicts are available with their respective component studies.

**Funding:** Self-funded.

**Ethics:** Not applicable; no human subjects. This phase performs no acquisition — it
assembles already-published component verdicts.
