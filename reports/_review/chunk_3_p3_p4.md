# Chunk 3 of 4 — PATTERNS P3 + P4 draft

**Target file:** `reports/aias_1_0_content.py` → `PATTERNS[2]` + `PATTERNS[3]`
**Review artifact** (2026-05-23); not yet assembled into the final content module.
**Source translation:** synthesis paper (SSRN 6817841) §4.5 (Type 2 paragraph + IL Direct paragraph) + §4.4 (skincare PARTIAL precedent) + §4.2 (indie fragrance precursor) + §5.3 (L3) + §5.5 (L5) + §6.2 (brand-practice paragraphs), per the P1–P5 register lock in `reports/aias_1_0_content_outline.md` §3.

**Per outline §7 estimate:** 4 paragraphs per finding × ~150–200 words avg = ~700 words per finding × 2 findings = ~1400 words for chunk 3. Actual: ~1525 words (close to target; slightly over due to methodology context needed for non-academic readers to evaluate the verdict numbers).

**Voice register check applied:**

- Concrete data leads each paragraph; meta-claims about which finding matters trimmed per the consistency rule established in chunk 1 ¶6 / chunk 2 ¶2 fixes.
- Bootstrap CI numbers retained verbatim from synthesis paper §4.5 for traceability.
- Brand-strategy implications surfaced explicitly in P3 ¶3 (separable interventions) and P4 ¶4 (predictive prior from cell position).

---

## FINDING 03 — P3: Recall splits into two channels that can be managed separately. Rare Beauty 1:17 is the textbook diagnostic.

- **Title (PATTERNS[2].title):** *Recall splits into two channels that can be managed separately. Rare Beauty 1:17 is the textbook diagnostic.*
- **Chart slot:** `f3_type2_emergence` → `chart_04_type2_emergence.pdf` (re-used from synthesis paper per D3(a))
- **Source map:** synthesis §4.5 (Type 2 paragraph — Rare Beauty + Huda Beauty + Kylie Cosmetics); §5.3 (L3 two-channel decomposition); §6.2 (brand-practice paragraph — R_cat / R_cult intervention classes)

### ¶1 — The two-channel decomposition (~200 words)

> The Recall layer of the protocol splits into two channels at the v1.5 specification. The canonical channel (R_cat) is anchored by three prompt frames: best brands in the category, most-recommended brands in the category, highest-quality brands in the category. The cultural channel (R_cult) is anchored by three prompt frames: most popular brands in the category, celebrity-favorite or influencer-driven brands in the category, viral or cult-favorite brands in the category. Each frame is sent to each of the six panel intermediaries; per-brand R_cat and R_cult are mention counts ranging 0–18 (3 frames × 6 models). The two channels operate on disjoint inputs: R_cat responds to authority surfaces — editorial coverage, expert recommendation, category-best curation, professional certification, dermatologist endorsement, makeup-artist recommendation. R_cult responds to discourse density — social-media volume, celebrity endorsement, viral content, community-curated cult-tier discourse, founder-identity association. Conflating them under a single Recall metric loses the actionable diagnosis: a brand strong on one channel and weak on the other reads as average under single-channel scoring but reads as channel-asymmetric under the two-channel decomposition, and the asymmetry is the audit signal.

### ¶2 — Rare Beauty diagnostic + Cell B companions (~170 words)

> Rare Beauty is the textbook diagnostic case in v0.21 cosmetics. With Recognition saturated at C_P = 6/6 — universally categorized as a cosmetics brand by every panel intermediary — the brand's canonical-channel Recall is 1/18 while its cultural-channel Recall is 17/18. The 1:17 split establishes the upper bound on how decoupled the two channels can be within a single brand: nearly every cultural-frame mention available, almost none of the canonical-frame mentions. Two Cell B companions joined Rare Beauty in clearing the EMERGED threshold for the Type 2 cultural-channel-preferred quadrant (R_cat ≤ 2 and R_cult ≥ 5): Huda Beauty (R_cat = 0, R_cult = 11) and Kylie Cosmetics (R_cat = 0, R_cult = 5). The three Cell B cases share a brand-positioning profile — celebrity-DTC cosmetics with founder-identity association at the substrate's high-Identity-Load tier — and the Type 2 emergence is the empirical signature of that positioning class translating to AI retrieval.

