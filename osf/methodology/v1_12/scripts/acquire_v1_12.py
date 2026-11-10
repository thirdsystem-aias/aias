#!/usr/bin/env python3
"""
AIAS v1.12 -- Coverage Paper A acquisition (CEP probes on the newest-model panel, search off).

FORK of osf/v42/scripts/acquire_v0_42.py (branch v0.42, git blob c40bb5f2194a499859bfd8b7dcf474e576b34699). Copied
byte for byte from that file: the S1 tool constants, CURRENT_MAX_TOKENS, PAUSE and MAX_ATTEMPTS, and Transient,
_empty_search, _dump, the three current-arm call functions, _now and _call_with_retry (themselves verbatim from
v0.39). S1 is never used here: every call is sent with search=False. New: the probe file and design (4 models x 75
probes x 3 runs = 900 calls, S0), the call record (PRE_REGISTRATION_v1_12.md section 6.5), the cost guard (section
6.6), the collection windows (section 6.7), the re-run cap and the prereg guard.

Decoding (section 6.4, as t4 = v0.42 section 4.4): temperature, top_p, top_k and reasoning effort are never sent
(provider defaults; Claude Fable 5.2's adaptive thinking is always on, default effort high); maximum output 16,384
tokens; no system prompt; no tools. Every record carries the settings sent (MC_Settings).

Cost guard (section 6.6): before every request it adds that request's worst case (200 input and 16,384 output
tokens at list price) to the spend so far plus the requests in flight, and does not send the request if the sum
passes US$100 (hard cap: programme rule of 2026-11-10, "at most $100 of paid model calls per paper"; the draft's
$120 is superseded). Once the recorded spend reaches US$80 nothing more is sent until Pablo approves; the run is resumed
with --approve-past-80 "<who, when>", which is logged. Spend = recorded tokens at list price (Gemini thinking tokens
billed as output); a request that ends in a client-side timeout is counted at its worst case. Gemini 4 Argon is
priced at $2/$10 per million tokens through 2026-11-30 and $4/$20 from 2026-12-01. Unsent calls are missing cells.

Modes:
  --dry-run   build and check the 900 call specs, the probe file, the decoding settings and the cost guard; no
              network call and no provider SDK import; writes prereg/dry_run_acquire_v1_12.txt
  --collect   refused unless tag v1.12-prereg-r1 is on origin and osf/methodology/v1_12/anchor/osf_anchor_v1_12.json
              names its commit; refused until t4 (v0.42) is complete: anchor/t4_complete_v1_12.json records t4's raw
              file, its SHA-256 and its last call, the file still has that SHA-256 (t4 wrote nothing since) and no
              t4 call finished after the recorded last call, which is in the past; refused while another paid
              collection (any acquire_v*.py --collect) runs on this machine; sends only inside a collection window
              (2026-11-14 00:00 to 11-16 23:59 UTC, else 11-22 12:00 to 11-29 23:59 UTC; never 11-17 to 11-21,
              v0.40), checked again before every request; resumable (answered calls are skipped; a call is sent in
              at most two passes: the main pass and one re-run pass)
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
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.environ.get("AIAS_ROOT", str(Path(__file__).resolve().parents[4])))
V112 = ROOT / "osf" / "methodology" / "v1_12"
PROBES_PATH = V112 / "prereg" / "probes_v1_12.jsonl"
RAW_PATH = V112 / "data" / "v112_raw.jsonl"
GUARD_LOG = V112 / "data" / "v112_guard_log.jsonl"
ANCHOR_PATH = V112 / "anchor" / "osf_anchor_v1_12.json"
DRY_RUN_PATH = V112 / "prereg" / "dry_run_acquire_v1_12.txt"
T4_RECORD = V112 / "anchor" / "t4_complete_v1_12.json"       # section 6.7: written after t4's last call
PAID_COLLECTION = re.compile(r"acquire_v[0-9][0-9_.]*\.py\b.*--collect")
PREREG_TAG = "v1.12-prereg-r1"

PANEL = [
    {"model_id": "claude-fable-5-2", "provider": "anthropic"},
    {"model_id": "claude-opus-5-5", "provider": "anthropic"},
    {"model_id": "gpt-6-astra", "provider": "openai"},
    {"model_id": "gemini-4-argon", "provider": "google"},
]
RUNS = [1, 2, 3]
N_PROBES, EXPECTED_TOTAL, MAX_PASSES = 75, 900, 2
SETTINGS = {"temperature": "provider default (not sent)", "top_p": "provider default (not sent)",
            "top_k": "provider default (not sent)", "reasoning_effort": "provider default (not sent)",
            "max_output_tokens": 16384, "system_prompt": None, "tools": None, "condition": "S0"}
SENT_PARAM_WORDS = ("temperature", "top_p", "top_k", "reasoning_effort", "\"reasoning\"", "effort",
                    "thinking_config", "thinking_budget")
CAP_USD, PAUSE_USD = 100.0, 80.0                            # section 6.6 ($100 rule of 2026-11-10)
IN_WORST, OUT_WORST = 200, 16384
PRICES = {"claude-fable-5-2": (8.0, 40.0), "claude-opus-5-5": (4.0, 20.0), "gpt-6-astra": (10.0, 50.0),
          "gemini-4-argon": (2.0, 10.0)}                       # US$ per 1M tokens in / out (vendor pages, Nov 10)
PRICES_FROM_DEC1 = {"gemini-4-argon": (4.0, 20.0)}
PRICE_CHANGE_UTC = datetime(2026, 12, 1, tzinfo=timezone.utc)
WINDOWS = [(datetime(2026, 11, 14, 0, 0, 0, tzinfo=timezone.utc), datetime(2026, 11, 16, 23, 59, 59, tzinfo=timezone.utc)),
           (datetime(2026, 11, 22, 12, 0, 0, tzinfo=timezone.utc), datetime(2026, 11, 29, 23, 59, 59, tzinfo=timezone.utc))]

# ----- copied byte for byte from acquire_v0_42.py (blob c40bb5f2): S1 constants, CURRENT_MAX_TOKENS, PAUSE, MAX_ATTEMPTS
# S1 tool configurations (pre-registration section 4.3).
S1_ANTHROPIC = {"type": "web_search_20250305", "name": "web_search", "max_uses": 5,
                "user_location": {"type": "approximate", "country": "US"}}
S1_OPENAI = {"type": "web_search", "search_context_size": "medium",
             "user_location": {"type": "approximate", "country": "US"}}
S1_OPENAI_INCLUDE = ["web_search_call.action.sources"]

CURRENT_MAX_TOKENS = 16384
PAUSE = {"anthropic": 2.0, "openai": 1.0, "google": 1.0}
MAX_ATTEMPTS = 3

# ----- copied byte for byte from acquire_v0_42.py (blob c40bb5f2): Transient, _empty_search, _dump, call functions, _now, _call_with_retry


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




# ----- end of the copied block


# ======================= v1.12 wrapper (new) =======================

CURRENT_DISPATCH = {"anthropic": call_anthropic_current, "openai": call_openai_current, "google": call_google_current}


class GuardStop(BaseException):
    """Stops sending. A BaseException, so the copied _call_with_retry (which catches Exception) never turns it into an
    error record: a call stopped before any request is unsent (missing cell) and is not written."""


def price(model_id, when):
    if when >= PRICE_CHANGE_UTC and model_id in PRICES_FROM_DEC1:
        return PRICES_FROM_DEC1[model_id]
    return PRICES[model_id]


def usd(model_id, provider, when, tin, tout, tthought):
    """List-price cost of one request; Google thinking tokens are billed as output (its candidate count excludes them),
    the other providers' output counts already include thinking."""
    pin, pout = price(model_id, when)
    out = (tout or 0) + ((tthought or 0) if provider == "google" else 0)
    return ((tin or 0) * pin + out * pout) / 1e6


