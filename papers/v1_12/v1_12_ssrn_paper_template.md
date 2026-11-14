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

Pre-registration: \texttt{ {{PREREG_TAG}} } (commit \texttt{ {{PREREG_COMMIT}} }; deposited on OSF before the first v1.12 call)\\
Data and code: OSF \texttt{ec6wh}, \texttt{methodology/v1\_12}\\

\end{center}
\end{titlepage}

# Abstract {-}

Presence records whether AI answers name a brand; it does not record whether the brand is named across the buying situations of its category or only in a few. This pre-registered study specifies a Coverage instrument for the AIAS measurement programme and tests whether it is a separate component. Seventy brand-free questions, one per category entry point (14 per category, two for each of seven cue types), were asked in three runs to the newest flagship model of each of three providers (Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon) and to Claude Opus 5.5, over five categories and 112 brands; {{MC_ANSWERED}} of {{MC_EXPECTED}} calls were answered. The component score, Cov*, measures within each model how many situations a brand's mentions touch against the number expected if the brand were named without regard to the situation, given the same number of mentions; {{RATED_N}} brands met its rating floor.
{% switch CASE_MSIT %}
{% case PASSED %}
The situations changed which brands were named (instrument check passed: brand sets overlapped {{MSIT_DIFF}} more between runs of one question than between questions).
{% case FAILED %}
The situations did not change which brands were named enough to pass the pre-registered instrument check (overlap difference {{MSIT_DIFF}} against a minimum of 0.10), so Coverage cannot differ from Presence on this instrument.
{% endswitch %}
Within category, Cov* correlated with Presence at ρ = {{H1_RHO}} (H1 {{H1_WORD}}), with Consistency at ρ = {{H2_RHO}} (H2 {{H2_WORD}}) and with the brand's own naming rate at ρ = {{H3_RHO}} (H3 {{H3_WORD}}); its split-half reliability was {{H4_REL}} (H4 {{H4_WORD}}).
{% switch CASE_GATE %}
{% case PASS %}
Every gate leg was confirmed, and the pre-registered gate returned PASS: Coverage breadth is a component separable from Presence and Consistency, and the instrument passes to a second paper.
{% case FAIL %}
At least one gate leg was falsified, and the pre-registered gate returned FAIL: on this instrument Coverage breadth is not separable from {{FAIL_LEGS_PLAIN}}, and no second paper follows on it. The negative result is reported with the prominence of a pass.
{% case MARGINAL %}
No gate leg was falsified, but not every leg was confirmed (not confirmed: {{MARGINAL_LEGS_PLAIN}}), and the pre-registered gate returned MARGINAL; a second paper follows only on the pre-registrant's recorded decision.
{% case MARGINAL_H7 %}
Every gate leg was confirmed, but separability against the published Presence scores of the earlier panel was falsified, and under the pre-registered rule the gate's PASS is downgraded to MARGINAL.
{% case MARGINAL_TWO_MODEL %}
Every gate leg was confirmed on a reduced, two-model panel, and under the pre-registered drop rule the gate returned at most MARGINAL.
{% case UNDETERMINED %}
The pre-registered gate returned UNDETERMINED: {{UNDET_LEGS_PLAIN}} could not be decided on the data, and no second paper follows until that cause is fixed.
{% case INSTRUMENT_FAIL %}
The pre-registered gate therefore returned INSTRUMENT FAIL, a negative result; the separability statistics are reported for the record.
{% endswitch %}
The cross-category baseline reports raw and rate-adjusted Coverage per category, model and cue type on the newest models.

**Keywords:** AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; category entry points; large language models; Coverage; separability; measurement validity; Double Jeopardy

**JEL codes:** M31; L86, L15, D83, M37

**Paper status:** Pre-registered methodology paper with new acquisition (tag `{{PREREG_TAG}}`, deposited on OSF before the first call); {{MC_ANSWERED}} of {{MC_EXPECTED}} design calls answered; Paper A verdict {{GATE_LABEL}}; {{DEV_STATUS}} Part of the AIAS measurement programme.

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

Panel N3 comprises the newest generally available flagship model of each provider: Claude Fable 5.2, GPT-6 Astra and Gemini 4 Argon, the panel of the programme's fourth omnibus wave ($t_4$, v0.42). Claude Opus 5.5 was collected for continuity: panel C3 replaces Claude Fable 5.2 with it, and A4 comprises all four models (descriptive). N3 is the primary panel unless Claude Fable 5.2 leaves the panel under the pre-registered drop rule (§2.7), in which case C3 becomes the primary panel{% if PRIMARY_C3 %}; Claude Fable 5.2 left the panel, so C3 is the primary panel throughout{% else %}; Claude Fable 5.2 did not leave the panel, so N3 is the primary panel throughout{% endif %}. All calls were made without tools (S0), with provider-default decoding as in $t_4$: no temperature, top-p, top-k or reasoning-effort parameter was sent, and the output cap was 16,384 tokens. The design is 4 models × 75 probes × 3 runs = 900 independent calls. The collection script refused to start until the pre-registration tag was public and its OSF anchor named the tag's commit, until the $t_4$ collection was recorded complete, and while any other paid collection ran; it sent calls only inside the pre-registered windows, under a hard cap of US\$100 for all calls.

