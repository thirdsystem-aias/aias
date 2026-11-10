#!/usr/bin/env python3
"""
score_v0_44.py -- AIAS(TM) v0.44 scorer (industry-breadth wave). Transcribes PRE_REGISTRATION_v0_44.md (draft r1)
sections 2 and 5: exactly the three pre-registered tests (H_Spread, H_Tier, H_Separation), the manipulation checks
and the descriptives. THE PRE-REGISTRATION PROSE IS AUTHORITATIVE; where it is silent the simplest faithful option
is taken and listed below (SCORER_NOTES). The real scoring runs ONCE (--run refuses if the verdicts file exists).

Imported unchanged from osf/v42/scripts/score_v0_42.py (which takes the kernel and helpers from
osf/v41/scripts/score_v41.py): phi_m (the v1.8 phi kernel on M models, with its zero / saturated / defined
partitions), within_ranks, _pearson, spearman, Data, pi_hat, phi_panel, pair_arrays, bootstrap, served_ok, rel3_of,
model_arrays, parity_p1, Cfg. Re-implemented in r1 with ranks centred within industry (note N15): rho_pw (in place of
pooled_within_rho), perm_p (in place of perm_p_within) and rel1 (in place of rel1_of); each is the imported function
with the centred statistic. Importing score_v0_42 bootstraps the v0.42 HOME shim (the certified
modules read ~/aias), so this script is re-executed once with HOME pointing at a temporary directory whose `aias`
links to this worktree; nothing outside the worktree is read.

SCORER_NOTES (choices where the pre-registration is silent)
 N1  pi_hat_b = sum of mentions / answered Phase B calls of b's industry over the 3 models and the runs
     (score_v0_42.pi_hat); equals sum k / 54 when complete. "Rated" = phi_b defined and pi_hat_b >= 1/6 (the
     proportional form of "at least 9 of 54 cells", identical when complete).
 N2  phi per run needs all 3 models to have all 6 Phase B answers of the industry in that run (score_v0_42.phi_runs);
     phi_b = mean over defined runs if >= 2 runs are defined (with run 3 dropped under section 4.5: both runs).
 N3  C_phi = 100 (1 - phi_b / phi_max), phi_max = 6M / (M - 1) = 9 for M = 3.
 N4  Permutation: y shuffled within industry, rho_pw recomputed on every draw; hit if rho_perm >= rho_obs - 1e-12;
     p = (1 + hits) / (draws + 1). Bootstrap: units resampled with replacement within industry; percentile 95%;
     draws with a non-finite statistic dropped and counted. Every alongside variant re-uses its test's seed.
 N5  H_Tier alongside "eligible rank in place of tier": x = -eligible_rank (rank 1 = largest), so a positive rho
     means larger brands have higher Presence, as for the tier score.
 N6  H_Spread interval: bootstrap of SD_i (population SD, ddof 0) over the industry's non-ghost units, seed 440041.
 N7  H_Separation: ghost units are included if rated (section 2.1 excludes ghosts from H_Spread and H_Tier only).
     "Interval inside (-0.70, 0.70)" = lower > -0.70 and upper < 0.70.
 N8  Drop rule: a model with < 90% of its expected calls answered in a phase (Phase B 3 x 48 = 144, or 96 with run 3
     dropped; Phase A 159) is excluded from that phase. Any model excluded from Phase B -> all three primary tests
     UNDETERMINED; the statistics are then reported on the remaining models as descriptives.
 N9  MC_Window: span first start -> last end <= 72 h and every start inside the window (US Central dates; the
     window recorded in the budget state file by acquire_v0_44.py, else 2026-11-24..2026-11-28).
 N10 Descriptive 6 (non-registry brands): candidate names are Markdown bold spans and the heads of list items
     (text before the first ':', ' - ', ' – ', ' — ', '(' or ','), 1-6 words, starting with an upper-case letter
     or a digit, not matched by any alias of the industry's registry; counted once per answer. Heuristic,
     descriptive only.
 N11 MC_Truncation: finish reason contains "max_tokens" or "max_output_tokens", or equals "length".
     Refusals (descriptive 8): finish reasons containing refus / content_filter / safety / prohibit / blocklist.
 N12 Cost (descriptive 9, MC_Budget): budget_v0_44.record_cost of every raw line (every attempt).
 N13 NaN rho (degenerate data) -> verdict UNDETERMINED.
 N14 Gate P2's locked probe hash is the one in osf/v44/LOCK_MANIFEST_v0_44.sha256 (written at the lock).
 N15 (r1 change, section 2.1) rho_pw uses ranks centred within industry (rho_pw below); the imported
     score_v41.pooled_within_rho does not centre, which with unequal industry sizes biases it upwards and
     breaks the 'identical up to sign' property of H_Separation's raw-phi variant. rel1 (descriptive 4) and
     the permutation use the same rho_pw. phi kernel, pi_hat and bootstrap are imported unchanged.
 N16 Before ranking, values are rounded to 10 decimals: phi of mirror-image count vectors (e.g. [4,5,6] and
     [0,1,2]) is equal in exact arithmetic but not always in floating point, which would split a tie.

Modes: --parity-p1 | --synthetic DIR | --run   (--run refuses unless tag v0.44-prereg-r1 is on origin, and if the
verdicts file already exists)
"""
import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parents[1] / "v42" / "scripts"))
import score_v0_42 as S42     # noqa: E402  (bootstraps ROOT / HOME shim, as in v0.42)
import code_v0_44 as C        # noqa: E402
import budget_v0_44 as BG     # noqa: E402

