#!/usr/bin/env python3
"""Cost estimate for the proposed v0.46 "From named to chosen" (DRAFT r0; not locked).

No model is called. Reads the recorded usage of the t4 wave (v0.42) from git, at the tag
v0.42-scoring-locked (osf/v42/data/t4_raw.jsonl), re-prices it with the price table of
osf/v45/scripts/budget_v0_45.py (prices read 2026-11-11) plus Gemini 4 Carbon (read 2026-11-11, see the
pre-registration section 4.5), and projects the cost of the v0.46 design and its alternatives.

Bases (per call, per model):
  floor   = mean cost of t4 yes/no brand questions (A-yn, v0.19-v0.22): a very short answer
  central = mean cost of t4 Phase B search-off answers (B-S0): a described list of several brands,
            longer than a one-brand choice, so conservative for a choice answer
  high    = 90th percentile of B-S0, +10% for re-sends (central: +2%)
Input tokens are replaced by the design's prompt length (LIST_IN / OPEN_IN, conservative).
Gemini 4 Carbon has no recorded call: Gemini 4 Argon's records x CARBON_MULT (central 2, high 3; Google's
page says Carbon "spends more thinking tokens per turn" than Argon), at Carbon's prices.
Prices on WHEN (2026-12-01: Gemini at its December list price; conservative if collection is earlier).
"""
import ast
import json
import os
import statistics as st
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("AIAS_ROOT", str(HERE.parents[2])))
sys.path.insert(0, str(ROOT / "osf" / "v45" / "scripts"))
import budget_v0_45 as BG  # noqa: E402

TAG = "v0.42-scoring-locked"
RAW = "osf/v42/data/t4_raw.jsonl"
WHEN = "2026-12-01T12:00:00+00:00"
CARBON = {"standard_to_2026_11_30": (2.0, 10.0), "standard_from_2026_12_01": (4.0, 20.0)}
CARBON_MULT = {"floor": 2.0, "central": 2.0, "high": 3.0}
RESEND = {"floor": 1.02, "central": 1.02, "high": 1.10}
LIST_IN, OPEN_IN = 600, 250          # input tokens per prompt (actual prompts are about 350 and 120)
MODELS = ("claude-fable-5-2", "gpt-6-astra", "gemini-4-carbon")
SOURCE = {"claude-fable-5-2": "claude-fable-5-2", "gpt-6-astra": "gpt-6-astra",
          "gemini-4-carbon": "gemini-4-argon", "gemini-4-argon": "gemini-4-argon",
          "claude-opus-5-5": "claude-fable-5-2"}


def load():
    raw = subprocess.run(["git", "-C", str(ROOT), "show", f"{TAG}:{RAW}"], check=True,
                         capture_output=True).stdout.decode()
    last = {}
    for line in raw.splitlines():
        r = json.loads(line)
        if r.get("status") == "ok" and (r.get("text") or "").strip():
            last[r["call_id"]] = r
    return list(last.values())


def qtype(r):
    if r["phase"] == "B":
        return "B-" + r["condition"]
    return "A-open" if r["substrate"] == "v23" else "A-yn"


def prices(model, mode):
    if model == "gemini-4-carbon":
        return CARBON["standard_from_2026_12_01"] if WHEN[:10] >= "2026-12-01" else CARBON["standard_to_2026_11_30"]
    return BG.prices(model, mode, WHEN)


def call_cost(target, rec, in_tokens, mult=1.0):
    """Cost of one design call modelled on one recorded t4 call (searches priced as recorded)."""
    parts = rec.get("usage_parts")
    if isinstance(parts, str):
        parts = ast.literal_eval(parts)
    parts = parts or []
    google = "gemini" in SOURCE[target]
    out = sum((p.get("output_tokens") or 0) + ((p.get("thinking_tokens") or 0) if google else 0) for p in parts)
    mode = parts[-1].get("mode", "standard") if parts else "standard"
    if target == "claude-opus-5-5":
        mode = "batch"
    pin, pout = prices(target, mode)
    search = sum(p.get("n_searches") or 0 for p in parts) * BG.SEARCH_FEE[BG.PROVIDER[SOURCE[target]]]
    return (in_tokens * pin + out * mult * pout) / 1e6 + search


def basis(lines):
    by = defaultdict(list)
    for r in lines:
        by[(r["model_requested"], qtype(r))].append(r)
    return by


def per_call(by, target, cls, level, in_tokens):
    recs = by[(SOURCE[target], cls)]
    mult = CARBON_MULT[level] if target == "gemini-4-carbon" else 1.0
    if cls == "B-S1":   # search-on: keep the recorded search-result input on top of the prompt
        costs = [call_cost(target, r, (r.get("input_tokens") or 0) + (r.get("tool_use_prompt_tokens") or 0)
                           + in_tokens, mult) for r in recs]
    else:
        costs = [call_cost(target, r, in_tokens, mult) for r in recs]
    costs.sort()
    v = costs[min(len(costs) - 1, int(0.9 * len(costs)))] if level == "high" else st.mean(costs)
    return v * RESEND[level], len(costs)


