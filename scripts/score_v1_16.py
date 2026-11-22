#!/usr/bin/env python3
"""
score_v1_16.py - AIAS v1.16, Ranking: the last measure. Co-mention precedence (a Bradley-Terry strength
fitted only on the order of brands named together in the same answer), tested once on the archived
answers (t1, t2, t3 omnibus waves and the t4 wave) under a gate fixed in advance.

STATUS: r1 (2026-11-12), to be locked at tag v1.16-prereg-r1. Rules transcribed from
osf/methodology/v1_16/prereg/PRE_REGISTRATION_v1_16.md (section cited inline).

Consequence clause (section 8, Pablo, Wed Nov 11, 2026, 11:22 pm): if the gate does not PASS, Ranking is
reported as part of Presence and not as a separate AIAS component, and there is no further Ranking redesign.

What is reused and what is new
  * Inputs are archived and already hashed: v1.10's 31 rank tables (pinned in v1.10's verdicts file), the
    locked P / C* table of the archived waves (osf/aias_2_0/aias_2_0_profiles.csv), and v1.14's Stage 1
    output for t4 (rank table and unit table with P and C* at t4). No answer is re-extracted.
  * Pooled within-category Spearman (centred ranks), permutation null, bootstrap CI, bands, n floor and
    the stability verdict are v1.10's, imported unchanged from scripts/score_v1_10.py.
  * New: the statistic PREC (section 3), the four-wave separability rule, the shuffle null for PREC,
    first-position concentration, and the gate with the consequence clause (section 8).

Modes
  --parity            input parity (allowed before the lock): pins, counts and n's only; no PREC on real data
  --dry-run           full analysis on synthetic data with known answers (three worlds); writes dryrun/
  --lock-manifest     writes prereg/LOCK_MANIFEST_v1_16.sha256 (does not tag)
  --verify-lock       checks the lock manifest
  --write-anchor      after the tag is pushed: writes anchor/git_anchor_v1_16.json
  --run               the confirmatory analysis (refuses before the lock; runs once)
No network, no model calls, no paid API.
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import io
import itertools
import json
import math
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_v1_10 as R  # noqa: E402  (v1.10's locked code, imported unchanged)
import score_v1_14 as S  # noqa: E402  (v1.14's locked code: rank-table reader, Halt)

# ===========================================================================
# TRANSCRIBED CONSTANTS
# ===========================================================================
PHASE_ID = "v1.16"
PREREG_TAG = "v1.16-prereg-r1"
ROOT = Path(__file__).resolve().parents[1]
V116 = "osf/methodology/v1_16"
ANCHOR_FILE = ROOT / V116 / "anchor/git_anchor_v1_16.json"
LOCK_MANIFEST = ROOT / V116 / "prereg/LOCK_MANIFEST_v1_16.sha256"
PARITY_FILE = ROOT / V116 / "prereg/input_parity_v1_16.json"
DRY_DIR = ROOT / V116 / "dryrun"
OUT_DIR = ROOT / V116 / "outputs"
RESULTS_FILE = OUT_DIR / "results_v1_16.json"

STAT = "PREC"
RATING_FLOOR = R.RATING_FLOOR          # 6 rankable mentions (v1.10, v1.14)
PRIOR = 1.0                            # section 3.2: one virtual comparison (half win, half loss) vs a reference
SEP_CONF, SEP_FALS = R.SEP_CONF, R.SEP_FALS        # 0.30 / 0.50
STAB_CONF, STAB_FALS = R.STAB_CONF, R.STAB_FALS    # 0.50 / 0.30
N_FLOOR_UNITS = R.N_FLOOR_UNITS        # 30
MIN_DETERMINED_WAVES = 3               # section 6.1: H1/H2 need >= 3 of the 4 waves determined
SEP_WAVES = ["t1", "t2", "t3", "t4"]
N_PERM, N_SHUFFLE = R.N_PERM, R.N_SHUFFLE          # 10,000 each
MQ7_MAX = R.NEG_CONTROL_MAX            # 0.20
MQ9_MAX_SHARE = 0.10                   # MQ9: flag if > 10% of units at the floor lie outside the main component
SEEDS = {"H1": 116001, "H2": 116002, "H3": 116003, "H4_S1": 116004, "H5": 116005, "SHUFFLE": 116010,
         "BOOT": R.SEEDS["BOOT"], "E3": 116020}
DENON = ("v0.19", "Denon")
# Cheil Worldwide / Iris agency ties (v0.62 DEVIATIONS Entry 0, Part F; v0.62 params COI_FLAGGED); in the
# v1.10 registry key of v0.23, Jack Daniel's is S03 (osf/methodology/v1_10/registries/v0_23_registry_v1_10.json)
COI_CHEIL = (("v0.20", "Eucerin"), ("v0.22", "BMW"), ("v0.22", "Bentley"), ("v0.22", "Chevrolet"), ("v0.23", "S03"))

# Pinned inputs (section 4): path relative to the repository root -> SHA-256. Verified before any read.
V110_VERDICTS_REL = "osf/methodology/v1_10/outputs/v1_10_verdicts.json"
V110_OUTPUTS_REL = "osf/methodology/v1_10/outputs"
PROFILES_REL = "osf/aias_2_0/aias_2_0_profiles.csv"
T4_RANK_REL = "osf/methodology/v1_14/outputs/stage1/rank_table_t4_v1_14.csv"
T4_STAGE1_REL = "osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json"
INPUT_PINS = {
    V110_VERDICTS_REL: "d4250ba79a6acfb9e211dbc561311da9fc07581bebf871dea3dbe149d6bdcb28",
    PROFILES_REL: "022ef56ecad9ddb60ad9ce0a2129698fd84ee9656630500e30b05f1e4b7e8c6e",
    T4_RANK_REL: "5e6286589f26c802da17b87db47b002707225dbea3950a093d1b63a6f1a0a23d",
    T4_STAGE1_REL: "4de97fea86fd7c74f990ba4bdecd43c19aa52afc60278676624374a164f68e2f",
}
# Numbers already published by v1.14 Stage 1 (stage1_v1_14.log) that the t4 loader must reproduce (parity).
V114_PUBLISHED = {"answers": 540, "rankable_rows_S0": 1641, "rankable_rows_S1": 1375, "units_rated_S0": 71,
                  "H1_n": 71, "H2_n": 70}

LOCKED_FILES = [
    V116 + "/prereg/PRE_REGISTRATION_v1_16.md",
    V116 + "/prereg/input_parity_v1_16.json",
    V116 + "/prereg/precision_note_v1_16.json",
    V116 + "/scripts/precision_note_v1_16.py",
    V116 + "/README.md",
    V116 + "/anchor/DEVIATIONS.md",
    V116 + "/dryrun/dryrun_v1_16.json",
    V116 + "/dryrun/dryrun_run_v1_16.log",
    V116 + "/dryrun/check_world_A_versions.py",
    V116 + "/dryrun/check_world_A_versions.log",
    "scripts/score_v1_16.py",
    "scripts/test_score_v1_16.py",
    "scripts/score_v1_14.py",
    "scripts/score_v1_10.py",
    V110_VERDICTS_REL,
    PROFILES_REL,
    T4_RANK_REL,
    T4_STAGE1_REL,
] + [f"{V110_OUTPUTS_REL}/rank_tables/OMNI_{w}_{s}.csv" for w in ("t1", "t2", "t3") for s in R.OMNI]

Halt = S.Halt


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ===========================================================================
# THE STATISTIC (section 3): co-mention precedence, PREC
# ===========================================================================


def fit_bt(W: np.ndarray, prior: float = PRIOR, tol: float = 1e-10, max_iter: int = 500) -> np.ndarray:
    """Bradley-Terry log-strengths theta from a win matrix W (W[i, j] = times i was named before j in an
    answer naming both; a tie adds 1/2 to each side). Penalised maximum likelihood: every brand also plays
    `prior` virtual comparisons (half won, half lost) against a reference brand of log-strength 0, so every
    estimate is finite and theta is anchored at 0 (section 3.2). Newton-Raphson with step halving; the
    objective is strictly concave for prior > 0. Deterministic."""
    W = np.asarray(W, float)
    n = W.shape[0]
    if n == 0:
        return np.zeros(0)
    N = W + W.T
    th = np.zeros(n)

    def obj(t):
        d = t[:, None] - t[None, :]
        return float((W * -np.logaddexp(0.0, -d)).sum() + prior / 2 * t.sum() - prior * np.logaddexp(0.0, t).sum())

    f = obj(th)
    for _ in range(max_iter):
        d = th[:, None] - th[None, :]
        s = 1.0 / (1.0 + np.exp(-d))
        sv = 1.0 / (1.0 + np.exp(-th))
        g = (W - N * s).sum(1) + prior / 2 - prior * sv
        A = N * s * (1 - s)                       # off-diagonal curvature
        Hn = np.diag(A.sum(1) + prior * sv * (1 - sv)) - A    # = -Hessian, positive definite
        step = np.linalg.solve(Hn, g)
        lam = 1.0
        while True:
            cand = th + lam * step
            fc = obj(cand)
            if fc >= f - 1e-12 or lam < 1e-8:
                break
            lam /= 2
        th, f = cand, fc
        if np.max(np.abs(lam * step)) < tol:
            break
    return th


def _components(adj: np.ndarray) -> np.ndarray:
    """Component label of every node of an undirected graph (boolean adjacency)."""
    n = adj.shape[0]
    lab = -np.ones(n, int)
    c = 0
    for i in range(n):
        if lab[i] >= 0:
            continue
        stack = [i]
        lab[i] = c
        while stack:
            k = stack.pop()
            for j in np.flatnonzero(adj[k]):
                if lab[j] < 0:
                    lab[j] = c
                    stack.append(j)
        c += 1
    return lab


class PairData:
    """The comparisons of one category in one panel x wave x condition: every rankable answer contributes,
    for every pair of registry brands it names, one comparison won by the brand with the smaller competition
    min-rank k_min (a tie: half to each). Weight per comparison: 1 (primary) or 1/(n_named - 1) (sensitivity
    S_w). Kept as arrays so that the within-answer order shuffle (section 6.3) is fast."""

    def __init__(self, rows, weighting: str = "pairs"):
        by_ans = collections.defaultdict(dict)
        for r in rows:
            by_ans[str(r["answer_id"])].setdefault(r["brand"], int(r["k_min"]))   # first occurrence wins (E4)
        self.brands = sorted({b for a in by_ans.values() for b in a})
        self.idx = {b: i for i, b in enumerate(self.brands)}
        ra, rb, wt, ka, kb, row_a, row_b = [], [], [], [], [], [], []
        self.n_rows = 0
        self.count = np.zeros(len(self.brands), int)
        self.answer_of_row = []
        for ai, aid in enumerate(sorted(by_ans)):
            items = sorted(by_ans[aid].items())
            m = len(items)
            base = self.n_rows
            for b, _k in items:
                self.count[self.idx[b]] += 1
                self.answer_of_row.append(ai)
            self.n_rows += m
            if m < 2:
                continue
            w = 1.0 if weighting == "pairs" else 1.0 / (m - 1)
            for (p, (b1, k1)), (q, (b2, k2)) in itertools.combinations(enumerate(items), 2):
                ra.append(self.idx[b1]); rb.append(self.idx[b2]); wt.append(w)
                ka.append(k1); kb.append(k2); row_a.append(base + p); row_b.append(base + q)
        self.ra, self.rb = np.array(ra, np.int64), np.array(rb, np.int64)
        self.wt, self.ka, self.kb = np.array(wt, float), np.array(ka, float), np.array(kb, float)
        self.row_a, self.row_b = np.array(row_a, np.int64), np.array(row_b, np.int64)
        self.n_answers = len(by_ans)
        self.answer_of_row = np.array(self.answer_of_row, np.int64)

    def win_matrix(self, ka=None, kb=None) -> np.ndarray:
        ka = self.ka if ka is None else ka
        kb = self.kb if kb is None else kb
        n = len(self.brands)
        a_first = (ka < kb).astype(float) + 0.5 * (ka == kb)
        W = np.bincount(self.ra * n + self.rb, weights=self.wt * a_first, minlength=n * n)
        W += np.bincount(self.rb * n + self.ra, weights=self.wt * (1.0 - a_first), minlength=n * n)
        return W.reshape(n, n)

    def shuffled_keys(self, rng):
        """Within-answer order shuffle: every answer's named brands get a uniformly random order (no ties);
        the named set and the list length are kept (= score_v1_10.shuffle_answer_ranks)."""
        key = rng.random(self.n_rows)
        return key[self.row_a], key[self.row_b]

    def main_component(self) -> np.ndarray:
        n = len(self.brands)
        adj = np.zeros((n, n), bool)
        if len(self.ra):
            adj[self.ra, self.rb] = True
            adj[self.rb, self.ra] = True
        lab = _components(adj)
        if not n:
            return np.zeros(0, bool)
        sizes = np.bincount(lab)
        return lab == int(np.argmax(sizes))     # ties between equal largest components: the lowest label


def prec_units(rows, floor: int = RATING_FLOOR, prior: float = PRIOR, weighting: str = "pairs",
               pair_data: dict | None = None) -> dict:
    """{(category, brand): {"n_ranked", "n_comparisons", "PREC", "main_component", "rated"}} for the rows of
    ONE panel x wave x condition (all rankable mentions pooled over models, runs and questions). A unit is
    rated iff it has >= `floor` rankable mentions and lies in the largest connected component of its
    category's comparison graph (section 3.3). Brands below the floor still enter the fit as rivals."""
    by_cat = collections.defaultdict(list)
    for r in rows:
        by_cat[r["category"]].append(r)
    out = {}
    for cat in sorted(by_cat):
        pd = pair_data[cat] if pair_data is not None else PairData(by_cat[cat], weighting)
        th = fit_bt(pd.win_matrix(), prior)
        mc = pd.main_component()
        W = pd.win_matrix()
        ncomp = (W + W.T).sum(1)
        for b, i in pd.idx.items():
            out[(cat, b)] = {"n_ranked": int(pd.count[i]), "n_comparisons": float(ncomp[i]), "PREC": float(th[i]),
                             "main_component": bool(mc[i]),
                             "rated": bool(pd.count[i] >= floor and mc[i])}
    return out


