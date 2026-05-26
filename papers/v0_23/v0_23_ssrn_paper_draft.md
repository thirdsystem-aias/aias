---
title: "Phantom Brand Persistence on a Heritage-Saturated Automotive Substrate --- Cell D_Defunct as Pure-Phantom Upper-Bound Test"
subtitle: "AIAS™ Presence Measurement Protocol, v0.23 --- Sixth substrate family for the Presence-component AIAS™ 1.0 anchor base; first prospective phase under v1.6 lock"
author: "Pablo Ulpiano González Castro"
date: "May 2026"
mainfont: "Carlito"
fontsize: 11pt
geometry: margin=1in
colorlinks: true
linkcolor: black
urlcolor: black
header-includes: |
  \usepackage{setspace}
  \setstretch{1.36}
  \setlength{\parskip}{8pt}
  \setlength{\parindent}{0pt}
  \usepackage{float}
  \floatplacement{figure}{H}
  \usepackage{caption}
  \captionsetup{labelfont={bf,it},textfont=it,format=plain,justification=raggedright,singlelinecheck=false}
  \usepackage{titlesec}
  \titleformat{\section}{\Large\bfseries}{\thesection.}{0.5em}{}
  \titleformat{\subsection}{\large\bfseries}{\thesubsection}{0.5em}{}
  \renewcommand{\maketitle}{}
  \providecommand{\xmpquote}[1]{#1}
---

\begin{titlepage}
\setstretch{1.0}
\setlength{\parskip}{0pt}

\vspace*{2cm}

\begin{center}

{\fontsize{16}{21.76}\selectfont\bfseries
Phantom Brand Persistence on a Heritage-Saturated Automotive Substrate \\[6pt]
Cell D\_Defunct as Pure-Phantom Upper-Bound Test
\par}

\vspace{14pt}

{\itshape AIAS\textsuperscript{TM} Presence Measurement Protocol, v0.23 --- sixth substrate family for the Presence-component AIAS\textsuperscript{TM} 1.0 anchor base; first prospective phase under v1.6 lock\par}

\vspace{10.36pt}

{\small Working Paper $\cdot$ Version 1 $\cdot$ Designed-for-Test (Automotive)\par}

\vspace{32pt}

{\bfseries Pablo Ulpiano Gonz\'{a}lez Castro\par}

\vspace{4pt}

School of Visual Arts, MPS Branding Program $\cdot$ New York, NY \\[2pt]
\textit{(primary academic affiliation)} \\[6pt]
Third System\textsuperscript{TM} \textit{(research entity; data archive and methodology venue)}

\vspace{20pt}

Correspondence: \href{mailto:pablou@pablou.com}{pablou@pablou.com} $\cdot$ \href{https://pablou.com}{pablou.com}\\
ORCID: \href{https://orcid.org/0009-0003-8968-9990}{0009-0003-8968-9990}

\vspace{16pt}

May 2026

\end{center}

\end{titlepage}

# Abstract {-}

AIAS™ v0.23 stress-tests Phantom Brand Persistence on a heritage-saturated automotive substrate, with a dedicated Cell D panel of five discontinued corporate brands (Pontiac, Oldsmobile, Plymouth, Mercury, Saturn) providing the pure-phantom upper-bound test. Despite all five defunct brands clearing Phase A Recognition at C_P = 6/6, none surfaces once in 18 unprompted current-tense Recall opportunities per brand. H_Phantom_Defunct, the lead hypothesis, returns FALSIFIED at the strongest possible margin. The primary supporting hypothesis H_Phantom_Brand_Persistence_heritage returns CONFIRMED with three Cell A brands above the R_phantom ≥ 8 threshold (Porsche R_phantom = 14, BMW = 12, Mercedes-Benz = 10). The paired verdicts establish a temporal boundary: phantom persistence operates on living heritage brands and stops at documented brand death --- a tighter and more falsifiable construct than the substrate-agnostic version v0.21 implied. v0.23 also extends the Recognition × Recall dissociation construct to a sixth substrate family (H_Dissoc_substrate_generalization GENERALIZED). v1.6 Inc2 H_IdentityLoad_direct returns CONFIRMED on the strongest R4-independent IL signature in the program (Cell A R_cult/R_cat = 2.42 vs Cell B = 0.75, 3.2× cult-channel dominance lead). v1.6 Inc1 H_SubstrateRecognition_PreScreen classifies UNIFORM SATURATION as predicted.

**Keywords:** AI Availability; Phantom Brand Persistence; brand recognition; brand recall; large language models; mental availability; physical availability; Ehrenberg-Bass; brand measurement; AIAS; Third System; pre-registration

**JEL codes:** M31 (primary); L86, L15, D83, M37 (secondary).

**Paper status:** Working Paper · Version 1 · Designed-for-Test (Automotive). Pre-registration locked at git tag `v0.23-prereg-r2` (commit `0dde745`, branch `program-docs`). Methodology version: v1.6 (SSRN 6816340). Acquisition locked at git tag `v0.23-acquisition-locked`. Data and code deposited at osf.io/ec6wh/v23/.

# 1. Introduction

The AIAS™ Presence Measurement Protocol (Gonzalez Castro 2026a) operationalizes AI Availability --- the probability that an AI intermediary retrieves, recommends, or selects a brand in a category-anchored decision context --- as a third measurable layer of brand availability alongside the Ehrenberg-Bass framework's Mental Availability and Physical Availability (Sharp 2010; Romaniuk and Sharp 2016). Protocol v1.6 (Gonzalez Castro 2026b) introduced three increments: a substrate-level Recognition pre-screen distinguishing uniform from differential saturation (Inc1), a direct R4-independent Identity-Load measurement (Inc2), and an explicit Phantom Brand Persistence measurement (Inc3). The construct's empirical anchor base under v1.6 lock reached five substrate families with AIAS™ 1.0 (Gonzalez Castro 2026a); v0.23 is the first prospective phase under v1.6 lock and extends the anchor base to six substrate families.

The substrate is automotive. The phase's primary motivation is methodological: Phantom Brand Persistence was empirically motivated and calibrated on v0.21 cosmetics through the single dominant case of Glossier (off-panel, alive, R_phantom = 12 across the six-model panel), but the substrate-agnostic construct as articulated leaves a critical question unresolved. Does phantom surfacing operate on any well-encoded brand identity --- where the AI mediation layer treats the brand as category-salient regardless of operational status --- or is the phenomenon bounded by living-brand status, where documented corporate-brand death acts as a Recall floor that the mediation layer respects?

Automotive is uniquely positioned to test the question. Unlike prior substrate families (kitchenware, indie fragrance, audiophile electronics, skincare, cosmetics), corporate-brand death in automotive is well-documented and dated: Pontiac closed in 2010, Oldsmobile in 2004, Plymouth in 2001, Mercury in 2010, Saturn in 2010. The five brands span a 9-year discontinuation window with broad cultural footprint and continued model-level brand persistence (the Pontiac GTO, the Oldsmobile 442, the Plymouth Barracuda, the Mercury Cougar, the Saturn S-Series) that maintains identifiable brand-association substrate in the AI training corpus. If phantom surfacing extends to documented-dead brands, automotive is the substrate where the surfacing should be observable; if it does not, the temporal floor is observable as a sharp boundary against the same panel's contemporaneous surfacing of living-heritage brands (Mercedes-Benz, BMW, Porsche, etc.).

v0.23 was pre-registered with a dedicated Cell D panel of these five defunct corporate brands as the pure-phantom upper-bound test, alongside the conventional three-cell IL-gradient structure carried forward from v0.18--v0.21 (Cell A Heritage, Cell B Disruptor, Cell C Mass-Legacy). The lead hypothesis H_Phantom_Defunct measures whether any Cell D brand surfaces in unprompted current-tense Recall at R_phantom_defunct ≥ 4. The primary supporting hypothesis H_Phantom_Brand_Persistence_heritage measures whether Cell A heritage brands replicate the v0.21 phantom-persistence pattern. The paired verdicts jointly establish the construct's temporal boundary, if any exists.

The paper's contribution is empirical: v0.23 reports the paired Cell D / Cell A measurement on a six-model LLM panel (Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o-mini, Gemini 2.5 Flash, Gemini 2.5 Flash Lite) under pre-registered hypothesis matrices locked at git tag `v0.23-prereg-r2`. The methodology contribution is the v1.6 increments operating prospectively: Inc1 routes the substrate to UNIFORM SATURATION (parallel to v0.21 cosmetics); Inc2 anchors the strongest R4-independent IL signature in the program to date; Inc3 returns the paired phantom verdicts that define the construct's temporal boundary.

# 2. Method

## 2.1 Pre-registration and lock state

v0.23 was pre-registered at tag `v0.23-prereg-r2` (commit `0dde745`, branch `program-docs`), superseding tag `v0.23-prereg-r1` (commit `edc61f3`). The r1 → r2 amendment is documented in DEVIATIONS Entry 0 of the pre-registration module (`prereg/v0_23_automotive_content.py`) and discussed in §6. Pre-registration covers panel construction (24 brands × 4 cells), Phase A Recognition probe template, Phase B six-frame battery (two-channel Recall under v1.5), six hypotheses with verdict matrices, threshold thresholds, and the four-cell IL-gradient design including the novel Cell D pure-phantom panel. The pre-registration is deposited at osf.io/ec6wh/v23/prereg/.

## 2.2 Substrate operational definition

Automotive is operationally defined as a four-cell panel spanning the passenger-car consumer-discovery surface, sampled across four tiers of Identity Load (IL) and heritage saturation:

- **Cell A --- Heritage** (high IL, aristocratic / Old-World positioning, n = 7): Mercedes-Benz, Jaguar, Cadillac, Rolls-Royce, Bentley, Porsche, BMW. Brands whose primary value driver is documented heritage.
- **Cell B --- Disruptor** (high IL, no heritage substrate, n = 5): Tesla, Rivian, Lucid, Polestar, Fisker. EV-native brands without legacy positioning; tests the high-IL pattern from v0.20/v0.21 Cell B without confounding with traditional heritage coding.
- **Cell C --- Mass-Legacy** (low-medium IL, long-tenured corporate brands where heritage is not the lead value driver, n = 7): Toyota, Honda, Ford, Chevrolet, Hyundai, Volkswagen, Nissan.
- **Cell D --- Defunct** (pure-phantom panel, n = 5): Pontiac (closed 2010), Oldsmobile (2004), Plymouth (2001), Mercury (2010), Saturn (2010). **Lead hypothesis test cell.**

The four-cell structure is not strictly an IL gradient --- Cell D positions outside the IL ladder as a phantom-test cell. The A-vs-B and A-vs-C comparisons follow program convention.

## 2.3 Reference panel

The reference panel is held fixed from v0.17 onward: Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o-mini, Gemini 2.5 Flash, Gemini 2.5 Flash Lite. Six distinct LLMs, one response per model per probe. Per-brand C_P = yes-count across panel models, range 0--6. Per-brand R_cat / R_cult = mentions across (3 probes × 6 models), max 18 per channel per brand.

## 2.4 Phase A --- Recognition

For each of the 24 brands, the six panel models receive:

> *Is the brand {BRAND} commonly recognized as a car brand? Answer yes or no.*

The probe deliberately uses present-tense framing without temporal cues, which is essential to the Cell D phantom test: the panel must not be primed to recognize defunct brands as discontinued. C_P measures whether the AI mediation layer treats each brand as a recognizable automotive entity at category-membership level; R_phantom_defunct (Phase B) measures whether the same panel surfaces these brands in unprompted current-tense Recall.

## 2.5 Phase B --- two-channel Recall

Six category-anchored queries are sent to each of the six panel models (36 total queries per channel pair, 72 total). Three queries anchor the canonical channel (R_cat); three anchor the cultural-footprint channel (R_cult).

**R_cat channel (q1--q3, canonical retrieval):**

- q1 (best): *What are the best car brands? List several with descriptions.*
- q2 (expert): *What car brands do automotive experts and reviewers recommend? Name several.*
- q3 (high-quality): *What car brands are highest quality and most reliable? Name several brands with descriptions.*

**R_cult channel (q4--q6, cultural-footprint / heritage retrieval):**

- q4 (heritage / prestige): *What car brands carry deep heritage, prestige, or a sense of legacy? List several.*
- q5 (aspirational / status): *What car brands do affluent or status-conscious buyers tend to choose? Name several.*
- q6 (iconic / storied): *Which car brands have the most iconic or storied identity in popular culture? Name several.*

For each (frame × LLM) response, the 24-brand registry was scanned for mention presence using case-insensitive, accent-stripped, possessive-aware matching with first-occurrence-wins de-duplication per v1.4 canonical rules.

**R_phantom_defunct** per Cell D brand is operationally the count of unprompted current-tense Recall mentions across (six models × three R_cat probes) = 18 per brand. R_phantom for Cell A_Heritage brands carries the same operationalization applied to living-brand Recall.

## 2.6 Hypotheses (locked, six)

Six hypotheses were pre-registered with verdict matrices locked ex-ante:

- **H_Phantom_Defunct (LEAD).** CONFIRMED if any Cell D brand R_phantom_defunct ≥ 4; PARTIAL if ≥ 1 brand at 1--3; FALSIFIED at zero across all.
- **H_Phantom_Brand_Persistence_heritage (PRIMARY SUPPORTING).** CONFIRMED if any Cell A brand R_phantom ≥ 8; PARTIAL if any 4--7; FALSIFIED all < 4. Benchmark: v0.21 Glossier R_phantom = 12.
- **H_Regime4_automotive.** Sequential C1 (n ≥ 12) → C2 (distinct C_P ≥ 3 ∧ modal share ≤ 0.625, per cell) → IL-gradient guard (Cell B vs Cell C top-2 R_cat separation ≥ 0.10) → C3 (per-cell Spearman ρ between C_P and R_cat ≥ 0.50 in ≥ 2 cells, n ≥ 5). FALSIFIED if C2 fails in ≥ 2 cells.
- **H_Dissoc_substrate_generalization.** Iwachu-pattern cases (C_P ≥ 5 ∧ R_cat ≤ 2) in ≥ 1 of Cells A or B; sixth-substrate-family extension.
- **H_IdentityLoad_direct (v1.6 Inc2).** Cell A IL > Cell B IL where IL = mean(R_cult) / mean(R_cat) per cell; R4-independent because it uses Phase B Recall only, not Phase A Recognition.
- **H_SubstrateRecognition_PreScreen (v1.6 Inc1).** Non-directional classification: UNIFORM SATURATION if all cells modal C_P ≥ 5; DIFFERENTIAL otherwise.

# 3. Results

## 3.1 Phase A --- Recognition (C_P)

Twenty-three of 24 brands in the panel score C_P = 6/6. All seven Cell A heritage brands; four of five Cell B disruptors; all seven Cell C mass-legacy brands; all five Cell D defunct brands. The single exception is Fisker at C_P = 5/6, where Claude Sonnet 4.5 returned "no" --- a recent-corporate-distress artifact reflecting Fisker's 2024 corporate distress, rather than a category-classification failure.

Per-cell distributions: Cell A mean C_P = 6.00 (distinct = 1, modal share = 1.000), Cell B mean = 5.80 (distinct = 2, modal share = 0.800), Cell C mean = 6.00 (distinct = 1, modal share = 1.000), Cell D mean = 6.00 (distinct = 1, modal share = 1.000).

The Cell D saturation carries the heaviest substantive weight. All five defunct corporate brands score C_P = 6/6 on a present-tense "commonly recognized as a car brand" probe. The AI mediation layer treats them as categorically self-evident automotive brands despite documented closures spanning 2001--2010. This is the precondition Cell D was designed for: if Recognition had fallen short, the lead hypothesis test would have collapsed into a Recognition story rather than a Recall story. Recognition holds; the lead hypothesis test runs cleanly at Phase B.

![Phase A Recognition (C_P) per brand, grouped by IL-tier cell. The v1.6 substrate Recognition pre-screen (Inc1) classifies the substrate as UNIFORM SATURATION: 23 of 24 brands at C_P = 6/6; the single exception (Fisker, 5/6) reflects recent corporate distress rather than category-classification failure. All five Cell D defunct brands are at C_P = 6/6 --- the precondition for the lead phantom test to run meaningfully at Phase B.](../../reports/figs/v23/chart_01_cp_distribution.pdf){#fig:phase_a width=100%}

## 3.2 Phantom Brand Persistence --- the paired verdicts

The lead measurement of v0.23 is the paired Cell D / Cell A phantom test. **H_Phantom_Defunct returns FALSIFIED at the strongest possible margin.** Across all five Cell D brands --- Pontiac, Oldsmobile, Plymouth, Mercury, Saturn --- R_phantom_defunct = 0. In none of the (six models × three R_cat probes) = 18 unprompted current-tense Recall opportunities per brand does any defunct brand surface a single time. The pre-registered CONFIRMED threshold (R_phantom_defunct ≥ 4) is not approached by any brand; the entire Cell D is at the FALSIFIED floor.

The falsification is informative because it occurs on the substrate where the lead hypothesis was predicted to confirm. The pre-registration's substantive predictions section forecast strong phantom surfacing for Pontiac (GTO / Firebird / Trans Am film footprint), Oldsmobile (corporate Americana through 2004), and Mercury (deep film and music references). All three are recognized at C_P = 6/6 by all six models. Their identities are well-encoded in the AI mediation layer. They simply do not appear in present-tense Recall --- not in canonical "best car" frames, not in cultural "heritage / prestige / iconic" frames, not in either channel for any of the six panel models.

The supporting hypothesis returns CONFIRMED on the same panel run. **H_Phantom_Brand_Persistence_heritage returns CONFIRMED with three Cell A brands above the R_phantom ≥ 8 threshold:** Porsche at R_phantom = 14/18 (with R_cult at the maximum 18/18 --- every cult-frame query in every model returns Porsche), BMW at 12/18, Mercedes-Benz at 10/18. The maximum R_phantom = 14 matches the v0.21 Glossier benchmark (R_phantom = 12) on a living-brand substrate; the construct's upper bound is therefore consistent across substrates.

The paired verdicts establish a temporal boundary. Phantom persistence operates on living heritage brands and stops at documented brand death. The boundary is sharp, not gradient: on the same panel run, in the same Phase B responses, the same models that produce zero defunct-brand mentions produce high-volume living-heritage-brand surfacing. The AI mediation layer does not merely associate brand names with categories --- it associates brand names with categories plus temporal status, and that temporal status is robust enough that documented discontinuation acts as a hard Recall floor.

![Phantom Brand Persistence --- defunct corporate brands. R_phantom_defunct per Cell D brand: the count of unprompted Recall mentions of discontinued brands across (3 R_cat probes × 6 panel models, max 18). All five Cell D brands at R_phantom_defunct = 0; H_Phantom_Defunct FALSIFIED at the strongest possible margin. Threshold ladder locked at v0.23-prereg-r2: CONFIRMED ≥ 4; PARTIAL 1--3; FALSIFIED at zero across all.](../../reports/figs/v23/chart_04_phantom_defunct.pdf){#fig:phantom_defunct width=100%}

For the AI Availability construct, this is a tighter and more interesting claim than the v0.21 framing suggested. Phantom Brand Persistence is not substrate-agnostic leakage; it is a property of brand-identity persistence in the AI mediation layer, bounded by the layer's (implicit, learned) temporal categorization. The construct now has empirically anchored upper and lower boundaries: v0.21 Glossier R_phantom = 12 (off-panel, alive, anchors the upper bound); v0.23 Cell D R_phantom = 0 across all five brands (in-panel, documented dead, anchors the lower bound).

## 3.3 Recognition × Recall dissociation --- sixth substrate family

H_Dissoc_substrate_generalization returns GENERALIZED. Seventeen Iwachu-pattern cases (C_P ≥ 5 ∧ R_cat ≤ 2) appear on the v0.23 automotive panel, distributed across all four cells: four in Cell A (Jaguar, Cadillac, Rolls-Royce, Bentley, all R_cat = 0), four in Cell B (Rivian R_cat = 1; Lucid, Polestar, Fisker all R_cat = 0), four in Cell C (Ford R_cat = 2, Chevrolet R_cat = 0, Volkswagen R_cat = 1, Nissan R_cat = 0), and five in Cell D (all five defunct brands at R_cat = 0).

The Cell D contribution warrants methodological consideration. Defunct brands meet the Iwachu criterion tautologically: they are recognized at ceiling (C_P = 6) precisely because they are well-encoded brand identities, and they do not appear in R_cat responses precisely because the lead hypothesis falsifies. Netting out the five Cell D cases, the substantive Iwachu base for v0.23 is twelve cases across Cells A, B, and C --- still the largest substantive single-phase count in the program, and the formal verdict (GENERALIZED) holds on the locked criterion (≥ 1 case in Cell A or B). The cross-substrate generalization claim now spans six substrate families.

![Recognition × Recall dissociation scatter --- Iwachu pattern on the v0.23 automotive panel. Each colored point is one brand: Phase A C_P (x-axis, 0--6) versus Phase B R_cat mention count (y-axis, 0--18). Shaded quadrant: Iwachu pattern (C_P ≥ 5 ∧ R_cat ≤ 2). Seventeen Iwachu cases total across all four cells; substantive base (excluding Cell D tautological contributions) is twelve cases. H_Dissoc_substrate_generalization GENERALIZED; sixth-substrate-family extension closed.](../../reports/figs/v23/chart_02_dissociation_scatter.pdf){#fig:dissociation width=100%}

## 3.4 Two-channel Recall --- channel asymmetry and within-cell bifurcations

The two-channel Recall decomposition surfaces seven Type 2 cases (cultural-channel-preferred; R_cat ≤ 2 ∧ R_cult ≥ 5), the largest single-phase Type 2 count in the program. Four cases sit in Cell A: Rolls-Royce (R_cat = 0, R_cult = 13), Bentley (0, 12), Jaguar (0, 10), Cadillac (0, 8). Three sit in Cell C: Ford (R_cat = 2, R_cult = 6), Chevrolet (0, 7), Volkswagen (1, 6). Cell B produces zero Type 2 cases; Cell D produces zero --- a result consistent with the lead falsification.

Within Cell A, the seven heritage brands split into two channel-presence patterns. "Saturated heritage" (n = 3): Mercedes-Benz (R_cat = 10, R_cult = 16), Porsche (14, 18 --- a perfect R_cult saturation), BMW (12, 10). These brands surface heavily in both canonical "best/expert/quality" frames and cultural "heritage/prestige/iconic" frames. "Pure heritage-phantom" (n = 4): Jaguar, Cadillac, Rolls-Royce, Bentley --- all at R_cat = 0, all at R_cult ≥ 8. These brands operate as cultural artifacts decoupled from the canonical "recommended car" frame. The AI mediation layer renders them as legacy/prestige reference points but not as candidates one might purchase.

Within Cell C, a parallel bifurcation along an unexpected axis. "Canonical-Recall reliability" brands: Toyota (R_cat = 18, R_cult = 6 --- perfect canonical saturation), Honda (18, 0 --- Type 1), Hyundai (15, 1 --- Type 1). All three are Asian-manufactured mass-legacy brands; all three are heavily coded as best/expert/quality choices and weakly coded in cultural frames. "Cultural-Recall Americana" brands: Ford (2, 6), Chevrolet (0, 7), Volkswagen (1, 6) --- all three Type 2. American (and German) mass-legacy brands carry cultural identity --- storied, iconic, American-coded --- but minimal canonical-recommendation presence. Nissan, the cell's seventh brand, is invisible in both channels (R_cat = R_cult = 0).

![Two-channel Recall scatter --- R_cat × R_cult on the v0.23 automotive panel. Per-brand canonical mentions (R_cat, x-axis, max 18) versus cultural-footprint mentions (R_cult, y-axis, max 18). Type 2 quadrant (cultural-preferred; R_cat ≤ 2 ∧ R_cult ≥ 5) populates with seven cases across Cells A and C --- the largest single-phase Type 2 count in the program. Within-cell bifurcations: "saturated heritage" (Mercedes-Benz, Porsche, BMW) vs "pure heritage-phantom" (Jaguar, Cadillac, Rolls-Royce, Bentley) in Cell A; canonical-Recall Asian brands vs cultural-Recall Americana brands in Cell C.](../../reports/figs/v23/chart_03_channel_asymmetry.pdf){#fig:channel width=100%}

## 3.5 Regime 4 routing and v1.6 Inc2 IL Direct

H_Regime4_automotive returns FALSIFIED at C2 in all four cells. Cell A: distinct = 1, modal share = 1.000. Cell B: distinct = 2, modal share = 0.800. Cell C: distinct = 1, modal share = 1.000. Cell D: distinct = 1, modal share = 1.000. The rule's logic is correct: fully saturated within-cell distributions do not supply the variance C3 rank-coherence would consume. Regime 4 routes to FALSIFIED at the regime-floor, before any IL-gradient guard or Phase D check is reached --- the v0.21 cosmetics pattern replicated.

H_IdentityLoad_direct (v1.6 Inc2 --- R4-independent) returns CONFIRMED with the strongest IL signature in the program. Cell A R_cult / R_cat = 12.43 / 5.14 = 2.42; Cell B R_cult / R_cat = 1.20 / 1.60 = 0.75. Cell A heritage brands carry 3.2× the cult-channel dominance of Cell B disruptors. Cell C's ratio (0.48) trails Cell B --- a methodologically interesting result showing that the mass-legacy substrate carries canonical-Recall dominance even though it contains substantial cultural heritage (Ford, Chevrolet, Volkswagen all surface as cultural-channel-preferred Type 2 cases). The IL gradient at the channel-asymmetry layer is now anchored independently of Regime 4's C2 conditions, satisfying v1.6 Inc2's design intent.

H_SubstrateRecognition_PreScreen (v1.6 Inc1) classifies the substrate as UNIFORM SATURATION as predicted. All four cells have modal C_P = 6 (Cell A, C, D at 6/6 unanimous; Cell B at 6/6 modal with the single Fisker non-yes at 5/6). The classification is non-directional but consequential: for substrates with this property, category-membership Recognition is not the discriminating channel; the AIAS signal lives entirely in Recall and the construct's downstream measurements carry that load alone. Automotive joins cosmetics as the second substrate in the program where this property is documented at all-cell saturation.

# 4. Pre-Reg Outcomes

Table 1 summarizes the six pre-registered hypothesis verdicts against the locked verdict matrices.

| Hypothesis | Pre-registered prediction | Result | Status |
|---|---|---|---|
| H_Phantom_Defunct (LEAD) | CONFIRMED if any Cell D R_phantom_defunct ≥ 4; PARTIAL 1--3; FALSIFIED at zero across all | All five Cell D brands at R_phantom_defunct = 0 (Pontiac, Oldsmobile, Plymouth, Mercury, Saturn). | **FALSIFIED** |
| H_Phantom_Brand_Persistence_heritage | CONFIRMED if any Cell A R_phantom ≥ 8; PARTIAL 4--7; FALSIFIED all < 4 | Porsche R_phantom = 14, BMW = 12, Mercedes-Benz = 10. Max R_phantom = 14 matches v0.21 Glossier benchmark. | **CONFIRMED** |
| H_Regime4_automotive | C1 → C2 → IL-guard → C3; FALSIFIED if C2 fails in ≥ 2 cells | C2 fails in 4 of 4 cells. Resolved at regime-floor. | **FALSIFIED** |
| H_Dissoc_substrate_generalization | GENERALIZED if ≥ 1 Iwachu case in Cell A or B (6th family) | 17 Iwachu cases across 4 cells; substantive base 12 cases across A, B, C (Cell D tautological). | **GENERALIZED** |
| H_IdentityLoad_direct (v1.6 Inc2) | CONFIRMED if Cell A IL > Cell B IL (R4-independent ratio) | Cell A IL = 2.42, Cell B IL = 0.75 (3.2× cult-channel dominance). Strongest R4-independent IL signature. | **CONFIRMED** |
| H_SubstrateRecognition_PreScreen (v1.6 Inc1) | UNIFORM SATURATION if all cells modal C_P ≥ 5 | All cells modal C_P = 6 (A, C, D at 6/6 unanimous; B at 6/6 modal). | **UNIFORM SATURATION** |

The lead hypothesis FALSIFIED at the strongest possible margin (every Cell D brand at zero) paired with the primary supporting hypothesis CONFIRMED with margin (three Cell A brands above the threshold, maximum R_phantom = 14) is the v0.23 headline result. The construct's temporal boundary is established; the boundary is sharp.

# 5. Discussion

## 5.1 What the Cell D falsification means for the construct

The v0.21 Phantom Brand Persistence framing was substrate-agnostic. The Glossier case (off-panel, alive, R_phantom = 12 across six panel models on a cosmetics substrate) was the construct's empirical anchor, and the substrate-agnostic claim was that the AI mediation layer surfaces well-encoded brand identities in unprompted category-anchored Recall regardless of formal panel inclusion. The construct's value as a managerial instrument was high in substrates where the brand-of-interest's panel-membership status is itself a moving question --- emerging brands, indie tiers, substrate categories where panel construction is contested.

v0.23 narrows the construct. The Cell D / Cell A paired verdicts demonstrate that the AI mediation layer associates brand names with categories *plus temporal status*, and that the temporal categorization is robust enough that documented discontinuation acts as a hard Recall floor. The phantom phenomenon operates on living heritage brands and stops at brand death. This is not a refutation of Phantom Brand Persistence as a phenomenon --- the supporting hypothesis confirms in the same panel run on the same substrate. What it refutes is the specific claim that phantom-surface leakage extends to documented-dead corporate brands. The construct survives in living-brand form; it is the discontinued-brand extension that fails.

The narrowed claim is more useful for brand-strategy practice. A brand audit using the Phantom Brand Persistence construct can rely on the substrate's living-brand assumption without correcting for temporal-categorization-aware floor effects on defunct competitors. The construct also becomes more falsifiable: the v0.23 measurement establishes the lower-bound floor (R_phantom = 0 on documented-dead brands) and the v0.21 measurement establishes the upper-bound demonstration (R_phantom = 12 on an off-panel living brand); future-phase substrates with living-brand registries can be evaluated against this defined range.

## 5.2 Within-cell channel bifurcations and cell-architecture implications

The v0.23 Cell A and Cell C within-cell bifurcations are substantively interesting in their own right and may motivate cell-design refinement in successor phases. Within Cell A, three "saturated heritage" brands (Mercedes-Benz, Porsche, BMW) surface heavily in both canonical and cultural Recall, while four "pure heritage-phantom" brands (Jaguar, Cadillac, Rolls-Royce, Bentley) surface only in R_cult. The R_cult-only brands operate as cultural reference points rather than purchase candidates --- a brand-strategy distinction with operational implications: brand managers at the four "pure heritage-phantom" brands face a different audit signal than the three "saturated heritage" brands, even within the same panel-design cell.

The Cell C bifurcation is unexpected. Asian-manufactured mass-legacy brands (Toyota, Honda, Hyundai) concentrate in canonical Recall; American and German mass-legacy brands (Ford, Chevrolet, Volkswagen) concentrate in cultural Recall. The pattern crosses a manufacturer-nationality axis that the panel-design IL-gradient construct does not capture. Whether the bifurcation generalizes to other panels (audio, appliances, other consumer durables with similar manufacturer-nationality structure) is a question for v0.23+ prospective phases.

## 5.3 v1.6 Inc2 H_IdentityLoad_direct --- strongest signature to date

The v0.23 Cell A vs Cell B IL ratio of 3.2× is the strongest R4-independent IL signature in the program (compared to v0.21 cosmetics Cell B vs Cell A δ = +7.13 in the IL Direct R_cult − R_cat sign-of-difference test in Gonzalez Castro 2026b). The result is achieved on a substrate where Regime 4 falsifies on the C2 saturation route in all four cells. v1.6 Inc2 was designed for exactly this case --- substrates where the IL signature is real but the Regime 4 C2 path cannot evaluate it --- and v0.23 supplies the cleanest demonstration the program has produced.

The interim operationalization used in the v0.23 scoring (mean R_cult / mean R_cat ratio per cell, sign-of-difference test) is robust to operationalization variants but is not the full v1.6 Inc2 specification. The v1.6 methodology paper (Gonzalez Castro 2026b) specifies an R4-independent bootstrap CI construction; the v0.23 scoring code's in-line documentation flags the interim choice and indicates the candidate to replace.

## 5.4 Phantom Brand Persistence has empirical boundaries

With v0.23 in place, Phantom Brand Persistence has empirical bounds. v0.21 Glossier (R_phantom = 12, off-panel, alive) anchors the upper-end demonstration. v0.23 Cell D (R_phantom_defunct = 0, in-panel, documented dead) anchors the lower-end floor. The phantom phenomenon is bounded by living-brand status. A natural Phase 2 extension is off-panel measurement on substrates other than cosmetics: scoring Phase B responses against a larger reference vocabulary captures phantom activity the panel-internal scoring misses. The v0.23 Phase B responses contained substantive off-panel brand activity not reflected in the locked-registry scoring (Lexus surfaced consistently in canonical "quality/reliability" frames as Toyota's luxury division; Ferrari and Lamborghini surfaced in cultural "iconic/heritage" frames; Aston Martin surfaced in heritage frames; Audi surfaced moderately in both channels). Phase 2 would lift Phantom Brand Persistence from a panel-edge observation to a first-class measured component.

# 6. Limitations

## 6.1 r1 → r2 pre-registration amendment

The r1 → r2 pre-registration amendment is a substantive methodology event that warrants surfacing here in addition to its locked documentation in DEVIATIONS Entry 0 of the pre-registration module. The r1 lock specified INSTRUMENT as single-model GPT-4.1 × n = 12 iterations --- a Claude-assisted drafting error that contradicted v0.17--v0.21 program convention (the six-model reference panel). The defect was caught pre-acquisition during mega-prompt drafting; no data was collected under r1. r2 corrects INSTRUMENT to the six-model panel and moves the H_Phantom_Defunct CONFIRMED threshold from 3 (on assumed max-12) to 4 (on corrected max-18) for proportional consistency with the supporting heritage hypothesis (also 4/18 PARTIAL floor). r1 is retained in git history for audit; r2 is the operative lock for v0.23.

The amendment did not alter the conclusion: H_Phantom_Defunct FALSIFIES with margin at either threshold (the maximum Cell D R_phantom_defunct is 0; any positive threshold would have FALSIFIED equivalently). The threshold harmonization is documentary completeness, not result-altering.

## 6.2 Tautological Iwachu cases in Cell D

Cell D Iwachu contributions are tautological. The Iwachu criterion (C_P ≥ 5 ∧ R_cat ≤ 2) is met by all five defunct brands precisely because they are well-recognized identities (C_P = 6/6) that do not surface in Recall (R_cat = 0) --- the lead hypothesis falsification produces the Iwachu signature mechanically. The formal verdict (H_Dissoc GENERALIZED) holds on the locked criterion (≥ 1 case in Cell A or B), but the substantive cross-substrate claim should rest on the twelve Cell A + Cell B + Cell C cases, not the seventeen-case total. Future v1.6+ increments may benefit from a substrate-internal Iwachu criterion that excludes phantom-floor cases.

## 6.3 Phase D Spearman ρ undefined on saturated cells

Phase D Spearman ρ is mathematically undefined in three of four cells (A, C, D) because C_P is constant (= 6) and rank correlation requires non-zero input variance. Only Cell B yields a defined ρ (= 0.395, n = 5). This is not a methodological failure mode but a substrate-saturation artifact: when Recognition fully saturates, the C3 rank-coherence test has no signal to compute. The v1.5 C2 path already routes Regime 4 to FALSIFIED at the regime-floor before C3 is reached, so the undefined ρ has no verdict consequence --- it is documented here for methodological transparency.

## 6.4 v1.6 Inc2 bootstrap CI outstanding

H_IdentityLoad_direct uses an interim operationalization (R_cult / R_cat ratio per cell, sign-of-difference test) pending v1.6 Inc2 methodology paper detail on the bootstrap CI construction. The verdict (CONFIRMED) is robust to operationalization variants --- Cell A IL of 2.42 vs Cell B IL of 0.75 is a 3.2× separation that no reasonable bootstrap envelope would collapse --- but the exact bootstrap procedure is unspecified in the locked pre-reg and the scoring code's in-line documentation flags the interim choice.

## 6.5 Off-panel scoring not in scope

Panel-internal scoring against the locked 24-brand registry captures Recall presence only for registered brands. Phase B responses contained substantive off-panel brand activity that the scoring does not reflect: Lexus surfaced consistently in canonical "quality/reliability" frames (Toyota's luxury division --- the Cell C Toyota saturation has a luxury-sibling phantom of its own); Ferrari and Lamborghini surfaced in cultural "iconic/heritage" frames; Aston Martin (the registry cut from Cell A) surfaced in heritage frames; Audi (a Cell A omission the registry design accepted) surfaced moderately in both channels. None of these affect the v0.23 verdicts under the locked methodology, but the off-panel pattern is informative for a Phantom Brand Persistence Phase 2 measurement that would score off-panel surfacing against a larger reference vocabulary.

## 6.6 Panel-state boundedness

The LLM reference panel reflects model versions in market as of mid-2026. Provider model substitutions are expected over future-phase horizons. v0.23's phantom-defunct falsification should be interpreted as the pattern observed against the locked panel at acquisition time, not as a permanent property of the AI mediation layer --- model-training-corpus shifts could in principle change defunct-brand temporal coding. A v2.x replication on a later panel would be informative.

# 7. Future Research

Three future-research arcs are implied by v0.23.

**Phantom Brand Persistence Phase 2 (off-panel measurement).** v0.23 Phase B responses contained substantive off-panel brand activity (Lexus, Ferrari, Lamborghini, Aston Martin, Audi). Phase 2 would score off-panel surfacing against a larger reference vocabulary, lifting Phantom Brand Persistence from a panel-edge observation to a first-class measured component. The construct's empirical bounds (v0.21 Glossier R_phantom = 12 upper; v0.23 Cell D R_phantom = 0 lower) provide the calibration range against which off-panel surfacing patterns can be evaluated.

**Cell-architecture refinement for heritage substrates.** v0.23's within-cell Cell A bifurcation ("saturated heritage" vs "pure heritage-phantom") suggests that a single Cell A panel may collapse substantively distinct brand-strategy positions. Successor phases on substrates with similar heritage saturation (luxury watches, premium spirits) could test whether the bifurcation generalizes and whether a two-tier heritage cell design (e.g., "active heritage" vs "legacy heritage") produces cleaner within-cell variance.

**v1.6 Inc2 bootstrap CI specification.** The v1.6 methodology paper (Gonzalez Castro 2026b) specifies R4-independent bootstrap CIs for H_IdentityLoad_direct but does not pin the bootstrap procedure in implementation-ready detail. A v1.6.1 methodology supplement could close the operationalization gap; v0.23's interim sign-of-difference test is the candidate to replace. The v0.23 verdict (CONFIRMED at 3.2× Cell A vs Cell B IL separation) is robust to operationalization variants but the precise bootstrap procedure is the methodology-paper deliverable.

# References {-}

Gonzalez Castro, P. U. (2026a). *AIAS 1.0 Synthesis: AI Availability as a Third Measurable Layer of Brand Availability*. SSRN Working Paper 6817841.

Gonzalez Castro, P. U. (2026b). *The AIAS Presence Measurement Protocol: Methodology v1.6 --- Substrate Recognition Pre-Screen, R4-Independent Identity Load, and Phantom Brand Persistence*. SSRN Working Paper 6816340.

Gonzalez Castro, P. U. (2026c). *AIAS v0.16 --- Kitchen Knives: Regime 4 Boundary and Discourse-Language Carryforward*. SSRN Working Paper 6791999.

Gonzalez Castro, P. U. (2026d). *AIAS v0.17 --- Premium Kitchenware: Panel Inadequacy and Recognition × Recall Dissociation*. SSRN Working Paper 6802261.

Gonzalez Castro, P. U. (2026e). *AIAS v0.18 --- Indie Fragrance: Identity-Load Moderator and Recognition × Recall Dissociation Generalization*. SSRN Working Paper 6806558.

Gonzalez Castro, P. U. (2026f). *AIAS v0.19 --- Audiophile Headphones: Two-Channel Recall Calibration*. SSRN Working Paper 6809182.

Gonzalez Castro, P. U. (2026g). *AIAS v0.20 --- Skincare: First Prospective Two-Channel Recall Phase*. SSRN Working Paper 6811441.

Gonzalez Castro, P. U. (2026h). *AIAS v0.21 --- Cosmetics: Type 2 EMERGED on an IL-Gradient Substrate*. SSRN Working Paper 6815378.

Gonzalez Castro, P. U. (2026i). *The AIAS Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy (v1.2)*. SSRN Working Paper 6761698.

Gonzalez Castro, P. U. (2026j). *The AIAS Presence Measurement Protocol: Methodology v1.5 --- Multi-Statistic C2 and Two-Channel Recall*. SSRN Working Paper 6810758.

Romaniuk, J., and Sharp, B. (2016). *How Brands Grow: Part 2 --- Including Emerging Markets, Services, Durables, New Brands and Luxury Brands*. Oxford University Press, Melbourne.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press, Oxford.

# Declarations {-}

## Conflict of interest

The author is employed full-time as Director, Corporate Brand Creative and Governance, at Samsung Electronics America. Samsung subsidiaries hold tier-2/3 component supply relationships with several brands in the v0.23 registry: Harman International (audio systems) supplies Mercedes-Benz, BMW, and other premium automotive OEMs; Samsung SDI (battery cells) supplies BMW (i-series), Volkswagen Group brands including Bentley and Porsche (Stellantis-adjacent platforms), and others; Samsung Display (infotainment) supplies Mercedes-Benz and BMW. Tesla and Polestar also have tangential Samsung-component exposure at the parts level. These are non-competitive supply relationships; Samsung Electronics America does not produce or market passenger car brands and has no brand-level competitive overlap with any v0.23 registry entry. The COI was screened and documented in DEVIATIONS Entry 0 (Part B) of the pre-registration module; no operational restriction on registry composition was imposed. The author's primary academic affiliation for this research is the School of Visual Arts MPS Branding Program; the research entity that maintains the data archive and methodology venue is Third System™ (thirdsystem.ai).

## Funding

Self-funded.

## Ethics

Not applicable. The research uses public LLM APIs and standard prompt batteries; no human subjects, no personal data, no protected populations.

## Data and code availability

All pre-registration artifacts, acquisition CSVs, scoring code, verdict matrices, and figures are deposited at the Open Science Framework: osf.io/ec6wh/v23/. Pre-registration is locked at git tag `v0.23-prereg-r2` (commit `0dde745`, branch `program-docs`). Acquisition is locked at git tag `v0.23-acquisition-locked`. The methodology version that governs scoring is Protocol v1.6 (Gonzalez Castro 2026b).

## Author information

Pablo Ulpiano González Castro is Director, Corporate Brand Creative and Governance, at Samsung Electronics America (this paper's research is conducted independently of his Samsung role). He is also Faculty in Creative Strategy at the School of Visual Arts MPS Branding Program, the primary academic affiliation for this research. He is the founder of Third System™ (thirdsystem.ai; hello@thirdsystem.ai), the independent research entity that maintains the AIAS™ data archive and methodology venue. ORCID: [0009-0003-8968-9990](https://orcid.org/0009-0003-8968-9990).
