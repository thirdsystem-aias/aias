#!/usr/bin/env python3
"""Tests for code_only_v0_40.py, audit_draw_v0_40.py and audit_ai_v0_40.py on SYNTHETIC data only (never study
data; no network; no provider SDK). Run: python3 osf/v40/scripts/test_audit_v0_40.py
The synthetic world is built from the frozen registry and probe set (as test_score_v0_40.py does)."""
import csv
import hashlib
import json
import random
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import score_v0_40 as S  # noqa: E402
import code_only_v0_40 as C  # noqa: E402
import audit_draw_v0_40 as D  # noqa: E402
import audit_ai_v0_40 as A  # noqa: E402

FAILS, N = [], [0]
FIXED = datetime(2026, 11, 23, 15, 0, tzinfo=timezone.utc)


def check(name, cond, detail=""):
    N[0] += 1
    print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if not cond and detail != "" else ""))
    if not cond:
        FAILS.append(name)


units, subjects = A.load_registry()
probes = json.loads((S.V40 / "prereg" / "probes_v0_40.json").read_text(encoding="utf-8"))["probes"]
SUBJ = {s["id"]: s for s in subjects}
INC_NAME = {"JPMC": "Chase", "BAC": "Bank of America", "AA": "American Airlines", "DL": "Delta Air Lines"}


def name(sid):
    return SUBJ[sid]["aliases"][0] if sid in SUBJ else INC_NAME[sid]


def world(seed=7):
    """Synthetic answers for every slot, condition, run and probe of the locked design (texts are invented)."""
    rng = random.Random(seed)
    recs = []
    for sl in S.TESTED_SLOTS + ["M5X"]:
        arm = "C" if sl.startswith("C") else "L"
        conds = (("S0", 3), ("S1", 1)) if arm == "C" else (("S0", 1 if sl == "M5X" else 3),)
        for cond, runs in conds:
            for run in range(1, runs + 1):
                for p in probes:
                    if cond == "S1" and not (p["kind"] == "recommendation" or p["tier"] == "S"):
                        continue
                    cat, sid = p["category"], p.get("subject_id")
                    if p["kind"] == "recommendation":
                        names = [u["aliases"][0] for u in units if u["category"] == cat and rng.random() < 0.4]
                        parts = [f"{n} is a solid choice" for n in names]
                        for g in [s for s in subjects if s["category"] == cat]:
                            if rng.random() < 0.15:
                                parts.append(rng.choice([f"{g['aliases'][0]} merged into another bank years ago",
                                                         f"{g['aliases'][0]} is still worth a look"]))
                        text = "Good options: " + ". ".join(parts) + "."
                    elif p["tier"] == "K":
                        text = f"{name(sid)} is a US company."
                    else:
                        text = rng.choice([f"{name(sid)} no longer exists.", f"Yes, {name(sid)} is open today.",
                                           "That brand was acquired some time ago; you would book with the successor."])
                    recs.append({"call_id": f"{sl}|{p['probe_id']}|{cond}|{run}", "arm": arm, "slot": sl,
                                 "condition": cond, "run": run, "probe_id": p["probe_id"], "tier": p["tier"],
                                 "kind": p["kind"], "category": cat, "brand_id": sid, "text": text, "status": "ok",
                                 "finish_reason": "stop", "output_tokens": 50,
                                 "search": {"n_searches": 1} if cond == "S1" else None})
    return recs


TMP = Path(tempfile.mkdtemp(prefix="v040_audit_test_"))
RAW = TMP / "raw.jsonl"
RECS = world()
RAW.write_text("".join(json.dumps(r) + "\n" for r in RECS), encoding="utf-8")
BASE = TMP / "codeonly"                              # plays the role of osf/v40 for the coding-only and audit steps
FULL = TMP / "fullrun"
(BASE / "prereg").mkdir(parents=True)
shutil.copy(S.V40 / "prereg" / "probes_v0_40.json", BASE / "prereg" / "probes_v0_40.json")

# ---- 1. coding-only step: locked scorer untouched, mentions identical to a full run's, no verdicts
check("locked scorer matches the lock manifest (score_v0_40.py)",
      C.sha256_file(HERE / "score_v0_40.py") == C.locked_sha("scripts/score_v0_40.py"))
check("locked stop-rule module matches the lock manifest", C.sha256_file(HERE / "stoprule_v0_40.py")
      == C.locked_sha("scripts/stoprule_v0_40.py"))
