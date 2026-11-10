#!/usr/bin/env python3
"""
score_v0_42.py -- AIAS(TM) v0.42 scorer (t4 wave). Transcribes PRE_REGISTRATION_v0_42.md (revision r2) sections 2
and 5. THE PRE-REGISTRATION PROSE IS AUTHORITATIVE; where it is silent the simplest faithful option is taken and
listed below (SCORER_NOTES).

r2 (2026-11-10, $100 rule): panel N3 only (Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon); Claude Opus 5.5, the C3
panel and H_Version_Presence are removed; Phase A is collected in S0, run 1 only; expected calls 876 (S0: 30 x 3 +
112 = 202 per model; S1: 30 x 3 = 90 per model). Notes N6, N8 and N12 are revised accordingly; N15 is new.

SCORER_NOTES (choices where the pre-registration is silent)
 N1  Helpers phi_m / phi_of / spearman / within_ranks / pooled_within_rho / _pearson / load_wave are IMPORTED
     from osf/v41/scripts/score_v41.py (not re-typed). Python: the system python3 (numpy+scipy); the v41 venv
     has no numpy.
 N2  Permutation: y is shuffled within substrate and rho_pw (within-substrate ranks, both vectors) is recomputed
     on every draw with score_v41.pooled_within_rho. A draw counts as a hit if rho_perm >= rho_obs - 1e-12
     (float tolerance for exact ties); p = (1 + hits) / (draws + 1).
 N3  Bootstrap: brands resampled with replacement within substrate (v41 _decay scheme); several statistics of one
     test are taken on the SAME resamples; draws where a statistic is non-finite are dropped for that statistic
     and counted.
 N4  Each alongside variant of a hypothesis re-uses that hypothesis' seed (fresh generator per test).
     Seed 420045 (descriptives) is recorded but unused: no descriptive carries an interval.
 N5  "Answered call" = deduplicated raw call with status ok, non-empty text, no error, served ID accepted
     (MC_Served). Phase B rates use the answered calls of each (model, run, substrate) as denominator; the
     answered set is the set of call_ids present in the coded Phase B table. Duplicate lines of one call_id
     (re-run pass): the last answered attempt, else the last attempt.
 N6  Model x condition is excluded if answered / expected < 0.90 (expected per model: S0 202 = 30 x 3 + 112,
     S1 90 = 30 x 3; a call absent from the raw file counts as unanswered). H_Gen_* use S0: any N3 model excluded
     -> UNDETERMINED (r2: no C3 fallback). The S1 alongside variant uses the N3 models retained in S1 (flagged
     reduced_panel); H_Search uses the models retained in BOTH conditions; none -> NOT_COMPUTED.
 N7  phi per run needs all models of the panel to have all 6 Phase B answers in that substrate; otherwise the run
     is undefined for that substrate. Brand phi = mean over defined runs if >= 2 of 3 are defined else None.
     Brand partition label: "defined" (phi available); else "zero"/"saturated" if every run is zero/saturated;
     else "undefined" (fewer than 2 defined runs, e.g. missing calls or mixed partitions).
 N8  rel1 (descriptive 1): mean of pooled-within rho over the run pairs for which >= 3 brands have both rates;
     k/6 uses the answered-call denominator. Recognition agreement across runs: mean over brands of the share of
     agreeing run pairs -- not computable in r2 (Phase A has one run); reported as None.
 N9  Descriptive 3 "the reverse": of the brands below the floor on N3,S0 at t4 (6*pi_hat < 1), the share that were
     below it at t3; the share of above-floor t3 brands that fall below is also given.
 N10 Refusals (descriptive 4): finish reasons containing refusal / content_filter / safety / prohibited / blocklist;
     unanswered calls (error / empty) counted separately.
 N11 MC_Truncation: finish reason (lower-case) contains "max_tokens" or "max_output_tokens", or equals "length".
     MC_Served: a call with status ok and no served ID is listed, not excluded. Dated snapshot = requested +
     "-YYYY-MM-DD" or "-YYYYMMDD". A leading "models/" is ignored.
 N12 Cost (descriptive 6): budget_v0_42.record_cost of every raw line (every attempt): the recorded usage of each
     billed request (`usage_parts`: batch or standard token prices; Google thinking tokens billed as output; search
     fees per recorded search), at the list prices of section 4.5 -- the same function as the collection guard.
 N13 Domains (descriptive 5): host of each citation URL, lower-case, leading "www." dropped.
 N14 NaN rho (degenerate data) -> verdict UNDETERMINED (the rules are silent).
 N15 (r2) Seed 420042 (H_Version_Presence) is retired with the hypothesis; the other seeds are unchanged. The
     manipulation checks count only calls of the design (Phase B: S0/S1, runs 1-3; Phase A: S0, run 1) and of the
     N3 models; any other raw line is reported as `outside_design` and not analysed.

Modes: --parity-p1 | --synthetic DIR | --run   (--run refuses unless tag v0.42-prereg-r1 is on origin)
"""
import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
import code_t4_v0_42 as C   # noqa: E402  (bootstraps ROOT / HOME shim, sys.path for the certified modules)

ROOT = C.ROOT

import argparse         # noqa: E402
import collections      # noqa: E402
import csv              # noqa: E402
import itertools        # noqa: E402
import json             # noqa: E402
import math             # noqa: E402
import re               # noqa: E402
from urllib.parse import urlparse  # noqa: E402

import numpy as np      # noqa: E402

import score_v41 as sv  # noqa: E402
import budget_v0_42 as BG  # noqa: E402

phi_m, phi_of, spearman, within_ranks, pooled_within_rho, _pearson, load_wave = (
    sv.phi_m, sv.phi_of, sv.spearman, sv.within_ranks, sv.pooled_within_rho, sv._pearson, sv.load_wave)