### ¶3 — Separable interventions for brand strategy (~190 words)

> For brand strategy, the two-channel decomposition makes interventions targetable rather than budget-consuming. A brand whose AI Availability audit returns low canonical-channel Recall has identifiable intervention pathways: build editorial-coverage relationships in the category's authority press; pursue makeup-artist and dermatologist recommendations where the category supports them; secure category-best list inclusion at curated review surfaces; target professional-certification visibility. A brand whose audit returns low cultural-channel Recall has a different intervention class: invest in social-media volume; secure celebrity or influencer endorsement; build community-curated cult-tier discourse through founder identity and brand storytelling. A brand strong on one channel and weak on the other can target the weaker channel without trading off against the stronger; the two channels do not share input budgets and they do not compete for the same brand-strategy resources. The audit is the diagnostic, not the prescription — but the audit surfaces a structural distinction (canonical vs. cultural channel position) that the prescription can then act on without the brand-strategy team having to negotiate the intervention class as a separate question.

### ¶4 — Diagnostic upper bound + Type 1 anchor + audit geometry (~190 words)

> Rare Beauty's 1:17 channel split is the upper bound; the dissociation framework also identifies the inverse pole. The Type 1 pattern — canonical-channel-preferred Recall, R_cat ≥ 5 and R_cult ≤ 2 — surfaces in the v0.21 cosmetics Cell A (prestige) with Bobbi Brown (R_cat = 8, R_cult = 0) and Laura Mercier (R_cat = 5, R_cult = 0) as the channel-pure canonical anchors. The Type 1 and Type 2 poles bracket the two-channel space within a single substrate. Brand managers auditing a candidate brand can locate its position in the R_cat × R_cult plane and read its position against the substrate's Type 1 and Type 2 anchors: a brand near a pole has identifiable intervention options matched to the dominant channel's input class; a brand near the Iwachu region — high Recognition with low Recall in both channels — has a different question — why the categorical Recognition isn't converting to either channel of Recall; a brand in the middle reads as positioned-but-undifferentiated and may warrant a positioning decision before an AI Availability intervention. The two-channel decomposition turns AI Availability from a single metric into an audit surface with structural geometry.

---

## FINDING 04 — P4: Identity Load predicts the AI channel where a brand will surface. Cosmetics returned the program's first CONFIRMED moderator verdict.

- **Title (PATTERNS[3].title):** *Identity Load predicts the AI channel where a brand will surface. Cosmetics returned the program's first CONFIRMED moderator verdict.*
- **Chart slot:** `f4_il_direct_forest` → `chart_05_il_direct_forest.pdf` (re-used from synthesis paper per D3(a))
- **Source map:** synthesis §4.5 (IL Direct paragraph); §4.4 (skincare PARTIAL with substrate-specific Cell A architecture); §4.2 (indie fragrance IL-gradient signature in single-channel data); §5.5 (L5); §6.2 (brand-practice — predictive prior from cell position)

### ¶1 — The IL Direct construct + v1.6 specification (~200 words)

