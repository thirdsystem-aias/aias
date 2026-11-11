#!/usr/bin/env python3
"""
make_scenarios_v1_12.py -- SYNTHETIC scorer outputs for testing the v1.12 (Coverage Paper A) paper pipeline.
Never real data: no v1.12 or t4 answer exists when this is written, none is read, and no API is called.

Step 1 ("scored"): the locked scorer itself (osf/methodology/v1_12/scripts/score_v1_12.py, imported read-only) runs
score_coverage() on the synthetic Coverage-shaped and t4-shaped inputs of its own unit tests
(scripts/tests/test_pipeline_v1_12.inputs: invented brand names, 900 synthetic calls), as its --synthetic mode does,
and its outputs are written with its own write_outputs(). The scorer's real output paths are never written.

Step 2 (derived scenarios): copies of that document in which the primary-panel legs are given other statistics; each
verdict word is then recomputed by the scorer's own verdict functions (verdict_separability, verdict_reliability,
verdict_replication) and the Paper A verdict by the scorer's own gate(), so every word in a scenario is one the scorer
would write for those statistics. The derived scenarios exercise every branch of the paper template:

  pass           all gate legs CONFIRMED; H5 active and gating (v1.14 Stage 1 SEPARABLE), CONFIRMED  -> PASS
  fail           H1 FALSIFIED; H5 active, reported not gating                                      -> FAIL
  marginal       H1 MARGINAL; H5 INACTIVE                                                          -> MARGINAL
  downgraded     all gate legs CONFIRMED, H7 FALSIFIED; H5 INACTIVE                                -> MARGINAL (downgrade)
  undetermined   H4 below the n floor; H5 active, Stage 1 output unavailable (N30, not gating)     -> UNDETERMINED
  instrument     MC_Situation fails (J_within - J_between below 0.10)                              -> INSTRUMENT FAIL
  fallback       as pass, but H1/H2 cross-panel (section 2.6 fallback) and GPT-6 Astra dropped (two-model)

Every file is named SYNTHETIC_<scenario>_v112_verdicts.json / SYNTHETIC_<scenario>_v112_unit_table.csv and carries
"synthetic_fixture" at the top level. Refuses any output directory under osf/.

Usage: python3 papers/v1_12/tests/make_scenarios_v1_12.py OUTDIR [--draws N] [scenario ...]
"""
import argparse
import copy
import hashlib
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "osf/methodology/v1_12/scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SCRIPTS / "tests"))
import score_v1_12 as S  # noqa: E402
import test_pipeline_v1_12 as TP  # noqa: E402

SCENARIOS = ["scored", "pass", "fail", "marginal", "downgraded", "undetermined", "instrument", "fallback"]
NAN = float("nan")


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def scored(draws):
    inp = TP.inputs(seed=0)
    t0 = time.time()
    doc, rows = S.score_coverage(inp, S.Cfg(draws, draws), {"enforce": True, "require_p1": False})
    doc["inputs"] = {"raw": "SYNTHETIC: test_pipeline_v1_12.inputs(seed=0), in process", "raw_sha256": None,
                     "coded": "SYNTHETIC", "t4": {"raw": "SYNTHETIC"}, "t4_missing": [],
                     "scorer_sha256": _sha(SCRIPTS / "score_v1_12.py"), "coder": "not loaded (synthetic mentions)"}
    print(f"  scorer ran in {time.time() - t0:.0f} s ({draws} draws)")
    return S._clean(doc), rows


def set_leg(leg, kind, rho, p=None, below=False):
    """Give a leg new statistics; its interval is shifted with it; the verdict is the scorer's function."""
    old = leg.get("rho_w")
    leg["rho_w"] = rho
    if leg.get("ci95_rho_w") and old is not None:
        leg["ci95_rho_w"] = [min(1.0, max(-1.0, c + rho - old)) for c in leg["ci95_rho_w"]]
    if kind == "rel":
        leg["transformed"] = S.spearman_brown_half(rho)
        if leg.get("ci95_rho_w"):
            leg["ci95_transformed"] = [S.spearman_brown_half(c) for c in leg["ci95_rho_w"]]
    if p is not None:
        leg["p_perm"] = p
    if below:
        leg["below_n_floor"] = True
        leg["n"] = min(leg.get("n") or 0, 24)
    leg["verdict"] = S.VERDICT_FN[kind](dict(leg, rho_w=rho, p_perm=leg.get("p_perm", NAN)))
    return leg


