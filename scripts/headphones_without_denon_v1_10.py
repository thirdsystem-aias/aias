#!/usr/bin/env python3
"""
AIAS v1.10 — EXPLORATORY / DESCRIPTIVE (added after the lock; DEVIATIONS Entry 2).
Headphone (v0.19) results with and without Denon, on the S7 rule: the Denon unit is
removed, answers are NOT re-ranked (every other brand keeps the position it holds with
Denon in the answer). Outside the locked scorer; changes no verdict.

Reads only: the hashed OMNI v0.19 rank tables (outputs/rank_tables/OMNI_t*_v0.19.csv),
outputs/v1_10_verdicts.json (baseline rows, for the with-Denon check) and
osf/aias_2_0/aias_2_0_profiles.csv (Denon's P, C* and mention count).
Writes: osf/methodology/v1_10/outputs/exploratory/headphones_without_denon_v1_10.json
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "osf/methodology/v1_10/outputs"
FLAG = "Denon"
REGISTRY_SIZE = 16          # osf/v19/panel_registry_v0_19.csv
FLOOR = 6
csv.field_size_limit(sys.maxsize)


def load(wave):
    with open(OUT / f"rank_tables/OMNI_{wave}_v0.19.csv", newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["rule"] == "lead_item" and r["status"] == "ok"]


def describe(rows, drop=None):
    """Baseline quantities (pre-registration section 8) for one wave, optionally without one brand."""
    answers = {}
    for r in rows:
        answers.setdefault(r["answer_id"], {"rankable": r["rankable"] == "1", "brands": {}})
        if r["brand"] and r["rankable"] == "1":
            answers[r["answer_id"]]["brands"][r["brand"]] = (float(r["k_mid"]), int(r["k_min"]), int(r["n_named"]))
    R = [a for a in answers.values() if a["rankable"]]
    q = defaultdict(list)
    for a in R:
        for b, (km, kn, n) in a["brands"].items():
            if b != drop:
                q[b].append((km - 1) / (n - 1))
    mnp = {b: 100 * (1 - np.mean(v)) for b, v in q.items()}
    rated = sorted(b for b, v in q.items() if len(v) >= FLOOR)
    named = [sum(1 for b in a["brands"] if b != drop) for a in R]
    firsts, led = Counter(), Counter()
    for a in R:
        f = [b for b, v in a["brands"].items() if v[1] == 1 and b != drop]
        for b in f:
            firsts[b] += 1.0 / len(f)
            led[b] += 1
    vals = [mnp[b] for b in rated]
    return {
        "registry_size": REGISTRY_SIZE - (1 if drop else 0),
        "rankable_answers": len(R),
        "registry_brands_named_per_rankable_answer": {"median": float(np.median(named)),
                                                      "q25": float(np.quantile(named, .25)),
                                                      "q75": float(np.quantile(named, .75)), "max": int(max(named))},
        "brands_rated": len(rated),
        "rated_share_of_registry": len(rated) / (REGISTRY_SIZE - (1 if drop else 0)),
        "R_star_MNP": {"median": float(np.median(vals)), "q25": float(np.quantile(vals, .25)),
                       "q75": float(np.quantile(vals, .75)), "min": float(min(vals)), "max": float(max(vals))},
        "leader_share_most_frequent_first": max(led.values()) / len(R),
        "leader_herfindahl": sum((v / len(R)) ** 2 for v in firsts.values()),
        "top3_by_R_star": [[b, mnp[b]] for b in sorted(rated, key=lambda b: (-mnp[b], b))[:3]],
        "flagged_brand_in_rankable_answers": [{"answer": aid.split("::")[1], "k_mid": a["brands"][FLAG][0],
                                               "n_named": a["brands"][FLAG][2]}
                                              for aid, a in answers.items() if a["rankable"] and FLAG in a["brands"]],
    }


def main():
    verdicts = json.loads((OUT / "v1_10_verdicts.json").read_text())
    base = {r["wave"]: r for r in verdicts["baseline"] if r["set"].startswith("OMNI") and r["category"] == "v0.19"}
    prof = {}
    with open(ROOT / "osf/aias_2_0/aias_2_0_profiles.csv", newline="") as f:
        for r in csv.DictReader(f):
            if r["substrate"] == "v0.19" and r["brand"] == FLAG:
                prof[r["wave"]] = {k: r[k] for k in ("P", "C_star", "rated", "n_mentions")}
    res = {"label": "EXPLORATORY / DESCRIPTIVE - added after the lock (DEVIATIONS Entry 2); changes no verdict",
           "rule": "Denon unit removed; answers not re-ranked", "denon_profiles_aias_2_0": prof, "waves": {}}
    for w in ("t1", "t2", "t3"):
        rows = load(w)
        withd, without = describe(rows), describe(rows, FLAG)
        b = base[w]
        check = {"brands_rated": b["brands_rated"] == withd["brands_rated"],
                 "median_named": b["brands_named_per_rankable_answer"]["median"] == withd["registry_brands_named_per_rankable_answer"]["median"],
                 "leader_share": abs(b["leader_share_most_frequent_first"] - withd["leader_share_most_frequent_first"]) < 1e-12,
                 "herfindahl": abs(b["leader_herfindahl"] - withd["leader_herfindahl"]) < 1e-12,
                 "R_star_median": abs(b["R_star_MNP"]["median"] - withd["R_star_MNP"]["median"]) < 1e-9}
        res["waves"][w] = {"with_denon": withd, "without_denon": without, "with_denon_matches_scorer_baseline": check}
    sens = verdicts["sensitivities"]["S7_without_coi_flagged"]
    res["S7_gate_statistics"] = {h: {w: [verdicts[k]["per_wave"][w]["rho"], sens["detail"][h]["per_wave"][w]["rho"]]
                                     for w in ("t1", "t2", "t3")}
                                 for h, k in (("H1", "H1_Sep_Presence"), ("H2", "H2_Sep_Consistency"))}
    res["S7_gate_statistics"]["H3"] = [verdicts["H3_Rank_Stability"]["rho"], sens["detail"]["H3"]["rho"]]
    (OUT / "exploratory").mkdir(exist_ok=True)
    p = OUT / "exploratory/headphones_without_denon_v1_10.json"
    p.write_text(json.dumps(res, indent=2) + "\n")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
