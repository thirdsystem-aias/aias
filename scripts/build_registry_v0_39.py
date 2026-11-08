"""Build the v0.39 registry and probe battery as a fork of the v0.38 registry.

Writes:
  <out>/registries/brands_commercial_roasters_v0.39.json
  <out>/prereg/probes_v0_39.json
Locked at tag v0.39-prereg-r1 (checksums in osf/v39/prereg/LOCK_MANIFEST_v0_39.sha256).
Usage: python3 scripts/build_registry_v0_39.py osf/v38/registries/brands_home_roasters_v0.38.json osf/v39
"""
import hashlib
import json
import re
import sys
from pathlib import Path

V38_REG = Path(sys.argv[1])          # v0.38 registry (source of carried-forward aliases)
OUT = Path(sys.argv[2])              # output root

v38 = {b["brand"]: b for b in json.loads(V38_REG.read_text(encoding="utf-8"))["brands"]}


def carry(name):
    """Aliases/exclusions carried verbatim from the v0.38 registry."""
    b = v38[name]
    return b["aliases"], b["exclusions"]


def A(pattern, flags=""):
    return {"pattern": pattern, "flags": flags}


brands = []


def add(bid, brand, stratum, segment, status, aliases, exclusions=None, note=None, carried=False):
    e = {"id": bid, "brand": brand, "stratum": stratum, "segment": segment, "status": status,
         "aliases": aliases, "exclusions": exclusions or []}
    if carried:
        e["carried_from"] = "v0.38"
    if note:
        e["note"] = note
    brands.append(e)


# ---- S: Coffee Fest Dallas-Fort Worth 2026 show floor -------------------------------------
add("B01", "Bellwether", "S", "shop", "active (focal)", [A(r"\bBellwether\b")],
    note="Case-sensitive; every match audited for common-noun use (§3.3). Booth DE 210.")
al, ex = carry("Aillio")
add("B02", "Aillio", "S", "micro", "active", al, ex, note="Booth DE 225.", carried=True)
add("B03", "Air-Motion Roasters", "S", "production", "active",
    [A(r"\bAir[- ]Motion\b"), A(r"\bAMR\s?-?(?:3|6|12|20)\b")],
    note="Booth DE 332, exhibited by its exclusive North American distributor Coffee Equipment Pros.")
al, ex = carry("Loring")
add("B04", "Loring", "S", "production", "active", al, ex, carried=True)
al, ex = carry("Mill City Roasters")
add("B05", "Mill City Roasters", "S", "production", "active", al, ex, carried=True)
add("B06", "Stronghold", "S", "shop", "active", [A(r"\bStronghold\b")],
    note="Case-sensitive; every match audited for common-noun use (§3.3). On the floor via RoasTronix, its US distributor.",
    carried=True)

# ---- A: v0.38 prosumer + commercial-spillover carry-forward, plus unregistered brands seen in v0.38 answers
al, ex = carry("Diedrich")
add("B07", "Diedrich", "A", "production", "active", al, ex, carried=True)
al, ex = carry("San Franciscan")
add("B08", "San Franciscan", "A", "production", "active", al, ex, carried=True)
add("B09", "Probat", "A", "production", "active", [A(r"\bProbat(?:ino|one)?\b", "i")],
    note="v0.38 alias widened to catch Probatino/Probatone (new phase; not a v0.38 amendment).", carried=True)
al, ex = carry("Giesen")
add("B10", "Giesen", "A", "production", "active", al, ex, carried=True)
al, ex = carry("US Roaster Corp")
add("B11", "US Roaster Corp", "A", "production", "active", al + [A(r"\bU\.S\.\s+Roaster\s+Corp", "i")], ex, carried=True)
al, ex = carry("Ikawa")
add("B12", "Ikawa", "A", "sample", "active", al, ex, carried=True)
add("B13", "Roest", "A", "sample", "active", [A(r"\bRoest\b"), A(r"\bROEST\b")], carried=True)
al, ex = carry("Coffee-Tech Engineering")
add("B14", "Coffee-Tech Engineering", "A", "shop", "active", al, ex,
    note="Also a claim holder: markets smokeless roasting technology (D4).", carried=True)
