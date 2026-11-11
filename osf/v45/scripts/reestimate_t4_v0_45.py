#!/usr/bin/env python3
"""
reestimate_t4_v0_45.py -- AIAS(TM) v0.45 (t5) pre-registration r1, section 4.5: the t5 cost re-estimated from t4's
RECORDED USAGE, at the prices that apply on the t5 dates (2026-12-03 to 12-06). Sends nothing.

Source: t4's raw file as locked, `git show v0.42-acquisition-locked:osf/v42/data/t4_raw.jsonl` (SHA-256 checked
against T4_RAW_SHA256; 990 lines, 876 calls). Only the fields in USAGE_FIELDS are kept from each line (call metadata,
status and usage); the answer text, the prompt, the search record (queries, sources, citations) and error messages are
dropped as each line is parsed and never printed or stored. Nothing about answer content is computed.

Prices: budget_v0_45 (vendor pages read 2026-11-10 and again 2026-11-11; unchanged): Claude Fable 5.2 at Message
Batches prices ($4 / $20 per 1M tokens) as at t4; GPT-6 Astra standard ($10 / $50); Gemini 4 Argon $4 / $20 from
2026-12-01 (t4 ran at $2 / $10); search fees $10 (Anthropic, OpenAI) and $14 (Google) per 1,000, the Google free
allowance not assumed; every search fee charged in full in batch mode (as r0).

Method (per model x block, collection order of section 4.2):
  t4 cost   each usage part at the price on its own date (equals the recorded cost_usd; checked line by line).
  central   t4's usage parts re-priced at t5 prices (date T5_DATE): the same calls, modes, tokens and searches, three
            weeks later. Re-sends need no extra factor: every billed request of t4 is a usage part (114 error lines
            carry no billed part).
  high      per model x question type (B-S0; A yes/no, v0.19-v0.22; A open, v0.23; B-S1): the 90th percentile of t4's
            per-call cost at t5 prices x the number of calls x 1.10 for re-sends, i.e. the conservative rule of r0 and
            v0.42 (every call at its 90th percentile) applied to t4's measured per-call costs instead of v0.39's tokens.
  guard     cumulative spend in collection order with the judge reserve (budget_v0_45.JUDGE_RESERVE_USD): where the
            $80 pause falls, and the projection rule after block 5 (spend + 2 x block 5's cost > $100 pauses).
Usage: python3 osf/v45/scripts/reestimate_t4_v0_45.py [--json OUT] [--txt OUT] [--raw FILE]
"""
import argparse
import hashlib
import json
import os
import statistics as st
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import budget_v0_45 as BG   # noqa: E402

ROOT = Path(os.environ.get("AIAS_ROOT", str(HERE.parents[2])))
T4_TAG = "v0.42-acquisition-locked"
T4_RAW_PATH = "osf/v42/data/t4_raw.jsonl"
T4_RAW_SHA256 = "f3109091f51af7899098d83a1d7b2080a26a06824caa5f6fc0486f3d6196d4bf"
T4_RECORDED_CALLS_USD = 67.4551       # v0.42 commit a790bb1: "$67.9551 incl. the $0.50 judge reserve"
T5_DATE = "2026-12-03T12:00:00+00:00"
USAGE_FIELDS = ("call_id", "substrate", "phase", "condition", "run", "model_requested", "provider", "mode", "status",
                "usage_parts", "cost_usd", "started_utc", "finished_utc", "served_model", "attempts", "empty_retry",
                "batch_id")
FORBIDDEN = ("text", "prompt", "system", "search", "error")
MODELS = ("claude-fable-5-2", "gpt-6-astra", "gemini-4-argon")
BLOCKS = [("1 B-S0 run 1", "B", "S0", 1), ("2 B-S0 run 2", "B", "S0", 2), ("3 B-S0 run 3", "B", "S0", 3),
          ("4 A-S0 run 1", "A", "S0", 1), ("5 B-S1 run 1", "B", "S1", 1), ("6 B-S1 run 2", "B", "S1", 2),
          ("7 B-S1 run 3", "B", "S1", 3)]
RESEND_HIGH = 1.10


