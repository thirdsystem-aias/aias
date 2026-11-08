#!/usr/bin/env python3
"""
Synthetic-fixture tests for score_v0_39.py (no study data). Locked with the pre-registration.
Run: python3 scripts/test_score_v0_39.py
"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_v0_39 as S

SPEC = json.loads(S.REGISTRY_PATH.read_text(encoding="utf-8"))
PROBES = json.loads(S.PROBES_PATH.read_text(encoding="utf-8"))
C = S.Coder(SPEC)
FAILS = []


def check(name, got, want):
    if got != want:
        FAILS.append(f"{name}: got {got!r}, want {want!r}")


def has(t, bid):
    return bid in C.brand_matches(t)


def gen(t):
    return C.generation(t, C.brand_matches(t))[0]


# ---- mention detection and collision rules (section 3.3) ----
check("bellwether brand", has("The Bellwether Shop Roaster is electric.", "B01"), True)
check("bellwether common noun lowercase", has("Probat is the industry bellwether.", "B01"), False)
check("stronghold brand", has("The Stronghold S7X is popular.", "B06"), True)
check("stronghold common noun", has("Seattle is a stronghold of specialty coffee.", "B06"), False)
check("air-motion", has("Air-Motion Roasters build fluid-bed machines.", "B03"), True)
check("amr model", has("The AMR12 roasts 12 kg.", "B03"), True)
check("air motion generic", has("The air motion keeps beans moving.", "B03"), False)
check("probatino", has("A Probatino is a classic shop roaster.", "B09"), True)
check("north model", has("The North TJ-067 is a popular import.", "B21"), True)
check("north generic", has("Roasters across North America use drums.", "B21"), False)
check("royal roaster", has("A vintage Royal No. 5 still roasts well.", "B33"), True)
check("royal coffee importer", has("Buy green beans from Royal Coffee.", "B33"), False)
check("vittoria coffee brand", has("Vittoria Coffee is an Australian brand.", "B31"), False)
check("vittoria roaster", has("A Vittoria roaster came up for sale.", "B31"), True)
check("primo model", has("The Primo Ranger XR5 has an internal cyclone.", "B28"), True)
check("primo generic", has("Primo location for a café.", "B28"), False)
check("has garanti", has("Has Garanti roasters are Turkish-made.", "B18"), True)
check("garanti bank", has("Pay with Garanti BBVA.", "B18"), False)
check("us roaster corp", has("U.S. Roaster Corp builds drums in Oklahoma.", "B11"), True)
check("java master", has("Java Master in-store roasters suit grocers.", "B36"), True)
check("roest lowercase", has("de roest op het ijzer", "B13"), False)
check("san francisco city", has("Roasters in San Francisco love drums.", "B08"), False)
check("san franciscan", has("The San Franciscan SF-6 is a workhorse.", "B08"), True)

# ---- generation coding (section 3.4) ----
check("shop only", gen("Bellwether's newest model is the Shop Roaster, a countertop machine."), "Shop-only")
check("preshop only", gen("Bellwether sells the Series 2, a 6 lb ventless roaster."), "PreShop-only")
check("generic shop roaster", gen("Consider a Bellwether roaster; it is a popular shop roaster."), "Unspecified")
check("both", gen("Bellwether Series 2 or the newer Shop Roaster"), "Both")
check("other brand between", gen("Bellwether is ventless. The Probat Series 2 is gas."), "Unspecified")
check("absent", gen("Diedrich and Mill City are common choices."), "Absent")
check("far token", gen("Bellwether" + " x" * 40 + " Series 2"), "Unspecified")

# ---- frame lexicons (section 5.5) ----
check("vent required", C.frame("You will need proper ventilation and an exhaust duct."), (1, 0))
check("ventless option", C.frame("A ventless electric roaster avoids ducting entirely."), (1, 1))
check("doesn't require", C.frame("It doesn't require any ventilation."), (1, 1))
check("no false vent", C.frame("Eventually, track inventory to prevent waste."), (0, 0))
check("smokeless", C.frame("Smokeless roasting is possible."), (0, 1))

# ---- McNemar and Wilson ----
check("mcnemar 5-0", round(S.mcnemar_one_sided(5, 0), 5), 0.03125)
check("mcnemar 3-1", round(S.mcnemar_one_sided(3, 1), 4), 0.3125)
check("mcnemar none", S.mcnemar_one_sided(0, 0), 1.0)
lo, hi = S.wilson(5, 10)
check("wilson", (round(lo, 3), round(hi, 3)), (0.237, 0.763))
check("domain www", S.source_domain({"url": "https://www.bellwethercoffee.com/faq"}), "bellwethercoffee.com")
check("domain gemini redirect", S.source_domain({"url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AbC",
                                                 "title": "bellwethercoffee.com"}), "bellwethercoffee.com")
check("k5 shop", S.k5_class(1.5), "Shop Roaster")
check("k5 series2", S.k5_class(2.72), "Series 2")


# ---- end-to-end on synthetic records (never written to osf/v39/data) ----
def text_for(p, slot, cond):
    t, pid = p["tier"], p["probe_id"]
    if t == "F":
        return "You will need ventilation, an exhaust hood and a gas line for a drum roaster."
    if t == "G":
        if cond == "S1":
            return "Try the Bellwether Shop Roaster or a Diedrich IR-2.5."
        return "Try a Diedrich IR-2.5 or a Mill City 1 kg."
    if t == "C":
        if slot in S.PRE_BOUNDARY:  # pre-boundary models cannot name the Shop Roaster
            return "Without ventilation, a Bellwether roaster is the usual answer; a Stronghold S7X is electric too."
        return "Without ventilation, the Bellwether Shop Roaster is the usual answer; a Stronghold S7X is electric too."
    if t == "R":
        return "Look at Loring, Probat and Giesen for production."
    # K probes
    if slot in S.PRE_BOUNDARY:
        return "Bellwether Coffee sells the Series 2, a 6 lb ventless roaster."
    if pid == "K3":
        return "No. The Bellwether roaster doesn't require ventilation or ducting."
    if pid == "K5":
        return "The Bellwether Shop Roaster roasts 1.5 kg per batch on a 240V 30A circuit."
    return "Bellwether's newest model is the Shop Roaster; it replaced the Series 2."


raw = []
for p in PROBES["probes"]:
    for arm, slots, conds in (("L", S.LEGACY_SLOTS, ("S0",)), ("C", S.CURRENT_SLOTS, ("S0", "S1"))):
        for cond in conds:
            for m in slots:
                raw.append({"probe_id": p["probe_id"], "tier": p["tier"], "kind": p["kind"], "arm": arm, "condition": cond,
                            "model_slot": m, "model_name": m, "boundary": "pre" if m in S.PRE_BOUNDARY else "post",
                            "status": "ok", "response": text_for(p, m, cond), "served_model": m, "finish_reason": "stop",
                            "search": ({"n_searches": 1, "queries": ["q"], "sources": [{"url": "https://bellwethercoffee.com/x"}],
                                        "citations": ([{"url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/x",
                                                        "title": "bellwethercoffee.com"}] if m == "C3"
                                                      else [{"url": "https://www.bellwethercoffee.com/x"}]), "errors": []}
                                       if cond == "S1" else None)})
check("synthetic cell count", len(raw), 360)

# provisional without an audit file
coded, mentions, tables, verdicts = S.score(raw, SPEC, PROBES, audit_path=None)
check("provisional without audit", verdicts["status"], "PROVISIONAL")

# complete audit with one common-noun removal
keys = sorted({S.key_of(r) for r in raw if any(b in C.brand_matches(r["response"]) for b in S.AUDITED)})
with tempfile.TemporaryDirectory() as td:
    ap = Path(td) / "audit.json"
    ap.write_text(json.dumps({"audited_keys": keys, "removals": []}), encoding="utf-8")
    coded, mentions, tables, verdicts = S.score(raw, SPEC, PROBES, audit_path=str(ap))
check("final with audit", verdicts["status"], "FINAL")
check("e2e H_CEP", verdicts["H_CEP"]["verdict"], "CONFIRMED")
check("e2e H_CEP delta", verdicts["H_CEP"]["delta"], 1.0)
check("e2e H_CEPDefault", verdicts["H_CEPDefault"]["verdict"], "PARTIAL")      # Bellwether ties Stronghold in C
check("e2e H_Frame", verdicts["H_Frame"]["verdict"], "CONFIRMED")
check("e2e H_Search", verdicts["H_Search"]["verdict"], "CONFIRMED")            # 18 G pairs flip S0->S1; C pairs concordant
check("e2e H_Search pairs", verdicts["H_Search"]["n_pairs"], 36)
check("e2e H_Search delta", verdicts["H_Search"]["delta"], 0.5)
check("e2e MC_Constraint", verdicts["MC_Constraint"]["pass"], True)
check("e2e MC_Boundary", verdicts["MC_Boundary"]["pass"], True)
check("e2e shop aware M1", tables["shop_aware"].get("M1|S0"), True)
check("e2e shop aware M3", tables["shop_aware"].get("M3|S0"), False)
check("e2e retrieval share", tables["descriptives"]["D7_retrieval"]["share_citing_bellwethercoffee"], 1.0)
d10 = tables["descriptives"]["D10_five_model_sensitivity"]
check("e2e D10 models", d10["models"], ["M1", "M2", "M3", "M4", "M6"])
check("e2e D10 cep delta", d10["H_CEP"]["delta"], 1.0)
check("e2e D10 frame n", d10["H_Frame"]["n"], 30)
check("e2e D10 m5 capped", d10["m5_capped_share"], 0.0)

# audit removal of a common-noun use flips presence for that cell only
raw2 = [dict(r) for r in raw]
raw2[0] = dict(raw2[0], response="Bellwether brands in roasting? Ask a roaster.")  # F1|M1|S0, a common-noun use
k0 = S.key_of(raw2[0])
keys2 = sorted({S.key_of(r) for r in raw2 if any(b in C.brand_matches(r["response"]) for b in S.AUDITED)})
with tempfile.TemporaryDirectory() as td:
    ap = Path(td) / "audit.json"
    ap.write_text(json.dumps({"audited_keys": keys2, "removals": [{"key": k0, "brand_id": "B01", "start": 0}]}), encoding="utf-8")
    coded2, _, _, _ = S.score(raw2, SPEC, PROBES, audit_path=str(ap))
check("audit removal", [c["bellwether"] for c in coded2 if c["key"] == k0], [0])

# missing cells are excluded from denominators and never crash the scorer
raw3 = [dict(r) for r in raw]
for i in (0, 1):
    raw3[i] = dict(raw3[i], status="error" if i == 0 else "empty", response="")
with tempfile.TemporaryDirectory() as td:
    ap = Path(td) / "audit.json"
    ap.write_text(json.dumps({"audited_keys": keys, "removals": []}), encoding="utf-8")
    _, _, tables3, verdicts3 = S.score(raw3, SPEC, PROBES, audit_path=str(ap))
check("missing cells excluded", tables3["n_ok"], 358)
check("frame n after missing", verdicts3["H_Frame"]["n"], 34)

if FAILS:
    print("FAILED:\n  " + "\n  ".join(FAILS))
    sys.exit(1)
print(f"all checks passed ({len(raw)} synthetic records; no study data used)")
