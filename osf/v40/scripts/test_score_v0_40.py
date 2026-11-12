#!/usr/bin/env python3
"""Tests for score_v0_40.py on SYNTHETIC data (never study data). Run: python3 test_score_v0_40.py
Two synthetic worlds are built from the frozen registry and probe set: A, where every pre-registered effect is
present by construction, and B, where none is. Plus unit tests of the coder and the exact tests."""
import json
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_v0_40 as S  # noqa: E402

FAILS = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if not cond and detail != "" else ""))
    if not cond:
        FAILS.append(name)


units, subjects, gaps = S.load_registry()
probes = json.loads((S.V40 / "prereg" / "probes_v0_40.json").read_text(encoding="utf-8"))["probes"]
M = S.build_matchers(units, subjects)
succ = {s["id"]: S.successor_names(s["successor"]) for s in subjects}

# ---- coder unit tests
m = S.code_answer("US Airways merged with American Airlines in 2015.", M, succ)
us = [x for x in m if x["entity"] == "US"]
check("ghost mention found and gone-flagged", us and us[0]["gone_flag"])
check("successor name near the ghost is coded", us and us[0]["successor_near"])
check("current unit found", any(x["entity"] == "AA" for x in m))
m = S.code_answer("I like Spirit for cheap fares.", M, succ)
check("bare collision alias coded ambiguous", m and m[0]["ambiguous"] and m[0]["entity"] == "NK")
m = S.code_answer("Bank of America is large.", M, succ)
check("longest alias wins, no overlapping shorter match", len(m) == 1 and m[0]["alias"] == "Bank of America", m)
m = S.code_answer("Wachovia is a bank. " + "x" * 200 + " It was acquired by Wells Fargo.", M, succ)
check("gone-flag needs the +-150 character window", m and not [x for x in m if x["entity"] == "WACHOVIA"][0]["gone_flag"])
check("Fable 5.2 uses the Opus 5.5 cutoff rows", S.GAP_MODEL["C1"] == "Claude Opus 5.5")
check("exact binomial sf", abs(S.binom_sf(3, 3, 0.5) - 0.125) < 1e-12 and S.binom_sf(0, 5, 0.3) == 1.0)
check("Fisher exact one-sided", abs(S.fisher_greater(3, 0, 0, 3) - 0.05) < 1e-12)
check("Spearman", abs(S.spearman([1, 2, 3, 4], [10, 20, 30, 40]) - 1) < 1e-12)

# ---- synthetic worlds
SLOTS = S.TESTED_SLOTS


def name(sid):
    for s in subjects:
        if s["id"] == sid:
            return s["aliases"][0]
    return {"JPMC": "Chase", "BAC": "Bank of America", "AA": "American Airlines", "DL": "Delta Air Lines"}[sid]


def world(effects, seed=1):
    rng = random.Random(seed)
    recs = []
    mx = {c: max(u["share"] for u in units if u["category"] == c) for c in ("airline", "bank")}
    for sl in SLOTS:
        arm = "C" if sl.startswith("C") else "L"
        for cond, runs in ((("S0", 3), ("S1", 1)) if arm == "C" else (("S0", 3),)):
            for run in range(1, runs + 1):
                for p in probes:
                    if cond == "S1" and not (p["kind"] == "recommendation" or p["tier"] == "S"):
                        continue
                    cat, sid = p["category"], p.get("subject_id")
                    if p["kind"] == "recommendation":
                        names = []
                        for u in units:
                            if u["category"] != cat:
                                continue
                            pr = (u["share"] / mx[cat]) ** 2 if effects else 0.3
                            if rng.random() < pr:
                                names.append(u["aliases"][0])
                        for g in [s for s in subjects if s["role"] == "ghost" and s["category"] == cat]:
                            gp = gaps.get((g["id"], S.GAP_MODEL[sl]))
                            if effects and gp is not None and gp > 0 and rng.random() < max(0.0, 0.7 - gp / 250):
                                names.append(g["aliases"][0])
                        text = "Good options: " + ". ".join(f"{n} is a solid choice" for n in names) + "."
                    elif p["tier"] == "K":
                        text = f"{name(sid)} is a US company."
                    else:
                        role = p["subject_role"]
                        gp = gaps.get((sid, S.GAP_MODEL[sl]))
                        if role == "ghost" and effects:
                            if cond == "S1":
                                gone = True
                            elif gp is not None and gp < 0:
                                gone = False
                            else:
                                gone = not (arm == "C" and sum(map(ord, sid)) % 3 == 0)
                        else:
                            gone = False
                        text = (f"{name(sid)} no longer exists." if gone else f"Yes, {name(sid)} is open today.")
                    recs.append({"call_id": f"{sl}|{p['probe_id']}|{cond}|{run}", "arm": arm, "slot": sl, "condition": cond,
                                 "run": run, "probe_id": p["probe_id"], "tier": p["tier"], "kind": p["kind"],
                                 "category": cat, "brand_id": sid, "text": text, "status": "ok", "finish_reason": "stop",
                                 "search": {"n_searches": 1} if cond == "S1" else None})
    return recs


A = S.Scorer(world(True), units, subjects, gaps, perms=300).run()
B = S.Scorer(world(False), units, subjects, gaps, perms=300).run()
for h in ("H_Reinforce", "H_Amplify", "H_Afterlife", "H_Decay", "H_Flag", "H_Search"):
    print(f"  world A {h:12s} {A[h]['verdict']:13s} world B {B[h]['verdict']}")
check("A: H_Reinforce CONFIRMED", A["H_Reinforce"]["verdict"] == "CONFIRMED", A["H_Reinforce"])
check("A: H_Amplify CONFIRMED", A["H_Amplify"]["verdict"] == "CONFIRMED", {c: A["H_Amplify"][c]["ratio"] for c in ("airline", "bank")})
check("A: H_Afterlife CONFIRMED", A["H_Afterlife"]["verdict"] == "CONFIRMED", A["H_Afterlife"])
check("A: H_Decay CONFIRMED", A["H_Decay"]["verdict"] == "CONFIRMED", A["H_Decay"])
check("A: H_Flag CONFIRMED", A["H_Flag"]["verdict"] == "CONFIRMED", A["H_Flag"])
check("A: H_Search CONFIRMED", A["H_Search"]["verdict"] == "CONFIRMED", A["H_Search"])
check("B: H_Afterlife FALSIFIED", B["H_Afterlife"]["verdict"] == "FALSIFIED", B["H_Afterlife"])
check("B: H_Decay UNDETERMINED (floor)", B["H_Decay"]["verdict"] == "UNDETERMINED", B["H_Decay"])
check("B: H_Flag FALSIFIED", B["H_Flag"]["verdict"] == "FALSIFIED", B["H_Flag"])
check("B: H_Search not CONFIRMED", B["H_Search"]["verdict"] != "CONFIRMED", B["H_Search"])
check("B: H_Reinforce not CONFIRMED", B["H_Reinforce"]["verdict"] != "CONFIRMED", B["H_Reinforce"])
check("manipulation checks pass in A", all(v["pass"] for k, v in A["manipulation_checks"].items() if not k.startswith("MC1")),
      {k: v["pass"] for k, v in A["manipulation_checks"].items()})
print(f"\n{'ALL PASS' if not FAILS else 'FAILED: ' + ', '.join(FAILS)}")
sys.exit(1 if FAILS else 0)
