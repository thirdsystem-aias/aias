#!/usr/bin/env python3
"""
score_v41.py — AIAS(TM) v0.41 scorer: Long-Horizon Stability t1->t2->t3.

Fork of score_v34.py (wave loaders, CV-CPC comparator, phantom rule) with the v1.8
phi/J kernel carried VERBATIM from score_v0_37.py / score_v1_8.py (phi_of, jaccard_of).
Transcribes osf/v41/prereg/v0_41_longitudinal_t3_omnibus_content.py (draft r1). THE
PRE-REGISTRATION PROSE IS AUTHORITATIVE: every constant below cites the section it
transcribes; a disagreement is a bug to fix toward the prose.

STEP 0 = PARITY GATES (PARITY P1-P4). They run first, on frozen t1/t2 inputs only.
Any failure HALTS (exit 2) before a single t3 file is opened.

Modes (exactly one):
  --parity-only        gates only (safe before the lock); writes
                       osf/v41/prereg/parity_gates_v0_41.json
  --synthetic DIR      full scoring with t3 read from DIR (same layout as
                       osf/v41/data/); outputs to DIR/_score/. Test use.
  --run                the real scoring: t3 = osf/v41/data/. Refuses unless the tag
                       v0.41-prereg-r1 exists. Outputs osf/v41/v41_verdicts.json and
                       osf/v41/v41_three_wave_table.csv.

Root: $AIAS_ROOT (worktree or repo). The certified upstream modules (score_v33,
score_v0_31, score_v20/21/22) hard-code ~/aias; when ~/aias is not AIAS_ROOT this
script re-executes itself with HOME pointing at a temporary folder whose 'aias'
entry links to AIAS_ROOT, so every module reads the same tree. Nothing else changes.
"""
import os
import sys
import tempfile
from pathlib import Path


def _bootstrap_root():
    root = Path(os.environ.get("AIAS_ROOT", str(Path.home() / "aias"))).resolve()
    try:
        same = (Path.home() / "aias").resolve() == root
    except OSError:
        same = False
    if same:
        return root
    if os.environ.get("_V41_HOME_SHIM"):
        sys.exit(f"[v41] ROOT shim failed: ~/aias -> {(Path.home() / 'aias').resolve()} != {root}")
    import site
    shim = Path(tempfile.mkdtemp(prefix="v41_home_"))
    (shim / "aias").symlink_to(root)
    env = dict(os.environ, HOME=str(shim), _V41_HOME_SHIM="1", AIAS_ROOT=str(root))
    env.setdefault("PYTHONUSERBASE", site.getuserbase())   # keep the real user site-packages
    # re-execute the ENTRY script (this file, or a test/calibration script importing it)
    os.execve(sys.executable, [sys.executable, os.path.abspath(sys.argv[0])] + sys.argv[1:], env)


ROOT = _bootstrap_root()
sys.path.insert(0, str(ROOT / "prereg"))
sys.path.insert(0, str(ROOT / "scripts"))

import argparse        # noqa: E402
import csv             # noqa: E402
import hashlib         # noqa: E402
import itertools       # noqa: E402
import json            # noqa: E402
import subprocess      # noqa: E402
from datetime import date, datetime  # noqa: E402

import numpy as np     # noqa: E402
from scipy import stats  # noqa: E402

# ===========================================================================
# TRANSCRIBED CONSTANTS (draft r1; section cited inline)
# ===========================================================================
PHASE_ID = "v0.41"
PREREG_TAG = "v0.41-prereg-r1"                       # PREREG_TAG
OMNI = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]  # SUBSTRATES
SUBDIR = {"v0.19": "v19", "v0.20": "v20", "v0.21": "v21", "v0.22": "v22", "v0.23": "v23"}
N_BRAND_UNITS = 112                                   # N_BRAND_UNITS
M = 6                                                 # METRICS: panel models
F = 6                                                 # METRICS: frames per model
MF = M * F
FLOOR = 1.0                                           # METRICS: phantom / CV-CPC floor (v0.34 rule)
EXPECTED_BRANDS = {"v0.19": 16, "v0.20": 24, "v0.21": 24, "v0.22": 24, "v0.23": 24}  # SUBSTRATES

N_PERM = 10_000                                       # HYPOTHESES: 10,000 draws
N_BOOT = 10_000                                       # H_Horizon_Decay: 10,000 resamples
SEED_PHI = 410041                                     # H_Phi_LongHorizon
SEED_BOOT = 410042                                    # H_Horizon_Decay
SEED_PRESENCE = 410043                                # SCORER_NOTES S1 (draft amendment)
SEED_DRIFT = 410044                                   # SCORER_NOTES S1 (draft amendment)
SEED_FRAME = 410045                                   # SCORER_NOTES S2: frame-structure null
N_FRAME = 10_000                                      #   (within-frame model shuffles of t3)
P_ALPHA = 0.05

PHI_CONF, PHI_FALS, PHI_N_FLOOR = 0.50, 0.30, 40      # H_Phi_LongHorizon
PRES_CONF, PRES_FALS = 0.70, 0.50                     # H_Presence_LongHorizon
PRES_CONF_K, PRES_FALS_K = 4, 3                       #   ">= 4/5", ">= 3/5"
DRIFT_CONF, DRIFT_FALS = 0.30, 0.50                   # H_Drift_Dissociation
MIN_PANEL = 4                                         # MODEL_DROP_RULE
TRUNC_REASONS = {"max_tokens", "MAX_TOKENS", "length"}  # MC_Truncation

DATED_ALIASES = ["claude-opus-4-5", "claude-sonnet-4-5", "gpt-4o", "gpt-4o-mini"]  # PANEL_STATUS
T2_SERVED = {"claude-opus-4-5": "claude-opus-4-5-20251101",                         # PANEL_STATUS
             "claude-sonnet-4-5": "claude-sonnet-4-5-20250929",
             "gpt-4o": "gpt-4o-2024-08-06",
             "gpt-4o-mini": "gpt-4o-mini-2024-07-18"}
