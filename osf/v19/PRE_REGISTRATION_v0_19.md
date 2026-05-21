# PRE_REGISTRATION v0.19 — C3 Rescue on Audiophile Headphones Substrate

**Program:** AIAS™ Presence Measurement Protocol
**Methodology base:** Protocol v1.4 (Recognition × Recall Decomposition; SSRN 6799479)
**Phase:** v0.19
**Pre-reg revision:** r1
**Pre-reg tag (proposed):** `v0.19-prereg-r1`
**Pre-reg commit:** `<COMMIT_HASH_TBD>` (assigned at git lock)
**Branch:** `v0.19-c3-rescue`
**OSF deposit location:** `osf.io/ec6wh/v19/`
**Author:** Pablo Ulpiano González Castro
**Date drafted:** May 2026

---

## §1 — Substrate definition and selection rationale

### 1.1 Substrate

The v0.19 substrate is **audiophile headphones**, defined operationally as over-ear and on-ear headphones marketed and enthusiast-recognized for music-listening fidelity, sampled across two cells split by audiophile headphone product-line emergence (Heritage: pre-2008 product line; Boutique: post-2008 product line). The substrate is English-language-anchored throughout; cross-cultural exposure is bounded to two pre-flagged brands (Stax, HiFiMan) and managed via a pre-registered robustness analysis.

### 1.2 Design pressure — what v0.18 left unresolved

The v0.19 design responds to three named limits from v0.18 (SSRN 6806558, §4.4), prioritized through the AIAS™ 1.0 critical-path lens:

1. **C3 ranking coherence test was structurally degenerate on v0.18 substrate.** Per-cell Spearman ρ between Phase A C_P score and Phase B mention rank requires within-cell variance in *both* Recognition *and* Recall. v0.18's IL-gradient design produced ceiling effects in Cell A (7/8 brands tied at C_P = 6/6), floor effects in Cell B (7/8 brands tied at 0 mentions), and cascade-exhaustion variance in Cell C. C3 has never been substantively cleared in the program. AIAS™ 1.0's canonical methodology layer (Protocol v1.4) ships v1.4's central within-cell variance test unverified unless v0.19 clears it.

2. **Recognition × Recall dissociation requires a third substrate-family anchor.** The v1.4 multi-component construct rests on the v0.17 Iwachu case (1 case, cross-cultural Japanese cell) and the v0.18 indie fragrance set (9 cases, English-language fragrance substrate). A third substrate family widens the empirical anchor base.

3. **Cultural-footprint Recall channel** surfaced as v0.18 §4.3 sensitivity finding (Tom Ford, Chanel, Dior surfacing in Phase B despite failing the niche-fragrance Recognition probe). AIAS™ 1.0 should not ship silent on this phenomenon; v0.19 collects the data preregisterably as descriptive sensitivity.

The IL moderator question — at PARTIAL across the v0.16 × v0.17 × v0.18 three-leg joint — is intentionally deferred for v0.19. It is not on the AIAS™ 1.0 critical path and can ship as a documented limitation ("operates with substrate-specific qualifications across three tested substrates; operating range to be characterized in v0.20+"). v0.19 trades the moderator test for the C3 rescue.

### 1.3 Why audiophile headphones

Three substrate criteria and how the substrate satisfies each:

**Criterion A — within-cell variance in Recognition AND Recall.** The audiophile headphone category has a multi-decade-deep boutique surface (ZMF, Spirit Torino, Meze, Dan Clark Audio) that is enthusiast-indexed but not mass-indexed, sitting alongside heritage brands (Sennheiser, Audeze, Focal) that are broadly indexed across both audiophile and mainstream surfaces. The variance shape v0.18 lacked is structurally present in this substrate.

**Criterion B — sharp category-anchored vs. cultural-footprint surface split** (required for H_CulturalFootprint sensitivity). Category-anchored frames ("best audiophile headphones") load on Sennheiser HD800S, Focal Utopia, HiFiMan Susvara, Audeze LCD line. Cultural-footprint frames ("famous headphone brands") load on a partially-disjoint set: Bose, Beats, AirPods Max, Sony WH-1000XM. The two discovery surfaces operate near-orthogonally on the same substrate.

