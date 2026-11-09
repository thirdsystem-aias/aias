#!/usr/bin/env python3
"""
AIAS v0.40 — US airlines and retail banks: pre-lock technical check (feasibility).

Sends only the neutral, non-category prompts of v0.39's --feasibility mode. It never sends a study probe,
names no brand and touches neither category. Declared as a technical check, not acquisition.

Reuses the locked v0.39 call functions verbatim (osf/v39/scripts/acquire_v0_39.py: legacy arm unchanged since
v0.38, current arm and search tools from v0.39) and adds one v0.40 setting: Gemini 2.5 Flash with thinking off
(thinking_budget 0), the v0.40 primary legacy setting. The v0.39 Flash setting runs as the extra pass.

Setups (13): M1-M4 and M6 at the v0.39 legacy setting; M5 twice (thinking 0, then the v0.39 setting);
C1-C3 at provider defaults in S0 (no tools) and S1 (provider web search). Calls: 10 S0 + 3 x 2 S1 = 16.
Output: osf/v40/prereg/feasibility_v0_40.json and feasibility_v0_40.csv.
Environment: ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY.

Usage:
  cd /Users/pablou/aias
  python3 osf/v40/scripts/feasibility_v0_40.py --dry-run
  python3 osf/v40/scripts/feasibility_v0_40.py
"""
import argparse
import csv
import hashlib
import importlib.util
import json
import os
import time
from pathlib import Path

ROOT = Path(os.environ.get("AIAS_ROOT", "/Users/pablou/aias"))
V39_PATH = ROOT / "osf" / "v39" / "scripts" / "acquire_v0_39.py"
OUT_JSON = ROOT / "osf" / "v40" / "prereg" / "feasibility_v0_40.json"
OUT_CSV = ROOT / "osf" / "v40" / "prereg" / "feasibility_v0_40.csv"

_spec = importlib.util.spec_from_file_location("acquire_v0_39", V39_PATH)
v39 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v39)


def call_google_thinking0(model_id, prompt):
    """v0.40 primary Gemini 2.5 Flash setting: v0.39's call_google with thinking off (budget 0)."""
    from google import genai
    from google.genai import errors, types
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    try:
        r = client.models.generate_content(
            model=model_id, contents=prompt,
            config=types.GenerateContentConfig(temperature=0.0, max_output_tokens=2048,
                                               thinking_config=types.ThinkingConfig(thinking_budget=0)))
    except errors.ServerError as e:
        raise v39.Transient(str(e)) from e
    except errors.ClientError as e:
        if getattr(e, "code", None) == 429:
            raise v39.Transient(str(e)) from e
        raise
    um = r.usage_metadata
    try:
        fr = str(r.candidates[0].finish_reason)
    except Exception:
        fr = None
    return {"text": r.text or "", "served_model": getattr(r, "model_version", None), "finish_reason": fr,
            "tokens_in": getattr(um, "prompt_token_count", None), "tokens_out": getattr(um, "candidates_token_count", None),
            "tokens_thought": getattr(um, "thoughts_token_count", None)}


L = {m["slot"]: m for m in v39.LEGACY}
C = {m["slot"]: m for m in v39.CURRENT}
LEG = "temperature 0, max output 2,048 (v0.39 legacy setting)"
CUR = "provider defaults, max output 16,384 (v0.39 current-arm setting)"
CUR_FN = {"anthropic": v39.call_anthropic_current, "openai": v39.call_openai_current, "google": v39.call_google_current}
SETUPS = [
    ("1", L["M1"], "L", "S0", LEG, v39.call_anthropic),
    ("2", L["M2"], "L", "S0", LEG, v39.call_anthropic),
    ("3", L["M3"], "L", "S0", LEG, v39.call_openai),
    ("4", L["M4"], "L", "S0", LEG, v39.call_openai),
    ("5", L["M5"], "L", "S0", "temperature 0, max output 2,048, thinking budget 0 (v0.40 primary)", call_google_thinking0),
    ("6", L["M5"], "L", "S0", LEG + "; provider-default thinking (v0.40 extra pass)", v39.call_google),
    ("7", L["M6"], "L", "S0", LEG, v39.call_google),
    ("8", C["C1"], "C", "S0", CUR + ", no tools", CUR_FN["anthropic"]),
    ("9", C["C1"], "C", "S1", CUR + ", provider web search", CUR_FN["anthropic"]),
    ("10", C["C2"], "C", "S0", CUR + ", no tools", CUR_FN["openai"]),
    ("11", C["C2"], "C", "S1", CUR + ", provider web search", CUR_FN["openai"]),
    ("12", C["C3"], "C", "S0", CUR + ", no tools", CUR_FN["google"]),
    ("13", C["C3"], "C", "S1", CUR + ", provider web search", CUR_FN["google"]),
]


