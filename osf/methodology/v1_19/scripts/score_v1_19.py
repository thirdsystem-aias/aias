#!/usr/bin/env python3
"""
score_v1_19.py -- AIAS(TM) v1.19 Coverage Paper B, re-analysis studies #32, #34, #35, #36: scorer SKELETON
(pre-registration DRAFT r0, 2026-11-12). Not locked.

Transcribes PRE_REGISTRATION_v1_19_DRAFT_r0.md. THE PRE-REGISTRATION PROSE IS AUTHORITATIVE; where it is silent the
choice is listed in SCORER_NOTES. Paper A's definitions and code are IMPORTED, not forked: score_v1_12.py (tag
v1.12-prereg-r1) supplies the answer index, the probe design, beta / Cov* (coverage_table, cov_star_map), the
leave-b-out Rasch deltas (rasch_deltas), rho_w, paired, perm_p, below_n_floor, the floors and the n floor.

r0 status: the real-data path (load_real, run_real) is written and tested on synthetic files laid out as Paper A's
scorer writes them (tests/test_loader_v1_19.py); its test on Paper A's own --synthetic pipeline output is an r1 step.

Nothing here calls a model API. --run refuses unless (1) tag v1.19-prereg-r1 is on origin and anchor/osf_anchor_v1_19.json
names its commit, (2) Paper A's verdict file exists and its gate allows Paper B (section 1 of the pre-registration),
(3) Paper A's unit table reproduces under the imported code (parity gate B-P1), and (4) no v1.19 output exists yet
(one run only). --dry-run scores synthetic worlds only.

SCORER_NOTES (choices where the draft is silent; each to be settled or confirmed at r1)
 B1  Answer index, design, panel: exactly Paper A's (build_analysis on A's deduplicated raw record and coded mention
     rows; A's primary panel as recorded in v112_verdicts.json "primary_panel").
 B2  Split codes (#32): a 7-bit vector over W_TYPES in Paper A's order; bit i = 1 puts W_i's half-B CEP in part 1.
     Unordered complementary pairs = codes with bit 0 ("why") = 0: 64 splits; code 0 is Paper A's H4 split.
 B3  Half and part Cov*: Paper A's H4 rule (own leave-b-out delta on the part's 7 CEPs; floor 7; >= 2 models naming).
 B4  Cliff's delta (#34): v0.35's D1, pooled over within-category cross pairs only; permutation strata = category.
 B5  Rank residuals (#34 secondary): within-category OLS of centred ranks of Cov* on centred ranks of P, fitted over
     all analysable units (v0.35 D2). #36 residual arm: within-category OLS of each raw profile coordinate on P.
 B6  Expected W occupancy (#35 secondary, #36): the exact inclusion probability of a slot under the conditional
     Bernoulli null given n (pi_s = w_s e_{n-1}(w without s) / e_n(w), w_s = exp(delta^(-b)_j(s))), summed over W's
     answered slots; observed minus expected, pooled over the panel models with n >= 1, divided by their total n.
 B7  Clustering (#36): Ward linkage, Euclidean, on the raw excess profiles (not z-scored); gap statistic over k = 1..8
     with B = 500 uniform references over the bounding box (seed), Tibshirani 1-SE rule; silhouette by its definition;
     ARI by its definition (Hubert and Arabie). scipy only (no scikit-learn on the machine).
 B8  Presence tiers (#36 inheritance): v0.23's regime rule (score_v0_23.py lines 332-356, numpy percentile, linear)
     applied within category to Paper A's P comparator: >= q75 Dominant, >= q50 Established, >= q25 Emerging, else Absent.
 B9  Floors the draft does not state: H32_CueType is UNDETERMINED if fewer than half of its 84 reference values are
     finite; H34_Floor_BeyondPresence needs >= 20 units with P; H35_IL_Robust needs >= 45 units with P; units without P
     leave only the arms that need P.
 B10 Random streams: H36's full-profile gap references, silhouette null and ARI null share one generator (seed
     119362) in that order; the residual arm uses 119363. H32_SetSampling permutes each split independently from one
     generator (119321), splits in code order.
 B11 Sensitivities (section 8): each variant re-runs the studies it touches with the same seeds. Exclusions (S-COI,
     S-LOCO) drop units from every map after Cov* and the profiles are computed (the other brands' delta fits are not
     refitted), as Paper A's S10 does. S-Floor6 changes the full Cov* floor only (halves stay at 7). S-Equal uses delta
     = 0 for Cov* and the profiles. S-Mid uses Paper A's beta_mid. S-C3 runs only if the answers hold every C3 model.
     S-IL-t1: v0.37's IL-Direct (R_cult_total - R_cat_total, v1_7_cpc.csv), eligible iff 0 < mean_r / 6 < 1.
     H34_Defunct_Occupancy is one category's test and is not re-run by S-LOCO.
"""
import argparse
import collections
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
A_SCRIPTS = ROOT / "osf/methodology/v1_12/scripts"
sys.path.insert(0, str(A_SCRIPTS))
import score_v1_12 as A  # noqa: E402  (Paper A's locked scorer, imported unchanged)

PHASE_ID = "v1.19"
PREREG_TAG = "v1.19-prereg-r1"
A_PREREG_TAG = "v1.12-prereg-r1"
DESIGN_DIR = ROOT / "osf/methodology/v1_19"
OUT_DIR = DESIGN_DIR / "outputs"
ANCHOR = DESIGN_DIR / "anchor/osf_anchor_v1_19.json"
ROSTER = DESIGN_DIR / "prereg/phantom_roster_v1_19.csv"
A_VERDICTS = A.VERDICTS_PATH
A_UNIT_TABLE = A.UNIT_TABLE_PATH
A_MANIFEST = ROOT / "osf/methodology/v1_12/prereg/LOCK_MANIFEST_v1_12.sha256"

W = list(A.W_TYPES)
TRIO = ("v0.20", "v0.21", "v0.22")
SE_CUES = ("with whom", "how feeling")                    # #35 secondary (decision D6)
SEEDS = {"H32_SetSampling": 119321, "H32_CueType": 119322, "H34_Floor_Signature": 119341,
         "H34_Floor_BeyondPresence": 119342, "H34_Defunct_Occupancy": 119343, "H35_IL_Coverage": 119351,
         "H35_IL_Robust": 119352, "H35_IL_CueType": 119353, "H36_Profile_Replication": 119361,
         "H36_Structure": 119362, "H36_Gap": 119363, "dry_run": 119390}
N_PERM = 10_000
GAP_B, K_MAX = 500, 8
REL_CONF, REL_FALS, P10_MIN, MIN_SPLITS = 0.50, 0.30, 0.30, 32           # H32_SetSampling
CUE_CONF_MAX, CUE_FALS_MIN, CUE_PCT = 1, 3, 5                            # H32_CueType
DELTA_CONF, DELTA_FALS, PH_MIN = 0.30, 0.15, 10                         # H34 (v0.35 bands)
DEF_MIN, DEF_SHARE = 10, 0.40                                            # H34_Defunct_Occupancy
IL_CONF, IL_FALS, IL_NFLOOR = 0.30, 0.15, 45                              # H35 (v0.37 bands and n floor)
REP_CONF, REP_FALS = 0.20, 0.10                                           # H36 replication
SIL_MIN, SIL_PCT, ARI_MIN, ARI_P = 0.25, 95, 0.30, 0.01                  # H36 structure (v0.36 criteria)
ALPHA = 0.05
CAVEAT_WINDOW = 150                                                       # v0.38 D7
CAVEAT_TERMS = ("discontinued", "defunct", "no longer", "ceased", "phased out", "out of production", "shut down",
                "was retired", "folded", "used market", "used car", "pre-owned", "bankrupt")
NAN = float("nan")
GATE_RUN, GATE_DECISION = ("PASS",), ("MARGINAL",)
GATE_NOT_RUN = ("FAIL", "UNDETERMINED", "INSTRUMENT FAIL")


class Refused(RuntimeError):
    pass


def _f(v):
    return A._finite(v)


