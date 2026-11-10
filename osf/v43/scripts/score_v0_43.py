#!/usr/bin/env python3
"""Scorer for AIAS v0.43 (PRE_REGISTRATION_v0_43.md s2.1-s2.8, s5). One run per stage:

  python3 score_v0_43.py --stage 1     -> osf/v43/v43_stage1_verdicts.json
  python3 score_v0_43.py --stage 2     -> osf/v43/v43_stage2_verdicts.json   (P_new via --pnew CSV)

rho_pw|Z: within each substrate Y, X and the controls are ranked (average ranks); rank(Y) and rank(X)
are OLS-residualised on an intercept and the control ranks; residuals are pooled; Pearson r.
Permutation p: X residuals shuffled within substrate. Bootstrap: units resampled within substrate,
ranks/residuals/rho recomputed. One numpy Generator per test (seeded as s2.1 assigns): permutation
draws first, then bootstrap draws.
"""
import argparse
import csv
import datetime as dt
import json
import os
import sys

import numpy as np
from scipy.stats import rankdata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trends_common_v0_43 as tc  # noqa: E402

SUBSTRATES = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
EPS = 1e-12
MIN_N, MIN_N_CONS = 60, 30


# ------------------------------------------------------------------ statistics core
def _resid(r, Z):
    """Residuals of r (B,n) on intercept + Z (list of (B,n) arrays)."""
    B, n = r.shape
    A = np.ones((B, n, 1 + len(Z)))
    for i, z in enumerate(Z):
        A[:, :, 1 + i] = z
    beta = np.linalg.pinv(A) @ r[:, :, None]
    return r - (A @ beta)[:, :, 0]


def _rank_rows(a):
    return rankdata(a, axis=1)


def stratum_resid(v, spec):
    """v: dict name -> (B,n) array (raw values); spec=(x,y,zs). Returns (ry, rx) (B,n)."""
    x, y, zs = spec
    Z = [_rank_rows(v[z]) for z in zs]
    return _resid(_rank_rows(v[y]), Z), _resid(_rank_rows(v[x]), Z)


def pearson_rows(a, b):
    a = a - a.mean(axis=1, keepdims=True)
    b = b - b.mean(axis=1, keepdims=True)
    den = np.sqrt((a * a).sum(axis=1) * (b * b).sum(axis=1))
    with np.errstate(invalid="ignore", divide="ignore"):
        return (a * b).sum(axis=1) / den


def rho_pw(strata, spec):
    """Pooled within-substrate partial Spearman for strata (list of dict name->1d array)."""
    ry, rx = [], []
    for v in strata:
        a, b = stratum_resid({k: np.asarray(x, float)[None, :] for k, x in v.items()}, spec)
        ry.append(a[0])
        rx.append(b[0])
    return float(pearson_rows(np.concatenate(ry)[None, :], np.concatenate(rx)[None, :])[0]), ry, rx


def perm_p(ry, rx, rho_obs, B, rng):
    """Permutation test: X residuals shuffled within substrate. Returns (p_one, p_two, rho_perm)."""
    dots = np.zeros(B)
    for a, b in zip(ry, rx):
        idx = np.argsort(rng.random((B, len(b))), axis=1)
        dots += (b[idx] * a[None, :]).sum(axis=1)
    ay = np.concatenate(ry)
    bx = np.concatenate(rx)
    ay = ay - ay.mean()
    bx = bx - bx.mean()
    den = np.sqrt((ay * ay).sum() * (bx * bx).sum())
    rp = dots / den if den > 0 else np.full(B, np.nan)
    p1 = (1 + np.sum(rp >= rho_obs - EPS)) / (B + 1)
    p2 = (1 + np.sum(np.abs(rp) >= abs(rho_obs) - EPS)) / (B + 1)
    return float(p1), float(p2), rp


def boot_rhos(strata, specs, B, rng):
    """Within-substrate bootstrap; ranks, residuals and rho recomputed on every resample.
    One shared resample for all specs. Returns array (len(specs), B)."""
    ry = [[] for _ in specs]
    rx = [[] for _ in specs]
    for v in strata:
        n = len(next(iter(v.values())))
        idx = rng.integers(0, n, size=(B, n))
        vb = {k: np.asarray(x, float)[idx] for k, x in v.items()}
        for i, sp in enumerate(specs):
            a, b = stratum_resid(vb, sp)
            ry[i].append(a)
            rx[i].append(b)
    return np.array([pearson_rows(np.concatenate(ry[i], axis=1), np.concatenate(rx[i], axis=1))
                     for i in range(len(specs))])


