#!/usr/bin/env python3
"""
stoprule_v0_40.py -- AIAS(TM) v0.40: the length-limit stop rule inside the collection (PRE_REGISTRATION_v0_40.md
section 4.7), the per-answer assessment shared with the pre-lock check (section 4.8, prelock_check_v0_40.py), and the
flags behind the declared handling of answers at the limit or with heavy thinking (section 5.9).

Programme rule (the pre-registrant, 2026-11-12, 11:36 pm CT): no lock while any model's answer, under the study's own
call settings, stops at the length limit before naming a brand; an answer whose thinking uses half the limit needs
pre-registered handling; every pre-registration not yet locked that collects answers also applies the test as a stop
rule inside its collection.

Per answer (one raw line with status "ok" or "empty"; an "error" line carries no answer and is skipped):
  at_limit          the finish reason is the provider's length stop: Anthropic "max_tokens"; OpenAI "length" (Chat
                    Completions) or "incomplete:max_output_tokens" (Responses); Google MAX_TOKENS, also with an enum
                    prefix ("FinishReason.MAX_TOKENS"). With no finish reason recorded: billed output tokens (Google:
                    candidates + thoughts) >= the limit. With neither, the answer is "unassessable".
  named             distinct registry brands the study's own matcher finds in the answer text (v0.40:
                    score_v0_40.code_answer over the frozen registry, as the primary coding counts them: bare
                    ambiguous aliases, D11, do not count)
  cut_before_brand  at_limit and named == 0, or an empty first answer that stopped at the limit and was re-sent
                    (its finish reason is kept as first_attempt_finish_reason)  -> the stop rule's trigger
  cut_after_brand   at_limit and named >= 1
  thinking          the provider's own count (Google thoughts_token_count, OpenAI reasoning_tokens); for a model that
                    may think under the study's settings but reports no separate count (Claude Fable 5.2, provider
                    defaults), its total output tokens, an upper bound; 0 when no count is reported for a call that
                    sends no thinking setting to a model without default thinking
  think_half        thinking >= half the limit (1,024 of 2,048 in the legacy arm; 8,192 of 16,384 in the current arm)

Stop rule: the first cut_before_brand answer of a model slot pauses that slot: no further request for it, in any block
or condition; every other slot goes on. Synchronous slots stop before their next request; Claude Fable 5.2's answers
arrive one Message Batch at a time, so its pause takes effect from its next batch. Every trigger is journaled
(osf/v40/data/v40_stoprule.jsonl) and printed for the pre-registrant. A paused slot stays paused across restarts until
`acquire_v0_40.py --resume-model SLOT NOTE` journals his decision. Slots in EXEMPT (M5X, the reported-only pass at the
v0.39 setting; PENDING PABLO, section 9 item 7) are assessed and journaled but never paused.
"""
import json
import sys
import threading
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIMIT = {"L": 2048, "C": 16384}                       # = acquire_v0_40.LEGACY_MAX_TOKENS, CURRENT_MAX_TOKENS (test)
EXEMPT = frozenset({"M5X"})                           # PENDING PABLO (pre-registration section 9, item 7)
MAY_THINK_UNREPORTED = frozenset({"claude-fable-5-2"})
FLAGS = ("at_limit", "cut_before_brand", "cut_after_brand", "think_half", "unassessable")


def _now():
    return datetime.now(timezone.utc).isoformat()


def is_length_stop(finish_reason):
    """True / False from a recorded finish reason; None when none was recorded."""
    if finish_reason is None or not str(finish_reason).strip():
        return None
    s = str(finish_reason).strip().lower()
    return s.split(".")[-1] in ("max_tokens", "length") or s.endswith("max_output_tokens")


def arm_of(rec):
    return "C" if rec.get("arm") == "C" or str(rec.get("slot") or "").startswith("C") else "L"


def limit_of(rec):
    return LIMIT[arm_of(rec)]


def thinking_count(rec):
    """(thinking tokens, True when the figure is the total output used as an upper bound)."""
    t = rec.get("thinking_tokens")
    if t is not None:
        return int(t), False
    if (rec.get("model_requested") or rec.get("model")) in MAY_THINK_UNREPORTED:
        return int(rec.get("output_tokens") or 0), True
    return 0, False


def at_limit(rec, limit=None):
    """True / False; None when neither a finish reason nor output tokens were recorded (unassessable)."""
    limit = limit or limit_of(rec)
    stop = is_length_stop(rec.get("finish_reason"))
    if stop is not None:
        return stop
    out = rec.get("output_tokens")
    if out is None:
        return None
    billed = int(out) + (int(rec.get("thinking_tokens") or 0) if rec.get("provider") == "google" else 0)
    return billed >= limit


