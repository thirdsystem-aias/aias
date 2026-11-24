---
title: "AI Availability in Eight Service and Retail Industries on the Newest Models"
subtitle: "A Pre-Registered Industry-Breadth Wave (AIAS™ v0.44)"
date: "November 2026"
mainfont: "Carlito"
fontsize: 11pt
geometry: [letterpaper, margin=1in]
header-includes: |
  \usepackage{setspace}
  \usepackage{float}
  \usepackage{caption}
  \usepackage{titlesec}
  \usepackage{needspace}
  \captionsetup{justification=raggedright,singlelinecheck=false}
  \setstretch{1.36}
  \setlength{\parskip}{8pt}
  \setlength{\parindent}{0pt}
  \renewcommand{\maketitle}{}
  \providecommand{\xmpquote}[1]{#1}
  \widowpenalty=10000
  \clubpenalty=10000
  \renewcommand{\topfraction}{0.9}
  \renewcommand{\bottomfraction}{0.8}
  \makeatletter\def\fps@figure{tbp}\makeatother
  \usepackage{booktabs}
  \usepackage{array}
  \renewcommand{\textfraction}{0.07}
  \renewcommand{\floatpagefraction}{0.8}
  \makeatletter\setlength{\@fptop}{0pt}\setlength{\@fpsep}{14pt}\makeatother
---

\begin{titlepage}
\setstretch{1.0}
\setlength{\parskip}{0pt}
\begin{center}

{\LARGE \textbf{AI Availability in Eight Service and Retail Industries\\ on the Newest Models}\par}\vspace{8pt}

{\large A Pre-Registered Industry-Breadth Wave (AIAS™ v0.44)}\\[28pt]

Pablo Ulpiano González Castro\\[4pt]
School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System™ (research entity; data archive and methodology venue)\\[8pt]
Correspondence: pablou@pablou.com · pablou.com\\
ORCID: \href{https://orcid.org/0009-0003-8968-9990}{0009-0003-8968-9990}\\[20pt]

Pre-registration: \texttt{v0.44-prereg-r1} (commit \texttt{01058b6})\\
locked and deposited on OSF before the first study call\\[4pt]
Data and code: OSF \texttt{ec6wh}, \texttt{v44}\\[4pt]
November 2026

\end{center}
\end{titlepage}

# Abstract {-}

The two locked components of AI Availability, Presence (how often AI answers name a brand) and Consistency (how evenly models agree in naming it), were established on premium consumer-goods categories and a retiring model panel. This pre-registered wave asks whether they behave the same way in service and retail industries on the newest models. The newest generally available flagship of three providers (Claude Fable 5.2, GPT-6 Astra and Gemini 4 Argon), without web search, answered six open category questions three times and one yes/no recognition question per brand about 159 brands in eight US industries new to the programme: car insurance, hotel chains, grocery store chains, fast-food chains, clothing and department stores, pharmacies, convenience stores and gas stations, and fashion and luxury. Brands were placed in leader, challenger and smaller-brand tiers from dated public rankings by one fixed rule, and three brands that have left the US market were added as ghosts. All 909 of 909 planned calls were answered, 3 of them in the logged re-run pass, for $9.77 against a $100 cap, and every manipulation check passed. Recall Presence spread across brands in 8 of 8 industries (standard deviation 0.267 to 0.377 against a threshold of 0.15; H_Spread CONFIRMED). Within industries it followed market tier (pooled within-industry Spearman ρ = 0.558, 95% CI 0.408–0.677, permutation p < 0.001, n = 156; H_Tier CONFIRMED), also on the eligible rank (ρ = 0.599) and without fashion and luxury (ρ = 0.611). Consistency did not follow Presence among the 85 brands with a rated Consistency score (ρ = 0.019, 95% CI −0.249 to 0.269; H_Separation CONFIRMED). Smaller brands were often recognised but never named, and most of them could not be rated for Consistency. Every pre-registered test, check and descriptive is reported.

**Keywords:** AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; large language models; market position; services marketing; retail; insurance; hospitality; quick-service restaurants; luxury

**JEL codes:** M31; L86, L15, D83, M37

**Paper status:** Pre-registered confirmatory study (tag `v0.44-prereg-r1`, locked on 11 November 2026 and deposited on OSF before the first study call); collected on 24 November 2026; scored once (`score_v0_44.py --run`); deviations recorded in `osf/v44/DEVIATIONS.md`. Part of the AIAS measurement programme.

# 1. Introduction

AI Availability, the discoverability and representation of a brand in the answers of large language models (LLMs), has been proposed as a third measurable layer of brand availability (González Castro, 2026a), beside the Mental and Physical Availability of the Ehrenberg-Bass tradition (Sharp, 2010; Romaniuk & Sharp, 2016), within the Tri-System framework of brand growth (González Castro, 2026l). It is measured under a versioned protocol (Methodology v1.2--v1.6, González Castro, 2026b--f; AIAS 1.0, 2026j). The programme now reports two components (AIAS 2.0, González Castro, 2026k). Presence is the share of a category's open questions in which a model names a brand, with recognition from a yes/no question as its second channel (v1.6). Consistency is how evenly the models of a panel name a brand, scored by a dispersion statistic φ that does not depend on Presence by construction (v1.8, González Castro, 2026h; scaled as C_φ in v1.9, 2026i), after a coefficient-of-variation measure failed that test (v1.7, 2026g).

Both components were established on five consumer-product categories (audiophile headphones, skincare, cosmetics, cars and premium spirits, the v0.19--v0.23 omnibus of 112 brands), mostly premium goods, and on a six-model panel that is now being retired. On that base, Presence separated brands within four of the five categories and held its order over five months (v0.41, González Castro, 2026p), and Consistency was separable from Presence. Whether either result carries to industries in which people buy a service, choose a store or visit a chain, and to the newest models, had not been measured.

The programme's industry-breadth rule prefers industries it has not measured. This wave adds eight US industries: car insurance, hotel chains, grocery store chains, fast-food chains, clothing and department stores, pharmacies, convenience stores and gas stations, and fashion and luxury. It asks three questions, fixed before data as three primary hypotheses (§2.4): does Presence separate brands within each new industry (H_Spread); do brands that lead their industry on public market measures have higher Presence than its challengers and smaller brands (H_Tier); and is Consistency still separable from Presence (H_Separation)? It is a breadth wave, not a longitudinal one: one collection, three primary tests and nine pre-registered descriptives. Under the programme's independence rule for public studies there is no focal brand, no finding is addressed to a brand, and no brand was contacted.

# 2. Method

## 2.1 Registries

Each industry's brand registry was built from a dated public ranking by the same tier rule, fixed in the pre-registration (§3) and deposited before the first call (`osf/v44/registries/`, one file per industry with each row's source title, URL, source date, data period and access date). Eligible units are consumer-facing brands under which the ranked company serves US customers; management companies, consortia, holdings and companies outside the industry's format are excluded, and sub-brands are neither merged into their parent nor counted as aliases. Eligible units are ordered by the source metric; leaders (L) are eligible ranks 1--6, challengers (C) ranks 7--14 and smaller brands (S) ranks 15 and below (all of them, or a systematic sample fixed before any answer for long tables). Ghosts (G) are brands that left the US market in a dated public event: Esurance (car insurance), A&P (grocery) and Rite Aid (pharmacies). Table 1 lists the industries and their sources.

| Industry | Units | L / C / S / G | Tier metric (source) |
|---|---:|---|---|
| Car insurance | 23 | 6 / 8 / 8 / 1 | Private passenger auto premiums written, 2024 (NAIC top 25 groups) |
| Hotel chains | 20 | 6 / 8 / 6 / 0 | US locations (ScrapeHero top 10), then rooms (HOTELS 325, 2026) |
| Grocery store chains | 20 | 6 / 8 / 5 / 1 | 2025 US retail sales (NRF Top 100 Retailers 2026) |
| Fast-food chains | 21 | 6 / 8 / 7 / 0 | 2024 US systemwide sales (QSR 50, 2025 edition) |
| Clothing and department stores | 16 | 6 / 8 / 2 / 0 | 2025 US retail sales (NRF Top 100 Retailers 2026) |
| Pharmacies | 16 | 6 / 8 / 1 / 1 | 2025 prescription revenue (Drug Channels Institute); NRF for two units |
| Convenience stores and gas stations | 19 | 6 / 8 / 5 / 0 | US store count, 1 January 2026 (CSP Top 40) |
| Fashion and luxury | 24 | 6 / 8 / 10 / 0 | Interbrand Best Global Brands 2026, then Lyst Index Q3 2026 |
| **Total** | **159** | **48 / 64 / 44 / 3** | |

: Industries, units and tier sources (pre-registration §3.1; `osf/v44/registries/industries_v0_44.csv`).

Telecom, media and streaming, and pharmaceutical manufacturers were not selected on conflict-of-interest grounds (Declarations); education and travel booking for want of a dated public ranking that could be opened; utilities because most US households cannot choose them (pre-registration §3.3). Fashion and luxury rests on global sources, and the Lyst Index includes AI discovery signals among its inputs, so H_Tier is also reported without that industry.

## 2.2 Probes, panel and collection

Each industry has six open category questions (Phase B), filled from the omnibus templates of v0.20--v0.22 with the category noun, an expert group and "in the US": for example, "What are the best car insurance companies in the US? List several with descriptions." Three frames (q1--q3) ask for the best, the expert-recommended and the highest-quality brands; three (q4--q6) ask for the popular, those with the most loyal customers and those with the most iconic identity in popular culture. Each brand has one recognition question (Phase A): "Is the brand {brand} commonly recognized as a/an {category} brand? Answer yes or no." There is no system prompt. The probe file (207 lines; SHA-256 beginning `107d9401c18d`) was locked with the pre-registration.

The panel is the newest generally available flagship of each of three providers, as verified for the programme's t₄ wave: Claude Fable 5.2 (`claude-fable-5-2`, through Anthropic's Message Batches API), GPT-6 Astra (`gpt-6-astra`) and Gemini 4 Argon (`gemini-4-argon`). Calls used no tools and no web search (condition S0), provider-default sampling and reasoning settings, and a cap of 16,384 output tokens. Each model answered the 48 category questions three times (runs 1--3) and the 159 brand questions once: 3 × (48 × 3 + 159) = 909 calls. Transient errors were retried up to three attempts, an empty answer was re-sent once, and one logged re-run pass inside the window was allowed (pre-registration §4.4). The budget was at most $100 of paid calls with a pause at $80, both from recorded usage; the pre-registered estimate was $27.24 central and $52.44 high. The collection window was 24 to 28 November 2026 (US Central), all calls within 72 hours of the first; the acquisition script refused to send outside the window, without the lock tag on the remote and its OSF anchor, or while another paid collection was running on the machine (§4.6).

