"""
v1.9 - Two-Component AIAS Composite Calibration (Presence x Consistency)
Pre-Registration Content Module
AIAS(TM) Measurement Program - Third System(TM)

DRAFT r1 (Nov 9, 2026) - NOT LOCKED. Target lock: with v0.40/v0.41 on Mon Nov 16, 2026
(tag v1.9-prereg-r1, pushed, plus the OSF deposit of osf/methodology/v1_9/prereg/),
BEFORE the first t3 call of v0.41, so the t2->t3 confirmation is blind.

METHODOLOGY LOCK (no new acquisition). Two stages:
  Stage 1 - CALIBRATION on the frozen t1 (May 2026) and t2 (Jun 10, 2026) waves of the
            five omnibus substrates (v0.19-v0.23, 112 brand units). These data are already
            in the record (v0.34, v1.8), so Stage 1 is declared as calibration, not as a
            test. It is run BEFORE the lock under the selection rule below, and the lock
            names the selected specification.
  Stage 2 - CONFIRMATION on t2 -> t3 (v0.41, collected Nov 17-21, 2026) under the locked
            specification. Blind: the specification is fixed before t3 exists.

Reconciles two forward references. v1.8's locked record names v1.9 "two-component phi/J
composite calibration" (the Consistency score from its two instruments). The roadmap
(v2.1) names v1.9 "two-component composite calibration" (Presence + Consistency, the
AIAS 2.0 score). v1.9 does both, in that order: it settles the Consistency score
(phi alone, or phi with J), then calibrates the Presence + Consistency composite.
"""

PHASE_ID = "v1.9"
PHASE_TITLE = "Two-Component AIAS Composite Calibration: Presence x Consistency"
PHASE_TYPE = "methodology_lock"
PREREG_TAG = "v1.9-prereg-r1"
PRESENCE_LOCK = "v1.6 (v0.25 presence_composite)"
CONSISTENCY_LOCK = "v1.8 (phi primary, J positional diagnostic)"
FEEDS_FORWARD = ["AIAS 2.0 synthesis (two-component construct claim)",
                 "v1.11 (two -> three-component calibration, after RS)"]

LINEAGE = """
Presence: v1.2 6761698, v1.3 6797679, v1.4 6799479, v1.5 6810758, v1.6 6816340; AIAS 1.0
synthesis 6817841; construct validity v0.29 6870778. Consistency: v1.7 6878818 (CV-CPC
falsified), v1.8 6963359 (phi), v0.34 6915458 (t1->t2), v0.37 (component-dissociation null;
OSF v37). Long horizon: v0.41 (t3, this lock's Stage 2). Framework: MSI Working Paper
26-132 (the six-dimension 0-100 AIAS score). Foundational: 6659000.
"""

# ===========================================================================
# DATA (frozen; extraction identical to v1.8 / v0.41)
# ===========================================================================
DATA = {
    "units": "112 brand units (v0.19 16; v0.20-v0.23 24 each); per-model recall counts k(b,m) "
             "in 0..6 (6 frames, channel-agnostic) and binary recognition per model, M = 6",
    "t1": "original substrate acquisitions (osf/v19..v23), as certified in v1.8 (reconciled "
          "bit-for-bit to v1.7 r_per_model for v0.20-v0.22)",
    "t2": "v0.34 re-acquisition (osf/v34/data)",
    "t3": "v0.41 re-acquisition (osf/v41/data), Stage 2 only",
    "extraction": "score_v41.load_wave (certified lineage, frame/count consistency asserted); "
                  "the v0.41 parity gates P1-P3 must pass before any Stage 1 statistic",
}

# ===========================================================================
# COMPONENTS
# ===========================================================================
PRESENCE = {
    "definition": "P = 100 * (C_P/6 + R_cat/18 + R_cult/18) / 3, the v0.25 presence_composite "
                  "(AIAS 1.0 lineage). Because R_cat + R_cult = R_total and pi_hat = R_total/36, "
                  "P = 100 * (C_P/6 + 2*pi_hat) / 3 exactly, so P is defined identically for all "
                  "five substrates, including v0.19 (single channel) and v0.23 (non-canonical "
                  "channels).",
    "range": "0-100; defined for every unit",
    "status": "LOCKED INPUT (not calibrated here)",
}

