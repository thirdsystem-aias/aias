#!/usr/bin/env python3
"""
score_v1_12.py -- AIAS(TM) v1.12 Coverage Paper A: scorer (pre-registration draft r1).

Transcribes PRE_REGISTRATION_v1_12.md section 2.3 (model coverage, raw Cov, pi_cov), 2.4 (beta, Cov*,
rating floors, the exact Rasch-type null of r1 and the equal-weight null of S3), 2.5 (rho_w,
permutation p, bootstrap, n floor), 3 (verdict and gate rules) and 4 (MC_Situation), and runs calibration
N1 (section 2.4). THE PRE-REGISTRATION PROSE IS AUTHORITATIVE; where it is silent the simplest faithful
option is taken and listed in SCORER_NOTES.

Added before the lock (2026-11-10, in a separate block that the core and N1 do not use): the coding step with
v0.42's coder (section 2.3; byte-identical copy code_t4_v0_42.py, git blob 2d36735d, checked at every load), the
comparators P_N3, C*_N3, pi_N3 and the fallback (2.6), parity gates P1-P3 (7.2), the other section 4 checks, the
drop rule (7.3), H1-H8 and the gate on the primary panel and repeated on C3 and A4 (3), the section 5 descriptives,
the section 7.4 sensitivities S1-S10, and the --code / --brandfree / --parity-p1 / --synthetic / --run modes.
Nothing here calls a model API; --run and the coding of the real record refuse before the lock.

SCORER_NOTES (choices where the pre-registration is silent)
 N1  Input unit: one answered CEP call = (substrate, model, CEP probe ID, run, set of registry brands named).
     A missing call is absent (it enters no denominator). One answer per (substrate, model, probe, run).
 N2  Null (r1): situation-blind Rasch-type model per panel model and category: logit P(y_b,s = 1) =
     theta_b + delta_j(s), no brand x CEP interaction. delta^(-b) = the joint maximum-likelihood fit (brand
     fixed effects and CEP effects on the binomial counts brand x CEP) on the OTHER registry brands of b's
     category in that model's answered CEP calls; brands named in none or all of the slots are left out;
     deterministic Newton steps with step halving, started from the fit on all informative brands; delta
     centred to sum to zero over the answered CEPs. A fit that does not converge within 100 steps, whose
     parameters pass |25|, or that has no informative brand: delta = 0 for that (b, m), counted. Given n,
     the named slots follow the conditional Bernoulli law P(Y) ~ prod_s exp(delta_j(s))^y_s; the exact null
     pmf of C is the x^n coefficient of prod_j [1 + z((1 + e^delta_j x)^s_j - 1)], normalised over z.
     No random draws: seed 112100 is no longer used by Cov*. S3 = equal weights (delta = 0).
 N3  c_max = min(n, number of CEPs with >= 1 answered run); c_min = the fewest CEPs that can hold n mentions,
     filling CEPs with the most answered runs first. r1: beta = (c - E) / (c_max - c_min) if c_max > c_min,
     else 0 (one linear normalisation: its null mean is 0 at every n).
 N4  Rating floor: n_b over the panel's models >= floor (14; 7 per half) and >= 2 panel models with n >= 1.
 N5  rho_w (r1): within-category average ranks centred on the category mean rank, r - (m_c + 1) / 2, then
     Pearson over all units pooled. S9 = the uncentred v0.37-v0.41 convention: _pearson, within_ranks and
     pooled_within_rho transcribed from osf/v41/scripts/score_v41.py (a unit test checks equality with that
     file). Categories with fewer than 5 units in the comparison are dropped before ranking. n floor:
     UNDETERMINED if pooled n < 30 or fewer than 3 categories retained.
 N6  Permutation: the within-category ranks of y are permuted within category (identical to re-ranking a
     within-category permutation of y); two-sided hit if |rho_perm| >= |rho_obs| - 1e-12, one-sided hit if
     rho_perm >= rho_obs - 1e-12; p = (1 + hits) / (draws + 1); seed = the hypothesis seed (112001-112008).
 N7  Bootstrap: units resampled with replacement within category (retained categories), ranks recomputed
     on each resample, percentile 95% interval; seed 112020, a fresh generator per test; non-finite
     resamples are dropped and counted.
 N8  H4: p is computed on r (rel = 2r / (1 + r) is monotone in r).
 N9  MC_Situation on the answered calls of the named panel (N3 for the gate). Per (model, run, category):
     J_between = mean Jaccard over pairs of different CEPs answered in that run; J_within = mean over that
     run's CEP answers of the Jaccard with the same CEP's other answered runs (same model). Pairs whose union
     is empty (neither answer names a registry brand) are skipped and counted. Pooled = mean over the
     (model, run, category) cells where both are defined. The C0 Jaccard is reported, not gated.
 N10 Gate: a two-model panel (drop rule, section 7.3) caps PASS at MARGINAL; inactive H5/H6 are ignored.
 N11 Calibration N1 (restated in r1): design and rule in calibrate_n1's docstring.
 N12 S8 mid-p variant: beta_mid = 2 [P0(C < c) + 0.5 P0(C = c)] - 1, P0 = the null distribution of C given n
     from the same Monte Carlo draws (weighted) or exact (equal weights: P(C = k) = [x^n y^k]
     prod_j (1 + y((1 + x)^s_j - 1)) / C(S, n)). Cov*_mid = 50 (1 + mean beta_mid), same floors.
 --- added before the lock (pipeline block; to be logged as clarifications at the lock) ---
 N13 Coder: a byte-identical copy of v0.42's code_t4_v0_42.py sits beside this file; its git blob (2d36735d) and
     SHA-256 (d0e4e685) are checked at every load and a mismatch refuses. AIAS_ROOT is set to this repository so
     the coder's certified substrate modules (identical blobs on branches v1.12 and v0.42) are read from here;
     its HOME shim may re-execute the entry script. The real record is coded only if the blob equals the coder
     at tag v0.42-prereg-r1 (section 2.3).
 N14 Coverage answers are coded through the coder's Phase B path, unchanged (code_calls, strip=True): certified
     mention detection on the answer text with URLs removed; the probe ID stands in for the frame; CEP and C0
     answers alike. Deduplication = the coder's rule (last answered attempt, else the last attempt).
 N15 P1 = the coder's own parity_p2 on the t3 omnibus answers (no API: the v0.23 judge is replayed from the locked
     outputs); the v1.12 criterion is zero mention mismatches with URL removal off (as v0.42 P2; URL-on changes
     listed). Recognition parity is reported but not required (v1.12 codes no recognition).
 N16 Analysis set: deduplicated calls of the design (4 models x 75 probes x runs 1-3, S0) that the coder coded as
     answered and whose served ID is the requested ID or a dated snapshot (acquire_v1_12.answered); an answered
     call without a served ID is excluded with the mismatches (MC_Served). Everything else is a missing cell.
 N17 MC_Complete per model: analysed calls / 225 (CEP and C0 calls); a model below 0.90 leaves every panel
     (section 7.3); Fable below -> C3 is primary; a primary panel of two models caps PASS at MARGINAL (N10).
     The Cov* floor "at least 2 of the 3 panel models" stays 2 on two-model panels and on A4.
 N18 Comparators (section 2.6, shared with v1.13): pi_hat = v0.42 brand-table column pi_N3_S0; C_P/3 = recognized /
     coded S0 Phase A rows of the N3 models (rows with no code, e.g. v0.23 without the judge, leave the
     denominator; none -> P not computed); C* from phi_N3_S0 when phi_partition_N3_S0 is "defined" (strictly), 100
     when "saturated", NOT RATED otherwise or with fewer than 6 N3 S0 Phase B mentions. Coded rows of calls that
     v0.42 excludes (outside its r2 design; served-ID mismatch, a missing served ID not excluded, as v0.42 N11) are
     dropped, so the comparators use v0.42's own analysis set.
 N19 Fallback (section 2.6): t4 counts as "scored" when v0.42's verdict file exists; "N3 fails v0.42's drop rule" =
     an N3 model listed with S0 in its models_excluded_condition. Then H1 uses the published AIAS 2.0 t3 P and H2
     its t3 C* where rated == 1, labelled cross-panel in the gate label; P2 is then not applicable.
 N20 P2: pi_hat and phi recomputed from v0.42's coded Phase B table (score_v0_42.pi_hat / phi_panel transcribed,
     score_v41.phi_m's reduced-panel branch transcribed; unit tests check both) must equal the brand table exactly.
     P3: every raw line's prompt equals the probe file's prompt and carries the probe file's SHA-256. A failed gate
     (or, in --run, a missing or failed P1 record) halts before any statistic.
 N21 MC_RegistryShare and MC_Defunct on the primary panel's analysed CEP answers. MC_Settings: every raw line of the
     design carries acquire_v1_12.SETTINGS. MC_Truncation: score_v0_42's finish-reason rule, per model.
 N22 MC_Defunct: flagged when the share of automotive CEP answers naming ANY cell D brand exceeds 5%; each brand's
     share is reported.
 N23 MC_Window: span from the first start to the last finish over every raw line of the design <= 72 h; every line
     inside acquire_v1_12.WINDOWS (which exclude 2026-11-17 to 11-22 12:00 UTC); no line overlapping [t4's first
     start, t4's last finish]; without a t4 raw file the overlap is not checked (reported None).
 N24 MC_Positive: raw Cov (k = 2) of the primary panel against pi_cov over all units (raw Cov has no floor).
 N25 H4 halves: Cov* on each half's 7 CEPs (its own leave-b-out delta fit on those CEPs), floor 7, primary panel.
     H7: P from aias_2_0_profiles.csv (wave t3). H8: Cov* on N3 and on C3 from the same tables; UNDETERMINED if
     Fable or Opus left the panel. The gate is repeated on C3 and A4 (all legs but H8, their own MC_Situation).
 N26 Sensitivity seeds: each re-uses its hypothesis seed (as v0.42 N4).
 N27 Sensitivities: rho_w and verdicts of the legs each touches; permutation p only where a verdict needs it (H4);
     no bootstrap. S1: raw Cov (k = 2) through H1-H3. S2: floors 6 and 28 on the full Cov* (H1-H3; the half floor
     stays 7). S3, S4, S8, S9, S10: H1-H4. S5: H1-H4 with each category left out, ranges of rho_w. S6: Cov* and
     pi_cov on the 12 CEPs left after dropping one W, floor 14, H1-H3. S7: H1 with pi_hat_N3 and with the N3 S0
     t4 mention total in place of P_N3 (not computed under the fallback).
 N28 Section 5 "non-registry brand mentions (count only)": NOT COMPUTED -- no detector for brands outside the
     registries is pre-registered.
 N29 S4: beta averaged over the panel models with n >= 1 and c_max > c_min; same rating rule; a rated unit with no
     such model is NOT RATED in S4.
 N30 H5/H6 are active only when their locked score is supplied (--h5-stage1 (N32-N34) / --h6, as recorded at the lock); an active
     leg without a score is UNDETERMINED with that reason.
 N31 Section 5 choices: missing cells = 45 per (category, model) minus analysed CEP and C0 answers; words per answer
     over analysed CEP and C0 answers (whitespace split); registry brands per CEP answer; per-W coverage = number
     of the W's two CEPs covered by >= 2 primary-panel models (the raw-Cov rule); "CEPs with no registry brand" =
     answered CEPs none of whose answered runs names one; run reliability per model on per-run shares of answered
     CEP answers naming the brand (centred rho_w, categories with >= 5 units); C0 agreement = mean Jaccard of
     each CEP answer with the same model-run's C0 answer; spend = usd_billed of every raw line.
 --- clarification of 2026-11-10 (before the lock; section 12 (f)) ---
 N32 H5's Ranking measure is v1.14's locked R* (modal position; tag v1.14-prereg-r1 -> 20fbc342), read from v1.14's
     Stage 1 output (osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json; --h5-stage1), never recomputed here.
     R*_S0 (v1.14's primary, pooled over N3 x 3 runs x 6 questions in S0) because H5 is defined on the t4 N3 S0 Phase B
     answers and Cov* is an S0 measure. Rated set = v1.14's (rated_S0; units of a substrate in v1.14's
     gate_excluded_substrates are NOT RATED). The file's SHA-256, its STAGE1_VERDICT and v1.14's H1/H2/H4_S1 and
     component verdicts are written to H5_ranking_source. A dry-run Stage 1 file is refused in --run.
 N33 v1.10's MNP is reported beside H5 as a non-gating comparability figure: computed from v1.14's hashed t4 rank table
     (rank_table_t4_v1_14.csv beside the Stage 1 file; SHA-256 must equal the Stage 1 record, else halt), lead-item
     rule, S0, floor 6 rankable mentions, rho_w(Cov*, MNP) centred, seed 112005, no bootstrap; its band reading is
     printed, never enters the gate.
 N34 Blindness guard: with H5 active (--run: tag v1.14-prereg-r1 exists; synthetic: a Stage 1 file is given) and no
     Stage 1 file, the run refuses before reading any record (exit 3); --h5-unavailable REASON instead scores with H5
     UNDETERMINED (N30), logged. v1.12 computes no rank statistic on a t4 answer.
 N35 (refinement R1, decision-rule change) H5 gates only when v1.14's Stage 1 interim verdict (STAGE1_VERDICT) is
     "SEPARABLE (Stage 2 pending)". With MARGINAL, FAIL or UNDETERMINED, or with Stage 1 halted (--h5-unavailable),
     H5 is computed where possible and reported (verdict, rho_w, h5_reported_not_gating in the gate record) but is left
     out of the gate on every panel; it never gates or downgrades. v1.14's final PASS/FAIL comes at its Stage 2 (t5).
 N36 (refinement R2, decision-rule change) H6 is active only with a locked Sentiment score on the t4 N3 answers from
     a pre-registration tagged before the v1.12 lock (--h6). v1.11's locked score is defined on the archived waves
     only, so it does not activate H6; the cross-panel fallback (--h6-cross-panel) is withdrawn and refused.

Modes:  --calibrate-n1   run N1 exactly as section 2.4 states; writes prereg/calibration_N1_v1_12.json
        --code           code data/v112_raw.jsonl (or --raw) with v0.42's coder -> data/coded (or --coded)
        --brandfree      MC_BrandFree on the 75 probes -> anchor/mc_brandfree_v1_12.json (or --out)
        --parity-p1      parity gate P1 -> anchor/parity_P1_v1_12.json (or --out)
        --synthetic DIR  score synthetic files (DIR/v112_raw.jsonl, DIR/coded, DIR/t4/...) -> DIR/_score
        --run            score the real record (refuses unless tag v1.12-prereg-r1 is on origin and P1-P3 pass)
"""
import argparse
import collections
import functools
import hashlib
import itertools
import json
import math
import platform
import sys
import time
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]                       # <repo>/osf/methodology/v1_12/scripts -> <repo>
N1_PATH = ROOT / "osf/methodology/v1_12/prereg/calibration_N1_v1_12.json"

PHASE_ID = "v1.12"
CATS = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
W_TYPES = ["why", "when", "where", "while", "with whom", "with what", "how feeling"]
RUNS = (1, 2, 3)
FLOOR_FULL, FLOOR_HALF, MIN_MODELS_NAMED = 14, 7, 2          # section 2.4; H4
FLOOR_SENS = (6, 28)                                          # S2
RASCH_MAX_ITER, RASCH_TOL, RASCH_BOUND = 100, 1e-9, 25.0       # SCORER_NOTES N2
SEED_N1, SEED_BOOT = 112200, 112020                           # section 2.5 (112100 no longer used, N2)
SEEDS = {"H1_Sep_Presence": 112001, "H2_Sep_Consistency": 112002, "H3_Sep_NamingRate": 112003,
         "H4_Reliability": 112004, "H5_Sep_Ranking": 112005, "H6_Sep_Sentiment": 112006,
         "H7_Sep_Presence_Legacy": 112007, "H8_Panel_Replication": 112008}
N_PERM, N_BOOT = 10_000, 10_000
SEP_CONF, SEP_FALS = 0.30, 0.50                               # section 3 bands
REL_CONF, REL_FALS, ALPHA = 0.50, 0.30, 0.05                  # H4
REP_CONF, REP_FALS = 0.70, 0.50                               # H8
N_FLOOR_UNITS, N_FLOOR_CATS, MIN_UNITS_PER_CAT = 30, 3, 5     # section 2.5
MCS_DIFF_MIN, MCS_JB_MAX = 0.10, 0.60                         # MC_Situation
N1_RULE_RHO, N1_RULE_DECILE = 0.05, 2.5                       # calibration N1 (r1)
TOL = 1e-12
NAN = float("nan")

FABLE, OPUS55, GPT6, GEM4 = "claude-fable-5-2", "claude-opus-5-5", "gpt-6-astra", "gemini-4-argon"
PANELS = {"N3": [FABLE, GPT6, GEM4], "C3": [OPUS55, GPT6, GEM4], "A4": [FABLE, OPUS55, GPT6, GEM4]}
PRIMARY_LEGS = ["H1_Sep_Presence", "H2_Sep_Consistency", "H3_Sep_NamingRate", "H4_Reliability"]
CONDITIONAL_LEGS = ["H5_Sep_Ranking", "H6_Sep_Sentiment"]
VERDICTS = {"CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED", "INACTIVE"}


