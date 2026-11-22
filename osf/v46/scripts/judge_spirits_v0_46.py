#!/usr/bin/env python3
"""judge_spirits_v0_46.py -- AIAS(TM) v0.46 (#76): the v0.23 recognition judge on the open spirits answers.

Stage 1 code r3, task 4. stage1_manuscript_r2.md section 3.4 ("Coding", "Judge model") and section 5.6 (MC_Judge):
the 72 open v0.23 Phase A answers (24 per model, block P2) are coded by the v0.23 recognition judge -- v0.23's
system prompt, user template, 3,000-character truncation, R0-R3 rubric and label parser, unchanged; recognised =
R1-R3 -- with the successor judge that passed v0.45's J1. Nothing is re-written here:
  * the judge call is score_v0_23.judge_recognition via v0.42's code_calls / code_v23_phase_a (blob 2d36735d), and
  * the model swap is v0.45's SuccessorJudgeClient (osf/v45/scripts/code_t5_v0_45.py), unchanged,
  * the judge is J1's recorded winner (osf/v45/data/judge_parity_J1_v0_45.json, key "judge"; MC_Judge). No winner
    -> nothing is coded, C_P is undefined for spirits and score_v0_46 leaves the 24 spirits units out (section 3.4).
Output: <coded dir>/v23_phase_a.csv in v0.42's table format (label = R level, recognized = 0/1) beside the tables
code_predictors_v0_46.py wrote, plus v23_judge_v0_46.json (judge, J1 source, requests, recorded usage, levels).

NO-CALL GUARD. --dry-run judges a synthetic fixture with a local fake client (no network, no key: API-key variables
are removed and `anthropic` is made unimportable before anything runs). --run is the only path that could build a
real client, and it refuses unless the lock tag v0.46-stage1-ipa exists (acquire_v0_46.lock_guard, checked locally
first) AND J1 names a winner. Stage 1 code never runs --run.

This script imports code_t5_v0_45 (which imports v0.42's coder): that coder re-executes the interpreter under a
~/aias shim when the worktree is not ~/aias, so the judge part runs only as `python3 judge_spirits_v0_46.py ...`,
never imported into another process. The pure helpers below (select_judge, v23_phase_a_lines, FakeJudge) import
nothing from v0.42 / v0.45 and can be imported.

Usage:
  python3 osf/v46/scripts/judge_spirits_v0_46.py --dry-run
  python3 osf/v46/scripts/judge_spirits_v0_46.py --run --raw osf/v46/data/v46_raw.jsonl --coded-dir osf/v46/data/coded
"""
import argparse
import csv
import json
import os
import sys
from collections import Counter
from pathlib import Path
from types import SimpleNamespace as NS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
V45_SCRIPTS = ROOT / "osf" / "v45" / "scripts"
J1_PATH = ROOT / "osf" / "v45" / "data" / "judge_parity_J1_v0_45.json"
CANDIDATES = ["claude-sonnet-5-5", "claude-sonnet-4-6"]      # = code_t5_v0_45.CANDIDATES (asserted in the child)
A_FIELDS = ["call_id", "substrate", "brand", "brand_id", "model", "condition", "run", "probe_id", "label",
            "recognized"]                                    # = code_t4_v0_42.A_FIELDS (asserted in the child)
EXPECTED_ANSWERS = 72


class JudgeHalt(RuntimeError):
    pass


def select_judge(j1_path=J1_PATH):
    """(model, reason). model is J1's recorded winner, or None (spirits left out, section 3.4)."""
    p = Path(j1_path)
    if not p.exists():
        return None, f"no J1 record ({p})"
    try:
        rec = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return None, f"J1 record unreadable: {e}"
    j = rec.get("judge")
    if not j:
        return None, "J1 names no winner (no candidate passed)"
    if j not in CANDIDATES:
        return None, f"J1 winner {j!r} is not a pre-registered candidate"
    if not (rec.get("verdict") or {}).get("pass"):
        return None, "J1 winner recorded without a passing verdict"
    return j, "J1 winner"


