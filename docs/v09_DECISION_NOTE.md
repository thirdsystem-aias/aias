# v0.9 Re-Baseline — Methodological Decision Note

**Date:** 2026-05-06
**Author:** Pablo Ulpiano Gonzalez Castro
**Study:** AIAS v0.9 longitudinal re-baseline of v0.6 categories at t₂
**Status:** Locked before measurement run

## Decisions

### 1. Model set
Run all three models (the v0.6 pair plus Gemini) at t₂. Compute longitudinal v0.6→v0.9 deltas on the matched 2-model subset only. Gemini's t₂ data is reported as a *parallel new baseline* — the t₁ reference for future Gemini longitudinal work — alongside but separately from the drift table.

**Rationale:** Gemini access cleared between v0.6 and v0.9. Folding Gemini into the aggregate longitudinal comparison would conflate AI drift with the introduction of a new model variable. Matched-subset preserves clean t₁/t₂ attribution while bringing Gemini into the program.

### 2. Mode classifier
Apply retroactively to v0.6 t₁ data. Both t₁ and t₂ datasets carry mode classifications under the same scheme.

**Rationale:** Forward-only application would create a known asymmetry. Retroactive classification preserves apples-to-apples longitudinal claims.

### 3. Registry
Freeze at v0.6's final state. No per-category revisions in v0.9.

**Rationale:** Revisions would conflate AI behavior change with measurement change. If a registry error surfaces during v0.9 analysis, document as a limitation rather than fix mid-study.

## Lock

Decisions locked in git as of this commit. Any deviation requires a methodology amendment with rationale.