def _finite(v):
    return v is not None and isinstance(v, (int, float, np.floating, np.integer)) and math.isfinite(float(v))


# =========================================================================== rho_w (v0.41 convention)
# _pearson, within_ranks, pooled_within_rho and _group_index: transcribed from osf/v41/scripts/score_v41.py.
def _pearson(a, b):
    a = np.asarray(a, float) - np.mean(a)
    b = np.asarray(b, float) - np.mean(b)
    d = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d > 0 else float("nan")


def within_ranks(values, groups):
    """Average ranks computed WITHIN each group (v0.37 convention)."""
    values = np.asarray(values, float)
    groups = np.asarray(groups)
    out = np.empty(len(values))
    for g in dict.fromkeys(groups):
        idx = np.where(groups == g)[0]
        out[idx] = stats.rankdata(values[idx])
    return out


def pooled_within_rho(x, y, groups):
    if len(x) < 3:
        return float("nan")
    return _pearson(within_ranks(x, groups), within_ranks(y, groups))


def _group_index(groups):
    groups = np.asarray(groups)
    return [np.where(groups == g)[0] for g in dict.fromkeys(groups)]


def centred_within_ranks(values, groups):
    """r1: within-category average ranks centred on the category mean rank, r - (m_c + 1) / 2."""
    groups = np.asarray(groups)
    r = within_ranks(values, groups)
    for g in dict.fromkeys(groups):
        idx = np.where(groups == g)[0]
        r[idx] -= (len(idx) + 1) / 2.0
    return r


def rho_w(x, y, groups, centred=True):
    """Section 2.5 rho_w: centred within-category ranks, Pearson pooled (r1 primary). centred=False: the
    uncentred v0.37-v0.41 convention (sensitivity S9; equals score_v41.pooled_within_rho)."""
    if not centred:
        return pooled_within_rho(x, y, groups)
    if len(x) < 3:
        return float("nan")
    return _pearson(centred_within_ranks(x, groups), centred_within_ranks(y, groups))


def paired(xd, yd, min_per_cat=MIN_UNITS_PER_CAT):
    """Units (substrate, brand) with both values finite; categories with fewer than `min_per_cat` such units
    are dropped (section 2.5). Returns keys, x, y, groups, info."""
    keys = sorted(k for k in xd if k in yd and _finite(xd[k]) and _finite(yd[k]))
    per = collections.Counter(k[0] for k in keys)
    keep = {c for c, n in per.items() if n >= min_per_cat}
    keys = [k for k in keys if k[0] in keep]
    x = np.array([float(xd[k]) for k in keys], float)
    y = np.array([float(yd[k]) for k in keys], float)
    g = np.array([k[0] for k in keys])
    info = {"n": len(keys), "n_categories": len(keep),
            "per_category": {c: per[c] for c in sorted(keep)},
            "dropped_categories": {c: n for c, n in sorted(per.items()) if c not in keep}}
    return keys, x, y, g, info


def below_n_floor(info):
    return info["n"] < N_FLOOR_UNITS or info["n_categories"] < N_FLOOR_CATS


def perm_p(x, y, g, obs, seed, sided, n_draws=N_PERM, centred=True):
    """Permutation p for rho_w: y permuted within category (section 2.5); see SCORER_NOTES N6."""
    if sided not in ("one", "two"):
        raise ValueError(sided)
    if not _finite(obs):
        return NAN
    rng = np.random.default_rng(seed)
    rk = centred_within_ranks if centred else within_ranks
    rx, ry = rk(x, g), rk(y, g)
    gidx = _group_index(g)
    idx = np.arange(len(y))
    hits = 0
    for _ in range(n_draws):
        for gi in gidx:
            idx[gi] = rng.permutation(gi)
        r = _pearson(rx, ry[idx])
        hits += bool(abs(r) >= abs(obs) - TOL) if sided == "two" else bool(r >= obs - TOL)
    return (1 + hits) / (n_draws + 1)


def bootstrap(g, seed, n_boot, fn):
    """Units resampled with replacement within category; fn(idx) -> {name: value}; percentile 95% per name."""
    rng = np.random.default_rng(seed)
    gidx = _group_index(g)
    store, dropped, names = collections.defaultdict(list), collections.Counter(), None
    for _ in range(n_boot):
        idx = np.concatenate([rng.choice(gi, size=len(gi), replace=True) for gi in gidx])
        res = fn(idx)
        names = names or list(res)
        for k, v in res.items():
            if _finite(v):
                store[k].append(v)
            else:
                dropped[k] += 1
    out = {}
    for k in names or []:
        ci = [float(q) for q in np.percentile(store[k], [2.5, 97.5])] if store[k] else None
        out[k] = {"ci95": ci, "n_draws": len(store[k]), "dropped_nonfinite": int(dropped[k])}
    return out


def rho_test(xd, yd, seed, sided, n_perm=N_PERM, n_boot=N_BOOT, transform=None, centred=True):
    """rho_w(x, y) with the n floor, permutation p (hypothesis seed) and bootstrap interval (seed 112020).
    transform: optional f(rho) reported with its own interval (H4: rel = 2r / (1 + r))."""
    keys, x, y, g, info = paired(xd, yd)
    out = dict(info, sided=sided, seed=seed, below_n_floor=below_n_floor(info))
    rho = rho_w(x, y, g, centred) if info["n"] >= 3 else NAN
    out["rho_w"] = rho
    out["centred"] = centred
    if transform is not None:
        out["transformed"] = transform(rho) if _finite(rho) else NAN
    if info["n"] < 3 or not _finite(rho):
        out["p_perm"] = NAN
        return out
    out["p_perm"] = perm_p(x, y, g, rho, seed, sided, n_perm, centred)
    out["n_perm"] = n_perm

    def fn(i):
        r = rho_w(x[i], y[i], g[i], centred)
        res = {"rho_w": r}
        if transform is not None:
            res["transformed"] = transform(r) if _finite(r) else NAN
        return res
    b = bootstrap(g, SEED_BOOT, n_boot, fn)
    out["ci95_rho_w"] = b["rho_w"]["ci95"]
    if transform is not None:
        out["ci95_transformed"] = b["transformed"]["ci95"]
    out["bootstrap"] = {k: {kk: vv for kk, vv in v.items() if kk != "ci95"} for k, v in b.items()}
    out["n_boot"] = n_boot
    return out


def spearman_brown_half(r):
    """rel = 2r / (1 + r) (H4)."""
    return 2 * r / (1 + r) if _finite(r) and r > -1 else NAN


# =========================================================================== verdicts (section 3)
def verdict_separability(t):
    """CONFIRMED iff |rho_w| <= 0.30; FALSIFIED iff |rho_w| >= 0.50; MARGINAL otherwise;
    UNDETERMINED below the n floor (or rho not finite)."""
    rho = t.get("rho_w", NAN)
    if t.get("below_n_floor", True) or not _finite(rho):
        return "UNDETERMINED"
    a = abs(rho)
    if a <= SEP_CONF:
        return "CONFIRMED"
    if a >= SEP_FALS:
        return "FALSIFIED"
    return "MARGINAL"


def verdict_reliability(t):
    """H4: rel = 2r / (1 + r). CONFIRMED iff rel >= 0.50 and one-sided p < 0.05; FALSIFIED iff rel < 0.30
    or p >= 0.05; MARGINAL otherwise; UNDETERMINED below the n floor."""
    r, p = t.get("rho_w", NAN), t.get("p_perm", NAN)
    if t.get("below_n_floor", True) or not _finite(r) or not _finite(p):
        return "UNDETERMINED"
    rel = spearman_brown_half(r)
    if not _finite(rel):
        return "UNDETERMINED"
    if rel >= REL_CONF and p < ALPHA:
        return "CONFIRMED"
    if rel < REL_FALS or p >= ALPHA:
        return "FALSIFIED"
    return "MARGINAL"


def verdict_replication(t):
    """H8: CONFIRMED iff rho >= 0.70 and one-sided p < 0.05; FALSIFIED iff rho < 0.50; MARGINAL otherwise."""
    rho, p = t.get("rho_w", NAN), t.get("p_perm", NAN)
    if t.get("below_n_floor", True) or not _finite(rho) or not _finite(p):
        return "UNDETERMINED"
    if rho >= REP_CONF and p < ALPHA:
        return "CONFIRMED"
    if rho < REP_FALS:
        return "FALSIFIED"
    return "MARGINAL"


def gate(mc_situation_pass, verdicts, active=None, h6_cross_panel=False, two_model=False):
    """Paper A verdict (section 3, GATE; section 7.3 two-model cap).
    verdicts: {tag: verdict} for H1-H8; active: {"H5_Sep_Ranking": bool, "H6_Sep_Sentiment": bool}."""
    active = active or {}
    for k, v in verdicts.items():
        if v not in VERDICTS:
            raise ValueError(f"{k}: unknown verdict {v!r}")
    legs = PRIMARY_LEGS + [h for h in CONDITIONAL_LEGS if active.get(h)]
    leg_v = {h: verdicts.get(h, "UNDETERMINED") for h in legs}
    for h in legs:
        if leg_v[h] == "INACTIVE":
            raise ValueError(f"{h} is declared active but its verdict is INACTIVE")
    notes = []
    if not mc_situation_pass:
        verdict = "INSTRUMENT FAIL"
        notes.append("MC_Situation failed: reported as a negative result; H1-H8 still computed for the record")
    elif any(v == "FALSIFIED" for v in leg_v.values()):
        verdict = "FAIL"
    elif any(v == "UNDETERMINED" for v in leg_v.values()):
        verdict = "UNDETERMINED"
    elif all(v == "CONFIRMED" for v in leg_v.values()):
        verdict = "PASS"
        if verdicts.get("H7_Sep_Presence_Legacy") == "FALSIFIED":
            verdict = "MARGINAL"
            notes.append("PASS downgraded to MARGINAL: H7_Sep_Presence_Legacy FALSIFIED")
    else:
        verdict = "MARGINAL"
    if two_model and verdict == "PASS":
        verdict = "MARGINAL"
        notes.append("two-model panel (section 7.3): gate at most MARGINAL")
    label = verdict
    if h6_cross_panel and leg_v.get("H6_Sep_Sentiment") == "CONFIRMED":
        label += " (H6 CONFIRMED cross-panel)"
    if verdict == "MARGINAL":
        notes.append("Paper B only on Pablo's recorded decision, the marginal leg as its first confirmatory test")
    return {"verdict": verdict, "label": label, "legs": leg_v,
            "inactive": [h for h in CONDITIONAL_LEGS if not active.get(h)], "notes": notes}


# =========================================================================== MC_Situation (section 4)
def jaccard(a, b):
    u = set(a) | set(b)
    if not u:
        return None
    return len(set(a) & set(b)) / len(u)


def mc_situation(cep_sets, control_sets, models):
    """cep_sets: {(substrate, model, cep_id, run): set of registry brands named} (answered CEP calls);
    control_sets: {(substrate, model, run): set} (answered C0 calls). SCORER_NOTES N9."""
    models = set(models)
    by_cell = collections.defaultdict(dict)            # (sub, model, run) -> {cep: set}
    by_cep = collections.defaultdict(dict)             # (sub, model, cep) -> {run: set}
    for (sub, m, cep, r), s in cep_sets.items():
        if m in models:
            by_cell[(sub, m, r)][cep] = s
            by_cep[(sub, m, cep)][r] = s
    cells, skipped_empty, c0_vals = [], 0, []
    for (sub, m, r) in sorted(by_cell):
        answers = by_cell[(sub, m, r)]
        ceps = sorted(answers)
        jb = []
        for a, b in itertools.combinations(ceps, 2):
            v = jaccard(answers[a], answers[b])
            if v is None:
                skipped_empty += 1
            else:
                jb.append(v)
        jw = []
        for cep in ceps:
            for r2, s2 in sorted(by_cep[(sub, m, cep)].items()):
                if r2 == r:
                    continue
                v = jaccard(answers[cep], s2)
                if v is None:
                    skipped_empty += 1
                else:
                    jw.append(v)
        c0 = control_sets.get((sub, m, r))
        c0j = []
        if c0 is not None:
            for cep in ceps:
                v = jaccard(answers[cep], c0)
                if v is not None:
                    c0j.append(v)
        c0_vals += c0j
        cells.append({"substrate": sub, "model": m, "run": r, "n_ceps": len(ceps),
                      "J_between": float(np.mean(jb)) if jb else None,
                      "J_within": float(np.mean(jw)) if jw else None,
                      "J_with_C0": float(np.mean(c0j)) if c0j else None})
    both = [c for c in cells if c["J_between"] is not None and c["J_within"] is not None]
    diff = float(np.mean([c["J_within"] - c["J_between"] for c in both])) if both else NAN
    jbm = float(np.mean([c["J_between"] for c in both])) if both else NAN
    passed = bool(_finite(diff) and _finite(jbm) and diff >= MCS_DIFF_MIN and jbm <= MCS_JB_MAX)
    return {"passed": passed, "pooled_mean_J_within_minus_J_between": diff, "pooled_mean_J_between": jbm,
            "pooled_mean_J_within": float(np.mean([c["J_within"] for c in both])) if both else NAN,
            "mean_J_with_C0": float(np.mean(c0_vals)) if c0_vals else NAN,
            "cells_used": len(both), "cells": cells, "pairs_skipped_empty_union": skipped_empty,
            "rule": f"pass iff pooled mean (J_within - J_between) >= {MCS_DIFF_MIN} and pooled mean J_between <= {MCS_JB_MAX}"}


# =========================================================================== Coverage core (sections 2.3-2.4)
def c_max_of(s_counts, n):
    """c_max = min(n, number of CEPs with >= 1 answered run) (normally min(14, n))."""
    return int(min(int(n), int(np.count_nonzero(np.asarray(s_counts)))))


def c_min_of(s_counts, n):
    """The fewest CEPs that can hold n mentions, filling CEPs with the most answered runs first."""
    if n <= 0:
        return 0
    cs = np.cumsum(np.sort(np.asarray(s_counts, int))[::-1])
    if n > cs[-1]:
        raise ValueError("n exceeds the answered slots")
    return int(np.searchsorted(cs, n, side="left") + 1)


def e_equal(s_counts, n):
    """S3 equal-weight null: E = sum_j [1 - C(S - s_j, n) / C(S, n)] (exact integers)."""
    s_counts = [int(s) for s in s_counts]
    S = sum(s_counts)
    if n <= 0:
        return 0.0
    tot = math.comb(S, n)
    return float(sum(1 - math.comb(S - s, n) / tot for s in s_counts if s > 0))


def beta_of(c, E, cmax, cmin):
    """r1: beta = (c - E) / (c_max - c_min) if c_max > c_min, else 0. One linear normalisation, so its null
    mean is (E0[c] - E) / (c_max - c_min) = 0 at every n."""
    if cmax <= cmin:
        return 0.0
    return float((c - E) / (cmax - cmin))


def null_pmf_equal(s_counts, n):
    """Exact equal-weight null distribution of C (CEPs touched) given n (SCORER_NOTES N12): {k: P(C = k)}."""
    return dict(_null_pmf_equal(tuple(int(s) for s in s_counts if s > 0), int(n)))


@functools.lru_cache(maxsize=None)
def _null_pmf_equal(s_counts, n):
    S = sum(s_counts)
    poly = [[1] + [0] * S]
    for s in s_counts:
        g = [0] + [math.comb(s, i) for i in range(1, s + 1)]          # (1 + x)^s - 1
        new = [[0] * (S + 1) for _ in range(len(poly) + 1)]
        for k, row in enumerate(poly):
            for i, a in enumerate(row):
                if a:
                    new[k][i] += a
                    for j, gc in enumerate(g):
                        if gc and i + j <= S:
                            new[k + 1][i + j] += a * gc
        poly = new
    tot = math.comb(S, n)
    return tuple((k, poly[k][n] / tot) for k in range(len(poly)) if poly[k][n])


def beta_mid(c, null_counts=None, null_pmf=None):
    """S8: beta_mid = 2 [P0(C < c) + 0.5 P0(C = c)] - 1 from Monte Carlo null counts or an exact pmf."""
    if null_pmf is not None:
        lt = sum(p for k, p in null_pmf.items() if k < c)
        eq = null_pmf.get(c, 0.0)
    else:
        counts = np.asarray(null_counts)
        lt, eq = float(np.mean(counts < c)), float(np.mean(counts == c))
    return float(2.0 * (lt + 0.5 * eq) - 1.0)


