#!/usr/bin/env python3
"""Cost estimate for v0.46 (#76) Stage 1 manuscript r4 (2026-11-24): D7 = cell_d applied. No model is called.

Same basis, prices and functions as stage1 r1 (cost_estimate_v0_46_stage1_r1.py, and through it cost r1 / r0,
all imported unchanged): t4's recorded usage (git v0.42-scoring-locked:osf/v42/data/t4_raw.jsonl) re-priced with
osf/v45/scripts/budget_v0_45.py, every call priced on 2026-12-01. The only change: the number of LIST calls is
taken from the live units of the probe builder (build_probes_v0_46.live_units(), which follows the logged D7
record osf/v46/prereg/d7_fisker_v0_46.json) instead of cost r1's fixed L = 24/24/19/24. With the record's outcome
(cell_d) the cars list has 18 brands: 90 live units, 180 LIST + 72 OPEN calls per model, 756 choice calls.
The predictor blocks (504 calls) and the judge reserve (US$2.50) do not depend on the unit set.
Also gives the cumulative cost by block (section 3.9) and the projection after C1 (section 3.9 iii).
Writes osf/v46/prereg/cost_estimate_v0_46_stage1_r2.json and .txt.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_probes_v0_46 as BP                # noqa: E402
import cost_estimate_v0_46 as R0               # noqa: E402
import cost_estimate_v0_46_r1 as R1            # noqa: E402
import cost_estimate_v0_46_stage1_r1 as SE     # noqa: E402

MODELS = SE.MODELS
LEVELS = ("central", "high")


def design(fisker_defunct=None):
    """Live units per category and the per-model call counts of design A for a D7 outcome (None = the record's)."""
    fd = BP.FISKER_DEFUNCT_DEFAULT if fisker_defunct is None else fisker_defunct
    L = {c: len(v) for c, v in BP.live_units(fd).items()}
    return fd, L, BP.N_SQUARES * sum(L.values()), R1.N_OPEN


def choice_cost(by, n_list, n_open):
    return {lv: R0.design_cost(by, MODELS, n_list, n_open, lv)[0] for lv in LEVELS}


def estimate(fisker_defunct=None, lines=None):
    lines = R0.load() if lines is None else lines
    by = R0.basis(lines)
    fd, L, n_list, n_open = design(fisker_defunct)
    _rows, rm = SE.remeasure(lines)
    jc, jp = SE.judge_cost()
    extra = {lv: rm[lv] + SE.JUDGE_RESERVE for lv in LEVELS}
    m = len(MODELS)
    designs = {}
    for name, nl, no in (("A", n_list, n_open), ("E", n_list // 2, n_open), ("F", 2 * n_list, 2 * n_open)):
        ch = choice_cost(by, nl, no)
        designs[name] = {"choice_calls": m * (nl + no), "predictor_calls": rm["calls"],
                         "choice": {lv: round(ch[lv], 2) for lv in LEVELS},
                         "total": {lv: round(ch[lv] + extra[lv], 2) for lv in LEVELS}}
    cum = dict(extra)
    blocks = [{"block": "P1-P4 + judge reserve", "calls": rm["calls"],
               **{lv + "_cumulative": round(cum[lv], 2) for lv in LEVELS}}]
    for lab, nl, no in (("C1 LIST square 1", n_list // 2, 0), ("C2 OPEN", 0, n_open),
                        ("C3 LIST square 2", n_list // 2, 0)):
        bc = choice_cost(by, nl, no)
        for lv in LEVELS:
            cum[lv] += bc[lv]
        blocks.append({"block": lab, "calls": m * (nl + no), **{lv + "_block": round(bc[lv], 2) for lv in LEVELS},
                       **{lv + "_cumulative": round(cum[lv], 2) for lv in LEVELS}})
    c1 = choice_cost(by, n_list // 2, 0)
    n_c1, n_rest = m * (n_list // 2), m * (n_list // 2 + n_open)
    proj = {lv: round(extra[lv] + c1[lv] + c1[lv] * n_rest / n_c1, 2) for lv in LEVELS}
    a = designs["A"]["total"]
    return {"source": f"git {R0.TAG}:{R0.RAW}", "prices_on": R0.WHEN[:10],
            "d7_fisker_defunct": fd, "live_units": L, "live_units_total": sum(L.values()),
            "calls_per_model": {"LIST": n_list, "OPEN": n_open, "predictor": rm["calls"] // m},
            "calls_total": m * (n_list + n_open) + rm["calls"],
            "remeasure_total": rm, "judge": {"answers": SE.JUDGE_N, "usd": jc, "price_in_out": jp,
                                             "reserve_counted": SE.JUDGE_RESERVE},
            "remeasure_with_reserve": {lv: round(extra[lv], 2) for lv in LEVELS},
            "designs": designs, "blocks": blocks,
            "projection_after_C1": {"factor": f"{n_rest}/{n_c1}", **proj},
            "checks": {"central_below_pause_80": a["central"] < SE.PAUSE, "high_below_pause_80": a["high"] < SE.PAUSE,
                       "high_below_cap_100": a["high"] < SE.CAP, "remeasure_calls_504": rm["calls"] == 504,
                       "projection_high_below_cap_100": proj["high"] < SE.CAP}}


def main():
    out = estimate()
    live = estimate(fisker_defunct=False)          # reproduces stage1 r1 (Fisker live): a check of the basis
    out["check_fisker_live_reproduces_stage1_r1"] = {"A_total": live["designs"]["A"]["total"],
                                                     "calls_total": live["calls_total"]}
    path = HERE.parent / "prereg" / "cost_estimate_v0_46_stage1_r2.json"
    path.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    txt = [f"source {out['source']}; prices on {out['prices_on']}; D7 Fisker Cell D = {out['d7_fisker_defunct']}",
           f"live units {out['live_units']} = {out['live_units_total']}; calls per model {out['calls_per_model']}; "
           f"calls in all {out['calls_total']}",
           f"re-measure {out['remeasure_total']}; judge {out['judge']}",
           f"re-measure + judge reserve: {out['remeasure_with_reserve']}"]
    for k, v in out["designs"].items():
        txt.append(f"design {k}: {v['choice_calls']} choice + {v['predictor_calls']} predictor calls; choice "
                   f"{v['choice']}; total {v['total']}")
    for b in out["blocks"]:
        txt.append(f"  block {b['block']:22s} {b['calls']:4d} calls  cumulative central ${b['central_cumulative']:.2f}"
                   f"  high ${b['high_cumulative']:.2f}")
    txt.append(f"projection after C1 (spend + C1 x {out['projection_after_C1']['factor']}): "
               f"central ${out['projection_after_C1']['central']:.2f}, high ${out['projection_after_C1']['high']:.2f}")
    txt.append(f"check (Fisker live, = stage1 r1): {out['check_fisker_live_reproduces_stage1_r1']}")
    txt.append(f"checks {out['checks']}")
    path.with_suffix(".txt").write_text("\n".join(txt) + "\n")
    print("\n".join(txt))


if __name__ == "__main__":
    main()
