# AIAS v0.12 — Pre-Registration

**Title.** Three-Category Construct-Validity Expansion of v0.11 — PM Software, Premium Olive Oil, Premium Running Shoes × Google Trends, t₁→t₂

**Version.** v0.12 pre-registration · draft for git lock
**Methodology Protocol.** AIAS Presence Measurement Protocol v1.1 (SSRN 6722319)
**Registry.** brands_pm.json, brands_oliveoil.json, brands_running.json (frozen at v0.6 lock)
**Date drafted.** 2026-05-10
**Lock target.** git commit prior to any Google Trends acquisition call against the v0.12 wave windows
**Author.** Pablo Ulpiano González Castro
**Research entity.** Third System™

**Cross-cites.** AI Availability foundational paper (SSRN 6659000) · AIAS Presence Measurement Protocol v1.1 (SSRN 6722319) · v0.6 Cross-Category Findings (SSRN 6720959) · v0.7 Phantom-Brand BBB (SSRN 6721779) · v0.8 Discourse-Language Knives (SSRN 6728000) · v0.9 Longitudinal Re-Baseline (SSRN 6736878) · v0.10 Naive-Phantom Rate Stability (SSRN 6741163) · **v0.11 PM Software × Google Trends Construct Validity (SSRN 6745040)**.

---

## 1. Background

v0.11 (SSRN 6745040) was the first construct-validity test in the AIAS programme: a single-category pre-registered pilot of per-brand AI Presence rate against per-brand Google Trends search interest, for 18 project management software brands at two longitudinal waves seven days apart.

v0.11 findings (matched two-model subset; Sonnet 4.6 + gpt-5.4-mini):

- **H1 (cross-sectional construct validity):** Spearman ρ = 0.496 at t₁, 0.476 at t₂; one-tailed *p* < 0.05 at both waves. Magnitude threshold (ρ > 0.5) missed by 0.004 at t₁. **Falsified.**
- **H2 (cross-wave stability):** |Δρ| = 0.020 against 0.15 tolerance. **Confirmed.**
- **H3 (leaderboard top-3 ⊆ top-5):** 1 of 3 at both waves. **Falsified.**
- **H4 (covariate-controlled, age + tier):** partial ρ = 0.407 / 0.428 across waves. **Falsified.**

Substantive interpretation: AI applies a tighter and partly-different category boundary than consumer search does. Two diagnostic cases anchor the finding:

- **Linear paradox:** AI's #1 PM-software recommendation at both waves (86.5%, 89.6% AI Presence) with negligible consumer search interest (Trends 1.88 with Asana indexed to 100). Inside AI's PM-software category, barely inside consumers'.
- **Todoist inverse:** 1.04% AI Presence with Trends value 28, comparable to GitHub Projects at 40× more AI Presence. Outside AI's PM-software category (AI frames it as a personal task manager), well inside consumers'.

The construct of AI Availability is correlated but not equivalent to Mental Availability. v0.12 tests whether this category-boundary mechanism generalises beyond PM software.

### Why three categories

v0.12 expands the v0.11 protocol from one category to three: PM software (replication), premium olive oil, premium running shoes. The two added categories test different structural conditions:

- **Premium running shoes** — high brand density (13 matched-subset brands); tests v0.11's category-boundary mechanism under competitive saturation, where 'top-3 leadership' is less informative.
- **Premium olive oil** — initially selected as a clean stable-leadership replication. Phase B validation against the out-of-sample window (2026-04-01 to 2026-04-07) revealed that 7 of 14 non-pivot matched-subset brands have Google Trends search-interest signal below the platform's global display threshold (Trends API response: "Google Trends hasn't returned any results for this query"). Bundled-pivot validation (replicating the acquisition methodology) confirmed: even with California Olive Ranch as a high-volume bundle anchor, those 7 brands return ALL_ZERO rescaled values across the validation window. The category-scale mismatch — measurable AI Presence at the matched-subset level coexisting with Trends signal below platform display threshold — is the v0.12 finding for olive oil. Per the n-floor rule (§3.4), olive oil's usable n = 8 routes H1/H2/H4 to descriptive-only; the Category-Scale Mismatch Finding is reported descriptively per §10.

### What v0.12 does and does not test

v0.12 tests two distinct generalisations of v0.11:

1. **Boundary-mismatch generalisation (H1–H4, H5, H6).** Whether v0.11's PM-software category-boundary mechanism (Linear paradox + Todoist inverse + sub-0.5 correlation with significance + leadership-failure) replicates across categories. PM software (replication) and running shoes (new category) carry this generalisation test. With olive oil routed to descriptive-only, H5/H6 cross-category conjunction reduces to 2-of-2 across PM + running shoes (see §2.2).

2. **Scale-mismatch finding (descriptive, no pre-registered H).** Whether AI Availability operates at a brand-coverage scale that consumer search at the platform level cannot resolve. Olive oil is the carrying category. This is reported as a descriptive finding, not as a pre-registered hypothesis test, because the operationalisation only became possible after Phase B revealed which brands fall below Trends' display threshold.

v0.12 is not a causal claim, nor a multi-validator construct-validity claim, nor an expansion of the validator beyond Google Trends search interest.

