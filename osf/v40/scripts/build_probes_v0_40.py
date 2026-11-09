#!/usr/bin/env python3
"""AIAS v0.40 probe builder (DRAFT for Pablo's review; locks at tag v0.40-prereg-r1).

Builds the probe battery by rule from the registry outputs:
  registries/out/exits_and_controls.csv   ghosts in the registry and living-brand controls
  registries/out/airlines_current.csv     top two airline brands by brand share (incumbent controls)
  registries/out/banks_current.csv        top two bank holders by deposit share (incumbent controls)
and copies the S1 tool configurations verbatim from the locked v0.39 battery (osf/v39/prereg/probes_v0_39.json).

Battery (approved design, 2026-11-08):
  per category: 6 generic recommendation probes (RQ1), 6 by need, 4 by Census region  -> 16 x 2 = 32
  per ghost and per control (living brands and the top two incumbents): one recognition probe (K)
  and one status probe (S)
Calls per probe: legacy 6 models x 3 runs + 1 Gemini 2.5 Flash pass at the v0.39 setting = 19;
current 3 models x 2 conditions (S0, S1) x 3 runs = 18; total 37.

Writes prereg/probes_v0_40.json (v0.39 schema plus subject fields) and prereg/probes_v0_40.md (review table).

Usage (from ~/aias):  python3 osf/v40/scripts/build_probes_v0_40.py
"""
import hashlib
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]          # osf/v40
V39 = ROOT.parent / "v39" / "prereg" / "probes_v0_39.json"
OUT_JSON = ROOT / "prereg" / "probes_v0_40.json"
OUT_MD = ROOT / "prereg" / "probes_v0_40.md"

REC = {
    "airline": {
        "G": ["What are the best airlines in the United States?",
              "Which airline should I fly for trips within the US?",
              "Can you recommend a few good US airlines?",
              "I'm booking a domestic flight in the US. Which airlines should I consider?",
              "What are the top US airlines for domestic travel?",
              "Which US airline would you recommend, and why?"],
        "N": ["Which US airline is best for cheap fares?",
              "Which US airline has the best frequent flyer program?",
              "Which US airline is the most comfortable to fly in economy?",
              "Which US airline is the most reliable for on-time arrivals?",
              "Which US airline has the best customer service?",
              "Which US airline is best for flying with young children?"],
        "R": "I live in the {region} of the United States. Which airline should I fly most of the time?",
    },
    "bank": {
        "G": ["What are the best banks in the United States?",
              "Which bank should I open a checking account with in the US?",
              "Can you recommend a few good US banks?",
              "I'm switching banks in the US. Which banks should I consider?",
              "What are the top US banks for everyday banking?",
              "Which US bank would you recommend, and why?"],
        "N": ["Which US bank is best for a high-yield savings account?",
              "Which US bank has the lowest fees on checking accounts?",
              "Which US bank is best for a small business?",
              "Which US bank is best for a college student's first account?",
              "Which US bank is best for getting a mortgage?",
              "Which US bank has the most branches and ATMs across the country?"],
        "R": "I live in the {region} of the United States. Which bank should I use?",
    },
}
REGIONS = ["Northeast", "Midwest", "South", "West"]           # the four Census regions
K_TEMPLATE = "What is {name}?"
S_TEMPLATE = {"airline": "Can I still book a flight with {name}?", "bank": "Can I still open an account with {name}?"}

FDIC = "https://api.fdic.gov/banks/institutions?filters=CERT:{}"
# Name used in K and S probes. Default: the registry brand. Overrides give the full consumer name, or add the
# disambiguator D11 requires where another US bank uses the same name (city from the FDIC institution record).
PROBE_NAME = {
    "COMMERCE":    ("Commerce Bank (Philadelphia)", "FDIC CERT 21140: Commerce Bank, National Association, Philadelphia, PA; " + FDIC.format(21140)),
    "UNIONBANK":   ("MUFG Union Bank", "FDIC CERT 22826: MUFG Union Bank, National Association, San Francisco, CA; " + FDIC.format(22826)),
    "SIGNATURE":   ("Signature Bank (New York)", "FDIC CERT 57053: Signature Bank, New York, NY; " + FDIC.format(57053)),
    "COUNTRYWIDE": ("Countrywide Bank", "registry alias"),
    "NATCITY":     ("National City Bank", "registry alias"),
    "BMOHARRIS":   ("BMO Harris Bank", "registry alias"),
    "DISCOVER":    ("Discover Bank", "registry alias"),
    "JPMC":        ("Chase Bank", "consumer name of the JPMorgan Chase holder"),
}
TIER_LABELS = {
    "AG": "Airline recommendation, generic (RQ1)", "AN": "Airline recommendation, by need",
    "AR": "Airline recommendation, by Census region", "BG": "Bank recommendation, generic (RQ1)",
    "BN": "Bank recommendation, by need", "BR": "Bank recommendation, by Census region",
    "K": "Recognition probe, one per ghost and per control", "S": "Status probe, one per ghost and per control",
}


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def subjects():
    ev = pd.read_csv(ROOT / "registries" / "out" / "exits_and_controls.csv", dtype=str).fillna("")
    rows = []
    for r in ev.itertuples():
        if r.role == "ghost" and r.in_registry != "True":
            continue
        rows.append({"subject_id": r.id, "category": r.category, "role": r.role, "registry_brand": r.brand})
    air = pd.read_csv(ROOT / "registries" / "out" / "airlines_current.csv").sort_values("brand_share_pct", ascending=False)
    for r in air.head(2).itertuples():
        rows.append({"subject_id": r.code, "category": "airline", "role": "incumbent", "registry_brand": r.name})
    bk = pd.read_csv(ROOT / "registries" / "out" / "banks_current.csv").sort_values("share_pct", ascending=False)
    tags = {"JPMORGAN CHASE & CO.": "JPMC", "BANK OF AMERICA CORPORATION": "BAC"}
    for r in bk.head(2).itertuples():
        rows.append({"subject_id": tags.get(r.holder_name, str(r.HOLDER)), "category": "bank", "role": "incumbent",
                     "registry_brand": r.brand, "holder_rssd": str(r.HOLDER)})
    for s in rows:
        name, src = PROBE_NAME.get(s["subject_id"], (s["registry_brand"], "registry brand"))
        s["name_in_probe"], s["name_source"] = name, src
    return rows


