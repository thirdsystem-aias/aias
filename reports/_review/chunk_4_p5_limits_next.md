# Chunk 4 of 4 — PATTERNS P5 + LIMITATIONS + WHATS_NEXT draft

**Target file:** `reports/aias_1_0_content.py` → `PATTERNS[4]` + `LIMITATIONS` + `WHATS_NEXT`
**Review artifact** (2026-05-23); final content-module checkpoint. After chunk 4 approves, content module locks → builders.
**Source translation:** synthesis paper (SSRN 6817841) §3 (methodology paragraph), §4.5 (v0.21 verdicts that anchor v1.6 increments), §5.7 (L7 scope discipline), §6.3 (limitations), §7 (Phase 3 / Phase 4 / expansion axes); v1.6 methodology paper (SSRN 6816340) for the increment specifications.

**Volumes per outline §7 estimate:**

- P5: ~700 words / 4 paragraphs (matching P1–P4 structure per chunk 3 fix 3)
- LIMITATIONS: ~700 words / 5 paragraphs (vs. v21's 4-paragraph single-phase)
- WHATS_NEXT: ~700 words / 5 paragraphs (vs. v21's 3-paragraph single-phase)
- **Chunk 4 total: ~2100 words** (largest chunk; three sections vs. two in chunks 2–3)

**Voice register check applied:**

- P5 ¶1 names the three increments as concrete methodology objects (not academic abstractions); ¶2 maps each to a v0.21 anchor with numbers; ¶3 translates to brand-strategy vocabulary; ¶4 holds scope discipline.
- LIMITATIONS leads each paragraph with a concrete constraint, not with hedging meta-claims. Brand-managers-reading-the-report framing surfaced explicitly in 4 of 5 paragraphs.
- WHATS_NEXT structures three planning timelines (v0.22+ near-term, Phase 3 multi-year, Phase 4 multi-year) so brand managers can sort the program's future work into actionable planning tracks.

---

## FINDING 05 — P5: Methodology v1.6 closes the operational layer

- **Title (PATTERNS[4].title):** *Methodology v1.6 closes the operational layer. Three increments shipped May 2026.*
- **Chart slot:** none (text-only per D3 — methodology-as-framing finding)
- **Source map:** synthesis §3 (methodology paragraph); §4.5 (v0.21 verdicts anchoring v1.6 increments); §5.7 (L7); v1.6 methodology paper (SSRN 6816340) for increment specifications

### ¶1 — Three v1.6 increments named (~185 words)

> Protocol v1.6 (SSRN 6816340, May 2026) shipped three increments that closed three measurement gaps the prior framework versions could not address. The first increment is a substrate-level Recognition pre-screen: a substrate whose Phase A Recognition distribution is uniformly saturated — every brand recognized as a category member by every panel intermediary, in every cell — is routed to a distinct verdict state rather than collapsed into the prior framework's FALSIFIED bucket. The second increment is an independent moderator pathway: the Identity-Load test is evaluable per-cell with bootstrap confidence intervals, separately from the protocol's four-regime test that the prior framework coupled it to. The third increment is the Phantom Brand Persistence Phase B extension: off-panel brand presence is scored against an exogenously-constructed reference vocabulary with a persistence threshold and a validity anchor, lifting the construct from a descriptive side observation to a measured component. Each increment was specified in v1.6's methodology paper and pre-registered at git tag `v1.6-prereg-r1` before retrospective scoring was applied to the v0.16–v0.21 corpus.

### ¶2 — Each increment mapped to its v0.21 anchor (~205 words)

> Each increment found its first measured anchor in v0.21 cosmetics. Increment 1 returned its first uniform-saturation trigger: every panel brand in every cell scored C_P = 6/6, producing distinct C_P count = 1 and modal share = 1.000 in Cell A, Cell B, and Cell C — a substrate where the prior framework's four-regime test was not applicable, and where v1.6's REGIME-4-UNAVAILABLE-AT-RECOGNITION verdict preserved the substrate's evidentiary value at the moderator and phantom layers (the substrate would have read as a FALSIFIED bucket under prior framework versions, losing the discrimination signal v1.6's pre-screen surfaces). Increment 2 returned the program's first CONFIRMED moderator verdict at any layer: H_IdentityLoad_Direct CONFIRMED with Cell B δ = +7.13 (CI [+4.75, +10.25]), Cell A δ = −3.13 (CI [−6.00, −0.25]), Cell C δ = +1.00 (CI [−0.50, +3.25]), monotonic-gradient check satisfied. Increment 3 returned CONFIRMED with margin: six off-panel brands cleared the K = 6 persistence threshold, and the pre-registered Glossier validity anchor passed at R_phantom = 12. Together they form a coordinated audit pathway for substrates where prior framework versions would have collapsed the verdict — Increment 1 preserves the substrate's evidentiary value, and Increments 2 and 3 carry the discrimination signal that Recognition can't supply when it's exhausted at ceiling.

### ¶3 — What v1.6 makes possible operationally (~205 words)

> For the brand-strategy practitioner, v1.6's increments translate to vocabulary the prior framework versions could not provide. A substrate where every brand is categorically recognized is now identifiable as a category where the discrimination signal lives entirely in Recall — a vocabulary distinction that lets brand managers diagnose maximally-coded categories (cosmetics is the first measured example; other consumer-facing categories with broad media coverage and stable category-membership consensus are candidates for similar shape) without conflating them with categories where Recognition itself carries the diagnostic signal. The moderator pathway makes Identity-Load asymmetry an audit input, not an inferred property — the audit returns δ values with bootstrap CIs, and brand managers can compare a brand's cell-relative position against the cell's measured asymmetry directly. The phantom layer measures off-panel presence, which means brand audits for emerging brands not yet on standard category-tracking panels can include AI Availability as a measurable construct rather than treating panel-absence as missing data. v0.22 and successor phases apply v1.6 prospectively to new substrate families under the same locked protocol; the operational layer is what each new prospective phase consumes, not what each new phase has to first redefine.

### ¶4 — AIAS™ 1.0 scope + composite roadmap (~185 words)

> AIAS™ 1.0 names the Presence component of the AIAS construct, not the full multi-component composite. The Tri-System framework names the composite as a 0–100 score across six measurable dimensions — Presence, Ranking, Consistency, Coverage, Grounding, Sentiment — and positions the composite as a multi-year research arc. AIAS™ 1.0 operationalizes the first of those six dimensions; the remaining five ship under a Phase 4 successor program with specifications, verdict matrices, and pre-registration discipline reserved for that program's pre-registration round. The version-number arc is load-bearing: 1.0 names the moment when the construct's first component reaches falsifiable measurement against a cross-substrate anchor base, and the version increments that follow will track the measurement surface rather than the architectural ambition. The construct does not jump to 2.0 by claiming additional components without measuring them. For brand managers consuming the report's findings, the boundary is the program's credibility asset — what AIAS 1.0 measures is what it claims to measure, and the multi-year roadmap is signposted, not over-claimed.

---

## LIMITATIONS

- **Section heading:** "Limitations"
- **Source map:** synthesis §6.3 (cross-family limitations)
- **Structure:** 5 paragraphs (vs. v21's 4-paragraph single-phase scope), each opening with a concrete constraint and closing with the brand-manager-reading-the-report implication

### ¶1 — Panel-fixed measurement and provider model substitutions (~140 words)

> The reference panel is held fixed at the v0.17 six-slot specification across all phases of the synthesis: Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o-mini, Gemini 2.5 Flash, and Gemini 2.5 Flash Lite. Holding the panel fixed across phases is the program's cross-phase comparability discipline. It is also a measurement-window constraint: the v0.21 verdicts and all earlier-phase verdicts are properties of brand × substrate × panel triples evaluated at acquisition time, not permanent properties of the substrate. Provider model substitutions over future-phase horizons are expected, and the construct's stability across model generations is itself future-work to demonstrate. Brand managers reading verdicts should treat them as measurements anchored in a specific panel state, with the panel's evolution itself a subject for the program's continued discipline.

### ¶2 — English-language anchor (~125 words)

> Four of the five substrate families operated in English-language consumer-discovery environments. The kitchenware family's substrate-language carryforward at v0.16 — where Japanese-language category-bound discourse surfaced different brand mention patterns than English-language responses for the same substrate — is the program's only cross-language acquisition. Cross-language replication is future work. The construct may behave structurally differently in substrates where consumer discovery operates in non-English discourse environments, and the panel intermediaries' English-language training bias is a known structural feature of the measurement system. Brand managers in markets where the brand-of-interest's consumer-discovery surface is non-English should treat the report's findings as suggestive rather than directly transferable, pending prospective cross-language replication phases.

### ¶3 — Cell-classification limits (~140 words)

> Cell-classification limits surfaced through the e.l.f. Cosmetics out-of-cell Type 2 case noted in Finding 01 ¶3 and Finding 03 ¶4. The IL-gradient cell structure assumes brands behave per their supply-side tier classification — a drugstore/mass brand should sit in Cell C, a celebrity-DTC brand in Cell B, a prestige brand in Cell A — and a brand whose observable channel behavior crosses the supply-side / discourse-side boundary exposes friction in the classification scheme. e.l.f. Cosmetics has drugstore/mass price points (Cell C by panel design) but a social-media-native cultural footprint that produces Type 2 dissociation more characteristic of Cell B brands. The classification scheme remains useful at the aggregate level — the IL gradient holds for cell-typical brands — but brand managers auditing brands at the supply-side / discourse-side boundary should expect classification friction.

### ¶4 — Retrospective-scoring boundary (~155 words)

> The synthesis honors the v1.6-locked retrospective-scoring boundary without extension. Increment 1 (substrate Recognition pre-screen) classifies all six phases by narrative or by scoring, depending on the phase's data shape. Increment 2 (H_IdentityLoad_Direct) is bounded to v0.20 and v0.21 — the only phases that acquired R_cult data under the v1.5 two-channel design. Increment 3 (Phantom Brand Persistence) is bounded to v0.21, the substrate where the construct was empirically motivated and where the validity anchor was anchored. The boundary is methodology discipline, not data — extending Increments 2 and 3 retrospectively beyond their stated scope would require either retrospective channel re-mapping (which the program has explicitly disallowed) or post-hoc reference-vocabulary construction (which would compromise the validity anchor's pre-registration). Brand managers should read v0.16–v0.19 verdicts as v1.4-era authoritative within-phase results, with v1.6 framing added only where the retrospective scope supports it.

### ¶5 — Construct validity + behavioral correlate not claimed (~155 words)

> The synthesis claims measurability of the Presence component across five substrate families. It does not claim construct validity. Predictive validity against behavioral outcomes (whether AI Availability scores predict consideration, search, or purchase behavior), convergent validity across alternative panel constructions (whether other panel compositions yield the same brand-rank ordering), and discriminant validity against Mental and Physical Availability (whether AI Availability captures variance the existing constructs do not) are Phase 3 future work and are not established here. The consumer-behavior correlate of AI Availability is plausible on theoretical grounds — the Ehrenberg-Bass canon's logic implies that availability constructs should be load-bearing for category buying — but the present program has not measured the correlation. Brand managers should treat AI Availability as a measurement-program construct with anchored measurability and bounded scope, not as a predictor of downstream consumer behavior pending Phase 3 evidence.

---

## WHATS_NEXT

- **Section heading:** "What's next"
- **Source map:** synthesis §7.1 (Phase 3 validation), §7.2 (Phase 4 composite), §7.3 (substrate + language + panel-construction expansion axes)
- **Structure:** 5 paragraphs (vs. v21's 3-paragraph single-phase scope), structured as three planning timelines (v0.22+ near-term; Phase 3 multi-year; Phase 4 multi-year) plus expansion axes plus a brand-strategy-roadmap close

### ¶1 — v0.22+ prospective substrate expansion (~125 words)

> The immediate next deliverable is v0.22, the program's first prospective phase under the locked v1.6 protocol. Substrate selection is open: candidates include automotive (a substrate with a different IL-gradient shape — brand identity carries strong individual-purchase identity but the discovery surface is dominated by review-channel discourse), consumer electronics outside audio (where heritage, cult, and mass tiers may map cleanly to the standard panel design), or premium spirits (where editorial authority and cultural-cult dimensions both run strong). Each candidate would test v1.6's three increments prospectively against a substrate not in the present retrospective scope. Pre-registration locks the panel and verdict matrices before acquisition, as the program's standing discipline requires.

### ¶2 — Phase 3 construct validation (~130 words)

> Phase 3 is construct validation. Predictive validity against behavioral outcomes — whether AI Availability scores predict consumer behavior such as consideration, search, or purchase — is the discipline's primary validation criterion and the program's Phase 3 anchor. The Phase 3 design requires a behavioral-outcome dataset paired with AI Availability scores measured at the same brand × substrate boundary, against panel constructions held fixed for measurement comparability and varied for convergent-validity testing. Discriminant validity against Mental Availability and Physical Availability requires paired measurements of all three constructs against a common brand × substrate cohort. Both validation arcs sit in the Phase 3 pre-registration roadmap; neither is in the present synthesis's claim scope.

### ¶3 — Phase 4 six-component composite (~160 words)

> Phase 4 is the full six-component AIAS™ composite. The Tri-System framework names the composite as a 0–100 score across Presence (operationalized by the present synthesis), Ranking (which brand surfaces first), Consistency (how stable the ranking is across panel intermediaries), Coverage (how completely the panel surfaces the category's relevant brand set), Grounding (whether brand mentions are accompanied by category-relevant context), and Sentiment (how favorable the mention's affective framing is). The remaining five components ship under a Phase 4 successor program at the level of intent only; component-level prioritization, panel-design implications, and methodology successors will follow the same pre-registration discipline that v1.2 through v1.6 established for the Presence layer. The composite reaches a fully-measured 6.0 state only when all six components have been operationalized to the standard the Presence component reaches in the present synthesis.

### ¶4 — Cross-language + panel-construction sensitivity (~135 words)

> Cross-language replication is the construct's second expansion axis. Non-English-language substrate phases — Japanese, Spanish, Mandarin, and others selected on substrate-availability grounds — will test whether the construct's measurement procedure transfers across discourse-language boundaries with the panel-internal scoring discipline held fixed. Panel-construction sensitivity is the third axis: studies that hold substrate and methodology version fixed while varying the panel — substituting providers, varying panel size, testing single-provider panels against multi-provider panels — will supply the convergent-validity evidence base that Phase 3 construct validation requires. The three expansion axes (substrate, language, panel-construction) together carry the construct's empirical anchor base from the present five families into a sustained replication program under the program's standing pre-registration discipline.

### ¶5 — Brand-strategy roadmap (~150 words)

> For brand managers planning against the construct's evolution, three timelines matter. AIAS 1.0's Presence component is anchored on cosmetics and four other families as of May 2026; new substrate families ship at the program's pace under v1.6 lock. Phase 3 construct validation is multi-year work that establishes whether AI Availability scores predict downstream consumer behavior — until that work ships, brand managers should treat AI Availability as a measurable property of brand × substrate × panel triples without inferring behavioral consequences. Phase 4 composite expansion is the longest-horizon arc; the version-number arc 1.0 → 6.0 will track the measurement surface rather than architectural ambition. Brand managers consuming the report should plan against the present anchored claim and against the future-work claims as separate planning tracks, with the construct's evolution timeline as the resource-allocation input.

---

## Chunk 4 self-scan

**Word counts:**

- FINDING 05 (P5): ¶1 185 / ¶2 205 / ¶3 205 / ¶4 185 = **780 words**
- LIMITATIONS: ¶1 140 / ¶2 125 / ¶3 140 / ¶4 155 / ¶5 155 = **715 words**
- WHATS_NEXT: ¶1 125 / ¶2 130 / ¶3 160 / ¶4 135 / ¶5 150 = **700 words**
- **Chunk 4 total: ~2195 words**

**Voice register checks:**

- P5 ¶1 opens "Protocol v1.6 (SSRN 6816340, May 2026) shipped three increments..." — concrete artifact + concrete count, then increment names follow. ✓
- P5 ¶2 opens "Each increment found its first measured anchor in v0.21 cosmetics." — concrete linkage, then per-increment numbers. ✓
- P5 ¶3 opens "For the brand-strategy practitioner, v1.6's increments translate to vocabulary the prior framework versions could not provide." — brand-strategy framing, then specific vocabulary distinctions. ✓
- P5 ¶4 opens "AIAS™ 1.0 names the Presence component of the AIAS construct, not the full multi-component composite." — direct scope statement. ✓
- LIMITATIONS ¶1 opens "The reference panel is held fixed at the v0.17 six-slot specification..." — concrete constraint + specific panel slots. ✓
- LIMITATIONS ¶2 opens "Four of the five substrate families operated in English-language consumer-discovery environments." — concrete count. ✓
- LIMITATIONS ¶3 opens "Cell-classification limits surfaced through the e.l.f. Cosmetics out-of-cell Type 2 case..." — concrete case + explicit cross-finding ref. ✓
- LIMITATIONS ¶4 opens "The synthesis honors the v1.6-locked retrospective-scoring boundary without extension." — methodology constraint + immediate per-increment scope. ✓
- LIMITATIONS ¶5 opens "The synthesis claims measurability of the Presence component across five substrate families. It does not claim construct validity." — direct two-sentence scope statement. ✓
- WHATS_NEXT ¶1 opens "The immediate next deliverable is v0.22..." — concrete next milestone + substrate candidates with brand-strategy framing. ✓
- WHATS_NEXT ¶2 opens "Phase 3 is construct validation." — direct framing. ✓
- WHATS_NEXT ¶3 opens "Phase 4 is the full six-component AIAS™ composite." — direct framing. ✓
- WHATS_NEXT ¶4 opens "Cross-language replication is the construct's second expansion axis." — direct framing. ✓
- WHATS_NEXT ¶5 opens "For brand managers planning against the construct's evolution, three timelines matter." — brand-strategy framing + actionable structure. ✓

**Conventions:**

- ™ marked on first AIAS appearance in P5 ¶4 ("AIAS™ 1.0"), P5 ¶4 ("AIAS construct" — second mention unmarked), and WHATS_NEXT ¶3 ("AIAS™ composite"). Subsequent in-section uses unmarked per v21 per-section first-mention pattern. WHATS_NEXT ¶5 "AIAS 1.0" appears after the section's first marked mention — leave unmarked. Double-check at final assembly.
- Verdict labels (CONFIRMED, EMERGED, PARTIAL, FALSIFIED, REGIME-4-UNAVAILABLE-AT-RECOGNITION) preserved.
- Cross-finding references explicit where helpful: LIMITATIONS ¶3 references Finding 01 ¶3 + Finding 03 ¶4 for the e.l.f. case; P5 ¶2 implicitly references Finding 04 (IL Direct verdict numbers identical).
- SSRN citation discipline: SSRN 6816340 (v1.6 paper) referenced once in P5 ¶1 (methodology origin); SSRN 6810758 (v1.5 paper) not re-cited in this chunk (covered in P3 ¶1 of chunk 3 via "v1.5 specification").

**Cross-section consistency check:**

- P5 ¶2 numbers exactly match P4 ¶2 (Cell B +7.13 / CI [+4.75, +10.25]; Cell A −3.13 / CI [−6.00, −0.25]; Cell C +1.00 / CI [−0.50, +3.25]; Glossier R_phantom = 12; six off-panel brands cleared K = 6). ✓
- LIMITATIONS ¶3 e.l.f. cross-reference matches Finding 01 ¶3 (Cell C, R_cat = 1, R_cult = 9) and Finding 03 ¶4 implicit (Cell C drugstore/mass cell membership). ✓
- WHATS_NEXT ¶3 six composite components (Presence, Ranking, Consistency, Coverage, Grounding, Sentiment) match exactly STANDFIRST + EXEC_SUMMARY ¶1 + P5 ¶4. ✓

**Chunks 1–4 cumulative content volume:**

| Section | Words |
|---|---|
| STANDFIRST (chunk 1) | 105 |
| EXEC_SUMMARY (chunk 1) | 882 |
| PATTERNS P1 + P2 (chunk 2, post-fixes) | ~1465 |
| PATTERNS P3 + P4 (chunk 3, post-fixes) | ~1520 |
| PATTERNS P5 (chunk 4) | 780 |
| LIMITATIONS (chunk 4) | 715 |
| WHATS_NEXT (chunk 4) | 700 |
| **PATTERNS total** | ~3765 |
| **Content-module total (drafted chunks 1–4)** | ~6167 |

Outline §7 estimate was ~2275 lines for the content module. At ~50 chars/word average and ~80 chars/line wrapped, ~6167 words ≈ ~7700 char-lines ÷ ~50 chars/line ≈ ~155 wrapped lines plus Python wrapping (~3× multiplier from string-literal continuation) ≈ ~465 lines. **Well within the 1500–2200 D6 target band** — comfortable cushion for the remaining sections (COVER, LEAD_DECK, WHAT_WE_MEASURED, PROPOSITION_SCORING, PROPOSITION_DETAILS, CLOSING) to bring the total to the target.

**Remaining sections after chunk 4 lock** (to be drafted at content-module assembly time, not in chunk-review checkpoints):

- COVER (~30 lines)
- LEAD_DECK (~40 lines)
- WHAT_WE_MEASURED (~220 lines)
- PROPOSITION_SCORING (~110 lines)
- PROPOSITION_DETAILS (~280 lines)
- CLOSING (~50 lines)

These were not on Pablo's chunk-checkpoint list (chunks 1–4 covered the high-prose-risk sections). Recommend drafting at content-module assembly with a single final review pass rather than additional checkpoints.

**Holding for chunk 4 verdict. After approval, content module locks and the work order proceeds to:**

1. `reports/build_charts_aias_1_0_report.py` — thin builder for P2 phantom channel brand-style upgrade only
2. `reports/build_report_aias_1_0.py` — surgical fork of `reports/build_report_v21.py` per D5
3. Assembly of `reports/aias_1_0_content.py` from chunks 1–4 + drafting of COVER/LEAD_DECK/WHAT_WE_MEASURED/PROPOSITION_SCORING/PROPOSITION_DETAILS/CLOSING
4. Render PDF; pre-flight; OSF deposit
