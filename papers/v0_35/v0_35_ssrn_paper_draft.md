---
title: "Two-Wave Temporal Stability of an AI Brand-Recall Consistency Quantity"
subtitle: "A Pre-Registered Longitudinal Re-Acquisition Across Five Product Categories (AIAS™ v0.35)"
date: "June 2026"
mainfont: "Carlito"
fontsize: 11pt
geometry: [letterpaper, margin=1in]
header-includes: |
  \usepackage{setspace}
  \usepackage{float}
  \usepackage{caption}
  \usepackage{titlesec}
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

{\LARGE \textbf{Two-Wave Temporal Stability of an AI Brand-Recall Consistency Quantity}}\\[8pt]

{\large A Pre-Registered Longitudinal Re-Acquisition Across Five Product Categories\\ (AIAS™ v0.35)}\\[28pt]

Pablo Ulpiano González Castro\\[4pt]
School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System™ (research entity; data archive and methodology venue)\\[8pt]
Correspondence: pablou@pablou.com · pablou.com\\
ORCID: 0009-0003-8968-9990\\[20pt]

Pre-registration: \texttt{v0.35-prereg-r1} (externally anchored before t\textsubscript{2} acquisition)\\
Data and code: OSF \texttt{ec6wh/v35}\\

\end{center}
\end{titlepage}

# Abstract {-}

Whether quantities derived from large language model (LLM) outputs are stable enough over time to function as brand-measurement instruments is an open empirical question. This study reports a pre-registered, two-wave longitudinal re-acquisition of the AIAS™ measurement protocol across five product-category panels (audiophile headphones, skincare, cosmetics, automotive, premium spirits; 112 brand units), re-running each panel's original acquisition pipeline verbatim 15--21 days after first measurement against a fixed six-model panel spanning three providers. Four hypotheses were pre-registered and externally anchored before re-acquisition. `H_CPC_Temporal_Stability` was CONFIRMED: per-brand rank order of the CV-based consistency quantity (CV-CPC) was stable in four of five categories (Spearman $\rho = 0.76$--$0.96$; the exception, the smallest panel, $\rho = 0.42$, n.s.). `H_CPC_Drift_Beyond_Presence` was MARGINAL by structural collapse: recognition saturation in four of five categories rendered Presence-residualization a no-op, leaving one informative category --- in which residualized stability ($\rho = 0.61$) exceeded raw stability ($\rho = 0.42$). `H_Presence_Temporal_Stability` was MARGINAL by ceiling: rank stability was high wherever rank variance existed ($\rho = 0.81$--$1.00$), but two categories were recognition-constant in both waves. Phantom status (below-recall-floor) persisted in 56 of 57 brands. The findings characterize CV-CPC's temporal behavior without validating it as a Consistency instrument, document pervasive recognition-ceiling effects in consumer categories, and motivate the mean-independent instrument requirement of the forthcoming v1.8 methodology revision.

**Keywords:** AI availability; brand availability; AIAS; large language models; temporal stability; test--retest reliability; consistency; CV-CPC; recognition saturation; pre-registration; Ehrenberg-Bass; brand recall

**JEL codes:** M31; L86, L15, D83, M37

**Paper status:** Pre-registered prospective two-wave re-acquisition (tag `v0.35-prereg-r1`, externally anchored before any t\textsubscript{2} call); 852 probes per wave; no deviations from pre-registration. Part of the AIAS measurement program.

# 1. Introduction

AI Availability --- the discoverability and representation of a brand in the outputs of large language models --- has been proposed as a third, measurable layer of brand availability (González Castro, 2026, SSRN 6659000), complementing the Mental and Physical Availability of the Ehrenberg-Bass tradition (Sharp, 2010; Romaniuk & Sharp, 2022). The AIAS™ (AI Availability Score) program operationalizes this layer as a multi-component construct measured under a versioned protocol. Presence --- the count of panel models that recognize a brand, denoted $C_P$ --- is the first component to have been measured and locked, under the v1.6 methodology revision (SSRN 6816340) and consolidated across the program's five-substrate empirical base (AIAS 1.0; SSRN 6817841). It is the validated reference point against which subsequent components are assessed.

