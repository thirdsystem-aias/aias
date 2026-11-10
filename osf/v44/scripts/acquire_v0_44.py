#!/usr/bin/env python3
"""
AIAS v0.44 -- industry-breadth wave acquisition (eight new industries, N3, search off), pre-registration draft r1.

FORK of osf/v42/scripts/acquire_v0_42.py (v0.42 r2, commit 527899e). The S1 tool configurations, CURRENT_MAX_TOKENS,
PAUSE, MAX_ATTEMPTS and the block from `class Transient` to the end of `_call_with_retry` (the current-arm call
functions of v0.39) are copied BYTE FOR BYTE from that file (checked by tests/test_acquire_v0_44.py); v0.44 never
sends a tool (S0 only), so the S1 parts of the copied functions are inert. The wrapper below follows v0.42's
(Message Batches path for Claude Fable 5.2, synchronous path for GPT-6 Astra and Gemini 4 Argon, budget guard,
resumable append-only raw file) with these v0.44 changes:
  - design: N3 x (Phase B 48 category questions x S0 x runs 1-3 + Phase A 159 brand questions x S0 x run 1)
    = 909 calls; blocks B-S0 run 1, run 2, run 3, A-S0 run 1. Probe counts are derived from
    registries/industries_v0_44.csv (6 Phase B questions per industry + one Phase A question per unit), so a
    pre-lock change of the industry list (section 3.4: dropping pharmacies) needs no code change;
  - projection pause (section 4.5 iii): after block 1, projected total = spend x R, R = central estimate of the
    design / central estimate of block 1, read from prereg/cost_estimate_v0_44.json; if it exceeds $80 collection
    pauses; the pre-registrant either continues (--approve-projection) or drops Phase B run 3 (--drop-run-3);
  - collection guards (section 4.6): --collect refuses unless osf/v44/anchor/osf_anchor_v0_44.json exists and names
    the commit of tag v0.44-prereg-r1 on origin, the time is inside the collection window (2026-11-24 to 2026-11-28
    US Central, or a window declared in a DEVIATIONS entry before the first call) and no other paid collection is
    running on this machine; no request is sent more than 72 hours after the first recorded call;
  - no feasibility mode (none is planned for v0.44; the N3 IDs were served correctly in v0.42's check).

Temperature, top_p, top_k and reasoning effort are never sent (provider defaults); max output 16,384 tokens.

Output (append-only, one JSON line per attempt, resumable): osf/v44/data/v44_raw.jsonl
Budget state (approvals): osf/v44/data/v44_budget_state.json

Modes (default: --dry-run):
  --dry-run   build the call matrix, print it with the cost estimate and the state of every guard; send nothing
  --collect   guarded paid collection (see above). Approvals: --approve-past-80 NOTE, --approve-projection NOTE,
              --drop-run-3 NOTE; declared window: --window START END --deviation-entry N (dates YYYY-MM-DD, Central)

Paths: ROOT = AIAS_ROOT or the worktree that contains this file (never a hard-coded /Users/pablou/aias).
"""
import argparse
import csv
import inspect
import json
import os
import re
import subprocess
import sys
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(os.environ.get("AIAS_ROOT", str(Path(__file__).resolve().parents[3])))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import budget_v0_44 as BG  # noqa: E402

V44 = ROOT / "osf" / "v44"
PROBES_PATH = V44 / "prereg" / "probes_v0_44.jsonl"
INDUSTRIES_PATH = V44 / "registries" / "industries_v0_44.csv"
COST_PATH = V44 / "prereg" / "cost_estimate_v0_44.json"
RAW_PATH = V44 / "data" / "v44_raw.jsonl"
STATE_PATH = V44 / "data" / "v44_budget_state.json"
ANCHOR_PATH = V44 / "anchor" / "osf_anchor_v0_44.json"
DEVIATIONS_PATH = V44 / "DEVIATIONS.md"
PREREG_TAG = "v0.44-prereg-r1"

