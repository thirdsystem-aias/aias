#!/usr/bin/env python3
"""
budget_v0_45.py -- AIAS(TM) v0.45 (t5 repeat wave, pre-registration r0 draft): price table, cost of a call from its
ACTUAL recorded usage, and the collection budget guard (pause at $80, hard stop at $100; Pablo's rule of 2026-11-10).
Hand-edited copy of osf/v42/scripts/budget_v0_42.py (branch v0.42 @ 61515b4). Changed: this docstring; SOURCES (pages
read again for v0.45 on 2026-11-10, about 5:10-5:30 pm US Central: every price below was found unchanged, and Gemini 4
Argon's December price was read on Google's Vertex AI pricing page, since the AI Studio model page now shows only the
introductory price); PROVIDER and TOKEN_PRICES gain the two candidate successors of the v0.23 recognition judge
(claude-sonnet-5-5 $2 / $10, Batch $1 / $5; claude-sonnet-4-6 $3 / $15, Batch $1.50 / $7.50; Anthropic pricing page);
JUDGE_RESERVE_USD 0.50 -> 2.50. Cost functions, worst case and Ledger are unchanged.
Model status read the same day: Anthropic model deprecations page (claude-fable-5-2 Active, not sooner than
2027-11-09; claude-sonnet-4-5-20250929 retires 2026-11-30, recommended replacement claude-sonnet-5-5); OpenAI
gpt-6-astra page and deprecations page (no GPT-6 model deprecated); Google Gemini API deprecations page (gemini-4-argon
not listed) and changelog (gemini-4-argon GA 2026-10-13; newest entry 2026-10-30).

Prices as v0.42 read them on 2026-11-10 (PRE_REGISTRATION_v0_42.md section 4.5, r2), confirmed again for v0.45:
  Anthropic  https://platform.claude.com/docs/about-claude/pricing  (model table, Batch API table, web search
             "$10 USD per 1,000 searches, plus standard token costs for search-generated content")
             https://platform.claude.com/docs/en/build-with-claude/batch-processing  ("All server tools (web search,
             ...) work in batch requests"; "All usage is charged at 50 percent of the standard API prices")
             https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost  (thinking "billed as
             output tokens"; output_tokens is "the inclusive, authoritative total used for billing")
  OpenAI     https://developers.openai.com/api/docs/pricing  (gpt-6-astra $10 / $50; web search "$10.00 / 1k calls"
             plus "Search content tokens billed at model rates")
             https://developers.openai.com/api/docs/guides/reasoning  (reasoning tokens "billed as output tokens")
  Google     https://ai.google.dev/gemini-api/docs/latest-model  (gemini-4-argon $2.00 / $10.00 "through November 30,
             2026", $4.00 / $20.00 from December 1, 2026; output "including thinking")
             https://cloud.google.com/vertex-ai/generative-ai/pricing  (Gemini 4 in the Gemini 3/4 grounding allowance;
             "$14 per 1,000 Grounding Queries" beyond 5,000 free per month -- the free allowance is NOT assumed here)

Cost of one billed request ("usage part"):
  input_tokens x input price + billed output x output price + n_searches x search fee
  billed output = output_tokens (Anthropic, OpenAI: thinking/reasoning included) or output_tokens + thinking_tokens
  (Google: candidates_token_count excludes thoughts). Anthropic Batch API parts use the batch token prices; the
  per-search fee is charged in full in every mode (the pages state the batch discount for tokens only).
A raw record's cost = the sum over its `usage_parts`; a record without `usage_parts` (older format) is costed as one
standard part from its token fields and its S1 search count.

Guard: spent = JUDGE_RESERVE_USD (the v0.23 Phase A recognition judge, Claude Sonnet 4.5, run by the coder after
collection) + the cost of every raw line already written. Before a request is sent, its WORST-CASE cost (WORST below)
is reserved; the request is refused if spent + reservations + worst case > $100 (hard stop), and no new request is
started once spent >= $80 unless the pause has been approved (state file; `acquire_v0_42.py --approve-past-80`).
"""
import json
import threading
from datetime import datetime, timezone
from pathlib import Path

