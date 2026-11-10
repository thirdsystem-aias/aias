#!/usr/bin/env python3
"""
cost_estimate_v0_42.py -- AIAS(TM) v0.42 pre-registration r2, section 4.5: cost of the t4 design and of the
alternatives, at the vendors' list prices (budget_v0_42.py) and MEASURED token counts. Sends nothing.

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
import budget_v0_42 as BG   # noqa: E402

ROOT = Path(os.environ.get("AIAS_ROOT", str(HERE.parents[2])))
V39_RAW = ROOT / "osf/v39/data/v39_raw.json"
FABLE_MULT = {"central": 2.0, "high": 3.0}
GEMINI_THINK_HIGH = 1.5
RETRY = {"central": 1.02, "high": 1.10}
LIST_TIERS, SHORT_TIERS = {"C", "F", "G", "R"}, {"K"}
BASE_OF = {"claude-fable-5-2": "claude-opus-5-5"}
WAVE_DATE = {"t4": "2026-11-11", "t5": "2026-12-03", "t6": "2027-02-12"}
N_PROBES = {"B": 30, "A_yn": 88, "A_open": 24}
PROBE_TYPE_TIERS = {"B": LIST_TIERS, "A_open": LIST_TIERS, "A_yn": SHORT_TIERS}


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


def cells(models_modes, b_s0=3, b_s1=3, a_s0=1, a_s1=0):
    d = []
    for m, mode in models_modes:
        for ptype, cond, runs in (("B", "S0", b_s0), ("B", "S1", b_s1), ("A_yn", "S0", a_s0), ("A_open", "S0", a_s0),
                                  ("A_yn", "S1", a_s1), ("A_open", "S1", a_s1)):
            if runs:
                d.append((m, mode, ptype, cond, runs))
    return d


FAB, OPUS, GPT, GEM = "claude-fable-5-2", "claude-opus-5-5", "gpt-6-astra", "gemini-4-argon"
DESIGNS = {
    "r2 (adopted): N3, Fable via Batch API; B S0x3, B S1x3, A S0x1": cells([(FAB, "batch"), (GPT, "standard"), (GEM, "standard")]),
    "r2 with Fable synchronous (no batch)": cells([(FAB, "standard"), (GPT, "standard"), (GEM, "standard")]),
    "r2 with Opus 5.5 in place of Fable (synchronous)": cells([(OPUS, "standard"), (GPT, "standard"), (GEM, "standard")]),
    "r2 with Opus 5.5 in place of Fable (Batch API)": cells([(OPUS, "batch"), (GPT, "standard"), (GEM, "standard")]),
    "r2 with Phase A S0 x3 runs": cells([(FAB, "batch"), (GPT, "standard"), (GEM, "standard")], a_s0=3),
    "r2 with B S1 x2 runs": cells([(FAB, "batch"), (GPT, "standard"), (GEM, "standard")], b_s1=2),
    "r1 as drafted: 4 models, 142 probes x S0/S1 x 3 runs, synchronous": cells(
        [(FAB, "standard"), (OPUS, "standard"), (GPT, "standard"), (GEM, "standard")], a_s0=3, a_s1=3),
}
ADDONS = {
    "H_Version_Presence add-on: Opus 5.5, B S0 x3 (90 calls), Batch API": [(OPUS, "batch", "B", "S0", 3)],
    "H_Version_Presence add-on: Opus 5.5, B S0 x3 (90 calls), synchronous": [(OPUS, "standard", "B", "S0", 3)],
    "H_Version_Presence standalone: Fable + Opus 5.5, B S0 x3 (180 calls), Batch API": [
        (FAB, "batch", "B", "S0", 3), (OPUS, "batch", "B", "S0", 3)],
    "Phase A S1 x1 run on N3 (336 calls)": cells([(FAB, "batch"), (GPT, "standard"), (GEM, "standard")], 0, 0, 0, 1),
    "Phase A S0 runs 2-3 on N3 (672 calls)": cells([(FAB, "batch"), (GPT, "standard"), (GEM, "standard")], 0, 0, 2, 0),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    basis = load_basis()
    res = {"accessed": BG.ACCESSED, "sources": BG.SOURCES, "basis_file": str(V39_RAW.relative_to(ROOT)),
           "basis": {"|".join(k): v for k, v in basis.items()}, "assumptions": {
               "fable_multiplier_on_opus_5_5": FABLE_MULT, "gemini_output_multiplier_high": GEMINI_THINK_HIGH,
               "resend_overhead": RETRY, "search_fee_usd": BG.SEARCH_FEE, "gemini_free_grounding_allowance": "not assumed",
               "batch_search_fee": "charged in full", "judge_reserve_usd": BG.JUDGE_RESERVE_USD,
               "wave_dates": WAVE_DATE}, "designs": {}, "addons": {}}
    for name, d in DESIGNS.items():
        res["designs"][name] = {w: cost_of(d, basis, w) for w in ("t4", "t5")}
    for name, d in ADDONS.items():
        res["addons"][name] = {w: cost_of(d, basis, w) for w in ("t4", "t5")}
    for sect in ("designs", "addons"):
        print(f"== {sect}")
        for name, v in res[sect].items():
            t4, t5 = v["t4"], v["t5"]
            print(f"  {name}\n     calls {t4['calls']:5d}  t4 central ${t4['central']:7.2f} high ${t4['high']:7.2f}"
                  f"   t5/t6 central ${t5['central']:7.2f} high ${t5['high']:7.2f}")
    adopted = res["designs"][next(iter(DESIGNS))]["t4"]
    print("\n== adopted design, per cell (t4 prices)")
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
