#!/usr/bin/env python3
"""Cost estimate for v0.46 (#76) Stage 1 Registered Report manuscript, draft r1 (2026-11-21; DRAFT, nothing run).

No model is called. Adds to cost r1 (cost_estimate_v0_46_r1.py, imported unchanged) the cost of
re-measuring Presence and Ranking inside #76, in the same post-IPA collection (Pablo, 2026-11-17,
venue-plan decisions item 4: keep PCI RR bias-control Level 6).

Re-measure design = t4's (v0.42) search-off blocks for the four #76 categories only (v0.20 skincare,
v0.21 cosmetics, v0.22 cars, v0.23 premium spirits; headphones v0.19 excluded, D8):
  Phase B S0: 6 category questions x 4 categories x 3 runs = 72 calls per model
  Phase A S0: 24 + 24 + 24 yes/no recognition questions (v0.20-v0.22) + 24 open v0.23 questions = 96 per model
  -> 168 calls per model, 504 for three models; plus the v0.23 recognition judge on 72 answers.
Basis: the recorded usage of exactly these calls at t4 (git v0.42-scoring-locked:osf/v42/data/t4_raw.jsonl),
re-priced with R0's functions and price table (osf/v45/scripts/budget_v0_45.py; prices read 2026-11-11 and
re-read for cost r1 on 2026-11-14), every call priced on 2026-12-01 (Gemini 4 Argon at its December price).
  central = sum of the re-priced recorded t4 calls (the same prompts), +2% for re-sends (as cost r1)
  high    = calls x the 90th-percentile cost of that call class in these four categories, +10% (as cost r1)
Judge: 72 v0.23 Phase A answers, at most 1,500 input and 10 output tokens each (v0.45 pre-registration 4.5),
Claude Sonnet 5.5 standard $2 / $10 (budget_v0_45.py); plus v0.45's $2.50 judge reserve, counted as spent.
Writes osf/v46/prereg/cost_estimate_v0_46_stage1_r1.json and .txt.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cost_estimate_v0_46 as R0      # noqa: E402
import cost_estimate_v0_46_r1 as R1   # noqa: E402

MODELS = R1.MODELS
SUBS = ("v20", "v21", "v22", "v23")
CLASSES = ("B-S0", "A-yn", "A-open")
JUDGE_N, JUDGE_IN, JUDGE_OUT = 72, 1500, 10
JUDGE_RESERVE = 2.50
PAUSE, CAP = 80.0, 100.0


def recorded_in(rec):
    parts = rec.get("usage_parts")
    if isinstance(parts, str):
        parts = R0.ast.literal_eval(parts)
    v = rec.get("input_tokens")
    if v is None:
        v = sum((p.get("input_tokens") or 0) for p in (parts or []))
    return v or 0


def remeasure(lines):
    """Per model x class: count, central (replay +2%), high (count x p90 +10%) for the four categories."""
    keep = [r for r in lines if r.get("substrate") in SUBS and R0.qtype(r) in CLASSES
            and (r["phase"] == "B" or (r.get("condition"), r.get("run")) == ("S0", 1))]
    rows, tot = {}, {"calls": 0, "central": 0.0, "high": 0.0}
    for m in MODELS:
        for cls in CLASSES:
            recs = [r for r in keep if r["model_requested"] == m and R0.qtype(r) == cls]
            costs = sorted(R0.call_cost(m, r, recorded_in(r)) for r in recs)
            if not costs:
                continue
            p90 = costs[min(len(costs) - 1, int(0.9 * len(costs)))]
            c = sum(costs) * R0.RESEND["central"]
            h = len(costs) * p90 * R0.RESEND["high"]
            rows[f"{m}|{cls}"] = {"calls": len(costs), "central": round(c, 2), "high": round(h, 2),
                                  "mean_call": round(sum(costs) / len(costs), 5), "p90_call": round(p90, 5)}
            tot["calls"] += len(costs)
            tot["central"] += c
            tot["high"] += h
    return rows, {k: (round(v, 2) if isinstance(v, float) else v) for k, v in tot.items()}


def judge_cost():
    pin, pout = R0.BG.prices("claude-sonnet-5-5", "standard", R0.WHEN)
    return round(JUDGE_N * (JUDGE_IN * pin + JUDGE_OUT * pout) / 1e6, 2), (pin, pout)


def main():
    lines = R0.load()
    by = R0.basis(lines)
    choice = {lv: R0.design_cost(by, MODELS, R1.N_LIST, R1.N_OPEN, lv)[0] for lv in ("central", "high")}
    choice_e = {lv: R0.design_cost(by, MODELS, R1.N_LIST // 2, R1.N_OPEN, lv)[0] for lv in ("central", "high")}
    choice_f = {lv: R0.design_cost(by, MODELS, 2 * R1.N_LIST, 2 * R1.N_OPEN, lv)[0] for lv in ("central", "high")}
    rows, rm = remeasure(lines)
    jc, jp = judge_cost()
    extra = {lv: round(rm[lv] + JUDGE_RESERVE, 2) for lv in ("central", "high")}
    out = {"source": f"git {R0.TAG}:{R0.RAW}", "prices_on": R0.WHEN[:10],
           "prices_file": "osf/v45/scripts/budget_v0_45.py (read 2026-11-11; re-read for cost r1 2026-11-14)",
           "remeasure_by_model_class": rows, "remeasure_total": rm,
           "judge": {"answers": JUDGE_N, "usd": jc, "price_in_out": jp, "reserve_counted": JUDGE_RESERVE,
                     "note": "the judge cost is inside the reserve"},
           "remeasure_with_reserve": extra,
           "choice_design_A_r1": choice,
           "stage1_total_design_A": {lv: round(choice[lv] + extra[lv], 2) for lv in extra},
           "stage1_total_design_E_one_square": {lv: round(choice_e[lv] + extra[lv], 2) for lv in extra},
           "stage1_total_design_F_four_squares_12_runs": {lv: round(choice_f[lv] + extra[lv], 2) for lv in extra}}
    a = out["stage1_total_design_A"]
    out["checks"] = {"central_below_pause_80": a["central"] < PAUSE, "high_below_pause_80": a["high"] < PAUSE,
                     "high_below_cap_100": a["high"] < CAP, "remeasure_calls_504": rm["calls"] == 504}
    path = HERE.parent / "prereg" / "cost_estimate_v0_46_stage1_r1.json"
    path.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    txt = [f"source {out['source']}; prices on {out['prices_on']} from {out['prices_file']}"]
    for k, v in rows.items():
        txt.append(f"  re-measure {k:26s} {v['calls']:4d} calls  central ${v['central']:6.2f}  high ${v['high']:6.2f}"
                   f"  (mean/call ${v['mean_call']:.4f}, p90/call ${v['p90_call']:.4f})")
    txt.append(f"re-measure total {rm['calls']} calls: central ${rm['central']:.2f}, high ${rm['high']:.2f}")
    txt.append(f"v0.23 judge {JUDGE_N} answers ${jc:.2f} at {jp}; reserve ${JUDGE_RESERVE:.2f} counted instead")
    txt.append(f"re-measure + judge reserve: central ${extra['central']:.2f}, high ${extra['high']:.2f}")
    txt.append(f"choice design A (cost r1): central ${choice['central']:.2f}, high ${choice['high']:.2f}")
    for k in ("stage1_total_design_A", "stage1_total_design_E_one_square", "stage1_total_design_F_four_squares_12_runs"):
        txt.append(f"{k}: central ${out[k]['central']:.2f}, high ${out[k]['high']:.2f}")
    txt.append(f"checks {out['checks']}")
    path.with_suffix(".txt").write_text("\n".join(txt) + "\n")
    print("\n".join(txt))


if __name__ == "__main__":
    main()
