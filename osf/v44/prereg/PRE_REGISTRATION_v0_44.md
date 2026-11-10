# AIAS™ Presence Measurement Protocol — Pre-Registration v0.44 (revision r0, DRAFT, not sent)

**Study:** The industry-breadth wave — AI availability of brands in eight industries the programme has not measured, on the newest models.
**Design:** 159 brand units in eight US-market industries (car insurance, hotel chains, grocery store chains, fast-food chains, clothing and department stores, pharmacies, convenience stores and gas stations, fashion and luxury), each built from dated public rankings by a fixed tier rule (§3). The three newest flagship models (N3: Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon) answer the 48 category questions (Phase B, six per industry) three times each and the 159 brand questions (Phase A) once, without web search (S0): 3 × (48 × 3 + 159) = **909 calls**.
**Budget:** at most US$100 of paid model calls, hard cap; pause at $80 (programme rule, 2026-11-10). **Estimate $30.10 central, $59.00 high** (§4.5), Gemini 4 Argon priced at its December list price as a margin.
**Protocol version:** Presence v1.6 (recognition from Phase A, recall from Phase B; SSRN 6816340); Consistency φ v1.8 (SSRN 6963359) scaled as C_φ per v1.9 (SSRN 7685126); call settings of the t₄ wave (v0.42 r2 §4.4, S0).
**Pre-registrant:** Pablo Ulpiano González Castro
**Status:** r0 draft, written 2026-11-10 by the programme runner from queue row 7 ("8–10 new industries, newest models: pre-registration → Pablo sees the list → collection"). Not yet sent. No study probe has been sent and none will be before the lock.
**Lock target:** git tag `v0.44-prereg-r1` on branch `v0.44`, pushed to `origin`; external anchor: deposit of this file, the registries, the probe file, the cost estimate, DEVIATIONS Entry 0, the scripts and the lock manifest at OSF `ec6wh` → `v44/prereg/` and `v44/anchor/` before the first call (§9). Locks 24 hours after the pre-registrant receives it, unless he objects; a change to the industry list restarts the 24 hours.
**Collection window:** 2026-11-24 to 2026-11-28 (US Central), all 909 calls within 72 hours of the first. Not before v0.40's collection (2026-11-17 to 2026-11-21) has ended, and never overlapping another paid collection (one at a time on the collection machine; v0.42 t₄ ends before 2026-11-17, its t₅ starts no earlier than 2026-12-03).
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

