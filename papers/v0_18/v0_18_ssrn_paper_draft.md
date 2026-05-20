---
title: "Identity-Load Moderator Test and Recognition × Recall Dissociation Generalization on an English-Language Indie Fragrance Substrate"
subtitle: "AIAS Presence Measurement Protocol, v0.18"
author:
  - name: "Pablo Ulpiano González Castro"
    affiliations:
      - "School of Visual Arts, MPS Branding Program, New York, NY (primary academic affiliation)"
      - "Third System™ (research entity; data archive and methodology venue)"
    email: "pablou@pablou.com"
    orcid: "0009-0003-8968-9990"
date: "2026-05-XX [TBD at SSRN submission]"
mainfont: Carlito
fontsize: 11pt
linkcolor: black
urlcolor: black
header-includes:
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

<!--
v0.18 SSRN paper draft — pre-acquisition state
Pre-reg lock: v0.18-prereg-r1 @ commit 183386c
Branch: v0.18-il-gradient
Sections marked [TBD-VERDICT] fill post-acquisition once score_v18.py emits.
Sections marked [TBD-DEVIATIONS] fill from running DEVIATIONS log.

Carlito glyph substitutions handled by build_paper_v0_18.py:
  ₜ → $_{t}$, ∈ → $\in$, ⁻ⁿ → decimal form, etc.
Body uses Unicode subscripts and Greek; build script does Unicode→LaTeX.
-->

# Abstract

The AIAS™ Presence Measurement Protocol operationalizes AI Availability — the brand-level probability of retrieval, recommendation, or selection by an AI intermediary — as a measurable construct alongside Ehrenberg-Bass Mental Availability and Physical Availability. Protocol v1.4 (SSRN 6799479) extends AI Availability into a multi-component construct (Recognition × Recall) anchored empirically by the Iwachu dissociation in v0.17 (SSRN 6802261). This paper reports v0.18, which tests two pre-registered hypotheses orthogonally: (a) the three-leg joint Identity-Load moderator hypothesis closing the AMBIGUOUS verdict left by the v0.16/v0.17 panel (v0.16 PARTIAL, v0.17 FALSIFIED on panel inadequacy), and (b) the generalization of the Recognition × Recall dissociation from the cross-cultural Japanese-cell substrate to a same-language IL-gradient substrate. The substrate is indie fragrance, sampled across three cells stratified by Identity Load: mass-prestige (medium IL), designer-niche (medium-high IL), and indie/artisan (high IL). Each cell holds 8 brands (worldwide n = 24 pre-floor; C1 floor n ≥ 12). The reference panel is the locked six-slot v0.17 panel. Phase B uses a three-frame query battery (niche / independent / perfumistas). [TBD-VERDICT: 1–2 sentence summary of resolved verdicts.] The pre-registration discipline (commit 183386c, tag v0.18-prereg-r1) locks panel, hypotheses, decision rules, and dissociation thresholds (Spearman ρ ≥ 0.5 with bootstrap 95% CI lower bound > 0.3) ex-ante.

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

Pre-registration discipline is treated as structurally definitive of the protocol's credibility (Nosek et al., 2018). The v0.18 pre-registration is locked at commit 183386c with tag v0.18-prereg-r1 on branch v0.18-il-gradient (deposited at osf.io/ec6wh/v18/), with all panel composition, hypothesis specifications, decision-rule thresholds, and verdict matrices fixed ex-ante. Any post-acquisition deviation is logged in the DEVIATIONS protocol and explicitly noted in §5.

---

# 2. Methods

## 2.1 Substrate definition and IL-gradient design

"Indie fragrance" is operationally defined as an IL-gradient panel spanning three tiers of Identity Load on the fragrance consumer-discovery surface, rather than strictly as independently-owned brands. Conglomerate ownership of designer-niche houses (Estée Lauder, LVMH) is treated as a borderline classification (see §2.2) and not an exclusion criterion. The panel is entirely English-language-presence anchored; no cross-cultural cells are included.

Three cells are stratified by Identity Load:

- **Cell A — Designer-niche, medium-high IL.** Selection involves curatorial signaling and connoisseur-adjacent discovery within the established prestige-fragrance retail surface.
- **Cell B — Indie/artisan, high IL.** Small-house identity is part of the brand's signal; perfumistas-native lexicon dominates the discovery vocabulary.
- **Cell C — Mass-prestige, medium IL (comparison anchor).** Mainstream designer fragrance with signature-scent role; selection process more separable from product identity.

