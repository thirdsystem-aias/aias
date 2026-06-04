---
title: "Consistency without Independence"
subtitle: "A Pre-Registered Test of Coefficient-of-Variation as the Consistency Component of AIAS™"
fontsize: 11pt
mainfont: "Carlito"
keywords: "AI Availability; AIAS; brand measurement; large language models; coefficient of variation; consistency; recall; pre-registration; negative result; mental availability"
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

{\LARGE\bfseries Consistency without Independence}

\vspace{0.8em}

{\large A Pre-Registered Test of Coefficient-of-Variation as the\\ Consistency Component of AIAS\texttrademark}

\vspace{2.5em}

Pablo Ulpiano González Castro

\vspace{0.6em}

School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System\texttrademark{} (research entity; data archive and methodology venue)

\vspace{1em}

Correspondence: pablou@pablou.com \textperiodcentered{} pablou.com\\
ORCID: 0009-0003-8968-9990

\vspace{2.5em}

\textit{AIAS\texttrademark{} Measurement Program \textperiodcentered{} Working Paper}\\
Methodology locked at \texttt{v1.7-prereg-r2}\\
Falsification and redefinition escalation recorded at \texttt{v1.7-prereg-r3}

\vspace{1.5em}

2026

\end{center}
\end{titlepage}

# Abstract {-}

AI Availability extends brand-science accounts of mental and physical availability into AI-mediated discovery, and its measurement programme builds the construct one component at a time. Presence shipped as the first component; Consistency, the stability of a brand's presence across a model panel, is the candidate second. This paper pre-registers and tests the natural operationalization: the coefficient of variation of cross-model recall, mapped to a bounded consistency score. Under a locked protocol applied to three anchored substrates, the instrument fails its pre-registered independence criterion. Consistency correlates with Presence at pooled $|\rho| = 0.77$, above the 0.50 ceiling and positive in every substrate. The failure traces to a mechanical identity: at the recall counts language models return, dispersion follows the Poisson relation in which the standard deviation scales with the square root of the mean, so the coefficient of variation approximates the reciprocal of the square root of the mean and reparametrizes presence level rather than isolating a distinct construct. A secondary result documents a recognition–recall gap that leaves consistency undefined for recognized-but-unrecalled brands, concentrated among prestige labels. Per the pre-registered rule, the instrument is not adopted, and the paper specifies the mean-independence requirement any replacement must satisfy.

**Keywords:** AI Availability; AIAS; brand measurement; large language models; coefficient of variation; consistency; recall; pre-registration; negative result; mental availability

**JEL codes:** M31 (primary); L86; L15; D83; M37

**Paper status:** Working paper in the AIAS\texttrademark{} Measurement Program. Pre-registered; methodology locked at git tag `v1.7-prereg-r2`, falsification and redefinition escalation recorded at `v1.7-prereg-r3`. Data and code deposited at OSF (`osf.io/ec6wh`).

# 1. Introduction

The availability of a brand inside large language model outputs is becoming a condition of its discoverability, as conversational systems mediate a growing share of the queries that once ran through search and retail shelves. The AIAS™ measurement programme treats this as a third system of availability, parallel to the mental and physical availability that organise the Ehrenberg-Bass account of brand growth (Sharp, 2010; Romaniuk & Sharp, 2022), and constructs it empirically rather than by assertion (González Castro, 2026, SSRN 6659000). Presence, the breadth of a brand's recognition and recall across a fixed model panel, was the first component to be specified and shipped (González Castro, 2026, SSRN 6817841). The programme's roadmap places Consistency next.

Consistency is intuitively simple. A brand whose presence reads the same across every model in a panel is stable; one that surfaces strongly in some models and disappears in others is not. The coefficient of variation is the textbook scale-free measure of that dispersion, and a monotone transform of it yields a bounded score on which higher values denote greater stability. The appeal is that the quantity appears to capture something Presence does not, namely the evenness of a brand's standing rather than its level.

A second component is only worth adding if it carries information the first does not. A composite assembled from components that move together double-counts, and a consistency score that merely restates presence level would inflate the construct without enriching it. The protocol therefore pre-registered an independence criterion before any value was computed: if the consistency score correlated with Presence above a stated ceiling, it would be judged a reparametrization rather than a component, and would not be adopted. Methodology was locked at git commit, the anchored set was fixed, and the falsification rule was written into the registration.

The instrument failed that test, and the manner of its failure is the paper's contribution. The correlation with Presence is not a contingent feature of the present data but the visible trace of a mathematical identity that holds wherever mention counts are small, as they are throughout language-model output. Because the result follows from the count regime rather than from any property of these particular brands or substrates, it generalises to the broad class of dispersion-over-mean consistency metrics now appearing in commercial AI-visibility tools. The paper reports the pre-registered failure, isolates its mechanism, documents a recognition–recall asymmetry that the test exposed along the way, and states the condition a valid Consistency instrument must meet.

