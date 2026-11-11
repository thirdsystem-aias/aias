#!/usr/bin/env python3
"""
score_v0_62.py -- AIAS(TM) v0.62 scorer (Spanish, Korean and Chinese against English t4), pre-registration r2 DRAFT,
sections 2 and 7. Exactly the pre-registered tests: H_Lang_Presence (PRIMARY, ES, KO, ZH), H_Lang_Phi (ES, KO, ZH),
H_Lang_Rank (ES, KO, ZH; conditional on v1.14 PASS), with the joint reading of section 2.6, the alongside figures of section 2.2
(per-category rho_c, level shift Delta_L, uncentred value) and the sensitivities S-Denon and S-Headphones (7.5).
THE PRE-REGISTRATION PROSE IS AUTHORITATIVE. The real scoring runs ONCE (--run refuses if the verdicts file exists
or tag v0.62-prereg-r1 is not on origin).

Statistic (section 2.1): rho_c = Pearson's r of within-category average ranks, centred on each category's mean rank,
pooled over categories; values rounded to 10 decimals before ranking (v0.44 r1, notes N15/N16; identical to
score_v0_44.rho_pw). Permutation: y shuffled within category, 10,000 draws, p = (1 + #{rho_perm >= rho_obs - 1e-12})
/ 10,001. Bootstrap: units resampled with replacement within category, 10,000, percentile 95%.

Kernels: pi_hat (sum of mentions / answered Phase B calls, model x run pooled) and phi (v1.8, per run on the three
models, mean of the defined runs if >= 2 are defined) are TRANSCRIBED here from score_v41.phi_m and
score_v0_42.pi_hat / phi_panel, because the v0.62 branch does not contain osf/v41-v42 (r1 draft note S1). Gate P1
(section 7.3) must show, before the lock, that these transcriptions reproduce v0.42's English t4 values exactly; if
the v0.42 scripts are merged into this branch first, the imports replace the transcriptions.

SCORER_NOTES
 S1  kernels transcribed (above).
 S2  units: the 112 registry units minus those removed by params_v0_62.HEADPHONES_OPTION (B: Denon; C: v0.19).
     S-Denon and S-Headphones are computed under option A only (under B, S-Denon equals the primary test; under C
     both are void and reported as such). r3: S-COI (the units in params_v0_62.COI_FLAGGED removed; DEVIATIONS
     Entry 0, Part F) is computed under every option, beside S-Denon and S-Headphones, for H_Lang_Presence.
 S3  drop rule (7.4): a model with < 90% of its expected Phase B calls answered in language L -> every test in L is
     UNDETERMINED (reported on the remaining models as descriptives, not here).
 S4  English comparator: a CSV with columns substrate, brand, pi, phi (v0.42's v42_brand_table.csv columns pi_N3_S0,
     phi_N3_S0 are mapped by read_english(); the mapping is re-checked against v0.42's table once it exists).
 S5  H_Lang_Rank: R* values are an input (v1.14's modal_position, computed by v1.14's own scorer); without
     --rank-status PASS the test is NOT TESTED.
"""
import argparse
import collections
import csv
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import params_v0_62 as P  # noqa: E402

ROOT = Path(os.environ.get("AIAS_ROOT", str(Path(__file__).resolve().parents[3]))).resolve()
V62 = ROOT / "osf/v62"
PREREG_TAG = "v0.62-prereg-r1"
VERDICTS = V62 / "v62_verdicts.json"
F, MODELS, RUNS = 6, ["claude-fable-5-2", "gpt-6-astra", "gemini-4-argon"], (1, 2, 3)
SUBS = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
LANGS = ("es", "ko", "zh")
SEEDS = {("H_Lang_Presence", "es"): 620101, ("H_Lang_Presence", "ko"): 620102, ("H_Lang_Presence", "zh"): 620103,
         ("H_Lang_Phi", "es"): 620111, ("H_Lang_Phi", "ko"): 620112, ("H_Lang_Phi", "zh"): 620113,
         ("H_Lang_Rank", "es"): 620121, ("H_Lang_Rank", "ko"): 620122, ("H_Lang_Rank", "zh"): 620123,
         "bootstrap": 620131, "descriptives": 620141}