PHASE_ID = "v0.42"
OMNI = sv.OMNI
F = 6
RUNS = (1, 2, 3)
PHASE_A_DESIGN = {("S0", 1)}                       # r2: Phase A in S0, run 1 only
EXPECTED_PER_MODEL_COND = {"S0": 30 * 3 + 112, "S1": 30 * 3}
EXPECTED_TOTAL = 876
N_PERM = 10_000
N_BOOT = 10_000
SEEDS = {"H_Gen_Presence": 420041, "H_Gen_Phi": 420043,
         "H_Search_Presence": 420044, "descriptives": 420045}   # 420042 retired with H_Version_Presence (r2)
FABLE, GPT6, GEM4 = "claude-fable-5-2", "gpt-6-astra", "gemini-4-argon"
MODELS = [FABLE, GPT6, GEM4]
PANELS = {"N3": [FABLE, GPT6, GEM4]}
CONDS = ["S0", "S1"]
import score_v0_31 as S31   # noqa: E402
L6 = list(S31.PANEL)   # claude-opus-4-5, claude-sonnet-4-5, gpt-4o, gpt-4o-mini, gemini-2.5-flash, gemini-2.5-flash-lite
PROVIDER_PAIRS = {  # legacy indices in L6 order -> new models (section 2.2 "per-provider generation pairs")
    "Anthropic": ((0, 1), [FABLE]), "OpenAI": ((2, 3), [GPT6]), "Google": ((4, 5), [GEM4])}
GEN_CONF, GEN_P, GEN_FALS = 0.70, 0.05, 0.50
PHI_CONF, PHI_FALS, PHI_N_FLOOR = 0.50, 0.30, 40
SEARCH_LO, SEARCH_HI = 0.80, 0.50
DROP_SHARE = 0.90
COMPLETE_SHARE, SEARCH_FLAG, TRUNC_FLAG = 0.98, 0.25, 0.05
MEAN_INDEP_FLAG = 0.50
T3_TABLE = ROOT / "osf/v41/v41_three_wave_table.csv"
P1_PATH = ROOT / "osf/v42/prereg/parity_P1_v0_42.json"
P2_PATH = C.P2_PATH
P3_PATH = ROOT / "osf/v42/prereg/probe_parity_v0_42.json"
VERDICTS = ROOT / "osf/v42/v42_verdicts.json"
BRAND_TABLE = ROOT / "osf/v42/v42_brand_table.csv"
NAN = float("nan")


class Cfg:
    def __init__(self, n_perm=N_PERM, n_boot=N_BOOT):
        self.n_perm, self.n_boot = n_perm, n_boot


# =========================================================================== t3 inputs
def load_t3_table(path=T3_TABLE):
    """Locked per-brand t3 values: {(sub, brand): {k:[6], pi, phi, partition}} (wave t3 rows)."""
    out = {}
    for r in csv.DictReader(open(path, newline="", encoding="utf-8")):
        if r["wave"] != "t3":
            continue
        out[(r["substrate"], r["brand"])] = {
            "k": json.loads(r["k_per_model"]), "pi": float(r["pi_hat"]),
            "phi": float(r["phi"]) if r["phi"] != "" else None, "partition": r["phi_partition"]}
    return out


def pi_from_counts(k, n_models=None, runs=1):
    """pi_hat = sum k / (6 * |P| * R)  (section 2.1)."""
    n_models = len(k) if n_models is None else n_models
    return float(sum(k) / (F * n_models * runs))


def phi_from_counts(k):
    """t3 phi: the v0.41 reduced-panel kernel phi_m, defined partition only."""
    return phi_m(list(k))


def parity_p1(out_path=P1_PATH):
    """P1: the scorer's t3 path, from the t3 RAW data via score_v41.load_wave, reproduces the locked table's t3
    k_per_model, pi_hat and phi (exact equality) for all 112 brands."""
    locked = load_t3_table()
    wave = load_wave(sv._layout(sv.DATA3, sv.DATA3 / "v23"))
    mine = {}
    for sub in OMNI:
        for b, vec in wave[sub]["counts"].items():
            k = [int(x) for x in vec]
            phi, pi_p, part = phi_from_counts(k)
            mine[(sub, b)] = {"k": k, "pi": pi_from_counts(k, 6, 1), "phi": phi, "partition": part}
    problems = []
    if set(mine) != set(locked) or len(mine) != 112:
        problems.append(f"brand sets differ: recomputed {len(mine)}, locked {len(locked)}")
    n_k = n_pi = n_phi = n_part = 0
    for key in sorted(set(mine) & set(locked)):
        m, l = mine[key], locked[key]
        n_k += m["k"] == l["k"]
        n_pi += m["pi"] == l["pi"]
        n_phi += (m["phi"] is None and l["phi"] is None) or (m["phi"] is not None and m["phi"] == l["phi"])
        n_part += m["partition"] == l["partition"]
        for f in ("k", "pi", "phi"):
            if not ((m[f] is None and l[f] is None) or m[f] == l[f]):
                problems.append(f"{key} {f}: recomputed={m[f]} locked={l[f]}")
    n = len(set(mine) & set(locked))
    res = {"gate": "P1", "passed": (not problems) and n == 112 and n_k == n_pi == n_phi == n,
           "brands_compared": n, "k_per_model_exact": n_k, "pi_hat_exact": n_pi, "phi_exact": n_phi,
           "phi_partition_exact_info": n_part,
           "phi_defined_brands": sum(1 for v in mine.values() if v["phi"] is not None),
           "locked_table": str(T3_TABLE.relative_to(ROOT)), "inputs": "osf/v41/data via score_v41.load_wave (t3 raw)",
           "problems": problems[:20]}
    if out_path:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        json.dump(res, open(out_path, "w"), indent=2)
    return res


# =========================================================================== t4 data
def served_ok(requested, served):
    s = (served or "").strip().removeprefix("models/")
    return s == requested or re.fullmatch(re.escape(requested) + r"-(\d{4}-\d{2}-\d{2}|\d{8})", s) is not None


