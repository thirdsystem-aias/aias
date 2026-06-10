---
title: "Provider-Asymmetric Consistency in AI Brand Availability"
subtitle: "A pre-registered re-analysis: modest between-provider structure in CV-CPC recall, and the limits of a Beyond-Presence gate under recognition saturation"
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

{\LARGE \textbf{Provider-Asymmetric Consistency in AI Brand Availability}}\\[8pt]

{\large A pre-registered re-analysis: modest between-provider structure in CV-CPC recall,\\ and the limits of a Beyond-Presence gate under recognition saturation}\\[28pt]

Pablo Ulpiano González Castro\\[4pt]
School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System™ (research entity; data archive and methodology venue)\\[8pt]
Correspondence: pablou@pablou.com · pablou.com\\
ORCID: 0009-0003-8968-9990\\[20pt]

Pre-registration: \texttt{v0.34-prereg-r1} (no deviations)\\
Data and code: OSF \texttt{ec6wh/v34}\\

\end{center}
\end{titlepage}

# Abstract {-}

AI Availability --- the discoverability and representation of a brand in the outputs of large language models --- has been proposed as a third layer of brand availability, complementing the Mental and Physical Availability of the Ehrenberg-Bass tradition. Within the AIAS™ (AI Availability Score) program, the Consistency component is operationalized as CV-CPC, a coefficient-of-variation statistic over per-model recall; a prior methodology lock found CV-CPC strongly presence-coupled ($|\rho| = 0.77$) and did not adopt it as a validated Consistency instrument. This pre-registered re-analysis tests, across five panel-uniform substrates (112 brands; a fixed six-model panel spanning three providers --- Anthropic, OpenAI, and Google), whether the per-model recall structure underlying CV-CPC is systematically organized by provider, and whether any such organization exceeds the provider structure present in Presence (recognition).

Between-provider organization of per-model recall is statistically robust but modest: the between-provider variance share exceeds its permutation null ($p < 0.001$) and survives all five leave-one-substrate-out refits, though its excess over a high small-group chance floor is small. The pre-registered Beyond-Presence gate met its criterion yet does not establish dissociation: binary recognition is saturated among recalled brands --- carrying negligible between-provider variance --- so the gate collapses onto the recall-asymmetry test rather than contrasting with Presence. This inverts the pre-registered directional prediction and reframes the gate's behavior as the study's principal methodological result: a Beyond-Presence contrast is uninformative wherever recognition is saturated. Provider rank-stability was uninformative as pre-registered, underpowered at five substrates. The study positions provider as a modest organizing factor in CV-CPC recall and bounds the conditions under which the AIAS Beyond-Presence gate can fire.

**Keywords:** AI Availability; AI Availability Score (AIAS); Consistency; CV-CPC; large language models; provider asymmetry; variance decomposition; recognition saturation; pre-registered re-analysis; brand availability; Ehrenberg-Bass; pre-registration

**JEL codes:** M31; L86; L15; D83; M37

**Paper status:** Pre-registered re-analysis (tag `v0.34-prereg-r1`); secondary analysis of frozen v0.31 inputs with no new data collection; no deviations from pre-registration. Part of the AIAS measurement program.

# 1. Introduction

AI Availability --- the discoverability and representation of a brand in the outputs of large language models --- has been proposed as a third layer of brand availability (González Castro, 2026, SSRN 6659000), complementing the Mental and Physical Availability of the Ehrenberg-Bass tradition (Sharp, 2010; Romaniuk & Sharp, 2022). The AIAS (AI Availability Score) program operationalizes this layer as a multi-component construct, of which Presence was the first component measured and locked (AIAS 1.0; SSRN 6817841). Consistency is the program's second component. Its current operationalization, CV-CPC --- a coefficient-of-variation statistic over per-model recall (v0.30; SSRN 6875319) --- was examined in a prior methodology lock and found strongly presence-coupled ($|\rho| = 0.77$); on that basis it was not adopted as a validated Consistency instrument, and a mean-independent redefinition was deferred (v1.7; SSRN 6878818).

Because CV-CPC is not a validated Consistency measure, this study does not attempt to validate it. It asks a narrower, descriptive question about the quantity as already computed: is the per-model recall structure underlying CV-CPC systematically organized by the LLM *provider* --- Anthropic, OpenAI, or Google --- that produced each model, and does any such organization exceed the provider structure present in Presence, reflecting something beyond a restatement of recognition? The first question is a between-provider variance decomposition; the second a pre-registered gate that contrasts the two.