**Criterion C — English-language anchored with bounded cross-cultural risk.** The audiophile category distributes across German (Sennheiser, Beyerdynamic), American (Audeze, Grado, Dan Clark Audio, ZMF), Japanese (Stax, Audio-Technica, Final Audio, Sony, Denon), Chinese (HiFiMan), French (Focal), and Romanian (Meze) houses. All have extensive English-language audiophile-press presence (Stereophile, Inner Fidelity, Audio Science Review, Head-Fi). Cross-cultural confound risk is bounded; pre-registered robustness analysis (Rule 6) handles the residual.

### 1.4 Why not coffee equipment or specialty board games

**Coffee equipment** was runner-up. Italian-brand concentration (Gaggia, Rancilio, La Marzocco, Lelit, ECM, Profitec, Bezzera all Italian-engineered) reintroduces cross-cultural-confound exposure the program already paid for in v0.16 (Japanese / French knives) and v0.17 (Japanese kitchenware). For a phase whose design pressure is C3 rescue, accepting renewed cross-cultural risk is the wrong trade.

**Specialty board games** were ruled out on two grounds: Recognition saturation risk (modern designer games heavily LLM-indexed via the BoardGameGeek corpus), and brand-vs-title analytic ambiguity (Catan, Wingspan, and Gloomhaven are titles, not brands; pivoting to publishers would change the analytic frame).

---

## §2 — Panel, reference panel, and protocol specifications

### 2.1 Brand registry (n = 16, locked at pre-reg)

**Cell A — Heritage audiophile** (audiophile headphone product line predates 2008):

| Brand | Country | Founded | Notes |
|---|---|---|---|
| Sennheiser | Germany | 1945 | HD-series (HD600 / HD650 / HD800S) flagship |
| Beyerdynamic | Germany | 1924 | DT / Tesla flagship |
| Denon | Japan | 1910 | AH-D7000 → D9200 audiophile line |
| Grado | USA | 1953 | RS / PS / Statement series |
| Sony | Japan | 1946 | MDR-R10 legacy → MDR-Z1R flagship |
| Audio-Technica | Japan | 1962 | ATH-W / AD / R series |
| Stax | Japan | 1938 | SR-series electrostatics (CROSS-CULTURAL FLAG) |
| Koss | USA | 1958 | ESP-95X + Porta Pro legacy |

**Cell B — Boutique / modern audiophile** (audiophile headphone product line post-2008):

| Brand | Country | Founded | Notes |
|---|---|---|---|
| Audeze | USA | 2008 | LCD-series planars |
| HiFiMan | China | 2007 | Susvara / HE1000 / Arya line (CROSS-CULTURAL FLAG) |
| Focal | France | 1979 | BORDERLINE — company 1979, headphone debut 2012 |
| Meze | Romania | 2009 | Empyrean / Elite flagship |
| ZMF Headphones | USA | ~2011 | Verite / Atrium / Caldera handcrafted |
| Spirit Torino | Italy | ~2011 | Pulsar / Valkyria flagship |
| Final Audio | Japan | 1974 | BORDERLINE — company 1974, audiophile renaissance post-2010 |
| Dan Clark Audio | USA | 2013 | Stealth / Expanse flagship |

### 2.2 Classification rule (pre-registered)

A brand classifies **Heritage** (Cell A) if its audiophile headphone *product line* predates 2008. A brand classifies **Boutique** (Cell B) if its audiophile headphone product line emerged or peaked post-2008. Company founding date is not the criterion. Focal (1979 company; post-2012 audiophile headphone line) and Final Audio (1974 company; post-2010 audiophile renaissance) classify as Boutique under this rule. Sony's audiophile headphone product line predates 2008 (MDR-R10 in 1989), so Sony classifies Heritage despite carrying a substantial post-2008 consumer-electronic line (WH-1000XM series) that loads on cultural-footprint frames.

### 2.3 Substitution decisions made at pre-reg

**AKG removed from Cell A short-list; Denon substituted.** AKG is Samsung-owned since 2016. The author's COI declaration names Samsung; including AKG would invite the kind of reviewer suspicion AIAS™ 1.0 does not need to absorb. Denon carries comparable heritage stature (founded 1910; AH-D7000 → D9200 audiophile line) and removes the question. Decision rationale recorded here for audit trail.

**Final Audio retained with borderline flag; Abyss Headphones available as swap candidate.** Final Audio's post-2010 audiophile-line dating sits cleanly under the product-line rule, and v0.18's borderline-classification protocol (which handled Le Labo / Frederic Malle / Byredo) is a tested mechanism. If reviewer pushback at SSRN review challenges the Final Audio classification, Abyss Headphones (USA, 2013, AB-1266 / Diana flagship) is the documented swap candidate. Under the DEVIATIONS Rule 5 (borderline classification stands), no swap occurs post-acquisition; the swap candidate is for revision history only.

