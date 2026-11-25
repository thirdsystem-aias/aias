#!/usr/bin/env python3
"""v1.22 Grounding Paper B scorer (pre-registration draft r1, 2026-11-25).

Computes every pre-registered test of v1.22 from per-wave inputs, with v1.13's locked scorer imported unchanged
(osf/methodology/v1_13/scripts/score_v1_13.py, SHA-256 pinned below) for every shared definition: answers, sources,
D_b, G*, floors, rho_w, permutation and bootstrap drivers, separability and reliability verdicts, MQ checks.

  section 1   paper_b_route / decision record: MARGINAL Paper A gate -> runs only on Pablo's dated, worded decision.
  HB1, HB4    separability of G*_t5 from P_t5 and C*_t5 (S1 and S0 legs), v1.13's H1/H2 rule (imported).
  HB2         t4 -> t5 retest of G*, computed by v0.45's own component_leg (loaded from tag v0.45-prereg-r1),
              so that it is v0.45 section 2.6's Grounding leg ("one test, one owner", C4); PARTIAL = MARGINAL.
  HB3         v1.13's H3 on t5's three runs (imported reliability_test / reliability_verdict).
  GB          gate completion rule (section 3.5).
  HB44(b)     SDRI x G*_pool (G*_t5), one-sided, v1.13 H7 bands.
  HB45        Stage 2: t5 -> t6 and t4 -> t6 retests, v0.45's statistic with this study's seeds.
  HB46(b)     pooled within-category Cliff's delta of G*_pool, F vs non-F (and on rank residuals given P_S1).
  HB47(b)     mean within-brand channel difference d_b (sign-flip test); rho_w(IL, G*_pool).
  HB48(b)     replication of the six-class source profile t4 -> t5; typology on the pooled profile.
  D44-D48, MQ, sensitivities (section 7).

Modes
  --stage 1 / --stage 2   real data; refused unless tag v1.22-prereg-r1 is on origin, the anchor names its commit,
                          Pablo's decision record is valid, v0.45's acquisition tag exists and the output folder is
                          empty -- all checked BEFORE any t5 (or t6) file is opened.
  --check-t4-parity       B-P1 on archived t4 only (reproduces Paper A's published G* and H1/H2 statistics).
  --dry-run DIR           synthetic worlds only (dryrun_v1_22.py); no network, no key, no real answer.
Nothing here calls a model.
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
import os
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage

HERE = Path(__file__).resolve().parent
PHASE = HERE.parent
REPO = PHASE.parents[2]
V113_SCRIPTS = REPO / "osf/methodology/v1_13/scripts"
sys.path.insert(0, str(V113_SCRIPTS))
import score_v1_13 as A  # noqa: E402  (Paper A's locked scorer, imported unchanged)

PHASE_ID = "v1.22"
PREREG_TAG = "v1.22-prereg-r1"
V113_SCORER = V113_SCRIPTS / "score_v1_13.py"
V113_SCORER_SHA256 = "fee2e5530030730ca964bb080840db4ca3b66b68b8c1d1ae3bb988dbd17a8641"
V113_MANIFEST = REPO / "osf/methodology/v1_13/prereg/LOCK_MANIFEST_v1_13.sha256"
V113_VERDICTS = REPO / "osf/methodology/v1_13/v1_13_verdicts.json"
V113_SDRI = REPO / "osf/methodology/v1_13/audit/v1_13_sdri.csv"
ROSTER_REF = ("v1.19-prereg-r1", "osf/methodology/v1_19/prereg/phantom_roster_v1_19.csv")
PHANTOM_ROSTER_SHA256 = "9b67e89231f4cab8ef6916a04acb886e8bab723fe71f4b308f9406938cb873cb"
PROBES_REF = ("v0.42-prereg-r1", "osf/v42/prereg/probes_v0_42.jsonl")
V045_TAG, V045_ACQ_TAG = "v0.45-prereg-r1", "v0.45-acquisition-locked"
V045_SCORER_PATH = "osf/v45/scripts/score_v0_45.py"
DECISION_FILE = PHASE / "anchor" / "pablo_decision_paper_B.json"
ANCHOR = PHASE / "anchor" / "osf_anchor_v1_22.json"
OUT_DIR = PHASE / "outputs"
CONDITIONAL_LABEL = "conditional on a MARGINAL Paper A gate (H1 MARGINAL, H3 UNDETERMINED)"
POOL_LABEL = "partly seen (t4 half published in Paper A)"

SEEDS = {"HB1": 122001, "HB2": 450046, "HB3": 122003, "HB4": 122004,
         "HB44": 122441, "HB44b": 122442, "HB45_t5t6": 122451, "HB45_t4t6": 122452,
         "HB46": 122461, "HB46b": 122462, "HB47": 122471, "HB47b": 122472,
         "HB48": 122481, "HB48b_full": 122482, "HB48b_resid": 122483}
DRY_RUN_SEEDS = (122490, 122491, 122492, 122493, 122494)
N_PERM, N_BOOT, HB2_N_BOOT = 10_000, A.N_BOOT, 10_000     # report-only intervals: v1.13's sep_leg (its seed
#                                                            113008, 2,000 draws); HB2 / HB45: v0.45's (10,000)
GAP_B, K_MAX = 500, 8
FLOOR_UNITS, MIN_PER_CAT = A.FLOOR_UNITS, A.MIN_UNITS_PER_SUB          # 30, 5
PH_MIN, PH_MIN_CATS, DELTA_CONF, DELTA_FALS = 10, 3, 0.30, 0.15        # HB46 (v1.19 H34 bands)
CH_MIN_G, CH_N, CH_MIN_CAT, CH_CONF, CH_FALS = 3, 20, 3, 5.0, 2.0     # HB47 (C9)
IL_N, IL_CONF, IL_FALS = 45, 0.30, 0.15                                # HB47b (v0.37 / v1.19 H35)
REP_CONF, REP_FALS = 0.20, 0.10                                        # HB48 (v1.19 D9, C9)
SIL_MIN, SIL_PCT, ARI_MIN, ARI_P = 0.25, 95, 0.30, 0.01               # HB48b (v1.19 section 7.3)
ALPHA, TOL, NAN = 0.05, A.TOL, float("nan")
TRIO = ("v20", "v21", "v22")
CATS = A.SUBSTRATES
N3 = A.PANELS["N3"]
CHANNEL_OF_LABEL = {"R_cat": "cat", "R_cult": "cult",                               # trio (v0.20-v0.22)
                    "category_anchored": "cat", "cultural_footprint": "cult",         # v0.19 (S-AllChannels)
                    "editorial-authority": "cat", "cultural-cult": "cult"}            # v0.23 (S-AllChannels)
PROFILE_CLASSES = ("brand_owned", "reference", "forum_ugc", "news", "review_editorial", "retailer")
COI_BRANDS = (("v19", "Denon"), ("v22", "Chevrolet"), ("v22", "BMW"), ("v22", "Bentley"),
              ("v23", "Jack Daniel's"), ("v20", "Eucerin"))
DEFUNCT = ("Pontiac", "Oldsmobile", "Plymouth", "Mercury", "Saturn")

C, M, F, U = "CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED"


class Refused(SystemExit):
    pass


def _f(v):
    return A._finite(v)


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def git(*args, check=False):
    r = subprocess.run(["git", *args], cwd=str(REPO), capture_output=True)
    if check and r.returncode:
        raise Refused(f"git {' '.join(args)} failed: {r.stderr.decode(errors='replace').strip()}")
    return r.stdout if r.returncode == 0 else None


def git_show(ref, path):
    out = git("show", f"{ref}:{path}")
    if out is None:
        raise Refused(f"cannot read {path} at {ref}")
    return out


# =========================================================================== section 1: conditionality
def paper_b_route(paper_a_verdict, decision):
    """Return 'RUN', 'NOT_RUN_PENDING', 'NOT_RUN_DECLINED' or 'REFUSED'."""
    if paper_a_verdict != "MARGINAL":
        return "REFUSED"
    if not decision:
        return "NOT_RUN_PENDING"
    if not (decision.get("date") and decision.get("text")) or "go" not in decision:
        return "NOT_RUN_PENDING"
    return "RUN" if decision["go"] is True else "NOT_RUN_DECLINED"


def read_decision(path=DECISION_FILE):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def paper_a_verdict(path=V113_VERDICTS):
    try:
        doc = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None, None
    return ((doc.get("gate") or {}).get("verdict")), doc


def not_run_record(route, verdict_path=V113_VERDICTS, verdict=None):
    p = Path(verdict_path)
    return {"phase": PHASE_ID, "prereg_tag": PREREG_TAG, "status": route, "paper_A_verdict": verdict,
            "paper_A_verdict_file": str(p), "paper_A_verdict_sha256": sha256_file(p) if p.exists() else None,
            "statistics": None, "note": "No v1.22 statistic was computed (section 1)."}


# =========================================================================== decision tables (sections 3.2-3.6)
def retest_verdict(rho, p, n):
    """HB2 / HB45 bands (v0.45 section 2.6); v0.45's PARTIAL is MARGINAL here."""
    if rho is None or not _f(rho) or n < 30 or p is None or not _f(p):
        return U
    if rho >= 0.50 and p < 0.05:
        return C
    if rho < 0.30:
        return F
    return M


def from_v045(v):
    return {"PARTIAL": M}.get(v, v)


def reliability_condition(hb2, hb3):
    vs = (hb2, hb3)
    if C in vs and F in vs:
        return "MIXED"
    if C in vs:
        return "MET"
    if F in vs:
        return "FAILED"
    return "OPEN"


def gate_completion(hb1, hb2, hb3, hb4):
    r = reliability_condition(hb2, hb3)
    if hb1 == F or r == "FAILED" or hb4 == F:
        return "FAIL"
    if hb1 == C and r == "MET":
        return "PASS"
    if hb1 == U or (r == "OPEN" and hb2 == U and hb3 == U):
        return "UNDETERMINED"
    return "MARGINAL"


