---
title: "Control-Dependent Verdicts in a Phantom-Brand Consistency Contrast"
subtitle: "A Pre-Registered Control-Flip Result on Frozen Multi-Substrate Inputs"
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

{\LARGE \textbf{Control-Dependent Verdicts in a Phantom-Brand Consistency Contrast}}\\[8pt]

{\large A Pre-Registered Control-Flip Result on Frozen Multi-Substrate Inputs\\ (AIAS™ v0.37)}\\[28pt]

Pablo Ulpiano González Castro\\[4pt]
School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System™ (research entity; data archive and methodology venue)\\[8pt]
Correspondence: pablou@pablou.com · pablou.com\\
ORCID: 0009-0003-8968-9990\\[20pt]

Pre-registration: \texttt{v0.37-prereg-r1} (externally anchored before analysis)\\
Data and code: OSF \texttt{ec6wh/v37}\\

\end{center}
\end{titlepage}

# Abstract {-}

Phantom-flagged brands — recognized by large language models yet falling below the recall floor — recur across the AIAS™ measurement program's substrate base, and exploratory observations have suggested they may carry a distinct cross-model consistency signature. This study tests that hypothesis under pre-registration, as a re-analysis of frozen multi-substrate inputs (five categories; 112 brand units; six-model panel), using the CV-CPC quantity in its locked characterization status. Because the phantom flag and the metric are both recall-coupled by construction, the design assigns the raw contrast the role of manipulation check (it confirms as expected: pooled Cliff's δ = −0.838, p = 0.0001) and places all inferential weight on a gating hypothesis with two co-primary controls and a binding disagreement rule. The controls disagree. Residualized on the Presence measure C_P, the contrast survives (δ = −0.797, p = 0.0001); residualized on recall-mean, it vanishes (δ = +0.068, p = 0.655). The gate is UNDETERMINED, and the pre-registered finding is the flip itself: recognition is saturated among analyzable units in three of five substrates, rendering the C_P control inert, while the recall-mean control removes the axis defining the classification. The disagreement is stable under leave-one-substrate-out resampling and reproduces on a second wave. The phantom-signature question is thereby shown to be undecidable with the current instrument, and the result supplies the pre-registered empirical case for the mean-independent consistency instrument and graded recognition signal mandated for the next methodology revision: a recognition-anchored control cannot govern a recall-coupled metric.

**Keywords:** AI Availability; brand availability; AIAS; Ehrenberg-Bass; consistency measurement; phantom brands; large language models; pre-registration; construct validity; brand growth

**JEL codes:** M31; L86; L15; D83; M37

**Paper status:** Working paper. Phase v0.37 of the AIAS™ Measurement Program; pre-registered at tag `v0.37-prereg-r1` prior to analysis.

# 1. Introduction

The AIAS™ Measurement Program operationalizes AI Availability as a measurable brand-growth construct, with the Presence component (C_P) validated across a multi-substrate base under Protocol v1.6 (SSRN 6816340) and a Consistency component under active methodological development. The candidate Consistency quantity CV-CPC — defined as 1/(1+CV) of the per-model recall vector — was specified and tested in the v1.7 methodology study (SSRN 6878818), which returned a pre-registered negative result: CV-CPC fails the dissociation criterion against Presence (ρ = 0.77) and was not adopted as a Consistency instrument. Subsequent phases (v0.32, SSRN 6898581; v0.33, SSRN 6909019; v0.34, SSRN 6915458) have consumed CV-CPC strictly as a characterization quantity under that status, documenting version-snapshot fragility, provider saturation-collapse, and two-wave temporal stability of its rank order, respectively.

This study addresses a question that has surfaced repeatedly at the edges of those phases: do phantom-flagged brands — units recognized by the model panel yet falling below the recall floor, the empirical signature locked as Phantom Brand Persistence at v1.6 — carry a distinct CV-CPC signature? Walled tertiary observations in v0.33 (provider-asymmetry contrasts in below-floor units) and v0.34 (near-total temporal persistence of phantom status, 0.98 across waves) motivated the hypothesis; per pre-registration, those observations serve as motivation only and carry no confirmatory weight here. The Naive-Phantom construct itself traces to the program's v1.0 stability study; operational anchoring in this phase is strictly the frozen recall-floor flags.

