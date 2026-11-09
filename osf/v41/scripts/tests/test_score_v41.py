#!/usr/bin/env python3
"""
test_score_v41.py — pre-lock tests for score_v41.py (no API calls; no repo writes).

  A. unit: kernel identity, statistics helpers, every verdict branch of every
     hypothesis on constructed data, and HALT-before-t3 on each parity gate failure.
  B. end-to-end: synthetic t3 waves (make_synthetic_t3.py) through the real
     extraction path, with known answers.

Usage: AIAS_ROOT=<tree> python3 osf/v41/scripts/tests/test_score_v41.py [--unit-only] [--scratch DIR]
Writes a results summary to <scratch>/test_results_v41.json.
"""
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent


def _shim():
    root = Path(os.environ.get("AIAS_ROOT", str(Path.home() / "aias"))).resolve()
    try:
        same = (Path.home() / "aias").resolve() == root
    except OSError:
        same = False
    if same:
        return root
    if os.environ.get("_V41_HOME_SHIM"):
        sys.exit("shim failed")
    import site
    shim = Path(tempfile.mkdtemp(prefix="v41_home_"))
    (shim / "aias").symlink_to(root)
    env = dict(os.environ, HOME=str(shim), _V41_HOME_SHIM="1", AIAS_ROOT=str(root))
    env.setdefault("PYTHONUSERBASE", site.getuserbase())
    os.execve(sys.executable, [sys.executable, str(Path(__file__).resolve())] + sys.argv[1:], env)


ROOT = _shim()
sys.path.insert(0, str(SCRIPTS))

import argparse      # noqa: E402
import copy          # noqa: E402
import csv           # noqa: E402
import json          # noqa: E402
import shutil        # noqa: E402
import subprocess    # noqa: E402
import time          # noqa: E402

import numpy as np   # noqa: E402
from scipy import stats  # noqa: E402

import score_v41 as S  # noqa: E402

RESULTS = []


def check(name, cond, detail=""):
    RESULTS.append({"test": name, "passed": bool(cond), "detail": detail})
    print(("  ok    " if cond else "  FAIL  ") + name + (f"  [{detail}]" if detail else ""))


# --------------------------------------------------------------------------- #
# constructed waves
# --------------------------------------------------------------------------- #
def mk(phi=None, pi=0.5, J=0.5, cp=6):
    return {"k": [], "pi_hat": pi, "phi": phi, "phi_partition": "defined" if phi is not None else "zero",
            "J": J, "J_n_models": 6, "C_P": cp, "cv_cpc": None, "phantom": False, "cell": ""}


def waves_from(arrays, n_per=20):
    """arrays: list of dicts key->np.array(len 5*n_per); returns list of wave dicts."""
    out = []
    for arr in arrays:
        w = {}
        for si, s in enumerate(S.OMNI):
            w[s] = {}
            for i in range(n_per):
                j = si * n_per + i
                w[s][f"B{i:02d}"] = mk(phi=float(arr["phi"][j]) if arr["phi"][j] is not None else None,
                                       pi=float(arr["pi"][j]))
        out.append(w)
    return out


