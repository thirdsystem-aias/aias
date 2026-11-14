#!/usr/bin/env python3
"""
check_first_answers_v1_12.py -- AIAS v1.12 Coverage Paper A: the declared check on the first answers for answers that
stop at the output length limit (anchor/DEVIATIONS.md, Entry 1, 2026-11-13; approved by the pre-registrant on
2026-11-12, 23:36 CT). Written by the AIAS runner (lane A) on 2026-11-13, before the first v1.12 call.

READ-ONLY. Reads the call record written so far (osf/methodology/v1_12/data/v112_raw.jsonl, or --raw PATH) in one
read and never writes to it or to any other file in the repository; no model API is called and no provider client is
created. It changes nothing in the collection: acquire_v1_12.py does not read its result.

Reported per model: records; answers (acquire_v1_12.answered, the collection's own rule); the finish reasons as
recorded; length stops; records at the cap by recorded tokens; answers that cannot be checked; thinking tokens at or
above half the cap; the largest output and thinking counts. For every record that triggers: whether its visible text
names a registry brand of its category.

Definitions (fixed before the first v1.12 call):
  cap            acquire_v1_12.CURRENT_MAX_TOKENS = 16,384: the max_tokens / max_output_tokens that the three copied
                 call functions send for all four models (also SETTINGS["max_output_tokens"] and OUT_WORST).
  length stop    the locked scorer's rule score_v1_12._truncated (= score_v0_42._truncated; MC_Truncation, section 4,
                 clarification (q)): the recorded finish reason contains "max_tokens" or "max_output_tokens" (any
                 case) or equals "length". As acquire_v1_12.py records a length stop: Anthropic stop_reason
                 "max_tokens"; OpenAI "incomplete:max_output_tokens"; Google "FinishReason.MAX_TOKENS".
  at the cap     recorded output tokens >= cap. The Anthropic and OpenAI output counts include thinking/reasoning;
                 Google's excludes thinking (acquire_v1_12.usd), so for Google output + thinking >= cap. Checked on
                 the record and on every billed attempt (billed_attempts): an empty first answer that the locked
                 empty-answer retry re-asked leaves its tokens only there.
  cannot check   a record holding an answer (status ok or empty, or any visible text) whose finish reason or output
                 token count is missing: the check cannot clear it.
  TRIGGER        any record with a length stop, at the cap, or that cannot be checked -> exit 3. After a pause and
                 resume, --reported-through N lists records 1..N (already reported; the record is append-only) without
                 a new trigger, so that only records written after them trigger.
  NOTE           thinking tokens >= half the cap (8,192) on the record or on a billed attempt (OpenAI reasoning,
                 Google thinking; Anthropic reports no separate count): reported, not a trigger.
  brand check    for each record that stopped at the cap and has visible text: v0.42's coder (scripts/code_t4_v0_42.py)
                 on that text through its Phase B path with URLs removed, exactly as score_v1_12 codes answers
                 (to_t4_record, then code_calls). Loaded only when a record triggers (--no-brand-check skips it).
                 The coder's bootstrap re-executes this script under a temporary HOME shim, as it does for the scorer,
                 and its certified modules import numpy, scipy and the anthropic SDK (no client is created, nothing is
                 sent). If it cannot load, the brand status says so and the trigger stands.

Locked code is reused read-only and checked first: acquire_v1_12.py is imported (only the standard library loads at
import; the provider SDKs load inside the call functions, which are never called); RAW_SUB, _truncated and
to_t4_record are executed from score_v1_12.py's own source text (not imported, so numpy and scipy do not load); the
coder is imported only for the brand check. All three files must match prereg/LOCK_MANIFEST_v1_12.sha256, else the
check refuses (exit 1).

Run on the Mac (about a second; seconds more when a brand check runs):
  cd /Users/pablou/aias/_worktrees/v1.12 && PYTHONDONTWRITEBYTECODE=1 /Users/pablou/aias/venv/bin/python \
      osf/methodology/v1_12/monitor/check_first_answers_v1_12.py [--raw PATH] [--json] [--no-brand-check] \
      [--reported-through N]
Exit: 0 clear (notes allowed); 3 trigger (pause, report to the pre-registrant, resume under the locked rules);
1 cannot run (a locked file differs from the manifest, or the record cannot be read); 2 usage.
"""
import argparse
import ast
import hashlib
import importlib.util
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"        # carried into the coder's HOME-shim re-exec: no __pycache__