def fit_delta_rasch(K, s, theta0=None, delta0=None):
    """Joint ML fit of logit P = theta_b + delta_j on binomial counts K (brands x CEPs) out of s (answered slots per
    CEP; all > 0; every brand 0 < sum_j K < sum_j s). Newton steps with step halving; delta_0 = 0 during the fit.
    Returns (theta, delta, converged)."""
    K, s = np.asarray(K, float), np.asarray(s, float)
    B, J = K.shape
    theta = np.array(theta0, float) if theta0 is not None else _logit((K.sum(1) + 0.5) / (s.sum() + 1.0))
    delta = np.array(delta0, float) - float(delta0[0]) if delta0 is not None else np.zeros(J)
    if J == 1:
        return theta, delta, True

    def loglik(t, d):
        eta = t[:, None] + d[None, :]
        return float(np.sum(K * eta - s[None, :] * np.logaddexp(0.0, eta)))
    cur = loglik(theta, delta)
    for _ in range(RASCH_MAX_ITER):
        p = _expit(theta[:, None] + delta[None, :])
        r = K - s[None, :] * p
        w = s[None, :] * p * (1.0 - p)
        A = w.sum(1)
        if np.any(A <= 0):
            return theta, delta, False
        g_t, g_d, Bm = r.sum(1), r.sum(0)[1:], w[:, 1:]
        try:
            step_d = np.linalg.solve(np.diag(w.sum(0)[1:]) - Bm.T @ (Bm / A[:, None]), g_d - Bm.T @ (g_t / A))
        except np.linalg.LinAlgError:
            return theta, delta, False
        step_t = (g_t - Bm @ step_d) / A
        lam = 1.0
        while True:
            t_new, d_new = theta + lam * step_t, delta + lam * np.r_[0.0, step_d]
            new = loglik(t_new, d_new)
            if new >= cur - 1e-12 or lam < 1e-8:
                break
            lam /= 2.0
        theta, delta, cur = t_new, d_new, new
        if max(np.abs(theta).max(), np.abs(delta).max()) > RASCH_BOUND:
            return theta, delta, False
        if lam * max(np.abs(step_t).max(), np.abs(step_d).max()) < RASCH_TOL:
            return theta, delta, True
    return theta, delta, False


def rasch_deltas(slot_cep, Y, n_ceps):
    """Leave-b-out CEP effects delta^(-b) for every brand column of one model's answered CEP calls in one category
    (SCORER_NOTES N2). Returns (deltas (B, n_ceps), status per brand: ok / not_converged / no_informative_brands)."""
    slot_cep = np.asarray(slot_cep, int)
    Y = np.asarray(Y, float)
    B = Y.shape[1]
    s = np.bincount(slot_cep, minlength=n_ceps).astype(float) if len(slot_cep) else np.zeros(n_ceps)
    Kjb = np.zeros((n_ceps, B))
    np.add.at(Kjb, slot_cep, Y)
    K, S_tot = Kjb.T, s.sum()
    cols = np.where(s > 0)[0]
    tot = K.sum(1)
    info = (tot > 0) & (tot < S_tot)
    deltas = np.zeros((B, n_ceps))
    if len(cols) <= 1:
        return deltas, ["ok"] * B
    th_all, d_all, ok_all = (fit_delta_rasch(K[info][:, cols], s[cols]) if info.sum() else (None, None, False))
    status = []
    for b in range(B):
        keep = info.copy()
        keep[b] = False
        if not keep.any():
            status.append("no_informative_brands")
            continue
        th0 = th_all[keep[info]] if ok_all else None
        _th, d, ok = fit_delta_rasch(K[keep][:, cols], s[cols], th0, d_all if ok_all else None)
        if not ok:
            status.append("not_converged")
            continue
        deltas[b, cols] = d - d.mean()
        status.append("ok")
    return deltas, status


def null_pmf_rasch(s_counts, delta, n):
    """Exact null pmf of C (CEPs touched) given n when the named slots follow the conditional Bernoulli law with CEP
    weights exp(delta_j): x^n coefficient of prod_j [1 + z((1 + e^delta_j x)^s_j - 1)], normalised over z."""
    s_counts = np.asarray(s_counts, int)
    delta = np.asarray(delta, float)
    S, J = int(s_counts.sum()), len(s_counts)
    if not 0 <= n <= S:
        raise ValueError("n outside 0..answered slots")
    used = s_counts > 0
    a = float(delta[used].max()) if used.any() else 0.0           # rescaling x: cancels in the normalisation
    P = np.zeros((J + 1, S + 1))
    P[0, 0] = 1.0
    for sj, dj in zip(s_counts, delta):
        if sj == 0:
            continue
        t = [math.comb(int(sj), k) * math.exp(k * (dj - a)) for k in range(sj + 1)]
        new = P * t[0]
        for k in range(1, sj + 1):
            new[1:, k:] += P[:-1, :-k] * t[k]
        P = new
    coef = P[:, n]
    tot = coef.sum()
    return {int(c): float(v / tot) for c, v in enumerate(coef) if v > 0}


def beta_bm(slot_cep, Y, bi, n_ceps, delta=None):
    """beta (and S8 beta_mid) for brand column bi of one model's answered CEP calls in one category, against the exact
    conditional-Bernoulli null with CEP effects delta (r1 primary: delta^(-b); S3: delta None = 0).
    slot_cep: (S,) CEP index of each answered call; Y: (S, B) 0/1 registry-brand mentions."""
    slot_cep = np.asarray(slot_cep, int)
    Y = np.asarray(Y)
    S = len(slot_cep)
    s_counts = np.bincount(slot_cep, minlength=n_ceps) if S else np.zeros(n_ceps, int)
    y = Y[:, bi].astype(int) if S else np.zeros(0, int)
    n = int(y.sum())
    rec = {"slots": S, "n": n}
    if n == 0:
        rec.update(c=0, E=None, cmax=0, cmin=0, beta=None, beta_mid=None)
        return rec
    c = int(np.count_nonzero(np.bincount(slot_cep[y == 1], minlength=n_ceps)))
    cmax, cmin = c_max_of(s_counts, n), c_min_of(s_counts, n)
    pmf = null_pmf_rasch(s_counts, np.zeros(n_ceps) if delta is None else delta, n)
    E = float(sum(k * p for k, p in pmf.items()))
    rec.update(c=c, E=E, cmax=cmax, cmin=cmin, beta=beta_of(c, E, cmax, cmin), beta_mid=beta_mid(c, null_pmf=pmf))
    return rec


def index_answers(answers):
    """{(substrate, model, probe_id, run): frozenset(brands)}; one answer per key (SCORER_NOTES N1)."""
    out = {}
    for a in answers:
        k = (a["substrate"], a["model"], a["probe_id"], int(a["run"]))
        if k in out:
            raise ValueError(f"duplicate answer {k}: deduplicate calls before scoring")
        out[k] = frozenset(a["brands"])
    return out


def coverage_table(ans_index, brands_by_sub, ceps_by_sub, models, null="rasch"):
    """beta record per (substrate, brand, model) for every model in `models`. null="rasch": the primary null
    (leave-b-out delta, SCORER_NOTES N2); null="equal": S3 (delta = 0). ceps_by_sub: {substrate: [CEP probe
    IDs]} (14, or a half's 7). Deterministic: no random draws."""
    if null not in ("rasch", "equal"):
        raise ValueError(null)
    out = {}
    for sub in sorted(ceps_by_sub):
        ceps = list(ceps_by_sub[sub])
        cidx = {p: i for i, p in enumerate(ceps)}
        brands = sorted(brands_by_sub[sub])
        bidx = {b: i for i, b in enumerate(brands)}
        for m in sorted(models):
            keys = sorted(k for k in ans_index if k[0] == sub and k[1] == m and k[2] in cidx)
            slot_cep = np.array([cidx[k[2]] for k in keys], int)
            Y = np.zeros((len(keys), len(brands)), np.int8)
            for i, k in enumerate(keys):
                for b in ans_index[k]:
                    if b in bidx:
                        Y[i, bidx[b]] = 1
            if null == "rasch":
                deltas, status = rasch_deltas(slot_cep, Y, len(ceps))
            for b in brands:
                bi = bidx[b]
                rec = beta_bm(slot_cep, Y, bi, len(ceps), deltas[bi] if null == "rasch" else None)
                rec["delta_status"] = status[bi] if null == "rasch" else "equal"
                out[(sub, b, m)] = rec
    return out


def cov_star(tab, sub, b, panel, floor=FLOOR_FULL, min_models=MIN_MODELS_NAMED, key="beta"):
    """Cov*_b = 50 * (1 + mean beta over the panel's models with n >= 1); rated iff n_b >= floor and at least
    `min_models` panel models have n >= 1; otherwise NOT RATED (None). key="beta_mid": sensitivity S8."""
    recs = [tab.get((sub, b, m)) for m in panel]
    ns = [r["n"] if r else 0 for r in recs]
    n_b, named = int(sum(ns)), int(sum(1 for x in ns if x >= 1))
    rated = n_b >= floor and named >= min_models
    betas = [r[key] for r in recs if r and r["n"] >= 1]
    val = 50.0 * (1.0 + float(np.mean(betas))) if rated and betas else None
    return {"cov_star": val, "rated": bool(rated), "n_b": n_b, "models_naming": named,
            "mean_beta": float(np.mean(betas)) if betas else None}


def cov_star_map(tab, panel, floor=FLOOR_FULL, min_models=MIN_MODELS_NAMED, key="beta"):
    units = sorted({(s, b) for (s, b, _m) in tab})
    return {u: cov_star(tab, u[0], u[1], panel, floor, min_models, key)["cov_star"] for u in units}


def pi_cov(tab, sub, b, panel):
    """Share of the panel's answered CEP answers in b's category that name b (section 2.3)."""
    recs = [tab.get((sub, b, m)) for m in panel]
    n = sum(r["n"] for r in recs if r)
    S = sum(r["slots"] for r in recs if r)
    return n / S if S else NAN


def pi_cov_map(tab, panel):
    units = sorted({(s, b) for (s, b, _m) in tab})
    return {u: pi_cov(tab, u[0], u[1], panel) for u in units}


def model_covers(ans_index, sub, m, cep, b):
    """m covers (b, j): named in a majority of its answered runs of CEP j (2 of 3 when complete)."""
    ys = [int(b in ans_index[(sub, m, cep, r)]) for r in RUNS if (sub, m, cep, r) in ans_index]
    return bool(ys) and sum(ys) > len(ys) / 2


def raw_cov(ans_index, sub, b, panel, ceps, k=2):
    """Cov_b = share (0-100) of the category's CEPs in which at least k panel models cover b."""
    hits = sum(1 for j in ceps if sum(model_covers(ans_index, sub, m, j, b) for m in panel) >= k)
    return 100.0 * hits / len(ceps)


# =========================================================================== calibration N1 (section 2.4)
def _expit(x):
    return 1.0 / (1.0 + np.exp(-x))


def _logit(p):
    return np.log(p / (1.0 - p))


def exact_equal_weight_beta(n_ceps=14, runs=3):
    """Diagnostic: complete data (n_ceps x runs slots), equal weights. Exact distribution of c for every n
    (P(c = k) = C(J, k) [x^n]((1 + x)^runs - 1)^k / C(S, n)), E and the expectation of beta."""
    S = n_ceps * runs
    base = [0] + [math.comb(runs, i) for i in range(1, runs + 1)]      # (1 + x)^runs - 1
    polys = [[1]]
    for _k in range(1, n_ceps + 1):
        prev, new = polys[-1], [0] * (len(polys[-1]) + runs)
        for i, a in enumerate(prev):
            if a:
                for j, bc in enumerate(base):
                    if bc:
                        new[i + j] += a * bc
        polys.append(new)
    s_counts, rows = [runs] * n_ceps, []
    for n in range(1, S + 1):
        tot = math.comb(S, n)
        probs = {k: math.comb(n_ceps, k) * polys[k][n] / tot
                 for k in range(1, n_ceps + 1) if n < len(polys[k]) and polys[k][n]}
        E = sum(k * p for k, p in probs.items())
        cmax, cmin = c_max_of(s_counts, n), c_min_of(s_counts, n)
        eb = sum(p * beta_of(k, E, cmax, cmin) for k, p in probs.items())
        rows.append({"n": n, "E": round(E, 6), "E_closed_form": round(e_equal(s_counts, n), 6), "c_min": cmin,
                     "c_max": cmax, "E_beta_under_null": round(eb, 6), "sum_p": round(sum(probs.values()), 12)})
    return rows


def _bins_0p1(pis, vals):
    """Mean Cov* by naming-rate decile: 0.1-wide bins of pi_cov holding rated units (the r0 record's binning)."""
    out = collections.defaultdict(list)
    for p, v in zip(pis, vals):
        out[min(int(p * 10), 9)].append(v)
    return {f"{d / 10:.1f}-{(d + 1) / 10:.1f}": {"mean": float(np.mean(v)), "count": len(v)}
            for d, v in sorted(out.items())}


def _quantile_deciles(pis, vals):
    pis, vals = np.asarray(pis), np.asarray(vals)
    order = np.argsort(pis, kind="stable")
    return [{"pi_cov_range": [float(pis[c].min()), float(pis[c].max())], "mean": float(np.mean(vals[c])),
             "count": int(len(c))} for c in np.array_split(order, 10)]