def worst_usd(model_id, when):
    pin, pout = price(model_id, when)
    return (IN_WORST * pin + OUT_WORST * pout) / 1e6


def in_window(when):
    return any(a <= when <= b for a, b in WINDOWS)


def _utcnow():
    """The clock of every window and guard check (one function, so the tests can set it)."""
    return datetime.now(timezone.utc)


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def t4_guard(now):
    """Section 6.7: v1.12 starts only after t4's last call is logged. Reads anchor/t4_complete_v1_12.json
    {t4_raw_path, t4_raw_sha256, t4_last_call_utc, recorded_by}; refuses unless the t4 raw file still has that
    SHA-256, no t4 record finished after t4_last_call_utc, and t4_last_call_utc is before now."""
    if not T4_RECORD.exists():
        sys.exit(f"REFUSED: {T4_RECORD.name} missing: t4 (v0.42) is not recorded as complete (section 6.7)")
    rec = json.loads(T4_RECORD.read_text(encoding="utf-8"))
    raw = Path(rec.get("t4_raw_path") or "")
    if not raw.is_file():
        sys.exit(f"REFUSED: t4 raw file not found: {raw}")
    if _sha256(raw) != rec.get("t4_raw_sha256"):
        sys.exit("REFUSED: t4 raw file changed since t4 was recorded complete (t4 may still be collecting)")
    last = datetime.fromisoformat(rec["t4_last_call_utc"])
    latest = None
    for line in raw.read_text(encoding="utf-8").splitlines():
        try:
            t = json.loads(line).get("finished_utc")
        except (json.JSONDecodeError, AttributeError):
            continue
        if t:
            t = datetime.fromisoformat(t)
            latest = t if latest is None or t > latest else latest
    if latest is not None and latest > last:
        sys.exit(f"REFUSED: a t4 call finished at {latest.isoformat()}, after the recorded last call {last.isoformat()}")
    if not last < now:
        sys.exit("REFUSED: t4's recorded last call is not in the past")
    return rec


