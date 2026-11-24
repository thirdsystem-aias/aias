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

The two locked components of AI Availability, Presence (how often AI answers name a brand) and Consistency (how evenly models agree in naming it), were established on premium consumer-goods categories and a retiring model panel. This pre-registered wave asks whether they behave the same way in service and retail industries on the newest models. The newest generally available flagship of three providers (Claude Fable 5.2, GPT-6 Astra and Gemini 4 Argon), without web search, answered six open category questions three times and one yes/no recognition question per brand about {{v:reg.units_total}} brands in eight US industries new to the programme: car insurance, hotel chains, grocery store chains, fast-food chains, clothing and department stores, pharmacies, convenience stores and gas stations, and fashion and luxury. Brands were placed in leader, challenger and smaller-brand tiers from dated public rankings by one fixed rule, and three brands that have left the US market were added as ghosts. All {{v:MC_Complete.answered}} of {{v:MC_Complete.expected}} planned calls were answered, {{v:raw.rerun_ok}} of them in the logged re-run pass, for {{v:MC_Budget.spend_usd}} against a $100 cap, and every manipulation check passed. Recall Presence spread across brands in {{v:H_Spread.n_with_spread}} of {{v:H_Spread.n_industries}} industries (standard deviation {{v:H_Spread.sd_min}} to {{v:H_Spread.sd_max}} against a threshold of 0.15; H_Spread {{v:H_Spread.verdict}}). Within industries it followed market tier (pooled within-industry Spearman ρ = {{v:H_Tier.rho}}, 95% CI {{v:H_Tier.ci}}, permutation p {{v:H_Tier.p}}, n = {{v:H_Tier.n}}; H_Tier {{v:H_Tier.verdict}}), also on the eligible rank (ρ = {{v:H_Tier.elig.rho}}) and without fashion and luxury (ρ = {{v:H_Tier.nofas.rho}}). Consistency did not follow Presence among the {{v:H_Sep.n}} brands with a rated Consistency score (ρ = {{v:H_Sep.rho}}, 95% CI {{v:H_Sep.ci}}; H_Separation {{v:H_Sep.verdict}}). Smaller brands were often recognised but never named, and most of them could not be rated for Consistency. Every pre-registered test, check and descriptive is reported.

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
| **Total** | **{{v:reg.units_total}}** | **48 / 64 / 44 / 3** | |

: Industries, units and tier sources (pre-registration §3.1; `osf/v44/registries/industries_v0_44.csv`).

Telecom, media and streaming, and pharmaceutical manufacturers were not selected on conflict-of-interest grounds (Declarations); education and travel booking for want of a dated public ranking that could be opened; utilities because most US households cannot choose them (pre-registration §3.3). Fashion and luxury rests on global sources, and the Lyst Index includes AI discovery signals among its inputs, so H_Tier is also reported without that industry.

## 2.2 Probes, panel and collection

Each industry has six open category questions (Phase B), filled from the omnibus templates of v0.20--v0.22 with the category noun, an expert group and "in the US": for example, "What are the best car insurance companies in the US? List several with descriptions." Three frames (q1--q3) ask for the best, the expert-recommended and the highest-quality brands; three (q4--q6) ask for the popular, those with the most loyal customers and those with the most iconic identity in popular culture. Each brand has one recognition question (Phase A): "Is the brand {brand} commonly recognized as a/an {category} brand? Answer yes or no." There is no system prompt. The probe file (207 lines; SHA-256 beginning `{{v:MC_Parity.P2.sha_short}}`) was locked with the pre-registration.

The panel is the newest generally available flagship of each of three providers, as verified for the programme's t₄ wave: Claude Fable 5.2 (`claude-fable-5-2`, through Anthropic's Message Batches API), GPT-6 Astra (`gpt-6-astra`) and Gemini 4 Argon (`gemini-4-argon`). Calls used no tools and no web search (condition S0), provider-default sampling and reasoning settings, and a cap of 16,384 output tokens. Each model answered the 48 category questions three times (runs 1--3) and the {{v:reg.units_total}} brand questions once: 3 × (48 × 3 + 159) = {{v:design.expected_total}} calls. Transient errors were retried up to three attempts, an empty answer was re-sent once, and one logged re-run pass inside the window was allowed (pre-registration §4.4). The budget was at most $100 of paid calls with a pause at $80, both from recorded usage; the pre-registered estimate was $27.24 central and $52.44 high. The collection window was 24 to 28 November 2026 (US Central), all calls within 72 hours of the first; the acquisition script refused to send outside the window, without the lock tag on the remote and its OSF anchor, or while another paid collection was running on the machine (§4.6).

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