def calibrate_n1(n_cats=1000, n_brands=24, n_models=3, n_ceps=14, n_runs=3, seed=SEED_N1,
                 rate_lo=0.02, rate_hi=0.98, cep_shift=1.0, n_ref_perm=20, log=None):
    """Calibration N1 (section 2.4; restated in r1). Synthetic design, unchanged from the r0 run:
      - each synthetic category has 24 brands with naming rates p_b ~ Uniform(0.02, 0.98), independent;
      - unequal list lengths across CEPs: CEP j carries a shift d_j ~ Uniform(-1, 1) on the logit scale, the same
        for every brand (no brand x situation association), model and run; brand b is named in an answer to CEP
        j with probability expit(logit(p_b) + d_j), independently across brands, models and runs;
      - 3 panel models, 14 CEPs x 3 runs, no missing cells;
      - Cov* as section 2.4 (r1: Rasch-type null, leave-b-out delta by deterministic ML and the exact conditional-
        Bernoulli pmf of C; floor 14 and >= 2 models naming) and pi_cov as section 2.3; one generator
        default_rng(112200), consumed per category in the order: rates, CEP shifts, the three models' answers (the r1
        null makes no random draws, so after the first category the synthetic realisation differs from the r0 run).
    Rule (r1): PASS iff |pooled centred rho_w(Cov*, pi_cov)| <= 0.05 over all rated units (categories with >= 5
    rated) AND every naming-rate decile (0.1-wide bin of pi_cov holding rated units) has mean Cov* within
    50 +/- 2.5. Reported beside it: the mean signed per-category rho, the per-category mean |rho| with its
    independence reference (Cov* permuted within category, 20 permutations, default_rng([112200, 1])), and,
    from the same data and draws, S8 (mid-p), S3 (equal weights, exact) and S9 (uncentred rho_w)."""
    log = log or (lambda *a: None)
    t0 = time.time()
    rng = np.random.default_rng(seed)
    ref_rng = np.random.default_rng([seed, 1])
    slot_cep = np.repeat(np.arange(n_ceps), n_runs)
    S = len(slot_cep)
    panel = list(range(n_models))
    variants = {"primary": ("rasch", "beta"), "S8_mid_p": ("rasch", "beta_mid"), "S3_equal_weights": ("eq", "beta")}
    fit_status, delta_err = collections.Counter(), []
    pool = {v: ([], [], []) for v in variants}
    rho_c, ref_abs, skipped = [], [], {"fewer_than_5_rated": 0, "rho_not_finite": 0}
    beta_by_n = collections.defaultdict(list)
    len_ratio, rated_total, units_total = [], 0, 0
    for k in range(n_cats):
        p = rng.uniform(rate_lo, rate_hi, n_brands)
        d = rng.uniform(-cep_shift, cep_shift, n_ceps)
        prob = _expit(_logit(p)[None, :] + d[:, None])
        Ys = [(rng.random((S, n_brands)) < prob[slot_cep]).astype(np.int8) for _ in panel]
        cep_len = np.mean([np.bincount(slot_cep, weights=Y.sum(axis=1), minlength=n_ceps) / n_runs for Y in Ys], axis=0)
        len_ratio.append(float(cep_len.max() / max(cep_len.min(), 1e-9)))
        tabs = {"rasch": {}, "eq": {}}
        fits = [rasch_deltas(slot_cep, Ys[m], n_ceps) for m in panel]
        for m in panel:
            fit_status.update(fits[m][1])
            for bi in range(n_brands):
                if fits[m][1][bi] == "ok":
                    delta_err.append(float(np.sqrt(np.mean((fits[m][0][bi] - (d - d.mean())) ** 2))))
        for bi in range(n_brands):
            for m in panel:
                tabs["rasch"][("N1", bi, m)] = beta_bm(slot_cep, Ys[m], bi, n_ceps, fits[m][0][bi])
                tabs["eq"][("N1", bi, m)] = beta_bm(slot_cep, Ys[m], bi, n_ceps, None)
        pi = np.array([pi_cov(tabs["rasch"], "N1", bi, panel) for bi in range(n_brands)])
        units_total += n_brands
        for v, (t, key) in variants.items():
            cov = np.array([np.nan if (c := cov_star(tabs[t], "N1", bi, panel, key=key)["cov_star"]) is None else c
                            for bi in range(n_brands)], float)
            rated = np.isfinite(cov)
            if v == "primary":
                rated_total += int(rated.sum())
                for bi in range(n_brands):
                    for m in panel:
                        rec = tabs["rasch"][("N1", bi, m)]
                        if rec["n"] >= 1:
                            beta_by_n[rec["n"]].append(rec["beta"])
            if rated.sum() < MIN_UNITS_PER_CAT:
                if v == "primary":
                    skipped["fewer_than_5_rated"] += 1
                continue
            x, y = cov[rated], pi[rated]
            pool[v][0].extend(x.tolist())
            pool[v][1].extend(y.tolist())
            pool[v][2].extend([k] * len(x))
            if v == "primary":
                r = rho_w(x, y, np.zeros(len(x), int))
                if not _finite(r):
                    skipped["rho_not_finite"] += 1
                else:
                    rho_c.append(r)
                    ref_abs.append(float(np.mean([abs(_pearson(stats.rankdata(ref_rng.permutation(x)),
                                                                stats.rankdata(y))) for _ in range(n_ref_perm)])))
        if (k + 1) % 100 == 0:
            xs, ys, gs = (np.array(a) for a in pool["primary"])
            log(f"N1: {k + 1}/{n_cats} categories, {time.time() - t0:.0f} s, running pooled centred rho_w = "
                f"{rho_w(xs, ys, gs):.4f}")
    res = {}
    for v in variants:
        xs, ys, gs = (np.array(a) for a in pool[v])
        bins = _bins_0p1(ys, xs)
        res[v] = {"pooled_centred_rho_w": float(rho_w(xs, ys, gs)),
                  "pooled_uncentred_rho_w_S9": float(rho_w(xs, ys, gs, centred=False)),
                  "n_units": int(len(xs)), "n_categories": int(len(set(gs.tolist()))),
                  "mean_cov_star": float(np.mean(xs)), "decile_means": bins,
                  "max_abs_decile_deviation_from_50": float(max(abs(b["mean"] - 50.0) for b in bins.values())),
                  "quantile_deciles": _quantile_deciles(ys, xs)}
    prim = res["primary"]
    ok_rho = abs(prim["pooled_centred_rho_w"]) <= N1_RULE_RHO
    ok_dec = prim["max_abs_decile_deviation_from_50"] <= N1_RULE_DECILE
    rho_c = np.array(rho_c)
    qs = [0, 2.5, 10, 25, 50, 75, 90, 97.5, 100]
    return {
        "statistic_r1": {
            "definition": "pooled centred rho_w(Cov*, pi_cov) over all rated synthetic units (categories with >= 5 "
                          "rated units), and the mean Cov* of every naming-rate decile (0.1-wide bin of pi_cov "
                          "holding rated units)",
            "pooled_centred_rho_w": prim["pooled_centred_rho_w"],
            "max_abs_decile_deviation_from_50": prim["max_abs_decile_deviation_from_50"],
            "rule": f"PASS iff |rho_w| <= {N1_RULE_RHO} and every decile mean Cov* within 50 +/- {N1_RULE_DECILE}",
            "rho_criterion_met": bool(ok_rho), "decile_criterion_met": bool(ok_dec),
            "result": "PASS" if ok_rho and ok_dec else "FAIL",
            "n_units": prim["n_units"], "n_categories": prim["n_categories"], "categories_skipped": skipped},
        "variants": res,
        "per_category_rho": {
            "mean_signed": float(rho_c.mean()), "sd": float(rho_c.std(ddof=1)),
            "se_of_mean": float(rho_c.std(ddof=1) / math.sqrt(len(rho_c))),
            "mean_abs": float(np.mean(np.abs(rho_c))),
            "mean_abs_under_independence_reference": float(np.mean(ref_abs)),
            "quantiles": {f"q{q}": float(np.percentile(rho_c, q)) for q in qs},
            "n_categories": int(len(rho_c))},
        "delta_fit": {"status_counts": dict(fit_status),
                      "failures_set_to_zero": int(sum(v for k, v in fit_status.items() if k != "ok")),
                      "rmse_delta_hat_vs_true_centred_shift": {"mean": float(np.mean(delta_err)),
                                                               "q90": float(np.percentile(delta_err, 90))}},
        "diagnostics": {
            "rated_units": rated_total, "units": units_total,
            "cep_mean_list_length_max_over_min": {"median": float(np.median(len_ratio)),
                                                  "q10": float(np.percentile(len_ratio, 10)),
                                                  "q90": float(np.percentile(len_ratio, 90))},
            "mean_beta_by_n": {str(n): {"mean": float(np.mean(v)), "count": len(v)}
                               for n, v in sorted(beta_by_n.items())},
            "exact_equal_weight_complete_data": exact_equal_weight_beta(n_ceps, n_runs)},
        "runtime_seconds": round(time.time() - t0, 1)}


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


R0_HISTORY = {
    "draft": "r0", "result": "FAIL",
    "beta": "(c - E) / (c_max - E) if c > E; (c - E) / (E - c_min) if c < E; 0 if c = E or c_max = c_min",
    "statistic": "mean over the 1,000 synthetic categories of |per-category rho_w(Cov*, pi_cov)|; rule <= 0.10",
    "mean_abs_rho_w": 0.5234236620662217, "pooled_rho_w_uncentred": 0.5282886254248434,
    "independence_reference_mean_abs_rho": 0.17572540107353307, "runtime_seconds": 109.8,
    "run_utc": "2026-11-10T12:32:53Z to 2026-11-10T12:34:43Z",
    "code_sha256": "4447d27d387179cec2619b903674034d95de68e943103d8eca708897db0be2fe",
    "record_sha256": "45ffe381a09e270542956dae8acaa62f16a93e063de4df20d9db18273b3e92cf",
    "why_restated": "r0's two-sided normalisation has a non-zero null mean; the per-category mean |rho| has a noise "
                    "floor of about 0.18 (0.1757 in that run)"}
R1_ATTEMPT_1_HISTORY = {
    "draft": "r1, first attempt (not sent)", "result": "FAIL",
    "beta": "(c - E) / (c_max - c_min); E from the length-weighted Monte Carlo null (w = 1 + L(-b), 2,000 draws, "
            "seed 112100)",
    "statistic": "pooled centred rho_w(Cov*, pi_cov) over all rated units; rule |rho_w| <= 0.05 and every decile "
                 "mean Cov* within 50 +/- 2.5",
    "pooled_centred_rho_w": 0.1732249193760613, "max_abs_decile_deviation_from_50": 2.2300664511714032,
    "mean_signed_per_category_rho": 0.17299646090928472, "runtime_seconds": 112.9,
    "run_utc": "2026-11-10T13:16:35Z to 2026-11-10T13:18:28Z",
    "code_sha256": "b3b6e5275022e9614f0f25ce4adf2afe2352432a13b96a4c08f982f7a4fa2606",
    "record_sha256": "4427f46d5c494826877884a5f42da44638b38f37295a9f1df1ce415b816c7305",
    "why_replaced": "the length weights (about 1.9-fold across CEPs) do not reproduce how a situation-blind brand "
                    "spreads (CEP odds exp(d_j), up to 7.4-fold): E too high, mean beta -0.03 to -0.05 at n = 5-25"}