## 2.3 Measures

**Mentions.** A brand is mentioned in a category answer of its own industry if any of its registry aliases occurs as a whole word, case-insensitively, or case-sensitively for brands whose names are also common words, places or names (for example Progressive, Nationwide, Subway, Gap, Coach, The Row). URLs are removed first, and answer and aliases are normalised (Unicode NFC, typographic apostrophes and hyphens). The alias matcher is new code, tested before the lock against an independent ground truth on synthetic answers.

**Recall Presence.** For brand b, model m and run r, k is the number of the six category questions whose answer names b (0--6). Recall Presence is π̂_b = Σ k ÷ (6 · 3 · 3), the share of the 54 model-run-question cells that name the brand.

**Recognition.** The Phase A answer is coded yes, no or ambiguous by the certified parser of the omnibus (v0.22); yes counts as recognised.

**Consistency.** Per run, φ is the quasi-binomial dispersion of the three models' counts around the run's recall rate (the locked v1.8 kernel and partitions: zero when no model names the brand, saturated when every cell names it, defined otherwise). φ_b is the mean over the runs in which φ is defined, and is undefined if fewer than two of the three runs are defined. Scaled Consistency is C_φ = 100 · (1 − φ_b ÷ φ_max) with φ_max = 9, the largest value φ can take on three models (the declared adaptation of v1.9's C_φ, whose φ_max is 7.2 on six models). A brand is rated if φ_b is defined and π̂_b ≥ 1/6 (at least 9 of 54 cells).

**Statistics.** ρ_pw is the pooled within-industry Spearman correlation: values ranked within industry (average ranks for ties), each industry's ranks centred on their mean, and Pearson's r of the centred ranks pooled across industries. Permutation p-values are one-sided, with y shuffled within industry (10,000 draws); intervals are percentile bootstrap intervals with units resampled within industry (10,000 resamples). Seeds: 440041 (H_Spread), 440042 (H_Tier), 440043 (H_Separation). α = 0.05 per test, with no multiplicity correction; verdicts rest on the pre-set thresholds. For comparability with v0.41 and v0.42, the uncentred statistic of the r0 draft is reported beside ρ_pw for H_Tier and H_Separation; no verdict reads it.

## 2.4 Hypotheses and verdict rules

The three primary hypotheses are quoted from the pre-registration (§2.2--§2.4).

**H_Spread (§2.2).** "In most of the new industries, recall Presence on N3 varies across the industry's brands well beyond run-to-run noise." For each industry, SD_i is the population standard deviation of π̂_b over its non-ghost units; an industry shows spread if SD_i ≥ 0.15. CONFIRMED if 6 or more of the 8 industries show spread, FALSIFIED if 3 or fewer, MARGINAL if 4 or 5.

**H_Tier (§2.3).** "Within industries, leaders (L) have higher Presence than challengers (C), and challengers than smaller brands (S)." With tier scored L = 3, C = 2, S = 1 and y = π̂_b over the 156 non-ghost units, ρ_tier = ρ_pw(tier, π̂). CONFIRMED if ρ_tier ≥ 0.40 and p < 0.05, FALSIFIED if ρ_tier < 0.20, MARGINAL otherwise.

**H_Separation (§2.4).** "Across the new industries, how consistently the three models name a brand does not follow how often they name it." Over rated units (a ghost counts if rated), ρ_sep = ρ_pw(π̂, C_φ) with a two-sided bootstrap interval. UNDETERMINED if fewer than 40 units are rated; CONFIRMED if |ρ_sep| ≤ 0.50 and the 95% interval lies strictly inside (−0.70, 0.70); FALSIFIED if |ρ_sep| > 0.50; MARGINAL otherwise.

## 2.5 Manipulation checks and descriptives

Seven manipulation checks were pre-registered (§2.5): MC_Complete (at least 98% of the 909 calls answered; a model below 90% in a phase is dropped from it), MC_Served (served model equals requested model), MC_Truncation (share of calls ending at the output cap; above 5% flagged), MC_Window (all calls inside the window and within 72 hours), MC_Parity (gate P1: the imported kernels reproduce v0.41's π̂ and φ for all 112 omnibus brands; gate P2: the probe file's SHA-256 equals the locked value and every sent prompt equals its probe), MC_Budget (spend at or below $100) and MC_Alias (every match of a case-sensitive alias exported with its sentence for an audit table; reported, never used to change codes). Nine descriptives carry no verdict (§2.6): Presence by industry, tier and model; recognition and the recognition--recall gap; the three ghosts; run-to-run reliability; model agreement; brands named that are not registry units; the three companies present in two industries; answer form; and cost.

## 2.6 Pre-registration, lock and deviations

The pre-registration (r1) was written on 10 November 2026 with its acquisition, coding and scoring scripts and 68 unit tests, and locked as tag `v0.44-prereg-r1` on 11 November 2026 (03:02 UTC) after the pre-registrant waived the 24-hour review; the pharmacy industry stayed in (DEVIATIONS Entry 1). The pre-registration, registries, scripts, deviations record and lock manifest were deposited on OSF (`ec6wh/v44`) and an anchor file naming the tagged commit was written before the first call. DEVIATIONS Entry 2, written ex ante on 11 November, records that two kinds of refusal leave no refusal finish reason in the raw record, so that refusal counts are lower bounds; Entry 3, written after the collection, records two refused starts (§3.1). The statistics were computed once by `score_v0_44.py --run` after gates P1 and P2 passed; the scorer refuses to run a second time.

# 3. Results

## 3.1 Collection

The collection ran on 24 November 2026. The first call started at 00:08 US Central (06:08:51 UTC). The main pass ended at 01:32 with 906 of 909 calls answered: 3 gemini-4-argon recognition calls on hotel brands (HOT_A_HOT03, HOT_A_HOT04, HOT_A_HOT05) ended at 01:09 with a ConnectTimeout error, before any answer or usage was recorded. The pre-registered re-run pass (§4.4) started at 02:07 and answered all 3 for $0.000456. The last call ended at 02:08 (08:08:18 UTC), 1.99 hours after the first. The raw file holds 912 lines, one per attempt record (909 answered calls and the 3 errors). Recorded spend was $9.77; neither the $80 pause nor the block-1 projection pause was reached.

Two starts were refused by the script's own guards before any request was sent, and are disclosed here. (1) At 00:07 the launch command written in the pre-registration (§4.7), `nohup caffeinate -i python3 osf/v44/scripts/acquire_v0_44.py --collect`, was refused by the one-paid-collection-at-a-time guard (§4.6): the guard found the `caffeinate` wrapper's own process, whose command line contains `--collect`, and read it as another collection (`osf/v44/data/collect_v0_44_refused_0008.log`). The collection was restarted with the same script and flag, launched as a background process under `nohup` (`python3 osf/v44/scripts/acquire_v0_44.py --collect &`), with `caffeinate -i -w` on that process keeping the machine awake beside it. Only the keep-awake wrapper changed; the script, its guards, probes, settings and budget rules did not. (2) At 02:07 the first start of the re-run pass stopped before any network call because the providers' API keys were not set in the non-login shell it was launched from; it was restarted in a login shell (`zsh -ic`), which is the start recorded in `osf/v44/data/collect_v0_44_rerun.log`. The refused re-run start left no log file. Both events are recorded in DEVIATIONS Entry 3 (24 November 2026). Neither event sent a request, changed a recorded answer or used budget.

## 3.2 Manipulation checks

All pre-registered manipulation checks passed (Table 2). No model fell below 90% of its calls in either phase, so no model was dropped and the three primary tests use all three models.

| Check | Result | Verdict |
|---|---|---|
| MC_Complete | 909 of 909 calls answered (100.0%); every model 144/144 in Phase B and 159/159 in Phase A | PASS |
| MC_Served | 0 served IDs differing from the requested ID | PASS |
| MC_Truncation | 0 calls ended at the 16,384-token cap; none flagged | PASS |
| MC_Window | 00:08 to 02:08 US Central on 24 November (1.99 h), inside 2026-11-24 to 2026-11-28 | PASS |
| MC_Parity P1 | kernels reproduce v0.41's π̂ and φ for all 112 omnibus brands | PASS |
| MC_Parity P2 | probe SHA-256 equals the locked value; 0 prompt mismatches in 912 raw lines | PASS |
| MC_Budget | $9.77 recorded against the $100 cap; 0 design calls never sent | PASS |
| MC_Alias | 1,507 case-sensitive alias matches in 361 answers, 27 units, exported with their sentences | reported (no verdict) |

: Pre-registered manipulation checks (`v44_verdicts.json`, `manipulation_checks`; MC_Alias from `data/coded/v44_alias_audit.csv`).

Coding produced 477 Phase A rows (159 brands × 3 models) and 8,586 Phase B rows (each answer × each unit of its industry), of which 2,929 record a mention. The MC_Alias export lists every match of the 45 aliases matched case-sensitively; Table A1 (Appendix) counts them per unit and alias. As pre-registered, the audit table is reported and was not used to change any code; no reading of the exported sentences, by a person or a model, was registered, and none was made.

## 3.3 H_Spread: Presence separates brands in every industry (CONFIRMED)

Recall Presence varied widely across the brands of every industry. The standard deviation of π̂ ranged from 0.267 (fashion and luxury) to 0.377 (convenience stores and gas stations), and all 8 of 8 industries reached the 0.15 threshold; the lowest bootstrap lower bound, 0.191 (clothing and department stores), is also above it (Table 3, Figure 1). Every industry had at least one brand that no answer named (Table 3). H_Spread is **CONFIRMED**.

| Industry | n | SD of π̂ | 95% CI | Range | Share at 0 | Spread |
|---|---:|---:|---|---|---:|---|
| Car insurance | 22 | 0.336 | 0.266–0.382 | 0.00–1.00 | 27% | yes |
| Hotel chains | 20 | 0.343 | 0.213–0.408 | 0.00–0.98 | 45% | yes |
| Grocery store chains | 19 | 0.362 | 0.219–0.441 | 0.00–1.00 | 42% | yes |
| Fast-food chains | 21 | 0.315 | 0.215–0.373 | 0.00–0.98 | 10% | yes |
| Clothing and department stores | 16 | 0.278 | 0.191–0.338 | 0.00–0.94 | 6% | yes |
| Pharmacies | 15 | 0.350 | 0.248–0.403 | 0.00–0.96 | 20% | yes |
| Convenience stores and gas stations | 19 | 0.377 | 0.290–0.426 | 0.00–1.00 | 26% | yes |
| Fashion and luxury | 24 | 0.267 | 0.203–0.310 | 0.00–0.83 | 12% | yes |

: H_Spread per industry over non-ghost units: population SD of π̂ with its bootstrap 95% interval (seed 440041), range and share of units never named (`verdicts.H_Spread.per_industry`).

![Standard deviation of recall Presence per industry with its bootstrap 95% interval, against the registered threshold.](../../reports/figs/v44/paper/fig_01_spread.pdf){#fig:spread width=100%}

**Reported alongside.** Per model, the standard deviation of π̂ over all units of an industry (ghosts included) was at least 0.25 in every model-industry pair (the lowest: Gemini 4 Argon, fashion and luxury; Table 8). The pre-registration also asked for the same statistic on the omnibus on N3 at t₄ if v0.42 had been scored. It had been, but the locked v0.44 scorer does not compute it; it was computed after scoring from v0.42's scored brand table (`osf/v42/v42_brand_table.csv` at commit `31c64c6`, column `pi_N3_S0`, population SD per category) and carries no verdict. On N3 at t₄, the SD was 0.294 for headphones (n = 16), 0.308 for skincare, 0.294 for cosmetics, 0.275 for cars and 0.156 for spirits (n = 24 each): 5 of 5 categories at or above 0.15.

## 3.4 H_Tier: Presence rises from smaller brands to leaders (CONFIRMED)

Within industries, recall Presence followed the tier set by the public rankings: ρ_tier = 0.558 (bootstrap 95% CI 0.408–0.677; one-sided permutation p = 0.00010, the smallest value 10,000 draws allow; n = 156). The estimate and its whole interval are above the 0.40 threshold. H_Tier is **CONFIRMED**. Leaders had a higher mean π̂ than challengers in 8 of 8 industries, and challengers than smaller brands in 7 of 8 (the exception is fast food, where the sampled smaller chains, among them In-N-Out Burger, Crumbl and Cava, averaged 0.26 against 0.22 for challengers; Table 5, Figure 2). Per industry, ρ ranged from 0.374 (fashion and luxury) to 0.775 (hotel chains).

| Specification | n | ρ_pw | 95% CI | p (perm.) | Uncentred |
|---|---:|---:|---|---|---:|
| **Registered: tier (L = 3, C = 2, S = 1)** | 156 | **0.558** | 0.408–0.677 | < 0.001 | 0.583 |
| Eligible rank (x = −rank) | 156 | 0.599 | 0.441–0.705 | < 0.001 | 0.620 |
| Without fashion and luxury | 132 | 0.611 | 0.458–0.728 | < 0.001 | 0.628 |
| Without Health Mart and Good Neighbor Pharmacy | 154 | 0.564 | 0.408–0.683 | < 0.001 | 0.595 |

: H_Tier and its pre-registered variants (seed 440042; `verdicts.H_Tier` and `.reported_alongside`). "Uncentred" is the r0 statistic, reported for comparability only.

| Industry | Mean π̂, L | Mean π̂, C | Mean π̂, S | ρ (tier) | ρ (eligible rank) |
|---|---:|---:|---:|---:|---:|
| Car insurance | 0.69 | 0.37 | 0.13 | 0.679 | 0.641 |
| Hotel chains | 0.56 | 0.24 | 0.00 | 0.775 | 0.774 |
| Grocery store chains | 0.54 | 0.25 | 0.00 | 0.592 | 0.714 |
| Fast-food chains | 0.53 | 0.22 | 0.26 | 0.484 | 0.573 |
| Clothing and department stores | 0.64 | 0.27 | 0.24 | 0.658 | 0.603 |
| Pharmacies | 0.49 | 0.36 | 0.00 | 0.393 | 0.450 |
| Convenience stores and gas stations | 0.63 | 0.50 | 0.10 | 0.591 | 0.577 |
| Fashion and luxury | 0.45 | 0.36 | 0.22 | 0.374 | 0.478 |

: Mean recall Presence by tier and per-industry rank correlations (descriptive; `reported_alongside.mean_pi_by_industry_tier`, `per_industry_rho`). Clothing and department stores have two S units, pharmacies one.

![Mean recall Presence of the three tiers in each industry, with the per-industry rank correlation.](../../reports/figs/v44/paper/fig_02_tier.pdf){#fig:tier width=100%}

Every pre-registered variant met the same rule as the registered test. With the eligible rank in place of the three-level tier the correlation was 0.599; without fashion and luxury, whose second source uses AI discovery signals, it was 0.611; without the two pharmacy units placed from a different metric it was 0.564 (pharmacies alone: 0.479).

## 3.5 H_Separation: Consistency does not follow Presence among rated brands (CONFIRMED)

85 brands were rated, above the minimum of 40: their φ was defined in at least two of three runs and their π̂ was at least 1/6. Among them, scaled Consistency was unrelated to recall Presence: ρ_sep = 0.019, bootstrap 95% CI −0.249 to 0.269 (seed 440043). The absolute value is far below 0.50 and the interval lies inside (−0.70, 0.70). H_Separation is **CONFIRMED** (Figure 3). With raw φ_b in place of C_φ the statistic is −0.019, its exact negative, as the scaling implies; the uncentred comparability value is 0.156. Among rated brands, C_φ ranged from 54.6 to 100.0. Two ghosts, A&P and Rite Aid, were rated and are included, as the pre-registration allows.

![Scaled Consistency against recall Presence for each rated brand.](../../reports/figs/v44/paper/fig_03_separation.pdf){#fig:separation width=100%}

**Reported alongside.** Per industry (descriptive; between 8 and 16 rated brands each), ρ was −0.342 for car insurance, −0.156 for hotel chains, −0.558 for grocery, 0.103 for fast food, −0.173 for clothing and department stores, 0.350 for pharmacies, 0.318 for convenience and fuel and 0.149 for fashion and luxury. Of the 477 brand-runs, φ was defined in 317, zero (no model named the brand) in 134 and saturated in 26. Across brands, 105 had a defined φ_b, 38 were zero in every run, 6 were saturated and 10 undefined. Unrated brands were concentrated among smaller brands: 33 of 44 smaller brands were unrated, against 30 of 64 challengers, 10 of 48 leaders and 1 of 3 ghosts (Table 6).

| Industry | Unrated | | Industry | Unrated |
|---|---|---|---|---|
| Car insurance | 11 of 23 | | Clothing and department stores | 5 of 16 |
| Hotel chains | 12 of 20 | | Pharmacies | 7 of 16 |
| Grocery store chains | 12 of 20 | | Convenience stores and gas stations | 8 of 19 |
| Fast-food chains | 11 of 21 | | Fashion and luxury | 8 of 24 |

: Unrated units per industry, all tiers including ghosts (`reported_alongside.unrated_share_by_industry_tier`, summed over tiers).

## 3.6 Summary of verdicts

| Test | Statistic | Threshold | Verdict |
|---|---|---|---|
| H_Spread | 8 of 8 industries with SD ≥ 0.15 (SD 0.267--0.377) | ≥ 6 of 8 | CONFIRMED |
| H_Tier | ρ_pw = 0.558 (0.408–0.677), p < 0.001, n = 156 | ρ ≥ 0.40 and p < 0.05 | CONFIRMED |
| H_Separation | ρ_pw = 0.019 (−0.249 to 0.269), n = 85 | \|ρ\| ≤ 0.50, CI inside ±0.70 | CONFIRMED |

: Primary verdicts as written by `score_v0_44.py --run` (`v44_verdicts.json`, `verdicts`).

## 3.7 Descriptives

The nine pre-registered descriptives carry no verdicts (`v44_verdicts.json`, `descriptives`).

**1. Presence by industry, tier and model.** Table 8 gives the mean and SD of π̂ per model over all units of each industry, and Table A2 (Appendix) the mean per model and tier. The three models' industry means are close: the largest difference between two models' means in one industry is 0.14 (pharmacies).

| Industry | Fable 5.2 | GPT-6 Astra | Gemini 4 Argon |
|---|---|---|---|
| Car insurance | 0.36 (0.34) | 0.36 (0.33) | 0.35 (0.36) |
| Hotel chains | 0.28 (0.36) | 0.25 (0.34) | 0.27 (0.35) |
| Grocery store chains | 0.27 (0.35) | 0.26 (0.36) | 0.29 (0.35) |
| Fast-food chains | 0.30 (0.32) | 0.33 (0.32) | 0.34 (0.32) |
| Clothing and department stores | 0.45 (0.33) | 0.41 (0.28) | 0.36 (0.28) |
| Pharmacies | 0.40 (0.35) | 0.30 (0.35) | 0.44 (0.35) |
| Convenience stores and gas stations | 0.49 (0.39) | 0.42 (0.39) | 0.39 (0.39) |
| Fashion and luxury | 0.32 (0.30) | 0.34 (0.30) | 0.31 (0.25) |

: Mean recall Presence per model and industry (SD in brackets), over all units including ghosts (descriptive 1, `<model>|<industry>|all`).

**2. Recognition and the recognition--recall gap.** Recognition was near its ceiling: Claude Fable 5.2 recognised 156/159 brands, GPT-6 Astra 156/159 and Gemini 4 Argon 154/159 (Table 9). 36 brands were recognised by all three models yet never named in any category answer (π̂ = 0): 22 smaller brands, 12 challengers, 1 leader and 1 ghost.

| Industry | Fable 5.2 | GPT-6 Astra | Gemini 4 Argon |
|---|---:|---:|---:|
| Car insurance | 22/23 | 22/23 | 22/23 |
| Hotel chains | 20/20 | 20/20 | 20/20 |
| Grocery store chains | 20/20 | 20/20 | 20/20 |
| Fast-food chains | 19/21 | 20/21 | 18/21 |
| Clothing and department stores | 16/16 | 16/16 | 16/16 |
| Pharmacies | 16/16 | 16/16 | 16/16 |
| Convenience stores and gas stations | 19/19 | 18/19 | 18/19 |
| Fashion and luxury | 24/24 | 24/24 | 24/24 |
| **All** | **156/159** | **156/159** | **154/159** |

: Brands recognised per model and industry, of all units including ghosts (descriptive 2, `share_per_model_industry`).

**3. Ghosts.** All three models recognised each ghost as a brand of its industry (Esurance 3 of 3, A&P 3 of 3, Rite Aid 3 of 3). In open answers Esurance was never named (π̂ = 0.00), while A&P (π̂ = 0.17) and Rite Aid (π̂ = 0.28) were. Whether those answers present them as current was not coded.

**4. Run-to-run reliability.** The rank order of a model's counts repeated closely across runs: rel1 (mean ρ_pw over the three run pairs) was 0.949 for Claude Fable 5.2, 0.962 for GPT-6 Astra and 0.949 for Gemini 4 Argon; the three-run reliability rel3 was 0.982, 0.987 and 0.982.

**5. Model agreement.** Pairwise ρ_pw of per-model recall over all 159 units was 0.906 (Fable--Astra), 0.925 (Fable--Argon) and 0.858 (Astra--Argon).

**6. Brands named outside the registries.** The heuristic extraction of bold spans and list-item heads found between 112 and 202 distinct candidate names per industry that match no registry alias (Table A3). The most frequent are brands that the tier rule or its sources left out: for example Trader Joe's and Costco in grocery, Drury Hotels and hotel sub-brands such as The Ritz-Carlton in hotels, Raising Cane's and Shake Shack in fast food, Bloomingdale's and Uniqlo in clothing, Amazon Pharmacy in pharmacies, Buc-ee's in convenience and fuel, and Tom Ford in fashion. The list also holds non-brand strings ("Pros", "Cons", "Bottom line") and advertising characters, as expected of a heuristic.

**7. Companies in two industries.** π̂ in the grocery and the pharmacy frame was 0.35 and 0.33 for Kroger, 1.00 and 0.80 for Publix, and 0.19 and 0.13 for Albertsons.

**8. Answer form.** Category answers averaged 250 words (Claude Fable 5.2), 368 (GPT-6 Astra) and 778 (Gemini 4 Argon) and named 6.99, 6.59 and 6.76 registry units on average. Recognition answers averaged 15.3, 1.0 and 1.3 words. Every answered call ended normally (Claude end_turn 303; GPT completed 303; Gemini STOP 303). Recorded refusals were 0, 0 and 0, unanswered calls 0, 0 and 0, and ambiguous recognition answers 0, 0 and 0. The raw file records 0 empty answers and 0 calls re-sent after an empty answer, so none of the calls could hide one of the two kinds of refusal that DEVIATIONS Entry 2 says leave no refusal finish reason.

**9. Cost.** Spend from recorded usage was $9.77 (Table 10), $9.27 for the category questions and $0.49 for the recognition questions, below the pre-registered central estimate. No usage part was estimated at its worst case (0 parts).

| Model (phase) | Billed requests | Input tokens | Output tokens | Of which thinking | Cost |
|---|---:|---:|---:|---:|---:|
| Claude Fable 5.2 (B) | 144 | 4,950 | 131,790 | 0 | $2.66 |
| Claude Fable 5.2 (A) | 159 | 6,629 | 16,016 | 0 | $0.35 |
| GPT-6 Astra (B) | 144 | 3,426 | 97,822 | 22,111 | $4.93 |
| GPT-6 Astra (A) | 159 | 3,823 | 1,682 | 650 | $0.12 |
| Gemini 4 Argon (B) | 144 | 7,020 | 167,772 | 0 | $1.69 |
| Gemini 4 Argon (A) | 159 | 7,825 | 909 | 0 | $0.02 |
| **All** | | | | | **$9.77** |

: Tokens and cost per model and phase from recorded usage at the listed prices (descriptive 9). Gemini 4 Argon's Phase A has 162 raw lines for 159 billed requests (the three timed-out attempts).

# 4. Discussion

On the newest models and in eight industries the programme had not measured, both components behaved as they did on the premium consumer-goods base. Presence separated brands within every industry, as it did in four of the five omnibus categories on the legacy panel; on the same three models, all five omnibus categories also cleared the spread threshold (a comparison computed after scoring, §3.3). It followed the industries' public market order with a moderate pooled correlation, and Consistency was separable from Presence. For services and retail, AI naming is therefore neither uniform nor random: the models name some chains, insurers and stores far more than others, and largely the ones that lead their industry on sales, premiums, locations or store counts.

The tier correlation leaves much of the ordering unexplained, and the per-industry values differ: highest in hotels and car insurance, lowest in pharmacies and fashion and luxury. Several reasons are visible in the registries rather than in the models. Tiers come from heterogeneous metrics that order size or salience, not one common quantity; hotel groups known to guests by their sub-brands (IHG, Choice, Wyndham) and multi-banner retailers are measured as one master brand; and the extraction of non-registry names shows that the answers often name brands the tier rule excluded, such as Trader Joe's, Costco, Raising Cane's or Buc-ee's, and hotel sub-brands. A registry built from a ranking measures the ranking's brands, not the set the models consider; the gap between the two is itself an AI-availability fact for the excluded brands, which this wave does not score.

Recognition was nearly saturated, as on the omnibus, so almost all the information is in recall. 36 brands, most of them smaller brands and challengers, were recognised by every model and never named in an open answer. That recognition--recall gap is the distance between being known and being suggested that the Presence measure was designed to capture.

The separation result rests on 85 rated brands, and rating removes most smaller brands, because φ is undefined or zero when the models rarely name a brand. H_Separation therefore says that among brands the models name at least occasionally, how consistently they name a brand does not follow how often; it says nothing about Consistency among rarely named brands. Among rated brands C_φ ranged from 54.6 to 100.0, with most values in the upper part of that range (Figure 3), so the test compares brands within a narrow band of high agreement.

# 5. Limitations

1. Tiers come from heterogeneous public metrics, some from reproductions of the original tables (NAIC via Agency Checklists, QSR 50 via FoodIndustry.com, DCI figures via Becker's); within an industry they order size or salience, not one common quantity.
2. Fashion and luxury rests on global sources and on the Lyst Index, which uses AI discovery signals; H_Tier holds without it (§3.4).
3. Some company totals cover several banners while the unit is one banner, and house-of-brands hotel groups are named by group names that guests may know by their sub-brands, which lowers their measured Presence.
4. Three models and three runs: φ is noisier than on six models, and the rated set excludes most smaller brands (§3.5).
5. No web search: the results describe the models' own knowledge, not what a search-enabled assistant retrieves.
6. One market and language (US English), one collection on one night, no retest.
7. The alias matcher is new. It matched an independent ground truth on synthetic answers before the lock, but it is not validated on these answers: the MC_Alias table of 1,507 case-sensitive matches is exported, not reviewed, and no human or model check of the coding was registered.
8. Grocery and pharmacy share three company names, measured in different frames and not independent.
9. ρ_pw centres ranks within industry, so its values are not computed identically to v0.41's and v0.42's uncentred statistic; the uncentred values are reported beside it.
10. The omnibus spread comparison (§3.3) was computed after scoring from another study's scored table, because the locked scorer does not output it; it carries no verdict.
11. Refusal counts are lower bounds (DEVIATIONS Entry 2); the launch of the collection differed from the pre-registered command in its keep-awake wrapper only (§3.1; DEVIATIONS Entry 3).

# 6. Future Research

The scores of these eight industries on the current panel are the first for them, and later waves (the Ranking, Sentiment, Coverage and Grounding papers) may reuse them under their own pre-registrations. A retest on the same registries and questions would show whether the industries' orders hold over time, as Presence did on the omnibus. A registry that also includes the brands the models name outside the ranking-based units (descriptive 6) would separate what the models know from what the rankings list. A search-on arm, which this wave left out to stay within budget, would show whether retrieval changes which chains and insurers are named.

# Declarations {-}

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. The brand registries of this study were built from dated public rankings by fixed rules and screened for Samsung-group ownership and relationships before any collection (DEVIATIONS Entry 0). The screen found no registry brand owned by a Samsung-group company; it checked the owners named by the registry sources against a list of Samsung-group companies and brands and did not open an ownership filing for each brand. Items of record: in the pharmacy registry, Samsung Bioepis, a Samsung affiliate, supplies private-label biosimilars to subsidiaries of the companies behind two registry units, Cordavis (CVS Caremark, CVS Health; unit CVS Pharmacy) and Quallent (Express Scripts; unit Express Scripts). Following the handling of the supply relationships disclosed in v0.22, this relationship is characterized as non-competitive with no brand-level overlap, and no operational restriction on registry composition was imposed. Two other pharmacy units belong to retailers (Walmart, Costco) that also sell Samsung products. Samsung affiliates operate in three of the eight industries outside the US market (insurance: Samsung Fire & Marine and Samsung Life; hotels: Hotel Shilla; fashion: Samsung C&T); none of their brands is in the registries, and whether their stores sell any registry brand was not screened. Whether Cheil Worldwide, a Samsung-affiliated advertising company, serves any registry brand was not screened (client lists are not public). Industries in which Samsung Electronics competes, or whose US companies are its device and network customers (telecom, media and streaming), were not selected, nor were pharmaceutical manufacturers, among which a Samsung affiliate markets biosimilars. Acquisition, coding and scoring are fully automated against registries locked and deposited before the first call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

## Funding {-}

Self-funded.

## Ethics {-}

Not applicable; no human subjects.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## Data and code availability {-}

The locked pre-registration, probe file, cost estimate, registries with their sources, scripts and tests, deviations record and lock manifest are deposited at OSF (osf.io/ec6wh), `v44/`. The raw answers (`data/v44_raw.jsonl`), collection logs, coded tables (`data/coded/`), verdict file (`v44_verdicts.json`) and unit table (`v44_unit_table.csv`) are in the programme's repository (github.com/thirdsystem-aias/aias, branch `v0.44`, `osf/v44/`) and are planned for OSF with the study's data deposit. Every number in this paper is read from `papers/v0_44/v44_values.json`, written by `papers/v0_44/values_v0_44.py` from those files, which names the source file and field of each value; the figures are drawn by `scripts/build_charts_v44_paper.py`.

# References {-}

González Castro, P. U. (2026a). *AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval*. SSRN 6659000.

González Castro, P. U. (2026b). *The AIAS™ Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy* (v1.2). SSRN 6761698.

González Castro, P. U. (2026c). *The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification (v1.3)*. SSRN 6797679.

González Castro, P. U. (2026d). *The AIAS Presence Measurement Protocol v1.4: Recognition × Recall Decomposition and Multi-Component AI Availability*. SSRN 6799479.

González Castro, P. U. (2026e). *The AIAS™ Presence Measurement Protocol: Multi-Statistic C2 Specification and Two-Channel Recall Decomposition* (v1.5). SSRN 6810758.

González Castro, P. U. (2026f). *Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension* (AIAS Methodology v1.6). SSRN 6816340.

González Castro, P. U. (2026g). *Consistency without Independence: A Pre-Registered Test of Coefficient-of-Variation as the Consistency Component of AIAS™* (v1.7). SSRN 6878818.

González Castro, P. U. (2026h). *A Mean-Independent Consistency Instrument for Cross-Model AI Presence: Redesigning CPC on a Quasi-Binomial Dispersion Basis* (AIAS Methodology v1.8). SSRN 6963359.

González Castro, P. U. (2026i). *One Score or Two? Calibrating a Presence and Consistency Composite for AI Brand Availability: A Pre-Registered Calibration with Blind Five-Month Confirmation (AIAS™ Methodology v1.9)*. Third System, <https://thirdsystem.ai/studies/v1-9/>; OSF, <https://osf.io/ec6wh/files/osfstorage/6af1fd459966c813ee53ba87>.

González Castro, P. U. (2026j). *AI Availability as a Third Measurable Layer of Brand Availability: Five-Substrate Empirical Anchoring of the AIAS™ Presence Measurement Protocol --- Synthesis under Locked v1.6 Methodology* (AIAS 1.0). SSRN 6817841.

González Castro, P. U. (2026k). *Presence and Consistency: A Two-Component Measurement of AI Availability. The AIAS™ 2.0 Synthesis*. OSF `ec6wh/aias_2_0`.

González Castro, P. U. (2026l). *Tri-System Brand Growth: The AI Mediation Layer*. MSI Working Paper, Report No. 26-132. Marketing Science Institute.

González Castro, P. U. (2026m). *Predictive Validity of AI Presence Index Against Google Trends Search Interest on the B2B SaaS Substrate: Construct Validity Pilot Under Protocol v1.6* (v0.25). Third System, <https://thirdsystem.ai/studies/v0-25/>.

González Castro, P. U. (2026p). *Five-Month Stability of AI Brand Consistency and Presence: A Pre-Registered Third Wave on a Retiring Six-Model Panel* (AIAS™ v0.41). Third System, <https://thirdsystem.ai/studies/v0-41/>; OSF `ec6wh/v41`.

Romaniuk, J., & Sharp, B. (2016). *How Brands Grow: Part 2*. Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

Programme records cited by version (OSF `ec6wh`; github.com/thirdsystem-aias/aias): the omnibus registries and phase papers of v0.19 (audiophile headphones, SSRN 6809182), v0.20 (skincare, SSRN 6811441), v0.21 (cosmetics, SSRN 6815378), v0.22 (automotive, SSRN 6829118) and v0.23 (premium spirits, SSRN 6834298); the t₄ wave v0.42 (pre-registration `v0.42-prereg-r1`, OSF `ec6wh/v42`), whose panel and call settings this wave uses and whose scored brand table gives the omnibus comparison of §3.3.

\clearpage

# Appendix {-}

\setcounter{table}{0}
\renewcommand{\thetable}{A\arabic{table}}

| Industry | Unit | Matches | Aliases matched (count) |
|---|---|---:|---|
| Convenience stores and gas stations | QuikTrip | 176 | QuikTrip (98); QT (78) |
| Pharmacies | CVS Pharmacy | 143 | CVS (115); CVS Pharmacy (23); CVS Caremark (5) |
| Car insurance | Erie Insurance | 127 | Erie (88); Erie Insurance (39) |
| Grocery store chains | H-E-B | 124 | H-E-B (124) |
| Hotel chains | IHG | 110 | IHG (83); IHG One Rewards (14); IHG Hotels (8); InterContinental Hotels Group (5) |
| Car insurance | USAA | 90 | USAA (90) |
| Car insurance | Progressive | 80 | Progressive (80) |
| Convenience stores and gas stations | Love's | 80 | Love's (53); Love's Travel Stops (27) |
| Hotel chains | Four Seasons | 71 | Four Seasons (71) |
| Fashion and luxury | The Row | 66 | The Row (66) |
| Fashion and luxury | Tiffany & Co. | 64 | Tiffany (32); Tiffany & Co. (16); Tiffany & Co (16) |
| Clothing and department stores | Gap | 58 | Gap (49); Gap Inc (9) |
| Car insurance | Travelers | 50 | Travelers (50) |
| Car insurance | Farmers Insurance | 43 | Farmers (34); Farmers Insurance (9) |
| Fast-food chains | Chipotle | 36 | Chipotle (29); Chipotle Mexican Grill (7) |
| Car insurance | Nationwide | 34 | Nationwide (34) |
| Clothing and department stores | Ross Dress for Less | 32 | Ross (19); Ross Dress for Less (13) |
| Grocery store chains | A&P | 30 | A&P (27); Great Atlantic & Pacific Tea (3) |
| Grocery store chains | Sprouts Farmers Market | 27 | Sprouts (17); Sprouts Farmers Market (10) |
| Fashion and luxury | Coach | 15 | Coach (15) |
| Fast-food chains | Domino's | 13 | Domino's (13) |
| Clothing and department stores | Burlington | 12 | Burlington (10); Burlington Coat Factory (2) |
| Fashion and luxury | Celine | 11 | Celine (11) |
| Fast-food chains | Subway | 8 | Subway (8) |
| Car insurance | AAA | 5 | AAA (4); Auto Club (1) |
| Fast-food chains | Cava | 1 | Cava (1) |
| Fashion and luxury | Chloé | 1 | Chloé (1) |

: MC_Alias: case-sensitive alias matches per unit and alias (1,507 matches in 361 answers; `data/coded/v44_alias_audit.csv`, which also holds each match's sentence). Reported as pre-registered; not used to change any code.

| Industry | Tier | Fable 5.2 | GPT-6 Astra | Gemini 4 Argon |
|---|---|---:|---:|---:|
| Car insurance | L | 0.73 | 0.64 | 0.71 |
| Car insurance | C | 0.33 | 0.40 | 0.38 |
| Car insurance | S | 0.15 | 0.15 | 0.10 |
| Car insurance | G | 0.00 | 0.00 | 0.00 |
| Hotel chains | L | 0.60 | 0.53 | 0.56 |
| Hotel chains | C | 0.25 | 0.22 | 0.24 |
| Hotel chains | S | 0.00 | 0.00 | 0.00 |
| Grocery store chains | L | 0.54 | 0.55 | 0.55 |
| Grocery store chains | C | 0.25 | 0.21 | 0.28 |
| Grocery store chains | S | 0.00 | 0.00 | 0.01 |
| Grocery store chains | G | 0.17 | 0.17 | 0.17 |
| Fast-food chains | L | 0.55 | 0.52 | 0.52 |
| Fast-food chains | C | 0.15 | 0.24 | 0.26 |
| Fast-food chains | S | 0.25 | 0.25 | 0.28 |
| Clothing and department stores | L | 0.70 | 0.65 | 0.57 |
| Clothing and department stores | C | 0.30 | 0.28 | 0.24 |
| Clothing and department stores | S | 0.28 | 0.22 | 0.22 |
| Pharmacies | L | 0.47 | 0.46 | 0.55 |
| Pharmacies | C | 0.40 | 0.26 | 0.42 |
| Pharmacies | S | 0.00 | 0.00 | 0.00 |
| Pharmacies | G | 0.33 | 0.00 | 0.50 |
| Convenience stores and gas stations | L | 0.72 | 0.60 | 0.57 |
| Convenience stores and gas stations | C | 0.51 | 0.52 | 0.45 |
| Convenience stores and gas stations | S | 0.16 | 0.06 | 0.09 |
| Fashion and luxury | L | 0.49 | 0.47 | 0.38 |
| Fashion and luxury | C | 0.33 | 0.42 | 0.34 |
| Fashion and luxury | S | 0.22 | 0.20 | 0.24 |

: Mean recall Presence per model, industry and tier (descriptive 1, `<model>|<industry>|<tier>`). G = the industry's ghost (one unit).

| Industry | Distinct | Ten most frequent candidate names (count) |
|---|---:|---|
| Car insurance | 115 | Flo (6); LiMu Emu and Doug (5); Mayhem (5); Cons (4); Pros (4); The Catch (4); Chubb (4); Bottom line (4); Best for (3); If you have military ties (3) |
| Hotel chains | 149 | Drury Hotels (24); The Ritz-Carlton (21); Waldorf Astoria (16); Residence Inn (15); Holiday Inn Express (15); Ritz-Carlton (12); Kimpton (12); Hampton Inn (11); Westin (10); Holiday Inn (8) |
| Grocery store chains | 112 | Trader Joe's (43); Costco (37); Whole Foods Market (26); Market Basket (24); Walmart (9); Whole Foods (8); Central Market (8); Target (6); Winn-Dixie (6); Meijer (6) |
| Fast-food chains | 112 | Raising Cane's (26); Shake Shack (20); Whataburger (19); Five Guys (15); White Castle (7); KFC (6); Jersey Mike's (5); My short list (4); Bojangles (4); Jersey Mike's Subs (4) |
| Clothing and department stores | 148 | Bloomingdale's (39); Uniqlo (31); Target (22); J.Crew (21); Old Navy (21); Zara (16); Patagonia (14); Banana Republic (13); Neiman Marcus (13); Brooks Brothers (13) |
| Pharmacies | 202 | Amazon Pharmacy (27); Mark Cuban Cost Plus Drug Company (15); Sam's Club Pharmacy (14); Wegmans (13); H-E-B Pharmacy (12); Sam's Club (9); H-E-B (9); Mark Cuban Cost Plus Drugs (8); Independent pharmacies (7); Duane Reade (7) |
| Convenience stores and gas stations | 130 | Buc-ee's (39); Costco (13); The Vibe (8); Sinclair (7); Primary Region (7); Stuckey's (6); Texaco (6); Breakfast Pizza (6); Speedway (5); Shell (5) |
| Fashion and luxury | 128 | Tom Ford (15); Thom Browne (14); Loro Piana (13); Oscar de la Renta (12); Gabriela Hearst (10); Brunello Cucinelli (10); Toteme (8); Purple Label (8); Carolina Herrera (7); Alaïa (7) |

: Candidate names in category answers that match no registry alias (descriptive 6; heuristic: bold spans and list-item heads of 1--6 words). Includes non-brand strings; descriptive only.
