#!/usr/bin/env python3
"""AIAS v1.20 — successor re-scoring of v1.11's judge replies. Final text (r1), locked by tag v1.20-prereg-r1.

PRE_REGISTRATION_v1_20.md (osf/methodology/v1_20/prereg/) defines the study. This module holds the
one rule it changes and the stages that apply it; everything else is v1.11's locked code, imported:

  A judge reply counts when it holds exactly one complete top-level JSON object and that object passes
  v1.11's own validation unchanged (score_v1_11.parse_judge_output: exactly the five keys, types,
  consistency rules, the 20-word evidence flag). Text before or after the object is ignored. Zero
  objects, two or more objects (switch Q4), an empty reply, a reply whose recorded finish reason shows
  the output cap (switch Q3) and a served-model mismatch are invalid.

Per unit, the stored attempts are read in v1.11's order and the first reply that counts is the
judgement (outcomes; switch Q2 can make v1.11's own judgement primary instead). The JUDGE_FAIL 2% rule,
S, H1-H9, the sensitivities and the descriptives are v1.11's functions on these outcomes.

The six switches of section 15 are in osf/methodology/v1_20/prereg/config_v1_20.json (one 'value'
each, set to Pablo's answers of 2026-11-14 to questions 1-6; DECIDED below).

Modes (repository root; system Python or the venv, PYTHONDONTWRITEBYTECODE=1):
  --stage J        after v1.11's --freeze and v1.11's own Stage J: outcomes under the rule, JUDGE_FAIL
                   check (halt above 2%), S, H1, self-consistency, S-ATT, comparison with v1.11.
                   Reads no P, C* or Ranking value.
  --stage C        after Stage J (and after v1.11's Stage C when v1.11's Stage J passed): P, C*, R*
                   -> H2-H9, v1.11's sensitivities, S-ATT, S-CUT, S-CUT-M, descriptives.
  --dry-run        either stage on the synthetic dry-run work folder (dryrun/work/, built by
                   osf/methodology/v1_20/dryrun/build_dryrun_v1_20.py); --draws N lowers the bootstrap
                   and permutation draws for a dry run only.
  --lock-manifest  content lock, last step: prereg/LOCK_MANIFEST_v1_20.sha256 over LOCK_FILES.
  --write-anchor --osf-deposit "<where>"
                   after the tag is pushed: anchor/git_anchor_v1_20.json (v1.11's anchor schema).
No model call in this file. --write-anchor runs git ls-remote against origin.
classify() describes a reply's format for format counts only; it never reads a valence.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import score_v1_11 as S  # noqa: E402  v1.11's locked scorer (tag v1.11-prereg-r1), imported unchanged

V = S.V                  # v1.10's locked module, as v1.11 imports it
Halt = S.Halt

# ======================================================================================
# 0. SWITCHES (Pablo's answers to questions 1-6, 2026-11-14; PRE_REGISTRATION_v1_20.md section 15)
# ======================================================================================
ROOT = S.ROOT
V120 = "osf/methodology/v1_20"
CONFIG_FILE = ROOT / V120 / "prereg/config_v1_20.json"
SWITCH_OPTIONS = {
    "Q1_study_id": ("v1.20", "v1.11-successor"),
    "Q2_scored_attempt": ("first_counting", "v1_11_first"),
    "Q3_cap_cut_reply_invalid": (True, False),
    "Q4_reject_identical_objects": (True, False),
    "Q5_cut_answers": ("keep_r4", "keep_r6", "drop_r4", "drop_r6"),
    "Q6_case_b_result": (True, False),
}
DECIDED = {"Q1_study_id": "v1.20", "Q2_scored_attempt": "first_counting", "Q3_cap_cut_reply_invalid": True,
           "Q4_reject_identical_objects": True, "Q5_cut_answers": "keep_r4", "Q6_case_b_result": True}


def _same_option(v, o) -> bool:
    return type(v) is type(o) and v == o          # True is not 1, "4" is not 4


def load_switches(path: Path = CONFIG_FILE) -> dict:
    """The switch values of config_v1_20.json; refuses a missing switch or a value outside its options."""
    doc = json.loads(Path(path).read_text(encoding="utf-8"))["switches"]
    sw = {}
    for k, opts in SWITCH_OPTIONS.items():
        if k not in doc:
            raise ValueError(f"config: switch {k} missing")
        v = doc[k]["value"]
        if not any(_same_option(v, o) for o in opts):
            raise ValueError(f"config: {k} = {v!r} is not one of {opts}")
        sw[k] = v
    extra = sorted(set(doc) - set(SWITCH_OPTIONS))
    if extra:
        raise ValueError(f"config: unknown switches {extra}")
    return sw


SW = load_switches()
PHASE_ID = SW["Q1_study_id"]
PREREG_TAG = f"{PHASE_ID}-prereg-r1"
BRANCH = "sentiment-successor"
STATUS = "r1, final (Pablo's answers of 2026-11-14); locked by tag v1.20-prereg-r1"
SUCCESSOR_OF = "v1.11"
SUCCESSOR_OF_TAG = S.PREREG_TAG  # v1.11-prereg-r1


def r_floor(sw: Optional[dict] = None) -> int:
    """Recognition-score floor wherever cut answers are dropped (switch Q5: _r4 or _r6)."""
    return 4 if (sw or SW)["Q5_cut_answers"].endswith("_r4") else 6


def primary_drops_cut(sw: Optional[dict] = None) -> bool:
    return (sw or SW)["Q5_cut_answers"].startswith("drop")


# ======================================================================================
# 1. THE RULE (section 3)
# ======================================================================================
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


def canonical(obj) -> str:
    """JSON-type-exact canonical form (true and 1 differ; key order ignored), for switch Q4."""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def parse_reply(raw: str, sw: Optional[dict] = None) -> dict:
    """The v1.20 rule on one reply text. Returns v1.11's parsed object (with its
    `evidence_over_limit` flag) or raises ReplyInvalid / S.JudgeOutputError."""
    sw = sw or SW
    text = raw or ""
    if not text.strip():
        raise ReplyInvalid("empty reply")
    objs = top_level_objects(text)
    if not objs:
        raise ReplyInvalid("no complete JSON object")
    if len(objs) > 1:
        same = len({canonical(o) for _, _, o in objs}) == 1
        if sw["Q4_reject_identical_objects"] or not same:
            raise ReplyInvalid(f"{len(objs)} complete JSON objects (exactly one required)")
    start, end, _ = objs[0]
    return S.parse_judge_output(text[start:end])  # v1.11's checks, unchanged, on the object's own text


def record_judgement(rec: dict, sw: Optional[dict] = None) -> Optional[dict]:
    """The judgement one stored call record yields under v1.20, or None. As score_v1_11.outcomes: only
    status 'ok' with the served model accepted can yield one; plus the output-cap rule (switch Q3)."""
    sw = sw or SW
    if rec.get("status") != "ok" or not rec.get("served_ok"):
        return None
    if sw["Q3_cap_cut_reply_invalid"] and cut_by_cap(rec.get("finish_reason")):
        return None
    try:
        return parse_reply(rec.get("text") or "", sw)
    except S.JudgeOutputError:
        return None


def _grouped(records: List[dict], roles: Dict[str, str]) -> Dict[tuple, List[dict]]:
    g: Dict[tuple, List[dict]] = defaultdict(list)
    for r in records:
        if roles.get(r["role"]) == r["judge_model"]:
            g[(r["role"], r["unit_id"], r["pass"])].append(r)
    return {k: sorted(rs, key=lambda r: (int(r["attempt"]), r.get("started_utc") or "")) for k, rs in g.items()}


def outcomes(records: List[dict], roles: Dict[str, str], sw: Optional[dict] = None) -> Dict[Tuple[str, str, str], dict]:
    """score_v1_11.outcomes with the v1.20 rule in place of v1.11's parser; nothing else changes.
    Records of the model assigned to each role; per (role, unit_id, pass) the stored attempts in
    (attempt, started_utc) order; API errors skipped; the first record that yields a judgement ->
    VALID (that judgement is scored); otherwise >= 1 + MAX_PARSE_RETRIES invalid responses ->
    JUDGE_FAIL; otherwise UNJUDGED."""
    out = {}
    for k, rs in _grouped(records, roles).items():
        valid, invalid = None, 0
        for r in rs:
            if r.get("status") not in ("ok", "empty"):
                continue
            parsed = record_judgement(r, sw)
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


def v111_attempts_used(records: List[dict], roles: Dict[str, str]) -> Dict[tuple, int]:
    """The attempt v1.11's own outcomes() scores for each VALID (role, unit, pass): the first record
    that is status 'ok', served-model accepted and parses under v1.11's parser (as its loop)."""
    out = {}
    for k, rs in _grouped(records, roles).items():
        for r in rs:
            if r.get("status") != "ok" or not r.get("served_ok"):
                continue
            try:
                S.parse_judge_output(r.get("text") or "")
            except S.JudgeOutputError:
                continue
            out[k] = int(r["attempt"])
            break
    return out