def feas(pid, prompt):
    return {"probe_id": pid, "prompt": prompt, "sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest()}


def plan():
    neutral = feas("FEAS", v39.FEASIBILITY_PROMPT)
    searches = [feas(f"FEAS-S1{'ab'[i]}", p) for i, p in enumerate(v39.FEASIBILITY_SEARCH_PROMPTS)]
    s0 = [(s, neutral) for s in SETUPS if s[3] == "S0"]
    s1 = [(s, q) for q in searches for s in SETUPS if s[3] == "S1"]
    return s0 + s1


def send(setup, probe):
    sid, model, arm, cond, setting, fn = setup
    args = (model["model_id"], probe["prompt"]) + ((cond == "S1",) if arm == "C" else ())
    t0, ts_start = time.time(), v39._now()
    out, attempts, err = v39._call_with_retry(fn, *args)
    empty_retry = False
    if out is not None and not out["text"].strip():
        empty_retry = True
        out2, a2, err2 = v39._call_with_retry(fn, *args)
        attempts += a2
        if out2 is not None:
            out = out2
        if err2:
            err = err2
    latency = round(time.time() - t0, 2)
    ts_end = v39._now()
    time.sleep(v39.PAUSE[model["provider"]])
    status = "error" if out is None else ("empty" if not out["text"].strip() else "ok")
    out = out or {}
    srch = out.get("search") if cond == "S1" else None
    return {
        "phase": "v0.40-feasibility", "setup": sid, "probe_id": probe["probe_id"], "kind": "feasibility",
        "prompt": probe["prompt"], "prompt_sha256": probe["sha256"], "arm": arm, "condition": cond,
        "model_slot": model["slot"], "model_name": model["name"], "model_id": model["model_id"],
        "provider": model["provider"], "setting": setting,
        "response": out.get("text", ""), "status": status, "error": err,
        "served_model": out.get("served_model"), "finish_reason": out.get("finish_reason"),
        "tokens_in": out.get("tokens_in"), "tokens_out": out.get("tokens_out"), "tokens_thought": out.get("tokens_thought"),
        "attempts": attempts, "empty_retry": empty_retry, "paused_continued": out.get("paused_continued", False),
        "search": srch, "latency_s": latency, "ts_start": ts_start, "ts_end": ts_end,
    }


CSV_COLS = ["setup", "arm", "condition", "model_slot", "model_name", "model_id", "setting", "probe_id", "status",
            "served_model", "finish_reason", "tokens_in", "tokens_out", "tokens_thought", "n_searches", "n_sources",
            "latency_s", "reply", "error"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="print the plan; send nothing")
    a = ap.parse_args()
    p = plan()
    if a.dry_run:
        for s, q in p:
            print(f"  setup {s[0]:>2} {s[1]['slot']} {s[1]['model_id']:22s} {s[3]} {q['probe_id']:8s} {s[4]}")
        print(f"{len(p)} calls planned; nothing sent.")
        return
    v39.require_keys()
    recs = []
    for s, q in p:
        r = send(s, q)
        recs.append(r)
        sr = r["search"] or {}
        print(f"  setup {r['setup']:>2} {r['model_slot']} {r['condition']} {r['status']:5s} served={r['served_model']} "
              f"fr={r['finish_reason']} out={r['tokens_out']} thought={r['tokens_thought']} "
              f"searches={sr.get('n_searches', '-')} reply={r['response'].strip()[:40]!r} err={r['error']}", flush=True)
    meta = {"phase": "v0.40", "purpose": "pre-lock technical check (non-acquisition; no study probe sent)",
            "run_utc": v39._now(), "reused_code": str(V39_PATH.relative_to(ROOT)),
            "prompts": {"S0": v39.FEASIBILITY_PROMPT, "S1": v39.FEASIBILITY_SEARCH_PROMPTS}, "records": recs}
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(meta, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLS)
        w.writeheader()
        for r in recs:
            sr = r["search"] or {}
            w.writerow({**{k: r.get(k) for k in CSV_COLS}, "n_searches": sr.get("n_searches") if r["search"] else "",
                        "n_sources": len(sr.get("sources", [])) if r["search"] else "",
                        "reply": r["response"].strip().replace("\n", " ")[:80]})
    ok = sum(r["status"] == "ok" for r in recs)
    searched = sorted({r["model_slot"] for r in recs if r["condition"] == "S1" and (r["search"] or {}).get("n_searches", 0) > 0})
    print(f"\nTechnical check: {ok}/{len(recs)} ok; web search used by {len(searched)}/3 current models "
          f"({', '.join(searched) or 'none'}) -> {OUT_JSON.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