# =========================================================================== section 1: conditionality on Paper A
def paper_b_decision(a_doc, pablo_decision=None):
    """Section 1. PASS -> run. MARGINAL -> run only with Pablo's recorded decision ({'go': True, 'date', 'text'}).
    FAIL / UNDETERMINED / INSTRUMENT FAIL -> NOT RUN (reported as not run). Anything else -> refused."""
    v = ((a_doc or {}).get("paper_A_verdict") or {}).get("verdict")
    if v in GATE_RUN:
        return {"run": True, "status": "RUN", "a_verdict": v, "reason": "Paper A PASS"}
    if v in GATE_DECISION:
        d = pablo_decision or {}
        if d.get("go") is True and d.get("date") and d.get("text"):
            legs = (a_doc["paper_A_verdict"].get("legs") or {})
            return {"run": True, "status": "RUN (Paper A MARGINAL; Pablo's recorded decision)", "a_verdict": v,
                    "reason": "Paper A MARGINAL", "decision": d,
                    "marginal_legs": sorted(h for h, x in legs.items() if x == "MARGINAL")}
        return {"run": False, "status": "NOT RUN (pending Pablo's decision)", "a_verdict": v,
                "reason": "Paper A MARGINAL: Paper B runs only on Pablo's recorded decision (v1.12 section 3, rule 5)"}
    if v in GATE_NOT_RUN:
        return {"run": False, "status": "NOT RUN", "a_verdict": v,
                "reason": f"Paper A verdict {v}: no Paper B on this instrument (v1.12 section 3)"}
    raise Refused(f"Paper A verdict {v!r} is not one of the v1.12 gate verdicts")


def not_run_record(dec, a_sha):
    return {"phase": PHASE_ID, "prereg_tag": PREREG_TAG, "status": dec["status"], "paper_A_verdict": dec["a_verdict"],
            "reason": dec["reason"], "paper_A_verdict_file_sha256": a_sha, "statistics": None,
            "note": "No Paper B statistic was computed. Reported as not run (section 1)."}


# =========================================================================== shared helpers
def cov_map_for(ans, brands, ceps_by_sub, panel, floor, null="rasch", key="beta"):
    tab = A.coverage_table(ans, brands, ceps_by_sub, panel, null)
    return tab, A.cov_star_map(tab, panel, floor, key=key)


def drop_keys(d, exclude):
    return {k: v for k, v in d.items() if k not in exclude} if exclude else d


def rho_pair(xd, yd, centred=True):
    keys, x, y, g, info = A.paired(xd, yd)
    r = A.rho_w(x, y, g, centred) if info["n"] >= 3 else NAN
    return r, keys, x, y, g, info


def perm_hits_rho(x, y, g, obs, rng, n_draws, sided):
    """Draws of rho_w with y permuted within category: (permuted rhos)."""
    rx, ry = A.centred_within_ranks(x, g), A.centred_within_ranks(y, g)
    gidx = A._group_index(g)
    idx = np.arange(len(y))
    out = np.empty(n_draws)
    for t in range(n_draws):
        for gi in gidx:
            idx[gi] = rng.permutation(gi)
        out[t] = A._pearson(rx, ry[idx])
    return out


# =========================================================================== #32 set sampling and cue type
def split_parts(design, code):
    """B2: (part1, part2) CEP lists per category for a 7-bit code."""
    p1, p2 = {}, {}
    for sub in design["ceps"]:
        a = {design["w"][p]: p for p in design["half"]["A"][sub]}
        b = {design["w"][p]: p for p in design["half"]["B"][sub]}
        p1[sub] = [(b if (code >> i) & 1 else a)[w] for i, w in enumerate(W)]
        p2[sub] = [(a if (code >> i) & 1 else b)[w] for i, w in enumerate(W)]
    return p1, p2


def split_codes():
    return [c for c in range(128) if not (c & 1)]


def h32_set_sampling(ans, brands, design, panel, n_perm=N_PERM, seed=SEEDS["H32_SetSampling"], opts=None):
    o = opts or {}
    rng = np.random.default_rng(seed)
    per, obs_r, prepared = {}, [], []
    for code in split_codes():
        p1, p2 = split_parts(design, code)
        _t1, c1 = cov_map_for(ans, brands, p1, panel, A.FLOOR_HALF, o.get("null", "rasch"), o.get("key", "beta"))
        _t2, c2 = cov_map_for(ans, brands, p2, panel, A.FLOOR_HALF, o.get("null", "rasch"), o.get("key", "beta"))
        c1, c2 = drop_keys(c1, o.get("exclude")), drop_keys(c2, o.get("exclude"))
        r, keys, x, y, g, info = rho_pair(c1, c2)
        ok = (not A.below_n_floor(info)) and _f(r)
        per[code] = {"r": r, "rel": A.spearman_brown_half(r), "n": info["n"], "n_categories": info["n_categories"],
                     "meets_n_floor": ok}
        if ok:
            obs_r.append(r)
            prepared.append((x, y, g))
    out = {"splits": len(per), "splits_meeting_n_floor": len(obs_r), "paper_A_H4_split_code": 0,
           "per_split": {str(k): v for k, v in per.items()}}
    if len(obs_r) < MIN_SPLITS:
        out.update(verdict="UNDETERMINED", reason=f"fewer than {MIN_SPLITS} splits meet Paper A's n floor")
        return out
    med = float(np.median(obs_r))
    rels = [A.spearman_brown_half(r) for r in obs_r]
    p10 = float(np.percentile(rels, 10))
    draws = np.vstack([perm_hits_rho(x, y, g, NAN, rng, n_perm, "one") for (x, y, g) in prepared])  # splits x draws
    med_null = np.median(draws, axis=0)
    p = (1 + int(np.sum(med_null >= med - A.TOL))) / (n_perm + 1)
    rel_med = A.spearman_brown_half(med)
    h4 = per.get(0, {})
    pct_h4 = (float(np.mean(np.array(obs_r) <= h4["r"])) * 100) if _f(h4.get("r")) and h4.get("meets_n_floor") else None
    if rel_med >= REL_CONF and p < ALPHA and p10 >= P10_MIN:
        v = "CONFIRMED"
    elif rel_med < REL_FALS or p >= ALPHA:
        v = "FALSIFIED"
    else:
        v = "MARGINAL"
    out.update(median_r=med, rel_median=rel_med, rel_p10=p10, p_perm_one_sided=p, n_perm=n_perm,
               paper_A_split_percentile=pct_h4, verdict=v)
    return out


def h32_cue_type(ans, brands, design, panel, full_cov, opts=None):
    """Leave-one-W-out against removing two CEPs of different W (84 reference pairs)."""
    o = opts or {}

    def drop(excl):
        return {s: [p for p in design["ceps"][s] if p not in excl] for s in design["ceps"]}

    def cov_map_for(a, b, c, p, floor):          # opts applied; floor of the full score (Paper A's S6 rule)
        t, m = globals()["cov_map_for"](a, b, c, p, o.get("floor", floor), o.get("null", "rasch"), o.get("key", "beta"))
        return t, drop_keys(m, o.get("exclude"))
    per_w, ref = {}, []
    undetermined = []
    for w in W:
        excl = {p for p in design["w"] if design["w"][p] == w}
        _t, cm = cov_map_for(ans, brands, drop(excl), panel, A.FLOOR_FULL)
        r, _k, _x, _y, _g, info = rho_pair(full_cov, cm)
        per_w[w] = {"rho_w_full_vs_minus_W": r, "n": info["n"]}
        if A.below_n_floor(info) or not _f(r):
            undetermined.append(w)
    # reference pairs: position (W_i, half h_i) and (W_k, half h_k), i < k, applied to every category alike
    pos = [(i, h) for i in range(len(W)) for h in ("A", "B")]
    pairs = [(a, b) for ai, a in enumerate(pos) for b in pos[ai + 1:] if a[0] != b[0]]
    for (i1, h1), (i2, h2) in pairs:
        excl = set()
        for s in design["ceps"]:
            for (ii, hh) in ((i1, h1), (i2, h2)):
                excl |= {p for p in design["half"][hh][s] if design["w"][p] == W[ii]}
        _t, cm = cov_map_for(ans, brands, drop(excl), panel, A.FLOOR_FULL)
        r, *_ = rho_pair(full_cov, cm)
        if _f(r):
            ref.append(r)
    out = {"per_W": per_w, "reference_pairs": len(pairs), "reference_finite": len(ref)}
    if undetermined or len(ref) < len(pairs) // 2:
        out.update(verdict="UNDETERMINED", reason=f"n floor not met for {undetermined}" if undetermined
                   else "too few finite reference values")
        return out
    p5 = float(np.percentile(ref, CUE_PCT))
    below = [w for w in W if per_w[w]["rho_w_full_vs_minus_W"] < p5]
    cnt = len(below)
    v = "CONFIRMED" if cnt <= CUE_CONF_MAX else ("FALSIFIED" if cnt >= CUE_FALS_MIN else "MARGINAL")
    out.update(reference_p5=p5, reference_median=float(np.median(ref)), W_below_p5=below, count=cnt, verdict=v)
    return out


