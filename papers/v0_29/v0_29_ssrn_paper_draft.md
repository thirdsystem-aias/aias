---
title: "The Presence Component Is Construct-Valid"
subtitle: "A Convergent--Discriminant (Campbell--Fiske) Baseline for AI Availability"
mainfont: "Carlito"
fontsize: 11pt
geometry: margin=1in
linkcolor: black
urlcolor: black
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
  \captionsetup{font=small,labelfont=bf}
---

\begin{titlepage}
\setstretch{1.0}
\setlength{\parskip}{0pt}
\begin{center}

{\LARGE \textbf{The Presence Component Is Construct-Valid}}\\[6pt]
{\large \textit{A Convergent--Discriminant (Campbell--Fiske) Baseline for AI Availability}}\\[10pt]
{\normalsize Working Paper $\cdot$ Version 0.29 $\cdot$ Synthesis (Construct-Validity Baseline)}\\[24pt]

{\large Pablo Ulpiano González Castro}\\[6pt]
SVA, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\[2pt]
Third System\texttrademark{} (research entity; data archive and methodology venue)\\[2pt]
Correspondence: pablou@pablou.com $\cdot$ pablou.com\\[2pt]
ORCID: 0009-0003-8968-9990\\[24pt]

\end{center}

\noindent This synthesis assembles a multitrait--multimethod (MTMM) construct-validity claim for the Presence component of the AIAS\texttrademark{} (AI Availability Score) measurement program. It performs no new acquisition; it assembles two locked component verdicts into a single Campbell--Fiske baseline and computes one quantity, the convergent--discriminant gap. The convergent and discriminant legs are inherited, respectively, from SSRN 6842138 and SSRN 6847678.

\vfill
\end{titlepage}

# Abstract {-}

A measurement instrument earns the label *valid* only when it correlates with what it should and fails to correlate with what it should not. The AIAS (AI Availability Score) program has, to date, established each half of that requirement in separate studies: a convergent leg, in which the Presence component ($C_P$) tracked an external salience criterion (Google Trends), and a discriminant leg, in which $C_P$ was found orthogonal to a commercial-popularity criterion (Amazon Best Sellers Rank). The present synthesis assembles those two locked results into a single multitrait--multimethod frame and evaluates the joint Campbell--Fiske condition that defines a construct-validity baseline: convergence where expected, divergence where expected, and a positive gap between the two. The convergent coefficient is $\rho = 0.74$ ($p < 0.001$, $n = 24$); the discriminant coefficient is $\rho = -0.0002$ ($p = 0.998$, $n = 88$); the gap is $C_3 = 0.74$, with the required significance asymmetry intact. The hypothesis $\mathrm{H_{CV\_Baseline}}$ is **CONFIRMED**: the Presence component clears a convergent--discriminant construct-validity baseline. The study is deliberately two-legged; predictive validity is not claimed here, because it requires a longitudinal external criterion not yet in the program's data pipeline, and is gated to a subsequent wave. The contribution is not a new effect but a consolidation: the first joint statement that AIAS Presence behaves, across two independent external instruments, as a construct-valid measure rather than an artifact of either method.

**Keywords:** AI Availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; construct validity; convergent validity; discriminant validity; multitrait--multimethod; Campbell--Fiske; brand presence; large language models; share of model

**JEL codes:** M31 (primary); L86; L15; D83; M37

**Paper status:** Pre-registration locked at `v0.29-prereg-r1` (commit `a66c8d8`). This is a *synthesis* phase: no acquisition was performed, and there is no acquisition tag. All verdicts are inherited from the locked component studies v0.25 (SSRN 6842138, convergent) and v0.26 (SSRN 6847678, discriminant); the single computed quantity, the convergent--discriminant gap $C_3$, was committed at `191a793`. Methodology is locked at Protocol v1.6. Data and code: osf.io/ec6wh/v29/.

# 1. Introduction

