---
title: "AI Availability as a Third Measurable Layer of Brand Availability"
subtitle: "Five-Substrate Empirical Anchoring of the AIAS Presence Measurement Protocol"
author: >-
  Pablo Ulpiano González Castro \\
  \textit{School of Visual Arts, MPS Branding Program, New York, NY} \\
  \textit{(primary academic affiliation)} \\
  \textit{Third System (research entity; data archive and methodology venue)} \\[0.4em]
  Correspondence: \texttt{pablou@pablou.com} · \texttt{pablou.com} \\
  ORCID: \href{https://orcid.org/0009-0003-8968-9990}{0009-0003-8968-9990}
date: "May 2026"
mainfont: Carlito
fontsize: 11pt
linkcolor: black
urlcolor: black
geometry:
  - letterpaper
  - margin=1in
header-includes:
  - \usepackage{setspace}
  - \usepackage{amssymb}
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
\setstretch{1.0}
\setlength{\parskip}{0pt}
\vspace*{2cm}
\begin{center}
{\fontsize{16}{21.76}\selectfont\bfseries AI Availability as a Third Measurable Layer of Brand Availability\par}
\vspace{10.36pt}
{\large Five-Substrate Empirical Anchoring of the AIAS Presence Measurement Protocol\par}
\vspace{2cm}
{\large Pablo Ulpiano González Castro\par}
\vspace{0.4em}
\textit{School of Visual Arts, MPS Branding Program, New York, NY}\\
\textit{(primary academic affiliation)}\\
\textit{Third System (research entity; data archive and methodology venue)}\\
\vspace{0.4em}
Correspondence: \texttt{pablou@pablou.com} · \texttt{pablou.com}\\
ORCID: \href{https://orcid.org/0009-0003-8968-9990}{0009-0003-8968-9990}\\
\vspace{2cm}
May 2026
\end{center}
\end{titlepage}

# Abstract

The AIAS Presence Measurement Protocol operationalizes AI Availability — the probability that an AI intermediary retrieves or recommends a brand in a category-anchored decision context — as a third measurable layer of brand availability alongside Ehrenberg-Bass Mental Availability and Physical Availability. A pre-registered measurement program across five substrate families (kitchenware, fragrance, headphones, skincare, cosmetics) anchors the construct under a locked six-LLM reference panel and versioned methodology. Headline findings: Type 2 dissociation cleared the EMERGED threshold; the Identity-Load moderator reached CONFIRMED; Phantom Brand Persistence was operationalized and confirmed. The construct claims measurability under replication discipline, not construct validity.

# Management Slant

- AI Availability is measurable now: a pre-registered protocol anchored across five consumer-product categories tracks brand position inside AI-mediated retrieval with falsifiable, replicable verdicts.
- Brand Recall in AI retrieval splits into two independently manageable channels — canonical authority (editorial, expert, clinical endorsement) and cultural footprint (social media, celebrity, community discourse).
- Identity Load predicts which channel dominates: high-identity brands lead culturally; heritage brands lead canonically. The gradient locates the intervention pathway.
- Off-panel brands persist in AI retrieval with channel signatures that track Identity Load — brand presence exceeds any single panel's scope.
- Brand managers can audit a brand's channel position against its substrate's IL gradient and target the underperforming channel directly.

# 1. Introduction

Large language models now mediate how consumers discover brands within categories, introducing a new structural layer to brand availability. When a consumer's decision surface is an AI-mediated conversation, the brand is retrieved by an intermediary whose representational state is a function of training data, retrieval policy, and prompt context — not from the consumer's own associative memory or the brand's physical distribution footprint. The discovery surface has acquired a third layer alongside the two the Ehrenberg-Bass tradition has formalized: Mental Availability, the probability that a brand is retrieved from category-anchored memory at decision time (Sharp, 2010; Romaniuk, 2018), and Physical Availability, the probability that a brand is accessible through distribution channels (Sharp and Romaniuk, 2021).

This paper presents the foundational claim that AI Availability — the brand-level probability that an AI intermediary retrieves, recommends, or selects a brand in a category-anchored decision context — is a third measurable layer of brand availability, and presents the AIAS Presence Measurement Protocol as the operational instrument for measuring it.

The claim is bounded. AIAS 1.0 names the Presence component of a multi-component AIAS construct; the full composite is a multi-year research program (González Castro, 2026a), and only Presence is currently operationalized. The claim is a measurability claim, not a construct-validity claim: the synthesis establishes that AI Availability can be measured under a falsifiable pre-registered protocol with cross-substrate replication, leaving predictive validity against behavioral outcomes, convergent validity across panel constructions, and discriminant validity against Mental and Physical Availability as future work. The synthesis is silent on the consumer-behavior correlate of AI Availability; that correlation is not yet established and is held explicitly out of scope.

The empirical anchor base spans five substrate families acquired between v0.16 and v0.21: kitchenware, indie fragrance, audiophile headphones, skincare, and cosmetics. Each phase is a pre-registered measurement event against a panel of six LLMs held fixed across the program. The cumulative six-phase corpus is consolidated under Protocol v1.6 (González Castro, 2026f), which locks the methodology with three increments detailed in §3. The construct claim is developed in seven layers in §5, spanning the construct's measurability (L1), its decomposition into Recognition and two-channel Recall (L2–L3), the dissociation framework and Identity-Load moderator (L4–L5), Phantom Brand Persistence as an empirical regularity (L6), and the scope discipline that names Presence without over-claiming the full composite (L7).

The remainder of the paper is structured as follows. §2 positions AI Availability against the Ehrenberg-Bass canon. §3 consolidates the methodology chain. §4 presents the empirical evidence across five substrate families. §5 develops the construct claim. §6 discusses implications and limitations. §7 outlines the future-research program.

# 2. Theoretical positioning

The Ehrenberg-Bass tradition formalizes brand availability as two structurally distinct probabilities. Mental Availability is the probability that a brand is retrieved from memory in a category-anchored decision context, operationalized through category entry points, distinctive brand assets, and memory-network strength (Sharp, 2010; Romaniuk, 2018). Physical Availability is the probability that a brand is encounterable at decision time through the distribution footprint connecting brand to purchase environment (Sharp and Romaniuk, 2021). The two are treated as orthogonal: a brand can be mentally available without being physically available, or physically available without sufficient memory anchoring to be considered.

AI-mediated retrieval breaks the two-layer framing. When the consumer's decision surface is an LLM-mediated conversation, the brand is neither retrieved from the consumer's own memory nor encountered through distribution. It is retrieved by an intermediary whose representational state is a function of training data, retrieval policy, and prompt context — none of which is reducible to consumer memory or to physical-distribution presence. The intermediary's selection of a brand for a category-anchored response is a third event in the availability chain, located between Mental Availability (which it does not require) and Physical Availability (which it does not require either). The construct that captures this third event is AI Availability.

The Tri-System Brand Growth framework (González Castro, 2026a) positions AI Availability as the third system of brand presence and provides the architectural context for the present synthesis. AIAS 1.0 operationalizes the first of six measurable dimensions specified by the framework — Presence, the brand-level probability that an AI intermediary retrieves a brand at all in a category-anchored context. The remaining five dimensions ship under a successor program; their specification is reserved and not load-bearing for the present construct claim.

The synthesis claims measurability under a falsifiable protocol, not construct validity. Construct validity — predictive validity against behavioral outcomes, convergent validity across panel constructions, and discriminant validity against Mental and Physical Availability — is the program's Phase 3 work. The present paper establishes that AI Availability behaves as a measurable property of brand-substrate-intermediary triples under pre-registration discipline; whether the measurement predicts downstream consumer behavior is a separate empirical question. Second, the synthesis is silent on the consumer-behavior correlate of AI Availability. The correlation is plausible on theoretical grounds and is implied by the Ehrenberg-Bass logic that availability constructs are load-bearing for category buying — but the present program has not measured it, and over-claim on this point would compromise the program's standing on the measurability claim that is established.

# 3. Methodology

The measurement procedure is consistent across all six phases. The reference panel is a six-slot LLM panel locked at v0.17 and held constant across the program: Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o-mini, Gemini 2.5 Flash, and Gemini 2.5 Flash Lite (González Castro, 2026h). Holding the panel fixed is the program's cross-phase comparability discipline; verdicts are properties of brand × substrate × panel triples evaluated under the same intermediaries each time.

Phase A is the Recognition layer. For each brand × model pair, the model is prompted with a category-membership probe (template locked at the v1.4 specification); the per-brand Recognition score C_P is the count of "yes" responses across the six panel models, range 0–6 (González Castro, 2026d).

Phase B is the Recall layer. Each panel model receives a six-frame open-ended query battery against the substrate's category. The v1.5 methodology introduced the two-channel decomposition: three canonical-authority frames (best, recommended, highest-quality) anchor R_cat (max 18); three cultural-footprint frames (popular, celebrity, viral/cult) anchor R_cult (max 18) (González Castro, 2026e). Mention detection follows the v1.4 canonical-detection rules (case-insensitive, accent-stripped, word-boundary anchored).

The dissociation taxonomy organizes the Recognition × Recall space into three named patterns: Iwachu (high Recognition with sparse canonical Recall: C_P ≥ 5 ∧ R_cat ≤ 2), Type 1 (canonical-preferred: R_cat ≥ 5 ∧ R_cult ≤ 2), and Type 2 (cultural-preferred: R_cat ≤ 2 ∧ R_cult ≥ 5).

Protocol v1.6 (González Castro, 2026f) closes the methodology layer with three increments: first, a substrate-level Recognition pre-screen classifies substrates with uniform Recognition saturation (all brands scoring C_P = 6/6 across all cells) as REGIME-4-UNAVAILABLE-AT-RECOGNITION — a verdict state distinct from FALSIFIED that preserves evidentiary value by distinguishing saturated substrates from substrates that fail on substantive grounds. Second, H_IdentityLoad_Direct introduces an independent per-cell moderator test: δ = mean(R_cult) − mean(R_cat) is computed per cell with a 95% percentile bootstrap confidence interval (n = 10,000), and the verdict matrix requires monotonic ordering of δ across the IL gradient (Cell A δ < Cell C δ < Cell B δ, reflecting medium → low → high Identity Load) for CONFIRMED. Third, Phantom Brand Persistence lifts off-panel brand mentions from a descriptive observation to a measured component, scoring R_phantom against an exogenously constructed reference vocabulary — the union of the substrate registry, a pre-registered market-share list, and prior-phase emergents cross-validated against that list — with a persistence threshold of K = 6.

The retrospective-scoring boundary is locked at v1.6: v0.20 and v0.21 score under v1.6 where each increment is supported; v0.16–v0.19 stand on their published v1.4-era verdicts. Every phase enters the program under pre-registration discipline (Nosek et al., 2018), with panel, registry, hypotheses, and decision rules locked ex-ante at a git tag. All artifacts are deposited under Open Science Framework project ec6wh.

# 4. Results: Empirical evidence across five substrate families

The five-substrate anchor base spans kitchenware (v0.16 and v0.17), indie fragrance (v0.18), audiophile headphones (v0.19), skincare (v0.20), and cosmetics (v0.21). Each family is presented below with the same shape: substrate definition and cell construction, headline findings under the methodology version prevailing at acquisition, v1.6 retrospective classification, and the construct contribution carried into §5. The retrospective-scoring boundary stated in §3 applies throughout: v0.20 and v0.21 score under v1.6 where each increment supports it; v0.16–v0.19 stand on their published v1.4-era verdicts, with v1.6 Increment 1 narrative classification added. Two cross-phase synthesis-layer contributions — out-of-cell Type 2 cases recovered by all-cell algorithmic application of the dissociation framework — are flagged at their occurrence in §4.4 and §4.5.

## 4.1 Kitchenware (v0.16 + v0.17)

The kitchenware family anchors the program in two pre-registered phases against substrates organized by heritage tier (Cell A), Japanese-cult tier (Cell B), and mass-market tier (Cell C). v0.16 sampled kitchen knives (González Castro, 2026g); v0.17 extended the substrate to broader premium kitchenware (González Castro, 2026h). The two phases carry the program's earliest methodology lineage — pre-v1.4 single-channel Recall scoring — and together establish the constructs that subsequent phases refine.

v0.17 surfaced the program's first named dissociation case. Iwachu, a Japanese cast-iron cookware brand from the v0.17 Cell B panel, scored at the high end of the Recognition layer (C_P ≥ 5 across the panel) while returning sparse canonical Recall — the pattern subsequently formalized as the Iwachu dissociation type: high Recognition with low canonical Recall (C_P ≥ 5 ∧ R_cat ≤ 2). The dissociation is now established as a cross-substrate empirical regularity: Iwachu-type cases appear in all five substrate families, with multi-cell distribution in three of them (kitchenware, indie fragrance, and cosmetics).

v0.16 produced the original Regime 4 boundary case — the substrate condition under which the IL-gradient moderator becomes evaluable — and the four-regime taxonomy that organized this condition was formalized in v1.2 (González Castro, 2026b). The v0.16 H_IdentityLoad_moderator leg returned PARTIAL, with the three-cell IL-gradient signature visible in the v1.4 single-channel data but not strong enough to resolve to CONFIRMED. v0.17's H_Regime4 returned FALSIFIED-on-panel-inadequacy: the Recognition layer for the v0.17 panel was insufficiently discriminating, and the verdict resolved at the panel-adequacy boundary. The panel-inadequacy condition became a methodology object that v1.3 developed into the Phase A pivot-validation specification (González Castro, 2026c).

Under v1.6 retrospective scoring, both kitchenware phases classify as differential by Increment 1 — each carries within-cell C_P variance sufficient to reject the uniform-saturation rule. Increments 2 and 3 do not apply: R_cult is a v1.5 prospective increment unavailable for these phases. The kitchenware family contributes the Iwachu dissociation pattern (the empirical motivation for the v1.4 Recognition × Recall decomposition), the original Regime 4 boundary definition, and the panel-inadequacy methodology object. These carry into §5's claim layers L2 (multi-component construct) and L4 (dissociation quadrants).

## 4.2 Indie fragrance (v0.18)

The indie fragrance substrate (González Castro, 2026i) was the program's first English-language extension of the dissociation framework outside the kitchenware family. The panel was constructed across heritage / niche perfumery (Cell A), perfumista-cult / DTC fragrance (Cell B), and mass-market fragrance (Cell C), with the IL-gradient design carrying forward from the kitchenware phases. v0.18 ran under v1.4 single-channel Recall scoring and produced the program's first multi-cell Iwachu generalization: the high-Recognition / low-canonical-Recall pattern surfaced in more than one cell, extending the construct from the Japanese-language anchor to an English-language discourse environment and establishing that the dissociation is not specific to a single substrate family or language.

The Identity-Load moderator concept was first articulated as a coherent cross-phase hypothesis in v0.18, building on the IL-gradient signatures visible in v0.16 and v0.17. The v0.18 single-channel Recall data carried a clear cell-structured asymmetry — high-IL Cell B brands surfaced in the panel's Recall responses at higher relative frequencies than brands in the medium-IL Cell A or low-IL Cell C — that the v1.4 single-channel framework could detect without decomposing into its canonical and cultural components. This asymmetry signal was the methodological motivation for the v1.5 two-channel Recall decomposition (González Castro, 2026e): if Recall behaves differently in canonical-authority frames than in cultural-footprint frames for high-IL cells, then a single-channel scoring conflates two empirically separable pathways. The v0.18 H_Regime4 returned PARTIAL; the H_IdentityLoad_moderator joint, evaluated over v0.16 × v0.17 × v0.18, returned PARTIAL.

Under v1.6, v0.18 classifies as differential by Increment 1. Increments 2 and 3 do not apply. The indie fragrance phase contributes the substrate-family generalization argument (Iwachu beyond the Japanese-language anchor), the first IL-gradient signature articulated as a moderator framework, and the methodology bridge from v1.4 single-channel to v1.5 two-channel Recall.

## 4.3 Audiophile headphones (v0.19)

The audiophile headphones substrate (González Castro, 2026j) departs from the three-cell IL-gradient design in a structurally informative way. The substrate's consumer-discovery surface imposes high cultural footprint on every category-member brand from entry tier to heritage tier — audiophile forums and community-canonization rituals turn specific models into cult-tier reference points regardless of market position. A standard three-cell IL-gradient design fits poorly: the high-IL Cell B position is not available because heritage brands themselves carry cult-tier cultural footprint. The v0.19 panel used a two-cell Heritage / Boutique structure with uniform Identity Load by construction — a substrate condition the IL-gradient framework cannot test against, but one that is empirically informative about the framework's domain limits. v0.19 was excluded from the H_IdentityLoad_moderator joint with explicit pre-registered rationale.

v0.19 ran under the v1.4.x protocol with the two-cell design and produced a Cell B saturation-prone Recognition distribution and a C2 FAILED → UNDETERMINED Regime 4 verdict under the v1.5 backport scoring. The Cell B modal share reached 0.875 — high but not the singleton 1.000 that triggers uniform-saturation classification under v1.6 Increment 1. The UNDETERMINED verdict is substantively informative: a substrate that does not satisfy the within-cell adequacy condition cannot be evaluated for Regime 4, but the unevaluable status is methodologically distinct from a substrate that fails the condition.

Under v1.6, v0.19 classifies as mixed by Increment 1 — Cell B's high modal share approaches but does not satisfy the uniform-saturation rule, and the Heritage cell carries enough variance to keep the substrate on the differential side. Increments 2 and 3 do not apply. The audiophile phase contributes substrate-shape information: uniform-IL as a substrate configuration the IL-gradient framework cannot test against, and the empirical reference point for v1.6 Increment 1's differential / mixed / uniform-saturation distinction. v0.19 is the program's nearest miss on the uniform-saturation rule; v0.21's cosmetics case (§4.5) is the rule's first measured trigger, and the contrast between the two substrates' Phase A distributions is the empirical content of the rule's discrimination value.

## 4.4 Skincare (v0.20)

The skincare substrate (González Castro, 2026k) was the program's first prospective phase under v1.5's full sequence — multi-statistic C2, two-channel Recall, and the v1.4 dissociation framework operating jointly. The panel was constructed across heritage / clinical / dermatologist-anchored skincare (Cell A), celebrity-DTC skincare (Cell B), and mass / drugstore skincare (Cell C), with the IL-gradient design carrying forward. v0.20 produced the program's first two-channel acquisition and the first prospective application of the v1.5 C2 multi-statistic adequacy rule.

H_Type2_emergence returned PARTIAL: Cell B Type 2 count was 2 (Rhode and Augustinus Bader), below the pre-registered EMERGED threshold of 3 but consistent with the IL-gradient prediction that high-IL cells should produce Type 2 cases. H_IdentityLoad_moderator returned NARROWED on the five-leg joint, with the within-phase IL signature carrying directionally with prediction but the Cell A canonical pole shifting from prestige to mass — clinical / heritage skincare brands such as CeraVe and La Roche-Posay concentrate in canonical-channel Recall through dermatologist-recommended and clinical-result-anchored discourse rather than editorial-prestige curation, and the substrate's IL-gradient signal accordingly lives in the Cell B versus Cell C contrast rather than the Cell A versus Cell B contrast.

Under v1.6 retrospective scoring (González Castro, 2026f), v0.20 classifies as differential by Increment 1 (distinct C_P = 2, 3, 1 across cells). Increment 2 returns PARTIAL on H_IdentityLoad_Direct: Cell B δ = +3.75 with 95% bootstrap CI [+2.25, +5.25] excludes zero in the IL-predicted direction; Cell A δ = +0.75 with CI [−0.25, +2.12] is against prediction with CI overlapping zero; Cell C δ = −2.50 with CI [−5.25, +0.38] breaks the monotonic-gradient check. Increment 3 is out of v1.6 retrospective scope.

A cross-phase synthesis-layer contribution surfaces here. The all-cell algorithmic dissociation framework — the same R_cat ≤ 2 ∧ R_cult ≥ 5 rule that v0.20's verdict matrix correctly anchored to Cell B — recovers a Type 2 case the verdict matrix did not surface: La Mer (Cell A — Prestige; C_P = 6, R_cat = 2, R_cult = 7). La Mer's Cell A position places her outside the Cell-B-anchored evidence base, which is why the published PARTIAL verdict correctly did not include her. Read across the cross-phase view, La Mer is the first algorithmic out-of-cell Type 2 case in the program. The v0.20 published verdict stands as the authoritative within-phase result; the synthesis adds the cross-phase perspective alongside it.

![H_IdentityLoad_Direct per-cell δ = mean(R_cult) − mean(R_cat) with 95% bootstrap CIs. v0.20 PARTIAL (skincare; Cell B vs. Cell C signal) → v0.21 CONFIRMED (cosmetics; monotonic A < C < B).](../../reports/figs/aias_1_0/chart_05_il_direct_forest.pdf){#fig:il-direct width=100%}

## 4.5 Cosmetics (v0.21)

The cosmetics substrate (González Castro, 2026l) is the program's strongest empirical anchor. The panel was constructed across prestige (Cell A — medium IL: MAC Cosmetics, NARS, Bobbi Brown, and five others), celebrity-DTC / cult (Cell B — high IL: Rare Beauty, Fenty Beauty, Haus Labs, Pat McGrath Labs, Charlotte Tilbury, Huda Beauty, Kylie Cosmetics, Anastasia Beverly Hills), and drugstore / mass (Cell C — low IL: Maybelline, L'Oréal Paris, CoverGirl, Revlon, NYX Professional Makeup, e.l.f. Cosmetics, Wet n Wild, Milani Cosmetics), 24 brands total. v0.21 was the first phase prospectively pre-registered to test Type 2 emergence in a high-IL substrate cell against an EMERGED threshold of 3 Cell B cases.

v0.21's headline findings cleared three thresholds simultaneously. H_Type2_emergence returned EMERGED with three Cell B cases: Rare Beauty (R_cat = 1, R_cult = 17 — the program's textbook Recognition × Recall dissociation case with C_P = 6 in the Recognition layer), Huda Beauty (R_cat = 0, R_cult = 11), and Kylie Cosmetics (R_cat = 0, R_cult = 5). The Rare Beauty profile anchors the two-channel construct at its sharpest: a brand fully recognized by every panel intermediary (C_P = 6/6), virtually absent from canonical-authority Recall (best, recommended, highest-quality frames), and dominant in cultural-footprint Recall (popular, celebrity, viral/cult frames). H_Dissociation_substrate_generalization returned GENERALIZED with 13 Iwachu cases distributed across all three cells.

H_Regime4 returned FALSIFIED at C2 under the v1.5 routing, with the Phase A distribution producing uniform Recognition saturation across all three cells — every panel brand scored C_P = 6/6, with distinct C_P = 1 and modal share = 1.000 in each cell. Under v1.6 retrospective scoring (González Castro, 2026f), this classifies as uniform-saturation by Increment 1 — the program's first measured trigger of the rule, routing Regime 4 to REGIME-4-UNAVAILABLE-AT-RECOGNITION.

Increment 2 returns CONFIRMED on H_IdentityLoad_Direct — the program's first CONFIRMED moderator verdict at any layer. Cell A δ = −3.13 (medium IL, canonical-led), Cell B δ = +7.13 (high IL, cultural-led), and Cell C δ = +1.00 (low IL, between) — the monotonic ordering Cell A δ < Cell C δ < Cell B δ runs in the IL-predicted direction. The 95% bootstrap CIs: Cell B [+4.75, +10.25] excludes zero; Cell A [−6.00, −0.25] excludes zero in the opposite direction as predicted; Cell C [−0.50, +3.25] satisfies the gradient check.

![Type 2 quadrant emergence: v0.20 PARTIAL → v0.21 EMERGED. Cell B count drives the H_Type2_emergence verdict (≥ 3 → EMERGED); cross-phase all-cell count surfaces out-of-cell cases.](../../reports/figs/aias_1_0/chart_04_type2_emergence.pdf){#fig:type2 width=100%}

Increment 3 returns CONFIRMED on H_PhantomBrandPersistence: six off-panel reference-vocabulary brands cleared K = 6 (Urban Decay 13, Estée Lauder 13, Glossier 12, Too Faced 9, Make Up For Ever 7, Clinique 6), and the validity anchor passed with margin (Glossier R_phantom = 12 ≥ required 6). The phantom cohort exhibits a striking channel signature: three of the six are channel-pure, with Estée Lauder and Clinique appearing exclusively in canonical-channel frames (R_cult = 0) and Glossier appearing exclusively in cultural-channel frames (R_cat = 0). The channel signatures track Identity Load — prestige / heritage cosmetics in the canonical channel, celebrity / DTC / cult in the cultural channel — establishing that the IL-gradient mechanism operates substrate-wide rather than panel-internally.

![v0.21 Phantom Brand Persistence — off-panel channel signature (R_cat_phantom × R_cult_phantom). Six off-panel brands clear K = 6; channel signatures track Identity Load. Glossier validity anchor passes with margin.](../../reports/figs/aias_1_0/chart_06_phantom_channel.pdf){#fig:phantom width=100%}

The cross-phase synthesis-layer contribution flagged in §4.4 continues here. The all-cell algorithmic dissociation framework recovers a fourth Type 2 case the v0.21 verdict matrix correctly did not surface within its Cell-B-anchored scope: e.l.f. Cosmetics (Cell C — Drugstore / mass; C_P = 6, R_cat = 1, R_cult = 9). Together with La Mer in v0.20, e.l.f. jointly establishes out-of-cell Type 2 as a recurrent feature of the dissociation framework — different substrate, different cell, same dissociation pattern. The v0.21 published verdict stands as the authoritative within-phase result; the synthesis adds the cross-phase algorithmic perspective alongside it.

# 5. The AIAS Presence construct

The construct claim is developed in seven layers. Each layer states the claim, names the empirical anchors in §4, and marks the boundary of what is established.

**L1 — AI Availability as a third measurable layer.** AI Availability — the brand-level probability that an AI intermediary retrieves, recommends, or selects a brand in a category-anchored decision context — is a third measurable layer alongside Ehrenberg-Bass Mental Availability and Physical Availability. Measurability is the operative claim: under the AIAS Presence Measurement Protocol's pre-registered procedure, AI Availability resolves to falsifiable verdicts that can be evaluated against each phase's locked verdict matrix and replicated across substrate families. The empirical support is the full six-phase corpus — all five substrate families produced coherent verdicts under the protocol, and no substrate drove the program to abandon the construct or rebuild the measurement procedure at the foundational layer. The boundary is the demarcation from construct validity: measurability is established; predictive, convergent, and discriminant validity remain Phase 3 work.

**L2 + L3 — Multi-component construct: Recognition × two-channel Recall.** AI Availability decomposes into at least two empirically separable components: Recognition (C_P, brand category-membership canonicity across the panel) and Recall (brand retrieval into category-anchored open-ended responses). v0.17's first Iwachu case demonstrated that a brand can be fully recognized (C_P ≥ 5) while returning sparse Recall, dissociating the two components empirically; v0.18 extended the dissociation across cells; v0.21's uniform Recognition saturation confirmed the dissociation in the limit case where Recognition is exhausted at the substrate level. Recall decomposes further into canonical authority (R_cat) and cultural footprint (R_cult). The two channels operate on disjoint inputs and can be managed independently. v0.21's Rare Beauty (R_cat = 1, R_cult = 17 against C_P = 6) anchors the textbook two-channel dissociation — a brand fully recognized by every panel intermediary, virtually absent from canonical Recall, and dominant in cultural Recall.

**L4 + L5 — Dissociation patterns and Identity-Load moderator.** Three canonical patterns occupy the Recognition × Recall plane: Iwachu (C_P ≥ 5 ∧ R_cat ≤ 2), Type 1 (canonical-preferred: R_cat ≥ 5 ∧ R_cult ≤ 2), and Type 2 (cultural-preferred: R_cat ≤ 2 ∧ R_cult ≥ 5). Iwachu generalizes across all five substrate families. Type 2 cleared the EMERGED threshold in v0.21 with three Cell B cases after PARTIAL in v0.20. The cross-phase synthesis layer — La Mer in v0.20 Cell A and e.l.f. Cosmetics in v0.21 Cell C — establishes out-of-cell Type 2 as a recurrent feature of the dissociation framework beyond per-phase Cell-B-anchored verdicts.

Per-cell channel asymmetry δ = mean(R_cult) − mean(R_cat) tracks the Identity-Load gradient. v0.21 H_IdentityLoad_Direct CONFIRMED is the program's first CONFIRMED moderator verdict, with Cell A δ = −3.13 (medium IL, canonical-led), Cell B δ = +7.13 (high IL, cultural-led), and Cell C δ = +1.00 (low IL, between) — the monotonic ordering Cell A δ < Cell C δ < Cell B δ runs in the IL-predicted direction. v0.20 H_IdentityLoad_Direct PARTIAL carried the moderator directionally in Cell B while surfacing the skincare-specific Cell A architecture. The boundary of L5: Identity Load is operationalized through cell construction at the panel-design layer, not measured at the consumer layer; the moderator's mechanism is the IL gradient of the panel design as it interacts with two-channel Recall.

**L6 — Phantom Brand Persistence as an empirical regularity.** Off-panel brands persistently surface in panel-anchored category retrieval. The phenomenon is framed as an empirical regularity — a stable pattern recoverable through replication-discipline measurement, comparable to Double Jeopardy or the duplication-of-purchase law — rather than a coordinate mechanism deduced from first principles. v0.21 H_PhantomBrandPersistence CONFIRMED with six brands clearing K = 6, the Glossier validity anchor passing with margin (R_phantom = 12), and channel signatures in which Estée Lauder and Clinique appear exclusively in canonical frames while Glossier appears exclusively in cultural frames, tracking Identity Load. The boundary: v0.21 is the calibration anchor; v0.22+ phases under v1.6 are the genuine generalization test.

**L7 — AIAS 1.0 as Presence, with the six-component composite as a multi-year roadmap.** The synthesis claims measurement of the Presence component, not the full multi-component composite. The remaining five dimensions (Ranking, Consistency, Coverage, Grounding, Sentiment) ship under a successor program. Measurability of one component established under pre-registration discipline against a five-substrate anchor base is a stronger claim to make and defend than measurement of an under-specified composite. The version number encodes the discipline: 1.0 names the moment when the construct's first component reaches falsifiable measurement under cross-substrate replication.

# 6. Discussion

## 6.1 Implications for marketing science

The construct claim is additive to the Ehrenberg-Bass canon, not a replacement of Mental or Physical Availability. Sharp's two-layer formulation (Sharp, 2010; Romaniuk, 2018; Sharp and Romaniuk, 2021) remains the discipline's central availability framework; the present synthesis adds a third measurable layer at the AI-mediated retrieval surface that the two-layer formulation does not cover by construction. Categories whose purchase environments are increasingly mediated by AI intermediaries gain a third construct that brand managers and marketing scientists can track alongside Mental Availability metrics (category entry points, distinctive asset strength) and Physical Availability metrics (distribution depth, channel coverage). The synthesis enters the discipline under the same pre-registration discipline that the Ehrenberg-Bass tradition has built credibility on — locked panels, locked hypothesis matrices, public data deposits, replication across substrates. Integration of the third layer into existing brand-tracking instruments is Phase 3 work: cross-construct calibration, shared-substrate measurement designs, and convergent / discriminant validity testing will determine the integration's operational form.

## 6.2 Implications for Practice

The construct's most actionable finding is the two-channel Recall decomposition. R_cat and R_cult operate on disjoint inputs and can be managed separately. Canonical-channel Recall responds to authority surfaces — editorial coverage, expert recommendation, dermatologist endorsement, makeup-artist recommendation. Cultural-channel Recall responds to discourse density — social-media volume, celebrity endorsement, viral content, community-curated cult-tier discourse. The v0.21 cosmetics evidence establishes that brands can occupy substantially different positions on the two channels within a single category, and that the IL gradient of the substrate's panel design predicts where a brand will land. Practitioners can audit a brand's current channel position with the protocol's measurement procedure and target the underperforming channel with the appropriate intervention class without conflating the two pathways into a single Recall budget.

The Rare Beauty case (R_cat = 1, R_cult = 17 against C_P = 6) is the textbook diagnostic: a brand with full Recognition and overwhelming cultural-channel Recall but negligible canonical-channel Recall has identifiably different brand-strategy options than a brand with the opposite profile. The measurement procedure surfaces this distinction at the audit layer rather than leaving it to interpretation.

Phantom Brand Persistence carries a second practical finding: brand presence in AI-mediated retrieval can exceed the boundaries of any single panel construction. A brand that does not appear in a measurement panel can nonetheless persistently surface in the panel's retrieval responses, with channel signature tracking the brand's Identity Load. For brands at the substrate's edge — strong cultural footprint but absent from the canonical panel of any category-tracking study — the phantom layer is the reason AI Availability cannot be inferred from panel-internal absence; it must be measured against an exogenously constructed reference vocabulary at the substrate level.

## 6.3 Limitations

Several limitations bound the present synthesis. The reference panel is held fixed at the v0.17 six-slot specification, and provider model substitutions over future-phase horizons are expected; v0.21's verdicts are properties of brand × substrate × panel triples measured at acquisition time. The fixed-panel discipline is the program's cross-phase comparability anchor, but it is also a measurement-window constraint — the construct's stability across model generations remains future work. Four of the five substrate families operated in English-language consumer-discovery environments; cross-language replication is held as future work. Cell-classification limits surfaced through e.l.f. Cosmetics' out-of-cell Type 2 case: the IL-gradient cell structure assumes brands behave per their supply-side tier classification, and a brand that crosses the supply-side / discourse-side boundary exposes friction in the classification scheme. The retrospective-scoring boundary is a methodology constraint: v0.16 through v0.19 lack R_cult data and cannot be evaluated against the v1.6 Increment 2 specification; the H_IdentityLoad_Direct evidence base is bounded to v0.20 and v0.21. The synthesis does not claim construct validity — predictive validity against behavioral outcomes, convergent validity across alternative panel constructions, and discriminant validity against Mental and Physical Availability are Phase 3 work. The synthesis is silent on the consumer-behavior correlate of AI Availability; any reading that imports a behavioral-correlate claim reads beyond the evidence presented.

# 7. Future research

## 7.1 Phase 3 — construct validation

The most consequential next step is construct validation. Predictive validity against behavioral outcomes — whether AI Availability scores predict downstream consumer behavior such as brand consideration, search behavior, or purchase — is the primary validation criterion and the program's Phase 3 anchor. Discriminant validity against Mental Availability and Physical Availability — establishing that AI Availability captures variance the existing constructs do not — requires paired measurements of all three constructs against a common brand-substrate cohort. Both sit in the Phase 3 pre-registration roadmap and are not in the present synthesis's claim scope. The validation design will inherit the same pre-registration discipline that v1.2 through v1.6 established for the measurement layer.

## 7.2 Phase 4 — full six-component AIAS composite

The Tri-System framework (González Castro, 2026a) names the full AIAS composite as a six-component construct spanning Presence (operationalized here), Ranking, Consistency, Coverage, Grounding, and Sentiment. The remaining five components ship under a Phase 4 successor program; their specifications, verdict matrices, and pre-registration discipline are reserved for the Phase 4 round and are not load-bearing for the present claim. The version-number arc increments only when each successor component reaches falsifiable measurement against a cross-substrate anchor base.

## 7.3 Substrate and language expansion

The five-substrate anchor base is foundational but not exhaustive. v0.22 and subsequent phases under v1.6 will extend the base into additional substrate families, test the v1.6 increments prospectively against substrates outside the present retrospective scope, and refine the substrate-classification taxonomy as new substrate shapes surface. Cross-language replication is the second expansion axis: non-English-language substrate phases will test whether the measurement procedure transfers across discourse-language boundaries with panel-internal scoring discipline held fixed. Panel-construction sensitivity is the third axis: studies that hold substrate and methodology version fixed while varying the panel — substituting providers, varying panel size, testing single-provider against multi-provider panels — will supply convergent-validity evidence that Phase 3 construct validation requires. The three axes together carry the construct's anchor base from the present five families into a sustained replication program. The anchor base does not need to be exhaustive to be load-bearing; it needs to be deep enough that the construct's claims are testable, replicable, and falsifiable. The present synthesis establishes that depth has been reached; the expansion program extends it.

# References

González Castro, P. U. (2026a). Tri-System Brand Growth: The AI Mediation Layer. SSRN Working Paper. https://ssrn.com/abstract=6659000

González Castro, P. U. (2026b). The AIAS Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy (v1.2). SSRN Working Paper. https://ssrn.com/abstract=6761698

González Castro, P. U. (2026c). The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification (v1.3). SSRN Working Paper. https://ssrn.com/abstract=6797679

González Castro, P. U. (2026d). The AIAS Presence Measurement Protocol: Recognition × Recall Decomposition and Multi-Component AI Availability (v1.4). SSRN Working Paper. https://ssrn.com/abstract=6799479

González Castro, P. U. (2026e). The AIAS Presence Measurement Protocol: Multi-Statistic C2 and Two-Channel Recall Decomposition (v1.5). SSRN Working Paper. https://ssrn.com/abstract=6810758

González Castro, P. U. (2026f). The AIAS Presence Measurement Protocol: Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension (v1.6). SSRN Working Paper. https://ssrn.com/abstract=6816340

González Castro, P. U. (2026g). Regime 4 Boundary and Discourse-Language Carryforward on the Kitchen-Knives Substrate (v0.16). SSRN Working Paper. https://ssrn.com/abstract=6791999

González Castro, P. U. (2026h). Panel Inadequacy and Recognition × Recall Dissociation on the Premium Kitchenware Substrate (v0.17). SSRN Working Paper. https://ssrn.com/abstract=6802261

González Castro, P. U. (2026i). Identity-Load Moderator Test and Recognition × Recall Dissociation Generalization on an English-Language Indie Fragrance Substrate (v0.18). SSRN Working Paper. https://ssrn.com/abstract=6806558

González Castro, P. U. (2026j). Panel Inadequacy and Recognition × Recall Dissociation on the Audiophile Headphones Substrate (v0.19). SSRN Working Paper. https://ssrn.com/abstract=6809182

González Castro, P. U. (2026k). Type 2 Emergence and First Prospective v1.5 C2 Calibration on a Skincare IL-Gradient Substrate (v0.20). SSRN Working Paper. https://ssrn.com/abstract=6811441

González Castro, P. U. (2026l). Type 2 Confirmation, Recognition Ceiling, and Phantom Brand Persistence on a Cosmetics IL-Gradient Substrate (v0.21). SSRN Working Paper. https://ssrn.com/abstract=6815378

Nosek, B. A., Ebersole, C. R., DeHaven, A. C., and Mellor, D. T. (2018). The Preregistration Revolution. Proceedings of the National Academy of Sciences, 115(11), 2600–2606.

Romaniuk, J. (2018). Building Distinctive Brand Assets. Oxford University Press.

Sharp, B. (2010). How Brands Grow: What Marketers Don't Know. Oxford University Press.

Sharp, B., and Romaniuk, J. (2021). How Brands Grow Part 2: Including Emerging Markets, Services and Durables, New Categories and Brand Purpose (revised edition). Oxford University Press.

---

# Declarations

**Declaration of interest.** The author is employed by Samsung Electronics America (Director, Corporate Brand Creative and Governance). The AIAS Presence Measurement Protocol and the synthesis work reported here are the author's independent academic research, conducted outside the scope of employment, in the author's role as faculty at the School of Visual Arts MPS Branding Program and founder of Third System. Samsung had no role in the design, execution, analysis, or interpretation of this work. Each phase in the v0.16–v0.21 corpus included a pre-acquisition COI screen confirming no brand in the phase panel is affiliated with Samsung Electronics America; the synthesis introduces no new panel and inherits the per-phase COI screens as documented at each phase's osf.io/ec6wh deposit.

**Funder.** Self-funded.

**Ethics.** Not applicable; no human subjects. The research uses publicly accessible LLM APIs queried with non-personal, category-anchored prompts.

**Data and code availability.** All pre-registration artifacts, acquisition data, scoring code, retrospective scoring outputs, cross-phase synthesis data, chart sources, and verdict outputs are deposited under Open Science Framework project ec6wh at osf.io/ec6wh/aias_1_0/. The phase-level deposits at osf.io/ec6wh/v16/ through osf.io/ec6wh/v21/ carry each phase's pre-registration, acquisition data, scoring code, and verdicts. The methodology paper deposits at osf.io/ec6wh/methodology/v1_2/ through osf.io/ec6wh/methodology/v1_6/ carry the locked methodology versions.

**AI disclosure.** Large language models are the measurement instrument of the study, not the writing instrument. The reference panel of six LLMs was queried per the locked measurement protocol. Manuscript writing was assisted by Claude (Anthropic) as a drafting and editing tool; all substantive intellectual content, methodology design, hypothesis specification, and conclusions are the author's own. AI-assisted writing is disclosed in alignment with COPE and ICMJE guidance on LLM use in scholarly writing.

**Trademark notice.** AIAS and Third System are trademarks of the research program.
