"""AIAS v1.18 analysis. Two modes:
  --synthetic   dry run on a synthetic world with a known answer (no real data read); writes outputs/dry_run/.
  --run         the real analysis on t4 (citations primary). REFUSES unless tag v1.18-prereg-r1 is on origin
                (git ls-remote) and every file in prereg/LOCK_MANIFEST_v1_18.sha256 matches its SHA-256.
"""
import argparse
import csv
import glob
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common_v1_18 as C  # noqa: E402

MANIFEST = C.PHASE / "prereg" / "LOCK_MANIFEST_v1_18.sha256"
REPO = C.PHASE.parents[2]
# Cheil Worldwide / Iris agency ties (v1.16 section 15; v0.62 DEVIATIONS Entry 0, Part F): Chevrolet, BMW,
# Bentley, Jack Daniel's, Eucerin, as unit keys of brand_domains_v1_13.csv.
COI_AGENCY_FIVE = (("v22", "C.4"), ("v22", "A.7"), ("v22", "A.5"), ("v23", "S03"), ("v20", "C.7"))


class Refused(SystemExit):
    pass


def tag_on_origin(tag=C.PREREG_TAG, remote="origin"):
    try:
        out = subprocess.run(["git", "-C", str(REPO), "ls-remote", "--tags", remote, f"refs/tags/{tag}"],
                             capture_output=True, text=True, timeout=60)
    except Exception as e:                                     # noqa: BLE001
        return False, f"ls-remote failed: {e}"
    ok = out.returncode == 0 and f"refs/tags/{tag}" in out.stdout
    return ok, out.stdout.strip() or out.stderr.strip()


def check_manifest(path=MANIFEST):
    if not path.exists():
        return False, "manifest missing"
    bad = []
    for line in path.read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        digest, rel = line.split(None, 1)
        p = Path(rel.strip())
        p = p if p.is_absolute() else REPO / p
        if not p.exists() or C.sha256_file(p) != digest:
            bad.append(rel.strip())
    return not bad, bad


def gate(tag_check=tag_on_origin, manifest_check=check_manifest):
    ok, info = tag_check()
    if not ok:
        raise Refused(f"REFUSED: tag {C.PREREG_TAG} is not on origin ({info}); nothing read")
    ok, bad = manifest_check()
    if not ok:
        raise Refused(f"REFUSED: lock-manifest mismatch: {bad}")
    return True


def run_all(answers, units, table, n_boot=C.N_BOOT, answers_sources=None, denon=("v19", "Denon")):
    all_db = set().union(*[u["domains"] for u in units.values()])
    res = {"primary": C.estimate(answers, units, all_db, table)}
    res["primary_ci"] = C.cluster_bootstrap(answers, units, all_db, table, n_boot=n_boot)
    sens = {
        "S1_unresolved_out": dict(opts={"unresolved": "out"}),
        "S1_unresolved_in": dict(opts={"unresolved": "in"}),
        "S2_retailer_as_company": dict(opts={"retailer_as_company": True}),
        "S3_alias_focal": dict(opts={"alias_focal": True}),
        "S4_floor_3": dict(floor=3), "S4_floor_10": dict(floor=10),
        "S6_without_denon": dict(exclude=(denon,)),
        "S6_COI_without_denon_and_agency_five": dict(exclude=(denon,) + COI_AGENCY_FIVE),
    }
    res["sensitivities"] = {k: C.estimate(answers, units, all_db, table, v.get("opts"), v.get("floor", C.FLOOR),
                                          v.get("exclude", ())) for k, v in sens.items()}
    gem = [a for a in answers if not a["model"].startswith("gemini")]
    res["sensitivities"]["S7_without_gemini"] = C.estimate(gem, units, all_db, table)
    if answers_sources is not None:
        res["sensitivities"]["S5_sources_field"] = C.estimate(answers_sources, units, all_db, table)
    return res


def jsonable(o):
    if isinstance(o, dict):
        return {(k if isinstance(k, str) else ":".join(map(str, k))): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, set):
        return sorted(o)
    return o