def pair_data_by_cat(rows, weighting: str = "pairs") -> dict:
    by_cat = collections.defaultdict(list)
    for r in rows:
        by_cat[r["category"]].append(r)
    return {c: PairData(v, weighting) for c, v in sorted(by_cat.items())}


def first_position_concentration(rows) -> dict:
    """Section 7 (moderator): per category, over rankable answers, the modal first brand (the brand most
    often at k_min = 1; ties -> alphabetical first) and the share of answers in which it is first."""
    first = collections.defaultdict(lambda: collections.defaultdict(set))
    answers = collections.defaultdict(set)
    for r in rows:
        answers[r["category"]].add(str(r["answer_id"]))
        if int(r["k_min"]) == 1:
            first[r["category"]][r["brand"]].add(str(r["answer_id"]))
    out = {}
    for c in sorted(answers):
        n = len(answers[c])
        if not first[c]:
            out[c] = {"modal_first_brand": None, "share": 0.0, "rankable_answers": n}
            continue
        best = sorted(first[c].items(), key=lambda kv: (-len(kv[1]), kv[0]))[0]
        out[c] = {"modal_first_brand": best[0], "share": len(best[1]) / n, "rankable_answers": n}
    return out


# ===========================================================================
# TESTS AND VERDICT RULES (sections 6 and 8)
# ===========================================================================

VERDICTS = ("CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED")