def read_t4_bytes(raw=None):
    """The locked t4 raw file: from the tag (default) or a file; its SHA-256 must equal T4_RAW_SHA256."""
    if raw:
        data = Path(raw).read_bytes()
    else:
        data = subprocess.run(["git", "-C", str(ROOT), "show", f"{T4_TAG}:{T4_RAW_PATH}"], capture_output=True,
                              check=True).stdout
    h = hashlib.sha256(data).hexdigest()
    if h != T4_RAW_SHA256:
        sys.exit(f"REFUSED: t4 raw SHA-256 {h} != {T4_RAW_SHA256}")
    return data


def usage_lines(data):
    """-> list of dicts with USAGE_FIELDS only (each parsed line is dropped as soon as the fields are copied)."""
    out = []
    for line in data.decode("utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            out.append({k: r.get(k) for k in USAGE_FIELDS})
            del r
    return out


def qtype(rec):
    if rec["phase"] == "B":
        return "B-" + rec["condition"]
    return "A-open" if rec["substrate"] == "v23" else "A-yn"


def block_of(rec):
    for label, ph, cond, run in BLOCKS:
        if (rec["phase"], rec["condition"], rec["run"]) == (ph, cond, run):
            return label
    raise KeyError((rec["phase"], rec["condition"], rec["run"]))


def line_cost(rec, when):
    return sum(BG.part_cost(rec["model_requested"], p, when) for p in (rec["usage_parts"] or []))


def _p90(v):
    v = sorted(v)
    return float(v[0]) if len(v) == 1 else float(st.quantiles(v, n=10, method="inclusive")[-1])


def estimate(lines):
    """-> dict with checks, per model x block cells, block rows, totals and the guard path."""
    checks = {"lines": len(lines), "max_abs_recorded_minus_repriced_t4": 0.0}
    calls = defaultdict(list)
    for r in lines:
        calls[r["call_id"]].append(r)
        d = abs((r["cost_usd"] or 0.0) - line_cost(r, r["started_utc"]))
        checks["max_abs_recorded_minus_repriced_t4"] = max(checks["max_abs_recorded_minus_repriced_t4"], d)
    checks["calls"] = len(calls)
    checks["calls_answered"] = sum(any(x["status"] == "ok" for x in v) for v in calls.values())
    checks["error_lines_with_billed_parts"] = sum(1 for r in lines if r["status"] != "ok" and r["usage_parts"])
    checks["recorded_calls_usd"] = round(sum(r["cost_usd"] or 0.0 for r in lines), 6)
    checks["served_differs_from_requested"] = sum(1 for r in lines if r["status"] == "ok" and r["served_model"]
                                                  and not str(r["served_model"]).startswith(r["model_requested"]))
    per_call = {}          # call_id -> (model, block, qtype, t4 usd, t5 usd, usage totals)
    for cid, rs in calls.items():
        r0 = rs[0]
        u = {"input_tokens": 0, "output_tokens": 0, "thinking_tokens": 0, "tool_use_prompt_tokens": 0, "n_searches": 0,
             "billed_parts": 0}
        for r in rs:
            for p in r["usage_parts"] or []:
                u["billed_parts"] += 1
                for k in ("input_tokens", "output_tokens", "thinking_tokens", "tool_use_prompt_tokens", "n_searches"):
                    u[k] += p.get(k) or 0
        per_call[cid] = {"model": r0["model_requested"], "mode": r0["mode"], "block": block_of(r0), "qtype": qtype(r0),
                         "t4": sum(line_cost(r, r["started_utc"]) for r in rs), "t5": sum(line_cost(r, T5_DATE) for r in rs),
                         "usage": u}
    p90 = {}
    for m in MODELS:
        for q in ("B-S0", "A-yn", "A-open", "B-S1"):
            v = [c["t5"] for c in per_call.values() if c["model"] == m and c["qtype"] == q]
            p90[f"{m}|{q}"] = {"n_calls": len(v), "mean_t5": st.mean(v), "p90_t5": _p90(v)}
    cells = {}
    for m in MODELS:
        for label, *_ in BLOCKS:
            cs = [c for c in per_call.values() if c["model"] == m and c["block"] == label]
            high = sum(p90[f"{m}|{c['qtype']}"]["p90_t5"] for c in cs) * RESEND_HIGH
            usage = {k: sum(c["usage"][k] for c in cs) for k in cs[0]["usage"]}
            cells[f"{m}|{label}"] = {"model": m, "block": label, "mode": cs[0]["mode"], "calls": len(cs),
                                     "t4_usd": sum(c["t4"] for c in cs), "t5_central_usd": sum(c["t5"] for c in cs),
                                     "t5_high_usd": high, **usage}
    rows, cum = [], {"central": BG.JUDGE_RESERVE_USD, "high": BG.JUDGE_RESERVE_USD}
    for label, *_ in BLOCKS:
        cs = [cells[f"{m}|{label}"] for m in MODELS]
        row = {"block": label, "calls": sum(c["calls"] for c in cs), "t4_usd": sum(c["t4_usd"] for c in cs),
               "central": sum(c["t5_central_usd"] for c in cs), "high": sum(c["t5_high_usd"] for c in cs)}
        cum = {k: cum[k] + row[k] for k in cum}
        row.update({"cumulative_central": cum["central"], "cumulative_high": cum["high"]})
        rows.append(row)
    totals = {"calls": sum(r["calls"] for r in rows), "t4_usd": sum(r["t4_usd"] for r in rows),
              "central": sum(r["central"] for r in rows), "high": sum(r["high"] for r in rows),
              "judge_reserve": BG.JUDGE_RESERVE_USD}
    totals["central_with_reserve"] = totals["central"] + BG.JUDGE_RESERVE_USD
    totals["high_with_reserve"] = totals["high"] + BG.JUDGE_RESERVE_USD
    per_model = {m: {k: sum(cells[f"{m}|{b[0]}"][k] for b in BLOCKS) for k in ("calls", "t4_usd", "t5_central_usd",
                                                                                "t5_high_usd")} for m in MODELS}
    return {"checks": checks, "p90_per_call": p90, "cells": cells, "blocks": rows, "per_model": per_model,
            "totals": totals, "guard": {lvl: guard_path(rows, lvl) for lvl in ("central", "high")}}


def guard_path(rows, level):
    """The guard of section 4.5 on per-block costs (spend accrues within a block; the reserve is in the cumulative)."""
    out = {"level": level, "pause_80_in_block": None, "projection_after_block_5": None, "blocks_before_any_pause": []}
    start = BG.JUDGE_RESERVE_USD
    for i, r in enumerate(rows):
        end = r[f"cumulative_{level}"]
        if out["pause_80_in_block"] is None and end >= BG.PAUSE_AT_USD:
            out["pause_80_in_block"] = r["block"]
            out["pause_80_share_of_block_done"] = (BG.PAUSE_AT_USD - start) / (end - start) if end > start else 1.0
        if r["block"].startswith("5 "):
            proj = end + 2 * r[level]
            out["projection_after_block_5"] = {"spend": end, "block_5_cost": r[level], "projected": proj,
                                               "pauses": proj > BG.BUDGET_CAP_USD}
        start = end
    for r in rows:
        if out["pause_80_in_block"] == r["block"]:
            break
        out["blocks_before_any_pause"].append(r["block"])
        if r["block"].startswith("5 ") and out["projection_after_block_5"]["pauses"]:
            break
    return out


def report(res):
    t, L = res["totals"], []
    c = res["checks"]
    L.append(f"t4 raw: {c['lines']} lines, {c['calls']} calls, {c['calls_answered']} answered; recorded calls "
             f"${c['recorded_calls_usd']:.4f} (v0.42 commit a790bb1: ${T4_RECORDED_CALLS_USD:.4f}); max |recorded - "
             f"re-priced| per line {c['max_abs_recorded_minus_repriced_t4']:.2e}; error lines with billed usage: "
             f"{c['error_lines_with_billed_parts']}; answered lines served by another model: {c['served_differs_from_requested']}")
    L.append(f"\n== per model x block: t4 actual (t4 prices) | t5 central | t5 high (US$; t5 prices, date {T5_DATE[:10]})")
    for m in MODELS:
        for b in BLOCKS:
            x = res["cells"][f"{m}|{b[0]}"]
            L.append(f"  {m:17s} {x['mode']:8s} {b[0]:13s} {x['calls']:4d} calls  t4 ${x['t4_usd']:6.2f} | "
                     f"central ${x['t5_central_usd']:6.2f} | high ${x['t5_high_usd']:6.2f}   in {x['input_tokens']:>9,d}"
                     f" out {x['output_tokens']:>8,d} think {x['thinking_tokens']:>7,d} tool {x['tool_use_prompt_tokens']:>8,d}"
                     f" srch {x['n_searches']:4d}")
        pm = res["per_model"][m]
        L.append(f"  {m:17s} total {pm['calls']:4d} calls  t4 ${pm['t4_usd']:6.2f} | central ${pm['t5_central_usd']:6.2f}"
                 f" | high ${pm['t5_high_usd']:6.2f}")
    L.append(f"\n== by block, collection order (cumulative includes the ${BG.JUDGE_RESERVE_USD:.2f} judge reserve)")
    for r in res["blocks"]:
        L.append(f"  {r['block']:13s} {r['calls']:4d} calls  t4 ${r['t4_usd']:6.2f}  t5 ${r['central']:6.2f} / "
                 f"${r['high']:6.2f}   cumulative ${r['cumulative_central']:6.2f} / ${r['cumulative_high']:6.2f}")
    L.append(f"  {'all':13s} {t['calls']:4d} calls  t4 ${t['t4_usd']:6.2f}  t5 ${t['central']:6.2f} / ${t['high']:6.2f}"
             f"   with reserve ${t['central_with_reserve']:6.2f} / ${t['high_with_reserve']:6.2f}")
    for lvl, g in res["guard"].items():
        pj = g["projection_after_block_5"]
        L.append(f"\n== guard at the {lvl} estimate: $80 pause in block {g['pause_80_in_block'] or 'none (not reached)'}"
                 + (f" (about {100 * g['pause_80_share_of_block_done']:.0f}% of that block done)" if g["pause_80_in_block"] else "")
                 + f"; projection after block 5: ${pj['spend']:.2f} + 2 x ${pj['block_5_cost']:.2f} = ${pj['projected']:.2f}"
                 + (" > $100: PAUSE before runs 2-3 of S1" if pj["pauses"] else " <= $100: no pause")
                 + f"; collected without a decision: {', '.join(b.split(' ')[0] for b in g['blocks_before_any_pause'])}")
    L.append("\n== 90th-percentile cost per call at t5 prices (high basis) | mean")
    for k, v in res["p90_per_call"].items():
        L.append(f"  {k:28s} n {v['n_calls']:3d}  p90 ${v['p90_t5']:.4f}  mean ${v['mean_t5']:.4f}")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=None, help="a copy of the locked t4 raw file (default: read at the tag)")
    ap.add_argument("--json", default=None)
    ap.add_argument("--txt", default=None)
    a = ap.parse_args(argv)
    res = estimate(usage_lines(read_t4_bytes(a.raw)))
    res["meta"] = {"t4_source": f"{T4_TAG}:{T4_RAW_PATH}", "t4_raw_sha256": T4_RAW_SHA256, "t5_price_date": T5_DATE,
                   "fields_read": list(USAGE_FIELDS), "fields_never_read": list(FORBIDDEN),
                   "prices": {m: {"t4": BG.prices(m, mode, "2026-11-11"), "t5": BG.prices(m, mode, T5_DATE), "mode": mode}
                              for m, mode in (("claude-fable-5-2", "batch"), ("gpt-6-astra", "standard"),
                                              ("gemini-4-argon", "standard"))},
                   "search_fee_usd": BG.SEARCH_FEE, "resend_factor_high": RESEND_HIGH,
                   "prices_read": "2026-11-10 (r0) and 2026-11-11 08:36-08:38 US Central (r1), unchanged",
                   "judge_reserve_usd": BG.JUDGE_RESERVE_USD}
    text = report(res)
    print(text, end="")
    if a.json:
        Path(a.json).write_text(json.dumps(res, indent=2) + "\n", encoding="utf-8")
    if a.txt:
        Path(a.txt).write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
