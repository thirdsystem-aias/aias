#!/usr/bin/env python3
"""
cost_estimate_v0_45.py -- AIAS(TM) v0.45 (t5) pre-registration r0, section 4.5: cost of the t5 design (t4's design
repeated), per block in collection order, of the alternatives and of the add-ons the budget cannot hold (the Coverage
re-ask), at the vendors' list prices read again on 2026-11-10 (budget_v0_45.py; Gemini 4 Argon at $4 / $20 from
2026-12-01) and on v0.42's token basis (below, unchanged). Sends nothing.
Hand-edited copy of osf/v42/scripts/cost_estimate_v0_42.py (v0.42 @ 61515b4): budget module, N_PROBES (+ "CEP": the
75 probes of v1.12, list basis), DESIGNS / ADDONS (t5), block table and judge line; load_basis, per_call, cost_of and
cells are v0.42's (cells gains c_s0, the Coverage re-ask runs). When t4's own usage exists (after v0.42's collection),
section 4.5 is re-estimated from it as a logged clarification (pre-registration section 9).

Token basis (per call), from the v0.39 current arm (osf/v39/data/v39_raw.json, arm "C", collected Oct 2026;
30 calls per model x condition, fields tokens_in / tokens_out / tokens_thought / search.n_searches):
  list-type questions  = v0.39 tiers C, F, G, R (24 calls): used for Phase B (category lists) and for v0.23 Phase A
                         ("What do you know about <brand>? ... Please be detailed and specific.")
  short questions      = v0.39 tier K (6 brand probes): used for Phase A v0.19-v0.22 (yes/no). Conservative: those
                         prompts ask for "yes or no"; no current-model yes/no answer has been recorded.
  Claude Fable 5.2     = no study-type record exists; Claude Opus 5.5's basis x FABLE_MULT (output tokens, S1 input
                         tokens, searches). Central 2: Fable's default effort is high, Opus 5.5's medium
                         (thinking-steering-and-cost page). High 3: in v0.42's feasibility check the one completed
                         paired search prompt gave Fable/Opus = 40,269/13,625 input, 1,042/325 output, 3/1 searches.
Central = means; high = 90th percentiles (Fable: Opus 5.5's x 3; Gemini output x 1.5 for thinking tokens, which
v0.39 did not record at S0). Re-sends: central +2%, high +10% of the call cost.
Usage: python3 cost_estimate_v0_42.py [--json OUT]
"""
import argparse
import json
import os
import statistics as st
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import budget_v0_45 as BG   # noqa: E402

ROOT = Path(os.environ.get("AIAS_ROOT", str(HERE.parents[2])))
V39_RAW = ROOT / "osf/v39/data/v39_raw.json"
FABLE_MULT = {"central": 2.0, "high": 3.0}
GEMINI_THINK_HIGH = 1.5
RETRY = {"central": 1.02, "high": 1.10}
LIST_TIERS, SHORT_TIERS = {"C", "F", "G", "R"}, {"K"}
BASE_OF = {"claude-fable-5-2": "claude-opus-5-5"}
WAVE_DATE = {"t4": "2026-11-11", "t5": "2026-12-03", "t6": "2027-02-12"}
N_PROBES = {"B": 30, "A_yn": 88, "A_open": 24, "CEP": 75}   # CEP: v1.12's 70 situation + 5 control probes
PROBE_TYPE_TIERS = {"B": LIST_TIERS, "A_open": LIST_TIERS, "A_yn": SHORT_TIERS, "CEP": LIST_TIERS}


def _p90(v):
    v = sorted(v)
    if len(v) == 1:
        return float(v[0])
    return float(st.quantiles(v, n=10, method="inclusive")[-1])


def load_basis(path=V39_RAW):
    with open(path, encoding="utf-8") as f:
        recs = [r for r in json.load(f) if r.get("arm") == "C" and r.get("status") == "ok"]
    basis = {}
    for m in sorted({r["model_id"] for r in recs}):
        for c in ("S0", "S1"):
            for kind, tiers in (("list", LIST_TIERS), ("short", SHORT_TIERS)):
                rs = [r for r in recs if r["model_id"] == m and r["condition"] == c and r["tier"] in tiers]
                if not rs:
                    continue
                f = {"in": [r.get("tokens_in") or 0 for r in rs], "out": [r.get("tokens_out") or 0 for r in rs],
                     "think": [r.get("tokens_thought") or 0 for r in rs],
                     "srch": [((r.get("search") or {}).get("n_searches") or 0) for r in rs]}
                basis[(m, c, kind)] = {"n": len(rs), **{f"{k}_mean": st.mean(v) for k, v in f.items()},
                                       **{f"{k}_p90": _p90(v) for k, v in f.items()}}
    return basis