T1_DATE = {"v0.19": "2026-05-20", "v0.20": "2026-05-21", "v0.21": "2026-05-22",      # SUBSTRATES t1_acq
           "v0.22": "2026-05-25", "v0.23": "2026-05-26"}

# PARITY P4 / MC_ProbeParity — acquisition_manifest_v41.md (8 SHA-256, t1 values)
PROBE_SHA256 = {
    "osf/v19/phase_a_queries.jsonl": "276f8f5c16a9b28e813842601b5ecc416b78e6948bfefdf2df7d617b658c687e",
    "osf/v19/phase_b_queries.jsonl": "75e4838dee08d6862118b6d4ef19d3f38b2d061e8059afc402eab88f874c4188",
    "osf/v19/thresholds_v0_19.json": "542fd89b9406d18bb8635baa64d99fa1ce0999cd183f16aa56d3fb023cf6aa61",
    "prereg/v0_20_registry.json": "eb9559eaa6595eaf588dc5ec26c5c742d14c91d4ea93aaedd1e4577e3fa25782",
    "prereg/v0_21_registry.json": "45efbae5db983c24e00ad30d4b66369e685857295e8fd292a0ee0ca73349b5d3",
    "prereg/v0_22_automotive_content.py": "431f919c809c6260815b9a7a10fe14cb915ae2ce67660aaa6ef48227783d66b9",
    "scripts/run_acquisition_v22.py": "59f711b82efb0846f8305e7d84423667571e819aa80ad071edb01c9b1c883cfe",
    "scripts/acquire_v0_23.py": "7056f4fa88a9c2e353421f9a967470375db77f5f4a17603115810681b87152da",
}

# PARITY P1/P2 references — v1.8 outputs frozen from branch v1.8, commit 21ce11c
# (they are not on the v0.37+ line); copies in osf/v41/registries/, checked here.
REF_DIR = ROOT / "osf/v41/registries"
REF_FILES = {
    "v1_8_instrument_table.csv": "2d0ea5e83b01a39d1b120fe75b79178b78c85a649837f0d40a473a38f041f6e6",
    "v1_8_verdicts.json": "a280385f1868cfdff06d6c3dfae6eb4288fb1a6ad01129d6d23320a3b88b7e78",
}
P1_TOL = 1e-9          # PARITY P1: |diff| <= 1e-9
P2_RHO, P2_N = 0.6454, 83   # PARITY P2: rho to four decimals, n = 83
P3_TOL = 1e-9          # PARITY P3 (SCORER_NOTES S5)
V34_VERDICTS = ROOT / "osf/v34/v34_verdicts.json"

OSF = ROOT / "osf"
DATA2 = OSF / "v34" / "data"
DATA3 = OSF / "v41" / "data"


class GateFailure(RuntimeError):
    pass


class Halt(RuntimeError):
    pass


# ===========================================================================
# KERNEL — verbatim from score_v0_37.py (seeded from score_v1_8.py). Do not edit.
# ===========================================================================
def phi_of(counts_vec):
    """phi_b = [1/(M-1)] * sum_m (k - F*pi_hat)^2 / [F*pi_hat*(1-pi_hat)] (locked).
    Fork-A: pi_hat==0 -> 'zero'; pi_hat==1 -> 'saturated'; else 'defined' -> phi.
    phi is INCONSISTENCY-oriented (higher phi = lower consistency). Returns
    (phi or None, pi_hat, label)."""
    k = np.asarray(counts_vec, float)
    pi = float(k.sum() / MF)
    if pi <= 0.0:
        return None, pi, "zero"
    if pi >= 1.0:
        return None, pi, "saturated"
    denom = F * pi * (1.0 - pi)
    phi = float(((k - F * pi) ** 2).sum() / denom / (M - 1))
    return phi, pi, "defined"


def jaccard_of(model_to_frames):
    """J_b = mean over model pairs of |S_m ∩ S_m'| / |S_m ∪ S_m'|. Defined for
    >=1 surfacing across >=2 models. KERNEL-KEEP: verbatim from the seeded template."""
    sets = [frozenset(s) for s in model_to_frames.values() if s]
    if len(sets) < 2:
        return None, len(sets)
    vals = []
    for a, b in itertools.combinations(sets, 2):
        union = a | b
        vals.append(len(a & b) / len(union) if union else 0.0)
    return (float(np.mean(vals)) if vals else None), len(sets)
# ============================ end verbatim kernel ============================


def phi_m(counts_vec):
    """phi on a reduced panel (MODEL_DROP_RULE): the locked formula with M' = len(k).
    Identical to phi_of when len(k) == 6 (asserted by the test suite)."""
    if len(counts_vec) == M:
        return phi_of(counts_vec)
    k = np.asarray(counts_vec, float)
    m = len(k)
    pi = float(k.sum() / (m * F))
    if pi <= 0.0:
        return None, pi, "zero"
    if pi >= 1.0:
        return None, pi, "saturated"
    phi = float(((k - F * pi) ** 2).sum() / (F * pi * (1.0 - pi)) / (m - 1))
    return phi, pi, "defined"


def cv_cpc(recall):
    """v0.34 CV-CPC (WALLED, comparability baseline only): 1/(1+CV), mean floor 1.0, ddof 0."""
    x = np.asarray(recall, float)
    mu = x.mean()
    if mu < FLOOR:
        return None
    return 1.0 / (1.0 + x.std(ddof=0) / mu)


# ===========================================================================
# statistics helpers
# ===========================================================================
def _pearson(a, b):
    a = np.asarray(a, float) - np.mean(a)
    b = np.asarray(b, float) - np.mean(b)
    d = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d > 0 else float("nan")


def spearman(x, y):
    """Spearman with average ranks (= scipy.stats.spearmanr). NaN if n < 3 or constant."""
    if len(x) < 3:
        return float("nan")
    return _pearson(stats.rankdata(x), stats.rankdata(y))


def within_ranks(values, groups):
    """Average ranks computed WITHIN each group (v0.37 convention)."""
    values = np.asarray(values, float)
    groups = np.asarray(groups)
    out = np.empty(len(values))
    for g in dict.fromkeys(groups):
        idx = np.where(groups == g)[0]
        out[idx] = stats.rankdata(values[idx])
    return out


