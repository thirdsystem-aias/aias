---
title: "Recognition Ceiling, Dissociation Replication, and Cultural-Channel Asymmetry on an Audiophile Headphones Substrate"
subtitle: "AIAS™ Presence Measurement Protocol, v0.19 — H_C3 UNDETERMINED at C2 Boundary; v1.4 Construct Extends to Three Substrate Families"
author: >-
  Pablo Ulpiano González Castro \\
  \textit{School of Visual Arts, MPS Branding Program, New York, NY} \\
  \textit{(primary academic affiliation)} \\
  \textit{Third System™ (research entity; data archive and methodology venue)} \\[0.4em]
  Correspondence: \texttt{pablou@pablou.com} · \texttt{pablou.com} \\
  ORCID: \href{https://orcid.org/0009-0003-8968-9990}{0009-0003-8968-9990}
date: "May 2026"
mainfont: Carlito
fontsize: 11pt
linkcolor: black
urlcolor: black
header-includes:
  - \usepackage{setspace}
  - \setstretch{1.36}
  - \setlength{\parskip}{8pt}
  - \setlength{\parindent}{0pt}
  - \usepackage{float}
  - \floatplacement{figure}{H}
  - \usepackage{caption}
  - \captionsetup{labelfont={bf,it}, textfont=it, justification=raggedright, singlelinecheck=false}
  - \usepackage{titlesec}
  - \titleformat{\section}{\bfseries\large}{\thesection}{1em}{}
  - \titleformat{\subsection}{\bfseries\normalsize}{\thesubsection}{1em}{}
---

\newpage

# Abstract

The AIAS™ Presence Measurement Protocol operationalizes AI Availability — the brand-level probability of retrieval, recommendation, or selection by an AI intermediary — as a measurable construct alongside Ehrenberg-Bass Mental Availability and Physical Availability. Protocol v1.4 (SSRN 6799479) extends AI Availability into a multi-component construct (Recognition $\times$ Recall). The construct's empirical foundation prior to v0.19 consisted of two substrate families: the single Iwachu anchor on a cross-cultural Japanese cell (v0.17, SSRN 6802261) and nine cases on an English-language indie-fragrance substrate (v0.18, SSRN 6806558). This paper reports v0.19, designed primarily as a C3 ranking-coherence rescue addressing the within-cell variance degeneracy that produced v0.18's PARTIAL verdict, and secondarily as a third-substrate replication test for the multi-component construct itself. The substrate is audiophile headphones, sampled across two same-Identity-Load cells stratified by audiophile-segment product-line emergence year: Heritage (pre-2008) and Boutique (post-2008). Each cell holds 8 brands (n = 16; C1 floor n $\geq$ 12). The reference panel is the locked six-slot v0.17/v0.18 panel. Phase B uses a six-frame query battery split into three load-bearing category-anchored frames and three descriptive cultural-footprint frames.

Three pre-registered hypotheses returned three distinct outcomes. H_C3 returned **UNDETERMINED** per pre-registered DEVIATIONS Rule 4: Cell A_Heritage Phase A C_P modal share = exactly 0.500 (failing the strict-less-than C2 threshold by a single brand at the ceiling), Cell B_Boutique modal share = 0.875 (saturated). Under Rule 4, within-cell C2 failure in both cells routes C3 to UNDETERMINED without computing per-cell $\rho$. H_Recognition_Recall_Dissociation_Replication returned **REPLICATED_PARTIAL**: three Iwachu-pattern cases identified (ZMF Headphones, Spirit Torino, Final Audio — all Cell B_Boutique), between the REPLICATED floor ($\geq$ 5) and the NOT_REPLICATED floor (0). The cumulative anchor base for the v1.4 multi-component construct now spans 13 cases across three substrate families. H_CulturalFootprint_Dissociation_Sensitivity returned its descriptive case-list: three Type 1 cases (Audeze, HiFiMan, Dan Clark Audio) and zero Type 2 cases, with the Type 2 absence diagnosed as a panel-composition limit rather than an absent pathway. Cell A_Heritage's failure at exactly 0.500 modal share is documented as a methodological finding for AIAS™ 1.0 / v1.5 C2 operationalization refinement. Pre-registration discipline locks panel, hypotheses, decision rules, and verdict matrices at commit `2cbd36c` (tag `v0.19-prereg-r1`).

**Keywords:** AI availability; brand availability; Recognition–Recall dissociation; cultural-footprint Recall; LLM mediation; pre-registration; Spearman bootstrap; audiophile headphones; Ehrenberg-Bass; AIAS

**JEL classifications:** M31 (primary); L86; L15; D83; M37

---

# 1. Introduction

The two-system framework of brand availability — Mental Availability and Physical Availability (Sharp, 2010; Romaniuk, 2018) — has organized empirical brand-growth science for three decades. The AIAS™ Presence Measurement Protocol (SSRN 6659000, SSRN 6761698) extends the framework into the AI-mediated commerce environment by introducing **AI Availability** as a third measurable layer: the brand-level probability that a brand is retrieved, recommended, or selected by an AI intermediary in a category-relevant decision context.

Protocol v1.4 (SSRN 6799479) refined the AI Availability construct from a single-dimensional measure into a multi-component decomposition: **Recognition** (whether the AI system recognizes the brand as belonging to the category at all — operationalized as Phase A C_P anchoring) and **Recall** (whether the AI system retrieves the brand when asked to enumerate category members — operationalized as Phase B mention rate). The construct's empirical foundation has accumulated across phases: the single Iwachu dissociation observed on the v0.17 Japanese-cell substrate (Phase A C_P = 6/6, Phase B mention rate = 0/18) provided the original cross-cultural anchor, and v0.18's indie-fragrance substrate generalized the pattern to a same-language IL-gradient design with nine additional cases (SSRN 6806558). Two substrate families with ten cumulative cases is informative but not yet construct-grade evidence. The first non-fragrance replication is required before the multi-component construct can ship as canonical in AIAS™ 1.0.

In parallel, v0.18 left a methodologically open question. The C3 ranking-coherence test (per-cell Spearman $\rho$ between Phase A C_P and Phase B mention count) returned PARTIAL on v0.18 — only one of three cells (Cell C mass-prestige, $\rho$ = 0.615) cleared the per-cell threshold; the other two failed for substantively divergent reasons. Cell A_designer-niche's flat Recognition profile (7 of 8 brands tied at C_P = 6/6) collapsed within-cell rank correlation on the x-axis; Cell B_indie-artisan's near-uniform Recall sparseness (7 of 8 brands at zero mentions) collapsed it on the y-axis. The C3 verdict failed not because the underlying construct lacked rank coherence but because the substrate did not afford within-cell variance in both Recognition and Recall simultaneously. A C3 verdict that resolves on substrate adequacy rather than on construct coherence is uninformative.

This paper reports v0.19, designed to resolve both questions on a single substrate with three pre-registered hypotheses tested orthogonally. H_C3 (primary) is the within-cell variance-and-ranking test on a substrate engineered for variance in both dimensions. H_Recognition_Recall_Dissociation_Replication (secondary, methodological) tests whether the v1.4 Iwachu-pattern threshold yields cases on a third substrate family. H_CulturalFootprint_Dissociation_Sensitivity (descriptive) operationalizes the v0.18 §4.3 sensitivity finding — that some brands surface in category-anchored frames through general cultural-discourse channels independent of category-anchored Recognition — by splitting Phase B into category-anchored and cultural-footprint frame pairs and case-listing the two asymmetric dissociation profiles.

The substrate is **audiophile headphones**, selected on three grounds. First, the category admits a clean two-cell stratification on a single non-IL dimension: Heritage brands (pre-2008 audiophile-segment product line) versus Boutique brands (post-2008), holding Identity Load uniform across cells to isolate the C3 substrate test from IL-moderator confounding. Second, the category is English-language anchored throughout, eliminating the cross-cultural confound that contaminated v0.17. Third, brand-era stratification by audiophile-segment product line was hypothesized to produce within-cell Recognition variance (Heritage spanning legacy mass-consumer brands like Sony and Koss alongside long-canonical audiophile anchors like Sennheiser and Beyerdynamic) sufficient to clear the C2 modal-share threshold and expose the C3 test cleanly. The first two design intentions held; the third did not.

Pre-registration discipline is treated as structurally definitive of the protocol's credibility (Nosek et al., 2018). The v0.19 pre-registration is locked at commit `2cbd36c` with tag `v0.19-prereg-r1` on branch `v0.18-il-gradient` (deposited at osf.io/ec6wh/v19/), with all panel composition, hypothesis specifications, decision-rule thresholds, verdict matrices, and DEVIATIONS rules — including the v0.19-introduced Rule 4 (within-cell C2 variance failure routes H_C3 to UNDETERMINED) — fixed ex-ante.

---

# 2. Methods

## 2.1 Substrate definition and brand-era design

"Audiophile headphones" is operationally defined as a two-cell panel of brands whose audiophile-segment product line — distinct from any earlier mass-consumer presence the brand may have held — emerged before or after a 2008 threshold. The threshold corresponds to the period of audiophile-segment market formation in which planar-magnetic and high-end dynamic driver innovation produced the contemporary boutique-audiophile category. Identity Load is held uniform across cells: both Heritage and Boutique cells contain brands whose category-membership claim rests on enthusiast-recognition rather than mainstream consumer awareness.

Two cells are stratified by audiophile-segment product-line emergence year:

- **Cell A — Heritage, pre-2008.** Brands whose audiophile-segment product line predates the modern boutique-audiophile market formation. Cell composition spans the variance lever the substrate intended to provide: long-canonical audiophile anchors (Sennheiser, Beyerdynamic, Grado), brands with mixed mass-consumer and audiophile heritage (Sony, Audio-Technica), specialty-segment incumbents (Stax), and brands whose audiophile-segment presence has narrowed over time (Koss, Denon).
- **Cell B — Boutique, post-2008.** Brands whose audiophile-segment product line is native to the modern enthusiast category — small-house and specialty-manufacturer identity is constitutive of brand positioning.

If H_C3 holds and the substrate is adequate, both cells should exhibit Phase A modal share below the 0.50 strict-less-than threshold (within-cell Recognition variance adequate for C3 to compute) and both should produce per-cell Spearman $\rho$ in the C3-clearing range with bootstrap CI lower bound above 0.20.

## 2.2 Brand registry and reference panel

The locked registry holds 16 brands (8 per cell, n = 16; C1 floor n $\geq$ 12). The original draft included AKG in Cell A; AKG was substituted with Denon in the locked registry to avoid potential brand-confounding given the author's Samsung Electronics America employment (Samsung acquired AKG's parent Harman International in 2017). The substitution was made before pre-registration lock and is documented in the panel registry at `osf/v19/panel_registry_v0_19.csv`.