## 2.3 Mentions and raw coverage

A brand is mentioned in an answer when the certified detector of its category finds it in the visible answer text with URLs removed, exactly as in $t_4$; the coder is v0.42's, used unchanged. A call without a valid answer after retries is a missing cell: it enters no denominator and is never read as "not named". Model $m$ covers brand $b$ in CEP $j$ if it names $b$ in at least two of its three runs. Raw coverage $\text{Cov}_b$ is the share of the 14 CEPs in which at least $k = 2$ of the primary panel's models cover $b$ (sensitivities $k = 1$ and $k = 3$). The naming rate $\pi_{\text{cov},b}$ is the share of the panel's answered CEP answers in $b$'s category that name $b$.

## 2.4 Coverage breadth Cov*

Breadth is measured within each model, so between-model differences (which are Consistency) do not enter, and against the spread that naming blind to the situation would give with the same number of mentions, so the naming rate does not enter. For brand $b$ and model $m$, let $n$ be the number of $m$'s answered CEP answers that name $b$ and $c$ the number of CEPs touched (named in at least one run). Under the situation-blind null, $P(y_{b,m,s} = 1) = \text{logistic}(\theta_b + \delta_{m,j(s)})$ for answer slot $s$: a CEP may draw longer or shorter lists of brands, but no brand is tied to a situation. Given $n$, the null distribution of $c$ does not depend on $\theta_b$. The CEP effects $\hat\delta^{(-b)}_{m,j}$ are fitted by maximum likelihood on the other registry brands of the category (leave-$b$-out, deterministic Newton steps; a fit that does not converge sets $\delta = 0$ and is counted). $E_{b,m}$ is the exact expected number of CEPs touched given $n$ under that null, computed from its generating function without simulation. With $c_{\max}$ and $c_{\min}$ the largest and smallest numbers of CEPs that $n$ mentions can touch,

$$
\beta_{b,m} = \frac{c - E_{b,m}}{c_{\max} - c_{\min}} \quad (\beta = 0 \text{ if } c_{\max} = c_{\min}), \qquad \text{Cov}^*_b = 50\,\bigl(1 + \overline{\beta}_{b,\cdot}\bigr),
$$

with the mean over the panel's models that name $b$ at least once. Cov* = 50 is situation-blind naming; above 50 the brand's mentions spread over more situations than that, below 50 they are packed into fewer. Cov* is rated only when the panel's mentions of $b$ total at least 14 and at least two panel models name it; otherwise it is not rated (no shrinkage, no imputation).

Because $\beta$ is linear in $c$ and $E$ is exact, $\beta$ has zero expectation under the null at every $n$, whatever the naming rate. Before the lock this was checked on synthetic situation-blind data (calibration N1: {{N1_UNITS}} rated units in {{N1_CATS}} synthetic categories). The pooled centred $\rho_w(\text{Cov}^*, \pi_{\text{cov}})$ was {{N1_RHO}} against a limit of $|\rho_w| \leq 0.05$, and the largest deviation of a naming-rate decile's mean Cov* from 50 was {{N1_DEC}} against a limit of 2.5; N1 returned {{N1_RESULT}}. Two earlier versions of the score failed this calibration and were replaced before the lock.

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

The Paper A verdict follows a fixed order. (1) INSTRUMENT FAIL if the instrument check `MC_Situation` fails: if situations do not change which brands are named, Coverage cannot differ from Presence. (2) Otherwise FAIL if any of H1–H4 or an active gating H5 or H6 is FALSIFIED. (3) Otherwise UNDETERMINED if any of them is UNDETERMINED. (4) Otherwise PASS if all are CONFIRMED, downgraded to MARGINAL if H7 is FALSIFIED. (5) Otherwise MARGINAL. Secondary tests never turn a FAIL into a PASS. A model with fewer than 90% of its calls answered leaves the panel (the drop rule): if Claude Fable 5.2 leaves, C3 replaces N3 as the primary panel; if GPT-6 Astra or Gemini 4 Argon leaves, the gate is computed on the two remaining models and capped at MARGINAL. {% if PRIMARY_C3 %}The gate is repeated on A4 for the record.{% else %}The gate is repeated on C3 and A4 for the record.{% endif %}

