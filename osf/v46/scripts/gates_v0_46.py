#!/usr/bin/env python3
"""gates_v0_46.py -- AIAS(TM) v0.46 (#76): code-parity gates G1 and G2 (stage1_manuscript_r1.md sections 3.4, 5.6).

G1: the v0.46 P function (predictors_v0_46.compute), run on t4's files at tag v0.42-scoring-locked, reproduces
    v1.14 Stage 1's stored P_S0 for every unit (stage1_v1_14.json at commit 3129674).
G2: its R* function reproduces Stage 1's stored R*_S0 for every rated unit (and the rated set), and the
    orientation holds (higher = nearer the top: each rated R* equals -(smallest modal k_min) of the unit's
    rankable mentions, recomputed independently, and R* <= -1).
Outcome-neutral: t4 values reproduced here enter no test of H1-H5. Inputs are read from git (`git show`), never
from the working tree; nothing is collected; NO MODEL IS CALLED.

Tolerance (DECISION: the manuscript says "reproduces"): P within 1e-9 absolute (floating point only); R* exact.
The gates run on all units Stage 1 stored (five substrates, t4's N3 panel); the v0.46 subset (v0.20-v0.23) is
also reported. The result file records the SHA-256 of predictors_v0_46.py; acquire_v0_46.py refuses unless
the file says both gates pass for the predictor code as it now stands.

Usage:
  python3 osf/v46/scripts/gates_v0_46.py            # runs G1, G2; writes osf/v46/prereg/code_parity_v0_46.json
  python3 osf/v46/scripts/gates_v0_46.py --check    # exit 0 iff the stored result is green for the current code
"""
import argparse
import collections
import csv
import hashlib
import io
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import predictors_v0_46 as PR  # noqa: E402

V114 = PR.V114
ROOT = PR.ROOT
T4_TAG = "v0.42-scoring-locked"
T4_RAW = "osf/v42/data/t4_raw.jsonl"
T4_CODED = "osf/v42/data/coded"
T4_BRAND_TABLE = "osf/v42/v42_brand_table.csv"
STAGE1_COMMIT = PR.REF_COMMIT
STAGE1_JSON = "osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json"
N3 = list(V114.N3)
P_TOL = 1e-9
RESULT = ROOT / "osf/v46/prereg/code_parity_v0_46.json"
ALL_SUBS = ("v0.19", "v0.20", "v0.21", "v0.22", "v0.23")


def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def code_fingerprint():
    """SHA-256 of the code the gates certify."""
    files = [HERE / "predictors_v0_46.py"] + [PR.REF_DIR / n for n in sorted(PR.REF_FILES)]
    return {str(p.relative_to(ROOT)): sha256_file(p) for p in files}


def _key(u):
    return (u["substrate"], u["brand"])


def g1(pred, stored_units, subs=ALL_SUBS, tol=P_TOL):
    """Every stored unit: P_S0 reproduced within `tol` (None must stay None)."""
    bad, n = [], 0
    for u in stored_units:
        if u["substrate"] not in subs:
            continue
        n += 1
        want, got = u.get("P_S0"), pred.get(_key(u), {}).get("P")
        ok = (want is None and got is None) or (want is not None and got is not None and abs(want - got) <= tol)
        if not ok:
            bad.append({"unit": list(_key(u)), "stored": want, "recomputed": got})
    diffs = [abs(u["P_S0"] - pred[_key(u)]["P"]) for u in stored_units if u["substrate"] in subs
             and u.get("P_S0") is not None and pred.get(_key(u), {}).get("P") is not None]
    return {"units_compared": n, "with_P": len(diffs), "mismatches": len(bad), "examples": bad[:10],
            "max_abs_diff": max(diffs) if diffs else None, "tolerance": tol, "passes": n > 0 and not bad}


def orientation(rows, pred, subs=ALL_SUBS):
    """R* = -(smallest modal k_min), recomputed from the rankable rows without v1.14's code; and R* <= -1."""
    km = collections.defaultdict(list)
    for r in rows:
        km[(r["category"], r["brand"])].append(int(r["k_min"]))
    bad = []
    for u, v in pred.items():
        if u[0] not in subs or not v["rated"]:
            continue
        c = collections.Counter(km[u])
        top = max(c.values())
        want = -float(min(k for k, n in c.items() if n == top))
        if v["R_star"] != want or v["R_star"] > -1:
            bad.append({"unit": list(u), "R_star": v["R_star"], "independent": want})
    return {"mismatches": len(bad), "examples": bad[:10], "passes": not bad}


def g2(pred, stored_units, rows, subs=ALL_SUBS):
    """Every stored rated unit: R*_S0 reproduced exactly; same rated set; orientation."""
    bad, n = [], 0
    for u in stored_units:
        if u["substrate"] not in subs:
            continue
        p = pred.get(_key(u), {})
        if bool(u.get("rated_S0")) != bool(p.get("rated")) or int(u.get("n_ranked_S0", 0)) != int(p.get("n_ranked", 0)):
            bad.append({"unit": list(_key(u)), "stored": [u.get("rated_S0"), u.get("n_ranked_S0")],
                        "recomputed": [p.get("rated"), p.get("n_ranked")]})
            continue
        if u.get("rated_S0"):
            n += 1
            if p.get("R_star") is None or float(u["R_star_S0"]) != float(p["R_star"]):
                bad.append({"unit": list(_key(u)), "stored": u["R_star_S0"], "recomputed": p.get("R_star")})
    extra = sorted(list(k) for k, v in pred.items() if k[0] in subs and v["rated"]
                   and k not in {_key(u) for u in stored_units})
    ori = orientation(rows, pred, subs)
    return {"rated_units_compared": n, "mismatches": len(bad), "examples": bad[:10],
            "rated_but_not_stored": extra, "orientation": ori,
            "passes": n > 0 and not bad and not extra and ori["passes"]}