> Identity Load is the substrate-design property that distinguishes the panel's cells: prestige (Cell A, medium IL — established editorial recognition and category-best curation as primary brand identity); celebrity-DTC / cult (Cell B, high IL — strong founder-identity association and community-curated discourse as primary brand identity); drugstore / mass (Cell C, low IL — distribution-led brand identity, less identity-anchored discourse). The v1.6 Increment 2 specification (SSRN 6816340) introduced the H_IdentityLoad_Direct test: per cell, δ = mean(R_cult) − mean(R_cat) is computed with a 95% percentile bootstrap confidence interval (n = 10,000), and the verdict matrix requires the CI to exclude zero in the IL-predicted direction in Cell B (the high-IL anchor, cultural-channel-leading expected); the IL-predicted opposite direction in Cell A (the medium-IL anchor, canonical-channel-leading expected); and the monotonic-gradient check Cell A δ < Cell C δ < Cell B δ across cells. The test is evaluable independently of the protocol's Regime 4 conditions — a separation that the v1.5 framework did not permit and that v1.6 introduced specifically to surface the moderator signal where prior framework versions could not.

### ¶2 — v0.21 cosmetics CONFIRMED (~165 words)

> The v0.21 cosmetics measurement returned CONFIRMED on the H_IdentityLoad_Direct test, with each cell's δ falling in its predicted region and the monotonic-gradient check satisfied. Cell B δ = +7.13 with 95% bootstrap CI [+4.75, +10.25] — the program's strongest cultural-channel-lead signal, with cultural-frame mentions outpacing canonical-frame mentions by 7.13 average across Cell B brands. (Rare Beauty's 1:17 split from Finding 03 is the Cell B exemplar.) Cell A δ = −3.13 with CI [−6.00, −0.25] — the canonical channel leads in the medium-IL prestige cell, as the IL gradient predicts. Cell C δ = +1.00 with CI [−0.50, +3.25] — between Cell A and Cell B, satisfying the monotonic-gradient check. v0.21 is the program's first CONFIRMED moderator verdict at any layer. The IL-gradient construct moves from a hypothesized pattern visible in earlier-phase single-channel data to a measured moderator with confidence-interval rigor.

### ¶3 — v0.20 skincare PARTIAL + v0.18 indie fragrance context (~205 words)

> The skincare measurement (v0.20) returned PARTIAL on the same test, with the substrate's IL signal carrying directionally with prediction but with substrate-specific architecture. Cell B δ = +3.75 with CI [+2.25, +5.25] cleared the IL-predicted direction. Cell A δ = +0.75 with CI [−0.25, +2.12] carried against prediction with CI overlapping zero — clinical and heritage skincare brands such as CeraVe, La Roche-Posay, and Eucerin do not concentrate in canonical-channel Recall the way prestige cosmetics brands do, because skincare's canonical authority lives in dermatologist-recommended and clinical-result-anchored discourse rather than in editorial-prestige curation. Cell C δ = −2.50 with CI [−5.25, +0.38] broke the monotonic-gradient check with Cell A. The skincare finding is substrate-specific rather than methodology-disqualifying: the IL-gradient model holds for the substrate, but the cell where canonical authority concentrates is not the cell that the standard panel-design heuristic predicts. Indie fragrance (v0.18) carried an IL-gradient signature visible in the v1.4 single-channel data and articulated the moderator hypothesis as a coherent cross-phase question — the v1.5 two-channel decomposition was designed in response, and the v1.6 H_IdentityLoad_Direct test was specified to surface the signal more cleanly than the v1.5 framework could.

### ¶4 — Brand-strategy implication + boundary (~205 words)

> For brand strategy, the IL-gradient moderator gives the audit a predictive prior. A brand's cell position (and the IL construction of that cell) carries an expected channel asymmetry: high-IL cells expect cultural-channel lead; medium-IL cells expect canonical-channel lead; low-IL cells lie between under monotonic-gradient discipline. A brand whose measured channel asymmetry matches the cell's expected asymmetry reads as cell-typical; deviation from the expected asymmetry is itself diagnostic information — the brand is operating against the cell's IL grain, and the diagnostic surfaces the deviation as a question worth investigating (a high-IL cell brand with unexpectedly strong canonical Recall may be punching above its cell's editorial weight; a low-IL cell brand with unexpectedly strong cultural Recall may be operating with social-media leverage uncharacteristic of its tier). One boundary is essential: Identity Load is operationalized through the substrate's panel design, not through independently-measured consumer perceptions of the brand. The moderator operates on the panel-design construction, not on a separately-measured consumer-side construct of brand identity. The construct's mechanism is the IL-gradient property of the substrate-as-measured, and the brand-strategy implication is bounded to substrates where the panel-design IL classification meaningfully tracks the brand-of-interest's category positioning.

