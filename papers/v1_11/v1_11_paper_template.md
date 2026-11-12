---
title: "Sentiment in AI Answers about Brands"
subtitle: "An AI-Judged Valence Instrument, Cross-Category Baseline and Separability Gate for a Sentiment Component of AI Availability (AIAS™ Methodology v1.11)"
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

{\large An AI-Judged Valence Instrument, Cross-Category Baseline and Separability Gate\\ for a Sentiment Component of AI Availability (AIAS™ Methodology v1.11)}\\[28pt]

Pablo Ulpiano González Castro\\[4pt]
School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System™ (research entity; data archive and methodology venue)\\[8pt]
Correspondence: pablou@pablou.com · pablou.com\\
ORCID: \href{https://orcid.org/0009-0003-8968-9990}{0009-0003-8968-9990}\\[20pt]

Pre-registration: \texttt{ {{PREREG_TAG}} } (commit \texttt{ {{PREREG_COMMIT}} }; deposited on OSF before the first judge call)\\
Data and code: OSF \texttt{ec6wh}, \texttt{methodology/v1\_11}\\
{% if SYNTHETIC %}
\vspace{14pt}\textbf{SYNTHETIC TEST BUILD: every number in this document comes from synthetic files. Not results.}\\
{% endif %}

\end{center}
\end{titlepage}

# Abstract {-}

Presence records whether AI answers name a brand, and Consistency how evenly the models of a panel do so; neither records how the answers describe the brand. This pre-registered study specifies an AI-judged valence instrument for the AIAS measurement programme and tests whether the resulting Sentiment score is a separate component. Archived answers of two answering panels were re-analysed without new collection: open recognition answers about 24 premium-spirits brands, mention windows from five omnibus categories at three waves, and mention windows from eight early category studies. A primary judge (Claude Opus 5.5) rated the valence of every judged unit on a five-point anchored scale, and a second judge from another provider (GPT-6.1 Sol) rated the recognition and omnibus units and a seeded sample of the early windows; {{J1_VALID}} units received a valid primary judgement. The Sentiment score S of a brand is the mean of its unit scores on a 0--100 scale, rated with at least six valid units. Agreement between the two judges was ordinal Krippendorff's $\alpha$ = {{H1_ALPHA}} on units and a within-category rank correlation of {{H1_BRHO}} on brand scores (instrument gate H1: {{V_H1}}).
{% switch CASE_OVERALL %}
{% case SEPARABLE %}
Within category, S was separable from Presence{% if H5_ACTIVE %}, Consistency and Ranking{% else %} and Consistency{% endif %} at every determined wave, and it kept its brand order over three weeks (H4: {{V_H4}}).
{% case SEPARABLE_FLAGGED %}
Within category, S was separable from Presence{% if H5_ACTIVE %}, Consistency and Ranking{% else %} and Consistency{% endif %} at every determined wave, and it kept its brand order over three weeks (H4: {{V_H4}}); because judge agreement was only marginal, every verdict carries that flag.
{% case NOT_SEPARABLE %}
At least one primary separability test was falsified (Presence H2: {{V_H2}}; Consistency H3: {{V_H3}}; Ranking H5: {{V_H5}}): on these data the AI-judged Sentiment score is not a separate component from the measure it tracks.
{% case MIXED %}
The primary tests did not all reach the confirmed band (Presence H2: {{V_H2}}; Consistency H3: {{V_H3}}; short-term stability H4: {{V_H4}}; Ranking H5: {{V_H5}}); none of the primary separability tests (H2, H3, H5) was falsified.
{% case INSTRUMENT_FAILED %}
The judges did not agree well enough for the instrument to be called reliable; under the pre-registered noise guard, the separability tests that depend on it are reported as UNDETERMINED, with their statistics shown as descriptive only.
{% case UNSTABLE %}
S did not keep its brand order over three weeks (H4: {{V_H4}}); under the pre-registered noise guard the separability tests are reported as UNDETERMINED, with their statistics shown as descriptive only.
{% case INSTRUMENT_UNDETERMINED %}
The instrument gate could not be determined on the units available, so no claim about the instrument's reliability is made; the remaining tests are reported with their own floors (Presence H2: {{V_H2}}; Consistency H3: {{V_H3}}; H4: {{V_H4}}).
{% endswitch %}
Sentiment remains provisional until human labels, collected under a separate pre-registration (Paper B), validate the judge.

**Keywords:** AI availability; brand sentiment; large language models; LLM-as-judge; inter-rater agreement; pre-registration; measurement validity

\clearpage

# 1. Introduction

AI Availability --- the discoverability and representation of a brand in the outputs of large language models (LLMs) --- has been proposed as a third layer of brand availability (González Castro, 2026a) beside the Mental and Physical Availability of the Ehrenberg-Bass tradition (Sharp, 2010; Sharp & Romaniuk, 2021), within the Tri-System framework (González Castro, 2026l). The AIAS™ programme builds the components of an AI availability score one at a time, each pre-registered and locked before it is used, on the Presence measurement protocol (González Castro, 2026b, 2026c, 2026d, 2026e). Presence is whether and how often models name a brand (Methodology v1.6: González Castro, 2026f), anchored across five categories in AIAS 1.0 (González Castro, 2026j). Consistency is how evenly the models of a panel name it: the first Consistency instrument failed its separability test because it moved with how often a brand is named (v1.7: González Castro, 2026g); its replacement measures the dispersion statistic $\varphi$ (v1.8: González Castro, 2026h), scaled to $C^*$ (v1.9: González Castro, 2026i). The AIAS 2.0 synthesis showed Consistency separable from Presence (González Castro, 2026k).

Being named is not the same as being described well. An answer can name a brand and recommend it, name it and warn against it, or name it in a list without comment. A brand's availability in AI answers therefore has a second face: the valence of what the answers say. This paper specifies a Sentiment instrument for that face and asks three questions, in the order the pre-registration fixes. First, is the instrument reliable enough to be read at all: do two judge models from different providers agree on the valence of the same text (H1), and does the score keep its brand order over weeks (H4, H6)? Second, is Sentiment a separate component: does it move independently of Presence, Consistency and Ranking within category (H2, H3, H5), of how often a brand is named in the early categories (H7), and, on a floor-free recognition score, of Presence (H8)? Third, does the primary judge favour answers written by its own provider's models (H9)?

The v1.7 lesson shapes the design. An instrument that rises with how often a brand is named reproduces Presence under another name. Sentiment carries that risk in a specific form: brands named often may be named in recommendation frames, and recommendation reads as warm. The separability tests are therefore within category, against the same Presence and Consistency values the Ranking paper (Methodology v1.10) is tested against, under the same three-wave rule, so that the two candidate components pass or fail under one standard. A noisy instrument would pass every separability test for the wrong reason; a pre-registered noise guard withdraws those verdicts if the instrument fails its reliability tests.

The score is AI-judged. Judging valence with a model is a measurement choice, not a finding: the judge is itself an instrument that needs validation. This paper calls Sentiment provisional throughout. A companion study (Paper B) collects human labels on a pre-drawn sample of the same units under its own pre-registration, and v1.11 Sentiment stays provisional until Paper B's validation thresholds, fixed before its labels are read, are met.

# 2. Method

The method is the locked pre-registration (§2.10), summarised here; section numbers in parentheses refer to it.

## 2.1 Data

The study re-analyses archived answers; no answer was collected for it (§2). Three blocks enter. Block R holds the open recognition answers of the v0.23 premium-spirits study ("what do you know about X"): 24 brands, six models of the legacy panel (Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o mini, Gemini 2.5 Flash and Gemini 2.5 Flash-Lite), three waves ($t_1$ May 20--26, $t_2$ June 10 and $t_3$ November 9, 2026), 432 answers. Block F holds the omnibus category answers of the five categories that carry Presence and Consistency (v0.19 audiophile headphones, v0.20 skincare, v0.21 cosmetics, v0.22 automotive, v0.23 premium spirits; 112 brand units), the same legacy panel and waves, 540 answers. Block E holds the eight early category studies (project management software, personal finance apps, olive oil, running shoes and facial skincare from v0.9; household retail and kitchen knives from v1.0; premium tea from v0.14), answered by a second six-model panel (Claude Sonnet 4.6, Claude Opus 4.7, GPT-5.4 mini, GPT-5.5, Gemini 2.5 Flash, Grok 4.1 Fast), 288 answers each, 2,304 in all. An input manifest pins every file by git blob and SHA-256; the scorer stops on any difference. No input cell is missing. The program's held studies, a technology panel pending its own conflict-of-interest screen, truncated recognition probes, yes/no probes and superseded or duplicate files are excluded for reasons fixed before the lock; three small sets formed a development sample used only to count windows before the lock (§2, §3).

## 2.2 Units and mention windows

A recognition answer is one unit, cut at 16,000 characters (none is that long). In blocks F and E the unit is a mention window: one per answer and registry brand that the answer names (§4.1). Which brands an omnibus answer names is the programme's certified mention record, so the number of F windows equals the mention count behind Presence; in the early blocks it is v1.10's alias rule on the phase registries. The window is the brand block: every segment that names the brand, each followed by up to four continuation segments, stopping at a heading, a list label or a segment naming another registry brand, capped at 1,500 characters. Brand aliases are located on the whole answer and mapped to segments. A mention with no locatable window would be counted and not judged; the unit build found none. At most 36 windows are judged per brand, answer set and wave (seeded, round-robin over models), which limits cost only in the early sets. The unit build of 10 November 2026 gave 7,578 judged units: 432 recognition answers, 2,781 omnibus windows and 4,365 early windows (of 13,463 before the cap).

## 2.3 Judges

The primary judge J1 is Claude Opus 5.5 (`claude-opus-5-5`, Anthropic Message Batches API); the reliability judge J2 is GPT-6.1 Sol (`gpt-6.1-sol`, OpenAI Batch API); Gemini 4 Argon is the alternate, used only if a judge cannot be (§4.2). Neither judge is its provider's flagship; the tier is a budget choice whose adequacy H1 and Paper B test. Every judge receives the same prompt, with explicit anchors, and returns JSON: a valence on $-2 \ldots +2$, whether the text refers to the target brand, whether it is evaluative, whether it is mixed, and an evidence quote of at most 20 words. Being named, listed or recommended by inclusion is not evaluation; plain facts are neutral; reported third-party judgements (awards, ratings, recalls, controversies) are (§4.3). No sampling parameter is sent; reasoning runs at the lowest documented effort ("low"); output is capped at 4,096 tokens. The judge sees the brand, the category, the question, the text type and the text, never the answering model, wave, answer set or any Presence, Consistency or Ranking value. An output that breaks the schema, is internally inconsistent, is empty or comes from another model than the one requested is retried twice with identical input and then counted as JUDGE_FAIL; above 2% of a set's units per judge the run halts before scoring. J1 judges every unit; J2 judges every R and F unit and a seeded 10% stratified sample of the early windows (3,650 units). A fixed 5% sample (379 units) is judged a second time by each judge to measure call-to-call variation; exact agreement below 0.90 is flagged, not halted.

## 2.4 The Sentiment score

A unit's score is $u = 25\,(v + 2) \in \{0, 25, 50, 75, 100\}$ for valence $v$. Non-evaluative units score 50 and stay in the score: a neutral description is an outcome, not missing data. Units that do not refer to the brand are excluded and counted. The Sentiment score of a brand in an answer set and wave is $S = $ the mean of $u$ over its valid units, computed on J1's outputs, and rated only with at least six valid units, without shrinkage: the rule mirrors $C^*$, six units are one model's full frame set, and shrinkage toward a midpoint by mention count tied a component to Presence in v1.9 (§4.4). Two descriptives travel with S: the evaluative share E and the mean unit score among evaluative units, NV (with at least three). The AIAS Sentiment score is the long-form S (block F for the omnibus categories, block E for the early ones); the recognition score $S_{\text{rec}}$ (block R) is a second elicitation used for a floor-free check.

## 2.5 Comparators

Presence is v1.6's $P = 100 \cdot \tfrac{1}{3}(C_P/6 + 2\hat\pi)$ with $\hat\pi$ the recall mentions over 36; Consistency is v1.9's $C^* = 100\,(1 - \varphi/7.2)$, rated with at least six mentions. Both are read from the AIAS 2.0 profile table (112 units × 3 waves), the file the Ranking paper uses, and opened only after H1 is written (§2, §8). Ranking $R^*$ is the statistic v1.10 selected at its Stage S, the mean normalised position (MNP), computed with v1.10's own locked code and extractor and its floor of six rankable mentions; every regenerated rank table must equal v1.10's, and $R^*$ is computed only after v1.10's own verdicts exist, so that v1.11 never computes a Ranking statistic first (§5).

## 2.6 Statistics

Rank associations are pooled within-category Spearman correlations $\rho_w$: average ranks are computed within each category and centred on the category's mean rank, and $\rho_w$ is the Pearson correlation of the pooled centred ranks (v1.10's implementation). A category enters a pooled statistic only with at least four units; a statistic is UNDETERMINED with fewer than 20 units pooled or fewer than three categories (H8, one category by design: at least 20 units). Separability bands are the programme's: $\lvert\rho\rvert \le 0.30$ confirmed separable, $\lvert\rho\rvert \ge 0.50$ falsified, marginal between. The omnibus separability tests use v1.10's locked three-wave rule: UNDETERMINED if fewer than two of $t_1$, $t_2$, $t_3$ are determined; otherwise FALSIFIED if $\lvert\rho\rvert \ge 0.50$ at any determined wave, CONFIRMED if $\lvert\rho\rvert \le 0.30$ at every determined wave, MARGINAL otherwise. Every $\rho$ carries a 95% bootstrap interval (units resampled within category, 10,000 draws); verdicts use the unrounded point estimate. Stability is tested with a one-sided stratified permutation test (later-wave scores permuted within category, 10,000 draws; $p = (\text{hits} + 1)/(N + 1)$). Judge agreement uses Krippendorff's ordinal $\alpha$ (Krippendorff, 2004) over every unit with valid outputs from both judges. **Noise guard:** if H1 or H4 is FALSIFIED, H2, H3, H5, H7 and H8 are reported as UNDETERMINED, with their statistics shown as descriptive only, because a noisy instrument is separable from everything.