def per_call(basis, model, cond, ptype, level, mode, when):
    kind = "short" if ptype == "A_yn" else "list"
    src = BASE_OF.get(model, model)
    b = basis[(src, cond, kind)]
    q = "mean" if level == "central" else "p90"
    tin, tout, think, srch = b[f"in_{q}"], b[f"out_{q}"], b[f"think_{q}"], b[f"srch_{q}"]
    if model in BASE_OF:
        mult = FABLE_MULT[level]
        tout, srch = tout * mult, srch * mult
        if cond == "S1":
            tin *= mult
    if BG.PROVIDER[model] == "google" and level == "high":
        tout *= GEMINI_THINK_HIGH
    part = {"mode": mode, "input_tokens": tin, "output_tokens": tout,
            "thinking_tokens": think if BG.PROVIDER[model] == "google" else 0, "n_searches": srch if cond == "S1" else 0}
    return BG.part_cost(model, part, when) * RETRY[level]


def cost_of(design, basis, wave="t4"):
    """design: list of cells (model, mode, ptype, cond, runs). -> {central, high, calls, rows}"""
    when = WAVE_DATE[wave] + "T12:00:00+00:00"
    out = {"central": 0.0, "high": 0.0, "calls": 0, "rows": []}
    for model, mode, ptype, cond, runs in design:
        n = N_PROBES[ptype] * runs
        row = {"model": model, "mode": mode, "phase": ptype, "condition": cond, "runs": runs, "calls": n}
        for level in ("central", "high"):
            row[f"usd_per_call_{level}"] = per_call(basis, model, cond, ptype, level, mode, when)
            row[f"usd_{level}"] = n * row[f"usd_per_call_{level}"]
            out[level] += row[f"usd_{level}"]
        out["calls"] += n
        out["rows"].append(row)
    return out


def cells(models_modes, b_s0=3, b_s1=3, a_s0=1, a_s1=0, c_s0=0):
    d = []
    for m, mode in models_modes:
        for ptype, cond, runs in (("B", "S0", b_s0), ("B", "S1", b_s1), ("A_yn", "S0", a_s0), ("A_open", "S0", a_s0),
                                  ("A_yn", "S1", a_s1), ("A_open", "S1", a_s1), ("CEP", "S0", c_s0)):
            if runs:
                d.append((m, mode, ptype, cond, runs))
    return d


FAB, OPUS, GPT, GEM = "claude-fable-5-2", "claude-opus-5-5", "gpt-6-astra", "gemini-4-argon"
N3_MODES = [(FAB, "batch"), (GPT, "standard"), (GEM, "standard")]
DESIGNS = {
    "t5 (adopted): t4's design repeated: N3, Fable via Batch API; B S0x3, A S0x1, B S1x3": cells(N3_MODES),
    "t5 blocks 1-3 only (B S0 x3: v1.14 Stage 2 and the primary tests)": cells(N3_MODES, 3, 0, 0),
    "t5 blocks 1-4 (B S0 x3 + A S0 x1)": cells(N3_MODES, 3, 0, 1),
    "t5 with B S1 x2 runs (blocks 1-6)": cells(N3_MODES, b_s1=2),
    "t5 + Coverage re-ask (v1.12's 75 probes, N3, S0 x3; Fable via Batch API)": cells(N3_MODES, c_s0=3),
}
ADDONS = {
    "Coverage re-ask alone: 75 probes x N3 x S0 x 3 runs (675 calls), Fable via Batch API":
        cells(N3_MODES, 0, 0, 0, 0, 3),
    "Coverage re-ask alone, every model synchronous (as v1.12 collects)":
        cells([(FAB, "standard"), (GPT, "standard"), (GEM, "standard")], 0, 0, 0, 0, 3),
    "Claude Opus 5.5 continuity arm: B S0 x3 (90 calls), Batch API (not adopted)": [(OPUS, "batch", "B", "S0", 3)],
}
# Collection order of section 4.2: (label, phase types, condition, run); B blocks are one run each.
BLOCK_ORDER = [("1 B-S0 run 1", ("B",), "S0", 1), ("2 B-S0 run 2", ("B",), "S0", 1), ("3 B-S0 run 3", ("B",), "S0", 1),
               ("4 A-S0 run 1", ("A_yn", "A_open"), "S0", 1), ("5 B-S1 run 1", ("B",), "S1", 1),
               ("6 B-S1 run 2", ("B",), "S1", 1), ("7 B-S1 run 3", ("B",), "S1", 1)]
JUDGE_CALLS = {"parity_t3": 144, "parity_t4": 72, "t5_coding": 72}
JUDGE_TOKENS = {"input": 1500, "output": 10}     # upper bound per call (v0.42 section 4.5)