## 2.8 Checks and sensitivity analyses

`MC_Situation` is computed per model, run and category: $J_{\text{between}}$ is the mean Jaccard similarity of the registry-brand sets named in answers to different CEPs, and $J_{\text{within}}$ the mean between runs of the same CEP. It passes if the pooled mean of $J_{\text{within}} - J_{\text{between}}$ is at least 0.10 and the pooled mean $J_{\text{between}}$ is at most 0.60. `MC_Complete` requires at least 98% of the 900 calls answered; `MC_Served`, `MC_Settings`, `MC_Truncation` (more than 5% of a model's calls at the output cap is flagged), `MC_RegistryShare` (a category in which fewer than half the CEP answers name a registry brand is flagged), `MC_Defunct` (automotive brands no longer sold named in more than 5% of automotive CEP answers is flagged), `MC_Positive` (raw Cov must correlate with the naming rate at $|\rho_w| \geq 0.50$, or the gate's sensitivity is flagged) and `MC_Window` complete the checks. Three parity gates ran before any statistic: the coder reproduces the locked $t_3$ mention codes (P1), the comparators reproduce v0.42's values (P2), and the probes sent equal the probe file (P3).

Ten sensitivity analyses were pre-registered and never change a verdict: S1 raw Cov through H1–H3; S2 rating floors 6 and 28; S3 an equal-weight null; S4 only models with room to vary; S5 leave one category out; S6 leave one cue type out; S7 $\hat\pi$ and total $t_4$ mentions in place of $P_{N3}$; S8 a mid-$p$ version of $\beta$; S9 the uncentred $\rho_w$; and S10 the gate legs without Denon (§Declarations).

## 2.9 Pre-registration

The pre-registration (revision r1) was locked at git tag `{{PREREG_TAG}}` (commit `{{PREREG_COMMIT}}`) and deposited on OSF (`ec6wh`, `methodology/v1_12/prereg/` and `anchor/`) with the SHA-256 of every locked file before any v1.12 call; its anchor record names the tag's commit. It was locked on 11 November 2026 at 02:45 UTC, before the earliest lock time its text states (11 November, about 3 pm CT), because the pre-registrant (the author) waived the programme's 24-hour review period on 10 November at 20:26 CT; `anchor/DEVIATIONS.md` records the waiver and the lock time in an entry made before the tag, and the locked text is unchanged by it. The scorer (`score_v1_12.py`) was written and unit-tested on synthetic data before the lock and run once, after the parity gates. Choices the pre-registration leaves open are listed in the scorer's notes and in the pre-registration's change log. {{DEV_SENTENCE}}

# 3. Results

## 3.1 Parity gates and data checks

{% switch CASE_PARITY %}
{% case PASSED %}
All three parity gates passed before any statistic was computed (P1, P2 and P3).
{% case SYNTHETIC %}
[Synthetic test run: parity gate P1 was not run; P2 {{P2_STATUS}}; P3 {{P3_STATUS}}.]
{% endswitch %}
{{MC_ANSWERED}} of the {{MC_EXPECTED}} design calls were answered ({{MC_SHARE}}), and `MC_Complete` {% if MC_COMPLETE_PASS %}passed{% else %}failed its 98% threshold{% endif %}. {% if ANY_DROPPED %}{{DROPPED_SENTENCE}}{% else %}No model fell below the 90% floor, so no model left the panel.{% endif %} {% if MC_SERVED_PASS %}`MC_Served` passed: every answered call was served by the requested model or a dated snapshot of it.{% else %}`MC_Served` failed: {{MC_SERVED_N}} answered calls were served by another model and were excluded.{% endif %} {% if MC_SETTINGS_PASS %}Every call carried the recorded decoding settings (`MC_Settings`).{% else %}`MC_Settings` failed: {{MC_SETTINGS_MISSING}} records lacked the recorded settings.{% endif %} {% if MCT_ANY_FLAG %}`MC_Truncation` flagged {{MCT_FLAGGED}}.{% else %}No model ended more than 5% of its calls at the output cap (`MC_Truncation`).{% endif %} {{FA_SENTENCE}} The first call started at {{WIN_FIRST}} and the last ended at {{WIN_LAST}} (UTC), a span of {{WIN_SPAN}} hours, and `MC_Window` {% if WIN_PASS %}passed{% else %}failed{% endif %}. Recorded spend on all billed requests was {{SPEND_TOTAL}}.

