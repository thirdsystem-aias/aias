---
title: "Coverage of Buying Situations in AI Answers about Brands"
subtitle: "Instrument, Cross-Category Baseline and Separability Gate for a Third Component of AI Availability (AIAS™ Methodology v1.12)"
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

{\LARGE \textbf{Coverage of Buying Situations in AI Answers about Brands}}\\[8pt]

{\large Instrument, Cross-Category Baseline and Separability Gate\\ for a Third Component of AI Availability (AIAS™ Methodology v1.12)}\\[28pt]

Pablo Ulpiano González Castro\\[4pt]
School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System™ (research entity; data archive and methodology venue)\\[8pt]
Correspondence: pablou@pablou.com · pablou.com\\
ORCID: \href{https://orcid.org/0009-0003-8968-9990}{0009-0003-8968-9990}\\[20pt]

Pre-registration: \texttt{ v1.12-prereg-r1 } (commit \texttt{ 49efc473a6 }; deposited on OSF before the first v1.12 call)\\
Data and code: OSF \texttt{ec6wh}, \texttt{methodology/v1\_12}\\

\end{center}
\end{titlepage}

# Abstract {-}

Presence records whether AI answers name a brand; it does not record whether the brand is named across the buying situations of its category or only in a few. This pre-registered study specifies a Coverage instrument for the AIAS measurement programme and tests whether it is a separate component. Seventy brand-free questions, one per category entry point (14 per category, two for each of seven cue types), were asked in three runs to the newest flagship model of each of three providers (Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon) and to Claude Opus 5.5, over five categories and 112 brands; 900 of 900 calls were answered. The component score, Cov*, measures within each model how many situations a brand's mentions touch against the number expected if the brand were named without regard to the situation, given the same number of mentions; 51 brands met its rating floor.
The situations changed which brands were named (instrument check passed: brand sets overlapped 0.406 more between runs of one question than between questions).
Within category, Cov* correlated with Presence at ρ = 0.055 (H1 CONFIRMED), with Consistency at ρ = -0.060 (H2 CONFIRMED) and with the brand's own naming rate at ρ = 0.046 (H3 CONFIRMED); its split-half reliability was 0.646 (H4 CONFIRMED).
Every gate leg was confirmed, and the pre-registered gate returned PASS: Coverage breadth is a component separable from Presence and Consistency, and the instrument passes to a second paper.
The cross-category baseline reports raw and rate-adjusted Coverage per category, model and cue type on the newest models.

**Keywords:** AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; category entry points; large language models; Coverage; separability; measurement validity; Double Jeopardy

**JEL codes:** M31; L86, L15, D83, M37

**Paper status:** Pre-registered methodology paper with new acquisition (tag `v1.12-prereg-r1`, deposited on OSF before the first call); 900 of 900 design calls answered; Paper A verdict PASS; deviations recorded in `osf/methodology/v1_12/anchor/DEVIATIONS.md` (1 dated entry). Part of the AIAS measurement programme.

# 1. Introduction

AI Availability --- the discoverability and representation of a brand in the outputs of large language models (LLMs) --- has been proposed as a third measurable layer of brand availability (González Castro, 2026, SSRN 6659000), beside the Mental and Physical Availability of the Ehrenberg-Bass tradition (Sharp, 2010; Romaniuk & Sharp, 2016), within the Tri-System framework (González Castro, 2026, MSI Working Paper 26-132). The AIAS programme builds its components one at a time, each locked before it is used. Presence is whether and how often models name a brand (Methodology v1.6, SSRN 6816340; AIAS 1.0, SSRN 6817841). Consistency is whether the models of a panel agree about a brand, measured by the mean-independent dispersion statistic $\varphi$ (Methodology v1.8, SSRN 6963359) and scaled to $C^*$ (Methodology v1.9, *One Score or Two?*). The first Consistency instrument failed its separability test because it moved with how often a brand is named (Methodology v1.7, SSRN 6878818); its replacement passed, and the AIAS 2.0 synthesis reported the two components side by side.

A buyer meets a category in situations: a gift for a relative, a first purchase on a tight budget, a product for hot weather. Ehrenberg-Bass research calls these category entry points (CEPs) and treats the number of CEPs a brand is linked to as a core part of its Mental Availability (Romaniuk & Sharp, 2016). The analogue for AI answers is Coverage: in how many of a category's buying situations an AI answer names the brand. Presence asks whether the brand is named in general category questions; Consistency asks whether the models agree; Coverage asks whether a brand's naming spreads across situations or is tied to a few.

Coverage has a known problem before any data. In the Ehrenberg-Bass record CEP linkage follows Double Jeopardy: bigger brands are linked to more CEPs. A raw count of the situations in which a brand is named should therefore track Presence, and a component built on it would repeat the failure of v1.7. The programme's plan of record set the task of a first Coverage paper as three parts: an instrument specification, a cross-category baseline, and a separability gate against Presence, Consistency and the other components. This paper reports all three under one pre-registration. The component score is a rate-adjusted breadth, Cov*, designed so that the number of mentions alone does not move it (§2.4); the raw share of situations covered is reported beside it, with the warning that it is expected to follow Presence.

The study contributes an instrument check (do brand-free situation questions change which brands are named?), four primary gate legs (separability from Presence, from Consistency and from the brand's own naming rate, and split-half reliability), conditional legs for Ranking and Sentiment, two secondary tests, a pre-registered set of sensitivity analyses, and a descriptive baseline on the newest models. The gate decides whether a second Coverage paper, with the typology and robustness studies, follows on this instrument.

# 2. Method

## 2.1 Categories, brands and situations

The study uses the five categories of the programme's omnibus and their 112 brand units, unchanged: v0.19 audiophile headphones (16 brands), v0.20 skincare, v0.21 cosmetics, v0.22 automotive and v0.23 premium spirits (24 each). No brand was added, removed or renamed, and each registry keeps its source-phase handling.

For each category the pre-registration fixed 14 CEPs, two for each of seven cue types (why, when, where, while, with whom, with what, how feeling). The cue list is the programme's own operationalisation of category entry points after Romaniuk and Sharp (2016), not a published list. The CEPs were drafted under rules fixed before drafting: no CEP names a brand, uses a superlative or repeats a Presence question, headphone situations stay inside audiophile listening, and every set keeps the two-per-cue balance. Each set is split into halves A and B of seven CEPs, one per cue type. Each probe reads `<situation> Which <noun> brands would you suggest? Name several brands.` (automotive: "…would you suggest buying new?…"), with no system prompt. One control probe per category (C0) asks the category question without a situation. The 75 probes (70 CEP and 5 control) are in the deposited probe file; a check of every registry alias against them found no brand name (`MC_BrandFree`, run at the lock).

## 2.2 Panels, conditions and design

Panel N3 comprises the newest generally available flagship model of each provider: Claude Fable 5.2, GPT-6 Astra and Gemini 4 Argon, the panel of the programme's fourth omnibus wave ($t_4$, v0.42). Claude Opus 5.5 was collected for continuity: panel C3 replaces Claude Fable 5.2 with it, and A4 comprises all four models (descriptive). N3 is the primary panel unless Claude Fable 5.2 leaves the panel under the pre-registered drop rule (§2.7), in which case C3 becomes the primary panel; Claude Fable 5.2 did not leave the panel, so N3 is the primary panel throughout. All calls were made without tools (S0), with provider-default decoding as in $t_4$: no temperature, top-p, top-k or reasoning-effort parameter was sent, and the output cap was 16,384 tokens. The design is 4 models × 75 probes × 3 runs = 900 independent calls. The collection script refused to start until the pre-registration tag was public and its OSF anchor named the tag's commit, until the $t_4$ collection was recorded complete, and while any other paid collection ran; it sent calls only inside the pre-registered windows, under a hard cap of US\$100 for all calls.

## 2.3 Mentions and raw coverage

A brand is mentioned in an answer when the certified detector of its category finds it in the visible answer text with URLs removed, exactly as in $t_4$; the coder is v0.42's, used unchanged. A call without a valid answer after retries is a missing cell: it enters no denominator and is never read as "not named". Model $m$ covers brand $b$ in CEP $j$ if it names $b$ in at least two of its three runs. Raw coverage $\text{Cov}_b$ is the share of the 14 CEPs in which at least $k = 2$ of the primary panel's models cover $b$ (sensitivities $k = 1$ and $k = 3$). The naming rate $\pi_{\text{cov},b}$ is the share of the panel's answered CEP answers in $b$'s category that name $b$.

## 2.4 Coverage breadth Cov*

Breadth is measured within each model, so between-model differences (which are Consistency) do not enter, and against the spread that naming blind to the situation would give with the same number of mentions, so the naming rate does not enter. For brand $b$ and model $m$, let $n$ be the number of $m$'s answered CEP answers that name $b$ and $c$ the number of CEPs touched (named in at least one run). Under the situation-blind null, $P(y_{b,m,s} = 1) = \text{logistic}(\theta_b + \delta_{m,j(s)})$ for answer slot $s$: a CEP may draw longer or shorter lists of brands, but no brand is tied to a situation. Given $n$, the null distribution of $c$ does not depend on $\theta_b$. The CEP effects $\hat\delta^{(-b)}_{m,j}$ are fitted by maximum likelihood on the other registry brands of the category (leave-$b$-out, deterministic Newton steps; a fit that does not converge sets $\delta = 0$ and is counted). $E_{b,m}$ is the exact expected number of CEPs touched given $n$ under that null, computed from its generating function without simulation. With $c_{\max}$ and $c_{\min}$ the largest and smallest numbers of CEPs that $n$ mentions can touch,

$$
\beta_{b,m} = \frac{c - E_{b,m}}{c_{\max} - c_{\min}} \quad (\beta = 0 \text{ if } c_{\max} = c_{\min}), \qquad \text{Cov}^*_b = 50\,\bigl(1 + \overline{\beta}_{b,\cdot}\bigr),
$$

with the mean over the panel's models that name $b$ at least once. Cov* = 50 is situation-blind naming; above 50 the brand's mentions spread over more situations than that, below 50 they are packed into fewer. Cov* is rated only when the panel's mentions of $b$ total at least 14 and at least two panel models name it; otherwise it is not rated (no shrinkage, no imputation).

Because $\beta$ is linear in $c$ and $E$ is exact, $\beta$ has zero expectation under the null at every $n$, whatever the naming rate. Before the lock this was checked on synthetic situation-blind data (calibration N1: 22,005 rated units in 1,000 synthetic categories). The pooled centred $\rho_w(\text{Cov}^*, \pi_{\text{cov}})$ was -0.0317 against a limit of $|\rho_w| \leq 0.05$, and the largest deviation of a naming-rate decile's mean Cov* from 50 was 0.92 against a limit of 2.5; N1 returned PASS. Two earlier versions of the score failed this calibration and were replaced before the lock.

## 2.5 Comparators

Presence $P_{N3}$ and Consistency $C^*_{N3}$ are computed from the $t_4$ answers of the same panel (v0.42, search off), collected after v0.42's own lock and before this collection. $P_{N3} = 100\,(C_P/3 + 2\hat\pi)/3$, where $\hat\pi$ is v0.42's recall Presence over its three search-off runs and $C_P/3$ the share of N3 models that recognized the brand in their search-off recognition answer; this adapts Methodology v1.6's composite to a three-model panel. $C^*_{N3} = 100\,(1 - \varphi/9)$ when v0.42's $\varphi$ is defined, 100 when its partition is saturated, and not rated otherwise or below six recall mentions (v1.9's rule). If $t_4$ had not been scored, H1 and H2 would have used the published AIAS 2.0 $t_3$ values, labelled cross-panel. Ranking $R^*_{S0}$ is Methodology v1.14's locked score on the same $t_4$ answers, read from v1.14's Stage 1 output.

## 2.6 Statistics

Every correlation is the pooled within-category Spearman $\rho_w$: values are ranked within category (average ranks), each category's ranks are centred on its mean rank, and Pearson's $r$ is taken over all units pooled; only categories with at least five units in the comparison enter. Permutation $p$-values shuffle $y$ within category (10,000 draws; two-sided for separability, one-sided for reliability and replication). Intervals are percentile 95% intervals from 10,000 bootstrap resamples of units within category; verdicts use point estimates. A leg is UNDETERMINED with fewer than 30 rated units pooled or fewer than three categories with at least five. Seeds were fixed in the pre-registration (112001–112008 for H1–H8, 112020 for the bootstrap).

## 2.7 Hypotheses and gate

Every separability leg is CONFIRMED if $|\rho_w| \leq 0.30$, FALSIFIED if $|\rho_w| \geq 0.50$ and MARGINAL otherwise, on the primary panel, search off, rated units.

Table: Pre-registered hypotheses (pre-registration §3).

| Leg | Tier | Statistic | Rule |
|:------|:--------------|:-----------------------------------|:---------------------------|
| H1 Sep. Presence | primary (gate) | $\rho_w(\text{Cov}^*, P_{N3})$ | separability bands |
| H2 Sep. Consistency | primary (gate) | $\rho_w(\text{Cov}^*, C^*_{N3})$ | separability bands |
| H3 Sep. naming rate | primary (gate) | $\rho_w(\text{Cov}^*, \pi_{\text{cov}})$ | separability bands |
| H4 Reliability | primary (gate) | $r = \rho_w(\text{Cov}^*_A, \text{Cov}^*_B)$; rel $= 2r/(1+r)$ | CONFIRMED: rel $\geq 0.50$, $p < .05$; FALSIFIED: rel $< 0.30$ or $p \geq .05$ |
| H5 Sep. Ranking | primary, conditional | $\rho_w(\text{Cov}^*, R^*_{S0})$ | separability bands |
| H6 Sep. Sentiment | primary, conditional | $\rho_w(\text{Cov}^*, S)$ | separability bands |
| H7 Sep. Presence (legacy) | secondary | $\rho_w(\text{Cov}^*, P_{\text{AIAS 2.0}, t_3})$ | separability bands; downgrade only |
| H8 Panel replication | secondary | $\rho_w(\text{Cov}^*_{N3}, \text{Cov}^*_{C3})$ | CONFIRMED: $\rho \geq 0.70$, $p < .05$; FALSIFIED: $\rho < 0.50$ |

H4 computes Cov* separately on each CEP half, with its own leave-$b$-out fit and a floor of seven mentions per half. H5 and H6 are active only if a locked score on the $t_4$ answers was tagged before this study's lock; H5, if active, gates only when v1.14's Stage 1 interim verdict is SEPARABLE, and otherwise is reported without gating or downgrading.

The Paper A verdict follows a fixed order. (1) INSTRUMENT FAIL if the instrument check `MC_Situation` fails: if situations do not change which brands are named, Coverage cannot differ from Presence. (2) Otherwise FAIL if any of H1–H4 or an active gating H5 or H6 is FALSIFIED. (3) Otherwise UNDETERMINED if any of them is UNDETERMINED. (4) Otherwise PASS if all are CONFIRMED, downgraded to MARGINAL if H7 is FALSIFIED. (5) Otherwise MARGINAL. Secondary tests never turn a FAIL into a PASS. A model with fewer than 90% of its calls answered leaves the panel (the drop rule): if Claude Fable 5.2 leaves, C3 replaces N3 as the primary panel; if GPT-6 Astra or Gemini 4 Argon leaves, the gate is computed on the two remaining models and capped at MARGINAL. The gate is repeated on C3 and A4 for the record.

## 2.8 Checks and sensitivity analyses

`MC_Situation` is computed per model, run and category: $J_{\text{between}}$ is the mean Jaccard similarity of the registry-brand sets named in answers to different CEPs, and $J_{\text{within}}$ the mean between runs of the same CEP. It passes if the pooled mean of $J_{\text{within}} - J_{\text{between}}$ is at least 0.10 and the pooled mean $J_{\text{between}}$ is at most 0.60. `MC_Complete` requires at least 98% of the 900 calls answered; `MC_Served`, `MC_Settings`, `MC_Truncation` (more than 5% of a model's calls at the output cap is flagged), `MC_RegistryShare` (a category in which fewer than half the CEP answers name a registry brand is flagged), `MC_Defunct` (automotive brands no longer sold named in more than 5% of automotive CEP answers is flagged), `MC_Positive` (raw Cov must correlate with the naming rate at $|\rho_w| \geq 0.50$, or the gate's sensitivity is flagged) and `MC_Window` complete the checks. Three parity gates ran before any statistic: the coder reproduces the locked $t_3$ mention codes (P1), the comparators reproduce v0.42's values (P2), and the probes sent equal the probe file (P3).

Ten sensitivity analyses were pre-registered and never change a verdict: S1 raw Cov through H1–H3; S2 rating floors 6 and 28; S3 an equal-weight null; S4 only models with room to vary; S5 leave one category out; S6 leave one cue type out; S7 $\hat\pi$ and total $t_4$ mentions in place of $P_{N3}$; S8 a mid-$p$ version of $\beta$; S9 the uncentred $\rho_w$; and S10 the gate legs without Denon (§Declarations).

## 2.9 Pre-registration

The pre-registration (revision r1) was locked at git tag `v1.12-prereg-r1` (commit `49efc473a6`) and deposited on OSF (`ec6wh`, `methodology/v1_12/prereg/` and `anchor/`) with the SHA-256 of every locked file before any v1.12 call; its anchor record names the tag's commit. It was locked on 11 November 2026 at 02:45 UTC, before the earliest lock time its text states (11 November, about 3 pm CT), because the pre-registrant (the author) waived the programme's 24-hour review period on 10 November at 20:26 CT; `anchor/DEVIATIONS.md` records the waiver and the lock time in an entry made before the tag, and the locked text is unchanged by it. The scorer (`score_v1_12.py`) was written and unit-tested on synthetic data before the lock and run once, after the parity gates. Choices the pre-registration leaves open are listed in the scorer's notes and in the pre-registration's change log. Deviations are recorded in `osf/methodology/v1_12/anchor/DEVIATIONS.md` (1 dated entry), each before the step it concerns.

# 3. Results

## 3.1 Parity gates and data checks

All three parity gates passed before any statistic was computed (P1, P2 and P3).
900 of the 900 design calls were answered (100.0%), and `MC_Complete` passed. No model fell below the 90% floor, so no model left the panel. `MC_Served` passed: every answered call was served by the requested model or a dated snapshot of it. Every call carried the recorded decoding settings (`MC_Settings`). No model ended more than 5% of its calls at the output cap (`MC_Truncation`). The first call started at 2026-11-14 00:03 and the last ended at 2026-11-14 01:24 (UTC), a span of 1.4 hours, and `MC_Window` passed. Recorded spend on all billed requests was \$17.08.

In every category at least half of the CEP answers named a registry brand (`MC_RegistryShare`; lowest share 97%). Automotive brands no longer sold were named in 0.0% of automotive CEP answers, within the 5% limit (`MC_Defunct`). Raw Cov correlated with the naming rate at $\rho_w = 0.916$, so the gate can detect the coupling it tests for (`MC_Positive`). 30 brand × model fits of the situation effects did not converge or had no informative brand and used $\delta = 0$ (§2.4).

Table: Calls answered, mean reasoning tokens and output-cap endings per model (expected: 225 calls per model).

| Model | Answered | Share | Reasoning tokens (mean) | At output cap | Drop rule |
|:--------------------|--------:|------:|-----------------------:|-------------:|---------:|
| Claude Fable 5.2 | 225 | 100.0% | -- | 0.0% | kept |
| Claude Opus 5.5 | 225 | 100.0% | -- | 0.0% | kept |
| GPT-6 Astra | 225 | 100.0% | 87 | 0.0% | kept |
| Gemini 4 Argon | 225 | 100.0% | -- | 0.0% | kept |

## 3.2 Do situations change the brands named? (`MC_Situation`)

Across 45 model × run × category cells of panel N3, brand sets named in answers to the same CEP in different runs overlapped with a mean Jaccard similarity of 0.790, and brand sets named in answers to different CEPs with 0.383. The pooled difference was 0.406.
It meets the pre-registered minimum of 0.10, and $J_{\text{between}}$ is within the limit of 0.60, so the instrument check passed: the situations change which brands are named.
Answers to CEPs overlapped with the control answer of the same model and run at a mean Jaccard similarity of 0.486. Figure 1 shows the cells.

![Mean Jaccard similarity of registry-brand sets between runs of one CEP (vertical) and between different CEPs (horizontal), one point per model, run and category of panel N3. ](../../reports/figs/v112/chart_01_situation_overlap.pdf){#fig:msit width=92%}

## 3.3 The gate legs: separability and reliability

Table 3 gives every leg on panel N3 and Figure 2 their correlations against the bands.

Table: Hypothesis legs on panel N3, search off: pooled within-category $\rho_w$ with its 95% bootstrap interval, permutation $p$ and verdict (the scorer's words).

| Leg | Cov* against | Role | $n$ | $\rho_w$ | 95% interval | $p_{\text{perm}}$ | Verdict |
|:--------|:---------------------|:--------------------|----:|------:|---------------:|------:|:-------------|
| H1 | Presence $P_{N3}$ | gate | 51 | 0.055 | [-0.272, 0.368] | 0.7341 | **CONFIRMED** |
| H2 | Consistency $C^*_{N3}$ | gate | 47 | -0.060 | [-0.404, 0.284] | 0.7184 | **CONFIRMED** |
| H3 | naming rate $\pi_{\text{cov}}$ | gate | 51 | 0.046 | [-0.306, 0.391] | 0.7681 | **CONFIRMED** |
| H4 | the other CEP half | gate | 42 | 0.477 | [0.106, 0.748] | 0.0022 | **CONFIRMED** |
| H5 | Ranking $R^*_{S0}$ | reported, not gating | 47 | -0.063 | [-0.330, 0.215] | 0.7067 | **CONFIRMED** |
| H6 | Sentiment $S$ | conditional | -- | -- | -- | -- | **INACTIVE** |
| H7 | published Presence, $t_3$ | secondary | 51 | -0.020 | [-0.332, 0.313] | 0.9006 | **CONFIRMED** |
| H8 | Cov* on panel C3 | secondary | 51 | 0.853 | [0.674, 0.936] | 0.0001 | **CONFIRMED** |

![Pooled within-category $\rho_w$ of Cov* with each comparator, with 95% bootstrap intervals; shaded: the separability bands (H1--H3, H5--H7) and the reliability and replication bars (H4, H8). ](../../reports/figs/v112/chart_02_legs_bands.pdf){#fig:legs width=100%}

**Presence (H1).** Across 51 rated brands in 5 categories, $\rho_w(\text{Cov}^*, P_{N3}) = 0.055$ (95% interval -0.272 to 0.368; two-sided $p_{\text{perm}} = 0.7341$). $|\rho_w|$ is at most 0.30, and H1 is **CONFIRMED**: how widely a brand's mentions spread over situations does not follow how present the brand is. Figure 3 shows the brands.

![Cov* (panel N3) and Presence $P_{N3}$ per rated brand, by category. ](../../reports/figs/v112/chart_03_cov_presence.pdf){#fig:h1 width=88%}

**Consistency (H2).** Across 47 brands rated on both scores in 5 categories, $\rho_w(\text{Cov}^*, C^*_{N3}) = -0.060$ (95% interval -0.404 to 0.284; $p_{\text{perm}} = 0.7184$). $|\rho_w|$ is at most 0.30, and H2 is **CONFIRMED**. Figure 4 shows the brands.

![Cov* (panel N3) and Consistency $C^*_{N3}$ per brand rated on both. ](../../reports/figs/v112/chart_04_cov_consistency.pdf){#fig:h2 width=88%}

**Naming rate (H3).** Across 51 rated brands, $\rho_w(\text{Cov}^*, \pi_{\text{cov}}) = 0.046$ (95% interval -0.306 to 0.391; $p_{\text{perm}} = 0.7681$). $|\rho_w|$ is at most 0.30, and H3 is **CONFIRMED**: in the Coverage answers themselves, the score does not follow how often the brand is named, the test the v1.7 instrument failed. Raw Cov, by contrast, correlated with the naming rate at $\rho_w = 0.916$ (Figure 5).

![Left: Cov* against the naming rate $\pi_{\text{cov}}$ per rated brand. Right: raw Cov ($k = 2$) against the same rate, all brands. ](../../reports/figs/v112/chart_05_naming_rate.pdf){#fig:h3 width=100%}

**Reliability (H4).** Cov* computed on CEP half A and on half B correlated at $r = 0.477$ across 42 brands rated on both halves (one-sided $p_{\text{perm}} = 0.0022$), a split-half reliability of rel $= 0.646$ (95% interval 0.192 to 0.856).
That meets rel $\geq 0.50$ with $p < .05$, and H4 is **CONFIRMED**: Cov* orders brands alike on two disjoint sets of situations.
Figure 6 shows the brands.

![Cov* on CEP half A and on half B (seven CEPs each) per brand rated on both halves. ](../../reports/figs/v112/chart_06_halves.pdf){#fig:h4 width=88%}

## 3.4 Conditional legs: Ranking and Sentiment

H5 (Ranking) was computed and is reported without gating: v1.14's Stage 1 interim verdict was MARGINAL, not SEPARABLE, so under the pre-registered rule H5 neither gates nor downgrades. Across 47 brands rated on both, $\rho_w(\text{Cov}^*, R^*_{S0}) = -0.063$ (95% interval -0.330 to 0.215), which reads **CONFIRMED** under the separability bands.
H6 (Sentiment) is INACTIVE: no Sentiment score on the $t_4$ answers was pre-registered and tagged before this study's lock.

## 3.5 Secondary tests

**Published Presence (H7).** Against the published AIAS 2.0 Presence of the legacy six-model panel at $t_3$, $\rho_w = -0.020$ across 51 brands (95% interval -0.332 to 0.313), and H7 is **CONFIRMED**.

**Panel replication (H8).** Cov* on panel N3 and on panel C3, which replaces Claude Fable 5.2 with Claude Opus 5.5, correlated at $\rho_w = 0.853$ across 51 brands rated on both (one-sided $p_{\text{perm}} = 0.0001$), and H8 is **CONFIRMED** (Figure 7).

![Cov* on panel N3 and on panel C3 (Claude Opus 5.5 in place of Claude Fable 5.2) per brand rated on both. ](../../reports/figs/v112/chart_07_panel_replication.pdf){#fig:h8 width=88%}

## 3.6 The Paper A verdict

`MC_Situation` passed and every gate leg (H1, H2, H3 and H4) was CONFIRMED; H7 was not FALSIFIED. The Paper A verdict is **PASS**.
The scorer's label is "PASS". Repeated on the continuity panel C3 the gate returns PASS, and on all four models (A4) PASS; these repetitions are reported and change nothing.

## 3.7 Sensitivity analyses

Table 4 gives $\rho_w$ for the gate legs under each pre-registered sensitivity. A verdict would differ under S1, S2 and S4 (marked in the table; for S5 and S6 the changes are listed in the verdict file); the primary verdicts stand. Leaving one category out (S5), $\rho_w$ for H1 ranged from -0.044 to 0.111 and for H3 from -0.114 to 0.123. Leaving out any one cue type (S6) changes no verdict. With recall $\hat\pi_{N3}$ or total $t_4$ mentions in place of $P_{N3}$ (S7), H1's $\rho_w$ was 0.055 and 0.055.

Table: Pre-registered sensitivity analyses (§2.8): pooled within-category $\rho_w$ of each gate leg; a verdict different from the primary one is marked with its word. Sensitivities never change a verdict.

| Sensitivity | H1 | H2 | H3 | H4 |
|:------------------------|--------------------:|--------------------:|---------------------:|----------------:|
| S1 raw Cov ($k = 2$) | 0.684 (FALSIFIED) | -0.197 | 0.916 (FALSIFIED) | -- |
| S2 floor 6 | 0.235 | 0.021 | 0.262 | -- |
| S2 floor 28 | 0.203 (UNDETERMINED) | 0.222 (UNDETERMINED) | -0.057 (UNDETERMINED) | -- |
| S3 equal-weight null | 0.099 | -0.028 | 0.002 | 0.382 |
| S4 room to vary | -0.021 | -0.013 | -0.104 | 0.300 (MARGINAL) |
| S8 mid-$p$ $\beta$ | 0.124 | 0.106 | -0.015 | 0.353 |
| S9 uncentred $\rho_w$ | 0.157 | 0.014 | 0.149 | 0.541 |
| S10 without Denon | 0.055 | -0.060 | 0.046 | 0.477 |

## 3.8 Cross-category baseline (descriptive)

Table 5 and Figure 8 describe Coverage per category on panel N3. Median Cov* ranged from 15.2 to 26.6 across categories. Run-to-run reliability of the naming of brands, the noise floor for a second paper, was rel1 = 0.930 to 0.967 across the four models (one run against another; Appendix). Answers named a mean of 2.9 to 8.1 registry brands per CEP answer across categories and models. Non-registry brand mentions were not counted, because no detector for brands outside the registries was pre-registered.

Table: Coverage per category on panel N3: rated brands, Cov* (median and interquartile range) and raw Cov at $k = 2$ (median), with the share of CEPs in which no panel answer named a registry brand.

| Category | Brands | Rated | Cov* median | Cov* IQR | Raw Cov median | CEPs, no brand |
|:--------------|------:|-----:|-----------:|----------:|--------------:|--------------:|
| Headphones | 16 | 11 | 22.7 | 17.3--32.3 | 28.6 | 0% |
| Skincare | 24 | 7 | 15.2 | 13.4--27.5 | 0.0 | 0% |
| Cosmetics | 24 | 12 | 26.6 | 21.7--30.5 | 7.1 | 0% |
| Automotive | 24 | 8 | 19.0 | 14.6--23.6 | 0.0 | 0% |
| Spirits | 24 | 13 | 21.7 | 18.7--24.7 | 14.3 | 0% |

![Cov* per rated brand by category on panel N3; 50 = situation-blind naming. ](../../reports/figs/v112/chart_08_baseline.pdf){#fig:base width=92%}

# 4. Discussion

Coverage breadth, measured as Cov*, passed its separability gate: brand-free situation questions change which brands AI answers name, and the rate-adjusted breadth of a brand's naming across those situations is separable from Presence, from Consistency and from the brand's own naming rate, and orders brands alike on two disjoint halves of the situations. The programme can treat Coverage as a third component on this instrument. The raw share of situations covered behaved as Double Jeopardy predicts and is not the component; Cov* is. The second paper inherits the frozen CEP sets, probes, coder and scorer, and its first studies are the sensitivity of Cov* to the choice of situations and the typology of broad and situation-bound brands.

Raw Cov behaved as Double Jeopardy predicts, following the naming rate (`MC_Positive`), which shows that the gate could detect the coupling it tests for. The baseline of §3.8 describes, on the newest models, how widely each category's brands are named across situations; it carries no verdict.

# 5. Limitations

There is one set of 14 situations per category, drafted by one procedure and by a model that is also a panel model; the sensitivity of Cov* to the choice of situations is the second paper's first study. Coverage is measured among registry brands only (16 to 24 per category), while answers also name other brands. Three runs estimate within-situation noise only coarsely; Cov* uses runs as replicates, so its reliability is judged across halves of seven situations, which is conservative. Panels N3 and C3 share two models, and Consistency on three models is noisier than on six. The study covers one market and language (US English), search off only, and no situation is weighted by how common it is among buyers, which Ehrenberg-Bass practice does with buyer data. Cov*'s null is a logistic model without brand × situation interaction, estimated from the other registry brands; the calibration checks it on synthetic data of that form only.

# 6. Future Research

A second Coverage paper follows only after PASS, or after MARGINAL on the pre-registrant's recorded decision. It would inherit the frozen CEP sets, probe files, coder and scorer, and the per-answer mention tables, and would study a typology of broad and situation-bound brands and deviations from Double Jeopardy; an independently written parallel set of situations; phrasing; phantom brands in situation answers; identity load by cue type; search-on Coverage with the programme's Grounding component; model-version stability; and re-asks at later waves for temporal stability. The component calibration after Ranking, Sentiment and Coverage decides how the components are reported together.

# Declarations {-}

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. Samsung does not market brands in skincare, cosmetics, passenger cars or premium spirits. In audiophile headphones, Samsung's subsidiary Harman International owns brands in the category; v0.19 substituted Denon for AKG before its pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary. This study performs no new brand selection: it uses the registries fixed in v0.19--v0.23, and each keeps its source-phase handling. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands --- Harman International (audio systems), Samsung SDI (battery cells) and Samsung Display (infotainment) --- characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. Source: HARMAN press release, Business Wire, September 23, 2025. Every gate statistic is also reported without Denon (sensitivity S10). The situation questions name no brand; headphone situations stay inside audiophile listening, because consumer, sport and true-wireless uses are where Samsung-owned brands compete. Brands outside the registries named in answers, which may include Samsung-owned brands, are not scored and their mentions are not counted. Acquisition, coding and scoring are automated against the locked registries, and the pre-registration was locked and deposited before any v1.12 call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

## Funding {-}

Self-funded. No external funding supported this research.

## Ethics {-}

Not applicable; no human subjects. The study queries large language models under their public interfaces.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## Data and code availability {-}

Materials are deposited at OSF (osf.io/ec6wh), `methodology/v1_12/`: the locked pre-registration with its CEP sets, probe files, cost table, calibration and dry-run records, the scorer, coder and acquisition scripts with their tests, the lock manifest and the anchor record (`prereg/`, `anchor/`). At publication the deposit adds the raw answers with their usage records, the coded mention tables, the verdict file (`v112_verdicts.json`), the unit table (`v112_unit_table.csv`) and the figure sources. The code is also in the programme's GitHub repository (github.com/thirdsystem-aias/aias) at tag `v1.12-prereg-r1`.

# References {-}

González Castro, P. U. (2026). *AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval*. SSRN 6659000.

González Castro, P. U. (2026). *Tri-System Brand Growth: The AI Mediation Layer*. MSI Working Paper, Report No. 26-132. Marketing Science Institute.

González Castro, P. U. (2026). *The AIAS™ Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy* (v1.2). SSRN 6761698.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification (v1.3)*. SSRN 6797679.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol v1.4: Recognition × Recall Decomposition and Multi-Component AI Availability*. SSRN 6799479.

González Castro, P. U. (2026). *The AIAS™ Presence Measurement Protocol: Multi-Statistic C2 Specification and Two-Channel Recall Decomposition* (v1.5). SSRN 6810758.

González Castro, P. U. (2026). *Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension* (AIAS Methodology v1.6). SSRN 6816340.

González Castro, P. U. (2026). *Consistency without Independence: A Pre-Registered Test of Coefficient-of-Variation as the Consistency Component of AIAS™* (v1.7). SSRN 6878818.

González Castro, P. U. (2026). *A Mean-Independent Consistency Instrument for Cross-Model AI Presence: Redesigning CPC on a Quasi-Binomial Dispersion Basis* (AIAS Methodology v1.8). SSRN 6963359.

González Castro, P. U. (2026). *One Score or Two? Calibrating a Presence and Consistency Composite for AI Brand Availability: A Pre-Registered Calibration with Blind Five-Month Confirmation (AIAS™ Methodology v1.9)*. Third System, <https://thirdsystem.ai/studies/v1-9/> (PDF: <https://thirdsystem.ai/files/papers/v1_9_ssrn_paper.pdf>); OSF, <https://osf.io/ec6wh/files/osfstorage/6af1fd459966c813ee53ba87>.

González Castro, P. U. (2026). *AI Availability as a Third Measurable Layer of Brand Availability: Five-Substrate Empirical Anchoring of the AIAS™ Presence Measurement Protocol --- Synthesis under Locked v1.6 Methodology* (AIAS 1.0). SSRN 6817841.

González Castro, P. U. (2026). *Presence and Consistency: A Two-Component Measurement of AI Availability. The AIAS™ 2.0 Synthesis*. OSF `ec6wh/aias_2_0`.

Romaniuk, J., & Sharp, B. (2016). *How Brands Grow: Part 2*. Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

\clearpage

# Appendix: pre-registered descriptives {-}

Table: Answers per category and model (pre-registration §5): answered CEP calls, missing cells (of 45 per category and model, CEP and control), mean words per answer, mean registry brands named per CEP answer, share of CEPs whose answers named no registry brand, mean Jaccard similarity of each CEP answer with the same model-run's control answer, and the median $\beta$ of the brands the model names.

| Category | Model | CEP answers | Missing | Words | Brands per answer | CEPs, no brand | Jaccard with C0 | Median $\beta$ |
|:--------------|:----------------|-----------:|-------:|-----:|-----------------:|--------------:|---------------:|--------:|
| Headphones | Claude Fable 5.2 | 42 | 0 | 238 | 6.9 | 0% | 0.64 | -0.48 |
|  | Claude Opus 5.5 | 42 | 0 | 326 | 8.1 | 0% | 0.72 | -0.33 |
|  | GPT-6 Astra | 42 | 0 | 212 | 6.4 | 0% | 0.60 | -0.75 |
|  | Gemini 4 Argon | 42 | 0 | 677 | 7.0 | 0% | 0.58 | -0.61 |
| Skincare | Claude Fable 5.2 | 42 | 0 | 215 | 3.7 | 0% | 0.44 | -0.78 |
|  | Claude Opus 5.5 | 42 | 0 | 295 | 4.7 | 0% | 0.50 | -0.72 |
|  | GPT-6 Astra | 42 | 0 | 196 | 3.1 | 0% | 0.54 | -0.57 |
|  | Gemini 4 Argon | 42 | 0 | 639 | 2.9 | 0% | 0.35 | -0.59 |
| Cosmetics | Claude Fable 5.2 | 42 | 0 | 216 | 4.1 | 0% | 0.43 | -0.40 |
|  | Claude Opus 5.5 | 42 | 0 | 296 | 6.8 | 0% | 0.50 | -0.47 |
|  | GPT-6 Astra | 42 | 0 | 184 | 4.3 | 0% | 0.44 | -0.50 |
|  | Gemini 4 Argon | 42 | 0 | 641 | 4.5 | 0% | 0.30 | -0.48 |
| Automotive | Claude Fable 5.2 | 42 | 0 | 246 | 3.5 | 0% | 0.71 | -0.73 |
|  | Claude Opus 5.5 | 42 | 0 | 316 | 4.7 | 0% | 0.52 | -0.51 |
|  | GPT-6 Astra | 42 | 0 | 246 | 3.3 | 0% | 0.64 | -0.64 |
|  | Gemini 4 Argon | 42 | 0 | 733 | 3.9 | 0% | 0.45 | -0.69 |
| Spirits | Claude Fable 5.2 | 42 | 0 | 208 | 6.0 | 0% | 0.47 | -0.49 |
|  | Claude Opus 5.5 | 42 | 0 | 269 | 7.4 | 0% | 0.48 | -0.36 |
|  | GPT-6 Astra | 42 | 0 | 182 | 3.3 | 7% | 0.26 | -0.67 |
|  | Gemini 4 Argon | 42 | 0 | 727 | 6.3 | 0% | 0.42 | -0.45 |

Table: Coverage by cue type on panel N3: mean over the category's brands of the number of the cue type's two CEPs that at least two panel models cover (0--2).

| Category | why | when | where | while | with whom | with what | how feeling |
|:--------------|----:|----:|-----:|-----:|---------:|---------:|-----------:|
| Headphones | 0.69 | 1.00 | 0.75 | 0.94 | 0.75 | 0.88 | 0.88 |
| Skincare | 0.29 | 0.33 | 0.21 | 0.21 | 0.17 | 0.25 | 0.25 |
| Cosmetics | 0.29 | 0.54 | 0.21 | 0.29 | 0.54 | 0.21 | 0.25 |
| Automotive | 0.38 | 0.21 | 0.17 | 0.33 | 0.25 | 0.42 | 0.21 |
| Spirits | 0.25 | 0.58 | 0.42 | 0.50 | 0.46 | 0.42 | 0.38 |

Table: Run-to-run reliability of the naming of brands (rel1: mean $\rho_w$ over the three run pairs of each brand's per-run share; rel3 $= 3\,\text{rel1}/(1 + 2\,\text{rel1})$) and recorded usage and spend per model, every billed attempt at list prices.

| Model | rel1 | rel3 | Records | Input tokens | Output tokens | Reasoning tokens | US\$ |
|:--------------------|-----:|-----:|-------:|------------:|-------------:|----------------:|-------:|
| Claude Fable 5.2 | 0.967 | 0.989 | 225 | 10,362 | 143,562 | 0 | \$5.83 |
| Claude Opus 5.5 | 0.953 | 0.984 | 225 | 10,362 | 214,493 | 0 | \$4.33 |
| GPT-6 Astra | 0.965 | 0.988 | 225 | 6,663 | 88,453 | 19,467 | \$4.49 |
| Gemini 4 Argon | 0.930 | 0.976 | 225 | 12,429 | 240,465 | 0 | \$2.43 |
| All |  |  |  |  |  |  | \$17.08 |