N_PERM = N_BOOT = 10_000
NAN = float("nan")
PRES = (0.70, 0.50)          # CONFIRMED rho >= 0.70 and p < .05; FALSIFIED rho < 0.50
PHI = (0.50, 0.30, 40)       # CONFIRMED >= 0.50 and p < .05; FALSIFIED < 0.30; UNDETERMINED n < 40
RANK = (0.50, 0.30, 30)      # CONFIRMED >= 0.50 and p < .05; FALSIFIED < 0.30 or p >= .05; UNDETERMINED n < 30
ALPHA, DROP_SHARE = 0.05, 0.90


# =========================================================================== statistics
def within_ranks(values, groups):
    v = np.round(np.asarray(values, float), 10)
    g = np.asarray(groups)
    r = np.empty(len(v))
    for k in dict.fromkeys(g):
        i = np.where(g == k)[0]
        order = v[i]
        sorter = np.argsort(order, kind="mergesort")
        ranks = np.empty(len(i))
        ranks[sorter] = np.arange(1, len(i) + 1)
        for val in np.unique(order):                      # average ranks for ties
            t = order == val
            ranks[t] = ranks[t].mean()
        r[i] = ranks
    return r


def centred_ranks(values, groups):
    r = within_ranks(values, groups)
    g = np.asarray(groups)
    for k in dict.fromkeys(g):
        i = g == k
        r[i] = r[i] - r[i].mean()
    return r


def _pearson(a, b):
    a = np.asarray(a, float) - np.mean(a)
    b = np.asarray(b, float) - np.mean(b)
    d = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d > 0 else NAN


def rho_c(x, y, groups):
    """Centred pooled within-category Spearman (section 2.1)."""
    return _pearson(centred_ranks(x, groups), centred_ranks(y, groups)) if len(x) >= 3 else NAN


def rho_uncentred(x, y, groups):
    """v0.41/v0.42's pooled within-substrate statistic (ranks within category, NOT centred): non-gating figure."""
    return _pearson(within_ranks(x, groups), within_ranks(y, groups)) if len(x) >= 3 else NAN


def _gidx(g):
    g = np.asarray(g)
    return [np.where(g == k)[0] for k in dict.fromkeys(g)]


def perm_p(x, y, g, obs, seed, n_draws=N_PERM):
    if not np.isfinite(obs):
        return NAN
    rng = np.random.default_rng(seed)
    y = np.asarray(y, float)
    hits = 0
    for _ in range(n_draws):
        yp = y.copy()
        for gi in _gidx(g):
            yp[gi] = y[rng.permutation(gi)]
        hits += bool(rho_c(x, yp, g) >= obs - 1e-12)
    return (1 + hits) / (n_draws + 1)


def bootstrap_ci(g, seed, n_boot, fn):
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(n_boot):
        idx = np.concatenate([rng.choice(gi, size=len(gi), replace=True) for gi in _gidx(g)])
        v = fn(idx)
        if np.isfinite(v):
            vals.append(v)
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))] if vals else [NAN, NAN]


# =========================================================================== kernels (transcribed; note S1)
def phi_m(k):
    """score_v41.phi_m: phi on M models from the per-model counts k (each of F questions). -> (phi, pi, partition)."""
    k = np.asarray(k, float)
    m = len(k)
    pi = float(k.sum() / (m * F))
    if pi <= 0.0:
        return None, pi, "zero"
    if pi >= 1.0:
        return None, pi, "saturated"
    return float(((k - F * pi) ** 2).sum() / (F * pi * (1.0 - pi)) / (m - 1)), pi, "defined"


def aggregate(B, excluded=frozenset()):
    """Coded Phase B rows -> (k[(model, run, sub, brand)], answered[(model, run, sub)] = set of call ids)."""
    k, ans = collections.defaultdict(int), collections.defaultdict(set)
    for r in B:
        if r["call_id"] in excluded or r.get("condition", "S0") != "S0":
            continue
        run = int(r["run"])
        ans[(r["model"], run, r["substrate"])].add(r["call_id"])
        k[(r["model"], run, r["substrate"], r["brand"])] += int(r["mentioned"])
    return k, ans