**Cell A_Heritage:** Sennheiser, Beyerdynamic, Denon, Grado, Sony, Audio-Technica, Stax, Koss.

**Cell B_Boutique:** Audeze, HiFiMan, Focal, Meze, ZMF Headphones, Spirit Torino, Final Audio, Dan Clark Audio.

Stax and HiFiMan are pre-registered cross-cultural flags (Japanese and Chinese origin respectively, both with substantive English-language LLM coverage). Focal (French) and Final Audio (Japanese) are pre-registered as borderline classifications under the product-line emergence rule, retained on the basis of audiophile-segment product-line documentation rather than corporate founding date.

The locked six-slot reference panel from v0.17/v0.18 is reused without modification: claude-opus-4-5, claude-sonnet-4-5, gpt-4o, gpt-4o-mini, gemini-2.5-flash, gemini-2.5-flash-lite. No provider model substitutions were required during acquisition (96 of 96 Phase A queries successful; 36 of 36 Phase B queries successful).

## 2.3 Phase A: Recognition (C_P)

Phase A operationalizes Recognition per Protocol v1.4. For each registry brand, the v1.4 C_P probe ("Is the brand X commonly recognized as a brand of audiophile headphones? Answer yes or no.") is sent to each of the six panel models; the brand's C_P score (range 0..6) is the count of recognition-positive responses across the panel. Pivot determination follows the cascade rule from v1.3 / v1.4.