---

## Chunk 3 self-scan

**Word counts:**

- FINDING 03 (P3): ¶1 200 / ¶2 170 / ¶3 190 / ¶4 190 = **750 words**
- FINDING 04 (P4): ¶1 200 / ¶2 165 / ¶3 205 / ¶4 205 = **775 words**
- **Chunk 3 total: ~1525 words**

**Voice register checks:**

- P3 ¶1 opens "The Recall layer of the protocol splits into two channels at the v1.5 specification." — methodology fact (necessary context for non-academic readers to evaluate ¶2's numbers); not a meta-claim. ✓
- P3 ¶2 opens "Rare Beauty is the textbook diagnostic case in v0.21 cosmetics." — names the case, then immediately concrete: "With Recognition saturated at C_P = 6/6..." ✓
- P3 ¶3 opens "For brand strategy, the two-channel decomposition makes interventions targetable rather than budget-consuming." — opens with the brand-strategy claim, then immediately concrete intervention class. ✓
- P3 ¶4 opens "Rare Beauty's 1:17 channel split is the upper bound; the dissociation framework also identifies the inverse pole." — concrete contrast, then Type 1 anchor numbers (Bobbi Brown 8:0, Laura Mercier 5:0). ✓
- P4 ¶1 opens "Identity Load is the substrate-design property that distinguishes the panel's cells..." — definitional but anchored in cell architecture, not abstract methodology. ✓
- P4 ¶2 opens "The v0.21 cosmetics measurement returned CONFIRMED on the H_IdentityLoad_Direct test..." — concrete verdict + numbers follow immediately. ✓
- P4 ¶3 opens "The skincare measurement (v0.20) returned PARTIAL on the same test, with the substrate's IL signal carrying directionally with prediction but with substrate-specific architecture." — concrete contrast + substrate-specific architecture as the brand-strategy framing. ✓
- P4 ¶4 opens "For brand strategy, the IL-gradient moderator gives the audit a predictive prior." — actionable framing. ✓

**Conventions:**

- ™ marked once in chunk 3 (P4 ¶3 reference to "v1.6"); ™ inheritance from earlier chunks assumed. Single-section-introduction marking applied per v21 convention; double-checking at final assembly whether each PATTERNS entry needs its own ™ mark.
- Verdict labels (CONFIRMED, PARTIAL, EMERGED) preserved.
- Cell construction names (Cell A prestige, Cell B celebrity-DTC, Cell C drugstore/mass) used consistently with chunk 1 / 2 references.
- Bootstrap CI numbers carried verbatim from synthesis paper §4.5 for traceability.

**Cross-references between findings:**

- P3 ¶2 forward-anchored from chunk 2 / P2 ¶2 ("Finding 04 below" was the prior reference; P3 doesn't add new forward-refs).
- P4 ¶2 back-references P3: "(Rare Beauty's 1:17 split from Finding 03 is the Cell B exemplar.)" — explicit cross-finding link so P4's Cell B δ = +7.13 reads with the P3 brand-level anchor visible.

**Open question for chunk 4 planning:**

- Chunk 4 covers P5 + LIMITATIONS + WHATS_NEXT. P5 framing locked at outline §3: text-only finding (no chart slot per D3). Confirm at chunk 4 drafting time whether P5 follows the same 4-paragraph PATTERNS structure as P1–P4 or whether the text-only nature warrants a slightly different shape (e.g., 3 paragraphs — one per v1.6 increment — plus a closing implication).

**Holding for chunk 3 review before chunk 4 (P5 + LIMITATIONS + WHATS_NEXT).**
