#!/usr/bin/env python3
"""
score_v29.py — v0.29 (CV.05) Campbell-Fiske construct-validity baseline scorer.

SYNTHESIS scorer: NO acquisition, NO probes, NO CSVs. It reads the two inherited
component verdict files, extracts the Presence-level (C_P) convergent and
discriminant Spearman coefficients, assembles the 2x2 MTMM matrix, computes the
Campbell-Fiske gap C3, applies the verdict logic locked in
prereg/v0_29_cv_baseline_content.py, and writes osf/v29/v29_verdicts.json.

Inheritance contract (pinned against live JSON; lock v0.29-prereg-r1):
  C1 convergent   -> v0.25 H_CV_Primary  (hypotheses = LIST; find by name)
  C2 discriminant -> v0.26 H_PV_Pooled   (hypotheses = DICT; key access)
  C3 = |rho_conv| - |rho_disc|, pooled discriminant as the C2 referent.
  CONFIRMED iff C1 significant AND C2 (|rho| < 0.20, n.s.) AND C3 > 0.
  FALSIFIED if C3 <= 0 (Campbell-Fiske inversion).
  PARTIAL  if C3 > 0 but a leg drifts (e.g. discriminant marginally significant).

Schema divergence and bare-NaN siblings in both source files are handled below:
extraction touches ONLY the two named hypotheses, so sibling NaNs never enter
the C3 math; output is dumped with allow_nan=False to guarantee valid JSON.
"""

from __future__ import annotations
import json
import math
import argparse
import datetime
import pathlib

# ---- locked thresholds (mirror prereg/v0_29_cv_baseline_content.py) ----
C2_RHO_CEILING = 0.20      # |rho_disc| must be below this
ALPHA = 0.05               # significance boundary
PHASE = "v0.29"
PROJECT_ID = "CV.05"
PROTOCOL = "v1.6"
PREREG_TAG = "v0.29-prereg-r1"

DEFAULT_V25 = "osf/v25/v25_verdicts.json"
DEFAULT_V26 = "osf/v26/v26_verdicts.json"
DEFAULT_OUT = "osf/v29/v29_verdicts.json"

# soft sanity anchors (warn-only; catch an accidental file swap)
EXPECT_CONV_RHO = 0.7411
EXPECT_DISC_RHO = -0.0002
ANCHOR_TOL = 0.05


def load_json_with_nan(path: str) -> dict:
    """json.load tolerates bare NaN/Infinity by default (parse_constant).
    We rely on that so the loader does not choke on sibling NaN hypotheses;
    we then extract only the named C_P hypotheses, so NaN never propagates."""
    with open(path) as f:
        return json.load(f)


def _resolve(d: dict, names, ctx: str):
    """Return the first present, non-null key from `names`; else raise,
    naming the keys actually available so a schema surprise fails LOUD."""
    for k in names:
        if isinstance(d, dict) and d.get(k) is not None:
            return d[k]
    raise KeyError(f"{ctx}: none of {list(names)} present. Available: {sorted(d) if isinstance(d, dict) else type(d).__name__}")


def _stat(stats: dict, ctx: str):
    rho = float(_resolve(stats, ["rho", "spearman_rho", "r"], f"{ctx} stats"))
    p = float(_resolve(stats, ["p", "p_value", "pvalue"], f"{ctx} stats"))
    n = stats.get("n") if isinstance(stats, dict) else None
    if n is None and isinstance(stats, dict):
        n = stats.get("n_obs")
    if math.isnan(rho) or math.isnan(p):
        raise ValueError(f"{ctx}: rho/p is NaN — cannot score this leg")
    return rho, p, n


def get_convergent(v25: dict) -> dict:
    """v0.25 stores hypotheses as a LIST of dicts; locate H_CV_Primary."""
    hyps = _resolve(v25, ["hypotheses"], "v0.25 root")
    if not isinstance(hyps, list):
        raise TypeError(f"v0.25 hypotheses expected list, got {type(hyps).__name__}")
    match = next((h for h in hyps
                  if (h.get("hypothesis") or h.get("name") or h.get("id")) == "H_CV_Primary"), None)
    if match is None:
        raise KeyError("v0.25: H_CV_Primary not found in hypotheses list")
    stats = _resolve(match, ["statistics", "stats"], "v0.25 H_CV_Primary")
    rho, p, n = _stat(stats, "v0.25 H_CV_Primary")
    return {"hypothesis": "H_CV_Primary", "rho": rho, "p": p, "n": n,
            "source": "v0.25", "ssrn": "6842138"}


def get_discriminant(v26: dict) -> dict:
    """v0.26 stores hypotheses as a DICT; pooled H_PV_Pooled is the C2 referent."""
    hyps = _resolve(v26, ["hypotheses"], "v0.26 root")
    if not isinstance(hyps, dict):
        raise TypeError(f"v0.26 hypotheses expected dict, got {type(hyps).__name__}")
    pooled = _resolve(hyps, ["H_PV_Pooled"], "v0.26 hypotheses")
    # v0.26 stores rho/p/n FLAT on the hypothesis (no nested statistics block,
    # unlike v0.25). Use the nested block only if a future file provides one.
    stats = pooled.get("statistics") or pooled.get("stats") or pooled
    rho, p, n = _stat(stats, "v0.26 H_PV_Pooled")
    return {"hypothesis": "H_PV_Pooled", "rho": rho, "p": p, "n": n,
            "source": "v0.26", "ssrn": "6847678"}


