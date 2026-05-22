# AIAS™ Presence Measurement Protocol — v0.21 Pre-Registration

**Phase:** v0.21 (Cosmetics; IL-gradient design)
**Protocol version:** v1.5 (SSRN 6810758) — unchanged from v0.20; second prospective phase under v1.5
**Working title:** *Type 2 EMERGED on a Cosmetics IL-Gradient Substrate — Fifth Substrate Family for the Presence-Component AIAS™ 1.0 Anchor Base*
**Working subtitle:** *AIAS™ Presence Measurement Protocol, v0.21 — Cell B Type 2 count clears EMERGED threshold; cross-substrate generalization closed*
**Author:** Pablo Ulpiano González Castro
**Pre-registration revision:** r1
**Lock target:** git tag `v0.21-prereg-r1` on branch `v0.21-cosmetics-il-gradient`; OSF deposit at osf.io/ec6wh/v21/prereg/
**Status at this draft:** Pre-acquisition. No Phase A or Phase B data exists.

---

## §1. Phase position and mission

### §1.1 Position in empirical sequence

v0.21 is the eighth acquisition phase in the AIAS™ Presence Measurement Protocol and the second prospective phase pre-registered against the v1.5 (SSRN 6810758) numerical thresholds. The phase sits in the empirical sequence as:

| Phase | Substrate | SSRN | Protocol version exercised |
|---|---|---|---|
| v0.16 | Kitchen knives | 6791999 | v1.2 (AI Presence × Google Trends) |
| v0.17 | Premium kitchenware (incl. Japanese cell) | 6802261 | v1.4 (Recognition × Recall, retrospective anchor) |
| v0.18 | Indie fragrance | 6806558 | v1.4 (first generalization; r4 numerical lock) |
| v0.19 | Audiophile headphones | 6809182 | v1.4 (within-family replication) |
| v0.20 | Skincare | 6811441 | v1.5 (first prospective; Type 2 PARTIAL, Iwachu GENERALIZED) |
| **v0.21** | **Cosmetics** | **(this paper)** | **v1.5 (second prospective)** |

### §1.2 Mission

v0.21 pursues four objectives, ordered by load-bearing weight on AIAS™ 1.0:

1. **Pursue Type 2 EMERGED on a fifth substrate family.** v0.20 (Skincare, SSRN 6811441) returned H_Type2_emergence = PARTIAL with two clean Cell B cases (Glossier R_cult = 9, Rhode R_cult = 8) and one boundary case (Augustinus Bader R_cat = 2). PARTIAL routes to the 1–2 band; EMERGED requires ≥ 3 clean Cell B cases. Cosmetics is the canonical follow-up substrate because the celebrity-DTC tier is structurally more populous than skincare's (Rare Beauty, Fenty Beauty, Haus Labs, Kylie Cosmetics, Huda Beauty, Pat McGrath Labs, Charlotte Tilbury, Anastasia Beverly Hills give eight viable Cell B brands without reaching). v0.21 hunts for ≥ 3 clean Type 2 cases to clear the EMERGED threshold.
2. **Close the cross-substrate generalization claim for AIAS™ 1.0's headline narrative.** v0.21 extends the Recognition × Recall dissociation construct to a fifth substrate family (Japanese kitchenware, indie fragrance, audiophile electronics, skincare, cosmetics). Five families anchor the Presence-component AIAS™ 1.0 release.
3. **Second prospective test of the v1.5 C2 multi-statistic rule** (distinct C_P values ≥ 3 ∧ modal share ≤ 0.625). The rule was calibrated retrospectively against joint v0.18 + v0.19 data, exercised prospectively for the first time in v0.20, and is locked again here. Either pass or fail behavior at the v1.5 thresholds is informative.
4. **Extend the H_IdentityLoad_moderator joint to a fifth leg.** The v0.16 × v0.17 × v0.18 × v0.20 four-leg joint contributes the antecedent state. v0.21 adds the fifth leg. v0.19 remains excluded (uniform-IL design).

