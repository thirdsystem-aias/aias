#!/usr/bin/env python3
"""
prelock_check_v0_40.py -- AIAS(TM) v0.40: the pre-lock length check (PRE_REGISTRATION_v0_40.md section 4.8).

Rule (the pre-registrant, 2026-11-12, 11:36 pm CT): no lock while any model's answer, under the study's own call
settings, stops at the length limit before naming a brand; tested on questions from an already-published category, so
no study data is collected early.

Questions: v0.39 (commercial coffee roasters), whose pre-registration, probe set, registry and answers are public on
OSF (ec6wh -> v39): its 24 probes that ask for or name a brand -- tiers G (6 cafe-roaster recommendations), C (6 under
an infrastructure constraint), R (6 production-roastery recommendations) and K (6 questions naming one roaster) --
verbatim from osf/v39/prereg/probes_v0_39.json (each prompt checked against its recorded sha256). The six F (frame)
probes ask for no brand and are not used. No v0.40 probe is sent.
Settings: acquire_v0_40.py's own call functions and request builders (same output limits, thinking settings,
temperature, tools and SDK calls; Claude Fable 5.2 through the Message Batches API), one answer per probe:
  search off: M1-M6, M5X and C1-C3 on the 24 probes      10 x 24 = 240 calls
  search on:  C1-C3 on the six G probes (G1-G6)            3 x 6  =  18 calls          258 calls in all
Assessment: stoprule_v0_40.assess; a brand is a v0.39 registry brand found by v0.39's own matcher
(score_v0_39.Coder.brand_matches, context exclusions included).
Verdict: BLOCKED when any answer of a non-exempt setting stops at the length limit before naming a brand, or records
neither a finish reason nor output tokens; INCOMPLETE while any planned call has no answer (re-run --run: it resumes);
otherwise PASS. Answers cut after a brand, and answers whose thinking reaches half the limit, do not block: their
handling is declared in section 5.9 and they are listed. M5X (the reported-only pass at the v0.39 setting) is assessed
and reported but cannot block (stoprule_v0_40.EXEMPT; PENDING PABLO).
Cost: the study's own per-call basis, prereg/cost_estimate_v0_40.txt (current arm: t4's recorded cost per completed
record, category questions "B" for recommendation probes and for every search-on call, brand questions "A" for K
probes, as section 6.2 maps them; legacy arm: v0.39's recorded tokens at the study's prices). The check's spend counts
toward the study's $100 cap: acquire_v0_40.py --collect carries it into its budget ledger. The check's own guard stops
before its spend could pass CEILING_USD.

Modes:
  --dry-run    print the planned calls and their estimated cost; no network call and no API key needed
  --run        PAID (approved by the pre-registrant, 2026-11-12): send the plan, resumable; refused once the v0.40
               collection has started; then evaluates
  --evaluate   assess the recorded answers (no network) and write prereg/prelock_check_v0_40.json
"""
import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import acquire_v0_40 as A  # noqa: E402  (no network on import)
import budget_v0_40 as BG  # noqa: E402
import stoprule_v0_40 as SR  # noqa: E402

V40 = HERE.parent
OSF = V40.parent
V39_PROBES = OSF / "v39" / "prereg" / "probes_v0_39.json"
V39_REGISTRY = OSF / "v39" / "registries" / "brands_commercial_roasters_v0.39.json"
V39_SCRIPTS = OSF / "v39" / "scripts"
COST_TXT = V40 / "prereg" / "cost_estimate_v0_40.txt"
RAW = A.PRELOCK_RAW                                      # prereg/prelock_check_v0_40.jsonl
RESULT = A.PRELOCK_RESULT                                # prereg/prelock_check_v0_40.json
STATE = V40 / "prereg" / "prelock_budget_state_v0_40.json"
JOURNAL = V40 / "prereg" / "prelock_batches_v0_40.jsonl"
S0_TIERS = ("G", "C", "R", "K")
S1_TIERS = ("G",)
CEILING_USD = 20.00      # the plan's high estimate ($14.93) plus one worst-case GPT-6 Astra search-on reservation
LEGACY_BASIS = {"M1": ("claude-opus-4-5", "std"), "M2": ("claude-sonnet-4-5", "std"), "M3": ("gpt-4o", "std"),
                "M4": ("gpt-4o-mini", "std"), "M5": ("gemini-2.5-flash", "budget0"),
                "M5X": ("gemini-2.5-flash", "v039"), "M6": ("gemini-2.5-flash-lite", "std")}


