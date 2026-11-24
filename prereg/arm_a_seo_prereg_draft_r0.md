# AIAS™ — Pre-Registration, Arm A of "Does AI presence pay?": Google visibility, AI presence and sales (revision r0, draft for review)

**Study:** For the same brands, month by month, how Google organic visibility (DataForSEO Historical Rank Overview, US) relates to AIAS Presence and, where public figures exist, to US sales; and whether AI presence adds anything to sales once Google visibility is known. Arm A of the study family "Does AI presence pay?" (S&P lessons work order v1.2, section 3; project doc `claude/runner-sp-lessons-nov22.md`), from the study idea `claude/idea-seo-sales-ai-presence-nov21.md` (v1.1).
**Design:** Re-analysis of archived AI waves (no new model calls) joined to one paid pull of monthly Google-visibility history (Nov 2024 to the pull month) for about 276 brand websites in 12 measured categories, plus one small re-pull after the t₅ wave. Association only; no causal claim anywhere in the study or its paper.
**Budget:** DataForSEO spend at most US$50 for this arm (Pablo, Mon 2026-11-23, 10:02 pm US Central: "if I put $50, use $50 not $3"); expected $45.39 (§5). Hard stop at $48 cumulative (§5.4). Inside the programme rule of at most $100 of paid calls per paper.
**Programme position:** Study number TO CONFIRM (coordinator assigns). It moves no AIAS 6.0 date. Arm B (prospective, listed one-brand companies) is a separate pre-registration.
**Design rules:** S&P work order section 11a (outcome rates by band; the shape written in advance; pooled and within category; each brand once and weighted by size; data as it stood; stability before fit; a reversion baseline). Pablo's OK of 🔴 item (o) is TO CONFIRM; this draft follows 11a either way.
**Pre-registrant:** Pablo Ulpiano González Castro
**Status:** r0 draft, written 2026-11-23 (US Central) by a writing lane for the coordinator. Not locked. Nothing has been pulled for any study brand. The only DataForSEO calls so far are the coordinator's $1-credit feasibility test (§4.2) on two domains outside the study.
**Lock:** 24 hours after this draft reaches the pre-registrant unless he holds it (coordinator's brief). Note: the idea doc v1.1 says the lock comes "in January, with the S&P order's section 3"; which applies is TO CONFIRM (§11, D1). Pablo tops up the $50 only after the lock. No study domain is pulled before the lock.

---

## §1 Context

- The book's opening scene (tracker numbers up, sales flat, Google category queries down because people ask a chatbot) is a picture; no study of ours puts the three measures side by side for the same brands (idea doc, "Why").
- What exists: v0.25 (Presence and Google Trends search interest, rho 0.74, n 24, B2B software; Trends measures demand, not SEO); v0.26 (Presence and Amazon sales rank, rho about 0, n 88); v0.43 (June Presence against later change in search interest); AIAS Shift (AI recommendation share against 2025 US car sales by competitive group, `claude/shift-public-numbers-nov19.md`); #76 "From named to chosen". Gap: no real SEO measure in any study (idea doc, "What exists").
- Decided by Pablo on Mon 2026-11-23: measured over time, not as one snapshot ("Yes over time yes?", 8:06 am); source DataForSEO pay as you go ("Ok yes", 8:16 am); cars first, then airlines and banks; budget $50, used in full (10:02 pm).
- This draft widens the scope from cars to every measured category with brand websites that fits the $50 (Pablo's 10:02 pm decision as relayed by the coordinator), with the sales link where public sales or share data exist.

## §2 Pre-registered hypotheses

### §2.1 Definitions (used by every test)

- **Google visibility, primary measure `G`:** `metrics.organic.etv` (estimated organic traffic volume) for the brand's domain, per month, US (location_code 2840), English. Analysed as `g = ln(1 + etv)`.
- **Secondary Google measures:** `metrics.organic.count` (ranked keywords) and top-10 keywords `pos_1 + pos_2_3 + pos_4_10`, each as `ln(1 + x)`. `clickstream_etv` is a robustness measure only if it is non-null for at least 80% of domain-months (§6.3).
- **Window:** the mean of `g` over the three complete months ending with the month of the AI wave (e.g. a May 2026 wave uses Mar, Apr and May 2026). Robustness: the wave month alone, and the month before it.
- **Complete month:** any month before the pull month. The pull month is always excluded (the 2026-11-23 test returned a partial November 2026).
- **AIAS Presence `P`:** recall Presence π̂ as each source study's locked scorer computes it (omnibus: v1.8 protocol in the v0.41 scorer `osf/v41/scripts/score_v41.py`, and v0.42's scorer for t₄). For categories from studies before the omnibus, the study's own published per-brand Presence (file per category TO CONFIRM, §3.3).
- **AI recommendation share `R` (cars):** Shift's share of first-round mentions on the three recommendation questions (18 answers per brand at t₁), within the brand's competitive group (`claude/shift-public-numbers-nov19.md`; counts from the site's deposited `content/explorers.json`).
- **Sales share `S` (cars):** the brand's 2025 US units × average transaction price, as a share of its competitive group (Shift's figures and sources, same doc). Groups: luxury (7), mass market (7), electric-only (4) = 18 brands still sold.
- **Google share `Gs` (cars):** the brand's summed etv over Jan–Dec 2025, as a share of its competitive group.
- **Category-month demeaning:** for change analyses, each brand's Δg is taken minus the median Δg of its category over the same months (a category-month fixed effect), so a change common to all domains (an index or method break) drops out.
- **Each brand once:** a brand in more than one category counts once, in the category of its earliest study; a domain shared by two categories (on disk: fentybeauty.com and rarebeauty.com in v0.20 and v0.21) is pulled once.
- **Pooling:** within-category Spearman ρ_c, pooled as the Fisher-z mean weighted by n_c − 3, over categories with n_c ≥ 8 analysable brands. Every pooled figure is shown beside every within-category figure (11a.3).
- **Seeds:** permutation and bootstrap seeds are fixed at lock (proposed 610001 onward; TO CONFIRM that no other study uses them). 10,000 permutations; 10,000 bootstrap resamples within category.

### §2.2 PRIMARY 1: `H_A1_Google_AI` — brands with more Google visibility have more AI presence (all pulled categories)

- **Prediction:** within category, `P` at the category's AI wave rises with the window mean of `g` at that wave.
- **Statistic:** pooled ρ̄ (§2.1) over all analysable categories; one-sided permutation test (P permuted within category); 95% bootstrap CI.
- **CONFIRMED:** ρ̄ ≥ 0.30 and Holm-adjusted p < 0.05. **FALSIFIED:** the CI's upper bound < 0.30. **MARGINAL:** p < 0.05 but ρ̄ < 0.30. **UNDETERMINED:** otherwise, or fewer than 4 analysable categories.
- **Also reported (no separate verdict):** each ρ_c; the same test on `count` and top-10 keywords; size-weighted version (§2.6).

### §2.3 PRIMARY 2: `H_A2_AI_adds_to_Google` — AI recommendation share tracks 2025 sales once Google share is known (cars)

- **Prediction:** within competitive group, `R` (t₁) is positively associated with `S` after controlling for `Gs`.
- **Statistic:** the partial Spearman correlation of `R` with `S` given `Gs`, on within-group normalised ranks ((rank − 1)/(n_g − 1)), n = 18 brands still sold; one-sided permutation test, `R` permuted within group.
- **CONFIRMED:** partial ρ ≥ 0.30 and Holm-adjusted p < 0.05. **FALSIFIED:** partial ρ ≤ 0. **UNDETERMINED:** otherwise.
- **Power:** n = 18 gives low power. The power at true partial ρ of 0.3 and 0.5 is computed by simulation before lock and written here (TO CONFIRM; light job, no API). A null is reported as a null, not as absence of a link.
- **Headline pair (S&P format, §3 of the work order):** of the brands whose AI share exceeds their Google share within group, the share whose sales share exceeds their Google share, against the same share for the other brands, with its source line. Whatever the result.

### §2.4 SECONDARY 1: `H_A3_which_tracks_sales` — Google share and AI share against sales (cars)

- ρ(Gs, S) and ρ(R, S) on within-group ranks, and their difference with a 95% bootstrap CI (resampling brands within group). **Verdict rule:** "Google tracks sales better" or "AI tracks sales better" only if the CI of the difference excludes 0; otherwise "no difference detected".

### §2.5 SECONDARY 2: `H_A4_bands` — Google change by Presence band, with a reversion baseline (five omnibus categories; 11a.1, 11a.2, 11a.7)

- **Groups:** Presence terciles within category at t₁ (2026-05-25), named bottom, middle, top (thirds, not fifths, because n_c is 16–24). A brand keeps its t₁ band for the whole holding period; no brand enters or leaves during it (closed brands stay in, §3.4).
- **Lookback and holding period:** baseline window Mar–May 2026 (t₁); outcome window the last three complete months before the pull (expected Sep–Nov 2026). **Outcome:** category-month-demeaned Δg between the two windows.
- **Shape written in advance:** mean outcome bottom < middle < top. **Statistics:** Jonckheere–Terpstra test for an ordered rise (one-sided, permutation within category); top-minus-bottom spread with 95% bootstrap CI; hit rate = share of top-band brands whose outcome exceeds their category median.
- **Reversion baseline:** (a) the same spread when brands are banded by their own pre-period Google level (mean g, Nov 2024–Feb 2026) instead of Presence: what level and reversion alone give; (b) a placebo on the past: t₁ Presence bands against Δg from Nov 2024–Jan 2025 to Mar–May 2026, which t₁ Presence cannot have caused.
- **SUPPORTED:** ordered rise with Holm-adjusted p < 0.05, spread CI above 0, and the Presence-band spread larger than baseline (a)'s, with the bootstrap CI of the difference above 0. **PARTIAL:** the rise is significant but the best band is not the top one, or the spread does not beat baseline (a) (never CONFIRMED in either case). **NOT SUPPORTED:** otherwise. A placebo (b) spread with its CI above 0 is reported as a sign of a standing trend, and the forward result is then labelled "not distinguishable from trend".

### §2.6 SECONDARY 3: `H_A5_co_movement` — within-brand change (five omnibus categories, same six-model panel t₁ → t₃)

- Spearman within category between ΔP (t₃ 2026-11-09 minus t₁) and category-month-demeaned Δg (window at t₃ minus window at t₁; the t₃ window is Sep–Nov 2026 if November is complete at the pull, otherwise Aug–Oct 2026), pooled as in §2.1. **SUPPORTED:** pooled ρ̄ > 0 with Holm-adjusted p < 0.05; otherwise NOT SUPPORTED. Stated limit: Presence held at ρ 0.93–0.98 from t₂ to t₃ (v0.42 pre-registration §1), so ΔP has little spread and power is low.
- **Size weighting (11a.4, applies to §2.2–§2.6):** the primary result is equal-weighted (each brand once). Also reported: weighted by 2025 sales where a sales figure exists (cars), otherwise by the brand's pre-period mean etv. Both are shown; the equal-weighted figure decides the verdict.

### §2.7 SECONDARY 4: `H_A6_other_sales` — the same tests in the other sales-link categories

- Airlines (US), retail banks (US), B2B software, project-management software, personal finance apps, premium spirits: ρ(g, sales measure), ρ(P, sales measure) and the partial of P given g, within category. This test is confirmatory only for categories whose sales measure, year and source file are fixed in this document before lock (§3.3; candidates: airline passenger or revenue share from US DOT, bank deposits from the FDIC, reported revenue for listed software companies from SEC filings, US 9-liter cases for the five spirits brands with published figures in the Shift doc). A category without a fixed source at lock moves to the exploratory list. SUPPORTED per category: partial ρ > 0 with Holm-adjusted p < 0.05.

### §2.8 Multiple testing

- **Primary family** (`H_A1`, `H_A2`): Holm, family-wise α = 0.05.
- **Secondary family** (`H_A3` difference test, `H_A4` ordered-rise test, `H_A5`, each confirmatory category of `H_A6`): Holm, α = 0.05, separately from the primary family.
- Robustness, sensitivity and exploratory analyses carry no verdict and no adjustment, and are labelled as such wherever shown.

### §2.9 Exploratory (labelled, no verdicts)

- AI intensity (work order 11b.7): `R`/`S` per car brand; whether brands with intensity above 1 gained Google share later (Δ`Gs`, 2025 to the last complete months).
- t₄ (v0.42, new panel) and t₅ (v0.45) Presence against g, once both waves are scored.
- Lead and lag: ρ between P at each wave and g in each month from six months before to six months after.
- Presence × Consistency grid (11b.3) against g.

### §2.10 What counts as support or failure, in one line

- Arm A supports "AI presence pays" only if `H_A2` is CONFIRMED. `H_A1` alone shows that AI and Google visibility go together, which brand size can explain; it is not evidence that AI presence pays. A FALSIFIED `H_A2` is the headline whatever `H_A1` shows.

---

## §3 Brands, domains and AI waves

### §3.1 Sources on disk (read 2026-11-23)

- **Brand master v1.0 (DRAFT):** `registries/master/brand_master_v1.0.json` and `category_list_v1.0.json`, `coverage_grid_v1.0.csv` on branch `sp7-category-brand-master` (worktree `_worktrees/sp7-category-brand-master`, commit 94c7bcf). 678 brand IDs, 28 categories (20 measured, 8 registered for v0.44). **It has no website-domain field**; only 77 records carry a `domain_status` inside `wikidata_on_disk`.
- **Domains on disk:** `osf/methodology/v1_13/registries/brand_domains_v1_13.csv` (branch `v1.13`, last change a8680f3, 2026-11-10): the five omnibus registries (112 brand units): 107 RESOLVED, 5 NONE (Pontiac, Oldsmobile, Plymouth, Mercury, Saturn), each with a dated Wikidata P856 source under rule R1. Two domains appear in two registries (fentybeauty.com, rarebeauty.com), so 105 unique domains.
- **Every other category has no domain on disk.** Resolving them is a pre-lock task (§3.3) under the same rule R1, with no paid API.

### §3.2 Categories and brand counts

Eligible = brand-master IDs in the category, not `alternate_only`, status not closed, merged or renamed. "Domains" = resolved domains on disk.

| Pri. | Category (brand master ID) | Source study | Master IDs | Eligible | Domains on disk | Sales link | Pull |
|---|---|---|---|---|---|---|---|
| 1 | Passenger cars (CAT-1012) | v0.22 omnibus | 24 | 19 | 19 (+5 NONE) | 2025 US units × price, 18 still sold (Shift) | yes |
| 2 | Premium spirits (CAT-1009) | v0.23 omnibus | 24 | 24 | 24 | US cases for 5 brands (Shift doc) | yes |
| 2 | Audiophile headphones (CAT-1011) | v0.19 omnibus | 16 | 15 (+Denon, COI flag) | 16 | none | yes |
| 2 | Facial skincare (CAT-1001) | v0.20 omnibus | 54 | 42 | 24 (omnibus units) | none | omnibus 24 only |
| 2 | Cosmetics (CAT-1002) | v0.21 omnibus | 32 | 24 | 24 | none | yes |
| 3 | Airlines, US (CAT-1019) | v0.40 | 18 | 11 | 0 | US DOT share (TO CONFIRM) | yes |
| 3 | Retail banks, US (CAT-1018) | v0.40 | 41 | 26 | 0 | FDIC deposits (TO CONFIRM) | yes |
| 3 | B2B software (CAT-1017) | v0.24 / v0.25 | 24 | 19 | 0 | SEC revenue where listed (TO CONFIRM) | yes |
| 3 | Project-management software (CAT-1015) | v0.6, v0.9 | 19 | 19 | 0 | SEC revenue where listed (TO CONFIRM) | yes |
| 3 | Personal finance apps (CAT-1016) | v0.6, v0.9, v0.10 | 16 | 16 | 0 | TO CONFIRM | yes |
| 4 | Kitchen knives (CAT-1004) | v0.8, v0.16, v0.26 | 53 | 53 | 0 | none | yes |
| 4 | Running shoes (CAT-1010) | v0.6, v0.9 | 17 | 17 | 0 | none | yes |

**Planned pull (domains):** priority 1: 19; priority 2: 86 unique (88 brand units); priority 3: up to 91; priority 4: up to 70; up to 10 extra US-site domains (§3.3) → **up to 276 domains**. Priority 3 and 4 counts are eligible brand IDs; the domain count falls where rule R1 finds no domain (closed banks and airlines are likely), TO CONFIRM after resolution.

**Not pulled (default; open decision D3):**
- Technology brands (CAT-1020, v0.28, 24 IDs): excluded under the COI rule. The list includes Apple and Google (phones), Whirlpool (appliances), Corning (displays) and Lam Research (semiconductors), categories covered by the conflict-of-interest screen (Declarations §COI), and the category has no common sales measure.
- Fragrance (24), home coffee roasters (30), commercial coffee roasters (36), premium tea (31), premium olive oil (20), household goods retail (21), premium cookware (4 eligible): outside the $50 after priorities 1–4. Fragrance carries the Ellis Brooklyn COI note and cookware the Hestan note; neither is pulled.
- The eight v0.44 industries (registered; collection starts 2026-11-24 00:05 US Central): not measured at lock. Candidates for a later arm.

### §3.3 Pre-lock tasks (no paid API; all fixed before lock)

1. **Domains for priorities 3–4:** resolve under v1.13 rule R1 (Wikidata P856 official website, dated source), recorded in `osf/arm_a/registries/arm_a_domains_r1.csv` (path TO CONFIRM) with brand-master ID, domain, status (RESOLVED, NONE, UNRESOLVED), source and access date.
2. **US site rule:** the study measures US Google results, but rule R1 gives the global official site. Where a brand's US consumer site is a separate domain (a possibility for global car and beauty brands; each case TO CONFIRM), both are listed; the **US domain is primary** and the R1 domain is a sensitivity. At most 10 such extra domains are pulled, in priority order.
3. **Independent check (no manual checks by Pablo):** a model of a provider other than the resolver's, blind to its output, resolves the same list; agreement % reported; on disagreement the domain is UNRESOLVED and not pulled (no human tiebreak). Model, cost and cap TO CONFIRM before lock; the cost counts toward the $100 per-paper cap, not the $50 DataForSEO cap. Limit stated: no human check.
4. **Presence files per category:** the per-brand Presence file, study and wave date for every priority 3–4 category (TO CONFIRM; v0.40 for airlines and banks only if scored before lock).
5. **Sales sources (§2.7):** source, year and file for each sales-link category other than cars, or the category moves to exploratory.
6. **Domain test for subdomains:** whether `historical_rank_overview` counts subdomains of the target (TO CONFIRM from DataForSEO's documentation; no paid call).

### §3.4 Archived car (and omnibus) AI waves on disk

Read from the answer files on 2026-11-23 (dates from each file's `timestamp` column). All 24 car brand units are present in every wave, the five closed brands included.

| Wave | Study | Date (UTC) | Models | Car brands | File |
|---|---|---|---|---|---|
| t₁ | v0.22 | 2026-05-25 | claude-opus-4-5, claude-sonnet-4-5, gemini-2.5-flash, gemini-2.5-flash-lite, gpt-4o, gpt-4o-mini | 24 | `osf/v22/phase_a_results.csv`, `phase_b_results.csv` |
| (version study) | v0.32 | 2026-06-05 | panel A: the t₁ six as dated snapshots (claude-opus-4-5-20251101, claude-sonnet-4-5-20250929, gpt-4o-2024-11-20, gpt-4o-mini-2024-07-18, gemini-2.5-flash, gemini-2.5-flash-lite); panel B: claude-opus-4-8, claude-sonnet-4-6, gpt-5.5-2026-04-23, gpt-5.4-mini-2026-03-17, gemini-3.5-flash, gemini-3.1-flash-lite | 24 | `osf/v32/data/phase_a_A.csv`, `phase_a_B.csv` |
| t₂ | v0.34 | 2026-06-10 | the t₁ six | 24 | `osf/v34/data/v22/phase_a_results.csv` |
| t₃ | v0.41 | 2026-11-09 | the t₁ six | 24 | `osf/v41/data/v22/phase_a_results.csv` (in worktree `aias-6.0-preview-paper`) |
| t₄ | v0.42 | collection log 2026-11-11 to 2026-11-14 (exact window TO CONFIRM from `t4_batches.jsonl`) | claude-fable-5-2, gpt-6-astra, gemini-4-argon (served IDs as requested) | 24 | `osf/v42/data/t4_raw.jsonl` (worktree `t4-paper`) |
| t₅ | v0.45 | planned 2026-12-03 to 2026-12-06 (pre-registration header) | t₄'s three | 24 | not yet collected |

- The same five omnibus categories (v0.19–v0.23, 112 brand units) are in each wave above. The coverage grid lists v0.42 for cars.
- `H_A2` and `H_A3` use t₁ (Shift's `R`). `H_A4` uses t₁ bands. `H_A5` uses t₁ → t₃ (same panel). t₄ and t₅ are exploratory (§2.9) because the panel changed.
- Problem found: the repo's `main` branch (c79f4f5, "merge v0.20 ship artifacts") does not carry osf/v41 onward; the analysis code must read the files at their locked tags (tag names TO CONFIRM), never from a working tree.

---

## §4 Google-visibility data

### §4.1 Request (fixed)

- Endpoint `POST /v3/dataforseo_labs/google/historical_rank_overview/live`; one task per request: `target` = the domain (no scheme, no `www.`), `location_code` 2840 (United States), `language_code` "en", `date_from` "2024-11-01". No other parameter.
- Why `date_from`: without it the endpoint returned only 6 months (Jun–Nov 2026); with "2024-11-01" it returned 25 monthly items, Nov 2024–Nov 2026 (§4.2). Nov 2024 covers every AI wave on disk (first: 2026-05-25) with an 18-month pre-period. Whether earlier months exist is TO CONFIRM from the documentation (open decision D5; default: keep 2024-11-01, the tested value).

### §4.2 Feasibility test (coordinator, Mon 2026-11-23 about 10:05 pm US Central; free $1 credit)

- Raw JSON: `_worktrees/_runner_tmp/dataforseo_test/` (`hro_allrecipes.com_20261124T040421Z.json`, `hro_nasa.gov_20261124T040421Z.json`, `hro_datefrom_allrecipes.com_20261124T040453Z.json`, scripts `hro_test.py`, `hro_test_datefrom.py`). Test domains allrecipes.com and nasa.gov are not in the study.
- Status "Ok." on all three. Cost $0.1272 per request for 6 months and $0.15 for 25 months, i.e. $0.12 + $0.0012 per month returned. Total test spend $0.4044.
- Per-month fields under `metrics.organic`: `pos_1`, `pos_2_3`, `pos_4_10`, `pos_11_20` … `pos_91_100`, `etv`, `count`, `estimated_paid_traffic_cost`, `is_new`, `is_up`, `is_down`, `is_lost`, `clickstream_etv`, `clickstream_gender_distribution`, `clickstream_age_distribution`.
- The pull month (Nov 2026) was partial. Visible level shifts (allrecipes.com etv 10.3M in Nov 2024, 67.5M in Dec 2024) suggest index or method breaks in the series (§6.2).
- Checked by this draft's writer on 2026-11-23 from the saved JSON: allrecipes.com etv 10,274,478 (Nov 2024), 67,467,793 (Dec 2024), 46,649,775 (Jan 2025), 13,097,337 (Oct 2026), 13,482,009 (Nov 2026, partial). `clickstream_etv` is null in these months, so it is not expected to be usable (§2.1).

---

## §5 Budget and spending rules

### §5.1 Prices (DataForSEO, checked 2026-11-23; re-check at lock)

$0.12 per request plus $0.0012 per month returned (idea doc, "Decided", and the test in §4.2). $50 minimum top-up; funds stay on the balance until spent. Pay as you go, no subscription.

### §5.2 Allocation and expected cost

| Pull | When | Domains | Months per request | Cost per domain | Expected |
|---|---|---|---|---|---|
| Main | after lock and top-up; expected December 2026 | up to 276 (§3.2) | 26 (Nov 2024–Dec 2026, the last partial) | $0.1512 | **$41.73** |
| Re-pull | after t₅ (v0.45, Dec 3–6), once December is complete: January 2027 | 24: the 19 car domains and the 5 spirits brands with published US cases | 27 (Nov 2024–Jan 2027) | $0.1524 | **$3.66** |
| Total | | | | | **$45.39** |

- If the main pull runs in November 2026 instead (25 months), it costs $41.40.
- The re-pull repeats the full history on purpose: it shows whether DataForSEO restated past months (11a.5, data as it stood), and it adds the t₅ month for exploratory use.
- Design trade-off: the price is mostly per request ($0.12), not per month, so the budget buys domains, not history. Pulling the remaining 166 eligible brands of the seven unpulled categories would add about $25 and break the $50 cap; priorities 1–4 keep every category with a sales link and the five omnibus categories (several AI waves), plus kitchen knives (the measured category with the most models, 11) and running shoes (two waves, v0.6 and v0.9), which fit under the limit.

### §5.3 Pull order (fixed in advance)

Priority 1 (cars) → priority 2 (spirits, headphones, skincare, cosmetics) → priority 3 (airlines, banks, B2B software, project-management software, finance apps) → priority 4 (kitchen knives, running shoes) → the US-site extras (§3.3, item 2) in the same category order. Within a category, brands in brand-master ID order. A category is pulled whole or not at all: before starting a category, the script checks that its full cost fits under the limit in §5.4; if not, it stops there.

### §5.4 Spending limits (computed from the `cost` field of every response, summed)

- **Main pull limit $43.00.** The script does not start a category whose expected cost would take the cumulative spend above $43.00.
- **Hard stop $48.00 cumulative** (main pull + re-pull + any retry), checked before every request; the $50 balance is never fully drawn, leaving room for price differences.
- **Price check:** if any single request costs more than $0.20, or its `cost` differs from $0.12 + $0.0012 × months returned by more than $0.005, the pull stops and the case goes to Pablo.
- **Retries:** a failed request (a `status_message` other than "Ok.", as in the test responses, or no items) is retried once after 60 s; its cost counts. A domain that fails twice is recorded as `PULL_FAILED` and excluded (§6.4).
- No pull runs beside another paid collection on the same Mac (programme rule: one paid collection at a time).
- Any spend beyond $50 needs Pablo's go; any study-wide total beyond $100 per paper is never reached by this arm.

---

## §6 Analysis plan

### §6.1 Data as it stood (11a.5)

- Each response is saved exactly as returned, one file per request, `osf/arm_a/data/raw/hro_{domain}_{UTC timestamp}.json` (path TO CONFIRM), never edited or overwritten; the re-pull goes to its own folder.
- A manifest row per request: brand-master ID, domain, request body, HTTP status, `status_message`, `cost`, months returned, pull time (UTC) and SHA-256 of the file. The manifest is committed the day of the pull.
- The API key lives on the Mac outside the repo (as the OSF token does) and is never written to any file in the repo or the deposit.
- The brand list is the list as it stood at each AI wave, closures included: Fisker (bankrupt 2024, domain on disk) is pulled and kept, labelled closed, in `H_A1`, `H_A4` and `H_A5`; it has no 2025 sales and is outside `H_A2`/`H_A3`. The five NONE car brands have no domain and are counted as excluded.
- Restatement: for months in both pulls, the share of domain-months whose etv changed by more than 1% is reported. Every analysis uses the main pull; the re-pull's values are a sensitivity only.

### §6.2 Index or method breaks (rule fixed before any data)

- For each month m, compute the median over all pulled domains of Δg(m) = g(m) − g(m−1), and the share of domains with |Δg| > 0.2 moving in the same direction.
- **A month is flagged as a break** if |median Δg| > 0.40, or if at least 80% of domains move by more than 0.2 in the same direction. Flags are computed once, from the main pull, before any AIAS variable is joined, and written to the manifest.
- Handling: (1) cross-sectional tests (`H_A1`, `H_A2`, `H_A3`) compare brands within the same category and month, so a common multiplicative shift does not change ranks; (2) change tests (`H_A4`, `H_A5`) use category-month demeaning (§2.1); (3) robustness: every test is re-run with flagged months dropped from every window, each window then using the three nearest unflagged complete months at or before the wave; (4) a figure of the monthly median g with flagged months marked goes in the paper.

### §6.3 Joining AI and Google data

- **The category's AI wave** for `H_A1`: t₁ (2026-05-25) for the five omnibus categories; for every other category its latest study with per-brand Presence on disk (study and date fixed in §3.3, item 4). A category whose wave falls before Feb 2025 has no full window and is excluded from `H_A1` (none expected; TO CONFIRM dates of v0.6, v0.8, v0.9, v0.10, v0.16, v0.24, v0.26).
- Joins are by brand-master ID only, never by name. The join script and its unit tests are written and frozen before lock; they are run first on simulated Google data of the right shape, never on real data, before lock.
- Stability before fit (11a.6): no threshold, window or transformation is tuned on the data. Every result is reported for the pre-registered choice first; robustness rows follow.

### §6.4 Exclusions and missing data (counted and listed in the paper)

- No domain (NONE or UNRESOLVED), `PULL_FAILED`, or a domain shared by two brands of the same category (both excluded from that category's tests).
- A domain with etv = 0 or missing in more than half of the months of a test's windows is excluded from that test.
- A category with fewer than 8 analysable brands is shown but not pooled.
- No imputation. A missing month inside a window: the window mean uses the remaining months if at least 2 of 3 are present; otherwise the brand is excluded from that test.

### §6.5 COI screen (pre-registered; DEVIATIONS Entry 0 at lock)

- The employer's categories are out: technology brands (CAT-1020) are not pulled; no phones, TVs, appliances, semiconductors or displays enter any test.
- The brand master flags one brand, Denon (BR-00303, v0.19), under the conflict-of-interest screen (Declarations §COI). It is pulled and handled as in v0.62: kept, with every result also reported without it (sensitivity S-COI).
- S-COI also drops the five omnibus brands for which Cheil Worldwide or its Iris unit has worked: Chevrolet, BMW, Bentley, Jack Daniel's, Eucerin (v0.62 DEVIATIONS Entry 0, Part F).
- Entry 0 for priority 3–4 categories (airlines, banks, software, finance apps, knives, running shoes) has not been run; it is a pre-lock task (TO CONFIRM). A brand it flags is handled like Denon unless Pablo decides otherwise.

### §6.6 Reporting

- Every page says: association only; these data cannot show that AI presence causes sales or Google visibility, or the reverse.
- Each hypothesis with its verdict word, statistic, CI, p (raw and Holm-adjusted) and n; pooled beside within-category (and, for cars, within competitive group); equal-weighted beside size-weighted; with and without S-COI; with and without flagged months.
- Band results as outcome rates by band (11a.1): mean outcome, hit rate and n per band, with the reversion baselines beside them.
- The headline is one plain pair of numbers with its source line (§2.3), null included.
- Uncertainty is always reported (the S&P reports' lack of intervals is not copied).

---

## §7 Limitations (stated up front)

- One sales year (2025) and n = 18 car brands: a first look with low power.
- DataForSEO's etv is DataForSEO's own estimate (its method per the documentation, TO CONFIRM), not Google's figures; breaks in its index (§6.2) are handled by rule, not removed.
- A brand's domain is not the brand: dealer, retailer, marketplace and review sites carry much of a brand's search demand, and multi-brand or global sites mix countries.
- Brand size drives all three measures; `H_A2` controls for Google share but not for advertising, distribution or price.
- The AI waves come from a retiring 2024–25 panel (t₁–t₃) and one new panel (t₄); answers are to set questions, not to real buyers' prompts.
- Showing that AI takes over from search needs further waves and a search-volume trend (idea doc, "Limits"); this arm does not claim it.

---

## §8 Declarations

**Conflict of interest.** The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-analyses archived AI answers against brand registries fixed in earlier phases and adds no new brand selection beyond the category choice in §3.2; each registry carries its source-phase conflict-of-interest handling forward unchanged, and the technology-brands category is left out because it includes Samsung's categories. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands — Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) — characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry, AKG was substituted with Denon before the v0.19 pre-registration lock (AKG is owned by Harman International, a Samsung subsidiary since March 2017; deal agreed November 2016) to avoid the appearance of conflict (v0.19 pre-registration §2.3; v0.19 DEVIATIONS Entry 1); Harman completed its acquisition of Masimo's Sound United brands, Denon included, on September 23, 2025, so Denon was already a Samsung-group brand; it is kept and every result is also reported without it. Samsung's agency Cheil Worldwide, or its Iris unit, has worked for five registry brands (Chevrolet, BMW, Bentley, Jack Daniel's, Eucerin; v0.62 DEVIATIONS Entry 0, Part F); results are also reported without them. TO CONFIRM: the COI text conformed verbatim to the source records before lock (CLAUDE.md rule: conform from the locked record, not memory).

**Funding.** Self-funded. Google-visibility data bought from DataForSEO (pay as you go), at most US$50.

**Ethics.** Not applicable; no human subjects.

**Use of AI tools.** During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

---

## §9 Lock procedure and change log

- **r0 draft** goes to the pre-registrant through the coordinator. It locks 24 hours after it reaches him unless he holds it (D1).
- **Before lock:** the pre-lock tasks of §3.3 and §6.5 are done and written into r1; every TO CONFIRM in §10 is closed or its default applied. Any change to a hypothesis, threshold, category list, pull order or spending limit after r1 reaches him restarts the 24 hours.
- **Lock:** a lock manifest (SHA-256 of this file, the domain list, the join and analysis scripts and their tests, the pull script); commit; tag (name TO CONFIRM, e.g. `arm-a-prereg-r1`); the coordinator pushes and deposits at OSF. Only then does Pablo add the $50, and only then may the pull script run.
- **After lock:** a locked pre-registration never changes; any change is a dated DEVIATIONS entry, and any new idea is a labelled exploratory analysis.

**Change log**

- 2026-11-23, r0: first draft, from the idea doc v1.1, the S&P work order v1.2 (§3, §11a), the brand master v1.0 draft (94c7bcf), `brand_domains_v1_13.csv` (a8680f3), the archived wave files and the coordinator's DataForSEO test of 2026-11-23. No study domain pulled.

---

## §10 Open items

### §10.1 TO CONFIRM (what is needed)

1. Study number and tag name (coordinator).
2. Lock timing: 24 h after this draft (coordinator's brief) or January with the S&P order's §3 (idea doc v1.1) (Pablo).
3. Pablo's OK of 🔴 (o), section 11a's design rules (Pablo; this draft follows them).
4. Domains for priority 3–4 categories under rule R1 and the independent check, with that check's model and cost (§3.3, items 1 and 3).
5. US-site domains for brands whose R1 domain is global (§3.3, item 2).
6. Per-brand Presence file, study and wave date for each priority 3–4 category (§3.3, item 4; §6.3).
7. Sales sources (measure, year, file) for airlines, banks, software and finance apps (§2.7).
8. Whether the endpoint counts subdomains, and how far back history goes (DataForSEO documentation, no paid call).
9. Exact t₄ collection window from `t4_batches.jsonl`, and the locked tags from which every wave file is read.
10. Power of `H_A2` by simulation (light job, no API).
11. COI Entry 0 for the priority 3–4 categories, and the COI text conformed to the source records.
12. Seeds not used elsewhere (§2.1).

### §10.2 Open decisions (recommended default in bold)

- **D1 Lock timing.** **24 hours after this draft reaches Pablo** (the pull is small and independent of the main path); alternative: January with arm B.
- **D2 Scope.** **Priorities 1–4, up to 276 domains, $45.39 expected**; alternative: cars only (19 domains, about $3), as in the idea doc's first estimate.
- **D3 Unpulled categories.** **Leave out technology brands (COI) and the seven lower-priority categories**; alternative: swap running shoes (17) for commercial coffee roasters (36, nine models), which adds about $2.87 and takes the expected total to $48.26, above the $48 hard stop, so it works only without the re-pull (D4).
- **D4 Re-pull.** **January 2027, the 19 car domains and 5 spirits domains, full history ($3.66)**; alternative: no re-pull, keeping $5 unspent.
- **D5 History start.** **`date_from` 2024-11-01 (tested)**; alternative: an earlier start if the documentation shows more history (adds $0.0012 per month per domain).
- **D6 Primary Google measure.** **etv**; alternative: ranked-keyword count, which does not depend on DataForSEO's click model.
- **D7 Denon and Cheil-linked brands.** **Kept, with S-COI reported beside every result (as v0.62)**; alternative: drop them from the primary results.
- **D8 v0.44 industries.** **Not in this arm**; alternative: add them to the re-pull once v0.44 is scored, as a later arm with its own lock.
- **D9 File location.** **`prereg/arm_a_seo_prereg_draft_r0.md` on branch `arma-seo-prereg`**, moving to `osf/<study>/prereg/PRE_REGISTRATION_<study>.md` (the v0.42 pattern) once the study number is set.
