# AIAS v0.11 — Pre-Registration

**Title.** PM Software × Google Trends Construct Validity — Phase 3 Pilot, t₁→t₂

**Version.** v0.11 pre-registration · draft for git lock
**Methodology Protocol.** AIAS Presence Measurement Protocol v1.1 (SSRN 6722319)
**Registry.** brands_pm.json (frozen at v0.6 lock; identical brand set used in v0.6 / v0.9 / v0.10)
**Date drafted.** 2026-05-09
**Lock target.** git commit prior to any Google Trends acquisition call against the v0.11 wave windows
**Author.** Pablo Ulpiano Gonzalez Castro
**Research entity.** Third System™

**Cross-cites.** AI Availability foundational paper (SSRN 6659000) · AIAS Presence Measurement Protocol v1.1 (SSRN 6722319) · v0.6 Cross-Category Findings (SSRN 6720959) · v0.7 Phantom-Brand BBB (SSRN 6721779) · v0.8 Discourse-Language Knives (SSRN 6728000) · v0.9 Longitudinal Re-Baseline (SSRN 6736878) · v0.10 Naive-Phantom Rate Stability (SSRN 6741163).

---

## 1. Background

The AIAS Presence Measurement Programme has, through v0.6 / v0.7 / v0.8 / v0.9 / v0.10, established a methodologically rigorous LLM-side measurement of brand presence in AI-mediated decision contexts. The programme's foundational paper introduces AI Availability as a theoretical layer above Mental and Physical Availability; the protocol document specifies how the *Presence* component of AI Availability is operationalised; v0.6 establishes a five-category cross-brand baseline; v0.7 / v0.8 demonstrate designed-for-test discrimination on phantom brands and discourse-language confounds; v0.9 / v0.10 demonstrate longitudinal stability of gross presence and the boundaries of caveated correction.

What none of these prior studies tests is the question on which the programme's external validity ultimately rests: **does LLM Presence correspond to anything consumers actually do?**

The Tri-System Brand Growth manuscript (Gonzalez Castro, 2026) names this gap explicitly. The framework's central empirical limitation, as currently published, is that **AI Presence has unverified consumer-level predictive value**. The framework has been developed with care to specify what it claims (a third availability layer in an AI-mediated retrieval substrate) and what it does not (proven causal predictive validity over consumer behaviour). v0.11 begins to close that gap.

v0.11 is positioned as the **Phase 3 pilot** in the AIAS programme: the smallest viable construct-validity test against an external behavioural validator. Phase 3 expansion (v0.12 to a 3-category protocol minimum, v0.13 to all five baseline categories) is contingent on v0.11 cleanly establishing the methodology. Phase 4 (the remaining five AIAS components — Ranking, Consistency, Coverage, Grounding, Sentiment) is contingent on Phase 3 by design.

### Why PM software

PM software is selected as the pilot category for three converging reasons. The discourse is English-only across the registry, removing the language-bias confounds that v0.8 isolated. Every brand has a public web presence and an external behavioural validator (Google Trends search volume, free and publicly accessible per brand). Among the five v0.6 baseline categories, PM software showed the most stable cross-model agreement, providing the cleanest input distribution for a correlation test.

### Why Google Trends

Google Trends provides daily-granularity search-interest indices per brand, free public access via documented APIs, worldwide and country-resolution geographic specificity, and entity-level disambiguation through topic IDs. Search interest is a behavioural proxy for brand mindshare — it captures what consumers actively look up in a category — and is the validator of choice for a construct-validity test where the construct is brand-level salience.

Google Trends is **not raw query volume**. The platform exposes only the 0–100 normalised search-interest index, normalised within the query bundle and timeframe of each request. The methodological consequences of that constraint are addressed in §5.

### What v0.11 does and does not test

v0.11 tests construct validity at single-category, single-validator scope. It is not a generalisation claim across categories, nor a causal claim about the direction of correspondence between AI Presence and search interest. The hypothesis is that, for the PM software category, per-brand AI Presence rate co-varies with per-brand search interest at sufficient strength to support the construct. The pilot is sized for *whether the methodology yields a defensible test*, not for definitive resolution of the construct-validity question.