def run_n1(out_path=N1_PATH, **kw):
    from datetime import datetime, timezone
    started = datetime.now(timezone.utc).isoformat()
    res = calibrate_n1(log=lambda s: print(s, flush=True), **kw)
    rec = {
        "phase": PHASE_ID, "check": "calibration N1 (PRE_REGISTRATION_v1_12.md section 2.4), as restated in draft r1",
        "rule_r1": "on the synthetic situation-blind design below, |pooled centred rho_w(Cov*, pi_cov)| <= 0.05 over all "
                   "rated synthetic units and every naming-rate decile's mean Cov* within 50 +/- 2.5; otherwise Cov* "
                   "is revised before the lock (logged)",
        "design": {"categories": kw.get("n_cats", 1000), "brands_per_category": kw.get("n_brands", 24),
                   "models": 3, "ceps": 14, "runs": 3, "naming_rates": "Uniform(0.02, 0.98) per brand",
                   "unequal_list_lengths": "CEP shift d_j ~ Uniform(-1, 1) on the logit scale, common to all "
                                           "brands, models and runs",
                   "seed": SEED_N1, "rating_floor": FLOOR_FULL, "min_models_naming": MIN_MODELS_NAMED,
                   "beta": "r1: (c - E) / (c_max - c_min) if c_max > c_min, else 0",
                   "null": "r1: Rasch-type (leave-b-out delta, deterministic ML; exact conditional-Bernoulli pmf)",
                   "details": "calibrate_n1 docstring in score_v1_12.py"},
        **res,
        "history": {"r0": R0_HISTORY, "r1_attempt_1": R1_ATTEMPT_1_HISTORY},
        "run_started_utc": started, "run_finished_utc": datetime.now(timezone.utc).isoformat(),
        "code": {"file": "osf/methodology/v1_12/scripts/score_v1_12.py", "sha256": sha256_file(__file__)},
        "environment": {"python": platform.python_version(), "numpy": np.__version__,
                        "scipy": __import__("scipy").__version__}}
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(json.dumps(rec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return rec



# =========================================================================== pipeline (added before the lock)
# Sections 2.3 (coding), 2.6 (comparators), 4 (checks), 5 (descriptives), 7.2 (parity gates), 7.3 (drop rule) and 7.4
# (sensitivities), and the --code / --brandfree / --parity-p1 / --synthetic / --run modes. Nothing in this block is
# used by the core above or by calibration N1. SCORER_NOTES N13-N33 list the choices made here.
import csv          # noqa: E402
import os           # noqa: E402
import re           # noqa: E402
import subprocess   # noqa: E402

DESIGN_DIR = ROOT / "osf/methodology/v1_12"
PROBES_PATH = DESIGN_DIR / "prereg/probes_v1_12.jsonl"
RAW_PATH = DESIGN_DIR / "data/v112_raw.jsonl"
CODED_DIR = DESIGN_DIR / "data/coded"
ANCHOR_DIR = DESIGN_DIR / "anchor"
P1_PATH = ANCHOR_DIR / "parity_P1_v1_12.json"
BRANDFREE_PATH = ANCHOR_DIR / "mc_brandfree_v1_12.json"
VERDICTS_PATH = DESIGN_DIR / "v112_verdicts.json"
UNIT_TABLE_PATH = DESIGN_DIR / "v112_unit_table.csv"
PROFILES_PATH = ROOT / "osf/aias_2_0/aias_2_0_profiles.csv"
T4_DEFAULTS = {"raw": ROOT / "osf/v42/data/t4_raw.jsonl", "coded": ROOT / "osf/v42/data/coded",
               "brand_table": ROOT / "osf/v42/v42_brand_table.csv", "verdicts": ROOT / "osf/v42/v42_verdicts.json"}
CODER_FILE = HERE / "code_t4_v0_42.py"                        # byte-identical copy of v0.42's coder (section 2.3)
CODER_BLOB = "2d36735d512cf9e13b74010ba5a7f655fc7de0bc"
CODER_SHA256 = "d0e4e685b5e3e1d983190726b5e88ef2b841b4589d5802ba67b86e31e4148220"
V042_TAG, V042_CODER_PATH = "v0.42-prereg-r1", "osf/v42/scripts/code_t4_v0_42.py"
PREREG_TAG = "v1.12-prereg-r1"
RAW_SUB = {"v0.19": "v19", "v0.20": "v20", "v0.21": "v21", "v0.22": "v22", "v0.23": "v23"}
MODELS4 = [FABLE, OPUS55, GPT6, GEM4]
T4_N3 = [FABLE, GPT6, GEM4]                                    # v0.42 r2 panel
CALLS_PER_MODEL, CALLS_TOTAL = 225, 900                        # section 6.2
COMPLETE_SHARE, DROP_SHARE = 0.98, 0.90                       # MC_Complete; drop rule (section 7.3)
TRUNC_FLAG, REGISTRY_SHARE_FLAG, DEFUNCT_MAX, POSITIVE_MIN, MAX_SPAN_HOURS = 0.05, 0.50, 0.05, 0.50, 72
DEFUNCT = ("Pontiac", "Oldsmobile", "Plymouth", "Mercury", "Saturn")   # v0.22 cell D (MC_Defunct)
DENON = ("v0.19", "Denon")                                    # S10 (section 8)
C_STAR_DIVISOR, C_STAR_MIN_MENTIONS, F_FRAMES = 9.0, 6, 6     # section 2.6
MENTION_FIELDS = ["call_id", "substrate", "probe_id", "model", "run", "brand", "mentioned"]
ALL_LEGS = PRIMARY_LEGS + CONDITIONAL_LEGS + ["H7_Sep_Presence_Legacy", "H8_Panel_Replication"]


class Refused(RuntimeError):
    pass


class Halt(RuntimeError):
    pass


class Cfg:
    def __init__(self, n_perm=N_PERM, n_boot=N_BOOT):
        self.n_perm, self.n_boot = n_perm, n_boot


def read_jsonl(path):
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return out


def read_csv_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _num(v):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


# --------------------------------------------------------------------------- the coder (section 2.3)
def git_blob_sha1(data):
    """git's object id of a file's bytes (what `git hash-object` prints)."""
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def verify_coder(path=None):
    path = CODER_FILE if path is None else path
    data = Path(path).read_bytes()
    blob, sha = git_blob_sha1(data), hashlib.sha256(data).hexdigest()
    return {"file": Path(path).name, "git_blob": blob, "sha256": sha, "pinned_git_blob": CODER_BLOB,
            "pinned_sha256": CODER_SHA256, "match": blob == CODER_BLOB and sha == CODER_SHA256}


def coder_blob_at_tag(tag=V042_TAG):
    """Section 2.3: the pinned blob re-checked against v0.42's tag (local git) before any v1.12 answer is coded."""
    try:
        r = subprocess.run(["git", "-C", str(ROOT), "rev-parse", f"{tag}:{V042_CODER_PATH}"], capture_output=True,
                           text=True, timeout=60)
        got = r.stdout.strip() if r.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        got = None
    return {"tag": tag, "blob_at_tag": got, "pinned": CODER_BLOB, "match": got == CODER_BLOB}


def load_coder():
    """Import the byte-identical copy of v0.42's coder. Its own bootstrap may re-execute this script under a HOME shim
    so that ~/aias resolves to ROOT (the certified substrate modules read ~/aias paths); SCORER_NOTES N13."""
    v = verify_coder()
    if not v["match"]:
        raise Refused(f"{CODER_FILE.name} is not v0.42's coder (blob {CODER_BLOB[:8]}, SHA-256 {CODER_SHA256[:8]}): {v}")
    os.environ["AIAS_ROOT"] = str(ROOT)
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    import code_t4_v0_42 as C   # noqa: E402
    return C


def to_t4_record(rec):
    """A v1.12 call record in the shape v0.42's coder reads: every Coverage answer goes through the coder's Phase B
    path (certified mention detection on the answer text, URLs removed); the probe stands in for the frame (N14)."""
    return {"call_id": rec["call_id"], "substrate": RAW_SUB[rec["substrate"]], "phase": "B",
            "probe_id": rec["probe_id"], "frame_id": rec["probe_id"], "model_requested": rec["model_requested"],
            "condition": rec.get("condition") or "S0", "run": rec["run"], "text": rec.get("text") or "",
            "status": rec.get("status"), "error": rec.get("error")}


def code_coverage(raw_records, C):
    """Deduplicate (coder rule) and code the Coverage answers. Returns (mention rows, deduplicated calls)."""
    calls = C.dedupe_calls([r for r in raw_records if r.get("substrate") in RAW_SUB])
    _a, B = C.code_calls([to_t4_record(r) for r in calls], probes={}, strip=True)
    rows = [{"call_id": r["call_id"], "substrate": r["substrate"], "probe_id": r["probe_id"], "model": r["model"],
             "run": int(r["run"]), "brand": r["brand"], "mentioned": int(r["mentioned"])} for r in B]
    return rows, calls


def registry_from_coder(C):
    """{substrate: {brand key: display name}}: the coder's registry keys (v0.23: ids, named from its REGISTRY)."""
    out = {}
    for sub in CATS:
        keys = C.brand_names_for(sub)
        names = {b["id"]: b["brand"] for b in C._modules()["S23"].REGISTRY} if sub == "v0.23" else {}
        out[sub] = {k: names.get(k, k) for k in keys}
    return out


def write_coded(rows, registry, record, out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "v112_mentions.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=MENTION_FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in MENTION_FIELDS})
    (out / "registry_v1_12.json").write_text(json.dumps(registry, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / "coding_record_v1_12.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return out


def read_coded(coded_dir):
    rows = read_csv_rows(Path(coded_dir) / "v112_mentions.csv")
    for r in rows:
        r["run"], r["mentioned"] = int(r["run"]), int(r["mentioned"])
    registry = json.loads((Path(coded_dir) / "registry_v1_12.json").read_text(encoding="utf-8"))
    return rows, registry


def run_code(raw_path=RAW_PATH, out_dir=CODED_DIR):
    """--code. The real record is coded only if the pinned blob equals the coder at tag v0.42-prereg-r1 (section 2.3);
    any difference is logged in anchor/DEVIATIONS.md before coding, so this refuses."""
    from datetime import datetime, timezone
    tag = coder_blob_at_tag()
    if Path(raw_path).resolve() == RAW_PATH.resolve() and not tag["match"]:
        raise Refused(f"coder blob at tag {V042_TAG} is {tag['blob_at_tag']}, pinned {CODER_BLOB}: log the difference in "
                      f"anchor/DEVIATIONS.md before coding (section 2.3)")
    C = load_coder()
    raw = read_jsonl(raw_path)
    rows, calls = code_coverage(raw, C)
    rec = {"phase": PHASE_ID, "step": "coding (section 2.3)", "coder": verify_coder(), "coder_at_v042_tag": tag,
           "raw": str(raw_path), "raw_sha256": sha256_file(raw_path), "raw_lines": len(raw),
           "calls_deduplicated": len(calls), "answered_calls_coded": len({r["call_id"] for r in rows}),
           "mention_rows": len(rows), "url_removal": True, "coded_utc": datetime.now(timezone.utc).isoformat()}
    write_coded(rows, registry_from_coder(C), rec, out_dir)
    return rec


def brandfree_check(probes, C):
    """MC_BrandFree: every substrate's certified detector (all registry aliases) on all 75 probe texts."""
    recs = [{"call_id": f"BF|{p['probe_id']}|{sub}", "substrate": raw, "phase": "B", "probe_id": p["probe_id"],
             "frame_id": p["probe_id"], "model_requested": "-", "condition": "S0", "run": 1, "text": p["prompt"],
             "status": "ok", "error": None} for p in probes for sub, raw in RAW_SUB.items()]
    _a, B = C.code_calls(recs, probes={}, strip=False)
    hits = [[r["probe_id"], r["substrate"], r["brand"]] for r in B if r["mentioned"]]
    reg = registry_from_coder(C)
    return {"check": "MC_BrandFree (section 4)", "rule": "0 alias matches in all 75 probes; a hit blocks the lock",
            "probes": len(probes), "probes_sha256": sha256_file(PROBES_PATH), "detector_runs": len(recs),
            "registry_sizes": {s: len(v) for s, v in reg.items()}, "hits": hits, "passed": not hits,
            "coder": verify_coder(), "registry": reg}


def run_parity_p1(out_path=P1_PATH):
    """P1 (section 7.2): the v1.12 coder on the t3 omnibus answers reproduces the locked t3 mention codes exactly, as
    v0.42's P2 (URL removal off; the URL-on changes listed). Runs the coder's own parity_p2 (no API call; the v0.23
    judge is replayed from the locked outputs) and adds the v1.12 criterion (N15)."""
    C = load_coder()
    tag = coder_blob_at_tag()
    r = C.parity_p2(out_path=out_path)
    off = r["url_removal_off"]
    r["v1_12"] = {"gate": "P1", "criterion": "url_removal_off total_mention_mismatches == 0 (mention codes; v1.12 codes "
                  "no recognition) and coder blob pinned", "mention_cells": off["total_mention_cells"],
                  "mention_mismatches": off["total_mention_mismatches"], "coder": verify_coder(),
                  "coder_at_v042_tag": tag,
                  "passed": bool(off["total_mention_mismatches"] == 0 and verify_coder()["match"])}
    Path(out_path).write_text(json.dumps(r, indent=2, ensure_ascii=False), encoding="utf-8")
    return r


# --------------------------------------------------------------------------- design and the analysis set
def load_probes(path=PROBES_PATH):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def probe_design(probes):
    """CEP IDs per substrate in file order (14), halves A/B (7 each), W of each CEP, the control probe C0."""
    d = {"ceps": collections.defaultdict(list), "half": {"A": collections.defaultdict(list),
                                                         "B": collections.defaultdict(list)},
         "w": {}, "control": {}, "role": {}, "sub": {}, "prompt": {}}
    for p in probes:
        pid, sub = p["probe_id"], p["substrate"]
        d["role"][pid], d["sub"][pid], d["prompt"][pid] = p["role"], sub, p["prompt"]
        if p["role"] == "CEP":
            d["ceps"][sub].append(pid)
            d["half"][p["half"]][sub].append(pid)
            d["w"][pid] = p["w"]
        else:
            d["control"][sub] = pid
    d["ceps"] = dict(d["ceps"])
    d["half"] = {h: dict(v) for h, v in d["half"].items()}
    return d


def is_answered(rec):
    """= code_t4_v0_42.is_answered (status ok, non-empty text, no error)."""
    return (rec.get("status") == "ok") and bool((rec.get("text") or "").strip()) and not rec.get("error")


def dedupe_calls(records):
    """= code_t4_v0_42.dedupe_calls: one record per call_id, the last answered attempt, else the last attempt."""
    best = {}
    for r in records:
        cid = r["call_id"]
        if cid not in best or is_answered(r) or not is_answered(best[cid]):
            best[cid] = r
    return list(best.values())


def served_ok(requested, served):
    """= acquire_v1_12.served_ok / score_v0_42.served_ok: the requested ID or a dated snapshot of it."""
    s = (served or "").strip().removeprefix("models/")
    return s == requested or re.fullmatch(re.escape(requested) + r"-(\d{4}-\d{2}-\d{2}|\d{8})", s) is not None


def in_design(rec, design):
    pid = rec.get("probe_id")
    return (rec.get("model_requested") in MODELS4 and pid in design["role"]
            and design["sub"][pid] == rec.get("substrate") and rec.get("run") in RUNS
            and (rec.get("condition") or "S0") == "S0")


def build_analysis(calls, mention_rows, design):
    """Analysis set (N16): deduplicated calls of the design, answered (coded by the coder), served ID accepted."""
    coded, named = set(), collections.defaultdict(set)
    for r in mention_rows:
        coded.add(r["call_id"])
        if r["mentioned"]:
            named[r["call_id"]].add(r["brand"])
    out = {"cep": {}, "ctl": {}, "calls": {}, "outside_design": [], "served_mismatch": [], "answered_not_coded": [],
           "ok_without_served_id": 0}
    for r in calls:
        cid = r["call_id"]
        if not in_design(r, design):
            out["outside_design"].append(cid)
            continue
        if not is_answered(r):
            continue
        if not served_ok(r["model_requested"], r.get("served_model")):
            out["served_mismatch"].append({"call_id": cid, "requested": r["model_requested"],
                                           "served": r.get("served_model")})
            out["ok_without_served_id"] += int(not r.get("served_model"))
            continue
        if cid not in coded:
            out["answered_not_coded"].append(cid)
            continue
        pid, m, run, sub = r["probe_id"], r["model_requested"], int(r["run"]), r["substrate"]
        out["calls"][cid] = r
        if design["role"][pid] == "CEP":
            out["cep"][(sub, m, pid, run)] = frozenset(named[cid])
        else:
            out["ctl"][(sub, m, run)] = frozenset(named[cid])
    return out


def answered_per_model(A):
    per = collections.Counter()
    for k in A["cep"]:
        per[k[1]] += 1
    for k in A["ctl"]:
        per[k[1]] += 1
    return {m: int(per.get(m, 0)) for m in MODELS4}


def select_panels(dropped):
    """Section 7.3: a model below 90% leaves the panel statistics; Claude Fable 5.2 dropped -> C3 replaces N3."""
    primary = "C3" if FABLE in dropped else "N3"
    panels = {name: [m for m in PANELS[name] if m not in dropped] for name in PANELS}
    return primary, panels


# --------------------------------------------------------------------------- section 4 checks
def _acquire():
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    import acquire_v1_12 as AQ   # noqa: E402  (constants only: SETTINGS, WINDOWS; nothing is sent)
    return AQ


def _truncated(rec):
    """= score_v0_42._truncated (N11 there)."""
    fr = str(rec.get("finish_reason") or "").lower()
    return "max_tokens" in fr or "max_output_tokens" in fr or fr == "length"


def _ts(s):
    from datetime import datetime
    return datetime.fromisoformat(s) if s else None


def mc_complete(A):
    per = answered_per_model(A)
    n = sum(per.values())
    per_model = {m: {"answered": per[m], "expected": CALLS_PER_MODEL, "share": per[m] / CALLS_PER_MODEL,
                     "below_90pct": per[m] / CALLS_PER_MODEL < DROP_SHARE} for m in MODELS4}
    return {"answered": n, "expected": CALLS_TOTAL, "share": n / CALLS_TOTAL, "pass": n / CALLS_TOTAL >= COMPLETE_SHARE,
            "per_model": per_model, "dropped_models": [m for m in MODELS4 if per_model[m]["below_90pct"]],
            "rule": "pass iff >= 98% of the 900 calls answered (non-empty text, accepted served ID); a model below 90% "
                    "leaves the panel statistics (section 7.3)"}


def mc_served(A):
    return {"n_mismatched": len(A["served_mismatch"]), "mismatched": A["served_mismatch"][:50],
            "of_which_without_served_id": A["ok_without_served_id"], "excluded": len(A["served_mismatch"]),
            "pass": not A["served_mismatch"]}


def mc_settings(raw_design, calls_design):
    AQ = _acquire()
    bad = [r["call_id"] for r in raw_design if r.get("settings") != AQ.SETTINGS]
    tok = {}
    for m in MODELS4:
        rs = [r for r in calls_design if r.get("model_requested") == m and is_answered(r)]
        th = [r.get("thinking_tokens") for r in rs if r.get("thinking_tokens") is not None]
        out = [r.get("output_tokens") for r in rs if r.get("output_tokens") is not None]
        tok[m] = {"answered_calls": len(rs), "reasoning_tokens_recorded": len(th),
                  "reasoning_tokens_total": int(sum(th)) if th else None,
                  "reasoning_tokens_mean": float(np.mean(th)) if th else None,
                  "output_tokens_mean": float(np.mean(out)) if out else None}
    return {"records": len(raw_design), "records_without_recorded_settings": len(bad), "examples": bad[:20],
            "share_with_settings": (1 - len(bad) / len(raw_design)) if raw_design else None,
            "pass": bool(raw_design) and not bad, "settings": AQ.SETTINGS, "reasoning_tokens_per_model": tok}


def mc_truncation(calls_design):
    out = {}
    for m in MODELS4:
        rs = [r for r in calls_design if r.get("model_requested") == m]
        k = sum(1 for r in rs if _truncated(r))
        out[m] = {"calls": len(rs), "at_cap": k, "share": k / len(rs) if rs else None,
                  "flag_above_5pct": bool(rs and k / len(rs) > TRUNC_FLAG)}
    return out


def mc_registry_share(A, panel):
    out = {}
    for sub in CATS:
        vals = [bool(s) for (s_, m, _p, _r), s in A["cep"].items() if s_ == sub and m in panel]
        per_m = {}
        for m in panel:
            v = [bool(s) for (s_, mm, _p, _r), s in A["cep"].items() if s_ == sub and mm == m]
            per_m[m] = float(np.mean(v)) if v else None
        share = float(np.mean(vals)) if vals else None
        out[sub] = {"cep_answers": len(vals), "share_naming_registry_brand": share, "per_model": per_m,
                    "flag_below_0_50": bool(share is not None and share < REGISTRY_SHARE_FLAG)}
    return out


def mc_defunct(A, panel, sub="v0.22"):
    ans = [s for (s_, m, _p, _r), s in A["cep"].items() if s_ == sub and m in panel]
    n = len(ans)
    per = {b: (sum(1 for s in ans if b in s) / n if n else None) for b in DEFUNCT}
    anyshare = sum(1 for s in ans if s & set(DEFUNCT)) / n if n else None
    return {"automotive_cep_answers": n, "share_naming_each": per, "share_naming_any": anyshare,
            "flagged": bool(anyshare is not None and anyshare > DEFUNCT_MAX),
            "rule": "flagged if the share of automotive CEP answers naming any cell D brand exceeds 5% (N22)"}


def mc_positive(raw_cov_map, pi_map):
    keys, x, y, g, info = paired(raw_cov_map, pi_map)
    rho = rho_w(x, y, g) if info["n"] >= 3 else NAN
    return {"rho_w_raw_cov_pi_cov": rho, "n": info["n"], "n_categories": info["n_categories"],
            "flagged": not (_finite(rho) and abs(rho) >= POSITIVE_MIN),
            "rule": "raw Cov (k = 2) must give |rho_w(Cov, pi_cov)| >= 0.50; otherwise the gate's sensitivity is flagged"}


def mc_window(raw_design, t4_window):
    AQ = _acquire()
    iv = [(r["call_id"], _ts(r.get("started_utc")), _ts(r.get("finished_utc"))) for r in raw_design]
    iv = [(c, a, b or a) for c, a, b in iv if a is not None]
    if not iv:
        return {"pass": False, "reason": "no timestamps"}
    first, last = min(a for _c, a, _b in iv), max(b for _c, _a, b in iv)
    span = (last - first).total_seconds() / 3600
    outside = [c for c, a, b in iv if not (AQ.in_window(a) and AQ.in_window(b))]
    res = {"first_call_utc": first.isoformat(), "last_call_utc": last.isoformat(), "span_hours": span,
           "within_72h": span <= MAX_SPAN_HOURS, "calls_outside_section_6_7_windows": len(outside),
           "examples_outside": outside[:20]}
    if t4_window:
        t0, t1 = _ts(t4_window[0]), _ts(t4_window[1])
        ov = [c for c, a, b in iv if a <= t1 and b >= t0]
        res.update(t4_first_call_utc=t4_window[0], t4_last_call_utc=t4_window[1], calls_overlapping_t4=len(ov),
                   no_t4_overlap=not ov)
    else:
        res.update(calls_overlapping_t4=None, no_t4_overlap=None)
    res["pass"] = bool(res["within_72h"] and not outside and res["no_t4_overlap"] is not False)
    res["rule"] = ("all calls within 72 hours; every call inside the section 6.7 windows (so none during 2026-11-17 "
                   "to 2026-11-21); none overlapping t4 (N23)")
    return res


# --------------------------------------------------------------------------- comparators (section 2.6) and P2
def t4_in_design(rec):
    """= score_v0_42.in_design (r2, its N15)."""
    if rec.get("model_requested") not in T4_N3 or rec.get("condition") not in ("S0", "S1"):
        return False
    if rec.get("phase") == "B":
        return rec.get("run") in RUNS
    if rec.get("phase") == "A":
        return (rec.get("condition"), rec.get("run")) == ("S0", 1)
    return False


def t4_excluded(t4_raw):
    """v0.42's analysis exclusions: calls outside its design and answered calls with another served ID (a missing
    served ID is listed there, not excluded). Returns (excluded call_ids, (first start, last finish) of t4)."""
    calls = dedupe_calls(t4_raw)
    excl = set()
    for r in calls:
        if not t4_in_design(r):
            excl.add(r["call_id"])
        elif is_answered(r) and r.get("served_model") and not served_ok(r["model_requested"], r["served_model"]):
            excl.add(r["call_id"])
    st = sorted(r["started_utc"] for r in t4_raw if r.get("started_utc"))
    en = sorted(r["finished_utc"] for r in t4_raw if r.get("finished_utc"))
    return excl, ((st[0], en[-1]) if st and en else None)


def read_t4_coded(coded_dir):
    A, B = [], []
    for raw in RAW_SUB.values():
        for ph, acc in (("a", A), ("b", B)):
            p = Path(coded_dir) / f"{raw}_phase_{ph}.csv"
            if not p.exists():
                continue
            for r in read_csv_rows(p):
                r["run"] = int(r["run"])
                if ph == "a":
                    r["recognized"] = None if r["recognized"] in ("", None) else int(r["recognized"])
                else:
                    r["mentioned"] = int(r["mentioned"])
                acc.append(r)
    return A, B


def t4_counts(coded_b, excluded, cond="S0"):
    """k per (model, run, substrate, brand) and answered Phase B call_ids per (model, run, substrate)."""
    k, ans = collections.defaultdict(int), collections.defaultdict(set)
    for r in coded_b:
        if r["call_id"] in excluded or r["condition"] != cond:
            continue
        ans[(r["model"], r["run"], r["substrate"])].add(r["call_id"])
        k[(r["model"], r["run"], r["substrate"], r["brand"])] += int(r["mentioned"])
    return k, ans


def pi_hat_t4(k, ans, units, models=T4_N3):
    """= score_v0_42.pi_hat: sum_m sum_r k / answered Phase B calls."""
    out = {}
    for (s, b) in units:
        num = sum(k.get((m, r, s, b), 0) for m in models for r in RUNS)
        den = sum(len(ans.get((m, r, s), ())) for m in models for r in RUNS)
        out[(s, b)] = num / den if den else NAN
    return out


def phi_m_reduced(counts_vec):
    """= score_v41.phi_m for a panel of M' != 6 models (the reduced-panel branch)."""
    k = np.asarray(counts_vec, float)
    m = len(k)
    if m == 6:
        raise ValueError("six-model panels use score_v41.phi_of")
    pi = float(k.sum() / (m * F_FRAMES))
    if pi <= 0.0:
        return None, pi, "zero"
    if pi >= 1.0:
        return None, pi, "saturated"
    phi = float(((k - F_FRAMES * pi) ** 2).sum() / (F_FRAMES * pi * (1.0 - pi)) / (m - 1))
    return phi, pi, "defined"


def phi_panel_t4(k, ans, units, models=T4_N3):
    """= score_v0_42.phi_runs / phi_panel: {(sub, brand): (phi or None, partition, per-run partitions)}."""
    out = {}
    for (s, b) in units:
        runs = []
        for r in RUNS:
            if any(len(ans.get((m, r, s), ())) != F_FRAMES for m in models):
                runs.append((None, "missing"))
                continue
            phi, _pi, part = phi_m_reduced([k.get((m, r, s, b), 0) for m in models])
            runs.append((phi, part))
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


def parity_p2(brand_table, coded_b, excluded):
    """P2 (section 7.2): pi_hat_{N3,S0} and phi_{N3,S0} recomputed from v0.42's coded Phase B table equal the
    brand table's pi_N3_S0, phi_N3_S0 and phi_partition_N3_S0 exactly."""
    units = [(r["substrate"], r["brand"]) for r in brand_table]
    k, ans = t4_counts(coded_b, excluded)
    pi, ph = pi_hat_t4(k, ans, units), phi_panel_t4(k, ans, units)
    bad = []
    for r in brand_table:
        u = (r["substrate"], r["brand"])
        tp, tphi, tpart = _num(r.get("pi_N3_S0")), _num(r.get("phi_N3_S0")), (r.get("phi_partition_N3_S0") or "")
        mp = pi[u] if _finite(pi[u]) else None
        if tp != mp or tphi != ph[u][0] or tpart != ph[u][1]:
            bad.append({"unit": list(u), "table": [tp, tphi, tpart], "recomputed": [mp, ph[u][0], ph[u][1]]})
    return {"gate": "P2", "units": len(units), "mismatches": len(bad), "examples": bad[:10],
            "passed": bool(units) and not bad}


def comparators_t4(brand_table, coded_a, coded_b, excluded, models=T4_N3):
    """Section 2.6: P_N3 = 100 (C_P/3 + 2 pi_hat) / 3 and C*_N3 = 100 (1 - phi / 9) (100 if saturated; NOT RATED if
    zero or undefined; rated only with >= 6 N3 S0 recall mentions); pi_hat_N3 and the t4 mention total (S7)."""
    pi, phi = {}, {}
    for r in brand_table:
        u = (r["substrate"], r["brand"])
        pi[u] = _num(r.get("pi_N3_S0"))
        part = (r.get("phi_partition_N3_S0") or "").strip()
        v = _num(r.get("phi_N3_S0"))
        phi[u] = v if (part == "defined" and v is not None) else (0.0 if part == "saturated" else None)
    rec = collections.defaultdict(lambda: [0, 0])
    for r in coded_a:
        if r["condition"] != "S0" or r["model"] not in models or r["call_id"] in excluded or r["recognized"] is None:
            continue
        t = rec[(r["substrate"], r["brand"])]
        t[0] += int(r["recognized"])
        t[1] += 1
    ment = collections.Counter()
    for r in coded_b:
        if r["condition"] == "S0" and r["model"] in models and r["call_id"] not in excluded and r["run"] in RUNS:
            ment[(r["substrate"], r["brand"])] += int(r["mentioned"])
    P, C = {}, {}
    for u in pi:
        n_rec = rec[u][1] if u in rec else 0
        P[u] = 100.0 * (rec[u][0] / n_rec + 2.0 * pi[u]) / 3.0 if (pi[u] is not None and n_rec) else None
        C[u] = 100.0 * (1.0 - phi[u] / C_STAR_DIVISOR) if (phi[u] is not None and ment[u] >= C_STAR_MIN_MENTIONS) \
            else None
    return {"P": P, "C": C, "pi_hat": dict(pi), "t4_mentions": {u: int(ment[u]) for u in pi},
            "recognition": {u: list(v) for u, v in rec.items()}}


def legacy_t3(profiles_rows):
    """Published AIAS 2.0 t3 values (legacy panel): P, and C* where rated."""
    P, C = {}, {}
    for r in profiles_rows:
        if r.get("wave") != "t3":
            continue
        u = (r["substrate"], r["brand"])
        P[u] = _num(r.get("P"))
        C[u] = _num(r.get("C_star")) if str(r.get("rated")).strip() == "1" else None
    return P, C


def choose_comparators(t4, profiles_rows):
    """Section 2.6 fallback: t4 not scored (no v0.42 verdicts file) or an N3 model excluded by v0.42's drop rule in S0
    -> H1 and H2 use the published AIAS 2.0 t3 values, labelled cross-panel."""
    lp, lc = legacy_t3(profiles_rows or [])
    reason = None
    if t4 is None:
        reason = "t4 (v0.42) outputs not available at analysis"
    else:
        gone = [x for x in t4["verdicts"].get("models_excluded_condition", [])
                if x.split("|")[0] in T4_N3 and x.split("|")[-1] == "S0"]
        if gone:
            reason = f"N3 failed v0.42's drop rule in S0: {gone}"
    if reason:
        return {"source": "AIAS 2.0 t3 (legacy panel)", "cross_panel": True, "reason": reason, "P": lp, "C": lc,
                "pi_hat": {}, "t4_mentions": {}, "legacy_P": lp}
    c = comparators_t4(t4["brand_table"], t4["coded_a"], t4["coded_b"], t4["excluded"])
    return dict(c, source="t4 (v0.42, N3, S0)", cross_panel=False, reason=None, legacy_P=lp)


def parity_p3(raw_all, design, probes_path=PROBES_PATH):
    """P3: the probes sent equal probes_v1_12.jsonl byte for byte (every raw line's prompt and the file's SHA-256)."""
    sha = sha256_file(probes_path)
    unknown = [r.get("call_id") for r in raw_all if r.get("probe_id") not in design["prompt"]]
    bad_prompt = [r.get("call_id") for r in raw_all if r.get("probe_id") in design["prompt"]
                  and r.get("prompt") != design["prompt"][r["probe_id"]]]
    bad_sha = [r.get("call_id") for r in raw_all if r.get("probes_sha256") != sha]
    return {"gate": "P3", "records": len(raw_all), "probes_sha256": sha, "unknown_probe": unknown[:20],
            "prompt_mismatch": bad_prompt[:20], "probes_sha256_mismatch": bad_sha[:20],
            "passed": bool(raw_all) and not (unknown or bad_prompt or bad_sha)}


# --------------------------------------------------------------------------- hypothesis legs (section 3)
VERDICT_FN = {"sep": verdict_separability, "rel": verdict_reliability, "rep": verdict_replication}
H13 = ["H1_Sep_Presence", "H2_Sep_Consistency", "H3_Sep_NamingRate"]
H14 = H13 + ["H4_Reliability"]


def _rho_only(xd, yd, seed, sided, n_perm, transform=None, centred=True):
    """rho_w with the n floor and (n_perm > 0) the permutation p; no bootstrap (sensitivities, N27)."""
    keys, x, y, g, info = paired(xd, yd)
    out = dict(info, sided=sided, seed=seed, below_n_floor=below_n_floor(info), centred=centred)
    rho = rho_w(x, y, g, centred) if info["n"] >= 3 else NAN
    out["rho_w"] = rho
    if transform is not None:
        out["transformed"] = transform(rho) if _finite(rho) else NAN
    ok = bool(n_perm) and info["n"] >= 3 and _finite(rho)
    out["p_perm"] = perm_p(x, y, g, rho, seed, sided, n_perm, centred) if ok else NAN
    out["n_perm"] = n_perm if ok else 0
    return out


def run_leg(kind, xd, yd, seed, n_perm=N_PERM, n_boot=N_BOOT, centred=True, exclude=()):
    """One leg: kind "sep" (two-sided, separability bands), "rel" (H4: one-sided, rel = 2r / (1 + r)) or "rep" (H8)."""
    xd = {k: v for k, v in xd.items() if k not in exclude}
    sided = "two" if kind == "sep" else "one"
    tf = spearman_brown_half if kind == "rel" else None
    t = rho_test(xd, yd, seed, sided, n_perm, n_boot, tf, centred) if n_boot > 0 else \
        _rho_only(xd, yd, seed, sided, n_perm, tf, centred)
    t["verdict"] = VERDICT_FN[kind](t)
    return t


def cov_star_room(tab, sub, b, panel, floor=FLOOR_FULL, min_models=MIN_MODELS_NAMED):
    """S4: Cov* with beta averaged only over the models with room to vary (n >= 1 and c_max > c_min); same rating
    rule; a rated unit with no such model is NOT RATED in S4 (N29)."""
    base = cov_star(tab, sub, b, panel, floor, min_models)
    betas = [r["beta"] for r in (tab.get((sub, b, m)) for m in panel) if r and r["n"] >= 1 and r["cmax"] > r["cmin"]]
    return 50.0 * (1.0 + float(np.mean(betas))) if base["rated"] and betas else None


def cov_map(tab, panel, floor=FLOOR_FULL, key="beta", room_only=False):
    if not room_only:
        return cov_star_map(tab, panel, floor, MIN_MODELS_NAMED, key)
    units = sorted({(s, b) for (s, b, _m) in tab})
    return {u: cov_star_room(tab, u[0], u[1], panel, floor) for u in units}


def coverage_maps(tabs, panel, floor=FLOOR_FULL, key="beta", room_only=False):
    """Cov* (14 CEPs), Cov*_A and Cov*_B (7 CEPs each, floor 7; H4) and pi_cov for one panel."""
    return {"cov": cov_map(tabs["full"], panel, floor, key, room_only),
            "covA": cov_map(tabs["A"], panel, FLOOR_HALF, key, room_only),
            "covB": cov_map(tabs["B"], panel, FLOOR_HALF, key, room_only),
            "pi": pi_cov_map(tabs["full"], panel)}


def legs_for(maps, comp, cfg, active=None, extra=None, which=None, n_boot=None, centred=True, exclude=()):
    """H1-H4, H5/H6 (active only) and H7 on one panel's maps. comp: {"P", "C", "legacy_P"}; extra: {H5/H6: map}."""
    active, extra = active or {}, extra or {}
    which = which or (PRIMARY_LEGS + CONDITIONAL_LEGS + ["H7_Sep_Presence_Legacy"])
    n_boot = cfg.n_boot if n_boot is None else n_boot
    spec = {"H1_Sep_Presence": ("sep", "cov", comp["P"]), "H2_Sep_Consistency": ("sep", "cov", comp["C"]),
            "H3_Sep_NamingRate": ("sep", "cov", maps["pi"]), "H4_Reliability": ("rel", "covA", maps.get("covB")),
            "H7_Sep_Presence_Legacy": ("sep", "cov", comp["legacy_P"])}
    out = {}
    for h in which:
        if h in CONDITIONAL_LEGS:
            if not active.get(h):
                out[h] = {"verdict": "INACTIVE", "reason": "activation rule (section 3): tag not pushed before the lock"}
                continue
            if extra.get(h) is None:
                out[h] = {"verdict": "UNDETERMINED", "reason": "leg active but no locked score was supplied (N30)"}
                continue
            kind, x, y = "sep", maps["cov"], extra[h]
        else:
            kind, xk, y = spec[h]
            x = maps[xk]
        out[h] = run_leg(kind, x, y, SEEDS[h], cfg.n_perm, n_boot, centred, exclude)
    return out


def h8_leg(tabs, panels, dropped, cfg):
    """H8: rho_w(Cov*_N3, Cov*_C3) on the units rated on both; one-sided; seed 112008."""
    gone = [m for m in (FABLE, OPUS55) if m in dropped]
    if gone:
        return {"verdict": "UNDETERMINED", "reason": f"{gone} left the panel statistics (section 7.3)"}
    return run_leg("rep", cov_star_map(tabs["full"], panels["N3"]), cov_star_map(tabs["full"], panels["C3"]),
                   SEEDS["H8_Panel_Replication"], cfg.n_perm, cfg.n_boot)


def evaluate_panel(name, panel, tabs, comp, A, cfg, active, extra, h6_cross_panel=False, h8=None, h5_gates=True):
    maps = coverage_maps(tabs, panel)
    legs = legs_for(maps, comp, cfg, active, extra)
    if h8 is not None:
        legs["H8_Panel_Replication"] = h8
    msit = mc_situation(A["cep"], A["ctl"], panel)
    verdicts = {h: legs[h]["verdict"] for h in legs}
    gate_active = dict(active, H5_Sep_Ranking=bool(active.get("H5_Sep_Ranking")) and h5_gates)   # N35
    g = gate(msit["passed"], verdicts, gate_active, h6_cross_panel, two_model=len(panel) == 2)
    if active.get("H5_Sep_Ranking") and not h5_gates:
        g["notes"].append(f"H5_Sep_Ranking ({verdicts.get('H5_Sep_Ranking')}) reported, not gating: v1.14's Stage 1 "
                          f"verdict is not SEPARABLE (N35)")
        g["h5_reported_not_gating"] = verdicts.get("H5_Sep_Ranking")
    if comp.get("cross_panel"):
        g["notes"].append("H1 and H2 computed cross-panel against the published AIAS 2.0 t3 values (section 2.6 fallback: "
                          f"{comp.get('reason')})")
        g["label"] += " (H1, H2 cross-panel)"
    if len(panel) == 2:
        g["label"] += " (two-model)"
    return {"panel": name, "models": panel, "two_model": len(panel) == 2, "MC_Situation": msit, "legs": legs,
            "verdicts": verdicts, "gate": g, "maps": maps}


# --------------------------------------------------------------------------- sensitivities (section 7.4)
def sensitivities(tabs, panel, comp, A, design, cfg, base, active=None, extra=None):
    """S1-S10 on the primary panel: rho_w and verdicts of the legs each one touches; p only where a verdict needs it
    (H4); no bootstrap (N27). Verdict changes against the primary verdicts are listed."""
    out = {}
    units = sorted({(s, b) for (s, b, _m) in tabs["rasch"]["full"]})

    def legs(maps, which, **kw):
        return legs_for(maps, comp, cfg, active, extra, which=which, n_boot=0, **kw)

    def summary(ls):
        return {"rho_w": {h: l.get("rho_w") for h, l in ls.items()}, "n": {h: l.get("n") for h, l in ls.items()},
                "verdicts": {h: l["verdict"] for h, l in ls.items()},
                "verdict_changes": {h: [base[h], l["verdict"]] for h, l in ls.items() if l["verdict"] != base.get(h)}}

    prim = coverage_maps(tabs["rasch"], panel)
    raw2 = {u: raw_cov(A["cep"], u[0], u[1], panel, design["ceps"][u[0]], 2) for u in units}
    out["S1_raw_Cov_k2"] = summary(legs(dict(prim, cov=raw2), H13))
    for fl in FLOOR_SENS:
        out[f"S2_floor_{fl}"] = summary(legs(dict(prim, cov=cov_star_map(tabs["rasch"]["full"], panel, fl)), H13))
    out["S3_equal_weight_null"] = summary(legs(coverage_maps(tabs["equal"], panel), H14))
    out["S4_room_to_vary"] = summary(legs(coverage_maps(tabs["rasch"], panel, room_only=True), H14))
    s5 = {}
    for c in CATS:
        ex = tuple(u for u in units if u[0] == c)
        s5[c] = summary(legs(prim, H14, exclude=ex))
    rng = {}
    for h in H14:
        v = [s5[c]["rho_w"][h] for c in CATS if _finite(s5[c]["rho_w"][h])]
        rng[h] = [min(v), max(v)] if v else None
    out["S5_leave_one_category_out"] = {"per_category_left_out": s5, "rho_w_range": rng,
                                        "verdict_changes": {c: s5[c]["verdict_changes"] for c in CATS
                                                            if s5[c]["verdict_changes"]}}
    s6 = {}
    for w in W_TYPES:
        t = tabs["wout"][w]
        s6[w] = summary(legs({"cov": cov_star_map(t, panel), "pi": pi_cov_map(t, panel)}, H13))
    out["S6_leave_one_W_out"] = {"per_W_left_out": s6,
                                 "verdict_changes": {w: s6[w]["verdict_changes"] for w in W_TYPES if s6[w]["verdict_changes"]}}
    s7 = {}
    for name, alt in (("pi_hat_N3", comp.get("pi_hat")), ("t4_mentions_N3_S0", comp.get("t4_mentions"))):
        if not alt:
            s7[name] = {"status": "NOT_COMPUTED", "reason": "t4 comparators not used (section 2.6 fallback)"}
            continue
        s7[name] = summary({"H1_Sep_Presence": run_leg("sep", prim["cov"], alt, SEEDS["H1_Sep_Presence"], 0, 0)})
    out["S7_presence_alternatives"] = s7
    out["S8_mid_p"] = summary(legs(coverage_maps(tabs["rasch"], panel, key="beta_mid"), H14))
    out["S9_uncentred_rho_w"] = summary(legs(prim, H14, centred=False))
    out["S10_without_Denon"] = summary(legs(prim, H14, exclude=(DENON,)))
    return out


# --------------------------------------------------------------------------- descriptives (section 5)
def distribution(vals):
    v = [float(x) for x in vals if _finite(x)]
    if not v:
        return {"n": 0}
    q1, med, q3 = (float(x) for x in np.percentile(v, [25, 50, 75]))
    return {"n": len(v), "median": med, "q1": q1, "q3": q3, "min": min(v), "max": max(v)}


def run_reliability(A, units, design, model):
    """rel1 = mean rho_w over the three run pairs of each brand's per-run covered-CEP share (share of the model's
    answered CEP answers in that run naming the brand); rel3 = 3 rel1 / (1 + 2 rel1)."""
    share = {}
    for r in RUNS:
        sh = {}
        for (s, b) in units:
            ans = [st for (s_, m, _p, rr), st in A["cep"].items() if s_ == s and m == model and rr == r]
            sh[(s, b)] = (sum(1 for st in ans if b in st) / len(ans)) if ans else NAN
        share[r] = sh
    pairs = {}
    for r1, r2 in itertools.combinations(RUNS, 2):
        keys, x, y, g, info = paired(share[r1], share[r2])
        pairs[f"{r1}-{r2}"] = rho_w(x, y, g) if info["n"] >= 3 else NAN
    vals = [v for v in pairs.values() if _finite(v)]
    rel1 = float(np.mean(vals)) if vals else NAN
    rel3 = 3 * rel1 / (1 + 2 * rel1) if _finite(rel1) and 1 + 2 * rel1 > 0 else NAN
    return {"rel1": rel1, "rel3": rel3, "run_pairs": pairs}


def descriptives(A, design, tabs, units, panels, primary, raw_design):
    d = {"note": "descriptive only; no verdicts (section 5)",
         "non_registry_brand_mentions": "NOT COMPUTED: the pre-registration asks for a count but names no detector for "
                                        "brands outside the registries (N28; clarification to settle at the lock)"}
    per = {}
    for sub in CATS:
        for m in MODELS4:
            cep = {k: s for k, s in A["cep"].items() if k[0] == sub and k[1] == m}
            ctl = {k: s for k, s in A["ctl"].items() if k[0] == sub and k[1] == m}
            texts = [r["text"] for r in A["calls"].values() if r["substrate"] == sub and r["model_requested"] == m]
            ceps = sorted({k[2] for k in cep})
            empty = [j for j in ceps if not any(s for k, s in cep.items() if k[2] == j)]
            c0j = [v for k, s in cep.items() if (sub, m, k[3]) in A["ctl"]
                   for v in [jaccard(s, A["ctl"][(sub, m, k[3])])] if v is not None]
            betas = [tabs["full"][(sub, b, m)]["beta"] for (s, b) in units if s == sub
                     and (sub, b, m) in tabs["full"] and tabs["full"][(sub, b, m)]["n"] >= 1]
            per[f"{sub}|{m}"] = {
                "cep_answers": len(cep), "control_answers": len(ctl),
                "missing_cells": len(design["ceps"].get(sub, [])) * len(RUNS) + len(RUNS) - len(cep) - len(ctl),
                "words_per_answer_mean": float(np.mean([len(t.split()) for t in texts])) if texts else None,
                "registry_brands_named_per_cep_answer_mean": float(np.mean([len(s) for s in cep.values()])) if cep else None,
                "share_of_ceps_with_no_registry_brand": len(empty) / len(ceps) if ceps else None,
                "mean_jaccard_cep_answer_vs_C0": float(np.mean(c0j)) if c0j else None,
                "beta_distribution": distribution(betas)}
    d["per_category_model"] = per
    pan = {}
    for name, models in panels.items():
        for sub in CATS:
            us = [u for u in units if u[0] == sub]
            cs = {u: cov_star(tabs["full"], sub, u[1], models) for u in us}
            cep = {k: s for k, s in A["cep"].items() if k[0] == sub and k[1] in models}
            ceps = sorted({k[2] for k in cep})
            empty = [j for j in ceps if not any(s for k, s in cep.items() if k[2] == j)]
            pan[f"{sub}|{name}"] = {
                "models": models, "units": len(us), "rated": sum(1 for v in cs.values() if v["rated"]),
                "cov_star": distribution([v["cov_star"] for v in cs.values()]),
                **{f"raw_cov_k{k}": distribution([raw_cov(A["cep"], sub, u[1], models, design["ceps"][sub], k)
                                                  for u in us]) for k in (1, 2, 3)},
                "share_of_ceps_no_registry_brand_in_any_panel_answer": len(empty) / len(ceps) if ceps else None}
    d["per_category_panel"] = pan
    pm = panels[primary]
    d["per_W_coverage_primary_panel"] = {
        f"{u[0]}|{u[1]}": {w: sum(1 for j in design["ceps"][u[0]] if design["w"][j] == w
                                  and sum(model_covers(A["cep"], u[0], m, j, u[1]) for m in pm) >= 2) for w in W_TYPES}
        for u in units}
    d["run_to_run_reliability"] = {m: run_reliability(A, units, design, m) for m in MODELS4}
    spend = {}
    for m in MODELS4:
        rs = [r for r in raw_design if r.get("model_requested") == m]
        spend[m] = {"records": len(rs), "input_tokens": int(sum(r.get("input_tokens") or 0 for r in rs)),
                    "output_tokens": int(sum(r.get("output_tokens") or 0 for r in rs)),
                    "thinking_tokens": int(sum(r.get("thinking_tokens") or 0 for r in rs)),
                    "usd_billed": float(sum(r.get("usd_billed") or 0.0 for r in rs))}
    d["tokens_and_spend"] = {"per_model": spend, "total_usd": float(sum(v["usd_billed"] for v in spend.values())),
                             "basis": "usd_billed of every raw line (every attempt), list prices (section 6.6)"}
    return d


# --------------------------------------------------------------------------- orchestration
def build_tables(A, design, brands_by_sub, models=MODELS4):
    """beta tables: Rasch-type null (primary) and equal weights (S3), on the 14 CEPs and on each half (H4), and the
    leave-one-W-out tables (S6)."""
    full, halves = design["ceps"], design["half"]
    tabs = {}
    for null in ("rasch", "equal"):
        tabs[null] = {"full": coverage_table(A["cep"], brands_by_sub, full, models, null),
                      "A": coverage_table(A["cep"], brands_by_sub, halves["A"], models, null),
                      "B": coverage_table(A["cep"], brands_by_sub, halves["B"], models, null)}
    tabs["wout"] = {w: coverage_table(A["cep"], brands_by_sub,
                                      {s: [p for p in full[s] if design["w"][p] != w] for s in full}, models)
                    for w in W_TYPES}
    return tabs


def unit_rows(units, tabs, prim, comp, panels, primary, A, design):
    pm = panels[primary]
    cs_by = {name: cov_star_map(tabs["rasch"]["full"], ms) for name, ms in panels.items()}
    mid = cov_star_map(tabs["rasch"]["full"], pm, key="beta_mid")
    eq = cov_star_map(tabs["equal"]["full"], pm)
    rows = []
    for u in units:
        c = cov_star(tabs["rasch"]["full"], u[0], u[1], pm)
        r = {"substrate": u[0], "brand": u[1], "primary_panel": primary, "cov_star": c["cov_star"], "rated": int(c["rated"]),
             "n_b": c["n_b"], "models_naming": c["models_naming"], "mean_beta": c["mean_beta"],
             "pi_cov": prim["maps"]["pi"].get(u)}
        for k in (1, 2, 3):
            r[f"raw_cov_k{k}"] = raw_cov(A["cep"], u[0], u[1], pm, design["ceps"][u[0]], k)
        r.update(cov_star_A=prim["maps"]["covA"].get(u), cov_star_B=prim["maps"]["covB"].get(u), cov_star_mid_S8=mid.get(u),
                 cov_star_equal_S3=eq.get(u))
        for name in panels:
            r[f"cov_star_{name}"] = cs_by[name].get(u)
        r.update(comparator_source=comp["source"], P_comparator=comp["P"].get(u), C_star_comparator=comp["C"].get(u),
                 pi_hat_N3_S0=comp["pi_hat"].get(u), t4_mentions_N3_S0=comp["t4_mentions"].get(u),
                 P_t3_legacy=comp["legacy_P"].get(u))
        rows.append(r)
    return rows


def score_coverage(inp, cfg=None, gates=None, with_sensitivities=True):
    """inp: raw (every v112_raw line), mentions (coded rows), registry ({sub: {key: name}}), probes, t4 (load_t4 dict or
    None), t4_window, profiles (AIAS 2.0 profile rows), active / extra (H5, H6), h6_cross_panel, brandfree (record).
    gates: {"P1": record, "require_p1": bool, "enforce": bool}. Returns (verdict document, unit rows)."""
    cfg, gates = cfg or Cfg(), gates or {}
    design = probe_design(inp["probes"])
    raw_all = inp["raw"]
    raw_design = [r for r in raw_all if in_design(r, design)]
    calls = dedupe_calls(raw_all)
    calls_design = [r for r in calls if in_design(r, design)]
    A = build_analysis(calls, inp["mentions"], design)
    brands = {s: list(inp["registry"][s]) for s in CATS if s in inp["registry"]}
    units = sorted((s, b) for s in brands for b in brands[s])
    t4 = inp.get("t4")
    comp = choose_comparators(t4, inp.get("profiles"))
    p1 = gates.get("P1") or {"gate": "P1", "status": "SKIPPED (not supplied)", "passed": None}
    gate_rec = {"P1": p1, "P2": parity_p2(t4["brand_table"], t4["coded_b"], t4["excluded"]) if not comp["cross_panel"]
                else {"gate": "P2", "status": "NOT_APPLICABLE: section 2.6 fallback comparators", "passed": None},
                "P3": parity_p3(raw_all, design, inp.get("probes_path", PROBES_PATH))}
    failed = [k for k, v in gate_rec.items() if v.get("passed") is False]
    if gates.get("require_p1") and p1.get("passed") is not True:
        failed.append("P1")
    if gates.get("enforce", True) and failed:
        raise Halt(f"parity gate(s) {sorted(set(failed))} failed: no v1.12 statistic is computed (section 7.2); log the "
                   f"fix in anchor/DEVIATIONS.md first. {json.dumps(_clean({k: gate_rec[k] for k in set(failed)}))[:1500]}")
    mcc = mc_complete(A)
    dropped = mcc["dropped_models"]
    primary, panels = select_panels(dropped)
    tabs = build_tables(A, design, brands)
    active, extra = inp.get("active") or {}, inp.get("extra") or {}
    h6x = bool(inp.get("h6_cross_panel"))
    h5g = h5_gates(inp.get("h5_source"))
    prim = evaluate_panel(primary, panels[primary], tabs["rasch"], comp, A, cfg, active, extra, h6x,
                          h8_leg(tabs["rasch"], panels, dropped, cfg), h5_gates=h5g)
    repeats = {name: evaluate_panel(name, panels[name], tabs["rasch"], comp, A, cfg, active, extra, h6x, h5_gates=h5g)
               for name in ("C3", "A4") if name != primary}
    pm = panels[primary]
    raw2 = {u: raw_cov(A["cep"], u[0], u[1], pm, design["ceps"][u[0]], 2) for u in units}
    status = collections.Counter(v["delta_status"] for v in tabs["rasch"]["full"].values())
    mcs = {"MC_BrandFree": inp.get("brandfree") or {"status": "run at the lock: --brandfree (anchor/mc_brandfree_v1_12.json)"},
           "MC_Complete": mcc, "MC_Served": mc_served(A), "MC_Settings": mc_settings(raw_design, calls_design),
           "MC_Truncation": mc_truncation(calls_design), "MC_RegistryShare": mc_registry_share(A, pm),
           "MC_Situation": prim["MC_Situation"], "MC_Defunct": mc_defunct(A, pm),
           "MC_Positive": mc_positive(raw2, prim["maps"]["pi"]),
           "MC_Window": mc_window(raw_design, inp.get("t4_window") or (t4 or {}).get("window"))}
    base = {h: prim["verdicts"][h] for h in H14}
    doc = {"phase": PHASE_ID, "prereg": "osf/methodology/v1_12/prereg/PRE_REGISTRATION_v1_12.md", "prereg_tag": PREREG_TAG,
           "seeds": dict(SEEDS, bootstrap=SEED_BOOT), "draws": {"permutation": cfg.n_perm, "bootstrap": cfg.n_boot},
           "panels": panels, "primary_panel": primary, "models_dropped_section_7_3": dropped,
           "parity_gates": gate_rec, "comparators": {"source": comp["source"], "cross_panel": comp["cross_panel"],
                                                     "reason": comp["reason"]},
           "paper_A_verdict": prim["gate"], "verdicts": prim["verdicts"],
           "legs": prim["legs"], "MC": mcs,
           "delta_fits": {"status_counts": dict(status),
                          "set_to_zero": int(sum(v for k, v in status.items() if k != "ok"))},
           "gate_repeated_on": {n: {"models": r["models"], "gate": r["gate"], "verdicts": r["verdicts"],
                                    "MC_Situation_passed": r["MC_Situation"]["passed"],
                                    "rho_w": {h: l.get("rho_w") for h, l in r["legs"].items()}}
                                for n, r in repeats.items()},
           "analysis_set": {"answered_calls_analysed": len(A["calls"]), "outside_design": len(A["outside_design"]),
                            "served_mismatch_excluded": len(A["served_mismatch"]),
                            "answered_not_coded": A["answered_not_coded"][:20], "raw_lines": len(raw_all)}}
    if with_sensitivities:
        sens = sensitivities(tabs, pm, comp, A, design, cfg, base, active, extra)
        doc["sensitivities"] = sens
        doc["verdict_changes_under_sensitivities"] = {
            k: v["verdict_changes"] for k, v in sens.items() if isinstance(v, dict) and v.get("verdict_changes")}
    doc["descriptives"] = descriptives(A, design, tabs["rasch"], units, panels, primary, raw_design)
    src = inp.get("h5_source")
    if src is not None or active.get("H5_Sep_Ranking"):
        doc["H5_ranking_source"] = h5_source_record(src, prim["maps"]["cov"], cfg, inp.get("h5_unavailable"))
    return doc, unit_rows(units, tabs, prim, comp, panels, primary, A, design)


def h5_gates(src):
    """N35: H5 gates only when v1.14's Stage 1 interim verdict is SEPARABLE ("SEPARABLE (Stage 2 pending)")."""
    return bool(src) and str(src.get("stage1_verdict") or "").startswith("SEPARABLE")


def h5_source_record(src, cov, cfg, unavailable=None):
    """N32-N34: where H5's R* came from, v1.14's own verdicts printed next to H5, and v1.10's MNP against Cov* as a
    non-gating comparability figure (centred rho_w, same seed; its band reading never enters the gate)."""
    if src is None:
        return {"measure": f"R*_{H5_CONDITION} of {V114_PREREG_TAG} (modal position)", "status": "NOT_AVAILABLE",
                "reason": unavailable or "v1.14 Stage 1 output not supplied", "h5_gates": False}
    rec = {k: v for k, v in src.items() if k not in ("values", "MNP")}
    rec["measure"] = f"R*_{src['condition']} of {V114_PREREG_TAG} (modal position, lead-item rule, floor 6)"
    rec["h5_gates"] = h5_gates(src)
    rec["reading"] = ("H5 gates only when v1.14's Stage 1 interim verdict is SEPARABLE; otherwise (MARGINAL, FAIL, "
                      "UNDETERMINED, or Stage 1 halted) H5 is computed where possible and reported, and neither gates "
                      "nor downgrades (N35). v1.14's final PASS/FAIL comes at its Stage 2 (t5)")
    m = src.get("MNP") or {}
    if m.get("status") == "COMPUTED":
        t = run_leg("sep", cov, m["values"], SEEDS["H5_Sep_Ranking"], cfg.n_perm, 0)
        rec["MNP_comparability_non_gating"] = {"rho_w": t.get("rho_w"), "n": t.get("n"), "p_perm": t.get("p_perm"),
                                               "band_reading": t["verdict"], "rank_table_sha256": m["sha256"],
                                               "rated_units": m["rated_units"], "gating": False}
    else:
        rec["MNP_comparability_non_gating"] = {"status": m.get("status", "NOT_COMPUTED"), "reason": m.get("reason"),
                                               "gating": False}
    return rec


def _clean(o):
    if isinstance(o, (float, np.floating)):
        return float(o) if math.isfinite(float(o)) else None
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, dict):
        return {("|".join(map(str, k)) if isinstance(k, tuple) else str(k)): _clean(v) for k, v in o.items()}
    if isinstance(o, (set, frozenset)):
        return [_clean(v) for v in sorted(o)]
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    return o


def write_outputs(doc, rows, verdicts_path, table_path):
    Path(verdicts_path).parent.mkdir(parents=True, exist_ok=True)
    Path(verdicts_path).write_text(json.dumps(_clean(doc), indent=2, ensure_ascii=False, allow_nan=False) + "\n",
                                   encoding="utf-8")
    fields = list(rows[0]) if rows else []
    with open(table_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if v is None or (isinstance(v, float) and not math.isfinite(v)) else v) for k, v in r.items()})


def load_t4(raw, coded, brand_table, verdicts):
    """v0.42's locked outputs. Returns (dict or None, window of t4 or None, missing paths)."""
    window = t4_excluded(read_jsonl(raw))[1] if Path(raw).exists() else None
    missing = [str(p) for p in (raw, coded, brand_table, verdicts) if not Path(p).exists()]
    if missing:
        return None, window, missing
    t4_raw = read_jsonl(raw)
    excl, window = t4_excluded(t4_raw)
    ca, cb = read_t4_coded(coded)
    return ({"coded_a": ca, "coded_b": cb, "brand_table": read_csv_rows(brand_table), "excluded": excl,
             "verdicts": json.loads(Path(verdicts).read_text(encoding="utf-8")), "window": window}, window, [])


def read_extra(path):
    return {(r["substrate"], r["brand"]): _num(r.get("value")) for r in read_csv_rows(path)} if path else None


# --------------------------------------------------------------------------- H5: v1.14's R* (clarification of 2026-11-10, N32-N34)
V114_PREREG_TAG = "v1.14-prereg-r1"                    # pushed 2026-11-10 (tag object 8398ab2d, commit 20fbc342)
V114_STAGE1_REL = "osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json"   # written once by score_v1_14.py --stage 1
V114_RANK_TABLE = "rank_table_t4_v1_14.csv"            # beside the Stage 1 file; its SHA-256 is in the Stage 1 file
V114_FLOOR = 6                                         # v1.14 section 3.1 rating floor (rankable mentions)
H5_CONDITION = "S0"                                    # section 3, H5: the t4 N3 S0 Phase B answers -> R*_S0


class BlindnessGuard(Refused):
    """The Ranking leg refuses to run before v1.14's Stage 1 output exists (v1.14 section 9, item 2)."""


def read_v114_stage1(path, condition=H5_CONDITION, allow_dry=False):
    """v1.14's locked R* per unit, read from its Stage 1 output (N32). Refuses (BlindnessGuard) while the file does not
    exist. condition "S0": R*_S0 where v1.14 rates it (rated_S0); "S1": R*_S1 where n_ranked_S1 >= 6 (v1.14's floor).
    Units of a substrate that v1.14 removed from its gate legs (MQ2, gate_excluded_substrates) are NOT RATED here too."""
    if not path or not Path(path).exists():
        raise BlindnessGuard(f"v1.14 Stage 1 output {path or V114_STAGE1_REL} does not exist: the Ranking leg does not run "
                             f"before it (blindness guard, v1.14 section 9 item 2)")
    data = Path(path).read_bytes()
    doc = json.loads(data.decode("utf-8"))
    if doc.get("phase") != "v1.14" or str(doc.get("stage")) != "1" or doc.get("prereg_tag") != V114_PREREG_TAG:
        raise Halt(f"{path} is not v1.14's Stage 1 output (phase/stage/prereg_tag = "
                   f"{doc.get('phase')}/{doc.get('stage')}/{doc.get('prereg_tag')})")
    if doc.get("dry_run") and not allow_dry:
        raise Halt(f"{path} is a v1.14 dry run, not its Stage 1 on t4")
    excl = set(doc.get("gate_excluded_substrates") or [])
    vals, rated = {}, 0
    for u in doc.get("units") or []:
        k = (u["substrate"], u["brand"])
        if condition == "S0":
            v, ok = _num(u.get("R_star_S0")), bool(u.get("rated_S0"))
        else:
            v, ok = _num(u.get("R_star_S1")), int(u.get("n_ranked_S1") or 0) >= V114_FLOOR
        vals[k] = v if (ok and v is not None and k[0] not in excl) else None
        rated += vals[k] is not None
    sv = lambda h: (doc.get(h) or {}).get("verdict")                                  # noqa: E731
    return {"file": str(path), "sha256": hashlib.sha256(data).hexdigest(), "condition": condition,
            "prereg_tag": doc.get("prereg_tag"), "created_utc": doc.get("created_utc"), "dry_run": bool(doc.get("dry_run")),
            "stage1_verdict": doc.get("STAGE1_VERDICT"),
            "v1_14_verdicts": {"H1_Sep_Presence": sv("H1_Sep_Presence"), "H2_Sep_Consistency": sv("H2_Sep_Consistency"),
                               "H4_Sep_Presence_S1": sv("H4_Sep_Presence_S1"), "components": doc.get("component_legs")},
            "gate_excluded_substrates": sorted(excl), "rated_units": rated,
            "rank_table_t4_sha256": doc.get("rank_table_t4_sha256"), "values": vals}


def mnp_from_rank_table(path, expected_sha256, condition=H5_CONDITION, excluded_subs=(), floor=V114_FLOOR):
    """v1.10's MNP (mean normalised position, 100 (1 - mean (k_mid - 1) / (n - 1)), lead-item rule, rated at >= 6
    rankable mentions) per unit from v1.14's hashed t4 rank table: the non-gating comparability figure (N33).
    A missing table -> not computed (reason); a table whose SHA-256 differs from the Stage 1 record halts."""
    if not path or not Path(path).exists():
        return {"status": "NOT_COMPUTED", "reason": f"rank table {path} not found", "values": {}}
    data = Path(path).read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    if expected_sha256 and sha != expected_sha256:
        raise Halt(f"v1.14 rank table {path}: SHA-256 {sha} differs from the Stage 1 record {expected_sha256}")
    acc = collections.defaultdict(list)
    for r in csv.DictReader(data.decode("utf-8").splitlines()):
        if (r.get("rule") != "lead_item" or r.get("condition") != condition or r.get("status") != "ok"
                or str(r.get("rankable")) != "1" or not r.get("brand") or r.get("k_mid") in ("", None)):
            continue
        n = float(r["n_named"])
        acc[(r["category"], r["brand"])].append((float(r["k_mid"]) - 1.0) / (n - 1.0))
    vals = {k: (100.0 * (1.0 - float(np.mean(q))) if len(q) >= floor and k[0] not in set(excluded_subs) else None)
            for k, q in acc.items()}
    return {"status": "COMPUTED", "file": str(path), "sha256": sha, "condition": condition, "floor": floor,
            "rated_units": sum(v is not None for v in vals.values()), "values": vals}


def load_ranking_source(stage1_path, condition=H5_CONDITION, allow_dry=False):
    """R* (gating) and MNP (non-gating) for H5 from v1.14's Stage 1 output directory."""
    src = read_v114_stage1(stage1_path, condition, allow_dry)
    src["MNP"] = mnp_from_rank_table(Path(stage1_path).parent / V114_RANK_TABLE, src["rank_table_t4_sha256"], condition,
                                     src["gate_excluded_substrates"])
    return src


def local_tag_exists(tag):
    r = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "-q", "--verify", f"refs/tags/{tag}"], capture_output=True,
                       text=True, timeout=60)
    return r.returncode == 0


