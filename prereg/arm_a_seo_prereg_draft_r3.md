# AIAS™ — Pre-Registration, Arm A of "Does AI presence pay?": Google visibility, AI presence and sales (revision r3 DRAFT, not locked)

**Study:** For brands with public US sales or share figures, month by month, how Google organic visibility (DataForSEO Historical Rank Overview, US) relates to AIAS Presence and to those figures; whether AI presence adds anything to sales once Google visibility is known; and, from three pulls tied to the AI waves, whether a brand's AI presence and its Google visibility move together over time. Arm A of the study family "Does AI presence pay?" (S&P lessons work order v1.2, section 3; project doc `claude/runner-sp-lessons-nov22.md`), from the study idea `claude/idea-seo-sales-ai-presence-nov21.md` (v1.1).
**Design:** Re-analysis of archived and scheduled AI waves (no new AI-wave model calls in this arm; one blind domain cross-check, §3.4) joined to three paid pulls of monthly Google-visibility history for 76 domains (72 brands, 4 US-site extras) in four categories with a public sales or share measure (cars, airlines, retail banks, B2B software) plus five spirits brands with published US case volumes (§3.2). First pull in December 2026 after the lock, with monthly history back to November 2024; one re-pull after each of the next two AI waves, t₅ and t₆ (§5.2). Association only; no causal claim anywhere in the study or its paper.
**Budget:** US$50 is a ceiling for the whole study, never a target; no second top-up; spend less if less answers the question (Pablo, Mon 2026-11-23, 10:28–10:33 pm US Central). Expected $32.65 over three pulls with the recommended re-pull mode (§5.2); hard stop at $48 cumulative; price check before every pull (§5.4). Inside the programme rule of at most $100 of paid calls per paper.
**Programme position:** Study number TO CONFIRM (coordinator assigns). It moves no AIAS 6.0 date. Arm B (prospective, listed one-brand companies) is a separate pre-registration.
**Design rules:** S&P work order section 11a (outcome rates by band; the shape written in advance; pooled and within category; each brand once and weighted by size; data as it stood; stability before fit; a reversion baseline). Pablo's OK of 🔴 item (o) is TO CONFIRM; this draft follows 11a either way.
**Pre-registrant:** Pablo Ulpiano González Castro
**Status:** **r3 DRAFT, not locked.** Written Tue 2026-11-24 (morning, US Central) by a runner lane for the coordinator, from r2 (b5caf6e, committed the same morning, 7:42 am US Central), after Pablo's decision D12 (b) at 8:13 am US Central ("As you suggest"). r3 changes only `H_A2`'s scale and the sections that describe it (change table below). Not locked. Nothing has been pulled for any study domain. The only DataForSEO calls so far are the coordinator's feasibility test on two domains outside the study (§4.2). The only paid model call is the blind domain cross-check (§3.4, item 3; $0.1161).
**Lock:** D12 (b) changes `H_A2`'s statistic, so the 24-hour clock restarted with Pablo's decision of Tue 2026-11-24, 8:13 am US Central (§9): lock at the earliest Wed 2026-11-25, about 8:15 am US Central, unless he holds it (r2 said about 7:30 am). Pablo adds the $50 once, after the lock. No study domain is pulled before the lock.

---

## r3, Tue 2026-11-24: changes from r2 (D12 b)

Pablo, Tue 2026-11-24, 8:13 am US Central, on D12: "As you suggest" (option b). `H_A2`'s confirmatory test moves from within-group ranks to log shares centred within competitive group, still by Freedman–Lane; the rank test becomes a declared sensitivity analysis. Alpha, one-sided direction, Holm family, number of permutations, seed policy, the 0.30 threshold and the verdict words are unchanged. Nothing else in the design changes: pulls Mon 2026-12-07, Mon 2027-01-04 and Mon 2027-03-01; planned cost $32.65, ceiling $50; `date_from` as drafted; the 76-domain list; Declarations unchanged.