class Data:
    """Aggregates coded Phase B rows: k per (cond, model, run, sub, brand) and answered Phase B calls per
    (cond, model, run, sub)."""

    def __init__(self, brands, A, B, excluded=frozenset()):
        self.brands = list(brands)
        self.k = collections.defaultdict(int)
        self.ans = collections.defaultdict(set)
        for r in B:
            if r["call_id"] in excluded:
                continue
            self.ans[(r["condition"], r["model"], r["run"], r["substrate"])].add(r["call_id"])
            self.k[(r["condition"], r["model"], r["run"], r["substrate"], r["brand"])] += int(r["mentioned"])
        self.A = [r for r in A if r["call_id"] not in excluded and r.get("recognized") is not None]

    def n(self, cond, model, run, sub):
        return len(self.ans.get((cond, model, run, sub), ()))

    def kk(self, cond, model, run, sub, brand):
        return self.k.get((cond, model, run, sub, brand), 0)


def pi_hat(D, models, cond, runs=RUNS):
    """pi_hat_{b,P,cond} = sum_m sum_r k / (answered Phase B calls) -- = k / (6|P|R) when complete."""
    out = {}
    for (s, b) in D.brands:
        num = sum(D.kk(cond, m, r, s, b) for m in models for r in runs)
        den = sum(D.n(cond, m, r, s) for m in models for r in runs)
        out[(s, b)] = num / den if den else NAN
    return out


def phi_runs(D, models, cond, s, b):
    """Per-run (phi, partition) for brand b on panel `models` (None, 'missing' if a model-run lacks answers)."""
    res = []
    for r in RUNS:
        if any(D.n(cond, m, r, s) != F for m in models):
            res.append((None, "missing"))
            continue
        phi, _pi, part = phi_m([D.kk(cond, m, r, s, b) for m in models])
        res.append((phi, part))
    return res


def phi_panel(D, models, cond):
    """{(sub, brand): (phi or None, partition label, [per-run partitions])}  (rule: >= 2 of 3 runs defined)."""
    out = {}
    for (s, b) in D.brands:
        runs = phi_runs(D, models, cond, s, b)
        vals = [p for p, part in runs if part == "defined"]
        parts = [part for _, part in runs]
        if len(vals) >= 2:
            out[(s, b)] = (float(np.mean(vals)), "defined", parts)
        elif parts and all(p == "zero" for p in parts):
            out[(s, b)] = (None, "zero", parts)
        elif parts and all(p == "saturated" for p in parts):
            out[(s, b)] = (None, "saturated", parts)
        else:
            out[(s, b)] = (None, "undefined", parts)
    return out


# =========================================================================== statistics
def pair_arrays(xd, yd, keys=None):
    keys = [k for k in (keys or list(xd)) if k in yd and xd[k] is not None and yd[k] is not None
            and np.isfinite(xd[k]) and np.isfinite(yd[k])]
    return (keys, np.array([xd[k] for k in keys], float), np.array([yd[k] for k in keys], float),
            np.array([k[0] for k in keys]))


def perm_p_within(x, y, g, obs, seed, n_draws):
    """One-sided permutation p: y shuffled within substrate, rho_pw recomputed (within-substrate ranks) on every draw.
    p = (1 + #{rho_perm >= rho_obs}) / (n_draws + 1)."""
    if not np.isfinite(obs):
        return NAN
    rng = np.random.default_rng(seed)
    gidx = sv._group_index(g)
    hits = 0
    for _ in range(n_draws):
        yp = y.copy()
        for gi in gidx:
            yp[gi] = y[rng.permutation(gi)]
        r = pooled_within_rho(x, yp, g)
        hits += bool(r >= obs - 1e-12)
    return (1 + hits) / (n_draws + 1)


def bootstrap(g, seed, n_boot, fn):
    """Brands resampled with replacement within substrate; fn(idx) -> {name: value}; percentile 95% per name."""
    rng = np.random.default_rng(seed)
    gidx = sv._group_index(g)
    store = collections.defaultdict(list)
    names = None
    dropped = collections.Counter()
    for _ in range(n_boot):
        idx = np.concatenate([rng.choice(gi, size=len(gi), replace=True) for gi in gidx])
        res = fn(idx)
        names = names or list(res)
        for k, v in res.items():
            if np.isfinite(v):
                store[k].append(v)
            else:
                dropped[k] += 1
    out = {}
    for k in names or []:
        if store[k]:
            lo, hi = np.percentile(store[k], [2.5, 97.5])
            out[k] = {"ci95": [float(lo), float(hi)], "n_draws": len(store[k]), "dropped_nonfinite": int(dropped[k])}
        else:
            out[k] = {"ci95": None, "n_draws": 0, "dropped_nonfinite": int(dropped[k])}
    return out


def per_substrate_rho(x, y, g):
    out = {}
    for s in OMNI:
        m = g == s
        out[s] = {"rho": spearman(x[m], y[m]) if m.sum() >= 3 else NAN, "n": int(m.sum())}
    return out


def presence_test(xd, yd, seed, cfg, with_p=True):
    """rho_pw(x, y) with permutation p, bootstrap interval, level shift (mean(y - x)) and its interval."""
    keys, x, y, g = pair_arrays(xd, yd)
    n = len(keys)
    rho = pooled_within_rho(x, y, g) if n >= 3 else NAN
    out = {"n": n, "rho": rho, "per_substrate": per_substrate_rho(x, y, g) if n else {}}
    if n < 3:
        return out
    if with_p:
        out["p_perm"] = perm_p_within(x, y, g, rho, seed, cfg.n_perm)
        out["n_perm"] = cfg.n_perm
    b = bootstrap(g, seed, cfg.n_boot, lambda i: {"rho": pooled_within_rho(x[i], y[i], g[i]),
                                                  "delta": float(np.mean(y[i] - x[i]))})
    out["ci95_rho"] = b["rho"]["ci95"]
    out["delta"] = float(np.mean(y - x))
    out["ci95_delta"] = b["delta"]["ci95"]
    out["bootstrap"] = {k: {kk: vv for kk, vv in v.items() if kk != "ci95"} for k, v in b.items()}
    return out


