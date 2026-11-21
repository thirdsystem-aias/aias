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

{\LARGE \textbf{Leaders, Challengers and Ghosts:\\ AI Answers about US Airlines and Retail Banks\\ against Market Share and Brand Exits}\par}\vspace{8pt}

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

Do AI assistants name brands in proportion to their market share, and do brands that have left the market keep a place in their answers? This pre-registered study asked nine large language models (a legacy panel of six and the newest generally available flagship of three providers, as checked on 12 November 2026, with and without web search) about US airlines and US retail banks, including the brands retired by merger, failure or rename since 2008 ("ghosts"). All 2,821 planned calls were answered, for $49.26 of a $100.00 cap. A rule-based coder met the registered agreement threshold with an AI-only audit (κ 0.883), but not on recommendation answers alone (κ 0.487).
The models' naming followed market share in both categories (Spearman ρ 0.612 for airlines and 0.679 for banks; CONFIRMED), though the airline result failed a pre-registered sensitivity (ρ 0.483). H_Amplify is FALSIFIED as registered (leader ratios 0.599 and 0.887 against a threshold of 1.25), but the test could not have confirmed: because answers name many brands, the largest ratio the registered measure could reach at the observed breadth of answers was 1.198 for airlines and 0.970 for banks, so the result does not show whether AI answers amplify the leader or understate it. Ghosts were named without a gone-flag in 5.5% and 6.3% of ghost-model pairs, between the registered null and pass lines (UNDETERMINED). Ghost Presence was lower at longer gaps between exit and training cutoff (ρ -0.286, 16 of 197 pairs named; PARTIAL). Status answers about ghosts carried a gone-flag in 98.0% of cases against 16.9% for living-brand and incumbent controls (CONFIRMED). With web search on, all 5 post-cutoff cells were flagged, most of them already without search, but the paired test had too few discordant cells (PARTIAL), and one model searched in 41 of 63 search-on answers. Every test is reported, including failures; pre-registered tables the scorer did not output were computed after scoring from the frozen coded data and are labelled as such.

**Keywords:** AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; large language models; Double Jeopardy; market share; brand exits; mergers; web search; airlines; retail banking

**JEL codes:** M31; L86, L15, D83, M37

**Paper status:** Pre-registered confirmatory study (tag `v0.40-prereg-r1`, locked and deposited on OSF before the first study call); scored once (`score_v0_40.py`); deviations recorded in `osf/v40/DEVIATIONS.md`. Part of the AIAS measurement programme.

# 1. Introduction

AI Availability, the discoverability and representation of a brand in the answers of large language models (LLMs), has been proposed as a third measurable layer of brand availability (González Castro, 2026, SSRN 6659000), beside the Mental and Physical Availability of the Ehrenberg-Bass tradition (Sharp, 2010; Romaniuk & Sharp, 2016), and measured under a versioned protocol (Methodology v1.2--v1.8; AIAS 1.0) in a series of category phases (González Castro, 2026, phase papers v0.16--v0.37). The Tri-System framework (González Castro, 2026, MSI Working Paper, Report No. 26-132) treats AI as a mediation layer between brand and buyer and takes the name "System 3", for artificial cognition beside human fast and slow thinking, from Shaw and Nave (2026, SSRN 6097646). The framework's first proposition, P1, asks whether AI answers track or amplify the market position of brands. That had not been measured against an official share base.

Outside this programme, work on LLMs in marketing has asked whether model outputs reproduce consumer perceptions of brands (Li, Castelo, Katona & Sarvary, 2024), how content can be shaped to appear in generative answers (Aggarwal et al., 2024), and how buyer personas change which brands are recommended (Jack, Lehman, Maloney & Xu, 2026; Rienecker et al., 2026). Work on language models as knowledge bases has shown that facts change after training and that models answer from the time of their data (Dhingra et al., 2022). Brand management has studied what happens to brands deleted or absorbed after a merger (Varadarajan, DeFanti & Busch, 2006). This study joins the three: it measures AI naming against official market shares, and it uses dated brand exits against each model's published training cutoff as a natural test of what models say about brands that no longer exist. Its contribution is a pre-registered, two-arm measurement in two categories with official share data (airlines: revenue passenger miles, Bureau of Transportation Statistics T-100; retail banks: deposits, FDIC Summary of Deposits) and many dated exits, which we call ghosts.

Six hypotheses were fixed before data (§2.3): H_Reinforce (AI share tracks market share), H_Amplify (AI amplifies the category leader, as Double Jeopardy would suggest; Ehrenberg, Goodhardt & Barwise, 1990), H_Afterlife (ghosts are still named as if current), H_Decay (ghost Presence decays with the exit-to-cutoff gap), H_Flag (status answers say a ghost is gone, and do not say so of living brands) and H_Search (web search corrects the status of ghosts). The study is the programme's first public flagship study under its independence rule: there is no focal brand, no finding is addressed to a brand, and no brand was contacted.

# 2. Method

## 2.1 Registry

The brand registry was built mechanically from official data under rules fixed in advance and frozen on 12 November 2026 (pre-registration §3). Current units are the airline share units (10, with Hawaiian counted inside Alaska) and the bank holding companies above the registry's deposit floor (25). Market share is the allocated brand share of revenue passenger miles for airlines and the share of deposits for banks. The ghosts are the airline and bank brands retired by merger, failure or rename from 2008 to the freeze (for example Continental, US Airways, Virgin America, Washington Mutual, Wachovia, SunTrust, BB&T, Silicon Valley Bank and First Republic). In each category the largest current unit is the leader (American Airlines; the JPMorgan Chase holder) and the other current units are the challengers. Hawaiian and Sun Country (airlines) and Discover (banks) are the living-brand controls, and American, Delta, Chase and Bank of America the incumbent controls. Discover's deposit accounts were being moved to Capital One during the study; the pre-registrant kept it as the bank control and declared a sensitivity without it (§2.5). Each model's training cutoff is the vendor's published month; the gap of a ghost-model pair is the number of months from the brand's retirement to that cutoff, and a pair with a positive gap is a pre-cutoff exit.