**No new LLM measurement is required.** v0.6 and v0.9 deposited the AI Presence rate input; v0.11 acquires the Google Trends side and conducts the correlation test on existing inputs.

---

## 2. Hypotheses

### H1 (primary, confirmatory) — Cross-Sectional Construct Validity

Per-brand AI Presence rate co-varies with per-brand Google Trends search-interest index at sufficient strength to support the construct.

- **Operationalisation.** Spearman ρ computed across the analysis brand set (subject to n-floor — see §3.4) between per-brand AI Presence rate and per-brand within-window mean Google Trends search interest (pivot-rescaled, Worldwide region). Computed independently for t₁ and t₂.
- **Confirmed if** ρ > 0.5 AND p < 0.05 (one-tailed) at **both** waves.
- **Falsified if** ρ ≤ 0.5 OR p ≥ 0.05 at **either** wave.

The both-waves conjunction is the test's primary FWER control: under the null, the joint probability of both passing is ≈ 0.05² = 0.0025, more stringent than 0.05 family-wise.

### H2 (secondary, confirmatory) — Correlation Stability

The correlation strength is stable across t₁ → t₂.

- **Operationalisation.** |ρ_t₂ − ρ_t₁|, computed against the t₁ and t₂ Spearman ρ values from H1.
- **Confirmed if** |Δρ| ≤ 0.15.
- **Falsified if** |Δρ| > 0.15 in either direction.

H2 protects against the interpretation that H1 confirmation is wave-specific noise. A construct stable enough to support causal inference should produce a stable correlation magnitude over a 7-day longitudinal interval.

### H3 (secondary, confirmatory) — Leaderboard Directional Consistency

Brands ranked top-3 by AI Presence are also among the top-5 by Google Trends search interest, at each wave independently.

- **Operationalisation.** At each wave, identify the top-3 brands by AI Presence rate and the top-5 brands by Google Trends within-window mean. Compute set membership of the top-3 within the top-5.
- **Confirmed if** all 3 of the AI-Presence top-3 appear in the Trends top-5, at **both** waves.
- **Falsified if** ≥ 1 of the AI-Presence top-3 is absent from the Trends top-5, at **either** wave.

H3 provides a rank-categorical check that survives noise more robustly than the correlation magnitude. A construct strong enough to support inference at the top of the distribution should produce overlapping leaderboards.

### H4 (secondary, confirmatory) — Covariate-Controlled Correlation

The H1 correlation survives partialling out brand age and within-category competitive density.

- **Operationalisation.** Spearman partial correlation between per-brand AI Presence rate and per-brand Google Trends search interest, controlling for (a) brand age = years since product launch (sourced from Wikipedia or primary corporate source at pre-reg lock), (b) competitive density = market tier from registry treated as ordinal (incumbent=1, mid-tier=2, challenger=3). Computed independently for t₁ and t₂.
- **Confirmed if** partial ρ > 0.5 AND p < 0.05 (one-tailed) at **both** waves.
- **Falsified if** partial ρ ≤ 0.5 OR p ≥ 0.05 at **either** wave.

H4 is a specification check on H1: the correlation should not be driven entirely by the obvious confounds of older / more established brands also being more searched.

### Test family and FWER

H1 is the primary confirmatory test. H2 / H3 / H4 are secondary confirmatory tests. The both-waves conjunction in H1 and H4 provides built-in FWER control for those hypotheses. No explicit family-wise correction is applied across H1–H4 in the primary inference; the structural primary/secondary framing does the equivalent work. Bonferroni-corrected p-values for all secondary hypotheses (α/3 = 0.0167) are reported in the OSF deposit's analysis output as a sensitivity.

All p-values are one-tailed throughout. The construct's predicted directionality (positive correlation between AI Presence and search interest) is theoretical; a negative correlation, if observed, would be a different and surprising finding outside H1's prediction space.

---

## 3. Threshold Justification

### ρ > 0.5

