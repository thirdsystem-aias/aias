#!/usr/bin/env python3
"""
make_scenarios_v0_43.py -- SYNTHETIC Stage 1 scorer outputs for testing the v0.43 paper pipeline.
Never real data: no Stage 1 search-interest response exists when this is written, none is read, and no API is called.

For each scenario a scratch repository root is built under OUTDIR/<scenario>/root (never inside this repository):
  osf/v43/registries/units_v0_43.csv     112 SYNTHETIC units (invented names SYN-H01 ... SYN-S24; the real substrate
                                         sizes 16/24/24/24/24 and five automotive units in cell D), synthetic P, C*, pi
  osf/v43/registries/terms_v0_43.json    synthetic term kinds (topic / plain)
  osf/v43/registries/bundles_v0_43.json  main bundles formed by the locked rule (trends_common.main_bundles)
  osf/v43/data/trends_raw/main{1,2,3}/   84 synthetic request records in the acquisition script's stored format,
                                         each response built like acquire_trends_v0_43.sim_response (Trends-style 0-100
                                         integers relative to the bundle's largest value)
Then the LOCKED scorer (osf/v43/scripts/score_v0_43.py, imported read-only) runs score(root, stage=1) on that root
with --draws permutations and bootstrap resamples (10,000 = the pre-registered number), and its output is written with
the scorer's own dump_json. Nothing is changed in the scorer's output except one added top-level key,
"synthetic_fixture", which the fill and the charts use to recognise synthetic input.

Scenarios (planted relation between June Presence and the June-to-November change; all scored by the locked scorer):
  lead       positive relation, every check passes                         -> H_Pred_Presence CONFIRMED (expected)
  lag        negative relation, every check passes                         -> FALSIFIED with REVERSED (expected)
  null       no relation                                                   -> UNDETERMINED (thresholds not met)
  marginal   weak positive relation; the generator seed is searched so that the scorer returns MARGINAL
  sparse     half the units with no search volume (n below 60), one request missing, noisy pulls, Presence unrelated
             to search level, 40% topics                                   -> UNDETERMINED (minimum n), all three flags
The expected words are only the generator's aim: every word in a fixture is the locked scorer's own output.

Writes OUTDIR/SYNTHETIC_<scenario>_v43_stage1_verdicts.json and OUTDIR/SYNTHETIC_<scenario>_v43_pulls.json (the pull
summary the fill reads), plus the scratch roots. Refuses an OUTDIR inside this repository.

Usage: python3 papers/v0_43/tests/make_scenarios_v0_43.py OUTDIR [--draws N] [scenario ...]
"""
import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import shutil
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
ROOT = PAPER.parents[1]
sys.path.insert(0, str(PAPER))
import numpy as np  # noqa: E402
import v043_values as VV  # noqa: E402  (imports the locked scorer read-only)

SC = VV.SC
TC = SC.tc
SCENARIOS = ["lead", "lag", "null", "marginal", "sparse"]
D = dt.date
WEEKS = [D(2025, 5, 4) + dt.timedelta(days=7 * i) for i in range(79)]          # 2025-05-04 .. 2026-11-01
IDX = {w: i for i, w in enumerate(WEEKS)}
I_FEB, I_MAY = IDX[D(2026, 2, 1)], IDX[D(2026, 5, 31)]                          # momentum ramp (W_prior -> W_base)
I_JUN, I_OCT = IDX[D(2026, 5, 31)], IDX[D(2026, 10, 11)]                        # growth ramp (W_base -> W_end)
PREFIX = {"v0.19": "H", "v0.20": "K", "v0.21": "C", "v0.22": "A", "v0.23": "S"}
SIZES = {"v0.19": 16, "v0.20": 24, "v0.21": 24, "v0.22": 24, "v0.23": 24}
PULL_START = {"main1": "2026-11-12T15:00:00+00:00", "main2": "2026-11-13T15:30:00+00:00",
              "main3": "2026-11-14T16:00:00+00:00"}

PARAMS = {  # beta_P: planted effect of z(P) on the change; conc: effect of z(P) on the June level
    "lead": dict(seed=43001, beta_P=0.30, beta_C=0.20, conc=0.8, pull_sd=0.06, topic=0.55, zero_share=0.0),
    "lag": dict(seed=43002, beta_P=-0.30, beta_C=0.0, conc=0.8, pull_sd=0.06, topic=0.55, zero_share=0.0),
    "null": dict(seed=43003, beta_P=0.0, beta_C=0.0, conc=0.8, pull_sd=0.06, topic=0.55, zero_share=0.0),
    "marginal": dict(seed=43100, beta_P=0.11, beta_C=0.0, conc=0.8, pull_sd=0.06, topic=0.55, zero_share=0.0,
                     search="MARGINAL"),
    "sparse": dict(seed=43005, beta_P=0.30, beta_C=0.0, conc=0.0, pull_sd=0.9, topic=0.40, zero_share=0.50,
                   missing=("main2", "v0.21", 2)),
}