## 2.7 Hypotheses

Table: Pre-registered hypotheses and decision rules (§5). MARGINAL otherwise in every row; UNDETERMINED as in §2.6.

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

H1 is the instrument gate: if it is FALSIFIED the AI-judged instrument is reported as not reliable; if it is MARGINAL every verdict carries that flag. H4 is a reliability floor, not a claim that Sentiment is fixed; H6 allows real change over five months. As a secondary row of H5, $\lvert\rho_w(S, R^*)\rvert$ is also reported within the eight early categories (band verdict). If H9 is FALSIFIED, S is also reported without J1-provider answers.

## 2.8 Sensitivity analyses and descriptives

Sensitivity analyses are reported next to the verdicts and never change one (§5.1): SU, every pooled statistic with the uncentred rank convention of the earlier programme papers; SD, every gate statistic without the Denon units of v0.19 (Declarations); NV in place of S, a model-balanced S (the mean of per-model means) and a J2-scored S, each for H2 and H3; $\alpha$ over the units both judges say refer to the brand. Pre-specified descriptives (§6): the cross-category baseline per category and panel; the convergence of $S_{\text{rec}}$ with the omnibus S in premium spirits; mean unit score by answering model, frame and panel; agreement detail (per-block $\alpha$, $\kappa$ on the evaluative flag, the J1 × J2 confusion matrix, self-consistency); and, as an exploratory row only, the agreement of J1's valence sign with archived per-brand labels written by a 2026 extraction model in five early sets.