The 0.5 threshold for the H1 correlation magnitude reflects the standard "moderate-to-strong correlation" benchmark in behavioural research. Below 0.5, a positive correlation would still be directionally consistent with the construct but would be too weak to support practical inference about AI Presence as a behavioural proxy. Above 0.5, the construct passes a non-trivial bar even at small n. The threshold is kept identical between Spearman primary and Pearson sensitivity; the literal magnitude does not change with the test type, and at n≈18 the two statistics typically track each other closely when the underlying relationship is well-behaved.

### |Δρ| ≤ 0.15 (H2)

The 0.15 stability band is calibrated against the test-retest stability typical of behavioural correlation measures over a one-week interval. A construct stable across consumers and time should not exhibit > 0.15 correlation drift over 7 days; the threshold is tight enough to detect meaningful instability but lenient enough to absorb sampling variance at small n. The band is symmetric and applied as |Δρ|, not signed.

### Top-3 ⊆ Top-5 (H3)

The asymmetric 3-vs-5 specification gives the leaderboard test slack at the boundary while preserving the directional claim. A strict top-3 ⊆ top-3 would over-constrain rank-order at small n; a top-3 ⊆ top-7 would under-constrain to the point of triviality. Top-3 in the analysis brand set corresponds to the leadership zone of the construct; top-5 in Trends corresponds to the visible-leadership band.

### One-tailed at α = 0.05

The construct predicts positive correlation; tests are one-tailed. The α = 0.05 is per-test; FWER is controlled structurally (both-waves conjunction; primary/secondary framing) rather than via p-value adjustment. See §2.

### 3.4 Effective-n Floor

H1, H2, and H4 are evaluated only if **n ≥ 16 of the 19 registry brands** have usable Trends signal at *each* wave, evaluated independently per wave. "Usable Trends signal" is defined in §5.4 (E1b). If either wave's brand count falls below 16, **H1 / H2 / H4 are routed to descriptive disclosure for both waves** (paired routing — H1 and H2 are coupled across waves by construction; H4 inherits the coupling). H3 is computable per-wave from whatever brands are present and is reported with explicit flagging if dropouts affect the rank composition.

The floor is set at 16 of 19 because the test's discriminating power lives in the brand-tier variance, and the brands at risk of dropping (challenger-tier brands with extreme semantic noise) are systematically the small ones. Losing more than three brands collapses the construct's variance source toward the saturated incumbent zone and biases the correlation toward inflation. The 16-of-19 floor tolerates exactly the predicted three-brand worst-case dropout.

**Running dropout count at lock.** As of pre-reg lock, **one** of the three tolerated dropouts has materialised: Shortcut is excluded pre-acquisition under E1a (see §5.4 and §4 below). The remaining tolerance budget is **two further dropouts at acquisition** before the floor is breached. Effective n entering acquisition: 18.

The floor is fixed at lock and is not adjusted post hoc.

---

## 4. Data and Subset

### Source 1 — AI Presence rate (pre-existing)

Per-brand AI Presence rates at t₁ and t₂ are pulled from prior deposits:

- **t₁ AI Presence (per brand).** v0.9-deposited canonical scoring at the matched-model subset (Sonnet 4.6 + gpt-5.4-mini) restricted to PM software, evaluating responses collected in the v0.6 baseline window (29–30 April 2026). Source: OSF project ec6wh, /v09/data/, git tag `v0.9-published`.
- **t₂ AI Presence (per brand).** v0.9-deposited canonical scoring at the matched-model subset (Sonnet 4.6 + gpt-5.4-mini) restricted to PM software, evaluating responses collected in the v0.9 re-baseline window (7 May 2026). Source: same as above.

The matched-model subset (Sonnet 4.6 + gpt-5.4-mini) is identical across both waves to maintain comparability with v0.9 H4. Other models present in the v0.6 / v0.9 deposits are excluded for v0.11.

### Source 2 — Google Trends search-interest index (acquired at v0.11)

Per-brand Google Trends search-interest index acquired at a single locked UTC timestamp following pre-reg lock and prior to any analysis. Acquisition specification:

