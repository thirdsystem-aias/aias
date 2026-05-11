# DEVIATIONS — AIAS v0.13

This file records all methodology decisions made during v0.13 execution that differ from, clarify, or extend the locked pre-registration. Each entry is dated and references the affected pre-registration section. Entries are appended chronologically and not edited post-commit, except for filling in placeholders that are explicitly marked `[FILL]` at the time of writing.

---

## Entry 1 — Phase A pivot validation: §4.2 query-string amendment for YNAB

**Date.** 2026-05-11 (pre-lock).

**Affects.** Pre-registration §4.1 (Per-category pivots table), §4.2 (Pivot validation protocol — Query bullet). Personal finance category.

**Pre-reg status at the time of this entry.** Draft. No `v0.13-prereg` git tag yet. The pre-reg's Acquisition lock and Git commit fields remain `[FILLED AT LOCK]`. This entry documents a pre-lock correction to a drafting flaw surfaced by the Phase A validation step, which is itself part of the pre-lock drafting process per the pre-reg's design.

### What was originally specified

§4.2's Query bullet read:

> Pivot brand canonical name + standard category disambiguation if needed (e.g., `CeraVe`; `YNAB personal finance`).

The example treated `YNAB personal finance` as the disambiguated query string for the YNAB primary pivot.

### What was empirically observed

The initial Phase A validation run on 2026-05-11 was executed with the §4.2 example query string `YNAB personal finance` for the finance primary pivot. The SerpAPI Google Trends engine returned the response *"hasn't returned any results for this query"* across all three retry attempts. This is the same signal class as the E1a `notEnoughSearchVolume` flag defined in §5.4. The result is logged at:

- `data/phaseA_test/finance_primary_YNAB_2026-05-11T20-44-42.418271+00-00.json`
  (`phase_a_status: FAIL_API`, error: SerpAPI no-results)

Under Phase A's fallback logic, Quicken was tested as fallback and PASSed (mean 87.0, CV 11.0%):

- `data/phaseA_test/finance_fallback_Quicken_2026-05-11T20-45-00.989880+00-00.json`
  (`phase_a_status: PASS`)

CeraVe (skincare primary) PASSed in the same run:

- `data/phaseA_test/skincare_primary_CeraVe_2026-05-11T20-44-37.845133+00-00.json`
  (`phase_a_status: PASS`, mean 89.43, CV 7.77%)

A subsequent diagnostic check — executed outside the canonical Phase A validator script as a one-off Python invocation — issued the bare query `YNAB` against the same out-of-sample window (2026-04-13 to 2026-04-19, Worldwide). Result: 7 daily values `[89, 86, 79, 82, 100, 69, 69]`; mean 82.0; sd 11.08; CV 13.5%. PASS by both §4.2 criteria with comfortable margin on each. This diagnostic result is recorded here for transparency; it is not stored as a `phaseA_test/` JSON because it was not produced by the canonical validator.

### Methodology decision

§4.2's "if needed" clause is conditional: the disambiguation suffix is added only when bare-query disambiguation is empirically insufficient. The evidence demonstrates the opposite for YNAB — the disambiguated query suppressed the signal entirely, while the bare query produced PASS-quality signal with substantial margin on both criteria. Under §4.2 as written and properly interpreted, `YNAB` (bare) is the correct application of the rule; `YNAB personal finance` was a drafting flaw embedded in the §4.2 illustrative example, not a binding query specification.

The corrective action is:

1. Re-run the official Phase A validator with the corrected query string `YNAB` for the finance primary pivot, producing the canonical JSON record in `data/phaseA_test/`. CeraVe is re-validated in the same run (idempotent PASS expected).

2. Tighten the §4.2 Query bullet wording to remove the misleading example and make the "if needed" rule operationally explicit. New wording locked at this entry's commit:

   > **Query.** Pivot brand canonical name. Default is the bare brand name; category-disambiguation suffix added only if Phase A demonstrates the bare query returns insufficient signal AND a disambiguated query produces PASS-quality signal. The chosen query string per pivot is recorded in `data/phaseA_test/` JSONs and in §4.1.