## 2.9 Run, budget and order of analysis

Paid model calls are capped at US\$100 in total and 30,000 calls, enforced before every call and batch from the worst case of each request, with a pause for the author's approval at US\$80 of recorded spend (§7). A binding projection made after the first 200 calls of each judge decides, from token counts only, whether four pre-registered reductions of the early block apply, in a fixed order; the recognition and omnibus units and the Paper B sample are never reduced. Batches were not submitted while other programme collections ran, and the first allowed submission was 22 November 2026 (§8). Analysis ran in two stages: Stage J computed judge agreement (H1) and the self-consistency check from the frozen judge outputs without reading any Presence, Consistency or Ranking value; Stage C then opened them and computed H2--H9, the sensitivities and the descriptives. Both stages refuse to run without the pushed tag and its anchor record.

## 2.10 Pre-registration and deviations

The pre-registration, its judge prompt, unit table, Paper B sample, cost projection and scripts were locked at tag `{{PREREG_TAG}}` ({{PREREG_DATE}}) and deposited on OSF before the first judge call; the anchor record names the tag's commit and the deposit. {{DEV_SENTENCE}} Predictions were written before any judge call (§10): H1 marginal to confirmed, H2 marginal, H3 confirmed, H4 marginal, H8 confirmed.

# 3. Results