### 2.4 Reference panel (locked six-slot panel, unchanged from v0.16 / v0.17 / v0.18)

| Provider | Model identifier |
|---|---|
| Anthropic | claude-opus-4-5 |
| Anthropic | claude-sonnet-4-5 |
| OpenAI | gpt-4o |
| OpenAI | gpt-4o-mini |
| Google | gemini-2.5-flash |
| Google | gemini-2.5-flash-lite |

Provider model deprecation between pre-reg lock and acquisition is handled per DEVIATIONS Rule 2.

### 2.5 Phase A protocol — Recognition (C_P probe per Protocol v1.4 §6.4)

**C_P probe template (verbatim, locked):**

> *"Is the brand [BRAND_NAME] commonly recognized as a brand of audiophile headphones? Answer yes or no."*

For each of the 16 registry brands, the probe is sent to each of the six reference panel models. The brand's C_P score is the count of recognition-positive responses across the panel (range 0..6).

Phase A total acquisition: 16 brands × 6 panel models = **96 queries**.

Cascade rule per Protocol v1.4 §6.4 (five-stage pivot-validation): the first brand in cascade order achieving C_P = 6/6 becomes the cell pivot. Cascade order is the order brands are listed in §2.1, top-to-bottom per cell.

### 2.6 Phase B protocol — Recall (six-frame battery)

Three category-anchored frames (load-bearing on H_C3 and H_Dissociation):

- **q1 (audiophile):** *"What are the best audiophile headphones? List several with descriptions."*
- **q2 (enthusiast):** *"Recommend high-quality headphones for serious music listening. Name several brands."*
- **q3 (reference):** *"What headphones do audiophiles and reviewers consider reference-grade? List several."*

Three cultural-footprint frames (sensitivity-only on H_CulturalFootprint, NOT load-bearing on the verdict matrix):

- **q4 (famous):** *"What are the most famous headphone brands?"*
- **q5 (popular):** *"What headphone brands are most well-known among general consumers?"*
- **q6 (iconic):** *"Which headphone brands have the strongest cultural recognition?"*

Each frame is sent to each of the six reference panel models. For each (frame, model) response, all 16 registry brands are scanned for mention presence under v1.4 canonical brand-mention detection rules (case-insensitive, accent-stripped, possessive-aware, first-occurrence-wins de-duplication). Rank within enumerated response lists is recorded for Phase D ρ analysis.

Phase B total acquisition: 16 brands × 6 frames × 6 panel models = **576 observations**, of which 288 (q1–q3) are load-bearing and 288 (q4–q6) are sensitivity-only.

---

## §3 — Pre-registered hypotheses

Three hypotheses, tested orthogonally.

### 3.1 H_C3_Within_Cell_Variance (PRIMARY, load-bearing)

*For at least one of the two cells, per-cell Spearman ρ between Phase A C_P score and Phase B category-anchored mention count meets the C3 threshold at post-attrition n ≥ 5.*

The hypothesis is intentionally weaker than v0.18's "≥ 2 of 3 cells" formulation because the two-cell design accepts redundancy rather than triangulation: one clean cell is sufficient to substantively clear C3 for v1.4 shipping. PARTIAL routing (exactly one cell clears) is treated as substantive clearance for AIAS™ 1.0's canonical methodology layer; PASS routing (both cells clear) is the stronger evidence.

### 3.2 H_Recognition_Recall_Dissociation_Replication (SECONDARY, load-bearing)

*Iwachu-pattern cases (Phase A C_P ≥ 5/6 ∧ Phase B category-anchored mention rate ≤ 2/18) replicate on the headphone substrate at a count widening the v1.4 empirical anchor base beyond v0.17 (1 case, Japanese cell) and v0.18 (9 cases, English-language fragrance).*

Replication at any non-zero count on the third substrate family contributes meaningfully to the multi-component construct claim; threshold matrix in §4.

### 3.3 H_CulturalFootprint_Dissociation_Sensitivity (DESCRIPTIVE, NOT load-bearing)

*Within each cell, brands satisfying either of two dissociation patterns are documented descriptively for v1.5 methodology development.*

