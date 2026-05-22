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
# C2 — Regime 4 mention concentration (locked r4, v1.4 framework)
# ============================================================
# v1.4 framework operationalization. Sourced from v0.18-prereg-r4 §4.0.
# NOT lifted from v0.16 (v1.2 framework, different methodology).

# Per-cell threshold: top-2 share of within-cell Phase B mentions
C2_REGIME4_TOP2_SHARE_THRESHOLD = 0.50

# Substantive IL-gradient guard: Cell B's top-2 share must exceed
# Cell C's top-2 share by at least this much for H_Regime4_indie_fragrance
# to CONFIRM (prevents uniform-concentration false positives)
C2_IL_GRADIENT_SEPARATION_MIN = 0.10

# Secondary informational metric (reported, not gated)
C2_REGIME4_TOP3_SHARE_INFORMATIONAL = 0.65

# Legacy alias preserved for backwards-compatibility with score_v18.py
# (older drafts used the C2_REGIME4_MENTION_THRESHOLD name)
C2_REGIME4_MENTION_THRESHOLD: float = C2_REGIME4_TOP2_SHARE_THRESHOLD
C2_OPERATIONALIZATION = "top_2_share_with_il_gradient_guard"


# ============================================================
# C3 — Within-cell ranking coherence (locked r4, v1.4 framework)
# ============================================================
# v1.4 framework: Spearman ρ between within-cell Phase B mention rank
# and within-cell Phase A C_P rank. Phase A C_P serves as the
# in-protocol prominence anchor.

# Per-cell threshold (Cohen's "large effect" convention, matches §2.3's
# Recognition–Recall correlation threshold for cross-use consistency)
C3_RANKING_COHERENCE_THRESHOLD = 0.50

# Cells must clear C3 in ≥ 2 of 3 cells at post-attrition cell n ≥ 5
# (cells with n < 5 are not counted in either direction)
C3_MIN_CELLS_CLEARING = 2
C3_TOTAL_CELLS = 3


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