PANEL = [
    {"model_id": "claude-fable-5-2", "provider": "anthropic", "mode": "batch"},
    {"model_id": "gpt-6-astra", "provider": "openai", "mode": "standard"},
    {"model_id": "gemini-4-argon", "provider": "google", "mode": "standard"},
]
CONDITIONS = ["S0"]
RUNS = [1, 2, 3]
# (phase, condition, run) blocks in collection order
BLOCKS = [("B", "S0", 1), ("B", "S0", 2), ("B", "S0", 3), ("A", "S0", 1)]
PROJECTION_BLOCK = ("B", "S0", 1)
DROPPABLE_BLOCK = ("B", "S0", 3)
WINDOW_DATES = ("2026-11-24", "2026-11-28")      # inclusive, US Central (section 4.6)
CENTRAL = ZoneInfo("America/Chicago")
MAX_SPAN_HOURS = 72
ADOPTED_DESIGN = "adopted"                       # key in cost_estimate_v0_44.json
# ---- copied byte for byte from osf/v42/scripts/acquire_v0_42.py (constants) ----
# S1 tool configurations (pre-registration section 4.3).
S1_ANTHROPIC = {"type": "web_search_20250305", "name": "web_search", "max_uses": 5,
                "user_location": {"type": "approximate", "country": "US"}}
S1_OPENAI = {"type": "web_search", "search_context_size": "medium",
             "user_location": {"type": "approximate", "country": "US"}}
S1_OPENAI_INCLUDE = ["web_search_call.action.sources"]

CURRENT_MAX_TOKENS = 16384
PAUSE = {"anthropic": 2.0, "openai": 1.0, "google": 1.0}
MAX_ATTEMPTS = 3

# ---- copied byte for byte from osf/v42/scripts/acquire_v0_42.py (Transient .. _call_with_retry) ----

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
# ---- end of copied block ----



# ======================= v0.44 wrapper (forked from v0.42 r2) =======================

CURRENT_DISPATCH = {"anthropic": call_anthropic_current, "openai": call_openai_current, "google": call_google_current}
BATCH_POLL_SECONDS = 60
EMPTY_RESENDS = 1          # an empty answer is re-sent once
DEADLINE_UTC = None        # set by collect(): no request is sent at or after this time (window end / 72 h)


def load_industries(path=None):
    return list(csv.DictReader(open(path or INDUSTRIES_PATH, encoding="utf-8")))


def expected_counts(industries=None):
    """(Phase B probes, Phase A probes) implied by the industry list: 6 per industry, one per unit."""
    inds = industries if industries is not None else load_industries()
    return 6 * len(inds), sum(int(i["units"]) for i in inds)


def load_probes(path=None):
    probes = [json.loads(l) for l in Path(path or PROBES_PATH).read_text(encoding="utf-8").splitlines() if l.strip()]
    nb, na = expected_counts()
    got = (sum(p["phase"] == "B" for p in probes), sum(p["phase"] == "A" for p in probes))
    if got != (nb, na):
        sys.exit(f"ABORT: probe file has Phase B/A = {got}, the industry list implies {(nb, na)}")
    return probes


def blocks_in_design(drop_run3=False):
    return [b for b in BLOCKS if not (drop_run3 and b == DROPPABLE_BLOCK)]


def expected_total(probes=None, drop_run3=False):
    probes = probes if probes is not None else load_probes()
    nb = sum(p["phase"] == "B" for p in probes)
    na = sum(p["phase"] == "A" for p in probes)
    return len(PANEL) * sum(nb if ph == "B" else na for ph, _c, _r in blocks_in_design(drop_run3))


def call_id(industry, phase, probe_id, model, cond, run):
    return f"{industry}|{phase}|{probe_id}|{model}|{cond}|{run}"


def build_specs(probes, drop_run3=False):
    """Matrix in collection order: block (BLOCKS order), then model (panel order), then probe (file order)."""
    specs = []
    for bi, (phase, cond, run) in enumerate(BLOCKS):
        if drop_run3 and (phase, cond, run) == DROPPABLE_BLOCK:
            continue
        for m in PANEL:
            for p in probes:
                if p["phase"] != phase:
                    continue
                specs.append({
                    "call_id": call_id(p["substrate"], p["phase"], p["probe_id"], m["model_id"], cond, run),
                    "substrate": p["substrate"], "phase": p["phase"], "probe_id": p["probe_id"],
                    "brand_id": p.get("brand_id"), "frame_id": p.get("frame_id"),
                    "model": m, "condition": cond, "run": run, "block": bi,
                    "system": p.get("system"), "prompt": p["prompt"],
                })
    ids = [s["call_id"] for s in specs]
    if len(set(ids)) != len(ids):
        sys.exit("ABORT: duplicate call_id")
    return specs