import argparse         # noqa: E402
import collections      # noqa: E402
import csv              # noqa: E402
import itertools        # noqa: E402
import json             # noqa: E402
import re               # noqa: E402
from datetime import datetime, timedelta, timezone  # noqa: E402
from zoneinfo import ZoneInfo  # noqa: E402

import numpy as np      # noqa: E402

sv = S42.sv
phi_m, pooled_within_rho, spearman = sv.phi_m, sv.pooled_within_rho, sv.spearman
Data, pi_hat, phi_panel, phi_runs = S42.Data, S42.pi_hat, S42.phi_panel, S42.phi_runs
pair_arrays, perm_p_within, bootstrap = S42.pair_arrays, S42.perm_p_within, S42.bootstrap
served_ok, rel1_of, rel3_of, model_arrays, Cfg = S42.served_ok, S42.rel1_of, S42.rel3_of, S42.model_arrays, S42.Cfg

ROOT = C.ROOT
V44 = ROOT / "osf/v44"
PHASE_ID = "v0.44"
COND = "S0"
F = 6
M_MODELS = ["claude-fable-5-2", "gpt-6-astra", "gemini-4-argon"]
M = len(M_MODELS)
PHI_MAX = F * M / (M - 1)                 # 9.0
RATED_FLOOR = 1.0 / 6.0
TIER_SCORE = {"L": 3, "C": 2, "S": 1}
SPREAD_SD = 0.15                          # counts: spread_thresholds(I) -> (6, 3) for 8 industries, (5, 3) for 7
TIER_CONF, TIER_FALS, ALPHA = 0.40, 0.20, 0.05
SEP_MAX, SEP_CI, SEP_N_FLOOR = 0.50, 0.70, 40
DROP_SHARE, COMPLETE_SHARE, TRUNC_FLAG = 0.90, 0.98, 0.05
SEEDS = {"H_Spread": 440041, "H_Tier": 440042, "H_Separation": 440043, "descriptives": 440045}
N_PERM = N_BOOT = 10_000
WINDOW_DATES = ("2026-11-24", "2026-11-28")
CENTRAL = ZoneInfo("America/Chicago")
PHARMACY_OTHER_METRIC = ("Health Mart", "Good Neighbor Pharmacy")
CROSS_FRAME = ("Kroger", "Publix", "Albertsons")
VERDICTS = V44 / "v44_verdicts.json"
UNIT_TABLE = V44 / "v44_unit_table.csv"
P1_PATH = V44 / "prereg/parity_P1_v0_44.json"
MANIFEST = V44 / "LOCK_MANIFEST_v0_44.sha256"
STATE_PATH = V44 / "data/v44_budget_state.json"
NAN = float("nan")


class Halt(RuntimeError):
    pass


# =========================================================================== rho_pw (r1: centred within-industry ranks)
def centred_ranks(values, groups):
    """Average ranks within each industry (score_v41.within_ranks), minus the industry's mean rank (n_i + 1) / 2.
    Values are rounded to 10 decimals first, so that floating-point noise does not split exact ties (note N16)."""
    r = sv.within_ranks(np.round(np.asarray(values, float), 10), groups)
    g = np.asarray(groups)
    for k in dict.fromkeys(g):
        i = g == k
        r[i] = r[i] - r[i].mean()
    return r


def rho_pw(x, y, groups):
    """Pooled within-industry Spearman (section 2.1, r1): Pearson's r of the ranks taken within industry and centred
    within industry. Without the centring (score_v41.pooled_within_rho) unequal industry sizes add a between-industry
    term, (n_i + 1) / 2, shared by x and y (null mean +0.056 on the H_Tier units instead of 0; tests). Identical to
    score_v41.pooled_within_rho when every industry has the same number of units."""
    if len(x) < 3:
        return NAN
    return sv._pearson(centred_ranks(x, groups), centred_ranks(y, groups))