3. Update §4.1 to record the canonical Phase A outcomes per category, including the YNAB result and a cross-reference to this entry.

4. Designate YNAB as the validated finance primary pivot at the v0.13-prereg lock.

5. Preserve the original failed-disambiguation JSON and the Quicken-fallback JSON in `data/phaseA_test/` as full audit trail. They are not deleted on re-run because the JSONs are timestamped and do not collide.

### Status of the corrective re-run

Re-run executed 2026-05-11T20:51 UTC. Both pivots PASS:

- Canonical CeraVe JSON: `data/phaseA_test/skincare_primary_CeraVe_2026-05-11T20-51-17.073555+00-00.json` — `phase_a_status: PASS`, mean 89.43, CV 7.77%. Replicates the original 2026-05-11T20:44:37 run within Trends sampling variance.
- Canonical YNAB JSON: `data/phaseA_test/finance_primary_YNAB_2026-05-11T20-51-22.483836+00-00.json` — `phase_a_status: PASS`, mean 82.00, CV 13.51%. Replicates the diagnostic bare-YNAB result within Trends sampling variance.
- `data/phaseA_summary.csv` overwritten with the canonical run; the original-run CSV is superseded but the per-pivot JSONs preserve the full audit trail.

### Files affected by this entry

| File | Change |
|---|---|
| `PRE_REGISTRATION_v0_13.md` §4.1 | Table updated with Phase A outcomes for Skincare and Personal finance. |
| `PRE_REGISTRATION_v0_13.md` §4.2 | Query bullet wording tightened (see Methodology decision §2). |
| `data/phaseA_test/` | 5 JSONs total — full audit trail: CeraVe primary × 2 runs, YNAB-disambiguated FAIL, YNAB-bare PASS, Quicken-fallback PASS. |
| `data/phaseA_summary.csv` | Overwritten with canonical Phase A run results. |
| `scripts/phaseA_validate_v13.py` | PIVOTS list line for finance primary changed from `"YNAB personal finance"` to `"YNAB"`. |

### Methodological reflection

Pre-registration discipline distinguishes pre-lock drafting corrections from post-lock deviations. This is a pre-lock drafting correction surfaced by the empirical validation step that the pre-reg itself prescribes. The full audit trail is preserved so any reviewer can verify the failed query, the diagnostic that identified the cause, the corrective re-run, and the wording change. Future AIAS pre-registrations should default to bare brand names for pivot queries unless prior evidence demonstrates need for disambiguation.

### Forward note for Phase B (YNAB-as-brand acquisition)

The Phase B disambiguation strategy for YNAB-as-brand (i.e., as a measured brand rather than as the pivot) is informed by this Phase A result: the bare query `YNAB` produces healthy signal at Worldwide region against the v0.13 wave windows, so Phase B should default to bare `YNAB` for YNAB's topic-ID resolution. Disambiguation only revisited if Phase B pytrends.suggestions() returns ambiguous results for bare `YNAB`. The decision is logged in `registries/topic_id_resolution_log_v0.13.csv` prior to acquisition lock.

---
## Entry 2 — Phase B outcome: Quicken Simplifi EXCLUDED_E1a; §5.2 finance B2 padding amendment

**Date.** 2026-05-11 (post-Phase-B, pre-acquisition-lock).

**Affects.** Pre-registration §3.5 (Personal finance apps brand registry membership at acquisition), §5.2 (Bundle composition per category — finance B2). Personal finance category.

**Pre-reg status at the time of this entry.** Locked at `v0.13-prereg` (commit `1a6294d`). This entry documents a post-lock pre-acquisition adjustment to bundle composition resulting from the §5.4 E1a mechanism operating as designed.

### What happened

Phase B (`scripts/phaseB_resolve_v13.py`) ran on 2026-05-11T21:22:39 UTC against the out-of-sample window 2026-04-13 to 2026-04-19, Worldwide. Two finance brands solo-failed and routed to E5 bundled rescue:

- **Quicken Simplifi** (pytrends-derived topic-ID `/g/11xvvz6wpg`): solo SerpAPI returned `notEnoughSearchVolume`. E5 bundled rescue result: ALL_ZERO across the 7-day window. Final tier: **EXCLUDED_E1a**. Audit trail at:
  - `data/phaseB_suggestions/Quicken_Simplifi.json`
  - `data/phaseB_validation/solo/Quicken_Simplifi.json`
  - `data/phaseB_validation/bundled/finance_e5_bundle_1.json`
- **Lunch Money** (pytrends-derived topic-ID `/g/11x_bjn3_l`): solo SerpAPI returned `notEnoughSearchVolume`. E5 bundled rescue result: nonzero. Final tier: **PASS_E5** with acquisition_query `/g/11x_bjn3_l`. Retained in acquisition with E5 flag.

The full canonical record is in `registries/topic_id_resolution_log_v0.13.csv`.

### Empirical observation

Quicken Simplifi is tagged `incumbent` in `registries/brands_finance.json`. Incumbent-tier brands falling below the E1a eligibility floor is unusual — most v0.6–v0.12 E1a exclusions have come from challenger-tier brands with naturally low search volume. Simplifi's exclusion at both the chosen pytrends topic-ID and the bundled rescue suggests one or more of:

1. The chosen topic-ID `/g/11xvvz6wpg` may not capture the full set of "Quicken Simplifi" or "Simplifi" searches that real users issue. Alternative queries (e.g., bare `Simplifi`, `Quicken Simplifi app`) were not tested in Phase B; topic-ID resolution is single-pass per pre-reg §5.2.
2. Simplifi's mass-market footprint may be smaller than its `incumbent` registry tier suggests. Simplifi is Intuit/Quicken's modern subscription replacement for the legacy Mint product (Mint was decommissioned in September 2025 and Simplifi was positioned as its successor); residual brand-search volume from that handoff may not have transferred at the magnitude anticipated when the registry was tier-labelled.
3. Worldwide search volume for Simplifi may be substantially US-concentrated such that the Worldwide region returns insufficient signal, while US-region acquisition (the §13 sensitivity arm) might have shown signal. Phase B is Worldwide-only per §5.4; this is a known design choice, not a deviation.

These hypotheses are recorded here as forward-pointers for a possible v0.14+ re-investigation. The v0.13 analysis treats Simplifi as EXCLUDED_E1a per the locked pre-reg without re-opening Phase B post-hoc.

### Cascade: §5.2 B2 bundle composition amendment

Per pre-reg §5.2, finance B2 was defined as: `YNAB + Quicken Simplifi + Rocket Money + PocketGuard + Goodbudget` (5 slots, including pivot). With Quicken Simplifi excluded by E1a, B2 has 3 non-pivot brand members + pivot = 4 slots. Per the v0.13 padding rule (§5.2, incumbent-tier brand-volume-comparable rule), the script `scripts/acquire_trends_v13.py` is amended to pad B2's vacated slot with NerdWallet (already an incumbent in B1, parallel to PAD_FIN_EMPOWER in B4):

Amended B2 composition:

> YNAB (pivot) + Rocket Money + PocketGuard + Goodbudget + `__pad_NerdWallet`

The padding entry uses NerdWallet's canonical acquisition_query (looked up from `topic_id_resolution_log_v0.13.csv`), so NerdWallet appears in B1 as the canonical measurement and in B2 as scale-anchoring padding. Per `rescale_trends_v13.py` (inherited from v0.12 logic via `is_padding` flag), the B2 padding entry contributes zero rows to NerdWallet's per-brand within-window aggregation — only B1's canonical entry counts.

### Files affected by this entry