def running_commands():
    r = subprocess.run(["ps", "-axo", "pid=,command="], capture_output=True, text=True)
    out = []
    for line in r.stdout.splitlines():
        pid, _, cmd = line.strip().partition(" ")
        if pid.isdigit():
            out.append((int(pid), cmd))
    return out


def other_collection_guard(commands=None):
    """Section 6.7: one paid collection on the Mac at a time (any acquire_v*.py --collect but this process)."""
    me = {os.getpid(), os.getppid()}
    others = [(pid, cmd) for pid, cmd in (running_commands() if commands is None else commands)
              if pid not in me and PAID_COLLECTION.search(cmd)]
    if others:
        sys.exit("REFUSED: another paid collection is running: " + "; ".join(f"{p} {c[:120]}" for p, c in others))


class Guard:
    """Section 6.6 cost guard and section 6.7 windows, checked before every request."""

    def __init__(self, spent=0.0, approved=None):
        self.spent, self.reserved, self.approved, self.stopped = float(spent), 0.0, approved, None
        self.lock = threading.Lock()

    def reserve(self, model_id, when):
        with self.lock:
            if self.stopped:
                raise GuardStop(self.stopped)
            if not in_window(when):
                self.stopped = f"outside the collection windows at {when.isoformat()}"
            elif self.spent >= PAUSE_USD and not self.approved:
                self.stopped = (f"PAUSED: recorded spend ${self.spent:.2f} reached ${PAUSE_USD:.0f}; ask Pablo, then "
                                f"resume with --approve-past-80")
            elif self.spent + self.reserved + worst_usd(model_id, when) > CAP_USD:
                self.stopped = (f"CAP: ${self.spent:.2f} spent + ${self.reserved:.2f} in flight + "
                                f"${worst_usd(model_id, when):.2f} worst case would pass ${CAP_USD:.0f}")
            if self.stopped:
                raise GuardStop(self.stopped)
            w = worst_usd(model_id, when)
            self.reserved += w
            return w

    def settle(self, reserved, actual):
        with self.lock:
            self.reserved -= reserved
            self.spent += actual


GUARD = Guard()
_LOCAL = threading.local()


def _guarded(provider):
    fn = CURRENT_DISPATCH[provider]

    def request(model_id, prompt, search, system=None):
        when = _utcnow()
        w = GUARD.reserve(model_id, when)
        try:
            out = fn(model_id, prompt, search, system)
        except Exception as e:
            timeout = "timeout" in (type(e).__name__ + type(e.__cause__).__name__ + str(e)).lower()
            cost = w if timeout else 0.0
            _LOCAL.billed.append({"utc": when.isoformat(), "input_tokens": None, "output_tokens": None,
                                  "thinking_tokens": None, "usd": cost, "estimated": timeout,
                                  "error": type(e).__name__})
            GUARD.settle(w, cost)
            raise
        cost = usd(model_id, provider, when, out.get("tokens_in"), out.get("tokens_out"), out.get("tokens_thought"))
        _LOCAL.billed.append({"utc": when.isoformat(), "input_tokens": out.get("tokens_in"),
                              "output_tokens": out.get("tokens_out"), "thinking_tokens": out.get("tokens_thought"),
                              "usd": cost, "estimated": False, "error": None})
        GUARD.settle(w, cost)
        return out
    return request


