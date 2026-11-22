#!/usr/bin/env python3
"""score_v0_46.py -- AIAS(TM) v0.46 (#76) scorer (Stage 1 code r1; stage1_manuscript_r2.md sections 2, 5.1-5.8).

Computes, from CODED choice records (code_v0_46.py) and a PREDICTOR table (P, R* per unit), every
pre-registered statistic: H1 (U_P, LIST), H2 (U_P, OPEN), H3 (U_R, LIST, rated units), H4 (conditional logit,
OR_R, Freedman-Lane p), H5 (d-bar, randomisation p, labels), the outcome-neutral checks (MC_*), the
sensitivities (S-COI, S-Recall, S-LOCO, S-Model, S-Pos-a, S-Pos-b, S-Panel) and descriptives 1-4 and 7 (5 when
per-model recall is supplied; 6, refusals and cannot-buy hedges, and 8, answer form and cost, when the raw answer
lines are supplied, r2). Verdict rules exactly as section 2; seeds as section 5.1.

The scorer joins predictors to choices only here, after coding (blinding, section 5.3). NO MODEL IS CALLED.

The predictor table is computed from the raw predictor answers by predictors_v0_46.py (v1.14's code at 3129674,
r2), certified by the code-parity gates G1, G2 (gates_v0_46.py). This script takes the table as input;
`presence_P` and `modal_position` below are the formulas, for tests.

Usage:
  python3 osf/v46/scripts/score_v0_46.py --synthetic [--squares 2] [--draws-scale 0.1]   # synthetic world
  python3 osf/v46/scripts/score_v0_46.py --coded CODED.jsonl --predictors PRED.csv --out RESULTS.json
"""
import argparse
import csv
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import rankdata

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_probes_v0_46 as B  # noqa: E402

SEEDS = {"H1": 460001, "H2": 460002, "H3": 460003, "H4": 460004, "BOOT": 460005, "H5": 460006}
N_PERM = 10_000          # H1-H3 permutation draws
N_FL = 2_000             # H4 Freedman-Lane draws
N_BOOT = 10_000
N_RAND = 10_000          # H5 randomisation draws
CI = (5.0, 95.0)         # 90% percentile interval
EPS = 1e-12
U_CONF, U_FALS = 0.70, 0.60
OR_CONF, OR_FALS = 1.25, 1.05
ALPHA = 0.05
ROBUST_BAND = (0.45, 0.55)
MIN_VALID = {"H1": 450, "H2": 120, "H3": 200, "H4": 200}
MIN_VALID_NO_SPIRITS = {"H1": 331, "H2": 90, "H3": 147, "H4": 147}
DESIGNED = {"LIST": 182, "OPEN": 72}                 # per model (section 5.4)
DESIGNED_NO_SPIRITS = {"LIST": 134, "OPEN": 54}      # DECISION NEEDED: 2 x 67 live units; 3 categories x 18
ANSWERED_MIN, CODABLE_MIN, CODABLE_FLAG = 0.90, 0.70, 0.85
MIN_RATED_UNITS = 5                                  # H3 (and, DECISION NEEDED, H4): categories entering
RATING_FLOOR = 6
COI_UNITS = {("cars", "Chevrolet"), ("cars", "BMW"), ("cars", "Bentley"), ("spirits", "Jack Daniel's"),
             ("skincare", "Eucerin")}
# DECISION NEEDED (codable): section 5.4 drops a model x condition with < 70% of answers "codable"; MC_Codable
# counts "a valid choice". With 30% OTHER assumed in OPEN (A5), "valid" would drop most models from H2, which
# the power analysis (UNDETERMINED <= 0.7%) does not do. Codable here = a choice was coded to a brand or to
# OTHER/OFF_LIST/DEFUNCT; AMBIGUOUS, NONE and MISSING are not codable.
CODABLE = {"VALID", "OTHER", "OFF_LIST", "DEFUNCT"}


# =========================================================================== predictor formulas (for tests)
def presence_P(recognized_by_model, pi_hat):
    """P = 100 (C_P/3 + 2 pi_hat)/3; C_P/3 = share of models with a coded answer that code b recognised
    (v1.14 comparators). recognized_by_model: list of 0/1/None."""
    coded = [int(x) for x in recognized_by_model if x is not None]
    if pi_hat is None or not coded:
        return None
    return 100.0 * (sum(coded) / len(coded) + 2.0 * pi_hat) / 3.0


def modal_position(kmins):
    """v1.14 `modal_position` (copied): R* = -(smallest modal k_min). Higher = nearer the top."""
    k = np.asarray(list(kmins), int)
    if not len(k):
        return float("nan")
    vals, cnt = np.unique(k, return_counts=True)
    return float(-vals[cnt == cnt.max()].min())


def ranking_rstar(kmins, floor=RATING_FLOOR):
    """R* if the unit has at least `floor` rankable mentions, else None (unrated)."""
    k = list(kmins)
    return modal_position(k) if len(k) >= floor else None


# =========================================================================== inputs
def mkey(r):
    return r.get("model") or r.get("model_slot")


def read_jsonl(path):
    return [json.loads(ln) for ln in open(path, encoding="utf-8") if ln.strip()]


def read_predictors(path):
    """CSV with columns category, brand, P, R_star[, pi_hat]; empty = not available."""
    out = {}
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            def num(v):
                return None if v in (None, "", "NA", "None") else float(v)
            out[(r["category"], r["brand"])] = {"P": num(r.get("P")), "R_star": num(r.get("R_star")),
                                               "pi_hat": num(r.get("pi_hat"))}
    return out


# =========================================================================== percentiles and U
def percentiles(pred, units, key):
    """u_X(b) = (average rank of X_b among `units` - 0.5) / len(units); units with X None are left out."""
    us = [b for b in units if pred.get(b, {}).get(key) is not None]
    if not us:
        return {}
    x = np.array([pred[b][key] for b in us], float)
    r = rankdata(x)
    return {b: (ri - 0.5) / len(us) for b, ri in zip(us, r)}