def within_pct(values, groups):
    """Within-substrate percentile rank = average rank / n_substrate (H_Drift_Dissociation)."""
    groups = np.asarray(groups)
    r = within_ranks(values, groups)
    n = np.array([np.sum(groups == g) for g in groups], float)
    return r / n


def pooled_within_rho(x, y, groups):
    if len(x) < 3:
        return float("nan")
    return _pearson(within_ranks(x, groups), within_ranks(y, groups))


def _group_index(groups):
    groups = np.asarray(groups)
    return [np.where(groups == g)[0] for g in dict.fromkeys(groups)]


def perm_p(x, y, groups, obs, seed, sided, n_draws=None):
    """Monte Carlo permutation p for a pooled Spearman: y permuted WITHIN groups
    (pass one group for an unstratified test). (count + 1) / (N + 1)."""
    n_draws = n_draws or N_PERM
    if not np.isfinite(obs):
        return float("nan")
    rng = np.random.default_rng(seed)
    rx = stats.rankdata(x)
    ry = stats.rankdata(y)            # pooled ranks are invariant to within-group permutation
    gidx = _group_index(groups)
    idx = np.arange(len(y))
    hits = 0
    for _ in range(n_draws):
        for g in gidx:
            idx[g] = rng.permutation(g)
        r = _pearson(rx, ry[idx])
        if sided == "one":
            hits += r >= obs - 1e-12
        else:
            hits += abs(r) >= abs(obs) - 1e-12
    return (hits + 1) / (n_draws + 1)


def mc_se(p, n_draws=None):
    n_draws = n_draws or N_PERM
    return float(np.sqrt(p * (1 - p) / n_draws)) if np.isfinite(p) else float("nan")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


# ===========================================================================
# wave loading (certified extraction lineage; same for every wave)
# ===========================================================================
def _layout(base, v23_dir):
    return {"base": Path(base), "v23": Path(v23_dir)}


LAYOUT = {
    "t1": _layout(OSF, OSF / "v23/data"),
    "t2": _layout(DATA2, DATA2 / "v23"),
}


def load_wave(lay):
    """Per substrate: counts {brand:[6]}, recog {brand:[6]}, frames {brand:{model:set}},
    cells {brand:cell}. Uses the certified extractors (score_v0_31, score_v33) and the
    v1.8 frame path; asserts frame/count consistency (fail loud)."""
    import score_v0_31 as S31
    import score_v33 as S33
    PANEL = S31.PANEL
    base, v23 = lay["base"], lay["v23"]
    wave = {}
    for sub in ("v0.20", "v0.21", "v0.22"):
        rk, rp, mod, _ = S33.RECON_CFG[sub]
        d = base / SUBDIR[sub]
        counts, cells = S31.counts_raw_text(rk, rp, mod, d / "phase_b_results.csv")
        recog = S33.recog_raw(d / "phase_a_results.csv")
        fmap = {b: {} for b in counts}
        for r in S31.read_csv(d / "phase_b_results.csv"):
            m, fr, txt = r["model"], r["frame_id"], r["response_text"]
            if m not in PANEL:
                continue
            for b in counts:
                if mod.detect_mention(txt, b):
                    fmap[b].setdefault(m, set()).add(fr)
        wave[sub] = {"counts": counts, "recog": recog, "frames": fmap, "cells": cells}
    # v0.19 — parsed results.csv
    d = base / "v19"
    counts, cells = S31.counts_v19(d / "phase_b_results.csv")
    recog = S33.recog_v19(d / "phase_a_results.csv")
    fmap = {b: {} for b in counts}
    for r in S31.read_csv(d / "phase_b_results.csv"):
        b, m, fr = r["brand"], r["panel_model"], r["frame"]
        if m in PANEL and str(r["mentioned"]).strip() == "1":
            fmap[b].setdefault(m, set()).add(fr)
    wave["v0.19"] = {"counts": counts, "recog": recog, "frames": fmap, "cells": cells}
    # v0.23 — coded scored json (brand ids S01..)
    counts, cells = S31.counts_v23(v23 / "v23_phase_b_scored.json")
    recog, _ = S33.recog_v23(v23 / "v23_phase_a_scored.json")
    fmap = {b: {} for b in counts}
    for r in json.load(open(v23 / "v23_phase_b_scored.json")):
        m = r.get("model_id")
        if m not in PANEL:
            continue
        for b, v in (r.get("brand_mentions") or {}).items():
            if v:
                fmap.setdefault(b, {}).setdefault(m, set()).add(r.get("probe_id"))
    wave["v0.23"] = {"counts": counts, "recog": recog, "frames": fmap, "cells": cells}

    for sub in OMNI:                                  # geometry + frame/count consistency
        w = wave[sub]
        for b, vec in w["counts"].items():
            assert len(vec) == M and all(0 <= int(x) <= F for x in vec), f"{sub}/{b}: bad counts {vec}"
            for i, m in enumerate(PANEL):
                got = len(w["frames"].get(b, {}).get(m, ()))
                assert got == int(vec[i]), \
                    f"frame/count mismatch {sub}/{b}/{m}: frames={got} count={vec[i]}"
    return wave


def wave_metrics(wave, keep):
    """{sub: {brand: metrics}} on the kept panel indices."""
    import score_v0_31 as S31
    PANEL = S31.PANEL
    kept_models = [PANEL[i] for i in keep]
    out = {}
    for sub in OMNI:
        w = wave[sub]
        out[sub] = {}
        for b, vec in w["counts"].items():
            k = [int(vec[i]) for i in keep]
            rg = w["recog"].get(b, [0] * M)
            phi, pi, part = phi_m(k)
            J, nJ = jaccard_of({m: s for m, s in w["frames"].get(b, {}).items() if m in kept_models})
            out[sub][b] = {
                "k": k, "pi_hat": pi, "phi": phi, "phi_partition": part,
                "J": J, "J_n_models": nJ, "C_P": int(sum(int(rg[i]) for i in keep)),
                "cv_cpc": cv_cpc(k), "phantom": float(np.mean(k)) < FLOOR,
                "cell": w["cells"].get(b, ""),
            }
    return out