def sep_one_wave(U: dict, Y: dict, seed: int, excl_units=(), excl_sub=(), boot=True, stat=STAT) -> dict:
    """rho_w(PREC, Y) on one wave: rated units with Y defined; categories with >= 5 units (v1.10)."""
    keys = sorted(k for k, s in U.items() if s["rated"] and k not in excl_units and k[0] not in excl_sub
                  and Y.get(k) is not None and math.isfinite(Y[k]))
    res = R.corr_test([Y[k] for k in keys], [U[k][stat] for k in keys], [k[0] for k in keys], seed, "two",
                      boot=boot)
    res["single_wave_reading"] = R.verdict_single_separability(res["rho"], res["n"])
    return res


def verdict_sep_multi(by_wave: dict) -> str:
    """H1 / H2 (section 6.1): {wave: (rho, n)} over t1-t4. A wave is determined iff n >= 30 and rho is
    finite. UNDETERMINED if fewer than 3 waves are determined; FALSIFIED if |rho| >= .50 at any determined
    wave; CONFIRMED if |rho| <= .30 at every determined wave; MARGINAL otherwise. Unrounded values."""
    ok = {w: r for w, (r, n) in by_wave.items() if n >= N_FLOOR_UNITS and r is not None and np.isfinite(r)}
    if len(ok) < MIN_DETERMINED_WAVES:
        return "UNDETERMINED"
    if any(abs(r) >= SEP_FALS for r in ok.values()):
        return "FALSIFIED"
    if all(abs(r) <= SEP_CONF for r in ok.values()):
        return "CONFIRMED"
    return "MARGINAL"


def separability(Uw: dict, Yw: dict, seed: int, excl_units=(), excl_sub=(), boot=True, stat=STAT) -> dict:
    per = {w: sep_one_wave(Uw[w], Yw.get(w, {}), seed, excl_units, excl_sub, boot, stat) for w in SEP_WAVES
           if w in Uw}
    return {"verdict": verdict_sep_multi({w: (v["rho"], v["n"]) for w, v in per.items()}), "per_wave": per}


def stability(rows_a, rows_b, seed_perm: int, n_shuffle: int | None = None, n_perm: int | None = None,
              floor: int = RATING_FLOOR, prior: float = PRIOR, weighting: str = "pairs", boot=True,
              nulls=True) -> dict:
    """H3 (t1 -> t2) and H5 (t2 -> t3): rho_w(PREC_a, PREC_b) over units rated in both waves (categories with
    >= 5 such units). Nulls: (a) PREC_b permuted within category, one-sided (v1.10); (b) within-answer order
    shuffle of both waves, PREC refitted, one-sided (hits: rho >= observed). v1.10's stability verdict.
    The mean shuffled rho is the negative control MQ7 (section 9)."""
    n_shuffle = N_SHUFFLE if n_shuffle is None else n_shuffle
    pa, pb = pair_data_by_cat(rows_a, weighting), pair_data_by_cat(rows_b, weighting)
    Ua = prec_units(rows_a, floor, prior, pair_data=pa)
    Ub = prec_units(rows_b, floor, prior, pair_data=pb)
    keys = sorted(k for k in Ua if Ua[k]["rated"] and k in Ub and Ub[k]["rated"])
    g = np.array([k[0] for k in keys])
    if len(g):
        m = R.keep_categories(g)
        keys, g = [k for k, ok in zip(keys, m) if ok], g[m]
    n = len(keys)
    x = np.array([Ua[k][STAT] for k in keys], float)
    y = np.array([Ub[k][STAT] for k in keys], float)
    rho = R.pooled_within_rho(x, y, g) if n >= 3 else float("nan")
    res = {"rho": rho, "n": n, "units_per_category": dict(collections.Counter(g.tolist()))}
    if not nulls:
        return res
    res["p_perm"] = R.perm_p(x, y, g, rho, seed_perm, "one", n_perm) if n >= 3 else float("nan")
    res["perm_seed"] = seed_perm
    res["ci90"] = list(R.boot_ci(x, y, g, SEEDS["BOOT"])) if (boot and n >= 3) else [float("nan")] * 2
    if n >= 3 and np.isfinite(rho):
        rng = np.random.default_rng(SEEDS["SHUFFLE"])
        gidx = R._group_index(g)
        cats = sorted(set(pa) | set(pb))
        hits, vals = 0, []
        for _ in range(n_shuffle):
            th = {}
            for side, P in (("a", pa), ("b", pb)):
                for c in cats:
                    if c not in P:
                        continue
                    d = P[c]
                    ka, kb = d.shuffled_keys(rng)
                    t = fit_bt(d.win_matrix(ka, kb), prior)
                    for b, i in d.idx.items():
                        th[(side, c, b)] = t[i]
            xs = np.array([th[("a",) + k] for k in keys])
            ys = np.array([th[("b",) + k] for k in keys])
            r = R._pearson(R._within_ranks_idx(xs, gidx), R._within_ranks_idx(ys, gidx))
            vals.append(r)
            hits += r >= rho - 1e-12
        res["p_shuffle"] = (hits + 1) / (n_shuffle + 1)
        res["shuffle_draws"], res["shuffle_seed"] = n_shuffle, SEEDS["SHUFFLE"]
        res["shuffled_mean_rho"] = float(np.nanmean(vals))
    else:
        res["p_shuffle"] = float("nan")
        res["shuffled_mean_rho"] = float("nan")
    res["verdict"] = R.verdict_stability(rho, res["p_perm"], res["p_shuffle"], n)
    return res


def gate(h1: str, h2: str, h3: str, h4_s1: str | None) -> str:
    """GATE (section 8): FAIL if any of H1, H2, H3 FALSIFIED; else UNDETERMINED if any UNDETERMINED; else
    PASS if all three CONFIRMED and H4_S1 not FALSIFIED; else MARGINAL."""
    trio = (h1, h2, h3)
    if "FALSIFIED" in trio:
        return "FAIL"
    if "UNDETERMINED" in trio:
        return "UNDETERMINED"
    if all(v == "CONFIRMED" for v in trio):
        return "MARGINAL" if h4_s1 == "FALSIFIED" else "PASS"
    return "MARGINAL"


CONSEQUENCE_PASS = ("PASS: Ranking (co-mention precedence) may be reported as a separate AIAS component; Ranking "
                    "Paper B and the AIAS 3.0 calibration may each be pre-registered.")
CONSEQUENCE_NOT_PASS = ("NOT PASS: Ranking is reported as part of Presence and not as a separate AIAS component. "
                        "There is no further Ranking redesign.")


def consequence(gate_verdict: str) -> str:
    """Section 8, the consequence clause: every outcome other than PASS (FAIL, MARGINAL, UNDETERMINED)."""
    return CONSEQUENCE_PASS if gate_verdict == "PASS" else CONSEQUENCE_NOT_PASS


# ===========================================================================
# INPUTS (section 4): pinned files, loaders
# ===========================================================================


def verify_pins(root: Path = ROOT, pins: dict | None = None) -> dict:
    """Every pinned input must match its SHA-256 (a mismatch halts). Returns {path: sha256}."""
    pins = INPUT_PINS if pins is None else pins
    got = {}
    for rel, want in pins.items():
        p = Path(root) / rel
        if not p.exists():
            raise Halt(f"missing pinned input: {rel}")
        h = sha256_file(p)
        if h != want:
            raise Halt(f"pinned input changed: {rel} (sha256 {h[:12]}..., pinned {want[:12]}...)")
        got[rel] = h
    return got


def read_t4_rank_table(path: Path) -> dict:
    """v1.14 Stage 1's t4 rank table -> {"rows": {(condition, rule): [row]}, "answers": {...}}. Row fields as
    score_v1_14.wave_rows writes them (only rankable answers' named brands with a position)."""
    rows = collections.defaultdict(list)
    answers, ok, rankable = set(), collections.defaultdict(set), collections.defaultdict(set)
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            answers.add(r["answer_id"])
            if r["status"] != "ok":
                continue
            ok[r["condition"]].add(r["answer_id"])
            if r["rankable"] == "1":
                rankable[r["condition"]].add(r["answer_id"])
            if r["brand"] and r["k_mid"] != "" and r["rankable"] == "1":
                rows[(r["condition"], r["rule"])].append({
                    "panel": "N3", "wave": "t4", "category": r["category"], "answer_id": r["answer_id"],
                    "model": r["model"], "run_idx": int(r["run_idx"]), "brand": r["brand"],
                    "k_mid": float(r["k_mid"]), "k_min": int(r["k_min"]), "n": int(r["n_named"])})
    return {"rows": dict(rows), "answers": len(answers),
            "answers_with_text": {c: len(v) for c, v in ok.items()},
            "rankable_answers": {c: len(v) for c, v in rankable.items()}}


