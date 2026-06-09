# AIAS™ v0.33 — Provider-Asymmetric CPC

A pre-registered re-analysis testing whether CV-CPC — the program's current
Consistency operationalization — varies systematically by the LLM provider that
produces a recall, holding the brand and category fixed.

**Phase type — re-analysis (no new acquisition).** This phase re-uses the frozen
per-model inputs of v0.31 and the CV-CPC instrument *as already computed*; it
makes no claim that CV-CPC is a validated Consistency measure. CV-CPC was found
strongly presence-coupled (|ρ| = 0.77) and was not adopted in the v1.7
methodology lock (SSRN 6878818); v0.33 analyzes the quantity as-is and is walled
accordingly.

**Pre-registration.** Methodology was locked before any scoring, at commit
`c8f2736`, annotated tag `v0.33-prereg-r1` (the external anchor; on origin).
DEVIATIONS: none.

---

## What was tested

| Hypothesis | Test | Verdict |
|---|---|---|
| **H_Provider_Asymmetry** (primary) | between-provider η² of recall consistency vs permutation null | **Confirmed, modest.** Mean η² = 0.360 > null (Monte Carlo p = 0.0007), robust across all five leave-one-category-out refits. A small excess over a high small-group chance floor — a dependable but minor influence. |
| **H_Provider_Beyond_Presence** (primary gate) | paired δη² = η²(recall) − η²(recognition) | **Numerical criterion met (δη² = 0.505, p = 0.0001) but saturation-collapsed.** Among above-floor brands, recognition carries essentially no provider variance, so the gate reduces to the recall arm and does **not** establish a dissociation. This collapse is the study's principal methodological finding. |
| **H_Provider_Ordinal** (secondary) | Kendall's W across the five categories | **Uninformative.** W = 0.31, exact p = 0.18; pre-registered as underpowered at N = 5. |
| **H_Provider_Phantom** (tertiary, exploratory) | below- vs above-floor η² | Descriptive and mechanical — below-floor brands carry less recall variance to organize, so their η² is lower by construction; not a signature. |

---

## Reconciliation

Per-model recall and recognition were recomputed from three heterogeneous
extraction paths (v0.19 phase-B CSV; v0.20–v0.22 phase-B CSV via the
v0.31-certified brand matcher; v0.23 scored JSON). As a computational-
reproducibility gate, the recomputed v0.20 / v0.21 / v0.22 per-model recall
vectors were required to reproduce the `r_per_model` column of the v1.7 CPC table
bit-for-bit.

**Result: 72 / 72 brands reproduced exactly**, aligned by model name (the v1.7
table stores models in sorted order; the panel order differs, so a positional
compare would have spuriously failed).

> ¹ The reconciliation anchor covers only v0.20, v0.21, and v0.22 — the three
> substrates with an external v1.7 per-model record. v0.19 and v0.23 have no such
> anchor and are carried as provenance-only (extraction verified; no bit-for-bit
> external check available).
>
> ² For v0.23, recognition was stored as a graded field (`r_level`) and
> normalized to binary recognition for this analysis; the normalization rule is
> recorded in the scoring script.

---

## Scope and method

- **Omnibus** — the five substrates carrying the canonical six-model panel:
  v0.19 headphones (16 brands), v0.20 skincare, v0.21 cosmetics, v0.22
  automotive, v0.23 premium spirits (24 each) = **112 brand units**.
- **Panel** — Anthropic {Opus 4.5, Sonnet 4.5}, OpenAI {GPT-4o, GPT-4o-mini},
  Google {Gemini 2.5 Flash, Flash-Lite}.
- **η²** — between-provider share of recall-consistency variance, per brand. The
  per-brand label space is exactly enumerable (90 assignments); the population
  test is Monte Carlo, ≥ 10,000 draws, seed 280400. Zero-variance brands are set
  to η² = 0 (not excluded).

---

## Contents

- `prereg/` — pre-registration content (`v0_33_provider_asymmetry_content.py`) and the re-analysis protocol (`v0_33_mega_prompt.md`); lock `v0.33-prereg-r1`
- `data/v33_eta2.csv` — per-brand η² decomposition (112 brands; recall and recognition arms; defined-flag)
- `v33_provider_asymmetry_verdicts.json` — the locked confirmatory verdicts
- `scripts/` — `score_v33.py` (confirmatory scorer), `audit_v33_recognition.py` (recognition-source audit), and the figure/report builders (`build_charts_v33.py`, `build_report_v33.py`)
- `exploratory/` — the walled post-hoc recognition-source audit (not part of the confirmatory test)
- `figures/` — the three finding charts (academic register: `chart_01_eta2_null`, `chart_02_gate_arms`, `chart_03_provider_ranks`)
- `papers/` — the SSRN paper (`v0_33_ssrn_paper_draft.md` + built `v0_33_ssrn_paper.pdf`)
- `reports/v33_provider_asymmetry_report.pdf` — the Third System™ brand-format report (managerial register; carries a 4th descriptive figure not in the paper's pre-registered set)

---

## Methodology lineage

CV-CPC specification — v0.30 (SSRN 6875319). Methodology lock and non-adoption —
v1.7 (SSRN 6878818). AI Availability framework — AIAS 1.0 (SSRN 6817841);
Tri-System foundation (SSRN 6659000). Cross-category CPC baseline — v0.31
(SSRN 6880959). Model-version snapshot — v0.32 (SSRN 6898581).

## Citation

González Castro, P. U. (2026). *AIAS v0.33 — Provider-Asymmetric CPC: a
pre-registered re-analysis.* SSRN [abstract ID backfilled on submission].

Author: Pablo Ulpiano González Castro · pablou@pablou.com · pablou.com ·
ORCID 0009-0003-8968-9990. Conflict-of-interest disclosure: see the paper's
Declarations.

---

*Third System™ · AIAS™ Measurement Program · OSF project ec6wh*
