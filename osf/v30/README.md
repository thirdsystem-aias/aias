# AIAS™ v0.30 (CPC.01) — Consistency Component: Instrument-Specification Pilot

**"Recognition Saturates, Consistency Doesn't."** First pilot specifying the AIAS Consistency
component (CPC) as the cross-model dispersion of a brand's recall signal, tested on skincare,
cosmetics, and automotive.

## Verdicts (lock: v0.30-results-r2)
- **F1 H_CPC_Computable — CONFIRMED.** Recall coverage 79% / 79% / 62% vs recognition 17% / 0% / 4%.
- **F2 H_CPC_LevelConfound — UNDETERMINED.** Testable only in skincare (ρ_raw = −0.47, p = .04);
  cosmetics & automotive saturate the recognition level variable.
- **F3 H_CPC_LevelCorrected — UNDETERMINED.** Skincare: −0.47 → −0.13 (72% attenuation), but < 2
  testable substrates. Bhatia–Davis correction carried forward as provisional working normalization.
- **F4 H_CPC_SubstrateVariation — CONFIRMED.** Kruskal–Wallis H = 14.24, p < 0.001.

## Reused inputs (no new model queries)
Phase A recognition + Phase B two-channel recall from v0.20 skincare (osf.io/ec6wh/v20; SSRN 6811441),
v0.21 cosmetics (v21; 6815378), v0.22 automotive (v22; 6829118). Input integrity hashes in
v30_run_log.md. Six-model panel: Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o-mini,
Gemini 2.5 Flash, Gemini 2.5 Flash Lite. Methodology lock v1.6 (SSRN 6816340).

## Pre-registration
Analysis pre-registration locked before scoring: v0.30-prereg-r1 → r2 (substrate-set amendment to the
doubly-homogeneous trio; DEVIATIONS Entry 1). All F1–F4 definitions and thresholds unchanged across r1→r2.

## Manifest
- prereg/ — locked pre-registration content module + mega-prompt
- data/v30_cpc.csv — per-brand CPC scores; v30_cpc_verdicts.json — per-hypothesis verdicts + stats
- v30_run_log.md — input certification (hashes) + scoring log
- scripts/score_v30.py — scoring code
- registries/ — the three reused 24-brand registries
- figures/ — chart_30_{coverage,confound,correction,variation}.pdf
- reports/ — brand-format report PDF; paper/ — SSRN paper PDF

## Citation
González Castro, P. U. (2026). *Recognition Saturates, Consistency Doesn't: An Instrument-Specification
Pilot of the AIAS Consistency Component (CPC) across Skincare, Cosmetics, and Automotive (v0.30 /
CPC.01)*. Third System™. SSRN [id pending].
