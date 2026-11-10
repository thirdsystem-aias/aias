# AIAS™ Presence Measurement Protocol — Pre-Registration v0.44 (revision r1, DRAFT for the pre-registrant)

Pablo Ulpiano González Castro
School of Visual Arts, MPS Branding Program, New York, NY (primary academic affiliation)
Third System™ (research entity; data archive and methodology venue)
Correspondence: pablou@pablou.com · pablou.com
ORCID: 0009-0003-8968-9990 (linked: https://orcid.org/0009-0003-8968-9990)

**Study:** The industry-breadth wave — AI availability of brands in eight industries the programme has not measured, on the newest models.
**Design:** 159 brand units in eight US-market industries (car insurance, hotel chains, grocery store chains, fast-food chains, clothing and department stores, pharmacies, convenience stores and gas stations, fashion and luxury), each built from dated public rankings by a fixed tier rule (§3). The newest generally available flagship of each of three providers (N3: Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon) answers the 48 category questions (Phase B, six per industry) three times each and the 159 brand questions (Phase A) once, without web search (S0): 3 × (48 × 3 + 159) = **909 calls**.
**Budget:** at most US$100 of paid model calls, hard cap; pause at $80; both computed from actual recorded usage (programme rule, 2026-11-10). **Estimate $27.24 central, $52.44 high** at the prices that apply in the collection window (Gemini 4 Argon at its November price); **$30.10 central, $59.00 high** if the collection slips past 2026-11-30 and Gemini 4 Argon bills at its December price (§4.5). Both are below the $80 pause.
**Protocol version:** Presence v1.6 (recognition from Phase A, recall from Phase B; SSRN 6816340); Consistency φ v1.8 (SSRN 6963359) scaled as C_φ per v1.9 (SSRN 7685126); call settings of the t₄ wave (v0.42 r2 §4.4, S0).
**Pre-registrant:** Pablo Ulpiano González Castro
**Status:** r1 draft, written 2026-11-10 by the programme runner. r0 (same day) set the design; r1 adds the acquisition, coding and scoring scripts with their tests, the exact commands, the re-priced budget, the collection window and its guards, the option to drop pharmacies before the lock, and the changes listed in §9. No study probe has been sent and none will be before the lock.
**Lock target:** git tag `v0.44-prereg-r1` on branch `v0.44`, pushed to `origin`; external anchor: deposit of this file, the registries, the probe file, the cost estimate, DEVIATIONS.md, the scripts and tests, the P1 record and the lock manifest at OSF `ec6wh` → `v44/prereg/` and `v44/anchor/` before the first call (§9). Locks 24 hours after the pre-registrant receives it, unless he objects (§9).
**Collection window:** 2026-11-24 to 2026-11-28 (US Central), all calls within 72 hours of the first (§4.6). The collection machine runs one paid collection at a time and is booked by other programme collections from 2026-11-11 to 2026-11-23 (v0.40's collection, 2026-11-17 to 2026-11-21, included); 2026-11-24 is the first free slot after the lock.
**Paper:** January 2027.

---

## §1 Context and question

Through v0.41 the programme measured AI availability in seventeen industries: kitchen knives, kitchenware, tea, olive oil, fragrance, skincare, cosmetics, headphones, running shoes, cars, spirits, coffee roasters, B2B and project software, tech brands, finance apps, airlines and retail banks. Its two locked components were established on five of them (the v0.19–v0.23 omnibus, 112 brands): Presence separates brands within a category and holds its order over five months (v0.41), and Consistency is separable from Presence (v1.8; v1.9 Stage 2, ρ = 0.189, n = 54). Every one of those results rests on consumer-product categories, mostly premium goods, and on the retiring six-model panel.

Industry-breadth rule (pre-registrant, 2026-11-09): prefer industries the programme has not measured. This wave asks whether the two components behave the same way in service and retail industries, on the newest models:

1. **Spread.** Does Presence separate brands within each new industry, as it did in four of the five omnibus categories?
2. **Market position.** Do brands that lead their industry on public market measures have higher Presence than its challengers and smaller brands?
3. **Separation.** Is Consistency still separable from Presence across the new industries?

It is a breadth wave, not a longitudinal one: one collection, three primary tests, descriptives. Its answers are also the first Presence and Consistency scores of these industries on N3, which later waves (Ranking, Sentiment, Coverage, Grounding papers) may reuse under their own pre-registrations.

---

## §2 Pre-registered hypotheses

### §2.1 Definitions

- **Units.** The rows of the registries (§3): 159 in eight industries (143 in seven if pharmacies are dropped before the lock, §3.4). Tier ∈ {L, C, S, G}; G (ghost) units are brands that left the US market (Esurance, A&P, Rite Aid) and are excluded from `H_Spread` and `H_Tier`; n = 156 non-ghost units (141 without pharmacies).
- **k_{b,m,r}.** Number of the six Phase B questions of b's industry in which model m's answer in run r mentions b (§5.1); 0–6.
- **Recall Presence.** π̂_b = Σ_m Σ_r k_{b,m,r} ÷ (6 · 3 · 3), over the answered calls (§5.4); 0–1.
- **Recognition.** Phase A answer coded yes / no / ambiguous by the certified v0.22 parser (`run_acquisition_v22.parse_yes_no`); one run per model.
- **Consistency.** Per run r, φ_{b,r} = [1/(M − 1)] · Σ_m (k_{b,m,r} − 6π̂_{b,r})² ÷ [6π̂_{b,r}(1 − π̂_{b,r})], with M = 3 and π̂_{b,r} the run's recall rate, the locked v1.8 partitions (π̂ = 0 → zero; π̂ = 1 → saturated; otherwise defined) and the v0.41/v0.42 kernel. φ_b = mean of φ_{b,r} over runs whose partition is defined; undefined if fewer than 2 of the 3 runs are defined.
- **Scaled Consistency.** C_φ = 100 · (1 − φ_b ÷ φ_max), φ_max = 6M ÷ (M − 1), the largest value φ can take on M models. For M = 6 this is 7.2 and the formula is v1.9's locked C_φ = 100(1 − φ/7.2); for N3 (M = 3) φ_max = 9. A brand is **rated** if φ_b is defined and its total mentions are at least 9 of 54 model-run-question cells (π̂_b ≥ 1/6, v1.9's floor of 6 of 36 in proportion). Declared adaptation of v1.9 to a three-model panel.
- **ρ_pw(x, y).** Pooled within-industry Spearman: values ranked within industry (average ranks for ties; values rounded to 10 decimals before ranking so that floating-point noise does not split ties), each industry's ranks centred on their industry mean, Pearson's r of the centred ranks pooled across industries. *(r1: the centring is new, §9 C2. Without it, industries of different sizes add a between-industry term to both variables: on the 156 H_Tier units the uncentred statistic has a null mean of +0.056 instead of 0, and the "identical up to sign" property of §2.4 fails. With equal industry sizes the two statistics are identical.)*
- **Permutation p.** One-sided unless stated; y shuffled within industry; ρ_pw recomputed on each draw; 10,000 draws; p = (1 + #{ρ_perm ≥ ρ_obs}) ÷ 10,001.
- **Bootstrap.** Units resampled with replacement within industry; 10,000 resamples; percentile 95% interval.
- **Seeds.** 440041 (`H_Spread` descriptive intervals), 440042 (`H_Tier`), 440043 (`H_Separation`), 440045 (descriptives).
- **α.** 0.05 per test; no multiplicity correction; verdicts rest on the pre-set thresholds; every test is reported.

### §2.2 PRIMARY: `H_Spread` — Presence separates brands within each new industry

**Statement.** In most of the new industries, recall Presence on N3 varies across the industry's brands well beyond run-to-run noise.

**Operationalisation.** For each industry i, SD_i = the population standard deviation of π̂_b over its non-ghost units. Industry i shows spread if SD_i ≥ 0.15.

**Verdict rule.** With I industries: CONFIRMED if at least ⌊0.8 · I⌋ show spread · FALSIFIED if fewer than half do (at most ⌈I/2⌉ − 1) · MARGINAL otherwise. For the eight industries: CONFIRMED if 6 or more, FALSIFIED if 3 or fewer, MARGINAL if 4 or 5 (unchanged from r0). If pharmacies are dropped before the lock (§3.4), I = 7: CONFIRMED if 5 or more, FALSIFIED if 3 or fewer, MARGINAL if 4.

**Rationale.** On the omnibus at t₃ (L6, one run; `osf/v41/v41_three_wave_table.csv`, computed 2026-11-10) SD was 0.267 (headphones), 0.328 (skincare), 0.252 (cosmetics), 0.261 (cars) and 0.101 (spirits): four of five at or above 0.15. With 54 cells per brand, a brand with a true rate of 0.25 has a sampling SD of about 0.06, so 0.15 is about 2.5 times the noise. The confirmation count is the omnibus rate (four of five, 0.8) times I, rounded down: 6 of 8 (r0's rule), 5 of 7.

**Reported alongside.** SD_i with its bootstrap interval (seed 440041), range, share of units at π̂ = 0, per industry and per model; the same statistic on the omnibus for N3 at t₄ if v0.42 is scored by then (descriptive only).

### §2.3 PRIMARY: `H_Tier` — Presence follows public market position

**Statement.** Within industries, leaders (L) have higher Presence than challengers (C), and challengers than smaller brands (S).

**Operationalisation.** x = tier score (L = 3, C = 2, S = 1); y = π̂_b; n = 156 non-ghost units (141 without pharmacies).

**Test.** ρ_tier = ρ_pw(x, y); one-sided permutation p (seed 440042); bootstrap interval.

**Verdict rule.** CONFIRMED if ρ_tier ≥ 0.40 and p < 0.05 · FALSIFIED if ρ_tier < 0.20 · MARGINAL otherwise.

**Rationale.** Presence correlated with Google search interest at 0.74 within B2B software (v0.25, n = 24). Tier is a coarse three-level ordinal with ties, from heterogeneous metrics (premiums, sales, locations, store counts, brand value), so the bar is set lower. Below 0.20 market position explains almost none of the ordering.

**Reported alongside.** Per-industry ρ; the same test with the eligible rank in place of tier (x = −eligible rank, so that a positive ρ again means larger brands have higher Presence); without FAS (the Lyst Index includes AI discovery signals among its inputs, a partial overlap with what is measured) and without the two pharmacy units placed from a different metric (Health Mart, Good Neighbor Pharmacy; not applicable if pharmacies are dropped); mean π̂ by tier and industry. Each variant uses the test's seed.

### §2.4 PRIMARY: `H_Separation` — Consistency is separable from Presence in the new industries

**Statement.** Across the new industries, how consistently the three models name a brand does not follow how often they name it.

**Operationalisation.** Rated units (§2.1; a ghost unit counts if it is rated); x = π̂_b, y = C_φ,b.

**Test.** ρ_sep = ρ_pw(x, y); two-sided bootstrap interval (seed 440043).

**Verdict rule.** UNDETERMINED if fewer than 40 rated units · CONFIRMED if |ρ_sep| ≤ 0.50 and the 95% interval lies inside (−0.70, 0.70) (lower bound > −0.70 and upper bound < 0.70) · FALSIFIED if |ρ_sep| > 0.50 · MARGINAL otherwise.

**Rationale.** 0.50 is the separability ceiling of v1.7 and v1.9 (constraint K1); v1.8 found |ρ(φ, μ)| = 0.091 and v1.9 Stage 2 ρ = 0.189 on the legacy panel. The interval condition guards against a passing point estimate that the data cannot distinguish from strong dependence.

**Reported alongside.** Per-industry ρ (descriptive; small n); share of unrated units per industry and tier; partition counts (zero, saturated, defined) per run; the same statistic with raw φ_b in place of C_φ (identical up to sign).

### §2.5 Manipulation checks

- **MC_Complete.** At least 98% of the design's calls (909; 807 without pharmacies; 765 if run 3 is dropped under §4.5) end with non-empty answer text after the retry policy. A model with fewer than 90% of its calls answered in a phase (Phase B: 144, or 96 without run 3; Phase A: 159) triggers the drop rule (§5.4).
- **MC_Served.** Every served model ID equals the requested ID (a dated snapshot of it is accepted); other IDs are excluded, re-run in the re-run pass and logged.
- **MC_Truncation.** Share of calls ending at the output cap per model; above 5% is flagged.
- **MC_Window.** First and last call times; all calls within 72 hours and inside the collection window (2026-11-24 to 2026-11-28, US Central, or the window of a DEVIATIONS entry written before the first call, §4.6). The acquisition script enforces both (§4.6); the scorer reports them.
- **MC_Parity.** Gates P1 and P2 (§5.3) pass before any statistic is computed.
- **MC_Budget.** Spend from recorded usage stays at or below $100; every pause, approval and stop is logged and reported with the calls not sent.
- **MC_Alias.** Every match of a case-sensitive (collision-prone) alias is exported with its sentence for the audit table (§5.1); reported, not used to override codes.

### §2.6 Pre-registered descriptives (no verdicts)

1. Presence by industry, tier and model (mean, SD, range, share at 0 and at 1).
2. Recognition share per model and industry; the recognition–recall gap (units recognised by all three models with π̂ = 0) by tier.
3. Ghosts: recognition and recall of Esurance, A&P and Rite Aid per model.
4. Run-to-run reliability per model: rel1 (mean ρ_pw over the three run pairs of k_{b,m,r}/6) and rel3 = 3 · rel1 ÷ (1 + 2 · rel1).
5. Model agreement: pairwise ρ_pw of per-model recall.
6. Brands named in Phase B answers that are not registry units (counts per industry; the ten most frequent per industry), to show what each registry leaves out. Candidate names are the Markdown bold spans and the heads of list items of each answer (1–6 words, starting with a capital letter or digit) that no alias of the industry's registry matches; a heuristic, descriptive only.
7. Units present in two industries (Kroger, Publix, Albertsons in grocery and pharmacy): Presence in each frame.
8. Answer form: words and registry brands per Phase B answer; finish reasons; refusals; Phase A ambiguous answers.
9. Cost: tokens and spend per model and phase from recorded usage.

---

## §3 Brand registries

### §3.1 Industries

Eight industries, all new to the programme, from the candidate list of 2026-11-09. Files: `osf/v44/registries/<file>.csv` (one per industry; every row carries its source title, URL, source date, data period and access date 2026-11-10), `industries_v0_44.csv` (summary) and `excluded_v0_44.csv` (every exclusion with its reason). Built by `osf/v44/scripts/make_registries_v0_44.py` (deterministic; tiers computed from the order, not typed).

| Industry (file) | Units | L / C / S / G | Tier metric and source (date) |
|---|---|---|---|
| Car insurance (`ins_car_insurance`) | 23 | 6 / 8 / 8 / 1 | Private passenger auto direct premiums written 2024, NAIC top 25 groups (NAIC 2025 report via Agency Checklists, 2025-03-17); top-7 order confirmed for 2025 (Repairer Driven News, 2026-03-31) |
| Hotel chains (`hot_hotel_chains`) | 20 | 6 / 8 / 6 / 0 | US locations, ScrapeHero top 10 (updated 2026-10-16); then rooms, HOTELS 325 (HOTELS magazine, July/Aug 2026) |
| Grocery store chains (`gro_grocery_chains`) | 20 | 6 / 8 / 5 / 1 | 2025 US retail sales, NRF Top 100 Retailers 2026 |
| Fast-food chains (`qsr_fast_food_chains`) | 21 | 6 / 8 / 7 / 0 | 2024 US systemwide sales, QSR 50 2025 edition (FoodIndustry.com, 2025-11-11); the 2026 edition's full table could not be opened, its reported top 10 has the same ten chains |
| Clothing and department stores (`apr_clothing_department_stores`) | 16 | 6 / 8 / 2 / 0 | 2025 US retail sales, NRF Top 100 Retailers 2026 |
| Pharmacies (`pha_pharmacies`) | 16 | 6 / 8 / 1 / 1 | 2025 prescription revenue, Drug Channels Institute (2026-03-17, via Becker's); NRF 2025 retail sales for Health Mart and Good Neighbor Pharmacy |
| Convenience stores and gas stations (`cvf_convenience_fuel`) | 19 | 6 / 8 / 5 / 0 | US store count at 2026-01-01, CSP Top 40 (2026-03-23) |
| Fashion and luxury (`fas_fashion_luxury`) | 24 | 6 / 8 / 10 / 0 | Interbrand Best Global Brands 2026 brand value (Retail Times, 2026-10-28) for the 8 luxury brands it ranks; then Lyst Index Q3 2026 rank (global sources; no US-only ranking was found) |
| **Total** | **159** | **48 / 64 / 44 / 3** | |

Brands per industry:

- **INS.** L: State Farm, Progressive, GEICO, Allstate, USAA, Farmers Insurance · C: Liberty Mutual, Travelers, AAA (three AAA club groups pooled), American Family Insurance, Auto-Owners Insurance, Erie Insurance, Nationwide, Mercury Insurance · S: Sentry Insurance, Kemper, The Hartford, Markel, Amica, COUNTRY Financial, Shelter Insurance, NJM Insurance · G: Esurance (phased out by Allstate in 2020).
- **HOT.** L: Hilton, Marriott, Choice Hotels, Wyndham, IHG, Best Western · C: Hyatt, Sonesta, Red Roof, Americas Best Value Inn, Motel 6, Extended Stay America, Four Seasons, Westgate Resorts · S (every 2nd of 11 guest-facing brands in rooms order): Margaritaville, Club Quarters, stayAPT Suites, AKA, GrandStay, Freehand.
- **GRO.** L: Kroger, Albertsons, Publix, Aldi, H-E-B, ShopRite · C: Hy-Vee, Wegmans, WinCo Foods, Giant Eagle, Sprouts Farmers Market, Piggly Wiggly, Raley's, Stater Bros. · S: Grocery Outlet, Weis Markets, Ingles, Schnucks, Save A Lot · G: A&P (bankrupt 2015, last stores closed or sold by November 2016).
- **QSR.** L: McDonald's, Starbucks, Chick-fil-A, Taco Bell, Wendy's, Dunkin' · C: Chipotle, Burger King, Subway, Domino's, Panda Express, Panera Bread, Popeyes, Pizza Hut · S (QSR 50 ranks 20, 25, …, 50): Jack in the Box, Culver's, In-N-Out Burger, Crumbl, El Pollo Loco, Cava, Tim Hortons.
- **APR.** L: T.J. Maxx, Ross Dress for Less, Macy's, Nordstrom, Kohl's, Gap · C: Burlington, Saks Fifth Avenue, JD Sports, Lululemon, Dillard's, JCPenney, Victoria's Secret, American Eagle · S: Urban Outfitters, Abercrombie & Fitch.
- **PHA.** L: CVS Pharmacy, Walgreens, Express Scripts, Optum Rx, Walmart Pharmacy, Kroger Pharmacy · C: Health Mart, CenterWell Pharmacy, Publix Pharmacy, Albertsons Pharmacy, Good Neighbor Pharmacy, PANTHERx Rare, CarelonRx, Costco Pharmacy · S: AcariaHealth · G: Rite Aid (had closed all of its stores and liquidated, per Drug Channels, 2026-03-17).
- **CVF.** L: 7-Eleven, Circle K, Casey's, Murphy USA, QuikTrip, Wawa · C: ExtraMile, Kwik Trip, Maverik, Sheetz, Love's, Pilot Flying J, RaceTrac, Yesway · S: Stewart's Shops, Jacksons, Royal Farms, RaceWay, Brake Time.
- **FAS.** L: Hermès, Louis Vuitton, Chanel, Cartier, Dior, Tiffany & Co. · C: Gucci, Prada, Miu Miu, Saint Laurent, Burberry, Ralph Lauren, Chloé, Celine · S: Bottega Veneta, Coach, Massimo Dutti, The Row, Moncler, Dries Van Noten, Loewe, Diesel, Stone Island, Khaite.

### §3.2 Tier rule (identical in every industry)

1. **Eligibility.** A unit is a consumer-facing brand under which the ranked company serves US customers: the company's name where it is the brand, otherwise its namesake, flagship or network banner as recorded in `mapping_basis`. Management companies, consortia, holdings, distributors and multi-banner operators without a single banner, and companies outside the industry's format, are excluded (`excluded_v0_44.csv`). Sub-brands are not merged into their parent and are not aliases.
2. **Order.** Eligible units are ordered by the source metric. Where a first source stops (ScrapeHero top 10; Interbrand's eight luxury brands), the order continues with the second source named in the table.
3. **Tiers.** L = eligible ranks 1–6; C = eligible ranks 7–14; S = eligible ranks 15 and below: all of them, or, for long tables, a systematic sample fixed before looking at any answer (QSR: every 5th rank from 20; hotels: every 2nd guest-facing brand, starting with the first). G = a brand that left the US market in a dated public event (one per industry where one was found in the sources: Esurance, A&P, Rite Aid).
4. **Programme cells.** The v0.20–v0.22 identity-load cells (A prestige, B cult-DTC, C mass) are specific to beauty and premium goods and are not applied. The ghost cell of v0.40 is applied as G.

### §3.3 Industries considered and not selected

- **Telecom** and **media and streaming**: conflict of interest (DEVIATIONS Entry 0, Part B; §8).
- **Pharmaceutical manufacturers**: conflict of interest (DEVIATIONS Entry 0, Part B; §8); pharmacies were selected instead.
- **Education** (online learning platforms) and **travel booking and car rental**: no dated public ranking with brand-level figures could be opened on 2026-11-10 (Similarweb shows only its top 5; Auto Rental News gives industry totals only).
- **Energy** is represented only by fuel retail (CVF); utilities are excluded because most US households cannot choose them.
- **A full luxury ranking** (Brand Finance Luxury & Premium 50 2026, Deloitte Global Powers of Luxury Goods) could not be opened in full; FAS therefore combines Interbrand and Lyst.

### §3.4 Pre-lock option: dropping pharmacies

Pharmacies stay in with the supply relationship disclosed in §8 (DEVIATIONS Entry 0, Part C) unless the pre-registrant types "drop pharmacies" before the lock. Dropping them is pre-specified here in full and touches no other industry:

1. `registries/industries_v0_44.csv` loses its `PHA` row; `registries/pha_pharmacies.csv` stays in the deposit, marked in `excluded_v0_44.csv` as "industry dropped before the lock (COI)". No other registry row changes.
2. `build_probes_v0_44.py` and `cost_estimate_v0_44.py` are re-run (they read the industry list); the probe file, its SHA-256 and the cost files are replaced, and the lock manifest is rewritten. The acquisition, coding and scoring scripts derive every count from the industry list and need no change (tested: `test_drop_run3_and_counts_from_industry_list`, `test_pharmacies_dropped_registry_needs_no_code_change`).
3. Consequences: 7 industries, 143 units (141 non-ghost; ghosts Esurance and A&P), 42 Phase B and 143 Phase A questions, 3 × (42 × 3 + 143) = **807 calls**; cost $24.06 central / $46.36 high at November prices, $26.59 / $52.17 at December prices; `H_Spread` with I = 7 (§2.2); `H_Tier` on 141 units without the pharmacy-metric variant; descriptive 7 not computed; §8 takes the seven-industry COI text.
4. The change is logged in §9 and in DEVIATIONS.md before the lock. Because its content is fixed here, it does not restart the 24 hours; any other change to the industry list does.

---

## §4 Probes and collection

### §4.1 Probe file

`osf/v44/prereg/probes_v0_44.jsonl`: 207 lines (Phase B 48, Phase A 159), built by `osf/v44/scripts/build_probes_v0_44.py` from the registries (Markdown view: `probes_v0_44.md`; SHA-256 `107d9401c18d9ee00ee4d5d717642aaeac7eb812ce843ff559947fe8525c2bb6`, recorded there and in the lock manifest). No system prompt. The templates are the omnibus templates of v0.20–v0.22 (`osf/v42/prereg/probes_v0_42.jsonl`), with the category noun and expert group filled per industry and "in the US" added because the registries are US-market registries:

| Frame | Channel | Template |
|---|---|---|
| q1 | R_cat | What are the best {noun} in the US? List several with descriptions. |
| q2 | R_cat | What {noun} do {experts} recommend in the US? Name several. |
| q3 | R_cat | What {noun} in the US are highest quality and most reliable? Name several with descriptions. |
| q4 | R_cult | What {noun} are popular in the US right now? List several. |
| q5 | R_cult | What {noun} in the US have the most loyal customers? Name several. |
| q6 | R_cult | Which {noun} in the US have the most iconic or storied identity in popular culture? Name several. |
| A | recognition | Is the brand {brand} commonly recognized as a/an {category} brand? Answer yes or no. |

q5 replaces the omnibus's celebrity (v0.20–v0.21) and affluent-buyer (v0.22) frames, which do not fit service industries, with customer loyalty; all other frames follow an omnibus template word for word apart from the filled slots. Nouns: car insurance companies; hotel chains; grocery store chains; fast-food chains; clothing and department store chains; pharmacies; convenience store and gas station chains; luxury fashion brands. Expert groups and Phase A categories: `industries_v0_44.csv`.

### §4.2 Design

| Block (collection order) | Phase | Condition | Run | Calls per model | Calls (N3) |
|---|---|---|---|---|---|
| 1–3 | B (48 category questions) | S0 | 1, 2, 3 | 144 | 432 |
| 4 | A (159 brand questions) | S0 | 1 | 159 | 477 |
| **Total** | | | | **303** | **909** |

Calls by industry (all three models, all blocks): car insurance 123, hotel chains 114, grocery 114, fast food 117, clothing and department stores 102, pharmacies 102, convenience and fuel 111, fashion and luxury 126 (`cost_estimate_v0_44.txt`; `acquire_v0_44.py --dry-run`). Each call is independent. Blocks run in order; within a block one worker per model, the three in parallel, probes in file order.

**Why no web search (S1).** The study's questions are about what the models name from their own knowledge across industries, the condition under which every locked Presence and Consistency result was obtained (all omnibus waves are S0). Search-on answers measure retrieval of the live web, which is the Grounding component's question (v1.13) and would need its own pre-registration. S1 is also the expensive part: at November prices one S1 run of Phase B would take the design to $51.05 central and $105.15 high (over the cap); three runs to $98.69 central and $210.57 high (§4.5). S1 is therefore not collected.

**Why three Phase B runs and one Phase A run.** `H_Separation` needs φ defined in at least 2 of 3 runs; descriptive 4 needs run pairs; π̂ over three runs halves the run-to-run noise of a single run, which `H_Spread`'s threshold assumes. Two runs would save $5.93 central ($27.24 → $21.31), but a brand with one undefined run would then have no φ, shrinking the rated set. No test rests on recognition agreement across runs, so Phase A has one run (three would cost $46.14 central and $92.12 high, over the $80 pause).

### §4.3 Panel

N3 as verified for v0.42 r2 on 2026-11-10 (`osf/v42/prereg/PRE_REGISTRATION_v0_42.md` §4.3): Claude Fable 5.2 (`claude-fable-5-2`), GPT-6 Astra (`gpt-6-astra`), Gemini 4 Argon (`gemini-4-argon`), the newest generally available flagship of each provider, one per provider (programme budget rule). r1 checked that these are exactly the IDs of v0.42 r2 and of its feasibility record (`osf/v42/prereg/feasibility_v0_42.json`, 2026-11-10 05:13 UTC: each ID served as requested); the test `test_model_ids_are_v042_r2_ids` checks the script against the v0.42 text. Vendor pages are re-read at the lock; a newer flagship released before the collection is not substituted (comparability with t₄) and is reported. Cheaper tiers are not used: Presence and Consistency are defined on the panel, and the wave's purpose is to place the new industries on the panel the programme now uses.

### §4.4 Call settings

As v0.42 r2 §4.4 for S0: no tools; temperature, top-p and reasoning effort at provider defaults (Claude Fable 5.2 accepts none of them; its adaptive thinking is on); maximum output 16,384 tokens per request (all three models); Claude Fable 5.2 through Anthropic's Message Batches API with exactly the synchronous call's parameters; GPT-6 Astra and Gemini 4 Argon synchronous; the v0.39/v0.42 retry policy (transient errors retried up to 3 attempts, an empty answer re-sent once, batched requests re-sent up to 3 attempts, one logged re-run pass inside the window). The call functions are byte copies of v0.42's (and so of v0.39's), checked by `test_copied_block_is_byte_identical_to_v042`. Raw artefact `osf/v44/data/v44_raw.jsonl`, one line per attempt, with the v0.42 fields (call ID, industry, phase, probe, unit or frame, requested and served model, run, prompt, answer, finish reason, tokens, times, attempts, call mode, `usage_parts`, `cost_usd`, batch and request IDs). No feasibility call is planned.

### §4.5 Budget

**Cap.** At most $100 of paid model calls for this paper, including re-sends; pause at $80 (programme rule, 2026-11-10). No judge model is needed (every Phase A question is yes/no).

**Prices** (programme list read 2026-11-10, US$ per 1M tokens in / out; = v0.42 r2 §4.5, whose vendor sources are listed in `budget_v0_44.SOURCES`): Claude Fable 5.2 8 / 40 standard, 4 / 20 batch (used); GPT-6 Astra 10 / 50 standard (used; batch 5 / 25 not used, as in v0.42 r2); Gemini 4 Argon 2 / 10 through 2026-11-30, 4 / 20 from 2026-12-01 (standard; no batch price listed). `budget_v0_44.py` prices each billed request at the price of the UTC date it started.

**Per-call basis.** The t₄ wave's measured-basis figures (v0.42 r2, `osf/v42/prereg/cost_estimate_v0_42_r2.json`), US$ per call, central / high, re-send allowance included: Claude Fable 5.2 via Batch API — category question 0.0750 / 0.1490, yes/no brand question 0.0344 / 0.0789; GPT-6 Astra — 0.0349 / 0.0511 and 0.0193 / 0.0284; Gemini 4 Argon — 0.0135 / 0.0262 and 0.0058 / 0.0175 at November prices, 0.0271 / 0.0524 and 0.0115 / 0.0350 at December prices.

**Estimate of the adopted design** (US$, central / high; `python3 osf/v44/scripts/cost_estimate_v0_44.py`):

| Model (mode) | Calls | November prices (planning) | December prices (slip check) |
|---|---|---|---|
| Claude Fable 5.2 (Batch API) | 303 | 16.27 / 34.01 | 16.27 / 34.01 |
| GPT-6 Astra (standard) | 303 | 8.10 / 11.87 | 8.10 / 11.87 |
| Gemini 4 Argon (standard) | 303 | 2.87 / 6.56 | 5.73 / 13.12 |
| **All** | **909** | **27.24 / 52.44** | **30.10 / 59.00** |
| of which Phase B (432) / Phase A (477) | | 17.78 / 32.59 and 9.45 / 19.84 | 19.73 / 36.37 and 10.37 / 22.63 |

The collection is planned inside November (§4.6), so the November figures are the planning estimate. If it slips past 2026-11-30, the December figures apply: the high estimate, $59.00, is still below the $80 pause and the $100 cap. Per industry (November / December, central): from $3.17 / $3.51 (clothing and department stores; pharmacies) to $3.65 / $4.03 (fashion and luxury).

**Design trade-off** (November prices, same basis):

| Design | Calls | Central | High |
|---|---|---|---|
| **Adopted: Phase B S0 × 3, Phase A S0 × 1** | **909** | **27.24** | **52.44** |
| Phase B S0 × 2 | 765 | 21.31 | 41.57 |
| Phase B S0 × 1 | 621 | 15.38 | 30.71 |
| Phase A S0 × 3 | 1,863 | 46.14 | 92.12 |
| Adopted + Phase B S1 × 1 | 1,053 | 51.05 | 105.15 |
| Adopted + Phase B S1 × 3 | 1,341 | 98.69 | 210.57 |
| Pharmacies dropped (§3.4) | 807 | 24.06 | 46.36 |

The adopted design is the fewest runs that keep the three primary tests as specified (§4.2), and its high estimate stays below the $80 pause at either price. An industry of 20 units costs $3.41 central and $6.57 high at November prices.

**Guard (from actual usage).** The v0.42 ledger, forked unchanged in its arithmetic to `budget_v0_44.py` (no judge reserve): spend = the cost of every raw line already written, from its recorded usage at the listed prices; before each request its worst case is reserved (output at the 16,384-token cap, 2,000 input tokens: $0.3357 Claude Fable 5.2 batch, $0.8392 GPT-6 Astra, $0.1678 Gemini 4 Argon in November, $0.3357 in December); a batch is cut to the requests whose worst cases fit. (i) **Hard stop:** no request is sent if spend + reservations + its worst case would exceed $100. (ii) **Pause at $80:** no new request starts until the pre-registrant's OK is recorded (`--approve-past-80`). (iii) **Projection pause:** after block 1 (Phase B run 1), projected total = actual spend × R, R = central estimate of the design ÷ central estimate of block 1 = 27.24 ÷ 5.93 = 4.5945 at November prices (4.5761 if block 1 starts on or after 2026-12-01), read by the script from `cost_estimate_v0_44.json`; if the projection exceeds $80 (block-1 spend above $17.41), collection pauses and the pre-registrant decides between continuing (`--approve-projection`) and dropping Phase B run 3 (`--drop-run-3`; 765 calls; `H_Separation` then needs φ defined in both remaining runs). At the central estimate none of these is reached (block 1 ≈ $5.93); at the high estimate block 1 ≈ $10.86 and the whole design ends at ≈ $52.44.

### §4.6 Collection window and guards

- **Window.** 2026-11-24 00:00 to 2026-11-28 24:00 US Central, after the lock and after the other programme collections booked on the collection machine from 2026-11-11 to 2026-11-23. No request is sent at or after the earlier of the window's end and 72 hours after the first recorded call.
- **One collection at a time.** `--collect` refuses while another acquisition process with `--collect` (or a legacy `run_acquisition_v*.py` runner) is running on the machine.
- **Anchor.** `--collect` refuses unless `osf/v44/anchor/osf_anchor_v0_44.json` exists, tag `v0.44-prereg-r1` is on `origin` and the anchor names the tag's commit.
- **Slip.** If the collection cannot start in the window, a DEVIATIONS entry naming the new dates and the reason is written and committed before the first call, and the collection runs with `--window START END --deviation-entry N` (the script refuses unless that entry names both dates). The 72-hour rule and the budget guard are unchanged. A slip past 2026-11-30 bills Gemini 4 Argon at its December price: high estimate $59.00, within the cap.

### §4.7 Scripts and exact commands

All commands run from the repository root of branch `v0.44` with the system Python 3 (numpy, scipy); paths are relative, never a hard-coded home directory. Nothing below sends a request except `--collect`.

| Step | Command | Output |
|---|---|---|
| Probe file | `python3 osf/v44/scripts/build_probes_v0_44.py` | `prereg/probes_v0_44.jsonl`, `.md` |
| Cost estimate | `python3 osf/v44/scripts/cost_estimate_v0_44.py` | `prereg/cost_estimate_v0_44.json`, `.txt` |
| ρ_pw check (C2) | `python3 osf/v44/scripts/rho_pw_check_v0_44.py` | `prereg/rho_pw_check_v0_44.txt` |
| Unit tests (local fakes, no network) | `python3 osf/v44/scripts/tests/run_all_v0_44.py` | 61 tests |
| Gate P1 | `python3 osf/v44/scripts/score_v0_44.py --parity-p1` | `prereg/parity_P1_v0_44.json` |
| Dry run (the default mode) | `python3 osf/v44/scripts/acquire_v0_44.py` | `prereg/dry_run_v0_44.txt` |
| Lock manifest | `python3 osf/v44/scripts/lock_manifest_v0_44.py` | `LOCK_MANIFEST_v0_44.sha256` |
| Collection (after the lock) | `nohup caffeinate -i python3 osf/v44/scripts/acquire_v0_44.py --collect > osf/v44/data/collect_v0_44.log 2>&1 &` | `data/v44_raw.jsonl`, `data/v44_budget_state.json` |
| Resume / re-run pass | the same command (calls with an answer are skipped) | appended lines |
| Approvals | add `--approve-past-80 "<who, when>"`, `--approve-projection "<who, when>"` or `--drop-run-3 "<who, when>"` | state file |
| Coding | `python3 osf/v44/scripts/code_v0_44.py` | `data/coded/v44_phase_a.csv`, `v44_phase_b.csv`, `v44_alias_audit.csv` |
| Scoring (once) | `python3 osf/v44/scripts/score_v0_44.py --run` | `v44_verdicts.json`, `v44_unit_table.csv` |

`acquire_v0_44.py` and `budget_v0_44.py` fork v0.42's acquisition and budget scripts (changes listed in their headers); `code_v0_44.py` and `score_v0_44.py` are new; `tests/` holds `test_acquire_v0_44.py`, `test_code_score_v0_44.py`, the synthetic-data builder `synth_v0_44.py` and the runner. The tests are unittest classes, which pytest also collects; pytest is not installed on the collection machine, so they are run with the runner above.

---

## §5 Analysis plan

### §5.1 Coding

- **Mentions (Phase B).** A unit is mentioned in an answer of its own industry if any of its aliases (registry column `aliases`) occurs as a whole word: case-insensitively for rule `ci`, case-sensitively for rule `cs` (aliases that are also common words, places or names: e.g. Progressive, Nationwide, Subway, Gap, Coach, Diesel, The Row). Whole word: not preceded or followed by a letter or digit (spaces, punctuation, underscores and Markdown marks are boundaries). Before matching, answer and aliases are put in Unicode NFC, typographic apostrophes are read as ', non-breaking and typographic hyphens as -, and no-break spaces as spaces (r1 clarification, C7). URLs are removed first (`strip_urls`, byte copy of `code_t4_v0_42.py`'s, checked by a test). Sub-brands are not aliases (§3.2). No alias of one unit matches inside an alias of another unit of the same industry (checked by a test). The alias matcher is new code (the omnibus matchers are registry-specific); its unit tests are part of the lock manifest. MC_Alias exports every case-sensitive match for the audit table; the audit is reported, never used to change codes.
- **Recognition (Phase A).** `run_acquisition_v22.parse_yes_no`, the certified omnibus parser (its file's SHA-256, `59f711b8…`, equals the value locked in `score_v41.PROBE_SHA256`; checked by a test), on the unstripped answer, as `code_t4_v0_42.recog_label` calls it; yes → recognised; no and ambiguous → not recognised; ambiguous answers are counted.
- **Coder and scorer.** `osf/v44/scripts/code_v0_44.py` and `score_v0_44.py`, written and tested on synthetic data before the lock. The φ kernel and its partitions, π̂, the bootstrap and the aggregation helpers are imported unchanged from `osf/v42/scripts/score_v0_42.py` (which takes them from `osf/v41/scripts/score_v41.py`); ρ_pw, the permutation test and rel1 use the centred ranks of §2.1 (C2). Scorer choices where the text is silent are listed in the scorer's header (SCORER_NOTES N1–N16) and are part of the lock.

### §5.2 Computation

All statistics by `score_v0_44.py --run`, run once after gates P1 and P2 (the script refuses to run if `v44_verdicts.json` exists or if the tag is not on `origin`), from `v44_raw.jsonl`, the coded tables and the locked registries. Output: `osf/v44/v44_verdicts.json` and a unit table (`v44_unit_table.csv`: k per model and run, π̂, φ partitions per run, φ_b, C_φ, rated flag, recognition per model).

### §5.3 Gates

- **P1 (kernel parity).** The imported functions, run on the locked t₃ data, reproduce v0.41's π̂ and φ for all 112 omnibus brands exactly (as v0.42's P1). Run on 2026-11-10 for r1: **PASS**, 112 of 112 brands exact for k, π̂ and φ (`prereg/parity_P1_v0_44.json`); re-run by the scorer before scoring.
- **P2 (probe parity).** The probe file's SHA-256 equals the value in `LOCK_MANIFEST_v0_44.sha256`; every sent prompt equals its probe text byte for byte.

A failed gate stops scoring; the fix is logged in DEVIATIONS before scoring resumes.

### §5.4 Drop rule and missing data

A model with fewer than 90% of its calls answered in a phase after the re-run pass is excluded from that phase's statistics. The three primary tests need all three models in Phase B: if one is excluded they are UNDETERMINED and reported on the remaining two models as descriptives. Calls not sent because of a budget stop count as unanswered. Rates use answered calls as the denominator; a model-run with a missing Phase B answer in an industry yields no φ for that industry's units in that run. No imputation.

### §5.5 Reporting

Every test, including failures and undetermined results, with per-industry breakdowns. The paper (January 2027) and its OSF deposit carry the verdicts, the unit table and the raw answers. Public-study rules apply: no focal brand, no lessons addressed to a brand, no brand contacted.

---

## §6 Limitations

1. Tiers come from heterogeneous public metrics (premiums, sales, locations, store counts, brand value, a demand index); within an industry they order size or salience, not one common quantity. Some sources are reproductions of the original tables (NAIC via Agency Checklists; QSR 50 via FoodIndustry.com; DCI figures via Becker's).
2. Fashion and luxury rests on global sources; the Lyst Index uses AI discovery signals among its inputs (`H_Tier` is also reported without FAS).
3. Some company totals cover several banners (TJX, Macy's, Gap, Kroger, Albertsons) while the unit is one banner; house-of-brands hotel groups (IHG, Choice, Wyndham) are named by groups that guests may know by their sub-brands, which lowers their measured Presence.
4. Three models, three runs: φ is noisier than on six models, and the rated set may be small in industries with low recall.
5. No web search: the results describe the models' own knowledge, not what a search-enabled assistant would retrieve.
6. One market and language (US English); one collection, no retest.
7. The alias matcher is new and unvalidated against hand coding; the case-sensitive rule trades recall for precision on collision-prone names.
8. Grocery and pharmacy share three company names (Kroger, Publix, Albertsons); their two units are measured in different frames and are not independent.
9. ρ_pw centres ranks within industry (C2); v0.41 and v0.42 use the uncentred statistic, so v0.44's rank correlations are not computed identically to theirs (they coincide when industries have equal sizes).

---

## §7 Decisions for the pre-registrant before the lock

1. **Industry list.** Eight industries (§3.1), within the requested 8–10. Telecom and media and streaming are left out on COI grounds; education and travel booking and car rental for want of an openable dated ranking (§3.3).
2. **Pharmacies.** Keep, with the supply relationship disclosed in §8 (the default), or type "drop pharmacies" (§3.4: 807 calls, $24.06 central).
3. **Search.** S1 not collected (§4.2); an S1 run would need its own budget.
4. **ρ_pw centring** (C2): adopted in r1 because the uncentred statistic is biased upwards with unequal industry sizes; the alternative is r0's uncentred statistic, which keeps identity with v0.41/v0.42.

---

## §8 Declarations

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. The brand registries of this study were built from dated public rankings by fixed rules and screened for Samsung-group ownership and relationships before any collection (DEVIATIONS Entry 0). The screen found no registry brand owned by a Samsung-group company; it checked the owners named by the registry sources against a list of Samsung-group companies and brands and did not open an ownership filing for each brand. Items of record: in the pharmacy registry, Samsung Bioepis, a Samsung affiliate, supplies private-label biosimilars to subsidiaries of the companies behind two registry units, Cordavis (CVS Caremark, CVS Health; unit CVS Pharmacy) and Quallent (Express Scripts; unit Express Scripts). Following the handling of the supply relationships disclosed in v0.22, this relationship is characterized as non-competitive with no brand-level overlap, and no operational restriction on registry composition was imposed. Two other pharmacy units belong to retailers (Walmart, Costco) that also sell Samsung products. Samsung affiliates operate in three of the eight industries outside the US market (insurance: Samsung Fire & Marine and Samsung Life; hotels: Hotel Shilla; fashion: Samsung C&T); none of their brands is in the registries, and whether their stores sell any registry brand was not screened. Whether Cheil Worldwide, a Samsung-affiliated advertising company, serves any registry brand was not screened (client lists are not public). Industries in which Samsung Electronics competes, or whose US companies are its device and network customers (telecom, media and streaming), were not selected, nor were pharmaceutical manufacturers, among which a Samsung affiliate markets biosimilars. Acquisition, coding and scoring are fully automated against registries locked and deposited before the first call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

*If pharmacies are dropped before the lock (§3.4), this subsection takes the seven-industry text instead:* The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. The brand registries of this study were built from dated public rankings by fixed rules and screened for Samsung-group ownership and relationships before any collection (DEVIATIONS Entry 0). The screen found no registry brand owned by a Samsung-group company; it checked the owners named by the registry sources against a list of Samsung-group companies and brands and did not open an ownership filing for each brand. A pharmacy industry was screened and dropped before the lock because a Samsung affiliate supplies private-label biosimilars to subsidiaries of two of its brands. Samsung affiliates operate in three of the seven industries outside the US market (insurance: Samsung Fire & Marine and Samsung Life; hotels: Hotel Shilla; fashion: Samsung C&T); none of their brands is in the registries, and whether their stores sell any registry brand was not screened. Whether Cheil Worldwide, a Samsung-affiliated advertising company, serves any registry brand was not screened (client lists are not public). Industries in which Samsung Electronics competes, or whose US companies are its device and network customers (telecom, media and streaming), were not selected, nor were pharmaceutical manufacturers, among which a Samsung affiliate markets biosimilars. Acquisition, coding and scoring are fully automated against registries locked and deposited before the first call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

## Funding {-}

Self-funded.

## Ethics {-}

Not applicable; no human subjects.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

---

## §9 Lock procedure and change log

- **r0 draft** (2026-11-10, commit `ef6472f`): design, registries, probes, cost estimate, DEVIATIONS Entry 0. Not sent.
- **r1 draft** (this file, 2026-11-10): scripts, tests, commands, re-priced budget, window and guards, pharmacies option; committed locally on branch `v0.44`; not pushed, not deposited. A staging copy of what goes to OSF `v44/prereg/draft_r1/` is kept untracked in `osf/v44/_osf_stage_draft/`, and a draft lock manifest in `osf/v44/LOCK_MANIFEST_v0_44_DRAFT.sha256`. The coordinator sends r1 to the pre-registrant.
- **Between sending and lock.** The pre-registrant sees the industry list (§3) and the decisions of §7. Clarifications that change no hypothesis, threshold, registry, probe or decision rule are logged below; dropping pharmacies follows §3.4; any other change restarts the 24 hours.
- **Lock** (24 hours after the pre-registrant receives this pre-registration, unless he objects): re-read the vendor model and price pages; re-run the tests, gate P1 and the dry run; write `LOCK_MANIFEST_v0_44.sha256` (`lock_manifest_v0_44.py`); commit; tag `v0.44-prereg-r1`; push branch and tag; deposit `osf/v44/prereg/`, `osf/v44/registries/`, `osf/v44/scripts/`, `DEVIATIONS.md` and the lock manifest at OSF `v44/`, verify their SHA-256 there and write `osf/v44/anchor/osf_anchor_v0_44.json` naming the tagged commit and the OSF paths. `acquire_v0_44.py --collect` refuses to run until the tag is on `origin`, the anchor file names its commit, the date is inside the window and no other paid collection is running (§4.6).

**Change log**

- 2026-11-10, r0: first draft.
- 2026-11-10, r1 — changes from r0 (the verdict matrix of every primary test is unchanged for the eight industries):
  - **C1 Scripts and commands.** `acquire_v0_44.py` (dry run by default; Message Batches for Claude Fable 5.2; per-call cost ledger from recorded usage; $80 pause, $100 hard stop, projection pause; output cap 16,384 tokens; resumable), `budget_v0_44.py` (fork of `budget_v0_42.py`, no judge reserve), `code_v0_44.py`, `score_v0_44.py`, `rho_pw_check_v0_44.py`, `lock_manifest_v0_44.py`, and 61 unit tests on local fakes and synthetic data (all pass). Exact commands in §4.7. The guards r0 §9 listed (tag on `origin`, anchor file, window, one paid collection at a time) are implemented and tested, and the 72-hour rule is enforced by the script (§4.6).
  - **C2 ρ_pw centred within industry (§2.1), an inconsistency exposed by the scorer.** r0's ρ_pw (Pearson's r of within-industry ranks pooled, as `score_v41.pooled_within_rho`) is not a purely within-industry statistic when industries differ in size: their mean ranks (n_i + 1)/2 enter x and y alike. On the 156 `H_Tier` units its null mean is +0.0560 against −0.0021 for the centred statistic, and it exceeds the centred statistic by 0.036 where the centred value is 0.353, close to the 0.40 threshold (`rho_pw_check_v0_44.py`, seed 1; `prereg/rho_pw_check_v0_44.txt`); and §2.4's raw-φ variant was not the negative of the C_φ statistic on synthetic data (a scorer test failed until the fix). r1 centres the ranks within industry (and rounds values to 10 decimals before ranking, so that floating-point noise does not split exact φ ties). Thresholds, seeds and draws are unchanged. Listed for the pre-registrant's decision (§7 item 4).
  - **C3 `H_Spread` count for I industries (§2.2).** Written for I industries so that pharmacies can be dropped: ⌊0.8 · I⌋ to confirm, fewer than half to falsify. For eight industries this is r0's rule (6 / 3); for seven it gives 5 / 3.
  - **C4 Dropping pharmacies (§3.4, new).** Pre-specified pre-lock option with its files, counts, cost, tests, thresholds and COI text; it does not restart the 24 hours.
  - **C5 Budget re-priced (§4.5, header).** Same per-call basis as r0. The planning estimate is now at November prices, $27.24 central / $52.44 high, because the window is in November (r0's headline, $30.10 / $59.00, priced Gemini 4 Argon at December's doubled price as a margin; it is kept as the slip check). Trade-off table at November prices; per-industry and per-phase costs added. Projection pause ratio 27.24 ÷ 5.93 = 4.5945 (r0: 30.10 ÷ 6.58), read from the cost file, December ratio 4.5761 if block 1 starts in December.
  - **C6 Window and guards (§4.6, new; header).** Window, 72-hour rule, one paid collection at a time, anchor check, slip procedure through a DEVIATIONS entry; the schedule line no longer names other studies' dates beyond the booked span.
  - **C7 Clarifications (no rule changed).** Rated floor in proportional form (N1); φ with run 3 dropped needs both runs (N2); eligible-rank variant uses −rank (§2.3); ghosts count in `H_Separation` if rated and "inside (−0.70, 0.70)" is strict (§2.4); MC_Complete and drop-rule counts for the fallback designs (§2.5); descriptive 6 extraction rule (§2.6); alias-matcher normalisation and boundaries (§5.1); `strip_urls` copied, not imported, with an identity test; the kernel's import path (r0: "from `score_v0_42.py`"; it is `score_v41.py`'s, re-exported by `score_v0_42.py`); P2's locked hash comes from the lock manifest; the scorer runs once.
  - **C8 Declarations.** The employer and its affiliates are named only in §8 (r0 also named them in §3.3 and §7); the standard author block is added; Declarations are split into subsections with the AI-use statement verbatim after Ethics; the COI text maps Cordavis and Quallent to the registry units, states the screen's method, adds the retail-channel and advertising-agency items of DEVIATIONS Entry 0 Part D, and has a seven-industry version.
  - **C9 Gate P1 run** (§5.3): PASS, 112 of 112 brands.
