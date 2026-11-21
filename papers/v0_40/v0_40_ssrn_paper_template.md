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
{{AUTHOR_CORRESPONDENCE}}
ORCID: \href{https://orcid.org/0009-0003-8968-9990}{0009-0003-8968-9990}\\[20pt]

Pre-registration: \texttt{v0.40-prereg-r1} (commit \texttt{a53d2b7})\\
locked and deposited on OSF before the first study call\\[4pt]
Data and code: OSF \texttt{ec6wh}, \texttt{v40}\\[4pt]
November 2026

\end{center}
\end{titlepage}

# Abstract {-}

Do AI assistants name brands in proportion to their market share, and do brands that have left the market keep a place in their answers? This pre-registered study asked nine large language models (a legacy panel of six and the newest generally available flagship of three providers, as checked on 12 November 2026, with and without web search) about US airlines and US retail banks, including the brands retired by merger, failure or rename since 2008 ("ghosts"). All {{v:acquisition.records_total}} planned calls were answered, for {{v:cost.paper_total_usd}} of a {{v:cost.paper_cap_usd}} cap. A rule-based coder met the registered agreement threshold with an AI-only audit (κ {{v:audit.threshold.kappa}}), but not on recommendation answers alone (κ {{v:audit.agreement.consensus_vs_rule.gone_flag.recommendation.kappa}}).
The models' naming followed market share in both categories (Spearman ρ {{v:H_Reinforce.airline.rho}} for airlines and {{v:H_Reinforce.bank.rho}} for banks; {{v:H_Reinforce.verdict}}), though the airline result failed a pre-registered sensitivity (ρ {{v:sensitivity.S-SunCountry.H_Reinforce_airline.rho}}). The leaders' share of all brand namings was below their market share ({{v:H_Amplify.airline.ratio}} and {{v:H_Amplify.bank.ratio}}; {{v:H_Amplify.verdict}}), but because answers name many brands the registered ratio could not have reached the amplification threshold, and the bank leader was named in most bank answers. Ghosts were named without a gone-flag in {{v:H_Afterlife.airline.rate}} and {{v:H_Afterlife.bank.rate}} of ghost-model pairs, between the registered null and pass lines ({{v:H_Afterlife.verdict}}). Ghost Presence was lower at longer gaps between exit and training cutoff (ρ {{v:H_Decay.rho}}, {{v:H_Decay.pairs_present}} of {{v:H_Decay.pairs}} pairs named; {{v:H_Decay.verdict}}). Status answers about ghosts carried a gone-flag in {{v:H_Flag.ghost_rate}} of cases against {{v:H_Flag.control_rate}} for living brands ({{v:H_Flag.verdict}}). With web search on, all {{v:H_Search.post_cutoff_cells}} post-cutoff cells were flagged, but the paired test had too few discordant cells ({{v:H_Search.verdict}}), and one model searched in {{v:manipulation_checks.MC2_search_used_C3.searched}} of {{v:manipulation_checks.MC2_search_used_C3.n}} search-on answers. Every test is reported, including failures.

**Keywords:** AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; large language models; Double Jeopardy; market share; brand exits; mergers; web search; airlines; retail banking

**JEL codes:** M31; L86, L15, D83, M37

**Paper status:** Pre-registered confirmatory study (tag `v0.40-prereg-r1`, locked and deposited on OSF before the first study call); scored once (`score_v0_40.py`); deviations recorded in `osf/v40/DEVIATIONS.md`. Part of the AIAS measurement programme.

# 1. Introduction

AI Availability, the discoverability and representation of a brand in the answers of large language models (LLMs), has been proposed as a third measurable layer of brand availability (González Castro, 2026, SSRN 6659000), beside the Mental and Physical Availability of the Ehrenberg-Bass tradition (Sharp, 2010; Romaniuk & Sharp, 2016), and measured under a versioned protocol (Methodology v1.2--v1.8; AIAS 1.0) in a series of category phases (González Castro, 2026, phase papers v0.16--v0.37). The Tri-System framework (González Castro, 2026, MSI Working Paper, Report No. 26-132) treats AI as a mediation layer between brand and buyer and takes the name "System 3", for artificial cognition beside human fast and slow thinking, from Shaw and Nave (2026, SSRN 6097646). The framework's first proposition, P1, asks whether AI answers track, amplify or flatten the market position of brands. That had not been measured against an official share base.

Outside this programme, work on LLMs in marketing has asked whether model outputs reproduce consumer perceptions of brands (Li, Castelo, Katona & Sarvary, 2024), how content can be shaped to appear in generative answers (Aggarwal et al., 2024), and how buyer personas change which brands are recommended (Jack, Lehman, Maloney & Xu, 2026; Rienecker et al., 2026). Work on language models as knowledge bases has shown that facts change after training and that models answer from the time of their data (Dhingra et al., 2022). Brand management has studied what happens to brands deleted or absorbed after a merger (Varadarajan, DeFanti & Busch, 2006). This study joins the three: it measures AI naming against official market shares, and it uses dated brand exits against each model's published training cutoff as a natural test of what models say about brands that no longer exist. Its contribution is a pre-registered, two-arm measurement in two categories with official share data (airlines: revenue passenger miles, Bureau of Transportation Statistics T-100; retail banks: deposits, FDIC Summary of Deposits) and many dated exits, which we call ghosts.

Six hypotheses were fixed before data (§2.3): H_Reinforce (AI share tracks market share), H_Amplify (AI amplifies the category leader, as Double Jeopardy would suggest; Ehrenberg, Goodhardt & Barwise, 1990), H_Afterlife (ghosts are still named as if current), H_Decay (ghost Presence decays with the exit-to-cutoff gap), H_Flag (status answers say a ghost is gone, and do not say so of living brands) and H_Search (web search corrects the status of ghosts). The study is the programme's first public flagship study under its independence rule: there is no focal brand, no finding is addressed to a brand, and no brand was contacted.

# 2. Method

## 2.1 Registry

The brand registry was built mechanically from official data under rules fixed in advance and frozen on 12 November 2026 (pre-registration §3). Current units are the airline share units ({{v:H_Reinforce.airline.n_units}}, with Hawaiian counted inside Alaska) and the bank holding companies above the registry's deposit floor ({{v:H_Reinforce.bank.n_units}}). Market share is the allocated brand share of revenue passenger miles for airlines and the share of deposits for banks. The ghosts are the airline and bank brands retired by merger, failure or rename from 2008 to the freeze (for example Continental, US Airways, Virgin America, Washington Mutual, Wachovia, SunTrust, BB&T, Silicon Valley Bank and First Republic). In each category the largest current unit is the leader (American Airlines; the JPMorgan Chase holder) and the other current units are the challengers. Hawaiian and Sun Country (airlines) and Discover (banks) are the living-brand controls, and American, Delta, Chase and Bank of America the incumbent controls. Discover's deposit accounts were being moved to Capital One during the study; the pre-registrant kept it as the bank control and declared a sensitivity without it (§2.5). Each model's training cutoff is the vendor's published month; the gap of a ghost-model pair is the number of months from the brand's retirement to that cutoff, and a pair with a positive gap is a pre-cutoff exit.

## 2.2 Probes, panel and collection

The probe set (pre-registration §4.1) has, per category, brand-free recommendation questions (generic, by need and by US Census region), and, for each ghost and control, one recognition question and one status question (whether one can still book with, or open an account at, the brand). Questions were asked in one user turn with no system prompt and no buyer persona.

The legacy arm is the programme's six-model panel fixed since v0.17 (Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o mini, Gemini 2.5 Flash with thinking budget 0, Gemini 2.5 Flash-Lite; temperature 0), plus one extra Gemini 2.5 Flash pass at the provider's default thinking that is reported and never tested. The current arm is each provider's newest generally available flagship as checked on the vendors' pages on 12 November 2026 (pre-registration §4.3): Claude Fable 5.2 (C1), GPT-6 Astra (C2) and Gemini 4 Argon (C3), at provider defaults, with search off (three runs) and with each provider's own web search on (one run on the recommendation and status probes; pre-registration §4.2--§4.4, §6.3--§6.4). The record is not consistent on one point: the pre-registration's check found no Gemini API statement that Gemini 4 Carbon was generally available, while DEVIATIONS Entry 1, written on 21 November for the audit, quotes a Gemini API changelog entry dated 10 November that declares it generally available, and notes that GPT-6.2 Astra is newer than GPT-6 Astra. Under the pre-registration's own rule, a generally available Carbon before the lock would have replaced Argon; the study ran with Argon as locked.

Collection ran from 17 to 19 November 2026 under a cost guard. All {{v:acquisition.records_total}} planned calls returned an answer ({{v:acquisition.records_ok}} with status ok; legacy search off {{v:acquisition.records.L.S0}}, current search off {{v:acquisition.records.C.S0}}, current search on {{v:acquisition.records.C.S1}}); none failed and none was re-run. The collection's recorded spend was {{v:cost.collection_usd}}; with the two declared pre-lock checks ({{v:cost.prelock_total_usd}}) the guard's spend was {{v:cost.acquisition_recorded_usd}}, and with the audit (§2.6, {{v:cost.audit_usd}}) the paper's total is {{v:cost.paper_total_usd}} against a cap of {{v:cost.paper_cap_usd}} and a pause at {{v:cost.pause_at_usd}}. A length-limit stop rule checked every answer as it arrived; no answer stopped at its token limit before naming a brand ({{v:coding.cut_before_first_brand_missing}} treated as missing).

## 2.3 Measures and tests

A **mention** is a whole-word, case-sensitive match of a registry alias; the longest alias wins. Bare names that collide with ordinary words or other brands (for example "American", "United", "Delta", "Discover") are coded ambiguous and excluded from every primary test, and every result is also reported with them (S-Ambig). The **AI share** of a current unit is, per model, the number of its search-off recommendation answers naming the unit divided by the same count summed over all current units of the category, averaged over the nine tested models (legacy six and current three, search off). A mention is **gone-flagged** when a locked lexicon ("no longer", "defunct", "merged into", "acquired by", "now part of", "rebranded", "failed" and similar) occurs within {{v:window_chars}} characters of it. The coder recorded {{v:coding.mentions}} mentions in {{v:coding.answers}} answers. No LLM was used as coder or judge. **Ghost Presence** of a ghost for a model is the share of the model's search-off recommendation answers in the ghost's category that name it (any run; ambiguous mentions excluded). For H_Amplify, k counts the answers that name the leader, while n adds up, over all current units, the answers that name each unit, so an answer naming four units counts four times in n (pre-registration §2.3).

Table: Pre-registered tests (pre-registration §2.2--§2.7). One-sided, α = 0.05, no multiplicity correction; permutation tests use {{v:permutations}} permutations with seed {{v:seed}}.

| Test | Statistic | Rule |
|:----------------|:----------------------------------------|:------------------------------------------|
| H_Reinforce | Spearman ρ, market share against AI share, per category; permutation test (ρ > 0) | A category passes with ρ ≥ {{v:thresholds.reinforce_rho}}, p < 0.05 and at least {{v:thresholds.min_units_present}} units named; CONFIRMED if both pass, PARTIAL if one |
| H_Amplify | Leader's ratio (k/n)/p₀ over the nine models; exact binomial test both ways | Amplified: ratio ≥ {{v:thresholds.amplify_ratio}} and p(X ≥ k) < 0.05; flattened: ratio < 1 and p(X ≤ k) < 0.05; CONFIRMED if amplified in both, FALSIFIED if flattened in both |
| H_Afterlife | Share of pre-cutoff ghost × model pairs named in a recommendation answer without a gone-flag; exact binomial test against {{v:thresholds.afterlife_null}} | A category passes with rate ≥ {{v:thresholds.afterlife_rate}} and p < 0.05; low below {{v:thresholds.afterlife_null}}; CONFIRMED if both pass, FALSIFIED if both low |
| H_Decay | Spearman ρ, gap in months against ghost Presence, over pre-cutoff pairs; permutation within model (ρ < 0) | CONFIRMED: ρ ≤ {{v:thresholds.decay_rho}} and p < 0.05; PARTIAL: ρ < 0, p < 0.05, ρ > {{v:thresholds.decay_rho}}; evaluable with at least {{v:thresholds.decay_min_present}} pairs named |
| H_Flag | Flag rate of ghost status answers against control status answers; one-sided Fisher exact test | CONFIRMED: ghost rate ≥ {{v:thresholds.flag_rate}} and p < 0.05; FALSIFIED: rate < {{v:thresholds.flag_floor}} and p ≥ 0.05 |
| H_Search | Exact McNemar test, current models, ghost status cells, search off (majority of three runs) against on; post-cutoff search-on flag rate | McNemar part: at least {{v:thresholds.search_min_discordant}} discordant cells and p < 0.05; post-cutoff part: rate ≥ {{v:thresholds.search_post_rate}}; CONFIRMED if both, PARTIAL if one |

## 2.4 Manipulation checks

Four checks were fixed before any verdict was read (pre-registration §2.8): completeness of each arm, search use by each current model with search on, recognition of the four incumbents, and truncation at the output cap. Their limits are those of pre-registration §2.8; the results are in Table 2.

## 2.5 Sensitivity analyses

Pre-registered sensitivities are reported beside each verdict and change none (pre-registration §5.6, §5.9): S-Ambig (ambiguous mentions included), S-Legal (legal-date gaps in place of brand-retirement gaps), S-Operating (airline operating share, with Delta as the leader), S-SunCountry (Sun Country inside Allegiant), S-D4 (banks without the three brokerage and wealth holders), S-Discover (H_Flag without the bank living-brand control), S-Arm (each test on the legacy and on the current arm alone) and S-Length (without the {{v:sensitivity.S-Length.excluded_answers}} answers that stopped at the length limit after naming a brand or used half the limit or more on thinking).

## 2.6 Audit of the coder

The declared audit sample (pre-registration §5.5) was drawn by script with seed {{v:seed}} after coding and before any verdict: recommendation answers with a ghost or control mention and status answers, stratified by arm, condition and role, {{v:audit.answers.total}} answers in all. DEVIATIONS Entry 1 (21 November 2026, written before the draw) replaced the human analyst named in the pre-registration with an AI-only analyst and added a coding-only step so that the sample could be drawn before scoring. Two blind coders from two providers, {{v:audit.coders.A}} and {{v:audit.coders.B}}, coded each answer from the written rules; {{v:audit.coders.T}} broke ties ({{v:audit.answers.tie_broken}} of {{v:audit.answers.total}} answers). **The audit has no human check**: no person coded or reviewed the sampled answers or the AI codes. The AI codes never replaced a rule-based code. The audit cost {{v:cost.audit_usd}} against its {{v:cost.audit_cap_usd}} cap.

## 2.7 Pre-registration, lock and deviations

The pre-registration was locked at tag `v0.40-prereg-r1` (commit a53d2b7) on 16 November 2026 and deposited on OSF (`ec6wh`, folders v40/prereg and v40/registries), every file verified by SHA-256, before the first study call. One discrepancy in the locked file is reported here rather than corrected: its first line still reads "revision r1, DRAFT for the pre-registrant's review --- not locked", and its status line describes the draft. The file was edited only at the lock, to correct §9's test count (DEVIATIONS lock record), and not after; what makes it locked is the tag, the lock manifest (`prereg/LOCK_MANIFEST_v0_40.sha256`) and the OSF deposit, all recorded in the lock entry of `DEVIATIONS.md`. Besides that lock record and the collection records, the study has two dated entries: Entry 0 (ex ante, the conflict-of-interest screen of the registry; Declarations) and Entry 1 (the coding-only step, the scripted audit draw and the AI-only analyst, §2.6). The scorer ran once, unchanged, after the audit; the mentions file it rewrote matched the coding step's SHA-256.

# 3. Results

## 3.1 Manipulation checks

Table: Manipulation checks (pre-registration §2.8).

| Check | Result | Pass |
|:------------------------------|:------------------------------------|:-----|
| MC1 completeness, legacy | {{v:manipulation_checks.MC1_complete_L.ok_calls}} of {{v:manipulation_checks.MC1_complete_L.expected}} ok | {{v:manipulation_checks.MC1_complete_L.pass}} |
| MC1 completeness, current | {{v:manipulation_checks.MC1_complete_C.ok_calls}} of {{v:manipulation_checks.MC1_complete_C.expected}} ok | {{v:manipulation_checks.MC1_complete_C.pass}} |
| MC2 search used, Claude Fable 5.2 | {{v:manipulation_checks.MC2_search_used_C1.searched}} of {{v:manipulation_checks.MC2_search_used_C1.n}} answers | {{v:manipulation_checks.MC2_search_used_C1.pass}} |
| MC2 search used, GPT-6 Astra | {{v:manipulation_checks.MC2_search_used_C2.searched}} of {{v:manipulation_checks.MC2_search_used_C2.n}} answers | {{v:manipulation_checks.MC2_search_used_C2.pass}} |
| MC2 search used, Gemini 4 Argon | {{v:manipulation_checks.MC2_search_used_C3.searched}} of {{v:manipulation_checks.MC2_search_used_C3.n}} answers | **{{v:manipulation_checks.MC2_search_used_C3.pass}}** |
| MC3 incumbents recognised | {{v:manipulation_checks.MC3_incumbents_recognised.named}} of {{v:manipulation_checks.MC3_incumbents_recognised.n}} answers | {{v:manipulation_checks.MC3_incumbents_recognised.pass}} |
| MC4 truncation, legacy (limit {{v:manipulation_checks.MC4_truncation_L.limit}}) | {{v:manipulation_checks.MC4_truncation_L.truncated}} of {{v:manipulation_checks.MC4_truncation_L.n}} | {{v:manipulation_checks.MC4_truncation_L.pass}} |
| MC4 truncation, current (limit {{v:manipulation_checks.MC4_truncation_C.limit}}) | {{v:manipulation_checks.MC4_truncation_C.truncated}} of {{v:manipulation_checks.MC4_truncation_C.n}} | {{v:manipulation_checks.MC4_truncation_C.pass}} |

Every check passed except MC2 for Gemini 4 Argon, which searched in {{v:manipulation_checks.MC2_search_used_C3.searched}} of its {{v:manipulation_checks.MC2_search_used_C3.n}} search-on answers. As registered, not searching is part of the condition and those answers are kept; H_Search is reported with this caveat (§3.8). The legacy truncations are the extra Gemini 2.5 Flash pass ({{v:descriptives.5_M5X_vs_M5.M5X.truncated}} of {{v:descriptives.5_M5X_vs_M5.M5X.calls}}, expected at its setting) and Gemini 2.5 Flash at thinking budget 0 ({{v:descriptives.5_M5X_vs_M5.M5.truncated}} of {{v:descriptives.5_M5X_vs_M5.M5.calls}}), each after a brand had been named.

## 3.2 Coder reliability

The AI consensus agreed with the rule-based gone-flag on {{v:audit.agreement.consensus_vs_rule.gone_flag.all.agree}} of {{v:audit.agreement.consensus_vs_rule.gone_flag.all.n}} coded entities ({{v:audit.agreement.consensus_vs_rule.gone_flag.all.percent_agreement}}; κ {{v:audit.threshold.kappa}} against the registered {{v:audit.threshold.kappa_min}}; threshold met: {{v:audit.threshold.met}}). The disagreements were asymmetric: the rule flagged {{v:audit.agreement.consensus_vs_rule.gone_flag.all.table.rule1_ai0}} entities the consensus did not, and missed {{v:audit.agreement.consensus_vs_rule.gone_flag.all.table.rule0_ai1}} that the consensus flagged. On the status answers κ was {{v:audit.agreement.consensus_vs_rule.gone_flag.status.kappa}}; on the recommendation answers alone it was {{v:audit.agreement.consensus_vs_rule.gone_flag.recommendation.kappa}} (of {{v:audit.agreement.consensus_vs_rule.gone_flag.recommendation.n}} entities, the rule missed {{v:audit.agreement.consensus_vs_rule.gone_flag.recommendation.table.rule0_ai1}} flags and added {{v:audit.agreement.consensus_vs_rule.gone_flag.recommendation.table.rule1_ai0}}). The registered threshold applies to the whole sample and was met, but the recommendation-answer subset, on which H_Afterlife rests, falls well short of it: in the sample, the rule left {{v:audit.sample_rates.rule.rec_ghost_mentions_not_gone_flagged_rate}} of {{v:audit.sample_rates.rule.rec_ghost_mentions}} recommendation ghost mentions unflagged, the AI consensus {{v:audit.sample_rates.ai.rec_ghost_mentions_not_gone_flagged_rate}}. The rule-based afterlife rates below are therefore more likely too high than too low. Subject and ambiguity codes agreed almost perfectly (κ {{v:audit.agreement.consensus_vs_rule.subject.all.kappa}} and {{v:audit.agreement.consensus_vs_rule.ambiguous.all.kappa}}); the successor-name code had κ {{v:audit.agreement.consensus_vs_rule.successor_near.all.kappa}}, and the two AI coders agreed with each other on the gone-flag at κ {{v:audit.agreement.A_vs_B.gone_flag.all.kappa}}.

## 3.3 H_Reinforce: AI share rises with market share in both categories ({{v:H_Reinforce.verdict}})

Across the nine models, AI share rose with market share in airlines (ρ = {{v:H_Reinforce.airline.rho}}, p = {{v:H_Reinforce.airline.p_perm}}, {{v:H_Reinforce.airline.units_present}} of {{v:H_Reinforce.airline.n_units}} units named) and in banks (ρ = {{v:H_Reinforce.bank.rho}}, p {{v:H_Reinforce.bank.p_perm}}, {{v:H_Reinforce.bank.units_present}} of {{v:H_Reinforce.bank.n_units}} units named); both categories passed and the verdict is {{v:H_Reinforce.verdict}} (Figure 1). The bank result held in every specification, including without the brokerage and wealth holders (S-D4, ρ = {{v:sensitivity.S-D4.rho}}). The airline result is fragile. It held with ambiguous mentions included (ρ = {{v:sensitivity.S-Ambig.H_Reinforce.airline.rho}}) and on operating share (ρ = {{v:sensitivity.S-Operating.H_Reinforce_airline.rho}}), but it failed the registered rule when Sun Country was placed inside Allegiant (S-SunCountry: ρ = {{v:sensitivity.S-SunCountry.H_Reinforce_airline.rho}}, p = {{v:sensitivity.S-SunCountry.H_Reinforce_airline.p_perm}}) and on the current arm alone (ρ = {{v:sensitivity.S-Arm.current.H_Reinforce.airline.rho}}, p = {{v:sensitivity.S-Arm.current.H_Reinforce.airline.p_perm}}; current-arm verdict {{v:sensitivity.S-Arm.current.H_Reinforce.verdict}}). With ten airline units, the placement of one unit moves the rank correlation across the line; the airline half of the verdict rests on that choice and on the legacy models.

![Spearman correlation of market share with AI share for each category, panel and pre-registered specification. Filled markers meet the registered rule.](../../reports/figs/v40/paper/fig_01_reinforce.pdf){#fig:reinforce width=100%}

## 3.4 H_Amplify: the leaders' share of namings is below their market share, on a ratio with a ceiling ({{v:H_Amplify.verdict}})

By the registered rule the leaders were not amplified but flattened (Figure 2). American Airlines accounted for {{v:H_Amplify.airline.k}} of the {{v:H_Amplify.airline.n}} airline unit-namings against a market share of {{v:H_Amplify.airline.p0}} of the current units, a ratio of {{v:H_Amplify.airline.ratio}} (p(X ≤ k) {{v:H_Amplify.airline.p_less}}). The JPMorgan Chase holder accounted for {{v:H_Amplify.bank.k}} of {{v:H_Amplify.bank.n}}, ratio {{v:H_Amplify.bank.ratio}} (p(X ≤ k) = {{v:H_Amplify.bank.p_less}}). Both categories meet the registered "flattened" rule, so H_Amplify is {{v:H_Amplify.verdict}}. The verdict stands as registered, but the ratio has a ceiling that the pre-registration did not anticipate. k counts answers that name the leader and cannot exceed the number of answers, while n counts every current unit named in every answer. Answers named several units each, so at the observed breadth of answers even a leader named in every answer would have had a ratio below the amplification threshold in airlines and below parity in banks. The "flattening" therefore describes the leader's share of the namings inside answers that list many brands; it does not mean the leader was left out. The JPMorgan Chase holder was named in {{v:H_Amplify.bank.k}} of the {{v:descriptives.8_near_floor_other.L_S0.answers}} legacy and {{v:descriptives.8_near_floor_other.C_S0.answers}} current bank recommendation answers. American's count is also lowered by the ambiguity rule, which excludes the bare name "American": with it included (S-Ambig), American was named in {{v:sensitivity.S-Ambig.H_Amplify.airline.k}} answers instead of {{v:H_Amplify.airline.k}} (ratio {{v:sensitivity.S-Ambig.H_Amplify.airline.ratio}}). The binomial test also treats each naming as an independent draw. The airline result holds with Delta as leader on operating share (ratio {{v:sensitivity.S-Operating.H_Amplify_airline.ratio}}); on the current arm alone the bank ratio was {{v:sensitivity.S-Arm.current.H_Amplify.bank.ratio}} and not significant either way (current-arm verdict {{v:sensitivity.S-Arm.current.H_Amplify.verdict}}). The descriptive log-log slopes of AI share on market share, which carry no verdict, were {{v:H_Amplify.airline.loglog_slope}} for airlines and {{v:H_Amplify.bank.loglog_slope}} for banks (the slope without the brokerage holders is not in the scored record; §3.10).

![The leader's share of AI naming divided by its market share, per category, panel and specification; dashed lines at parity and at the registered amplification threshold.](../../reports/figs/v40/paper/fig_02_amplify.pdf){#fig:amplify width=100%}

## 3.5 H_Afterlife: ghosts named without a gone-flag fall between the null and the pass line ({{v:H_Afterlife.verdict}})

Of the pre-cutoff ghost × model pairs, {{v:H_Afterlife.airline.afterlife_pairs}} of {{v:H_Afterlife.airline.pairs}} airline pairs ({{v:H_Afterlife.airline.rate}}, p = {{v:H_Afterlife.airline.p_exact}}) and {{v:H_Afterlife.bank.afterlife_pairs}} of {{v:H_Afterlife.bank.pairs}} bank pairs ({{v:H_Afterlife.bank.rate}}, p = {{v:H_Afterlife.bank.p_exact}}) had at least one search-off recommendation answer naming the ghost without a gone-flag (Figure 3). Neither category reached the registered pass rate, and neither fell below the registered low rate, so H_Afterlife is {{v:H_Afterlife.verdict}}. With ambiguous names included the airline rate rose to {{v:sensitivity.S-Ambig.H_Afterlife.airline.rate}} (p = {{v:sensitivity.S-Ambig.H_Afterlife.airline.p_exact}}), still below the pass rate. Because the audit found the rule more likely to miss a gone-flag than to add one in recommendation answers (§3.2), these rates are more likely too high than too low.

![Afterlife rate per category by panel and specification, against the registered null and pass lines.](../../reports/figs/v40/paper/fig_03_afterlife.pdf){#fig:afterlife width=100%}

## 3.6 H_Decay: ghost Presence is lower at longer exit-to-cutoff gaps, below the registered strength ({{v:H_Decay.verdict}})

Over the {{v:H_Decay.pairs}} pre-cutoff pairs, of which {{v:H_Decay.pairs_present}} had a ghost Presence above zero (floor {{v:thresholds.decay_min_present}}), the correlation between gap and ghost Presence was ρ = {{v:H_Decay.rho}} (p {{v:H_Decay.p_perm}}): negative and significant, but short of the registered {{v:thresholds.decay_rho}}, so H_Decay is {{v:H_Decay.verdict}} (Figure 4). The legacy arm alone met the CONFIRMED band (ρ = {{v:sensitivity.S-Arm.legacy.H_Decay.rho}}, p {{v:sensitivity.S-Arm.legacy.H_Decay.p_perm}}, {{v:sensitivity.S-Arm.legacy.H_Decay.pairs_present}} pairs named); the current arm had only {{v:sensitivity.S-Arm.current.H_Decay.pairs_present}} pairs named, below the floor, and is {{v:sensitivity.S-Arm.current.H_Decay.verdict}}. The direction held under S-Ambig (ρ = {{v:sensitivity.S-Ambig.H_Decay.rho}}) and S-Legal (ρ = {{v:sensitivity.S-Legal.H_Decay.rho}}). Most pairs have zero Presence, so the correlation rests on few named pairs and many ties.

![Correlation of the exit-to-cutoff gap with ghost Presence by panel and specification, with the number of pairs named.](../../reports/figs/v40/paper/fig_04_decay.pdf){#fig:decay width=100%}

## 3.7 H_Flag: status answers about ghosts carry a gone-flag ({{v:H_Flag.verdict}})

Asked whether one can still book with or open an account at a ghost, the nine models' answers carried a gone-flag in {{v:H_Flag.ghost_flagged}} of {{v:H_Flag.ghost_answers}} answers ({{v:H_Flag.ghost_rate}}), against {{v:H_Flag.control_flagged}} of {{v:H_Flag.control_answers}} answers about living brands ({{v:H_Flag.control_rate}}; Fisher p {{v:H_Flag.p_fisher}}); H_Flag is {{v:H_Flag.verdict}} (Figure 5). Without Discover the control rate was {{v:sensitivity.S-Discover.control_rate}}. The control rate differs by arm: {{v:sensitivity.S-Arm.legacy.H_Flag.control_rate}} for the legacy models and {{v:sensitivity.S-Arm.current.H_Flag.control_rate}} ({{v:sensitivity.S-Arm.current.H_Flag.control_flagged}} of {{v:sensitivity.S-Arm.current.H_Flag.control_answers}}) for the current models, which flagged every ghost answer ({{v:sensitivity.S-Arm.current.H_Flag.ghost_rate}}). Part of the control flagging is expected and may be correct: two living-brand controls were in recent mergers or account moves (Hawaiian with Alaska; Discover with Capital One), and the gone-flag lexicon fires on a merger mentioned near the brand. In the audit sample, the AI consensus flagged {{v:audit.sample_rates.ai.status_control_flag_rate}} of the {{v:audit.sample_rates.ai.status_control_answers}} sampled control answers, against {{v:audit.sample_rates.rule.status_control_flag_rate}} for the rule.

![Gone-flag rate of status answers about ghosts and about living brands, by panel and without the bank living-brand control.](../../reports/figs/v40/paper/fig_05_flag.pdf){#fig:flag width=100%}

## 3.8 H_Search: post-cutoff exits flagged with search on; the paired test is not evaluable ({{v:H_Search.verdict}})

Of the {{v:H_Search.paired_cells}} paired ghost × current-model status cells, {{v:H_Search.s1_only_flagged}} was flagged with search on only and {{v:H_Search.s0_only_flagged}} with search off only (exact McNemar p = {{v:H_Search.p_mcnemar_exact}}); with fewer than {{v:thresholds.search_min_discordant}} discordant cells the McNemar part fails its registered floor. The discordant cells went against the hypothesis (more flagged with search off only than with search on only). Without search the current models already flagged nearly every ghost, so there was little left for search to correct. The post-cutoff part passed: with search on, the current models flagged all {{v:H_Search.post_cutoff_cells}} cells in which the exit came after the model's cutoff ({{v:H_Search.post_cutoff_s1_rate}}). These cells come from two brands (Silicon Valley Bank for all three models, Spirit for two), and there is no search-off figure for them in the scored record, so the count is small and does not show what search added. One part passing gives {{v:H_Search.verdict}} (Figure 6). The verdict carries the MC2 caveat: Gemini 4 Argon searched in only {{v:manipulation_checks.MC2_search_used_C3.searched}} of {{v:manipulation_checks.MC2_search_used_C3.n}} search-on answers. When a ghost status answer was flagged with search on, the most frequently cited domains were Google's grounding redirect ({{v:descriptives.7_search_traces.domains_cited_when_ghost_flagged.vertexaisearch.cloud.google.com}} citations), en.wikipedia.org ({{v:descriptives.7_search_traces.domains_cited_when_ghost_flagged.en.wikipedia.org}}), reddit.com ({{v:descriptives.7_search_traces.domains_cited_when_ghost_flagged.reddit.com}}) and sec.gov ({{v:descriptives.7_search_traces.domains_cited_when_ghost_flagged.sec.gov}}).

![Discordant ghost status cells of the current models with search off and on, and the search-on flag rate on post-cutoff cells.](../../reports/figs/v40/paper/fig_06_search.pdf){#fig:search width=100%}

## 3.9 Summary of verdicts and sensitivities

Table: Verdicts and sensitivity verdicts. "--" marks a sensitivity that does not apply to the test.

| Test | Verdict | S-Ambig | S-Length | Legacy arm | Current arm |
|:--------------|:--------------|:--------------|:--------------|:--------------|:--------------|
| H_Reinforce | {{v:H_Reinforce.verdict}} | {{v:sensitivity.S-Ambig.H_Reinforce.verdict}} | {{v:sensitivity.S-Length.H_Reinforce.verdict}} | {{v:sensitivity.S-Arm.legacy.H_Reinforce.verdict}} | {{v:sensitivity.S-Arm.current.H_Reinforce.verdict}} |
| H_Amplify | {{v:H_Amplify.verdict}} | {{v:sensitivity.S-Ambig.H_Amplify.verdict}} | {{v:sensitivity.S-Length.H_Amplify.verdict}} | {{v:sensitivity.S-Arm.legacy.H_Amplify.verdict}} | {{v:sensitivity.S-Arm.current.H_Amplify.verdict}} |
| H_Afterlife | {{v:H_Afterlife.verdict}} | {{v:sensitivity.S-Ambig.H_Afterlife.verdict}} | {{v:sensitivity.S-Length.H_Afterlife.verdict}} | {{v:sensitivity.S-Arm.legacy.H_Afterlife.verdict}} | {{v:sensitivity.S-Arm.current.H_Afterlife.verdict}} |
| H_Decay | {{v:H_Decay.verdict}} | {{v:sensitivity.S-Ambig.H_Decay.verdict}} | {{v:sensitivity.S-Length.H_Decay.verdict}} | {{v:sensitivity.S-Arm.legacy.H_Decay.verdict}} | {{v:sensitivity.S-Arm.current.H_Decay.verdict}} |
| H_Flag | {{v:H_Flag.verdict}} | {{v:sensitivity.S-Ambig.H_Flag.verdict}} | {{v:sensitivity.S-Length.H_Flag.verdict}} | {{v:sensitivity.S-Arm.legacy.H_Flag.verdict}} | {{v:sensitivity.S-Arm.current.H_Flag.verdict}} |
| H_Search | {{v:H_Search.verdict}} | {{v:sensitivity.S-Ambig.H_Search.verdict}} | {{v:sensitivity.S-Length.H_Search.verdict}} | -- | {{v:sensitivity.S-Arm.current.H_Search.verdict}} |

The single-category sensitivities carry no verdict of their own: S-Operating passed the airline rule (ρ = {{v:sensitivity.S-Operating.H_Reinforce_airline.rho}}) and flattened Delta (ratio {{v:sensitivity.S-Operating.H_Amplify_airline.ratio}}); S-SunCountry failed the airline rule (ρ = {{v:sensitivity.S-SunCountry.H_Reinforce_airline.rho}}) and flattened American (ratio {{v:sensitivity.S-SunCountry.H_Amplify_airline.ratio}}); S-D4 passed the bank rule (ρ = {{v:sensitivity.S-D4.rho}}); S-Discover kept H_Flag {{v:sensitivity.S-Discover.verdict}}; S-Legal left H_Afterlife {{v:sensitivity.S-Legal.H_Afterlife.verdict}} and H_Decay {{v:sensitivity.S-Legal.H_Decay.verdict}}.

## 3.10 Descriptives

*Old versus new name.* Of the ghost mentions, the successor's name appeared within the same window in {{v:descriptives.3_old_vs_new_name.L_S0.share}} for the legacy models ({{v:descriptives.3_old_vs_new_name.L_S0.with_successor}} of {{v:descriptives.3_old_vs_new_name.L_S0.ghost_mentions}}), {{v:descriptives.3_old_vs_new_name.C_S0.share}} for the current models without search and {{v:descriptives.3_old_vs_new_name.C_S1.share}} with search ({{v:descriptives.3_old_vs_new_name.C_S1.with_successor}} of {{v:descriptives.3_old_vs_new_name.C_S1.ghost_mentions}}).

*Run-to-run precision.* The standard error of per-model Presence across the three search-off runs averaged {{v:descriptives.6_run_to_run_se.L.se_mean}} in the legacy arm ({{v:descriptives.6_run_to_run_se.L.se_mean_some_not_all}} for units named in some answers but not all) and {{v:descriptives.6_run_to_run_se.C.se_mean}} in the current arm ({{v:descriptives.6_run_to_run_se.C.se_mean_some_not_all}}), below the method v1.17 planning estimates quoted in pre-registration §2.10.

*Near-floor banks.* Of the brands below the bank deposit floor, legacy recommendation answers ({{v:descriptives.8_near_floor_other.L_S0.answers}}) named USAA {{v:descriptives.8_near_floor_other.L_S0.USAA}} times, Synchrony {{v:descriptives.8_near_floor_other.L_S0.Synchrony}}, Santander {{v:descriptives.8_near_floor_other.L_S0.Santander}}, Zions {{v:descriptives.8_near_floor_other.L_S0.Zions}}, Western Alliance {{v:descriptives.8_near_floor_other.L_S0.Western Alliance}} and RBC {{v:descriptives.8_near_floor_other.L_S0.RBC}}; current answers without search ({{v:descriptives.8_near_floor_other.C_S0.answers}}) named them {{v:descriptives.8_near_floor_other.C_S0.USAA}}, {{v:descriptives.8_near_floor_other.C_S0.Synchrony}}, {{v:descriptives.8_near_floor_other.C_S0.Santander}}, {{v:descriptives.8_near_floor_other.C_S0.Zions}}, {{v:descriptives.8_near_floor_other.C_S0.Western Alliance}} and {{v:descriptives.8_near_floor_other.C_S0.RBC}} times, and with search ({{v:descriptives.8_near_floor_other.C_S1.answers}}) {{v:descriptives.8_near_floor_other.C_S1.USAA}}, {{v:descriptives.8_near_floor_other.C_S1.Synchrony}}, {{v:descriptives.8_near_floor_other.C_S1.Santander}}, {{v:descriptives.8_near_floor_other.C_S1.Zions}}, {{v:descriptives.8_near_floor_other.C_S1.Western Alliance}} and {{v:descriptives.8_near_floor_other.C_S1.RBC}} times.

*Extra Gemini 2.5 Flash pass.* At the provider's default thinking, {{v:descriptives.5_M5X_vs_M5.M5X.truncated}} of {{v:descriptives.5_M5X_vs_M5.M5X.calls}} answers ended at the output cap and {{v:descriptives.10_length_flags.M5X|S0.thinking_ge_half}} spent half the cap or more on thinking; none was cut before naming a brand. Its {{v:descriptives.5_M5X_vs_M5.M5X.calls}} answers carried {{v:descriptives.5_M5X_vs_M5.M5X.ghost_mentions}} ghost mentions, against {{v:descriptives.5_M5X_vs_M5.M5.ghost_mentions}} in the {{v:descriptives.5_M5X_vs_M5.M5.calls}} answers of Gemini 2.5 Flash at thinking budget 0.

*First mention.* Among bank recommendation answers naming a current unit, the JPMorgan Chase holder was named first in {{v:descriptives.9_first_mention_share.M1|S0|bank.share.1039502}} (Claude Opus 4.5), {{v:descriptives.9_first_mention_share.M2|S0|bank.share.1039502}} (Claude Sonnet 4.5), {{v:descriptives.9_first_mention_share.M3|S0|bank.share.1039502}} (GPT-4o), {{v:descriptives.9_first_mention_share.M4|S0|bank.share.1039502}} (GPT-4o mini), {{v:descriptives.9_first_mention_share.M5|S0|bank.share.1039502}} (Gemini 2.5 Flash), {{v:descriptives.9_first_mention_share.M6|S0|bank.share.1039502}} (Gemini 2.5 Flash-Lite), {{v:descriptives.9_first_mention_share.C1|S0|bank.share.1039502}} (Claude Fable 5.2), {{v:descriptives.9_first_mention_share.C2|S0|bank.share.1039502}} (GPT-6 Astra) and {{v:descriptives.9_first_mention_share.C3|S0|bank.share.1039502}} (Gemini 4 Argon) of answers, search off; with search on the current models' shares were {{v:descriptives.9_first_mention_share.C1|S1|bank.share.1039502}}, {{v:descriptives.9_first_mention_share.C2|S1|bank.share.1039502}} and {{v:descriptives.9_first_mention_share.C3|S1|bank.share.1039502}}.

*Not in the scored record.* Several pre-registered reporting items are not in the scorer's verdict file and are not reported here: descriptives 1 and 2 (the AI share of each current unit and the ghost Presence of each ghost, per model and arm); the per-ghost and per-model results promised beside each test (pre-registration §8, item 6); the H_Amplify log-log slope without the brokerage holders (§2.3); and the Discover status answers in full (§3.2). The coded mentions from which they follow are in the study data (`v40_mentions.csv`). Whether they are computed after scoring and labelled as such, or recorded as a deviation, is open. The recognition codes (descriptive 4) and the search traces (descriptive 7) are in the verdict file in full.

# 4. Discussion

The models' naming of current brands followed market share in both categories, which is in line with the Tri-System framework's P1 (MSI Working Paper 26-132) in its ordinal form; in airlines this rests on the legacy models and on how one small unit is placed (below). Whether AI amplifies the leader could not be decided by this measure: the registered ratio divides answers by unit-namings, and at the breadth the models' answers showed it could not reach the amplification threshold (§3.4). The bank leader was named in most bank answers and first in a majority of them for every legacy model (§3.10). A test of leader amplification needs a measure built per answer, such as the share of answers naming the leader against its market share, or rank within the answer.

Second, status answers about ghosts carried a gone-flag in nearly every case, and with web search on the current models flagged the few exits that came after their cutoff, a small count from two brands with no search-off comparison. Whether ghosts still surface in recommendations without such a flag was not settled: the rates sat between the registered null and pass lines, and the audit suggests the rule-based coder overstates them. Ghost Presence was lower at longer exit-to-cutoff gaps, as expected if a brand's footprint in training text fades after it leaves the market, but the association was weaker than the registered band and rested on few named pairs; the design shows an association, not its cause.

The airline reinforcement result should be read with its sensitivity. With ten units, moving Sun Country into Allegiant changes the airline correlation from passing to failing, and the current models alone did not pass. The banks, with twenty-five units, held in every specification.

# 5. Limitations

1. *One market, one language, two categories, three days.* US airlines and US retail banks, asked in English, without a buyer persona, collected 17--19 November 2026; answers drift between model versions and days.
2. *Search on is thin.* One search-on run on the recommendation and status probes; each provider decided whether and what to search, and Gemini 4 Argon did not search in about a third of its answers (MC2).
3. *Rule-based coding.* The gone-flag lexicon misses paraphrases and fires on living brands whose answers mention a merger they survived. The audit met its registered threshold overall but not on the recommendation answers alone (κ {{v:audit.agreement.consensus_vs_rule.gone_flag.recommendation.kappa}}).
4. *The audit has no human check.* The analyst named in the pre-registration was replaced by two blind AI coders and an AI tie-breaker (DEVIATIONS Entry 1); one of them, Claude Fable 5.2, is also a model of the study's current arm.
5. *Cutoffs are vendor-published months.* Claude Fable 5.2 takes Claude Opus 5.5's cutoff rows; differences within a month are not resolved.
6. *Pairs are not independent.* Ghost × model pairs share ghosts, and answers share probes and runs; the exact tests treat them as independent, as does the binomial test of H_Amplify, which treats each naming as a draw. The pre-registration promised per-ghost and per-model results beside each test; they are not in the scored record and are not reported here (§3.10).
7. *The bank living-brand control was itself changing.* Discover's deposits were moving to Capital One; H_Flag is also reported without it.
8. *Share measures.* AI share counts answers that name a unit, not rank or prominence; the leader ratio has a ceiling set by the breadth of answers (§3.4); the ambiguity rule removes the bare names of the largest airlines; brokerage-sweep holders enter by the deposit rule; near-floor brands such as USAA are not units.
9. *Pre-registered reporting not in the scored record* (§3.10): descriptives 1 and 2, the per-ghost and per-model results, the log-log slope without the brokerage holders, and the Discover status answers in full.
10. *The locked file's first line still reads DRAFT* (§2.7); the lock rests on the tag, the manifest and the OSF deposit.

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

Materials are deposited at OSF (osf.io/ec6wh), `v40/`: the locked pre-registration, probe set, cost estimate, pre-lock and technical checks and lock manifest (`prereg/`) and the frozen registry with its sources (`registries/`). The answers, coded mentions, verdict file, audit records and values file are in the repository at `osf/v40/` and are planned for OSF with the study's data deposit. The pre-registered code is in the programme's GitHub repository (github.com/thirdsystem-aias/aias) at tag `v0.40-prereg-r1`; the scripts that fill this paper and draw its figures are on the branch `v0.40-paper`. Every number in this paper is read from `osf/v40/v40_values.json`, which names the source file and path of each value.

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

Jack, Lehman, Maloney & Xu (2026). arXiv 2605.30207, May 2026 (as cited in the v0.40 pre-registration, §8 item 10; title not verified).

Li, P., Castelo, N., Katona, Z., & Sarvary, M. (2024). Frontiers: Determining the validity of large language models for automated perceptual analysis. *Marketing Science*, 43(2), 254--266.

Rienecker et al. (2026). Auditing preferences for brands and cultures in LLMs (ChoiceEval). arXiv 2603.18300.

Romaniuk, J., & Sharp, B. (2016). *How Brands Grow: Part 2*. Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

Shaw, S., & Nave, G. (2026). *Thinking---Fast, Slow, and Artificial: How AI is Reshaping Human Reasoning and the Rise of Cognitive Surrender*. SSRN 6097646.

Varadarajan, R., DeFanti, M. P., & Busch, P. S. (2006). Brand portfolio, corporate image, and reputation: Managing brand deletions. *Journal of the Academy of Marketing Science*, 34(2), 195--205.
