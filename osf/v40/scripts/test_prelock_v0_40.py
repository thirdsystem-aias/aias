#!/usr/bin/env python3
"""Tests (mock only; nothing is sent) for the length-limit stop rule (stoprule_v0_40.py, section 4.7), its hooks in
acquire_v0_40.py, the pre-lock check (prelock_check_v0_40.py, section 4.8), the budget carry-over of the check's spend,
and the Discover switch (a) (section 3.2). Run: python3 test_prelock_v0_40.py"""
import json
import sys
import tempfile
from functools import partial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import acquire_v0_40 as A  # noqa: E402
import budget_v0_40 as BG  # noqa: E402
import prelock_check_v0_40 as P  # noqa: E402
import score_v0_40 as S  # noqa: E402
import stoprule_v0_40 as SR  # noqa: E402

FAILS = []
QUIET = lambda *a, **k: None  # noqa: E731


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if detail and not cond else ""))
    if not cond:
        FAILS.append(name)


def rows(p):
    p = Path(p)
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


def rec(slot, fr, text, out=500, thought=None, model=None, provider=None, status="ok", cond="S0"):
    arm = "C" if slot.startswith("C") else "L"
    return {"call_id": f"t|{slot}|{fr}|{out}|{thought}", "slot": slot, "arm": arm, "condition": cond, "status": status,
            "finish_reason": fr, "text": text, "output_tokens": out, "thinking_tokens": thought,
            "model_requested": model, "provider": provider}


NAMED = SR.v40_named_fn()
NAMED39 = P.v39_named_fn()

# ---------------------------------------------------------------- 1. the assessment (stoprule_v0_40)
check("limits are acquire's own (2,048 legacy, 16,384 current)",
      SR.LIMIT == {"L": A.LEGACY_MAX_TOKENS, "C": A.CURRENT_MAX_TOKENS} == {"L": 2048, "C": 16384})
stops = ["max_tokens", "length", "incomplete:max_output_tokens", "FinishReason.MAX_TOKENS", "MAX_TOKENS"]
normal = ["end_turn", "stop", "completed", "FinishReason.STOP", "pause_turn", "incomplete:content_filter"]
check("length stops recognised for all three providers", all(SR.is_length_stop(f) for f in stops))
check("normal finishes are not length stops", not any(SR.is_length_stop(f) for f in normal))
check("no finish reason -> None", SR.is_length_stop(None) is None and SR.is_length_stop("") is None)
a = SR.assess(rec("M6", "FinishReason.MAX_TOKENS", "When choosing a bank, consider fees, branches and", provider="google"), NAMED)
check("cut at the limit with no registry brand = cut_before_brand", a["cut_before_brand"] and not a["cut_after_brand"])
a = SR.assess(rec("M3", "length", "Delta Air Lines and Chase are often recommended, and", provider="openai"), NAMED)
check("cut at the limit after a registry brand = cut_after_brand", a["cut_after_brand"] and a["named"] >= 2)
a = SR.assess(rec("C2", "completed", "Delta Air Lines.", provider="openai"), NAMED)
check("normal finish is not at the limit", a["at_limit"] is False and not a["cut_before_brand"])
a = SR.assess(rec("M5X", None, "", out=1000, thought=1048, provider="google", status="empty"), NAMED)
check("no finish reason: Google visible + thinking >= 2,048 is at the limit; empty answer = cut before a brand",
      a["at_limit"] is True and a["cut_before_brand"])
a = SR.assess(rec("M3", None, "Chase.", out=2047, provider="openai"), NAMED)
check("no finish reason: 2,047 output tokens is below the limit", a["at_limit"] is False)
a = SR.assess(rec("M3", None, "Chase.", out=None, provider="openai"), NAMED)
check("neither finish reason nor tokens = unassessable", a["unassessable"] and a["at_limit"] is None)
check("error line carries no answer", SR.assess(rec("M3", None, "", status="error"), NAMED) is None)
a = SR.assess(rec("C1", "end_turn", "Chase.", out=9000, model="claude-fable-5-2", provider="anthropic"), NAMED)
check("Fable 5.2 (no separate thinking count): total output is the upper bound, 9,000 >= 8,192 flags",
      a["think_half"] and a["thinking_upper_bound"])