The collection ran on 24 November 2026. The first call started at {{v:MC_Window.first_ct}} US Central ({{v:MC_Window.first_utc}} UTC). The main pass ended at {{v:raw.main_end_ct}} with {{v:raw.main_ok}} of {{v:MC_Complete.expected}} calls answered: {{v:raw.errors}} {{v:raw.error_model}} recognition calls on hotel brands ({{v:raw.error_probes}}) ended at {{v:raw.error_first_ct}} with a {{v:raw.error_kind}} error, before any answer or usage was recorded. The pre-registered re-run pass (§4.4) started at {{v:raw.rerun_start_ct}} and answered all {{v:raw.rerun_ok}} for {{v:raw.rerun_cost}}. The last call ended at {{v:MC_Window.last_ct}} ({{v:MC_Window.last_utc}} UTC), {{v:MC_Window.span_hours}} hours after the first. The raw file holds {{v:raw.lines}} lines, one per attempt record ({{v:MC_Complete.answered}} answered calls and the {{v:raw.errors}} errors). Recorded spend was {{v:MC_Budget.spend_usd}}; neither the $80 pause nor the block-1 projection pause was reached.

Two starts were refused by the script's own guards before any request was sent, and are disclosed here. (1) At 00:07 the launch command written in the pre-registration (§4.7), `nohup caffeinate -i python3 osf/v44/scripts/acquire_v0_44.py --collect`, was refused by the one-paid-collection-at-a-time guard (§4.6): the guard found the `caffeinate` wrapper's own process, whose command line contains `--collect`, and read it as another collection (`osf/v44/data/collect_v0_44_refused_0008.log`). The collection was restarted with the same script and flag, launched as a background process under `nohup` (`python3 osf/v44/scripts/acquire_v0_44.py --collect &`), with `caffeinate -i -w` on that process keeping the machine awake beside it. Only the keep-awake wrapper changed; the script, its guards, probes, settings and budget rules did not. (2) At 02:07 the first start of the re-run pass stopped before any network call because the providers' API keys were not set in the non-login shell it was launched from; it was restarted in a login shell (`zsh -ic`), which is the start recorded in `osf/v44/data/collect_v0_44_rerun.log`. The refused re-run start left no log file. Both events are recorded in DEVIATIONS Entry 3 (24 November 2026). Neither event sent a request, changed a recorded answer or used budget.

## 3.2 Manipulation checks

All pre-registered manipulation checks passed (Table 2). No model fell below 90% of its calls in either phase, so no model was dropped and the three primary tests use all three models.

| Check | Result | Verdict |
|---|---|---|
| MC_Complete | {{v:MC_Complete.answered}} of {{v:MC_Complete.expected}} calls answered ({{v:MC_Complete.share}}); every model 144/144 in Phase B and 159/159 in Phase A | {{v:MC_Complete.pass}} |
| MC_Served | {{v:MC_Served.n_mismatched}} served IDs differing from the requested ID | {{v:MC_Served.pass}} |
| MC_Truncation | {{v:MC_Truncation.at_cap_total}} calls ended at the 16,384-token cap; {{v:MC_Truncation.flagged}} | {{v:MC_Truncation.pass}} |
| MC_Window | {{v:MC_Window.first_ct}} to {{v:MC_Window.last_ct}} US Central on 24 November ({{v:MC_Window.span_hours}} h), inside {{v:budget.window}} | {{v:MC_Window.pass}} |
| MC_Parity P1 | kernels reproduce v0.41's π̂ and φ for all 112 omnibus brands | {{v:MC_Parity.P1}} |
| MC_Parity P2 | probe SHA-256 equals the locked value; {{v:MC_Parity.P2.prompt_mismatches}} prompt mismatches in {{v:MC_Parity.P2.lines_checked}} raw lines | {{v:MC_Parity.P2}} |
| MC_Budget | {{v:MC_Budget.spend_usd}} recorded against the $100 cap; {{v:MC_Budget.never_sent}} design calls never sent | {{v:MC_Budget.pass}} |
| MC_Alias | {{v:alias.matches}} case-sensitive alias matches in {{v:alias.answers}} answers, {{v:alias.units}} units, exported with their sentences | reported (no verdict) |

: Pre-registered manipulation checks (`v44_verdicts.json`, `manipulation_checks`; MC_Alias from `data/coded/v44_alias_audit.csv`).

Coding produced {{v:coded.a_rows}} Phase A rows (159 brands × 3 models) and {{v:coded.b_rows}} Phase B rows (each answer × each unit of its industry), of which {{v:coded.b_mentions}} record a mention. The MC_Alias export lists every match of the {{v:alias.aliases}} aliases matched case-sensitively; Table A1 (Appendix) counts them per unit and alias. As pre-registered, the audit table is reported and was not used to change any code; no reading of the exported sentences, by a person or a model, was registered, and none was made.

## 3.3 H_Spread: Presence separates brands in every industry ({{v:H_Spread.verdict}})

Recall Presence varied widely across the brands of every industry. The standard deviation of π̂ ranged from {{v:H_Spread.sd_min}} ({{v:H_Spread.sd_min_ind}}) to {{v:H_Spread.sd_max}} ({{v:H_Spread.sd_max_ind}}), and all {{v:H_Spread.n_with_spread}} of {{v:H_Spread.n_industries}} industries reached the 0.15 threshold; the lowest bootstrap lower bound, {{v:H_Spread.ci_low_min}} ({{v:H_Spread.ci_low_min_ind}}), is also above it (Table 3, Figure 1). Every industry had at least one brand that no answer named (Table 3). H_Spread is **{{v:H_Spread.verdict}}**.

