"""
analyze_v1_17.py -- AIAS(TM) methodology v1.17, "How many runs are enough". Transcribes PRE_REGISTRATION_v1_17.md
section 4 (estimands) and section 5 (outputs). The pre-registration prose is authoritative.

Modes
  --loader-check     counts per cell and the one published number (v0.42 descriptive 3: 49 brands below the
                     recall floor on N3, S0, three runs). Computes no estimand. Allowed before the lock.
  --synthetic OUT    the whole analysis on synthetic data with known run-to-run variance (dry run).
  --run              the analysis on the real inputs, ONCE. Refuses unless tag v1.17-prereg-r1 is on origin and
                     every input matches LOCK_MANIFEST_v1_17.sha256.
"""
import argparse
import json
import math
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v1_17_lib as L   # noqa: E402

PREREG_TAG = "v1.17-prereg-r1"
MANIFEST = L.V117 / "LOCK_MANIFEST_v1_17.sha256"
OUT_REAL = L.V117 / "outputs"


# =========================================================================== t4
def _strata(meta, coi_mask, bands):
    """Pre-registered strata. Returns (primary, alongside): {name: bool mask}."""
    size = meta.size
    primary = {"all": np.ones(len(size), bool)}
    for s in sorted(set(size.tolist())):
        primary[f"size_{s}"] = size == s
    along = {}
    for c in L.CONDS:
        along[f"cond_{c}"] = meta.cond == c
        for s in sorted(set(size.tolist())):
            along[f"size_{s}_cond_{c}"] = (size == s) & (meta.cond == c)
    for m in L.N3:
        along[f"model_{m}"] = meta.model == m
    for cat in L.CATEGORIES:
        along[f"category_{cat}"] = meta.cat == cat
    for b in L.BANDS:
        along[f"band_{b}"] = bands == b
        for s in sorted(set(size.tolist())):
            along[f"size_{s}_band_{b}"] = (size == s) & (bands == b)
    named = (bands != "zero") & (bands != "full")
    along["named_not_saturated"] = named
    for s in sorted(set(size.tolist())):
        along[f"size_{s}_named_not_saturated"] = named & (size == s)
    along["S_COI_all"] = ~coi_mask
    for s in sorted(set(size.tolist())):
        along[f"S_COI_size_{s}"] = (~coi_mask) & (size == s)
    return primary, along


def _coi_mask(cat, brand, coi_keys):
    return np.array([(c, b) in set(coi_keys) for c, b in zip(cat, brand)])


def analyse_t4(t4, coi_keys, n_boot=L.N_BOOT, seed=L.SEEDS["bootstrap"]):
    p = L.per_run(t4)
    s2 = L.unit_var(p)
    bands = L.bands_t4(t4)
    coi = _coi_mask(t4.cat, t4.brand, coi_keys)
    primary, along = _strata(t4, coi, bands)
    res = {"unit": "brand x model x search condition (per-run Presence = mentions / 6 frames)",
           "n_units": len(t4.units), "runs": len(L.RUNS), "frames": L.F,
           "primary": {k: L.projection_row(s2, m, t4.cluster, n_boot, seed) for k, m in primary.items()},
           "alongside": {k: L.projection_row(s2, m, t4.cluster, n_boot, seed) for k, m in along.items()}}
    # A-frame: per-question (frame) scale, the scale of Schulte et al.'s per-prompt figures
    xf = np.var(t4.X, axis=1, ddof=1)                    # [u, f]
    s2f = xf.reshape(-1)
    clf = np.repeat(t4.cluster, L.F)
    sizef = np.repeat(t4.size, L.F)
    res["alongside_frame_level"] = {"all": L.projection_row(s2f, np.ones(len(s2f), bool), clf, n_boot, seed)}
    for s in sorted(set(t4.size.tolist())):
        res["alongside_frame_level"][f"size_{s}"] = L.projection_row(s2f, sizef == s, clf, n_boot, seed)
    # A-panel: the N3 panel mean of the three models (the brand table's pi_N3_<cond>)
    pk = sorted({(c, b, d) for c, b, d in zip(t4.cat, t4.brand, t4.cond)})
    P = np.array([p[(t4.cat == c) & (t4.brand == b) & (t4.cond == d)].mean(axis=0) for c, b, d in pk])
    s2p = L.unit_var(P)
    clp = np.array([f"{c}|{d}" for c, b, d in pk])
    sizep = np.array([int(t4.size[t4.cat == c][0]) for c, b, d in pk])
    res["alongside_panel_N3"] = {"all": L.projection_row(s2p, np.ones(len(pk), bool), clp, n_boot, seed)}
    for s in sorted(set(sizep.tolist())):
        res["alongside_panel_N3"][f"size_{s}"] = L.projection_row(s2p, sizep == s, clp, n_boot, seed)
    # E3: per-unit standard errors (each from three runs, two degrees of freedom: descriptive only)
    se3 = np.sqrt(s2 / 3)
    res["per_unit_se"] = {
        "n_units": len(s2),
        "se3_below_0.10": int((se3 < 0.10).sum()), "se3_below_0.05": int((se3 < 0.05).sum()),
        "se1_below_0.10": int((np.sqrt(s2) < 0.10).sum()), "se1_below_0.05": int((np.sqrt(s2) < 0.05).sum()),
        "units_zero_variance": int((s2 == 0).sum()),
        "band_counts": {b: int((bands == b).sum()) for b in L.BANDS}}
    res["once_vs_three"] = once_vs_three(t4)
    return res


