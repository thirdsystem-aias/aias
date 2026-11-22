---
title: "Sentiment in AI Answers about Brands"
subtitle: "Sentiment Paper A: the locked judging rule halted, the pre-registered successor rule was scored once, and the score failed its separability gate against Presence (AIAS™ Methodology v1.11, scored under v1.20)"
date: "{{PAPER_DATE}}"
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
  \usepackage{longtable}
  \renewcommand{\textfraction}{0.07}
  \renewcommand{\floatpagefraction}{0.8}
  \makeatletter\setlength{\@fptop}{0pt}\setlength{\@fpsep}{14pt}\makeatother
---

\begin{titlepage}
\setstretch{1.0}
\setlength{\parskip}{0pt}
\begin{center}

{\LARGE \textbf{Sentiment in AI Answers about Brands}}\\[8pt]

{\large Sentiment Paper A: the Locked Judging Rule Halted, the Pre-Registered Successor Rule\\ Was Scored Once, and the Score Failed Its Separability Gate against Presence\\ (AIAS™ Methodology v1.11, scored under v1.20)}\\[28pt]

Pablo Ulpiano González Castro\\[4pt]
School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System™ (research entity; data archive and methodology venue)\\[8pt]
Correspondence: pablou@pablou.com · pablou.com\\
ORCID: \href{https://orcid.org/0009-0003-8968-9990}{0009-0003-8968-9990}\\[20pt]

Pre-registrations: \texttt{{{V111_TAG}}} (commit \texttt{{{V111_COMMIT}}}, {{V111_DATE}}) and its successor rule\\ \texttt{{{PREREG_TAG}}} (commit \texttt{{{PREREG_COMMIT}}}, {{PREREG_DATE}}); both deposited on OSF before the first judge call\\
Data and code: OSF \texttt{ec6wh}, \texttt{methodology/v1\_11} and \texttt{methodology/v1\_20}\\
{% if SYNTHETIC %}
\vspace{14pt}\textbf{SYNTHETIC TEST BUILD: every number in this document comes from synthetic files. Not results.}\\
{% endif %}

\end{center}
\end{titlepage}

# Abstract {-}

Presence records whether AI answers name a brand, and Consistency how evenly the models of a panel do so; neither records how the answers describe the brand. This pre-registered study (AIAS Methodology v1.11) specifies an AI-judged valence instrument and tests whether the resulting Sentiment score is a separate component. Archived answers were re-analysed without new collection: {{UNITS_J1}} units from open recognition answers, five omnibus categories at three waves and eight early category studies, rated on a five-point anchored scale by a primary judge (Claude Opus 5.5) and, for {{UNITS_J2}} of them, by a second judge from another provider (GPT-6.1 Sol), in {{RECORDS}} batch calls at a recorded spend of {{SPEND}}. **The study's own locked rule halted it.** v1.11 accepted a judge reply only if the whole reply was one JSON object. Replies of the primary judge failed that rule often enough to need {{RETRIES}} retries, and after two identical retries {{V111_FAIL}} of {{UNITS_J1}} units were judge failures, above the pre-registered 2% halt in {{V111_HALT_N}} of {{J1_SETS}} sets; under v1.11's rule there are no Sentiment scores. A successor rule, pre-registered and locked before any v1.11 reply existed (v1.20: a reply counts when it holds exactly one complete JSON object that passes v1.11's checks), was then applied once to the same stored replies, with every other rule, seed and threshold v1.11's: {{V120_FAIL}} judge failures. Under it, judge agreement was ordinal Krippendorff's $\alpha$ = {{H1_ALPHA}} on units and a within-category rank correlation of {{H1_BRHO}} on brand scores (instrument gate H1: {{V_H1}}); stability over three weeks and five months was {{H4_RHO}} and {{H6_RHO}} (H4: {{V_H4}}; H6: {{V_H6}}); separability from Consistency was H3: {{V_H3}}.
{% switch CASE_OVERALL %}
{% case NOT_SEPARABLE %}
Within category, the correlation of Sentiment with Presence was {{H2_T1}}, {{H2_T2}} and {{H2_T3}} at the three waves, {{H2_FALS_SHORT}} (H2: {{V_H2}}); against Ranking, H5 was {{V_H5}}. {{ABS_SENS}} Sentiment, as measured here, failed its Paper A separability gate: it is reported, not carried into a release.
{% case SEPARABLE|SEPARABLE_FLAGGED|MIXED|INSTRUMENT_FAILED|UNSTABLE|INSTRUMENT_UNDETERMINED %}
Separability from Presence was H2: {{V_H2}}, and from Ranking H5: {{V_H5}}. {{ABS_SENS}}
{% endswitch %}
It remains provisional until human labels (Paper B) validate the judge.

**Keywords:** AI availability; brand sentiment; large language models; LLM-as-judge; inter-rater agreement; pre-registration; successor rule; measurement validity

\clearpage

# 1. Introduction

AI Availability --- the discoverability and representation of a brand in the outputs of large language models (LLMs) --- has been proposed as a third layer of brand availability (González Castro, 2026a) beside the Mental and Physical Availability of the Ehrenberg-Bass tradition (Sharp, 2010; Sharp & Romaniuk, 2021), within the Tri-System framework (González Castro, 2026l). The AIAS™ programme builds the components of an AI availability score one at a time, each pre-registered and locked before it is used, on the Presence measurement protocol (González Castro, 2026b, 2026c, 2026d, 2026e). Presence is whether and how often models name a brand (Methodology v1.6: González Castro, 2026f), anchored across five categories in AIAS 1.0 (González Castro, 2026j). Consistency is how evenly the models of a panel name it: the first Consistency instrument failed its separability test because it moved with how often a brand is named (v1.7: González Castro, 2026g); its replacement measures the dispersion statistic $\varphi$ (v1.8: González Castro, 2026h), scaled to $C^*$ (v1.9: González Castro, 2026i). The AIAS 2.0 synthesis showed Consistency separable from Presence (González Castro, 2026k).

Being named is not the same as being described well. An answer can name a brand and recommend it, name it and warn against it, or name it in a list without comment. This paper specifies a Sentiment instrument for the valence of what answers say and asks, in the order the pre-registration fixes: is the instrument reliable enough to be read at all (judge agreement, H1; stability over weeks and months, H4, H6)? Is Sentiment a separate component, moving independently of Presence, Consistency and Ranking within category (H2, H3, H5), of how often a brand is named in the early categories (H7) and, on a floor-free recognition score, of Presence (H8)? And does the primary judge favour answers written by its own provider's models (H9)? The v1.7 lesson shapes the design: an instrument that rises with how often a brand is named reproduces Presence under another name, and Sentiment carries that risk in a specific form, because brands named often may be named in recommendation frames, which read as warm.

The paper also reports a failure of the study's own procedure, with the same prominence as its scores. v1.11 locked a strict rule for the judges' JSON replies. A sister study run first on newer answers (v1.15) halted under that rule because the primary judge put a short sentence before an otherwise complete reply, and the same was likely for v1.11, whose locked text gave no lever. Before v1.11's first judge call, a second pre-registration (v1.20) fixed a successor rule that changes only which replies count, and declared in advance that if v1.11 halted on judge failures its verdicts would be Sentiment Paper A's result. v1.11 did halt. Section 3.2 reports the halt; the scores and verdicts that follow are v1.20's.

The score is AI-judged. Judging valence with a model is a measurement choice, not a finding: the judge is itself an instrument that needs validation. Sentiment is called provisional throughout; a companion study (Paper B) collects human labels on a pre-drawn sample of the same units under its own pre-registration.

# 2. Method

The method is v1.11's locked pre-registration, summarised here (section numbers in parentheses refer to it), with one rule replaced by its locked successor, v1.20 (§2.10).

## 2.1 Data

The study re-analyses archived answers; no answer was collected for it (§2). Three blocks enter. Block R holds the open recognition answers of the v0.23 premium-spirits study ("what do you know about X"): 24 brands, six models of the legacy panel (Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o mini, Gemini 2.5 Flash and Gemini 2.5 Flash-Lite), three waves ($t_1$ May 20--26, $t_2$ June 10 and $t_3$ November 9, 2026), 432 answers. Block F holds the omnibus category answers of the five categories that carry Presence and Consistency (v0.19 audiophile headphones, v0.20 skincare, v0.21 cosmetics, v0.22 automotive, v0.23 premium spirits; 112 brand units), the same legacy panel and waves, 540 answers. Block E holds the eight early category studies (project management software, personal finance apps, olive oil, running shoes and facial skincare from v0.9; household retail and kitchen knives from v1.0; premium tea from v0.14), answered by a second six-model panel (Claude Sonnet 4.6, Claude Opus 4.7, GPT-5.4 mini, GPT-5.5, Gemini 2.5 Flash, Grok 4.1 Fast), 288 answers each, 2,304 in all. An input manifest pins every file by git blob and SHA-256; the scorer stops on any difference. The programme's held studies, a technology panel pending its own conflict-of-interest screen, truncated recognition probes, yes/no probes and superseded or duplicate files are excluded for reasons fixed before the lock; three small sets formed a development sample used only to count windows before the lock (§2, §3).

## 2.2 Units and mention windows

A recognition answer is one unit. In blocks F and E the unit is a mention window: one per answer and registry brand that the answer names (§4.1). Which brands an omnibus answer names is the programme's certified mention record, so the number of F windows equals the mention count behind Presence; in the early blocks it is v1.10's alias rule on the phase registries. The window is the brand block: every segment that names the brand, each followed by up to four continuation segments, stopping at a heading, a list label or a segment naming another registry brand, capped at 1,500 characters. At most 36 windows are judged per brand, answer set and wave (seeded, round-robin over models), which limits cost only in the early sets. The unit build of 10 November 2026 gave 7,578 judged units: 432 recognition answers, 2,781 omnibus windows and 4,365 early windows (of 13,463 before the cap); it found no extraction miss.

## 2.3 Judges

The primary judge J1 is Claude Opus 5.5 (`claude-opus-5-5`, Anthropic Message Batches API); the reliability judge J2 is GPT-6.1 Sol (`gpt-6.1-sol`, OpenAI Batch API); Gemini 4 Argon is the alternate, used only if a judge cannot be (§4.2). Neither judge is its provider's flagship; the tier is a budget choice whose adequacy H1 and Paper B test. Every judge receives the same prompt, with explicit anchors, and returns JSON with five keys: a valence on $-2 \ldots +2$, whether the text refers to the target brand, whether it is evaluative, whether it is mixed, and an evidence quote of at most 20 words. Being named, listed or recommended by inclusion is not evaluation; plain facts are neutral; reported third-party judgements (awards, ratings, recalls, controversies) are (§4.3). No sampling parameter is sent; reasoning runs at the lowest documented effort ("low"); output is capped at 4,096 tokens. The judge sees the brand, the category, the question, the text type and the text, never the answering model, wave, answer set or any Presence, Consistency or Ranking value. An invalid reply is retried twice with identical input; after three invalid replies the unit is JUDGE_FAIL; above 2% of a set's units per judge the study halts before scoring (§4.2; which replies count is §2.10). J1 judges every unit; J2 judges every R and F unit and a seeded 10% stratified sample of the early windows (3,650 units). A fixed 5% sample (379 units) is judged a second time by each judge to measure call-to-call variation; exact agreement below 0.90 is flagged, not halted.

## 2.4 The Sentiment score

A unit's score is $u = 25\,(v + 2) \in \{0, 25, 50, 75, 100\}$ for valence $v$. Non-evaluative units score 50 and stay in the score: a neutral description is an outcome, not missing data. Units that do not refer to the brand are excluded and counted. The Sentiment score of a brand in an answer set and wave is $S = $ the mean of $u$ over its valid units, computed on J1's outputs, and rated only with at least six valid units, without shrinkage: the rule mirrors $C^*$, and shrinkage toward a midpoint by mention count tied a component to Presence in v1.9 (§4.4). The AIAS Sentiment score is the long-form S (block F for the omnibus categories, block E for the early ones); the recognition score $S_{\text{rec}}$ (block R) is a second elicitation used for a floor-free check.

## 2.5 Comparators

Presence is v1.6's $P = 100 \cdot \tfrac{1}{3}(C_P/6 + 2\hat\pi)$ with $\hat\pi$ the recall mentions over 36; Consistency is v1.9's $C^* = 100\,(1 - \varphi/7.2)$, rated with at least six mentions. Both are read from the AIAS 2.0 profile table (112 units × 3 waves), the file the Ranking paper uses, and opened only after H1 is written. Ranking $R^*$ is the statistic v1.10 selected at its Stage S, the mean normalised position (MNP), computed with v1.10's own locked code and extractor; every regenerated rank table must equal v1.10's, and $R^*$ is computed only after v1.10's own verdicts exist (§5).

## 2.6 Statistics

Rank associations are pooled within-category Spearman correlations $\rho_w$: average ranks are computed within each category and centred on the category's mean rank, and $\rho_w$ is the Pearson correlation of the pooled centred ranks (v1.10's implementation). A category enters a pooled statistic only with at least four units; a statistic is UNDETERMINED with fewer than 20 units pooled or fewer than three categories (H8, one category by design: at least 20 units). Separability bands are the programme's: $\lvert\rho\rvert \le 0.30$ confirmed separable, $\lvert\rho\rvert \ge 0.50$ falsified, marginal between. The omnibus separability tests use v1.10's locked three-wave rule: UNDETERMINED if fewer than two of $t_1$, $t_2$, $t_3$ are determined; otherwise FALSIFIED if $\lvert\rho\rvert \ge 0.50$ at any determined wave, CONFIRMED if $\lvert\rho\rvert \le 0.30$ at every determined wave, MARGINAL otherwise. Every $\rho$ carries a 95% bootstrap interval (units resampled within category, 10,000 draws); verdicts use the unrounded point estimate. Stability is tested with a one-sided stratified permutation test (later-wave scores permuted within category, 10,000 draws; $p = (\text{hits} + 1)/(N + 1)$). Judge agreement uses Krippendorff's ordinal $\alpha$ (Krippendorff, 2004) over every unit with valid outputs from both judges. **Noise guard:** if H1 or H4 is FALSIFIED, H2, H3, H5, H7 and H8 are reported as UNDETERMINED, because a noisy instrument is separable from everything.

## 2.7 Hypotheses

Table: Pre-registered hypotheses and decision rules (v1.11 §5; v1.20 adds none). MARGINAL otherwise in every row; UNDETERMINED as in §2.6.

| | Tier | Test | CONFIRMED iff | FALSIFIED iff |
|:----|:----------|:----------------------------------------------|:------------------|:------------------|
| H1 | Primary (gate) | Judge agreement: ordinal $\alpha$, J1 vs J2; brand $\rho_w(S_{J1}, S_{J2})$, F units, waves pooled | $\alpha \ge 0.667$ and $\rho \ge 0.80$ | $\alpha < 0.50$ or $\rho < 0.60$ |
| H2 | Primary | Separable from Presence: $\lvert\rho_w(S, P)\rvert$ per wave | three-wave rule $\le 0.30$ | three-wave rule $\ge 0.50$ |
| H3 | Primary | Separable from Consistency: $\lvert\rho_w(S, C^*)\rvert$ per wave | three-wave rule $\le 0.30$ | three-wave rule $\ge 0.50$ |
| H4 | Primary | Short-term stability: $\rho_w(S_{t_1}, S_{t_2})$, one-sided permutation | $\rho \ge 0.50$ and $p < .05$ | $\rho < 0.30$ or $p \ge .05$ |
| H5 | Primary | Separable from Ranking: $\lvert\rho_w(S, R^*)\rvert$ per wave | three-wave rule $\le 0.30$ | three-wave rule $\ge 0.50$ |
| H6 | Secondary | Long-term stability: $\rho_w(S_{t_2}, S_{t_3})$ | $\rho \ge 0.50$ and $p < .05$ | $\rho < 0.30$ or $p \ge .05$ |
| H7 | Secondary | Early categories: $\lvert\rho_w(S, n_{\text{named}})\rvert$ | $\le 0.30$ | $\ge 0.50$ |
| H8 | Secondary | Recognition score: $\lvert\rho(S_{\text{rec}}, P)\rvert$ per wave | three-wave rule $\le 0.30$ | three-wave rule $\ge 0.50$ |
| H9 | Secondary | Self-preference: $\Delta$ of mean $u_{J1} - u_{J2}$, J1-provider answers minus others | $\lvert\Delta\rvert \le 5$ points | $\lvert\Delta\rvert \ge 10$ points |

H1 is the instrument gate; H1 and the separability tests H2, H3 and H5 decide whether Sentiment passes its Paper A gate (v1.20 §7). H4 is a reliability floor, not a claim that Sentiment is fixed; H6 allows real change over five months. As a secondary row of H5, $\lvert\rho_w(S, R^*)\rvert$ is also reported within the eight early categories (band verdict).

## 2.8 Sensitivity analyses and descriptives

Sensitivity analyses are reported next to the verdicts and never change one. From v1.11 (§5.1): SU, every pooled statistic with the uncentred rank convention of the earlier programme papers; SD, every gate statistic without the Denon units of v0.19 (Declarations); NV in place of S, a model-balanced S and a J2-scored S, each for H2 and H3; $\alpha$ over the units both judges say refer to the brand. From v1.20 (§4, §8), each recomputing H1--H9 on one unit filter: **S-ATT**, every unit judged from the attempt v1.11's own rule would score where v1.11's rule yields a judgement, and from the v1.20 rule only where it does not; **S-CUT**, without the units whose answer is known or likely to have ended at the answering model's output limit (a list built before the lock from recorded finish reasons, recorded token counts and, for {{CUT_INFERRED}} answers, byte-identical text with a cut answer; {{CUT_ANSWERS}} answers); **S-CUT-M**, without every unit of the model × block × category cells in which at least half of the $t_3$ answers ended at the limit, at every wave ({{CUT_M_CELLS}} cells). In S-CUT and S-CUT-M the recognition floor is four valid units instead of six, because every recognition brand loses its Gemini 2.5 Flash answer at $t_3$. Pre-specified descriptives (v1.11 §6): the cross-category baseline; the convergence of $S_{\text{rec}}$ with the omnibus S in premium spirits; mean unit score by answering model, frame and panel; agreement detail; and, as an exploratory row only, the agreement of J1's valence sign with archived per-brand labels written by a 2026 extraction model in five early sets.

## 2.9 Run, budget and order of analysis

Paid model calls were capped at US\$100 in total, enforced before every batch from the worst case of each request, with a pause at US\$80 (v1.11 §7). A binding projection made after the first calls of each judge decided, from token counts only, whether four pre-registered reductions of the early block applied. Batches could not be submitted before 22 November 2026, 06:00 UTC, nor while another programme collection ran (§8). Analysis runs in two stages: Stage J computes judge agreement (H1) and the self-consistency check from the frozen judge outputs without reading any Presence, Consistency or Ranking value; Stage C then opens them and computes H2--H9, the sensitivities and the descriptives. Each stage runs once, refuses to run without the pushed tag and its anchor record, and refuses to start before the stage that must precede it.

## 2.10 The reply rule: v1.11 and its pre-registered successor v1.20

**v1.11's rule** (§4.2) accepts a reply only if the whole reply is one JSON object (a code fence is stripped only when the reply begins with one) with exactly the five keys, the right types and consistent flags. **Why a successor.** v1.15, which ran v1.11's instrument unchanged on newer answers on 12 November 2026, halted at its Stage J: the primary judge put a short sentence before a complete JSON object on some first tries, identical retries did not remove it, and one set passed 2% (v1.15 DEVIATIONS Entry 2). Every failed reply still held a complete object with the five keys. v1.11 used the same judges, prompt and rule and was likely to halt the same way; its locked text gave no lever, and a locked pre-registration never changes. **v1.20** (locked at tag `{{PREREG_TAG}}` on {{PREREG_DATE}}, before the first v1.11 judge batch was allowed, on 22 November 2026 at 06:00 UTC) re-scores v1.11's own stored replies under one changed rule: *a reply counts when it holds exactly one complete JSON object and that object passes v1.11's checks; any text around it, code fences included, is ignored.* Zero objects, two or more objects (identical copies included), an empty reply, a served-model mismatch and a reply whose recorded finish reason shows the output cap stay invalid. For each unit the first stored reply that counts is its judgement (v1.11's own choice is sensitivity S-ATT). Nothing is re-sent and no model is called (US\$0); every other rule, statistic, seed and threshold is v1.11's, run with v1.11's code, whose files v1.20 checks against v1.11's lock manifest. The rule was written after seeing the *format* of v1.15's replies, never a valence, and before any v1.11 reply existed; it removes a failure of format, not of content.

**Which result counts** (v1.20 §7, decided before the lock). v1.11 runs first, in full, under its own rule. If it completes, v1.11 is the confirmatory record and v1.20 a re-scoring beside it. If v1.11's Stage J halts on judge failures (case B), v1.11's record is the halt, reported with the same prominence as the scores, and **v1.20's verdicts are Sentiment Paper A's result**. The case is not chosen after the fact: v1.20's scorer recomputes v1.11's own outcome and failure check on the frozen records and writes the case and the role of its verdicts into its outputs.

## 2.11 Pre-registrations and deviations

v1.11 was locked at tag `{{V111_TAG}}` ({{V111_DATE}}) and v1.20 at tag `{{PREREG_TAG}}` ({{PREREG_DATE}}); each was deposited on OSF with an anchor record naming the tag's commit before v1.11's first judge call. {{DEV_SENTENCE}} Predictions written before any judge call (v1.11 §10): H1 marginal to confirmed, H2 marginal, H3 confirmed, H4 marginal, H8 confirmed. v1.20 added one prediction, about the rule itself: J1 JUDGE_FAIL below 0.5% in every set under the v1.20 rule (v1.20 §6).

# 3. Results

{% if SYNTHETIC %}
**Synthetic test build.** Every number and verdict in this section comes from synthetic files. They are not results.

{% endif %}
## 3.1 The judge run

The judge run took place on 22 November 2026, from {{RUN_FIRST}} to {{RUN_LAST}} UTC, entirely through the two vendors' batch services ({{BATCHES_J1}} J1 batches, {{BATCHES_J2}} J2 batches). It recorded {{RECORDS}} calls: {{REC_J1}} by J1 and {{REC_J2}} by J2, of which {{FIRST_TRIES}} were first tries of the main and repeat passes and {{RETRIES}} were retries after a reply v1.11's rule rejected (all by J1). No call ended in an API error ({{ERRORS}} records with an error or a status other than "ok"); every response was served by the requested model ({{SERVED_J1}} by `claude-opus-5-5`, {{SERVED_J2}} by `gpt-6.1-sol`), and none ended at the output cap (finish reasons: J1 "end_turn" {{FIN_J1}}, J2 "completed" {{FIN_J2}}). Recorded spend was {{SPEND}} (J1 {{SPEND_J1}}, J2 {{SPEND_J2}}; all at batch prices), under the US\$80 pause, so no approval was needed. The binding projection after {{CAL_J1}} calibration calls of J1 and {{CAL_J2}} of J2 measured {{OUT_J1}} and {{OUT_J2}} output tokens per call, reasoning included, and projected {{PLAN_USD}} with overhead; {{REDUCTION_SENTENCE}} {{REPLACEMENT_SENTENCE}} Reasoning tokens: J2 reported {{THINK_J2}} over its {{REC_J2}} calls; J1's records carry no separate reasoning count. The vendors' invoices are not part of the recorded outputs and have not been reconciled with the recorded spend here (v1.11 §7).

## 3.2 v1.11 under its own rule: Stage J halted

v1.11's Stage J ran once, on the frozen replies, at {{V111_STAGEJ_START}} UTC, and stopped before scoring (exit code {{V111_EXIT}}). Under v1.11's rule J1 had {{V111_FAIL}} JUDGE_FAIL units of {{UNITS_J1}} on the main pass ({{V111_FAIL_SHARE}}), and {{V111_REP_FAIL}} more on the repeat sample; J2 had {{V111_J2_FAIL}}. The share passed the 2% halt in {{V111_HALT_N}} of J1's {{J1_SETS}} sets: {{V111_HALT_DESC}} (Table 2, Figure 1); the highest share was {{V111_FAIL_MAX}} ({{V111_FAIL_MAX_SET}}). **Under v1.11's locked rule the study has no Sentiment score and no verdict on H1--H9.** This is v1.11's record (case B of v1.20 §7), as v1.15's halt is v1.15's.

Table: J1 JUDGE_FAIL per set on the main pass: units sent, JUDGE_FAIL under v1.11's rule and its share (halt above 2%), and JUDGE_FAIL under the v1.20 rule and under S-ATT. J2 had no JUDGE_FAIL in any set under any rule.

{{TABLE_HALT}}

![JUDGE_FAIL share of the primary judge per answer set, under the locked reply rule and the successor rule, against the 2% halt line. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_01_judge_fail_by_set.pdf){#fig:halt width=100%}

## 3.3 The successor rule v1.20 on the same replies

v1.20's Stage J then ran once on the same frozen records ({{V120_STAGEJ_UTC}} UTC). Under its rule J1 had {{V120_FAIL}} JUDGE_FAIL and {{V120_UNJ}} UNJUDGED units: all {{V111_FAIL}} units that failed under v1.11's rule became valid, as did the {{V111_REP_FAIL}} repeat-sample failures, and every unit valid under v1.11's rule stayed valid ({{TRANS_VV}} J1 main-pass units). For {{DIFF_ATTEMPT}} J1 main-pass units valid under both rules the judgement comes from an earlier attempt than the one v1.11's rule would score (an earlier reply that v1.11's rule rejected counts under the v1.20 rule); S-ATT reports the effect of scoring v1.11's attempt instead. J2's {{UNITS_J2}} units were valid under both rules. The highest JUDGE_FAIL share under the v1.20 rule was {{V120_FAIL_MAX}}, so v1.20's prediction (below 0.5% in every set) held, and Stage J passed its 2% check. Stage C then ran once ({{V120_STAGEC_UTC}} UTC). Everything below is v1.20's result, and, under case B, Sentiment Paper A's.

The omnibus units joined the Presence and Consistency table one to one at every wave{% if JOIN_PASS %}{% else %} (not passed: see the verdict file){% endif %}, and the number of omnibus windows differed from the Presence mention count in {{WINDOW_MISMATCH}} units. {{RANKING_SENTENCE}} v1.20's Stage C output does not carry the cross-check of Presence and $C^*$ against the v1.9 unit table that v1.11's Stage C writes (v1.11 §2), so that check is not reported here.

## 3.4 Judge agreement (H1) and self-consistency

Over {{H1_PAIRS}} units with valid outputs from both judges, ordinal $\alpha$ was {{H1_ALPHA}} ({{H1_ALPHA_REF}} over the units both judges said refer to the brand; recognition {{H1_ALPHA_R}}, omnibus {{H1_ALPHA_F}}, early sample {{H1_ALPHA_E}}), and Cohen's $\kappa$ on the evaluative flag was {{H1_KAPPA}}. Over {{H1_BRHO_N}} omnibus brand scores rated under both judges, the within-category brand correlation was {{H1_BRHO}} (95% CI {{H1_BRHO_LO}} to {{H1_BRHO_HI}}).
{% switch CASE_H1 %}
{% case CONFIRMED %}
Both statistics met the confirmed thresholds ($\alpha \ge 0.667$, $\rho \ge 0.80$): H1 is CONFIRMED, and the AI-judged instrument is read as reliable at the level the pre-registration requires.
{% case MARGINAL %}
Neither falsifying threshold was reached ($\alpha < 0.50$ or $\rho < 0.60$), but the confirmed thresholds were not both met: H1 is MARGINAL, and every verdict below carries that flag.
{% case FALSIFIED %}
At least one statistic fell below its falsifying threshold ($\alpha < 0.50$ or $\rho < 0.60$): H1 is FALSIFIED. The AI-judged instrument is reported as not reliable, and the noise guard applies.
{% case UNDETERMINED %}
The brand-level statistic did not meet its floor: H1 is UNDETERMINED, and no claim is made about the instrument's reliability.
{% endswitch %}
Under S-ATT, H1 is {{V_H1_SATT}} ($\alpha$ = {{H1_ALPHA_SATT}}, brand $\rho_w$ = {{H1_BRHO_SATT}}).

Figure 2 shows where the two judges' valences met and where they parted: {{CONF_SENTENCE}} Self-consistency (Table 3) measures each judge's call-to-call variation on the repeat sample: overall exact valence agreement was {{SC_J1_ALL}} for J1 and {{SC_J2_ALL}} for J2.{% if SC_ANY_FLAG %} At least one judge and block fell below the 0.90 flag; the flag is reported, not acted on.{% else %} No judge and block fell below the 0.90 flag.{% endif %}

![Valence from J1 (rows) and J2 (columns) on every unit with valid outputs from both judges. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_02_judge_confusion.pdf){#fig:confusion width=82%}

Table: Self-consistency: each judge's second judgement of the fixed repeat sample, against its first (exact valence agreement, ordinal $\alpha$, $\kappa$ on the evaluative flag).

{{TABLE_SELFCON}}

## 3.5 Separability from Presence, Consistency and Ranking (H2, H3, H5)

Table 4 gives the per-wave statistics; Figure 3 places them against the bands.
{% switch CASE_H2 %}
{% case CONFIRMED %}
Against Presence, $\lvert\rho_w\rvert$ stayed at or below 0.30 at every determined wave: H2 is CONFIRMED.
{% case MARGINAL %}
Against Presence, $\lvert\rho_w\rvert$ exceeded 0.30 at a determined wave without reaching 0.50 at any: H2 is MARGINAL.
{% case FALSIFIED %}
Against Presence, $\rho_w$ was {{H2_T1}} at $t_1$, {{H2_T2}} at $t_2$ and {{H2_T3}} at $t_3$ (unrounded values as the verdict uses them). {{H2_FALS_TEXT}} Under the three-wave rule one such wave is enough: H2 is FALSIFIED. {{H2_DIRECTION}}
{% case UNDETERMINED_GUARD %}
Against Presence, H2 is UNDETERMINED under the noise guard; its statistics are descriptive only.
{% case UNDETERMINED_WAVES %}
Against Presence, fewer than two waves met the floor: H2 is UNDETERMINED.
{% endswitch %}
{% switch CASE_H3 %}
{% case CONFIRMED %}
Against Consistency, $\lvert\rho_w\rvert$ stayed at or below 0.30 at every determined wave: H3 is CONFIRMED.
{% case MARGINAL %}
Against Consistency, $\lvert\rho_w\rvert$ exceeded 0.30 at a determined wave without reaching 0.50 at any: H3 is MARGINAL.
{% case FALSIFIED %}
Against Consistency, $\lvert\rho_w\rvert$ reached 0.50 at a determined wave: H3 is FALSIFIED.
{% case UNDETERMINED_GUARD %}
Against Consistency, H3 is UNDETERMINED under the noise guard; its statistics are descriptive only.
{% case UNDETERMINED_WAVES %}
Against Consistency, fewer than two waves met the floor: H3 is UNDETERMINED.
{% endswitch %}
{% switch CASE_H5 %}
{% case CONFIRMED %}
Against Ranking ($R^*$, MNP), $\lvert\rho_w\rvert$ stayed at or below 0.30 at every determined wave: H5 is CONFIRMED. In the early categories, $\rho_w(S, R^*)$ was {{H5E_RHO}} over {{H5E_N}} brands (band verdict {{H5E_V}}).
{% case MARGINAL %}
Against Ranking ($R^*$, MNP), $\lvert\rho_w\rvert$ exceeded 0.30 at {{H5_OVER}} without reaching 0.50 at any: H5 is MARGINAL. In the early categories, $\rho_w(S, R^*)$ was {{H5E_RHO}} over {{H5E_N}} brands (band verdict {{H5E_V}}).
{% case FALSIFIED %}
Against Ranking ($R^*$, MNP), $\lvert\rho_w\rvert$ reached 0.50 at a determined wave: H5 is FALSIFIED. In the early categories, $\rho_w(S, R^*)$ was {{H5E_RHO}} over {{H5E_N}} brands (band verdict {{H5E_V}}).
{% case UNDETERMINED_GUARD %}
Against Ranking, H5 is UNDETERMINED under the noise guard; its statistics are descriptive only.
{% case UNDETERMINED_WAVES %}
Against Ranking, fewer than two waves met the floor: H5 is UNDETERMINED.
{% case PENDING %}
H5 is PENDING: v1.10's own Stage C verdicts did not yet exist when this analysis ran.
{% case INACTIVE %}
H5 is INACTIVE: the scorer did not find tag `v1.10-prereg-r2`.
{% endswitch %}

Table: Separability: $\rho_w$ of the Sentiment score with each comparator per wave, with 95% bootstrap interval and number of brand units ("n.d." = below the floor). H8 uses the recognition score in premium spirits (one category, plain Spearman).

{{TABLE_SEP}}

![Within-category rank correlation of the Sentiment score with Presence, Consistency, Ranking and (recognition score) Presence, per wave, with 95% intervals and the separability bands. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_03_separability.pdf){#fig:sep width=100%}

## 3.6 Stability over three weeks and five months (H4, H6)

Over {{H4_N}} omnibus brand units rated at $t_1$ and $t_2$, $\rho_w$ was {{H4_RHO}} (95% CI {{H4_LO}} to {{H4_HI}}; permutation $p$ = {{H4_P}}).
{% switch CASE_H4 %}
{% case CONFIRMED %}
H4 is CONFIRMED: the score kept its brand order over three weeks.
{% case MARGINAL %}
The correlation was significant but below 0.50: H4 is MARGINAL.
{% case FALSIFIED_RHO %}
The correlation was below 0.30: H4 is FALSIFIED, and the noise guard applies.
{% case FALSIFIED_P %}
The permutation test did not reach $p < .05$: H4 is FALSIFIED, and the noise guard applies.
{% case UNDETERMINED %}
Too few units met the floor: H4 is UNDETERMINED.
{% endswitch %}
Over {{H6_N}} units rated at $t_2$ and $t_3$, $\rho_w$ was {{H6_RHO}} (95% CI {{H6_LO}} to {{H6_HI}}; $p$ = {{H6_P}}).
{% switch CASE_H6 %}
{% case CONFIRMED %}
H6 is CONFIRMED: the brand order held over five months.
{% case MARGINAL %}
H6 is MARGINAL: the order held in part over five months, a period over which real change is allowed.
{% case FALSIFIED_RHO %}
H6 is FALSIFIED by the size of the correlation; the pre-registration allows real change over five months.
{% case FALSIFIED_P %}
H6 is FALSIFIED by the permutation test; the pre-registration allows real change over five months.
{% case UNDETERMINED %}
Too few units met the floor: H6 is UNDETERMINED.
{% endswitch %}
{% if P_MIN %}Both permutation $p$ values are the smallest that {{N_PERM}} permutations can give.{% endif %}{% if GUARD_ON %} The noise guard applies.{% else %} Neither H1 nor H4 is FALSIFIED, so the noise guard does not apply.{% endif %}

![Rank correlation of each brand's Sentiment score between waves, with 95% intervals and the stability thresholds. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_04_stability.pdf){#fig:stab width=88%}

## 3.7 Secondary tests (H7, H8, H9)

In the eight early categories, the correlation of S with the number of answers naming the brand was {{H7_RHO}} (95% CI {{H7_LO}} to {{H7_HI}}; {{H7_N}} rated brands).
{% switch CASE_H7 %}
{% case CONFIRMED %}
H7 is CONFIRMED: in the early categories S did not track how often a brand is named.
{% case MARGINAL %}
H7 is MARGINAL.
{% case FALSIFIED %}
H7 is FALSIFIED: in the early categories, on a second answering panel and without the omnibus rating floor, S tracked how often a brand is named. {{H7_DIRECTION}}
{% case UNDETERMINED_GUARD %}
H7 is UNDETERMINED under the noise guard; the statistic is descriptive only.
{% case UNDETERMINED_FLOOR %}
Too few brands or categories met the floor: H7 is UNDETERMINED.
{% endswitch %}
{% switch CASE_H8 %}
{% case CONFIRMED %}
The floor-free recognition score was separable from Presence at every determined wave (Table 4): H8 is CONFIRMED.
{% case MARGINAL %}
The recognition score's correlation with Presence was {{H8_T1}}, {{H8_T2}} and {{H8_T3}} at the three waves (Table 4), above 0.30 at {{H8_OVER}} and below 0.50 at all: H8 is MARGINAL.
{% case FALSIFIED %}
The recognition score's correlation with Presence reached 0.50 at a determined wave (Table 4): H8 is FALSIFIED.
{% case UNDETERMINED_GUARD %}
H8 is UNDETERMINED under the noise guard (Table 4, descriptive only).
{% case UNDETERMINED_WAVES %}
Fewer than two waves met the floor of 20 recognition brands: H8 is UNDETERMINED.
{% endswitch %}

On recognition and omnibus units judged validly by both judges and referring to the brand, J1 scored answers by its own provider's models {{H9_OWN}} points relative to J2 ({{H9_N_OWN}} units) and other answers {{H9_OTHER}} points ({{H9_N_OTHER}} units): $\Delta$ = {{H9_DELTA}} points (Figure 5).
{% switch CASE_H9 %}
{% case CONFIRMED %}
$\lvert\Delta\rvert$ was at most 5 points: H9 is CONFIRMED, and no self-preference of the primary judge was found.{% if H9_NEG %} The sign runs the other way: relative to J2, J1 was slightly less generous to its own provider's answers than to the others.{% endif %}
{% case MARGINAL %}
$\lvert\Delta\rvert$ was between 5 and 10 points: H9 is MARGINAL.
{% case FALSIFIED %}
$\lvert\Delta\rvert$ reached 10 points: H9 is FALSIFIED, and S is also reported without J1-provider answers (§3.9).
{% case UNDETERMINED %}
One of the two groups had fewer than 20 units: H9 is UNDETERMINED.
{% endswitch %}

![Mean difference between the primary and the second judge's unit scores, for answers written by the primary judge's provider's models and for the other answers. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_05_self_preference.pdf){#fig:selfpref width=78%}

## 3.8 Verdicts

Table 5 lists every pre-registered test once, with the verdict as v1.20's scorer wrote it.{% if GUARD_ON %} The noise guard was applied: H1 or H4 was FALSIFIED.{% else %} The noise guard was not applied.{% endif %}{% if H1_FLAG %} Because H1 is MARGINAL, every verdict in the table carries that flag.{% endif %} Under v1.11's own rule no test has a verdict (§3.2).

Table: Verdicts of the pre-registered tests (scorer's words; v1.20 rule, Sentiment Paper A's result under case B).

{{TABLE_VERDICTS}}

## 3.9 Sensitivity analyses

{{SENS_SENTENCE}} Table 6 gives the verdicts under every sensitivity that recomputes the hypotheses; Table 7 gives H2's per-wave statistics under each of them, because H2 decides the gate.

Table: Verdicts under the sensitivity analyses (they never change a primary verdict). SU: uncentred ranks; SD: without Denon; S-ATT: v1.11's attempt where v1.11's rule yields a judgement; S-CUT: without answers known or likely cut at the output limit; S-CUT-M: without the cells mostly cut at $t_3$. "--": not recomputed by that sensitivity.

{{TABLE_SENS}}

Table: H2 (Sentiment against Presence) per wave under the primary analysis and each sensitivity: $\rho_w$ [95% CI] (brand units).

{{TABLE_H2_SENS}}

{{CUT_SENTENCE}}

## 3.10 Cross-category baseline (descriptive)

Figure 6 shows the median and interquartile range of the rated brands' Sentiment scores in each category, wave and block. Median S ranged from {{BASE_F_MIN}} to {{BASE_F_MAX}} across the omnibus categories and waves and from {{BASE_E_MIN}} to {{BASE_E_MAX}} across the early categories, on a scale where 50 is neutral. Mean unit score was {{PANEL_LEGACY}} on the legacy panel and {{PANEL_EARLY}} on the early panel. In premium spirits, the recognition score and the omnibus score correlated {{CONV_T1}}, {{CONV_T2}} and {{CONV_T3}} at $t_1$, $t_2$ and $t_3$ (brands rated in both: {{CONV_N1}}, {{CONV_N2}}, {{CONV_N3}}). The full baseline and the other pre-registered descriptives are in the appendix.

![Median and interquartile range of the rated brands' Sentiment scores per category, wave and block. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_06_baseline.pdf){#fig:base width=100%}

# 4. Discussion

**The procedure.** The study's own locked rule halted it, and the halt is a result. It is a result about a reply format, not about valence: every unit that failed under v1.11's rule had a stored reply holding exactly one complete object that passed v1.11's checks once the text around it was set aside, which is the one thing v1.20 changes. The successor was locked before any v1.11 reply existed, applied once, with v1.11's code for everything else, and its role in case B was fixed in advance; the programme's rule since v1.15 is that a pre-registration with an LLM judge states its extraction rule in advance and tests it on recorded replies. {{SATT_SENTENCE}}

{% switch CASE_OVERALL %}
{% case SEPARABLE %}
**The instrument and the gate.** Under the successor rule the instrument passed its reliability tests and was separable within category from the components already in the score.
{% case SEPARABLE_FLAGGED %}
**The instrument and the gate.** The separability tests came out as the programme requires, on an instrument whose two judges agreed only marginally; the verdicts carry that flag.
{% case NOT_SEPARABLE %}
**The instrument and the gate.** Under the successor rule the instrument is reliable at the level the pre-registration requires: two judges from different providers agreed (H1 {{V_H1}}), the score kept its brand order over three weeks and five months (H4 {{V_H4}}, H6 {{V_H6}}), and the primary judge showed no self-preference (H9 {{V_H9}}). It is also separable from Consistency (H3 {{V_H3}}). But it is not separable from Presence (H2 {{V_H2}}): within category, brands that the models name more often and more widely are described more warmly. The early categories, on another answering panel and without the omnibus rating floor, give H7 {{V_H7}} ({{H7_RHO}}), and against Ranking the score sits in the marginal band (H5 {{V_H5}}). Read with the v1.7 lesson, this is the outcome the gate exists to catch: part of what the Sentiment score records is how present a brand already is. A reliable instrument that re-measures an existing component adds no separate dimension to the composite, whatever its face validity.
{% case MIXED %}
**The instrument and the gate.** The primary tests did not all reach the confirmed band, and none of the primary separability tests was falsified.
{% case INSTRUMENT_FAILED %}
**The instrument and the gate.** The two judges did not agree well enough for the instrument to be read; the noise guard withdraws the separability statistics.
{% case UNSTABLE %}
**The instrument and the gate.** The score did not keep its brand order over three weeks; under the noise guard the separability statistics are descriptive only.
{% case INSTRUMENT_UNDETERMINED %}
**The instrument and the gate.** The instrument gate could not be determined on the units available.
{% endswitch %}

**How firm the Presence result is.** {{H2_FIRM}} {{CUT_DISCUSSION}} {{H2_ROBUST}} The rating floor of six units also restricts the range of Presence among rated omnibus brands, which can understate the association (v1.11 §11).

**What this does not show.** The judge is a model, and a systematic tilt shared by both judges would pass H1 unseen; whether the instrument's valence is valence as a human reader would judge it is Paper B's question. The answers were archived and written by panels that are not the newest models.

# 5. Programme consequence

Under the programme's plan, a component that fails its Paper A separability gate is reported and not shipped: Sentiment, as measured by this instrument, does not enter a release score, and no release number is attached to it. Two paths remain open, and this paper does not choose between them: a redesigned Sentiment instrument, which would need its own pre-registration; or reporting valence within Presence, as a description of how answers describe a brand, without a separate component claim. That choice is a later decision by the author. Paper B's human-label validation of the judge stands on its own and does not depend on it.

# 6. Limitations

The instrument is AI-judged and provisional until Paper B. The scores rest on a successor reply rule chosen after one study (v1.15) had shown how the judge fails; it was fixed before any v1.11 reply existed and changes only which replies count, but it is still a rule picked with knowledge of a failure mode, and a reply that argues one valence in prose and gives another in its object is scored on the object. The judges reason at their lowest available effort and no sampling parameter can be fixed, so a judge's output varies from call to call; the self-consistency check measures this variation, it does not remove it. The rating floor restricts the range of Presence among rated omnibus brands; H8 (floor-free) and H7 (early panel) are the checks. There is one judge pair, and self-preference is tested, not removed. The cut-answer sensitivities rely on recorded evidence that is missing for most $t_1$ and $t_2$ answers and for every early answer, and on one inference (identical text). The two answering panels are not the newest models, and the early categories have one wave each. S measures how answers describe brands, not consumer sentiment, and no behavioural validity is claimed. For budget reasons neither judge is its provider's flagship and J2 judged a 10% sample of the early windows.

# 7. Future Research

Paper B labels a 566-unit sample drawn at the unit build, before any judge call, with the judge's instructions verbatim and two independent student labellers per unit, under its own pre-registration whose validation thresholds are fixed before the labels are read. Whether a redesigned Sentiment instrument is pre-registered, or valence is reported within Presence, is open (§5).

# Declarations {-}

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance, at Samsung Electronics America. This study re-analyses answers collected against brand registries fixed in earlier phases; it performs no new brand selection, and each registry carries its source phase's conflict-of-interest handling forward unchanged (the source records are quoted verbatim in v1.11 DEVIATIONS Entry 0; v1.20 adds no brand, registry, unit or judge call). Two items of record apply. In the automotive registry (v0.22), Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands --- Harman International (audio systems), Samsung SDI (battery cells) and Samsung Display (infotainment) --- characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry (v0.19), AKG was substituted with Denon before the v0.19 pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary (v0.19 PRE_REGISTRATION §2.3; v0.19 paper, DEVIATIONS Entry 1). Correction (November 10, 2026): Harman International, a Samsung subsidiary since March 2017, completed its acquisition of Masimo's Sound United brands, Denon included, on September 23, 2025, so Denon, substituted for AKG before the v0.19 lock, was already a Samsung-group brand; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. Every gate statistic is therefore also reported without Denon (sensitivity SD). A string screen of all thirteen registries on November 10, 2026, for Samsung, Harman and the Harman and Sound United brand names listed in DEVIATIONS Entry 0, matched Denon (v0.19) only. Cheil Worldwide, a marketing company of the Samsung group in which Samsung Electronics holds 28.43%, or its agency Iris has done advertising, public-relations or search-marketing work for five registry brands: Chevrolet (for GM Korea, 2017), BMW (UK consumer public relations, 2018), Bentley (experiential agency of record in the Americas from 2021), Jack Daniel's (UK digital agency from 2022, since replaced) and Eucerin (search marketing for Beiersdorf from 2024) (conflict-of-interest screen of v0.62, DEVIATIONS Entry 0, Part F). These five brands stay in every analysis as locked. Valence judging adds no brand choice and is fully automated against the locked registries and units, and both pre-registrations were locked and deposited before any judge call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

## Funding {-}

Self-funded.

## Ethics {-}

Not applicable: no human subjects (archived AI answers judged by AI models). The Paper B human labelling is governed by Paper B's own pre-registration.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## Data and code availability {-}

Materials are deposited at OSF (osf.io/ec6wh). `methodology/v1_11/`: the locked pre-registration with its judge prompt, unit table, Paper B sample, parity, cost and precision records, the input manifest, the scorer and judge scripts with their tests, the lock manifest, the deviations record and the anchor record. `methodology/v1_20/`: the locked successor pre-registration, its configuration, scoping scripts and cut-answer list, dry-run record, deviations record and anchor record. After the run: the judge call records, batch log and plan (`methodology/v1_11/data/`), the frozen-output record and v1.11's Stage J console record (`methodology/v1_11/outputs/`), and v1.20's outputs with their console records (`methodology/v1_20/outputs/`: `stage_j_v1_20.json`, `unit_outcomes_v1_20.csv`, `comparison_v1_11_v1_20.json`, `v1_20_verdicts.json`). The code is in the programme's GitHub repository (github.com/thirdsystem-aias/aias) at tags `{{V111_TAG}}` and `{{PREREG_TAG}}`; this paper's builders and figure sources are added at publication.

# References {-}

González Castro, P. U. (2026a). *AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval*. SSRN 6659000.

González Castro, P. U. (2026b). *The AIAS™ Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy* (v1.2). SSRN 6761698.

González Castro, P. U. (2026c). *The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification (v1.3)*. SSRN 6797679.

González Castro, P. U. (2026d). *The AIAS Presence Measurement Protocol v1.4: Recognition × Recall Decomposition and Multi-Component AI Availability*. SSRN 6799479.

González Castro, P. U. (2026e). *The AIAS™ Presence Measurement Protocol: Multi-Statistic C2 Specification and Two-Channel Recall Decomposition* (v1.5). SSRN 6810758.

González Castro, P. U. (2026f). *Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension* (AIAS Methodology v1.6). SSRN 6816340.

González Castro, P. U. (2026g). *Consistency without Independence: A Pre-Registered Test of Coefficient-of-Variation as the Consistency Component of AIAS™* (v1.7). SSRN 6878818.

González Castro, P. U. (2026h). *A Mean-Independent Consistency Instrument for Cross-Model AI Presence: Redesigning CPC on a Quasi-Binomial Dispersion Basis* (AIAS Methodology v1.8). SSRN 6963359.

González Castro, P. U. (2026i). *One Score or Two? Calibrating a Presence and Consistency Composite for AI Brand Availability: A Pre-Registered Calibration with Blind Five-Month Confirmation (AIAS™ Methodology v1.9)*. Third System, <https://thirdsystem.ai/studies/v1-9/> (PDF: <https://thirdsystem.ai/files/papers/v1_9_ssrn_paper.pdf>); OSF, <https://osf.io/ec6wh/files/osfstorage/6af1fd459966c813ee53ba87>.

González Castro, P. U. (2026j). *AI Availability as a Third Measurable Layer of Brand Availability: Five-Substrate Empirical Anchoring of the AIAS™ Presence Measurement Protocol --- Synthesis under Locked v1.6 Methodology* (AIAS 1.0). SSRN 6817841.

González Castro, P. U. (2026k). *Presence and Consistency: A Two-Component Measurement of AI Availability. The AIAS™ 2.0 Synthesis*. OSF `ec6wh/aias_2_0`.

González Castro, P. U. (2026l). *Tri-System Brand Growth: Mental, Physical, and AI Availability in Brand Architecture*. MSI Working Paper, Report No. 26-132. Marketing Science Institute.

Krippendorff, K. (2004). *Content Analysis: An Introduction to Its Methodology* (2nd ed.). Sage.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

Sharp, B., & Romaniuk, J. (2021). *How Brands Grow Part 2: Including Emerging Markets, Services, Durables, New and Luxury Brands* (revised ed.). Oxford University Press.

Programme records cited by version (OSF `ec6wh`; github.com/thirdsystem-aias/aias): the pre-registrations of Methodology v1.10 (Ranking, tag `v1.10-prereg-r2`), v1.11 (Sentiment, tag `v1.11-prereg-r1`), v1.15 (Sentiment on $t_4$, with its DEVIATIONS Entry 2) and v1.20 (Sentiment successor rule, tag `v1.20-prereg-r1`); the conflict-of-interest screen of v0.62 (DEVIATIONS Entry 0, Part F); the omnibus registries of v0.19 (audiophile headphones, SSRN 6809182), v0.20 (skincare, SSRN 6811441), v0.21 (cosmetics, SSRN 6815378), v0.22 (automotive, SSRN 6829118) and v0.23 (premium spirits, SSRN 6834298). HARMAN press release, Business Wire, September 23, 2025, <https://www.businesswire.com/news/home/20250923135384/en/HARMAN-Completes-Sound-United-Acquisition-to-Expand-Premium-Audio-Leadership>.

\clearpage

# Appendix: pre-registered descriptives {-}

Table: Cross-category baseline (v1.11 §6.1): brands, brands rated, median and interquartile range of S, mean evaluative share E, and the shares of non-evaluative and mixed units and of units not referring to the brand, per block, category and wave.

{{TABLE_BASE}}

Table: Cross-category baseline, continued (v1.11 §6.1): judged units, J1's JUDGE_FAIL and UNJUDGED units under the v1.20 rule, the share of bare windows (the brand's segments carry fewer than four other words) and the extraction misses of the unit build, per block, category and wave.

{{TABLE_BASE2}}

Table: Ordinal $\alpha$ between J1 and J2 per block, and the variants of S for H2 and H3 (v1.11 §5.1): verdict and $\rho_w$ per wave.

{{TABLE_SENS_S}}

Table: Mean unit score by answering model and block (J1, valid units referring to the brand).

{{TABLE_MODEL}}

Table: Mean unit score by frame or prompt type and block (J1, valid units referring to the brand; frame identifiers as in the source studies).

{{TABLE_FRAME}}

Table: Units whose answer is in the cut-answer list (S-CUT) or in an S-CUT-M cell, per block, wave, category and answering model: units, judged, in J2's coverage and in the Paper B sample (v1.20 §8 item 4).

{{TABLE_CUT}}

The J1 × J2 confusion matrix of v1.11 §6.5 is Figure 2, which prints every count. {{LEGACY_SENTENCE}}