The design difficulty is stated at lock rather than discovered post hoc: both sides of the raw contrast are recall-coupled by construction. The phantom flag is defined by recall-floor status, and CV-CPC is mechanically depressed at low recall mean (CV scales approximately as 1/√mean). A raw phantom-versus-non-phantom contrast on CV-CPC is therefore close to tautological, and the pre-registration assigns it the role of manipulation check only. The phase's entire inferential claim rests on a gating hypothesis, H_Phantom_Beyond_Presence, equipped with two co-primary controls — residualization on C_P (the construct-level Presence control) and residualization on recall-mean (the mechanical driver itself) — and a binding pre-registered rule: if the gate verdict differs across the two controls, the gate is UNDETERMINED and the flip itself is the reportable finding.

The flip fired. Under the C_P control the residualized contrast is large and significant (δ_resid = −0.797, p = 0.0001); under the recall-mean control it vanishes (δ_resid = +0.068, p = 0.655). The disagreement is stable under leave-one-substrate-out resampling and reproduces in the second-wave test-retest check. The mechanism is identified rather than conjectured: recognition is saturated among analyzable units in three of five substrates, rendering the C_P control inert exactly where the contrast lives, while the recall-mean control removes the axis that defines the phantom flag. The result is a pre-registered empirical demonstration that a recognition-anchored control cannot govern a recall-coupled metric — the concrete case for the mean-independent Consistency instrument and graded recognition signal already mandated for the v1.8 methodology revision.

A provenance note: the frozen inputs consumed here originate in the v0.31 phase, whose paper is withdrawn; the governing consumption convention is stated in §2.1.

# 2. Method

## 2.1 Design and inputs

v0.37 is a pre-registered re-analysis with no new LLM acquisition (lock tag `v0.37-prereg-r1`, externally anchored by remote push and OSF deposit prior to any computation). Inputs are the frozen per-brand t₁ quantities across the five omnibus substrates carrying the canonical six-model panel — v0.19 audiophile headphones (16 brands), v0.20 skincare (24), v0.21 cosmetics (24), v0.22 automotive (24), v0.23 premium spirits (24); 112 brand units: per-brand CV-CPC, per-brand C_P (Protocol v1.6), per-brand recall-mean, and the frozen phantom-flag classification. The tertiary test-retest check additionally consumes the v0.34 t₂ wave.

The consumption convention governing these inputs is stated explicitly: the frozen per-model inputs were originally deposited by the v0.31 phase, whose paper is withdrawn; those inputs remain valid archived data, and CV-CPC's methodological status is fixed by v1.7 (computation defined; instrument not adopted). All downstream phases, including this one, consume the quantity under that convention.

## 2.2 Metric

CV-CPC = 1/(1+CV) of the per-model recall vector, exactly per the v1.7 computation; higher values indicate greater cross-model consistency. The quantity is a characterization metric, not an adopted instrument. The pinned mechanical note: CV scales approximately as 1/√mean at low recall, mechanically depressing CV-CPC for low-recall units — the contamination the gating hypothesis exists to handle. CV-CPC is computed below the v1.7 adoption floor for characterization purposes; only all-zero recall vectors (undefined CV) are excluded.

## 2.3 Phantom classification

Method anchor: Phantom Brand Persistence as locked at v1.6 and instantiated in the substrate phases. Operational input: the frozen recall-floor flags archived in the v0.31 OSF deposit, consumed as data provenance only; these are the identical flags consumed by v0.33 and v0.34. Flag consistency was verified across all 112 units (status ⟺ recall-mean below floor; zero disagreements). No judgment calls were made at analysis time.

## 2.4 Reconciliation gate

