# AIAS™ Presence Measurement Protocol — v0.20 Pre-Registration

**Phase:** v0.20 (Skincare; IL-gradient design)
**Protocol version:** v1.5 (SSRN 6810758) — first prospective phase under v1.5
**Working title:** *Type 2 Emergence and First Prospective v1.5 C2 Calibration on a Skincare IL-Gradient Substrate*
**Working subtitle:** *AIAS™ Presence Measurement Protocol, v0.20 — Fourth Substrate Family; Type 2 Quadrant Test*
**Author:** Pablo Ulpiano González Castro
**Pre-registration revision:** r1
**Lock target:** git tag `v0.20-prereg-r1` on branch `v0.20-skincare-il-gradient`; OSF deposit at osf.io/ec6wh/v20/
**Status at this draft:** Pre-acquisition. No Phase A or Phase B data exists.

---

## §1. Phase position and mission

### §1.1 Position in empirical sequence

v0.20 is the seventh acquisition phase in the AIAS™ Presence Measurement Protocol and the first prospective phase pre-registered against the v1.5 (SSRN 6810758) numerical thresholds. The phase sits in the empirical sequence as:

| Phase | Substrate | SSRN | Protocol version exercised |
|---|---|---|---|
| v0.16 | Kitchen knives | 6791999 | v1.2 (AI Presence × Google Trends) |
| v0.17 | Premium kitchenware (incl. Japanese cell) | 6802261 | v1.4 (Recognition × Recall, retrospective anchor) |
| v0.18 | Indie fragrance | 6806558 | v1.4 (first generalization; r4 numerical lock) |
| v0.19 | Audiophile headphones | 6809182 | v1.4 (within-family replication) |
| **v0.20** | **Skincare** | **(this paper)** | **v1.5 (first prospective)** |

### §1.2 Mission

v0.20 pursues four objectives, ordered by load-bearing weight on AIAS™ 1.0:

1. **Probe the Type 2 (cultural-channel-preferred) quadrant of the v1.5 dissociation framework.** Type 2 cases (R_cat ≤ 2/18 ∧ R_cult ≥ 5/18) have zero empirical observations across v0.17–v0.19. The Type 2 quadrant is currently a *predicted but unpopulated* region of the construct space. v0.20 selects a substrate (celebrity-DTC skincare) where the construct predicts Type 2 should emerge if the cultural-footprint Recall channel operates as theorized.
2. **First prospective test of the v1.5 C2 multi-statistic rule** (distinct C_P values ≥ 3 ∧ modal share ≤ 0.625). The rule was calibrated retrospectively against joint v0.18 + v0.19 data; v0.20 is the first phase to lock it into pre-registration before acquisition. Either pass or fail behavior at the v1.5 thresholds is informative.
3. **Generalize the v1.4/v1.5 multi-component construct to a fourth substrate family.** The cumulative anchor base spans three families (Japanese kitchenware, indie fragrance, audiophile electronics). Skincare is the fourth and the headline cross-substrate-family claim for AIAS™ 1.0.
4. **Extend the H_IdentityLoad_moderator joint to a fourth leg.** The v0.16/v0.17/v0.18 three-leg joint returned PARTIAL (v0.18 SSRN 6806558 §3.5). v0.20 contributes the fourth leg. (v0.19 is excluded from the IL joint because v0.19 was a uniform-IL design.)

---

## §2. Substrate definition and IL-gradient design

### §2.1 Substrate

Skincare. The substrate is selected on three grounds:

1. **Type 2 hunting power.** The category contains a populous celebrity-DTC tier (Rare Beauty, Rhode, Fenty Skin, Drunk Elephant, Goop, Glossier, Augustinus Bader, Tower 28) whose brand identities are heavily cultural and whose canonical-retrieval positioning is plausibly weak. If Type 2 exists, this is the cell that should produce it.
2. **Three-tier IL stratification on the consumer-discovery surface.** Skincare admits a cleaner low → medium → high IL gradient than any prior substrate, spanning a wider IL range (clinical dermatology → prestige acquisition → celebrity identity statement). This gives the H_IdentityLoad_moderator joint a stronger fourth leg than v0.18 afforded.
3. **English-language anchored.** No cross-cultural confound. All cells are sampled from the same LLM-coverage baseline.