def one_sided_assoc_verdict(rho, p, n, floor=30):
    """#44 (v1.13 H7 bands)."""
    if rho is None or not _f(rho) or n < floor:
        return U
    if rho >= 0.30 and p is not None and p < 0.05:
        return C
    if rho <= 0.10:
        return F
    return M


def signed_band_verdict(stat, p, enough, predicted_sign, conf=0.30, null=0.15):
    """#46 (Cliff's delta, v1.19 H34) and #47b (rho_w, v1.19 H35): sign split."""
    if not enough or stat is None or not _f(stat):
        return U
    if abs(stat) >= conf and p is not None and p < 0.05:
        return C if (stat > 0) == (predicted_sign > 0) else "CONFIRMED_REVERSED"
    if abs(stat) < null:
        return F
    return M


def channel_verdict(dbar, p, n, min_cat_units):
    """#47 primary: mean within-brand difference, percentage points (C9 bands)."""
    if dbar is None or not _f(dbar) or n < CH_N or min_cat_units < CH_MIN_CAT:
        return U
    if dbar >= CH_CONF and p < 0.05:
        return C
    if dbar < CH_FALS:
        return F
    return M


def replication_verdict(r, p, n):
    """#48 primary (v1.19 D9 bands)."""
    if r is None or not _f(r) or n < 30:
        return U
    if r >= REP_CONF and p < 0.05:
        return C
    if r < REP_FALS or p >= 0.05:
        return F
    return M


# =========================================================================== frozen design inputs
def load_roster(data=None):
    """F (recall-floor flags) and D (defunct) from v1.19's frozen roster, imported by hash."""
    raw = data if data is not None else git_show(*ROSTER_REF)
    if sha256_bytes(raw) != PHANTOM_ROSTER_SHA256:
        raise Refused("B-P0: phantom roster SHA-256 differs from 9b67e892...")
    rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8"))))
    return rows


def roster_flags(units, rows=None):
    """{unit: {'F': bool, 'D': bool}} keyed on v1.13 units through (coder substrate, coder key)."""
    rows = rows if rows is not None else load_roster()
    byc = A._by_coder(units)
    out, missing = {}, []
    for r in rows:
        k = byc.get((r["substrate"], r["brand"]))
        if k is None:
            missing.append((r["substrate"], r["brand"]))
            continue
        out[k] = {"F": r["recall_floor_flag_F"] == "1", "D": r["defunct_D"] == "1"}
    if missing:
        raise Refused(f"roster rows without a v1.13 unit: {missing}")
    return out


def load_channels(data=None):
    """{(substrate 'v19', Phase B probe_id): 'cat' | 'cult'} from v0.42's probe file; the raw label is kept too."""
    raw = data if data is not None else git_show(*PROBES_REF)
    out, labels = {}, {}
    for line in raw.decode("utf-8").splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        if d.get("phase") == "B" and d.get("channel"):
            if d["channel"] not in CHANNEL_OF_LABEL:
                raise Refused(f"unknown channel label {d['channel']!r}")
            out[(d["substrate"], d["probe_id"])] = CHANNEL_OF_LABEL[d["channel"]]
            labels[(d["substrate"], d["probe_id"])] = d["channel"]
    return out, labels


def coi_keys(units):
    names = {(u["substrate"], u["brand"]): k for k, u in units.items()}
    keys = [names[nb] for nb in COI_BRANDS if nb in names]
    if len(keys) != len(COI_BRANDS):
        raise Refused(f"COI units not all found: {[nb for nb in COI_BRANDS if nb not in names]}")
    return tuple(keys)


# =========================================================================== v0.45's locked scorer (HB2, HB45)
_V045 = {}


def load_v045():
    """v0.45's score_v0_45 module exactly as at tag v0.45-prereg-r1 (the tag's tree is extracted once to a cache
    folder; the scorer's bytes are checked against the tag's blob). Its imports need the tag's whole tree."""
    if "mod" in _V045:
        return _V045["mod"]
    commit = (git("rev-parse", f"{V045_TAG}^{{commit}}") or b"").decode().strip()
    if not commit:
        raise Refused(f"tag {V045_TAG} not found: HB2 is v0.45's own test and cannot run without it (C4)")
    blob = git_show(V045_TAG, V045_SCORER_PATH)
    cache = Path(tempfile.gettempdir()) / f"aias_v122_v045_{commit[:12]}"
    target = cache / V045_SCORER_PATH
    done = cache / ".v122_extracted"
    if not (done.exists() and target.exists() and target.read_bytes() == blob):
        cache.mkdir(parents=True, exist_ok=True)
        tar = subprocess.run(["git", "archive", "--format=tar", V045_TAG], cwd=str(REPO), capture_output=True,
                             check=True).stdout
        with tarfile.open(fileobj=io.BytesIO(tar)) as tf:      # the tree's one symlink is skipped (not imported)
            tf.extractall(cache, filter=lambda m, p: None if (m.issym() or m.islnk()) else tarfile.data_filter(m, p))
        done.write_text(commit, encoding="utf-8")
    if target.read_bytes() != blob:
        raise Refused("v0.45 scorer bytes differ from the tag's blob")
    sys.path.insert(0, str(target.parent))
    # v0.42's coder (imported by v0.45) re-executes the whole process with HOME shimmed unless ~/aias resolves to
    # its tree root; the same shim is set here for the import only, so nothing is re-executed. ROOT is the tag tree.
    shim = Path(tempfile.mkdtemp(prefix="v122_home_"))
    (shim / "aias").symlink_to(cache.resolve())
    saved = {k: os.environ.get(k) for k in ("HOME", "AIAS_ROOT")}
    os.environ["HOME"], os.environ["AIAS_ROOT"] = str(shim), str(cache.resolve())
    cwd = os.getcwd()
    try:
        import score_v0_45 as SC  # noqa: E402
    finally:
        os.chdir(cwd)
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    _V045.update(mod=SC, commit=commit, scorer_sha256=sha256_bytes(blob))
    return SC


def v045_brand_key(units):
    return {k: (A.CODER_SUB[u["substrate"]], u["coder_key"]) for k, u in units.items()}


def write_component_csv(path, gmap, units):
    bk = v045_brand_key(units)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["substrate", "brand", "value"])
        for k in sorted(units):
            v = gmap.get(k)
            w.writerow([bk[k][0], bk[k][1], "" if v is None else repr(float(v))])


def hb2_retest(g4, g5, units, n_perm=N_PERM, n_boot=HB2_N_BOOT, exclude=(), out_dir=None, gate="MARGINAL"):
    """HB2 = v0.45 section 2.6's Grounding component leg, called as v0.45 calls it (C4): rho_pw(G*_t4, G*_t5) on
    centred within-substrate ranks, t5 shuffled within substrate (one-sided), seed 450046, bootstrap 95%."""
    SC = load_v045()
    d = Path(out_dir) if out_dir else Path(tempfile.mkdtemp(prefix="v122_hb2_"))
    d.mkdir(parents=True, exist_ok=True)
    f4, f5 = d / "g_star_t4_v1_22.csv", d / "g_star_t5_v1_22.csv"
    write_component_csv(f4, g4, units)
    write_component_csv(f5, g5, units)
    bk = v045_brand_key(units)
    brands = [b for b in SC.brands_list() if b not in {bk[k] for k in exclude}]
    leg = SC.component_leg("Grounding", str(f4), str(f5), gate, SC.S.Cfg(n_perm, n_boot), brands)
    rho, p = leg.get("rho"), leg.get("p_perm")
    rho = None if rho is None or not _f(rho) else float(rho)
    p = None if p is None or not _f(p) else float(p)
    out = {"n": leg.get("n", 0), "rho_pw": rho, "p_perm_one_sided": p, "ci95": leg.get("ci95_rho"),
           "seed": SC.SEEDS["components"], "n_perm": n_perm, "n_boot": n_boot,
           "v045_verdict": leg.get("verdict"), "verdict": from_v045(leg.get("verdict")),
           "inputs_sha256": leg.get("inputs_sha256"), "v045_tag": V045_TAG, "v045_commit": _V045["commit"],
           "v045_scorer_sha256": _V045["scorer_sha256"], "files": [str(f4), str(f5)]}
    out["v122_band_check"] = retest_verdict(rho, p, out["n"])
    return out


def retest_leg(gA, gB, units, seed, n_perm=N_PERM, n_boot=HB2_N_BOOT, exclude=()):
    """HB45: the same statistic as v0.45's component_leg (v0.42's rho_pw, perm_p_within, bootstrap, loaded with
    v0.45), with this study's seed; same keys, same order."""
    SC = load_v045()
    S = SC.S
    bk = v045_brand_key(units)
    inv = {v: k for k, v in bk.items()}
    keys = [inv[b] for b in SC.brands_list() if b in inv and inv[b] not in exclude
            and _f(gA.get(inv[b])) and _f(gB.get(inv[b]))]
    n = len(keys)
    x = np.array([float(gA[k]) for k in keys])
    y = np.array([float(gB[k]) for k in keys])
    g = np.array([bk[k][0] for k in keys])
    rho = S.rho_pw(x, y, g) if n >= 3 else NAN
    p = S.perm_p_within(x, y, g, rho, seed, n_perm) if n >= 3 else NAN
    ci = None
    if n >= 3 and n_boot:
        ci = S.bootstrap(g, seed, n_boot, lambda i: {"rho": S.rho_pw(x[i], y[i], g[i])})["rho"]["ci95"]
    rho = float(rho) if _f(rho) else None
    p = float(p) if _f(p) else None
    return {"n": n, "rho_pw": rho, "p_perm_one_sided": p, "ci95": ci, "seed": seed, "n_perm": n_perm,
            "verdict": retest_verdict(rho, p, n)}


