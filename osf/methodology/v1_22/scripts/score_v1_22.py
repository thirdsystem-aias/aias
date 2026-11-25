"""v1.22 Grounding Paper B scorer -- STUB (draft r0, 2026-11-25).

Holds the constants, the pre-registered decision tables (sections 1, 3.5, 3.6) and the
refusal guards. Data paths (t4/t5 loaders, G* via v1.13's imported functions, the
structure tests) are r1 work. Nothing here reads real data or calls a model.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PHASE = HERE.parent
REPO = PHASE.parents[2]
PREREG_TAG = "v1.22-prereg-r1"
V113_SCORER = REPO / "osf/methodology/v1_13/scripts/score_v1_13.py"
V113_SCORER_SHA256 = "fee2e5530030730ca964bb080840db4ca3b66b68b8c1d1ae3bb988dbd17a8641"
V113_VERDICTS = REPO / "osf/methodology/v1_13/v1_13_verdicts.json"
PHANTOM_ROSTER_SHA256 = "9b67e89231f4cab8ef6916a04acb886e8bab723fe71f4b308f9406938cb873cb"
DECISION_FILE = PHASE / "anchor" / "pablo_decision_paper_B.json"
CONDITIONAL_LABEL = "conditional on a MARGINAL Paper A gate (H1 MARGINAL, H3 UNDETERMINED)"

SEEDS = {"HB1": 122001, "HB2": 450046, "HB3": 122003, "HB4": 122004,
         "HB44": 122441, "HB44b": 122442, "HB45_t5t6": 122451, "HB45_t4t6": 122452,
         "HB46": 122461, "HB46b": 122462, "HB47": 122471, "HB47b": 122472,
         "HB48": 122481, "HB48b_full": 122482, "HB48b_resid": 122483}
DRY_RUN_SEEDS = (122490, 122491, 122492, 122493, 122494)

C, M, F, U = "CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED"


# ---- section 1: conditionality ------------------------------------------------
def paper_b_route(paper_a_verdict, decision):
    """Return 'RUN', 'NOT_RUN_PENDING', 'NOT_RUN_DECLINED' or 'REFUSED'."""
    if paper_a_verdict != "MARGINAL":
        return "REFUSED"
    if not decision:
        return "NOT_RUN_PENDING"
    if not (decision.get("date") and decision.get("text")) or "go" not in decision:
        return "NOT_RUN_PENDING"
    return "RUN" if decision["go"] is True else "NOT_RUN_DECLINED"


def read_decision(path=DECISION_FILE):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return None


# ---- section 3.2: HB2 retest (v0.45 section 2.6 bands) -------------------------
def retest_verdict(rho, p, n):
    if rho is None or n < 30:
        return U
    if rho >= 0.50 and p < 0.05:
        return C
    if rho < 0.30:
        return F
    return M


# ---- section 3.5: reliability condition R and gate completion GB -----------------
def reliability_condition(hb2, hb3):
    vs = (hb2, hb3)
    if C in vs and F in vs:
        return "MIXED"
    if C in vs:
        return "MET"
    if F in vs:
        return "FAILED"
    return "OPEN"


def gate_completion(hb1, hb2, hb3, hb4):
    r = reliability_condition(hb2, hb3)
    if hb1 == F or r == "FAILED" or hb4 == F:
        return "FAIL"
    if hb1 == C and r == "MET":
        return "PASS"
    if hb1 == U or (r == "OPEN" and hb2 == U and hb3 == U):
        return "UNDETERMINED"
    return "MARGINAL"


# ---- section 3.6: structure-study bands ------------------------------------------
def one_sided_assoc_verdict(rho, p, n, floor=30):
    """#44 (v1.13 H7 bands)."""
    if rho is None or n < floor:
        return U
    if rho >= 0.30 and p < 0.05:
        return C
    if rho <= 0.10:
        return F
    return M


def signed_band_verdict(stat, p, enough, predicted_sign, conf=0.30, null=0.15):
    """#46 (Cliff's delta, v1.19 H34) and #47b (rho_w, v1.19 H35): sign split."""
    if not enough or stat is None:
        return U
    if abs(stat) >= conf and p < 0.05:
        return C if (stat > 0) == (predicted_sign > 0) else "CONFIRMED_REVERSED"
    if abs(stat) < null:
        return F
    return M


def channel_verdict(dbar, p, n, min_cat_units):
    """#47 primary: mean within-brand difference, percentage points (C9 bands)."""
    if dbar is None or n < 20 or min_cat_units < 3:
        return U
    if dbar >= 5 and p < 0.05:
        return C
    if dbar < 2:
        return F
    return M


def replication_verdict(r, p, n):
    """#48 primary (v1.19 D9 bands)."""
    if r is None or n < 30:
        return U
    if r >= 0.20 and p < 0.05:
        return C
    if r < 0.10 or p >= 0.05:
        return F
    return M


def main(argv=None):
    raise SystemExit("v1.22 scorer stub (r0): data stages are not implemented; nothing to run.")


if __name__ == "__main__":
    main()