def _ls_remote_tag(tag):
    r = subprocess.run(["git", "-C", str(ROOT), "ls-remote", "--tags", "origin", tag], capture_output=True, text=True,
                       timeout=60)
    if r.returncode != 0:
        raise Refused(f"git ls-remote failed ({r.stderr.strip()[:200]}); cannot verify tag {tag}")
    return r.stdout


def tag_on_origin(tag=PREREG_TAG):
    return f"refs/tags/{tag}" in _ls_remote_tag(tag)


def h5_inputs(stage1_path, real, unavailable=None):
    """N32/N34: (active, R* map or None, source record or None) for H5. Real run: H5 is active when tag
    v1.14-prereg-r1 exists (pushed before the v1.12 lock); synthetic run: active when a Stage 1 file is given. An active
    H5 without v1.14's Stage 1 output refuses the whole run (blindness guard) unless --h5-unavailable REASON is given,
    in which case H5 is UNDETERMINED with that reason (N30)."""
    active = local_tag_exists(V114_PREREG_TAG) if real else bool(stage1_path)
    if not active:
        return False, None, None
    if not stage1_path or not Path(stage1_path).exists():
        if unavailable:
            return True, None, None
        raise BlindnessGuard(f"H5 is active ({V114_PREREG_TAG}) but v1.14's Stage 1 output ({stage1_path or 'not given'}) "
                             f"does not exist: v1.12 is not scored before it (blindness guard); pass --h5-stage1 once it "
                             f"exists, or --h5-unavailable REASON for an UNDETERMINED H5 (N30)")
    src = load_ranking_source(stage1_path, H5_CONDITION, allow_dry=not real)
    return True, src["values"], src