def ramp(i, a, b):
    return min(1.0, max(0.0, (i - a) / float(b - a)))


def z(x):
    x = np.asarray(x, float)
    return (x - x.mean()) / (x.std() or 1.0)


def make_units(rng, prm):
    rows = []
    for s in VV.SUBS:
        n = SIZES[s]
        P2 = np.round(rng.uniform(25, 98, n), 4)
        for i in range(n):
            p2 = float(P2[i])
            p1 = float(np.clip(p2 + rng.normal(0, 6), 0, 100))
            p3 = float(np.clip(p2 + rng.normal(0, 6), 0, 100))
            ment = int(max(0, round(p2 / 4 + rng.normal(0, 4))))
            cs = float(np.round(rng.uniform(20, 100), 4)) if ment >= 6 else None
            pi = float(np.clip(p2 / 110 + rng.normal(0, 0.05), 0, 1))
            cell = ("D" if i >= n - 5 else "A") if s == "v0.22" else ("" if s in ("v0.19", "v0.23") else "BC"[i % 2])
            name = f"SYN-{PREFIX[s]}{i + 1:02d}"
            rows.append({"substrate": s, "unit": name, "search_name": name, "cell": cell,
                         "P_t1": f"{p1:.4f}", "C_star_t1": "" if cs is None else f"{cs:.4f}", "mentions_t1": str(ment),
                         "pi_hat_t1": repr(pi), "P_t2": f"{p2:.4f}", "C_star_t2": "" if cs is None else f"{cs:.4f}",
                         "mentions_t2": str(ment), "pi_hat_t2": repr(pi), "P_t3": f"{p3:.4f}",
                         "C_star_t3": "" if cs is None else f"{cs:.4f}", "mentions_t3": str(ment), "pi_hat_t3": repr(pi)})
    return rows


def latent(rng, rows, prm):
    """Weekly log volume per unit (None = no search volume): level + season + momentum + planted growth."""
    out = {}
    for s in VV.SUBS:
        rs = [r for r in rows if r["substrate"] == s]
        zp = z([float(r["P_t2"]) for r in rs])
        cs = [float(r["C_star_t2"]) if r["C_star_t2"] else None for r in rs]
        rated = [c for c in cs if c is not None]
        zc = {i: (c - np.mean(rated)) / (np.std(rated) or 1) for i, c in enumerate(cs) if c is not None}
        amp, phase = rng.uniform(0.05, 0.25), rng.uniform(0, 52)
        for i, r in enumerate(rs):
            key = (s, r["unit"])
            if rng.random() < prm["zero_share"]:
                out[key] = None
                continue
            a = 4.0 + prm["conc"] * zp[i] + 0.6 * rng.normal()
            mom = 0.25 * rng.normal()
            g = prm["beta_P"] * zp[i] + prm["beta_C"] * zc.get(i, 0.0) + 0.5 * rng.normal()
            own = 0.15 * rng.normal(size=len(WEEKS))
            out[key] = np.array([a + amp * math.sin(2 * math.pi * (k + phase) / 52.0) + mom * ramp(k, I_FEB, I_MAY)
                                 + g * ramp(k, I_JUN, I_OCT) + own[k] for k in range(len(WEEKS))])
    return out


def response(cols_log, terms):
    """Trends-style response: values relative to the bundle's largest weekly value, 0-100 integers."""
    raw = [np.zeros(len(WEEKS)) if c is None else np.exp(c) for c in cols_log]
    mx = max(float(x.max()) for x in raw) or 1.0
    pts = []
    for k, w in enumerate(WEEKS):
        ts = int(dt.datetime(w.year, w.month, w.day, tzinfo=dt.timezone.utc).timestamp())
        vals = []
        for t, x in zip(terms, raw):
            v = int(round(100 * float(x[k]) / mx))
            vals.append({"query": t, "value": str(v), "extracted_value": v})
        pts.append({"date": w.isoformat(), "timestamp": str(ts), "values": vals})
    return {"search_metadata": {"status": "Success"}, "interest_over_time": {"timeline_data": pts}}