def unit_tests():
    print("A. unit tests")
    rng = np.random.default_rng(7)

    # kernel / helpers -------------------------------------------------------
    vecs = [list(rng.integers(0, 7, 6)) for _ in range(300)] + [[0] * 6, [6] * 6]
    check("phi_m == phi_of on 6-model vectors", all(S.phi_m(v) == S.phi_of(v) for v in vecs))
    k5 = [3, 1, 4, 1, 5]
    pi = sum(k5) / 30
    manual = sum((x - 6 * pi) ** 2 for x in k5) / (6 * pi * (1 - pi)) / 4
    check("phi_m on a 5-model panel = locked formula with M'=5", abs(S.phi_m(k5)[0] - manual) < 1e-12)
    sim = [S.phi_m(list(rng.binomial(6, 0.4, 5)))[0] for _ in range(4000)]
    check("phi_m E[phi] ~ 1 under homogeneity (M'=5)", abs(np.mean([x for x in sim if x is not None]) - 1) < 0.06,
          f"mean={np.mean([x for x in sim if x is not None]):.3f}")
    x, y = rng.normal(size=60), rng.normal(size=60)
    check("spearman == scipy.spearmanr", abs(S.spearman(x, y) - stats.spearmanr(x, y)[0]) < 1e-12)
    g = np.repeat(S.OMNI, 12)
    check("perm_p (identical vectors) < 0.001", S.perm_p(x, x, ["a"] * 60, 1.0, 1, "one", 2000) < 0.001)
    p_null = [S.perm_p(rng.normal(size=40), rng.normal(size=40), ["a"] * 40,
                       S.spearman(*(rng.normal(size=(2, 40)))), 3, "one", 300) for _ in range(5)]
    check("perm_p returns (0,1]", all(0 < p <= 1 for p in p_null))
    w = S.within_ranks([5, 1, 3, 9, 2], ["a", "a", "a", "b", "b"])
    check("within_ranks ranks inside each substrate", list(w) == [3, 1, 2, 2, 1])

    # H_Phi_LongHorizon branches --------------------------------------------
    n = 100
    base = rng.normal(size=n)
    seen = set()
    for noise in (0.1, 0.5, 1.0, 1.5, 2.0, 3.0, 6.0):
        y = base + noise * rng.normal(size=n)
        w2, w3 = waves_from([{"phi": base, "pi": np.full(n, .5)}, {"phi": y, "pi": np.full(n, .5)}])
        r = S.h_phi_long(w2, w3)
        rho, p = r["rho"], r["p_perm"]
        want = ("CONFIRMED" if rho >= .5 and p < .05 else "FALSIFIED" if (rho < .3 or p >= .05) else "MARGINAL")
        check(f"H_Phi rule holds (noise {noise}: rho={rho:.2f}, p={p:.4f})", r["verdict"] == want, r["verdict"])
        seen.add(r["verdict"])
    check("H_Phi reaches CONFIRMED, MARGINAL and FALSIFIED", {"CONFIRMED", "MARGINAL", "FALSIFIED"} <= seen,
          str(sorted(seen)))
    y = base + 0.5 * rng.normal(size=n)
    w2, w3 = waves_from([{"phi": base, "pi": np.full(n, .5)}, {"phi": y, "pi": np.full(n, .5)}])
    r = S.h_phi_long(w2, w3, frame_null={"p_frame": 0.30})
    check("H_Phi high rho that does not beat the frame null -> MARGINAL", r["verdict"] == "MARGINAL",
          f"rho={r['rho']:.2f}")
    r = S.h_phi_long(w2, w3, frame_null={"p_frame": 0.001})
    check("H_Phi high rho beating the frame null -> CONFIRMED", r["verdict"] == "CONFIRMED")
    w2, w3 = waves_from([{"phi": base[:35], "pi": np.full(35, .5)}, {"phi": base[:35], "pi": np.full(35, .5)}], n_per=7)
    check("H_Phi n < 40 -> UNDETERMINED", S.h_phi_long(w2, w3)["verdict"] == "UNDETERMINED")
    k = {"phi": np.array([None] * n, dtype=object), "pi": np.full(n, .5)}
    check("H_Phi no defined pairs -> UNDETERMINED", S.h_phi_long(*waves_from([k, k]))["verdict"] == "UNDETERMINED")

    # H_Presence_LongHorizon branches ---------------------------------------
    def pres_case(patterns):
        a, b = [], []
        for pat in patterns:
            v = np.arange(20, dtype=float) / 20
            a.append(v)
            if pat == "same":
                b.append(v)
            elif pat == "rev":
                b.append(v[::-1])
            else:                                   # moderate: ~0.6
                vv = v.copy()
                vv[:8] = vv[:8][::-1]
                b.append(vv)
        a, b = np.concatenate(a), np.concatenate(b)
        w2, w3 = waves_from([{"phi": np.full(100, 1.0), "pi": a}, {"phi": np.full(100, 1.0), "pi": b}])
        return S.h_presence_long(w2, w3)
    check("H_Presence 5/5 identical -> CONFIRMED", pres_case(["same"] * 5)["verdict"] == "CONFIRMED")
    check("H_Presence 4/5 identical -> CONFIRMED", pres_case(["same"] * 4 + ["rev"])["verdict"] == "CONFIRMED")
    check("H_Presence 3/5 reversed -> FALSIFIED", pres_case(["rev"] * 3 + ["same"] * 2)["verdict"] == "FALSIFIED")
    r = pres_case(["same"] * 2 + ["rev"] * 2 + ["mod"])
    check("H_Presence 2 same / 2 rev / 1 moderate -> MARGINAL", r["verdict"] == "MARGINAL",
          f"mod rho={r['per_substrate']['v0.23']['rho']:.2f}")

    # H_Drift_Dissociation branches -----------------------------------------
    seen = set()
    for mix in (0.0, 0.3, 0.45, 0.6, 1.0):
        phi2 = np.tile(np.arange(20, dtype=float), 5)
        # t2 Presence ordering independent of t2 phi (shared-baseline coupling ~ 0)
        pi2 = np.concatenate([rng.permutation(20) for _ in range(5)]).astype(float) / 40 + .1
        perm = np.concatenate([rng.permutation(20) for _ in range(5)]).astype(float)
        other = np.concatenate([rng.permutation(20) for _ in range(5)]).astype(float)
        phi3 = perm
        pi3 = (mix * perm + (1 - mix) * other) / 40 + .1
        w2, w3 = waves_from([{"phi": phi2, "pi": pi2}, {"phi": phi3, "pi": pi3}])
        r = S.h_drift(w2, w3)
        rho, p = r["rho"], r["p_perm_two_sided"]
        want = ("CONFIRMED" if abs(rho) <= .3 else "FALSIFIED" if (abs(rho) >= .5 and p < .05) else "MARGINAL")
        check(f"H_Drift rule holds (mix {mix}: rho={rho:.2f})", r["verdict"] == want, r["verdict"])
        seen.add(r["verdict"])
    c2 = np.tile(np.arange(20, dtype=float), 5)
    p3 = np.concatenate([rng.permutation(20) for _ in range(5)]).astype(float)
    r = S.h_drift(*waves_from([{"phi": c2, "pi": c2 / 40 + .1}, {"phi": p3, "pi": p3 / 40 + .1}]))
    check("H_Drift components moving together -> FALSIFIED", r["verdict"] == "FALSIFIED", f"rho={r['rho']:.2f}")
    seen.add(r["verdict"])
    check("H_Drift reaches CONFIRMED, MARGINAL and FALSIFIED", {"CONFIRMED", "MARGINAL", "FALSIFIED"} <= seen,
          str(sorted(seen)))
    c2 = np.tile(np.arange(20, dtype=float), 5)
    p3 = np.concatenate([rng.permutation(20) for _ in range(5)]).astype(float)
    o3 = np.concatenate([rng.permutation(20) for _ in range(5)]).astype(float)
    r = S.h_drift(*waves_from([{"phi": c2, "pi": c2 / 40 + .1}, {"phi": p3, "pi": o3 / 40 + .1}]))
    check("H_Drift reports t2 baseline coupling (= 1 when t2 orders coincide)",
          abs(r["baseline_coupling_t2_rho"] - 1) < 1e-12,
          f"independent t3 moves still give delta rho={r['rho']:.2f}")
    w2, w3 = waves_from([{"phi": phi2, "pi": pi2}, {"phi": phi2 + 1, "pi": pi2}])
    check("H_Drift no change -> UNDETERMINED (degenerate)", S.h_drift(w2, w3)["verdict"] == "UNDETERMINED")

    # H_Horizon_Decay branches ----------------------------------------------
    v = rng.normal(size=n)
    noisy = v + 1.0 * rng.normal(size=n)
    piv = np.tile(np.linspace(.05, .95, 20), 5)
    pin = np.clip(piv + .25 * rng.normal(size=n), .01, .99)
    w1, w2, w3 = waves_from([{"phi": v, "pi": piv}, {"phi": v, "pi": piv}, {"phi": noisy, "pi": pin}])
    r = S.h_horizon_decay(w1, w2, w3)
    check("H_Decay t3 noisier -> CONFIRMED (phi)", r["phi"]["verdict"] == "CONFIRMED", str(r["phi"].get("ci95")))
    check("H_Decay t3 noisier -> CONFIRMED (pi_hat)", r["pi_hat"]["verdict"] == "CONFIRMED", str(r["pi_hat"].get("ci95")))
    w1, w2, w3 = waves_from([{"phi": v, "pi": piv}, {"phi": noisy, "pi": pin}, {"phi": v, "pi": piv}])
    r = S.h_horizon_decay(w1, w2, w3)
    check("H_Decay t2 noisier -> FALSIFIED (phi)", r["phi"]["verdict"] == "FALSIFIED", str(r["phi"].get("ci95")))
    check("H_Decay t2 noisier -> FALSIFIED (pi_hat)", r["pi_hat"]["verdict"] == "FALSIFIED")
    w1, w2, w3 = waves_from([{"phi": v, "pi": piv}] * 3)
    r = S.h_horizon_decay(w1, w2, w3)
    check("H_Decay identical waves -> MARGINAL (CI = [0,0])", r["phi"]["verdict"] == "MARGINAL"
          and r["phi"]["ci95"] == [0.0, 0.0])
    check("H_Decay reports the 4-instrument horizon table",
          set(r["reported_alongside"]) == {"phi", "pi_hat", "J", "C_P"})

    # parity gates halt BEFORE any t3 file is read ---------------------------
    loaded = []
    real_load = S.load_wave

    def spy(lay):
        loaded.append(str(lay["base"]))
        return real_load(lay)
    S.load_wave = spy
    t1, t2 = real_load(S.LAYOUT["t1"]), real_load(S.LAYOUT["t2"])
    ref_rows = list(csv.DictReader(open(S.REF_DIR / "v1_8_instrument_table.csv", newline="")))
    ref_v = json.load(open(S.REF_DIR / "v1_8_verdicts.json"))
    v34 = json.load(open(S.V34_VERDICTS))
    gates, _, _ = S.run_gates(t1, t2, ref_rows, ref_v, v34)
    check("gates pass on the real frozen inputs", gates["all_passed"])
    fake_t3 = {"base": Path("/nonexistent/t3"), "v23": Path("/nonexistent/t3/v23")}

    def expect_halt(label, **inj):
        loaded.clear()
        args = dict(t1=t1, t2=t2, ref_rows=ref_rows, ref_verdicts=ref_v, v34=v34)
        args.update(inj)
        try:
            g, _, _ = S.run_gates(**args)
            S.score(fake_t3, t1, t2, g)
            check(f"{label}: halts", False, "no GateFailure")
        except S.GateFailure:
            check(f"{label}: halts before t3", not any("nonexistent" in x for x in loaded))
    bad = copy.deepcopy(ref_rows)
    for r in bad:
        if r["phi_defined"] == "True":
            r["phi"] = str(float(r["phi"]) + 1e-6)
            break
    expect_halt("P1 (one phi off by 1e-6)", ref_rows=bad)
    bad = copy.deepcopy(ref_rows)[:-1]
    expect_halt("P1 (a reference row missing)", ref_rows=bad)
    badv = copy.deepcopy(ref_v)
    badv["two_wave_reproducibility"]["phi_t1_t2_rank_agreement"]["n"] = 82
    expect_halt("P2 (reference n changed)", ref_verdicts=badv)
    bad34 = copy.deepcopy(v34)
    bad34["per_substrate"]["v0.22"]["cpc"]["rho"] += 1e-6
    expect_halt("P3 (v0.34 rho off by 1e-6)", v34=bad34)
    saved = dict(S.PROBE_SHA256)
    S.PROBE_SHA256["scripts/acquire_v0_23.py"] = "0" * 64
    expect_halt("P4 (probe checksum differs)")
    S.PROBE_SHA256.clear(); S.PROBE_SHA256.update(saved)
    saved = dict(S.REF_FILES)
    S.REF_FILES["v1_8_instrument_table.csv"] = "0" * 64
    try:
        S.check_references()
        check("frozen v1.8 reference checksum enforced", False)
    except S.GateFailure:
        check("frozen v1.8 reference checksum enforced", True)
    S.REF_FILES.clear(); S.REF_FILES.update(saved)
    S.load_wave = real_load
    return t1, t2