def v23_phase_a_lines(raw):
    """The open spirits answers: v46_raw predictor lines of substrate v23, phase A (block P2)."""
    return [r for r in raw if r.get("part", "predictor") == "predictor" and r.get("substrate") == "v23"
            and r.get("phase") == "A"]


class FakeJudge:
    """Local stand-in for anthropic.Anthropic() in --dry-run and tests: never touches the network. Replies R0 when
    the judged answer says it does not know the brand, R3 when it names a distillery, else R2."""

    def __init__(self):
        self.messages = self
        self.requests = []

    def create(self, **kw):
        self.requests.append(kw)
        user = kw["messages"][0]["content"].lower()
        lvl = "R0" if ("not familiar" in user or "don't know" in user) else ("R3" if "distillery" in user else "R2")
        return NS(content=[NS(type="text", text=lvl)], usage=NS(input_tokens=500, output_tokens=2),
                  stop_reason="end_turn")


# --------------------------------------------------------------------------- judge part (own process only)
def _v45():
    """code_t5_v0_45 (and through it v0.42's coder), checked against their pins. Re-executes this script under the
    ~/aias shim the first time when the worktree is not ~/aias (the argv and the key-stripped env are kept)."""
    sys.path.insert(0, str(V45_SCRIPTS))
    import code_t5_v0_45 as T
    ok, blob = T.coder_blob_ok()
    if not ok:
        raise JudgeHalt(f"v0.42 coder blob {blob} != pin {T.CODER_BLOB_PIN}")
    if list(T.CANDIDATES) != CANDIDATES or list(T.C.A_FIELDS) != A_FIELDS:
        raise JudgeHalt("v0.45 candidates or v0.42 table fields differ from this script's copy")
    return T


def judge_and_write(raw, coded_dir, model, inner, log=print):
    """Judge the open spirits answers of `raw` with `model` (through v0.45's SuccessorJudgeClient around `inner`) and
    write <coded_dir>/v23_phase_a.csv + v23_judge_v0_46.json. -> the judge record."""
    T = _v45()
    C = T.C
    coded_dir = Path(coded_dir)
    out = coded_dir / "v23_phase_a.csv"
    if out.exists():
        with open(out, newline="", encoding="utf-8") as f:
            if any(True for _ in csv.DictReader(f)):
                raise JudgeHalt(f"{out} already has coded rows; not overwritten")
    calls = C.dedupe_calls(v23_phase_a_lines(raw))
    answered = [r for r in calls if C.is_answered(r)]
    client = T.SuccessorJudgeClient(inner, model)
    A, _B = C.code_calls(answered, C.load_probe_map(), strip=True, judge_client=client)
    A = [r for r in A if r["substrate"] == "v0.23"]
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=A_FIELDS)
        w.writeheader()
        for r in A:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in A_FIELDS})
    rec = {"judge": model, "j1_source": str(J1_PATH.relative_to(ROOT)), "calls": len(calls),
           "answered": len(answered), "coded": len(A), "requests": len(client.log),
           "levels": dict(Counter(str(r["label"]) for r in A)),
           "recognized": sum(int(r["recognized"] or 0) for r in A),
           "r_err": sum(r["recognized"] is None for r in A),
           "input_tokens": sum(e.get("input_tokens") or 0 for e in client.log),
           "output_tokens": sum(e.get("output_tokens") or 0 for e in client.log)}
    (coded_dir / "v23_judge_v0_46.json").write_text(json.dumps(rec, indent=2, sort_keys=True), encoding="utf-8")
    log(f"[v46] spirits judge {model}: {rec['coded']} coded, levels {rec['levels']} -> {out}")
    return rec


def _block_network_and_keys():
    """Dry-run guard: drop API-key variables (also for the re-exec and child processes) and replace `anthropic` by a
    stub whose client refuses to be built (score_v0_23 imports anthropic at module level, so it must import)."""
    import types
    import code_predictors_v0_46 as CP
    for k in list(os.environ):
        if k not in CP.keyless_env({k: ""}):
            del os.environ[k]

    def _refuse(*_a, **_k):
        raise JudgeHalt("no-call guard: an API client was requested during a dry run")

    stub = types.ModuleType("anthropic")
    stub.Anthropic = stub.AsyncAnthropic = _refuse
    stub.__no_call_stub__ = True
    sys.modules["anthropic"] = stub