def verdict_gen(rho, p):
    if not np.isfinite(rho) or p is None or not np.isfinite(p):
        return "UNDETERMINED"
    if rho >= GEN_CONF and p < GEN_P:
        return "CONFIRMED"
    if rho < GEN_FALS:
        return "FALSIFIED"
    return "MARGINAL"


def verdict_phi(n, rho, p):
    if n < PHI_N_FLOOR:
        return "UNDETERMINED"
    if not np.isfinite(rho) or not np.isfinite(p):
        return "UNDETERMINED"
    if rho >= PHI_CONF and p < GEN_P:
        return "CONFIRMED"
    if rho < PHI_FALS:
        return "FALSIFIED"
    return "MARGINAL"


def label_search(ci):
    if ci is None:
        return "UNDETERMINED"
    lo, hi = ci
    if lo >= SEARCH_LO:
        return "search-robust"
    if hi < SEARCH_HI:
        return "search-dominated"
    return "search-sensitive"


def rel3_of(r):
    return 3 * r / (1 + 2 * r) if np.isfinite(r) else NAN


def rel1_of(K, Nn, g):
    """Mean pooled-within rho over the three run pairs of k/n (K, Nn: 3 x brands)."""
    with np.errstate(invalid="ignore", divide="ignore"):
        rates = np.where(Nn > 0, K / np.where(Nn > 0, Nn, 1), np.nan)
    vals = []
    for a, b in itertools.combinations(range(K.shape[0]), 2):
        m = np.isfinite(rates[a]) & np.isfinite(rates[b])
        if m.sum() >= 3:
            vals.append(pooled_within_rho(rates[a][m], rates[b][m], g[m]))
    vals = [v for v in vals if np.isfinite(v)]
    return float(np.mean(vals)) if vals else NAN


def model_arrays(D, model, cond, keys):
    K = np.array([[D.kk(cond, model, r, s, b) for (s, b) in keys] for r in RUNS], float)
    Nn = np.array([[D.n(cond, model, r, s) for (s, b) in keys] for r in RUNS], float)
    return K, Nn


def recognition_codes(D, model, cond):
    """{(sub, brand): [recognized per answered run]}."""
    out = collections.defaultdict(list)
    for r in D.A:
        if r["model"] == model and r["condition"] == cond:
            out[(r["substrate"], r["brand"])].append(int(r["recognized"]))
    return out


# =========================================================================== manipulation checks / drop rule
def _search_n(rec):
    s = rec.get("search") or {}
    return s.get("n_searches") or len(s.get("queries") or [])


def _truncated(rec):
    fr = str(rec.get("finish_reason") or "").lower()
    return "max_tokens" in fr or "max_output_tokens" in fr or fr == "length"


def in_design(rec):
    """r2 design: N3 models; Phase B in S0/S1, runs 1-3; Phase A in S0, run 1 (N15)."""
    if rec.get("model_requested") not in MODELS or rec.get("condition") not in CONDS:
        return False
    if rec.get("phase") == "B":
        return rec.get("run") in RUNS
    if rec.get("phase") == "A":
        return (rec.get("condition"), rec.get("run")) in PHASE_A_DESIGN
    return False


def manipulation_checks(calls_all):
    """calls_all: deduplicated raw records (before the served-ID exclusion). Returns (mcs, excluded_call_ids).
    Calls outside the r2 design are counted in `outside_design` and excluded from the analysis (N15)."""
    outside = [r["call_id"] for r in calls_all if not in_design(r)]
    calls_all = [r for r in calls_all if in_design(r)]
    per = collections.defaultdict(lambda: {"calls": 0, "answered": 0})
    mism, missing = [], []
    excluded = set(outside)
    for r in calls_all:
        if C.is_answered(r):
            if not r.get("served_model"):
                missing.append(r["call_id"])
            elif not served_ok(r["model_requested"], r["served_model"]):
                mism.append({"call_id": r["call_id"], "requested": r["model_requested"], "served": r["served_model"]})
                excluded.add(r["call_id"])
    for r in calls_all:
        d = per[(r["model_requested"], r["condition"])]
        d["calls"] += 1
        d["answered"] += int(C.is_answered(r) and r["call_id"] not in excluded)
    n_ans = sum(d["answered"] for d in per.values())
    per_mc = {f"{m}|{c}": {**d, "expected": EXPECTED_PER_MODEL_COND[c],
                           "share_of_expected": d["answered"] / EXPECTED_PER_MODEL_COND[c],
                           "excluded_below_90pct": d["answered"] / EXPECTED_PER_MODEL_COND[c] < DROP_SHARE}
              for (m, c), d in sorted(per.items())}
    for m in MODELS:                                   # a model x condition with no call at all is also short
        for c in CONDS:
            per_mc.setdefault(f"{m}|{c}", {"calls": 0, "answered": 0, "expected": EXPECTED_PER_MODEL_COND[c],
                                           "share_of_expected": 0.0, "excluded_below_90pct": True})
    mcs = {"MC_Complete": {"answered": n_ans, "expected": EXPECTED_TOTAL, "share": n_ans / EXPECTED_TOTAL,
                           "pass": n_ans / EXPECTED_TOTAL >= COMPLETE_SHARE, "per_model_condition": per_mc,
                           "below_90pct": [k for k, v in per_mc.items() if v["excluded_below_90pct"]],
                           "outside_design": {"n": len(outside), "call_ids": outside[:50]}},
           "MC_Served": {"n_mismatched": len(mism), "mismatched": mism[:50],
                         "ok_calls_without_served_id": len(missing), "excluded_from_analysis": len(excluded),
                         "pass": not mism}}
    s1 = collections.defaultdict(lambda: [0, 0])
    for r in calls_all:
        if r["condition"] == "S1" and C.is_answered(r):
            s1[r["model_requested"]][0] += 1
            s1[r["model_requested"]][1] += int(_search_n(r) >= 1)
    mcs["MC_Search"] = {m: {"s1_answered_calls": a, "with_search": b, "share": b / a if a else None,
                            "flag_search_rarely_used": bool(a and b / a < SEARCH_FLAG)} for m, (a, b) in s1.items()}
    tr = collections.defaultdict(lambda: [0, 0])
    for r in calls_all:
        tr[f"{r['model_requested']}|{r['condition']}"][0] += 1
        tr[f"{r['model_requested']}|{r['condition']}"][1] += int(_truncated(r))
    mcs["MC_Truncation"] = {k: {"calls": a, "at_cap": b, "share": b / a, "flag_above_5pct": b / a > TRUNC_FLAG}
                            for k, (a, b) in sorted(tr.items())}
    starts = sorted(r["started_utc"] for r in calls_all if r.get("started_utc"))
    ends = sorted(r["finished_utc"] for r in calls_all if r.get("finished_utc"))
    win = {"first_call_utc": starts[0] if starts else None, "last_call_utc": ends[-1] if ends else None}
    if starts and ends:
        from datetime import datetime
        h = (datetime.fromisoformat(ends[-1]) - datetime.fromisoformat(starts[0])).total_seconds() / 3600
        win["span_hours"] = h
        win["pass"] = h <= 72
    else:
        win["span_hours"] = None
        win["pass"] = False
    mcs["MC_Window"] = win
    return mcs, excluded


