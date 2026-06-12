---
title: "Does Cross-Platform Consistency Have Regime Structure?"
subtitle: "A Pre-Registered Clustering Test Against a Frozen Brand-Presence Classification"
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

{\LARGE \textbf{Does Cross-Platform Consistency Have Regime Structure?}}\\[8pt]

{\large A Pre-Registered Clustering Test Against a Frozen Brand-Presence Classification\\ (AIAS™ CPC, v0.36)}\\[28pt]

Pablo Ulpiano González Castro\\[4pt]
School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System™ (research entity; data archive and methodology venue)\\[8pt]
Correspondence: pablou@pablou.com · pablou.com\\
ORCID: 0009-0003-8968-9990\\[20pt]

Pre-registration: \texttt{v0.36-prereg-r1} (locked before analysis); amended \texttt{r2} (corrections, outcome-blind) and \texttt{r3} (post-results deviations log)\\
Data and code: OSF \texttt{ec6wh/v36}\\

\end{center}
\end{titlepage}

# Abstract {-}

Whether cross-platform consistency (CPC) — the uniformity of a brand's recall across large language models — carries diagnostic structure of its own, or merely reflects the brand-presence hierarchy, is an open question for AI-availability measurement. This study pre-registered a clustering test on fully frozen inputs: 112 brand-units across five consumer substrates, a fixed six-model panel, and the CV-based CPC characterization quantity assessed (and not adopted) by Protocol v1.7. Four hypotheses were locked before any statistic was computed: regime inheritance (H_RegimeInheritance), autonomous structure (H_RegimeAutonomy), residual structure after Presence removal (H_ResidualStructure), and saturation degeneracy (H_SaturationDegeneracy), with a four-cell verdict matrix predicting borrowed structure (Cell A). The result falsified the prediction: the phase landed in Cell D (unstructured). No hypothesis met its locked bar — inheritance was unevaluable at power after a CV computability floor removed 15 of 24 units in the label-bearing substrate; saturation reversed direction (saturated substrates exhibited greater CPC dispersion, Levene p = .003); omnibus structure (k = 3) fell just short of the silhouette threshold (0.2422 vs 0.25); and structure emerged only in a sensitivity arm that removed mean recall entirely. The failure modes converge on mean-coupling pathology in the CV instrument, motivating the v1.8 mean-independent specification. Pre-scoring amendments — three corrections (data-lineage, construct-identity, and scope-assignment) and a recognition-commensurability finding — are documented in the deposited record.

**Keywords:** brand availability; large language models; cross-platform consistency; pre-registration; cluster analysis; construct validity; measurement; AI Availability; Ehrenberg-Bass; AIAS

**JEL codes:** M31; L86; L15; D83; M37

**Paper status:** Working paper. Phase v0.36 of the AIAS™ Measurement Program; pre-registered at tag `v0.36-prereg-r1` prior to analysis, amended at `r2` (outcome-blind corrections) and `r3` (post-results deviations-log addition).

# 1. Introduction

The AIAS™ Measurement Program treats a brand's standing inside large language models as a third availability system alongside the Ehrenberg-Bass constructs of mental and physical availability. Its Presence component is anchored on a five-substrate empirical base under Protocol v1.6 (SSRN 6816340); consistency (CPC) is the candidate second component, currently represented by a CV-based characterization quantity that Protocol v1.7 (SSRN 6878818) assessed and declined to adopt, on the evidence of strong coupling with Presence (ρ = 0.77).

Four prior results constrain any consistency instrument. The v1.7 study measured the Presence-coupling directly; the v0.33 phase (SSRN 6909019) found the Beyond-Presence gate collapsing under recognition saturation; the v0.34 phase (SSRN 6915458) found residualization a structural no-op under recognition ceilings; and the v0.35 phase (SSRN 6921758) returned a pre-registered control-flip in the phantom-brand contrast. Each implicates the same mechanism — the coefficient of variation's dependence on the recall mean it divides by.