def base_units(cfg, cat, key):
    live = [b for b in cfg["live"][cat] if (cat, b) not in cfg["drop_units"]]
    if key == "R_star":
        live = [b for b in live if cfg["pred"].get((cat, b), {}).get("R_star") is not None]
    return live


def utable(cfg, key, rated_only=False):
    """{cat: {brand: u}} over the categories in cfg; for R*, among rated live units."""
    out = {}
    for cat in cfg["cats"]:
        units = base_units(cfg, cat, "R_star" if (key == "R_star" or rated_only) else key)
        pk = {b: cfg["pred"].get((cat, b), {}) for b in units}
        out[cat] = percentiles(pk, units, key)
    return out


def u_test(choices, ut, seed, n_perm=N_PERM, n_boot=N_BOOT):
    """choices: list of (cat, unit, model). Ū, one-sided within-category permutation p, 90% bootstrap CI."""
    choices = [c for c in choices if c[1] in ut.get(c[0], {})]
    n = len(choices)
    if n == 0:
        return {"U": None, "p": None, "ci90": None, "n": 0}
    obs = sum(ut[c][b] for c, b, _m in choices) / n
    rng = np.random.default_rng(seed)
    null = np.zeros(n_perm)
    for cat in sorted(ut):
        units = sorted(ut[cat])
        if not units:
            continue
        cnt = Counter(b for c, b, _m in choices if c == cat)
        cvec = np.array([cnt.get(b, 0) for b in units], float)
        if cvec.sum() == 0:
            continue
        uvec = np.array([ut[cat][b] for b in units])
        idx = rng.permuted(np.tile(np.arange(len(units)), (n_perm, 1)), axis=1)
        null += (uvec[idx] * cvec).sum(axis=1)
    null /= n
    p = (1 + int((null >= obs - EPS).sum())) / (n_perm + 1)
    ci = bootstrap_mean([(c, m, ut[c][b]) for c, b, m in choices], n_boot)
    return {"U": obs, "p": p, "ci90": ci, "n": n}


def bootstrap_mean(items, n_boot=N_BOOT, seed=SEEDS["BOOT"]):
    """items: (cat, model, value). Resample within (category, model) strata; 90% percentile interval of the mean.
    DECISION NEEDED: every interval starts a fresh generator at seed 460005; strata resample the valid choices."""
    if not items or n_boot <= 0:
        return None
    rng = np.random.default_rng(seed)
    strata = defaultdict(list)
    for c, m, v in items:
        strata[(c, m)].append(v)
    tot = np.zeros(n_boot)
    for k in sorted(strata):
        v = np.asarray(strata[k], float)
        tot += v[rng.integers(0, len(v), (n_boot, len(v)))].sum(axis=1)
    est = tot / len(items)
    return [float(np.percentile(est, CI[0])), float(np.percentile(est, CI[1]))]


def verdict_u(res, undetermined):
    if undetermined or res["U"] is None:
        return "UNDETERMINED"
    if res["U"] >= U_CONF and res["p"] < ALPHA:
        return "CONFIRMED"
    if res["U"] < U_FALS:
        return "FALSIFIED"
    return "MARGINAL"


def verdict_or(res, undetermined):
    if undetermined or res.get("OR_R") is None:
        return "UNDETERMINED"
    if res["OR_R"] >= OR_CONF and res["p"] < ALPHA:
        return "CONFIRMED"
    if res["OR_R"] < OR_FALS:
        return "FALSIFIED"
    return "MARGINAL"


# =========================================================================== conditional logit
def clogit_fit(X, mask, y, beta0=None, iters=60, tol=1e-10):
    """X (n, J, k), mask (n, J) bool, y (n,) chosen option index. Newton-Raphson MLE. Returns (beta, se, conv)."""
    n, J, k = X.shape
    beta = np.zeros(k) if beta0 is None else np.array(beta0, float)
    conv = False
    rows = np.arange(n)
    for _ in range(iters):
        eta = np.where(mask, X @ beta, -np.inf)
        eta -= eta.max(axis=1, keepdims=True)
        p = np.exp(eta)
        p /= p.sum(axis=1, keepdims=True)
        xbar = np.einsum("nj,njk->nk", p, X)
        g = (X[rows, y] - xbar).sum(axis=0)
        H = np.einsum("nj,njk,njl->kl", p, X, X) - xbar.T @ xbar
        try:
            step = np.linalg.solve(H + 1e-12 * np.eye(k), g)
        except np.linalg.LinAlgError:
            step = np.linalg.lstsq(H, g, rcond=None)[0]
        beta = beta + step
        if np.max(np.abs(step)) < tol:
            conv = True
            break
    try:
        se = np.sqrt(np.diag(np.linalg.inv(H)))
    except np.linalg.LinAlgError:
        se = np.full(k, np.nan)
    return beta, se, conv


def zscore(d):
    """{b: v} -> {b: (v - mean)/sd} (population sd; sd 0 -> 0)."""
    if not d:
        return {}
    v = np.array(list(d.values()), float)
    sd = v.std()
    return {b: ((x - v.mean()) / sd if sd > 0 else 0.0) for b, x in d.items()}


def _design(calls, feats, pos_terms=True):
    """calls: list of (cat, chosen, order); feats: {cat: {brand: [features]}} (only brands in feats are options).
    Returns X, mask, y and the per-option metadata needed to rebuild X."""
    J = max(len(o) for _c, _b, o in calls)
    kf = len(next(iter(next(iter(feats.values())).values())))
    k = kf + (3 if pos_terms else 0)
    X = np.zeros((len(calls), J, k))
    mask = np.zeros((len(calls), J), bool)
    y = np.zeros(len(calls), int)
    for i, (cat, chosen, order) in enumerate(calls):
        L = len(order)
        j = 0
        for pos, b in enumerate(order, start=1):
            if b not in feats[cat]:
                continue
            row = list(feats[cat][b])
            if pos_terms:
                row += [1.0 if pos == 1 else 0.0, 1.0 if pos == L else 0.0, (pos - 1) / (L - 1)]
            X[i, j] = row
            mask[i, j] = True
            if b == chosen:
                y[i] = j
            j += 1
    return X, mask, y


