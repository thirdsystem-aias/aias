# AIAS™ Presence Measurement Protocol — Pre-Registration v0.43 (revision r1, draft for review)

**Study:** Predictive validity of the AIAS Presence and Consistency scores against later change in US search interest. Stage 1 on past data (scores of June 2026 → change to November 2026); Stage 2 prospective (scores of November 2026 → change to March 2027), locked now, before any of its outcome weeks has happened; and the monthly outcome-tracking protocol that feeds Stage 2.
**Design:** Longitudinal, correlational and rank-based, within category. The predictors are scores the programme has already locked and published; no AI model is called. The outcome is the change in each brand's US Google search interest between two four-week windows, from Google Trends through SerpAPI (the programme's v0.11 and v0.25 source), measured in size-matched, chained request bundles, in three pulls at least 24 hours apart.
**Programme position:** Study list #60 (predictive validity on past data → the predictive-validity paper) and the Presence and Consistency part of #62 (predictive validity on the monthly snapshots → validated AIAS 6.0). v0.29 bound Presence's convergent and discriminant evidence and left predictive validity open for want of a longitudinal criterion; this study supplies that criterion.
**Scores (locked):** Presence score P and Consistency score C* as locked by Methodology v1.9 (SSRN 7685126) and used by AIAS 2.0 (`osf/methodology/v1_9/v1_9_unit_table.csv`); recall Presence π̂ as locked by v0.41 (SSRN 7685100); for the new model panel, v0.42's t₄ measures (§2.1).
**Lock target:** git tag `v0.43-prereg-r1` on branch `v0.43`, pushed to `origin`. **External anchor (pre-declared):** deposit of this pre-registration, the frozen inputs, the scripts and the lock manifest at OSF `ec6wh` → `v43/prereg/`, with `v43/anchor/` naming the tag's commit, before any search-interest request. The acquisition script refuses to run until the tag is on `origin` and the anchor file exists.
**Pre-registrant:** Pablo Ulpiano González Castro
**Status:** r1 draft, sent to the pre-registrant for review on 2026-11-10 (UTC) and deposited on OSF at `v43/prereg/draft/`. Locks 24 hours after it reached him unless he objects (programme rule for new data collections, Nov 9, 2026). No search-interest data has been requested for any brand of this study; the repository holds no Google Trends data for these brands and none later than May 2026.
**Data access:** requests need a SerpAPI key, which the pre-registrant provides. If the key arrives after the lock, collection starts when it does; every window is fixed in calendar time (§2.1), so a later start changes no measurement. Requests do not run during v0.40's collection window (2026-11-17 to 2026-11-21).

---

## §1 Context

AIAS 2.0 reports two scores side by side, Presence and Consistency, separable from each other and stable over five months on the legacy six-model panel (v1.9; v0.41). Presence has convergent evidence (same-week search interest, ρ = 0.74, n = 24, v0.25), discriminant evidence (Amazon sales rank, v0.26; the BRAND norms, v0.28) and a baseline that binds them (v0.29). It has no predictive evidence: no study has yet asked whether a brand's AI availability says anything about where its demand goes next.

Two accounts predict opposite answers.

1. **AI availability leads.** If AI answers are a third route by which brands come to mind and to hand (the Tri-System framework, MSI Working Paper Report No. 26-132), a brand that AI assistants name more than its current search level would suggest should gain search interest relative to comparable brands.
2. **AI availability lags.** If model answers mostly echo training data and web text that trail the market, AI presence beyond a brand's current search level marks a brand whose popularity peaked earlier, and search momentum carries it further down, while rising brands are under-named. This predicts the opposite sign.

The tests are directional (account 1); a result of the opposite sign is reported as support for account 2. The criterion is Google search interest: the programme's established external signal (v0.11, v0.25), available weekly for any brand in the US, and a behavioural trace of people looking for a brand. It is not sales. Sales rank, also named in the plan, is not collected here until the pre-registrant chooses its source (§4.6).