def run_score(raw_path, coded_dir, t4_paths, verdicts_path, table_path, cfg, real, extra_paths=None,
              h6_cross_panel=False, h5_stage1=None, h5_unavailable=None):
    if real and not tag_on_origin():
        raise Refused(f"tag {PREREG_TAG} is not on origin: the v1.12 record is not scored before the lock")
    if h6_cross_panel:
        raise Refused("the cross-panel Sentiment fallback (v1.11's archived-wave score) was withdrawn by the "
                      "clarification of 2026-11-10 (N36): H6 is active only with a locked Sentiment score on the t4 answers")
    extra_paths = dict(extra_paths or {})
    extra_paths.pop("H5_Sep_Ranking", None)          # H5 reads v1.14's Stage 1 output only (N32)
    h5_active, h5_map, h5_src = h5_inputs(h5_stage1, real, h5_unavailable)
    mentions, registry = read_coded(coded_dir)
    t4, window, missing = load_t4(**t4_paths)
    extra = {h: read_extra(p) for h, p in extra_paths.items() if p}
    gates = {"enforce": True, "require_p1": real}
    if P1_PATH.exists() and real:
        gates["P1"] = json.loads(P1_PATH.read_text(encoding="utf-8")).get("v1_12")
    bf = json.loads(BRANDFREE_PATH.read_text(encoding="utf-8")) if BRANDFREE_PATH.exists() else None
    if bf:
        bf.pop("registry", None)
    inp = {"raw": read_jsonl(raw_path), "mentions": mentions, "registry": registry, "probes": load_probes(),
           "t4": t4, "t4_window": window, "t4_missing": missing,
           "profiles": read_csv_rows(PROFILES_PATH) if PROFILES_PATH.exists() else None,
           "active": {h: True for h in extra}, "extra": extra, "h6_cross_panel": h6_cross_panel, "brandfree": bf}
    if h5_active:
        inp["active"]["H5_Sep_Ranking"] = True
        if h5_map is not None:
            inp["extra"]["H5_Sep_Ranking"] = h5_map
        inp["h5_source"], inp["h5_unavailable"] = h5_src, h5_unavailable
    doc, rows = score_coverage(inp, cfg, gates)
    doc["inputs"] = {"raw": str(raw_path), "raw_sha256": sha256_file(raw_path), "coded": str(coded_dir),
                     "t4": {k: str(v) for k, v in t4_paths.items()}, "t4_missing": missing,
                     "scorer_sha256": sha256_file(__file__), "coder": verify_coder()}
    write_outputs(doc, rows, verdicts_path, table_path)
    return doc