def load_probes():
    raw = PROBES_PATH.read_bytes()
    probes = [json.loads(line) for line in raw.decode("utf-8").splitlines() if line.strip()]
    ids = [p["probe_id"] for p in probes]
    if len(probes) != N_PROBES or len(set(ids)) != N_PROBES:
        sys.exit(f"ABORT: expected {N_PROBES} unique probes, found {len(probes)} ({len(set(ids))} unique)")
    return probes, hashlib.sha256(raw).hexdigest()


def call_id(p, model_id, run):
    return f"{p['substrate']}|{p['probe_id']}|{model_id}|S0|{run}"


def build_specs(probes):
    """Order (section 6.5): model (panel order), then run 1, 2, 3, probes in file order."""
    specs = [{"call_id": call_id(p, m["model_id"], run), "probe": p, "model": m, "run": run}
             for m in PANEL for run in RUNS for p in probes]
    if len({s["call_id"] for s in specs}) != len(specs):
        sys.exit("ABORT: duplicate call_id")
    return specs


def served_ok(requested, served):
    """As score_v0_42.served_ok: the requested ID or a dated snapshot of it."""
    s = (served or "").strip().removeprefix("models/")
    return s == requested or re.fullmatch(re.escape(requested) + r"-(\d{4}-\d{2}-\d{2}|\d{8})", s) is not None


def send_call(spec, probes_sha, pass_no):
    """One call (with the copied retry policy and one empty-answer retry). Returns (record or None, guard stop)."""
    model, p = spec["model"], spec["probe"]
    _LOCAL.billed = []
    ts_start = _now()
    out, attempts, err, empty_retry, stop = None, 0, None, False, None

    def invoke():
        return _call_with_retry(_guarded(model["provider"]), model["model_id"], p["prompt"], False, None)
    try:
        out, attempts, err = invoke()
    except GuardStop as e:
        stop = str(e)
    if stop is None and out is not None and not out["text"].strip():
        empty_retry = True
        try:
            out2, a2, err2 = invoke()
            attempts += a2
            if out2 is not None:
                out = out2
            if err2:
                err = err2
        except GuardStop as e:
            stop = str(e)
    if stop is not None and not _LOCAL.billed:
        return None, stop
    ts_end = _now()
    time.sleep(PAUSE[model["provider"]])
    status = "error" if out is None else ("empty" if not out["text"].strip() else "ok")
    out = out or {}
    rec = {
        "phase": "v1.12", "call_id": spec["call_id"], "substrate": p["substrate"], "category": p["category"],
        "probe_id": p["probe_id"], "role": p["role"], "w": p["w"], "half": p["half"],
        "model_requested": model["model_id"], "provider": model["provider"], "served_model": out.get("served_model"),
        "served_ok": served_ok(model["model_id"], out.get("served_model")) if out else False,
        "condition": "S0", "run": spec["run"], "pass": pass_no, "prompt": p["prompt"], "system": None,
        "text": out.get("text", ""), "status": status, "error": err if stop is None else (err or f"guard: {stop}"),
        "finish_reason": out.get("finish_reason"), "input_tokens": out.get("tokens_in"),
        "output_tokens": out.get("tokens_out"), "thinking_tokens": out.get("tokens_thought"),
        "settings": SETTINGS, "attempts": max(attempts, len(_LOCAL.billed)), "empty_retry": empty_retry,
        "paused_continued": out.get("paused_continued", False), "billed_attempts": list(_LOCAL.billed),
        "usd_billed": float(sum(b["usd"] for b in _LOCAL.billed)), "guard_stop": stop,
        "probes_sha256": probes_sha, "started_utc": ts_start, "finished_utc": ts_end}
    return rec, stop


def read_raw():
    recs = []
    if RAW_PATH.exists():
        for line in RAW_PATH.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    recs.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return recs


def answered(r):
    return (r.get("status") == "ok" and bool((r.get("text") or "").strip()) and not r.get("error")
            and served_ok(r.get("model_requested"), r.get("served_model")))


