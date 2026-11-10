---
title: "Five-Month Stability of AI Brand Consistency and Presence"
subtitle: "A Pre-Registered Third Wave on a Retiring Six-Model Panel (AIAS™ v0.41)"
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
---

\begin{titlepage}
\setstretch{1.0}
\setlength{\parskip}{0pt}
\begin{center}

{\LARGE \textbf{Five-Month Stability of AI Brand Consistency and Presence}}\\[8pt]

{\large A Pre-Registered Third Wave on a Retiring Six-Model Panel\\ (AIAS™ v0.41)}\\[28pt]

Pablo Ulpiano González Castro\\[4pt]
School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System™ (research entity; data archive and methodology venue)\\[8pt]
Correspondence: pablou@pablou.com · pablou.com\\
ORCID: 0009-0003-8968-9990\\[20pt]

Pre-registration: \texttt{v0.41-prereg-r1} (deposited on OSF before the first t\textsubscript{3} call)\\
Data and code: OSF \texttt{ec6wh/v41}\\

\end{center}
\end{titlepage}

# Abstract {-}

Brand measures derived from large language model (LLM) outputs are only useful if they hold still when nothing about the brand has changed. This study reports a pre-registered third wave of the AIAS™ measurement protocol: a verbatim re-acquisition, in November 2026, of five product-category panels (audiophile headphones, skincare, cosmetics, automotive, premium spirits; 112 brand units) first measured in May 2026 ($t_1$) and re-measured in June 2026 ($t_2$), on a fixed six-model panel whose dated versions were confirmed identical to $t_2$ and which begins retiring on 24 November 2026. The $t_2 \rightarrow t_3$ interval is 152 days. All 852 study calls returned, and four computational-reproducibility gates passed before any $t_3$ statistic was computed. The per-brand rank order of the v1.8 Consistency instrument $\varphi$ held over the long horizon (`H_Phi_LongHorizon` CONFIRMED: pooled $\rho = 0.681$, $n = 80$), exceeding both a brand-label permutation null and a pre-registered frame-structure null that scrambles model identity within each question ($p_{\text{frame}} = 0.0001$; null 95th percentile $0.51$). Recall Presence held its order in all five categories (`H_Presence_LongHorizon` CONFIRMED: $\rho = 0.927$--$0.976$). No decay from the three-week to the five-month horizon was detectable for either instrument (`H_Horizon_Decay` MARGINAL for both; $D = +0.019$ and $+0.002$, intervals spanning zero). Changes in Consistency were unrelated to changes in Presence (`H_Drift_Dissociation` CONFIRMED: $\rho = 0.032$). Of 58 brands below the recall floor at $t_2$, 56 remained below it. The results give the two-component AIAS 2.0 construct a long-horizon reliability base and are the last data this model panel can provide.

**Keywords:** AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; large language models; test--retest reliability; longitudinal measurement; consistency; brand recall

**JEL codes:** M31; L86, L15, D83, M37

**Paper status:** Pre-registered prospective third-wave re-acquisition (tag `v0.41-prereg-r1`; pre-registration deposited on OSF before the first $t_3$ call); 852 study calls; three deviations recorded before the steps they concern, none affecting a locked rule, probe or model (§2.7). Part of the AIAS measurement program.

# 1. Introduction

AI Availability --- the discoverability and representation of a brand in the outputs of large language models --- has been proposed as a third measurable layer of brand availability (González Castro, 2026, SSRN 6659000), alongside the Mental and Physical Availability of the Ehrenberg-Bass tradition (Sharp, 2010; Romaniuk & Sharp, 2022). The AIAS™ program measures it as a multi-component construct under a versioned protocol. Presence --- whether and how often the panel names a brand --- was the first component locked (v1.6, SSRN 6816340; AIAS 1.0, SSRN 6817841). Consistency --- whether the panel's models agree about a brand --- is the second. Its first operationalization, a coefficient-of-variation quantity (CV-CPC), was falsified as a Consistency instrument because it tracked Presence (v1.7, SSRN 6878818). Its replacement, the quasi-binomial dispersion statistic $\varphi$, was shown to be independent of the recall level ($|\rho(\varphi, \mu)| = 0.091$) and reproducible over a 15--21-day interval ($\rho = 0.645$) in the v1.8 methodology revision (SSRN 6963359).

