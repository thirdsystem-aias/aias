# v0.18 Indie Fragrance — Kickoff Prompt

**Context:** This kicks off the v0.18 Indie Fragrance phase of the AIAS™ Presence Measurement research line. v0.17 Premium Kitchenware just shipped (SSRN 6802261, OSF v17/). v1.4 Methodology shipped (SSRN 6799479) and is now the canonical protocol citation. v0.18 is the deciding test of `H_IdentityLoad_moderator` per the joint verdict matrix that left v0.16/v0.17 at AMBIGUOUS.

You have full context from user memory and access to the project. Begin by acknowledging the v0.17 close-out state and the three forward actions v0.17 explicitly handed off to v0.18.

---

## What v0.18 is

The third leg of the Identity-Load moderator test, on a **higher-Identity-Load substrate than v0.16/v0.17 and entirely English-language**. Indie fragrance was pre-selected in v0.17's joint verdict matrix as the substrate that disambiguates between two readings of v0.17's Japanese cell collapse: (1) Identity Load does not moderate AI Availability, or (2) Western-language LLM training-data bias is large enough on cross-cultural substrates to swamp the Identity-Load signal.

v0.18's same-language design removes the cross-cultural confound. The substrate's higher Identity Load (fragrance selection is itself part of what the purchase accomplishes; perfume is a culturally and personally identity-bearing category) provides the IL gradient the moderator hypothesis predicts should produce stronger Regime 4 signature.

---

## Three explicit v0.17 → v0.18 forward actions

Carry these forward into the v0.18 pre-registration. The v0.17 SSRN paper §7.3 and v0.17 README §"Methodological findings" explicitly committed v0.18 to these:

1. **Panel over-provisioning for LLM-substrate attrition.** v0.17 pre-reg anticipated 1–3 brands of attrition under Trends-substrate Phase B; observed 5 brands of attrition under LLM-substrate Phase B (the substrate substitution committed in DEVIATIONS Entry 7, now canonical in v1.4). For a three-cell panel with worldwide C1 floor at n ≥ 12, cell sizes should be at least 6 brands each, ideally 7–8, so the worldwide pre-registered panel pre-floor is ~21–24. The American long-tail attrition (Field Company, Smithey EXCLUDED_E1a) suggests v0.18's lower-prominence brands need explicit anticipation.

2. **Same-language substrate for clean Identity-Load test.** Indie fragrance is entirely English-language on the consumer-discovery surface. The Japanese cell's confound that contaminated v0.17 does not apply. The Identity-Load gradient within indie fragrance can be tested on equal LLM-coverage terms across cells.

3. **Recognition × Recall dissociation as substrate property.** v0.18 Phase A and Phase B will be analyzed not only against the substantive Regime 4 hypothesis but also against the dissociation pattern. If the dissociation generalizes to a same-language substrate, v1.4's multi-component construct claim is strengthened; if the dissociation is specific to cross-cultural substrates, the claim narrows. This is a secondary hypothesis worth pre-specifying.

---

## Joint verdict matrix routing

The v0.16/v0.17 joint matrix landed at PARTIAL × FALSIFIED → AMBIGUOUS pending v0.18. v0.18's verdict combines with v0.16 (PARTIAL) and v0.17 (FALSIFIED) per a pre-registered three-leg joint matrix. The natural cell structure for v0.18:

- **CONFIRMED at v0.18:** Three-leg matrix lifts joint H_IdentityLoad_moderator from AMBIGUOUS to CONFIRMED (the higher-IL substrate produces the stronger Regime 4 signature the moderator predicts)
- **PARTIAL at v0.18:** Three-leg matrix routes to PARTIAL — the moderator may operate but its strength is bounded or substrate-specific
- **FALSIFIED at v0.18:** Three-leg matrix routes to FALSIFIED — Identity Load does not moderate AI Availability across this gradient
- **NULL at v0.18 (e.g., same C1 inadequacy mechanism):** Joint matrix routes to AMBIGUOUS-deferred → v0.19 with further substrate refinement

The pre-registered three-leg matrix must be specified at lock time, not after v0.18 outcomes are observed.

---

## Phase 1 — Substrate and panel design

Tasks for the first pre-reg draft round:

### Substrate definition

Indie fragrance is non-trivial to define. Operational definition options:

