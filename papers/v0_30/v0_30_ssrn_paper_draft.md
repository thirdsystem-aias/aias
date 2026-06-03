---
title: "AI Availability is Not Reducible to Recognition Memory --- and is Underpowered Against Familiarity at n = 24"
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
  Figures expected at reports/figs/chart_28_*.pdf (adjust the path if the
  build runs from a directory other than the repo root).
  Titlepage is the first body block; Abstract is forced to page 2.
-->

\begin{titlepage}
\setstretch{1.0}
\setlength{\parskip}{0pt}
\centering
\vspace*{1.2cm}

{\LARGE\bfseries AI Availability is Not Reducible to Recognition Memory ---\\[2pt] and is Underpowered Against Familiarity at \textit{n} = 24\par}

\vspace{0.5cm}
{\large\itshape A pre-registered discriminant-validity test of AIAS\texttrademark{} Presence against human brand familiarity and recognition sensitivity\par}

\vspace{0.4cm}
{\normalsize Working Paper \textperiodcentered{} Version 1 \textperiodcentered{} Designed-for-Test (Technology)\par}
{\normalsize AIAS Presence Measurement Protocol \textperiodcentered{} Construct-Validity Phase CV.04 (v0.30)\par}

\vspace{1.0cm}
{\large Pablo Ulpiano González Castro\par}

\vspace{0.3cm}
{\normalsize MPS Branding Program, School of Visual Arts, New York, NY\\(primary academic affiliation)\par}
{\normalsize Third System\texttrademark{} --- research entity; data archive and methodology venue\par}

\vspace{0.5cm}
{\small Correspondence: pablou@pablou.com \textperiodcentered{} pablou.com\par}
{\small ORCID: 0009-0003-8968-9990\par}

\vspace{1.0cm}
{\small Pre-registration: OSF \texttt{osf.io/ec6wh} \textperiodcentered{} tags \texttt{v0.30-prereg-r1 / r2}\\
Data, scoring, and verdicts deposited under \texttt{osf.io/ec6wh} (v30).\par}

\vfill
{\footnotesize June 2026\par}
\end{titlepage}

# Abstract {-}

AI Availability --- the degree to which a brand is surfaced, recognized, and recalled by large language models --- has been proposed as a third measurable layer of brand availability alongside mental and physical availability. For the construct to earn that status it must be shown to be distinct from the human memory measures it superficially resembles. This paper reports a pre-registered discriminant-validity test of the AIAS\texttrademark{} Presence component against two human brand norms drawn from the published BRAND database: familiarity (1--7) and recognition sensitivity (\textit{d}′). Presence was composed blind from a six-model panel over 24 technology brands stratified by familiarity, joined to the validator only at a one-shot scoring step. Against recognition sensitivity, Presence is discriminant (Spearman ρ = 0.379, |ρ| < 0.50; BCa 95% CI upper 0.714 excludes the 0.74 reducibility threshold) --- CONFIRMED, though the interval is wide. Against familiarity the point estimate sits in the partial band (ρ = 0.593) but the BCa interval [0.179, 0.832] spans all three pre-registered bands, so the locked rule returns UNDETERMINED rather than a finding. A descriptive within-panel dissociation is full and bidirectional: Presence amplifies core-technology brands and suppresses consumer-famous but non-core-technology brands relative to familiarity. The enterprise-heavy panel and consumer-framed recall cues floored the recall channel, reducing Presence toward its recognition component; the familiarity question therefore remains open and is flagged for a higher-powered follow-up. The result pairs with the convergent (v0.25) and Amazon-BSR discriminant (v0.26) evidence as one cell of a multitrait--multimethod construct-validity program.

**Keywords:** AI availability; large language models; brand measurement; construct validity; discriminant validity; recognition memory; mental availability; AIAS; share of model; pre-registration

**JEL codes:** M31 (primary); L86; L15; D83; M37

**Paper status:** Pre-registered, blind-acquired, one-shot scored. All hypotheses, thresholds, panel, and the Presence definition were frozen at git tags before any model was queried; the validator was joined only at scoring. This is a single empirical cell of the AIAS construct-validity program, not a standalone validation of the full construct.

# 1. Introduction