# ===========================================================================
# STEP 0 — PARITY GATES
# ===========================================================================
def gate_p1(t1m, ref_rows):
    """t1 phi reproduces the v1.8 instrument table (112 rows; definedness identical;
    |diff| <= 1e-9 where defined)."""
    mine = {(s, b): m for s in OMNI for b, m in t1m[s].items()}
    ref = {(r["substrate"], r["brand"]): r for r in ref_rows}
    problems = []
    if len(ref) != N_BRAND_UNITS or len(mine) != N_BRAND_UNITS:
        problems.append(f"row counts: recomputed {len(mine)}, reference {len(ref)}, expected {N_BRAND_UNITS}")
    if set(ref) != set(mine):
        problems.append(f"key sets differ: only recomputed {sorted(set(mine) - set(ref))[:5]}, "
                        f"only reference {sorted(set(ref) - set(mine))[:5]}")
    max_diff, k_mismatch = 0.0, 0
    for key in sorted(set(ref) & set(mine)):
        r, m = ref[key], mine[key]
        ref_def = str(r["phi_defined"]).strip() == "True"
        if ref_def != (m["phi"] is not None):
            problems.append(f"{key}: definedness ref={ref_def} recomputed={m['phi'] is not None}")
            continue
        if ref_def:
            d = abs(float(r["phi"]) - m["phi"])
            max_diff = max(max_diff, d)
            if d > P1_TOL:
                problems.append(f"{key}: phi ref={r['phi']} recomputed={m['phi']}")
        if json.loads(r["k_per_model"]) != m["k"]:
            k_mismatch += 1
    return {"gate": "P1", "passed": not problems, "rows_checked": len(set(ref) & set(mine)),
            "max_abs_diff": max_diff, "k_vector_mismatches_info_only": k_mismatch,
            "problems": problems[:20]}


def pooled_phi_pairs(wa, wb):
    xs, ys, gs, keys = [], [], [], []
    for s in OMNI:
        for b in wa[s]:
            if b in wb[s] and wa[s][b]["phi"] is not None and wb[s][b]["phi"] is not None:
                xs.append(wa[s][b]["phi"]); ys.append(wb[s][b]["phi"]); gs.append(s); keys.append((s, b))
    return np.array(xs), np.array(ys), np.array(gs), keys


def gate_p2(t1m, t2m, ref_verdicts):
    x, y, _, _ = pooled_phi_pairs(t1m, t2m)
    rho = spearman(x, y)
    rec = ref_verdicts["two_wave_reproducibility"]["phi_t1_t2_rank_agreement"]
    ok = (len(x) == P2_N == rec["n"]) and round(rho, 4) == P2_RHO == round(rec["rho"], 4)
    return {"gate": "P2", "passed": bool(ok), "rho": rho, "n": len(x),
            "reference": {"rho": rec["rho"], "n": rec["n"], "prereg": [P2_RHO, P2_N]}}


def gate_p3(t1m, t2m, v34):
    rows, problems = {}, []
    for s in OMNI:
        both = [b for b in t1m[s] if b in t2m[s]
                and t1m[s][b]["cv_cpc"] is not None and t2m[s][b]["cv_cpc"] is not None]
        rho = spearman([t1m[s][b]["cv_cpc"] for b in both], [t2m[s][b]["cv_cpc"] for b in both])
        ref = v34["per_substrate"][s]["cpc"]["rho"]
        ref_n = v34["per_substrate"][s]["cpc"]["n_defined_both"]
        if ref is None:
            ok = not np.isfinite(rho)
        else:
            ok = np.isfinite(rho) and abs(rho - ref) <= P3_TOL
        ok = ok and len(both) == ref_n
        rows[s] = {"rho": rho, "n": len(both), "ref_rho": ref, "ref_n": ref_n, "match": bool(ok)}
        if not ok:
            problems.append(s)
    return {"gate": "P3", "passed": not problems, "per_substrate": rows, "failed": problems}


def gate_p4():
    rows, problems = {}, []
    manifest = (ROOT / "osf/v41/prereg/acquisition_manifest_v41.md").read_text()
    for rel, want in PROBE_SHA256.items():
        got = sha256(ROOT / rel)
        ok = got == want and want in manifest
        rows[rel] = {"sha256": got, "match": ok}
        if not ok:
            problems.append(rel)
    return {"gate": "P4", "passed": not problems, "artifacts": rows, "failed": problems}


def check_references():
    out = {}
    for name, want in REF_FILES.items():
        got = sha256(REF_DIR / name)
        out[name] = {"sha256": got, "match": got == want}
    if not all(v["match"] for v in out.values()):
        raise GateFailure(f"frozen v1.8 reference files changed: {out}")
    return out


def run_gates(t1=None, t2=None, ref_rows=None, ref_verdicts=None, v34=None):
    """Returns (gates, t1 wave, t2 wave). Raises GateFailure on any failure.
    Arguments are injectable for the test suite; defaults read the frozen inputs."""
    refs = check_references() if ref_rows is None else {"injected": True}
    if ref_rows is None:
        ref_rows = list(csv.DictReader(open(REF_DIR / "v1_8_instrument_table.csv", newline="")))
    if ref_verdicts is None:
        ref_verdicts = json.load(open(REF_DIR / "v1_8_verdicts.json"))
    if v34 is None:
        v34 = json.load(open(V34_VERDICTS))
    t1 = t1 or load_wave(LAYOUT["t1"])
    t2 = t2 or load_wave(LAYOUT["t2"])
    full = list(range(M))
    t1m, t2m = wave_metrics(t1, full), wave_metrics(t2, full)
    gates = {"reference_files": refs,
             "P1": gate_p1(t1m, ref_rows), "P2": gate_p2(t1m, t2m, ref_verdicts),
             "P3": gate_p3(t1m, t2m, v34), "P4": gate_p4()}
    gates["all_passed"] = all(gates[g]["passed"] for g in ("P1", "P2", "P3", "P4"))
    if not gates["all_passed"]:
        raise GateFailure(json.dumps(_clean(gates), indent=2))
    return gates, t1, t2