The motivation is cross-sectional. A prior phase found CV-CPC version-stability to be provider-dependent --- confirmed in aggregate but fragile under leave-one-provider-out, the overall stability resting disproportionately on a single provider --- a result in the *temporal* dimension (v0.32; SSRN 6898581). The present study asks the orthogonal *cross-sectional* question at a single fixed model snapshot: holding versions constant, do providers differ systematically? The two dimensions are kept distinct throughout.

The work is a pre-registered re-analysis: it issues no new model queries and is a secondary analysis of frozen per-model inputs from an earlier cross-category baseline (v0.31; archived at OSF, osf.io/ec6wh/v34), with the full methodology --- hypotheses, decomposition, null model, and decision rules --- locked at a tagged commit before any scoring was run. Three results follow. Between-provider organization of per-model recall is statistically robust but modest. The pre-registered Beyond-Presence gate meets its numerical criterion but does not establish a dissociation: among recalled brands, binary recognition proves saturated, so the gate collapses onto the recall-asymmetry test rather than contrasting with it. That collapse --- not the asymmetry itself --- is the study's principal contribution: it bounds the conditions under which a Beyond-Presence contrast can be informative at all.

# 2. Method

## 2.1 Design and data provenance

The study is a secondary re-analysis; no language-model queries were issued. The frozen inputs are the per-model recall and recognition records assembled for an earlier cross-category CPC baseline (v0.31; archived at OSF, osf.io/ec6wh/v34), restricted to the five substrates carrying the program's canonical six-model panel: audiophile headphones (16 brands), skincare, cosmetics, automotive, and premium spirits (24 each), for 112 brand units. Three substrates fall outside the panel-uniform set: two are structurally incompatible (a 14-model legacy panel without per-model recall; off-panel model versions), and one remains unscored. A sixth substrate (indie fragrance) carries the panel but a non-comparable three-frame geometry and enters only as a walled descriptive concordance check.

Because the baseline's published outputs are brand-collapsed, per-model granularity was recovered by re-running its certified extraction across three heterogeneous input formats; this recompute is the operative path, not a fallback. As a reproducibility guardrail, recomputed per-model recall vectors for three substrates were required to reproduce the methodology-lock's stored per-model column bit-for-bit; the check passed for all 72 brands in scope (aligned by model name, the lock having stored models in sorted rather than panel order). The remaining two substrates have no external anchor and rest on the baseline's extraction provenance, which is stated rather than overclaimed.

## 2.2 Provider grouping and quantities

The six-model panel comprises three providers of two models each --- Anthropic (Claude Opus 4.5, Sonnet 4.5), OpenAI (GPT-4o, GPT-4o-mini), and Google (Gemini 2.5 Flash, Flash-Lite) --- at a fixed snapshot. The CV-CPC definition is inherited unchanged from the baseline and is treated throughout as the descriptive, presence-coupled quantity the methodology lock declined to adopt.

For each brand the per-model recall counts form a six-vector; provider organization is quantified as the between-provider share of variance, $\eta^2 = \mathrm{SS}_{\text{between}}(\text{provider}) / \mathrm{SS}_{\text{total}}$, in a one-way layout with provider as a three-level factor and two models per level. A brand whose six per-model values are identical has no variance to partition; its share is defined as $\eta^2 := 0$ rather than excluded, since a brand on which models do not differ exhibits zero provider asymmetry and excluding such brands would upward-bias the mean. The identical decomposition applied to per-model binary recognition yields the Presence share $\eta^2_{CP}$. The inherited recall floor --- below which the CV-CPC scalar is undefined --- governs the brands entering the paired contrast and the below-/above-floor comparison, but not the $\eta^2$ decomposition itself, which is computed across all 112 brands under the zero-variance convention.

## 2.3 Hypotheses, inference, and robustness