HERE = Path(__file__).resolve().parent             # <repo>/osf/methodology/v1_12/monitor
V112 = HERE.parent
ROOT = V112.parents[2]
SCRIPTS = V112 / "scripts"
MANIFEST = V112 / "prereg" / "LOCK_MANIFEST_v1_12.sha256"
LOCKED = ("osf/methodology/v1_12/scripts/acquire_v1_12.py", "osf/methodology/v1_12/scripts/score_v1_12.py",
          "osf/methodology/v1_12/scripts/code_t4_v0_42.py")
SCORER_PARTS = ("RAW_SUB", "_truncated", "to_t4_record")
ANSWER_STATUSES = ("ok", "empty")
EXIT_CLEAR, EXIT_CANNOT_RUN, EXIT_TRIGGER = 0, 1, 3
EARLIER_ATTEMPT = ("an earlier attempt of this call reached the cap; its text is not recorded (the locked retry "
                   "re-asks only empty answers); the recorded answer did not stop at the cap")


# --------------------------------------------------------------------------- locked code, read-only
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_locked(root=ROOT, manifest=MANIFEST, files=LOCKED):
    """The files of `files` that are missing from the manifest, missing on disk, or whose SHA-256 differs from it."""
    pinned = {}
    for ln in Path(manifest).read_text(encoding="utf-8").splitlines():
        if ln.strip():
            h, rel = ln.split(None, 1)
            pinned[rel.strip()] = h
    return [rel for rel in files if rel not in pinned or not (Path(root) / rel).is_file()
            or sha256(Path(root) / rel) != pinned[rel]]


def load_acquire(path=SCRIPTS / "acquire_v1_12.py"):
    """acquire_v1_12.py, loaded as the pre-launch check loads it (module level: constants and definitions only)."""
    spec = importlib.util.spec_from_file_location("acquire_v1_12", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_scorer_parts(path=SCRIPTS / "score_v1_12.py", names=SCORER_PARTS):
    """RAW_SUB, _truncated and to_t4_record, executed from the locked scorer's own source text (the last definition
    of a name wins, as on import). Nothing else of the scorer runs."""
    src = Path(path).read_text(encoding="utf-8")
    seg = {}
    for node in ast.parse(src).body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            seg[node.name] = ast.get_source_segment(src, node)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id in names:
                    seg[t.id] = ast.get_source_segment(src, node)
    missing = [n for n in names if n not in seg]
    if missing:
        raise RuntimeError(f"{Path(path).name} does not define {missing}")
    ns = {"__name__": "score_v1_12_parts"}
    for n in names:
        exec(compile(seg[n], f"{Path(path).name}:{n}", "exec"), ns)
    return {n: ns[n] for n in names}


def coder_detector(parts):
    """The scorer's coding path for one record: to_t4_record, then the coder's code_calls (Phase B, URLs removed).
    Importing the coder may re-execute this script under a HOME shim (its bootstrap): call it before printing."""
    os.environ["AIAS_ROOT"] = str(ROOT)
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    import code_t4_v0_42 as C   # noqa: E402

    def detect(rec):
        r = dict(rec, status="ok", error=None)   # the visible text as recorded; status and error do not gate detection
        _a, rows = C.code_calls([parts["to_t4_record"](r)], probes={}, strip=True)
        return sorted({row["brand"] for row in rows if row["mentioned"]})
    return detect


# --------------------------------------------------------------------------- the record (read-only)
def read_record(path):
    """One read of the call record (never opened for writing). Returns (records or None if absent, unreadable
    lines, last line incomplete). An incomplete last line (being written) is skipped, not counted as unreadable."""
    p = Path(path)
    if not p.exists():
        return None, 0, False
    data = p.read_bytes()
    incomplete = bool(data) and not data.endswith(b"\n")
    lines = data.split(b"\n")
    recs, bad = [], 0
    for i, raw in enumerate(lines):
        if not raw.strip():
            continue
        try:
            r = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            r = None
        if isinstance(r, dict):
            recs.append(r)
        elif not (incomplete and i == len(lines) - 1):
            bad += 1
    return recs, bad, incomplete


def _count(v):
    """A token count as an int; None when missing, null or not a whole number."""
    if v is None or isinstance(v, bool):
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, float) and v.is_integer():
        return int(v)
    if isinstance(v, str) and v.strip().isdigit():
        return int(v.strip())
    return None