CONSISTENCY = {
    "phi": "v1.8 phi (quasi-binomial between-model dispersion); higher = less consistent",
    "scale": "C_phi = 100 * (1 - phi / phi_max), phi_max = F*M/(M-1) = 7.2 for M = F = 6: the "
             "value when every model names the brand in all frames or none. 100 = identical "
             "counts across models; 0 = maximal polarization. Absolute, bounded, comparable "
             "across categories (no within-category ranking). On a reduced panel phi_max uses "
             "the panel's M.",
    "partitions": "pi_hat = 1 (named by every model in every frame): C = 100 (no dispersion). "
                  "pi_hat = 0 (never named): C is NOT RATED - consistency of absence is not "
                  "consistency of availability.",
    "J_option": "C_phiJ = (C_phi + 100*J) / 2 where J is defined (>= 2 models name the brand); "
                "C_phi otherwise. v1.8 found rho(phi, J) = -0.40 (non-redundant).",
}

PRELOOK = """
Scoping look on frozen t1/t2 (osf/methodology/v1_9/scoping/prelook_v1_9.py, Nov 9, 2026; no
t3 data exist). Informed the candidate set; not a result.
- C_phi vs P: rho = 0.096 (t1, n 84), -0.041 (t2, n 88), within-substrate ranks.
- Test-retest t1->t2 (within-substrate): P 0.970; C_phi 0.533 (n 83).
- Low counts: mean C_phi = 85 for brands with 1-2 total mentions, 86 at 3-6 and 7-18, 76
  at 19-36. At one or two mentions phi sits near its binomial expectation whatever the
  models do, so C_phi is high by default and carries no information.
- Consequence for a naive average (P + C_phi)/2: brands named once score 58.0 on average
  (n 9) against 30.4 for brands never named (n 28) - a windfall from noise.
- v0.41 pre-lock calibration: within-frame model shuffles leave rho(phi_t2, phi_shuffled)
  at mean 0.39 (95th pct 0.55), so part of phi's stability is frame structure, not model
  behaviour (v0.41 SCORER_NOTES S2).
"""

# ===========================================================================
# STAGE 1 - CALIBRATION (frozen t1/t2; run before the lock)
# ===========================================================================
CANDIDATES = {
    "consistency_score": ["C_phi", "C_phiJ"],
    "low_count_rule": {
        "SHRINK": "C* = w*C + (1-w)*C_0, w = n/(n + kappa), n = total mentions (sum of k), "
                  "kappa = 6 (one model's full frame set); C_0 = 50 (scale midpoint, no "
                  "information). Defined for every recalled brand.",
        "FLOOR": "C* = C if n >= 6, else NOT RATED (composite falls back as for pi_hat = 0).",
    },
    "composite_form": {
        "ADD": "A = (P + C*)/2; A = P where C* is not rated",
        "MOD": "A = P * (0.5 + 0.5 * C*/100); A = 0.5 * P where C* is not rated "
               "(Consistency modulates Presence; a brand cannot score on Consistency alone)",
    },
    "grid": "2 x 2 x 2 = 8 specifications, all computed; none dropped after the fact",
}

CONSTRAINTS = [  # every candidate must pass all three (t1 and t2 separately)
    {"id": "K1_Dissociation", "rule": "|rho(C*, P)| <= 0.50 (within-substrate ranks, units with "
                                     "C* rated). Make-or-break: if NO candidate passes, v1.9 locks "
                                     "'no composite' and AIAS 2.0 reports the two components side "
                                     "by side."},
    {"id": "K2_Incremental", "rule": "|rho(A, P)| <= 0.95 (within-substrate ranks, all 112): the "
                                    "composite must carry information P does not."},
    {"id": "K3_NoWindfall", "rule": "mean A(1-2 mentions) - mean A(never named) <= "
                                   "[mean P(1-2 mentions) - mean P(never named)] + 5 points: one or "
                                   "two mentions may not buy more than Presence already credits."},
]

SELECTION_RULE = """
Among candidates passing K1-K3 at both t1 and t2, select the one with the highest
test-retest reliability rho(A_t1, A_t2) (within-substrate ranks, all 112 units). Candidates
within 0.01 of the best count as tied; ties go to the simpler choice in this order: C_phi
over C_phiJ, FLOOR over SHRINK, ADD over MOD. The selected specification, its Stage 1
statistics and the full 8-row table are written into this module (SELECTED, below) before
the lock commit.
"""

SELECTED = "TBD - filled by the Stage 1 run before the lock (osf/methodology/v1_9/v1_9_calibration.json)"