man = C.main(["--raw", str(RAW), "--out-dir", str(BASE)])
check("coding-only writes no verdict file", not list(BASE.rglob("*verdict*")) and man["verdicts_computed"] is False)
subprocess.run([sys.executable, str(HERE / "score_v0_40.py"), "--raw", str(RAW), "--out-dir", str(FULL),
                "--perms", "20"], check=True, capture_output=True)
a_bytes = (BASE / "data" / "v40_mentions.csv").read_bytes()
b_bytes = (FULL / "data" / "v40_mentions.csv").read_bytes()
check("coding-only v40_mentions.csv is byte-identical to the full run's (synthetic fixture)",
      a_bytes == b_bytes and len(a_bytes) > 1000, f"{len(a_bytes)} vs {len(b_bytes)} bytes")
check("full run did write verdicts (control)", (FULL / "v40_verdicts.json").exists())
check("manifest records the mentions file's SHA-256", man["outputs"]["v40_mentions.csv"]["sha256"]
      == hashlib.sha256(a_bytes).hexdigest())
coded_rows = D.read_csv(BASE / "data" / "v40_coded_answers.csv")
check("coded-answers frame has one row per kept answer", len(coded_rows) == man["answers_coded"] > 0)
try:
    C.main(["--raw", str(RAW), "--out-dir", str(FULL)])
    check("coding-only refuses when a verdict file exists", False)
except SystemExit as e:
    check("coding-only refuses when a verdict file exists", "verdict" in str(e))
bad_manifest = TMP / "bad_manifest.sha256"
bad_manifest.write_text("0" * 64 + "  osf/v40/scripts/score_v0_40.py\n", encoding="utf-8")
try:
    C.check_locked(bad_manifest)
    check("coding-only stops if the scorer differs from the lock manifest", False)
except SystemExit:
    check("coding-only stops if the scorer differs from the lock manifest", True)

# ---- 2. audit draw
check("allocation: proportional, largest remainder, sums to 100",
      D.allocate({"a": 50, "b": 30, "c": 20}, 100) == {"a": 50, "b": 30, "c": 20}
      and D.allocate({"a": 333, "b": 333, "c": 334}, 100) == {"a": 33, "b": 33, "c": 34}
      and sum(D.allocate({"x": 7, "y": 900, "z": 93}, 100).values()) == 100)
check("allocation: all units when the frame is not larger than the sample", D.allocate({"a": 40, "b": 20}, 100)
      == {"a": 40, "b": 20})
s1 = D.main(["--base", str(BASE)])
s2 = D.main(["--base", str(BASE)])
check("draw is deterministic (seed 4040) and re-running writes the same sample", s1["items"] == s2["items"])
check("draw: 100 recommendation + 100 status answers",
      sum(1 for x in s1["items"] if x["set"] == "recommendation") == 100
      and sum(1 for x in s1["items"] if x["set"] == "status") == 100)
ment = D.read_csv(BASE / "data" / "v40_mentions.csv")
with_subj = {m["call_id"] for m in ment if m["kind"] in ("ghost", "control")}
kinds = {r["call_id"]: r for r in coded_rows}
check("draw: every recommendation answer has a ghost or control mention",
      all(x["call_id"] in with_subj and kinds[x["call_id"]]["kind"] == "recommendation"
          for x in s1["items"] if x["set"] == "recommendation"))
check("draw: every status answer is an S answer", all(kinds[x["call_id"]]["tier"] == "S"
                                                       for x in s1["items"] if x["set"] == "status"))
check("draw: strata are arm|condition and arm|condition|role",
      {x["stratum"] for x in s1["items"] if x["set"] == "recommendation"} <= {"L|S0", "C|S0", "C|S1"}
      and all(x["stratum"].split("|")[2] in D.ROLES for x in s1["items"] if x["set"] == "status"))
alt = D.build_sample(coded_rows, ment, probes, seed=4041)
check("a different seed gives a different sample (the seed is used)", alt["items"] != s1["items"])
mf = (BASE / "audit" / "AUDIT_SAMPLE_v0_40.sha256").read_text(encoding="utf-8")
check("sample manifest lists the sample files and the inputs by SHA-256",
      "v40_audit_sample.json" in mf and "v40_mentions.csv" in mf and "probes_v0_40.json" in mf)
p = BASE / "audit" / "v40_audit_sample.json"
keep = p.read_text(encoding="utf-8")
p.write_text(keep.replace('"seed": 4040', '"seed": 1'), encoding="utf-8")
try:
    D.main(["--base", str(BASE)])
    check("draw refuses to overwrite a different existing sample", False)