# =========================================================================== G* and the gate re-tests
def gstar(answers, units, floor=A.FLOOR_G, denominator="g"):
    stats = A.brand_stats(answers, units, floor, denominator)
    return A.gstar_map(stats), stats


def sep_test(gs, comp, seed, n_perm=N_PERM, n_boot=N_BOOT, centred=True, exclude=(), mq5_failed=False):
    """HB1 / HB4: S1 and S0 legs, v1.13's sep_leg and sep_verdict (imported)."""
    legs = [dict(A.sep_leg(gs, comp[c], seed, n_perm, n_boot, centred, exclude=exclude), condition=c)
            for c in ("S1", "S0")]
    return {"legs": legs, "verdict": A.sep_verdict(legs, mq5_failed)}


def hb3_reliability(answers5, units, n_perm=N_PERM, centred=True, exclude=(), floor=A.FLOOR_G_RUN):
    runs = A.per_run_maps(answers5, units, (1, 2, 3), floor)
    t = A.reliability_test(runs, SEEDS["HB3"], n_perm, centred, exclude)
    return dict(t, verdict=A.reliability_verdict(t))


def six_run_pairs(answers4, answers5, units, exclude=()):
    """Reported beside HB3 (no verdict): the 15 run pairs of t4 + t5, rho_w and units, floor g >= 3."""
    maps = {}
    for w, ans in (("t4", answers4), ("t5", answers5)):
        for r in (1, 2, 3):
            maps[(w, r)] = A.gstar_map(A.brand_stats([a for a in ans if a["run"] == r], units, A.FLOOR_G_RUN))
    out = []
    for a, b in itertools.combinations(sorted(maps), 2):
        keys, x, y, g, info = A.paired(maps[a], maps[b], exclude=exclude)
        out.append({"pair": [f"{a[0]}r{a[1]}", f"{b[0]}r{b[1]}"], "within_wave": a[0] == b[0], "n": info["n"],
                    "rho_w": A.rho_w(x, y, g) if info["n"] >= 3 else None})
    return out


# =========================================================================== #44 structured data
def hb44(sdri, gmap, seed, n_perm=N_PERM, n_boot=N_BOOT, centred=True, exclude=()):
    leg = A.sep_leg(sdri, gmap, seed, n_perm, n_boot, centred, sided="one", exclude=exclude)
    return dict(leg, verdict=one_sided_assoc_verdict(leg["rho_w"], leg["p"], leg["n"]))


# =========================================================================== #46 phantom signature
def _rated_keys(gmap, exclude=()):
    keys = sorted(k for k, v in gmap.items() if _f(v) and k not in exclude)
    per = collections.Counter(k[0] for k in keys)
    return [k for k in keys if per[k[0]] >= MIN_PER_CAT]


def cliffs_delta_within(values, flags, groups):
    """Pooled within-category Cliff's delta (flagged minus unflagged), pair-count weighted (v1.19 B4)."""
    values, flags = np.asarray(values, float), np.asarray(flags, bool)
    num = den = 0.0
    for gi in A._group_index(list(groups)):
        v, f = values[gi], flags[gi]
        a, b = v[f], v[~f]
        if len(a) and len(b):
            num += float(np.sign(a[:, None] - b[None, :]).sum())
            den += len(a) * len(b)
    return num / den if den else NAN


def stratified_perm_delta(values, flags, groups, obs, seed, n_perm):
    """Two-sided: F labels shuffled within category (counts fixed)."""
    flags = np.asarray(flags, bool)
    gidx = [np.array(i) for i in A._group_index(list(groups))]
    rng = np.random.default_rng(seed)
    f = flags.copy()
    hits = 0
    for _ in range(n_perm):
        for gi in gidx:
            f[gi] = flags[rng.permutation(gi)]
        hits += abs(cliffs_delta_within(values, f, groups)) >= abs(obs) - TOL
    return (1 + hits) / (n_perm + 1)


def rank_residuals(y, p, g):
    """Within-category residual of centred ranks of y on centred ranks of p (v1.19 B5, on v1.13's ranks)."""
    ry = np.array(A.within_ranks(list(y), list(g)))
    rp = np.array(A.within_ranks(list(p), list(g)))
    out = np.empty(len(y))
    for gi in A._group_index(list(g)):
        X = np.column_stack([np.ones(len(gi)), rp[gi]])
        coef, *_ = np.linalg.lstsq(X, ry[gi], rcond=None)
        out[gi] = ry[gi] - X @ coef
    return out


def hb46(gmap, flags, seed, n_perm=N_PERM, P=None, exclude=()):
    """HB46 (P=None) / HB46b (P = {unit: P_S1 mean of waves}): Cliff's delta F vs non-F."""
    keys = [k for k in _rated_keys(gmap, exclude) if k in flags and (P is None or _f(P.get(k)))]
    per = collections.Counter(k[0] for k in keys)
    keys = [k for k in keys if per[k[0]] >= MIN_PER_CAT]
    fl = np.array([flags[k]["F"] for k in keys], bool)
    g = [k[0] for k in keys]
    both = sorted({k[0] for k, x in zip(keys, fl) if x} & {k[0] for k, x in zip(keys, fl) if not x})
    info = {"n": len(keys), "n_F": int(fl.sum()), "n_nonF": int((~fl).sum()), "categories_with_both": both}
    enough = info["n_F"] >= PH_MIN and info["n_nonF"] >= PH_MIN and len(both) >= PH_MIN_CATS
    if not keys:
        return dict(info, delta=None, p=None, verdict=U, reason="no rated units")
    vals = np.array([float(gmap[k]) for k in keys])
    if P is not None:
        vals = rank_residuals(vals, [float(P[k]) for k in keys], g)
    d = cliffs_delta_within(vals, fl, g)
    p = stratified_perm_delta(vals, fl, g, d, seed, n_perm) if enough and _f(d) and n_perm else None
    v = signed_band_verdict(d if _f(d) else None, p, enough, +1, DELTA_CONF, DELTA_FALS)
    return dict(info, delta=d if _f(d) else None, p=p, seed=seed, n_perm=n_perm, verdict=v,
                arm="rank residuals given P_S1" if P is not None else "G*")


# =========================================================================== #47 identity load
def channel_counts(answers, units, subs=TRIO, min_g=CH_MIN_G, exclude=()):
    """{unit: (g_cat, o_cat, g_cult, o_cult)} on grounded answers naming the unit (units with a D_b in subs)."""
    acc = collections.defaultdict(lambda: [0, 0, 0, 0])
    for a in answers:
        ch = a.get("channel")
        if ch not in ("cat", "cult") or a["substrate"] not in subs:
            continue
        doms = A.resolved_domains(a["sources"])
        if not doms:
            continue
        j = 0 if ch == "cat" else 2
        for k in a["named"]:
            u = units[k]
            if u["status"] != "RESOLVED" or k in exclude:
                continue
            acc[k][j] += 1
            acc[k][j + 1] += bool(doms & u["domains"])
    return {k: tuple(v) for k, v in acc.items()}


def signflip_p(d, seed, n_perm):
    """One-sided sign-flip permutation p for mean(d) > 0."""
    d = np.asarray(d, float)
    obs = d.mean()
    rng = np.random.default_rng(seed)
    hits = 0
    for _ in range(n_perm):
        s = rng.integers(0, 2, len(d)) * 2 - 1
        hits += (s * d).mean() >= obs - TOL
    return (1 + hits) / (n_perm + 1)


def signflip_p_exact(d):
    d = np.asarray(d, float)
    obs = d.mean()
    hits = sum((np.array(s) * d).mean() >= obs - TOL for s in itertools.product((-1, 1), repeat=len(d)))
    return hits / 2 ** len(d)


def hb47(answers_pool, units, seed=SEEDS["HB47"], n_perm=N_PERM, subs=TRIO, exclude=()):
    cnt = channel_counts(answers_pool, units, subs, exclude=exclude)
    d = {k: 100.0 * (oc / gc - ou / gu) for k, (gc, oc, gu, ou) in cnt.items() if gc >= CH_MIN_G and gu >= CH_MIN_G}
    per = collections.Counter(k[0] for k in d)
    min_cat = min(per.get(s, 0) for s in subs)
    out = {"n": len(d), "per_category": dict(sorted(per.items())), "min_category_units": min_cat,
           "categories": list(subs), "seed": seed, "n_perm": n_perm}
    if not d:
        return dict(out, dbar=None, p=None, verdict=U)
    vals = [d[k] for k in sorted(d)]
    dbar = float(np.mean(vals))
    p = signflip_p(vals, seed, n_perm) if n_perm else None
    return dict(out, dbar=dbar, sd=float(np.std(vals, ddof=1)) if len(vals) > 1 else None, p=p,
                verdict=channel_verdict(dbar, p if p is not None else 1.0, len(d), min_cat))


def il_from_coded(coded_b_rows, channels, units, models=N3, excluded=()):
    """IL_b = k_cult/n_cult - k_cat/n_cat on t4 N3 S0 Phase B answers of the trio (v1.19 D6), with pi_hat over the
    six questions; rows are v0.42 coded Phase B rows; calls v0.42 excludes are dropped."""
    byc = A._by_coder(units)
    calls = collections.defaultdict(set)
    named = collections.defaultdict(set)
    excluded = set(excluded)
    inv_sub = {v: k for k, v in A.CODER_SUB.items()}
    for r in coded_b_rows:
        sub = inv_sub.get(r["substrate"], r["substrate"])
        if r["model"] not in models or (r.get("condition") or "S0") != "S0" or sub not in TRIO:
            continue
        if r["call_id"] in excluded:
            continue
        ch = channels.get((sub, r["probe_id"]))
        if ch not in ("cat", "cult"):
            continue
        calls[(sub, ch)].add(r["call_id"])
        if str(r["mentioned"]) in ("1", "True", "true"):
            k = byc.get((r["substrate"], r["brand"]))
            if k is not None:
                named[(k, ch)].add(r["call_id"])
    out = {}
    for k in units:
        s = k[0]
        if s not in TRIO:
            continue
        nc, nu = len(calls[(s, "cat")]), len(calls[(s, "cult")])
        kc, ku = len(named[(k, "cat")]), len(named[(k, "cult")])
        if nc and nu:
            out[k] = {"il": ku / nu - kc / nc, "pi_hat": (kc + ku) / (nc + nu)}
    return out