def perm_p(x, y, g, obs, seed, n_draws):
    """One-sided permutation p: y shuffled within industry, rho_pw recomputed on every draw (as
    score_v0_42.perm_p_within, with rho_pw). p = (1 + #{rho_perm >= rho_obs - 1e-12}) / (n_draws + 1)."""
    if not np.isfinite(obs):
        return NAN
    rng = np.random.default_rng(seed)
    gidx = sv._group_index(g)
    hits = 0
    for _ in range(n_draws):
        yp = y.copy()
        for gi in gidx:
            yp[gi] = y[rng.permutation(gi)]
        hits += bool(rho_pw(x, yp, g) >= obs - 1e-12)
    return (1 + hits) / (n_draws + 1)


def rel1(K, Nn, g):
    """Descriptive 4: mean rho_pw over the run pairs of k/n (as score_v0_42.rel1_of, with rho_pw)."""
    with np.errstate(invalid="ignore", divide="ignore"):
        rates = np.where(Nn > 0, K / np.where(Nn > 0, Nn, 1), np.nan)
    vals = []
    for a, b in itertools.combinations(range(K.shape[0]), 2):
        m = np.isfinite(rates[a]) & np.isfinite(rates[b])
        if m.sum() >= 3:
            vals.append(rho_pw(rates[a][m], rates[b][m], g[m]))
    vals = [v for v in vals if np.isfinite(v)]
    return float(np.mean(vals)) if vals else NAN


# =========================================================================== design
def design(registry, drop_run3=False):
    inds = list(registry)
    runs = (1, 2) if drop_run3 else (1, 2, 3)
    n_b, n_a = F * len(inds), sum(len(v) for v in registry.values())
    return {"industries": inds, "runs_b": runs, "expected": {"B": n_b * len(runs), "A": n_a},
            "expected_total": M * (n_b * len(runs) + n_a)}


def in_design(rec, dz):
    if rec.get("model_requested") not in M_MODELS or rec.get("condition") != COND:
        return False
    if rec.get("substrate") not in dz["industries"]:
        return False
    if rec.get("phase") == "B":
        return rec.get("run") in dz["runs_b"]
    return rec.get("phase") == "A" and rec.get("run") == 1


def _truncated(rec):
    fr = str(rec.get("finish_reason") or "").lower()
    return "max_tokens" in fr or "max_output_tokens" in fr or fr == "length"


def manipulation_checks(calls_all, raw_all, dz, window=WINDOW_DATES):
    """calls_all: deduplicated raw records. -> (mcs, excluded call ids, {phase: [excluded models]})."""
    outside = [r["call_id"] for r in calls_all if not in_design(r, dz)]
    calls = [r for r in calls_all if in_design(r, dz)]
    excluded, mism, missing = set(outside), [], []
    for r in calls:
        if C.is_answered(r):
            if not r.get("served_model"):
                missing.append(r["call_id"])
            elif not served_ok(r["model_requested"], r["served_model"]):
                mism.append({"call_id": r["call_id"], "requested": r["model_requested"], "served": r["served_model"]})
                excluded.add(r["call_id"])
    per = {(m, ph): 0 for m in M_MODELS for ph in ("B", "A")}
    for r in calls:
        if C.is_answered(r) and r["call_id"] not in excluded:
            per[(r["model_requested"], r["phase"])] += 1
    per_mp = {f"{m}|{ph}": {"answered": n, "expected": dz["expected"][ph], "share": n / dz["expected"][ph],
                            "excluded_below_90pct": n / dz["expected"][ph] < DROP_SHARE}
              for (m, ph), n in per.items()}
    drop = {ph: [m for m in M_MODELS if per_mp[f"{m}|{ph}"]["excluded_below_90pct"]] for ph in ("B", "A")}
    n_ans = sum(per.values())
    mcs = {"MC_Complete": {"answered": n_ans, "expected": dz["expected_total"], "share": n_ans / dz["expected_total"],
                           "pass": n_ans / dz["expected_total"] >= COMPLETE_SHARE, "per_model_phase": per_mp,
                           "dropped_models": drop, "outside_design": {"n": len(outside), "call_ids": outside[:50]}},
           "MC_Served": {"n_mismatched": len(mism), "mismatched": mism[:50], "ok_calls_without_served_id": len(missing),
                         "pass": not mism}}
    tr = collections.defaultdict(lambda: [0, 0])
    for r in calls:
        tr[r["model_requested"]][0] += 1
        tr[r["model_requested"]][1] += int(_truncated(r))
    mcs["MC_Truncation"] = {m: {"calls": a, "at_cap": b, "share": b / a, "flag_above_5pct": b / a > TRUNC_FLAG}
                            for m, (a, b) in sorted(tr.items())}
    starts = sorted(r["started_utc"] for r in calls if r.get("started_utc"))
    ends = sorted(r["finished_utc"] for r in calls if r.get("finished_utc"))
    w0 = datetime.fromisoformat(window[0]).replace(tzinfo=CENTRAL)
    w1 = datetime.fromisoformat(window[1]).replace(tzinfo=CENTRAL) + timedelta(days=1)
    win = {"window_us_central": list(window), "first_call_utc": starts[0] if starts else None,
           "last_call_utc": ends[-1] if ends else None}
    if starts and ends:
        span = (datetime.fromisoformat(ends[-1]) - datetime.fromisoformat(starts[0])).total_seconds() / 3600
        inside = all(w0 <= datetime.fromisoformat(s) < w1 for s in starts)
        win.update(span_hours=span, all_starts_inside_window=inside, **{"pass": span <= 72 and inside})
    else:
        win.update(span_hours=None, all_starts_inside_window=None, **{"pass": False})
    mcs["MC_Window"] = win
    spend = sum(BG.record_cost(r) for r in raw_all)
    sent = {r["call_id"] for r in raw_all}
    mcs["MC_Budget"] = {"spend_usd": spend, "cap_usd": BG.BUDGET_CAP_USD, "pause_usd": BG.PAUSE_AT_USD,
                        "pass": spend <= BG.BUDGET_CAP_USD, "raw_lines": len(raw_all),
                        "design_calls_never_sent": dz["expected_total"] - len(sent & {r["call_id"] for r in calls})}
    return mcs, excluded, drop