| Section | r2 (old) | r3 (new) | Reason |
|---|---|---|---|
| §2.3 `H_A2` statistic | Partial Spearman of `R` with `S` given `Gs` on within-group normalised ranks | Partial (Pearson) correlation of `r` with `s` given `gs`: natural-log shares centred within competitive group | D12 (b): FL on ranks over-rejects under simulated size-driven nulls (r2: up to 8.1% at 2.5%); FL on centred unranked values holds size (r3: 2.46–2.63% at 2.5%, 4.74–5.20% at 5%) |
| §2.3 zero handling | Not needed (ranks) | `R` = (m + 0.5)/(M + 0.5·n_g) before logs; `S`, `Gs` positive (zero etv excluded by §6.4) | Brands named in 0 of 18 answers exist (e.g. Chevrolet, named in 0 of 18 recommendation answers in Shift's counts); logs need a fixed rule before data |
| §2.3 test | Freedman–Lane on the ranks (reduced model `R` ~ `Gs`, residuals permuted within group, `R*` not re-ranked) | The same Freedman–Lane scheme on the centred log values (reduced model `r` ~ `gs`); p formula stated | Same scheme, new scale |
| §2.3 sensitivity | Per-group slopes in the reduced model | (i) the r2 rank test (FL on within-group ranks, ties at average rank), (ii) per-group slopes, (iii) zero offset 0.25 and 1; no verdict, outside Holm | D12 (b) keeps the rank version as a declared check; ties and the offset needed stating |
| §2.3 "Why" and stated limit | FL lowers but does not remove the rank excess; a CONFIRMED is reported with the limit "up to about three times nominal" | Why centred unranked values; r3 size figures; the limit sentence is dropped (it applied to the rank test, now a sensitivity) | D12 decided |
| §2.3 CONFIRMED / FALSIFIED | partial ρ ≥ 0.30 / ≤ 0 | partial r (confirmatory statistic) ≥ 0.30 / ≤ 0 | Same thresholds, new statistic |
| §2.11 power | r2 rank-FL size table and base-case power (0.171 / 0.397 at .025) | r3 size table (4 r2 scenarios + R-from-counts scenario) and power table (4 scenarios × 5 effects, log and rank); r2 figures kept as record | Re-run for the new test, seed 20261124, `prereg/armA_power_sim_r3.py` |
| §6.2 (1), §7 | Common shifts do not change ranks; sales measures used as ranks | Also: they do not change within-group shares or their logs; `H_A2` uses log shares (zero rule, offsets as sensitivity) | Consistency with the new scale |
| Header, §9, §10 | r2 draft; lock earliest Wed 2026-11-25 ~7:30 am; D12 open | r3 DRAFT, not locked; lock earliest Wed 2026-11-25 ~8:15 am (24 h from 8:13 am); D12 decided (b); file `..._r3.md` | §9: a change to a hypothesis's test restarts the 24 hours |

---

## r2, Tue 2026-11-24: changes from r1

1. **`H_A2` test (Pablo, 7:29 am US Central, "ok Freedman–Lane").** The permutation test changes from permuting `R` within competitive group to Freedman–Lane (§2.3). Alpha, one-sided direction, number of permutations, seed policy, statistic and thresholds are unchanged. The power simulation was re-run with the FL version (§2.11): FL reduces the size excess but does not remove it on within-group ranks; the excess is traced to the rank scale (open decision D12).
2. **Blind domain cross-check run (Pablo, 7:29 am, "go arm A cross-check").** gpt-6-astra (OpenAI), given brand name, category and country only: 72 of 72 brands agree with our list (71 exact, 1 same site), $0.1161 (§3.4, item 3).
3. **The 8 TO CONFIRM domains resolved** (§3.3): all kept; the 4 US-site extras (mbusa.com, bmwusa.com, jaguarusa.com, marcus.com) are confirmed and become primary for their brands (D9), the R1 global domain the sensitivity; td.com, bmo.com, firstcitizens.com confirmed; hsbc.com stays the pulled target, us.hsbc.com (the model's answer, same site) is recorded but not pulled (§3.3). Domain count unchanged: **76**; costs unchanged (§5.2).
4. **Lock line** updated (above): earliest Wed 2026-11-25, about 7:30 am US Central. `date_from` and the pull calendar (pull 2 Mon 2027-01-04) unchanged.

---

## Changes from r0 (made in r1)

1. **Sample (replaces r0 D2).** r0's 276 domains in 12 categories are dropped for 72 brands with a public sales or share figure: cars 18, airlines 11, retail banks 26, B2B software 12 (listed companies only), spirits 5 (the five with published US case volumes), plus 4 US-site extras (§3.2). The ~200 brands without sales data (headphones, skincare, cosmetics, the other 19 spirits, project-management software, finance apps, kitchen knives, running shoes, and the categories r0 already left out) are not pulled; a broader snapshot comes only later and only on Pablo's go. Fisker leaves the car list (no 2025 sales). Seven B2B software brands without public revenue filings leave (Notion, Airtable, Linear, Zendesk, Slack, Miro, Stripe).
2. **Pulls and budget (replaces r0 §5.2 and D4).** Three pulls (December 2026; January 2027 after t₅; March 2027 after t₆) instead of one large pull and one small re-pull. Expected $32.65 instead of $45.39. The $50 is a ceiling, not a target (Pablo's 10:28–10:33 pm decision replaces his 10:02 pm "use $50").
3. **Hypotheses.** `H_A1` pools four categories (was up to 11) and is UNDETERMINED below 3 analysable categories (was 4). `H_A4` and `H_A5` are cars only (the other omnibus categories are no longer pulled). `H_A6` covers airlines, banks and B2B software; spirits become descriptive only (n = 5). New SECONDARY `H_A7`: within-brand co-movement of Presence and Google visibility over t₄ → t₆, made possible by the re-pulls (§2.8).
4. **Power** stated as approximations for `H_A1` and `H_A2` (§2.11); the simulation stays a pre-lock task.
5. **Domain list** given in full with sources (§3.3); 8 of 76 domains marked TO CONFIRM.
6. **Pull calendar** tied to the wave dates (§5.2); t₇ is not dated in the roadmap, so no pull is planned for it.
7. **Blind model cross-check of domains** stays a pre-lock task with a cost estimate; no paid model call was made for r1 (§3.4).
8. **Declarations:** the headphones registry is not used in this arm, so the Denon clause keeps the CLAUDE.md fact but drops "it is kept and every result is also reported without it" (not applicable); §6.5 drops Denon and Eucerin from S-COI. AI-use statement unchanged.

---

## §1 Context

- The book's opening scene (tracker numbers up, sales flat, Google category queries down because people ask a chatbot) is a picture; no study of ours puts the three measures side by side for the same brands (idea doc, "Why").
- What exists: v0.25 (Presence and Google Trends search interest, rho 0.74, n 24, B2B software; Trends measures demand, not SEO); v0.26 (Presence and Amazon sales rank, rho about 0, n 88); v0.43 (June Presence against later change in search interest); AIAS Shift (AI recommendation share against 2025 US car sales by competitive group, `claude/shift-public-numbers-nov19.md`); #76 "From named to chosen". Gap: no real SEO measure in any study (idea doc, "What exists").
- Decided by Pablo on Mon 2026-11-23: measured over time, not as one snapshot ("Yes over time yes?", 8:06 am); source DataForSEO pay as you go ("Ok yes", 8:16 am); cars first, then airlines and banks. At 10:28–10:33 pm: $50 is a ceiling for the whole study, spread over its length; only brands with public sales or share data, about 80 domains in cars, airlines, banks and B2B software (spirits with published US case volumes may join), pulled three times; design approved ("Ok").

## §2 Pre-registered hypotheses

### §2.1 Definitions (used by every test)

- **Google visibility, primary measure `G`:** `metrics.organic.etv` (estimated organic traffic volume) for the brand's domain, per month, US (location_code 2840), English. Analysed as `g = ln(1 + etv)`.
- **Secondary Google measures:** `metrics.organic.count` (ranked keywords) and top-10 keywords `pos_1 + pos_2_3 + pos_4_10`, each as `ln(1 + x)`. `clickstream_etv` is a robustness measure only if it is non-null for at least 80% of domain-months (§6.3).
- **Window:** the mean of `g` over the three complete months ending with the month of the AI wave (e.g. a May 2026 wave uses Mar, Apr and May 2026). Robustness: the wave month alone, and the month before it.
- **Complete month:** any month before the pull month. The pull month is always excluded (the 2026-11-23 test returned a partial November 2026).
- **Vintage:** the pull a value comes from. Each test uses values from one vintage only (§6.1): cross-sectional tests at t₁–t₄ use pull 1; `H_A7` uses pull 3, which carries the full history (§5.2).
- **AIAS Presence `P`:** recall Presence π̂ as each source study's locked scorer computes it (omnibus: v1.8 protocol in the v0.41 scorer `osf/v41/scripts/score_v41.py`, and v0.42's scorer for t₄; t₅ and t₆ with their own locked scorers). For airlines, banks and B2B software, the study's own published per-brand Presence (file per category TO CONFIRM, §3.4, item 4).
- **AI recommendation share `R` (cars):** Shift's share of first-round mentions on the three recommendation questions (18 answers per brand at t₁), within the brand's competitive group (`claude/shift-public-numbers-nov19.md`; counts from the site's deposited `content/explorers.json`).
- **Sales share `S` (cars):** the brand's 2025 US units × average transaction price, as a share of its competitive group (Shift's figures and sources, same doc). Groups: luxury (7), mass market (7), electric-only (4) = 18 brands still sold.
- **Google share `Gs` (cars):** the brand's summed etv over Jan–Dec 2025, as a share of its competitive group.
- **Category-month demeaning:** for change analyses, each brand's Δg is taken minus the median Δg of its category over the same months (a category-month fixed effect), so a change common to all domains (an index or method break) drops out.
- **Each brand once:** no brand of the sample is in two of its categories; each domain is pulled once per pull.
- **Pooling:** within-category Spearman ρ_c, pooled as the Fisher-z mean weighted by n_c − 3, over categories with n_c ≥ 8 analysable brands. Every pooled figure is shown beside every within-category figure (11a.3).
- **Seeds:** permutation and bootstrap seeds are fixed at lock (proposed 610001 onward; TO CONFIRM that no other study uses them). 10,000 permutations; 10,000 bootstrap resamples within category.

### §2.2 PRIMARY 1: `H_A1_Google_AI` — brands with more Google visibility have more AI presence (cars, airlines, banks, B2B software)

- **Prediction:** within category, `P` at the category's AI wave rises with the window mean of `g` at that wave.
- **Statistic:** pooled ρ̄ (§2.1) over the analysable categories among the four; one-sided permutation test (P permuted within category); 95% bootstrap CI. Spirits (n = 5) are shown, not pooled.
- **CONFIRMED:** ρ̄ ≥ 0.30 and Holm-adjusted p < 0.05. **FALSIFIED:** the CI's upper bound < 0.30. **MARGINAL:** p < 0.05 but ρ̄ < 0.30. **UNDETERMINED:** otherwise, or fewer than 3 analysable categories.
- **Also reported (no separate verdict):** each ρ_c; the same test on `count` and top-10 keywords; size-weighted version (§2.7).

### §2.3 PRIMARY 2: `H_A2_AI_adds_to_Google` — AI recommendation share tracks 2025 sales once Google share is known (cars)

- **Prediction:** within competitive group, `R` (t₁) is positively associated with `S` after controlling for `Gs`.
- **Variables (r3, D12 b):** `r`, `s` and `gs` are the natural logs of `R`, `S` and `Gs`, each centred within competitive group: the brand's log share minus the mean log share of its group (equivalently, the log of its share over the group's geometric-mean share; the same as the log of the raw count, sales or etv centred within group). **Zero rule for `R`, fixed before data:** `R` = (m + 0.5) / (M + 0.5·n_g), where m is the brand's first-round mentions on the three recommendation questions, M the group's total and n_g the group's size, so a brand named in none of its 18 answers has a finite log share. `S` and `Gs` are used as defined in §2.1 (positive for every analysable brand; a brand with zero or missing 2025 etv is excluded under §6.4).
- **Statistic (confirmatory):** the partial (Pearson) correlation of `r` with `s` given `gs`, n = 18 brands still sold. **Test:** one-sided permutation test by Freedman–Lane: fit the reduced model `r` ~ `gs` by least squares (one intercept and one slope: the model the partial correlation conditions on; `H_A2` has no other covariate, and the group means of centred values are 0 by construction); permute the reduced model's residuals within competitive group; add them back to its fitted values to give `r*`; recompute the same partial correlation of `r*` with `s` given `gs`; p = (1 + number of permuted partials ≥ the observed) / (1 + 10,000); 10,000 permutations, seed as §2.1.
- **Declared sensitivity analyses (no verdict; outside the Holm family; shown beside the confirmatory result wherever it is shown):** (i) **the r2 rank version:** the partial Spearman correlation of `R` with `S` given `Gs` on within-group normalised ranks ((rank − 1)/(n_g − 1), ties at the average rank), tested by the same Freedman–Lane scheme (reduced model on the ranks, `R*` not re-ranked); its simulated size is above nominal when brand size drives all three measures (§2.11), so it cannot confirm or falsify; (ii) the confirmatory test with an intercept and slope per group in the reduced model; (iii) the zero offset 0.5 replaced by 0.25 and by 1. If the confirmatory result and a sensitivity result point different ways, both are reported and the confirmatory result decides the verdict.
- **Why centred, unranked values (D12 b):** r1's simulation found that permuting `R` within group rejects too often under the null; r2 moved to Freedman–Lane, which lowered but did not remove the excess on within-group ranks, and traced the remainder to the rank scale (ranks of `Gs` within groups of 7, 7 and 4 do not remove its linear effect). r3's re-run (§2.11, seed 20261124) shows the r3 test holding size in every simulated scenario: 2.46–2.63% at nominal 2.5% and 4.74–5.20% at 5% (the rank version 2.80–7.86% and 5.60–13.27%), and also when `R` is built from small mention counts with zeros and the 0.5 rule (2.28–2.61% and 4.55–5.11%). Logs are used because shares are skewed; the simulation treats its normal values as logs of the raw quantities (log-normal raw values), so it covers skew of that kind but not other shapes.
- **CONFIRMED:** partial r ≥ 0.30 (confirmatory statistic) and Holm-adjusted p < 0.05. **FALSIFIED:** partial r ≤ 0. **UNDETERMINED:** otherwise.
- **Power:** low (§2.11). A null is reported as a null, not as absence of a link.
- **Headline pair (S&P format, §3 of the work order):** of the brands whose AI share exceeds their Google share within group, the share whose sales share exceeds their Google share, against the same share for the other brands, with its source line. Whatever the result.

### §2.4 SECONDARY 1: `H_A3_which_tracks_sales` — Google share and AI share against sales (cars)

- ρ(Gs, S) and ρ(R, S) on within-group ranks, and their difference with a 95% bootstrap CI (resampling brands within group). **Verdict rule:** "Google tracks sales better" or "AI tracks sales better" only if the CI of the difference excludes 0; otherwise "no difference detected".

### §2.5 SECONDARY 2: `H_A4_bands` — Google change by Presence band, with a reversion baseline (cars; 11a.1, 11a.2, 11a.7)

- **Groups:** Presence terciles at t₁ (2026-05-25) among the 18 car brands (6 per band), named bottom, middle, top. A brand keeps its t₁ band for the whole holding period; no brand enters or leaves during it.
- **Lookback and holding period:** baseline window Mar–May 2026 (t₁); outcome window Sep–Nov 2026 (the last three complete months at pull 1). **Outcome:** category-month-demeaned Δg between the two windows, demeaned over the 18 car domains.
- **Shape written in advance:** mean outcome bottom < middle < top. **Statistics:** Jonckheere–Terpstra test for an ordered rise (one-sided, permutation); top-minus-bottom spread with 95% bootstrap CI; hit rate = share of top-band brands whose outcome exceeds the car median.
- **Reversion baseline:** (a) the same spread when brands are banded by their own pre-period Google level (mean g, Nov 2024–Feb 2026) instead of Presence: what level and reversion alone give; (b) a placebo on the past: t₁ Presence bands against Δg from Nov 2024–Jan 2025 to Mar–May 2026, which t₁ Presence cannot have caused.
- **SUPPORTED:** ordered rise with Holm-adjusted p < 0.05, spread CI above 0, and the Presence-band spread larger than baseline (a)'s, with the bootstrap CI of the difference above 0. **PARTIAL:** the rise is significant but the best band is not the top one, or the spread does not beat baseline (a) (never CONFIRMED in either case). **NOT SUPPORTED:** otherwise. A placebo (b) spread with its CI above 0 is reported as a sign of a standing trend, and the forward result is then labelled "not distinguishable from trend".
- Stated limit: 6 brands per band; power is low.

### §2.6 SECONDARY 3: `H_A5_co_movement_legacy` — within-brand change on the legacy panel (cars, t₁ → t₃)

- Spearman between ΔP (t₃ 2026-11-09 minus t₁, same six-model panel) and category-month-demeaned Δg (Sep–Nov 2026 window minus Mar–May 2026 window, pull 1), n = 18. **SUPPORTED:** ρ > 0 with Holm-adjusted p < 0.05; otherwise NOT SUPPORTED. Stated limit: Presence held at ρ 0.93–0.98 from t₂ to t₃ (v0.42 pre-registration §1), so ΔP has little spread and power is low.

### §2.7 Size weighting (11a.4, applies to §2.2–§2.9)

- The primary result is equal-weighted (each brand once). Also reported: weighted by the brand's sales measure (cars: 2025 sales; airlines: passengers; banks: deposits; software: revenue; §3.3), otherwise by the brand's pre-period mean etv. Both are shown; the equal-weighted figure decides the verdict.

### §2.8 SECONDARY 4 (new in r1): `H_A7_co_movement_current` — within-brand change on the current panel over the three pulls (cars)

- **Why it is added, and why it is defensible:** the re-pulls exist to follow brands over time. Within-brand change removes brand size, the confound that limits `H_A1`. t₄ (v0.42, 2026-11-11 to 11-14), t₅ (v0.45, planned 2026-12-03 to 12-06) and t₆ (planned about 2027-02-12) are on one panel (t₄'s three models; t₆'s panel TO CONFIRM), so ΔP is not a panel change. It is defensible only as a SECONDARY test with low power (n = 18, three months), never as evidence that AI presence pays.
- **Statistic:** Spearman between ΔP (t₆ minus t₄) and category-month-demeaned Δg (Dec 2026–Feb 2027 window minus Sep–Nov 2026 window), both g windows from pull 3 (one vintage). One-sided permutation test. **SUPPORTED:** ρ > 0 with Holm-adjusted p < 0.05; otherwise NOT SUPPORTED.
- **Conditions:** if t₆ does not use t₄'s panel, or t₆ is not collected by 2027-03-31, `H_A7` is UNDETERMINED and the same analysis on t₄ → t₅ (windows Sep–Nov vs Oct–Dec 2026, pull 2 overlap and pull 3) is reported as exploratory.
- **Also reported (exploratory):** the three-point path (t₄, t₅, t₆) per brand; the same test in spirits (n = 5, descriptive) if t₄–t₆ cover them.

### §2.9 SECONDARY 5: `H_A6_other_sales` — the same tests in the other sales-link categories

- Airlines (US), retail banks (US), B2B software: ρ(g, sales measure), ρ(P, sales measure) and the partial of P given g, within category. Confirmatory only for categories whose sales measure, year and source file are fixed in this document before lock (§3.3; airline passengers from US DOT/BTS, bank deposits from the FDIC, revenue from SEC filings). A category without a fixed source at lock moves to the exploratory list. SUPPORTED per category: partial ρ > 0 with Holm-adjusted p < 0.05.
- Spirits (5 brands, US 9-liter cases from the published sources in §3.3, years 2024 and 2025 mixed): the three correlations are shown as description only; no verdict.

### §2.10 Multiple testing

- **Primary family** (`H_A1`, `H_A2`): Holm, family-wise α = 0.05.
- **Secondary family** (`H_A3` difference test, `H_A4` ordered-rise test, `H_A5`, `H_A7`, each confirmatory category of `H_A6`): Holm, α = 0.05, separately from the primary family.
- Robustness, sensitivity and exploratory analyses carry no verdict and no adjustment, and are labelled as such wherever shown.

### §2.11 Power (approximations from r1; simulation results from r1–r3)

- **Simulation (r1 pre-lock, re-run in r2 and r3):** `prereg/armA_power_sim.py`, seed 20261124 (outside the proposed 610001+ range); r1 output `armA_power_sim_out.txt`, r2 output `armA_power_sim_out_r2.txt` (the r1 rows reproduce exactly), diagnostic `armA_power_sim_fl_diag.py` / `armA_power_sim_fl_diag_out.txt`; **r3: `prereg/armA_power_sim_r3.py`, output `prereg/armA_power_sim_out_r3.txt`** (seed 20261124, its own run; 20,000 null replicates per scenario, 4,000 power replicates per cell, 2,000 permutations each; run 2026-11-24, 215 s). Assumptions in the script headers (latent normal, no ties, equal effect in every category, all brands analysable; for `H_A2` corr(Gs, S) / corr(R, Gs) 0.6/0.5 base, 0.3/0.3 weak, 0.8/0.7 strong, 0.9/0.85 very strong; r3 reads the latent normal values as the logs of the raw quantities, so log shares centred within group are the latent values centred within group). `H_A1`: P(CONFIRMED) 0.504 at true ρ 0.30, 0.807 at 0.40, 0.961 at 0.50; size 0.024 at .025 and 0.048 at .05.
- **r3: `H_A2` size under the null** (20,000 replicates per scenario; within each replicate the same data and permutation indices for every test; Monte Carlo SE about 0.0011 at .025 and 0.0015 at .05):

| Null scenario (corr Gs–S / R–Gs) | **r3 confirmatory: FL, centred log values**, at .025 / .05 | FL, centred log, per-group slopes (sens. ii), at .025 / .05 | FL, within-group ranks (r2 test; sens. i), at .025 / .05 | Mean partial: log / rank |
|---|---|---|---|---|
| base (0.6 / 0.5) | **0.0263 / 0.0519** | 0.0262 / 0.0510 | 0.0360 / 0.0667 | −0.002 / 0.038 |
| weak size link (0.3 / 0.3) | **0.0249 / 0.0520** | 0.0246 / 0.0505 | 0.0280 / 0.0560 | −0.002 / 0.010 |
| strong size link (0.8 / 0.7) | **0.0262 / 0.0516** | 0.0248 / 0.0528 | 0.0551 / 0.0941 | −0.000 / 0.082 |
| size drives all three, very strong (0.9 / 0.85) | **0.0246 / 0.0474** | 0.0232 / 0.0501 | 0.0786 / 0.1327 | −0.000 / 0.123 |
| *R from mention counts (Poisson, mean 4 per brand, about 3.2 of 18 brands at 0; 0.5 rule):* base | **0.0228 / 0.0455** | 0.0219 / 0.0450 | 0.0329 / 0.0647 | −0.001 / 0.033 |
| counts: weak size link | **0.0253 / 0.0505** | 0.0247 / 0.0503 | 0.0283 / 0.0549 | 0.002 / 0.012 |
| counts: strong size link | **0.0261 / 0.0511** | 0.0255 / 0.0510 | 0.0464 / 0.0838 | −0.001 / 0.060 |
| counts: size drives all three, very strong | **0.0249 / 0.0507** | 0.0250 / 0.0510 | 0.0587 / 0.1038 | 0.001 / 0.090 |

The r3 test holds size within Monte Carlo error in every scenario (the counts base case is slightly conservative at .05). For the r3 test, P(CONFIRMED) under the null equals the rejection rate (to within 0.0001 in every cell, `armA_power_sim_out_r3.txt`), because at n = 18 a one-sided p below .05 already needs a partial above 0.30; the power table below therefore gives P(CONFIRMED). The rank version's partial is undefined in 2 and 35 of 20,000 replicates (strong, very strong) and 3 and 33 (counts: strong, very strong), counted as no rejection; the log version is never undefined. In the counts scenario the simulation breaks ties in ranks arbitrarily, whereas the analysis uses average ranks (sens. i only).

- **r3: `H_A2` power** (4,000 replicates per cell; true effect as in r1/r2: ρ_p, a latent Pearson partial of 2 sin(πρ_p/6)); P(CONFIRMED) at Holm's first step .025 / at .05:

| Scenario | Test | ρ_p 0.10 | 0.20 | 0.30 | 0.40 | 0.50 |
|---|---|---|---|---|---|---|
| base | **r3: FL, centred log** | 0.057 / 0.104 | 0.104 / 0.177 | **0.201 / 0.310** | 0.344 / 0.476 | **0.524 / 0.653** |
| base | r2 test: FL, ranks | 0.066 / 0.120 | 0.105 / 0.175 | 0.186 / 0.276 | 0.265 / 0.385 | 0.400 / 0.532 |
| weak size link | **r3: FL, centred log** | 0.057 / 0.100 | 0.112 / 0.185 | **0.196 / 0.307** | 0.325 / 0.464 | **0.507 / 0.651** |
| weak size link | r2 test: FL, ranks | 0.058 / 0.102 | 0.102 / 0.164 | 0.156 / 0.251 | 0.254 / 0.369 | 0.373 / 0.502 |
| strong size link | **r3: FL, centred log** | 0.054 / 0.107 | 0.105 / 0.180 | **0.201 / 0.314** | 0.330 / 0.473 | **0.516 / 0.651** |
| strong size link | r2 test: FL, ranks | 0.091 / 0.146 | 0.136 / 0.214 | 0.199 / 0.295 | 0.293 / 0.401 | 0.405 / 0.525 |
| size drives all three, very strong | **r3: FL, centred log** | 0.053 / 0.096 | 0.120 / 0.194 | **0.204 / 0.307** | 0.333 / 0.472 | **0.506 / 0.641** |
| size drives all three, very strong | r2 test: FL, ranks | 0.120 / 0.182 | 0.181 / 0.263 | 0.227 / 0.324 | 0.322 / 0.419 | 0.409 / 0.525 |

So the r3 test has about 0.20 power at a true partial of 0.30 and about 0.51–0.52 at 0.50 (Holm's first step), the same in every size-link scenario, close to r1's normal approximation (0.21 and 0.54). Part of the rank version's apparent power at small effects under strong size links is its size excess. Power stays low; a null is reported as a null (§2.3).

- **Record from r2 (superseded by the r3 tables above): `H_A2` size under the null with the r2 rank test** (20,000 replicates per scenario, 2,000 permutations each, the same data and permutation indices for every test):

| Null scenario (corr Gs–S / R–Gs) | r1 within-group permutation, at .025 / .05 | Freedman–Lane, at .025 / .05 | FL, per-group slopes, at .025 / .05 | Mean partial ρ (rank scale) |
|---|---|---|---|---|
| base (0.6 / 0.5) | 0.0400 / 0.0738 | 0.0360 / 0.0684 | 0.0351 / 0.0707 | 0.040 |
| weak size link (0.3 / 0.3) | 0.0267 / 0.0547 | 0.0255 / 0.0541 | 0.0262 / 0.0549 | 0.013 |
| strong size link (0.8 / 0.7) | 0.0687 / 0.1070 | 0.0561 / 0.0945 | 0.0527 / 0.0938 | 0.083 |
| size drives all three, very strong (0.9 / 0.85) | 0.1027 / 0.1502 | 0.0810 / 0.1335 | 0.0799 / 0.1305 | 0.121 |

Monte Carlo SE about 0.0011 at .025 and 0.0015 at .05. In the very strong scenario 31 of 20,000 replicates had an undefined partial (ranks of `R` or `S` identical to those of `Gs`); they count as no rejection.

- r2 diagnostic (record; 10,000 replicates): FL on within-group ranks 0.028–0.087 at .025 and 0.054–0.140 at .05; FL on the simulated values centred within group (no ranks) 0.024–0.028 and 0.051–0.053 in all four scenarios, mean partial −0.004 to 0.001. The size excess comes from the rank scale (ranks of `Gs` within groups of 7, 7 and 4 do not remove its linear effect, so the rank partial is above 0 when the true partial is 0), not from the permutation scheme (D12).
- r2 record, **`H_A2` power with FL on ranks (4,000 replicates, base case; superseded by the r3 power table):** P(CONFIRMED at Holm's first step .025) 0.171 at true partial 0.30, 0.397 at 0.50; at .05: 0.264 and 0.527. (r1's within-group test: 0.187 and 0.411 at .025, part of it from the size excess.)

**r1's approximations (kept for the record):**

- **`H_A1`:** with n_c ≈ 18, 11, 26, 12 (if every brand is analysable), Σ(n_c − 3) = 55, so the pooled Fisher-z has SE ≈ 1/√55 = 0.135. At true ρ = 0.30 (z = 0.310): z/SE ≈ 2.29, power to reach p < 0.025 (Holm's first step) ≈ Φ(2.29 − 1.96) ≈ 0.63, but the CONFIRMED rule also needs ρ̄ ≥ 0.30, which holds about half the time at a true 0.30, so P(CONFIRMED) ≈ 0.5. At true ρ = 0.50 (z = 0.549): z/SE ≈ 4.07, power ≈ 0.99, P(ρ̄ ≥ 0.30) ≈ 0.95. Normal approximation for Pearson; Spearman's variance is somewhat larger, so these are upper bounds.
- **`H_A2`:** n = 18 with one control, SE ≈ 1/√(18 − 4) = 0.267. At true partial ρ = 0.30: z/SE ≈ 1.16, power ≈ Φ(1.16 − 1.96) ≈ 0.21. At 0.50: ≈ 2.06, power ≈ 0.54. The within-group permutation test may differ; the simulation (light job, no API) replaces these figures before lock (done: r3 tables above).
- **`H_A5`, `H_A7`:** n = 18; at true ρ = 0.30 power ≈ Φ(0.310·√15 − 1.96) ≈ 0.22 at Holm's strictest step. Reported as low-power tests.
- **What repeat pulls buy:** they do not raise n; they make `H_A7` possible and give two restatement checks (§6.1).

### §2.12 Exploratory (labelled, no verdicts)

- AI intensity (work order 11b.7): `R`/`S` per car brand; whether brands with intensity above 1 gained Google share later (Δ`Gs`, 2025 to the last complete months of pull 3).
- t₄, t₅ and t₆ Presence against g, cross-sectionally, once each wave is scored.
- Lead and lag: ρ between P at each wave and g in each month from six months before to six months after (as far as the pulls reach).
- Presence × Consistency grid (11b.3) against g.
- US-site extras (§3.3) against their global domains.

### §2.13 What counts as support or failure, in one line

- Arm A supports "AI presence pays" only if `H_A2` is CONFIRMED. `H_A1` alone shows that AI and Google visibility go together, which brand size can explain; `H_A7` shows only that they move together within a brand. A FALSIFIED `H_A2` is the headline whatever the others show.

---

## §3 Brands, domains and AI waves

### §3.1 Sources on disk (read 2026-11-23)

- **Brand master v1.0 (DRAFT):** `registries/master/brand_master_v1.0.json` on branch `sp7-category-brand-master` (worktree `_worktrees/sp7-category-brand-master`, commit 94c7bcf). Brand-master IDs, status, parent company and SEC CIK below come from it. It has no website-domain field.
- **Domains on disk:** `osf/methodology/v1_13/registries/brand_domains_v1_13.csv` (branch `v1.13`, a8680f3, 2026-11-10): cars and spirits, each with a dated source under rule R1 (Wikidata P856, US-first rule for global car brands, decided by lane6 2026-11-10).
- **Domains resolved for r1:** airlines, banks and B2B software had no domain on disk. This lane queried Wikidata on 2026-11-23 (about 11:30 pm US Central): the SPARQL endpoint (one query by English label, `wdt:P856`) and the `wbgetentities` API by English Wikipedia title for six brands the label query missed. Raw results: `_worktrees/_runner_tmp/armA_r1/out_sparql.json` and the script output in the same folder (not in the deposit until the pre-lock check, §3.4). Free; no paid call.
- **Sales figures:** cars and spirits from `claude/shift-public-numbers-nov19.md` (figures checked against their sources on 2026-11-19); airlines, banks and software from the source types in §3.3, files fixed before lock.

### §3.2 Sample (replaces r0 §3.2)

| Category (brand master ID) | Source study for Presence | Eligible in master | In sample | Left out, and why | Sales or share measure |
|---|---|---|---|---|---|
| Passenger cars (CAT-1012) | v0.22 omnibus; t₁–t₆ | 19 | 18 (+3 US-site extras) | Fisker (no 2025 sales; bankrupt 2024); 5 closed brands (no domain) | 2025 US units × average transaction price (Shift) |
| Airlines, US (CAT-1019) | v0.40 (TO CONFIRM scored) | 11 | 11 | 7 closed or merged | 2025 US domestic enplaned passengers, US DOT/BTS |
| Retail banks, US (CAT-1018) | v0.40 (TO CONFIRM scored) | 26 | 26 (+1 US-site extra) | 15 merged, renamed or closed | Total deposits of the brand's FDIC-insured US bank, FDIC |
| B2B software (CAT-1017) | v0.24 / v0.25 (TO CONFIRM per brand) | 19 | 12 | Notion, Airtable, Linear, Miro, Stripe (private, no public revenue); Zendesk (private since 2022); Slack (inside Salesforce, no separate revenue); 5 closed or merged | Total revenue, latest fiscal year ended on or before 2025-12-31, SEC 10-K (SAP: 20-F) |
| Premium spirits (CAT-1009) | v0.23 omnibus; t₁–t₆ | 24 | 5 | 19 with no published US case volume | US 9-liter cases (published sources, §3.3); descriptive only |
| **Total** | | | **72 brands + 4 extras = 76 domains** | | |

- Not pulled: every other category (headphones, skincare, cosmetics, project-management software, personal finance apps, kitchen knives, running shoes, fragrance, coffee, tea, olive oil, household retail, cookware, technology brands, the v0.44 industries). About 200 brands with no public sales figure are dropped; a broader snapshot only later, on Pablo's go (D3). Technology brands stay out under the COI screen (§6.5).
- US-site rule (kept from r0): where a brand's US consumer site is a separate domain, the US domain is primary and the R1 global domain is a sensitivity. The 4 extras are listed in §3.3; at most 8 extras are allowed.

### §3.3 Domain list (exact; 76 domains)

Status: **OK** = domain from a dated source (Wikidata P856, or the v1.13 registry under rule R1); **TO CONFIRM** = not verified, must be checked before lock (§3.4), and not pulled if still unverified at lock (none left in r2; r1's 8 are marked "(r2)"). "Sales source" names the source; per-brand files, tables and identifiers are fixed before lock where marked.

**Cars (18 brands, 3 extras).** Domain source for every R1 domain: `brand_domains_v1_13.csv` (Wikidata P856 accessed 2026-11-10 unless stated). Sales source: `claude/shift-public-numbers-nov19.md`, 2025 US units with each brand's named source, × KBB December 2025 average transaction price by make where listed (otherwise the price named there).

| # | Group | Brand (ID) | Domain | Domain source | Status | 2025 US units source (Shift doc) |
|---|---|---|---|---|---|---|
| 1 | Luxury | Mercedes-Benz (BR-00370) | mercedes-benz.com | P856 Q36008 (brand item) | OK, sensitivity (mbusa.com confirmed) | Mercedes-Benz USA |
| 2 | Luxury | Mercedes-Benz, US site | mbusa.com | US-site rule; resolves (HTTP 301 to /en/home, 2026-11-23); cross-check agrees (2026-11-24) | OK, primary (r2) | — |
| 3 | Luxury | BMW (BR-00376) | bmw.com | P856 Q26678 | OK, sensitivity (bmwusa.com confirmed) | BMW of North America |
| 4 | Luxury | BMW, US site | bmwusa.com | US-site rule; no answer to a plain request on 2026-11-23 (likely bot filter); search index shows the US site; cross-check agrees (2026-11-24) | OK, primary (r2) | — |
| 5 | Luxury | Cadillac (BR-00372) | cadillac.com | P856 Q27436 | OK | best-selling-cars.com |
| 6 | Luxury | Porsche (BR-00375) | porsche.com | P856 Q40993 | OK | Porsche Cars North America |
| 7 | Luxury | Jaguar (BR-00371) | jaguar.com | v1.13 R1 web-search fallback (no P856) | OK, sensitivity (jaguarusa.com confirmed) | Automotive News estimate |
| 8 | Luxury | Jaguar, US site | jaguarusa.com | US-site rule; resolves (HTTP 302 to /en-us/, 2026-11-23); cross-check agrees (2026-11-24) | OK, primary (r2) | — |
| 9 | Luxury | Rolls-Royce (BR-00373) | rolls-roycemotorcars.com | P856 Q234803 | OK | Automotive News estimate |
| 10 | Luxury | Bentley (BR-00374) | bentleymotors.com | P856 Q27224 | OK | Automotive News estimate |
| 11 | Mass | Toyota (BR-00382) | toyota.com | P856 Q53268, US-first | OK | Toyota Motor North America |
| 12 | Mass | Honda (BR-00383) | honda.com | P856 Q9584, US-first | OK | Shift doc (units as listed) |
| 13 | Mass | Ford (BR-00384) | ford.com | P856 Q44294 | OK | Shift doc (without Lincoln) |
| 14 | Mass | Chevrolet (BR-00385) | chevrolet.com | P856 Q29570 | OK | Shift doc (Automotive News figure beside it) |
| 15 | Mass | Hyundai (BR-00386) | hyundaiusa.com | P856 Q55931, US-first | OK | Shift doc |
| 16 | Mass | Volkswagen (BR-00387) | vw.com | P856 Q246, US-first | OK | Shift doc |
| 17 | Mass | Nissan (BR-00388) | nissanusa.com | P856 Q20165 | OK | best-selling-cars.com |
| 18 | Electric | Tesla (BR-00377) | tesla.com | P856 Q478214 | OK | Cox Automotive estimate |
| 19 | Electric | Rivian (BR-00378) | rivian.com | P856 Q125552500 | OK | Cox Automotive estimate |
| 20 | Electric | Lucid (BR-00379) | lucidmotors.com | P856 Q28027517 | OK | Cox Automotive estimate |
| 21 | Electric | Polestar (BR-00380) | polestar.com | P856 Q4047174 | OK | Automotive News estimate |

**Airlines (11).** Domain source: Wikidata P856, accessed 2026-11-23. Share source for all: US DOT Bureau of Transportation Statistics, T-100 Domestic Segment (U.S. Carriers), calendar 2025, passengers summed by reporting carrier (TranStats); file and carrier codes TO CONFIRM.

| # | Brand (ID) | Domain | Domain source | Status | Note |
|---|---|---|---|---|---|
| 22 | American Airlines (BR-00488) | aa.com | P856 Q32396 | OK | |
| 23 | Delta Air Lines (BR-00489) | delta.com | P856 Q188920 (www. and language subdomains) | OK | |
| 24 | United Airlines (BR-00490) | united.com | P856 Q174769 | OK | |
| 25 | Southwest Airlines (BR-00491) | southwest.com | P856 Q503308 | OK | |
| 26 | Alaska Airlines (BR-00492) | alaskaair.com | P856 Q822614 | OK | |
| 27 | JetBlue (BR-00493) | jetblue.com | P856 Q161086 | OK | |
| 28 | Frontier Airlines (BR-00494) | flyfrontier.com | P856 Q1139541 | OK | |
| 29 | Allegiant Air (BR-00495) | allegiantair.com | P856 Q1319601 | OK | |
| 30 | Breeze Airways (BR-00496) | flybreeze.com | P856 Q55641146 | OK | whether it reports T-100 for all of 2025: TO CONFIRM |
| 31 | Hawaiian Airlines (BR-00497) | hawaiianairlines.com | P856 Q642610 | OK | owned by Alaska Air Group; whether BTS reports it separately for 2025: TO CONFIRM |
| 32 | Sun Country Airlines (BR-00498) | suncountry.com | P856 Q866289 | OK | |

**Retail banks (26, 1 extra).** Domain source: Wikidata P856, accessed 2026-11-23. Measure for all: total deposits of the brand's FDIC-insured US bank subsidiary (or subsidiaries, summed) in the Call Report for 2025-12-31, from FDIC BankFind Suite; the FDIC certificate number per brand is TO CONFIRM (one pre-lock item).

| # | Brand (ID) | Domain | Domain source | Status | Note |
|---|---|---|---|---|---|
| 33 | Chase (BR-00463) | chase.com | P856 Q524629 (Chase Bank) | OK | |
| 34 | Bank of America (BR-00464) | bankofamerica.com | P856 Q487907 | OK | |
| 35 | Wells Fargo (BR-00465) | wellsfargo.com | P856 Q744149 | OK | |
| 36 | Citi (BR-00466) | citi.com | P856 Q857063 (Citibank) | OK | |
| 37 | U.S. Bank (BR-00467) | usbank.com | P856 Q739084 (U.S. Bancorp) | OK | |
| 38 | Capital One (BR-00468) | capitalone.com | P856 Q1034654 | OK | |
| 39 | Morgan Stanley (BR-00469) | morganstanley.com | P856 Q334204 | OK | |
| 40 | Goldman Sachs / Marcus (BR-00470) | goldmansachs.com | P856 Q193326 | OK, sensitivity (marcus.com confirmed) | consumer deposits are under Marcus |
| 41 | Marcus, US consumer site | marcus.com | US-site rule (consumer brand of BR-00470); request blocked (HTTP 403) on 2026-11-23; search shows marcus.com/us/en (Marcus by Goldman Sachs); cross-check agrees (2026-11-24) | OK, primary (r2) | primary for BR-00470 |
| 42 | PNC (BR-00471) | pnc.com | P856 Q38928 | OK | |
| 43 | Truist (BR-00472) | truist.com | P856 Q795486 | OK | |
| 44 | TD Bank (BR-00473) | td.com | P856 Q7669891 (TD Bank, US); www.td.com 301 to /us/en/personal-banking, tdbank.com redirects to it (2026-11-24); cross-check agrees | OK (r2) | td.com also serves Canada; the US site is a path, not a separate domain (§7) |
| 45 | Charles Schwab (BR-00474) | schwab.com | P856 Q1066028 | OK | |
| 46 | Fifth Third (BR-00475) | 53.com | P856 Q1411810 | OK | |
| 47 | Huntington (BR-00476) | huntington.com | P856 Q798819 | OK | |
| 48 | BMO (BR-00477) | bmo.com | P856 Q806693 (Bank of Montreal); Q4835981 (BMO Bank, US) lists bmoharris.com and bmo.com/en-us; bmo.com 301 to /en-us/main/personal/, bmoharris.com no answer (2026-11-24); cross-check agrees | OK (r2) | bmo.com also serves Canada; the US site is a path (§7) |
| 49 | Citizens (BR-00478) | citizensbank.com | P856 Q5122694 | OK | |
| 50 | First Citizens (BR-00479) | firstcitizens.com | P856 Q5452733 is ir.firstcitizens.com; root domain taken; firstcitizens.com 301 to www (200, First Citizens Bank personal banking, 2026-11-24); cross-check agrees | OK (r2) | |
| 51 | M&T Bank (BR-00480) | mtb.com | P856 Q3272257 (www3.mtb.com; root domain) | OK | |
| 52 | American Express (BR-00481) | americanexpress.com | P856 Q194360 | OK | |
| 53 | KeyBank (BR-00482) | key.com | P856 Q1740314 | OK | |
| 54 | Ally (BR-00483) | ally.com | P856 Q2032800 | OK | |
| 55 | HSBC (BR-00484) | hsbc.com | P856 Q190464 (global); Q5635869 (HSBC Bank USA) gives us.hsbc.com; both answer (2026-11-24); cross-check answered us.hsbc.com (same site) | OK (r2): hsbc.com pulled | us.hsbc.com not pulled: DataForSEO's endpoint page does not document subdomain targets (§3.4, item 6); global site mixes countries (§7) |
| 56 | Regions (BR-00485) | regions.com | P856 Q917131 | OK | |
| 57 | UBS (BR-00486) | ubs.com | P856 Q193199 | OK | global site; US deposits small relative to brand |
| 58 | Pinnacle (BR-00487) | pnfp.com | P856 Q7196294 | OK | status after its announced merger with Synovus: TO CONFIRM |
| 59 | Discover (BR-00521) | discover.com | P856 Q5281775 | OK | status after Capital One's 2025 acquisition, and whether Discover Bank still files separately: TO CONFIRM |

**B2B software (12).** Domain source: Wikidata P856, accessed 2026-11-23. Revenue source for all: total revenue for the latest fiscal year ended on or before 2025-12-31, from the company's 10-K (SAP SE: Form 20-F, euros, converted at the year's average rate; rate source TO CONFIRM), SEC EDGAR by the CIK in the brand master. US revenue where the filing discloses it is a sensitivity.

| # | Brand (ID) | Domain | Domain source | Status | SEC CIK (brand master) |
|---|---|---|---|---|---|
| 60 | Salesforce (BR-00418) | salesforce.com | P856 Q941127 | OK | 0001108524 |
| 61 | HubSpot (BR-00419) | hubspot.com | P856 Q5926631 | OK | 0001404655 |
| 62 | ServiceNow (BR-00420) | servicenow.com | P856 Q7455653 | OK | 0001373715 |
| 63 | Workday (BR-00421) | workday.com | P856 Q8034666 | OK | 0001327811 |
| 64 | SAP (BR-00422) | sap.com | P856 Q552581 | OK | 0001000184 |
| 65 | Oracle (BR-00423) | oracle.com | P856 Q19900 | OK | 0001341439 |
| 66 | Figma (BR-00425) | figma.com | P856 Q96186334 (product item) | OK | 0001579878 |
| 67 | Datadog (BR-00428) | datadoghq.com | P856 Q16248637 | OK | 0001561550 |
| 68 | Snowflake (BR-00429) | snowflake.com | P856 Q22078063 (also lists snowflake.net; .com taken) | OK | 0001640147 |
| 69 | Twilio (BR-00431) | twilio.com | P856 Q7858039 | OK | 0001447669 |
| 70 | Cloudflare (BR-00432) | cloudflare.com | P856 Q4778915 | OK | 0001477333 |
| 71 | MongoDB (BR-00433) | mongodb.com | P856 Q4546965 (MongoDB Inc.) | OK | 0001441816 |

**Spirits (5; descriptive only).** Domain source: `brand_domains_v1_13.csv` (P856, accessed 2026-11-10). Case-volume source: `claude/shift-public-numbers-nov19.md`; the article URLs behind each figure are TO CONFIRM (the doc names the publisher, not the URL).

| # | Brand (ID) | Domain | Status | US 9-liter cases: published source named in the Shift doc |
|---|---|---|---|---|
| 72 | Jack Daniel's (BR-00396) | jackdaniels.com | OK | 2025, Impact Databank via Whisky Advocate |
| 73 | Jameson (BR-00401) | jamesonwhiskey.com | OK | 2025, Impact Databank via Whisky Advocate |
| 74 | Grey Goose (BR-00398) | greygoose.com | OK | 2025, Vinetur with Impact Databank figures |
| 75 | Hennessy (BR-00395) | hennessy.com | OK | 2024, Market Watch |
| 76 | Rémy Martin (BR-00408) | remymartin.com | OK | 2024, Market Watch |

**Counts.** Cars 21 domains (18 brands + 3 extras), airlines 11, banks 27 (26 + 1 extra), B2B software 12, spirits 5: **76 domains**. r1's **8 TO CONFIRM domains are all resolved in r2** (mbusa.com, bmwusa.com, jaguarusa.com, marcus.com: confirmed, primary for their brands, the R1 domain the sensitivity; td.com, bmo.com, firstcitizens.com: confirmed; hsbc.com: confirmed and pulled, us.hsbc.com recorded, not pulled), from the free HTTP and search checks of 2026-11-23/24 (`prereg/armA_prelock_notes_r1.md`, §1) and the blind cross-check (§3.4, item 3). No domain is UNRESOLVED. Final count: cars 21 (18 + 3 extras), airlines 11, banks 27 (26 + 1 extra), B2B software 12, spirits 5 = **76 domains, 72 brands**.

### §3.4 Pre-lock tasks (all fixed before lock)

1. **Domain file:** this list written to `osf/arm_a/registries/arm_a_domains_r1.csv` (path TO CONFIRM) with brand-master ID, domain, status (RESOLVED, NONE, UNRESOLVED), source and access date.
2. **The 8 TO CONFIRM domains** checked under rule R1 and the US-site rule (no paid API). DONE 2026-11-24: all 8 resolve (`prereg/armA_prelock_notes_r1.md`, §1); outcome in §3.3.
3. **Blind model cross-check.** A model from a provider other than the resolver's (the resolver here is Wikidata plus a Claude lane, so a non-Anthropic model), blind to this list, is given each brand name and category and asked for the official US website domain. Agreement % reported; on disagreement the domain is UNRESOLVED and not pulled (no human tiebreak). It counts toward the $100 per-paper cap, not the $50 DataForSEO ceiling. It runs only when no other paid collection runs on the Mac (none was running). Limit stated: no human check. **DONE Tue 2026-11-24, 13:36–13:39 UTC (Pablo's go, 7:29 am US Central):**
   - Model `gpt-6-astra` (OpenAI; served model id as returned: `gpt-6-astra`), Responses API, no web search, provider defaults, max 800 output tokens; one call per brand with only the brand name, category and "Country: United States"; 72 calls, no errors. Price $10 / $50 per 1M input / output tokens (OpenAI pricing page as read 2026-11-24, recorded in `osf/v46/scripts/ai_checks_v0_46.py`); 6,268 input and 1,068 output tokens: **$0.1161** (hard cap $2, checked before every call).
   - Matching rule, fixed in the script before the first call: host names normalised (scheme, path, `www.` removed); agree if the model's host equals our primary or the brand's US-site extra or alternate, or has the same registrable domain; a remaining difference would have been checked for a redirect to our domain and otherwise been a disagreement.
   - **Result: 72 of 72 agree (100%)**; 71 exact (including mbusa.com, bmwusa.com, jaguarusa.com, marcus.com and us.hsbc.com, each matching the brand's US-site extra or alternate), 1 same registrable domain (Honda: automobiles.honda.com against honda.com; honda.com kept). No disagreement, so no domain is UNRESOLVED.
   - Files: `prereg/armA_crosscheck/armA_domain_crosscheck.py` (script), `raw_responses_20261124T133629Z.jsonl` (every response as returned, with sent and received UTC times, usage and cost), `crosscheck_20261124T133629Z.csv` (agree/disagree per brand), `summary_20261124T133629Z.json`, run and compare logs.
4. **Presence files per category:** the per-brand Presence file, study and wave date for airlines and banks (v0.40, only if scored before lock) and B2B software (v0.24 or v0.25, per brand); a category without one leaves `H_A1` and `H_A6`.
5. **Sales sources:** the BTS file and carrier codes; the FDIC certificate per bank; the 10-K/20-F per software company and the euro rate; the spirits article URLs. A category without a fixed source at lock moves to exploratory (§2.9).
6. **Domain test for subdomains:** whether `historical_rank_overview` counts subdomains of the target and accepts a subdomain as the target (us.hsbc.com), from DataForSEO's documentation; no paid call. Read 2026-11-24: not documented on the endpoint page (`prereg/armA_prelock_notes_r1.md`, §3); hsbc.com is therefore the pulled target (§3.3).
7. **Status checks:** Discover (Capital One acquisition) and Pinnacle (Synovus merger): which brand and bank file stood at the wave date. Each brand is kept as it stood at its wave (11a.5).

### §3.5 AI waves

Read from the answer files on 2026-11-23 (dates from each file's `timestamp` column), plus the planned waves.

| Wave | Study | Date (UTC) | Models | Car brands | File |
|---|---|---|---|---|---|
| t₁ | v0.22 | 2026-05-25 | claude-opus-4-5, claude-sonnet-4-5, gemini-2.5-flash, gemini-2.5-flash-lite, gpt-4o, gpt-4o-mini | 24 | `osf/v22/phase_a_results.csv`, `phase_b_results.csv` |
| (version study) | v0.32 | 2026-06-05 | panel A: the t₁ six as dated snapshots; panel B: claude-opus-4-8, claude-sonnet-4-6, gpt-5.5-2026-04-23, gpt-5.4-mini-2026-03-17, gemini-3.5-flash, gemini-3.1-flash-lite | 24 | `osf/v32/data/phase_a_A.csv`, `phase_a_B.csv` |
| t₂ | v0.34 | 2026-06-10 | the t₁ six | 24 | `osf/v34/data/v22/phase_a_results.csv` |
| t₃ | v0.41 | 2026-11-09 | the t₁ six | 24 | `osf/v41/data/v22/phase_a_results.csv` (worktree `aias-6.0-preview-paper`) |
| t₄ | v0.42 | collection log 2026-11-11 to 2026-11-14 (exact window TO CONFIRM from `t4_batches.jsonl`) | claude-fable-5-2, gpt-6-astra, gemini-4-argon | 24 | `osf/v42/data/t4_raw.jsonl` (worktree `t4-paper`) |
| t₅ | v0.45 | models available Wed 2026-12-02; collection Thu 2026-12-03 (window to 12-06 per its pre-registration header) | t₄'s three | 24 | not yet collected |
| t₆ | TO CONFIRM | about Fri 2027-02-12 (roadmap: t₄ + 3 months) | TO CONFIRM (t₄'s three expected) | 24 | not yet collected |
| t₇ | — | **not dated**: `aias_roadmap_ssot.md` names t₄, t₅ (+3 weeks) and t₆ (+3 months) only | — | — | — |

- `H_A2`, `H_A3` use t₁ (Shift's `R`). `H_A4` uses t₁ bands. `H_A5` uses t₁ → t₃ (same panel). `H_A7` uses t₄ → t₆ (same panel). Airlines, banks and B2B software use their own study's wave (§3.4, item 4).
- Problem found in r0, still open: the repo's `main` branch (c79f4f5) does not carry osf/v41 onward; the analysis code must read the files at their locked tags (tag names TO CONFIRM), never from a working tree.

---

## §4 Google-visibility data

### §4.1 Request (fixed)

- Endpoint `POST /v3/dataforseo_labs/google/historical_rank_overview/live`; one task per request: `target` = the domain (no scheme, no `www.`), `location_code` 2840 (United States), `language_code` "en", `date_from` as set per pull in §5.2 ("2024-11-01" for every full-history request). No other parameter.
- Why `date_from`: without it the endpoint returned only 6 months (Jun–Nov 2026); with "2024-11-01" it returned 25 monthly items, Nov 2024–Nov 2026 (§4.2). Nov 2024 covers every AI wave on disk (first: 2026-05-25) with an 18-month pre-period. Whether earlier months exist is TO CONFIRM from the documentation (D5; default: keep 2024-11-01, the tested value).
- Whether a later `date_from` (e.g. "2026-11-01") returns only the months from that date, as the incremental mode assumes, is TO CONFIRM from the documentation; the price check (§5.4) stops the pull if the first response returns a different number of months than planned.

### §4.2 Feasibility test (coordinator, Mon 2026-11-23 about 10:05 pm US Central; paid test, $0.4044)

- Raw JSON: `_worktrees/_runner_tmp/dataforseo_test/` (`hro_allrecipes.com_20261124T040421Z.json`, `hro_nasa.gov_20261124T040421Z.json`, `hro_datefrom_allrecipes.com_20261124T040453Z.json`, scripts `hro_test.py`, `hro_test_datefrom.py`). Test domains allrecipes.com and nasa.gov are not in the study.
- Status "Ok." on all three. Cost $0.1272 per request for 6 months and $0.15 for 25 months, i.e. $0.12 + $0.0012 per month returned.
- Per-month fields under `metrics.organic`: `pos_1`, `pos_2_3`, `pos_4_10`, `pos_11_20` … `pos_91_100`, `etv`, `count`, `estimated_paid_traffic_cost`, `is_new`, `is_up`, `is_down`, `is_lost`, `clickstream_etv`, `clickstream_gender_distribution`, `clickstream_age_distribution`.
- The pull month (Nov 2026) was partial. Visible level shifts (allrecipes.com etv 10.3M in Nov 2024, 67.5M in Dec 2024) suggest index or method breaks in the series (§6.2).
- Checked by r0's writer from the saved JSON: allrecipes.com etv 10,274,478 (Nov 2024), 67,467,793 (Dec 2024), 46,649,775 (Jan 2025), 13,097,337 (Oct 2026), 13,482,009 (Nov 2026, partial). `clickstream_etv` is null in these months, so it is not expected to be usable (§2.1).

---

## §5 Budget, pull calendar and spending rules

### §5.1 Prices (DataForSEO, checked 2026-11-23; re-checked before every pull)

$0.12 per request plus $0.0012 per month returned (the test in §4.2). $50 minimum top-up; funds stay on the balance until spent. Pay as you go, no subscription. Pablo adds $50 once, after the lock; there is no second top-up.

### §5.2 Pull calendar and expected cost (n = 76 domains)

Cost per pull = n_domains × ($0.12 + $0.0012 × months returned). Months are counted including the partial pull month, which the API returns and charges.

| Pull | Tied to | Planned date (US Central) | Full history: `date_from`, months, cost | Incremental: `date_from`, months, cost |
|---|---|---|---|---|
| 1 | after the lock (history for t₁–t₄ and the baseline) | Mon 2026-12-07 (first weekday after the lock and after the t₅ collection, Dec 3–6, so no two paid collections run together); fallback any day to Thu 2026-12-31 | 2024-11-01; Nov 2024–Dec 2026 = **26**; 76 × (0.12 + 0.0312) = 76 × 0.1512 = **$11.49** | — (first pull is always full) |
| 2 | after t₅ (Dec 3–6), once December is complete | Mon 2027-01-04; fallback to Fri 2027-01-29 | 2024-11-01; Nov 2024–Jan 2027 = 27; 76 × 0.1524 = $11.58 | 2026-11-01 (Nov = overlap month; Dec new; Jan partial) = **3**; 76 × (0.12 + 0.0036) = 76 × 0.1236 = **$9.39** |
| 3 | after t₆ (about 2027-02-12), once February is complete | Mon 2027-03-01; fallback: if t₆ slips, the first Monday of the month after t₆ ends, and no later than Mon 2027-04-05 | 2024-11-01; Nov 2024–Mar 2027 = **29**; 76 × (0.12 + 0.0348) = 76 × 0.1548 = **$11.76** | 2026-12-01 (Dec = overlap month; Jan, Feb new; Mar partial) = 4; 76 × 0.1248 = $9.48 |

**Three modes, totals (n = 76):**

| Mode | Pull 1 | Pull 2 | Pull 3 | Total | Cushion to $50 |
|---|---|---|---|---|---|
| A. All full history | 11.49 | 11.58 | 11.76 | **$34.84** | $15.16 |
| B. All incremental (one overlap month) | 11.49 | 9.39 | 9.48 | **$30.37** | $19.63 |
| **C. Recommended: pull 2 incremental, pull 3 full** | 11.49 | 9.39 | 11.76 | **$32.65** | $17.35 |

Running total, mode C: $11.49 after pull 1 → $20.88 after pull 2 → $32.65 after pull 3. If pull 3 falls back to Mon 2027-04-05 (30 months full): 76 × 0.1560 = $11.86, total $32.74. At the cap of 80 domains (if extras are added up to the allowed 8, §3.2), mode C costs 80 × (0.1512 + 0.1236 + 0.1548) = 80 × 0.4296 = $34.37. Every case stays under the $48 hard stop, with room for one full retry of a pull.

Exact arithmetic (mode C): 76 × 0.1512 = 11.4912; 76 × 0.1236 = 9.3936; 76 × 0.1548 = 11.7648; sum 32.6496.

**Why mode C.** Pull 2 only has to add December (t₅'s window month) and January, so an incremental request with one overlap month (November) is enough: the overlap shows whether November was restated. Pull 3 is full history on purpose: it gives one vintage for every month Nov 2024–Feb 2027, so `H_A7` compares the t₄ and t₆ windows from the same version of DataForSEO's index (no splice across vintages), and it is the full restatement check against pull 1 (11a.5, data as it stood). Mode B saves $2.28 more but leaves `H_A7` on a splice of three vintages joined by one-month overlaps; mode A spends $2.19 more for a second full restatement check that adds little. If Pablo prefers to spend the least, mode B is the fallback (D4).

**Breadth against repeat pulls.** Almost all of the price is the $0.12 charged per request, not the $0.0012 per month, so a domain costs about the same whether it brings two years of history or three months. The $50 can therefore buy one wide snapshot (about 300 domains once, r0's plan) or a narrow panel bought three times (76 domains at three dates). A wide snapshot adds categories with no sales figure, which can only test whether Google and AI visibility go together, a link brand size already explains; it cannot test whether AI presence pays. Repeat pulls on brands with public sales or share figures keep every test that touches sales (`H_A2`, `H_A3`, `H_A6`), add the only within-brand test (`H_A7`), which removes brand size, and check twice whether DataForSEO rewrote past months. The cost is n: about 70 brands in four categories, so power stays low and the pooled `H_A1` rests on four categories. We choose depth because the question is whether AI presence pays, and only brands with sales figures, followed over time, can answer it; a broader snapshot can be bought later, on Pablo's go, if this arm finds something worth widening.

### §5.3 Pull order (fixed in advance; the same in every pull)

Cars → airlines → banks → B2B software → spirits → US-site extras, in table order (§3.3). A pull runs whole or not at all: before it starts, the script checks that its full expected cost fits under the limits in §5.4; if not, it does not start and the case goes to Pablo.

### §5.4 Spending limits (computed from the `cost` field of every response, summed across all pulls)

- **Per-pull limit $13.00** (pull 1 expected $11.49, pull 2 $9.39, pull 3 $11.76). A pull stops when it reaches its limit.
- **Hard stop $48.00 cumulative** (all pulls + any retry), checked before every request; the $50 balance is never fully drawn.
- **Price check before every pull:** (1) DataForSEO's published price for the endpoint is read and written to the manifest; if it differs from $0.12 + $0.0012 per month, the pull does not start and the case goes to Pablo; (2) after the first request of the pull, its `cost` and its number of months are compared with the plan; if `cost` differs from $0.12 + $0.0012 × months returned by more than $0.005, or any single request costs more than $0.20, or the months returned differ from §5.2, the pull stops and the case goes to Pablo.
- **Retries:** a failed request (a `status_message` other than "Ok.", or no items) is retried once after 60 s; its cost counts. A domain that fails twice is recorded as `PULL_FAILED` for that pull (§6.4).
- No pull runs beside another paid collection on the same Mac (programme rule: one paid collection at a time).
- No spend beyond $48 in any case; the ceiling is $50 and there is no second top-up. Any later broader snapshot is a new decision by Pablo with its own budget line. The arm's spend counts toward the $100 per-paper cap.
- Any money left after pull 3 stays on the balance; it is not spent to reach $50.

---

## §6 Analysis plan

### §6.1 Data as it stood (11a.5)

- Each response is saved exactly as returned, one file per request, `osf/arm_a/data/raw/pull{1,2,3}/hro_{domain}_{UTC timestamp}.json` (path TO CONFIRM), never edited or overwritten; each pull in its own folder.
- A manifest row per request: pull number, brand-master ID, domain, request body, HTTP status, `status_message`, `cost`, months returned, pull time (UTC), the price read before the pull, and SHA-256 of the file. The manifest is committed the day of each pull.
- The API key lives on the Mac outside the repo (as the OSF token does) and is never written to any file in the repo or the deposit.
- The brand list is the list as it stood at each AI wave; a brand that closes or merges after its wave stays in, labelled.
- **Vintages:** cross-sectional tests at t₁–t₄ and `H_A4`, `H_A5` use pull 1 (the first data as it stood). `H_A7` uses pull 3 (single vintage over all its months). Pull 2 serves the t₅ exploratory analyses and the November overlap check.
- **Restatement:** for months in two pulls (Nov 2026 in pulls 1 and 2; Nov 2024–Nov 2026 in pulls 1 and 3; Dec 2026 in pulls 2 and 3), the share of domain-months whose etv changed by more than 1% is reported. If more than 20% of domain-months changed by more than 10% between pulls 1 and 3, every test using pull 1 is also re-run on pull 3 and both are shown; the pre-registered vintage still decides the verdict.

### §6.2 Index or method breaks (rule fixed before any data)

- For each month m, compute the median over all pulled domains of Δg(m) = g(m) − g(m−1), and the share of domains with |Δg| > 0.2 moving in the same direction.
- **A month is flagged as a break** if |median Δg| > 0.40, or if at least 80% of domains move by more than 0.2 in the same direction. Flags are computed once per pull, before any AIAS variable is joined, and written to the manifest.
- Handling: (1) cross-sectional tests (`H_A1`, `H_A2`, `H_A3`, `H_A6`) compare brands within the same category and month, so a common multiplicative shift does not change ranks, nor (for `H_A2`, r3) within-group shares or their logs; (2) change tests (`H_A4`, `H_A5`, `H_A7`) use category-month demeaning (§2.1); (3) robustness: every test is re-run with flagged months dropped from every window, each window then using the three nearest unflagged complete months at or before the wave; (4) a figure of the monthly median g with flagged months marked goes in the paper.

### §6.3 Joining AI and Google data

- **The category's AI wave** for `H_A1`: t₁ (2026-05-25) for cars; for airlines, banks and B2B software the study and date fixed in §3.4, item 4. A category whose wave falls before Feb 2025 has no full window and is excluded from `H_A1` (TO CONFIRM dates of v0.24, v0.25).
- Joins are by brand-master ID only, never by name. A US-site extra joins to its brand's ID and replaces the R1 domain only where §3.3 says so. The join script and its unit tests are written and frozen before lock; they are run first on simulated Google data of the right shape, never on real data, before lock.
- Stability before fit (11a.6): no threshold, window or transformation is tuned on the data. Every result is reported for the pre-registered choice first; robustness rows follow.

### §6.4 Exclusions and missing data (counted and listed in the paper)

- No domain (UNRESOLVED), `PULL_FAILED` in the pull a test uses, or a domain shared by two brands of the same category (both excluded from that category's tests).
- A domain with etv = 0 or missing in more than half of the months of a test's windows is excluded from that test.
- A category with fewer than 8 analysable brands is shown but not pooled.
- No imputation. A missing month inside a window: the window mean uses the remaining months if at least 2 of 3 are present; otherwise the brand is excluded from that test.

### §6.5 COI screen (pre-registered; DEVIATIONS Entry 0 at lock)

- The employer's categories are out: technology brands (CAT-1020) are not pulled; no phones, TVs, appliances, semiconductors or displays enter any test.
- S-COI (sensitivity): every result is also reported without the four sample brands for which Cheil Worldwide or its Iris unit has worked: Chevrolet, BMW, Bentley, Jack Daniel's (v0.62 DEVIATIONS Entry 0, Part F). The headphones registry (Denon) and Eucerin are not in this arm's sample.
- Entry 0 for airlines, banks and B2B software has not been run; it is a pre-lock task (TO CONFIRM). A brand it flags is kept and reported with and without it, as the Cheil-linked brands are, unless Pablo decides otherwise.

### §6.6 Reporting

- Every page says: association only; these data cannot show that AI presence causes sales or Google visibility, or the reverse.
- Each hypothesis with its verdict word, statistic, CI, p (raw and Holm-adjusted) and n; pooled beside within-category (and, for cars, within competitive group); equal-weighted beside size-weighted; with and without S-COI; with and without flagged months; the vintage used.
- Band results as outcome rates by band (11a.1): mean outcome, hit rate and n per band, with the reversion baselines beside them.
- The headline is one plain pair of numbers with its source line (§2.3), null included.
- Spend per pull and in total, against the plan in §5.2.
- Uncertainty is always reported (the S&P reports' lack of intervals is not copied).

---

## §7 Limitations (stated up front)

- One sales year (2025, spirits 2024–2025) and small n (18 cars, 11 airlines, 26 banks, 12 software, 5 spirits): a first look with low power (§2.11).
- Only brands with public figures: listed software companies and large banks and airlines; results do not speak for private or small brands.
- Sales measures differ by category (revenue in money, passengers, deposits, cases) and are used only within category, as ranks (for `H_A2`, r3: as log shares centred within competitive group; the zero rule for `R` in §2.3 is a fixed choice, with other offsets as sensitivity).
- Bank deposits and software revenue are company-level; one company can carry several brands or sites, and global sites (td.com, bmo.com, hsbc.com, ubs.com, sap.com) mix countries.
- DataForSEO's etv is DataForSEO's own estimate (its method per the documentation, TO CONFIRM), not Google's figures; breaks in its index (§6.2) are handled by rule, not removed.
- A brand's domain is not the brand: dealer, retailer, marketplace, travel-agency and review sites carry much of a brand's search demand.
- Brand size drives all three measures; `H_A2` controls for Google share but not for advertising, distribution or price; `H_A7` removes level differences but covers only three months.
- The AI waves come from a retiring 2024–25 panel (t₁–t₃) and one new panel (t₄–t₆); answers are to set questions, not to real buyers' prompts.
- Showing that AI takes over from search needs further waves and a search-volume trend (idea doc, "Limits"); this arm does not claim it.

---

## §8 Declarations

**Conflict of interest.** The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-analyses archived AI answers against brand registries fixed in earlier phases and adds no new brand selection beyond the category and brand choice in §3.2 (brands with public sales or share figures); each registry carries its source-phase conflict-of-interest handling forward unchanged, and the technology-brands category is left out because it includes Samsung's categories. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands — Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) — characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). For the record of the programme's registries: in the audiophile-headphones registry, AKG was substituted with Denon before the v0.19 pre-registration lock (AKG is owned by Harman International, a Samsung subsidiary since March 2017; deal agreed November 2016) to avoid the appearance of conflict (v0.19 pre-registration §2.3; v0.19 DEVIATIONS Entry 1); Harman completed its acquisition of Masimo's Sound United brands, Denon included, on September 23, 2025, so Denon was already a Samsung-group brand. That registry is not used in this arm. Samsung's agency Cheil Worldwide, or its Iris unit, has worked for four brands in this arm's sample (Chevrolet, BMW, Bentley, Jack Daniel's; v0.62 DEVIATIONS Entry 0, Part F); results are also reported without them. The airline, bank and B2B software registries have not yet been screened; their screen is a pre-lock task (§6.5). TO CONFIRM: the COI text conformed verbatim to the source records before lock (CLAUDE.md rule: conform from the locked record, not memory).

**Funding.** Self-funded. Google-visibility data bought from DataForSEO (pay as you go), at most US$50 for the whole study.

**Ethics.** Not applicable; no human subjects.

**Use of AI tools.** During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

---

## §9 Lock procedure and change log

- **r3 draft** goes to the pre-registrant through the coordinator. The 24 hours restarted with his decision D12 (b) of Tue 2026-11-24, 8:13 am US Central (it changes `H_A2`'s statistic); it locks at the earliest Wed 2026-11-25, about 8:15 am US Central, unless he holds it (D1).
- **Before lock:** the remaining pre-lock tasks of §3.4 and §6.5 are done and written into the lock text (or into the lock commit); every TO CONFIRM in §10 is closed or its default applied. Any further change to a hypothesis, test, threshold, category or brand list, pull calendar, pull mode or spending limit restarts the 24 hours (D12 (b), which changes `H_A2`'s statistic, did: r3).
- **Lock:** a lock manifest (SHA-256 of this file, the domain list, the join and analysis scripts and their tests, the pull script); commit; tag (name TO CONFIRM, e.g. `arm-a-prereg-r1`); the coordinator pushes and deposits at OSF. Only then does Pablo add the $50, and only then may the pull script run.
- **After lock:** a locked pre-registration never changes; any change is a dated DEVIATIONS entry, and any new idea is a labelled exploratory analysis.

**Change log**

- 2026-11-23, r0 (c7e96f7, f3102e0): first draft, from the idea doc v1.1, the S&P work order v1.2 (§3, §11a), the brand master v1.0 draft (94c7bcf), `brand_domains_v1_13.csv` (a8680f3), the archived wave files and the coordinator's DataForSEO test of 2026-11-23. No study domain pulled.
- 2026-11-23, r1: Pablo's 10:28–10:33 pm decision (ceiling, sales-data brands only, three pulls). Sample 76 domains; pull calendar and modes; `H_A7` added; power approximations; domain list with sources (Wikidata queried 2026-11-23); Declarations adjusted to the new sample. No study domain pulled; no paid call made.
- 2026-11-24, r1 pre-lock (a5f1696): power simulation (seed 20261124) and pre-lock notes; no paid call.
- 2026-11-24, r2: Pablo's 7:29 am US Central decisions ("Ok to all"): `H_A2` by Freedman–Lane; blind domain cross-check run (gpt-6-astra, 72/72 agree, $0.1161); the 8 TO CONFIRM domains resolved (76 domains kept); power simulation re-run with FL and a diagnostic (D12); lock earliest Wed 2026-11-25, about 7:30 am US Central. No study domain pulled; no DataForSEO call.
- 2026-11-24, r3: Pablo's 8:13 am US Central decision D12 (b) ("As you suggest"): `H_A2` by Freedman–Lane on log shares centred within competitive group, with a fixed zero rule for `R`; the r2 rank test kept as a declared sensitivity; power and size simulation re-run (`armA_power_sim_r3.py`, seed 20261124); change table at the top; lock earliest Wed 2026-11-25, about 8:15 am US Central. No study domain pulled; no DataForSEO or other paid call.

---

## §10 Open items

### §10.1 TO CONFIRM (what is needed)

1. Study number and tag name (coordinator).
2. Pablo's OK of 🔴 (o), section 11a's design rules (Pablo; this draft follows them).
3. ~~The 8 TO CONFIRM domains~~ CLOSED in r2: all resolved, 76 domains kept (§3.3).
4. ~~Blind model cross-check~~ CLOSED in r2: gpt-6-astra, 72/72 agree, $0.1161 (§3.4, item 3).
5. Per-brand Presence file, study and wave date for airlines, banks (v0.40 scored?) and B2B software (§3.4, item 4).
6. Sales sources: BTS T-100 file and carrier codes (Breeze, Hawaiian); FDIC certificate per bank; 10-K/20-F per software company and the euro rate for SAP; the spirits article URLs (§3.4, item 5).
7. Status at the wave date of Discover and Pinnacle (§3.4, item 7).
8. Whether the endpoint counts subdomains or accepts a subdomain target; how far back history goes; whether a later `date_from` returns only months from that date (DataForSEO documentation, no paid call).
9. t₆ date and panel (needed for `H_A7`); exact t₄ window from `t4_batches.jsonl`; the locked tags from which every wave file is read.
10. ~~Power of `H_A2` (and `H_A1`) by simulation~~ CLOSED (r1 pre-lock; FL re-run in r2; r3 test re-run in r3, §2.11). D12 decided (b) in r3.
11. COI Entry 0 for airlines, banks and B2B software, and the COI text conformed to the source records.
12. Seeds not used elsewhere (§2.1).

### §10.2 Open decisions (recommended default in bold)

- **D1 Lock timing.** **At the earliest 24 h after Pablo's decision D12 (b) of Tue 2026-11-24, 8:13 am US Central: Wed 2026-11-25, about 8:15 am US Central, unless he holds it** (r2: 7:30 am, from his 7:29 am decisions); alternative: January with arm B (idea doc v1.1).
- **D2 Scope (decided by Pablo 2026-11-23, 10:28–10:33 pm).** 72 brands with public sales or share figures + 4 US-site extras = 76 domains (cars 18, airlines 11, banks 26, B2B software 12, spirits 5). Open only: **include the 5 spirits as descriptive** (adds $2.15 over three pulls in mode C); alternative: leave them out.
- **D3 Broader snapshot.** **None in this arm**; a snapshot of the ~200 brands without sales data only later, on Pablo's go, with its own budget line.
- **D4 Re-pull mode.** **Mode C: pull 2 incremental (3 months), pull 3 full history; $32.65 expected**; alternatives: mode B all incremental ($30.37), mode A all full ($34.84).
- **D5 History start.** **`date_from` 2024-11-01 (tested)**; alternative: an earlier start if the documentation shows more history (adds $0.0012 per month per domain per full pull).
- **D6 Primary Google measure.** **etv**; alternative: ranked-keyword count, which does not depend on DataForSEO's click model.
- **D7 Cheil-linked brands.** **Kept, with S-COI reported beside every result (as v0.62)**; alternative: drop them from the primary results.
- **D8 `H_A7` status.** **SECONDARY (in the secondary Holm family), conditional on t₆ using t₄'s panel by 2027-03-31**; alternative: exploratory only, which leaves the other secondary tests a lighter Holm burden.
- **D9 US-site extras.** **The 4 listed (mbusa.com, bmwusa.com, jaguarusa.com, marcus.com), US site primary once confirmed** (all 4 confirmed in r2, §3.3); alternative: R1 domains only (72 domains, saves $1.72 over three pulls).
- **D10 t₇.** **No pull planned** (t₇ is not dated in the roadmap); a fourth pull, if a t₇ is set, is a new decision by Pablo (about $9.48 incremental at 76 domains; the total then stays under the $48 hard stop in every mode: at most $34.84 + $9.48 = $44.32).
- **D11 File location.** **`prereg/arm_a_seo_prereg_draft_r3.md` on branch `arma-seo-prereg`**, moving to `osf/<study>/prereg/PRE_REGISTRATION_<study>.md` (the v0.42 pattern) once the study number is set.
- ~~**D12 (new in r2) `H_A2`'s scale.**~~ **DECIDED (b) by Pablo, Tue 2026-11-24, 8:13 am US Central ("As you suggest"); applied in r3 (§2.3, §2.11).** r2's text, kept for the record: Freedman–Lane on within-group normalised ranks (as decided) still over-rejects under the simulated nulls in which brand size drives all three measures (FL size at nominal 2.5%: 3.6% in the base case, 5.6% and 8.1% with strong and very strong size links, 2.6% with a weak one; §2.11); the same FL test on values not ranked holds size in the simulation. Options: **(a) keep as decided, with the stated limit in §2.3** (no clock restart); (b) compute `H_A2`'s partial on values centred within group (for example log shares) with Freedman–Lane, the rank version as sensitivity (restarts the 24 hours; real shares are skewed, which the simulation does not model); (c) keep ranks and raise the evidence bar for CONFIRMED (restarts the 24 hours). For Pablo or the coordinator; not decided by this lane.