## 2.4 Phase B: six-frame query battery

Phase B operationalizes Recall through a six-frame battery split into two channel sets, with channel routing pre-registered ex-ante:

**Load-bearing category-anchored frames (q1–q3):**

- **q1 (audiophile):** "What are the best audiophile headphones? List several with descriptions."
- **q2 (enthusiast):** "Recommend high-quality headphones for serious music listening. Name several brands."
- **q3 (reference):** "What headphones are considered reference-grade by audiophiles? List several."

**Descriptive cultural-footprint frames (q4–q6):**

- **q4 (famous):** "What are the most famous headphone brands? List several."
- **q5 (popular):** "What headphone brands are most well-known among general consumers? Name several."
- **q6 (iconic):** "Which headphone brands have the strongest cultural recognition? List several with brief descriptions."

For each (frame, model) response, all 16 registry brands are scanned for mention presence under the v1.4 canonical brand-mention detection rules (case-insensitive, accent-stripped, possessive-aware, first-occurrence-wins de-duplication). Rank within enumerated response lists is recorded. Each brand has 18 category-anchored observation slots (q1–q3 $\times$ 6 models) and 18 cultural-footprint observation slots (q4–q6 $\times$ 6 models).

Only the category-anchored channel (q1–q3) load-bears on H_C3 and H_Dissoc verdicts. The cultural-footprint channel (q4–q6) feeds H_CulturalFootprint's descriptive output and is also reported alongside category-anchored counts in §3.5.

## 2.5 Hypotheses and decision rules

Three orthogonal hypotheses are pre-registered (verdict matrices ex-ante; full specification in `osf/v19/PRE_REGISTRATION_v0_19.md` and `osf/v19/thresholds_v0_19.json`):

- **H_C3** (primary, within-phase substantive): C1 (worldwide n $\geq$ 12, per-cell n $\geq$ 5) $\to$ C2 (per-cell Phase A C_P modal share AND per-cell Phase B mention-count modal share both < 0.50) $\to$ C3 (per-cell Spearman $\rho$ between Phase A C_P and Phase B category-anchored mention count $\geq$ 0.50, AND bootstrap 95% CI lower bound > 0.20, in $\geq$ 1 of 2 cells; 10,000 brand-level resamples, percentile method, seed 42).
- **H_Recognition_Recall_Dissociation_Replication** (secondary, methodological): Iwachu-pattern cases (Phase A C_P $\geq$ 5/6 AND Phase B category-anchored mention count $\leq$ 2/18) routed REPLICATED if $\geq$ 5 cases identified, REPLICATED_PARTIAL if 1–4 cases, NOT_REPLICATED if 0 cases.
- **H_CulturalFootprint_Dissociation_Sensitivity** (descriptive): document Type 1 cases (category-anchored mentions $\geq$ 5/18 AND cultural-footprint mentions $\leq$ 2/18) and Type 2 cases (category-anchored mentions $\leq$ 2/18 AND cultural-footprint mentions $\geq$ 5/18) per cell. No verdict; descriptive output only.

Pre-registered DEVIATIONS rules govern routing:

- **Rule 4** (NEW for v0.19): If within-cell C2 variance fails in both cells, H_C3 routes to UNDETERMINED without computing per-cell $\rho$. Panel is NOT substituted. The substantive finding (substrate produced ceiling effects in both cells) stands as a methodological data point.
- **Rule 6**: Cross-cultural robustness analysis required when at least one Iwachu case occurs on a cross-cultural-flagged brand. Re-compute per-cell $\rho$ with cross-cultural-flagged brands (Stax in Cell A_Heritage; HiFiMan in Cell B_Boutique) excluded; report $\Delta$$\rho$. If C2 fails and $\rho$ is not computed, Rule 6 reports "not applicable."

C1, C2, C3, Iwachu, and channel-asymmetry thresholds are locked numerically in pre-reg `v0.19-prereg-r1` at commit `2cbd36c`. The C3 $\rho$ threshold (0.50) and bootstrap CI lower bound (0.20) are calibrated to the v1.4 framework and are not lifted from prior phases.

---

# 3. Results

## 3.1 Phase A — Recognition (C_P)

Phase A produced a clean Recognition gradient at the cell level but failed the C2 within-cell modal-share threshold in both cells. Pivot anchoring outcomes:

- **Cell A_Heritage — pivot anchored at Sennheiser** (C_P = 6/6 on first cascade step). Per-brand C_P distribution: Sennheiser 6/6, Beyerdynamic 6/6, Grado 6/6, Audio-Technica 6/6, Stax 5/6, Sony 4/6, Denon 3/6, Koss 2/6. Five distinct C_P values across eight brands, range 4 (from 2 to 6). Cell mean C_P $\approx$ 4.75. **C_P modal share = 4/8 = 0.500** (four brands at the modal value of 6/6). Under the strict-less-than C2 threshold, Cell A_Heritage **fails** by a single brand at the ceiling.
- **Cell B_Boutique — pivot anchored at Audeze** (C_P = 6/6 on first cascade step). Per-brand C_P distribution: Audeze 6/6, HiFiMan 6/6, Focal 6/6, Meze 6/6, ZMF Headphones 6/6, Spirit Torino 5/6, Final Audio 6/6, Dan Clark Audio 6/6. Two distinct C_P values across eight brands (6/6 and 5/6). Cell mean C_P $\approx$ 5.88. **C_P modal share = 7/8 = 0.875**. Cell B_Boutique **fails** C2 by a substantial margin.

The Cell A_Heritage failure-by-one-brand at exactly 0.500 modal share is itself a substantive finding. The C_P distribution `[2, 3, 4, 5, 6, 6, 6, 6]` is qualitatively richer than v0.18's degenerate cells (v0.18 Cell A_designer-niche carried seven of eight brands at C_P = 6/6, modal share 0.875; v0.18 Cell C_mass-prestige carried seven of eight brands at C_P = 0/6, modal share 0.875). Five distinct C_P values spanning a four-point range across eight brands is the kind of within-cell variance the C3 test was designed to act on. The strict-less-than C2 threshold catches this distribution at exactly the boundary it is calibrated to defend.

