# v0.11 OSF Deposit Manifest

**Project:** PM Software × Google Trends Construct Validity (v0.11)
**Pre-registration:** locked at git commit f20ade8 (tag v0.11-prereg), 10 May 2026 UTC
**SSRN abstract:** 6745040 — https://ssrn.com/abstract=6745040

## Folder inventory

- **PRE_REGISTRATION.md** — locked pre-registration document
- **DEVIATIONS.md** — log of deviations from pre-registration (none recorded)
- **analysis/** — canonical scoring outputs and per-brand paired wave data
- **data/** — Google Trends acquisition inputs and outputs
  - **phaseA_test/** — pre-acquisition topic-mid pass-through verification (Asana)
  - **phaseB_suggestions/** — pytrends suggestions() output for topic-mid resolution
  - **phaseB_validation/** — per-brand validation against out-of-sample window
  - **trends_raw/** — locked acquisition session (10 pivot bundles × 2 regions)
  - **trends_processed/** — pivot-rescaled per-brand daily and within-window means
- **figures/** — four chart PDFs (F1 t1 scatter, F2 t2 scatter, F3 rank-shift, F4 partial residual)
- **papers/** — SSRN paper source, preamble.tex, rendered PDF, submission packet
- **registries/** — frozen brand registry (PM software), query specs, brand age sources
- **reports/** — Third System brand-format report PDF
- **scripts/** — Phase A/B acquisition and validation scripts

## Lineage

1. Pre-registration locked at git commit f20ade8 prior to acquisition.
2. Acquisition session at 2026-05-10T11:59:43.459987+00:00 UTC via SerpAPI.
3. Pivot-rescaling per pre-reg §5.1 → `data/trends_processed/`.
4. Scoring against locked hypotheses → `analysis/`.
5. Chart generation → `figures/`.
6. Brand-format report → `reports/v11_pmtrends_construct_validity.pdf`.
7. SSRN paper → `papers/v11_ssrn_paper_v2.pdf` (abstract 6745040).

## Cross-references

- AI Availability foundational paper: SSRN 6659000
- AIAS Presence Measurement Protocol v1.1: SSRN 6722319
- v0.6 Cross-Category Findings: SSRN 6720959
- v0.7 Phantom-Brand Persistence: SSRN 6721779
- v0.8 Discourse-Language Knives: SSRN 6728000
- v0.9 Longitudinal Re-Baseline: SSRN 6736878
- v0.10 Naive-Phantom Rate Stability: SSRN 6741163