def score(conv: dict, disc: dict) -> dict:
    c1_sig = conv["p"] < ALPHA
    c2_below_ceiling = abs(disc["rho"]) < C2_RHO_CEILING
    c2_nonsig = disc["p"] >= ALPHA
    c2_pass = c2_below_ceiling and c2_nonsig
    c3 = abs(conv["rho"]) - abs(disc["rho"])
    c3_pass = c3 > 0
    asymmetry = c1_sig and c2_nonsig

    if not c3_pass:
        verdict, reason = "FALSIFIED", "C3 <= 0: discriminant >= convergent (Campbell-Fiske inversion)"
    elif c1_sig and c2_pass and c3_pass:
        verdict, reason = "CONFIRMED", "C1 significant AND C2 (|rho| < 0.20, n.s.) AND C3 > 0"
    else:
        fails = []
        if not c1_sig:
            fails.append("C1 non-significant")
        if not c2_below_ceiling:
            fails.append("C2 |rho| at/above 0.20 ceiling")
        if not c2_nonsig:
            fails.append("C2 significant (discriminant correlated)")
        verdict, reason = "PARTIAL", "C3 > 0 but: " + "; ".join(fails)

    return {
        "verdict": verdict,
        "reason": reason,
        "C1_convergent": {"rho": conv["rho"], "p": conv["p"], "significant": c1_sig, "pass": c1_sig},
        "C2_discriminant": {"rho": disc["rho"], "p": disc["p"],
                            "below_ceiling": c2_below_ceiling, "nonsignificant": c2_nonsig, "pass": c2_pass},
        "C3_campbell_fiske_gap": {"value": round(c3, 4), "pass": c3_pass},
        "significance_asymmetry": asymmetry,
        "MTMM_2x2": {
            "monotrait_heteromethod_convergent": conv["rho"],  # Presence (C_P) x Google Trends
            "heterotrait_discriminant": disc["rho"],           # Presence (C_P) x Amazon BSR
        },
    }


def _anchor_warn(conv: dict, disc: dict) -> list:
    warns = []
    if abs(conv["rho"] - EXPECT_CONV_RHO) > ANCHOR_TOL:
        warns.append(f"convergent rho {conv['rho']} deviates from locked anchor {EXPECT_CONV_RHO}")
    if abs(disc["rho"] - EXPECT_DISC_RHO) > ANCHOR_TOL:
        warns.append(f"discriminant rho {disc['rho']} deviates from locked anchor {EXPECT_DISC_RHO}")
    return warns


def main():
    ap = argparse.ArgumentParser(description="v0.29 (CV.05) synthesis scorer")
    ap.add_argument("--v25", default=DEFAULT_V25, help="convergent verdicts JSON")
    ap.add_argument("--v26", default=DEFAULT_V26, help="discriminant verdicts JSON")
    ap.add_argument("--out", default=DEFAULT_OUT, help="output verdicts JSON")
    args = ap.parse_args()

    conv = get_convergent(load_json_with_nan(args.v25))
    disc = get_discriminant(load_json_with_nan(args.v26))
    result = score(conv, disc)
    warns = _anchor_warn(conv, disc)

    out = {
        "phase": PHASE,
        "project_id": PROJECT_ID,
        "protocol": PROTOCOL,
        "design_class": "synthesis",
        "hypothesis": "H_CV_Baseline",
        "scored_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "result": result,
        "provenance": {
            "lock_tag": PREREG_TAG,
            "convergent": {"source": "v0.25", "ssrn": "6842138",
                           "prereg_tag": "v0.25-prereg-r1", "file": args.v25,
                           "inherited_rho": conv["rho"], "inherited_p": conv["p"], "n": conv["n"]},
            "discriminant": {"source": "v0.26", "ssrn": "6847678",
                             "prereg_tag": "v0.26-prereg-r2", "file": args.v26,
                             "inherited_rho": disc["rho"], "inherited_p": disc["p"], "n": disc["n"]},
            "note": "Synthesis of inherited locked verdicts; no acquisition. "
                    "C3 = |rho_conv| - |rho_disc| with pooled discriminant as C2 referent.",
        },
        "warnings": warns,
    }

    outp = pathlib.Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    with open(outp, "w") as f:
        json.dump(out, f, indent=2, allow_nan=False)  # valid JSON: no bare NaN in output

    print(f"[score_v29] {result['verdict']}  "
          f"C1 rho={conv['rho']:.4f} p={conv['p']:.2e} | "
          f"C2 rho={disc['rho']:.4f} p={disc['p']:.3f} | "
          f"C3={result['C3_campbell_fiske_gap']['value']}")
    for w in warns:
        print(f"[score_v29][WARN] {w}")
    print(f"[score_v29] wrote {outp}")


if __name__ == "__main__":
    main()
