#!/usr/bin/env python3
"""
AIAS v0.39 — Commercial coffee roasters (Bellwether-focal) acquisition script
Pre-reg tag: v0.39-prereg-r1 | Presence definitions per Methodology v1.2 (SSRN 6761698)

Forked from scripts/acquire_v0_38.py.
Legacy arm (M1-M6): call functions and decoding unchanged from v0.38 (temperature 0.0,
max output 2,048 tokens, single user turn, no system prompt, one call per probe x model).
Added (pre-registration sections 4.3-4.4):
  * current arm (C1-C3), each in S0 (no tools) and S1 (the provider's own web search);
    temperature and reasoning effort left at provider defaults; max output 16,384 tokens;
  * S1 records every search query, consulted source and citation;
  * an Anthropic `pause_turn` stop is continued once with identical tools and logged;
  * --feasibility sends only neutral, non-category prompts (section 10, item 3) and writes
    osf/v39/prereg/feasibility_v0_39.json. It never sends a study probe.

Calls: 30 probes x (6 legacy + 3 current x 2 conditions) = 360.
Order: probes in battery order; within probe M1..M6 (S0), then C1..C3 in S0, then C1..C3 in S1.
Output: osf/v39/data/v39_raw.json (checkpointed every 12 calls).
Environment: ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY.

Usage:
  cd /Users/pablou/aias
  python3 scripts/acquire_v0_39.py --dry-run
  python3 scripts/acquire_v0_39.py --feasibility
  python3 scripts/acquire_v0_39.py
  python3 scripts/acquire_v0_39.py --resume
"""
import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PIPELINE_ROOT = Path(os.environ.get("AIAS_ROOT", "/Users/pablou/aias"))
PROBES_PATH = PIPELINE_ROOT / "osf" / "v39" / "prereg" / "probes_v0_39.json"
OUTPUT_DIR = PIPELINE_ROOT / "osf" / "v39" / "data"
RAW_PATH = OUTPUT_DIR / "v39_raw.json"
FEASIBILITY_PATH = PIPELINE_ROOT / "osf" / "v39" / "prereg" / "feasibility_v0_39.json"

# Legacy panel (fixed from v0.17). Boundary = position of the documented cutoff relative to the
# Bellwether Shop Roaster announcement (2024-03-07).
LEGACY = [
    {"slot": "M1", "name": "Claude Opus 4.5",       "provider": "anthropic", "model_id": "claude-opus-4-5",       "boundary": "post", "documented_cutoff": "May 2025 (reliable knowledge)"},
    {"slot": "M2", "name": "Claude Sonnet 4.5",     "provider": "anthropic", "model_id": "claude-sonnet-4-5",     "boundary": "post", "documented_cutoff": "Jan 2025 (reliable knowledge)"},
    {"slot": "M3", "name": "GPT-4o",                "provider": "openai",    "model_id": "gpt-4o",                "boundary": "pre",  "documented_cutoff": "Oct 2023"},
    {"slot": "M4", "name": "GPT-4o-mini",           "provider": "openai",    "model_id": "gpt-4o-mini",           "boundary": "pre",  "documented_cutoff": "Oct 2023"},
    {"slot": "M5", "name": "Gemini 2.5 Flash",      "provider": "google",    "model_id": "gemini-2.5-flash",      "boundary": "post", "documented_cutoff": "Jan 2025"},
    {"slot": "M6", "name": "Gemini 2.5 Flash Lite", "provider": "google",    "model_id": "gemini-2.5-flash-lite", "boundary": "post", "documented_cutoff": "Jan 2025"},
]
# Current arm: each provider's flagship. All documented cutoffs postdate the Shop Roaster and
# predate the 2026 model (2026-10-15).
CURRENT = [
    {"slot": "C1", "name": "Claude Opus 5.5", "provider": "anthropic", "model_id": "claude-opus-5-5", "boundary": "post", "documented_cutoff": "Jun 2026 (reliable knowledge)"},
    {"slot": "C2", "name": "GPT-6 Astra",     "provider": "openai",    "model_id": "gpt-6-astra",     "boundary": "post", "documented_cutoff": "2026-04-30"},
    {"slot": "C3", "name": "Gemini 4 Argon",  "provider": "google",    "model_id": "gemini-4-argon",  "boundary": "post", "documented_cutoff": "not documented"},
]

# S1 tool configurations (pre-registration section 4.3).
S1_ANTHROPIC = {"type": "web_search_20250305", "name": "web_search", "max_uses": 5,
                "user_location": {"type": "approximate", "country": "US"}}