def outcomes_v111_first(oc111: dict, oc120: dict) -> dict:
    """S-ATT: v1.11's own judgement wherever v1.11's rule yields one; the v1.20 rule only where v1.11
    has JUDGE_FAIL or UNJUDGED (section 4)."""
    out = {}
    for k in set(oc111) | set(oc120):
        a = oc111.get(k)
        out[k] = a if (a is not None and a["status"] == S.VALID) else oc120.get(k, a)
    return out


def classify(raw: str) -> dict:
    """Format of one reply, for format counts only (no valence is read or returned).
    shape: empty | no_object | several_objects | bare | text_before | text_after | text_before_and_after,
    read after a code fence around the single object is set aside (fenced = True; '```json' or '```'
    directly before it and '```' directly after it). v111_valid: v1.11's parser on the whole reply.
    v120_valid: the v1.20 rule on the reply text with the decided settings (finish reason and served model
    are checked by record_judgement)."""
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


# ======================================================================================
# 2. PATHS, RUN CONTEXT, INPUT CHECKS
# ======================================================================================
PREREG_DIR = ROOT / V120 / "prereg"
SCOPING_DIR = ROOT / V120 / "scoping"
OUTDIR = ROOT / V120 / "outputs"
ANCHOR_FILE = ROOT / V120 / "anchor/git_anchor_v1_20.json"
CUT_CSV = SCOPING_DIR / "cut_units_v1_20.csv"
CUT_JSON = SCOPING_DIR / "cut_units_v1_20.json"
DRY_DIR = ROOT / V120 / "dryrun"
DRY_WORK = DRY_DIR / "work"                       # synthetic; built by dryrun/build_dryrun_v1_20.py; not committed
DRY_REPLICA = DRY_WORK / "replica"                # v1.11's synthetic input replica (v1.11's own builder)
DRY_MANIFEST = DRY_WORK / "INPUTS_MANIFEST_dryrun_v1_11.json"
DRY_V111_OUT = DRY_WORK / "v1_11_outputs"         # v1.11's dry-run U0 + the synthetic judge records
DRY_OUTDIR = DRY_WORK / "v1_20_outputs"
DRY_CUT_CSV = DRY_WORK / "cut_units_dryrun.csv"
DRY_CUT_JSON = DRY_WORK / "cut_units_dryrun.json"
STAGE_J_NAME = "stage_j_v1_20.json"
OUTCOMES_NAME = "unit_outcomes_v1_20.csv"
VERDICTS_NAME = "v1_20_verdicts.json"
COMPARISON_NAME = "comparison_v1_11_v1_20.json"
V111_LOCK_MANIFEST = "osf/methodology/v1_11/prereg/LOCK_MANIFEST_v1_11.sha256"
V111_IMPORTED = ("scripts/score_v1_11.py", "scripts/score_v1_10.py")
ROLES = ("J1", "J2")
RULE_TEXT = ("a judge reply counts when it holds exactly one complete JSON object that passes v1.11's checks; "
             "text around it, code fences included, is ignored (PRE_REGISTRATION_v1_20.md section 3)")


