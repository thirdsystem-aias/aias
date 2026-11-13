#!/usr/bin/env python3
"""
AIAS v0.40 — US airlines and retail banks (leaders, challengers and ghosts): acquisition.
Pre-registration: osf/v40/prereg/PRE_REGISTRATION_v0_40.md (tag v0.40-prereg-r1, not yet locked).

Generated (2026-11-12) as a fork of osf/v39/scripts/acquire_v0_39.py:
  * legacy arm (M1-M6): call_anthropic, call_openai and call_google copied VERBATIM from acquire_v0_39.py
    (temperature 0.0, max output 2,048 tokens, single user turn, no system prompt); added call_google_budget0, which
    is call_google with thinking_config(thinking_budget=0) and nothing else changed, for Gemini 2.5 Flash's three runs;
    the extra Gemini 2.5 Flash pass (slot M5X) uses the verbatim call_google, i.e. the v0.39 setting.
  * current arm: call_anthropic_current, call_openai_current, call_google_current, _empty_search, _dump, Transient,
    _now and _call_with_retry as v0.42 carries them (git show v0.42:osf/v42/scripts/acquire_v0_42.py), i.e. v0.39's
    functions plus an optional system argument (always None here) and the billed-search usage fields; the Anthropic
    Message Batches runner, batch journal and recovery, the synchronous runner, the one-collection-at-a-time guard
    and the writer are copied from the same file. Budget: budget_v0_40.py (fork of budget_v0_42.py).
Design (pre-registration section 4): 94 probes (prereg/probes_v0_40.json, frozen 2026-11-12).
  Legacy arm, S0, 3 runs per cell: 94 x 6 x 3 = 1,692; plus Gemini 2.5 Flash at the v0.39 setting, 1 run: 94.
  Current arm (Claude Fable 5.2 via the Message Batches API; GPT-6 Astra and Gemini 4 Argon synchronous):
    S0, 3 runs: 94 x 3 x 3 = 846; S1 (each provider's own web search), 1 run, on the 32 recommendation probes and
    the 31 status (S) probes: 63 x 3 = 189. Total 2,821 calls.
  Output cap: legacy 2,048; current 16,384. Temperature, top_p, top_k and reasoning effort are never sent to the
  current arm (provider defaults).
Order (blocks; within a block one worker per model slot in parallel): L run 1, L run 2, L run 3, L-X (Flash at the
  v0.39 setting), C S0 run 1, C S0 run 2, C S0 run 3, C S1 run 1. All S1 calls are sent in that last block, inside one
  window: no new S1 request later than S1_WINDOW_HOURS after the first S1 request (or after the collection window).
Budget guard (budget_v0_40.py): spend from the recorded usage of every billed request; worst case reserved before a
  request is sent; no new request once spend >= $80 until approved (--approve-past-80); hard stop at $100.
Collection window: 2026-11-17 00:00 CT to 2026-11-21 23:59:59 CT (the legacy panel retires from 2026-11-24).
Output (append-only, one JSON line per attempt, resumable): osf/v40/data/v40_raw.jsonl

Modes:
  --dry-run       build the call matrix, print it with the cost estimate; send nothing
  --fake-run DIR  run the whole collection loop against FAKE providers into DIR (zero cost; nothing is sent)
  --feasibility   the declared technical check: neutral, non-category prompts only (never a study probe)
  --collect       refused unless tag v0.40-prereg-r1 is on origin AND osf/v40/anchor/osf_anchor_v0_40.json names its
                  commit, the pre-lock check passed (prereg/prelock_check_v0_40.json, section 4.8), inside the
                  collection window, and while no other paid collection runs
  --resume-model SLOT NOTE  journal the pre-registrant's decision to resume a slot paused by the stop rule
Stop rule (added 2026-11-13, section 4.7; stoprule_v0_40.py): every written line is assessed; an answer that stops at
  the length limit before naming a registry brand pauses its model slot (M5X exempt, pending the pre-registrant) and is
  reported; exit code 7 when the run ends with a paused slot. The pre-lock check's spend (prereg/
  prelock_check_v0_40.jsonl) is carried into the budget ledger, so it counts toward the $100 cap.
"""
import argparse
import hashlib
import inspect
import json
import os
import re
import subprocess
import sys
import threading
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from functools import partial
from pathlib import Path

ROOT = Path(os.environ.get("AIAS_ROOT", str(Path(__file__).resolve().parents[3])))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import budget_v0_40 as BG  # noqa: E402
import stoprule_v0_40 as SR  # noqa: E402  (length-limit stop rule, pre-registration section 4.7; added 2026-11-13)

V40 = ROOT / "osf" / "v40"
PROBES_PATH = V40 / "prereg" / "probes_v0_40.json"
RAW_PATH = V40 / "data" / "v40_raw.jsonl"
STATE_PATH = V40 / "data" / "v40_budget_state.json"
BATCH_LOG = V40 / "data" / "v40_batches.jsonl"
FEASIBILITY_PATH = V40 / "prereg" / "feasibility_check_v0_40.json"
ANCHOR_PATH = V40 / "anchor" / "osf_anchor_v0_40.json"
STOP_JOURNAL = V40 / "data" / "v40_stoprule.jsonl"                 # stop-rule events (section 4.7)
PRELOCK_RAW = V40 / "prereg" / "prelock_check_v0_40.jsonl"          # pre-lock check answers (section 4.8)
PRELOCK_RESULT = V40 / "prereg" / "prelock_check_v0_40.json"        # its verdict (must be PASS before --collect)
PREREG_TAG = "v0.40-prereg-r1"
N_PROBES = 94
PROBES_SHA256 = "93aee03f655cb8c4c6b04211e941b854bd921c3dbd31a9f5ffbaa91249be38ca"  # registry draft r3, item 6

