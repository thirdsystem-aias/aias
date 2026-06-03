---
title: "Recognition Saturates, Consistency Doesn't"
subtitle: 'An Instrument-Specification Pilot of the AIAS™ Consistency Component (CPC) across Skincare, Cosmetics, and Automotive'
author: "Pablo Ulpiano González Castro"
date: "June 2026"
mainfont: "Carlito"
fontsize: 11pt
geometry: "margin=1in"
linkcolor: "black"
urlcolor: "black"
header-includes: |
  \usepackage{setspace}
  \usepackage{booktabs}
  \usepackage{graphicx}
  \usepackage{float}
  \usepackage{caption}
  \captionsetup{font=small,labelfont=bf}
  \setstretch{1.08}
  \renewcommand{\maketitle}{}
---

<!--
  build: thin pandoc wrapper -> xelatex (Carlito). NO LaTeX from Python.
  Figures expected at ../../reports/figs/v30/chart_30_*.pdf, resolved via
  --resource-path=papers/v0_30. Titlepage is the first body block; Abstract
  is forced to page 2.
-->

\begin{titlepage}
\setstretch{1.0}
\setlength{\parskip}{0pt}
\centering
\vspace*{1.2cm}

{\LARGE\bfseries Recognition Saturates, Consistency Doesn't\par}

\vspace{0.5cm}
{\large\itshape An Instrument-Specification Pilot of the AIAS\texttrademark{} Consistency Component (CPC) across Skincare, Cosmetics, and Automotive\par}

\vspace{0.4cm}
{\normalsize Working Paper \textperiodcentered{} Instrument-Specification Pilot\par}
{\normalsize AIAS Presence Measurement Protocol \textperiodcentered{} Consistency Component CPC.01 (v0.30)\par}

\vspace{1.0cm}
{\large Pablo Ulpiano González Castro\par}

\vspace{0.3cm}
{\normalsize MPS Branding Program, School of Visual Arts, New York, NY\\(primary academic affiliation)\par}
{\normalsize Third System\texttrademark{} --- research entity; data archive and methodology venue\par}

\vspace{0.5cm}
{\small Correspondence: pablou@pablou.com \textperiodcentered{} pablou.com\par}
{\small ORCID: 0009-0003-8968-9990\par}

\vspace{1.0cm}
{\small Pre-registration: OSF \texttt{osf.io/ec6wh} \textperiodcentered{} tags \texttt{v0.30-prereg-r1 / r2}; results \texttt{v0.30-results-r2}\\
Data, scoring, and verdicts deposited under \texttt{osf.io/ec6wh} (v30).\par}

\vfill
{\footnotesize June 2026\par}
\end{titlepage}

# Abstract {-}

The AIAS (AI Availability Score) program measures a brand's availability inside large language models. Its first component, Presence, captures whether a brand surfaces; its second, Consistency (CPC), captures how stably it surfaces across the model panel. This instrument-specification pilot defines Consistency as the cross-model dispersion of a brand's recall signal and tests it on three anchored substrates — skincare, cosmetics, and automotive — each measured against an identical six-model panel, reusing deposited data under a pre-registered analysis plan. Recall-based Consistency is defined for a majority of brands precisely where recognition has saturated and can no longer discriminate (confirmed), and corrected Consistency differs significantly across categories with the apparatus held fixed (confirmed). The raw measure is mechanically confounded with brand prominence, and a maximum-normalized (Bhatia–Davis) correction removes that confound — but this was testable in only one substrate, because the apparatus-homogeneous categories that sharpen the cross-category comparison are the mature categories in which recognition, the prominence variable, saturates. The confound hypotheses are therefore undetermined rather than confirmed. That tension — between the apparatus homogeneity a clean category comparison demands and the prominence variance a confound test requires — is the pilot's principal contribution, and it specifies the design the construct's validation must adopt.

**Keywords:** AI Availability; AI Availability Score; large language models; brand consistency; construct validity; coefficient of variation; brand measurement; generative AI search

**JEL codes:** M31 (primary); M37, L15, L86, D83

**Paper status:** Working paper · v0.30 (CPC.01). Pre-registered analysis; methodology and decision rules locked before scoring at git tags v0.30-prereg-r1 / r2, results at v0.30-results-r2. Pre-registration, data, scoring code, and verdicts deposited at OSF (osf.io/ec6wh).

# 1. Introduction

The AIAS (AI Availability Score) program treats a brand's availability inside large language models as a measurable layer of brand growth, alongside the mental and physical availability of the Ehrenberg-Bass tradition. Its first component, Presence, established that the degree to which a fixed panel of models recognizes and recalls a brand can be measured reliably and varies systematically across categories. Presence captures only *whether* a brand surfaces, however — not how stably it does so. Two brands may share an identical Presence score while one appears in every model's response and the other in half of them, differing sharply in the reliability of their AI representation. That stability is the object of the second component, Consistency (CPC).

Consistency is operationalized as the dispersion of a brand's recall signal across the model panel: a brand that surfaces evenly across all panel models is consistent; one that surfaces erratically is not. The natural statistic is the cross-model coefficient of variation, which carries a known hazard. On a bounded signal the coefficient of variation is mechanically coupled to its mean — dispersion is constrained near the floor and ceiling and maximized mid-range — so a raw measure registers low-frequency brands as inconsistent for an arithmetic reason rather than a substantive one. Establishing Consistency as a construct therefore requires more than computing a number: it requires showing the measure can be separated from sheer prominence, and that a principled correction restores that separation.

This study is an instrument-specification pilot. It does not estimate population values but specifies the Consistency instrument, exposes its failure modes on real data, and hands a normalization recommendation to the forthcoming methodology lock. Four pre-registered hypotheses structure the test. H_CPC_Computable asks whether a recall-based consistency signal is definable in categories where recognition has saturated — where every brand is recognized by every model and recognition can no longer discriminate. H_CPC_LevelConfound asks whether the raw measure is contaminated by prominence. H_CPC_LevelCorrected asks whether a maximum-normalized (Bhatia–Davis) correction removes that contamination. H_CPC_SubstrateVariation asks whether Consistency, once corrected, varies across categories rather than behaving as a fixed brand trait.

The pilot reuses already-deposited measurement data from three anchored substrates — skincare, cosmetics, and automotive — each measured against an identical six-model panel under a common protocol, with no new model queries. The substrates were selected for apparatus homogeneity, so that any cross-category difference in Consistency could be attributed to category rather than to measurement.

The outcome is mixed in an informative way. H_CPC_Computable and H_CPC_SubstrateVariation are confirmed: recall yields a defined consistency signal precisely where recognition has gone dark, and corrected Consistency differs significantly across categories. The confound hypotheses are not. In the single substrate that retained variance in the prominence variable (skincare), the predicted pattern held cleanly — the raw measure was confounded with prominence, and the correction removed that confound — but in the two saturated substrates the confound test is mathematically undefined, because the prominence variable is constant. The headline confound claim is therefore UNDETERMINED, not because the instrument failed but because the same category homogeneity that sharpened the substrate-variation result eliminated the prominence variance the confound test requires. That tension — between the apparatus homogeneity a clean category comparison demands and the prominence variance a confound test demands — is the pilot's principal methodological contribution, and §5 develops it as a design constraint for the methodology lock.

# 2. Method

**2.1 Design and data.** The pilot analyses previously collected measurement data; no new model queries were issued. Three anchored substrates supply the data — skincare, cosmetics, and automotive — each a locked registry of 24 brands measured under a common protocol and deposited in the program's archive. All three were measured against an identical six-model reference panel (Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o-mini, Gemini 2.5 Flash, Gemini 2.5 Flash Lite) with identical two-channel recall instrumentation. This homogeneity is deliberate: holding the panel and instrument fixed across substrates ensures that any cross-substrate difference in Consistency is attributable to the substrate, not to the measurement. Each brand carries two prior signals — a Phase A recognition count and a Phase B two-channel recall record.

**2.2 The consistency instrument.** For each brand *b* and model *m*, a recall signal $s(b,m)$ is the fraction of Phase B recall frames in which *b* surfaces in *m*'s response. The battery comprises six frames per model — three category-canonical (R_cat) and three cultural-footprint (R_cult) — so $s(b,m) \in [0,1]$. Mentions are detected with each substrate's own canonical matcher (case-insensitive, accent-stripped, possessive-aware, first-occurrence-wins), reused unchanged so detection matches each phase's original scoring. Each brand thus yields a six-element vector across the panel.

Consistency is the dispersion of that vector. Because the six models constitute the full reference population, dispersion is the population standard deviation. Two forms are reported. The raw instrument is the cross-model coefficient of variation, $\mathrm{CPC}_{\mathrm{raw}} = \mathrm{SD}_m[s] / \mathrm{mean}_m[s]$. Because the coefficient of variation on a bounded signal is mechanically coupled to its mean, a level-corrected instrument is also computed: $\mathrm{CPC}_{\mathrm{corr}} = \mathrm{SD}_m[s] / \sqrt{\mu(1-\mu)}$, where $\mu = \mathrm{mean}_m[s]$. The denominator is the maximum standard deviation attainable by any [0,1] variable with mean $\mu$ — the Bhatia–Davis bound — so CPC_corr expresses dispersion as a fraction of the maximum possible at that level and is, in principle, freed from the mean-dependence that contaminates the raw measure. A level-residualized coefficient of variation (the raw measure regressed on $\mu$, residuals retained) is reported as a robustness variant.

**2.3 Level variable and degenerate cells.** The confound is assessed against the brand's recognition count, L(*b*) = C_P $\in$ {0, …, 6}, from Phase A. Recognition is chosen deliberately over a recall-inclusive prominence measure: because the recall mean already appears inside the consistency statistic, correlating Consistency with a recall-based level would be partly tautological, whereas recognition is an independent signal. A brand is treated as consistency-undefined where μ = 0 (recall floor) or μ ≥ 0.98 (recall ceiling), since dispersion is uninformative at the bounds; the share of brands with a defined score — the coverage rate — is itself a reported outcome. For the coverage comparison, a recognition-based consistency is defined only where 0 < C_P < 6, since a brand recognized by all or none of the panel admits no recognition dispersion.

**2.4 Hypotheses and decision rules.** H_CPC_Computable holds if recall coverage is at least 50% in all three substrates and exceeds recognition coverage in automotive, the substrate predicted to saturate recognition most severely. H_CPC_LevelConfound holds if the Spearman correlation ρ(CPC_raw, L) is significant with |ρ| ≥ 0.30 in at least two of three substrates; H_CPC_LevelCorrected holds if |ρ(CPC_corr, L)| < 0.20 with at least 50% attenuation relative to the raw correlation, again in at least two of three. Correlations carry BCa 95% confidence intervals (10,000 resamples, seed 280400). A substrate in which L is constant — every brand at the recognition ceiling — admits no correlation, the statistic being undefined against a constant input; such a substrate is classed untestable rather than as evidence either way, and where fewer than two substrates are testable the two-of-three bar cannot be reached and the verdict is UNDETERMINED rather than FALSIFIED. H_CPC_SubstrateVariation holds if a Kruskal–Wallis test across the three corrected-consistency distributions is significant at p < .05. A non-confirmatory exploratory analysis compares the rank ordering of recognition-based and recall-based consistency where both are defined.

**2.5 Pre-registration.** Methodology, thresholds, and decision rules were committed to a version-controlled tag before any scoring code was run. An initial registration was amended before analysis when input certification revealed that one originally specified substrate had been measured on a different model generation and another on a single-channel recall instrument; the substrate set was replaced with the present doubly-homogeneous trio, all hypothesis definitions and thresholds carried forward unchanged. The amendment and its rationale are recorded in the pre-registration's deviations log.

# 3. Results

Across the three substrates, recall yields a defined consistency score for a clear majority of brands while recognition yields almost none. Coverage is 79% in skincare, 79% in cosmetics, and 62% in automotive, against recognition-based coverage of 17%, 0%, and 4% respectively (Figure 1). Recognition has saturated: in cosmetics all 24 brands are recognized by every model, and in automotive 23 of 24 are, leaving recognition with no dispersion to measure. Recall-based consistency remains defined precisely where recognition has gone dark. Both conditions of H_CPC_Computable hold — coverage exceeds 50% in every substrate, and recall coverage exceeds recognition coverage in automotive (62% against 4%) — and the hypothesis is **confirmed**.

![Recall yields a consistency signal where recognition cannot. Share of each 24-brand category with a defined consistency score, recall-based versus recognition-based. Recognition is saturated (cosmetics 24/24, automotive 23/24 fully recognized) and yields a usable score for almost no brands; recall-based consistency is defined for 79%, 79%, and 62% of brands across skincare, cosmetics, and automotive.](../../reports/figs/v30/chart_30_coverage.pdf){#fig:coverage width=100%}

The same saturation that confirms H_CPC_Computable constrains the confound test. The correlation between raw consistency and recognition level can be estimated only where recognition varies, and recognition varies only in skincare. There, the raw measure is significantly associated with prominence: ρ(CPC_raw, L) = −0.47 (p = .04), the negative sign indicating that less-recognized brands register as less consistent — the mechanical inflation the correction is designed to remove (Figure 2). In cosmetics and automotive the recognition level is constant across the recall-defined brands, so the correlation is undefined; these substrates are untestable for the confound rather than evidence against it. With one testable substrate, the two-of-three bar cannot be reached, and H_CPC_LevelConfound is **undetermined**.

![Raw consistency tracks prominence where prominence varies. CPC_raw against recognition level L (C_P) for recall-defined brands. In skincare, where recognition varies, the two are correlated (ρ = −0.47, p = .04); in cosmetics and automotive every brand sits at full recognition, collapsing to a vertical stack where the correlation is undefined.](../../reports/figs/v30/chart_30_confound.pdf){#fig:confound width=100%}

Where the correction could be evaluated, it behaved as specified. In skincare the association with prominence fell from −0.47 to −0.13 (p = .59, no longer significant), an attenuation of 72%; the residualized robustness variant moved in the same direction (ρ = −0.27), corroborating that the bias is both real and removable (Figure 3). Considered alone, skincare satisfies both conditions of H_CPC_LevelCorrected (|ρ_corr| < 0.20 and attenuation ≥ 50%). But the hypothesis requires the pattern in at least two substrates, and only one is testable; H_CPC_LevelCorrected is therefore **undetermined**, with the single-substrate demonstration reported as supporting rather than confirmatory evidence.

![The level correction removes the prominence bias (skincare). Raw (CPC_raw) and corrected (CPC_corr) consistency against recognition level for skincare brands. The Bhatia–Davis correction attenuates the association with prominence by 72% (ρ from −0.47 to −0.13, no longer significant).](../../reports/figs/v30/chart_30_correction.pdf){#fig:correction width=100%}

With the measurement apparatus held identical across substrates, the corrected-consistency distributions differ significantly (Kruskal–Wallis H = 14.24, p < 0.001; Figure 4). Because the panel and instrument are constant, the difference is attributable to the substrate rather than to measurement, and H_CPC_SubstrateVariation is **confirmed**: Consistency is category-conditioned, not a property a brand carries uniformly across categories.

![Consistency differs by category. Corrected consistency (CPC_corr) per recall-defined brand, by category, with the model panel held identical across categories. The distributions differ significantly (Kruskal–Wallis H = 14.24, p < 0.001).](../../reports/figs/v30/chart_30_variation.pdf){#fig:variation width=100%}

The pre-registered exploratory comparison of recognition-based and recall-based consistency rankings could not be computed: recognition-based consistency is defined for fewer than three brands across the trio — the same saturation that rendered the confound test untestable. Table 1 summarizes the per-substrate coverage and correlations.

Table: Per-substrate coverage and prominence correlations. Correlations are undefined where recognition level is constant across recall-defined brands.

| Substrate | n (defined) | Recall coverage | Recognition coverage | ρ(CPC_raw, L) | ρ(CPC_corr, L) | Attenuation |
|---|---|---|---|---|---|---|
| Skincare | 19 | 79% | 17% | −0.47 (p = .04) | −0.13 (p = .59) | 72% |
| Cosmetics | 19 | 79% | 0% | undefined (L constant) | — | — |
| Automotive | 15 | 62% | 4% | undefined (L constant) | — | — |

# 4. Discussion

Two results establish Consistency as a construct worth measuring, and a third — the indeterminate one — locates the condition under which it can be validated.

That H_CPC_Computable is confirmed is more consequential than a coverage statistic suggests. Recognition is the cheaper and more obvious signal, and in mature, high-identity categories it saturates: every serious brand is recognized by every model, and recognition ceases to discriminate. A consistency measure that merely tracked recognition would inherit that ceiling and go dark with it. Recall-based Consistency does not. It remains defined for a clear majority of brands exactly where recognition is exhausted — the first evidence that the component carries information the recognition channel cannot, a discriminant property established not by a low correlation but by the measure's survival where the prior signal collapses.

H_CPC_SubstrateVariation, also confirmed, establishes that this information has structure. With the panel and instrument held identical across categories, corrected Consistency still differs significantly between them; the difference cannot be a measurement artifact and is therefore a property of the category. Consistency is not a trait a brand carries uniformly wherever it appears — it is conditioned by the category in which the brand is being surfaced. A construct that varied randomly, or not at all, would not repay further measurement; one that varies systematically by category does.

The confound results are where interpretation must be most disciplined. In the single substrate that retained variance in the prominence variable, the instrument behaved exactly as its design anticipates: the raw coefficient of variation was significantly and negatively associated with recognition (ρ = −0.47), meaning less-recognized brands were scored as less consistent for an arithmetic reason rather than a substantive one, and the Bhatia–Davis correction removed that association (to ρ = −0.13, n.s.), with the residualized variant corroborating the direction. This is a clean demonstration that the confound is real and that the correction works. It is not, however, a confirmation. A single substrate cannot establish that the correction generalizes across categories whose prominence distributions differ, and the pre-registered decision rule — requiring the pattern in at least two of three substrates — returns UNDETERMINED rather than read a general claim from one case. The program therefore carries the Bhatia–Davis correction forward as a provisional working normalization: demonstrated where it could be tested, pending confirmation where it could not.

The reason it could not be tested is the pilot's central methodological finding. The substrate set was chosen for apparatus homogeneity, so that the category comparison underlying H_CPC_SubstrateVariation would be clean. But apparatus-homogeneous categories in a mature market are precisely the categories in which recognition saturates — and recognition is the variable against which the confound is assessed. The design choice that sharpened one validity test eliminated the variance the other required. This is not an accident of the categories selected; it is a structural tension for any dispersion measure whose confound is assessed against a bounded prominence signal. Wherever prominence saturates, the confound is simultaneously most suspected — the coefficient of variation being mechanically lowest at the ceiling — and least testable, there being no variance to test against. Validating Consistency therefore requires a substrate set selected deliberately to span prominence, not merely matched on apparatus, together with a level variable that retains variance where recognition does not.

A final point bears on the correction's practical stakes. The bias it removes runs against less-recognized brands: the raw measure would score smaller brands as less consistent regardless of how stably they actually surface. An AI-availability diagnostic is most decision-relevant precisely for such brands, so a correction that restores fairness across the prominence range is not a statistical refinement but a precondition for the metric's usefulness.

# 5. Limitations

The confound results rest on a single testable substrate. The instrument's central mechanic — bias and its correction — was observable only in skincare, so the demonstration that the Bhatia–Davis correction removes the prominence bias, however clean, is a single case rather than a confirmed generalization. The category selection is the proximate cause: the trio was chosen for apparatus homogeneity and sits mid-to-high on brand identity, with no low-recognition category to preserve a prominence spread, so two of three substrates saturated the variable against which the confound is assessed.

The level variable compounds this. Recognition count is a coarse ordinal on {0, …, 6} with no resolution above its ceiling; the same coarseness that keeps it independent of the recall mean — and so free of tautology — is what causes it to saturate and lose all variance in mature categories. A variable that discriminated among fully-recognized brands would have left the confound testable.

The remaining limitations are of scope. Consistency is measured across models at a single point in time; cross-platform consistency — dispersion across deployment surfaces, with their retrieval and system-prompt augmentation — is defined in the protocol but not measured here, and temporal consistency is not addressed. The analysis reuses already-deposited measurement data rather than fresh acquisition, and each substrate contributes only 24 brands (15–19 with a defined score), limiting correlation power even where the confound is testable. None of these bound the two confirmed hypotheses, which rest on coverage and cross-substrate comparison rather than within-substrate correlation; they bound the confound pair specifically.

# 6. Future Research

The pilot's indeterminate result is also its clearest instruction for what follows. Construct-validating Consistency requires a design that satisfies two demands the present one could meet only separately: a homogeneous measurement apparatus, so that category differences are real, and a spread of brand prominence, so that the confound test can run. These are reconcilable, but only by deliberate design rather than convenience.

Two pre-registered changes, fixed before any data is seen, would accomplish it. First, a graded prominence variable that retains variance where recognition saturates — drawn from a signal with resolution above the recognition ceiling, while remaining independent of the recall mean so the confound test stays non-tautological. Second, a category set spanning recognition levels from niche to ubiquitous, so that at least two substrates carry the prominence variance the test requires, with the panel and recall instrument held fixed across them. Together these resolve the apparatus-versus-prominence tension by construction.

This is the recommendation the pilot carries into the methodology lock: that cross-substrate Consistency validation mandate apparatus homogeneity and prominence spread jointly, with a saturation-robust level variable, as preconditions rather than as properties discovered after the fact. Beyond it lie the scopes deferred here — cross-platform consistency across deployment surfaces, and temporal consistency across measurement waves — each extending the construct along a dimension this pilot held fixed. The Bhatia–Davis correction carries forward as the provisional working normalization until the redesigned test either confirms it across categories or selects the residualized or agreement-coefficient alternative pre-registered in its place.

# Declarations {-}

**Conflict of interest.** The author is employed by Samsung Electronics America; the research entity Third System is independent. The three substrates analysed (skincare, cosmetics, automotive) contain no Samsung-owned brands, and the employer had no role in the design, analysis, or reporting.

**Funding.** Self-funded.

**Ethics.** Not applicable; no human subjects; public APIs and LLM prompts only.

**Data and code availability.** Pre-registration, reused measurement data, scoring code, and verdicts are deposited at OSF (osf.io/ec6wh, v30), under tags v0.30-prereg-r1 / r2 and v0.30-results-r2.
