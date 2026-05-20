---
title: |
  Panel Inadequacy and the Recognition--Recall Dissociation\
  on the Premium Kitchenware Substrate:\
  AIAS v0.17
author: |
  Pablo Ulpiano González Castro\
  School of Visual Arts, MPS Branding Program, New York, NY\
  (primary academic affiliation)\
  Third System™ (research entity; data archive and methodology venue)\
  Correspondence: pablou@pablou.com $\cdot$ pablou.com\
  ORCID: 0009-0003-8968-9990
date: May 2026
keywords: AI Availability; AIAS; LLM-mediated retrieval; brand measurement; Identity Load; recognition memory; recall memory; pre-registration; premium kitchenware
abstract: |
  This paper reports the v0.17 Premium Kitchenware program of the AIAS™ Presence Measurement research line. Following the pre-registered v0.17-prereg-r1 protocol, a 16-brand panel spanning three tradition cells (European, American, Japanese) was assembled and tested against the pre-registered substantive hypothesis $H_{\text{Regime4\_kitchenware}}$ and against the joint v0.16/v0.17 hypothesis $H_{\text{IdentityLoad\_moderator}}$. The substantive verdict is FALSIFIED on panel inadequacy: post-Phase-B operational panel worldwide $n = 10$ breached the pre-registered C1 floor of $n \geq 12$, with the Japanese cell fully collapsing (0/3 eligible) and the American cell sustaining partial attrition (4/6 eligible). The pre-registered joint verdict matrix routes the Identity-Load moderator hypothesis to AMBIGUOUS pending v0.18 indie fragrance. Beyond the substantive verdict, v0.17 produced a methodologically significant secondary finding: Phase A and Phase B of the AIAS protocol measure dissociable constructs of AI Availability. The canonical case is Iwachu, a Japanese cookware brand that achieved Phase A C_P PASS at 6/6 (recognition anchoring positive in all six reference LLMs) and Phase B EXCLUDED_E1a at 0/18 (zero recall presence in unprompted category retrieval across all six reference LLMs and all three category queries). The dissociation generalized across the Japanese cell. This empirical finding motivated the v1.4 Methodology paper revision specifying AI Availability as a multi-component construct comprising Recognition and Recall components. v0.17 also produced an observation of substrate-substitution attrition (LLM-substrate Phase B has approximately twice the attrition rate of Trends-substrate Phase B), and a cross-cultural confound observation (Western-language LLM training-data bias is large enough on cross-cultural substrates to plausibly swamp the Identity Load signal). Both observations are forward actions for v0.18 panel design and for the v1.4 protocol revision.
---

# 1. Introduction

The v0.17 Premium Kitchenware program is the eighth pre-registered phase of the AIAS™ Presence Measurement research line (González Castro 2026a). It is positioned as the second leg of a two-leg joint test of the Identity Load moderator hypothesis $H_{\text{IdentityLoad\_moderator}}$, with v0.16 Kitchen Knives (González Castro 2026b, SSRN 6791999) as the first leg. Premium kitchenware was selected as the v0.17 substrate because it falls in the same medium-Identity-Load tier as kitchen knives, allowing within-tier replication of the v0.16 PARTIAL verdict for $H_{\text{Regime4\_replication\_knives}}$.

The pre-registration `v0.17-prereg-r1` (commit `3ebe426`) was finalized on 2026-05-19 against the v1.3 Methodology protocol (González Castro 2026c, SSRN 6797679) and committed prior to any data acquisition. The pre-registration anticipated three possible outcome paths for the substantive hypothesis: CONFIRMED, PARTIAL, or FALSIFIED, with FALSIFIED resolving via either panel-inadequacy (¬C1) or effect-size (¬C2) breach. The pre-registration also committed in advance to a joint verdict matrix specifying how v0.16 and v0.17 outcomes combine to resolve the Identity Load moderator hypothesis.

This paper reports the empirical outcomes of v0.17 acquisition, classification, and Phase B mentionability validation; the formal verdicts that follow mechanically from the pre-registered decision rules; and the methodological findings that motivated the v1.4 Methodology revision (González Castro 2026d). The Methods section is intentionally brief: v0.17 operates under the v1.4 Methodology canonical specification, and protocol mechanics are documented in that paper. The Results and Discussion sections carry the substantive content.

## 1.1 Outcomes in Summary

Three principal outcomes:

1. **Substantive verdict.** $H_{\text{Regime4\_kitchenware}}$ FALSIFIED on panel inadequacy. Worldwide eligible $n = 10$ at end of Phase B, below the pre-registered C1 floor of $n \geq 12$. The pre-registration explicitly anticipated this outcome path; no protocol amendment or verdict reframing was required.

