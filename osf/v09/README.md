# AI Presence Drift — AI Presence Index v0.9

**Longitudinal re-baseline of five categories on the matched two-model subset (29–30 April 2026 → 7 May 2026)**

This OSF deposit is the data, code, and supporting materials for **v0.9 of the AI Presence Index (AIAS) measurement program**, conducted by Third System™. The deposit accompanies the SSRN working paper *AI Presence Drift: Longitudinal Re-Baseline of Five Categories* and the Third System brand-format report *AI Presence Drift — AI Presence Index v0.9*.

---

## What v0.9 is

v0.9 is the longitudinal re-baseline that closes Phase 2 of the AIAS measurement program. The five categories first measured in the v0.6 cross-category baseline (project management software, premium running shoes, premium olive oil, premium facial skincare, personal finance applications) were re-measured at a second time point (t₂ = 7 May 2026) approximately seven days after t₁ (= 29–30 April 2026). The v0.6 registries, prompt set, and methodology version were preserved at v0.6 final state to support direct longitudinal comparison.

The matched two-model subset that carries the longitudinal claim consists of **Anthropic Claude Sonnet 4.6** and **OpenAI gpt-5.4-mini** — the original v0.6 lineup, the only models present at both waves. Four parallel-baseline models were added at t₂ for downstream cross-vendor work (Anthropic Claude Opus 4.7, OpenAI gpt-5.4, Google Gemini 2.5 Pro, xAI Grok 4) but cannot contribute to the longitudinal claim itself.

**Total measurement volume**: 1,440 successful measurements (5 categories × 6 prompts × 6 models × 8 runs). Matched-subset volume: 480 per wave (2 models × 5 categories × 6 prompts × 8 runs).

## What v0.9 found

Six hypotheses with explicit numerical thresholds were committed to a pre-registration document locked at git commit `f8cebbd` (tag `v0.9-prereg-locked`) prior to any t₂ data collection.

| Hypothesis | Outcome |
|---|---|
| H1 — Drift small and tightly bounded (≥70% within ±5pp; ≥90% within ±10pp) | **Confirmed** — 88.3% within ±5pp; 99.0% within ±10pp |
| H2 — Top-3 at t₁ remain in top-5 at t₂ (5 of 5 categories) | **Confirmed** — 5 of 5; no exceptions |
| H3 — Within-category variance ordering preserves (Spearman ρ ≥ 0.7) | **Confirmed** — ρ = 0.8 |
| H4 — Mint matched-subset gross Presence stable within ±5pp | **Stability (predicted)** — −3.1pp (44.8% → 41.7%) |
| H5 strict — Spanish olive oil ≤12.5pp AND K-beauty ≤5pp | **Confirmed** — 11.5pp / 1.0pp |
| H5 inclusive — As above with Graza added to Spanish cohort | **Partially confirmed** — 14.2pp (breach); 1.0pp |
| H6 — Per-brand cross-model spread Pearson r ≥ 0.7 (≥4 of 5 categories) | **Confirmed** — 5 of 5 |
| Pattern 1 (post-hoc) — v0.6 cross-model spread ordering replicates | **Replicated** — ρ = 0.800 (t₁/t₂); ρ = 0.900 (t₂ / v0.6 narrative) |

**Headline result**: five formal hypotheses confirmed at threshold; the sixth (H4) landed at the predicted stability band; the H5 inclusive sensitivity surfaces Graza as a sharper diagnostic case for the brand-marketing-language tier identified in v0.6 §4.4; the post-hoc Pattern 1 test replicates v0.6's qualitative cross-model spread ordering.

The combined result set is interpreted in the discussion as a **longitudinal validity argument** for AI Presence as a measurable underlying construct of the LLM tier rather than instrument-and-occasion noise. The result unblocks Phase 3 construct-validity work, which requires three categories at two time points and now has data for five.

## What's in this deposit

The deposit is organized as follows. See `MANIFEST.md` for the file-by-file index.

```
/v09/
├── README.md                              ← this file
├── MANIFEST.md                            ← file-by-file index
│
├── papers/
│   ├── v09_ssrn_paper_v3.pdf              ← SSRN working paper
│   ├── v09_ssrn_paper_v3.md               ← SSRN paper source
│   └── PRE_REGISTRATION_v09_rebaseline_v1.0.md
│
├── reports/
│   └── v09_longitudinal_rebaseline.pdf    ← Third System brand-format report
│
├── figures/
│   ├── chart_v09_h1_drift_scatter_6col.pdf
│   ├── chart_v09_h2_leaderboard_6col.pdf
│   ├── chart_v09_h3_within_cat_variance_6col.pdf
│   ├── chart_v09_h4_mint_persistence_4col.pdf
│   ├── chart_v09_h5_pattern4_sensitivity_6col.pdf
│   ├── chart_v09_h6_cross_model_spread_6col.pdf
│   ├── chart_v09_pattern1_spread_6col.pdf
│   ├── chart_v09_mode_distribution_6col.pdf
│   └── chart_v09_pattern_matrix_6col.pdf
│
├── code/
│   ├── build_charts_v09_rebaseline.py     ← chart generator
│   ├── build_report_v09.py                ← brand-format report builder
│   ├── v09_rebaseline_content.py          ← report content data structures
│   ├── analyze_v09.py                     ← H1–H6 scoring
│   ├── analyze_v09_posthoc_pattern1.py    ← post-hoc Pattern 1 test
│   ├── extract_v09.py                     ← brand-mention extraction
│   └── smoke_providers_v09.py             ← provider availability smoke test
│
├── registries/
│   └── brands_<category>.json             ← five category registries, frozen at v0.6 final
│
└── data/
    ├── raw/                               ← raw model responses
    ├── extracted/                         ← canonical brand-mention extractions
    ├── mode_classified/                   ← five-mode classifications
    └── scoring/                           ← per-hypothesis outcome scores
```