def excluded_set(mc_complete):
    return {tuple(k.split("|")) for k in mc_complete["below_90pct"]}


# =========================================================================== hypotheses
def _models_ok(models, cond, excl):
    return [m for m in models if (m, cond) not in excl]


def gen_panel(excl, cond="S0"):
    """Section 5.4: panel for H_Gen_*. Returns (name, models, note) or (None, None, reason)."""
    gone = [m for m in PANELS["N3"] if (m, cond) in excl]
    if gone:
        return None, None, f"{', '.join(gone)} excluded (answered < 90%): hypothesis UNDETERMINED (r2: no fallback panel)"
    return "N3", PANELS["N3"], None


def _t3_vectors(t3):
    return ({k: v["pi"] for k, v in t3.items()}, {k: v["phi"] for k, v in t3.items()},
            {k: v["k"] for k, v in t3.items()})


def h_gen_presence(D, t3, excl, cfg):
    seed = SEEDS["H_Gen_Presence"]
    x, _, kk = _t3_vectors(t3)
    name, models, note = gen_panel(excl)
    out = {"tier": "PRIMARY", "seed": seed}
    if name is None:
        out.update(verdict="UNDETERMINED", reason=note)
    else:
        t = presence_test(x, pi_hat(D, models, "S0"), seed, cfg)
        out.update(panel_used=name, models=models, substituted=name != "N3", substitution_note=note, **t,
                   verdict=verdict_gen(t["rho"], t.get("p_perm")),
                   rule="CONFIRMED if rho>=0.70 and p<0.05; FALSIFIED if rho<0.50; MARGINAL otherwise")
    alt = {}
    for label, panel, cond in (("N3_S1", "N3", "S1"),):
        ms = _models_ok(PANELS[panel], cond, excl)
        if not ms:
            alt[label] = {"status": "NOT_COMPUTED", "reason": "all models excluded"}
            continue
        t = presence_test(x, pi_hat(D, ms, cond), seed, cfg)
        alt[label] = {"models": ms, "reduced_panel": len(ms) < 3, **t,
                      "verdict_if_primary": verdict_gen(t["rho"], t.get("p_perm"))}
    pairs = {}
    for prov, (idx, newm) in PROVIDER_PAIRS.items():
        xl = {k: (v[idx[0]] + v[idx[1]]) / (2 * F) for k, v in kk.items()}
        for m in newm:
            if (m, "S0") in excl:
                pairs[f"{prov}: legacy pair -> {m}"] = {"status": "NOT_COMPUTED", "reason": "model excluded"}
                continue
            keys, a, b, g = pair_arrays(xl, pi_hat(D, [m], "S0"))
            pairs[f"{prov}: legacy pair -> {m}"] = {"n": len(keys), "rho": pooled_within_rho(a, b, g) if len(keys) >= 3 else NAN}
    out["reported_alongside"] = {"variants": alt, "per_provider_generation_pairs": pairs,
                                 "level_shift_delta": {"delta": out.get("delta"), "ci95": out.get("ci95_delta")},
                                 "per_substrate_rho": out.get("per_substrate")}
    return out


def partition_counts(phis):
    c = collections.Counter(v[1] for v in phis.values())
    return {k: int(c.get(k, 0)) for k in ("defined", "zero", "saturated", "undefined")}


