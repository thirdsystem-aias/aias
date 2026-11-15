#!/usr/bin/env python3
"""Cost estimate for v0.46 "From named to chosen", pre-registration r1 (2026-11-14; not locked).

No model is called. Same basis and functions as r0 (cost_estimate_v0_46.py, imported unchanged): t4's
recorded usage read from git at v0.42-scoring-locked (osf/v42/data/t4_raw.jsonl), re-priced per call.
Change from r0: the Google chooser is Gemini 4 Argon (gemini-4-argon; Gemini 4 Carbon not shown as
generally available on Google's own pages on 2026-11-14, pre-registration section 4.3). Argon has t4
records of its own, so no thinking multiplier is applied to it. Argon is called synchronously (standard
price), as at t4. Prices are those of osf/v45/scripts/budget_v0_45.py, re-checked on the vendors' pages on
2026-11-14 (section 4.5): Fable 5.2 batch 4/20; GPT-6 Astra 10/50; Gemini 4 Argon 2/10 through 2026-11-30
and 4/20 from 2026-12-01. The estimate prices every call on 2026-12-01 (conservative).
Writes osf/v46/prereg/cost_estimate_v0_46_r1.json and .txt.
"""
import json
import statistics as st
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cost_estimate_v0_46 as R0  # noqa: E402

MODELS = ("claude-fable-5-2", "gpt-6-astra", "gemini-4-argon")
L = {"skincare": 24, "cosmetics": 24, "cars": 19, "spirits": 24}
N_LIST = 2 * sum(L.values())   # 182 per model: two Latin squares per category
N_OPEN = 4 * 3 * 6             # 72 per model: categories x briefs x runs
PAUSE, CAP = 80.0, 100.0


def token_basis(by):
    """Mean and 90th-percentile billed output tokens (Google: plus thinking) of the t4 B-S0 records."""
    out = {}
    for m in MODELS:
        recs = by[(R0.SOURCE[m], "B-S0")]
        google = "gemini" in m
        toks = []
        for r in recs:
            parts = r.get("usage_parts")
            if isinstance(parts, str):
                parts = R0.ast.literal_eval(parts)
            toks.append(sum((p.get("output_tokens") or 0) + ((p.get("thinking_tokens") or 0) if google else 0)
                            for p in (parts or [])))
        toks.sort()
        out[m] = {"n": len(toks), "mean_out": round(st.mean(toks)),
                  "p90_out": toks[min(len(toks) - 1, int(0.9 * len(toks)))]}
    return out


def run(by, models, n_list, n_open, open_s1=0):
    res = {lv: R0.design_cost(by, models, n_list, n_open, lv, open_s1=open_s1) for lv in ("floor", "central", "high")}
    calls = len(models) * (n_list + n_open + open_s1)
    return {"calls": calls, **{lv: {"total": t, "by_model": r} for lv, (t, r) in res.items()}}


