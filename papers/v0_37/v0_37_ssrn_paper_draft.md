---
title: "Identity Load Does Not Moderate Cross-Model Consistency"
subtitle: "A Pre-Registered Component-Dissociation Null (AIAS™ v0.37)"
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

{\LARGE \textbf{Identity Load Does Not Moderate Cross-Model Consistency}}\\[8pt]

{\large A Pre-Registered Component-Dissociation Null\\ (AIAS™ v0.37)}\\[28pt]

Pablo Ulpiano González Castro\\[4pt]
School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System™ (research entity; data archive and methodology venue)\\[8pt]
Correspondence: pablou@pablou.com · pablou.com\\
ORCID: 0009-0003-8968-9990\\[20pt]

Pre-registration: \texttt{v0.37-prereg-r2} (externally anchored before analysis; amends r1)\\
Data and code: OSF \texttt{ec6wh/v37}\\

\end{center}
\end{titlepage}

# Abstract {-}

Identity Load — the degree to which a brand surfaces through cultural rather than category-canonical retrieval channels — is a confirmed moderator of AI Presence: v1.6's H_IdentityLoad_Direct returned CONFIRMED on these substrates (v0.21 cosmetics Cell B IL-Direct δ = +7.12, 95% CI excluding 0; v0.22 automotive CONFIRMED; v0.20 skincare PARTIAL; v1.6, SSRN 6816340). This paper asks whether that same moderator governs a different component — cross-model Consistency, operationalized as the mean-independent dispersion instrument φ (higher φ = greater cross-model dispersion, i.e. lower consistency) — and finds that it does not. In a pre-registered, frozen re-analysis of the canonical two-channel trio (skincare, cosmetics, automotive; 72 brand units, 53 analyzable after the pre-specified true-zero/saturation partition), the pooled within-substrate rank association between continuous IL-Direct and φ is null: ρ = −0.008 (stratified permutation p = 0.955; n = 53, above the pre-registered power floor of 45). The association remains null under a presence-controlled partial (ρ = +0.004), placing the result in the verdict matrix's clean-null cell rather than its suppression cell. The test is powered, not silent: φ's mean-independence (|ρ(φ, recall-mean)| = 0.091) makes the raw association an inferential claim, and the surviving IL-Direct spread is real — the excluded units are the identity-load-neutral category staples. The orthogonality of an active Presence-side moderator to Consistency is positive evidence that the two components are governed by different mechanisms — the dissociation a two-component account of AI availability requires. The claim is deliberately bounded: a single moderator against a single consistency instrument is one dissociation result contributing to component-distinctness, not a proof of it.

**Keywords:** AI Availability; brand availability; AIAS; Ehrenberg-Bass; cross-model consistency; identity load; component dissociation; large language models; pre-registration; construct validity

**JEL codes:** M31; L86; L15; D83; M37

**Paper status:** Working paper. Phase v0.37 of the AIAS™ Measurement Program; pre-registered at tag `v0.37-prereg-r2` (amending r1) prior to analysis.

# 1. Introduction

The AIAS™ Measurement Program operationalizes AI availability as a multi-component brand-growth construct rather than a single quantity. Presence — whether and how strongly a brand is retrieved by a panel of large language models — is the program's anchored first component, validated across a multi-substrate base under Protocol v1.6 (SSRN 6816340). Consistency — whether that retrieval is stable across models rather than idiosyncratic to any one — is a candidate second component. Its standing as a distinct component, rather than a re-description of Presence, is the open question, and settling it requires dissociation evidence: a variable that moves one component while leaving the other unmoved.

Identity Load supplies a sharp test of that distinctness. IL-Direct — the per-brand recall asymmetry δ = R_cult − R_cat between cultural and category-canonical retrieval channels — is a confirmed moderator on the Presence side. Under Protocol v1.6's H_IdentityLoad_Direct (SSRN 6816340), cultural-channel-led brands surfaced markedly more through identity-laden frames: the hypothesis returned CONFIRMED on cosmetics (v0.21 Cell B δ = +7.12, 95% CI excluding 0; Cell A δ = −3.13 in the predicted negative direction) and automotive (v0.22), and PARTIAL on skincare (v0.20) — across the same trio later analyzed here. If Consistency were merely Presence under another name, IL-Direct should carry to it: a brand surfacing idiosyncratically by channel might plausibly surface idiosyncratically across model corpora — predicting a positive IL-Direct → φ association.