# =========================================================================== unit-level values
def unit_keys(registry):
    return [(ind, u["unit_id"]) for ind, units in registry.items() for u in units]


def unit_info(registry):
    return {(ind, u["unit_id"]): u for ind, units in registry.items() for u in units}


def c_phi(phi):
    return None if phi is None else 100.0 * (1.0 - phi / PHI_MAX)


def unit_values(D, registry, models):
    pis = pi_hat(D, models, COND)
    phis = phi_panel(D, models, COND)
    out = {}
    for key in unit_keys(registry):
        phi, part, parts = phis[key]
        pi = pis[key]
        out[key] = {"pi": pi, "phi": phi, "partition": part, "run_partitions": parts, "c_phi": c_phi(phi),
                    "rated": bool(phi is not None and np.isfinite(pi) and pi >= RATED_FLOOR - 1e-12)}
    return out


# =========================================================================== tests
def spread_thresholds(n_industries):
    """Section 2.2: CONFIRMED if >= floor(0.8 I) industries show spread (8 -> 6, 7 -> 5); FALSIFIED if fewer than
    half do, i.e. <= ceil(I / 2) - 1 (8 -> 3, 7 -> 3); MARGINAL otherwise."""
    return int(np.floor(0.8 * n_industries + 1e-9)), int(np.ceil(n_industries / 2)) - 1


def _verdict_spread(n_spread, n_industries=8):
    conf, fals = spread_thresholds(n_industries)
    if n_spread >= conf:
        return "CONFIRMED"
    if n_spread <= fals:
        return "FALSIFIED"
    return "MARGINAL"


def h_spread(V, registry, cfg, undetermined=None):
    info = unit_info(registry)
    keys = [k for k in unit_keys(registry) if info[k]["tier"] != "G" and np.isfinite(V[k]["pi"])]
    y = np.array([V[k]["pi"] for k in keys])
    g = np.array([k[0] for k in keys])
    per = {}
    for ind in registry:
        v = y[g == ind]
        per[ind] = {"n": int(len(v)), "sd": float(np.std(v)) if len(v) else NAN,
                    "range": [float(v.min()), float(v.max())] if len(v) else None,
                    "share_at_0": float(np.mean(v == 0)) if len(v) else None}
        per[ind]["spread"] = bool(np.isfinite(per[ind]["sd"]) and per[ind]["sd"] >= SPREAD_SD)
    inds = list(registry)
    b = bootstrap(g, SEEDS["H_Spread"], cfg.n_boot,
                  lambda i: {ind: float(np.std(y[i][g[i] == ind])) for ind in inds})
    for ind in inds:
        per[ind]["sd_ci95"] = b[ind]["ci95"]
    n_spread = sum(per[i]["spread"] for i in inds)
    conf, fals = spread_thresholds(len(inds))
    out = {"tier": "PRIMARY", "seed": SEEDS["H_Spread"], "n_industries": len(inds), "n_with_spread": n_spread,
           "per_industry": per, "thresholds": {"confirmed_at_least": conf, "falsified_at_most": fals},
           "rule": f"spread if SD_i >= 0.15; CONFIRMED if >= {conf} of {len(inds)} industries show spread; "
                   f"FALSIFIED if <= {fals}; MARGINAL otherwise"}
    out["verdict"] = undetermined and "UNDETERMINED" or _verdict_spread(n_spread, len(inds))
    if undetermined:
        out["reason"] = undetermined
    return out


