# AIAS v0.10 — Naive-Phantom Rate Longitudinal Stability

**Status.** Pre-registered, locked 2026-05-09 at git commit `8767f44`. Analysis status: pre-analysis.
**Methodology.** AIAS Presence Measurement Protocol v1.1 (SSRN 6722319).
**Scope.** Single-brand (Mint) designed-for-test extension applying the v0.7 caveat-classifier to v0.9 raw responses. No new measurement.
**Author.** Pablo Ulpiano Gonzalez Castro.
**Research entity.** Third System™ (thirdsystem.ai).

## Cross-citations

- AI Availability foundational paper — SSRN 6659000
- AIAS Presence Measurement Protocol v1.1 — SSRN 6722319
- v0.6 Cross-Category Findings — SSRN 6720959
- v0.7 Phantom-Brand BBB — SSRN 6721779
- v0.8 Discourse-Language Knives — SSRN 6728000
- v0.9 Longitudinal Re-Baseline — SSRN 6736878
- v0.10 — SSRN [pending]

## Source data

Raw responses inherited from v0.9 (OSF project ec6wh, `/v09/data/responses/`, git tag `v0.9-published`). No new prompting, no new model calls. Analysis restricted to:

- **Brand.** Mint only.
- **Models — matched subset.** Sonnet 4.6 + gpt-5.4-mini.
- **Waves.** t₁, t₂ as defined in v0.9 pre-registration.
- **Effective-n floor.** H1 evaluated only if matched-subset n ≥ 100 at both waves (per pre-reg §3.4).

## Folder structure

```
/v10/
├── README.md                          (this file)
├── PRE_REGISTRATION.md                (locked at tag v0.10-prereg)
├── DEVIATIONS.md                      (post-lock deviations log)
├── MANIFEST.md                        (file inventory + checksums)
├── data/
│   ├── responses_mint/                (filtered v0.9 subset)
│   ├── classifications.csv            (per-response classifier output)
│   └── adjudication_log.csv           (E4 author-adjudication log)
├── registries/
│   ├── brands_pmtools_v0.6.json       (frozen, identical to v0.7–v0.9)
│   └── v07_caveat_classifier.json     (v0.7 rule list, verbatim)
├── analysis/
│   ├── canonical_scoring.csv
│   ├── canonical_scoring.json
│   └── sensitivity_E3.csv             (light-hedging robustness check)
├── code/
│   ├── classify_v10.py
│   ├── score_v10.py
│   ├── build_charts_v10.py
│   └── build_report_v10.py            (forks build_report_v09.py)
├── reports/
│   ├── v10_naive_phantom_stability.pdf (Third System brand format)
│   └── chart_v10_*.pdf
└── manuscript/
    ├── v10_ssrn.tex
    └── v10_ssrn.pdf
```

## Reproduction

1. Clone repo, checkout tag `v0.10-published`.
2. Pull v0.9 raw responses into `data/responses_mint/` via filter script in `code/`.
3. Run `python code/classify_v10.py` → `data/classifications.csv`.
4. Run `python code/score_v10.py` → `analysis/canonical_scoring.{csv,json}`.
5. Run `python code/build_charts_v10.py` → `reports/chart_v10_*.pdf`.
6. Run `python code/build_report_v10.py` → `reports/v10_naive_phantom_stability.pdf`.

## Declarations

**COI.** The author is also Director of Corporate Brand Creative and Governance at Samsung Electronics America. The v0.10 study, like all AIAS program publications, is independent research developed outside the scope of that employment. Mint and Credit Karma are not Samsung properties.
**Funding.** None.
**Pre-registration discipline.** `PRE_REGISTRATION.md` locked at git commit `8767f44` on `2026-05-09`, prior to any application of the classifier to v0.9 responses. `DEVIATIONS.md` logs any post-lock changes.

## Contact

hello@thirdsystem.ai