Binding pre-condition, run before any contrast: re-extracted per-model recall and recognition vectors reproduced the v0.33-deposited values bit-for-bit (SHA-256, all five substrates, 112 units), and the v0.20/v0.21/v0.22 vectors reconciled to the v1.7 `r_per_model` column (72 values checked, zero mismatches; anchor scope limited to those three phases per the v0.33 convention). Defined-unit CV-CPC reproduced the frozen archive values exactly (maximum absolute error 0.0 over 55 units).

## 2.5 Enumeration and attrition

Phantom enumeration preceded all contrasts. Of 112 units, 57 are phantom-flagged (v0.19: 8; v0.20: 14; v0.21: 10; v0.22: 10; v0.23: 15). Twenty-eight flagged units have all-zero recall vectors (undefined CV) and are excluded; the analysis set is 29 analyzable phantoms versus 55 non-phantoms (n = 84) across five within-substrate strata. The pre-registered bias statement: this exclusion drops the most mechanically extreme phantoms, attenuating the raw contrast (conservative for the raw arm) and unsigned for the residualized gate, where it stands as a limitation. Per-substrate eligibility (≥4 analyzable phantoms) holds for v0.19, v0.20, v0.21, and v0.23; v0.22 (one analyzable phantom) enters pooled analysis only (Table 1).

| Substrate | Brands | Phantom-flagged | Analyzable | Excluded (all-zero) | Non-phantom | Per-substrate eligible (≥4) |
|---|---|---|---|---|---|---|
| v0.19 audiophile headphones | 16 | 8 | 4 | 4 | 8 | Yes |
| v0.20 skincare | 24 | 14 | 9 | 5 | 10 | Yes |
| v0.21 cosmetics | 24 | 10 | 5 | 5 | 14 | Yes |
| v0.22 automotive | 24 | 10 | 1 | 9 | 14 | No — pooled only |
| v0.23 premium spirits | 24 | 15 | 10 | 5 | 9 | Yes |
| **Total** | **112** | **57** | **29** | **28** | **55** | **4 of 5** |