b = SR.assess(rec("C1", "end_turn", "Chase.", out=8191, model="claude-fable-5-2", provider="anthropic"), NAMED)
check("Fable 5.2 with 8,191 output tokens is not flagged", not b["think_half"])
check("GPT-6 Astra reasoning 8,192 of 16,384 flags, 8,191 does not",
      SR.assess(rec("C2", "completed", "Chase.", thought=8192, provider="openai"), NAMED)["think_half"]
      and not SR.assess(rec("C2", "completed", "Chase.", thought=8191, provider="openai"), NAMED)["think_half"])
check("Gemini 2.5 Flash thoughts 1,024 of 2,048 flags (legacy limit)",
      SR.assess(rec("M5X", "FinishReason.STOP", "Chase.", thought=1024, provider="google"), NAMED)["think_half"])
check("legacy Claude without a thinking parameter counts 0 thinking tokens",
      SR.assess(rec("M1", "end_turn", "Chase.", out=2000, model="claude-opus-4-5", provider="anthropic"), NAMED)["thinking"] == 0)

# ---------------------------------------------------------------- 2. the StopRule object
with tempfile.TemporaryDirectory() as d:
    j = Path(d) / "stop.jsonl"
    sr = SR.StopRule(NAMED, journal=j, log=QUIET)
    sr.observe(rec("M6", "MAX_TOKENS", "Consider fees and", provider="google"))
    sr.observe(rec("M5X", "MAX_TOKENS", "", provider="google", status="empty"))
    sr.observe(rec("M3", "length", "Chase is", provider="openai"))
    check("trigger pauses its slot", sr.is_paused("M6") and sr.paused_slots() == ["M6"])
    check("M5X (exempt) is journaled but not paused", not sr.is_paused("M5X")
          and any(e["event"] == "exempt" and e["slot"] == "M5X" for e in sr.events()))
    check("cut after a brand does not pause, is journaled as a flag", not sr.is_paused("M3")
          and any(e["event"] == "flag" and e["slot"] == "M3" for e in sr.events()))
    check("a pause survives a restart (journal)", SR.StopRule(NAMED, journal=j, log=QUIET).is_paused("M6"))
    sr.resume("M6", "test: pre-registrant resumes unchanged")
    check("a journaled resume lifts the pause after a restart", not SR.StopRule(NAMED, journal=j, log=QUIET).is_paused("M6"))
    w = sr.wrap(lambda r: None)
    check("wrapping the writer is idempotent", sr.wrap(w) is w)


# ---------------------------------------------------------------- 3. the hooks in acquire_v0_40 (fake providers)
ALL = A.build_specs(A.load_probes())


def mini_run(d, slots, legacy=None, current=None, batch_kw=None):
    saved = (dict(A.LEGACY_DISPATCH), dict(A.CURRENT_DISPATCH), dict(A.PAUSE))
    try:
        for k in A.LEGACY_DISPATCH:
            A.LEGACY_DISPATCH[k] = legacy or A.fake_legacy
        for k in A.CURRENT_DISPATCH:
            A.CURRENT_DISPATCH[k] = current or A.fake_current
        for k in A.PAUSE:
            A.PAUSE[k] = 0.0
        A.DEADLINE = None
        A.STOP = SR.StopRule(NAMED, journal=Path(d) / "stop.jsonl", log=QUIET)
        raw = Path(d) / "raw.jsonl"
        specs = [s for s in ALL if s["model"]["slot"] in slots]
        runners = {"batch": partial(A.run_anthropic_batch, client=A.fake_client(**(batch_kw or {})), poll=0,
                                    sleep=lambda s: None, journal=Path(d) / "b.jsonl"),
                   "standard": partial(A.run_sync, sleep=lambda s: None)}
        st = A.run_collection(specs, BG.Ledger(raw, Path(d) / "s.json"), raw, runners, log=QUIET,
                              write=A.make_writer(raw, log=QUIET))
        return st, specs, rows(raw), A.STOP.events()
    finally:
        A.LEGACY_DISPATCH.update(saved[0]); A.CURRENT_DISPATCH.update(saved[1]); A.PAUSE.update(saved[2])
        A.STOP, A.DEADLINE = None, None