except SystemExit:
    check("draw refuses to overwrite a different existing sample", True)
p.write_text(keep, encoding="utf-8")
(BASE / "v40_verdicts.json").write_text("{}", encoding="utf-8")
try:
    D.main(["--base", str(BASE)])
    check("draw refuses when a verdict file exists", False)
except SystemExit as e:
    check("draw refuses when a verdict file exists", "verdict" in str(e))
(BASE / "v40_verdicts.json").unlink()


# ---- 3. AI audit: reply rule, kappa, consensus, blindness, dry run, guard, resume (fake providers only)
ids = {"TZ", "AA"}
ok, _ = A.parse_reply('Sure. {"mentions": [{"entity": "TZ", "ambiguous": false, "gone_flag": true, '
                      '"successor_near": false}], "opening_says_gone": true} Done.', ids)
check("reply rule: one complete JSON object counts, surrounding text ignored",
      ok and ok["mentions"]["TZ"]["gone_flag"] is True and ok["opening_says_gone"] is True)
two = '{"mentions": [], "opening_says_gone": false} {"mentions": [], "opening_says_gone": true}'
check("reply rule: two objects with the required keys is invalid", A.parse_reply(two, ids)[0] is None)
check("reply rule: a missing required key is invalid", A.parse_reply('{"mentions": []}', ids)[0] is None)
check("reply rule: a truncated object is invalid", A.parse_reply('{"mentions": [', ids)[0] is None)
u, _ = A.parse_reply('{"mentions": [{"entity": "XX", "ambiguous": false, "gone_flag": false, "successor_near": false}],'
                     ' "opening_says_gone": false}', ids)
check("reply rule: an ID outside the list is dropped and counted", u["mentions"] == {} and u["unknown_entities"] == ["XX"])
kp = A.kappa([(1, 1)] * 40 + [(0, 0)] * 40 + [(1, 0)] * 10 + [(0, 1)] * 10)
check("Cohen's kappa and percent agreement (0.80 agreement, 0.50 chance -> 0.60)",
      abs(kp["percent_agreement"] - 80) < 1e-9 and abs(kp["kappa"] - 0.6) < 1e-12)
check("kappa undefined when there is no variation", A.kappa([(1, 1)] * 5)["kappa"] is None)
mk = lambda g: {"mentions": {"TZ": {"ambiguous": False, "gone_flag": g, "successor_near": False}},  # noqa: E731
                "opening_says_gone": False}
cons = A.consensus(mk(True), mk(True), None, ["TZ", "AA"])
check("consensus: A and B agree -> their code", cons["mentions"]["TZ"]["gone_flag"] is True and cons["named"]["AA"] is False)
cons = A.consensus(mk(True), mk(False), mk(False), ["TZ", "AA"])
check("consensus: A and B disagree -> the tie-breaker decides", cons["mentions"]["TZ"]["gone_flag"] is False)
cons = A.consensus(mk(True), None, mk(False), ["TZ", "AA"])
check("consensus: one coder missing and the others split -> unresolved", cons["mentions"]["TZ"]["gone_flag"] is None)
check("disagree(): any code difference sends the answer to the tie-breaker",
      A.disagree(mk(True), mk(False), ["TZ"]) and not A.disagree(mk(True), mk(True), ["TZ"]))

sample = A.verify_sample(BASE)
recs = S.load_raw(RAW)
items, ghost_ids = A.build_items(sample, recs, units, subjects, probes, D.read_csv(BASE / "data" / "v40_mentions.csv"))
check("items: 200 sampled answers with the locked coder's codes", len(items) == 200 and all("rule" in it for it in items))
it0 = items[0]
r_a = A.request_for(it0, units, subjects)
flipped = dict(it0, rule={"mentions": {"ZZ": {"ambiguous": True, "gone_flag": True, "successor_near": True}},
                          "status_flag": True})
check("blind: the request does not depend on the rule-based codes", A.request_for(flipped, units, subjects) == r_a)
check("blind: the user message is the answer text only", r_a["user"] == A.USER_TEMPLATE.format(text=it0["text"]))
kws = [A.request_kwargs(r, **r_a) for r in A.CODERS]


def texts(k):
    if "messages" in k:
        return k["system"], k["messages"][0]["content"]
    if "instructions" in k:
        return k["instructions"], k["input"]
    return k["config"]["system_instruction"], k["contents"]


