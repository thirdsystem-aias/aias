#!/usr/bin/env python3
"""
judge_v1_11.py - AIAS v1.11 Sentiment Paper A: judge acquisition (the only paid calls of v1.11).

STATUS: r1 pre-lock (2026-11-10). PRE_REGISTRATION_v1_11.md sections 4.2, 7 and 8 (decisions 1 and 7).

Call functions: forked from the three current-arm functions of osf/v42/scripts/acquire_v0_42.py
(branch v0.42; the copy in osf/methodology/v1_12/scripts/acquire_v1_12.py), changed only to send
the judge's system prompt and the model's lowest documented reasoning effort, to drop web search
and to take the request as a dict that is recorded. Transient and _call_with_retry are unchanged
(3 attempts on rate limits, 5xx, connection errors and timeouts, backoff 1 s, 2 s).

No sampling parameter (temperature, top_p, top_k) is ever sent. Reasoning: Claude Opus 5.5
output_config.effort "low"; GPT-6.1 Sol reasoning.effort "low"; Gemini 4 Argon (alternate)
thinking_config.thinking_level "low" (score_v1_11.JUDGES). Max output 4,096 tokens including
reasoning. Prompt-only JSON. Every request parameter is written to the record of every call.

Endpoints (budget redesign of 2026-11-10, section 7): J1 through Anthropic's Message Batches API and
J2 through OpenAI's Batch API (/v1/responses), each at 50% of list price, in batches of at most 500
requests; the alternate (contingency only) through Google's synchronous API. The request body is
the same dict in both modes (request_kwargs). Every submitted batch is logged (batches_v1_11.jsonl)
before its results are read, so an interrupted run re-attaches to its batches instead of resending.

Cost guard (section 7): before every call, or every batch, it adds the worst case (input tokens
bounded by the request's UTF-8 bytes; output at the 4,096-token cap, twice for Gemini, whose
thinking is billed beside it; batch price for batch calls) to the recorded spend plus the worst
cases in flight, and does not send if the sum passes US$100; a batch is cut to the requests that
fit. At US$80 of recorded spend nothing more is sent until the run is resumed with
--approve-past-pause "<who, when>" (logged). 30,000 calls at most. Spend = recorded tokens at list
price (batch price for batch calls; no cache discount assumed); a call that times out is counted at
its worst case. A batch is submitted only if no blackout window starts within its 24-hour window.

Order (section 8): phase A = R and F, J1 and J2 in parallel; A2 = their self-consistency repeats;
B = E (J1 all judged windows, J2 its sample); B2 = E repeats. Within a phase and judge the order is
shuffled (seed 111000). Calibration: after the first 200 phase-A calls of each judge the projection
is recomputed from the measured tokens and the fixed reduction order is applied, once, before any E
call (plan file; it must fit under US$80 with 15% overhead). Resumable: every call is appended to
the raw JSONL; done units are skipped.

Modes
  --dry-run   no network and no provider SDK import: every request built from the U0 unit table,
              sampling-parameter check, cost projection (planning values, scenarios, break-even),
              guard simulation, lock / window status. Writes prereg/dry_run_judge_v1_11.txt and
              prereg/cost_projection_v1_11.json (with --replica: the synthetic replica).
  --simulate  end-to-end rehearsal on the synthetic replica: a fake judge and a fake batch service
              stand in for every provider (no network), with invalid outputs, a served-ID mismatch,
              errored batch items, an interrupted run with a batch in flight, the pause, a resume
              and the freeze.
  --run       the paid run (refused unless tag v1.11-prereg-r1 is on origin, the anchor file passes
              score_v1_11.anchor_problems (its commit and a non-empty osf_deposit), the time is
              outside every blackout window, no other collection process runs, and
              --no-other-collection "<who, when>" is given).
  --freeze    hashes the raw outputs; --run then refuses; score_v1_11.py --stage J may run.

Interpreter: the system Python 3.14 (/Library/Frameworks/Python.framework/Versions/3.14/bin/python3),
which has numpy and the provider SDKs (on 2026-11-10: anthropic 0.102.0, openai 2.37.0, google-genai
2.3.0; each accepts the request fields above, checked offline). The .venv-v41 environment has the SDKs
but not numpy, which score_v1_11 / score_v1_10 import. --run records the interpreter and SDK versions.
"""
from __future__ import annotations

import argparse
import hashlib
import inspect
import json
import math
import os
import random
import re
import subprocess
import sys
import threading
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import score_v1_11 as S  # noqa: E402

V = S.V
PLAN_NAME = "plan_v1_11.json"
GUARD_LOG_NAME = "guard_log_v1_11.jsonl"
BATCHES_NAME = "batches_v1_11.jsonl"
DRY_TXT = S.PREREG_DIR / "dry_run_judge_v1_11.txt"
COST_JSON = S.PREREG_DIR / "cost_projection_v1_11.json"
PREREG_TAG = S.PREREG_TAG
PHASES = ["A", "A2", "B", "B2"]
MAX_PASSES = 2                       # an API error (after the transient retries) is re-sent once
PAUSE = {"anthropic": 2.0, "openai": 1.0, "google": 1.0}     # v0.42 values (seconds between calls)
MAX_ATTEMPTS = 3                                             # v0.42 transient retry policy

UTC = timezone.utc
BLACKOUTS = [  # decision 7: one paid collection at a time on the Mac; never during Nov 17-21
    ("t4 = v0.42 collection: from Nov 10, 11:30 pm CT, up to 72 h",
     datetime(2026, 11, 11, 5, 30, tzinfo=UTC), datetime(2026, 11, 14, 5, 30, tzinfo=UTC)),
    ("v1.12 Coverage collection: Nov 14-16 UTC",
     datetime(2026, 11, 14, 0, 0, tzinfo=UTC), datetime(2026, 11, 17, 0, 0, tzinfo=UTC)),
    ("no judge run Nov 17-21 (UTC dates and US Central dates)",
     datetime(2026, 11, 17, 0, 0, tzinfo=UTC), datetime(2026, 11, 22, 6, 0, tzinfo=UTC)),
]
OTHER_COLLECTION = re.compile(r"acquire_v\d|run_acquisition|run_t\d_chain|acquire_[a-z_]*\.py")
SAMPLING_WORDS = ("temperature", "top_p", "top_k")


def in_blackout(when: datetime):
    return next((name for name, a, b in BLACKOUTS if a <= when < b), None)


def blackout_within(start: datetime, hours: float = S.BATCH_WINDOW_HOURS):
    """A batch may be processed at any time in [start, start + 24 h): it is submitted only if no
    blackout window overlaps that interval."""
    end = start + timedelta(hours=hours)
    return next((name for name, a, b in BLACKOUTS if a < end and start < b), None)


# ----- copied unchanged from acquire_v0_42.py (via acquire_v1_12.py): Transient, _call_with_retry
class Transient(Exception):
    """Rate limit, 5xx/overload, connection or timeout error: retry-eligible."""


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


# ======================= requests (one source of truth: score_v1_11) =======================
def request_kwargs(model_id: str, provider: str, system: str, user: str) -> dict:
    """The exact SDK request. No sampling parameter; the reasoning parameter is the model's."""
    rp = next(j["reasoning_param"] for j in S.JUDGES.values() if j["model_id"] == model_id)
    if provider == "anthropic":
        return {"model": model_id, "max_tokens": S.MAX_OUTPUT_TOKENS, "system": system,
                "messages": [{"role": "user", "content": user}], **rp}
    if provider == "openai":
        return {"model": model_id, "instructions": system, "input": user,
                "max_output_tokens": S.MAX_OUTPUT_TOKENS, **rp}
    if provider == "google":
        return {"model": model_id, "contents": user,
                "config": {"system_instruction": system, "max_output_tokens": S.MAX_OUTPUT_TOKENS, **rp}}
    raise ValueError(provider)


def _h(s: str) -> dict:
    return {"sha256": hashlib.sha256(s.encode("utf-8")).hexdigest(), "chars": len(s)}


def params_record(kw: dict) -> dict:
    """Every request parameter, with the two message texts replaced by their SHA-256 and length
    (both are rebuilt exactly from the unit table and the prompt)."""
    r = json.loads(json.dumps(kw))
    if "messages" in r:
        r["messages"] = [{"role": m["role"], "content": _h(m["content"])} for m in r["messages"]]
    for k in ("system", "instructions", "input", "contents"):
        if isinstance(r.get(k), str):
            r[k] = _h(r[k])
    if "config" in r and isinstance(r["config"].get("system_instruction"), str):
        r["config"]["system_instruction"] = _h(r["config"]["system_instruction"])
    return r


def sampling_params_sent(kw: dict) -> list:
    flat = json.dumps(params_record(kw))
    return [w for w in SAMPLING_WORDS if f'"{w}"' in flat]


def is_batch(model_id: str) -> bool:
    return S.judge_mode(model_id) == "batch"


def worst_usd(model_id: str, provider: str, kw: dict, when: datetime, batch: bool = False) -> float:
    tin = len(json.dumps(kw).encode("utf-8"))                 # tokens <= bytes of the request
    tout = S.MAX_OUTPUT_TOKENS * (2 if provider == "google" else 1)
    return S.call_usd(model_id, tin, tout, when, batch)