- **Region (primary).** Worldwide.
- **Region (sensitivity).** US-only, captured in the same acquisition session, deposited but not used in primary inference.
- **Granularity.** Daily.
- **Wave windows.**
  - **t₁ window.** 27 April – 3 May 2026 (Mon–Sun, 7 days, centred on 30 April — the v0.6 collection closing day).
  - **t₂ window.** 4 May – 10 May 2026 (Mon–Sun, 7 days, centred on 7 May — the v0.9 collection day).
  - Windows are fully disjoint at the 3 May / 4 May boundary. Both windows have identical weekday composition (one of each Monday through Sunday).
- **Per-brand within-window statistic.** Arithmetic mean of the daily 0–100 search-interest index across the 7 days.
- **Cross-brand normalisation.** Pivot-rescaled. See §5.1.
- **Index type.** Google Trends 0–100 search-interest index (Google does not publish raw query counts; the 0–100 index is the only available exposure of the underlying volume).
- **Acquisition library.** SerpAPI Google Trends engine (`engine=google_trends`, `data_type=TIMESERIES`, `geo=` worldwide for primary / `geo=US` for sensitivity, `no_cache=true`). Library version pinned at acquisition; raw JSON response per bundle deposited to `/v11/data/trends_raw/`. Per-bundle UTC timestamp, parameters, and rate-limit status captured in `/v11/data/trends_acquisition_log.csv`.

### Brand registry

`brands_pm.json` (frozen at v0.6 lock; identical to the registry used in v0.6 / v0.9 / v0.10). 19 brands across three market tiers: 5 incumbent, 8 mid-tier, 6 challenger. Distributed under `/v11/registries/brands_pm.json` in the OSF deposit.

### Pre-acquisition exclusions

**Shortcut** is excluded from the v0.11 analysis based on pre-acquisition validation. The locked T3 compound query `"shortcut project management"` returned zero Trends signal at the out-of-sample validation window (April 1–7, 2026), with SerpAPI returning the explicit response *"Google Trends hasn't returned any results for this query"*. The exclusion is logged in `/v11/data/phaseB_validation/validation_summary_*.json` and `/v11/data/phaseB_validation/validation_Shortcut.json`. Per E1a (see §5.4), the exclusion is documented in the locked spec table at the `v0.11-prereg` tag and counts toward the n-floor as one dropout. **Effective n at acquisition: 18 brands.**

### Defunct brand disclosure (Height)

**Height** (`height.app`) shut down operations on 24 September 2025, approximately seven months before the v0.11 measurement windows. Per the registry-frozen-ness principle (registry locked at v0.6), Height remains in the v0.11 analysis as a phantom brand — analogous to Mint in v0.7 / v0.10. Pre-acquisition validation confirmed that the locked T3 compound query `"height project management"` returns non-zero residual Trends signal at the out-of-sample window (April 1–7, 2026), consistent with the residual-mindshare framing of phantom-brand presence developed in the v0.7 / v0.10 designed-for-test thread. Height is **not excluded** from H1 / H2 / H3 / H4 inference on grounds of brand status; the v0.11 paper's Discussion section will address the implications of including a defunct brand in the cross-sectional construct validity test, with reference to the AIAS programme's prior treatment of phantom brands.

### Unit of analysis

A single brand is the unit of analysis. Each brand contributes one (AI Presence rate, Trends within-window mean) pair per wave. Two waves yields **18 pairs at full coverage** (subject to further n-floor evaluation at acquisition; Shortcut excluded pre-acquisition per above).

---

## 5. Operationalisation

### 5.1 Pivot rescaling (Trends acquisition)

Google Trends 0–100 search-interest indices are normalised within the query bundle and timeframe of each request. Bundles can contain at most 5 terms. To enable cross-brand comparability across the 18-brand analysis set, the acquisition uses overlapping bundles each containing the same **pivot brand**.