def design_cost(by, models, n_list, n_open, level, open_s1=0):
    cls = "A-yn" if level == "floor" else "B-S0"
    tot, rows = 0.0, {}
    for m in models:
        c = n_list * per_call(by, m, cls, level, LIST_IN)[0] + n_open * per_call(by, m, cls, level, OPEN_IN)[0]
        if open_s1:
            c += open_s1 * per_call(by, m, "B-S1", "central" if level == "floor" else level, OPEN_IN)[0]
        rows[m] = round(c, 2)
        tot += c
    return round(tot, 2), rows


def main():
    lines = load()
    by = basis(lines)
    out = {"source": f"git {TAG}:{RAW}", "answered_calls": len(lines), "when": WHEN,
           "list_in_tokens": LIST_IN, "open_in_tokens": OPEN_IN, "per_call": {}, "designs": {}}
    for m in MODELS + ("gemini-4-argon", "claude-opus-5-5"):
        for cls, lv in (("A-yn", "floor"), ("B-S0", "central"), ("B-S0", "high"), ("B-S1", "central"), ("B-S1", "high")):
            v, n = per_call(by, m, cls, lv, LIST_IN)
            out["per_call"][f"{m}|{cls}|{lv}|list_prompt"] = {"usd": round(v, 5), "n_t4_records": n}
    L = {"skincare": 24, "cosmetics": 24, "cars": 19, "spirits": 24}
    n_list = 2 * sum(L.values())          # two Latin squares per category and model
    n_open = 4 * 3 * 6                    # categories x briefs x runs
    designs = {
        "A adopted: Fable 5.2 (batch), GPT-6 Astra, Gemini 4 Carbon; LIST 2 squares + OPEN 6 runs; S0":
            dict(models=MODELS, n_list=n_list, n_open=n_open),
        "B adopted + Gemini 4 Argon arm (matched to t4 Presence)":
            dict(models=MODELS + ("gemini-4-argon",), n_list=n_list, n_open=n_open),
        "C adopted + OPEN with web search (S1), 6 runs":
            dict(models=MODELS, n_list=n_list, n_open=n_open, open_s1=n_open),
        "D Claude Opus 5.5 (batch) in place of Fable 5.2":
            dict(models=("claude-opus-5-5", "gpt-6-astra", "gemini-4-carbon"), n_list=n_list, n_open=n_open),
        "E LIST 1 square + OPEN 6 runs": dict(models=MODELS, n_list=n_list // 2, n_open=n_open),
        "F LIST 4 squares + OPEN 12 runs": dict(models=MODELS, n_list=2 * n_list, n_open=2 * n_open),
        "G adopted + v0.44's 8 industries (156 live units), after v0.44 is scored":
            dict(models=MODELS, n_list=n_list + 2 * 156, n_open=n_open + 8 * 3 * 6),
    }
    for name, d in designs.items():
        calls = len(d["models"]) * (d["n_list"] + d["n_open"] + d.get("open_s1", 0))
        res = {lv: design_cost(by, d["models"], d["n_list"], d["n_open"], lv, open_s1=d.get("open_s1", 0))
               for lv in ("floor", "central", "high")}
        out["designs"][name] = {"calls": calls, **{lv: {"total": t, "by_model": r} for lv, (t, r) in res.items()}}
    blocks = [("1 LIST square 1", n_list // 2, 0), ("2 OPEN", 0, n_open), ("3 LIST square 2", n_list // 2, 0)]
    cum = {"central": 0.0, "high": 0.0}
    out["blocks"] = []
    for lab, nl, no in blocks:
        row = {"block": lab, "calls": 3 * (nl + no)}
        for lv in cum:
            cum[lv] += design_cost(by, MODELS, nl, no, lv)[0]
            row[lv + "_cumulative"] = round(cum[lv], 2)
        out["blocks"].append(row)
    path = ROOT / "osf" / "v46" / "prereg" / "cost_estimate_v0_46_r0.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    txt = [f"source {out['source']}; answered t4 calls {len(lines)}; prices on {WHEN[:10]}"]
    for k, v in out["per_call"].items():
        txt.append(f"  per call {k:48s} ${v['usd']:.4f} (n {v['n_t4_records']})")
    for k, v in out["designs"].items():
        txt.append(f"{k}: {v['calls']} calls; floor ${v['floor']['total']:.2f}; central ${v['central']['total']:.2f}; "
                   f"high ${v['high']['total']:.2f}; central by model {v['central']['by_model']}")
    for b in out["blocks"]:
        txt.append(f"  block {b['block']:18s} {b['calls']:4d} calls  cumulative central ${b['central_cumulative']:.2f}"
                   f"  high ${b['high_cumulative']:.2f}")
    path.with_suffix(".txt").write_text("\n".join(txt) + "\n")
    print("\n".join(txt))


if __name__ == "__main__":
    main()
