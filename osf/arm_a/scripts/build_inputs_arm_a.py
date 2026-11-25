#!/usr/bin/env python3
"""Arm A: AI-side inputs read from locked or committed files, never from a working tree (pre-registration r4,
sections 2.1, 3.4 item 4, 3.5). No API call; no Google data.

  python3 osf/arm_a/scripts/build_inputs_arm_a.py   -> registries/arm_a_presence_r1.csv, registries/arm_a_shift_r1.csv

Every source is read with `git show <ref>:<path>` and its SHA-256 checked against SOURCES before use.
"""
import csv
import hashlib
import io
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import params_arm_a as P   # noqa: E402

WEBSITE = P.ROOT.parent / "website"     # github.com/thirdsystem-aias/website worktree (own repository)
SOURCES = {
    "v41": {"repo": None, "ref": "aias-2-0-data-locked", "path": "osf/v41/v41_three_wave_table.csv",
            "sha256": "dd239926886f24f3c9e5b12c27ea89c9c8e12a222ff7dce4070b51fd49923219"},
    "v42": {"repo": None, "ref": "v0.42-scoring-locked", "path": "osf/v42/v42_brand_table.csv",
            "sha256": "792e14addb7ad1ef03a147ee16cee56e82cfecd58030d2e8e3cf3e3ea255af7f"},
    "v40": {"repo": None, "ref": "0f40d4f", "path": "osf/v40/v40_postscore.json",
            "sha256": "aab2442f12e73f89cf0ba4b498f2aa8be3b3777dba91c8b961f6a918bb0cc00c"},
    "v25": {"repo": None, "ref": "cc36d7a", "path": "osf/v25/data/v25_merged_presence_trends.csv",
            "sha256": "2f7eb7208693ed0f67b9cde127dd368bed25abcd245729fbc6bea498911cb573"},
    "explorers": {"repo": "website", "ref": "240b2cf", "path": "content/explorers.json",
                  "sha256": "261cc2cb7a2247e421b12f231f8fe8ea040ac96a6de4789ca1a590dfc64f1910"},
}
AIRLINE_UNIT = {"AA": "BR-00488", "DL": "BR-00489", "UA": "BR-00490", "WN": "BR-00491", "AS": "BR-00492",
                "B6": "BR-00493", "F9": "BR-00494", "G4": "BR-00495", "MX": "BR-00496", "SY": "BR-00498"}
# Hawaiian (BR-00497) is inside the Alaska unit in v0.40 (R8): no own value.
BANK_UNIT = {"1039502": "BR-00463", "1073757": "BR-00464", "1120754": "BR-00465", "1951350": "BR-00466",
             "1119794": "BR-00467", "2277860": "BR-00468", "2162966": "BR-00469", "2380443": "BR-00470",
             "1069778": "BR-00471", "1074156": "BR-00472", "1238565": "BR-00473", "1026632": "BR-00474",
             "1070345": "BR-00475", "1068191": "BR-00476", "1231333": "BR-00477", "1132449": "BR-00478",
             "1075612": "BR-00479", "1037003": "BR-00480", "1275216": "BR-00481", "1068025": "BR-00482",
             "1562859": "BR-00483", "1857108": "BR-00484", "3242838": "BR-00485", "4795461": "BR-00486",
             "6073350": "BR-00487"}
# Discover (BR-00521) is a v0.40 living-brand control, not a current unit: no own value.
SPIRITS_NAMES = {"Jack Daniel's": "BR-00396", "Jameson": "BR-00401", "Grey Goose": "BR-00398",
                 "Hennessy": "BR-00395", "Rémy Martin": "BR-00408"}


def read_locked(key, sources=SOURCES):
    s = sources[key]
    cwd = str(WEBSITE if s["repo"] == "website" else P.ROOT)
    raw = subprocess.run(["git", "-C", cwd, "show", f"{s['ref']}:{s['path']}"], capture_output=True, check=True).stdout
    h = hashlib.sha256(raw).hexdigest()
    if h != s["sha256"]:
        raise ValueError(f"{key}: SHA-256 {h} differs from the fixed {s['sha256']}")
    return raw.decode("utf-8")