# ===========================================================================
# STAGE 2 - CONFIRMATION (t2 -> t3, v0.41; locked specification only)
# Verdicts CONFIRMED / MARGINAL / FALSIFIED; UNDETERMINED if v0.41 halts or n floors fail.
# ===========================================================================
HYPOTHESES = [
    {"tag": "H_Composite_Reliability", "tier": "PRIMARY",
     "statement": "The locked two-component score keeps its brand order over ~5 months.",
     "statistic": "rho(A_t2, A_t3), within-substrate ranks pooled, all units in both waves; "
                  "one-sided stratified permutation (t3 permuted within substrate), 10,000 "
                  "draws, seed 190019.",
     "confirmed_iff": "rho >= 0.80 AND p_perm < .05 AND rho >= rho(P_t2, P_t3) - 0.05",
     "falsified_iff": "rho < 0.60 OR p_perm >= .05",
     "marginal": "otherwise (including rho >= 0.80 but more than 0.05 below Presence alone)",
     "rationale": "Adding Consistency is worth it only if the composite stays nearly as "
                  "reliable as Presence; the 0.05 margin is the cost the program accepts for "
                  "a second dimension."},
    {"tag": "H_Dissociation_t3", "tier": "PRIMARY",
     "statement": "Consistency stays separable from Presence at t3.",
     "statistic": "|rho(C*_t3, P_t3)|, within-substrate ranks, units with C* rated.",
     "confirmed_iff": "|rho| <= 0.30",
     "falsified_iff": "|rho| >= 0.50",
     "marginal": "otherwise"},
    {"tag": "H_Consistency_Reliability", "tier": "SECONDARY",
     "statement": "The selected Consistency score C* is reliable beyond frame structure.",
     "statistic": "rho(C*_t2, C*_t3) (within-substrate ranks, rated in both) against the v0.41 "
                  "within-frame model-shuffle null applied to C* (10,000 draws, seed 190020).",
     "confirmed_iff": "rho >= 0.50 AND p_frame < .05",
     "falsified_iff": "rho < 0.30 OR p_frame >= .05",
     "marginal": "otherwise",
     "note": "Not double-counted with v0.41 H_Phi_LongHorizon: that tests raw phi; this tests "
             "the calibrated score that enters AIAS 2.0."},
    {"tag": "H_NoWindfall_t3", "tier": "SECONDARY",
     "statement": "The low-count rule still holds on new data.",
     "statistic": "K3 recomputed at t3.",
     "confirmed_iff": "K3 passes", "falsified_iff": "K3 fails", "marginal": "-- n/a --"},
]

DESCRIPTIVES = [
    "The 8-row Stage 1 table (all candidates, all constraints, both waves).",
    "Distribution of A by substrate at t1, t2, t3; share of units with C* not rated per wave.",
    "Each component's contribution to A's variance (within substrate).",
    "Sensitivity: the selected specification re-run with the runner-up; and without any "
    "model that v0.41 MC_Snapshot flags.",
]

PREDICTIONS = """
Stage 1: lean C_phi + FLOOR or SHRINK + ADD; K3 is the binding constraint for ADD.
H_Composite_Reliability: lean CONFIRMED on rho >= 0.80, at risk on the 0.05 margin
(t1->t2: P 0.97 vs naive composite 0.91). H_Dissociation_t3: lean CONFIRMED (0.10 / -0.04
so far). H_Consistency_Reliability: lean MARGINAL (frame structure, v0.41 S2).
"""

LIMITATIONS = """
Stage 1 selects on data already seen (declared calibration; only Stage 2 is confirmatory).
One panel (the retiring six-model legacy panel); weights and scale bind this panel until a
new panel is calibrated. Five substrates, 112 units; brand-level n per substrate 16-24.
Presence is taken as locked (no re-weighting of recognition vs recall). The composite's
validity against behaviour is not tested (Phase 3/S). The 0-100 scale is a measurement
convention, not a probability.
"""

DEVIATIONS = [
    {"entry_id": "Entry 0", "type": "ex-ante (COI + anchor)",
     "coi_screen": "No new brand selection; the five substrates carry their source-phase COI "
                   "handling unchanged (v0.22 tier-2/3 Harman / Samsung SDI / Samsung Display "
                   "disclosure; v0.19 AKG -> Denon substitution), as recorded in v0.41 Entry 0.",
     "anchor_preamble": "Stage 1 run and SELECTED filled -> content lock -> commit -> tag "
                        "v1.9-prereg-r1 -> push -> OSF deposit -> both remotes verified -> only "
                        "then the first v0.41 t3 call.",
     "lock_state": "DRAFT (not locked)"},
]