def _rank_test(xd, yd, keys, seed, cfg):
    keys, x, y, g = pair_arrays({k: xd[k] for k in keys}, {k: yd[k] for k in keys})
    n = len(keys)
    rho = rho_pw(x, y, g) if n >= 3 else NAN
    t = {"n": n, "rho": rho}
    if n >= 3 and np.isfinite(rho):
        t["p_perm"] = perm_p(x, y, g, rho, seed, cfg.n_perm)
        b = bootstrap(g, seed, cfg.n_boot, lambda i: {"rho": rho_pw(x[i], y[i], g[i])})
        t["ci95_rho"] = b["rho"]["ci95"]
    t["per_industry_rho"] = {ind: (spearman(x[g == ind], y[g == ind]) if (g == ind).sum() >= 3 else NAN)
                             for ind in dict.fromkeys(g)}
    return t


def verdict_tier(rho, p):
    if not np.isfinite(rho) or p is None or not np.isfinite(p):
        return "UNDETERMINED"
    if rho >= TIER_CONF and p < ALPHA:
        return "CONFIRMED"
    if rho < TIER_FALS:
        return "FALSIFIED"
    return "MARGINAL"


def h_tier(V, registry, cfg, undetermined=None):
    info = unit_info(registry)
    keys = [k for k in unit_keys(registry) if info[k]["tier"] != "G"]
    x = {k: float(TIER_SCORE[info[k]["tier"]]) for k in keys}
    y = {k: V[k]["pi"] for k in keys}
    seed = SEEDS["H_Tier"]
    t = _rank_test(x, y, keys, seed, cfg)
    out = {"tier": "PRIMARY", "seed": seed, **t,
           "rule": "CONFIRMED if rho >= 0.40 and p < 0.05; FALSIFIED if rho < 0.20; MARGINAL otherwise"}
    out["verdict"] = "UNDETERMINED" if undetermined else verdict_tier(t["rho"], t.get("p_perm"))
    if undetermined:
        out["reason"] = undetermined
    xr = {k: -float(info[k]["eligible_rank"]) for k in keys if info[k]["eligible_rank"] is not None}
    alt = {"eligible_rank": _rank_test(xr, y, [k for k in keys if k in xr], seed, cfg)}
    if "FAS" in registry:
        alt["without_FAS"] = _rank_test(x, y, [k for k in keys if k[0] != "FAS"], seed, cfg)
    other = [k for k in keys if info[k]["brand"] in PHARMACY_OTHER_METRIC]
    if other:
        alt["without_pharmacy_units_from_other_metric"] = {
            "units_removed": [info[k]["brand"] for k in other],
            **_rank_test(x, y, [k for k in keys if k not in other], seed, cfg)}
    means = collections.defaultdict(list)
    for k in keys:
        if np.isfinite(y[k]):
            means[(k[0], info[k]["tier"])].append(y[k])
    alt["mean_pi_by_industry_tier"] = {f"{i}|{tr}": float(np.mean(v)) for (i, tr), v in sorted(means.items())}
    out["reported_alongside"] = alt
    return out


def verdict_sep(n, rho, ci):
    if n < SEP_N_FLOOR:
        return "UNDETERMINED"
    if not np.isfinite(rho) or ci is None:
        return "UNDETERMINED"
    if abs(rho) <= SEP_MAX and ci[0] > -SEP_CI and ci[1] < SEP_CI:
        return "CONFIRMED"
    if abs(rho) > SEP_MAX:
        return "FALSIFIED"
    return "MARGINAL"


def h_separation(V, registry, cfg, undetermined=None):
    info = unit_info(registry)
    rated = [k for k in unit_keys(registry) if V[k]["rated"]]
    seed = SEEDS["H_Separation"]
    keys, x, y, g = pair_arrays({k: V[k]["pi"] for k in rated}, {k: V[k]["c_phi"] for k in rated})
    n = len(keys)
    rho = rho_pw(x, y, g) if n >= 3 else NAN
    ci = None
    if n >= 3 and np.isfinite(rho):
        ci = bootstrap(g, seed, cfg.n_boot, lambda i: {"rho": rho_pw(x[i], y[i], g[i])})["rho"]["ci95"]
    out = {"tier": "PRIMARY", "seed": seed, "n_rated": n, "rho": rho, "ci95_rho": ci,
           "rule": "UNDETERMINED if < 40 rated units; CONFIRMED if |rho| <= 0.50 and the 95% interval lies inside "
                   "(-0.70, 0.70); FALSIFIED if |rho| > 0.50; MARGINAL otherwise"}
    out["verdict"] = "UNDETERMINED" if undetermined else verdict_sep(n, rho, ci)
    if undetermined:
        out["reason"] = undetermined
    _, xr, yr, gr = pair_arrays({k: V[k]["pi"] for k in rated}, {k: V[k]["phi"] for k in rated})
    unrated = collections.defaultdict(lambda: [0, 0])
    for k in unit_keys(registry):
        unrated[f"{k[0]}|{info[k]['tier']}"][0] += int(not V[k]["rated"])
        unrated[f"{k[0]}|{info[k]['tier']}"][1] += 1
    runs = collections.Counter(p for k in unit_keys(registry) for p in V[k]["run_partitions"])
    out["reported_alongside"] = {
        "per_industry_rho": {ind: (spearman(x[g == ind], y[g == ind]) if (g == ind).sum() >= 3 else NAN)
                             for ind in registry},
        "unrated_share_by_industry_tier": {k: {"unrated": a, "units": b, "share": a / b} for k, (a, b) in
                                           sorted(unrated.items())},
        "partition_counts_per_run": dict(runs),
        "unit_partitions": dict(collections.Counter(V[k]["partition"] for k in unit_keys(registry))),
        "rho_with_raw_phi": rho_pw(xr, yr, gr) if len(xr) >= 3 else NAN}
    return out