Consistency is the program's second component, and its operational status is deliberately provisional. Its current operationalization, CV-CPC --- a coefficient-of-variation statistic over per-model recall, originating in the v0.30 instrument pilot (SSRN 6875319) --- was tested for dissociation from Presence in a dedicated methodology lock and falsified: pooled recall-coupling reached $|\rho| = 0.77$, well past the program's independence ceiling, and CV-CPC was on that basis *not adopted* as a validated Consistency instrument, with a mean-independent redefinition escalated to a future revision (v1.7; SSRN 6878818). Subsequent phases have characterized the quantity's behavior under perturbation --- across version snapshots (v0.32; SSRN 6898581) and across provider groupings (v0.33; SSRN 6909019) --- explicitly as inputs to the v1.8 instrument redesign rather than as steps toward validating CV-CPC as it stands.

This phase fills a specific gap in that characterization arc. Every prior treatment of CV-CPC has been either cross-sectional or re-analytic over a single frozen acquisition; none has addressed whether the quantity is *temporally stable* when registries, probe wording, and the model panel are all held fixed and the measurement is simply repeated. Temporal stability is a necessary condition for any future instrument built on the same measurement machinery: a quantity that does not reproduce across a short interval cannot anchor a managed brand metric, irrespective of its construct validity. The program's Presence-side precedent for this question is the v0.9 Re-Baseline, which established short-interval reproducibility for recognition; no equivalent test had been run for the recall-based consistency quantity.

This study contributes four results. First, it is the program's first two-wave re-acquisition: a full second collection of measurements against the same locked apparatus, with byte-checksummed probe fidelity and a pre-registration pushed and externally deposited before the second wave began. Second, it returns a CONFIRMED primary stability result for the per-brand rank order of CV-CPC. Third, it documents recognition-ceiling effects severe enough to structurally collapse two pre-registered tests --- the phase's most consequential finding, and direct empirical motivation for the v1.8 requirement of a recognition signal with room to vary. Fourth, it captures per-call provider-returned version identifiers absent at first measurement, establishing the baseline for a version-isolated third wave. Throughout, CV-CPC is treated strictly as a quantity whose temporal behavior is being characterized, not as a Consistency instrument under validation.

# 2. Method

## 2.1 Design

The study is a prospective two-wave longitudinal re-acquisition. The first wave ($t_1$) comprises the five original substrate acquisitions conducted in May 2026 (per-panel dates in §2.6); the second wave ($t_2$) is a single-day re-acquisition on 2026-06-10. Per-substrate intervals ($\Delta t$) range from 15 to 21 days and are recorded descriptively in the design table; no $\Delta t$-dependent hypothesis is posed, and interval heterogeneity is treated as a limitation rather than a predictor. Brand registries are bit-identical to the $t_1$ locks, with no new brand selection. Each substrate's original acquisition runner was executed verbatim, with exactly two permitted modifications --- redirection of the output directory and emission of a provenance sidecar --- and nothing else; probe text, frame ordering, and output schema were frozen. Each runner's probe set was verified by SHA-256 checksum against its $t_1$ lock immediately before execution. Each wave issues 852 probes (672 recognition; 180 recall) across the five panels.

## 2.2 Panel and version pinning

The panel comprises six models from three providers, two per provider. Models were pinned by their public alias, the same identifiers used at $t_1$. Pinning to dated model snapshots was infeasible: the $t_1$ acquisitions recorded aliases only, so the dated versions to which those aliases resolved in May 2026 are not recoverable. Consequently, any silent provider-side version change within the interval is, by design, a component of the measured (in)stability rather than a confound to be controlled out --- the study measures the stability a fixed-alias caller would observe. At $t_2$, the provider-returned dated identifier was captured for every call (Anthropic and OpenAI return dated snapshots; Google returns the alias), establishing the dated baseline for a future version-isolated wave. The minimum viable panel was pre-registered at four models, with pairwise exclusion and a deviations entry for any alias that failed to resolve; all six resolved at $t_2$, so no exclusion was applied. For the premium-spirits panel, recognition coding uses an LLM judge; that judge was pinned to the same alias used at $t_1$, and its 144 calls are recorded as coding, distinct from the 852-probe acquisition.