def hb47b(il, gmap, seed=SEEDS["HB47b"], n_perm=N_PERM, n_boot=N_BOOT, centred=True, exclude=()):
    elig = {k: v["il"] for k, v in il.items() if 0 < v["pi_hat"] < 1}
    leg = A.sep_leg(elig, gmap, seed, n_perm, n_boot, centred, sided="two", exclude=exclude)
    enough = leg["n"] >= IL_N and leg["n_substrates"] == len(TRIO)
    v = signed_band_verdict(leg["rho_w"], leg["p"], enough, -1, IL_CONF, IL_FALS)
    return dict(leg, eligible_il_units=len(elig), verdict=v)


# =========================================================================== #48 source-class profiles and typology
def profiles(answers, units, keys=None):
    """{unit: {'x': six class shares (v1.13 source_mix), 'other': share, 'unresolved': share, 'grounded': n}}."""
    by = collections.defaultdict(list)
    unres = collections.defaultdict(list)
    for a in answers:
        if not A.resolved_domains(a["sources"]):
            continue
        for k in a["named"]:
            if keys is None or k in keys:
                by[k].append(a["sources"])
                unres[k].append(sum(s["cls"] == "unresolved" for s in a["sources"]) / len(a["sources"]))
    out = {}
    for k, lst in by.items():
        mix = A.source_mix(lst)
        out[k] = {"x": [mix[c] or 0.0 for c in PROFILE_CLASSES], "other": mix["other"],
                  "unresolved": float(np.mean(unres[k])), "grounded": len(lst)}
    return out


def _centre_by_cat(X, g):
    X = np.array(X, float)
    for gi in A._group_index(list(g)):
        X[gi] -= X[gi].mean(axis=0)
    return X


def _corr(a, b):
    a, b = a - a.mean(), b - b.mean()
    d = math.sqrt(float((a * a).sum() * (b * b).sum()))
    return float((a * b).sum() / d) if d > 0 else NAN


def hb48(prof4, prof5, g4, g5, seed=SEEDS["HB48"], n_perm=N_PERM, exclude=()):
    """R = mean over the six classes of rho_w(x_t4,c, x_t5,c) over units rated at both waves; one-sided p with the
    t5 profiles permuted across units within category (one permutation for all classes)."""
    keys = sorted(k for k in g4 if _f(g4.get(k)) and _f(g5.get(k)) and k in prof4 and k in prof5
                  and k not in exclude)
    per = collections.Counter(k[0] for k in keys)
    keys = [k for k in keys if per[k[0]] >= MIN_PER_CAT]
    info = {"n": len(keys), "n_categories": len({k[0] for k in keys})}
    if len(keys) < 3:
        return dict(info, R=None, p=None, verdict=U)
    g = [k[0] for k in keys]
    X4 = _centre_by_cat([prof4[k]["x"] for k in keys], g)
    X5 = _centre_by_cat([prof5[k]["x"] for k in keys], g)
    R4 = np.column_stack([A.within_ranks(list(X4[:, j]), g) for j in range(6)])
    R5 = np.column_stack([A.within_ranks(list(X5[:, j]), g) for j in range(6)])
    per_c = [_corr(R4[:, j], R5[:, j]) for j in range(6)]
    ok = [j for j in range(6) if _f(per_c[j])]

    def stat(idx):
        return float(np.mean([_corr(R4[:, j], R5[idx, j]) for j in ok])) if ok else NAN
    obs = stat(np.arange(len(keys)))
    p = None
    if _f(obs) and n_perm:
        rng = np.random.default_rng(seed)
        gidx = [np.array(i) for i in A._group_index(g)]
        idx = np.arange(len(keys))
        hits = 0
        for _ in range(n_perm):
            for gi in gidx:
                idx[gi] = gi[rng.permutation(len(gi))]
            s = stat(idx)
            hits += _f(s) and s >= obs - TOL
        p = (1 + hits) / (n_perm + 1)
    v = replication_verdict(obs if _f(obs) else None, p if p is not None else 1.0, len(keys))
    return dict(info, R=obs if _f(obs) else None, per_class=dict(zip(PROFILE_CLASSES, per_c)),
                classes_defined=[PROFILE_CLASSES[j] for j in ok], p=p, seed=seed, n_perm=n_perm, verdict=v)


def silhouette(X, lab):
    lab = np.asarray(lab)
    ks = np.unique(lab)
    if len(ks) < 2:
        return NAN
    D = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(-1))
    onehot = (lab[:, None] == ks[None, :]).astype(float)
    sums = D @ onehot
    counts = onehot.sum(0)
    own = np.searchsorted(ks, lab)
    n_own = counts[own]
    a = np.where(n_own > 1, sums[np.arange(len(X)), own] / np.maximum(n_own - 1, 1), 0.0)
    mean_other = sums / counts[None, :]
    mean_other[np.arange(len(X)), own] = np.inf
    b = mean_other.min(1)
    mx = np.maximum(a, b)
    s = np.where((n_own > 1) & (mx > 0), (b - a) / np.where(mx > 0, mx, 1.0), 0.0)
    return float(s.mean())


def ari(a, b):
    a, b = np.asarray(a), np.asarray(b)
    _, ia = np.unique(a, return_inverse=True)
    _, ib = np.unique(b, return_inverse=True)
    Mx = np.zeros((ia.max() + 1, ib.max() + 1))
    np.add.at(Mx, (ia, ib), 1)
    c2 = lambda v: v * (v - 1) / 2.0  # noqa: E731
    s_ij, s_a, s_b, n2 = c2(Mx).sum(), c2(Mx.sum(1)).sum(), c2(Mx.sum(0)).sum(), c2(len(a))
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
    """Gap statistic over k = 1..8 (uniform box references, 1-SE rule), as v1.19."""
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
        gidx = [np.array(i) for i in A._group_index(list(g))]
        for _ in range(n_perm):
            Xp = X.copy()
            for j in range(X.shape[1]):
                for gi in gidx:
                    Xp[gi, j] = X[gi[rng.permutation(len(gi))], j]
            null.append(silhouette(Xp, ward_labels(Xp, k)))
    pct = float(np.percentile(null, SIL_PCT)) if null else NAN
    auto = bool(k >= 2 and sil >= SIL_MIN and sil > pct)
    return {"k": int(k), "gap": gap, "silhouette": None if not _f(sil) else sil,
            "silhouette_null_p95": None if not _f(pct) else pct, "n_null": len(null),
            "internal_structure": auto}, lab


def presence_tiers(P, keys):
    """v0.23 regime rule within category (quartiles)."""
    out = {}
    for s in dict.fromkeys(k[0] for k in keys):
        ks = [k for k in keys if k[0] == s and _f(P.get(k))]
        vals = sorted(float(P[k]) for k in ks)
        q25, q50, q75 = (float(np.percentile(vals, q)) for q in (25, 50, 75)) if len(vals) >= 4 else (0, 0, 0)
        for k in ks:
            v = float(P[k])
            out[k] = "Dominant" if v >= q75 else "Established" if v >= q50 else "Emerging" if v >= q25 else "Absent"
    return out


def typology_cell(rep, inherit, auto, resid):
    """v1.19 section 7.3's exhaustive matrix."""
    if rep not in (C, M):
        return "NO TYPOLOGY (profiles do not replicate); structure reported descriptively"
    tag = "" if rep == C else " [provisional: replication MARGINAL]"
    if inherit:
        return ("LAYERED" if resid else "BORROWED") + tag
    if auto:
        return ("AUTONOMOUS" if resid else "PRESENCE-DEPENDENT") + tag
    return ("RESIDUAL-ONLY" if resid else "UNSTRUCTURED") + tag


def _zscore(X):
    X = np.array(X, float)
    sd = X.std(0)
    return (X - X.mean(0)) / np.where(sd > 0, sd, 1.0)