S1_OPENAI = {"type": "web_search", "search_context_size": "medium",
             "user_location": {"type": "approximate", "country": "US"}}
S1_OPENAI_INCLUDE = ["web_search_call.action.sources"]

LEGACY_MAX_TOKENS = 2048
CURRENT_MAX_TOKENS = 16384
PAUSE = {"anthropic": 2.0, "openai": 1.0, "google": 1.0}
MAX_ATTEMPTS = 3

FEASIBILITY_PROMPT = "Reply with the single word: ready"
# Two neutral, non-category S1 prompts: a model may answer the first from its own context without searching.
FEASIBILITY_SEARCH_PROMPTS = [
    "Use web search to find today's date in Coordinated Universal Time. Reply with the date only.",
    "Search the web for the current top headline on bbc.com and give the source URL.",
]


class Transient(Exception):
    """Rate limit, 5xx/overload, connection or timeout error: retry-eligible."""


def _empty_search():
    return {"n_searches": 0, "queries": [], "sources": [], "citations": [], "errors": []}


def _dump(o):
    if o is None or isinstance(o, (str, int, float, bool)):
        return o
    if isinstance(o, dict):
        return {k: _dump(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_dump(v) for v in o]
    if hasattr(o, "model_dump"):
        return o.model_dump()
    return str(o)


# ======================= legacy arm (verbatim from v0.38) =======================

def call_anthropic(model_id, prompt):
    import anthropic
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    try:
        m = client.messages.create(model=model_id, max_tokens=2048, temperature=0.0,
                                   messages=[{"role": "user", "content": prompt}])
    except (anthropic.RateLimitError, anthropic.APIConnectionError, anthropic.APITimeoutError) as e:
        raise Transient(str(e)) from e
    except anthropic.APIStatusError as e:
        if e.status_code >= 500:
            raise Transient(str(e)) from e
        raise
    text = "".join(b.text for b in m.content if hasattr(b, "text"))
    return {"text": text, "served_model": m.model, "finish_reason": m.stop_reason,
            "tokens_in": m.usage.input_tokens, "tokens_out": m.usage.output_tokens, "tokens_thought": None}


def call_openai(model_id, prompt):
    import openai
    client = openai.OpenAI()  # reads OPENAI_API_KEY
    try:
        r = client.chat.completions.create(model=model_id, max_tokens=2048, temperature=0.0,
                                           messages=[{"role": "user", "content": prompt}])
    except (openai.RateLimitError, openai.APIConnectionError, openai.APITimeoutError) as e:
        raise Transient(str(e)) from e
    except openai.APIStatusError as e:
        if e.status_code >= 500:
            raise Transient(str(e)) from e
        raise
    c = r.choices[0]
    return {"text": c.message.content or "", "served_model": r.model, "finish_reason": c.finish_reason,
            "tokens_in": r.usage.prompt_tokens, "tokens_out": r.usage.completion_tokens, "tokens_thought": None}


def call_google(model_id, prompt):
    from google import genai
    from google.genai import errors, types
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    try:
        r = client.models.generate_content(model=model_id, contents=prompt,
                                           config=types.GenerateContentConfig(temperature=0.0, max_output_tokens=2048))
    except errors.ServerError as e:
        raise Transient(str(e)) from e
    except errors.ClientError as e:
        if getattr(e, "code", None) == 429:
            raise Transient(str(e)) from e
        raise
    um = r.usage_metadata
    try:
        fr = str(r.candidates[0].finish_reason)
    except Exception:
        fr = None
    return {"text": r.text or "", "served_model": getattr(r, "model_version", None), "finish_reason": fr,
            "tokens_in": getattr(um, "prompt_token_count", None), "tokens_out": getattr(um, "candidates_token_count", None),
            "tokens_thought": getattr(um, "thoughts_token_count", None)}


# ======================= current arm (new in v0.39) =======================

def call_anthropic_current(model_id, prompt, search):
    import anthropic
    client = anthropic.Anthropic()
    msgs = [{"role": "user", "content": prompt}]
    kw = {"model": model_id, "max_tokens": CURRENT_MAX_TOKENS}
    if search:
        kw["tools"] = [S1_ANTHROPIC]
    try:
        m = client.messages.create(messages=msgs, **kw)
        blocks, paused = list(m.content), False
        tin, tout = m.usage.input_tokens, m.usage.output_tokens
        if m.stop_reason == "pause_turn":  # continue once with identical tools (section 4.4)
            paused = True
            m2 = client.messages.create(messages=msgs + [{"role": "assistant", "content": m.content}], **kw)
            blocks += list(m2.content)
            tin += m2.usage.input_tokens
            tout += m2.usage.output_tokens
            m = m2
    except (anthropic.RateLimitError, anthropic.APIConnectionError, anthropic.APITimeoutError) as e:
        raise Transient(str(e)) from e
    except anthropic.APIStatusError as e:
        if e.status_code >= 500:
            raise Transient(str(e)) from e
        raise
    s = _empty_search()
    text = []
    for b in blocks:
        t = getattr(b, "type", None)
        if t == "text":
            text.append(b.text)
            for c in (getattr(b, "citations", None) or []):
                url = getattr(c, "url", None)
                if url:
                    s["citations"].append({"url": url, "title": getattr(c, "title", None)})
        elif t == "server_tool_use" and getattr(b, "name", "") == "web_search":
            s["n_searches"] += 1
            inp = getattr(b, "input", None) or {}
            s["queries"].append(inp.get("query") if isinstance(inp, dict) else str(inp))
        elif t == "web_search_tool_result":
            content = getattr(b, "content", None)
            if isinstance(content, list):
                for res in content:
                    s["sources"].append({"url": getattr(res, "url", None), "title": getattr(res, "title", None),
                                         "page_age": getattr(res, "page_age", None)})
            else:
                s["errors"].append(str(getattr(content, "error_code", content)))
    return {"text": "".join(text), "served_model": m.model, "finish_reason": m.stop_reason,
            "tokens_in": tin, "tokens_out": tout, "tokens_thought": None,
            "paused_continued": paused, "search": s if search else None}


def call_openai_current(model_id, prompt, search):
    import openai
    client = openai.OpenAI()
    kw = {"model": model_id, "input": prompt, "max_output_tokens": CURRENT_MAX_TOKENS}
    if search:
        kw["tools"] = [S1_OPENAI]
        kw["include"] = S1_OPENAI_INCLUDE
    try:
        r = client.responses.create(**kw)
    except (openai.RateLimitError, openai.APIConnectionError, openai.APITimeoutError) as e:
        raise Transient(str(e)) from e
    except openai.APIStatusError as e:
        if e.status_code >= 500:
            raise Transient(str(e)) from e
        raise
    s = _empty_search()
    for item in (r.output or []):
        d = _dump(item)
        if not isinstance(d, dict):
            continue
        if d.get("type") == "web_search_call":
            a = d.get("action") or {}
            if a.get("type") == "search":
                s["n_searches"] += 1
                if a.get("query"):
                    s["queries"].append(a["query"])
                for q in (a.get("queries") or []):
                    s["queries"].append(q)
                for src in (a.get("sources") or []):
                    s["sources"].append({"url": src.get("url"), "title": src.get("title")})
            elif a.get("url"):
                s["sources"].append({"url": a.get("url"), "title": None, "action": a.get("type")})
        elif d.get("type") == "message":
            for c in (d.get("content") or []):
                for ann in (c.get("annotations") or []):
                    if ann.get("type") == "url_citation":
                        s["citations"].append({"url": ann.get("url"), "title": ann.get("title")})
    u = r.usage
    det = getattr(u, "output_tokens_details", None)
    fr = r.status
    inc = getattr(r, "incomplete_details", None)
    if inc is not None and getattr(inc, "reason", None):
        fr = f"{r.status}:{inc.reason}"
    return {"text": r.output_text or "", "served_model": r.model, "finish_reason": fr,
            "tokens_in": getattr(u, "input_tokens", None), "tokens_out": getattr(u, "output_tokens", None),
            "tokens_thought": getattr(det, "reasoning_tokens", None) if det is not None else None,
            "paused_continued": False, "search": s if search else None}


def call_google_current(model_id, prompt, search):
    from google import genai
    from google.genai import errors, types
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    cfg = {"max_output_tokens": CURRENT_MAX_TOKENS}
    if search:
        cfg["tools"] = [types.Tool(google_search=types.GoogleSearch())]
    try:
        r = client.models.generate_content(model=model_id, contents=prompt, config=types.GenerateContentConfig(**cfg))
    except errors.ServerError as e:
        raise Transient(str(e)) from e
    except errors.ClientError as e:
        if getattr(e, "code", None) == 429:
            raise Transient(str(e)) from e
        raise
    s = _empty_search()
    fr = None
    try:
        cand = r.candidates[0]
        fr = str(cand.finish_reason)
        gm = getattr(cand, "grounding_metadata", None)
    except Exception:
        gm = None
    if gm is not None:
        qs = list(getattr(gm, "web_search_queries", None) or [])
        s["queries"] = qs
        s["n_searches"] = len(qs)
        chunks = list(getattr(gm, "grounding_chunks", None) or [])
        for ch in chunks:
            w = getattr(ch, "web", None)
            if w is not None:
                s["sources"].append({"url": getattr(w, "uri", None), "title": getattr(w, "title", None)})
        for sup in (getattr(gm, "grounding_supports", None) or []):
            for i in (getattr(sup, "grounding_chunk_indices", None) or []):
                if 0 <= i < len(s["sources"]):
                    s["citations"].append(s["sources"][i])
    um = r.usage_metadata
    return {"text": r.text or "", "served_model": getattr(r, "model_version", None), "finish_reason": fr,
            "tokens_in": getattr(um, "prompt_token_count", None), "tokens_out": getattr(um, "candidates_token_count", None),
            "tokens_thought": getattr(um, "thoughts_token_count", None),
            "paused_continued": False, "search": s if search else None}


LEGACY_DISPATCH = {"anthropic": call_anthropic, "openai": call_openai, "google": call_google}
CURRENT_DISPATCH = {"anthropic": call_anthropic_current, "openai": call_openai_current, "google": call_google_current}


def _now():
    return datetime.now(timezone.utc).isoformat()


def _call_with_retry(fn, *args):
    last = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            return fn(*args), attempt, None
        except Transient as e:
            last = f"transient: {e}"[:500]
            if attempt < MAX_ATTEMPTS:
                time.sleep(2 ** (attempt - 1))
        except Exception as e:
            return None, attempt, f"{type(e).__name__}: {e}"[:500]
    return None, MAX_ATTEMPTS, last


def cells():
    """(model, arm, condition) in pre-registered order."""
    return ([(m, "L", "S0") for m in LEGACY] + [(m, "C", "S0") for m in CURRENT] + [(m, "C", "S1") for m in CURRENT])


def _invoke(model, arm, cond, prompt):
    if arm == "L":
        return _call_with_retry(LEGACY_DISPATCH[model["provider"]], model["model_id"], prompt)
    return _call_with_retry(CURRENT_DISPATCH[model["provider"]], model["model_id"], prompt, cond == "S1")


def send_cell(model, arm, cond, probe):
    ts_start = _now()
    out, attempts, err = _invoke(model, arm, cond, probe["prompt"])
    empty_retry = False
    if out is not None and not out["text"].strip():
        empty_retry = True
        out2, a2, err2 = _invoke(model, arm, cond, probe["prompt"])
        attempts += a2
        if out2 is not None:
            out = out2
        if err2:
            err = err2
    ts_end = _now()
    time.sleep(PAUSE[model["provider"]])
    status = "error" if out is None else ("empty" if not out["text"].strip() else "ok")
    out = out or {}
    return {
        "phase": "v0.39", "probe_id": probe["probe_id"], "tier": probe["tier"], "kind": probe["kind"],
        "prompt": probe["prompt"], "prompt_sha256": probe["sha256"],
        "arm": arm, "condition": cond,
        "model_slot": model["slot"], "model_name": model["name"], "model_id": model["model_id"],
        "provider": model["provider"], "boundary": model["boundary"],
        "response": out.get("text", ""), "status": status, "error": err,
        "served_model": out.get("served_model"), "finish_reason": out.get("finish_reason"),
        "tokens_in": out.get("tokens_in"), "tokens_out": out.get("tokens_out"), "tokens_thought": out.get("tokens_thought"),
        "attempts": attempts, "empty_retry": empty_retry, "paused_continued": out.get("paused_continued", False),
        "search": out.get("search") if cond == "S1" else None,
        "ts_start": ts_start, "ts_end": ts_end,
    }


def load_probes():
    spec = json.loads(PROBES_PATH.read_text(encoding="utf-8"))
    for p in spec["probes"]:
        if hashlib.sha256(p["prompt"].encode("utf-8")).hexdigest() != p["sha256"]:
            sys.exit(f"ABORT: checksum mismatch on probe {p['probe_id']}")
    expected = spec.get("calls", {}).get("total")
    if expected is not None and expected != len(spec["probes"]) * len(cells()):
        sys.exit("ABORT: call count in probe file does not match the panel")
    return spec["probes"]


def save(records, path=RAW_PATH):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def require_keys():
    missing = [v for v in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY") if not os.environ.get(v)]
    if missing:
        sys.exit(f"ERROR: missing environment variables: {', '.join(missing)}")


def feasibility():
    """Neutral, non-category prompts only (pre-registration section 10, item 3). No study probe."""
    require_keys()
    def feas(pid, prompt):
        return {"probe_id": pid, "tier": "-", "kind": "feasibility", "prompt": prompt,
                "sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest()}

    neutral = feas("FEAS", FEASIBILITY_PROMPT)
    searches = [feas(f"FEAS-S1{'ab'[i]}", p) for i, p in enumerate(FEASIBILITY_SEARCH_PROMPTS)]
    plan = ([(m, a, "S0", neutral) for m, a, c in cells() if c == "S0"]
            + [(m, "C", "S1", s) for s in searches for m in CURRENT])
    recs = []
    for m, a, c, p in plan:
        r = send_cell(m, a, c, p)
        r["phase"] = "v0.39-feasibility"
        recs.append(r)
        srch = r.get("search") or {}
        print(f"  {m['slot']} {m['name']:22s} {c} {r['status']:5s} served={r['served_model']} fr={r['finish_reason']} "
              f"searches={srch.get('n_searches', '-')} sources={len(srch.get('sources', [])) if srch else '-'} "
              f"reply={r['response'].strip()[:40]!r} err={r['error']}", flush=True)
    out = {"phase": "v0.39", "purpose": "pre-lock feasibility check (non-acquisition; no study probe sent)",
           "run_utc": _now(), "prompts": {"S0": FEASIBILITY_PROMPT, "S1": FEASIBILITY_SEARCH_PROMPTS}, "records": recs}
    FEASIBILITY_PATH.parent.mkdir(parents=True, exist_ok=True)
    FEASIBILITY_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    ok = sum(r["status"] == "ok" for r in recs)
    searched = {r["model_slot"] for r in recs if r["condition"] == "S1" and (r.get("search") or {}).get("n_searches", 0) > 0}
    print(f"\nFeasibility: {ok}/{len(recs)} ok; S1 tool used on at least one neutral prompt by {len(searched)}/{len(CURRENT)} "
          f"current models ({', '.join(sorted(searched)) or 'none'}) -> {FEASIBILITY_PATH}")


def main():
    ap = argparse.ArgumentParser(description="AIAS v0.39 acquisition — commercial coffee roasters (Bellwether-focal)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--feasibility", action="store_true", help="neutral non-category pings only; no study probe")
    ap.add_argument("--resume", action="store_true", help="keep cells already 'ok' in the raw file")
    args = ap.parse_args()
    if args.feasibility:
        feasibility()
        return
    probes = load_probes()
    plan = [(p, m, a, c) for p in probes for m, a, c in cells()]
    if args.dry_run:
        for p, m, a, c in plan:
            print(f"  DRY RUN: {p['probe_id']} [{p['tier']}] -> {m['slot']} {m['name']} arm={a} {c}")
        print(f"\nDry run complete. {len(plan)} calls would be sent.")
        return
    require_keys()
    done = {}
    if args.resume and RAW_PATH.exists():
        for r in json.loads(RAW_PATH.read_text(encoding="utf-8")):
            if r["status"] == "ok":
                done[(r["probe_id"], r["model_slot"], r["condition"])] = r
    records = []
    for n, (p, m, a, c) in enumerate(plan, 1):
        key = (p["probe_id"], m["slot"], c)
        if key in done:
            records.append(done[key])
            continue
        rec = send_cell(m, a, c, p)
        records.append(rec)
        srch = rec.get("search") or {}
        print(f"  [{n:3d}/{len(plan)}] {p['probe_id']} -> {m['slot']} {c} {m['name']:22s} {rec['status']:5s} "
              f"served={rec['served_model']} out={rec['tokens_out']} fr={rec['finish_reason']}"
              + (f" searches={srch.get('n_searches')}" if c == "S1" else ""), flush=True)
        if n % 12 == 0:
            save(records)
    save(records)
    ok = sum(r["status"] == "ok" for r in records)
    print(f"\nAcquisition complete: {ok}/{len(records)} ok -> {RAW_PATH}")


if __name__ == "__main__":
    main()