- **Niche/artisan + small-house:** Le Labo, Byredo, Diptyque, Maison Francis Kurkdjian, Frederic Malle, Aesop, Comme des Garçons, etc.
- **Pure indie (small-house only, no LVMH/Estée Lauder ownership):** D.S. & Durga, Régime des Fleurs, Heretic Parfum, Vyrao, Henry Rose, Ellis Brooklyn
- **Mass-prestige bridge:** Tom Ford, Chanel Les Exclusifs, Hermès Hermessence — these complicate the IL gradient

Decide on substrate scope before brand selection. The cleanest test is a same-IL-tier panel (all niche/artisan, no LVMH-owned major houses); the most interesting test is an IL-gradient panel (mass-prestige bridge brands + pure-indie + designer-niche, structured to produce the IL gradient within the panel).

### Panel design

Per the over-provisioning rule (v0.17 lesson):

- **Three cells, ≥6 brands each, worldwide n ≥ 21–24 pre-floor** (vs. v0.17's 16). Suggested cell stratification:
  - **Cell A: Designer-niche (medium-high IL).** Maison Francis Kurkdjian, Frederic Malle, Diptyque, Byredo, Le Labo, Tom Ford Private Blend, Hermès Hermessence
  - **Cell B: Indie/artisan (high IL).** D.S. & Durga, Régime des Fleurs, Heretic Parfum, Vyrao, Henry Rose, Ellis Brooklyn, Boy Smells
  - **Cell C: Mass-prestige (medium IL — comparison anchor).** Chanel No. 5, Tom Ford Black Orchid, Dior Sauvage, YSL Libre, Marc Jacobs Daisy, Calvin Klein One

  The IL gradient runs Cell C (medium) → Cell A (medium-high) → Cell B (high). Each cell sized to survive ~30–50% LLM-substrate attrition and still hit worldwide C1 ≥ 12.

- **No cross-cultural cells.** Cell membership is English-language-presence anchored; Japanese fragrance houses (Issey Miyake, Shiseido) excluded to avoid replicating v0.17's confound.

### Pivots and cascade ordering

Per v1.4 cascade protocol: each cell has a primary pivot + alternates in cascade order. Pivot must produce 6/6 C_P anchoring for the cell to proceed to Phase B. v0.17's Vermicular FAIL → Iwachu cascade shows the protocol works; ordering matters.

Recommended primary pivots (high-prominence anchors):

- **Cell A pivot:** Maison Francis Kurkdjian (or Le Labo as fallback)
- **Cell B pivot:** D.S. & Durga (or Byredo if relabelled as indie)
- **Cell C pivot:** Chanel No. 5

Alternates should descend in prominence within each cell.

### Reference panel

Same locked six-slot panel as v0.17:

- claude-opus-4-5, claude-sonnet-4-5, gpt-4o, gpt-4o-mini, gemini-2.5-flash, gemini-2.5-flash-lite

Provider model substitutions get documented in DEVIATIONS as encountered.

### Phase B category queries (same-language, English)

Modeled on v0.17's tradition-agnostic format:

- *q1:* "What are the best premium / niche / artisan fragrances? List several with descriptions."
- *q2:* "Recommend high-quality independent fragrance brands. Name several brands."
- *q3:* "What fragrances do industry insiders and perfumistas recommend? List several."

The exact wording deserves discussion — "indie" vs "niche" vs "artisan" vs "premium" each pull on different LLM-retrieval surfaces.

---

## Pre-registration structure

Mirror v0.17 pre-reg structure with v0.18-specific content. Sections:

1. **Substrate and panel** — operational definition of indie fragrance; cell stratification; brand registry locked.
2. **Hypotheses:**
   - `H_Regime4_indie_fragrance` (substantive): same C1/C2/C3 conditions as v0.17, calibrated to indie fragrance panel.
   - `H_IdentityLoad_moderator` (three-leg joint v0.16/v0.17/v0.18): three-leg joint verdict matrix specified ex-ante.
   - `H_Recognition_Recall_dissociation_generalization` (secondary, novel for v0.18): pre-registers whether the dissociation generalizes from cross-cultural Japanese-cell substrate to same-language fragrance substrate.
3. **Descriptive sensitivities** — US/worldwide divergence; per-cell n; per-cell ρ at cell n ≥ 5.
4. **Decision rules** — C1/C2/C3 verbatim from v0.17 with C1 floor recalibrated to ≥12 (same).
5. **Joint verdict matrix** — three-leg ex-ante, with cells for each combination of v0.16/v0.17/v0.18 outcomes.
6. **Borderline classifications** — for any indie fragrance brand whose substrate scope is ambiguous (e.g., Byredo's LVMH acquisition; Aesop's apparel-adjacent positioning), pre-register `borderline_classification: true, borderline_resolution_at: phase_b_topic_id`.

Lock at git commit before any acquisition. Tag `v0.18-prereg-r1`.

---

## Deliverables sequence (matches v0.17 publication workflow)

1. Pre-registration draft → review → lock at git commit (`v0.18-prereg-r1`)
2. Phase A acquisition + classification → Phase A lock (`v0.18-phase-a-locked`)
3. Phase B acquisition + measurement → Phase B lock (`v0.18-phase-b-locked`)
4. Canonical scoring + formal verdict document (`v0_18_verdict.md`)
5. Build chart pipeline (`scripts/build_charts_v18.py`) — likely same three-chart structure as v17: mention rate distribution, cell attrition, dissociation scatter
6. Brand-format report PDF (`reports/build_report_v18.py` + `reports/v18_indie_fragrance_content.py`) using ReportLab two-pass overlay
7. SSRN academic paper (`scripts/build_paper_v0_18.py`, pandoc+xelatex+Carlito)
8. OSF deposit at `osf/v18/` with README + manifest + data + figures + scripts
9. SSRN submission yields abstract ID; backfill into Tri-System MSI WP bibliography and v0.19 pre-reg

---

## Programmatic context to carry forward

All canonical references for v0.18 paper Methods section and pre-reg cross-references:

- **AI Availability foundational:** SSRN 6659000
- **AIAS Methodology citation chain:** v1.2 SSRN 6761698, v1.3 SSRN 6797679, v1.4 SSRN 6799479 (canonical pair extended to triple)
- **Immediate-prior phase:** v0.17 SSRN 6802261 (the joint matrix routes from this)
- **First leg of joint Identity-Load test:** v0.16 SSRN 6791999

OSF project: ec6wh; v0.18 deposit will be `osf/v18/`.

GitHub: thirdsystem-aias/aias; working branch likely `v0.11-phase3-pilot` (carry forward) or new `v0.18-substrate-test` branch — Pablo's call.

---

## Operating preferences (carried forward from v0.17)

- **Surgical precision over broad rewrites.** Scoped edits with verification before execution.
- **Single unified pipelines, no toggles.** Pre-reg lock at commit before measurement.
- **Two-stage commits.** Substantive change → backfill hash placeholders.
- **Trademark ™ on first prominent mention in formal documents only.**
- **Per-phase build files copy from prior phase with new prefix; prior phases untouched.**
- **DOCX editing workflow:** extract-text → unpack.py at /mnt/skills/public/docx/scripts/office/unpack.py → str_replace edits to /home/claude/unpacked/word/document.xml → pack.py with --original flag pointing to versioned local copy. Always cp from outputs to a versioned local copy before unpacking.
- **Pre-registration discipline is non-negotiable.** Every phase locks methodology at git commit before any data collection.

---

## Decisions to make in the first turn

These shape everything downstream and should be made before writing the pre-reg draft:

1. **Substrate scope:** pure-indie / designer-niche / mass-prestige / IL-gradient mix?
2. **Cell stratification rationale:** what makes A, B, C meaningfully different on the IL dimension?
3. **Brand panel composition:** 6/6/6 (worldwide n=18) or 7/7/7 (worldwide n=21) or 8/8/8 (worldwide n=24)?
4. **Pivot ordering per cell.**
5. **Phase B category query wording** — "indie" vs "niche" vs "artisan" vs "premium" framing.
6. **Branch strategy:** continue on `v0.11-phase3-pilot` or new branch?
7. **Optional Phase D scoring:** v0.17 paper skipped Phase D ρ because verdict resolved at C1. For v0.18, plan Phase D scoring from the start so the paper has ρ values regardless of which decision rule resolves the verdict.

Once these are nailed, the pre-reg draft can be written, locked, and tagged in a single working session.

---

## Open the chat with:

> "Confirmed v0.17 close-out state: SSRN 6802261 + 6799479 deposited, OSF v17/ live, joint H_IdentityLoad_moderator at AMBIGUOUS pending v0.18 resolution. Three v0.17→v0.18 forward actions absorbed: panel over-provisioning, same-language substrate, Recognition × Recall dissociation pre-specified. Ready to draft v0.18 pre-reg. First decision: substrate scope and cell stratification."

Then ask the seven first-turn decisions above as ask_user_input_v0 questions, batched.