2. **Joint verdict.** $H_{\text{IdentityLoad\_moderator}}$ AMBIGUOUS — the pre-registered joint v0.16/v0.17 verdict matrix at cell `PARTIAL × FALSIFIED` routes the Identity Load moderator hypothesis to v0.18 indie fragrance for resolution.

3. **Methodological finding.** Phase A C_P and Phase B mention rate measure dissociable components of AI Availability. The Iwachu canonical case—Phase A C_P PASS at 6/6, Phase B EXCLUDED_E1a at 0/18—is the strongest empirical demonstration to date in the AIAS programme that AI Availability is multi-component (Recognition and Recall). This finding motivated the v1.4 Methodology revision and is potentially of greater theoretical significance than the substantive verdict itself.

## 1.2 Paper Structure

§2 reproduces the pre-registered hypotheses and decision rules. §3 summarizes the v0.17 methodology with explicit reference to v1.4 for protocol details. §4 reports the Phase A cascade results and Phase A lock. §5 reports the Phase B mentionability results, the C1 floor breach, and the substantive verdicts. §6 reports the methodological findings (Recognition--Recall dissociation, substrate-substitution attrition, cross-cultural confound). §7 discusses theoretical implications and v0.18 forward actions. §8 contains declarations.

# 2. Pre-Registered Hypotheses and Decision Rules

## 2.1 Substantive Hypothesis

$H_{\text{Regime4\_kitchenware}}$: Premium kitchenware exhibits the Regime 4 pattern of LLM-mediated retrieval per the Methodology v1.2 four-regime taxonomy (González Castro 2026e, SSRN 6761698), conditional on panel adequacy and effect-size persistence under tradition and age controls.

The pre-registered decision rules are:

- **C1 — Panel adequacy.** Worldwide $n \geq 12$ brands surviving the 14-day Trends floor and Phase A pivot validation per v1.3 §6.4.2.
- **C2 — Effect threshold.** Spearman $\rho$ on the operational panel at $t_1$ satisfies the Regime 4 boundary criteria per the four-regime taxonomy.
- **C3 — Control persistence.** Partial $\rho$ controlling for age and tradition retains the Regime 4 boundary criteria at $t_1$ and at $t_2$.

The pre-registered verdict structure:

- **CONFIRMED:** $C_1 \wedge C_2 \wedge C_3$.
- **PARTIAL:** $C_1 \wedge C_2 \wedge \neg C_3$ (positive partial after controls; weak-signature boundary case).
- **FALSIFIED:** $\neg C_1 \vee \neg C_2$ (panel-inadequacy or effect-threshold failure).

## 2.2 Joint Hypothesis

$H_{\text{IdentityLoad\_moderator}}$: Identity Load moderates the strength of the Regime 4 pattern. Specifically, the pattern is hypothesized to weaken or invert as Identity Load decreases. The hypothesis is tested jointly across v0.16 Kitchen Knives (medium Identity Load) and v0.17 Premium Kitchenware (medium Identity Load), with v0.18 indie fragrance (higher Identity Load) and future low-IL substrates extending the test in either direction.

The pre-registered joint verdict matrix specifies, for each combination of v0.16 and v0.17 outcomes, the corresponding $H_{\text{IdentityLoad\_moderator}}$ verdict. The relevant cell for v0.17's outcome path is `PARTIAL × FALSIFIED`, which the pre-registration routes to AMBIGUOUS pending v0.18.

## 2.3 Descriptive Sensitivities

Two descriptive sensitivities were pre-registered alongside the substantive hypotheses:

- **§2.3.1 US-versus-worldwide divergence.** Per the v0.16 SECOND APERTURE finding (US/worldwide divergence on knives: worldwide $\rho = +0.022$ vs US $\rho = -0.881$), the kitchenware substrate was expected to surface similar registry-coverage asymmetry. Worldwide and US sub-panels are reported separately as descriptive sensitivities; only the worldwide panel resolves the primary hypothesis decision rules.

- **§2.3.2 Tradition-cell richness.** Per-cell $n$ (European / American / Japanese) at post-floor; per-cell Regime classification per the four-regime taxonomy; per-cell $\rho$ if cell $n \geq 5$ (otherwise reported as "cell n below ρ-reporting floor"). No moderator hypothesis is tested at the cell level.

# 3. Methods