{% if SYNTHETIC %}
**Synthetic test build.** Every number and verdict in this section comes from synthetic scorer outputs (the scorer's dry run on synthetic replicas, or a scenario derived from it). They are not results.

{% endif %}
## 3.1 The judge run and data checks

The run recorded {{RECORDS}} judge responses, retries and repeats included, at a recorded spend of {{SPEND}} (batch {{SPEND_BATCH}}, synchronous {{SPEND_SYNC}}). The binding projection after {{CAL_J1}} calibration calls of J1 and {{CAL_J2}} of J2 measured {{OUT_J1}} and {{OUT_J2}} output tokens per call, reasoning included, and projected {{PLAN_USD}} with overhead; {{REDUCTION_SENTENCE}} {{REPLACEMENT_SENTENCE}} On the main pass J1 returned {{J1_VALID}} valid judgements, {{J1_FAIL}} JUDGE_FAIL and {{J1_UNJ}} UNJUDGED units; J2 returned {{J2_VALID}}, {{J2_FAIL}} and {{J2_UNJ}}. The highest JUDGE_FAIL share of any set was {{FAIL_MAX}}, below the 2% halt. {{SERVED_SENTENCE}}

The omnibus units joined the Presence and Consistency table one to one at every wave{% if JOIN_PASS %}{% else %} (not passed: see the verdict file){% endif %}. The number of omnibus windows differed from the Presence mention count in {{WINDOW_MISMATCH}} units, and the cross-check of Presence and $C^*$ against the v1.9 unit table found {{PC_DIFF}} differing rows of {{PC_ROWS}}. {{RANKING_SENTENCE}}

## 3.2 Judge agreement (H1) and self-consistency

Over {{H1_PAIRS}} units with valid outputs from both judges, ordinal $\alpha$ was {{H1_ALPHA}} ({{H1_ALPHA_REF}} over the units both judges said refer to the brand; recognition {{H1_ALPHA_R}}, omnibus {{H1_ALPHA_F}}, early sample {{H1_ALPHA_E}}), and Cohen's $\kappa$ on the evaluative flag was {{H1_KAPPA}}. Over {{H1_BRHO_N}} omnibus brand scores rated under both judges, the within-category brand correlation was {{H1_BRHO}} (95% CI {{H1_BRHO_LO}} to {{H1_BRHO_HI}}).
{% switch CASE_H1 %}
{% case CONFIRMED %}
Both statistics met the confirmed thresholds ($\alpha \ge 0.667$, $\rho \ge 0.80$): H1 is CONFIRMED, and the AI-judged instrument is read as reliable at the level the pre-registration requires.
{% case MARGINAL %}
Neither falsifying threshold was reached ($\alpha < 0.50$ or $\rho < 0.60$), but the confirmed thresholds were not both met: H1 is MARGINAL, and every verdict below carries that flag.
{% case FALSIFIED %}
At least one statistic fell below its falsifying threshold ($\alpha < 0.50$ or $\rho < 0.60$): H1 is FALSIFIED. The AI-judged instrument is reported as not reliable, and the noise guard applies.
{% case UNDETERMINED %}
The brand-level statistic did not meet its floor (at least 20 brand scores from at least three category-wave groups, with at least 20 unit pairs): H1 is UNDETERMINED, and no claim is made about the instrument's reliability.
{% endswitch %}

Figure 1 shows where the two judges' valences met and where they parted. Self-consistency (Table 2) measures the judges' own call-to-call variation on the repeat sample: overall exact valence agreement was {{SC_J1_ALL}} for J1 and {{SC_J2_ALL}} for J2.{% if SC_ANY_FLAG %} At least one judge and block fell below the 0.90 flag; the flag is reported, not acted on.{% else %} No judge and block fell below the 0.90 flag.{% endif %}

![Valence from J1 (rows) and J2 (columns) on every unit with valid outputs from both judges. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_01_judge_confusion.pdf){#fig:confusion width=82%}

Table: Self-consistency: each judge's second judgement of the fixed repeat sample, against its first (exact valence agreement, ordinal $\alpha$, $\kappa$ on the evaluative flag).

{{TABLE_SELFCON}}

## 3.3 Separability from Presence, Consistency and Ranking (H2, H3, H5)

Table 3 gives the per-wave statistics; Figure 2 places them against the bands.
{% switch CASE_H2 %}
{% case CONFIRMED %}
Against Presence, $\lvert\rho_w\rvert$ stayed at or below 0.30 at every determined wave: H2 is CONFIRMED: within category, Sentiment stayed in the separable band against how often and how widely a brand is named.
{% case MARGINAL %}
Against Presence, $\lvert\rho_w\rvert$ exceeded 0.30 at a determined wave without reaching 0.50 at any: H2 is MARGINAL.
{% case FALSIFIED %}
Against Presence, $\lvert\rho_w\rvert$ reached 0.50 at a determined wave: H2 is FALSIFIED. Sentiment moved with Presence, the failure the v1.7 lesson warns of.
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
Against Ranking ($R^*$, MNP), $\lvert\rho_w\rvert$ exceeded 0.30 at a determined wave without reaching 0.50 at any: H5 is MARGINAL. In the early categories, $\rho_w(S, R^*)$ was {{H5E_RHO}} over {{H5E_N}} brands (band verdict {{H5E_V}}).
{% case FALSIFIED %}
Against Ranking ($R^*$, MNP), $\lvert\rho_w\rvert$ reached 0.50 at a determined wave: H5 is FALSIFIED. In the early categories, $\rho_w(S, R^*)$ was {{H5E_RHO}} over {{H5E_N}} brands (band verdict {{H5E_V}}).
{% case UNDETERMINED_GUARD %}
Against Ranking, H5 is UNDETERMINED under the noise guard; its statistics are descriptive only.
{% case UNDETERMINED_WAVES %}
Against Ranking, fewer than two waves met the floor: H5 is UNDETERMINED.
{% case PENDING %}
H5 is PENDING: v1.10's own Stage C verdicts did not yet exist when this analysis ran, and v1.11 does not compute a Ranking statistic before v1.10 reports its own. H5 will be completed under this pre-registration.
{% case INACTIVE %}
H5 is INACTIVE: the scorer did not find tag `v1.10-prereg-r2`, which the pre-registration makes the condition for computing $R^*$.
{% endswitch %}

Table: Separability: $\rho_w$ of the Sentiment score with each comparator per wave, with 95% bootstrap interval and number of brand units (determined waves only; "n.d." = below the floor). H8 uses the recognition score in premium spirits (one category).

{{TABLE_SEP}}

![Within-category rank correlation of the Sentiment score with Presence, Consistency, Ranking and (recognition score) Presence, per wave, with 95% intervals and the separability bands. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_02_separability.pdf){#fig:sep width=100%}

## 3.4 Stability over three weeks and five months (H4, H6)

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
H6 is FALSIFIED by the size of the correlation; the pre-registration allows real change over five months, so this is not read as instrument noise on its own.
{% case FALSIFIED_P %}
H6 is FALSIFIED by the permutation test; the pre-registration allows real change over five months, so this is not read as instrument noise on its own.
{% case UNDETERMINED %}
Too few units met the floor: H6 is UNDETERMINED.
{% endswitch %}

![Rank correlation of each brand's Sentiment score between waves, with 95% intervals and the stability thresholds. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_03_stability.pdf){#fig:stab width=88%}

## 3.5 Secondary tests (H7, H8, H9)

In the eight early categories, the correlation of S with the number of answers naming the brand was {{H7_RHO}} (95% CI {{H7_LO}} to {{H7_HI}}; {{H7_N}} rated brands).
{% switch CASE_H7 %}
{% case CONFIRMED %}
H7 is CONFIRMED: in the early categories S did not track how often a brand is named.
{% case MARGINAL %}
H7 is MARGINAL.
{% case FALSIFIED %}
H7 is FALSIFIED: in the early categories S tracked how often a brand is named.
{% case UNDETERMINED_GUARD %}
H7 is UNDETERMINED under the noise guard; the statistic is descriptive only.
{% case UNDETERMINED_FLOOR %}
Too few brands or categories met the floor: H7 is UNDETERMINED.
{% endswitch %}
{% switch CASE_H8 %}
{% case CONFIRMED %}
The floor-free recognition score was separable from Presence at every determined wave (Table 3): H8 is CONFIRMED.
{% case MARGINAL %}
The recognition score's correlation with Presence exceeded 0.30 at a determined wave without reaching 0.50 (Table 3): H8 is MARGINAL.
{% case FALSIFIED %}
The recognition score's correlation with Presence reached 0.50 at a determined wave (Table 3): H8 is FALSIFIED.
{% case UNDETERMINED_GUARD %}
H8 is UNDETERMINED under the noise guard (Table 3, descriptive only).
{% case UNDETERMINED_WAVES %}
Fewer than two waves met the floor of 20 recognition brands: H8 is UNDETERMINED.
{% endswitch %}

On recognition and omnibus units judged validly by both judges and referring to the brand, J1 scored answers by its own provider's models {{H9_OWN}} points relative to J2 ({{H9_N_OWN}} units) and other answers {{H9_OTHER}} points ({{H9_N_OTHER}} units): $\Delta$ = {{H9_DELTA}} points (Figure 4).
{% switch CASE_H9 %}
{% case CONFIRMED %}
$\lvert\Delta\rvert$ was at most 5 points: H9 is CONFIRMED, and no self-preference of the primary judge was found.
{% case MARGINAL %}
$\lvert\Delta\rvert$ was between 5 and 10 points: H9 is MARGINAL.
{% case FALSIFIED %}
$\lvert\Delta\rvert$ reached 10 points: H9 is FALSIFIED, and S is also reported without J1-provider answers (§3.7).
{% case UNDETERMINED %}
One of the two groups had fewer than 20 units: H9 is UNDETERMINED.
{% endswitch %}

![Mean difference between the primary and the second judge's unit scores, for answers written by the primary judge's provider's models and for the other answers. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_04_self_preference.pdf){#fig:selfpref width=78%}

## 3.6 Verdicts

Table 4 lists every pre-registered test once, with the verdict as the scorer wrote it and, where the noise guard changed it, the word before the guard.{% if GUARD_ON %} The noise guard was applied: H1 or H4 was FALSIFIED.{% else %} The noise guard was not applied.{% endif %}{% if H1_FLAG %} Because H1 is MARGINAL, every verdict in the table carries that flag.{% endif %}

Table: Verdicts of the pre-registered tests (scorer's words).

{{TABLE_VERDICTS}}

## 3.7 Sensitivity analyses

{{SENS_SENTENCE}} Table 5 gives the verdicts under the uncentred rank convention (SU) and without Denon (SD); the per-wave statistics of the NV, model-balanced and J2-scored variants are in the appendix.

Table: Verdicts under the sensitivity analyses SU and SD (they never change a verdict; differences from the primary analysis are listed in the text).

{{TABLE_SENS}}

## 3.8 Cross-category baseline (descriptive)

Figure 5 shows the median and interquartile range of the rated brands' Sentiment scores in each category, wave and block. Median S ranged from {{BASE_F_MIN}} to {{BASE_F_MAX}} across the omnibus categories and waves and from {{BASE_E_MIN}} to {{BASE_E_MAX}} across the early categories. Mean unit score was {{PANEL_LEGACY}} on the legacy panel and {{PANEL_EARLY}} on the early panel. In premium spirits, the recognition score and the omnibus score correlated {{CONV_T1}}, {{CONV_T2}} and {{CONV_T3}} at $t_1$, $t_2$ and $t_3$ (brands rated in both: {{CONV_N1}}, {{CONV_N2}}, {{CONV_N3}}). The full baseline is in the appendix.

![Median and interquartile range of the rated brands' Sentiment scores per category, wave and block. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_05_baseline.pdf){#fig:base width=100%}

# 4. Discussion

{% switch CASE_OVERALL %}
{% case SEPARABLE %}
The AI-judged Sentiment instrument passed its reliability tests and was separable within category from the components already in the score. The result supports treating Sentiment as a candidate component, provisionally: separability shows that the score carries information Presence and Consistency do not, not that the information is valence as a human reader would judge it. That question belongs to Paper B.
{% case SEPARABLE_FLAGGED %}
The separability tests came out as the programme requires, but on an instrument whose two judges agreed only marginally. The verdicts stand as written and carry the flag. Marginal agreement between two models from different providers means the valence of a text is less determinate than the anchored scale assumes, or that one judge reads it differently; Paper B's human labels are the test of which.
{% case NOT_SEPARABLE %}
A primary separability test was falsified. Read with the v1.7 lesson, this is the outcome the gate exists to catch: a score that tracks another component adds no separate dimension to the composite, whatever its face validity. The result is published with the same prominence as a pass, and any redesign of the instrument requires its own pre-registration.
{% case MIXED %}
The primary tests did not all reach the confirmed band, and none of the primary separability tests (H2, H3, H5) was falsified. The evidence is therefore partial: Sentiment is not shown to move with the other components, nor shown to be clearly apart from them, and the marginal rows are the ones a redesign or a further wave would need to resolve.
{% case INSTRUMENT_FAILED %}
The two judges did not agree well enough for the instrument to be read. This is a result about the instrument, not about brand sentiment: the separability statistics would look favourable for a noisy score, which is why the noise guard withdraws them. A second instrument --- other judges, another scale or a human-labelled calibration --- would need its own pre-registration.
{% case UNSTABLE %}
The score did not keep its brand order over three weeks, a period short enough that real change in how models describe brands is not the expected explanation. Under the noise guard the separability statistics are descriptive only. Whether the instability lies in the judges or in the answers is a question for the self-consistency data and for Paper B.
{% case INSTRUMENT_UNDETERMINED %}
The instrument gate could not be determined on the units available, so the paper makes no claim about the instrument's reliability, and the remaining verdicts are read without that support.
{% endswitch %}
{% switch CASE_H2 %}
{% case CONFIRMED %}
The Presence result matters most for the programme: within category, Sentiment stayed in the separable band against Presence at every determined wave, although the pre-registration predicted a marginal result here because brands named often may be named in recommendation frames.
{% case MARGINAL %}
The Presence result was the one the pre-registration predicted: within category, Sentiment moved partly with Presence at one or more waves, without crossing the falsifying band; the direction is in Table 3.
{% case FALSIFIED %}
The Presence result is the decisive one: within category, Sentiment moved with Presence at a determined wave (the direction is in Table 3), so Sentiment as measured here partly re-measures how often and how widely a brand is named.
{% case UNDETERMINED_GUARD|UNDETERMINED_WAVES %}
The Presence test did not return a determined verdict, so the question the v1.7 lesson raises remains open for Sentiment.
{% endswitch %}

The study has two features that bound its reading. The answers were archived and written by panels that are not the newest models; the score describes those answers, not the current models. And the judge is a model: a systematic tilt shared by both judges would pass H1 and remain invisible here, which is why the human labels of Paper B, not this paper, decide whether "Sentiment" is the right name for what the instrument measures.

# 5. Limitations

The instrument is AI-judged and provisional until Paper B. The judges reason at their lowest available effort and no sampling parameter can be fixed, so a judge's output varies from call to call; the self-consistency check measures this variation, it does not remove it. The rating floor of six units restricts the range of Presence among rated omnibus brands, which can understate $\lvert\rho(S, P)\rvert$; H8 (floor-free) and H7 (early panel) are the checks. There is one judge pair, and self-preference is tested (H9), not removed: every judge provider also supplied answering models. The two answering panels are not the newest models, and the early categories have one wave each. S measures how answers describe brands, not consumer sentiment, and no behavioural validity is claimed. The window rule can miss evaluations far from the brand name and can carry a neighbouring sentence; Paper B's labels test the unit as well as the judge. Five of the eight early sets carry archived per-brand labels from a 2026 extraction model; they were never analysed before and enter only an exploratory descriptive. For budget reasons neither judge is its provider's flagship and J2 judged only a sample of the early windows (10% as planned; §3.1 reports any reduction); H1 and Paper B are the checks on that choice.

# 6. Future Research

Paper B labels a 566-unit sample drawn at the unit build, before any judge call, with the judge's instructions verbatim and two independent student labellers per unit, under its own pre-registration whose validation thresholds are fixed before the labels are read. Its planning date for the labels is 22 January 2027. If Sentiment is validated and separable, the calibration of a composite that includes it follows Ranking and Sentiment under its own pre-registration; Paper B also carries the stability and phrasing studies of the instrument.

# Declarations {-}

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance, at Samsung Electronics America. This study re-analyses answers collected against brand registries fixed in earlier phases; it performs no new brand selection, and each registry carries its source phase's conflict-of-interest handling forward unchanged (the source records are quoted verbatim in DEVIATIONS Entry 0 of the pre-registration). Two items of record apply. In the automotive registry (v0.22), Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands --- Harman International (audio systems), Samsung SDI (battery cells) and Samsung Display (infotainment) --- characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry (v0.19), AKG was substituted with Denon before the v0.19 pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary (v0.19 PRE_REGISTRATION §2.3; v0.19 paper, DEVIATIONS Entry 1). Correction (November 10, 2026): Harman International, a Samsung subsidiary since March 2017, completed its acquisition of Masimo's Sound United brands, Denon included, on September 23, 2025, so Denon, substituted for AKG before the v0.19 lock, was already a Samsung-group brand; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. Every gate statistic is therefore also reported without Denon (sensitivity SD). A string screen of all thirteen registries on November 10, 2026, for Samsung, Harman and the Harman and Sound United brand names listed in DEVIATIONS Entry 0, matched Denon (v0.19) only. Valence judging adds no brand choice and is fully automated against the locked registries and units, and the pre-registration was locked and deposited before any judge call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

## Funding {-}

Self-funded.

## Ethics {-}

Not applicable: no human subjects (archived AI answers judged by AI models). The Paper B human labelling is governed by Paper B's own pre-registration.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## Data and code availability {-}

Materials are deposited at OSF (osf.io/ec6wh), `methodology/v1_11/`: the locked pre-registration with its judge prompt, unit table, Paper B sample, parity, cost and precision records, the input manifest, the scorer and judge scripts with their tests, the lock manifest, the deviations record and the anchor record (`prereg/`, `registries/`, `anchor/`). At publication the deposit adds the frozen judge outputs with their usage records, the plan file, the unit outcomes, the Stage J and Stage C outputs (`stage_j_v1_11.json`, `v1_11_verdicts.json`) and the figure sources. The code is also in the programme's GitHub repository (github.com/thirdsystem-aias/aias) at tag `{{PREREG_TAG}}`.

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

Programme records cited by version, as the locked pre-registration names them (OSF `ec6wh`; github.com/thirdsystem-aias/aias): the pre-registrations of Methodology v1.10 (Ranking, tag `v1.10-prereg-r2`) and v1.11 (Sentiment, tag `v1.11-prereg-r1`); the omnibus registries of v0.19 (audiophile headphones, SSRN 6809182), v0.20 (skincare, SSRN 6811441), v0.21 (cosmetics, SSRN 6815378), v0.22 (automotive, SSRN 6829118) and v0.23 (premium spirits, SSRN 6834298). HARMAN press release, Business Wire, September 23, 2025, <https://www.businesswire.com/news/home/20250923135384/en/HARMAN-Completes-Sound-United-Acquisition-to-Expand-Premium-Audio-Leadership>.

\clearpage

# Appendix: pre-registered descriptives {-}

Table: Cross-category baseline (pre-registration §6.1): brands, brands rated, median and interquartile range of S, mean evaluative share E, and the shares of non-evaluative and mixed units and of units not referring to the brand, per block, category and wave.

{{TABLE_BASE}}

Table: Cross-category baseline, continued (pre-registration §6.1): judged units, J1's JUDGE_FAIL and UNJUDGED units, the share of bare windows (the brand's segments carry fewer than four other words) and the extraction misses of the unit build, per block, category and wave (recognition answers are whole answers, so no window is extracted).

{{TABLE_BASE2}}

Table: Ordinal $\alpha$ between J1 and J2 per block, and the variants of S for H2 and H3 (pre-registration §5.1): verdict and $\rho_w$ per wave.

{{TABLE_SENS_S}}

Table: Mean unit score by answering model and block (J1, valid units referring to the brand).

{{TABLE_MODEL}}

Table: Mean unit score by frame or prompt type and block (J1, valid units referring to the brand; frame identifiers as in the source studies).

{{TABLE_FRAME}}

The J1 × J2 confusion matrix of pre-registration §6.5 is Figure 1, which prints every count. {{LEGACY_SENTENCE}}
