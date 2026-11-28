#!/usr/bin/env python3
"""
length_check_v0_46.py -- AIAS v0.46 (#76): length-limit check for the two panel models the 2026-11-13 pre-lock check
did not cover (gpt-6.2-astra, gemini-4-carbon), as evidence for Section 3.10 (DEVIATIONS Entry 7; added after the
lock, ex ante: no #76 probe is sent, so no study data is collected early).

The programme's pre-lock length check (osf/v40/scripts/prelock_check_v0_40.py, run 2026-11-13, PASS) is repeated for
the new models with v0.46's own call functions and settings (Section 3.7: no system prompt, no tools, provider
defaults, max output 16,384 tokens; both models synchronous), on the same questions: v0.39's 24 published probes of
tiers G/C/R/K (osf/v39/prereg/probes_v0_39.json, each prompt checked against its recorded SHA-256), search off,
one answer per probe per model: 2 x 24 = 48 calls. A brand is a v0.39 registry brand found by v0.39's matcher.

Guard: the study's own budget_v0_45.Ledger (with the v0.46 price overlay, prices by request date; judge reserve
counted as spent; worst case reserved before each request, two per synchronous request), with its cap lowered for this
check to the judge reserve + CEILING_USD; the spend already in v46_raw.jsonl (none before the collection) is counted
too. Its raw lines go to osf/v46/data/v46_length_check_raw.jsonl, and acquire_v0_46.run() adds their cost to the
collection's Ledger, so the check counts toward the study's US$100 cap. Refused once the collection has started.
Stop: a model's first answer at the output limit (acquire_v0_46.at_limit; Google: output + thinking) pauses that model
(no further request) and the check reports it; the other model goes on (Section 3.10's stop rule would fire on an
answer cut before its outcome).
Paired comparison: the same 24 probes were answered by gpt-6-astra and gemini-4-argon under the same settings in the
2026-11-13 check (osf/v40/prereg/prelock_check_v0_40.jsonl at commit 456ba10, read from git); billed-output and
input ratios new/old are reported for the Section 3.9 recompute.

Modes: --dry-run (plan and estimate; no network), --run (PAID; resumable; then evaluates), --evaluate (no network).
Output: osf/v46/data/v46_length_check.json.
"""
import argparse
import hashlib
import json
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import acquire_v0_46 as A  # noqa: E402  (imports budget_v0_45 and the v0.46 price overlay; no network on import)

BG = A.BG
ROOT = A.ROOT
OSF = ROOT / "osf"
V39_PROBES = OSF / "v39" / "prereg" / "probes_v0_39.json"
V39_REGISTRY = OSF / "v39" / "registries" / "brands_commercial_roasters_v0.39.json"
V39_SCRIPTS = OSF / "v39" / "scripts"
LC_RAW = A.DATA / "v46_length_check_raw.jsonl"
LC_STATE = A.DATA / "v46_length_check_state.json"      # read for approvals only; never written by this check
RESULT = A.DATA / "v46_length_check.json"
TIERS = ("G", "C", "R", "K")
CEILING_USD = 10.00
COVERED_2026_11_13 = {"claude-fable-5-2", "gpt-6-astra", "gemini-4-argon"}
PRIOR_COMMIT, PRIOR_RAW = "456ba1018d3de884a4b339880d6e4a5797a3c871", "osf/v40/prereg/prelock_check_v0_40.jsonl"
PRIOR_MODEL = {"gpt-6.2-astra": "gpt-6-astra", "gemini-4-carbon": "gemini-4-argon"}


def load_questions(path=V39_PROBES):
    probes = [p for p in json.loads(Path(path).read_text(encoding="utf-8"))["probes"] if p["tier"] in TIERS]
    for p in probes:
        if hashlib.sha256(p["prompt"].encode("utf-8")).hexdigest() != p["sha256"]:
            raise A.Refused(f"v0.39 probe {p['probe_id']} does not match its recorded sha256")
    if len(probes) != 24:
        raise A.Refused(f"expected 24 v0.39 probes of tiers {TIERS}, found {len(probes)}")
    return probes


def new_models(panel_path=None):
    """The panel record's models not covered by the 2026-11-13 check (expected: M2_openai, M3_google)."""
    panel = A.panel_guard(panel_path)
    return [m for m in panel if m["model_id"] not in COVERED_2026_11_13]


def build_plan(questions=None, models=None):
    questions = load_questions() if questions is None else questions
    models = new_models() if models is None else models
    specs = []
    for m in models:
        for p in questions:
            specs.append({"call_id": f"LENGTHCHECK|v39:{p['probe_id']}|{m['slot']}|{m['model_id']}|S0|1",
                          "substrate": "v39-questions", "phase": "v0.46-length-check", "probe_id": "v39:" + p["probe_id"],
                          "brand_id": None, "frame_id": p["tier"], "model": m, "condition": "S0", "run": 1,
                          "block": "LC", "system": None, "prompt": p["prompt"],
                          "v46": {"part": "length_check", "block": "LC", "model": m["model_id"],
                                  "model_slot": m["slot"], "search_condition": "S0", "tier": p["tier"],
                                  "kind": p.get("kind")}})
    return specs