def _invoke(model, cond, prompt, system):
    return _call_with_retry(CURRENT_DISPATCH[model["provider"]], model["model_id"], prompt, cond == "S1", system)


def _part(out, mode, cond):
    """Usage of one billed request, for budget_v0_44.record_cost."""
    s = out.get("search") or {}
    return {"mode": mode, "input_tokens": out.get("tokens_in"), "output_tokens": out.get("tokens_out"),
            "thinking_tokens": out.get("tokens_thought"), "n_searches": (s.get("n_searches") or 0) if cond == "S1" else 0}


def _record(spec, out, status, err, attempts, empty_retry, ts_start, ts_end, parts, extra=None):
    out = out or {}
    model, cond = spec["model"], spec["condition"]
    rec = {
        "call_id": spec["call_id"], "substrate": spec["substrate"], "phase": spec["phase"],
        "probe_id": spec["probe_id"], "brand_id": spec["brand_id"], "frame_id": spec["frame_id"],
        "model_requested": model["model_id"], "provider": model["provider"],
        "served_model": out.get("served_model"), "condition": cond, "run": spec["run"],
        "system": spec["system"], "prompt": spec["prompt"],
        "text": out.get("text", ""), "status": status, "error": err,
        "finish_reason": out.get("finish_reason"),
        "input_tokens": out.get("tokens_in"), "output_tokens": out.get("tokens_out"),
        "thinking_tokens": out.get("tokens_thought"),
        "search": out.get("search") if cond == "S1" else None,
        "paused_continued": out.get("paused_continued", False),
        "attempts": attempts, "empty_retry": empty_retry,
        "started_utc": ts_start, "finished_utc": ts_end,
        "mode": model.get("mode", "standard"), "usage_parts": parts,
    }
    rec.update(extra or {})
    rec["cost_usd"] = BG.record_cost(rec)
    return rec


def past_deadline(now=None):
    if DEADLINE_UTC is None:
        return False
    return (now or datetime.now(timezone.utc)) >= DEADLINE_UTC


def send_call(spec):
    """Synchronous call (GPT-6 Astra, Gemini 4 Argon) with the usage of every billed request in `usage_parts`."""
    model, cond = spec["model"], spec["condition"]
    ts_start = _now()
    out, attempts, err = _invoke(model, cond, spec["prompt"], spec["system"])
    parts = [_part(out, "standard", cond)] if out is not None else []
    empty_retry = False
    if out is not None and not out["text"].strip():
        empty_retry = True
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
    return _record(spec, out, status, err, attempts, empty_retry, ts_start, ts_end, parts)


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
    """Text (and, inert in S0, the search record) from Anthropic content blocks: call_anthropic_current's parsing."""
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


def _batch_message_out(spec, m):
    """A succeeded batch message -> (call-function output, usage parts). S0 only: no tool, so no pause_turn
    continuation is possible; a pause_turn stop reason would be recorded as the finish reason."""
    blocks = list(m.content)
    parts = [{"mode": "batch", "input_tokens": m.usage.input_tokens, "output_tokens": m.usage.output_tokens,
              "thinking_tokens": None, "n_searches": 0}]
    text, srec = parse_anthropic_blocks(blocks, spec["condition"] == "S1")
    out = {"text": text, "served_model": m.model, "finish_reason": m.stop_reason,
           "tokens_in": m.usage.input_tokens, "tokens_out": m.usage.output_tokens,
           "tokens_thought": None, "paused_continued": False, "search": srec}
    return out, parts


TRANSIENT_BATCH_ERRORS = ("api_error", "overloaded_error", "rate_limit_error", "timeout_error")


