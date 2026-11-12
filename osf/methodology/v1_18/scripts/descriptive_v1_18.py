"""AIAS v1.18 ex-post descriptive (DEVIATIONS Entry 1, 2026-11-12). Changes no locked file and no locked result.
Closes three reporting gaps of the locked output:
  (a) per rated brand and pooled, the UNRESOLVED share of cited domains, citations field (pre-registration §4.3);
  (b) the same for the sources field (S5);
  (c) per rated brand, the number of bootstrap draws with a value, flagged below 1,000 (50% of 2,000),
      read from outputs/v1_18_results.json.
UNRESOLVED share of one (answer, brand) pair = table-UNRESOLVED domains / all distinct resolved domains of the
answer (the S1 'unresolved out' denominator, common_v1_18.pair_shares(..., {'unresolved': 'out'})["_mix"]).
Pooled pair-weighted = mean over all pairs (primary; the way program_level pools S1's mix); also given:
pair-weighted over rated brands' pairs only, brand-weighted over rated brands, and domain-weighted over answers.
Run: python3 osf/methodology/v1_18/scripts/descriptive_v1_18.py --t4 T4 --coded CODED_DIR
"""
import argparse
import csv
import glob
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common_v1_18 as C  # noqa: E402

RESULTS = C.PHASE / "outputs" / "v1_18_results.json"
OUT = C.PHASE / "outputs" / "descriptive_v1_18.json"
DRAW_FLAG = 1000          # fewer than 50% of N_BOOT = 2,000 draws with a value
OUT_OPTS = {"unresolved": "out"}


def key(u):
    return ":".join(map(str, u))


def unresolved_shares(answers, units, table, rated):
    """UNRESOLVED share (0-100) per brand and pooled, under the S1 'out' denominator."""
    all_db = set().union(*[u["domains"] for u in units.values()])
    _, pairs = C.brand_shares(answers, units, all_db, table, OUT_OPTS)
    per = {}
    for u, ps in pairs:
        per.setdefault(key(u), []).append(ps["_mix"]["UNRESOLVED"])
    brands = {k: {"n_pairs": len(v), "unresolved_share": 100.0 * sum(v) / len(v)}
              for k, v in sorted(per.items()) if k in rated}
    allv = [ps["_mix"]["UNRESOLVED"] for _, ps in pairs]
    ratedv = [ps["_mix"]["UNRESOLVED"] for u, ps in pairs if key(u) in rated]
    n_un = n_all = 0
    for a in answers:
        labels = [table.get(d, {}).get("cls") for d in a["domains"] if d not in all_db]
        n_all += len(a["domains"])
        n_un += sum(1 for x in labels if x == "UNRESOLVED")
    mean = lambda v: 100.0 * sum(v) / len(v) if v else None  # noqa: E731
    return {
        "pooled": {
            "pair_weighted_all_pairs": mean(allv), "n_pairs_all": len(allv),
            "pair_weighted_rated_brands": mean(ratedv), "n_pairs_rated": len(ratedv),
            "brand_weighted_rated_brands": (sum(b["unresolved_share"] for b in brands.values()) / len(brands)
                                            if brands else None),
            "domain_weighted_answers": 100.0 * n_un / n_all if n_all else None,
            "n_domain_mentions": n_all, "n_unresolved_mentions": n_un},
        "brands": brands,
    }


def draw_counts(results, flag=DRAW_FLAG):
    """Per rated brand: draws with a value, per definition and the minimum; flag if the minimum < flag."""
    rated = sorted(k for k, r in results["primary"]["brands"].items() if r["rated"])
    ci = results["primary_ci"]["brand"]
    out = {}
    for b in rated:
        per = {d: ci[f"{b}|{d}"][2] for d in C.DEF_ORDER if f"{b}|{d}" in ci}
        m = min(per.values()) if per else 0
        out[b] = {"draws_with_value": per, "min_draws": m, "below_flag": m < flag}
    return {"n_boot": results["primary_ci"]["n_boot"], "flag_below": flag, "brands": out,
            "flagged": [b for b, v in out.items() if v["below_flag"]]}


def build(answers, answers_src, units, table, results):
    rated = {k for k, r in results["primary"]["brands"].items() if r["rated"]}
    return {"citations_field": unresolved_shares(answers, units, table, rated),
            "sources_field_S5": unresolved_shares(answers_src, units, table, rated),
            "bootstrap_draws": draw_counts(results)}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--t4", required=True)
    ap.add_argument("--coded", required=True)
    a = ap.parse_args(argv)
    s = C.load_v113()
    classes = s.load_classes(C.V113_CLASSES)
    units = s.load_brand_domains(C.V113_DOMAINS)
    table = C.load_domain_table()
    recs = s.dedupe_calls(s.read_jsonl(a.t4))
    cat = s.select_calls(recs, s.PANELS["N3"], "S1", "B")
    rows = []
    for p in sorted(glob.glob(str(Path(a.coded) / "*_phase_b.csv"))):
        with open(p, newline="", encoding="utf-8") as f:
            rows += list(csv.DictReader(f))
    named = s.named_index(rows, units)
    ans = C.answers_from_records(cat, named, classes, s, C.PRIMARY_FIELD)
    ans_src = C.answers_from_records(cat, named, classes, s, C.SENS_FIELD)
    results = json.loads(RESULTS.read_text())
    res = build(ans, ans_src, units, table, results)
    res["inputs"] = {"t4": [a.t4, C.sha256_file(a.t4)], "n_answers": len(ans),
                     "domain_table": C.sha256_file(C.DOMAIN_TABLE),
                     "v1_18_results": C.sha256_file(RESULTS),
                     "script": C.sha256_file(Path(__file__))}
    res["note"] = ("Ex-post descriptive (DEVIATIONS Entry 1). No estimand, interval or verdict of "
                   "v1_18_results.json changes. Shares in percent.")
    OUT.write_text(json.dumps(res, indent=1) + "\n")
    print("written", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