Table: Per-substrate phantom roster and attrition. {#tbl:roster}

## 2.6 Hypotheses and statistics

All thresholds and rules per the locked pre-registration. H_Phantom_CPC_Signature (PRIMARY, raw arm, manipulation check): phantom-versus-non-phantom contrast on CV-CPC; pooled Cliff's δ over within-substrate cross pairs (pair-count weighted), stratified permutation with labels shuffled within substrate only, 10,000 Monte Carlo draws, two-sided, add-one p-values; CONFIRMED at |δ| ≥ 0.30 with p < 0.05, FALSIFIED at |δ| < 0.15 or reversed sign at p < 0.05, otherwise MARGINAL. The mechanistic annotation (descriptive only) predicts δ < 0. H_Phantom_Beyond_Presence (PRIMARY, gating): rank-residualization of CV-CPC on C_P within substrate, identical pooled contrast on residuals; co-primary control residualizing on recall-mean; binding flip rule — disagreement between controls yields UNDETERMINED with the flip reported as the finding. H_Phantom_Cross_Substrate (SECONDARY): sign consistency of per-substrate δ across eligible substrates, exact binomial, pre-registered as structurally underpowered (unanimity at n = 4 yields p = 0.125). H_Phantom_t2_Stability (TERTIARY, walled): identical pooled contrasts on the v0.34 t₂ wave, descriptive only, quarantined from verdict logic. Sensitivity: leave-one-substrate-out on both PRIMARY verdicts (fragile verdicts reported UNDETERMINED, v0.32 precedent) and threshold reruns at 0.20/0.40. RNG seed 280400; per-statistic derived offsets documented in the deposited methods log.

## 2.7 Scoring-time deviations

Three estimand resolutions were recorded contemporaneously in the deposited methods log and ratified in session review; none alters a locked rule. D1: "pooled Cliff's δ" resolved as within-substrate cross-pair pooling, required for permutation exchangeability. D2: residualization fit over all analyzable units, so the residual carries the contrast. D3: the SECONDARY's per-substrate δ is the raw arm. The locked pre-registration artifact was not modified.

# 3. Results

## 3.1 H_Phantom_CPC_Signature (PRIMARY, raw arm): CONFIRMED — as a manipulation check

The pooled phantom-versus-non-phantom contrast on CV-CPC is large and in the mechanistically annotated direction: Cliff's δ = −0.838 (29 analyzable phantoms vs. 55 non-phantoms; 296 within-substrate pairs), permutation p = 0.0001 (add-one lower bound at 10,000 draws; no draw exceeded the observed statistic). Phantom-flagged brands carry lower CV-CPC. The verdict is stable under leave-one-substrate-out resampling (δ ∈ [−0.932, −0.786]) and unchanged at the 0.20 and 0.40 sensitivity thresholds. Per the locked inferential-weight statement, this result is reported as a manipulation check: the phantom flag is defined by recall-floor status and CV-CPC is mechanically depressed at low recall mean, so a large raw contrast confirms that the pipeline reproduces the known mechanical coupling — it is not evidence of a Consistency-flavored phantom signature.

![Raw-arm contrast: pooled Cliff's δ with leave-one-substrate-out range against the locked verdict thresholds. H_Phantom_CPC_Signature is CONFIRMED as a manipulation check only.](../../reports/figs/v37/chart_03_raw_manipulation_check.pdf){#fig:rawarm width=100%}

## 3.2 H_Phantom_Beyond_Presence (PRIMARY, gating): UNDETERMINED — control flip; the flip is the finding

The gate's two co-primary controls return opposite verdicts. Residualized on C_P, the contrast survives essentially undiminished: δ_resid = −0.797, p = 0.0001 — CONFIRMED. Residualized on recall-mean, it vanishes: δ_resid = +0.068, p = 0.655 — FALSIFIED. Under the binding pre-registered flip rule, the gate verdict is UNDETERMINED, and the disagreement between controls is the reportable finding.

The mechanism is identified in the per-substrate covariate diagnostics rather than conjectured. Recognition is saturated — C_P constant across all analyzable units — in three of five substrates (v0.21, v0.22, v0.23). A constant covariate removes nothing under residualization, so the C_P control is inert exactly where the contrast lives and inherits the raw signal. The recall-mean control, by contrast, removes the axis that defines the phantom flag, and the residual contrast collapses to zero. The flip is stable: it persists across all five leave-one-substrate-out runs (C_P arm δ_resid ∈ [−0.87, −0.77], all p = 0.0001; recall-mean arm δ_resid ∈ [−0.04, +0.11], all non-significant), with the control disagreement itself present in every leave-out.

The substantive reading is symmetric and deflationary in both directions. The C_P-control result does not establish a beyond-Presence signature, because the control had no variance to remove in most of the panel; the recall-mean-control result does not establish pure mechanical redundancy, because that control removes the defining axis of the classification and would null a genuine signature co-located with it. What the pair establishes — with pre-registered confirmatory status — is that the verdict on a recall-coupled quantity is not invariant to the choice between a recognition-anchored control and the mechanical driver itself. A binary, saturating recognition signal cannot govern this metric.

![The gate flip: identical residualized contrast under the two co-primary controls, with opposite verdicts. H_Phantom_Beyond_Presence is UNDETERMINED under the pre-registered flip rule.](../../reports/figs/v37/chart_01_gate_flip.pdf){#fig:gateflip width=100%}

![Mechanism of the flip: C_P collapses to a constant in three of five substrates (control no-op), while recall-mean separates phantom from non-phantom units in every substrate.](../../reports/figs/v37/chart_02_recognition_saturation.pdf){#fig:saturation width=100%}

## 3.3 H_Phantom_Cross_Substrate (SECONDARY): UNINFORMATIVE — unanimous direction, structurally underpowered

All five per-substrate raw-arm contrasts are negative and concordant: v0.19 −0.938, v0.20 −0.956, v0.21 −0.886, v0.22 −1.000 (one analyzable phantom; non-inferential), v0.23 −0.622. Among the four eligible substrates the exact binomial sign test gives 4/4 concordance at p = 0.125 — the pre-registered structural floor: unanimity at n = 4 cannot reach significance. The verdict is recorded as UNINFORMATIVE per the pre-acknowledged underpower convention; the descriptive concordance is reported for completeness.

![Per-substrate raw-arm δ: unanimous negative direction; v0.22 non-inferential at one analyzable phantom; exact binomial floor p = 0.125 at n = 4 eligible substrates.](../../reports/figs/v37/chart_04_cross_substrate_concordance.pdf){#fig:crosssubstrate width=100%}

## 3.4 H_Phantom_t2_Stability (TERTIARY, walled): the full structure reproduces

Computed descriptively on the v0.34 t₂ wave — a near-replica panel (0.98 phantom persistence; no independence claimed) — the entire result structure recurs: raw δ = −0.815; C_P-control δ_resid = −0.791; recall-mean-control δ_resid = +0.062, non-significant. The flip replicates across waves, and the per-substrate negative direction is again unanimous (5/5). Two panel-composition facts are distinguished: no t₁ analysis-set unit is absent from the t₂ panel (zero attrition at the panel level), while the analyzable phantom set is recomputed from t₂ recall and expands from 29 to 33 units, as four t₁ all-zero phantoms exhibit non-zero recall at t₂. The check is quarantined from all verdict logic per the lock; its contribution is test-retest evidence that the flip is a stable property of the measurement structure rather than a single-wave artifact.

![Test-retest stability: t₁ and t₂ values of the raw contrast and both gate controls. The flip — large under the C_P control, null under the recall-mean control — reproduces across waves.](../../reports/figs/v37/chart_05_t2_stability.pdf){#fig:t2stability width=100%}

## 3.5 Sensitivity summary

Both PRIMARY verdicts survive leave-one-substrate-out resampling in full: the raw arm remains CONFIRMED in all five leave-outs, and the gate's control disagreement persists in all five — the UNDETERMINED verdict is robust, not an artifact of any single substrate. Threshold reruns at 0.20 and 0.40 leave every verdict unchanged. The RNG seed (280400), per-statistic offsets, and draw counts are recorded in the deposited verdicts file and methods log.

# 4. Discussion

## 4.1 The flip as the finding

The central result of this study is not a verdict about phantom brands but a verdict about the instrument: the gate's conclusion is not invariant to the choice of control. Residualizing on the construct-level Presence measure (C_P) leaves the phantom contrast essentially intact; residualizing on the metric's mechanical driver (recall-mean) eliminates it. Both arms are stable, survive leave-one-substrate-out resampling — with the disagreement itself present in every leave-out — and reproduce on the t₂ wave. Under the pre-registered flip rule this yields UNDETERMINED, and the disagreement carries more methodological information than either verdict alone would have. The v1.7 negative result established that CV-CPC is Presence-coupled at the correlation level (ρ = 0.77); the present study escalates that finding to the verdict level, demonstrating that the coupling is consequential: it changes confirmatory conclusions depending on how it is controlled.

## 4.2 Why the recognition control fails

The diagnostic mechanism generalizes beyond this phase. C_P is a six-level count of binary recognitions, and among analyzable units it saturates to a constant in three of five substrates — the comparator (non-phantom) population sits at the recognition ceiling almost everywhere consumer brands are studied. This is the same ceiling that collapsed the beyond-Presence gates in v0.34's longitudinal design; the present study shows that restricting attention to phantom-adjacent contrasts does not rescue the gate, because the control must vary in the joint analysis set, and the non-phantom side anchors it at ceiling. A binary, saturating recognition signal is structurally incapable of serving as the Presence control for a recall-coupled quantity. This is the concrete, pre-registered case for the two requirements already mandated for the v1.8 methodology revision: a mean-independent Consistency instrument, and a graded recognition signal with variance where contrasts live.

## 4.3 The substantive question remains open — and is currently undecidable

Whether phantom-flagged brands carry a Consistency signature distinct from their Presence deficit is neither confirmed nor refuted here. The recall-mean control's null is not evidence of absence: that control removes the axis defining the classification and would null a genuine signature co-located with it. The C_P control's confirmation is not evidence of presence: the control was inert. The honest statement is that CV-CPC, governed by the available controls, cannot decide the question — which converts the phantom-signature hypothesis from an open empirical question into a designated re-test target for the v1.8 instrument.

## 4.4 Concordance as description

The unanimous negative direction across all five substrates reproduces at t₂ (5/5 in both waves; magnitudes vary). This pattern is descriptively consistent with a single mechanical generator — CV's mean-dependence — operating uniformly across categories. Nothing in the cross-substrate pattern requires a category-specific or signature-like explanation, which is itself a deflationary observation worth carrying into the v1.8 design discussion.

# 5. Limitations

Attrition is the largest internal limitation: 28 of 57 phantom-flagged units have all-zero recall vectors, undefined CV, and are excluded. The exclusion is conservative for the raw arm but unsigned for the gate, and it removes precisely the most extreme members of the classification; the analyzable phantom set is the moderate phantom population. Second, the operational classification is the frozen recall-floor flag, which captures below-floor recall status rather than verified phantom status in the Phantom Brand Persistence sense — the analyzable set plausibly mixes genuinely defunct or displaced brands with low-salience live brands, and the present design cannot separate them. Third, this is a re-analysis of frozen inputs whose tertiary ancestors partly motivated the hypothesis; the t₂ check is test-retest evidence on a near-replica panel, not independent replication. Fourth, substrate-level inference rests on five consumer categories measured in English on a single six-model panel at a single pair of time points; the SECONDARY hypothesis was structurally underpowered by design and reported as such. Fifth, CV-CPC itself holds characterization status only, and C_P's six-level coarseness — the proximate cause of the saturation diagnosed here — bounds what any analysis conditioned on it can conclude. Finally, three scoring-time estimand resolutions (D1–D3) were made at analysis time; each is the statistically mandated reading and all were contemporaneously documented, but they were not literally pinned in the locked text.

# 6. Future Research

The direct successor is the v1.8 methodology revision, for which this study supplies two design requirements with pre-registered empirical backing: the Consistency instrument must be mean-independent (the recall-mean control's annihilation of the contrast is the demonstration), and the Presence control must be graded with variance in the populations where contrasts are evaluated (the C_P saturation no-op is the demonstration; signal-detection-style graded recognition of the kind examined in the v0.28 validator work is one candidate). Once a v1.8-compliant instrument exists, the phantom-signature hypothesis returns as a designated re-test (roadmapped as the CPC × Phantom Brand Persistence phase), with the present study's frozen analysis set available as the comparison baseline. Two further extensions follow naturally: a classification refinement separating defunct/displaced phantoms from low-salience live brands within the below-floor population, and the regime-emergence question of whether Consistency, once properly instrumented, exhibits typology structure of its own.

# Declarations {-}

## Conflict of interest {-}

The author is employed full-time as Director, Corporate Brand Creative and Governance, at Samsung Electronics America. v0.37 reuses the v0.19–v0.23 registries and inherits their conflict-of-interest screen (pre-registration DEVIATIONS Entry 0). Samsung subsidiaries hold tier-2/3 component supply relationships with several brands in the reused registries: Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment). These are non-competitive supply relationships; Samsung Electronics America does not produce or market passenger car brands and has no brand-level competitive overlap with any registry entry. No operational restriction on registry composition was imposed. Separately, AKG was substituted with Denon before the v0.19 pre-registration lock (AKG owned by Harman International, a Samsung subsidiary, since 2016) to avoid any appearance of conflict; the substitution preserved Cell A_Heritage's eight-brand composition, occurred prior to lock, and was AKG only (not JBL). Samsung had no role in study design, analysis, or reporting. The author's primary academic affiliation for this research is the School of Visual Arts MPS Branding Program; the research entity maintaining the data archive and methodology venue is Third System™.

## Funding {-}

Self-funded.

## Ethics {-}

Not applicable; no human subjects; the study analyzes archived outputs of public LLM APIs.

## Data and code availability {-}

All pre-registration artifacts, frozen input reconciliation logs, the phantom roster, scoring code, verdicts file, and figures are deposited at osf.io/ec6wh (v37/). The pre-registration is locked at git tag `v0.37-prereg-r1`, externally anchored prior to analysis. Upstream phase and methodology papers are indexed in the cross-citation registry (see `_upstream_phases.md`).

# References {-}

González Castro, P. U. (2025). *Tri-System Brand Growth*. SSRN 6659000.

González Castro, P. U. (2026). *Construct Validity and Four-Regime Taxonomy*. AIAS Protocol v1.2. SSRN 6761698.

González Castro, P. U. (2026). *Phase A Pivot-Validation Specification*. AIAS Protocol v1.3. SSRN 6797679.

González Castro, P. U. (2026). *Recognition × Recall Decomposition*. AIAS Protocol v1.4. SSRN 6799479.

González Castro, P. U. (2026). *Multi-Statistic C2 and Two-Channel Recall*. AIAS Protocol v1.5. SSRN 6810758.

González Castro, P. U. (2026). *Substrate Pre-Screening, Independent Moderator, Phantom Extension*. AIAS Protocol v1.6. SSRN 6816340.

González Castro, P. U. (2026). *CPC Consistency --- Pre-Registered Negative Result (CV not independent of Presence)*. AIAS Protocol v1.7. SSRN 6878818.

González Castro, P. U. (2026). *Five-Substrate Foundational Construct Claim*. AIAS 1.0. SSRN 6817841.

González Castro, P. U. (2026). *AI Presence in Kitchen knives: AIAS v0.16*. SSRN 6791999.

González Castro, P. U. (2026). *AI Presence in Premium kitchenware: AIAS v0.17*. SSRN 6802261.

González Castro, P. U. (2026). *AI Presence in Indie fragrance: AIAS v0.18*. SSRN 6806558.

González Castro, P. U. (2026). *AI Presence in Audiophile headphones: AIAS v0.19*. SSRN 6809182.

González Castro, P. U. (2026). *AI Presence in Skincare: AIAS v0.20*. SSRN 6811441.

González Castro, P. U. (2026). *AI Presence in Cosmetics: AIAS v0.21*. SSRN 6815378.

González Castro, P. U. (2026). *AI Presence in Automotive: AIAS v0.22*. SSRN 6829118.

González Castro, P. U. (2026). *AI Presence in Premium spirits: AIAS v0.23*. SSRN 6834298.

González Castro, P. U. (2026). *AI Presence in B2B SaaS: AIAS v0.24*. SSRN 6838802.

González Castro, P. U. (2026). *B2B SaaS Construct Validity: AIAS v0.25*. SSRN 6842138.

González Castro, P. U. (2026). *Amazon BSR Discriminant Validity: AIAS v0.26*. SSRN 6847678.

González Castro, P. U. (2026). *B2B SaaS Convergent Validity: AIAS v0.27*. SSRN 6854758.

González Castro, P. U. (2026). *AI Availability is Not Reducible to Recognition Memory --- and is Underpowered Against Familiarity at n = 24: AIAS v0.28*. SSRN 6865478.

González Castro, P. U. (2026). *The Presence Component Is Construct-Valid: AIAS v0.29*. SSRN 6870778.

González Castro, P. U. (2026). *Recognition Saturates, Consistency Doesn't — An Instrument-Specification Pilot of the AIAS Consistency Component (CPC): AIAS v0.30*. SSRN 6875319.

González Castro, P. U. (2026). *Version-Snapshot Stability of an AI-Presence Consistency Score: AIAS v0.32*. SSRN 6898581.

González Castro, P. U. (2026). *Provider-Asymmetric Consistency in AI Brand Availability: AIAS v0.33*. SSRN 6909019.

González Castro, P. U. (2026). *Two-Wave Temporal Stability of an AI Brand-Recall Consistency Quantity: AIAS v0.34*. SSRN 6915458.