- **Type 1 — Category-channel-preferred:** [category-anchored mentions ≥ 5/18] ∧ [cultural-footprint mentions ≤ 2/18]. Expected for boutique-tier brands with strong audiophile-discourse presence but limited mainstream cultural footprint.
- **Type 2 — Cultural-channel-preferred:** [category-anchored mentions ≤ 2/18] ∧ [cultural-footprint mentions ≥ 5/18]. The v0.18 Tom Ford / Chanel / Dior pattern, predicted here for heritage brands with strong consumer-electronic cultural footprint (Sony WH-1000XM consumer line is the primary candidate; Bose-adjacent presence may surface as well).

This hypothesis returns no verdict against the matrix. It produces a documented case list and pattern counts for v1.5 methodology paper.

---

## §4 — Decision rules and numerical thresholds (locked at pre-reg)

### 4.1 C1 — Panel adequacy

- **Worldwide:** n ≥ 12 post-attrition (n = 16 acquisition; 25% attrition margin).
- **Per-cell:** n ≥ 5 post-attrition.

Justification: Carries forward from v0.18. With n = 16 acquisition, the 25% attrition margin holds without v0.18's 50% margin because headphone-substrate LLM coverage density is higher than indie fragrance. Per-cell n ≥ 5 is required for Spearman ρ to have meaningful rank distinction.

### 4.2 C2 — Within-cell variance adequacy (NEW operationalization for v0.19)

For each cell post-attrition:

- Modal share of C_P distribution **< 0.50** (i.e., the most common C_P value is held by fewer than 50% of cell brands), **AND**
- Modal share of category-anchored mention-count distribution **< 0.50**.

Justification: v0.18 Cell A had 7/8 brands tied at C_P = 6/6 (modal share = 0.875) — would FAIL. Cell B had 7/8 brands tied at 0 mentions (modal share = 0.875) — would FAIL. The C2 check operationalizes "engineered for variance, not for concentration." Tighter thresholds (< 0.40) would over-restrict; looser (< 0.60) would tolerate the v0.18 degeneracy.

### 4.3 C3 — Ranking coherence (carries forward from v0.18; CI requirement added)

Per cell, post-attrition n ≥ 5:

- Spearman ρ between Phase A C_P score and Phase B category-anchored mention count **≥ 0.50**, **AND**
- 95% bootstrap CI lower bound on ρ **> 0.20** (10,000 brand-level resamples, percentile method).

Justification: ρ ≥ 0.50 carries forward from v0.18 unchanged (program commitment against threshold-loosening). The bootstrap CI is *tightening*, not loosening: it adds robustness against the small-n (n = 8 per cell) point-estimate noise that is unavoidable at this panel size. CI lower bound > 0.20 is calibrated as a "rules out near-zero effect" floor; tighter (> 0.30) would over-restrict at n = 8.

### 4.4 Iwachu-pattern threshold (carries forward unchanged from v0.17 / v0.18)

A brand qualifies as an Iwachu-pattern case if:

- Phase A C_P **≥ 5/6**, **AND**
- Phase B category-anchored mention rate **≤ 2/18** (across q1–q3 × 6 panel models).

### 4.5 H_Dissociation_Replication verdict-matrix thresholds

| Case count (of n = 16 panel) | Verdict |
|---|---|
| ≥ 5 | REPLICATED |
| 1 — 4 | PARTIAL |
| 0 | NOT_REPLICATED |

Justification: v0.18 prevalence was 9/24 = 37.5%; v0.19 REPLICATED threshold (≥ 5/16 = ≥ 31%) is calibrated for comparable prevalence on a smaller panel. A single Iwachu-pattern case on the headphone substrate is still empirical extension of the v1.4 anchor base to a third substrate family — PARTIAL starts at 1, not 0.

### 4.6 Cultural-footprint K threshold (sensitivity)

K = **5/18** for "non-trivial Recall" in either channel. The threshold screens out single-model or single-frame artifacts. Symmetric with the Iwachu mentions floor (≤ 2/18 = "near-zero"; ≥ 5/18 = "non-trivial").

### 4.7 Cross-cultural robustness (DEVIATIONS Rule 6)

Per-cell C3 ρ is computed twice:

- **Primary:** Full-cell ρ (all 8 brands per cell). Drives the verdict.
- **Robustness:** ρ recomputed excluding Stax (Cell A) and HiFiMan (Cell B), reducing each cell to n = 7. Reported as documented characterization.