def h4_test(cfg, list_valid, n_fl=N_FL, seed=SEEDS["H4"]):
    """Conditional logit on rated live units: beta_P z(u_P) + beta_R z(u_R) + gamma_1 first + gamma_L last +
    gamma_d (pos-1)/(L-1); z within category over rated live units. One-sided Freedman-Lane p for beta_R."""
    uP = utable(cfg, "P")
    uR = utable(cfg, "R_star")
    cats = [c for c in cfg["cats"] if len(uR.get(c, {})) >= MIN_RATED_UNITS]
    zP, zR, fit_parts = {}, {}, {}
    for c in cats:
        rated = sorted(uR[c])
        zP[c] = zscore({b: uP[c][b] for b in rated if b in uP[c]})
        zR[c] = zscore({b: uR[c][b] for b in rated})
        bs = [b for b in rated if b in zP[c]]
        a = np.array([uP[c][b] for b in bs])
        r = np.array([uR[c][b] for b in bs])
        A = np.column_stack([np.ones(len(a)), a])
        coef = np.linalg.lstsq(A, r, rcond=None)[0]
        fit_parts[c] = (bs, A @ coef, r - A @ coef)
    calls = [(c, b, o) for c, b, _m, o in list_valid if c in cats and b in zR[c] and b in zP[c]]
    if len(calls) < 2:
        return {"n": len(calls), "OR_R": None, "beta_R": None, "p": None, "categories": cats}
    feats = {c: {b: [zP[c][b], zR[c][b]] for b in zR[c] if b in zP[c]} for c in cats}
    X, mask, y = _design(calls, feats)
    beta, se, conv = clogit_fit(X, mask, y)
    rng = np.random.default_rng(seed)
    hits = 0
    # map each option cell to a flat (cat, brand) index so the R column can be rebuilt per draw
    flat = [(c, b) for c in cats for b in fit_parts[c][0]]
    fidx = {cb: i for i, cb in enumerate(flat)}
    cell = np.zeros(mask.shape, int)
    for i, (cat, _b, order) in enumerate(calls):
        j = 0
        for b in order:
            if b in feats[cat]:
                cell[i, j] = fidx[(cat, b)]
                j += 1
    null = np.zeros(n_fl)
    Xs = X.copy()
    for d in range(n_fl):
        zr_vec = np.zeros(len(flat))
        for c in cats:
            bs, fitted, resid = fit_parts[c]
            ur_star = fitted + resid[rng.permutation(len(resid))]
            sd = ur_star.std()
            zs = (ur_star - ur_star.mean()) / sd if sd > 0 else np.zeros(len(bs))
            for b, z in zip(bs, zs):
                zr_vec[fidx[(c, b)]] = z
        Xs[:, :, 1] = np.where(mask, zr_vec[cell], 0.0)
        bs_, _se, _cv = clogit_fit(Xs, mask, y, beta0=beta, iters=25, tol=1e-8)
        null[d] = bs_[1]
        hits += int(bs_[1] >= beta[1] - EPS)
    p = (1 + hits) / (n_fl + 1)
    names = ["beta_P", "beta_R", "gamma_1", "gamma_L", "gamma_d"]
    return {"n": len(calls), "categories": cats, "converged": bool(conv),
            "coef": dict(zip(names, map(float, beta))), "se": dict(zip(names, map(float, se))),
            "beta_R": float(beta[1]), "OR_R": float(math.exp(beta[1])), "p": p}


def position_logit(cfg, list_valid, key="P"):
    """S-Pos-b and H5's position terms: P only (z within category over live units) + position terms,
    on all valid LIST choices, choice set = the full list."""
    uP = utable(cfg, key)
    feats = {c: {b: [v] for b, v in zscore(uP[c]).items()} for c in cfg["cats"] if uP.get(c)}
    calls = [(c, b, o) for c, b, _m, o in list_valid if c in feats and b in feats[c]]
    if len(calls) < 2:
        return {"n": len(calls)}
    X, mask, y = _design(calls, feats)
    beta, se, conv = clogit_fit(X, mask, y)
    names = ["beta_P", "gamma_1", "gamma_L", "gamma_d"]
    return {"n": len(calls), "converged": bool(conv), "coef": dict(zip(names, map(float, beta))),
            "se": dict(zip(names, map(float, se))), "OR_P_per_SD": float(math.exp(beta[0]))}


# =========================================================================== H5
def h5_test(list_valid_full, n_rand=N_RAND, n_boot=N_BOOT, seed=SEEDS["H5"]):
    """list_valid_full: (cat, unit, model, brief, order). d-bar; randomisation test within (cat, model, brief):
    the orders of that stratum's valid calls are reassigned at random. DECISION NEEDED: (i) the orders reassigned
    are those of the stratum's VALID calls; (ii) two-sided p is centred on the randomisation null's mean."""
    if not list_valid_full:
        return {"n": 0, "d_bar": None, "p": None, "label": "inconclusive"}
    d = [(o.index(b)) / (len(o) - 1) for _c, b, _m, _br, o in list_valid_full]
    n = len(d)
    obs = float(np.mean(d))
    strata = defaultdict(list)
    for c, b, m, br, o in list_valid_full:
        strata[(c, m, br)].append((b, o))
    rng = np.random.default_rng(seed)
    null = np.zeros(n_rand)
    for k in sorted(strata):
        items = strata[k]
        M = np.array([[o.index(b) / (len(o) - 1) for _b2, o in items] for b, _o in items])   # call i x order j
        idx = rng.permuted(np.tile(np.arange(len(items)), (n_rand, 1)), axis=1)
        null += M[np.arange(len(items))[None, :], idx].sum(axis=1)
    null /= n
    m0 = null.mean()
    p = (1 + int((np.abs(null - m0) >= abs(obs - m0) - EPS).sum())) / (n_rand + 1)
    ci = bootstrap_mean([(c, m, di) for (c, _b, m, _br, _o), di in zip(list_valid_full, d)], n_boot)
    if p < ALPHA:
        label = "order-sensitive"
    elif ci is not None and ROBUST_BAND[0] <= ci[0] and ci[1] <= ROBUST_BAND[1]:
        label = "order-robust"
    else:
        label = "inconclusive"
    Ls = [len(o) for *_x, o in list_valid_full]
    pos = [o.index(b) + 1 for _c, b, _m, _br, o in list_valid_full]
    share1 = float(np.mean([q == 1 for q in pos]))
    terc = Counter(min(2, int(3 * (q - 1) / L)) for q, L in zip(pos, Ls))
    return {"n": n, "d_bar": obs, "p": p, "ci90": ci, "null_mean": float(m0), "label": label,
            "PR1": share1 * float(np.mean(Ls)), "share_pos1": share1,
            "tercile_shares": {t: terc.get(i, 0) / n for i, t in enumerate(("first", "middle", "last"))}}