# =========================================================================== #34 phantom brands
def cliffs_delta_within(values, flags, groups):
    """B4: pooled within-category Cliff's delta (flagged minus unflagged)."""
    values, flags, groups = np.asarray(values, float), np.asarray(flags, bool), np.asarray(groups)
    num = den = 0.0
    for gi in A._group_index(groups):
        r = A.stats.rankdata(values[gi])          # average ranks: U = #(x > y) + 0.5 #(x = y)
        f = flags[gi]
        n1, n2 = int(f.sum()), int((~f).sum())
        if n1 and n2:
            U = r[f].sum() - n1 * (n1 + 1) / 2.0
            num += 2.0 * U - n1 * n2
            den += n1 * n2
    return num / den if den else NAN


def stratified_perm_delta(values, flags, groups, obs, rng, n_perm):
    flags = np.asarray(flags, bool)
    gidx = A._group_index(np.asarray(groups))
    hits = 0
    f = flags.copy()
    for _ in range(n_perm):
        for gi in gidx:
            f[gi] = rng.permutation(flags[gi])
        d = cliffs_delta_within(values, f, groups)
        hits += abs(d) >= abs(obs) - A.TOL
    return (1 + hits) / (n_perm + 1)


def band_signed(stat, p, conf, fals, negative_is_predicted=True):
    """v0.37 sign-split bands: |s| >= conf and p < .05 -> CONFIRMED (predicted sign) / CONFIRMED_REVERSED;
    |s| < fals -> FALSIFIED; otherwise MARGINAL."""
    if not _f(stat):
        return "UNDETERMINED"
    if abs(stat) >= conf and _f(p) and p < ALPHA:
        pred = stat < 0 if negative_is_predicted else stat > 0
        return "CONFIRMED" if pred else "CONFIRMED_REVERSED"
    if abs(stat) < fals:
        return "FALSIFIED"
    return "MARGINAL"


def rank_residuals(y, p, g):
    """B5: residual of centred within ranks of y on centred within ranks of p, within each category."""
    ry, rp = A.centred_within_ranks(y, g), A.centred_within_ranks(p, g)
    out = np.empty(len(y))
    for gi in A._group_index(np.asarray(g)):
        X = np.column_stack([np.ones(len(gi)), rp[gi]])
        coef, *_ = np.linalg.lstsq(X, ry[gi], rcond=None)
        out[gi] = ry[gi] - X @ coef
    return out


def h34_floor(cov, flags, P, n_perm=N_PERM):
    keys = sorted(k for k in cov if _f(cov.get(k)) and k in flags)
    per = collections.Counter(k[0] for k in keys)
    keys = [k for k in keys if per[k[0]] >= A.MIN_UNITS_PER_CAT]
    vals = [float(cov[k]) for k in keys]
    fl = [bool(flags[k]) for k in keys]
    grp = [k[0] for k in keys]
    nf, nn = sum(fl), len(fl) - sum(fl)
    cats_with_pairs = {g for g in set(grp) if any(f for f, gg in zip(fl, grp) if gg == g)
                       and any((not f) for f, gg in zip(fl, grp) if gg == g)}
    out = {"n_flagged_rated": nf, "n_unflagged_rated": nn, "categories_with_pairs": sorted(cats_with_pairs)}
    if nf < PH_MIN or nn < PH_MIN or len(cats_with_pairs) < 3:
        out["primary"] = {"verdict": "UNDETERMINED", "reason": f"fewer than {PH_MIN} rated flagged or unflagged units, "
                                                               "or fewer than 3 categories with both"}
        out["beyond_presence"] = {"verdict": "UNDETERMINED"}
        return out
    d = cliffs_delta_within(vals, fl, grp)
    p = stratified_perm_delta(vals, fl, grp, d, np.random.default_rng(SEEDS["H34_Floor_Signature"]), n_perm)
    out["primary"] = {"cliffs_delta": d, "p_perm_two_sided": p, "n_perm": n_perm,
                      "verdict": band_signed(d, p, DELTA_CONF, DELTA_FALS)}
    kp = [i for i, k in enumerate(keys) if _f(P.get(k))]
    if len(kp) >= 2 * PH_MIN:
        y = np.array([vals[i] for i in kp])
        pp = np.array([float(P[keys[i]]) for i in kp])
        gg = np.array([grp[i] for i in kp])
        res = rank_residuals(y, pp, gg)
        f2 = [fl[i] for i in kp]
        d2 = cliffs_delta_within(list(res), f2, list(gg))
        p2 = stratified_perm_delta(list(res), f2, list(gg), d2,
                                   np.random.default_rng(SEEDS["H34_Floor_BeyondPresence"]), n_perm)
        out["beyond_presence"] = {"cliffs_delta_resid": d2, "p_perm_two_sided": p2, "n": len(kp),
                                  "verdict": band_signed(d2, p2, DELTA_CONF, DELTA_FALS)}
    else:
        out["beyond_presence"] = {"verdict": "UNDETERMINED", "reason": "P missing for too many units"}
    return out


def h34_defunct(ans, design, panel, defunct, sub="v0.22", texts=None, n_draws=N_PERM):
    """Answers (panel, automotive CEPs) naming >= 1 defunct brand, by W; null W shares = W shares of all other
    registry-brand mentions in the same answers; Monte Carlo multinomial (seed)."""
    keys = [k for k in ans if k[0] == sub and k[1] in panel]
    cnt = collections.Counter(design["w"][k[2]] for k in keys if ans[k] & set(defunct))
    ref = collections.Counter()
    for k in keys:
        ref[design["w"][k[2]]] += len(ans[k] - set(defunct))
    n = int(sum(cnt.values()))
    out = {"answers_naming_defunct": n, "by_W": {w: cnt.get(w, 0) for w in W},
           "answers": len(keys), "per_brand": {b: sum(1 for k in keys if b in ans[k]) for b in defunct}}
    if texts is not None:
        out["caveat"] = caveat_counts(ans, keys, defunct, texts, design)
    tot = sum(ref.values())
    if n < DEF_MIN or tot == 0:
        out.update(verdict="UNDETERMINED", reason=f"fewer than {DEF_MIN} answers name a defunct brand")
        return out
    q = np.array([ref.get(w, 0) / tot for w in W])
    obs = max(cnt.values()) / n
    rng = np.random.default_rng(SEEDS["H34_Defunct_Occupancy"])
    sims = rng.multinomial(n, q, size=n_draws).max(axis=1) / n
    p = (1 + int(np.sum(sims >= obs - A.TOL))) / (n_draws + 1)
    v = ("CONFIRMED" if obs >= DEF_SHARE else "MARGINAL") if p < ALPHA else "FALSIFIED"
    out.update(max_W_share=obs, max_W=max(cnt, key=cnt.get), null_W_shares=dict(zip(W, q.tolist())),
               p_mc=p, n_draws=n_draws, verdict=v)
    return out


def caveat_counts(ans, keys, defunct, texts, design):
    """D34 (descriptive): an answer's defunct mention is caveated if a CAVEAT_TERMS term occurs within
    CAVEAT_WINDOW characters of the brand name (case-insensitive), else naive (v0.10 / v0.38 D7)."""
    res = {"naive": collections.Counter(), "caveated": collections.Counter()}
    for k in keys:
        t = (texts.get(k) or "").lower()
        for b in sorted(ans[k] & set(defunct)):
            pos = [i for i in range(len(t)) if t.startswith(b.lower(), i)]
            cav = any(term in t[max(0, i - CAVEAT_WINDOW): i + len(b) + CAVEAT_WINDOW] for i in pos for term in CAVEAT_TERMS)
            res["caveated" if cav else "naive"][design["w"][k[2]]] += 1
    return {k: dict(v) for k, v in res.items()}


# =========================================================================== expected W occupancy (B6)
def esp(w, n):
    """Elementary symmetric polynomials e_0..e_n of weights w."""
    e = np.zeros(n + 1)
    e[0] = 1.0
    for x in w:
        e[1:] = e[1:] + x * e[:-1]
    return e


def inclusion_probs(slot_cep, delta, n):
    """pi_s for each slot under the conditional Bernoulli law with weights exp(delta_j(s)), given n named."""
    slot_cep = np.asarray(slot_cep, int)
    w = np.exp(np.asarray(delta, float)[slot_cep] - np.max(np.asarray(delta, float)))
    S = len(w)
    if n <= 0:
        return np.zeros(S)
    if n >= S:
        return np.ones(S)
    e_all = esp(w, n)
    out = np.empty(S)
    cache = {}
    for i in range(S):
        key = slot_cep[i]
        if key not in cache:
            wo = np.delete(w, i)
            cache[key] = w[i] * esp(wo, n - 1)[n - 1] / e_all[n]
        out[i] = cache[key]
    return out