def read_t4_comparators(path: Path) -> dict:
    """P_S0, C*_S0 and P_S1 at t4 (v1.14 section 5.2, the definition shared with v1.12 and v1.13), from v1.14
    Stage 1's unit table. Units never named in a rankable t4 answer are absent (they cannot be rated)."""
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    P0, C0, P1 = {}, {}, {}
    for u in d["units"]:
        k = (u["substrate"], u["brand"])
        if u.get("P_S0") is not None:
            P0[k] = float(u["P_S0"])
        if u.get("C_star_S0") is not None:
            C0[k] = float(u["C_star_S0"])
        if u.get("P_S1") is not None:
            P1[k] = float(u["P_S1"])
    return {"P_S0": P0, "C_S0": C0, "P_S1": P1, "rank_table_t4_sha256": d.get("rank_table_t4_sha256"),
            "stage1_verdict": d.get("STAGE1_VERDICT"), "units_listed": len(d["units"]),
            "published_units_rated_S0": sum(1 for u in d["units"] if u.get("rated_S0")),
            "published_H1_n": d["H1_Sep_Presence"]["n"], "published_H2_n": d["H2_Sep_Consistency"]["n"]}


def load_inputs(root: Path = ROOT, pins: dict | None = None) -> dict:
    """All inputs of v1.16, after the pins are verified. Archived waves: v1.10's rank tables (each verified
    against the SHA-256 recorded in v1.10's verdicts file by score_v1_14.load_v110_tables) and the locked
    P / C* table. t4: v1.14 Stage 1's rank table (its SHA-256 must equal the one Stage 1 recorded) and unit
    table."""
    root = Path(root)
    hashes = verify_pins(root, pins)
    tables, v110 = S.load_v110_tables(root / V110_VERDICTS_REL, root / V110_OUTPUTS_REL)
    with open(root / PROFILES_REL, newline="", encoding="utf-8") as fh:
        prof_rows = list(csv.DictReader(fh))
    P, C, NM = R.parse_profiles(prof_rows)
    t4 = read_t4_rank_table(root / T4_RANK_REL)
    comp4 = read_t4_comparators(root / T4_STAGE1_REL)
    if comp4["rank_table_t4_sha256"] != sha256_file(root / T4_RANK_REL):
        raise Halt("t4 rank table differs from the one v1.14 Stage 1 recorded")
    rows = {}
    for rule in R.RULES:
        for w in ("t1", "t2", "t3"):
            rows[(w, "S0", rule)] = S._omni_rows(tables, w, rule)
        for cond in ("S0", "S1"):
            rows[("t4", cond, rule)] = t4["rows"].get((cond, rule), [])
    Pw = {w: dict(P[w]) for w in ("t1", "t2", "t3")}
    Cw = {w: dict(C[w]) for w in ("t1", "t2", "t3")}
    Pw["t4"], Cw["t4"] = comp4["P_S0"], comp4["C_S0"]
    sizes = collections.Counter(r["substrate"] for r in prof_rows if r["wave"] == "t1")
    return {"rows": rows, "P": Pw, "C": Cw, "P_t4_S1": comp4["P_S1"], "tables": tables, "v110": v110,
            "t4_meta": t4, "t4_comp_meta": comp4, "category_size": dict(sizes), "hashes": hashes,
            "rank_table_hashes": {n: e["sha256"] for n, e in v110["rank_tables"].items()}}


# ===========================================================================
# THE ANALYSIS (sections 6, 7, 9, 10) - one function for the real run and the dry run
# ===========================================================================


def _cat_spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 3:
        return float("nan")
    return R._pearson(R._rankdata(x[m]), R._rankdata(y[m]))