Ehrenberg-Bass theory frames brand growth through two forms of availability: mental availability, the propensity of a brand to be thought of in buying situations, and physical availability, the ease of finding and buying it (Sharp 2010; Romaniuk & Sharp 2022). A third layer has been proposed --- AI Availability, the propensity of a brand to be surfaced, recognized, and recalled by the large language models that increasingly mediate discovery and recommendation (González Castro 2026b). The AIAS\texttrademark{} (AI Availability Score) program operationalizes the first observable slice of this layer as **Presence**: a composite of whether models recognize a brand in its category and whether they recall it under category and cultural cues.

A new construct earns its place only by surviving construct validation. Convergent evidence has been reported: AIAS Presence correlates with an external interest signal (Google Trends) at ρ ≈ 0.74 (González Castro 2026c). Convergence alone is insufficient. A measure that merely re-indexes how well known a brand already is would be redundant with existing, cheaper human norms --- it would have convergent validity and no discriminant validity. The multitrait--multimethod logic of Campbell and Fiske requires that a measure correlate less with conceptually distinct traits than with itself across methods (Campbell & Fiske 1959). Two human brand norms make the sharpest adversarial tests: **familiarity**, a direct fame rating, and **recognition sensitivity** (\textit{d}′), a signal-detection measure of how reliably people distinguish a real brand from a foil.

This paper reports the discriminant cell of that program (phase CV.04). The pre-registered question is narrow and falsifiable: *is AIAS Presence reducible to human familiarity and to human recognition sensitivity?* The category was chosen to be adversarial. Technology brands are the case where AI fame and human fame should align most tightly --- model training corpora are saturated with technology discourse --- so if Presence is going to collapse into a familiarity proxy anywhere, it should collapse here. A discriminant result on an adversarial substrate is stronger than one on a forgiving one; an inconclusive result on it is honest about the limits of the present sample.

# 2. Method

## 2.1 Design and pre-registration

The study follows the AIAS Presence Measurement Protocol v1.6 (González Castro 2026a). Every hypothesis, threshold, the brand panel, the validator, and the Presence composition rule were committed to git and pushed before any model was queried (tag `v0.30-prereg-r1`); a single amendment fixing a normalization denominator was committed before acquisition (tag `v0.30-prereg-r2`, see §2.5). Acquisition was run blind to the validator, and scoring --- the join of Presence to the human norms --- was executed exactly once, after the data were locked and deposited.

## 2.2 Validator and panel

The validator is the published BRAND database, which provides familiarity ratings (1--7) and recognition sensitivity (\textit{d}′) from a signal-detection task for the Brand Finance US 500 roster (Raffaelli et al. 2025). From its technology category (80 brands), 70 had complete familiarity and \textit{d}′ data. One eligible brand, Harman, was removed by a frame-level conflict-of-interest screen (Samsung ownership; see Declarations), leaving 69. A panel of 24 was drawn stratified by familiarity tertile (eight per tertile) with a fixed random seed (280400). The panel spans the full familiarity range (1.00--6.83) and includes both consumer-facing brands (Apple, Google, Microsoft, Netflix, Instagram) and enterprise or industrial brands (Corning, VMware, HPE, NetApp, Jabil, Pitney Bowes, Parker-Hannifin, Lam Research, 3M).

## 2.3 Presence composition

Presence was composed from a fixed six-model panel held constant across the program since v0.17: `claude-opus-4-5`, `claude-sonnet-4-5`, `gpt-4o`, `gpt-4o-mini`, `gemini-2.5-flash`, and `gemini-2.5-flash-lite`. Two phases were run.

*Phase A --- recognition.* Each brand was put to each model with a single recognition probe ("Is the brand *X* commonly recognized as a technology brand? Answer yes or no."). The brand's recognition count $C_P$ is the number of models answering yes (0--6). This yields 24 × 6 = 144 probes.

*Phase B --- recall.* Six category-level recall frames were posed to each model, three keyed to category quality ($R_{cat}$: best / expert-chosen / highest-quality technology brands) and three to cultural salience ($R_{cult}$: most talked-about / biggest cultural footprint / most iconic). A brand scores a recall point each time it is named in a frame × model response, to a maximum of 18 per channel (3 frames × 6 models). This yields 6 × 6 = 36 recall queries.

Presence is the equal-weight mean of the three fraction-of-maximum components, on a 0--100 scale:

$$\text{Presence} = \frac{1}{3}\left(\frac{C_P}{6} + \frac{R_{cat}}{18} + \frac{R_{cult}}{18}\right)\times 100.$$

This is the same composition that produced the convergent ρ ≈ 0.74 anchor in v0.25; it is forced by commensurability, not chosen post hoc.