LEGACY = [
    {"slot": "M1", "name": "Claude Opus 4.5", "provider": "anthropic", "model_id": "claude-opus-4-5", "arm": "L", "dispatch": "anthropic", "mode": "standard"},
    {"slot": "M2", "name": "Claude Sonnet 4.5", "provider": "anthropic", "model_id": "claude-sonnet-4-5", "arm": "L", "dispatch": "anthropic_legacy_org", "mode": "standard"},
    {"slot": "M3", "name": "GPT-4o", "provider": "openai", "model_id": "gpt-4o", "arm": "L", "dispatch": "openai", "mode": "standard"},
    {"slot": "M4", "name": "GPT-4o-mini", "provider": "openai", "model_id": "gpt-4o-mini", "arm": "L", "dispatch": "openai", "mode": "standard"},
    {"slot": "M5", "name": "Gemini 2.5 Flash (thinking budget 0)", "provider": "google", "model_id": "gemini-2.5-flash", "arm": "L", "dispatch": "google_budget0", "mode": "standard"},
    {"slot": "M6", "name": "Gemini 2.5 Flash Lite", "provider": "google", "model_id": "gemini-2.5-flash-lite", "arm": "L", "dispatch": "google", "mode": "standard"},
]
LEGACY_X = {"slot": "M5X", "name": "Gemini 2.5 Flash (v0.39 setting)", "provider": "google", "model_id": "gemini-2.5-flash", "arm": "L", "dispatch": "google", "mode": "standard"}
# Current arm: each provider's newest generally available flagship, checked on the vendors' pages on 2026-11-12
# (pre-registration section 4.3). Gemini 4 Carbon is excluded: "available to verified enterprise customers in select
# regions" (Google Cloud model page), i.e. restricted.
CURRENT = [
    {"slot": "C1", "name": "Claude Fable 5.2", "provider": "anthropic", "model_id": "claude-fable-5-2", "arm": "C", "mode": "batch"},
    {"slot": "C2", "name": "GPT-6 Astra", "provider": "openai", "model_id": "gpt-6-astra", "arm": "C", "mode": "standard"},
    {"slot": "C3", "name": "Gemini 4 Argon", "provider": "google", "model_id": "gemini-4-argon", "arm": "C", "mode": "standard"},
]
PANEL = LEGACY + [LEGACY_X] + CURRENT
# (arm, condition, run, slots, probe filter) in collection order
S1_KINDS = {"recommendation"}
S1_TIERS = {"S"}
BLOCKS = [("L", "S0", 1), ("L", "S0", 2), ("L", "S0", 3), ("LX", "S0", 1),
          ("C", "S0", 1), ("C", "S0", 2), ("C", "S0", 3), ("C", "S1", 1)]
EXPECTED_TOTAL = 2821
S1_WINDOW_HOURS = 24
WINDOW_START = datetime(2026, 11, 17, 6, 0, 0, tzinfo=timezone.utc)      # 2026-11-17 00:00 CT
WINDOW_HARD_END = datetime(2026, 11, 22, 5, 59, 59, tzinfo=timezone.utc)  # 2026-11-21 23:59:59 CT
WINDOW_HOURS = 120

S1_ANTHROPIC = {"type": "web_search_20250305", "name": "web_search", "max_uses": 5,
                "user_location": {"type": "approximate", "country": "US"}}
S1_OPENAI = {"type": "web_search", "search_context_size": "medium",
             "user_location": {"type": "approximate", "country": "US"}}
S1_OPENAI_INCLUDE = ["web_search_call.action.sources"]

LEGACY_MAX_TOKENS = 2048
CURRENT_MAX_TOKENS = 16384
PAUSE = {"anthropic": 2.0, "openai": 1.0, "google": 1.0}
MAX_ATTEMPTS = 3
BATCH_POLL_SECONDS = 60
EMPTY_RESENDS = 1
PAID_COLLECTION = re.compile(r"acquire_v[0-9][0-9_.]*\.py\b.*--collect")
DEADLINE = None
STOP = None          # stoprule_v0_40.StopRule while a collection (or a fake run) is active

FEASIBILITY_PROMPT = "Reply with the single word: ready"
FEASIBILITY_SEARCH_PROMPTS = [
    "Use web search to find today's date in Coordinated Universal Time. Reply with the date only.",
    "Search the web for the current top headline on bbc.com and give the source URL.",
]


# ======================= copied from acquire_v0_42.py (v0.39 current-arm functions) =======================

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


# ======================= current arm (new in v0.39) =======================

def call_anthropic_current(model_id, prompt, search, system=None):
    import anthropic
    client = anthropic.Anthropic()
    msgs = [{"role": "user", "content": prompt}]
    kw = {"model": model_id, "max_tokens": CURRENT_MAX_TOKENS}
    if system:
        kw["system"] = system
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


def call_openai_current(model_id, prompt, search, system=None):
    import openai
    client = openai.OpenAI()
    kw = {"model": model_id, "input": prompt, "max_output_tokens": CURRENT_MAX_TOKENS}
    if system:
        kw["instructions"] = system
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
    n_calls = 0                 # C28: web_search_call items (billed tool calls)
    for item in (r.output or []):
        d = _dump(item)
        if not isinstance(d, dict):
            continue
        if d.get("type") == "web_search_call":
            n_calls += 1
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
            "billed_searches": n_calls,
            "paused_continued": False, "search": s if search else None}


def call_google_current(model_id, prompt, search, system=None):
    from google import genai
    from google.genai import errors, types
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    cfg = {"max_output_tokens": CURRENT_MAX_TOKENS}
    if system:
        cfg["system_instruction"] = system
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
            "tokens_tool_prompt": getattr(um, "tool_use_prompt_token_count", None),
            "billed_searches": max(s["n_searches"], 1 if s["sources"] else 0),
            "paused_continued": False, "search": s if search else None}


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




# ======================= legacy arm (verbatim from acquire_v0_39.py, which kept v0.38's) =======================

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


# Key routing (new, 2026-11-13, before the lock). The pre-lock check's first run sent Claude Sonnet 4.5's 24 calls with
# ANTHROPIC_API_KEY and all returned 404 "model: claude-sonnet-4-5": the new Anthropic organization does not serve that
# model. The old organization does (it served v0.42's Sonnet 4.5 coding judge under the pre-registrant's option (a),
# 2026-11-11). M2 is therefore sent by this copy of call_anthropic with the old organization's key; the request is
# unchanged (same model, max_tokens, temperature and message) and each record names the key's environment variable.
LEGACY_ORG_KEY_ENV = "ANTHROPIC_API_KEY_LEGACY"


def call_anthropic_legacy_org(model_id, prompt):
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ[LEGACY_ORG_KEY_ENV])  # the old organization's key
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
            "tokens_in": m.usage.input_tokens, "tokens_out": m.usage.output_tokens, "tokens_thought": None,
            "api_key_env": LEGACY_ORG_KEY_ENV}


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