Stage 1 can run now because the June scores and the June-to-November search history both exist; it is pre-registered because those search data have not been looked at. Stage 2 repeats the test forward, from the November scores (t₃, v0.41; t₄, v0.42) to March 2027, and is locked before any of its outcome weeks has happened.

---

## §2 Pre-registered hypotheses

### §2.1 Definitions (used by every test)

- **Brand units.** The 112 brand units of the five omnibus registries (v0.19 audiophile headphones 16, v0.20 skincare 24, v0.21 cosmetics 24, v0.22 automotive 24, v0.23 premium spirits 24), as in v0.41 and v0.42. Rare Beauty is a unit in both v0.20 and v0.21 and is requested within each substrate's bundles. v0.23 brands keep their codes (S01–S24) in every output; their names (`osf/v23/scripts/acquire_v0_23.py`) are used only to form search terms.
- **Substrate.** The analysis stratum: each of the five registries.
- **Weeks and windows.** A week is a Google Trends week, Sunday to Saturday. W(e) = the four complete weeks ending on Saturday e. For unit b in one request, S_b(W) = the sum of b's four weekly index values in W.
- **Change (outcome).** Y_b = ln[(S_b(W_end) + 1) ÷ (S_b(W_base) + 1)], computed inside one request, so it does not depend on the request's scale; combined over bundles and pulls as in §5.2.
- **Level (control).** L_b = b's mean weekly index over W_base on its substrate's chained scale (§5.2), as a within-substrate rank averaged over pulls.
- **Momentum (control, `H_Pred_Presence_Momentum` only).** M_b = ln[(S_b(W_base) + 1) ÷ (S_b(W_prior) + 1)].
- **Seasonally adjusted change.** Y^SA_b = Y_b − Y′_b, where Y′_b is the same change over the same calendar weeks one year earlier (both windows moved back 52 weeks).
- **Presence score.** P = 100 · (C_P/6 + 2π̂)/3, the AIAS 2.0 Presence score as locked in v1.9 (column `P` of the v1.9 unit table), with C_P the number of the six models that recognise the brand and π̂ its recall rate. For the new panel at t₄: P_new = 100 · (r + 2π̂)/3 on N3 without search (S0), where r is the share of answered N3 model-runs coding the brand as recognised and π̂ is v0.42's recall rate on N3, S0 (v0.42 §2.1). If v0.42's §5.4 replaces N3 by C3 for S0, the same replacement applies here.
- **Consistency score.** C* = 100 · (1 − φ/7.2) for brands with at least 6 total mentions in the wave, not rated otherwise (v1.9's locked C_φ+FLOOR, column `C_star`). Higher C* = more consistent across models.
- **Schedule.**

| Stage | Predictors (wave, date) | W_prior ends | W_base ends | W_end ends |
|---|---|---|---|---|
| 1 | P, C*, π̂ at t₂ (legacy panel, collected by 2026-06-10) | Sat 2026-02-07 | Sat 2026-06-06 | Sat 2026-11-07 |
| 2 | P, C* at t₃ (legacy panel, 2026-11-09); P_new at t₄ (N3, from 2026-11-11) | — | Sat 2026-11-07 | Sat 2027-03-06 |

  W_base ends on the last Saturday before the predictors' wave began. Before the lock this is checked against the t₂ collection records (v0.34); if a substrate's t₂ calls began before 2026-06-07, that substrate's W_base ends on the last Saturday before its first call (logged in §8).
- **ρ_pw|Z (pooled within-substrate partial Spearman).** Within each substrate, Y, X and each control in Z are ranked (average ranks for ties); the rank of Y and the rank of X are each regressed by ordinary least squares on an intercept and the control ranks; the residuals are pooled over substrates; ρ_pw|Z is Pearson's r of the pooled residuals. With no control it is the v0.41 `pooled_within_rho`.
- **Permutation p.** One-sided (positive). Within each substrate the residuals of X are shuffled and ρ is recomputed from them; 10,000 draws; p = (1 + #{ρ_perm ≥ ρ_obs − 10⁻¹²}) ÷ 10,001. The two-sided p (on |ρ|) is reported alongside.
- **Bootstrap.** Units resampled with replacement within substrate; ranks, residuals and ρ recomputed on every resample; 10,000 resamples; percentile 90% and 95% intervals.
- **Seeds.** 430041 to 430048 for the tests in the order of §2.2 to §2.5; 430049 for the manipulation checks; 430050 for the descriptives.
- **α.** 0.05 per test, no multiplicity correction; every test is reported.
- **Minimum n.** A test with fewer than 60 units with a defined outcome (30 for the Consistency tests) is UNDETERMINED.
- **Verdict rule (every test of §2.2 to §2.6).** CONFIRMED if ρ_pw|Z ≥ 0.15 and p < 0.05 · FALSIFIED if the upper end of the 90% bootstrap interval is below 0.10 · MARGINAL if ρ_pw|Z > 0 and p < 0.10, and neither of the above · UNDETERMINED otherwise. A test whose ρ is negative with two-sided p < 0.05 also carries the label REVERSED (support for the lag account, §1); the label adds to the verdict and changes none.
- **Why these thresholds.** A brand's search level is mostly stable from month to month, so a score that predicts its change explains a small part of a small variance; partial correlations of 0.1 to 0.3 are what a useful leading indicator would show. The rule therefore asks for a positive association that clears 0.15 with p < 0.05, and calls a hypothesis falsified only when the data exclude even 0.10. With about 105 units in five strata a test has about 80% power for ρ = 0.25 and about 40% for ρ = 0.15: a true effect near 0.15 may well come out MARGINAL or UNDETERMINED, and the paper will say so.

### §2.2 PRIMARY (Stage 1): `H_Pred_Presence` — June Presence predicts the change in search interest to November

**Statement.** Among brands of the same category and the same June search level, those with a higher AIAS Presence score in June 2026 gained more US search interest by November 2026.

**Operationalisation.** X = P at t₂; Y = the change from W(2026-06-06) to W(2026-11-07); Z = {L at W(2026-06-06)}; all units with a defined Y.

**Test.** ρ_pw|Z; permutation p (seed 430041); bootstrap intervals.

**Why the control.** Presence and current search level are correlated (v0.25), and brands with high search levels tend to fall back (regression to the mean); without the control a negative association could be regression alone. With it, the question is whether AI availability says something beyond what search already shows.

### §2.3 SECONDARY (Stage 1)

- **`H_Pred_Presence_SA`** — the same test with Y^SA (one year earlier: W(2025-06-07) → W(2025-11-08)); units with both years defined; seed 430042. Categories differ in seasonality, and within-substrate ranks remove only the category-wide part; comparing a brand with its own previous year also removes its own seasonal pattern (a gift brand that rises into November every year).
- **`H_Pred_Presence_Momentum`** — Z = {L, M} with W_prior = W(2026-02-07); seed 430043. The lag account says AI presence beyond search level marks brands already in decline; controlling the February-to-June change asks whether Presence adds anything beyond the trend search had already shown.
- **`H_Pred_Consistency`** — X = C* at t₂ (rated units only); Z = {L, P at t₂}; seed 430044. Among rated brands, those named more consistently across models gained more, at equal Presence and June search level. AIAS 2.0 reports Consistency as a separate score; its worth as a second score depends on carrying information that Presence does not.

### §2.4 PRIMARY (Stage 2): `H_Pred_Presence_Confirm` — November Presence predicts the change to March 2027

**Operationalisation.** X = P at t₃; Y = the change from W(2026-11-07) to W(2027-03-06); Z = {L at W(2026-11-07)}; seed 430045. The same test on the same instrument (the legacy panel), forward in time, on outcome weeks that had not happened when it was locked. Stage 1 is retrospective evidence; Stage 2 is the confirmatory test, and a predictive-validity claim for Presence in validated AIAS 6.0 rests on it.

### §2.5 SECONDARY (Stage 2)

- **`H_Pred_Presence_Confirm_SA`** — Y^SA (one year earlier: W(2025-11-08) → W(2026-03-07)); seed 430046.
- **`H_Pred_Presence_NewPanel`** — X = P_new at t₄ (N3, S0); seed 430047. The programme's scores now come from current models; this asks whether the relation carries over to them.
- **`H_Pred_Consistency_Confirm`** — X = C* at t₃ (rated units); Z = {L, P at t₃}; seed 430048.

### §2.6 The four new components (Stage 2, by amendment)

Ranking, Sentiment, Coverage and Grounding scores at t₄ do not exist yet. Each component's predictive hypothesis is added to Stage 2 by a dated amendment to this pre-registration, deposited on OSF before the first Stage 2 outcome pull (§4.5), with this section's outcome, windows, statistic and verdict rule unchanged and Z = {L, P_new}. A component that failed its Paper A separability gate is not added.

### §2.7 Manipulation checks (each stage, with its own predictors and windows; seed 430049)

- **MC_Concurrent.** ρ_pw(P, L at W_base) ≥ 0.30 with p < 0.05: the same-time link of v0.25, in five other categories. If it fails, every predictive verdict of that stage carries the flag "criterion doubtful".
- **MC_PullReliability.** The mean, over the three pairs of pulls, of the pooled within-substrate Spearman correlation of per-pull Y ≥ 0.70. Below it, verdicts carry the flag "outcome unreliable".
- **MC_Weekly.** Every request returns weekly points (Sunday starts) covering its declared range, with no partial point inside a window; otherwise it is re-sent (§4.4).
- **MC_Terms.** The share of units searched by topic (§3.2), reported; below 50% the verdicts carry the flag "mostly plain search terms".
- **MC_Chain.** Per pull, the number of chain links that hold (§5.2), reported.

### §2.8 Pre-registered descriptives and exploratory analyses (no verdicts)

1. Every test per substrate.
2. Every Presence test without the five defunct automotive brands (registry cell D: Mercury, Oldsmobile, Plymouth, Pontiac, Saturn).
3. Recall alone: X = π̂ in place of P.
4. Units searched by topic only (§3.2).
5. A longer lead: X = P at t₁ (May 2026), with the Y of `H_Pred_Presence`.
6. Cross-lagged comparison (exploratory): AI → search, ρ_pw(P at t₂, L at W(2026-11-07) | L at W(2026-06-06)), against search → AI, ρ_pw(L at W(2026-06-06), P at t₃ | P at t₂), with a bootstrap interval for their difference (seed 430050).
7. The monthly series (§4.5): each unit's weekly chained index, shown descriptively.

---

## §3 Brand registries and search terms

### §3.1 Frozen inputs

Copies of every input, each with its source branch, path, commit and SHA-256 in `osf/v43/registries/INPUTS_MANIFEST_v0_43.json`: the v1.9 unit table (P, C*, mentions per brand and wave), the v0.41 three-wave table (π̂, φ, cells), and the v0.23 registry names. `osf/v43/registries/units_v0_43.csv` lists the 112 units with substrate, unit label, search name, registry cell and the predictors available at the lock (P, C* and π̂ at t₁, t₂ and t₃). Before the lock a parity check confirms that its values equal the frozen sources exactly. v0.42's t₄ values enter only after v0.42 is scored, read from its locked scoring outputs.

### §3.2 Search-term rule (a non-acquisition step: it returns entity suggestions, never interest values)

For each distinct search name, one SerpAPI `google_trends_autocomplete` request with that name. The term is the first returned suggestion, in returned order, that meets both conditions:

(a) its title, normalised (lower case, accents removed, "&" → "and", everything but letters and digits removed), begins with the normalised search name; and

(b) its type contains, at the start of a word, one of the substrate's words. All substrates: company, brand, corporation, manufacturer, business. Headphones: audio, headphone, electronics, loudspeaker. Skincare and cosmetics: cosmetic, beauty, skin, makeup, personal care, fragrance, perfume. Automotive: auto, car, vehicle, motor. Spirits: whisk, bourbon, scotch, cognac, brandy, tequila, mezcal, gin, rum, vodka, liqueur, liquor, spirit, distill, beverage, drink.

The term is that suggestion's topic ID. If no suggestion meets both, the term is the search name itself, as a plain search term. There is no manual correction. Every suggestion list and the chosen terms are committed before the first interest request.

### §3.3 Panels not included

The B2B software panel of v0.24/v0.25 and the technology panel of v0.28 also have scores from May–June 2026. They are not part of v0.43: each would first need its own conflict-of-interest screen. Either can be added by its own pre-registration.

---

## §4 Requests and collection

### §4.1 Requests

Each request: SerpAPI `google_trends`, `data_type=TIMESERIES`, `geo=US`, all categories, web search, `tz=0`, `date` = the request's fixed range, up to five terms.

### §4.2 Sizing pull (day 1, after the term rule; one pull, 28 requests)

Range 2025-09-07 → 2026-06-06 (39 weeks). In each substrate, units in alphabetical order of search name; the first request holds the first five; each next request holds the previous request's largest unit (by its sum over the range) and the next four. Values are chained through the shared units (§5.2), and a unit's size is its chained mean weekly index over W(2026-06-06). No week after 2026-06-06 is requested, so no outcome week is seen before the bundles are fixed.

### §4.3 Main pulls (days 2, 3 and 4, at least 24 hours apart; 28 requests each)

In each substrate, units are sorted by size (largest first; ties alphabetical); request 1 holds units 1–5, and each next request holds the previous request's last unit and the next four (16 units → 4 requests; 24 → 6). Range 2025-05-04 → 2026-11-07 (79 weeks). The same bundles serve every later pull of this study (§4.5).

### §4.4 Re-sends and records

A request that errors, returns no timeline or fails MC_Weekly is re-sent up to twice the same day, then recorded as missing for that pull. There is no other re-request. Every response is stored raw with its parameters and UTC time (`osf/v43/data/trends_raw/`).

### §4.5 Monthly snapshots and Stage 2 pulls

On the first day of each month from 2026-12-01 to 2027-05-01, one pull of the 28 bundles, range 2025-05-04 → the last Saturday before the pull; stored, and not analysed for Stage 2. Stage 2's outcome comes from three pulls at least 24 hours apart, the first no earlier than Wednesday 2027-03-10, range 2025-05-04 → 2027-03-06, same bundles; Stage 2 statistics use these three pulls only.

### §4.6 Sales rank

Not collected. The plan also names sales rank as an outcome; its source awaits the pre-registrant's decision (v0.26 read Amazon product pages by scripted browsing, which Amazon's conditions of use prohibit). If a source is approved, it is added by a dated amendment, with its own hypotheses, before its first snapshot.

### §4.7 Budget

No model calls. SerpAPI requests: 111 term look-ups, 28 sizing and 84 main requests for Stage 1 (223); 28 per monthly snapshot; 84 for Stage 2's outcome pulls. Each month stays within SerpAPI's free plan (250 searches a month).

---

## §5 Analysis plan

### §5.1 Parsing

For each request: the weekly series of each term; MC_Weekly; the window sums S.

### §5.2 Outcome, level and chaining

- Per pull and bundle, Y, Y′ and M as defined in §2.1; for a unit in two bundles, the mean of its two values. A unit's Y is defined in a pull if S(W_base) + S(W_end) ≥ 4 in at least one of its bundles. Y_b = the mean over the pulls in which it is defined; undefined if defined in fewer than two of the three pulls. Y′ and M follow the same rule; Y^SA is defined where both Y and Y′ are.
- Chaining within a pull and substrate: f₁ = 1 and f_{j+1} = f_j · T_j ÷ T_{j+1}, where T_j and T_{j+1} are the shared unit's sums over the full range in bundles j and j + 1. If either sum is zero the link fails; later bundles then rank below every unit of the earlier ones, in their own within-bundle order. A unit's chained level = f_j × its mean weekly index over W_base in the first bundle that holds it. L_b = the mean over pulls of its within-substrate rank by chained level.
- Stage 2 applies the same rules with its own windows.

### §5.3 Computation

`score_v0_43.py`, one run per stage on the complete pulls; verdicts to `osf/v43/v43_stage1_verdicts.json` and `osf/v43/v43_stage2_verdicts.json`.

### §5.4 Checks before the lock

Unit tests on synthetic Trends responses: window sums on Sunday weeks; chaining recovers simulated volumes within rounding; a planted partial correlation is recovered; the null gives uniform p-values; the verdict rule on edge cases. Parity of the units file with the frozen inputs (P, C* and π̂ exact).

### §5.5 Missing data

No imputation. Units without a defined outcome leave that test and are counted per substrate.

### §5.6 Reporting

Every test, check and descriptive, with per-substrate breakdowns and the number of units in each test. Stage 1 goes to the predictive-validity paper (target early December 2026) and its OSF deposit; Stage 2 to validated AIAS 6.0 (spring 2027).

---

## §6 Limitations

1. Search interest is a trace of people looking for a brand, not of buying it; one search engine, one country.
2. Google Trends values are sampled and rounded. Size-matched bundles and three pulls reduce that noise; they do not remove it.
3. The term rule is mechanical: some names fall back to plain terms that also catch other meanings, and a topic can be the wrong entity of the same name. Descriptive 4 shows the topic-only result, and the full look-up record is published.
4. Brand-level search mixes categories for brands that sell in many (for example Sony), while P is measured in one category.
5. The design is correlational. A positive partial association fits AI availability leading demand, but a common cause, such as advertising or a launch that reaches both the web and search, could produce it; the cross-lagged comparison is only suggestive.
6. Stage 1's scores come from the retiring legacy panel; Stage 2's new-panel test asks whether the relation carries over.
7. Five categories of 16 to 24 brands; the strata are small.
8. The horizons differ: 22 weeks between window ends in Stage 1, 17 in Stage 2.

---

## §7 Declarations

**Conflict of interest.** The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study measures search interest for the brands of registries fixed in earlier phases (v0.19–v0.23); it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward unchanged. Two items of record apply. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands — Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) — characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry, AKG was substituted with Denon before the v0.19 pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary. Data collection and scoring are fully automated against the locked registries, and this pre-registration is locked and deposited before any search-interest request. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

**Funding.** Self-funded.

**Ethics.** Not applicable; no human subjects.

**Use of AI tools.** The author used Anthropic's Claude to assist with analysis code, drafting and editing of text, and figure production. The study design, pre-registered hypotheses and decision rules, and all interpretations are the author's; the author reviewed all content and takes full responsibility for it.

---

## §8 Lock procedure and change log

- **r1 draft** sent to the pre-registrant on 2026-11-10. It locks 24 hours after it reached him unless he objects.
- **Between sending and lock:** clarifications that change no hypothesis, threshold, window, term rule or decision rule are logged below; any other change restarts the 24 hours.
- **Lock:** write `LOCK_MANIFEST_v0_43.sha256` (this file, the frozen inputs, the units file, the acquisition and scoring scripts and their tests); commit; tag `v0.43-prereg-r1`; push branch and tag; deposit `osf/v43/prereg/`, `osf/v43/registries/` and `osf/v43/anchor/` at OSF `v43/` and verify their SHA-256 there. Only then the first request (§3.2).

**Change log**

- (none yet)