# ===========================================================================
# manipulation checks (t3)
# ===========================================================================
def _norm_alias(a):
    return (a or "").strip().removeprefix("models/")


def _sidecar(path):
    if not Path(path).exists():
        return None
    return [r for r in csv.DictReader(open(path, newline="")) if "judge" not in r["phase"].lower()]


def mc_snapshot(sidecar_rows):
    if sidecar_rows is None:
        return {"status": "NOT_EVALUABLE", "reason": "t3 provenance sidecar absent", "mismatched": []}
    per = {}
    for a in DATED_ALIASES:
        ids = sorted({r["returned_model_id"] for r in sidecar_rows if _norm_alias(r["alias"]) == a})
        per[a] = {"t2": T2_SERVED[a], "t3": ids, "match": ids == [T2_SERVED[a]]}
    mism = [a for a, v in per.items() if not v["match"]]
    return {"status": "PASS" if not mism else "MISMATCH", "per_model": per,
            "n_match": len(DATED_ALIASES) - len(mism), "mismatched": mism}


def mc_truncation(sidecar_rows):
    if sidecar_rows is None:
        return {"status": "NOT_EVALUABLE"}
    per = {}
    for r in sidecar_rows:
        a = _norm_alias(r["alias"])
        d = per.setdefault(a, {"calls": 0, "truncated": 0, "finish_reason_missing": 0})
        d["calls"] += 1
        fr = (r.get("finish_reason") or "").strip()
        if not fr:
            d["finish_reason_missing"] += 1
        elif fr in TRUNC_REASONS or fr.split(".")[-1] in TRUNC_REASONS:
            d["truncated"] += 1
    for d in per.values():
        d["share_truncated"] = d["truncated"] / d["calls"] if d["calls"] else None
    return {"status": "DESCRIPTIVE", "per_model": per,
            "note": "t1/t2 recorded no finish reasons; no wave contrast"}


def mc_completeness(base, v23_dir):
    """Responses present per (substrate, phase, model) vs expected. 852 = 672 + 180."""
    import score_v0_31 as S31
    PANEL = S31.PANEL
    ok = {}

    def add(sub, ph, m, good):
        d = ok.setdefault((sub, ph, m), [0, 0])
        d[0] += 1
        d[1] += int(bool(good))

    for ph, fn in (("A", "phase_a_responses.jsonl"), ("B", "phase_b_responses.jsonl")):
        p = base / "v19" / fn
        if p.exists():
            for line in open(p):
                if line.strip():
                    o = json.loads(line)
                    add("v0.19", ph, o.get("panel_model"), (o.get("response") or "").strip() and not o.get("error"))
    for sub in ("v0.20", "v0.21", "v0.22"):
        for ph, fn in (("A", "phase_a_results.csv"), ("B", "phase_b_results.csv")):
            p = base / SUBDIR[sub] / fn
            if p.exists():
                for r in S31.read_csv(p):
                    add(sub, ph, r["model"], (r.get("response_text") or "").strip())
    for ph, fn in (("A", "v23_phase_a_raw.json"), ("B", "v23_phase_b_raw.json")):
        p = v23_dir / fn
        if p.exists():
            for r in json.load(open(p)):
                add("v0.23", ph, r.get("model_id"),
                    r.get("status") == "ok" and (r.get("response") or "").strip())
    expected = {}
    for sub in OMNI:
        for m in PANEL:
            expected[(sub, "A", m)] = EXPECTED_BRANDS[sub]
            expected[(sub, "B", m)] = F
    per_model = {m: {"expected": 0, "ok": 0} for m in PANEL}
    cells = []
    for key, exp in expected.items():
        got = ok.get(key, [0, 0])[1]
        per_model[key[2]]["expected"] += exp
        per_model[key[2]]["ok"] += min(got, exp)
        if got != exp:
            cells.append({"substrate": key[0], "phase": key[1], "model": key[2], "expected": exp, "ok": got})
    total_ok = sum(v["ok"] for v in per_model.values())
    unavailable = [m for m, v in per_model.items() if v["ok"] == 0]
    partial = [m for m, v in per_model.items() if 0 < v["ok"] < v["expected"]]
    return {"expected_total": sum(expected.values()), "ok_total": total_ok,
            "status": "PASS" if total_ok == sum(expected.values()) and not cells else "INCOMPLETE",
            "per_model": per_model, "unavailable_models": unavailable,
            "partially_failed_models": partial, "short_cells": cells[:40]}


# ===========================================================================
# hypotheses
# ===========================================================================
def frame_shuffle_null(w2, t3, keep, obs, seed=SEED_FRAME, draws=None):
    """SCORER_NOTES S2. Null for 'phi keeps its brand order because models keep their
    consistency patterns': the kept models' t3 answers are permuted WITHIN every
    (substrate, frame) — one permutation per frame, applied to every brand, since a
    model's answer covers all brands — so each frame keeps which brands it elicits and
    pi_hat is preserved exactly, while model identity is scrambled. The statistic is
    re-taken as in H_Phi (pooled Spearman, phi-defined in both). p_frame = (#null >= obs
    + 1) / (draws + 1)."""
    import score_v0_31 as S31
    draws = draws or N_FRAME
    kept = [S31.PANEL[i] for i in keep]
    rng = np.random.default_rng(seed)
    prep = []
    for s in OMNI:
        fr = sorted({f for b in t3[s]["frames"].values() for m, fs in b.items() if m in kept for f in fs}, key=str)
        fidx = {f: i for i, f in enumerate(fr)}
        brands = []
        for b in t3[s]["counts"]:
            if b in w2[s] and w2[s][b]["phi"] is not None:
                hits = [(kept.index(m), fidx[f]) for m, fs in t3[s]["frames"].get(b, {}).items()
                        if m in kept for f in fs]
                brands.append((w2[s][b]["phi"], np.array(hits, int).reshape(-1, 2)))
        prep.append((len(fr), brands))
    nulls = np.empty(draws)
    for d in range(draws):
        xs, ys = [], []
        for nf, brands in prep:
            perm = np.array([rng.permutation(len(kept)) for _ in range(nf)]).reshape(nf, len(kept))
            for phi2, hits in brands:
                k = np.zeros(len(kept), int)
                if len(hits):
                    np.add.at(k, perm[hits[:, 1], hits[:, 0]], 1)
                p3 = phi_m(list(k))[0]
                if p3 is not None:
                    xs.append(phi2); ys.append(p3)
        nulls[d] = spearman(xs, ys)
    nulls = nulls[np.isfinite(nulls)]
    p = (np.sum(nulls >= obs - 1e-12) + 1) / (len(nulls) + 1)
    return {"p_frame": float(p), "null_mean": float(nulls.mean()), "null_p95": float(np.percentile(nulls, 95)),
            "null_max": float(nulls.max()), "draws": int(len(nulls)), "seed": seed}


