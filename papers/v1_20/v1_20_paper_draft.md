---
title: "Sentiment in AI Answers about Brands"
subtitle: "Sentiment Paper A: the locked judging rule halted, the pre-registered successor rule was scored once, and the score failed its separability gate against Presence (AIAS™ Methodology v1.11, scored under v1.20)"
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

Pre-registrations: \texttt{v1.11-prereg-r1} (commit \texttt{62e2d38}, 10 November 2026) and its successor rule\\ \texttt{v1.20-prereg-r1} (commit \texttt{f2870d3}, 14 November 2026); both deposited on OSF before the first judge call\\
Data and code: OSF \texttt{ec6wh}, \texttt{methodology/v1\_11} and \texttt{methodology/v1\_20}\\

\end{center}
\end{titlepage}

# Abstract {-}

Presence records whether AI answers name a brand, and Consistency how evenly the models of a panel do so; neither records how the answers describe the brand. This pre-registered study (AIAS Methodology v1.11) specifies an AI-judged valence instrument and tests whether the resulting Sentiment score is a separate component. Archived answers were re-analysed without new collection: 7,578 units from open recognition answers, five omnibus categories at three waves and eight early category studies, rated on a five-point anchored scale by a primary judge (Claude Opus 5.5) and, for 3,650 of them, by a second judge from another provider (GPT-6.1 Sol), in 12,336 batch calls at a recorded spend of US\$33.93. **The study's own locked rule halted it.** v1.11 accepted a judge reply only if the whole reply was one JSON object. Replies of the primary judge failed that rule often enough to need 545 retries, and after two identical retries 155 of 7,578 units were judge failures, above the pre-registered 2% halt in 11 of 26 sets; under v1.11's rule there are no Sentiment scores. A successor rule, pre-registered and locked before any v1.11 reply existed (v1.20: a reply counts when it holds exactly one complete JSON object that passes v1.11's checks), was then applied once to the same stored replies, with every other rule, seed and threshold v1.11's: 0 judge failures. Under it, judge agreement was ordinal Krippendorff's $\alpha$ = 0.874 on units and a within-category rank correlation of 0.874 on brand scores (instrument gate H1: CONFIRMED); stability over three weeks and five months was 0.735 and 0.743 (H4: CONFIRMED; H6: CONFIRMED); separability from Consistency was H3: CONFIRMED.
Within category, the correlation of Sentiment with Presence was 0.4771, 0.4477 and 0.5013 at the three waves, reaching the falsifying 0.50 line at $t_3$ (H2: FALSIFIED); against Ranking, H5 was MARGINAL. In sensitivity analyses, without the answers that ended at the answering models' output limit (S-CUT, S-CUT-M), H2 is MARGINAL; under SU, H5 is FALSIFIED; under J2-scored S, H2 is MARGINAL; the primary verdicts stand. Sentiment, as measured here, failed its Paper A separability gate: it is reported, not carried into a release.
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

Sensitivity analyses are reported next to the verdicts and never change one. From v1.11 (§5.1): SU, every pooled statistic with the uncentred rank convention of the earlier programme papers; SD, every gate statistic without the Denon units of v0.19 (Declarations); NV in place of S, a model-balanced S and a J2-scored S, each for H2 and H3; $\alpha$ over the units both judges say refer to the brand. From v1.20 (§4, §8), each recomputing H1--H9 on one unit filter: **S-ATT**, every unit judged from the attempt v1.11's own rule would score where v1.11's rule yields a judgement, and from the v1.20 rule only where it does not; **S-CUT**, without the units whose answer is known or likely to have ended at the answering model's output limit (a list built before the lock from recorded finish reasons, recorded token counts and, for 8 answers, byte-identical text with a cut answer; 66 answers); **S-CUT-M**, without every unit of the model × block × category cells in which at least half of the $t_3$ answers ended at the limit, at every wave (4 cells). In S-CUT and S-CUT-M the recognition floor is four valid units instead of six, because every recognition brand loses its Gemini 2.5 Flash answer at $t_3$. Pre-specified descriptives (v1.11 §6): the cross-category baseline; the convergence of $S_{\text{rec}}$ with the omnibus S in premium spirits; mean unit score by answering model, frame and panel; agreement detail; and, as an exploratory row only, the agreement of J1's valence sign with archived per-brand labels written by a 2026 extraction model in five early sets.

## 2.9 Run, budget and order of analysis

Paid model calls were capped at US\$100 in total, enforced before every batch from the worst case of each request, with a pause at US\$80 (v1.11 §7). A binding projection made after the first calls of each judge decided, from token counts only, whether four pre-registered reductions of the early block applied. Batches could not be submitted before 22 November 2026, 06:00 UTC, nor while another programme collection ran (§8). Analysis runs in two stages: Stage J computes judge agreement (H1) and the self-consistency check from the frozen judge outputs without reading any Presence, Consistency or Ranking value; Stage C then opens them and computes H2--H9, the sensitivities and the descriptives. Each stage runs once, refuses to run without the pushed tag and its anchor record, and refuses to start before the stage that must precede it.

## 2.10 The reply rule: v1.11 and its pre-registered successor v1.20

**v1.11's rule** (§4.2) accepts a reply only if the whole reply is one JSON object (a code fence is stripped only when the reply begins with one) with exactly the five keys, the right types and consistent flags. **Why a successor.** v1.15, which ran v1.11's instrument unchanged on newer answers on 12 November 2026, halted at its Stage J: the primary judge put a short sentence before a complete JSON object on some first tries, identical retries did not remove it, and one set passed 2% (v1.15 DEVIATIONS Entry 2). Every failed reply still held a complete object with the five keys. v1.11 used the same judges, prompt and rule and was likely to halt the same way; its locked text gave no lever, and a locked pre-registration never changes. **v1.20** (locked at tag `v1.20-prereg-r1` on 14 November 2026, before the first v1.11 judge batch was allowed, on 22 November 2026 at 06:00 UTC) re-scores v1.11's own stored replies under one changed rule: *a reply counts when it holds exactly one complete JSON object and that object passes v1.11's checks; any text around it, code fences included, is ignored.* Zero objects, two or more objects (identical copies included), an empty reply, a served-model mismatch and a reply whose recorded finish reason shows the output cap stay invalid. For each unit the first stored reply that counts is its judgement (v1.11's own choice is sensitivity S-ATT). Nothing is re-sent and no model is called (US\$0); every other rule, statistic, seed and threshold is v1.11's, run with v1.11's code, whose files v1.20 checks against v1.11's lock manifest. The rule was written after seeing the *format* of v1.15's replies, never a valence, and before any v1.11 reply existed; it removes a failure of format, not of content.

**Which result counts** (v1.20 §7, decided before the lock). v1.11 runs first, in full, under its own rule. If it completes, v1.11 is the confirmatory record and v1.20 a re-scoring beside it. If v1.11's Stage J halts on judge failures (case B), v1.11's record is the halt, reported with the same prominence as the scores, and **v1.20's verdicts are Sentiment Paper A's result**. The case is not chosen after the fact: v1.20's scorer recomputes v1.11's own outcome and failure check on the frozen records and writes the case and the role of its verdicts into its outputs.

## 2.11 Pre-registrations and deviations

v1.11 was locked at tag `v1.11-prereg-r1` (10 November 2026) and v1.20 at tag `v1.20-prereg-r1` (14 November 2026); each was deposited on OSF with an anchor record naming the tag's commit before v1.11's first judge call. The deviations records (OSF `methodology/`) hold, for v1.11, Entries 0 and 1 (`v1_11/anchor/DEVIATIONS.md`: the conflict-of-interest screen, the Denon correction and the pre-lock record; the replacement of two Denon units in the Paper B sample) and Entry 2 in its post-lock continuation (`v1_11/postlock/`: the successor rule, recorded ex ante before the first judge call); and, for v1.20, Entries 0 and 1 (`v1_20/anchor/DEVIATIONS.md`, both ex ante, before its lock). No entry was made after a judge reply existed. Predictions written before any judge call (v1.11 §10): H1 marginal to confirmed, H2 marginal, H3 confirmed, H4 marginal, H8 confirmed. v1.20 added one prediction, about the rule itself: J1 JUDGE_FAIL below 0.5% in every set under the v1.20 rule (v1.20 §6).

# 3. Results

## 3.1 The judge run

The judge run took place on 22 November 2026, from 08:06 to 09:53 UTC, entirely through the two vendors' batch services (29 J1 batches, 11 J2 batches). It recorded 12,336 calls: 8,502 by J1 and 3,834 by J2, of which 11,791 were first tries of the main and repeat passes and 545 were retries after a reply v1.11's rule rejected (all by J1). No call ended in an API error (0 records with an error or a status other than "ok"); every response was served by the requested model (8,502 by `claude-opus-5-5`, 3,834 by `gpt-6.1-sol`), and none ended at the output cap (finish reasons: J1 "end_turn" 8,502, J2 "completed" 3,834). Recorded spend was US\$33.93 (J1 US\$29.62, J2 US\$4.31; all at batch prices), under the US\$80 pause, so no approval was needed. The binding projection after 209 calibration calls of J1 and 200 of J2 measured 81 and 43 output tokens per call, reasoning included, and projected US\$36.98 with overhead; no reduction of the early block applied. Neither judge was replaced by the alternate. Reasoning tokens: J2 reported 12,642 over its 3,834 calls; J1's records carry no separate reasoning count. The vendors' invoices are not part of the recorded outputs and have not been reconciled with the recorded spend here (v1.11 §7).

## 3.2 v1.11 under its own rule: Stage J halted

v1.11's Stage J ran once, on the frozen replies, at 2026-11-22 10:13 UTC, and stopped before scoring (exit code 2). Under v1.11's rule J1 had 155 JUDGE_FAIL units of 7,578 on the main pass (2.05%), and 7 more on the repeat sample; J2 had 0. The share passed the 2% halt in 11 of J1's 26 sets: all eight early sets, the omnibus automotive set at $t_1$, the omnibus headphones set at $t_3$ and the recognition spirits set at $t_1$ (Table 2, Figure 1); the highest share was 3.93% (early finance apps set). **Under v1.11's locked rule the study has no Sentiment score and no verdict on H1--H9.** This is v1.11's record (case B of v1.20 §7), as v1.15's halt is v1.15's.

Table: J1 JUDGE_FAIL per set on the main pass: units sent, JUDGE_FAIL under v1.11's rule and its share (halt above 2%), and JUDGE_FAIL under the v1.20 rule and under S-ATT. J2 had no JUDGE_FAIL in any set under any rule.

| Block | Category | Wave | Units | JUDGE_FAIL v1.11 | Share | Halt | JUDGE_FAIL v1.20 | S-ATT |
|:---------------|:----------------|:----|-----:|----------------:|-----:|:----|----------------:|-----:|
| Recognition | Spirits | t1 | 144 | 4 | 2.78% | yes | 0 | 0 |
| Recognition | Spirits | t2 | 144 | 1 | 0.69% | no | 0 | 0 |
| Recognition | Spirits | t3 | 144 | 0 | 0.00% | no | 0 | 0 |
| Omnibus | Headphones | t1 | 166 | 1 | 0.60% | no | 0 | 0 |
| Omnibus | Skincare | t1 | 222 | 2 | 0.90% | no | 0 | 0 |
| Omnibus | Cosmetics | t1 | 226 | 3 | 1.33% | no | 0 | 0 |
| Omnibus | Automotive | t1 | 217 | 5 | 2.30% | yes | 0 | 0 |
| Omnibus | Spirits | t1 | 110 | 1 | 0.91% | no | 0 | 0 |
| Omnibus | Headphones | t2 | 159 | 0 | 0.00% | no | 0 | 0 |
| Omnibus | Skincare | t2 | 215 | 2 | 0.93% | no | 0 | 0 |
| Omnibus | Cosmetics | t2 | 234 | 3 | 1.28% | no | 0 | 0 |
| Omnibus | Automotive | t2 | 220 | 2 | 0.91% | no | 0 | 0 |
| Omnibus | Spirits | t2 | 103 | 1 | 0.97% | no | 0 | 0 |
| Omnibus | Headphones | t3 | 157 | 5 | 3.18% | yes | 0 | 0 |
| Omnibus | Skincare | t3 | 221 | 3 | 1.36% | no | 0 | 0 |
| Omnibus | Cosmetics | t3 | 215 | 3 | 1.40% | no | 0 | 0 |
| Omnibus | Automotive | t3 | 214 | 3 | 1.40% | no | 0 | 0 |
| Omnibus | Spirits | t3 | 102 | 1 | 0.98% | no | 0 | 0 |
| Early | Premium tea | -- | 546 | 13 | 2.38% | yes | 0 | 0 |
| Early | Finance apps | -- | 483 | 19 | 3.93% | yes | 0 | 0 |
| Early | Olive oil | -- | 508 | 14 | 2.76% | yes | 0 | 0 |
| Early | PM software | -- | 586 | 19 | 3.24% | yes | 0 | 0 |
| Early | Running shoes | -- | 454 | 12 | 2.64% | yes | 0 | 0 |
| Early | Facial skincare | -- | 683 | 14 | 2.05% | yes | 0 | 0 |
| Early | Household retail | -- | 635 | 14 | 2.20% | yes | 0 | 0 |
| Early | Kitchen knives | -- | 470 | 10 | 2.13% | yes | 0 | 0 |

![JUDGE_FAIL share of the primary judge per answer set, under the locked reply rule and the successor rule, against the 2% halt line. ](../../reports/figs/v120/chart_01_judge_fail_by_set.pdf){#fig:halt width=100%}

## 3.3 The successor rule v1.20 on the same replies

v1.20's Stage J then ran once on the same frozen records (2026-11-22 10:15 UTC). Under its rule J1 had 0 JUDGE_FAIL and 0 UNJUDGED units: all 155 units that failed under v1.11's rule became valid, as did the 7 repeat-sample failures, and every unit valid under v1.11's rule stayed valid (7,423 J1 main-pass units). For 174 J1 main-pass units valid under both rules the judgement comes from an earlier attempt than the one v1.11's rule would score (an earlier reply that v1.11's rule rejected counts under the v1.20 rule); S-ATT reports the effect of scoring v1.11's attempt instead. J2's 3,650 units were valid under both rules. The highest JUDGE_FAIL share under the v1.20 rule was 0.0%, so v1.20's prediction (below 0.5% in every set) held, and Stage J passed its 2% check. Stage C then ran once (2026-11-22 10:19 UTC). Everything below is v1.20's result, and, under case B, Sentiment Paper A's.

The omnibus units joined the Presence and Consistency table one to one at every wave, and the number of omnibus windows differed from the Presence mention count in 0 units. $R^*$ (MNP) was computed with v1.10's locked code after v1.10's own verdicts existed; all 23 regenerated rank tables equalled v1.10's Stage S tables. v1.20's Stage C output does not carry the cross-check of Presence and $C^*$ against the v1.9 unit table that v1.11's Stage C writes (v1.11 §2), so that check is not reported here.

## 3.4 Judge agreement (H1) and self-consistency

Over 3,650 units with valid outputs from both judges, ordinal $\alpha$ was 0.874 (0.873 over the units both judges said refer to the brand; recognition 0.743, omnibus 0.870, early sample 0.906), and Cohen's $\kappa$ on the evaluative flag was 0.878. Over 163 omnibus brand scores rated under both judges, the within-category brand correlation was 0.874 (95% CI 0.770 to 0.915).
Both statistics met the confirmed thresholds ($\alpha \ge 0.667$, $\rho \ge 0.80$): H1 is CONFIRMED, and the AI-judged instrument is read as reliable at the level the pre-registration requires.
Under S-ATT, H1 is CONFIRMED ($\alpha$ = 0.873, brand $\rho_w$ = 0.869).

Figure 2 shows where the two judges' valences met and where they parted: they gave the same valence on 3,238 units and differed on 412, of which 407 were one step apart. Self-consistency (Table 3) measures each judge's call-to-call variation on the repeat sample: overall exact valence agreement was 0.982 for J1 and 0.978 for J2. No judge and block fell below the 0.90 flag.

![Valence from J1 (rows) and J2 (columns) on every unit with valid outputs from both judges. ](../../reports/figs/v120/chart_02_judge_confusion.pdf){#fig:confusion width=82%}

Table: Self-consistency: each judge's second judgement of the fixed repeat sample, against its first (exact valence agreement, ordinal $\alpha$, $\kappa$ on the evaluative flag).

| Judge | Block | Pairs | Exact | $\alpha$ | $\kappa$ | Below 0.90 |
|:------------------------|:-----------|-----:|-----:|-----:|-----:|:----------|
| J1 (Claude Opus 5.5) | Recognition | 22 | 1.000 | 1.000 | -- | no |
|  | Omnibus | 139 | 0.978 | 0.965 | 1.000 | no |
|  | Early | 218 | 0.982 | 0.974 | 0.979 | no |
|  | All | 379 | 0.982 | 0.979 | 0.985 | no |
| J2 (GPT-6.1 Sol) | Recognition | 22 | 1.000 | 1.000 | -- | no |
|  | Omnibus | 139 | 0.978 | 0.975 | 0.942 | no |
|  | Early | 23 | 0.957 | 0.922 | 1.000 | no |
|  | All | 184 | 0.978 | 0.977 | 0.957 | no |

## 3.5 Separability from Presence, Consistency and Ranking (H2, H3, H5)

Table 4 gives the per-wave statistics; Figure 3 places them against the bands.
Against Presence, $\rho_w$ was 0.4771 at $t_1$, 0.4477 at $t_2$ and 0.5013 at $t_3$ (unrounded values as the verdict uses them). At $t_3$ $\lvert\rho_w\rvert$ reached 0.50. Under the three-wave rule one such wave is enough: H2 is FALSIFIED. All determined correlations are positive: within category, brands with higher Presence received warmer descriptions, the failure the v1.7 lesson warns of. At $t_1$ and $t_2$ it was in the marginal band, not below it.
Against Consistency, $\lvert\rho_w\rvert$ stayed at or below 0.30 at every determined wave: H3 is CONFIRMED.
Against Ranking ($R^*$, MNP), $\lvert\rho_w\rvert$ exceeded 0.30 at all three determined waves without reaching 0.50 at any: H5 is MARGINAL. In the early categories, $\rho_w(S, R^*)$ was 0.462 over 136 brands (band verdict MARGINAL).

Table: Separability: $\rho_w$ of the Sentiment score with each comparator per wave, with 95% bootstrap interval and number of brand units ("n.d." = below the floor). H8 uses the recognition score in premium spirits (one category, plain Spearman).

|  | Against | $t_1$ | $t_2$ | $t_3$ | Verdict |
|:--------|:-------------|----------------------------:|----------------------------:|----------------------------:|:---------|
| H2 | Presence $P$ | +0.477 [+0.190, +0.676] (55) | +0.448 [+0.242, +0.595] (54) | +0.501 [+0.264, +0.665] (54) | FALSIFIED |
| H3 | Consistency $C^*$ | +0.060 [−0.254, +0.342] (55) | −0.016 [−0.344, +0.328] (54) | +0.149 [−0.163, +0.418] (54) | CONFIRMED |
| H5 | Ranking $R^*$ | +0.440 [+0.167, +0.619] (55) | +0.385 [+0.084, +0.605] (54) | +0.418 [+0.112, +0.631] (54) | MARGINAL |
| H8 | Presence ($S_{\text{rec}}$) | +0.230 [−0.124, +0.546] (24) | +0.341 [−0.046, +0.689] (24) | +0.267 [−0.115, +0.594] (24) | MARGINAL |

![Within-category rank correlation of the Sentiment score with Presence, Consistency, Ranking and (recognition score) Presence, per wave, with 95% intervals and the separability bands. ](../../reports/figs/v120/chart_03_separability.pdf){#fig:sep width=100%}

## 3.6 Stability over three weeks and five months (H4, H6)

Over 53 omnibus brand units rated at $t_1$ and $t_2$, $\rho_w$ was 0.735 (95% CI 0.492 to 0.853; permutation $p$ = 0.0001).
H4 is CONFIRMED: the score kept its brand order over three weeks.
Over 52 units rated at $t_2$ and $t_3$, $\rho_w$ was 0.743 (95% CI 0.496 to 0.865; $p$ = 0.0001).
H6 is CONFIRMED: the brand order held over five months.
Both permutation $p$ values are the smallest that 10,000 permutations can give. Neither H1 nor H4 is FALSIFIED, so the noise guard does not apply.

![Rank correlation of each brand's Sentiment score between waves, with 95% intervals and the stability thresholds. ](../../reports/figs/v120/chart_04_stability.pdf){#fig:stab width=88%}

## 3.7 Secondary tests (H7, H8, H9)

In the eight early categories, the correlation of S with the number of answers naming the brand was 0.532 (95% CI 0.364 to 0.645; 136 rated brands).
H7 is FALSIFIED: in the early categories, on a second answering panel and without the omnibus rating floor, S tracked how often a brand is named. The correlation is positive, the same direction as H2.
The recognition score's correlation with Presence was 0.230, 0.341 and 0.267 at the three waves (Table 4), above 0.30 at one of the three determined waves ($t_2$) and below 0.50 at all: H8 is MARGINAL.

On recognition and omnibus units judged validly by both judges and referring to the brand, J1 scored answers by its own provider's models +0.26 points relative to J2 (1,168 units) and other answers +0.81 points (2,045 units): $\Delta$ = −0.55 points (Figure 5).
$\lvert\Delta\rvert$ was at most 5 points: H9 is CONFIRMED, and no self-preference of the primary judge was found. The sign runs the other way: relative to J2, J1 was slightly less generous to its own provider's answers than to the others.

![Mean difference between the primary and the second judge's unit scores, for answers written by the primary judge's provider's models and for the other answers. ](../../reports/figs/v120/chart_05_self_preference.pdf){#fig:selfpref width=78%}

## 3.8 Verdicts

Table 5 lists every pre-registered test once, with the verdict as v1.20's scorer wrote it. The noise guard was not applied. Under v1.11's own rule no test has a verdict (§3.2).

Table: Verdicts of the pre-registered tests (scorer's words; v1.20 rule, Sentiment Paper A's result under case B).

| Test | Tier | Statistic | Value(s) | Verdict |
|:-------------------------|:--------------|:--------------------|----------------------:|:---------|
| H1\_Judge\_Agreement | Primary (gate) | ordinal $\alpha$; brand $\rho_w(S_{J1}, S_{J2})$ | $\alpha$ 0.874; $\rho_w$ 0.874 | CONFIRMED |
| H2\_Sep\_Presence | Primary | $\lvert\rho_w(S, P)\rvert$ per wave | 0.477 / 0.448 / 0.501 | FALSIFIED |
| H3\_Sep\_Consistency | Primary | $\lvert\rho_w(S, C^*)\rvert$ per wave | 0.060 / -0.016 / 0.149 | CONFIRMED |
| H4\_Stability\_Short | Primary | $\rho_w(S_{t_1}, S_{t_2})$, permutation | 0.735 | CONFIRMED |
| H5\_Sep\_Ranking | Primary | $\lvert\rho_w(S, R^*)\rvert$ per wave | 0.440 / 0.385 / 0.418 | MARGINAL |
| H6\_Stability\_Long | Secondary | $\rho_w(S_{t_2}, S_{t_3})$, permutation | 0.743 | CONFIRMED |
| H7\_Naming\_Frequency | Secondary | $\lvert\rho_w(S, n_{\text{named}})\rvert$, early | 0.532 | FALSIFIED |
| H8\_Recognition\_Sep | Secondary | $\lvert\rho(S_{\text{rec}}, P)\rvert$ per wave | 0.230 / 0.341 / 0.267 | MARGINAL |
| H9\_Self\_Preference | Secondary | $\Delta$ of $u_{J1} - u_{J2}$, own vs other | −0.55 | CONFIRMED |

## 3.9 Sensitivity analyses

Verdicts that differ under a sensitivity analysis (never replacing the primary verdict): H5 under SU, MARGINAL $\rightarrow$ FALSIFIED; H2 under S-CUT, FALSIFIED $\rightarrow$ MARGINAL; H2 under S-CUT-M, FALSIFIED $\rightarrow$ MARGINAL; H2 under J2-scored S, FALSIFIED $\rightarrow$ MARGINAL. Table 6 gives the verdicts under every sensitivity that recomputes the hypotheses; Table 7 gives H2's per-wave statistics under each of them, because H2 decides the gate.

Table: Verdicts under the sensitivity analyses (they never change a primary verdict). SU: uncentred ranks; SD: without Denon; S-ATT: v1.11's attempt where v1.11's rule yields a judgement; S-CUT: without answers known or likely cut at the output limit; S-CUT-M: without the cells mostly cut at $t_3$. "--": not recomputed by that sensitivity.

|  | Primary | SU | SD | S-ATT | S-CUT | S-CUT-M |
|:--------|:---------|:---------|:---------|:---------|:---------|:---------|
| H1 | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED |
| H2 | FALSIFIED | FALSIFIED | FALSIFIED | FALSIFIED | MARGINAL | MARGINAL |
| H3 | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED |
| H4 | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED |
| H5 | MARGINAL | FALSIFIED | MARGINAL | MARGINAL | MARGINAL | MARGINAL |
| H6 | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED |
| H7 | FALSIFIED | FALSIFIED | FALSIFIED | FALSIFIED | FALSIFIED | FALSIFIED |
| H8 | MARGINAL | MARGINAL | MARGINAL | MARGINAL | MARGINAL | MARGINAL |
| H9 | CONFIRMED | -- | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED |

Table: H2 (Sentiment against Presence) per wave under the primary analysis and each sensitivity: $\rho_w$ [95% CI] (brand units).

| Analysis | H2 | $t_1$ | $t_2$ | $t_3$ |
|:--------------------|:---------|----------------------------:|----------------------------:|----------------------------:|
| Primary | FALSIFIED | +0.477 [+0.190, +0.676] (55) | +0.448 [+0.242, +0.595] (54) | +0.501 [+0.264, +0.665] (54) |
| SU | FALSIFIED | +0.541 [+0.292, +0.717] (55) | +0.523 [+0.349, +0.652] (54) | +0.556 [+0.347, +0.703] (54) |
| SD | FALSIFIED | +0.477 [+0.190, +0.676] (55) | +0.448 [+0.242, +0.595] (54) | +0.501 [+0.264, +0.665] (54) |
| S-ATT | FALSIFIED | +0.477 [+0.190, +0.676] (55) | +0.454 [+0.245, +0.602] (54) | +0.501 [+0.264, +0.665] (54) |
| S-CUT | MARGINAL | +0.473 [+0.185, +0.674] (55) | +0.451 [+0.244, +0.598] (54) | +0.488 [+0.249, +0.654] (53) |
| S-CUT-M | MARGINAL | +0.457 [+0.171, +0.657] (55) | +0.453 [+0.247, +0.604] (54) | +0.489 [+0.249, +0.656] (53) |
| NV in place of S | FALSIFIED | +0.509 [+0.227, +0.700] (55) | +0.323 [+0.053, +0.537] (54) | +0.385 [+0.117, +0.611] (54) |
| Model-balanced S | FALSIFIED | +0.510 [+0.219, +0.708] (55) | +0.468 [+0.241, +0.612] (54) | +0.530 [+0.286, +0.712] (54) |
| J2-scored S | MARGINAL | +0.310 [+0.010, +0.559] (55) | +0.423 [+0.179, +0.591] (54) | +0.475 [+0.210, +0.662] (54) |

Without the 116 units whose answer is in the cut-answer list (S-CUT), $\rho_w(S, P)$ was 0.4728, 0.4506 and 0.4885 (H2 MARGINAL); without the 175 units of the mostly cut cells (S-CUT-M), 0.4566, 0.4532 and 0.4891 (H2 MARGINAL). The units are listed in the appendix.

## 3.10 Cross-category baseline (descriptive)

Figure 6 shows the median and interquartile range of the rated brands' Sentiment scores in each category, wave and block. Median S ranged from 70.4 to 85.7 across the omnibus categories and waves and from 64.2 to 71.4 across the early categories, on a scale where 50 is neutral. Mean unit score was 79.2 on the legacy panel and 67.3 on the early panel. In premium spirits, the recognition score and the omnibus score correlated 0.531, 0.810 and 0.527 at $t_1$, $t_2$ and $t_3$ (brands rated in both: 9, 9, 10). The full baseline and the other pre-registered descriptives are in the appendix.

![Median and interquartile range of the rated brands' Sentiment scores per category, wave and block. ](../../reports/figs/v120/chart_06_baseline.pdf){#fig:base width=100%}

# 4. Discussion

**The procedure.** The study's own locked rule halted it, and the halt is a result. It is a result about a reply format, not about valence: every unit that failed under v1.11's rule had a stored reply holding exactly one complete object that passed v1.11's checks once the text around it was set aside, which is the one thing v1.20 changes. The successor was locked before any v1.11 reply existed, applied once, with v1.11's code for everything else, and its role in case B was fixed in advance; the programme's rule since v1.15 is that a pre-registration with an LLM judge states its extraction rule in advance and tests it on recorded replies. Scoring v1.11's own attempt where v1.11's rule yields a judgement (S-ATT) changes no verdict.

**The instrument and the gate.** Under the successor rule the instrument is reliable at the level the pre-registration requires: two judges from different providers agreed (H1 CONFIRMED), the score kept its brand order over three weeks and five months (H4 CONFIRMED, H6 CONFIRMED), and the primary judge showed no self-preference (H9 CONFIRMED). It is also separable from Consistency (H3 CONFIRMED). But it is not separable from Presence (H2 FALSIFIED): within category, brands that the models name more often and more widely are described more warmly. The early categories, on another answering panel and without the omnibus rating floor, give H7 FALSIFIED (0.532), and against Ranking the score sits in the marginal band (H5 MARGINAL). Read with the v1.7 lesson, this is the outcome the gate exists to catch: part of what the Sentiment score records is how present a brand already is. A reliable instrument that re-measures an existing component adds no separate dimension to the composite, whatever its face validity.

**How firm the Presence result is.** The H2 verdict rests on one wave at or above the 0.50 line (0.5013 at $t_3$) and two in the marginal band. Without the answers that ended, or probably ended, at the answering models' output limit, the $t_3$ correlation falls to 0.4885 (S-CUT) or 0.4891 (S-CUT-M), below the line, and H2 is MARGINAL in both. No variant put H2 in the confirmed band, and the correlation with Presence was positive at every determined wave in the primary analysis and in all eight variants (Table 7); S-CUT, S-CUT-M and J2-scored S give MARGINAL, the others FALSIFIED. The falsification is narrow, not a sign that Sentiment is separable from Presence, and the pre-registered verdict, H2 FALSIFIED, stands. The rating floor of six units also restricts the range of Presence among rated omnibus brands, which can understate the association (v1.11 §11).

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

Materials are deposited at OSF (osf.io/ec6wh). `methodology/v1_11/`: the locked pre-registration with its judge prompt, unit table, Paper B sample, parity, cost and precision records, the input manifest, the scorer and judge scripts with their tests, the lock manifest, the deviations record and the anchor record. `methodology/v1_20/`: the locked successor pre-registration, its configuration, scoping scripts and cut-answer list, dry-run record, deviations record and anchor record. After the run: the judge call records, batch log and plan (`methodology/v1_11/data/`), the frozen-output record and v1.11's Stage J console record (`methodology/v1_11/outputs/`), and v1.20's outputs with their console records (`methodology/v1_20/outputs/`: `stage_j_v1_20.json`, `unit_outcomes_v1_20.csv`, `comparison_v1_11_v1_20.json`, `v1_20_verdicts.json`). The code is in the programme's GitHub repository (github.com/thirdsystem-aias/aias) at tags `v1.11-prereg-r1` and `v1.20-prereg-r1`; this paper's builders and figure sources are added at publication.

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

| Block | Category | Wave | Brands | Rated | S median | S IQR | E | Non-eval. | Mixed | Not brand |
|:---------------|:----------------|:-----|------:|-----:|--------:|----------:|----:|---------:|-----:|---------:|
| Recognition | Spirits | t1 | 24 | 24 | 91.7 | 91.7--95.8 | 1.00 | 0% | 43% | 0.0% |
| Recognition | Spirits | t2 | 24 | 24 | 91.7 | 90.6--95.8 | 1.00 | 0% | 42% | 0.0% |
| Recognition | Spirits | t3 | 24 | 24 | 91.7 | 87.5--95.8 | 1.00 | 0% | 39% | 0.0% |
| Omnibus | Headphones | t1 | 12 | 8 | 77.3 | 70.5--81.9 | 0.77 | 19% | 4% | 0.0% |
| Omnibus | Headphones | t2 | 13 | 8 | 75.0 | 69.7--82.6 | 0.79 | 21% | 3% | 0.0% |
| Omnibus | Headphones | t3 | 12 | 8 | 75.8 | 70.3--82.0 | 0.77 | 18% | 4% | 0.0% |
| Omnibus | Skincare | t1 | 19 | 10 | 70.4 | 68.2--76.6 | 0.74 | 23% | 1% | 0.0% |
| Omnibus | Skincare | t2 | 18 | 9 | 74.3 | 69.6--75.9 | 0.79 | 25% | 1% | 0.0% |
| Omnibus | Skincare | t3 | 17 | 9 | 72.5 | 67.9--74.0 | 0.75 | 25% | 2% | 0.0% |
| Omnibus | Cosmetics | t1 | 19 | 14 | 73.4 | 70.5--79.0 | 0.82 | 18% | 0% | 0.0% |
| Omnibus | Cosmetics | t2 | 20 | 14 | 73.6 | 70.5--77.7 | 0.75 | 21% | 0% | 0.0% |
| Omnibus | Cosmetics | t3 | 19 | 13 | 72.5 | 70.5--76.6 | 0.79 | 17% | 0% | 0.0% |
| Omnibus | Automotive | t1 | 15 | 14 | 78.7 | 73.9--85.7 | 0.86 | 15% | 3% | 0.0% |
| Omnibus | Automotive | t2 | 16 | 14 | 75.0 | 75.0--84.0 | 0.85 | 14% | 2% | 0.0% |
| Omnibus | Automotive | t3 | 16 | 14 | 79.9 | 77.2--86.5 | 0.90 | 9% | 5% | 0.0% |
| Omnibus | Spirits | t1 | 19 | 9 | 85.7 | 80.6--86.4 | 0.99 | 3% | 3% | 0.0% |
| Omnibus | Spirits | t2 | 21 | 9 | 81.2 | 77.8--85.7 | 0.96 | 5% | 3% | 0.0% |
| Omnibus | Spirits | t3 | 19 | 10 | 84.4 | 82.7--89.4 | 0.99 | 2% | 2% | 0.0% |
| Early | Finance apps | v0.9 | 14 | 14 | 68.9 | 64.5--73.1 | 0.74 | 26% | 29% | 3.7% |
| Early | Household retail | v1.0 | 20 | 20 | 64.4 | 58.3--68.4 | 0.59 | 38% | 15% | 3.1% |
| Early | Kitchen knives | v1.0 | 17 | 15 | 69.4 | 62.8--77.1 | 0.78 | 20% | 24% | 3.6% |
| Early | Olive oil | v0.9 | 19 | 16 | 69.2 | 66.9--72.2 | 0.77 | 24% | 12% | 0.2% |
| Early | PM software | v0.9 | 18 | 17 | 64.7 | 58.3--68.4 | 0.66 | 34% | 20% | 0.5% |
| Early | Premium tea | v0.14 | 22 | 17 | 71.4 | 66.7--73.5 | 0.76 | 23% | 9% | 0.9% |
| Early | Running shoes | v0.9 | 17 | 15 | 66.0 | 62.6--68.4 | 0.54 | 42% | 10% | 6.6% |
| Early | Facial skincare | v0.9 | 29 | 22 | 64.2 | 62.5--71.8 | 0.71 | 28% | 18% | 0.7% |

Table: Cross-category baseline, continued (v1.11 §6.1): judged units, J1's JUDGE_FAIL and UNJUDGED units under the v1.20 rule, the share of bare windows (the brand's segments carry fewer than four other words) and the extraction misses of the unit build, per block, category and wave.

| Block | Category | Wave | Judged units | JUDGE_FAIL | UNJUDGED | Bare windows | Extraction misses |
|:---------------|:----------------|:-----|------------:|----------:|--------:|------------:|-----------------:|
| Recognition | Spirits | t1 | 144 | 0 | 0 | 0.0% | -- |
| Recognition | Spirits | t2 | 144 | 0 | 0 | 0.0% | -- |
| Recognition | Spirits | t3 | 144 | 0 | 0 | 0.0% | -- |
| Omnibus | Headphones | t1 | 166 | 0 | 0 | 7.2% | 0 |
| Omnibus | Headphones | t2 | 159 | 0 | 0 | 8.8% | 0 |
| Omnibus | Headphones | t3 | 157 | 0 | 0 | 8.9% | 0 |
| Omnibus | Skincare | t1 | 222 | 0 | 0 | 12.6% | 0 |
| Omnibus | Skincare | t2 | 215 | 0 | 0 | 8.8% | 0 |
| Omnibus | Skincare | t3 | 221 | 0 | 0 | 10.4% | 0 |
| Omnibus | Cosmetics | t1 | 226 | 0 | 0 | 9.3% | 0 |
| Omnibus | Cosmetics | t2 | 234 | 0 | 0 | 10.7% | 0 |
| Omnibus | Cosmetics | t3 | 215 | 0 | 0 | 7.9% | 0 |
| Omnibus | Automotive | t1 | 217 | 0 | 0 | 10.1% | 0 |
| Omnibus | Automotive | t2 | 220 | 0 | 0 | 8.6% | 0 |
| Omnibus | Automotive | t3 | 214 | 0 | 0 | 4.2% | 0 |
| Omnibus | Spirits | t1 | 110 | 0 | 0 | 0.0% | 0 |
| Omnibus | Spirits | t2 | 103 | 0 | 0 | 0.0% | 0 |
| Omnibus | Spirits | t3 | 102 | 0 | 0 | 0.0% | 0 |
| Early | Finance apps | v0.9 | 483 | 0 | 0 | 1.4% | 0 |
| Early | Household retail | v1.0 | 635 | 0 | 0 | 9.3% | 0 |
| Early | Kitchen knives | v1.0 | 470 | 0 | 0 | 6.6% | 0 |
| Early | Olive oil | v0.9 | 508 | 0 | 0 | 8.3% | 0 |
| Early | PM software | v0.9 | 586 | 0 | 0 | 2.7% | 0 |
| Early | Premium tea | v0.14 | 546 | 0 | 0 | 2.2% | 0 |
| Early | Running shoes | v0.9 | 454 | 0 | 0 | 10.1% | 0 |
| Early | Facial skincare | v0.9 | 683 | 0 | 0 | 4.1% | 0 |

Table: Ordinal $\alpha$ between J1 and J2 per block, and the variants of S for H2 and H3 (v1.11 §5.1): verdict and $\rho_w$ per wave.

| Variant | Verdict | Value | $t_1$ | $t_2$ | $t_3$ |
|:------------------------|:---------|-----:|----------------------------:|----------------------------:|----------------------------:|
| $\alpha$, block R |  | 0.743 |  |  |  |
| $\alpha$, block F |  | 0.870 |  |  |  |
| $\alpha$, block E |  | 0.906 |  |  |  |
| NV in place of S, H2 | FALSIFIED |  | +0.509 [+0.227, +0.700] (55) | +0.323 [+0.053, +0.537] (54) | +0.385 [+0.117, +0.611] (54) |
| NV in place of S, H3 | CONFIRMED |  | +0.025 [−0.276, +0.301] (55) | +0.051 [−0.273, +0.367] (54) | +0.158 [−0.155, +0.431] (54) |
| Model-balanced S, H2 | FALSIFIED |  | +0.510 [+0.219, +0.708] (55) | +0.468 [+0.241, +0.612] (54) | +0.530 [+0.286, +0.712] (54) |
| Model-balanced S, H3 | CONFIRMED |  | −0.089 [−0.387, +0.217] (55) | −0.033 [−0.355, +0.310] (54) | +0.134 [−0.183, +0.421] (54) |
| J2-scored S, H2 | MARGINAL |  | +0.310 [+0.010, +0.559] (55) | +0.423 [+0.179, +0.591] (54) | +0.475 [+0.210, +0.662] (54) |
| J2-scored S, H3 | CONFIRMED |  | +0.031 [−0.278, +0.343] (55) | −0.157 [−0.467, +0.195] (54) | +0.104 [−0.211, +0.417] (54) |

Table: Mean unit score by answering model and block (J1, valid units referring to the brand).

| Answering model | Recognition | Omnibus | Early |
|:---------------------------|-----------:|----------:|----------:|
| `claude-opus-4-5` | 75.0 (72) | 63.0 (521) | -- |
| `claude-opus-4-7` | -- | -- | 63.7 (755) |
| `claude-sonnet-4-5` | 81.2 (72) | 74.1 (503) | -- |
| `claude-sonnet-4-6` | -- | -- | 64.0 (590) |
| `gemini-2.5-flash` | 96.5 (72) | 88.1 (318) | 74.6 (710) |
| `gemini-2.5-flash-lite` | 99.7 (72) | 86.6 (507) | -- |
| `gpt-4o` | 98.3 (72) | 78.0 (476) | -- |
| `gpt-4o-mini` | 100.0 (72) | 77.9 (456) | -- |
| `gpt-5.4-mini` | -- | -- | 67.4 (748) |
| `gpt-5.5` | -- | -- | 66.2 (768) |
| `grok-4-1-fast` | -- | -- | 67.7 (695) |

Table: Mean unit score by frame or prompt type and block (J1, valid units referring to the brand; frame identifiers as in the source studies).

| Block | Frame / prompt | Mean u | Units |
|:---------------|:---------------|------:|-----:|
| Recognition | `A` | 91.8 | 432 |
| Omnibus | `CC-1` | 68.3 | 26 |
|  | `CC-2` | 78.0 | 59 |
|  | `CC-3` | 81.0 | 29 |
|  | `EA-1` | 88.5 | 63 |
|  | `EA-2` | 89.9 | 42 |
|  | `EA-3` | 84.9 | 96 |
|  | `q1` | 83.5 | 331 |
|  | `q1_audiophile` | 87.9 | 89 |
|  | `q2` | 74.5 | 325 |
|  | `q2_enthusiast` | 77.7 | 112 |
|  | `q3` | 82.8 | 238 |
|  | `q3_reference` | 77.8 | 100 |
|  | `q4` | 71.7 | 360 |
|  | `q4_famous` | 69.6 | 84 |
|  | `q5` | 70.4 | 447 |
|  | `q5_popular` | 68.9 | 49 |
|  | `q6` | 79.6 | 283 |
|  | `q6_iconic` | 75.0 | 48 |
| Early | `p1_functional` | 70.2 | 580 |
|  | `p2_contextual` | 71.5 | 632 |
|  | `p3_constraint` | 67.2 | 602 |
|  | `p4_identity` | 63.6 | 1,150 |
|  | `p5_discovery` | 67.0 | 611 |
|  | `p6_comparison` | 67.6 | 691 |

Table: Units whose answer is in the cut-answer list (S-CUT) or in an S-CUT-M cell, per block, wave, category and answering model: units, judged, in J2's coverage and in the Paper B sample (v1.20 §8 item 4).

| List | Block | Wave | Category | Model | Units | Judged | J2 | Paper B |
|:-----------|:-----------|:----|:----------|:-----------------------|-----:|------:|----:|-------:|
| S-CUT | Omnibus | t1 | Headphones | `gemini-2.5-flash-lite` | 14 | 14 | 14 | 1 |
| S-CUT | Omnibus | t1 | Spirits | `gemini-2.5-flash-lite` | 8 | 8 | 8 | 1 |
| S-CUT | Omnibus | t2 | Headphones | `gemini-2.5-flash-lite` | 15 | 15 | 15 | 3 |
| S-CUT | Omnibus | t2 | Spirits | `gemini-2.5-flash-lite` | 8 | 8 | 8 | 1 |
| S-CUT | Omnibus | t3 | Headphones | `gemini-2.5-flash-lite` | 22 | 22 | 22 | 1 |
| S-CUT | Omnibus | t3 | Spirits | `gemini-2.5-flash` | 2 | 2 | 2 | 2 |
| S-CUT | Omnibus | t3 | Spirits | `gemini-2.5-flash-lite` | 8 | 8 | 8 | 1 |
| S-CUT | Recognition | t1 | Spirits | `gemini-2.5-flash-lite` | 2 | 2 | 2 | 0 |
| S-CUT | Recognition | t2 | Spirits | `gemini-2.5-flash-lite` | 2 | 2 | 2 | 0 |
| S-CUT | Recognition | t3 | Spirits | `claude-opus-4-5` | 9 | 9 | 9 | 1 |
| S-CUT | Recognition | t3 | Spirits | `gemini-2.5-flash` | 24 | 24 | 24 | 2 |
| S-CUT | Recognition | t3 | Spirits | `gemini-2.5-flash-lite` | 2 | 2 | 2 | 0 |
| S-CUT-M | Omnibus | t1 | Headphones | `gemini-2.5-flash-lite` | 33 | 33 | 33 | 3 |
| S-CUT-M | Omnibus | t1 | Spirits | `gemini-2.5-flash` | 4 | 4 | 4 | 2 |
| S-CUT-M | Omnibus | t2 | Headphones | `gemini-2.5-flash-lite` | 31 | 31 | 31 | 4 |
| S-CUT-M | Omnibus | t2 | Spirits | `gemini-2.5-flash` | 5 | 5 | 5 | 2 |
| S-CUT-M | Omnibus | t3 | Headphones | `gemini-2.5-flash-lite` | 28 | 28 | 28 | 1 |
| S-CUT-M | Omnibus | t3 | Spirits | `gemini-2.5-flash` | 2 | 2 | 2 | 2 |
| S-CUT-M | Recognition | t1 | Spirits | `gemini-2.5-flash` | 24 | 24 | 24 | 4 |
| S-CUT-M | Recognition | t2 | Spirits | `gemini-2.5-flash` | 24 | 24 | 24 | 1 |
| S-CUT-M | Recognition | t3 | Spirits | `gemini-2.5-flash` | 24 | 24 | 24 | 2 |

The J1 × J2 confusion matrix of v1.11 §6.5 is Figure 2, which prints every count. Exploratory (v1.11 §6.6): on 2,583 (answer, brand) pairs of the five v0.9 early sets, the sign of J1's valence agreed with the archived per-brand label in 47.3% of pairs.