## 2.4 Hypotheses and decision rule

Two gating hypotheses were registered, each testing reducibility of Presence to a human norm via Spearman rank correlation, banded on the absolute coefficient |ρ|:

- **H_Disc_Familiarity** (primary) --- Presence vs familiarity.
- **H_Disc_Recognition** (secondary) --- Presence vs \textit{d}′.

Bands: |ρ| < 0.50 → **CONFIRMED** (discriminant); 0.50 ≤ |ρ| < 0.74 → **PARTIAL**; |ρ| ≥ 0.74 → **FALSIFIED** (reducible). The 0.74 ceiling is the convergent benchmark: a discriminant correlation at or above the level the measure shows with its *own* convergent criterion would indicate redundancy. Verdicts are gated on the point estimate. A BCa bootstrap 95% confidence interval (10,000 resamples, seed 280400) is reported as non-gating context, with two flags: `ci_excludes_reducibility` (CI upper < 0.74) and a provisional flag for any CONFIRMED whose CI upper reaches 0.74. A locked override returns **UNDETERMINED** when *n* < 12 or when the CI spans all three bands.

A third, descriptive hypothesis, **H_Dissociation**, was registered as non-gating and excluded from the headline: the count of brands whose within-panel standardized Presence and familiarity diverge by more than one standard deviation in either direction (amplified, Presence ≫ familiarity; suppressed, familiarity ≫ Presence). It is mechanically coupled to the primary correlation and is reported as corroborating texture, not independent evidence.

A directional prediction was registered: ρ in the 0.30--0.60 range (partial, modal), reflecting the adversarial choice of Technology.

## 2.5 Normalization amendment

The r2 amendment recorded one deviation. The v0.25 anchor normalized recall on a 36-frame Phase B; Protocol v1.6 canon is a 6-frame battery with three frames per channel (maximum 18 per channel). The r1 design correctly implements the v1.6 battery; the amendment pinned the bridge to normalize recall on the v1.6 maximum (/18), preserving the equal-weight semantic. The benchmark comparison to the v0.25 convergent anchor is therefore approximate on cue breadth (the anchor used more cues per channel), a point carried to §5.

# 3. Results

The panel joined 24-to-24 against the validator with no name-mismatch drops. Presence ranged from 0.0 (QVC) to 100.0 (Apple), with Microsoft (94.4) and Google (85.2) next; recognition $C_P$ varied genuinely across the panel (QVC 0, Flex and Whirlpool 1, Jabil 2, several enterprise brands 3--4, the consumer leaders 6), so the test is well powered on the predictor even where recall is sparse.

\begin{figure}[H]
\centering
\includegraphics[width=0.95\textwidth]{reports/figs/chart_28_verdict_bands.pdf}
\caption{Point |ρ| with BCa 95\% confidence interval for each gating hypothesis, against the three pre-registered bands. Familiarity's interval straddles all three bands (UNDETERMINED); Recognition's stops left of the 0.74 line (CONFIRMED). \textit{n} = 24, seed 280400.}
\end{figure}

**Recognition (secondary) --- CONFIRMED.** Presence correlates with recognition sensitivity at ρ = 0.379 (|ρ| < 0.50), inside the discriminant band. The BCa interval is [−0.076, 0.714]; its absolute upper bound (0.714) sits below the 0.74 reducibility threshold, so `ci_excludes_reducibility` is true and the verdict is not provisional. The verdict is clean on the locked rule, but the interval is wide and reaches into the partial band --- this is confirmed discriminance, not a tight one, and should be read as such.

**Familiarity (primary) --- UNDETERMINED.** The point estimate is ρ = 0.593, inside the partial band, consistent with the registered prediction. But the BCa interval is [0.179, 0.832]: its lower bound falls in the CONFIRMED band and its upper bound in the FALSIFIED band, so the interval spans all three. The locked override fires and returns UNDETERMINED, overriding the partial point verdict. At *n* = 24 the data cannot distinguish a discriminant Presence from one reducible to familiarity; the honest reading is that the primary question is unresolved at this sample size, not that a partial relationship has been established.

\begin{figure}[H]
\centering
\includegraphics[width=0.95\textwidth]{reports/figs/chart_28_discriminant_scatters.pdf}
\caption{Presence against human familiarity (left) and recognition sensitivity \textit{d}′ (right), 24 brands. ρ is rank-based (Spearman); axes show raw values. Labelled points are the dissociation crossers.}
\end{figure}