def hb48b(prof_pool, gpool, P_S1, C_S0, rep_verdict, n_perm=N_PERM, B=GAP_B, exclude=()):
    """Typology on G*_pool-rated units: the pooled six-class profile (centred on the category mean) plus centred
    within-category ranks of G*_pool, P_S1 and C*_S0 (means of the waves); each feature z-scored (r1); Ward."""
    if rep_verdict not in (C, M):
        return {"cell": "NO TYPOLOGY", "reason": f"HB48 is {rep_verdict}"}
    keys = sorted(k for k in gpool if _f(gpool.get(k)) and k in prof_pool and _f(P_S1.get(k)) and _f(C_S0.get(k))
                  and k not in exclude)
    per = collections.Counter(k[0] for k in keys)
    keys = [k for k in keys if per[k[0]] >= MIN_PER_CAT]
    res = {"n": len(keys)}
    if len(keys) < FLOOR_UNITS:
        return dict(res, cell=U, reason="below the n floor of 30")
    g = [k[0] for k in keys]
    prof = _centre_by_cat([prof_pool[k]["x"] for k in keys], g)
    ranks = np.column_stack([A.within_ranks([float(d[k]) for k in keys], g) for d in (gpool, P_S1, C_S0)])
    X = _zscore(np.column_stack([prof, ranks]))
    st, lab = structure(X, g, np.random.default_rng(SEEDS["HB48b_full"]), n_perm, B)
    tiers = presence_tiers(P_S1, keys)
    tl = np.array([tiers[k] for k in keys])
    a_obs = ari(lab, tl) if st["k"] >= 2 else 0.0
    rng = np.random.default_rng(SEEDS["HB48b_full"] + 1)
    nulls = []
    for _ in range(n_perm if st["k"] >= 2 else 0):
        t2 = tl.copy()
        for gi in A._group_index(g):
            gi = np.array(gi)
            t2[gi] = tl[gi[rng.permutation(len(gi))]]
        nulls.append(ari(lab, t2))
    p_ari = (1 + sum(x >= a_obs - TOL for x in nulls)) / (len(nulls) + 1) if nulls else 1.0
    inherit = bool(st["k"] >= 2 and a_obs >= ARI_MIN and p_ari < ARI_P)
    Pv = np.array([float(P_S1[k]) for k in keys])
    Xr = X.copy()
    for gi in A._group_index(g):
        Z = np.column_stack([np.ones(len(gi)), Pv[gi]])
        for j in range(X.shape[1]):
            cf, *_ = np.linalg.lstsq(Z, Xr[gi, j], rcond=None)
            Xr[gi, j] = Xr[gi, j] - Z @ cf
    st_r, _ = structure(Xr, g, np.random.default_rng(SEEDS["HB48b_resid"]), n_perm, B)
    auto = bool(st["internal_structure"] and a_obs < ARI_MIN)
    cell = typology_cell(rep_verdict, inherit, auto, st_r["internal_structure"])
    types = {}
    for t in sorted(set(lab.tolist())):
        rows = [i for i in range(len(keys)) if lab[i] == t]
        types[f"type {int(t)}"] = {"n": len(rows), "mean_profile": dict(zip(PROFILE_CLASSES,
                                                                         prof[rows].mean(0).tolist()))}
    return dict(res, full=st, ari_vs_presence_tiers=a_obs, p_ari=p_ari, inheritance=inherit, autonomy=auto,
                residual=st_r, residual_structure=st_r["internal_structure"], cell=cell, types=types,
                features="6 centred class shares + centred ranks of G*_pool, P_S1, C*_S0; z-scored")


# =========================================================================== descriptives (no verdicts)
def _median(v):
    v = [x for x in v if _f(x)]
    return float(np.median(v)) if v else None


def d44(sdri, gpool, prof_pool):
    rich, sparse = [], []
    for s in CATS:
        ks = sorted((k for k in sdri if k[0] == s and _f(sdri.get(k))), key=lambda k: sdri[k])
        t = len(ks) // 3
        if t:
            sparse += ks[:t]
            rich += ks[-t:]

    def summ(ks):
        rated = [k for k in ks if _f(gpool.get(k))]
        prof = [prof_pool[k]["x"] for k in rated if k in prof_pool]
        return {"units": len(ks), "rated": len(rated), "median_g_star_pool": _median([gpool[k] for k in rated]),
                "mean_profile": dict(zip(PROFILE_CLASSES, np.mean(prof, 0).tolist())) if prof else None}
    return {"rich_top_tercile": summ(rich), "sparse_bottom_tercile": summ(sparse)}


def _top_domains(answers, n=20, cls=None):
    cnt = collections.Counter()
    for a in answers:
        for s in a["sources"]:
            if s["cls"] != "unresolved" and (cls is None or s["cls"] == cls):
                cnt[s["domain"]] += 1
    return {d for d, _ in sorted(cnt.items(), key=lambda t: (-t[1], t[0]))[:n]}


def _jacc(a, b):
    return len(a & b) / len(a | b) if a | b else None


def d45(ansA, ansB, units, labels=("t4", "t5")):
    out = {"jaccard_top20_domains_by_model": {}, "jaccard_top10_by_class": {}, "class_mix_by_category": {}}
    for m in sorted({a["model"] for a in ansA} & {a["model"] for a in ansB}):
        aa, bb = [a for a in ansA if a["model"] == m], [a for a in ansB if a["model"] == m]
        out["jaccard_top20_domains_by_model"][m] = _jacc(_top_domains(aa), _top_domains(bb))
        out["jaccard_top10_by_class"][m] = {c: _jacc(_top_domains(aa, 10, c), _top_domains(bb, 10, c))
                                            for c in PROFILE_CLASSES}
    for s in CATS:
        mixes = {lab: A.source_mix([a["sources"] for a in ans if a["substrate"] == s])
                 for lab, ans in zip(labels, (ansA, ansB))}
        out["class_mix_by_category"][s] = mixes
    _, stA = gstar(ansA, units, floor=1)
    _, stB = gstar(ansB, units, floor=1)
    both = [k for k in units if units[k]["status"] == "RESOLVED" and stA[k]["g"] and stB[k]["g"]]
    flip = [k for k in both if bool(stA[k]["o"]) != bool(stB[k]["o"])]
    out["own_domain_retrieved_at_one_wave_only"] = {"units_grounded_at_both": len(both), "units": len(flip),
                                                    "share": len(flip) / len(both) if both else None}
    return out


CAVEAT_WINDOW = 150
CAVEAT_TERMS = ("discontinued", "defunct", "no longer", "ceased", "phased out", "out of production", "shut down",
                "was retired", "folded", "used market", "used car", "pre-owned", "bankrupt")


def is_caveated(text, brand):
    t, b = (text or "").lower(), brand.lower()
    i = t.find(b)
    while i >= 0:
        win = t[max(0, i - CAVEAT_WINDOW): i + len(b) + CAVEAT_WINDOW]
        if any(w in win for w in CAVEAT_TERMS):
            return True
        i = t.find(b, i + 1)
    return False


def d46(answers, units, flags, texts=None, named_s0=None):
    fk = {k for k, v in flags.items() if v["F"]}
    dk = {k for k, v in flags.items() if v["D"]}
    out = {"class_mix_answers_naming_F": A.source_mix([a["sources"] for a in answers if a["named"] & fk]),
           "class_mix_answers_naming_nonF": A.source_mix([a["sources"] for a in answers
                                                         if a["named"] - fk - dk])}
    if named_s0 is not None:
        s1 = set().union(*[a["named"] for a in answers]) if answers else set()
        out["F_units_search_surfaced"] = sorted(f"{k[0]}|{k[1]}" for k in fk if k in s1 and k not in named_s0)
    dd = {}
    for k in sorted(dk):
        aa = [a for a in answers if k in a["named"]]
        rec = {"s1_answers": len(aa), "class_mix": A.source_mix([a["sources"] for a in aa])}
        if texts is not None:
            cav = sum(is_caveated(texts.get(a["call_id"]), units[k]["brand"]) for a in aa)
            rec.update(caveated=cav, naive=len(aa) - cav)
        dd[f"{k[0]}|{units[k]['brand']}"] = rec
    out["defunct_D"] = dd
    return out


def d48(gpool, P_S1, rstar=None):
    q = collections.Counter()
    for s in CATS:
        ks = [k for k in gpool if k[0] == s and _f(gpool.get(k)) and _f(P_S1.get(k))]
        if not ks:
            continue
        mg, mp = np.median([gpool[k] for k in ks]), np.median([P_S1[k] for k in ks])
        for k in ks:
            q[("own-site-led" if gpool[k] > mg else "third-party-led",
               "named" if P_S1[k] > mp else "seldom named")] += 1
    out = {f"{a} and {b}": v for (a, b), v in sorted(q.items())}
    if rstar is not None:
        out["R_star_S1_t4_column"] = {f"{k[0]}|{k[1]}": rstar.get(k) for k in sorted(gpool) if _f(gpool.get(k))}
    return out


def mq_wave(w, units):
    ans = w["answers"]
    gs, _ = gstar(ans, units)
    out = {"MQ2": A.mq2_search_use(ans, w.get("models", N3)), "MQ3": A.mq3_class_coverage(ans),
           "MQ5": A.mq5_degenerate(gs), "MQ10_answered_by_model": w.get("answered_by_model"),
           "dropped_models": w.get("dropped", []), "panel": w.get("models", list(N3)),
           "reduced_panel": len(w.get("models", N3)) < len(N3),
           "C5_arm_used": any(a.get("source") == "C5" for a in ans)}
    if w.get("served") is not None:
        out["MQ9_served_ids"] = w["served"]
    return out


# =========================================================================== orchestration
NM = "NOT MEASURED"


def _mean_waves(*maps):
    out = {}
    for k in set().union(*maps):
        v = [float(m[k]) for m in maps if _f(m.get(k))]
        out[k] = float(np.mean(v)) if v else None
    return out


def _gb_in(v):
    return U if v == NM else v