The AIAS (AI Availability Score) program advances a specific theoretical claim: that the presence of a brand inside large language models constitutes a third system of brand availability, alongside the Mental and Physical Availability of the Ehrenberg--Bass tradition (Sharp, 2010; Romaniuk & Sharp, 2016). The first component of that score to be operationalized is *Presence* ($C_P$) -- the degree to which a brand is recognized and recalled by a fixed panel of models when probed under controlled conditions. A measurement claim of this kind is only as strong as its construct validity. A number that rises and falls with a brand's standing might be measuring that standing; it might equally be measuring an incidental correlate, or an artifact of the measurement method itself. Distinguishing these possibilities is the classical problem of construct validation (Cronbach & Meehl, 1955), and its classical instrument is the multitrait--multimethod (MTMM) matrix of Campbell and Fiske (1959): a measure is construct-valid to the extent that it converges with conceptually related measures obtained by different methods, and diverges from conceptually unrelated measures.

The program has accumulated the two halves of that requirement in separate, independently pre-registered studies. The convergent half (v0.25) tested whether $C_P$ tracks an external, human-behavioral salience signal -- search interest, as measured by Google Trends -- and found a strong monotonic association. The discriminant half (v0.26) tested whether $C_P$ tracks a conceptually distinct commercial signal -- sales rank, as measured by Amazon Best Sellers Rank (BSR) -- and found no association, a near-zero coefficient that functions as evidence that Presence is *not* merely a proxy for what sells. Each study stands on its own; neither, alone, is a construct-validity claim. Convergence without divergence cannot rule out a measure that correlates with everything; divergence without convergence cannot show that the measure tracks anything at all. The Campbell--Fiske condition is explicitly joint.

This paper supplies that joint statement. It is a synthesis, not a new experiment: it introduces no acquisition, no new panel, and no new brands. It assembles the two locked component verdicts into a single MTMM frame and evaluates the one comparison that neither component study could make from inside itself -- whether the convergent coefficient meaningfully exceeds the discriminant coefficient, with the convergent leg significant and the discriminant leg not. That comparison is the construct-validity baseline for AIAS Presence, and establishing it is the gate that the program's broader measurement roadmap has been built toward.

The scope is deliberately bounded to two legs. Predictive validity -- whether Presence at one time forecasts an external outcome at a later time -- is a third and distinct form of evidence, and it is not claimed here. It requires a longitudinal external criterion measured across a temporal gap, which the program's single-wave data pipeline does not yet contain; asserting it without that data would be a category error. Predictive validity is therefore gated to a subsequent measurement wave and is treated throughout as forthcoming, not as a finding.

# 2. Method

## 2.1 Design: synthesis, not acquisition

The study is a synthesis of two locked component verdicts. It performs no probing, runs no models, and constructs no new registry. The six-model reference panel held fixed across the program -- Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o-mini, Gemini 2.5 Flash, and Gemini 2.5 Flash Lite -- is inherited as published, as are both external instruments. The analysis reads the two component verdict files, places their coefficients in an MTMM frame, computes a single comparison statistic, and applies a pre-registered verdict rule. Every input is traceable to a locked, publicly deposited component study; the synthesis adds exactly one number.

## 2.2 The Campbell--Fiske frame

Two coefficients populate the relevant cells of the MTMM matrix. The *monotrait--heteromethod* (convergent) cell pairs Presence with an external measure of the same underlying construct -- salience -- obtained by a different method: search interest. The *heterotrait* (discriminant) cell pairs Presence with an external measure of a conceptually distinct construct -- commercial popularity -- obtained by yet another method: retail sales rank. Construct validity, in the Campbell--Fiske sense, requires the convergent coefficient to be substantial and significant while the discriminant coefficient is negligible and non-significant. A measure that satisfies both is behaving as a measure of its intended construct rather than of method variance or of an unrelated trait.

## 2.3 Inherited legs

The **convergent** leg is inherited from v0.25 (SSRN 6842138; pre-registration `v0.25-prereg-r1`). There, $C_P$ was correlated with Google Trends search interest across a 24-brand B2B SaaS registry, using Spearman's $\rho$ (rank correlation, appropriate to the bounded, non-normal composite). The locked primary verdict, $\mathrm{H_{CV\_Primary}}$, was CONFIRMED at $\rho = 0.7411$, $p = 3.4 \times 10^{-5}$, $n = 24$ (95% CI [0.398, 0.912]).