def prior_rows():
    """The 2026-11-13 check's answered S0 lines (git, commit 456ba10)."""
    txt = subprocess.run(["git", "-C", str(ROOT), "show", f"{PRIOR_COMMIT}:{PRIOR_RAW}"], capture_output=True,
                         text=True, check=True).stdout
    rows = [json.loads(l) for l in txt.splitlines() if l.strip()]
    return [r for r in rows if r.get("status") == "ok" and r.get("condition") == "S0"]


def billed_out(r):
    out = r.get("output_tokens") or 0
    if r.get("provider") == "google":
        out += r.get("thinking_tokens") or 0
    return out


def dry_run(log=print):
    specs = build_plan()
    pri = prior_rows()
    tot_c = tot_h = 0.0
    for m in sorted({s["model"]["model_id"] for s in specs}):
        old = [r for r in pri if r["model_requested"] == PRIOR_MODEL[m]]
        pin, pout = BG.prices(m, "standard")
        c = sum((r["input_tokens"] or 0) * pin + billed_out(r) * pout for r in old) / 1e6
        h = c * (3.0 if m == "gemini-4-carbon" else 1.5)
        tot_c, tot_h = tot_c + c, tot_h + h
        log(f"{m}: 24 calls; estimate on {PRIOR_MODEL[m]}'s 2026-11-13 tokens at today's price: ${c:.2f} "
            f"(high, x{3.0 if m == 'gemini-4-carbon' else 1.5}: ${h:.2f}); worst case per request "
            f"${BG.worst_case(m, 'S0', 'standard'):.4f} (x2 reserved)")
    log(f"TOTAL {len(specs)} calls: ${tot_c:.2f} (high ${tot_h:.2f}); ceiling ${CEILING_USD:.2f} + judge reserve "
        f"${BG.JUDGE_RESERVE_USD:.2f}; nothing sent.")
    return {"calls": len(specs), "estimate_usd": round(tot_c, 4), "high_usd": round(tot_h, 4)}


class AnyLimitStop(A.StopRule):
    """Stricter than Section 3.10 for this check: any answer at the output limit pauses its model."""

    def check(self, rec):
        if rec.get("status") == "error" or not A.at_limit(rec):
            return False
        with self.lock:
            self.paused.add(rec.get("model_slot"))
            A._journal(self.path, {"event": "trigger", "utc": A._now(), "model_slot": rec.get("model_slot"),
                                   "model": rec.get("model_requested"), "call_id": rec.get("call_id"),
                                   "finish_reason": rec.get("finish_reason"), "output_tokens": rec.get("output_tokens"),
                                   "thinking_tokens": rec.get("thinking_tokens"), "check": "length_check"})
        return True


def run(log=print, specs=None, sender=None, raw=LC_RAW, stop_path=None, guards=True):
    """PAID: send the plan under the study's Ledger class (cap lowered to reserve + CEILING_USD)."""
    if guards:
        if A.RAW_PATH.exists() and A.RAW_PATH.read_text(encoding="utf-8").strip():
            raise A.Refused("the v0.46 collection has started; the length check runs before it only")
        A.other_collection_guard()
        A.require_keys_v46()
    specs = build_plan() if specs is None else specs
    ledger = BG.Ledger(raw, LC_STATE, cap=BG.JUDGE_RESERVE_USD + CEILING_USD, pause_at=BG.PAUSE_AT_USD)
    ledger.settle(None, sum(BG.record_cost(r) for r in A._raw_lines(A.RAW_PATH)))
    stop = AnyLimitStop(stop_path or (A.DATA / "v46_length_check_stoprule.jsonl"))
    write = A.make_writer(raw, stop, log)
    done = A.done_ids(raw)
    groups = {}
    for s in specs:
        if s["call_id"] not in done:
            groups.setdefault(s["model"]["slot"], []).append(s)
    send = partial_sender(sender)
    with ThreadPoolExecutor(max_workers=max(1, len(groups))) as pool:
        res = list(pool.map(lambda kv: A.run_sync(kv[1], A.ModelLedger(ledger, stop, kv[0]), write, sender=send),
                            groups.items()))
    log(f"length check sending: {res}; {ledger.summary()}; paused: {sorted(stop.paused)}")
    return res, sorted(stop.paused)


def partial_sender(sender):
    return sender or A.send_call


def v39_named_fn():
    sys.path.insert(0, str(V39_SCRIPTS))
    import score_v0_39 as S39
    coder = S39.Coder(json.loads(V39_REGISTRY.read_text(encoding="utf-8")))
    return lambda text: len(coder.brand_matches(text or ""))


def _p90(xs):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(0.9 * len(xs)))] if xs else None