class Run:
    """Where a v1.20 stage reads v1.11's records (v1.11's own context and paths) and writes its own.
    Real runs read v1.11's frozen records at their v1.11 paths in this tree."""

    def __init__(self, dry: bool = False):
        self.dry = dry
        self.ctx = (S.make_ctx(True, root=DRY_REPLICA, manifest=DRY_MANIFEST, outdir=DRY_V111_OUT) if dry
                    else S.make_ctx(False))
        self.out = DRY_OUTDIR if dry else OUTDIR
        self.cut_csv, self.cut_json = (DRY_CUT_CSV, DRY_CUT_JSON) if dry else (CUT_CSV, CUT_JSON)


def v111_integrity(root: Path = ROOT) -> List[str]:
    """The v1.11 and v1.10 scorers this module imports must equal their hashes in v1.11's lock
    manifest (tag v1.11-prereg-r1); returns the paths that differ."""
    man = {}
    for line in (root / V111_LOCK_MANIFEST).read_text(encoding="utf-8").splitlines():
        if line.strip():
            h, p = line.split("  ", 1)
            man[p] = h
    return [p for p in V111_IMPORTED if V.sha256(root / p) != man.get(p)]


def load_cut(csv_path: Path, json_path: Path) -> Tuple[set, set, dict]:
    """S-CUT answers (answer_id of every row of the cut list, section 8) and S-CUT-M cells
    ((block, category, model) from the list's summary, by the half-of-t3 rule)."""
    with open(csv_path, encoding="utf-8", newline="") as f:
        ids = {r["answer_id"] for r in csv.DictReader(f)}
    js = json.loads(Path(json_path).read_text(encoding="utf-8"))
    cells = {tuple(c) for c in js["s_cut_m_cells"]}
    return ids, cells, {"csv": str(csv_path.name), "csv_sha256": V.sha256(csv_path), "json": str(json_path.name),
                        "json_sha256": V.sha256(json_path), "answers_flagged": len(ids),
                        "s_cut_m_cells": sorted(list(c) for c in cells)}


def both(*keeps: Optional[Callable]) -> Optional[Callable]:
    """Unit filter that keeps a unit only if every given filter keeps it (None = keep all)."""
    ks = [k for k in keeps if k is not None]
    if not ks:
        return None
    return lambda u: all(k(u) for k in ks)


def scores(units, oc, role: str, keep=None, rfloor: int = S.N_FLOOR) -> Dict[tuple, dict]:
    """v1.11's score_map; with rfloor != 6 the recognition block (R) is rated at n >= rfloor (switch
    Q5, wherever cut answers are dropped). F and E keep v1.11's floor of 6."""
    s = S.score_map(units, oc, role, keep)
    if rfloor != S.N_FLOOR:
        kr = both(keep, lambda u: u["block"] == "R")
        s = {k: v for k, v in s.items() if k[0] != "R"}
        s.update(S.score_map(units, oc, role, kr, floor=rfloor))
    return s


def pick(oc120: dict, ocatt: dict, sw: Optional[dict] = None) -> Tuple[dict, dict, str]:
    """(primary outcomes, the other attempt rule's outcomes, the sensitivity's name), by switch Q2."""
    if (sw or SW)["Q2_scored_attempt"] == "first_counting":
        return oc120, ocatt, "S_ATT_v1_11_first"
    return ocatt, oc120, "S_FIRST_first_counting"