def require_keys():
    if not os.environ.get("GOOGLE_API_KEY") and os.environ.get("GEMINI_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]  # call_google_current reads GOOGLE_API_KEY
    missing = [v for v in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY") if not os.environ.get(v)]
    if missing:
        sys.exit(f"ERROR: missing environment variables: {', '.join(missing)}")


def prereg_guard():
    """Refuse unless the prereg tag is on origin and the anchor file names its commit (as v0.42)."""
    r = subprocess.run(["git", "ls-remote", "--tags", "origin", PREREG_TAG], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"REFUSED: git ls-remote failed: {r.stderr.strip()}")
    shas = dict(reversed(line.split("\t")) for line in r.stdout.splitlines() if "\t" in line)
    tag_ref = f"refs/tags/{PREREG_TAG}"
    if tag_ref not in shas:
        sys.exit(f"REFUSED: tag {PREREG_TAG} not found on origin")
    commit = shas.get(tag_ref + "^{}", shas[tag_ref])
    if not ANCHOR_PATH.exists():
        sys.exit(f"REFUSED: anchor file missing: {ANCHOR_PATH}")
    text = ANCHOR_PATH.read_text(encoding="utf-8")
    if commit not in text and shas[tag_ref] not in text:
        sys.exit(f"REFUSED: {ANCHOR_PATH.name} does not name the commit of {PREREG_TAG} ({commit})")
    return commit


def _log_guard(event):
    GUARD_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(GUARD_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps({"utc": _now(), **event}, ensure_ascii=False) + "\n")


def collect(max_conc, approval):
    commit = prereg_guard()
    print(f"prereg guard passed: {PREREG_TAG} -> {commit}")
    now = _utcnow()
    if not in_window(now):
        sys.exit("REFUSED: outside the collection windows (section 6.7)")
    t4 = t4_guard(now)
    print(f"t4 guard passed: t4 last call {t4['t4_last_call_utc']}")
    other_collection_guard()
    require_keys()
    probes, sha = load_probes()
    specs = build_specs(probes)
    recs = read_raw()
    spent = sum(float(r.get("usd_billed") or 0.0) for r in recs)
    passes = Counter(r["call_id"] for r in recs)
    done = {r["call_id"] for r in recs if answered(r)}
    todo = [s for s in specs if s["call_id"] not in done and passes[s["call_id"]] < MAX_PASSES]
    capped = [s for s in specs if s["call_id"] not in done and passes[s["call_id"]] >= MAX_PASSES]
    GUARD.spent, GUARD.approved = spent, approval
    if approval:
        _log_guard({"event": "approval to spend past $80", "approval": approval, "spend_so_far": spent})
    print(f"{len(specs)} specs, {len(done)} answered, {len(capped)} past the re-run cap (missing), {len(todo)} to send; "
          f"recorded spend ${spent:.2f}")
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    lock = threading.Lock()
    counter = Counter()

    def one(spec):
        if GUARD.stopped:
            return
        rec, _stop = send_call(spec, sha, passes[spec["call_id"]] + 1)
        if rec is None:
            return
        with lock:
            with open(RAW_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
                os.fsync(f.fileno())
            counter[rec["model_requested"], rec["status"]] += 1
        print(f"  {rec['call_id']} {rec['status']} out={rec['output_tokens']} fr={rec['finish_reason']} "
              f"${rec['usd_billed']:.4f} (spend ${GUARD.spent:.2f})", flush=True)

    def worker(model_id):
        mine = [s for s in todo if s["model"]["model_id"] == model_id]
        with ThreadPoolExecutor(max_workers=max_conc) as pool:
            list(pool.map(one, mine))

    with ThreadPoolExecutor(max_workers=len(PANEL)) as pool:
        list(pool.map(worker, [m["model_id"] for m in PANEL]))
    print("done:", dict(counter), f"recorded spend ${GUARD.spent:.2f}")
    if GUARD.stopped:
        _log_guard({"event": "stopped", "reason": GUARD.stopped, "spend": GUARD.spent})
        print("STOPPED:", GUARD.stopped)
        return 4
    return 0


def simulate_worst_case(specs):
    """Paper check of the guard: every request ends at the output cap; workers interleaved one call per model."""
    when = WINDOWS[0][0]
    queues = [[s for s in specs if s["model"]["model_id"] == m["model_id"]] for m in PANEL]
    order = [q[i] for i in range(max(map(len, queues))) for q in queues if i < len(q)]
    res = {}
    for label, approved in (("without approval", None), ("with approval past $80", "simulation")):
        g, sent = Guard(0.0, approved), 0
        for s in order:
            try:
                w = g.reserve(s["model"]["model_id"], when)
            except GuardStop:
                break
            g.settle(w, w)
            sent += 1
        res[label] = (sent, g.spent, g.stopped)
    return res


def dry_run():
    lines = []

    def say(s=""):
        print(s)
        lines.append(s)
    now = datetime.now(timezone.utc)
    say(f"acquire_v1_12.py --dry-run at {now.isoformat(timespec='seconds')} (no network call, no provider SDK import)")
    probes, sha = load_probes()
    specs = build_specs(probes)
    roles = Counter(p["role"] for p in probes)
    say(f"probe file {PROBES_PATH.relative_to(ROOT)}: {len(probes)} probes ({roles.get('CEP', 0)} CEP + "
        f"{roles.get('CONTROL', 0)} control), sha256 {sha}")
    c = Counter((s["model"]["model_id"], s["run"]) for s in specs)
    say(f"{'model':18s} " + " ".join(f"run{r}" for r in RUNS) + "  total")
    for m in PANEL:
        row = [c[(m["model_id"], r)] for r in RUNS]
        say(f"{m['model_id']:18s} " + " ".join(f"{x:4d}" for x in row) + f"  {sum(row):5d}")
    say(f"TOTAL calls: {len(specs)} (expected {EXPECTED_TOTAL}) -> {'OK' if len(specs) == EXPECTED_TOTAL else 'MISMATCH'}")
    bad = {f.__name__: [w for w in SENT_PARAM_WORDS if w in inspect.getsource(f)] for f in CURRENT_DISPATCH.values()}
    say("decoding parameters in the copied call functions: "
        + ("none (temperature, top_p, top_k, reasoning effort and thinking settings are not sent)"
           if not any(bad.values()) else json.dumps(bad)))
    say(f"settings written to every record: {json.dumps(SETTINGS)}")
    for m in PANEL:
        say(f"worst case per request {m['model_id']}: ${worst_usd(m['model_id'], WINDOWS[0][0]):.4f} "
            f"(from 2026-12-01: ${worst_usd(m['model_id'], PRICE_CHANGE_UTC):.4f})")
    for label, (sent, spent, why) in simulate_worst_case(specs).items():
        say(f"guard simulation, every request at the 16,384-token cap, {label}: {sent} calls sent, spend ${spent:.2f}; "
            f"then: {why}")
    tag_local = subprocess.run(["git", "-C", str(ROOT), "tag", "-l", PREREG_TAG], capture_output=True,
                               text=True).stdout.strip()
    say(f"prereg guard (local check only): tag {PREREG_TAG} {'present locally' if tag_local else 'absent'}; anchor "
        f"file {'present' if ANCHOR_PATH.exists() else 'absent'} -> --collect would be "
        f"{'checked against origin' if tag_local and ANCHOR_PATH.exists() else 'REFUSED'}")
    say("collection windows (UTC): " + "; ".join(f"{a:%Y-%m-%d %H:%M} to {b:%Y-%m-%d %H:%M}" for a, b in WINDOWS)
        + f"; now {'inside' if in_window(now) else 'outside'}")
    say(f"t4 completion record {T4_RECORD.relative_to(ROOT)}: {'present' if T4_RECORD.exists() else 'absent'} -> "
        f"--collect {'checks it against the t4 raw file' if T4_RECORD.exists() else 'would be REFUSED'}; "
        f"--collect also refuses while another acquire_v*.py --collect runs")
    say(f"raw record {RAW_PATH.relative_to(ROOT)}: {'exists' if RAW_PATH.exists() else 'absent (nothing collected)'}")
    sdk = [m for m in ("anthropic", "openai", "google.genai") if m in sys.modules]
    say(f"provider SDKs imported: {', '.join(sdk) if sdk else 'none'}; nothing sent.")
    DRY_RUN_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0 if len(specs) == EXPECTED_TOTAL and not any(bad.values()) and not sdk else 1


def main():
    ap = argparse.ArgumentParser(description="AIAS v1.12 Coverage Paper A acquisition")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--collect", action="store_true", help="guarded: prereg tag on origin + anchor file + window")
    ap.add_argument("--max-concurrency", type=int, default=1, help="concurrent calls per model (default 1)")
    ap.add_argument("--approve-past-80", default=None, metavar="WHO_WHEN",
                    help="Pablo's recorded approval to spend past $80 (the $100 cap stays)")
    a = ap.parse_args()
    if a.dry_run == a.collect:
        ap.error("choose exactly one of --dry-run / --collect")
    if a.dry_run:
        return dry_run()
    return collect(a.max_concurrency, a.approve_past_80)


if __name__ == "__main__":
    sys.exit(main())