| File | Change |
|---|---|
| `scripts/acquire_trends_v13.py` | Added `PAD_FIN_NERDWALLET = ("__pad_NerdWallet", "NerdWallet")` constant. Replaced B2 members: removed `"Quicken Simplifi"`, appended `PAD_FIN_NERDWALLET`. |
| `data/phaseB_suggestions/` | 47 per-brand JSONs (audit trail). |
| `data/phaseB_validation/solo/` | 46 per-brand solo JSONs + 3 Mint-strategy JSONs. |
| `data/phaseB_validation/bundled/` | 1 E5 bundle JSON. |
| `registries/topic_id_resolution_log_v0.13.csv` | Canonical Phase B record; 47 rows, 14+1+1 PASS / PASS_E5 / EXCLUDED_E1a (skincare 31/0/0; finance 14/1/1). |

### Effect on H1–H8

- **H1, H2, H3, H4 (finance):** Quicken Simplifi is dropped from the finance brand set for these per-category tests. Effective finance brand set = 15 brands; analyses proceed against this set with the n_eligible threshold checks per §3.6a.
- **H6 (Linear-style / Todoist-style cross-category):** Simplifi's absence from the finance scatter is recorded but does not affect H6 detection thresholds (the test is per-category, not per-brand).
- **H7 (Three-regimes accounting):** Finance category's regime classification proceeds on the 15-brand set. Per pre-reg §3.6a, the n_PASS / n_matched_subset floor for descriptive-only routing is 0.6; with 15 of 15 PASS-eligible brands now in the acquisition set, the floor is met by design.
- **H8 (Mint phantom-persistence):** Unaffected. Mint's Phase B disambiguation (Entry 1's pattern) resolved separately from Simplifi.

### Methodological reflection

The E1a mechanism in §5.4 is designed to surface exactly this kind of empirical observation pre-acquisition. The Simplifi result is the pre-reg working as intended — not a deviation in the strict sense. This entry documents the bundle-composition cascade for full transparency and records the Simplifi observation as a forward-pointer for v0.14+ investigation.

---
---

## Entry 3 — Three-regimes taxonomy under-covers the 5-category panel; fourth empirical regime emergent

**Date:** 2026-05-11
**Status:** Post-acquisition empirical finding. No methodology change. No pre-registered hypothesis is re-stated.
**Affected sections of pre-registration:** §2 H7 (three-regimes accounting); §10 (regime taxonomy and Category-Scale Mismatch); §11 (phantom-persistence handling); §3.6a (descriptive-only routing for olive oil).

### 3.1 Summary

The v0.13 construct-validity expansion was designed to test whether the three-regime taxonomy derived from v0.12's 3-category panel (PM software, premium olive oil, running shoes) generalizes to a 5-category panel that adds premium facial skincare and personal finance apps. The pre-registered H7 hypothesis required every category in the v0.13 panel to classify cleanly into exactly one of three regimes: Marginal-direct (Regime 1), Age-mediated strong (Regime 2), or Scale-mismatch (Regime 3).

The empirical result is that **three of five categories classify cleanly into the predicted regimes, but the two new categories — skincare and finance — fall outside all three**. This is not a methodological problem; it is the construct-validity test functioning correctly. The three-regime taxonomy was inferred from a smaller panel and the wider panel reveals that the taxonomy under-covers the empirical landscape. A fourth empirical regime emerges in the two new categories.

H7 is therefore FALSIFIED at 3-of-5 clean classifications against a required-all rule. This is recorded as a successful construct-validity finding rather than as a framework defect. The four-regime extension claim becomes a substantive contribution of the v0.13 paper.

### 3.2 What the pre-registration predicted

Section 2 H7 of the pre-registration anticipates three regimes:

| Regime | Empirical signature | Theoretical interpretation |
|---|---|---|
| **Regime 1 — Marginal direct** | ρ ∈ [0.35, 0.65] both waves; bivariate-minus-partial decrement ≤ 0.15 both waves; n_eligible ≥ 10 | Brand-age and tier covariates explain little; AI Presence and consumer-search rank align directly |
| **Regime 2 — Age-mediated strong** | ρ > 0.65 both waves; decrement > 0.25 both waves; n_eligible ≥ 10 | Strong bivariate signal is mostly absorbed by brand-age and tier covariates; the AI Presence/Trends co-rank is largely a downstream consequence of the underlying maturity gradient |
| **Regime 3 — Scale-mismatch** | n_eligible < 0.6 × n_matched_subset at either wave | Trends measurement layer fails to register the category's brand-level differentiation; AI Presence may be informative but Trends-paired analysis is not |