def excess_profiles(ans, brands, ceps_by_sub, design, panel, null="rasch"):
    """B6: {unit: (excess share per W (len 7, NaN where the W has no CEP in the set), total n)}. null="equal": delta 0
    (sensitivity S-Equal)."""
    prof = {}
    for sub in sorted(ceps_by_sub):
        ceps = list(ceps_by_sub[sub])
        cidx = {p: i for i, p in enumerate(ceps)}
        bl = sorted(brands[sub])
        bidx = {b: i for i, b in enumerate(bl)}
        acc = {b: [np.zeros(len(W)), np.zeros(len(W)), 0] for b in bl}
        for m in sorted(panel):
            keys = sorted(k for k in ans if k[0] == sub and k[1] == m and k[2] in cidx)
            slot = np.array([cidx[k[2]] for k in keys], int)
            Y = np.zeros((len(keys), len(bl)), np.int8)
            for i, k in enumerate(keys):
                for b in ans[k]:
                    if b in bidx:
                        Y[i, bidx[b]] = 1
            if null == "equal":
                deltas = np.zeros((len(bl), len(ceps)))
            else:
                deltas, _status = A.rasch_deltas(slot, Y, len(ceps))
            wslot = np.array([W.index(design["w"][ceps[j]]) for j in slot], int) if len(slot) else np.zeros(0, int)
            for b in bl:
                y = Y[:, bidx[b]]
                n = int(y.sum())
                if n == 0:
                    continue
                pi = inclusion_probs(slot, deltas[bidx[b]], n)
                acc[b][0] += np.bincount(wslot[y == 1], minlength=len(W))
                acc[b][1] += np.bincount(wslot, weights=pi, minlength=len(W))
                acc[b][2] += n
        present = {W.index(design["w"][p]) for p in ceps}
        for b in bl:
            o, e, n = acc[b]
            v = (o - e) / n if n else np.full(len(W), NAN)
            v = np.array([v[i] if i in present else NAN for i in range(len(W))])
            prof[(sub, b)] = (v, n)
    return prof


# =========================================================================== #35 identity load
def load_channels(probes_v042_path):
    """{(substrate 'v0.NN', Phase B probe_id): channel} from v0.42's probe file (trio probe IDs q1-q6 repeat across
    categories, so the key carries the category)."""
    inv = {v: k for k, v in A.RAW_SUB.items()}
    out = {}
    for line in Path(probes_v042_path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        if d.get("phase") == "B" and d.get("channel"):
            out[(inv.get(d["substrate"], d["substrate"]), d["probe_id"])] = d["channel"]
    return out


def il_from_t4(coded_b_rows, channel_of_probe, units, models, excluded=()):
    """IL_b = k_cult/n_cult - k_cat/n_cat on the t4 N3 S0 Phase B answers of the trio (v0.37 IL-Direct normalised by
    answered calls, as the v0.65 draft's EN definition); also pi_hat over the six questions. Rows: v0.42 coded
    Phase B rows (call_id, substrate, brand, model, condition, run, probe_id, mentioned), answered calls only;
    calls v0.42 excludes (excluded) are dropped, as Paper A's comparators drop them. channel_of_probe is keyed by
    (substrate, probe_id) (load_channels) or by probe_id alone (tests)."""
    calls = collections.defaultdict(set)
    named = collections.defaultdict(set)
    excluded = set(excluded)
    for r in coded_b_rows:
        if r["model"] not in models or (r.get("condition") or "S0") != "S0" or r["substrate"] not in TRIO:
            continue
        if r["call_id"] in excluded:
            continue
        ch = channel_of_probe.get((r["substrate"], r["probe_id"]), channel_of_probe.get(r["probe_id"]))
        if ch not in ("R_cat", "R_cult"):
            continue
        calls[(r["substrate"], ch)].add(r["call_id"])
        if str(r["mentioned"]) in ("1", "True", "true"):
            named[(r["substrate"], r["brand"], ch)].add(r["call_id"])
    out = {}
    for (s, b) in units:
        if s not in TRIO:
            continue
        nc, nu = len(calls[(s, "R_cat")]), len(calls[(s, "R_cult")])
        kc, ku = len(named[(s, b, "R_cat")]), len(named[(s, b, "R_cult")])
        if nc and nu:
            out[(s, b)] = {"il": ku / nu - kc / nc, "pi_hat": (kc + ku) / (nc + nu)}
    return out


def partial_rho(x, y, z, g):
    rx, ry, rz = (A.centred_within_ranks(v, g) for v in (x, y, z))

    def res(a):
        X = np.column_stack([np.ones(len(a)), rz])
        c, *_ = np.linalg.lstsq(X, a, rcond=None)
        return a - X @ c
    return A._pearson(res(rx), res(ry))


def h35(cov, il, P, se_excess, n_perm=N_PERM):
    elig = {k: v["il"] for k, v in il.items() if 0 < v["pi_hat"] < 1}
    r, keys, x, y, g, info = rho_pair(elig, cov)
    out = {"n": info["n"], "per_category": info["per_category"], "eligible_il_units": len(elig)}
    if info["n"] < IL_NFLOOR or info["n_categories"] < 3 or not _f(r):
        out["primary"] = {"verdict": "UNDETERMINED", "reason": f"n < {IL_NFLOOR} or fewer than 3 trio categories"}
        out["robust"] = {"verdict": "UNDETERMINED"}
        out["cue_type"] = {"verdict": "UNDETERMINED"}
        return out
    p = A.perm_p(x, y, g, r, SEEDS["H35_IL_Coverage"], "two", n_perm)
    v = band_signed(r, p, IL_CONF, IL_FALS)
    out["primary"] = {"rho_w": r, "p_perm_two_sided": p, "n_perm": n_perm, "verdict": v}
    kp = [i for i, k in enumerate(keys) if _f(P.get(k))]
    if len(kp) >= IL_NFLOOR:
        xx, yy, gg = x[kp], y[kp], g[kp]
        zz = np.array([float(P[keys[i]]) for i in kp])
        pr = partial_rho(xx, yy, zz, gg)
        rng = np.random.default_rng(SEEDS["H35_IL_Robust"])
        gidx = A._group_index(gg)
        idx = np.arange(len(xx))
        hits = 0
        for _ in range(n_perm):
            for gi in gidx:
                idx[gi] = rng.permutation(gi)
            hits += abs(partial_rho(xx[idx], yy, zz, gg)) >= abs(pr) - A.TOL
        pp = (1 + hits) / (n_perm + 1)
        pband = ("CONFIRMED" if abs(pr) >= IL_CONF and pp < ALPHA else ("NULL" if abs(pr) < IL_FALS else "MIDDLE"))
        out["robust"] = {"partial_rho_given_P": pr, "p_perm_two_sided": pp, "partial_band": pband,
                         "cell": il_matrix(v, pr, pband)}
    else:
        out["robust"] = {"verdict": "UNDETERMINED", "reason": "P missing for too many units"}
    r3, k3, x3, y3, g3, i3 = rho_pair(elig, se_excess)
    if i3["n"] >= IL_NFLOOR and i3["n_categories"] >= 3 and _f(r3):
        p3 = A.perm_p(x3, y3, g3, r3, SEEDS["H35_IL_CueType"], "two", n_perm)
        out["cue_type"] = {"rho_w": r3, "p_perm_two_sided": p3, "n": i3["n"],
                           "verdict": band_signed(r3, p3, IL_CONF, IL_FALS, negative_is_predicted=False)}
    else:
        out["cue_type"] = {"verdict": "UNDETERMINED", "n": i3["n"]}
    return out


def il_matrix(v, pr, pband):
    """v0.37 verdict matrix (r2), carried over; exhaustive."""
    if v in ("CONFIRMED", "CONFIRMED_REVERSED"):
        return ("moderation beyond Presence" if abs(pr) >= IL_FALS else "moderation carried by Presence") + \
            (" (reversed sign)" if v == "CONFIRMED_REVERSED" else "")
    if v == "FALSIFIED":
        return "CLEAN NULL" if pband == "NULL" else "null on the raw arm, not clean (partial not null)"
    return "MARGINAL"


# =========================================================================== #36 typology
def silhouette(X, lab):
    lab = np.asarray(lab)
    ks = np.unique(lab)
    if len(ks) < 2:
        return NAN
    D = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(-1))
    s = np.zeros(len(X))
    for i in range(len(X)):
        same = lab == lab[i]
        if same.sum() <= 1:
            s[i] = 0.0
            continue
        a = D[i, same].sum() / (same.sum() - 1)
        b = min(D[i, lab == k].mean() for k in ks if k != lab[i])
        s[i] = (b - a) / max(a, b) if max(a, b) > 0 else 0.0
    return float(s.mean())


