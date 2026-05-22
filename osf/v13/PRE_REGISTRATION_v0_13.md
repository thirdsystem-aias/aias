# AIAS v0.13 Pre-Registration

**Cross-Category Construct-Validity Panel: Five-Category Three-Regimes Accounting and Phantom-Brand Persistence**

---

| | |
|---|---|
| Programme | AIAS Measurement Programme |
| Phase | Phase 3 expansion (last before Phase 4 component expansion) |
| Acquisition lock | `[FILLED AT LOCK]` (UTC) |
| Git commit | `[FILLED AT LOCK]` |
| Git tag | `v0.13-prereg` |
| Pre-registration author | Pablo Ulpiano González Castro |
| Affiliations | SVA MPS Branding Program (primary academic); Third System™ (research entity) |
| ORCID | 0009-0003-8968-9990 |
| Protocol version | AIAS Presence Measurement Protocol v1.1 (SSRN 6722319, unchanged from v0.9 onward) |
| Reuses inputs from | v0.9 AI Presence rates (SSRN 6736878); v0.12 Trends data for 3 of 5 categories (osf.io/ec6wh/files/osfstorage/v12/) |

---

## §1. Pre-Registration Scope and Timing

v0.13 is the five-category cross-category construct-validity panel that builds directly on v0.12's three-category finding of three distinct empirical regimes (SSRN 6748341). The pre-registration locks the analysis plan prior to any new Trends acquisition call against the v0.13 wave windows.

The v0.13 design has two operational arms operating in parallel:

**(a) The reuse arm.** Trends data for three categories (project management software, premium running shoes, premium olive oil) is taken verbatim from the v0.12 deposit at osf.io/ec6wh/files/osfstorage/v12/. No re-acquisition; the analysis runs against v0.12's pivot-rescaled per-brand within-window values. The v0.13 hypothesis tests for these three categories are accordingly tests of the same data under a new analysis frame (five-category cross-section rather than three-category cross-section) rather than independent longitudinal re-tests at a new time point. This is disclosed transparently throughout the analysis and reporting.

**(b) The fresh-acquisition arm.** Trends data for two new categories (premium facial skincare, personal finance apps) is acquired fresh under this pre-registration, against v0.12's wave windows (t₁: 27 April – 3 May 2026; t₂: 4 May – 10 May 2026). The acquisition is timed for a single locked SerpAPI session covering both regions (Worldwide + US) and both waves, matching v0.12's acquisition pattern.

The pre-registration as a whole locks all eight hypotheses, all routing rules, all eligibility flags, and all sensitivities before either (a) or (b) is executed against v0.13's analysis pipeline. The combined arms are reported under a single v0.13 manuscript and OSF deposit.

---

## §2. Hypotheses

Eight pre-registered hypotheses, six per-category (H1–H4) extended to five categories and two cross-category (H5–H6) extended to n = 5, plus two new cross-category hypotheses (H7 three-regimes accounting, H8 phantom-brand persistence).

All thresholds, operational definitions, and conjunction rules are locked at this commit. Any post-hoc adjustment to any threshold or rule is disclosed explicitly in the v0.13 report and treated as an exploratory finding rather than a confirmatory result.

### H1 — Cross-Sectional Construct Validity (per category)

**Claim.** Per-brand AI Presence rate co-varies with per-brand Google Trends search-interest index at sufficient strength to support the AI Availability construct, in each of the five v0.13 categories considered independently.

**Operationalization.** Spearman ρ across the eligible brand set per category per wave.

**Decision rule per category.** Confirmed if ρ > 0.5 AND p₁ₜ < 0.05 at BOTH waves. Otherwise falsified for that category. Both-waves conjunction provides built-in family-wise error rate control at p ≈ 0.0025 per category.

**Applicability.** Per-category H1 evaluates each of the five categories independently. Categories routing to descriptive-only per §3.6a carry no per-category H1 inference.

### H2 — Correlation Stability (per category)

**Claim.** The H1 correlation strength is stable across the t₁ → t₂ interval in each category.

**Operationalization.** |Δρ| = |ρ_t₂ − ρ_t₁|.

**Decision rule per category.** Confirmed if |Δρ| ≤ 0.15. Otherwise falsified for that category. Tolerance calibrated to absorb sampling variance at small n while detecting meaningful instability.

**Applicability.** Per-category H2 evaluates each of the five categories independently. Categories routing to descriptive-only per §3.6a carry no per-category H2 inference. For the three reuse-arm categories, H2 is a re-statement of v0.12's already-deposited finding under v0.13's analysis frame; no new information is generated.

### H3 — Leaderboard Directional Consistency (per category)

**Claim.** Brands ranked top-3 by AI Presence are also among the top-5 by Trends, at each wave, in each category.