def once_vs_three(t4):
    """E5: what changes if each brand were measured once instead of three times (integer counts throughout)."""
    K = t4.X.sum(axis=2).astype(int)          # [u, r] mentions per run
    out = {}
    # unit level: category x model x condition cells
    for label, ref_kind in (("vs_three_run_mean", "all"), ("vs_other_two_runs_alongside", "other")):
        tot = {"brand_runs": 0, "brands_changing_place": 0, "discordant_pairs": 0, "pairs": 0}
        for cell in sorted(set(t4.cluster.tolist())):
            idx = t4.cluster == cell
            for ri in range(len(L.RUNS)):
                single = K[idx, ri]
                ref = K[idx].sum(axis=1) if ref_kind == "all" else K[idx].sum(axis=1) - K[idx, ri]
                nb, nd, npairs = L.discordance(single, ref)
                tot["brand_runs"] += int(idx.sum()); tot["brands_changing_place"] += nb
                tot["discordant_pairs"] += nd; tot["pairs"] += npairs
        tot["share_brands_changing_place"] = tot["brands_changing_place"] / tot["brand_runs"]
        tot["share_pairs_reversed"] = tot["discordant_pairs"] / tot["pairs"]
        out[f"unit_level_{label}"] = tot
    # panel level (N3) and the published floor, per category x condition
    pk = sorted({(c, b, d) for c, b, d in zip(t4.cat, t4.brand, t4.cond)})
    KP = np.array([K[(t4.cat == c) & (t4.brand == b) & (t4.cond == d)].sum(axis=0) for c, b, d in pk])  # [brand, r]
    n_models = len(L.N3)
    for label, ref_kind in (("vs_three_run_mean", "all"), ("vs_other_two_runs_alongside", "other")):
        tot = {"brand_runs": 0, "brands_changing_place": 0, "discordant_pairs": 0, "pairs": 0}
        for c in L.CATEGORIES:
            for d in L.CONDS:
                idx = np.array([k[0] == c and k[2] == d for k in pk])
                for ri in range(len(L.RUNS)):
                    single = KP[idx, ri]
                    ref = KP[idx].sum(axis=1) if ref_kind == "all" else KP[idx].sum(axis=1) - KP[idx, ri]
                    nb, nd, npairs = L.discordance(single, ref)
                    tot["brand_runs"] += int(idx.sum()); tot["brands_changing_place"] += nb
                    tot["discordant_pairs"] += nd; tot["pairs"] += npairs
        tot["share_brands_changing_place"] = tot["brands_changing_place"] / tot["brand_runs"]
        tot["share_pairs_reversed"] = tot["discordant_pairs"] / tot["pairs"]
        out[f"panel_N3_{label}"] = tot
    floor = {}
    for d in L.CONDS:
        idx = np.array([k[2] == d for k in pk])
        three = np.array([L.below_floor(int(x), n_models * L.F * len(L.RUNS)) for x in KP[idx].sum(axis=1)])
        per = []
        for ri in range(len(L.RUNS)):
            one = np.array([L.below_floor(int(x), n_models * L.F) for x in KP[idx, ri]])
            per.append({"run": L.RUNS[ri], "below_floor_one_run": int(one.sum()),
                        "brands_crossing": int((one != three).sum()),
                        "below_three_above_one": int((three & ~one).sum()),
                        "above_three_below_one": int((~three & one).sum())})
        floor[d] = {"n_brands": int(idx.sum()), "below_floor_three_runs": int(three.sum()), "per_run": per,
                    "mean_brands_crossing": float(np.mean([x["brands_crossing"] for x in per]))}
    out["published_floor_N3"] = floor
    # unit level: named at all over three runs but not in a single run
    tot3 = K.sum(axis=1)
    out["unit_named_three_runs_not_in_one"] = {
        "units_named_in_three_runs": int((tot3 > 0).sum()),
        "per_run_missed": [int(((tot3 > 0) & (K[:, ri] == 0)).sum()) for ri in range(len(L.RUNS))]}
    return out