## How to use this deposit

**To replicate the analysis**: run the scripts in `/code/` against the data in `/data/`. The `analyze_v09.py` script computes H1–H6 against the matched subset and writes the scoring outputs. The `analyze_v09_posthoc_pattern1.py` script computes the post-hoc Pattern 1 replication.

**To re-render figures**: `build_charts_v09_rebaseline.py` regenerates all nine chart PDFs. Output at native figsize per `chart_construction_rules` — no rescaling.

**To audit the pre-registration**: `PRE_REGISTRATION_v09_rebaseline_v1.0.md` was locked at git commit `f8cebbd` prior to any t₂ data collection. The hypothesis statements, numerical thresholds, and sensitivity-check protocol are exactly as committed pre-measurement.

**To audit registry construction**: `/registries/brands_<category>.json` are the v0.6 final-state registries used at v0.9. The K-beauty and Spanish olive oil cohorts referenced in H5 are documented in the pre-registration; the Graza inclusive-cohort sensitivity check is also documented there.

**To extend the program**: methodology decisions for v0.9 (matched-subset convention, retroactive mode classification of v0.6 data, registry freeze) were locked at git commit `e6428a4` prior to the pre-registration. The decisions are documented in the `methodology_decisions` section of the pre-registration document and in §2 of the SSRN paper. Extensions should preserve these conventions or document deviations.

## Methodological lineage

v0.9 follows the AIAS Presence Measurement Protocol v1.1 — same protocol as v0.7 (Phase 2 BBB) and v0.8 (Phase 2 Knives). Cross-references to upstream and adjacent deposits:

- **AI Availability foundational paper** — SSRN abstract `6659000`
- **AIAS Presence Measurement Protocol v1.1** — SSRN abstract `6722319`
- **v0.6 Cross-Category Findings** — SSRN abstract `6720959` (the t₁ baseline this study re-measures)
- **v0.7 Phantom-Brand BBB** — SSRN abstract `6721779`
- **v0.8 Discourse-Language Knives** — SSRN abstract `6728000`

## Limitations summary

Seven caveats apply to v0.9. See §6 of the SSRN paper for full treatment. Briefly:

1. **Single-pair longitudinal subset.** The longitudinal claim generalizes most directly to the matched-subset model behavior (Sonnet 4.6 and gpt-5.4-mini). Parallel-baseline models contribute new t₂ baselines but not drift deltas.
2. **Seven-day inter-measurement interval.** Short enough that no major model release or training-cutoff change is expected within. Longer intervals (one month, three months, twelve months) remain v0.10+ priorities.
3. **Gross Presence vs naive-phantom rate.** The H4 finding measures the gross-Presence variable v0.6 §4.6 reported. The v0.7 reframe distinguishing naive-phantom rate is not unpacked at v0.9; the v0.9 raw responses are deposited so a v0.10 pre-registration could address the question without new measurement.
4. **Registry-construction reflexivity.** The K-beauty observation establishes that registry construction inherits Anglo-discourse coverage bias. Disclosed for transparency; does not invalidate H1–H6.
5. **Construct validity remains open.** v0.9 establishes longitudinal validity at the LLM tier. Whether AI Presence correlates with consumer-tier validators is the Phase 3 question.
6. **v0.6 personal finance metadata anomaly.** The `brand_registry_version` stamp on the v0.6 personal finance measurement reads `v2-skincare`, inherited from the prior session's module-level constant. The metadata is cosmetic; raw-response inspection confirms correct prompts and registry fired.
7. **Mode-classification audits deferred.** The v0.8 audit established 96% strict agreement on the brand-surfacing macro unit (the unit at which H1–H6 score) and 68% strict agreement on the underlying five-mode taxonomy. Manual v0.9 audits are scheduled prior to v0.10.

## Citation

Gonzalez Castro, P. U. (2026). *AI Presence Drift: AI Presence Index v0.9 — Longitudinal re-baseline of five categories*. Third System. https://thirdsystem.ai/v09-longitudinal-rebaseline

OSF deposit: [add OSF URL after deposit]
SSRN abstract: [add SSRN ID after submission]

## Contact

Correspondence: pablou@pablou.com · pablou.com
Research entity: Third System™ · hello@thirdsystem.ai · thirdsystem.ai

## License

Data and code released under CC-BY-4.0 / MIT respectively. Findings may be cited with attribution.

---

*Pre-registration locked at git commit `f8cebbd` (tag `v0.9-prereg-locked`) prior to any t₂ data collection. Methodology decisions locked at git commit `e6428a4` prior to the pre-registration. Deposit prepared at git tag `v0.9-published` on 8 May 2026.*