This phase tests that prediction directly, as a frozen re-analysis (no new acquisition) of the canonical two-channel trio — v0.20 skincare, v0.21 cosmetics, v0.22 automotive — the intersection where both φ and a continuous IL-Direct decomposition are construct-valid (v0.19 is single-channel and out of construct; v0.23 is a walled extension). The dependent variable is φ, the v1.8 mean-independent consistency instrument adopted after the earlier CV-based candidate CV-CPC was found not independent of Presence and not adopted at v1.7 (SSRN 6878818). φ's mean-independence (|ρ(φ, recall-mean)| = 0.091) is load-bearing: it makes an IL-Direct → φ association a genuine inferential claim rather than a recall-level artifact or a pipeline manipulation check. The single pre-registered inferential test, H_IL_Consistency, is a pooled within-substrate rank association under stratified permutation, routed against a presence-controlled partial; its verdict matrix was completed to exhaustiveness before scoring (tag `v0.37-prereg-r2`, a pre-acquisition amendment to r1) so that no reachable outcome — including presence-suppression — maps to a positive claim.

The result is a powered null. The prediction was directional — ρ(IL-Direct, φ) > 0 (higher identity load → lower cross-model consistency → higher φ); the observed ρ = −0.008 is null, not reversed, landing in the matrix's clean-null cell rather than the distinct CONFIRMED_REVERSED cell, and the presence-controlled partial (ρ = +0.004) is null on the same footing. Read against IL-Direct's confirmed Presence-side effect, this null is not a flat negative but a dissociation: affirmative evidence that cross-model Consistency is governed by structure other than identity load, and thus a component that earns separate standing. §2 specifies the locked design; §3 reports the verdict against the locked `v37_verdicts.json`; §4 develops the dissociation reading; §5 states the limits — single-moderator, single-instrument, and the common-functional caveat that cuts in both directions.

# 2. Method

## 2.1 Design and inputs

This phase is a frozen re-analysis: no new language-model acquisition is performed, and all per-brand quantities are read from inputs locked in prior phases (the v0.33 re-analysis pattern). The analysis scope is the canonical two-channel trio — v0.20 skincare, v0.21 cosmetics, v0.22 automotive — comprising 72 brand units (24 per substrate). This is the intersection of two construct constraints: φ-availability, defined across all five omnibus substrates, and a continuous IL-Direct decomposition, which exists only where the two-channel recall split was acquired (the trio). v0.19 is excluded as single-channel by acquisition (the IL-Direct decomposition is out of construct and not recomputable without re-acquisition); v0.23 is a walled, optional runtime-verify extension, not part of the trio. Three per-brand inputs enter: the dependent variable φ (the consistency instrument, §2.2); the moderator IL-Direct (§2.3); and, for the secondary robustness arm only, two controls — the Presence measure C_P (Protocol v1.6) and recall-mean. The model panel is six LLMs (M = 6) over six channel-agnostic frames each (F = 6). The single output of record is `osf/v37/v37_verdicts.json`.

## 2.2 Metric (the dependent variable φ)

φ is the v1.8 cross-model consistency instrument, computed per brand from the channel-agnostic per-model surfacing counts under the locked formula

$$\varphi_b = \frac{1}{M-1}\sum_m \frac{(k_m - F\hat\pi)^2}{F\hat\pi(1-\hat\pi)},$$