The pre-registration further committed to declaring H7 confirmed only if every category in the panel classifies cleanly (i.e., into exactly one regime, no boundary flag within 0.05 of any threshold). This is a strict rule and was chosen deliberately: weaker rules cannot detect taxonomy under-coverage.

### 3.3 What the data show

| Category | n_elig (t1/t2) | Bivariate ρ (t1/t2) | Partial ρ (t1/t2) | Decrement (t1/t2) | Classification |
|---|---|---|---|---|---|
| PM software | 17 / 18 | 0.506 / 0.482 | 0.417 / 0.434 | 0.089 / 0.048 | **Regime 1** (clean) |
| Olive oil | 8 / 8 | 0.168 / −0.095 | 0.011 / −0.249 | — | **Regime 3** (via §3.6a) |
| Running | 12 / 12 | 0.808 / 0.786 | 0.466 / 0.488 | 0.342 / 0.298 | **Regime 2** (boundary-flagged on t2 decrement) |
| Skincare | 28 / 28 | 0.282 / 0.332 | −0.205 / −0.117 | 0.487 / 0.449 | **Unclassifiable** (boundary-flagged on t2 ρ) |
| Finance | 13 / 13 | 0.168 / 0.094 | −0.159 / −0.287 | 0.327 / 0.381 | **Unclassifiable** |

Three categories classify cleanly into the predicted regimes. Two do not. Per the strict H7 rule, the hypothesis is FALSIFIED at 3-of-5.

#### Boundary flags

Two of the five categories raise the boundary flag (within 0.05 of a regime threshold):

- **Running** sits at the lower edge of Regime 2: decrement_t2 = 0.298 against the 0.25 minimum, Δ = 0.048. The age-mediated-strong pattern is real and reproducible across waves, but at t2 the residual partial ρ has lifted enough that the decrement is one statistical sneeze from dropping under the regime floor.
- **Skincare** sits at the lower edge of Regime 1: bivariate ρ_t2 = 0.332 against the 0.35 floor, Δ = 0.018. Skincare is *just outside* the marginal-direct band. With slightly cleaner Trends measurement (or a small model-mix shift) it could enter Regime 1 — but as measured under the v0.13 protocol it does not.

Neither boundary flag is a measurement defect. Both are substantive empirical positions on the regime map.

### 3.4 The fourth regime: empirical signature

The two unclassifiable categories share a distinctive empirical pattern that is not anticipated by Regimes 1, 2, or 3:

- **n_eligible is well above the hard floor.** Skincare has 28 of 31 brands eligible at both waves (90.3%); finance has 13 of 15 live brands eligible (86.7%). Neither category fails the Trends measurement layer in a way that would route it to Regime 3 via §10's n-fraction criterion.
- **Bivariate ρ is positive but well below 0.35.** Skincare: 0.282 / 0.332. Finance: 0.168 / 0.094. The bivariate signal is detectably present but at less than half the magnitude required for Regime 1.
- **Partial ρ is negative.** Skincare: −0.205 / −0.117. Finance: −0.159 / −0.287. After controlling for brand age and tier, the residual association is *negative* — meaning the covariates absorb the entire bivariate signal and then some.
- **Decrement exceeds Regime 2's threshold.** Bivariate-minus-partial in both categories is 0.30–0.49. That is to say: by the decrement criterion alone, both categories would qualify as "covariates absorb a lot." But the *starting* bivariate ρ is so low that the absorbed quantity is small in absolute terms, and the residual partial ρ ends up below zero.

This is a structurally distinct pattern. Skincare and finance have *moderate-to-large brand panels* with *small-positive bivariate AI/Trends rank correlation* that is *fully attributable to brand age and tier covariates*. The framework's existing regime taxonomy has no slot for this.

