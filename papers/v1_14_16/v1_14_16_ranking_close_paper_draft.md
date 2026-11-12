---
title: "Precedence Without Separation: Closing the Ranking Component of AI Brand Availability"
subtitle: "Two Pre-Registered Re-Analyses of Where Models Place Brands: the Modal Position and Co-Mention Precedence, Both MARGINAL on Separability from Presence (AIAS™ Methodology v1.14 and v1.16)"
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
  \usepackage{etoolbox}
  \AtBeginEnvironment{longtable}{\setstretch{1.1}}
  \setstretch{1.36}
  \setlength{\parskip}{8pt}
  \setlength{\parindent}{0pt}
  \renewcommand{\maketitle}{}
  \providecommand{\xmpquote}[1]{#1}
  \floatplacement{figure}{H}
---

\begin{titlepage}
\setstretch{1.0}
\setlength{\parskip}{0pt}
\begin{center}

{\LARGE \textbf{Precedence Without Separation: Closing the Ranking\\ Component of AI Brand Availability}}\\[8pt]

{\large Two Pre-Registered Re-Analyses of Where Models Place Brands: the Modal Position\\ and Co-Mention Precedence, Both MARGINAL on Separability from Presence\\ (AIAS™ Methodology v1.14 and v1.16)}\\[28pt]

Pablo Ulpiano González Castro\\[4pt]
School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System™ (research entity; data archive and methodology venue)\\[8pt]
Correspondence: pablou@pablou.com · pablou.com\\
ORCID: 0009-0003-8968-9990\\[20pt]

Pre-registrations: \texttt{v1.14-prereg-r2} and \texttt{v1.16-prereg-r1} (each locked and deposited on OSF before its confirmatory run)\\
Materials: OSF \texttt{ec6wh/methodology/v1\_14} and \texttt{ec6wh/methodology/v1\_16}\\

\end{center}
\end{titlepage}

# Abstract {-}

The AIAS™ program measures AI brand availability with two validated components, Presence and Consistency. Ranking, where a brand sits among the registry brands an answer names, given that it is named, was tested as a third; its first instrument (v1.10, mean normalised position) was reliable but not clearly separable from Presence. This paper closes the Ranking line with two pre-registered re-analyses, each run once. v1.14 confirmed the modal position, chosen after v1.10's sensitivity check, on an unseen fourth wave of the newest three-model panel: separable from Consistency ($\rho_w$ = 0.132, $n$ = 70) but not clearly from Presence ($\rho_w$ = 0.369, $n$ = 71) or, with search on, 0.496 (MARGINAL). v1.16 replaced position with co-mention precedence (PREC), a Bradley–Terry strength fitted from which brand comes first among brands named together, so that list length and rival mix cannot enter the score. PREC is highly reliable: its three-week retest is $\rho_w$ = 0.893 ($n$ = 53; permutation and within-answer shuffle $p$ = 0.0001) and its five-month retest 0.874. It is separable from Consistency at all four waves. Its correlation with Presence is 0.255, 0.411, 0.434 and 0.258 at the four waves, inside the 0.30 band at two and between the bands at two; with search on, 0.388. The gate is MARGINAL. Under the consequence clause fixed before the run, Ranking is reported as part of Presence, not as a separate AIAS component, and no further Ranking redesign follows. Among brands named together, those named more often tend to come first.

**Keywords:** AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; large language models; ranking; paired comparison; separability; measurement reliability

**JEL codes:** M31; L86; L15; D83; M37

**Paper status:** Two pre-registered methodology studies, reported together. Re-analyses of archived answers: no new data collection and no model calls. v1.14 (tag `v1.14-prereg-r2`): Stage 1 scored once on the fourth wave; Stage 1 verdict MARGINAL; its Stage 2 retest on a fifth wave runs for the record and cannot change the verdict. v1.16 (tag `v1.16-prereg-r1`): scored once after the lock and the OSF deposit; gate MARGINAL; consequence clause applied. Part of the AIAS measurement program.

# 1. Introduction

AI Availability --- the discoverability and representation of a brand in the outputs of large language models --- has been proposed as a third measurable layer of brand availability (González Castro, 2026, SSRN 6659000), beside the Mental and Physical Availability of the Ehrenberg-Bass tradition (Sharp, 2010; Romaniuk & Sharp, 2022). The Tri-System framework describes the AI Availability Score (AIAS) as a score built from several dimensions (González Castro, 2026, MSI Working Paper, Report No. 26-132). The program has validated two of them. Presence, how often a fixed panel of models recognizes and names a brand, was anchored across five product categories under the v1.6 protocol (SSRN 6816340; AIAS 1.0, SSRN 6817841). Consistency, whether the panel's models agree about a brand, reached a usable instrument only after its first version was falsified for moving with recall (v1.7, SSRN 6878818) and was replaced by the dispersion statistic $\varphi$ (v1.8, SSRN 6963359), scaled to $C^*$ in the v1.9 calibration (*One Score or Two?*). The AIAS 2.0 synthesis reports the two side by side.

## 1.1 Why a ranking component

Whether a brand is named at all is Presence's information; how evenly the models name it is Consistency's. A third piece of information is plausible: *where* a brand sits among the brands an answer names. A model that names a brand first in a list of recommendations treats it differently from one that names it seventh, and a buyer who reads the answer meets them in that order. A Ranking component would be worth adding to the score only if it carries information the first two do not. The risk is specific and was named in advance. In consumer markets, brands with more buyers also tend to score higher on loyalty and attitude measures (the Double Jeopardy pattern; Ehrenberg, Goodhardt & Barwise, 1990), and the brands a model names most often may also be the ones it names first. If so, a ranking score re-expresses Presence.

## 1.2 What v1.10 found

Ranking Paper A (v1.10; tag `v1.10-prereg-r2`) built a deterministic extractor that recovers each named registry brand's position in archived long-form answers and selected, blind to Presence and Consistency, the mean normalised position (MNP) as the rank statistic (split-half reliability 0.951 on the early panel). Its gate ran on the five omnibus categories at three waves of a six-model legacy panel. MNP was separable from Consistency and held its brand order over three weeks ($\rho_w$ = 0.897) beyond what list composition produces, but its within-category correlation with Presence was 0.275, 0.366 and 0.307 at $t_1$, $t_2$ and $t_3$: inside the confirmation band ($|\rho| \le 0.30$) at the first wave only. On the early panel it tracked recall share at 0.663 (FALSIFIED). The gate was MARGINAL, and Ranking was not added to the reported components.

## 1.3 This paper

Two further pre-registered studies followed, and this paper reports both. v1.14 took the one v1.10 candidate that had stayed inside the Presence band at every archived wave, the modal position (MODE), and, because it was chosen after seeing those waves, confirmed it on a wave it had not seen (§2.1). v1.16 diagnosed why both position statistics could carry Presence by construction and replaced position with co-mention precedence, which compares only brands named in the same answer (§2.2). Before v1.16 was locked, the author recorded that it would be the last Ranking redesign: if it did not pass, Ranking would be reported as part of Presence and not as a separate component (§2.3). Both studies returned MARGINAL. The paper's contribution is the result and what it locates: precedence among co-named brands is a highly reliable property of AI answers, distinct from Consistency, and it is tied to how often brands are named strongly enough, at two of four waves, to fail the program's bar for a separate component.

# 2. The two redesigns and their pre-registered gates

Both studies keep v1.10's construct, extractor (rules E0--E7, including the lead-item ordering rule), registries, unit (a brand within a category), rating floor of six rankable mentions, and conventions (§2.4). They change only the statistic and the data it is confirmed on.

## 2.1 v1.14: the modal position, confirmed on an unseen wave

**Statistic.** $R^*_b$ is minus the most frequent competition min-rank of brand $b$ over its rankable mentions, ties between modes broken toward the top. It was one of v1.10's six pre-registered candidates and was the only one whose correlation with Presence stayed inside the band at all three archived waves (0.093, 0.247, 0.206 in v1.10's sensitivity check, reproduced exactly by v1.14's calibration). The pre-registration states this selection history openly and treats the archived waves as calibration only.

**Confirmation data.** The fourth wave, $t_4$ (study v0.42, November 2026): the 30 category questions of the five omnibus categories asked of the newest panel (Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon), three runs each, without (S0) and with (S1) the provider's web search; 540 answers, 54 per category and condition. Presence and Consistency at $t_4$ follow the definition the program's Coverage and Grounding studies share.

**Stage 1 gate legs.** H1, $\rho_w(R^*, P)$ at $t_4$, search off; H2, $\rho_w(R^*, C^*)$; H4_S1, $\rho_w(R^*_{S1}, P_{S1})$, search on, downgrade-only. Separability is CONFIRMED iff $|\rho_w| \le 0.30$, FALSIFIED iff $|\rho_w| \ge 0.50$, MARGINAL otherwise, UNDETERMINED below 30 units. Separability legs against Coverage, Grounding and Sentiment were pre-registered as conditional; none was active at the lock. **Stage 2** is a $t_4 \rightarrow t_5$ retest (H3). The interim verdict after Stage 1 is MARGINAL if any leg is MARGINAL; under the author's decision recorded before the v1.14 lock, only a PASS opens a Ranking Paper B.

The pre-registration was locked at tag `v1.14-prereg-r2` on 10 November 2026 (r1 was superseded before any $t_4$ answer existed, DEVIATIONS Entry 1) and deposited on OSF; Stage 1 refused to run until v0.42's acquisition was locked, read the raw answers from that tag and the comparators from v0.42's scoring tag, and ran once on 11 November 2026 (01:43 UTC on 12 November).

## 2.2 v1.16: co-mention precedence

**Diagnosis.** MNP and MODE both summarise a brand's own positions over the answers that name it. In that frame, naming frequency can enter the score through two channels that belong to the statistic rather than to a ranking. *List length*: a rarely named brand tends to appear when a model goes further down its list, in longer answers, where absolute positions are larger. *Rival mix*: a brand's position depends on which rivals share the answer, and a frequently named brand meets a different mix of rivals from a rarely named one. A third channel is substantive: models may list brands in the order in which they associate them with the category, so that being named often and being named early are one fact. v1.10 and v1.14 cannot separate the three.

**Statistic.** For every pair of registry brands named in the same rankable answer, the brand with the smaller min-rank wins (ties give half a win to each); all such comparisons in a category, wave and condition are pooled over models, runs and questions into a win matrix, and PREC$_b$ is the brand's Bradley--Terry log-strength, fitted by maximum likelihood with one virtual comparison per brand against a reference of strength zero (which keeps every estimate finite and the maximum unique). PREC never uses an answer that names only one of the two brands, never uses an absolute position, and adjusts each head-to-head for the strength of the rival. By construction, appending brands after a pair leaves that pair's outcome unchanged, and naming frequency changes only the number of comparisons, not their expected outcome; both properties are unit-tested. The substantive channel is not removed, and should not be. The Bradley--Terry model is a standard paired-comparison model; no source for it is cited because the program's literature check has not verified one. A unit is rated with at least six rankable mentions and membership of its category's main comparison component.

**Why this measure, from outside evidence.** A practitioner study by SparkToro with Gumshoe (Fishkin, 2026; not peer-reviewed) found that the same brand list recurred in fewer than 1 in 100 answers and the same order in about 1 in 1,000, while how often a brand appeared was steadier than its position; Schulte, Bleeker and Kaufmann (2026) found same-day brand overlap of 0.327--0.477 and recommend at least seven runs per prompt per day. Both imply that a statistic built on a brand's full positions inherits that noise and falls back onto its steadiest part, which is Presence. But the top of an order can be concentrated: the abstract of Boffa, Farronato, Fedele, Levi and Mantovani (2026) reports that in 20 of 100 product and service categories a single product is listed first in more than three quarters of responses (the full text was not read). Head-to-head precedence uses the part of the order that can be stable and pools it over every answer of a category and wave.

**Data.** No answer was re-extracted. $t_1$--$t_3$ use v1.10's fifteen hashed omnibus rank tables (36 answers per category and wave, 161 rankable answers of 180 at each wave) and the locked AIAS 2.0 profiles table for $P$ and $C^*$; $t_4$ uses v1.14 Stage 1's hashed rank table and unit table. Every input was pinned by SHA-256, and a parity run before the lock reproduced every count v1.10 and v1.14 had published for these inputs, without computing any precedence value.

**Hypotheses and gate.** Table 1 lists the confirmatory tests. H1 and H2 keep v1.10's every-wave rule, now over four waves, the legacy panel ($t_1$--$t_3$) and the newest panel ($t_4$) together. H3 is v1.10's three-week retest, unchanged in rule and data. The gate FAILS if any of H1--H3 is FALSIFIED; is UNDETERMINED if any is UNDETERMINED; PASSES if all three are CONFIRMED and H4_S1 is not FALSIFIED; and is MARGINAL otherwise.

\needspace{14\baselineskip}

\begingroup\small

Table: v1.16 hypotheses. $\rho_w$ = pooled within-category Spearman correlation on centred ranks; separability CONFIRMED iff $|\rho_w| \le 0.30$ at every determined wave (H1, H2) or at $t_4$ (H4_S1), FALSIFIED iff $|\rho_w| \ge 0.50$ at any; reliability CONFIRMED iff $\rho_w \ge 0.50$ and both nulls $p < .05$, FALSIFIED iff $\rho_w < 0.30$ or either null $p \ge .05$. A wave is determined with at least 30 units; H1 and H2 need at least three of four determined waves.

| Tag | Tier | Statistic | Null (10,000 draws; seed) |
|:-------------------------|:-------------|:-----------------------------------|:-------------------------------|
| H1 Separable from Presence | primary (gate) | $\rho_w$(PREC, $P$) at $t_1$, $t_2$, $t_3$, $t_4$ | PREC permuted within category (116001), two-sided |
| H2 Separable from Consistency | primary (gate) | $\rho_w$(PREC, $C^*$) at $t_1$--$t_4$ | as H1 (116002) |
| H3 Retest, three weeks | primary (gate) | $\rho_w$(PREC$_{t_1}$, PREC$_{t_2}$) | (a) permutation (116003); (b) within-answer order shuffle, PREC refitted (116010); one-sided |
| H4_S1 Separability, search on | secondary (downgrade only) | $\rho_w$(PREC$_{S1}$, $P_{S1}$) at $t_4$ | as H1 (116004) |
| H5 Retest, five months | secondary | $\rho_w$(PREC$_{t_2}$, PREC$_{t_3}$) | as H3 (116005; 116010) |

\endgroup

**Predictions** (written before any PREC value existed): P1, PREC correlates positively with Presence; P2, its three-week retest is lower than MODE's archived 0.858, and higher in smaller and more concentrated categories; P3, it is separable from Consistency.

**Precision.** The pre-registration's analytic precision note states that the every-wave rule is demanding: a measure whose true correlation with Presence is 0.20 passes H1 with probability between 0.38 (independent waves) and 0.77 (fully dependent waves), one at 0.10 with probability between 0.77 and 0.93. A rule on a pooled estimate was considered and not used, because it would have been looser than the bar v1.10 and v1.14 faced.

A synthetic dry run in the real file formats, with three worlds of known answer (precedence independent of popularity, precedence equal to popularity, no precedence), returned the expected verdict in each world before the lock (pre-registration §11).

## 2.3 The consequence clause

On 11 November 2026, after v1.14's Stage 1, the author decided that v1.16 would be the last Ranking redesign, and that "if it does not PASS, Ranking is reported as part of Presence and not as a separate AIAS component; no further redesigns" (v1.16 DEVIATIONS Entry 0). The pre-registration carries the clause in §8, applies it to every outcome other than PASS, UNDETERMINED included, and states that no sensitivity, secondary result or later wave can turn the verdict into a PASS. The scorer prints the consequence next to the gate.

## 2.4 Conventions and order of operations

$\rho_w$ is v1.10's pooled within-category Spearman correlation: average ranks within each category, centred on the category's mean rank, then the Pearson correlation of the pooled centred ranks, over categories with at least five units; values are compared unrounded. Permutation $p$-values are $(h + 1)/(N + 1)$, so 0.0001 is the smallest value 10,000 draws can return. Bootstrap 90% intervals (units resampled within category, 2,000 draws, seed 110020) are reported and never enter a verdict.

v1.16 was locked at tag `v1.16-prereg-r1` (pushed 09:10:50 UTC on 12 November 2026), its folder was deposited on OSF with 13 files SHA-256 verified (09:12:34 UTC), and the anchor record was written (09:12:42 UTC). The scorer refuses to run without the tag, the anchor and an unchanged lock manifest, or if a results file exists. It ran once; the results file is dated 09:13:48 UTC.

# 3. Results

Every number in this section is read from `osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json` (v1.14) or `osf/methodology/v1_16/outputs/results_v1_16.json` (v1.16); the file `NUMBERS_PROVENANCE.md` beside this paper lists each with its key.

## 3.1 The modal position does not clear the Presence bar on the newest panel

All 540 answers of the fourth wave were answered and entered the analysis set; mention parity with v0.42's coded tables was 1.0000 in four categories and 0.9988 in spirits (2,589 of 2,592 cells, above the 0.98 requirement); the comparators matched v0.42's brand table on all 112 units in both conditions; and no model was dropped. 71 units were rated with search off.

\needspace{10\baselineskip}

Table: v1.14 Stage 1 on $t_4$ (newest panel). Two-sided permutation $p$; 90% bootstrap intervals.

| Hypothesis | $\rho_w$ | $n$ | $p$ | 90% interval | Verdict |
|:-----------------------------|:-----:|:---:|:-----:|:------------------:|:----------:|
| H1 Separable from Presence (search off) | 0.369 | 71 | 0.003 | [0.125, 0.561] | MARGINAL |
| H2 Separable from Consistency (search off) | 0.132 | 70 | 0.305 | [−0.083, 0.343] | CONFIRMED |
| H4_S1 Separable from Presence (search on) | 0.496 | 65 | 0.0002 | [0.267, 0.652] | MARGINAL |

**Stage 1 is MARGINAL.** The correlation of the modal position with Presence, 0.369, lies between the confirmation and falsification lines, as MNP's did at two archived waves, and is higher than any of the three archived calibration values (0.093 to 0.247), as the pre-registration expected of a statistic selected on the outcome. With search on it reaches 0.496, just below the falsification line. Separation from Consistency holds. The three component legs were inactive.

![Correlation of the modal-position score with Presence and Consistency on the fourth wave, with search off and on. Shaded: confirmation band ($|\rho_w| \le 0.30$, lower) and falsification band ($\ge 0.50$, upper).](figures/fig_1.pdf){width=100%}

The checks behaved as designed. The positive control (a penalised MNP that scores unnamed brands as last) tracked Presence at 0.930 ($n$ = 112), so the gate can detect a Ranking score that carries Presence. The modal position was not degenerate (the most common value was held by 0.211 of rated units, every category had spread). Run-to-run reliability of the score over the three $t_4$ runs was 0.868 (Spearman--Brown over three runs), against 0.045 when brand order was shuffled within answers. The search-off and search-on scores correlated at 0.792 ($n$ = 60), and the modal position correlated with MNP at 0.834 ($n$ = 71).

Two pre-set sensitivities read H1 CONFIRMED: a rating floor of ten (0.292, $n$ = 58) and the top-1 candidate (0.284, $n$ = 71). Every other sensitivity read MARGINAL, including the other v1.10 candidates (0.312 to 0.326), the first-mention rule (0.367), leaving out each category in turn (0.333 to 0.407) and uncentred ranks (0.414). Under v1.14's locked rule a sensitivity cannot turn a MARGINAL into a pass. Stage 2, the $t_4 \rightarrow t_5$ retest, runs for the record on the fifth wave (about 7 December 2026, by the v1.16 pre-registration) and cannot change the verdict.

## 3.2 Precedence and Presence: inside the band at two waves of four

PREC was rated for 55, 54, 54 and 71 units at $t_1$ to $t_4$ (65 at $t_4$ with search on); no unit at the rating floor fell outside its category's main comparison component at any wave.

\needspace{16\baselineskip}

Table: v1.16 gate hypotheses. Two-sided permutation $p$ for H1, H2 and H4_S1; one-sided $p$ for both nulls of H3 and H5. 90% bootstrap intervals.

| Hypothesis | Wave | $\rho_w$ | $n$ | $p$ | 90% interval | Verdict |
|:----------------------|:-------:|:-----:|:---:|:--------------|:------------------:|:----------:|
| H1 Separable from Presence | $t_1$ | 0.255 | 55 | 0.095 | [−0.010, 0.499] | |
| | $t_2$ | 0.411 | 54 | 0.007 | [0.150, 0.616] | |
| | $t_3$ | 0.434 | 54 | 0.004 | [0.278, 0.560] | |
| | $t_4$ | 0.258 | 71 | 0.040 | [0.017, 0.453] | MARGINAL |
| H2 Separable from Consistency | $t_1$ | 0.204 | 55 | 0.186 | [−0.067, 0.414] | |
| | $t_2$ | 0.071 | 54 | 0.652 | [−0.195, 0.319] | |
| | $t_3$ | 0.182 | 54 | 0.237 | [−0.061, 0.383] | |
| | $t_4$ | 0.139 | 70 | 0.281 | [−0.084, 0.361] | CONFIRMED |
| H3 Retest, three weeks | $t_1 \rightarrow t_2$ | 0.893 | 53 | perm 0.0001; shuffle 0.0001 | [0.756, 0.946] | CONFIRMED |
| H4_S1 Search on (secondary) | $t_4$ | 0.388 | 65 | 0.004 | [0.160, 0.560] | MARGINAL |
| H5 Retest, five months (secondary) | $t_2 \rightarrow t_3$ | 0.874 | 52 | perm 0.0001; shuffle 0.0001 | [0.708, 0.933] | CONFIRMED |

**H1 is MARGINAL.** The correlation of precedence with Presence is positive at every wave, as predicted (P1). It lies inside the confirmation band at $t_1$ (0.255) and $t_4$ (0.258) and between the bands at $t_2$ (0.411) and $t_3$ (0.434). At $t_3$ the 90% interval runs from 0.278 to 0.560. No wave reaches the falsification line. With search on (H4_S1), 0.388: MARGINAL, which cannot downgrade a gate that is already MARGINAL.

![Precedence against Presence at the four waves; legacy six-model panel at the first three, newest three-model panel at the fourth.](figures/fig_2.pdf){width=100%}

Removing the list-length and rival-mix channels did not remove the coupling. On the legacy panel PREC's correlation with Presence is at least as high as MNP's at $t_2$ and $t_3$ (§3.6); on the newest panel it is lower than the modal position's.

## 3.3 Precedence and Consistency: separable at every wave

**H2 is CONFIRMED,** as predicted (P3): $\rho_w$(PREC, $C^*$) is 0.204, 0.071, 0.182 and 0.139, inside the band at all four waves, and the smallest permutation $p$ is 0.186. Where a brand comes among the brands it is named with is not a re-expression of how evenly the models name it.

![Precedence against Consistency at the four waves.](figures/fig_3.pdf){width=100%}

## 3.4 Precedence is a stable property of the order

**H3 is CONFIRMED.** The brand order by precedence holds from $t_1$ to $t_2$ at $\rho_w$ = 0.893 ($n$ = 53), and both nulls return the smallest attainable $p$. The decisive null shuffles the order of the named brands within every answer, keeping which brands appear and how many, and refits PREC: the mean shuffled retest is 0.0001 (MQ7; flag threshold 0.20). The reliability is therefore a property of precedence, not of list composition. Over five months (H5, secondary), 0.874 ($n$ = 52), CONFIRMED. Contrary to P2, the three-week retest is higher than MODE's archived 0.858, not lower.

![Retest of precedence over three weeks and five months, against the mean of the within-answer shuffle null.](figures/fig_4.pdf){width=100%}

## 3.5 The gate and its consequence

H1 MARGINAL, H2 CONFIRMED, H3 CONFIRMED, H4_S1 MARGINAL: **the v1.16 gate is MARGINAL.** The scorer printed the pre-registered consequence with it: Ranking is reported as part of Presence and not as a separate AIAS component, and there is no further Ranking redesign. The positive control from the published record (penalised MNP against Presence: 0.909, 0.901 and 0.918 at $t_1$--$t_3$, 0.930 at $t_4$; $n$ = 112) passes, and neither the negative control (MQ7) nor the identification check (MQ9) is flagged.

\needspace{26\baselineskip}

## 3.6 Sensitivities and the three statistics compared

\begingroup\footnotesize\setlength{\tabcolsep}{4pt}

Table: v1.16 sensitivities of H1 and H2 ($\rho_w$ at $t_1$ / $t_2$ / $t_3$ / $t_4$). Bold: a verdict that differs from the primary one. None changes the gate (pre-registration §8).

| Analysis | H1 $\rho_w$(PREC, $P$) | H1 | H2 $\rho_w$(PREC, $C^*$) | H2 |
|:--------------------|:------------------------------:|:----------:|:------------------------------:|:----------:|
| Primary | 0.255 / 0.411 / 0.434 / 0.258 | MARGINAL | 0.204 / 0.071 / 0.182 / 0.139 | CONFIRMED |
| S1 first-mention rule | 0.247 / 0.411 / 0.441 / 0.223 | MARGINAL | 0.187 / 0.071 / 0.170 / 0.118 | CONFIRMED |
| S2 floor 3 | 0.330 / 0.288 / 0.412 / 0.403 | MARGINAL | 0.204 / 0.071 / 0.182 / 0.139 | CONFIRMED |
| S2 floor 10 | 0.659 / 0.731 / 0.468 / 0.175 | **FALSIFIED** | 0.293 / 0.090 / 0.282 / 0.279 | CONFIRMED |
| S7 without Denon | 0.255 / 0.411 / 0.434 / 0.258 | MARGINAL | 0.204 / 0.071 / 0.182 / 0.139 | CONFIRMED |
| S-COI (106-unit registries) | 0.246 / 0.373 / 0.409 / 0.306 | MARGINAL | 0.149 / 0.060 / 0.109 / 0.034 | CONFIRMED |
| S9 uncentred ranks | 0.345 / 0.491 / 0.496 / 0.310 | MARGINAL | 0.300 / 0.196 / 0.271 / 0.185 | **MARGINAL** |
| S_w weight $1/(k-1)$ | 0.299 / 0.373 / 0.364 / 0.314 | MARGINAL | 0.234 / 0.105 / 0.082 / 0.154 | CONFIRMED |
| S_prior $\lambda$ = 0.1 | 0.247 / 0.425 / 0.434 / 0.250 | MARGINAL | 0.201 / 0.062 / 0.182 / 0.119 | CONFIRMED |
| S_prior $\lambda$ = 10 | 0.284 / 0.402 / 0.452 / 0.277 | MARGINAL | 0.189 / 0.058 / 0.170 / 0.142 | CONFIRMED |
| S4 without headphones | 0.227 / 0.385 / 0.418 / 0.206 | MARGINAL | 0.242 / 0.124 / 0.258 / 0.171 | CONFIRMED |
| S4 without skincare | 0.290 / 0.457 / 0.500 / 0.278 | MARGINAL | 0.192 / 0.060 / 0.210 / 0.109 | CONFIRMED |
| S4 without cosmetics | 0.172 / 0.362 / 0.262 / 0.277 | MARGINAL | 0.238 / 0.118 / 0.132 / 0.143 | CONFIRMED |
| S4 without automotive | 0.243 / 0.284 / 0.296 / 0.234 | **CONFIRMED** | 0.033 / −0.046 / −0.016 / 0.017 | CONFIRMED |
| S4 without spirits | 0.316 / 0.514 / 0.618 / 0.311 | **FALSIFIED** | 0.274 / 0.075 / 0.253 / 0.276 | CONFIRMED |

\endgroup

The scorer lists four verdict changes. Two point toward a stronger coupling: among brands named often enough to reach a floor of ten (31 to 58 units), the correlation with Presence reaches 0.659 and 0.731 on the legacy panel, and without spirits it reaches 0.514 at $t_2$ and 0.618 at $t_3$. One points the other way: without automotive, H1 would be CONFIRMED (every wave between 0.234 and 0.296). Uncentred ranks move H2 to MARGINAL at $t_1$ (0.300, compared unrounded). Without the brands of record in the Declarations (S7, S-COI) every verdict is unchanged. Without skincare, the $t_3$ value (0.4995) lies just below the falsification line.

\needspace{8\baselineskip}

Across the three statistics the coupling is a matter of degree, not of kind (Figure 5). On the legacy panel PREC shares most of its information with MNP ($\rho_w$(PREC, MNP) = 0.923, 0.951, 0.939 at $t_1$--$t_3$; 0.952 at $t_4$) and less with MODE (0.717, 0.713, 0.781; 0.816). On the early panel, where v1.10's H4 had falsified MNP at 0.663, PREC's correlation with recall share is 0.687 ($n$ = 154; exploratory E3). With search on and off at $t_4$, PREC correlates at 0.786 ($n$ = 60).

![Correlation with Presence of the three Ranking statistics by wave: MNP from v1.10 ($t_4$ value from v1.14's sensitivity check), MODE from v1.14 (calibration at $t_1$--$t_3$, confirmatory at $t_4$) and PREC from v1.16.](figures/fig_5.pdf){width=100%}

# 4. Exploratory moderators (v1.16 E1)

The literature check suggested that position may be informative where the top of the order is concentrated and in smaller categories. v1.16 declared two moderators before any precedence value existed and reports them as exploratory: *category size* (registry brand count: 16 for headphones, 24 for the other four, so a contrast of one category against four, not a gradient) and *first-position concentration* (FPC: the share of a category's rankable answers, in one wave, in which the modal first brand is first). With five categories these are descriptions, not tests, and they change no verdict.

\needspace{16\baselineskip}

\begingroup\footnotesize\setlength{\tabcolsep}{4pt}

Table: Exploratory moderators by category, values at $t_1$ / $t_2$ / $t_3$ / $t_4$ (search off). FPC = first-position concentration; modal first brand as recorded in the results file (spirits as registry keys). Within-category Spearman $\rho$(PREC, $P$) over 8 to 18 rated brands. Retest = within-category $\rho$(PREC$_{t_1}$, PREC$_{t_2}$).

| Category (size) | FPC | Modal first brand | $\rho$(PREC, $P$) | Retest ($n$) |
|:------------------|:------------------------------:|:--------------------|:--------------------------------:|:---------:|
| Headphones (16) | 0.567 / 0.667 / 0.600 / 0.519 | Sennheiser (all) | 0.647 / 0.771 / 0.639 / 0.806 | 0.833 (8) |
| Skincare (24) | 0.417 / 0.472 / 0.389 / 0.685 | CeraVe (all) | 0.018 / −0.017 / −0.151 / 0.132 | 0.933 (9) |
| Cosmetics (24) | 0.257 / 0.257 / 0.250 / 0.259 | Fenty Beauty; Charlotte Tilbury ($t_3$); Rare Beauty ($t_4$) | 0.403 / 0.493 / 0.822 / 0.188 | 0.989 (13) |
| Automotive (24) | 0.444 / 0.444 / 0.472 / 0.500 | Toyota (all) | 0.276 / 0.628 / 0.654 / 0.367 | 0.811 (14) |
| Spirits (24) | 0.208 / 0.208 / 0.217 / 0.217 | S11; S17 ($t_4$) | −0.369 / −0.557 / −0.735 / 0.169 | 0.917 (9) |

\endgroup

Across the 20 category-wave cells, the absolute within-category correlation with Presence is unrelated to FPC (Spearman 0.055) and correlated with category size at −0.520: the smaller headphones category carries the strongest coupling at three of the four waves. The retest expectations of P2 are not borne out: the smallest and most concentrated category has the second-lowest retest (0.833), and cosmetics, the least concentrated category apart from spirits, has the highest (0.989).

![Within-category correlation of precedence with Presence against first-position concentration, one point per category and wave.](figures/fig_6.pdf){width=100%}

Two descriptive patterns stand out. First, the categories differ more than the pooled values show. The coupling is strong in headphones and, at two or three waves, in automotive and cosmetics; it is near zero in skincare; and in spirits on the legacy panel it is negative (precedence goes with *lower* Presence), which is why leaving spirits out moves H1 into the falsification band (§3.6). Second, concentration at the top does not by itself make precedence separable: skincare at $t_4$ has the highest FPC of any cell (0.685) and a low coupling, headphones has high FPC and the highest coupling. Category size cannot be separated from category identity with one small category. These patterns are leads; they are not confirmed by any test here, and the consequence clause leaves no Ranking Paper B to test them.

# 5. What it means

Three redesign attempts have now asked the same question of the same construct with progressively stricter instruments, and the answers agree. Where a brand sits among the brands an answer names is a real and stable property of AI answers. Precedence holds its order over three weeks (0.893) and five months (0.874), and that stability vanishes when the order within answers is shuffled (0.0001). It is distinct from Consistency at every wave on two panels. These are properties a component needs, and PREC has them more clearly than either position statistic.

What precedence does not do is stay clear of Presence by the bar the program set for a separate component. At $t_1$ and $t_4$ it does; at $t_2$ and $t_3$ it does not, and at $t_3$ the interval barely reaches below the line. This matters because PREC was built to remove the two ways in which frequency could enter a position score by construction. With list length and rival mix removed, what remains is the substantive channel the v1.16 pre-registration named: among the brands an answer names together, the models tend to put first the brands they name most often across prompts. A plausible mechanism, not tested here, is that models open an answer with the brands most typical of the category, and those are the brands they name across most prompts. In marketing terms this resembles a Double Jeopardy regularity in AI answers (Ehrenberg, Goodhardt & Barwise, 1990): the brands with more presence also get the better places among their rivals. On this evidence, that overlap is not an artefact of how position was summarised.

The pre-registered rule therefore applies without discretion. Ranking is reported as part of Presence and not as a separate AIAS component; there is no further Ranking redesign, and no later wave, including $t_5$, can turn this verdict into a pass. Presence and Consistency remain the program's reported components for availability, and the next component to pass its gate makes the next release. The position results of v1.10, v1.14 and v1.16 remain available as descriptions of Presence: where a brand sits among co-named brands, at a given wave, is a legitimate description of how a model presents it, labelled as such and never added to the score.

The result should not be pushed further than it goes. Separability failed by degree (0.411 and 0.434 against a 0.30 bar; no wave at 0.50), the rule was demanding by design (§2.2), and single categories move the pooled values in both directions (§3.6). A reader who sets a looser bar could reach a different reporting decision on the same numbers; the program fixed its bar before seeing PREC, and it holds to it.

# 6. Limitations

All four waves had been analysed with other position statistics before v1.16 existed, and the decision to build a frequency-free measure was taken after seeing that MNP and MODE track Presence; the statistic, rules, thresholds and data were fixed before any precedence value was computed (v1.16 pre-registration §4.3). v1.14's statistic was chosen after seeing the three archived waves; only its fourth-wave confirmation is evidence.

PREC pools one precedence per brand per wave over models; models that disagree on order lower its reliability, which H3 tested on the legacy panel only. The newest panel has a single wave in the archive, so its retest belongs to v1.14 Stage 2 and is reported for the record only. Each comparison rests on 52 to 71 rated brands, 8 to 18 per category, and roughly half of the 112 units are not rated at the legacy waves; the result is about brands named often enough to have a position. The every-wave rule has limited power for true correlations near 0.20 (§2.2). The H1 values at $t_2$ and $t_3$ would be lower under some sensitivities and higher under others (§3.6).

Positions are among registry brands only; position in text is not visual prominence, and the lead-item rule relies on Markdown conventions. Five categories, US English, provider-default settings; Presence at $t_4$ rests on one recognition answer per model. The outside evidence that motivated PREC includes a study that is not peer-reviewed (Fishkin, 2026) and a paper checked from its abstract only (Boffa et al., 2026). The exploratory moderators (§4) rest on five categories and twenty cells, one of them the only small category.

# Declarations {-}

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. Both studies re-analyse archived answers already scored against brand registries fixed in earlier phases; they perform no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward (v1.10 DEVIATIONS Entry 0; v1.14 DEVIATIONS Entry 0; v1.16 DEVIATIONS Entry 0). Three items of record apply to the registries used.

*Audiophile headphones (v0.19).* The v0.19 record states: "The panel substitution of AKG → Denon documented in §5 was made out of an abundance of caution given that Samsung's subsidiary Harman International owns AKG; the substitution occurred prior to pre-registration lock." (v0.19 paper, Declaration of interest; see also v0.19 pre-registration §2.3 and v0.19 DEVIATIONS Entry 1.) Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. Source: HARMAN, "HARMAN Completes Sound United Acquisition to Expand Premium Audio Leadership", press release, Business Wire, September 23, 2025. In both studies Denon remains in the locked registry and in the primary analysis; the separability tests against Presence and Consistency are also reported without the Denon unit (sensitivity S7).

*Automotive (v0.22).* The v0.22 record states: "Samsung subsidiaries hold tier-2/3 component supply relationships with several brands in the v0.22 registry: Harman International (audio systems) supplies Mercedes-Benz, BMW, and other premium automotive OEMs; Samsung SDI (battery cells) supplies BMW (i-series), Volkswagen Group brands including Bentley and Porsche (Stellantis-adjacent platforms), and others; Samsung Display (infotainment) supplies Mercedes-Benz and BMW. Tesla and Polestar also have tangential Samsung-component exposure at the parts level. These are non-competitive supply relationships; Samsung Electronics America does not produce or market passenger car brands and has no brand-level competitive overlap with any v0.22 registry entry. The COI was screened and documented in DEVIATIONS Entry 0 (Part B) of the pre-registration module; no operational restriction on registry composition was imposed." (v0.22 paper, Conflict of interest.) These are supply relationships, not ownership; no v0.22 brand is removed in either study.

*Agency work (Cheil Worldwide and Iris).* Cheil Worldwide, a marketing company of the Samsung group in which Samsung Electronics holds 28.43%, or its agency Iris has done advertising, public-relations or search-marketing work for five registry brands: Chevrolet (for GM Korea, 2017), BMW (UK consumer public relations, 2018), Bentley (experiential agency of record in the Americas from 2021), Jack Daniel's (UK digital agency from 2022, since replaced) and Eucerin (search marketing for Beiersdorf from 2024). (Conflict-of-interest screen of v0.62, DEVIATIONS Entry 0, Part F.) As Denon, these five brands stay in every analysis, and every separability statistic is also reported without them and Denon (sensitivity S-COI, 106 units). (v1.16 pre-registration §15; v1.14 predates this screen and reports S7 only.)

Extraction and scoring are automated against the locked registries and the locked pre-registrations. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

## Funding {-}

Self-funded. No external funding supported this research.

## Ethics {-}

Not applicable; no human subjects. The studies analyse archived responses of large language models queried under their public interfaces.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## Data and code availability {-}

*v1.16.* OSF `ec6wh`, `methodology/v1_16`: the locked pre-registration, lock manifest, input-parity record, precision note, dry run with its synthetic worlds, deviations record and README (13 files SHA-256 verified at the deposit), with the scorer and its tests staged in `methodology/v1_16/code/` (pre-registration §12). Repository github.com/thirdsystem-aias/aias, tag `v1.16-prereg-r1` (commit `5afa7d6`); the scorer `scripts/score_v1_16.py` imports `scripts/score_v1_10.py` and `scripts/score_v1_14.py` unchanged. The results file `osf/methodology/v1_16/outputs/results_v1_16.json` (with the per-unit PREC table) and the run log `outputs/run_v1_16.log` are on branch `v1.16` (commit `b6f5749`) and join the OSF deposit with this paper.

*v1.14.* OSF `ec6wh`, `methodology/v1_14/r2/` (pre-registration, calibration, anchor; r1 kept under `methodology/v1_14/`). Repository tag `v1.14-prereg-r2`; scorer `scripts/score_v1_14.py`. The Stage 1 outputs (`osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json`, the hashed $t_4$ rank table and the log) are on branch `v1.14` (commit `3129674`) and join the OSF deposit with this paper. Stage 2 will write `outputs/stage2/`.

*Inputs.* v1.10's rank tables and verdicts (OSF `ec6wh/methodology/v1_10`; tag `v1.10-prereg-r2`); the AIAS 2.0 profiles table (`osf/aias_2_0/aias_2_0_profiles.csv`); the $t_4$ answers of v0.42 (tags `v0.42-acquisition-locked` and `v0.42-scoring-locked`). The underlying answers are deposited with their source studies.

# References {-}

Boffa, F., Farronato, C., Fedele, A., Levi, E., & Mantovani, A. (2026). *An Empirical Audit of LLM Product Recommendations*. NET Institute Working Paper No. 26-09. <https://econpapers.repec.org/RePEc:net:wpaper:2609> (checked against the EconPapers record and abstract only; full text not read).

Ehrenberg, A. S. C., Goodhardt, G. J., & Barwise, T. P. (1990). Double jeopardy revisited. *Journal of Marketing, 54*(3), 82--91.

Fishkin, R. (2026, January 27). *NEW Research: AIs are highly inconsistent when recommending brands or products; marketers should take care when tracking AI visibility*. SparkToro blog; research partner Patrick O'Donnell (Gumshoe.ai). Not peer-reviewed. <https://sparktoro.com/blog/new-research-ais-are-highly-inconsistent-when-recommending-brands-or-products-marketers-should-take-care-when-tracking-ai-visibility/>

González Castro, P. U. (2026). *AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval*. SSRN 6659000.

González Castro, P. U. (2026). *Tri-System Brand Growth: The AI Mediation Layer*. MSI Working Paper, Report No. 26-132. Marketing Science Institute.

González Castro, P. U. (2026). *Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension* (AIAS Methodology v1.6). SSRN 6816340.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol: CPC Consistency --- A Pre-Registered Negative Result* (v1.7). SSRN 6878818.

González Castro, P. U. (2026). *A Mean-Independent Consistency Instrument for Cross-Model AI Presence: Redesigning CPC on a Quasi-Binomial Dispersion Basis* (AIAS Methodology v1.8). SSRN 6963359.

González Castro, P. U. (2026). *One Score or Two? Calibrating a Presence and Consistency Composite for AI Brand Availability: A Pre-Registered Calibration with Blind Five-Month Confirmation* (AIAS™ Methodology v1.9). Third System, <https://thirdsystem.ai/studies/v1-9/>; OSF, <https://osf.io/ec6wh/files/osfstorage/6af1fd459966c813ee53ba87>.

González Castro, P. U. (2026). *AI Availability as a Third Measurable Layer of Brand Availability: Five-Substrate Empirical Anchoring of the AIAS™ Presence Measurement Protocol* (AIAS 1.0). SSRN 6817841.

González Castro, P. U. (2026). *Presence and Consistency: A Two-Component Measurement of AI Availability* (AIAS 2.0). Working paper; OSF `ec6wh/aias_2_0`.

González Castro, P. U. (2026). *Where a Brand Sits in an AI Answer: A Reliable Ranking Instrument That Does Not Pass Its Separability Gate* (AIAS™ Methodology v1.10). Working paper; OSF `ec6wh/methodology/v1_10`.

González Castro, P. U. (2026). *Recognition Ceiling, Dissociation Replication, and Cultural-Channel Asymmetry on an Audiophile Headphones Substrate* (v0.19). SSRN 6809182.

González Castro, P. U. (2026). *Type 2 Emergence and First Prospective v1.5 C2 Calibration on a Skincare IL-Gradient Substrate* (v0.20). SSRN 6811441.

González Castro, P. U. (2026). *Type 2 Confirmation, Recognition Ceiling, and Phantom Brand Persistence on a Cosmetics IL-Gradient Substrate* (v0.21). SSRN 6815378.

González Castro, P. U. (2026). *Phantom Brand Persistence on a Heritage-Saturated Automotive Substrate: Cell D\_Defunct as Pure-Phantom Upper-Bound Test* (v0.22). SSRN 6829118.

González Castro, P. U. (2026). *AIAS Presence Index v0.23: Premium Spirits* (v0.23). SSRN 6834298.

Romaniuk, J., & Sharp, B. (2022). *How Brands Grow, Part 2* (Revised ed.). Oxford University Press.

Schulte, J., Bleeker, M., & Kaufmann, P. (2026). *Don't Measure Once: Measuring Visibility in AI Search (GEO)*. arXiv 2604.07585. <https://arxiv.org/abs/2604.07585>

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

Programme records cited by version (OSF `ec6wh`; github.com/thirdsystem-aias/aias): the pre-registrations of Methodology v1.14 (tag `v1.14-prereg-r2`) and v1.16 (tag `v1.16-prereg-r1`) with their deviations records; the $t_2$ wave (v0.34) and $t_3$ wave (v0.41) of the omnibus categories; the $t_4$ wave, v0.42 (tags `v0.42-acquisition-locked`, `v0.42-scoring-locked`); the conflict-of-interest screen of v0.62 (DEVIATIONS Entry 0, Part F). HARMAN press release, Business Wire, September 23, 2025.