def lite_cut(model_id, prompt):
    if model_id == "gemini-2.5-flash-lite":
        return {"text": "There are several factors to weigh before", "served_model": model_id, "finish_reason":
                "FinishReason.MAX_TOKENS", "tokens_in": 20, "tokens_out": 2048, "tokens_thought": None}
    return A.fake_legacy(model_id, prompt)


with tempfile.TemporaryDirectory() as d:
    st, sp, r, ev = mini_run(d, {"M4", "M6"}, legacy=lite_cut)
    m6 = [x for x in r if x["slot"] == "M6"]
    check("legacy: a cut-before-brand answer pauses its slot before its next request", st == "model_paused"
          and len(m6) == 1, f"{st} {len(m6)}")
    check("legacy: the other slot completes all its calls", sum(x["slot"] == "M4" for x in r) == 282)
    check("legacy: the trigger is journaled", [e["slot"] for e in ev if e["event"] == "trigger"] == ["M6"])

with tempfile.TemporaryDirectory() as d:
    st, sp, r, ev = mini_run(d, {"C1", "C3"}, batch_kw={"stop_reason": "max_tokens",
                                                       "text": lambda m, p, s: "Let me think about the options"})
    c1 = [x for x in r if x["slot"] == "C1"]
    check("Fable 5.2 (batch): the pause takes effect from its next batch (94 lines of block 5, nothing after)",
          st == "model_paused" and len(c1) == 94 and {x["run"] for x in c1} == {1}
          and {x["condition"] for x in c1} == {"S0"}, f"{st} {len(c1)}")
    check("current: the other slot completes (S0 x3 + S1)", sum(x["slot"] == "C3" for x in r) == 345)

with tempfile.TemporaryDirectory() as d:
    st, *_ = mini_run(d, {"M1", "C2"})
    check("no cut answer: the run ends 'done' with nothing paused", st == "done")
    st2, _, r2, _ = A.fake_run(d)
    check("full fake run with the stop rule active still completes 2,821 calls", st2 == "done" and len(rows(r2)) == 2821)

# ---------------------------------------------------------------- 4. budget: the check's spend counts toward the cap
with tempfile.TemporaryDirectory() as d:
    f = Path(d) / "pre.jsonl"
    line = {"model_requested": "gpt-6-astra", "condition": "S0", "started_utc": "2026-11-14T00:00:00+00:00",
            "usage_parts": [{"mode": "standard", "input_tokens": 1000, "output_tokens": 1000, "n_searches": 0}]}
    f.write_text(json.dumps(line) + "\n" + json.dumps(line) + "\n")
    check("spend_of sums the recorded cost of every line", abs(BG.spend_of(f) - 2 * BG.record_cost(line)) < 1e-12
          and BG.spend_of(Path(d) / "missing.jsonl") == 0.0)
    led = BG.Ledger(Path(d) / "raw.jsonl", Path(d) / "s.json", prior_usd=99.9)
    check("prior spend counts as spent and in the summary", abs(led.spent() - 99.9) < 1e-9
          and led.summary()["prior_usd"] == 99.9)
    led.approve("past_80", "test")
    check("prior spend blocks a request that could pass $100", led.reserve(0.5)[0] == "stop")
    led2 = BG.Ledger(Path(d) / "raw.jsonl", Path(d) / "s2.json", prior_usd=80.0)
    check("prior spend reaches the $80 pause", led2.reserve(0.01)[0] == "pause")
    try:
        A.prelock_guard(Path(d) / "none.json")
        ok = False
    except SystemExit:
        ok = True
    (Path(d) / "pass.json").write_text(json.dumps({"verdict": "PASS"}))
    check("--collect refuses without a passed pre-lock check, accepts PASS",
          ok and A.prelock_guard(Path(d) / "pass.json") == "PASS")

