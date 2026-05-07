# v0.9 Re-Baseline — Methodological Decision Note

**Date:** 2026-05-06
**Author:** Pablo Ulpiano Gonzalez Castro
**Study:** AIAS v0.9 longitudinal re-baseline of v0.6 categories at t₂
**Status:** Locked before measurement run
**Methodology version (v0.9 rows):** 0.4

## Decisions

### 1. Model set
Run all six models at t₂ (the Phase 2 lineup that v0.7 and v0.8 used):

| Slot              | Model              | Role at v0.9                 |
|-------------------|--------------------|------------------------------|
| anthropic_sonnet  | claude-sonnet-4-6  | matched subset (in v0.6 t₁)  |
| openai_mini       | gpt-5.4-mini       | matched subset (in v0.6 t₁)  |
| anthropic_opus    | claude-opus-4-7    | parallel new baseline        |
| openai_flagship   | gpt-5.5            | parallel new baseline        |
| google_flash      | gemini-2.5-flash   | parallel new baseline        |
| xai_grok          | grok-4-1-fast      | parallel new baseline        |

Longitudinal v0.6→v0.9 deltas are computed only on the matched subset (claude-sonnet-4-6 and gpt-5.4-mini). The other four models report as parallel new baselines — first measurement for each, t₁ reference for their own future longitudinal work.

**Rationale:** v0.6 used 2 models. Phase 2 (v0.7, v0.8) expanded to 6. Folding the 4 new models into the longitudinal comparison would conflate AI drift with model expansion. Matched-subset preserves clean t₁/t₂ attribution while bringing the full Phase 2 lineup into the program.

### 2. Mode classifier
Apply retroactively to v0.6 t₁ data. Both t₁ and t₂ datasets carry mode classifications under the same scheme.

**Rationale:** Forward-only application would create a known asymmetry. Retroactive classification preserves apples-to-apples longitudinal claims and lets the mode dimension enter drift analysis on equal footing.

### 3. Registry
Freeze at v0.6's final state. No per-category revisions in v0.9.

**Verified:** v0.6 measurement CSVs across all 5 categories show 96 rows each (6 prompts × 2 models × 8 runs) with brand_registry_version stamps `v2`, `v2-runningshoes`, `v2-oliveoil-rev1`, `v2-skincare`, and `v2-skincare`.

**Documented anomaly:** Finance v0.6 data carries the stamp `v2-skincare` due to a module-level metadata constant carryover in the pre-Phase-2 runner. Verified by inspection of raw_response content: finance prompts produced finance responses (YNAB, budgeting topics) and registry loading was correct. The stamp is cosmetic only, not a measurement defect. Disclosed in the v0.9 report's methodology section.

**Rationale:** Revisions would conflate AI behavior change with measurement change. If a registry error surfaces during v0.9 analysis, document as a limitation rather than fix mid-study.

## Methodology version bump

`METHODOLOGY_VERSION` in `run_aias_v2.py` bumps from `"0.3"` (v0.6 stamp) to `"0.4"` for v0.9. Provides a clean partition variable on every row in addition to the filename pattern (`results_v2_<cat>_<timestamp>.csv` for v0.9 vs `results_v2_<timestamp>.csv` for v0.6).

## Lock

Decisions locked in git as of this commit. Any deviation requires a methodology amendment with rationale.
