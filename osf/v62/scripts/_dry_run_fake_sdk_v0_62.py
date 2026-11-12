"""v0.62 fake-SDK dry run of the acquisition (no network, no paid call), with adversarial cases.

r3 update (2026-11-12, runner lane v0.62 pre-lock): re-run after the r3 guard fix and with the adopted design
(pre-registrant's decision of 2026-11-12 00:48 CT, section 9 item 7 (b): blocks 1-3 + block 4 = 1,602 calls, the 88
yes/no brand questions per language last; block 5 not collected). r2's version of this script (git history, commit
f09068f) built the specs with drop_phase_a=True and recorded a 'drop_phase_a' approval, which switched the projection
pause off; this version takes the specs from acquire_v0_62.collection_specs (no approval recorded) and, at each resume,
builds a new Ledger from the raw and state files, as --collect does.
Fakes: _fakesdk_v0_62.py, a byte copy of the sibling lane's /tmp/aias_prelock_dryrun_1110/fakesdk.py (SHA-256
1fdb58fd2767c7f8a7a02465e3334fcb86f057b2f6e5da463b89c1747845afd7; r2 used the same file from /tmp).
Scenario 1 (adversarial, r2's plan on the category questions: transient failures, timeouts at MAX attempts, fatal 4xx,
empty answers re-sent once, refusals, truncation at the cap, served-model mismatch, English and Traditional-script
answers, expired and errored batch requests; plus yes/no cases), in stages with the pre-registrant's approvals:
(1) none; (2) --approve-projection; (3) --approve-past-80.
Scenario 2 (mild: answers at the fakes' default usage; adversarial cases on the yes/no questions only): one run.
Yes/no answers are prepared by code_v0_62.prepare_record and read by the certified parsers of this tree
(scripts/run_acquisition_v20-22.py parse_yes_no; osf/v19/acquire_v0_19.py parse_phase_a_response; the same git blobs as
at tag v0.42-prereg-r1). Output: osf/v62/prereg/dry_run_fake_sdk_v0_62_r3.txt (this script prints it)."""
import collections
import json
import os
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import _fakesdk_v0_62 as FK  # noqa: E402
FK.install()
os.environ.update({"ANTHROPIC_API_KEY": "fake", "OPENAI_API_KEY": "fake", "GOOGLE_API_KEY": "fake"})
import acquire_v0_62 as A  # noqa: E402
import budget_v0_62 as BG  # noqa: E402
import code_v0_62 as C  # noqa: E402
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "osf" / "v19"))
import run_acquisition_v20 as R20  # noqa: E402
import run_acquisition_v21 as R21  # noqa: E402
import run_acquisition_v22 as R22  # noqa: E402
import acquire_v0_19 as A19  # noqa: E402

PARSE = {"v20": R20.parse_yes_no, "v21": R21.parse_yes_no, "v22": R22.parse_yes_no,
         "v19": lambda t: {1: "yes", 0: "no", None: "ambiguous"}[A19.parse_phase_a_response(t)]}
NOSLEEP = (lambda *_: None)
A.time.sleep = NOSLEEP
A.PAUSE = collections.defaultdict(float)
RUNNERS = {"batch": lambda s, l, w: A.run_anthropic_batch(s, l, w, poll=0, sleep=NOSLEEP),
           "standard": lambda s, l, w: A.run_sync(s, l, w, sleep=NOSLEEP)}
TEXT = {"es": "Las mejores: Sennheiser, Audio-Technica y Sony; también Hennessy.",
        "ko": "추천: 젠하이저의 HD 800 S, 오디오 테크니카, 소니. 코스메틱은 아님.",
        "zh": "推荐森海塞尔、铁三角和索尼（ＳＯＮＹ）。"}