What none of these results addresses is whether CPC exhibits *regime structure*: whether brands cluster into discrete consistency types, and if so, whether those types are the Presence hierarchy under another name (inheritance), an independent typology (autonomy), or absent altogether. The question matters in both directions. Inheritance would add a fifth convergent line to the mean-independence requirement; autonomy would establish that consistency carries diagnostic content even in its flawed CV form.

The study is a fully retrospective, pre-registered re-analysis: frozen per-model recall vectors for 112 brand-units across five substrates; Ward clustering with gap-statistic model selection; agreement against the only per-brand four-valued brand classification existing in frozen form (the v0.23 Presence-quartile regime; SSRN 6834298); residualization and saturation tests; all thresholds, decision rules, and predictions locked and deposited before any statistic was computed.

The pre-registered prediction (Cell A, borrowed structure) was falsified; the phase landed in Cell D (unstructured), and the paper reports the miss as scored. Three contributions follow. First, the falsification itself, whose failure modes are individually diagnostic of mean-coupling pathology: a computability floor that silently disqualifies low-recall brands, a direction-reversed saturation result mechanically consistent with a ratio metric, and structure that appears only when the mean is removed. Second, a construct-identity audit: "regime" is shown to be overloaded across three distinct constructs in the program's own record — the Protocol v1.2 substrate-level taxonomy (SSRN 6761698), the v0.23 per-brand Presence-quartile classification, and a hypothesis-label family — a conflation the pre-registration record corrects transparently. Third, a recognition-commensurability finding: the program's instrument evolution from binary to graded recognition renders the graded-recognition Presence composite uncomputable for earlier substrates, independently reinforcing the graded-signal requirement for the v1.8 specification.

Section 2 details data lineage, the construct disambiguation, scope assignment, and the locked procedure; Section 3 reports the four verdicts; Section 4 develops the instrument-pathology interpretation under explicit post-hoc labeling; Sections 5 and 6 treat limitations and designated future work.

# 2. Method

## 2.1 Data and lineage

The study consumes frozen inputs only; it issues no new LLM acquisition calls. The clustering feature is the per-brand six-model recall vector for the five panel-uniform omnibus substrates — v0.19 audiophile headphones, v0.20 skincare, v0.21 cosmetics, v0.22 automotive, v0.23 premium spirits; 112 brand-units in all — read from the frozen `v33_eta2.csv` deposit, which carries the per-model recall and recognition vectors in canonical six-model panel order. The CPC quantity is CV-CPC = 1/(1+CV) of that vector, in the characterization status fixed by Protocol v1.7 (computation defined; instrument not adopted). The lineage of the per-model inputs traces to the v0.31 phase; that paper is withdrawn and is cited here as archived data via its OSF deposit only, not as methodological authority, following the consumption convention of the v0.33–v0.35 arc. The regime target and the Presence composite are read as frozen fields from the v0.23 deposit (`brand_details[].regime` and `composite_presence`), present for v0.23 alone, a constraint the pre-registration documents rather than papers over (§2.2). The v0.35 frozen 84-unit analysis set enters as a verdict-concordance check only.

## 2.2 Construct disambiguation

"Regime" denotes three distinct constructs in the program's record, and they must not be conflated. (i) The Protocol v1.2 *Four-Regime Taxonomy* (SSRN 6761698) is a per-substrate classification of the AI-Presence × Google-Trends construct-validity relationship; it is not a per-brand label, is defined by external trend data, and is unassigned for the consistency substrates. (ii) The v0.23 per-brand *regime* (Dominant / Established / Emerging / Absent) is a within-substrate Presence-composite quartile classification — the only per-brand four-valued classification existing in frozen form, present for v0.23 only. (iii) `H_Regime4_*` in earlier substrate verdicts is a hypothesis-label family, not a per-brand classification. The operative target of this phase is construct (ii). The initial pre-registration mis-cited construct (i) as the per-brand label source; the correction was made at amendment (§2.3) and is preserved in the deposited record.