def run_anthropic_batch(specs, ledger, write, client=None, poll=None, sleep=time.sleep):
    """Send `specs` (one model, one block) through the Message Batches API under the budget guard.
    Each attempt is one raw line. Transient errors and expired requests are re-sent up to MAX_ATTEMPTS attempts;
    an empty answer is re-sent once. Returns 'done' | 'pause' | 'stop'."""
    if client is None:
        import anthropic
        client = anthropic.Anthropic()
    poll = BATCH_POLL_SECONDS if poll is None else poll
    pending = [(s, 1, 0) for s in specs]          # (spec, attempt number, empty re-sends so far)
    while pending:
        if past_deadline():
            ledger.halt("stop", f"deadline {DEADLINE_UTC.isoformat()} reached")
            return "stop"
        model_id, cond = pending[0][0]["model"]["model_id"], pending[0][0]["condition"]
        st, k, tok = ledger.fit(BG.worst_case(model_id, cond, "batch"), len(pending))
        if st == "wait":
            sleep(5)
            continue
        if st != "ok":
            return st
        chunk, pending = pending[:k], pending[k:]
        ids = {f"v44-{i:04d}-a{att}": (s, att, ne) for i, (s, att, ne) in enumerate(chunk)}
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
        while True:
            b = client.messages.batches.retrieve(b.id)
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
                out, parts = _batch_message_out(s, res.message)
                empty = not out["text"].strip()
                rec = _record(s, out, "empty" if empty else "ok", None, att, ne > 0, ts_start, ts_end, parts, extra)
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
        ledger.settle(tok, spent)
        pending = retry + pending
    return "done"


def run_sync(specs, ledger, write, sender=None, sleep=time.sleep):
    """Send `specs` (one model, one block) one at a time under the budget guard. Returns 'done' | 'pause' | 'stop'."""
    sender = sender or send_call
    for s in specs:
        if past_deadline():
            ledger.halt("stop", f"deadline {DEADLINE_UTC.isoformat()} reached")
            return "stop"
        while True:
            st, tok = ledger.reserve(BG.worst_case(s["model"]["model_id"], s["condition"], "standard"))
            if st != "wait":
                break
            sleep(5)
        if st != "ok":
            return st
        rec = sender(s)
        write(rec)
        ledger.settle(tok, rec["cost_usd"])
    return "done"