# ---------------------------------------------------------------- 5. the pre-lock check (prelock_check_v0_40)
plan = P.build_plan()
v40_prompts = {p["prompt"] for p in A.load_probes()}
v39 = {p["prompt"] for p in json.loads(P.V39_PROBES.read_text(encoding="utf-8"))["probes"]}
check("plan: 258 calls = 10 settings x 24 search off + 3 x 6 search on",
      len(plan) == 258 and sum(s["condition"] == "S0" for s in plan) == 240
      and sum(s["condition"] == "S1" for s in plan) == 18)
check("plan: every question is a published v0.39 probe, none is a v0.40 probe",
      all(s["prompt"] in v39 for s in plan) and not any(s["prompt"] in v40_prompts for s in plan))
check("plan: the study's own settings (acquire's PANEL entries; S1 on C1-C3 only, G1-G6)",
      all(s["model"] in A.PANEL for s in plan)
      and {(s["model"]["slot"], s["probe_id"]) for s in plan if s["condition"] == "S1"}
      == {(m["slot"], f"v39:G{i}") for m in A.CURRENT for i in range(1, 7)})
boom = {"n": 0}


def no_network(*a, **k):
    boom["n"] += 1
    raise AssertionError("network call in a dry run")


saved = (dict(A.LEGACY_DISPATCH), dict(A.CURRENT_DISPATCH))
for k in A.LEGACY_DISPATCH:
    A.LEGACY_DISPATCH[k] = no_network
for k in A.CURRENT_DISPATCH:
    A.CURRENT_DISPATCH[k] = no_network
out = []
dr = P.dry_run(log=out.append)
A.LEGACY_DISPATCH.update(saved[0]); A.CURRENT_DISPATCH.update(saved[1])
check("dry run sends nothing and imports no provider SDK", boom["n"] == 0
      and not any(m in sys.modules for m in ("anthropic", "openai", "google.genai")) and out[-1] == "nothing sent.")
check("dry run cost from the study's basis: $5.91 central, $14.93 high, 258 calls",
      dr["calls"] == 258 and round(dr["central_usd"], 2) == 5.91 and round(dr["high_usd"], 2) == 14.93, dr)
check("the check's own ceiling covers its high estimate", P.CEILING_USD >= dr["high_usd"])


def fake_check(d, legacy_google=None, legacy_openai=None):
    """Run the check's plan through acquire's runners with fake providers; return the evaluation."""
    saved = (dict(A.LEGACY_DISPATCH), dict(A.CURRENT_DISPATCH), dict(A.PAUSE))
    try:
        for k in A.LEGACY_DISPATCH:
            A.LEGACY_DISPATCH[k] = A.fake_legacy
        if legacy_google:
            A.LEGACY_DISPATCH["google"] = legacy_google          # M5X and M6 (M5 uses google_budget0)
        if legacy_openai:
            A.LEGACY_DISPATCH["openai"] = legacy_openai          # M3, M4
        for k in A.CURRENT_DISPATCH:
            A.CURRENT_DISPATCH[k] = A.fake_current
        for k in A.PAUSE:
            A.PAUSE[k] = 0.0
        raw = Path(d) / "pre.jsonl"
        runners = {"batch": partial(A.run_anthropic_batch, client=A.fake_client(), poll=0, sleep=lambda s: None,
                                    journal=Path(d) / "b.jsonl"),
                   "standard": partial(A.run_sync, sleep=lambda s: None)}
        st = P.run(raw=raw, state=Path(d) / "s.json", runners=runners, log=QUIET, guards=False)
        return st, P.evaluate(raw=raw, out=Path(d) / "res.json", named_fn=NAMED39), raw
    finally:
        A.LEGACY_DISPATCH.update(saved[0]); A.CURRENT_DISPATCH.update(saved[1]); A.PAUSE.update(saved[2])


def cut(model_id, prompt, text, fr):
    return {"text": text, "served_model": model_id, "finish_reason": fr, "tokens_in": 20, "tokens_out": 2048,
            "tokens_thought": 1500 if model_id == "gemini-2.5-flash" else None}