Threshold: if |Δρ| **< 0.10** between primary and robustness across both cells, cross-cultural risk is *bounded* for v0.19. If |Δρ| ≥ 0.10 in either cell, the cross-cultural confound is *substantive* and recorded as documented limitation for the AIAS™ 1.0 substrate-coverage section.

---

## §5 — Verdict matrices (ex-ante)

### 5.1 H_C3_Within_Cell_Variance — primary verdict matrix

| Cell A C3 status | Cell B C3 status | Verdict |
|---|---|---|
| CLEAR | CLEAR | **PASS** |
| CLEAR | FAIL (passes C2) | **PARTIAL** |
| FAIL (passes C2) | CLEAR | **PARTIAL** |
| FAIL (passes C2) | FAIL (passes C2) | **FALSIFIED** |
| C1 inadequate (n < 12) | — | **UNDETERMINED** |
| C2 fails in either cell | — | **UNDETERMINED** |

CLEAR = ρ ≥ 0.50 ∧ CI lower bound > 0.20. FAIL = C3 not met but C2 cleared (cell has variance but no rank coherence). UNDETERMINED routings preserve the substantive interpretation: failure to clear C2 means the substrate did not expose C3, not that C3 is false.

### 5.2 H_Recognition_Recall_Dissociation_Replication — secondary verdict matrix

| Case count | Verdict | Interpretation |
|---|---|---|
| ≥ 5 | REPLICATED | Third-substrate-family anchor established; v1.4 multi-component construct widened to ≥ 3 substrate families |
| 1 — 4 | PARTIAL | Replication evidence at lower prevalence than v0.18 |
| 0 | NOT_REPLICATED | Pattern absent on headphone substrate; documented limit for v1.4 substrate coverage |

### 5.3 H_CulturalFootprint_Dissociation_Sensitivity — descriptive output

No verdict. Output is a case list:

- **Type 1 cases (category-channel-preferred):** Brand list with [C_P, category-anchored mention count, cultural-footprint mention count]
- **Type 2 cases (cultural-channel-preferred):** Same list format

Pattern counts per cell. Used as input to v1.5 methodology paper for formalization decisions.

---

## §6 — DEVIATIONS protocol — carryforward and new rules

The DEVIATIONS protocol carries forward from v0.16 / v0.17 / v0.18. Five rules carry; one is new for v0.19.

**Rule 1 — Panel lock.** The 16-brand registry is fixed at pre-reg commit. No substitution post-lock under any circumstance. Brands with C_P = 0/6 remain in panel with measured score.

**Rule 2 — Provider model deprecation.** If any panel model is deprecated between pre-reg lock and acquisition, the protocol substitutes the closest-version successor model and opens a DEVIATIONS entry documenting (a) substituted model identity, (b) acquisition-date provider state, (c) impact assessment.

**Rule 3 — Recognition-floor cascade exhaustion.** If a cell's Phase A cascade exhausts without C_P = 6/6 anchor (the v0.18 Cell C precedent), the result is documented as substrate-level Recognition pattern. Cell alternates are NOT invoked. The substantive finding stands. Cell still feeds C3 analysis at measured C_P values.

**Rule 4 — Within-cell C2 variance failure (NEW for v0.19).** If a cell post-acquisition fails C2 (modal share ≥ 0.50 on Recognition or Recall), the cell is flagged as variance-degenerate and routes the H_C3 verdict to UNDETERMINED. Panel is NOT substituted; the substantive finding ("substrate produces ceiling/floor effect in cell X") stands and is documented in the v0.19 SSRN paper Limits section.

**Rule 5 — Borderline classification stands.** Focal (Cell B, headphone-line dating per §2.2) and Final Audio (Cell B, audiophile renaissance per §2.2) retain pre-registered classifications regardless of post-acquisition data shape. No retroactive reclassification.

**Rule 6 — Cross-cultural robustness analysis required.** Stax / HiFiMan exclusion analysis per §4.7 is required regardless of full-cell C3 outcome. Δρ reported in primary results; documented limit if |Δρ| ≥ 0.10.

---

## §7 — Pipeline and acquisition plan

### 7.1 Pre-reg lock

This document committed to branch `v0.19-c3-rescue`, tagged `v0.19-prereg-r1` at commit `<COMMIT_HASH_TBD>`. Pre-reg artifacts (this file + locked brand registry CSV + locked probe template files) deposited at `osf.io/ec6wh/v19/` prior to any Phase A API call.

### 7.2 Acquisition order