The provisional naming convention for the v0.13 paper is **Regime 4 — Covariate-saturated weak**: positive but weak bivariate ρ, fully absorbed by the covariates with negative residual. The theoretical interpretation is that in these categories, AI mediation surfaces brands that match the underlying maturity/tier gradient but does not produce a Trends-rank co-movement beyond what age and tier alone would predict.

This naming is provisional, deferred to the v0.13 paper for formal definition. Until that paper is in circulation, the categories are recorded as "Unclassifiable against the v0.12 three-regime taxonomy" in canonical scoring outputs.

### 3.5 Mint phantom-persistence canonical confirmation (H8)

H8 was pre-registered to evaluate whether Mint — Intuit's personal finance app, formally shut down in September 2025 — would continue to surface in AI Presence measurement at strength while showing zero Trends signal, seven to nine months after operational closure. The three-condition diagnostic per pre-registration §2 H8:

| Condition | Pre-registration requirement | v0.13 measurement | Status |
|---|---|---|---|
| C1 — AI Presence ≥ 5.0% both waves | Mint must show ≥ 5% AI Presence at t1 (29-Apr) and t2 (7-May) | t1: 44.79%; t2: 41.67% | ✓ Satisfied |
| C2 — AI top-5 both waves | Mint must rank in top-5 by AI Presence at both waves | t1: rank 5; t2: rank 5 | ✓ Satisfied |
| C3 — NOT Trends top-5 either wave | Mint must rank outside top-5 by Trends rescaled mean at both waves | t1: not E1b-eligible; t2: not E1b-eligible | ✓ Satisfied via §11 trivial-satisfaction route |

All three conditions hold. H8 is CONFIRMED. This is the cleanest phantom-persistence anchor observed in the AIAS programme to date — Mint is a textbook case.

The §11 trivial-satisfaction route applies because Mint's Trends signal is undetectable in both regions at both waves (worldwide rescaled mean = 0.0; US rescaled mean = 0.0). Pre-registration §11 specifies that when a phantom candidate is not E1b-eligible (no Trends signal at all), Condition C3 is trivially satisfied — being outside the top-5 by Trends rank is logically guaranteed when the brand has no Trends rank at all. The v0.13 H8 confirmation thus rests on the canonical pattern: substantial AI Presence + complete Trends absence + persistence across the wave gap.

### 3.6 Secondary findings worth recording

#### 3.6.1 Lunch Money — sub-category Worldwide-vs-US scale mismatch in finance

Lunch Money is WW-ineligible (rescaled mean 0.0 at both waves) but US-eligible at both waves. Its AI Presence is low (t1: 1.0%; t2: 6.2%) and rises slightly across the wave gap. Phase B disposition was PASS_E5 (E5 bundled rescue at the diagnostic worldwide window), but the wave-window rescaling subsequently returned 0.0 worldwide.

This is a region-of-measurement scale mismatch rather than a phantom: Lunch Money is operationally active (no shutdown), AI Presence is detectable, US Trends signal is detectable, but Worldwide Trends signal is below the display threshold. The brand is regionally scoped — its consumer-search base appears concentrated in the United States — and the worldwide aggregation underweights its visibility.

This is not pre-registered as a separate hypothesis. It is recorded here as descriptive observation. Inclusion in the v0.13 paper's discussion is at the author's discretion.

#### 3.6.2 SK-II and Vanicream — sub-category scale mismatch within skincare

Two skincare brands show the same Worldwide-vs-US asymmetry as Lunch Money:

- **SK-II:** WW 0.0 / 0.0; US 0.30 / 0.62
- **Vanicream:** WW 0.0 / 0.0; US 1.13 / 1.55

SK-II is the J&J/P&G premium brand historically concentrated in East Asia; Vanicream is a niche US-domestic dermatologist-recommended brand. Both have substantive AI Presence but Worldwide Trends signal below display threshold. They contribute to the skincare US-region n (n=30) but not the Worldwide n (n=28).

