# v0.14 — Premium Tea Regime 4 Replication

Pre-registered, single-category replication of the v0.13 Covariate-saturated weak (Regime 4) finding from the AIAS™ Presence Measurement Programme.

**H_Regime4_replication CONFIRMED** at both measurement waves (t₁ = 29 April 2026; t₂ = 7 May 2026) and surviving Tea Box-excluded sensitivity testing. Three datapoints across three categories (premium facial skincare, personal-finance apps, premium tea) elevate Regime 4 from a provisional zone (v0.13) to a canonical pattern (v0.14).

## Deposit contents

- `PRE_REGISTRATION_v0_14.md` — full pre-registration, locked at git tag `v0.14-prereg` (commit b0ef30a), 12 May 2026 UTC, prior to LLM acquisition
- `DEVIATIONS.md` — Entry 1 (Phase B bare-canonical query methodology amendment), Entry 2 (Yunnan Sourcing alternate activation)
- `registries/` — brand registry (`brands_premium_tea.json`, v3-premium_tea schema, 25 brands), brand-age verified sources, topic-ID resolution log
- `data/` — Google Trends raw response bundles (8 bundles × 2 waves × 2 regions), processed per-brand/per-day/within-window outputs, LLM acquisition results (288 calls, matched-model subset)
- `analysis/` — canonical scoring outputs (`canonical_scoring.csv`, `canonical_scoring.json`, `per_brand_paired.csv`), regime classification (`h7_regime_classification.csv`), replication test (`h_regime4_replication.csv`)
- `figures/` — 4 chart PDFs (regime4 canonical, primary vs sensitivity, per-category construct validity comparison, premium tea per-brand scatter)
- `reports/v14_premium_tea.pdf` — brand-format public-facing report
- `papers/v14_ssrn_paper.pdf` — SSRN Working Paper 6755621 (academic paper)
- `papers/v14_ssrn_paper_draft.md` — paper source markdown (pandoc + xelatex + Carlito build)

## Headline results

- **Bivariate Spearman ρ(AI Presence × Google Trends):** −0.066 at t₁, −0.134 at t₂ (worldwide, n = 17)
- **Partial Spearman ρ** (controlling for brand age and premium tier): −0.084 at t₁, −0.146 at t₂
- **Tea Box-excluded sensitivity** (n = 16): bivariate −0.011 / −0.129; partial −0.005 / −0.130 — verdict robust
- Premium tea is the cleanest Regime 4 case to date: bivariate ρ already negative before covariate control (skincare and finance both required positive-to-negative migration under covariate control)
- Headline classification axes evolved from (bivariate ρ × covariate decrement) in v0.13 to (bivariate ρ × partial ρ) in v0.14 to accommodate categories with already-negative bivariate signal

## Key references

- **SSRN paper:** [Working Paper 6755621](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6755621)
- **Pre-registration lock:** git tag `v0.14-prereg` (commit b0ef30a)
- **Canonical scoring script:** `score_v14.py` at commit e71e135
- **Programme stack** (full SSRN cross-references):
    - AI Availability foundational paper: SSRN 6659000
    - AIAS Presence Measurement Protocol v1.1: SSRN 6722319
    - v0.6 Cross-Category Findings: SSRN 6720959
    - v0.7 Phantom-Brand Persistence Phase 2 (BBB): SSRN 6721779
    - v0.8 Discourse-Language Knives: SSRN 6728000
    - v0.9 Longitudinal Re-Baseline: SSRN 6736878
    - v0.10 Naive-Phantom Rate Stability: SSRN 6741163
    - v0.11 PM Software × Trends Construct Validity Pilot: SSRN 6745040
    - v0.12 Three Empirical Regimes: SSRN 6748341
    - v0.13 Four Empirical Regimes: SSRN 6750498
    - Tri-System Brand Growth: Marketing Science Institute Working Paper Series

## Reproducibility

All pre-registered conditions and statistical tests are deterministic given the locked inputs:

- LLM responses cached in `data/llm_acquisition/results_*.csv`
- Trends raw bundles cached in `data/trends_raw/`
- Scoring script `score_v14.py` (e71e135) recomputes all reported statistics from the cached inputs

The pre-registration locked at `v0.14-prereg` (b0ef30a) on 12 May 2026 UTC prior to any LLM acquisition call against the wave windows. Two deviation entries are documented (`DEVIATIONS.md`); no pre-registered hypothesis, threshold, or routing rule was modified.

## Author

Pablo Ulpiano González Castro · School of Visual Arts, MPS Branding Program (primary academic affiliation) · Third System™ (research entity, secondary) · ORCID [0009-0003-8968-9990](https://orcid.org/0009-0003-8968-9990) · pablou@pablou.com · pablou.com

## License

Data, code, and pre-registration materials are released under CC-BY-4.0 for reuse with attribution.