# =========================================================================== omnibus
def analyse_omni(o, coi_keys, n_boot=L.N_BOOT, seed=L.SEEDS["bootstrap"]):
    s2 = L.unit_var(o.W)
    tot = np.rint(o.W * L.F).sum(axis=1).astype(int)
    bands = np.array([L.band_of(int(k), L.F * len(L.WAVES)) for k in tot])
    coi = _coi_mask(o.cat, o.brand, coi_keys)
    res = {"unit": "brand x legacy model (one run per wave; waves t1 May 20-26, t2 Jun 10, t3 Nov 9, 2026)",
           "note": "time drift plus run noise, legacy six models; never pooled with t4; no runs projection",
           "n_units": len(o.units), "strata": {}}
    masks = {"all": np.ones(len(s2), bool)}
    for s in sorted(set(o.size.tolist())):
        masks[f"size_{s}"] = o.size == s
    for b in L.BANDS:
        masks[f"band_{b}"] = bands == b
    masks["S_COI_all"] = ~coi
    for k, m in masks.items():
        row = L.projection_row(s2, m, o.cluster, n_boot, seed)
        row = {kk: vv for kk, vv in row.items() if not kk.startswith("R_needed") and kk != "se_at_R"}
        res["strata"][k] = row
    gaps = {}
    for (a, b), name in (((0, 1), "t1_t2"), ((1, 2), "t2_t3"), ((0, 2), "t1_t3")):
        d2 = (o.W[:, b] - o.W[:, a]) ** 2 / 2
        gaps[name] = {"all": float(d2.mean())}
        for s in sorted(set(o.size.tolist())):
            gaps[name][f"size_{s}"] = float(d2[o.size == s].mean())
    res["half_mean_squared_change"] = gaps
    res["band_counts"] = {b: int((bands == b).sum()) for b in L.BANDS}
    return res


# =========================================================================== synthetic
def make_synthetic(seed, scenario="A", n_runs=3):
    """t4-shaped data with KNOWN run-to-run variance. Each (unit, frame) has a mention probability pi; runs are
    independent. Scenario A: every call independent. Scenario B: within each call (category, model, condition,
    run, frame) a shared 'short answer' shock (probability 0.3) halves every brand's chance, so brands named in the
    same answer are dependent; the per-unit truth stays analytic because the marginal chance is pi * (1 - 0.15).
    True per-run variance of a unit: sum_f pi'_f (1 - pi'_f) / 36."""
    rng = np.random.default_rng(seed)
    sizes = {"v0.19": 16, "v0.20": 24, "v0.21": 24, "v0.22": 24, "v0.23": 24}
    units, pis = [], []
    for cat, n in sizes.items():
        for bi in range(n):
            base = 0.0 if rng.random() < 0.25 else rng.beta(1.2, 1.5)
            for m in L.N3:
                for c in L.CONDS:
                    if base == 0.0:
                        pf = np.zeros(L.F)
                    else:
                        lg = math.log(base / (1 - base + 1e-9) + 1e-9) + rng.normal(0, 0.8, L.F)
                        pf = 1 / (1 + np.exp(-lg))
                    units.append((cat, f"B{bi:02d}", m, c))
                    pis.append(pf)
    pis = np.array(pis)                                   # [u, f]
    U = len(units)
    if scenario == "A":
        X = (rng.random((U, n_runs, L.F)) < pis[:, None, :]).astype(float)
        eff = pis
    else:
        cells = sorted({(u[0], u[2], u[3]) for u in units})
        cid = {c: i for i, c in enumerate(cells)}
        uc = np.array([cid[(u[0], u[2], u[3])] for u in units])
        shock = rng.random((len(cells), n_runs, L.F)) < 0.3
        mult = np.where(shock, 0.5, 1.0)[uc]               # [u, r, f]
        X = (rng.random((U, n_runs, L.F)) < pis[:, None, :] * mult).astype(float)
        eff = pis * (1 - 0.3 * 0.5)
    t = L.T4(X, units, {c: [f"f{i}" for i in range(L.F)] for c in sizes})
    true_unit_var = (eff * (1 - eff)).sum(axis=1) / L.F ** 2
    truth = {"all": float(true_unit_var.mean())}
    for s in (16, 24):
        truth[f"size_{s}"] = float(true_unit_var[t.size == s].mean())
    return t, truth


