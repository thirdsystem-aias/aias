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
check("Discover switch (a)/draft: no extra control", S.switch_controls(subjects) == [])
import tempfile  # noqa: E402
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
    json.dump({"subjects": [{"subject_id": "MERRILL", "category": "bank", "role": "control", "registry_brand": "Merrill",
                             "name_in_probe": "Merrill"}]}, f)
xc = S.switch_controls(subjects, f.name)
check("Discover switch (b): replacement control is added and matched",
      len(xc) == 1 and S.code_answer("Yes, Merrill is open.", S.build_matchers(units, subjects + xc), {})[0]["entity"] == "MERRILL")

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

# ---- declared sensitivities (section 5.6) and descriptives 3-9 (section 2.9), on synthetic data
sA = A["sensitivity"]
check("sensitivities reported: S-D4, S-Discover, S-Ambig, S-Legal, S-Operating, S-SunCountry, S-Arm",
      set(sA) == {"S-D4", "S-Discover", "S-Ambig", "S-Legal", "S-Operating", "S-SunCountry", "S-Arm"}, sorted(sA))
check("S-Ambig runs all six tests", set(sA["S-Ambig"]) == {"H_Reinforce", "H_Amplify", "H_Afterlife", "H_Decay", "H_Flag", "H_Search"})
check("S-Arm: legacy five tests, current six", len(sA["S-Arm"]["legacy"]) == 5 and len(sA["S-Arm"]["current"]) == 6)
check("S-Operating: Delta leads the airlines", sA["S-Operating"]["H_Amplify_airline"]["leader"] == "DL")
check("S-SunCountry: Sun Country inside Allegiant (10 airline units)",
      sA["S-SunCountry"]["H_Reinforce_airline"]["n_units"] == sum(u["category"] == "airline" for u in units) - 1)
su = S.sun_country_inside_allegiant(units)
check("S-SunCountry: Allegiant at the registry's alternative share 2.6673", abs([u for u in su if u["id"] == "G4"][0]["share"] - 2.6673) < 1e-9)
lg = S.load_gaps(column="gap_legal_m")
check("S-Legal reads gap_legal_m (differs from gap_brand_m somewhere)", any(lg.get(k) != v for k, v in gaps.items()))

# S-Ambig counts an ambiguous mention; the primary does not (one-record world)
rec = [{"call_id": "x1", "arm": "C", "slot": "C1", "condition": "S0", "run": 1, "probe_id": "R", "tier": "R",
        "kind": "recommendation", "category": "airline", "brand_id": None, "status": "ok", "finish_reason": "stop",
        "text": "Fly Delta this year."}]
sc = S.Scorer(rec, units, subjects, gaps, perms=10)
pri = sc.unit_counts(sc.recs("recommendation"), "airline")
amb = sc.variant(amb=True).unit_counts(sc.recs("recommendation"), "airline")
check("S-Ambig: bare 'Delta' (ambiguous) counted for DL only in the sensitivity",
      pri["DL"] == 0 and amb["DL"] == 1 and sc.amb is False, (pri["DL"], amb["DL"]))

# first-mention share: the first current unit named wins
rec = [{"call_id": f"f{i}", "arm": "C", "slot": "C2", "condition": "S0", "run": 1, "probe_id": "R", "tier": "R",
        "kind": "recommendation", "category": "airline", "brand_id": None, "status": "ok", "finish_reason": "stop",
        "text": t} for i, t in enumerate(["Delta Air Lines, then American Airlines.", "American Airlines first; Delta Air Lines.",
                                          "Delta Air Lines only."])]
fm = S.Scorer(rec, units, subjects, gaps, perms=10).d9_first_mention()["C2|S0|airline"]
check("first-mention share (DL 2/3, AA 1/3)", fm["answers"] == 3 and abs(fm["share"]["DL"] - 2 / 3) < 1e-12
      and abs(fm["share"]["AA"] - 1 / 3) < 1e-12, fm)

# descriptive 4: recognition coding
def krec(i, sid, text):
    return {"call_id": f"k{i}", "arm": "L", "slot": "M1", "condition": "S0", "run": 1, "probe_id": "K", "tier": "K",
            "kind": "recognition", "category": "bank", "brand_id": sid, "status": "ok", "finish_reason": "stop", "text": text}
wid = [s for s in subjects if s["id"] == "WACHOVIA"]
if wid:
    nm = wid[0]["aliases"][0]
    d4 = S.Scorer([krec(1, "WACHOVIA", f"{nm} was acquired by Wells Fargo in 2008."),
                   krec(2, "WACHOVIA", f"{nm} is a large bank with many branches."),
                   krec(3, "WACHOVIA", "I'm not familiar with that bank.")], units, subjects, gaps, perms=10).d4_recognition()
    c = d4.get("WACHOVIA|M1|S0", {})
    check("descriptive 4: flagged / current / not recognised", c.get("flagged") == 1 and c.get("current") == 1
          and c.get("not_recognised") == 1, c)
else:
    check("descriptive 4: Wachovia ghost present in registry", False)

# descriptive 8: near-floor holders coded "other", not as registry units
rec = [{"call_id": "o1", "arm": "L", "slot": "M3", "condition": "S0", "run": 1, "probe_id": "R", "tier": "R",
        "kind": "recommendation", "category": "bank", "brand_id": None, "status": "ok", "finish_reason": "stop",
        "text": "Consider USAA or Synchrony Bank."}]
sc = S.Scorer(rec, units, subjects, gaps, perms=10)
d8 = sc.d8_other()["L_S0"]
check("descriptive 8: USAA and Synchrony counted as other", d8["USAA"] == 1 and d8["Synchrony"] == 1 and d8["Zions"] == 0, d8)
check("descriptive 8: near-floor names are not registry units", sum(sc.unit_counts(sc.recs("recommendation"), "bank").values()) == 0)

dA = A["descriptives"]
check("descriptives 3-9 reported", all(k in dA for k in ("3_old_vs_new_name", "4_recognition", "5_M5X_vs_M5", "6_run_to_run_se",
                                                       "7_search_traces", "8_near_floor_other", "9_first_mention_share")))
check("descriptive 3: per arm and condition", set(dA["3_old_vs_new_name"]) == {"L_S0", "C_S0", "C_S1"})
check("descriptive 6: run-to-run SE per arm", set(dA["6_run_to_run_se"]) == {"L", "C"} and dA["6_run_to_run_se"]["C"]["units"] > 0)
check("descriptive 7: one trace per S1 answer", len(dA["7_search_traces"]["answers"]) == sum(
    1 for p in probes if p["kind"] == "recommendation" or p["tier"] == "S") * 3)

print(f"\n{'ALL PASS' if not FAILS else 'FAILED: ' + ', '.join(FAILS)}")
sys.exit(1 if FAILS else 0)