al, ex = carry("Kaleido")
add("B15", "Kaleido", "A", "micro", "active", al, ex, carried=True)
al, ex = carry("Santoker")
add("B16", "Santoker", "A", "micro", "active", al, ex, carried=True)
add("B17", "Toper", "A", "production", "active", [A(r"\bToper\b")],
    note="Named in 2 v0.38 answers. Kept in stratum A at lock (pre-registrant, 2026-11-08).")
add("B18", "Has Garanti", "A", "production", "active",
    [A(r"\bHas\s?Garanti\b", "i"), A(r"\bGaranti\s+(?:coffee\s+)?roasters?\b", "i")],
    note="Named in 1 v0.38 answer. Bare 'Garanti' not matched (bank-name collision).")
add("B19", "BC Roasters", "A", "micro", "status to verify", [A(r"\bBC\s+Roasters?\b")],
    note="Named in 3 v0.38 answers (all M1).")
add("B20", "Buckeye", "A", "production", "status to verify", [A(r"\bBuckeye\s+(?:Coffee\s+)?Roast(?:ers?|ing)\b", "i")],
    note="Named in 1 v0.38 answer.")
add("B21", "North", "A", "micro", "status to verify",
    [A(r"\bNorth\s+(?:TJ-?\d+|(?:coffee\s+)?roasters?)\b")],
    note="Taiwanese maker (TJ-067 named in 1 v0.38 answer). Requires a model number or 'roaster' context.")

# ---- M: Coffee Equipment Pros 'Roasters by Manufacturer' brand collections (snapshot 2026-11-08)
add("B22", "Ambex", "M", "production", "active", [A(r"\bAmbex\b", "i")])
add("B23", "ARC", "M", "sample", "status to verify", [A(r"\bARC[- ]?(?:\d{3,4}|sample\s+roasters?)\b")],
    note="Requires a model number or 'sample roaster' context.")
add("B24", "Joper", "M", "production", "active", [A(r"\bJoper\b", "i")])
add("B25", "Lilla", "M", "production", "active", [A(r"\bLilla\b")])
add("B26", "Öztürkbay", "M", "production", "active", [A(r"\b(?:Ö|O)zt(?:ü|u)rkbay\b", "i")])
add("B27", "Petroncini", "M", "production", "active", [A(r"\bPetroncini\b", "i")])
add("B28", "Primo", "M", "production", "status to verify",
    [A(r"\bPrimo\s+(?:Ranger|XR-?\d*|(?:coffee\s+)?roasters?|Roasting)\b")],
    note="Requires a model or 'roaster' context.")
add("B29", "Proaster", "M", "production", "status to verify", [A(r"\bProaster\b", "i")])
add("B30", "Trabattoni", "M", "production", "status to verify", [A(r"\bTrabattoni\b", "i")])
add("B31", "Vittoria", "M", "production", "status to verify", [A(r"\bVittoria\s+(?:coffee\s+)?roasters?\b", "i")],
    note="Requires 'roaster' context (Vittoria Coffee, the Australian coffee brand, is not a match).")
add("B32", "Jabez Burns", "M", "legacy", "historic (vintage used machines)",
    [A(r"\bJabez\s+Burns\b", "i"), A(r"\bBurns\s+(?:Thermalo|(?:coffee\s+)?roasters?|No\.?\s?\d+)\b")])
add("B33", "Royal", "M", "legacy", "historic (vintage used machines)",
    [A(r"\bRoyal\s+(?:No\.?\s?\d+|(?:coffee\s+)?roasters?)\b")],
    note="Requires a model or 'roaster' context (Royal Coffee, the green-coffee importer, is not a match).")
add("B34", "Sivetz", "M", "legacy", "status to verify", [A(r"\bSivetz\b", "i")])

# ---- D: in-store / on-site retail roasting claim holders (pre-lock fact check)
add("B35", "Sonofresco", "D", "in-store retail", "active",
    [A(r"\bSonofresco\b", "i")],
    note="Owned by Coffee Holding (booth DE 420). Kept in stratum D at lock (pre-registrant, 2026-11-08).")
add("B36", "Java Master", "D", "in-store retail", "active", [A(r"\bJava\s?Master\b", "i")])