- **Pivot brand.** Asana (topic mid `/m/0c3z_p8`). Selection criteria: incumbent-tier, expected highest stable Trends volume in the registry, present across the competitive set as a comparison anchor in industry coverage. Validated at Phase A test (see `/v11/data/phaseA_test/`): mean within-window value 74.9 across the 14-day combined-wave window with realistic daily variance.
- **Bundle structure.** Each acquisition bundle contains [Pivot, Brand₁, Brand₂, Brand₃, Brand₄] — Asana plus four other brands. With 17 non-pivot brands in the analysis set, this requires 5 bundles (four bundles of 4 non-pivot brands; one bundle of 1 non-pivot brand plus padding). Padding-brand choice is a high-volume non-PM term ("kanban") that anchors the bundle without contaminating the rescaling, and is excluded from the analysis. Actual bundle composition is documented in `/v11/data/trends_acquisition_log.csv` at acquisition time.
- **Rescaling formula.** For each brand B and each day d in each wave window, the rescaled index is:

  `rescaled_B(d) = raw_B(d) / raw_Pivot(d) × 100`

  where `raw_X(d)` is the Google Trends 0–100 daily value for brand X on day d in the bundle containing both B and Pivot. The rescaling produces a dimensionless ratio expressing each brand's daily search interest relative to the pivot, multiplied by 100 for readability.
- **Within-window statistic.** Per-brand within-window mean is the arithmetic mean of `rescaled_B(d)` across the 7 days of the wave window.
- **Pivot brand's own statistic.** The pivot brand's rescaled value is by construction 100 every day. Its within-window mean is therefore 100 by definition. The pivot is included in the correlation analyses as a brand on equal footing with the others — its position in the AI Presence dimension carries informative variance even if its Trends dimension is anchored.
- **Reproducibility note.** Google Trends responses are sampled, not deterministic. The 0–100 values can vary slightly across requests for the same window. The acquisition's exact UTC timestamp is captured, and the raw API response per bundle is captured to OSF before any rescaling or transformation. The pulled snapshot is the locked validator; subsequent pulls are not used as a substitute for the locked snapshot.

### 5.2 Brand-name disambiguation (tiered query specification)

Each brand is assigned to one of three query tiers:

- **T1 — Topic ID.** Where Google Trends has an entity (topic) ID corresponding unambiguously to the PM-software brand, the topic mid (e.g. `/g/11g9mtgxxw`) is passed as the query. Topic IDs aggregate Google's own canonical disambiguation across variant strings.
- **T2 — Distinctive search string.** Where no topic ID exists but the brand string is low-noise, the bare brand name is used as the query.
- **T3 — Brand+category compound.** Where no topic ID exists and the brand string is high-noise, the fixed compound `"<brand> project management"` is used as the query, applied uniformly across all T3-tier brands.

Topic-ID resolution was conducted via `pytrends.suggestions()` on 2026-05-10. The procedure was: (a) call `pytrends.suggestions(keyword=<search_input>)` for each brand; (b) inspect candidate entities by title and type; (c) pick the most specific brand-product entity available (e.g. "Software", "Productivity software", "Software company"); (d) for brands where no software entity surfaced, retry with a domain-style search input (`coda.io`, `linear.app`, `height.app`, `usemotion`, `shortcut.com`); (e) descend to T3 for brands where retry also surfaced no entity. Raw suggestion outputs are deposited at `/v11/data/phaseB_suggestions/`. The full per-brand specification — initial tier, final tier, exact query (topic mid or string), entity label where T1, lookup timestamp, and rationale — is shown in the table below and committed to `/v11/registries/brands_pm_query_spec.csv` at pre-reg lock.

#### 5.2.1 Per-brand specification table (locked)