check("same system prompt and user message for A, B and T", len({texts(k) for k in kws}) == 1
      and texts(kws[0]) == (r_a["system"], r_a["user"]))
check("no sampling parameter is sent to any coder",
      not any(f'"{w}"' in json.dumps(k) for k in kws for w in ("temperature", "top_p", "top_k")))
check("the system prompt carries no rule-based code or probe role",
      "ghost" not in r_a["system"].lower() and "incumbent" not in r_a["system"].lower()
      and "control" not in r_a["system"].lower())

# dry run: no network, no SDK import
saved = {k: sys.modules.get(k) for k in ("anthropic", "openai", "google", "google.genai")}
for k in saved:
    sys.modules[k] = None                      # any import of these now raises ImportError
try:
    dr = A.dry_run(BASE, items, recs, units, subjects, log=lambda *_: None)
    check("dry run builds every request without importing a provider SDK", "projection" in dr)
    dr2 = A.dry_run(BASE, None, recs, units, subjects, log=lambda *_: None)
    check("dry run works before the sample exists (length proxy)", dr2["projection"]["central"]["total"] > 0)
finally:
    for k, v in saved.items():
        if v is None:
            sys.modules.pop(k, None)
        else:
            sys.modules[k] = v



def perfect_reply(it, flip=False):
    """A reply that reproduces the rule-based codes (flip: invert the first gone-flag or the opening code)."""
    ms = [{"entity": e, **v} for e, v in it["rule"]["mentions"].items()]
    opening = bool(S.GONE_RE.search(it["text"][:2 * S.WINDOW]))
    if flip:
        if ms:
            ms[0] = dict(ms[0], gone_flag=not ms[0]["gone_flag"])
        else:
            opening = not opening
    return "Here is the coding:\n" + json.dumps({"mentions": ms, "opening_says_gone": opening})


class FakeBatch:
    """Fake batch APIs: A replies like the rule; B flips every 5th answer; usage fixed (1,000 in / 500 out)."""

    def __init__(self, items):
        self.by_cid = {}
        for it in items:
            for role in ("A", "B"):
                for pas in (1, 2):
                    self.by_cid[A.custom_id(role, it["call_id"], pas)] = (role, it)
        self.idx = {it["call_id"]: i for i, it in enumerate(items)}
        self.batches, self.submitted = {}, 0

    def submit(self, provider, items):
        self.submitted += len(items)
        bid = f"b{len(self.batches)}"
        self.batches[bid] = [cid for cid, _ in items]
        return bid

    def status(self, provider, bid):
        return True, "ended" if provider == "anthropic" else "completed"

    def results(self, provider, bid):
        out = {}
        for cid in self.batches[bid]:
            role, it = self.by_cid[cid]
            txt = perfect_reply(it, flip=(role == "B" and self.idx[it["call_id"]] % 5 == 0))
            if provider == "anthropic":
                body = {"content": [{"type": "text", "text": txt}], "model": "claude-fable-5-2", "stop_reason": "end_turn",
                        "usage": {"input_tokens": 1000, "output_tokens": 500}}
            else:
                body = {"output": [{"type": "message", "content": [{"type": "output_text", "text": txt}]}],
                        "model": "gpt-6.2-astra", "status": "completed",
                        "usage": {"input_tokens": 1000, "output_tokens": 500}}
            out[cid] = {"body": body, "error": None}
        return out


def fake_google(kw):
    it = next(x for x in items if A.USER_TEMPLATE.format(text=x["text"]) == kw["contents"])   # same text, same codes
    return {"text": perfect_reply(it), "served_model": "gemini-4-carbon", "finish_reason": "STOP",
            "tokens_in": 1000, "tokens_out": 200, "tokens_thought": 300}


RUNBASE = TMP / "runbase"
shutil.copytree(BASE, RUNBASE)
fb = FakeBatch(items)
au = A.Audit(RUNBASE, items, units, subjects, batch_client=fb, dispatch={"google": fake_google}, sim=True,
             now=lambda: FIXED, log=lambda *_: None)
stopped = au.run()
summ = au.summary()
flips = sum(1 for i in range(len(items)) if i % 5 == 0)
check("fake run completes under the cap", stopped is None and summ["complete"] and summ["spent_usd"] <= A.CAP_USD)
T_CALLS = [r["call_id"] for r in A.Audit._read(RUNBASE / "audit" / "ai_raw_v0_40.jsonl") if r["role"] == "T"]
check("tie-breaker called exactly for the answers where A and B disagree", sorted(T_CALLS) ==
      sorted(items[i]["call_id"] for i in range(len(items)) if i % 5 == 0) and len(T_CALLS) == flips)