def actual_usd(model_id: str, provider: str, when: datetime, tin, tout, tthought, batch: bool = False) -> float:
    """Google thinking tokens are billed as output and not included in its candidate count;
    the other providers' output counts already include reasoning (as v1.12)."""
    out = (tout or 0) + ((tthought or 0) if provider == "google" else 0)
    return S.call_usd(model_id, tin or 0, out, when, batch)


# ======================= response parsers (one per provider format; sync and batch) ==========
def parse_anthropic_message(d: dict) -> dict:
    """A Messages API response (dict). All input tokens are counted at the base input price,
    including any cache read or write (an upper bound); output tokens include thinking."""
    u = d.get("usage") or {}
    tin = sum(int(u.get(k) or 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
    content = d.get("content") or []
    return {"text": "".join(b.get("text", "") for b in content if b.get("type") == "text"),
            "served_model": d.get("model"), "finish_reason": d.get("stop_reason"),
            "tokens_in": tin, "tokens_out": u.get("output_tokens"), "tokens_thought": None,
            "thinking_blocks": sum(1 for b in content if b.get("type") in ("thinking", "redacted_thinking"))}


def parse_openai_response(d: dict) -> dict:
    """A Responses API response (dict; the batch output line's response.body)."""
    u = d.get("usage") or {}
    det = u.get("output_tokens_details") or {}
    text = "".join(c.get("text", "") for item in (d.get("output") or []) if item.get("type") == "message"
                   for c in (item.get("content") or []) if c.get("type") == "output_text")
    fr = d.get("status")
    inc = d.get("incomplete_details") or {}
    if inc.get("reason"):
        fr = f"{fr}:{inc['reason']}"
    return {"text": text, "served_model": d.get("model"), "finish_reason": fr,
            "tokens_in": u.get("input_tokens"), "tokens_out": u.get("output_tokens"),
            "tokens_thought": det.get("reasoning_tokens")}


PARSERS = {"anthropic": parse_anthropic_message, "openai": parse_openai_response}


def served_ok(requested: str, served) -> bool:
    """As score_v0_42.served_ok: the requested ID or a dated snapshot of it."""
    s = (served or "").strip().removeprefix("models/")
    return s == requested or re.fullmatch(re.escape(requested) + r"-(\d{4}-\d{2}-\d{2}|\d{8})", s) is not None


# ======================= provider calls (forked from acquire_v0_42.py) =======================
def call_anthropic(kw):
    import anthropic
    client = anthropic.Anthropic()
    try:
        m = client.messages.create(**kw)
    except (anthropic.RateLimitError, anthropic.APIConnectionError, anthropic.APITimeoutError) as e:
        raise Transient(str(e)) from e
    except anthropic.APIStatusError as e:
        if e.status_code >= 500:
            raise Transient(str(e)) from e
        raise
    text = "".join(b.text for b in m.content if getattr(b, "type", None) == "text")
    thinking = sum(1 for b in m.content if getattr(b, "type", None) in ("thinking", "redacted_thinking"))
    return {"text": text, "served_model": m.model, "finish_reason": m.stop_reason,
            "tokens_in": m.usage.input_tokens, "tokens_out": m.usage.output_tokens, "tokens_thought": None,
            "thinking_blocks": thinking}


def call_openai(kw):
    import openai
    client = openai.OpenAI()
    try:
        r = client.responses.create(**kw)
    except (openai.RateLimitError, openai.APIConnectionError, openai.APITimeoutError) as e:
        raise Transient(str(e)) from e
    except openai.APIStatusError as e:
        if e.status_code >= 500:
            raise Transient(str(e)) from e
        raise
    u = r.usage
    det = getattr(u, "output_tokens_details", None)
    fr = r.status
    inc = getattr(r, "incomplete_details", None)
    if inc is not None and getattr(inc, "reason", None):
        fr = f"{r.status}:{inc.reason}"
    return {"text": r.output_text or "", "served_model": r.model, "finish_reason": fr,
            "tokens_in": getattr(u, "input_tokens", None), "tokens_out": getattr(u, "output_tokens", None),
            "tokens_thought": getattr(det, "reasoning_tokens", None) if det is not None else None}


def call_google(kw):
    from google import genai
    from google.genai import errors, types
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    c = dict(kw["config"])
    tc = c.pop("thinking_config", None)
    cfg = types.GenerateContentConfig(**c, thinking_config=types.ThinkingConfig(
        thinking_level=tc["thinking_level"]) if tc else None)
    try:
        r = client.models.generate_content(model=kw["model"], contents=kw["contents"], config=cfg)
    except errors.ServerError as e:
        raise Transient(str(e)) from e
    except errors.ClientError as e:
        if getattr(e, "code", None) == 429:
            raise Transient(str(e)) from e
        raise
    try:
        fr = str(r.candidates[0].finish_reason)
    except Exception:
        fr = None
    try:
        text = r.text or ""
    except Exception:
        text = ""
    um = r.usage_metadata
    return {"text": text, "served_model": getattr(r, "model_version", None), "finish_reason": fr,
            "tokens_in": getattr(um, "prompt_token_count", None), "tokens_out": getattr(um, "candidates_token_count", None),
            "tokens_thought": getattr(um, "thoughts_token_count", None)}


DISPATCH = {"anthropic": call_anthropic, "openai": call_openai, "google": call_google}


# ======================= paths, units, plan =======================
class Paths:
    def __init__(self, dry: bool):
        self.dry = dry
        self.prereg = S.DRY_OUTDIR if dry else S.PREREG_DIR
        self.data = S.DRY_OUTDIR if dry else S.DATA_DIR
        self.out = S.DRY_OUTDIR if dry else S.OUTDIR
        self.units, self.u0 = self.prereg / S.UNITS_NAME, self.prereg / S.U0_NAME
        self.raw, self.plan = self.data / S.RAW_NAME, self.data / PLAN_NAME
        self.roles = self.data / "roles_v1_11.json"
        self.guard_log, self.frozen = self.data / GUARD_LOG_NAME, self.out / S.FROZEN_NAME
        self.batches = self.data / BATCHES_NAME
        self.dry_txt = (S.DRY_OUTDIR / "dry_run_judge_v1_11.txt") if dry else DRY_TXT
        self.cost_json = (S.DRY_OUTDIR / "cost_projection_v1_11.json") if dry else COST_JSON


def load_units(P: Paths):
    u0 = json.loads(P.u0.read_text(encoding="utf-8"))
    if V.sha256(P.units) != u0["units_file"]["sha256"]:
        sys.exit("ABORT: the unit table differs from the U0 record")
    return u0, S.read_units(P.units)


DEFAULT_ROLES = {"J1": S.JUDGES["J1"]["model_id"], "J2": S.JUDGES["J2"]["model_id"]}


def provider_of_model(model_id: str) -> str:
    return next(j["provider"] for j in S.JUDGES.values() if j["model_id"] == model_id)


def current_roles(P: Paths) -> dict:
    if P.roles.exists():
        return json.loads(P.roles.read_text(encoding="utf-8"))["roles"]
    return dict(DEFAULT_ROLES)


def jobs_for(units, params):
    """Every call of the plan, in run order: phases A (R+F), A2 (R+F repeats), B (E), B2 (E repeats);
    J1 and J2 jobs per phase, each shuffled with seed 111000."""
    eff = S.effective_units(units, params)
    by = {u["unit_id"]: u for u in eff}
    jobs = []
    for phase in PHASES:
        for role in ("J1", "J2"):
            sel = sorted(u["unit_id"] for u in eff if u["judged"] and (role == "J1" or u["j2"])
                         and (u["block"] in ("R", "F")) == (phase in ("A", "A2"))
                         and (phase in ("A", "B") or u["selfcon"]))
            random.Random(f"{S.SEEDS['unit_order']}|{phase}|{role}").shuffle(sel)
            jobs += [{"phase": phase, "role": role, "unit_id": uid,
                      "pass": "repeat" if phase in ("A2", "B2") else "main"} for uid in sel]
    return jobs, by


def project_jobs(jobs, by, roles, in_per_char: dict, out_per_call: dict, when: datetime, batch=None) -> dict:
    """Projected spend of a job list. batch: {role: bool} (default: each model's judge mode)."""
    usd, n = 0.0, Counter()
    tok_in, tok_out = Counter(), Counter()
    bm = {r: (is_batch(m) if batch is None else batch[r]) for r, m in roles.items()}
    for j in jobs:
        m = roles[j["role"]]
        ti = math.ceil(by[j["unit_id"]]["request_chars"] * in_per_char[j["role"]])
        to = out_per_call[j["role"]]
        usd += S.call_usd(m, ti, to, when, bm[j["role"]])
        n[j["role"]] += 1
        tok_in[j["role"]] += ti
        tok_out[j["role"]] += to
    return {"calls": sum(n.values()), "calls_by_role": dict(n), "tokens_in_by_role": dict(tok_in),
            "tokens_out_by_role": dict(tok_out), "usd": usd, "usd_with_overhead": usd * S.COST_OVERHEAD,
            "calls_with_overhead": math.ceil(sum(n.values()) * S.COST_OVERHEAD)}


def choose_plan(units, roles, in_per_char, out_per_call, when, cap=S.PLAN_TARGET_USD) -> dict:
    """The binding projection (section 7): the full design first; while the projection with 15%
    overhead passes US$80 (the pause; or 30,000 calls), the next reduction of the fixed order is
    applied."""
    params, applied, steps = dict(S.DEFAULT_PLAN), [], []
    jobs, by = jobs_for(units, params)
    p = project_jobs(jobs, by, roles, in_per_char, out_per_call, when)
    steps.append({"params": dict(params), **p})
    for key, val in S.REDUCTION_ORDER:
        if p["usd_with_overhead"] <= cap and p["calls_with_overhead"] <= S.HARD_CAP_CALLS:
            break
        params[key] = val
        applied.append(f"{key}={val}")
        jobs, by = jobs_for(units, params)
        p = project_jobs(jobs, by, roles, in_per_char, out_per_call, when)
        steps.append({"params": dict(params), **p})
    fits = p["usd_with_overhead"] <= cap and p["calls_with_overhead"] <= S.HARD_CAP_CALLS
    return {"params": params, "reductions_applied": applied, "steps": steps, "fits": fits,
            "jobs_sha256": hashlib.sha256(json.dumps(jobs).encode()).hexdigest()}


# ======================= guard and the call loop =======================
class GuardStop(BaseException):
    """Stops sending (a BaseException, so the copied _call_with_retry never records it as an error)."""


class Guard:
    def __init__(self, spent: float, calls: int, approved, sim: bool = False, max_new_calls=None):
        self.cg = S.CostGuard(spent_usd=spent, calls=calls, approved_past_pause=approved)
        self.lock, self.stopped, self.sim, self.new_calls, self.max_new = threading.Lock(), None, sim, 0, max_new_calls

    def reserve(self, worst: float, when: datetime) -> None:
        with self.lock:
            if self.stopped:
                raise GuardStop(self.stopped)
            b = None if self.sim else in_blackout(when)
            if b:
                self.stopped = f"blackout window: {b}"
            elif self.max_new is not None and self.new_calls >= self.max_new:
                self.stopped = f"stopped after {self.max_new} calls (requested)"
            else:
                self.stopped = self.cg.check(worst)
            if self.stopped:
                raise GuardStop(self.stopped)
            self.cg.reserve(worst)
            self.new_calls += 1

    def reserve_batch(self, worsts, when: datetime) -> int:
        """Reserve the worst cases of the leading requests of a batch that fit; returns how many.
        0 = none fits now but other batches are in flight (wait for them); otherwise GuardStop."""
        with self.lock:
            if self.stopped:
                raise GuardStop(self.stopped)
            b = None if self.sim else blackout_within(when)
            if b:
                self.stopped = f"blackout window within the batch's {S.BATCH_WINDOW_HOURS} h window: {b}"
                raise GuardStop(self.stopped)
            worsts = list(worsts)
            if self.max_new is not None:
                room = self.max_new - self.new_calls
                if room <= 0:
                    self.stopped = f"stopped after {self.max_new} calls (requested)"
                    raise GuardStop(self.stopped)
                worsts = worsts[:room]
            k, why = self.cg.fit(worsts)
            if k == 0:
                if why and why.startswith("CAP") and self.cg.reserved_usd > 1e-12:
                    return 0
                self.stopped = why or "CAP: no request fits"
                raise GuardStop(self.stopped)
            self.cg.reserve_many(worsts[:k])
            self.new_calls += k
            return k

    def hold(self, worsts) -> None:
        """Re-attached in-flight batches: their worst cases are reserved without any check."""
        with self.lock:
            self.cg.reserved_usd += sum(worsts)
            self.cg.calls += len(worsts)

    def stop(self, why: str) -> None:
        with self.lock:
            self.stopped = self.stopped or why

    def settle(self, reserved: float, actual: float) -> None:
        with self.lock:
            self.cg.settle(reserved, actual)


def _now_dt():
    return datetime.now(UTC)


def send_one(job, unit, model_id, provider, attempt, guard, dispatch) -> dict:
    req = S.build_request(unit)
    kw = request_kwargs(model_id, provider, req["system"], req["user"])
    when = _now_dt()
    w = worst_usd(model_id, provider, kw, when)
    guard.reserve(w, when)
    t0 = _now_dt().isoformat()
    out, tries, err = _call_with_retry(dispatch[provider], kw)
    if out is None:
        cost, est = (w, True) if (err and "timeout" in err.lower()) else (0.0, False)
    else:
        cost, est = actual_usd(model_id, provider, when, out.get("tokens_in"), out.get("tokens_out"),
                               out.get("tokens_thought")), False
    guard.settle(w, cost)
    return make_record(job["role"], job["pass"], job["phase"], unit["unit_id"], model_id, provider, attempt,
                       kw, out, err, tries, cost, est, w, t0, _now_dt().isoformat(), {"mode": "sync"})


def make_record(role, pas, phase, unit_id, model_id, provider, attempt, kw, out, err, tries, cost, est, w,
                t0, t1, extra) -> dict:
    """One call record (sync or batch): status, validity and every request parameter."""
    out = out or {}
    status = "error" if not out else ("empty" if not (out.get("text") or "").strip() else "ok")
    sok = served_ok(model_id, out.get("served_model")) if out else False
    perr, valid = None, False
    if status == "ok" and sok:
        try:
            S.parse_judge_output(out["text"])
            valid = True
        except S.JudgeOutputError as e:
            perr = str(e)
    elif status == "ok":
        perr = f"served model {out.get('served_model')!r} is not {model_id}"
    return {"phase_id": S.PHASE_ID, "call_id": f"{role}|{unit_id}|{pas}|{attempt}",
            "role": role, "judge_model": model_id, "provider": provider, "unit_id": unit_id,
            "pass": pas, "plan_phase": phase, "attempt": attempt, "status": status,
            "valid": valid, "parse_error": perr, "text": out.get("text", ""), "served_model": out.get("served_model"),
            "served_ok": sok, "finish_reason": out.get("finish_reason"), "input_tokens": out.get("tokens_in"),
            "output_tokens": out.get("tokens_out"), "thinking_tokens": out.get("tokens_thought"),
            "thinking_blocks": out.get("thinking_blocks"), "transient_tries": tries, "error": err,
            "usd": cost, "usd_estimated": est, "worst_case_usd": w, "request": params_record(kw),
            "sampling_parameters_sent": sampling_params_sent(kw), "started_utc": t0, "finished_utc": t1, **extra}


# ======================= batch endpoints (J1 and J2; section 7) =======================
def custom_id(role: str, unit_id: str, pas: str, attempt: int) -> str:
    """Batch request id (Anthropic: [A-Za-z0-9_-]{1,64}); the unit is identified by a hash."""
    return f"v111-{role}-{pas}-{attempt}-" + hashlib.sha256(unit_id.encode("utf-8")).hexdigest()[:24]


class RealBatchClient:
    """Anthropic Message Batches API and OpenAI Batch API (/v1/responses). Network: --run only.
    The request body of each item is request_kwargs(...) unchanged."""

    TERMINAL = {"anthropic": {"ended"}, "openai": {"completed", "failed", "expired", "cancelled"}}

    def __init__(self):
        self._c = {}

    def _client(self, provider):
        if provider not in self._c:
            if provider == "anthropic":
                import anthropic
                self._c[provider] = anthropic.Anthropic()
            elif provider == "openai":
                import openai
                self._c[provider] = openai.OpenAI()
            else:
                raise ValueError(f"no batch endpoint used for {provider}")
        return self._c[provider]

    def submit(self, provider: str, items) -> str:
        c = self._client(provider)
        if provider == "anthropic":
            return c.messages.batches.create(requests=[{"custom_id": cid, "params": kw} for cid, kw in items]).id
        body = "".join(json.dumps({"custom_id": cid, "method": "POST", "url": "/v1/responses", "body": kw},
                                  ensure_ascii=False) + "\n" for cid, kw in items).encode("utf-8")
        f = c.files.create(file=("v1_11_batch.jsonl", body), purpose="batch")
        return c.batches.create(input_file_id=f.id, endpoint="/v1/responses", completion_window="24h").id

    def status(self, provider: str, batch_id: str):
        c = self._client(provider)
        st = (c.messages.batches.retrieve(batch_id).processing_status if provider == "anthropic"
              else c.batches.retrieve(batch_id).status)
        return st in self.TERMINAL[provider], st

    def results(self, provider: str, batch_id: str) -> dict:
        c = self._client(provider)
        out = {}
        if provider == "anthropic":
            for r in c.messages.batches.results(batch_id):
                d = r.model_dump()
                res = d.get("result") or {}
                out[d["custom_id"]] = ({"body": res.get("message"), "error": None} if res.get("type") == "succeeded"
                                       else {"body": None, "error": f"{res.get('type')}: {res.get('error')}"[:500]})
            return out
        b = c.batches.retrieve(batch_id)
        for fid in (b.output_file_id, b.error_file_id):
            if not fid:
                continue
            for line in c.files.content(fid).text.splitlines():
                if not line.strip():
                    continue
                d = json.loads(line)
                resp = d.get("response") or {}
                if d.get("error") or resp.get("status_code") != 200:
                    out[d["custom_id"]] = {"body": None, "error": str(d.get("error") or resp.get("body"))[:500]}
                else:
                    out[d["custom_id"]] = {"body": resp.get("body"), "error": None}
        return out


def read_batches(P: Paths) -> list:
    return read_raw(P.batches)


def open_batches(P: Paths) -> list:
    ents = read_batches(P)
    closed = {e["batch_id"] for e in ents if e.get("event") == "collected"}
    return [e for e in ents if e.get("event") == "submitted" and e["batch_id"] not in closed]


def _apply(st, rec, roles, lock, P: Paths):
    with lock:
        with open(P.raw, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())
        if roles.get(rec["role"]) != rec["judge_model"]:
            return
        s = st[(rec["role"], rec["unit_id"], rec["pass"])]
        s["attempt_max"] = max(s["attempt_max"], rec["attempt"])
        if rec["status"] == "error":
            s["errors"] += 1
        elif rec["valid"]:
            s["valid"] = True
        else:
            s["invalid"] += 1


def collect_batch(entry, by, roles, guard, bc, st, P: Paths, sim, lock, log) -> None:
    """Wait for a submitted batch to end, then write one call record per item (in submission
    order), settle the guard with the recorded cost, and log the collection."""
    prov, model, bid = entry["provider"], entry["judge_model"], entry["batch_id"]
    polls, fails = 0, 0
    while True:
        try:
            ended, status = bc.status(prov, bid)
            fails = 0
        except Exception as e:  # noqa: BLE001  (network: keep polling; the batch is already paid for)
            ended, status, fails = False, f"status error: {type(e).__name__}: {e}"[:300], fails + 1
            if fails in (1, 10, 100):
                log(f"[v1.11] batch {bid}: {status} (polling continues)")
        if ended:
            break
        polls += 1
        time.sleep(0 if sim else S.BATCH_POLL_SECONDS)
    res = bc.results(prov, bid)
    when = datetime.fromisoformat(entry["submitted_utc"])
    t1 = _now_dt().isoformat()
    by_cid = {}
    for cid, kw in entry.get("_kw", []):
        by_cid[cid] = kw
    for it in entry["items"]:
        unit = by.get(it["unit_id"])
        kw = by_cid.get(it["custom_id"])
        if kw is None:                                   # re-attached: rebuild the identical request
            req = S.build_request(unit)
            kw = request_kwargs(model, prov, req["system"], req["user"])
        r = res.get(it["custom_id"]) or {"body": None, "error": f"missing from the batch results ({status})"}
        out = PARSERS[prov](r["body"]) if r.get("body") is not None else None
        cost = actual_usd(model, prov, when, out.get("tokens_in"), out.get("tokens_out"), out.get("tokens_thought"),
                          batch=True) if out else 0.0
        guard.settle(it["worst_case_usd"], cost)
        rec = make_record(entry["role"], it["pass"], it["plan_phase"], it["unit_id"], model, prov, it["attempt"],
                          kw, out, None if out else r.get("error"), 1, cost, False, it["worst_case_usd"],
                          entry["submitted_utc"], t1, {"mode": "batch", "batch_id": bid, "custom_id": it["custom_id"],
                                                       "batch_status": status})
        _apply(st, rec, roles, lock, P)
    with lock:
        with open(P.batches, "a", encoding="utf-8") as f:
            f.write(json.dumps({"event": "collected", "batch_id": bid, "collected_utc": t1, "status": status,
                                "results": len(res), "polls": polls}) + "\n")


def batch_worker(role, jobs_role, by, roles, guard, bc, st, P: Paths, sim, lock, log) -> None:
    model = roles[role]
    prov = provider_of_model(model)
    while True:
        if guard.stopped:
            return
        pending = [j for j in jobs_role if not done(st[(role, j["unit_id"], j["pass"])])]
        if not pending:
            return
        now = _now_dt()
        cand = []
        for j in pending[:S.BATCH_MAX_REQUESTS]:
            att = st[(role, j["unit_id"], j["pass"])]["attempt_max"] + 1
            req = S.build_request(by[j["unit_id"]])
            kw = request_kwargs(model, prov, req["system"], req["user"])
            cand.append((j, att, kw, worst_usd(model, prov, kw, now, batch=True)))
        try:
            k = guard.reserve_batch([c[3] for c in cand], now)
        except GuardStop:
            return
        if k == 0:                                   # other batches in flight hold the room: wait
            time.sleep(0.01 if sim else S.BATCH_POLL_SECONDS)
            continue
        cand = cand[:k]
        items = [(custom_id(role, j["unit_id"], j["pass"], att), kw) for j, att, kw, _ in cand]
        try:
            bid = bc.submit(prov, items)
        except Exception as e:  # noqa: BLE001
            for *_, w in cand:
                guard.settle(w, 0.0)
            guard.stop(f"batch submission failed ({role}): {type(e).__name__}: {e}"[:300])
            return
        entry = {"event": "submitted", "batch_id": bid, "role": role, "judge_model": model, "provider": prov,
                 "submitted_utc": now.isoformat(), "n": len(items),
                 "worst_case_usd": sum(c[3] for c in cand),
                 "request_sha256": hashlib.sha256("".join(json.dumps(kw, sort_keys=True) for _, kw in items)
                                                  .encode("utf-8")).hexdigest(),
                 "items": [{"custom_id": cid, "unit_id": j["unit_id"], "pass": j["pass"], "plan_phase": j["phase"],
                            "attempt": att, "worst_case_usd": w} for (cid, _), (j, att, _, w) in zip(items, cand)]}
        with lock:
            P.batches.parent.mkdir(parents=True, exist_ok=True)
            with open(P.batches, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                f.flush()
                os.fsync(f.fileno())
        if getattr(bc, "interrupt_now", None) and bc.interrupt_now():
            guard.stop("simulated interruption with a batch in flight")
            return
        collect_batch({**entry, "_kw": items}, by, roles, guard, bc, st, P, sim, lock, log)


def reattach(P: Paths, by, roles, guard, bc, st, sim, log) -> int:
    """Batches submitted by an earlier, interrupted run: hold their worst cases, wait for them and
    record their results before anything new is sent. Returns how many were collected."""
    ents = open_batches(P)
    if not ents:
        return 0
    lock = threading.Lock()
    for e in ents:
        guard.hold([it["worst_case_usd"] for it in e["items"]])
    for e in ents:
        log(f"[v1.11] re-attaching batch {e['batch_id']} ({e['role']}, {e['n']} requests)")
        collect_batch(e, by, roles, guard, bc, st, P, sim, lock, log)
    log_guard(P, {"event": "re-attached in-flight batches", "batches": [e["batch_id"] for e in ents]})
    return len(ents)


def read_raw(path: Path) -> list:
    recs = []
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    recs.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return recs


def state_from(recs, roles):
    st = defaultdict(lambda: {"valid": False, "invalid": 0, "errors": 0, "attempt_max": 0})
    for r in recs:
        if roles.get(r["role"]) != r["judge_model"]:
            continue
        s = st[(r["role"], r["unit_id"], r["pass"])]
        s["attempt_max"] = max(s["attempt_max"], int(r["attempt"]))
        if r["status"] == "error":
            s["errors"] += 1
        elif r.get("valid"):
            s["valid"] = True
        else:
            s["invalid"] += 1
    return st


def done(s) -> bool:
    return s["valid"] or s["invalid"] >= 1 + S.MAX_PARSE_RETRIES or s["errors"] >= MAX_PASSES


def execute(jobs, by, roles, guard, dispatch, st, P: Paths, sim: bool, log, bc=None):
    """J1 and J2 in parallel (one thread each): batch judges through `bc` (batch_worker), the
    synchronous alternate call by call through `dispatch`."""
    lock = threading.Lock()
    by_role = defaultdict(list)
    for j in jobs:
        by_role[j["role"]].append(j)

    def worker(role):
        model = roles[role]
        prov = provider_of_model(model)
        if is_batch(model):
            if bc is None:
                raise RuntimeError(f"{model} runs through the batch endpoint, but no batch client was given")
            return batch_worker(role, by_role[role], by, roles, guard, bc, st, P, sim, lock, log)
        for j in by_role[role]:
            s = st[(role, j["unit_id"], j["pass"])]
            while not done(s):
                if guard.stopped:
                    return
                try:
                    rec = send_one(j, by[j["unit_id"]], model, prov, s["attempt_max"] + 1, guard, dispatch)
                except GuardStop:
                    return
                with lock:
                    with open(P.raw, "a", encoding="utf-8") as f:
                        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                        f.flush()
                        os.fsync(f.fileno())
                    s["attempt_max"] = rec["attempt"]
                    if rec["status"] == "error":
                        s["errors"] += 1
                    elif rec["valid"]:
                        s["valid"] = True
                    else:
                        s["invalid"] += 1
                if not sim:
                    time.sleep(PAUSE[prov])

    P.raw.parent.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=max(1, len(by_role))) as ex:
        list(ex.map(worker, sorted(by_role)))


def log_guard(P: Paths, event: dict):
    P.guard_log.parent.mkdir(parents=True, exist_ok=True)
    with open(P.guard_log, "a", encoding="utf-8") as f:
        f.write(json.dumps({"utc": _now_dt().isoformat(), **event}, ensure_ascii=False) + "\n")


def measure(recs, roles, by) -> tuple:
    """Calibration: tokens per request character and output tokens per call (reasoning included;
    Gemini's thinking added) from the recorded phase-A responses of each judge."""
    ipc, opc, n = {}, {}, {}
    for role, model in roles.items():
        rs = [r for r in recs if r["role"] == role and r["judge_model"] == model and r["status"] != "error"
              and r.get("input_tokens") is not None]
        chars = sum(by[r["unit_id"]]["request_chars"] for r in rs)
        ipc[role] = ((sum(r["input_tokens"] for r in rs) / chars) if chars
                     else S.plan_tokens_per_char(provider_of_model(model)))
        outs = [(r.get("output_tokens") or 0) + ((r.get("thinking_tokens") or 0) if r["provider"] == "google" else 0)
                for r in rs]
        opc[role] = (sum(outs) / len(outs)) if outs else float(S.PLAN_OUT_VISIBLE + S.PLAN_REASONING)
        n[role] = len(rs)
    return ipc, opc, n


def run(P: Paths, dispatch, approval=None, sim=False, max_new_calls=None, log=print, bc=None) -> int:
    if P.frozen.exists():
        log("REFUSED: the judge outputs are frozen")
        return 3
    u0, units = load_units(P)
    roles = current_roles(P)
    recs = read_raw(P.raw)
    guard = Guard(sum(float(r.get("usd") or 0) for r in recs), len(recs), approval, sim, max_new_calls)
    if approval:
        log_guard(P, {"event": "approval past the pause threshold", "approval": approval, "spend": guard.cg.spent_usd})
    st = state_from(recs, roles)
    P.raw.parent.mkdir(parents=True, exist_ok=True)
    if open_batches(P):
        if bc is None:
            log("REFUSED: batches from an earlier run are in flight and no batch client was given")
            return 5
        reattach(P, jobs_for(units, S.DEFAULT_PLAN)[1], roles, guard, bc, st, sim, log)
    plan = json.loads(P.plan.read_text(encoding="utf-8")) if P.plan.exists() else None
    if plan is not None and plan.get("roles") != roles:
        log_guard(P, {"event": "roles changed: recalibrating", "old": plan.get("roles"), "new": roles})
        plan = None
    if plan is None:
        jobs, by = jobs_for(units, S.DEFAULT_PLAN)
        cal = [j for role in sorted(roles) for j in [x for x in jobs if x["phase"] == "A" and x["role"] == role]
               [:S.CALIBRATION_CALLS]]
        log(f"[v1.11] calibration: first {S.CALIBRATION_CALLS} phase-A calls of each judge")
        execute(cal, by, roles, guard, dispatch, st, P, sim, log, bc)
        if guard.stopped:
            log_guard(P, {"event": "stopped during calibration", "reason": guard.stopped, "spend": guard.cg.spent_usd})
            log(f"STOPPED: {guard.stopped}")
            return 4
        recs = read_raw(P.raw)
        ipc, opc, n = measure([r for r in recs if r["plan_phase"] == "A"], roles, by)
        ch = choose_plan(units, roles, ipc, opc, _now_dt())
        plan = {"phase": S.PHASE_ID, "created_utc": _now_dt().isoformat(), "roles": roles,
                "units_sha256": u0["units_file"]["sha256"], "calibration": {"calls": n, "tokens_in_per_char": ipc,
                "output_tokens_per_call": opc}, **ch}
        P.plan.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
        log_guard(P, {"event": "plan written", "reductions": ch["reductions_applied"], "fits": ch["fits"],
                      "projected_usd_with_overhead": ch["steps"][-1]["usd_with_overhead"]})
        log(f"[v1.11] plan: reductions {ch['reductions_applied'] or 'none'}; projected "
            f"${ch['steps'][-1]['usd_with_overhead']:.2f} with overhead; fits={ch['fits']}")
    jobs, by = jobs_for(units, plan["params"])
    for phase in PHASES:
        execute([j for j in jobs if j["phase"] == phase], by, roles, guard, dispatch, st, P, sim, log, bc)
        if guard.stopped:
            break
    recs = read_raw(P.raw)
    spent = sum(float(r.get("usd") or 0) for r in recs)
    todo = sum(1 for j in jobs if not done(st[(j["role"], j["unit_id"], j["pass"])]))
    if guard.stopped:
        log_guard(P, {"event": "stopped", "reason": guard.stopped, "spend": spent, "jobs_left": todo})
        log(f"STOPPED: {guard.stopped} (recorded spend ${spent:.2f}; {todo} jobs left)")
        return 4
    log(f"[v1.11] all jobs done: {len(recs)} calls, recorded spend ${spent:.2f}; next: --freeze")
    return 0


def freeze(P: Paths, log=print) -> int:
    if P.frozen.exists():
        log("REFUSED: already frozen")
        return 3
    if open_batches(P):
        log("REFUSED: batches are still in flight; run --run again to collect them first")
        return 3
    u0, units = load_units(P)
    plan = json.loads(P.plan.read_text(encoding="utf-8"))
    roles = current_roles(P)
    recs = read_raw(P.raw)
    oc = S.outcomes(recs, roles)
    doc = {"phase": S.PHASE_ID, "frozen_utc": _now_dt().isoformat(), "dry_run": P.dry, "raw_file": S.RAW_NAME,
           "raw_sha256": V.sha256(P.raw), "records": len(recs), "roles": roles,
           "batches_file": BATCHES_NAME, "batches_sha256": V.sha256(P.batches) if P.batches.exists() else None,
           "spend_usd_by_mode": {m: sum(float(r.get("usd") or 0) for r in recs if r.get("mode", "sync") == m)
                                 for m in ("batch", "sync")},
           "replacements": json.loads(P.roles.read_text(encoding="utf-8")).get("replacements", []) if P.roles.exists() else [],
           "plan_sha256": V.sha256(P.plan), "plan_params": plan["params"], "units_sha256": u0["units_file"]["sha256"],
           "spend_usd": sum(float(r.get("usd") or 0) for r in recs),
           "outcomes": {f"{r} {p}": dict(Counter(v["status"] for k, v in oc.items() if k[0] == r and k[2] == p))
                        for r in ("J1", "J2") for p in ("main", "repeat")},
           "sampling_parameters_sent": sorted({w for r in recs for w in r.get("sampling_parameters_sent", [])}),
           "served_models": dict(Counter(r.get("served_model") for r in recs))}
    P.frozen.parent.mkdir(parents=True, exist_ok=True)
    P.frozen.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    log(f"[v1.11] frozen: {len(recs)} records, sha256 {doc['raw_sha256'][:16]}..., spend ${doc['spend_usd']:.2f}")
    return 0


# ======================= pre-run checks (decision 7) =======================
def prereg_guard() -> str:
    """Refuse unless the prereg tag is on origin and the anchor file anchors it: the same check as
    score_v1_11.anchor_problems (every field of score_v1_11.ANCHOR_FIELDS, the tag's commit, a
    non-empty osf_deposit), i.e. the record score_v1_11.py --write-anchor writes."""
    r = subprocess.run(["git", "-C", str(S.ROOT), "ls-remote", "--tags", "origin", PREREG_TAG],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"REFUSED: git ls-remote failed: {r.stderr.strip()}")
    shas = dict(reversed(line.split("\t")) for line in r.stdout.splitlines() if "\t" in line)
    ref = f"refs/tags/{PREREG_TAG}"
    if ref not in shas:
        sys.exit(f"REFUSED: tag {PREREG_TAG} not found on origin")
    commit = shas.get(ref + "^{}", shas[ref])
    if not S.ANCHOR_FILE.exists():
        sys.exit(f"REFUSED: anchor file missing: {S.ANCHOR_FILE}")
    anchor = json.loads(S.ANCHOR_FILE.read_text(encoding="utf-8"))
    bad = S.anchor_problems(anchor, commit)
    if bad:
        sys.exit("REFUSED: " + "; ".join(bad))
    return commit


def other_collections() -> list:
    out = subprocess.run(["ps", "-axo", "pid=,command="], capture_output=True, text=True).stdout
    me = str(os.getpid())
    return [line.strip() for line in out.splitlines()
            if OTHER_COLLECTION.search(line) and line.split()[0] != me and "judge_v1_11" not in line]


def sdk_versions() -> dict:
    """Interpreter and provider SDK versions (imports the SDKs: --run only, never --dry-run)."""
    out = {"python": sys.version.split()[0], "executable": sys.executable}
    for m in ("anthropic", "openai", "google.genai"):
        try:
            mod = __import__(m, fromlist=["__version__"])
            out[m] = getattr(mod, "__version__", None)
        except Exception as e:  # noqa: BLE001
            out[m] = f"missing: {type(e).__name__}"
    return out


def require_keys(roles):
    if not os.environ.get("GOOGLE_API_KEY") and os.environ.get("GEMINI_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]
    need = {"anthropic": "ANTHROPIC_API_KEY", "openai": "OPENAI_API_KEY", "google": "GOOGLE_API_KEY"}
    miss = [need[provider_of_model(m)] for m in roles.values() if not os.environ.get(need[provider_of_model(m)])]
    if miss:
        sys.exit(f"ERROR: missing environment variables: {', '.join(sorted(set(miss)))}")


# ======================= dry run (no network, no SDK import) =======================
def _interleave(jobs):
    out = []
    for phase in PHASES:
        a = [j for j in jobs if j["phase"] == phase and j["role"] == "J1"]
        b = [j for j in jobs if j["phase"] == phase and j["role"] == "J2"]
        for i in range(max(len(a), len(b))):
            out += ([a[i]] if i < len(a) else []) + ([b[i]] if i < len(b) else [])
    return out


def ipc_for(roles: dict) -> dict:
    """Planning input tokens per request character for each role's model (S.plan_tokens_per_char)."""
    return {r: S.plan_tokens_per_char(S.provider_of(m)) for r, m in roles.items()}


def design_table(units, run_day: datetime, dec: datetime) -> dict:
    """The budget trade-off of section 7: the projected cost of each design considered, from the
    measured token counts, at the vendors' list prices (batch or synchronous as stated)."""
    full = dict(S.DEFAULT_PLAN)
    j2_all = {**S.DEFAULT_PLAN, "j2_e_share": 1.0}
    rows = [
        ("prepared r1: J1 claude-opus-5-5 + J2 gpt-6-astra, synchronous",
         {"J1": "claude-opus-5-5", "J2": "gpt-6-astra"}, {"J1": False, "J2": False}, full, run_day),
        ("same pair through the batch APIs",
         {"J1": "claude-opus-5-5", "J2": "gpt-6-astra"}, {"J1": True, "J2": True}, full, run_day),
        ("both flagships, batch: J1 claude-fable-5-2 + J2 gpt-6-astra",
         {"J1": "claude-fable-5-2", "J2": "gpt-6-astra"}, {"J1": True, "J2": True}, full, run_day),
        ("CHOSEN, batch: J1 claude-opus-5-5 + J2 gpt-6.1-sol (J2: R, F and 10% of E)",
         {"J1": "claude-opus-5-5", "J2": "gpt-6.1-sol"}, {"J1": True, "J2": True}, full, run_day),
        ("chosen pair after reduction (4): R and F only, plus the Paper B E units (J1); the H1 gate's units",
         {"J1": "claude-opus-5-5", "J2": "gpt-6.1-sol"}, {"J1": True, "J2": True},
         {**S.DEFAULT_PLAN, "e_cap": 24, "j2_e_share": 0.05, "e_half": True, "e_none": True}, run_day),
        ("chosen pair with J2 on every E window too",
         {"J1": "claude-opus-5-5", "J2": "gpt-6.1-sol"}, {"J1": True, "J2": True}, j2_all, run_day),
        ("cheaper J1, batch: J1 claude-sonnet-5-5 + J2 gpt-6.1-sol",
         {"J1": "claude-sonnet-5-5", "J2": "gpt-6.1-sol"}, {"J1": True, "J2": True}, full, run_day),
        ("alternate replaces J2 (gemini-4-argon, synchronous, Dec 1 prices)",
         {"J1": "claude-opus-5-5", "J2": "gemini-4-argon"}, {"J1": True, "J2": False}, full, dec),
        ("alternate replaces J2, after reduction (4)",
         {"J1": "claude-opus-5-5", "J2": "gemini-4-argon"}, {"J1": True, "J2": False},
         {**S.DEFAULT_PLAN, "e_cap": 24, "j2_e_share": 0.05, "e_half": True, "e_none": True}, dec),
        ("alternate replaces J1 (gemini-4-argon, synchronous, Dec 1 prices)",
         {"J1": "gemini-4-argon", "J2": "gpt-6.1-sol"}, {"J1": False, "J2": True}, full, dec),
    ]
    out = {}
    for name, roles, batch, params, when in rows:
        jobs, by = jobs_for(units, params)
        ipc = ipc_for(roles)
        res = {rt: project_jobs(jobs, by, roles, ipc, {r: S.PLAN_OUT_VISIBLE + rt for r in roles}, when, batch)
               for rt in (0, 176, 270, 375)}
        out[name] = {"roles": roles, "batch": batch, "plan_params": params, "priced_at": when.isoformat(),
                     "calls": res[270]["calls"], "calls_by_role": res[270]["calls_by_role"],
                     "tokens_in_by_role": res[270]["tokens_in_by_role"],
                     "usd_with_overhead": {rt: res[rt]["usd_with_overhead"] for rt in res},
                     "usd": {rt: res[rt]["usd"] for rt in res}}
    return out


def guard_simulation(jobs, by, roles, cost_of, approved) -> dict:
    g = S.CostGuard(approved_past_pause=approved)
    sent = 0
    for j in _interleave(jobs):
        u = by[j["unit_id"]]
        m = roles[j["role"]]
        req = S.build_request(u)
        kw = request_kwargs(m, provider_of_model(m), req["system"], req["user"])
        w = worst_usd(m, provider_of_model(m), kw, datetime(2026, 11, 22, 12, tzinfo=UTC), is_batch(m))
        why = g.check(w)
        if why:
            return {"calls_sent": sent, "spend": g.spent_usd, "stopped": why}
        g.reserve(w)
        g.settle(w, cost_of(j, u, m, w))
        sent += 1
    return {"calls_sent": sent, "spend": g.spent_usd, "stopped": None}


def dry_run(P: Paths, log=print) -> int:
    lines = []

    def say(s=""):
        log(s)
        lines.append(s)
    now = _now_dt()
    run_day = datetime(2026, 11, 22, 12, tzinfo=UTC)     # earliest day outside every blackout
    dec = datetime(2026, 12, 1, 12, tzinfo=UTC)
    u0, units = load_units(P)
    roles = dict(DEFAULT_ROLES)
    jobs, by = jobs_for(units, S.DEFAULT_PLAN)
    say(f"judge_v1_11.py --dry-run at {now.isoformat(timespec='seconds')} (no network call, no provider SDK import)")
    say(f"unit table {P.units.name}: {len(units)} rows, sha256 {u0['units_file']['sha256']}")
    say(f"judges: J1 {roles['J1']}, J2 {roles['J2']}; alternate {S.JUDGES['ALT']['model_id']}")
    c = Counter((j["phase"], j["role"]) for j in jobs)
    say("calls by phase x judge: " + ", ".join(f"{p}/{r} {c[(p, r)]}" for p in PHASES for r in ("J1", "J2")))
    say(f"TOTAL planned calls (before invalid-output retries): {len(jobs)}")
    bad, chars = [], Counter()
    for j in jobs:
        u, m = by[j["unit_id"]], roles[j["role"]]
        req = S.build_request(u)
        kw = request_kwargs(m, provider_of_model(m), req["system"], req["user"])
        if sampling_params_sent(kw):
            bad.append(j)
        chars[j["role"]] += u["request_chars"]
    alt_kw = request_kwargs(S.JUDGES["ALT"]["model_id"], "google", "s", "u")
    src = {f.__name__: [w for w in SAMPLING_WORDS if w in inspect.getsource(f)] for f in DISPATCH.values()}
    say(f"sampling parameters in the {len(jobs)} built requests: {'none' if not bad else len(bad)}; "
        f"in the call functions' source: {'none' if not any(src.values()) else src}; alternate request: "
        f"{sampling_params_sent(alt_kw) or 'none'}")
    for k in ("J1", "J2", "ALT"):
        say(f"reasoning parameter {S.JUDGES[k]['model_id']}: {json.dumps(S.JUDGES[k]['reasoning_param'])}; "
            f"max output {S.MAX_OUTPUT_TOKENS} tokens; no tools; prompt-only JSON")
    ipc = ipc_for(roles)
    scen = {}
    for rt in (0, 176, 270, 375):
        scen[rt] = project_jobs(jobs, by, roles, ipc, {r: S.PLAN_OUT_VISIBLE + rt for r in roles}, run_day)
    a = project_jobs(jobs, by, roles, ipc, {r: 0 for r in roles}, run_day)["usd"]
    b = project_jobs(jobs, by, roles, ipc, {r: 1 for r in roles}, run_day)["usd"] - a
    o_star = (S.PLAN_TARGET_USD / S.COST_OVERHEAD - a) / b
    o_cap = (S.HARD_CAP_USD / S.COST_OVERHEAD - a) / b
    say("input tokens (request characters x planning tokens per character: o200k measurement "
        f"{S.O200K_CHARS_PER_TOKEN} characters per token x vendor factor {S.TOKEN_FACTOR}): "
        + ", ".join(f"{r} {roles[r]} {math.ceil(chars[r] * ipc[r]):,}" for r in roles))
    say(f"projection at the vendors' batch list prices (J1 {roles['J1']} ${S.PRICES_BATCH[roles['J1']][0]:g}/"
        f"${S.PRICES_BATCH[roles['J1']][1]:g}, J2 {roles['J2']} ${S.PRICES_BATCH[roles['J2']][0]:g}/"
        f"${S.PRICES_BATCH[roles['J2']][1]:g} per 1M in/out), output = {S.PLAN_OUT_VISIBLE} visible tokens + "
        f"r reasoning tokens per call, x{S.COST_OVERHEAD} overhead (pause ${S.PAUSE_USD:.0f}, cap ${S.HARD_CAP_USD:.0f}):")
    for rt, p in scen.items():
        say(f"  r = {rt:3d}: ${p['usd']:.2f} -> ${p['usd_with_overhead']:.2f} with overhead "
            f"({'under the pause' if p['usd_with_overhead'] <= S.PAUSE_USD else 'under the cap' if p['usd_with_overhead'] <= S.HARD_CAP_USD else 'OVER the cap'})")
    say(f"  break-even: the full design fits under ${S.PAUSE_USD:.0f} with overhead while mean reasoning <= "
        f"{o_star - S.PLAN_OUT_VISIBLE:.0f} tokens per call, under ${S.HARD_CAP_USD:.0f} while <= "
        f"{o_cap - S.PLAN_OUT_VISIBLE:.0f} (input-only cost ${a:.2f})")
    designs = design_table(units, run_day, dec)
    say("design comparison (US$ with overhead at r = 0 / 176 / 270 / 375 reasoning tokens per call):")
    for k, d in designs.items():
        say(f"  {k}: " + " / ".join(f"{d['usd_with_overhead'][rt]:.2f}" for rt in (0, 176, 270, 375))
            + f"  ({d['calls']:,} calls)")
    plan270 = choose_plan(units, roles, ipc, {r: S.PLAN_OUT_VISIBLE + S.PLAN_REASONING for r in roles}, run_day)
    plan375 = choose_plan(units, roles, ipc, {r: S.PLAN_OUT_VISIBLE + 375 for r in roles}, run_day)
    say(f"reductions the binding rule (fit under ${S.PLAN_TARGET_USD:.0f} with overhead) would apply at r = 270: "
        f"{plan270['reductions_applied'] or 'none'}; at r = 375: {plan375['reductions_applied'] or 'none'} "
        f"(binding only at calibration, on measured tokens)")
    worst = defaultdict(float)
    for j in jobs:
        u, m = by[j["unit_id"]], roles[j["role"]]
        req = S.build_request(u)
        kw = request_kwargs(m, provider_of_model(m), req["system"], req["user"])
        worst[m] = max(worst[m], worst_usd(m, provider_of_model(m), kw, run_day, is_batch(m)))
    say(f"largest per-call worst case (request bytes in, {S.MAX_OUTPUT_TOKENS:,} out, batch prices): "
        + ", ".join(f"{m} ${w:.4f}" for m, w in worst.items())
        + f"; a batch of {S.BATCH_MAX_REQUESTS} requests reserves at most "
        + ", ".join(f"{m} ${w * S.BATCH_MAX_REQUESTS:.2f}" for m, w in worst.items()))
    sims = {"every call at its worst case, no approval": guard_simulation(jobs, by, roles, lambda j, u, m, w: w, None),
            "every call at its worst case, approval past the pause": guard_simulation(
                jobs, by, roles, lambda j, u, m, w: w, "sim"),
            "planning cost (r = 270), no approval": guard_simulation(
                jobs, by, roles, lambda j, u, m, w: S.call_usd(
                    m, math.ceil(u["request_chars"] * S.plan_tokens_per_char(provider_of_model(m))),
                    S.PLAN_OUT_VISIBLE + S.PLAN_REASONING, run_day, is_batch(m)), None)}
    for k, v in sims.items():
        say(f"guard simulation, {k}: {v['calls_sent']} calls sent, spend ${v['spend']:.2f}; then: {v['stopped'] or 'all sent'}")
    tag_local = subprocess.run(["git", "-C", str(S.ROOT), "tag", "-l", PREREG_TAG], capture_output=True, text=True).stdout.strip()
    say(f"prereg guard (local check only): tag {PREREG_TAG} {'present locally' if tag_local else 'absent'}; anchor file "
        f"{'present' if S.ANCHOR_FILE.exists() else 'absent'} -> --run would be "
        f"{'checked against origin' if tag_local and S.ANCHOR_FILE.exists() else 'REFUSED'}")
    say("blackout windows (UTC): " + "; ".join(f"{n}: {x:%Y-%m-%d %H:%M} to {y:%Y-%m-%d %H:%M}" for n, x, y in BLACKOUTS)
        + f"; now {'inside: ' + in_blackout(now) if in_blackout(now) else 'outside'}")
    first = next((now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=h) for h in range(1, 24 * 60)
                  if not blackout_within(now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=h))), None)
    say(f"first hour at which a batch may be submitted (no blackout within its {S.BATCH_WINDOW_HOURS} h window): "
        f"{first.isoformat() if first else 'none in 60 days'}")
    oc = other_collections()
    say(f"other collection processes now: {len(oc)}" + (" (" + "; ".join(x[:80] for x in oc) + ")" if oc else ""))
    say(f"raw record {P.raw.name}: {'exists' if P.raw.exists() else 'absent (nothing judged)'}")
    sdk = [m for m in ("anthropic", "openai", "google.genai") if m in sys.modules]
    say(f"provider SDKs imported: {', '.join(sdk) if sdk else 'none'}; nothing sent.")
    P.dry_txt.parent.mkdir(parents=True, exist_ok=True)
    P.dry_txt.write_text("\n".join(lines) + "\n", encoding="utf-8")
    P.cost_json.write_text(json.dumps(V._clean({
        "phase": S.PHASE_ID, "created_utc": now.isoformat(timespec="seconds"), "units_sha256": u0["units_file"]["sha256"],
        "roles": roles, "endpoints": {r: ("batch" if is_batch(m) else "sync") for r, m in roles.items()},
        "prices_usd_per_mtok": S.PRICES, "prices_batch_usd_per_mtok": S.PRICES_BATCH,
        "price_changes": S.PRICE_CHANGES, "price_changes_batch": S.PRICE_CHANGES_BATCH,
        "price_sources": S.PRICE_SOURCES,
        "planning": {"tokens_in": "request characters x tokens per character (o200k measurement, "
                                  "prereg/token_counts_v1_11.json, x vendor factor)",
                     "tokens_per_char": ipc, "o200k_chars_per_token": S.O200K_CHARS_PER_TOKEN,
                     "vendor_token_factor": S.TOKEN_FACTOR, "visible_output_tokens": S.PLAN_OUT_VISIBLE,
                     "reasoning_tokens": S.PLAN_REASONING, "reasoning_basis":
                     "p90 of GPT-6 Astra reasoning tokens at default effort on the program's probes, "
                     "osf/v42/prereg/cost_inputs_v0_42.txt (mean 176, max 375); no judge-task measurement exists",
                     "overhead": S.COST_OVERHEAD, "cache_discount_assumed": False},
        "calls_by_phase_role": {f"{p}/{r}": c[(p, r)] for p in PHASES for r in ("J1", "J2")},
        "scenarios_by_reasoning_tokens": scen,
        "break_even_reasoning_tokens_pause": o_star - S.PLAN_OUT_VISIBLE,
        "break_even_reasoning_tokens_cap": o_cap - S.PLAN_OUT_VISIBLE,
        "input_only_usd": a, "designs": designs, "binding_rule_preview": {"r270": plan270, "r375": plan375},
        "worst_case_per_call": dict(worst), "batch_max_requests": S.BATCH_MAX_REQUESTS, "guard_simulations": sims,
        "cap_usd": S.HARD_CAP_USD, "pause_usd": S.PAUSE_USD, "plan_target_usd": S.PLAN_TARGET_USD,
        "cap_calls": S.HARD_CAP_CALLS}),
        indent=2) + "\n", encoding="utf-8")
    return 0 if not bad and not any(src.values()) and not sdk else 1


# ======================= simulation (synthetic replica, fake judge) =======================
def _h01(*a) -> float:
    return int(hashlib.sha256("|".join(map(str, a)).encode()).hexdigest()[:8], 16) / 0xFFFFFFFF


class FakeJudge:
    """Synthetic stand-in for the providers (dry run only, no network). Valence = a brand latent
    shared by both judges + judge shift + call noise; ~1.5% invalid outputs, ~0.3% served-ID
    mismatches, ~0.1% units that never parse (JUDGE_FAIL)."""

    def __init__(self):
        self.n, self.lock = Counter(), threading.Lock()

    def __call__(self, provider):
        def fn(kw):
            model = kw["model"]
            user = (kw["messages"][0]["content"] if provider == "anthropic" else
                    kw["input"] if provider == "openai" else kw["contents"])
            system = kw.get("system") or kw.get("instructions") or kw.get("config", {}).get("system_instruction", "")
            brand = re.search(r"^TARGET BRAND: (.*)$", user, re.M).group(1)
            with self.lock:
                self.n[(model, user)] += 1
                k = self.n[(model, user)]
            served = model if _h01("served", model, user, k) >= 0.003 else "some-other-model"
            reasoning = int(120 + 360 * _h01("rt", model, user, k))
            tin = (len(system) + len(user)) // 4 + 8
            usage = ({"tokens_out": 60, "tokens_thought": reasoning} if provider == "google" else
                     {"tokens_out": 60 + reasoning, "tokens_thought": reasoning if provider == "openai" else None})
            base = {"served_model": served, "finish_reason": "end_turn", "tokens_in": tin, **usage}
            if _h01("never", model, user) < 0.001 or _h01("invalid", model, user, k) < 0.015:
                return {**base, "text": "Here is my rating: favourable."}
            refers = _h01("ref", user) > 0.01
            lat = _h01("brand", brand) * 2.0 - 0.5
            v = int(round(max(-2.0, min(2.0, lat + (0.2 if model.startswith("gpt") else 0.0)
                                        + (_h01("noise", model, user, k) - 0.5) * 1.4))))
            ev = refers and (v != 0 or _h01("ev", model, user, k) < 0.3)
            v = v if ev else 0
            obj = {"refers_to_brand": refers, "evaluative": ev, "mixed": bool(ev and _h01("mx", model, user, k) < 0.1),
                   "valence": v, "evidence": "synthetic quote" if ev else ""}
            return {**base, "text": json.dumps(obj)}
        return fn


def fake_raw(provider: str, o: dict) -> dict:
    """A FakeJudge output in the provider's raw response format (what the batch results carry)."""
    if provider == "anthropic":
        return {"type": "message", "model": o["served_model"], "stop_reason": o.get("finish_reason"),
                "content": [{"type": "thinking", "thinking": ""}, {"type": "text", "text": o["text"]}],
                "usage": {"input_tokens": o["tokens_in"], "output_tokens": o["tokens_out"],
                          "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0}}
    return {"object": "response", "model": o["served_model"], "status": "completed", "incomplete_details": None,
            "output": [{"type": "reasoning", "summary": []},
                       {"type": "message", "content": [{"type": "output_text", "text": o["text"]}]}],
            "usage": {"input_tokens": o["tokens_in"], "output_tokens": o["tokens_out"],
                      "output_tokens_details": {"reasoning_tokens": o.get("tokens_thought") or 0}}}


class FakeBatchClient:
    """Synthetic batch service (no network): every item is answered by FakeJudge in the provider's
    raw format; ~0.5% of items come back errored; a batch ends at its `polls`-th status call.
    interrupt_after = n: the run is interrupted (guard stop) right after the n-th submission,
    leaving that batch in flight for the next run to re-attach."""

    def __init__(self, fake=None, polls: int = 2, interrupt_after=None):
        self.fake, self.polls, self.interrupt_after = fake or FakeJudge(), polls, interrupt_after
        self.batches, self.n_submits, self.submitted, self.lock = {}, 0, [], threading.Lock()

    def submit(self, provider: str, items) -> str:
        fn = self.fake(provider)
        res = {}
        for cid, kw in items:
            res[cid] = ({"body": None, "error": "errored: synthetic"} if _h01("batch-error", cid) < 0.005
                        else {"body": fake_raw(provider, fn(kw)), "error": None})
        with self.lock:
            self.n_submits += 1
            bid = f"fakebatch_{provider}_{self.n_submits:04d}"
            self.batches[bid] = {"left": self.polls, "res": res}
            self.submitted += [cid for cid, _ in items]
        return bid

    def status(self, provider: str, batch_id: str):
        with self.lock:
            b = self.batches[batch_id]
            b["left"] -= 1
            return b["left"] <= 0, ("ended" if b["left"] <= 0 else "in_progress")

    def results(self, provider: str, batch_id: str) -> dict:
        with self.lock:
            return dict(self.batches[batch_id]["res"])

    def interrupt_now(self) -> bool:
        with self.lock:
            if self.interrupt_after is not None and self.n_submits >= self.interrupt_after:
                self.interrupt_after = None
                return True
        return False


def simulate(log=print) -> int:
    P = Paths(dry=True)
    if not P.units.exists():
        sys.exit("build the replica unit table first: python3 scripts/score_v1_11.py --build-units --dry-run")
    for p in (P.raw, P.plan, P.frozen, P.guard_log, P.roles, P.batches):
        if p.exists():
            p.unlink()
    fake = FakeJudge()
    dispatch = {k: fake(k) for k in ("anthropic", "openai", "google")}
    bc = FakeBatchClient(fake)
    out = []
    rc = run(P, dispatch, sim=True, max_new_calls=1500, log=log, bc=bc)
    out.append(f"step 1 (stop after 1,500 calls): rc {rc}, {len(read_raw(P.raw))} records")
    bc.interrupt_after = bc.n_submits + 1
    rc = run(P, dispatch, sim=True, log=log, bc=bc)
    out.append(f"step 2 (interrupted with a batch in flight): rc {rc}, {len(read_raw(P.raw))} records, "
               f"{len(open_batches(P))} batch(es) in flight")
    rc = run(P, dispatch, sim=True, log=log, bc=bc)
    out.append(f"step 3 (resume: re-attach, then continue; no approval): rc {rc}, {len(read_raw(P.raw))} records")
    if rc == 4:
        rc = run(P, dispatch, approval="simulation only (no real approval)", sim=True, log=log, bc=bc)
        out.append(f"step 4 (resume with approval past the pause): rc {rc}, {len(read_raw(P.raw))} records")
    sent = Counter(bc.submitted)
    out.append(f"batches submitted {bc.n_submits}; batch requests {len(bc.submitted)}; any request id sent twice: "
               f"{any(v > 1 for v in sent.values())}")
    rcf = freeze(P, log)
    recs = read_raw(P.raw)
    plan = json.loads(P.plan.read_text())
    out.append(f"freeze rc {rcf}; spend ${sum(float(r.get('usd') or 0) for r in recs):.2f}; plan reductions "
               f"{plan['reductions_applied'] or 'none'}; guard events: "
               + "; ".join(json.loads(x)["event"] for x in P.guard_log.read_text().splitlines()))
    out.append(f"sampling parameters sent: {sorted({w for r in recs for w in r['sampling_parameters_sent']}) or 'none'}; "
               f"provider SDKs imported: {[m for m in ('anthropic', 'openai', 'google.genai') if m in sys.modules] or 'none'}")
    (S.DRY_OUTDIR / "simulate_judge_v1_11.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    for x in out:
        log(x)
    return 0 if rcf == 0 else 1


def replace(P: Paths, spec: str, reason: str, log=print) -> int:
    role, key = spec.split("=")
    if role not in ("J1", "J2") or key not in S.JUDGES:
        sys.exit("usage: --replace J1=ALT|J2=ALT --reason '<why>'")
    if P.frozen.exists():
        sys.exit("REFUSED: outputs are frozen")
    roles = current_roles(P)
    prev = json.loads(P.roles.read_text())["replacements"] if P.roles.exists() else []
    rec = {"role": role, "from": roles[role], "to": S.JUDGES[key]["model_id"], "reason": reason,
           "utc": _now_dt().isoformat()}
    roles[role] = S.JUDGES[key]["model_id"]
    P.roles.parent.mkdir(parents=True, exist_ok=True)
    P.roles.write_text(json.dumps({"roles": roles, "replacements": prev + [rec]}, indent=2) + "\n")
    log_guard(P, {"event": "judge replaced", **rec})
    log(f"[v1.11] {role}: {rec['from']} -> {rec['to']} ({reason}); its outputs are kept, not used")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="AIAS v1.11 Sentiment Paper A judge acquisition")
    m = ap.add_mutually_exclusive_group(required=True)
    m.add_argument("--dry-run", action="store_true")
    m.add_argument("--simulate", action="store_true")
    m.add_argument("--run", action="store_true")
    m.add_argument("--freeze", action="store_true")
    m.add_argument("--replace", metavar="ROLE=ALT")
    ap.add_argument("--replica", action="store_true", help="--dry-run / --freeze on the synthetic replica")
    ap.add_argument("--reason", default=None)
    ap.add_argument("--approve-past-pause", default=None, metavar="WHO_WHEN",
                    help="Pablo's recorded approval to continue past US$80 of recorded spend")
    ap.add_argument("--no-other-collection", default=None, metavar="WHO_WHEN",
                    help="the operator's attestation that no other paid collection runs on this machine")
    a = ap.parse_args(argv)
    if a.dry_run:
        return dry_run(Paths(dry=a.replica))
    if a.simulate:
        return simulate()
    if a.freeze:
        return freeze(Paths(dry=a.replica))
    if a.replace:
        if not a.reason:
            ap.error("--replace needs --reason")
        return replace(Paths(dry=a.replica), a.replace, a.reason)
    P = Paths(dry=False)
    commit = prereg_guard()
    print(f"prereg guard passed: {PREREG_TAG} -> {commit}")
    b = in_blackout(_now_dt())
    if b:
        sys.exit(f"REFUSED: blackout window ({b})")
    oc = other_collections()
    if oc:
        sys.exit("REFUSED: another collection process is running: " + "; ".join(x[:100] for x in oc))
    if not a.no_other_collection:
        sys.exit('REFUSED: give --no-other-collection "<who, when>" (no other paid collection on this machine)')
    require_keys(current_roles(P))
    log_guard(P, {"event": "run started", "attestation": a.no_other_collection, "prereg_commit": commit,
                  "environment": sdk_versions()})
    return run(P, DISPATCH, approval=a.approve_past_pause, bc=RealBatchClient())


if __name__ == "__main__":
    sys.exit(main())