| Industry | n | SD of π̂ | 95% CI | Range | Share at 0 | Spread |
|---|---:|---:|---|---|---:|---|
| Car insurance | {{v:H_Spread.INS.n}} | {{v:H_Spread.INS.sd}} | {{v:H_Spread.INS.ci}} | {{v:H_Spread.INS.range}} | {{v:H_Spread.INS.share0}} | {{v:H_Spread.INS.spread}} |
| Hotel chains | {{v:H_Spread.HOT.n}} | {{v:H_Spread.HOT.sd}} | {{v:H_Spread.HOT.ci}} | {{v:H_Spread.HOT.range}} | {{v:H_Spread.HOT.share0}} | {{v:H_Spread.HOT.spread}} |
| Grocery store chains | {{v:H_Spread.GRO.n}} | {{v:H_Spread.GRO.sd}} | {{v:H_Spread.GRO.ci}} | {{v:H_Spread.GRO.range}} | {{v:H_Spread.GRO.share0}} | {{v:H_Spread.GRO.spread}} |
| Fast-food chains | {{v:H_Spread.QSR.n}} | {{v:H_Spread.QSR.sd}} | {{v:H_Spread.QSR.ci}} | {{v:H_Spread.QSR.range}} | {{v:H_Spread.QSR.share0}} | {{v:H_Spread.QSR.spread}} |
| Clothing and department stores | {{v:H_Spread.APR.n}} | {{v:H_Spread.APR.sd}} | {{v:H_Spread.APR.ci}} | {{v:H_Spread.APR.range}} | {{v:H_Spread.APR.share0}} | {{v:H_Spread.APR.spread}} |
| Pharmacies | {{v:H_Spread.PHA.n}} | {{v:H_Spread.PHA.sd}} | {{v:H_Spread.PHA.ci}} | {{v:H_Spread.PHA.range}} | {{v:H_Spread.PHA.share0}} | {{v:H_Spread.PHA.spread}} |
| Convenience stores and gas stations | {{v:H_Spread.CVF.n}} | {{v:H_Spread.CVF.sd}} | {{v:H_Spread.CVF.ci}} | {{v:H_Spread.CVF.range}} | {{v:H_Spread.CVF.share0}} | {{v:H_Spread.CVF.spread}} |
| Fashion and luxury | {{v:H_Spread.FAS.n}} | {{v:H_Spread.FAS.sd}} | {{v:H_Spread.FAS.ci}} | {{v:H_Spread.FAS.range}} | {{v:H_Spread.FAS.share0}} | {{v:H_Spread.FAS.spread}} |

: H_Spread per industry over non-ghost units: population SD of π̂ with its bootstrap 95% interval (seed 440041), range and share of units never named (`verdicts.H_Spread.per_industry`).

