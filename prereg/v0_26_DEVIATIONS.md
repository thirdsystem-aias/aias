# v0.26 DEVIATIONS LOG

## Entry 0 — Pre-registration amendment r1 → r2

**Date:** May 28, 2026
**Trigger:** Data integration during scoring revealed three substrate-level incompatibilities invisible at pre-registration time.

### Amendment 1: v0.17 (premium kitchenware) excluded

v0.17 Phase A halted at C1 inadequacy. Per-brand C_P was never computed; no usable artifact exists. Substrate dropped from the study entirely.

### Amendment 2: v0.21 (cosmetics) reclassified as ceiling-only

All 24 cosmetics brands scored C_P = 6 in Phase A (zero predictor variance). Within-substrate Spearman ρ is undefined. Substrate contributes to pooled cross-substrate and Cell A analyses only, not to within-substrate correlation tests.

### Amendment 3: v0.16 (kitchen knives) C_P retrofitted

v0.16 originally ran under methodology v1.2, which scored AI Availability via Google Trends + high-N LLM probes summarized as a continuous percentage (ai_t1_pct, ai_t2_pct). The v1.4+ C_P metric (integer 0–6, count of panel models recognizing the brand) did not exist in v0.16's output. No back-derivation from existing artifacts was possible.

**Retrofit:** 156 Recognition probes (26 brands × 6 panel models) run under the canonical v1.4+ protocol using the v0.19 probe template ("Is the brand [BRAND] commonly recognized as a brand of kitchen knives? Answer yes or no."). Output: osf/v26/data/v16_cp_retrofit.csv + v16_cp_retrofit_aggregated.csv + v16_cp_retrofit_responses.jsonl (full provenance sidecar).

**Provenance note:** The retrofit was acquired contemporaneously with BSR data (May 2026), creating temporal alignment between C_P and BSR for this substrate. This contrasts with v0.19 and v0.20 where C_P was measured months earlier.

### H_PV_Primary threshold adjustment

Original (r1): "Spearman ρ ≤ −0.40, p < 0.05, in at least 3 of 5 substrates."
Amended (r2): "Spearman ρ ≤ −0.40, p < 0.05, in at least 2 of 3 testable substrates."

Verdict taxonomy unchanged: CONFIRMED ≥ 2/3; PARTIAL = 1/3; FALSIFIED = 0/3.