**Operationalization.** All 3 of the per-category AI-top-3 brands appear in the per-category Trends top-5, at both waves.

**Decision rule per category.** Confirmed if 3 of 3 AI-top-3 brands clear the Trends top-5 bar at both waves. Otherwise falsified for that category.

**Applicability.** Per-category H3 evaluates each of the five categories independently. Categories routing to descriptive-only carry no per-category H3 inference.

### H4 — Covariate-Controlled Correlation (per category)

**Claim.** The H1 correlation survives partialling out brand age and within-category competitive density.

**Operationalization.** Spearman correlation on rank residuals after OLS on rank-transformed covariates (brand age in years; tier ordinal incumbent=1 / mid=2 / challenger=3). df corrected for k = 2 covariates.

**Decision rule per category.** Confirmed if partial ρ > 0.5 AND p₁ₜ < 0.05 at BOTH waves. Otherwise falsified for that category.

**Applicability.** Per-category H4 evaluates each of the five categories independently. Categories routing to descriptive-only carry no per-category H4 inference.

### H5 — Cross-Category Generalisation of v0.12 Marginal Signature

**Claim.** The v0.12 PM-software construct-validity signature (Spearman ρ ∈ [0.35, 0.65], H3 falsified at 1 of 3 both waves, H6 confirmed) generalises across categories.

**Operationalization.** Categories matching the v0.12 marginal signature defined as: ρ ∈ [0.35, 0.65] at both waves AND H3 falsified at 1 or 2 of 3 both waves AND at least one Linear-style brand surfaces.

**Decision rule.** Confirmed if 3 or more of the 5 v0.13 categories (or 3 or more of the confirmatory-eligible categories if any route to descriptive) match the v0.12 marginal signature at both waves. Otherwise falsified.

**Applicability.** Cross-category. Categories routing to descriptive-only contribute 0 of N to the numerator and are excluded from the denominator (per the effective N rule at v0.12).

### H6 — Cross-Category Diagnostic-Case Detection

**Claim.** Linear-style brands (AI ≥ 50% AND Trends ≤ 5) AND Todoist-style brands (AI ≤ 5% AND Trends ≥ 20) surface at both waves in each confirmatory-eligible category.

**Operationalization.** Per category: presence of at least one brand matching the Linear-style box at both waves AND at least one brand matching the Todoist-style box at both waves.

**Decision rule.** Confirmed if 4 or more of the 5 v0.13 categories (or 4 or more of the confirmatory-eligible categories) show both Linear-style and Todoist-style brands at both waves. Otherwise falsified.

**Applicability.** Cross-category. Categories routing to descriptive-only contribute 0 of N to the numerator and are excluded from the denominator. The asymmetric falsification mode (Linear-style present, Todoist-style absent — as observed in v0.12 running shoes) is recorded separately as a categorical observation about each category's boundary structure.

### H7 — Three-Regimes Accounting at n = 5 (NEW)

**Claim.** The three empirical regimes documented in v0.12 (Marginal-direct; Age-mediated strong; Scale-mismatch) account for the construct-validity behaviour of all five v0.13 categories when defunct/phantom brands (see H8) are excluded from the analysis.

**Operationalization.** Each of the 5 v0.13 categories classifies into exactly one of three regimes by the following decision tree applied to the matched-subset eligible brand set:

- **Regime 1 — Marginal direct.** Bivariate ρ ∈ [0.35, 0.65] at BOTH waves AND (bivariate ρ − partial ρ) ≤ 0.15 at both waves AND n_eligible ≥ 10. (PM software's v0.12 signature.)

- **Regime 2 — Age-mediated strong.** Bivariate ρ > 0.65 at BOTH waves AND (bivariate ρ − partial ρ) > 0.25 at both waves AND n_eligible ≥ 10. (Running shoes' v0.12 signature.)

- **Regime 3 — Scale-mismatch.** n_eligible (matched-subset brands clearing E1b at either wave) < 0.6 × n_matched_subset AT EITHER WAVE. (Olive oil's v0.12 signature; routes the category to descriptive-only per §3.6a.)

A category is **unclassifiable** if it satisfies the criteria for two regimes simultaneously OR if it satisfies the criteria for none. A category is **boundary** if it sits within 0.05 of any regime threshold at either wave.

**Decision rule.** Confirmed if every v0.13 category classifies cleanly (not unclassifiable, not boundary) into exactly one of the three regimes. Otherwise falsified.

**Applicability.** Cross-category. Mint (and any other registered defunct/phantom brand) is excluded from H7 regime classification before the per-category statistical tests are computed; H7 is a test of the regime taxonomy for live brands only. Phantom-brand behaviour is tested separately by H8.

**Rationale.** v0.12 documented three regimes in three categories. The question H7 asks is whether the regime taxonomy is a stable population property of categories or a v0.12-specific coincidence. At n = 5, if even one category resists classification or shows mixed indicators, the taxonomy is not yet stable enough to bear theoretical weight for the Tri-System Brand Growth framework's separability claims.

### H8 — Mint Phantom-Brand Persistence (NEW)

**Claim.** Mint (Intuit; decommissioned September 2025) exhibits the four-regime phantom-persistence empirical signature in personal finance: high AI Presence at both waves despite the brand's operational non-currency, combined with construct-divergence in the phantom direction (AI Presence rank exceeds Trends rank).

**Operationalization.** Three conjunctive conditions:

- **Condition 1.** Mint AI Presence ≥ 5.0% at BOTH waves. (Establishes phantom presence in AI substantively above the eligibility floor.)
- **Condition 2.** Mint is ranked in the top-5 by AI Presence in personal finance at BOTH waves. (Establishes phantom presence in AI at competitive-leadership magnitude, not just trace levels.)
- **Condition 3.** Mint is NOT ranked in the top-5 by Trends rescaled mean in personal finance at EITHER wave. (Establishes construct divergence in the phantom direction — AI persistence > consumer-search persistence post-shutdown.)

**Decision rule.** Confirmed if all three conditions hold. Otherwise falsified.

**Applicability.** Personal finance specifically. The H8 prediction is anchored to Mint as the unique post-shutdown phantom case in the v0.13 brand registry. If H8 confirms, the personal finance category instances a fourth empirical regime (Phantom-persistence) alongside the three v0.12 regimes — operationally defined by H8's signature. If H8 falsifies, the Mint phantom mechanism is more constrained than v0.7 / v0.10 documented or has decayed in the wave windows.

**Reference.** Mint phantom persistence at gross AI Presence has been measured longitudinally in v0.7 (SSRN 6721779) and v0.10 (SSRN 6741163), with stable persistence at 41–44% gross at the matched-subset level. H8 extends this to a construct-validity claim by predicting the specific phantom-construct-divergence signature.

---

## §3. Categories and Routing Rules

Five categories evaluated. Brand registries frozen at the deposited states referenced below.

### §3.1 Project management software

Registry: `registries/brands_pm.json` (v0.6 final state; 19 brands).

Confirmatory expectations from v0.12: Regime 1 (Marginal direct), H1 falsified at the 0.5 magnitude bar at one wave, H2 confirmed, H3 falsified at 1 of 3 both waves, H4 falsified, H6 confirmed.

v0.13 reuse-arm: Trends data taken from v0.12 deposit. Pivot Asana (validated in v0.11 § 5.2.1).

### §3.2 Premium running shoes

Registry: `registries/brands_running.json` (v0.6 final state; 17 brands).

Confirmatory expectations from v0.12: Regime 2 (Age-mediated strong), H1 confirmed decisively, H2 confirmed, H3 falsified at 2 of 3 both waves, H4 falsified (partial ρ ≈ 0.47), H6 falsified asymmetrically (Linear-style present, no Todoist-style).

v0.13 reuse-arm: Trends data taken from v0.12 deposit. Pivot Asics (Phase A validated in v0.12: mean 84.5, CV 7.9%).

### §3.3 Premium olive oil

Registry: `registries/brands_oliveoil.json` (v0.6 final state; 20 brands).

Confirmatory expectations from v0.12: Regime 3 (Scale-mismatch). Descriptive routing per §3.6a (n_PASS = 8 at Worldwide, n_PASS = 7 at US in v0.12; both below the hard floor of 10). H1–H4 not evaluable; Category-Scale Mismatch index = 46.7%.

v0.13 reuse-arm: Trends data taken from v0.12 deposit. Pivot California Olive Ranch (Phase A validated in v0.12: mean 83.5, CV 12.4%). Routing confirmed: descriptive-only per §3.6a applies in v0.13 as in v0.12 (same data).

### §3.4 Premium facial skincare (NEW for v0.13)

Registry: `registries/brands_skincare.json` (reconstructed v2-skincare; 31 brands). Reconstruction note in the registry file is preserved verbatim. The 24 brands surfaced in v2-skincare CSVs plus 6 traditional luxury brands cited in v0.6 findings as 0% mentioned plus Beauty of Joseon as K-beauty boundary-condition test.

Pivot candidate: **CeraVe** (mass-market dermatologist-recommended; stable year-round search; no holiday-driven seasonality). Phase A validation required prior to acquisition lock per §4.2.

v0.13 fresh-acquisition arm: Trends acquisition scheduled for `[ACQUISITION TIMESTAMP TBL]`. Phase B topic-ID resolution to follow standard pytrends.suggestions() workflow per v0.12 § 5.2.

### §3.5 Personal finance apps (NEW for v0.13)

Registry: `registries/brands_finance.json` (v0.6 final state; 16 brands; includes Mint as an `incumbent` despite September 2025 shutdown, consistent with the registry-frozen-ness convention from v0.7 / v0.10).

Pivot candidate: **YNAB** (You Need A Budget; established 2004; consistent subscription-based product with stable mass-market search interest). Phase A validation required prior to acquisition lock per §4.2.

**Fallback pivot:** Quicken (longer history, mass-market). Used if YNAB fails Phase A (out-of-sample window CV > 25% or mean < 25 against the pivot baseline).

v0.13 fresh-acquisition arm: Trends acquisition scheduled jointly with skincare. Phase B topic-ID resolution to follow standard pytrends workflow. Critical Phase B requirement: Mint topic-ID resolution must disambiguate "Mint (personal finance software)" from the herb, the colour, "mint condition", and brand-extension uses (e.g., MINT MOBILE). Failure to disambiguate routes Mint to a more disambiguated query string (e.g., `mint personal finance` or `mint intuit`); the resolution decision is logged in `registries/topic_id_resolution_log_v0.13.csv` prior to acquisition lock.

### §3.6 Routing rule §3.6a (descriptive-only)

A category routes to descriptive-only if either of the following holds at either wave:

- **n-floor.** n_eligible (matched-subset brands clearing E1b OR rescued by E5) < 10 at either wave.
- **PASS-fraction floor.** n_PASS / n_matched_subset < 0.6 at either wave.

A descriptive-only category contributes 0 of N to confirmatory hypothesis numerators (H5, H6, H7) and is excluded from the effective N denominators. Descriptive-only findings are reported as Category-Scale Mismatch indices and Phase B disposition breakdowns per § 10.

Routing decisions are determined POST-acquisition once n_PASS is known. Pre-registered expectation per category from § 3:

- PM software: confirmatory route expected.
- Running shoes: confirmatory route expected.
- Olive oil: descriptive-only expected (matches v0.12).
- Skincare: confirmatory route expected (large registry; mass-market brands).
- Personal finance: confirmatory route expected, with Mint excluded from H1–H7 regime classification per H8 phantom-handling rule.

---

## §4. Phase A — Pivot Validation

### §4.1 Per-category pivots

| Category | Pivot | Status at lock |
|---|---|---|
| PM software | Asana | Validated v0.11 § 5.2.1; reused |
| Running shoes | Asics | Validated v0.12: mean 84.5, CV 7.9%; reused |
| Olive oil | California Olive Ranch | Validated v0.12: mean 83.5, CV 12.4%; reused |
| Skincare | CeraVe (primary) | Phase A v0.13: mean 89.4, CV 7.8%; PASS |
| Personal finance | YNAB (primary) | Phase A v0.13: mean 82.0, CV 13.5%; PASS. See DEVIATIONS.md Entry 1 for § 4.2 query-string amendment. |

### §4.2 Pivot validation protocol

For each NEW pivot (skincare, personal finance), Phase A tests stability against an out-of-sample window prior to acquisition lock:

- **Out-of-sample window.** 13 – 19 April 2026 (two weeks before v0.13's t₁, fully disjoint from t₁/t₂).
- **Region.** Worldwide.
- **Query.** Pivot brand canonical name. Default is the bare brand name; category-disambiguation suffix added only if Phase A demonstrates the bare query returns insufficient signal AND a disambiguated query produces PASS-quality signal. The chosen query string per pivot is recorded in `data/phaseA_test/` JSONs and in § 4.1.
- **PASS criteria.** Daily values mean ≥ 25 AND coefficient of variation (sd/mean) < 25% across the 7-day window.
- **Fallback.** If primary pivot fails either PASS criterion, fallback pivot (Cetaphil for skincare, Quicken for personal finance) is tested under the same criteria.
- **Hard fail.** If both primary and fallback fail Phase A, the category cannot acquire under v0.13 design; the analysis plan defaults to a literature-grounded pivot decision recorded as a deviation in DEVIATIONS.md.

Phase A validation outputs (per pivot test JSON) are deposited at `data/phaseA_test/` and timestamped at execution.

---

## §5. Acquisition Design

### §5.1 Pivot rescaling

Bundle-relative Trends values (0–100 scale per bundle as returned by SerpAPI) are pivot-rescaled to a cross-bundle-comparable scale where the pivot brand is fixed at 100 daily across all bundles in the category, by category, by region, by wave.

Formula: for each (brand, day) cell with bundle-local value `v_brand` and bundle-local pivot value `v_pivot` (both in 0–100 scale, both > 0):

```
rescaled(brand, day) = 100 × v_brand / v_pivot
```

If `v_pivot` is 0 or undefined at any (bundle, region, wave, day) cell, the affected day is dropped from the brand's eligible value pool. The pivot brand itself is exempted from E1b (sd = 0 by construction; see § 5.4).

### §5.2 Bundle composition per category

Bundle composition is locked at this commit (see `registries/trends_query_strings_v0.13.json`, to be committed at lock). Bundle size ≤ 5 brands including pivot. Bundles balanced across tiers (incumbent / mid-tier / challenger) where possible.

Reuse arm (PM, running, olive): bundle composition inherited from v0.12.

Fresh-acquisition arm (skincare, finance):

**Skincare** (31 brands → 8 bundles per region):
- B1: CeraVe + Cetaphil + Neutrogena + La Roche-Posay + Vanicream
- B2: CeraVe + Skinceuticals + Eucerin + Paula's Choice + Drunk Elephant
- B3: CeraVe + Tatcha + The Ordinary + EltaMD + Bioderma
- B4: CeraVe + Avène + Aveeno + First Aid Beauty + Augustinus Bader
- B5: CeraVe + Youth to the People + La Mer + Estée Lauder + Lancôme
- B6: CeraVe + Clinique + Kiehl's + Sunday Riley + SK-II
- B7: CeraVe + Olay + Origins + Dermalogica + Murad
- B8: CeraVe + Glossier + Beauty of Joseon + (2 additional incumbent-tier from prior bundles as scale-anchoring padding)

**Personal finance** (16 brands → 4 bundles per region):
- B1: YNAB + Mint + Quicken + Empower + NerdWallet
- B2: YNAB + Quicken Simplifi + Rocket Money + PocketGuard + Goodbudget
- B3: YNAB + EveryDollar + Monarch Money + Copilot + Lunch Money
- B4: YNAB + Origin + Cleo + Tiller + (1 additional incumbent-tier as scale-anchoring padding)

Padding rule (lesson from v0.12 DEVIATIONS.md Entry 1): padding terms must be brand-volume-comparable, not category-generic. Padding in v0.13 uses incumbent-tier brand canonical names from elsewhere in the same category registry rather than generic category terms.

Total fresh-acquisition v0.13: (8 + 4) × 2 regions = 24 bundles in a single locked session.

### §5.3 Back-fill design

The v0.13 design uses v0.12's wave windows verbatim. This means:

- **For the three reuse-arm categories** (PM, running, olive): no new Trends acquisition. The per-brand within-window aggregations from v0.12's deposit at `osf/v12/data/trends_processed/per_brand_within_window.csv` are loaded directly into v0.13's analysis. Pivot rescaling, eligibility flags, and PASS/FAIL determinations are inherited verbatim.

- **For the two fresh-arm categories** (skincare, finance): new SerpAPI session against the v0.12 wave windows (which are now fully historical at v0.13 acquisition time). SerpAPI's Google Trends engine returns historical daily values for any past window; back-filling at past windows is methodologically equivalent to fresh acquisition at those windows, modulo the acquisition timestamp.

The back-fill design is transparent: the v0.13 acquisition timestamp will be later than v0.12's 2026-05-11T10:33:22Z, but the data being acquired is for the same calendar windows. This is disclosed in the v0.13 manuscript, the OSF deposit README, and DEVIATIONS.md if material to interpretation.

Rationale for back-fill design (not fresh windows for all 5 categories):
- Clean cross-sectional comparison across 5 categories at identical wave windows
- Two-week timeline saved (no waiting for t₂ window to pass)
- Three categories' data already deposited; no re-collection burden or re-acquisition risk

### §5.4 Eligibility rules

Identical to v0.12 §5.4:

- **E1a (pre-acquisition exclusion).** Brand returns 'notEnoughSearchVolume' or 'noResults' from SerpAPI solo Phase B validation against the out-of-sample window. Confirmed via E5 bundled validation rescue: ALL_ZERO in bundle = E1a confirmed; nonzero in bundle = PASS_E5.
- **E1b (within-window eligibility).** Per (brand, region, wave) cell: rescaled-window-mean > 0 AND rescaled-window-sd > 0 (rules out constant-zero or constant-flat brands). Pivot brand exempted (sd = 0 by construction).
- **E5 (rescue).** Per (brand, region, wave) cell: brand FAILed E1a solo but PASSed bundled validation = retained in confirmatory analysis with E5 flag in `per_brand_within_window.csv`.

Phase B validation outputs (per-brand solo + bundled) deposited at `data/phaseB_validation/` and `data/phaseB_bundled/` for the two fresh-acquisition categories. Reused for the three reuse-arm categories.

---

## §6. Wave Windows

Locked at v0.12's wave windows:

| Wave | Worldwide region | US region | Composition |
|---|---|---|---|
| t₁ | 27 April – 3 May 2026 | 27 April – 3 May 2026 | Mon–Sun, 7 days |
| t₂ | 4 May – 10 May 2026 | 4 May – 10 May 2026 | Mon–Sun, 7 days |

The 3-May / 4-May boundary makes t₁ and t₂ fully disjoint with no calendar-day overlap. Both waves are 7-day Mon–Sun windows for identical week-of-week comparison.

---

## §7. AI Presence Inputs

Per-brand AI Presence rates for all 5 v0.13 categories are taken from the v0.9 Longitudinal Re-Baseline deposit (SSRN 6736878; OSF v09/):

- t₁ corresponds to v0.6 collection window (29–30 April 2026)
- t₂ corresponds to v0.9 collection window (7 May 2026)
- Matched-model subset: Claude Sonnet 4.6 + GPT-5.4-mini (the model pair that has been used for v0.9, v0.10, v0.11, v0.12)
- Matched subset restricted per category per wave

No new LLM measurement for v0.13. The contribution of v0.13 is the external-behavioural construct-validity test against fresh and back-filled Google Trends data.

---

## §8. Per-Category Analysis Plan

For each of the 5 categories, compute:

1. Per-brand paired dataset: `analysis/per_brand_paired.csv` row per (brand, region, wave) with columns: `ai_t1_pct`, `ai_t2_pct`, `trends_ww_t1_mean`, `trends_ww_t2_mean`, `trends_us_t1_mean`, `trends_us_t2_mean`, `brand_age_years`, `tier`, `trends_*_eligible`, `e1a_excluded`, `e5_rescued`, `is_pivot`.

2. Per-category H1–H4 evaluated against pre-reg thresholds, both waves separately and conjunctively. Region = Worldwide primary; US sensitivity.

3. Per-category H3 leaderboards: AI-top-3, Trends-top-5, overlap count.

4. Per-category H4 partial Spearman ρ after OLS on rank-transformed (brand age, tier ordinal).

5. Per-category H6 Linear-style / Todoist-style brand detection.

6. Per-category regime classification per §2 H7 decision tree.

Outputs deposited at `analysis/canonical_scoring.json` (structured), `analysis/canonical_scoring.csv` (flat table).

---

## §9. Cross-Category Analysis Plan

Cross-category aggregations after per-category analyses complete:

1. H5 — count of confirmatory-eligible categories matching the v0.12 marginal signature; decision against 3-of-effective-N rule.

2. H6 — count of confirmatory-eligible categories showing both Linear-style and Todoist-style brands at both waves; decision against 4-of-effective-N rule.

3. H7 — regime classification for each of 5 categories; decision against the clean-classification rule for all categories.

4. Pooled rank-within-category Spearman ρ across confirmatory-eligible categories per wave (sensitivity check on construct-validity at the within-category-rank level).

5. Pooled Pearson r sensitivity (untransformed values, both regions, both waves).

6. US-only sensitivity (Worldwide is primary; US is secondary).

---

## §10. Category-Scale Mismatch reporting

For any category routing to descriptive-only per §3.6a, compute and report:

1. n_matched_subset (size of the AI-presence × Trends matched subset eligible for analysis at either wave)
2. n_PASS (count of brands clearing both AI Presence ≥ 5% at either wave AND Trends within-window-mean > 0 at either wave)
3. n_scale_mismatch (count of brands clearing AI Presence ≥ 5% at either wave BUT Trends within-window-mean ≤ 0 at either wave — i.e., signal below display threshold)
4. scale_mismatch_index_pct = 100 × n_scale_mismatch / n_matched_subset
5. Per-brand table identifying scale-mismatch cases by name with AI Presence values

Deposited as `analysis/category_scale_mismatch_table.csv` per descriptive-only category.

Pre-registered expectation for v0.13: olive oil routes to descriptive-only with scale_mismatch_index_pct in the 40–55% range (matches v0.12's 46.7%).

---

## §11. Phantom-Brand Analysis (NEW for v0.13)

H8 evaluation procedure:

1. **Identify Mint in personal finance per-brand paired dataset.** Verify Mint appears in `analysis/per_brand_paired.csv` with non-null AI Presence values at both waves. Verify Mint's Trends data was acquired (Phase B should yield PASS or PASS_E5; if EXCLUDED_E1a, Condition 3 is satisfied trivially with caveat).

2. **Evaluate Condition 1** (Mint AI ≥ 5% at both waves). From v0.9 deposit: t₁ Mint AI Presence = 44.79% gross (matched subset; v0.7 BBB cohort). t₂ Mint AI Presence to be computed against v0.9 t₂. Pre-registered expectation: both ≥ 5% with substantial margin per v0.10's stability finding.

3. **Evaluate Condition 2** (Mint top-5 AI rank at both waves). Compute per-wave per-region AI Presence ranks for personal finance brands; check Mint's rank ≤ 5 at both waves.

4. **Evaluate Condition 3** (Mint NOT top-5 Trends rank at either wave). Compute per-wave per-region Trends rescaled-mean ranks; verify Mint's rank > 5 at both waves.

5. **H8 confirm/falsify decision** by conjunction of all three conditions.

Per-wave Mint diagnostic table reported in `analysis/h8_mint_diagnostic.csv`. If H8 confirms, the personal finance category is operationally classified as exhibiting the Phantom-persistence regime (fourth regime in the v0.13 taxonomy) alongside its baseline-regime classification per H7 (which excludes Mint).

**Methodology note on Mint topic-ID resolution.** Phase B for Mint must succeed via a disambiguation strategy that isolates "Mint (personal finance software)" from non-software Mint queries. The chosen query string is logged in `registries/topic_id_resolution_log_v0.13.csv` prior to acquisition lock. If no disambiguation strategy produces an acquirable Trends signal (i.e., Mint routes to EXCLUDED_E1a even after extensive Phase B attempts), the H8 evaluation proceeds with Condition 3 treated as satisfied (no Trends signal at all = not top-5 by Trends at either wave) and the absence-of-signal is itself recorded as evidence consistent with the phantom regime.

---

## §12. Three-Regimes Accounting (NEW for v0.13)

H7 evaluation procedure:

1. For each of the 5 categories, exclude phantom-flagged brands (Mint in personal finance) from the per-brand paired dataset.

2. Re-compute per-category H1 bivariate Spearman ρ at both waves on the live-brands-only dataset.

3. Re-compute per-category H4 partial Spearman ρ at both waves on the live-brands-only dataset.

4. Compute per-category PASS-fraction = n_PASS / n_matched_subset.

5. Apply the H7 decision tree per category. For ambiguous or boundary classifications, record diagnostic detail.

6. Deposit `analysis/h7_regime_classification.csv` with per-category: bivariate_rho_t1, bivariate_rho_t2, partial_rho_t1, partial_rho_t2, decrement_t1, decrement_t2, pass_fraction_t1, pass_fraction_t2, regime_class, boundary_flag, unclassifiable_flag.

7. H7 confirm/falsify decision against the clean-classification rule.

Pre-registered expectation: PM software → Regime 1; running shoes → Regime 2; olive oil → Regime 3. Skincare and finance regimes are open questions resolved by H7 evaluation. Personal finance is expected on substantive grounds (large incumbent brand age range; mid-mass-market category) to lean toward Regime 1 or Regime 2; skincare is expected to lean toward Regime 2 (high age-of-brand variance; strong incumbent dominance).

---

## §13. Sensitivities

Reported alongside primary results:

1. **Pearson r vs Spearman ρ** — primary is Spearman; Pearson reported as sensitivity per v0.11 / v0.12 convention.
2. **US-only vs Worldwide** — Worldwide is primary; US-only sensitivity reported per v0.12 § 13.
3. **Strict E1b vs E5-inclusive** — primary uses E5-inclusive (rescued brands retained); strict-E1b sensitivity reported.
4. **Live-brands-only vs full-registry** — H1–H6 primary includes all eligible brands; H7-prep sensitivity excludes phantom-flagged.
5. **Phantom inclusion sensitivity** — sensitivity reporting Mint's effect on personal finance's H1 if included in the main analysis: report per-category H1 both with and without Mint.

---

## §14. Pre-Reg Outcomes Table (template)

Final table for the v0.13 report. Rows correspond to all hypothesis evaluations.

| Wave / Cat | Hypothesis | Pre-registered threshold | Result | Status |
|---|---|---|---|---|
| PM × both | H1 | ρ > 0.5 AND p₁ₜ < 0.05 at both waves | TBD | TBD |
| PM × both | H2 | \|Δρ\| ≤ 0.15 | TBD | TBD |
| PM × both | H3 | AI top-3 ⊆ Trends top-5 at both waves | TBD | TBD |
| PM × both | H4 | partial ρ > 0.5 AND p < 0.05 at both waves | TBD | TBD |
| Running × both | H1 | ρ > 0.5 AND p₁ₜ < 0.05 at both waves | TBD | TBD |
| Running × both | H2 | \|Δρ\| ≤ 0.15 | TBD | TBD |
| Running × both | H3 | AI top-3 ⊆ Trends top-5 at both waves | TBD | TBD |
| Running × both | H4 | partial ρ > 0.5 AND p < 0.05 at both waves | TBD | TBD |
| Olive × both | H1–H4 | descriptive-only routing per §3.6a | n/a | Descriptive |
| Olive × both | §10.2 | Scale-Mismatch index | TBD | Descriptive |
| Skincare × both | H1 | ρ > 0.5 AND p₁ₜ < 0.05 at both waves | TBD | TBD |
| Skincare × both | H2 | \|Δρ\| ≤ 0.15 | TBD | TBD |
| Skincare × both | H3 | AI top-3 ⊆ Trends top-5 at both waves | TBD | TBD |
| Skincare × both | H4 | partial ρ > 0.5 AND p < 0.05 at both waves | TBD | TBD |
| Finance × both | H1 | ρ > 0.5 AND p₁ₜ < 0.05 at both waves (live brands only per §11) | TBD | TBD |
| Finance × both | H2 | \|Δρ\| ≤ 0.15 (live brands only) | TBD | TBD |
| Finance × both | H3 | AI top-3 ⊆ Trends top-5 at both waves (live brands only) | TBD | TBD |
| Finance × both | H4 | partial ρ > 0.5 AND p < 0.05 at both waves (live brands only) | TBD | TBD |
| Cross-category | H5 | v0.12 marginal signature in 3+ of effective-N | TBD | TBD |
| Cross-category | H6 | Linear-style + Todoist-style in 4+ of effective-N | TBD | TBD |
| Cross-category | H7 | All 5 categories classify cleanly into 3 regimes (live brands only) | TBD | TBD |
| Finance | H8 | All 3 Mint phantom-persistence conditions hold | TBD | TBD |

22 pre-registered hypothesis evaluations total. Hypotheses H1–H4 evaluated per-category-per-wave with both-waves conjunction; H5–H8 cross-category single decisions.

---

## §15. Output Formats

Deposited at `osf.io/ec6wh/files/osfstorage/v13/`:

| Path | Contents |
|---|---|
| `PRE_REGISTRATION.md` | This file, locked at the git commit referenced in the header |
| `DEVIATIONS.md` | Methodology notes accumulated during acquisition/analysis |
| `README.md` | Deposit overview, headline finding, cross-references |
| `MANIFEST.md` | Structured file inventory with sizes and lineage map |
| `registries/` | Brand registries (5 files), topic-ID resolution log, trends query strings, wave windows, brand age sources |
| `data/phaseA_test/` | Pivot validation tests for the 2 NEW categories |
| `data/phaseB_suggestions/` | pytrends suggestions output for the 2 NEW categories |
| `data/phaseB_validation/` | Solo + bundled validation per brand for the 2 NEW categories |
| `data/trends_raw/` | 24 NEW bundles × 2 regions for the 2 NEW categories; reuse-arm data referenced via cross-link to v0.12 deposit |
| `data/trends_processed/` | Combined per-brand-per-day and per-brand-within-window CSVs spanning all 5 categories |
| `data/trends_acquisition_log.csv` | Per-bundle PASS manifest for the v0.13 fresh-acquisition session |
| `analysis/` | per_brand_paired.csv, canonical_scoring.json, canonical_scoring.csv, category_scale_mismatch_table.csv, h7_regime_classification.csv, h8_mint_diagnostic.csv |
| `figures/` | Chart PDFs for SSRN paper and brand-format report (target: ~15 PDFs across H1 cross-cat scatter t₁/t₂, per-category H3 rank-shift, per-category H4 partial residual, H6 zones cross-cat, H7 regime taxonomy visualisation, H8 Mint diagnostic, Scale-Mismatch viz) |

Companion deliverables:

- **SSRN working paper.** "Cross-Category Construct Validity at Five Categories: Three Empirical Regimes Hold, Phantom Persistence Surfaces a Fourth." Carlito 11pt; visual identity matching v0.7–v0.12.
- **Third System brand-format report.** "Five Categories, Four Regimes." Akkurat Pro; brand palette.
- **OSF deposit.** Automated upload via `~/aias/scripts/osf_upload.py`.

---

## §16. Declarations

**Conflict of interest.** The author serves as Director, Corporate Brand Creative and Governance at Samsung Electronics America. The research presented here is independent of Samsung Electronics America and does not constitute Samsung research. No Samsung Electronics America data, personnel, or commercial interests influenced the design, conduct, analysis, or reporting of this study. Samsung Electronics America did not review the manuscript prior to posting. The brand populations evaluated in this study do not include Samsung product lines.

**Funding.** Self-funded. No external funding sources contributed to this research.

**Ethics approval.** Not applicable. This study does not involve human or animal participants. The measurement is of (a) large language model outputs in response to category-recommendation prompts (inputs sourced from prior v0.9 deposit) and (b) publicly available aggregate Google Trends search-interest indices. No identifiable individual data, no participant recruitment, no intervention on human subjects.

**Data and code availability.** Pre-registration, registry files, raw Trends data, processed Trends data, AI Presence inputs (cross-referenced to v0.9 deposit), analysis scripts, chart-build scripts, paper-build scripts, and the published manuscript are deposited at osf.io/ec6wh/files/osfstorage/v13/. The git repository tracking source is the private AIAS Measurement Programme repo; the deposited materials are bit-identical to the locked git commit referenced in the header.

---

*End of pre-registration. Lock at `git tag v0.13-prereg` prior to any Trends acquisition call against the v0.13 wave windows under this design.*
