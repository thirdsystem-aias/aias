"""
protocol/thresholds.py — canonical numerical thresholds

Every threshold used by score_vNN.py and acquire_*.py lives here, tagged
with the protocol version that locked it. Phase scripts import; they do
not redefine.

Threshold provenance:
  - v1.2 (SSRN 6761698) — four-regime taxonomy thresholds (C2 / C3)
  - v1.3 (SSRN 6797679) — Phase A pivot threshold + cascade rule
  - v1.4 (SSRN 6799479) — Recognition × Recall thresholds
  - pre-reg r3 §2.3 (per-phase) — Spearman/bootstrap parameters for §5.2

When a threshold changes, bump the protocol version and update the
PROTOCOL_VERSION constant in protocol/__init__.py simultaneously.
"""


# ============================================================
# C1 — Panel adequacy (locked at v1.2)
# ============================================================
# Worldwide post-attrition n must clear this floor for any verdict
# beyond NULL. Sourced from v1.2 four-regime taxonomy.

C1_PANEL_ADEQUACY_FLOOR = 12


# ============================================================
# C2 — Regime 4 mention concentration (locked at v1.2)
# ============================================================
# Operationalizes the Regime 4 retrieval signature. The exact
# operationalization (top-2-share vs. Gini vs. Herfindahl) is
# protocol-canonical and consistent across phases.
#
# TODO ONE-TIME LIFT: Copy the locked value from your existing v17
# scoring code (likely scripts/score_v17.py). After this lift,
# never again — all future phases inherit.

C2_REGIME4_MENTION_THRESHOLD: float | None = None  # TODO: lift from score_v17.py
C2_OPERATIONALIZATION = "top_2_share"  # TODO: confirm against score_v17.py


# ============================================================
# C3 — Ranking coherence (locked at v1.2)
# ============================================================
# Operationalizes within-cell rank-order coherence between mention
# rate and anchor-pivot prominence. Protocol-canonical.
#
# TODO ONE-TIME LIFT: Copy from score_v17.py.

C3_RANKING_COHERENCE_THRESHOLD: float | None = None  # TODO: lift from score_v17.py


# ============================================================
# Phase A — Pivot anchoring (locked at v1.3)
# ============================================================

PIVOT_C_P_THRESHOLD = 6        # 6/6 across the 6-slot panel = pivot-eligible
PHASE_A_PANEL_SIZE = 6         # six-slot reference panel


# ============================================================
# Recognition × Recall (locked at v1.4 + pre-reg r3 §2.3)
# ============================================================

# Iwachu-pattern dissociation thresholds (v1.4)
DISSOCIATION_C_P_FLOOR = 5             # brand C_P ≥ 5/6
DISSOCIATION_MENTION_CEILING = 2       # brand Phase B mention count ≤ 2/18

# Pooled Recognition–Recall correlation threshold (pre-reg r3 §2.3)
# Used to route 0-dissociation-case outcomes to NARROWED vs UNDETERMINED
RECOGNITION_RECALL_CORRELATION_THRESHOLD = 0.5    # Spearman ρ ≥ 0.5
RECOGNITION_RECALL_CI_LOWER_FLOOR = 0.3           # bootstrap 95% CI lower > 0.3

# Bootstrap parameters
BOOTSTRAP_N_RESAMPLES = 10_000
BOOTSTRAP_RNG_SEED = 20260520          # date-of-pre-reg-lock derived seed


# ============================================================
# Phase D — Within-cell ρ (planned-from-start as of v0.18)
# ============================================================

PHASE_D_RHO_MIN_CELL_N = 5             # post-attrition n ≥ 5 for ρ computation