ACCESSED = "2026-11-10"
SOURCES = {
    "anthropic_pricing": "https://platform.claude.com/docs/about-claude/pricing",
    "anthropic_batch": "https://platform.claude.com/docs/en/build-with-claude/batch-processing",
    "anthropic_thinking_billing": "https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost",
    "anthropic_fable_5_2": "https://platform.claude.com/docs/en/models/fable-5-2/overview",
    "openai_pricing": "https://developers.openai.com/api/docs/pricing",
    "openai_gpt_6_astra": "https://developers.openai.com/docs/models/gpt-6-astra",
    "openai_reasoning_billing": "https://developers.openai.com/api/docs/guides/reasoning",
    "openai_batch": "https://developers.openai.com/api/docs/guides/batch",
    "openai_web_search": "https://developers.openai.com/api/docs/guides/tools-web-search",
    "google_gemini_4_argon": "https://ai.google.dev/gemini-api/docs/latest-model",
    "google_gemini_api_pricing": "https://ai.google.dev/gemini-api/docs/pricing",
    "google_vertex_pricing": "https://cloud.google.com/vertex-ai/generative-ai/pricing",
    # added for v0.45 (read 2026-11-10)
    "anthropic_model_deprecations": "https://platform.claude.com/docs/en/about-claude/model-deprecations",
    "anthropic_sonnet_5_5": "https://platform.claude.com/docs/en/models/sonnet-5-5",
    "anthropic_sonnet_5_5_migration": "https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide",
    "openai_deprecations": "https://developers.openai.com/api/docs/deprecations",
    "google_ai_studio_latest_model": "https://aistudio.google.com/docs/latest-model",
    "google_deprecations": "https://ai.google.dev/gemini-api/docs/deprecations",
    "google_changelog": "https://ai.google.dev/gemini-api/docs/changelog",
}
ACCESSED_V45 = "2026-11-10"

PROVIDER = {"claude-fable-5-2": "anthropic", "claude-opus-5-5": "anthropic", "claude-sonnet-4-5": "anthropic",
            "claude-sonnet-5-5": "anthropic", "claude-sonnet-4-6": "anthropic",
            "gpt-6-astra": "openai", "gemini-4-argon": "google"}

# USD per 1M tokens (input, output) by billing mode. "batch" only where the vendor's page lists it for the model.
TOKEN_PRICES = {
    "claude-fable-5-2": {"standard": (8.0, 40.0), "batch": (4.0, 20.0)},
    "claude-opus-5-5": {"standard": (4.0, 20.0), "batch": (2.0, 10.0)},
    "claude-sonnet-4-5": {"standard": (3.0, 15.0), "batch": (1.5, 7.5)},
    "claude-sonnet-5-5": {"standard": (2.0, 10.0), "batch": (1.0, 5.0)},    # successor judge, first candidate
    "claude-sonnet-4-6": {"standard": (3.0, 15.0), "batch": (1.5, 7.5)},    # successor judge, fallback candidate
    "gpt-6-astra": {"standard": (10.0, 50.0), "batch": (5.0, 25.0)},
    "gemini-4-argon": {"standard": (2.0, 10.0)},
}
# Dated price changes: (model, first UTC date of the new price, prices)
PRICE_CHANGES = [("gemini-4-argon", "2026-12-01", {"standard": (4.0, 20.0)})]
SEARCH_FEE = {"anthropic": 0.010, "openai": 0.010, "google": 0.014}  # USD per search / search call / grounding query

BUDGET_CAP_USD = 100.0
PAUSE_AT_USD = 80.0
JUDGE_RESERVE_USD = 2.50          # successor v0.23 judge: (216 parity + 72 t5) calls on up to two candidates x
                                  # (<= 1,500 in, <= 10 out): $0.87 (Sonnet 5.5) + $1.30 (Sonnet 4.6) = $2.17
OUTPUT_CAP = 16384                # max output tokens per request (section 4.4)
WORST = {"S0_input_tokens": 2_000, "S1_input_tokens": 150_000, "searches": {"S0": 0, "S1": 10}}


def prices(model, mode="standard", when_utc=None):
    """(input, output) USD per 1M tokens for `model` in `mode` on the date of `when_utc` (ISO string or None=today)."""
    table = dict(TOKEN_PRICES[model])
    day = (when_utc or datetime.now(timezone.utc).isoformat())[:10]
    for m, first, new in PRICE_CHANGES:
        if m == model and day >= first:
            table.update(new)
    if mode not in table:
        raise KeyError(f"no {mode} price for {model}")
    return table[mode]


def part_cost(model, part, when_utc=None):
    pin, pout = prices(model, part.get("mode", "standard"), when_utc)
    out = (part.get("output_tokens") or 0)
    if PROVIDER[model] == "google":
        out += part.get("thinking_tokens") or 0
    return ((part.get("input_tokens") or 0) * pin + out * pout) / 1e6 + \
        (part.get("n_searches") or 0) * SEARCH_FEE[PROVIDER[model]]


def legacy_part(rec):
    s = rec.get("search") or {}
    n = (s.get("n_searches") or len(s.get("queries") or [])) if rec.get("condition") == "S1" else 0
    return {"mode": "standard", "input_tokens": rec.get("input_tokens"), "output_tokens": rec.get("output_tokens"),
            "thinking_tokens": rec.get("thinking_tokens"), "n_searches": n}


def record_cost(rec):
    """USD of one raw line, from its recorded usage (every billed request of the attempt chain)."""
    model = rec.get("model_requested") or rec.get("model")
    if model not in PROVIDER:
        return 0.0
    parts = rec.get("usage_parts")
    if parts is None:
        parts = [legacy_part(rec)] if rec.get("input_tokens") is not None or rec.get("output_tokens") is not None else []
    return sum(part_cost(model, p, rec.get("started_utc")) for p in parts)