## 2.3 Pre-registration record

Hypotheses, thresholds, decision rules, the verdict matrix, and all predictions were locked at the initial tag (`v0.36-prereg-r1`) and deposited before any statistic was computed; none was subsequently changed. The first amended tag (`v0.36-prereg-r2`) carries three corrections — the data-lineage defect, the construct-identity correction of §2.2, and the assignment of each locked criterion to its maximal executable scope — and a recognition-commensurability finding, together with the extension of the gap-statistic range to k = 1 through 8 and the seed-bearing scoring code; these amendments were authored outcome-blind, as the deposited deviations log attests, though the r2 deposit timestamp postdates the deterministic scoring run. A second amended tag (`v0.36-prereg-r3`) is, by contrast, a post-results deviations-log addition and is labeled as such: it records that the locked sensitivity arms were executed in a deterministic second pass after primary verdicts existed (§3.5), with no evidentiary parameter changed. The integrity claim therefore rests on the r1 lock for all evidentiary parameters, the attested outcome-blind authorship of the r2 corrections, and the explicit post-results labeling of r3. All tags and deposits are public.

## 2.4 Feature space and clustering procedure

The primary feature is the six-dimensional per-model recall vector — the per-model components from which CV-CPC is formed — z-scored within substrate per model; the scalar CV-CPC is a sensitivity feature. The analysis set is the units with computable CV-CPC (mean recall ≥ 1.0); units below that floor have undefined CV and are excluded and counted per substrate. Clustering is Ward hierarchical with Euclidean distance on the standardized features. The number of clusters is selected by the gap statistic (Tibshirani's one-standard-error rule; uniform reference over the feature bounding box; B = 500 reference samples) computed over k = 1 through 8, with k = 1 selectable so the unstructured and degeneracy verdicts are expressible. Cluster validity against the regime labels uses the adjusted Rand index, evaluated against a permutation null of 10,000 within-substrate label shuffles; internal validity uses the mean silhouette against the same within-substrate permutation null. All stochastic steps run under a single fixed seed (36); the adjusted Rand index, silhouette, gap, and k-means routines are implemented in-script without external machine-learning dependencies, and the deposited verdicts reproduce bit-for-bit from the locked, tagged scorer. Three pre-specified robustness arms accompany the primary procedure: a scalar CV-CPC feature arm, a k-means concordance arm at the gap-selected k (50 restarts), and a verdict-concordance check on the v0.35 frozen 84-unit set; all are reported in §3.5 and none is verdict-determining.

## 2.5 Hypotheses, criteria, scopes, and verdict matrix

Four hypotheses were locked, each evaluated at its maximal executable scope. **H_RegimeInheritance** (scope: v0.23, the label-bearing substrate): cluster structure recovers the per-brand regime classification — supported iff the adjusted Rand index against the regime labels is at least 0.30 and exceeds the 99th percentile of the permutation null (p < 0.01). **H_RegimeAutonomy** (scope: omnibus internal-structure legs over all 112 units, with the agreement leg on v0.23): clusters carry internally valid structure independent of the regime labels — supported iff the gap selects k ≥ 2, the mean silhouette is at least 0.25 and exceeds the 95th percentile of the null, and the adjusted Rand index is below 0.30; it is mutually exclusive with inheritance. **H_ResidualStructure** (scope: v0.23 primary, residualized on the Presence composite; with an omnibus mean-recall sensitivity arm): cluster structure survives residualization on Presence — supported iff the autonomy internal-validity criteria hold on the residual vector. **H_SaturationDegeneracy** (scope: omnibus): CPC structure collapses under recognition saturation — supported iff (a) within-substrate CPC variance is lower in saturated than unsaturated substrates by a directional Brown-Forsythe test at p < 0.05, and (b) the within-substrate gap resolves k = 1 in a majority of saturated substrates while resolving k ≥ 2 in a majority of unsaturated substrates. The verdict matrix maps inheritance and residual structure onto four cells: Cell A borrowed structure (inheritance, no residual), Cell B layered structure (inheritance, residual), Cell C autonomous structure (autonomy, residual), Cell D unstructured (neither, no residual). The pre-registered prediction was Cell A.

## 2.6 Saturation classification

The operative saturated-substrate list is the v0.34 `saturation_flagged` enumeration (≥ 90% per-model recognition among defined brands): saturated = v0.20 skincare, v0.21 cosmetics, v0.22 automotive, v0.23 premium spirits; unsaturated = v0.19 audiophile headphones. A secondary observation — the v0.35 per-substrate covariate-constant flag (C_P constant across brands: v0.21, v0.22, v0.23) — is recorded as a sensitivity caveat: skincare (v0.20) is recognition-saturated under v0.34 but not covariate-constant under v0.35. The majority tests of H_SaturationDegeneracy use the v0.34 operative list.

# 3. Results

## 3.0 Verdict-matrix landing

The phase landed in Cell D (unstructured) against the pre-registered Cell A (borrowed structure). No hypothesis met its locked criterion; the residual-structure prediction was the single sub-call that held. Figure 1 summarizes the landing.

![The locked verdict matrix. The pre-registered prediction was Cell A (borrowed structure: H_RegimeInheritance supported, H_ResidualStructure not supported); the observed verdicts place the phase in Cell D (unstructured). The right ribbon reports each hypothesis verdict at its locked scope.](../../reports/figs/v36/chart_05_verdict_matrix.pdf){#fig:matrix width=100%}

## 3.1 H_RegimeInheritance — not supported (unevaluable at adequate power)

The CV-CPC computability floor (mean recall < 1.0) left 9 of 24 premium-spirits units defined. On the surviving units, the gap statistic selected k = 1; with a single cluster, the adjusted Rand index against the Presence-quartile regime labels is 0 by construction (observed ARI = 0.0, 0th percentile of the permutation null, p = 1.0). The locked criterion is not met. The verdict is recorded as-scored, with the explicit qualification that a forced single-cluster solution on nine units constitutes a failure of evaluability rather than evidence against inheritance; §4.1 develops the point that the floor itself — disqualification of precisely the low-recall brands — is the instrument-diagnostic content of this result.

![H_RegimeInheritance, scope v0.23 (n = 9 defined). Left: the computability floor reduces the 24-unit substrate to 9 units with defined CV-CPC. Right: the gap statistic on the surviving units selects k = 1, forcing ARI = 0 against the frozen Presence-quartile regime labels.](../../reports/figs/v36/chart_02_inheritance_floor.pdf){#fig:inheritance width=100%}

## 3.2 H_RegimeAutonomy — not supported

On the 112-unit omnibus, the gap statistic selected k = 3 and the observed mean silhouette (0.2422) exceeded the 95th percentile of its within-substrate permutation null; the v0.23 agreement leg (ARI < 0.30) was also satisfied. The silhouette criterion, however, fell below the locked 0.25 threshold, and the hypothesis is therefore not supported. No threshold was relaxed. The configuration — structure above chance, below the evidentiary bar — is reported per component and scope in Figure 3 and taken up descriptively in §4.3.

![H_RegimeAutonomy internal-structure legs, scope omnibus (n = 112). Left: gap curve over k = 1 to 8 with one-standard-error bars; k = 3 selected. Right: observed mean silhouette (0.2422) against the permutation-null distribution; the observed value exceeds the 95th-percentile null but falls below the locked 0.25 threshold.](../../reports/figs/v36/chart_01_omnibus_structure.pdf){#fig:omnibus width=100%}

## 3.3 H_ResidualStructure — not supported (as predicted)

On the primary scope, residualizing the per-model CPC vector on the frozen v0.23 Presence composite and reclustering yielded k = 1: no residual structure, matching the locked prediction. The pre-specified omnibus sensitivity arm — residualization on per-brand mean recall, never verdict-determining — selected k = 2 with the internal-validity criteria met. The divergence is reported in full: the one configuration in which structure satisfies the locked internal criteria is the configuration in which the recall mean has been removed from the signal entirely (§4.3).

![H_ResidualStructure, primary scope v0.23 versus the pre-specified omnibus sensitivity arm. Left: residualization on composite_presence yields k = 1 (no residual structure; locked verdict basis). Right: the sensitivity-only omnibus arm residualizing on per-brand mean recall yields k = 2 with internal-validity criteria met; this arm is never verdict-determining.](../../reports/figs/v36/chart_04_residual_divergence.pdf){#fig:residual width=100%}

## 3.4 H_SaturationDegeneracy — not supported (direction reversed)

Within-substrate CPC dispersion was *higher* in saturated substrates (0.095) than in the unsaturated substrate (0.024); the two-sided Levene test rejects equality at p = .003 with the sign opposite to the locked direction, and the directional Brown-Forsythe test accordingly fails (p = .9997). Criterion (b) also fails: per-substrate gap resolution was k = 2/3/2/4/1 across v0.19–v0.23 — the saturated substrates mostly resolve multiple clusters, while the single k = 1 occurs in saturated premium spirits. The pre-registered degeneracy prediction is reversed, not merely unmet.

![H_SaturationDegeneracy, scope omnibus. Within-substrate CPC dispersion by substrate (saturated per the operative v0.34 classification): saturated substrates carry greater dispersion (0.095 vs 0.024), reversing the pre-registered direction; Levene p = .003 with opposite sign, Brown-Forsythe directional p = .9997, criterion (b) failed.](../../reports/figs/v36/chart_03_saturation_reversal.pdf){#fig:saturation width=100%}

## 3.5 Sensitivity and robustness

The scalar CV-CPC feature arm selected k = 1 (ARI = 0.0 against the 6-dim primary), locating the weak omnibus structure in the multivariate per-model signal rather than the scalar summary. K-means at the gap-selected k = 3 (50 restarts) recovered the Ward partition at ARI = 0.43, moderate concordance consistent with a weak three-cluster solution. The pre-registered v0.35 84-unit concordance check was **discordant**: under the inclusion floor (mean recall > 0, n = 84) the omnibus silhouette rose to 0.350, clearing the 0.25 threshold, so the autonomy criteria were met and the configuration mapped to no defined matrix cell — the Cell D verdict is sensitive to the recall floor, a dependence that is itself diagnostic (§4.3). These three arms were executed in a deterministic second pass after the primary verdicts existed and are labeled accordingly in the deposited record (§2.3; deviations-log Entry 5). Determinism: the deposited verdicts reproduce bit-for-bit from the tagged scorer at seed 36.

# 4. Discussion

The pre-registered prediction was falsified. The interpretation developed in this section is post hoc: it is proposed as explanation, not as vindication of the locked prediction, and §6 states the falsifiable commitments it generates.

## 4.1 The computability floor

CV-CPC is undefined wherever mean recall falls below the locked floor, and §3.1 shows the consequence: fifteen of twenty-four units in the only label-bearing substrate were disqualified before the inheritance test could run. The floor is not incidental to the instrument; it is the instrument's mean-dependence expressed as a coverage rule. A consistency diagnostic that ceases to exist precisely for low-recall brands cannot classify the segment for which a consistency reading would carry the greatest diagnostic value. The inheritance verdict is therefore read as a failure of evaluability with an instrument-diagnostic cause, not as evidence about the relation between consistency and the Presence hierarchy.

## 4.2 The saturation reversal

The degeneracy hypothesis predicted that recognition-saturated categories would compress CPC variation; the observed dispersion ordering reversed, significantly. A mechanical account is available: the coefficient of variation inflates as its denominator shrinks, and saturated categories — recognition at ceiling, recall still heavy-tailed — supply long low-recall tails in which that ratio both explodes and varies across brands. On this account the reversal indexes instrument behavior, not brand-level consistency structure. The account is falsifiable and is registered here as a commitment: a mean-independent consistency instrument should not reproduce the reversal on the same frozen inputs. If it does, the mechanical explanation fails and the reversal demands a substantive one.

## 4.3 The mean-removal signature

Across every configuration examined, the internal-validity criteria for cluster structure are satisfied in exactly two: the pre-specified omnibus arm in which per-brand mean recall is residualized out of the signal (§3.3), and the v0.35-floor robustness arm in which the computability threshold is loosened from adoption (mean recall ≥ 1.0) to inclusion (mean recall > 0) and the omnibus silhouette rises from 0.2422 to 0.350 (§3.5). The pattern admits a single description: such structure as the CV signal carries becomes visible where the mean's grip on the measurement loosens, and is suppressed — or rendered undefined — where it binds. The headline verdict is itself an instance: Cell D holds at the stricter floor and dissolves at the looser one, and the floor is a mean threshold. The verdict's floor-dependence is reported as the phase's most instrument-diagnostic single result.

## 4.4 The audit findings

Two corrections in the pre-registration record are findings in their own right. First, "regime" was shown to denote three distinct constructs in the program's record — a substrate-level external-validity taxonomy, a per-brand Presence-quartile classification, and a hypothesis-label family — and the initial registration conflated the first two. The disambiguation is a construct-hygiene contribution independent of any verdict. Second, the program's instrument evolution from binary to graded recognition leaves the graded-recognition Presence composite uncomputable for four of the five substrates from any frozen artifact: a commensurability break that independently entails the graded-recognition requirement already motivated on other grounds.

## 4.5 Convergence

Five lines of evidence now bear on the consistency component: the v1.7 Presence-coupling measurement (ρ = 0.77), the saturation collapse of the Beyond-Presence gate (v0.33), the structural no-op of residualization under recognition ceilings (v0.34), the pre-registered control-flip (v0.35), and the four-pathology pattern of the present phase — undefined coverage at low recall, a mechanically explicable direction reversal, structure visible only under mean removal, and a floor-dependent headline verdict. Jointly they do more than motivate the v1.8 specification; they constrain it. The successor instrument must be mean-independent, must consume a graded recognition signal, and must be defined over the low-recall segment the CV floor excludes. The first two requirements were established before this phase; the third is its addition.

# 5. Limitations

Six limitations bound the claims. The inheritance test ran on nine defined units in a single substrate and is reported as unevaluable at adequate power rather than as evidence; nothing in this paper bears on whether consistency clusters would recover a presence classification under an instrument with full coverage. The regime target itself exists for one substrate only, so even a fully powered test would have been a single-substrate result. The locked verdict matrix proved non-exhaustive: an autonomy-supported, residual-absent configuration maps to no cell — a design gap the primary run masked and the robustness arm exposed, recorded here as a pre-registration design lesson rather than repaired post hoc. The headline verdict is floor-sensitive (§3.5, §4.3) and is accordingly stated as a verdict at the locked floor, not as a floor-invariant fact. The locked robustness arms were executed in a deterministic second pass after primary verdicts existed; the deposited record labels this deviation as not outcome-blind (Entry 5), and no primary verdict depends on it. Finally, the design is fully retrospective and the consistency quantity holds characterization status only under Protocol v1.7; every claim is therefore bounded to the CV instrument, not to consistency as a construct.

# 6. Future Research

Four designations follow. First, the v1.8 mean-independent consistency instrument, with the regime-emergence question designated for re-test under it; any successor must explain three observations this phase leaves standing — the faint omnibus three-cluster signature, the 0.350 silhouette at the inclusion floor, and the floor-dependence of the verdict itself. Second, a common-protocol graded-recognition re-scoring of all anchored substrates, which would materialize the omnibus per-brand regime target this phase could not have. Third, assignment of the Protocol v1.2 substrate-level taxonomy to the consistency substrates, which requires new external trend-data acquisition and was explicitly out of retrospective scope. Fourth, at the program level: verdict matrices should be checked for exhaustiveness over the reachable outcome space at pre-registration — the institutional lesson of Entry 5.

# Declarations {-}

## Conflict of interest {-}

The author is employed full-time as Director, Corporate Brand Creative and Governance, at Samsung Electronics America. v0.36 reuses the v0.19–v0.23 registries and inherits their conflict-of-interest screen (pre-registration DEVIATIONS Entry 2). Samsung subsidiaries hold tier-2/3 component supply relationships with several brands in the reused registries: Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment). These are non-competitive supply relationships; Samsung Electronics America does not produce or market passenger car brands and has no brand-level competitive overlap with any registry entry. No operational restriction on registry composition was imposed. Separately, AKG was substituted with Denon before the v0.19 pre-registration lock (AKG owned by Harman International, a Samsung subsidiary, since 2016) to avoid any appearance of conflict; the substitution preserved Cell A_Heritage's eight-brand composition, occurred prior to lock, and was AKG only (not JBL). Samsung had no role in study design, analysis, or reporting. The author's primary academic affiliation for this research is the School of Visual Arts MPS Branding Program; the research entity maintaining the data archive and methodology venue is Third System™.

## Funding {-}

Self-funded.

## Ethics {-}

Not applicable; no human subjects. The study is a fully retrospective re-analysis of archived outputs of public LLM APIs, with no new acquisition.

## Data and code availability {-}

All pre-registration artifacts (tags `v0.36-prereg-r1`, `r2`, `r3`), the verdicts file, clustering intermediates, figures, the brand-format report, and the scoring code are deposited at osf.io/ec6wh (v36/). The CPC inputs originate in the v0.31 phase and are consumed as archived data via that phase's OSF deposit; the v0.31 SSRN abstract is withdrawn and is not cited as methodological authority. The regime target and Presence composite are read as frozen fields from the v0.23 deposit. Upstream phase and methodology papers are indexed in the cross-citation registry (see `_upstream_phases.md`).

# References {-}

González Castro, P. U. (2025). *Tri-System Brand Growth*. SSRN 6659000.

González Castro, P. U. (2026). *Construct Validity and the Four-Regime Taxonomy*. AIAS Protocol v1.2. SSRN 6761698.

González Castro, P. U. (2026). *Phase A Pivot-Validation Specification*. AIAS Protocol v1.3. SSRN 6797679.

González Castro, P. U. (2026). *Recognition × Recall Decomposition*. AIAS Protocol v1.4. SSRN 6799479.

González Castro, P. U. (2026). *Multi-Statistic C2 and Two-Channel Recall*. AIAS Protocol v1.5. SSRN 6810758.

González Castro, P. U. (2026). *Substrate Pre-Screening, Independent Moderator, Phantom Extension*. AIAS Protocol v1.6. SSRN 6816340.

González Castro, P. U. (2026). *CPC Consistency — Pre-Registered Negative Result (CV not independent of Presence)*. AIAS Protocol v1.7. SSRN 6878818.

González Castro, P. U. (2026). *Five-Substrate Foundational Construct Claim*. AIAS 1.0. SSRN 6817841.

González Castro, P. U. (2026). *AI Presence in Premium spirits: AIAS v0.23*. SSRN 6834298.

González Castro, P. U. (2026). *Consistency Component Instrument Pilot (CPC): AIAS v0.30*. SSRN 6875319.

González Castro, P. U. (2026). *Provider-Asymmetric Consistency in AI Brand Availability: AIAS v0.33*. SSRN 6909019.

González Castro, P. U. (2026). *Two-Wave Temporal Stability of an AI Brand-Recall Consistency Quantity: AIAS v0.34*. SSRN 6915458.

González Castro, P. U. (2026). *Control-Dependent Verdicts in a Phantom-Brand Consistency Contrast: AIAS v0.35*. SSRN 6921758.