def output_total(provider, out, think):
    """Output tokens as they count against the cap: Google's output count excludes thinking (acquire_v1_12.usd)."""
    if out is None:
        return None
    return out + (think or 0) if provider == "google" else out


def finish_missing(fr):
    return fr is None or str(fr).strip() in ("", "None")    # Google: str(None) == "None" when no finish reason came


# --------------------------------------------------------------------------- the check (pure: no printing, no writing)
def evaluate(rec, cap, truncated):
    """Signals of one record: length stop, at the cap (record or billed attempt), missing fields, thinking >= cap/2."""
    provider = rec.get("provider")
    out, think = _count(rec.get("output_tokens")), _count(rec.get("thinking_tokens"))
    fr = rec.get("finish_reason")
    has_answer = rec.get("status") in ANSWER_STATUSES or bool(str(rec.get("text") or "").strip())
    signals = []
    if not finish_missing(fr) and truncated(rec):
        signals.append("finish reason")
    total = output_total(provider, out, think)
    if total is not None and total >= cap:
        signals.append("tokens at cap")
    att_cap = att_think = 0
    for b in rec.get("billed_attempts") or []:
        if not isinstance(b, dict):
            continue
        b_out, b_think = _count(b.get("output_tokens")), _count(b.get("thinking_tokens"))
        b_total = output_total(provider, b_out, b_think)
        att_cap += bool(b_total is not None and b_total >= cap)
        att_think += bool(b_think is not None and b_think >= cap / 2)
    if att_cap and "tokens at cap" not in signals:
        signals.append("billed attempt at cap")
    missing = ([k for k, gone in (("finish_reason", finish_missing(fr)), ("output_tokens", out is None)) if gone]
               if has_answer else [])
    return {"signals": signals, "missing": missing, "trigger": bool(signals or missing),
            "think_half": bool((think is not None and think >= cap / 2) or att_think), "out": out, "think": think}


def _new_row(provider=None):
    return {"provider": provider, "records": 0, "answered": 0, "finish_reasons": Counter(), "length_stops": 0,
            "at_cap_tokens": 0, "earlier_attempt_at_cap": 0, "cannot_check": 0, "thinking_half_cap": 0,
            "max_output_tokens": None, "max_thinking_tokens": None, "settings_other_cap": 0}


def check(records, AQ, parts, cap=None, reported_through=0):
    """Per-model summary and the records that trigger. `records`: dicts as acquire_v1_12.py writes them, in file
    order. Records numbered <= reported_through (already reported to the pre-registrant before a resume; the record
    is append-only, so the numbers are stable) are listed but do not trigger again."""
    cap = int(cap or AQ.CURRENT_MAX_TOKENS)
    truncated = parts["_truncated"]
    rows = {m["model_id"]: _new_row(m["provider"]) for m in AQ.PANEL}
    flagged = []
    for i, rec in enumerate(records):
        m = rec.get("model_requested") or "(no model_requested)"
        row = rows.setdefault(m, _new_row(rec.get("provider")))
        ev = evaluate(rec, cap, truncated)
        row["records"] += 1
        row["answered"] += bool(rec.get("model_requested")) and bool(AQ.answered(rec))
        row["finish_reasons"][str(rec.get("finish_reason"))] += 1
        row["length_stops"] += "finish reason" in ev["signals"]
        row["at_cap_tokens"] += "tokens at cap" in ev["signals"]
        row["earlier_attempt_at_cap"] += "billed attempt at cap" in ev["signals"]
        row["cannot_check"] += bool(ev["missing"])
        row["thinking_half_cap"] += ev["think_half"]
        for key, v in (("max_output_tokens", ev["out"]), ("max_thinking_tokens", ev["think"])):
            if v is not None and (row[key] is None or v > row[key]):
                row[key] = v
        st = rec.get("settings")
        if isinstance(st, dict) and st.get("max_output_tokens") not in (None, cap):
            row["settings_other_cap"] += 1
        if ev["trigger"]:
            flagged.append({"record_no": i + 1, "call_id": rec.get("call_id"), "model": m,
                            "provider": rec.get("provider"), "pass": rec.get("pass"), "status": rec.get("status"),
                            "finish_reason": rec.get("finish_reason"), "output_tokens": ev["out"],
                            "thinking_tokens": ev["think"], "signals": ev["signals"], "missing": ev["missing"],
                            "new": i + 1 > reported_through, "named": None, "brand": None, "_rec": rec})
    return {"checked_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"), "cap": cap,
            "settings_cap": AQ.SETTINGS.get("max_output_tokens"), "per_model_expected": AQ.EXPECTED_TOTAL // len(AQ.PANEL),
            "n_records": len(records), "reported_through": reported_through, "models": rows, "flagged": flagged,
            "exit": EXIT_TRIGGER if any(f["new"] for f in flagged) else EXIT_CLEAR}