def h_phi_long(w2, w3, seed=SEED_PHI, frame_null=None):
    x, y, g, keys = pooled_phi_pairs(w2, w3)
    n = len(x)
    rho = spearman(x, y)
    if n < PHI_N_FLOOR:
        return {"verdict": "UNDETERMINED", "reason": f"n={n} < {PHI_N_FLOOR}", "rho": rho, "n": n}
    if not np.isfinite(rho):
        return {"verdict": "UNDETERMINED", "reason": "degenerate (no rank variance)", "rho": rho, "n": n}
    p = perm_p(x, y, g, rho, seed, "one")
    fn = frame_null(rho) if callable(frame_null) else frame_null
    beats_frames = True if fn is None else fn["p_frame"] < P_ALPHA
    if rho >= PHI_CONF and p < P_ALPHA and beats_frames:
        v = "CONFIRMED"
    elif rho < PHI_FALS or p >= P_ALPHA:
        v = "FALSIFIED"
    else:
        v = "MARGINAL"
    loso = {}
    for s in OMNI:
        keep = g != s
        loso[s] = spearman(x[keep], y[keep])
    finite = [r for r in loso.values() if np.isfinite(r)]
    return {"verdict": v, "rho": rho, "p_perm": p, "p_mc_se": mc_se(p), "n": n,
            "frame_structure_null": fn,
            "rule": "CONFIRMED iff rho >= 0.50 AND p_perm < .05 AND p_frame < .05 (SCORER_NOTES S2); "
                    "FALSIFIED iff rho < 0.30 OR p_perm >= .05; else MARGINAL",
            "n_per_substrate": {s: int(np.sum(g == s)) for s in OMNI},
            "sensitivity": {
                "pooled_within_substrate_rank_rho": pooled_within_rho(x, y, g),
                "leave_one_substrate_out": loso,
                "loso_range": [min(finite), max(finite)] if finite else None}}


def h_presence_long(w2, w3, seed=SEED_PRESENCE):
    rng_seeds = np.random.SeedSequence(seed).spawn(len(OMNI))
    per = {}
    for s, ss in zip(OMNI, rng_seeds):
        brands = [b for b in w2[s] if b in w3[s]]
        a = [w2[s][b]["pi_hat"] for b in brands]
        b3 = [w3[s][b]["pi_hat"] for b in brands]
        rho = spearman(a, b3)
        p = perm_p(a, b3, ["all"] * len(a), rho, ss, "one") if np.isfinite(rho) else float("nan")
        per[s] = {"rho": rho, "p_perm": p, "n": len(brands)}
    n_conf = sum(1 for d in per.values() if np.isfinite(d["rho"]) and d["rho"] >= PRES_CONF)
    n_fals = sum(1 for d in per.values() if np.isfinite(d["rho"]) and d["rho"] < PRES_FALS)
    v = "CONFIRMED" if n_conf >= PRES_CONF_K else "FALSIFIED" if n_fals >= PRES_FALS_K else "MARGINAL"
    return {"verdict": v, "n_ge_070": n_conf, "n_lt_050": n_fals,
            "n_undefined": sum(1 for d in per.values() if not np.isfinite(d["rho"])),
            "per_substrate": per}


def _three_wave_units(w1, w2, w3, key, require_defined):
    rows = []
    for s in OMNI:
        for b in w1[s]:
            if b in w2[s] and b in w3[s]:
                v = (w1[s][b][key], w2[s][b][key], w3[s][b][key])
                if require_defined and any(x is None for x in v):
                    continue
                rows.append((s, b) + v)
    return rows


def _decay(rows, stat, n_floor, seed):
    g = np.array([r[0] for r in rows])
    v1 = np.array([r[2] for r in rows], float)
    v2 = np.array([r[3] for r in rows], float)
    v3 = np.array([r[4] for r in rows], float)
    n = len(rows)
    r12, r13 = stat(v1, v2, g), stat(v1, v3, g)
    D = r12 - r13
    out = {"n": n, "rho_t1_t2": r12, "rho_t1_t3": r13, "D": D}
    if n_floor and n < n_floor:
        return {**out, "verdict": "UNDETERMINED", "reason": f"n={n} < {n_floor}"}
    if not np.isfinite(D):
        return {**out, "verdict": "UNDETERMINED", "reason": "degenerate (no rank variance)"}
    rng = np.random.default_rng(seed)
    gidx = _group_index(g)
    boots, dropped = [], 0
    for _ in range(N_BOOT):
        idx = np.concatenate([rng.choice(gi, size=len(gi), replace=True) for gi in gidx])
        d = stat(v1[idx], v2[idx], g[idx]) - stat(v1[idx], v3[idx], g[idx])
        if np.isfinite(d):
            boots.append(d)
        else:
            dropped += 1
    lo, hi = np.percentile(boots, [2.5, 97.5])
    v = "CONFIRMED" if lo > 0 else "FALSIFIED" if hi < 0 else "MARGINAL"
    return {**out, "ci95": [float(lo), float(hi)], "boot_dropped_degenerate": dropped, "verdict": v}


