---
title: "Does AI Brand Presence Hold Across Languages?"
subtitle: "Spanish, Korean and Chinese against the English t4 Wave: A Pre-Registered Non-English Wave (AIAS™ v0.62)"
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
  \usepackage{fancyhdr}
  \pagestyle{fancy}
  \fancyhf{}
  \fancyfoot[C]{\thepage}
  \renewcommand{\headrulewidth}{0pt}
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

{\LARGE \textbf{Does AI Brand Presence Hold Across Languages?}\par}\vspace{8pt}

{\large Spanish, Korean and Chinese against the English t₄ Wave:\\ A Pre-Registered Non-English Wave (AIAS™ v0.62)}\\[28pt]

Pablo Ulpiano González Castro\\[4pt]
School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System™ (research entity; data archive and methodology venue)\\[8pt]
Correspondence: pablou@pablou.com · pablou.com\\
ORCID: \href{https://orcid.org/0009-0003-8968-9990}{0009-0003-8968-9990}\\[20pt]

Pre-registration: \texttt{v0.62-prereg-r1} (commit \texttt{e449b6c})\\
locked on 12 November 2026 and deposited on OSF before the first study call\\[4pt]
Data and code: OSF \texttt{ec6wh}, \texttt{v62}\\[4pt]
November 2026 (r2)

\end{center}
\end{titlepage}

# Abstract {-}

Every AI Availability measurement of the AIAS programme so far was taken in US English. This pre-registered wave asks whether AI brand Presence holds when the same questions are asked in other languages. The 30 open category questions of the English t₄ wave (five consumer categories, {{v:design.n_units}} brand units) were translated into Spanish, Korean and Simplified Chinese and asked of the same three models (Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon), without web search, three times each; 88 yes/no brand questions per language were collected last. All {{v:raw.ok}} of {{v:design.expected}} planned calls were answered ({{v:raw.per_lang}} per language and {{v:raw.per_model}} per model), one of them in the logged re-run pass after a connection timeout, for {{v:cost.spend}} of recorded spend against a $100 cap. Recall Presence ordered the brands as it does in English in all three languages: centred within-category Spearman ρ_c = {{v:P.es.rho}} in Spanish (95% CI {{v:P.es.ci}}), {{v:P.ko.rho}} in Korean ({{v:P.ko.ci}}) and {{v:P.zh.rho}} in Chinese ({{v:P.zh.ci}}), permutation p {{v:P.es.p}} in each; H_Lang_Presence is {{v:P.es.verdict}} in each language, and the pre-registered joint reading is {{v:joint}}. Spanish answers named the registry brands slightly more often than English answers (mean difference in Presence {{v:P.es.dL}}), Korean ({{v:P.ko.dL}}) and Chinese ({{v:P.zh.dL}}) answers less often. Consistency (φ) ordered the brands alike in Spanish (ρ_c = {{v:Phi.es.rho}}; H_Lang_Phi {{v:Phi.es.verdict}}) but only weakly in Korean ({{v:Phi.ko.rho}}) and Chinese ({{v:Phi.zh.rho}}), both {{v:Phi.ko.verdict}}. Ranking was {{v:Rank.es.verdict}}, because its instrument has not passed its own test. No verdict changed under any sensitivity: without Denon, without the headphones category, without the units with a disclosed conflict-of-interest tie (on {{v:COI.n_as_run}} units as run and on {{v:COI.n_106}} units after a key mismatch was corrected), without translation-flagged questions, without an alias that an independent AI check judged unused, or with a corrected English comparator, under which Chinese Consistency agreement falls to {{v:ENC.Phi.zh.rho4}} and stays {{v:ENC.Phi.zh.verdict}}. The pre-registered checks, secondary analyses and descriptives that the locked scorer did not compute were computed afterwards from the archived data, with no model called, and change no verdict (DEVIATIONS Entry 7; Appendix A). The translations were model-made and checked by independent AI models only, without native review. DEVIATIONS Entries 0--8 are recorded and reported.

**Keywords:** AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; large language models; multilingual; cross-language measurement; Spanish; Korean; Chinese; measurement invariance

**JEL codes:** M31; L86, L15, D83, M37

**Paper status:** r2 (25 November 2026). Pre-registered confirmatory study (tag `v0.62-prereg-r1`, locked on 12 November 2026 and deposited on OSF before the first study call); collected on 25 November 2026; scored once (`score_v0_62.py`, commit `262464d`); post-scoring sensitivities in commit `4ac1aa9`; post-scoring computation of the remaining pre-registered items and the cost record in commit `69e1aa9`; deviations recorded in `osf/v62/DEVIATIONS.md`, Entries 0--{{v:dev.last}} (§4). Part of the AIAS measurement programme.

# 1. Introduction

AI Availability, the discoverability and representation of a brand in the answers of large language models (LLMs), has been proposed as a third measurable layer of brand availability (González Castro, 2026a), beside the Mental and Physical Availability of the Ehrenberg-Bass tradition (Sharp, 2010; Romaniuk & Sharp, 2016), within the Tri-System framework of brand growth (González Castro, 2026l). It is measured under a versioned protocol (Methodology v1.2--v1.6, González Castro, 2026b--f; AIAS 1.0, 2026j), and the programme reports two components (AIAS 2.0, 2026k): Presence, the share of a category's open questions in which a model names a brand, and Consistency, how evenly the models of a panel name it, scored by a dispersion statistic φ that does not depend on Presence by construction (v1.8, 2026h; after a coefficient-of-variation measure failed that test, v1.7, 2026g).

Every one of those measurements was taken in US English. A brand's AI availability describes what a model makes available to a person who asks, and people ask in many languages; a model's knowledge of brands need not be the same in each. If the scores depend on the language of the question, an English-only measure describes English-speaking users only.

The English t₄ wave (v0.42) measured the five consumer categories of the programme's omnibus (audiophile headphones, skincare, cosmetics, cars and premium spirits; v0.19--v0.23, 112 brand units) on the newest flagship model of three providers. This wave asks the same category questions, translated, of the same models with the same settings, and tests whether the brand orderings reproduce. It asks three questions, fixed before data (§2.4): does recall Presence order brands in Spanish, in Korean and in Chinese as it does in English (H_Lang_Presence, primary); does Consistency order them alike (H_Lang_Phi); and, if the Ranking instrument had passed its own test, does Ranking (H_Lang_Rank)? The three languages come from three scripts (Latin, Hangul, Han) and three language families. Language is varied alone: no country, market or location is stated in any question, and no system prompt is sent. Under the programme's independence rule for public studies there is no focal brand, no finding is addressed to a brand, and no brand was contacted.

# 2. Method

## 2.1 Units and comparator

The units are the 112 brands of the five omnibus registries, unchanged (16 headphone brands and 24 in each other category), exactly as the English t₄ wave measured them. The comparator values are t₄'s locked English values on the same models without search (condition S0): recall Presence π̂ and Consistency φ with its partition, from v0.42's scored brand table (`v42_brand_table.csv`, pre-registration §2.1 and §7.3). An erratum to that table was published on 25 November 2026, after this wave's scoring; its effect is reported as a sensitivity (§3.7, DEVIATIONS Entry 6).

## 2.2 Translation, questions and coding

The 30 English category questions (six per category), the five yes/no templates and the 15 spirits category labels were translated by a model (Claude Opus 5.5) into neutral Latin American Spanish, standard South Korean and Simplified Chinese (Mainland usage), under a fixed checklist: the category noun covers the same set of brands as the US English one (for example, every cosmetics item uses the word for colour cosmetics, because the general word in all three languages includes skincare), "list several" and "name several" are kept distinct, and nothing is added or removed (pre-registration §3). Brand names are written in Latin script in all three languages. The planned native checks did not take place; they were replaced, before any study call, by an independent check by models of two other providers (DEVIATIONS Entry 2; §3.8).

Answers are prepared by a language pre-step before the English matchers certified for t₄ run on them: Unicode normalisation (full-width Latin letters to ordinary forms, typographic apostrophes to '), URL removal, and, for Korean and Chinese, replacement of each listed Hangul or Han alias by the registry name (120 Korean aliases over 111 units; 80 Chinese aliases over 74 units), with rules for Korean particles and word joints (pre-registration §4). An alias may not be looser than the English matcher, which counts only the full registry string. Collision-prone aliases (for example the Korean and Chinese words that are also common words or other names) are counted and every match is exported for audit.

## 2.3 Panel, design and collection

The panel is t₄'s: Claude Fable 5.2 (`claude-fable-5-2`, through Anthropic's Message Batches API), GPT-6 Astra (`gpt-6-astra`) and Gemini 4 Argon (`gemini-4-argon`), without tools or web search, at provider-default sampling and reasoning settings, with a cap of 16,384 output tokens and no language, locale or region parameter. Each model answered the 30 category questions in each language three times (blocks 1--3: 3 × 3 × 30 × 3 = {{v:raw.B}} calls) and then, last, the 88 yes/no brand questions of v0.19--v0.22 in each language once (block 4: {{v:raw.A}} calls), for {{v:design.expected}} calls. The 24 open spirits brand questions were not collected (pre-registration §9 item 7 (b)). Every confirmatory test uses blocks 1--3 only; block 4 feeds a descriptive. Transient errors were retried, an empty answer was re-sent once, and one logged re-run pass was allowed.

The budget was at most $100 of paid calls with a pause at $80, both from recorded usage, and a projection pause after block 1; the pre-registered central estimate was $34.52 (November prices) and the conservative high $124.77 (pre-registration §6.3). The collection window, moved before any call to 25 November--2 December 2026 (DEVIATIONS Entry 3), required every call within 72 hours of the first; the acquisition script refused to send outside the window, without the lock tag on the remote and its OSF anchor, or while another paid collection ran on the machine.

## 2.4 Measures, statistics and hypotheses

**Measures.** For brand b, model m, run r and language L, k is the number of the six category questions of b's category whose answer names b. Recall Presence is π̂ = Σ k ÷ (6 · 3 · 3), as t₄ defines it. Consistency φ is t₄'s: the v1.8 quasi-binomial dispersion of the three models' counts per run, averaged over the runs in which it is defined, undefined if fewer than two of three runs are defined; higher φ means less consistent naming.

**Statistics.** ρ_c is the centred pooled within-category Spearman correlation: values ranked within category, each category's ranks centred, and Pearson's r of the centred ranks pooled. Permutation p-values are one-sided (10,000 within-category permutations); intervals are percentile bootstrap intervals (10,000 within-category resamples). Seeds are fixed per test (620101--620103 for H_Lang_Presence, 620111--620113 for H_Lang_Phi). α = 0.05 per test, without multiplicity correction; verdicts rest on the pre-set thresholds and every test is reported. The uncentred statistic of earlier waves is reported beside ρ_c for comparability (S-Uncentred); no verdict reads it.

**H_Lang_Presence (primary, §2.2).** "Asked in language L, the newest models order brands by recall Presence as they do in English." x = English π̂, y = π̂ in L, all 112 units, one test per language. CONFIRMED if ρ_c ≥ 0.70 and p < 0.05; FALSIFIED if ρ_c < 0.50; MARGINAL otherwise. Reported alongside: per-category ρ_c and the level shift Δ_L = mean(π̂ in L − English π̂) with its bootstrap interval.

**H_Lang_Phi (secondary, §2.3).** x = English φ, y = φ in L, over the units with φ defined in both. UNDETERMINED if n < 40; CONFIRMED if ρ_c ≥ 0.50 and p < 0.05; FALSIFIED if ρ_c < 0.30; MARGINAL otherwise.

**H_Lang_Rank (secondary, conditional, §2.4).** Tested only if the Ranking instrument v1.14 resolved PASS before scoring; otherwise NOT TESTED.

**Joint reading (§2.6).** Language-robust if H_Lang_Presence is CONFIRMED in all three languages; language-dependent if it is FALSIFIED in any; partly robust otherwise. H_Lang_Phi and H_Lang_Rank do not change it.

**Sensitivities (§7.5; DEVIATIONS Entries 2, 4--7).** Reported beside the tests and never changing a verdict: S-Denon (111 units, without the one headphone brand owned by a group disclosed in the Declarations); S-Headphones (96 units, without the headphones category); S-COI (without the six units with a tie disclosed in the Declarations, 106 units; §3.7 and Entry 4); S-Trans (without translation-flagged questions, Entry 2); S-AliasAI (without aliases the AI check judged unused, Entry 2); and, added after scoring, the corrected English comparator (Entry 6). The three further Presence sensitivities of §7.5, which the locked scorer does not compute, were computed after scoring under Entry 7: S-Language (without category answers the pre-step marks as not in the asked language), S-Script (Chinese, without answers containing a Traditional-only character) and S-Alias (Korean and Chinese re-coded with the 13 collision-prone aliases switched off). If a primary verdict differed under S-Denon, S-Headphones, S-COI, S-Trans or S-AliasAI, the abstract would report both.

## 2.5 Lock and gates

The pre-registration (r3) was locked as tag `v0.62-prereg-r1` on commit `e449b6c` on 12 November 2026 and anchored on OSF (`ec6wh/v62`) the same day, with its scripts, probe files, alias table, cost estimate, deviations record and a 73-file lock manifest. Before any statistic, four gates had to pass (§7.3): P1, the transcribed π̂ and φ kernels reproduce t₄'s locked kernels and scored table; P2, the language pre-step changes nothing on English text; P3, the probe files equal the locked ones and every sent prompt equals its probe; P4, every Korean and Chinese alias reaches its unit and no decoy matches (unit tests before the lock). The statistics were computed once, by `score_v0_62.py`, on 25 November 2026, after gates P1--P3 had passed on the collected data.

# 3. Results

## 3.1 Collection

The collection ran on 25 November 2026. The first call started at {{v:win.first_ct}} US Central ({{v:win.first_utc}} UTC). The main pass ended at {{v:log.main_end_ct}} with {{v:log.main_spend}} recorded and all calls answered but one: the Korean answer of {{v:err.model}} to the headphones question {{v:err.probe}} in run {{v:err.run}} ended at {{v:err.time_ct}} with a {{v:err.kind}} error, before any answer or usage was recorded. Recorded spend before blocks 2, 3 and 4 was {{v:log.before_block2}}, {{v:log.before_block3}} and {{v:log.before_block4}}; block 1 thus cost less than the $25.83 at which the projection pause would have stopped the collection, and neither the $80 pause nor the $100 stop was reached. The logged re-run pass of §5.3 ran from {{v:log.rerun_start_s}} to {{v:log.rerun_end_s}} US Central and answered the one call for {{v:err.rerun_cost}} (DEVIATIONS Entry 8). The last call ended at {{v:win.last_ct}}, {{v:win.span_h}} hours after the first, inside the window ({{v:budget.window}}, DEVIATIONS Entry {{v:budget.window_entry}}) and the 72-hour rule. The raw file holds {{v:raw.lines}} lines: the {{v:raw.ok}} answered calls ({{v:raw.per_lang}} per language, {{v:raw.per_model}} per model) and the one error. Recorded spend was {{v:cost.spend}}.

**Cost note (DEVIATIONS Entry 8).** The guard charged the timed-out attempt {{v:err.cost}}: its raw line records no usage ({{v:err.usage_parts}} usage parts). Pre-registration §6.5 rule 2 states that every attempt of a synchronous call that returned no usage is costed at the request's worst case (2,000 input and 16,384 output tokens). The locked code turns only Google's server errors and rate-limit responses into a transient error, so the connection timeout was recorded as a final non-transient error, not retried within the call, and counted as not billed. (A GPT-6 Astra call that started ten seconds later also lost its first attempt; the OpenAI path classes that failure as transient, so it was retried and answered, and its failed attempt was charged at the worst case, {{v:cost.astra_wc}}, as rule 2 requires; that charge is in the recorded spend.) Under strict rule 2, at Gemini 4 Argon's price on the date of the request ({{v:cost.wc_price}} per million input and output tokens), the timed-out attempt costs {{v:cost.worst_case}}: the main pass would have recorded {{v:cost.main_strict}} instead of {{v:cost.main_recorded}}, and the total is {{v:cost.strict_total}} against {{v:raw.cost_sum6}} recorded. This paper reports {{v:cost.spend}} from recorded usage, with {{v:cost.strict_total4}} under strict rule 2 beside it. No guard decision would have differed: while the call was in flight its reservation of two worst cases was held, the projection stayed below the pause either way, and the $80 pause and $100 stop were never near. The re-run pass ran under the pre-registrant's projection approval of {{v:budget.rerun_note_given}} US Central, recorded in `v62_budget_state.json` when the pass started. Entry 8 records that, read against the locked collection rule, the projection pause applies only while calls of later blocks remain unsent; none did, so the re-run pass would not have paused without the approval either. The independent translation and alias check (§3.8) was paid outside the acquisition guard under its own $8 cap and cost {{v:AIC.spend}} in {{v:AIC.requests}} requests; acquisition and check together cost {{v:cost.with_check}}.

## 3.2 Gates and manipulation checks

All four gates passed (Table 1). The pre-step was inert on English: on t₄'s English answers, coding with the full pre-step and with its normalisation step alone gave the same {{v:gate.P2.cells}} cells. The apostrophe mapping itself changed {{v:gate.P2.apos_diff}} cells and added {{v:gate.P2.apos_only2}} relative to t₄'s locked codes (Paula's Choice, L'Oréal Paris and the spirits registry ids); as pre-registered, P2 reported this delta and did not correct the English comparator. That correction is the subject of DEVIATIONS Entry 6 (§3.7).

| Gate or check | Result | Status |
|---|---|---|
| P1 kernel parity | transcribed kernels against t₄'s locked kernels on t₄'s coded tables: {{v:gate.P1.mismatches}} mismatches over {{v:gate.P1.units}} units; {{v:gate.P1.table_diffs}} differences from t₄'s scored table | {{v:gate.P1.result}} |
| P2 pre-step inert on English | {{v:gate.P2.diff}} differing cells of {{v:gate.P2.cells}} | {{v:gate.P2.result}} |
| P3 probe parity | probe files equal the lock manifest; {{v:gate.P3.mismatches}} prompt mismatches in {{v:gate.P3.checked}} raw lines | {{v:gate.P3.result}} |
| P4 alias reach | unit tests before the lock (pre-registration §7.3) | passed before the lock |
| MC_Complete | {{v:raw.ok}} of {{v:design.expected}} calls answered; every model, language and phase complete | met |
| MC_Window | {{v:win.first_ct}} to {{v:win.last_ct}} US Central on 25 November ({{v:win.span_h}} h), inside {{v:budget.window}} | met |
| MC_Budget | {{v:cost.spend}} recorded against the $100 cap; no pause or stop; 0 calls not sent | met |
| MC_Alias | {{v:alias.matches}} collision-prone alias matches in {{v:E7.mc.alias.calls}} calls exported for audit (`data/coded/v62_alias_audit.csv`) | reported (no verdict) |
| MC_Served | {{v:E7.mc.served.mismatched}} served-model mismatches in {{v:E7.mc.served.checked}} answered calls | {{v:E7.mc.served.pass}} |
| MC_Language | category answers: every model-language cell at or above 95% (lowest {{v:E7.mc.lang.zh.claude-fable-5-2.B}}, Chinese, Claude Fable 5.2); all answers: the {{v:E7.mc.lang.n_flagged_all}} Spanish cells below 95%, because the fixed rule does not count a short yes/no answer such as "Sí." as Spanish (Appendix A.3) | flagged (Spanish, all answers); no code changed |
| MC_Script | {{v:E7.mc.script.n}} Chinese answers with a Traditional-only character | not flagged |
| MC_Truncation | {{v:E7.mc.trunc.n}} calls at the output cap | not flagged |

: Gates and pre-registered manipulation checks (`data/gates/`, `data/v62_raw.jsonl`, the collection logs). MC_Complete, MC_Window and MC_Budget are read from the raw file and logs; MC_Served, MC_Language, MC_Script, MC_Truncation and the call count of MC_Alias were computed after scoring under DEVIATIONS Entry 7 (`data/v62_planned_items_v0_62.json`), since the locked scorer writes no manipulation-check record. Under §2.8 none of these checks changes a code or a verdict.

## 3.3 H_Lang_Presence: brands keep their Presence order in all three languages ({{v:P.es.verdict}} in each)

Recall Presence ordered the 112 brands in each language much as it does in English (Table 2, Figure 1). In Spanish ρ_c = {{v:P.es.rho}} (95% CI {{v:P.es.ci}}), in Korean {{v:P.ko.rho}} ({{v:P.ko.ci}}) and in Chinese {{v:P.zh.rho}} ({{v:P.zh.ci}}); the one-sided permutation p was {{v:P.es.p}} in each, the smallest value 10,000 draws allow. Every estimate is above the 0.70 threshold, and so is the lower bound of every interval except Chinese ({{v:P.zh.ci}}), whose interval reaches below 0.70 but stays above the 0.50 falsification line. H_Lang_Presence is **{{v:P.es.verdict}}** in Spanish, **{{v:P.ko.verdict}}** in Korean and **{{v:P.zh.verdict}}** in Chinese, and the pre-registered joint reading is **{{v:joint}}**.

| Category | Spanish | Korean | Chinese |
|---|---:|---:|---:|
| Audiophile headphones (v0.19, 16 units) | {{v:P.es.cat.v0.19}} | {{v:P.ko.cat.v0.19}} | {{v:P.zh.cat.v0.19}} |
| Skincare (v0.20, 24) | {{v:P.es.cat.v0.20}} | {{v:P.ko.cat.v0.20}} | {{v:P.zh.cat.v0.20}} |
| Cosmetics (v0.21, 24) | {{v:P.es.cat.v0.21}} | {{v:P.ko.cat.v0.21}} | {{v:P.zh.cat.v0.21}} |
| Automotive (v0.22, 24) | {{v:P.es.cat.v0.22}} | {{v:P.ko.cat.v0.22}} | {{v:P.zh.cat.v0.22}} |
| Premium spirits (v0.23, 24) | {{v:P.es.cat.v0.23}} | {{v:P.ko.cat.v0.23}} | {{v:P.zh.cat.v0.23}} |
| **Pooled ρ_c (112)** | **{{v:P.es.rho}}** | **{{v:P.ko.rho}}** | **{{v:P.zh.rho}}** |
| 95% CI | {{v:P.es.ci}} | {{v:P.ko.ci}} | {{v:P.zh.ci}} |
| Uncentred (comparability) | {{v:P.es.unc}} | {{v:P.ko.unc}} | {{v:P.zh.unc}} |
| Verdict | {{v:P.es.verdict}} | {{v:P.ko.verdict}} | {{v:P.zh.verdict}} |

: H_Lang_Presence per language and its per-category ρ_c (reported alongside; `v62_verdicts.json`, `tests.H_Lang_Presence_<language>`).

![Rank agreement of recall Presence with English per language, with the per-category values.](../../reports/figs/v62/paper/fig_01_presence.pdf){#fig:presence width=100%}

Per category (descriptive), {{v:P.cat_n70}} of the 15 category-language values were at or above 0.70; they ranged from {{v:P.cat_min}} (skincare in Chinese) to {{v:P.cat_max}} (automotive in Korean). The two lowest values are skincare in Chinese ({{v:P.zh.cat.v0.20}}) and cosmetics in Korean ({{v:P.ko.cat.v0.21}}).

## 3.4 Level: Spanish answers name the registry brands a little more often, Korean and Chinese answers less often (reported alongside)

The order held, but the level moved (Figure 2). The mean difference in π̂ between the language and English, over the 112 units, was {{v:P.es.dL}} in Spanish (95% CI {{v:P.es.dL_ci}}), {{v:P.ko.dL}} in Korean ({{v:P.ko.dL_ci}}) and {{v:P.zh.dL}} in Chinese ({{v:P.zh.dL_ci}}). π̂ is a share of the 54 model-run-question cells of a brand's category, so these shifts amount to a few of the 54 cells per brand on average. No interval contains zero. Under the corrected English comparator the shifts are {{v:ENC.P.es.dL}}, {{v:ENC.P.ko.dL}} and {{v:ENC.P.zh.dL}}. By the descriptive labels of pre-registration §2.5, applied to the pooled values, every language reads as "level-shifted" (ρ_c ≥ 0.70 and an interval of Δ_L that excludes zero) rather than "language-stable". Per category (computed after scoring under DEVIATIONS Entry 7; Appendix A.2, Table A2), {{v:E7.cat.n.level-shifted}} of the 15 category-language cells read as level-shifted, {{v:E7.cat.n.language-stable}} as language-stable, {{v:E7.cat.n.intermediate}} as intermediate (skincare in Chinese) and {{v:E7.cat.n.language-sensitive}} as language-sensitive.

![Mean difference in recall Presence from English per language, under the locked and the corrected English comparator.](../../reports/figs/v62/paper/fig_02_level.pdf){#fig:level width=100%}

## 3.5 H_Lang_Phi: Consistency carries over in Spanish, only weakly in Korean and Chinese (ES {{v:Phi.es.verdict}}; KO, ZH {{v:Phi.ko.verdict}})

How evenly the three models named a brand carried over to Spanish but much less to Korean and Chinese (Table 3, Figure 3). Over the units with φ defined in both languages, ρ_c was {{v:Phi.es.rho}} in Spanish (n = {{v:Phi.es.n}}; 95% CI {{v:Phi.es.ci}}; p {{v:Phi.es.p}}), {{v:Phi.ko.rho}} in Korean (n = {{v:Phi.ko.n}}; {{v:Phi.ko.ci}}; p = {{v:Phi.ko.p}}) and {{v:Phi.zh.rho}} in Chinese (n = {{v:Phi.zh.n}}; {{v:Phi.zh.ci}}; p = {{v:Phi.zh.p}}). H_Lang_Phi is **{{v:Phi.es.verdict}}** in Spanish and **{{v:Phi.ko.verdict}}** in Korean and in Chinese ({{v:Phi.zh.verdict}}): both are significant and above the 0.30 falsification line, below the 0.50 confirmation threshold, and both intervals span the marginal band. Per category the Korean and Chinese values varied widely, from {{v:Phi.cat_min}} (skincare in Chinese) upward; {{v:Phi.cat_nneg}} of the 15 category-language values were negative. The pre-registered flag for φ tracking Presence within a language (|ρ_c(φ, π̂)| of 0.50 or more, §2.3), computed after scoring under DEVIATIONS Entry 7, is not raised in any language: the largest absolute value was {{v:E7.phipi.max_abs}} (Chinese; Appendix A.1).

| | Spanish | Korean | Chinese |
|---|---:|---:|---:|
| n (φ defined in both) | {{v:Phi.es.n}} | {{v:Phi.ko.n}} | {{v:Phi.zh.n}} |
| ρ_c | **{{v:Phi.es.rho}}** | **{{v:Phi.ko.rho}}** | **{{v:Phi.zh.rho}}** |
| 95% CI | {{v:Phi.es.ci}} | {{v:Phi.ko.ci}} | {{v:Phi.zh.ci}} |
| p (permutation) | {{v:Phi.es.p}} | {{v:Phi.ko.p}} | {{v:Phi.zh.p}} |
| Uncentred (comparability) | {{v:Phi.es.unc}} | {{v:Phi.ko.unc}} | {{v:Phi.zh.unc}} |
| Units: φ defined / zero / saturated / undefined (language side) | {{v:Phi.es.part.defined}} / {{v:Phi.es.part.zero}} / {{v:Phi.es.part.saturated}} / {{v:Phi.es.part.undefined}} | {{v:Phi.ko.part.defined}} / {{v:Phi.ko.part.zero}} / {{v:Phi.ko.part.saturated}} / {{v:Phi.ko.part.undefined}} | {{v:Phi.zh.part.defined}} / {{v:Phi.zh.part.zero}} / {{v:Phi.zh.part.saturated}} / {{v:Phi.zh.part.undefined}} |
| Headphones (v0.19) | {{v:Phi.es.cat.v0.19}} | {{v:Phi.ko.cat.v0.19}} | {{v:Phi.zh.cat.v0.19}} |
| Skincare (v0.20) | {{v:Phi.es.cat.v0.20}} | {{v:Phi.ko.cat.v0.20}} | {{v:Phi.zh.cat.v0.20}} |
| Cosmetics (v0.21) | {{v:Phi.es.cat.v0.21}} | {{v:Phi.ko.cat.v0.21}} | {{v:Phi.zh.cat.v0.21}} |
| Automotive (v0.22) | {{v:Phi.es.cat.v0.22}} | {{v:Phi.ko.cat.v0.22}} | {{v:Phi.zh.cat.v0.22}} |
| Premium spirits (v0.23) | {{v:Phi.es.cat.v0.23}} | {{v:Phi.ko.cat.v0.23}} | {{v:Phi.zh.cat.v0.23}} |
| Verdict | {{v:Phi.es.verdict}} | {{v:Phi.ko.verdict}} | {{v:Phi.zh.verdict}} |

: H_Lang_Phi per language, with the language-side partition of φ over the 112 units and the per-category ρ_c (reported alongside; `tests.H_Lang_Phi_<language>`).

![Rank agreement of Consistency with English per language, under the locked and the corrected English comparator.](../../reports/figs/v62/paper/fig_03_phi.pdf){#fig:phi width=100%}

## 3.6 H_Lang_Rank: not tested

H_Lang_Rank was to be tested only if the Ranking instrument (Methodology v1.14) had resolved PASS before v0.62 was scored. It had not: the scorer records "{{v:Rank.reason}}". H_Lang_Rank is **{{v:Rank.es.verdict}}** in Spanish, **{{v:Rank.ko.verdict}}** in Korean and **{{v:Rank.zh.verdict}}** in Chinese. No Ranking statistic was computed.

## 3.7 Sensitivities: no specification changes a verdict

Every pre-registered and added sensitivity left every verdict as scored (Table 4, Figure 4). Without Denon (S-Denon, 111 units), without the headphones category (S-Headphones, 96 units), without the units with a disclosed tie (S-COI), without translation-flagged questions (S-Trans), without the alias the AI check judged unused (S-AliasAI) and with the corrected English comparator, H_Lang_Presence stayed CONFIRMED in every language, and the joint reading stayed {{v:joint}}. None of the abstract rules of §7.5 and Entry 2 (b)--(c) was triggered. The three §7.5 sensitivities computed after scoring under Entry 7 also give the primary verdict in every language: S-Language excludes no Spanish or Korean category answer and {{v:E7.S-Language.zh.excluded}} Chinese answers (Claude Fable 5.2, spirits question {{v:E7.mc.lang.zh_off_probe}}, runs 1--3); S-Script excludes no answer; S-Alias changes {{v:E7.S-Alias.ko.cells}} coded Korean cell and {{v:E7.S-Alias.zh.cells}} Chinese cells (Spanish has no alias, so its line is the primary one). §7.5's abstract rule does not cover these three.

| Specification | n | Spanish | Korean | Chinese |
|---|---:|---|---|---|
| Primary | {{v:P.es.n}} | {{v:P.es.rho}} ({{v:P.es.ci}}) | {{v:P.ko.rho}} ({{v:P.ko.ci}}) | {{v:P.zh.rho}} ({{v:P.zh.ci}}) |
| S-Denon | {{v:S-Denon.es.n}} | {{v:S-Denon.es.rho}} ({{v:S-Denon.es.ci}}) | {{v:S-Denon.ko.rho}} ({{v:S-Denon.ko.ci}}) | {{v:S-Denon.zh.rho}} ({{v:S-Denon.zh.ci}}) |
| S-Headphones | {{v:S-Headphones.es.n}} | {{v:S-Headphones.es.rho}} ({{v:S-Headphones.es.ci}}) | {{v:S-Headphones.ko.rho}} ({{v:S-Headphones.ko.ci}}) | {{v:S-Headphones.zh.rho}} ({{v:S-Headphones.zh.ci}}) |
| S-COI as run | {{v:S-COI.es.n}} | {{v:S-COI.es.rho}} ({{v:S-COI.es.ci}}) | {{v:S-COI.ko.rho}} ({{v:S-COI.ko.ci}}) | {{v:S-COI.zh.rho}} ({{v:S-COI.zh.ci}}) |
| S-COI, Entry 4 | {{v:S-COI106.es.n}} | {{v:S-COI106.es.rho}} ({{v:S-COI106.es.ci}}) | {{v:S-COI106.ko.rho}} ({{v:S-COI106.ko.ci}}) | {{v:S-COI106.zh.rho}} ({{v:S-COI106.zh.ci}}) |
| S-Trans (both lines) | {{v:STrans.flagged.P.es.n}} | {{v:STrans.flagged.P.es.rho}} ({{v:STrans.flagged.P.es.ci}}) | {{v:STrans.flagged.P.ko.rho}} ({{v:STrans.flagged.P.ko.ci}}) | {{v:STrans.flagged.P.zh.rho}} ({{v:STrans.flagged.P.zh.ci}}) |
| S-AliasAI | {{v:SAliasAI.ko.n}} | not applicable | {{v:SAliasAI.ko.rho}} ({{v:SAliasAI.ko.ci}}) | {{v:SAliasAI.zh.rho}} ({{v:SAliasAI.zh.ci}}) |
| Corrected comparator | {{v:ENC.P.es.n}} | {{v:ENC.P.es.rho}} ({{v:ENC.P.es.ci}}) | {{v:ENC.P.ko.rho}} ({{v:ENC.P.ko.ci}}) | {{v:ENC.P.zh.rho}} ({{v:ENC.P.zh.ci}}) |
| S-Language, Entry 7 | {{v:E7.S-Language.es.n}} | {{v:E7.S-Language.es.rho}} ({{v:E7.S-Language.es.ci}}) | {{v:E7.S-Language.ko.rho}} ({{v:E7.S-Language.ko.ci}}) | {{v:E7.S-Language.zh.rho}} ({{v:E7.S-Language.zh.ci}}) |
| S-Script, Entry 7 | {{v:E7.S-Script.zh.n}} | not applicable | not applicable | {{v:E7.S-Script.zh.rho}} ({{v:E7.S-Script.zh.ci}}) |
| S-Alias, Entry 7 | {{v:E7.S-Alias.ko.n}} | {{v:E7.S-Alias.es.rho}} ({{v:E7.S-Alias.es.ci}}) | {{v:E7.S-Alias.ko.rho}} ({{v:E7.S-Alias.ko.ci}}) | {{v:E7.S-Alias.zh.rho}} ({{v:E7.S-Alias.zh.ci}}) |

: H_Lang_Presence under each specification: ρ_c (bootstrap 95% CI); permutation p {{v:P.es.p}} and verdict {{v:P.es.verdict}} in every cell (the verdict field of each source record). S-COI, Entry 4: Jack Daniel's removed; S-Trans: the flagged and the strictly flagged line are identical; corrected comparator: DEVIATIONS Entry 6; S-Language, S-Script and S-Alias: computed after scoring under DEVIATIONS Entry 7 (S-Alias in Spanish is the primary line, as Spanish has no alias). Sources: `v62_verdicts.json` (`sensitivities`), `data/v62_sens_coi106_v0_62.json`, `data/v62_sens_ai_check_v0_62.json`, `data/v62_sens_en_corrected_v0_62.json` and `data/v62_planned_items_v0_62.json`.

![Rank agreement of recall Presence with English under each specification, by language.](../../reports/figs/v62/paper/fig_04_sensitivity.pdf){#fig:sensitivity width=100%}

**S-COI as run and on 106 units (DEVIATIONS Entry 4).** S-COI was defined as the primary test without the {{v:COI.n_flagged}} units with a tie disclosed in the Declarations (106 units). The locked parameter named the spirits unit Jack Daniel's by its brand name, while the English table and the coded tables key spirits units by registry id ({{v:COI.left_in_id}}); the locked code therefore did not find it, and the as-run S-COI has n = {{v:COI.n_as_run}} in every language. The unit tests used synthetic brand names and did not catch the mismatch. Both lines are reported as scored. With Jack Daniel's removed, ρ_c was {{v:S-COI106.es.rho4}} ({{v:S-COI106.es.ci4}}) in Spanish, {{v:S-COI106.ko.rho4}} ({{v:S-COI106.ko.ci4}}) in Korean and {{v:S-COI106.zh.rho4}} ({{v:S-COI106.zh.ci4}}) in Chinese, against {{v:S-COI.es.rho4}}, {{v:S-COI.ko.rho4}} and {{v:S-COI.zh.rho4}} as run; every line is {{v:S-COI106.es.verdict}}. The 106-unit line was computed by a script that first re-ran the locked scorer on the locked inputs and reproduced the verdict file byte for byte; no model was called.

**S-Trans and S-AliasAI (DEVIATIONS Entries 2 and 5).** The independent check flagged no category question in any language ({{v:AIC.es.phase_b_flagged}} Spanish, {{v:AIC.ko.phase_b_flagged}} Korean and {{v:AIC.zh.phase_b_flagged}} Chinese questions flagged; {{v:AIC.zh.flagged}} Chinese item flagged in all, a spirits category label that is not a category question). Both S-Trans lines therefore ran on all 30 questions and reproduce every primary statistic exactly (Presence and Consistency equal to the locked values in each language). The alias check judged {{v:AIC.alias.ko.not_used_for_this_brand}} Korean alias "not used for this brand" (an alias of {{v:AIC.alias.ko.off_brand}}) and no Chinese alias; that alias occurs in no Korean answer, so S-AliasAI equals the primary values. Entry 5 records that the S-Trans and S-AliasAI functions, committed before the first study call, had no run entry point and were run after scoring by a wrapper that only reads files and calls the committed functions.

**Corrected English comparator (DEVIATIONS Entry 6).** The English comparator is fixed as t₄'s locked table (§7.3). On 25 November 2026, after scoring, an erratum to t₄ found that t₄'s coder had missed typographic apostrophes in "Paula's Choice" and "L'Oréal Paris" and published a corrected table; the v0.62 pre-step already reads those apostrophes, so the corrected table is the like-for-like comparator. Table 5 sets the two side by side. Every verdict is the same under both comparators. Chinese H_Lang_Phi moves closer to the 0.30 falsification line, to {{v:ENC.Phi.zh.rho4}} (p = {{v:ENC.Phi.zh.p}}), and stays **{{v:ENC.Phi.zh.verdict}}**.

| Test | Spanish: locked → corrected | Korean: locked → corrected | Chinese: locked → corrected |
|---|---|---|---|
| H_Lang_Presence ρ_c | {{v:P.es.rho4}} → {{v:ENC.P.es.rho4}} | {{v:P.ko.rho4}} → {{v:ENC.P.ko.rho4}} | {{v:P.zh.rho4}} → {{v:ENC.P.zh.rho4}} |
| 95% CI | {{v:P.es.ci4}} → {{v:ENC.P.es.ci4}} | {{v:P.ko.ci4}} → {{v:ENC.P.ko.ci4}} | {{v:P.zh.ci4}} → {{v:ENC.P.zh.ci4}} |
| Δ_L | {{v:P.es.dL4}} → {{v:ENC.P.es.dL4}} | {{v:P.ko.dL4}} → {{v:ENC.P.ko.dL4}} | {{v:P.zh.dL4}} → {{v:ENC.P.zh.dL4}} |
| H_Lang_Phi ρ_c | {{v:Phi.es.rho4}} → {{v:ENC.Phi.es.rho4}} | {{v:Phi.ko.rho4}} → {{v:ENC.Phi.ko.rho4}} | {{v:Phi.zh.rho4}} → {{v:ENC.Phi.zh.rho4}} |
| H_Lang_Phi p | {{v:Phi.es.p4}} → {{v:ENC.Phi.es.p4}} | {{v:Phi.ko.p4}} → {{v:ENC.Phi.ko.p4}} | {{v:Phi.zh.p4}} → {{v:ENC.Phi.zh.p4}} |
| S-COI, 107 units | {{v:S-COI.es.rho4}} → {{v:ENC.S-COI.es.rho4}} | {{v:S-COI.ko.rho4}} → {{v:ENC.S-COI.ko.rho4}} | {{v:S-COI.zh.rho4}} → {{v:ENC.S-COI.zh.rho4}} |
| S-COI, 106 units | {{v:S-COI106.es.rho4}} → {{v:ENC.S-COI106.es.rho4}} | {{v:S-COI106.ko.rho4}} → {{v:ENC.S-COI106.ko.rho4}} | {{v:S-COI106.zh.rho4}} → {{v:ENC.S-COI106.zh.rho4}} |
| Verdicts (Presence; Phi) | {{v:ENC.P.es.verdict}}; {{v:ENC.Phi.es.verdict}} | {{v:ENC.P.ko.verdict}}; {{v:ENC.Phi.ko.verdict}} | {{v:ENC.P.zh.verdict}}; {{v:ENC.Phi.zh.verdict}} |

: The locked comparison beside the corrected-comparator sensitivity (`data/v62_sens_en_corrected_v0_62.json`). Joint reading under the corrected comparator: {{v:ENC.joint}}.

## 3.8 Translation and alias check

The questions were checked, before collection, by models of two providers other than the translator's, blind to one another as fixed in DEVIATIONS Entry 2: an independent back-translation from the target text only (C1, GPT-6 Astra), a bilingual review of source and target (C2, GPT-6 Astra), a coding of the back-translation against the English source (C3, Gemini 4 Argon), and an alias check (C4, GPT-6 Astra). Each of 50 items per language was coded equivalent, minor drift or meaning change. No item was strictly flagged (meaning change by both C2 and C3) in any language, so the pre-set rule for a re-lock decision (more than 6 of 30 questions strictly flagged) was not reached. Agreement between the three coders was low (Table 6): meaning change was almost never coded (one Chinese spirits label, by one checker), but the coders often disagreed on which items were equivalent and which showed minor drift. C2 rated {{v:AIC.es.nat.natural}} of 50 Spanish items natural and {{v:AIC.es.nat.acceptable}} acceptable, {{v:AIC.ko.nat.natural}} and {{v:AIC.ko.nat.acceptable}} in Korean, {{v:AIC.zh.nat.natural}} and {{v:AIC.zh.nat.acceptable}} in Chinese, none unnatural. The alias check coded {{v:AIC.alias.ko.n}} Korean aliases ({{v:AIC.alias.ko.standard}} standard, {{v:AIC.alias.ko.acceptable_variant}} acceptable variants, {{v:AIC.alias.ko.not_used_for_this_brand}} not used) and {{v:AIC.alias.zh.n}} Chinese aliases ({{v:AIC.alias.zh.standard}}, {{v:AIC.alias.zh.acceptable_variant}} and {{v:AIC.alias.zh.not_used_for_this_brand}}).

| Pair (items) | Spanish | Korean | Chinese |
|---|---|---|---|
| Translator vs C2 (35) | {{v:AIC.es.claude_vs_c2.agree}}, κ {{v:AIC.es.claude_vs_c2.kappa}} | {{v:AIC.ko.claude_vs_c2.agree}}, κ {{v:AIC.ko.claude_vs_c2.kappa}} | {{v:AIC.zh.claude_vs_c2.agree}}, κ {{v:AIC.zh.claude_vs_c2.kappa}} |
| Translator vs C3 (35) | {{v:AIC.es.claude_vs_c3.agree}}, κ {{v:AIC.es.claude_vs_c3.kappa}} | {{v:AIC.ko.claude_vs_c3.agree}}, κ {{v:AIC.ko.claude_vs_c3.kappa}} | {{v:AIC.zh.claude_vs_c3.agree}}, κ {{v:AIC.zh.claude_vs_c3.kappa}} |
| C2 vs C3 (50) | {{v:AIC.es.c2_vs_c3.agree}}, κ {{v:AIC.es.c2_vs_c3.kappa}} | {{v:AIC.ko.c2_vs_c3.agree}}, κ {{v:AIC.ko.c2_vs_c3.kappa}} | {{v:AIC.zh.c2_vs_c3.agree}}, κ {{v:AIC.zh.c2_vs_c3.kappa}} |
| Flagged / strictly flagged items | {{v:AIC.es.flagged}} / {{v:AIC.es.strictly_flagged}} | {{v:AIC.ko.flagged}} / {{v:AIC.ko.strictly_flagged}} | {{v:AIC.zh.flagged}} / {{v:AIC.zh.strictly_flagged}} |

: Agreement on the three equivalence codes (percent agreement, Cohen's κ; the linearly weighted κ equals or nearly equals κ here) between the translator's own back-translation codes and the independent checks (`ai_check/results/ai_check_analysis_v0_62.json`). The translator coded 35 items per language (the 15 spirits labels carry no translator code).

## 3.9 Summary of verdicts

Table 7 lists every pre-registered test with its verdict as written by the locked scorer. No sensitivity, and no item computed after scoring (§3.10), changes any of them.

| Test | Spanish | Korean | Chinese |
|---|---|---|---|
| H_Lang_Presence (primary): ρ_c ≥ 0.70 and p < 0.05 | {{v:P.es.verdict}} ({{v:P.es.rho}}) | {{v:P.ko.verdict}} ({{v:P.ko.rho}}) | {{v:P.zh.verdict}} ({{v:P.zh.rho}}) |
| H_Lang_Phi: ρ_c ≥ 0.50 and p < 0.05 | {{v:Phi.es.verdict}} ({{v:Phi.es.rho}}) | {{v:Phi.ko.verdict}} ({{v:Phi.ko.rho}}) | {{v:Phi.zh.verdict}} ({{v:Phi.zh.rho}}) |
| H_Lang_Rank (conditional on v1.14) | {{v:Rank.es.verdict}} | {{v:Rank.ko.verdict}} | {{v:Rank.zh.verdict}} |
| Joint reading (§2.6) | {{v:joint}} | | |

: Verdicts as written by `score_v0_62.py` (`v62_verdicts.json`). No sensitivity changes any of them (§3.7).

## 3.10 Pre-registered items computed after scoring (DEVIATIONS Entry 7)

The locked scorer writes the nine tests, the per-category values, Δ_L, the uncentred values and the S-Denon, S-Headphones and S-COI sensitivities. The other items the pre-registration plans were computed afterwards, under DEVIATIONS Entry 7, by a script that imports the locked modules unchanged, first re-ran the locked scorer and reproduced the verdict file byte for byte, read only archived files and called no model. They are secondary or descriptive, none bears on a verdict, and Appendix A reports them in full. In brief: per-model ρ_c with English Presence ranged from {{v:E7.pm.min}} to {{v:E7.pm.max}} across the 18 model-language-reading cells, {{v:E7.pm.n_below70}} of them below 0.70 (A.1); the languages agreed with one another at ρ_c {{v:E7.pair.ES-KO.rho}} (Spanish--Korean), {{v:E7.pair.ES-ZH.rho}} (Spanish--Chinese) and {{v:E7.pair.KO-ZH.rho}} (Korean--Chinese) (A.2); no category is language-sensitive by the labels of §2.5 (A.2); the two units that moved most in Spanish are the two units of t₄'s apostrophe erratum, measured against the locked comparator (A.2); MC_Language flags every Spanish model on all answers because the fixed rule does not count a short "Sí." as Spanish, while every category answer passes (A.3); S-Language, S-Script and S-Alias give the primary verdict everywhere (§3.7); each model recognised between {{v:E7.rec.min}} and {{v:E7.rec.max}} of the 88 yes/no brands per language (A.4); and the pooled measured cost factors of the three languages were below the central planning factors of pre-registration §6.2 (A.4). The home-language descriptive of §2.9 was not computed, because the country column it requires was not built before the lock, and the time benchmark of §2.7 awaits the scoring of the English t₅ wave.

# 4. Deviations

The deviations record (`osf/v62/DEVIATIONS.md`) holds {{v:dev.n_entries}} entries. Entry 0 was written before the lock; Entries 1--3 after the lock and before any study call; Entries 4--8 after the single scoring run. None changes a hypothesis, threshold, unit set, model, question, seed or scored verdict.

| Entry | Date | What it records | Used in |
|---|---|---|---|
| 0 | 10--12 Nov | Pre-acquisition conflict-of-interest screen of all 112 units (Declarations). Registries unchanged, Denon kept (option A); every Presence result also reported without Denon, without headphones and without the six units with a tie (S-COI). Decided 12 November. | §3.7 |
| 1 | 12 Nov | Fake-SDK dry-run re-runs: the spend at which the $80 pause and $100 stop fire varies by under $1; the rules hold. A record only. | none |
| 2 | 21 Nov | Native translation checks (not done before the lock) replaced by an independent AI check (C1--C4) by two other providers, fixed before data with its comparisons, rule (no human tiebreak), $8 cap and limits; adds S-Trans and S-AliasAI. Two addenda: script hashes; a one-line client fix in a free lookup. | §3.7, §3.8, limitation 1 |
| 3 | 24--25 Nov | Window start moved from 29 to 25 November (end unchanged) through the locked script's declared-window route; approved by the pre-registrant. | §3.1 |
| 4 | 25 Nov | S-COI ran on 107 units: Jack Daniel's left in by a key mismatch; the 106-unit S-COI reported beside it. Approved by the pre-registrant. | §3.7, Table 4 |
| 5 | 25 Nov | Run wrapper for S-Trans and S-AliasAI, whose committed functions had no entry point; procedure only. Approved by the pre-registrant. | §3.7 |
| 6 | 25 Nov | Sensitivity with t₄'s corrected English table (erratum of 25 November) beside the locked comparison. Approved by the pre-registrant. | §3.7, Table 5, Figures 2--3 |
| 7 | 25 Nov | Pre-registered items the locked scorer did not compute (per-model ρ_c, the φ--π̂ flag, the §2.5 labels, pairs and largest shifts, five manipulation checks, S-Language, S-Script, S-Alias and the §2.9 descriptives), computed from the archived data with the locked modules unchanged; the readings chosen where the text is open are recorded. Home-language descriptive not computed; time benchmark not available. Approved by the pre-registrant. | §3.2, §3.4, §3.7, §3.10, Appendix A |
| 8 | 25 Nov | The one timed-out call: charged $0 by the guard, not the §6.5 worst case; strict figures reported beside the recorded spend; the re-run pass and its approval recorded. No spend record changed. Approved by the pre-registrant. | §3.1 |

: DEVIATIONS Entries 0--8 (`osf/v62/DEVIATIONS.md`). Entries 4--8 were approved by the pre-registrant on 25 November 2026; Entries 7 and 8 are in commit `69e1aa9`.

# 5. Discussion

Asked in Spanish, Korean or Chinese, the three newest flagship models named the omnibus brands in much the same order as in English. Presence agreement was highest in Spanish and lowest in Chinese, and all three cleared the confirmation threshold, under every sensitivity. For Presence as the programme measures it, an English measurement is therefore a good guide to the order of brands that the same models make available in these three languages, at least for the five consumer categories of the omnibus and for questions that name no market. The order is not the whole picture: the level moved, upward in Spanish and downward in Korean and Chinese, so a brand's absolute Presence in one language is not its Presence in another, even where its rank among competitors holds.

Consistency is a different matter. Whether the three models agree in naming a brand carried over to Spanish with a moderate correlation and only weakly to Korean and Chinese, with large differences between categories, including negative values. Two readings are open and this wave cannot separate them. φ is noisier than π̂, because it depends on three models and on at least two defined runs, so a weaker correlation is expected from measurement alone; and the models may genuinely agree differently in different languages, for example where one model knows a brand's Korean or Chinese name and another does not. The alias table, which names only the forms the runner could list (§2.2; limitation 7), adds a third possibility for Korean and Chinese: a brand named in a script the table does not cover is a missed mention for one model and not another. The script descriptive computed after scoring (Appendix A.4) shows how much the alias table carries: {{v:E7.script.ko.share_native_only}} of the coded Korean mentions and {{v:E7.script.zh.share_native_only}} of the Chinese ones were found only through a Hangul or Han alias.

The study also shows how small coding details reach a cross-language comparison. A typographic apostrophe in two English brand names moved English values enough to shift Chinese Consistency agreement from {{v:Phi.zh.rho4}} to {{v:ENC.Phi.zh.rho4}}, and a key mismatch left one unit in a sensitivity it was meant to leave. Neither changed a verdict; both are reported beside the locked results.

# 6. Limitations

1. **No native review.** The questions were translated by a model (Claude Opus 5.5) and checked only by other models: an independent back-translation (GPT-6 Astra, from the target text only), coded against the source by a third model (Gemini 4 Argon), and a bilingual model review (GPT-6 Astra). No native speaker reviewed any language; naturalness and equivalence were judged by models only, and the low agreement between them on minor drift (§3.8) shows the check's limits. Shared model biases, for example toward literal renderings, are not detected.
2. The forward translator belongs to the same provider as one of the measured models; the two checkers are also measured models (they saw translations, never answers).
3. Language is varied without a market: the registries are US-market selections, and the results describe what these three models answer when asked in each language, not what users in any country receive from locally available assistants.
4. One variety per language: neutral Latin American Spanish, standard South Korean and Simplified Mainland Chinese.
5. Time and language are confounded: t₄ was collected from 11 November 2026, this wave on 25 November; the t₅ benchmark that would separate them is not yet available (§3.10).
6. No web search; one model per provider; three runs, as t₄.
7. Korean and Chinese coding rests on a new alias table whose forms were mostly unconfirmed on brand sites before the lock; 38 units have no Chinese alias and are matched in Latin script only, which under-counts Han-script mentions the table does not list.
8. The pre-registered checks, Presence sensitivities S-Language, S-Script and S-Alias, and descriptives of Appendix A were computed after the scoring run (Entry 7), under readings of the text chosen then and recorded in that entry; the home-language descriptive was not computed, and the fixed language rule of MC_Language does not recognise short Spanish yes/no answers.
9. No buyer persona: as at t₄, every question is asked without a description of the asker. Outside audits find that a stated persona changes which mid-market brands are recommended (Jack et al., 2026) and that U.S.-developed models favour American entities (Rienecker et al., 2026); whether the language results hold with a persona is not tested.
10. The as-run S-COI kept one unit it was meant to drop (Entry 4), and the S-Trans and S-AliasAI sensitivities were run after scoring by a wrapper (Entry 5); the English comparator was corrected after scoring (Entry 6); and the guard charged the one timed-out attempt nothing where pre-registration §6.5 prices it at its worst case (Entry 8). All four are reported beside the locked results and none changes a verdict.

# 7. Future Research and Open Items

The non-English results invite three follow-ups. A Consistency test with more models or runs per language would show whether the weak Korean and Chinese agreement is noise or a real difference in how models agree. A wave with questions that name a market (for example "in Korea" or "in Mexico") would separate language from market, which this wave held apart by design. The English t₅ wave, once scored, gives the time benchmark of §2.7: how much of the gap between English and each language is time rather than language. A home-language descriptive (§2.9) needs a country-of-origin column built from cited sources before data; a later wave can fix one at its lock.

# Declarations {-}

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-asks, in Spanish, Korean and Chinese, questions against brand registries fixed in earlier phases (v0.19--v0.23); it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward unchanged. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands --- Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) --- characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry, AKG was substituted with Denon before the v0.19 pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary. Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. The registries of this study are those of the English t₄ wave, with Denon included and disclosed; every result is also reported without the Denon unit (S-Denon) and without the headphones category (S-Headphones). One of the three languages is Korean, and South Korea is Samsung Electronics' home market: answers in Korean, as in any language, may name Samsung-group brands that are not registry units; such names are never coded or scored, because coding counts only the 112 registry units. The conflict-of-interest screen of this study (DEVIATIONS Entry 0, Part F) found further ties. Cheil Worldwide, a marketing company of the Samsung group in which Samsung Electronics holds 28.43%, or its agency Iris has done advertising, public-relations or search-marketing work for five registry brands: Chevrolet (for GM Korea, 2017), BMW (UK consumer public relations, 2018), Bentley (experiential agency of record in the Americas from 2021), Jack Daniel's (UK digital agency from 2022, since replaced) and Eucerin (search marketing for Beiersdorf from 2024). As the pre-registrant decided on November 12, 2026, these five brands were kept in every analysis, as Denon was, and every Presence result is also reported without them and Denon (sensitivity S-COI). The S-COI computed by the locked scorer left Jack Daniel's in by a key mismatch and ran on 107 units; the intended 106-unit S-COI is reported beside it (DEVIATIONS Entry 4), and neither changes a verdict. Samsung Electronics supplies semiconductors to Tesla under a contract running from 2025 to 2033, and Samsung SDI supplies batteries to Hyundai under an agreement of 2023; like the supply relationships of record, these are non-competitive and impose no restriction on the registries. Hotel Shilla, a Samsung affiliate, operates duty-free shops that sell brands of several registry categories among many others. Acquisition, coding and scoring are fully automated against the locked registries, and the pre-registration was locked and deposited before the first call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

## Funding {-}

Self-funded.

## Ethics {-}

Not applicable; no human subjects.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## Data and code availability {-}

The locked pre-registration, English source and translated probe files, alias table, cost estimate, scripts and tests, deviations record and lock manifest are deposited at OSF (osf.io/ec6wh), `v62/`. The raw answers (`data/v62_raw.jsonl`), collection logs, gate records, coded tables (`data/coded/`), verdict file (`v62_verdicts.json`), the AI check results (`ai_check/results/`), the three sensitivity files of Entries 4--6 (commit `4ac1aa9`), and the files of Entries 7 and 8 (commit `69e1aa9`: `scripts/post_scoring_planned_items_v62.py`, `data/v62_planned_items_v0_62.json`, `data/v62_planned_items_summary_v0_62.json`, `data/v62_planned_category_labels_v0_62.csv`, `data/v62_planned_top10_shift_v0_62.csv`, `data/v62_planned_checks_v0_62.csv`, and the re-coded tables `data/s_alias_off/` and `data/latin_only/`) are in the programme's repository (github.com/thirdsystem-aias/aias, branch `v0.62-nohand`, `osf/v62/`) and are planned for OSF with the study's data deposit. Every number in this paper is read from `papers/v0_62/v62_values.json`, written by `papers/v0_62/values_v0_62.py` from those files, which names the source file and field of each value; the figures are drawn by `scripts/build_charts_v62_paper.py`.

# References {-}

González Castro, P. U. (2026a). *AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval*. SSRN 6659000.

González Castro, P. U. (2026b). *The AIAS™ Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy* (v1.2). SSRN 6761698.

González Castro, P. U. (2026c). *The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification (v1.3)*. SSRN 6797679.

González Castro, P. U. (2026d). *The AIAS Presence Measurement Protocol v1.4: Recognition × Recall Decomposition and Multi-Component AI Availability*. SSRN 6799479.

González Castro, P. U. (2026e). *The AIAS™ Presence Measurement Protocol: Multi-Statistic C2 Specification and Two-Channel Recall Decomposition* (v1.5). SSRN 6810758.

González Castro, P. U. (2026f). *Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension* (AIAS Methodology v1.6). SSRN 6816340.

González Castro, P. U. (2026g). *Consistency without Independence: A Pre-Registered Test of Coefficient-of-Variation as the Consistency Component of AIAS™* (v1.7). SSRN 6878818.

González Castro, P. U. (2026h). *A Mean-Independent Consistency Instrument for Cross-Model AI Presence: Redesigning CPC on a Quasi-Binomial Dispersion Basis* (AIAS Methodology v1.8). SSRN 6963359.

González Castro, P. U. (2026j). *AI Availability as a Third Measurable Layer of Brand Availability: Five-Substrate Empirical Anchoring of the AIAS™ Presence Measurement Protocol --- Synthesis under Locked v1.6 Methodology* (AIAS 1.0). SSRN 6817841.

González Castro, P. U. (2026k). *Presence and Consistency: A Two-Component Measurement of AI Availability. The AIAS™ 2.0 Synthesis*. OSF `ec6wh/aias_2_0`.

González Castro, P. U. (2026l). *Tri-System Brand Growth: The AI Mediation Layer*. MSI Working Paper, Report No. 26-132. Marketing Science Institute.

Jack, W., Lehman, N., Maloney, K., & Xu, S. (2026). *Persona Conditioning of Brand Recommendations in Retrieval-Augmented Commercial Chat: A Prominence-Stratified Cross-Provider Audit*. arXiv 2605.30207 (v1, 28 May 2026; cs.AI).

Rienecker et al. (2026). *Auditing Preferences for Brands and Cultures in LLMs* (ChoiceEval). arXiv 2603.18300.

Romaniuk, J., & Sharp, B. (2016). *How Brands Grow: Part 2*. Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

Programme records cited by version (OSF `ec6wh`; github.com/thirdsystem-aias/aias): the omnibus registries and phase papers of v0.19 (audiophile headphones, SSRN 6809182), v0.20 (skincare, SSRN 6811441), v0.21 (cosmetics, SSRN 6815378), v0.22 (automotive, SSRN 6829118) and v0.23 (premium spirits, SSRN 6834298); the English t₄ wave v0.42 (pre-registration `v0.42-prereg-r1`, OSF `ec6wh/v42`), whose panel, settings, coder and scored brand table this wave uses, and its erratum of 25 November 2026; and the Ranking instrument v1.14 (Stage 1, commit `{{v:Rank.v114_commit}}`).

\clearpage
\setcounter{table}{0}
\renewcommand{\thetable}{A\arabic{table}}

# Appendix A. Pre-registered items computed after scoring (DEVIATIONS Entry 7) {-}

Everything in this appendix was computed after the one scoring run (commit `262464d`), under DEVIATIONS Entry 7 (commit `69e1aa9`), from archived files only: no model or API was called and nothing was paid. The script (`osf/v62/scripts/post_scoring_planned_items_v62.py`) imports the locked scorer, coder, parameter and budget modules unchanged, first re-ran the locked scorer on the locked inputs and reproduced `v62_verdicts.json` byte for byte, and wrote `data/v62_planned_items_v0_62.json` and its summary and tables. No item here changes a verdict, the joint reading, a coded table or a locked file; under the pre-registration's own rules none of them bears on a verdict. Where the pre-registration's text is open, Entry 7 records the reading chosen; the readings that matter for a table are stated with it.

## A.1 Per-model agreement and the Consistency--Presence flag {-}

Per-model ρ_c (pre-registration §2.2) is reported under two readings, both on all {{v:E7.pm.n}} units and as point values, like the locked per-category ρ_c. Reading (i) compares each model with itself: x is that model's own English t₄ π̂ (t₄'s coded rows), y is the same model's π̂ in the language. Reading (ii) compares each model with the panel: x is the three-model English π̂ of the locked t₄ table, y is the model's π̂ in the language. Under both readings every model clears 0.70 in every language; Claude Fable 5.2 agrees most closely with English in each language.

| Model | Spanish (i) / (ii) | Korean (i) / (ii) | Chinese (i) / (ii) |
|---|---|---|---|
| Claude Fable 5.2 | {{v:E7.pm.es.claude-fable-5-2.i}} / {{v:E7.pm.es.claude-fable-5-2.ii}} | {{v:E7.pm.ko.claude-fable-5-2.i}} / {{v:E7.pm.ko.claude-fable-5-2.ii}} | {{v:E7.pm.zh.claude-fable-5-2.i}} / {{v:E7.pm.zh.claude-fable-5-2.ii}} |
| GPT-6 Astra | {{v:E7.pm.es.gpt-6-astra.i}} / {{v:E7.pm.es.gpt-6-astra.ii}} | {{v:E7.pm.ko.gpt-6-astra.i}} / {{v:E7.pm.ko.gpt-6-astra.ii}} | {{v:E7.pm.zh.gpt-6-astra.i}} / {{v:E7.pm.zh.gpt-6-astra.ii}} |
| Gemini 4 Argon | {{v:E7.pm.es.gemini-4-argon.i}} / {{v:E7.pm.es.gemini-4-argon.ii}} | {{v:E7.pm.ko.gemini-4-argon.i}} / {{v:E7.pm.ko.gemini-4-argon.ii}} | {{v:E7.pm.zh.gemini-4-argon.i}} / {{v:E7.pm.zh.gemini-4-argon.ii}} |

: Per-model ρ_c with English recall Presence (n = {{v:E7.pm.n}}): reading (i), the model's own English t₄ π̂; reading (ii), the three-model English π̂ of the locked t₄ table (`data/v62_planned_items_summary_v0_62.json`, `per_model_rho_c`).

The pre-registration (§2.3) flags a language if φ and π̂ in that language are correlated at |ρ_c| of 0.50 or more, which would mean that Consistency is tracking Presence. On the units with φ defined in the language, |ρ_c(φ, π̂)| was {{v:E7.phipi.es.def.abs}} in Spanish (n = {{v:E7.phipi.es.def.n}}), {{v:E7.phipi.ko.def.abs}} in Korean (n = {{v:E7.phipi.ko.def.n}}) and {{v:E7.phipi.zh.def.abs}} in Chinese (ρ_c = {{v:E7.phipi.zh.def.rho}}, n = {{v:E7.phipi.zh.def.n}}); on the units of the H_Lang_Phi test it was {{v:E7.phipi.es.hlp.abs}}, {{v:E7.phipi.ko.hlp.abs}} and {{v:E7.phipi.zh.hlp.abs}} (n = {{v:E7.phipi.es.hlp.n}}, {{v:E7.phipi.ko.hlp.n}}, {{v:E7.phipi.zh.hlp.n}}). The flag is not raised in any language.

## A.2 Level labels, agreement between languages and the largest shifts (§2.5) {-}

Table A2 applies the descriptive labels of pre-registration §2.5 per category. Δ_L is the mean of π̂ in the language minus English π̂ over the category's units, with a 95% percentile interval from 10,000 bootstrap resamples of those units (seed 620131, the seed of the locked Δ_L interval); a unit "moves" if its π̂ in the language differs from its English π̂ by more than 1/6. No category-language cell is language-sensitive. Skincare in Chinese is the one intermediate cell: its ρ_c is below 0.70 and a third of its units move.

| Language | Category | ρ_c | Δ_L (95% CI) | Units moving > 1/6 | Label |
|---|---|---:|---|---|---|
| Spanish | Headphones (v0.19) | {{v:E7.cat.es.v0.19.rho}} | {{v:E7.cat.es.v0.19.dL}} ({{v:E7.cat.es.v0.19.dL_ci}}) | {{v:E7.cat.es.v0.19.moved}} | {{v:E7.cat.es.v0.19.label}} |
| Spanish | Skincare (v0.20) | {{v:E7.cat.es.v0.20.rho}} | {{v:E7.cat.es.v0.20.dL}} ({{v:E7.cat.es.v0.20.dL_ci}}) | {{v:E7.cat.es.v0.20.moved}} | {{v:E7.cat.es.v0.20.label}} |
| Spanish | Cosmetics (v0.21) | {{v:E7.cat.es.v0.21.rho}} | {{v:E7.cat.es.v0.21.dL}} ({{v:E7.cat.es.v0.21.dL_ci}}) | {{v:E7.cat.es.v0.21.moved}} | {{v:E7.cat.es.v0.21.label}} |
| Spanish | Automotive (v0.22) | {{v:E7.cat.es.v0.22.rho}} | {{v:E7.cat.es.v0.22.dL}} ({{v:E7.cat.es.v0.22.dL_ci}}) | {{v:E7.cat.es.v0.22.moved}} | {{v:E7.cat.es.v0.22.label}} |
| Spanish | Spirits (v0.23) | {{v:E7.cat.es.v0.23.rho}} | {{v:E7.cat.es.v0.23.dL}} ({{v:E7.cat.es.v0.23.dL_ci}}) | {{v:E7.cat.es.v0.23.moved}} | {{v:E7.cat.es.v0.23.label}} |
| Korean | Headphones (v0.19) | {{v:E7.cat.ko.v0.19.rho}} | {{v:E7.cat.ko.v0.19.dL}} ({{v:E7.cat.ko.v0.19.dL_ci}}) | {{v:E7.cat.ko.v0.19.moved}} | {{v:E7.cat.ko.v0.19.label}} |
| Korean | Skincare (v0.20) | {{v:E7.cat.ko.v0.20.rho}} | {{v:E7.cat.ko.v0.20.dL}} ({{v:E7.cat.ko.v0.20.dL_ci}}) | {{v:E7.cat.ko.v0.20.moved}} | {{v:E7.cat.ko.v0.20.label}} |
| Korean | Cosmetics (v0.21) | {{v:E7.cat.ko.v0.21.rho}} | {{v:E7.cat.ko.v0.21.dL}} ({{v:E7.cat.ko.v0.21.dL_ci}}) | {{v:E7.cat.ko.v0.21.moved}} | {{v:E7.cat.ko.v0.21.label}} |
| Korean | Automotive (v0.22) | {{v:E7.cat.ko.v0.22.rho}} | {{v:E7.cat.ko.v0.22.dL}} ({{v:E7.cat.ko.v0.22.dL_ci}}) | {{v:E7.cat.ko.v0.22.moved}} | {{v:E7.cat.ko.v0.22.label}} |
| Korean | Spirits (v0.23) | {{v:E7.cat.ko.v0.23.rho}} | {{v:E7.cat.ko.v0.23.dL}} ({{v:E7.cat.ko.v0.23.dL_ci}}) | {{v:E7.cat.ko.v0.23.moved}} | {{v:E7.cat.ko.v0.23.label}} |
| Chinese | Headphones (v0.19) | {{v:E7.cat.zh.v0.19.rho}} | {{v:E7.cat.zh.v0.19.dL}} ({{v:E7.cat.zh.v0.19.dL_ci}}) | {{v:E7.cat.zh.v0.19.moved}} | {{v:E7.cat.zh.v0.19.label}} |
| Chinese | Skincare (v0.20) | {{v:E7.cat.zh.v0.20.rho}} | {{v:E7.cat.zh.v0.20.dL}} ({{v:E7.cat.zh.v0.20.dL_ci}}) | {{v:E7.cat.zh.v0.20.moved}} | {{v:E7.cat.zh.v0.20.label}} |
| Chinese | Cosmetics (v0.21) | {{v:E7.cat.zh.v0.21.rho}} | {{v:E7.cat.zh.v0.21.dL}} ({{v:E7.cat.zh.v0.21.dL_ci}}) | {{v:E7.cat.zh.v0.21.moved}} | {{v:E7.cat.zh.v0.21.label}} |
| Chinese | Automotive (v0.22) | {{v:E7.cat.zh.v0.22.rho}} | {{v:E7.cat.zh.v0.22.dL}} ({{v:E7.cat.zh.v0.22.dL_ci}}) | {{v:E7.cat.zh.v0.22.moved}} | {{v:E7.cat.zh.v0.22.label}} |
| Chinese | Spirits (v0.23) | {{v:E7.cat.zh.v0.23.rho}} | {{v:E7.cat.zh.v0.23.dL}} ({{v:E7.cat.zh.v0.23.dL_ci}}) | {{v:E7.cat.zh.v0.23.moved}} | {{v:E7.cat.zh.v0.23.label}} |

: Per-category level labels of pre-registration §2.5 against the locked English comparator (`data/v62_planned_category_labels_v0_62.csv`).

Agreement between pairs of languages (§2.5), on the {{v:E7.pair.ES-KO.n}} units with a 95% bootstrap interval and permutation p (10,000 each, seed 620141): Spanish--Korean ρ_c = {{v:E7.pair.ES-KO.rho}} ({{v:E7.pair.ES-KO.ci}}; p {{v:E7.pair.ES-KO.p}}), Spanish--Chinese {{v:E7.pair.ES-ZH.rho}} ({{v:E7.pair.ES-ZH.ci}}; p {{v:E7.pair.ES-ZH.p}}) and Korean--Chinese {{v:E7.pair.KO-ZH.rho}} ({{v:E7.pair.KO-ZH.ci}}; p {{v:E7.pair.KO-ZH.p}}).

Table A3 lists the ten units whose π̂ moved most from English in each language. The two largest Spanish shifts, {{v:E7.top.es.1.name}} and {{v:E7.top.es.2.name}}, are the two units of t₄'s apostrophe erratum (§3.7, DEVIATIONS Entry 6): they are measured here against the locked English comparator, in which t₄'s coder missed their typographic apostrophes, so part of each shift reflects the English coding rather than the Spanish answers. {{v:E7.top.ko.9.name}} also appears in the Korean list (ninth). In Chinese, two skincare brands that the English answers did not name at all rank second and fifth ({{v:E7.top.zh.2.name}} and {{v:E7.top.zh.5.name}}). Units tied with the tenth are counted, not listed: {{v:E7.top.es.ties}} in Spanish, {{v:E7.top.ko.ties}} in Korean and {{v:E7.top.zh.ties}} in Chinese.

| Rank | Spanish | Korean | Chinese |
|---:|---|---|---|
| 1 | {{v:E7.top.es.1.name}} ({{v:E7.top.es.1.shift}}) | {{v:E7.top.ko.1.name}} ({{v:E7.top.ko.1.shift}}) | {{v:E7.top.zh.1.name}} ({{v:E7.top.zh.1.shift}}) |
| 2 | {{v:E7.top.es.2.name}} ({{v:E7.top.es.2.shift}}) | {{v:E7.top.ko.2.name}} ({{v:E7.top.ko.2.shift}}) | {{v:E7.top.zh.2.name}} ({{v:E7.top.zh.2.shift}}) |
| 3 | {{v:E7.top.es.3.name}} ({{v:E7.top.es.3.shift}}) | {{v:E7.top.ko.3.name}} ({{v:E7.top.ko.3.shift}}) | {{v:E7.top.zh.3.name}} ({{v:E7.top.zh.3.shift}}) |
| 4 | {{v:E7.top.es.4.name}} ({{v:E7.top.es.4.shift}}) | {{v:E7.top.ko.4.name}} ({{v:E7.top.ko.4.shift}}) | {{v:E7.top.zh.4.name}} ({{v:E7.top.zh.4.shift}}) |
| 5 | {{v:E7.top.es.5.name}} ({{v:E7.top.es.5.shift}}) | {{v:E7.top.ko.5.name}} ({{v:E7.top.ko.5.shift}}) | {{v:E7.top.zh.5.name}} ({{v:E7.top.zh.5.shift}}) |
| 6 | {{v:E7.top.es.6.name}} ({{v:E7.top.es.6.shift}}) | {{v:E7.top.ko.6.name}} ({{v:E7.top.ko.6.shift}}) | {{v:E7.top.zh.6.name}} ({{v:E7.top.zh.6.shift}}) |
| 7 | {{v:E7.top.es.7.name}} ({{v:E7.top.es.7.shift}}) | {{v:E7.top.ko.7.name}} ({{v:E7.top.ko.7.shift}}) | {{v:E7.top.zh.7.name}} ({{v:E7.top.zh.7.shift}}) |
| 8 | {{v:E7.top.es.8.name}} ({{v:E7.top.es.8.shift}}) | {{v:E7.top.ko.8.name}} ({{v:E7.top.ko.8.shift}}) | {{v:E7.top.zh.8.name}} ({{v:E7.top.zh.8.shift}}) |
| 9 | {{v:E7.top.es.9.name}} ({{v:E7.top.es.9.shift}}) | {{v:E7.top.ko.9.name}} ({{v:E7.top.ko.9.shift}}) | {{v:E7.top.zh.9.name}} ({{v:E7.top.zh.9.shift}}) |
| 10 | {{v:E7.top.es.10.name}} ({{v:E7.top.es.10.shift}}) | {{v:E7.top.ko.10.name}} ({{v:E7.top.ko.10.shift}}) | {{v:E7.top.zh.10.name}} ({{v:E7.top.zh.10.shift}}) |

: The ten largest shifts in π̂ from English per language (π̂ in the language minus English π̂; locked English comparator; `data/v62_planned_top10_shift_v0_62.csv`).

## A.3 Manipulation checks (§2.8) {-}

MC_Complete: {{v:E7.mc.complete.answered}} of {{v:E7.mc.complete.sent}} calls answered ({{v:E7.mc.complete.lines}} attempt lines, the extra line being the timed-out attempt), {{v:E7.mc.complete.share}} in every model, language and phase. MC_Served: {{v:E7.mc.served.mismatched}} mismatches between the requested and the served model in {{v:E7.mc.served.checked}} answered calls ({{v:E7.mc.served.pass}}). MC_Script: {{v:E7.mc.script.n}} Chinese answers with any of the 24 Traditional-only characters, for every model. MC_Alias: {{v:E7.mc.alias.matches}} matches of collision-prone aliases exported in {{v:E7.mc.alias.calls}} calls (Korean aliases of {{v:E7.mc.alias.ko}}; Chinese aliases of {{v:E7.mc.alias.zh}}); these are counts only, and no match was read for Entry 7. MC_Truncation: {{v:E7.mc.trunc.n}} calls at the output cap; the only finish reasons recorded are {{v:E7.mc.trunc.reasons}}. MC_Window: {{v:E7.mc.window.h}} hours from the first call to the last. MC_Budget: {{v:E7.mc.budget.spend}} from recorded usage, {{v:E7.mc.budget.not_sent}} calls not sent, no pause or stop (Entry 8 adds the strict figure, §3.1).

MC_Language (Table A4) applies the pre-registered fixed rule (`code_v0_62.in_language`) and flags a model-language cell below 95%. Read on all answers, the unit the pre-registration names, it flags every Spanish model: the rule counts an answer as Spanish only if Spanish function words outnumber English ones, and a short yes/no answer such as "Sí." contains none of the listed words, so most Spanish yes/no answers fail it. The category answers, on which every test rests, pass in every cell; the lowest is Chinese Claude Fable 5.2 at {{v:E7.mc.lang.zh.claude-fable-5-2.B}} ({{v:E7.mc.lang.zh.claude-fable-5-2.B.count}}), not flagged; its three off-language answers are the three runs of one spirits question ({{v:E7.mc.lang.zh_off_probe}}), which S-Language drops (§3.7). Read on the yes/no answers alone, the rule also flags Chinese Claude Fable 5.2 ({{v:E7.mc.lang.zh.claude-fable-5-2.A}}). Under §2.8 an MC_Language flag changes no code and no verdict.

| Model | Language | All answers | Category answers (Phase B) | Yes/no answers (Phase A) |
|---|---|---|---|---|
| Claude Fable 5.2 | Spanish | {{v:E7.mc.lang.es.claude-fable-5-2.all}} ({{v:E7.mc.lang.es.claude-fable-5-2.all.flag}}) | {{v:E7.mc.lang.es.claude-fable-5-2.B}} ({{v:E7.mc.lang.es.claude-fable-5-2.B.flag}}) | {{v:E7.mc.lang.es.claude-fable-5-2.A}} ({{v:E7.mc.lang.es.claude-fable-5-2.A.flag}}) |
| GPT-6 Astra | Spanish | {{v:E7.mc.lang.es.gpt-6-astra.all}} ({{v:E7.mc.lang.es.gpt-6-astra.all.flag}}) | {{v:E7.mc.lang.es.gpt-6-astra.B}} ({{v:E7.mc.lang.es.gpt-6-astra.B.flag}}) | {{v:E7.mc.lang.es.gpt-6-astra.A}} ({{v:E7.mc.lang.es.gpt-6-astra.A.flag}}) |
| Gemini 4 Argon | Spanish | {{v:E7.mc.lang.es.gemini-4-argon.all}} ({{v:E7.mc.lang.es.gemini-4-argon.all.flag}}) | {{v:E7.mc.lang.es.gemini-4-argon.B}} ({{v:E7.mc.lang.es.gemini-4-argon.B.flag}}) | {{v:E7.mc.lang.es.gemini-4-argon.A}} ({{v:E7.mc.lang.es.gemini-4-argon.A.flag}}) |
| Claude Fable 5.2 | Korean | {{v:E7.mc.lang.ko.claude-fable-5-2.all}} ({{v:E7.mc.lang.ko.claude-fable-5-2.all.flag}}) | {{v:E7.mc.lang.ko.claude-fable-5-2.B}} ({{v:E7.mc.lang.ko.claude-fable-5-2.B.flag}}) | {{v:E7.mc.lang.ko.claude-fable-5-2.A}} ({{v:E7.mc.lang.ko.claude-fable-5-2.A.flag}}) |
| GPT-6 Astra | Korean | {{v:E7.mc.lang.ko.gpt-6-astra.all}} ({{v:E7.mc.lang.ko.gpt-6-astra.all.flag}}) | {{v:E7.mc.lang.ko.gpt-6-astra.B}} ({{v:E7.mc.lang.ko.gpt-6-astra.B.flag}}) | {{v:E7.mc.lang.ko.gpt-6-astra.A}} ({{v:E7.mc.lang.ko.gpt-6-astra.A.flag}}) |
| Gemini 4 Argon | Korean | {{v:E7.mc.lang.ko.gemini-4-argon.all}} ({{v:E7.mc.lang.ko.gemini-4-argon.all.flag}}) | {{v:E7.mc.lang.ko.gemini-4-argon.B}} ({{v:E7.mc.lang.ko.gemini-4-argon.B.flag}}) | {{v:E7.mc.lang.ko.gemini-4-argon.A}} ({{v:E7.mc.lang.ko.gemini-4-argon.A.flag}}) |
| Claude Fable 5.2 | Chinese | {{v:E7.mc.lang.zh.claude-fable-5-2.all}} ({{v:E7.mc.lang.zh.claude-fable-5-2.all.flag}}) | {{v:E7.mc.lang.zh.claude-fable-5-2.B}} ({{v:E7.mc.lang.zh.claude-fable-5-2.B.flag}}) | {{v:E7.mc.lang.zh.claude-fable-5-2.A}} ({{v:E7.mc.lang.zh.claude-fable-5-2.A.flag}}) |
| GPT-6 Astra | Chinese | {{v:E7.mc.lang.zh.gpt-6-astra.all}} ({{v:E7.mc.lang.zh.gpt-6-astra.all.flag}}) | {{v:E7.mc.lang.zh.gpt-6-astra.B}} ({{v:E7.mc.lang.zh.gpt-6-astra.B.flag}}) | {{v:E7.mc.lang.zh.gpt-6-astra.A}} ({{v:E7.mc.lang.zh.gpt-6-astra.A.flag}}) |
| Gemini 4 Argon | Chinese | {{v:E7.mc.lang.zh.gemini-4-argon.all}} ({{v:E7.mc.lang.zh.gemini-4-argon.all.flag}}) | {{v:E7.mc.lang.zh.gemini-4-argon.B}} ({{v:E7.mc.lang.zh.gemini-4-argon.B.flag}}) | {{v:E7.mc.lang.zh.gemini-4-argon.A}} ({{v:E7.mc.lang.zh.gemini-4-argon.A.flag}}) |

: MC_Language: share of answers in the asked language by the fixed rule, flagged below 95% (`data/v62_planned_checks_v0_62.csv`). Category answers: 90 per cell; yes/no answers: 88.

## A.4 Descriptives (§2.9) {-}

**Run-to-run reliability and recognition.** rel1 and rel3 are v0.42's run-to-run reliability of recall Presence per model and language: rel1 is the mean ρ_c over the three pairs of runs, rel3 its Spearman--Brown step-up to the mean of three runs (on t₄'s English rows the transcription reproduces v0.42's locked rel1 exactly). Recognition is the number of the 88 yes/no brand questions of v0.19--v0.22 answered "yes"; English is recomputed on the same 88 questions from t₄'s coded tables. No yes/no answer was a non-answer.

| Model | Measure | English (t₄) | Spanish | Korean | Chinese |
|---|---|---:|---:|---:|---:|
| Claude Fable 5.2 | rel1 | {{v:E7.rel.en.claude-fable-5-2.rel1}} | {{v:E7.rel.es.claude-fable-5-2.rel1}} | {{v:E7.rel.ko.claude-fable-5-2.rel1}} | {{v:E7.rel.zh.claude-fable-5-2.rel1}} |
| | rel3 | {{v:E7.rel.en.claude-fable-5-2.rel3}} | {{v:E7.rel.es.claude-fable-5-2.rel3}} | {{v:E7.rel.ko.claude-fable-5-2.rel3}} | {{v:E7.rel.zh.claude-fable-5-2.rel3}} |
| | recognised (of 88) | {{v:E7.rec.en.claude-fable-5-2}} | {{v:E7.rec.es.claude-fable-5-2}} | {{v:E7.rec.ko.claude-fable-5-2}} | {{v:E7.rec.zh.claude-fable-5-2}} |
| GPT-6 Astra | rel1 | {{v:E7.rel.en.gpt-6-astra.rel1}} | {{v:E7.rel.es.gpt-6-astra.rel1}} | {{v:E7.rel.ko.gpt-6-astra.rel1}} | {{v:E7.rel.zh.gpt-6-astra.rel1}} |
| | rel3 | {{v:E7.rel.en.gpt-6-astra.rel3}} | {{v:E7.rel.es.gpt-6-astra.rel3}} | {{v:E7.rel.ko.gpt-6-astra.rel3}} | {{v:E7.rel.zh.gpt-6-astra.rel3}} |
| | recognised (of 88) | {{v:E7.rec.en.gpt-6-astra}} | {{v:E7.rec.es.gpt-6-astra}} | {{v:E7.rec.ko.gpt-6-astra}} | {{v:E7.rec.zh.gpt-6-astra}} |
| Gemini 4 Argon | rel1 | {{v:E7.rel.en.gemini-4-argon.rel1}} | {{v:E7.rel.es.gemini-4-argon.rel1}} | {{v:E7.rel.ko.gemini-4-argon.rel1}} | {{v:E7.rel.zh.gemini-4-argon.rel1}} |
| | rel3 | {{v:E7.rel.en.gemini-4-argon.rel3}} | {{v:E7.rel.es.gemini-4-argon.rel3}} | {{v:E7.rel.ko.gemini-4-argon.rel3}} | {{v:E7.rel.zh.gemini-4-argon.rel3}} |
| | recognised (of 88) | {{v:E7.rec.en.gemini-4-argon}} | {{v:E7.rec.es.gemini-4-argon}} | {{v:E7.rec.ko.gemini-4-argon}} | {{v:E7.rec.zh.gemini-4-argon}} |

: Run-to-run reliability of recall Presence and recognition of the 88 yes/no brands (`data/v62_planned_items_v0_62.json`, `2.9_descriptives`).

**Answer form and the language factor.** The measured language factor is the mean recorded cost per answered call in the language over the same in English (t₄'s answers to the same questions without search); "pooled" sums the three models' means. Pre-registration §6.2 planned the budget with central factors applied to the whole per-call cost. Every pooled factor is below its central planning factor; individual models were above it in a few cells (GPT-6 Astra on Spanish category questions, Gemini 4 Argon on Spanish yes/no questions).

| Language | Claude Fable 5.2 | GPT-6 Astra | Gemini 4 Argon | Pooled, category | Pooled, yes/no | §6.2 central (high) |
|---|---:|---:|---:|---:|---:|---:|
| Spanish | {{v:E7.lf.es.claude-fable-5-2.B}} | {{v:E7.lf.es.gpt-6-astra.B}} | {{v:E7.lf.es.gemini-4-argon.B}} | {{v:E7.lf.es.pooled.B}} | {{v:E7.lf.es.pooled.A}} | {{v:E7.lf.es.plan}} ({{v:E7.lf.es.plan_high}}) |
| Korean | {{v:E7.lf.ko.claude-fable-5-2.B}} | {{v:E7.lf.ko.gpt-6-astra.B}} | {{v:E7.lf.ko.gemini-4-argon.B}} | {{v:E7.lf.ko.pooled.B}} | {{v:E7.lf.ko.pooled.A}} | {{v:E7.lf.ko.plan}} ({{v:E7.lf.ko.plan_high}}) |
| Chinese | {{v:E7.lf.zh.claude-fable-5-2.B}} | {{v:E7.lf.zh.gpt-6-astra.B}} | {{v:E7.lf.zh.gemini-4-argon.B}} | {{v:E7.lf.zh.pooled.B}} | {{v:E7.lf.zh.pooled.A}} | {{v:E7.lf.zh.plan}} ({{v:E7.lf.zh.plan_high}}) |

: Measured cost factor per answered call relative to English (per-model columns: category questions) against the planning factors of pre-registration §6.2.

| Model | English (t₄) | Spanish | Korean | Chinese |
|---|---|---|---|---|
| Claude Fable 5.2 | {{v:E7.form.en.claude-fable-5-2.chars}}; {{v:E7.form.en.claude-fable-5-2.brands}} | {{v:E7.form.es.claude-fable-5-2.chars}}; {{v:E7.form.es.claude-fable-5-2.brands}} | {{v:E7.form.ko.claude-fable-5-2.chars}}; {{v:E7.form.ko.claude-fable-5-2.brands}} | {{v:E7.form.zh.claude-fable-5-2.chars}}; {{v:E7.form.zh.claude-fable-5-2.brands}} |
| GPT-6 Astra | {{v:E7.form.en.gpt-6-astra.chars}}; {{v:E7.form.en.gpt-6-astra.brands}} | {{v:E7.form.es.gpt-6-astra.chars}}; {{v:E7.form.es.gpt-6-astra.brands}} | {{v:E7.form.ko.gpt-6-astra.chars}}; {{v:E7.form.ko.gpt-6-astra.brands}} | {{v:E7.form.zh.gpt-6-astra.chars}}; {{v:E7.form.zh.gpt-6-astra.brands}} |
| Gemini 4 Argon | {{v:E7.form.en.gemini-4-argon.chars}}; {{v:E7.form.en.gemini-4-argon.brands}} | {{v:E7.form.es.gemini-4-argon.chars}}; {{v:E7.form.es.gemini-4-argon.brands}} | {{v:E7.form.ko.gemini-4-argon.chars}}; {{v:E7.form.ko.gemini-4-argon.brands}} | {{v:E7.form.zh.gemini-4-argon.chars}}; {{v:E7.form.zh.gemini-4-argon.brands}} |

: Answer form of the category answers: mean characters per answer; mean registry brands named per answer. Characters are not comparable across scripts (a Hangul syllable or a Han character carries more than a Latin letter). Finish reasons: {{v:E7.mc.trunc.reasons}} only; {{v:E7.form.refusals}} refusals.

**Script of brand mentions.** For each brand mention coded in a Korean or Chinese category answer, the script descriptive asks whether it would also be coded without any alias (Latin form) and whether an alias form occurs. Korean: {{v:E7.script.ko.mentions}} mentions, {{v:E7.script.ko.latin_only}} in Latin script only, {{v:E7.script.ko.native_only}} in Hangul only and {{v:E7.script.ko.both}} in both ({{v:E7.script.ko.share_with_latin_form}} with a Latin form, {{v:E7.script.ko.share_with_native_form}} with a Hangul form). Chinese: {{v:E7.script.zh.mentions}} mentions, {{v:E7.script.zh.latin_only}} Latin only, {{v:E7.script.zh.native_only}} Han only and {{v:E7.script.zh.both}} both ({{v:E7.script.zh.share_with_latin_form}} with a Latin form, {{v:E7.script.zh.share_with_native_form}} with a Han form).

**Cost per model and language** (recorded usage): Spanish Claude Fable 5.2 {{v:E7.cost.es.claude-fable-5-2}}, GPT-6 Astra {{v:E7.cost.es.gpt-6-astra}}, Gemini 4 Argon {{v:E7.cost.es.gemini-4-argon}}; Korean {{v:E7.cost.ko.claude-fable-5-2}}, {{v:E7.cost.ko.gpt-6-astra}}, {{v:E7.cost.ko.gemini-4-argon}}; Chinese {{v:E7.cost.zh.claude-fable-5-2}}, {{v:E7.cost.zh.gpt-6-astra}}, {{v:E7.cost.zh.gemini-4-argon}} (same model order); total {{v:E7.cost.total}}. Strict §6.5 pricing of the one timed-out attempt would add {{v:cost.worst_case}} to Korean Gemini 4 Argon (§3.1, Entry 8).

## A.5 Items not computed {-}

**Home-language descriptive (§2.9 item 5): {{v:E7.home.status}}.** It requires a country-of-origin column built from cited sources before the lock. No such column was built: it is not among the files of the lock manifest, and no v0.62 file holds it. Building it after scoring would not meet the pre-registered condition, so the descriptive is not reported.

**Benchmark for time (§2.7): {{v:E7.time.status}}.** It needs the English t₅ wave, which had not been scored before v0.62; until it is, time and language are not separated (limitation 5).