# Gemini 2.5 Flash, thinking budget 0 (v0.40 primary setting for slot M5)
def call_google_budget0(model_id, prompt):
    """call_google (verbatim v0.39) with thinking_config(thinking_budget=0); nothing else changed."""
    from google import genai
    from google.genai import errors, types
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    try:
        r = client.models.generate_content(model=model_id, contents=prompt,
                                           config=types.GenerateContentConfig(temperature=0.0, max_output_tokens=2048,
                                                                                   thinking_config=types.ThinkingConfig(thinking_budget=0)))
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



# ======================= copied from acquire_v0_42.py (guards, batch runner, sync runner, writer) =======================

def process_table():
    r = subprocess.run(["ps", "-axo", "pid=,ppid=,command="], capture_output=True, text=True)
    rows = {}
    for line in r.stdout.splitlines():
        parts = line.strip().split(None, 2)
        if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
            rows[int(parts[0])] = (int(parts[1]), parts[2] if len(parts) == 3 else "")
    return rows


def other_collection_guard(rows=None, me=None):
    """One paid collection on the machine at a time (pre-registration header): refuse while any acquire_v*.py --collect
    runs outside this process's own family (itself, its ancestors, its descendants)."""
    rows = process_table() if rows is None else rows
    me = os.getpid() if me is None else me
    family, p = {me}, me
    while p in rows and rows[p][0] > 0 and rows[p][0] not in family:
        p = rows[p][0]
        family.add(p)
    desc, grew = {me}, True
    while grew:
        grew = False
        for pid, (ppid, _) in rows.items():
            if ppid in desc and pid not in desc:
                desc.add(pid)
                grew = True
    family |= desc
    others = [(pid, cmd) for pid, (ppid, cmd) in rows.items() if pid not in family and PAID_COLLECTION.search(cmd)]
    if others:
        sys.exit("REFUSED: another paid collection is running: " + "; ".join(f"{p} {c[:120]}" for p, c in others))
    return sorted(family)


def _journal(path, event):
    if path is None:
        return
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def open_batches(path):
    """Batches the journal records as created but not as recorded (a run stopped while they were in flight)."""
    created, recorded = {}, set()
    if path is not None and Path(path).exists():
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("event") == "created":
                created[ev["batch_id"]] = ev
            elif ev.get("event") == "recorded":
                recorded.add(ev["batch_id"])
    return [ev for bid, ev in created.items() if bid not in recorded]


def written_batch_requests(raw_path):
    """(batch_id, custom_id) of every raw line already written (so a recovered batch never writes a line twice)."""
    out = set()
    if raw_path is not None and Path(raw_path).exists():
        for line in Path(raw_path).read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("batch_id"):
                out.add((r["batch_id"], r.get("custom_id")))
    return out


def _part(out, mode, cond):
    """Usage of one billed request, for budget_v0_42.record_cost. Clarification C28 (conservative): n_searches is the
    larger of the searches recorded in `search` and the provider's billed tool calls (`billed_searches`); Google's
    tool_use_prompt_token_count is added to input_tokens (and kept as tool_use_prompt_tokens)."""
    s = out.get("search") or {}
    tin, tool = out.get("tokens_in"), out.get("tokens_tool_prompt")
    n = max(int(s.get("n_searches") or 0), int(out.get("billed_searches") or 0)) if cond == "S1" else 0
    return {"mode": mode, "input_tokens": None if tin is None and tool is None else (tin or 0) + (tool or 0),
            "output_tokens": out.get("tokens_out"), "thinking_tokens": out.get("tokens_thought"),
            "tool_use_prompt_tokens": tool, "n_searches": n}


def _anthropic_billed_searches(m, blocks):
    """C28: web searches of one Anthropic message: the larger of its server_tool_use blocks and
    usage.server_tool_use.web_search_requests (the field Anthropic bills on)."""
    u = getattr(getattr(m, "usage", None), "server_tool_use", None)
    return max(_searches_in(blocks), int(getattr(u, "web_search_requests", None) or 0))


def _record(spec, out, status, err, attempts, empty_retry, ts_start, ts_end, parts, extra=None):
    out = out or {}
    model, cond = spec["model"], spec["condition"]
    rec = {
        "call_id": spec["call_id"], "substrate": spec["substrate"], "phase": spec["phase"],
        "probe_id": spec["probe_id"], "brand_id": spec["brand_id"], "frame_id": spec["frame_id"],
        "arm": spec["arm"], "slot": spec["model"]["slot"], "tier": spec["tier"], "kind": spec["kind"],
        "category": spec["category"],
        "model_requested": model["model_id"], "provider": model["provider"],
        "served_model": out.get("served_model"), "condition": cond, "run": spec["run"],
        "system": spec["system"], "prompt": spec["prompt"],
        "text": out.get("text", ""), "status": status, "error": err,
        "finish_reason": out.get("finish_reason"),
        "input_tokens": out.get("tokens_in"), "output_tokens": out.get("tokens_out"),
        "thinking_tokens": out.get("tokens_thought"),
        "tool_use_prompt_tokens": out.get("tokens_tool_prompt"),          # C28 (Google; None for the others)
        "search": out.get("search") if cond == "S1" else None,
        "paused_continued": out.get("paused_continued", False),
        "attempts": attempts, "empty_retry": empty_retry,
        "started_utc": ts_start, "finished_utc": ts_end,
        "mode": model.get("mode", "standard"), "usage_parts": parts,
    }
    if out.get("api_key_env"):
        rec["api_key_env"] = out["api_key_env"]                          # key routing, 2026-11-13 (legacy arm)
    rec.update(extra or {})
    rec["cost_usd"] = BG.record_cost(rec)
    return rec


def send_call(spec):
    """Synchronous call (GPT-6 Astra, Gemini 4 Argon; and the feasibility check). As r1, plus the usage of every
    billed request (an empty first answer is billed too) in `usage_parts`."""
    model, cond = spec["model"], spec["condition"]
    ts_start = _now()
    out, attempts, err = _invoke(model, cond, spec["prompt"], spec["system"])
    parts = [_part(out, "standard", cond)] if out is not None else []
    empty_retry = False
    extra = None
    if out is not None and not out["text"].strip():
        empty_retry = True
        # the stop rule (section 4.7) also reads the empty first answer's finish reason (added 2026-11-13)
        extra = {"first_attempt_finish_reason": out.get("finish_reason")}
        out2, a2, err2 = _invoke(model, cond, spec["prompt"], spec["system"])
        attempts += a2
        if out2 is not None:
            out = out2
            parts.append(_part(out2, "standard", cond))
        if err2:
            err = err2
    ts_end = _now()
    time.sleep(PAUSE[model["provider"]])
    status = "error" if out is None else ("empty" if not out["text"].strip() else "ok")
    return _record(spec, out, status, err, attempts, empty_retry, ts_start, ts_end, parts, extra)