def verdict(rho, p_one, p_two, ci90_hi, n, min_n):
    """Verdict rule s2.1. REVERSED is a label added to the verdict."""
    if n is None or n < min_n or rho is None or (isinstance(rho, float) and np.isnan(rho)):
        return {"verdict": "UNDETERMINED", "labels": [], "reason": f"n={n} < {min_n}" if n is not None and n < min_n else "rho undefined"}
    if rho >= 0.15 and p_one < 0.05:
        v = "CONFIRMED"
    elif ci90_hi is not None and ci90_hi < 0.10:
        v = "FALSIFIED"
    elif rho > 0 and p_one < 0.10:
        v = "MARGINAL"
    else:
        v = "UNDETERMINED"
    labels = ["REVERSED"] if (rho < 0 and p_two < 0.05) else []
    return {"verdict": v, "labels": labels, "reason": None}


def run_stat(rows, spec, seed, B_perm=10000, B_boot=10000, rng=None, boot=True):
    """Test of spec=(x,y,zs) on rows (dicts with 'sub' and the variables); returns stats dict."""
    need = [spec[0], spec[1]] + list(spec[2])
    rows = [r for r in rows if all(r.get(k) is not None for k in need)]
    strata, per = [], {}
    for s in SUBSTRATES:
        rs = [r for r in rows if r["sub"] == s]
        per[s] = len(rs)
        if len(rs) >= 2:
            strata.append({k: np.array([r[k] for r in rs], float) for k in need})
    out = {"n": len(rows), "n_per_substrate": per, "seed": seed}
    if len(rows) < 3 or not strata:
        out.update(rho=None, p_one=None, p_two=None)
        return out
    rng = rng if rng is not None else np.random.default_rng(seed)
    rho, ry, rx = rho_pw(strata, spec)
    out["rho"] = rho
    if B_perm:
        p1, p2, _ = perm_p(ry, rx, rho, B_perm, rng)
        out["p_one"], out["p_two"] = p1, p2
    if boot and B_boot:
        br = boot_rhos(strata, [spec], B_boot, rng)[0]
        ok = br[~np.isnan(br)]
        out["boot_valid"] = int(len(ok))
        out["ci90"] = [float(np.percentile(ok, 5)), float(np.percentile(ok, 95))]
        out["ci95"] = [float(np.percentile(ok, 2.5)), float(np.percentile(ok, 97.5))]
    return out