def analyse(inp: dict, log=print, n_shuffle: int | None = None, n_perm: int | None = None, boot: bool = True,
            sensitivities: bool = True) -> dict:
    rows = inp["rows"]
    P, C = inp["P"], inp["C"]
    U = {w: prec_units(rows[(w, "S0", "lead_item")]) for w in SEP_WAVES}
    U4s1 = prec_units(rows[("t4", "S1", "lead_item")])
    log(f"[v1.16] PREC fitted: rated units " + ", ".join(f"{w} {sum(s['rated'] for s in U[w].values())}"
                                                       for w in SEP_WAVES)
        + f", t4 S1 {sum(s['rated'] for s in U4s1.values())}")
    res = {"phase": PHASE_ID, "statistic": STAT, "rating_floor": RATING_FLOOR, "prior": PRIOR, "seeds": SEEDS,
           "draws": {"perm": N_PERM if n_perm is None else n_perm,
                     "shuffle": N_SHUFFLE if n_shuffle is None else n_shuffle}}
    h1 = separability(U, P, SEEDS["H1"], boot=boot)
    h2 = separability(U, C, SEEDS["H2"], boot=boot)
    if n_perm is not None:   # reduced draws (dry run): recompute permutation p with n_perm
        for h, Y, sd in ((h1, P, SEEDS["H1"]), (h2, C, SEEDS["H2"])):
            for w, v in h["per_wave"].items():
                keys = sorted(k for k, s in U[w].items() if s["rated"] and Y.get(w, {}).get(k) is not None
                              and math.isfinite(Y[w][k]))
                x = [Y[w][k] for k in keys]; y = [U[w][k][STAT] for k in keys]; g = np.array([k[0] for k in keys])
                if len(g):
                    m = R.keep_categories(g)
                    x, y, g = np.asarray(x)[m], np.asarray(y)[m], g[m]
                v["p_perm"] = R.perm_p(x, y, g, v["rho"], sd, "two", n_perm) if len(g) >= 3 else float("nan")
    log(f"  H1 " + "  ".join(f"{w} {v['rho']:.4f} (n {v['n']})" for w, v in h1["per_wave"].items())
        + f" -> {h1['verdict']}")
    log(f"  H2 " + "  ".join(f"{w} {v['rho']:.4f} (n {v['n']})" for w, v in h2["per_wave"].items())
        + f" -> {h2['verdict']}")
    log("  H3 t1 -> t2 (permutation and within-answer shuffle nulls) ...")
    h3 = stability(rows[("t1", "S0", "lead_item")], rows[("t2", "S0", "lead_item")], SEEDS["H3"], n_shuffle,
                   n_perm, boot=boot)
    log(f"  H3 rho {h3['rho']:.4f} (n {h3['n']}; p_perm {h3['p_perm']:.4f}; p_shuffle {h3['p_shuffle']:.4f})"
        f" -> {h3['verdict']}")
    h4 = sep_one_wave(U4s1, inp["P_t4_S1"], SEEDS["H4_S1"], boot=boot)
    h4["verdict"] = h4["single_wave_reading"]
    log(f"  H4_S1 rho {h4['rho']:.4f} (n {h4['n']}) -> {h4['verdict']}")
    g = gate(h1["verdict"], h2["verdict"], h3["verdict"], h4["verdict"])
    res.update(H1_Sep_Presence=h1, H2_Sep_Consistency=h2, H3_Retest_t1_t2=h3, H4_Sep_Presence_t4_S1=h4,
               GATE=g, CONSEQUENCE=consequence(g))
    res["MQ7_negative_control"] = {"shuffled_mean_rho_H3": h3.get("shuffled_mean_rho"), "threshold": MQ7_MAX,
                                   "flag": bool(np.isfinite(h3.get("shuffled_mean_rho", float("nan")))
                                                and h3["shuffled_mean_rho"] >= MQ7_MAX)}
    res["MQ9_identification"] = {w: {"units_at_floor": sum(1 for s in U[w].values() if s["n_ranked"] >= RATING_FLOOR),
                                     "at_floor_outside_main_component": sum(1 for s in U[w].values()
                                                                            if s["n_ranked"] >= RATING_FLOOR
                                                                            and not s["main_component"])}
                                 for w in SEP_WAVES}
    res["MQ9_identification"]["flag"] = any(
        v["units_at_floor"] and v["at_floor_outside_main_component"] > MQ9_MAX_SHARE * v["units_at_floor"]
        for v in res["MQ9_identification"].values())
    log(f"  GATE: {g}  ->  {res['CONSEQUENCE']}")
    # ---- secondary: H5 t2 -> t3 (reported; never changes the gate)
    log("  H5 t2 -> t3 (secondary) ...")
    res["H5_Retest_t2_t3"] = stability(rows[("t2", "S0", "lead_item")], rows[("t3", "S0", "lead_item")],
                                       SEEDS["H5"], n_shuffle, n_perm, boot=boot)
    # ---- descriptives
    D = {}
    for w in SEP_WAVES + ["t4_S1"]:
        key = ("t4", "S1", "lead_item") if w == "t4_S1" else (w, "S0", "lead_item")
        Uw = U4s1 if w == "t4_S1" else U[w]
        rr = rows[key]
        D[w] = {"rankable_answers": len({r["answer_id"] for r in rr}), "rankable_rows": len(rr),
                "units_with_rows": len(Uw), "units_rated": sum(s["rated"] for s in Uw.values()),
                "comparisons": float(sum(s["n_comparisons"] for s in Uw.values()) / 2),
                "PREC_rated_distribution": S._dist([s[STAT] for s in Uw.values() if s["rated"]])}
    res["D1_descriptives"] = D
    d4 = {}
    for w in SEP_WAVES:
        V = R.units_cat_brand(rows[(w, "S0", "lead_item")], RATING_FLOOR)
        keys = sorted(k for k in U[w] if U[w][k]["rated"] and k in V and V[k]["rated"])
        d4[w] = {s: R._rho_only([V[k][s] for k in keys], [U[w][k][STAT] for k in keys], [k[0] for k in keys])
                 for s in ("MNP", "MODE")}
    res["D2_PREC_vs_v1_10_and_v1_14_statistics"] = d4
    both = sorted(k for k in U["t4"] if U["t4"][k]["rated"] and k in U4s1 and U4s1[k]["rated"])
    res["D3_PREC_S0_vs_S1_t4"] = R._rho_only([U["t4"][k][STAT] for k in both], [U4s1[k][STAT] for k in both],
                                             [k[0] for k in both])
    # ---- exploratory E1: moderators (category size, first-position concentration)
    E1 = {"cells": []}
    for w in SEP_WAVES:
        fpc = first_position_concentration(rows[(w, "S0", "lead_item")])
        for c in sorted(fpc):
            keys = sorted(k for k, s in U[w].items() if k[0] == c and s["rated"] and P[w].get(k) is not None
                          and math.isfinite(P[w][k]))
            rc = _cat_spearman([P[w][k] for k in keys], [U[w][k][STAT] for k in keys])
            E1["cells"].append({"wave": w, "category": c, "category_size": inp["category_size"].get(c),
                                "first_position_concentration": fpc[c]["share"],
                                "modal_first_brand": fpc[c]["modal_first_brand"],
                                "rankable_answers": fpc[c]["rankable_answers"], "rho_PREC_P": rc, "n": len(keys)})
    cells = [x for x in E1["cells"] if x["n"] >= R.MIN_UNITS_PER_CATEGORY]
    E1["spearman_across_cells"] = {
        "abs_rho_PREC_P_vs_category_size": _cat_spearman([abs(x["rho_PREC_P"]) for x in cells],
                                                         [x["category_size"] for x in cells]),
        "abs_rho_PREC_P_vs_fpc": _cat_spearman([abs(x["rho_PREC_P"]) for x in cells],
                                               [x["first_position_concentration"] for x in cells]),
        "cells": len(cells)}
    Ua, Ub = U["t1"], U["t2"]
    per_cat = []
    for c in sorted({k[0] for k in Ua}):
        keys = sorted(k for k in Ua if k[0] == c and Ua[k]["rated"] and k in Ub and Ub[k]["rated"])
        per_cat.append({"category": c, "category_size": inp["category_size"].get(c), "n": len(keys),
                        "retest_rho_t1_t2": _cat_spearman([Ua[k][STAT] for k in keys], [Ub[k][STAT] for k in keys])})
    E1["retest_by_category"] = per_cat
    res["E1_moderators"] = E1
    # ---- exploratory E3: early panel (v1.10's H4 data, pi_hat), PREC
    x, y, gg = [], [], []
    for name, t in inp.get("tables", {}).items():
        if S._set_role(name) != "early6":
            continue
        Ue = prec_units(t["rows"]["lead_item"])
        T = t["answers_ok"]
        for k, s in sorted(Ue.items()):
            if s["rated"]:
                x.append(sum(1 for a in T if k[1] in t["named"][a]) / len(T))
                y.append(s[STAT])
                gg.append(k[0])
    res["E3_early_panel_pi_hat"] = (R.corr_test(x, y, gg, SEEDS["E3"], "two", boot=False, n_perm=n_perm)
                                    if len(gg) >= 3 else {"rho": None, "n": len(gg)})
    # ---- sensitivities (section 10): H1 and H2 per wave; never change a verdict
    if sensitivities:
        sens = {}

        def block(Ux, excl_units=(), excl_sub=()):
            return {h: separability(Ux, Y, SEEDS[h], excl_units, excl_sub, boot=False) for h, Y in
                    (("H1", P), ("H2", C))}
        sens["S1_first_mention"] = block({w: prec_units(rows[(w, "S0", "first_mention")]) for w in SEP_WAVES})
        for fl in (3, 10):
            sens[f"S2_floor_{fl}"] = block({w: prec_units(rows[(w, "S0", "lead_item")], fl) for w in SEP_WAVES})
        sens["S7_without_Denon"] = block(U, (DENON,))
        sens["S_COI_without_Denon_and_Cheil_Iris"] = block(U, (DENON,) + COI_CHEIL)
        with R.uncentred():
            sens["S9_uncentred"] = block(U)
        sens["S_w_pair_weight_1_over_n_minus_1"] = block(
            {w: prec_units(rows[(w, "S0", "lead_item")], weighting="per_answer") for w in SEP_WAVES})
        for pr in (0.1, 10.0):
            sens[f"S_prior_{pr}"] = block({w: prec_units(rows[(w, "S0", "lead_item")], prior=pr) for w in SEP_WAVES})
        for sub in R.OMNI:
            sens[f"S4_leave_out_{sub}"] = block(U, excl_sub=(sub,))
        res["sensitivities"] = sens
        res["verdict_changes_under_sensitivities"] = [
            {"sensitivity": n, "hypothesis": h, "primary": res[f"{h}_Sep_{'Presence' if h == 'H1' else 'Consistency'}"]["verdict"],
             "under_sensitivity": v["verdict"]}
            for n, blk in sens.items() for h, v in blk.items()
            if v["verdict"] != res[f"{h}_Sep_{'Presence' if h == 'H1' else 'Consistency'}"]["verdict"]]
    res["units"] = [{"wave": w, "substrate": k[0], "brand": k[1], **{f: U[w][k][f] for f in
                     ("n_ranked", "n_comparisons", "PREC", "main_component", "rated")},
                     "P": P[w].get(k), "C_star": C[w].get(k)} for w in SEP_WAVES for k in sorted(U[w])]
    return res


# ===========================================================================
# INPUT PARITY (allowed before the lock): counts and n's only, no PREC on real data
# ===========================================================================


def _units_at_floor(rows, floor=RATING_FLOOR):
    c = collections.Counter((r["category"], r["brand"]) for r in rows)
    return {k for k, v in c.items() if v >= floor}