1. **Phase A — Recognition.** 96 queries (16 brands × 6 panel models). Cell A cascade-order first, then Cell B cascade-order. Single acquisition pass.
2. **Phase B — Recall.** 576 observations (16 brands × 6 frames × 6 panel models). Frames q1–q3 (category-anchored, load-bearing) acquired first; q4–q6 (cultural-footprint, sensitivity) acquired second.
3. **Phase C — Scoring.** Pipeline scripts modeled on v0.18 `score_v18.py`, refactored for v0.19's two-cell design and v1.4-canonical framework. Outputs: per-cell C2 status, per-cell C3 ρ with bootstrap CI, dissociation case lists (load-bearing and sensitivity), cultural-footprint Type 1 / Type 2 outputs, cross-cultural robustness ρ. No scoring code is read or run against acquisition data before Phase B closes.

### 7.3 Post-acquisition shipping

Per the established per-phase workflow:

1. **Brand-format report PDF.** Third System™ format, drawing on v0.18 report template.
2. **SSRN academic paper.** Title-page block + abstract + body + Declarations / COI / Data availability.
3. **OSF deposit.** README + MANIFEST + Phase A + Phase B data + registries + figures + scoring code + DEVIATIONS log.
4. **SSRN submission.** Abstract ID issued; cross-cited in v0.20 and v1.5 bibliographies.

No technical scaffolding (build scripts, OSF assembly, paper template) is committed until acquisition completes and verdicts route. Pre-reg lock is the only artifact that ships before Phase A.

---

## Appendix A — Revision history

**r1 (this version):** Initial pre-reg lock. Substrate selected (audiophile headphones, Heritage × Boutique two-cell). Panel composed (n = 16). Hypotheses specified (H_C3 primary, H_Dissociation secondary, H_CulturalFootprint sensitivity). Numerical thresholds locked (C1, C2, C3 with bootstrap CI, Iwachu-pattern, dissociation counts, cultural-footprint K, cross-cultural robustness). DEVIATIONS protocol carried forward from v0.16 / v0.17 / v0.18 with Rule 4 added for within-cell variance failure.

---

## References

González Castro, P. U. (2026a). AI Availability — A Third System in Brand Availability Theory. *SSRN Working Paper*. https://ssrn.com/abstract=6659000

González Castro, P. U. (2026b). The AIAS Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy (v1.2). *SSRN Working Paper*. https://ssrn.com/abstract=6761698

González Castro, P. U. (2026c). The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification (v1.3). *SSRN Working Paper*. https://ssrn.com/abstract=6797679

González Castro, P. U. (2026d). The AIAS Presence Measurement Protocol: Recognition × Recall Decomposition and Multi-Component AI Availability (v1.4). *SSRN Working Paper*. https://ssrn.com/abstract=6799479

González Castro, P. U. (2026e). Regime 4 Boundary and Discourse-Language Carryforward on the Kitchen-Knives Substrate (v0.16). *SSRN Working Paper*. https://ssrn.com/abstract=6791999

González Castro, P. U. (2026f). Panel Inadequacy and Recognition × Recall Dissociation on the Premium Kitchenware Substrate (v0.17). *SSRN Working Paper*. https://ssrn.com/abstract=6802261

González Castro, P. U. (2026g). Identity-Load Moderator Test and Recognition × Recall Dissociation Generalization on an English-Language Indie Fragrance Substrate (v0.18). *SSRN Working Paper*. https://ssrn.com/abstract=6806558

Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The Preregistration Revolution. *Proceedings of the National Academy of Sciences*, 115(11), 2600–2606.

---

## Declarations

**Declaration of interest.** The author is employed by Samsung Electronics America (Director, Corporate Brand Creative and Governance). The AIAS™ Presence Measurement Protocol and the work specified here are the author's independent academic research, conducted outside the scope of employment, in the author's role as faculty at the School of Visual Arts MPS Branding Program and founder of Third System™. Samsung had no role in the design of this pre-registration. Note: AKG (Samsung-owned since 2016) was considered for Cell A inclusion on substantive heritage-audiophile grounds and substituted with Denon to avoid any appearance of conflict; substitution rationale recorded in §2.3 above.

**Funder.** Self-funded.

**Ethics.** Not applicable; no human subjects. The research uses publicly accessible LLM APIs queried with non-personal, category-anchored prompts.

**Trademark notice.** AIAS™ and Third System™ are trademarks of the research program.

<!-- End PRE_REGISTRATION_v0_19.md r1 -->