# ----------------------------------------------------------------- Anthropic Message Batches (Claude Fable 5.2)
def anthropic_params(spec):
    """Request parameters of one batched request: exactly the keyword arguments call_anthropic_current sends."""
    kw = {"model": spec["model"]["model_id"], "max_tokens": CURRENT_MAX_TOKENS,
          "messages": [{"role": "user", "content": spec["prompt"]}]}
    if spec["system"]:
        kw["system"] = spec["system"]
    if spec["condition"] == "S1":
        kw["tools"] = [S1_ANTHROPIC]
    return kw


def parse_anthropic_blocks(blocks, search):
    """Text and search record from Anthropic content blocks: the parsing of call_anthropic_current, unchanged."""
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
    return "".join(text), (s if search else None)


def _searches_in(blocks):
    return sum(1 for b in blocks if getattr(b, "type", None) == "server_tool_use" and getattr(b, "name", "") == "web_search")


def _batch_message_out(spec, m, client, ledger):
    """Turn a succeeded batch message into the call-function output; a pause_turn is continued once,
    synchronously, with identical tools (section 4.4), under the budget guard. -> (out, parts, note)"""
    search = spec["condition"] == "S1"
    blocks = list(m.content)
    parts = [{"mode": "batch", "input_tokens": m.usage.input_tokens, "output_tokens": m.usage.output_tokens,
              "thinking_tokens": None, "n_searches": _anthropic_billed_searches(m, blocks) if search else 0}]
    paused, note = False, None
    if m.stop_reason == "pause_turn":
        st, tok = ledger.reserve(BG.worst_case(spec["model"]["model_id"], spec["condition"], "standard"))
        if st == "ok":
            paused = True
            kw = anthropic_params(spec)
            msgs = kw.pop("messages")
            try:
                m2 = client.messages.create(messages=msgs + [{"role": "assistant", "content": m.content}], **kw)
                b2 = list(m2.content)
                blocks += b2
                parts.append({"mode": "standard", "input_tokens": m2.usage.input_tokens,
                              "output_tokens": m2.usage.output_tokens, "thinking_tokens": None,
                              "n_searches": _anthropic_billed_searches(m2, b2) if search else 0})
                m = m2
            except Exception as e:  # recorded; the call keeps its first part
                note = f"pause_turn continuation failed: {type(e).__name__}: {e}"[:500]
            ledger.settle(tok, 0.0)
        else:
            note = f"pause_turn not continued: budget guard {st}"
    text, srec = parse_anthropic_blocks(blocks, search)
    out = {"text": text, "served_model": m.model, "finish_reason": m.stop_reason,
           "tokens_in": sum(p["input_tokens"] or 0 for p in parts), "tokens_out": sum(p["output_tokens"] or 0 for p in parts),
           "tokens_thought": None, "paused_continued": paused, "search": srec}
    return out, parts, note


TRANSIENT_BATCH_ERRORS = ("api_error", "overloaded_error", "rate_limit_error", "timeout_error")


def run_anthropic_batch(specs, ledger, write, client=None, poll=None, sleep=time.sleep, journal=None):
    """Send `specs` (one model, one block) through the Message Batches API under the budget guard.
    Each attempt is one raw line. Transient errors and expired requests are re-sent up to MAX_ATTEMPTS attempts;
    an empty answer is re-sent once. With `journal`, every created batch is journaled before it is polled and marked
    recorded once its lines are written (recover_batches). Returns 'done' | 'pause' | 'stop'."""
    if client is None:
        import anthropic
        client = anthropic.Anthropic()
    poll = BATCH_POLL_SECONDS if poll is None else poll
    pending = [(s, 1, 0) for s in specs]          # (spec, attempt number, empty re-sends so far)
    while pending:
        if past_deadline(ledger):
            return "stop"
        if STOP is not None and STOP.is_paused(pending[0][0]["model"]["slot"]):   # stop rule (section 4.7)
            return "model_paused"
        model_id, cond = pending[0][0]["model"]["model_id"], pending[0][0]["condition"]
        st, k, tok = ledger.fit(BG.worst_case(model_id, cond, "batch"), len(pending))
        if st == "wait":
            sleep(5)
            continue
        if st != "ok":
            return st
        chunk, pending = pending[:k], pending[k:]
        ids = {f"v40-{i:04d}-a{att}": (s, att, ne) for i, (s, att, ne) in enumerate(chunk)}
        reqs = [{"custom_id": cid, "params": anthropic_params(s)} for cid, (s, _, _) in ids.items()]
        ts_start = _now()
        try:
            b = client.messages.batches.create(requests=reqs)
        except Exception as e:
            ledger.settle(tok, 0.0)
            for cid, (s, att, ne) in ids.items():
                write(_record(s, None, "error", f"batch create failed: {type(e).__name__}: {e}"[:500], att, ne > 0,
                              ts_start, _now(), [], {"batch_id": None, "custom_id": cid}))
            return "stop"
        _journal(journal, {"event": "created", "batch_id": b.id, "utc": ts_start,
                           "requests": [{"custom_id": cid, "call_id": s["call_id"], "attempt": att, "empty_resends": ne}
                                        for cid, (s, att, ne) in ids.items()]})
        retry, spent = _finish_batch(b.id, ids, client, ledger, write, ts_start, poll, sleep)
        ledger.settle(tok, spent)
        _journal(journal, {"event": "recorded", "batch_id": b.id, "utc": _now()})
        pending = retry + pending
    return "done"