# =========================================================================== descriptives (section 2.6)
LIST_HEAD = re.compile(r"(?m)^\s*(?:\d+[.)]|[-*•])\s+(.+)$")
BOLD = re.compile(r"\*\*([^*\n]{1,80})\*\*|__([^_\n]{1,80})__")


def candidate_names(text):
    found = set()
    for m in BOLD.finditer(text):
        found.add((m.group(1) or m.group(2)).strip())
    for m in LIST_HEAD.finditer(text):
        head = re.split(r":| - | – | — |\(|,", m.group(1).replace("**", "").replace("__", ""))[0]
        found.add(head.strip())
    out = set()
    for c in found:
        c = c.strip(" *_#.:;–—-")
        if c and 1 <= len(c.split()) <= 6 and (c[0].isupper() or c[0].isdigit()):
            out.add(c)
    return out


def non_registry_names(calls, registry):
    Mt = C.Matcher(registry)
    cnt = collections.defaultdict(collections.Counter)
    for r in calls:
        if r["phase"] != "B" or not C.is_answered(r) or r["substrate"] not in registry:
            continue
        for c in candidate_names(C.normalize(C.strip_urls(r["text"]))):
            if not any(Mt.mentions(r["substrate"], c).values()):
                cnt[r["substrate"]][c] += 1
    return {ind: {"distinct": len(cnt[ind]), "top10": cnt[ind].most_common(10)} for ind in registry}


def descriptives(D, V, registry, calls, raw_all, models, recog):
    info = unit_info(registry)
    keys = unit_keys(registry)
    d = {"seed_reserved": SEEDS["descriptives"], "note": "descriptive only; no verdicts"}
    pres = {}
    for m in models:
        pm = pi_hat(D, [m], COND)
        for ind in registry:
            for tr in ("L", "C", "S", "G", "all"):
                v = np.array([pm[k] for k in keys if k[0] == ind and (tr == "all" or info[k]["tier"] == tr)
                              and np.isfinite(pm[k])])
                if len(v):
                    pres[f"{m}|{ind}|{tr}"] = {"n": int(len(v)), "mean": float(v.mean()), "sd": float(v.std()),
                                               "min": float(v.min()), "max": float(v.max()),
                                               "share_0": float(np.mean(v == 0)), "share_1": float(np.mean(v == 1))}
    d["1_presence_by_model_industry_tier"] = pres
    rs = {}
    for m in M_MODELS:
        for ind in registry:
            v = [recog[(ind, u["unit_id"])].get(m) for u in registry[ind]]
            v = [x for x in v if x is not None]
            rs[f"{m}|{ind}"] = {"recognized": int(sum(v)), "coded": len(v), "share": (sum(v) / len(v)) if v else None}
    gap = collections.Counter()
    for k in keys:
        if all(recog[k].get(m) == 1 for m in M_MODELS) and V[k]["pi"] == 0:
            gap[info[k]["tier"]] += 1
    d["2_recognition"] = {"share_per_model_industry": rs, "recognised_by_all_three_with_pi_0_by_tier": dict(gap)}
    d["3_ghosts"] = {f"{k[0]}|{info[k]['brand']}": {"pi": V[k]["pi"], "recognition": recog[k]}
                     for k in keys if info[k]["tier"] == "G"}
    g = np.array([k[0] for k in keys])
    rel = {}
    for m in models:
        K, Nn = model_arrays(D, m, COND, keys)
        r1 = rel1(K, Nn, g)
        rel[m] = {"rel1": r1, "rel3": rel3_of(r1)}
    d["4_run_reliability"] = rel
    agree = {}
    for a, b in itertools.combinations(models, 2):
        kk, x, y, gg = pair_arrays(pi_hat(D, [a], COND), pi_hat(D, [b], COND), keys)
        agree[f"{a}~{b}"] = {"n": len(kk), "rho_pw": rho_pw(x, y, gg) if len(kk) >= 3 else NAN}
    d["5_model_agreement"] = agree
    d["6_non_registry_names_in_phase_b"] = non_registry_names(calls, registry)
    cross = {}
    for name in CROSS_FRAME:
        units = [k for k in keys if info[k]["brand"] == name or info[k]["brand"].startswith(name + " ")]
        cross[name] = {f"{k[0]}:{info[k]['brand']}": V[k]["pi"] for k in units}
    d["7_units_in_two_industries"] = cross
    form = {}
    named = collections.Counter()
    for r in D_B_ROWS:
        named[r["call_id"]] += int(r["mentioned"])
    for m in M_MODELS:
        rs_ = [r for r in calls if r["model_requested"] == m]
        ans = [r for r in rs_ if C.is_answered(r)]
        wa = [len(r["text"].split()) for r in ans if r["phase"] == "A"]
        wb = [len(r["text"].split()) for r in ans if r["phase"] == "B"]
        form[m] = {"words_A_mean": float(np.mean(wa)) if wa else None, "words_B_mean": float(np.mean(wb)) if wb else None,
                   "registry_units_per_B_answer": float(np.mean([named[r["call_id"]] for r in ans if r["phase"] == "B"]))
                   if wb else None,
                   "finish_reasons": dict(collections.Counter(str(r.get("finish_reason")) for r in rs_)),
                   "refusals": sum(1 for r in rs_ if re.search(r"refus|content_filter|safety|prohibit|blocklist",
                                                                 str(r.get("finish_reason") or ""), re.I)),
                   "unanswered": sum(1 for r in rs_ if not C.is_answered(r)),
                   "phase_A_ambiguous": sum(1 for r in D.A if r["model"] == m and r.get("label") == "ambiguous")}
    d["8_answer_form"] = form
    cost = {}
    for m in M_MODELS:
        for ph in ("B", "A"):
            rr = [r for r in raw_all if r.get("model_requested") == m and r.get("phase") == ph]
            parts = [p for r in rr for p in (r.get("usage_parts") or [])]
            cost[f"{m}|{ph}"] = {"raw_lines": len(rr), "billed_requests": len(parts),
                                 "input_tokens": sum(p.get("input_tokens") or 0 for p in parts),
                                 "output_tokens": sum(p.get("output_tokens") or 0 for p in parts),
                                 "thinking_tokens": sum(p.get("thinking_tokens") or 0 for p in parts),
                                 "usd": sum(BG.record_cost(r) for r in rr)}
    d["9_cost"] = {"per_model_phase": cost, "total_usd": sum(v["usd"] for v in cost.values()),
                   "basis": "budget_v0_44.record_cost of every raw line (recorded usage x list prices)"}
    return d