assert len(brands) == len({b["id"] for b in brands}) == 36
for b in brands:
    for a in b["aliases"]:
        re.compile(a["pattern"], re.I if a["flags"] == "i" else 0)
    for x in b["exclusions"]:
        re.compile(x["pattern"], re.I)

registry = {
    "phase": "v0.39",
    "status": "locked at tag v0.39-prereg-r1 (2026-11-08)",
    "substrate": "Commercial coffee roasters for cafés, retailers and specialty roasteries (US market): sample, shop and production machines",
    "focal_brand": "B01",
    "flags_legend": {"i": "case-insensitive", "": "case-sensitive"},
    "exclusion_semantics": "a match is discarded if an exclusion pattern (case-insensitive) occurs within `window` characters before or after it",
    "inclusion_rule": {
        "S": "Show floor: every roasting-machine maker, or its exclusive distributor, on the Coffee Fest Dallas-Fort Worth 2026 exhibitor list (139 exhibitors; snapshot 2026-11-08)",
        "A": "AI shelf: v0.38 registry brands in the prosumer and commercial-spillover segments, plus unregistered commercial roaster brands named in v0.38's 132 panel answers",
        "M": "Market: manufacturers with a brand collection page in the Coffee Equipment Pros 'Roasters by Manufacturer' index (the show-floor distributor's marketplace; snapshot 2026-11-08); one-off product listings excluded",
        "D": "Claim holders: makers whose own materials market in-store or on-site retail roasting, found in the pre-lock fact check",
        "precedence": "A brand's stratum is its first qualifying route in the order S, A, M, D",
    },
    "resolved_at_lock": [
        "Show-floor stratum kept as listed, six brands (pre-registrant, 2026-11-08): Toper stays in A, Sonofresco in D, Wiltronic Corporation not added",
        "Brands with 'status to verify' keep that label; segment and status labels enter no test",
    ],
    "audited_brands": ["B01", "B06"],
    "brands": brands,
    "bellwether_generation_coding": {
        "anchors": [A(r"\bBellwether\b")],
        "preshop_tokens": [A(r"\bSeries\s?(?:1|2|One|Two)\b", "i"),
                           A(r"\boriginal\s+Bellwether(?:\s+(?:Coffee\s+)?roaster)?\b", "i")],
        "shop_tokens": [A(r"\bShop\s+Roaster\b")],
        "model_2026_markers": [A(r"\bnew\s+Shop\s+Roaster\b", "i"), A(r"\bdeep\s+bronze\b", "i"),
                               A(r"\bQ1\s+2027\b", "i"), A(r"\bCoffee\s+Fest\s+(?:Dallas|DFW)\b", "i"),
                               A(r"\bBellwether\s+app\b", "i")],
        "attribution_window_chars": 60,
        "attribution_rule": "token attributed to Bellwether iff an anchor ends within the 60 characters preceding the token and no other registry brand alias match lies between that anchor and the token",
        "codes": ["PreShop-only", "Shop-only", "Both", "Unspecified", "Absent"],
        "note": "Shop tokens are case-sensitive so the generic phrase 'shop roaster' is not read as Bellwether's product name.",
    },
    "frame_lexicons": {
        "flags": "i",
        "venting": [r"\bvent(?:s|ed|ing|ilation|ilate|ilated)?\b", r"\bexhausts?\b", r"\bduct(?:s|ing|work)?\b",
                    r"\bchimneys?\b", r"\bflues?\b", r"\bafterburners?\b", r"\bcatalytic\b", r"\bhoods?\b"],
        "ventless": [r"\bventless\b", r"\bvent[- ]free\b", r"\bsmokeless\b", r"\bsmoke[- ]free\b", r"\bzero[- ]emissions?\b",
                     r"\b(?:no|without(?:\s+any)?|without\s+the\s+need\s+for)\s+(?:external\s+|outside\s+)?(?:venting|ventilation|vents?|ducting|ductwork|ducts|exhaust|chimney|hood)\b",
                     r"\b(?:does\s+not|doesn't|do\s+not|don't|won't|will\s+not|never)\s+(?:need|require)s?\s+(?:any\s+|an?\s+)?(?:external\s+|outside\s+)?(?:venting|ventilation|vents?|ducting|ductwork|exhaust|chimney|hood)\b",
                     r"\bno\s+need\s+(?:for|to)\s+(?:an?\s+)?(?:vent|venting|ventilation|ducting|ductwork|exhaust)\b"],
    },
    "grounding_fact_sheet": {
        "Shop Roaster": {"batch": "1.5 kg (3.3 lb)", "roasts_per_hour": "3-4",
                         "power": "200-240 VAC single phase, 30 A circuit, 5 kW; NEMA L6-30P",
                         "ventilation": "no external exhaust, ductwork or gas line; internal afterburner",
                         "certifications": "UL 197, UL 710, NSF 4, CE", "announced": "2024-03-07"},
        "Series 2": {"batch": "2.7 kg (6 lb)", "power": "240 V single phase or 208 V three phase, 50 A circuit",
                     "announced": "2022-02"},
        "Series 1": {"launched": "2018 (US)", "support": "technical and software support ended 2026-01-01"},
        "new Shop Roaster (2026)": {"announced": "2026-10-15", "public_debut": "Coffee Fest Dallas-Fort Worth, 2026-10-17/18, booth 210",
                                    "deliveries": "from Q1 2027", "specs": "not published in the launch release"},
        "competitor_specs_for_D4": {"Air-Motion Roasters": "spec sheet lists an exhaust exit pipe (AMR12: 247 mm); vented machine"},
    },
    "sources": [
        "Bellwether, 'Bellwether Roaster Specifications' (published 2026-02-13, modified 2026-06-19) and Shop Roaster technical specifications PDF",
        "Bellwether FAQ (Series 1 end of support; Series 2 power) and Series 2 page; accessed 2026-11-08",
        "Sprudge, 'Bellwether Announces New Smaller Footprint Shop Roaster' (2024-03-07)",
        "Sprudge, 'Bellwether Debuts New Shop Roaster ...' (2026-10-15)",
        "Daily Coffee News (2022-02-15), Bellwether Series 2; Global Coffee Report (2019-09-05; 2022)",
        "Kokoquest, Coffee Fest Dallas Fort Worth 2026 exhibitor list (accessed 2026-11-08)",
        "Coffee Equipment Pros, Roasters by Manufacturer index (accessed 2026-11-08)",
        "Daily Coffee News (2025-05-29), Air-Motion Roasters; Air-Motion AMR12 specification page",
        "Perfect Daily Grind (2023-09-11), RoasTronix / Stronghold US distribution",
        "Coffee-Tech Engineering llms.txt; Java Master (BusinessWire / CSNews); Sonofresco (Benzinga; DCN 2014, 2020)",
    ],
}

