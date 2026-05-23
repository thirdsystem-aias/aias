# §5 Joint Retrospective Scoring — Source Data

**Purpose.** Source artifact for the v1.6 paper §5 joint retrospective scoring table. Compiled from: v1.6 retrospective scorer outputs (`methodology/v1_6/retrospective/v0_*/v1_6_retrospective_*.json`) for v0.20 and v0.21; published verdict JSON / scoring output files for v0.16–v0.19 under their respective `~/aias/osf/v*/` trees.

**Locked at:** v1.6-prereg-r1 (commit `f10616a`).

---

## §5 Table (6 rows × 7 columns, schema locked)

| Phase | Substrate | Routing (v1.5) | Routing (v1.6 — Inc 1) | Moderator verdict (v1.5) | Moderator verdict (v1.6 — H_IdentityLoad_Direct) | Phantom verdict |
|---|---|---|---|---|---|---|
| v0.16 | Kitchen knives | Standard (v1.4 protocol) | differential (narrative — published Phase A C_P distributions show within-cell variance) | PARTIAL leg (joint with v0.17, v0.18) | N/A — two-channel R_cult data not collected at acquisition | N/A (out of v1.6 retrospective scope) |
| v0.17 | Premium kitchenware | Standard (v1.4 protocol) | differential (narrative — within-cell variance plus panel inadequacy) | FALSIFIED-on-panel-inadequacy leg | N/A — two-channel R_cult data not collected at acquisition | N/A |
| v0.18 | Indie fragrance | Standard (v1.4 protocol; ρ-based C3 only) | differential (narrative — C_P modal share 0.69 worst cell; not uniform) | PARTIAL joint (3-leg with v0.16, v0.17) | N/A — two-channel R_cult data not collected at acquisition | N/A |
| v0.19 | Audiophile headphones | v1.4.x protocol (Heritage/Boutique 2-cell design); C2 FAILED → UNDETERMINED | mixed (narrative — Cell B modal_share 0.875 high but distinct ≠ 1 in either cell) | Excluded from joint (uniform-IL design; no contribution) | N/A — channel q1–q6 not yet decomposed into R_cat / R_cult at acquisition | N/A |
| v0.20 | Skincare | v1.5 full sequence; C2 FALSIFIED (1 cell saturated, 1 cell bimodal) | differential (scored: distinct = {2, 3, 1} across A, B, C) | NARROWED (5-leg joint) | **PARTIAL** (Cell B δ=+3.75 CI [+2.25, +5.25] excludes 0; Cell A δ=+0.75 against IL prediction with CI [−0.25, +2.12] overlapping 0; Cell C δ=−2.50 carries the substrate's R_cat dominance) | N/A (Phantom prospective-only from v0.22+; v0.20 out of scope) |
| v0.21 | Cosmetics | v1.5 full sequence; C2 FALSIFIED (uniform saturation 6/6 all cells) | **uniform-saturation** (scored: distinct = 1 in all 3 cells; modal_share 1.000) → routes to `REGIME-4-UNAVAILABLE-AT-RECOGNITION` | NARROWED (5-leg joint) | **CONFIRMED** (Cell A δ=−3.13 CI [−6.00, −0.25] excludes 0; Cell B δ=+7.12 CI [+4.75, +10.25] excludes 0; Cell C δ=+1.00 monotonic-gradient check passes: A < C < B) | **CONFIRMED** (6 off-panel reference-vocabulary brands clear R_phantom ≥ 6; validity anchor Glossier R_phantom = 12 ≥ required 6 ✓) |

---

## Headline before/after deltas

**v0.21 — primary headline.**
- **v1.5 Regime 4:** FALSIFIED (uniform saturation indistinguishable from differential failure).
- **v1.6 Regime 4:** REGIME-4-UNAVAILABLE-AT-RECOGNITION (substrate-shape information explicit).
- **v1.5 moderator:** NARROWED (joint backed off despite strong within-phase signal).
- **v1.6 moderator (H_IdentityLoad_Direct):** CONFIRMED. δ = +7.12 in Cell B is the program's strongest cult signal; CI excludes 0 by a wide margin; Cell A's δ = −3.13 also excludes 0 in the predicted negative direction.
- **v1.6 Phantom:** CONFIRMED with margin. Six off-panel brands (Urban Decay 13, Estée Lauder 13, Glossier 12, Too Faced 9, Make Up For Ever 7, Clinique 6) clear K=6.

**v0.20 — modest uplift, substantive finding.**
- **v1.5 moderator:** NARROWED.
- **v1.6 moderator:** PARTIAL. Cell B's δ = +3.75 with CI excluding 0 supports the IL-gradient prediction in the high-IL cell. But Cell A's δ = +0.75 (CI overlaps 0) is against prediction — skincare's Cell A (heritage/clinical/dermatologist) does not concentrate in the canonical channel the way cosmetics' Cell A (prestige/heritage) does. Cell C's δ = −2.50 carries the substrate's R_cat dominance (drugstore/mass skincare names like Cetaphil, Neutrogena are canonical-channel-dominant). The substrate's IL-gradient signal lives in Cell B vs. Cell C, not Cell A vs. Cell B as the standard prediction.

**v0.16–v0.19 — applicability boundary.**
- Inc 1 narrative classification feasible from published Phase A C_P distributions; all four classify as differential or mixed (no uniform-saturation).
- Inc 2 retrospective bootstrap not feasible — two-channel R_cult decomposition is a v1.5 prospective increment (first acquired in v0.20). v0.19 used single-dimensional q1–q6 frames; v0.16–v0.18 used single-channel mention scoring. Retrospective channel re-mapping considered and rejected as introducing measurement artifacts not present at acquisition.

---

## Phantom Brand Persistence — full off-panel results (v0.21)

| Brand | R_cat_phantom (max 18) | R_cult_phantom (max 18) | R_phantom (max 36) | Channel signature | Cleared K=6? |
|---|---|---|---|---|---|
| Urban Decay | 8 | 5 | 13 | mixed (slight canonical lean) | ✓ |
| Estée Lauder | 13 | 0 | 13 | **pure canonical** | ✓ |
| Glossier | 0 | 12 | 12 | **pure cultural** | ✓ (validity anchor) |
| Too Faced | 3 | 6 | 9 | cultural-leaning | ✓ |
| Make Up For Ever | 6 | 1 | 7 | canonical-leaning | ✓ |
| Clinique | 6 | 0 | 6 | **pure canonical** | ✓ |
| (44 other off-panel brands) | — | — | < 6 | — | ✗ |

**Empirical weight of the construct.** Outline §4.5 motivated Phantom on a single brand (Glossier). The actual measurement surfaces six off-panel brands clearing K=6 — a substrate-level pattern, not a one-off anomaly.

**Phantom carries channel signature — a §4 headline.** Three of six phantom brands have channel-pure signatures: Estée Lauder and Clinique appear exclusively in canonical frames (R_cat = 13 and 6, R_cult = 0 for both); Glossier appears exclusively in cultural frames (R_cult = 12, R_cat = 0). The channel signatures track the brands' identity loads: Estée Lauder and Clinique are prestige/heritage (low-IL canonical brands), Glossier is celebrity/DTC/cult (high-IL cultural brand). The IL-gradient mechanism that produces panel-level channel asymmetry also produces off-panel phantom channel asymmetry. This is a substantive theoretical finding for §4 and a precursor for the AIAS™ 1.0 synthesis.

(Source: `methodology/v1_6/retrospective/v0_21/v1_6_retrospective_v0_21.json`, Increment 3 per-brand block.)

---

## Methodology-log notes for §7

- **v0.21 substrate classification.** First measured case of uniform-saturation. Validates the locked rule (distinct C_P = 1 in all 3 cells) — caught by the rule precisely, with v0.20 (distinct = {2, 3, 1}) correctly rejected.
- **H_IdentityLoad_Direct vs. H_IdentityLoad_moderator semantics.** v0.21 demonstrates the wedge: when Regime 4 falsifies for *substrate-wide* reasons (saturation), the joint moderator hypothesis backs off (NARROWED) despite a positive within-phase signal. The Direct pathway evaluates the signal regardless of Regime 4 routing — for v0.21, this lifts the verdict from NARROWED to CONFIRMED.
- **Phantom K calibration validity.** v0.21 Glossier R_phantom = 12 ≥ required 6 ✓. K = 6 threshold validated. No pre-reg amendment required.