YES = {"es": "Sí, es una marca ampliamente reconocida.", "ko": "예, 널리 알려진 브랜드입니다.", "zh": "是的，这是一个广为人知的品牌。"}
NO = {"es": "No.", "ko": "아니요.", "zh": "否。"}
# a sentence BEFORE the answer word (the analogue of v1.15's JSON preamble): ES with and without the negation 'no'
PRE = {"es": ["Es una marca alemana con mucha historia. Sí.", "Denon no es tan conocida como Sony, pero sí, la reconozco."],
       "ko": ["젠하이저는 독일의 오디오 브랜드입니다. 예."], "zh": ["这是一个德国音频品牌。是。"]}
RATIO = A.projection_ratio(when_utc="2026-11-29T06:00:00")      # core + block 4, November (3.0975)


def plan(specs, adversarial_b=True, extra_ok=4):
    """FK.PLAN: per (model, prompt) a list of attempts consumed in order; `extra_ok` ok attempts at the end serve
    the re-sends of a resumed run."""
    FK.PLAN.clear(), FK.LOG.clear(), FK.BILL.clear()
    by_key = collections.defaultdict(list)
    for s in specs:
        by_key[(s["model"]["model_id"], s["prompt"])].append(s)
    cases, case_of = collections.Counter(), {}
    for i, ((m, prompt), ss) in enumerate(sorted(by_key.items())):
        lg, kind = ss[0]["language"], A.BLOCKS[ss[0]["block"]][0]
        q = []
        for j, s in enumerate(ss):
            sel = (i * 3 + j) % 23
            if kind == "A_yn":
                ok, c = {"kind": "ok", "text": YES[lg], "tin": 40, "tout": 12}, "plain yes"
                if sel in (1, 6, 11):
                    pre = PRE[lg][(i // 23) % len(PRE[lg])]
                    ok, c = dict(ok, text=pre), "preamble" + (" containing 'no'" if " no " in pre else "")
                elif sel == 2:
                    ok, c = dict(ok, text=NO[lg]), "plain no"
                elif sel == 3:
                    ok, c = dict(ok, text="Yes."), "English 'Yes.'"
                elif sel == 4:
                    q.append({"kind": "ok", "text": ""}); c = "empty -> re-sent once"
                elif sel == 5:
                    q.append({"kind": "expired"} if m == "claude-fable-5-2" else {"kind": "transient"})
                    c = "expired / transient -> re-sent"
                q.append(ok)
                cases[f"yes/no {lg}: {c}"] += 1
                case_of[(m, prompt)] = c
                continue
            ok = {"kind": "ok", "text": TEXT[lg], "tin": 60, "tout": 900}
            if not adversarial_b:
                q.append(ok)
                continue
            if m == "claude-fable-5-2":
                if sel == 1:
                    q += [{"kind": "expired"}, ok]; cases["fable expired -> resent"] += 1
                elif sel == 2:
                    q += [{"kind": "errored_transient"}, ok]; cases["fable errored transient -> resent"] += 1
                elif sel == 3:
                    q += [{"kind": "errored_fatal"}]; cases["fable errored fatal"] += 1
                elif sel == 4:
                    q += [{"kind": "ok", "text": ""}, ok]; cases["fable empty -> resent once"] += 1
                elif sel == 5:
                    q += [dict(ok, kind="trunc", tout=16384)]; cases["fable truncated at cap"] += 1
                else:
                    q.append(ok)
            else:
                if sel == 1:
                    q += [{"kind": "transient"}, {"kind": "transient"}, ok]; cases[m + " 2 transient -> ok"] += 1
                elif sel == 2:
                    q += [{"kind": "fatal"}]; cases[m + " fatal 4xx"] += 1
                elif sel == 3:
                    q += [{"kind": "transient"}] * A.MAX_ATTEMPTS; cases[m + " transient x MAX"] += 1
                elif sel == 4:
                    q += [{"kind": "ok", "text": ""}, ok]; cases[m + " empty -> resent once"] += 1
                elif sel == 5:
                    q += [dict(ok, served=m + "-preview")]; cases[m + " served-model mismatch"] += 1
                elif sel == 6:
                    q += [{"kind": "refusal"}, {"kind": "refusal"}]; cases[m + " refusal (empty) x2"] += 1
                elif sel == 7:
                    q += [dict(ok, kind="trunc", tout=16384)]; cases[m + " truncated at cap"] += 1
                elif sel == 8 and lg == "zh":
                    q += [dict(ok, text="推薦這些品牌們：森海塞爾。")]; cases["zh Traditional-script answer"] += 1
                elif sel == 9:
                    q += [dict(ok, text="The best are Sennheiser and Sony.")]; cases[m + " answer in English"] += 1
                else:
                    q.append(ok)
        q += [dict(q[-1]) if q and q[-1].get("kind") == "ok" and q[-1].get("text") else
              {"kind": "ok", "text": (YES[lg] if kind == "A_yn" else TEXT[lg]), "tin": 60, "tout": 900}] * extra_ok
        FK.PLAN[(m, prompt, "S0")] = q
    return cases, case_of


def lines(raw):
    return [json.loads(x) for x in raw.read_text(encoding="utf-8").splitlines() if x.strip()] if raw.exists() else []


def stage(raw, state, approvals, label):
    """One --collect invocation: a new Ledger from the raw and state files, approvals recorded, specs from
    collection_specs, then run_collection (resumable: answered calls are skipped, unanswered ones re-sent)."""
    ledger = BG.Ledger(raw, state, judge_reserve=BG.JUDGE_RESERVE_USD if A.open_on() else 0.0)
    for k, note in approvals:
        ledger.approve(k, note)
    specs = A.collection_specs(ledger)
    n0, logs = len(lines(raw)), []
    st = A.run_collection(specs, ledger, raw, RUNNERS, RATIO, log=logs.append)
    new = lines(raw)[n0:]
    halt = [x for x in logs if x.startswith(("HALT", "PAUSE"))]
    return {"stage": label, "approvals": [k for k, _ in approvals], "result": st, "specs": len(specs),
            "raw_lines_written": len(new), "lines_by_block_kind": dict(collections.Counter(A.kind_of(r) for r in new)),
            "spend_usd_after": round(ledger.spent(), 4), "halt": halt[-1][:160] if halt else None,
            "halt_reason": ledger.halt_reason}


def summary(raw, specs):
    recs = lines(raw)
    ok = {r["call_id"] for r in recs if r["status"] == "ok"}
    bill = 0.0
    for m, tin, tout, think in FK.BILL:
        pin, pout = BG.prices(m, "batch" if m == "claude-fable-5-2" else "standard", "2026-11-29")
        bill += (tin * pin + (tout + ((think or 0) if m == "gemini-4-argon" else 0)) * pout) / 1e6
    spent = sum(r["cost_usd"] for r in recs)
    kinds = {A.BLOCKS[s["block"]][0] for s in specs}
    return {"specs": len(specs), "raw_lines": len(recs), "status": dict(collections.Counter(r["status"] for r in recs)),
            "unique_calls_ok": len(ok), "unique_calls_ok_by_block_kind": {k: sum(1 for s in specs if s["call_id"] in ok
                                                                            and A.BLOCKS[s["block"]][0] == k) for k in sorted(kinds)},
            "requests_served_by_fakes": len(FK.LOG),
            "independent_bill_usd (Nov prices, requests with usage)": round(bill, 4),
            "ledger_spend_from_raw_usd": round(spent, 4), "worst_case_allowances_usd": round(spent - bill, 4),
            "worst_case_parts": sum(1 for r in recs for p in (r.get("usage_parts") or []) if p.get("worst_case"))}


def yes_no_coding(raw, case_of):
    """The block-4 answers as the coder prepares them, read by the certified parsers: label counts per case."""
    out = collections.defaultdict(collections.Counter)
    for r in lines(raw):
        if r["status"] != "ok" or A.kind_of(r) != "A_yn":
            continue
        p = C.prepare_record(r)
        c = case_of.get((r["model_requested"], r["prompt"]), "?")
        out[f"{r['language']} | {c}"][PARSE[r["substrate"]](p["text"])] += 1
    return {k: dict(v) for k, v in sorted(out.items())}


def main():
    out = {"design": A.design_key(), "projection_ratio_nov": round(RATIO, 4), "params": {
        "BRAND_EXTRAS": A.extras_on(), "BRAND_YES_NO": A.yes_no_on(), "HEADPHONES_OPTION": A.P.HEADPHONES_OPTION}}
    with tempfile.TemporaryDirectory() as d:                       # scenario 1: adversarial, staged approvals
        raw, state = Path(d) / "raw.jsonl", Path(d) / "state.json"
        specs = A.collection_specs(BG.Ledger(raw, state, judge_reserve=0.0))
        cases, case_of = plan(specs, adversarial_b=True)
        st = [stage(raw, state, [], "1: --collect"),
              stage(raw, state, [("projection", "dry run: continue after the projection pause")], "2: --approve-projection"),
              stage(raw, state, [("past_80", "dry run: continue past $80")], "3: --approve-past-80"),
              stage(raw, state, [], "4: --collect again (re-run pass)")]
        recs = lines(raw)
        yn_lines = [i for i, r in enumerate(recs) if A.kind_of(r) == "A_yn"]
        out["scenario_1_adversarial"] = {
            "stages": st, "summary": summary(raw, specs),
            "yes_no_lines_written": len(yn_lines),
            "category_lines_written_after_the_first_yes_no_line (re-sends in a later --collect)":
                sum(1 for i, r in enumerate(recs) if yn_lines and i > min(yn_lines) and A.kind_of(r) == "B"),
            "served_mismatch_lines": sum(1 for r in recs if r.get("served_model") and r["served_model"] != r["model_requested"]),
            "zh_traditional_flagged": sum(1 for r in recs if r["status"] == "ok" and r["language"] == "zh"
                                          and A.kind_of(r) == "B" and C.zh_traditional(r["text"])),
            "yes_no_coding": yes_no_coding(raw, case_of), "adversarial_cases": dict(sorted(cases.items()))}
    with tempfile.TemporaryDirectory() as d:                       # scenario 2: mild, block 4 reached
        raw, state = Path(d) / "raw.jsonl", Path(d) / "state.json"
        specs = A.collection_specs(BG.Ledger(raw, state, judge_reserve=0.0))
        cases, case_of = plan(specs, adversarial_b=False)
        st = [stage(raw, state, [], "1: --collect")]
        recs = lines(raw)
        kinds = [A.kind_of(r) for r in recs]
        fable_b4 = [r for r in recs if A.kind_of(r) == "A_yn" and r["model_requested"] == "claude-fable-5-2"]
        out["scenario_2_mild"] = {
            "stages": st, "summary": summary(raw, specs),
            "block_4_strictly_after_blocks_1_3": max(i for i, k in enumerate(kinds) if k == "B") <
                                                 min(i for i, k in enumerate(kinds) if k == "A_yn"),
            "fable_block4_batches": len({r["batch_id"] for r in fable_b4}),
            "fable_block4_requests_per_batch": sorted(collections.Counter(r["batch_id"] for r in fable_b4).values(), reverse=True),
            "yes_no_coding": yes_no_coding(raw, case_of), "adversarial_cases": dict(sorted(cases.items()))}
    return out


if __name__ == "__main__":
    res = main()
    text = ("# v0.62 fake-SDK dry run, r3 update (no network, no paid call). Script: osf/v62/scripts/_dry_run_fake_sdk_v0_62.py; "
            "fakes: osf/v62/scripts/_fakesdk_v0_62.py (SHA-256 1fdb58fd...45afd7). Design: blocks 1-3 + block 4 "
            "(section 9 item 7 (b)).\n" + json.dumps(res, indent=1, ensure_ascii=False) + "\n")
    if "--write" in sys.argv:
        (HERE.parent / "prereg" / "dry_run_fake_sdk_v0_62_r3.txt").write_text(text, encoding="utf-8")
    print(text, end="")