# =========================================================================== exclusions, drops, checks
def drop_rules(coded, cfg):
    """Model x condition drops (section 5.4). Returns {cond: {model: reason}} and the per-model shares."""
    designed = DESIGNED_NO_SPIRITS if cfg["spirits_out"] else DESIGNED
    shares, drops = {}, {"LIST": {}, "OPEN": {}}
    for cond in ("LIST", "OPEN"):
        for m in cfg["models"]:
            rs = [r for r in coded if r["condition"] == cond and mkey(r) == m and r["category"] in cfg["cats"]]
            answered = [r for r in rs if r["code"] != "MISSING"]
            codable = [r for r in answered if r["code"] in CODABLE]
            valid = [r for r in answered if r["code"] == "VALID"]
            a_sh = len(answered) / designed[cond]
            c_sh = len(codable) / len(answered) if answered else 0.0
            shares[(cond, m)] = {"answered": len(answered), "answered_share": a_sh, "codable_share": c_sh,
                                 "valid_share": len(valid) / len(answered) if answered else 0.0}
            if a_sh < ANSWERED_MIN:
                drops[cond][m] = "answered < 90%"
            elif c_sh < CODABLE_MIN:
                drops[cond][m] = "codable < 70%"
    for m, sh in (cfg.get("predictor_answered") or {}).items():
        if sh < ANSWERED_MIN:
            drops["LIST"][m] = drops["OPEN"][m] = "predictor blocks < 90% answered"
    return drops, shares


def checks(coded, cfg, shares):
    out = {}
    out["MC_Codable"] = {f"{c}/{m}": {"valid_share": round(v["valid_share"], 4),
                                      "flag": v["valid_share"] < CODABLE_FLAG} for (c, m), v in shares.items()}
    lst = [r for r in coded if r["condition"] == "LIST" and r["code"] != "MISSING"]
    opn = [r for r in coded if r["condition"] == "OPEN" and r["code"] != "MISSING"]
    off = sum(r["code"] == "OFF_LIST" for r in lst) / len(lst) if lst else None
    dfn = sum(r["code"] == "DEFUNCT" for r in opn) / len(opn) if opn else None
    out["MC_OnList"] = {"off_list_share": off, "flag": off is not None and off > 0.05}
    out["MC_Defunct"] = {"defunct_share_open": dfn, "flag": dfn is not None and dfn > 0.02}
    n_choice = len(coded)
    answered = sum(r["code"] != "MISSING" for r in coded)
    out["MC_Complete_choice_part"] = {"answered": answered, "designed": 762, "share": answered / 762,
                                      "pass": answered / 762 >= 0.98, "records": n_choice,
                                      "note": "predictor part (504 calls) checked from the raw file, not here"}
    tr = defaultdict(lambda: [0, 0])
    for r in coded:
        if r["code"] != "MISSING" or r.get("reason") == "cut_at_limit":
            t = tr[f"{r['condition']}/{mkey(r)}"]
            t[0] += int(bool(r.get("at_limit")))
            t[1] += 1
    out["MC_Truncation"] = {k: {"share": v[0] / v[1], "flag": v[0] / v[1] > 0.05} for k, v in sorted(tr.items())}
    mp = {}
    for c in cfg["cats"]:
        P = [cfg["pred"][(c, b)]["P"] for b in cfg["live"][c] if cfg["pred"].get((c, b), {}).get("P") is not None]
        iqr = float(np.percentile(P, 75) - np.percentile(P, 25)) if P else None
        all_rec = (cfg.get("recalled_by_all") or {}).get(c)
        mp[c] = {"IQR_P": iqr, "recalled_by_every_model": all_rec,
                 "flag": (iqr is None or iqr < 10) or (all_rec is False)}
    out["MC_Predictor"] = mp
    out["refusals"] = sum(r.get("reason") == "refusal" for r in coded)
    out["exclusions"] = {f"{k[0]}/{k[1]}/{k[2]}/{k[3]}": v for k, v in sorted(Counter(
        (r["condition"], mkey(r), r["category"], r["code"]) for r in coded if r["code"] != "VALID").items())}
    return out


# =========================================================================== the tests
def make_cfg(pred, models, live=None, cats=None, drop_units=(), key_P="P", **kw):
    live = live or B.live_units()
    spirits_out = not any((pred.get(("spirits", b)) or {}).get("P") is not None for b in live["spirits"])
    cats = list(cats or [c for c, _s, _i in B.CATEGORIES])
    if spirits_out and "spirits" in cats:
        cats.remove("spirits")
    p2 = pred
    if key_P != "P":   # S-Recall: pi_hat in place of P
        p2 = {u: dict(v, P=v.get(key_P)) for u, v in pred.items()}
    return dict(pred=p2, models=list(models), live=live, cats=cats, drop_units=set(drop_units),
                spirits_out=spirits_out, **kw)