![Standard deviation of recall Presence per industry with its bootstrap 95% interval, against the registered threshold.](../../reports/figs/v44/paper/fig_01_spread.pdf){#fig:spread width=100%}

**Reported alongside.** Per model, the standard deviation of π̂ over all units of an industry (ghosts included) was at least {{v:D1.sd_min}} in every model-industry pair (the lowest: {{v:D1.sd_min_where}}; Table 8). The pre-registration also asked for the same statistic on the omnibus on N3 at t₄ if v0.42 had been scored. It had been, but the locked v0.44 scorer does not compute it; it was computed after scoring from v0.42's scored brand table (`osf/v42/v42_brand_table.csv` at commit `31c64c6`, column `pi_N3_S0`, population SD per category) and carries no verdict. On N3 at t₄, the SD was {{v:omni.v0.19.sd}} for headphones (n = {{v:omni.v0.19.n}}), {{v:omni.v0.20.sd}} for skincare, {{v:omni.v0.21.sd}} for cosmetics, {{v:omni.v0.22.sd}} for cars and {{v:omni.v0.23.sd}} for spirits (n = 24 each): {{v:omni.n_spread}} of {{v:omni.n_sub}} categories at or above 0.15.

## 3.4 H_Tier: Presence rises from smaller brands to leaders ({{v:H_Tier.verdict}})

Within industries, recall Presence followed the tier set by the public rankings: ρ_tier = {{v:H_Tier.rho}} (bootstrap 95% CI {{v:H_Tier.ci}}; one-sided permutation p = {{v:H_Tier.p_exact}}, the smallest value 10,000 draws allow; n = {{v:H_Tier.n}}). The estimate and its whole interval are above the 0.40 threshold. H_Tier is **{{v:H_Tier.verdict}}**. Leaders had a higher mean π̂ than challengers in {{v:H_Tier.count_L_gt_C}} of 8 industries, and challengers than smaller brands in {{v:H_Tier.count_C_gt_S}} of 8 (the exception is fast food, where the sampled smaller chains, among them In-N-Out Burger, Crumbl and Cava, averaged {{v:H_Tier.mean.QSR.S}} against {{v:H_Tier.mean.QSR.C}} for challengers; Table 5, Figure 2). Per industry, ρ ranged from {{v:H_Tier.ind_rho_min}} ({{v:H_Tier.ind_rho_min_ind}}) to {{v:H_Tier.ind_rho_max}} ({{v:H_Tier.ind_rho_max_ind}}).

| Specification | n | ρ_pw | 95% CI | p (perm.) | Uncentred |
|---|---:|---:|---|---|---:|
| **Registered: tier (L = 3, C = 2, S = 1)** | {{v:H_Tier.n}} | **{{v:H_Tier.rho}}** | {{v:H_Tier.ci}} | {{v:H_Tier.p}} | {{v:H_Tier.rho_unc}} |
| Eligible rank (x = −rank) | {{v:H_Tier.elig.n}} | {{v:H_Tier.elig.rho}} | {{v:H_Tier.elig.ci}} | {{v:H_Tier.elig.p}} | {{v:H_Tier.elig.rho_unc}} |
| Without fashion and luxury | {{v:H_Tier.nofas.n}} | {{v:H_Tier.nofas.rho}} | {{v:H_Tier.nofas.ci}} | {{v:H_Tier.nofas.p}} | {{v:H_Tier.nofas.rho_unc}} |
| Without Health Mart and Good Neighbor Pharmacy | {{v:H_Tier.nopha.n}} | {{v:H_Tier.nopha.rho}} | {{v:H_Tier.nopha.ci}} | {{v:H_Tier.nopha.p}} | {{v:H_Tier.nopha.rho_unc}} |

: H_Tier and its pre-registered variants (seed 440042; `verdicts.H_Tier` and `.reported_alongside`). "Uncentred" is the r0 statistic, reported for comparability only.

| Industry | Mean π̂, L | Mean π̂, C | Mean π̂, S | ρ (tier) | ρ (eligible rank) |
|---|---:|---:|---:|---:|---:|
| Car insurance | {{v:H_Tier.mean.INS.L}} | {{v:H_Tier.mean.INS.C}} | {{v:H_Tier.mean.INS.S}} | {{v:H_Tier.INS.rho}} | {{v:H_Tier.elig.INS.rho}} |
| Hotel chains | {{v:H_Tier.mean.HOT.L}} | {{v:H_Tier.mean.HOT.C}} | {{v:H_Tier.mean.HOT.S}} | {{v:H_Tier.HOT.rho}} | {{v:H_Tier.elig.HOT.rho}} |
| Grocery store chains | {{v:H_Tier.mean.GRO.L}} | {{v:H_Tier.mean.GRO.C}} | {{v:H_Tier.mean.GRO.S}} | {{v:H_Tier.GRO.rho}} | {{v:H_Tier.elig.GRO.rho}} |
| Fast-food chains | {{v:H_Tier.mean.QSR.L}} | {{v:H_Tier.mean.QSR.C}} | {{v:H_Tier.mean.QSR.S}} | {{v:H_Tier.QSR.rho}} | {{v:H_Tier.elig.QSR.rho}} |
| Clothing and department stores | {{v:H_Tier.mean.APR.L}} | {{v:H_Tier.mean.APR.C}} | {{v:H_Tier.mean.APR.S}} | {{v:H_Tier.APR.rho}} | {{v:H_Tier.elig.APR.rho}} |
| Pharmacies | {{v:H_Tier.mean.PHA.L}} | {{v:H_Tier.mean.PHA.C}} | {{v:H_Tier.mean.PHA.S}} | {{v:H_Tier.PHA.rho}} | {{v:H_Tier.elig.PHA.rho}} |
| Convenience stores and gas stations | {{v:H_Tier.mean.CVF.L}} | {{v:H_Tier.mean.CVF.C}} | {{v:H_Tier.mean.CVF.S}} | {{v:H_Tier.CVF.rho}} | {{v:H_Tier.elig.CVF.rho}} |
| Fashion and luxury | {{v:H_Tier.mean.FAS.L}} | {{v:H_Tier.mean.FAS.C}} | {{v:H_Tier.mean.FAS.S}} | {{v:H_Tier.FAS.rho}} | {{v:H_Tier.elig.FAS.rho}} |

: Mean recall Presence by tier and per-industry rank correlations (descriptive; `reported_alongside.mean_pi_by_industry_tier`, `per_industry_rho`). Clothing and department stores have two S units, pharmacies one.

![Mean recall Presence of the three tiers in each industry, with the per-industry rank correlation.](../../reports/figs/v44/paper/fig_02_tier.pdf){#fig:tier width=100%}

Every pre-registered variant met the same rule as the registered test. With the eligible rank in place of the three-level tier the correlation was {{v:H_Tier.elig.rho}}; without fashion and luxury, whose second source uses AI discovery signals, it was {{v:H_Tier.nofas.rho}}; without the two pharmacy units placed from a different metric it was {{v:H_Tier.nopha.rho}} (pharmacies alone: {{v:H_Tier.nopha.PHA.rho}}).

## 3.5 H_Separation: Consistency does not follow Presence among rated brands ({{v:H_Sep.verdict}})

{{v:H_Sep.n}} brands were rated, above the minimum of 40: their φ was defined in at least two of three runs and their π̂ was at least 1/6. Among them, scaled Consistency was unrelated to recall Presence: ρ_sep = {{v:H_Sep.rho}}, bootstrap 95% CI {{v:H_Sep.ci}} (seed 440043). The absolute value is far below 0.50 and the interval lies inside (−0.70, 0.70). H_Separation is **{{v:H_Sep.verdict}}** (Figure 3). With raw φ_b in place of C_φ the statistic is {{v:H_Sep.rho_raw_phi}}, its exact negative, as the scaling implies; the uncentred comparability value is {{v:H_Sep.rho_unc}}. Among rated brands, C_φ ranged from {{v:unit.cphi_min}} to {{v:unit.cphi_max}}. Two ghosts, {{v:unit.ghosts_rated}}, were rated and are included, as the pre-registration allows.

![Scaled Consistency against recall Presence for each rated brand.](../../reports/figs/v44/paper/fig_03_separation.pdf){#fig:separation width=100%}

**Reported alongside.** Per industry (descriptive; between {{v:H_Sep.rated_ind_min}} and {{v:H_Sep.rated_ind_max}} rated brands each), ρ was {{v:H_Sep.INS.rho}} for car insurance, {{v:H_Sep.HOT.rho}} for hotel chains, {{v:H_Sep.GRO.rho}} for grocery, {{v:H_Sep.QSR.rho}} for fast food, {{v:H_Sep.APR.rho}} for clothing and department stores, {{v:H_Sep.PHA.rho}} for pharmacies, {{v:H_Sep.CVF.rho}} for convenience and fuel and {{v:H_Sep.FAS.rho}} for fashion and luxury. Of the {{v:H_Sep.part_run.total}} brand-runs, φ was defined in {{v:H_Sep.part_run.defined}}, zero (no model named the brand) in {{v:H_Sep.part_run.zero}} and saturated in {{v:H_Sep.part_run.saturated}}. Across brands, {{v:H_Sep.part_unit.defined}} had a defined φ_b, {{v:H_Sep.part_unit.zero}} were zero in every run, {{v:H_Sep.part_unit.saturated}} were saturated and {{v:H_Sep.part_unit.undefined}} undefined. Unrated brands were concentrated among smaller brands: {{v:H_Sep.unrated.tier.S}} smaller brands were unrated, against {{v:H_Sep.unrated.tier.C}} challengers, {{v:H_Sep.unrated.tier.L}} leaders and {{v:H_Sep.unrated.tier.G}} ghosts (Table 6).

| Industry | Unrated | | Industry | Unrated |
|---|---|---|---|---|
| Car insurance | {{v:H_Sep.unrated.INS}} | | Clothing and department stores | {{v:H_Sep.unrated.APR}} |
| Hotel chains | {{v:H_Sep.unrated.HOT}} | | Pharmacies | {{v:H_Sep.unrated.PHA}} |
| Grocery store chains | {{v:H_Sep.unrated.GRO}} | | Convenience stores and gas stations | {{v:H_Sep.unrated.CVF}} |
| Fast-food chains | {{v:H_Sep.unrated.QSR}} | | Fashion and luxury | {{v:H_Sep.unrated.FAS}} |

: Unrated units per industry, all tiers including ghosts (`reported_alongside.unrated_share_by_industry_tier`, summed over tiers).

## 3.6 Summary of verdicts

| Test | Statistic | Threshold | Verdict |
|---|---|---|---|
| H_Spread | {{v:H_Spread.n_with_spread}} of {{v:H_Spread.n_industries}} industries with SD ≥ 0.15 (SD {{v:H_Spread.sd_min}}--{{v:H_Spread.sd_max}}) | ≥ 6 of 8 | {{v:H_Spread.verdict}} |
| H_Tier | ρ_pw = {{v:H_Tier.rho}} ({{v:H_Tier.ci}}), p {{v:H_Tier.p}}, n = {{v:H_Tier.n}} | ρ ≥ 0.40 and p < 0.05 | {{v:H_Tier.verdict}} |
| H_Separation | ρ_pw = {{v:H_Sep.rho}} ({{v:H_Sep.ci}}), n = {{v:H_Sep.n}} | \|ρ\| ≤ 0.50, CI inside ±0.70 | {{v:H_Sep.verdict}} |

: Primary verdicts as written by `score_v0_44.py --run` (`v44_verdicts.json`, `verdicts`).

## 3.7 Descriptives

The nine pre-registered descriptives carry no verdicts (`v44_verdicts.json`, `descriptives`).

**1. Presence by industry, tier and model.** Table 8 gives the mean and SD of π̂ per model over all units of each industry, and Table A2 (Appendix) the mean per model and tier. The three models' industry means are close: the largest difference between two models' means in one industry is {{v:D1.max_model_gap}} ({{v:D1.max_model_gap_ind}}).

| Industry | Fable 5.2 | GPT-6 Astra | Gemini 4 Argon |
|---|---|---|---|
| Car insurance | {{v:D1.claude-fable-5-2.INS.mean}} ({{v:D1.claude-fable-5-2.INS.sd}}) | {{v:D1.gpt-6-astra.INS.mean}} ({{v:D1.gpt-6-astra.INS.sd}}) | {{v:D1.gemini-4-argon.INS.mean}} ({{v:D1.gemini-4-argon.INS.sd}}) |
| Hotel chains | {{v:D1.claude-fable-5-2.HOT.mean}} ({{v:D1.claude-fable-5-2.HOT.sd}}) | {{v:D1.gpt-6-astra.HOT.mean}} ({{v:D1.gpt-6-astra.HOT.sd}}) | {{v:D1.gemini-4-argon.HOT.mean}} ({{v:D1.gemini-4-argon.HOT.sd}}) |
| Grocery store chains | {{v:D1.claude-fable-5-2.GRO.mean}} ({{v:D1.claude-fable-5-2.GRO.sd}}) | {{v:D1.gpt-6-astra.GRO.mean}} ({{v:D1.gpt-6-astra.GRO.sd}}) | {{v:D1.gemini-4-argon.GRO.mean}} ({{v:D1.gemini-4-argon.GRO.sd}}) |
| Fast-food chains | {{v:D1.claude-fable-5-2.QSR.mean}} ({{v:D1.claude-fable-5-2.QSR.sd}}) | {{v:D1.gpt-6-astra.QSR.mean}} ({{v:D1.gpt-6-astra.QSR.sd}}) | {{v:D1.gemini-4-argon.QSR.mean}} ({{v:D1.gemini-4-argon.QSR.sd}}) |
| Clothing and department stores | {{v:D1.claude-fable-5-2.APR.mean}} ({{v:D1.claude-fable-5-2.APR.sd}}) | {{v:D1.gpt-6-astra.APR.mean}} ({{v:D1.gpt-6-astra.APR.sd}}) | {{v:D1.gemini-4-argon.APR.mean}} ({{v:D1.gemini-4-argon.APR.sd}}) |
| Pharmacies | {{v:D1.claude-fable-5-2.PHA.mean}} ({{v:D1.claude-fable-5-2.PHA.sd}}) | {{v:D1.gpt-6-astra.PHA.mean}} ({{v:D1.gpt-6-astra.PHA.sd}}) | {{v:D1.gemini-4-argon.PHA.mean}} ({{v:D1.gemini-4-argon.PHA.sd}}) |
| Convenience stores and gas stations | {{v:D1.claude-fable-5-2.CVF.mean}} ({{v:D1.claude-fable-5-2.CVF.sd}}) | {{v:D1.gpt-6-astra.CVF.mean}} ({{v:D1.gpt-6-astra.CVF.sd}}) | {{v:D1.gemini-4-argon.CVF.mean}} ({{v:D1.gemini-4-argon.CVF.sd}}) |
| Fashion and luxury | {{v:D1.claude-fable-5-2.FAS.mean}} ({{v:D1.claude-fable-5-2.FAS.sd}}) | {{v:D1.gpt-6-astra.FAS.mean}} ({{v:D1.gpt-6-astra.FAS.sd}}) | {{v:D1.gemini-4-argon.FAS.mean}} ({{v:D1.gemini-4-argon.FAS.sd}}) |

: Mean recall Presence per model and industry (SD in brackets), over all units including ghosts (descriptive 1, `<model>|<industry>|all`).

**2. Recognition and the recognition--recall gap.** Recognition was near its ceiling: Claude Fable 5.2 recognised {{v:D2.claude-fable-5-2.all}} brands, GPT-6 Astra {{v:D2.gpt-6-astra.all}} and Gemini 4 Argon {{v:D2.gemini-4-argon.all}} (Table 9). {{v:D2.gap.total}} brands were recognised by all three models yet never named in any category answer (π̂ = 0): {{v:D2.gap.S}} smaller brands, {{v:D2.gap.C}} challengers, {{v:D2.gap.L}} leader and {{v:D2.gap.G}} ghost.

| Industry | Fable 5.2 | GPT-6 Astra | Gemini 4 Argon |
|---|---:|---:|---:|
| Car insurance | {{v:D2.claude-fable-5-2.INS}} | {{v:D2.gpt-6-astra.INS}} | {{v:D2.gemini-4-argon.INS}} |
| Hotel chains | {{v:D2.claude-fable-5-2.HOT}} | {{v:D2.gpt-6-astra.HOT}} | {{v:D2.gemini-4-argon.HOT}} |
| Grocery store chains | {{v:D2.claude-fable-5-2.GRO}} | {{v:D2.gpt-6-astra.GRO}} | {{v:D2.gemini-4-argon.GRO}} |
| Fast-food chains | {{v:D2.claude-fable-5-2.QSR}} | {{v:D2.gpt-6-astra.QSR}} | {{v:D2.gemini-4-argon.QSR}} |
| Clothing and department stores | {{v:D2.claude-fable-5-2.APR}} | {{v:D2.gpt-6-astra.APR}} | {{v:D2.gemini-4-argon.APR}} |
| Pharmacies | {{v:D2.claude-fable-5-2.PHA}} | {{v:D2.gpt-6-astra.PHA}} | {{v:D2.gemini-4-argon.PHA}} |
| Convenience stores and gas stations | {{v:D2.claude-fable-5-2.CVF}} | {{v:D2.gpt-6-astra.CVF}} | {{v:D2.gemini-4-argon.CVF}} |
| Fashion and luxury | {{v:D2.claude-fable-5-2.FAS}} | {{v:D2.gpt-6-astra.FAS}} | {{v:D2.gemini-4-argon.FAS}} |
| **All** | **{{v:D2.claude-fable-5-2.all}}** | **{{v:D2.gpt-6-astra.all}}** | **{{v:D2.gemini-4-argon.all}}** |

: Brands recognised per model and industry, of all units including ghosts (descriptive 2, `share_per_model_industry`).

**3. Ghosts.** All three models recognised each ghost as a brand of its industry (Esurance {{v:D3.Esurance.rec}}, A&P {{v:D3.AandP.rec}}, Rite Aid {{v:D3.RiteAid.rec}}). In open answers Esurance was never named (π̂ = {{v:D3.Esurance.pi}}), while A&P (π̂ = {{v:D3.AandP.pi}}) and Rite Aid (π̂ = {{v:D3.RiteAid.pi}}) were. Whether those answers present them as current was not coded.

**4. Run-to-run reliability.** The rank order of a model's counts repeated closely across runs: rel1 (mean ρ_pw over the three run pairs) was {{v:D4.claude-fable-5-2.rel1}} for Claude Fable 5.2, {{v:D4.gpt-6-astra.rel1}} for GPT-6 Astra and {{v:D4.gemini-4-argon.rel1}} for Gemini 4 Argon; the three-run reliability rel3 was {{v:D4.claude-fable-5-2.rel3}}, {{v:D4.gpt-6-astra.rel3}} and {{v:D4.gemini-4-argon.rel3}}.

**5. Model agreement.** Pairwise ρ_pw of per-model recall over all {{v:D5.claude-fable-5-2.gpt-6-astra.n}} units was {{v:D5.claude-fable-5-2.gpt-6-astra}} (Fable--Astra), {{v:D5.claude-fable-5-2.gemini-4-argon}} (Fable--Argon) and {{v:D5.gpt-6-astra.gemini-4-argon}} (Astra--Argon).

**6. Brands named outside the registries.** The heuristic extraction of bold spans and list-item heads found between {{v:D6.QSR.distinct}} and {{v:D6.PHA.distinct}} distinct candidate names per industry that match no registry alias (Table A3). The most frequent are brands that the tier rule or its sources left out: for example Trader Joe's and Costco in grocery, Drury Hotels and hotel sub-brands such as The Ritz-Carlton in hotels, Raising Cane's and Shake Shack in fast food, Bloomingdale's and Uniqlo in clothing, Amazon Pharmacy in pharmacies, Buc-ee's in convenience and fuel, and Tom Ford in fashion. The list also holds non-brand strings ("Pros", "Cons", "Bottom line") and advertising characters, as expected of a heuristic.

**7. Companies in two industries.** π̂ in the grocery and the pharmacy frame was {{v:D7.Kroger.GRO}} and {{v:D7.Kroger.PHA}} for Kroger, {{v:D7.Publix.GRO}} and {{v:D7.Publix.PHA}} for Publix, and {{v:D7.Albertsons.GRO}} and {{v:D7.Albertsons.PHA}} for Albertsons.

**8. Answer form.** Category answers averaged {{v:D8.claude-fable-5-2.wB}} words (Claude Fable 5.2), {{v:D8.gpt-6-astra.wB}} (GPT-6 Astra) and {{v:D8.gemini-4-argon.wB}} (Gemini 4 Argon) and named {{v:D8.claude-fable-5-2.units}}, {{v:D8.gpt-6-astra.units}} and {{v:D8.gemini-4-argon.units}} registry units on average. Recognition answers averaged {{v:D8.claude-fable-5-2.wA}}, {{v:D8.gpt-6-astra.wA}} and {{v:D8.gemini-4-argon.wA}} words. Every answered call ended normally (Claude {{v:D8.claude-fable-5-2.finish}}; GPT {{v:D8.gpt-6-astra.finish}}; Gemini {{v:D8.gemini-4-argon.finish}}). Recorded refusals were {{v:D8.claude-fable-5-2.refusals}}, {{v:D8.gpt-6-astra.refusals}} and {{v:D8.gemini-4-argon.refusals}}, unanswered calls {{v:D8.claude-fable-5-2.unanswered}}, {{v:D8.gpt-6-astra.unanswered}} and {{v:D8.gemini-4-argon.unanswered}}, and ambiguous recognition answers {{v:D8.claude-fable-5-2.phase_A_ambiguous}}, {{v:D8.gpt-6-astra.phase_A_ambiguous}} and {{v:D8.gemini-4-argon.phase_A_ambiguous}}. The raw file records {{v:raw.empty}} empty answers and {{v:raw.empty_retry}} calls re-sent after an empty answer, so none of the calls could hide one of the two kinds of refusal that DEVIATIONS Entry 2 says leave no refusal finish reason.

**9. Cost.** Spend from recorded usage was {{v:D9.total}} (Table 10), {{v:D9.B.usd}} for the category questions and {{v:D9.A.usd}} for the recognition questions, below the pre-registered central estimate. No usage part was estimated at its worst case ({{v:D9.est_parts}} parts).

| Model (phase) | Billed requests | Input tokens | Output tokens | Of which thinking | Cost |
|---|---:|---:|---:|---:|---:|
| Claude Fable 5.2 (B) | {{v:D9.claude-fable-5-2.B.billed}} | {{v:D9.claude-fable-5-2.B.in}} | {{v:D9.claude-fable-5-2.B.out}} | {{v:D9.claude-fable-5-2.B.think}} | {{v:D9.claude-fable-5-2.B.usd}} |
| Claude Fable 5.2 (A) | {{v:D9.claude-fable-5-2.A.billed}} | {{v:D9.claude-fable-5-2.A.in}} | {{v:D9.claude-fable-5-2.A.out}} | {{v:D9.claude-fable-5-2.A.think}} | {{v:D9.claude-fable-5-2.A.usd}} |
| GPT-6 Astra (B) | {{v:D9.gpt-6-astra.B.billed}} | {{v:D9.gpt-6-astra.B.in}} | {{v:D9.gpt-6-astra.B.out}} | {{v:D9.gpt-6-astra.B.think}} | {{v:D9.gpt-6-astra.B.usd}} |
| GPT-6 Astra (A) | {{v:D9.gpt-6-astra.A.billed}} | {{v:D9.gpt-6-astra.A.in}} | {{v:D9.gpt-6-astra.A.out}} | {{v:D9.gpt-6-astra.A.think}} | {{v:D9.gpt-6-astra.A.usd}} |
| Gemini 4 Argon (B) | {{v:D9.gemini-4-argon.B.billed}} | {{v:D9.gemini-4-argon.B.in}} | {{v:D9.gemini-4-argon.B.out}} | {{v:D9.gemini-4-argon.B.think}} | {{v:D9.gemini-4-argon.B.usd}} |
| Gemini 4 Argon (A) | {{v:D9.gemini-4-argon.A.billed}} | {{v:D9.gemini-4-argon.A.in}} | {{v:D9.gemini-4-argon.A.out}} | {{v:D9.gemini-4-argon.A.think}} | {{v:D9.gemini-4-argon.A.usd}} |
| **All** | | | | | **{{v:D9.total}}** |

: Tokens and cost per model and phase from recorded usage at the listed prices (descriptive 9). Gemini 4 Argon's Phase A has {{v:D9.gemini-4-argon.A.lines}} raw lines for {{v:D9.gemini-4-argon.A.billed}} billed requests (the three timed-out attempts).

# 4. Discussion

On the newest models and in eight industries the programme had not measured, both components behaved as they did on the premium consumer-goods base. Presence separated brands within every industry, as it did in four of the five omnibus categories on the legacy panel; on the same three models, all five omnibus categories also cleared the spread threshold (a comparison computed after scoring, §3.3). It followed the industries' public market order with a moderate pooled correlation, and Consistency was separable from Presence. For services and retail, AI naming is therefore neither uniform nor random: the models name some chains, insurers and stores far more than others, and largely the ones that lead their industry on sales, premiums, locations or store counts.

The tier correlation leaves much of the ordering unexplained, and the per-industry values differ: highest in hotels and car insurance, lowest in pharmacies and fashion and luxury. Several reasons are visible in the registries rather than in the models. Tiers come from heterogeneous metrics that order size or salience, not one common quantity; hotel groups known to guests by their sub-brands (IHG, Choice, Wyndham) and multi-banner retailers are measured as one master brand; and the extraction of non-registry names shows that the answers often name brands the tier rule excluded, such as Trader Joe's, Costco, Raising Cane's or Buc-ee's, and hotel sub-brands. A registry built from a ranking measures the ranking's brands, not the set the models consider; the gap between the two is itself an AI-availability fact for the excluded brands, which this wave does not score.

Recognition was nearly saturated, as on the omnibus, so almost all the information is in recall. {{v:D2.gap.total}} brands, most of them smaller brands and challengers, were recognised by every model and never named in an open answer. That recognition--recall gap is the distance between being known and being suggested that the Presence measure was designed to capture.

The separation result rests on {{v:H_Sep.n}} rated brands, and rating removes most smaller brands, because φ is undefined or zero when the models rarely name a brand. H_Separation therefore says that among brands the models name at least occasionally, how consistently they name a brand does not follow how often; it says nothing about Consistency among rarely named brands. Among rated brands C_φ ranged from {{v:unit.cphi_min}} to {{v:unit.cphi_max}}, with most values in the upper part of that range (Figure 3), so the test compares brands within a narrow band of high agreement.

# 5. Limitations

1. Tiers come from heterogeneous public metrics, some from reproductions of the original tables (NAIC via Agency Checklists, QSR 50 via FoodIndustry.com, DCI figures via Becker's); within an industry they order size or salience, not one common quantity.
2. Fashion and luxury rests on global sources and on the Lyst Index, which uses AI discovery signals; H_Tier holds without it (§3.4).
3. Some company totals cover several banners while the unit is one banner, and house-of-brands hotel groups are named by group names that guests may know by their sub-brands, which lowers their measured Presence.
4. Three models and three runs: φ is noisier than on six models, and the rated set excludes most smaller brands (§3.5).
5. No web search: the results describe the models' own knowledge, not what a search-enabled assistant retrieves.
6. One market and language (US English), one collection on one night, no retest.
7. The alias matcher is new. It matched an independent ground truth on synthetic answers before the lock, but it is not validated on these answers: the MC_Alias table of {{v:alias.matches}} case-sensitive matches is exported, not reviewed, and no human or model check of the coding was registered.
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

{{table:alias}}

{{table:d1tier}}

{{table:d6}}