def load_t4(repo=ROOT):
    """t4's raw answers and coded tables at T4_TAG, and v1.14 Stage 1's stored units at 3129674 (git only)."""
    src = V114.Source(ref=T4_TAG, repo=repo)
    raw = V114.read_jsonl_text(src.text(T4_RAW))
    coded_a, coded_b = V114.read_coded(src, T4_CODED)
    st = V114.Source(ref=STAGE1_COMMIT, repo=repo)
    stage1 = json.loads(st.text(STAGE1_JSON))
    reads = {f"{T4_TAG}:{k}": v for k, v in src.log.items()}
    reads.update({f"{STAGE1_COMMIT[:7]}:{k}": v for k, v in st.log.items()})
    return raw, coded_a, coded_b, stage1, reads


def run_gates(log=print):
    raw, ca, cb, stage1, reads = load_t4()
    regs = PR.load_registries(ALL_SUBS)
    log(f"[v46 gates] t4: {len(raw)} raw lines, {len(ca)} coded A rows, {len(cb)} coded B rows; "
        f"Stage 1 stored units {len(stage1['units'])}")
    pred, meta = PR.compute(raw, ca, cb, N3, subs=ALL_SUBS, registries=regs, wave="t4")
    rows = V114.wave_rows(meta.pop("_infos"), PR.RULE, PR.COND)
    units = stage1["units"]
    res = {"phase": "v0.46", "gates": "G1/G2 code parity (stage1_manuscript_r1.md 3.4)",
           "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "t4_tag": T4_TAG, "stage1_commit": STAGE1_COMMIT, "inputs_read": reads, "panel": N3,
           "code_sha256": code_fingerprint(), "answers_in_analysis_set": meta["answers"]}
    res["G1"] = g1(pred, units)
    res["G2"] = g2(pred, units, rows)
    res["G1_v46_subset"] = g1(pred, units, PR.V46_SUBS)
    res["G2_v46_subset"] = g2(pred, units, rows, PR.V46_SUBS)
    # informative (not a gate input): Stage 1 stored P only for the 93 units with ranked mentions; for all 112
    # units, the recomputed pi_hat is compared with v0.42's brand table (pi_N3_S0), the input v1.14 read
    bt = list(csv.DictReader(io.StringIO(V114.Source(ref=T4_TAG, repo=ROOT).text(T4_BRAND_TABLE))))
    mis = [(r["substrate"], r["brand"]) for r in bt
           if V114._num(r.get("pi_N3_S0")) != pred.get((r["substrate"], r["brand"]), {}).get("pi_hat")]
    res["pi_hat_vs_v042_brand_table"] = {"units": len(bt), "mismatches": len(mis), "examples": mis[:10],
                                         "agrees": bool(bt) and not mis}
    res["both_pass"] = bool(res["G1"]["passes"] and res["G2"]["passes"])
    log(f"  G1: {res['G1']['units_compared']} units ({res['G1']['with_P']} with P), mismatches "
        f"{res['G1']['mismatches']}, max |diff| {res['G1']['max_abs_diff']} -> {'PASS' if res['G1']['passes'] else 'FAIL'}")
    log(f"  G2: {res['G2']['rated_units_compared']} rated units, mismatches {res['G2']['mismatches']}, orientation "
        f"{'ok' if res['G2']['orientation']['passes'] else 'FAIL'} -> {'PASS' if res['G2']['passes'] else 'FAIL'}")
    log(f"  v0.46 subset: G1 {res['G1_v46_subset']['units_compared']} units "
        f"{'PASS' if res['G1_v46_subset']['passes'] else 'FAIL'}; G2 {res['G2_v46_subset']['rated_units_compared']} "
        f"rated {'PASS' if res['G2_v46_subset']['passes'] else 'FAIL'}")
    log(f"  pi_hat vs v0.42 brand table (informative): {res['pi_hat_vs_v042_brand_table']['units']} units, "
        f"mismatches {res['pi_hat_vs_v042_brand_table']['mismatches']}")
    return res


def green(path=RESULT):
    """(ok, why): the stored gate result says both pass AND certifies the predictor code as it now stands."""
    p = Path(path)
    if not p.exists():
        return False, f"no gate result {p} (run gates_v0_46.py)"
    try:
        r = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return False, f"unreadable gate result: {e}"
    if not r.get("both_pass"):
        return False, "G1/G2 did not both pass"
    if r.get("code_sha256") != code_fingerprint():
        return False, "predictor code changed since the gates ran (re-run gates_v0_46.py)"
    return True, "G1 and G2 pass for the current predictor code"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--out", default=str(RESULT))
    a = ap.parse_args(argv)
    if a.check:
        ok, why = green(a.out)
        print(f"[v46 gates] {'GREEN' if ok else 'NOT GREEN'}: {why}")
        return 0 if ok else 1
    res = run_gates()
    Path(a.out).write_text(json.dumps(res, indent=1, sort_keys=True, default=str) + "\n", encoding="utf-8")
    print(f"[v46 gates] both_pass={res['both_pass']} -> {a.out}")
    return 0 if res["both_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