def block_table(basis, wave="t5"):
    """Per-block cost in collection order, with the cumulative spend (judge reserve included) at each block's end."""
    rows, cum = [], {"central": BG.JUDGE_RESERVE_USD, "high": BG.JUDGE_RESERVE_USD}
    for label, ptypes, cond, run in BLOCK_ORDER:
        d = [(m, mode, pt, cond, run) for m, mode in N3_MODES for pt in ptypes]
        c = cost_of(d, basis, wave)
        cum = {k: cum[k] + c[k] for k in cum}
        rows.append({"block": label, "calls": c["calls"], "central": c["central"], "high": c["high"],
                     "cumulative_central": cum["central"], "cumulative_high": cum["high"],
                     "per_model": {r["model"]: [r["usd_central"], r["usd_high"]] for r in c["rows"]}})
    return rows


def judge_cost():
    out = {}
    n = sum(JUDGE_CALLS.values())
    for m in ("claude-sonnet-5-5", "claude-sonnet-4-6"):
        part = {"mode": "standard", "input_tokens": JUDGE_TOKENS["input"] * n, "output_tokens": JUDGE_TOKENS["output"] * n}
        out[m] = {"calls": n, "usd_upper": BG.part_cost(m, part)}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    basis = load_basis()
    res = {"accessed": BG.ACCESSED_V45, "sources": BG.SOURCES, "basis_file": str(V39_RAW.relative_to(ROOT)),
           "basis": {"|".join(k): v for k, v in basis.items()}, "assumptions": {
               "fable_multiplier_on_opus_5_5": FABLE_MULT, "gemini_output_multiplier_high": GEMINI_THINK_HIGH,
               "resend_overhead": RETRY, "search_fee_usd": BG.SEARCH_FEE, "gemini_free_grounding_allowance": "not assumed",
               "batch_search_fee": "charged in full", "judge_reserve_usd": BG.JUDGE_RESERVE_USD,
               "wave_dates": WAVE_DATE, "gemini_4_argon_price_on_t5": BG.prices(GEM, "standard", WAVE_DATE["t5"])},
           "designs": {}, "addons": {}}
    for name, d in DESIGNS.items():
        res["designs"][name] = {w: cost_of(d, basis, w) for w in ("t4", "t5")}
    for name, d in ADDONS.items():
        res["addons"][name] = {w: cost_of(d, basis, w) for w in ("t4", "t5")}
    res["blocks_t5"] = block_table(basis, "t5")
    res["judge"] = judge_cost()
    for sect in ("designs", "addons"):
        print(f"== {sect} (t5 = prices on 2026-12-03; t4 prices for comparison)")
        for name, v in res[sect].items():
            t4, t5 = v["t4"], v["t5"]
            print(f"  {name}\n     calls {t5['calls']:5d}  t5 central ${t5['central']:7.2f} high ${t5['high']:7.2f}"
                  f"   (t4 prices: central ${t4['central']:7.2f} high ${t4['high']:7.2f})")
    print(f"\n== adopted design by block, collection order (t5 prices; cumulative includes the ${BG.JUDGE_RESERVE_USD:.2f} judge reserve)")
    for r in res["blocks_t5"]:
        flag = ""
        if r["cumulative_high"] > BG.BUDGET_CAP_USD:
            flag = "  <- high estimate passes the $100 stop"
        elif r["cumulative_high"] > BG.PAUSE_AT_USD:
            flag = "  <- high estimate passes the $80 pause"
        print(f"  {r['block']:14s} {r['calls']:4d} calls  ${r['central']:6.2f} / ${r['high']:6.2f}"
              f"   cumulative ${r['cumulative_central']:6.2f} / ${r['cumulative_high']:6.2f}{flag}")
    print("\n== successor judge (upper bound; parity on t3 + t4 answers and t5 coding):",
          {k: f"{v['calls']} calls ${v['usd_upper']:.2f}" for k, v in res["judge"].items()})
    adopted = res["designs"][next(iter(DESIGNS))]["t5"]
    print("\n== adopted design, per cell (t5 prices)")
    for r in adopted["rows"]:
        print(f"  {r['model']:17s} {r['mode']:8s} {r['phase']:6s} {r['condition']} x{r['runs']} {r['calls']:4d} calls"
              f"  ${r['usd_per_call_central']:.4f}/${r['usd_per_call_high']:.4f} per call"
              f"  -> ${r['usd_central']:6.2f} / ${r['usd_high']:6.2f}")
    if a.json:
        Path(a.json).write_text(json.dumps(res, indent=2), encoding="utf-8")
        print("wrote", a.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