| # | Brand | Market tier | Final query tier | Acquisition query | Entity label (T1) | Lookup ts (UTC) |
|---|---|---|---|---|---|---|
| 1 | Asana | incumbent | T1 | `/m/0c3z_p8` | Asana, Inc. — Software | 2026-05-10T03:49:00Z |
| 2 | Monday | incumbent | T1 | `/g/11h1m5p60w` | monday.com — Software company | 2026-05-10T04:12:26Z |
| 3 | Jira | incumbent | T1 | `/g/11bc5c0lmw` | Jira — Software | 2026-05-10T04:12:26Z |
| 4 | Trello | incumbent | T1 | `/m/0h665rh` | Trello — Software | 2026-05-10T04:12:26Z |
| 5 | Confluence | incumbent | T1 | `/m/05nyz0` | Confluence — Software | 2026-05-10T04:12:26Z |
| 6 | Notion | mid-tier | T1 | `/g/11fd7dbddz` | Notion — Productivity software | 2026-05-10T04:12:26Z |
| 7 | ClickUp | mid-tier | T1 | `/g/11g9n26732` | ClickUp — Project management software company | 2026-05-10T04:12:26Z |
| 8 | Smartsheet | mid-tier | T1 | `/m/010h7t67` | Smartsheet Inc — Software company | 2026-05-10T04:12:26Z |
| 9 | Airtable | mid-tier | T1 | `/g/11c3ypc1q3` | Airtable — Web site | 2026-05-10T04:12:26Z |
| 10 | Basecamp | mid-tier | T1 | `/m/0d04n6` | Basecamp — Software | 2026-05-10T04:12:26Z |
| 11 | Coda | mid-tier | T1 | `/g/11f3h7_jw9` | Coda — Document editor | 2026-05-10T04:17:11Z |
| 12 | Wrike | mid-tier | T2 | `wrike` | n/a | n/a |
| 13 | Workfront | mid-tier | T2 | `workfront` | n/a | n/a |
| 14 | Todoist | challenger | T2 | `todoist` | n/a | n/a |
| 15 | GitHub Projects | challenger | T2 | `github projects` | n/a | n/a |
| 16 | Linear | challenger | T3 | `linear project management` | n/a | n/a |
| 17 | Height | challenger | T3 | `height project management` | n/a | n/a |
| 18 | Motion | challenger | T3 | `motion project management` | n/a | n/a |
| 19 | Shortcut | challenger | **EXCLUDED (pre-acquisition, E1a)** | `shortcut project management` (locked but unused) | n/a | n/a |

Pre-acquisition validation results (out-of-sample window 1–7 April 2026) deposited at `/v11/data/phaseB_validation/`. 17 brands PASS validation (non-zero, non-flat timeseries returns). 1 brand SKIP (Asana, validated at Phase A). 1 brand FAIL (Shortcut, "Google Trends hasn't returned any results for this query"; excluded under E1a).

### 5.3 H4 covariate operationalisation

- **Brand age.** Years since product launch, sourced per brand from Wikipedia infobox or primary corporate source ("About" page, founder interview, original launch announcement). Source URL captured at pre-reg lock per brand. The full per-brand source table is committed to `/v11/registries/brand_age_sources.csv`.
- **Competitive density.** Market tier from `brands_pm.json` treated as ordinal: incumbent = 1, mid-tier = 2, challenger = 3. The mapping is fixed and inherits the registry's own tier assignment.

### 5.4 Pre-Specified Decision Rules — Edge Cases

**E1a — Pre-acquisition exclusion.** If a brand's locked acquisition query returns no Trends signal during pre-acquisition validation (validation script `validate_acquisition_queries.py` against the out-of-sample April 1–7, 2026 window), the brand is excluded from the v0.11 analysis. Pre-acquisition exclusions are documented in the locked spec table (§5.2.1) at the `v0.11-prereg` tag with rationale, and each exclusion counts toward the n-floor (§3.4) as one dropout. As of lock: Shortcut excluded under E1a.

**E1b — At-acquisition exclusion.** If a brand's pivot-rescaled within-window mean is 0 OR within-window standard deviation is 0 at either wave during the actual acquisition (May 2026 wave windows), the brand is excluded from that wave's analysis. The exclusion is logged with rationale in `/v11/data/at_acquisition_exclusions.csv`. Wave-level n is recalculated; n-floor evaluation per §3.4 then determines whether confirmatory inference proceeds.