def require_keys():
    if not os.environ.get("GOOGLE_API_KEY") and os.environ.get("GEMINI_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]  # call_google_current reads GOOGLE_API_KEY
    missing = [v for v in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY") if not os.environ.get(v)]
    if missing:
        sys.exit(f"ERROR: missing environment variables: {', '.join(missing)}")


def confirm_no_sampling_params():
    """claude-fable-5-2 must not get temperature/top_p/top_k: check the copied function and the batch builder."""
    src = inspect.getsource(call_anthropic_current) + inspect.getsource(anthropic_params)
    return [w for w in ("temperature", "top_p", "top_k") if w in src]


# ----------------------------------------------------------------- cost file
def cost_estimate(path=None):
    """The locked cost estimate (cost_estimate_v0_44.py output)."""
    return json.loads(Path(path or COST_PATH).read_text(encoding="utf-8"))


def projection_ratio(path=None, when_utc=None):
    """R = central estimate of the adopted design / central estimate of block 1, at the prices of the day block 1
    started (December ratio from 2026-12-01, when Gemini 4 Argon's price doubles)."""
    ce = cost_estimate(path)
    day = (when_utc.isoformat() if hasattr(when_utc, "isoformat") else (when_utc or ""))[:10]
    key = "ratio_design_to_block1_central_december" if day >= "2026-12-01" else "ratio_design_to_block1_central"
    return float(ce["projection"][key])


# ----------------------------------------------------------------- guards
def window_bounds(dates=WINDOW_DATES):
    """(start, end) in UTC of an inclusive range of US Central dates."""
    a = datetime.fromisoformat(dates[0]).replace(tzinfo=CENTRAL)
    b = datetime.fromisoformat(dates[1]).replace(tzinfo=CENTRAL) + timedelta(days=1)
    return a.astimezone(timezone.utc), b.astimezone(timezone.utc)


def declared_window(start, end, entry, deviations_path=None):
    """A collection window declared in a DEVIATIONS entry (written before the first call). The entry heading must
    start with '## Entry <entry>' and the entry must name both dates. Returns (start, end) dates."""
    text = Path(deviations_path or DEVIATIONS_PATH).read_text(encoding="utf-8")
    parts = re.split(r"(?m)^## ", text)
    body = next((p for p in parts if re.match(rf"Entry {re.escape(str(entry))}\b", p)), None)
    if body is None:
        sys.exit(f"REFUSED: DEVIATIONS.md has no '## Entry {entry}'")
    if start not in body or end not in body:
        sys.exit(f"REFUSED: DEVIATIONS Entry {entry} does not name both window dates {start} and {end}")
    if datetime.fromisoformat(end) < datetime.fromisoformat(start):
        sys.exit("REFUSED: window end before start")
    return start, end


def first_call_utc(raw_path=None):
    raw_path = RAW_PATH if raw_path is None else Path(raw_path)
    first = None
    if raw_path.exists():
        for line in raw_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    t = json.loads(line).get("started_utc")
                except json.JSONDecodeError:
                    continue
                if t and (first is None or t < first):
                    first = t
    return datetime.fromisoformat(first) if first else None


def deadline(dates=WINDOW_DATES, raw_path=None):
    """No request at or after min(window end, first recorded call + 72 h)."""
    _, end = window_bounds(dates)
    f = first_call_utc(raw_path)
    return min(end, f + timedelta(hours=MAX_SPAN_HOURS)) if f else end


def window_check(now=None, dates=WINDOW_DATES, raw_path=None):
    """-> (ok, reason)."""
    now = now or datetime.now(timezone.utc)
    start, _end = window_bounds(dates)
    dl = deadline(dates, raw_path)
    if now < start:
        return False, f"before the collection window ({dates[0]} US Central)"
    if now >= dl:
        return False, f"at or after the deadline {dl.isoformat()} (window end or first call + {MAX_SPAN_HOURS} h)"
    return True, f"inside the window {dates[0]}..{dates[1]} US Central; deadline {dl.isoformat()}"


ACQ_RE = re.compile(r"(acquire|acquisition)[\w.-]*\.py")


def _ps():
    """`ps -axo pid=,ppid=,command=` (separate function: tests patch it)."""
    return subprocess.run(["ps", "-axo", "pid=,ppid=,command="], capture_output=True, text=True, timeout=30).stdout


def other_collections(ps_text=None, me=None):
    """Running processes, other than this one and its ancestors, whose command runs an acquisition script with
    --collect (or a legacy run_acquisition_v*.py runner, which collects by default). -> list of (pid, command)."""
    ps_text = _ps() if ps_text is None else ps_text
    me = os.getpid() if me is None else me
    procs = {}
    for line in ps_text.splitlines():
        f = line.strip().split(None, 2)
        if len(f) == 3 and f[0].isdigit() and f[1].isdigit():
            procs[int(f[0])] = (int(f[1]), f[2])
    anc, p = {me}, me
    while p in procs and procs[p][0] not in anc and procs[p][0] > 1:
        p = procs[p][0]
        anc.add(p)
    hits = []
    for pid, (_pp, cmd) in procs.items():
        if pid in anc or not ACQ_RE.search(cmd):
            continue
        if "--collect" in cmd or re.search(r"run_acquisition_v\d+\.py", cmd):
            if "--dry-run" in cmd and "--collect" not in cmd:
                continue
            hits.append((pid, cmd))
    return hits


def record_window(dates, deviation_entry=None, state_path=None):
    """Write the collection window used into the budget state file (read by the scorer's MC_Window)."""
    p = Path(state_path or STATE_PATH)
    try:
        st = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    except json.JSONDecodeError:
        st = {}
    st["window"] = list(dates)
    st["window_deviation_entry"] = deviation_entry
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(st, indent=2), encoding="utf-8")
    return st


def prereg_guard():
    """Refuse unless the anchor file exists, the prereg tag is on origin and the anchor names its commit."""
    if not ANCHOR_PATH.exists():
        sys.exit(f"REFUSED: anchor file missing: {ANCHOR_PATH}")
    r = subprocess.run(["git", "ls-remote", "--tags", "origin", PREREG_TAG], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"REFUSED: git ls-remote failed: {r.stderr.strip()}")
    shas = {}
    for line in r.stdout.splitlines():
        sha, ref = line.split("\t")
        shas[ref] = sha
    tag_ref = f"refs/tags/{PREREG_TAG}"
    if tag_ref not in shas:
        sys.exit(f"REFUSED: tag {PREREG_TAG} not found on origin")
    commit = shas.get(tag_ref + "^{}", shas[tag_ref])  # peeled commit for annotated tags
    text = ANCHOR_PATH.read_text(encoding="utf-8")
    if commit not in text and shas[tag_ref] not in text:
        sys.exit(f"REFUSED: {ANCHOR_PATH.name} does not name the commit of {PREREG_TAG} ({commit})")
    return commit


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


def run_collection(specs, ledger, raw_path, runners, ratio, log=print):
    """Blocks in order; within a block one worker per model in parallel (runners[mode](specs, ledger, write)).
    After the projection block, pause if spend x ratio > $80 (unless the projection was approved or run 3 dropped).
    Returns 'done' | 'pause' | 'stop'."""
    done = done_ids(raw_path)
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    lock = threading.Lock()

    def write(rec):
        with lock:
            with open(raw_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
                os.fsync(f.fileno())
        log(f"  {rec['call_id']} {rec['status']} out={rec.get('output_tokens')} fr={rec.get('finish_reason')} "
            f"${rec['cost_usd']:.4f}")

    for bi, block in enumerate(BLOCKS):
        todo = [s for s in specs if s["block"] == bi and s["call_id"] not in done]
        if todo:
            log(f"block {bi + 1} {block}: {len(todo)} calls to send; {ledger.summary()}")
            groups = [[s for s in todo if s["model"]["model_id"] == m["model_id"]] for m in PANEL]
            groups = [(g, runners[g[0]["model"]["mode"]]) for g in groups if g]
            with ThreadPoolExecutor(max_workers=len(groups)) as pool:
                res = list(pool.map(lambda gr: gr[1](gr[0], ledger, write), groups))
            for st in ("stop", "pause"):
                if st in res:
                    log(f"HALT ({st}) in block {bi + 1}: {ledger.summary()}")
                    return st
        if block == PROJECTION_BLOCK and not (ledger.approved("projection") or ledger.approved("drop_run3")):
            proj = ledger.spent() * ratio
            if any(s["block"] > bi and s["call_id"] not in done for s in specs) and proj > ledger.pause_at:
                ledger.halt("pause", f"projection: spend ${ledger.spent():.2f} x {ratio:.4f} = ${proj:.2f} "
                                     f"> ${ledger.pause_at:.0f}")
                log(f"PAUSE (projection) after block {bi + 1}: {ledger.summary()}")
                return "pause"
    return "done"


# ----------------------------------------------------------------- dry run
def dry_run(out=print):
    probes = load_probes()
    specs = build_specs(probes)
    total = expected_total(probes)
    bad = confirm_no_sampling_params()
    out(f"AIAS v0.44 acquisition: DRY RUN (nothing is sent). ROOT = {ROOT}")
    out(f"sampling params in call_anthropic_current / anthropic_params: {bad or 'none (temperature/top_p/top_k not sent)'}")
    out(f"max output tokens per request: {CURRENT_MAX_TOKENS}")
    out(f"{'block':24s} " + " ".join(f"{m['model_id']:>17s}" for m in PANEL) + "  total")
    for bi, (ph, cond, run) in enumerate(BLOCKS):
        row = [sum(1 for s in specs if s["block"] == bi and s["model"]["model_id"] == m["model_id"]) for m in PANEL]
        out(f"{bi + 1}. Phase {ph} {cond} run {run}        " + " ".join(f"{x:17d}" for x in row) + f"  {sum(row):5d}")
    out(f"TOTAL calls: {len(specs)} (expected {total}) -> {'OK' if len(specs) == total else 'MISMATCH'}")
    out("by model: " + json.dumps({m["model_id"]: sum(1 for s in specs if s["model"]["model_id"] == m["model_id"])
                                   for m in PANEL}) + "  modes: " + json.dumps({m["model_id"]: m["mode"] for m in PANEL}))
    inds = [i["industry"] for i in load_industries()]
    out("by industry (all models): " + json.dumps({i: sum(1 for s in specs if s["substrate"] == i) for i in inds}))
    out(f"without Phase B run 3 (projection fallback): {expected_total(probes, drop_run3=True)} calls")
    out("worst-case reservation per request (USD; 2,000 input tokens, output at the cap):")
    for m in PANEL:
        out(f"  {m['model_id']:17s} {m['mode']:8s} S0 {BG.worst_case(m['model_id'], 'S0', m['mode'], '2026-11-24'):.4f}"
            f" (Nov)  {BG.worst_case(m['model_id'], 'S0', m['mode'], '2026-12-01'):.4f} (Dec)")
    out(f"budget: pause at ${BG.PAUSE_AT_USD:.0f}, hard stop at ${BG.BUDGET_CAP_USD:.0f}; judge reserve "
        f"${BG.JUDGE_RESERVE_USD:.2f}")
    try:
        ce = cost_estimate()
        for k in ("adopted", "adopted_december"):
            d = ce["designs"][k]
            out(f"cost estimate [{k}]: {d['calls']} calls, central ${d['central']:.2f}, high ${d['high']:.2f}")
        out(f"projection pause after block 1: spend x {projection_ratio():.4f} > ${BG.PAUSE_AT_USD:.0f}")
    except Exception as e:
        out(f"cost estimate unavailable: {type(e).__name__}: {e}")
    ok, why = window_check()
    out(f"guard (state now, informational): anchor file {'present' if ANCHOR_PATH.exists() else 'MISSING'}; "
        f"window: {why}; other collections running: {len(other_collections())}")
    out("nothing sent.")
    return 0 if len(specs) == total else 1


# ----------------------------------------------------------------- collect
def collect(approve_past_80=None, approve_projection=None, drop_run3=None, window=None, deviation_entry=None):
    global DEADLINE_UTC
    commit = prereg_guard()
    print(f"prereg guard passed: {PREREG_TAG} -> {commit}; anchor {ANCHOR_PATH}")
    dates = WINDOW_DATES
    if window:
        if deviation_entry is None:
            sys.exit("REFUSED: --window needs --deviation-entry")
        dates = declared_window(window[0], window[1], deviation_entry)
    ok, why = window_check(dates=dates)
    if not ok:
        sys.exit(f"REFUSED: {why}")
    others = other_collections()
    if others:
        sys.exit("REFUSED: another paid collection is running: " + "; ".join(f"{p} {c[:120]}" for p, c in others))
    DEADLINE_UTC = deadline(dates)
    print(f"window ok: {why}")
    require_keys()
    ledger = BG.Ledger(RAW_PATH, STATE_PATH)
    if approve_past_80:
        ledger.approve("past_80", approve_past_80)
    if approve_projection:
        ledger.approve("projection", approve_projection)
    if drop_run3:
        ledger.approve("drop_run3", drop_run3)
    record_window(dates, deviation_entry)
    specs = build_specs(load_probes(), drop_run3=ledger.approved("drop_run3"))
    print(f"{len(specs)} specs, {len(done_ids())} already done; budget {ledger.summary()}")
    st = run_collection(specs, ledger, RAW_PATH, {"batch": run_anthropic_batch, "standard": run_sync},
                        projection_ratio(when_utc=first_call_utc() or datetime.now(timezone.utc)))
    print("result:", st, ledger.summary())
    return {"done": 0, "pause": 5, "stop": 6}[st]


def main(argv=None):
    ap = argparse.ArgumentParser(description="AIAS v0.44 acquisition (pre-registration draft r1); default --dry-run")
    ap.add_argument("--dry-run", action="store_true", help="the default: print the matrix and guards, send nothing")
    ap.add_argument("--collect", action="store_true", help="guarded paid collection")
    ap.add_argument("--approve-past-80", metavar="NOTE", default=None)
    ap.add_argument("--approve-projection", metavar="NOTE", default=None)
    ap.add_argument("--drop-run-3", metavar="NOTE", default=None)
    ap.add_argument("--window", nargs=2, metavar=("START", "END"), default=None)
    ap.add_argument("--deviation-entry", default=None)
    a = ap.parse_args(argv)
    if a.dry_run and a.collect:
        ap.error("choose one of --dry-run / --collect")
    if not a.collect:
        if any([a.approve_past_80, a.approve_projection, a.drop_run_3, a.window]):
            ap.error("approvals and --window apply to --collect only")
        return dry_run()
    return collect(a.approve_past_80, a.approve_projection, a.drop_run_3, a.window, a.deviation_entry)


if __name__ == "__main__":
    sys.exit(main())