D_B_ROWS = []   # set by score() for descriptive 8


# =========================================================================== orchestration
def recognition(D, registry):
    rec = {k: {} for k in unit_keys(registry)}
    for r in D.A:
        k = (r["substrate"], r["brand"])
        if k in rec and int(r["run"]) == 1:
            rec[k][r["model"]] = int(r["recognized"])
    return rec


def score(raw_all, A, B, registry, cfg, gates, drop_run3=False, window=WINDOW_DATES):
    if gates.get("enforce") and not gates.get("passed"):
        raise Halt("parity gates not all passed: no statistic is computed (section 5.3)")
    dz = design(registry, drop_run3)
    calls = C.dedupe_calls(raw_all)
    mcs, excl_ids, drop = manipulation_checks(calls, raw_all, dz, window)
    mcs["MC_Parity"] = {"passed": bool(gates.get("passed")), "detail": gates.get("detail")}
    a_ok = [r for r in A if r["call_id"] not in excl_ids and r["model"] not in drop["A"]]
    b_ok = [r for r in B if r["call_id"] not in excl_ids and r["model"] not in drop["B"]]
    global D_B_ROWS
    D_B_ROWS = b_ok
    D = Data(unit_keys(registry), a_ok, b_ok)
    models = [m for m in M_MODELS if m not in drop["B"]]
    und = (f"{', '.join(drop['B'])} excluded from Phase B (answered < 90%): primary tests UNDETERMINED; statistics "
           f"below are on the remaining models, descriptive only") if drop["B"] else None
    V = unit_values(D, registry, models) if models else {k: {"pi": NAN, "phi": None, "partition": "undefined",
                                                             "run_partitions": [], "c_phi": None, "rated": False}
                                                         for k in unit_keys(registry)}
    hyps = {"H_Spread": h_spread(V, registry, cfg, und), "H_Tier": h_tier(V, registry, cfg, und),
            "H_Separation": h_separation(V, registry, cfg, und)}
    recog = recognition(D, registry)
    desc = descriptives(D, V, registry, calls, raw_all, models, recog)
    out = {"phase": PHASE_ID, "prereg": "osf/v44/prereg/PRE_REGISTRATION_v0_44.md", "prereg_tag": C.PREREG_TAG,
           "design": {**dz, "runs_b": list(dz["runs_b"]), "drop_run3": drop_run3, "models_used": models},
           "seeds": SEEDS, "draws": {"permutation": cfg.n_perm, "bootstrap": cfg.n_boot},
           "manipulation_checks": mcs, "verdicts": hyps, "descriptives": desc}
    return out, unit_rows(D, V, registry, recog)


