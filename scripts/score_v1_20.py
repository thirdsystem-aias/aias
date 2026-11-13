#!/usr/bin/env python3
"""AIAS v1.20 (proposed id) — successor re-scoring rule for v1.11's judge replies. DRAFT r0, NOT LOCKED.

PRE_REGISTRATION_v1_20.md (osf/methodology/v1_20/prereg/) defines the study. This module holds the one
rule it changes and nothing else:

  A judge reply counts when it holds exactly one complete top-level JSON object and that object passes
  v1.11's own validation unchanged (score_v1_11.parse_judge_output: exactly the five keys, types,
  consistency rules, the 20-word evidence flag). Text before or after the object is ignored. Zero
  objects, two or more objects, an empty reply, a reply whose recorded finish reason shows the output
  cap, and a served-model mismatch are invalid (the last two as v1.11 states them).

Per unit, the stored attempts are read in v1.11's order and the first reply that counts is the
judgement (outcomes); everything downstream (JUDGE_FAIL 2% rule, Stage J, Stage C) is v1.11's code.
classify() describes a reply's format for format counts only; it never reads a valence.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import score_v1_11 as S  # noqa: E402  v1.11's locked scorer (tag v1.11-prereg-r1), imported unchanged

PHASE_ID = "v1.20"
STATUS = "r0 draft (2026-11-13), not locked"
SUCCESSOR_OF = "v1.11"
SUCCESSOR_OF_TAG = S.PREREG_TAG  # v1.11-prereg-r1

_DECODER = json.JSONDecoder()  # the decoder behind json.loads, with json.loads' defaults (as v1.11's parser)
CAP_REASONS = frozenset({"max_tokens", "max_output_tokens", "length"})
FENCE_TAIL = re.compile(r"```[A-Za-z0-9_-]*$")  # classify() only: a fence opening right before the object


class ReplyInvalid(S.JudgeOutputError):
    """Invalid under the v1.20 rule (a JudgeOutputError, so v1.11's handling applies unchanged)."""


def cut_by_cap(finish_reason) -> bool:
    """True when the recorded finish reason says the output cap ended the reply. Anthropic
    'max_tokens'; OpenAI Responses 'incomplete:max_output_tokens' (as judge_v1_11 records it);
    Gemini 'MAX_TOKENS' or 'FinishReason.MAX_TOKENS'; chat-style 'length'. Case-insensitive; the
    part after the last ':' or '.' is read."""
    if finish_reason is None:
        return False
    tail = re.split(r"[.:]", str(finish_reason).strip())[-1].strip().lower()
    return tail in CAP_REASONS


def top_level_objects(text: str) -> List[Tuple[int, int, dict]]:
    """Every complete top-level JSON object in `text`, left to right, as (start, end, object).

    The scan stops at each '{' that is not inside an object already found and tries the standard
    decoder there (json.JSONDecoder().raw_decode). A success is one object, and the scan resumes after
    its last character, so objects nested inside it, and braces inside its strings, are never counted
    again. A failure (not valid JSON from that '{', e.g. cut off or malformed) moves the scan to the
    next '{'. Arrays, numbers and strings outside an object are surrounding text."""
    out: List[Tuple[int, int, dict]] = []
    i = 0
    while True:
        i = text.find("{", i)
        if i < 0:
            return out
        try:
            obj, end = _DECODER.raw_decode(text, i)
        except (json.JSONDecodeError, RecursionError):
            i += 1
            continue
        out.append((i, end, obj))  # a JSON value that starts with '{' is always an object (dict)
        i = end


def parse_reply(raw: str) -> dict:
    """The v1.20 rule on one reply text. Returns v1.11's parsed object (with its
    `evidence_over_limit` flag) or raises ReplyInvalid / S.JudgeOutputError."""
    text = raw or ""
    if not text.strip():
        raise ReplyInvalid("empty reply")
    objs = top_level_objects(text)
    if not objs:
        raise ReplyInvalid("no complete JSON object")
    if len(objs) > 1:
        raise ReplyInvalid(f"{len(objs)} complete JSON objects (exactly one required)")
    start, end, _ = objs[0]
    return S.parse_judge_output(text[start:end])  # v1.11's checks, unchanged, on the object's own text


def record_judgement(rec: dict) -> Optional[dict]:
    """The judgement one stored call record yields under v1.20, or None. As score_v1_11.outcomes: only
    status 'ok' with the served model accepted can yield one; plus the output-cap rule of v1.11 §4.2."""
    if rec.get("status") != "ok" or not rec.get("served_ok"):
        return None
    if cut_by_cap(rec.get("finish_reason")):
        return None
    try:
        return parse_reply(rec.get("text") or "")
    except S.JudgeOutputError:
        return None


def outcomes(records: List[dict], roles: Dict[str, str]) -> Dict[Tuple[str, str, str], dict]:
    """score_v1_11.outcomes with the v1.20 rule in place of v1.11's parser; nothing else changes.
    Records of the model assigned to each role; per (role, unit_id, pass) the stored attempts in
    (attempt, started_utc) order; API errors skipped; the first record that yields a judgement ->
    VALID (that judgement is scored); otherwise >= 1 + MAX_PARSE_RETRIES invalid responses ->
    JUDGE_FAIL; otherwise UNJUDGED."""
    g: Dict[tuple, List[dict]] = defaultdict(list)
    for r in records:
        if roles.get(r["role"]) == r["judge_model"]:
            g[(r["role"], r["unit_id"], r["pass"])].append(r)
    out = {}
    for k, rs in g.items():
        rs = sorted(rs, key=lambda r: (int(r["attempt"]), r.get("started_utc") or ""))
        valid, invalid = None, 0
        for r in rs:
            if r.get("status") not in ("ok", "empty"):
                continue
            parsed = record_judgement(r)
            if parsed is not None:
                valid = (r, parsed)
                break
            invalid += 1
        if valid:
            out[k] = {"status": S.VALID, "out": valid[1], "attempts": len(rs),
                      "served_model": valid[0].get("served_model"), "attempt_used": int(valid[0]["attempt"])}
        elif invalid >= 1 + S.MAX_PARSE_RETRIES:
            out[k] = {"status": S.FAIL, "out": None, "attempts": len(rs)}
        else:
            out[k] = {"status": S.UNJUDGED, "out": None, "attempts": len(rs)}
    return out


def classify(raw: str) -> dict:
    """Format of one reply, for format counts only (no valence is read or returned).
    shape: empty | no_object | several_objects | bare | text_before | text_after | text_before_and_after,
    read after a code fence around the single object is set aside (fenced = True; '```json' or '```'
    directly before it and '```' directly after it). v111_valid: v1.11's parser on the whole reply.
    v120_valid: the v1.20 rule on the reply text (finish reason and served model are checked by
    record_judgement)."""
    text = raw or ""
    res = {"shape": None, "fenced": False, "n_objects": 0, "v111_valid": False, "v120_valid": False,
           "object_checks": None}
    try:
        S.parse_judge_output(text)
        res["v111_valid"] = True
    except S.JudgeOutputError:
        pass
    if not text.strip():
        res["shape"] = "empty"
        return res
    objs = top_level_objects(text)
    res["n_objects"] = len(objs)
    if not objs:
        res["shape"] = "no_object"
        return res
    if len(objs) > 1:
        res["shape"] = "several_objects"
        return res
    start, end, _ = objs[0]
    before, after = text[:start].strip(), text[end:].strip()
    m = FENCE_TAIL.search(before)
    if m and after.startswith("```"):
        res["fenced"] = True
        before, after = before[:m.start()].strip(), after[3:].strip()
    if not before and not after:
        res["shape"] = "bare"
    elif before and not after:
        res["shape"] = "text_before"
    elif after and not before:
        res["shape"] = "text_after"
    else:
        res["shape"] = "text_before_and_after"
    try:
        S.parse_judge_output(text[start:end])
        res["object_checks"] = "pass"
        res["v120_valid"] = True
    except S.JudgeOutputError as e:
        res["object_checks"] = "fail: " + str(e).split(":")[0]
    return res