def _n_kept(keys) -> int:
    """Units left after v1.10's rule that a category enters a pooled statistic only with >= 5 units."""
    c = collections.Counter(k[0] for k in keys)
    return sum(v for v in c.values() if v >= R.MIN_UNITS_PER_CATEGORY)


def input_parity(root: Path = ROOT, pins: dict | None = None, log=print) -> dict:
    """Section 4.3. Pins, then counts: answers, rankable answers, rankable rows, comparisons (pairs), units at
    the rating floor, and the n's of the comparator joins, checked against the numbers v1.10 and v1.14
    published. Computes no PREC, no correlation and no first-position concentration on real data."""
    inp = load_inputs(root, pins)
    v110, tables = inp["v110"], inp["tables"]
    out = {"phase": PHASE_ID, "kind": "input parity before the lock (counts and n's only)", "created_utc": _now(),
           "pinned_inputs_sha256": inp["hashes"], "v1_10_rank_tables_verified": len(tables), "checks": {}}
    chk = out["checks"]
    # v1.10's rank tables: data rows as recorded in its verdicts file
    rowcount = {}
    for name, e in v110["rank_tables"].items():
        with open(Path(root) / V110_OUTPUTS_REL / e["path"], newline="", encoding="utf-8") as f:
            rowcount[name] = sum(1 for _ in csv.DictReader(f))
    chk["v1_10_rank_table_rows_equal_recorded"] = all(rowcount[n] == e["rows"] for n, e in v110["rank_tables"].items())
    s3 = v110["sensitivities"]["S3_candidate_MODE"]["detail"]
    waves = {}
    for w in ("t1", "t2", "t3"):
        rr = inp["rows"][(w, "S0", "lead_item")]
        at = _units_at_floor(rr)
        ok_answers = sum(len(t["answers_ok"]) for n, t in tables.items() if S._set_role(n) == "omni" and n.split()[1] == w)
        waves[w] = {"answers_with_text": ok_answers, "rankable_answers": len({r["answer_id"] for r in rr}),
                    "rankable_rows": len(rr), "pairs": sum(math.comb(v, 2) for v in collections.Counter(
                        r["answer_id"] for r in rr).values()),
                    "units_at_floor": len(at),
                    "units_at_floor_with_P": _n_kept([k for k in at if math.isfinite(inp["P"][w].get(k, float("nan")))]),
                    "units_at_floor_with_C": _n_kept([k for k in at if k in inp["C"][w]]),
                    "v1_10_published_n_H1": s3["H1"]["per_wave"][w]["n"], "v1_10_published_n_H2": s3["H2"]["per_wave"][w]["n"]}
        waves[w]["n_H1_equals_v1_10"] = waves[w]["units_at_floor_with_P"] == waves[w]["v1_10_published_n_H1"]
        waves[w]["n_H2_equals_v1_10"] = waves[w]["units_at_floor_with_C"] == waves[w]["v1_10_published_n_H2"]
    t4 = inp["t4_meta"]
    c4 = inp["t4_comp_meta"]
    r0, r1 = inp["rows"][("t4", "S0", "lead_item")], inp["rows"][("t4", "S1", "lead_item")]
    at0 = _units_at_floor(r0)
    waves["t4"] = {"answers": t4["answers"], "answers_with_text": t4["answers_with_text"],
                   "rankable_answers": t4["rankable_answers"], "rankable_rows_S0": len(r0), "rankable_rows_S1": len(r1),
                   "pairs_S0": sum(math.comb(v, 2) for v in collections.Counter(r["answer_id"] for r in r0).values()),
                   "pairs_S1": sum(math.comb(v, 2) for v in collections.Counter(r["answer_id"] for r in r1).values()),
                   "units_at_floor_S0": len(at0), "units_at_floor_S1": len(_units_at_floor(r1)),
                   "units_at_floor_S0_with_P": _n_kept([k for k in at0 if k in inp["P"]["t4"]]),
                   "units_at_floor_S0_with_C": _n_kept([k for k in at0 if k in inp["C"]["t4"]]),
                   "v1_14_published": V114_PUBLISHED,
                   "v1_14_unit_table_rated_S0": c4["published_units_rated_S0"],
                   "v1_14_unit_table_H1_n": c4["published_H1_n"], "v1_14_unit_table_H2_n": c4["published_H2_n"]}
    w4 = waves["t4"]
    w4["equal_v1_14"] = {
        "answers": w4["answers"] == V114_PUBLISHED["answers"],
        "rankable_rows_S0": w4["rankable_rows_S0"] == V114_PUBLISHED["rankable_rows_S0"],
        "rankable_rows_S1": w4["rankable_rows_S1"] == V114_PUBLISHED["rankable_rows_S1"],
        "units_at_floor_S0": w4["units_at_floor_S0"] == V114_PUBLISHED["units_rated_S0"] == c4["published_units_rated_S0"],
        "H1_n": w4["units_at_floor_S0_with_P"] == V114_PUBLISHED["H1_n"] == c4["published_H1_n"],
        "H2_n": w4["units_at_floor_S0_with_C"] == V114_PUBLISHED["H2_n"] == c4["published_H2_n"]}
    out["waves"] = waves
    out["category_size_registry_brands"] = inp["category_size"]
    chk["t4_equals_v1_14_published"] = all(w4["equal_v1_14"].values())
    chk["archived_n_equal_v1_10"] = all(waves[w]["n_H1_equals_v1_10"] and waves[w]["n_H2_equals_v1_10"]
                                        for w in ("t1", "t2", "t3"))
    chk["t4_rank_table_sha256_equals_v1_14_record"] = True    # load_inputs halts otherwise
    chk["all_pass"] = all(v for k, v in chk.items() if k != "all_pass")
    out["note"] = ("No PREC value, correlation, verdict statistic or first-position concentration was computed on "
                   "real data; the units at the rating floor are counts of rankable mentions only. The n's of the "
                   "rated sets in the confirmatory run can be smaller (PREC also requires the main comparison "
                   "component, section 3.3).")
    for w, v in waves.items():
        log(f"[v1.16] parity {w}: " + json.dumps({k: v[k] for k in v if not isinstance(v[k], dict)}))
    log(f"[v1.16] parity checks: {chk}")
    return out


# ===========================================================================
# DRY RUN (section 11): synthetic inputs in the real file formats, three worlds with known answers
# ===========================================================================

SYN_SIZES = {"v0.19": 16, "v0.20": 24, "v0.21": 24, "v0.22": 24, "v0.23": 24}   # registry brand counts (112)
SYN_WORLDS = {
    "A_independent_precedence": "inclusion by popularity; order by a precedence strength independent of popularity",
    "B_popularity_order": "inclusion by popularity; order by the same popularity (position = Presence)",
    "C_noise_order": "inclusion by popularity; order uniformly random (no precedence signal)",
}
EXPECTED = {"A_independent_precedence": {"GATE": "PASS"},
            "B_popularity_order": {"GATE": "FAIL", "H1": "FALSIFIED"},
            "C_noise_order": {"GATE": "FAIL", "H3": "FALSIFIED"}}
V110_COLS = R.RANK_COLS
T4_COLS = S.RANK_COLS


def _syn_answer(rng, names, u, v, world, noise=0.6):
    L = int(rng.choice(np.arange(0, 11), p=[.02, .04, .10, .12, .14, .14, .12, .10, .08, .07, .07]))
    L = min(L, len(names))
    keys = 1.5 * u + rng.gumbel(size=len(u))
    chosen = list(np.argsort(-keys)[:L])
    if world == "C_noise_order":
        order = list(rng.permutation(chosen))
    else:
        score = {i: v[i] + rng.normal(0, noise) for i in chosen}
        order = sorted(chosen, key=lambda i: -score[i])
    return [names[i] for i in order]