v0.17 operated under the v1.4 Methodology canonical specification (González Castro 2026d). Protocol mechanics—Phase A automated C_P classification, cascade pipeline, LLM-substrate Phase B with mechanical alias generation, tier vocabulary, and audit-trail discipline—are documented in v1.4 and are not re-stated here. This section reports only the v0.17-specific configuration.

## 3.1 Substrate and Panel

The v0.17 substrate is premium cookware. The pre-registered 16-brand panel comprises three tradition cells:

- **European cell (n=6):** Le Creuset (primary pivot), Staub, Mauviel, Demeyere, Fissler, de Buyer.
- **American cell (n=6):** All-Clad (primary pivot), Lodge, Made In, Field Company, Smithey, Hestan.
- **Japanese cell (n=4):** Vermicular (primary pivot), Iwachu, Sori Yanagi, Noda Horo. Noda Horo was pre-registered as borderline ("borderline_classification": true, "borderline_resolution_at": "phase_b_topic_id").

The panel was pre-registered at worldwide $n = 16$ pre-floor, with conservative anticipated attrition of 1–3 brands leaving a post-floor worldwide $n = 13$–15, comfortably above the C1 floor of $n \geq 12$.

## 3.2 Reference Panel

The Phase A and Phase B LLM reference panel is the locked six-slot configuration: claude-opus-4-5, claude-sonnet-4-5, gpt-4o, gpt-4o-mini, gemini-2.5-flash, gemini-2.5-flash-lite. Three Google model substitutions occurred during the v0.17 acquisition window and are documented in DEVIATIONS Entries 2 and 3 (provider model sunsetting; substitutions made before any pivot-validation data acquisition).

## 3.3 Phase B Category Queries

The pre-registered LLM-substrate Phase B (per v1.4 §4.2 canonical specification, anticipated during v0.17 as DEVIATIONS Entry 7) uses three tradition-agnostic category queries:

- $Q_1$: "What are the best premium cookware brands? Please list several with brief descriptions."
- $Q_2$: "Recommend high-quality cookware brands for serious home cooks. Name several specific brands."
- $Q_3$: "What cookware brands do professional chefs use? List several."

Each query is issued once per reference slot, producing 18 total response cells per panel.

## 3.4 Pre-Registered Substrate-Substitution

DEVIATIONS Entry 7 (committed 2026-05-19, commit `55e28ed`) records the v0.17-time substitution of LLM-substrate Phase B for the v1.3-inherited Trends-substrate Phase B. The substitution is provisional in v0.17 and canonical in v1.4. The substantive consequence is that Phase B in v0.17 measures LLM mentionability rather than Trends signal; the operational consequence is that Phase B attrition rates may differ from those anticipated by the pre-registered panel design.

# 4. Phase A Results

## 4.1 Cascade Outcome

Phase A measurement against the six-slot reference panel produced one cascade event in the Japanese cell. Tradition-cell verdicts:

\begin{table}[h]
\centering
\begin{tabular}{lllll}
\hline
\textbf{Cell} & \textbf{Pivot} & \textbf{Anchoring} & \textbf{Verdict} & \textbf{Cascade depth} \\
\hline
European & Le Creuset & 6/6 & C\_P PASSED & 0 \\
American & All-Clad & 6/6 & C\_P PASSED & 0 \\
Japanese & Vermicular & 4/6 & C\_P FAILED & --- \\
Japanese (cascaded) & Iwachu & 6/6 & C\_P PASSED & 1 \\
\hline
\end{tabular}
\caption{Phase A cascade outcomes per tradition cell. Cascade depth indicates the ordinal position of the activated pivot relative to the cell's pre-registered alternate sequence.}
\end{table}

The European and American primary pivots achieved C_P PASS at full 6/6 anchoring without cascade. The Japanese primary pivot Vermicular C_P FAILED at 4/6: two reference models (gpt-4o-mini at slot 4; gemini-2.5-flash at slot 5) led their responses with non-substrate referents (slot 4 framed "vermicular" as a term with multiple meanings; slot 5 defined "vermicular" as an adjective meaning worm-like). The other four reference models led with the Japanese cookware brand identity. The cascade activated Japanese cell ordinal 2, Iwachu, which achieved C_P PASS at 6/6 with classifier rationales reading uniformly as variations on "Japanese manufacturer of cast iron cookware."

## 4.2 Phase A Lock and Operational Panel

Phase A formally closed on 2026-05-19 with tag `v0.17-phase-a-locked` (commit `8cdf0cd`). The post-cascade operational panel comprised 15 brands: the 6 European, 6 American, and the Japanese cell minus the descoped Vermicular (Iwachu, Sori Yanagi, Noda Horo). Worldwide $n = 15$, comfortably above the C1 floor of $n \geq 12$. C1 floor HOLDS at end of Phase A with margin of 3 brands above floor.

# 5. Phase B Results

## 5.1 Mentionability Tier Verdicts

Phase B measurement on the 15-brand panel against the locked six-slot reference panel and three category queries produced the per-brand mentionability tier verdicts shown in Table 2.

\begin{table}[h]
\centering
\small
\begin{tabular}{lllrrl}
\hline
\textbf{Brand} & \textbf{Cell} & \textbf{Role} & \textbf{Mentions} & \textbf{Rate} & \textbf{Tier} \\
\hline
Le Creuset & european & pivot & 18/18 & 1.000 & PASS \\
Mauviel & european & alt 2 & 18/18 & 1.000 & PASS \\
All-Clad & american & pivot & 18/18 & 1.000 & PASS \\
Staub & european & alt 1 & 17/18 & 0.944 & PASS \\
Demeyere & european & alt 3 & 15/18 & 0.833 & PASS \\
Lodge & american & alt 1 & 7/18 & 0.389 & PASS \\
de Buyer & european & alt 5 & 6/18 & 0.333 & PASS \\
Hestan & american & alt 5 & 6/18 & 0.333 & PASS \\
Made In & american & alt 2 & 4/18 & 0.222 & PASS \\
Fissler & european & alt 4 & 2/18 & 0.111 & PASS\_E5 \\
Field Company & american & alt 3 & 0/18 & 0.000 & EXCLUDED\_E1a \\
Smithey & american & alt 4 & 0/18 & 0.000 & EXCLUDED\_E1a \\
Iwachu & japanese & pivot & 0/18 & 0.000 & EXCLUDED\_E1a \\
Sori Yanagi & japanese & alt 2 & 0/18 & 0.000 & EXCLUDED\_E1a \\
Noda Horo & japanese & alt 3 & 0/18 & 0.000 & EXCLUDED\_E1a \\
\hline
\end{tabular}
\caption{Phase B mentionability tier verdicts. Mentions are out of 18 measurement cells (3 category queries $\times$ 6 reference LLMs). Tier thresholds: PASS at mention rate $\geq 1/6$; PASS\_E5 at $0 < \text{rate} < 1/6$; EXCLUDED\_E1a at rate $= 0$.}
\end{table}

Per-cell summary: European cell intact at 6/6 eligible (all PASS); American cell at 4/6 eligible with two EXCLUDED_E1a (Field Company, Smithey); Japanese cell fully collapsed at 0/3 eligible (all three remaining brands EXCLUDED_E1a). Worldwide eligible $n = 10$.

Figure 1 displays the per-brand mention-rate distribution across the 15-brand operational panel, sorted descending and color-coded by tradition cell. The distribution shape itself is informative: the European cell saturates the high-mention end; the American cell occupies the mid-range with two long-tail exclusions; the Japanese cell is concentrated entirely at zero.

\begin{figure}[H]
\centering
\includegraphics[width=0.90\textwidth]{fig1_mention_rates.pdf}
\caption{Phase B mention-rate distribution across the 15-brand operational panel. Mention rate is the proportion of $3 \times 6 = 18$ measurement cells (three category queries against the six-slot LLM reference panel) in which the brand was mentioned. Bars are sorted descending and color-coded by tradition cell. PASS threshold ($1/6$) is shown as a dashed vertical reference. EXCLUDED tags mark brands with zero mentions across all 18 cells.}
\label{fig:phase_b_mention_rates}
\end{figure}

## 5.2 Noda Horo Borderline Resolution

Noda Horo was pre-registered as a borderline classification case with resolution scheduled at Phase B per the brand registry field `borderline_resolution_at: "phase_b_topic_id"`. Noda Horo's Phase B tier verdict (EXCLUDED_E1a at 0/18 mentions) constitutes the protocol-mandated borderline resolution: OUT_OF_SCOPE (enamelware-only; not in-scope premium cookware). Noda Horo is formally descoped from the v0.17 operational panel.

## 5.3 C1 Floor Breach

Worldwide eligible $n = 10$ at end of Phase B is below the pre-registered C1 floor of $n \geq 12$. C1 is BREACHED with a deficit of 2 brands. Per the pre-registered decision rule (§2.1): FALSIFIED requires $\neg C_1 \vee \neg C_2$. $\neg C_1$ is satisfied; FALSIFIED follows mechanically. C2 and C3 are not evaluated because the verdict resolves at C1.

The pre-registration anticipated this outcome path explicitly. Pre-reg §3.2 specifies that "Worldwide panel adequacy holds even under full Japanese cell collapse ($n_{\text{after\_Japanese\_collapse}} = 12$, exactly at C1)." The observed outcome combined full Japanese cell collapse with partial American cell attrition (Field Company, Smithey), producing $n = 10$—below the boundary the pre-registration had identified as the worst-case Japanese-only collapse scenario. The pre-reg's joint verdict matrix at cell `PARTIAL × FALSIFIED` already specified the joint Identity Load verdict for exactly this outcome: AMBIGUOUS pending v0.18.

Figure 2 summarizes the cell-level attrition pattern. The European cell remained intact from pre-Phase-A registration through post-Phase-B operational state. The American cell sustained partial attrition: two long-tail brands (Field Company, Smithey) failed Phase B mentionability and were descoped. The Japanese cell fully collapsed: Vermicular was descoped at Phase A (C_P FAIL); Iwachu, Sori Yanagi, and Noda Horo were descoped at Phase B (zero mentions each). Worldwide $n$ dropped from 16 to 10 across the two attrition stages, breaching the C1 floor of 12 by a deficit of 2.

\begin{figure}[H]
\centering
\includegraphics[width=0.85\textwidth]{fig3_cell_collapse.pdf}
\caption{Per-cell brand survival from registered panel (pre-Phase-A) to operational panel (post-Phase-B). Light grey bars show the pre-registered cell sizes; Indigo bars show the post-Phase-B eligible counts. Worldwide $n$ dropped from 16 to 10, below the C1 adequacy floor of 12. The European cell remained intact; the American cell lost two long-tail brands; the Japanese cell collapsed entirely.}
\label{fig:cell_collapse}
\end{figure}

## 5.4 Formal Substantive Verdicts

The formal v0.17 substantive verdicts follow mechanically from the pre-registered decision rules:

> $H_{\text{Regime4\_kitchenware}}$: **FALSIFIED on panel inadequacy** ($\neg C_1$; worldwide $n = 10 < 12$).

> $H_{\text{IdentityLoad\_moderator}}$ (joint v0.16/v0.17): **AMBIGUOUS** — kitchenware fails C1; Identity Load moderator hypothesis inconclusive pending v0.18 indie fragrance.

The Phase B lock document (`osf/v17/phase_b_lock.md` at commit `afa950c`, tag `v0.17-phase-b-locked`) and the formal verdict document (`osf/v17/v0_17_verdict.md` at the same commit) are the canonical references.

# 6. Methodological Findings

Beyond the substantive verdicts, v0.17 produced three methodologically significant findings that motivated the v1.4 Methodology paper revision (González Castro 2026d).

## 6.1 Recognition--Recall Dissociation: The Iwachu Canonical Case

Iwachu's Phase A C_P verdict (6/6 PASS) and Phase B mention rate (0/18 EXCLUDED_E1a) constitute a structurally robust dissociation between two measurement surfaces of LLM-mediated brand retrieval. At Phase A, the disambiguation query "Who or what is Iwachu?" produced six responses, each of which led with an identification statement placing Iwachu within the cookware substrate. The classifier rationales read uniformly as variations on "Japanese manufacturer of cast iron cookware." At Phase B, the same six reference LLMs queried with three unprompted category queries about premium cookware brands produced 18 response cells in which Iwachu was mentioned zero times.

Figure 3 plots Phase A C_P anchoring scores against Phase B mention rates for the four pivots that received Phase A measurement. Le Creuset and All-Clad occupy the full-Presence corner (high recognition, high recall). Vermicular sits in the descoped region (Phase A FAIL at 4/6, no Phase B measurement). Iwachu sits alone in the recognition-only corner: full recognition anchoring (6/6) at Phase A, zero recall presence (0/18) at Phase B. The empty quadrant in the upper-left—low recognition, high recall—is theoretically possible but not observed: a brand cannot generate high category-recall presence without underlying identity representation in the LLM's training.

\begin{figure}[H]
\centering
\includegraphics[width=0.90\textwidth]{fig2_dissociation.pdf}
\caption{Phase A C_P anchoring score (x-axis, out of 6 reference LLMs) versus Phase B mention rate (y-axis, mentions / 18 cells) for the four pivot brands that received Phase A measurement. Vermicular ($x=4$) failed the Phase A supermajority threshold (5/6) and was descoped before Phase B. Le Creuset, All-Clad, and Iwachu all achieved Phase A 6/6. Iwachu's Phase B mention rate of zero, while Le Creuset and All-Clad saturate Phase B, is the canonical Recognition--Recall dissociation case: full recognition anchoring without any recall presence in unprompted category retrieval.}
\label{fig:dissociation}
\end{figure}

The dissociation is observable at the within-LLM level: the same model that produced "Iwachu is a Japanese cookware brand" in response to the Phase A query did not include Iwachu in its response to the Phase B query "What are the best premium cookware brands?". This is not classifier disagreement, prompt artifact, or measurement noise. The brand has stable identity in the LLM's representation (the model knows what Iwachu is) but no recall presence in category-conditioned retrieval (the model does not surface Iwachu when asked about its category).

The pattern generalized across the Japanese cell. Sori Yanagi and Noda Horo, like Iwachu, received 0/18 mentions at Phase B. The full Japanese cell at Phase B exhibited the same dissociation pattern: stable identity (for Iwachu, confirmed at Phase A; for Sori Yanagi and Noda Horo, assumed by symmetry pending direct measurement) but zero recall presence.

This empirical pattern motivated the v1.4 Methodology revision specifying AI Availability as a multi-component construct with Recognition and Recall as the two principal components (González Castro 2026d, §§2.1–2.5). The v0.17 program is the empirical anchor for the multi-component construct claim.

## 6.2 Substrate-Substitution Attrition

The v0.17 pre-registration anticipated 1–3 brands of Phase B attrition based on the v1.3-inherited Trends-substrate Phase B specification. The provisional LLM-substrate Phase B (DEVIATIONS Entry 7) produced 5 brands of attrition: the full Japanese cell (3) and the long-tail American cell brands Field Company and Smithey (2). Observed attrition was approximately twice the pre-registration's worst-case Trends-substrate estimate.

The mechanism is intuitive in retrospect. Google Trends signal is approximately democratic across brands with non-trivial market presence: even niche brands with modest search volume produce non-zero signal on a 14-day out-of-sample window. LLM unprompted category recall is approximately winner-take-most: when asked "What are the best cookware brands?", LLMs concentrate their responses on the most prominent five-to-ten brands and rarely mention beyond that band. The two substrates measure related constructs (brand prominence in market awareness) on the surface but differ sharply in their concentration profiles at the long-tail end.

The substrate-substitution attrition observation directly contributed to the v0.17 C1 floor breach: had Phase B operated on the Trends substrate (per the pre-registration's original assumption), the European and American attrition might have been lower, with the Japanese cell collapse alone leaving worldwide $n = 12$ at the C1 floor exactly (per pre-reg §3.2's calibration). The substrate substitution—justified on substrate-coherence grounds (DEVIATIONS Entry 7) and now canonical in v1.4—has different panel-survival characteristics that were not accounted for in the pre-registered panel design. This is a methodological finding rather than a protocol defect: future programs operating under v1.4 should calibrate panel over-provisioning for LLM-substrate Phase B's higher natural attrition rate.

## 6.3 Cross-Cultural Confound on Cross-Cultural Substrates

The Japanese cell's full collapse at Phase B is hard to disambiguate from Western-language LLM training-data bias on a cross-cultural substrate. All three Japanese brands carried high Identity Load by the Tri-System theoretical framework: Iwachu's approximately 400-year nambu-tekki heritage; Sori Yanagi's designer-craft heritage; Noda Horo's enamelware heritage. By the substantive prediction of $H_{\text{IdentityLoad\_moderator}}$ (higher Identity Load → stronger AI Availability), these brands should have shown stronger AI Availability than equivalently-positioned but lower-IL brands. The opposite pattern was observed: zero Phase B Recall across the cell.

Two non-trivial readings:

**Reading 1: Identity Load does not moderate AI Availability.** The Japanese cell's collapse is direct disconfirming evidence for the moderator hypothesis. High-IL brands receive no more AI Availability than low-IL brands; if anything, the cross-cultural high-IL brands receive less.

**Reading 2: Western-language training-data bias is a confound large enough on cross-cultural substrates to swamp the Identity Load signal.** The Japanese brands' absence from English-language LLM training data dominates whatever Identity Load effect might otherwise operate. The hypothesis is not disconfirmed but is untestable on this substrate.

The v0.17 data does not distinguish between these readings. The pre-registered FALSIFIED-on-panel-inadequacy verdict was reached on independent grounds (C1 floor breach), which left the Identity Load moderator hypothesis at AMBIGUOUS per the pre-registered joint matrix.

The methodological implication is structurally important: AIAS measurement on cross-cultural substrates requires a confound-control reporting protocol. The v1.4 Methodology paper (§6.2) specifies this requirement and recommends same-language substrates for clean Identity Load tests. v0.18 indie fragrance, with entirely English-language category surface, is the immediate forward action.

# 7. Discussion

## 7.1 Substantive Implications

The substantive FALSIFIED verdict on $H_{\text{Regime4\_kitchenware}}$ is informationally weaker than a CONFIRMED or PARTIAL verdict would have been. Panel-inadequacy failures do not provide evidence about the underlying substrate; they only indicate that the operational panel size was insufficient to support the planned analysis. The pre-registration's joint verdict matrix routes the substantive Identity Load question to v0.18 for resolution. v0.17's substantive contribution is therefore primarily its role as the first leg of the joint test—establishing that the kitchenware substrate produces panel-collapse outcomes on cross-cultural cells under the v1.4 LLM-substrate Phase B specification.

The pattern of the collapse is itself informative even where the substantive verdict is null. The European cell remained intact at 6/6 eligible with strong mention rates (Le Creuset, Mauviel, All-Clad at saturation; Staub and Demeyere near-saturated). The American cell sustained partial attrition with mid-tier brands (Lodge, Hestan, Made In, de Buyer) sitting in the 0.22–0.39 mention rate range and the long-tail (Field Company, Smithey) at zero. The Japanese cell collapsed entirely. Cross-cell, the pattern suggests Phase B mentionability is approximately monotone in English-language LLM training-data coverage: cells with strong English-language coverage retain mid-tier brands; cells with weak English-language coverage lose even high-Identity-Load anchored brands.

## 7.2 Methodological Implications

The Recognition--Recall dissociation finding (§6.1) is, in the author's assessment, the most theoretically significant single result the AIAS programme has produced to date. Recognition and Recall are not interchangeable measurement surfaces; they have different cognitive-architectural properties; they produce dissociable verdicts on the same brands. The v1.4 Methodology revision formalizes this distinction as the protocol's foundational measurement structure.

The implication for the broader Tri-System theoretical framework (González Castro 2026f, manuscript under preparation): AI Availability, as the third system of brand availability alongside Mental Availability and Physical Availability, requires multi-component measurement. A single-metric proxy for AI Availability is inadequate. The Iwachu case demonstrates that a brand can have full Recognition with zero Recall; such a brand has partial AI Availability but is functionally invisible in AI-mediated category retrieval. Consumer behavior in AI-mediated commerce depends on what AI intermediaries spontaneously surface (Recall), not on what they can identify when prompted (Recognition). The substantive theoretical interest is in the Recall component; the Recognition component is methodologically important as a substrate-anchoring gate.

The substrate-substitution attrition finding (§6.2) is a forward action for v0.18 and subsequent program design. The cross-cultural confound observation (§6.3) is a forward action for cross-cultural AIAS measurement design more broadly.

## 7.3 Forward Actions for v0.18

The pre-registration's joint verdict matrix already commits v0.18 to indie fragrance as the deciding test of $H_{\text{IdentityLoad\_moderator}}$. Three v0.17 lessons inform v0.18 design:

1. **Panel over-provisioning for LLM-substrate attrition.** v0.18 cells should be sized assuming approximately 30–50% Phase B attrition at the long-tail end, per §6.2. For a three-cell panel with worldwide C1 floor at $n \geq 12$, this implies cell sizes of at least 6 brands.

2. **Same-language substrate for clean IL test.** Indie fragrance is entirely English-language; the cross-cultural confound that contaminated v0.17 does not apply. The Identity Load gradient within indie fragrance can be tested on equal LLM-coverage terms.

3. **Recognition--Recall dissociation as substrate property.** v0.18's Phase A and Phase B will be analyzed not only against the substantive hypothesis but also against the Recognition--Recall dissociation pattern. If the dissociation generalizes to a same-language substrate, the v1.4 Methodology's multi-component construct claim is strengthened; if the dissociation is specific to cross-cultural substrates, the claim narrows.

## 7.4 Limitations

The v0.17 program has three principal limitations:

**Panel design pre-substrate-substitution.** The pre-registration's panel was sized for Trends-substrate Phase B attrition. The substrate substitution (DEVIATIONS Entry 7) was implemented after pre-registration lock and produced higher-than-expected attrition. The pre-registered FALSIFIED verdict is mechanically correct but is partially a consequence of the substrate substitution rather than the substantive hypothesis being tested. This limitation is documented and motivates the v1.4 specification.

**Cross-cultural confound on Japanese cell.** As discussed in §6.3, the Japanese cell's collapse cannot be cleanly attributed to either the Identity Load null or the Western-LLM bias confound. v0.18's same-language design addresses this limitation; v0.17 itself does not resolve it.

**Single substrate, single time window.** v0.17 measures one substrate at one time window. The Recognition--Recall dissociation finding generalizes within v0.17 across cells and brands but has not yet been replicated across substrates or time windows. v0.18 will provide the cross-substrate replication; the time-window replication is a v1.5+ forward action.

# 8. Declarations

**Author affiliations.** Pablo Ulpiano González Castro. School of Visual Arts, MPS Branding Program, New York, NY (primary academic affiliation). Third System™ (research entity; data archive and methodology venue).

**Correspondence.** pablou@pablou.com $\cdot$ pablou.com. ORCID 0009-0003-8968-9990.

**Declaration of Interest.** The author is employed by Samsung Electronics America in a corporate brand governance role. The AIAS research program is conducted outside the scope of employment, on personal time, with no Samsung resources or data. Samsung has no review, approval, or veto rights over AIAS publications. The author has no financial or material interest in any of the brands measured in the v0.17 Premium Kitchenware panel.

**Funding.** Self-funded.

**Ethics.** Not applicable. No human subjects. Measurement is on publicly accessible APIs (Anthropic, OpenAI, Google) and pre-specified LLM prompts.

**Data availability.** All v0.17 data, code, classification ledgers, Phase B response caches, DEVIATIONS entries, lock documents, and verdict documents are publicly available via the AIAS programmatic git repository and OSF project `ec6wh`. Specific references for v0.17:
- Pre-registration: `registries/PRE_REGISTRATION_v0_17.md` at commit `3ebe426`, tagged `v0.17-prereg-r1`.
- Phase A lock: `osf/v17/phase_a_lock.md` at commit `8cdf0cd`, tagged `v0.17-phase-a-locked`.
- Phase B lock + verdict: `osf/v17/phase_b_lock.md` and `osf/v17/v0_17_verdict.md` at commit `54c83ec`, tagged `v0.17-phase-b-locked`.
- DEVIATIONS entries: `osf/v17/DEVIATIONS.md` (Entries 1–8).

**Pre-registration compliance statement.** This paper reports outcomes that follow mechanically from the pre-registered decision rules in `v0.17-prereg-r1` §§2.1, 2.2, and 2.3. No post-acquisition decision rule modification, threshold adjustment, or interpretive reframing has been applied. The C1 floor breach was a pre-registered outcome path with a pre-committed verdict. Methodological findings reported in §6 are post-hoc observations that motivated the v1.4 Methodology paper revision but did not affect the substantive verdict on $H_{\text{Regime4\_kitchenware}}$.

**JEL classification.** M31 (primary); L86, L15, D83, M37 (secondary).

**Keywords.** AI Availability; AIAS; LLM-mediated retrieval; brand measurement; Identity Load; recognition memory; recall memory; pre-registration; premium kitchenware.

# References

González Castro, P. U. (2026a). *AI Availability: A Third System of Brand Presence*. SSRN Working Paper 6659000.

González Castro, P. U. (2026b). *Regime 4 Boundary and Discourse-Language Carryforward on the Kitchen-Knives Substrate*. SSRN Working Paper 6791999.

González Castro, P. U. (2026c). *The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification*. SSRN Working Paper 6797679.

González Castro, P. U. (2026d). *The AIAS Presence Measurement Protocol v1.4: Recognition × Recall Decomposition and Multi-Component AI Availability*. SSRN Working Paper (forthcoming, v1.4 Methodology paper).

González Castro, P. U. (2026e). *The AIAS Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy*. SSRN Working Paper 6761698.

González Castro, P. U. (2026f). *The Third System: AI Availability and the Architecture of Brand Growth*. Manuscript under preparation, Routledge Studies in Marketing.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

Sharp, B., and Romaniuk, J. (2021). *How Brands Grow Part 2: Including Emerging Markets, Services, Durables, B2B and Luxury Brands* (Revised Edition). Oxford University Press.

---

*v0.17 Premium Kitchenware program report. Pre-registration: `v0.17-prereg-r1` (commit `3ebe426`). Phase locks: `v0.17-phase-a-locked` (commit `8cdf0cd`), `v0.17-phase-b-locked` (commit `54c83ec`). Submitted to SSRN, May 2026.*