P = [
    ("F1", "F", "frame", "I own a coffee shop. Should we start roasting our own coffee in-house?"),
    ("F2", "F", "frame", "What do I need to start roasting coffee inside my café?"),
    ("F3", "F", "frame", "What are the requirements for installing a coffee roaster in a café?"),
    ("F4", "F", "frame", "Is it realistic for a small café to roast its own beans?"),
    ("F5", "F", "frame", "How much does it cost to start roasting coffee in a café?"),
    ("F6", "F", "frame", "We want to roast coffee in our retail store where customers can watch. What's involved?"),
    ("G1", "G", "recommendation", "What's the best coffee roaster for a café?"),
    ("G2", "G", "recommendation", "I run a coffee shop and want to roast our own beans. Which roaster should I buy?"),
    ("G3", "G", "recommendation", "Can you recommend a commercial coffee roaster for a small café?"),
    ("G4", "G", "recommendation", "Which roaster should a café buy to roast about 50 pounds of coffee a week?"),
    ("G5", "G", "recommendation", "What shop roasters do café owners recommend?"),
    ("G6", "G", "recommendation", "We have two cafés and want to roast for both locations. What roaster should we get?"),
    ("C1", "C", "recommendation", "What's the best coffee roaster for a café that doesn't have a gas line?"),
    ("C2", "C", "recommendation", "Can you recommend a coffee roaster we can use in our café without installing ventilation or ductwork?"),
    ("C3", "C", "recommendation", "We lease our café space and can't vent through the roof. What roaster options do we have?"),
    ("C4", "C", "recommendation", "Which commercial coffee roaster produces the least smoke for roasting indoors in a café?"),
    ("C5", "C", "recommendation", "Our city has strict air-quality rules. Which roaster can we use to roast in our shop?"),
    ("C6", "C", "recommendation", "What's the best electric coffee roaster for a coffee shop?"),
    ("R1", "R", "recommendation", "What's the best production coffee roaster for a growing specialty roastery?"),
    ("R2", "R", "recommendation", "We roast about 500 pounds of coffee a week and need a bigger roaster. What should we buy?"),
    ("R3", "R", "recommendation", "Which commercial coffee roasters are the most reliable for a wholesale roastery?"),
    ("R4", "R", "recommendation", "What's the most energy-efficient, lowest-emission production coffee roaster?"),
    ("R5", "R", "recommendation", "Which roaster should a new roasting company buy to supply local cafés and grocery stores?"),
    ("R6", "R", "recommendation", "What do professional roasters consider the best commercial coffee roaster on the market?"),
    ("K1", "K", "bellwether_probe", "What is Bellwether Coffee's newest roaster?"),
    ("K2", "K", "bellwether_probe", "Which coffee roasters does Bellwether Coffee currently sell?"),
    ("K3", "K", "bellwether_probe", "Does the Bellwether coffee roaster need ventilation?"),
    ("K4", "K", "bellwether_probe", "I've decided to buy a Bellwether roaster for my café. Which model should I get?"),
    ("K5", "K", "bellwether_probe", "How much coffee can a Bellwether roaster roast per batch?"),
    ("K6", "K", "bellwether_probe", "How is Bellwether's coffee roaster different from other commercial roasters?"),
]
probes = [{"probe_id": i, "tier": t, "kind": k, "prompt": p,
           "sha256": hashlib.sha256(p.encode("utf-8")).hexdigest()} for i, t, k, p in P]