def _syn_latents(seed, world):
    rng = np.random.default_rng(seed)
    lat = {}
    for s, n in SYN_SIZES.items():
        u = rng.normal(0, 1, n)
        if world == "B_popularity_order":
            v = u.copy()
        elif world == "C_noise_order":
            v = np.zeros(n)
        else:   # A: precedence balanced against popularity: along the popularity order the precedence values
            # repeat an 8-value cycle with zero sum and zero linear trend (small jitter breaks ties), so every
            # block of eight brands adjacent in popularity carries no popularity trend; sizes 16 and 24 are
            # whole cycles
            cyc = np.array([1.5, -0.5, -1.5, 0.5, 0.5, -1.5, -0.5, 1.5])
            v = np.empty(n)
            v[np.argsort(-u)] = cyc[np.arange(n) % 8] + rng.normal(0, 0.05, n)
        names = (["Denon"] if s == "v0.19" else []) + [f"Zq{s[-2:]}b{j:02d}" for j in range(n - (s == "v0.19"))]
        lat[s] = (names, u, v)
    return lat


def build_synthetic(root: Path, world: str, seed: int = 116100) -> dict:
    """Writes a complete synthetic input set under `root` in the formats of the real inputs and returns the
    pins (path -> SHA-256) for load_inputs. Same latent brands at every wave (a stable world)."""
    root = Path(root)
    lat = _syn_latents(seed, world)
    rng = np.random.default_rng(seed + 1)
    rt_dir = root / V110_OUTPUTS_REL / "rank_tables"
    rt_dir.mkdir(parents=True, exist_ok=True)
    rank_tables, prof = {}, []
    models6 = [f"legacy-m{i}" for i in range(1, 7)]
    for w in ("t1", "t2", "t3"):
        for s, (names, u, v) in lat.items():
            name = f"OMNI {w} {s}"
            buf = io.StringIO()
            wr = csv.writer(buf, lineterminator="\n")
            wr.writerow(V110_COLS)
            cnt = collections.Counter()
            for m in models6:
                for q in range(1, 7):
                    order = _syn_answer(rng, names, u, v, world)
                    aid = f"{name}::{m}|q{q}|"
                    n = len(order)
                    for b in order:
                        cnt[b] += 1
                    base = [name, "LEGACY-6", w, s, m, f"q{q}", "", aid, "ok", "", n, int(n >= 2), 1, 1]
                    for rule in R.RULES:
                        if not order:
                            wr.writerow(base + [rule, "", "", "", ""])
                        for k, b in enumerate(order, 1):
                            if n >= 2:
                                wr.writerow(base + [rule, b, float(k), k, (k - 1) / (n - 1)])
                            else:
                                wr.writerow(base + [rule, b, "", "", ""])
            data = buf.getvalue().encode("utf-8")
            fn = f"OMNI_{w}_{s}.csv"
            (rt_dir / fn).write_bytes(data)
            rank_tables[name] = {"path": f"rank_tables/{fn}", "sha256": hashlib.sha256(data).hexdigest(),
                                 "rows": data.decode().count("\n") - 1}
            for b in names:
                prof.append({"wave": w, "substrate": s, "brand": b, "P": 100.0 * cnt[b] / 36.0,
                             "C_star": float(rng.uniform(50, 100)), "rated": int(cnt[b] >= RATING_FLOOR),
                             "n_mentions": cnt[b], "A_descriptive": ""})
    vpath = root / V110_VERDICTS_REL
    vpath.write_text(json.dumps({"phase": "synthetic", "rank_tables": rank_tables}), encoding="utf-8")
    ppath = root / PROFILES_REL
    ppath.parent.mkdir(parents=True, exist_ok=True)
    with open(ppath, "w", newline="", encoding="utf-8") as f:
        dw = csv.DictWriter(f, fieldnames=list(prof[0]), lineterminator="\n")
        dw.writeheader()
        dw.writerows(prof)
    # t4: N3 x 6 frames x 3 runs, S0 and S1, in v1.14's rank-table format, and its unit table
    buf = io.StringIO()
    wr = csv.writer(buf, lineterminator="\n")
    wr.writerow(T4_COLS)
    cnt = collections.Counter()
    for cond in ("S0", "S1"):
        for s, (names, u, v) in lat.items():
            for m in S.N3:
                for q in range(1, 7):
                    for run in S.RUNS:
                        order = _syn_answer(rng, names, u, v, world)
                        n = len(order)
                        aid = f"t4::{s}|B|q{q}|{m}|{cond}|{run}"
                        for b in order:
                            cnt[(cond, s, b)] += 1
                        base = [aid, "t4", cond, s, m, f"q{q}", run, "ok", n, int(n >= 2), 1]
                        for rule in R.RULES:
                            if not order:
                                wr.writerow(base + [rule, "", "", ""])
                            for k, b in enumerate(sorted(order)):
                                pos = order.index(b) + 1
                                wr.writerow(base + [rule, b] + ([repr(float(pos)), pos] if n >= 2 else ["", ""]))
    data = buf.getvalue().encode("utf-8")
    tpath = root / T4_RANK_REL
    tpath.parent.mkdir(parents=True, exist_ok=True)
    tpath.write_bytes(data)
    units = []
    for s, (names, u, v) in lat.items():
        for b in names:
            if cnt[("S0", s, b)] + cnt[("S1", s, b)] == 0:
                continue
            units.append({"substrate": s, "brand": b, "rated_S0": cnt[("S0", s, b)] >= RATING_FLOOR,
                          "P_S0": 100.0 * cnt[("S0", s, b)] / 54.0, "P_S1": 100.0 * cnt[("S1", s, b)] / 54.0,
                          "C_star_S0": float(rng.uniform(50, 100)) if cnt[("S0", s, b)] >= RATING_FLOOR else None})
    spath = root / T4_STAGE1_REL
    spath.write_text(json.dumps({"rank_table_t4_sha256": hashlib.sha256(data).hexdigest(), "STAGE1_VERDICT": "synthetic",
                                 "H1_Sep_Presence": {"n": None}, "H2_Sep_Consistency": {"n": None}, "units": units}),
                     encoding="utf-8")
    return {rel: sha256_file(root / rel) for rel in (V110_VERDICTS_REL, PROFILES_REL, T4_RANK_REL, T4_STAGE1_REL)}


def _mode_vs_P(inp) -> dict:
    """Dry run only: rho_w(MODE, P) per wave, to show the list-length channel that PREC removes."""
    out = {}
    for w in SEP_WAVES:
        V = R.units_cat_brand(inp["rows"][(w, "S0", "lead_item")], RATING_FLOOR)
        keys = sorted(k for k, s in V.items() if s["rated"] and inp["P"][w].get(k) is not None)
        out[w] = R._rho_only([inp["P"][w][k] for k in keys], [V[k]["MODE"] for k in keys], [k[0] for k in keys])["rho"]
    return out


def _truth(res, seed, world) -> dict:
    """Dry run only: on the rated units of each wave, rho_w(true precedence v, P) (what H1 should find) and
    rho_w(PREC, v) (how well PREC recovers the true precedence)."""
    lat = _syn_latents(seed, world)
    vmap = {(s, nm[i]): v[i] for s, (nm, _u, v) in lat.items() for i in range(len(nm))}
    out = {}
    for w in SEP_WAVES:
        us = [u for u in res["units"] if u["wave"] == w and u["rated"] and u["P"] is not None]
        g = [u["substrate"] for u in us]
        out[w] = {"rho_true_v_P": R._rho_only([u["P"] for u in us], [vmap[(u["substrate"], u["brand"])] for u in us], g)["rho"],
                  "rho_PREC_v": R._rho_only([vmap[(u["substrate"], u["brand"])] for u in us], [u["PREC"] for u in us], g)["rho"]}
    return out