# 2. Method

## 2.1 The construct and the candidate instrument

Consistency is defined as the stability of a brand's recall across a fixed panel of language models. For a given brand, each model returns a recall count, and a brand whose counts cluster tightly across the panel is more consistent than one whose counts scatter. The coefficient of variation, the ratio of the standard deviation to the mean, is the conventional scale-free summary of that scatter, and the protocol mapped it to a bounded score through the transform $\text{CPC} = 1 / (1 + \text{CV})$, under which a perfectly even brand scores one and rising dispersion lowers the score toward zero.

The recall signal is the two-channel measure carried forward from the Presence protocol (González Castro, 2026, SSRN 6816340). Each model is probed in a category channel and a cultural channel, three prompts in each, so the combined count for a brand under one model is the sum of its category and cultural hits and ranges from zero to six. The six per-model counts form the observations from which the coefficient of variation is computed. Because the six models constitute the entire reference panel rather than a sample drawn from a larger population, dispersion is computed with the population standard deviation.

## 2.2 Pre-registration and the anchored set

Methodology was locked at git commit before any consistency value was computed, in keeping with the programme's pre-registration discipline (protocol series: González Castro, 2026, SSRN 6761698, 6797679, 6799479, 6810758, 6816340). The original registration named the full anchor base. A pre-computation audit of the stored recall data then established that the two-channel panel measure the instrument requires is present for only three anchored substrates: skincare, cosmetics, and automotive. The remaining substrates were excluded on data-availability grounds, and the exclusion was recorded as an amendment to the registration before computation rather than after inspection of results. One substrate carries no panel recall; three carry single-channel recall from which the combined count cannot be formed; one uses a non-canonical channel pair whose category-side construct differs from the panel standard; and one was run on an off-panel model set. The anchored set was narrowed to the three-substrate trio accordingly, matching the set used in the instrument's pilot (González Castro, 2026, SSRN 6875319). No re-acquisition was performed, and the exclusions are mechanical rather than result-driven.

## 2.3 Computation

For each brand and model, the combined recall count was formed as above, the population standard deviation and mean were taken across the six models, and the coefficient of variation was transformed to the bounded score. A floor returned as undefined any brand whose mean combined recall fell below one, on the reasoning that a stability score for a brand with essentially no recall is not interpretable. Computation reused the pilot's certified mention matchers without modification, and its output was required to reconcile with the pilot's recorded values as a regression check.

## 2.4 The independence test

The association between Consistency and Presence is the decisive quantity, since a second component is admissible only if it carries information the first does not. Presence was operationalized as the programme's canonical composite, the mean of scaled recognition breadth and the two scaled recall channels, a measure that retains spread across brands even where bare recognition saturates. Recognition-only Presence was examined in parallel. The association was measured by rank correlation, pooled across the trio and computed within each substrate, with a bias-corrected and accelerated bootstrap interval. The pre-registered rule judged the instrument non-independent, and therefore not adoptable, if the absolute correlation reached or exceeded 0.50.

## 2.5 Hypotheses

Three pre-registered claims were evaluated:

1. **H_CPC_Defined.** The score is computable for in-market brands across the trio; a material fraction returning undefined would indicate a mis-set floor.
2. **H_CPC_Dissociates.** The score is not a function of Presence, operationalized as an absolute rank correlation below 0.50; reaching the ceiling triggers escalation to redefinition rather than adoption.
3. **H_CPC_PhantomNull.** Defunct brands, which carry no current recall, return undefined under the floor.

# 3. Results

## 3.1 Computation integrity

The consistency values reconciled with the pilot's recorded output to within floating-point tolerance, a maximum absolute difference of $2\times10^{-16}$ across thirty-eight brands, and the mention matchers were the pilot's own. The findings that follow are therefore properties of the data and the instrument, not of a coding error.

## 3.2 Defunct brands (H_CPC_PhantomNull, confirmed)

The five defunct automotive brands returned no recall across the panel, fell below the floor, and were returned as undefined, exactly as predicted. The boundary rule behaves as intended: a brand with no presence yields no consistency reading rather than a spurious one.