Two-wave evidence at a three-week horizon leaves the question that matters for a managed metric open: does the instrument hold its brand order over months? A quarterly or semi-annual tracking cadence is the natural unit of brand measurement, and a quantity that drifts at that scale would be unusable however well it behaves over three weeks. The program's only prior longitudinal test, v0.34 (SSRN 6915458), measured $t_1 \rightarrow t_2$ under the now-retired CV-CPC quantity and was limited by recognition ceilings.

A practical deadline shaped this study. The six-model panel used throughout the program since v0.17 begins retiring on 24 November 2026 (Claude Opus 4.5 not sooner than that date; Claude Sonnet 4.5 on 30 November 2026; the GPT-4o and GPT-4o mini snapshots on 14 January 2027). A third wave on this panel had to be collected before then or not at all.

This study contributes four results. First, a long-horizon (152-day) test of the v1.8 Consistency instrument, judged against a pre-registered frame-structure null as well as the conventional permutation null. Second, a parallel long-horizon test of recall Presence. Third, a direct comparison of three horizons --- 15--21 days, 152 days and 167--173 days --- on the same brands. Fourth, a test of whether long-horizon change in Consistency is a by-product of change in Presence, the dynamic counterpart of v1.8's static independence result.

# 2. Method

## 2.1 Design

The study is a prospective third-wave re-acquisition. $t_1$ is the five original substrate acquisitions (20--26 May 2026); $t_2$ is the v0.34 re-acquisition (10 June 2026); $t_3$ is this study's re-acquisition (9 November 2026). Intervals are reported in Table 1. Brand registries are bit-identical to the $t_1$ locks, with no new brand selection. Each substrate's original acquisition runner was executed verbatim through a logging dispatcher, with exactly two permitted modifications --- the output directory and a provenance sidecar --- and nothing else. The eight probe-set artifacts were verified by SHA-256 against their $t_1$ values immediately before each substrate's runner ran (8/8 on every check). Each wave issues 852 study calls: 672 recognition (Phase A) and 180 recall (Phase B). Premium-spirits recognition is coded by an LLM judge (alias `claude-sonnet-4-5`, as at $t_1$ and $t_2$); its 144 calls are coding, not acquisition.

## 2.2 Panel and version pinning

The panel is six models from three providers: Claude Opus 4.5 and Claude Sonnet 4.5 (Anthropic), GPT-4o and GPT-4o mini (OpenAI), Gemini 2.5 Flash and Gemini 2.5 Flash Lite (Google). Models are called by the same aliases as at $t_1$. Because $t_2$ recorded the dated identifier each alias served, version isolation could be checked rather than assumed: a pre-registered manipulation check (`MC_Snapshot`) required each dated alias to serve its $t_2$ snapshot on every $t_3$ call, with a sensitivity analysis without any model that did not. All four dated aliases served their $t_2$ snapshots on every call (`claude-opus-4-5-20251101`, `claude-sonnet-4-5-20250929`, `gpt-4o-2024-08-06`, `gpt-4o-mini-2024-07-18`); the sensitivity analysis was therefore not triggered. Google serves undated aliases, so Gemini-side version change cannot be excluded (§5). The pre-registered minimum viable panel was four models; all six returned every call, and no model was dropped.

## 2.3 Measures

For each brand $b$ and model $m$, $k(b,m) \in \{0,\dots,6\}$ counts the recall frames in which $m$ names $b$. Recall Presence is $\hat\pi_b = \sum_m k(b,m) / 36$. Consistency is the v1.8 instrument,

$$
\varphi_b = \frac{1}{M-1}\sum_{m=1}^{M} \frac{\left(k(b,m) - F\hat\pi_b\right)^2}{F\hat\pi_b(1-\hat\pi_b)}, \qquad M = F = 6,
$$