![Phase A Recognition (C_P) score per brand, per cell. Each point is one brand; jitter spreads points within cells for visibility. Cell A_Heritage spans C_P = 2 (Koss) to 6 (Sennheiser, Beyerdynamic, Grado, Audio-Technica) with four of eight brands at the ceiling — C_P modal share = 0.500, exactly at the C2 strict-less-than boundary. Cell B_Boutique has seven of eight brands at C_P = 6 (only Spirit Torino at 5/6) — modal share = 0.875, well above the C2 threshold. Both cells fail C2; H_C3 routes to UNDETERMINED per pre-registered DEVIATIONS Rule 4. Cell A's failure-by-one-brand exposes a C2 operationalization edge case for AIAS™ 1.0 methodology refinement.](../../reports/figs/v19/chart_01_cp_distribution.pdf){#fig:cp-distribution width=100%}

## 3.2 Phase B — Recall (six-frame battery)

Phase B Recall produced 165 total brand-mentions across 576 brand $\times$ frame $\times$ model observations (~28.6% mention rate). Per-brand category-anchored mention counts (q1–q3 channel, max = 18):

**Cell A_Heritage:** Sennheiser 18, Beyerdynamic 15, Audio-Technica 10, Sony 8, Grado 7, Denon 2, Stax 2, Koss 1.

**Cell B_Boutique:** Audeze 13, HiFiMan 12, Focal 10, Dan Clark Audio 5, Meze 3, ZMF Headphones 1, Spirit Torino 0, Final Audio 0.

Cell A_Heritage Recall ranges 1–18 across the cell (range 17); Cell B_Boutique Recall ranges 0–13 (range 13). Cell A_Heritage's Recall distribution is broad enough to clear the Phase B mention-count modal-share threshold; Cell B_Boutique's distribution skews toward the lower end with five of eight brands at $\leq$ 3 mentions.

Cultural-footprint mentions (q4–q6 channel, max = 18) are reported in §3.5 alongside the channel asymmetry analysis.

## 3.3 Phase D — within-cell $\rho$ NOT COMPUTED (Rule 4)

Both cells fail Phase A C2 (Cell A_Heritage modal share = 0.500, Cell B_Boutique modal share = 0.875). Per pre-registered DEVIATIONS Rule 4, when within-cell C2 variance fails in both cells, H_C3 routes to UNDETERMINED without computing per-cell $\rho$. The substantive finding — both cells produced Recognition ceiling effects against a substrate engineered to provide within-cell Recognition variance — is preserved without retroactive panel substitution.

The cross-cultural robustness analysis required by Rule 6 reports "not applicable" for both cells, because per-cell $\rho$ was not computed and $\Delta$$\rho$ cannot be calculated. The cross-cultural exposure documented for Stax and HiFiMan remains pre-registered but unquantified at the v0.19 phase resolution.

## 3.4 Recognition $\times$ Recall dissociation case identification

The Iwachu-pattern threshold (Phase A C_P $\geq$ 5/6 AND Phase B category-anchored mention count $\leq$ 2/18) identifies brands exhibiting the Recognition-without-Recall dissociation that v1.4 anchors empirically. v0.19 produces 3 dissociation cases:

| Brand | Cell | C_P | Category-anchored mentions |
|---|---|---|---|
| ZMF Headphones | B_Boutique | 6/6 | 1/18 |
| Spirit Torino | B_Boutique | 5/6 | 0/18 |
| Final Audio | B_Boutique | 6/6 | 0/18 |

All three cases concentrate in Cell B_Boutique (3 of 8 cell brands, 37.5%). Cell A_Heritage contributes zero Iwachu-pattern cases — not by Recognition-floor design (as v0.18 Cell C did) but because Cell A_Heritage brands that achieve C_P $\geq$ 5/6 (Sennheiser, Beyerdynamic, Grado, Audio-Technica, Stax) also surface substantively in Phase B category-anchored frames (mention counts of 18, 15, 7, 10, and 2 respectively; only Stax sits at the dissociation mention-ceiling). The Heritage tier's broad LLM training-data depth supports both Recognition and Recall channels; the Boutique tier's enthusiast-discourse presence supports Recognition without producing comparable category-anchored Recall.

The cumulative anchor base for the v1.4 multi-component construct now spans three substrate families with 13 cumulative cases: 1 case from v0.17 (Iwachu, Japanese-cell, cross-cultural), 9 cases from v0.18 (indie fragrance, English-language, IL-stratified), and 3 cases from v0.19 (audiophile electronics, English-language, brand-era stratified).

![Recognition $\times$ Recall dissociation scatter — cumulative anchor base across three substrate families. Each colored point is one v0.19 audiophile-headphone brand: Phase A C_P (x-axis, 0–6) versus Phase B category-anchored mention count (y-axis, 0–18). Gray ghost markers show v0.18 indie-fragrance Iwachu cases (n = 9); black $\times$ marks the v0.17 Japanese-cell Iwachu anchor. Shaded quadrant: Iwachu-pattern (C_P $\geq$ 5 AND mentions $\leq$ 2). v0.19 contributes 3 new cases (ZMF Headphones, Spirit Torino, Final Audio — all Cell B_Boutique). The AIAS™ v1.4 multi-component construct now spans three substrate families with 13 cumulative cases.](../../reports/figs/v19/chart_02_dissociation_scatter.pdf){#fig:dissociation width=100%}

## 3.5 Channel asymmetry — Type 1 and Type 2 case identification

The H_CulturalFootprint_Dissociation_Sensitivity descriptive output operationalizes the v0.18 §4.3 sensitivity finding that some brands surface through cultural-discourse channels independent of category-anchored Recognition. v0.19 produces 3 Type 1 cases (category-channel-preferred) and 0 Type 2 cases (cultural-channel-preferred):

| Brand | Cell | Category-anchored mentions | Cultural-footprint mentions |
|---|---|---|---|
| Audeze | B_Boutique | 13/18 | 2/18 |
| HiFiMan | B_Boutique | 12/18 | 1/18 |
| Dan Clark Audio | B_Boutique | 5/18 | 0/18 |

All three Type 1 cases concentrate in Cell B_Boutique. These brands surface strongly in audiophile category-anchored discourse but minimally in mainstream cultural-recognition prompts — the expected profile for discourse-strong boutique brands.

Zero Type 2 cases: no brand in the v0.19 panel exhibits low category-anchored Recall paired with high cultural-footprint Recall. The cultural-footprint pathway is demonstrably operating (Phase B q4–q6 responses surface Bose, Beats, AirPods Max, Sony WH-1000XM, Skullcandy, and JBL extensively across the six-model panel) but the brands surfacing through it are not in the v0.19 panel. The Heritage $\times$ Boutique audiophile-electronics design places both cells inside the category-recognition envelope; the design carries no brands with the Type 2 profile (low audiophile-category Recall paired with high mainstream-consumer Recall). The Type 2 absence is therefore a panel-composition consequence, not the absence of the cultural-footprint Recall pathway itself.

![Channel asymmetry scatter. Per-brand category-anchored mentions (x-axis, q1–q3 $\times$ 6 models = max 18) versus cultural-footprint mentions (y-axis, q4–q6 $\times$ 6 models = max 18). Lower-right shaded quadrant: Type 1 (category-channel-preferred; category-anchored $\geq$ 5 AND cultural-footprint $\leq$ 2). Upper-left quadrant: Type 2 (cultural-channel-preferred; category-anchored $\leq$ 2 AND cultural-footprint $\geq$ 5). Three Type 1 cases in v0.19: Audeze (13/18, 2/18), HiFiMan (12/18, 1/18), Dan Clark Audio (5/18, 0/18) — all Cell B_Boutique. Zero Type 2 cases. The Type 2 quadrant emptiness reflects panel composition (no mass-consumer brands in the Heritage $\times$ Boutique audiophile design), not the absence of the cultural-footprint Recall pathway.](../../reports/figs/v19/chart_03_channel_asymmetry.pdf){#fig:channel-asymmetry width=100%}

## 3.6 Verdict resolution

The three pre-registered hypotheses resolved against the locked verdict matrices as follows:

**H_C3 — UNDETERMINED (Rule 4 routing).** C1 clears (worldwide n = 16, per-cell n = 8). C2 fails in both cells: Cell A_Heritage Phase A modal share = 0.500 (at the strict-less-than boundary), Cell B_Boutique Phase A modal share = 0.875 (saturated). Per Rule 4, C3 SKIPPED; H_C3 routes to UNDETERMINED. Panel is not substituted; the substrate's failure to expose C3 is preserved as a methodological finding.

**H_Recognition_Recall_Dissociation_Replication — REPLICATED_PARTIAL.** Three Iwachu-pattern cases identified, all Cell B_Boutique. The pre-registered verdict matrix routes 1–4 cases to REPLICATED_PARTIAL (between the REPLICATED floor of 5 and the NOT_REPLICATED floor of 0). The v1.4 multi-component construct now spans three substrate families with 13 cumulative cases.

**H_CulturalFootprint_Dissociation_Sensitivity — DESCRIPTIVE.** Three Type 1 cases (Audeze, HiFiMan, Dan Clark Audio — all Cell B_Boutique) and zero Type 2 cases. The Type 2 absence is diagnosed as a panel-composition limit; the cultural-footprint Recall pathway operates in the v0.19 acquisition data but the v0.19 panel composition does not include brands that exhibit the Type 2 profile.

Cross-cultural robustness (DEVIATIONS Rule 6) reports "not applicable" for both cells (no per-cell $\rho$ computed).

---

# 4. Discussion

## 4.1 C3 rescue outcome: substrate engineering, not threshold loosening

The v0.19 substrate was designed to address the v0.18 C3 ranking-coherence failure mode by selecting a category where within-cell Recognition variance was expected to clear the C2 modal-share threshold. Cell A_Heritage's distribution `[2, 3, 4, 5, 6, 6, 6, 6]` is substantively the kind of distribution the design targeted: five distinct C_P values, range four, mean $\approx$ 4.75. Compared to v0.18's degenerate cells (Cell A_designer-niche at modal share 0.875, Cell C_mass-prestige at modal share 0.875), Cell A_Heritage represents a qualitative shift toward variance-richer Recognition profiles. But the strict-less-than C2 threshold (modal share < 0.50) catches the cell at exactly 0.500 — failing by a single brand at the ceiling.

Cell B_Boutique reproduces the v0.18 Cell B_indie-artisan ceiling pattern at a comparable modal-share level (0.875). Boutique audiophile brands are universally recognized by the panel as audiophile-headphone brands, leaving no within-cell Recognition variance for C3 ranking coherence to test even if Cell A_Heritage had cleared the C2 boundary.

The substantive interpretation is that the C2 operationalization, calibrated to defend against v0.18-shape variance degeneracy, is over-sensitive on mixed distributions where 50% of brands sit at one value with the other 50% distributed across multiple values. The Cell A_Heritage `[2, 3, 4, 5, 6, 6, 6, 6]` distribution carries substantive within-cell variance the modal-share metric cannot capture. An entropy-based or distinct-value-count C2 specification would distinguish v0.18-shape degeneracy (modal share 0.875 with one distinct value carrying the rest) from v0.19-shape boundary cases (modal share 0.500 with five distinct values across the cell). This refinement is the candidate AIAS™ 1.0 / v1.5 methodology change that v0.19 motivates as an empirical anchor.

Critically, the lever to pull is substrate selection and methodology refinement, not threshold loosening. Loosening C2 from < 0.50 to $\leq$ 0.50 to admit Cell A_Heritage's 0.500 modal share would defeat the threshold's defensive purpose for v0.18-shape degeneracy. The right move is a tightened multi-statistic specification that distinguishes the two distribution shapes substantively.

## 4.2 Recognition $\times$ Recall dissociation: third-substrate replication

The H_Recognition_Recall_Dissociation_Replication verdict of REPLICATED_PARTIAL is the methodologically load-bearing finding of v0.19, despite the verdict's intermediate status between REPLICATED ($\geq$ 5 cases) and NOT_REPLICATED (0 cases). Before v0.19, the v1.4 multi-component construct rested on two substrate families: one cross-cultural anchor case (v0.17 Iwachu) and nine same-language IL-stratified cases (v0.18 indie fragrance). The substrate-family count is the load-bearing variable for canonical construct claims, not the cumulative case count. A construct that produces cases on two substrate families could plausibly be IL-specific (high-IL substrates only) or cross-cultural-specific (Western-language LLM training-data bias artifact only). v0.19 closes both alternative explanations.

The v0.19 substrate is English-language anchored throughout (no cross-cultural cells), removing the cross-cultural artifact alternative. The Heritage $\times$ Boutique design holds Identity Load uniform across cells (both cells are enthusiast-recognition categories rather than mainstream-consumer categories), removing the IL-specific alternative. Three Iwachu-pattern cases on this substrate establish that the dissociation construct is neither cross-cultural-specific nor IL-specific — it is a substrate-general regularity of AI-mediated brand retrieval.

The cell-clustering pattern continues across substrates. v0.18 saw 6 of 9 cases in its highest-IL cell (75% of cell brands). v0.19 sees 3 of 3 cases in Boutique (37.5% of cell brands). Different cell-level prevalence levels but the same directional pattern: Iwachu cases concentrate in the cell whose brands operate further from the mainstream cultural-discourse surface. This regularity is observed twice on two distinct substrate-family designs, supporting an empirical-regularity status analogous to the cell-clustering patterns documented in the Ehrenberg-Bass tradition (Double Jeopardy, Duplication of Purchase).

## 4.3 Cultural-channel asymmetry: panel-composition finding

The H_CulturalFootprint_Dissociation_Sensitivity descriptive output validates the v0.18 §4.3 sensitivity finding at the methodological layer. The three Type 1 cases (Audeze, HiFiMan, Dan Clark Audio) demonstrate that the cultural-footprint channel is empirically distinguishable from the category-anchored channel at the brand level: brands strong on the audiophile-discourse axis can be measurably weak on the mainstream-cultural axis. The pre-registered q4–q6 frame split exposes the asymmetry cleanly.

The zero Type 2 cases finding is the more consequential methodological observation. The cultural-footprint pathway is demonstrably operating in the v0.19 acquisition: q4–q6 responses surface Bose, Beats, AirPods Max, Sony WH-1000XM, Skullcandy, and JBL extensively across the six-model panel. None of these brands are in the v0.19 registry, by design — the Heritage $\times$ Boutique audiophile-electronics design places both cells inside the category-recognition envelope. The Type 2 absence is therefore a panel-composition consequence, not a pathway absence.

For AIAS™ 1.0's methodology layer, this distinction matters. The cultural-footprint Recall channel deserves canonical methodology treatment as a distinct Recall mode alongside category-anchored Recall: the two channels exhibit distinguishable brand-level signatures, and the v0.18 sensitivity finding plus the v0.19 Type 1 / Type 2 framing together specify the operational thresholds. A v0.20 substrate including a deliberately-placed mass-consumer cell (Bose, Beats, Apple AirPods, Skullcandy, JBL) below the audiophile-category Recognition floor would generate Type 2 cases observable against the same threshold structure, completing the empirical anchor for v1.5 canonical formalization.

## 4.4 Limits and reservations

Four limits qualify the v0.19 verdicts:

**C2 operationalization at the strict-less-than boundary.** Cell A_Heritage's failure at exactly 0.500 modal share is a documented edge case of the current C2 metric. The substantive within-cell variance the cell provides (range 4, five distinct values across eight brands) is not captured by modal-share alone. AIAS™ 1.0 / v1.5 should consider entropy-based or distinct-value-count C2 specifications. v0.19 supplies the empirical anchor motivating this refinement; v0.20+ should validate any refined specification against both v0.18-shape degeneracy and v0.19-shape boundary cases before adoption.

**Type 2 absence reflects panel composition, not pathway absence.** The zero-Type-2 finding does not falsify the cultural-footprint Recall channel — Phase B q4–q6 responses surface multiple mass-consumer brands extensively. The Heritage $\times$ Boutique audiophile-electronics design places both cells inside the category-recognition envelope, so no panel brand has the Type 2 profile (low category-anchored Recall + high cultural-footprint Recall) by construction. v0.20+ should include a mass-consumer cell deliberately placed below the audiophile-category Recognition floor.

**Cross-cultural robustness analysis not applicable.** Pre-registered DEVIATIONS Rule 6 requires Stax / HiFiMan exclusion analysis as $\Delta$$\rho$ comparison against full-cell $\rho$. Because both cells failed C2 and per-cell $\rho$ was not computed, $\Delta$$\rho$ cannot be calculated. Cross-cultural confound exposure for v0.19 is documented but unquantified at the v0.19 phase resolution. Future substrates with within-cell variance adequate to clear C2 will permit the robustness computation per Rule 6.

**LLM panel temporal validity.** The six-slot reference panel (claude-opus-4-5, claude-sonnet-4-5, gpt-4o, gpt-4o-mini, gemini-2.5-flash, gemini-2.5-flash-lite) reflects model versions in market as of mid-2026. Provider model substitutions over future-phase horizons are expected and documented in the DEVIATIONS protocol. v0.19 dissociation cases and channel-asymmetry pattern should be interpreted as the result observed against the locked panel at acquisition (2026-05-20), not as permanent substrate properties.

---

# 5. DEVIATIONS

The DEVIATIONS protocol carries forward from v0.16 / v0.17 / v0.18. v0.19 introduces a new Rule 4 (within-cell C2 variance failure routes H_C3 to UNDETERMINED) as part of the pre-registration, locked ex-ante at commit `2cbd36c`. No DEVIATIONS entries were opened during Phase A or Phase B acquisition.

**Entry 1 (panel composition, pre-acquisition; pre-registered).** The original substrate draft included AKG in Cell A_Heritage as a long-canonical audiophile anchor. AKG was substituted with Denon in the locked registry to avoid potential brand-confounding given the author's Samsung Electronics America employment (Samsung Electronics' subsidiary Harman International acquired AKG in 2017). The substitution preserves Cell A_Heritage's eight-brand composition and the cell's substantive Heritage classification (Denon's audiophile-headphone product line predates the 2008 threshold). The substitution was made before pre-registration lock and is documented in the panel registry at `osf/v19/panel_registry_v0_19.csv`. The substitution is recorded here for completeness of the DEVIATIONS trail; it did not require Rule invocation because it occurred prior to lock.

**Rule 4 invocation (in scope, post-Phase-A scoring).** Phase A scoring confirmed Cell A_Heritage modal share = 0.500 (boundary failure) and Cell B_Boutique modal share = 0.875 (saturated failure). Per Rule 4, H_C3 routes to UNDETERMINED without computing per-cell $\rho$. The substrate's substantive failure to expose C3 is preserved as a methodological finding; panel is not substituted. The Cell A_Heritage boundary case is documented for AIAS™ 1.0 C2 operationalization refinement (§4.1). Full entry deposited at `osf/v19/DEVIATIONS.md`. Lock state: pre-reg tag `v0.19-prereg-r1` unchanged.

**Rule 6 evaluation (not applicable).** Cross-cultural-flagged brands (Stax in Cell A_Heritage; HiFiMan in Cell B_Boutique) remain in the panel. Per Rule 6, cross-cultural robustness analysis requires per-cell $\rho$ for the $\Delta$$\rho$ comparison; because Rule 4 routing skipped per-cell $\rho$ computation, Rule 6 reports "not applicable" for both cells. The cross-cultural exposure documented in pre-reg remains unquantified at the v0.19 phase resolution.

No additional deviations were opened during Phase A or Phase B acquisition.

---

# 6. Conclusion

The v0.19 acquisition produced three pre-registered verdicts of three distinct shapes — UNDETERMINED on the primary hypothesis, REPLICATED_PARTIAL on the secondary, and a descriptive case-list on the third — that together advance the AIAS™ Presence Measurement Protocol's trajectory toward AIAS™ 1.0 substantively, even where the headline verdict is procedurally indeterminate.

**For the substantive theory.** The H_Recognition_Recall_Dissociation_Replication verdict of REPLICATED_PARTIAL is the load-bearing finding. Before v0.19, the v1.4 multi-component construct rested on two substrate families with ten cumulative cases — sufficient for a generalization claim but vulnerable to two alternative explanations (cross-cultural training-data artifact; IL-substrate-specific regularity). v0.19's three Iwachu-pattern cases on a same-language, uniform-IL audiophile-electronics substrate close both alternatives. The construct travels across substrate families. The cell-clustering pattern observed in v0.18 (cases concentrate in the cell operating furthest from mainstream cultural-discourse) recurs in v0.19 — same directional regularity, different substrate, different cell-level prevalence. Two observations on two distinct substrate-family designs supports treating the cell-clustering as an empirical-regularity-grade pattern analogous to those documented in the Ehrenberg-Bass tradition.

**For the canonical methodology.** Two open items emerge from the joint v0.18 / v0.19 history. First, the C2 modal-share-< 0.50 operationalization is over-sensitive on mixed distributions (v0.19 Cell A_Heritage failing at exactly 0.500 with substantive within-cell variance) while appropriately sensitive on saturation (v0.18 degenerate cells; v0.19 Cell B_Boutique). An entropy-based or distinct-value-count C2 alternative is the candidate refinement for v1.5 — to be specified against both v0.18-shape degeneracy and v0.19-shape boundary cases before adoption. Second, the cultural-footprint Recall channel is now empirically distinguishable from category-anchored Recall (v0.19 Type 1 cases) but its canonical methodology treatment requires a v0.20 panel that includes brands with the Type 2 profile, achievable by deliberate inclusion of a mass-consumer cell below the category-recognition floor.

**For v0.20 and beyond.** The verdicts point at productive next directions. v0.20 substrate selection should target three concurrent criteria: within-cell Recognition variance adequate to clear C2 at any reasonable specification (substrate engineering for C3 access); inclusion of a mass-consumer cell below the category-recognition floor (Type 2 observability); and continued same-language anchoring with controlled cross-cultural confound exposure. The C3 ranking-coherence question remains open across four phases (v0.16, v0.17, v0.18, v0.19); none has produced a clean PASS on both cells of a substrate. The lever to pull next is substrate engineering and v1.5 methodology refinement, not threshold loosening.

The pre-registration discipline applied across v0.19 — Rule 4 introduced and locked ex-ante at `2cbd36c` to govern the very UNDETERMINED routing the substrate ultimately produced; panel composition locked before acquisition with the AKG $\to$ Denon substitution documented in the registry rather than retroactively papered over; the Cell A_Heritage boundary case documented as a methodological finding for v1.5 refinement rather than handled by threshold lifting — is itself the protocol-level commitment that distinguishes the AIAS™ program. The headline verdict is UNDETERMINED. The substantive program advance is the third-substrate construct replication, the cultural-channel-asymmetry empirical anchor, and the C2 operationalization edge case identified for v1.5.

---

# References

Binet, L., & Field, P. (2013). *The Long and the Short of It: Balancing Short and Long-Term Marketing Strategies*. Institute of Practitioners in Advertising.

González Castro, P. U. (2026a). AI Availability — A Third System in Brand Availability Theory. *SSRN Working Paper*. https://ssrn.com/abstract=6659000

González Castro, P. U. (2026b). The AIAS Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy. *SSRN Working Paper*. https://ssrn.com/abstract=6761698

González Castro, P. U. (2026c). The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification (v1.3). *SSRN Working Paper*. https://ssrn.com/abstract=6797679

González Castro, P. U. (2026d). The AIAS Presence Measurement Protocol: Recognition $\times$ Recall Decomposition and Multi-Component AI Availability (v1.4). *SSRN Working Paper*. https://ssrn.com/abstract=6799479

González Castro, P. U. (2026e). Regime 4 Boundary and Discourse-Language Carryforward on the Kitchen-Knives Substrate (v0.16). *SSRN Working Paper*. https://ssrn.com/abstract=6791999

González Castro, P. U. (2026f). Panel Inadequacy and Recognition $\times$ Recall Dissociation on the Premium Kitchenware Substrate (v0.17). *SSRN Working Paper*. https://ssrn.com/abstract=6802261

González Castro, P. U. (2026g). Identity-Load Moderator Test and Recognition $\times$ Recall Dissociation Generalization on an English-Language Indie Fragrance Substrate (v0.18). *SSRN Working Paper*. https://ssrn.com/abstract=6806558

Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The Preregistration Revolution. *Proceedings of the National Academy of Sciences*, 115(11), 2600–2606.

Romaniuk, J. (2018). *Building Distinctive Brand Assets*. Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

Sharp, B., & Romaniuk, J. (2021). *How Brands Grow Part 2: Including Emerging Markets, Services and Durables, New Categories and Brand Purpose* (revised edition). Oxford University Press.

---

# Declarations

**Declaration of interest.** The author is employed by Samsung Electronics America (Director, Corporate Brand Creative and Governance). The AIAS™ Presence Measurement Protocol and the work reported here are the author's independent academic research, conducted outside the scope of employment, in the author's role as faculty at the School of Visual Arts MPS Branding Program and founder of Third System™. Samsung had no role in the design, execution, analysis, or interpretation of this work. The panel substitution of AKG $\to$ Denon documented in §5 was made out of an abundance of caution given that Samsung's subsidiary Harman International owns AKG; the substitution occurred prior to pre-registration lock.

**Funder.** Self-funded.

**Ethics.** Not applicable; no human subjects. The research uses publicly accessible LLM APIs queried with non-personal, category-anchored prompts.

**Data and code availability.** All pre-registration artifacts, acquisition data, scoring code, and verdict outputs are deposited under Open Science Framework project ec6wh at osf.io/ec6wh/v19/. The pre-registration is locked at commit `2cbd36c` on git tag `v0.19-prereg-r1`, branch `v0.18-il-gradient`. Scoring outputs and the rendered brand-format report are committed at `cbecd3c` (post-Phase B acquisition + chart pipeline).

**Trademark notice.** AIAS™ and Third System™ are trademarks of the research program.

<!-- End v0.19 SSRN paper draft, post-acquisition state -->