![Defunct brands return undefined consistency. Cell-D automotive brands record zero recall across the panel and fall below the floor, shown against the in-market recall spread for reference.](../../reports/figs/v1_7/fig_03_phantom_null.pdf){#fig:phantom width=100%}

## 3.3 Recall sparsity (H_CPC_Defined, falsified)

The score was undefined for a large share of recognized brands. The pooled defined-rate was 57 percent, ranging from 42 percent in skincare through 58 percent in cosmetics to 74 percent in automotive. Inspection confirmed the undefined cases are genuine rather than matcher misses: prestige labels such as Lancôme, Chanel, and Dior Beauty register full recognition across the panel yet draw nearly no spontaneous recall, while functional and clinical brands hold category recall. The pattern is a recognition–recall gap. A brand can be universally known and still almost never named in response to a category or cultural prompt, and for such brands a recall-based stability score has nothing to measure. Under the pre-registered reading, the high undefined fraction reports this gap as a finding rather than signalling a mis-set floor.

![Many recognized brands have no defined consistency. Defined against undefined under the locked floor, by substrate; the undefined brands are recognized but rarely recalled.](../../reports/figs/v1_7/fig_01_cpc_defined.pdf){#fig:defined width=100%}

## 3.4 Consistency does not dissociate from Presence (H_CPC_Dissociates, falsified)

The recognition-only test could not be computed: recognition breadth stood at its ceiling for all thirty-eight defined brands, leaving no variance against which to correlate. Against the composite, the rank correlation was strongly positive: pooled at 0.77, with a bootstrap interval of 0.60 to 0.89 and $p = 2\times10^{-8}$, and positive within every substrate, at 0.94 in skincare, 0.85 in cosmetics, and 0.64 in automotive. The pre-registered ceiling was exceeded pooled and in each substrate. Off-diagonal occupancy was sparse, with three brands high on presence and low on consistency and three in the reverse position, out of thirty-eight.

The source of the correlation is a mechanical identity rather than a substantive relationship. At the recall counts observed, which lie between zero and six, count dispersion approximates the Poisson regime in which the standard deviation scales with the square root of the mean, so the coefficient of variation approximates the reciprocal of the square root of the mean. The consistency score is a monotone transform of the coefficient of variation and therefore moves inversely with mean recall, while mean recall is the dominant term in the composite Presence measure. The rank correlation between the coefficient of variation and mean recall was $-0.77$, equal in magnitude to the correlation between Consistency and Presence; because the score is a monotone function of the coefficient of variation, the two correlations are mirror images by construction. Consistency as specified does not measure stability independent of level. It restates level.

![Consistency tracks Presence rather than dissociating from it. Each brand's consistency score against its composite presence, by substrate, with the pooled rank correlation annotated; at recall counts between zero and six the coefficient of variation approximates the reciprocal of the square root of the mean.](../../reports/figs/v1_7/fig_02_cpc_dissociation.pdf){#fig:dissociation width=100%}

Per the pre-registered rule, an absolute correlation at or above 0.50 escalates the component to redefinition rather than adoption. That threshold was met, and the consequences are taken up next.

# 4. Discussion

## 4.1 A failure that generalizes beyond the data

The correlation between Consistency and Presence is not an accident of these three substrates. It follows from the count regime in which language-model recall data sit. Wherever mention counts are small, the standard deviation of a count tracks the square root of its mean, and the coefficient of variation falls as the mean rises. Any consistency measure built as dispersion over mean inherits this behaviour, so the result is a property of the instrument class rather than of the present panel. The implication reaches past the programme. Commercial tools that score a brand's consistency or variance of AI visibility from mention counts are, to the degree they divide dispersion by level, measuring level a second time. The appeal of such scores is their apparent orthogonality to presence; the arithmetic denies it at the counts these tools observe.

The error in the original intuition is worth naming precisely. A coefficient of variation is scale-free in its units, and scale-freeness was mistaken for independence from level. The two coincide only when counts are large enough that the mean and the dispersion vary freely of one another. At large counts the coefficient of variation does approach a level-independent quantity; at the counts a six-model panel returns, it does not. The instrument was specified for a regime it does not occupy.

## 4.2 The recognition–recall gap

The undefined fraction records a structural feature of how language models surface brands rather than a measurement nuisance. Recognition and recall come apart. A heritage or prestige label can be recognized by every model and still draw almost no spontaneous mention when a category or cultural prompt invites one, while a functional or clinical brand with a thinner public profile occupies the category's recalled set. In AI-mediated discovery the operative question is not whether a model knows a brand but whether it offers the brand unprompted, and the gap between the two is widest for the brands whose standing has historically rested on recognition. The observation sits alongside the programme's existing work on identity-driven presence and warrants its own treatment; here it explains why a recall-based stability score is undefined for so large a share of recognized brands.

## 4.3 Implication for the construct

The result narrows the design space for Consistency without closing it. It does not establish that the stability of AI presence is unmeasurable. It establishes that one natural operationalization measures level in disguise, and that any admissible replacement must be demonstrably independent of level at the counts the panel produces. The component is returned for redefinition rather than abandoned, and the empirical baseline that would have followed its adoption is deferred until a valid instrument exists.

# 5. Limitations

The demonstration rests on three substrates, the set for which the two-channel panel measure exists. Generality across the full anchor base is provisional and awaits back-fill of two-channel recall for the remaining substrates; the present claim is bounded to the trio.

The negative result is specific to the count regime the current probe design produces. A denser recall instrument, with more prompts per channel or an aggregated elicitation, would raise counts and weaken the coupling, and the coefficient of variation might recover some independence from level. The result does not assert that dispersion is uninformative at any count. It asserts that at the counts this design returns, the instrument fails. Whether counts can be raised to the required regime without prohibitive cost at panel scale is itself open, and bears on the practicality of any dispersion-based measure.

The formal independence test could not be run against a recall-free measure of Presence. Recognition breadth stood at its ceiling for every defined brand, so a recognition-only correlation was undefined, and the composite, which contains the recall channels, was the only Presence measure with usable spread. A correlation between a recall-based score and a recall-containing composite is in part expected from shared input. The conclusion does not rest on that correlation alone. The direct association between the coefficient of variation and mean recall, measured without reference to the composite, was equally strong and establishes the dependence on level directly. The shared-input concern bears on the formal test, not on the mechanism.

# 6. The redefinition mandate

The pre-registered rule converts the failed test into a specification for what follows. A Consistency instrument is admissible only if its dispersion measure is independent of level at the count magnitudes a model panel returns. Several directions meet that requirement in principle and will be pre-registered in turn rather than chosen here. Dispersion can be normalized against the maximum a count of a given mean can exhibit, which removes the Poisson floor and leaves a residual that varies freely of level. Consistency can be defined on the shape of the cross-model distribution through a concentration or entropy measure rather than on the ratio of two moments. Agreement among models on a brand's relative standing, rather than the spread of its counts, can be scored with a rank-agreement statistic, which is not coupled to level in the same manner. Each carries its own assumptions and failure modes, and each must clear the same independence test before adoption.

The recognition–recall gap raises a second design question any Consistency component must answer. A score undefined for a large share of recognized brands is either reporting a real gap or excluding a population a stability measure ought to cover, and the choice between those readings turns on what Consistency is meant to certify. That question is left to the redefinition.

The escalation routes to the next methodology lock. The empirical baseline that would have applied the component across the anchor base is held until the redefinition yields an instrument that passes the independence requirement.

# Declarations {-}

**Conflict of interest.** The author is employed by Samsung Electronics America. Samsung markets no consumer brands in the skincare or cosmetics categories examined. In automotive, Samsung does not market vehicle marques of the kind measured here, though affiliated units participate in the automotive supply chain (Harman International in connected-vehicle and audio systems; Samsung SDI in vehicle batteries); this is disclosed for completeness. The employer had no role in the study's design, execution, analysis, or decision to publish, and the research is conducted independently through Third System™.

**Funding.** Self-funded.

**Ethics.** Not applicable; no human subjects. The study uses public APIs and language-model prompts.

**Data and code availability.** Pre-registration artifacts, scoring code, the scored dataset, and figures are deposited at OSF (`osf.io/ec6wh/methodology/v1_7`). Consistency values reconcile with the pilot's recorded output to a maximum absolute difference of $2\times10^{-16}$.

# References {-}

González Castro, P. U. (2026). *The third system: foundational theory.* SSRN Working Paper 6659000.

González Castro, P. U. (2026). *AIAS Presence Measurement Protocol, v1.6.* SSRN Working Paper 6816340.

González Castro, P. U. (2026). *Coefficient-of-variation consistency: instrument-specification pilot (v0.30).* SSRN Working Paper 6875319.

González Castro, P. U. (2026). *AIAS 1.0: the Presence component.* SSRN Working Paper 6817841.

González Castro, P. U. (2026). *The four-regime taxonomy (Protocol v1.2).* SSRN Working Paper 6761698.

González Castro, P. U. (2026). *AIAS Presence Measurement Protocol, v1.3 (Phase A pivot-validation).* SSRN Working Paper 6797679.

González Castro, P. U. (2026). *AIAS Presence Measurement Protocol, v1.4 (multi-component construct).* SSRN Working Paper 6799479.

González Castro, P. U. (2026). *AIAS Presence Measurement Protocol, v1.5 (multi-statistic C₂ and two-channel recall).* SSRN Working Paper 6810758.

Romaniuk, J., & Sharp, B. (2022). *How brands grow: Part 2* (Rev. ed.). Oxford University Press.

Sharp, B. (2010). *How brands grow: What marketers don't know.* Oxford University Press.