### §2.2 IL-gradient design

| Cell | IL tier | Identity function | Substrate role |
|---|---|---|---|
| **A — Prestige** | Medium | Status / signaling: La Mer-tier acquisition is part of what the purchase accomplishes | Middle comparator |
| **B — Celebrity DTC / cult** | High | Identity statement: brand is the identity; perfumistas-equivalent for skincare | **Type 2 hunting cell** |
| **C — Clinical / dermatologist-recommended** | Low | Functional: eczema treatment, barrier repair, retinol regimen — selection separable from product identity | Canonical-retrieval baseline |

The IL stratification is monotonic C → A → B (low → medium → high). The C → B span is wider than the v0.18 fragrance design (medium → medium-high → high) and substantially wider than v0.19 (uniform-IL). This is the design's primary contribution to the H_IdentityLoad_moderator joint.

---

## §3. Brand registry (LOCKED)

Pre-floor n = 24 worldwide (8 per cell). C1 floor n ≥ 12 is satisfied with 50% LLM-substrate attrition headroom.

### §3.1 Cell A — Prestige (medium IL)

1. Estée Lauder
2. Lancôme
3. La Mer
4. Sisley
5. Dior Beauty
6. Chanel Beauty
7. La Prairie
8. Clé de Peau Beauté

### §3.2 Cell B — Celebrity DTC / cult (high IL, Type 2 hunting cell)

1. Rare Beauty (Selena Gomez)
2. Rhode (Hailey Bieber)
3. Fenty Skin (Rihanna; LVMH/Kendo) — borderline; see §3.4
4. Goop (Gwyneth Paltrow)
5. Drunk Elephant (Shiseido) — borderline; see §3.4
6. Glossier
7. Augustinus Bader
8. Tower 28

### §3.3 Cell C — Clinical / dermatologist-recommended (low IL)

1. SkinCeuticals
2. La Roche-Posay
3. Paula's Choice
4. CeraVe
5. The Ordinary (EL/Deciem) — borderline; see §3.4
6. Cetaphil
7. Eucerin
8. Bioderma

### §3.4 Borderline classifications (pre-registered ex-ante)

Per the v0.18 §2.2 conglomerate-ownership precedent (Le Labo, Frederic Malle, Byredo retained in their identity-aligned cell despite EL/LVMH ownership), the following v0.20 brands carry conglomerate ownership but are classified by **identity-signal positioning** on the consumer-discovery surface:

| Brand | Conglomerate parent | Identity-signal cell | Rationale |
|---|---|---|---|
| Fenty Skin | LVMH / Kendo | B | Celebrity-founder identity (Rihanna) is the primary positioning |
| Drunk Elephant | Shiseido | B | Cult / "clean-clinical" indie identity retained post-acquisition |
| The Ordinary | EL / Deciem | C | Category-recognition (clinical actives, derm-recommended) is the primary classifier |
| Rare Beauty | (LVMH-adjacent; Sephora-led distribution) | B | Celebrity-founder identity (Selena Gomez) is the primary positioning |

All four are subject to retrieval-frame resolution in Phase B; their cell assignment is locked but their canonical-retrieval pattern will be examined in §3.4 of the eventual SSRN paper.

### §3.5 Alternates (DEVIATIONS Rule 5)

Up to 5 alternates per cell, invoked only on **substrate-level mismatch** (e.g., LLM-substrate failure-by-name-change, structural acquisition restructure), **not** on Phase A pivot-cascade exhaustion. The v0.18 Cell C precedent — cascade exhaustion is treated as substantive finding, not alternate-trigger — applies in full.

**Cell A alternates:** Guerlain (skincare line), Givenchy Beauty, Tom Ford Beauty, Armani Beauty, Helena Rubinstein.
**Cell B alternates:** Kylie Skin, KKW Beauty (skincare line), JLo Beauty, Pattern Beauty (skincare extensions only), Honest Beauty.
**Cell C alternates:** Avène, Vichy, Aveeno (clinical SKUs), Differin, RoC.

---

## §4. Reference panel (LOCKED, carry-forward)

The six-slot LLM reference panel from v0.17 / v0.18 / v0.19 carries forward unchanged:

1. claude-opus-4-5
2. claude-sonnet-4-5
3. gpt-4o
4. gpt-4o-mini
5. gemini-2.5-flash
6. gemini-2.5-flash-lite

No provider model substitutions are anticipated at acquisition time. Forced substitutions (model deprecation, API change) are documented under the DEVIATIONS protocol if they occur.

---

## §5. Probe frames (LOCKED EX-ANTE)

### §5.1 Phase A — Recognition (C_P anchoring per v1.5)

For each registry brand, the Phase A C_P probe is sent to each of the six panel models with the exact wording:

> Is the brand [BRAND] commonly recognized as a skincare brand? Answer yes or no.

C_P score per brand: count of yes responses across the six-slot panel, range 0..6.

**Cascade order per cell** (top-of-list to bottom, exactly as enumerated in §3.1–§3.3 above):

- Cell A: Estée Lauder → Lancôme → La Mer → Sisley → Dior Beauty → Chanel Beauty → La Prairie → Clé de Peau Beauté
- Cell B: Rare Beauty → Rhode → Fenty Skin → Goop → Drunk Elephant → Glossier → Augustinus Bader → Tower 28
- Cell C: SkinCeuticals → La Roche-Posay → Paula's Choice → CeraVe → The Ordinary → Cetaphil → Eucerin → Bioderma

Per-cell pivot resolution follows v1.5 §6.4 (Phase A pivot-validation specification, SSRN 6797679): the first brand in cascade order achieving C_P = 6/6 becomes the cell pivot; remaining brands are probed for the dissociation analysis. If cascade exhausts (no brand at C_P = 6/6), the cell is documented as a DEVIATIONS entry and treated as a substantive finding per the v0.18 §5 Cell C precedent. **Alternates are NOT invoked on cascade exhaustion.**

### §5.2 Phase B — Recall (six-frame battery per v1.5)

Phase B operationalizes the v1.5 two-channel Recall decomposition. Six query frames are sent to each of the six panel models, yielding 36 (brand-eligible) observations per brand.

**R_cat channel (category-canonical retrieval, q1–q3):**

- **q1 (best):** *What are the best skincare brands? List several with descriptions.*
- **q2 (dermatologist):** *What skincare brands do dermatologists recommend? Name several.*
- **q3 (effective):** *What skincare brands are most effective? Name several brands with descriptions.*

**R_cult channel (cultural-footprint retrieval, q4–q6):**

- **q4 (popular):** *What skincare brands are popular right now? List several.*
- **q5 (celebrity):** *What skincare brands do celebrities and influencers use? Name several.*
- **q6 (cult/viral):** *What viral or cult-favorite skincare brands have gained big followings? Name several.*

For each (frame, model) response, all 24 registry brands are scanned for mention presence under the v1.4 canonical brand-mention detection rules: case-insensitive, accent-stripped, possessive-aware, first-occurrence-wins de-duplication.

**Per-brand R_cat** = sum of mentions across (q1, q2, q3) × 6 models = max 18.
**Per-brand R_cult** = sum of mentions across (q4, q5, q6) × 6 models = max 18.

Rank within enumerated response lists is recorded for Phase D ρ analysis.

---

## §6. Pre-registered hypotheses (FOUR, LOCKED EX-ANTE)

Four hypotheses are pre-registered, tested orthogonally. Verdict matrices are specified in §7.

### §6.1 H_Type2_emergence — PRIMARY, NOVEL FOR v0.20

**Claim:** Type 2 cases (R_cat ≤ 2/18 ∧ R_cult ≥ 5/18) emerge in Cell B at post-attrition n ≥ 5.

**Rationale:** The v1.5 dissociation framework predicts three classifications (Iwachu, Type 1, Type 2). Two of the three are populated empirically; Type 2 has zero observations across v0.17–v0.19. Cell B (celebrity DTC) is the substantively predicted home of Type 2: brands whose canonical-retrieval positioning is plausibly weak (absent from "best skincare" / "dermatologist-recommended" lists) but whose cultural-footprint surface is heavy (heavily mentioned in "popular," "celebrity," "viral" frames).

**Verdict matrix:**

| Type 2 cases in Cell B | Verdict |
|---|---|
| ≥ 3 | EMERGED |
| 1–2 | PARTIAL |
| 0 (at post-attrition Cell B n ≥ 5) | FALSIFIED |
| Cell B post-attrition n < 5 | UNDETERMINED |