# --------------------------------------------------------------------------- #
# end-to-end
# --------------------------------------------------------------------------- #
def run_scorer(args):
    env = dict(os.environ)
    t0 = time.time()
    r = subprocess.run([sys.executable, str(SCRIPTS / "score_v41.py")] + args, capture_output=True, text=True, env=env)
    return r, time.time() - t0


SCENARIOS = ("copy_t2", "copy_t1", "shuffle_models", "drop_model", "partial_fail", "snapshot_drift", "rerun")


class _R:
    def __init__(self, d):
        self.returncode, self.stderr = d["exit"], d["stderr"]


def run_scenario(scratch, sc):
    """Generate one synthetic t3 wave and score it; record exit/stderr/time."""
    gen = SCRIPTS / "tests" / "make_synthetic_t3.py"
    if sc == "rerun":                                   # determinism: score copy_t1 again
        r, dt = run_scorer(["--synthetic", str(scratch / "copy_t1"), "--out", str(scratch / "copy_t1_rerun")])
        d = scratch / "copy_t1_rerun"
        d.mkdir(parents=True, exist_ok=True)
    else:
        d = scratch / sc
        subprocess.run([sys.executable, str(gen), sc, str(d)], check=True, capture_output=True)
        r, dt = run_scorer(["--synthetic", str(d)])
    json.dump({"exit": r.returncode, "stderr": r.stderr[-2000:], "stdout": r.stdout[-2000:],
               "seconds": dt}, open(d / "_run.json", "w"), indent=2)
    print(f"  [{sc}] exit {r.returncode} in {dt:.0f}s")


