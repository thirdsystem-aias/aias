"""v0.62 r2 fake-SDK dry run of the acquisition (no network, no paid call), with adversarial cases.
Fakes: copy of the sibling lane's /tmp/aias_prelock_dryrun_1110/fakesdk.py (this dir)."""
import collections
import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/tmp/aias_v062_dryrun")
import fakesdk as FK  # noqa: E402
FK.install()
os.environ.update({"ANTHROPIC_API_KEY": "fake", "OPENAI_API_KEY": "fake", "GOOGLE_API_KEY": "fake"})
SCR = "/Users/pablou/aias/_worktrees/v0.62/osf/v62/scripts"
sys.path.insert(0, SCR)
import acquire_v0_62 as A  # noqa: E402
import budget_v0_62 as BG  # noqa: E402
import code_v0_62 as C  # noqa: E402

A.time.sleep = lambda *_: None
A.PAUSE = collections.defaultdict(float)
TEXT = {"es": "Las mejores: Sennheiser, Audio-Technica y Sony; también Hennessy.",
        "ko": "추천: 젠하이저의 HD 800 S, 오디오 테크니카, 소니. 코스메틱은 아님.",
        "zh": "推荐森海塞尔、铁三角和索尼（ＳＯＮＹ）。"}
specs = A.build_specs(A.load_probes(), drop_phase_a=True)
assert len(specs) == 810, len(specs)
# adversarial plan: per (model, prompt) a list consumed in run order
by_key = collections.defaultdict(list)
for s in specs:
    by_key[(s["model"]["model_id"], s["prompt"])].append(s)
cases = collections.Counter()
for i, ((m, prompt), ss) in enumerate(sorted(by_key.items())):
    lg = ss[0]["language"]
    q = []
    for j, s in enumerate(ss):
        ok = {"kind": "ok", "text": TEXT[lg], "tin": 60, "tout": 900}
        sel = (i * 3 + j) % 23
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
    FK.PLAN[(m, prompt, "S0")] = q

with tempfile.TemporaryDirectory() as d:
    raw, state = Path(d) / "raw.jsonl", Path(d) / "state.json"
    ledger = BG.Ledger(raw, state, judge_reserve=0.0)
    ledger.approve("drop_phase_a", "dry run: extras off")
    logs = []
    st = A.run_collection(specs, ledger, raw, {"batch": A.run_anthropic_batch, "standard": A.run_sync}, 3.0,
                          log=logs.append)
    recs = [json.loads(x) for x in raw.read_text(encoding="utf-8").splitlines() if x.strip()]
    status = collections.Counter(r["status"] for r in recs)
    done = {r["call_id"] for r in recs if r["status"] == "ok"}
    bill = 0.0
    for m, tin, tout, think in FK.BILL:
        pin, pout = BG.prices(m, "batch" if m == "claude-fable-5-2" else "standard", "2026-12-01")
        bill += (tin * pin + (tout + ((think or 0) if m == "gemini-4-argon" else 0)) * pout) / 1e6
    worst_parts = sum(1 for r in recs for p in (r.get("usage_parts") or []) if p.get("worst_case"))
    left = [p for q in FK.PLAN.values() for p in q]
    hits = []
    prepared = [C.prepare_record(r, hits=hits) for r in recs if r["status"] == "ok"]
    import re
    sen = sum(1 for p in prepared if re.search(r"\bSennheiser\b", p["text"]))
    koss = sum(1 for p in prepared if re.search(r"\bKoss\b", p["text"]))
    trad = sum(1 for p in prepared if p.get("zh_traditional"))
    offl = collections.Counter(p["language"] for p in prepared if p["in_language"] is False)
    out = {
        "result": st, "specs": len(specs), "raw_lines": len(recs), "status": dict(status),
        "unique_calls_ok": len(done), "calls_without_ok": len({s["call_id"] for s in specs} - done),
        "requests_served_by_fakes": len(FK.LOG), "planned_attempts_unused": len(left),
        "independent_bill_usd (Dec prices, requests with usage)": round(bill, 4),
        "ledger_calls_spent_usd": round(ledger.calls_spent(), 4),
        "ledger_minus_bill_usd (worst-case allowances)": round(ledger.calls_spent() - bill, 4),
        "worst_case_parts": worst_parts, "reserved_left": ledger.summary()["reserved_in_flight_usd"],
        "served_mismatch_lines": sum(1 for r in recs if r.get("served_model") and not r["served_model"] == r["model_requested"]),
        "truncated_lines": sum(1 for r in recs if str(r.get("finish_reason")) in ("max_tokens", "incomplete:max_output_tokens")),
        "coded_ok_answers_with_Sennheiser": sen, "Koss_false_matches": koss,
        "zh_traditional_flagged": trad, "off_language_flagged": dict(offl),
        "adversarial_cases": dict(cases),
    }
    print(json.dumps(out, indent=1, ensure_ascii=False))
    print("\n".join(logs[-3:]))