def dry_run(n_shuffle: int | None = None, n_perm: int | None = None, log=print, seed: int = 116100) -> dict:
    out = {"phase": PHASE_ID, "kind": "dry run on synthetic data with known answers (no real answer read)",
           "created_utc": _now(), "seed": seed, "worlds": {}, "draws": {
               "perm": N_PERM if n_perm is None else n_perm, "shuffle": N_SHUFFLE if n_shuffle is None else n_shuffle}}
    for world, desc in SYN_WORLDS.items():
        with tempfile.TemporaryDirectory() as td:
            pins = build_synthetic(Path(td), world, seed)
            inp = load_inputs(Path(td), pins)
            log(f"[v1.16] dry run, world {world}")
            res = analyse(inp, log=lambda m: log("    " + m), n_shuffle=n_shuffle, n_perm=n_perm, boot=False,
                          sensitivities=(world == "A_independent_precedence"))
            got = {"GATE": res["GATE"], "H1": res["H1_Sep_Presence"]["verdict"],
                   "H2": res["H2_Sep_Consistency"]["verdict"], "H3": res["H3_Retest_t1_t2"]["verdict"],
                   "H4_S1": res["H4_Sep_Presence_t4_S1"]["verdict"]}
            exp = EXPECTED[world]
            out["worlds"][world] = {
                "description": desc, "expected": exp, "got": got,
                "matches_expected": all(got[k] == v for k, v in exp.items()),
                "H1_rho_per_wave": {w: v["rho"] for w, v in res["H1_Sep_Presence"]["per_wave"].items()},
                "H1_n_per_wave": {w: v["n"] for w, v in res["H1_Sep_Presence"]["per_wave"].items()},
                "H2_rho_per_wave": {w: v["rho"] for w, v in res["H2_Sep_Consistency"]["per_wave"].items()},
                "H3": {k: res["H3_Retest_t1_t2"][k] for k in ("rho", "n", "p_perm", "p_shuffle", "shuffled_mean_rho")},
                "H4_S1": {k: res["H4_Sep_Presence_t4_S1"][k] for k in ("rho", "n")},
                "MODE_vs_P_rho_per_wave": _mode_vs_P(inp), "CONSEQUENCE": res["CONSEQUENCE"],
                "truth": _truth(res, seed, world),
                "MQ7_flag": res["MQ7_negative_control"]["flag"],
                "sensitivity_verdict_changes": res.get("verdict_changes_under_sensitivities")}
    out["all_match_expected"] = all(v["matches_expected"] for v in out["worlds"].values())
    return out


# ===========================================================================
# LOCK, ANCHOR AND THE ONE CONFIRMATORY RUN (section 12)
# ===========================================================================


def lock_manifest_text(files=LOCKED_FILES, root: Path = ROOT) -> str:
    return "".join(f"{sha256_file(Path(root) / f)}  {f}\n" for f in files)


def verify_lock_manifest(path: Path = LOCK_MANIFEST, root: Path = ROOT) -> list[str]:
    if not Path(path).exists():
        return [f"missing lock manifest {path}"]
    bad = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        h, f = line.split("  ", 1)
        p = Path(root) / f
        if not p.exists():
            bad.append(f"missing {f}")
        elif sha256_file(p) != h:
            bad.append(f"changed {f}")
    return bad


def _git(*args) -> str:
    r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise Halt(f"git {' '.join(args)}: {r.stderr.strip()[:200]}")
    return r.stdout.strip()


def tag_exists(tag: str = PREREG_TAG) -> bool:
    return subprocess.run(["git", "-C", str(ROOT), "rev-parse", "-q", "--verify", f"refs/tags/{tag}"],
                          capture_output=True).returncode == 0


def write_anchor(osf_note: str = "", anchor: Path = ANCHOR_FILE) -> dict:
    """After tag v1.16-prereg-r1 is pushed: tag object, commit, tree, UTC time and the SHA-256 of every
    locked file. Refuses to overwrite."""
    if anchor.exists():
        raise Halt(f"anchor exists: {anchor}")
    if not tag_exists():
        raise Halt(f"tag {PREREG_TAG} does not exist")
    bad = verify_lock_manifest()
    if bad:
        raise Halt("lock manifest: " + "; ".join(bad[:5]))
    rec = {"phase": PHASE_ID, "tag": PREREG_TAG, "tag_object": _git("rev-parse", PREREG_TAG),
           "commit": _git("rev-list", "-n", "1", PREREG_TAG), "tree": _git("rev-parse", f"{PREREG_TAG}^{{tree}}"),
           "written_utc": _now(), "osf": osf_note,
           "lock_manifest_sha256": sha256_file(LOCK_MANIFEST),
           "locked_files": {f: sha256_file(ROOT / f) for f in LOCKED_FILES}}
    anchor.parent.mkdir(parents=True, exist_ok=True)
    anchor.write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    return rec


def lock_status() -> list[str]:
    """Everything that must hold before the confirmatory run (section 12)."""
    why = []
    if not tag_exists():
        why.append(f"tag {PREREG_TAG} does not exist")
    if not ANCHOR_FILE.exists():
        why.append(f"anchor file {ANCHOR_FILE.relative_to(ROOT)} does not exist (OSF deposit not recorded)")
    why += verify_lock_manifest()
    if RESULTS_FILE.exists():
        why.append(f"results exist ({RESULTS_FILE.relative_to(ROOT)}): the analysis runs once")
    return why


def run(log=print) -> dict:
    why = lock_status()
    if why:
        raise Halt("refused (section 12): " + "; ".join(why))
    par = input_parity(log=log)
    if not par["checks"]["all_pass"]:
        raise Halt(f"input parity failed: {par['checks']}")
    inp = load_inputs()
    res = analyse(inp, log=log)
    res.update(created_utc=_now(), prereg_tag=PREREG_TAG, anchor_sha256=sha256_file(ANCHOR_FILE),
               inputs_sha256=inp["hashes"], rank_tables_sha256=inp["rank_table_hashes"],
               published_controls={"MQ6_v1_10": inp["v110"].get("MQ6"),
                                   "MQ6_v1_14_t4": json.loads((ROOT / T4_STAGE1_REL).read_text())
                                   .get("MQ6_positive_control")})
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_FILE.write_text(json.dumps(R._clean(res), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    log(f"[v1.16] results written: {RESULTS_FILE} (sha256 {sha256_file(RESULTS_FILE)[:16]}...)")
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--parity", action="store_true")
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--lock-manifest", action="store_true")
    g.add_argument("--verify-lock", action="store_true")
    g.add_argument("--write-anchor", action="store_true")
    g.add_argument("--run", action="store_true")
    ap.add_argument("--shuffle-draws", type=int, default=None)
    ap.add_argument("--perm-draws", type=int, default=None)
    ap.add_argument("--osf-note", default="")
    a = ap.parse_args(argv)
    if a.parity:
        out = input_parity()
        PARITY_FILE.parent.mkdir(parents=True, exist_ok=True)
        PARITY_FILE.write_text(json.dumps(R._clean(out), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"[v1.16] parity written: {PARITY_FILE}; all_pass = {out['checks']['all_pass']}")
        return 0 if out["checks"]["all_pass"] else 1
    if a.dry_run:
        out = dry_run(a.shuffle_draws, a.perm_draws)
        DRY_DIR.mkdir(parents=True, exist_ok=True)
        f = DRY_DIR / "dryrun_v1_16.json"
        f.write_text(json.dumps(R._clean(out), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"[v1.16] dry run written: {f}; all worlds match expected = {out['all_match_expected']}")
        return 0 if out["all_match_expected"] else 1
    if a.lock_manifest:
        LOCK_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        LOCK_MANIFEST.write_text(lock_manifest_text(), encoding="utf-8")
        print(f"[v1.16] lock manifest written: {LOCK_MANIFEST} ({len(LOCKED_FILES)} files)")
        return 0
    if a.verify_lock:
        bad = verify_lock_manifest()
        print("[v1.16] lock manifest OK" if not bad else "[v1.16] lock manifest FAILED: " + "; ".join(bad))
        return 0 if not bad else 1
    if a.write_anchor:
        rec = write_anchor(a.osf_note)
        print(f"[v1.16] anchor written: {ANCHOR_FILE} (commit {rec['commit'][:12]})")
        return 0
    if a.run:
        run()
        return 0


if __name__ == "__main__":
    sys.exit(main())