def core(inp, n_perm=N_PERM, n_boot=N_BOOT, opts=None, typology=False, gap_b=GAP_B, hb2_full=True, out_dir=None):
    """HB1-HB4, GB, HB44(b), HB46(b), HB47(b), HB48 (and HB48b if typology) on one set of options.
    inp: units, flags, il, sdri, waves {t4, t5: {answers, P, C, models, ...}}. opts: exclude, floor, denominator,
    centred, drop_models, cited, no_c5, structure_on ('pool' | 't5'), sdri (override map), il (override),
    channel_subs."""
    o = opts or {}
    units, flags = inp["units"], inp["flags"]
    ex = tuple(o.get("exclude", ()))
    floor, den, centred = o.get("floor", A.FLOOR_G), o.get("denominator", "g"), o.get("centred", True)

    def view(w):
        ans = w.get("answers_cited") if o.get("cited") else w["answers"]
        if ans is None:
            return None, []
        models = [m for m in w.get("models", N3) if m not in o.get("drop_models", ())]
        return [a for a in ans if a["model"] in models and not (o.get("no_c5") and a.get("source") == "C5")], models

    a4, m4 = view(inp["waves"]["t4"])
    a5, m5 = view(inp["waves"]["t5"])
    if a4 is None or a5 is None:
        return {"skipped": "input not available for this option"}
    W4, W5 = inp["waves"]["t4"], inp["waves"]["t5"]
    g4, _ = gstar(a4, units, floor, den)
    g5, st5 = gstar(a5, units, floor, den)
    ap = a4 + a5
    gp, stp = gstar(ap, units, floor, den)
    mq5 = A.mq5_degenerate({k: v for k, v in g5.items() if k not in ex})
    t5_ok, t4_ok = len(m5) >= 2, len(m4) >= 2
    common = [m for m in m4 if m in m5]
    res = {"panel_t4": m4, "panel_t5": m5, "common_panel": common,
           "reduced_panel": len(m5) < len(N3) or len(m4) < len(N3), "MQ5_t5": mq5,
           "rated": {"t4": sum(_f(v) for v in g4.values()), "t5": sum(_f(v) for v in g5.values()),
                     "pool": sum(_f(v) for v in gp.values())}}
    V = {}
    if t5_ok:
        res["HB1"] = sep_test(g5, W5["P"], SEEDS["HB1"], n_perm, n_boot, centred, ex, mq5["failed"])
        res["HB4"] = sep_test(g5, W5["C"], SEEDS["HB4"], n_perm, n_boot, centred, ex, mq5["failed"])
        res["HB3"] = hb3_reliability(a5, units, n_perm, centred, ex)
        V.update(HB1=res["HB1"]["verdict"], HB4=res["HB4"]["verdict"], HB3=res["HB3"]["verdict"])
    else:
        V.update(HB1=NM, HB4=NM, HB3=NM)
    if len(common) >= 2 and t5_ok and t4_ok:
        gc4 = g4 if common == m4 else gstar([a for a in a4 if a["model"] in common], units, floor, den)[0]
        gc5 = g5 if common == m5 else gstar([a for a in a5 if a["model"] in common], units, floor, den)[0]
        if hb2_full:
            res["HB2"] = hb2_retest(gc4, gc5, units, n_perm, HB2_N_BOOT, ex, out_dir)
        else:
            res["HB2"] = retest_leg(gc4, gc5, units, SEEDS["HB2"], n_perm, 0, ex)
        V["HB2"] = res["HB2"]["verdict"]
    else:
        V["HB2"] = NM
    V["GB"] = gate_completion(*(_gb_in(V[h]) for h in ("HB1", "HB2", "HB3", "HB4")))
    res["R"] = reliability_condition(_gb_in(V["HB2"]), _gb_in(V["HB3"]))
    on_t5 = o.get("structure_on", "pool") == "t5"
    gS, aS = (g5, a5) if on_t5 else (gp, ap)
    sdri = o.get("sdri", inp.get("sdri") or {})
    res["HB44"] = hb44(sdri, gS, SEEDS["HB44"], n_perm, n_boot, centred, ex)
    res["HB44b"] = hb44(sdri, g5, SEEDS["HB44b"], n_perm, n_boot, centred, ex)
    P1 = _mean_waves(W4["P"]["S1"], W5["P"]["S1"])
    C0 = _mean_waves(W4["C"]["S0"], W5["C"]["S0"])
    res["HB46"] = hb46(gS, flags, SEEDS["HB46"], n_perm, None, ex)
    res["HB46b"] = hb46(gS, flags, SEEDS["HB46b"], n_perm, P1, ex)
    if res["HB46"]["verdict"] != res["HB46b"]["verdict"]:
        res["HB46"]["label"] = "Presence-sensitive"
    res["HB47"] = hb47(aS, units, SEEDS["HB47"], n_perm, o.get("channel_subs", TRIO), ex)
    res["HB47b"] = hb47b(o.get("il", inp.get("il") or {}), gS, SEEDS["HB47b"], n_perm, n_boot, centred, ex)
    prof4, prof5 = profiles(a4, units), profiles(a5, units)
    if t5_ok and t4_ok:
        res["HB48"] = hb48(prof4, prof5, g4, g5, SEEDS["HB48"], n_perm, ex)
    else:
        res["HB48"] = {"verdict": NM}
    for h in ("HB44", "HB44b", "HB46", "HB46b", "HB47", "HB47b", "HB48"):
        V[h] = res[h]["verdict"]
    if typology:
        prof_pool = profiles(ap, units)
        res["HB48b"] = hb48b(prof_pool, gp, P1, C0, V["HB48"], n_perm, gap_b, ex)
        V["HB48b"] = res["HB48b"]["cell"]
        res["_prof_pool"] = prof_pool
    res["verdicts"] = V
    res["_maps"] = {"g4": g4, "g5": g5, "gp": gp, "P1": P1, "a4": a4, "a5": a5, "ap": ap}
    return res


def leave_one_category_out(inp, n_perm, base_ex=()):
    out = {}
    for s in CATS:
        ex = tuple(base_ex) + tuple(k for k in inp["units"] if k[0] == s)
        r = core(inp, n_perm, 0, {"exclude": ex}, hb2_full=False)
        out[s] = r.get("verdicts")
    return out


def sensitivities(inp, n_perm=N_PERM):
    """Section 7: each re-computes the verdict-bearing tests (no bootstrap, HB2 by the identical retest_leg); none
    changes a verdict. Sensitivities whose input is not supplied are listed as not available."""
    units = inp["units"]
    coi = coi_keys(units)
    dkeys = tuple(k for k, v in inp["flags"].items() if v["D"])
    spec = {"S-COI": {"exclude": coi}, "S-House": {"exclude": tuple(A.HOUSE_PORTAL_UNITS)},
            "S-Floor3": {"floor": 3}, "S-Floor10": {"floor": 10}, "S-m": {"denominator": "m"},
            "S-Uncentred": {"centred": False}, "S-NoGemini": {"drop_models": (A.GEM4,)},
            "S-Wave": {"structure_on": "t5"}, "S-AllChannels": {"channel_subs": CATS},
            "S-F-noD": {"exclude": dkeys}}
    if all(inp["waves"][w].get("answers_cited") is not None for w in ("t4", "t5")):
        spec["S-Cited"] = {"cited": True}
    if any(a.get("source") == "C5" for a in inp["waves"]["t5"]["answers"]):
        spec["S-C5"] = {"no_c5": True}
    for name, key in (("S-SDRI-t5", "sdri_t5"), ("S-SDRI-kg", "sdri_kg"), ("S-SDRI-site", "sdri_site")):
        if inp.get(key):
            spec[name] = {"sdri": inp[key]}
    if inp.get("il_t1"):
        spec["S-IL-t1"] = {"il": inp["il_t1"]}
    out = {}
    for name, o in spec.items():
        r = core(inp, n_perm, 0, o, hb2_full=False)
        out[name] = {"options": {k: (v if not isinstance(v, (tuple, dict)) or k != "exclude" else len(v))
                                 for k, v in o.items() if k not in ("sdri", "il")},
                     "verdicts": r.get("verdicts"), "skipped": r.get("skipped")}
    out["S-LOCO"] = leave_one_category_out(inp, n_perm)
    missing = [n for n in ("S-Cited", "S-C5", "S-SDRI-t5", "S-SDRI-kg", "S-SDRI-site", "S-IL-t1") if n not in out]
    out["_not_available"] = missing
    return out


def verdict_changes(base, sens):
    out = {}
    for name, s in sens.items():
        if name.startswith("_"):
            continue
        rows = s.items() if name == "S-LOCO" else [(None, s.get("verdicts"))]
        for sub, v in rows:
            for h, x in (v or {}).items():
                if base.get(h) is not None and x != base[h]:
                    out.setdefault(name if sub is None else f"{name}:{sub}", {})[h] = [x, base[h]]
    return out


def stage1(inp, n_perm=N_PERM, n_boot=N_BOOT, gap_b=GAP_B, with_sensitivities=True, out_dir=None):
    """Section 6 Stage 1 on loaded inputs (real or synthetic). Section 1 first: no statistic unless RUN."""
    route = paper_b_route(inp.get("paper_a_verdict"), inp.get("decision"))
    if route != "RUN":
        if route == "REFUSED":
            raise Refused(f"REFUSED: Paper A verdict {inp.get('paper_a_verdict')!r} is not MARGINAL")
        return {"phase": PHASE_ID, "stage": 1, "status": route, "statistics": None,
                "paper_A_verdict": inp.get("paper_a_verdict")}
    units = inp["units"]
    r = core(inp, n_perm, n_boot, typology=True, gap_b=gap_b, out_dir=out_dir)
    mp = r.pop("_maps")
    prof_pool = r.pop("_prof_pool")
    mqs = {w: mq_wave(inp["waves"][w], units) for w in ("t4", "t5")}
    mqs["pool"] = {"MQ3": A.mq3_class_coverage(mp["ap"]), "MQ5": A.mq5_degenerate(mp["gp"])}
    low_cov = any((mqs[w]["MQ3"] or {}).get("low_coverage") for w in ("t4", "t5", "pool"))
    labels = {"all": CONDITIONAL_LABEL, "pool_tests": POOL_LABEL,
              "reduced_panel": "reduced panel" if r["reduced_panel"] else None,
              "class_based_low_coverage": "low coverage (MQ3)" if low_cov else None}
    doc = {"phase": PHASE_ID, "stage": 1, "status": "RUN", "prereg_tag": PREREG_TAG,
           "paper_A_verdict": inp.get("paper_a_verdict"), "decision": inp.get("decision"), "labels": labels,
           "verdicts": r["verdicts"], "results": {k: v for k, v in r.items() if k != "verdicts"},
           "six_run_pairs": six_run_pairs(mp["a4"], mp["a5"], units),
           "descriptives": {"D44": d44(inp.get("sdri") or {}, mp["gp"], prof_pool),
                            "D45_t4_t5": d45(mp["a4"], mp["a5"], units),
                            "D46": d46(mp["ap"], units, inp["flags"], inp.get("texts"), inp.get("named_s0")),
                            "D48": d48(mp["gp"], mp["P1"], inp.get("rstar"))},
           "MQ": mqs, "seeds": SEEDS, "draws": {"permutation": n_perm, "bootstrap": n_boot,
                                                "HB2_bootstrap": HB2_N_BOOT, "gap_references": gap_b}}
    if with_sensitivities:
        sens = sensitivities(inp, n_perm)
        doc["sensitivities"] = sens
        doc["verdict_changes"] = verdict_changes(r["verdicts"], sens)
    return doc