def needs_coder(f):
    return bool(f["new"] and f["signals"] and f["signals"] != ["billed attempt at cap"]
                and str(f["_rec"].get("text") or "").strip())


def apply_brand_check(rep, detect, why_not=None):
    """Brand status of every flagged record. detect(rec) -> registry brands named in its visible text."""
    for f in rep["flagged"]:
        rec = f["_rec"]
        if not f["new"]:
            f["brand"] = f"reported earlier (record {f['record_no']} <= --reported-through {rep['reported_through']})"
        elif not f["signals"]:
            f["brand"] = "not checked: no stop at the cap seen (fields missing)"
        elif f["signals"] == ["billed attempt at cap"]:
            f["brand"] = EARLIER_ATTEMPT
        elif not str(rec.get("text") or "").strip():
            f["named"], f["brand"] = [], "no visible text: stopped before naming any brand"
        elif detect is None:
            f["brand"] = f"not checked: {why_not}"
        else:
            try:
                named = detect(rec)
            except Exception as e:  # the trigger stands either way
                f["brand"] = f"not checked: {type(e).__name__}: {e}"[:300]
                continue
            f["named"] = named
            f["brand"] = (f"names {len(named)} registry brand(s) before the cut: {', '.join(named)}" if named
                          else "names no registry brand: stopped before naming any brand")
    return rep


# --------------------------------------------------------------------------- output
def public(rep):
    """The report without the raw records (JSON-safe)."""
    out = {k: v for k, v in rep.items() if k not in ("models", "flagged")}
    out["models"] = {m: {**r, "finish_reasons": dict(r["finish_reasons"])} for m, r in rep["models"].items()}
    out["flagged"] = [{k: v for k, v in f.items() if k != "_rec"} for f in rep["flagged"]]
    return out


