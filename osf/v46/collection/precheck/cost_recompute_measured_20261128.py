"""DRAFT (runner, Sat 2026-11-28; not committed). Section 3.9 recompute for the panel of Section 3.3 on 2026-11-28,
on MEASURED token counts (Pablo's option C, Fri 9:58 pm): as cost_recompute_new_panel_DRAFT.py (locked estimators
imported unchanged; t4 records as basis; gpt-6.2-astra on gpt-6-astra's records, gemini-4-carbon on gemini-4-argon's),
except that the output multiplier on each new model's basis is MEASURED instead of assumed: from the v0.46 length check
(osf/v46/data/v46_length_check.json), the paired billed-output ratio new/old on the same 24 v0.39 probes under the
same settings (gpt-6.2-astra vs gpt-6-astra; gemini-4-carbon vs gemini-4-argon, both 2026-11-13 check):
  central multiplier = ratio of sums; high multiplier = the larger of ratio of sums and ratio of 90th percentiles.
Variant B (reported): multipliers floored at 1.0 (no credit for a model answering shorter than its predecessor).
Variant 0 (reported): the r0 assumption (Astra x1, Carbon x2 / x3), = cost_recompute_new_panel_DRAFT.json.
Prices: the overlay read 2026-11-28 (prices_v0_46_collection.py), every call priced at 2026-12-01 as Section 3.9 does.
Writes only cost_recompute_measured_DRAFT.json in this folder."""
import json
import sys
from pathlib import Path

WT = Path("/Users/pablou/aias/_worktrees/v0.46-stage1")
sys.path.insert(0, str(WT / "osf" / "v46" / "scripts"))
sys.path.insert(0, str(WT / "osf" / "v45" / "scripts"))
import budget_v0_45 as BG                    # noqa: E402
import prices_v0_46_collection               # noqa: E402,F401  (adds gpt-6.2-astra / gemini-4-carbon rows)
import cost_estimate_v0_46 as R0             # noqa: E402
import cost_estimate_v0_46_stage1_r1 as SE   # noqa: E402
import cost_estimate_v0_46_stage1_r2 as S2   # noqa: E402

NEW = ("claude-fable-5-2", "gpt-6.2-astra", "gemini-4-carbon")
R0.SOURCE["gpt-6.2-astra"] = "gpt-6-astra"
assert R0.CARBON["standard_from_2026_12_01"] == BG.prices("gemini-4-carbon", "standard", R0.WHEN) == (4.0, 20.0)
LC = json.loads((WT / "osf/v46/data/v46_length_check.json").read_text())


def measured(floor=False):
    out = {"claude-fable-5-2": {"central": 1.0, "high": 1.0}}
    for m in ("gpt-6.2-astra", "gemini-4-carbon"):
        p = LC["models"][m]["paired_vs_2026_11_13"]
        c, h = p["billed_output_ratio_of_sums"], max(p["billed_output_ratio_of_sums"], p["billed_output_ratio_of_p90"])
        if floor:
            c, h = max(1.0, c), max(1.0, h)
        out[m] = {"central": c, "high": h}
    return out


ASSUMED = {"claude-fable-5-2": {"central": 1.0, "high": 1.0}, "gpt-6.2-astra": {"central": 1.0, "high": 1.0},
           "gemini-4-carbon": {"central": 2.0, "high": 3.0}}
_orig_per_call = R0.per_call


def install(mult):
    def per_call(by, target, cls, level, in_tokens):
        recs = by[(R0.SOURCE[target], cls)]
        k = mult.get(target, {}).get(level, 1.0)
        costs = sorted(R0.call_cost(target, r, in_tokens, k) for r in recs)
        v = costs[min(len(costs) - 1, int(0.9 * len(costs)))] if level == "high" else R0.st.mean(costs)
        return v * R0.RESEND[level], len(costs)

    def remeasure(lines):
        keep = [r for r in lines if r.get("substrate") in SE.SUBS and R0.qtype(r) in SE.CLASSES
                and (r["phase"] == "B" or (r.get("condition"), r.get("run")) == ("S0", 1))]
        tot = {"calls": 0, "central": 0.0, "high": 0.0}
        for m in NEW:
            for cls in SE.CLASSES:
                recs = [r for r in keep if r["model_requested"] == R0.SOURCE[m] and R0.qtype(r) == cls]
                for lv in ("central", "high"):
                    costs = sorted(R0.call_cost(m, r, SE.recorded_in(r), mult[m][lv]) for r in recs)
                    if not costs:
                        continue
                    p90 = costs[min(len(costs) - 1, int(0.9 * len(costs)))]
                    tot[lv] += sum(costs) * R0.RESEND["central"] if lv == "central" else len(costs) * p90 * R0.RESEND["high"]
                if recs:
                    tot["calls"] += len(recs)
        return {}, {k: (round(v, 2) if isinstance(v, float) else v) for k, v in tot.items()}

    R0.per_call = per_call
    SE.remeasure = remeasure
    S2.MODELS = NEW
    SE.MODELS = NEW


def summary(e):
    d = e["designs"]
    return {"A": d["A"]["total"], "E": d["E"]["total"], "remeasure_with_reserve": e["remeasure_with_reserve"],
            "blocks": e["blocks"], "projection_after_C1": e["projection_after_C1"], "checks": e["checks"]}


def main():
    locked = S2.estimate()["designs"]["A"]["total"]          # must reproduce 43.92 / 85.92 (old panel)
    out = {"status": "DRAFT, not a deposit record", "panel": NEW, "locked_panel_check": locked, "variants": {}}
    for name, mult in (("measured", measured()), ("measured_floor_1", measured(floor=True)), ("assumed_r0", ASSUMED)):
        install(mult)
        out["variants"][name] = {"multipliers": mult, **summary(S2.estimate())}
        R0.per_call = _orig_per_call
    hi = out["variants"]["measured"]["A"]["high"]
    out["rule_section_3_3"] = {"design_A_high_measured": hi, "design": "A" if hi <= 100 else "E"}
    Path(__file__).with_name("cost_recompute_measured_DRAFT.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk in ("multipliers", "A", "E")} for k, v in out["variants"].items()}, indent=1))
    print("locked panel:", locked, "rule:", out["rule_section_3_3"])


if __name__ == "__main__":
    main()