def load_questions(path=V39_PROBES):
    raw = Path(path).read_bytes()
    probes = [p for p in json.loads(raw.decode("utf-8"))["probes"] if p["tier"] in S0_TIERS]
    for p in probes:
        if hashlib.sha256(p["prompt"].encode("utf-8")).hexdigest() != p["sha256"]:
            sys.exit(f"ABORT: v0.39 probe {p['probe_id']} does not match its recorded sha256")
    if len(probes) != 24:
        sys.exit(f"ABORT: expected 24 v0.39 probes of tiers {S0_TIERS}, found {len(probes)}")
    return probes


def _spec(m, p, cond):
    return {"call_id": f"PRELOCK|{m['arm']}|v39:{p['probe_id']}|{m['slot']}|{m['model_id']}|{cond}|1",
            "substrate": "v39-questions", "phase": "v0.40-prelock", "arm": m["arm"], "probe_id": "v39:" + p["probe_id"],
            "tier": p["tier"], "kind": p["kind"], "category": "commercial coffee roasters (v0.39, published)",
            "brand_id": None, "frame_id": p["tier"], "model": m, "condition": cond, "run": 1,
            "block": 0 if cond == "S0" else 1, "system": None, "prompt": p["prompt"]}


def build_plan(questions=None):
    """Search off: every panel slot (A.PANEL: M1-M6, M5X, C1-C3) on every question; then search on: C1-C3 on G1-G6."""
    questions = load_questions() if questions is None else questions
    specs = [_spec(m, p, "S0") for m in A.PANEL for p in questions]
    specs += [_spec(m, p, "S1") for m in A.CURRENT for p in questions if p["tier"] in S1_TIERS]
    return specs