{% if REGSHARE_ANY_FLAG %}`MC_RegistryShare` flagged {{REGSHARE_FLAGGED}}: fewer than half of the CEP answers named a registry brand, so the registry may not represent situation answers there.{% else %}In every category at least half of the CEP answers named a registry brand (`MC_RegistryShare`; lowest share {{REGSHARE_MIN}}).{% endif %} {% if DEFUNCT_FLAG %}`MC_Defunct` was flagged: automotive brands no longer sold were named in {{DEFUNCT_SHARE}} of automotive CEP answers, above the 5% limit; this is phantom contamination, carried to the second paper.{% else %}Automotive brands no longer sold were named in {{DEFUNCT_SHARE}} of automotive CEP answers, within the 5% limit (`MC_Defunct`).{% endif %} {% if POSITIVE_FLAG %}`MC_Positive` was flagged: raw Cov correlated with the naming rate at $\rho_w = {{POSITIVE_RHO}}$, below the 0.50 the gate needs to show it can detect coupling.{% else %}Raw Cov correlated with the naming rate at $\rho_w = {{POSITIVE_RHO}}$, so the gate can detect the coupling it tests for (`MC_Positive`).{% endif %} {{DELTA_SENTENCE}}

Table: Calls answered, mean reasoning tokens and output-cap endings per model (expected: 225 calls per model).

{{TABLE_MC}}

## 3.2 Do situations change the brands named? (`MC_Situation`)

Across {{MSIT_CELLS}} model × run × category cells of panel {{PRIMARY}}, brand sets named in answers to the same CEP in different runs overlapped with a mean Jaccard similarity of {{MSIT_JW}}, and brand sets named in answers to different CEPs with {{MSIT_JB}}. The pooled difference was {{MSIT_DIFF}}.
{% switch CASE_MSIT %}
{% case PASSED %}
It meets the pre-registered minimum of 0.10, and $J_{\text{between}}$ is within the limit of 0.60, so the instrument check passed: the situations change which brands are named.
{% case FAILED %}
The check requires a difference of at least 0.10 and $J_{\text{between}}$ at most 0.60; it failed, and under the gate the Paper A verdict is INSTRUMENT FAIL whatever the separability legs show.
{% endswitch %}
Answers to CEPs overlapped with the control answer of the same model and run at a mean Jaccard similarity of {{MSIT_C0}}. Figure 1 shows the cells.