def recover_batches(specs, ledger, write, journal, raw_path, client=None, poll=None, sleep=time.sleep, log=print):
    """Before any new request: every batch the journal shows as created but not recorded (the run that created it
    stopped while it was in flight) is polled until it ends and its results are written and costed exactly as
    run_anthropic_batch writes them; lines already written for it are not written again. Re-sends of its failed or
    empty requests are left to the collection pass (the call is not done). Returns the number of batches recovered."""
    todo = open_batches(journal)
    if not todo:
        return 0
    if client is None:
        import anthropic
        client = anthropic.Anthropic()
    poll = BATCH_POLL_SECONDS if poll is None else poll
    by_id = {s["call_id"]: s for s in specs}
    seen = written_batch_requests(raw_path)
    for ev in todo:
        ids = {r["custom_id"]: (by_id[r["call_id"]], r["attempt"], r["empty_resends"]) for r in ev["requests"]
               if (ev["batch_id"], r["custom_id"]) not in seen}
        log(f"recovering batch {ev['batch_id']} (created {ev['utc']}): {len(ids)} of {len(ev['requests'])} results to record")
        _, spent = _finish_batch(ev["batch_id"], ids, client, ledger, write, ev["utc"], poll, sleep)
        ledger.settle(None, spent)
        _journal(journal, {"event": "recorded", "batch_id": ev["batch_id"], "utc": _now(), "recovered": True})
    return len(todo)


def _finish_batch(batch_id, ids, client, ledger, write, ts_start, poll, sleep):
    """Poll one batch until it ends, then write one raw line per request in `ids`. -> (retry list, USD written)."""
    while True:
        b = client.messages.batches.retrieve(batch_id)
        if getattr(b, "processing_status", None) == "ended":
            break
        sleep(poll)
    ts_end = getattr(b, "ended_at", None)
    ts_end = ts_end.isoformat() if hasattr(ts_end, "isoformat") else (ts_end or _now())
    results = {r.custom_id: r.result for r in client.messages.batches.results(b.id)}
    retry, spent = [], 0.0
    for cid, (s, att, ne) in ids.items():
        res = results.get(cid)
        rtype = getattr(res, "type", "missing")
        extra = {"batch_id": b.id, "custom_id": cid}
        if rtype == "succeeded":
            out, parts, note = _batch_message_out(s, res.message, client, ledger)
            empty = not out["text"].strip()
            rec = _record(s, out, "empty" if empty else "ok", note, att, ne > 0, ts_start, ts_end, parts, extra)
            if empty and ne < EMPTY_RESENDS:
                retry.append((s, att + 1, ne + 1))
        else:
            err = getattr(res, "error", None)
            etype = getattr(getattr(err, "error", err), "type", None) if err is not None else None
            rec = _record(s, None, "error", f"batch result {rtype}" + (f": {etype}" if etype else ""), att, ne > 0,
                          ts_start, ts_end, [], extra)
            transient = rtype == "expired" or (rtype == "errored" and etype in TRANSIENT_BATCH_ERRORS)
            if transient and att < MAX_ATTEMPTS:
                retry.append((s, att + 1, ne))
        write(rec)
        spent += rec["cost_usd"]
    return retry, spent


def run_sync(specs, ledger, write, sender=None, sleep=time.sleep):
    """Send `specs` (one model, one block) one at a time under the budget guard. Returns 'done' | 'pause' | 'stop'."""
    sender = sender or send_call
    for s in specs:
        if past_deadline(ledger):
            return "stop"
        if STOP is not None and STOP.is_paused(s["model"]["slot"]):   # stop rule (section 4.7): before the next request
            return "model_paused"
        while True:
            # C28: a synchronous call may bill 1 + EMPTY_RESENDS requests (an empty answer is re-sent)
            st, tok = ledger.reserve((1 + EMPTY_RESENDS) * BG.worst_case(s["model"]["model_id"], s["condition"], "standard"))
            if st != "wait":
                break
            sleep(5)
        if st != "ok":
            return st
        rec = sender(s)
        write(rec)
        ledger.settle(tok, rec["cost_usd"])
    return "done"


def warm_imports():
    """Import the SDK modules once in the main thread before any worker thread starts (2026-11-13): the pre-lock
    check's first run lost one GPT-6 Astra call to "_DeadlockError: deadlock detected by
    _ModuleLock('openai.resources.chat')" when two threads imported that module lazily at the same time."""
    import anthropic  # noqa: F401
    import anthropic.resources.messages  # noqa: F401
    import openai  # noqa: F401
    import openai.resources.chat  # noqa: F401
    import openai.resources.responses  # noqa: F401
    from google import genai  # noqa: F401
    from google.genai import types  # noqa: F401


