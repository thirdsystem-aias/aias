# AIAS™ v0.31 — CPC Cross-Category Baseline · Pre-registration (r1)

**Phase type:** Retroactive rescore. **No new LLM acquisition.** This phase rescores committed Phase B recall data from prior substrates under the v1.7 CPC instrument, generalized to a channel-agnostic per-model unit (below). There is no acquisition mega-prompt for this phase; this document is the locked methodology declaration that the `v0.31-prereg-r1` tag points at. Authoritative parameter values live in `v0_31_cpc_baseline_content.py`, committed alongside this file.

## Lock

- Methodology: v1.7 (SSRN 6878818); instrument source v0.30 (SSRN 6875319).
- Reference panel: canonical six, fixed from v0.17 — Opus 4.5, Sonnet 4.5, GPT-4o, GPT-4o-mini, Gemini 2.5 Flash, Gemini 2.5 Flash Lite. Population, ddof=0.

## Unit (channel-agnostic generalization)

Per (brand, model): total mentions summed across all Phase B frames, channel-agnostic. Range 0..6 on the omnibus set.

**Identity.** On a two-channel substrate this equals R_cat + R_cult = v1.7 `combined_recall_count` by construction — the channels partition the six frames, none dropped or double-counted. The generalization contains the locked unit as a special case; no instrument is swapped.

**Counting convention (locked).** Per (brand, model), sum `mention==1` over all 6 frames; frames absent from a brand-resolved table are treated as 0. Applies to v0.19 (`brand|panel_model|frame|mentioned`).

## Reconciliation gate (scoring step 0)

Compute generalized CPC on v0.20 / v0.21 / v0.22; assert **exact** equality (zero difference) to v1.7-published CPC (`osf/methodology/v1_7/v1_7_cpc_verdicts.json`). Equality is definitional, so tolerance is exactly zero; the gate is a regression test on the channel-agnostic scorer. Any nonzero diff → **HALT**.

## Scoring (inherited from v1.7)

- Dispersion: CV = population SD / mean (ddof=0).
- Transform: CPC = 1 / (1 + CV), bounded (0,1], higher = more consistent.
- Floor: mean combined recall < 1.0 → CPC undefined (N/A). Undefined brands excluded from the substrate distribution; count reported per substrate.

## Registry

- **Omnibus (confirmatory; uniform 0..6 geometry):** v0.19 headphones, v0.20 skincare, v0.21 cosmetics, v0.22 automotive, v0.23 premium spirits. 24 brands each.
- **Supplementary (descriptive only; OUT of the omnibus test; 3-frame → 0..3):** v0.17 kitchenware, v0.18 indie fragrance.
- **Excluded (non-comparable axis):** v0.16 (14-model legacy panel; Trends-validation Phase B); v0.24 (off the locked six).

## Hypotheses

- **H_CPC_Computable** — within each omnibus substrate, brand-level CPC (defined brands) shows non-degenerate variance. Fails if degenerate in ≥4 of 5 substrates.
- **H_CPC_CrossCategory** — CPC differs systematically across the 5 omnibus substrates. Kruskal–Wallis, α = 0.05. Committed reporting rule: a significant or large effect is reported as-scored, no post-hoc reframing. Fails to reject if p ≥ 0.05.

## Predictions

High-recall incumbents carry defined, higher CPC; editorial/cultural-dense substrates (spirits) predicted less consistent than utilitarian (skincare, automotive); defunct / near-zero-recall brands resolve to undefined, not low.

## Deviations

Entry 0 released — nothing to log. The exclusions are clean pre-scoring non-comparability calls; the channel-agnostic generalization is declared here at r1, not amended at r2.