def make_synthetic_omni(seed):
    """Omnibus-shaped synthetic data (112 brands x 6 legacy models x 3 waves, one run per wave) with drift."""
    rng = np.random.default_rng(seed + 5)
    sizes = {"v0.19": 16, "v0.20": 24, "v0.21": 24, "v0.22": 24, "v0.23": 24}
    units, W = [], []
    for cat, n in sizes.items():
        for bi in range(n):
            base = 0.0 if rng.random() < 0.25 else rng.beta(1.2, 1.5)
            for m in L.L6:
                pis = np.clip(base + rng.normal(0, 0.1, len(L.WAVES)), 0, 1) if base > 0 else np.zeros(len(L.WAVES))
                units.append((cat, f"B{bi:02d}", m))
                W.append(rng.binomial(L.F, pis) / L.F)
    return L.Omni(np.array(W), units)


def dry_run(out_dir, seed=L.SEEDS["dry_run"], n_rep=300, n_boot_rep=1000):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    report = {"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "seed": seed,
              "scenarios": {}}
    for sc in ("A", "B"):
        t, truth = make_synthetic(seed, sc)
        res = analyse_t4(t, coi_keys=(), n_boot=L.N_BOOT)
        cmp = {}
        for k in ("all", "size_16", "size_24"):
            row = res["primary"][k]
            cmp[k] = {"true_var": truth[k], "est_var": row["pooled_var"],
                      "true_sd": math.sqrt(truth[k]), "est_sd": row["sd_one_run"],
                      "ci95_cluster": row["var_ci95_cluster_bootstrap"],
                      "covers_truth": row["var_ci95_cluster_bootstrap"][0] <= truth[k] <= row["var_ci95_cluster_bootstrap"][1]}
            for tau in L.TAUS:
                cmp[k][f"R_true_{tau:.2f}"] = L.runs_needed(truth[k], tau)
                cmp[k][f"R_est_{tau:.2f}"] = row[f"R_needed_se_below_{tau:.2f}"]
        # coverage over replicates
        cov = {k: {"cluster": 0, "chi2": 0, "R10_exact": 0, "R05_exact": 0, "rel_bias_sum": 0.0}
               for k in ("all", "size_16", "size_24")}
        for i in range(n_rep):
            t2, tr2 = make_synthetic(L.SEEDS["coverage"] + 1000 * (sc == "B") + i, sc)
            s2 = L.unit_var(L.per_run(t2))
            for k in cov:
                m = np.ones(len(s2), bool) if k == "all" else t2.size == int(k.split("_")[1])
                v = L.pooled_var(s2, m)
                lo, hi, _, _ = L.cluster_bootstrap_var(s2[m], t2.cluster[m], n_boot_rep, L.SEEDS["bootstrap"] + i)
                clo, chi = L.chi2_interval(v, int(m.sum()))
                cov[k]["cluster"] += lo <= tr2[k] <= hi
                cov[k]["chi2"] += clo <= tr2[k] <= chi
                cov[k]["R10_exact"] += L.runs_needed(v, 0.10) == L.runs_needed(tr2[k], 0.10)
                cov[k]["R05_exact"] += L.runs_needed(v, 0.05) == L.runs_needed(tr2[k], 0.05)
                cov[k]["rel_bias_sum"] += (v - tr2[k]) / tr2[k]
        for k in cov:
            cov[k] = {"replicates": n_rep, "bootstrap_draws_each": n_boot_rep,
                      "coverage_cluster_bootstrap": cov[k]["cluster"] / n_rep,
                      "coverage_chi2_alongside": cov[k]["chi2"] / n_rep,
                      "R_0.10_exact_share": cov[k]["R10_exact"] / n_rep,
                      "R_0.05_exact_share": cov[k]["R05_exact"] / n_rep,
                      "mean_relative_bias_var": cov[k]["rel_bias_sum"] / n_rep}
        report["scenarios"][sc] = {"one_dataset": cmp, "coverage": cov,
                                   "once_vs_three": res["once_vs_three"]}
        om = analyse_omni(make_synthetic_omni(seed), coi_keys=(), n_boot=L.N_BOOT)
        with open(out_dir / f"synthetic_results_{sc}.json", "w") as fh:
            json.dump({"synthetic": True, "scenario": sc, "t4": res, "omnibus": om}, fh, indent=1)
    with open(out_dir / "dry_run_v1_17.json", "w") as fh:
        json.dump(report, fh, indent=1)
    return report