## 2.3 Measures

CV-CPC is defined per brand as $1/(1+\mathrm{CV})$ over the brand's per-model recall counts, where CV is the population coefficient of variation; a brand whose mean per-model recall falls below 1.0 is treated as undefined (below the recall floor). Presence is the integer recognition count $C_P \in \{0,\dots,6\}$ per the v1.6 lock. For the premium-spirits substrate, the recognition level is normalized to binary identically in both waves. All paired statistics use pairwise definedness: a brand enters a category's test only if the relevant quantity is defined in both waves, and the count of brands excluded for either-wave undefinedness is reported per category.

## 2.4 Hypotheses and decision criteria

Four hypotheses were locked verbatim in the pre-registration. `H_CPC_Temporal_Stability` (primary): per-category Spearman $\rho$ between per-brand CV-CPC at $t_1$ and $t_2$; CONFIRMED at $\rho \ge 0.70$ in at least four of five categories, FALSIFIED at $\rho < 0.50$ in at least three, otherwise MARGINAL. `H_CPC_Drift_Beyond_Presence` (primary, gating): (a) the per-category Spearman $\rho$ between $\Delta$CV-CPC and $\Delta C_P$ across brands, and (b) the stability of CV-CPC residualized on $C_P$ within each wave; CONFIRMED at residualized $\rho \ge 0.50$ in at least three categories, with the directional pre-commitment leaning FALSIFIED-or-marginal given the established Presence-coupling. A single saturation trigger was pre-registered: where all six models recognize at least 90% of a category's defined brands, $C_P$ is effectively constant, residualization is a no-op, and that category's gate contribution is down-weighted to MARGINAL. `H_Presence_Temporal_Stability` (secondary): per-category Spearman $\rho$ between $C_P$ at $t_1$ and $t_2$; CONFIRMED at $\rho \ge 0.80$ in at least four of five, FALSIFIED at $\rho < 0.60$ in at least three. The higher bar reflects Presence's status as the validated component and the v0.9 Re-Baseline precedent. `H_Phantom_Temporal_Persistence` (tertiary, exploratory): the proportion of $t_1$ below-recall-floor brands retaining that status at $t_2$, reported descriptively with no confirmation threshold. The gate's confirmatory verdict space is deliberately binary: absent saturation, the $\ge 0.50$-in-$\ge 3/5$ confirmed and falsified partitions are mutually exhaustive over the five-category outcome.

## 2.5 Inference

Null distributions for the rank statistics were generated by Monte Carlo permutation of the second-wave labels, at least 10,000 draws per category, one-sided, under a fixed seed. Per-category observed $\rho$, the permutation mean and upper quantile, and the one-sided $p$-value are reported; verdicts follow the locked category-count thresholds rather than any pooled test.

## 2.6 Pre-registration and computational integrity

The pre-registration was locked at annotated tag `v0.35-prereg-r1`, pushed to the version-control remote and deposited to OSF before the first $t_2$ acquisition call --- the program's first externally anchored pre-registration, establishing the timestamp chain ahead of data collection. Two $t_1$-side parity gates were required to pass before any acquisition: for the three raw-text categories, recomputed per-model recall vectors had to reproduce the v1.7 methodology lock's stored per-model column bit-for-bit (72 brand units, aligned by model name); for the remaining two categories, recomputation had to reproduce the frozen per-model inputs as consumed by the program's extraction pipeline. Both gates passed before $t_2$ began.

# 3. Results

Both $t_1$-side parity gates passed before acquisition (§2.6), and all six model aliases resolved at $t_2$, so the full six-model panel and all five categories entered analysis. Per-category defined-brand counts in each wave, the measurement interval, and the paired sample available to each rank statistic are reported in Table 1. Paired samples range from 8 to 14 brands; the recall floor removes roughly half of each registry in both waves, as expected for the recall-based quantity.

Table: Per-category design summary. Defined = CV-CPC defined (mean per-model recall $\ge 1.0$); paired $n$ = brands defined in both waves (the Spearman sample).