### §1.3 Side-test: Rare Beauty Recognition substrate-anchor

Rare Beauty failed Phase A in v0.20 (C_P = 0/6, "skincare brand?" probe) because its primary LLM-corpus identity is cosmetics, not skincare. v0.21's Phase A re-runs Rare Beauty under the "cosmetics brand?" probe; clearing C_P here would demonstrate that the v0.20 failure was substrate-anchor mismatch, not brand absence. This is reported descriptively in §4 of the eventual SSRN paper; it is **not** a pre-registered hypothesis and does not gate any verdict.

---

## §2. Substrate definition and IL-gradient design

### §2.1 Substrate

Cosmetics, operationally defined as the makeup / decorative-cosmetics consumer-discovery surface. The substrate is selected on three grounds:

1. **Type 2 hunting power, populous high-IL tier.** Cosmetics' celebrity-DTC tier is the most populous identified in the AIAS™ programme to date: eight viable Cell B brands without reaching for alternates. If Type 2 EMERGED is going to clear empirically, this is the substrate where it should.
2. **Three-tier IL stratification on the consumer-discovery surface.** Cosmetics admits a clean low → medium → high IL gradient spanning drugstore (purely functional purchase) → counter prestige (status-signaling acquisition) → celebrity-founder DTC (identity-statement purchase).
3. **English-language anchored.** No cross-cultural confound. All cells are sampled from the same LLM-coverage baseline.

### §2.2 IL-gradient design

| Cell | IL tier | Identity function | Substrate role |
|---|---|---|---|
| **A — Prestige** | Medium | Status / signaling: counter-purchase at department store, brand-association partially performs status acquisition | Middle comparator |
| **B — Celebrity DTC / cult** | High | Identity statement: founder- or celebrity-identity brands where brand identity is part of the product signal | **Type 2 hunting cell** |
| **C — Drugstore / mass** | Low | Functional: drugstore acquisition, selection separable from product identity | Canonical-retrieval baseline |

The IL stratification is monotonic C → A → B (low → medium → high). The C → B span matches v0.20's design and remains wider than v0.18/v0.19.

---

## §3. Brand registry (LOCKED)

Pre-floor n = 24 worldwide (8 per cell). C1 floor n ≥ 12 is satisfied with 50% LLM-substrate attrition headroom.

### §3.1 Cell A — Prestige (medium IL)

1. MAC Cosmetics
2. NARS
3. Bobbi Brown
4. Tom Ford Beauty
5. Giorgio Armani Beauty
6. Hourglass
7. Chantecaille
8. Laura Mercier

### §3.2 Cell B — Celebrity DTC / cult (high IL, Type 2 hunting cell)

1. Rare Beauty (Selena Gomez)
2. Fenty Beauty (Rihanna)
3. Haus Labs (Lady Gaga)
4. Pat McGrath Labs
5. Charlotte Tilbury
6. Huda Beauty
7. Kylie Cosmetics
8. Anastasia Beverly Hills

### §3.3 Cell C — Drugstore / mass (low IL)

1. Maybelline
2. L'Oréal Paris
3. CoverGirl
4. Revlon
5. NYX Professional Makeup
6. e.l.f. Cosmetics
7. Wet n Wild
8. Milani Cosmetics

### §3.4 Borderline classifications (pre-registered ex-ante)

Per the v0.18 §2.2 conglomerate-ownership precedent and the v0.20 §3.4 identity-signal positioning rule, the following v0.21 brands carry positioning ambiguity and are classified by **primary classifier** on the consumer-discovery surface:

| Brand | Ambiguity | Cell | Primary classifier |
|---|---|---|---|
| Pat McGrath Labs | Founder-makeup-artist identity at prestige price-point | B | Founder-identity primary classifier |
| Charlotte Tilbury | Founder-makeup-artist identity at prestige price-point | B | Founder-identity primary classifier |
| e.l.f. Cosmetics | Drugstore price-point with cult following | C | Drugstore-distribution primary classifier; flagged for retrospective dissociation review if Type 2 boundary case |
| NYX Professional Makeup | Drugstore distribution with semi-professional positioning | C | Drugstore-distribution primary classifier |
| Tom Ford Beauty | Prestige beauty under LVMH/Estée Lauder umbrella | A | Counter-distribution primary classifier; primary-cosmetics identity in LLM corpora (no fragrance/skincare-extension dilution as in v0.20's Dior Beauty / Chanel Beauty) |
| Giorgio Armani Beauty | Prestige beauty under L'Oréal Luxe licensing | A | Counter-distribution primary classifier; primary-cosmetics identity in LLM corpora |

All six are subject to retrieval-frame resolution in Phase B; their cell assignment is locked but their canonical-retrieval pattern will be examined in §3.4 of the eventual SSRN paper.

### §3.5 Alternates (DEVIATIONS Rule 5)

Up to 5 alternates per cell, invoked only on **substrate-level mismatch** (e.g., LLM-substrate failure-by-name-change, structural acquisition restructure), **not** on Phase A pivot-cascade exhaustion. The v0.18 Cell C / v0.20 carry-forward precedent — cascade exhaustion is treated as substantive finding, not alternate-trigger — applies in full.

**Cell A alternates (ordered):** Smashbox, Urban Decay, Too Faced.
**Cell B alternates (ordered):** Florence by Mills, Flower Beauty (Drew Barrymore). (Selena Gomez's other ventures excluded.)
**Cell C alternates (ordered):** Almay, Physicians Formula, Black Radiance.

---

## §4. Reference panel (LOCKED, carry-forward)

The six-slot LLM reference panel from v0.17 / v0.18 / v0.19 / v0.20 carries forward unchanged:

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

> Is the brand [BRAND] commonly recognized as a cosmetics brand? Answer yes or no.

C_P score per brand: count of yes responses across the six-slot panel, range 0..6.

**Cascade order per cell** (top-of-list to bottom, exactly as enumerated in §3.1–§3.3 above):

- Cell A: MAC Cosmetics → NARS → Bobbi Brown → Tom Ford Beauty → Giorgio Armani Beauty → Hourglass → Chantecaille → Laura Mercier
- Cell B: Rare Beauty → Fenty Beauty → Haus Labs → Pat McGrath Labs → Charlotte Tilbury → Huda Beauty → Kylie Cosmetics → Anastasia Beverly Hills
- Cell C: Maybelline → L'Oréal Paris → CoverGirl → Revlon → NYX Professional Makeup → e.l.f. Cosmetics → Wet n Wild → Milani Cosmetics

Per-cell pivot resolution follows v1.5 §6.4 (Phase A pivot-validation specification, SSRN 6797679): the first brand in cascade order achieving C_P = 6/6 becomes the cell pivot; remaining brands are probed for the dissociation analysis. If cascade exhausts (no brand at C_P = 6/6), the cell is documented as a DEVIATIONS entry and treated as a substantive finding per the v0.18 §5 / v0.20 carry-forward precedent. **Alternates are NOT invoked on cascade exhaustion.**

### §5.2 Phase B — Recall (six-frame battery per v1.5)

Phase B operationalizes the v1.5 two-channel Recall decomposition. Six query frames are sent to each of the six panel models, yielding 36 (brand-eligible) observations per brand.

**R_cat channel (category-canonical retrieval, q1–q3):**

- **q1 (best):** *What are the best cosmetics brands? List several with descriptions.*
- **q2 (professional):** *What makeup brands do professional makeup artists recommend? Name several.*
- **q3 (high-quality):** *What cosmetics brands are highest quality and most reliable? Name several brands with descriptions.*

**R_cult channel (cultural-footprint retrieval, q4–q6):**

- **q4 (popular):** *What cosmetics brands are popular right now? List several.*
- **q5 (celebrity):** *What makeup brands do celebrities and influencers use? Name several.*
- **q6 (cult/viral):** *What viral or cult-favorite makeup brands have gained big followings? Name several.*

For each (frame, model) response, all 24 registry brands are scanned for mention presence under the v1.4 canonical brand-mention detection rules: case-insensitive, accent-stripped, possessive-aware, first-occurrence-wins de-duplication.

**Per-brand R_cat** = sum of mentions across (q1, q2, q3) × 6 models = max 18.
**Per-brand R_cult** = sum of mentions across (q4, q5, q6) × 6 models = max 18.

Rank within enumerated response lists is recorded for Phase D ρ analysis.

---

## §6. Pre-registered hypotheses (FOUR, LOCKED EX-ANTE)

Four hypotheses are pre-registered, tested orthogonally. Verdict matrices are specified in §7.

### §6.1 H_Type2_EMERGED_cosmetics — PRIMARY, novel for v0.21 (pursues v0.20's PARTIAL)

**Claim:** Type 2 cases (R_cat ≤ 2/18 ∧ R_cult ≥ 5/18) emerge in Cell B at post-attrition n ≥ 5, with **count ≥ 3**.

**Rationale:** v0.20 returned PARTIAL with Cell B Type 2 count = 2 (Glossier, Rhode). The PARTIAL band is [1, 2]; EMERGED requires ≥ 3. Cosmetics' celebrity-DTC tier is structurally more populous than skincare's, providing eight viable Cell B brands. Strong Type 2 candidates: Haus Labs (Lady Gaga's brand is heavily celebrity-coded; canonical-frame Recall may be sparse despite full Recognition), Kylie Cosmetics (similar — Kylie Jenner brand identity dominates cultural-frame discourse), Huda Beauty (founder-celebrity / Instagram-native cult).

**Verdict matrix:**

| Type 2 cases in Cell B | Verdict |
|---|---|
| ≥ 3 | **EMERGED** ← primary v0.21 target |
| 1–2 | PARTIAL (matches v0.20) |
| 0 (at post-attrition Cell B n ≥ 5) | FALSIFIED |
| Cell B post-attrition n < 5 | UNDETERMINED |

### §6.2 H_Regime4_cosmetics — within-phase substantive; second prospective v1.5 C2

**Claim:** The cosmetics substrate produces a Regime 4 (multi-component AI Availability + IL-gradient) signature under the v1.5 numerical thresholds.

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

### §6.3 H_Dissociation_substrate_generalization_5th_family — 5th-family extension

**Claim:** Iwachu-pattern cases (Phase A C_P ≥ 5/6 ∧ R_cat ≤ 2/18) and Type 1 cases (R_cat ≥ 5/18 ∧ R_cult ≤ 2/18) reproduce on the cosmetics substrate family, extending the cumulative anchor base to five substrate families and closing the cross-substrate generalization claim for Presence-component AIAS™ 1.0.

**Verdict matrix:**

| Iwachu cases distribution | Verdict | Precedent shape |
|---|---|---|
| Iwachu cases in ≥ 2 of 3 cells | GENERALIZED | v0.18 / v0.20 multi-cell distribution |
| Iwachu cases in 1 of 3 cells | PARTIAL | v0.19 single-cell concentration |
| Iwachu cases in 0 cells | NARROWED | Mechanism does not generalize to cosmetics |

Type 1 cases are reported descriptively alongside Iwachu cases and do not gate the verdict (Type 1 has been observed in v0.19 and v0.20; further evidence is confirmatory).

**Programme significance:** GENERALIZED here completes the five-family anchor base. The cross-substrate generalization claim of Presence-component AIAS™ 1.0 ships on this verdict.

### §6.4 H_IdentityLoad_moderator — 5-leg joint, DESCRIPTIVE

**Claim:** The H_IdentityLoad_moderator joint over v0.16 × v0.17 × v0.18 × v0.20 × v0.21 returns a more confident verdict than the four-leg antecedent joint.

**v0.19 is excluded** from the joint (uniform-IL design; no contribution to moderator). This exclusion carries forward unchanged from v0.20.

**Verdict matrix (joint):**

| v0.21 leg outcome | Joint verdict (with prior four legs) |
|---|---|
| v0.21 CONFIRMED on H_Regime4 with monotonic IL signature (C → A → B) | CONFIRMED-bounded (moderator operates) |
| v0.21 PARTIAL | PARTIAL (moderator operates with substrate-specific qualifications) |
| v0.21 FALSIFIED (not on panel inadequacy) | NARROWED (moderator does not generalize to cosmetics IL range) |
| v0.21 FALSIFIED on panel inadequacy | INDETERMINATE (rerun on adequate panel; no joint update) |

H_IdentityLoad_moderator is reported descriptively in the v0.21 SSRN paper §4.3; not load-bearing for v0.21's primary headline (Type 2 EMERGED pursuit).

---

## §7. Decision rules and numerical thresholds — locked summary

All thresholds below are locked at pre-reg r1 commit. They derive from v1.5 (SSRN 6810758) §3 (C2 multi-statistic), v1.5 §4 (two-channel Recall), v1.4 (SSRN 6799479) §5 (Iwachu and Type 1 thresholds), and v0.18 §2.5 (IL-gradient guard carry-forward). All thresholds are unchanged from v0.20 pre-reg §7 (no methodology increment in v0.21).

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
| Type2_emerged_count | 3 | v0.20 §6.1 / v0.21 §6.1 | Type 2 cases in Cell B for EMERGED verdict |
| Type2_partial_range | 1–2 | v0.20 §6.1 / v0.21 §6.1 | Type 2 cases in Cell B for PARTIAL verdict |

**No thresholds are derived from v0.16's `score_v16.py`** (which operates on the v1.2 framework — AI Presence × Google Trends correlation). v1.2 and v1.5 operationalize fundamentally different constructs.

---

## §8. Substantive predictions (DESCRIPTIVE, NOT LOAD-BEARING)

These orient the eventual SSRN paper §4 Discussion; they are *not* part of the verdict resolution and do not affect any hypothesis's matrix.

**Phase A expectations:**

- **Cell A** (prestige) C_P: near-saturated mean (~5.5–6.0/6). All eight brands are primary-cosmetics identities in LLM corpora; no fragrance/skincare-extension dilution. Variance prediction: low to moderate. Tom Ford Beauty / Armani Beauty / Hourglass / Chantecaille tail should provide some variance (modal share likely 0.625–0.750). **Risk: Cell A could fully saturate similar to v0.20 Cell C, with v1.5 C2 rejection.**
- **Cell B** (celebrity DTC) C_P: variance-rich distribution (mean ~4.5–5.5/6). Celebrity-founder brands should be well-recognized (Rare Beauty, Fenty Beauty, Charlotte Tilbury, Huda Beauty all near saturation), with possible C_P drop for newer or smaller-presence brands (Haus Labs, Kylie Cosmetics at moderate). **This is the variance-rich cell v1.5 C2 was designed for; pass expected.**
- **Cell C** (drugstore) C_P: near-saturation similar to v0.20's Clinical cell. Maybelline / L'Oréal Paris / CoverGirl / Revlon / NYX all heavily represented in LLM corpora as cosmetics brands. **v1.5 C2 likely rejects on saturation.** This is acceptable: primary v0.21 verdict (H_Type2) does not depend on H_Regime4 clearing.

**Phase B expectations:**

- **Cell A R_cat:** high, distributed (MAC, NARS, Charlotte Tilbury [if classified A — not in this design], Bobbi Brown, Laura Mercier broad coverage in canonical "best" frames).
- **Cell B R_cat:** moderate to high. Fenty Beauty especially — its product-quality reputation is independent of celebrity status; Rare Beauty, Charlotte Tilbury, Pat McGrath Labs likely substantial.
- **Cell C R_cat:** very high, near-saturated (drugstore brands dominate canonical lists).
- **Cell A R_cult:** low to moderate (prestige cosmetics surface in celebrity coverage but not as cult/viral).
- **Cell B R_cult:** very high (the hunting target — celebrity-founder brands should saturate cultural frames).
- **Cell C R_cult:** moderate (e.l.f. especially — cult-drugstore positioning).

**Type 2 case projections (R_cat ≤ 2 ∧ R_cult ≥ 5):**

- **Strong Type 2 candidates:** Haus Labs, Kylie Cosmetics, Huda Beauty (heavily celebrity-coded; canonical-frame Recall may be sparse despite full Recognition).
- **Boundary cases:** Rare Beauty, Charlotte Tilbury (both have substantial canonical-channel reputation in addition to cultural footprint; may not cross the R_cat ≤ 2 threshold).
- **Predicted Cell B Type 2 count:** 3–4. EMERGED verdict probable but not guaranteed.

These predictions are descriptive scaffolding for §4 of the eventual SSRN paper. The actual verdict resolution comes from the scorer's application of the locked verdict matrices in §6 and §7 to the acquired data, not from these expectations.

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
**Subject:** Samsung Electronics America (author's primary employer) potential exposure to v0.21 registry.

**Screen result:** None of the 24 brands in the locked registry (§3) is affiliated with Samsung Electronics America. Samsung's Harman International (audio acquisition) has no cosmetics exposure. Samsung's historical beauty/cosmetics activities through Cheil Industries (Hera, IOPE, Mamonde, Sulwhasoo, Espoir under Amorepacific licensing) were divested pre-2018 and have no current overlap with the v0.21 registry. The author's role at Samsung (Director, Corporate Brand Creative and Governance) carries no commercial, strategic, or signaling interest in any v0.21 brand outcome.

**Disposition:** No deviation from pre-registration warranted. Entry deposited ex-ante to document the screen in the OSF artifact.

**Lock state:** v0.21-prereg-r1 unchanged.

### §9.3 Open-state at lock

No deviations open at pre-reg r1 commit other than Entry 0 (ex-ante COI screen). Additional entries (if any) will be opened during acquisition and post-acquisition with full timestamping.

---

## §10. Pre-registration discipline and lock sequence

The pre-registration is non-negotiably locked **before any measurement.** Sequence:

1. Author `~/aias/prereg/v0_21_prereg.md` (this document) and `~/aias/prereg/v0_21_registry.json` (locked brand registry per §3).
2. `git add` both files; commit with message `prereg: v0.21 r1 — cosmetics IL-gradient, Type 2 EMERGED pursuit, fifth substrate family`.
3. `git tag v0.21-prereg-r1 <commit>`.
4. `git push origin v0.21-cosmetics-il-gradient && git push origin v0.21-prereg-r1`.
5. Deposit pre-reg artifact + registry JSON to `osf.io/ec6wh/v21/prereg/` (read-only after deposit).
6. **Only then** run acquisition (Phase A → Phase B).
7. After acquisition CSVs are written: `git tag v0.21-acquisition-locked <commit>`.

If iterative pre-reg refinement is needed (r1 → r2 → r3 …), each revision is tagged separately. Full revision history is preserved in Appendix A. v0.18 ran r1–r4; v0.19 and v0.20 each ran r1; v0.21 begins at r1.

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
| r1 | `v0.21-prereg-r1` | [TBD at lock] | [TBD at lock] | Initial pre-registration: cosmetics substrate, 24-brand IL-gradient panel, six-frame Phase B battery (cosmetics-anchored), four hypotheses (Type 2 EMERGED pursuit as PRIMARY), v1.5 numerical thresholds (carried forward unchanged), 5-leg H_IdentityLoad_moderator joint, Entry 0 COI screen. |

Subsequent revisions (r2, r3, …) will be appended here if needed before acquisition lock.

---

## Trademark notice

AIAS™ and Third System™ are trademarks of the research program.

<!-- End v0.21 pre-registration artifact, r1 draft, pre-lock state -->