def h_gen_phi(D, t3, excl, cfg):
    seed = SEEDS["H_Gen_Phi"]
    _, xphi, _ = _t3_vectors(t3)
    name, models, note = gen_panel(excl)
    out = {"tier": "SECONDARY", "seed": seed}

    def test(models_, cond):
        ph = phi_panel(D, models_, cond)
        y = {k: v[0] for k, v in ph.items()}
        keys, x, yy, g = pair_arrays(xphi, y)
        n = len(keys)
        rho = pooled_within_rho(x, yy, g) if n >= 3 else NAN
        t = {"n": n, "rho": rho}
        if n >= 3:
            t["p_perm"] = perm_p_within(x, yy, g, rho, seed, cfg.n_perm)
            b = bootstrap(g, seed, cfg.n_boot, lambda i: {"rho": pooled_within_rho(x[i], yy[i], g[i])})
            t["ci95_rho"] = b["rho"]["ci95"]
            t["per_substrate"] = per_substrate_rho(x, yy, g)
        return t, ph

    if name is None:
        out.update(verdict="UNDETERMINED", reason=note)
    else:
        t, _ph = test(models, "S0")
        out.update(panel_used=name, models=models, substituted=name != "N3", substitution_note=note, **t,
                   verdict=verdict_phi(t["n"], t["rho"], t.get("p_perm")),
                   rule="UNDETERMINED if n<40; CONFIRMED if rho>=0.50 and p<0.05; FALSIFIED if rho<0.30; else MARGINAL")
    alt, indep, parts = {}, {}, {}
    for pn in ("N3",):
        ms = _models_ok(PANELS[pn], "S0", excl)
        if not ms:
            continue
        ph = phi_panel(D, ms, "S0")
        pi = pi_hat(D, ms, "S0")
        keys, a, b, g = pair_arrays({k: v[0] for k, v in ph.items()}, pi)
        r = pooled_within_rho(a, b, g) if len(keys) >= 3 else NAN
        indep[pn] = {"n": len(keys), "rho_pw_phi_pi": r, "abs": abs(r) if np.isfinite(r) else None,
                     "flag_ge_0_50": bool(np.isfinite(r) and abs(r) >= MEAN_INDEP_FLAG)}
    for pn in ("N3",):
        for cond in CONDS:
            ms = _models_ok(PANELS[pn], cond, excl)
            if not ms:
                continue
            ph = phi_panel(D, ms, cond)
            runs = collections.Counter(p for v in ph.values() for p in v[2])
            parts[f"{pn}_{cond}"] = {"models": ms, "brand_level": partition_counts(ph),
                                     "per_run_partitions": {k: int(v) for k, v in runs.items()}}
    parts["L6_t3"] = dict(collections.Counter(v["partition"] for v in t3.values()))
    out["reported_alongside"] = {"variants": alt, "mean_independence_S0": indep, "partition_counts": parts}
    return out


def h_search(D, excl, cfg):
    seed = SEEDS["H_Search_Presence"]
    out = {"tier": "SECONDARY", "seed": seed, "question": "two-sided; labels, no confirm/falsify"}

    def one(panel):
        ms = [m for m in PANELS[panel] if (m, "S0") not in excl and (m, "S1") not in excl]
        if not ms:
            return {"status": "NOT_COMPUTED", "reason": "no model retained in both conditions"}
        x, y = pi_hat(D, ms, "S0"), pi_hat(D, ms, "S1")
        t = presence_test(x, y, seed, cfg, with_p=False)
        per_model = {}
        for m in ms:
            keys, a, b, g = pair_arrays(pi_hat(D, [m], "S0"), pi_hat(D, [m], "S1"))
            per_model[m] = {"n": len(keys), "rho": pooled_within_rho(a, b, g) if len(keys) >= 3 else NAN,
                            "delta": float(np.mean(b - a)) if len(keys) else NAN}
        return {"models": ms, "reduced_panel": len(ms) < 3, **t, "label": label_search(t.get("ci95_rho")),
                "per_model": per_model}

    out.update(one("N3"))
    out["reported_alongside"] = {"per_substrate_rho": out.get("per_substrate")}
    out["rule"] = "search-robust if CI lower >= 0.80; search-dominated if CI upper < 0.50; else search-sensitive"
    return out


# =========================================================================== descriptives (section 2.7; no verdicts)
def _legacy_recognition():
    """Per legacy model, share of the 112 brands recognised at t3 (score_v41.load_wave recog vectors)."""
    try:
        wave = load_wave(sv._layout(sv.DATA3, sv.DATA3 / "v23"))
    except Exception as e:                          # data not present
        return {"status": f"NOT_AVAILABLE: {type(e).__name__}"}
    tot = {m: [0, 0] for m in L6}
    for sub in OMNI:
        for b, vec in wave[sub]["recog"].items():
            for i, m in enumerate(L6):
                tot[m][0] += int(vec[i])
                tot[m][1] += 1
    return {m: {"recognized": a, "brands": n, "share": a / n} for m, (a, n) in tot.items()}


def _domain(url):
    try:
        h = (urlparse(url).netloc or "").lower()
    except Exception:
        return ""
    return h[4:] if h.startswith("www.") else h