The presence of intra-category scale mismatch in two of the four confirmatory categories (finance: Lunch Money; skincare: SK-II, Vanicream) is worth noting in the v0.13 discussion as evidence that scale mismatch is not exclusively a between-category phenomenon (as in olive oil's §3.6a routing) but operates at the brand level within categories too. This was not pre-registered and is descriptive only.

#### 3.6.3 Height — first observed inter-wave eligibility transition in the programme

The PM software brand Height crosses the eligibility floor between t1 and t2:

- WW t1: mean 0.0, eligible False
- WW t2: mean 1.97, eligible True

This is the first inter-wave eligibility transition observed across all AIAS measurement to date (v0.6 through v0.13). The brand's Worldwide Trends signal lifted from below-display to above-display over the eight-day wave gap. n_eligible for PM software accordingly increments from 17 to 18 between t1 and t2.

The transition does not affect H1-H4 evaluation logic — the per-wave correlations are computed on each wave's eligible set independently — and the increment in n is small enough that it changes none of PM software's hypothesis outcomes. It is recorded here for programme continuity: future versions may want to track eligibility transitions as a separate descriptive measure.

### 3.7 Methodological notes

#### 3.7.1 Running has four brands without `brand_age_years` (carry-forward from v0.12)

Four running registry brands lack founding-year data in `brand_age_sources_v0.13.csv`: Mizuno, Reebok, Tracksmith, Under Armour. These rows have `NaN` in the `brand_age_years` column and are silently dropped by the `correlations()` function via `dropna(subset=[..., "brand_age_years", "tier_ordinal"])` whenever partial-Spearman computation is invoked.

This is **inherited from v0.12** and is not a v0.13-induced gap. The same four brands lacked age data in `brand_age_sources_v0.12.csv` and were dropped in identical fashion by v0.12's `score_v12.py`. The running n_eligible = 12 reported in v0.13 matches v0.12's value exactly, confirming that the v0.13 reuse-arm analysis is methodologically identical to v0.12.

**Action:** This DEVIATIONS entry serves as notice that future programme phases (v0.14 onwards) should source `brand_age_years` for these four running brands. The gap does not affect any v0.13 conclusion but is a programme-hygiene item for the next acquisition cycle.

A fifth running brand, Saucony, has age data but is not Trends-eligible. This is a substantive E1b outcome, not a data gap. Saucony's Worldwide Trends signal is below the alignment-floor threshold and the brand is correctly routed out of correlation analysis at both waves.

#### 3.7.2 Skincare and finance brand-age data are DRAFT values

The 47 new brand-age entries added in v0.13 (`brand_age_sources_v0.13_new_brands.csv`, appended to v0.12's age file to produce `brand_age_sources_v0.13.csv`) carry "DRAFT — verify" in the notes column. Founding years are drawn from common-knowledge brand histories and were not source-verified against authoritative URLs at acquisition time.

The H1-H8 results in this run are computed on the DRAFT values. For publication-grade values, the author commits to source-verifying each of the 47 entries before SSRN deposit and replacing the notes-column flag with an authoritative source URL. Any founding-year corrections discovered during verification will be applied via a subsequent re-run of `score_v13.py` and recorded as a v0.13 amendment.

Pre-registration §6 specifies brand_age_years as a covariate in the partial-Spearman computation. Changes to individual brand ages would propagate into the partial ρ values for the affected categories. The current best estimate is that no single founding-year correction would move skincare or finance from "Unclassifiable" into Regime 1 — both categories are too far from the regime thresholds for a 1- to 2-year age correction on a single brand to change classification. But the verification step is committed regardless.

### 3.8 Impact on canonical hypothesis evaluation

This DEVIATIONS entry **does not modify** any pre-registered hypothesis status:

- H1 per category remains evaluated as pre-registered (FALSIFIED for PM/skincare/finance, CONFIRMED for running, INDETERMINATE for olive oil).
- H2, H3, H4 likewise unchanged.
- H5 (v0.12 marginal signature, 3-of-effective-N): FALSIFIED at 1-of-4.
- H6 (Linear+Todoist co-presence, 4-of-effective-N): FALSIFIED at 1-of-4.
- H7 (three-regimes clean classification): FALSIFIED at 3-of-5.
- H8 (Mint phantom-persistence): CONFIRMED.

The H7 falsification is the principal substantive observation. The v0.13 paper will frame this as a successful construct-validity test that exposes a previously-unrecognized fourth regime. The strict all-categories-clean rule was chosen precisely so that taxonomy under-coverage could be detected; it was detected; the framework's three-regime structure was found to be incomplete.

### 3.9 Implications for the v0.13 SSRN paper

The Results section of the v0.13 paper will report H1-H8 outcomes as specified above without modification.

The Discussion section will frame the principal finding in three layers:

1. **Construct validity result.** v0.13 was designed to test whether the v0.12 three-regime taxonomy holds in an expanded panel. It does not. Two of the two new categories occupy a regime not anticipated by v0.12. The taxonomy under-covers the wider empirical landscape.
2. **The fourth regime.** Skincare and finance share a distinctive signature (moderate-to-large n, low bivariate ρ, fully covariate-absorbed) that warrants formal regime status. Provisional name: Covariate-saturated weak. The paper will offer this as a post-registration extension claim — not as a tested hypothesis, but as an inductive observation supported by two independent categories that emerged consistently.
3. **The PM software anchor.** What looked in v0.12 like a candidate cross-category regularity — the marginal-direct pattern with Linear-style and Todoist-style brand co-presence — turns out to be PM-specific. H5 and H6 are both falsified at 1-of-4 in v0.13. The dual-style co-presence and the marginal-direct ρ band may both be structural properties of project-management software's brand ecology, not general regularities. This is a narrowing of the v0.12 claim's scope, not a refutation of v0.12 itself.

The pooled rank-within-category sensitivity (ρ ≈ 0.46-0.48, p ≤ 10⁻⁴, n ≈ 70-71) is the cross-category secondary headline: AI Presence and Trends rank-orders DO co-vary moderately across categories at the rank-within-category level, even though the strength of the within-category relationship is heterogeneous across regimes.

### 3.10 Implications for AIAS Protocol v1.1 and future programme phases

The AIAS Presence Measurement Protocol v1.1 (SSRN 6722319) describes the measurement methodology that produces the per-brand AI Presence values feeding into v0.13. The four-regime finding does not require any change to v1.1's measurement protocol — measurement methodology is upstream of regime taxonomy and the AI Presence values themselves are unaffected.

The four-regime finding does, however, suggest two action items for the AIAS programme:

1. **Regime taxonomy formalisation.** A short methodology note formalizing Regime 4 — the covariate-saturated weak pattern — should be prepared for the AIAS methodology paper (slated to follow Tri-System paper clearance). This entry's §3.4 contains the empirical signature; the methodology note would specify a formal pre-registration-grade definition with thresholds analogous to those for Regimes 1, 2, and 3.
2. **Phase 4 candidate selection.** Future cross-category phases should sample at least one Regime 4 candidate alongside Regime 1/2/3 candidates to verify that the four-regime structure is stable beyond skincare and finance. Categories with high brand-age dispersion and weak prima-facie AI Presence/Trends rank alignment would be appropriate. Premium tea remains a Phase 3 candidate; whether it is Regime 3 or Regime 4 is empirically open until measured.

### 3.11 Closing note

The empirical pattern reported here was not anticipated at pre-registration lock. The pre-registration's strict all-categories-clean rule for H7 was the safeguard that permitted detection. The four-regime emergence is a *result of the construct-validity test functioning as designed* — not evidence of methodological compromise. v0.13 is recorded as a productive falsification: a pre-registered hypothesis was tested against new data, failed at a structurally informative threshold, and surfaced an empirical pattern that the framework's prior version could not have produced on its own.

No retroactive modification of v0.12 is contemplated. The v0.12 paper's three-regime taxonomy stands as the description of the 3-category panel it was inferred from. The v0.13 paper documents that the taxonomy under-covers the wider 5-category panel and proposes an extension.

— Pablo Ulpiano González Castro
2026-05-11