def e2e(scratch):
    print("B. end-to-end (synthetic t3 through the real extraction path)")
    res = {}
    for sc in SCENARIOS[:-1]:
        run = json.load(open(scratch / sc / "_run.json"))
        out = (json.load(open(scratch / sc / "_score" / "v41_verdicts.json")) if run["exit"] == 0 else None)
        res[sc] = (_R(run), out, run["seconds"])

    def V(sc):
        return res[sc][1]["verdicts"]

    o = res["copy_t2"][1]
    check("copy_t2: exits 0", res["copy_t2"][0].returncode == 0, res["copy_t2"][0].stderr[-300:])
    if o:
        v = o["verdicts"]
        check("copy_t2: H_Phi CONFIRMED, rho = 1", v["H_Phi_LongHorizon"]["verdict"] == "CONFIRMED"
              and abs(v["H_Phi_LongHorizon"]["rho"] - 1) < 1e-12,
              f"n={v['H_Phi_LongHorizon']['n']}, frame null p95 "
              f"{v['H_Phi_LongHorizon']['frame_structure_null']['null_p95']:.3f}")
        check("copy_t2: H_Presence CONFIRMED, 5/5 rho = 1", v["H_Presence_LongHorizon"]["verdict"] == "CONFIRMED"
              and all(abs(x["rho"] - 1) < 1e-12 for x in v["H_Presence_LongHorizon"]["per_substrate"].values()))
        check("copy_t2: H_Decay phi MARGINAL with CI [0,0]", v["H_Horizon_Decay"]["phi"]["verdict"] == "MARGINAL"
              and v["H_Horizon_Decay"]["phi"]["ci95"] == [0.0, 0.0])
        check("copy_t2: H_Drift UNDETERMINED (no change)", v["H_Drift_Dissociation"]["verdict"] == "UNDETERMINED")
        check("copy_t2: phantom retention = 1.0", v["H_Phantom_LongPersistence"]["pooled"]["proportion"] == 1.0,
              str(v["H_Phantom_LongPersistence"]["pooled"]))
        mc = o["manipulation_checks"]
        check("copy_t2: MC_Completeness 852/852", mc["MC_Completeness"]["ok_total"] == 852
              and mc["MC_Completeness"]["status"] == "PASS")
        check("copy_t2: MC_Snapshot PASS 4/4", mc["MC_Snapshot"]["status"] == "PASS")
        check("copy_t2: MC_Truncation descriptive per model", mc["MC_Truncation"]["status"] == "DESCRIPTIVE")
        tw = list(csv.DictReader(open(scratch / "copy_t2/_score/v41_three_wave_table.csv")))
        check("copy_t2: three-wave table 336 rows (112 x 3)", len(tw) == 336, str(len(tw)))
        check("copy_t2: delta-t t2->t3 = 161 days", all(r["days_t2_t3"] == 161 for r in o["delta_t"]),
              str([r["days_t2_t3"] for r in o["delta_t"]]))

    o = res["copy_t1"][1]
    check("copy_t1: exits 0", res["copy_t1"][0].returncode == 0, res["copy_t1"][0].stderr[-300:])
    if o:
        v = o["verdicts"]
        h = v["H_Phi_LongHorizon"]
        check("copy_t1: rho(t2,t3) reproduces v1.8 0.6454 (n = 83)", round(h["rho"], 4) == 0.6454 and h["n"] == 83,
              f"rho={h['rho']:.4f}, n={h['n']}")
        fn = h["frame_structure_null"]
        want = ("CONFIRMED" if fn["p_frame"] < .05 else "MARGINAL")
        check("copy_t1: H_Phi follows the three-condition rule", h["verdict"] == want,
              f"{h['verdict']}; p_perm={h['p_perm']:.4f}, p_frame={fn['p_frame']:.4f}, "
              f"null mean {fn['null_mean']:.3f}, p95 {fn['null_p95']:.3f}")
        check("copy_t1: H_Decay phi FALSIFIED (long horizon 'more stable')",
              v["H_Horizon_Decay"]["phi"]["verdict"] == "FALSIFIED", str(v["H_Horizon_Decay"]["phi"]["ci95"]))
        check("copy_t1: horizon table rho(t1,t3) = 1 for phi",
              abs(v["H_Horizon_Decay"]["reported_alongside"]["phi"]["t1_t3"]["rho"] - 1) < 1e-12)
        check("copy_t1: drift verdict obeys its rule", v["H_Drift_Dissociation"]["verdict"] in
              ("CONFIRMED", "MARGINAL", "FALSIFIED"), f"{v['H_Drift_Dissociation']['verdict']} rho="
              f"{v['H_Drift_Dissociation'].get('rho')}")

    o = res["shuffle_models"][1]
    check("shuffle_models: exits 0", res["shuffle_models"][0].returncode == 0, res["shuffle_models"][0].stderr[-300:])
    if o:
        v = o["verdicts"]
        check("shuffle_models: pi_hat preserved -> Presence CONFIRMED 5/5",
              all(abs(x["rho"] - 1) < 1e-12 for x in v["H_Presence_LongHorizon"]["per_substrate"].values()))
        h = v["H_Phi_LongHorizon"]
        check("shuffle_models: not CONFIRMED (model identity scrambled)", h["verdict"] != "CONFIRMED",
              f"rho={h['rho']:.3f}, p_frame={h['frame_structure_null']['p_frame']:.3f} -> {h['verdict']}")
        check("shuffle_models: Drift UNDETERMINED (Presence unchanged)",
              v["H_Drift_Dissociation"]["verdict"] == "UNDETERMINED")

    o = res["drop_model"][1]
    check("drop_model: exits 0 on a 5-model panel", res["drop_model"][0].returncode == 0,
          res["drop_model"][0].stderr[-300:])
    if o:
        check("drop_model: gemini-2.5-flash-lite dropped in all waves",
              o["models_dropped"] == ["gemini-2.5-flash-lite"] and len(o["panel_used"]) == 5)
        check("drop_model: H_Phi computed on the reduced panel", o["verdicts"]["H_Phi_LongHorizon"]["verdict"]
              in ("CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED"),
              f"rho={o['verdicts']['H_Phi_LongHorizon'].get('rho')}")
    check("partial_fail: HALT (exit 4) on a residual failure", res["partial_fail"][0].returncode == 4,
          res["partial_fail"][0].stderr.strip()[-200:])
    o = res["snapshot_drift"][1]
    check("snapshot_drift: exits 0", res["snapshot_drift"][0].returncode == 0)
    if o:
        check("snapshot_drift: MC_Snapshot names gpt-4o", o["manipulation_checks"]["MC_Snapshot"]["mismatched"] == ["gpt-4o"])
        check("snapshot_drift: sensitivity without gpt-4o reported",
              (o.get("snapshot_sensitivity") or {}).get("without_models") == ["gpt-4o"])
        check("snapshot_drift: main verdicts keep all 6 models", len(o["panel_used"]) == 6)

    # determinism + --run guard
    a = json.load(open(scratch / "copy_t1/_score/v41_verdicts.json"))
    b = json.load(open(scratch / "copy_t1_rerun/v41_verdicts.json"))
    check("deterministic: identical verdicts JSON on re-run", a == b)
    r, _ = run_scorer(["--run"])
    check("--run refuses without the v0.41-prereg-r1 tag (exit 3)", r.returncode == 3, r.stderr.strip()[-120:])
    return {k: {"exit": v[0].returncode, "seconds": round(v[2], 1),
                "verdicts": ({h: (x.get("verdict") if h != "H_Horizon_Decay" else
                                  {"phi": x["phi"]["verdict"], "pi_hat": x["pi_hat"]["verdict"]})
                              for h, x in v[1]["verdicts"].items()} if v[1] else None)}
            for k, v in res.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--unit-only", action="store_true")
    ap.add_argument("--scenario", choices=SCENARIOS + ("all",),
                    help="generate + score scenario(s) only (no checks); then run without it to check")
    ap.add_argument("--scratch", default=None)
    a = ap.parse_args()
    scratch = Path(a.scratch or tempfile.mkdtemp(prefix="v41_tests_"))
    scratch.mkdir(parents=True, exist_ok=True)
    if a.scenario:
        for sc in (SCENARIOS if a.scenario == "all" else (a.scenario,)):
            run_scenario(scratch, sc)
        return 0
    unit_tests()
    summary = e2e(scratch) if not a.unit_only else None
    n_fail = sum(1 for r in RESULTS if not r["passed"])
    out = {"passed": len(RESULTS) - n_fail, "failed": n_fail, "results": RESULTS, "scenarios": summary}
    json.dump(out, open(scratch / "test_results_v41.json", "w"), indent=2, default=str)
    print(f"\n{len(RESULTS) - n_fail}/{len(RESULTS)} passed  -> {scratch / 'test_results_v41.json'}")
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