where $k_m \in \{0,\dots,F\}$ is model $m$'s surfacing count and $\hat\pi = \sum_m k_m / (MF)$. φ is inconsistency-oriented: higher φ means greater cross-model dispersion, i.e. lower consistency. A pre-specified Fork-A partition removes two boundary states from the analysis set as exclusions, with counts reported separately: $\hat\pi = 0$ (the true-zero floor) and $\hat\pi = 1$ (the saturation ceiling); φ is finite and defined on $0 < \hat\pi < 1$. The instrument's defining property is mean-independence: at the v1.8 results lock, $|\rho(\varphi,\text{recall-mean})| = 0.091$ (against the CV-based predecessor's 0.682), so the raw IL-Direct → φ association is a genuine inferential claim, not a recall-coupled manipulation check. The retired CV-based quantity CV-CPC (v1.7, not adopted) is retained only as a comparator (§2.6), never as the dependent variable; J, the frame-resolved consistency facet, is reported descriptively where frame-resolved and enters no verdict.

## 2.3 Moderator (IL-Direct)

The moderator is IL-Direct, the per-brand recall asymmetry between cultural and category-canonical channels, $\text{IL-Direct}(b) = R_{\text{cult}}(b) - R_{\text{cat}}(b)$, consumed as $R_{\text{cult\_total}} - R_{\text{cat\_total}}$ from `osf/methodology/v1_7/data/v1_7_cpc.csv`. Higher IL-Direct denotes more cultural-channel-led surfacing — higher Identity Load. The construct anchor is Protocol v1.6 (SSRN 6816340) Increment 2, H_IdentityLoad_Direct, $\delta = \overline{R}_{\text{cult}} - \overline{R}_{\text{cat}}$, which v1.6 evaluated at cell granularity; this phase uses the identical functional at brand granularity as a continuous covariate. The two-channel decomposition is frozen per brand only for the trio, which is precisely the scope where IL-Direct is construct-valid — the n = 72 restriction is the design's scope boundary, not an arbitrary truncation.

## 2.4 Reconciliation gate

A reconciliation gate runs after lock and before any contrast; failure halts the phase. Three clauses: (1) the consumed CV-CPC and C_P vectors reproduce the v0.33-deposited values bit-for-bit; (2) the v0.20/21/22 per-model count vectors reconcile to the v1.7 `r_per_model` column bit-for-bit, via the certified Stage-0 extraction path (φ is computed from that extraction, not recomputed from the CSV, so this remains a genuine check rather than a tautology); (3) — added at r1 — the IL-Direct source columns ($R_{\text{cat\_total}}$, $R_{\text{cult\_total}}$) reproduce the v1.7-deposited values, placing the moderator axis on the same footing as the DV-side inputs. Because the v1.7 deposit is itself the source CSV (no standalone reference-hash artifact), clause 3 is operationalized as a recorded SHA-256 baseline over the consumed IL columns: the first scoring run records the baseline; any subsequent run halts on mismatch.

## 2.5 Eligibility, attrition, and the power floor

A brand unit is eligible iff φ is defined (Fork-A excludes $\hat\pi \in \{0,1\}$) and IL-Direct is defined (guaranteed across the trio). The analysis set is enumerated and written before any contrast. Primary inference is pooled at brand level using within-substrate ranks; the per-substrate test is descriptive only (§2.6). A pre-registered Fork-A saturation diagnostic reports, regardless of outcome, the realized analyzable n per substrate and the IL-Direct distribution of excluded versus included units, so any truncation of the IL range is characterized empirically rather than assumed. A power floor of n = 45 is locked: if realized pooled analyzable n < 45 the primary is reported INDETERMINATE-UNDERPOWERED rather than forced (the v0.17 panel-inadequacy disposition). The floor is band-coherence-derived, not plucked: the CONFIRMED band requires |ρ| ≥ 0.30 and p < .05, but the critical two-sided Spearman ρ at p = .05 rises as n falls, crossing 0.30 near n ≈ 44; below ~44 the band's two conditions are mutually inconsistent — one cannot reach p < .05 at |ρ| = 0.30 — so the verdict structure is incoherent, and 45 pins the floor with a hair of margin. A per-substrate fragility flag (< 10 analyzable units) attaches as a note, not a gate.

## 2.6 Hypotheses and statistics

**H_IL_Consistency (PRIMARY, gating — the single inferential test).** Pooled within-substrate Spearman ρ(IL-Direct, φ), with inference by within-substrate stratified permutation (IL-Direct labels permuted within substrate only, ≥ 10,000 Monte Carlo draws, two-sided). Bands: |ρ| ≥ 0.30 and p < .05 → CONFIRMED, sign-split — ρ > 0 is the predicted direction (cultural-channel-led presence surfaces more idiosyncratically across corpora), ρ < 0 → CONFIRMED_REVERSED; |ρ| < 0.15 → FALSIFIED; otherwise MARGINAL.

**H_IL_Presence_Robustness (SECONDARY, not a gate).** Partial Spearman ρ(IL-Direct, φ | C_P, recall-mean), computed by inverting the four-variable Spearman rank-correlation matrix over {IL-Direct, φ, C_P, recall-mean} (the single locked computation), with the same within-substrate stratified permutation. Substantial attenuation (|ρ_partial| < 0.15 when the raw ρ ≥ 0.30) is reported as a presence-mediated scope qualification, not a falsification.

**H_IL_Cross_Substrate (SECONDARY, descriptive).** Per-substrate ρ sign consistency; N = 3 substrates carries no inferential claim.

**H_IL_t2_Stability (TERTIARY, exploratory, walled).** A descriptive test-retest of the IL-Direct → φ association where the v0.34 second wave intersects the trio; no confirmatory threshold; dropped silently if no intersecting wave exists.

**Supplementary contrast (non-gating).** The same pooled within-substrate Spearman is run on IL-Direct → CV-CPC as an instrument-sensitivity illustration, pre-registered as supplementary so the "only the instrument that worked is reported" objection cannot land; it touches no verdict.

**Robustness.** Leave-one-substrate-out (LOSO) recomputes ρ on the remaining two substrates; non-survival (a sign flip or a band-boundary crossing) downgrades the verdict one band (CONFIRMED → MARGINAL; a MARGINAL that fails LOSO is reported as fragile-MARGINAL) — a deliberate softening of the v0.32 hard-UNDETERMINED precedent, brittle at N = 3. Permutation determinism: the Monte Carlo seed is fixed in the scorer (not the pre-registration, which would over-constrain the lock with an arbitrary integer); every permutation p is reported with its Monte Carlo standard error, and any |ρ| whose p sits within ~2 MC-SE of .05 is flagged seed-sensitive.

## 2.7 Verdict matrix and the r2 pre-acquisition completion

The verdict matrix is exhaustive over the reachable outcome space — the cross of the primary ρ verdict with presence-robustness concordance — and no positive claim arises from a suppression-only or threshold-edge pattern. A CONFIRMED primary (predicted ρ > 0) routes to HEADLINE-POSITIVE when the partial is concordant (|ρ_partial| ≥ 0.15) and to PRESENCE-SCOPED-POSITIVE when it attenuates; CONFIRMED_REVERSED is reported in its own cell with the same concordance qualifier; MARGINAL is reported as weak-but-present. In the FALSIFIED row, a partial that is also null (|ρ_partial| < 0.15) → CLEAN-NULL; any non-null partial (CONFIRMED, |ρ_partial| ≥ 0.30 and p < .05; or the intermediate band) → UNDETERMINED-pending-suppression-diagnosis.

That FALSIFIED-row split is a pre-acquisition completion of the matrix, recorded transparently. The original lock (r1) defined the partial cut only in the raw-CONFIRMED branch (the attenuation case); in the FALSIFIED row the boundary between a suppression-bearing partial and a genuinely null one was unpinned. This was caught by inspection of the scorer against the locked matrix before any scoring call — the blinding boundary intact, no verdict computed — and fixed in the lock, not the code: tag `v0.37-prereg-r2` (DEVIATIONS Entry 2) pinned "partial CONFIRMED" symmetric to the primary band and mapped every FALSIFIED-row cell, erring conservatively toward UNDETERMINED so a suppression-shaped result can never read as a clean negative. It changes no band value and reverses no verdict; r1 remains frozen as the original design lock. No scoring-time deviations occurred: the first and only scoring call was made after this amendment.

# 3. Results

## 3.1 Analysis set and attrition — the saturation bit at the floor, not the ceiling

Of the 72 trio brand units, 53 are analyzable after the Fork-A partition (v0.20: 19 of 24; v0.21: 19 of 24; v0.22: 15 of 24); every substrate clears the 10-unit fragility threshold, and the pooled n = 53 is above the pre-registered power floor of 45, so the primary is a powered test, not an INDETERMINATE-UNDERPOWERED disposition. The 19 exclusions are informative against the pre-registration's own expectation. The lock anticipated that heavy recognition saturation in this trio would make the φ saturation-ceiling exclusion (π̂ = 1) bite; it did not. All 19 excluded units fall at the true-zero recall floor (π̂ = 0); none fall at the saturation ceiling (floor/ceiling counts — v0.20: 5/0, v0.21: 5/0, v0.22: 9/0). The mechanism is a recognition/recall split visible directly in the inputs: 16 of the 19 true-zeros sit at full recognition (C_P = 6/6) and 17 of 19 at or near the recognition ceiling (C_P ≥ 5), yet none surface in recall (π̂ = 0). The saturation the lock anticipated was real but lived on the recognition axis, not the recall axis φ is built from — brands the panel recognizes yet never surfaces in recall fall to the floor, not the ceiling. The attrition is therefore floor-driven, and it strengthens rather than threatens the null: the excluded true-zeros are identity-load-neutral (excluded-unit IL-Direct mean = 0.0 in all three substrates — the category-canonical staples), so the surviving analysis set retains genuine IL-Direct spread (included means 0.84, 2.11, 1.40), the spread across which the primary is tested. The recognition/recall split underlying this attrition is shown in Figure 1.

![The saturation bit at the recall floor, not the φ ceiling. Recognition (C_P, 0–6) against recall (π̂) for the 72 trio brands: the 19 Fork-A exclusions fall at the recall floor (π̂ = 0) and none at the saturation ceiling, and 16 of the 19 sit at full recognition (C_P = 6/6) — recognized by the panel, never recalled. Fork-A counts and IL-means are from the verdicts file; the C_P recognition axis is from osf/methodology/v1_7/data/v1_7_cpc.csv.](../../reports/figs/v37/chart_01_floor_not_ceiling.pdf){#fig:floor width=100%}

## 3.2 H_IL_Consistency (PRIMARY): FALSIFIED → CLEAN-NULL

The pre-registered prediction was directional: ρ(IL-Direct, φ) > 0. The observed pooled within-substrate Spearman association is ρ = −0.008 (within-substrate stratified permutation p = 0.955; Monte Carlo SE = 0.002; n = 53). With |ρ| = 0.008 < 0.15, the primary is FALSIFIED. The observed value is null, not reversed: ρ ≈ 0 lands in the FALSIFIED → clean-null region, categorically distinct from the CONFIRMED_REVERSED cell, which requires ρ < 0 and |ρ| ≥ 0.30 at p < .05. This is a precise null rather than an absence of power: at n = 53 the critical two-sided |ρ| at p = .05 is ≈ 0.27, below the 0.30 CONFIRMED threshold, so a true association at or above the pre-registered threshold would have cleared both significance and the band — the design could have rejected the null had a threshold-level effect existed, and did not. The permutation p sits far from the .05 boundary, so the verdict is not seed-sensitive. Identity load, as the continuous IL-Direct moderator, has no detectable association with cross-model φ-consistency. Figure 2 places the estimate against the detectable-effect threshold.

![A precise null, not an absence of power. The primary association ρ(IL-Direct, φ) = −0.008 against the detectable-effect threshold at n = 53: the critical |ρ| at p = .05 (≈ 0.27) lies below the 0.30 CONFIRMED band, so a band-level effect was reachable, and the estimate sits at ~0 with a 95% CI that excludes the band.](../../reports/figs/v37/chart_02_precise_null.pdf){#fig:null width=100%}

## 3.3 H_IL_Presence_Robustness and the verdict-matrix cell

The presence-controlled partial — Spearman ρ(IL-Direct, φ | C_P, recall-mean), via the locked four-variable rank-correlation-matrix inversion — is ρ_partial = +0.004 (permutation p = 0.980; Monte Carlo SE = 0.001; n = 53), in the partial-NULL band (|ρ_partial| < 0.15). The null survives control for Presence and recall level alike; the association is not a presence-suppressed signal. Crossed in the verdict matrix, FALSIFIED primary × partial-NULL routes to CLEAN-NULL — the single clean-negative cell, explicitly not the suppression cell, which the partial would have to be non-null to reach. Figure 3 sets the confirmed Presence-side effect against this null as the component dissociation.

![Identity load moves Presence, not Consistency, across the same trio. Left: IL-Direct is a confirmed Presence-side moderator (v1.6 H_IdentityLoad_Direct, cell-level, δ = +7.12, 95% CI excluding 0). Right: the same moderator is null for cross-model φ-Consistency (v0.37, brand-level, raw ρ = −0.008, presence-controlled ρ = +0.004). The panels are different phases at different granularities — a cross-phase contrast, not one analysis.](../../reports/figs/v37/chart_03_dissociation.pdf){#fig:dissoc width=100%}

## 3.4 H_IL_Cross_Substrate (SECONDARY, descriptive)

The per-substrate associations carry no inferential claim (N = 3) and are reported for completeness: v0.20 ρ = +0.137 (n = 19), v0.21 ρ = −0.172 (n = 19), v0.22 ρ = −0.125 (n = 15). The signs disagree across substrates, consistent with sampling noise around a null rather than a suppressed common effect.

## 3.5 Supplementary contrast, tertiary stability, and descriptive J

The pre-registered non-gating supplementary contrast on the retired instrument — IL-Direct → CV-CPC — is also essentially null (ρ = +0.129, n = 38; CV-CPC's recall-mean definedness floor of mean count ≥ 1 excludes more low-recall units than φ's Fork-A partition keeps, itself a quiet restatement of the v1.7→v1.8 point that the retired instrument is the more recall-coupled one). The result therefore does not depend on having chosen the instrument that "worked": neither instrument shows an effect. The walled tertiary test-retest, where the v0.34 second wave intersects the trio, reports a descriptive φ rank-agreement of 0.637 (n = 52 pairs), carried with no confirmatory weight. The descriptive J facet resolved for all three trio substrates and the walled v0.23 extension; it enters no verdict.

## 3.6 Sensitivity

Leave-one-substrate-out recomputes the primary ρ at −0.112 (drop v0.20), +0.087 (drop v0.21), and −0.018 (drop v0.22) — a sign flip across subsets, which the pre-registration flags as LOSO non-survival. At a confirmed effect this would trigger a one-band downgrade; here it is uninformative-at-null: the verdict is already FALSIFIED (the floor band, not downgradable), and a sign that flips around zero across two-substrate subsets is noise, not a buried signal masked by pooling. Both the primary and partial permutation p-values lie far from .05, so no result is seed-sensitive, and threshold reruns are immaterial at |ρ| ≈ 0.

# 4. Discussion

## 4.1 The dissociation is the contribution

The result of record is a null, but the contribution is a dissociation — and the honest statement of it owns that both legs are phase-level empirical findings, not one fact and one finding. On the Presence side, identity load is a confirmed moderator: v1.6's H_IdentityLoad_Direct returned CONFIRMED on v0.21 cosmetics (Cell B δ = +7.12, CI excluding 0) and v0.22 automotive, and PARTIAL on v0.20 skincare (SSRN 6816340) — at cell granularity, across the same trio the present null is computed over. On the Consistency side, the same moderator, taken to brand granularity across the trio, is orthogonal to φ — ρ = −0.008 raw, +0.004 presence-controlled, a powered null. The dissociation is therefore a contrast across two phase-level results: a confirmed-to-partial Presence-side effect set against a powered Consistency null, spanning two granularities (cell, then brand) on the same trio substrates — which sharpens rather than dilutes the contrast: identity load moves Presence but not φ-Consistency across the same substrates. That contrast is real and reportable — two functionals of brand retrieval that both responded to identity load would be hard to defend as distinct components, and one that responds while the other does not is the dissociation a two-component account requires — but neither leg is an unshakable premise. Just as the Consistency null is bounded to one instrument (§4.3), the Presence-side effect anchoring the contrast is itself one confirmed finding with its own scope. Within those bounds the null carries a positive claim: φ-consistency is governed by structure other than identity-load asymmetry, the evidence that lets Consistency stand as a candidate component in its own right rather than a re-description of Presence — one leg of the distinctness argument the AIAS 2.0 program is built to assemble.

## 4.2 A nested dissociation: recognition versus recall

The attrition pattern (§3.1) is a second, smaller dissociation, worth a glance rather than a claim. The pre-registration expected recognition saturation to express as a φ saturation-ceiling exclusion; instead the saturation lived entirely on the recognition axis (16 of 19 excluded units recognized at C_P = 6/6) while recall floored to zero (π̂ = 0). Recognition and recall come apart at exactly these units: brands the full panel recognizes yet never surfaces in recall. That recognition/recall gap is a standing program theme, traceable across prior records rather than asserted: v1.7 documented it as a secondary finding — consistency left undefined for recognized-but-unrecalled brands, concentrated among prestige labels (SSRN 6878818) — and v0.34 surfaced it as recognition-ceiling collapse, where recognition saturation in four of five categories rendered Presence-residualization a no-op. It is one of the two requirements the v1.8 revision was mandated to address — the graded recognition signal — and is distinct from the requirement that drove φ itself: the mean-independence fix for CV-CPC's recall-coupling (the √mean identity, |ρ(φ, recall-mean)| 0.682 → 0.091). Here the gap surfaces as the structural reason the φ partition bit at the floor, reinforcing the lesson the main result rests on: recognition-anchored and recall-anchored measures are not interchangeable, which is why φ rather than a recognition-coupled quantity is the instrument under test.

## 4.3 The bounded claim

One dissociation result is not proof of component-distinctness, and the claim is deliberately bounded on two axes. It is a single moderator (IL-Direct) against a single consistency instrument (φ): "identity load moderates Presence but not Consistency" is supported for this operationalization of identity load against this instrument, and stands as evidence toward distinctness, not a settled case for it. A fuller dissociation argument wants additional moderators — Phantom Brand Persistence is the literal next phase (v0.38) and a natural sequel rather than a redundancy, since it probes a different Presence-side structure against the same Consistency instrument — and, eventually, other candidate components (for instance ranking or sentiment stability). This phase contributes one well-powered dissociation to that argument and marks the scope within which it holds.

## 4.4 The common-functional caveat, in both directions

IL-Direct (δ = R_cult − R_cat) and φ are different functionals of the same probe matrix, and the pre-registration carried this as a stated limitation for a confirmed link — a shared diffuse-identity cause could in principle drive both. For the null, the same fact cuts in two directions, and the honest position states both. It strengthens the null: because both quantities derive from the same recall data with no separating measurement channel, a genuine identity-load-to-consistency relationship would have been detectable here if it existed — there is no hidden-channel artifact in which a real effect could be hiding, so the orthogonality is a real absence rather than a measurement gap. And it bounds the null: the absence is specific to consistency operationalized as φ-dispersion, not to consistency in general. A differently constructed consistency measure — rank-order stability, the J facet, or a future instrument — could relate to identity load where φ does not. The defensible conclusion is therefore precise: cross-model φ-consistency is orthogonal to identity load, mean- and presence-independently, within the scope this instrument defines.

# 5. Limitations

The bounds below are stated once; each is developed where cited and not re-argued here.

**1. Single moderator, single instrument.** The dissociation rests on one moderator (IL-Direct) against one consistency instrument (φ); it is evidence toward component-distinctness, not a settled case (§4.3). Generalization requires additional moderators — Phantom Brand Persistence at v0.38 — and, eventually, other candidate components.

**2. A cross-phase, cross-granularity contrast.** The Presence-side leg of the dissociation is v1.6's H_IdentityLoad_Direct — confirmed on v0.21/v0.22 and partial on v0.20, at cell granularity — while the Consistency-side null is at brand granularity; the legs differ in granularity (cell vs brand) on the same trio substrates (§4.1). The contrast holds between two phase-level findings, each with its own scope, not between a fixed premise and a single result.

**3. φ-specificity.** The null is specific to consistency operationalized as φ-dispersion; a differently constructed measure — rank-order stability, the J facet, a future instrument — could relate to identity load where φ does not (§4.4). The result does not speak to consistency in general.

**4. Shared-functional derivation.** IL-Direct and φ are different functionals of the same probe matrix (§4.4). This strengthens the null — no separating channel in which a real effect could hide — but the conclusion is scoped accordingly: the test speaks to identity load and φ as derived from one recall matrix, not to constructs measured on independent channels.

**5. Floor attrition.** Nineteen of 72 units were excluded at the true-zero recall floor (§3.1). Because those units are identity-load-neutral category staples (IL-Direct ≈ 0), their exclusion does not truncate the tested IL-Direct spread; but the null is not evidence about brands the panel recognizes yet never recalls. These are also the units where φ-consistency is undefined by construction (π̂ = 0), so any identity-load-to-consistency relationship in that population lies outside the reach of any φ-based test, not only this one's — the floor attrition and the φ-specificity of limitation 3 are the same boundary viewed from two sides, and a recognition-anchored rather than recall-anchored consistency measure would be required to probe it.

**6. Coarse robustness at three substrates.** Leave-one-substrate-out resampling operates on N = 3, a weak robustness instrument; the observed LOSO sign-instability is uninformative-at-null (§3.6), but LOSO at this N could not adjudicate genuine substrate heterogeneity were any present.

**7. Frozen single-wave re-analysis.** The study re-analyzes frozen t₁ inputs with no new acquisition (§2.1); the t₂ test-retest is walled and descriptive. Results are conditional on the frozen inputs and the fixed six-model panel — and because φ is a cross-model dispersion measure, the dispersion is measured across this specific six-model panel, so the null is scoped to cross-model consistency as these models instantiate it: a different or larger panel could in principle show identity-load structure in cross-model dispersion that these six do not surface.

# 6. Future Research

Three specific resolutions follow, each named by what it would settle.

The immediate successor is v0.38, the Phantom Brand Persistence × φ phase, which does double duty. As the next leg of the dissociation argument (§4.3) it tests a second, structurally different Presence-side moderator against the same consistency instrument: a second null would strengthen the component-distinctness case, while a confirmed association would bound the present result to identity load specifically. It is also the re-test v0.35 designated and could not perform. There, the phantom-signature question — whether phantom-flagged brands carry a distinct cross-model consistency signature — was shown undecidable with CV-CPC: the gate flipped between a recognition-anchored and a recall-mean control, returned UNDETERMINED, and v0.35 explicitly deferred the question to the v1.8 instrument (SSRN 6921758). v0.37 deploys exactly that instrument; v0.38 applies it to the phantom population, with v0.35's frozen analysis set as the comparison baseline. The concrete resolution it offers: whether the phantom signature CV-CPC could not adjudicate exists under a mean-independent measure.

The recognized-but-unrecalled population is the boundary shared by limitations 3 and 5: φ is undefined there by construction (π̂ = 0, recall floored), so any identity-load-to-consistency structure in that population lies outside any recall-anchored test. Probing it requires a consistency measure operating on the recognition channel rather than recall — for which the graded recognition signal mandated for v1.8 is the natural input. This is a distinct measurement question, not a larger sample of the present one, and it is the natural home for the prestige staples (recognized but unrecalled) that the recall floor sets aside here.

Finally, the distinctness argument generalizes only by accumulation. Each additional moderator and each additional candidate component — ranking stability, sentiment stability — contributes one dissociation test, and the case for Consistency as a separate AIAS component is the convergence of those tests, not any single one. The present study is one such test, and its weight in that argument is bounded accordingly (§4.3).

# Declarations {-}

## Conflict of interest {-}

The author is employed full-time as Director, Corporate Brand Creative and Governance, at Samsung Electronics America; the AIAS™ Presence Measurement Protocol and the work reported here are the author's independent academic research, conducted outside the scope of employment, and Samsung had no role in the design, analysis, or reporting of this study. v0.37 is a frozen re-analysis of the v0.20 / v0.21 / v0.22 registries and inherits their locked pre-acquisition conflict-of-interest screens (pre-registration DEVIATIONS Entry 0), summarized here per substrate.

For v0.20 skincare, none of the 24 registry brands is affiliated with Samsung Electronics America; Samsung's historical beauty exposure was via Cheil Industries, spun off prior to 2026 in corporate restructuring, with no current overlap with the v0.20 registry. For v0.21 cosmetics, none of the 24 registry brands is affiliated with Samsung Electronics America. For v0.22 automotive, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands: Harman International (audio systems) supplies Mercedes-Benz, BMW, and other premium automotive OEMs; Samsung SDI (battery cells) supplies BMW (i-series), Volkswagen Group marques including Bentley and Porsche, and others; Samsung Display (infotainment) supplies Mercedes-Benz and BMW; Tesla and Polestar carry tangential component exposure at the parts level.^[The v0.22 Declarations §COI — verbatim-conformed into this phase's pre-registration (DEVIATIONS Entry 0) under the discipline of not editing a published locked record — attributed Bentley and Porsche to "Stellantis-adjacent platforms." Both are Volkswagen Group marques; the attribution is corrected here, as this paper's Declarations constitute a new published statement rather than a reproduction of the locked v0.22 record.] These are non-competitive supply relationships; Samsung Electronics America does not produce or market passenger-car brands and has no brand-level competitive overlap with any registry entry, and no operational restriction on registry composition was imposed. As program-lineage provenance only — the substrate is not in the v0.37 analysis set — the v0.19 audiophile-headphones registry substituted AKG with Denon before its pre-registration lock (AKG having been owned by Harman International, a Samsung subsidiary, since 2016) to avoid any appearance of conflict; the substitution was AKG only, not JBL.

The author's primary academic affiliation for this research is the School of Visual Arts MPS Branding Program; the research entity maintaining the data archive and methodology venue is Third System™.

## Funding {-}

Self-funded.

## Ethics {-}

Not applicable; no human subjects; public APIs and LLM prompts only.

## Data and code availability {-}

All pre-registration artifacts, input-reconciliation logs, the analysis-set CSV, scoring code, the verdicts file, and figures are deposited at osf.io/ec6wh (v37/). The pre-registration is locked at git tag `v0.37-prereg-r2` (amending r1), externally anchored prior to analysis. Upstream phase and methodology papers are listed in the references below.

# References {-}

*Citation titles are sourced from each cited paper's own submission draft; live SSRN verification was unavailable (the abstract pages returned HTTP 403). SSRN abstract IDs are given where recorded in the paper's OSF deposit record, and otherwise marked [SSRN ID pending] for verification at submission. Entries marked [pending] could not be sourced from an in-repository primary artifact and must be completed before submission.*

## Methodology {-}

González Castro, P. U. (2026). *[A methodology-chain paper (labeled v1.2 per the program registry, version-attribution unverified) — title and SSRN ID pending verification; no draft in repository].*

González Castro, P. U. (2026). *[A methodology-chain paper (labeled v1.3 per the program registry, version-attribution unverified) — title and SSRN ID pending verification; draft lacks a title field].*

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol v1.4: Recognition × Recall Decomposition and Multi-Component AI Availability.* AIAS™ Protocol v1.4. SSRN Working Paper [SSRN ID pending].

González Castro, P. U. (2026). *The AIAS™ Presence Measurement Protocol: Multi-Statistic C2 Specification and Two-Channel Recall Decomposition.* AIAS™ Protocol v1.5. SSRN Working Paper [SSRN ID pending]. (Title from a build-intermediate, not the submission draft; confirm against the source draft at submission.)

González Castro, P. U. (2026). *Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension.* AIAS™ Protocol v1.6. SSRN Working Paper [SSRN ID pending].

González Castro, P. U. (2026). *Consistency without Independence.* AIAS™ Protocol v1.7. SSRN Working Paper [SSRN ID pending].

González Castro, P. U. (in preparation). *The mean-independent consistency instrument (φ).* AIAS™ Protocol v1.8.

González Castro, P. U. *[Foundational AIAS™ paper (AI Availability) — title and SSRN ID pending verification; no draft in repository].*

## Phase papers {-}

González Castro, P. U. (2026). *Recognition Ceiling, Dissociation Replication, and Cultural-Channel Asymmetry on an Audiophile Headphones Substrate* (AIAS™ v0.19). SSRN Working Paper 6809182. https://ssrn.com/abstract=6809182

González Castro, P. U. (2026). *Type 2 Emergence and First Prospective v1.5 C2 Calibration on a Skincare IL-Gradient Substrate* (AIAS™ v0.20). SSRN Working Paper [SSRN ID pending].

González Castro, P. U. (2026). *Type 2 Confirmation, Recognition Ceiling, and Phantom Brand Persistence on a Cosmetics IL-Gradient Substrate* (AIAS™ v0.21). SSRN Working Paper [SSRN ID pending].

González Castro, P. U. (2026). *Phantom Brand Persistence on a Heritage-Saturated Automotive Substrate — Cell D_Defunct as Pure-Phantom Upper-Bound Test* (AIAS™ v0.22). SSRN Working Paper [SSRN ID pending].

González Castro, P. U. (2026). *[AIAS™ v0.23 premium spirits — title and SSRN ID pending verification; draft title field stale (carries the v0.22 title)].*

González Castro, P. U. (2026). *Recognition Saturates, Consistency Doesn't* (AIAS™ v0.30). SSRN Working Paper 6875319. https://ssrn.com/abstract=6875319

González Castro, P. U. (2026). *Consistency Across Categories: A Cross-Category Baseline for the AIAS™ Consistency Component (CPC)* (AIAS™ v0.31). SSRN Working Paper [SSRN ID pending].

González Castro, P. U. (2026). *Version-Snapshot Stability of an AI-Presence Consistency Score* (AIAS™ v0.32). SSRN Working Paper [SSRN ID pending].

González Castro, P. U. (2026). *Provider-Asymmetric Consistency in AI Brand Availability* (AIAS™ v0.33). SSRN Working Paper 6909019. https://ssrn.com/abstract=6909019

González Castro, P. U. (2026). *Two-Wave Temporal Stability of an AI Brand-Recall Consistency Quantity* (AIAS™ v0.34). SSRN Working Paper [SSRN ID pending].

González Castro, P. U. (2026). *Control-Dependent Verdicts in a Phantom-Brand Consistency Contrast* (AIAS™ v0.35). SSRN Working Paper 6921758. https://ssrn.com/abstract=6921758

## Synthesis {-}

González Castro, P. U. (2026). *AI Availability as a Third Measurable Layer of Brand Availability* (AIAS™ 1.0). SSRN Working Paper [SSRN ID pending].