def unit_rows(D, V, registry, recog):
    info = unit_info(registry)
    rows = []
    for k in unit_keys(registry):
        u = info[k]
        row = {"industry": k[0], "unit_id": k[1], "brand": u["brand"], "tier": u["tier"],
               "eligible_rank": u["eligible_rank"], "pi_hat": V[k]["pi"], "phi_b": V[k]["phi"],
               "phi_partition": V[k]["partition"], "phi_run_partitions": json.dumps(V[k]["run_partitions"]),
               "c_phi": V[k]["c_phi"], "rated": int(V[k]["rated"])}
        for m in M_MODELS:
            row[f"k_{m}"] = json.dumps([D.kk(COND, m, r, k[0], k[1]) for r in (1, 2, 3)])
            row[f"recognized_{m}"] = recog[k].get(m)
        rows.append(row)
    return rows


def write_outputs(out, rows, verdicts_path, table_path):
    S42.write_outputs(out, rows, verdicts_path, table_path)


def locked_probe_sha(manifest=MANIFEST):
    if not Path(manifest).exists():
        return None
    for line in Path(manifest).read_text(encoding="utf-8").splitlines():
        f = line.split()
        if len(f) == 2 and f[1].endswith("osf/v44/prereg/probes_v0_44.jsonl"):
            return f[0]
    return None


def parity_p1(out_path=P1_PATH):
    """P1 (section 5.3): the imported functions reproduce v0.41's t3 pi_hat and phi for all 112 omnibus brands."""
    return S42.parity_p1(out_path=out_path)


def state():
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def main(argv=None):
    ap = argparse.ArgumentParser(description="AIAS v0.44 scorer")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--parity-p1", action="store_true")
    g.add_argument("--synthetic", metavar="DIR", help="score DIR/v44_raw.jsonl + DIR/coded; outputs to DIR/_score")
    g.add_argument("--run", action="store_true", help="the real scoring, once (refuses unless the tag is on origin)")
    ap.add_argument("--draws", type=int, default=None, help="override permutation/bootstrap draws (tests only)")
    ap.add_argument("--drop-run3", action="store_true", help="synthetic only: score the design without run 3")
    a = ap.parse_args(argv)
    cfg = Cfg(a.draws, a.draws) if a.draws else Cfg(N_PERM, N_BOOT)
    if a.parity_p1:
        r = parity_p1()
        print(f"P1 {'PASS' if r['passed'] else 'FAIL'}: brands={r['brands_compared']} k_exact={r['k_per_model_exact']} "
              f"pi_exact={r['pi_hat_exact']} phi_exact={r['phi_exact']} -> {P1_PATH}")
        return 0 if r["passed"] else 2
    registry = C.load_registry()
    try:
        if a.synthetic:
            d = Path(a.synthetic).resolve()
            raw = C.read_raw(d / "v44_raw.jsonl")
            A, B = C.read_tables(d / "coded")
            gates = {"passed": True, "enforce": False, "detail": "SKIPPED_SYNTHETIC"}
            out, rows = score(raw, A, B, registry, cfg, gates, drop_run3=a.drop_run3)
            write_outputs(out, rows, d / "_score/v44_verdicts.json", d / "_score/v44_unit_table.csv")
            dest = d / "_score"
        else:
            if VERDICTS.exists():
                print(f"[v44] REFUSED: {VERDICTS} exists; the scorer runs once", file=sys.stderr)
                return 3
            if not C.tag_on_origin():
                print(f"[v44] REFUSED: tag {C.PREREG_TAG} is not on origin; real data is not read", file=sys.stderr)
                return 3
            raw = C.read_raw(C.REAL_RAW)
            p1 = parity_p1(out_path=None)
            p2 = C.probe_parity(raw, locked_sha=locked_probe_sha())
            gates = {"passed": bool(p1["passed"] and p2["passed"]), "enforce": True,
                     "detail": {"P1": p1["passed"], "P2": p2}}
            A, B = C.read_tables(C.DEFAULT_OUT)
            st = state()
            out, rows = score(raw, A, B, registry, cfg, gates,
                              drop_run3=bool((st.get("approvals") or {}).get("drop_run3")),
                              window=tuple(st.get("window") or WINDOW_DATES))
            write_outputs(out, rows, VERDICTS, UNIT_TABLE)
            dest = VERDICTS.parent
    except C.Refused as e:
        print(f"[v44] REFUSED: {e}", file=sys.stderr)
        return 3
    except Halt as e:
        print(f"[v44] HALT: {e}", file=sys.stderr)
        return 4
    print(f"wrote {dest}")
    for k, v in out["verdicts"].items():
        print(f"  {k}: {v.get('verdict')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