Two primary hypotheses were pre-registered. H_Provider_Asymmetry holds that the between-provider component is a material, non-null share of total cross-model recall dispersion, confirmed when mean $\eta^2$ exceeds its permutation null and falsified when it lies within. H_Provider_Beyond_Presence, the gating hypothesis, holds that provider asymmetry in CV-CPC exceeds that in Presence; its statistic is the paired $\delta\eta^2 = \eta^2_{\text{CVCPC}} - \eta^2_{CP}$, over brands for which both decompositions are defined. A secondary hypothesis, H_Provider_Ordinal, holds that provider rank by within-pair consistency is stable across substrates (Kendall's $W$), pre-registered as underpowered at five substrates, with a null $W$ to be read as uninformative rather than disconfirming. A tertiary, exploratory hypothesis examined whether asymmetry differs for below-floor brands.

Inference is by permutation. Each brand's space of model-to-provider assignments is exactly enumerable --- six models into three labelled pairs yields ninety assignments --- and the population test resamples from these per-brand spaces (Monte Carlo, at least 10,000 draws, one-sided); Kendall's $W$ is tested against its exact null over the 7,776 joint rank arrangements. Primary robustness is assessed by leave-one-substrate-out refitting across the five substrates. By pre-registration the design is exploratory and descriptive: with two models per provider the within-provider variance is a single-degree-of-freedom estimate, and the small-group structure places a high null expectation under $\eta^2$ --- both are carried into interpretation rather than treated as nuisances.

# 3. Results

## 3.1 Reconciliation

The per-model recompute reproduced the methodology-lock's stored recall vectors bit-for-bit for all 72 brands in the three anchored substrates, after alignment by model name rather than panel position. No discrepancy arose, so no computational-reproducibility note was warranted; the two unanchored substrates rest on the baseline's extraction provenance as stated.

## 3.2 Provider asymmetry (H_Provider_Asymmetry)

Provider organization of per-model recall is significant but modest. The mean between-provider variance share across the 112 brands is $\eta^2 = 0.360$, against a permutation-null mean of 0.293 (95th percentile 0.326); the observed value exceeds the null at $p = 0.0007$ and survives all five leave-one-substrate-out refits (each $p < 0.005$). H_Provider_Asymmetry is CONFIRMED and robust. Its magnitude, however, is small: with three providers of two models each, between-provider variance captures a high share by construction --- the null expectation alone is 0.293 --- so the genuine provider signal is the excess of roughly 0.07 above that floor, not the raw 0.360. The result is a reliably-detectable but slight provider organization, not a dominant one (Figure 1).

![Permutation-null distribution of the mean between-provider variance share, with the observed $\eta^2 = 0.360$ and the null 95th percentile (0.326) marked. The observed value sits modestly above a high null expectation (0.293); the genuine provider signal is the small excess over that floor, not the raw share.](../../reports/figs/v34/chart_01_eta2_null.pdf){#fig:eta2null width=100%}

## 3.3 The Beyond-Presence gate (H_Provider_Beyond_Presence)

The pre-registered gate meets its numerical criterion: the paired $\delta\eta^2 = \eta^2_{\text{CVCPC}} - \eta^2_{CP}$ is $+0.505$ against a paired-null mean of $+0.378$ (95th percentile 0.433), $p = 0.0001$, so by the locked rule H_Provider_Beyond_Presence is CONFIRMED. It does not, however, establish a dissociation between Consistency and Presence, and is not reported as one. Among the above-floor brands entering the contrast, per-model binary recognition is saturated: 54 of 55 carry zero between-model recognition variance --- every model recognizes them --- and the premium-spirits substrate is saturated at source, giving a mean Presence share of $\eta^2_{CP} \approx 0.0045$. With $\eta^2_{CP} \approx 0$, the statistic and its null both reduce to the recall arm: the recall-$\eta^2$ null is 0.385, and the paired null (0.378) differs from it only by a negligible recognition term (0.007), so the gate measures recall asymmetry on the above-floor subset rather than contrasting it with Presence. The pre-registered prediction --- that CV-CPC asymmetry would merely restate Presence asymmetry --- is thereby inverted, but not because a dissociation was found: the restatement concern cannot arise where Presence carries no provider structure to restate (Figure 2). This collapse is the study's principal methodological result, developed in Section 4.

![Between-provider variance share for the recall arm ($\eta^2 = 0.510$, null mean 0.385) versus the recognition arm ($\eta^2_{CP} \approx 0.0045$, null mean 0.007) among above-floor brands. Recognition is saturated --- 54 of 55 brands carry zero between-model recognition variance and premium spirits is saturated at source --- so the paired gate ($\delta\eta^2 = 0.505$, $p = 0.0001$) collapses onto the recall arm rather than contrasting with Presence.](../../reports/figs/v34/chart_02_gate_arms.pdf){#fig:gatearms width=100%}

## 3.4 Provider rank stability (H_Provider_Ordinal)

Provider rank by within-pair consistency is not stably ordered across the five substrates: Kendall's $W = 0.31$ against the exact null ($p = 0.18$). As pre-registered, this is read as uninformative rather than disconfirming --- at five substrates the test cannot resolve concordance --- and the per-substrate ranks are reported descriptively (Figure 3).

![Provider within-pair-consistency ranks by substrate (skincare is a genuine tie between Anthropic and OpenAI, shown as 1.5 / 1.5 / 3). Kendall's $W = 0.31$, exact $p = 0.18$: underpowered at five substrates and uninformative about concordance, not disconfirming.](../../reports/figs/v34/chart_03_provider_ranks.pdf){#fig:ranks width=100%}

## 3.5 Below-floor brands (H_Provider_Phantom, exploratory)

The exploratory contrast runs opposite to the loose hypothesis: below-floor brands show lower provider asymmetry ($\eta^2 = 0.216$) than above-floor brands (0.510). The direction is mechanical --- brands near the recall floor have little per-model recall variance to partition, depressing the between-provider share --- and is reported as such, not as evidence about phantom-prone brands.

# 4. Discussion

Two findings carry the study, and the more consequential is the negative one.

First, provider identity is a real but slight organizing factor in the per-model recall that underlies CV-CPC. The between-provider share of recall variance is reliably above its permutation null and stable across substrates, but the excess over the high small-group null expectation is small. For the AIAS program this means the cross-model dispersion CV-CPC summarizes is only modestly structured by provider: recall counts cluster somewhat by the model's maker, but provider is far from the dominant source of dispersion. A Consistency instrument therefore need not stratify heavily by provider, and reported CV-CPC values are not strongly an artifact of which providers populate a panel --- a reassurance, not a large effect.

Second, and more instructive, the pre-registered Beyond-Presence gate met its criterion without doing the work it was designed to do. The gate exists to separate genuine Consistency-asymmetry from a mere restatement of Presence-asymmetry, by contrasting the provider structure of recall against the provider structure of recognition. That contrast is meaningful only where recognition carries provider structure to contrast against. Among recalled brands it does not: binary recognition is saturated --- every model recognizes the brand --- so recognition has essentially no between-provider variance, and the gate degenerates into the recall-asymmetry test it was meant to be checked against. The gate is thus informative only in the partial-recognition regime, which by construction excludes the brands a model actually recalls. This is not a peculiarity of the present data but a structural property of any Presence-versus-Consistency gate built on binary recognition: the comparison vanishes exactly where recall --- and therefore Consistency --- is defined.

This refines, rather than overturns, the prior methodology lock. That lock found CV-CPC presence-coupled at the brand level ($|\rho| = 0.77$) and on that basis declined to adopt it, reasoning that CV-CPC might merely restate Presence (v1.7; SSRN 6878818). The present result locates the limit of that concern: the coupling is a phenomenon of level --- brands recognized more are recalled more --- not of provider structure. The provider organization of recall is not inherited from a provider organization of recognition, because among recalled brands there is none. Level-coupling and provider-structure independence can coexist, and the Beyond-Presence gate cannot adjudicate the latter while recognition is saturated.

# 5. Limitations

The design is, by pre-registration, exploratory and descriptive, and several limits bound its claims. Substrate-level power is thin: five substrates cannot resolve provider rank-stability (the Ordinal test was pre-registered as underpowered and returned uninformative) or support substrate-level generalization, and the brand-level sample of 112 supports only the existence tests for aggregate asymmetry. With two models per provider the within-provider variance is a single-degree-of-freedom estimate, and the three-by-two structure places a high null expectation (0.293) under $\eta^2$, so all effect sizes must be read against that floor rather than at face value. The analyzed quantity is CV-CPC as computed, not a validated Consistency measure; the prior lock declined to adopt it, and nothing here revises that status. Recognition enters as a binary signal and is saturated among recalled brands; a recognition-source audit confirms that the only graded recognition field in the corpus (v0.23 r_level) is itself saturated, so no graded signal with between-model variance exists to probe the saturation further, and the bound on the gate's informativeness is a real property of the available recognition instrument rather than an artifact of binarization. Finally, two of the five substrates lack an external reconciliation anchor and rest on the baseline's extraction provenance, and the analysis is confined to a single fixed model snapshot --- orthogonal to, and not generalizable across, the temporal axis of the prior version-stability phase.

# 6. Future Work

The clearest implication is for the next Consistency instrument. The recall-arm asymmetry is real, but the Beyond-Presence gate cannot test it against Presence while recognition is saturated; a graded or continuous recognition measure --- which the current corpus does not contain --- would give the gate variance to work with and let the dissociation question be asked where recall is defined. A graded-recognition acquisition is therefore the natural prerequisite for any future Beyond-Presence claim. Beyond the instrument, a larger substrate panel would power the provider-level characterization and rank-stability that five substrates cannot, and more than two models per provider would escape the single-degree-of-freedom within-provider estimate and lower the $\eta^2$ null floor that makes the present asymmetry read as modest. Together with the mean-independent Consistency redefinition already motivated by the prior lock, these extensions would convert the present descriptive bound into a testable account of whether provider organizes Consistency once the instrument can see past recognition saturation.

# Declarations {-}

**Conflict of interest.** The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study is a secondary re-analysis of data assembled in earlier phases (v0.19--v0.23); it introduces no new brand selection or data collection. Two of the five re-analyzed substrates intersect businesses owned by Samsung Electronics: audiophile headphones, a category that includes brands of Harman International (a Samsung subsidiary), and automotive, where Samsung interests include Harman automotive systems and Samsung SDI. The brand registries were fixed under the locked protocol of the original phases, scoring is fully automated against those registries, and the analysis reported here was pre-registered (tag `v0.34-prereg-r1`) before any scoring; the author's affiliation played no role in registry construction, scoring, or the resulting verdicts. Samsung Electronics had no role in the design, conduct, analysis, or reporting of this work.

**Funding.** Self-funded.

**Ethics.** Not applicable; no human subjects; public APIs and LLM prompts.

**Data and code availability.** Pre-registration, scoring code, per-brand outputs, and verdicts are deposited at OSF (`osf.io/ec6wh`, component `v34`): the locked pre-registration (`v0.34-prereg-r1`), the scorer (`score_v34.py`), the per-brand recall/recognition vectors and $\eta^2$ values (`v34_eta2.csv`), the verdicts (`v34_longitudinal_t1_t2_omnibus_verdicts.json`) including reconciliation and computation notes, and the post-hoc recognition-source audit.

# References {-}

*(Titles verified against the SSRN registry; abstract IDs and URLs are canonical. The v0.31 precursor's SSRN working paper has been withdrawn — its frozen per-model inputs are archived at OSF, osf.io/ec6wh/v34.)*

González Castro, P. U. (2026). *AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval.* SSRN. https://ssrn.com/abstract=6659000

González Castro, P. U. (2026). *AI Availability as a Third Measurable Layer of Brand Availability: Five-Substrate Empirical Anchoring of the AIAS™ Presence Measurement Protocol — Synthesis under Locked v1.6 Methodology.* SSRN. https://ssrn.com/abstract=6817841

González Castro, P. U. (2026). *Recognition Saturates, Consistency Doesn't — An Instrument-Specification Pilot of the AIAS™ Consistency Component (CPC) across Skincare, Cosmetics, and Automotive.* SSRN. https://ssrn.com/abstract=6875319

González Castro, P. U. (2026). *The AIAS™ Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy.* SSRN. https://ssrn.com/abstract=6761698

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification (v1.3).* SSRN. https://ssrn.com/abstract=6797679

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol v1.4: Recognition × Recall Decomposition and Multi-Component AI Availability.* SSRN. https://ssrn.com/abstract=6799479

González Castro, P. U. (2026). *The AIAS™ Presence Measurement Protocol: Multi-Statistic C2 Specification and Two-Channel Recall Decomposition.* SSRN. https://ssrn.com/abstract=6810758

González Castro, P. U. (2026). *Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension.* SSRN. https://ssrn.com/abstract=6816340

González Castro, P. U. (2026). *Consistency without Independence: A Pre-Registered Test of Coefficient-of-Variation as the Consistency Component of AIAS™.* SSRN. https://ssrn.com/abstract=6878818

González Castro, P. U. (2026). *Consistency Across Categories: A Cross-Category Baseline for the AIAS™ Consistency Component (CPC).* AIAS v0.31 — SSRN working paper withdrawn; frozen per-model inputs archived at OSF, osf.io/ec6wh/v34.

González Castro, P. U. (2026). *Version-Snapshot Stability of an AI-Presence Consistency Score.* SSRN. https://ssrn.com/abstract=6898581

Romaniuk, J., & Sharp, B. (2022). *How Brands Grow: Part 2* (Rev. ed.). Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know.* Oxford University Press.