exp = 200 * 2 * A.call_usd("claude-fable-5-2", 1000, 500, batch=True) + flips * A.call_usd("gemini-4-carbon", 1000, 500)
check("spend recomputed from recorded usage (batch at 50%, Google thinking billed as output)",
      abs(summ["spent_usd"] - exp) < 1e-6, f"{summ['spent_usd']} vs {exp}")
cr = summ["agreement"]["consensus_vs_rule"]
check("consensus of a rule-faithful A and tie-breaker agrees fully with the rule (gone-flag kappa 1 or n/a)",
      cr["gone_flag"]["all"]["percent_agreement"] == 100 and cr["subject"]["all"]["percent_agreement"] == 100)
check("threshold met -> no test marked", summ["threshold"]["met"] is True and summ["marked_tests"] == [])
check("B's flips show up in B vs rule", summ["agreement"]["B_vs_rule"]["gone_flag"]["all"]["percent_agreement"] < 100
      or summ["agreement"]["B_vs_rule"]["status_flag"]["all"]["percent_agreement"] < 100)
check("per-field output: n, percent agreement and kappa for every field",
      all(set(cr[f]["all"]) >= {"n", "percent_agreement", "kappa"} for f in A.FIELDS))
check("the report says there is no human check", summ["human_check"] is False)
A.write_outputs(RUNBASE, summ)
check("agreement files written", (RUNBASE / "audit" / "v40_audit_agreement.json").exists()
      and "No human check" in (RUNBASE / "audit" / "v40_audit_agreement.md").read_text(encoding="utf-8"))
au2 = A.Audit(RUNBASE, items, units, subjects, batch_client=fb, dispatch={"google": fake_google}, sim=True,
              now=lambda: FIXED, log=lambda *_: None)
before = fb.submitted
au2.run()
check("resume: a second run re-reads the records, recomputes spend and sends nothing new",
      fb.submitted == before and abs(au2.guard.spent - summ["spent_usd"]) < 1e-6)

# guard: a small cap stops the run before it could be exceeded
GB = TMP / "guardbase"
shutil.copytree(BASE, GB)
fb3 = FakeBatch(items)
au3 = A.Audit(GB, items, units, subjects, batch_client=fb3, dispatch={"google": fake_google}, cap=1.50, sim=True,
              now=lambda: FIXED, log=lambda *_: None)
st3 = au3.run()
check("guard: stops before the cap, never past it", st3 is not None and au3.guard.spent <= 1.50 + 1e-9
      and fb3.submitted < 400, f"spent {au3.guard.spent}, sent {fb3.submitted}")
check("guard: the summary records the stop and the run is incomplete", au3.summary()["complete"] is False
      and au3.summary()["guard_stopped"])


# threshold miss: AI codes that contradict the rule's gone-flags -> tests marked, coder not changed
bad = {r: {it["call_id"]: A.parse_reply(perfect_reply(dict(it, rule={"mentions": {
    e: dict(v, gone_flag=not v["gone_flag"]) for e, v in it["rule"]["mentions"].items()}, "status_flag": None})),
    set(it["cand_ids"]))[0] for it in items} for r in ("A", "B")}
miss = A.summarize(items, bad, ghost_ids, {"cap_usd": A.CAP_USD, "spent_usd": 0.0, "guard_stopped": None,
                                           "complete": True})
check("threshold miss (kappa < 0.80) marks H_Flag, H_Afterlife and H_Search and keeps the coder",
      miss["threshold"]["met"] is False and miss["marked_tests"] == ["H_Flag", "H_Afterlife", "H_Search"]
      and miss["mark"] == "coder reliability below threshold" and miss["coder_not_changed"] is True)
check("on a miss the analyst-coded rates of the sample are given beside the rule-coded ones",
      set(miss["sample_rates"]) == {"rule", "ai"}
      and miss["sample_rates"]["ai"]["status_ghost_answers"] > 0)
check("undefined kappa is read as not met", A.summarize(items[:1], {"A": {}, "B": {}}, ghost_ids,
      {"cap_usd": 25, "spent_usd": 0, "guard_stopped": None, "complete": False})["threshold"]["met"] is False)

shutil.rmtree(TMP, ignore_errors=True)
print(f"\n{N[0] - len(FAILS)} of {N[0]} checks pass" + (f"; FAILED: {FAILS}" if FAILS else ""))
sys.exit(1 if FAILS else 0)