def build_root(root, prm, seed):
    rng = np.random.default_rng(seed)
    rows = make_units(rng, prm)
    lat = latent(rng, rows, prm)
    reg = root / "osf/v43/registries"
    reg.mkdir(parents=True)
    with open(reg / "units_v0_43.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    chosen, terms = {}, {}
    for r in rows:
        kind = "topic" if rng.random() < prm["topic"] else "plain"
        t = "/g/syn" + hashlib.sha1(r["unit"].encode()).hexdigest()[:6] if kind == "topic" else r["unit"]
        chosen[f"{r['substrate']}|{r['unit']}"] = {"kind": kind, "search_name": r["unit"], "term": t,
                                                   "suggestion": None}
        terms[(r["substrate"], r["unit"])] = t
    TC.dump_json({"chosen": chosen, "summary": {"synthetic": True}}, reg / "terms_v0_43.json")
    bundles = {}
    i_base = [IDX[w] for w in TC.window_starts(D(2026, 6, 6))]
    for s in VV.SUBS:
        us = [r["unit"] for r in rows if r["substrate"] == s]
        lvl = {u: (0, -1e9 if lat[(s, u)] is None else float(np.exp(lat[(s, u)][i_base]).mean())) for u in us}
        mb = TC.main_bundles(us, lambda u: TC.size_sort_key(lvl[u], u))
        bundles[s] = {"main_bundles": mb, "terms": {u: terms[(s, u)] for u in us}}
    TC.dump_json({"created_utc": "SYNTHETIC", "substrates": bundles}, reg / "bundles_v0_43.json")
    raw = root / "osf/v43/data/trends_raw"
    for p, step in enumerate(VV.STEPS):
        t0 = dt.datetime.fromisoformat(PULL_START[step])
        k = 0
        for s in VV.SUBS:
            for j, b in enumerate(bundles[s]["main_bundles"]):
                cols = [None if lat[(s, u)] is None else lat[(s, u)] + prm["pull_sd"] * rng.normal(size=len(WEEKS))
                        for u in b]
                tm = (t0 + dt.timedelta(seconds=20 * k)).isoformat()
                k += 1
                q = [terms[(s, u)] for u in b]
                params = {"engine": "google_trends", "data_type": "TIMESERIES", "geo": "US", "tz": "0",
                          "date": "2025-05-04 2026-11-07", "q": ",".join(q)}
                if prm.get("missing") == (step, s, j):
                    att = [{"utc": tm, "http_status": 500, "error": "SYNTHETIC HTTP 500", "response": None}] * 3
                    rec = {"status": "missing", "n_attempts": 3, "attempts": att}
                else:
                    resp = response(cols, q)
                    rec = {"status": "ok", "n_attempts": 1,
                           "attempts": [{"utc": tm, "http_status": 200, "error": None, "response": resp,
                                         "mc_weekly_ok": True, "mc_weekly_reasons": []}]}
                rec.update({"step": step, "substrate": s, "bundle": j, "units": b, "terms": q, "params": params,
                            "fetched_utc": tm})
                (raw / step).mkdir(parents=True, exist_ok=True)
                TC.dump_json(rec, raw / step / f"{s}_b{j}.json")
    return rows


def score_root(root, draws):
    out, _ = SC.score(str(root), 1, draws, draws)
    return out


def run(outdir, name, draws):
    prm = PARAMS[name]
    base = outdir / name
    seed = prm["seed"]
    tries = 0
    while True:
        if base.exists():
            shutil.rmtree(base)
        root = base / "root"
        build_root(root, prm, seed)
        if not prm.get("search"):
            break
        quick = score_root(root, 999)
        t = quick["tests"]["H_Pred_Presence"]
        ok = t["verdict"] == prm["search"] and 0.055 < t.get("p_one", 1) < 0.09
        tries += 1
        if ok or tries >= 60:
            break
        seed += 1
    t0 = time.time()
    out = score_root(root, draws)
    out["synthetic_fixture"] = {
        "scenario": name, "generator": "papers/v0_43/tests/make_scenarios_v0_43.py", "generator_seed": seed,
        "planted": {k: v for k, v in prm.items() if k not in ("seed", "search")},
        "note": "SYNTHETIC: invented units and synthetic Trends responses scored by the locked score_v0_43.score(); "
                "not results"}
    vpath = outdir / f"SYNTHETIC_{name}_v43_stage1_verdicts.json"
    TC.dump_json(out, vpath)
    pulls = VV.pull_summary(root / "osf/v43/data/trends_raw")
    pulls["raw_dir"] = f"SYNTHETIC scratch root ({name})"
    TC.dump_json(pulls, outdir / f"SYNTHETIC_{name}_v43_pulls.json")
    words = {k: (v["verdict"], v.get("labels")) for k, v in out["tests"].items()}
    print(f"  {name}: seed {seed}, scored in {time.time() - t0:.0f} s; flags {out['flags']}; {words}")
    if prm.get("search") and out["tests"]["H_Pred_Presence"]["verdict"] != prm["search"]:
        print(f"  WARNING: {name}: full run gave {out['tests']['H_Pred_Presence']['verdict']}, aimed at {prm['search']}")
    return vpath


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("outdir", type=Path)
    ap.add_argument("scenarios", nargs="*")
    ap.add_argument("--draws", type=int, default=10000)
    a = ap.parse_args(argv)
    out = a.outdir.resolve()
    if str(out).startswith(str(ROOT.resolve()) + "/") or out == ROOT.resolve():
        raise SystemExit(f"REFUSED: {out} is inside the repository (synthetic roots and raw data never go there)")
    out.mkdir(parents=True, exist_ok=True)
    names = a.scenarios or SCENARIOS
    for n in names:
        if n not in PARAMS:
            raise SystemExit(f"unknown scenario {n}")
    for n in names:
        run(out, n, a.draws)
    return 0


if __name__ == "__main__":
    sys.exit(main())