| Category | $\Delta t$ (days) | Defined $t_1$ | Defined $t_2$ | Paired $n$ |
|------------------|:--:|:--:|:--:|:--:|
| audiophile headphones | 21 | 8 | 8 | 8 |
| skincare | 20 | 10 | 9 | 9 |
| cosmetics | 19 | 14 | 14 | 13 |
| automotive | 16 | 14 | 14 | 14 |
| premium spirits | 15 | 9 | 9 | 9 |

## 3.1 Temporal stability of CV-CPC (`H_CPC_Temporal_Stability`)

Per-category Spearman $\rho$ between waves was: audiophile headphones $\rho = 0.419$ (MC $p = 0.152$, $n = 8$), skincare $\rho = 0.783$ ($p = 0.0087$, $n = 9$), cosmetics $\rho = 0.890$ ($p = 0.0002$, $n = 13$), automotive $\rho = 0.960$ ($p = 0.0001$, $n = 14$), and premium spirits $\rho = 0.762$ ($p = 0.0102$, $n = 9$). Four of five categories meet the pre-registered $0.70$ criterion, and the verdict is **CONFIRMED**. The exception is the smallest panel and the smallest paired sample, where $\rho = 0.419$ falls below both the confirmation and the falsification threshold and the permutation test is non-significant.