def run_tests(coded, cfg, draws=1.0, apply_minimum=True, drops=None, pos_a=False):
    """H1-H5 on the coded records under cfg. draws scales every draw count (1.0 = pre-registered)."""
    npm, nfl, nbt, nrd = (max(1, int(N_PERM * draws)), max(1, int(N_FL * draws)), max(0, int(N_BOOT * draws)),
                          max(1, int(N_RAND * draws)))
    if drops is None:
        drops, _ = drop_rules(coded, cfg)
    mins = MIN_VALID_NO_SPIRITS if cfg["spirits_out"] else MIN_VALID
    ok = [r for r in coded if r["code"] == "VALID" and r["category"] in cfg["cats"] and mkey(r) in cfg["models"]
          and (r["category"], r["unit"]) not in cfg["drop_units"] and r["unit"] in cfg["live"][r["category"]]]
    lst = [r for r in ok if r["condition"] == "LIST"]
    opn = [r for r in ok if r["condition"] == "OPEN"]
    if pos_a:   # S-Pos-a: choices of the brand shown first or last are left out
        lst = [r for r in lst if 1 < r["position"] < r["L"]]
    dl, do = bool(drops["LIST"]), bool(drops["OPEN"])
    uP, uR = utable(cfg, "P"), utable(cfg, "R_star")
    res = {}
    h1 = u_test([(r["category"], r["unit"], mkey(r)) for r in lst], uP, SEEDS["H1"], npm, nbt)
    h1["verdict"] = verdict_u(h1, dl or (apply_minimum and h1["n"] < mins["H1"]))
    res["H1"] = h1
    if not pos_a:
        h2 = u_test([(r["category"], r["unit"], mkey(r)) for r in opn], uP, SEEDS["H2"], npm, nbt)
        h2["verdict"] = verdict_u(h2, do or (apply_minimum and h2["n"] < mins["H2"]))
        res["H2"] = h2
    uR3 = {c: v for c, v in uR.items() if len(v) >= MIN_RATED_UNITS}
    h3 = u_test([(r["category"], r["unit"], mkey(r)) for r in lst], uR3, SEEDS["H3"], npm, nbt)
    h3["categories"] = sorted(uR3)
    h3["verdict"] = verdict_u(h3, dl or (apply_minimum and h3["n"] < mins["H3"]))
    res["H3"] = h3
    if pos_a:
        return res
    lv = [(r["category"], r["unit"], mkey(r), r["order"]) for r in lst]
    h4 = h4_test(cfg, lv, nfl)
    h4["verdict"] = verdict_or(h4, dl or (apply_minimum and h4["n"] < mins["H4"]))
    res["H4"] = h4
    h5 = h5_test([(r["category"], r["unit"], mkey(r), r["brief"], r["order"]) for r in lst], nrd, nbt)
    if dl:
        h5["label"] = "UNDETERMINED (model dropped)"
    h5["position_terms_P_only"] = position_logit(cfg, lv)
    res["H5"] = h5
    return res


def sensitivities(coded, cfg, drops, draws):
    """Section 5.8. DECISION NEEDED: in sensitivities the minimum-valid-choice rule is not applied (S-Model
    and S-LOCO could never reach 450); the effect-size and p rules are."""
    s = {}
    kw = dict(draws=draws, apply_minimum=False, drops={"LIST": {}, "OPEN": {}})
    s["S-COI"] = run_tests(coded, dict(cfg, drop_units=cfg["drop_units"] | COI_UNITS), **kw)
    if any(v.get("pi_hat") is not None for v in cfg["pred"].values()):
        s["S-Recall"] = run_tests(coded, dict(cfg, pred={u: dict(v, P=v.get("pi_hat"))
                                                          for u, v in cfg["pred"].items()}), **kw)
    for c in cfg["cats"]:
        s[f"S-LOCO-{c}"] = run_tests(coded, dict(cfg, cats=[x for x in cfg["cats"] if x != c]), **kw)
    for m in cfg["models"]:
        s[f"S-Model-{m}"] = run_tests(coded, dict(cfg, models=[m]), **kw)
    s["S-Pos-a"] = run_tests(coded, cfg, pos_a=True, **kw)
    lst = [(r["category"], r["unit"], mkey(r), r["order"]) for r in coded if r["code"] == "VALID"
           and r["condition"] == "LIST" and r["category"] in cfg["cats"] and mkey(r) in cfg["models"]]
    s["S-Pos-b"] = position_logit(cfg, lst)
    dropped = set(drops["LIST"]) | set(drops["OPEN"])
    if dropped:
        s["S-Panel"] = run_tests(coded, dict(cfg, models=[m for m in cfg["models"] if m not in dropped]), **kw)
    return s


