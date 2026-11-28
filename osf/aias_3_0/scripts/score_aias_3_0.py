#!/usr/bin/env python3
"""
score_aias_3_0.py - AIAS(TM) 3.0 (the Coverage release): calibration of three scores (section 4), three-score
dissociation (section 5), sensitivities (10.1), S-Q beside every statistic (10.2), descriptives (10.3), the checks of
section 11.2 and the mechanical class of section 6.2.

STATUS: r0 (2026-11-28), written after the lock (tag aias-3-0-prereg-r1, commit 2545427; anchor f19d7a1) to the locked
text (osf/aias_3_0/prereg/PRE_REGISTRATION_aias_3_0.md; sections cited inline), as section 11.1 item 3 asks. Tested on
synthetic data only. Not run on program data. No network, no model call, no spend.

Reused unchanged: osf/methodology/v1_12/scripts/score_v1_12.py (blob 11cded95, SHA-256 f7689898 as in v1.12's lock
manifest; checked before every run): rho_w, paired, perm_p, bootstrap, the Coverage tables (coverage_table, cov_star),
the comparators (comparators_t4, t4_excluded, read_t4_coded) and the separability verdict.

Runs (each once; each refuses to overwrite its output; section 11.3):
  --calibration   -> osf/aias_3_0/outputs/aias_3_0_calibration.json   (primary and S-Q)
  --dissociation  -> osf/aias_3_0/outputs/aias_3_0_dissociation.json  (primary and S-Q) and aias_3_0_profile.csv (D1)
  both add their record of inputs to outputs/inputs_read_aias_3_0.json (one key per run).
  --sq-ref REF       the git ref that holds the S-Q wrapper's committed outputs (osf/methodology/v1_12/sensitivity/)
  --preview-ref REF  the git ref that holds the Preview's results file (section 5.4), if it exists
Other modes: --verify-lock (MQ_Lock), --pin-report (pinned refs and blobs; reads no statistic), --dry-run DIR
(synthetic world; never program data).

SCORER_NOTES (where the text is silent or ambiguous; none changes a test, band, floor, seed or rule; "A<n>" = listed in
the hand-off as an ambiguity, with the reading chosen closest to the text)
 N1  Unit key = (substrate, brand) as v112_unit_table.csv writes it (section 2). P = P_comparator, C* =
     C_star_comparator, Cov* = cov_star where rated == 1, mentions (K3) = t4_mentions_N3_S0, Cov*_C3 (SD) = cov_star_C3,
     Cov*_mid (SE) = cov_star_mid_S8, all read at 949be61 (section 3). "NOT RATED" = blank.
 N2  The Coverage tables for the calibration (halves, SHRINK, Cov*_mid halves) and SF (floors 6, 28) are rebuilt from
     v1.12's mentions, raw file and probes at 949be61 with v1.12's own functions (build_analysis, coverage_table with
     the Rasch-type null), on the N3 models; MQ_Parity checks that the rebuilt Cov* equals the unit table.
 N3  (A1) Permutation for a pair: the first-named variable is permuted within category (section 2): rho_w(Cov*, P)
     permutes Cov*, rho_w(P, C*) permutes P. v1.12's H1/H2 permuted the comparator; p is reported only, rho is the same.
 N4  (A2) H3_Cov_C_U3 is carried from v1.12 H2 only when the unit set after the >= 5-units rule equals v1.12's H2 set
     exactly; then rho must equal v1.12's within 1e-9 or the run halts (MQ_Parity). Otherwise it is computed.
 N5  (A3) K1_3 passes on the two Coverage conditions only (|rho_w(Cov_cand, P)| <= 0.50 and |rho_w(Cov_cand, C*)| <=
     0.50). C*'s own K1 (the Preview's H_PC_N3 where it exists, else D_PC_U3) is printed beside it and does not enter
     the pass. A constraint whose statistic cannot be computed (non-finite) does not pass. The n floor of section 2 is
     not applied to the calibration's constraints (a declared calibration, not a test, section 4.1); n is printed.
 N6  (A4) Ties in the selection (section 4.5): a candidate whose stepped-up reliability is >= best - 0.01 is tied
     (inclusive); among tied candidates the simpler wins lexicographically: Cov* over Cov*_mid, then FLOOR over SHRINK,
     then ADD3 over MOD3. A candidate with non-finite reliability cannot be selected.
 N7  (A5) Composite A needs P: a unit without P has no A (P is "always present", section 4.3). MOD3: a part not rated
     contributes the factor 0.5. SHRINK: w = n_b / (n_b + kappa) with n_b the brand's N3 mention total in the table
     used (full: kappa 14; each half: kappa 7); Cov*_u = v1.12's cov_star with floor 1 and 1 model (defined iff n_b >= 1
     and >= 1 model names the brand). FLOOR halves: floor 7 and >= 2 models (v1.12 H4). K3 uses the units with A and a
     mention count; K3's P difference uses the same units.
 N8  (A6) Bootstraps (reported, never a verdict input): 330010 = each candidate's rho_w(A, P) and half-split rho_w (with
     its stepped-up value), one call per statistic with the same seed; 330020 = R_adj, rho_w(Cov*, P), rho_w(Cov*, C*)
     and rho_w(P, C*) on U3 in one resampling loop; 330021 = the bridge (D3). 10,000 resamples, within category,
     percentile 95% (section 2).
 N9  (A7) Sensitivities (10.1): every sensitivity recomputes H3_Cov_Joint, H3_Cov_P_U3, H3_Cov_C_U3 and D_PC_U3 (no
     carried verdict), with its own seed (SA 330030, S-COI 330031, SB 330032, SC 330033, SD 330034, SE 330035, SF 330036)
     for every permutation inside it; no bootstrap. The calibration's constraints are recomputed in SC (named there)
     and in SA and S-COI (unit exclusions); SD-SF change the Coverage statistic of the dissociation only. SB (uncentred
     ranks) changes the pairwise rows; the joint regression keeps centred ranks (it has no intercept; the Preview's
     precedent, its section 10 SB).
 N10 (A8) S-Q inputs (10.2 step 4, 11.3): the S-Q wrapper (osf/methodology/v1_12/sensitivity/quotes_v1_12.py) writes,
     beside the files section 10.2 step 6 lists, v1.12's S-Q unit table (v112_unit_table_SQ.csv) and its S-Q mentions;
     every statistic here is computed on them in the same run as the primary. The run refuses if they do not exist or
     the wrapper's record does not show the reproduction with 0 differences (MQ_SQ).
 N11 (A9) Class (6.2): G3 UNDETERMINED is read as "not issued" (the table gives it no row); when G2 is UNDETERMINED and
     G3 is PARTLY DISTINCT, the class is U (G2's own row; B's headline needs an R_adj that does not exist).
 N12 D1 is written as outputs/aias_3_0_profile.csv (the text names no file). D2 terciles: within-category average rank
     of P over (n + 1): <= 1/3 low, <= 2/3 middle, else high (the Preview's N10). D3's legacy values come from
     aias_2_0_profiles.csv (wave t3, P; C_star where rated) at tag aias-2-0-data-locked; P_t3_legacy of the unit table
     is checked against it (within 1e-5: the profile file has six decimals).
 N13 (A10) inputs_read_aias_3_0.json holds one key per run (calibration, dissociation); a run refuses if its key exists.
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import io
import json
import math
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]                      # <repo>/osf/aias_3_0/scripts -> <repo>
V112_SCRIPTS = ROOT / "osf/methodology/v1_12/scripts"
if str(V112_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(V112_SCRIPTS))
import score_v1_12 as A  # noqa: E402  (locked at tag v1.12-prereg-r1; imported unchanged; blob-checked at run time)

PHASE_ID = "AIAS 3.0"
PREREG_TAG = "aias-3-0-prereg-r1"
PREREG_COMMIT = "2545427655a31d0a82623101e7bb5d8d3d34a1ea"
NAN = float("nan")

SEP_CONF, SEP_FALS = A.SEP_CONF, A.SEP_FALS                 # 0.30 / 0.50 (section 2)
N_FLOOR_UNITS, N_FLOOR_CATS, MIN_PER_CAT = A.N_FLOOR_UNITS, A.N_FLOOR_CATS, A.MIN_UNITS_PER_CAT   # 30 / 3 / 5
N_PERM, N_BOOT = 10_000, 10_000                             # section 2
PARITY_TOL = 1e-9                                           # section 3
K1_MAX, K2_MAX, K3_POINTS = 0.50, 0.95, 5.0                 # section 4.4
TIE = 0.01                                                  # section 4.5
FLOOR, HALF_FLOOR, MIN_MODELS = A.FLOOR_FULL, A.FLOOR_HALF, A.MIN_MODELS_NAMED   # 14 / 7 / 2
KAPPA_FULL, KAPPA_HALF = 14, 7                              # sections 4.3, 4.5
SF_FLOORS = tuple(A.FLOOR_SENS)                             # (6, 28)
N3 = list(A.PANELS["N3"])

SEEDS = {"H3_Cov_Joint": 330001, "H3_Cov_P_U3": 330002, "H3_Cov_C_U3": 330003, "D_PC_U3": 330004,
         "calibration_bootstrap": 330010, "dissociation_bootstrap": 330020, "bridge_bootstrap": 330021}
SENS_ORDER = ["SA", "S-COI", "SB", "SC", "SD", "SE", "SF"]   # section 10.1, seeds 330030-330036 in this order
SENS_SEEDS = {name: 330030 + i for i, name in enumerate(SENS_ORDER)}
DENON = tuple(A.DENON)
COI_UNITS = (("v0.19", "Denon"), ("v0.22", "Chevrolet"), ("v0.22", "BMW"), ("v0.22", "Bentley"), ("v0.23", "S03"),
             ("v0.20", "Eucerin"))                          # = score_v1_19.COI_UNITS (S03 = Jack Daniel's); section 15

STATS = ("Cov*", "Cov*_mid")
LOWS = ("FLOOR", "SHRINK")
FORMS = ("ADD3", "MOD3")
CANDIDATES = [(s, lo, f) for s in STATS for lo in LOWS for f in FORMS]   # 8 (section 4.3)
SELECTED_RULE = "Cov* (v1.12 section 2.4), floor 14, >= 2 models"        # section 4.2

DISTINCT, PARTLY, NOT_DISTINCT = "DISTINCT", "PARTLY DISTINCT", "NOT DISTINCT"
W1 = {"NO COMPOSITE": "No combination of the three scores both adds information to Presence and keeps each part "
                      "separate, so AIAS 3.0 reports three scores side by side.",
      "CANDIDATE COMPOSITE": "One combined score ({cand}) passed the calibration's constraints on one week of answers; it "
                             "is reported as a candidate and is not adopted until a wave that re-measures Coverage "
                             "confirms it."}


class Halt(RuntimeError):
    """A check that stops the run (section 11.2)."""


class Refused(RuntimeError):
    """A run that may not happen (lock, order, overwrite)."""


def _f(v) -> bool:
    return A._finite(v)


def drop_units(d: dict, exclude) -> dict:
    ex = {tuple(u) for u in exclude}
    return {u: v for u, v in d.items() if tuple(u) not in ex}


def keep_cats(d: dict, cats) -> dict:
    cats = set(cats)
    return {u: v for u, v in d.items() if u[0] in cats}


def band(value, ok: bool = True) -> str:
    """Separability bands on |value| (section 2): CONFIRMED <= 0.30, FALSIFIED >= 0.50, MARGINAL between."""
    if not ok or not _f(value):
        return "UNDETERMINED"
    a = abs(float(value))
    if a <= SEP_CONF:
        return "CONFIRMED"
    if a >= SEP_FALS:
        return "FALSIFIED"
    return "MARGINAL"


def below_floor(n: int, c: int) -> bool:
    """n floor of section 2: UNDETERMINED with fewer than 30 units pooled or fewer than 3 categories entering."""
    return n < N_FLOOR_UNITS or c < N_FLOOR_CATS


# =========================================================================== 5.3 pairwise rows
def pair_row(first: dict, second: dict, seed: int, n_perm: int = N_PERM, centred: bool = True) -> dict:
    """rho_w(first, second) on the pairwise-complete units (>= 5 per category, section 2); the FIRST-named variable is
    permuted within category (two-sided; N3); bands of section 2; UNDETERMINED below the n floor."""
    keys, x, y, g, info = A.paired(first, second)
    rho = A.rho_w(x, y, g, centred) if info["n"] >= 3 else NAN
    p = NAN
    if n_perm and info["n"] >= 3 and _f(rho):
        p = A.perm_p(y, x, g, rho, seed, "two", n_perm, centred)       # perm_p permutes its 2nd argument (= first)
    low = below_floor(info["n"], info["n_categories"])
    return {"rho_w": rho, "n": info["n"], "n_categories": info["n_categories"],
            "per_category": info["per_category"], "dropped_categories": info["dropped_categories"],
            "p_perm": p, "n_perm": n_perm, "perm_seed": seed, "sided": "two", "centred": centred,
            "below_n_floor": low, "verdict": band(rho, not low), "units": [list(k) for k in keys]}


# =========================================================================== 5.2 H3_Cov_Joint
def joint_arrays(cov: dict, P: dict, C: dict):
    """U3 rows after the >= 5-units rule: centred within-category ranks of Cov* (y) and of P, C* (X), recomputed within
    U3 (section 5.2). Returns keys, y, X, groups, n, c."""
    keys = sorted(u for u in cov if _f(cov.get(u)) and _f(P.get(u)) and _f(C.get(u)))
    per = collections.Counter(k[0] for k in keys)
    keep = {k for k, v in per.items() if v >= MIN_PER_CAT}
    keys = [k for k in keys if k[0] in keep]
    g = np.array([k[0] for k in keys])
    if not keys:
        return keys, np.array([]), np.zeros((0, 2)), g, 0, 0
    y = A.centred_within_ranks(np.array([cov[k] for k in keys], float), g)
    X = np.column_stack([A.centred_within_ranks(np.array([d[k] for k in keys], float), g) for d in (P, C)])
    return keys, y, X, g, len(keys), len(keep)


def r2_of(y: np.ndarray, X: np.ndarray) -> float:
    """Least squares of y on X, no intercept; R^2 = 1 - SSR / SST (SST = y'y: ranks are centred)."""
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    sst = float(y @ y)
    return 1.0 - float(resid @ resid) / sst if sst > 0 else NAN


def r_adj_of(r2: float, n: int, c: int, j: int = 2) -> tuple[float, float]:
    """R^2_adj = 1 - (1 - R^2)(n - c)/(n - c - j); R_adj = sqrt(max(0, R^2_adj)) (section 5.2, j = 2)."""
    if not _f(r2) or n - c - j <= 0:
        return NAN, NAN
    r2a = 1.0 - (1.0 - r2) * (n - c) / (n - c - j)
    return r2a, math.sqrt(max(0.0, r2a))


def joint_test(cov: dict, P: dict, C: dict, seed: int = SEEDS["H3_Cov_Joint"], n_perm: int = N_PERM) -> dict:
    """H3_Cov_Joint (section 5.2): the Preview's I-test with j = 2 on U3. CONFIRMED iff R_adj <= 0.30, FALSIFIED iff
    R_adj >= 0.50, MARGINAL otherwise, UNDETERMINED below the n floor. One-sided permutation p on R^2 (Cov* ranks
    permuted within category; p = (1 + hits) / (n_perm + 1))."""
    keys, y, X, g, n, c = joint_arrays(cov, P, C)
    out = {"statistic": "R_adj", "n": n, "categories": c, "predecessors": ["P", "C*"], "perm_seed": seed,
           "n_perm": n_perm, "sided": "one (R^2)", "units": [list(k) for k in keys],
           "per_category": dict(sorted(collections.Counter(k[0] for k in keys).items()))}
    if below_floor(n, c) or n - c - 2 <= 0:
        out.update(R2=NAN, R2_adj=NAN, R_adj=NAN, p_perm=NAN, below_n_floor=True, verdict="UNDETERMINED")
        return out
    r2 = r2_of(y, X)
    r2a, radj = r_adj_of(r2, n, c)
    p = NAN
    if n_perm:
        rng = np.random.default_rng(seed)
        gidx = A._group_index(g)
        idx = np.arange(n)
        hits = 0
        for _ in range(n_perm):
            for gi in gidx:
                idx[gi] = rng.permutation(gi)
            hits += bool(r2_of(y[idx], X) >= r2 - A.TOL)
        p = (1 + hits) / (n_perm + 1)
    out.update(R2=r2, R2_adj=r2a, R_adj=radj, p_perm=p, below_n_floor=False, verdict=band(radj, _f(radj)))
    return out


# =========================================================================== 5.1-5.5 dissociation on one set of scores
def u3_units(P: dict, C: dict, cov: dict) -> list:
    """U3 (section 5.1): P defined, C* rated and Cov* rated."""
    return sorted(u for u in cov if _f(cov.get(u)) and _f(P.get(u)) and _f(C.get(u)))


def _on(d: dict, keys) -> dict:
    return {k: d[k] for k in keys}


def dissociation(P: dict, C: dict, cov: dict, n_perm: int = N_PERM, seeds: dict | None = None, centred: bool = True,
                 carried_h2: dict | None = None) -> dict:
    """H3_Cov_Joint (primary), H3_Cov_P_U3, H3_Cov_C_U3 (secondary) and D_PC_U3 (descriptive) on U3.
    seeds: {test: seed} (sensitivities pass one seed for all); carried_h2: v1.12's H2 {"units", "rho_w", "verdict"}."""
    seeds = seeds or SEEDS
    U3 = u3_units(P, C, cov)
    cv, p_, c_ = _on(cov, U3), _on(P, U3), _on(C, U3)
    joint = joint_test(cv, p_, c_, seeds["H3_Cov_Joint"], n_perm)
    pc = pair_row(cv, p_, seeds["H3_Cov_P_U3"], n_perm, centred)
    cc = pair_row(cv, c_, seeds["H3_Cov_C_U3"], n_perm, centred)
    dpc = pair_row(p_, c_, seeds["D_PC_U3"], n_perm, centred)
    cc["source"] = "AIAS 3.0 (computed on U3)"
    if carried_h2 is not None:
        same = {tuple(u) for u in cc["units"]} == {tuple(u) for u in carried_h2["units"]}
        cc["U3_equals_v112_H2_set"] = same
        if same:
            if not (_f(cc["rho_w"]) and abs(cc["rho_w"] - carried_h2["rho_w"]) <= PARITY_TOL):
                raise Halt(f"MQ_Parity: H3_Cov_C_U3 on v1.12's H2 set gives {cc['rho_w']!r}, v1.12 H2 "
                           f"{carried_h2['rho_w']!r}")
            cc.update(verdict=carried_h2["verdict"], source="carried: v1.12 H2_Sep_Consistency (section 5.3)")
    dpc["verdict_reading"] = dpc.pop("verdict")
    dpc["role"] = "descriptive (section 5.3)"
    return {"U3": {"n": len(U3), "units": [list(u) for u in U3]},
            "joint": joint, "pairs": {"P_Cov": pc, "C_Cov": cc, "P_C": dpc},
            "verdicts": {"H3_Cov_Joint": joint["verdict"], "H3_Cov_P_U3": pc["verdict"],
                         "H3_Cov_C_U3": cc["verdict"]}}


def dissociation_bootstrap(P: dict, C: dict, cov: dict, n_boot: int = N_BOOT,
                           seed: int = SEEDS["dissociation_bootstrap"]) -> dict:
    """Percentile 95% intervals (units resampled within category; seed 330020) of R_adj and the three rho_w on U3
    (after the >= 5-units rule). Reported, never a verdict input (section 2)."""
    keys, y, X, g, n, c = joint_arrays(*(_on(d, u3_units(P, C, cov)) for d in (cov, P, C)))
    if below_floor(n, c) or n - c - 2 <= 0 or not n_boot:
        return {"status": "not computed (below the n floor or no draws)", "n_boot": n_boot, "seed": seed}
    vc = np.array([cov[k] for k in keys], float)
    vp = np.array([P[k] for k in keys], float)
    vC = np.array([C[k] for k in keys], float)

    def fn(i):
        gi = g[i]
        yy = A.centred_within_ranks(vc[i], gi)
        XX = np.column_stack([A.centred_within_ranks(v[i], gi) for v in (vp, vC)])
        return {"R_adj": r_adj_of(r2_of(yy, XX), n, c)[1], "rho_Cov_P": A.rho_w(vc[i], vp[i], gi),
                "rho_Cov_C": A.rho_w(vc[i], vC[i], gi), "rho_P_C": A.rho_w(vp[i], vC[i], gi)}
    b = A.bootstrap(g, seed, n_boot, fn)
    return {"seed": seed, "n_boot": n_boot, "percentile": 95, "intervals": b}


# =========================================================================== 4 calibration of three scores
def cand_name(c) -> str:
    stat, low, form = c
    return f"{form} | {stat} | {low}"


def cov_from_table(tab: dict, units, stat: str = "Cov*", low: str = "FLOOR", floor: int = FLOOR,
                   kappa: int = KAPPA_FULL, panel=None) -> dict:
    """Coverage of every unit for one candidate rule (sections 4.2-4.3), from a v1.12 beta table (one panel).
    FLOOR: v1.12's cov_star (NOT RATED below the floor or with fewer than 2 models). SHRINK: w Cov*_u + (1 - w) 50,
    w = n_b / (n_b + kappa), Cov*_u = cov_star without the floor (n_b >= 1, >= 1 model), else NOT RATED."""
    panel = panel or N3
    key = "beta" if stat == "Cov*" else "beta_mid"
    out = {}
    for (s, b) in units:
        if low == "FLOOR":
            out[(s, b)] = A.cov_star(tab, s, b, panel, floor, MIN_MODELS, key)["cov_star"]
        else:
            r = A.cov_star(tab, s, b, panel, 1, 1, key)
            if r["cov_star"] is None:
                out[(s, b)] = None
            else:
                w = r["n_b"] / (r["n_b"] + kappa)
                out[(s, b)] = w * r["cov_star"] + (1.0 - w) * 50.0
    return out


def composite(P: dict, C: dict, cov: dict, form: str) -> dict:
    """ADD3: mean of the rated scores among P, C*, Cov (a part not rated drops out); MOD3: P (0.5 + 0.5 C*/100)
    (0.5 + 0.5 Cov/100), factor 0.5 for a part not rated (section 4.3). No P -> no A (N7)."""
    out = {}
    for u, p in P.items():
        if not _f(p):
            out[u] = None
            continue
        c, v = C.get(u), cov.get(u)
        if form == "ADD3":
            out[u] = float(np.mean([x for x in (p, c, v) if _f(x)]))
        else:
            fc = 0.5 + 0.5 * c / 100.0 if _f(c) else 0.5
            fv = 0.5 + 0.5 * v / 100.0 if _f(v) else 0.5
            out[u] = p * fc * fv
    return out


def k3_windfall(Amap: dict, P: dict, mentions: dict) -> dict:
    """K3_3 (section 4.4): mean A over units with 1-2 N3 S0 recall mentions minus mean A over units with none must be
    <= the same difference in P plus 5 points (units with A and a mention count; N7)."""
    keys = [u for u in Amap if _f(Amap.get(u)) and mentions.get(u) is not None]
    low = [u for u in keys if 1 <= mentions[u] <= 2]
    none = [u for u in keys if mentions[u] == 0]
    if not low or not none:
        return {"dA": NAN, "dP": NAN, "limit": NAN, "n_low": len(low), "n_none": len(none), "passes": False}
    dA = float(np.mean([Amap[u] for u in low]) - np.mean([Amap[u] for u in none]))
    dP = float(np.mean([P[u] for u in low]) - np.mean([P[u] for u in none]))
    return {"dA": dA, "dP": dP, "limit": dP + K3_POINTS, "n_low": len(low), "n_none": len(none),
            "passes": bool(dA <= dP + K3_POINTS)}


def _rho(xd: dict, yd: dict) -> dict:
    keys, x, y, g, info = A.paired(xd, yd)
    return {"rho_w": A.rho_w(x, y, g) if info["n"] >= 3 else NAN, "n": info["n"], "n_categories": info["n_categories"]}


def candidate_row(c, world: dict, n_boot: int = 0, seed: int = SEEDS["calibration_bootstrap"]) -> dict:
    """One row of the 8-row table (section 4.5): K1_3, K2_3, K3_3 and the half-split reliability."""
    stat, low, form = c
    units, P, C, tabs = world["units"], world["P"], world["C"], world["tabs"]
    cov = cov_from_table(tabs["full"], units, stat, low, FLOOR, KAPPA_FULL)
    k1p, k1c = _rho(cov, P), _rho(cov, C)
    k1 = {"rho_Cov_P": k1p, "rho_Cov_C": k1c, "line": K1_MAX,
          "passes": bool(_f(k1p["rho_w"]) and _f(k1c["rho_w"]) and abs(k1p["rho_w"]) <= K1_MAX
                         and abs(k1c["rho_w"]) <= K1_MAX)}
    Am = composite(P, C, cov, form)
    k2r = _rho(Am, P)
    k2 = dict(k2r, line=K2_MAX, passes=bool(_f(k2r["rho_w"]) and abs(k2r["rho_w"]) <= K2_MAX))
    k3 = k3_windfall(Am, P, world["mentions"])
    halves = {}
    for h in ("A", "B"):
        cv = cov_from_table(tabs[h], units, stat, low, HALF_FLOOR, KAPPA_HALF)
        halves[h] = composite(P, C, cv, form)
    rh = _rho(halves["A"], halves["B"])
    rel = A.spearman_brown_half(rh["rho_w"]) if _f(rh["rho_w"]) else NAN
    row = {"candidate": cand_name(c), "coverage_statistic": stat, "low_count_rule": low, "form": form,
           "n_cov_rated": sum(1 for v in cov.values() if _f(v)), "n_A": sum(1 for v in Am.values() if _f(v)),
           "K1_3": k1, "K2_3": k2, "K3_3": k3,
           "reliability": {"rho_w_halfA_halfB": rh["rho_w"], "n": rh["n"], "stepped_up": rel,
                           "half_floor": HALF_FLOOR if low == "FLOOR" else None,
                           "half_kappa": KAPPA_HALF if low == "SHRINK" else None},
           "passes_all": bool(k1["passes"] and k2["passes"] and k3["passes"])}
    if n_boot:
        for name, (xd, yd, tf) in {"rho_A_P": (Am, P, None),
                                   "half_split": (halves["A"], halves["B"], A.spearman_brown_half)}.items():
            keys, x, y, g, info = A.paired(xd, yd)
            if info["n"] < 3:
                continue

            def fn(i, x=x, y=y, g=g, tf=tf):
                r = A.rho_w(x[i], y[i], g[i])
                return {"rho_w": r, "stepped_up": tf(r) if (tf and _f(r)) else NAN}
            row.setdefault("bootstrap", {"seed": seed, "n_boot": n_boot})[name] = A.bootstrap(g, seed, n_boot, fn)
    return row, Am


def select(rows: list[dict]) -> dict:
    """Section 4.5 (N6): among candidates passing K1_3-K3_3, the highest stepped-up reliability; ties within 0.01 go to
    the simpler choice (Cov* over Cov*_mid, FLOOR over SHRINK, ADD3 over MOD3). None passing -> NO COMPOSITE."""
    passing = [r for r in rows if r["passes_all"] and _f(r["reliability"]["stepped_up"])]
    best_ap = min((r for r in rows if _f(r["K2_3"]["rho_w"])), key=lambda r: abs(r["K2_3"]["rho_w"]), default=None)
    best = {"rho_A_P": best_ap["K2_3"]["rho_w"] if best_ap else NAN, "candidate": best_ap["candidate"] if best_ap else None}
    if not passing:
        return {"verdict": "NO COMPOSITE", "selected": None, "tied": [], "best": best,
                "sentence": W1["NO COMPOSITE"], "adopted": False}
    top = max(r["reliability"]["stepped_up"] for r in passing)
    tied = [r for r in passing if r["reliability"]["stepped_up"] >= top - TIE - 1e-12]
    simple = lambda r: (STATS.index(r["coverage_statistic"]), LOWS.index(r["low_count_rule"]), FORMS.index(r["form"]))  # noqa: E731
    sel = sorted(tied, key=simple)[0]
    return {"verdict": "CANDIDATE COMPOSITE", "selected": sel["candidate"], "tied": [r["candidate"] for r in tied],
            "best": best, "best_reliability": top, "sentence": W1["CANDIDATE COMPOSITE"].format(cand=sel["candidate"]),
            "adopted": False, "not_adopted_reason": "section 4.6 default (section 17 choice 2): not adopted in 3.0"}


def calibration(world: dict, n_boot: int = 0, c_k1: dict | None = None) -> dict:
    """Section 4: CAL_RULE (4.2), the eight candidates (4.3) against K1_3-K3_3 (4.4), the selection (4.5)."""
    units, tabs = world["units"], world["tabs"]
    rated = {u for u, v in world["Cov"].items() if _f(v)}
    rule = {"selected": {"rule": SELECTED_RULE, "share_rated_112": len(rated) / len(units), "rated": len(rated),
                         "units": len(units)},
            "descriptive_beside": {f"floor_{f}": sum(1 for v in cov_from_table(tabs["full"], units, "Cov*", "FLOOR", f)
                                                     .values() if _f(v)) / len(units) for f in SF_FLOORS}}
    rule["descriptive_beside"]["Cov*_mid_floor_14"] = sum(
        1 for v in cov_from_table(tabs["full"], units, "Cov*_mid", "FLOOR", FLOOR).values() if _f(v)) / len(units)
    rows = []
    for c in CANDIDATES:
        row, _A = candidate_row(c, world, n_boot)
        rows.append(row)
    sel = select(rows)
    return {"CAL_RULE": rule, "candidates": len(rows), "table": rows, "composite": sel,
            "C_star_K1": c_k1 or {"status": "not supplied"},
            "W1_comparison": {"K2_line": K2_MAX, "AIAS_2_0_rho_A_P": 0.969}}


# =========================================================================== 10.1 sensitivities (never change a verdict)
def _sens_seeds(name: str) -> dict:
    return {k: SENS_SEEDS[name] for k in ("H3_Cov_Joint", "H3_Cov_P_U3", "H3_Cov_C_U3", "D_PC_U3")}


def _short(d: dict) -> dict:
    j, p = d["joint"], d["pairs"]
    return {"H3_Cov_Joint": {"R_adj": j["R_adj"], "n": j["n"], "categories": j["categories"], "p_perm": j["p_perm"],
                             "verdict": j["verdict"]},
            "H3_Cov_P_U3": {k: p["P_Cov"][k] for k in ("rho_w", "n", "p_perm", "verdict")},
            "H3_Cov_C_U3": {k: p["C_Cov"][k] for k in ("rho_w", "n", "p_perm", "verdict")},
            "D_PC_U3": {k: p["P_C"][k] for k in ("rho_w", "n", "p_perm", "verdict_reading")}}


def _cal_short(cal: dict) -> dict:
    return {"verdict": cal["composite"]["verdict"], "selected": cal["composite"]["selected"],
            "rows": {r["candidate"]: {"K1_3": r["K1_3"]["passes"], "K2_3": r["K2_3"]["passes"],
                                      "K3_3": r["K3_3"]["passes"], "rho_A_P": r["K2_3"]["rho_w"],
                                      "rho_Cov_P": r["K1_3"]["rho_Cov_P"]["rho_w"],
                                      "rho_Cov_C": r["K1_3"]["rho_Cov_C"]["rho_w"],
                                      "stepped_up": r["reliability"]["stepped_up"]} for r in cal["table"]}}


def _world_without(world: dict, exclude=(), cats=None) -> dict:
    w = dict(world)
    for k in ("P", "C", "Cov", "mentions", "cov_C3", "cov_mid"):
        if k in w and w[k] is not None:
            d = drop_units(w[k], exclude)
            w[k] = keep_cats(d, cats) if cats is not None else d
    w["units"] = [u for u in world["units"] if tuple(u) not in {tuple(x) for x in exclude}
                  and (cats is None or u[0] in set(cats))]
    return w


def sensitivities(world: dict, n_perm: int = N_PERM, with_calibration: bool = True) -> dict:
    """Section 10.1: SA, S-COI, SB, SC, SD, SE, SF (seeds 330030-330036). N9."""
    P, C, cov = world["P"], world["C"], world["Cov"]
    out = {}
    for name, excl in (("SA", [DENON]), ("S-COI", list(COI_UNITS))):
        w = _world_without(world, excl)
        rec = {"excluded": [list(u) for u in excl],
               "dissociation": _short(dissociation(w["P"], w["C"], w["Cov"], n_perm, _sens_seeds(name)))}
        if with_calibration and world.get("tabs"):
            rec["calibration"] = _cal_short(calibration(w))
        out[name] = rec
    out["SB"] = {"what": "uncentred pooled ranks for the pairwise rows (v1.12 S9); the joint test keeps centred ranks",
                 "dissociation": _short(dissociation(P, C, cov, n_perm, _sens_seeds("SB"), centred=False))}
    cats = sorted({u[0] for u in world["units"]})
    loo = {}
    for c in cats:
        w = _world_without(world, cats=[x for x in cats if x != c])
        rec = {"dissociation": _short(dissociation(w["P"], w["C"], w["Cov"], n_perm, _sens_seeds("SC")))}
        if with_calibration and world.get("tabs"):
            rec["calibration"] = _cal_short(calibration(w))
        loo[f"without {c}"] = rec
    out["SC"] = {"leave_one_category_out": loo, "range": _sc_range(loo)}
    if world.get("cov_C3") is not None:
        out["SD"] = {"what": "Cov* from the continuity panel C3 (cov_star_C3); comparators unchanged",
                     "dissociation": _short(dissociation(P, C, world["cov_C3"], n_perm, _sens_seeds("SD")))}
    if world.get("cov_mid") is not None:
        out["SE"] = {"what": "Cov*_mid (cov_star_mid_S8) in place of Cov*",
                     "dissociation": _short(dissociation(P, C, world["cov_mid"], n_perm, _sens_seeds("SE")))}
    if world.get("tabs"):
        out["SF"] = {f"floor_{f}": {"dissociation": _short(dissociation(
            P, C, cov_from_table(world["tabs"]["full"], world["units"], "Cov*", "FLOOR", f), n_perm,
            _sens_seeds("SF")))} for f in SF_FLOORS}
    return out


def _sc_range(loo: dict) -> dict:
    def rng(vals):
        v = [x for x in vals if _f(x)]
        return [min(v), max(v)] if v else None
    d = [r["dissociation"] for r in loo.values()]
    return {"R_adj": rng(x["H3_Cov_Joint"]["R_adj"] for x in d),
            "rho_Cov_P": rng(x["H3_Cov_P_U3"]["rho_w"] for x in d),
            "rho_Cov_C": rng(x["H3_Cov_C_U3"]["rho_w"] for x in d),
            "rho_P_C": rng(x["D_PC_U3"]["rho_w"] for x in d)}


def verdict_changes(primary: dict, sens: dict) -> list:
    """Every label that differs from the primary one under a sensitivity (listed; never changes a verdict)."""
    out = []

    def walk(name, rec):
        if "dissociation" in rec:
            for t in ("H3_Cov_Joint", "H3_Cov_P_U3", "H3_Cov_C_U3"):
                v = rec["dissociation"][t]["verdict"]
                if v != primary[t]:
                    out.append({"sensitivity": name, "test": t, "primary": primary[t], "under_sensitivity": v})
        if "calibration" in rec and rec["calibration"]["verdict"] != primary.get("composite"):
            out.append({"sensitivity": name, "test": "composite", "primary": primary.get("composite"),
                        "under_sensitivity": rec["calibration"]["verdict"]})
        for k, v in rec.items():
            if isinstance(v, dict) and k not in ("dissociation", "calibration", "range"):
                walk(f"{name} / {k}", v)
    for name, rec in sens.items():
        walk(name, rec)
    return out


# =========================================================================== 10.3 descriptives
def _dist(vals) -> dict:
    return A.distribution(vals)


def terciles(P: dict) -> dict:
    """Within-category Presence tercile (N12)."""
    out = {}
    for c in sorted({u[0] for u in P}):
        keys = [u for u in P if u[0] == c and _f(P[u])]
        if not keys:
            continue
        r = A.within_ranks(np.array([P[u] for u in keys], float), np.array([c] * len(keys)))
        for u, rk in zip(keys, r):
            q = rk / (len(keys) + 1)
            out[u] = "low" if q <= 1 / 3 else ("middle" if q <= 2 / 3 else "high")
    return out


def d2_rated(world: dict) -> dict:
    P, C, cov, units = world["P"], world["C"], world["Cov"], world["units"]
    U3 = set(u3_units(P, C, cov))
    t = terciles(P)
    per = {}
    for c in sorted({u[0] for u in units}):
        us = [u for u in units if u[0] == c]
        per[c] = {"units": len(us), "P_defined": sum(_f(P.get(u)) for u in us), "C_rated": sum(_f(C.get(u)) for u in us),
                  "Cov_rated": sum(_f(cov.get(u)) for u in us), "U3": sum(u in U3 for u in us)}
    by_t = {k: {"units": sum(1 for u in units if t.get(u) == k), "Cov_rated": sum(1 for u in units if t.get(u) == k
                                                                                    and _f(cov.get(u))),
                "U3": sum(1 for u in units if t.get(u) == k and u in U3)} for k in ("low", "middle", "high")}
    return {"per_category": per, "by_presence_tercile": by_t, "U3_share_of_112": len(U3) / len(units) if units else NAN}


def d3_bridge(P: dict, C: dict, P_t3: dict, C_t3: dict, n_boot: int = N_BOOT,
              seed: int = SEEDS["bridge_bootstrap"]) -> dict:
    """Section 10.3 D3: rho_w(P_AIAS2.0,t3, P_N3) with the mean level shift of P (N3 - t3) and its bootstrap interval
    (seed 330021); rho_w(C*_AIAS2.0,t3, C*_N3) without a level comparison. Descriptive."""
    out = {}
    keys, x, y, g, info = A.paired(P_t3, P)
    rho = A.rho_w(x, y, g) if info["n"] >= 3 else NAN
    rec = {"rho_w": rho, "n": info["n"], "n_categories": info["n_categories"],
           "mean_level_shift_N3_minus_t3": float(np.mean(y - x)) if info["n"] else NAN}
    if n_boot and info["n"] >= 3:
        rec["bootstrap"] = A.bootstrap(g, seed, n_boot, lambda i: {"rho_w": A.rho_w(x[i], y[i], g[i]),
                                                                   "mean_level_shift": float(np.mean(y[i] - x[i]))})
    out["P"] = rec
    keys, x, y, g, info = A.paired(C_t3, C)
    rec = {"rho_w": A.rho_w(x, y, g) if info["n"] >= 3 else NAN, "n": info["n"], "n_categories": info["n_categories"],
           "level_comparison": "none (phi_max depends on the number of models; AIAS 2.0 outline D9)"}
    if n_boot and info["n"] >= 3:
        rec["bootstrap"] = A.bootstrap(g, seed, n_boot, lambda i: {"rho_w": A.rho_w(x[i], y[i], g[i])})
    out["C_star"] = rec
    return out


def d4_joint(world: dict) -> dict:
    """Joint distribution of the three scores on U3, by category: quartiles and within-category Spearman matrix."""
    P, C, cov = world["P"], world["C"], world["Cov"]
    U3 = u3_units(P, C, cov)
    out = {}
    for c in sorted({u[0] for u in U3}):
        us = [u for u in U3 if u[0] == c]
        rec = {"n": len(us), "P": _dist([P[u] for u in us]), "C_star": _dist([C[u] for u in us]),
               "Cov_star": _dist([cov[u] for u in us])}
        if len(us) >= 3:
            g = np.array([c] * len(us))
            vs = {k: np.array([d[u] for u in us], float) for k, d in (("P", P), ("C", C), ("Cov", cov))}
            rec["spearman"] = {"P_C": A.rho_w(vs["P"], vs["C"], g), "P_Cov": A.rho_w(vs["P"], vs["Cov"], g),
                               "C_Cov": A.rho_w(vs["C"], vs["Cov"], g)}
        out[c] = rec
    return out


def profile_rows(world: dict) -> list[dict]:
    """D1: the per-unit profile (P, C*, Cov*, rated flags, labels)."""
    rows = []
    U3 = set(u3_units(world["P"], world["C"], world["Cov"]))
    for u in world["units"]:
        p, c, v = world["P"].get(u), world["C"].get(u), world["Cov"].get(u)
        rows.append({"substrate": u[0], "brand": u[1], "P": p if _f(p) else "", "C_star": c if _f(c) else "",
                     "Cov_star": v if _f(v) else "", "P_defined": int(_f(p)), "C_rated": int(_f(c)),
                     "Cov_rated": int(_f(v)), "in_U3": int(u in U3),
                     "label": "rated on all three" if u in U3 else "NOT RATED on " + ", ".join(
                         n for n, x in (("P", p), ("C*", c), ("Cov*", v)) if not _f(x))})
    return rows


# =========================================================================== 6.2 class (mechanical)
def wording_class(g2: str, g3: str | None) -> dict:
    """Section 6.2 (N11). g2 = H3_Cov_Joint's verdict; g3 = the Preview's Cov* status or None (not issued)."""
    g3n = None if g3 in (None, "", "UNDETERMINED", "NOT ISSUED") else g3
    if g2 == "FALSIFIED" or g3n == NOT_DISTINCT:
        cls = "C"
    elif g2 == "UNDETERMINED":
        cls = "U"
    elif g2 == "MARGINAL" or g3n == PARTLY:
        cls = "B"
    elif g2 == "CONFIRMED" and g3n in (None, DISTINCT):
        cls = "A"
    else:
        raise ValueError(f"no class for G2={g2!r}, G3={g3!r}")
    return {"class": cls, "G2": g2, "G3": g3 if g3 else "not issued", "G3_read_as": g3n or "not issued",
            "drafting_pauses": cls == "C",
            "both_stated": bool(g3n) and ((g2 == "CONFIRMED") != (g3n == DISTINCT))}


# =========================================================================== inputs (sections 0.1, 3, 11.2 MQ_Inputs)
PINS = {
    "v1.12": {"ref": "949be61e01dfad9773e43b0855dc33e9de3cc852", "lock_tag": "v1.12-prereg-r1",
              "lock_commit": "49efc473a63f415b9ae3eaa86811ca62fd81b91a",
              "manifest": "osf/methodology/v1_12/prereg/LOCK_MANIFEST_v1_12.sha256",
              "scorer": "osf/methodology/v1_12/scripts/score_v1_12.py",
              "scorer_blob": "11cded95437fd2ed30c1cdf1120b23a5a3cebe2d",
              "scorer_sha256": "f7689898fdc68715f207ffc0c1e335a0264aefcce0b2836d1fd5e79624709d20",
              "unit_table": "osf/methodology/v1_12/v112_unit_table.csv",
              "verdicts": "osf/methodology/v1_12/v112_verdicts.json",
              "raw": "osf/methodology/v1_12/data/v112_raw.jsonl",
              "coded_dir": "osf/methodology/v1_12/data/coded",
              "probes": "osf/methodology/v1_12/prereg/probes_v1_12.jsonl"},
    "v0.42": {"ref": "31c64c64656b7b0393eca49e5d10384744475dd9",
              "brand_table": "osf/v42/v42_brand_table.csv", "verdicts": "osf/v42/v42_verdicts.json",
              "coded_dir": "osf/v42/data/coded", "raw": "osf/v42/data/t4_raw.jsonl"},
    "v0.45_SQ": {"ref": "47f174810946401862b02de3ebe8f6f1f7c8d3e6",
                 "brand_table": "osf/v45/sensitivity/t4_SQ/v42_brand_table_SQ.csv",
                 "brand_table_sha256": "de8559cbe21db91e8922337c7ab5bdfaa7d1d2325f6bbe0870e6abcd812a5c4d",
                 "coded_dir": "osf/v45/sensitivity/t4_SQ/coded",
                 "verdicts": "osf/v45/sensitivity/t4_SQ/v42_verdicts_SQ.json"},
    "aias_2_0": {"ref": "aias-2-0-data-locked", "commit": "94f66182beac37d620006b1be127d72f2c5e0e1e",
                 "path": "osf/aias_2_0/aias_2_0_profiles.csv",
                 "sha256": "022ef56ecad9ddb60ad9ce0a2129698fd84ee9656630500e30b05f1e4b7e8c6e"},
    "v1.19": {"ref": "6e8f1570de0967749a7ab2e8e0a4e968c9a18c06",
              "verdicts": "osf/methodology/v1_19/outputs/v119_verdicts.json"},
    "preview": {"lock_tag": "aias-6-0-preview-prereg-r1", "lock_commit": "598990b8a5d761c9ee13c2dd7f00ca8cfb91c673",
                "results": "osf/aias_6_0_preview/outputs/results_aias_6_0_preview.json"},
    "sq": {"unit_table": "osf/methodology/v1_12/sensitivity/v112_unit_table_SQ.csv",
           "coded_dir": "osf/methodology/v1_12/sensitivity/coded_SQ",
           "record": "osf/methodology/v1_12/sensitivity/sq_record_v1_12.json"},
}
T4_CODED_FILES = [f"{s}_phase_{p}.csv" for s in A.RAW_SUB.values() for p in ("a", "b")]
V112_CODED_FILES = ["v112_mentions.csv", "registry_v1_12.json"]
OUT_REL = "osf/aias_3_0/outputs"
OUT_NAMES = {"calibration": "aias_3_0_calibration.json", "dissociation": "aias_3_0_dissociation.json",
             "profile": "aias_3_0_profile.csv", "inputs": "inputs_read_aias_3_0.json"}
MANIFEST_REL = "osf/aias_3_0/prereg/LOCK_MANIFEST_aias_3_0.sha256"
ANCHOR_REL = "osf/aias_3_0/anchor/git_anchor_aias_3_0.json"
DEVIATIONS_REL = "osf/aias_3_0/anchor/DEVIATIONS.md"
SQ_OUTPUT_PATHS = ["osf/methodology/v1_12/sensitivity/v112_verdicts_SQ.json",
                   "osf/methodology/v1_12/sensitivity/v119_verdicts_SQ.json"]


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git_blob_sha1(b: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def _git_ok(root: Path, *args) -> str:
    r = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def _git_show(root: Path, ref: str, path: str) -> bytes | None:
    r = subprocess.run(["git", "-C", str(root), "show", f"{ref}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class Reader:
    """Inputs read with `git show REF:PATH` (never the working tree), each logged with ref, commit, git blob and
    SHA-256 (MQ_Inputs). materialise() writes the bytes to a scratch directory so that v1.12's own readers
    (read_jsonl, read_coded, read_t4_coded, read_csv_rows, load_probes) are used unchanged."""

    def __init__(self, root: Path = ROOT, scratch: Path | None = None):
        import tempfile
        self.root, self.log = Path(root), {}
        self.scratch = Path(scratch) if scratch else Path(tempfile.mkdtemp(prefix="aias30_inputs_"))

    def commit(self, ref: str) -> str:
        return _git_ok(self.root, "rev-parse", "-q", "--verify", f"{ref}^{{commit}}")

    def exists(self, ref: str, path: str) -> bool:
        return bool(_git_ok(self.root, "rev-parse", "-q", "--verify", f"{ref}:{path}"))

    def read(self, ref: str, path: str) -> bytes:
        b = _git_show(self.root, ref, path)
        if b is None:
            raise Halt(f"MQ_Inputs: cannot read {ref}:{path}")
        self.log[f"{ref}:{path}"] = {"ref": ref, "commit": self.commit(ref), "path": path,
                                     "git_blob": git_blob_sha1(b), "sha256": sha256_bytes(b), "bytes": len(b)}
        return b

    def materialise(self, ref: str, path: str, sub: str) -> Path:
        dest = self.scratch / sub / Path(path).name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(self.read(ref, path))
        return dest

    def materialise_dir(self, ref: str, dirpath: str, names, sub: str) -> Path:
        for n in names:
            if self.exists(ref, f"{dirpath}/{n}"):
                self.materialise(ref, f"{dirpath}/{n}", sub)
        (self.scratch / sub).mkdir(parents=True, exist_ok=True)
        return self.scratch / sub

    def json(self, ref: str, path: str):
        return json.loads(self.read(ref, path).decode("utf-8"))

    def rows(self, ref: str, path: str) -> list[dict]:
        return list(csv.DictReader(io.StringIO(self.read(ref, path).decode("utf-8"))))


def check_scorer(root: Path = ROOT, pins: dict = PINS) -> dict:
    """MQ_Inputs: the imported v1.12 scorer is byte-identical to the file of v1.12's lock manifest and to the scored
    commit's file (section 2: "imported unchanged and blob-checked")."""
    p = pins["v1.12"]
    disk = Path(A.__file__).read_bytes()
    man = _git_show(root, p["lock_tag"], p["manifest"])
    listed = [ln.split()[0] for ln in (man or b"").decode("utf-8").splitlines() if ln.strip().endswith(p["scorer"])]
    at_ref = _git_ok(root, "rev-parse", "-q", "--verify", f"{p['ref']}:{p['scorer']}")
    rec = {"imported": str(A.__file__), "git_blob": git_blob_sha1(disk), "sha256": sha256_bytes(disk),
           "manifest_sha256": listed, "blob_at_scored_commit": at_ref, "pinned_blob": p["scorer_blob"]}
    rec["passed"] = (rec["git_blob"] == p["scorer_blob"] == at_ref and listed == [rec["sha256"]] == [p["scorer_sha256"]])
    return rec


def world_from_rows(rows: list[dict]) -> dict:
    """The three scores and the columns section 3 names, from v112_unit_table.csv rows (N1)."""
    num = A._num
    units = [(r["substrate"], r["brand"]) for r in rows]
    w = {"units": units, "P": {}, "C": {}, "Cov": {}, "mentions": {}, "cov_C3": {}, "cov_mid": {}, "P_t3_legacy": {},
         "rated_flag": {}}
    for r, u in zip(rows, units):
        w["P"][u] = num(r.get("P_comparator"))
        w["C"][u] = num(r.get("C_star_comparator"))
        rated = str(r.get("rated", "")).strip() == "1"
        w["rated_flag"][u] = rated
        w["Cov"][u] = num(r.get("cov_star")) if rated else None
        m = num(r.get("t4_mentions_N3_S0"))
        w["mentions"][u] = int(m) if m is not None else None
        w["cov_C3"][u] = num(r.get("cov_star_C3"))
        w["cov_mid"][u] = num(r.get("cov_star_mid_S8"))
        w["P_t3_legacy"][u] = num(r.get("P_t3_legacy"))
    return w


def v112_tables(raw: list, mentions: list, probes: list, registry: dict, panel=None) -> dict:
    """N2: v1.12's analysis set and beta tables (Rasch-type null) on the 14 CEPs and on each half, for one panel."""
    panel = panel or N3
    design = A.probe_design(probes)
    An = A.build_analysis(A.dedupe_calls(raw), mentions, design)
    brands = {s: list(registry[s]) for s in A.CATS if s in registry}
    return {"full": A.coverage_table(An["cep"], brands, design["ceps"], panel),
            "A": A.coverage_table(An["cep"], brands, design["half"]["A"], panel),
            "B": A.coverage_table(An["cep"], brands, design["half"]["B"], panel)}


# =========================================================================== 11.2 checks
def _same(a, b, tol=PARITY_TOL) -> bool:
    if a is None or b is None:
        return a is None and b is None
    return abs(float(a) - float(b)) <= tol


def mq_parity(world: dict, comp: dict, tabs: dict, v112_doc: dict | None) -> dict:
    """MQ_Parity (section 3): P and C* recomputed (score_v1_12.comparators_t4 on v0.42's files) equal the unit table;
    Cov* and its rated flag recomputed (v1.12's coverage table) equal the unit table; rho_w(Cov*, P) and rho_w(Cov*,
    C*) on v1.12's own unit sets equal its H1 and H2 within 1e-9. Any difference halts."""
    bad = collections.defaultdict(list)
    for u in world["units"]:
        if not _same(world["P"].get(u), comp["P"].get(u)):
            bad["P"].append([list(u), world["P"].get(u), comp["P"].get(u)])
        if not _same(world["C"].get(u), comp["C"].get(u)):
            bad["C_star"].append([list(u), world["C"].get(u), comp["C"].get(u)])
        r = A.cov_star(tabs["full"], u[0], u[1], N3)
        if bool(r["rated"]) != bool(world["rated_flag"].get(u)) or not _same(world["Cov"].get(u), r["cov_star"]):
            bad["Cov_star"].append([list(u), world["Cov"].get(u), r["cov_star"], world["rated_flag"].get(u), r["rated"]])
        if world["mentions"].get(u) != comp["t4_mentions"].get(u):
            bad["t4_mentions_N3_S0"].append([list(u), world["mentions"].get(u), comp["t4_mentions"].get(u)])
    rho = {}
    h2_units = None
    if v112_doc is not None:
        for leg, other in (("H1_Sep_Presence", "P"), ("H2_Sep_Consistency", "C")):
            keys, x, y, g, info = A.paired(world["Cov"], world[other])
            r = A.rho_w(x, y, g) if info["n"] >= 3 else NAN
            pub = v112_doc["legs"][leg]["rho_w"]
            rho[leg] = {"recomputed": r, "v1_12": pub, "n": info["n"], "v1_12_n": v112_doc["legs"][leg]["n"],
                        "equal": bool(_f(r) and abs(r - pub) <= PARITY_TOL and info["n"] == v112_doc["legs"][leg]["n"])}
            if not rho[leg]["equal"]:
                bad[leg].append(rho[leg])
            if leg == "H2_Sep_Consistency":
                h2_units = {"units": [list(k) for k in keys], "rho_w": pub,
                            "verdict": v112_doc["legs"][leg]["verdict"]}
    rec = {"check": "MQ_Parity (section 3)", "units": len(world["units"]),
           "rated_112": sum(1 for v in world["Cov"].values() if _f(v)), "rho": rho,
           "mismatches": {k: v[:10] for k, v in bad.items()}, "n_mismatches": {k: len(v) for k, v in bad.items()},
           "passed": not bad}
    rec["carried_h2"] = h2_units
    return rec


def mq_join(world: dict, registry_units, P_t3: dict, expected: int = 112) -> dict:
    """MQ_Join: the unit table carries the 112 unit keys 1:1 (= v1.12's registry); the AIAS 2.0 profile joins."""
    units = world["units"]
    dup = [u for u, n in collections.Counter(units).items() if n > 1]
    reg = set(map(tuple, registry_units))
    rec = {"units": len(units), "unique": len(set(units)), "duplicates": [list(u) for u in dup],
           "not_in_registry": [list(u) for u in set(units) - reg], "registry_not_in_table": [list(u) for u in reg - set(units)],
           "profile_t3_missing": [list(u) for u in units if u not in P_t3]}
    rec["passed"] = (len(units) == expected and not dup and not rec["not_in_registry"]
                     and not rec["registry_not_in_table"] and not rec["profile_t3_missing"])
    return rec


def legacy_t3(rows: list[dict]) -> tuple[dict, dict]:
    """= score_v1_12.legacy_t3: AIAS 2.0's published t3 P, and C* where rated."""
    return A.legacy_t3(rows)


def manifest_entries(text: str) -> list[tuple[str, str]]:
    return [tuple(line.split("  ", 1)) for line in text.splitlines() if line.strip()]


def verify_manifest(root: Path = ROOT, tag: str = PREREG_TAG) -> list[str]:
    """Every file of the lock manifest is unchanged on disk and at the tag; anchor/DEVIATIONS.md may only grow (its
    locked bytes stay an unchanged prefix; section 11.2 MQ_Lock)."""
    p = root / MANIFEST_REL
    if not p.exists():
        return [f"lock manifest missing: {MANIFEST_REL}"]
    text = p.read_text(encoding="utf-8")
    bad = []
    at_tag = _git_show(root, tag, MANIFEST_REL)
    if at_tag is None or at_tag.decode("utf-8") != text:
        bad.append(f"lock manifest differs from the one at tag {tag}")
    for h, f in manifest_entries(text):
        locked = _git_show(root, tag, f)
        if locked is None or sha256_bytes(locked) != h:
            bad.append(f"differs from the manifest at tag {tag}: {f}")
        q = root / f
        if not q.exists():
            bad.append(f"missing on disk: {f}")
            continue
        cur = q.read_bytes()
        if sha256_bytes(cur) == h:
            continue
        if f == DEVIATIONS_REL and locked is not None and sha256_bytes(locked) == h and cur.startswith(locked):
            continue
        bad.append(f"changed since the lock: {f}")
    return bad


def mq_lock(root: Path = ROOT, tag: str = PREREG_TAG) -> dict:
    """MQ_Lock: the tag and the anchor exist, the tag is the locked commit, the anchor names it, its file hashes equal
    the manifest's, and every manifest file is unchanged."""
    why = []
    commit = _git_ok(root, "rev-parse", "-q", "--verify", f"refs/tags/{tag}^{{commit}}")
    if not commit:
        why.append(f"git tag {tag} does not exist")
    elif commit != PREREG_COMMIT:
        why.append(f"tag {tag} is commit {commit}, locked {PREREG_COMMIT}")
    ap = root / ANCHOR_REL
    if not ap.exists():
        why.append(f"anchor file {ANCHOR_REL} does not exist")
    else:
        a = json.loads(ap.read_text(encoding="utf-8"))
        if a.get("tag") != tag or a.get("commit") != PREREG_COMMIT:
            why.append("the anchor does not name the tag and its commit")
        mp = root / MANIFEST_REL
        man = dict((f, h) for h, f in manifest_entries(mp.read_text(encoding="utf-8"))) if mp.exists() else {}
        for e in a.get("files", []):
            if "sha256" in e and man.get(e["path"]) != e["sha256"]:
                why.append(f"anchor SHA-256 of {e['path']} differs from the manifest")
    why += verify_manifest(root, tag)
    return {"check": "MQ_Lock", "ok": not why, "why": why, "tag": tag, "commit": commit or None}


def tag_date(root: Path, tag: str = PREREG_TAG) -> str:
    return _git_ok(root, "for-each-ref", "--format=%(taggerdate:iso-strict)", f"refs/tags/{tag}")


def mq_blind(root: Path = ROOT, tag: str = PREREG_TAG, paths=None) -> dict:
    """MQ_Blind: the tag's date precedes the first commit (on any ref) of every release output and every S-Q output;
    otherwise the affected statistics are labelled exploratory and a DEVIATIONS entry is due (no halt)."""
    paths = paths or ([f"{OUT_REL}/{n}" for n in OUT_NAMES.values()] + SQ_OUTPUT_PATHS)
    td = tag_date(root, tag)
    if not td:
        raise Halt(f"MQ_Lock: tag {tag} not found")
    t0 = datetime.fromisoformat(td)
    early = []
    for p in paths:
        for line in _git_ok(root, "log", "--all", "--diff-filter=A", "--format=%H %cI", "--", p).splitlines():
            h, d = line.split(" ", 1)
            if datetime.fromisoformat(d) <= t0:
                early.append({"path": p, "commit": h, "date": d})
    return {"check": "MQ_Blind", "ok": not early, "tag_date": td, "early": early,
            "label": None if not early else "exploratory (MQ_Blind): a DEVIATIONS entry records it and Pablo is told"}


def mq_sq(record: dict | None) -> dict:
    """MQ_SQ (section 10.2 step 5): the S-Q wrapper reproduced v1.12 and v1.19 with 0 differences before writing."""
    if record is None:
        return {"check": "MQ_SQ", "ok": False, "why": "the S-Q wrapper's record does not exist"}
    rep = record.get("reproduction") or {}
    keys = ("coded_cells_differ", "v112_verdict_leaves_differ", "v112_unit_table_cells_differ",
            "v119_verdict_leaves_differ")
    ok = all(rep.get(k) == 0 for k in keys)
    return {"check": "MQ_SQ", "ok": ok, "reproduction": {k: rep.get(k) for k in keys}}


# =========================================================================== loading the two worlds (primary, S-Q)
def load_world(rd: Reader, coding: str = "primary", sq_ref: str | None = None, pins: dict = PINS) -> dict:
    """Primary: v1.12 at 949be61 with t4's primary tables (v0.42, 31c64c6). S-Q: the S-Q wrapper's unit table and
    mentions (at sq_ref) with t4's S-Q tables (v0.45, 47f1748), both sides together (section 10.2 step 2)."""
    v112, v042, q45, sq = pins["v1.12"], pins["v0.42"], pins["v0.45_SQ"], pins["sq"]
    tag = coding
    raw = A.read_jsonl(rd.materialise(v112["ref"], v112["raw"], f"{tag}/v112"))
    probes = A.load_probes(rd.materialise(v112["ref"], v112["probes"], f"{tag}/v112"))
    t4_raw = A.read_jsonl(rd.materialise(v042["ref"], v042["raw"], f"{tag}/v042"))
    excl, _window = A.t4_excluded(t4_raw)
    if coding == "primary":
        rows = rd.rows(v112["ref"], v112["unit_table"])
        coded = rd.materialise_dir(v112["ref"], v112["coded_dir"], V112_CODED_FILES, f"{tag}/v112_coded")
        bt_ref, bt_path, cd_ref, cd_dir = v042["ref"], v042["brand_table"], v042["ref"], v042["coded_dir"]
        v112_doc = rd.json(v112["ref"], v112["verdicts"])
    else:
        if not sq_ref:
            raise Refused("S-Q inputs: --sq-ref is required (section 11.3: primary and S-Q in the same run)")
        rows = rd.rows(sq_ref, sq["unit_table"])
        coded = rd.materialise_dir(sq_ref, sq["coded_dir"], V112_CODED_FILES, f"{tag}/v112_coded")
        bt_ref, bt_path, cd_ref, cd_dir = q45["ref"], q45["brand_table"], q45["ref"], q45["coded_dir"]
        b = rd.read(bt_ref, bt_path)
        if sha256_bytes(b) != q45["brand_table_sha256"]:
            raise Halt(f"MQ_Inputs: {bt_path} at {bt_ref} has SHA-256 {sha256_bytes(b)}, pinned {q45['brand_table_sha256']}")
        v112_doc = rd.json(sq_ref, SQ_OUTPUT_PATHS[0])
    mentions, registry = A.read_coded(coded)
    bt = A.read_csv_rows(rd.materialise(bt_ref, bt_path, f"{tag}/t4"))
    ca, cb = A.read_t4_coded(rd.materialise_dir(cd_ref, cd_dir, T4_CODED_FILES, f"{tag}/t4_coded"))
    comp = A.comparators_t4(bt, ca, cb, excl)
    world = world_from_rows(rows)
    world["tabs"] = v112_tables(raw, mentions, probes, registry)
    world["coding"] = coding
    reg_units = [(s, b) for s in registry for b in registry[s]]
    return {"world": world, "comp": comp, "v112_doc": v112_doc, "registry_units": reg_units}


def load_legacy(rd: Reader, pins: dict = PINS) -> tuple[dict, dict, dict]:
    p = pins["aias_2_0"]
    if rd.commit(p["ref"]) != p["commit"]:
        raise Halt(f"MQ_Inputs: {p['ref']} is not commit {p['commit']}")
    b = rd.read(p["ref"], p["path"])
    if sha256_bytes(b) != p["sha256"]:
        raise Halt(f"MQ_Inputs: {p['path']} SHA-256 differs from the pin")
    P_t3, C_t3 = legacy_t3(list(csv.DictReader(io.StringIO(b.decode("utf-8")))))
    return P_t3, C_t3, {"ref": p["ref"], "commit": p["commit"], "sha256": p["sha256"]}


def legacy_check(world: dict, P_t3: dict) -> dict:
    bad = [[list(u), world["P_t3_legacy"].get(u), P_t3.get(u)] for u in world["units"]
           if not _same(world["P_t3_legacy"].get(u), P_t3.get(u), 1e-5)]
    return {"check": "P_t3_legacy (unit table) = AIAS 2.0 t3 P (profiles)", "mismatches": bad[:10], "passed": not bad}


def read_preview(rd: Reader | None, ref: str | None, pins: dict = PINS) -> dict:
    """Section 5.4: the Preview's locked Coverage tests as issued, if they exist at the data lock."""
    path = pins["preview"]["results"]
    if not ref or rd is None or not rd.exists(ref, path):
        return {"status": "not issued", "G3": None}
    doc = rd.json(ref, path)
    st = doc.get("structure") or {}
    s = st.get("S_tests") or {}
    return {"status": "issued", "ref": ref, "commit": rd.commit(ref), "G3": (st.get("status") or {}).get("Cov"),
            "K": doc.get("K"), "H_PC_N3": st.get("H_PC_N3"), "S_tests": {k: s.get(k) for k in s if "Cov" in k},
            "I_test_Cov": (st.get("I_tests") or {}).get("Cov"), "H_PC_N3_rho": (s.get("PxC") or {}).get("rho")}


# =========================================================================== the two analyses on one world
def c_star_k1(world: dict, preview: dict, n_perm: int) -> dict:
    """C*'s own K1, printed beside K1_3 (N5): the Preview's H_PC_N3 where it exists, else D_PC_U3 (descriptive)."""
    if preview.get("H_PC_N3"):
        return {"source": "Preview H_PC_N3 (carried)", "verdict": preview["H_PC_N3"], "rho": preview.get("H_PC_N3_rho")}
    U3 = u3_units(world["P"], world["C"], world["Cov"])
    r = pair_row(_on(world["P"], U3), _on(world["C"], U3), SEEDS["D_PC_U3"], n_perm)
    return {"source": "D_PC_U3 (recomputed here, descriptive)", "rho": r["rho_w"], "n": r["n"],
            "passes_K1_line_0_50": bool(_f(r["rho_w"]) and abs(r["rho_w"]) <= K1_MAX)}


def cal_sensitivities(world: dict) -> dict:
    """The calibration's constraints under SA, S-COI and SC (N9)."""
    out = {name: {"excluded": [list(u) for u in ex], "calibration": _cal_short(calibration(_world_without(world, ex)))}
           for name, ex in (("SA", [DENON]), ("S-COI", list(COI_UNITS)))}
    cats = sorted({u[0] for u in world["units"]})
    out["SC"] = {f"without {c}": {"calibration": _cal_short(calibration(_world_without(world, cats=[x for x in cats
                                                                                                  if x != c])))}
                 for c in cats}
    return out


def calibration_doc(world: dict, preview: dict, n_perm: int, n_boot: int) -> dict:
    cal = calibration(world, n_boot, c_star_k1(world, preview, n_perm))
    cal["sensitivities"] = cal_sensitivities(world)
    cal["verdict_changes_under_sensitivities"] = verdict_changes({"composite": cal["composite"]["verdict"]},
                                                                 cal["sensitivities"])
    return cal


def dissociation_doc(world: dict, carried_h2: dict | None, preview: dict, legacy: tuple | None, n_perm: int,
                     n_boot: int) -> dict:
    P, C, cov = world["P"], world["C"], world["Cov"]
    d = dissociation(P, C, cov, n_perm, SEEDS, carried_h2=carried_h2)
    d["bootstrap"] = dissociation_bootstrap(P, C, cov, n_boot)
    d["sensitivities"] = sensitivities(world, n_perm, with_calibration=False)
    d["verdict_changes_under_sensitivities"] = verdict_changes(d["verdicts"], d["sensitivities"])
    d["descriptives"] = {"D2_rated": d2_rated(world), "D4_joint_on_U3": d4_joint(world),
                         "D5": "the calibration table: outputs/aias_3_0_calibration.json (section 4.5)"}
    if legacy is not None:
        d["descriptives"]["D3_bridge"] = d3_bridge(P, C, legacy[0], legacy[1], n_boot)
    d["preview_beside"] = preview
    d["class"] = wording_class(d["verdicts"]["H3_Cov_Joint"], preview.get("G3"))
    d["DIS"] = {"DIS_JOINT": d["joint"]["R_adj"], "DIS_N": d["joint"]["n"], "DIS_RHO_P_COV": d["pairs"]["P_Cov"]["rho_w"],
                "DIS_RHO_C_COV": d["pairs"]["C_Cov"]["rho_w"], "DIS_VERDICT": d["verdicts"]["H3_Cov_Joint"]}
    return d


def compare_sq(primary: dict, sq: dict, tests) -> dict:
    """W5 / section 10.2 step 7: beside each statistic the S-Q value, its label and whether the label is the same."""
    rows = []
    for t, (pv, qv, ps, qs) in tests.items():
        rows.append({"test": t, "primary": {"statistic": ps, "verdict": pv}, "SQ": {"statistic": qs, "verdict": qv},
                     "same_label": pv == qv, "flag": "" if pv == qv else "coding-sensitive"})
    return {"sensitivity": "S-Q (U+2019/U+2018 -> U+0027 before coding; section 10.2)", "tests": rows,
            "all_labels_same": all(r["same_label"] for r in rows),
            "rule": "S-Q never replaces a primary verdict, never changes the class, never re-opens v1.12's GATE"}


# =========================================================================== outputs
def _jsonable(o):
    if isinstance(o, dict):
        return {("|".join(map(str, k)) if isinstance(k, tuple) else str(k)): _jsonable(v) for k, v in o.items()}
    if isinstance(o, (set, frozenset)):
        return [_jsonable(v) for v in sorted(o)]
    if isinstance(o, (list, tuple)):
        return [_jsonable(v) for v in o]
    if isinstance(o, (bool, np.bool_)):
        return bool(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, (float, np.floating)):
        return float(o) if math.isfinite(float(o)) else None
    return o


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_jsonable(obj), indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")


def write_profile(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["substrate", "brand"])
        w.writeheader()
        w.writerows(rows)


def _guard_outputs(out_dir: Path, mode: str) -> None:
    targets = [out_dir / OUT_NAMES[mode]] + ([out_dir / OUT_NAMES["profile"]] if mode == "dissociation" else [])
    for t in targets:
        if t.exists():
            raise Refused(f"{t} exists: each run is made once and never overwrites its output (section 11.3)")
    ip = out_dir / OUT_NAMES["inputs"]
    if ip.exists() and mode in json.loads(ip.read_text(encoding="utf-8")):
        raise Refused(f"{ip} already records a {mode} run (N13)")


def _record_inputs(out_dir: Path, mode: str, rec: dict) -> None:
    ip = out_dir / OUT_NAMES["inputs"]
    doc = json.loads(ip.read_text(encoding="utf-8")) if ip.exists() else {"phase": PHASE_ID, "prereg_tag": PREREG_TAG}
    doc[mode] = rec
    write_json(ip, doc)


def run(mode: str, root: Path = ROOT, sq_ref: str | None = None, preview_ref: str | None = None,
        out_dir: Path | None = None, n_perm: int = N_PERM, n_boot: int = N_BOOT, log=print) -> dict:
    """--calibration or --dissociation on program data (section 11.3). Refuses without MQ_Lock, without the S-Q
    outputs (MQ_SQ), or when its output exists; halts on MQ_Inputs, MQ_Join or MQ_Parity."""
    if mode not in ("calibration", "dissociation"):
        raise ValueError(mode)
    root = Path(root)
    out_dir = Path(out_dir) if out_dir else root / OUT_REL
    lock = mq_lock(root)
    if not lock["ok"]:
        raise Refused("MQ_Lock: " + "; ".join(lock["why"]))
    sc = check_scorer(root)
    if not sc["passed"]:
        raise Halt(f"MQ_Inputs: the imported v1.12 scorer is not the locked file: {sc}")
    _guard_outputs(out_dir, mode)
    rd = Reader(root)
    sq_rec = rd.json(sq_ref, PINS["sq"]["record"]) if (sq_ref and rd.exists(sq_ref, PINS["sq"]["record"])) else None
    msq = mq_sq(sq_rec)
    if not msq["ok"]:
        raise Refused(f"MQ_SQ: {msq} (section 10.2: the S-Q wrapper runs first and must reproduce the published files)")
    blind = mq_blind(root)
    preview = read_preview(rd, preview_ref)
    P_t3, C_t3, leg_rec = load_legacy(rd)
    worlds, checks = {}, {}
    for coding in ("primary", "SQ"):
        L = load_world(rd, coding, sq_ref)
        par = mq_parity(L["world"], L["comp"], L["world"]["tabs"], L["v112_doc"])
        if not par["passed"]:
            raise Halt(f"MQ_Parity ({coding}): {json.dumps(_jsonable(par['mismatches']))[:2000]}")
        join = mq_join(L["world"], L["registry_units"], P_t3)
        if not join["passed"]:
            raise Halt(f"MQ_Join ({coding}): {json.dumps(_jsonable(join))[:2000]}")
        worlds[coding] = L
        checks[coding] = {"MQ_Parity": {k: v for k, v in par.items() if k != "carried_h2"}, "MQ_Join": join,
                          "legacy": legacy_check(L["world"], P_t3)}
    head = {"phase": PHASE_ID, "prereg": "osf/aias_3_0/prereg/PRE_REGISTRATION_aias_3_0.md", "prereg_tag": PREREG_TAG,
            "created_utc": _now(), "run": mode, "MQ_Lock": lock, "MQ_Inputs_scorer": sc, "MQ_SQ": msq, "MQ_Blind": blind,
            "checks": checks, "seeds": {"tests": SEEDS, "sensitivities": SENS_SEEDS},
            "draws": {"permutation": n_perm, "bootstrap": n_boot}, "label": blind["label"] or "confirmatory as registered"}
    if mode == "calibration":
        res = {c: calibration_doc(worlds[c]["world"], preview, n_perm, n_boot) for c in ("primary", "SQ")}
        tests = {"composite": (res["primary"]["composite"]["verdict"], res["SQ"]["composite"]["verdict"],
                               res["primary"]["composite"]["selected"], res["SQ"]["composite"]["selected"])}
        doc = dict(head, primary=res["primary"], SQ=res["SQ"], SQ_comparison=compare_sq(res["primary"], res["SQ"], tests))
        write_json(out_dir / OUT_NAMES["calibration"], doc)
        log(f"[aias3] calibration: {res['primary']['composite']['verdict']} (S-Q {res['SQ']['composite']['verdict']})"
            f" -> {out_dir / OUT_NAMES['calibration']}")
    else:
        prim_par = mq_parity(worlds["primary"]["world"], worlds["primary"]["comp"], worlds["primary"]["world"]["tabs"],
                             worlds["primary"]["v112_doc"])
        sq_par = mq_parity(worlds["SQ"]["world"], worlds["SQ"]["comp"], worlds["SQ"]["world"]["tabs"],
                           worlds["SQ"]["v112_doc"])
        res = {"primary": dissociation_doc(worlds["primary"]["world"], prim_par["carried_h2"], preview, (P_t3, C_t3),
                                           n_perm, n_boot),
               "SQ": dissociation_doc(worlds["SQ"]["world"], sq_par["carried_h2"], preview, (P_t3, C_t3), n_perm, n_boot)}
        tests = {}
        for t, key in (("H3_Cov_Joint", ("joint", "R_adj")), ("H3_Cov_P_U3", ("pairs", "P_Cov")),
                       ("H3_Cov_C_U3", ("pairs", "C_Cov"))):
            stat = (lambda r: r["joint"]["R_adj"]) if t == "H3_Cov_Joint" else (lambda r, k=key[1]: r["pairs"][k]["rho_w"])
            tests[t] = (res["primary"]["verdicts"][t], res["SQ"]["verdicts"][t], stat(res["primary"]), stat(res["SQ"]))
        doc = dict(head, primary=res["primary"], SQ=res["SQ"], SQ_comparison=compare_sq(res["primary"], res["SQ"], tests),
                   CLASS=res["primary"]["class"], legacy=leg_rec)
        write_json(out_dir / OUT_NAMES["dissociation"], doc)
        write_profile(out_dir / OUT_NAMES["profile"], profile_rows(worlds["primary"]["world"]))
        log(f"[aias3] H3_Cov_Joint {res['primary']['verdicts']['H3_Cov_Joint']} (R_adj "
            f"{res['primary']['joint']['R_adj']}); class {res['primary']['class']['class']} -> {out_dir}")
    _record_inputs(out_dir, mode, {"created_utc": _now(), "sq_ref": sq_ref, "preview_ref": preview_ref,
                                   "inputs_read": rd.log, "scorer_sha256": sha256_bytes(Path(__file__).read_bytes())})
    return doc


def pin_report(root: Path = ROOT, pins: dict = PINS) -> dict:
    """Every pinned ref and file exists (git rev-parse only; no file content is read beyond hashing two pinned files)."""
    out, probs = {}, []
    for name, p in pins.items():
        ref = p.get("ref") or p.get("lock_tag")
        if not ref:
            continue
        c = _git_ok(root, "rev-parse", "-q", "--verify", f"{ref}^{{commit}}")
        r = {"ref": ref, "commit": c or None}
        if not c:
            probs.append(f"{name}: {ref} not found")
        for k, v in p.items():
            if isinstance(v, str) and "/" in v and k not in ("manifest",) and not k.endswith("dir"):
                ok = bool(_git_ok(root, "rev-parse", "-q", "--verify", f"{ref}:{v}"))
                r[k] = ok
                if not ok and name not in ("preview",):
                    probs.append(f"{name}: {ref}:{v} absent")
        out[name] = r
    if pins["aias_2_0"].get("commit") and out["aias_2_0"]["commit"] != pins["aias_2_0"]["commit"]:
        probs.append("aias_2_0: data-locked tag moved")
    b = _git_show(root, pins["v0.45_SQ"]["ref"], pins["v0.45_SQ"]["brand_table"])
    if b is None or sha256_bytes(b) != pins["v0.45_SQ"]["brand_table_sha256"]:
        probs.append("v0.45_SQ: brand table SHA-256 differs from the pin")
    out["scorer"] = check_scorer(root, pins)
    if not out["scorer"]["passed"]:
        probs.append("v1.12 scorer blob/SHA-256 check failed")
    out["problems"] = probs
    return out


# =========================================================================== synthetic data (tests and --dry-run only)
SIZES = {"v0.19": 16, "v0.20": 24, "v0.21": 24, "v0.22": 24, "v0.23": 24}   # 112 units


def synthetic_world(seed: int = 330999, overlap: float = 0.0, n_ceps: int = 14) -> dict:
    """A synthetic world with the shapes of section 3 (NOT program data): answers of 3 models x 3 runs to 14 situations
    (halves of 7) per category, Coverage tables built by v1.12's functions, Cov* rated by v1.12's rule; P, C* and the
    t4 mention counts drawn so that P follows the naming rate; `overlap` adds Cov*'s centred value to P and C*."""
    rng = np.random.default_rng(seed)
    ans, brands, ceps, halves = {}, {}, {}, {"A": {}, "B": {}}
    lat = {}
    for sub, nb in SIZES.items():
        bs = [f"{sub}-b{i:02d}" for i in range(nb)]
        brands[sub] = bs
        cp = [f"{sub}-cep{j:02d}" for j in range(n_ceps)]
        ceps[sub], halves["A"][sub], halves["B"][sub] = cp, cp[: n_ceps // 2], cp[n_ceps // 2:]
        rate = rng.beta(0.6, 3.0, nb)
        spread = rng.uniform(0.0, 1.0, nb)                                 # situation breadth (Coverage's signal)
        prof = rng.dirichlet(np.ones(n_ceps) * 0.5, nb)
        for i, b in enumerate(bs):
            lat[(sub, b)] = rate[i]
        for m in N3:
            for j, p in enumerate(cp):
                for r in A.RUNS:
                    q = rate * (spread + (1 - spread) * prof[:, j] * n_ceps)
                    named = [b for b, x in zip(bs, np.clip(q, 0, 0.95)) if rng.random() < x]
                    ans[(sub, m, p, r)] = frozenset(named)
    tabs = {"full": A.coverage_table(ans, brands, ceps, N3), "A": A.coverage_table(ans, brands, halves["A"], N3),
            "B": A.coverage_table(ans, brands, halves["B"], N3)}
    units = [(s, b) for s in SIZES for b in brands[s]]
    cov = {u: A.cov_star(tabs["full"], u[0], u[1], N3)["cov_star"] for u in units}
    w = {"units": units, "tabs": tabs, "Cov": cov, "P": {}, "C": {}, "mentions": {}, "rated_flag": {},
         "cov_C3": {}, "cov_mid": {}, "P_t3_legacy": {}, "coding": "synthetic"}
    for u in units:
        c = cov[u]
        shift = overlap * (c - 50.0) if _f(c) else 0.0
        p = 100.0 * lat[u] ** 0.5 * 0.8 + rng.normal(0, 6) + shift
        w["P"][u] = float(np.clip(p, 0, 100))
        k = int(rng.binomial(54, min(lat[u], 1.0)))
        w["mentions"][u] = k
        w["C"][u] = float(np.clip(rng.normal(80, 10) + shift, 0, 100)) if k >= 6 else None
        w["rated_flag"][u] = _f(c)
        w["cov_mid"][u] = A.cov_star(tabs["full"], u[0], u[1], N3, key="beta_mid")["cov_star"]
        w["cov_C3"][u] = (c + rng.normal(0, 4)) if _f(c) else None
        w["P_t3_legacy"][u] = float(np.clip(w["P"][u] + rng.normal(0, 8), 0, 100))
    return w


def dry_run(out_dir: Path, n_perm: int = 500, n_boot: int = 200, seed: int = 330999, log=print) -> dict:
    """Both analyses on a synthetic world (primary) and a perturbed copy standing in for S-Q; never program data."""
    out_dir = Path(out_dir)
    prim = synthetic_world(seed)
    sq = synthetic_world(seed + 1)
    legacy = (prim["P_t3_legacy"], {u: (v + 3 if _f(v) else None) for u, v in prim["C"].items()})
    preview = {"status": "not issued", "G3": None}
    cal = {c: calibration_doc(w, preview, n_perm, n_boot) for c, w in (("primary", prim), ("SQ", sq))}
    dis = {c: dissociation_doc(w, None, preview, legacy, n_perm, n_boot) for c, w in (("primary", prim), ("SQ", sq))}
    head = {"phase": PHASE_ID, "DRY_RUN": f"synthetic data (seed {seed}); not program data", "draws":
            {"permutation": n_perm, "bootstrap": n_boot}}
    write_json(out_dir / OUT_NAMES["calibration"], dict(head, **cal))
    write_json(out_dir / OUT_NAMES["dissociation"], dict(head, **dis, CLASS=dis["primary"]["class"]))
    write_profile(out_dir / OUT_NAMES["profile"], profile_rows(prim))
    log(f"[dry run] composite {cal['primary']['composite']['verdict']}; H3_Cov_Joint "
        f"{dis['primary']['verdicts']['H3_Cov_Joint']} (R_adj {dis['primary']['joint']['R_adj']:.3f}, n "
        f"{dis['primary']['joint']['n']}); class {dis['primary']['class']['class']} -> {out_dir}")
    return {"calibration": cal, "dissociation": dis}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="AIAS 3.0 release scorer (calibration, dissociation; section 11.3)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--calibration", action="store_true")
    g.add_argument("--dissociation", action="store_true")
    g.add_argument("--verify-lock", action="store_true")
    g.add_argument("--pin-report", action="store_true")
    g.add_argument("--dry-run", metavar="DIR")
    ap.add_argument("--sq-ref", help="git ref holding the S-Q wrapper's committed outputs")
    ap.add_argument("--preview-ref", help="git ref holding the Preview's results file (section 5.4), if it exists")
    ap.add_argument("--out", help="output directory (default osf/aias_3_0/outputs)")
    ap.add_argument("--draws", type=int, default=None, help="permutation/bootstrap draws (dry run and tests only)")
    a = ap.parse_args(argv)
    try:
        if a.verify_lock:
            r = mq_lock(ROOT)
            print(json.dumps(r, indent=2))
            return 0 if r["ok"] else 2
        if a.pin_report:
            r = pin_report(ROOT)
            print(json.dumps(_jsonable(r), indent=2))
            return 0 if not r["problems"] else 2
        if a.dry_run:
            d = a.draws or 500
            dry_run(Path(a.dry_run), d, d)
            return 0
        if a.draws:
            raise Refused("--draws is for the dry run and tests only: the registered run uses 10,000 / 10,000")
        run("calibration" if a.calibration else "dissociation", ROOT, a.sq_ref, a.preview_ref,
            Path(a.out) if a.out else None)
        return 0
    except Refused as e:
        print(f"[aias3] REFUSED: {e}", file=sys.stderr)
        return 3
    except Halt as e:
        print(f"[aias3] HALT: {e}", file=sys.stderr)
        return 4


if __name__ == "__main__":
    sys.exit(main())