def unit_values(units, B, models=MODELS):
    """{unit: {'pi', 'phi', 'partition'}} as score_v0_42.pi_hat and phi_panel (N3, S0)."""
    k, ans = aggregate(B)
    out = {}
    for (s, b) in units:
        num = sum(k[(m, r, s, b)] for m in models for r in RUNS)
        den = sum(len(ans[(m, r, s)]) for m in models for r in RUNS)
        runs = []
        for r in RUNS:
            if any(len(ans[(m, r, s)]) != F for m in models):
                runs.append((None, "missing"))
                continue
            phi, _pi, part = phi_m([k[(m, r, s, b)] for m in models])
            runs.append((phi, part))
        vals = [p for p, part in runs if part == "defined"]
        parts = [part for _, part in runs]
        if len(vals) >= 2:
            phi, part = float(np.mean(vals)), "defined"
        elif parts and all(p == "zero" for p in parts):
            phi, part = None, "zero"
        elif parts and all(p == "saturated" for p in parts):
            phi, part = None, "saturated"
        else:
            phi, part = None, "undefined"
        out[(s, b)] = {"pi": num / den if den else NAN, "phi": phi, "partition": part}
    return out


def dropped_models(B, n_b_per_run):
    """Models with < 90% of their expected Phase B calls answered (expected = 3 runs x Phase B probes)."""
    calls = collections.defaultdict(set)
    for r in B:
        calls[r["model"]].add(r["call_id"])
    return [m for m in MODELS if len(calls[m]) < DROP_SHARE * 3 * n_b_per_run]


# =========================================================================== tests
def _pairs(xd, yd, keys):
    keys = [k for k in keys if k in xd and k in yd and xd[k] is not None and yd[k] is not None
            and np.isfinite(xd[k]) and np.isfinite(yd[k])]
    return keys, np.array([xd[k] for k in keys], float), np.array([yd[k] for k in keys], float), np.array([k[0] for k in keys])


def rank_test(xd, yd, keys, seed, n_perm=N_PERM, n_boot=N_BOOT, min_cat=1):
    keys, x, y, g = _pairs(xd, yd, keys)
    if min_cat > 1:                                     # H_Lang_Rank: categories with >= 5 units rated in both
        cnt = collections.Counter(g)
        m = np.array([cnt[c] >= min_cat for c in g], bool)
        keys, x, y, g = [k for k, z in zip(keys, m) if z], x[m], y[m], g[m]
    rho = rho_c(x, y, g)
    t = {"n": len(keys), "rho_c": rho, "rho_uncentred_comparability": rho_uncentred(x, y, g)}
    t["p_perm"] = perm_p(x, y, g, rho, seed, n_perm) if np.isfinite(rho) else NAN
    t["ci95_rho_c"] = bootstrap_ci(g, seed, n_boot, lambda i: rho_c(x[i], y[i], g[i])) if np.isfinite(rho) else [NAN, NAN]
    t["per_category_rho_c"] = {c: (rho_c(x[g == c], y[g == c], g[g == c]) if (g == c).sum() >= 3 else NAN)
                               for c in dict.fromkeys(g)}
    return t


def verdict_presence(rho, p):
    if not np.isfinite(rho) or not np.isfinite(p):
        return "UNDETERMINED"
    if rho >= PRES[0] and p < ALPHA:
        return "CONFIRMED"
    return "FALSIFIED" if rho < PRES[1] else "MARGINAL"


def verdict_phi(n, rho, p):
    if n < PHI[2] or not np.isfinite(rho) or not np.isfinite(p):
        return "UNDETERMINED"
    if rho >= PHI[0] and p < ALPHA:
        return "CONFIRMED"
    return "FALSIFIED" if rho < PHI[1] else "MARGINAL"