def evaluate(raw=LC_RAW, specs=None, named_fn=None, out=RESULT, write=True, prior=None):
    specs = build_plan() if specs is None else specs
    named_fn = named_fn or v39_named_fn()
    prior = prior_rows() if prior is None else prior
    planned = {s["call_id"]: s for s in specs}
    rows = [r for r in A._raw_lines(raw) if r.get("call_id") in planned]
    res = {"check": "v0.46 length check (Section 3.10 evidence; DEVIATIONS Entry 7)", "evaluated_utc": A._now(),
           "questions": f"v0.39 {V39_PROBES.name}, tiers {list(TIERS)}, search off", "limit": A.CURRENT_MAX_TOKENS,
           "models": {}, "raw": str(Path(raw).relative_to(ROOT)) if str(raw).startswith(str(ROOT)) else str(raw)}
    for mid in sorted({s["model"]["model_id"] for s in specs}):
        mine = [r for r in rows if r["model_requested"] == mid]
        ok = [r for r in mine if r.get("status") == "ok"]
        answered = {r["call_id"] for r in ok}
        at = [r for r in mine if r.get("status") in ("ok", "empty") and A.at_limit(r)]   # an empty answer too
        cut_before = [r["call_id"] for r in at if named_fn(r.get("text")) == 0]
        served = sorted({str(r.get("served_model")) for r in ok})
        old = {r["probe_id"]: r for r in prior if r["model_requested"] == PRIOR_MODEL[mid]}
        pairs = [(r, old[r["probe_id"]]) for r in ok if r["probe_id"] in old]
        bo_new, bo_old = [billed_out(a) for a, _ in pairs], [billed_out(b) for _, b in pairs]
        in_new, in_old = [a.get("input_tokens") or 0 for a, _ in pairs], [b.get("input_tokens") or 0 for _, b in pairs]
        res["models"][mid] = {
            "planned": sum(1 for s in specs if s["model"]["model_id"] == mid), "raw_lines": len(mine),
            "answered": len(answered), "errors_or_empty": [(r["call_id"], r.get("status"), (r.get("error") or "")[:160])
                                                           for r in mine if r.get("status") != "ok"],
            "missing": sorted(c for c, s in planned.items() if s["model"]["model_id"] == mid and c not in answered),
            "served_models": served, "served_equals_requested": all(s == mid or s.startswith(mid) for s in served),
            "finish_reasons": sorted({str(r.get("finish_reason")) for r in ok}),
            "at_limit": len(at), "cut_before_brand": cut_before,
            "named_zero": sum(1 for r in ok if named_fn(r.get("text")) == 0),
            "input_tokens": {"sum": sum(r.get("input_tokens") or 0 for r in ok), "max": max([r.get("input_tokens") or 0 for r in ok], default=None)},
            "output_tokens": {"sum": sum(r.get("output_tokens") or 0 for r in ok), "max": max([r.get("output_tokens") or 0 for r in ok], default=None)},
            "thinking_tokens": {"sum": sum(r.get("thinking_tokens") or 0 for r in ok), "max": max([r.get("thinking_tokens") or 0 for r in ok], default=None),
                                "reported_on": sum(1 for r in ok if r.get("thinking_tokens") is not None)},
            "billed_output": {"sum": sum(billed_out(r) for r in ok), "mean": (sum(billed_out(r) for r in ok) / len(ok)) if ok else None,
                              "p90": _p90([billed_out(r) for r in ok]), "max": max([billed_out(r) for r in ok], default=None)},
            "cost_usd": round(sum(r.get("cost_usd") or 0.0 for r in mine), 6),
            "paired_vs_2026_11_13": {
                "old_model": PRIOR_MODEL[mid], "pairs": len(pairs),
                "billed_output_ratio_of_sums": (sum(bo_new) / sum(bo_old)) if pairs and sum(bo_old) else None,
                "billed_output_ratio_of_p90": (_p90(bo_new) / _p90(bo_old)) if pairs and _p90(bo_old) else None,
                "input_ratio_of_sums": (sum(in_new) / sum(in_old)) if pairs and sum(in_old) else None,
                "old_billed_output_sum": sum(bo_old), "new_billed_output_sum": sum(bo_new)},
        }
    allm = res["models"].values()
    res["verdict"] = ("STOP" if any(m["at_limit"] for m in allm) else
                      "INCOMPLETE" if any(m["missing"] for m in allm) else "PASS")
    res["spend_usd"] = round(sum(m["cost_usd"] for m in allm), 6)
    if write:
        Path(out).write_text(json.dumps(res, indent=1, default=str) + "\n", encoding="utf-8")
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description="v0.46 length check for the new panel models (Section 3.10 evidence)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--run", action="store_true")
    g.add_argument("--evaluate", action="store_true")
    a = ap.parse_args(argv)
    try:
        if a.dry_run:
            dry_run()
            return 0
        if a.run:
            run()
        res = evaluate()
    except A.Refused:
        return 2
    for mid, m in res["models"].items():
        print(f"{mid}: answered {m['answered']}/{m['planned']}, at limit {m['at_limit']}, cut before brand "
              f"{len(m['cut_before_brand'])}, max billed output {m['billed_output']['max']}, cost ${m['cost_usd']:.4f}")
    print(f"verdict: {res['verdict']}; spend ${res['spend_usd']:.4f}")
    return {"PASS": 0, "STOP": 3, "INCOMPLETE": 4}[res["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