def v111_stage_j_state(run: Run, units, recs, roles) -> dict:
    """v1.11's own Stage J result, which must exist before v1.20 scores (section 7). Case B: v1.11's
    rule halts on these frozen records (recomputed with v1.11's own outcomes and fail_check; v1.11's
    Stage J stops there and writes no file). Case A: v1.11's rule does not halt and its
    stage_j_v1_11.json exists. Otherwise v1.11's Stage J has not been run: ORDER halt."""
    fc = S.fail_check(units, S.outcomes(recs, roles), ROLES)
    p = S.out_dir(run.ctx, "outputs") / S.STAGE_J_NAME
    if fc["halt"]:
        return {"state": "halted", "case": "B", "halt": fc["halt"],
                "how_known": "v1.11's outcomes and fail_check recomputed on the frozen records"}
    if p.exists():
        return {"state": "passed", "case": "A", "stage_j_v1_11_sha256": V.sha256(p)}
    raise Halt("ORDER: v1.11's own Stage J must run first (stage_j_v1_11.json is missing and v1.11's rule does not halt)")


def comparison(recs, roles, oc111: dict, oc120: dict, fcs: Dict[str, dict]) -> dict:
    """Per judge x set JUDGE_FAIL under each rule; status transitions v1.11 -> v1.20 per role and pass;
    units VALID under both whose judgement comes from a different stored attempt (ids listed)."""
    att111 = v111_attempts_used(recs, roles)
    trans, diff = Counter(), defaultdict(list)
    for k in sorted(set(oc111) | set(oc120)):
        a = oc111.get(k, {"status": S.UNJUDGED})
        b = oc120.get(k, {"status": S.UNJUDGED})
        trans[f"{k[0]} {k[2]}: {a['status']} -> {b['status']}"] += 1
        if a["status"] == S.VALID and b["status"] == S.VALID and att111.get(k) != b.get("attempt_used"):
            diff[f"{k[0]} {k[2]}"].append(k[1])
    per_set: Dict[str, dict] = defaultdict(dict)
    for name, fc in fcs.items():
        for js, row in fc["per_judge_set"].items():
            per_set[js][name] = row
    return {"judge_fail_by_judge_set": dict(per_set), "halts": {n: fc["halt"] for n, fc in fcs.items()},
            "status_transitions_v1_11_to_v1_20": dict(sorted(trans.items())),
            "valid_under_both_from_a_different_attempt": {k: {"n": len(v), "unit_ids": v} for k, v in sorted(diff.items())}}


def _counts(oc: dict) -> dict:
    return {r: dict(Counter(v["status"] for k, v in oc.items() if k[0] == r and k[2] == "main")) for r in ROLES}


