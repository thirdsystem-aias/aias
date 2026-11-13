#!/usr/bin/env python3
"""Tests for acquire_v0_40.py against FAKE providers (zero cost; nothing is sent). Run: python3 test_acquire_v0_40.py"""
import inspect
import json
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import acquire_v0_40 as A  # noqa: E402

FAILS = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if detail and not cond else ""))
    if not cond:
        FAILS.append(name)


def rows(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()]


specs = A.build_specs(A.load_probes())
check("matrix has 2,821 calls", len(specs) == A.EXPECTED_TOTAL == 2821, len(specs))
check("legacy arm 1,786 calls (6 x 94 x 3 + 94)", sum(s["arm"] == "L" for s in specs) == 1786)
s1 = [s for s in specs if s["condition"] == "S1"]
check("S1 = 63 probes x 3 current models", len(s1) == 189 and {s["model"]["arm"] for s in s1} == {"C"})
check("S1 probes are the recommendation and status probes only",
      all(s["kind"] == "recommendation" or s["tier"] == "S" for s in s1))
check("S1 is the last block", max(s["block"] for s in specs if s["condition"] == "S0") < min(s["block"] for s in s1))
check("no sampling parameter in the current-arm functions", A.confirm_no_sampling_params() == [])
src0 = inspect.getsource(A.call_google_budget0)
check("M5 uses thinking budget 0", "thinking_budget=0" in src0 and A.LEGACY[4]["dispatch"] == "google_budget0")
v39 = (Path(__file__).resolve().parents[2] / "v39/scripts/acquire_v0_39.py").read_text(encoding="utf-8")
check("legacy call functions verbatim from v0.39",
      all(inspect.getsource(f) in v39 for f in (A.call_anthropic, A.call_openai, A.call_google)))
check("M5X (extra pass) uses the verbatim v0.39 call_google", A.LEGACY_X["dispatch"] == "google")
# Key routing of 2026-11-13: M2 (Claude Sonnet 4.5) goes through the old organization's key; the request is unchanged.
check("M2 is sent with the old organization's key, M1 with the default key",
      A.LEGACY[1]["model_id"] == "claude-sonnet-4-5" and A.LEGACY[1]["dispatch"] == "anthropic_legacy_org"
      and A.LEGACY_DISPATCH["anthropic_legacy_org"] is A.call_anthropic_legacy_org
      and A.LEGACY[0]["dispatch"] == "anthropic" and A.LEGACY_ORG_KEY_ENV == "ANTHROPIC_API_KEY_LEGACY")
_req_old = inspect.getsource(A.call_anthropic).split("try:", 1)[1].split("text = ", 1)[0]
_req_new = inspect.getsource(A.call_anthropic_legacy_org).split("try:", 1)[1].split("text = ", 1)[0]
check("the old-organization copy sends the same request as the verbatim call_anthropic", _req_old == _req_new)
import os  # noqa: E402
_env = dict(os.environ)
try:
    os.environ.update({"ANTHROPIC_API_KEY": "x", "OPENAI_API_KEY": "x", "GOOGLE_API_KEY": "x"})
    os.environ.pop("ANTHROPIC_API_KEY_LEGACY", None)
    try:
        A.require_keys()
        _rk = "no exit"
    except SystemExit as e:
        _rk = str(e)
finally:
    os.environ.clear()
    os.environ.update(_env)
check("require_keys asks for the old organization's key", "ANTHROPIC_API_KEY_LEGACY" in _rk, _rk)
check("current arm = Fable 5.2 (batch), GPT-6 Astra, Gemini 4 Argon",
      [(m["model_id"], m["mode"]) for m in A.CURRENT] == [("claude-fable-5-2", "batch"), ("gpt-6-astra", "standard"),
                                                           ("gemini-4-argon", "standard")])

with tempfile.TemporaryDirectory() as d:
    st, sp, raw, led = A.fake_run(d)
    r = rows(raw)
    check("fake run completes", st == "done" and len(r) == 2821 and all(x["status"] == "ok" for x in r), st)
    check("every call_id written once", len({x["call_id"] for x in r}) == 2821)
    order = [x["condition"] for x in r]
    check("all S1 lines after all S0 lines", order.index("S1") > max(i for i, c in enumerate(order) if c == "S0"))
    check("Fable lines carry a batch id", all(x.get("batch_id") for x in r if x["model_requested"] == "claude-fable-5-2"))
    check("costs recorded on every line", all(x["cost_usd"] > 0 for x in r))
    st2, _, raw2, _ = A.fake_run(d)
    check("resume sends nothing new", st2 == "done" and len(rows(raw2)) == 2821)

with tempfile.TemporaryDirectory() as d:
    st, sp, raw, led = A.fake_run(d, cap=5.0)
    spent = led.spent()
    check("budget guard halts under a small cap and never exceeds it", st in ("stop", "pause") and spent <= 5.0,
          f"{st} {spent}")

with tempfile.TemporaryDirectory() as d:
    raw = Path(d) / "r.jsonl"
    old = (datetime.now(timezone.utc) - timedelta(hours=A.S1_WINDOW_HOURS + 1)).isoformat()
    raw.write_text(json.dumps({"call_id": "x", "condition": "S1", "started_utc": old, "text": "", "status": "error"}) + "\n")
    s1specs = [s for s in specs if s["condition"] == "S1" and s["model"]["slot"] == "C2"][:3]
    sent = []
    A.DEADLINE = None
    st = A.run_collection(s1specs, A.BG.Ledger(raw, Path(d) / "s.json"), raw,
                          {"batch": lambda g, l, w: sent.extend(g) or "done",
                           "standard": lambda g, l, w: (A.run_sync(g, l, w, sender=lambda s: sent.append(s)) )},
                          log=lambda *a: None, write=lambda rec: None)
    check("no S1 request after the S1 window", st == "stop" and not sent, f"{st} {len(sent)}")
    A.DEADLINE = None

print(f"\n{'ALL PASS' if not FAILS else 'FAILED: ' + ', '.join(FAILS)}")
sys.exit(1 if FAILS else 0)