def verdict_rank(n, rho, p, degenerate=False):
    if n < RANK[2] or degenerate or not np.isfinite(rho) or not np.isfinite(p):
        return "UNDETERMINED"
    if rho >= RANK[0] and p < ALPHA:
        return "CONFIRMED"
    return "FALSIFIED" if (rho < RANK[1] or p >= ALPHA) else "MARGINAL"


def joint_reading(*verdicts):
    """Section 2.6, on the H_Lang_Presence verdicts in LANGS order (ES, KO, ZH)."""
    named = list(zip([l.upper() for l in LANGS], verdicts))
    if all(v == "CONFIRMED" for v in verdicts):
        return "Language-robust"
    if "FALSIFIED" in verdicts:
        return "Language-dependent (" + ", ".join(l for l, v in named if v == "FALSIFIED") + ")"
    return "Partly robust"


def unit_set(units, option=None, sensitivity=None):
    """Units of the primary test under the headphones option; sensitivity 'S-Denon' / 'S-Headphones' (option A);
    r3: 'S-COI' removes every unit in params_v0_62.COI_FLAGGED (any option)."""
    keep = [u for u in units if not P.excluded_unit(u[0], u[1], option)]
    if sensitivity == "S-Denon":
        keep = [u for u in keep if u != ("v0.19", P.DENON[1])]
    elif sensitivity == "S-Headphones":
        keep = [u for u in keep if u[0] != "v0.19"]
    elif sensitivity == "S-COI":
        flagged = set(P.COI_FLAGGED)
        keep = [u for u in keep if u not in flagged]
    return keep


def score(units, en, lang_B, n_b_per_run=30, rank=None, rank_status="NOT RESOLVED", option=None,
          n_perm=N_PERM, n_boot=N_BOOT):
    """units: [(substrate, brand)] (112); en: {unit: {'pi', 'phi'}}; lang_B: {'es': coded B rows, 'ko': ..., 'zh': ...};
    rank: {'en': {unit: R*}, 'es': {...}, 'ko': {...}, 'zh': {...}} or None. -> verdict dict."""
    option = option or P.HEADPHONES_OPTION
    keys = unit_set(units, option)
    out = {"phase": "v0.62", "headphones_option": option, "n_units": len(keys), "tests": {}, "sensitivities": {}}
    pres = {}
    for lg in LANGS:
        V = unit_values(units, lang_B[lg])
        drop = dropped_models(lang_B[lg], n_b_per_run)
        und = f"models below 90% of Phase B calls in {lg}: {drop}" if drop else None
        xpi, ypi = {u: en[u]["pi"] for u in en}, {u: V[u]["pi"] for u in V}
        t = rank_test(xpi, ypi, keys, SEEDS[("H_Lang_Presence", lg)], n_perm, n_boot)
        t["verdict"] = "UNDETERMINED" if und else verdict_presence(t["rho_c"], t["p_perm"])
        _k, x, y, g = _pairs(xpi, ypi, keys)
        t["delta_L"] = float(np.mean(y - x)) if len(x) else NAN
        t["delta_L_ci95"] = bootstrap_ci(g, SEEDS["bootstrap"], n_boot, lambda i: float(np.mean(y[i] - x[i]))) if len(x) else [NAN, NAN]
        if und:
            t["reason"] = und
        out["tests"][f"H_Lang_Presence_{lg}"] = t
        pres[lg] = t["verdict"]
        xph = {u: en[u]["phi"] for u in en if en[u].get("phi") is not None}
        yph = {u: V[u]["phi"] for u in V if V[u]["phi"] is not None}
        tp = rank_test(xph, yph, keys, SEEDS[("H_Lang_Phi", lg)], n_perm, n_boot)
        tp["verdict"] = "UNDETERMINED" if und else verdict_phi(tp["n"], tp["rho_c"], tp["p_perm"])
        tp["partitions"] = dict(collections.Counter(V[u]["partition"] for u in keys))
        out["tests"][f"H_Lang_Phi_{lg}"] = tp
        if rank_status != "PASS" or not rank:
            out["tests"][f"H_Lang_Rank_{lg}"] = {"verdict": "NOT TESTED", "reason": f"v1.14 status: {rank_status}"}
        else:
            tr = rank_test(rank["en"], rank[lg], keys, SEEDS[("H_Lang_Rank", lg)], n_perm, n_boot, min_cat=5)
            vals = [rank[lg][k] for k in keys if k in rank[lg] and k in rank["en"]]
            deg = bool(vals) and collections.Counter(vals).most_common(1)[0][1] > 0.8 * len(vals)
            tr["verdict"] = "UNDETERMINED" if und else verdict_rank(tr["n"], tr["rho_c"], tr["p_perm"], deg)
            out["tests"][f"H_Lang_Rank_{lg}"] = tr
        for sens in ("S-Denon", "S-Headphones", "S-COI"):
            if sens != "S-COI" and (option == "C" or (option == "B" and sens == "S-Denon")):
                out["sensitivities"][f"{sens}_{lg}"] = {"void": f"headphones option {option}"}
                continue
            ks = unit_set(units, option, sens)
            s = rank_test(xpi, ypi, ks, SEEDS[("H_Lang_Presence", lg)], n_perm, n_boot)
            s["verdict"] = "UNDETERMINED" if und else verdict_presence(s["rho_c"], s["p_perm"])
            out["sensitivities"][f"{sens}_{lg}"] = s
    out["joint_reading"] = joint_reading(*(pres[lg] for lg in LANGS))
    return out


