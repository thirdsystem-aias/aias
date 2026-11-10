---
title: "Presence and Consistency: A Two-Component Measurement of AI Availability"
subtitle: "The AIAS™ 2.0 Synthesis: Five Product Categories, Three Waves, Two Scores Reported Side by Side"
date: "November 2026"
mainfont: "Carlito"
fontsize: 11pt
geometry: [letterpaper, margin=1in]
header-includes: |
  \usepackage{setspace}
  \usepackage{float}
  \usepackage{caption}
  \usepackage{titlesec}
  \usepackage{needspace}
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

{\LARGE \textbf{Presence and Consistency: A Two-Component\\ Measurement of AI Availability}}\\[8pt]

{\large The AIAS™ 2.0 Synthesis: Five Product Categories, Three Waves,\\ Two Scores Reported Side by Side}\\[28pt]

Pablo Ulpiano González Castro\\[4pt]
School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System™ (research entity; data archive and methodology venue)\\[8pt]
Correspondence: pablou@pablou.com · pablou.com\\
ORCID: \href{https://orcid.org/0009-0003-8968-9990}{0009-0003-8968-9990}\\[20pt]

Outline lock: \texttt{aias-2-0-outline-locked} (deposited on OSF before any third-wave score existed)\\
Data lock: \texttt{aias-2-0-data-locked} · Figures: \texttt{aias-2-0-charts-locked}\\
Materials: OSF \texttt{ec6wh/aias\_2\_0}\\

\end{center}
\end{titlepage}

# Abstract {-}

AIAS 1.0 established Presence, how often a fixed panel of large language models names a brand, as a measurable component of AI Availability. This synthesis adds a second component, Consistency: how evenly the panel's models name the same brand across the same questions. The Consistency arc of the measurement program first used a coefficient-of-variation statistic, which a pre-registered test showed to be coupled to Presence (pooled ρ = 0.766), and replaced it with a mean-independent dispersion statistic, φ (pooled |ρ(φ, μ)| = 0.091). A methodology lock (v1.9) then scaled φ to 0–100, rated it only for brands named at least six times across the panel, and found that no candidate composite of the two scores both carries information Presence does not and keeps Consistency separate from Presence. The synthesis therefore reports the two scores side by side. Its outline, including the wording of its headline for every possible outcome, was deposited before a third measurement wave was scored. On five product categories (112 brands, six models), Consistency stayed separable from Presence in each wave (|ρ| = 0.073 and 0.082 in the two calibration waves, 0.189 in the confirmatory wave) and kept its brand order over 152 days beyond what the question structure alone produces (ρ = 0.647, n = 52, frame-structure p = 0.008). Presence kept its order as well (ρ = 0.954, n = 112). About half the brands are named too rarely to be rated for Consistency. The results bind to one retiring six-model panel; behavioural validity is not tested.

**Keywords:** AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; large language models; consistency; inter-model agreement; test--retest reliability; measurement synthesis

**JEL codes:** M31; L86, L15, D83, M37

**Paper status:** Synthesis of locked records (no new acquisition). Outline locked and deposited on OSF before the third-wave verdicts existed; every statistic reported is taken from a locked verdict or calibration file or the data lock's declared summaries, and the outline's pre-specified wording rule (§3.5) sets the headline. One procedural deviation in the outline's anchoring is recorded (§3.5). Part of the AIAS measurement program.

# 1. Introduction

When a person asks an AI assistant which running shoe, olive oil or savings app to choose, the brands named in the answer form a consideration set that the person did not build. The AIAS measurement program studies that set as a third layer of brand availability (González Castro, 2026, SSRN 6659000), beside the Mental and Physical Availability of the Ehrenberg-Bass tradition (Sharp, 2010; Romaniuk & Sharp, 2022), under the Tri-System framework (González Castro, 2026, MSI Working Paper 26-132). AIAS 1.0 (SSRN 6817841) operationalized the first component, Presence: the rate at which a fixed panel of models recognizes and recalls a brand in category-anchored prompts. A later baseline showed that Presence behaves as a construct should, converging with search interest and diverging from sales rank (v0.29, SSRN 6870778).

Presence is a rate pooled across models, and a pooled rate hides how it is reached. A brand named in every answer by three models and in none by the other three has the same Presence as a brand named in half the answers by all six. For a manager the two situations differ: the first brand's availability depends on which assistant a buyer happens to use; the second brand's does not. The program calls the second property Consistency, and built it as the second AIAS component between June and November 2026.

That construction did not go in a straight line. The first instrument, a coefficient-of-variation statistic over per-model recall (CV-CPC), produced a sequence of studies (v0.30–v0.36) before a pre-registered test showed that it moves with recall itself and so cannot stand as a separate component (v1.7, SSRN 6878818). A redesigned, mean-independent statistic, φ, replaced it (v1.8, SSRN 6963359). A null result then showed that the moderator that shapes Presence does not shape Consistency (v0.37). A methodology lock decided how the two components are reported (v1.9), and a third measurement wave, collected five months after the second, tested whether both components hold their brand order over time (v0.41).

This paper is the synthesis of that arc. It states what AIAS 2.0 measures, binds each claim to the locked verdict that governs it, and reports where the evidence stops. Its outline, including how the headline would be worded under each possible third-wave outcome, was committed before the first third-wave call and deposited on OSF before any third-wave score existed (§3.5). Section 2 positions Consistency as a measurement property. Section 3 sets out the corpus, the two scores and the locked tests. Section 4 presents the evidence, Section 5 the AIAS 2.0 construct as eight claims, Section 6 the implications and limits, and Section 7 the next steps.

# 2. Theoretical positioning

Mental Availability describes how readily a brand comes to mind in buying situations; Physical Availability, how easily it can be found and bought (Sharp, 2010; Romaniuk & Sharp, 2022). The Tri-System framework adds a layer between the buyer and both: an AI intermediary that retrieves, ranks and recommends brands before the buyer sees them (González Castro, 2026, MSI Working Paper 26-132). AI Availability is that layer's measure. The program defines it through six components, built one at a time, each locked before it is used and each reported only once measured (Figure 1).

![AI Availability as six components, in roadmap order. Presence (AIAS 1.0) and Consistency (AIAS 2.0) are measured; Ranking, Sentiment, Coverage and Grounding are planned.](../../reports/figs/aias_2_0/chart_01_component_roadmap.pdf){#fig:roadmap width=100%}

Consistency is a measurement property with a long history outside marketing. When several raters classify the same objects, their agreement is a quantity in its own right, distinct from how often any category is used (Fleiss, 1971). The panel of models plays the raters' role: each model answers the same frames about the same brands, and the question is how far their answers agree. Two statistical facts shape how that agreement can be measured. First, for counts bounded by the number of frames, dispersion across raters depends mechanically on the mean unless the statistic removes that dependence; the quasi-binomial dispersion parameter does so by scaling the observed between-model variance by the variance a binomial with the same mean would show (McCullagh & Nelder, 1989). Second, a property worth reporting about a brand must keep its order when the measurement is repeated, which is the test–retest logic of reliability (Shrout & Fleiss, 1979).

A second component is only worth reporting if it is not the first one in disguise. The program's discriminant logic follows Campbell and Fiske (1959): a candidate component must correlate weakly with the established one, and the weakness must hold across occasions. Presence's own baseline (v0.29) used the same logic against external measures. For Consistency it applies internally, against Presence.

The synthesis claims measurability with falsifiable verdicts under pre-registration (Nosek, Ebersole, DeHaven & Mellor, 2018), not validity against behaviour. Whether brands that are named more consistently are chosen more often is a later test (§7).

# 3. Corpus, scores and locked tests

## 3.1 Corpus and panel

The synthesis uses the only corpus on which both components were measured on the same brands, panel and occasions: the five panel-uniform substrates of the program's omnibus, audiophile headphones (v0.19, 16 brands), skincare (v0.20), cosmetics (v0.21), automotive (v0.22) and premium spirits (v0.23), with 24 brands each, 112 brand units in all. Each was measured three times with the same six-model panel (Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o mini, Gemini 2.5 Flash and Gemini 2.5 Flash Lite; temperature 0; 2,048-token cap) and byte-identical probe text: at $t_1$ (the original acquisitions, May 20–26, 2026), at $t_2$ (the v0.34 re-acquisition, June 10, 2026, 15–21 days later) and at $t_3$ (the v0.41 re-acquisition, November 9, 2026, 152 days after $t_2$). Each wave comprises 852 calls: 672 recognition probes and 180 recall queries. The third wave returned all 852 responses; a computer restart interrupted the collection, which was resumed the same day and logged (v0.41 DEVIATIONS Entry 2). All eight probe artifacts reproduced their $t_1$ checksums before each runner ran, and the four models with dated identifiers served the same snapshots as at $t_2$; the two Gemini models carry no dated identifier, so their constancy between waves cannot be verified. The fourth check, truncation, is descriptive and not clean: at $t_3$ the share of calls ending on the token cap was 35.4% for Gemini 2.5 Flash (58 of 164 logged calls), 11.0% for Claude Opus 4.5, 6.1% for Gemini 2.5 Flash Lite, 0.5% for Claude Sonnet 4.5 and zero for both GPT-4o models; $t_1$ and $t_2$ recorded no finish reasons, so the waves cannot be compared on this point (v0.41 manipulation checks).

For each brand $b$ and model $m$, recall is the count $k_{bm} \in \{0, \ldots, 6\}$ of the six recall frames (three category frames, three cultural frames) in which the model names the brand, pooled across channels; recognition is binary per model.

## 3.2 Presence

Presence is taken as locked from the AIAS 1.0 lineage (protocol v1.6; the v0.25 Presence composite), not recalibrated here:

$$P_b = 100 \cdot \tfrac{1}{3}\left(\frac{C_{P,b}}{6} + 2\,\hat\pi_b\right), \qquad \hat\pi_b = \frac{1}{36}\sum_m k_{bm},$$

where $C_{P,b}$ is the number of models that recognize the brand. $P$ runs from 0 to 100 and is defined for every brand.

## 3.3 Consistency

Consistency is measured by the v1.8 statistic φ, the quasi-binomial dispersion of the per-model recall counts around the pooled rate:

$$\varphi_b = \frac{1}{M-1}\sum_{m=1}^{M} \frac{\left(k_{bm} - F\hat\pi_b\right)^2}{F\hat\pi_b\left(1-\hat\pi_b\right)}, \qquad M = F = 6.$$

Higher φ means less agreement among the models. φ is undefined for a brand no model names ($\hat\pi_b = 0$) and shows no dispersion for a brand every model names in every frame ($\hat\pi_b = 1$). The v1.9 lock scales it to an absolute 0–100 score,

$$C_{\varphi,b} = 100\left(1 - \frac{\varphi_b}{\varphi_{\max}}\right), \qquad \varphi_{\max} = \frac{FM}{M-1} = 7.2,$$

where 100 means identical counts across models and 0 means maximal polarization (each model names the brand in all frames or in none). The reported Consistency score, $C^*$, is $C_\varphi$ rated only for brands with at least six mentions across the panel ($\sum_m k_{bm} \ge 6$, one model's full frame set); below that floor the brand carries Presence only. Section 4.3 gives the reason.

## 3.4 Locked tests

The synthesis adds no test. Its claims rest on verdicts locked in v0.41 and v1.9 (Table 1), each scored once under rules fixed before the third wave existed.

| Record | Hypothesis | Statistic | Confirmed if | Falsified if |
|----------|----------------------|----------------|------------|------------|
| v1.9 Stage 2 | H_\allowbreak{}Presence_\allowbreak{}Score_\allowbreak{}Reliability | $\rho(P_{t_2}, P_{t_3})$, within-category ranks | $\rho \ge 0.80$ and $p_{\text{perm}} < .05$ | $\rho < 0.60$ or $p_{\text{perm}} \ge .05$ |
| v1.9 Stage 2 | H_\allowbreak{}Dissociation_\allowbreak{}t3 | $\lvert\rho(C^*_{t_3}, P_{t_3})\rvert$, within-category ranks | $\le 0.30$ | $\ge 0.50$ |
| v1.9 Stage 2 | H_\allowbreak{}Consistency_\allowbreak{}Reliability | $\rho(C^*_{t_2}, C^*_{t_3})$ vs frame-structure null | $\rho \ge 0.50$ and $p_{\text{frame}} < .05$ | $\rho < 0.30$ or $p_{\text{frame}} \ge .05$ |
| v0.41 | H_\allowbreak{}Phi_\allowbreak{}LongHorizon | $\rho(\varphi_{t_2}, \varphi_{t_3})$, pooled | $\rho \ge 0.50$, $p_{\text{perm}} < .05$, $p_{\text{frame}} < .05$ | $\rho < 0.30$ or $p_{\text{perm}} \ge .05$ |
| v0.41 | H_\allowbreak{}Presence_\allowbreak{}LongHorizon | $\rho(\hat\pi_{t_2}, \hat\pi_{t_3})$ per category | $\rho \ge 0.70$ in at least 4 of 5 | $\rho < 0.50$ in at least 3 of 5 |
| v0.41 | H_\allowbreak{}Horizon_\allowbreak{}Decay | $\rho(t_1,t_2) - \rho(t_1,t_3)$, bootstrap CI | CI above 0 | CI below 0 |
| v0.41 | H_\allowbreak{}Drift_\allowbreak{}Dissociation | $\rho(\Delta\varphi, \Delta\hat\pi)$ | $\lvert\rho\rvert \le 0.30$ | $\lvert\rho\rvert \ge 0.50$ with $p < .05$ |

: Locked tests consumed by the synthesis. Intermediate values are MARGINAL. Permutation nulls and the frame-structure null (within-frame model shuffles that preserve each brand's pooled rate) use 10,000 draws.

## 3.5 Pre-registration chain and the outline's wording rule

The v0.41 and v1.9 pre-registrations were tagged on November 9, 2026, at 06:24 UTC and deposited on OSF within the minute. Because GitHub write access was unavailable that morning, their git hashes were also anchored on OSF (13:31–13:32 UTC) before the first third-wave call (13:32 UTC), and the tags were pushed later that day; they resolve to the anchored hashes (v0.41 and v1.9 DEVIATIONS Entry 1).

This synthesis's outline was committed at 13:27 UTC, before the first third-wave call, and deposited on OSF at 15:11–15:12 UTC, after collection had started but before it was complete (15:36 UTC) and before anything was scored (both scorers were tagged at 16:16 UTC). Its deviation from the planned sequence, an OSF anchor in place of a tag push, is recorded as its DEVIATIONS Entry 1. The outline fixed eight claims, the verdict that governs each, and the headline wording for every combination of the two governing verdicts, H_Dissociation_t3 and H_Consistency_Reliability: class A (separable; brand order held over five months), B (separable; Consistency holds less reliably than Presence), C (separable; Consistency not yet a stable brand trait), D (not separable; drafting pauses for a change-of-direction decision) and U (third wave incomplete). The synthesis data builder computes the class mechanically from the locked verdict files, after reproducing the v1.9 Stage 1 values exactly from the frozen first two waves and checking that both pre-registration tags resolve to their anchored objects on the remote. The computed class is A, with none of the outline's secondary flags raised (§4).

# 4. Evidence

## 4.1 From CV-CPC to φ

The Consistency arc began with a coefficient-of-variation statistic over per-model recall (CV-CPC). Its studies are part of the record but not of the AIAS 2.0 claim, because the instrument was not adopted (Table 2).

| Phase | Locked result | Role here |
|---|---|---|
| v0.30, instrument pilot | Computable CONFIRM; level confound and level correction UNDETERMINED; substrate variation CONFIRM | first operationalization |
| v0.31, cross-category baseline | Computable and cross-category variation CONFIRM (Kruskal–Wallis H = 21.51, p = 0.00025) | lineage |
| v0.32, version-snapshot stability | Rank stability CONFIRMED (ρ = 0.708); magnitude stability and emerging instability FALSIFIED; leave-one-provider-out ρ 0.48–0.82 | lineage |
| v0.33, provider asymmetry | CONFIRMED but modest (mean $\eta^2$ = 0.360, MC p = 0.0007); beyond-Presence criterion met ($\delta\eta^2$ = 0.505, MC p = 0.0001) but uninformative under recognition saturation | lineage |
| v0.34, three-week stability | CONFIRMED (ρ 0.76–0.96 in four of five categories; headphones 0.42); beyond-Presence gate MARGINAL | short-horizon lineage |
| v0.35, phantom brands | Signature CONFIRMED; beyond-Presence UNDETERMINED (control flip) | lineage |
| v0.36, regime emergence | Unstructured (Cell D); all four structure hypotheses NOT SUPPORTED | no typology claimed |
| v1.7, CV-CPC methodology test | H_CPC_Dissociates FALSIFIED (pooled ρ = 0.766, n = 38); defined for 56.7% of in-market brands | instrument not adopted |

: The CV-CPC era. Declined and withdrawn papers (v0.30, v0.31, v0.35, v0.36) are cited by title with their OSF copies.

The CV-CPC studies showed that a consistency quantity could be computed and that it held its order over a model-version change and over three weeks. No attempt to show it was more than Presence gave an interpretable positive result: where recognition saturates, residualizing on Presence leaves nothing, and where recall varies, CV-CPC varies with it. v1.7 made the reason explicit: the coefficient of variation of counts bounded at six is mechanically tied to their mean.

v1.8 rebuilt the instrument on the quasi-binomial basis of §3.3. It reproduced CV-CPC's coupling on the same data (|ρ(CV-CPC, μ)| = 0.682, n = 55) and showed φ to be mean-independent (pooled |ρ(φ, μ)| = 0.091 over 197 brand observations from three analysis sets; 0.082, 0.082 and 0.107 within sets), defined for every brand named at least once (84 of 84, against 55 for CV-CPC) and distinct from the positional agreement index J (ρ(φ, J) = −0.403, n = 74). Figure 2 sets the instruments side by side.

![Coupling of each Consistency measure with Presence or mean recall. CV-CPC sits above the 0.50 independence ceiling; φ and the reported score $C^*$ stay below 0.20 wherever they were measured.](../../reports/figs/aias_2_0/chart_02_coupling_by_instrument.pdf){#fig:coupling width=100%}

## 4.2 Consistency is separable from Presence

On the reported score, separability held in each wave: within-category |ρ($C^*$, P)| was 0.073 in May (n = 55) and 0.082 in June (n = 54), both calibration values, and 0.189 in November (n = 54), the confirmatory test. H_Dissociation_t3 is CONFIRMED. The November coupling is higher than in the first two waves but inside the confirmation band. Change over time is separable as well: the five-month change in a brand's φ rank is unrelated to the change in its recall rank (ρ = 0.032, n = 80; H_Drift_Dissociation CONFIRMED), against a June coupling of 0.151 between the two levels. Figure 3 shows the pattern within each category: brands of similar Presence differ in Consistency, mostly within the upper part of its scale.

![Presence against Consistency for every rated brand, by category, in June and November. Brands below the six-mention floor appear on the strip under each panel at their Presence.](../../reports/figs/aias_2_0/chart_03_presence_by_consistency.pdf){#fig:scatter width=100%}

A moderator test points the same way. Identity load, which shapes how Presence divides between canonical and cultural recall (AIAS 1.0, layer L5), does not moderate Consistency: ρ = −0.008, p_perm = 0.955, n = 53 (v0.37, H_IL_Consistency FALSIFIED). The one moderator tested, on 53 brands in three categories, does not carry over from Presence to Consistency.

## 4.3 The rating floor

At one or two mentions, φ sits close to its binomial expectation whatever the models do, so the scaled score is high by default. In the v1.9 pre-look, a plain average of Presence and the unfloored score would have given brands named once an average of 58.0 (n = 9) against 30.4 for brands never named (n = 28): a premium earned by noise. The floor removes it. Under the floor, 55 of 112 brands were rated in May, 54 in June and 54 in November (49%, 48% and 48%); by category and wave the share ranges from 38% to 58% (Figure 4). The rated set is the set of brands the models name with some regularity; AIAS 2.0's Consistency claims are about those brands.

![Share of brands rated for Consistency, by category and wave. A brand is rated when the six models together name it at least six times out of 36.](../../reports/figs/aias_2_0/chart_06_rating_floor.pdf){#fig:floor width=100%}

## 4.4 Both scores keep their brand order over five months

Presence kept its order almost perfectly: ρ = 0.970 over three weeks and 0.954 over five months (n = 112; $p_{\text{perm}}$ = 0.0001, the smallest value 10,000 draws return), and recall Presence held within every category (ρ 0.927–0.976, five of five above 0.70). H_Presence_Score_Reliability and H_Presence_LongHorizon are CONFIRMED.

Consistency kept its order with more noise. The reported score correlated 0.736 across three weeks (n = 53) and 0.647 across five months (n = 52). The three-week value is a calibration value, since the floor was selected with it in view, so 0.647 is the only out-of-sample estimate of the reported score's stability. No locked test covers the difference between the two; raw φ moved the other way (0.645 to 0.681), and the decay interval for φ (up to 0.168) is wide enough that a loss of that size can be neither shown nor excluded. Part of any agreement statistic's stability comes from the questions themselves: when the models' answers are shuffled within each frame, the five-month correlation still averages 0.438 (95th percentile 0.585). The observed value exceeds that null ($p_{\text{frame}}$ = 0.008), so H_Consistency_Reliability is CONFIRMED. Raw φ shows the same pattern on the larger set of brands for which it is defined: 0.645 over three weeks (n = 83) and 0.681 over five months (n = 80), against a frame-structure null averaging 0.357 (95th percentile 0.509; $p_{\text{frame}}$ = 0.0001); H_Phi_LongHorizon is CONFIRMED. Stability did not decay detectably between the two horizons for either φ (difference 0.019, 95% CI −0.132 to 0.168) or recall (0.002, CI −0.025 to 0.032), so H_Horizon_Decay is MARGINAL. Of the 58 brands below the six-mention line in June (v0.34's recall floor), 56 were still below it in November. Figure 5 summarizes the three statistics.

![Agreement between waves for the three statistics over about three weeks and about five months, with each test's pass mark and, for the two Consistency statistics, the frame-structure null.](../../reports/figs/aias_2_0/chart_04_reliability_ladder.pdf){#fig:reliability width=100%}

## 4.5 Why there is no composite score

The Tri-System framework describes AI Availability as a single 0–100 score. v1.9 tested whether Presence and Consistency can be combined into one without losing either. It evaluated a pre-specified grid of eight composites, two Consistency scores (φ alone, or φ with J), two rules for brands with few mentions (the floor, or shrinkage toward the scale midpoint) and two forms (average, or Consistency modulating Presence), against three constraints at both early waves: Consistency must stay separable from Presence (K1, |ρ| ≤ 0.50), the composite must carry information Presence does not (K2, |ρ(A, P)| ≤ 0.95), and one or two mentions must not buy more than Presence already credits (K3).

No candidate passed (Figure 6). Every floored composite ranked brands almost exactly as Presence did (ρ(A, P) = 0.971–0.997): Presence spans the whole scale, while rated Consistency sits mostly between 60 and 100, so any average follows Presence. Shrinkage tied Consistency to Presence (ρ = 0.715 and 0.773 for φ) and gave low-count brands the windfall K3 forbids (an advantage of 10.3–14.2 points in May against an allowance of 7.3). Adding J raised retest reliability (0.868) but put Consistency on the K1 line (0.456, 0.530). The only candidate that passed K2, φ with J under shrinkage as an average (0.944 and 0.946), failed K1 and K3. Under the pre-registered rule, v1.9 locked no composite, and the November wave replicated the reason: the floored average still tracked Presence (ρ = 0.969).

![The eight pre-specified composites against K1 and K2 in May and June, with the November values for the locked score.](../../reports/figs/aias_2_0/chart_05_no_composite.pdf){#fig:nocomposite width=100%}

## 4.6 What Consistency is not

Four boundaries follow from the record. Consistency is not moderated by identity load as the registries operationalize it, through their cell design (v0.37, a confirmatory null). It carries no phantom-brand signature under φ (v1.8, an exploratory null). It has no regime typology: the only typology test ran on CV-CPC and found none (v0.36). Provider structure was measured only on CV-CPC (v0.33) and is not claimed for φ. On the evidence so far, none of Presence's established structures has been shown to carry over to Consistency; two of the four, typology and provider structure, have not been tested on φ.

# 5. The AIAS 2.0 construct

The outline's wording rule returns class A, whose locked headline reads: "AI Availability measured on two separable components, each holding its brand order over five months on one panel." Table 3 states the construct as eight claims, each with the verdict that governs it.

| Claim | Statement | Governing record | Status |
|-----------|---------------------------|-----------------|--------|
| 1. Two components, one profile | Each brand receives two scores: Presence $P$ (0–100, every brand) and Consistency $C^*$ (0–100, brands named at least six times). They are reported side by side, not combined. | v1.9 Stage 1 (no composite locked) | Locked |
| 2. What Consistency is | How evenly the panel's models name a brand across the same frames, measured by φ and scaled to $C_\varphi$; 100 = identical counts across models, 0 = maximal polarization. | v1.8 instrument; v1.9 scale | Locked |
| 3. Separable from Presence | A brand's Consistency carries information its Presence does not, in level and in change. | H_\allowbreak{}Dissociation_\allowbreak{}t3 (0.189); H_\allowbreak{}Drift_\allowbreak{}Dissociation (0.032) | CONFIRMED |
| 4. Rated where there is evidence | Below six mentions Consistency is not rated; about half the brands fall below the floor in each wave. | v1.9 FLOOR; pre-look | Locked |
| 5. Brand order held over five months | Both scores keep their brand order over 152 days; Consistency does so beyond the question structure. | H_\allowbreak{}Presence_\allowbreak{}Score_\allowbreak{}Reliability (0.954); H_\allowbreak{}Consistency_\allowbreak{}Reliability (0.647) | CONFIRMED |
| 6. No single score | No 0–100 combination of the two adds information to Presence while keeping Consistency separate. | v1.9 Stage 1; November replication (0.969) | Locked |
| 7. Not Presence's structure | No identity-load moderation, no phantom signature under φ, no typology found (tested on CV-CPC only); provider structure not claimed. | v0.37 (null); v1.8 (exploratory null); v0.36 (CV era) | Boundary |
| 8. Position | AIAS 2.0 is the Presence and Consistency profile on one panel; four components remain. | Roadmap; this synthesis | Position |

: The AIAS 2.0 construct. Values in parentheses are the governing rank correlations.

Claims 1, 3 and 5 carry the construct. Claim 1 is a decision forced by evidence rather than taken for convenience: the framework's single 0–100 score remains the goal, but with two components, one spread across the whole scale and the other concentrated near its top, a single score would be Presence under another name. Claim 3 is what makes the second component worth reporting: if Consistency followed Presence, the profile would be one score printed twice. Claim 5 is what makes it a property of the brand rather than of a wave; it holds for the score AIAS 2.0 publishes, and the frame-structure null keeps it honest about how much of that stability the questions themselves supply.

Claims 4 and 7 bound the construct. Consistency speaks only about brands the models name with some regularity, and it does not inherit the moderators and typology that organize Presence. Claim 8 fixes the scope: every number above belongs to one panel, and the scale's maximum depends on the number of models, so the score must be recalibrated before a different panel's values can be compared with these.

# 6. Discussion

For marketing science, the result is a second measured component of AI Availability that is separate from the first. The Tri-System framework proposed AI Availability as a multi-dimensional layer; until now only one dimension had been measured. A brand's Consistency does not follow its Presence, does not respond to the moderator that shapes Presence, and holds its order over five months. The evidence that AI Availability has more than one dimension is therefore no longer conceptual.

For practice, the profile separates two questions a brand team would otherwise read as one. Presence asks how often AI assistants name the brand; Consistency asks whether they agree in doing so. Two brands with the same Presence can differ widely in Consistency (Figure 3), and the difference is of practical interest: a brand named by some models and not others is exposed to which assistant the buyer happens to use, while a brand named evenly is not. Because the two scores move independently over time, a change in one is not evidence about the other, and each needs its own tracking.

The evidence has limits. All results bind to one panel of six models from three providers, queried without web search; that panel is retiring between November 2026 and January 2027, and the current generation of models has not been calibrated. The six are not six independent raters: two models from the same provider may share training data and design, so part of the agreement Consistency measures may reflect shared provenance. Five categories and 112 brands, with 16 to 24 per category, limit the precision of every correlation; the Consistency tests rest on 52 to 54 rated brands. The verdict rules act on point estimates: at that size the 95% sampling margin of a rank correlation is roughly ±0.2 to 0.25 (an approximation; no interval was pre-registered), so the November coupling of 0.189 is compatible with true values above the 0.30 confirmation mark. About half the brands are not rated for Consistency, so the second component describes the regularly named part of each category. Prompts were in English, and recognition was recorded as binary by design. Answers cut off at the token cap can lower one model's recall counts and so register as disagreement between models; at $t_3$ this affected about a third of Gemini 2.5 Flash's calls, and its effect on φ has not been measured. Part of Consistency's stability comes from the structure of the questions, which the frame-structure null measures but does not remove. Stage 1 of v1.9 was calibration on data already seen, and only its Stage 2 is confirmatory. Neither score has been tested against buyer behaviour: separability and reliability are necessary conditions for a useful measure, not evidence that it predicts market outcomes.

# 7. Future research

Four steps follow. First, the profile is to be recalibrated on a new reference panel of the newest models, with web search off and on (v0.42, whose pre-registration was deposited on OSF in November 2026), and its separability and reliability re-tested there before any score from that panel is compared with these. Second, the third component, Ranking, opens AIAS 3.0; when it is measured, the composite question returns under a new calibration lock that carries forward v1.9's constraints and selection rule, so that a future composite is admitted or refused by the same rule. Third, a typology test on φ, which the program has not run, would show whether Consistency has regime structure of its own. Fourth, the profile's predictive validity against behavioural outcomes, the test that neither component has yet faced, belongs to the program's final validation phase; its first step, a test against later change in search interest (v0.43), has a pre-registration deposited on OSF in November 2026, before any of its data were collected.

# Declarations {-}

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This synthesis re-reports measurements taken against brand registries fixed in earlier phases (v0.19--v0.23); it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward unchanged. Two items of record apply. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands --- Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) --- characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry, AKG was substituted with Denon before the v0.19 pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary (v0.19 pre-registration §2.3; v0.19 DEVIATIONS Entry 1). All statistics reported here were computed automatically from locked verdict files; the synthesis outline was locked and deposited before any third-wave score existed; and, apart from the AKG substitution noted above, the author's affiliation played no role in registry construction, scoring, or the resulting verdicts. Samsung Electronics had no role in the design, conduct, analysis, or reporting of this work.

## Funding {-}

Self-funded. No external funding supported this research.

## Ethics {-}

Not applicable; no human subjects. The study analyses responses of large language models queried under their public interfaces.

## Use of AI tools {-}

The author used Anthropic's Claude to assist with analysis code, drafting and editing of text, and figure production. The study design, pre-registered hypotheses and decision rules, and all interpretations are the author's; the author reviewed all content and takes full responsibility for it.

## Data and code availability {-}

Materials are deposited at OSF, `ec6wh/aias_2_0`: the locked outline and its anchor record (tag, commit and file hashes) and deviations record. At publication the deposit adds the synthesis data (`aias_2_0_synthesis_data.json`), the per-brand profiles (`aias_2_0_profiles.csv`), the builder and its tests (`aias_2_0_synthesis_data.py`), and the figure builder. The underlying records are deposited with their source studies (OSF `ec6wh/v19`--`v23`, `v29`--`v37`, `v41`, `methodology/v1_7`, `methodology/v1_8`, `methodology/v1_9`).

## Pre-registration {-}

Synthesis outline locked at `aias-2-0-outline-locked` (commit `f97db70`, November 9, 2026, 13:27 UTC; deposited on OSF at 15:11–15:12 UTC, before any third-wave score; DEVIATIONS Entry 1 records the OSF anchor in place of a tag push). Data lock `aias-2-0-data-locked`; figures `aias-2-0-charts-locked`. The confirmatory tests are those of v0.41 (`v0.41-prereg-r1`) and v1.9 (`v1.9-prereg-r1`).

**Trademark notice.** AIAS™ and Third System™ are trademarks of the research program.

# References {-}

Campbell, D. T., & Fiske, D. W. (1959). Convergent and discriminant validation by the multitrait-multimethod matrix. *Psychological Bulletin*, 56(2), 81--105.

Fleiss, J. L. (1971). Measuring nominal scale agreement among many raters. *Psychological Bulletin*, 76(5), 378--382.

González Castro, P. U. (2026). *AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval*. SSRN 6659000.

González Castro, P. U. (2026). *Tri-System Brand Growth: The AI Mediation Layer*. MSI Working Paper, Report No. 26-132. Marketing Science Institute.

González Castro, P. U. (2026). *The AIAS™ Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy* (v1.2). SSRN 6761698.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification (v1.3)*. SSRN 6797679.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol v1.4: Recognition × Recall Decomposition and Multi-Component AI Availability*. SSRN 6799479.

González Castro, P. U. (2026). *The AIAS™ Presence Measurement Protocol: Multi-Statistic C2 Specification and Two-Channel Recall Decomposition* (v1.5). SSRN 6810758.

González Castro, P. U. (2026). *Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension* (AIAS Methodology v1.6). SSRN 6816340.

González Castro, P. U. (2026). *Consistency without Independence: A Pre-Registered Test of Coefficient-of-Variation as the Consistency Component of AIAS™* (v1.7). SSRN 6878818.

González Castro, P. U. (2026). *A Mean-Independent Consistency Instrument for Cross-Model AI Presence: Redesigning CPC on a Quasi-Binomial Dispersion Basis* (AIAS Methodology v1.8). SSRN 6963359.

González Castro, P. U. (2026). *One Score or Two? Calibrating a Presence and Consistency Composite for AI Brand Availability: A Pre-Registered Calibration with Blind Five-Month Confirmation (AIAS™ Methodology v1.9)*. SSRN 7685126.

González Castro, P. U. (2026). *AI Availability as a Third Measurable Layer of Brand Availability: Five-Substrate Empirical Anchoring of the AIAS™ Presence Measurement Protocol --- Synthesis under Locked v1.6 Methodology* (AIAS 1.0). SSRN 6817841.

González Castro, P. U. (2026). *The Presence Component Is Construct-Valid: A Convergent--Discriminant (Campbell--Fiske) Baseline for AI Availability* (v0.29). SSRN 6870778.

González Castro, P. U. (2026). *Recognition Saturates, Consistency Doesn't: An Instrument-Specification Pilot of the AIAS™ Consistency Component (CPC) across Skincare, Cosmetics, and Automotive* (v0.30). Working paper; OSF `ec6wh/v30`.

González Castro, P. U. (2026). *Consistency Across Categories: A Cross-Category Baseline for the AIAS™ Consistency Component (CPC)* (v0.31). Working paper; OSF `ec6wh/v31`.

González Castro, P. U. (2026). *Version-Snapshot Stability of an AI-Presence Consistency Score: A Pre-Registered Two-Arm Cross-Generation Test of the v1.7 CPC Operationalization* (v0.32). SSRN 6898581.

González Castro, P. U. (2026). *Provider-Asymmetric Consistency in AI Brand Availability: A Pre-Registered Re-Analysis: Modest between-Provider Structure in CV-CPC Recall, and the Limits of a Beyond-Presence Gate under Recognition Saturation* (v0.33). SSRN 6909019.

González Castro, P. U. (2026). *Two-Wave Temporal Stability of an AI Brand-Recall Consistency Quantity: A Pre-Registered Longitudinal Re-Acquisition Across Five Product Categories (AIAS™ v0.34)*. SSRN 6915458.

González Castro, P. U. (2026). *Control-Dependent Verdicts in a Phantom-Brand Consistency Contrast: A Pre-Registered Control-Flip Result on Frozen Multi-Substrate Inputs* (v0.35). Working paper; OSF `ec6wh/v35`.

González Castro, P. U. (2026). *Does Cross-Platform Consistency Have Regime Structure? A Pre-Registered Clustering Test Against a Frozen Brand-Presence Classification* (v0.36). Working paper; OSF `ec6wh/v36`.

González Castro, P. U. (2026). *Identity Load Does Not Moderate Cross-Model Consistency: A Pre-Registered Component-Dissociation Null (AIAS™ v0.37)*. Working paper; OSF `ec6wh/v37`.

González Castro, P. U. (2026). *Five-Month Stability of AI Brand Consistency and Presence: A Pre-Registered Third Wave on a Retiring Six-Model Panel (AIAS™ v0.41)*. SSRN 7685100.

González Castro, P. U. (2026). *Recognition Ceiling, Dissociation Replication, and Cultural-Channel Asymmetry on an Audiophile Headphones Substrate* (v0.19). SSRN 6809182.

González Castro, P. U. (2026). *Type 2 Emergence and First Prospective v1.5 C2 Calibration on a Skincare IL-Gradient Substrate* (v0.20). SSRN 6811441.

González Castro, P. U. (2026). *Type 2 Confirmation, Recognition Ceiling, and Phantom Brand Persistence on a Cosmetics IL-Gradient Substrate* (v0.21). SSRN 6815378.

González Castro, P. U. (2026). *Phantom Brand Persistence on a Heritage-Saturated Automotive Substrate --- Cell D_Defunct as Pure-Phantom Upper-Bound Test* (v0.22). SSRN 6829118.

González Castro, P. U. (2026). *AIAS Presence Index v0.23: Premium Spirits Recognition Ceiling, Recall-driven Regime Classification, and the Conglomerate Ownership Hypothesis across 24 Brands and Six Large Language Models*. SSRN 6834298.

McCullagh, P., & Nelder, J. A. (1989). *Generalized Linear Models* (2nd ed.). Chapman and Hall.

Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The preregistration revolution. *Proceedings of the National Academy of Sciences*, 115(11), 2600--2606.

Romaniuk, J., & Sharp, B. (2022). *How Brands Grow, Part 2* (Revised ed.). Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

Shrout, P. E., & Fleiss, J. L. (1979). Intraclass correlations: Uses in assessing rater reliability. *Psychological Bulletin*, 86(2), 420--428.