**Dissociation (descriptive) --- FULL.** Eleven of 24 brands cross the ±1 SD threshold in both directions (population SD, within-panel standardization). Four are amplified --- Apple (+1.23), Microsoft (+1.15), HPE (+1.07), NetApp (+1.07) --- all core-technology brands the panel surfaces more strongly than human familiarity does. Seven are suppressed --- Netflix (−1.04), Instagram (−1.05), Uber (−1.25), Airbnb (−1.05), Whirlpool (−1.71), 3M (−1.03), QVC (−1.56). The suppressed set splits into consumer-famous but non-core-technology brands (Netflix, Instagram, Uber, Airbnb) and human-familiar but low-AI-presence brands (Whirlpool, 3M, QVC). The pattern is systematic, not noise, and it reconciles with the recall-channel evidence: Netflix and Instagram surfaced under the cultural cues ($R_{cult}$) but not the quality cues ($R_{cat}$), while several enterprise brands showed the reverse.

\begin{figure}[H]
\centering
\includegraphics[width=0.78\textwidth]{reports/figs/chart_28_dissociation.pdf}
\caption{Within-panel standardized difference z(Presence) − z(familiarity) for all 24 brands, with ±1.0 thresholds. Amplified brands (Presence ≫ familiarity) and suppressed brands (familiarity ≫ Presence). Descriptive and non-gating.}
\end{figure}

Table 1 records the pre-registered outcomes.

| Hypothesis | Role | ρ (signed) | \|ρ\| band | BCa 95% CI | Verdict |
|---|---|---|---|---|---|
| H_Disc_Familiarity | Primary (gating) | 0.593 | PARTIAL (point) | [0.179, 0.832] | **UNDETERMINED** |
| H_Disc_Recognition | Secondary (gating) | 0.379 | CONFIRMED | [−0.076, 0.714] | **CONFIRMED** |
| H_Dissociation | Tertiary (descriptive) | --- | --- | --- | **FULL** (11/24) |

: Pre-registered outcomes. Verdicts gated on the point estimate; the UNDETERMINED override fires when the BCa interval spans all three bands. Dissociation is non-gating and excluded from the headline.

# 4. Discussion

The two gating verdicts describe a measure that is distinct from one human norm and unresolved against the other --- and the reason for the asymmetry is the same fact in both cases.

The panel was enterprise-heavy by construction (a familiarity-stratified draw from a category whose mass is industrial and B2B brands), and the recall frames were consumer-oriented ("best technology brands," "most iconic"). Those frames do not surface Jabil or Pitney Bowes or Parker-Hannifin. Recall therefore floored for most of the panel, and where recall floors, Presence reduces toward its recognition component $C_P$ (Figure 4). What the study actually tested, for most brands, was AI recognition against the two human norms.

\begin{figure}[H]
\centering
\includegraphics[width=0.95\textwidth]{reports/figs/chart_28_presence_composition.pdf}
\caption{Presence decomposed into its three components for each brand. For most of the enterprise-heavy panel the recall channels contribute little and Presence reduces toward the recognition component $C_P$.}
\end{figure}

Read through that lens, the recognition result is the more interesting one. AI recognition --- does a model class a brand as a technology brand --- diverges from human recognition sensitivity (\textit{d}′) at ρ = 0.379. The two recognition measures are only moderately related; the model's category judgement is not a restatement of how reliably a person tells the brand from a foil. That is a substantive discriminant finding, and the wide interval is the honest qualifier on it.

The familiarity result is what an underpowered adversarial test should look like when it refuses to overclaim. The point estimate leans toward partial discriminance, exactly as predicted, but the interval is too wide to exclude either a genuinely discriminant Presence or one that collapses into familiarity. The pre-registered override did its job: it converted a tempting partial point estimate into an explicit "unresolved." A study that reported ρ = 0.59 as a partial finding here would be reading more into 24 brands than 24 brands can bear.

The dissociation supplies the qualitative complement the correlation cannot. Presence and familiarity do not merely correlate imperfectly; they diverge in a patterned way. The model layer over-weights core-technology identity (Apple, Microsoft, the enterprise infrastructure brands) and under-weights brands that are culturally famous without being category-canonical technology (Netflix, Instagram, Uber, Airbnb). This is the kind of structured divergence one would expect if AI Availability indexes something other than fame --- but it is mechanically coupled to the primary correlation and is offered as illustration, not proof.