**E2 — Pivot brand failure.** If the pivot brand (Asana) returns zero or anomalous values in any acquisition bundle (bundle rejection, query failure, sampling artefact), acquisition halts. The pivot is the rescaling anchor; pivot failure invalidates the whole bundle. Re-acquisition follows a documented retry protocol (up to 3 attempts at the same UTC timestamp; if all fail, acquisition is deferred to a new locked timestamp and the previous attempt is logged but not used).

**E3 — At-acquisition topic-ID failure.** If a T1-tiered brand's acquisition query (topic mid) returns anomalous signal at the actual wave windows (zero values at wave windows despite passing pre-acquisition validation at the out-of-sample window), the brand triggers E1b exclusion. The pre-reg does not permit re-querying with an alternative entity post-lock; topic-ID assignments are fixed at the v0.11-prereg tag.

**E4 — Trends API failure during acquisition.** If Google Trends acquisition fails during the locked session (rate limiting, partial bundle returns, network failure), acquisition halts and a documented retry protocol engages. Up to 3 retry attempts at the same locked UTC timestamp; if all fail, the acquisition is deferred to a new locked timestamp, the previous attempt is logged with the failure mode, and the new timestamp becomes the locked acquisition timestamp.

**E5 — Within-window data sparsity.** If a brand has Trends signal on fewer than 4 of the 7 within-window days at either wave (i.e., majority-zero within window), the within-window mean is reported but flagged. The brand is included in the analysis if the mean is > 0 and standard deviation is > 0 (per E1b), but the sparsity flag is reported alongside H1 outcome and addressed in the descriptive narrative if it affects > 3 brands.

---

## 6. Analysis Plan

1. **Pre-acquisition.** Verify brands_pm.json frozen state. Verify v0.9-deposited matched-subset AI Presence rates for PM software at t₁ (v0.6 collection) and t₂ (v0.9 collection). Verify brand age sources and capture per-brand source URL table. (Done at pre-reg lock per `/v11/registries/brand_age_sources.csv`.)
2. **Trends acquisition.** Execute pivot-bundled acquisition at single locked UTC timestamp post-lock. Capture raw API response per bundle. Capture bundle composition log. Apply pivot rescaling per §5.1.
3. **Validator construction.** Compute per-brand within-window mean for t₁ and t₂. Apply E1b / E5 rules. Determine per-wave brand count.
4. **n-floor check.** Verify n ≥ 16 at both waves per §3.4. If breached, route H1 / H2 / H4 to descriptive disclosure path.
5. **H1 evaluation.** Compute Spearman ρ at t₁ and t₂. Compute one-tailed p. Evaluate against ρ > 0.5 AND p < 0.05 conjunction. Compute Pearson r at both waves as sensitivity.
6. **H2 evaluation.** Compute |Δρ| from t₁ and t₂ Spearman ρ values. Evaluate against ≤ 0.15.
7. **H3 evaluation.** Identify top-3 by AI Presence and top-5 by Trends at each wave. Compute set membership.
8. **H4 evaluation.** Compute Spearman partial correlation at each wave controlling for brand age and competitive density. Evaluate against ρ > 0.5 AND p < 0.05 conjunction at both waves.
9. **Sensitivity analyses.** US-only region (re-run H1 with US-only Trends data). Bonferroni-corrected p-values for H2 / H3 / H4 (α/3 = 0.0167). Report alongside primary inference.
10. **Canonical scoring.** Generate canonical_scoring.csv and canonical_scoring.json with hypothesis status, per-brand pairs, correlation values, p-values, sensitivity values.
11. **Build report and paper.** Generate brand-format report (build_report_v11.py forks build_report_v10.py; build_charts_v11_pmtrends.py with construct-validity-specific charts: scatter at each wave with brand labels, leaderboard comparison, partial-correlation visualisation). Draft SSRN paper (pandoc + xelatex per established template).
12. **Deposit at OSF project ec6wh, /v11/.**

**No additional analyses beyond the above will be reported as confirmatory.** Any further exploration is labeled exploratory and confined to the discussion section.

---