def cost_basis(path=COST_TXT):
    """Per-call (central, high) USD from the study's own estimate record."""
    t4, v39 = {}, {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s+([a-z][\w.-]+)\s+([AB])\s+(S[01])\s+n=\s*\d+\s+ok=\s*\d+\s+([\d.]+)\s*/\s*([\d.]+)\s*$", line)
        if m:
            t4[(m[1], m[2], m[3])] = (float(m[4]), float(m[5]))
            continue
        m = re.match(r"^\s+v0\.39\s+(\S+)\s+(\S+)\s+([\d.]+)\s*/\s*([\d.]+)\s*$", line)
        if m:
            v39[(m[1], m[2])] = (float(m[3]), float(m[4]))
    return t4, v39


def call_cost(spec, t4, v39):
    m = spec["model"]
    if m["arm"] == "L":
        return v39[LEGACY_BASIS[m["slot"]]]
    phase = "B" if spec["kind"] == "recommendation" or spec["condition"] == "S1" else "A"
    return t4[(m["model_id"], phase, spec["condition"])]


def dry_run(log=print):
    """Planned calls and estimated cost. Sends nothing; needs no API key."""
    qs = load_questions()
    specs = build_plan(qs)
    t4, v39 = cost_basis()
    rows = defaultdict(lambda: [0, 0.0, 0.0])
    for s in specs:
        c, h = call_cost(s, t4, v39)
        r = rows[(s["model"]["slot"], s["model"]["model_id"], s["condition"])]
        r[0] += 1
        r[1] += c
        r[2] += h
    log(f"pre-lock check (section 4.8): questions from v0.39 ({V39_PROBES.name}, sha256 "
        f"{hashlib.sha256(V39_PROBES.read_bytes()).hexdigest()}), tiers {'/'.join(S0_TIERS)}: {len(qs)} probes; "
        f"search on: tiers {'/'.join(S1_TIERS)}")
    log(f"{'slot':4s} {'model':22s} {'cond':4s} {'calls':>5s} {'central $':>10s} {'high $':>8s}")
    for (slot, model, cond), (n, c, h) in rows.items():
        note = "  (exempt from the block; reported)" if slot in SR.EXEMPT else ""
        log(f"{slot:4s} {model:22s} {cond:4s} {n:5d} {c:10.4f} {h:8.4f}{note}")
    n, c, h = len(specs), sum(r[1] for r in rows.values()), sum(r[2] for r in rows.values())
    log(f"TOTAL {n} calls: central ${c:.2f}, high ${h:.2f} (basis: {COST_TXT.name}); own ceiling ${CEILING_USD:.2f}; "
        f"counts toward the study's ${BG.BUDGET_CAP_USD:.0f} cap")
    log("nothing sent.")
    return {"calls": n, "central_usd": round(c, 4), "high_usd": round(h, 4),
            "by_condition": dict(Counter(s["condition"] for s in specs))}


def run(specs=None, raw=RAW, state=STATE, journal=JOURNAL, runners=None, ceiling=CEILING_USD, log=print, guards=True):
    """PAID. Sends the plan through acquire_v0_40's own runners (batch for Claude Fable 5.2, synchronous otherwise),
    search off first, then search on; resumable (calls already answered are skipped)."""
    if guards:
        if A.RAW_PATH.exists():
            sys.exit("REFUSED: the v0.40 collection has started; the pre-lock check runs before the lock only")
        A.other_collection_guard()
        A.require_keys()
    specs = build_plan() if specs is None else specs
    raw = Path(raw)
    ledger = BG.Ledger(raw, state, cap=ceiling, pause_at=ceiling)
    write = A.make_writer(raw, log)
    runners = runners or {"batch": partial(A.run_anthropic_batch, journal=journal), "standard": A.run_sync}
    done = A.done_ids(raw)
    status = "done"
    for cond in ("S0", "S1"):
        todo = [s for s in specs if s["condition"] == cond and s["call_id"] not in done]
        groups = [[s for s in todo if s["model"]["slot"] == m["slot"]] for m in A.PANEL]
        groups = [(g, runners[g[0]["model"]["mode"]]) for g in groups if g]
        if not groups:
            continue
        with ThreadPoolExecutor(max_workers=len(groups)) as pool:
            res = list(pool.map(lambda gr: gr[1](gr[0], ledger, write), groups))
        if "stop" in res or "pause" in res:
            status = "stop"
            break
    log(f"pre-lock check sending: {status}; {ledger.summary()}")
    return status


def v39_named_fn():
    sys.path.insert(0, str(V39_SCRIPTS))
    import score_v0_39 as S39
    coder = S39.Coder(json.loads(V39_REGISTRY.read_text(encoding="utf-8")))
    return lambda text: len(coder.brand_matches(text))


def evaluate(raw=RAW, specs=None, named_fn=None, out=RESULT, write=True):
    specs = build_plan() if specs is None else specs
    named_fn = named_fn or v39_named_fn()
    planned = {s["call_id"]: s for s in specs}
    table = defaultdict(Counter)
    for s in specs:
        table[f"{s['model']['slot']}|{s['condition']}"]["planned"] += 1
    rows = []
    if Path(raw).exists():
        rows = [json.loads(l) for l in Path(raw).read_text(encoding="utf-8").splitlines() if l.strip()]
    answered, blockers, flagged = set(), [], []
    for r in rows:
        if r.get("call_id") not in planned:
            continue
        a = SR.assess(r, named_fn)
        if a is None:
            continue
        answered.add(r["call_id"])
        t = table[f"{r['slot']}|{r['condition']}"]
        t["answers"] += 1
        for k in SR.FLAGS:
            t[k] += int(bool(a[k]))
        t["max_thinking"] = max(t["max_thinking"], a["thinking"])
        brief = {k: a[k] for k in ("call_id", "finish_reason", "output_tokens", "thinking", "thinking_upper_bound",
                                   "named", "cut_before_brand", "cut_after_brand", "think_half", "unassessable")}
        if (a["cut_before_brand"] or a["unassessable"]) and r["slot"] not in SR.EXEMPT:
            blockers.append(brief)
        elif a["at_limit"] or a["think_half"] or a["unassessable"]:
            flagged.append(dict(brief, exempt=r["slot"] in SR.EXEMPT))
    missing = sorted(set(planned) - answered)
    verdict = "BLOCKED" if blockers else ("INCOMPLETE" if missing else "PASS")
    res = {"phase": "v0.40", "check": "pre-lock length check (PRE_REGISTRATION_v0_40.md section 4.8)",
           "questions": f"v0.39 {V39_PROBES.name}, tiers {list(S0_TIERS)} (search on: {list(S1_TIERS)})",
           "verdict": verdict, "blockers": blockers, "flagged_not_blocking": flagged, "missing_calls": missing,
           "exempt_slots": sorted(SR.EXEMPT), "limits": SR.LIMIT,
           "by_setting": {k: dict(v) for k, v in sorted(table.items())},
           "spend_usd": round(BG.spend_of(raw), 4), "evaluated_utc": SR._now()}
    if write:
        Path(out).write_text(json.dumps(res, indent=2), encoding="utf-8")
    return res


def main():
    ap = argparse.ArgumentParser(description="AIAS v0.40 pre-lock length check (pre-registration section 4.8)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true", help="print planned calls and cost; no network")
    g.add_argument("--run", action="store_true", help="PAID: send the plan (resumable), then evaluate")
    g.add_argument("--evaluate", action="store_true", help="assess the recorded answers; no network")
    a = ap.parse_args()
    if a.dry_run:
        dry_run()
        return 0
    if a.run:
        run()
    res = evaluate()
    print(f"verdict: {res['verdict']}; blockers {len(res['blockers'])}; missing {len(res['missing_calls'])}; "
          f"flagged (not blocking) {len(res['flagged_not_blocking'])}; spend ${res['spend_usd']:.4f}")
    return {"PASS": 0, "BLOCKED": 3, "INCOMPLETE": 4}[res["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