The **discriminant** leg is inherited from v0.26 (SSRN 6847678; pre-registration `v0.26-prereg-r2`). There, the relationship between $C_P$ and Amazon BSR was tested across a pooled set ($n = 88$; including the v0.16 retrofit substrate), again by Spearman's $\rho$. The study had framed this as a candidate predictive relationship; the pooled coefficient was $\rho = -0.0002$, $p = 0.998$ -- statistically indistinguishable from zero. In the present MTMM frame, that null is not a failure but the discriminant evidence: Presence does not track sales rank, which is precisely what a construct distinct from commercial popularity should do.

## 2.4 The gap statistic and verdict rule

The synthesis computes one quantity, the convergent--discriminant gap:

$$C_3 = \lvert \rho_{\text{conv}} \rvert - \lvert \rho_{\text{disc}} \rvert.$$

The pre-registered verdict rule ($\mathrm{H_{CV\_Baseline}}$, locked at `v0.29-prereg-r1`) is conjunctive and is **CONFIRMED** if and only if three conditions hold jointly: **C1**, the convergent leg is positive and significant; **C2**, the discriminant leg satisfies $\lvert \rho \rvert < 0.20$ and is non-significant; and **C3**, the gap is strictly positive. The verdict is **FALSIFIED** if $C_3 \le 0$ (a Campbell--Fiske inversion, in which the measure correlates more with the unrelated trait than the related one), and **PARTIAL** if the gap is positive but a leg drifts -- most plausibly the discriminant leg edging into significance. The pre-registration fixed $\lvert \rho \rvert < 0.20$ as the sole magnitude threshold; the convergent leg is governed by significance, not by a registered floor.

# 3. Results

## 3.1 Convergent leg (C1)

The inherited convergent coefficient is $\rho = 0.7411$ at $p = 3.4 \times 10^{-5}$, comfortably significant. Across the 24-brand B2B SaaS registry, Presence rises monotonically with external search interest (Figure 1). C1 holds.