def descriptives(coded, cfg):
    d = {}
    ok = [r for r in coded if r["code"] == "VALID" and r["category"] in cfg["cats"]]
    d["1_choice_shares"] = {f"{c}/{cond}/{br}/{m}/{u}": n for (c, cond, br, m, u), n in sorted(Counter(
        (r["category"], r["condition"], r["brief"], mkey(r), r["unit"]) for r in ok).items())}
    top5 = {}
    for c in cfg["cats"]:
        for m in cfg["models"]:
            cnt = Counter(r["unit"] for r in ok if r["category"] == c and mkey(r) == m)
            top5[f"{c}/{m}"] = cnt.most_common(5)
    d["1_top5"] = top5
    opn = [r for r in coded if r["condition"] == "OPEN" and r["code"] != "MISSING" and r["category"] in cfg["cats"]]
    d["2_open_other_share"] = sum(r["code"] == "OTHER" for r in opn) / len(opn) if opn else None
    d["2_open_other_top10"] = {c: Counter(r["other_text"] for r in opn if r["category"] == c and
                                          r["code"] == "OTHER").most_common(10) for c in cfg["cats"]}

    def modal(rs):
        cnt = Counter(r["unit"] for r in rs)
        if not cnt:
            return None
        top = max(cnt.values())
        return sorted(u for u, v in cnt.items() if v == top)[0]   # DECISION NEEDED: ties -> alphabetical first
    same, tot = 0, 0
    for c in cfg["cats"]:
        for br in B.BRIEF_IDS:
            for m in cfg["models"]:
                ml = modal([r for r in ok if r["condition"] == "LIST" and r["category"] == c and
                            r["brief"] == br and mkey(r) == m])
                for r in ok:
                    if r["condition"] == "OPEN" and r["category"] == c and r["brief"] == br and mkey(r) == m:
                        tot += 1
                        same += int(r["unit"] == ml)
    d["2_open_equals_modal_list"] = same / tot if tot else None
    agree = {}
    for cond in ("LIST", "OPEN"):
        cells = [(c, br) for c in cfg["cats"] for br in B.BRIEF_IDS]
        hits = 0
        for c, br in cells:
            mods = [modal([r for r in ok if r["condition"] == cond and r["category"] == c and r["brief"] == br
                           and mkey(r) == m]) for m in cfg["models"]]
            hits += int(None not in mods and len(set(mods)) == 1)
        agree[cond] = hits / len(cells)
    d["3_model_agreement"] = agree
    uP = utable(cfg, "P")
    d["4_U_P_by_brief"] = {f"{cond}/{br}": (float(np.mean(v)) if v else None) for cond in ("LIST", "OPEN")
                           for br in B.BRIEF_IDS for v in [[uP[r["category"]][r["unit"]] for r in ok
                           if r["condition"] == cond and r["brief"] == br and r["unit"] in uP[r["category"]]]]}
    own = cfg.get("pi_hat_by_model")
    if own:
        o = {}
        for m in cfg["models"]:
            cm = make_cfg({u: {"P": own.get(m, {}).get(u)} for u in cfg["pred"]}, [m], cfg["live"], cfg["cats"])
            um = utable(cm, "P")
            for cond in ("LIST", "OPEN"):
                v = [um[r["category"]][r["unit"]] for r in ok if mkey(r) == m and r["condition"] == cond
                     and r["unit"] in um.get(r["category"], {})]
                o[f"{m}/{cond}"] = float(np.mean(v)) if v else None
        d["5_own_model_link"] = o
    conc = {}
    for cond in ("LIST", "OPEN"):
        for c in cfg["cats"]:
            cnt = Counter(r["unit"] for r in ok if r["condition"] == cond and r["category"] == c)
            n = sum(cnt.values())
            if n:
                sh = np.array(sorted(cnt.values(), reverse=True)) / n
                conc[f"{cond}/{c}"] = {"top3_share": float(sh[:3].sum()), "HHI": float((sh ** 2).sum()),
                                       "distinct": len(cnt)}
    d["7_concentration"] = conc
    d["6_refusals"] = sum(r.get("reason") == "refusal" for r in coded)
    return d


# =========================================================================== descriptives 6 and 8 (need raw answers)
# Section 5.7, 6: "share of answers that decline to choose, or choose while saying the model cannot buy".
# DECISION (operationalisation, deterministic, no model): DECLINE = an answered choice call coded NONE (a refusal or
# no codable choice); HEDGE = an answered call with a choice (VALID, OTHER, OFF_LIST, DEFUNCT, AMBIGUOUS) whose text
# matches CANNOT_BUY_RE (the model says it cannot itself buy / purchase / order). Patterns fixed here, before data.
CANNOT_BUY_RE = re.compile(
    r"\bi(?:['’]m|\s+am)?\s+"
    r"(?:can(?:no|['’])t|can\s+not|could(?:n['’]t|\s+not)|(?:am\s+)?not\s+able\s+to|(?:am\s+)?unable\s+to|"
    r"(?:don['’]t|do\s+not)\s+have\s+(?:the\s+)?(?:ability|means|way)\s+to|have\s+no\s+way\s+to)\s+"
    r"(?:actually\s+|personally\s+|directly\s+|physically\s+)?"
    r"(?:buy|purchase|order|make\s+(?:a\s+|the\s+|any\s+)?purchases?|complete\s+(?:a\s+|the\s+)?purchase|check\s*out)\b"
    r"|\bas\s+an\s+ai\b[^.\n]{0,80}\b(?:buy|purchase|order|shop)",
    re.I)
CHOSEN_CODES = {"VALID", "OTHER", "OFF_LIST", "DEFUNCT", "AMBIGUOUS"}
WORD_RE = re.compile(r"\S+")


def _answered(r):
    return r.get("status", "ok") == "ok" and bool((r.get("text") or "").strip()) and not r.get("error")


def final_answers(raw):
    """One raw line per call_id: the last answered attempt, else the last attempt (= v0.42 dedupe_calls)."""
    best = {}
    for r in raw:
        cid = r.get("call_id")
        if cid is None:
            continue
        if cid not in best or _answered(r) or not _answered(best[cid]):
            best[cid] = r
    return best


def _summ(v):
    v = [x for x in v if x is not None]
    if not v:
        return {"n": 0, "mean": None, "median": None, "sum": 0}
    a = np.asarray(v, float)
    return {"n": int(a.size), "mean": float(a.mean()), "median": float(np.median(a)), "sum": float(a.sum())}


def descriptive_6(coded, raw):
    """Per model x condition: answered calls, declines (NONE; refusals among them) and cannot-buy hedges."""
    fin = final_answers(raw)
    acc = defaultdict(lambda: {"answered": 0, "decline": 0, "refusal": 0, "hedge": 0})
    for c in coded:
        if c.get("condition") not in ("OPEN", "LIST") or c.get("code") == "MISSING":
            continue
        r = fin.get(c.get("call_id"), {})
        a = acc[f"{mkey(c)}/{c['condition']}"]
        a["answered"] += 1
        if c["code"] == "NONE":
            a["decline"] += 1
            a["refusal"] += int(c.get("reason") == "refusal")
        elif c["code"] in CHOSEN_CODES and CANNOT_BUY_RE.search(r.get("text") or ""):
            a["hedge"] += 1
    out = {}
    for k, a in sorted(acc.items()):
        n = a["answered"]
        out[k] = dict(a, decline_share=a["decline"] / n if n else None, hedge_share=a["hedge"] / n if n else None)
    tot = {f: sum(a[f] for a in acc.values()) for f in ("answered", "decline", "refusal", "hedge")}
    out["all"] = dict(tot, decline_share=tot["decline"] / tot["answered"] if tot["answered"] else None,
                      hedge_share=tot["hedge"] / tot["answered"] if tot["answered"] else None)
    return out