### §6.2 H_Regime4_skincare — within-phase substantive; FIRST PROSPECTIVE v1.5 C2

**Claim:** The skincare substrate produces a Regime 4 (multi-component AI Availability + IL-gradient) signature under the v1.5 numerical thresholds.

**Conditions (sequential C1 → C2 → C2-guard → C3):**

- **C1:** post-attrition worldwide n ≥ 12 (panel adequacy floor).
- **C2 (v1.5 multi-statistic, per cell):** distinct C_P values ≥ 3 ∧ modal C_P share ≤ 0.625.
- **C2 IL-gradient guard:** Cell B top-2 R_cat share − Cell C top-2 R_cat share ≥ 0.10 (carry-forward from v0.18 §2.5).
- **C3:** per-cell Spearman ρ between Phase A C_P and Phase B R_cat ≥ 0.50, in ≥ 2 of 3 cells at post-attrition n ≥ 5.

**Phase D ρ uses R_cat as the y-variable**, preserving v1.4 Phase D semantics. R_cult contributes to dissociation classification (§6.3), not to Phase D rank coherence.

**Verdict routing:** standard four-regime truth table per v1.5 §4. Specifically:

| Earliest failing condition | Verdict |
|---|---|
| C1 fails | FALSIFIED (panel inadequacy) |
| C1 ok, C2 fails in ≥ 2 cells | FALSIFIED (regime-floor failure) |
| C1 ok, C2 fails in 1 cell only | PARTIAL |
| C1 + C2 ok, C2 IL-gradient guard fails | PARTIAL (IL-gradient inadequate) |
| C1 + C2 + guard ok, C3 fails | PARTIAL |
| All conditions clear | CONFIRMED |

If both/all cells fail C2 within-cell adequacy, **C3 is SKIPPED without computing per-cell ρ** (DEVIATIONS Rule 4 carry-forward; panel NOT substituted post-Phase-A).

### §6.3 H_Dissociation_substrate_generalization — 4th-family extension

**Claim:** Iwachu-pattern cases (Phase A C_P ≥ 5/6 ∧ R_cat ≤ 2/18) and Type 1 cases (R_cat ≥ 5/18 ∧ R_cult ≤ 2/18) reproduce on the skincare substrate family, extending the cumulative anchor base to ~24+ cases across 4 substrate families.

**Verdict matrix:**

| Iwachu cases distribution | Verdict | Precedent shape |
|---|---|---|
| Iwachu cases in ≥ 2 of 3 cells | GENERALIZED | v0.18 multi-cell distribution |
| Iwachu cases in 1 of 3 cells | PARTIAL | v0.19 single-cell concentration |
| Iwachu cases in 0 cells | NARROWED | Mechanism does not generalize to skincare |

Type 1 cases are reported descriptively alongside Iwachu cases and do not gate the verdict (Type 1 has been observed in v0.19; further evidence is confirmatory).

### §6.4 H_IdentityLoad_moderator — 4-leg joint, SECONDARY

**Claim:** The H_IdentityLoad_moderator joint over v0.16 × v0.17 × v0.18 × v0.20 returns a more confident verdict than the three-leg joint (v0.16 PARTIAL × v0.17 FALSIFIED-on-panel-inadequacy × v0.18 PARTIAL → joint PARTIAL).

**Verdict matrix (joint):**

| v0.20 leg outcome | Joint verdict (with prior three legs) |
|---|---|
| v0.20 CONFIRMED on H_Regime4 with monotonic IL signature (C → A → B) | CONFIRMED-bounded (moderator operates) |
| v0.20 PARTIAL | PARTIAL (moderator operates with substrate-specific qualifications) |
| v0.20 FALSIFIED (not on panel inadequacy) | NARROWED (moderator does not generalize to skincare IL range) |
| v0.20 FALSIFIED on panel inadequacy | INDETERMINATE (rerun on adequate panel; no joint update) |

v0.19 is excluded from the joint (uniform-IL design; no contribution to moderator). Reported descriptively in the v0.20 SSRN paper §4.3; not load-bearing for v0.20's primary headline.

---

## §7. Decision rules and numerical thresholds — locked summary

