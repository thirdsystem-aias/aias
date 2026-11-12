"""
v1_17_lib.py -- AIAS(TM) methodology v1.17, "How many runs are enough" (exploratory re-analysis).

Loaders for the archived inputs and the estimators of PRE_REGISTRATION_v1_17.md (section 4). Pure numpy/scipy;
no network, no API calls. Every path is resolved from this file's location (the repository root is four levels
up), so the scripts run in whichever worktree holds them.

Data layout used throughout
  t4 (study v0.42): X[u, r, f] in {0, 1} -- unit u = (category, brand, model, condition), run r = 1..3,
      frame f = the six Phase B question frames of the category; 1 = the answer named the brand (coded column
      `mentioned` of osf/v42/data/coded/vNN_phase_b.csv).
  omnibus (v0.41 table): W[u, w] = k / 6 -- unit u = (category, brand, legacy model), wave w = t1, t2, t3;
      k = the model's mentions over the six frames (column k_per_model of osf/v41/v41_three_wave_table.csv).
"""
import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]                       # .../osf/methodology/v1_17/scripts -> repository root
V117 = HERE.parent

T4_CODED = ROOT / "osf/v42/data/coded"
T4_VERDICTS = ROOT / "osf/v42/v42_verdicts.json"
T4_PROBES = ROOT / "osf/v42/prereg/probes_v0_42.jsonl"
OMNI_TABLE = ROOT / "osf/v41/v41_three_wave_table.csv"

CATEGORIES = {"v0.19": "v19", "v0.20": "v20", "v0.21": "v21", "v0.22": "v22", "v0.23": "v23"}
CATEGORY_LABEL = {"v0.19": "audiophile headphones", "v0.20": "skincare", "v0.21": "cosmetics",
                  "v0.22": "automotive", "v0.23": "premium spirits"}
N3 = ("claude-fable-5-2", "gpt-6-astra", "gemini-4-argon")
CONDS = ("S0", "S1")
RUNS = (1, 2, 3)
F = 6
WAVES = ("t1", "t2", "t3")
# Legacy six in the order of k_per_model (score_v0_31.PANEL, as quoted in score_v0_42.py, L6).
L6 = ("claude-opus-4-5", "claude-sonnet-4-5", "gpt-4o", "gpt-4o-mini", "gemini-2.5-flash", "gemini-2.5-flash-lite")
TAUS = (0.10, 0.05)                          # Schulte, Bleeker and Kaufmann (2026) benchmarks
SE_AT_R = (1, 2, 3, 5, 7, 10, 24)
# Sensitivity S-COI (v0.62 params COI_FLAGGED): Denon + the five Cheil Worldwide / Iris brands. v0.23 brands are
# coded S01..S24 in the t4 tables; the name is mapped through the locked t4 probe file (brand_id -> brand).
COI_FLAGGED_NAMES = (("v0.19", "Denon"), ("v0.20", "Eucerin"), ("v0.22", "BMW"), ("v0.22", "Bentley"),
                     ("v0.22", "Chevrolet"), ("v0.23", "Jack Daniel's"))
BANDS = ("zero", "low", "middle", "high", "full")
SEEDS = {"bootstrap": 117017, "dry_run": 117001, "coverage": 117002}
N_BOOT = 10_000
FEW_CLUSTERS = 10      # below this the cluster-bootstrap interval is flagged (dry run: it under-covers with 6)


# =========================================================================== hashing
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# =========================================================================== loaders
class T4:
    """t4 Phase B mentions as X[u, r, f] with unit metadata."""

    def __init__(self, X, units, frames):
        self.X = np.asarray(X, dtype=float)
        self.units = list(units)               # [(category, brand, model, cond)]
        self.frames = frames                   # {category: [frame ids]}
        self.cat = np.array([u[0] for u in self.units])
        self.brand = np.array([u[1] for u in self.units])
        self.model = np.array([u[2] for u in self.units])
        self.cond = np.array([u[3] for u in self.units])
        sizes = {c: len({u[1] for u in self.units if u[0] == c}) for c in set(self.cat)}
        self.size = np.array([sizes[c] for c in self.cat])
        self.cluster = np.array(["|".join((u[0], u[2], u[3])) for u in self.units])