# ------------------------------------------------------------------ data assembly
def read_json(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def f(x):
    return float(x) if x not in ("", None) else None


def load_stage_data(root, stage, raw_dir=None, allow_incomplete=False, pnew_path=None):
    v43 = os.path.join(root, "osf/v43")
    with open(os.path.join(v43, "registries/units_v0_43.csv"), newline="", encoding="utf-8") as fh:
        urows = list(csv.DictReader(fh))
    bundles = read_json(os.path.join(v43, "registries/bundles_v0_43.json"))["substrates"]
    raw_dir = raw_dir or os.path.join(v43, "data/trends_raw")
    prefix = "main" if stage == 1 else "stage2_"
    steps = [f"{prefix}{n}" for n in (1, 2, 3)]
    pulls, mc_weekly = [], {"requests": 0, "ok": 0, "missing": 0, "resent": 0}
    chain = {}
    for step in steps:
        per_sub, complete = {}, True
        for s in SUBSTRATES:
            sers = []
            for j in range(len(bundles[s]["main_bundles"])):
                fn = os.path.join(raw_dir, step, f"{s}_b{j}.json")
                if not os.path.exists(fn):
                    complete = False
                    sers.append(None)
                    continue
                rec = read_json(fn)
                mc_weekly["requests"] += 1
                mc_weekly["ok"] += rec["status"] == "ok"
                mc_weekly["missing"] += rec["status"] != "ok"
                mc_weekly["resent"] += rec["n_attempts"] - 1
                sers.append(tc.parse_timeseries(rec["attempts"][-1]["response"]) if rec["status"] == "ok" else None)
            per_sub[s] = tc.pull_stats(bundles[s]["main_bundles"], sers, stage)
            chain.setdefault(step, {})[s] = {"links_held": int(sum(per_sub[s]["links"])),
                                             "links": len(per_sub[s]["links"])}
        if not complete and not allow_incomplete:
            raise SystemExit(f"pull {step} is incomplete (use --allow-incomplete for tests)")
        if complete or allow_incomplete:
            pulls.append((step, per_sub))
    if not pulls:
        raise SystemExit("no pulls found")
    pnew = {}
    if pnew_path and os.path.exists(pnew_path):
        with open(pnew_path, newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                pnew[(r["substrate"], r["unit"])] = f(r["P_new"])
    terms_path = os.path.join(v43, "registries/terms_v0_43.json")
    kinds = {}
    share_topic = None
    if os.path.exists(terms_path):
        t = read_json(terms_path)
        kinds = {k: v["kind"] for k, v in t["chosen"].items()}
        share_topic = sum(1 for v in kinds.values() if v == "topic") / len(kinds) if kinds else None
    wave = "t2" if stage == 1 else "t3"
    rows, comb = [], {}
    for s in SUBSTRATES:
        comb[s] = tc.combine_pulls([pp[s]["units"] for _, pp in pulls])
    for r in urows:
        s, u = r["substrate"], r["unit"]
        c = comb[s].get(u, {})
        row = {"sub": s, "unit": u, "cell": r["cell"],
               "kind": kinds.get(f"{s}|{u}"),
               "Y": c.get("Y"), "Y_SA": c.get("Y_SA"), "M": c.get("M"), "Yp": c.get("Yp"),
               "L": c.get("L"), "L_end": c.get("L_end"), "Y_pulls": c.get("Y_pulls"),
               "P": f(r[f"P_{wave}"]), "Cs": f(r[f"C_star_{wave}"]), "pi": f(r[f"pi_hat_{wave}"]),
               "P_t1": f(r["P_t1"]), "P_t2": f(r["P_t2"]), "P_t3": f(r["P_t3"]),
               "P_new": pnew.get((s, u))}
        rows.append(row)
    return {"rows": rows, "steps": [s for s, _ in pulls], "mc_weekly": mc_weekly, "chain": chain,
            "share_topic": share_topic, "pnew_present": bool(pnew), "bundles": bundles}


# ------------------------------------------------------------------ test specifications
def test_specs(stage):
    if stage == 1:
        return [
            ("H_Pred_Presence", ("P", "Y", ["L"]), 430041, MIN_N, "presence"),
            ("H_Pred_Presence_SA", ("P", "Y_SA", ["L"]), 430042, MIN_N, "presence"),
            ("H_Pred_Presence_Momentum", ("P", "Y", ["L", "M"]), 430043, MIN_N, "presence"),
            ("H_Pred_Consistency", ("Cs", "Y", ["L", "P"]), 430044, MIN_N_CONS, "consistency"),
        ]
    return [
        ("H_Pred_Presence_Confirm", ("P", "Y", ["L"]), 430045, MIN_N, "presence"),
        ("H_Pred_Presence_Confirm_SA", ("P", "Y_SA", ["L"]), 430046, MIN_N, "presence"),
        ("H_Pred_Presence_NewPanel", ("P_new", "Y", ["L"]), 430047, MIN_N, "presence"),
        ("H_Pred_Consistency_Confirm", ("Cs", "Y", ["L", "P"]), 430048, MIN_N_CONS, "consistency"),
    ]


def pooled_spearman_pairs(rows, key_lists):
    """Mean over pairs of pooled within-substrate Spearman of per-pull Y (MC_PullReliability)."""
    k = len(key_lists[0]) if key_lists else 0
    res = []
    for a in range(k):
        for b in range(a + 1, k):
            rr = [{"sub": r["sub"], "ya": r["Y_pulls"][a], "yb": r["Y_pulls"][b]} for r in rows
                  if r["Y_pulls"] and r["Y_pulls"][a] is not None and r["Y_pulls"][b] is not None]
            if len(rr) < 3:
                continue
            st = [{"ya": np.array([r["ya"] for r in rr if r["sub"] == s], float),
                   "yb": np.array([r["yb"] for r in rr if r["sub"] == s], float)}
                  for s in SUBSTRATES if sum(1 for r in rr if r["sub"] == s) >= 3]
            res.append(rho_pw(st, ("ya", "yb", []))[0])
    return (float(np.mean(res)) if res else None), res


def score(root, stage, B_perm=10000, B_boot=10000, raw_dir=None, pnew_path=None, allow_incomplete=False):
    D = load_stage_data(root, stage, raw_dir, allow_incomplete, pnew_path)
    rows = D["rows"]
    out = {"stage": stage, "prereg": "PRE_REGISTRATION_v0_43.md (tag v0.43-prereg-r1)",
           "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
           "pulls_used": D["steps"], "B_perm": B_perm, "B_boot": B_boot}
    # --- manipulation checks (seed 430049)
    rng = np.random.default_rng(430049)
    conc = run_stat([dict(r, Lc=r["L"]) for r in rows], ("P", "Lc", []), 430049, B_perm, 0, rng, boot=False)
    conc_ok = bool(conc.get("rho") is not None and conc["rho"] >= 0.30 and conc.get("p_one", 1) < 0.05)
    rel, pairs = pooled_spearman_pairs(rows, [r["Y_pulls"] for r in rows if r["Y_pulls"]])
    rel_ok = bool(rel is not None and rel >= 0.70)
    share = D["share_topic"]
    mc = {"MC_Concurrent": dict(conc, pass_=conc_ok, rule="rho_pw(P, L) >= 0.30 and one-sided p < 0.05"),
          "MC_PullReliability": {"mean_pairwise_pooled_spearman": rel, "pairs": pairs, "pass_": rel_ok},
          "MC_Weekly": D["mc_weekly"],
          "MC_Terms": {"share_topic": share, "pass_": (share is not None and share >= 0.5)},
          "MC_Chain": D["chain"]}
    out["manipulation_checks"] = mc
    flags = []
    if not conc_ok:
        flags.append("criterion doubtful")
    if not rel_ok:
        flags.append("outcome unreliable")
    if share is not None and share < 0.5:
        flags.append("mostly plain search terms")
    out["flags"] = flags
    # --- tests
    tests, defined = {}, {}
    for s in SUBSTRATES:
        defined[s] = {"units": sum(1 for r in rows if r["sub"] == s),
                      "Y_defined": sum(1 for r in rows if r["sub"] == s and r["Y"] is not None)}
    out["outcome_defined_per_substrate"] = defined
    for name, spec, seed, min_n, fam in test_specs(stage):
        if name == "H_Pred_Presence_NewPanel" and not D["pnew_present"]:
            tests[name] = {"verdict": "UNDETERMINED", "labels": [], "flags": flags, "seed": seed,
                           "reason": "P_new input absent (v0.42 t4 scores not yet supplied)", "spec": spec_json(spec)}
            continue
        st = run_stat(rows, spec, seed, B_perm, B_boot)
        v = verdict(st.get("rho"), st.get("p_one"), st.get("p_two"),
                    st.get("ci90", [None, None])[1], st["n"], min_n)
        tests[name] = dict(st, **v, flags=flags, min_n=min_n, spec=spec_json(spec))
    out["tests"] = tests
    # --- descriptives (no verdicts; seed 430050)
    out["descriptives"] = descriptives(rows, stage, B_perm, B_boot)
    out["unit_table"] = [{k: r[k] for k in ("sub", "unit", "cell", "kind", "Y", "Y_SA", "Yp", "M", "L", "L_end",
                                          "P", "Cs", "pi", "P_t1", "P_new")} for r in rows]
    return out, D


def spec_json(spec):
    return {"x": spec[0], "y": spec[1], "controls": spec[2]}


def slim(st):
    return {k: st[k] for k in ("n", "n_per_substrate", "rho", "p_one", "p_two", "ci90", "ci95") if k in st}


def descriptives(rows, stage, B_perm, B_boot):
    rng = np.random.default_rng(430050)
    d = {}
    specs = test_specs(stage)
    # 1. every test per substrate
    d["per_substrate"] = {}
    for name, spec, _, _, _ in specs:
        d["per_substrate"][name] = {}
        for s in SUBSTRATES:
            rs = [r for r in rows if r["sub"] == s]
            d["per_substrate"][name][s] = slim(run_stat(rs, spec, 430050, B_perm, 0, rng, boot=False))
    # 2. Presence tests without the five defunct automotive brands (cell D)
    nd = [r for r in rows if not (r["sub"] == "v0.22" and r["cell"] == "D")]
    d["presence_without_defunct_automotive"] = {
        name: slim(run_stat(nd, spec, 430050, B_perm, B_boot, rng)) for name, spec, _, _, fam in specs if fam == "presence"}
    # 3. recall alone
    d["recall_alone"] = slim(run_stat(rows, ("pi", "Y", ["L"]), 430050, B_perm, B_boot, rng))
    # 4. topic-only units
    d["topic_only_primary"] = slim(run_stat([r for r in rows if r["kind"] == "topic"], specs[0][1], 430050, B_perm, B_boot, rng))
    if stage == 1:
        # 5. longer lead: P at t1
        d["longer_lead_P_t1"] = slim(run_stat(rows, ("P_t1", "Y", ["L"]), 430050, B_perm, B_boot, rng))
        # 6. cross-lagged comparison
        rr = [r for r in rows if None not in (r["P_t2"], r["P_t3"], r["L"], r["L_end"])]
        for r in rr:
            r["_a"] = r["P_t2"]
        sp_a = ("P_t2", "L_end", ["L"])      # AI -> search
        sp_b = ("L", "P_t3", ["P_t2"])       # search -> AI
        strata = []
        for s in SUBSTRATES:
            rs = [r for r in rr if r["sub"] == s]
            if len(rs) >= 2:
                strata.append({k: np.array([r[k] for r in rs], float) for k in ("P_t2", "P_t3", "L", "L_end")})
        if strata:
            ra, _, _ = rho_pw(strata, sp_a)
            rb, _, _ = rho_pw(strata, sp_b)
            br = boot_rhos(strata, [sp_a, sp_b], B_boot, rng) if B_boot else None
            e = {"n": len(rr), "rho_AI_to_search": ra, "rho_search_to_AI": rb, "difference": ra - rb}
            if br is not None:
                diff = br[0] - br[1]
                diff = diff[~np.isnan(diff)]
                e["difference_ci90"] = [float(np.percentile(diff, 5)), float(np.percentile(diff, 95))]
                e["difference_ci95"] = [float(np.percentile(diff, 2.5)), float(np.percentile(diff, 97.5))]
            d["cross_lagged"] = e
    return d


def monthly_series(root, bundles, out_csv):
    """Descriptive 7: each unit's weekly chained index for every stored monthly snapshot."""
    base = os.path.join(root, "osf/v43/data/trends_raw")
    if not os.path.isdir(base):
        return 0
    n = 0
    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["snapshot", "substrate", "unit", "week_start", "chained_index", "segment"])
        for step in sorted(x for x in os.listdir(base) if x.startswith("snapshot_")):
            for s in SUBSTRATES:
                bl = bundles[s]["main_bundles"]
                sers = []
                for j in range(len(bl)):
                    fn = os.path.join(base, step, f"{s}_b{j}.json")
                    rec = read_json(fn) if os.path.exists(fn) else None
                    sers.append(tc.parse_timeseries(rec["attempts"][-1]["response"]) if rec and rec["status"] == "ok" else None)
                info, _ = tc.chain_factors(bl, sers)
                seen = set()
                for b, ser, inf in zip(bl, sers, info):
                    if ser is None or inf is None:
                        continue
                    for i, u in enumerate(b):
                        if u in seen:
                            continue
                        seen.add(u)
                        for wk, val in sorted(ser.values[i].items()):
                            w.writerow([step, s, u, wk.isoformat(), repr(inf[1] * val), inf[0]])
                            n += 1
    return n


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", type=int, choices=[1, 2], required=True)
    ap.add_argument("--root", default=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../..")))
    ap.add_argument("--raw-dir", default=None)
    ap.add_argument("--pnew", default=None, help="CSV substrate,unit,P_new (v0.42 locked t4 scores)")
    ap.add_argument("--B-perm", type=int, default=10000)
    ap.add_argument("--B-boot", type=int, default=10000)
    ap.add_argument("--out", default=None)
    ap.add_argument("--allow-incomplete", action="store_true")
    a = ap.parse_args(argv)
    out, D = score(a.root, a.stage, a.B_perm, a.B_boot, a.raw_dir, a.pnew, a.allow_incomplete)
    path = a.out or os.path.join(a.root, f"osf/v43/v43_stage{a.stage}_verdicts.json")
    tc.dump_json(out, path)
    if a.stage == 2:
        n = monthly_series(a.root, D["bundles"], os.path.join(os.path.dirname(path), "v43_monthly_series.csv"))
        print(f"monthly series rows: {n}")
    for k, v in out["tests"].items():
        print(k, v["verdict"], v.get("labels"), v.get("rho"), v.get("p_one"), v.get("n"))
    print("flags:", out["flags"], "->", path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