def _write_json(path: Path, doc: dict) -> None:
    path.write_text(json.dumps(V._clean(doc), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ======================================================================================
# 3. STAGE J (v1.11 section 8, with the v1.20 rule): reads no P, C* or Ranking value
# ======================================================================================
def run_stage_j(run: Run, log=print) -> dict:
    bad = v111_integrity()
    if bad:
        raise Halt(f"imported scorer differs from v1.11's lock manifest: {bad}")
    u0, units = S.load_u0(run.ctx)
    recs, frozen = S.load_frozen_outputs(run.ctx)
    if frozen.get("units_sha256") != u0["units_file"]["sha256"]:
        raise Halt("frozen judge outputs were produced on another unit table")
    units = S.effective_units(units, frozen.get("plan_params"))
    roles = frozen["roles"]
    v111 = v111_stage_j_state(run, units, recs, roles)
    oc111, oc120 = S.outcomes(recs, roles), outcomes(recs, roles)
    ocatt = outcomes_v111_first(oc111, oc120)
    oc, oc_alt, alt_name = pick(oc120, ocatt)
    cut_ids, _cells, cut_meta = load_cut(run.cut_csv, run.cut_json)
    pkeep = (lambda u: u["answer_id"] not in cut_ids) if primary_drops_cut() else None
    prf = r_floor() if primary_drops_cut() else S.N_FLOOR
    fcs = {"v1.11 rule": S.fail_check(units, oc111, ROLES), "v1.20 rule (first counting)": S.fail_check(units, oc120, ROLES),
           "S-ATT (v1.11 first)": S.fail_check(units, ocatt, ROLES)}
    fc = fcs["v1.20 rule (first counting)"] if oc is oc120 else fcs["S-ATT (v1.11 first)"]
    od = run.out
    od.mkdir(parents=True, exist_ok=True)
    base = {"phase": PHASE_ID, "successor_of": SUCCESSOR_OF, "successor_of_tag": SUCCESSOR_OF_TAG, "status": STATUS,
            "rule": RULE_TEXT, "switches": SW, "config_sha256": V.sha256(CONFIG_FILE), "created_utc": S._now(),
            "dry_run": run.dry, "roles": roles, "replacements": frozen.get("replacements", []),
            "v1_11_frozen_sha256": V.sha256(S.out_dir(run.ctx, "outputs") / S.FROZEN_NAME),
            "units_sha256": u0["units_file"]["sha256"], "v1_11_stage_j": v111, "cut_list": cut_meta,
            "primary_attempt_rule": SW["Q2_scored_attempt"], "primary_cut_answers": SW["Q5_cut_answers"]}
    _write_json(od / COMPARISON_NAME, {**base, "stage": "J", **comparison(recs, roles, oc111, oc120, fcs),
                                       "outcome_counts": {"v1.11 rule": _counts(oc111), "v1.20 rule": _counts(oc120),
                                                          "S-ATT": _counts(ocatt)}})
    if fc["halt"]:
        _write_json(od / STAGE_J_NAME, {**base, "stage": "J", "halted": True, "judge_fail": fc,
                                        "judge_fail_all_rules": fcs, "outcome_counts": _counts(oc)})
        raise Halt(f"JUDGE_FAIL above 2% of a set's units under the v1.20 rule: {fc['halt']} (halt before scoring)")
    s1, s2 = scores(units, oc, "J1", pkeep, prf), scores(units, oc, "J2", pkeep, prf)
    h1 = S.h1_block(units, oc, pkeep)
    sc = S.selfcon_block(units, oc)
    h1_alt = S.h1_block(units, oc_alt, pkeep)
    ob = S.outcomes_csv_bytes(units, oc)
    (od / OUTCOMES_NAME).write_bytes(ob)
    doc = {**base, "stage": "J", "halted": False, "outcomes_sha256": V.sha256_bytes(ob), "judge_fail": fc,
           "judge_fail_all_rules": fcs, "H1_Judge_Agreement": h1, "self_consistency": sc,
           "scores": {"J1": {"|".join(k): v for k, v in s1.items()}, "J2": {"|".join(k): v for k, v in s2.items()}},
           "outcome_counts": _counts(oc),
           "sensitivity": {alt_name: {"H1_Judge_Agreement": h1_alt, "self_consistency": S.selfcon_block(units, oc_alt),
                                      "outcome_counts": _counts(oc_alt)}}}
    _write_json(od / STAGE_J_NAME, doc)
    log(f"[{PHASE_ID}] Stage J: v1.11 Stage J {v111['state']} (case {v111['case']}); JUDGE_FAIL halts: v1.11 rule "
        f"{fcs['v1.11 rule']['halt'] or 'none'}, v1.20 {fc['halt'] or 'none'}; H1 {h1['verdict']} (alpha "
        f"{h1['alpha_ordinal']:.3f}, brand rho {h1['brand_rho']['rho']:.3f}, n {h1['brand_rho']['n']}); "
        f"{alt_name} H1 {h1_alt['verdict']}")
    return doc


# ======================================================================================
# 4. STAGE C (v1.11 section 8, after Stage J): P, C* and R* are opened here and nowhere else
# ======================================================================================
def cut_counts(units, cut_ids: set, cells: set) -> dict:
    """Section 8 item 4: flagged units per block x wave x model; judged, in J2's sample, in Paper B's."""
    out = {}
    for name, flag in (("S_CUT", lambda u: u["answer_id"] in cut_ids),
                       ("S_CUT_M", lambda u: (u["block"], u["category"], u["model"]) in cells)):
        c: Dict[str, Counter] = defaultdict(Counter)
        for u in units:
            if flag(u):
                k = f"{u['block']}|{u['wave']}|{u['category']}|{u['model']}"
                c[k]["units"] += 1
                c[k]["judged"] += bool(u["judged"])
                c[k]["j2_sample"] += bool(u["j2"])
                c[k]["paper_b_sample"] += bool(u["human"])
        out[name] = {k: dict(v) for k, v in sorted(c.items())}
    return out


def run_stage_c(run: Run, log=print) -> dict:
    sj_p = run.out / STAGE_J_NAME
    if not sj_p.exists():
        raise Halt("ORDER: v1.20's Stage J (H1) must be written before P, C* or R* are opened")
    sj = json.loads(sj_p.read_text(encoding="utf-8"))
    if sj.get("halted"):
        raise Halt("v1.20's Stage J halted on JUDGE_FAIL above 2%: no Stage C (section 5)")
    if V.sha256(run.out / OUTCOMES_NAME) != sj["outcomes_sha256"]:
        raise Halt("unit outcomes changed since Stage J")
    if sj["switches"] != SW:
        raise Halt("the switches changed since Stage J (config_v1_20.json)")
    case = sj["v1_11_stage_j"]["case"]
    v111_verdicts_p = S.out_dir(run.ctx, "outputs") / S.VERDICTS_NAME
    if case == "A" and not v111_verdicts_p.exists():
        raise Halt("ORDER: v1.11's Stage J passed, so v1.11's Stage C must be written first (section 7)")
    bad = v111_integrity()
    if bad:
        raise Halt(f"imported scorer differs from v1.11's lock manifest: {bad}")
    bad = V.verify_manifest(run.ctx.manifest_path, run.ctx.root)
    if bad:
        raise Halt("manifest verification failed: " + "; ".join(bad[:10]))
    u0, units = S.load_u0(run.ctx)
    recs, frozen = S.load_frozen_outputs(run.ctx)
    units = S.effective_units(units, frozen.get("plan_params"))
    roles = frozen["roles"]
    oc111, oc120 = S.outcomes(recs, roles), outcomes(recs, roles)
    oc, oc_alt, alt_name = pick(oc120, outcomes_v111_first(oc111, oc120))
    cut_ids, cells, cut_meta = load_cut(run.cut_csv, run.cut_json)
    keep_cut = lambda u: u["answer_id"] not in cut_ids                                  # noqa: E731
    keep_cutm = lambda u: (u["block"], u["category"], u["model"]) not in cells         # noqa: E731
    pkeep = keep_cut if primary_drops_cut() else None
    prf = r_floor() if primary_drops_cut() else S.N_FLOOR
    S1, S2 = scores(units, oc, "J1", pkeep, prf), scores(units, oc, "J2", pkeep, prf)
    # --- first read of P and C* (v1.11 section 8; v1.11's code, unchanged) ---
    prof = V._read_csv(run.ctx.path(S.PROFILES_REL))
    f_units = defaultdict(set)
    for spec in S.build_sets():
        if spec["block"] == "F":
            _r, unit, _n = V.load_registry(run.ctx, spec["registry"], spec["reg_fmt"])
            f_units[spec["wave"]] |= {(spec["category"], u) for u in unit.values()}
    join = V.join_check([(r["wave"], r["substrate"], r["brand"]) for r in prof], f_units)
    if not join["passes"]:
        raise Halt("join: F units do not match aias_2_0_profiles.csv 1:1")
    P, C, NM = V.parse_profiles(prof)
    win = Counter((u["wave"], u["category"], u["brand"]) for u in units if u["block"] == "F")
    miss = Counter((s.split()[1], s.split()[2], m["brand"]) for m in u0["extraction_misses"] for s in [m["set"]]
                   if s.startswith("OMNI"))
    count_check = [f"{w}|{c}|{b}" for w in S.WAVES for (c, b), n in NM[w].items()
                   if math.isfinite(n) and win.get((w, c, b), 0) + miss.get((w, c, b), 0) != int(n)]
    state, why = S.h5_status(run.ctx)
    R, rchk = (None, {"status": state, "reason": why})
    if state == "ACTIVE":
        R, rchk = S.ranking_scores(run.ctx, log)
        rchk["status"] = state
    active, nn = state == "ACTIVE", u0["n_named"]
    j1_prov = S.provider_of(roles["J1"])
    prim = S.gate_set(units, oc, S1, P, C, R, nn, active, keep=pkeep)
    prim["H1_Judge_Agreement"] = sj["H1_Judge_Agreement"]          # H1 as written at Stage J
    h9res = S.h9(units, oc, j1_prov, keep=pkeep)
    raw_v = S.verdict_row(prim, h9res, state)
    final_v, guard_on = S.apply_noise_guard(raw_v)
    sens: dict = {}
    changes = []

    def note(name, v):
        for h, val in v.items():
            if val != raw_v.get(h):
                changes.append({"sensitivity": name, "hypothesis": h, "primary": raw_v.get(h), "under_sensitivity": val})

    def variant(name, o, keep, rfloor):
        """Every statistic SD recomputes (H1-H6, H9) plus H7, H8: gate_set and H9 on one unit filter."""
        s = scores(units, o, "J1", keep, rfloor)
        g = S.gate_set(units, o, s, P, C, R, nn, active, keep=keep)
        h = S.h9(units, o, j1_prov, keep=keep)
        sens[name] = {**g, "H9_Self_Preference": h, "unit_filter": name, "r_floor": rfloor}
        note(name, S.verdict_row(g, h, state))

    # v1.11's sensitivities (section 5.1), on the primary outcomes, unchanged
    with V.uncentred():
        su = S.gate_set(units, oc, S1, P, C, R, nn, active, keep=pkeep)
    sens["SU_uncentred_ranks"] = su
    note("SU_uncentred_ranks", S.verdict_row(su, h9res, state))
    not_denon = lambda u: not (u["block"] == "F" and (u["category"], u["brand"]) == S.DENON)  # noqa: E731
    key_nd = lambda k: not (k[0] == "F" and (k[2], k[3]) == S.DENON)                           # noqa: E731
    sd = S.gate_set(units, oc, S1, P, C, R, nn, active, keep=both(pkeep, not_denon), keep_key=key_nd)
    sd_h9 = S.h9(units, oc, j1_prov, keep=both(pkeep, not_denon))
    sens["SD_without_Denon_v0_19"] = {**sd, "H9_Self_Preference": sd_h9}
    note("SD_without_Denon_v0_19", S.verdict_row(sd, sd_h9, state))
    nv = {k: {**v, "rated": v["rated"] and v["NV"] is not None} for k, v in S1.items()}
    sens["S_NV_in_place_of_S"] = {"H2": S.sep_by_wave(nv, P, field="NV"), "H3": S.sep_by_wave(nv, C, field="NV")}
    mb = S.model_balanced(units, oc, keep=pkeep)
    sens["S_model_balanced"] = {"H2": S.sep_by_wave(mb, P), "H3": S.sep_by_wave(mb, C)}
    sens["S_J2_scored"] = {"H2": S.sep_by_wave(S2, P), "H3": S.sep_by_wave(S2, C)}
    if h9res["verdict"] == "FALSIFIED":
        Snp = scores(units, oc, "J1", both(pkeep, lambda u: u["provider"] != j1_prov), prf)
        sens["S_without_J1_provider_answers"] = {"H2": S.sep_by_wave(Snp, P), "H3": S.sep_by_wave(Snp, C)}
    # v1.20's sensitivities (sections 4 and 8)
    variant(alt_name, oc_alt, pkeep, prf)
    if primary_drops_cut():
        variant("S_ALL_with_cut_answers", oc, None, S.N_FLOOR)
    else:
        variant("S_CUT_without_cut_answers", oc, keep_cut, r_floor())
    variant("S_CUT_M_without_cut_cells", oc, both(pkeep, keep_cutm), r_floor())
    sens["verdict_changes"] = changes
    desc = S.descriptives(run.ctx, units, oc, S1, S2, u0)
    desc["cut_answers"] = cut_counts(units, cut_ids, cells)
    v111_v = json.loads(v111_verdicts_p.read_text(encoding="utf-8")).get("VERDICTS") if v111_verdicts_p.exists() else None
    role = ("Sentiment Paper A's result (case B; switch Q6 = true)" if case == "B" and SW["Q6_case_b_result"] else
            "pre-registered re-scoring reported beside v1.11's confirmatory record (case A)" if case == "A" else
            "pre-registered re-scoring only (case B; switch Q6 = false)")
    doc = {"phase": PHASE_ID, "stage": "C", "created_utc": S._now(), "dry_run": run.dry, "prereg_tag": PREREG_TAG,
           "successor_of_tag": SUCCESSOR_OF_TAG, "rule": RULE_TEXT, "switches": SW, "config_sha256": V.sha256(CONFIG_FILE),
           "role_of_these_verdicts": role, "v1_11_stage_j": sj["v1_11_stage_j"], "v1_11_verdicts": v111_v,
           "roles": roles, "stage_j_sha256": V.sha256(sj_p), "units_sha256": u0["units_file"]["sha256"],
           "manifest_sha256": V.sha256(run.ctx.manifest_path), "cut_list": cut_meta,
           "rank_convention": "within-category average ranks centred on the category mean rank",
           "join": join, "F_window_count_vs_n_mentions": {"mismatches": count_check},
           "ranking": rchk, "verdicts_before_noise_guard": raw_v, "VERDICTS": final_v, "noise_guard_applied": guard_on,
           "H1_marginal_flag_on_all_verdicts": final_v["H1"] == "MARGINAL",
           **{k: v for k, v in prim.items()}, "H9_Self_Preference": h9res, "sensitivities": sens,
           "descriptives": desc, "self_consistency": sj["self_consistency"], "seeds": S.SEEDS,
           "draws": {"perm": S.N_PERM, "boot": S.N_BOOT, "ci": S.CI_LEVEL}}
    _write_json(run.out / VERDICTS_NAME, doc)
    comp_p = run.out / COMPARISON_NAME
    comp = json.loads(comp_p.read_text(encoding="utf-8"))
    comp["verdicts_side_by_side"] = {"v1.11": v111_v, PHASE_ID: final_v, "role_of_v1_20_verdicts": role}
    _write_json(comp_p, comp)
    log(f"[{PHASE_ID}] Stage C verdicts: {final_v} (noise guard {'ON' if guard_on else 'off'}); case {case}: {role}; "
        f"{len(changes)} sensitivity verdict changes; written to {run.out / VERDICTS_NAME}")
    return doc


# ======================================================================================
# 5. LOCK MANIFEST, ANCHOR, LOCK STATUS (v1.11's schema and steps; decision 24 of v1.11)
# ======================================================================================
LOCK_FILES = [
    f"{V120}/prereg/PRE_REGISTRATION_v1_20.md", f"{V120}/prereg/config_v1_20.json",
    f"{V120}/scoping/format_counts_v1_15.py", f"{V120}/scoping/format_counts_v1_15.json",
    f"{V120}/scoping/cut_units_v1_20.py", f"{V120}/scoping/cut_units_v1_20.csv", f"{V120}/scoping/cut_units_v1_20.json",
    f"{V120}/dryrun/build_dryrun_v1_20.py", f"{V120}/dryrun/dry_run_v1_20.txt", f"{V120}/anchor/DEVIATIONS.md",
    "scripts/score_v1_20.py", "scripts/test_score_v1_20.py",
    V111_LOCK_MANIFEST, "scripts/score_v1_11.py", "scripts/score_v1_10.py",
]
LOCK_MANIFEST_FILE = PREREG_DIR / "LOCK_MANIFEST_v1_20.sha256"
ANCHOR_FIELDS = S.ANCHOR_FIELDS


def _git(*args) -> str:
    r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise Halt(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout.strip()


def lock_manifest_text(root: Path = ROOT) -> str:
    """sha256sum format, LOCK_FILES order, from the working tree."""
    return "".join(f"{V.sha256(root / p)}  {p}\n" for p in LOCK_FILES)


def anchor_template(osf_deposit: str = "") -> dict:
    return {k: ({} if k == "locked_files" else "") for k in ANCHOR_FIELDS} | {"osf_deposit": osf_deposit}


def anchor_problems(anchor: dict, commit: Optional[str] = None) -> List[str]:
    """v1.11's anchor_problems with v1.20's tag and lock files (empty list = the anchor anchors the lock)."""
    why = [f"anchor field missing or empty: {k}" for k in ANCHOR_FIELDS if k != "osf_deposit" and not anchor.get(k)]
    if not str(anchor.get("osf_deposit") or "").strip():
        why.append("the anchor file records no OSF deposit (osf_deposit is empty)")
    if anchor.get("tag") and anchor["tag"] != PREREG_TAG:
        why.append(f"anchor tag {anchor['tag']} is not {PREREG_TAG}")
    if commit and anchor.get("commit") != commit and anchor.get("tag_object") != commit:
        why.append(f"the anchor file does not name the commit of {PREREG_TAG} ({commit})")
    lf = anchor.get("locked_files") or {}
    if lf and sorted(lf) != sorted(LOCK_FILES):
        why.append("the anchor's locked_files differ from LOCK_FILES")
    return why


def build_anchor(osf_deposit: str) -> dict:
    """The anchor record of the pushed tag (v1.11's build_anchor with v1.20's tag, branch and files)."""
    if not str(osf_deposit or "").strip():
        raise Halt("--write-anchor needs a non-empty --osf-deposit")
    remote = _git("ls-remote", "--tags", "origin", PREREG_TAG)
    if f"refs/tags/{PREREG_TAG}" not in remote:
        raise Halt(f"tag {PREREG_TAG} is not on origin: push it before writing the anchor")
    files = {}
    for p in LOCK_FILES:
        blob = _git("rev-parse", f"{PREREG_TAG}:{p}")
        data = subprocess.run(["git", "-C", str(ROOT), "cat-file", "blob", blob], capture_output=True).stdout
        files[p] = {"sha256": hashlib.sha256(data).hexdigest(), "git_blob": blob}
    doc = anchor_template(osf_deposit)
    doc.update({"tag": PREREG_TAG, "tag_object": _git("rev-parse", PREREG_TAG),
                "commit": _git("rev-parse", f"{PREREG_TAG}^{{commit}}"),
                "tree": _git("rev-parse", f"{PREREG_TAG}^{{tree}}"), "branch": BRANCH,
                "tagger_date": _git("for-each-ref", "--format=%(taggerdate:iso-strict)", f"refs/tags/{PREREG_TAG}"),
                "remote_tag_ref": remote.splitlines()[0], "recorded_utc": S._now(),
                "repository": _git("remote", "get-url", "origin"), "locked_files": files})
    bad = anchor_problems(doc, doc["commit"])
    if bad:
        raise Halt("; ".join(bad))
    return doc


def lock_status() -> Tuple[bool, str]:
    """Stages J and C on real data need v1.20's tag and anchor AND v1.11's (v1.11's lock_status)."""
    why = []
    if not V._tag_exists(PREREG_TAG, ROOT):
        why.append(f"git tag {PREREG_TAG} does not exist")
    if not ANCHOR_FILE.exists():
        why.append(f"anchor file {ANCHOR_FILE} does not exist")
    elif not why:
        commit = _git("rev-parse", f"{PREREG_TAG}^{{commit}}")
        why += anchor_problems(json.loads(ANCHOR_FILE.read_text(encoding="utf-8")), commit)
    ok111, why111 = S.lock_status()
    if not ok111:
        why.append("v1.11: " + why111)
    return (not why), "; ".join(why)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--stage", choices=["J", "C"])
    ap.add_argument("--dry-run", action="store_true", help="synthetic dry-run work folder only")
    ap.add_argument("--draws", type=int, default=None, metavar="N",
                    help="dry run only: bootstrap and permutation draws (v1.11's 10,000 otherwise)")
    ap.add_argument("--lock-manifest", action="store_true",
                    help="write prereg/LOCK_MANIFEST_v1_20.sha256 (LOCK_FILES, working tree); last step of the content lock")
    ap.add_argument("--write-anchor", action="store_true",
                    help="after the tag is pushed: write anchor/git_anchor_v1_20.json from the tag (needs --osf-deposit)")
    ap.add_argument("--osf-deposit", default=None, metavar="WHERE")
    a = ap.parse_args(argv)
    if a.lock_manifest:
        LOCK_MANIFEST_FILE.write_text(lock_manifest_text(), encoding="utf-8")
        print(f"[{PHASE_ID}] {LOCK_MANIFEST_FILE} written ({len(LOCK_FILES)} files)")
        return 0
    if a.write_anchor:
        try:
            doc = build_anchor(a.osf_deposit)
        except V.Halt as e:
            print(f"[{PHASE_ID}] REFUSED: {e}", file=sys.stderr)
            return 3
        ANCHOR_FILE.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"[{PHASE_ID}] {ANCHOR_FILE} written: {doc['tag']} -> {doc['commit']}")
        return 0
    if a.stage:
        if a.draws is not None:
            if not a.dry_run:
                print(f"[{PHASE_ID}] --draws is for dry runs only", file=sys.stderr)
                return 3
            S.N_BOOT = S.N_PERM = int(a.draws)
        if not a.dry_run:
            ok, why = lock_status()
            if not ok:
                print(f"[{PHASE_ID}] refusing --stage {a.stage} on real data before the lock: {why}", file=sys.stderr)
                return 3
        elif not DRY_MANIFEST.exists():
            print(f"[{PHASE_ID}] no dry-run work folder; build it with python3 {V120}/dryrun/build_dryrun_v1_20.py",
                  file=sys.stderr)
            return 2
        try:
            (run_stage_j if a.stage == "J" else run_stage_c)(Run(a.dry_run))
        except V.Halt as e:
            print(f"[{PHASE_ID}] HALT: {e}", file=sys.stderr)
            return 2
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