![Per-brand CV-CPC at $t_1$ versus $t_2$ by category, identity diagonal dashed; per-category Spearman $\rho$, permutation $p$, and paired $n$ annotated. Four categories meet the pre-registered $0.70$ criterion; audiophile headphones ($\rho = 0.42$, n.s., $n = 8$) is the single miss.](../../reports/figs/v35/chart_01_cpc_t1_t2_stability.pdf){#fig:cpc width=100%}

## 3.2 The Beyond-Presence gate (`H_CPC_Drift_Beyond_Presence`)

The pre-registered saturation trigger fired in four of five categories: in skincare, cosmetics, automotive, and premium spirits, all six models recognized at least 90% of defined brands in both waves, rendering $C_P$ effectively constant, residualization a no-op (residualized $\rho$ identical to raw $\rho$ in all four: $0.783$, $0.890$, $0.960$, $0.762$), and the drift-coupling statistic undefined ($\Delta C_P \equiv 0$). Those categories' gate contributions are down-weighted to MARGINAL under the locked rule, leaving one informative category. In audiophile headphones --- the only category with recognition variance --- residualized stability ($\rho = 0.611$) exceeded raw stability ($\rho = 0.419$), with drift-coupling $\rho(\Delta\text{CV-CPC}, \Delta C_P) = 0.190$. With the $\ge 3/5$ confirmation count unreachable, the verdict is **MARGINAL** by structural collapse. The single informative category is suggestive --- once Presence variation is removed, the residual quantity is *more* stable, the direction a genuine Consistency-specific signal would produce --- but one category cannot carry a confirmatory claim.

![Raw versus Presence-residualized CV-CPC stability by category, $0.50$ gate criterion marked. In the four recognition-saturated categories residualization is a no-op (residual $\equiv$ raw; $\Delta C_P \equiv 0$). Audiophile headphones is the lone informative category: residual $\rho = 0.61 >$ raw $\rho = 0.42$, drift-coupling $\rho = 0.19$.](../../reports/figs/v35/chart_02_residual_gate_saturation.pdf){#fig:gate width=100%}

## 3.3 Temporal stability of Presence (`H_Presence_Temporal_Stability`)

Where $C_P$ carried rank variance, stability was high: audiophile headphones $\rho = 0.815$ ($p = 0.0006$), skincare $\rho = 0.986$ ($p = 0.0001$), and automotive $\rho = 1.00$ ($p = 0.042$, reflecting limited effective rank variance). In cosmetics and premium spirits, $C_P$ was constant at $6/6$ for every brand in both waves; Spearman $\rho$ is undefined, and the pre-registered $\ge 4/5$ confirmation count is unreachable. The verdict is **MARGINAL** by ceiling. The labeled descriptive supplement records that the constant was identical across waves --- exact-match proportion $1.00$ in both degenerate categories --- so the substantive reading is perfect persistence at the recognition ceiling that the rank statistic cannot register.

![Per-brand $C_P$ ($0$--$6$) at $t_1$ versus $t_2$. Three categories carry rank variance ($\rho = 0.81$--$1.00$, all above the $0.80$ criterion); cosmetics and premium spirits are constant at the $6/6$ recognition ceiling in both waves --- rank-degenerate, reported via the exact-match supplement rather than a fabricated correlation.](../../reports/figs/v35/chart_03_presence_stability.pdf){#fig:presence width=100%}

## 3.4 Phantom persistence (`H_Phantom_Temporal_Persistence`, exploratory)

Below-recall-floor status at $t_1$ persisted at $t_2$ in $8/8$, $14/14$, $9/10$, $10/10$, and $15/15$ brands for the five categories respectively; pooled, $56$ of $57$ ($0.982$). The single transition was one cosmetics brand crossing the floor. The result is reported descriptively, per pre-registration, with no confirmation threshold.

![Retention of below-recall-floor (phantom) status from $t_1$ to $t_2$, per category and pooled. Descriptive; no confirmation threshold. Pooled retention $56/57 = 0.98$; the single mover is in cosmetics.](../../reports/figs/v35/chart_04_phantom_persistence.pdf){#fig:phantom width=100%}

# 4. Discussion

The headline result is that the per-brand rank order of CV-CPC reproduces across a 15--21-day interval under fixed registries and fixed wording. "Stability" here means precisely the stability a fixed-alias caller observes, silent provider-side version changes included: the alias-pinning design folds any in-window version drift into the measured quantity rather than controlling it out. That the standings held through whatever updates shipped within the window strengthens rather than weakens the managerial relevance of the result, and it sits consistently beside the prior finding that CV-CPC fragility concentrates at *major* version transitions rather than within short alias windows (v0.32; SSRN 6898581).

The single miss is interpretable. Audiophile headphones combines the smallest registry, the lowest defined rate (paired $n = 8$), and --- not coincidentally --- the only recognition variance in the study. Where Presence varies, raw CV-CPC inherits Presence noise; the same category's residualized stability rising to $0.611$ is exactly the pattern the established $|\rho| = 0.77$ Presence-coupling (v1.7; SSRN 6878818) predicts. The miss is thus more naturally read as coupling-induced instability than as evidence against a stable underlying consistency signal --- an interpretation the present design can suggest but, with one informative category, cannot confirm.

The saturation finding is the study's most consequential contribution. Four of five consumer categories sit at a recognition ceiling severe enough to structurally collapse both the Beyond-Presence gate and the Presence rank-test. This extends the saturation collapse first observed in a single re-analysis (v0.33; SSRN 6909019) to a pervasive property of established consumer-brand panels, and it converts the forthcoming methodology requirements from desiderata into demonstrated necessities: a mean-independent consistency instrument *and* a graded recognition signal with room to vary are both prerequisites for any beyond-Presence claim in this regime, not refinements of it.

Finally, phantom persistence of $56/57$ indicates that below-recall-floor status is a structural property of the brand--model--corpus relationship rather than sampling noise. This is consistent with the Phantom Brand Persistence construct established under the v1.6 lock (SSRN 6816340), and it is the program's strongest evidence to date that AI invisibility is a standing condition rather than a transient state.

# 5. Limitations

Several boundaries frame these findings. The interval is 15--21 days, so quarter-scale or annual stability is untested. Alias-level pinning means that $t_1 \rightarrow t_2$ version drift is unobservable within this design; the limitation is remedied prospectively by the $t_2$ provenance capture rather than retrospectively. Paired samples are small (8--14 brands per category), bounding per-category Spearman precision, and the primary verdict is a category-count rule that a single category could flip. CV-CPC remains a non-adopted, Presence-coupled quantity; this study characterizes its temporal behavior and revises nothing about its validity status. Recognition saturation prevents a clean beyond-Presence test in four of five categories, so the gate's MARGINAL verdict reflects an instrument limit rather than an answered question. And premium-spirits recognition coding depends on an LLM judge --- pinned to the $t_1$ alias, with returned versions recorded --- so judge-model dependence is a coding-layer assumption the design carries forward.

# 6. Future Research

Three threads follow directly. First, a version-isolated third wave is now possible against the $t_2$ dated-identifier baseline, separating "the model changed" from "the answers drifted" --- the question alias pinning cannot resolve. Second, the v1.8 instrument redesign --- a mean-independent consistency measure paired with a graded recognition signal --- is now empirically motivated rather than merely proposed, the recognition-ceiling effects documented here standing as its demonstrated requirement. Third, longer-horizon and intervention designs become tractable: if below-floor status persists passively, the open managerial question is which interventions move a brand across the recall floor and on what lag, a question the stable baseline established here makes answerable.

# Declarations {-}

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-acquires measurements against brand registries fixed in earlier phases (v0.19--v0.23); it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward unchanged. Two items of record apply. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands --- Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) --- characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry, AKG was substituted with Denon before the v0.19 pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary. Acquisition, coding, and scoring are fully automated against the locked registries; the pre-registration was tagged and externally deposited before any second-wave call; and the author's affiliation played no role in registry construction, acquisition, scoring, or the resulting verdicts. Samsung Electronics had no role in the design, conduct, analysis, or reporting of this work.

## Funding {-}

Self-funded. No external funding supported this research.

## Ethics {-}

Not applicable; no human subjects. The study queries large language models under their public interfaces.

## Data and code availability {-}

All materials are deposited at OSF, `ec6wh/v35`: the locked pre-registration (`v0.35-prereg-r1`, externally deposited before acquisition), both waves' acquisition outputs and the provenance sidecar, the acquisition manifest with per-substrate probe-set SHA-256 checksums, the scorer (`score_v35.py`), the verdicts (`v35_verdicts.json`), and the figure sources.

# References {-}

González Castro, P. U. (2026). *AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval*. SSRN 6659000.

González Castro, P. U. (2026). *The AIAS™ Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy* (v1.2). SSRN 6761698.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification* (v1.3). SSRN 6797679.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol v1.4: Recognition × Recall Decomposition and Multi-Component AI Availability*. SSRN 6799479.

González Castro, P. U. (2026). *The AIAS™ Presence Measurement Protocol: Multi-Statistic C2 Specification and Two-Channel Recall Decomposition* (v1.5). SSRN 6810758.

González Castro, P. U. (2026). *Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension* (AIAS Methodology v1.6). SSRN 6816340.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol: CPC Consistency --- A Pre-Registered Negative Result* (v1.7). SSRN 6878818.

González Castro, P. U. (2026). *AI Availability as a Third Measurable Layer of Brand Availability: Five-Substrate Empirical Anchoring of the AIAS™ Presence Measurement Protocol* (AIAS 1.0). SSRN 6817841.

González Castro, P. U. (2026). *Recognition Saturates, Consistency Doesn't --- An Instrument-Specification Pilot of the AIAS™ Consistency Component (CPC) across Skincare, Cosmetics, and Automotive* (v0.30). SSRN 6875319.

González Castro, P. U. (2026). *CPC Version-Snapshot Stability: A Two-Arm Cross-Generation Test* (v0.32). SSRN 6898581.

González Castro, P. U. (2026). *Provider-Asymmetric CPC: A Pre-Registered Re-Analysis* (v0.33). SSRN 6909019.

González Castro, P. U. (2026). *AI Presence in Audiophile headphones: AIAS v0.19*. SSRN 6809182.

González Castro, P. U. (2026). *AI Presence in Skincare: AIAS v0.20*. SSRN 6811441.

González Castro, P. U. (2026). *AI Presence in Cosmetics: AIAS v0.21*. SSRN 6815378.

González Castro, P. U. (2026). *AIAS™ v0.22 --- Automotive Substrate: Phantom Brand Persistence on a Heritage-Saturated Category*. SSRN 6829118.

González Castro, P. U. (2026). *AIAS™ v0.23 --- Premium Spirits Substrate*. SSRN 6834298.

Romaniuk, J., & Sharp, B. (2022). *How Brands Grow, Part 2* (Revised ed.). Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.