defined for $0 < \hat\pi_b < 1$; higher $\varphi$ means less agreement between models, and $E[\varphi] = 1$ under homogeneity. The positional diagnostic $J$ is the mean pairwise Jaccard overlap of the models' frame sets. Recognition $C_P \in \{0,\dots,6\}$ follows the v1.6 lock, with premium-spirits recognition levels normalized to binary identically in every wave. A brand is below the recall floor (a phantom) when its mean per-model recall count is below 1.0, the v0.34 rule. Extraction uses the certified lineage of v0.34 and v1.8 in all three waves, and the $\varphi$ and $J$ kernels are carried verbatim from the v1.8 scorer.

## 2.4 Hypotheses and decision rules

Five hypotheses were locked in the pre-registration, with verdicts CONFIRMED, MARGINAL or FALSIFIED, and UNDETERMINED only where a pre-specified floor is not met or a statistic is degenerate.

`H_Phi_LongHorizon` (primary): pooled Spearman $\rho(\varphi_{t_2}, \varphi_{t_3})$ over brands with $\varphi$ defined in both waves, computed as in v1.8. CONFIRMED if $\rho \ge 0.50$, $p_{\text{perm}} < .05$ and $p_{\text{frame}} < .05$; FALSIFIED if $\rho < 0.30$ or $p_{\text{perm}} \ge .05$; otherwise MARGINAL; UNDETERMINED below 40 brands. $p_{\text{perm}}$ comes from a stratified permutation of $t_3$ values within substrate (10,000 draws, one-sided). $p_{\text{frame}}$ comes from a frame-structure null: within each substrate and each recall question, the six models' $t_3$ answers are permuted (one permutation per question, applied to every brand), which preserves which brands each question elicits and every $\hat\pi_b$ exactly while scrambling model identity; $p_{\text{frame}}$ is the share of 10,000 such shuffles whose $\rho(\varphi_{t_2}, \varphi_{\text{shuffled}})$ reaches the observed value. This condition was added to the draft before the lock after a pre-lock calibration on the frozen $t_2$ wave showed that such shuffles alone leave $\rho$ at a mean of 0.39 (95th percentile 0.55; 12% of draws at or above 0.50), and that the brand-label permutation null calls nearly all of them significant. Without it, a third wave with no model-level consistency at all would usually have been classed MARGINAL and sometimes CONFIRMED.

`H_Presence_LongHorizon` (primary): per-substrate Spearman $\rho(\hat\pi_{t_2}, \hat\pi_{t_3})$ over all registry brands, with a one-sided permutation test per substrate. CONFIRMED if $\rho \ge 0.70$ in at least four of five substrates; FALSIFIED if $\rho < 0.50$ in at least three.

`H_Horizon_Decay` (secondary): for $\varphi$ (pooled ranks) and for $\hat\pi$ (pooled within-substrate ranks), $D = \rho(t_1,t_2) - \rho(t_1,t_3)$ over brands defined in all three waves, with a 95% interval from 10,000 paired bootstrap resamples of brand units within substrate. CONFIRMED (decay) if the interval lies above zero; FALSIFIED if below; MARGINAL if it includes zero.

`H_Drift_Dissociation` (secondary): pooled Spearman $\rho(\Delta\varphi, \Delta\hat\pi)$, where each $\Delta$ is the change in within-substrate percentile rank from $t_2$ to $t_3$, over brands with $\varphi$ defined in both waves; two-sided stratified permutation. CONFIRMED if $|\rho| \le 0.30$; FALSIFIED if $|\rho| \ge 0.50$ with $p < .05$; otherwise MARGINAL.

`H_Phantom_LongPersistence` (tertiary, descriptive): the share of $t_2$ phantom brands still below the floor at $t_3$.

Seeds were fixed in the pre-registration (410041--410045). Spearman statistics use average ranks; every paired statistic uses pairwise definedness.

## 2.5 Parity gates