def render(rep):
    cap, half = rep["cap"], rep["cap"] // 2
    read = (f"{rep['n_records']} records read" if rep.get("raw_exists", True) else "absent: nothing collected yet")
    if rep.get("unreadable_lines"):
        read += f"; {rep['unreadable_lines']} unreadable line(s) skipped"
    if rep.get("last_line_incomplete"):
        read += "; last line incomplete (being written?), skipped"
    L = [f"v1.12 first-answers check (anchor/DEVIATIONS.md, Entry 1) at {rep['checked_utc']}",
         f"record: {rep.get('raw')} ({read})",
         f"cap: {cap:,} output tokens for every model (acquire_v1_12.CURRENT_MAX_TOKENS; settings max_output_tokens "
         f"{rep['settings_cap']}). Length stop = score_v1_12._truncated on the recorded finish reason; at the cap = "
         f"output tokens >= cap (Google: output + thinking), record or billed attempt; note at thinking >= {half:,}.",
         "",
         f"{'model':17s} {'records':>7s} {'answered':>9s} {'len.stop':>8s} {'at cap':>6s} {'earlier':>7s} "
         f"{'no check':>8s} {'think>=half':>11s} {'max out':>8s} {'max think':>9s}  finish reasons as recorded"]
    for m, r in rep["models"].items():
        th = "n/a" if r["provider"] == "anthropic" else str(r["thinking_half_cap"])
        fr = ", ".join(f"{k} {n}" for k, n in sorted(r["finish_reasons"].items())) or "-"
        L.append(f"{m:17s} {r['records']:7d} {str(r['answered']) + '/' + str(rep['per_model_expected']):>9s} "
                 f"{r['length_stops']:8d} {r['at_cap_tokens']:6d} {r['earlier_attempt_at_cap']:7d} "
                 f"{r['cannot_check']:8d} {th:>11s} {str(r['max_output_tokens']):>8s} "
                 f"{str(r['max_thinking_tokens']):>9s}  {fr}"
                 + (f"  [settings with another cap: {r['settings_other_cap']}]" if r["settings_other_cap"] else ""))
    flagged = rep["flagged"]
    new = [f for f in flagged if f["new"]]
    if flagged:
        L += ["", f"Records that stop at the cap or cannot be checked ({len(flagged)}: new {len(new)}, reported "
                  f"earlier {len(flagged) - len(new)}):"]
        for f in flagged:
            why = ", ".join(f["signals"] + [f"missing {k}" for k in f["missing"]])
            L.append(f"  {'NEW' if f['new'] else 'earlier'} #{f['record_no']} {f['call_id']} pass {f['pass']} status "
                     f"{f['status']} finish_reason={f['finish_reason']} output={f['output_tokens']} "
                     f"thinking={f['thinking_tokens']} [{why}] -> {f['brand']}")
    notes = sum(r["thinking_half_cap"] for r in rep["models"].values())
    note = f" NOTE: {notes} record(s) with thinking tokens >= {half:,} (half the cap; not a trigger)." if notes else ""
    if new:
        k = lambda s: sum(1 for f in new if s in f["signals"])   # noqa: E731
        L += ["", f"RESULT: TRIGGER (exit 3): {len(new)} new record(s): {k('finish reason')} length stop(s) by finish "
                  f"reason, {k('tokens at cap')} at the cap by tokens, {k('billed attempt at cap')} with an earlier "
                  f"attempt at the cap, {sum(1 for f in new if f['missing'])} that cannot be checked; stopped before "
                  f"naming any brand {sum(1 for f in new if f['named'] == [])}, after naming one "
                  f"{sum(1 for f in new if f['named'])}. Pause the collection, report to the pre-registrant, resume "
                  f"under the locked rules (DEVIATIONS.md Entry 1); after the resume, check with --reported-through "
                  f"N, N = the records read by a check run after the pause." + note]
    elif flagged:
        L += ["", f"RESULT: CLEAR (exit 0): no record after record {rep['reported_through']} stops at the cap or "
                  f"lacks a finish reason or output-token count ({len(flagged)} reported earlier, listed above)." + note]
    else:
        L += ["", "RESULT: CLEAR (exit 0): no record stops at the cap; every answer carries a finish reason and an "
                  "output-token count." + note]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description="v1.12 first-answers check: answers that stop at the output length limit "
                                             "(read-only)")
    ap.add_argument("--raw", default=None, help="call record to read (default: acquire_v1_12.RAW_PATH)")
    ap.add_argument("--json", action="store_true", help="print the result as JSON instead of the table")
    ap.add_argument("--no-brand-check", action="store_true", help="do not load the coder (brand status: not checked)")
    ap.add_argument("--reported-through", type=int, default=0, metavar="N",
                    help="records 1..N were already reported to the pre-registrant (before a resume): listed, no "
                         "new trigger")
    a = ap.parse_args(argv)
    bad = verify_locked()
    if bad:
        print(f"REFUSED: locked file(s) differ from {MANIFEST.name}: {', '.join(bad)}; check not run (exit 1)")
        return EXIT_CANNOT_RUN
    AQ = load_acquire()
    parts = load_scorer_parts()
    raw = Path(a.raw).resolve() if a.raw else AQ.RAW_PATH
    try:
        recs, bad_lines, incomplete = read_record(raw)
    except OSError as e:
        print(f"CANNOT RUN: {raw}: {e} (exit 1)")
        return EXIT_CANNOT_RUN
    rep = check(recs or [], AQ, parts, reported_through=max(0, a.reported_through))
    rep.update(raw=str(raw), raw_exists=recs is not None, unreadable_lines=bad_lines, last_line_incomplete=incomplete)
    if rep["flagged"]:
        detect, why = None, "--no-brand-check"
        if not a.no_brand_check and any(needs_coder(f) for f in rep["flagged"]):
            try:
                detect, why = coder_detector(parts), None      # may re-exec this script once (HOME shim)
            except (Exception, SystemExit) as e:
                detect, why = None, f"coder not loaded ({type(e).__name__}: {e})"[:300]
        apply_brand_check(rep, detect, why)
    print(json.dumps(public(rep), indent=1, ensure_ascii=False, default=str) if a.json else render(rep))
    return rep["exit"]


if __name__ == "__main__":
    sys.exit(main())
