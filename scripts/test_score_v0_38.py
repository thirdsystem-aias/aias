#!/usr/bin/env python3
"""
Synthetic-fixture tests for score_v0_38.py (no study data). Locked with the pre-registration.
Run: python3 scripts/test_score_v0_38.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_v0_38 as S

SPEC = json.loads(S.REGISTRY_PATH.read_text(encoding="utf-8"))
PROBES = json.loads(S.PROBES_PATH.read_text(encoding="utf-8"))
C = S.Coder(SPEC)
FAILS = []


def check(name, got, want):
    if got != want:
        FAILS.append(f"{name}: got {got!r}, want {want!r}")


def gen(t):
    return C.generation(t, C.brand_matches(t))[0]


def has(t, bid):
    return bid in C.brand_matches(t)


# mention detection and exclusions
check("aillio plain", has("Look at the Aillio Bullet.", "R01"), True)
check("aillio misspelt", has("The Ailio Bullet is great.", "R01"), True)
check("kaldi legend excluded", has("Legend says Kaldi the goat herder found coffee.", "R15"), False)
check("kaldi roaster kept", has("The Kaldi Wide is a gas drum roaster.", "R15"), True)
check("generic fresh roast", has("Nothing beats a fresh roast in the morning.", "R05"), False)
check("fresh roast brand", has("The Fresh Roast SR800 is a popular air roaster.", "R05"), True)
check("sr540 alone", has("Start with an SR540.", "R05"), True)
check("popcorn popper excluded", has("A Popcorn Popper works in a pinch.", "R20"), False)
check("roest lowercase", has("de roest op het ijzer", "R08"), False)
check("hottop", has("The Hottop KN-8828B-2K+ is solid.", "R02"), True)
check("iroast", has("The i-Roast 2 was popular.", "R29"), True)
check("quest generic", has("On a quest for better coffee.", "R13"), False)

# generation attribution
check("R1 V2", gen("I recommend the Aillio Bullet R1 V2 for serious roasting."), "R1-only")
check("both", gen("Consider the Aillio Bullet R2, which replaced the R1."), "Both")
check("R2 Pro", gen("Get the Aillio Bullet R2 Pro if you have 220V."), "R2-only")
check("unspecified", gen("The Aillio Bullet is the enthusiast favourite."), "Unspecified")
check("absent", gen("Try a Behmor 2000AB."), "Absent")
check("sandbox R2 before anchor", gen("The Sandbox Smart R2 is compact. The Aillio Bullet is great too."), "Unspecified")
check("sandbox R2 between", gen("Options: Aillio Bullet, Sandbox Smart R2, Hottop."), "Unspecified")
check("far token", gen("Aillio Bullet" + " x" * 40 + " R1"), "Unspecified")

# first-mention order
order = C.first_mention_order(C.brand_matches("Behmor first, then the Aillio Bullet, then a Hottop."))
check("order", order, ["R04", "R01", "R02"])

# K4 coding
check("k4 superseded", S.k4_code("No. The R1 has been discontinued and replaced by the R2."), "Superseded")
check("k4 current", S.k4_code("Yes, the Aillio Bullet R1 is still in production."), "Current")
check("k4 unclear", S.k4_code("I am not certain about Aillio's current lineup."), "Unclear")

# Wilson interval
lo, hi = S.wilson(5, 10)
check("wilson", (round(lo, 3), round(hi, 3)), (0.237, 0.763))

# end-to-end on synthetic records (never written to osf/v38/data)
raw = []
for p in PROBES["probes"]:
    for i, m in enumerate(S.SLOTS):
        if p["kind"] == "recommendation":
            if p["tier"] == "B":
                txt = "Try the Fresh Roast SR800 or a Behmor."
            else:
                txt = "The Aillio Bullet R1 V2 is the standard; also the Hottop." if (m in S.PRE_BOUNDARY or i % 2 == 0) else "Consider the Aillio Bullet R2 or a Kaffelogic Nano 7."
        else:
            txt = "The newest is the Aillio Bullet R2 and R2 Pro." if m not in S.PRE_BOUNDARY else "The Aillio Bullet R1 V2 is the latest."
        raw.append({"probe_id": p["probe_id"], "tier": p["tier"], "kind": p["kind"], "model_slot": m,
                    "model_name": m, "boundary": "pre" if m in S.PRE_BOUNDARY else "post", "status": "ok",
                    "response": txt, "served_model": m, "finish_reason": "stop"})
coded, mentions, tables, verdicts = S.score(raw, SPEC, PROBES)
check("e2e tier verdict", verdicts["H_Tier"]["verdict"], "CONFIRMED")
check("e2e mc", verdicts["MC_Boundary"]["pass"], True)
check("e2e aware", [m for m, a in tables["r2_aware"].items() if a], ["M1", "M2", "M5", "M6"])
check("e2e legacy n", verdicts["H_LegacySlot"]["n"], 48)

if FAILS:
    print("FAILED:\n  " + "\n  ".join(FAILS))
    sys.exit(1)
print(f"all checks passed ({len(raw)} synthetic records; no study data used)")