def battery(subs):
    probes = []
    for cat, pre in (("airline", "A"), ("bank", "B")):
        for kind, tier in (("G", pre + "G"), ("N", pre + "N")):
            for i, p in enumerate(REC[cat][kind], 1):
                probes.append({"probe_id": f"{tier}{i}", "tier": tier, "kind": "recommendation", "category": cat, "prompt": p})
        for i, reg in enumerate(REGIONS, 1):
            probes.append({"probe_id": f"{pre}R{i}", "tier": pre + "R", "kind": "recommendation", "category": cat,
                           "region": reg, "prompt": REC[cat]["R"].format(region=reg)})
    for t, kind in (("K", "recognition"), ("S", "status")):
        for s in subs:
            tpl = K_TEMPLATE if t == "K" else S_TEMPLATE[s["category"]]
            probes.append({"probe_id": f"{t}_{s['subject_id']}", "tier": t, "kind": kind, "category": s["category"],
                           "subject_id": s["subject_id"], "subject_role": s["role"],
                           "prompt": tpl.format(name=s["name_in_probe"])})
    for p in probes:
        p["sha256"] = sha(p["prompt"])
    ids = [p["probe_id"] for p in probes]
    assert len(ids) == len(set(ids)), "duplicate probe IDs"
    assert len({p["prompt"] for p in probes}) == len(probes), "duplicate prompts"
    return probes


def main():
    v39 = json.loads(V39.read_text(encoding="utf-8"))
    subs = subjects()
    probes = battery(subs)
    n = len(probes)
    spec = {
        "phase": "v0.40",
        "status": "DRAFT for Pablo's review (2026-11-08); locks at tag v0.40-prereg-r1",
        "tier_labels": TIER_LABELS,
        "arms": {
            "L": {"label": "legacy fixed panel (v0.17-v0.39)", "models": ["M1", "M2", "M3", "M4", "M5", "M6"],
                  "decoding": {"temperature": 0.0, "max_output_tokens": 2048, "system_prompt": None, "runs_per_cell": 3,
                               "M5_gemini_2_5_flash": "thinking_budget 0 (primary); plus one pass per probe at the v0.39 setting (provider-default thinking), reported, not tested"},
                  "conditions": ["S0"]},
            "C": {"label": "current assistants", "models": ["C1", "C2", "C3"],
                  "decoding": {"temperature": "provider default", "reasoning_effort": "provider default",
                               "max_output_tokens": 16384, "system_prompt": None, "runs_per_cell": 3},
                  "conditions": ["S0", "S1"]},
        },
        "conditions": v39["conditions"],
        "calls": {"per_probe": {"L": 19, "C": 18, "total": 37}, "L": 19 * n, "C": 18 * n, "total": 37 * n},
        "subjects": subs,
        "probes": probes,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")

    by = pd.DataFrame(probes)
    lines = ["# AIAS v0.40 probe set (DRAFT for review)", "",
             f"Built by `osf/v40/scripts/build_probes_v0_40.py` from the registry outputs. {n} probes; "
             f"{37 * n:,} calls (37 per probe: legacy 6 models x 3 runs + 1 Gemini 2.5 Flash pass at the v0.39 setting; "
             f"current 3 models x 2 conditions x 3 runs). Locks at tag `v0.40-prereg-r1`.", "",
             "Wording rules: one user turn, no system prompt; recommendation probes name no brand and say \"US\"; "
             "the generic probes feed RQ1; every ghost and every control gets one recognition (K) and one status (S) probe; "
             "a disambiguator from the FDIC institution record is added where another US bank uses the same name (D11).", ""]
    for tier, lab in TIER_LABELS.items():
        sub = by[by.tier == tier]
        lines += [f"## {tier}: {lab} ({len(sub)})", "", "| ID | Prompt |", "|---|---|"]
        lines += [f"| {r.probe_id} | {r.prompt} |" for r in sub.itertuples()]
        lines.append("")
    lines += ["## Subjects of the K and S probes", "", "| ID | Category | Role | Name in probe | Source of the name |", "|---|---|---|---|---|"]
    lines += [f"| {s['subject_id']} | {s['category']} | {s['role']} | {s['name_in_probe']} | {s['name_source']} |" for s in subs]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    counts = by.tier.value_counts().reindex(list(TIER_LABELS)).to_dict()
    roles = pd.DataFrame(subs).role.value_counts().to_dict()
    print(json.dumps({"probes": n, "by_tier": counts, "subjects": len(subs), "by_role": roles, "calls": spec["calls"]}, indent=1))


if __name__ == "__main__":
    main()