def descriptives(D, B, calls, raw_all, t3, excl, legacy_recog=None):
    d = {"seed_reserved": SEEDS["descriptives"], "note": "descriptive only; no verdicts"}
    # 1. run-to-run reliability + recognition agreement across runs
    rel = {}
    for m in MODELS:
        for c in CONDS:
            K, Nn = model_arrays(D, m, c, D.brands)
            g = np.array([k[0] for k in D.brands])
            r1 = rel1_of(K, Nn, g)
            codes = recognition_codes_by_run(D, m, c)
            ag = []
            for key, v in codes.items():
                runs = list(v.values())
                if len(runs) >= 2:
                    ag.append(np.mean([a == b for a, b in itertools.combinations(runs, 2)]))
            rel[f"{m}|{c}"] = {"rel1": r1, "rel3": rel3_of(r1),
                               "recognition_pairwise_agreement": float(np.mean(ag)) if ag else None,
                               "recognition_brands_with_>=2_runs": len(ag),
                               "note": "Phase A has one run in r2 (S0): recognition agreement across runs not computable"}
    d["1_run_reliability"] = rel
    # 2. recognition share beside legacy models
    shares = {}
    for m in MODELS:
        for c in CONDS:
            v = [int(r["recognized"]) for r in D.A if r["model"] == m and r["condition"] == c]
            shares[f"{m}|{c}"] = {"recognized": sum(v), "coded_answers": len(v), "share": sum(v) / len(v) if v else None}
    d["2_recognition"] = {"t4": shares, "t3_legacy": legacy_recog if legacy_recog is not None else _legacy_recognition(),
                          "note": "v0.23 t4 recognition is blank until the judge has been run (coder --judge)"}
    # 3. floor persistence (N3, S0)
    name, models, _ = gen_panel(excl)
    if name is None:
        d["3_floor_persistence"] = {"status": "NOT_COMPUTED"}
    else:
        pi4 = pi_hat(D, models, "S0")
        below3 = {k for k, v in t3.items() if float(np.mean(v["k"])) < 1.0}
        below4 = {k for k, v in pi4.items() if np.isfinite(v) and F * v < 1.0}
        valid = {k for k, v in pi4.items() if np.isfinite(v)}
        both = below3 & below4
        above3 = (set(t3) & valid) - below3
        d["3_floor_persistence"] = {
            "panel_t4": name, "below_floor_t3": len(below3), "below_floor_t4": len(below4), "below_both": len(both),
            "share_below_t3_still_below_t4": len(both) / len(below3) if below3 else None,
            "reverse_share_below_t4_that_were_below_t3": len(both) / len(below4) if below4 else None,
            "share_above_t3_now_below_t4": len(below4 & above3) / len(above3) if above3 else None,
            "floor": "t3: mean k per model < 1; t4: mean k per model-run (6 * pi_hat) < 1"}
    # 4. answer form
    per = collections.defaultdict(lambda: {"words_A": [], "words_B": [], "finish": collections.Counter(),
                                            "unanswered": 0, "refusals": 0, "ambiguous_A": 0})
    brands_named = collections.defaultdict(int)
    for r in B:
        brands_named[r["call_id"]] += int(r["mentioned"])
    ncall_b = collections.Counter()
    for r in calls:
        x = per[f"{r['model_requested']}|{r['condition']}"]
        x["finish"][str(r.get("finish_reason"))] += 1
        if not C.is_answered(r):
            x["unanswered"] += 1
            continue
        w = len(r["text"].split())
        x["words_" + r["phase"]].append(w)
        if re.search(r"refus|content_filter|safety|prohibit|blocklist", str(r.get("finish_reason") or ""), re.I):
            x["refusals"] += 1
    for r in D.A:
        if r["substrate"] in ("v0.19", "v0.20", "v0.21", "v0.22") and r.get("label") == "ambiguous":
            per[f"{r['model']}|{r['condition']}"]["ambiguous_A"] += 1
    form = {}
    for k, x in sorted(per.items()):
        m, c = k.split("|")
        ids = {r["call_id"] for r in B if r["model"] == m and r["condition"] == c}
        form[k] = {"words_per_answer_A_mean": float(np.mean(x["words_A"])) if x["words_A"] else None,
                   "words_per_answer_B_mean": float(np.mean(x["words_B"])) if x["words_B"] else None,
                   "registry_brands_named_per_phase_B_answer": float(np.mean([brands_named[i] for i in ids])) if ids else None,
                   "finish_reasons": dict(x["finish"]), "non_answers": {
                       "phase_A_no_yes_or_no_v0_19_to_v0_22": x["ambiguous_A"], "refusals_by_finish_reason": x["refusals"],
                       "unanswered_calls_error_or_empty": x["unanswered"]}}
    d["4_answer_form"] = form
    # 5. search (S1)
    s = {}
    for m in MODELS:
        cs = [r for r in calls if r["model_requested"] == m and r["condition"] == "S1" and C.is_answered(r)]
        if not cs:
            continue
        dom = collections.Counter()
        for r in cs:
            for c in ((r.get("search") or {}).get("citations") or []):
                u = c.get("url") if isinstance(c, dict) else None
                if u:
                    dom[_domain(u)] += 1
        s[m] = {"s1_answered_calls": len(cs),
                "searches_per_call": float(np.mean([_search_n(r) for r in cs])),
                "sources_per_call": float(np.mean([len((r.get("search") or {}).get("sources") or []) for r in cs])),
                "citations_per_call": float(np.mean([len((r.get("search") or {}).get("citations") or []) for r in cs])),
                "share_with_citation": float(np.mean([bool((r.get("search") or {}).get("citations")) for r in cs])),
                "top20_cited_domains": dom.most_common(20)}
    d["5_search"] = s
    # 6. cost (ESTIMATE)
    cost, tot = {}, 0.0
    for m in MODELS:
        for c in CONDS:
            rs = [r for r in raw_all if r["model_requested"] == m and r["condition"] == c]
            parts = [p for r in rs for p in (r.get("usage_parts") if r.get("usage_parts") is not None
                                             else ([BG.legacy_part(r)] if r.get("input_tokens") is not None else []))]
            tin = sum(p.get("input_tokens") or 0 for p in parts)
            tout = sum((p.get("output_tokens") or 0) + ((p.get("thinking_tokens") or 0) if m == GEM4 else 0) for p in parts)
            usd = sum(BG.record_cost(r) for r in rs)
            tot += usd
            cost[f"{m}|{c}"] = {"records": len(rs), "records_with_tokens": sum(1 for r in rs if r.get("input_tokens") is not None),
                                "billed_requests": len(parts), "input_tokens": tin, "output_tokens_billed": tout,
                                "searches_billed": sum(p.get("n_searches") or 0 for p in parts), "usd": usd}
    d["6_cost"] = {"BASIS": "recorded usage of every billed request (usage_parts) x list prices of section 4.5 "
                            "(budget_v0_42.record_cost: batch/standard token prices, Google thinking billed as output, "
                            "search fees); all raw attempts; the v0.23 judge's spend is not in the raw file",
                   "per_model_condition": cost, "total_usd": tot}
    return d


def recognition_codes_by_run(D, model, cond):
    out = collections.defaultdict(dict)
    for r in D.A:
        if r["model"] == model and r["condition"] == cond:
            out[(r["substrate"], r["brand"])][r["run"]] = int(r["recognized"])
    return out


# =========================================================================== orchestration
class Halt(RuntimeError):
    pass