assert len(probes) == 30 and len({p["probe_id"] for p in probes}) == 30

battery = {
    "phase": "v0.39",
    "status": "locked at tag v0.39-prereg-r1 (2026-11-08)",
    "tier_labels": {"F": "Frame: in-house roasting decision (no brand asked)",
                    "G": "Café roaster recommendation, no constraint",
                    "C": "Café roaster recommendation under the infrastructure constraint (gas / venting / smoke / air quality / electric)",
                    "R": "Production roastery recommendation (contrast)",
                    "K": "Bellwether probe (brand named)"},
    "arms": {
        "L": {"label": "legacy fixed panel (v0.17-v0.38)", "models": ["M1", "M2", "M3", "M4", "M5", "M6"],
              "decoding": {"temperature": 0.0, "max_output_tokens": 2048, "system_prompt": None, "calls_per_cell": 1},
              "conditions": ["S0"]},
        "C": {"label": "current assistants", "models": ["C1", "C2", "C3"],
              "decoding": {"temperature": "provider default (not set)", "reasoning_effort": "provider default (not set)",
                           "max_output_tokens": 16384, "system_prompt": None, "calls_per_cell": 1},
              "conditions": ["S0", "S1"]},
    },
    "conditions": {
        "S0": "no tools",
        "S1": {"anthropic": {"type": "web_search_20250305", "name": "web_search", "max_uses": 5,
                             "user_location": {"type": "approximate", "country": "US"}},
               "openai": {"type": "web_search", "search_context_size": "medium",
                          "user_location": {"type": "approximate", "country": "US"},
                          "include": ["web_search_call.action.sources"]},
               "google": {"tool": "google_search", "note": "provider defaults"}},
    },
    "calls": {"L": 30 * 6, "C": 30 * 3 * 2, "total": 30 * 6 + 30 * 3 * 2},
    "probes": probes,
}

(OUT / "registries").mkdir(parents=True, exist_ok=True)
(OUT / "prereg").mkdir(parents=True, exist_ok=True)
(OUT / "registries" / "brands_commercial_roasters_v0.39.json").write_text(
    json.dumps(registry, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
(OUT / "prereg" / "probes_v0_39.json").write_text(
    json.dumps(battery, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("brands:", len(brands), "| strata:", {s: sum(b["stratum"] == s for b in brands) for s in "SAMD"},
      "| probes:", len(probes), "| calls:", battery["calls"])