- **Units.** The 159 rows of the eight registries (§3). Tier ∈ {L, C, S, G}; G (ghost) units are three brands that left the US market (Esurance, A&P, Rite Aid) and are excluded from `H_Spread` and `H_Tier`; n = 156 non-ghost units.
- **k_{b,m,r}.** Number of the six Phase B questions of b's industry in which model m's answer in run r mentions b (§5.1); 0–6.
- **Recall Presence.** π̂_b = Σ_m Σ_r k_{b,m,r} ÷ (6 · 3 · 3), over the answered calls (§5.4); 0–1.
- **Recognition.** Phase A answer coded yes / no / ambiguous by the certified v0.22 parser (`run_acquisition_v22.parse_yes_no`); one run per model.
- **Consistency.** Per run r, φ_{b,r} = [1/(M − 1)] · Σ_m (k_{b,m,r} − 6π̂_{b,r})² ÷ [6π̂_{b,r}(1 − π̂_{b,r})], with M = 3 and π̂_{b,r} the run's recall rate, the locked v1.8 partitions (π̂ = 0 → zero; π̂ = 1 → saturated; otherwise defined) and the v0.41/v0.42 kernel. φ_b = mean of φ_{b,r} over runs whose partition is defined; undefined if fewer than 2 of the 3 runs are defined.
- **Scaled Consistency.** C_φ = 100 · (1 − φ_b ÷ φ_max), φ_max = 6M ÷ (M − 1), the largest value φ can take on M models. For M = 6 this is 7.2 and the formula is v1.9's locked C_φ = 100(1 − φ/7.2); for N3 (M = 3) φ_max = 9. A brand is **rated** if φ_b is defined and its total mentions are at least 9 of 54 model-run-question cells (π̂_b ≥ 1/6, v1.9's floor of 6 of 36 in proportion). Declared adaptation of v1.9 to a three-model panel.
- **ρ_pw(x, y).** Pooled within-industry Spearman correlation (values ranked within industry, average ranks for ties, Pearson's r of the ranks pooled; `pooled_within_rho` as in `score_v0_42.py`).
- **Permutation p.** One-sided unless stated; y shuffled within industry; 10,000 draws; p = (1 + #{ρ_perm ≥ ρ_obs}) ÷ 10,001.
- **Bootstrap.** Units resampled with replacement within industry; 10,000 resamples; percentile 95% interval.
- **Seeds.** 440041 (`H_Spread` descriptive intervals), 440042 (`H_Tier`), 440043 (`H_Separation`), 440045 (descriptives).
- **α.** 0.05 per test; no multiplicity correction; verdicts rest on the pre-set thresholds; every test is reported.

### §2.2 PRIMARY: `H_Spread` — Presence separates brands within each new industry

**Statement.** In most of the eight new industries, recall Presence on N3 varies across the industry's brands well beyond run-to-run noise.

**Operationalisation.** For each industry i, SD_i = the population standard deviation of π̂_b over its non-ghost units. Industry i shows spread if SD_i ≥ 0.15.

**Verdict rule.** CONFIRMED if at least 6 of the 8 industries show spread · FALSIFIED if 3 or fewer do · MARGINAL otherwise (4 or 5).

**Rationale.** On the omnibus at t₃ (L6, one run; `osf/v41/v41_three_wave_table.csv`, computed 2026-11-10) SD was 0.267 (headphones), 0.328 (skincare), 0.252 (cosmetics), 0.261 (cars) and 0.101 (spirits): four of five at or above 0.15. With 54 cells per brand, a brand with a true rate of 0.25 has a sampling SD of about 0.06, so 0.15 is about 2.5 times the noise. Six of eight is the omnibus rate (four of five) rounded down.

**Reported alongside.** SD_i with its bootstrap interval (seed 440041), range, share of units at π̂ = 0, per industry and per model; the same statistic on the omnibus for N3 at t₄ if v0.42 is scored by then (descriptive only).

### §2.3 PRIMARY: `H_Tier` — Presence follows public market position

**Statement.** Within industries, leaders (L) have higher Presence than challengers (C), and challengers than smaller brands (S).

**Operationalisation.** x = tier score (L = 3, C = 2, S = 1); y = π̂_b; n = 156 non-ghost units.

**Test.** ρ_tier = ρ_pw(x, y); one-sided permutation p (seed 440042); bootstrap interval.

**Verdict rule.** CONFIRMED if ρ_tier ≥ 0.40 and p < 0.05 · FALSIFIED if ρ_tier < 0.20 · MARGINAL otherwise.

**Rationale.** Presence correlated with Google search interest at 0.74 within B2B software (v0.25, n = 24). Tier is a coarse three-level ordinal with ties, from heterogeneous metrics (premiums, sales, locations, store counts, brand value), so the bar is set lower. Below 0.20 market position explains almost none of the ordering.

**Reported alongside.** Per-industry ρ; the same test with the eligible rank in place of tier; without FAS (the Lyst Index includes AI discovery signals among its inputs, a partial overlap with what is measured) and without the two pharmacy units placed from a different metric (Health Mart, Good Neighbor Pharmacy); mean π̂ by tier and industry.

### §2.4 PRIMARY: `H_Separation` — Consistency is separable from Presence in the new industries

**Statement.** Across the new industries, how consistently the three models name a brand does not follow how often they name it.

**Operationalisation.** Rated units (§2.1); x = π̂_b, y = C_φ,b.

**Test.** ρ_sep = ρ_pw(x, y); two-sided bootstrap interval (seed 440043).

**Verdict rule.** UNDETERMINED if fewer than 40 rated units · CONFIRMED if |ρ_sep| ≤ 0.50 and the 95% interval lies inside (−0.70, 0.70) · FALSIFIED if |ρ_sep| > 0.50 · MARGINAL otherwise.

**Rationale.** 0.50 is the separability ceiling of v1.7 and v1.9 (constraint K1); v1.8 found |ρ(φ, μ)| = 0.091 and v1.9 Stage 2 ρ = 0.189 on the legacy panel. The interval condition guards against a passing point estimate that the data cannot distinguish from strong dependence.

**Reported alongside.** Per-industry ρ (descriptive; small n); share of unrated units per industry and tier; partition counts (zero, saturated, defined) per run; the same statistic with raw φ_b in place of C_φ (identical up to sign).

### §2.5 Manipulation checks

- **MC_Complete.** At least 98% of the 909 calls end with non-empty answer text after the retry policy. A model with fewer than 90% of its calls answered in a phase (Phase B: 144; Phase A: 159) triggers the drop rule (§5.4).
- **MC_Served.** Every served model ID equals the requested ID (a dated snapshot of it is accepted); other IDs are excluded, re-run in the re-run pass and logged.
- **MC_Truncation.** Share of calls ending at the output cap per model; above 5% is flagged.
- **MC_Window.** First and last call times; all calls within 72 hours and inside 2026-11-24 to 2026-11-28 (Central).
- **MC_Parity.** Gate P1 (§5.3) passes before any statistic is computed.
- **MC_Budget.** Spend from recorded usage stays at or below $100; every pause, approval and stop is logged and reported with the calls not sent.
- **MC_Alias.** Every match of a case-sensitive (collision-prone) alias is exported with its sentence for the audit table (§5.1); reported, not used to override codes.

### §2.6 Pre-registered descriptives (no verdicts)

1. Presence by industry, tier and model (mean, SD, range, share at 0 and at 1).
2. Recognition share per model and industry; the recognition–recall gap (units recognised by all three models with π̂ = 0) by tier.
3. Ghosts: recognition and recall of Esurance, A&P and Rite Aid per model.
4. Run-to-run reliability per model: rel1 (mean ρ_pw over the three run pairs of k_{b,m,r}/6) and rel3 = 3 · rel1 ÷ (1 + 2 · rel1).
5. Model agreement: pairwise ρ_pw of per-model recall.
6. Brands named in Phase B answers that are not registry units (counts per industry; the ten most frequent per industry), to show what each registry leaves out.
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

- **Telecom** and **media and streaming**: conflict of interest (DEVIATIONS Entry 0, Part B).
- **Pharmaceutical manufacturers**: conflict of interest (a Samsung affiliate markets competing biosimilars); pharmacies were selected instead.
- **Education** (online learning platforms) and **travel booking and car rental**: no dated public ranking with brand-level figures could be opened on 2026-11-10 (Similarweb shows only its top 5; Auto Rental News gives industry totals only).
- **Energy** is represented only by fuel retail (CVF); utilities are excluded because most US households cannot choose them.
- **A full luxury ranking** (Brand Finance Luxury & Premium 50 2026, Deloitte Global Powers of Luxury Goods) could not be opened in full; FAS therefore combines Interbrand and Lyst.

---

## §4 Probes and collection

### §4.1 Probe file

`osf/v44/prereg/probes_v0_44.jsonl`: 207 lines (Phase B 48, Phase A 159), built by `osf/v44/scripts/build_probes_v0_44.py` from the registries (Markdown view: `probes_v0_44.md`; SHA-256 recorded there and in the lock manifest). No system prompt. The templates are the omnibus templates of v0.20–v0.22 (`osf/v42/prereg/probes_v0_42.jsonl`), with the category noun and expert group filled per industry and "in the US" added because the registries are US-market registries:

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

Each call is independent. Blocks run in order; within a block one worker per model, the three in parallel, probes in file order.

**Why no web search (S1).** The study's questions are about what the models name from their own knowledge across industries, the condition under which every locked Presence and Consistency result was obtained (all omnibus waves are S0). Search-on answers measure retrieval of the live web, which is the Grounding component's question (v1.13) and would need its own pre-registration. S1 is also the expensive part: one S1 run of Phase B would add $24.48 central and $54.02 high, taking the high estimate to $113 (over the cap); three runs would cost $104 central (§4.5). S1 is therefore not collected.

**Why three Phase B runs and one Phase A run.** `H_Separation` needs φ defined in at least 2 of 3 runs; descriptive 4 needs run pairs; π̂ over three runs halves the run-to-run noise of a single run, which `H_Spread`'s threshold assumes. Two runs would save $6.58 central, but a brand with one undefined run would then have no φ, shrinking the rated set. No test rests on recognition agreement across runs, so Phase A has one run (three would add $20.74 central and take the high estimate to $104).

### §4.3 Panel

N3 as verified for v0.42 r2 on 2026-11-10 (`osf/v42/prereg/PRE_REGISTRATION_v0_42.md` §4.3): Claude Fable 5.2 (`claude-fable-5-2`), GPT-6 Astra (`gpt-6-astra`), Gemini 4 Argon (`gemini-4-argon`), the newest generally available flagship of each provider, one per provider (programme budget rule). Vendor pages are re-read at the lock; a newer flagship released before the collection is not substituted (comparability with t₄) and is reported. Cheaper tiers are not used: Presence and Consistency are defined on the panel, and the wave's purpose is to place the new industries on the panel the programme now uses.

### §4.4 Call settings

As v0.42 r2 §4.4 for S0: no tools; temperature, top-p and reasoning effort at provider defaults (Claude Fable 5.2 accepts none of them; its adaptive thinking is on); maximum output 16,384 tokens; Claude Fable 5.2 through Anthropic's Message Batches API with exactly the synchronous call's parameters; GPT-6 Astra and Gemini 4 Argon synchronous; the v0.39/v0.42 retry policy (transient errors retried, an empty answer re-sent once, batched requests re-sent up to 3 attempts, one logged re-run pass inside the window). Raw artefact `osf/v44/data/v44_raw.jsonl`, one line per attempt, with the v0.42 fields (call ID, industry, phase, probe, unit or frame, requested and served model, run, prompt, answer, finish reason, tokens, times, attempts, call mode, `usage_parts`, `cost_usd`, batch and request IDs).

### §4.5 Budget

**Cap.** At most $100 of paid model calls for this paper, including re-sends; pause at $80 (programme rule, 2026-11-10). No judge model is needed (every Phase A question is yes/no).

**Per-call basis.** The t₄ wave's measured-basis figures (v0.42 r2, `osf/v42/prereg/cost_estimate_v0_42_r2.json`; prices read 2026-11-10 from the vendors' pages, sources listed in v0.42 §4.5), US$ per call, central / high, re-send allowance included: Claude Fable 5.2 via Batch API — category question (S0) 0.0750 / 0.1490, yes/no brand question 0.0344 / 0.0789; GPT-6 Astra — 0.0349 / 0.0511 and 0.0193 / 0.0284; Gemini 4 Argon at its list price from 2026-12-01 (double November's) — 0.0271 / 0.0524 and 0.0115 / 0.0350. Gemini 4 Argon bills at November prices for a call made on 2026-11-24 to 2026-11-28; the December price is used as a margin, so that a collection slipping past November 30 stays inside the estimate. Script: `osf/v44/scripts/cost_estimate_v0_44.py` → `cost_estimate_v0_44.json` and `.txt`.

**Estimate of the adopted design** (US$, central / high):

| Model (mode) | Phase B S0 × 3 (144) | Phase A S0 × 1 (159) | Total (303 calls) |
|---|---|---|---|
| Claude Fable 5.2 (Batch API) | 10.81 / 21.46 | 5.47 / 12.55 | 16.27 / 34.01 |
| GPT-6 Astra (standard) | 5.03 / 7.36 | 3.07 / 4.51 | 8.10 / 11.87 |
| Gemini 4 Argon (standard, Dec-1 price) | 3.90 / 7.55 | 1.83 / 5.57 | 5.73 / 13.12 |
| **All (909 calls)** | **19.74 / 36.37** | **10.37 / 22.63** | **30.10 / 59.00** |

At November Gemini prices: $27.24 central, $52.44 high.

**Design trade-off** (same basis):

| Design | Calls | Central | High |
|---|---|---|---|
| **Adopted: Phase B S0 × 3, Phase A S0 × 1** | **909** | **30.10** | **59.00** |
| Phase B S0 × 2 | 765 | 23.52 | 46.87 |
| Phase B S0 × 1 | 621 | 16.95 | 34.75 |
| Phase A S0 × 3 | 1,863 | 50.84 | 104.26 |
| Adopted + Phase B S1 × 1 | 1,053 | 54.59 | 113.02 |
| Adopted + Phase B S1 × 3 | 1,341 | 103.55 | 221.05 |

The adopted design is the fewest runs that keep the three primary tests as specified (§4.2), and its high estimate stays below the $80 pause. Each further industry of about 20 units would add about $3.80 central and $7.40 high.

**Guard (from actual usage).** The v0.42 ledger (`budget_v0_42.Ledger`, forked to `budget_v0_44.py` before the lock): spend = the cost of every raw line already written, from its recorded usage at the listed prices; before each request its worst case is reserved (output at the 16,384-token cap, 2,000 input tokens); a batch is cut to the requests whose worst cases fit. (i) **Hard stop:** no request is sent if spend + reservations + its worst case would exceed $100. (ii) **Pause at $80:** no new request starts until the pre-registrant's OK is recorded. (iii) **Projection pause:** after block 1 (Phase B run 1), the projected total = actual spend × (central estimate of the design ÷ central estimate of block 1) = spend × 30.10 ÷ 6.58; if it exceeds $80, collection pauses and the pre-registrant decides between continuing and dropping run 3 (the first fallback; `H_Separation` then needs φ defined in both remaining runs). At the central estimate none of these is reached (spend after block 1 ≈ $6.6); at the high estimate the whole design ends at ≈ $59.

---

## §5 Analysis plan

### §5.1 Coding

- **Mentions (Phase B).** A unit is mentioned in an answer if any of its aliases (registry column `aliases`) occurs as a whole word: case-insensitively for rule `ci`, case-sensitively for rule `cs` (aliases that are also common words, places or names: e.g. Progressive, Nationwide, Subway, Gap, Coach, Diesel, The Row). URLs are removed first (`strip_urls` of `code_t4_v0_42.py`). Sub-brands are not aliases (§3.2). The alias matcher is new code (the omnibus matchers are registry-specific); its unit tests are part of the lock manifest. MC_Alias exports every case-sensitive match for the audit table; the audit is reported, never used to change codes.
- **Recognition (Phase A).** `run_acquisition_v22.parse_yes_no`, the certified omnibus parser (as called by `code_t4_v0_42.recog_label`); ambiguous answers are counted, not coded.
- **Coder and scorer.** `osf/v44/scripts/code_v0_44.py` and `score_v0_44.py`, written and tested on synthetic data before the lock; the φ kernel, partitions, `pooled_within_rho`, permutation and bootstrap are imported unchanged from `osf/v42/scripts/score_v0_42.py`.

### §5.2 Computation

All statistics by `score_v0_44.py`, run once after gate P1, from `v44_raw.jsonl` and the locked registries. Output: `osf/v44/v44_verdicts.json` and a unit table (`v44_unit_table.csv`: k per model and run, π̂, φ per run, φ_b, C_φ, rated flag, recognition per model).

### §5.3 Gates

- **P1 (kernel parity).** The imported functions, run on the locked t₃ table, reproduce v0.41's π̂ and φ for all 112 omnibus brands exactly (as v0.42's P1).
- **P2 (probe parity).** The probe file's SHA-256 equals the locked value; every sent prompt equals its probe text byte for byte.

A failed gate stops scoring; the fix is logged in this file's DEVIATIONS before scoring resumes.

### §5.4 Drop rule and missing data

A model with fewer than 90% of its calls answered in a phase after the re-run pass is excluded from that phase's statistics. The three primary tests need all three models in Phase B: if one is excluded they are UNDETERMINED and reported on the remaining two models as descriptives. Calls not sent because of a budget stop count as unanswered. Rates use answered calls as the denominator; a model-run with a missing Phase B answer in an industry yields no φ for that industry's units in that run. No imputation.

### §5.5 Reporting

Every test, including failures and undetermined results, with per-industry breakdowns. The paper (January 2027) and its OSF deposit carry the verdicts, the unit table and the raw answers. Public-study rules apply: no focal brand, no lessons addressed to a brand, no brand contacted.

---

## §6 Limitations

1. Tiers come from heterogeneous public metrics (premiums, sales, locations, store counts, brand value, a demand index); within an industry they order size or salience, not one common quantity. Two sources are reproductions of the original tables (NAIC via Agency Checklists; QSR 50 via FoodIndustry.com; DCI figures via Becker's).
2. Fashion and luxury rests on global sources; the Lyst Index uses AI discovery signals among its inputs (`H_Tier` is also reported without FAS).
3. Some company totals cover several banners (TJX, Macy's, Gap, Kroger, Albertsons) while the unit is one banner; house-of-brands hotel groups (IHG, Choice, Wyndham) are named by groups that guests may know by their sub-brands, which lowers their measured Presence.
4. Three models, three runs: φ is noisier than on six models, and the rated set may be small in industries with low recall.
5. No web search: the results describe the models' own knowledge, not what a search-enabled assistant would retrieve.
6. One market and language (US English); one collection, no retest.
7. The alias matcher is new and unvalidated against hand coding; the case-sensitive rule trades recall for precision on collision-prone names.
8. Grocery and pharmacy share three company names (Kroger, Publix, Albertsons); their two units are measured in different frames and are not independent.

---

## §7 Decisions for the pre-registrant before the lock

1. **Industry list.** Eight industries (§3.1), within the requested 8–10. Telecom and media and streaming are left out on COI grounds; education and travel booking and car rental for want of an openable dated ranking (§3.3).
2. **Pharmacies.** Keep with the disclosed Samsung Bioepis supply relationship to CVS Caremark and Express Scripts subsidiaries (draft default), or drop (DEVIATIONS Entry 0, Part C).
3. **Search.** S1 not collected (§4.2); an S1 run would need its own budget.

---

## §8 Declarations

**Conflict of interest.** The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. The brand registries of this study were built from dated public rankings by fixed rules and screened for Samsung-group ownership before any collection (DEVIATIONS Entry 0): no registry brand is owned by a Samsung-group company. Items of record: in the pharmacy registry, Samsung Bioepis, a Samsung affiliate, supplies private-label biosimilars through subsidiaries of two registry brands, CVS Caremark (Cordavis) and Express Scripts (Quallent), a supply relationship that is non-competitive, has no brand-level overlap and imposed no restriction on registry composition. Samsung affiliates operate in three of the eight industries outside the US market (insurance: Samsung Fire & Marine and Samsung Life; hotels: Hotel Shilla; fashion: Samsung C&T); none of their brands is in the registries. Industries in which Samsung Electronics competes, or whose US companies are its device and network customers, were not selected. Acquisition, coding and scoring are fully automated against registries locked and deposited before the first call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

**Funding.** Self-funded.

**Ethics.** Not applicable; no human subjects.

**Use of AI tools.** During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

---

## §9 Lock procedure and change log

- **r0 draft** (this file): written 2026-11-10 in worktree `_worktrees/v0.44` (branch `v0.44`, from `527899e`, the v0.42 r2 draft); committed locally; not pushed, not deposited, not sent. The coordinator sends it to the pre-registrant.
- **Between sending and lock.** The pre-registrant sees the industry list (§3) and the decisions of §7. Clarifications that change no hypothesis, threshold, registry, probe or decision rule are logged below; any other change restarts the 24 hours.
- **Before the lock (scripts; no paid call).** Fork `acquire_v0_42.py` and `budget_v0_42.py` to `acquire_v0_44.py` and `budget_v0_44.py` (S0 only, blocks of §4.2, the guard of §4.5, the collection window and the one-collection-at-a-time check); write `code_v0_44.py` (alias matcher) and `score_v0_44.py`; unit tests against local fakes and synthetic data; run gate P1. No feasibility call is planned: the N3 model IDs were served correctly in v0.42's neutral feasibility check of 2026-11-10 05:13 UTC (`osf/v42/prereg/feasibility_v0_42.json`).
- **Lock** (24 hours after the pre-registrant receives this pre-registration, unless he objects; the scripts above implement the registered rules without changing them and are finished in that interval, otherwise the lock waits for them): write `LOCK_MANIFEST_v0_44.sha256` (this file, DEVIATIONS.md, the registries, the probe file, the cost estimate and every script and test); commit; tag `v0.44-prereg-r1`; push branch and tag; deposit `osf/v44/prereg/`, `osf/v44/registries/`, `DEVIATIONS.md` and `osf/v44/anchor/` at OSF `v44/` and verify their SHA-256 there. `acquire_v0_44.py --collect` refuses to run until the tag is on `origin`, the anchor file exists, the date is inside the window and no other paid collection is running.

**Change log**

- 2026-11-10, r0: first draft.