def score_t4(raw_all, A, B, t3, cfg, gates):
    """raw_all: every raw line; A/B: coded rows (coder output); t3: load_t3_table(); gates: dict with
    'passed' (bool) and 'enforce' (bool)."""
    if gates.get("enforce") and not gates.get("passed"):
        raise Halt("parity gates not all passed: no t4 statistic is computed (section 5.3)")
    calls = C.dedupe_calls(raw_all)
    mcs, served_excl = manipulation_checks(calls)
    excl = excluded_set(mcs["MC_Complete"])
    brands = list(t3)
    D = Data(brands, A, B, excluded=served_excl)
    hyps = {"H_Gen_Presence": h_gen_presence(D, t3, excl, cfg),
            "H_Gen_Phi": h_gen_phi(D, t3, excl, cfg), "H_Search_Presence": h_search(D, excl, cfg)}
    desc = descriptives(D, [r for r in B if r["call_id"] not in served_excl], calls, raw_all, t3, excl)
    mcs["MC_Parity"] = {"passed": bool(gates.get("passed")), "detail": gates.get("detail")}
    out = {"phase": PHASE_ID, "prereg": "osf/v42/prereg/PRE_REGISTRATION_v0_42.md (revision r2)",
           "prereg_tag": C.PREREG_TAG, "seeds": SEEDS, "draws": {"permutation": cfg.n_perm, "bootstrap": cfg.n_boot},
           "panels": {"L6": L6, **PANELS}, "models_excluded_condition": sorted(f"{m}|{c}" for m, c in excl),
           "manipulation_checks": mcs, "verdicts": hyps, "descriptives": desc}
    return out, brand_rows(D, t3, excl)


def brand_rows(D, t3, excl):
    pis = {f"pi_{m}_{c}": pi_hat(D, [m], c) for m in MODELS for c in CONDS}
    panels = {}
    for pn in ("N3",):
        for c in CONDS:
            ms = _models_ok(PANELS[pn], c, excl)
            if ms:
                panels[f"{pn}_{c}"] = (pi_hat(D, ms, c), phi_panel(D, ms, c))
    rows = []
    for (s, b) in D.brands:
        r = {"substrate": s, "brand": b, "t3_k_per_model": json.dumps(t3[(s, b)]["k"]), "t3_pi_hat": t3[(s, b)]["pi"],
             "t3_phi": t3[(s, b)]["phi"], "t3_phi_partition": t3[(s, b)]["partition"]}
        for k, v in pis.items():
            r[k] = v[(s, b)]
        for k, (p, ph) in panels.items():
            r[f"pi_{k}"] = p[(s, b)]
            r[f"phi_{k}"] = ph[(s, b)][0]
            r[f"phi_partition_{k}"] = ph[(s, b)][1]
        rows.append(r)
    return rows


def write_outputs(out, rows, verdicts_path, table_path):
    Path(verdicts_path).parent.mkdir(parents=True, exist_ok=True)
    json.dump(sv._clean(out), open(verdicts_path, "w"), indent=2, allow_nan=False)
    fields = []
    for r in rows:
        for k in r:
            if k not in fields:
                fields.append(k)
    with open(table_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if (v is None or (isinstance(v, float) and not np.isfinite(v))) else v)
                        for k, v in r.items()})


def real_gates():
    """P1 recomputed; P2 and P3 read from their records (written by the coder and the probe export)."""
    p1 = parity_p1(out_path=None)
    p2 = json.load(open(P2_PATH)) if P2_PATH.exists() else {"passed": False}
    p3 = json.load(open(P3_PATH)) if P3_PATH.exists() else {}
    p3ok = bool(p3.get("artifact_checksums_all_match"))
    return {"passed": bool(p1["passed"] and p2.get("passed") and p3ok), "enforce": True,
            "detail": {"P1": p1["passed"], "P2": p2.get("passed"), "P3": p3ok}}


def main():
    ap = argparse.ArgumentParser(description="AIAS v0.42 scorer")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--parity-p1", action="store_true")
    g.add_argument("--synthetic", metavar="DIR", help="score DIR/t4_raw.jsonl + DIR/coded (synthetic files only); outputs to DIR/_score")
    g.add_argument("--run", action="store_true", help="the real scoring (refuses unless the prereg tag is on origin)")
    ap.add_argument("--draws", type=int, default=None, help="override permutation/bootstrap draws (tests only)")
    a = ap.parse_args()
    cfg = Cfg(*(a.draws,) * 2) if a.draws else Cfg()
    if a.parity_p1:
        r = parity_p1()
        print(f"P1 {'PASS' if r['passed'] else 'FAIL'}: brands={r['brands_compared']} k_exact={r['k_per_model_exact']} "
              f"pi_exact={r['pi_hat_exact']} phi_exact={r['phi_exact']} -> {P1_PATH}")
        return 0 if r["passed"] else 2
    try:
        if a.synthetic:
            d = Path(a.synthetic).resolve()
            raw = C.read_raw(d / "t4_raw.jsonl")
            A, B = C.read_tables(d / "coded")
            gates = {"passed": True, "enforce": False, "detail": "SKIPPED_SYNTHETIC"}
            out, rows = score_t4(raw, A, B, load_t3_table(), cfg, gates)
            write_outputs(out, rows, d / "_score/v42_verdicts.json", d / "_score/v42_brand_table.csv")
            dest = d / "_score"
        else:
            if not C.tag_on_origin():
                print(f"[v42] REFUSED: tag {C.PREREG_TAG} is not on origin; real t4 data is not read", file=sys.stderr)
                return 3
            gates = real_gates()
            raw = C.read_raw(C.REAL_RAW)
            A, B = C.read_tables(C.DEFAULT_OUT)
            out, rows = score_t4(raw, A, B, load_t3_table(), cfg, gates)
            write_outputs(out, rows, VERDICTS, BRAND_TABLE)
            dest = VERDICTS.parent
    except C.Refused as e:
        print(f"[v42] REFUSED: {e}", file=sys.stderr)
        return 3
    except Halt as e:
        print(f"[v42] HALT: {e}", file=sys.stderr)
        return 4
    print(f"wrote {dest}")
    for k, v in out["verdicts"].items():
        print(f"  {k}: {v.get('verdict', v.get('label'))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