## 7. Falsification Summary

| Hypothesis | Confirmed | Falsified | Indeterminate |
|---|---|---|---|
| **H1** — Cross-sectional construct validity | ρ > 0.5 AND p < 0.05 at **both** waves | ρ ≤ 0.5 OR p ≥ 0.05 at **either** wave | n < 16 at either wave (per §3.4) |
| **H2** — Correlation stability | \|Δρ\| ≤ 0.15 | \|Δρ\| > 0.15 | n < 16 at either wave |
| **H3** — Leaderboard consistency | top-3 ⊆ top-5 at **both** waves | top-3 ⊄ top-5 at **either** wave | n insufficient to define top-5 (n < 5 at either wave; not anticipated) |
| **H4** — Covariate-controlled | partial ρ > 0.5 AND p < 0.05 at **both** waves | partial ρ ≤ 0.5 OR p ≥ 0.05 at **either** wave | n < 16 at either wave |

---

## 8. Deviations and Amendments

Any deviation from this pre-registration after git lock is logged in `/v11/DEVIATIONS.md` with timestamp, change rationale, and the original-vs-amended specification. The v0.11 paper carries an explicit deviations section in its declarations block. Substantive amendments after data are touched are flagged as exploratory in the published paper, regardless of label.

---

## 9. Methodology Version and Cross-References

- **AIAS Presence Measurement Protocol.** v1.1 (unchanged) — SSRN 6722319.
- **Brand registry.** brands_pm.json (frozen at v0.6 lock; identical to v0.6 / v0.9 / v0.10) — distributed under `/v11/registries/`.
- **AI Presence input.** OSF project ec6wh, /v09/data/, git tag `v0.9-published`. Restriction: matched-model subset (Sonnet 4.6 + gpt-5.4-mini), PM software category.
- **Topic-ID resolution.** `pytrends` library (version pinned at lock). Raw suggestion outputs deposited at `/v11/data/phaseB_suggestions/`.
- **Pre-acquisition validation.** SerpAPI Google Trends engine, out-of-sample window 2026-04-01 to 2026-04-07. Per-brand validation outputs at `/v11/data/phaseB_validation/`. Summary at `validation_summary_*.json`.
- **Google Trends acquisition (post-lock).** SerpAPI Google Trends engine. Locked UTC timestamp captured at acquisition; raw JSON response per bundle deposited to `/v11/data/trends_raw/`.

---

## 10. Authorship and Declarations

**Author.** Pablo Ulpiano Gonzalez Castro.
**Research entity.** Third System™ (thirdsystem.ai).
**Affiliation (academic).** Faculty, MPS Branding, School of Visual Arts.
**COI declaration.** The author is also Director of Corporate Brand Creative and Governance at Samsung Electronics America. The v0.11 study, like all AIAS programme publications, is independent research developed outside the scope of that employment. None of the brands in `brands_pm.json` are Samsung properties.
**Funding.** None.
**Data and code availability.** All inputs (v0.9 AI Presence rates), Google Trends raw responses, topic-ID suggestion logs, pre-acquisition validation outputs, brand age source table, registry files, scoring outputs, build scripts, and SSRN paper draft are deposited at OSF project ec6wh, /v11/, prior to SSRN submission.

---

## 11. Lock

This document is locked at git commit a039560 on 2026-05-10, **prior to any Google Trends acquisition call against the v0.11 wave windows (t₁: 27 April – 3 May 2026; t₂: 4 May – 10 May 2026)**.

Pre-lock activity completed and deposited:
- Topic-ID resolution via `pytrends.suggestions()` (deposited at `/v11/data/phaseB_suggestions/`).
- Pre-acquisition query validation via SerpAPI against the out-of-sample window 2026-04-01 to 2026-04-07 (deposited at `/v11/data/phaseB_validation/`).
- Phase A pivot-brand verification (deposited at `/v11/data/phaseA_test/`).

No analysis output exists at the moment of lock. The fully resolved per-brand query specification table (§5.2.1) is committed in the same commit as the `v0.11-prereg` tag.