# =========================================================================== synthetic world (dry run)
def synthetic_world():
    """Two substrates x 6 brands; brand i (1..6) is named in 9 answers (3 models x 3 runs of question i).
    Each answer cites: 1 focal, i company, 7-i listing, 1 review, 1 editorial, 1 UNRESOLVED domain.
    Known answer: K = 10, P = 10(1+i), Y = 10(8-i), M = 90 for every brand; rho_w(P,Y) = -1; K has no variance.
    Plus a NONE unit (never rated) and a unit named in 3 answers only (not rated at floor 6)."""
    units, table, answers = {}, {}, []
    for k, c in (("co", "company"), ("li", "listing"), ("rv", "review_social"), ("ed", "editorial_other"),
                 ("un", "UNRESOLVED")):
        for j in range(1, 8):
            table[f"{k}{j}.example"] = {"cls": c, "retailer": False, "alias_of": ""}
    for s in ("v19", "v20"):
        for i in range(1, 7):
            units[(s, f"B{i}")] = {"substrate": s, "brand_id": f"B{i}", "brand": f"B{i}", "coder_key": f"B{i}",
                                   "status": "RESOLVED", "domains": {f"{s}-b{i}.example"}}
        units[(s, "NONE")] = {"substrate": s, "brand_id": "NONE", "brand": "NONE", "coder_key": "NONE",
                              "status": "NONE", "domains": set()}
        units[(s, "THIN")] = {"substrate": s, "brand_id": "THIN", "brand": "THIN", "coder_key": "THIN",
                              "status": "RESOLVED", "domains": {f"{s}-thin.example"}}
        for m in ("claude-x", "gpt-x", "gemini-x"):
            for i in range(1, 7):
                for run in (1, 2, 3):
                    doms = {f"{s}-b{i}.example"} | {f"co{j}.example" for j in range(1, i + 1)} \
                        | {f"li{j}.example" for j in range(1, 8 - i)} | {"rv1.example", "ed1.example", "un1.example"}
                    named = {(s, f"B{i}"), (s, "NONE")} | ({(s, "THIN")} if (m == "gpt-x" and i == 1) else set())
                    answers.append(C.make_answer(f"{s}-{m}-{i}-{run}", s, m, (s, m, i), run, named, doms))
    return answers, units, table


def expected_synthetic():
    exp = {}
    for i in range(1, 7):
        exp[i] = {"K_own_domain": 10.0, "P_any_company": 10.0 * (1 + i), "Y_own_plus_listings": 10.0 * (8 - i),
                  "M_not_owned": 90.0}
    return exp


def expected_program_pair_weighted():
    """Per substrate: 54 brand pairs (shares above) + 3 THIN pairs (B1's answers: B1's domain is 'company' for
    THIN, so THIN's 10 classified domains are 2 company, 6 listing, 1 review, 1 editorial: K 0, P 20, Y 60, M 100)."""
    e = expected_synthetic()
    tot = {d: 9 * sum(e[i][d] for i in e) for d in C.DEF_ORDER}
    thin = {"K_own_domain": 0.0, "P_any_company": 20.0, "Y_own_plus_listings": 60.0, "M_not_owned": 100.0}
    return {d: (tot[d] + 3 * thin[d]) / 57.0 for d in C.DEF_ORDER}