def h_horizon_decay(w1, w2, w3):
    phi_rows = _three_wave_units(w1, w2, w3, "phi", True)
    pi_rows = _three_wave_units(w1, w2, w3, "pi_hat", True)
    phi = _decay(phi_rows, lambda a, b, g: spearman(a, b), PHI_N_FLOOR, SEED_BOOT)
    pi = _decay(pi_rows, pooled_within_rho, None, SEED_BOOT)
    return {"phi": phi, "pi_hat": pi, "reported_alongside": horizon_table(w1, w2, w3)}


def horizon_table(w1, w2, w3):
    waves = {"t1": w1, "t2": w2, "t3": w3}
    out = {}
    for metric, pooled_raw in (("phi", True), ("pi_hat", False), ("J", True), ("C_P", False)):
        out[metric] = {}
        for a, b in (("t1", "t2"), ("t2", "t3"), ("t1", "t3")):
            xs, ys, gs = [], [], []
            for s in OMNI:
                for br in waves[a][s]:
                    if br in waves[b][s]:
                        va, vb = waves[a][s][br][metric], waves[b][s][br][metric]
                        if va is not None and vb is not None:
                            xs.append(va); ys.append(vb); gs.append(s)
            rho = spearman(xs, ys) if pooled_raw else pooled_within_rho(xs, ys, gs)
            out[metric][f"{a}_{b}"] = {"rho": rho, "n": len(xs),
                                       "statistic": "pooled Spearman" if pooled_raw
                                       else "pooled within-substrate-rank Spearman"}
    return out


def h_drift(w2, w3, seed=SEED_DRIFT):
    _, _, g, keys = pooled_phi_pairs(w2, w3)
    n = len(keys)
    if n < PHI_N_FLOOR:
        return {"verdict": "UNDETERMINED", "reason": f"n={n} < {PHI_N_FLOOR}", "n": n}
    phi2 = [w2[s][b]["phi"] for s, b in keys]; phi3 = [w3[s][b]["phi"] for s, b in keys]
    pi2 = [w2[s][b]["pi_hat"] for s, b in keys]; pi3 = [w3[s][b]["pi_hat"] for s, b in keys]
    dphi = within_pct(phi3, g) - within_pct(phi2, g)
    dpi = within_pct(pi3, g) - within_pct(pi2, g)
    rho = spearman(dphi, dpi)
    if not np.isfinite(rho):
        return {"verdict": "UNDETERMINED", "reason": "degenerate (no change in one component)", "n": n,
                "rho": rho}
    p = perm_p(dphi, dpi, g, rho, seed, "two")
    if abs(rho) <= DRIFT_CONF:
        v = "CONFIRMED"
    elif abs(rho) >= DRIFT_FALS and p < P_ALPHA:
        v = "FALSIFIED"
    else:
        v = "MARGINAL"
    # Descriptive (SCORER_NOTES S4): both deltas share the t2 baseline, so a t2 coupling
    # between phi and pi_hat ranks induces delta coupling with no co-movement at all.
    base = spearman(within_pct(phi2, g), within_pct(pi2, g))
    return {"verdict": v, "rho": rho, "p_perm_two_sided": p, "p_mc_se": mc_se(p), "n": n,
            "baseline_coupling_t2_rho": base,
            "baseline_note": "rho(phi_t2, pi_hat_t2) on within-substrate percentile ranks; "
                             "descriptive, not verdict-bearing"}


def h_phantom(w2, w3):
    per, tot_ph, tot_ret = {}, 0, 0
    for s in OMNI:
        ph = [b for b in w2[s] if b in w3[s] and w2[s][b]["phantom"]]
        ret = [b for b in ph if w3[s][b]["phantom"]]
        per[s] = {"t2_phantom": len(ph), "retained_t3": len(ret),
                  "proportion": len(ret) / len(ph) if ph else None}
        tot_ph += len(ph); tot_ret += len(ret)
    return {"verdict": "DESCRIPTIVE", "per_substrate": per,
            "pooled": {"t2_phantom": tot_ph, "retained_t3": tot_ret,
                       "proportion": tot_ret / tot_ph if tot_ph else None},
            "v0_34_reference_t1_t2": "56/57"}


# ===========================================================================
# delta t
# ===========================================================================
def _first_dates(sidecar_path):
    if not Path(sidecar_path).exists():
        return {}
    first = {}
    for r in csv.DictReader(open(sidecar_path, newline="")):
        sub = "v0." + r["substrate"].lstrip("v")
        try:
            ts = datetime.fromisoformat(r["timestamp"].replace("Z", "+00:00"))
        except Exception:
            continue
        if sub not in first or ts < first[sub]:
            first[sub] = ts
    return {k: v.date().isoformat() for k, v in first.items()}


def delta_t(sidecar3):
    t2 = _first_dates(DATA2 / "v34_provenance.csv")
    t3 = _first_dates(sidecar3)
    rows = []
    for s in OMNI:
        r = {"substrate": s, "t1": T1_DATE[s], "t2": t2.get(s), "t3": t3.get(s)}
        for a, b in (("t1", "t2"), ("t2", "t3"), ("t1", "t3")):
            try:
                r[f"days_{a}_{b}"] = (date.fromisoformat(r[b]) - date.fromisoformat(r[a])).days
            except Exception:
                r[f"days_{a}_{b}"] = None
        rows.append(r)
    return rows


# ===========================================================================
# orchestration
# ===========================================================================
def score_all(t1, t2, t3, keep):
    w1, w2, w3 = (wave_metrics(w, keep) for w in (t1, t2, t3))
    hyps = {
        "H_Phi_LongHorizon": {"tier": "PRIMARY", **h_phi_long(
            w2, w3, frame_null=lambda obs: frame_shuffle_null(w2, t3, keep, obs))},
        "H_Presence_LongHorizon": {"tier": "PRIMARY", **h_presence_long(w2, w3)},
        "H_Horizon_Decay": {"tier": "SECONDARY", **h_horizon_decay(w1, w2, w3)},
        "H_Drift_Dissociation": {"tier": "SECONDARY", **h_drift(w2, w3)},
        "H_Phantom_LongPersistence": {"tier": "TERTIARY (descriptive)", **h_phantom(w2, w3)},
    }
    return hyps, (w1, w2, w3)


