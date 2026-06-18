---
title: "A Mean-Independent Consistency Instrument for Cross-Model AI Presence"
subtitle: "Redesigning CPC on a Quasi-Binomial Dispersion Basis"
fontsize: 11pt
mainfont: "Carlito"
keywords: "AI Availability; AIAS; brand measurement; large language models; overdispersion; consistency; mean-independence; pre-registration; cross-model presence"
jel: "M31; L86; L15; D83; M37"
linkcolor: black
urlcolor: black
geometry:
  - letterpaper
  - margin=1in
header-includes:
  - \usepackage{setspace}
  - \usepackage{float}
  - \usepackage{caption}
  - \usepackage{titlesec}
  - \setstretch{1.36}
  - \setlength{\parskip}{8pt}
  - \setlength{\parindent}{0pt}
  - \renewcommand{\maketitle}{}
  - \providecommand{\xmpquote}[1]{#1}
---

\begin{titlepage}
\setstretch{1.0}
\setlength{\parskip}{0pt}
\begin{center}

\vspace*{2em}

{\LARGE\bfseries A Mean-Independent Consistency Instrument\\ for Cross-Model AI Presence}

\vspace{0.8em}

{\large Redesigning CPC on a Quasi-Binomial Dispersion Basis}

\vspace{2.5em}

Pablo Ulpiano González Castro

\vspace{0.6em}

School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System\texttrademark{} (independent research entity; data archive and methodology venue)

\vspace{1em}

Correspondence: pablou@pablou.com \textperiodcentered{} pablou.com\\
ORCID: 0009-0003-8968-9990

\vspace{2.5em}

\textit{AIAS\texttrademark{} Measurement Program \textperiodcentered{} Working Paper}\\
Methodology locked at \texttt{v1.8-prereg-r4}\\
Results locked at \texttt{v1.8-results-r1} (commit \texttt{85d2202})

\vspace{1.5em}

2026

\end{center}
\end{titlepage}

# Abstract {-}

Cross-model Presence Consistency (CPC) — the stability of a brand's surfacing across a reference panel of large language models — is the Consistency component of the AI Availability Score (AIAS™), a proposed third brand-growth system alongside mental and physical availability. A prior coefficient-of-variation operationalization (CV-CPC) was falsified as a consistency instrument: because the coefficient of variation of a low-rate count couples to its mean ($\mathrm{CV} \approx 1/\sqrt{\mathrm{mean}}$), CV-CPC reparametrized recall level rather than measuring consistency (pooled $|\rho(\text{CV-CPC}, \mu)| = 0.77$). We redesign CPC on a mean-independent basis as $\varphi$, the between-model quasi-binomial dispersion (Pearson $\chi^2/\mathrm{df}$), which divides out the binomial-expected variance and is therefore defined into the low-recall segment where the corrected CV is not. In a pre-registered re-analysis of a frozen five-substrate, six-model omnibus (112 brand-units) under three validation framings, $\varphi$ achieves mean-independence (pooled $|\rho(\varphi, \mu)| = 0.091$) where CV-CPC reproduces its coupling (0.682); $\varphi$ extends defined coverage to 29 low-recall brands the corrected CV cannot reach; and $\varphi$ dissociates from a positional set-stability diagnostic ($J$; $\rho = -0.403$), confirming the two capture distinct facets. $\varphi$ reproduces across measurement waves ($\rho = 0.645$). The result is a validated, mean-independent Consistency instrument that supersedes CV-CPC and advances the AIAS measurement program toward multi-instrument composition.

**Keywords:** AI Availability; AIAS; brand measurement; large language models; overdispersion; consistency; mean-independence; pre-registration; cross-model presence

**JEL codes:** M31 (primary); L86; L15; D83; M37

**Paper status:** Working paper in the AIAS\texttrademark{} Measurement Program. Pre-registered; methodology locked at git tag `v1.8-prereg-r4`, results locked at `v1.8-results-r1` (commit `85d2202`). Pre-registration, scorer, verdicts, instrument table, and materialization manifest deposited at OSF (`osf.io/ec6wh/methodology/v1_8`).

# 1. Introduction

Brand growth research has long organized demand-side brand equity around two systems: mental availability — the propensity of a brand to be noticed or thought of in buying situations — and physical availability, the ease with which it can be found and bought (Romaniuk & Sharp, 2022). For an environment in which large language models increasingly mediate discovery, a third such system has been proposed — AI availability, the propensity of a brand to be surfaced by AI systems when buyers delegate consideration to them — operationalized through the AI Availability Score (AIAS™; SSRN 6817841). Within that program, Cross-model Presence Consistency (CPC) is the Consistency component: the degree to which a brand's surfacing is stable across a fixed reference panel of models rather than idiosyncratic to any one of them.

A consistency instrument must measure agreement among models, not the overall rate at which a brand is surfaced. A prior operationalization of CPC built on the coefficient of variation of per-model surfacing counts (CV-CPC) fails this requirement and was falsified as a pre-registered negative result (SSRN 6878818). The failure is structural: for a low-rate count the coefficient of variation couples mechanically to its mean — for a Poisson count, $\mathrm{CV} \approx 1/\sqrt{\mathrm{mean}}$ — so CV-CPC does not isolate cross-model agreement but re-expresses recall level. Across a frozen evaluation base the coupling was strong and direct, pooled $|\rho(\text{CV-CPC}, \mu)| = 0.77$, well above the 0.50 ceiling at which an instrument can be said to dissociate from the mean; three subsequent phases confirmed that the instrument, not the phenomenon, was the binding constraint (SSRN 6909019; 6915458).

The corrective requirement is therefore precise and falsifiable: a redesigned CPC must be mean-independent — its values must not track recall level — while remaining defined across the brands of interest, including the low-recall segment where most candidate brands sit. We fix this in advance as a make-or-break criterion: the redesigned instrument is retained only if its correlation with the mean falls at or below the same 0.50 ceiling that CV-CPC exceeded.

We redesign CPC as $\varphi$, the between-model quasi-binomial dispersion of per-model surfacing counts (a Pearson $\chi^2/\mathrm{df}$ dispersion statistic). $\varphi$ measures how far the panel's models disagree relative to the agreement expected under a shared surfacing rate, and by dividing out the binomial-expected variance $F\,\hat{\pi}(1-\hat{\pi})$ it removes the level coupling by construction rather than by post-hoc correction. The same construction extends $\varphi$ into the low-recall segment where the mean-corrected CV is undefined: a brand surfacing only once across the panel still yields a finite dispersion. Two further instruments accompany $\varphi$ — a positional set-stability diagnostic, $J$ (the mean pairwise Jaccard of the frames in which a brand surfaces), which reads where a brand surfaces rather than how consistently in magnitude; and a graded-recognition measure, $R_{\text{grad}}$, carried here as a forward specification because the frozen recognition channel is binary by probe design.

We validate the redesign by pre-registered re-analysis of a frozen omnibus rather than by new acquisition, so that the test isolates the instrument from the data-generating process. The base is a five-substrate, six-model panel of 112 brand-units, read under three framings — a two-wave reproducibility set, a phantom-roster partition, and a low-recall stratum — that together stress mean-independence, coverage, and positional dissociation. The instrument definitions, validation plan, hypotheses, and falsification criteria were locked at a version-controlled commit and externally anchored before any score was computed; the first scoring call is the one-way boundary the anchor precedes. Because the omnibus spans substrates of heterogeneous channel structure — including a single-channel substrate and one whose channels are not the canonical category/cultural pair — the primary instruments are computed channel-agnostically, with a per-channel variant retained as a non-gating secondary diagnostic on the canonical two-channel substrates.

The contribution is a validated, mean-independent Consistency instrument. $\varphi$ achieves mean-independence (pooled $|\rho(\varphi, \mu)| = 0.091$) where CV-CPC reproduces its coupling on the same base (0.682); it extends defined coverage to the low-recall brands the corrected CV cannot reach; it dissociates from the positional facet $J$; and it reproduces across measurement waves. Section 2 specifies the instruments, Section 3 the validation design, and Section 4 the results; Section 5 states the limitations and the path to multi-instrument composition — the next step in assembling AIAS from its components.

# 2. Instrument specifications

## 2.1 Notation

For a brand *b* and the fixed six-model reference panel $m \in \{1, \ldots, M\}$, $M = 6$, each model is probed under $F = 6$ frames (three category frames and three cultural frames), pooled channel-agnostically for the primary instruments. Surfacing is binary per (model, frame). The per-model count $k(b, m) \in \{0, \ldots, F\}$ is the number of frames in which model *m* surfaces *b*, and the pooled surfacing rate is $\hat{\pi}_b = (\sum_m k(b, m)) / (M\cdot F)$, with $M\cdot F = 36$. The recall mean $\mu_b$ is monotone in $\hat{\pi}_b$, and the mean-independence criterion is stated as the Spearman rank correlation $\rho(\cdot, \mu)$ against $\hat{\pi}_b$.

## 2.2 φ — the primary instrument

$\varphi$ is the between-model quasi-binomial dispersion of the per-model counts: the observed cross-model variance relative to the variance expected if every model surfaced *b* at the shared rate $\hat{\pi}_b$. It is a Pearson $\chi^2/\mathrm{df}$ dispersion statistic,

$$\varphi_b = \frac{1}{M-1}\sum_{m}\frac{\bigl(k(b,m) - F\hat{\pi}_b\bigr)^2}{F\hat{\pi}_b\,(1-\hat{\pi}_b)},$$

with $\mathrm{df} = M - 1$ and null expectation $E[\varphi] = 1$ under homogeneity (all models drawing from the common rate). $\varphi > 1$ indicates the models disagree more than chance — inconsistent surfacing — and $\varphi < 1$ that they agree beyond chance.

The denominator $F\cdot\hat{\pi}_b(1 - \hat{\pi}_b)$ is the binomial-expected variance of a per-model count, so dividing by it removes the dependence on level by construction: where the coefficient of variation of a low-rate count carries $1/\sqrt{\mathrm{mean}}$, $\varphi$ carries no such term. This is the property the redesign requires, and it is structural rather than a fitted correction.

$\varphi$ is defined for $\hat{\pi}_b \in (0, 1)$ — at least one surfacing, short of full saturation. Two boundary cases are undefined and partitioned out before analysis, as a pre-specified rule rather than a finding: the true-zero floor ($\hat{\pi}_b = 0$) and the saturation ceiling ($\hat{\pi}_b = 1$), at which the dispersion is $0/0$. Within the defined domain, coverage reaches the low-recall segment that defeats the mean-corrected CV: a brand surfacing once across the entire panel ($\hat{\pi}_b = 1/36$) still yields a finite $\varphi$.

## 2.3 J — positional diagnostic

$\varphi$ reads the magnitude of cross-model agreement but not its position — whether the models that surface *b* do so in the same frames. $J$ captures that facet as the mean pairwise Jaccard overlap of the frame sets. Writing $S(b, m)$ for the set of frames in which model *m* surfaces *b*,

$$J_b = \operatorname*{mean}_{(m,m')}\frac{\lvert S(b,m)\cap S(b,m')\rvert}{\lvert S(b,m)\cup S(b,m')\rvert},$$

over model pairs with non-empty union. $J \in [0, 1]$: $J = 1$ when every model surfaces *b* in identical frames (positional consistency) and $J \to 0$ for disjoint frame sets; it is defined for a brand surfacing at least once across at least two models. A pre-registered contingency, fixed in advance, guards against small-set bias: should $|\rho(J, \mu)|$ exceed 0.50, $J$ is replaced by its chance-corrected form $J_{\text{adj}} = (J - E[J \mid \text{sizes}]) / (1 - E[J \mid \text{sizes}])$.

## 2.4 R_grad — forward specification

A graded-recognition measure $R_{\text{grad}}$ is specified as part of the instrument family but is not scored here. The frozen recognition channel is binary by probe design; no graded tiers are recoverable from it, and an audit of the base confirms the recognition saturation is genuine rather than a binarization artifact. $R_{\text{grad}}$ is therefore carried forward to a phase with a re-scorable recognition probe.

## 2.5 CV-CPC baseline

Two coefficient-of-variation forms serve as baselines. The raw form $\text{CPC}_{\text{raw}} = \mathrm{SD}(k)/\mu$ is the v1.7 instrument; it carries a recall floor (defined for $\mu$ at or above a fixed MU_FLOOR) and supplies the reproduction test — whether the mean coupling that falsified it recurs on the present base. The mean-corrected form $\text{CPC}_{\text{corr}} = \mathrm{SD}(k)/\sqrt{\hat{\pi}(1 - \hat{\pi})}$ shares $\varphi$'s defined domain $(0, 1)$ and serves as the same-domain reference: $\varphi$ is defined strictly beyond $\text{CPC}_{\text{raw}}$'s floor, covering the sub-floor low-recall band, while $\text{CPC}_{\text{corr}}$ — defined on the same interval as $\varphi$ — isolates that the gain is a property of the floor, not of the domain.

## 2.6 Per-channel secondary

A per-channel variant of $\varphi$ and $J$ — computed within each channel, $F = 3$ frames per channel — is retained as a non-gating secondary diagnostic. Because $\varphi$ is already mean-independent by construction, the level confound that would motivate separating channels is removed and the residual channel signal is positional ($J$'s domain); the variant therefore only reports category/cultural asymmetry where the channels are genuinely canonical. Its substrate scope is specified in §3.

# 3. Validation design

## 3.1 The frozen omnibus

The instrument is validated against a frozen base rather than newly acquired data, so the test discriminates the instrument from the data-generating process: the same surfacing records the falsified CV-CPC was computed on are re-scored under the redesign. The base is a five-substrate omnibus (v0.19–v0.23) spanning headphones, skincare, cosmetics, automotive, and premium spirits, each probed against the same six-model panel — two models from each of three providers — for 112 brand-units in total. No probes are re-issued; the records are fixed at their deposited state.

## 3.2 Three validation framings

The omnibus is read under three framings, each stressing a distinct property. The two-wave reproducibility framing (v0.34) reads the full omnibus at two measurement waves, $t_1$ and $t_2$, supporting both a per-wave mean-independence test and a wave-to-wave stability check of $\varphi$. The phantom-roster framing (v0.35) partitions the base into an 84-unit analyzable set — the brand-units surfacing at least once — against which a near-phantom subset is contrasted; the 28 units no model surfaces are partitioned out as true-zeros. The low-recall framing (v0.36) isolates the stratum on which $\varphi$'s coverage advantage is defined: the units for which $\varphi$ is defined but the floor-bearing CV is not.

These framings are not statistically independent, and the paper treats them accordingly. Because $\varphi$ is undefined at the true-zero floor, its defined set under the full omnibus (v0.34) coincides with the 84-unit analyzable set of the phantom framing (v0.35) — the 28 units undefined under the former are precisely the phantom-excluded true-zeros of the latter — so the two framings yield one shared mean-independence estimate rather than two. The load-bearing evidence is therefore the per-framing correlations together with the two-wave stability, with the pooled correlation reported as a cross-framing summary, not an independent-observation count.

## 3.3 Surfacing extraction

Binary surfacing is derived from the frozen response records, not read from a pre-deposited table, through the certified extraction lineage of the source phases: a pre-scored mention field for the single-channel substrate, a certified string matcher over response text for the canonical two-channel substrates, and a certified judge-scored field for the remaining substrate. The three provenances are reconciled to commensurable per-model counts through the established reconciliation gate, which reproduces the v1.7 reference exactly on the substrates that admit it. Because the provenance is uniform within each substrate and $\varphi$ is a between-model statistic computed within a substrate, the heterogeneity does not confound the dispersion; it is recorded among the limitations (§5).

## 3.4 Channel scope

The primary instruments are computed channel-agnostically — the six frames per model pooled to a single 0–6 count — because the omnibus admits no uniform per-channel decomposition. One substrate is single-channel and has no category/cultural split at all; another carries two channels that are not the canonical category/cultural pair, and mapping them onto it would invoke a channel-construct equivalence deferred elsewhere as unvalidated. Two of the five substrates therefore break a per-channel framing, making channel-agnostic computation a necessity, not a convenience. A per-channel variant of $\varphi$ and $J$ is retained as a non-gating secondary diagnostic on the three canonical two-channel substrates alone, reporting category/cultural asymmetry where the channels are genuinely canonical and gating no verdict.

## 3.5 Hypotheses and falsification criteria

The validation fixes six hypotheses with thresholds set in advance. The make-or-break hypothesis, H_MeanIndependent, requires $|\rho(\varphi, \mu)| \le 0.50$ pooled across framings — the ceiling CV-CPC exceeded; should it fail, the pre-registered escalation is a beta-binomial intraclass-correlation re-estimation, flagged but not run automatically. The baseline hypothesis, H_CV_Reproduces, requires the CV mean-coupling to recur ($|\rho(\text{CV-CPC}_{\text{raw}}, \mu)| \ge 0.50$), confirming the base carries the coupling $\varphi$ must dissociate from. H_LowRecallDefined requires $\varphi$ to be defined for every surfacing unit, to contain the CV-defined set strictly, and to place the coverage gain in the low-recall stratum. H_PositionalDissociation requires $\varphi$ and $J$ to capture distinct facets ($|\rho(\varphi, J)| \le 0.70$, with at least one identified discordant unit). H_GradedRecognition is carried as a forward specification; H_PhantomSignature is exploratory, with no directional commitment.

H_LowRecallDefined is adjudicated against a four-cell verdict matrix, complete over the outcomes reachable from the instrument's structure. Because $\varphi$ is total on the open interval $(0, 1)$, the only surfacing unit that can lack a $\varphi$ is one at the saturation ceiling, which the floor-bearing CV still defines; when the coverage gain holds but such a ceiling unit exists, the two defined sets are non-nested and strict containment breaks. The matrix resolves CONFIRMED (gain present, full coverage, strict containment), FALSIFIED (no gain), and PARTIAL-STRUCTURAL (gain present, containment broken solely by the by-design ceiling) as the reachable outcomes, and retains a fourth cell, PARTIAL-IMPLEMENTATION, as a fail-loud guard for a residual undefined unit of any non-ceiling cause — a state the instrument's totality renders structurally impossible, so that its occurrence would signal an extraction defect rather than a legitimate partial.

## 3.6 Pre-registration discipline

The instrument definitions, framings, hypotheses, thresholds, and verdict matrix were locked at a version-controlled commit and externally anchored — a remote tag and an open archival deposit — before any score was computed, in keeping with the program's standing pre-registration protocol (SSRN 6761698; 6797679; 6799479; 6810758). Absent an acquisition step, the first scoring call is the one-way boundary the anchor precedes; no $\varphi$, $J$, or CV value was computed before the lock was anchored. Three pre-scoring amendments refined the lock — a frame-count correction, the channel-agnostic primary decision, and the structural verdict cell of §3.5 — each additive, each recorded in a contemporaneous deviations log, and each made before the boundary with no data inspected. The verdict matrix's completeness was checked exhaustively as an institutional rule.

# 4. Results

Stage-0 integrity held before any instrument was read: the reconciliation gate passed with no mismatches on the substrates that admit a v1.7 reference, and the frame-to-count consistency check held across all five substrates, confirming that the per-frame surfacing used for $J$ sums to the reconciled per-model count used for $\varphi$. Of the 112 brand-units, 84 are $\varphi$-defined, 28 are true-zeros partitioned out at the floor, and none sit at the saturation ceiling.

## 4.1 Mean-independence (make-or-break)

$\varphi$ is mean-independent. The pooled rank correlation between $\varphi$ and the recall mean is $|\rho(\varphi, \mu)| = 0.091$ — far inside the 0.50 ceiling, and roughly a seventh of the 0.682 the coefficient of variation reproduces on the same base (§4.5). The result holds in every framing: $-0.082$ on the shared analyzable set (v0.34 and v0.35, which coincide as one estimate of 84 units) and $+0.107$ on the low-recall stratum (v0.36, 29 units). The pre-registered escalation to a beta-binomial intraclass-correlation re-estimation was therefore not entered; H_MeanIndependent is CONFIRMED. $\varphi$ measures cross-model agreement without re-expressing recall level — the property CV-CPC structurally could not provide.

![$\varphi$ against the recall mean (left) and CV-CPC against the same mean (right) on the shared brand set: $|\rho(\varphi,\mu)| = 0.091$ versus $0.682$. Dividing by the binomial-expected variance removes the level coupling that dividing by the mean retains.](../../reports/figs/v1_8/chart_01_mean_independence.pdf){#fig:meanindep width=100%}

## 4.2 The dissociation is not a coverage artifact (supplementary)

$\varphi$ is defined on a broader set (84 units) than the floor-bearing CV (55), so the headline contrast spans different domains. As a supplementary check — computed post-registration from the locked instrument table, not a pre-registered test — $\varphi$'s mean-correlation restricted to the identical 55-unit CV-defined set is $\rho = +0.02$ ($n = 55$, $p = 0.86$): statistically null, and against $\text{CV-CPC}_{\text{raw}}$'s 0.682 on those very same 55 units, smaller by more than an order of magnitude. $\varphi$'s mean-independence is therefore a property of the instrument rather than an artifact of admitting the extra 29 low-recall units — it is null on the restricted 55-unit set and on the shared 84-unit set alike.

## 4.3 Low-recall coverage

$\varphi$ extends defined coverage into the segment the floor-bearing CV cannot reach. Among the 84 surfacing units $\varphi$ is defined for all of them, and its defined set strictly contains the 55-unit CV-defined set; the 29-unit gain is exactly the sub-floor low-recall band, every gain unit carrying a pooled rate at or below 0.139 — fewer than one surfacing per model on average. The mean-corrected CV, which shares $\varphi$'s domain, is defined for the same 84 units, confirming the gain is a property of the floor rather than of the domain. No unit sits at the saturation ceiling, so strict containment holds cleanly and H_LowRecallDefined resolves to its confirmed cell. The structural cell reserved for a containment break at the ceiling was pre-specified for completeness but is not realized by this base; the matrix was exhaustive ex ante regardless.

![Defined coverage of $\varphi$ and the floor-bearing CV across the recall range. The 29-unit gain lies below the CV floor at $\hat{\pi} = 1/6$; the defined set of $\varphi$ strictly contains the CV-defined set.](../../reports/figs/v1_8/chart_02_defined_coverage.pdf){#fig:coverage width=100%}

## 4.4 Positional dissociation

$\varphi$ and $J$ capture distinct facets. Their rank correlation is $\rho(\varphi, J) = -0.403$, well within the 0.70 redundancy ceiling, and the percentile-divergence rule identifies nine units on which the magnitude and positional facets disagree. H_PositionalDissociation is CONFIRMED: a brand can be consistent in how often the panel surfaces it yet inconsistent in where, and $J$ reads the facet $\varphi$ cannot.

![$\varphi$ against the positional diagnostic $J$: $\rho(\varphi, J) = -0.403$, within the 0.70 redundancy ceiling, with the nine discordant units ringed.](../../reports/figs/v1_8/chart_03_phi_j_dissociation.pdf){#fig:dissociation width=100%}

## 4.5 CV-CPC baseline

The mean coupling that falsified CV-CPC recurs on the present base: $|\rho(\text{CV-CPC}_{\text{raw}}, \mu)| = 0.682$, above the 0.50 ceiling; H_CV_Reproduces is CONFIRMED. The base therefore carries the very coupling $\varphi$ dissociates from, which is what makes the §4.1 contrast a like-for-like comparison rather than a difference in data.

## 4.6 Temporal reproducibility

$\varphi$ reproduces across measurement waves at a moderate level: the rank correlation between the two waves of the reproducibility framing is $\rho(\varphi(t_1), \varphi(t_2)) = 0.645$ ($n = 83$, $p \approx 4.5 \times 10^{-11}$). The instrument is stable enough to track a brand's consistency across re-measurement, while leaving room — reported plainly rather than overstated — for wave-to-wave variation.

![$\varphi$ at wave $t_1$ against $\varphi$ at wave $t_2$: rank correlation $0.645$ ($n = 83$), scattered about the identity line.](../../reports/figs/v1_8/chart_04_two_wave.pdf){#fig:twowave width=100%}

## 4.7 Secondary and exploratory measures

The per-channel secondary diagnostic, computed on the three canonical two-channel substrates, returns defined $\varphi$ counts split by channel and gates no verdict; it is reported in the supplementary table. The exploratory phantom-signature contrast (29 near-phantom units against 55 non-phantom units within the 84-unit baseline — the same 29 that constitute $\varphi$'s low-recall coverage gain in §4.3) carries no directional commitment and is recorded as NULL.

# 5. Limitations and the path to composition

## 5.1 Limitations

Several limitations bound the present claim. The surfacing signal underlying $\varphi$ is extracted through three provenances — a pre-scored mention field, a certified string matcher, and a judge-scored field — rather than one uniform procedure. The provenance is uniform within each substrate, so a between-model statistic computed within a substrate is not confounded by it; but the pooled correlations combine substrate-level values whose surfacing was determined by different methods, and a single-procedure replication would strengthen the commensurability the reconciliation gate establishes.

The primary instruments are channel-agnostic by necessity, pooling the six frames per model to a single count. This is the correct decision for an omnibus two of whose substrates break a per-channel decomposition, but it is coarse: the channel-agnostic count discards the category/cultural structure that the per-channel secondary recovers only on the three canonical substrates. A base whose substrates were uniformly two-channel would permit a channel-resolved primary and a sharper read of where consistency concentrates.

The three validation framings are not independent. The full-omnibus and phantom framings coincide as one mean-independence estimate, so the effective evidence for the make-or-break is two estimates — a shared 84-unit set and a 29-unit low-recall stratum — supported by a two-wave stability check, rather than three independent replications. The counts are modest: the coverage gain rests on 29 units and the positional dissociation on nine discordant units. The result is internally consistent across every cut, but its external reach awaits a larger, structurally uniform base.

Two measurement properties are reported plainly rather than resolved. Recognition is binary by probe design across the frozen base, and an audit confirms the saturation is genuine; the graded-recognition instrument $R_{\text{grad}}$ is therefore specified but not scored, and a re-scorable recognition probe is needed to test it. And $\varphi$'s temporal reproducibility is moderate ($\rho = 0.645$) — adequate to track consistency across re-measurement, but short of the reliability a high-stakes single-number index would require.

Finally, the study validates one instrument, not a composite. $\varphi$ is the Consistency component of a larger score; its construct validity here does not establish the validity of any combination of components, and the omnibus spans five consumer categories whose generalization to other categories and to a wider model panel remains open.

## 5.2 The path to composition

The redesigned Consistency instrument is now a validated input rather than a falsified one, which moves the program from instrument repair to instrument assembly. The immediate next step, deferred from this phase, is composition: $\varphi$ and $J$ are two coupled instruments, and combining a magnitude facet with a positional one into a single Consistency reading is a distinct methodological problem with its own validity criteria. Beyond Consistency, the remaining components of the score — ranking, coverage, grounding, and sentiment — each require the construct-validity arc this phase completed for Consistency before any of them can enter a composite. $R_{\text{grad}}$ rejoins that sequence at the first phase with a graded recognition probe. The contribution here is narrow by design and load-bearing by intent: a single component, redesigned on a mean-independent basis, validated against its own falsified predecessor, and ready to compose.

# Declarations {-}

**Declaration of interest.** The author is Director, Corporate Brand Creative & Governance at Samsung Electronics America. This role is disclosed here and nowhere else in the paper, and it bears on two substrates of the frozen omnibus. In the headphones substrate (v0.19), the Samsung-affiliated brand AKG was excluded before the methodology lock and Denon substituted in its place, so that no Samsung-affiliated brand entered that substrate's scoring. In the automotive substrate (v0.22), the brand set contains Harman International, Samsung SDI, and Samsung Display as tier-2/3 Samsung subsidiaries; these were retained and scored under the same automated procedure as every other unit, and are flagged here. No analysis, threshold, or verdict was conditioned on any Samsung-affiliated brand, and the pre-registration discipline — lock and external anchor before any scoring — applied uniformly. The author's academic and independent-research affiliations (School of Visual Arts, MPS Branding Program; Third System™) carry no financial interest in the outcome.

**Funding.** Self-funded. No external grant or sponsor supported this work.

**Ethics.** Not applicable. The study involves no human subjects; all data derive from public model probes and their recorded responses.

**Data and materials.** The pre-registration, scorer, verdicts, instrument table, and materialization manifest are deposited to the project's Open Science Framework archive (osf.io/ec6wh) under the methodology namespace; the frozen omnibus is reproducible from the manifest's pinned references.

# References {-}

<!-- v1.8 reference list. SSRN titles transcribed verbatim from the author dashboard (2026-06-18).
     Eight DISTRIBUTED and citable. 6878818 (v1.7) is PRELIMINARY_UPLOAD: cite as in-process, and
     hold the public submission (step 9) until it distributes. 6921758 (v0.35) and 6927958 (v0.36)
     are REMOVED/inactive on SSRN: re-anchored to the OSF archive (their data provenance). 6816340
     trimmed (its verbatim title is an empirical phase-B extension, not a protocol paper). Confirm
     transcriptions against the dashboard before lock. -->

**Foundational (two-system framing).** Romaniuk, J., & Sharp, B. (2022). *How Brands Grow: Part 2* (Rev. ed.). Oxford University Press. [⚠ confirm edition/year]

**Program context — AIAS synthesis.** González Castro, P. U. (2026). *AI Availability as a Third Measurable Layer of Brand Availability: Five-Substrate Empirical Anchoring of the AIAS™ Presence Measurement Protocol — Synthesis under Locked v1.6 Methodology.* SSRN Working Paper 6817841.

**Pre-registration protocol (methodology series).** González Castro, P. U. (2026).

- *The AIAS™ Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy.* SSRN Working Paper 6761698.
- *The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification (v1.3).* SSRN Working Paper 6797679.
- *The AIAS Presence Measurement Protocol v1.4: Recognition × Recall Decomposition and Multi-Component AI Availability.* SSRN Working Paper 6799479.
- *The AIAS™ Presence Measurement Protocol: Multi-Statistic C2 Specification and Two-Channel Recall Decomposition.* SSRN Working Paper 6810758.

**Direct predecessor (CV-CPC, falsified).** González Castro, P. U. (2026). *Consistency without Independence: A Pre-Registered Test of Coefficient-of-Variation as the Consistency Component of AIAS™.* SSRN Working Paper 6878818. [In process; pending SSRN distribution.]

**Binding-constraint cascade.** González Castro, P. U. (2026). *Provider-Asymmetric Consistency in AI Brand Availability A Pre-Registered Re-Analysis: Modest between-Provider Structure in CV-CPC Recall, and the Limits of a Beyond-Presence Gate under Recognition Saturation.* SSRN Working Paper 6909019.

**Two-wave framing (v0.34).** González Castro, P. U. (2026). *Two-Wave Temporal Stability of an AI Brand-Recall Consistency Quantity: A Pre-Registered Longitudinal Re-Acquisition Across Five Product Categories (AIAS™ v0.34).* SSRN Working Paper 6915458.

**Validation framings v0.35 / v0.36 (frozen data).** González Castro, P. U. (2026). *AIAS™ phantom-roster (v0.35) and low-recall-stratum (v0.36) validation framings.* Frozen data deposited at the Open Science Framework, osf.io/ec6wh (methodology/v1_8); see the materialization manifest for the pinned records. [SSRN deposits inactive; provenance is the OSF archive.]