def dry_run(out_dir, n_boot=200):
    answers, units, table = synthetic_world()
    res = run_all(answers, units, table, n_boot=n_boot, denon=("v19", "B6"))
    exp, checks = expected_synthetic(), []
    for s in ("v19", "v20"):
        for i, row in exp.items():
            got = res["primary"]["brands"][(s, f"B{i}")]
            for d, v in row.items():
                checks.append((f"{s}:B{i} {d}", abs(got[d] - v) < 1e-9, got[d], v))
    for s in ("v19", "v20"):
        checks.append((f"{s}:NONE absent", (s, "NONE") not in res["primary"]["brands"], None, None))
        thin = res["primary"]["brands"].get((s, "THIN"))
        checks.append((f"{s}:THIN not rated (g=3)", thin is not None and thin["g"] == 3 and not thin["rated"],
                       None, None))
    ag = res["primary"]["agreement"]
    checks.append(("rho_w(P,Y) = -1", abs(ag["P_any_company~Y_own_plus_listings"]["rho_w"] + 1) < 1e-12,
                   ag["P_any_company~Y_own_plus_listings"]["rho_w"], -1))
    checks.append(("rho_w(K,P) undefined (K constant)", ag["K_own_domain~P_any_company"]["rho_w"] is None, None, None))
    want = {"K_own_domain~P_any_company": 4 / 6, "K_own_domain~Y_own_plus_listings": 4 / 6,
            "K_own_domain~M_not_owned": 1.0, "P_any_company~Y_own_plus_listings": 4 / 6,
            "P_any_company~M_not_owned": 5 / 6, "Y_own_plus_listings~M_not_owned": 5 / 6}
    for p, v in want.items():
        checks.append((f"share_changed>25 {p}", abs(ag[p]["share_changed"] - v) < 1e-12, ag[p]["share_changed"], v))
    pw = res["primary"]["program"]["pair_weighted"]
    for d, v in expected_program_pair_weighted().items():
        checks.append((f"program pair-weighted {d}", abs(pw[d] - v) < 1e-9, pw[d], v))
    bw = res["primary"]["program"]["brand_weighted"]
    for d, v in {"K_own_domain": 10, "P_any_company": 45, "Y_own_plus_listings": 45, "M_not_owned": 90}.items():
        checks.append((f"program brand-weighted {d}", abs(bw[d] - v) < 1e-9, bw[d], v))
    for i in (1, 6):
        lo, hi, n = res["primary_ci"]["brand"][f"v19:B{i}|P_any_company"]
        checks.append((f"bootstrap CI degenerate v19:B{i} P", abs(lo - 10 * (1 + i)) < 1e-9 and abs(hi - lo) < 1e-9,
                       [lo, hi], 10 * (1 + i)))
    s3 = res["sensitivities"]["S1_unresolved_out"]["brands"][("v19", "B1")]
    checks.append(("S1 unresolved counted out: K = 100/11", abs(s3["K_own_domain"] - 100 / 11) < 1e-9,
                   s3["K_own_domain"], 100 / 11))
    checks.append(("S6 without B6", ("v19", "B6") not in res["sensitivities"]["S6_without_denon"]["brands"], None, None))
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "dry_run_results_v1_18.json").write_text(json.dumps(jsonable(res), indent=1) + "\n")
    lines = [f"v1.18 synthetic dry run ({datetime.now(timezone.utc).isoformat()}), bootstrap draws {n_boot}"]
    for name, ok, got, want_ in checks:
        lines.append(f"{'PASS' if ok else 'FAIL'}  {name}  got={got} expected={want_}")
    n_fail = sum(1 for c in checks if not c[1])
    lines.append(f"{len(checks) - n_fail}/{len(checks)} checks pass")
    (out_dir / "dry_run_v1_18.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[-3:]))
    return n_fail


def real_run(a):
    gate()
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
    res = run_all(ans, units, table, answers_sources=ans_src)
    res["inputs"] = {"t4": [a.t4, C.sha256_file(a.t4)], "n_answers": len(ans),
                     "domain_table": C.sha256_file(C.DOMAIN_TABLE)}
    out = C.PHASE / "outputs" / "v1_18_results.json"
    out.write_text(json.dumps(jsonable(res), indent=1) + "\n")
    print("written", out)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--synthetic", action="store_true")
    g.add_argument("--run", action="store_true")
    ap.add_argument("--t4")
    ap.add_argument("--coded")
    ap.add_argument("--n-boot", type=int, default=200)
    a = ap.parse_args(argv)
    if a.synthetic:
        return 1 if dry_run(C.PHASE / "outputs" / "dry_run", a.n_boot) else 0
    if not (a.t4 and a.coded):
        raise Refused("REFUSED: --run needs --t4 and --coded")
    return real_run(a)


if __name__ == "__main__":
    sys.exit(main())