def dry_run(log=print):
    """Synthetic v46_raw -> v0.42 coder (task 3) -> spirits judge with FakeJudge -> predictors. -> fails"""
    import tempfile
    import code_predictors_v0_46 as CP
    import predictors_v0_46 as PR
    fails = []
    if CP.keyless_env() != dict(os.environ) or not getattr(sys.modules.get("anthropic"), "__no_call_stub__", False):
        fails.append("no-call guard not in place (API-key variables present or anthropic not stubbed)")
    raw, panel = CP.fixture_raw()
    for i, r in enumerate(v23_phase_a_lines(raw)):           # varied open answers for the fake judge
        r["text"] = ("I'm not familiar with this brand." if i % 4 == 0 else
                     "It is made at a well-known distillery." if i % 4 == 1 else "A respected premium label.")
    with tempfile.TemporaryDirectory(prefix="v46_judge_") as out:
        CP.run_v42_coder(raw, out, log=log)
        fake = FakeJudge()
        rec = judge_and_write(raw, out, "claude-sonnet-5-5", fake, log=log)
        ca, cb = PR.read_coded_dir(out)
    if (rec["coded"], rec["requests"], len(fake.requests)) != (EXPECTED_ANSWERS,) * 3:
        fails.append(f"coded/requests {rec['coded']}/{rec['requests']} != {EXPECTED_ANSWERS}")
    if rec["levels"] != {"R0": 18, "R3": 18, "R2": 36} or rec["recognized"] != 54:
        fails.append(f"levels {rec['levels']} recognized {rec['recognized']}")
    sent = fake.requests[0]
    if sent.get("model") != "claude-sonnet-5-5" or "temperature" in sent or sent.get("max_tokens") != 10:
        fails.append(f"request not v0.45's Sonnet 5.5 form: { {k: sent.get(k) for k in ('model', 'max_tokens')} }")
    pred, _meta = PR.compute(raw, ca, cb, [m["model_id"] for m in panel])
    n_sp = sum(1 for k, v in pred.items() if k[0] == "v0.23" and v["P"] is not None)
    log(f"  spirits units with P after the judge: {n_sp}")
    if n_sp != 24:
        fails.append(f"spirits P defined for {n_sp} units, not 24")
    return fails


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true", help="synthetic fixture, local fake judge; no model called")
    ap.add_argument("--run", action="store_true", help="real judge (refused before the lock)")
    ap.add_argument("--raw")
    ap.add_argument("--coded-dir")
    a = ap.parse_args(argv)
    try:
        if a.dry_run:
            _block_network_and_keys()
            _v45()                    # any ~/aias re-exec happens here, before work starts
            print("[v46] spirits judge dry run (fake client; keyless; no model called)")
            fails = dry_run()
            print(f"[v46] spirits judge dry run {'PASS' if not fails else 'FAIL: ' + '; '.join(fails)}")
            return 1 if fails else 0
        if not a.run:
            ap.error("--dry-run or --run")
        import acquire_v0_46 as A
        try:
            A.lock_guard()
        except A.Refused:
            print("[v46] REFUSED: not locked; the spirits judge makes paid calls only after the lock", file=sys.stderr)
            return 3
        model, why = select_judge()
        if model is None:
            print(f"[v46] spirits judge not run: {why}. C_P undefined for spirits; the 24 units are left out "
                  "(section 3.4).", file=sys.stderr)
            return 4
        if not (a.raw and a.coded_dir):
            ap.error("--run needs --raw and --coded-dir")
        _v45()
        raw = [json.loads(ln) for ln in open(a.raw, encoding="utf-8") if ln.strip()]
        import anthropic
        judge_and_write(raw, a.coded_dir, model, anthropic.Anthropic())
        return 0
    except JudgeHalt as e:
        print(f"[v46] HALT: {e}", file=sys.stderr)
        return 5


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    sys.exit(main())