def assess(rec, named_fn, limit=None):
    """Assessment of one raw line; None for a line without an answer (status 'error')."""
    if rec.get("status") not in ("ok", "empty"):
        return None
    limit = limit or limit_of(rec)
    text = rec.get("text") or ""
    named = named_fn(text) if text.strip() else 0
    lim = at_limit(rec, limit)
    th, bound = thinking_count(rec)
    # a synchronous call re-sends an empty answer once and records the second; an empty first answer that stopped at
    # the limit is itself an answer cut before any brand (acquire_v0_40.send_call keeps its finish reason)
    first_cut = bool(is_length_stop(rec.get("first_attempt_finish_reason")))
    return {"call_id": rec.get("call_id"), "slot": rec.get("slot"), "condition": rec.get("condition"),
            "model": rec.get("model_requested"), "finish_reason": rec.get("finish_reason"), "limit": limit,
            "output_tokens": rec.get("output_tokens"), "thinking": th, "thinking_upper_bound": bound,
            "named": named, "at_limit": lim, "unassessable": lim is None, "empty_first_cut": first_cut,
            "cut_before_brand": (bool(lim) and named == 0) or first_cut, "cut_after_brand": bool(lim) and named > 0,
            "think_half": 2 * th >= limit}


def v40_named_fn():
    """Number of distinct registry entities (units, ghosts, controls) in a text that the primary coding counts, by
    score_v0_40's own matcher over the frozen registry. Bare ambiguous aliases (D11; e.g. "United" in "United States")
    do not count, so the rule errs toward triggering."""
    sys.path.insert(0, str(HERE))
    import score_v0_40 as S
    units, subjects, _ = S.load_registry()
    subjects = subjects + S.switch_controls(subjects)
    matchers = S.build_matchers(units, subjects)
    return lambda text: len({m["entity"] for m in S.code_answer(text, matchers, {}) if not m["ambiguous"]})


class StopRule:
    """Thread-safe: observe() is called by the writer of every model slot's worker."""

    def __init__(self, named_fn, journal=None, exempt=EXEMPT, log=print):
        self.named_fn, self.exempt, self.log = named_fn, frozenset(exempt), log
        self.journal = Path(journal) if journal else None
        self.lock = threading.Lock()
        self.paused = {}
        self.counts = defaultdict(Counter)
        for ev in self.events():
            if ev.get("event") == "trigger":
                self.paused.setdefault(ev["slot"], ev)
            elif ev.get("event") == "resume":
                self.paused.pop(ev["slot"], None)

    def events(self):
        if not self.journal or not self.journal.exists():
            return []
        out = []
        for line in self.journal.read_text(encoding="utf-8").splitlines():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return out

    def _append(self, ev):
        if self.journal:
            self.journal.parent.mkdir(parents=True, exist_ok=True)
            with open(self.journal, "a", encoding="utf-8") as f:
                f.write(json.dumps(ev, ensure_ascii=False) + "\n")

    def observe(self, rec):
        a = assess(rec, self.named_fn)
        if a is None:
            return None
        with self.lock:
            c = self.counts[f"{a['slot']}|{a['condition']}"]
            c["answers"] += 1
            for k in FLAGS:
                c[k] += int(bool(a[k]))
            if a["cut_before_brand"]:
                kind = "exempt" if a["slot"] in self.exempt else "trigger"
                self._append(dict(a, event=kind, utc=_now()))
                if kind == "trigger" and a["slot"] not in self.paused:
                    self.paused[a["slot"]] = a
                    self.log(f"STOP RULE (section 4.7): {a['call_id']} stopped at the length limit "
                             f"({a['finish_reason']}, {a['output_tokens']} output tokens) before naming a brand; "
                             f"slot {a['slot']} paused; report to the pre-registrant")
            elif a["cut_after_brand"] or a["think_half"] or a["unassessable"]:
                self._append(dict(a, event="flag", utc=_now()))
        return a

    def is_paused(self, slot):
        with self.lock:
            return slot in self.paused

    def paused_slots(self):
        with self.lock:
            return sorted(self.paused)

    def resume(self, slot, note):
        """The pre-registrant's decision to resume a paused slot unchanged (journaled; a DEVIATIONS entry)."""
        ev = {"event": "resume", "slot": slot, "note": note, "utc": _now()}
        with self.lock:
            self._append(ev)
            self.paused.pop(slot, None)
        return ev

    def wrap(self, write):
        """Writer that assesses every line right after it is written."""
        if getattr(write, "_stoprule", None) is self:
            return write

        def w(rec):
            write(rec)
            self.observe(rec)
        w._stoprule = self
        return w

    def summary(self):
        with self.lock:
            return {"paused": sorted(self.paused), "exempt": sorted(self.exempt),
                    "counts": {k: dict(v) for k, v in sorted(self.counts.items())}}