def ari(a, b):
    a, b = np.asarray(a), np.asarray(b)
    ua, ia = np.unique(a, return_inverse=True)
    ub, ib = np.unique(b, return_inverse=True)
    M = np.zeros((len(ua), len(ub)))
    np.add.at(M, (ia, ib), 1)
    c2 = lambda v: v * (v - 1) / 2.0  # noqa: E731
    s_ij, s_a, s_b, n2 = c2(M).sum(), c2(M.sum(1)).sum(), c2(M.sum(0)).sum(), c2(len(a))
    exp = s_a * s_b / n2 if n2 else 0.0
    mx = (s_a + s_b) / 2.0
    return float((s_ij - exp) / (mx - exp)) if mx != exp else 0.0


def ward_labels(X, k):
    if k <= 1 or len(X) < 2:
        return np.ones(len(X), int)
    return fcluster(linkage(X, "ward"), k, "maxclust")


def wk(X, lab):
    return sum(((X[lab == c] - X[lab == c].mean(0)) ** 2).sum() for c in np.unique(lab))


def gap_k(X, rng, B=GAP_B, kmax=K_MAX):
    kmax = min(kmax, len(X) - 1)
    lo, hi = X.min(0), X.max(0)
    logw = np.array([math.log(max(wk(X, ward_labels(X, k)), 1e-300)) for k in range(1, kmax + 1)])
    ref = np.empty((B, kmax))
    for b in range(B):
        R = rng.uniform(lo, hi, size=X.shape)
        ref[b] = [math.log(max(wk(R, ward_labels(R, k)), 1e-300)) for k in range(1, kmax + 1)]
    gap = ref.mean(0) - logw
    sk = ref.std(0) * math.sqrt(1 + 1.0 / B)
    for k in range(1, kmax):
        if gap[k - 1] >= gap[k] - sk[k]:
            return k, gap.tolist()
    return kmax, gap.tolist()


def structure(X, g, rng, n_perm, B=GAP_B):
    k, gap = gap_k(X, rng, B)
    lab = ward_labels(X, k)
    sil = silhouette(X, lab) if k >= 2 else NAN
    null = []
    if k >= 2:
        gidx = A._group_index(g)
        for _ in range(n_perm):
            Xp = X.copy()
            for j in range(X.shape[1]):
                for gi in gidx:
                    Xp[gi, j] = X[rng.permutation(gi), j]
            null.append(silhouette(Xp, ward_labels(Xp, k)))
    pct = float(np.percentile(null, SIL_PCT)) if null else NAN
    auto = bool(k >= 2 and sil >= SIL_MIN and sil > pct)
    return {"k": k, "gap": gap, "silhouette": sil, "silhouette_null_p95": pct, "n_null": len(null),
            "internal_structure": auto}, lab


def presence_tiers(P, keys):
    """B8: v0.23 regime rule within category."""
    out = {}
    for s in dict.fromkeys(k[0] for k in keys):
        ks = [k for k in keys if k[0] == s and _f(P.get(k))]
        vals = sorted(float(P[k]) for k in ks)
        if len(vals) >= 4:
            q25, q50, q75 = (float(np.percentile(vals, q)) for q in (25, 50, 75))
        else:
            q25 = q50 = q75 = 0.0
        for k in ks:
            v = float(P[k])
            out[k] = "Dominant" if v >= q75 else "Established" if v >= q50 else "Emerging" if v >= q25 else "Absent"
    return out


def h36_replication(profA, profB, keys_ok, n_perm=N_PERM):
    keys = sorted(k for k in keys_ok if k in profA and k in profB and profA[k][1] >= A.FLOOR_HALF
                  and profB[k][1] >= A.FLOOR_HALF)
    per = collections.Counter(k[0] for k in keys)
    keys = [k for k in keys if per[k[0]] >= A.MIN_UNITS_PER_CAT]
    info = {"n": len(keys), "n_categories": len({k[0] for k in keys})}
    if A.below_n_floor(info):
        return {"verdict": "UNDETERMINED", **info}
    g = np.array([k[0] for k in keys])
    XA = np.array([profA[k][0] for k in keys])
    XB = np.array([profB[k][0] for k in keys])
    RA = np.column_stack([A.centred_within_ranks(XA[:, j], g) for j in range(len(W))])
    RB = np.column_stack([A.centred_within_ranks(XB[:, j], g) for j in range(len(W))])

    def stat(idx):
        return float(np.mean([A._pearson(RA[:, j], RB[idx, j]) for j in range(len(W))]))
    obs = stat(np.arange(len(keys)))
    rng = np.random.default_rng(SEEDS["H36_Profile_Replication"])
    gidx = A._group_index(g)
    idx = np.arange(len(keys))
    hits = 0
    for _ in range(n_perm):
        for gi in gidx:
            idx[gi] = rng.permutation(gi)
        hits += stat(idx) >= obs - A.TOL
    p = (1 + hits) / (n_perm + 1)
    per_w = {w: A._pearson(RA[:, j], RB[:, j]) for j, w in enumerate(W)}
    v = "CONFIRMED" if obs >= REP_CONF and p < ALPHA else ("FALSIFIED" if obs < REP_FALS or p >= ALPHA else "MARGINAL")
    return {"mean_rho_w_over_W": obs, "per_W": per_w, "p_perm_one_sided": p, "n_perm": n_perm, "verdict": v, **info}


def h36_structure(prof, cov, P, rep_verdict, n_perm=N_PERM, B=GAP_B):
    keys = sorted(k for k in prof if _f(cov.get(k)) and np.all(np.isfinite(prof[k][0])))
    per = collections.Counter(k[0] for k in keys)
    keys = [k for k in keys if per[k[0]] >= A.MIN_UNITS_PER_CAT]
    g = np.array([k[0] for k in keys])
    X = np.array([prof[k][0] for k in keys])
    rng = np.random.default_rng(SEEDS["H36_Structure"])
    res = {"n": len(keys)}
    if A.below_n_floor({"n": len(keys), "n_categories": len(set(g))}):
        res.update(cell="UNDETERMINED", reason="below Paper A's n floor")
        return res
    st, lab = structure(X, g, rng, n_perm, B)
    tiers = presence_tiers(P, keys)
    kt = [i for i, k in enumerate(keys) if k in tiers]
    a_obs = ari(lab[kt], [tiers[keys[i]] for i in kt]) if st["k"] >= 2 else 0.0
    tl = np.array([tiers[keys[i]] for i in kt])
    gt = g[kt]
    nulls = []
    for _ in range(n_perm if st["k"] >= 2 else 0):
        t2 = tl.copy()
        for gi in A._group_index(gt):
            t2[gi] = tl[rng.permutation(gi)]
        nulls.append(ari(lab[kt], t2))
    p_ari = (1 + sum(x >= a_obs - A.TOL for x in nulls)) / (len(nulls) + 1) if nulls else 1.0
    inherit = bool(st["k"] >= 2 and a_obs >= ARI_MIN and p_ari < ARI_P)
    Pv = np.array([float(P[k]) if _f(P.get(k)) else NAN for k in keys])
    ok = np.isfinite(Pv)
    Xr = X[ok].copy()
    for gi in A._group_index(g[ok]):
        Z = np.column_stack([np.ones(len(gi)), Pv[ok][gi]])
        for j in range(X.shape[1]):
            c, *_ = np.linalg.lstsq(Z, Xr[gi, j], rcond=None)
            Xr[gi, j] = Xr[gi, j] - Z @ c
    st_r, _ = structure(Xr, g[ok], np.random.default_rng(SEEDS["H36_Gap"]), n_perm, B)
    resid = st_r["internal_structure"]
    auto = bool(st["internal_structure"] and a_obs < ARI_MIN)
    cell = typology_cell(rep_verdict, inherit, auto, resid)
    res.update(full=st, ari_vs_presence_tiers=a_obs, p_ari=p_ari, inheritance=inherit, autonomy=auto,
               residual=st_r, residual_structure=resid, cell=cell,
               dj_quadrants=dj_quadrants(cov, P, keys))
    return res