![Convergent leg: AIAS Presence against Google Trends search interest across the 24-brand B2B SaaS registry ($\rho = 0.74$). The discriminant relationship (Presence against Amazon BSR, $\rho = -0.0002$, $n = 88$) is asserted from the inherited v0.26 verdict, not re-plotted -- a synthesis reports its components' locked results rather than re-deriving them.](../../reports/figs/v29/chart_29_convergent_scatter.pdf){#fig:convergent width=100%}

## 3.2 Discriminant leg (C2)

The inherited discriminant coefficient is $\rho = -0.0002$ at $p = 0.998$. Its magnitude, $0.0002$, sits far below the pre-registered $0.20$ ceiling, and it is non-significant. Presence and sales rank are, to the resolution of the data, unrelated. C2 holds.

## 3.3 The Campbell--Fiske gap (C3)

$$C_3 = \lvert 0.7411 \rvert - \lvert -0.0002 \rvert = 0.7409 > 0.$$

The gap is large and positive, and the significance asymmetry is intact: the convergent leg is significant, the discriminant leg is not (Figure 2). C3 holds.

![The construct-validity gap: convergent correlation magnitude ($\lvert \rho \rvert = 0.74$, significant) against discriminant magnitude ($\lvert \rho \rvert = 0.0002$, non-significant, inside the pre-registered 0.20 ceiling). The gap $C_3 = 0.74$ is the single quantity this synthesis computes.](../../reports/figs/v29/chart_29_mtmm_gap.pdf){#fig:gap width=100%}

## 3.4 Verdict

All three conditions hold: C1 (significant convergence), C2 ($\lvert \rho \rvert < 0.20$, non-significant divergence), and C3 (positive gap), with the significance asymmetry present. $\mathrm{H_{CV\_Baseline}}$ is **CONFIRMED**. The Presence component clears a convergent--discriminant construct-validity baseline.

One pre-registration note belongs in the record. The pre-registered point estimate for $C_3$ was approximately $0.55$, anchored to the upper edge of the $\lvert \rho \rvert < 0.20$ discriminant band. The realized gap, $0.7409$, exceeds that estimate -- not because the convergent leg was stronger than expected, but because the inherited discriminant coefficient came in near zero ($-0.0002$) rather than near the band ceiling. The estimate was a non-binding forecast; the verdict rule depends on the sign and significance pattern, not on the point value, and the realization strengthens rather than complicates the baseline. The pre-registration lock is left untouched; this is a forecast-versus-realization observation, not a methodological change.

# 4. Discussion

The result is a consolidation rather than a discovery, and that is its point. Each component study was, in isolation, suggestive but incomplete. A strong convergent correlation alone is consistent with a measure that correlates indiscriminately; a near-zero discriminant correlation alone is consistent with a measure that correlates with nothing. Only the joint Campbell--Fiske condition distinguishes a construct-valid measure from these alternatives, and only a synthesis -- standing outside both component studies -- can evaluate it. The convergent--discriminant gap of $0.74$, with its significance asymmetry, is the first statement that AIAS Presence is construct-valid in the technical sense, not merely correlated with something.

The discriminant result deserves emphasis, because its interpretation inverts the usual reading of a null. That Presence does not track Amazon BSR is, here, the desired outcome: it shows that what the panel of models "knows" about a brand is not a restatement of what that brand sells. Presence and commercial popularity are separable, which is a precondition for treating AI Availability as a distinct system rather than a downstream shadow of sales. Had the discriminant coefficient been large, the more parsimonious account would have been that Presence simply reflects market success channelled through training corpora; the near-zero coefficient closes that account off for this criterion.

For the broader program, the baseline functions as a gate. The Presence component can now be carried forward into the wider AIAS roadmap with a documented construct-validity warrant behind it, rather than on the strength of face validity alone. The synthesis does not, however, license overreach. It validates Presence against two external criteria by two methods; it does not validate the remaining AIAS components, which are not yet operationalized, and it does not establish that Presence predicts anything over time.

# 5. Limitations

The study inherits the limitations of its components and adds one of its own. It is **two-legged by design**: convergent and discriminant evidence are present, predictive evidence is absent, and a construct-validity baseline built on two legs is genuinely a baseline rather than a complete validation. The **convergent leg rests on a single external instrument** (Google Trends) and a single sector (B2B SaaS); the **discriminant leg rests on a single criterion** (Amazon BSR) over a pooled set whose composition is fixed by v0.26 and not re-opened here. The synthesis cannot exceed the evidential reach of those instruments, and a different convergent or discriminant criterion could in principle yield a different coefficient. Finally, both component coefficients are point estimates from finite samples ($n = 24$ and $n = 88$); the baseline is a claim about the present panel and registries, not a universal property of the measure.

# 6. Future research

Three extensions follow directly. First and most consequential, **predictive validity** -- the gated next study -- requires a second measurement wave so that Presence at $t_1$ can be tested against an external criterion at $t_2$. This is the missing third leg, and the program is structured to add it once longitudinal external-criterion data exists. Second, the **convergent and discriminant legs invite additional criteria and methods**: a convergent test against an independent salience instrument, and a discriminant test against a construct other than sales rank, would each broaden the MTMM frame beyond its current single-cell-per-quadrant form. The Mental Availability leg deferred from the construct-validity sequence is the natural next convergent criterion. Third, the **remaining AIAS components** -- Ranking, Consistency, Coverage, Grounding, and Sentiment -- each await their own operationalization and, in turn, their own construct-validity baselines; the present synthesis establishes the template they will follow.

# Declarations {-}

**Conflict of interest.** The author is employed by Samsung Electronics America in a corporate brand role. That employment played no part in the design, conduct, analysis, or reporting of this research, which was carried out independently under the Third System research entity. No commercial relationship exists between any brand examined in the inherited component studies and the author or his employer that bears on the findings.

**Funding.** Self-funded.

**Ethics.** Not applicable; no human subjects. The inherited component studies used public APIs and large-language-model prompts only.

**Data and code availability.** This synthesis deposits its verdict assembly, scoring code, figures, and pre-registration at osf.io/ec6wh/v29/. The inherited data and verdicts are available with their respective component studies: convergent, SSRN 6842138; discriminant, SSRN 6847678. The methodology is documented across SSRN 6761698, 6797679, 6799479, 6810758, and 6816340, and the foundational AIAS 1.0 synthesis at SSRN 6817841.

# References {-}

Campbell, D. T., & Fiske, D. W. (1959). Convergent and discriminant validation by the multitrait-multimethod matrix. *Psychological Bulletin, 56*(2), 81--105.

Cronbach, L. J., & Meehl, P. E. (1955). Construct validity in psychological tests. *Psychological Bulletin, 52*(4), 281--302.

Romaniuk, J., & Sharp, B. (2016). *How Brands Grow: Part 2* (Revised ed.). Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.