def descriptive_8(raw):
    """Answer form and cost. Per model x block (and x condition for choice blocks), over each call's final answered
    line: words per answer (whitespace tokens of the visible text), output and thinking tokens. Spend per model x
    block: the recorded cost_usd of EVERY raw line (every billed attempt, re-sends included), as the guard counts it.
    DECISION: lines without cost_usd are counted in `lines_without_cost`, never imputed."""
    fin = final_answers(raw)
    form = defaultdict(lambda: {"words": [], "output_tokens": [], "thinking_tokens": []})
    for r in fin.values():
        if not _answered(r):
            continue
        m = r.get("model") or r.get("model_requested")
        for k in (f"{m}/{r.get('block')}", f"{m}/{r.get('part')}/{r.get('condition')}"):
            form[k]["words"].append(len(WORD_RE.findall(r.get("text") or "")))
            form[k]["output_tokens"].append(r.get("output_tokens"))
            form[k]["thinking_tokens"].append(r.get("thinking_tokens"))
    spend = defaultdict(lambda: {"usd": 0.0, "lines": 0, "lines_without_cost": 0})
    for r in raw:
        m = r.get("model") or r.get("model_requested")
        for k in (f"{m}/{r.get('block')}", f"{m}/ALL"):
            s = spend[k]
            s["lines"] += 1
            if isinstance(r.get("cost_usd"), (int, float)):
                s["usd"] += float(r["cost_usd"])
            else:
                s["lines_without_cost"] += 1
    total = sum(float(r["cost_usd"]) for r in raw if isinstance(r.get("cost_usd"), (int, float)))
    return {"form": {k: {f: _summ(v[f]) for f in v} for k, v in sorted(form.items())},
            "spend": {k: dict(v, usd=round(v["usd"], 6)) for k, v in sorted(spend.items())},
            "spend_total_usd": round(total, 6), "raw_lines": len(raw), "calls": len(fin)}


def score(coded, pred, models=None, draws=1.0, with_sens=True, raw=None, **cfg_kw):
    """raw: the raw answer lines (acquire_v0_46.py output), needed for descriptives 6 (hedges) and 8."""
    models = models or sorted({mkey(r) for r in coded})
    cfg = make_cfg(pred, models, **cfg_kw)
    drops, shares = drop_rules(coded, cfg)
    out = {"phase": B.PHASE, "models": models, "categories": cfg["cats"], "spirits_left_out": cfg["spirits_out"],
           "draws_scale": draws, "drops": drops,
           "shares": {f"{k[0]}/{k[1]}": v for k, v in shares.items()}}
    out["checks"] = checks(coded, cfg, shares)
    out["tests"] = run_tests(coded, cfg, draws=draws, drops=drops)
    if with_sens:
        out["sensitivities"] = sensitivities(coded, cfg, drops, draws)
    out["descriptives"] = descriptives(coded, cfg)
    if raw is not None:
        out["descriptives"]["6_refusals_hedges"] = descriptive_6(coded, raw)
        out["descriptives"]["8_answer_form_and_cost"] = descriptive_8(raw)
    return out