def main():
    ap = argparse.ArgumentParser(description="AIAS v1.12 Coverage Paper A scorer")
    ap.add_argument("--calibrate-n1", action="store_true", help="run calibration N1 (section 2.4)")
    ap.add_argument("--code", action="store_true", help="code the Coverage answers with v0.42's coder (section 2.3)")
    ap.add_argument("--brandfree", action="store_true", help="MC_BrandFree on the 75 probes (section 4)")
    ap.add_argument("--parity-p1", action="store_true", help="parity gate P1 on the t3 omnibus answers (section 7.2)")
    ap.add_argument("--synthetic", metavar="DIR", help="score DIR/v112_raw.jsonl, DIR/coded and DIR/t4/* (synthetic "
                                                       "files only); outputs in DIR/_score")
    ap.add_argument("--run", action="store_true", help="score the real record (refuses unless the prereg tag is on origin)")
    ap.add_argument("--raw", default=str(RAW_PATH))
    ap.add_argument("--coded", default=str(CODED_DIR))
    for k, v in T4_DEFAULTS.items():
        ap.add_argument(f"--t4-{k.replace('_', '-')}", default=str(v))
    ap.add_argument("--h5-stage1", help=f"v1.14's Stage 1 output ({V114_STAGE1_REL}, with {V114_RANK_TABLE} beside it): "
                                        f"H5's R*_S0 (N32)")
    ap.add_argument("--h5-unavailable", metavar="REASON", help="score with H5 UNDETERMINED (N30) when v1.14's Stage 1 "
                                                                 "output cannot exist; logged")
    ap.add_argument("--h6", help="CSV substrate,brand,value: a locked Sentiment score on the t4 N3 answers, from a "
                                 "pre-registration tagged before the v1.12 lock (activates H6; N36). v1.11's archived-wave "
                                 "score does not activate H6")
    ap.add_argument("--h6-cross-panel", action="store_true", help="withdrawn (N36): refused")
    ap.add_argument("--draws", type=int, default=None, help="permutation/bootstrap draws (tests only)")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if a.calibrate_n1:
        out = a.out or str(N1_PATH)
        rec = run_n1(out)
        s = rec["statistic_r1"]
        print(f"N1 {s['result']}: pooled centred rho_w(Cov*, pi_cov) = {s['pooled_centred_rho_w']:.4f} (rule |rho_w| <= "
              f"{N1_RULE_RHO}); max |decile mean Cov* - 50| = {s['max_abs_decile_deviation_from_50']:.2f} (rule <= "
              f"{N1_RULE_DECILE}); mean signed per-category rho = {rec['per_category_rho']['mean_signed']:.4f}; "
              f"{s['n_units']} rated units; delta fits set to 0: {rec['delta_fit']['failures_set_to_zero']}; "
              f"runtime {rec['runtime_seconds']} s -> {out}")
        return 0 if s["result"] == "PASS" else 2
    try:
        if a.code:
            rec = run_code(a.raw, a.out or a.coded)
            print(f"coded {rec['calls_deduplicated']} calls ({rec['answered_calls_coded']} answered) -> "
                  f"{rec['mention_rows']} mention rows in {a.out or a.coded}")
            return 0
        if a.brandfree:
            C = load_coder()
            rec = brandfree_check(load_probes(), C)
            out = Path(a.out or BRANDFREE_PATH)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(rec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"MC_BrandFree {'PASS' if rec['passed'] else 'FAIL'}: {rec['probes']} probes x 5 detectors, "
                  f"hits={rec['hits']} -> {out}")
            return 0 if rec["passed"] else 2
        if a.parity_p1:
            out = Path(a.out or P1_PATH)
            out.parent.mkdir(parents=True, exist_ok=True)
            r = run_parity_p1(out)["v1_12"]
            print(f"P1 {'PASS' if r['passed'] else 'FAIL'}: mention cells={r['mention_cells']} "
                  f"mismatches={r['mention_mismatches']} -> {out}")
            return 0 if r["passed"] else 2
        if a.synthetic or a.run:
            cfg = Cfg(a.draws, a.draws) if a.draws else Cfg()
            ex = {"H6_Sep_Sentiment": a.h6}
            h5kw = {"h5_stage1": a.h5_stage1, "h5_unavailable": a.h5_unavailable}
            if a.synthetic:
                d = Path(a.synthetic).resolve()
                t4p = {"raw": d / "t4/t4_raw.jsonl", "coded": d / "t4/coded", "brand_table": d / "t4/v42_brand_table.csv",
                       "verdicts": d / "t4/v42_verdicts.json"}
                doc = run_score(d / "v112_raw.jsonl", d / "coded", t4p, d / "_score/v112_verdicts.json",
                                d / "_score/v112_unit_table.csv", cfg, False, ex, a.h6_cross_panel, **h5kw)
                dest = d / "_score"
            else:
                t4p = {"raw": a.t4_raw, "coded": a.t4_coded, "brand_table": a.t4_brand_table, "verdicts": a.t4_verdicts}
                doc = run_score(a.raw, a.coded, t4p, VERDICTS_PATH, UNIT_TABLE_PATH, cfg, True, ex, a.h6_cross_panel,
                                **h5kw)
                dest = VERDICTS_PATH.parent
            print(f"Paper A: {doc['paper_A_verdict']['label']} -> {dest}")
            for h, v in doc["verdicts"].items():
                print(f"  {h}: {v}")
            return 0
    except Refused as e:
        print(f"[v1.12] REFUSED: {e}", file=sys.stderr)
        return 3
    except Halt as e:
        print(f"[v1.12] HALT: {e}", file=sys.stderr)
        return 4
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