## 2.2 Probes, panel and collection

The probe set (pre-registration §4.1) has, per category, brand-free recommendation questions (generic, by need and by US Census region), and, for each ghost and control, one recognition question and one status question (whether one can still book with, or open an account at, the brand). Questions were asked in one user turn with no system prompt and no buyer persona.

The legacy arm is the programme's six-model panel fixed since v0.17 (Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o mini, Gemini 2.5 Flash with thinking budget 0, Gemini 2.5 Flash-Lite; temperature 0), plus one extra Gemini 2.5 Flash pass at the provider's default thinking that is reported and never tested. The current arm is each provider's newest generally available flagship as checked on the vendors' pages on 12 November 2026 (pre-registration §4.3): Claude Fable 5.2 (C1), GPT-6 Astra (C2) and Gemini 4 Argon (C3), at provider defaults, with search off (three runs) and with each provider's own web search on (one run on the recommendation and status probes; pre-registration §4.2--§4.4, §6.3--§6.4). The record is not consistent on one point: the pre-registration's check found no Gemini API statement that Gemini 4 Carbon was generally available, while DEVIATIONS Entry 1, written on 21 November for the audit, quotes a Gemini API changelog entry dated 10 November that declares it generally available, and notes that GPT-6.2 Astra is newer than GPT-6 Astra. OpenAI's pricing page as read for the pre-registration on 12 November listed no GPT-6.2 model (pre-registration §4.3); when GPT-6.2 Astra became generally available, and so whether the §4.3 rule applied to OpenAI before the lock, was not checked. Under the pre-registration's own rule, a generally available Carbon before the lock would have replaced Argon; the study ran with Argon as locked. DEVIATIONS Entry 2 records the pre-registrant's ruling of 21 November: the point is accepted as disclosed; had the 10 November entry been visible at the pre-lock check, Carbon would have been used in place of Argon; data and verdicts are unchanged.

Collection ran from 17 to 19 November 2026 under a cost guard. All 2,821 planned calls returned an answer (2,821 with status ok; legacy search off 1,786, current search off 846, current search on 189); none failed and none was re-run. The collection's recorded spend was $36.74; with the declared pre-lock check and technical check ($6.40) the guard's spend was $43.14, and with the audit (§2.6, $6.12) the paper's total is $49.26 against a cap of $100.00 and a pause at $80.00. A length-limit stop rule checked every answer as it arrived; no answer stopped at its token limit before naming a brand (0 treated as missing).

## 2.3 Measures and tests

A **mention** is a whole-word, case-sensitive match of a registry alias; the longest alias wins. Bare names that collide with ordinary words or other brands (for example "American", "United", "Delta", "Discover") are coded ambiguous and excluded from every primary test, and every result is also reported with them (S-Ambig). The **AI share** of a current unit is, per model, the number of its search-off recommendation answers naming the unit divided by the same count summed over all current units of the category, averaged over the nine tested models (legacy six and current three, search off). A mention is **gone-flagged** when a locked lexicon ("no longer", "defunct", "merged into", "acquired by", "now part of", "rebranded", "failed" and similar) occurs within 150 characters of it. The coder recorded 27,647 mentions in 2,821 answers. No LLM was used as coder or judge. **Ghost Presence** of a ghost for a model is the share of the model's search-off recommendation answers in the ghost's category that name it (any run; ambiguous mentions excluded). One departure of the locked scorer from the pre-registration is reported here and was not corrected: pre-registration §2.1 (registry decision D12) counts Discover's mentions toward the Capital One holder, but the scorer assigns a control brand to a current unit only when their aliases overlap, and Discover's do not overlap Capital One's, so non-ambiguous Discover mentions count toward no unit in H_Reinforce, H_Amplify or descriptive 1. Nothing was re-scored; every result follows the locked scorer (DEVIATIONS Entry 2). For H_Amplify, k counts the answers that name the leader, while n adds up, over all current units, the answers that name each unit, so an answer naming four units counts four times in n (pre-registration §2.3).

Table: Pre-registered tests (pre-registration §2.2--§2.7). One-sided, α = 0.05, no multiplicity correction; permutation tests use 10,000 permutations with seed 4040.

| Test | Statistic | Rule |
|:----------------|:----------------------------------------|:------------------------------------------|
| H_Reinforce | Spearman ρ, market share against AI share, per category; permutation test (ρ > 0) | A category passes with ρ ≥ 0.5, p < 0.05 and at least 5 units named; CONFIRMED if both pass, PARTIAL if one |
| H_Amplify | Leader's ratio (k/n)/p₀ over the nine models; exact binomial test both ways | Amplified: ratio ≥ 1.25 and p(X ≥ k) < 0.05; below parity: ratio < 1 and p(X ≤ k) < 0.05; CONFIRMED if amplified in both, FALSIFIED if below parity in both |
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

The pre-registration was locked at tag `v0.40-prereg-r1` (commit a53d2b7) on 16 November 2026 and deposited on OSF (`ec6wh`, folders v40/prereg and v40/registries), every file verified by SHA-256, before the first study call. One discrepancy in the locked file is reported here rather than corrected: its first line still reads "revision r1, DRAFT for the pre-registrant's review --- not locked", and its status line describes the draft. The file was edited only at the lock, to correct §9's test count (DEVIATIONS lock record), and not after; what makes it locked is the tag, the lock manifest (`prereg/LOCK_MANIFEST_v0_40.sha256`) and the OSF deposit, all recorded in the lock entry of `DEVIATIONS.md`. Besides that lock record and the collection records, the study has three dated entries: Entry 0 (ex ante, the conflict-of-interest screen of the registry; Declarations), Entry 1 (the coding-only step, the scripted audit draw and the AI-only analyst, §2.6) and Entry 2 (after scoring: the ceiling of the H_Amplify ratio, §3.4; the Gemini 4 Carbon timing, §2.2; and the pre-registered reporting the scorer did not output, computed afterwards, §3.10 and Appendix A; it also records, without acting on it, the Discover mapping of §2.3). Entry 3 corrects two points of Entry 2 the same day, before publication. The scorer ran once, unchanged, after the audit; the mentions file it rewrote matched the coding step's SHA-256.

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