def worst_case(model, cond, mode="standard", when_utc=None):
    """Reservation for one request: input at WORST, output at the cap, WORST searches (practical bounds)."""
    pin, pout = prices(model, mode, when_utc)
    tin = WORST["S1_input_tokens"] if cond == "S1" else WORST["S0_input_tokens"]
    return (tin * pin + OUTPUT_CAP * pout) / 1e6 + WORST["searches"][cond] * SEARCH_FEE[PROVIDER[model]]


class Ledger:
    """Thread-safe spend ledger for one collection. Actual spend is read from the raw file at start and grows by
    the cost of every record written; requests reserve their worst case before they are sent."""

    def __init__(self, raw_path, state_path, cap=BUDGET_CAP_USD, pause_at=PAUSE_AT_USD, judge_reserve=JUDGE_RESERVE_USD):
        self.raw_path, self.state_path = Path(raw_path), Path(state_path)
        self.cap, self.pause_at, self.judge_reserve = cap, pause_at, judge_reserve
        self.lock = threading.Lock()
        self.actual = 0.0
        self.reserved = {}
        self._next = 0
        self.halted = None          # None | "pause" | "stop"
        self.halt_reason = None
        if self.raw_path.exists():
            for line in self.raw_path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    try:
                        self.actual += record_cost(json.loads(line))
                    except (json.JSONDecodeError, KeyError):
                        continue

    # ---- state (pause approval)
    def state(self):
        if self.state_path.exists():
            try:
                return json.loads(self.state_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                return {}
        return {}

    def approved(self, kind="past_80"):
        """kind: 'past_80' (continue after the $80 pause) or 'projection' (continue after the S1 projection pause)."""
        return bool((self.state().get("approvals") or {}).get(kind))

    def approve(self, kind, note):
        if kind not in ("past_80", "projection"):
            raise ValueError(kind)
        st = self.state()
        st.setdefault("approvals", {})[kind] = {"note": note, "utc": datetime.now(timezone.utc).isoformat(),
                                                "spent_at_approval_usd": round(self.spent(), 4)}
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(json.dumps(st, indent=2), encoding="utf-8")
        return st

    def halt(self, kind, reason):
        """Record a pause/stop decided outside reserve() (e.g. the S1 projection)."""
        with self.lock:
            self.halted = kind
            self.halt_reason = reason

    # ---- accounting
    def spent(self):
        return self.judge_reserve + self.actual

    def committed(self):
        with self.lock:
            return self.spent() + sum(self.reserved.values())

    def reserve(self, amount):
        """-> (status, token). status: 'ok' | 'wait' (would fit once in-flight requests settle) | 'pause' | 'stop'."""
        with self.lock:
            if self.halted:
                return self.halted, None
            if self.spent() >= self.pause_at and not self.approved():
                self.halted, self.halt_reason = "pause", f"spend ${self.spent():.2f} >= ${self.pause_at:.0f}"
                return "pause", None
            if self.spent() + sum(self.reserved.values()) + amount > self.cap:
                if self.reserved and self.spent() + amount <= self.cap:
                    return "wait", None
                self.halted, self.halt_reason = "stop", f"spend ${self.spent():.2f} + worst case would pass ${self.cap:.0f}"
                return "stop", None
            self._next += 1
            self.reserved[self._next] = amount
            return "ok", self._next

    def fit(self, per_request, n):
        """Largest k <= n whose k worst cases fit under the cap now; reserves them as one token. -> (status, k, token)."""
        with self.lock:
            if self.halted:
                return self.halted, 0, None
            if self.spent() >= self.pause_at and not self.approved():
                self.halted, self.halt_reason = "pause", f"spend ${self.spent():.2f} >= ${self.pause_at:.0f}"
                return "pause", 0, None
            room = self.cap - self.spent() - sum(self.reserved.values())
            k = min(n, int(room // per_request)) if per_request > 0 else n
            if k <= 0:
                if self.reserved and self.cap - self.spent() >= per_request:
                    return "wait", 0, None
                self.halted, self.halt_reason = "stop", f"spend ${self.spent():.2f} + worst case would pass ${self.cap:.0f}"
                return "stop", 0, None
            self._next += 1
            self.reserved[self._next] = k * per_request
            return "ok", k, self._next

    def settle(self, token, actual_usd):
        """Release a reservation (token may be None) and add the actual cost of what was written."""
        with self.lock:
            if token is not None:
                self.reserved.pop(token, None)
            self.actual += actual_usd

    def summary(self):
        with self.lock:
            return {"actual_calls_usd": round(self.actual, 4), "judge_reserve_usd": self.judge_reserve,
                    "spent_usd": round(self.spent(), 4), "reserved_in_flight_usd": round(sum(self.reserved.values()), 4),
                    "pause_at_usd": self.pause_at, "cap_usd": self.cap, "approved_past_80": self.approved("past_80"),
                    "approved_projection": self.approved("projection"), "halted": self.halted,
                    "halt_reason": self.halt_reason}