def main():
    lines = R0.load()
    by = R0.basis(lines)
    out = {"source": f"git {R0.TAG}:{R0.RAW}", "answered_calls": len(lines), "when": R0.WHEN,
           "list_in_tokens": R0.LIST_IN, "open_in_tokens": R0.OPEN_IN,
           "calls_per_model": {"LIST": N_LIST, "OPEN": N_OPEN},
           "prices_usd_per_1M_in_out": {m: R0.prices(m, "batch" if m.startswith("claude") else "standard")
                                        for m in MODELS},
           "output_token_basis_B_S0": token_basis(by), "per_call": {}, "designs": {}}
    for m in MODELS:
        for lv in ("floor", "central", "high"):
            cls = "A-yn" if lv == "floor" else "B-S0"
            for lab, it in (("list_prompt", R0.LIST_IN), ("open_prompt", R0.OPEN_IN)):
                v, n = R0.per_call(by, m, cls, lv, it)
                out["per_call"][f"{m}|{cls}|{lv}|{lab}"] = {"usd": round(v, 5), "n_t4_records": n}
    carbon = ("claude-fable-5-2", "gpt-6-astra", "gemini-4-carbon")
    designs = {
        "A adopted r1: Fable 5.2 (batch), GPT-6 Astra, Gemini 4 Argon; LIST 2 squares + OPEN 6 runs; S0":
            dict(models=MODELS, n_list=N_LIST, n_open=N_OPEN),
        "B r0's design with Gemini 4 Carbon (not GA on 2026-11-14; not used)":
            dict(models=carbon, n_list=N_LIST, n_open=N_OPEN),
        "C A + OPEN with web search (S1), 6 runs (not adopted)":
            dict(models=MODELS, n_list=N_LIST, n_open=N_OPEN, open_s1=N_OPEN),
        "D Claude Opus 5.5 (batch) in place of Fable 5.2":
            dict(models=("claude-opus-5-5", "gpt-6-astra", "gemini-4-argon"), n_list=N_LIST, n_open=N_OPEN),
        "E LIST 1 square + OPEN 6 runs": dict(models=MODELS, n_list=N_LIST // 2, n_open=N_OPEN),
        "F LIST 4 squares + OPEN 12 runs": dict(models=MODELS, n_list=2 * N_LIST, n_open=2 * N_OPEN),
        "G A + v0.44's 8 industries (156 live units), after v0.44 is scored":
            dict(models=MODELS, n_list=N_LIST + 2 * 156, n_open=N_OPEN + 8 * 3 * 6),
    }
    for name, d in designs.items():
        out["designs"][name] = run(by, d["models"], d["n_list"], d["n_open"], d.get("open_s1", 0))
    blocks = [("1 LIST square 1", N_LIST // 2, 0), ("2 OPEN", 0, N_OPEN), ("3 LIST square 2", N_LIST // 2, 0)]
    cum = {"central": 0.0, "high": 0.0}
    out["blocks"] = []
    for lab, nl, no in blocks:
        row = {"block": lab, "calls": len(MODELS) * (nl + no)}
        for lv in cum:
            cum[lv] += R0.design_cost(by, MODELS, nl, no, lv)[0]
            row[lv + "_cumulative"] = round(cum[lv], 2)
        out["blocks"].append(row)
    b1 = out["blocks"][0]
    total_calls = out["designs"][next(iter(designs))]["calls"]
    out["projection_after_block1"] = {lv: round(b1[lv + "_cumulative"] * total_calls / b1["calls"], 2)
                                      for lv in cum}
    # November price variant (all calls before 2026-12-01): Argon at 2/10, others unchanged
    R0.WHEN = "2026-11-25T12:00:00+00:00"
    nov = run(by, MODELS, N_LIST, N_OPEN)
    out["adopted_if_all_calls_before_2026_12_01"] = {lv: nov[lv]["total"] for lv in ("floor", "central", "high")}
    a = out["designs"][next(iter(designs))]
    out["checks"] = {"high_below_pause_80": a["high"]["total"] < PAUSE, "high_below_cap_100": a["high"]["total"] < CAP,
                     "calls_762": a["calls"] == 762}
    path = HERE.parent / "prereg" / "cost_estimate_v0_46_r1.json"
    path.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    txt = [f"source {out['source']}; answered t4 calls {len(lines)}; prices on 2026-12-01 (r1, 2026-11-14)",
           f"prices (in/out per 1M, as used) {out['prices_usd_per_1M_in_out']}",
           f"output-token basis, t4 B-S0 {out['output_token_basis_B_S0']}"]
    for k, v in out["per_call"].items():
        txt.append(f"  per call {k:48s} ${v['usd']:.4f} (n {v['n_t4_records']})")
    for k, v in out["designs"].items():
        txt.append(f"{k}: {v['calls']} calls; floor ${v['floor']['total']:.2f}; central ${v['central']['total']:.2f}; "
                   f"high ${v['high']['total']:.2f}; central by model {v['central']['by_model']}; "
                   f"high by model {v['high']['by_model']}")
    for b in out["blocks"]:
        txt.append(f"  block {b['block']:18s} {b['calls']:4d} calls  cumulative central ${b['central_cumulative']:.2f}"
                   f"  high ${b['high_cumulative']:.2f}")
    txt.append(f"projection after block 1 (x {total_calls}/{b1['calls']}): {out['projection_after_block1']}")
    txt.append(f"adopted if every call is before 2026-12-01: {out['adopted_if_all_calls_before_2026_12_01']}")
    txt.append(f"checks {out['checks']}")
    path.with_suffix(".txt").write_text("\n".join(txt) + "\n")
    print("\n".join(txt))


if __name__ == "__main__":
    main()
