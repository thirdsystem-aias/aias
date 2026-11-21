---
title: "Leaders, Challengers and Ghosts: AI Answers about US Airlines and Retail Banks against Market Share and Brand Exits"
subtitle: "A Pre-Registered Two-Arm Study (AIAS™ v0.40)"
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

{\LARGE \textbf{Leaders, Challengers and Ghosts:\\ AI Answers about US Airlines and Retail Banks\\ against Market Share and Brand Exits}}\\[8pt]

{\large A Pre-Registered Two-Arm Study (AIAS™ v0.40)}\\[28pt]

Pablo Ulpiano González Castro\\[4pt]
School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System™ (research entity; data archive and methodology venue)\\[8pt]
Correspondence: pablou@pablou.com · pablou.com\\
ORCID: \href{https://orcid.org/0009-0003-8968-9990}{0009-0003-8968-9990}\\[20pt]

Pre-registration: \texttt{v0.40-prereg-r1} (commit \texttt{a53d2b7})\\
locked and deposited on OSF before the first study call\\[4pt]
Data and code: OSF \texttt{ec6wh}, \texttt{v40}\\[4pt]
November 2026

\end{center}
\end{titlepage}

# Abstract {-}

Do AI assistants name brands in proportion to their real market share, and do brands that have left the market keep a place in their answers? This pre-registered study asked nine large language models (a legacy panel of six and the newest flagship of each of three providers, with and without the provider's own web search) brand-free recommendation questions and brand-named recognition and status questions about US airlines and US retail banks, including the brands retired by merger, failure or rename since 2008 ("ghosts"). All 2,821 planned calls were answered; recorded spend was $49.26 of a $100.00 cap. Coding was rule-based; an AI-only audit of a declared sample, with no human check, met the registered agreement threshold on the gone-flag (Cohen's κ 0.883).
AI share tracked market share in both categories (Spearman ρ 0.612 for airlines and 0.679 for banks; H_Reinforce CONFIRMED), but the airline result did not survive the pre-registered sensitivity that places Sun Country inside Allegiant (ρ 0.483, p 0.099). The category leaders were not amplified: American received 0.599 times and the JPMorgan Chase holder 0.887 times its market share of naming, both significantly below parity (H_Amplify FALSIFIED). Ghosts were rarely named as if current in recommendation answers (5.5% of airline and 6.3% of bank ghost-model pairs; H_Afterlife UNDETERMINED). Ghost Presence fell with the time between exit and a model's training cutoff (ρ -0.286, p < 0.001; H_Decay PARTIAL, short of the registered -0.3 band). Asked directly, the models said a ghost was gone in 98.0% of answers against 16.9% for living brands (H_Flag CONFIRMED). Web search flagged every post-cutoff exit (5 of 5) but produced too few discordant cells for the paired test (H_Search PARTIAL); one current model searched in only 41 of 63 search-on answers, failing a manipulation check. Every test is reported, including failures.

**Keywords:** AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; large language models; Double Jeopardy; market share; brand exits; mergers; web search; airlines; retail banking

**JEL codes:** M31; L86, L15, D83, M37

**Paper status:** Pre-registered confirmatory study (tag `v0.40-prereg-r1`, locked and deposited on OSF before the first study call); scored once (`score_v0_40.py`); deviations recorded in `osf/v40/DEVIATIONS.md`. Part of the AIAS measurement programme.

# 1. Introduction

AI Availability, the discoverability and representation of a brand in the answers of large language models (LLMs), has been proposed as a third measurable layer of brand availability (González Castro, 2026, SSRN 6659000), beside the Mental and Physical Availability of the Ehrenberg-Bass tradition (Sharp, 2010; Romaniuk & Sharp, 2016). The Tri-System framework (González Castro, 2026, MSI Working Paper, Report No. 26-132) treats AI as a mediation layer between brand and buyer and takes the name "System 3", for artificial cognition beside human fast and slow thinking, from Shaw and Nave (2026, SSRN 6097646). Its first proposition, P1 (default reinforcement), holds that AI answers usually reinforce brands that are already large. Whether they reinforce, amplify or flatten market share had not been measured against an official share base.

This study does that for two US categories with official share data and many dated exits: airlines (revenue passenger miles, Bureau of Transportation Statistics T-100) and retail banks (deposits, FDIC Summary of Deposits). It also asks a question that earlier phases could only bracket: what happens to brands that have left the market. A merger, a failure or a rename removes a brand from the market on a known date, while a model's training data stop at a known month. The gap between the two gives a natural test of whether such "ghost" brands keep a place in AI answers, whether that place fades with time, whether the answers say the brand is gone, and whether web search corrects them.

Six hypotheses were fixed before data (§2.3): H_Reinforce (AI share tracks market share), H_Amplify (AI amplifies the category leader, as Double Jeopardy would suggest; Ehrenberg, Goodhardt & Barwise, 1990), H_Afterlife (ghosts are still named as if current), H_Decay (ghost Presence decays with the exit-to-cutoff gap), H_Flag (status answers say a ghost is gone, and do not say so of living brands) and H_Search (web search corrects the status of ghosts). The study is the programme's first public flagship study under its independence rule: there is no focal brand, no finding is addressed to a brand, and no brand was contacted.

# 2. Method

## 2.1 Registry

The brand registry was built mechanically from official data under rules fixed in advance and frozen on 12 November 2026 (pre-registration §3; `osf/v40/registries/out/`). Current units are the airline share units (10, with Hawaiian counted inside Alaska) and the bank holding companies above the registry's deposit floor (25). Market share is the allocated brand share of revenue passenger miles for airlines and the share of deposits for banks. The ghosts are the airline and bank brands retired by merger, failure or rename from 2008 to the freeze (for example Continental, US Airways, Virgin America, Washington Mutual, Wachovia, SunTrust, BB&T, Silicon Valley Bank and First Republic). Hawaiian and Sun Country (airlines) and Discover (banks) are the living-brand controls, and American, Delta, Chase and Bank of America the incumbent controls. Discover's deposit accounts were being moved to Capital One during the study; the pre-registrant kept it as the bank control and declared a sensitivity without it (§2.5). Each model's training cutoff is the vendor's published month; the gap of a ghost-model pair is the number of months from the brand's retirement to that cutoff, and a pair with a positive gap is a pre-cutoff exit.

## 2.2 Probes, panel and collection

The probe set (pre-registration §4.1) has, per category, brand-free recommendation questions (generic, by need and by US Census region), and, for each ghost and control, one recognition question and one status question (whether one can still book with, or open an account at, the brand). Questions were asked in one user turn with no system prompt and no buyer persona.

The legacy arm is the programme's six-model panel fixed since v0.17 (Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o mini, Gemini 2.5 Flash with thinking budget 0, Gemini 2.5 Flash-Lite; temperature 0), plus one extra Gemini 2.5 Flash pass at the provider's default thinking that is reported and never tested. The current arm is each provider's newest generally available flagship on the vendors' pages at the lock: Claude Fable 5.2 (C1), GPT-6 Astra (C2) and Gemini 4 Argon (C3), at provider defaults, with search off (three runs) and with each provider's own web search on (one run on the recommendation and status probes; pre-registration §4.2--§4.4, §6.3--§6.4).

Collection ran from 17 to 19 November 2026 under a cost guard. All 2,821 planned calls returned an answer (2,821 with status ok; legacy search off 1,786, current search off 846, current search on 189); none failed and none was re-run. The collection's recorded spend was $36.74; with the two declared pre-lock checks ($6.40) the guard's spend was $43.14, and with the audit (§2.6, $6.12) the paper's total is $49.26 against a cap of $100.00 and a pause at $80.00. A length-limit stop rule checked every answer as it arrived; no answer stopped at its token limit before naming a brand (0 treated as missing).

## 2.3 Measures and tests

A **mention** is a whole-word, case-sensitive match of a registry alias; the longest alias wins. Bare names that collide with ordinary words or other brands (for example "American", "United", "Delta", "Discover") are coded ambiguous and excluded from every primary test, and every result is also reported with them (S-Ambig). The **AI share** of a current unit is, per model, the number of its search-off recommendation answers naming the unit divided by the same count summed over all current units of the category, averaged over the nine tested models (legacy six and current three, search off). A mention is **gone-flagged** when a locked lexicon ("no longer", "defunct", "merged into", "acquired by", "now part of", "rebranded", "failed" and similar) occurs within 150 characters of it. The coder recorded 27,647 mentions in 2,821 answers. No LLM was used as coder or judge.

Table: Pre-registered tests (pre-registration §2.2--§2.7). One-sided, α = 0.05, no multiplicity correction; permutation tests use 10,000 permutations with seed 4040.

| Test | Statistic | Rule |
|:----------------|:----------------------------------------|:------------------------------------------|
| H_Reinforce | Spearman ρ, market share against AI share, per category; permutation test (ρ > 0) | A category passes with ρ ≥ 0.5, p < 0.05 and at least 5 units named; CONFIRMED if both pass, PARTIAL if one |
| H_Amplify | Leader's ratio (k/n)/p₀ over the nine models; exact binomial test both ways | Amplified: ratio ≥ 1.25 and p(X ≥ k) < 0.05; flattened: ratio < 1 and p(X ≤ k) < 0.05; CONFIRMED if amplified in both, FALSIFIED if flattened in both |
| H_Afterlife | Share of pre-cutoff ghost × model pairs named in a recommendation answer without a gone-flag; exact binomial test against 0.05 | A category passes with rate ≥ 0.2 and p < 0.05; low below 0.05; CONFIRMED if both pass, FALSIFIED if both low |
| H_Decay | Spearman ρ, gap in months against ghost Presence, over pre-cutoff pairs; permutation within model (ρ < 0) | CONFIRMED: ρ ≤ -0.3 and p < 0.05; PARTIAL: ρ < 0, p < 0.05, ρ > -0.3; evaluable with at least 10 pairs named |
| H_Flag | Flag rate of ghost status answers against control status answers; one-sided Fisher exact test | CONFIRMED: ghost rate ≥ 0.8 and p < 0.05; FALSIFIED: rate < 0.5 and p ≥ 0.05 |
| H_Search | Exact McNemar test, current models, ghost status cells, search off (majority of three runs) against on; post-cutoff search-on flag rate | McNemar part: at least 10 discordant cells and p < 0.05; post-cutoff part: rate ≥ 0.8; CONFIRMED if both, PARTIAL if one |

## 2.4 Manipulation checks

Four checks were fixed before any verdict was read (pre-registration §2.8): completeness of each arm, search use by each current model with search on, recognition of the four incumbents, and truncation at the output cap. Their limits are those of pre-registration §2.8; the results are in Table 2.

## 2.5 Sensitivity analyses

Pre-registered sensitivities are reported beside each verdict and change none (pre-registration §5.6, §5.9): S-Ambig (ambiguous mentions included), S-Legal (legal-date gaps in place of brand-retirement gaps), S-Operating (airline operating share, with Delta as the leader), S-SunCountry (Sun Country inside Allegiant), S-D4 (banks without the three brokerage and wealth holders), S-Discover (H_Flag without the bank living-brand control), S-Arm (each test on the legacy and on the current arm alone) and S-Length (without the 43 answers that stopped at the length limit after naming a brand or used half the limit or more on thinking).

## 2.6 Audit of the coder

The declared audit sample (pre-registration §5.5) was drawn by script with seed 4040 after coding and before any verdict: recommendation answers with a ghost or control mention and status answers, stratified by arm, condition and role, 200 answers in all. DEVIATIONS Entry 1 (21 November 2026, written before the draw) replaced the human analyst named in the pre-registration with an AI-only analyst and added a coding-only step so that the sample could be drawn before scoring. Two blind coders from two providers, claude-fable-5-2 and gpt-6.2-astra, coded each answer from the written rules; gemini-4-carbon broke ties (12 of 200 answers). **The audit has no human check**: no person coded or reviewed the sampled answers or the AI codes. The AI codes never replaced a rule-based code. The audit cost $6.12 against its $25.00 cap.

## 2.7 Pre-registration, lock and deviations

The pre-registration was locked at tag `v0.40-prereg-r1` (commit a53d2b7) on 16 November 2026 and deposited on OSF (`ec6wh`, `v40/prereg` and `v40/registries`), every file verified by SHA-256, before the first study call. One discrepancy in the locked file is reported here rather than corrected: its first line still reads "revision r1, DRAFT for the pre-registrant's review --- not locked", and its status line describes the draft. The file was not edited at or after the lock; what makes it locked is the tag, the lock manifest (`prereg/LOCK_MANIFEST_v0_40.sha256`) and the OSF deposit, all recorded in the lock entry of `DEVIATIONS.md`. Besides that lock record and the collection records, the study has two dated entries: Entry 0 (ex ante, the conflict-of-interest screen of the registry; Declarations) and Entry 1 (the coding-only step, the scripted audit draw and the AI-only analyst, §2.6). The scorer ran once, unchanged, after the audit; the mentions file it rewrote matched the coding step's SHA-256.

# 3. Results

## 3.1 Manipulation checks

Table: Manipulation checks (pre-registration §2.8).

| Check | Result | Pass |
|:------------------------------|:------------------------------------|:-----|
| MC1 completeness, legacy | 1,786 of 1,786 ok | yes |
| MC1 completeness, current | 1,035 of 1,035 ok | yes |
| MC2 search used, Claude Fable 5.2 | 63 of 63 answers | yes |
| MC2 search used, GPT-6 Astra | 63 of 63 answers | yes |
| MC2 search used, Gemini 4 Argon | 41 of 63 answers | **no** |
| MC3 incumbents recognised | 108 of 108 answers | yes |
| MC4 truncation, legacy (limit 5.0%) | 29 of 1,786 | yes |
| MC4 truncation, current (limit 2.0%) | 0 of 1,035 | yes |

Every check passed except MC2 for Gemini 4 Argon, which searched in 41 of its 63 search-on answers. As registered, not searching is part of the condition and those answers are kept; H_Search is reported with this caveat (§3.8). The legacy truncations are the extra Gemini 2.5 Flash pass (27 of 94, expected at its setting) and Gemini 2.5 Flash at thinking budget 0 (2 of 282), each after a brand had been named.

## 3.2 Coder reliability

The AI consensus agreed with the rule-based gone-flag on 895 of 932 coded entities (96.0%; κ 0.883 against the registered 0.8; threshold met: yes). The disagreements were asymmetric: the rule flagged 6 entities the consensus did not, and missed 31 that the consensus flagged. On the status answers κ was 0.914; on the recommendation answers alone it was 0.487 (of 737 entities, the rule missed 28 flags and added 5). The registered threshold applies to the whole sample and was met, but the recommendation-answer subset, on which H_Afterlife rests, falls well short of it: in the sample, the rule left 83.3% of 30 recommendation ghost mentions unflagged, the AI consensus 63.3%. The rule-based afterlife rates below are therefore more likely too high than too low. Subject and ambiguity codes agreed almost perfectly (κ 0.999 and 1.000); the successor-name code had κ 0.933, and the two AI coders agreed with each other on the gone-flag at κ 0.985.

## 3.3 H_Reinforce: AI share rises with market share in both categories (CONFIRMED)

Across the nine models, AI share rose with market share in airlines (ρ = 0.612, p = 0.033, 10 of 10 units named) and in banks (ρ = 0.679, p < 0.001, 21 of 25 units named); both categories passed and the verdict is CONFIRMED (Figure 1). The bank result held in every specification, including without the brokerage and wealth holders (S-D4, ρ = 0.733). The airline result is fragile. It held with ambiguous mentions included (ρ = 0.915) and on operating share (ρ = 0.636), but it failed the registered rule when Sun Country was placed inside Allegiant (S-SunCountry: ρ = 0.483, p = 0.099) and on the current arm alone (ρ = 0.285, p = 0.216; current-arm verdict PARTIAL). With ten airline units, the placement of one unit moves the rank correlation across the line; the airline half of the verdict rests on that choice and on the legacy models.

![Spearman correlation of market share with AI share for each category, panel and pre-registered specification. Filled markers meet the registered rule. Values: `H_Reinforce.*`, `sensitivity.*.H_Reinforce*`.](../../reports/figs/v40/paper/fig_01_reinforce.pdf){#fig:reinforce width=100%}

## 3.4 H_Amplify: the leaders receive less than their market share (FALSIFIED)

The registered leaders were not amplified; they were flattened (Figure 2). American Airlines was named in 216 of the 1,668 airline unit-namings against a market share of 0.216 of the current units, a ratio of 0.599 (p(X ≤ k) < 0.001). The JPMorgan Chase holder was named in 395 of 2,458, ratio 0.887 (p(X ≤ k) = 0.004). Both categories were flattened under the registered rule, so H_Amplify is FALSIFIED. The airline result holds with Delta as leader on operating share (ratio 0.755) and with ambiguous mentions (ratio 0.672). On the current arm alone the bank ratio was 0.945 and not significant either way (p(X ≤ k) = 0.255), so the current-arm verdict is UNDETERMINED. The descriptive log-log slopes of AI share on market share, which carry no verdict, were 0.629 for airlines and 0.985 for banks.

![The leader's share of AI naming divided by its market share, per category, panel and specification; dashed lines at parity and at the registered amplification threshold. Values: `H_Amplify.*`, `sensitivity.*.H_Amplify*`.](../../reports/figs/v40/paper/fig_02_amplify.pdf){#fig:amplify width=100%}

## 3.5 H_Afterlife: ghosts are seldom named as current (UNDETERMINED)

Of the pre-cutoff ghost × model pairs, 3 of 55 airline pairs (5.5%, p = 0.523) and 9 of 142 bank pairs (6.3%, p = 0.281) had at least one search-off recommendation answer naming the ghost without a gone-flag (Figure 3). Neither category reached the registered pass rate, and neither fell below the registered low rate, so H_Afterlife is UNDETERMINED: the rates sit just above the null. With ambiguous names included the airline rate rose to 12.7% (p = 0.019), still below the pass rate. Because the audit found the rule more likely to miss a gone-flag than to add one in recommendation answers (§3.2), these rates are upper bounds rather than central estimates.

![Afterlife rate per category by panel and specification, against the registered null and pass lines. Values: `H_Afterlife.*`, `sensitivity.*.H_Afterlife*`.](../../reports/figs/v40/paper/fig_03_afterlife.pdf){#fig:afterlife width=100%}

## 3.6 H_Decay: ghost Presence falls with the exit-to-cutoff gap, below the registered strength (PARTIAL)

Over the 197 pre-cutoff pairs, of which 16 had a ghost Presence above zero (floor 10), the correlation between gap and ghost Presence was ρ = -0.286 (p < 0.001): negative and significant, but short of the registered -0.3, so H_Decay is PARTIAL (Figure 4). The legacy arm alone met the CONFIRMED band (ρ = -0.327, p < 0.001, 11 pairs named); the current arm had only 5 pairs named, below the floor, and is UNDETERMINED. The direction held under S-Ambig (ρ = -0.231) and S-Legal (ρ = -0.225). Most pairs have zero Presence, so the correlation rests on few named pairs and many ties.

![Correlation of the exit-to-cutoff gap with ghost Presence by panel and specification, with the number of pairs named. Values: `H_Decay.*`, `sensitivity.*.H_Decay*`.](../../reports/figs/v40/paper/fig_04_decay.pdf){#fig:decay width=100%}

## 3.7 H_Flag: status answers say a ghost is gone (CONFIRMED)

Asked whether one can still book with or open an account at a ghost, the nine models said it was gone in 579 of 591 answers (98.0%), against 32 of 189 answers about living brands (16.9%; Fisher p < 0.001); H_Flag is CONFIRMED (Figure 5). Without Discover the control rate was 13.6%. The control rate differs by arm: 7.9% for the legacy models and 34.9% (22 of 63) for the current models, which flagged every ghost answer (100.0%). Part of the control flagging is expected and may be correct: two living-brand controls were in recent mergers or account moves (Hawaiian with Alaska; Discover with Capital One), and the gone-flag lexicon fires on a merger mentioned near the brand. In the audit sample, the AI consensus flagged 30.4% of the 23 sampled control answers, against 26.1% for the rule.

![Gone-flag rate of status answers about ghosts and about living brands, by panel and without the bank living-brand control. Values: `H_Flag.*`, `sensitivity.*.H_Flag*`, `sensitivity.S-Discover.*`.](../../reports/figs/v40/paper/fig_05_flag.pdf){#fig:flag width=100%}

## 3.8 H_Search: web search flags post-cutoff exits; the paired test is not evaluable (PARTIAL)

Of the 72 paired ghost × current-model status cells, 1 was flagged with search on only and 4 with search off only (exact McNemar p = 0.969); with fewer than 10 discordant cells the McNemar part fails its registered floor. Without search the current models already flagged nearly every ghost, so there was little left for search to correct. The post-cutoff part passed: with search on, the current models flagged all 5 cells in which the exit came after the model's cutoff (100.0%). One part passing gives PARTIAL (Figure 6). The verdict carries the MC2 caveat: Gemini 4 Argon searched in only 41 of 63 search-on answers. When a ghost status answer was flagged with search on, the most frequently cited domains were Google's grounding redirect (201 citations), en.wikipedia.org (139), reddit.com (134) and sec.gov (94).

![Discordant ghost status cells of the current models with search off and on, and the search-on flag rate on post-cutoff cells. Values: `H_Search.*`.](../../reports/figs/v40/paper/fig_06_search.pdf){#fig:search width=100%}

## 3.9 Summary of verdicts and sensitivities

Table: Verdicts and sensitivity verdicts. "--" marks a sensitivity that does not apply to the test.

| Test | Verdict | S-Ambig | S-Length | Legacy arm | Current arm |
|:--------------|:--------------|:--------------|:--------------|:--------------|:--------------|
| H_Reinforce | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | PARTIAL |
| H_Amplify | FALSIFIED | FALSIFIED | FALSIFIED | FALSIFIED | UNDETERMINED |
| H_Afterlife | UNDETERMINED | UNDETERMINED | UNDETERMINED | UNDETERMINED | UNDETERMINED |
| H_Decay | PARTIAL | PARTIAL | PARTIAL | CONFIRMED | UNDETERMINED |
| H_Flag | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED |
| H_Search | PARTIAL | PARTIAL | PARTIAL | -- | PARTIAL |

The single-category sensitivities carry no verdict of their own: S-Operating passed the airline rule (ρ = 0.636) and flattened Delta (ratio 0.755); S-SunCountry failed the airline rule (ρ = 0.483) and flattened American (ratio 0.604); S-D4 passed the bank rule (ρ = 0.733); S-Discover kept H_Flag CONFIRMED; S-Legal left H_Afterlife UNDETERMINED and H_Decay PARTIAL.

## 3.10 Descriptives

*Old versus new name.* Of the ghost mentions, the successor's name appeared within the same window in 56.0% for the legacy models (1,942 of 3,468), 52.9% for the current models without search and 67.1% with search (165 of 246).

*Run-to-run precision.* The standard error of per-model Presence across the three search-off runs averaged 0.008 in the legacy arm (0.010 for units named in some answers but not all) and 0.017 in the current arm (0.022), below the method v1.17 planning estimate the pre-registration cites (§2.10).

*Near-floor banks.* Among the brands below the bank deposit floor, USAA was named in 19 of 288 legacy recommendation answers, 5 of 144 current answers without search and 2 of 48 with search.

*Extra Gemini 2.5 Flash pass.* At the provider's default thinking, 27 of 94 answers ended at the output cap and 41 spent half the cap or more on thinking; none was cut before naming a brand.

*Not in the scored record.* The pre-registration also lists, as descriptives 1 and 2, the AI share of each current unit and the ghost Presence of each ghost, per model and arm. The scorer's verdict file carries the tests built from them but not these per-unit and per-ghost tables, so they are not reported in this paper; the coded mentions from which they follow are in the study data (`v40_mentions.csv`). The recognition codes (descriptive 4), first-mention shares (descriptive 9) and search traces (descriptive 7) are in the verdict file and the values file in full.

# 4. Discussion

Two findings are clear. First, the models' naming of current brands followed market share in both categories but did not concentrate on the leader: the largest airline and the largest bank holder received a smaller share of AI naming than of the market. In these two categories the models reproduced the existing order of brands while spreading their naming beyond the leader. This supports the MSI framework's P1 (default reinforcement) in its ordinal form and runs against a Double Jeopardy-style amplification on this measure. The measure counts answers that name a unit, not rank or prominence within an answer, so a leader named first in most answers can still be "flattened" here; the first-mention shares in the values file show the JPMorgan Chase holder named first in most bank answers of the legacy Claude and GPT-4o models (64.6%, 60.4% and 68.8%).

Second, when asked directly, the models knew that the ghosts were gone. Status answers flagged ghosts at a rate close to the ceiling, and web search flagged the exits that came after a model's cutoff. Whether ghosts still surface unprompted in recommendations was not settled: the afterlife rates sat between the registered null and pass lines, and the audit suggests the rule-based coder overstates them. Ghost Presence did fall with the exit-to-cutoff gap, as expected if a brand's footprint in training text fades after it leaves the market, but the association was weaker than the registered band and rested on few named pairs; the design shows an association, not its cause.

The airline reinforcement result should be read with its sensitivity. With ten units, moving Sun Country into Allegiant changes the airline correlation from passing to failing, and the current models alone did not pass. The banks, with twenty-five units, held in every specification.

# 5. Limitations

1. *One market, one language, two categories, three days.* US airlines and US retail banks, asked in English, without a buyer persona, collected 17--19 November 2026; answers drift between model versions and days.
2. *Search on is thin.* One search-on run on the recommendation and status probes; each provider decided whether and what to search, and Gemini 4 Argon did not search in about a third of its answers (MC2).
3. *Rule-based coding.* The gone-flag lexicon misses paraphrases and fires on living brands whose answers mention a merger they survived. The audit met its registered threshold overall but not on the recommendation answers alone (κ 0.487).
4. *The audit has no human check.* The analyst named in the pre-registration was replaced by two blind AI coders and an AI tie-breaker (DEVIATIONS Entry 1); one of them, Claude Fable 5.2, is also a model of the study's current arm.
5. *Cutoffs are vendor-published months.* Claude Fable 5.2 takes Claude Opus 5.5's cutoff rows; differences within a month are not resolved.
6. *Pairs are not independent.* Ghost × model pairs share ghosts, and answers share probes and runs; the exact tests treat them as independent.
7. *The bank living-brand control was itself changing.* Discover's deposits were moving to Capital One; H_Flag is also reported without it.
8. *Share measures.* AI share counts answers that name a unit, not rank or prominence; brokerage-sweep holders enter by the deposit rule; near-floor brands such as USAA are not units.
9. *Two pre-registered descriptives are missing from the scored record* (§3.10).
10. *The locked file's first line still reads DRAFT* (§2.7); the lock rests on the tag, the manifest and the OSF deposit.

# 6. Future Research

A second wave on the same registry and questions would test whether the flattening of leaders and the decay of ghost Presence repeat, with more search-on runs and a persona arm. The afterlife question needs a coder whose gone-flag is reliable on recommendation answers, fixed before data, and enough named ghost pairs in the current arm to evaluate decay there.

# Declarations {-}

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. Samsung does not compete in US airlines or US retail banking; banking has an adjacency through Samsung Wallet, which is disclosed here. The programme's record from the v0.62 pre-registration reads: "Cheil Worldwide, a marketing company of the Samsung group in which Samsung Electronics holds 28.43%, or its agency Iris has done advertising, public-relations or search-marketing work for five registry brands: Chevrolet (for GM Korea, 2017), BMW (UK consumer public relations, 2018), Bentley (experiential agency of record in the Americas from 2021), Jack Daniel's (UK digital agency from 2022, since replaced) and Eucerin (search marketing for Beiersdorf from 2024)." None of those five brands is in the v0.40 registry: every brand of the frozen registry, with its aliases, was screened against them on 12 November 2026 and none matched (DEVIATIONS Entry 0, ex ante), so no v0.40 brand has a recorded Cheil Worldwide or Iris tie. For the programme record, the correction of 10 November 2026 to the v0.19 disclosure is carried here: Harman International (a Samsung subsidiary since March 2017; deal agreed November 2016) completed its acquisition of Masimo's Sound United brands, Denon included, on 23 September 2025. Denon, chosen for v0.19 in place of AKG, was therefore already a Samsung-group brand. No v0.40 brand is affected. No brand was contacted. Acquisition, coding and scoring are fully automated against the frozen registry, and the pre-registration was locked and deposited before the first call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

## Funding {-}

Self-funded. No external funding supported this research.

## Ethics {-}

Not applicable; no human subjects. Public model APIs, including the providers' own web search tools, and public official data (BTS, FDIC, SEC filings).

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## Data and code availability {-}

Materials are deposited at OSF (osf.io/ec6wh), `v40/`: the locked pre-registration, probe set, cost estimate, pre-lock and technical checks and lock manifest (`prereg/`) and the frozen registry with its sources (`registries/`). The answers, coded mentions, verdict file, audit records and values file are in the repository at `osf/v40/` and go to OSF with the study's data deposit. The pre-registered code is in the programme's GitHub repository (github.com/thirdsystem-aias/aias) at tag `v0.40-prereg-r1`; the scripts that fill this paper and draw its figures are on the branch `v0.40-paper`. Every number in this paper is read from `osf/v40/v40_values.json`, which names the source file and path of each value.

# References {-}

Ehrenberg, A. S. C., Goodhardt, G. J., & Barwise, T. P. (1990). Double jeopardy revisited. *Journal of Marketing*, 54(3), 82--91.

González Castro, P. U. (2026). *AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval*. SSRN 6659000.

González Castro, P. U. (2026). *Tri-System Brand Growth: The AI Mediation Layer*. MSI Working Paper, Report No. 26-132. Marketing Science Institute.

González Castro, P. U. (2026). *The AIAS™ Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy* (v1.2). SSRN 6761698.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification (v1.3)*. SSRN 6797679.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol v1.4: Recognition × Recall Decomposition and Multi-Component AI Availability*. SSRN 6799479.

González Castro, P. U. (2026). *The AIAS™ Presence Measurement Protocol: Multi-Statistic C2 Specification and Two-Channel Recall Decomposition* (v1.5). SSRN 6810758.

González Castro, P. U. (2026). *Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension* (AIAS Methodology v1.6). SSRN 6816340.

González Castro, P. U. (2026). *CPC Consistency: A Pre-Registered Negative Result* (AIAS Methodology v1.7). SSRN 6878818.

González Castro, P. U. (2026). *CPC Consistency Instrument Redesign* (AIAS Methodology v1.8). SSRN 6963359.

González Castro, P. U. (2026). *AI Availability as a Third Measurable Layer of Brand Availability: Five-Substrate Empirical Anchoring of the AIAS™ Presence Measurement Protocol* (AIAS 1.0). SSRN 6817841.

González Castro, P. U. (2026). AIAS phase papers v0.16--v0.24, v0.26, v0.29, v0.32--v0.34 and v0.37 (SSRN 6791999, 6802261, 6806558, 6809182, 6811441, 6815378, 6829118, 6834298, 6838802, 6847678, 6870778, 6898581, 6909019, 6915458 and 7685199); v0.25, v0.27, v0.28, v0.30, v0.31, v0.35 and v0.36 on OSF (osf.io/ec6wh) and thirdsystem.ai.

González Castro, P. U. (2026). *Method v1.17: run-to-run precision of per-model Presence*. OSF `ec6wh`, `methodology/v1_17` (tag `v1.17-prereg-r1`).

Romaniuk, J., & Sharp, B. (2016). *How Brands Grow: Part 2*. Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

Shaw, S., & Nave, G. (2026). *Thinking---Fast, Slow, and Artificial: How AI is Reshaping Human Reasoning and the Rise of Cognitive Surrender*. SSRN 6097646.