All thresholds below are locked at pre-reg r1 commit. They derive from v1.5 (SSRN 6810758) §3 (C2 multi-statistic), v1.5 §4 (two-channel Recall), v1.4 (SSRN 6799479) §5 (Iwachu and Type 1 thresholds), and v0.18 §2.5 (IL-gradient guard carry-forward).

| Symbol | Value | Source | Function |
|---|---|---|---|
| n_floor (worldwide) | 12 | C1 (v1.4 §6) | Panel adequacy floor |
| n_floor (per cell, C3 ρ) | 5 | C3 (v1.4 §6, v0.18 §2.5) | Per-cell minimum for Phase D ρ |
| distinct_CP_min | 3 | C2 (v1.5 §3) | Within-cell distinct C_P values |
| modal_CP_share_max | 0.625 | C2 (v1.5 §3) | Within-cell modal C_P share ceiling |
| IL_gradient_separation_min | 0.10 | C2 guard (v0.18 §2.5) | Cell B − Cell C top-2 R_cat share |
| ρ_C3_min | 0.50 | C3 (v1.4 §6) | Per-cell Phase D Spearman ρ |
| C3_cells_clearing_min | 2 of 3 | C3 (v1.4 §6) | Minimum cells clearing ρ_C3 |
| Iwachu_CP_min | 5/6 | v1.4 §5 | Iwachu dissociation Recognition floor |
| Iwachu_Rcat_max | 2/18 | v1.4 §5 / v1.5 §4 | Iwachu dissociation Recall ceiling |
| Type1_Rcat_min | 5/18 | v1.5 §4 | Type 1 R_cat floor |
| Type1_Rcult_max | 2/18 | v1.5 §4 | Type 1 R_cult ceiling |
| Type2_Rcat_max | 2/18 | v1.5 §4 | Type 2 R_cat ceiling |
| Type2_Rcult_min | 5/18 | v1.5 §4 | Type 2 R_cult floor |
| Type2_emerged_count | 3 | v0.20 §6.1 | Type 2 cases in Cell B for EMERGED verdict |
| Type2_partial_range | 1–2 | v0.20 §6.1 | Type 2 cases in Cell B for PARTIAL verdict |

**No thresholds are derived from v0.16's `score_v16.py`** (which operates on the v1.2 framework — AI Presence × Google Trends correlation). v1.2 and v1.5 operationalize fundamentally different constructs.

---

## §8. Substantive predictions (DESCRIPTIVE, NOT LOAD-BEARING)

These orient the eventual SSRN paper §4 Discussion; they are *not* part of the verdict resolution and do not affect any hypothesis's matrix.

**Phase A expectations:**

- **Cell C** (clinical) C_P: near-saturated for the major derm-recommended brands. Modal C_P share may be high → potential v1.5 C2 failure on degenerate-cell signature if cascade locks at first brand and most cell brands cluster at C_P = 6/6.
- **Cell A** (prestige) C_P: near-saturated for legacy names (Estée Lauder, Lancôme, La Mer, Chanel Beauty, Dior Beauty); some variance possible for La Prairie, Clé de Peau, Sisley.
- **Cell B** (celebrity DTC) C_P: **the substantive variance cell**. Major celebrity-founder brands (Rare Beauty, Rhode, Fenty Skin, Drunk Elephant) likely high C_P; Goop, Augustinus Bader, Tower 28 may register lower C_P. **This is where Cell B's within-cell C_P variance gives v1.5 C2 something to test prospectively.**

**Phase B expectations:**

- **Cell B R_cat:** likely sparse — celebrity DTC brands typically absent from "best skincare" / "dermatologist-recommended" / "most effective" canonical lists.
- **Cell B R_cult:** likely heavy — celebrity DTC brands surface in "popular," "celebrity," "viral" frames.
- **The combined Cell B R_cat-sparse / R_cult-heavy signature IS the Type 2 emergence claim.** If H_Type2_emergence returns EMERGED or PARTIAL, AIAS™ 1.0's foundational construct ships complete (all three dissociation quadrants empirically populated). If FALSIFIED, the construct still ships but with Type 2 as a predicted-but-not-observed quadrant — a substantive negative result.

---

## §9. DEVIATIONS protocol

### §9.1 Carry-forward rules