If the Identity-Load moderator hypothesis holds, the Regime 4 signature should strengthen monotonically C → A → B.

A descriptive sensitivity is pre-registered for Cell C's internal IL variance: the cell spans iconic mass-prestige houses (Chanel, Dior) and mainstream-prestige houses (Marc Jacobs, Calvin Klein). If post-acquisition data reveals sub-clustering, it is reported under §3 sensitivities and does not retroactively re-stratify the cell.

## 2.2 Brand registry and borderline classifications

The locked registry holds 24 brands (8 per cell, n = 24 worldwide pre-floor; C1 floor n ≥ 12). The pre-floor allows 50% LLM-substrate attrition while still clearing C1, addressing the v0.17 lesson where 31% attrition reduced n from 16 to 10 and triggered FALSIFICATION on panel inadequacy.

**Cell A:** Maison Francis Kurkdjian, Le Labo, Diptyque, Frederic Malle, Byredo, Comme des Garçons Parfums, Memo Paris, Etat Libre d'Orange. **Cell B:** D.S. & Durga, Boy Smells, Heretic Parfum, Ellis Brooklyn, Vyrao, Henry Rose, Phlur, Snif. **Cell C:** Chanel, Dior, YSL, Tom Ford, Givenchy, Versace, Marc Jacobs, Calvin Klein.

Borderline-classified brands (Le Labo, Frederic Malle, Byredo) carry conglomerate ownership (EL or LVMH) while retaining designer-niche brand identity. Cell A placement is canonical at lock; Phase B retrieval-frame disposition determines final classification under the DEVIATIONS protocol if surfaces diverge.

Same-house collisions are explicitly excluded: Tom Ford Private Blend and Chanel Les Exclusifs are not split into Cell A despite their designer-niche brand identity, because their parent houses occupy Cell C. Brand-house granularity is the unit of analysis.

## 2.3 Reference panel

The locked six-slot reference panel from v0.16/v0.17 is reused without modification: claude-opus-4-5, claude-sonnet-4-5, gpt-4o, gpt-4o-mini, gemini-2.5-flash, gemini-2.5-flash-lite. Provider model substitutions encountered during acquisition are documented in DEVIATIONS.

## 2.4 Phase A: C_P anchoring

Phase A operationalizes Recognition per Protocol v1.4. For each registry brand, the v1.4 C_P probe is sent to each of the six panel models; the brand's C_P score (range 0..6) is the count of recognition-positive responses across the panel. Per-cell pivot determination follows the cascade rule: the first brand in cascade order achieving C_P = 6/6 becomes the cell pivot, and remaining cell brands are probed for the dissociation analysis and §3 sensitivities. If a full cell cascade fails to anchor a pivot, alternates are invoked under a DEVIATIONS entry (alternates locked in pre-reg §1.4).

## 2.5 Phase B: three-frame query battery

Phase B operationalizes Recall. Three category-anchored query frames are sent to each of the six panel models, yielding 18 observations per brand:

- **q1 (primary anchor — niche):** "What are the best niche fragrances? List several with descriptions."
- **q2 (cross-frame — independent):** "Recommend high-quality independent fragrance brands. Name several brands."
- **q3 (perfumista lexicon):** "What fragrances do industry insiders and perfumistas recommend? List several."

For each (frame, model) response, all 24 registry brands are scanned for mention presence under the v1.4 canonical brand-mention detection rules (case-insensitive, accent-stripped, possessive-aware, first-occurrence-wins de-duplication). Rank within enumerated response lists is recorded for Phase D ρ analysis.

The "niche" lexical anchor is selected as the primary surface because it is the perfumista-native vocabulary most tightly bound to identity-loaded fragrance discovery; the cross-frame structure preserves diagnostic capacity against alternate retrieval anchors.

## 2.6 Phase D ρ — planned from start

Phase D ρ is computed for each cell with post-attrition n ≥ 5, regardless of where C1/C2/C3 resolution occurs. ρ is the Spearman rank correlation between Phase A C_P (per brand) and Phase B mention count (per brand) within the cell. Pre-registering Phase D as planned-from-start (rather than conditional on verdict resolution) follows the internal consistency requirement that arises once the Recognition × Recall dissociation is pre-registered as a primary co-hypothesis (§2.8): ρ is the natural quantitative layer for the Recall component, and its conditioning would compromise the multi-component construct's internal coherence.

## 2.7 Hypotheses

Three orthogonal hypotheses are pre-registered, operating at three distinct scopes (within-phase, three-leg-joint, methodological-generalization). Verdict matrices are specified ex-ante (§2.9).