def typology_cell(rep, inherit, auto, resid):
    """Exhaustive matrix (section 6.4)."""
    if rep not in ("CONFIRMED", "MARGINAL"):
        return "NO TYPOLOGY (profiles do not replicate); structure reported descriptively"
    tag = "" if rep == "CONFIRMED" else " [provisional: replication MARGINAL]"
    if inherit:
        return ("LAYERED" if resid else "BORROWED") + tag
    if auto:
        return ("AUTONOMOUS" if resid else "PRESENCE-DEPENDENT") + tag
    return ("RESIDUAL-ONLY" if resid else "UNSTRUCTURED") + tag


def dj_quadrants(cov, P, keys):
    """D36 (descriptive): P above/below its within-category median x Cov* above/below 50."""
    q = collections.Counter()
    for s in dict.fromkeys(k[0] for k in keys):
        ks = [k for k in keys if k[0] == s and _f(P.get(k))]
        if not ks:
            continue
        med = float(np.median([float(P[k]) for k in ks]))
        for k in ks:
            q[("high P" if float(P[k]) > med else "low P", "broad" if cov[k] > 50 else "situation-bound")] += 1
    return {f"{a} | {b}": v for (a, b), v in sorted(q.items())}


# =========================================================================== orchestration
def score_b(inp, n_perm=N_PERM, gap_b=GAP_B, studies=("32", "34", "35", "36"), opts=None):
    """inp: ans (Paper A answer index), design, brands, panel, P ({unit: P comparator}), flags ({unit: bool}),
    defunct (names), il ({unit: {'il', 'pi_hat'}} or None), texts ({answer key: text} or None),
    a_doc (Paper A verdict document), pablo_decision (or None). opts (sensitivities only): exclude (units),
    floor (full Cov* floor), null ("rasch" / "equal"), key ("beta" / "beta_mid")."""
    dec = paper_b_decision(inp["a_doc"], inp.get("pablo_decision"))
    if not dec["run"]:
        return not_run_record(dec, inp.get("a_sha256"))
    o = opts or {}
    ex = set(o.get("exclude") or ())
    ans, design, brands, panel = inp["ans"], inp["design"], inp["brands"], inp["panel"]
    _tab, cov = cov_map_for(ans, brands, design["ceps"], panel, o.get("floor", A.FLOOR_FULL), o.get("null", "rasch"),
                            o.get("key", "beta"))
    cov = drop_keys(cov, ex)
    inp = dict(inp, P=drop_keys(inp["P"], ex), flags=drop_keys(inp["flags"], ex),
               il=None if inp.get("il") is None else drop_keys(inp["il"], ex))
    doc = {"phase": PHASE_ID, "prereg_tag": PREREG_TAG, "status": dec["status"], "paper_A": dec,
           "panel": panel, "draws": {"permutation": n_perm, "gap_reference": gap_b}, "seeds": SEEDS,
           "rated_units": int(sum(1 for v in cov.values() if _f(v)))}
    if dec["a_verdict"] == "MARGINAL":
        doc["label"] = "every verdict below is conditional on a MARGINAL Paper A gate (legs: %s)" % dec.get("marginal_legs")
    if "32" in studies:
        doc["H32_SetSampling"] = h32_set_sampling(ans, brands, design, panel, n_perm, opts=o)
        doc["H32_CueType"] = h32_cue_type(ans, brands, design, panel, cov, opts=o)
    prof = drop_keys(excess_profiles(ans, brands, design["ceps"], design, panel, o.get("null", "rasch")), ex)
    if "34" in studies:
        doc["H34_Floor"] = h34_floor(cov, inp["flags"], inp["P"], n_perm)
        doc["H34_Defunct_Occupancy"] = h34_defunct(ans, design, panel, inp["defunct"], texts=inp.get("texts"),
                                                   n_draws=n_perm)
    if "35" in studies:
        se_idx = [W.index(w) for w in SE_CUES]
        se = {k: float(v[0][se_idx].sum()) for k, v in prof.items() if v[1] > 0 and _f(cov.get(k))}
        doc["H35"] = h35(cov, inp["il"] or {}, inp["P"], se, n_perm) if inp.get("il") is not None else \
            {"primary": {"verdict": "UNDETERMINED", "reason": "identity-load input not supplied"}}
    if "36" in studies:
        pa = drop_keys(excess_profiles(ans, brands, design["half"]["A"], design, panel, o.get("null", "rasch")), ex)
        pb = drop_keys(excess_profiles(ans, brands, design["half"]["B"], design, panel, o.get("null", "rasch")), ex)
        rated = [k for k, v in cov.items() if _f(v)]
        rep = h36_replication(pa, pb, rated, n_perm)
        doc["H36_Profile_Replication"] = rep
        doc["H36_Structure"] = h36_structure(prof, cov, inp["P"], rep["verdict"], n_perm, gap_b)
    doc["verdict_summary"] = summary(doc)
    return doc


COI_UNITS = (("v0.19", "Denon"), ("v0.22", "Chevrolet"), ("v0.22", "BMW"), ("v0.22", "Bentley"), ("v0.23", "S03"),
             ("v0.20", "Eucerin"))                          # section 14; S03 = Jack Daniel's


def load_il_t1(path=ROOT / "osf/methodology/v1_7/data/v1_7_cpc.csv"):
    """S-IL-t1 (B11): v0.37's IL-Direct = R_cult_total - R_cat_total on the trio, read as score_v0_37.load_il_direct
    reads it; eligibility 0 < mean_r / 6 < 1 (six Phase B frames per model). Ranks equal v0.37's count form."""
    out = {}
    for r in A.read_csv_rows(path):
        if r["substrate"] in TRIO:
            out[(r["substrate"], r["brand"])] = {"il": float(r["R_cult_total"]) - float(r["R_cat_total"]),
                                                 "pi_hat": float(r["mean_r"]) / 6.0}
    return out


def sensitivities(inp, base, n_perm=N_PERM, gap_b=GAP_B, only=None):
    """Section 8: each variant re-scores the studies it touches; verdicts are reported with their changes against
    the primary summary `base`; no variant changes a verdict."""
    cats = A.CATS
    defunct_units = {k for k in inp["flags"] if k[0] == "v0.22" and k[1] in set(inp["defunct"])}
    variants = {
        "S-COI": ({"exclude": COI_UNITS}, ("32", "34", "35", "36"), None),
        "S-Floor6": ({"floor": 6}, ("34", "35", "36"), None),
        "S-Equal": ({"null": "equal"}, ("32", "36"), None),
        "S-Mid": ({"key": "beta_mid"}, ("32", "34"), None),
        "S-F-noD": ({}, ("34",), {"flags": {k: v for k, v in inp["flags"].items() if k not in defunct_units}}),
    }
    for c in cats:                                   # H34_Defunct_Occupancy is one category's test: unchanged by LOCO
        variants[f"S-LOCO-{c}"] = ({"exclude": tuple((c, b) for b in inp["brands"].get(c, ()))},
                                   ("32", "34", "35", "36"), None)
    c3 = list(A.PANELS["C3"])
    if all(any(k[1] == m for k in inp["ans"]) for m in c3):
        variants["S-C3"] = ({}, ("32", "34", "35", "36"), {"panel": c3})
    if inp.get("il_t1") is not None:
        variants["S-IL-t1"] = ({}, ("35",), {"il": inp["il_t1"]})
    out = {}
    for name, (opts, studies, repl) in variants.items():
        if only and name not in only:
            continue
        doc = score_b(dict(inp, **(repl or {})), n_perm, gap_b, studies, opts)
        s = doc.get("verdict_summary") or {}
        out[name] = {"opts": {k: (list(v) if isinstance(v, tuple) else v) for k, v in opts.items()},
                     "studies": list(studies), "verdicts": s,
                     "verdict_changes": {h: [base.get(h), v] for h, v in s.items() if v != base.get(h)}}
    return out


def summary(doc):
    s = {}
    for k in ("H32_SetSampling", "H32_CueType", "H34_Defunct_Occupancy", "H36_Profile_Replication"):
        if k in doc:
            s[k] = doc[k].get("verdict")
    if "H34_Floor" in doc:
        s["H34_Floor_Signature"] = doc["H34_Floor"]["primary"].get("verdict")
        s["H34_Floor_BeyondPresence"] = doc["H34_Floor"]["beyond_presence"].get("verdict")
    if "H35" in doc:
        s["H35_IL_Coverage"] = doc["H35"]["primary"].get("verdict")
        s["H35_IL_Robust_cell"] = (doc["H35"].get("robust") or {}).get("cell", (doc["H35"].get("robust") or {}).get("verdict"))
        s["H35_IL_CueType"] = (doc["H35"].get("cue_type") or {}).get("verdict")
    if "H36_Structure" in doc:
        s["H36_Typology_cell"] = doc["H36_Structure"].get("cell")
    return s