Four gates had to pass before any $t_3$ statistic was computed, and the scorer halts otherwise. P1: per-brand $\varphi$ recomputed from the frozen $t_1$ inputs reproduces the v1.8 instrument table for all 112 rows (definedness identical; absolute difference at most $10^{-9}$). P2: the recomputed pooled $\rho(\varphi_{t_1}, \varphi_{t_2})$ equals the v1.8 record, 0.6454 with $n = 83$. P3: the recomputed per-substrate CV-CPC $t_1 \rightarrow t_2$ $\rho$ reproduces the v0.34 verdicts for all five substrates. P4: the eight probe artifacts reproduce their $t_1$ checksums. The scorer was tested before the lock on six synthetic $t_3$ waves passed through the real extraction path, including a copy of $t_2$, a copy of $t_1$, a model-identity shuffle, a dropped model and a partial failure (76 of 76 tests).

## 2.6 Manipulation checks

`MC_ProbeParity` (P4 at scoring, plus the per-substrate checks during acquisition); `MC_Snapshot` (§2.2); `MC_Completeness`, requiring 852 of 852 study calls; and `MC_Truncation`, a descriptive record of calls that ended on a token limit, which $t_1$ and $t_2$ did not record.

## 2.7 Pre-registration and deviations

The pre-registration was locked at annotated tag `v0.41-prereg-r1` on 9 November 2026 and deposited on OSF (`ec6wh/v41/prereg`), where it was verified byte for byte before the first $t_3$ call. Three deviations were recorded, each before the step it concerns. Entry 1: the tag could not be pushed to the public repository before acquisition, so the tag object, commit and tree hashes and the SHA-256 of every locked file were deposited on OSF at 13:32 UTC, before the first study call, as the external anchor; the pushed tag must resolve to those hashes. Entry 2: the acquisition machine restarted during premium-spirits recognition, after 132 of 144 calls; the locked runner cannot resume, so the 132 answers were archived unanalysed and the substrate was re-run in full with the same runner. Entry 3: premium-spirits coding ran in a second Python environment because the coding script requires a library the acquisition environment lacks; the client library version was identical, and no coding rule, prompt or model changed.

# 3. Results

All four parity gates passed (P1: 112 of 112 rows, maximum absolute difference 0.0; P2: $\rho = 0.6454$, $n = 83$; P3: five of five; P4: eight of eight). All 852 study calls returned. `MC_Snapshot` passed for all four dated aliases. Table 1 reports the intervals and the brands with $\varphi$ defined in each wave.

\needspace{8\baselineskip}

Table: Intervals (days) and brands with $\varphi$ defined in each wave, by substrate. Undefined brands are all true zeros ($\hat\pi = 0$); no brand was named in every frame by every model in any wave.

| Substrate | $t_1$ | $t_1 \rightarrow t_2$ | $t_2 \rightarrow t_3$ | Brands | $\varphi$ $t_1$ | $\varphi$ $t_2$ | $\varphi$ $t_3$ |
|--------------|:------:|:----:|:----:|:----:|:----:|:----:|:----:|
| Headphones | 20 May | 21 | 152 | 16 | 12 | 13 | 12 |
| Skincare | 21 May | 20 | 152 | 24 | 19 | 18 | 17 |
| Cosmetics | 22 May | 19 | 152 | 24 | 19 | 20 | 19 |
| Automotive | 25 May | 16 | 152 | 24 | 15 | 16 | 16 |
| Spirits | 26 May | 15 | 152 | 24 | 19 | 21 | 19 |

## 3.1 Long-horizon stability of Consistency (`H_Phi_LongHorizon`)

Eighty brands had $\varphi$ defined at both $t_2$ and $t_3$ (12, 16, 19, 15 and 18 by substrate). Their pooled rank correlation was $\rho = 0.681$, with $p_{\text{perm}} = 0.0001$, the smallest value 10,000 draws can return. Against the frame-structure null, the shuffled correlations had a mean of 0.357 and a 95th percentile of 0.510, with a maximum of 0.661; none of the 10,000 reached the observed value ($p_{\text{frame}} = 0.0001$). All three conditions hold, and the verdict is **CONFIRMED**. The result is robust to the pre-registered sensitivity analyses: pooled within-substrate ranks give $\rho = 0.629$, and leaving out one substrate at a time gives $\rho = 0.637$--$0.730$. One headphones brand sits at the maximum possible value, $\varphi = 7.2$, in both waves: some models name it in every recall question and the rest never do.