def require_keys():
    if not os.environ.get("GOOGLE_API_KEY") and os.environ.get("GEMINI_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]  # call_google_current reads GOOGLE_API_KEY
    needed = ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY", LEGACY_ORG_KEY_ENV)
    missing = [v for v in needed if not os.environ.get(v)]
    if missing:
        sys.exit(f"ERROR: missing environment variables: {', '.join(missing)}")
    warm_imports()


def done_ids(raw_path=None):
    done = set()
    raw_path = RAW_PATH if raw_path is None else raw_path
    if raw_path.exists():
        for line in raw_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if (r.get("text") or "").strip() and not r.get("error") and r.get("status", "ok") == "ok":
                done.add(r["call_id"])
    return done


def block_cost(raw_path, block):
    """Actual cost of every raw line of one (phase, condition, run) block."""
    ph, cond, run = block
    tot = 0.0
    if raw_path.exists():
        for line in raw_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                if r.get("phase") == ph and r.get("condition") == cond and r.get("run") == run:
                    tot += BG.record_cost(r)
    return tot


def blocks_started(raw_path):
    """(phase, condition, run) of every block with at least one raw line."""
    out = set()
    if raw_path.exists():
        for line in raw_path.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            out.add((r.get("phase"), r.get("condition"), r.get("run")))
    return out


def make_writer(raw_path, log=print):
    """Thread-safe append of one raw line (fsynced), with a one-line log."""
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    lock = threading.Lock()

    def write(rec):
        with lock:
            with open(raw_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
                os.fsync(f.fileno())
        s = rec.get("search") or {}
        log(f"  {rec['call_id']} {rec['status']} out={rec['output_tokens']} fr={rec['finish_reason']} "
            f"${rec['cost_usd']:.4f}" + (f" searches={s.get('n_searches')}" if rec["condition"] == "S1" else ""))
    return write




# ======================= v0.40 wrapper (new) =======================

LEGACY_DISPATCH = {"anthropic": call_anthropic, "openai": call_openai, "google": call_google,
                   "google_budget0": call_google_budget0,
                   "anthropic_legacy_org": call_anthropic_legacy_org}       # M2, key routing of 2026-11-13
CURRENT_DISPATCH = {"anthropic": call_anthropic_current, "openai": call_openai_current, "google": call_google_current}


def load_probes(path=None):
    path = PROBES_PATH if path is None else path
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != PROBES_SHA256:
        sys.exit(f"ABORT: {path.name} does not match the frozen checksum {PROBES_SHA256}")
    probes = json.loads(raw.decode("utf-8"))["probes"]
    for p in probes:
        if hashlib.sha256(p["prompt"].encode("utf-8")).hexdigest() != p["sha256"]:
            sys.exit(f"ABORT: checksum mismatch on probe {p['probe_id']}")
    if len(probes) != N_PROBES:
        sys.exit(f"ABORT: expected {N_PROBES} probes, found {len(probes)}")
    return probes


def call_id(arm, probe_id, slot, model_id, cond, run):
    return f"v40|{arm}|{probe_id}|{slot}|{model_id}|{cond}|{run}"


def in_s1(p):
    return p["kind"] in S1_KINDS or p["tier"] in S1_TIERS


def build_specs(probes):
    """Collection matrix in order: block, then model slot (PANEL order), then probe (file order)."""
    specs = []
    for bi, (arm, cond, run) in enumerate(BLOCKS):
        models = {"L": LEGACY, "LX": [LEGACY_X], "C": CURRENT}[arm]
        for m in models:
            for p in probes:
                if cond == "S1" and not in_s1(p):
                    continue
                specs.append({
                    "call_id": call_id(m["arm"], p["probe_id"], m["slot"], m["model_id"], cond, run),
                    "substrate": "v40", "phase": "v0.40", "arm": m["arm"], "probe_id": p["probe_id"],
                    "tier": p["tier"], "kind": p["kind"], "category": p["category"],
                    "brand_id": p.get("subject_id"), "frame_id": p["tier"],
                    "model": m, "condition": cond, "run": run, "block": bi, "system": None, "prompt": p["prompt"],
                })
    ids = [s["call_id"] for s in specs]
    if len(set(ids)) != len(ids):
        sys.exit("ABORT: duplicate call_id")
    return specs


def _invoke(model, cond, prompt, system):
    if model["arm"] == "L":
        return _call_with_retry(LEGACY_DISPATCH[model["dispatch"]], model["model_id"], prompt)
    return _call_with_retry(CURRENT_DISPATCH[model["provider"]], model["model_id"], prompt, cond == "S1", system)


def collection_deadline(raw_path, now=None):
    """The earlier of WINDOW_HOURS after the first recorded call (else now) and WINDOW_HARD_END."""
    first = first_start(raw_path)
    start = first or now or datetime.now(timezone.utc)
    return min(start + timedelta(hours=WINDOW_HOURS), WINDOW_HARD_END)


def first_start(raw_path, cond=None):
    first = None
    if Path(raw_path).exists():
        for line in Path(raw_path).read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
                if cond and r.get("condition") != cond:
                    continue
                t = datetime.fromisoformat(r["started_utc"]) if r.get("started_utc") else None
            except (json.JSONDecodeError, ValueError, TypeError, KeyError):
                continue
            if t is not None and (first is None or t < first):
                first = t
    return first


def past_deadline(ledger=None, now=None):
    if DEADLINE is None or (now or datetime.now(timezone.utc)) <= DEADLINE:
        return False
    if ledger is not None:
        ledger.halt("stop", f"collection window ended at {DEADLINE.isoformat()}")
    return True


def run_collection(specs, ledger, raw_path, runners, log=print, write=None, now=None):
    """Blocks in order; within a block one worker per model slot in parallel (runners[mode](specs, ledger, write)).
    Before the S1 block, the deadline is tightened to S1_WINDOW_HOURS after the first S1 request (all search-on calls
    in one window). With the stop rule active (STOP; section 4.7) every written line is assessed, a paused slot sends
    nothing more and the other slots go on. Returns 'done' | 'pause' | 'stop' | 'model_paused' (the run went as far as
    it could, but at least one slot is paused by the stop rule)."""
    global DEADLINE
    done = done_ids(raw_path)
    write = write or make_writer(raw_path, log)
    if STOP is not None:
        write = STOP.wrap(write)
    for bi, block in enumerate(BLOCKS):
        todo = [s for s in specs if s["block"] == bi and s["call_id"] not in done
                and not (STOP is not None and STOP.is_paused(s["model"]["slot"]))]
        if not todo:
            continue
        if block[1] == "S1":
            s1_first = first_start(raw_path, "S1") or now or datetime.now(timezone.utc)
            s1_end = s1_first + timedelta(hours=S1_WINDOW_HOURS)
            DEADLINE = s1_end if DEADLINE is None else min(DEADLINE, s1_end)
            log(f"S1 window: no new S1 request after {DEADLINE.isoformat()}")
        log(f"block {bi + 1} {block}: {len(todo)} calls to send; {ledger.summary()}")
        slots = [m["slot"] for m in PANEL]
        groups = [[s for s in todo if s["model"]["slot"] == sl] for sl in slots]
        groups = [(g, runners[g[0]["model"]["mode"]]) for g in groups if g]
        with ThreadPoolExecutor(max_workers=len(groups)) as pool:
            res = list(pool.map(lambda gr: gr[1](gr[0], ledger, write), groups))
        for st in ("stop", "pause"):
            if st in res:
                log(f"HALT ({st}) in block {bi + 1}: {ledger.summary()}")
                return st
    if STOP is not None and STOP.paused_slots():
        log(f"STOP RULE: paused slots {STOP.paused_slots()}; report to the pre-registrant (section 4.7)")
        return "model_paused"
    return "done"


# ----------------------------------------------------------------- fakes (zero-cost dry run of the whole loop)
def _fake_text(model_id, prompt, search):
    h = int(hashlib.sha256(f"{model_id}|{prompt}|{search}".encode()).hexdigest()[:8], 16)
    names = ["Delta Air Lines", "American Airlines", "United Airlines", "Southwest Airlines", "Chase",
             "Bank of America", "Wells Fargo", "Capital One", "US Airways, which merged with American",
             "Wachovia (now part of Wells Fargo)"]
    return f"FAKE answer ({model_id}, search={search}): " + ", ".join(names[(h + i) % len(names)] for i in range(4)) + "."


def fake_legacy(model_id, prompt):
    return {"text": _fake_text(model_id, prompt, False), "served_model": model_id + "-fake", "finish_reason": "stop",
            "tokens_in": 20, "tokens_out": 300, "tokens_thought": None}


def fake_current(model_id, prompt, search, system=None):
    s = _empty_search()
    if search:
        s.update({"n_searches": 1, "queries": ["fake query"], "sources": [{"url": "https://example.org", "title": "x"}]})
    return {"text": _fake_text(model_id, prompt, search), "served_model": model_id + "-fake", "finish_reason": "stop",
            "tokens_in": 20, "tokens_out": 600, "tokens_thought": None, "paused_continued": False,
            "search": s if search else None, "billed_searches": 1 if search else 0}


class FakeBatches:
    """Stands in for anthropic.Anthropic().messages.batches (create / retrieve / results); nothing is sent.
    `stop_reason` and `text` (a function of model, prompt, search) let a test fake an answer cut at the limit."""
    def __init__(self, stop_reason="end_turn", text=None):
        from types import SimpleNamespace as NS
        self.NS, self.store, self.n = NS, {}, 0
        self.stop_reason, self.text = stop_reason, text or _fake_text

    def create(self, requests):
        self.n += 1
        bid = f"fakebatch_{self.n}"
        self.store[bid] = requests
        return self.NS(id=bid)

    def retrieve(self, bid):
        return self.NS(id=bid, processing_status="ended", ended_at=datetime.now(timezone.utc))

    def results(self, bid):
        NS = self.NS
        for r in self.store[bid]:
            p = r["params"]
            search = "tools" in p
            content = []
            if search:
                content.append(NS(type="server_tool_use", name="web_search", input={"query": "fake"}))
            text = self.text(p["model"], p["messages"][0]["content"], search)
            content.append(NS(type="text", text=text, citations=None))
            usage = NS(input_tokens=20, output_tokens=600, server_tool_use=NS(web_search_requests=1 if search else 0))
            msg = NS(content=content, usage=usage, stop_reason=self.stop_reason, model=p["model"])
            yield NS(custom_id=r["custom_id"], result=NS(type="succeeded", message=msg))


def fake_client(**batch_kw):
    from types import SimpleNamespace as NS
    return NS(messages=NS(batches=FakeBatches(**batch_kw), create=None))


def fake_run(out_dir, cap=None, log=print, legacy=None, current=None, batch_kw=None, stop_rule=True, prior_usd=0.0):
    """Whole collection loop against fakes: real specs, budget ledger, writer, batch runner, block order and the
    stop rule (section 4.7; journal in out_dir). Tests may replace the fake providers (`legacy`, `current`, `batch_kw`)
    to fake answers cut at the length limit."""
    global DEADLINE, STOP
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    raw, state, journal = out_dir / "fake_raw.jsonl", out_dir / "fake_budget_state.json", out_dir / "fake_batches.jsonl"
    saved = (dict(LEGACY_DISPATCH), dict(CURRENT_DISPATCH), dict(PAUSE))
    try:
        for k in LEGACY_DISPATCH:
            LEGACY_DISPATCH[k] = legacy or fake_legacy
        for k in CURRENT_DISPATCH:
            CURRENT_DISPATCH[k] = current or fake_current
        for k in PAUSE:
            PAUSE[k] = 0.0
        DEADLINE = None
        STOP = SR.StopRule(SR.v40_named_fn(), journal=out_dir / "fake_stoprule.jsonl", log=lambda *a: None) \
            if stop_rule else None
        ledger = BG.Ledger(raw, state, prior_usd=prior_usd) if cap is None else \
            BG.Ledger(raw, state, cap=cap, pause_at=cap * 0.8, prior_usd=prior_usd)
        specs = build_specs(load_probes())
        client = fake_client(**(batch_kw or {}))
        runners = {"batch": partial(run_anthropic_batch, client=client, poll=0, sleep=lambda s: None, journal=journal),
                   "standard": partial(run_sync, sleep=lambda s: None)}
        st = run_collection(specs, ledger, raw, runners, log=lambda *a: None)
        return st, specs, raw, ledger
    finally:
        LEGACY_DISPATCH.update(saved[0]); CURRENT_DISPATCH.update(saved[1]); PAUSE.update(saved[2])
        DEADLINE = None
        STOP = None


def confirm_no_sampling_params():
    """The current arm must not get temperature/top_p/top_k: check the copied functions and the batch builder."""
    src = (inspect.getsource(call_anthropic_current) + inspect.getsource(anthropic_params)
           + inspect.getsource(call_openai_current) + inspect.getsource(call_google_current))
    return [w for w in ("temperature", "top_p", "top_k") if w in src]


def dry_run():
    specs = build_specs(load_probes())
    bad = confirm_no_sampling_params()
    print(f"sampling params in the current-arm functions: {bad or 'none (temperature/top_p/top_k not sent)'}")
    for bi, block in enumerate(BLOCKS):
        c = Counter(s["model"]["slot"] for s in specs if s["block"] == bi)
        print(f"{bi + 1}. {block}: " + ", ".join(f"{k} {v}" for k, v in c.items()) + f"  = {sum(c.values())}")
    print(f"\nTOTAL calls: {len(specs)} (expected {EXPECTED_TOTAL}) -> {'OK' if len(specs) == EXPECTED_TOTAL else 'MISMATCH'}")
    print("by condition:", dict(Counter(s["condition"] for s in specs)), " by arm:", dict(Counter(s["arm"] for s in specs)))
    print("S1 probes:", len({s["probe_id"] for s in specs if s["condition"] == "S1"}), "(recommendation + status)")
    print("worst-case reservation per request (USD):")
    for m in CURRENT:
        print(f"  {m['model_id']:17s} {m['mode']:8s} S0 {BG.worst_case(m['model_id'], 'S0', m['mode']):.3f}"
              f"  S1 {BG.worst_case(m['model_id'], 'S1', m['mode']):.3f}")
    print(f"budget: pause at ${BG.PAUSE_AT_USD:.0f}, hard stop at ${BG.BUDGET_CAP_USD:.0f}")
    print("nothing sent.")
    return 0 if len(specs) == EXPECTED_TOTAL else 1


def feasibility():
    """Declared technical check (non-acquisition): neutral, non-category prompts only. Never a study probe."""
    require_keys()
    plan = [(m, "S0", FEASIBILITY_PROMPT) for m in PANEL]
    plan += [(m, "S1", p) for p in FEASIBILITY_SEARCH_PROMPTS for m in CURRENT]
    recs = []
    for i, (m, cond, prompt) in enumerate(plan):
        spec = {"call_id": f"FEAS|{i}|{m['slot']}|{cond}", "substrate": "-", "phase": "-", "arm": m["arm"],
                "probe_id": f"FEAS-{i}", "tier": "-", "kind": "feasibility", "category": "-", "brand_id": None,
                "frame_id": None, "model": dict(m, mode="standard"), "condition": cond, "run": 1, "system": None,
                "prompt": prompt}
        r = send_call(spec)
        recs.append({k: r.get(k) for k in ("model_requested", "condition", "served_model", "finish_reason",
                                           "input_tokens", "output_tokens", "thinking_tokens", "status", "error")}
                    | {"slot": m["slot"], "reply": (r.get("text") or "").strip()[:120]})
        print(f"  {m['slot']} {cond} {r['status']} served={r['served_model']} err={r['error']}", flush=True)
    FEASIBILITY_PATH.parent.mkdir(parents=True, exist_ok=True)
    FEASIBILITY_PATH.write_text(json.dumps({"phase": "v0.40", "purpose": "technical check (non-acquisition; no study probe)",
                                            "run_utc": _now(), "records": recs}, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


def prereg_guard():
    """Refuse unless the prereg tag is on origin and the anchor file names its commit."""
    r = subprocess.run(["git", "ls-remote", "--tags", "origin", PREREG_TAG], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"REFUSED: git ls-remote failed: {r.stderr.strip()}")
    shas = dict(reversed(line.split("\t")) for line in r.stdout.splitlines() if "\t" in line)
    tag_ref = f"refs/tags/{PREREG_TAG}"
    if tag_ref not in shas:
        sys.exit(f"REFUSED: tag {PREREG_TAG} not found on origin")
    commit = shas.get(tag_ref + "^{}", shas[tag_ref])
    if not ANCHOR_PATH.exists() or (commit not in ANCHOR_PATH.read_text(encoding="utf-8")
                                    and shas[tag_ref] not in ANCHOR_PATH.read_text(encoding="utf-8")):
        sys.exit(f"REFUSED: {ANCHOR_PATH} missing or does not name the commit of {PREREG_TAG}")
    return commit


def prelock_guard(path=None):
    """Refuse unless the pre-lock check (section 4.8) recorded the verdict PASS."""
    path = PRELOCK_RESULT if path is None else Path(path)
    try:
        verdict = json.loads(Path(path).read_text(encoding="utf-8")).get("verdict")
    except (OSError, json.JSONDecodeError):
        verdict = None
    if verdict != "PASS":
        sys.exit(f"REFUSED: the pre-lock check (section 4.8) has not passed ({path.name}: {verdict})")
    return verdict


def collect(approve_past_80=None):
    global DEADLINE, STOP
    now = datetime.now(timezone.utc)
    if now < WINDOW_START:
        sys.exit(f"REFUSED: the collection window opens {WINDOW_START.isoformat()}")
    other_collection_guard()
    commit = prereg_guard()
    prelock_guard()
    require_keys()
    DEADLINE = collection_deadline(RAW_PATH)
    print(f"prereg guard passed: {PREREG_TAG} -> {commit}; window ends {DEADLINE.isoformat()}")
    prior = BG.spend_of(PRELOCK_RAW)        # the pre-lock check's spend counts toward the $100 cap (section 4.8)
    ledger = BG.Ledger(RAW_PATH, STATE_PATH, prior_usd=prior)
    if approve_past_80:
        ledger.approve("past_80", approve_past_80)
    STOP = SR.StopRule(SR.v40_named_fn(), journal=STOP_JOURNAL)
    if STOP.paused_slots():
        print(f"STOP RULE: slots paused by an earlier trigger and not resumed: {STOP.paused_slots()}")
    specs = build_specs(load_probes())
    write = STOP.wrap(make_writer(RAW_PATH))
    n = recover_batches(specs, ledger, write, BATCH_LOG, RAW_PATH)
    if n:
        print(f"recovered {n} batch(es); budget {ledger.summary()}")
    st = run_collection(specs, ledger, RAW_PATH, {"batch": partial(run_anthropic_batch, journal=BATCH_LOG),
                                                  "standard": run_sync}, write=write)
    print("result:", st, ledger.summary(), "stop rule:", STOP.summary())
    return {"done": 0, "pause": 5, "stop": 6, "model_paused": 7}[st]


def resume_model(slot, note):
    """The pre-registrant's decision to resume a slot paused by the stop rule, unchanged (section 4.7)."""
    if slot not in {m["slot"] for m in PANEL}:
        sys.exit(f"unknown slot {slot}")
    stop = SR.StopRule(lambda text: 0, journal=STOP_JOURNAL)
    if not stop.is_paused(slot):
        sys.exit(f"slot {slot} is not paused")
    print(json.dumps(stop.resume(slot, note)))
    return 0


def main():
    ap = argparse.ArgumentParser(description="AIAS v0.40 acquisition (US airlines and retail banks)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--fake-run", metavar="DIR")
    ap.add_argument("--feasibility", action="store_true", help="declared technical check; never a study probe")
    ap.add_argument("--collect", action="store_true")
    ap.add_argument("--approve-past-80", metavar="NOTE", default=None)
    ap.add_argument("--resume-model", nargs=2, metavar=("SLOT", "NOTE"), default=None,
                    help="journal the pre-registrant's decision to resume a slot paused by the stop rule (section 4.7)")
    a = ap.parse_args()
    if a.resume_model:
        return resume_model(*a.resume_model)
    if sum([a.dry_run, bool(a.fake_run), a.feasibility, a.collect]) != 1:
        ap.error("choose exactly one of --dry-run / --fake-run / --feasibility / --collect / --resume-model")
    if a.dry_run:
        return dry_run()
    if a.fake_run:
        st, specs, raw, ledger = fake_run(a.fake_run)
        rows = [json.loads(l) for l in raw.read_text(encoding="utf-8").splitlines() if l.strip()]
        print(f"fake run: {st}; {len(rows)} lines for {len(specs)} specs; ok {sum(r['status'] == 'ok' for r in rows)}; "
              f"fake spend {ledger.summary()}")
        return 0 if st == "done" and len(rows) == len(specs) else 1
    if a.feasibility:
        return feasibility()
    return collect(a.approve_past_80)


if __name__ == "__main__":
    sys.exit(main())