# =========================================================================== I/O and --run
def read_coded_b(coded_dir):
    rows = []
    for raw in ("v19", "v20", "v21", "v22", "v23"):
        p = Path(coded_dir) / f"{raw}_phase_b.csv"
        if p.exists():
            rows += list(csv.DictReader(open(p, encoding="utf-8")))
    return rows


def read_english(path):
    """S4: v0.42's brand table -> {unit: {'pi', 'phi'}}."""
    out = {}
    for r in csv.DictReader(open(path, encoding="utf-8")):
        pi = r.get("pi") or r.get("pi_N3_S0")
        phi = r.get("phi") if "phi" in r else r.get("phi_N3_S0")
        out[(r["substrate"], r["brand"])] = {"pi": float(pi) if pi not in (None, "") else NAN,
                                             "phi": float(phi) if phi not in (None, "", "None") else None}
    return out


def tag_on_origin():
    r = subprocess.run(["git", "-C", str(ROOT), "ls-remote", "--tags", "origin", PREREG_TAG],
                       capture_output=True, text=True, timeout=60)
    return r.returncode == 0 and f"refs/tags/{PREREG_TAG}" in r.stdout


def _clean(o):
    if isinstance(o, dict):
        return {(k if isinstance(k, str) else "|".join(map(str, k))): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, (float, np.floating)):
        return None if not np.isfinite(o) else float(o)
    return o


def main(argv=None):
    ap = argparse.ArgumentParser(description="AIAS v0.62 scorer (r1 draft)")
    ap.add_argument("--run", action="store_true", help="the one real scoring run (guarded)")
    ap.add_argument("--english", help="English t4 brand table (v0.42)")
    ap.add_argument("--coded", default=str(V62 / "data/coded"), help="dir with fr/ and ja/ coded tables")
    ap.add_argument("--rank-status", default="NOT RESOLVED")
    ap.add_argument("--out", default=str(VERDICTS))
    a = ap.parse_args(argv)
    if not a.run:
        ap.error("only --run is available; the tests exercise score() on synthetic data")
    if Path(a.out).exists():
        sys.exit(f"REFUSED: {a.out} exists (the scoring runs once)")
    if not tag_on_origin():
        sys.exit(f"REFUSED: tag {PREREG_TAG} is not on origin")
    en = read_english(a.english)
    lang_B = {lg: read_coded_b(Path(a.coded) / lg) for lg in LANGS}
    v = score(sorted(en), en, lang_B, rank_status=a.rank_status)
    Path(a.out).write_text(json.dumps(_clean(v), indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: t.get("verdict") for k, t in v["tests"].items()}, indent=1), v["joint_reading"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