KIND = {"H1_Sep_Presence": "sep", "H2_Sep_Consistency": "sep", "H3_Sep_NamingRate": "sep", "H4_Reliability": "rel",
        "H5_Sep_Ranking": "sep", "H6_Sep_Sentiment": "sep", "H7_Sep_Presence_Legacy": "sep",
        "H8_Panel_Replication": "rep"}


def h5_record(state, base_leg):
    """H5 in the shapes the scorer writes (legs_for / h5_source_record): INACTIVE, gating, reported, unavailable."""
    if state == "inactive":
        return {"verdict": "INACTIVE", "reason": "activation rule (section 3): tag not pushed before the lock"}, None
    if state == "unavailable":
        return ({"verdict": "UNDETERMINED", "reason": "leg active but no locked score was supplied (N30)"},
                {"measure": f"R*_S0 of {S.V114_PREREG_TAG} (modal position)", "status": "NOT_AVAILABLE",
                 "reason": "SYNTHETIC: v1.14 Stage 1 halted", "h5_gates": False})
    leg = copy.deepcopy(base_leg)
    src = {"file": "SYNTHETIC", "sha256": None, "condition": "S0", "prereg_tag": S.V114_PREREG_TAG,
           "stage1_verdict": "SEPARABLE (Stage 2 pending)" if state == "gating" else "MARGINAL",
           "rated_units": leg.get("n"), "h5_gates": state == "gating",
           "measure": f"R*_S0 of {S.V114_PREREG_TAG} (modal position, lead-item rule, floor 6)",
           "MNP_comparability_non_gating": {"rho_w": 0.21, "n": leg.get("n"), "p_perm": 0.04,
                                            "band_reading": "CONFIRMED", "gating": False}}
    return leg, src


PLAN = {  # leg -> (rho, p, below the n floor)
    "pass": {"H1_Sep_Presence": (0.142, 0.03, False), "H2_Sep_Consistency": (-0.081, 0.31, False),
             "H3_Sep_NamingRate": (0.037, 0.66, False), "H4_Reliability": (0.583, 0.0002, False),
             "H7_Sep_Presence_Legacy": (0.188, 0.02, False), "H8_Panel_Replication": (0.812, 0.0001, False)},
    "fail": {"H1_Sep_Presence": (0.574, 0.0001, False), "H2_Sep_Consistency": (0.122, 0.11, False),
             "H3_Sep_NamingRate": (-0.064, 0.41, False), "H4_Reliability": (0.471, 0.0004, False),
             "H7_Sep_Presence_Legacy": (0.611, 0.0001, False), "H8_Panel_Replication": (0.744, 0.0001, False)},
    "marginal": {"H1_Sep_Presence": (0.412, 0.0001, False), "H2_Sep_Consistency": (0.093, 0.22, False),
                 "H3_Sep_NamingRate": (0.051, 0.52, False), "H4_Reliability": (0.522, 0.0003, False),
                 "H7_Sep_Presence_Legacy": (0.377, 0.0001, False), "H8_Panel_Replication": (0.633, 0.0001, False)},
    "downgraded": {"H1_Sep_Presence": (0.244, 0.002, False), "H2_Sep_Consistency": (0.019, 0.81, False),
                   "H3_Sep_NamingRate": (-0.112, 0.15, False), "H4_Reliability": (0.536, 0.0002, False),
                   "H7_Sep_Presence_Legacy": (0.523, 0.0001, False), "H8_Panel_Replication": (0.722, 0.0001, False)},
    "undetermined": {"H1_Sep_Presence": (0.201, 0.01, False), "H2_Sep_Consistency": (0.044, 0.62, False),
                     "H3_Sep_NamingRate": (0.012, 0.88, False), "H4_Reliability": (0.388, 0.04, True),
                     "H7_Sep_Presence_Legacy": (0.233, 0.01, False), "H8_Panel_Replication": (0.302, 0.08, False)},
    "instrument": {"H1_Sep_Presence": (0.688, 0.0001, False), "H2_Sep_Consistency": (0.301, 0.001, False),
                   "H3_Sep_NamingRate": (0.155, 0.06, False), "H4_Reliability": (0.214, 0.03, False),
                   "H7_Sep_Presence_Legacy": (0.702, 0.0001, False), "H8_Panel_Replication": (0.418, 0.002, False)},
}
PLAN["fallback"] = PLAN["pass"]
H5_STATE = {"pass": "gating", "fail": "reported", "marginal": "inactive", "downgraded": "inactive",
            "undetermined": "unavailable", "instrument": "inactive", "fallback": "gating"}