# =========================================================================== guards for the real run
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tag_on_origin(tag):
    try:
        out = subprocess.run(["git", "-C", str(ROOT), "ls-remote", "--tags", "origin", f"refs/tags/{tag}"],
                             capture_output=True, text=True, timeout=60).stdout
    except Exception:  # noqa: BLE001
        return False
    return bool(out.strip())


A_SCORER_SHA256 = "f7689898fdc68715f207ffc0c1e335a0264aefcce0b2836d1fd5e79624709d20"   # v1.12 LOCK_MANIFEST line


def parity_b_p0():
    """B-P0: the imported Paper A scorer is the locked file (SHA-256 in v1.12's LOCK_MANIFEST)."""
    got = sha256(A.__file__)
    listed = [ln.split()[0] for ln in A_MANIFEST.read_text(encoding="utf-8").splitlines()
              if ln.strip().endswith("osf/methodology/v1_12/scripts/score_v1_12.py")]
    return {"gate": "B-P0", "imported": got, "manifest": listed, "expected": A_SCORER_SHA256,
            "passed": got == A_SCORER_SHA256 and listed == [A_SCORER_SHA256]}


def real_run_guards():
    """Section 9: refuse unless B's tag is on origin and anchored, A's verdict exists, and no B output exists."""
    if not tag_on_origin(PREREG_TAG):
        raise Refused(f"tag {PREREG_TAG} is not on origin: no Paper B statistic before the lock")
    if not ANCHOR.exists():
        raise Refused(f"{ANCHOR} missing: the lock is not anchored (OSF deposit and commit record)")
    try:
        tag_commit = subprocess.run(["git", "-C", str(ROOT), "rev-parse", f"{PREREG_TAG}^{{commit}}"],
                                    capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception:  # noqa: BLE001
        tag_commit = ""
    if not tag_commit or json.loads(ANCHOR.read_text(encoding="utf-8")).get("commit") != tag_commit:
        raise Refused(f"{ANCHOR} does not name the commit of {PREREG_TAG}")
    if not A_VERDICTS.exists() or not A_UNIT_TABLE.exists():
        raise Refused("Paper A's verdict file or unit table is missing: Paper B waits for Paper A's scored output")
    if OUT_DIR.exists() and any(OUT_DIR.iterdir()):
        raise Refused(f"{OUT_DIR} is not empty: Paper B is scored once")


def parity_b_p1(cov, unit_rows):
    """B-P1: Cov* recomputed with the imported code equals Paper A's unit table (column cov_star), every unit."""
    mism = []
    for r in unit_rows:
        k = (r["substrate"], r["brand"])
        a = float(r["cov_star"]) if r.get("cov_star") not in (None, "") else None
        b = cov.get(k)
        if (a is None) != (not _f(b)) or (a is not None and abs(a - b) > 1e-9):
            mism.append({"unit": list(k), "paper_A": a, "recomputed": b})
    return {"gate": "B-P1", "units": len(unit_rows), "mismatches": mism[:20], "passed": not mism}


REAL_PATHS = {"a_raw": A.RAW_PATH, "a_coded": A.CODED_DIR, "a_verdicts": A_VERDICTS, "a_unit_table": A_UNIT_TABLE,
              "a_probes": A.PROBES_PATH, "roster": ROSTER, "t4_raw": A.T4_DEFAULTS["raw"],
              "t4_coded": A.T4_DEFAULTS["coded"], "t4_probes": ROOT / "osf/v42/prereg/probes_v0_42.jsonl",
              "decision": DESIGN_DIR / "anchor/pablo_decision_paper_B.json", "out": OUT_DIR,
              "il_t1": ROOT / "osf/methodology/v1_7/data/v1_7_cpc.csv", "only_sens": None}


def read_roster(path):
    rows = A.read_csv_rows(path)
    flags = {(r["substrate"], r["brand"]): r["recall_floor_flag_F"] == "1" for r in rows}
    defunct = tuple(r["brand"] for r in rows if r["defunct_D"] == "1")
    return flags, defunct


def load_real(paths):
    """B1: Paper A's analysis set through Paper A's own functions; Paper A's verdict document, panel and P; the frozen
    roster; t4 identity load (N3, S0, trio; v0.42's exclusions). Returns (inp, unit_rows, record of inputs)."""
    p = {k: Path(v) for k, v in paths.items() if isinstance(v, (str, Path))}
    a_doc = json.loads(p["a_verdicts"].read_text(encoding="utf-8"))
    decision = json.loads(p["decision"].read_text(encoding="utf-8")) if p["decision"].exists() else None
    rec = {"paper_A_verdicts_sha256": sha256(p["a_verdicts"])}
    if not paper_b_decision(a_doc, decision)["run"]:
        return {"a_doc": a_doc, "pablo_decision": decision, "a_sha256": rec["paper_A_verdicts_sha256"]}, [], rec
    raw = A.read_jsonl(p["a_raw"])
    mentions, registry = A.read_coded(p["a_coded"])
    design = A.probe_design(A.load_probes(p["a_probes"]))
    An = A.build_analysis(A.dedupe_calls(raw), mentions, design)
    texts = {(r["substrate"], r["model_requested"], r["probe_id"], int(r["run"])): r.get("text") or ""
             for r in An["calls"].values() if design["role"][r["probe_id"]] == "CEP"}
    brands = {s: list(registry[s]) for s in A.CATS if s in registry}
    panel = list(a_doc["panels"][a_doc["primary_panel"]])
    unit_rows = A.read_csv_rows(p["a_unit_table"])
    P = {(r["substrate"], r["brand"]): float(r["P_comparator"]) for r in unit_rows if r.get("P_comparator") not in (None, "")}
    flags, defunct = read_roster(p["roster"])
    units = sorted((s, b) for s in brands for b in brands[s])
    il = None
    if p["t4_raw"].exists() and p["t4_coded"].exists() and p["t4_probes"].exists():
        excl, _w = A.t4_excluded(A.read_jsonl(p["t4_raw"]))
        _ca, cb = A.read_t4_coded(p["t4_coded"])
        il = il_from_t4(cb, load_channels(p["t4_probes"]), units, list(A.T4_N3), excl)
        rec.update(t4_raw_sha256=sha256(p["t4_raw"]), t4_probes_sha256=sha256(p["t4_probes"]))
    rec.update(paper_A_raw_sha256=sha256(p["a_raw"]), paper_A_unit_table_sha256=sha256(p["a_unit_table"]),
               roster_sha256=sha256(p["roster"]), panel=panel, primary_panel=a_doc["primary_panel"],
               identity_load="t4 N3 S0 (v0.42)" if il is not None else "NOT AVAILABLE (t4 files missing)")
    inp = {"ans": An["cep"], "design": design, "brands": brands, "panel": panel, "P": P, "flags": flags,
           "defunct": defunct, "il": il, "texts": texts, "a_doc": a_doc, "pablo_decision": decision,
           "a_sha256": rec["paper_A_verdicts_sha256"]}
    return inp, unit_rows, rec


def run_real(paths=None, n_perm=N_PERM, gap_b=GAP_B, guards=True):
    """--run: guards (section 9), load, B-P0 and B-P1, score once, write outputs/."""
    paths = dict(REAL_PATHS, **(paths or {}))
    if guards:
        real_run_guards()
    p0 = parity_b_p0()
    if not p0["passed"]:
        raise Refused(f"B-P0 failed: the imported Paper A scorer is not the locked file: {p0}")
    inp, unit_rows, rec = load_real(paths)
    out = Path(paths["out"])
    out.mkdir(parents=True, exist_ok=True)
    if "ans" not in inp:
        doc = score_b(inp)
        doc["inputs"] = rec
        (out / "v119_not_run.json").write_text(json.dumps(clean(doc), indent=2) + "\n", encoding="utf-8")
        return doc
    _t, cov = cov_map_for(inp["ans"], inp["brands"], inp["design"]["ceps"], inp["panel"], A.FLOOR_FULL)
    p1 = parity_b_p1(cov, unit_rows)
    if not p1["passed"]:
        raise Refused(f"B-P1 failed: Cov* does not reproduce Paper A's unit table: {json.dumps(clean(p1))[:1500]}")
    doc = score_b(inp, n_perm, gap_b)
    if Path(paths.get("il_t1", "")).is_file():
        inp["il_t1"] = load_il_t1(paths["il_t1"])
        rec["il_t1_sha256"] = sha256(paths["il_t1"])
    doc["sensitivities"] = sensitivities(inp, doc["verdict_summary"], n_perm, gap_b, only=paths.get("only_sens"))
    doc["verdict_changes_under_sensitivities"] = {k: v["verdict_changes"] for k, v in doc["sensitivities"].items()
                                                  if v["verdict_changes"]}
    doc["inputs"] = rec
    doc["parity"] = {"B-P0": p0, "B-P1": p1}
    doc["scorer_sha256"] = sha256(__file__)
    (out / "v119_verdicts.json").write_text(json.dumps(clean(doc), indent=2, ensure_ascii=False, allow_nan=False) + "\n",
                                            encoding="utf-8")
    return doc


# =========================================================================== synthetic worlds (dry run, tests)
SIZES = {"v0.19": 16, "v0.20": 24, "v0.21": 24, "v0.22": 24, "v0.23": 24}
DEFUNCT = tuple(A.DEFUNCT)


STRENGTH = {"weak": {"type_bonus": 1.5, "il_sigma": 0.6, "flag_sigma": 1.4},
            "strong": {"type_bonus": 3.0, "il_sigma": 1.6, "flag_sigma": 1.4}}


def synthetic_world(effects, seed, design=None, panel=None, models_shift=0.2, strength="strong"):
    """Fake data shaped like Paper A's analysis set: answer index {(sub, model, CEP, run): brands}, Paper A's real
    probe design (14 CEPs per category, halves, W), N3, P comparator, recall-floor flags, trio IL, defunct texts and a
    Paper A verdict document (PASS). effects=True builds in: flagged brands situation-bound; IL lowers breadth and
    raises with-whom / how-feeling occupancy; 60% of brands tied to one cue type; breadth varies stably across brands;
    defunct brands concentrated in 'when' situations. effects=False: situation-blind naming throughout."""
    rng = np.random.default_rng(seed)
    st = STRENGTH[strength]
    design = design or A.probe_design(A.load_probes())
    panel = panel or list(A.PANELS["N3"])
    brands, ans, P, flags, il, texts = {}, {}, {}, {}, {}, {}
    for sub, nb in SIZES.items():
        names = [f"{sub}-b{i:02d}" for i in range(nb)]
        if sub == "v0.22":
            names = names[:nb - len(DEFUNCT)] + list(DEFUNCT)
        brands[sub] = names
        ceps = design["ceps"][sub]
        d = rng.uniform(-0.8, 0.8, len(ceps))
        a = {b: rng.uniform(-2.6, -0.2) for b in names}
        med = np.median([a[b] for b in names if b not in DEFUNCT])
        ilz = {b: rng.normal() for b in names}
        typ = {b: (rng.choice(["why", "with whom", "how feeling"]) if (effects and rng.random() < 0.6) else None)
               for b in names}
        u = {}
        for b in names:
            fl = a[b] < med
            flags[(sub, b)] = bool(fl) if b not in DEFUNCT else True
            sig = 0.0
            if effects:
                sig = 0.25 + st["flag_sigma"] * fl + (st["il_sigma"] * max(ilz[b], 0.0) if sub in TRIO else 0.0)
            u[b] = sig * rng.normal(size=len(ceps))
            P[(sub, b)] = 100.0 * A._expit(a[b] + rng.normal(0, 0.3))
            if sub in TRIO:
                il[(sub, b)] = {"il": 0.15 * ilz[b], "pi_hat": float(A._expit(a[b]))}
        for m_i, m in enumerate(panel):
            ms = rng.normal(0, models_shift)
            for j, p in enumerate(ceps):
                w = design["w"][p]
                for r in A.RUNS:
                    named = set()
                    for b in names:
                        if b in DEFUNCT:
                            lo = (-6.0 + (5.0 if w == "when" else 0.0)) if effects else -3.0
                            if rng.random() < A._expit(lo):
                                named.add(b)
                            continue
                        x = a[b] + d[j] + ms + u[b][j]
                        if effects and typ[b] == w:
                            x += st["type_bonus"]
                        if effects and sub in TRIO and w in SE_CUES:
                            x += 0.9 * ilz[b]
                        if rng.random() < A._expit(x):
                            named.add(b)
                    ans[(sub, m, p, r)] = frozenset(named)
                    if sub == "v0.22":
                        texts[(sub, m, p, r)] = " ".join(
                            f"{b} (discontinued years ago)" if (effects and rng.random() < 0.5) else f"Consider {b}."
                            for b in sorted(named))
    a_doc = {"paper_A_verdict": {"verdict": "PASS", "legs": {h: "CONFIRMED" for h in A.PRIMARY_LEGS}},
             "primary_panel": "N3"}
    return {"ans": ans, "design": design, "brands": brands, "panel": panel, "P": P, "flags": flags,
            "defunct": DEFUNCT, "il": il, "texts": texts, "a_doc": a_doc, "pablo_decision": None}


EXPECTED = {
    "effects": {"H32_SetSampling": "CONFIRMED", "H34_Floor_Signature": "CONFIRMED", "H34_Defunct_Occupancy": "CONFIRMED",
                "H35_IL_Coverage": "CONFIRMED", "H35_IL_CueType": "CONFIRMED", "H36_Profile_Replication": "CONFIRMED"},
    "null": {"H32_SetSampling": "FALSIFIED", "H32_CueType": "CONFIRMED", "H34_Floor_Signature": "FALSIFIED",
             "H34_Defunct_Occupancy": "FALSIFIED", "H35_IL_Coverage": "FALSIFIED", "H36_Profile_Replication": "FALSIFIED"},
    # power illustration: the r0 first world (weaker type and identity-load effects); only #32 and #34 are built strong
    "effects_weak": {"H32_SetSampling": "CONFIRMED", "H34_Floor_Signature": "CONFIRMED",
                     "H34_Defunct_Occupancy": "CONFIRMED"},
}


def clean(o):
    return A._clean(o)


def dry_run(out_dir, n_perm, gap_b, seed=SEEDS["dry_run"]):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rec = {"phase": PHASE_ID, "kind": "dry run on synthetic worlds (no real answer read; no model call)",
           "draws": {"permutation": n_perm, "gap_reference": gap_b}, "worlds": {},
           "scorer_sha256": sha256(__file__), "paper_A_scorer": parity_b_p0()}
    import time
    for i, (name, eff, strength) in enumerate((("effects", True, "strong"), ("null", False, "strong"),
                                               ("effects_weak", True, "weak"))):
        t0 = time.time()
        world = synthetic_world(eff, seed + i, strength=strength)
        doc = score_b(world, n_perm, gap_b)
        exp = EXPECTED[name]
        got = doc["verdict_summary"]
        checks = {h: {"expected": v, "got": got.get(h), "as_built": got.get(h) == v} for h, v in exp.items()}
        rec["worlds"][name] = {"seed": seed + i, "runtime_s": round(time.time() - t0, 1), "verdicts": got,
                               "built_in_checks": checks, "all_as_built": all(c["as_built"] for c in checks.values()),
                               "detail": doc}
    for name, how in (("not_run_FAIL", "FAIL"), ("not_run_MARGINAL_no_decision", "MARGINAL")):
        doc = score_b({"a_doc": {"paper_A_verdict": {"verdict": how, "legs": {"H1_Sep_Presence": "MARGINAL"}}}}, n_perm)
        rec["worlds"][name] = {"verdicts": {"status": doc["status"]}, "statistics": doc.get("statistics")}
    (out_dir / "dry_run_v1_19.json").write_text(json.dumps(clean(rec), indent=2, ensure_ascii=False) + "\n",
                                                encoding="utf-8")
    return rec


def main():
    ap = argparse.ArgumentParser(description="AIAS v1.19 Coverage Paper B (re-analysis) scorer skeleton")
    ap.add_argument("--dry-run", metavar="DIR", help="score two synthetic worlds and the not-run paths; no real data")
    ap.add_argument("--draws", type=int, default=N_PERM)
    ap.add_argument("--gap-b", type=int, default=GAP_B)
    ap.add_argument("--run", action="store_true", help="score the real record (refuses before the lock)")
    a = ap.parse_args()
    try:
        if a.dry_run:
            rec = dry_run(a.dry_run, a.draws, a.gap_b)
            for name, w in rec["worlds"].items():
                print(name, json.dumps(clean(w["verdicts"])), "as built:" if "all_as_built" in w else "",
                      w.get("all_as_built", ""))
            return 0
        if a.run:
            doc = run_real(n_perm=N_PERM, gap_b=GAP_B)
            print(json.dumps(clean(doc.get("verdict_summary") or {"status": doc.get("status")}), indent=1))
            return 0
    except Refused as e:
        print(f"[v1.19] REFUSED: {e}", file=sys.stderr)
        return 3
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