def three_wave_rows(waves):
    rows = []
    for s in OMNI:
        for b in sorted(waves[0][s]):
            for name, w in zip(("t1", "t2", "t3"), waves):
                if b not in w[s]:
                    continue
                m = w[s][b]
                rows.append({"substrate": s, "brand": b, "cell": m["cell"], "wave": name,
                             "k_per_model": json.dumps(m["k"]), "pi_hat": m["pi_hat"],
                             "phi": m["phi"], "phi_partition": m["phi_partition"], "J": m["J"],
                             "J_n_models": m["J_n_models"], "C_P": m["C_P"], "cv_cpc": m["cv_cpc"],
                             "phantom": m["phantom"]})
    return rows


def score(lay3, t1=None, t2=None, gates=None):
    import score_v0_31 as S31
    PANEL = S31.PANEL
    if gates is None:
        gates, t1, t2 = run_gates()                        # STEP 0: halts on failure
    sidecar3 = lay3["base"] / "v41_provenance.csv"
    side = _sidecar(sidecar3)
    mcs = {"MC_ProbeParity": {"status": "PASS" if gates["P4"]["passed"] else "FAIL",
                              "source": "PARITY P4 recomputed at scoring"},
           "MC_Snapshot": mc_snapshot(side),
           "MC_Completeness": mc_completeness(lay3["base"], lay3["v23"]),
           "MC_Truncation": mc_truncation(side)}
    comp = mcs["MC_Completeness"]
    if comp["partially_failed_models"]:
        raise Halt("residual failures on " + ", ".join(comp["partially_failed_models"]) +
                   ": resolve them with logged retries (v0.34 precedent) or record a DEVIATIONS "
                   "decision before scoring; see SCORER_NOTES S7.")
    dropped = comp["unavailable_models"]
    keep = [i for i, m in enumerate(PANEL) if m not in dropped]
    if len(keep) < MIN_PANEL:
        raise Halt(f"only {len(keep)} models available at t3 (< {MIN_PANEL}): phase halts for re-scope")
    t3 = load_wave(lay3)
    hyps, waves = score_all(t1, t2, t3, keep)

    sens = None
    mism = mcs["MC_Snapshot"].get("mismatched", [])
    if mism:
        keep_s = [i for i in keep if PANEL[i] not in mism]
        if len(keep_s) >= MIN_PANEL:
            h2, _ = score_all(t1, t2, t3, keep_s)
            sens = {"without_models": mism,
                    "verdicts": {k: v.get("verdict") for k, v in h2.items()},
                    "H_Phi_LongHorizon": {k: h2["H_Phi_LongHorizon"].get(k) for k in ("rho", "p_perm", "n")},
                    "H_Presence_LongHorizon": h2["H_Presence_LongHorizon"]["per_substrate"]}
        else:
            sens = {"without_models": mism, "note": f"fewer than {MIN_PANEL} models remain; not computed"}

    out = {
        "phase": PHASE_ID, "title": "Long-Horizon Stability t1->t2->t3", "prereg_tag": PREREG_TAG,
        "locks": {"presence": "v1.6", "consistency": "v1.8"},
        "panel": PANEL, "panel_used": [PANEL[i] for i in keep], "models_dropped": dropped,
        "seeds": {"phi": SEED_PHI, "bootstrap": SEED_BOOT, "presence": SEED_PRESENCE, "drift": SEED_DRIFT},
        "mc_draws": N_PERM, "bootstrap_resamples": N_BOOT,
        "parity_gates": gates,
        "manipulation_checks": mcs,
        "verdicts": hyps,
        "snapshot_sensitivity": sens,
        "delta_t": delta_t(sidecar3),
    }
    return out, waves


def _clean(o):
    if isinstance(o, (float, np.floating)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    return o


def write_outputs(out, waves, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    json.dump(_clean(out), open(outdir / "v41_verdicts.json", "w"), indent=2, allow_nan=False)
    rows = three_wave_rows(waves)
    with open(outdir / "v41_three_wave_table.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if v is None else v) for k, v in r.items()})
    return outdir


def _tag_exists():
    r = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "-q", "--verify", f"refs/tags/{PREREG_TAG}"],
                       capture_output=True, text=True)
    return r.returncode == 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--parity-only", action="store_true")
    g.add_argument("--synthetic", metavar="DIR")
    g.add_argument("--run", action="store_true")
    ap.add_argument("--out", metavar="DIR", help="override the output folder (parity-only/synthetic)")
    a = ap.parse_args()
    try:
        if a.parity_only:
            gates, _, _ = run_gates()
            p = Path(a.out) if a.out else ROOT / "osf/v41/prereg"
            p.mkdir(parents=True, exist_ok=True)
            json.dump(_clean(gates), open(p / "parity_gates_v0_41.json", "w"), indent=2, allow_nan=False)
            print(f"parity gates P1-P4: PASS -> {p / 'parity_gates_v0_41.json'}")
            return 0
        if a.synthetic:
            base = Path(a.synthetic).resolve()
            out, waves = score(_layout(base, base / "v23"))
            d = write_outputs(out, waves, Path(a.out) if a.out else base / "_score")
        else:
            if not _tag_exists():
                print(f"[v41] refusing --run: tag {PREREG_TAG} does not exist (lock first)", file=sys.stderr)
                return 3
            out, waves = score(_layout(DATA3, DATA3 / "v23"))
            d = write_outputs(out, waves, ROOT / "osf/v41")
    except GateFailure as e:
        print("[v41] PARITY GATE FAILURE — halted before any t3 statistic\n" + str(e), file=sys.stderr)
        return 2
    except Halt as e:
        print(f"[v41] HALT: {e}", file=sys.stderr)
        return 4
    print(f"wrote {d}")
    for k, v in out["verdicts"].items():
        if k == "H_Horizon_Decay":
            print(f"  {k}: phi {v['phi']['verdict']} / pi_hat {v['pi_hat']['verdict']}")
        else:
            print(f"  {k}: {v['verdict']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