Placed in the construct-validity program, CV.04 contributes one multitrait--multimethod cell: discriminant from recognition sensitivity (confirmed), discriminant from familiarity (unresolved, flagged for replication at higher power). It sits beside the convergent evidence of v0.25 (Presence × Google Trends) and the discriminant evidence of v0.26 (Amazon BSR discriminant), which together form a Campbell--Fiske pairing of convergent and discriminant tests across methods.

# 5. Limitations

Three limitations bound the reading, and they compound.

*Sample size.* At *n* = 24 the BCa intervals are wide enough that the primary hypothesis cannot be resolved. This is the binding constraint. The panel size was fixed by the requirement to stratify a single category by familiarity tertile while holding the six-model panel and probe battery constant; resolving the familiarity question requires a larger panel, which a future phase should supply.

*Recall floor and substrate.* The enterprise-heavy Technology panel under consumer-framed recall cues floored the recall channels, so Presence reduced toward recognition for most brands. The discriminant tests therefore largely evaluated AI recognition, not the full tri-component Presence construct, against the human norms. A consumer-category panel with richer recall would test the full construct against familiarity more cleanly, and is the natural next substrate.

*Benchmark commensurability.* The 0.74 reducibility threshold is the v0.25 convergent anchor, which normalized recall over a wider per-channel cue set than the v1.6 battery used here. The threshold comparison is therefore approximate on cue breadth. It is used as a fixed, pre-registered decision boundary, not as a precise like-for-like quantity.

# 6. Future Research

The immediate priority is a higher-powered replication of the familiarity test on a consumer category where recall does not floor, so that the full Presence composite --- not its recognition component alone --- is what confronts familiarity. Two further cells would complete the discriminant matrix: a direct mental-availability comparison using category-entry-point measures, which requires a brand-level dataset the present study could not source without primary human-subjects collection; and a recognition-sensitivity replication on a substrate where AI and human recognition are expected to diverge more sharply. Consolidating these cells is the gate to expanding AIAS beyond the Presence component to the full multi-component composite.

# References {-}

Campbell, D. T., & Fiske, D. W. (1959). Convergent and discriminant validation by the multitrait-multimethod matrix. *Psychological Bulletin*, 56(2), 81--105.

Efron, B. (1987). Better bootstrap confidence intervals. *Journal of the American Statistical Association*, 82(397), 171--185.

González Castro, P. U. (2026a). *AIAS Presence Measurement Protocol, Version 1.6.* SSRN Working Paper 6816340.

González Castro, P. U. (2026b). *AIAS 1.0 Synthesis.* SSRN Working Paper 6817841.

González Castro, P. U. (2026c). *Convergent validity of AIAS Presence (B2B SaaS).* SSRN Working Paper (v0.25).

González Castro, P. U. (2026d). *Amazon BSR discriminant validity of AIAS Presence.* SSRN Working Paper 6847678 (v0.26).

Raffaelli, Q., Bocchi, A., Estes, Z., & Adelman, J. S. (2025). The BRAND database: Familiarity and recognition norms for the Brand Finance US 500. *Behavior Research Methods*, 57(1), 17.

Romaniuk, J., & Sharp, B. (2022). *How Brands Grow: Part 2* (rev. ed.). Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know.* Oxford University Press.

# Declarations {-}

**Conflict of interest.** The author is employed by Samsung Electronics America. Samsung had no role in the design, conduct, analysis, or reporting of this study. To prevent any conflict at the data level, the Samsung-owned brand Harman was removed from the eligible frame by a pre-registered screen before panel sampling.

**Funding.** Self-funded.

**Ethics.** Not applicable; no human subjects. Data are public model outputs queried through provider APIs and a published, de-identified human-norms dataset (the BRAND database).

**Pre-registration and data availability.** Pre-registration, acquisition data, scoring code, and verdicts are deposited at OSF (`osf.io/ec6wh`, v30), with the design frozen at git tags `v0.30-prereg-r1` and `v0.30-prereg-r2` prior to acquisition and the result at `v0.30-results-locked`.

# Author Information {-}

Pablo Ulpiano González Castro --- MPS Branding Program, School of Visual Arts, New York, NY (primary academic affiliation); Third System\texttrademark{} (research entity; data archive and methodology venue). Correspondence: pablou@pablou.com \textperiodcentered{} pablou.com. ORCID: 0009-0003-8968-9990.