def car_ids():
    with open(P.REG / "arm_a_domains_r1.csv", newline="", encoding="utf-8") as f:
        return {r["brand"]: r["brand_id"] for r in csv.DictReader(f) if r["category"] == "cars" and "site" not in r["brand"]}


def presence_rows(text=None):
    rows = []
    cars = car_ids()
    v41 = list(csv.DictReader(io.StringIO(text["v41"] if text else read_locked("v41"))))
    for r in v41:
        if r["substrate"] == "v0.22" and r["brand"] in cars and r["wave"] in ("t1", "t3"):
            rows.append(("cars", cars[r["brand"]], r["wave"], float(r["pi_hat"]), r["brand"], "v41"))
        if r["substrate"] == "v0.23" and r["brand"] in SPIRITS_NAMES and r["wave"] in ("t1", "t3"):
            rows.append(("spirits", SPIRITS_NAMES[r["brand"]], r["wave"], float(r["pi_hat"]), r["brand"], "v41"))
    v42 = list(csv.DictReader(io.StringIO(text["v42"] if text else read_locked("v42"))))
    for r in v42:
        if r["substrate"] == "v0.22" and r["brand"] in cars:
            rows.append(("cars", cars[r["brand"]], "t4", float(r["pi_N3_S0"]), r["brand"], "v42"))
        if r["substrate"] == "v0.23" and r["brand"] in SPIRITS_NAMES:
            rows.append(("spirits", SPIRITS_NAMES[r["brand"]], "t4", float(r["pi_N3_S0"]), r["brand"], "v42"))
    v40 = json.loads(text["v40"] if text else read_locked("v40"))["prereg"]["d1_ai_share"]
    for cat, umap, label in (("airline", AIRLINE_UNIT, "airlines"), ("bank", BANK_UNIT, "banks")):
        pooled = v40[cat]["pooled"]["all_nine_S0"]
        for unit, v in pooled.items():
            if unit in umap:
                rows.append((label, umap[unit], "v0.40", float(v["ai_share"]), unit, "v40"))
    v25 = list(csv.DictReader(io.StringIO(text["v25"] if text else read_locked("v25"))))
    with open(P.REG / "arm_a_domains_r1.csv", newline="", encoding="utf-8") as f:
        sw = {r["brand"]: r["brand_id"] for r in csv.DictReader(f) if r["category"] == "software"}
    for r in v25:
        if r["brand"] in sw:
            rows.append(("software", sw[r["brand"]], "v0.24", float(r["presence_composite"]), r["brand"], "v25"))
    return rows


def shift_rows(text=None):
    """Cars at t1: first-round mentions m on the three recommendation questions (q1-q3, 18 answers per brand) from
    the site's deposited explorer data, joined to the transcribed 2025 units x price (registries/arm_a_cars_sales_r1.csv)."""
    ex = json.loads(text["explorers"] if text else read_locked("explorers"))["explorers"]["v0.22"]
    rec_ids = [q["id"] for q in ex["questions"] if q["set"] == "cat"]
    if rec_ids != ["q1", "q2", "q3"]:
        raise ValueError(f"recommendation questions are {rec_ids}, expected q1-q3")
    m = {b["name"]: sum(b["q"][:3]) for b in ex["brands"]}
    out = []
    with open(P.REG / "arm_a_cars_sales_r1.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out.append({"brand_id": r["brand_id"], "brand": r["brand"], "group": r["group"], "m_rec": m[r["brand"]],
                        "answers": 18, "sales_usd": int(r["units_2025"]) * int(r["price_usd"])})
    return out


def main():
    pres = presence_rows()
    with open(P.REG / "arm_a_presence_r1.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["category", "brand_id", "wave", "P", "source_unit", "source"])
        w.writerows(pres)
    sh = shift_rows()
    with open(P.REG / "arm_a_shift_r1.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(sh[0]))
        w.writeheader()
        w.writerows(sh)
    print(f"presence rows {len(pres)}; shift rows {len(sh)}")


if __name__ == "__main__":
    main()