def stage2(g4, g5, g6, units, n_perm=N_PERM, n_boot=HB2_N_BOOT, answers=None, t6_models=N3):
    """Section 6 Stage 2: HB45_t5t6, HB45_t4t6 (v0.45's statistic, this study's seeds) and D45 for t6 pairs.
    Fewer than two t6 models with search-on answers -> NOT MEASURED; a t6 model outside N3 -> 'model changed'."""
    hs = ("HB45_t5t6", "HB45_t4t6")
    if len(t6_models) < 2:
        out = {h: {"verdict": NM, "reason": "fewer than two t6 models with search-on answers"} for h in hs}
    else:
        out = {"HB45_t5t6": retest_leg(g5, g6, units, SEEDS["HB45_t5t6"], n_perm, n_boot),
               "HB45_t4t6": retest_leg(g4, g6, units, SEEDS["HB45_t4t6"], n_perm, n_boot)}
    out["t6_panel"] = list(t6_models)
    out["label"] = "model changed" if any(m not in N3 for m in t6_models) else None
    out["verdicts"] = {h: out[h]["verdict"] for h in hs}
    if answers:
        out["D45_t5_t6"] = d45(answers["t5"], answers["t6"], units, ("t5", "t6"))
        out["D45_t4_t6"] = d45(answers["t4"], answers["t6"], units, ("t4", "t6"))
    return out


# =========================================================================== real inputs (guarded)
_GUARD = {"passed": None}
S1_CALLS_PER_MODEL, ANSWERED_MIN = 90, 0.90            # v0.42 section 5.4 drop rule


def tag_commit_on_origin(tag):
    out = git("ls-remote", "--tags", "origin", f"refs/tags/{tag}", f"refs/tags/{tag}^{{}}")
    if not out:
        return None
    lines = [ln.split("\t") for ln in out.decode().strip().splitlines() if ln.strip()]
    peeled = [c for c, ref in lines if ref.endswith("^{}")]
    return (peeled or [lines[0][0]])[0] if lines else None


def manifest_hashes(path=V113_MANIFEST):
    out = {}
    for ln in Path(path).read_text(encoding="utf-8").splitlines():
        if ln.strip() and not ln.startswith("#"):
            h, p = ln.split(None, 1)
            out[p.strip()] = h
    return out


def b_p0():
    """Imported v1.13 scorer and frozen lists hash to v1.13's lock manifest; roster hash (load_roster checks it)."""
    man = manifest_hashes()
    checks = {}
    for rel in ("osf/methodology/v1_13/scripts/score_v1_13.py", "osf/methodology/v1_13/prereg/source_classes_v1_13.md",
                "osf/methodology/v1_13/registries/brand_domains_v1_13.csv"):
        have = sha256_file(REPO / rel)
        checks[rel] = {"sha256": have, "manifest": man.get(rel), "match": have == man.get(rel)}
    checks["score_v1_13.py pinned"] = {"match": sha256_file(V113_SCORER) == V113_SCORER_SHA256}
    load_roster()
    checks["phantom_roster"] = {"sha256": PHANTOM_ROSTER_SHA256, "match": True}
    ok = all(v["match"] for v in checks.values())
    if not ok:
        raise Refused(f"B-P0 failed: {checks}")
    return checks


def guard_stage(stage, v045_scored_commit=None, t6_tags=()):
    """Refuse unless the lock exists (tag on origin + anchor naming its commit), Pablo's decision record is valid,
    the wave's tags exist and the stage's output folder is empty. Runs before any t5 / t6 file is opened."""
    commit = tag_commit_on_origin(PREREG_TAG)
    if not commit:
        raise Refused(f"REFUSED: tag {PREREG_TAG} is not on origin (not locked); no real-data stage runs.")
    if not ANCHOR.exists() or json.loads(ANCHOR.read_text(encoding="utf-8")).get("commit") != commit:
        raise Refused(f"REFUSED: {ANCHOR.name} missing or not naming the tag's commit {commit}.")
    verdict, _ = paper_a_verdict()
    route = paper_b_route(verdict, read_decision())
    if route != "RUN":
        raise Refused(f"NOT RUN: section 1 route is {route} (Paper A verdict {verdict}).")
    if not tag_commit_on_origin(V045_ACQ_TAG):
        raise Refused(f"REFUSED: {V045_ACQ_TAG} is not on origin (t5 not acquisition-locked).")
    if stage == 1:
        if not v045_scored_commit or git("cat-file", "-e", f"{v045_scored_commit}^{{commit}}") is None:
            raise Refused("REFUSED: v0.45's scored commit not given or not in this repository.")
    for t in t6_tags:
        if not tag_commit_on_origin(t):
            raise Refused(f"REFUSED: t6 tag {t} is not on origin.")
    out = OUT_DIR / f"stage{stage}"
    if out.exists() and any(out.iterdir()):
        raise Refused(f"REFUSED: {out} is not empty (each stage runs once).")
    b_p0()
    _GUARD["passed"] = stage
    return {"prereg_commit": commit, "route": route}


def read_coded(coded_dir):
    coded_a, coded_b = [], []
    for sub in A.SUBSTRATES:
        for ph, acc in (("a", coded_a), ("b", coded_b)):
            p = Path(coded_dir) / f"{sub}_phase_{ph}.csv"
            if p.exists():
                acc.extend(A.read_csv(p))
    return coded_a, coded_b


def _attach(answers, recs, channels, label):
    by = {r["call_id"]: r for r in recs}
    for a in answers:
        r = by[a["call_id"]]
        a["channel"] = channels.get((r["substrate"], r.get("probe_id")))
        a["wave"] = label
        a["source"] = r.get("_source", "wave")
    return answers


def load_wave_real(label, raw, coded_dir, brand_table, units, classes, channels, c5_raw=None, panel=None):
    """One wave's inputs with v1.13's imported functions. t5 / t6 are refused unless guard_stage passed.
    panel: N3 for t4 and t5; for t6 the models found in its answered S1 Phase B records (Stage 2)."""
    if label != "t4" and not _GUARD["passed"]:
        raise Refused(f"REFUSED: {label} data are not read before the lock (guard_stage).")
    records = A.read_jsonl(raw)
    if c5_raw:
        for r in A.read_jsonl(c5_raw):
            records.append(dict(r, _source="C5"))
    recs = A.dedupe_calls(records)
    coded_a, coded_b = read_coded(coded_dir)
    named = A.named_index(coded_b, units)
    if panel is None:
        panel = N3
    elif panel == "from_records":
        panel = tuple(sorted({r["model_requested"] for r in recs if r.get("condition") == "S1"
                              and r.get("phase") == "B" and A.is_answered(r)}))
    cat = A.select_calls(recs, panel, "S1", "B")
    for r in [r for r in recs if r.get("condition") == "S1" and A.is_answered(r)]:   # MQ1 / B-P2: parse
        A.answer_sources(r, classes, set(), A.PRIMARY_FIELD)
        A.answer_sources(r, classes, set(), A.CITED_FIELD)
    answered = {m: sum(r["model_requested"] == m for r in cat) for m in panel}
    dropped = [m for m in panel if answered[m] < ANSWERED_MIN * S1_CALLS_PER_MODEL]
    all_ans = _attach(A.build_answers(cat, named, units, classes), recs, channels, label)
    mq2, mq4 = A.mq2_search_use(all_ans, panel), A.mq4_google(all_ans)
    dropped += [m for m in panel if mq2[m]["dropped_from_g_star"] and m not in dropped]
    if mq4["drop_gemini"] and A.GEM4 in panel and A.GEM4 not in dropped:
        dropped.append(A.GEM4)
    models = [m for m in panel if m not in dropped]
    cited = _attach(A.build_answers(cat, named, units, classes, A.CITED_FIELD), recs, channels, label)
    excluded = A.t4_excluded(records)
    bt = A.read_csv(brand_table)
    s0_calls = {r["call_id"] for r in recs if r.get("condition") == "S0" and r.get("phase") == "B"}
    return {"label": label, "answers": [a for a in all_ans if a["model"] in models],
            "answers_cited": [a for a in cited if a["model"] in models], "models": models, "dropped": dropped,
            "answered_by_model": answered,
            "P": {c: A.p_t4(bt, coded_a, units, c, N3, excluded) for c in ("S0", "S1")},
            "C": {c: A.c_star_t4(bt, coded_b, units, c, N3, excluded) for c in ("S0", "S1")},
            "served": {m: sorted({str(r.get("served_model")) for r in cat if r["model_requested"] == m}) for m in panel},
            "texts": {r["call_id"]: r.get("text") for r in cat},
            "named_s0": set().union(*[named.get(c, set()) for c in s0_calls]) if s0_calls else set(),
            "coded_b": coded_b, "excluded": excluded,
            "inputs_sha256": {"raw": sha256_file(raw), "brand_table": sha256_file(brand_table),
                              "c5_raw": sha256_file(c5_raw) if c5_raw else None}}