**No new LLM measurement is required.** v0.6 / v0.9 deposited the AI Presence rate input across all three categories; v0.12 acquires the Google Trends side for olive oil and running shoes (PM software Trends data is also re-acquired against v0.11's locked windows, for consistency with the v0.12 pooled-sensitivity test in §6).

---

## 2. Hypotheses

v0.12 has three inferential layers:

- **Layer 1 (primary):** H1–H4 per category. 6 hypotheses × 3 categories = 18 outcomes. Replicates v0.11 hypothesis structure and thresholds.
- **Layer 2 (cross-category integrator):** H5 and H6.
- **Layer 3 (sensitivity):** pooled ρ on stacked within-category-rescaled data.

### 2.1 Per-category hypotheses (Layer 1)

Thresholds and definitions replicate v0.11 §2 exactly. Each category evaluated independently.

**H1 (per category) — Cross-Sectional Construct Validity.** Per-brand AI Presence rate co-varies with per-brand Google Trends search-interest index at sufficient strength to support the construct.

- *Operationalisation.* Spearman ρ across the analysis brand set between per-brand AI Presence rate (v0.9 matched subset) and per-brand within-window mean Google Trends search interest (pivot-rescaled, Worldwide region). Computed independently for t₁ and t₂.
- *Confirmed if* ρ > 0.5 AND p < 0.05 (one-tailed) at **both** waves.
- *Falsified if* ρ ≤ 0.5 OR p ≥ 0.05 at **either** wave.

**H2 (per category) — Correlation Stability.** Correlation strength is stable across t₁ → t₂.

- *Operationalisation.* |ρ_t₂ − ρ_t₁| computed against H1 Spearman ρ values per category.
- *Confirmed if* |Δρ| ≤ 0.15.
- *Falsified if* |Δρ| > 0.15.

**H3 (per category) — Leaderboard Directional Consistency.** Top-3 brands by AI Presence rate appear in the top-5 by Google Trends search interest, at each wave.

- *Operationalisation.* Set membership of AI-Presence top-3 within Trends top-5, per wave.
- *Confirmed if* all 3 in top-5 at **both** waves.
- *Falsified if* ≥ 1 absent from top-5 at **either** wave.

**H4 (per category) — Covariate-Controlled Correlation.** H1 correlation survives partialling brand age and within-category competitive tier.

- *Operationalisation.* Spearman partial correlation controlling for (a) brand age = years from brand-as-marketed founding to 1 January 2026 per `registries/brand_age_sources_v0.12.csv`; (b) competitive tier from v0.6 registry treated as ordinal (incumbent = 1, mid-tier = 2, challenger = 3). Computed independently for t₁ and t₂.
- *Confirmed if* partial ρ > 0.5 AND p < 0.05 (one-tailed) at **both** waves.
- *Falsified if* partial ρ ≤ 0.5 OR p ≥ 0.05 at **either** wave.

All p-values are one-tailed throughout. No Bonferroni correction is applied across the 18 per-category tests (categories are not exchangeable samples from a population; joint inference is via H5). Multiplicity disclosure recorded in §7.

### 2.2 Cross-category generalisation (Layer 2)

**H5 — Generalisation of v0.11 signature.** The v0.11 PM-software construct-validity signature is operationalised as the conjunction:

- ρ < 0.5 (H1 magnitude bar missed) AND
- p < 0.05 one-tailed (significance bar cleared) AND
- H3 falsified (top-3 ⊄ top-5)
- at both waves.

- *Confirmed if* ≥ 2 of 3 categories produce the full signature at both waves.
- *Falsified if* 0 or 1 categories produce the full signature.
- *Indeterminate if* all 3 categories route to descriptive-only (per §3.4).

**Effective evaluation at v0.12 lock.** Phase B routes olive oil to descriptive-only (§3.4). H5 is therefore evaluable on PM software + running shoes only; the 2-of-3 threshold reduces to 2-of-2 (both functional categories must show the signature). Olive oil's contribution is reported separately as the Category-Scale Mismatch Finding (§10) and does not enter H5 arithmetic.

**H6 — Category-boundary mechanism.** Each category produces brands fitting both v0.11 diagnostic types.

*H6a (per-category, per-wave):* Category produces ≥ 1 Linear-paradox-style brand AND ≥ 1 Todoist-inverse-style brand.

Thresholds (in pivot-rescaled units, pivot = 100, strict inequalities, one-decimal rounding):

- **Linear-paradox-style brand:** AI Presence ≥ 50% AND Trends rescaled mean ≤ 5
- **Todoist-inverse-style brand:** AI Presence ≤ 5% AND Trends rescaled mean ≥ 20

Thresholds derived from v0.11 reference cases: Linear (AI 86.5%, Trends 1.88) and Todoist (AI 1.04%, Trends 28). Both reference brands clear their respective thresholds with margin.

*H6a confirmed* for a category only if both diagnostic-type brands exist at **both** waves. A category producing only one of the two types does not confirm H6a (the test distinguishes "different boundary" from "tighter boundary"; tighter-only produces only Todoist-style cases).

*H6b (cross-category):*

- *Confirmed if* ≥ 2 of 3 categories confirm H6a.
- *Falsified if* 0 or 1 categories confirm H6a.
- *Indeterminate if* all 3 categories route to descriptive-only.

**Effective evaluation at v0.12 lock.** Phase B routes olive oil to descriptive-only (§3.4). H6b is therefore evaluable on PM software + running shoes only; the 2-of-3 threshold reduces to 2-of-2 (both functional categories must produce both diagnostic-type brands). Olive oil's H6a is not computable under pivot-rescaling because 7 of 14 non-pivot brands fall below Trends' display threshold; its descriptive treatment is in §10.

### 2.3 Pooled sensitivity (Layer 3)

Pooled Spearman ρ on stacked within-category-rescaled data (all matched-subset brands across all three categories). Reported at both waves. No H1–H4 evaluation on pooled data; reported descriptively as programme-level construct-validity statement.

### Test family and FWER

H1–H4 per category are primary confirmatory tests; the both-waves conjunction in H1 and H4 provides built-in FWER control. No explicit family-wise correction is applied across the 18 per-category tests; the structural per-category framing plus the H5 cross-category integrator (single 2-of-3 test) does the equivalent work at the design level. Bonferroni-corrected p-values (α/3 = 0.0167) for secondary hypotheses per category are reported in the OSF deposit as sensitivity.

---

## 3. Threshold Justification

### ρ > 0.5

The 0.5 threshold for H1 correlation magnitude replicates v0.11 §3. Standard "moderate-to-strong correlation" benchmark in behavioural research. Threshold identical between Spearman primary and Pearson sensitivity.

### |Δρ| ≤ 0.15 (H2)

Replicates v0.11 §3. Test-retest stability calibration over one-week interval.

### Top-3 ⊆ Top-5 (H3)

Replicates v0.11 §3. Asymmetric 3-vs-5 specification gives leaderboard test slack at the boundary while preserving directional claim.

### One-tailed at α = 0.05

Replicates v0.11 §3. Per-test α; FWER controlled structurally.

### 3.4 Effective-n Floor

H1, H2, and H4 are evaluated only if **n ≥ 10** brands have usable Trends signal at each wave per category, with a soft alignment threshold disclosed at **n = 12**. "Usable Trends signal" follows v0.11 §5.4 (E1b) verbatim.

**Floor evolution from v0.11.** v0.11 set n ≥ 16 of 19 for PM software, corresponding to a tolerance budget of three brand dropouts. v0.12 lowers the hard floor to n = 10 to accommodate smaller matched subsets in the two added categories (olive oil n = 15, running shoes n = 13 from v0.9 matched-subset deposit). At n ≤ 11 the critical Spearman ρ for one-tailed p < 0.05 exceeds the H1 magnitude threshold of 0.5 (n = 10: critical ρ = 0.564; n = 11: critical ρ = 0.523); pre-reg states this explicitly. At n ≥ 12 magnitude is the binding constraint for H1 (n = 12: critical ρ = 0.497). All three v0.12 categories sit above n = 12 from the locked matched subsets (PM 17, olive 15, running 13); dual-binding disclosure does not trigger at this version. The protocol-level rule remains for future versions.

If a category's analytic n falls below 10 at acquisition, **H1 / H2 / H4 for that category are routed to descriptive disclosure path** (paired routing — H1 / H2 coupled across waves by construction; H4 inherits). H3 is computable per wave from whatever brands are present and is reported with explicit flagging if dropouts affect rank composition. H5 / H6 cross-category accounting excludes any category routed to descriptive-only.

The floor is fixed at lock and is not adjusted post hoc.

### 3.4a Phase B Lock Outcomes

Phase B pre-acquisition validation (out-of-sample window 2026-04-01 to 2026-04-07) completed prior to pre-reg lock. Outcomes per category at the `v0.12-prereg` tag:

- **PM software (n_locked = 17 + Shortcut E1a-inherited from v0.11).** No re-validation at v0.12; query specification inherited verbatim from v0.11 §5.2.1. Analytic n ≥ 12 (alignment threshold) at both waves. **Normal H1–H4 evaluation.**
- **Running shoes (n_locked = 13).** All 13 matched-subset brands PASS Phase B validation with robust signal (range 50.9–90.6 mean, 7/7 nonzero days in all cases). Analytic n ≥ 12 at both waves. **Normal H1–H4 evaluation.**
- **Premium olive oil (n_locked = 8).** Phase B validation produced 7 E1a exclusions:
  - **E1a-excluded:** Colonna, Frescobaldi Laudemio, Lucini, Manni, McEvoy Ranch, Núñez de Prado, Olio Verde. All 7 returned "Google Trends hasn't returned any results for this query" at the out-of-sample window. Bundled-validation diagnostic (replicating the acquisition pivot-rescaling methodology) confirmed: all 7 return ALL_ZERO rescaled values in 5-term bundles anchored on California Olive Ranch. The brands are below the platform's absolute-volume display threshold globally.
  - **PASS_E5 (sparsity flag):** Frantoio Muraglia (bundled-rescue PASS: 1/7 nonzero in bundle, mean 8.3, range 0–58), Castillo de Canena (solo PASS but 1/7 nonzero), Kosterina (solo PASS but 1/7 nonzero). All three carry E5 sparsity flags but are retained in analysis.
  - **PASS robust:** California Olive Ranch (pivot, Phase A validated mean 83.5 CV 12.4%), Bertolli (mean 77.3), Brightland (mean 29.4), Cobram Estate (mean 77.3), Graza (mean 84.0).
  - **Analytic n = 8 < 10 hard floor.** Olive oil routes to descriptive-only per §3.4. H1, H2, H4 indeterminate. H3 reported with sparsity-flag annotation. The category contributes the Category-Scale Mismatch Finding (§10) instead of confirmatory inference.

Phase B summary deposited at `/v12/data/phaseB_validation/validation_summary_2026-05-11T02-29-00Z.json` and `/v12/data/phaseB_bundled/`. AI Presence rates at v0.9 matched subset for the 7 E1a-excluded brands range 3.1%–22.9% (Frescobaldi Laudemio and Olio Verde at 22.9%; Lucini at 17.7%); these rates document the scale-mismatch and are sourced from `/v09/data/results_enriched_v09_*.csv` (matched-subset filter: anthropic_sonnet + openai_mini).

---

## 4. Data and Subset

### Source 1 — AI Presence rate (pre-existing, no new measurement)

Per-brand AI Presence rates at t₁ and t₂ pulled from prior deposits across all three categories:

- **t₁ AI Presence (per brand).** v0.9-deposited canonical scoring at the matched-model subset (Sonnet 4.6 + gpt-5.4-mini), restricted to {PM software, olive oil, running shoes}, evaluating responses collected in the v0.6 baseline window (29–30 April 2026). Source: OSF project ec6wh, /v09/data/, git tag `v0.9-published`.
- **t₂ AI Presence (per brand).** v0.9-deposited canonical scoring at the matched-model subset, restricted to {PM software, olive oil, running shoes}, evaluating responses collected in the v0.9 re-baseline window (7 May 2026). Source: same as above.

The matched-model subset (Sonnet 4.6 + gpt-5.4-mini) is identical across both waves and across all three categories to maintain comparability with v0.9 and v0.11.

### Source 2 — Google Trends search-interest index (acquired at v0.12)

Per-brand Google Trends search-interest index acquired at a single locked UTC timestamp following pre-reg lock and prior to any analysis. Acquisition specification replicates v0.11 §4 verbatim:

- **Region (primary).** Worldwide.
- **Region (sensitivity).** US-only, captured in the same acquisition session, deposited but not used in primary inference.
- **Granularity.** Daily.
- **Wave windows.**
  - **t₁ window.** 27 April – 3 May 2026 (Mon–Sun, 7 days, centred on 30 April — the v0.6 collection closing day). *Identical to v0.11.*
  - **t₂ window.** 4 May – 10 May 2026 (Mon–Sun, 7 days, centred on 7 May — the v0.9 collection day). *Identical to v0.11.*
  - Windows fully disjoint at the 3 May / 4 May boundary. Both windows have identical weekday composition.
- **Per-brand within-window statistic.** Arithmetic mean of the daily 0–100 search-interest index across the 7 days.
- **Cross-brand normalisation.** Pivot-rescaled per §5.1.
- **Acquisition library.** SerpAPI Google Trends engine (replicates v0.11 §4). Per-bundle UTC timestamp, parameters, and rate-limit status captured to `/v12/data/trends_acquisition_log.csv`.

### Brand registries

Three registries, all frozen at v0.6 final state:

| Category | Registry | Matched-subset n (v0.9) | Pivot brand |
|---|---|---|---|
| Project management software | `brands_pm.json` | 17 | Asana |
| Premium olive oil | `brands_oliveoil.json` | 15 | California Olive Ranch |
| Premium running shoes | `brands_running.json` | 13 | Asics |

Matched-subset brand lists committed in `registries/matched_subset_v0.12.json`.

### Defunct brand disclosure

Per v0.11 §4, brands operationally defunct at acquisition time remain in analysis per registry-frozen-ness principle. No defunct brands identified at v0.12 lock across olive oil and running shoes registries. Height (PM software, defunct September 2025) status carries forward from v0.11 unchanged. Any defunct-brand identification during Phase B validation is documented in `DEVIATIONS.md`.

### Unit of analysis

One brand per category contributes one (AI Presence rate, Trends within-window mean) pair per wave. Across three categories and two waves, **maximum 90 pairs at full coverage** (PM 17 × 2 + olive 15 × 2 + running 13 × 2 = 90), subject to Phase B validation and acquisition-time exclusions.

---

## 5. Operationalisation

### 5.1 Pivot rescaling (Trends acquisition)

Replicates v0.11 §5.1 verbatim, applied per category. Each acquisition bundle contains [Pivot, Brand₁, Brand₂, Brand₃, Brand₄] — pivot plus four other brands. Per-brand within-window mean computed as arithmetic mean of pivot-rescaled daily values:

`rescaled_B(d) = raw_B(d) / raw_Pivot(d) × 100`

Pivot brand's rescaled value is 100 every day by construction. Pivots:

- PM software: Asana (topic mid `/m/0c3z_p8`, per v0.11)
- Olive oil: California Olive Ranch (topic-mid TBD at Phase B)
- Running shoes: Asics (topic-mid TBD at Phase B)

Pivot stability across the window pair: California Olive Ranch and Asics presumed Trends-stable across windows; if either exhibits > 50% within-window standard deviation in raw Trends index, secondary-pivot-selection rule per v0.11 §5.2 is invoked, documented in `DEVIATIONS.md`, and substituted pivot locked before any re-scoring.

### 5.2 Brand-name disambiguation (tiered query specification)

Replicates v0.11 §5.2 verbatim. Each brand assigned to one of three query tiers:

- **T1 — Topic ID.** Topic-mid passed as query.
- **T2 — Distinctive search string.** Bare brand name.
- **T3 — Brand+category compound.** Fixed compound `<brand> <category-anchor>` where category-anchor is `project management` (PM software) / `olive oil` (olive oil) / `running shoes` (running).

Topic-ID resolution conducted via `pytrends.suggestions()` at Phase B. Per-brand specification — initial tier, final tier, exact query, entity label where T1, lookup timestamp, rationale — committed in `registries/trends_query_strings_v0.12.json` at pre-reg lock.

PM software per-brand specification table replicated from v0.11 §5.2.1 unchanged. Olive oil and running shoes per-brand specification committed in `registries/trends_query_strings_v0.12.json`.

### 5.3 H4 covariate operationalisation

- **Brand age.** Integer years from brand-as-marketed founding to reference date 1 January 2026.
  - *Operational definition.* Year the consumer-facing brand was first commercially available under its current name. For estates predating the modern brand identity (e.g. Castillo de Canena 1780 estate, modern brand 2003), the modern brand-as-marketed year is used. For brand renames (e.g. Onitsuka → Asics 1977; Blue Ribbon Sports → Nike 1971), the renamed-brand year is used per the "brand-as-marketed" rule.
  - *Primary source.* Brand's official "About" or company-history page.
  - *Tie-breaker.* Wikipedia; then trade press (Olive Oil Times, Runner's World) or Crunchbase.
  - *Tie-breaker rules.* (i) acquisitions → brand founding, not acquirer; (ii) reformulations or relaunches → renamed-brand year; (iii) ≤ 2-year disagreement → earlier year; (iv) > 2-year disagreement → document conflict, use primary.
- **Competitive tier.** Ordinal from v0.6 registry: incumbent = 1, mid-tier = 2, challenger = 3. Mapping inherits the registry's own tier assignment per category.

Per-brand age values and sources committed in `registries/brand_age_sources_v0.12.csv`.

### 5.4 Pre-Specified Decision Rules — Edge Cases

Replicates v0.11 §5.4 exactly, applied across all three categories.

**E1a — Pre-acquisition exclusion.** If a brand's locked acquisition query returns no Trends signal during pre-acquisition validation (validation script against out-of-sample window 1–7 April 2026), the brand is excluded from v0.12 analysis. Pre-acquisition exclusions documented in the locked spec at the `v0.12-prereg` tag with rationale, each counting toward category n-floor as one dropout.

**E1a amendment (v0.12-specific):** Solo validation is the primary test. When solo validation returns FAIL_API ("Google Trends hasn't returned any results for this query") in a low-volume premium category, a secondary bundled-validation test is run replicating the acquisition pivot-rescaling methodology. If the brand returns ALL_ZERO rescaled values in a 5-term pivot-anchored bundle at the out-of-sample window, E1a-exclusion stands. If the brand returns any nonzero rescaled signal in the bundle (any day in any rescaling), the brand is INCLUDED with E5 sparsity flag set. The amendment is responsive to Phase B finding that Trends' platform-side display threshold is observed at the solo-query level but bundle-level queries can rescue marginal-volume brands. At v0.12 lock: 7 olive oil brands fail both solo and bundled (E1a-excluded); 1 olive oil brand (Frantoio Muraglia) fails solo, marginal-passes bundled (INCLUDED + E5).

**E1b — At-acquisition exclusion.** If a brand's pivot-rescaled within-window mean is 0 OR within-window standard deviation is 0 at either wave during the actual acquisition session, the brand is excluded from that wave's analysis for that category. Exclusion logged with rationale in `/v12/data/at_acquisition_exclusions.csv`. Wave-level n recalculated; n-floor evaluation per §3.4 determines whether confirmatory inference proceeds for that category.

**E2 — Pivot brand failure.** If any pivot (Asana, California Olive Ranch, Asics) returns zero or anomalous values in any acquisition bundle, acquisition halts for that category. Re-acquisition follows a documented retry protocol (up to 3 attempts at the same UTC timestamp; if all fail, deferred to a new locked timestamp and previous attempt logged but not used).

**E3 — At-acquisition topic-ID failure.** If a T1-tiered brand returns anomalous signal at the actual wave windows despite passing Phase B validation, the brand triggers E1b exclusion. Re-querying with alternative entities post-lock is not permitted; topic-ID assignments are fixed at the `v0.12-prereg` tag.

**E4 — Trends API failure during acquisition.** If Google Trends acquisition fails during the locked session (rate limiting, partial bundle returns, network failure), acquisition halts and retry protocol engages. Up to 3 retry attempts; if all fail, deferred to a new locked timestamp.

**E5 — Within-window data sparsity.** If a brand has Trends signal on fewer than 4 of 7 within-window days at either wave (majority-zero within window), within-window mean is reported but flagged. Brand is included if mean > 0 AND standard deviation > 0 (per E1b), with sparsity flag reported alongside H1 outcome.

---

## 6. Analysis Plan

1. **Pre-acquisition.** Verify all three registries frozen state. Verify v0.9-deposited matched-subset AI Presence rates for {PM, olive, running} at t₁ and t₂. Verify brand age sources per `registries/brand_age_sources_v0.12.csv`. Verify per-brand query specifications per `registries/trends_query_strings_v0.12.json`.
2. **Phase A — Pivot brand verification.** Out-of-sample timeseries acquisition for each pivot (Asana, California Olive Ranch, Asics) against the April 1–7 2026 out-of-sample window. Deposited at `/v12/data/phaseA_test/`.
3. **Phase B — Topic-ID resolution and pre-acquisition validation.** `pytrends.suggestions()` per brand; SerpAPI validation against out-of-sample window 1–7 April 2026 per-brand. Brands failing validation excluded under E1a, documented at lock. Outputs deposited at `/v12/data/phaseB_suggestions/` and `/v12/data/phaseB_validation/`.
4. **Trends acquisition.** Execute pivot-bundled acquisition at single locked UTC timestamp post-lock, all three categories in the same session. Capture raw API response per bundle. Apply pivot rescaling per §5.1.
5. **Validator construction.** Compute per-brand within-window mean for t₁ and t₂ per category. Apply E1b / E5 rules. Determine per-wave, per-category brand count.
6. **n-floor check.** Verify n ≥ 10 at both waves per category per §3.4. If breached, route H1 / H2 / H4 to descriptive disclosure path for that category. H5 / H6 cross-category accounting excludes routed categories.
7. **Per-category H1 / H2 / H3 / H4 evaluation.** Per §2.1, replicates v0.11 §6 analysis steps 5–8 per category. Pearson r as sensitivity for H1 at each wave per category.
8. **Cross-category H5 / H6 evaluation.** Per §2.2. With olive oil routed to descriptive-only at lock, H5/H6 effective evaluation reduces to 2-of-2 across PM software + running shoes.
9. **Olive oil descriptive arm.** Per §10. Report per-brand AI Presence at v0.9 matched subset alongside Trends acquisition outcome (PASS / PASS_E5 / E1a). Compute and report:
   - **Scale-mismatch index per category**: proportion of matched-subset brands with AI Presence ≥ 5% and Trends signal below display threshold. Compare across PM software (none), running shoes (none expected), olive oil (predicted 7/14 from Phase B).
   - **Diagnostic case studies**: Frescobaldi Laudemio, Olio Verde, Lucini — narrative description as scale-mismatch cases stronger than v0.11's Linear paradox (Linear: 86.5% AI Presence, 1.88 Trends; v0.12 cases: 17.7%–22.9% AI Presence, Trends below display threshold).
   - **No correlation statistic computed for the descriptive arm**; H1/H2/H4 explicitly routed to indeterminate per §3.4.
10. **Pooled sensitivity ρ.** Per §2.3. Pooled stack excludes olive oil's E1a-excluded brands; includes the 8 olive oil PASS / PASS_E5 brands plus PM software and running shoes.
11. **Sensitivity analyses.** US-only region (re-run H1 with US-only Trends data per category). Bonferroni-corrected p-values for secondary hypotheses per category. Report alongside primary inference.
12. **Canonical scoring.** Generate per-category and cross-category canonical scoring files with hypothesis status, per-brand pairs, correlation values, p-values, sensitivity values.
13. **Build report and paper.** Fork `build_report_v11.py` → `build_report_v12.py`; fork `build_charts_v11_pmtrends.py` → `build_charts_v12.py` with per-category scatter, leaderboard, and partial-correlation visualisations plus one cross-category summary. Draft SSRN paper (pandoc + xelatex template).
14. **Deposit at OSF project ec6wh, /v12/.**

**No additional analyses beyond the above will be reported as confirmatory.** Any further exploration is labeled exploratory and confined to discussion.

---

## 7. Falsification Summary

| Hypothesis | Confirmed | Falsified | Indeterminate |
|---|---|---|---|
| **H1 (per category)** | ρ > 0.5 AND p < 0.05 at **both** waves | ρ ≤ 0.5 OR p ≥ 0.05 at **either** wave | n < 10 at either wave (per §3.4) |
| **H2 (per category)** | \|Δρ\| ≤ 0.15 | \|Δρ\| > 0.15 | n < 10 at either wave |
| **H3 (per category)** | top-3 ⊆ top-5 at **both** waves | top-3 ⊄ top-5 at **either** wave | n < 5 at either wave (not anticipated) |
| **H4 (per category)** | partial ρ > 0.5 AND p < 0.05 at **both** waves | partial ρ ≤ 0.5 OR p ≥ 0.05 at **either** wave | n < 10 at either wave |
| **H5 (cross-category)** | v0.11 signature in ≥ 2 of 3 categories | v0.11 signature in 0 or 1 of 3 | All 3 categories routed to descriptive-only |
| **H6 (cross-category)** | Both Linear-style AND Todoist-style brands at both waves in ≥ 2 of 3 categories | Both-and-both pattern in 0 or 1 of 3 | All 3 categories routed to descriptive-only |

---

## 8. Deviations and Amendments

Any deviation from this pre-registration after git lock is logged in `/v12/DEVIATIONS.md` with timestamp, change rationale, and original-vs-amended specification. The v0.12 paper carries an explicit deviations section in declarations. Substantive amendments after data are touched are flagged as exploratory in the published paper.

---

## 9. Methodological Risks Documented at Lock Time

In addition to the E1–E5 decision rules in §5.4, the following risks are documented at lock:

1. **Brand-set composition.** Matched subsets include brands at soft edges of "premium" framing (Bertolli, Lucini in olive oil; Puma, Salomon, Topo Athletic, Norda in running). Registry-freeze convention applies; brands stay in. Caveat reported in v0.12 paper §6.
2. **H6 threshold sensitivity.** Thresholds anchored to v0.11 reference cases (Linear 86.5/1.88; Todoist 1.04/28). Marginal cases reported with threshold-anchoring rationale; thresholds not retroactively adjusted.
3. **'On' brand disambiguation risk.** The running brand 'On' has extreme polysemy ('on' is an English preposition); T1 topic-mid resolution is essential. If neither T1 nor T3 fallback resolves usable signal at Phase B, On is excluded under E1a. This is the highest-disambiguation-risk brand at v0.12.
4. **Multiplicity disclosure.** 18 per-category tests inflate false-positive rate under family-wise null hypothesis. Pre-registered position: per-category tests address independent construct claims in non-exchangeable populations; joint inference is via H5 (single 2-of-3 test). No Bonferroni or BH correction applied to per-category H1–H4. Position documented here and in the v0.12 paper §5.

---

## 10. Category-Scale Mismatch Finding (Olive Oil)

This section specifies the descriptive analysis that olive oil contributes to v0.12 in lieu of confirmatory H1–H4 inference. The finding emerged from Phase B validation (per §3.4a) and is reported descriptively because its operationalisation was not pre-registerable in advance — pre-registration could not specify which brands would fall below Trends' platform display threshold without first running validation.

### 10.1 What the finding is

In the premium olive oil category, the matched-subset brand set produced by v0.6 / v0.9 (Sonnet 4.6 + gpt-5.4-mini) includes brands AI-presents at non-trivial rates (3%–37%) whose consumer search-interest signal at the global level is **below Google Trends' display threshold**. Bundled-pivot validation (replicating the acquisition methodology) confirmed the threshold operates at the absolute-volume level, not the bundle-relative level: even with California Olive Ranch as a high-volume bundle anchor, 7 of 14 non-pivot brands return ALL_ZERO rescaled values across the 7-day validation window.

The finding extends v0.11's Linear-paradox case along a new dimension. v0.11 Linear paradox: 86.5% AI Presence with Trends signal of 1.88 (rescaled to Asana = 100). v0.12 scale-mismatch cases: 17.7%–22.9% AI Presence (Frescobaldi Laudemio, Olio Verde, Lucini) with Trends signal below platform display threshold — not merely small, but literally undetectable in the validator. The construct of AI Availability is shown to operate at a brand-coverage scale that consumer search at the platform level cannot resolve. This is a stronger separability claim than the boundary-mismatch of v0.11 alone.

### 10.2 What is reported

The v0.12 paper reports, for olive oil:

1. **Per-brand AI Presence (v0.9 matched subset) and Trends acquisition outcome.** Table including 15 matched-subset brands with columns: brand, market tier (registry), v0.9 AI Presence rate, Phase B disposition (PASS / PASS_E5 / EXCLUDED_E1a), within-window Trends mean at t₁ / t₂ (for PASS / PASS_E5 only; "below display threshold" for EXCLUDED_E1a). Source: `/v12/data/category_scale_mismatch_table.csv`.
2. **Scale-mismatch index per category.** Defined as: proportion of matched-subset brands with AI Presence ≥ 5% AND Trends signal below platform display threshold (per Phase B). Computed for all three categories:
   - PM software: predicted 0/17 (validated at v0.11)
   - Running shoes: predicted 0/13 (validated at v0.12 Phase B)
   - Olive oil: 7/14 = 50%
   The index quantifies the prevalence of the scale-mismatch in each category and supports cross-category comparison.
3. **Diagnostic case studies.** Narrative description of Frescobaldi Laudemio (22.9% / undetectable), Olio Verde (22.9% / undetectable), and Lucini (17.7% / undetectable) as the cleanest individual scale-mismatch cases at v0.12. Frantoio Muraglia (36.5% / bundled-marginal-sparse) discussed as the bundled-rescue threshold case.
4. **Discussion of Tri-System framework implications.** The scale-mismatch evidence is positioned as supporting separability of AI Availability from Mental Availability — not just a different boundary on the same scale (v0.11) but a different scale altogether (v0.12). Explicit cross-reference to the Tri-System Brand Growth paper (Gonzalez Castro, 2026) §4 and to Routledge monograph Chapter 4 (currently in production).

### 10.3 What is not reported

- **No correlation statistics for olive oil.** ρ, p-values, partial ρ, |Δρ|, top-3 / top-5 set membership are not computed for olive oil. H1, H2, H3, H4 olive oil are explicitly indeterminate per §3.4.
- **No imputation.** "Below display threshold" Trends values are reported as such; not imputed as 0, near-0, or otherwise. The whole point is that the construct cannot be placed on a common scale.
- **No revised H5 or H6 to include olive oil.** Cross-category arithmetic reduces to 2-of-2 across PM software + running shoes per §2.2.

---

## 11. Pre-Locked Companion Files

The following files committed in the same git tree at lock time and referenced by hash in the lock metadata block:

| File | Contents |
|---|---|
| `wave_windows_v0.12.json` | Exact Mon-Sun date ranges for t₁ and t₂, both regions |
| `registries/matched_subset_v0.12.json` | Per-category matched-subset brand lists |
| `registries/trends_query_strings_v0.12.json` | Per-brand T1/T2/T3 tier with disambiguation rationale, fallback rules, and Phase B locked status per brand |
| `registries/topic_id_resolution_log_v0.12.csv` | Per-brand Phase B locked acquisition query: tier, mid or string, entity label, lookup timestamp, rationale |
| `registries/brand_age_sources_v0.12.csv` | Per-brand founding year, primary URL, tie-breaker URL, notes (PM software section replicated from v0.11) |

---

## 12. Methodology Version and Cross-References

- **AIAS Presence Measurement Protocol.** v1.1 (unchanged) — SSRN 6722319.
- **Brand registries.** `brands_pm.json`, `brands_oliveoil.json`, `brands_running.json` — frozen at v0.6 lock; identical to v0.6 / v0.9 / v0.10 / v0.11 — distributed under `/v12/registries/`.
- **AI Presence input.** OSF project ec6wh, /v09/data/, git tag `v0.9-published`. Restriction: matched-model subset (Sonnet 4.6 + gpt-5.4-mini), three categories.
- **v0.11 prior.** OSF project ec6wh, /v11/, git tag `v0.11-prereg` (pre-reg) and `v0.11-published` (deposit). The v0.12 pre-reg replicates v0.11 §3.4 (with n-floor evolution), §4, §5, §5.4 (with E1a bundled-rescue amendment), and §6 step structure. PM software query specification table replicated verbatim from v0.11 §5.2.1.
- **Topic-ID resolution.** `pytrends` library (version pinned at lock). Raw suggestion outputs deposited at `/v12/data/phaseB_suggestions/`.
- **Pre-acquisition validation.** SerpAPI Google Trends engine, out-of-sample window 1–7 April 2026 (same as v0.11). Per-brand validation outputs at `/v12/data/phaseB_validation/`. Bundled-validation diagnostic at `/v12/data/phaseB_bundled/`.
- **Google Trends acquisition (post-lock).** SerpAPI Google Trends engine. Locked UTC timestamp captured at acquisition; raw JSON response per bundle deposited to `/v12/data/trends_raw/`.

---

## 13. Authorship and Declarations

**Author.** Pablo Ulpiano González Castro.
**Research entity.** Third System™ (thirdsystem.ai).
**Affiliation (academic).** Faculty, MPS Branding, School of Visual Arts.
**COI declaration.** The author is also Director of Corporate Brand Creative and Governance at Samsung Electronics America. The v0.12 study, like all AIAS programme publications, is independent research developed outside the scope of that employment. None of the brands in the three registries are Samsung properties.
**Funding.** None.
**Data and code availability.** All inputs (v0.9 AI Presence rates), Google Trends raw responses, topic-ID suggestion logs, pre-acquisition validation outputs, brand age source table, registry files, scoring outputs, build scripts, and SSRN paper draft are deposited at OSF project ec6wh, /v12/, prior to SSRN submission.

---

## 14. Lock

This document is locked at git commit *[pending]* on *[lock date pending]*, **prior to any Google Trends acquisition call against the v0.12 wave windows (t₁: 27 April – 3 May 2026; t₂: 4 May – 10 May 2026)**.

Pre-lock activity completed and deposited prior to tag:

- **PM software query specification:** replicated verbatim from v0.11 §5.2.1 into `registries/trends_query_strings_v0.12.json` PM software section. ✓
- **PM software brand-age rows:** replicated verbatim from v0.11 `/v11/registries/brand_age_sources.csv` into `registries/brand_age_sources_v0.12.csv` with schema-normalised mapping (brand_canonical→brand, launch_year→founding_year). 18 rows. ✓
- **Competitive tier assignments for all three categories:** confirmed encoded as `tier` field in `brands_pm.json`, `brands_oliveoil.json`, `brands_running.json`. Distribution: PM 5/8/6, olive oil 3/6/6, running 5/2/6 (inc/mid/chal). ✓
- **Phase A pivot verification.** California Olive Ranch (`/g/11cn92g97s`, mean 83.5, CV 12.4%, PASS) and Asics (`/m/04xxy1`, mean 84.5, CV 7.9%, PASS) verified at 2026-05-11. Asana inherited from v0.11. ✓
- **Phase B topic-mid resolution and pre-acquisition validation.** All 26 non-pivot olive oil and running brands resolved and validated. Locked Phase B outcomes per §3.4a: 7 olive oil E1a-excluded; Frantoio Muraglia PASS_E5 via bundled-rescue amendment; remaining olive oil and all 13 running brands PASS. Olive oil routes to descriptive-only at lock. ✓
- **Brand age verification.** Frantoio Muraglia (~1940) and McEvoy Ranch (1990) flagged APPROXIMATE in CSV. Both brands are in the v0.12 matched subset; Frantoio Muraglia retained as PASS_E5, McEvoy Ranch E1a-excluded. Approximate-year flag does not affect H4 covariate computation for the retained brand.

No analysis output exists at the moment of lock. The fully resolved Phase B specification (`topic_id_resolution_log_v0.12.csv`) and Phase B validation summary are committed in the same commit as the `v0.12-prereg` tag.