with tempfile.TemporaryDirectory() as d:
    st, res, raw = fake_check(d)
    check("mocked check, no answer at the limit: PASS, 258 answers", st == "done" and res["verdict"] == "PASS"
          and sum(v.get("answers", 0) for v in res["by_setting"].values()) == 258, res["verdict"])
    check("the check's spend is recorded and carried into the collection ledger",
          res["spend_usd"] > 0 and abs(BG.Ledger(Path(d) / "x.jsonl", Path(d) / "x.json",
                                                 prior_usd=BG.spend_of(raw)).spent() - BG.spend_of(raw)) < 1e-12)
    check("resume: a second --run sends nothing new", P.run(raw=raw, state=Path(d) / "s.json", runners={
        "batch": lambda g, l, w: (_ for _ in ()).throw(AssertionError("sent")),
        "standard": lambda g, l, w: (_ for _ in ()).throw(AssertionError("sent"))}, log=QUIET, guards=False) == "done")

with tempfile.TemporaryDirectory() as d:
    g = lambda m, p: cut(m, p, "Roasting in-house depends on volume and" if m == "gemini-2.5-flash-lite"  # noqa: E731
                         else "", "FinishReason.MAX_TOKENS")
    st, res, raw = fake_check(d, legacy_google=g)
    slots = {b["call_id"].split("|")[3] for b in res["blockers"]}
    check("M6 cut before a v0.39 brand: BLOCKED, 24 blockers, all M6", res["verdict"] == "BLOCKED"
          and len(res["blockers"]) == 24 and slots == {"M6"}, (res["verdict"], len(res["blockers"]), slots))
    check("M5X cut before a brand is reported, never a blocker (exempt)",
          any(f["exempt"] and f["cut_before_brand"] for f in res["flagged_not_blocking"]))

with tempfile.TemporaryDirectory() as d:
    o = lambda m, p: cut(m, p, "Loring and Diedrich both make shop roasters, and", "length")  # noqa: E731
    st, res, raw = fake_check(d, legacy_openai=o)
    check("cut after naming a v0.39 brand: not a blocker (PASS), flagged for section 5.9",
          res["verdict"] == "PASS" and sum(f["cut_after_brand"] for f in res["flagged_not_blocking"]) == 48,
          (res["verdict"], len(res["flagged_not_blocking"])))
    keep = [l for l in Path(raw).read_text(encoding="utf-8").splitlines() if "|M1|" not in l]
    Path(raw).write_text("\n".join(keep) + "\n")
    check("missing answers: INCOMPLETE", P.evaluate(raw=raw, write=False, named_fn=NAMED39)["verdict"] == "INCOMPLETE")

# ---------------------------------------------------------------- 6. Discover switch (a): text, config, scorer
import build_probes_v0_40 as BP  # noqa: E402

subs = BP.subjects()
out_subs, status = BP.apply_discover_switch(subs, BP.DISCOVER_OPTION, BP.DISCOVER_REPLACEMENT)
check("config: DISCOVER_OPTION is 'a'", BP.DISCOVER_OPTION == "a" and BP.DISCOVER_REPLACEMENT is None)
check("final build under (a) keeps Discover as the bank living-brand control",
      out_subs == subs and "Discover kept" in status
      and any(s["subject_id"] == "DISCOVER" and s["role"] == "control" for s in out_subs))
units, subjects, _ = S.load_registry()
check("scorer under (a): Discover is a control, no replacement control is added",
      S.switch_controls(subjects) == [] and any(s["id"] == "DISCOVER" and s["role"] == "control" for s in subjects))
pre = (Path(__file__).resolve().parents[1] / "prereg" / "PRE_REGISTRATION_v0_40.md").read_text(encoding="utf-8")
check("pre-registration text: Discover switch decided (a), no 'PENDING PABLO (a/b)' left",
      "PENDING PABLO (a/b)" not in pre and "DECIDED (a)" in pre)

print(f"\n{'ALL PASS' if not FAILS else 'FAILED: ' + ', '.join(FAILS)}")
sys.exit(1 if FAILS else 0)
