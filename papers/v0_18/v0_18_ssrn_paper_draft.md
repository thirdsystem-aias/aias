---
title: "Identity-Load Moderator Test and Recognition × Recall Dissociation Generalization on an English-Language Indie Fragrance Substrate"
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
  - \renewcommand{\maketitle}{}
---

\begin{titlepage}
\centering
\vspace*{2cm}

{\fontsize{16}{21.76}\selectfont\bfseries
Identity-Load Moderator Test and Recognition × Recall Dissociation Generalization on an English-Language Indie Fragrance Substrate
\par}

\vspace{1.2em}

{\large\itshape
AIAS™ Presence Measurement Protocol, v0.18 --- Multi-Component Construct Generalizes; Moderator Bounded
\par}

\vfill

{\large Pablo Ulpiano González Castro \par}

\vspace{0.8em}

\textit{School of Visual Arts, MPS Branding Program, New York, NY} \\
\textit{(primary academic affiliation)} \\[0.3em]
\textit{Third System™ (research entity; data archive and methodology venue)}

\vspace{1.2em}

Correspondence: \texttt{pablou@pablou.com} · \texttt{pablou.com} \\
ORCID: \href{https://orcid.org/0009-0003-8968-9990}{0009-0003-8968-9990}

\vfill

{\large May 2026 \par}

\vspace{1cm}
\end{titlepage}

# Abstract

The AIAS™ Presence Measurement Protocol operationalizes AI Availability — the brand-level probability of retrieval, recommendation, or selection by an AI intermediary — as a measurable construct alongside Ehrenberg-Bass Mental Availability and Physical Availability. Protocol v1.4 (SSRN 6799479) extends AI Availability into a multi-component construct (Recognition × Recall) anchored empirically by the Iwachu dissociation in v0.17 (SSRN 6802261). This paper reports v0.18, which tests two pre-registered hypotheses orthogonally: (a) the three-leg joint Identity-Load moderator hypothesis closing the AMBIGUOUS verdict left by the v0.16/v0.17 panel (v0.16 PARTIAL, v0.17 FALSIFIED on panel inadequacy), and (b) the generalization of the Recognition × Recall dissociation from the cross-cultural Japanese-cell substrate to a same-language IL-gradient substrate. The substrate is indie fragrance, sampled across three cells stratified by Identity Load: mass-prestige (medium IL), designer-niche (medium-high IL), and indie/artisan (high IL). Each cell holds 8 brands (worldwide n = 24 pre-floor; C1 floor n ≥ 12). The reference panel is the locked six-slot v0.17 panel. Phase B uses a three-frame query battery (niche / independent / perfumistas).

All three pre-registered hypotheses returned **PARTIAL** verdicts. H_Regime4_indie_fragrance resolved at C3, with C1 panel adequacy and both C2 conditions (within-cell concentration and IL-gradient separation) clearing. The three-leg joint H_IdentityLoad_moderator returned PARTIAL, indicating the moderator operates but with substrate-specific qualifications. H_Recognition_Recall_dissociation_generalization returned DISSOCIATION_PARTIAL: 9 Iwachu-pattern cases identified across 2 of 3 cells, concentrated in the highest-IL Cell B (6 of 8 cell brands, 75%). The Recognition × Recall multi-component construct (Protocol v1.4) generalizes to a same-language substrate, strengthening v1.4's foundational construct claim beyond its original cross-cultural empirical anchor. Cell C's pivot cascade exhausted at the "niche fragrance" Recognition probe (mean C_P ≈ 0.25/6 across the 6-slot panel) — documented as DEVIATIONS Entry 1 and treated as a substantive finding that the IL-gradient operates on Recognition itself, not only on Recall. The pre-registration discipline (commit `183386c`, tag `v0.18-prereg-r1`, refined through r4 at commit `1195cb8`) locks panel, hypotheses, decision rules, and dissociation thresholds ex-ante.

**Keywords:** AI availability; brand availability; Identity Load; Recognition–Recall dissociation; LLM mediation; pre-registration; Spearman bootstrap; indie fragrance; Ehrenberg-Bass; AIAS

**JEL classifications:** M31 (primary); L86; L15; D83; M37

---

# 1. Introduction

The two-system framework of brand availability — Mental Availability and Physical Availability (Sharp, 2010; Romaniuk, 2018) — has organized empirical brand-growth science for three decades. The AIAS™ Presence Measurement Protocol (SSRN 6659000, SSRN 6761698) extends the framework into the AI-mediated commerce environment by introducing **AI Availability** as a third measurable layer: the brand-level probability that a brand is retrieved, recommended, or selected by an AI intermediary in a category-relevant decision context.

Protocol v1.4 (SSRN 6799479) refined the AI Availability construct from a single-dimensional measure into a multi-component decomposition: **Recognition** (whether the AI system recognizes the brand as belonging to the category at all — operationalized as Phase A C_P anchoring) and **Recall** (whether the AI system retrieves the brand when asked to enumerate category members — operationalized as Phase B mention rate). The multi-component construct currently rests on a single empirical anchor: the Iwachu dissociation observed on the v0.17 Japanese-cell substrate (Phase A C_P = 6/6 with Phase B mention rate = 0/18). A single anchor is insufficient ground for a canonical methodology claim. The first generalization test is required.

In parallel, the **Identity-Load moderator hypothesis** — that the AI Availability retrieval signature strengthens monotonically with category Identity Load — remained at AMBIGUOUS through the v0.16/v0.17 cycle. v0.16 (SSRN 6791999) returned PARTIAL on the kitchen-knives substrate; v0.17 (SSRN 6802261) returned FALSIFIED, but with the falsification grounded in panel inadequacy (worldwide n = 10 below C1 floor) rather than in substantive moderator failure. The two legs do not converge to a substantive verdict, and v0.18 is the deciding third leg.

This paper reports v0.18, which is designed to resolve both questions on a single substrate, with three pre-registered hypotheses tested orthogonally: H_Regime4_indie_fragrance (within-phase substantive), H_IdentityLoad_moderator (three-leg joint), and H_Recognition_Recall_dissociation_generalization (methodological).

The substrate is **indie fragrance**, selected on three grounds. First, fragrance is a culturally and personally identity-bearing category — fragrance selection is itself part of what the purchase accomplishes — positioning the substrate at the high-IL end of the consumer-category spectrum, ahead of v0.16 and v0.17. Second, the indie-fragrance category admits a clean three-tier Identity-Load stratification (mass-prestige → designer-niche → indie/artisan) on the consumer-discovery surface. Third, the substrate is entirely English-language-anchored, removing the cross-cultural confound that contaminated v0.17's Japanese cell (Vermicular → Iwachu cascade) and isolating the IL moderator on equal LLM-coverage terms across cells.

The Identity-Load gradient design within v0.18 produces an additional within-phase test of the moderator that neither v0.16 nor v0.17 afforded (both were uniform-IL panels). If H_IdentityLoad_moderator is true, the within-phase Regime 4 signature should strengthen monotonically from Cell C through Cell A to Cell B.

Pre-registration discipline is treated as structurally definitive of the protocol's credibility (Nosek et al., 2018). The v0.18 pre-registration is locked at commit `183386c` with tag `v0.18-prereg-r1` on branch `v0.18-il-gradient` (deposited at osf.io/ec6wh/v18/), with all panel composition, hypothesis specifications, decision-rule thresholds, and verdict matrices fixed ex-ante. The pre-registration was iteratively refined through revisions r1–r4 prior to acquisition. r4 (commit `1195cb8`) numerically locked the C2/C3 thresholds for the v1.4 framework, which v0.17 had not exercised because it FALSIFIED at C1.

---

# 2. Methods

## 2.1 Substrate definition and IL-gradient design

"Indie fragrance" is operationally defined as an IL-gradient panel spanning three tiers of Identity Load on the fragrance consumer-discovery surface, rather than strictly as independently-owned brands. Conglomerate ownership of designer-niche houses (Estée Lauder, LVMH) is treated as a borderline classification and not an exclusion criterion. The panel is entirely English-language-presence anchored; no cross-cultural cells are included.

Three cells are stratified by Identity Load:

- **Cell A — Designer-niche, medium-high IL.** Selection involves curatorial signaling and connoisseur-adjacent discovery within the established prestige-fragrance retail surface.
- **Cell B — Indie/artisan, high IL.** Small-house identity is part of the brand's signal; perfumistas-native lexicon dominates the discovery vocabulary.
- **Cell C — Mass-prestige, medium IL (comparison anchor).** Mainstream designer fragrance with signature-scent role; selection process more separable from product identity.

If the Identity-Load moderator hypothesis holds, the Regime 4 signature should strengthen monotonically C → A → B.

## 2.2 Brand registry and reference panel

The locked registry holds 24 brands (8 per cell, n = 24 worldwide pre-floor; C1 floor n ≥ 12). The pre-floor allows 50% LLM-substrate attrition while still clearing C1.

**Cell A:** Maison Francis Kurkdjian, Le Labo, Diptyque, Frederic Malle, Byredo, Comme des Garçons Parfums, Memo Paris, Etat Libre d'Orange.
**Cell B:** D.S. & Durga, Boy Smells, Heretic Parfum, Ellis Brooklyn, Vyrao, Henry Rose, Phlur, Snif.
**Cell C:** Chanel, Dior, YSL, Tom Ford, Givenchy, Versace, Marc Jacobs, Calvin Klein.

Le Labo (EL ownership), Frederic Malle (EL), and Byredo (LVMH) are borderline-classified — designer-niche brand identity retained under conglomerate ownership — and pre-registered for Phase B retrieval-frame resolution.

The locked six-slot reference panel from v0.16/v0.17 is reused without modification: claude-opus-4-5, claude-sonnet-4-5, gpt-4o, gpt-4o-mini, gemini-2.5-flash, gemini-2.5-flash-lite. No provider model substitutions were required during acquisition.

## 2.3 Phase A: Recognition (C_P)

Phase A operationalizes Recognition per Protocol v1.4. For each registry brand, the v1.4 C_P probe ("Is the brand X commonly recognized as a niche fragrance? Answer yes or no.") is sent to each of the six panel models; the brand's C_P score (range 0..6) is the count of recognition-positive responses across the panel. Per-cell pivot determination follows the cascade rule: the first brand in cascade order achieving C_P = 6/6 becomes the cell pivot, and remaining cell brands are probed for the dissociation analysis.

## 2.4 Phase B: three-frame query battery

Phase B operationalizes Recall. Three category-anchored query frames are sent to each of the six panel models, yielding 18 observations per brand:

- **q1 (niche):** "What are the best niche fragrances? List several with descriptions."
- **q2 (independent):** "Recommend high-quality independent fragrance brands. Name several brands."
- **q3 (perfumistas):** "What fragrances do industry insiders and perfumistas recommend? List several."

For each (frame, model) response, all 24 registry brands are scanned for mention presence under the v1.4 canonical brand-mention detection rules (case-insensitive, accent-stripped, possessive-aware, first-occurrence-wins de-duplication). Rank within enumerated response lists is recorded for Phase D ρ analysis.

## 2.5 Hypotheses and decision rules

Three orthogonal hypotheses are pre-registered (verdict matrices ex-ante; full specification in r4 §4.0 and §5):

- **H_Regime4_indie_fragrance** (within-phase substantive): C1 (n ≥ 12) → C2 within-cell (per-cell top-2 share ≥ 0.50) → C2 IL-gradient (Cell B share − Cell C share ≥ 0.10) → C3 (per-cell Spearman ρ between Phase A C_P and Phase B mention count ≥ 0.50, in ≥ 2 of 3 cells at post-attrition n ≥ 5).
- **H_IdentityLoad_moderator** (three-leg joint, v0.16 × v0.17 × v0.18): joint verdict over the three-leg matrix specified ex-ante.
- **H_Recognition_Recall_dissociation_generalization** (primary co-hypothesis, novel for v0.18): Iwachu-pattern cases (Phase A C_P ≥ 5/6 ∧ Phase B mention rate ≤ 2/18) routed to GENERALIZED / PARTIAL / NARROWED / UNDETERMINED per §5.2. Pooled Recognition–Recall correlation threshold for the NARROWED routing: Spearman ρ ≥ 0.5 ∧ bootstrap 95% CI lower bound > 0.3 (10,000 brand-level resamples, percentile method).

C2 and C3 numerical thresholds were locked in pre-reg r4. They are NOT lifted from v0.16's `score_v16.py` (which operates on the v1.2 framework — AI Presence × Google Trends correlation, |ρ| < 0.35 and partial ρ < 0). v1.2's thresholds and v1.4's thresholds operationalize fundamentally different constructs; v0.18 is the first phase reaching numerical operationalization of v1.4 C2/C3.

---

# 3. Results

## 3.1 Phase A — Recognition (C_P anchoring)

Phase A produced clean Recognition gradients across the three cells. Pivot anchoring outcomes:

- **Cell A — pivot anchored at Maison Francis Kurkdjian** (C_P = 6/6 on first cascade step). Per-brand C_P distribution: 7/8 brands at C_P = 6/6, one (Comme des Garçons Parfums) at C_P = 5/6. Cell mean C_P ≈ 5.88/6 (near-saturation).
- **Cell B — pivot anchored at D.S. & Durga** (C_P = 6/6 on first cascade step). Per-brand C_P distribution: D.S. & Durga 6/6, Boy Smells 5/6, Heretic Parfum 6/6, Ellis Brooklyn 4/6, Vyrao 6/6, Henry Rose 3/6, Phlur 5/6, Snif 5/6. Cell mean C_P ≈ 5.00/6 (strong but varied).
- **Cell C — pivot cascade exhausted**. No brand in the full Cell C cascade (Chanel → Dior → YSL → Tom Ford → Givenchy → Versace → Marc Jacobs → Calvin Klein) achieved C_P = 6/6. Per-brand C_P distribution: 7/8 brands at 0/6, Tom Ford at 2/6. Cell mean C_P ≈ 0.25/6 (near-zero). Documented as DEVIATIONS Entry 1; alternates not invoked because the cascade exhaustion is a substrate-level pattern rather than a brand-level failure (see §5).

The Recognition data show a strong IL-gradient signal at the recognition layer itself: Cell C → Cell A is a near-threshold transition from outside-category (~0/6) to inside-category (~5.88/6), with Cell B at 5.00/6 sitting between Cell A and the threshold. The Cell A > Cell B inversion against strict monotonicity is itself substantive: "niche fragrance" as a lexical anchor most tightly maps to designer-niche houses (Cell A), with American-DTC indie brands (Cell B) occupying an adjacent category sometimes labeled "indie" or "clean" rather than "niche" in perfumistas-vocabulary terms.

## 3.2 Phase B — Recall (three-frame mention rates)

Phase B produced sharply differentiated Recall patterns across the three cells:

- **Cell A:** Distributed mention coverage. Per-brand mention counts (out of 18) ranged from 0 (Memo Paris) to 17 (Le Labo). The five highest-mentioned Cell A brands (Le Labo 17, MFK 16, Diptyque 15, Frederic Malle 12, Byredo 10) account for substantial cumulative coverage; top-2 share = 0.446 (below the C2 within-cell threshold of 0.50, reflecting the distributed pattern across many recognized designer-niche houses).
- **Cell B:** Near-total Recall attrition. Of 8 Cell B brands, 7 received zero mentions across the 18 Phase B observations. Only D.S. & Durga registered mentions, at 2/18. Top-2 share = 1.000 (the second-highest mention count is 0). This is a *degenerate* top-2 share — high concentration arises from sparse Recall rather than from a healthy Pareto distribution.
- **Cell C:** Sparse coverage of select brands despite zero Recognition. Of 8 Cell C brands, 4 received zero mentions. Tom Ford (4 mentions), Chanel (3), Versace (1), and Dior (1) accounted for the cell's Recall coverage. Top-2 share = 0.688.

The Recall data show a second IL-gradient signal, this time operating as **dissociation pattern** rather than as Pareto concentration. Cell B's high-Recognition brands (mean C_P 5.00/6) almost uniformly fail to surface in category-anchored Phase B queries. Cell A's high-Recognition brands surface broadly. Cell C's no-Recognition brands occasionally surface through general fragrance-discourse pathways (Tom Ford's broad cultural footprint, Chanel's signature-scent status) despite failing the niche-fragrance Recognition probe.

![Phase B mention-rate distribution per cell. Box-and-whisker plots show within-cell distribution of brand mention counts across the 3 (query frames) × 6 (reference panel models) = 18 measurement cells. Cell A shows distributed Recall (Le Labo 17/18, MFK 16/18, Diptyque 15/18 lead a broad coverage). Cell B shows near-total Recall attrition (only D.S. & Durga with non-zero mentions, at 2/18). Cell C surfaces sporadically (Tom Ford 4, Chanel 3, Versace and Dior 1 each) despite failing the niche-fragrance Recognition probe — evidence of a parallel cultural-footprint Recall channel.](../../reports/figs/v18/chart_01_mention_rate_distribution.pdf){#fig:mention-rates width=100%}

![Cell attrition from Phase A registered panel to Phase B mention-positive set. Light bars are the registered panel (n = 8 per cell); dark bars are brands with ≥ 1 mention across the 18 Phase B observations. Cell A retains 7/8 (only Memo Paris is mention-zero); Cell B retains 1/8 (D.S. & Durga alone); Cell C retains 4/8 (the four with cultural-footprint discourse channels). The cell-attrition pattern is non-monotonic across IL tiers — the IL-gradient operates as dissociation pattern at the high-IL tier rather than as Pareto concentration.](../../reports/figs/v18/chart_02_cell_attrition.pdf){#fig:cell-attrition width=100%}

## 3.3 Phase D — within-cell ρ (Recognition × Recall)

Spearman rank correlation between Phase A C_P score and Phase B mention count, computed per cell (post-attrition n = 8 for all three cells; the n ≥ 5 minimum is satisfied):

| Cell | n | Top-2 share | Spearman ρ |
|---|---|---|---|
| Cell A (designer-niche) | 8 | 0.446 | 0.247 |
| Cell B (indie/artisan) | 8 | 1.000 | 0.434 |
| Cell C (mass-prestige) | 8 | 0.688 | 0.615 |

The ρ values are diagnostic of three distinct within-cell dynamics. Cell A's ρ = 0.247 reflects the cell's flat Recognition profile (7/8 brands at C_P = 6/6 produces near-uniform rank ties) — rank correlation has minimal signal when Recognition varies negligibly. Cell B's ρ = 0.434 reflects the cell's high-Recognition / sparse-Recall dissociation: brands with C_P = 6/6 (Heretic Parfum, Vyrao) and brands with C_P = 5/6 (Boy Smells, Phlur, Snif) both have zero mentions, while the lone Recall-positive brand (D.S. & Durga, C_P = 6/6, 2 mentions) doesn't carry the rank correlation alone. Cell C's ρ = 0.615 is the highest of the three and reflects the cell's marginal Recognition variance (Tom Ford C_P = 2/6 + 4 mentions, Chanel C_P = 0/6 + 3 mentions) correlating with sub-threshold Recall variance.

## 3.4 Recognition × Recall dissociation case identification

The Iwachu-pattern threshold (Phase A C_P ≥ 5/6 ∧ Phase B mention rate ≤ 2/18) identifies brands exhibiting the Recognition-without-Recall dissociation that v1.4 anchors empirically. v0.18 produces 9 dissociation cases:

**Cell A (3 cases):**

| Brand | C_P | Mentions |
|---|---|---|
| Comme des Garçons Parfums | 5/6 | 2/18 |
| Memo Paris | 6/6 | 0/18 |
| Etat Libre d'Orange | 6/6 | 1/18 |

**Cell B (6 cases):**

| Brand | C_P | Mentions |
|---|---|---|
| D.S. & Durga | 6/6 | 2/18 |
| Boy Smells | 5/6 | 0/18 |
| Heretic Parfum | 6/6 | 0/18 |
| Vyrao | 6/6 | 0/18 |
| Phlur | 5/6 | 0/18 |
| Snif | 5/6 | 0/18 |

**Cell C (0 cases).** By construction: the Iwachu-pattern threshold requires C_P ≥ 5/6, which no Cell C brand achieves (maximum is Tom Ford at 2/6). Cell C contributes zero to the dissociation pool because the asymmetric design of the multi-component construct captures Recognition-without-Recall, not Non-Recognition-with-Non-Recall.

The cell distribution is markedly cell-clustered: 9 cases concentrate in Cells A (3) and B (6), with the Cell B share (6/8 = 75%) dominating. This pattern is itself substantive — dissociation appears most pronounced at the highest-IL tier, consistent with the moderator hypothesis though it does not formally satisfy the cross-cell generalization criterion (≥ 1 case in *every* cell).

![Recognition × Recall dissociation scatter for the v0.18 panel. Phase A C_P score (Recognition, x-axis, 0–6 across the reference panel) versus Phase B mention count (Recall, y-axis, 0–18 across the three-frame query battery). Shaded quadrant: Iwachu-pattern threshold (C_P ≥ 5 and mentions ≤ 2). Black × marks the v0.17 Iwachu reference point (C_P = 6, mentions = 0). v0.18 contributes 9 cases to the shaded quadrant: 3 in Cell A (Comme des Garçons Parfums, Memo Paris, Etat Libre d'Orange) and 6 in Cell B (D.S. & Durga, Boy Smells, Heretic Parfum, Vyrao, Phlur, Snif). Cell C contributes zero by Recognition-floor design — no Cell C brand satisfies C_P ≥ 5/6.](../../reports/figs/v18/chart_03_dissociation_scatter.pdf){#fig:dissociation width=100%}

## 3.5 Verdict resolution

The three pre-registered hypotheses resolved against the locked verdict matrices as follows:

**H_Regime4_indie_fragrance — PARTIAL (resolved at C3).** C1 (worldwide post-attrition n = 24 ≥ 12) clears. C2 within-cell (top-2 share ≥ 0.50 met by Cells B and C) clears. C2 IL-gradient separation (Cell B 1.000 − Cell C 0.688 = 0.3125 ≥ 0.10) clears. C3 (per-cell ρ ≥ 0.50 in ≥ 2 of 3 cells) fails: only Cell C (ρ = 0.615) clears the threshold; Cells A and B do not (Cell A ρ = 0.247, Cell B ρ = 0.434). The verdict routes to PARTIAL per the §4.0 truth table.

**H_IdentityLoad_moderator (three-leg joint, v0.16 × v0.17 × v0.18) — PARTIAL.** The v0.18 leg returns PARTIAL; the joint matrix routes to PARTIAL ("moderator operates but bounded; substrate-specific qualifications") given v0.16 PARTIAL and v0.17 FALSIFIED (on panel inadequacy). The moderator is neither falsified nor cleanly confirmed across the three-substrate history.

**H_Recognition_Recall_dissociation_generalization — DISSOCIATION_PARTIAL.** 9 Iwachu-pattern cases identified across 2 of 3 cells (Cells A and B). The "cell-clustered" cell of the §5.2 matrix routes to DISSOCIATION_PARTIAL: the v1.4 multi-component construct generalizes from the cross-cultural Japanese-cell substrate (v0.17 Iwachu) to a same-language IL-gradient substrate, but the dissociation pool is asymmetrically populated, with Cell C contributing zero by construction.

---

# 4. Discussion

## 4.1 Identity-Load moderator: substantive interpretation

The H_IdentityLoad_moderator joint verdict of PARTIAL reflects bounded moderator operation rather than ambiguous evidence. The IL-gradient signal appears at two layers — Recognition (Phase A) and Recall (Phase B) — but operates differently at each layer.

At the Recognition layer, the gradient is sharp and threshold-like: Cell C (mass-prestige, mean C_P ≈ 0.25/6) is below the category-recognition floor entirely, while Cell A (designer-niche, mean C_P ≈ 5.88/6) and Cell B (indie/artisan, mean C_P ≈ 5.00/6) are both near-saturated. The C → A transition is a step function, not a gradient. The A → B inversion (Cell A slightly higher than Cell B against strict monotonicity) is itself substantive: the lexical anchor "niche fragrance" maps more tightly to designer-niche houses than to American-DTC indie brands, which occupy an adjacent semantic space ("indie", "clean", "artisan") that sometimes overlaps with "niche" and sometimes does not.

At the Recall layer, the gradient takes the form of dissociation pattern rather than monotonic concentration. Cell B's Recognition is high but its Recall is near-zero (top-2 share = 1.000 with the second brand at zero mentions). Cell A's Recognition is high and its Recall is broadly distributed (top-2 share = 0.446, well below the C2 within-cell threshold of 0.50). Cell C's Recognition is near-zero but some brands surface in general fragrance discourse despite failing the niche-fragrance probe.

The C3 failure (only Cell C clears ρ ≥ 0.50) reflects the consequences of these layer-specific dynamics. Cell A's flat Recognition profile (7/8 brands tied at C_P = 6/6) makes rank correlation degenerate; the rank distinction collapses. Cell B's near-uniform low Recall similarly degenerates the rank structure on the y-axis. Only Cell C exhibits sufficient variance in both dimensions to produce a meaningful ρ — and the ρ there is driven by Tom Ford's marginal Recognition advantage (C_P = 2 vs. 0 for the rest of the cell) correlating with its higher mention count.

The substantive theory implication is that the v1.4 multi-component construct exposes mechanism complexity the v1.2 framework could not. The IL-gradient is real but operates through layer-specific channels: as a Recognition-floor effect at the C → A boundary, and as a dissociation pattern at the A → B end. Future work (v0.19+) is positioned to probe whether substrates with greater within-cell Recognition variance produce cleaner C3 verdicts.

## 4.2 Recognition × Recall dissociation: methodological interpretation

The DISSOCIATION_PARTIAL verdict for the generalization hypothesis is the methodological headline finding of v0.18 and the primary contribution to AIAS™ 1.0's canonical methodology layer.

Before v0.18, the v1.4 multi-component construct rested on a single empirical anchor: the Iwachu case from v0.17 (Phase A C_P = 6/6, Phase B mention rate = 0/18) on a Japanese-cell substrate. A single anchor is insufficient ground for a canonical construct claim. The cross-cultural framing of the Iwachu substrate left open the possibility that the dissociation pattern was a Western-language LLM training-data bias artifact rather than a substantive mechanism of AI-mediated retrieval.

v0.18 identifies 9 Iwachu-pattern cases on a same-language English substrate, across 2 of 3 cells. The pattern generalizes — it is not specific to cross-cultural substrates. The v1.4 construct claim is strengthened. The DISSOCIATION_PARTIAL routing (rather than DISSOCIATION_GENERALIZED) reflects the cell-clustering: Cell C contributes zero by construction, because its near-zero Recognition baseline precludes the Iwachu-pattern threshold. This is the asymmetric design of the construct — it captures Recognition-without-Recall, not Non-Recognition-with-Non-Recall — and the cell-clustering pattern is therefore an expected consequence of the IL-gradient design rather than a weakness of the methodology.

The substrate-specific concentration of cases in Cell B (75% of cell brands) is itself an empirical finding worth foregrounding: dissociation appears most pronounced at the highest-IL tier of a single substrate. This pattern, if it replicates in v0.19+, suggests that Identity Load is a moderator of dissociation prevalence, not only of mention-rate concentration. The construct gains an additional layer of theoretical structure: AI mediation produces dissociation patterns that scale with category Identity Load.

For AIAS 1.0, the v0.18 result moves the multi-component construct from "anchored by one cross-cultural case" to "anchored by ten cases across two substrate families, with a substantive IL-pattern in the second substrate." This is the empirical strengthening v1.4 requires before the construct can ship as canonical.

## 4.3 Cell C internal variance — sensitivity finding

The pre-registered descriptive sensitivity for Cell C internal variance (§1.2 note) is partially realized in v0.18. Tom Ford's marginal Recognition (C_P = 2/6 vs. zero for the rest of Cell C) and elevated Recall (4 mentions vs. 0-3 for the rest of the cell) suggest a sub-threshold Recognition variance operating within the mass-prestige tier. Chanel (C_P = 0/6, 3 mentions) and Dior (C_P = 0/6, 1 mention) similarly surface in general fragrance discourse despite failing the niche-fragrance Recognition probe.

This pattern suggests that the "niche fragrance" anchor does not perfectly partition the IL-gradient — some mass-prestige brands accrue Recall through cultural-footprint channels independent of the category-anchored Recognition probe. The C2 IL-gradient separation guard (Cell B 1.000 − Cell C 0.688 = 0.3125) clears the 0.10 floor cleanly, so the substantive C2 condition is satisfied. But the magnitude of the separation is inflated by Cell B's degenerate top-2 share (1.000 from D.S. & Durga alone) rather than by genuine Cell B concentration. Future phases with finer IL stratification within Cell C — separating icon-tier (Chanel, Dior) from mainstream-tier (Marc Jacobs, Calvin Klein) — would clarify whether the cultural-footprint Recall channel operates uniformly across mass-prestige or stratifies further.

## 4.4 Limits and reservations

Four limits qualify the v0.18 verdicts:

**Single-substrate constraint on the multi-component construct claim.** The DISSOCIATION_PARTIAL verdict strengthens v1.4's construct claim from one cross-cultural anchor to two substrate families. It does not establish the construct as canonical across the consumer-category spectrum. v0.19+ should probe substrates with different IL profiles — finer gradients within high-IL tiers; categories with shifted Recognition surfaces; non-fragrance substrates where the category vocabulary is differently structured.

**LLM panel temporal validity.** The six-slot reference panel (claude-opus-4-5, claude-sonnet-4-5, gpt-4o, gpt-4o-mini, gemini-2.5-flash, gemini-2.5-flash-lite) reflects model versions in market as of mid-2026. Provider model substitutions are expected over future-phase horizons and are documented in the DEVIATIONS protocol when they occur. The v0.18 dissociation cases should be interpreted as the pattern observed against the locked panel at acquisition time, not as a permanent property of the substrate.

**C2 IL-gradient guard's degenerate case for Cell B.** Cell B's top-2 share = 1.000 emerges from sparse Recall (D.S. & Durga alone, with 2 mentions) rather than from a healthy Pareto distribution. The IL-gradient separation guard clears against a near-empty Cell B baseline, which is a documented degenerate case (DEVIATIONS Entry 1, §"Downstream implications"). The substantive interpretation rests on the Recognition × Recall dissociation pattern in §3.4, not on the C2 mention concentration metric alone.

**C3 ranking coherence as a within-cell variance test.** Phase D ρ requires within-cell variance in both Recognition and Recall to produce meaningful rank correlation. Cell A's flat Recognition and Cell B's flat Recall both undermine within-cell ρ informativeness. Future Phase D operationalization may benefit from supplementary measures that do not require variance in both dimensions simultaneously — for example, comparing pooled within-cell vs. across-cell rank correlations.

---

# 5. DEVIATIONS

The DEVIATIONS protocol carries forward from v0.16 / v0.17. One entry is opened in v0.18 prior to Phase B acquisition.

**Entry 1 — Cell C pivot cascade exhausted at the "niche fragrance" Recognition probe** (2026-05-20). The Phase A C_P probe template anchored to "niche fragrance" produced near-zero Recognition across all eight Cell C brands (7/8 at C_P = 0/6; Tom Ford at C_P = 2/6). No brand achieved C_P = 6/6; the pivot cascade exhausted. The result is treated as a substantive empirical finding rather than a panel construction error: the IL-gradient operates on Recognition itself, consistent with H_IdentityLoad_moderator. Cell C alternates (Hugo Boss, Lancôme, Carolina Herrera, Paco Rabanne, Burberry) are NOT invoked because they share Cell C's mass-prestige IL tier and would hit the same Recognition-anchor mismatch. The pre-registered panel of 24 brands is unchanged. Cell C Phase A data feeds §3 sensitivities and the §2.3 dissociation analysis (Cell C contributing zero cases by construction). Full entry deposited at `osf/v18/DEVIATIONS.md`. Lock state: pre-reg tag `v0.18-prereg-r1` (refined through r4 at commit `1195cb8`) unchanged.

No additional deviations were opened during Phase A or Phase B acquisition.

---

# 6. Conclusion

The v0.18 acquisition produced three PARTIAL verdicts that are individually informative and jointly significant for the AIAS™ Presence Measurement Protocol's trajectory toward AIAS™ 1.0.

**For the substantive theory.** The H_IdentityLoad_moderator three-leg joint verdict of PARTIAL — across v0.16 (PARTIAL on kitchen knives), v0.17 (FALSIFIED on premium kitchenware, with the falsification grounded in panel inadequacy), and v0.18 (PARTIAL on the IL-gradient indie fragrance substrate) — indicates that Identity Load is a real moderator of AI-mediated retrieval, with operation bounded by substrate-specific mechanisms. The v0.18 substrate exposes that the moderator acts through layer-specific channels: as a Recognition-floor effect at the medium-IL/medium-high-IL boundary, and as a dissociation pattern at the high-IL tier. The moderator is not a single-mechanism construct; it operates through multiple coordinated channels that v1.2's framework did not surface.

**For the canonical methodology.** The H_Recognition_Recall_dissociation_generalization verdict of DISSOCIATION_PARTIAL provides the v1.4 multi-component construct with its first generalization beyond the cross-cultural Iwachu anchor. Nine same-language Iwachu-pattern cases across two cells (with the highest-IL cell contributing six of the nine) demonstrate that the dissociation captures a real mechanism, not a Western-language training-data bias artifact. The construct is strengthened. For AIAS™ 1.0, this is the empirical anchor the methodology layer requires to ship multi-component Recognition × Recall as canonical.

**For v0.19 and beyond.** The PARTIAL verdicts point at productive next directions. The C3 failure (Cell A's flat Recognition, Cell B's flat Recall) suggests substrates with greater within-cell variance in both dimensions. The dissociation cell-clustering in Cell B (75%) invites testing whether the IL × dissociation relationship replicates on a substrate with finer IL stratification within the high-IL tier. The Cell C internal variance finding (Tom Ford / Chanel sub-threshold Recall channels) suggests v0.19 could profitably stratify mass-prestige into icon-tier and mainstream-tier sub-cells. Each direction is preregisterable; each leaves the v0.18 results unchanged.

The pre-registration discipline applied across r1–r4 — locking panel, hypotheses, thresholds, and verdict matrices ex-ante before any acquisition; documenting Cell C's cascade exhaustion as a substantive finding rather than retroactively substituting alternates; carrying the C2/C3 numerical specification gap from v0.17 forward to v0.18 as its proper locking moment — is itself the protocol-level commitment that distinguishes the AIAS™ program from looser AI-visibility tooling. The verdicts are PARTIAL because the empirical reality is partial. The construct, the moderator, and the substrate together carry more structure than any single phase can resolve.

---

# References

Binet, L., & Field, P. (2013). *The Long and the Short of It: Balancing Short and Long-Term Marketing Strategies*. Institute of Practitioners in Advertising.

González Castro, P. U. (2026a). AI Availability — A Third System in Brand Availability Theory. *SSRN Working Paper*. https://ssrn.com/abstract=6659000

González Castro, P. U. (2026b). The AIAS Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy. *SSRN Working Paper*. https://ssrn.com/abstract=6761698

González Castro, P. U. (2026c). The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification (v1.3). *SSRN Working Paper*. https://ssrn.com/abstract=6797679

González Castro, P. U. (2026d). The AIAS Presence Measurement Protocol: Recognition × Recall Decomposition and Multi-Component AI Availability (v1.4). *SSRN Working Paper*. https://ssrn.com/abstract=6799479

González Castro, P. U. (2026e). Regime 4 Boundary and Discourse-Language Carryforward on the Kitchen-Knives Substrate (v0.16). *SSRN Working Paper*. https://ssrn.com/abstract=6791999

González Castro, P. U. (2026f). Panel Inadequacy and Recognition × Recall Dissociation on the Premium Kitchenware Substrate (v0.17). *SSRN Working Paper*. https://ssrn.com/abstract=6802261

Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The Preregistration Revolution. *Proceedings of the National Academy of Sciences*, 115(11), 2600–2606.

Romaniuk, J. (2018). *Building Distinctive Brand Assets*. Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

Sharp, B., & Romaniuk, J. (2021). *How Brands Grow Part 2: Including Emerging Markets, Services and Durables, New Categories and Brand Purpose* (revised edition). Oxford University Press.

---

# Declarations

**Declaration of interest.** The author is employed by Samsung Electronics America (Director, Corporate Brand Creative and Governance). The AIAS™ Presence Measurement Protocol and the work reported here are the author's independent academic research, conducted outside the scope of employment, in the author's role as faculty at the School of Visual Arts MPS Branding Program and founder of Third System™. Samsung had no role in the design, execution, analysis, or interpretation of this work.

**Funder.** Self-funded.

**Ethics.** Not applicable; no human subjects. The research uses publicly accessible LLM APIs queried with non-personal, category-anchored prompts.

**Data and code availability.** All pre-registration artifacts, acquisition data, scoring code, and verdict outputs are deposited under Open Science Framework project ec6wh at osf.io/ec6wh/v18/. The pre-registration is locked at commit `183386c` on git tag `v0.18-prereg-r1`, branch `v0.18-il-gradient`, with full revision history (r1 → r2 → r3 → r4) preserved in Appendix A of the pre-registration artifact. C2/C3 numerical thresholds locked at commit `1195cb8` (pre-reg r4) per §2.5 above.

**Trademark notice.** AIAS™ and Third System™ are trademarks of the research program.

<!-- End v0.18 SSRN paper draft, post-acquisition state -->
