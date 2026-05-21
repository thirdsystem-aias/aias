# DEVIATIONS — AIAS v0.19

**Phase:** v0.19
**Pre-reg tag:** `v0.19-prereg-r1`
**Pre-reg commit:** `2cbd36c6ed53b99c65490765d3d9f1a2eb49b890`

This document logs any departures from the pre-registered protocol that arise during Phase A or Phase B acquisition, or during scoring. Each entry is dated, anchored to a git commit reference, and routes per the DEVIATIONS Rules specified in §6 of `PRE_REGISTRATION_v0_19.md`.

The pre-registration carries six DEVIATIONS rules:

- **Rule 1** — Panel lock (no substitution post-lock; brands with C_P = 0/6 remain in panel)
- **Rule 2** — Provider model deprecation (closest-version successor + entry here)
- **Rule 3** — Recognition-floor cascade exhaustion (substantive finding; alternates NOT invoked)
- **Rule 4** — Within-cell C2 variance failure (NEW for v0.19; cell routes to UNDETERMINED; panel NOT substituted)
- **Rule 5** — Borderline classification stands (no retroactive reclassification of Focal or Final Audio)
- **Rule 6** — Cross-cultural robustness analysis required (Stax / HiFiMan exclusion analysis)

---

## Entries

### Entry 1 — Phase A Recognition saturation; both cells fail C2 modal-share check

**Date:** 2026-05-20
**Rule reference:** Rule 4 (Within-cell C2 variance failure, NEW for v0.19)
**Affected artifact(s):** Phase A scoring, H_C3_Within_Cell_Variance verdict matrix

**Description.** Phase A Recognition probe returned modal-share = 0.500 in Cell A_Heritage (4 of 8 brands at C_P = 6/6: Sennheiser, Beyerdynamic, Grado, Audio-Technica) and modal-share = 0.875 in Cell B_Boutique (7 of 8 brands at C_P = 6/6; only Spirit Torino at 5/6 below ceiling). Both cells fail the pre-registered C2 threshold of `cp_modal_share < 0.50`. Per DEVIATIONS Rule 4, both cells route H_C3 to UNDETERMINED. Panel is NOT substituted; the substantive finding stands: the audiophile-headphone substrate produces Recognition ceiling effects across both Heritage and Boutique tiers when the panel is populated with category-enrolled brands. Cell A_Heritage's failure at exactly the boundary (modal share = 0.500, not strictly less than 0.50, distinguished from PASS by a single brand at the ceiling) is itself a methodological finding regarding C2 operationalization sensitivity at mixed-shape distributions.

**Lock state.** Pre-reg tag `v0.19-prereg-r1` at commit `2cbd36c6ed53b99c65490765d3d9f1a2eb49b890` unchanged. No revision triggered.

**Downstream implications.**
- H_C3 verdict: **UNDETERMINED** (per §5.1 matrix; both cells fail C2 → routing).
- H_Recognition_Recall_Dissociation_Replication: **PARTIAL** (3 cases: ZMF Headphones, Spirit Torino, Final Audio — all Cell B_Boutique; independent of C2 status).
- H_CulturalFootprint_Dissociation_Sensitivity: 3 Type 1 cases (Audeze, HiFiMan, Dan Clark Audio — all Cell B_Boutique), 0 Type 2 cases (descriptive output; no verdict implication).
- Cross-cultural robustness (Rule 6) on Stax / HiFiMan reports "not applicable" because both cells failed C2; no Δρ computed. Cross-cultural confound exposure documented but unquantified for v0.19.
- C2 `modal_share < 0.50` operationalization documented in the v0.19 SSRN paper Limits section as candidate refinement for AIAS™ 1.0 methodology layer. Entropy-based or multi-statistic C2 specifications are candidate replacements; the strict-less-than boundary at exactly 0.500 in Cell A_Heritage is the empirical anchor motivating refinement.
- v0.20 substrate selection must produce within-cell Recognition variance below the 0.50 modal-share threshold in both cells. The Heritage × Boutique audiophile-electronics design does not satisfy this constraint and should not be re-tried without a substrate that includes mass-consumer brands below the category-recognition floor.

---

## Summary table

| Entry | Date | Rule | Title | Lock-state impact |
|---|---|---|---|---|
| 1 | 2026-05-20 | Rule 4 | Phase A Recognition saturation; both cells fail C2 modal-share check | Tag unchanged |