def derive(base, name):
    d = copy.deepcopy(base)
    legs = d["legs"]
    tmpl = copy.deepcopy(legs["H1_Sep_Presence"])          # a computed separability leg, for H5's shape
    for h, (rho, p, below) in PLAN[name].items():
        set_leg(legs[h], KIND[h], rho, p, below)
    h5_state = H5_STATE[name]
    leg5, src5 = h5_record(h5_state, tmpl)
    if h5_state in ("gating", "reported"):
        set_leg(leg5, "sep", 0.553 if name == "fail" else 0.176, 0.02)
    legs["H5_Sep_Ranking"] = leg5
    d.pop("H5_ranking_source", None)
    if src5 is not None:
        d["H5_ranking_source"] = src5
    d["verdicts"] = {h: legs[h]["verdict"] for h in legs}
    msit = d["MC"]["MC_Situation"]
    if name == "instrument":
        msit["pooled_mean_J_within_minus_J_between"] = 0.062
        msit["passed"] = False
    else:
        msit["pooled_mean_J_within_minus_J_between"] = max(msit.get("pooled_mean_J_within_minus_J_between") or 0, 0.18)
        msit["pooled_mean_J_between"] = min(msit.get("pooled_mean_J_between") or 1.0, 0.31)
        msit["passed"] = True
    gate_active = {"H5_Sep_Ranking": h5_state == "gating", "H6_Sep_Sentiment": False}   # N35: only SEPARABLE gates
    g = S.gate(msit["passed"], d["verdicts"], gate_active, False, two_model=(name == "fallback"))
    if h5_state == "reported":
        g["notes"].append(f"H5_Sep_Ranking ({d['verdicts']['H5_Sep_Ranking']}) reported, not gating: v1.14's Stage 1 "
                          f"verdict is not SEPARABLE (N35)")
        g["h5_reported_not_gating"] = d["verdicts"]["H5_Sep_Ranking"]
    if name == "fallback":
        d["comparators"] = {"source": "AIAS 2.0 t3 (cross-panel)", "cross_panel": True,
                            "reason": "SYNTHETIC: t4 (v0.42) outputs not available at analysis"}
        g["notes"].append("H1 and H2 computed cross-panel against the published AIAS 2.0 t3 values (section 2.6 "
                          "fallback: SYNTHETIC)")
        g["label"] += " (H1, H2 cross-panel) (two-model)"
        d["models_dropped_section_7_3"] = [S.GPT6]
        d["MC"]["MC_Complete"]["dropped_models"] = [S.GPT6]
        pm = d["MC"]["MC_Complete"]["per_model"][S.GPT6]
        pm["answered"], pm["share"], pm["below_90pct"] = 187, 187 / 225, True
        d["panels"] = {k: [m for m in v if m != S.GPT6] for k, v in d["panels"].items()}
    d["paper_A_verdict"] = g
    d["synthetic_fixture"] = {"scenario": name, "derived_from": "scored",
                              "note": "SYNTHETIC: leg statistics set by make_scenarios_v1_12.py; verdict words from "
                                      "the scorer's verdict functions and gate()"}
    return d


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("out", type=Path)
    ap.add_argument("scenarios", nargs="*", default=SCENARIOS)
    ap.add_argument("--draws", type=int, default=999)
    a = ap.parse_args(argv)
    out = a.out.resolve()
    if str(out).startswith(str((ROOT / "osf").resolve())):
        raise SystemExit(f"REFUSED: {out} is under osf/ (the scorer's real output location)")
    out.mkdir(parents=True, exist_ok=True)
    base, rows = scored(a.draws)
    base["synthetic_fixture"] = {"scenario": "scored", "note": "SYNTHETIC: the scorer's own output on synthetic inputs"}
    for name in a.scenarios:
        doc = base if name == "scored" else derive(base, name)
        S.write_outputs(doc, rows, out / f"SYNTHETIC_{name}_v112_verdicts.json",
                        out / f"SYNTHETIC_{name}_v112_unit_table.csv")
        print(f"{name}: Paper A {doc['paper_A_verdict']['label']} | "
              + ", ".join(f"{h.split('_')[0]} {v}" for h, v in doc["verdicts"].items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