![Mean Jaccard similarity of registry-brand sets between runs of one CEP (vertical) and between different CEPs (horizontal), one point per model, run and category of panel {{PRIMARY}}. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_01_situation_overlap.pdf){#fig:msit width=92%}

## 3.3 The gate legs: separability and reliability

Table 3 gives every leg on panel {{PRIMARY}} and Figure 2 their correlations against the bands.{% if CROSS_PANEL %} H1 and H2 use the published AIAS 2.0 $t_3$ values (cross-panel): {{CROSS_REASON}}.{% endif %}

Table: Hypothesis legs on panel {{PRIMARY}}, search off: pooled within-category $\rho_w$ with its 95% bootstrap interval, permutation $p$ and verdict (the scorer's words).

{{TABLE_LEGS}}

![Pooled within-category $\rho_w$ of Cov* with each comparator, with 95% bootstrap intervals; shaded: the separability bands (H1--H3, H5--H7) and the reliability and replication bars (H4, H8). {{FIG_CAPTION}}]({{FIG_DIR}}/chart_02_legs_bands.pdf){#fig:legs width=100%}

**Presence (H1).** {% switch CASE_H1 %}{% case CONFIRMED %}Across {{H1_N}} rated brands in {{H1_NCAT}} categories, $\rho_w(\text{Cov}^*, P_{N3}) = {{H1_RHO}}$ (95% interval {{H1_CI_LO}} to {{H1_CI_HI}}; two-sided $p_{\text{perm}} = {{H1_P}}$). $|\rho_w|$ is at most 0.30, and H1 is **CONFIRMED**: how widely a brand's mentions spread over situations does not follow how present the brand is.{% case MARGINAL %}Across {{H1_N}} rated brands in {{H1_NCAT}} categories, $\rho_w(\text{Cov}^*, P_{N3}) = {{H1_RHO}}$ (95% interval {{H1_CI_LO}} to {{H1_CI_HI}}; two-sided $p_{\text{perm}} = {{H1_P}}$). $|\rho_w|$ lies between 0.30 and 0.50, and H1 is **MARGINAL**.{% case FALSIFIED %}Across {{H1_N}} rated brands in {{H1_NCAT}} categories, $\rho_w(\text{Cov}^*, P_{N3}) = {{H1_RHO}}$ (95% interval {{H1_CI_LO}} to {{H1_CI_HI}}; two-sided $p_{\text{perm}} = {{H1_P}}$). $|\rho_w|$ is at least 0.50, and H1 is **FALSIFIED**: Cov* moves with Presence.{% case UNDETERMINED_FLOOR %}Only {{H1_N}} rated brands in {{H1_NCAT}} categories with at least five entered, below the floor of 30 units in three categories, and H1 is **UNDETERMINED**.{% case UNDETERMINED_REASON|UNDETERMINED_DEGENERATE %}H1 is **UNDETERMINED**: {{H1_WHY}}.{% endswitch %} Figure 3 shows the brands.

![Cov* (panel {{PRIMARY}}) and Presence $P_{N3}$ per rated brand, by category. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_03_cov_presence.pdf){#fig:h1 width=88%}

**Consistency (H2).** {% switch CASE_H2 %}{% case CONFIRMED %}Across {{H2_N}} brands rated on both scores in {{H2_NCAT}} categories, $\rho_w(\text{Cov}^*, C^*_{N3}) = {{H2_RHO}}$ (95% interval {{H2_CI_LO}} to {{H2_CI_HI}}; $p_{\text{perm}} = {{H2_P}}$). $|\rho_w|$ is at most 0.30, and H2 is **CONFIRMED**.{% case MARGINAL %}Across {{H2_N}} brands rated on both scores in {{H2_NCAT}} categories, $\rho_w(\text{Cov}^*, C^*_{N3}) = {{H2_RHO}}$ (95% interval {{H2_CI_LO}} to {{H2_CI_HI}}; $p_{\text{perm}} = {{H2_P}}$). $|\rho_w|$ lies between 0.30 and 0.50, and H2 is **MARGINAL**.{% case FALSIFIED %}Across {{H2_N}} brands rated on both scores in {{H2_NCAT}} categories, $\rho_w(\text{Cov}^*, C^*_{N3}) = {{H2_RHO}}$ (95% interval {{H2_CI_LO}} to {{H2_CI_HI}}; $p_{\text{perm}} = {{H2_P}}$). $|\rho_w|$ is at least 0.50, and H2 is **FALSIFIED**: Cov* moves with Consistency.{% case UNDETERMINED_FLOOR %}Only {{H2_N}} brands rated on both scores in {{H2_NCAT}} categories with at least five entered, below the floor, and H2 is **UNDETERMINED**.{% case UNDETERMINED_REASON|UNDETERMINED_DEGENERATE %}H2 is **UNDETERMINED**: {{H2_WHY}}.{% endswitch %} Figure 4 shows the brands.

![Cov* (panel {{PRIMARY}}) and Consistency $C^*_{N3}$ per brand rated on both. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_04_cov_consistency.pdf){#fig:h2 width=88%}

**Naming rate (H3).** {% switch CASE_H3 %}{% case CONFIRMED %}Across {{H3_N}} rated brands, $\rho_w(\text{Cov}^*, \pi_{\text{cov}}) = {{H3_RHO}}$ (95% interval {{H3_CI_LO}} to {{H3_CI_HI}}; $p_{\text{perm}} = {{H3_P}}$). $|\rho_w|$ is at most 0.30, and H3 is **CONFIRMED**: in the Coverage answers themselves, the score does not follow how often the brand is named, the test the v1.7 instrument failed.{% case MARGINAL %}Across {{H3_N}} rated brands, $\rho_w(\text{Cov}^*, \pi_{\text{cov}}) = {{H3_RHO}}$ (95% interval {{H3_CI_LO}} to {{H3_CI_HI}}; $p_{\text{perm}} = {{H3_P}}$). $|\rho_w|$ lies between 0.30 and 0.50, and H3 is **MARGINAL**.{% case FALSIFIED %}Across {{H3_N}} rated brands, $\rho_w(\text{Cov}^*, \pi_{\text{cov}}) = {{H3_RHO}}$ (95% interval {{H3_CI_LO}} to {{H3_CI_HI}}; $p_{\text{perm}} = {{H3_P}}$). $|\rho_w|$ is at least 0.50, and H3 is **FALSIFIED**: on real answers the score moves with the naming rate, although it did not on the situation-blind calibration data, so real answers depart from the null's form.{% case UNDETERMINED_FLOOR %}Only {{H3_N}} rated brands in {{H3_NCAT}} categories with at least five entered, below the floor, and H3 is **UNDETERMINED**.{% case UNDETERMINED_REASON|UNDETERMINED_DEGENERATE %}H3 is **UNDETERMINED**: {{H3_WHY}}.{% endswitch %} Raw Cov, by contrast, correlated with the naming rate at $\rho_w = {{POSITIVE_RHO}}$ (Figure 5).

![Left: Cov* against the naming rate $\pi_{\text{cov}}$ per rated brand. Right: raw Cov ($k = 2$) against the same rate, all brands. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_05_naming_rate.pdf){#fig:h3 width=100%}

**Reliability (H4).** {% switch CASE_H4 %}{% case CONFIRMED|MARGINAL|FALSIFIED %}Cov* computed on CEP half A and on half B correlated at $r = {{H4_RHO}}$ across {{H4_N}} brands rated on both halves (one-sided $p_{\text{perm}} = {{H4_P}}$), a split-half reliability of rel $= {{H4_REL}}$ (95% interval {{H4_REL_LO}} to {{H4_REL_HI}}).{% case UNDETERMINED_FLOOR %}Only {{H4_N}} brands in {{H4_NCAT}} categories with at least five were rated on both halves (floor: seven mentions per half), below the floor of 30 units in three categories.{% case UNDETERMINED_REASON|UNDETERMINED_DEGENERATE %}The split-half statistic could not be computed: {{H4_WHY}}.{% endswitch %}
{% switch CASE_H4 %}
{% case CONFIRMED %}
That meets rel $\geq 0.50$ with $p < .05$, and H4 is **CONFIRMED**: Cov* orders brands alike on two disjoint sets of situations.
{% case MARGINAL %}
That is not below 0.30 and does not meet rel $\geq 0.50$ with $p < .05$, and H4 is **MARGINAL**.
{% case FALSIFIED %}
That is below 0.30 or not significant at .05, and H4 is **FALSIFIED**: on seven situations per half, Cov* does not order brands reproducibly.
{% case UNDETERMINED_FLOOR|UNDETERMINED_REASON|UNDETERMINED_DEGENERATE %}
H4 is **UNDETERMINED**.
{% endswitch %}
Figure 6 shows the brands.

![Cov* on CEP half A and on half B (seven CEPs each) per brand rated on both halves. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_06_halves.pdf){#fig:h4 width=88%}

## 3.4 Conditional legs: Ranking and Sentiment

{% switch CASE_H5 %}
{% case INACTIVE %}
H5 (Ranking) is INACTIVE: its activation condition was not met, so it has no verdict and may be tested only under a later pre-registration.
{% case GATING %}
H5 (Ranking) was active and gating: v1.14's Stage 1 interim verdict was {{H5_STAGE1}}. Across {{H5_N}} brands rated on both, $\rho_w(\text{Cov}^*, R^*_{S0}) = {{H5_RHO}}$ (95% interval {{H5_CI_LO}} to {{H5_CI_HI}}; $p_{\text{perm}} = {{H5_P}}$), and H5 is **{{H5_WORD}}**.
{% case REPORTED %}
H5 (Ranking) was computed and is reported without gating: v1.14's Stage 1 interim verdict was {{H5_STAGE1}}, not SEPARABLE, so under the pre-registered rule H5 neither gates nor downgrades. Across {{H5_N}} brands rated on both, $\rho_w(\text{Cov}^*, R^*_{S0}) = {{H5_RHO}}$ (95% interval {{H5_CI_LO}} to {{H5_CI_HI}}), which reads **{{H5_WORD}}** under the separability bands.
{% case UNAVAILABLE %}
H5 (Ranking) was active, but v1.14's Stage 1 output, which supplies $R^*_{S0}$, was not available ({{H5_WHY}}); H5 is **UNDETERMINED** and, under the pre-registered rule, neither gates nor downgrades.
{% endswitch %}
{% switch CASE_H6 %}
{% case INACTIVE %}
H6 (Sentiment) is INACTIVE: no Sentiment score on the $t_4$ answers was pre-registered and tagged before this study's lock.
{% case ACTIVE %}
H6 (Sentiment) was active: $\rho_w(\text{Cov}^*, S) = {{H6_RHO}}$ across {{H6_N}} brands, and H6 is **{{H6_WORD}}**.
{% endswitch %}

## 3.5 Secondary tests

**Published Presence (H7).** {% switch CASE_H7 %}{% case CONFIRMED|MARGINAL|FALSIFIED %}Against the published AIAS 2.0 Presence of the legacy six-model panel at $t_3$, $\rho_w = {{H7_RHO}}$ across {{H7_N}} brands (95% interval {{H7_CI_LO}} to {{H7_CI_HI}}), and H7 is **{{H7_WORD}}**{% if H7_DOWNGRADES %}; a FALSIFIED H7 downgrades a PASS to MARGINAL (§3.6){% endif %}.{% case UNDETERMINED_FLOOR|UNDETERMINED_REASON|UNDETERMINED_DEGENERATE %}H7 is **UNDETERMINED**: {{H7_WHY}}.{% endswitch %}

**Panel replication (H8).** {% switch CASE_H8 %}{% case CONFIRMED|MARGINAL|FALSIFIED %}Cov* on panel N3 and on panel C3, which replaces Claude Fable 5.2 with Claude Opus 5.5, correlated at $\rho_w = {{H8_RHO}}$ across {{H8_N}} brands rated on both (one-sided $p_{\text{perm}} = {{H8_P}}$), and H8 is **{{H8_WORD}}** (Figure 7).{% case UNDETERMINED_FLOOR|UNDETERMINED_REASON|UNDETERMINED_DEGENERATE %}H8 is **UNDETERMINED**: {{H8_WHY}} (Figure 7).{% endswitch %}

![Cov* on panel N3 and on panel C3 (Claude Opus 5.5 in place of Claude Fable 5.2) per brand rated on both. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_07_panel_replication.pdf){#fig:h8 width=88%}

## 3.6 The Paper A verdict

{% switch CASE_GATE %}
{% case PASS %}
`MC_Situation` passed and every gate leg ({{GATE_LEG_LIST}}) was CONFIRMED; H7 was not FALSIFIED. The Paper A verdict is **PASS**.
{% case FAIL %}
`MC_Situation` passed, but {{FAIL_LEGS}} {{FAIL_VERB}} FALSIFIED. The Paper A verdict is **FAIL**: a negative result, reported with the same prominence as a pass, and no second paper follows on this instrument.
{% case MARGINAL %}
`MC_Situation` passed and no gate leg was FALSIFIED or UNDETERMINED, but {{MARGINAL_LEGS}} {{MARGINAL_VERB}} MARGINAL. The Paper A verdict is **MARGINAL**: a second paper follows only on the pre-registrant's recorded decision, with the marginal leg as its first confirmatory test.
{% case MARGINAL_H7 %}
`MC_Situation` passed and every gate leg ({{GATE_LEG_LIST}}) was CONFIRMED, but H7 was FALSIFIED, and under the pre-registered rule the PASS is downgraded. The Paper A verdict is **MARGINAL**: a second paper follows only on the pre-registrant's recorded decision.
{% case MARGINAL_TWO_MODEL %}
Every gate leg ({{GATE_LEG_LIST}}) was CONFIRMED, but on a two-model panel ({{DROPPED_NAMES}} left under the drop rule), where the gate is capped at MARGINAL. The Paper A verdict is **MARGINAL**.
{% case UNDETERMINED %}
`MC_Situation` passed and no gate leg was FALSIFIED, but {{UNDET_LEGS}} {{UNDET_VERB}} UNDETERMINED. The Paper A verdict is **UNDETERMINED**: its data cause is reported above, and no second paper follows until it is fixed.
{% case INSTRUMENT_FAIL %}
`MC_Situation` failed, and the Paper A verdict is **INSTRUMENT FAIL** whatever the separability legs show; they are reported above for the record.
{% endswitch %}
The scorer's label is "{{GATE_LABEL}}". {% if PRIMARY_C3 %}Repeated on all four models (A4) the gate returns {{GATE_A4}}; the repetition is reported and changes nothing.{% else %}Repeated on the continuity panel C3 the gate returns {{GATE_C3}}, and on all four models (A4) {{GATE_A4}}; these repetitions are reported and change nothing.{% endif %}

## 3.7 Sensitivity analyses

Table 4 gives $\rho_w$ for the gate legs under each pre-registered sensitivity. {{SENS_CHANGES_SENTENCE}} Leaving one category out (S5), $\rho_w$ for H1 ranged from {{S5_H1_LO}} to {{S5_H1_HI}} and for H3 from {{S5_H3_LO}} to {{S5_H3_HI}}. {{S6_SENTENCE}} {{S7_SENTENCE}}

Table: Pre-registered sensitivity analyses (§2.8): pooled within-category $\rho_w$ of each gate leg; a verdict different from the primary one is marked with its word. Sensitivities never change a verdict.

{{TABLE_SENS}}

## 3.8 Cross-category baseline (descriptive)

Table 5 and Figure 8 describe Coverage per category on panel {{PRIMARY}}. {{BASE_SENTENCE}} Run-to-run reliability of the naming of brands, the noise floor for a second paper, was rel1 = {{REL1_MIN}} to {{REL1_MAX}} across the four models (one run against another; Appendix). Answers named a mean of {{BRANDS_MIN}} to {{BRANDS_MAX}} registry brands per CEP answer across categories and models. Non-registry brand mentions were not counted, because no detector for brands outside the registries was pre-registered.

Table: Coverage per category on panel {{PRIMARY}}: rated brands, Cov* (median and interquartile range) and raw Cov at $k = 2$ (median), with the share of CEPs in which no panel answer named a registry brand.

{{TABLE_BASE}}

![Cov* per rated brand by category on panel {{PRIMARY}}; 50 = situation-blind naming. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_08_baseline.pdf){#fig:base width=92%}

# 4. Discussion

{% switch CASE_GATE %}
{% case PASS %}
Coverage breadth, measured as Cov*, passed its separability gate: brand-free situation questions change which brands AI answers name, and the rate-adjusted breadth of a brand's naming across those situations is separable from Presence, from Consistency and from the brand's own naming rate, and orders brands alike on two disjoint halves of the situations. The programme can treat Coverage as a third component on this instrument. The raw share of situations covered behaved as Double Jeopardy predicts and is not the component; Cov* is. The second paper inherits the frozen CEP sets, probes, coder and scorer, and its first studies are the sensitivity of Cov* to the choice of situations and the typology of broad and situation-bound brands.
{% case FAIL %}
Coverage breadth, as measured here, did not pass its gate: {{FAIL_LEGS}} {{FAIL_VERB}} FALSIFIED. Under the pre-registered rule this is a negative result with the standing of a pass, as v1.7's was for the first Consistency instrument. It does not show that situation breadth is irrelevant to AI Availability; it shows that this instrument does not separate it from {{FAIL_LEGS_PLAIN}} on these categories and models. A redesigned instrument would need its own pre-registration and calibration.
{% case MARGINAL|MARGINAL_H7|MARGINAL_TWO_MODEL %}
The gate's result is intermediate: no leg falsified separability, but not every condition for a pass was met. Under the pre-registered rule a second paper may follow only on the pre-registrant's recorded decision, and the marginal condition becomes its first confirmatory test. Until then Cov* is a candidate component, reported beside Presence and Consistency without being combined with them.
{% case UNDETERMINED %}
The gate could not decide: {{UNDET_LEGS}} {{UNDET_VERB}} UNDETERMINED for the data cause reported in §3. The instrument is neither adopted nor rejected, and no second paper follows until that cause is fixed under a recorded deviation or a new collection.
{% case INSTRUMENT_FAIL %}
The situation questions did not change which brands the models named enough to pass the instrument check. Without that, a breadth score can only re-express Presence, and the gate ends at INSTRUMENT FAIL. The separability statistics are reported for the record and carry no verdict on Coverage as a construct; a different set of situations, or a different way of asking, would need its own pre-registration.
{% endswitch %}

{% if POSITIVE_FLAG %}`MC_Positive` was flagged: raw Cov did not reach the coupling with the naming rate that Double Jeopardy predicts, so the gate's power to detect coupling on these data is in question, and confirmed separability legs should be read with that flag.{% else %}Raw Cov behaved as Double Jeopardy predicts, following the naming rate (`MC_Positive`), which shows that the gate could detect the coupling it tests for.{% endif %} The baseline of §3.8 describes, on the newest models, how widely each category's brands are named across situations; it carries no verdict.{{BASE_BELOW50}}

# 5. Limitations

There is one set of 14 situations per category, drafted by one procedure and by a model that is also a panel model; the sensitivity of Cov* to the choice of situations is the second paper's first study. Coverage is measured among registry brands only (16 to 24 per category), while answers also name other brands. Three runs estimate within-situation noise only coarsely; Cov* uses runs as replicates, so its reliability is judged across halves of seven situations, which is conservative. Panels N3 and C3 share two models, and Consistency on three models is noisier than on six. The study covers one market and language (US English), search off only, and no situation is weighted by how common it is among buyers, which Ehrenberg-Bass practice does with buyer data. Cov*'s null is a logistic model without brand × situation interaction, estimated from the other registry brands; the calibration checks it on synthetic data of that form only.{% if POSITIVE_FLAG %} `MC_Positive` was flagged (§3.1).{% endif %}{% if DEFUNCT_FLAG %} Defunct automotive brands appeared in situation answers above the pre-registered limit (§3.1).{% endif %}

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

Materials are deposited at OSF (osf.io/ec6wh), `methodology/v1_12/`: the locked pre-registration with its CEP sets, probe files, cost table, calibration and dry-run records, the scorer, coder and acquisition scripts with their tests, the lock manifest and the anchor record (`prereg/`, `anchor/`). At publication the deposit adds the raw answers with their usage records, the coded mention tables, the verdict file (`v112_verdicts.json`), the unit table (`v112_unit_table.csv`) and the figure sources. The code is also in the programme's GitHub repository (github.com/thirdsystem-aias/aias) at tag `{{PREREG_TAG}}`.

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

{{TABLE_DESC}}

Table: Coverage by cue type on panel {{PRIMARY}}: mean over the category's brands of the number of the cue type's two CEPs that at least two panel models cover (0--2).

{{TABLE_PERW}}

Table: Run-to-run reliability of the naming of brands (rel1: mean $\rho_w$ over the three run pairs of each brand's per-run share; rel3 $= 3\,\text{rel1}/(1 + 2\,\text{rel1})$) and recorded usage and spend per model, every billed attempt at list prices.

{{TABLE_RELCOST}}