### H_Regime4_indie_fragrance (within-phase substantive)

The Cell C → Cell A → Cell B Regime 4 signature strengthens monotonically along the Identity-Load gradient, with Cell B exhibiting the strongest signature. Operationalized through the C1 → C2 → C3 cascade (§2.8).

### H_IdentityLoad_moderator (three-leg joint, v0.16 × v0.17 × v0.18)

Identity Load moderates the Regime 4 signature across substrates: higher-IL substrates produce stronger signatures. The three-leg joint verdict combines v0.16 (PARTIAL), v0.17 (FALSIFIED on panel inadequacy), and v0.18 (this phase) per the matrix in §2.9.

### H_Recognition_Recall_dissociation_generalization (primary co-hypothesis, novel for v0.18)

The Recognition × Recall dissociation pattern documented in v0.17 (Iwachu: Phase A C_P = 6/6, Phase B mention rate = 0/18) generalizes to a same-language, IL-gradient substrate.

A **dissociation case** is operationalized per the Iwachu-pattern threshold: any panel brand with Phase A C_P ≥ 5/6 (≥ 83% recognition) *and* Phase B mention rate ≤ 2/18 (≤ 11% recall across three frames).

The **Recognition–Recall correlation threshold** (pre-reg r3 §2.3) is pre-registered for the §2.9 DISSOCIATION_NARROWED routing: Spearman ρ between Phase A C_P and Phase B mention count, pooled across all anchored brands, with ρ ≥ 0.5 *and* bootstrap 95% CI lower bound > 0.3 (10,000 brand-level resamples, percentile-method CI). The CI lower-bound guard prevents small-n inflation from spuriously routing zero-case outcomes to NARROWED at post-attrition pooled n in the 18–24 range. Failure of either condition routes to DISSOCIATION_UNDETERMINED.

## 2.8 Decision rules (C1 / C2 / C3 cascade)

The substantive verdict is resolved through a three-condition cascade carried forward verbatim from v0.17 protocol:

- **C1 — panel adequacy.** Worldwide post-attrition n ≥ 12. Failure → NULL (panel inadequacy).
- **C2 — Regime 4 signature.** Per-cell mention concentration index meets the v0.17 protocol-canonical Regime 4 threshold. Failure → FALSIFIED.
- **C3 — ranking coherence.** Per-cell Phase B mention-rank order coherent with anchor-pivot prominence. Failure → PARTIAL.

Pass through all three → CONFIRMED. C2 and C3 threshold values are protocol-canonical from v0.17 (cited rather than re-specified here).

## 2.9 Verdict matrices

### Three-leg joint H_IdentityLoad_moderator (ex-ante)

| v0.18 leg | Joint verdict (v0.16 PARTIAL × v0.17 FALSIFIED × v0.18) |
|---|---|
| CONFIRMED | CONFIRMED — higher-IL substrate produces stronger Regime 4 signature; v0.17 reread as panel-inadequacy artifact |
| PARTIAL | PARTIAL — moderator operates but bounded; substrate-specific qualifications |
| FALSIFIED | FALSIFIED — Identity Load does not moderate AI Availability across this gradient |
| NULL (C1 inadequacy) | AMBIGUOUS-deferred → v0.19 with further substrate refinement |

### Recognition × Recall dissociation generalization (ex-ante)

| v0.18 dissociation cases (per §2.7 threshold) | Verdict |
|---|---|
| ≥1 case in every cell (cross-cell generalization) | DISSOCIATION_GENERALIZED — v1.4 multi-component claim strengthened |
| ≥1 case but cell-clustered (e.g., only Cell B) | DISSOCIATION_PARTIAL — v1.4 claim qualified; dissociation may be IL-dependent |
| 0 cases, R–R correlation strong (ρ ≥ 0.5 ∧ CI lower > 0.3) | DISSOCIATION_NARROWED — Iwachu may be cross-cultural artifact; v1.4 claim narrows |
| 0 cases, R–R correlation NOT strong | DISSOCIATION_UNDETERMINED — defer to v0.19+ |
| C1 panel inadequacy precludes test | DISSOCIATION_UNDETERMINED — defer to v0.19+ |

The two matrices are independent. Cross-cell entanglement between H_IdentityLoad_moderator and H_Recognition_Recall_dissociation_generalization is reported descriptively in §4 but does not affect formal verdict routing.

## 2.10 Pre-registration lock state