# =========================================================================== synthetic world (known truth)
def synth_world(seed=4607, squares=2, beta_P=1.5, beta_R=0.5, gamma_1=0.7, open_other=0.3, n_models=3,
                rated_share=0.6, r_PR=0.4, scale=1.0, as_text=False):
    """A world whose true effects are known. Units: the real live units. P ~ U(0, 100); R* defined for the
    top `rated_share` of units by P, correlated r_PR with P. Each LIST call chooses by a logit on
    scale * (beta_P zL(u_P) + beta_R zR(u_R) [rated units only] + gamma_1 [shown first]), zL over live units,
    zR over rated units (the scorer's own definitions). OPEN: a share `open_other` goes to a brand outside the
    registry, the rest chooses by the same logit without position. Returns (records, predictors, truth).
    as_text=True returns RAW answers ("...\\nCHOICE: brand") for the coder instead of coded records."""
    rng = np.random.default_rng(seed)
    live = B.live_units()
    pred, zL, zR, uPd, uRd = {}, {}, {}, {}, {}
    for cat, _s, _i in B.CATEGORIES:
        units = live[cat]
        P = rng.permutation(np.linspace(2, 98, len(units)))
        for b, p in zip(units, P):
            pred[(cat, b)] = {"P": float(p), "R_star": None, "pi_hat": float(p) / 100 * 0.9}
        k = int(round(rated_share * len(units)))
        rated = [units[i] for i in np.argsort(-P)[:k]]
        zp = (P - P.mean()) / P.std()
        zpd = dict(zip(units, zp))
        for b in rated:
            pred[(cat, b)]["R_star"] = float(-np.round(np.clip(
                5 - 3 * (r_PR * zpd[b] + math.sqrt(1 - r_PR ** 2) * rng.normal()), 1, 12)))
            pred[(cat, b)]["R_star"] += rng.uniform(-1e-3, 1e-3)    # break ties (truth uses exact u's anyway)
        cfg = make_cfg(pred, ["x"], live)
        uPd[cat] = utable(cfg, "P")[cat]
        uRd[cat] = utable(cfg, "R_star")[cat]
        zL[cat] = zscore(uPd[cat])
        zR[cat] = zscore(uRd[cat])
    models = [f"model_{i + 1}" for i in range(n_models)]
    recs = []
    tU = {"LIST": [0.0, 0], "OPEN": [0.0, 0]}
    tUR = [0.0, 0.0]
    tD = [0.0, 0]
    for m in models:
        for cat, _s, _i in B.CATEGORIES:
            units = live[cat]
            L = len(units)
            for sq in range(1, squares + 1):
                orders = B.cyclic_latin_square(units, rng)
                for r_i, order in enumerate(orders):
                    brief = B.BRIEF_IDS[r_i % 3]
                    v = np.array([beta_P * zL[cat][b] + beta_R * zR[cat].get(b, 0.0) +
                                  (gamma_1 if j == 0 else 0.0) for j, b in enumerate(order)]) * scale
                    pr = np.exp(v - v.max())
                    pr /= pr.sum()
                    tU["LIST"][0] += float(sum(pr[j] * uPd[cat][b] for j, b in enumerate(order)))
                    tU["LIST"][1] += 1
                    tUR[0] += float(sum(pr[j] * uRd[cat][b] for j, b in enumerate(order) if b in uRd[cat]))
                    tUR[1] += float(sum(pr[j] for j, b in enumerate(order) if b in uRd[cat]))
                    tD[0] += float(sum(pr[j] * j / (L - 1) for j in range(L)))
                    tD[1] += 1
                    ch = order[int(rng.choice(L, p=pr))]
                    recs.append(dict(condition="LIST", category=cat, brief=brief, model=m, square=sq,
                                     row=r_i + 1, order=order, chosen=ch, call_id=f"{m}/{cat}/L{sq}/{r_i + 1}"))
            v = np.array([beta_P * zL[cat][b] + beta_R * zR[cat].get(b, 0.0) for b in units]) * scale
            pr = np.exp(v - v.max())
            pr /= pr.sum()
            for br in B.BRIEF_IDS:
                for run in range(1, B.OPEN_RUNS + 1):
                    tU["OPEN"][0] += float(sum(pr[j] * uPd[cat][b] for j, b in enumerate(units)))
                    tU["OPEN"][1] += 1
                    ch = None if rng.random() < open_other else units[int(rng.choice(L, p=pr))]
                    recs.append(dict(condition="OPEN", category=cat, brief=br, model=m, run=run, order=None,
                                     chosen=ch, call_id=f"{m}/{cat}/O/{br}/{run}"))
    truth = {"U_P_LIST": tU["LIST"][0] / tU["LIST"][1], "U_P_OPEN": tU["OPEN"][0] / tU["OPEN"][1],
             "U_R_LIST": tUR[0] / tUR[1], "beta_R": beta_R, "OR_R": math.exp(beta_R), "gamma_1": gamma_1,
             "d_bar": tD[0] / tD[1]}
    out = []
    for r in recs:
        if as_text:
            name = r["chosen"] or "Acme House Brand"
            out.append({k: v for k, v in r.items() if k != "chosen"} |
                       {"status": "ok", "text": f"It suits this buyer.\nCHOICE: {name}"})
        else:
            c = {k: v for k, v in r.items() if k != "chosen"}
            if r["chosen"] is None:
                c.update(code="OTHER", unit=None, other_text="Acme House Brand", position=None, L=None)
            else:
                c.update(code="VALID", unit=r["chosen"], position=(r["order"].index(r["chosen"]) + 1
                                                                   if r["order"] else None),
                         L=len(r["order"]) if r["order"] else None)
            out.append(c)
    return out, pred, truth


def recovery_report(res, truth):
    t = res["tests"]
    rows = [("U_P LIST (H1)", t["H1"]["U"], truth["U_P_LIST"]), ("U_P OPEN (H2)", t["H2"]["U"], truth["U_P_OPEN"]),
            ("U_R LIST (H3)", t["H3"]["U"], truth["U_R_LIST"]), ("OR_R (H4)", t["H4"]["OR_R"], truth["OR_R"]),
            ("gamma_1 (H4 model)", t["H4"]["coef"]["gamma_1"], truth["gamma_1"]),
            ("d_bar (H5)", t["H5"]["d_bar"], truth["d_bar"])]
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--synthetic", action="store_true")
    ap.add_argument("--squares", type=int, default=2)
    ap.add_argument("--draws-scale", type=float, default=1.0)
    ap.add_argument("--no-sens", action="store_true")
    ap.add_argument("--end-to-end", action="store_true", help="synthetic: pass raw answers through the coder")
    ap.add_argument("--coded")
    ap.add_argument("--predictors")
    ap.add_argument("--raw", help="raw answer lines (descriptives 6 hedges and 8 answer form / cost)")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    if a.synthetic:
        for label, kw in (("NULL world (beta_P = beta_R = gamma_1 = 0)", dict(beta_P=0, beta_R=0, gamma_1=0)),
                          ("EFFECT world (beta_P 1.5, beta_R 0.5, gamma_1 0.7)", {})):
            recs, pred, truth = synth_world(squares=a.squares, as_text=a.end_to_end, **kw)
            if a.end_to_end:
                import code_v0_46 as C
                recs = C.code_all(recs)
            res = score(recs, pred, draws=a.draws_scale, with_sens=not a.no_sens)
            t = res["tests"]
            print(f"[v46] {label}; squares {a.squares}; {len(recs)} calls; draws x{a.draws_scale}")
            for name, got, want in recovery_report(res, truth):
                print(f"    {name:20s} estimate {got:7.4f}   truth {want:7.4f}   diff {got - want:+.4f}")
            print(f"    H1 {t['H1']['verdict']} (p {t['H1']['p']:.4f}, n {t['H1']['n']})  "
                  f"H2 {t['H2']['verdict']} (p {t['H2']['p']:.4f}, n {t['H2']['n']})  "
                  f"H3 {t['H3']['verdict']} (p {t['H3']['p']:.4f}, n {t['H3']['n']})  "
                  f"H4 {t['H4']['verdict']} (OR {t['H4']['OR_R']:.3f}, p {t['H4']['p']:.4f}, n {t['H4']['n']})  "
                  f"H5 {t['H5']['label']} (p {t['H5']['p']:.4f})")
        return 0
    if not (a.coded and a.predictors and a.out):
        ap.error("--coded, --predictors and --out are required unless --synthetic")
    res = score(read_jsonl(a.coded), read_predictors(a.predictors), draws=a.draws_scale, with_sens=not a.no_sens,
                raw=read_jsonl(a.raw) if a.raw else None)
    Path(a.out).write_text(json.dumps(res, indent=1, default=str, ensure_ascii=False), encoding="utf-8")
    print(f"[v46] wrote {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
