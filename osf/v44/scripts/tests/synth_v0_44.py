#!/usr/bin/env python3
"""
synth_v0_44.py -- SYNTHETIC v0.44 raw data in the real raw format (acquire_v0_44 records). Synthetic only: never
touches osf/v44/data/. No model is called.

A k function kfn(model, run, industry, unit) -> k in 0..6 sets how many of the industry's six Phase B answers of
(model, run) name the unit: the answer to frame q(i+1) lists the units with k > i (by their first alias), so the
coder reproduces k from the raw text. Phase A answers are "Yes." or "No." from recog(model, industry, unit).

  build(kfn, recog=None, drop=None, fail=None, served=None, runs=(1, 2, 3), t0=..., hours=0.0, extra_text="")
    -> list of raw records (909 for the full design)
"""
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import code_v0_44 as C   # noqa: E402

MODELS = ["claude-fable-5-2", "gpt-6-astra", "gemini-4-argon"]
PROVIDER = {"claude-fable-5-2": "anthropic", "gpt-6-astra": "openai", "gemini-4-argon": "google"}
T0 = "2026-11-24T15:00:00+00:00"


def probes():
    return [json.loads(l) for l in open(C.PROBES_PATH, encoding="utf-8") if l.strip()]


def registry():
    return C.load_registry()


def answer_b(units, extra_text=""):
    lines = [f"{i + 1}. **{u['aliases'][0]}** - a well-known choice." for i, u in enumerate(units)]
    return ("Here are several options:\n" + "\n".join(lines) + extra_text) if lines else "I cannot name any."


def build(kfn, recog=None, drop=None, fail=None, served=None, runs=(1, 2, 3), t0=T0, hours=0.0, extra_text=""):
    reg = registry()
    ps = probes()
    recog = recog or (lambda m, ind, u: 1)
    start = datetime.fromisoformat(t0)
    blocks = [("B", r) for r in runs] + [("A", 1)]
    n_total = len(MODELS) * sum(len([p for p in ps if p["phase"] == ph]) for ph, _ in blocks)
    raw, i = [], 0
    for ph, run in blocks:
        for m in MODELS:
            for p in ps:
                if p["phase"] != ph:
                    continue
                ind = p["substrate"]
                spec = {"model": m, "phase": ph, "run": run, "industry": ind, "probe_id": p["probe_id"]}
                if ph == "B":
                    fi = int(p["frame_id"][1:]) - 1
                    named = [u for u in reg[ind] if kfn(m, run, ind, u) > fi]
                    text = answer_b(named, extra_text)
                else:
                    u = next(x for x in reg[ind] if x["unit_id"] == p["brand_id"])
                    text = "Yes." if recog(m, ind, u) else "No."
                ts = start + timedelta(hours=hours * i / max(1, n_total - 1))
                i += 1
                if drop and drop(spec):
                    continue
                bad = bool(fail and fail(spec))
                rec = {"call_id": f"{ind}|{ph}|{p['probe_id']}|{m}|S0|{run}", "substrate": ind, "phase": ph,
                       "probe_id": p["probe_id"], "brand_id": p.get("brand_id"), "frame_id": p.get("frame_id"),
                       "model_requested": m, "provider": PROVIDER[m],
                       "served_model": (served(spec) if served else m), "condition": "S0", "run": run,
                       "system": None, "prompt": p["prompt"], "text": "" if bad else text,
                       "status": "error" if bad else "ok", "error": "synthetic error" if bad else None,
                       "finish_reason": "end_turn", "input_tokens": 30, "output_tokens": 200, "thinking_tokens": None,
                       "search": None, "paused_continued": False, "attempts": 1, "empty_retry": False,
                       "started_utc": ts.isoformat(), "finished_utc": (ts + timedelta(seconds=5)).isoformat(),
                       "mode": "batch" if m == "claude-fable-5-2" else "standard",
                       "usage_parts": [{"mode": "batch" if m == "claude-fable-5-2" else "standard",
                                        "input_tokens": 30, "output_tokens": 200, "thinking_tokens": None,
                                        "n_searches": 0}]}
                rec["cost_usd"] = 0.0
                raw.append(rec)
    return raw


def write(raw, d):
    d = Path(d)
    d.mkdir(parents=True, exist_ok=True)
    with open(d / "v44_raw.jsonl", "w", encoding="utf-8") as f:
        for r in raw:
            f.write(json.dumps(r) + "\n")
    return d / "v44_raw.jsonl"