- **Rule 1 (carry-forward from v0.17):** Any deviation from this pre-registration after lock requires a separate DEVIATIONS entry with timestamp, rationale, and git commit. Lock state is preserved across deviations.
- **Rule 2 (carry-forward from v0.17):** Deviations opened post-pre-reg-lock require OSF re-deposit of the updated DEVIATIONS.md alongside the unchanged pre-reg artifact.
- **Rule 3 (carry-forward from v0.18):** Phase A cascade exhaustion is treated as a substantive finding, not as an alternate-trigger. Alternates per §3.5 are reserved for substrate-level mismatch.
- **Rule 4 (carry-forward from v0.17):** If both/all cells fail C2 within-cell adequacy, C3 is SKIPPED without computing per-cell ρ. Panel is NOT substituted post-Phase-A.
- **Rule 5 (carry-forward from v0.18):** Each cell pre-registers up to 5 alternates; invocation criteria per §3.5 above.

### §9.2 Entry 0 — Pre-acquisition COI screen (ex-ante)

**Date:** [LOCK DATE — populated at git commit]
**Trigger:** Pre-acquisition COI screen per AIAS™ Declarations standard.
**Subject:** Samsung Electronics America (author's primary employer) potential exposure to v0.20 registry.

**Screen result:** None of the 24 brands in the locked registry (§3) is affiliated with Samsung Electronics America. Samsung's historical beauty-category exposure was via Cheil Industries (spun off pre-2026 in corporate restructuring); no current overlap with the v0.20 registry. The author's role at Samsung (Director, Corporate Brand Creative and Governance) carries no commercial, strategic, or signaling interest in any v0.20 brand outcome.

**Disposition:** No deviation from pre-registration warranted. Entry deposited ex-ante to document the screen in the OSF artifact.

**Lock state:** v0.20-prereg-r1 unchanged.

### §9.3 Open-state at lock

No deviations open at pre-reg r1 commit other than Entry 0 (ex-ante COI screen). Additional entries (if any) will be opened during acquisition and post-acquisition with full timestamping.

---

## §10. Pre-registration discipline and lock sequence

The pre-registration is non-negotiably locked **before any measurement.** Sequence:

1. Author `~/aias/prereg/v0_20_prereg.md` (this document) and `~/aias/prereg/v0_20_registry.json` (locked brand registry per §3).
2. `git add` both files; commit with message `prereg: v0.20 r1 — skincare IL-gradient, four hypotheses, v1.5 first prospective`.
3. `git tag v0.20-prereg-r1 <commit>`.
4. `git push origin v0.20-skincare-il-gradient && git push origin v0.20-prereg-r1`.
5. Deposit pre-reg artifact + registry JSON to `osf.io/ec6wh/v20/` (read-only after deposit).
6. **Only then** run acquisition (Phase A → Phase B).
7. After acquisition CSVs are written: `git tag v0.20-acquisition-locked <commit>`.

If iterative pre-reg refinement is needed (r1 → r2 → r3 …), each revision is tagged separately. Full revision history is preserved in Appendix A. v0.18 ran r1–r4; v0.19 ran r1; v0.20 begins at r1.

---

## §11. Author and affiliation block (SSRN standard)

| Field | Value |
|---|---|
| First name | Pablo |
| Middle name | Ulpiano |
| Last name | González Castro |
| Email | pablou@pablou.com |
| ORCID | 0009-0003-8968-9990 |
| Primary affiliation | School of Visual Arts, MPS Branding Program, New York, NY |
| Secondary affiliation | Third System™ (research entity; data archive and methodology venue) |

Samsung Electronics America is disclosed only in Declarations §COI, never in the author block.

---

## Appendix A — Revision history

| Revision | Tag | Commit | Date | Changes |
|---|---|---|---|---|
| r1 | `v0.20-prereg-r1` | [TBD at lock] | [TBD at lock] | Initial pre-registration: substrate, panel, six-frame Phase B battery, four hypotheses, v1.5 numerical thresholds, Entry 0 COI screen. |

Subsequent revisions (r2, r3, …) will be appended here if needed before acquisition lock.

---

## Trademark notice

AIAS™ and Third System™ are trademarks of the research program.

<!-- End v0.20 pre-registration artifact, r1 draft, pre-lock state -->