![Per-brand $\varphi$ at $t_2$ (June) versus $t_3$ (November), coloured by substrate; dashed line = no change. One brand at $\varphi = 7.2$ in both waves lies off scale. Pooled $\rho = 0.68$ ($n = 80$), above both the permutation null and the frame-structure null (95th percentile 0.51).](../../reports/figs/v41/chart_01_phi_t2_t3.pdf){#fig:phi width=100%}

## 3.2 Long-horizon stability of Presence (`H_Presence_LongHorizon`)

Recall Presence held its brand order in every substrate: audiophile headphones $\rho = 0.944$ ($n = 16$), skincare $\rho = 0.941$, cosmetics $\rho = 0.941$, automotive $\rho = 0.976$ and premium spirits $\rho = 0.927$ ($n = 24$ each), each with $p_{\text{perm}} = 0.0001$. Five of five substrates meet the 0.70 criterion, and the verdict is **CONFIRMED**. Unlike recognition in v0.34, recall shows no ceiling: no brand was named in every frame by every model.

![Per-brand recall share $\hat\pi$ at $t_2$ versus $t_3$, by substrate; dashed line = no change. All five substrates exceed the 0.70 criterion ($\rho = 0.93$--$0.98$).](../../reports/figs/v41/chart_02_presence_t2_t3.pdf){#fig:presence width=100%}

## 3.3 Short versus long horizon (`H_Horizon_Decay`)

On the 80 brands with $\varphi$ defined in all three waves, $\rho(t_1,t_2) = 0.656$ and $\rho(t_1,t_3) = 0.638$, so $D = +0.019$ (95% interval $-0.132$ to $+0.168$). For recall Presence on all 112 brands, $\rho(t_1,t_2) = 0.965$ and $\rho(t_1,t_3) = 0.963$, so $D = +0.002$ ($-0.025$ to $+0.032$). Both intervals include zero, and both verdicts are **MARGINAL**: no decay is detectable. Figure 3 reports, descriptively, each instrument's correlation at all three horizons with pairwise definedness. $J$ was at least as stable over the long horizon as over the short one (0.719 at $t_1 \rightarrow t_2$; 0.801 at $t_2 \rightarrow t_3$). Recognition $C_P$ was the only instrument whose long-horizon correlation fell below its short-horizon value (0.957 to 0.865), within overlapping descriptive intervals.

![Rank stability at three horizons for $\varphi$, $J$, $\hat\pi$ and $C_P$, with descriptive 95% bootstrap intervals (2,000 resamples within substrate). The box reports the pre-registered decay contrast $D$ with its 10,000-resample interval.](../../reports/figs/v41/chart_03_horizon.pdf){#fig:horizon width=100%}

## 3.4 Change in Consistency versus change in Presence (`H_Drift_Dissociation`)

Across the 80 brands, the correlation between the change in $\varphi$ rank and the change in Presence rank from $t_2$ to $t_3$ was $\rho = 0.032$ (two-sided $p_{\text{perm}} = 0.777$), inside the confirmation band, and the verdict is **CONFIRMED**. Because both changes are measured from the same $t_2$ ranks, a $t_2$ association between $\varphi$ and $\hat\pi$ would induce some correlation between the changes even without joint movement; the pre-registered descriptive baseline was $\rho(\varphi_{t_2}, \hat\pi_{t_2}) = 0.151$ on within-substrate percentile ranks.

![Change in within-substrate $\varphi$ rank versus change in within-substrate Presence rank, $t_2$ to $t_3$, by substrate. $\rho = 0.03$ ($n = 80$).](../../reports/figs/v41/chart_04_drift_dissociation.pdf){#fig:drift width=100%}

## 3.5 Phantom persistence (`H_Phantom_LongPersistence`, descriptive)

Of the brands below the recall floor at $t_2$, 8 of 8 (headphones), 15 of 15 (skincare), 9 of 10 (cosmetics), 10 of 10 (automotive) and 14 of 15 (premium spirits) remained below it at $t_3$; pooled, 56 of 58 (0.966). v0.34 reported 56 of 57 over the short horizon.

## 3.6 Truncation

`MC_Truncation` recorded the share of calls ending on a token limit, across all calls in the provenance record (including the 132 interrupted premium-spirits calls and the judge's coding calls for Claude Sonnet 4.5): Gemini 2.5 Flash 58 of 164 (35%), Claude Opus 4.5 18 of 164 (11%), Gemini 2.5 Flash Lite 10 of 164 (6%), Claude Sonnet 4.5 1 of 193, and GPT-4o and GPT-4o mini none. The runners are verbatim, so token limits match $t_1$ and $t_2$; finish reasons were not recorded then, so no wave contrast is possible.

# 4. Discussion

The central result is that the v1.8 Consistency instrument keeps its brand order over five months. The point estimate at 152 days (0.681) is no lower than v1.8's 15--21-day figure (0.645), and the direct decay contrast on the same brands is indistinguishable from zero. The second condition matters as much as the correlation. The pre-lock calibration showed that a meaningful part of $\varphi$'s apparent stability comes from the questions rather than the models: when model identity is scrambled within each question, the rank correlation still averages about 0.36--0.39. The observed $t_2 \rightarrow t_3$ value exceeded every one of 10,000 such shuffles. Consistency therefore carries model-level structure that persists for months, not only the structure the questions impose. Reports of $\varphi$ stability that omit a question-structure null overstate what the instrument shows.

Presence was more stable still, at 0.93--0.98 in every category, and it did not saturate. This complements v0.34, where recognition sat at a ceiling in four of five categories and two pre-registered tests collapsed. Recall carries the variation recognition lacks, and the recall face of Presence is the part of the component that moves least over time. Recognition was the one instrument whose long-horizon correlation dipped below its short-horizon value. The dip is within overlapping descriptive intervals and was not tested, but it is consistent with recognition being near its ceiling, where a handful of single-model flips move ranks.

The dissociation result extends v1.8's static finding to change over time. A two-component construct needs components that are not only uncorrelated in a single cross-section but also move separately; the change correlation of 0.03 shows that a brand gaining or losing Presence over five months does not thereby gain or lose Consistency. Together with the v1.9 methodology result that a single 0--100 composite of the two ranks brands almost exactly as Presence does, this supports reporting Presence and Consistency side by side.

Phantom status persisted almost entirely over five months, as it did over three weeks. Brands that the panel does not name in June are, with two exceptions in 58, still not named in November.

# 5. Limitations

The three waves have unequal intervals, so the design supports a horizon contrast but not a drift-rate model. Google's aliases are undated, so Gemini-side version change between waves cannot be excluded, and $t_1$ recorded no served identifiers at all, so contrasts anchored at $t_1$ may include version change on any model. Runners that leave generation settings at provider defaults inherit any change in those defaults. Gemini 2.5 Flash ended 35% of its calls on its token limit, which can truncate recall lists; the setting is identical across waves, so the effect is common to all waves rather than a source of change. Brand counts are 16--24 per substrate, and $\varphi$ is defined for 80 of 112 brands in the long-horizon test, which bounds precision. The premium-spirits recognition judge is itself an LLM, pinned by alias and recorded by served version. The frame-structure condition was added before the lock in response to a calibration on $t_2$ data, which is disclosed in §2.4. Most importantly, every verdict binds this six-model panel; whether it carries to current models requires a new reference panel, which the program will choose and lock separately.

# 6. Future Research

This is the last wave this panel can give, so the next longitudinal question moves to a new panel: a reference panel of current models, measured at baseline and again after a comparable interval, with dated versions recorded from the first call. The frame-structure null should become standard for any consistency claim, and a decomposition of $\varphi$ into question-level and model-level parts is a natural methodology increment. The AIAS 2.0 synthesis will bind Presence and Consistency into the program's second construct claim, using the present results as its long-horizon reliability evidence.

# Declarations {-}

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-acquires measurements against brand registries fixed in earlier phases (v0.19--v0.23); it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward unchanged. Two items of record apply. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands --- Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) --- characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry, AKG was substituted with Denon before the v0.19 pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary. Acquisition, coding, and scoring are fully automated against the locked registries; the pre-registration was locked and deposited before any third-wave call; and the author's affiliation played no role in registry construction, acquisition, scoring, or the resulting verdicts. Samsung Electronics had no role in the design, conduct, analysis, or reporting of this work.

## Funding {-}

Self-funded. No external funding supported this research.

## Ethics {-}

Not applicable; no human subjects. The study queries large language models under their public interfaces.

## Use of AI tools {-}

The author used Anthropic's Claude to assist with analysis code, drafting and editing of text, and figure production. The study design, pre-registered hypotheses and decision rules, and all interpretations are the author's; the author reviewed all content and takes full responsibility for it.

## Data and code availability {-}

Materials are deposited at OSF, `ec6wh/v41`: the locked pre-registration and its anchor record (tag, commit and file hashes), the acquisition manifest with probe-set checksums, the pre-lock feasibility check, parity record and frame-structure calibration, and the deviations record. At publication the deposit adds the $t_3$ acquisition outputs and provenance sidecar, the scorer (`score_v41.py`) and its test suite, the verdicts (`v41_verdicts.json`), the three-wave table and the figure sources.

# References {-}

González Castro, P. U. (2026). *AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval*. SSRN 6659000.

González Castro, P. U. (2026). *The AIAS™ Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy* (v1.2). SSRN 6761698.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification* (v1.3). SSRN 6797679.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol v1.4: Recognition × Recall Decomposition and Multi-Component AI Availability*. SSRN 6799479.

González Castro, P. U. (2026). *The AIAS™ Presence Measurement Protocol: Multi-Statistic C2 Specification and Two-Channel Recall Decomposition* (v1.5). SSRN 6810758.

González Castro, P. U. (2026). *Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension* (AIAS Methodology v1.6). SSRN 6816340.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol: CPC Consistency --- A Pre-Registered Negative Result* (v1.7). SSRN 6878818.

González Castro, P. U. (2026). *A Mean-Independent Consistency Instrument for Cross-Model AI Presence: Redesigning CPC on a Quasi-Binomial Dispersion Basis* (AIAS Methodology v1.8). SSRN 6963359.

González Castro, P. U. (2026). *AI Availability as a Third Measurable Layer of Brand Availability: Five-Substrate Empirical Anchoring of the AIAS™ Presence Measurement Protocol* (AIAS 1.0). SSRN 6817841.

González Castro, P. U. (2026). *CPC Version-Snapshot Stability: A Two-Arm Cross-Generation Test* (v0.32). SSRN 6898581.

González Castro, P. U. (2026). *Provider-Asymmetric CPC: A Pre-Registered Re-Analysis* (v0.33). SSRN 6909019.

González Castro, P. U. (2026). *Two-Wave Temporal Stability of an AI Brand-Recall Consistency Quantity: A Pre-Registered Longitudinal Re-Acquisition Across Five Product Categories* (v0.34). SSRN 6915458.

González Castro, P. U. (2026). *Two-Component AIAS Composite Calibration: Presence × Consistency* (AIAS Methodology v1.9). Working paper; OSF `ec6wh/methodology/v1_9`.

González Castro, P. U. (2026). *AI Presence in Audiophile headphones: AIAS v0.19*. SSRN 6809182.

González Castro, P. U. (2026). *AI Presence in Skincare: AIAS v0.20*. SSRN 6811441.

González Castro, P. U. (2026). *AI Presence in Cosmetics: AIAS v0.21*. SSRN 6815378.

González Castro, P. U. (2026). *AIAS™ v0.22 --- Automotive Substrate: Phantom Brand Persistence on a Heritage-Saturated Category*. SSRN 6829118.

González Castro, P. U. (2026). *AIAS™ v0.23 --- Premium Spirits Substrate*. SSRN 6834298.

Romaniuk, J., & Sharp, B. (2022). *How Brands Grow, Part 2* (Revised ed.). Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.