def load_t4(coded_dir=T4_CODED, categories=CATEGORIES):
    """Read the coded Phase B tables; refuse on any duplicate, missing or out-of-design row."""
    cells = {}
    frames = {}
    n_rows = 0
    for cat, short in categories.items():
        path = Path(coded_dir) / f"{short}_phase_b.csv"
        fr = []
        with open(path, newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        for r in rows:
            n_rows += 1
            if r["substrate"] != cat or r["model"] not in N3 or r["condition"] not in CONDS:
                raise ValueError(f"out-of-design row in {path.name}: {r['call_id']}")
            run = int(r["run"])
            if run not in RUNS or r["mentioned"] not in ("0", "1"):
                raise ValueError(f"bad run or code in {path.name}: {r['call_id']}")
            if r["frame_id"] not in fr:
                fr.append(r["frame_id"])
            key = (cat, r["brand"], r["model"], r["condition"], run, r["frame_id"])
            if key in cells:
                raise ValueError(f"duplicate row {key}")
            cells[key] = int(r["mentioned"])
        if len(fr) != F:
            raise ValueError(f"{cat}: {len(fr)} frames, expected {F}")
        frames[cat] = sorted(fr)
    units = sorted({k[:4] for k in cells})
    X = np.full((len(units), len(RUNS), F), np.nan)
    for i, (cat, b, m, c) in enumerate(units):
        for ri, r in enumerate(RUNS):
            for fi, f in enumerate(frames[cat]):
                key = (cat, b, m, c, r, f)
                if key not in cells:
                    raise ValueError(f"missing cell {key}")
                X[i, ri, fi] = cells[key]
    t = T4(X, units, frames)
    t.n_rows = n_rows
    return t


class Omni:
    """Omnibus waves as W[u, w] = k/6 with unit metadata (unit = category, brand, legacy model)."""

    def __init__(self, W, units):
        self.W = np.asarray(W, dtype=float)
        self.units = list(units)
        self.cat = np.array([u[0] for u in self.units])
        self.brand = np.array([u[1] for u in self.units])
        self.model = np.array([u[2] for u in self.units])
        sizes = {c: len({u[1] for u in self.units if u[0] == c}) for c in set(self.cat)}
        self.size = np.array([sizes[c] for c in self.cat])
        self.cluster = np.array(["|".join((u[0], u[2])) for u in self.units])


def load_omni(path=OMNI_TABLE):
    k = {}
    pi_check = []
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        vec = json.loads(r["k_per_model"])
        if len(vec) != len(L6) or any((not isinstance(x, int)) or x < 0 or x > F for x in vec):
            raise ValueError(f"bad k_per_model {r['substrate']} {r['brand']} {r['wave']}")
        if r["wave"] not in WAVES:
            raise ValueError(f"unknown wave {r['wave']}")
        for m, x in zip(L6, vec):
            key = (r["substrate"], r["brand"], m, r["wave"])
            if key in k:
                raise ValueError(f"duplicate {key}")
            k[key] = x
        pi_check.append(abs(sum(vec) / (F * len(L6)) - float(r["pi_hat"])))
    units = sorted({key[:3] for key in k})
    W = np.full((len(units), len(WAVES)), np.nan)
    for i, u in enumerate(units):
        for wi, w in enumerate(WAVES):
            if u + (w,) not in k:
                raise ValueError(f"missing {u + (w,)}")
            W[i, wi] = k[u + (w,)] / F
    o = Omni(W, units)
    o.max_pi_hat_abs_diff = max(pi_check)       # table consistency: pi_hat == sum k / 36
    return o


def coi_brand_keys(probes_path=T4_PROBES):
    """(category, brand as coded in t4) of the S-COI brands; v0.23 names mapped to S-codes via the probe file."""
    code = {}
    with open(probes_path, encoding="utf-8") as fh:
        lines = fh.readlines()
    for line in lines:
        d = json.loads(line)
        if d.get("substrate") == "v23" and d.get("phase") == "A" and d.get("brand_id"):
            code[d["brand"]] = d["brand_id"]
    out = []
    for cat, name in COI_FLAGGED_NAMES:
        out.append((cat, code[name]) if cat == "v0.23" else (cat, name))
    return tuple(out)


def published_floor_count(t4, cond="S0"):
    """v0.42 descriptive 3 quantity on N3: brands with 6 * pi_hat < 1 over three runs (published: 49 in S0)."""
    keys = sorted({(c, b) for c, b, cc in zip(t4.cat, t4.brand, t4.cond) if cc == cond})
    n = 0
    for c, b in keys:
        idx = (t4.cat == c) & (t4.brand == b) & (t4.cond == cond)
        if below_floor(int(t4.X[idx].sum()), int(t4.X[idx].size)):
            n += 1
    return n


def below_floor(total_k, n_answers):
    """Published recall floor (v0.42 descriptive 3): 6 * pi_hat < 1 with pi_hat = total_k / n_answers, in integers."""
    return 6 * total_k < n_answers


# =========================================================================== estimators
def per_run(t4):
    """p[u, r] = mentions / 6 (per-run Presence of a unit)."""
    return t4.X.mean(axis=2)


def unit_var(P):
    """s2[u] = sample variance (ddof 1) of a unit's per-run (or per-wave) values P[u, :]."""
    return np.var(P, axis=1, ddof=1)


def pooled_var(s2, idx=None):
    """Pooled run-to-run variance: mean of unit variances (equal degrees of freedom per unit)."""
    s2 = np.asarray(s2, float) if idx is None else np.asarray(s2, float)[idx]
    return float(np.mean(s2)) if len(s2) else float("nan")


def se_at(var, R):
    return math.sqrt(var / R) if var == var else float("nan")


def runs_needed(var, tau):
    """Smallest R with sqrt(var / R) < tau  (strict, as in 'below 0.10'); assumes independent runs, constant var."""
    if not (var == var):
        return None
    if var <= 0:
        return 1
    R = max(1, math.ceil(var / tau ** 2 - 1e-9))
    while math.sqrt(var / R) >= tau:
        R += 1
    while R > 1 and math.sqrt(var / (R - 1)) < tau:
        R -= 1
    return R


def chi2_interval(var, n_units, df_per_unit=2, level=0.95):
    """Interval for a pooled variance assuming independent normal units (alongside only)."""
    df = n_units * df_per_unit
    if df <= 0 or not (var == var):
        return (float("nan"), float("nan"))
    a = (1 - level) / 2
    return (var * df / stats.chi2.ppf(1 - a, df), var * df / stats.chi2.ppf(a, df))


def cluster_bootstrap_var(s2, clusters, n_boot=N_BOOT, seed=SEEDS["bootstrap"], level=0.95):
    """Percentile interval for the pooled variance, resampling whole clusters (category x model x condition at
    t4: the units that share the same answers). Returns (lo, hi, n_clusters, draws)."""
    s2 = np.asarray(s2, float)
    clusters = np.asarray(clusters)
    ids = sorted(set(clusters.tolist()))
    sums = np.array([s2[clusters == c].sum() for c in ids])
    cnts = np.array([(clusters == c).sum() for c in ids], float)
    rng = np.random.default_rng(seed)
    draw = rng.integers(0, len(ids), size=(n_boot, len(ids)))
    boot = sums[draw].sum(axis=1) / cnts[draw].sum(axis=1)
    a = (1 - level) / 2
    return float(np.quantile(boot, a)), float(np.quantile(boot, 1 - a)), len(ids), n_boot


def band_of(total_k, n_answers):
    """Presence band of a unit from its total mentions over all its answers (exact integer rule)."""
    if total_k == 0:
        return "zero"
    if total_k == n_answers:
        return "full"
    share = total_k / n_answers
    if share < 1 / 3:
        return "low"
    if share <= 2 / 3:
        return "middle"
    return "high"


def bands_t4(t4):
    tot = t4.X.sum(axis=(1, 2)).astype(int)
    n = t4.X.shape[1] * t4.X.shape[2]
    return np.array([band_of(int(k), n) for k in tot])


def projection_row(s2, idx, clusters, n_boot=N_BOOT, seed=SEEDS["bootstrap"]):
    """The pre-registered block for one stratum: pooled variance, SD, SE at R, R* for each tau, intervals."""
    idx = np.asarray(idx, bool)
    n = int(idx.sum())
    v = pooled_var(s2, idx)
    out = {"n_units": n, "pooled_var": v, "sd_one_run": math.sqrt(v) if n else None,
           "se_at_R": {str(R): se_at(v, R) for R in SE_AT_R} if n else None}
    if n == 0:
        return out
    lo, hi, n_cl, B = cluster_bootstrap_var(np.asarray(s2)[idx], np.asarray(clusters)[idx], n_boot, seed)
    clo, chi = chi2_interval(v, n)
    out.update({"n_clusters": n_cl, "var_ci95_cluster_bootstrap": [lo, hi], "var_ci95_chi2_alongside": [clo, chi],
                "bootstrap_draws": B, "few_clusters_flag": n_cl < FEW_CLUSTERS})
    for tau in TAUS:
        out[f"R_needed_se_below_{tau:.2f}"] = {
            "point": runs_needed(v, tau),
            "ci95_cluster_bootstrap": [runs_needed(lo, tau), runs_needed(hi, tau)],
            "ci95_chi2_alongside": [runs_needed(clo, tau), runs_needed(chi, tau)]}
    return out


# =========================================================================== once vs three times
def discordance(single, ref):
    """Strict order reversals between two score vectors over the same brands.
    Returns (n_brands_changing_place, n_discordant_pairs, n_pairs). A brand 'changes place' when at least one
    other brand is strictly above it under one measurement and strictly below it under the other; moves between
    a tie and a strict order are not reversals."""
    a = np.asarray(single, float)
    b = np.asarray(ref, float)
    da = np.sign(a[:, None] - a[None, :])
    db = np.sign(b[:, None] - b[None, :])
    disc = (da * db) < 0
    n = len(a)
    return int(disc.any(axis=1).sum()), int(np.triu(disc, 1).sum()), n * (n - 1) // 2