# =========================================================================== gates and main
def tag_on_origin(tag=PREREG_TAG):
    r = subprocess.run(["git", "-C", str(L.ROOT), "ls-remote", "--tags", "origin", f"refs/tags/{tag}"],
                       capture_output=True, text=True, timeout=60)
    return r.returncode == 0 and tag in r.stdout


def manifest_problems(path=MANIFEST):
    if not Path(path).exists():
        return [f"missing {path}"]
    bad = []
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        digest, rel = line.split(None, 1)
        f = L.ROOT / rel
        if not f.exists():
            bad.append(f"missing {rel}")
        elif L.sha256(f) != digest:
            bad.append(f"changed {rel}")
    return bad


def loader_check():
    t4 = L.load_t4()
    o = L.load_omni()
    coi = L.coi_brand_keys()
    cells = {}
    for cat in L.CATEGORIES:
        for m in L.N3:
            for c in L.CONDS:
                idx = (t4.cat == cat) & (t4.model == m) & (t4.cond == c)
                cells[f"{cat}|{m}|{c}"] = {"units": int(idx.sum()), "runs": len(L.RUNS), "frames": L.F}
    sizes = {cat: int(t4.size[t4.cat == cat][0]) for cat in L.CATEGORIES}
    with open(L.T4_VERDICTS, encoding="utf-8") as fh:
        published = json.load(fh)["descriptives"]["3_floor_persistence"]["below_floor_t4"]
    mine = L.published_floor_count(t4, "S0")
    out = {"t4_rows": t4.n_rows, "t4_units": len(t4.units), "t4_cells": cells, "category_sizes": sizes,
           "omnibus_units": len(o.units), "omnibus_waves": list(L.WAVES),
           "omnibus_units_per_size": {str(s): int((o.size == s).sum()) for s in sorted(set(o.size.tolist()))},
           "omnibus_table_pi_hat_max_abs_diff": o.max_pi_hat_abs_diff,
           "coi_keys": coi, "coi_present_t4": sum(1 for k in coi if any((t4.cat == k[0]) & (t4.brand == k[1]))),
           "published_below_floor_t4_S0": published, "reproduced_below_floor_t4_S0": mine,
           "loader_check_passed": published == mine}
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--loader-check", action="store_true")
    g.add_argument("--synthetic", metavar="OUT")
    g.add_argument("--run", action="store_true")
    a = ap.parse_args(argv)
    if a.loader_check:
        print(json.dumps(loader_check(), indent=1))
        return 0
    if a.synthetic:
        rep = dry_run(a.synthetic)
        print(json.dumps({k: v["one_dataset"] for k, v in rep["scenarios"].items()}, indent=1))
        return 0
    if not tag_on_origin():
        print(f"REFUSED: tag {PREREG_TAG} is not on origin (the lock is not anchored)")
        return 2
    bad = manifest_problems()
    if bad:
        print("REFUSED: inputs differ from LOCK_MANIFEST_v1_17.sha256: " + "; ".join(bad))
        return 3
    t4, o, coi = L.load_t4(), L.load_omni(), L.coi_brand_keys()
    out = {"study": "v1.17", "prereg_tag": PREREG_TAG, "generated_utc":
           datetime.now(timezone.utc).isoformat(timespec="seconds"), "seed_bootstrap": L.SEEDS["bootstrap"],
           "bootstrap_draws": L.N_BOOT, "loader_check": loader_check(),
           "t4": analyse_t4(t4, coi), "omnibus": analyse_omni(o, coi)}
    OUT_REAL.mkdir(parents=True, exist_ok=True)
    with open(OUT_REAL / "v1_17_results.json", "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print(f"wrote {OUT_REAL / 'v1_17_results.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