def b_p1(w4, units, verdicts_doc, tol=1e-12):
    """G*_t4 recomputed with the imported functions equals Paper A's per-unit G* (o, g, rated) for all 112 units,
    and Paper A's H1/H2 rho_w reproduce to 1e-12 (on Paper A's own panel)."""
    panel = verdicts_doc["panel_models"]
    ans = [a for a in w4["answers"] if a["model"] in panel]
    if sorted(panel) != sorted(w4["models"]):
        raise Refused(f"B-P1: panel {w4['models']} differs from Paper A's {panel}")
    _, st = gstar(ans, units)
    bad = []
    for k, v in st.items():
        pa = verdicts_doc["units"][f"{k[0]}|{k[1]}"]
        if (v["o"], v["g"], v["rated"]) != (pa["o"], pa["g"], pa["rated"]):
            bad.append((k, (v["o"], v["g"], v["rated"]), (pa["o"], pa["g"], pa["rated"])))
    gs = A.gstar_map(st)
    legs = {}
    for h, comp in (("H1_Sep_Presence", w4["P"]), ("H2_Sep_Consistency", w4["C"])):
        for i, c in enumerate(("S1", "S0")):
            mine = A.sep_leg(gs, comp[c], 0, 0, 0)["rho_w"]
            theirs = verdicts_doc["legs"][h][i]["rho_w"]
            legs[f"{h}_{c}"] = {"recomputed": mine, "paper_A": theirs,
                                "match": mine is not None and theirs is not None and abs(mine - theirs) <= tol}
    ok = not bad and len(st) == 112 and all(v["match"] for v in legs.values())
    return {"passed": ok, "units": len(st), "unit_mismatches": [str(b) for b in bad[:10]],
            "n_unit_mismatches": len(bad), "legs": legs}


def b_p2(probes_t4, probes_t5):
    same = Path(probes_t4).read_bytes() == Path(probes_t5).read_bytes()
    return {"passed": same, "t4_sha256": sha256_file(probes_t4), "t5_sha256": sha256_file(probes_t5)}


def b_p3(w5, units, v045_unit_table, tol=1e-9):
    """P_S0 at t5 recomputed here equals v0.45's reported P_t5_S0 wherever both exist."""
    byc = A._by_coder(units)
    rows = A.read_csv(v045_unit_table)
    diffs, n = [], 0
    for r in rows:
        k = byc.get((r.get("substrate"), r.get("brand")))
        theirs = A._num(r.get("P_t5_S0"))
        mine = w5["P"]["S0"].get(k) if k else None
        if theirs is None or mine is None:
            continue
        n += 1
        if abs(mine - theirs) > tol:
            diffs.append((str(k), mine, theirs))
    return {"passed": n > 0 and not diffs, "compared": n, "mismatches": diffs[:10], "n_mismatches": len(diffs),
            "v045_unit_table_sha256": sha256_file(v045_unit_table)}


def read_sdri_cols(path, units):
    """SDRI (Paper A's H7 input, v1.13 read_sdri) plus SDRI_kg and SDRI_site for the sensitivities."""
    main = A.read_sdri(path, units)
    kg, site = {}, {}
    for r in A.read_csv(path):
        k = (r["substrate"], r["brand_id"])
        if k in units and str(r.get("phantom", "0")) != "1":
            kg[k], site[k] = A._num(r.get("SDRI_kg")), A._num(r.get("SDRI_site"))
    return main, kg, site


def _jsonable(o):
    if isinstance(o, dict):
        return {(f"{k[0]}|{k[1]}" if isinstance(k, tuple) else str(k)): _jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_jsonable(v) for v in o]
    if isinstance(o, set):
        return sorted(_jsonable(v) for v in o)
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, float) and not math.isfinite(o):
        return None
    return o


def write_json(path, doc):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(_jsonable(doc), indent=2, default=str), encoding="utf-8")


def run_stage1(a):
    g = guard_stage(1, a.v045_scored_commit)
    units, classes = A.load_brand_domains(), A.load_classes()
    channels, _ = load_channels()
    flags = roster_flags(units)
    _, vdoc = paper_a_verdict()
    w4 = load_wave_real("t4", a.t4, a.t4_coded, a.t4_brand_table, units, classes, channels)
    p1 = b_p1(w4, units, vdoc)
    if not p1["passed"]:
        raise Refused(f"B-P1 failed: {p1}")
    p2 = b_p2(a.probes_t4, a.probes_t5)
    if not p2["passed"]:
        raise Refused(f"B-P2 failed: {p2}")
    w5 = load_wave_real("t5", a.t5, a.t5_coded, a.t5_brand_table, units, classes, channels, a.t5_c5)
    p3 = b_p3(w5, units, a.v045_unit_table)
    if not p3["passed"]:
        raise Refused(f"B-P3 failed: {p3}")
    sdri, kg, site = read_sdri_cols(a.sdri, units)
    sdri_t5 = A.read_sdri(a.sdri_t5, units) if a.sdri_t5 else None
    il = il_from_coded(w4["coded_b"], channels, units, N3, w4["excluded"])
    inp = {"units": units, "flags": flags, "il": il, "sdri": sdri, "sdri_kg": kg, "sdri_site": site,
           "sdri_t5": sdri_t5, "waves": {"t4": w4, "t5": w5}, "paper_a_verdict": vdoc["gate"]["verdict"],
           "decision": read_decision(), "texts": {**w4["texts"], **w5["texts"]},
           "named_s0": w4["named_s0"] | w5["named_s0"]}
    out = OUT_DIR / "stage1"
    out.mkdir(parents=True, exist_ok=True)
    doc = stage1(inp, a.draws, N_BOOT, a.gap_b, True, out)
    doc.update(guard=g, parity={"B-P0": "passed", "B-P1": p1, "B-P2": p2, "B-P3": p3},
               inputs={"t4": w4["inputs_sha256"], "t5": w5["inputs_sha256"]},
               scorer_sha256=sha256_file(__file__), written_utc=datetime.now(timezone.utc).isoformat())
    write_json(out / "v122_stage1.json", doc)
    write_json(out / "v122_hb2_for_v045.json", {"HB2": doc["results"].get("HB2"), "verdict": doc["verdicts"]["HB2"],
                                                "label": CONDITIONAL_LABEL})
    print(f"Stage 1: GB {doc['verdicts']['GB']} -> {out}")


def run_stage2(a):
    guard_stage(2, t6_tags=tuple(a.t6_tags or ()))
    units, classes = A.load_brand_domains(), A.load_classes()
    channels, _ = load_channels()
    s1_path = OUT_DIR / "stage1" / "v122_stage1.json"
    if not s1_path.exists():
        raise Refused("REFUSED: Stage 2 needs this study's Stage 1 output (section 6).")
    s1 = json.loads(s1_path.read_text(encoding="utf-8"))
    w = {lab: load_wave_real(lab, raw, cd, bt, units, classes, channels,
                             panel="from_records" if lab == "t6" else None)
         for lab, raw, cd, bt in (("t4", a.t4, a.t4_coded, a.t4_brand_table), ("t5", a.t5, a.t5_coded,
                                                                                a.t5_brand_table),
                                  ("t6", a.t6, a.t6_coded, a.t6_brand_table))}
    gs = {lab: gstar(w[lab]["answers"], units)[0] for lab in w}
    doc = stage2(gs["t4"], gs["t5"], gs["t6"], units, a.draws, HB2_N_BOOT, {lab: w[lab]["answers"] for lab in w},
                 t6_models=w["t6"]["models"])
    doc.update(stage=2, stage1_sha256=sha256_file(OUT_DIR / "stage1" / "v122_stage1.json"),
               stage1_GB=s1["verdicts"]["GB"], written_utc=datetime.now(timezone.utc).isoformat())
    write_json(OUT_DIR / "stage2" / "v122_stage2.json", doc)
    print(f"Stage 2: {doc['verdicts']}")


def run_t4_parity(a):
    """B-P1 on archived t4 only (allowed before the lock: it reproduces Paper A's published numbers)."""
    units, classes = A.load_brand_domains(), A.load_classes()
    channels, _ = load_channels()
    _, vdoc = paper_a_verdict()
    w4 = load_wave_real("t4", a.t4, a.t4_coded, a.t4_brand_table, units, classes, channels)
    res = b_p1(w4, units, vdoc)
    res["inputs_sha256"] = w4["inputs_sha256"]
    res["channels_attached"] = sum(1 for x in w4["answers"] if x["channel"]) / max(len(w4["answers"]), 1)
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description="v1.22 Grounding Paper B scorer")
    ap.add_argument("--stage", type=int, choices=[1, 2])
    ap.add_argument("--check-t4-parity", action="store_true")
    ap.add_argument("--dry-run", metavar="DIR")
    ap.add_argument("--draws", type=int, default=N_PERM)
    ap.add_argument("--gap-b", type=int, default=GAP_B)
    for w in ("t4", "t5", "t6"):
        ap.add_argument(f"--{w}", help=f"{w} raw jsonl")
        ap.add_argument(f"--{w}-coded", help=f"{w} coder tables directory")
        ap.add_argument(f"--{w}-brand-table")
    ap.add_argument("--t5-c5", help="C5 arm raw jsonl (contingent)")
    ap.add_argument("--probes-t4")
    ap.add_argument("--probes-t5")
    ap.add_argument("--v045-unit-table")
    ap.add_argument("--v045-scored-commit")
    ap.add_argument("--sdri", default=str(V113_SDRI))
    ap.add_argument("--sdri-t5")
    ap.add_argument("--t6-tags", nargs="*")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    if a.dry_run:
        import dryrun_v1_22 as DR
        return DR.main(["--out", a.dry_run, "--draws", str(a.draws), "--gap-b", str(a.gap_b)])
    if a.check_t4_parity:
        res = run_t4_parity(a)
        if a.out:
            write_json(a.out, res)
        print(json.dumps(_jsonable({k: res[k] for k in ("passed", "units", "n_unit_mismatches", "legs")}), indent=1))
        return 0 if res["passed"] else 1
    if a.stage == 1:
        run_stage1(a)
        return 0
    if a.stage == 2:
        run_stage2(a)
        return 0
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