The full v0.18 pre-registration is deposited at osf.io/ec6wh/v18/ with the locked artifact at `osf/v18/PRE_REGISTRATION_v0_18.md` on branch `v0.18-il-gradient`, tagged `v0.18-prereg-r1` at commit `183386c`. Three revision draft iterations (r1 → r2 → r3) preceded lock; revision history is documented in the pre-registration's Appendix A. The Recognition–Recall correlation threshold operationalization (§2.7) was added in r3 in response to drafting `scripts/score_v18.py` and surfacing the matrix-routing gap.

---

# 3. Results

[TBD-VERDICT — fills post-acquisition once `python scripts/score_v18.py` emits `data/verdicts/v0_18_verdict.json` and `v0_18_verdict.md`.]

## 3.1 Phase A — Recognition (C_P anchoring)

[TBD-VERDICT: Per-cell C_P score distributions; pivot anchoring outcomes; cascade history; brands clearing the DISSOCIATION_C_P_FLOOR of 5/6.]

## 3.2 Phase B — Recall (three-frame mention rates)

[TBD-VERDICT: Per-cell mention-rate distributions; per-frame divergence; US/worldwide divergence; post-attrition n per cell.]

## 3.3 Phase D — ρ within cells

[TBD-VERDICT: Per-cell Spearman ρ between Phase A C_P and Phase B mention rate, at n ≥ 5; signal-strength interpretation.]

## 3.4 Recognition × Recall dissociation case identification

[TBD-VERDICT: Brands satisfying the Iwachu-pattern threshold (C_P ≥ 5/6 ∧ mention ≤ 2/18); per-cell distribution; pooled Spearman ρ with bootstrap 95% CI if zero cases observed.]

## 3.5 Verdict resolution

[TBD-VERDICT: Three-orthogonal verdicts: H_Regime4_indie_fragrance, H_IdentityLoad_moderator (three-leg joint), H_Recognition_Recall_dissociation_generalization.]

---

# 4. Discussion

[TBD-VERDICT — fills post-acquisition once verdicts are resolved.]

## 4.1 Identity-Load moderator: substantive interpretation

[TBD-VERDICT: Interpretation of the three-leg joint verdict in the context of the AIAS framework; implications for the v0.17 FALSIFIED-on-panel-inadequacy retrospective reading.]

## 4.2 Recognition × Recall dissociation: methodological interpretation

[TBD-VERDICT: Interpretation of the dissociation generalization verdict for v1.4's multi-component construct; consequences for the AIAS 1.0 canonical methodology layer.]

## 4.3 Cell C internal variance — sensitivity finding

[TBD-VERDICT: Post-hoc analysis of icon-tier vs. mainstream-tier sub-clustering within Cell C, if observed.]

## 4.4 Limits and reservations

[TBD: Substrate-scope limits; LLM-panel temporal validity (model-version drift); the single-substrate constraint on multi-component construct generalization; threshold conservatism trade-offs.]

---

# 5. DEVIATIONS

The DEVIATIONS protocol carries forward from v0.16 / v0.17 (Protocol v1.2 §[ref]; Protocol v1.4 cascade addendum). Any post-lock deviation from the pre-registered design is logged with timestamp, locus, and consequence-for-verdict-routing. New v0.18 entries:

[TBD-DEVIATIONS: Entries opened during Phase A acquisition (provider model substitutions, cascade failures, alternate invocations). Entries opened during Phase B acquisition (brand-mention parsing ambiguities, same-house collision detection at retrieval). Entries opened during scoring (any borderline reclassification under §1.5 resolution).]

---

# 6. Conclusion

[TBD-VERDICT: 2–3 paragraph synthesis. Anticipated framing: (a) joint H_IdentityLoad_moderator verdict and its implication for the substantive theory of AI-mediated brand availability; (b) Recognition × Recall dissociation generalization verdict and its implication for v1.4's multi-component construct as it ships in AIAS 1.0; (c) forward-looking note on v0.19 pre-registration triggers, if any verdicts route to deferred resolution.]

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

**Data and code availability.** All pre-registration artifacts, acquisition data, scoring code, and verdict outputs are deposited under Open Science Framework project ec6wh at osf.io/ec6wh/v18/. The pre-registration is locked at commit 183386c on git tag v0.18-prereg-r1, branch v0.18-il-gradient, with full revision history (r1 → r2 → r3) preserved in Appendix A of the pre-registration artifact.

**Trademark notice.** AIAS™ and Third System™ are trademarks of the research program.

<!-- End v0.18 SSRN paper draft, pre-acquisition state -->