![Spearman correlation of market share with AI share for each category, panel and pre-registered specification. Filled markers meet the registered rule.](../../reports/figs/v40/paper/fig_01_reinforce.pdf){#fig:reinforce width=100%}

## 3.4 H_Amplify: falsified as registered, on a ratio that could not reach its threshold (FALSIFIED)

American Airlines accounted for 216 of the 1,668 airline unit-namings against a market share of 0.216 of the current units, a ratio of 0.599 (p(X ≤ k) < 0.001), and the JPMorgan Chase holder for 395 of 2,458, a ratio of 0.887 (p(X ≤ k) = 0.004; Figure 2). Neither reached the amplification threshold and both met the registered rule for a ratio below parity, so H_Amplify is FALSIFIED, and the verdict stands as registered.

A post-scoring check (DEVIATIONS Entry 2), not in the pre-registration, shows that the test could not have confirmed. k counts the answers that name the leader and cannot exceed the number of answers (432 search-off recommendation answers per category), while n counts every current unit named in every answer; the answers named on average 3.861 airline and 5.690 bank units. At that breadth, a leader named in every answer would have had a ratio of 1.198 in airlines and 0.970 in banks: below the registered 1.25 in both categories, and below parity in banks. The locked measure therefore cannot show whether AI answers amplify the leader, and a ratio below parity on it is no evidence that they understate the leader. For scale, the JPMorgan Chase holder was named in 395 of the 432 bank answers (91.4%) and American in 216 of 432 (50.0%); counting the bare name "American", which the ambiguity rule excludes, American was named in 349 (80.8%; S-Ambig ratio 0.672). The ceiling depends on the specification (Figure 2): on the current arm alone in airlines it was 1.497, and with Delta as leader on operating share 1.299, above the threshold, against observed ratios of 0.457 and 0.755; these sensitivities carry no verdict. On the current arm alone the bank ratio was 0.945 and not significant either way (current-arm verdict UNDETERMINED). The binomial test also treats each naming as an independent draw. The descriptive log-log slopes of AI share on market share, which carry no verdict, were 0.629 for airlines and 0.985 for banks, and 1.001 for banks without the brokerage and wealth holders (computed after scoring; §3.10).

![The leader's share of AI naming divided by its market share, per category, panel and specification, with the largest value the measure could reach at the observed breadth of answers (grey tick; post-scoring check, DEVIATIONS Entry 2); dashed lines at parity and at the registered amplification threshold.](../../reports/figs/v40/paper/fig_02_amplify.pdf){#fig:amplify width=100%}

## 3.5 H_Afterlife: ghosts named without a gone-flag fall between the null and the pass line (UNDETERMINED)

Of the pre-cutoff ghost × model pairs, 3 of 55 airline pairs (5.5%, p = 0.523) and 9 of 142 bank pairs (6.3%, p = 0.281) had at least one search-off recommendation answer naming the ghost without a gone-flag (Figure 3). Neither category reached the registered pass rate, and neither fell below the registered low rate, so H_Afterlife is UNDETERMINED. With ambiguous names included the airline rate rose to 12.7% (p = 0.019), still below the pass rate. Because the audit found the rule more likely to miss a gone-flag than to add one in recommendation answers (§3.2), these rates are more likely too high than too low.

![Afterlife rate per category by panel and specification, against the registered null and pass lines.](../../reports/figs/v40/paper/fig_03_afterlife.pdf){#fig:afterlife width=100%}

## 3.6 H_Decay: ghost Presence is lower at longer exit-to-cutoff gaps, below the registered strength (PARTIAL)

Over the 197 pre-cutoff pairs, of which 16 had a ghost Presence above zero (floor 10), the correlation between gap and ghost Presence was ρ = -0.286 (p < 0.001): negative and significant, but short of the registered -0.3, so H_Decay is PARTIAL (Figure 4). The legacy arm alone met the CONFIRMED band (ρ = -0.327, p < 0.001, 11 pairs named); the current arm had only 5 pairs named, below the floor, and is UNDETERMINED. The direction held under S-Ambig (ρ = -0.231) and S-Legal (ρ = -0.225). Most pairs have zero Presence, so the correlation rests on few named pairs and many ties.

![Correlation of the exit-to-cutoff gap with ghost Presence by panel and specification, with the number of pairs named.](../../reports/figs/v40/paper/fig_04_decay.pdf){#fig:decay width=100%}

## 3.7 H_Flag: status answers about ghosts carry a gone-flag (CONFIRMED)

Asked whether one can still book with or open an account at a ghost, the nine models' answers carried a gone-flag in 579 of 591 answers (98.0%), against 32 of 189 answers about living brands (16.9%; Fisher p < 0.001); H_Flag is CONFIRMED (Figure 5). Without Discover the control rate was 13.6%. The control rate differs by arm: 7.9% for the legacy models and 34.9% (22 of 63) for the current models, which flagged every ghost answer (100.0%). Part of the control flagging is expected and may be correct: the three living-brand controls (Hawaiian, Sun Country, Discover) are brands whose answers may mention a merger or account move they survived (pre-registration §8, item 4; Discover's deposits were moving to Capital One), and the gone-flag lexicon fires on a merger mentioned near the brand. In the audit sample, the AI consensus flagged 30.4% of the 23 sampled control answers, against 26.1% for the rule.

![Gone-flag rate of status answers about ghosts and about living brands, by panel and without the bank living-brand control.](../../reports/figs/v40/paper/fig_05_flag.pdf){#fig:flag width=100%}

## 3.8 H_Search: post-cutoff exits flagged with search on; the paired part failed (PARTIAL)

Of the 72 paired ghost × current-model status cells, 1 was flagged with search on only and 4 with search off only (exact McNemar p = 0.969); with fewer than 10 discordant cells the McNemar part fails its registered floor. The discordant cells went against the hypothesis (more flagged with search off only than with search on only). Without search the current models already flagged nearly every ghost, so there was little left for search to correct. The post-cutoff part passed: with search on, the current models flagged all 5 cells in which the exit came after the model's cutoff (100.0%). These cells come from two brands (Silicon Valley Bank for all three models, Spirit for two) and are among the paired cells; since only 1 paired cell was flagged with search on alone, most of them were already flagged without search. The count is small and shows little that search added. One part passing gives PARTIAL (Figure 6). The verdict carries the MC2 caveat: Gemini 4 Argon searched in only 41 of 63 search-on answers. When a ghost status answer was flagged with search on, the most frequently cited domains were Google's grounding redirect (201 citations), en.wikipedia.org (139), reddit.com (134) and sec.gov (94).

![Discordant ghost status cells of the current models with search off and on, and the search-on flag rate on post-cutoff cells.](../../reports/figs/v40/paper/fig_06_search.pdf){#fig:search width=100%}

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

The single-category sensitivities carry no verdict of their own: S-Operating passed the airline rule (ρ = 0.636) and gave Delta a leader ratio of 0.755; S-SunCountry failed the airline rule (ρ = 0.483) and gave American a ratio of 0.604; S-D4 passed the bank rule (ρ = 0.733); S-Discover kept H_Flag CONFIRMED; S-Legal left H_Afterlife UNDETERMINED and H_Decay PARTIAL.

## 3.10 Descriptives

*Old versus new name.* Of the ghost mentions, the successor's name appeared within the same window in 56.0% for the legacy models (1,942 of 3,468), 52.9% for the current models without search and 67.1% with search (165 of 246).

*Run-to-run precision.* The standard error of per-model Presence across the three search-off runs averaged 0.008 in the legacy arm (0.010 for units named in some answers but not all) and 0.017 in the current arm (0.022), below the method v1.17 planning estimates beside which pre-registration §2.9 item 6 reports them (0.040 for all units and 0.050 for units named in some answers but not all).

*Near-floor banks.* Of the brands below the bank deposit floor, legacy recommendation answers (288) named USAA 19 times, Synchrony 11, Santander 9, Zions 9, Western Alliance 1 and RBC 0; current answers without search (144) named them 5, 4, 3, 4, 0 and 0 times, and with search (48) 2, 1, 0, 1, 1 and 0 times.

*Extra Gemini 2.5 Flash pass.* At the provider's default thinking, 27 of 94 answers ended at the output cap and 41 spent half the cap or more on thinking; none was cut before naming a brand. Its 94 answers carried 237 ghost mentions, against 663 in the 282 answers of Gemini 2.5 Flash at thinking budget 0.

*First mention.* Among bank recommendation answers naming a current unit, the JPMorgan Chase holder was named first in 64.6% (Claude Opus 4.5), 60.4% (Claude Sonnet 4.5), 68.8% (GPT-4o), 56.3% (GPT-4o mini), 75.0% (Gemini 2.5 Flash), 75.0% (Gemini 2.5 Flash-Lite), 54.2% (Claude Fable 5.2), 40.4% (GPT-6 Astra) and 27.1% (Gemini 4 Argon) of answers, search off; with search on the current models' shares were 25.0%, 6.3% and 31.3%.

*Computed after scoring.* The locked scorer did not output four pre-registered reporting items: descriptive 1 (the AI share of each current unit per model and arm, with the log-log slope without the brokerage holders, §2.3; the slope with them is in the verdict file), descriptive 2 (the ghost Presence of each ghost per model and arm), the per-ghost and per-model results beside each test (pre-registration §8, item 6) and the Discover status answers in full (§3.2). They were computed afterwards by a separate script that checks the SHA-256 of the frozen coded mentions, imports the locked scorer unchanged and, before writing anything, reproduces the coded mentions byte for byte and the six primary tests and S-D4 exactly (DEVIATIONS Entry 2). They are pre-registered, computed after scoring because the locked scorer did not output them, and they change no verdict. Appendix A gives the per-model results (Tables 4 and 5), the per-ghost results (Table 6), the AI and market shares of each current unit (Tables 7 and 8) and ghost Presence by model (Table 9). The afterlife pairs came from BB&T (5 pairs), SunTrust (4), Virgin America (2) and Northwest (1); no other ghost was named without a gone-flag in a pre-cutoff pair (Table 6). Of the 27 search-off status answers about Discover, 10 carried a gone-flag and 14 named Capital One (9 did both); with search on, 2 of 3 were flagged and 3 named Capital One. These answers, which may be correct when they say Discover's deposits now sit with Capital One, are given in full in `osf/v40/v40_discover_status_answers.md`. The recognition codes (descriptive 4) and the search traces (descriptive 7) are in the verdict file in full.

# 4. Discussion

The models' naming of current brands followed market share in both categories, which is in line with the Tri-System framework's P1 (MSI Working Paper 26-132) in its ordinal form; in airlines this rests on the legacy models and on how one small unit is placed (below). Whether AI amplifies the leader could not be decided by this measure: the registered ratio divides answers by unit-namings, and at the breadth the models' answers showed it could not reach the amplification threshold (§3.4). The falsified verdict is therefore no evidence that AI answers understate the leader either. A test of leader amplification needs a measure built per answer, such as the share of answers naming the leader against its market share, or rank within the answer.

Second, status answers about ghosts carried a gone-flag in nearly every case, and with web search on the current models flagged the few exits that came after their cutoff, a small count from two brands, most of them already flagged without search. Whether ghosts still surface in recommendations without such a flag was not settled: the rates sat between the registered null and pass lines, and the audit suggests the rule-based coder overstates them. Ghost Presence was lower at longer exit-to-cutoff gaps, as expected if a brand's footprint in training text fades after it leaves the market, but the association was weaker than the registered band and rested on few named pairs; the design shows an association, not its cause.

The airline reinforcement result should be read with its sensitivity. With ten units, moving Sun Country into Allegiant changes the airline correlation from passing to failing, and the current models alone did not pass. The banks, with twenty-five units, held in every specification.

# 5. Limitations

1. *One market, one language, two categories, three days.* US airlines and US retail banks, asked in English, without a buyer persona, collected 17--19 November 2026; answers drift between model versions and days.
2. *Search on is thin.* One search-on run on the recommendation and status probes; each provider decided whether and what to search, and Gemini 4 Argon did not search in about a third of its answers (MC2).
3. *Rule-based coding.* The gone-flag lexicon misses paraphrases and fires on living brands whose answers mention a merger they survived. The audit met its registered threshold overall but not on the recommendation answers alone (κ 0.487).
4. *The audit has no human check.* The analyst named in the pre-registration was replaced by two blind AI coders and an AI tie-breaker (DEVIATIONS Entry 1); one of them, Claude Fable 5.2, is also a model of the study's current arm.
5. *Cutoffs are vendor-published months.* Claude Fable 5.2 takes Claude Opus 5.5's cutoff rows; differences within a month are not resolved.
6. *Pairs are not independent.* Ghost × model pairs share ghosts, and answers share probes and runs; the exact tests treat them as independent, as does the binomial test of H_Amplify, which treats each naming as a draw. The per-ghost and per-model results promised beside each test were computed after scoring (Appendix A; DEVIATIONS Entry 2).
7. *The bank living-brand control was itself changing.* Discover's deposits were moving to Capital One; H_Flag is also reported without it.
8. *Share measures.* AI share counts answers that name a unit, not rank or prominence; the leader ratio has a ceiling set by the breadth of answers (§3.4); the ambiguity rule removes the bare names of the largest airlines; brokerage-sweep holders enter by the deposit rule; near-floor brands such as USAA are not units.
9. *Pre-registered reporting computed after scoring.* The locked scorer did not output descriptives 1 and 2, the per-ghost and per-model results, the log-log slope without the brokerage holders or the Discover status answers in full; they were computed afterwards from the frozen coded data with the locked scorer's own code and are labelled as such (§3.10, Appendix A; DEVIATIONS Entry 2).
10. *The locked file's first line still reads DRAFT* (§2.7); the lock rests on the tag, the manifest and the OSF deposit.
11. *The current arm's Google model.* The pre-lock check of 12 November found no Gemini API statement that Gemini 4 Carbon was generally available; a changelog entry dated 10 November, quoted in DEVIATIONS Entry 1, says it was. Had that entry been visible at the pre-lock check, the pre-registration's rule would have put Carbon in place of Gemini 4 Argon. The pre-registrant accepted the point as disclosed; data and verdicts are unchanged (§2.2; DEVIATIONS Entry 2). Whether GPT-6.2 Astra was generally available before the lock was not checked.
12. *Discover is not counted toward Capital One.* The locked scorer does not apply pre-registration §2.1 (D12) to Discover (§2.3); the bank results and Table 8 follow the scorer as locked, and nothing was re-scored.

# 6. Future Research

A second wave on the same registry and questions would test whether the order of brands and the decay of ghost Presence repeat, with more search-on runs and a persona arm, and would test leader amplification on a measure built per answer (§3.4). The afterlife question needs a coder whose gone-flag is reliable on recommendation answers, fixed before data, and enough named ghost pairs in the current arm to evaluate decay there.

# Declarations {-}

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. Samsung does not compete in US airlines or US retail banking; banking has an adjacency through Samsung Wallet, which is disclosed here. The programme's record (v0.62 DEVIATIONS Entry 0, Part F, as quoted in this study's pre-registration) reads: "Cheil Worldwide, a marketing company of the Samsung group in which Samsung Electronics holds 28.43%, or its agency Iris has done advertising, public-relations or search-marketing work for five registry brands: Chevrolet (for GM Korea, 2017), BMW (UK consumer public relations, 2018), Bentley (experiential agency of record in the Americas from 2021), Jack Daniel's (UK digital agency from 2022, since replaced) and Eucerin (search marketing for Beiersdorf from 2024)." Those five are brands of the programme's earlier omnibus registries; none of them is in the v0.40 registry: every brand of the frozen registry, with its aliases, was screened against them on 12 November 2026 and none matched (DEVIATIONS Entry 0, ex ante), so no v0.40 brand has a recorded Cheil Worldwide or Iris tie. For the programme record, the correction of 10 November 2026 to the v0.19 disclosure is carried here: Harman International (a Samsung subsidiary since March 2017; deal agreed November 2016) completed its acquisition of Masimo's Sound United brands, Denon included, on 23 September 2025. Denon, chosen for v0.19 in place of AKG, was therefore already a Samsung-group brand. No v0.40 brand is affected. No brand was contacted. Acquisition, coding and scoring are fully automated against the frozen registry, and the pre-registration was locked and deposited before the first call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

## Funding {-}

Self-funded. No external funding supported this research.

## Ethics {-}

Not applicable; no human subjects. Public model APIs, including the providers' own web search tools, and public official data (BTS, FDIC, SEC filings).

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## Data and code availability {-}

Materials are deposited at OSF (osf.io/ec6wh), `v40/`: the locked pre-registration, probe set, cost estimate, pre-lock and technical checks and lock manifest (`prereg/`) and the frozen registry with its sources (`registries/`). The answers, coded mentions, verdict file, audit records, post-scoring file and values file are in the repository at `osf/v40/` and are planned for OSF with the study's data deposit. The pre-registered code is in the programme's GitHub repository (github.com/thirdsystem-aias/aias) at tag `v0.40-prereg-r1`; the scripts that fill this paper and draw its figures are on the branch `v0.40-paper-r2`. The post-scoring computations of DEVIATIONS Entry 2 are in `osf/v40/v40_postscore.json`, written by `osf/v40/scripts/postscore_v0_40.py`. Every number in this paper is read from `osf/v40/v40_values.json`, which names the source file and path of each value.

# References {-}

Aggarwal, P., Murahari, V., Rajpurohit, T., Kalyan, A., Narasimhan, K., & Deshpande, A. (2024). GEO: Generative engine optimization. *Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining*. arXiv 2311.09735.

Dhingra, B., Cole, J. R., Eisenschlos, J. M., Gillick, D., Eisenstein, J., & Cohen, W. W. (2022). Time-aware language models as temporal knowledge bases. *Transactions of the Association for Computational Linguistics*, 10, 257--273.

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

Jack, Lehman, Maloney & Xu (2026). *Persona conditioning of brand recommendations in retrieval-augmented commercial chat: A prominence-stratified cross-provider audit*. arXiv 2605.30207.

Li, P., Castelo, N., Katona, Z., & Sarvary, M. (2024). Frontiers: Determining the validity of large language models for automated perceptual analysis. *Marketing Science*, 43(2), 254--266.

Rienecker et al. (2026). Auditing preferences for brands and cultures in LLMs (ChoiceEval). arXiv 2603.18300.

Romaniuk, J., & Sharp, B. (2016). *How Brands Grow: Part 2*. Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

Shaw, S., & Nave, G. (2026). *Thinking---Fast, Slow, and Artificial: How AI is Reshaping Human Reasoning and the Rise of Cognitive Surrender*. SSRN 6097646.

Varadarajan, R., DeFanti, M. P., & Busch, P. S. (2006). Brand portfolio, corporate image, and reputation: Managing brand deletions. *Journal of the Academy of Marketing Science*, 34(2), 195--205.

<!-- APPENDIX A START (appendix_tables_v0_40.py) -->

# Appendix A. Pre-registered tables computed after scoring {-}

These tables are pre-registered, computed after scoring because the locked scorer did not output them (§3.10; DEVIATIONS Entry 2). They were computed from the frozen coded mentions by `osf/v40/scripts/postscore_v0_40.py`, which imports the locked scorer unchanged and first reproduces the six primary tests and S-D4 exactly; they carry no verdict and change none. The one exception to the label is the ceiling columns of Table 4, which belong to the post-scoring check of DEVIATIONS Entry 2 and are not pre-registered. Every value is read from `osf/v40/v40_values.json` (keys `prereg_post.*`; the ceilings `ceiling.*`).

Table: Per-model results beside H_Reinforce and H_Amplify (search off; computed after scoring, DEVIATIONS Entry 2). ρ: Spearman correlation of market share with the model's AI share; ratio: the leader's (k/n)/p₀ for the model, with k of n. The ceiling columns are not pre-registered: they belong to the post-scoring check of DEVIATIONS Entry 2 (the largest ratio at the model's observed breadth of answers). Per-model statistics carry no test and rest on 48 answers per model and category.

| Model | ρ airlines | ρ banks | Ratio airlines | Ceiling airlines | Ratio banks | Ceiling banks |
|:---|---:|---:|---:|---:|---:|---:|
| Claude Opus 4.5 (M1) | 0.284 | 0.577 | 0.167 (3 of 83) | 2.676 | 1.018 (45 of 244) | 1.086 |
| Claude Sonnet 4.5 (M2) | 0.596 | 0.615 | 0.430 (12 of 129) | 1.722 | 0.913 (45 of 272) | 0.974 |
| GPT-4o (M3) | 0.888 | 0.681 | 0.734 (36 of 227) | 0.978 | 0.758 (40 of 291) | 0.910 |
| GPT-4o mini (M4) | 0.863 | 0.625 | 0.727 (41 of 261) | 0.851 | 0.805 (42 of 288) | 0.920 |
| Gemini 2.5 Flash (M5) | 0.912 | 0.639 | 0.649 (38 of 271) | 0.820 | 0.850 (45 of 292) | 0.907 |
| Gemini 2.5 Flash-Lite (M6) | 0.979 | 0.604 | 0.771 (42 of 252) | 0.881 | 0.849 (48 of 312) | 0.849 |
| Claude Fable 5.2 (C1) | -0.231 | 0.626 | 0.000 (0 of 93) | 2.388 | 0.868 (45 of 286) | 0.926 |
| GPT-6 Astra (C2) | 0.265 | 0.487 | 0.220 (3 of 63) | 3.525 | 1.254 (40 of 176) | 1.505 |
| Gemini 4 Argon (C3) | 0.879 | 0.652 | 0.656 (41 of 289) | 0.768 | 0.836 (45 of 297) | 0.892 |

Table: Per-model results beside H_Afterlife, H_Decay, H_Flag and H_Search (computed after scoring, DEVIATIONS Entry 2). Afterlife: pre-cutoff ghost pairs named without a gone-flag; Decay: pairs with ghost Presence above zero, and the within-model Spearman ρ of gap against ghost Presence (n/a: no pair named); Flag: flagged status answers about pre-cutoff ghosts and about living brands; Search: paired ghost status cells flagged with search on only / with search off only (current models).

| Model | Afterlife airlines | Afterlife banks | Decay pairs named | Decay ρ | Flag ghosts | Flag living brands | Search on / off only |
|:---|---:|---:|---:|---:|---:|---:|---:|
| Claude Opus 4.5 (M1) | 0 of 6 | 0 of 16 | 0 of 22 | n/a | 66 of 66 | 4 of 21 | -- |
| Claude Sonnet 4.5 (M2) | 0 of 6 | 2 of 16 | 3 of 22 | -0.460 | 66 of 66 | 6 of 21 | -- |
| GPT-4o (M3) | 0 of 6 | 1 of 15 | 2 of 21 | -0.348 | 60 of 63 | 0 of 21 | -- |
| GPT-4o mini (M4) | 0 of 6 | 0 of 15 | 1 of 21 | -0.240 | 57 of 63 | 0 of 21 | -- |
| Gemini 2.5 Flash (M5) | 1 of 6 | 2 of 16 | 3 of 22 | -0.328 | 66 of 66 | 0 of 21 | -- |
| Gemini 2.5 Flash-Lite (M6) | 0 of 6 | 2 of 16 | 2 of 22 | -0.299 | 63 of 66 | 0 of 21 | -- |
| Claude Fable 5.2 (C1) | 0 of 7 | 0 of 16 | 0 of 23 | n/a | 69 of 69 | 11 of 21 | 0 / 2 |
| GPT-6 Astra (C2) | 0 of 6 | 0 of 16 | 0 of 22 | n/a | 66 of 66 | 5 of 21 | 1 / 2 |
| Gemini 4 Argon (C3) | 2 of 6 | 2 of 16 | 5 of 22 | -0.383 | 66 of 66 | 6 of 21 | 0 / 0 |

Table: Per-ghost results (descriptive 2 and the per-ghost results beside each test; computed after scoring, DEVIATIONS Entry 2). Pairs: ghost × tested model, search off; pre- and post-cutoff exits shown apart. Afterlife: pre-cutoff pairs named without a gone-flag; named: pre-cutoff pairs with ghost Presence above zero; Presence: mean over pre-cutoff pairs; Flag: flagged search-off status answers (pre-cutoff pairs; -- where there are none); Search: cells flagged with search on only / off only; post-cutoff: of the post-cutoff current-model cells, those flagged with search on.

| Ghost | Pre-cutoff pairs | Post-cutoff pairs | Afterlife | Named | Presence | Flag | Search on / off only | Post-cutoff flagged |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| ATA Airlines | 9 | 0 | 0 | 0 | 0.000 | 27 of 27 | 0 / 0 | 0 of 0 |
| Northwest Airlines | 9 | 0 | 1 | 1 | 0.002 | 27 of 27 | 0 / 0 | 0 of 0 |
| Continental Airlines | 9 | 0 | 0 | 0 | 0.000 | 27 of 27 | 0 / 0 | 0 of 0 |
| AirTran Airways | 9 | 0 | 0 | 0 | 0.000 | 27 of 27 | 0 / 0 | 0 of 0 |
| US Airways | 9 | 0 | 0 | 0 | 0.000 | 27 of 27 | 0 / 0 | 0 of 0 |
| Virgin America | 9 | 0 | 2 | 2 | 0.009 | 27 of 27 | 0 / 0 | 0 of 0 |
| Spirit Airlines | 1 | 8 | 0 | 0 | 0.000 | 3 of 3 | 1 / 0 | 2 of 2 |
| Commerce Bank (Philadelphia) | 9 | 0 | 0 | 0 | 0.000 | 21 of 27 | 0 / 0 | 0 of 0 |
| North Fork Bank | 9 | 0 | 0 | 0 | 0.000 | 27 of 27 | 0 / 0 | 0 of 0 |
| LaSalle Bank | 9 | 0 | 0 | 0 | 0.000 | 27 of 27 | 0 / 0 | 0 of 0 |
| Washington Mutual | 9 | 0 | 0 | 0 | 0.000 | 27 of 27 | 0 / 0 | 0 of 0 |
| Countrywide | 9 | 0 | 0 | 0 | 0.000 | 27 of 27 | 0 / 0 | 0 of 0 |
| National City | 9 | 0 | 0 | 0 | 0.000 | 27 of 27 | 0 / 0 | 0 of 0 |
| Wachovia | 9 | 0 | 0 | 0 | 0.000 | 27 of 27 | 0 / 0 | 0 of 0 |
| ING Direct | 9 | 0 | 0 | 0 | 0.000 | 27 of 27 | 0 / 0 | 0 of 0 |
| Sovereign Bank | 9 | 0 | 0 | 0 | 0.000 | 27 of 27 | 0 / 1 | 0 of 0 |
| BBVA Compass | 9 | 0 | 0 | 0 | 0.000 | 27 of 27 | 0 / 0 | 0 of 0 |
| SunTrust | 9 | 0 | 4 | 6 | 0.046 | 27 of 27 | 0 / 0 | 0 of 0 |
| BB&T | 9 | 0 | 5 | 5 | 0.039 | 27 of 27 | 0 / 1 | 0 of 0 |
| Union Bank (MUFG Union Bank) | 9 | 0 | 0 | 0 | 0.000 | 27 of 27 | 0 / 0 | 0 of 0 |
| Signature Bank | 9 | 0 | 0 | 0 | 0.000 | 27 of 27 | 0 / 0 | 0 of 0 |
| First Republic Bank | 7 | 2 | 0 | 1 | 0.003 | 21 of 21 | 0 / 0 | 0 of 0 |
| BMO Harris | 9 | 0 | 0 | 1 | 0.007 | 21 of 27 | 0 / 2 | 0 of 0 |
| Silicon Valley Bank | 0 | 9 | 0 | 0 | n/a | -- | 0 / 0 | 3 of 3 |

Table: AI share and market share of each current airline unit (descriptive 1; computed after scoring, DEVIATIONS Entry 2). Market share: share of the category's current units; AI share: mean over the models of each model's share of unit-namings (search off unless stated). Log-log slope of AI share on market share: all nine 0.629, legacy 1.209, current 0.210, current with search 0.448. Each model's own shares are in the values file.

| Unit | Market share | AI share, nine | Legacy | Current | Current, search on |
|:---|---:|---:|---:|---:|---:|
| American Airlines | 21.6% | 10.5% | 12.5% | 6.3% | 5.8% |
| Delta Air Lines | 20.3% | 13.1% | 15.0% | 9.4% | 11.0% |
| United Airlines | 19.7% | 10.2% | 12.4% | 5.7% | 6.5% |
| Southwest Airlines | 17.5% | 12.1% | 14.9% | 6.6% | 7.9% |
| Alaska Airlines | 8.7% | 18.4% | 16.0% | 23.2% | 19.5% |
| JetBlue | 4.7% | 21.4% | 17.5% | 29.1% | 34.8% |
| Frontier Airlines | 4.0% | 4.2% | 5.7% | 1.2% | 0.9% |
| Allegiant Air | 2.2% | 7.7% | 5.8% | 11.6% | 10.1% |
| Breeze Airways | 0.8% | 0.8% | 0.1% | 2.2% | 2.5% |
| Sun Country Airlines | 0.6% | 1.6% | 0.0% | 4.7% | 0.9% |

Table: AI share and market share of each current bank unit (descriptive 1; computed after scoring, DEVIATIONS Entry 2). Market share: share of the category's current units; AI share: mean over the models of each model's share of unit-namings (search off unless stated). Log-log slope of AI share on market share: all nine 0.985, legacy 1.079, current 0.904, current with search 0.787; without the brokerage and wealth holders (D4): 1.001, 1.075, 0.943 and 0.830. Capital One's share does not include Discover's mentions: the locked scorer does not apply pre-registration §2.1 (D12) to Discover (§2.3). Each model's own shares are in the values file.

| Unit | Market share | AI share, nine | Legacy | Current | Current, search on |
|:---|---:|---:|---:|---:|---:|
| Chase (JPMorgan Chase) | 18.1% | 16.4% | 15.7% | 17.9% | 19.5% |
| Bank of America | 16.2% | 14.2% | 15.2% | 12.1% | 9.0% |
| Wells Fargo | 12.7% | 10.7% | 13.2% | 5.7% | 5.6% |
| Citi | 7.3% | 2.7% | 3.2% | 1.9% | 1.5% |
| U.S. Bank | 4.3% | 5.1% | 5.4% | 4.4% | 6.0% |
| Capital One | 4.2% | 11.7% | 9.7% | 15.7% | 17.1% |
| Morgan Stanley | 3.9% | 0.0% | 0.0% | 0.0% | 0.0% |
| Goldman Sachs / Marcus | 3.9% | 4.5% | 5.0% | 3.3% | 3.5% |
| PNC | 3.7% | 4.9% | 5.9% | 2.8% | 1.9% |
| Truist | 3.4% | 1.6% | 1.8% | 1.3% | 1.6% |
| TD Bank | 2.5% | 2.4% | 2.9% | 1.3% | 1.0% |
| Charles Schwab | 2.1% | 4.2% | 1.5% | 9.7% | 9.9% |
| Fifth Third | 2.0% | 0.9% | 0.9% | 1.1% | 1.5% |
| Huntington | 1.8% | 1.0% | 0.9% | 1.3% | 1.9% |
| BMO | 1.6% | 0.5% | 0.2% | 1.0% | 2.1% |
| Citizens | 1.5% | 1.1% | 1.1% | 1.2% | 0.3% |
| First Citizens | 1.4% | 0.7% | 0.7% | 0.6% | 2.1% |
| M&T Bank | 1.4% | 0.7% | 0.7% | 0.7% | 0.9% |
| American Express | 1.4% | 1.0% | 0.7% | 1.6% | 0.3% |
| KeyBank | 1.3% | 0.6% | 0.9% | 0.1% | 0.6% |
| Ally | 1.3% | 13.7% | 13.0% | 15.2% | 12.1% |
| HSBC | 1.1% | 0.0% | 0.0% | 0.0% | 0.0% |
| Regions | 1.1% | 1.4% | 1.4% | 1.3% | 1.6% |
| UBS | 0.9% | 0.0% | 0.0% | 0.0% | 0.0% |
| Pinnacle | 0.8% | 0.0% | 0.0% | 0.0% | 0.0% |

Table: Ghost Presence by model: search-off recommendation answers naming the ghost, of the 48 answers per model and category (descriptive 2; computed after scoring, DEVIATIONS Entry 2). †: post-cutoff exit for that model (not a tested pair). Models: M1 Claude Opus 4.5, M2 Claude Sonnet 4.5, M3 GPT-4o, M4 GPT-4o mini, M5 Gemini 2.5 Flash, M6 Gemini 2.5 Flash-Lite, C1 Claude Fable 5.2, C2 GPT-6 Astra, C3 Gemini 4 Argon. The search-on answers and the gaps are in the values file.

| Ghost | M1 | M2 | M3 | M4 | M5 | M6 | C1 | C2 | C3 |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ATA Airlines | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Northwest Airlines | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| Continental Airlines | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| AirTran Airways | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| US Airways | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Virgin America | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 1 |
| Spirit Airlines | 3† | 6† | 11† | 16† | 22† | 21† | 0 | 0† | 10† |
| Commerce Bank (Philadelphia) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| North Fork Bank | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LaSalle Bank | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Washington Mutual | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Countrywide | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| National City | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Wachovia | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ING Direct | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Sovereign Bank | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| BBVA Compass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| SunTrust | 0 | 4 | 3 | 3 | 4 | 3 | 0 | 0 | 3 |
| BB&T | 0 | 4 | 3 | 0 | 4 | 3 | 0 | 0 | 3 |
| Union Bank (MUFG Union Bank) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Signature Bank | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| First Republic Bank | 0 | 1 | 0† | 0† | 0 | 0 | 0 | 0 | 0 |
| BMO Harris | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |
| Silicon Valley Bank | 0† | 0† | 0† | 0† | 0† | 3† | 0† | 0† | 0† |

<!-- APPENDIX A END -->
