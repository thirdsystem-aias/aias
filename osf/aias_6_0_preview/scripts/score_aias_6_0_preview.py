#!/usr/bin/env python3
"""
score_aias_6_0_preview.py - AIAS 6.0 Preview (provisional six-part synthesis): the structure scorer.

STATUS: r0 SKELETON (2026-11-10), written with the pre-registration draft r0
(osf/aias_6_0_preview/prereg/PRE_REGISTRATION_aias_6_0_preview.md; sections cited inline).
Implemented and tested on synthetic data: gate reading (section 4.1), inclusion (4.2),
S-tests (6.2), incremental and complete-profile sets (6.1), I-tests (6.3), component
status (6.4), H_Structure (6.5), wording class (6.6), the descriptive composite check (7.2),
carried-pair parity (11.2 MQ_Parity), sensitivities SA-SC (10), hashed reads from git refs,
MQ_Blind (11.2), the lock-manifest text, and a synthetic dry run.
NOT YET IMPLEMENTED (r1, before the lock; section 16): wiring the readers to the pinned input
paths of v0.42, v1.12, v1.13, v1.14 and S_t4, MQ_Lock, MQ_Join, the P/C* recomputation with
score_v1_14.comparators, descriptives D1-D9, sensitivities SD-SH and --write-anchor.
`--run` therefore refuses. No network, no model call.

Reused unchanged: scripts/score_v1_10.py (tag v1.10-prereg-r2): centred pooled within-category
Spearman, within-category ranks, the >= 5-units category rule, permutation and bootstrap.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import score_v1_10 as R  # noqa: E402  (locked at tag v1.10-prereg-r2; imported unchanged)

PHASE_ID = "AIAS 6.0 Preview"
PREREG_TAG = "aias-6-0-preview-prereg-r1"
SEP_CONF, SEP_FALS = R.SEP_CONF, R.SEP_FALS            # 0.30 / 0.50 (section 2)
N_FLOOR_UNITS = R.N_FLOOR_UNITS                        # 30
MIN_UNITS_PER_CATEGORY = R.MIN_UNITS_PER_CATEGORY      # 5
MIN_CATEGORIES = 3                                     # v1.12 section 2.5
N_PERM = 10_000
N_BOOT = 2_000
PARITY_TOL = 1e-9

# Programme order (section 4.5): P (1.0), C (2.0), R (3.0), S (4.0), Cov (5.0), G (6.0)
ORDER = ["P", "C", "R", "S", "Cov", "G"]
NAMES = {"P": "Presence", "C": "Consistency", "R": "Ranking", "S": "Sentiment",
         "Cov": "Coverage", "G": "Grounding"}
PAIR_SEEDS = {("P", "C"): 600001, ("P", "R"): 600002, ("C", "R"): 600003, ("P", "S"): 600004,
              ("C", "S"): 600005, ("R", "S"): 600006, ("P", "Cov"): 600007, ("C", "Cov"): 600008,
              ("R", "Cov"): 600009, ("S", "Cov"): 600010, ("P", "G"): 600011, ("C", "G"): 600012,
              ("R", "G"): 600013, ("S", "G"): 600014, ("Cov", "G"): 600015}
I_SEEDS = {"C": 600021, "R": 600022, "S": 600023, "Cov": 600024, "G": 600025}
BOOT_SEED = 600030
PA_SEED = 600040

# Gate states (section 4.2)
PASS, PASS_RETEST, PASS_AI = "PASS", "PASS_RETEST_PENDING", "PASS_AI_JUDGED"
MARGINAL, FAIL, UNDET, NOT_RUN = "MARGINAL", "FAIL", "UNDETERMINED", "NOT_RUN"
IN_K_STATES = {PASS, PASS_RETEST, PASS_AI}
LABELS = {PASS: "provisional", PASS_RETEST: "provisional; retest pending",
          PASS_AI: "provisional; AI-judged, human-label check pending",
          MARGINAL: "under review", FAIL: None, UNDET: "not determined", NOT_RUN: "pending"}


class Halt(RuntimeError):
    """A check that must stop the run (section 11.2)."""


def pair_key(a: str, b: str) -> tuple[str, str]:
    """Pair in programme order (earlier, later)."""
    return (a, b) if ORDER.index(a) < ORDER.index(b) else (b, a)


# ===========================================================================
# 4.1 Reading each component's gate
# ===========================================================================
def gate_ranking(final_gate: str | None, interim: str | None) -> str:
    """v1.14: final GATE after Stage 2 if it exists; else the Stage 1 interim verdict."""
    if final_gate:
        return {"PASS": PASS, "MARGINAL": MARGINAL, "FAIL": FAIL, "UNDETERMINED": UNDET}[final_gate]
    if not interim:
        return NOT_RUN
    if interim.startswith("SEPARABLE"):
        return PASS_RETEST
    return {"MARGINAL": MARGINAL, "FAIL": FAIL, "UNDETERMINED": UNDET}[interim]


def gate_sentiment(h: dict | None, s_t4_available: bool, paper_b: str | None = None) -> str:
    """v1.11 PRIMARY H1-H5 read with the sister papers' gate rule; PENDING H5 does not block.
    Without a locked and scored S_t4 the Sentiment part is not on N3 (section 3.4): NOT_RUN."""
    if not h or not s_t4_available:
        return NOT_RUN
    keys = ["H1_Judge_Agreement", "H2_Sep_Presence", "H3_Sep_Consistency", "H4_Stability_Short",
            "H5_Sep_Ranking"]
    v = [h.get(k, "UNDETERMINED") for k in keys]
    if "FALSIFIED" in v:
        return FAIL
    if "UNDETERMINED" in v:
        return UNDET
    if all(x in ("CONFIRMED", "PENDING") for x in v):
        if paper_b == "FAIL":
            return FAIL              # section 4.1: a failed human-label check removes it from the profile
        return PASS if paper_b == "PASS" else PASS_AI
    return MARGINAL


def gate_component(gate: str | None) -> str:
    """v1.12 / v1.13 GATE verdict as issued (INSTRUMENT FAIL counts as FAIL)."""
    if not gate:
        return NOT_RUN
    return {"PASS": PASS, "MARGINAL": MARGINAL, "FAIL": FAIL, "INSTRUMENT FAIL": FAIL,
            "UNDETERMINED": UNDET}[gate]


def included_set(states: dict) -> list[str]:
    """K = {P, C} + every component in a PASS row (section 4.2), in programme order."""
    return [x for x in ORDER if x in ("P", "C") or states.get(x) in IN_K_STATES]


# ===========================================================================
# 6.2 S-tests
# ===========================================================================
def _finite(v) -> bool:
    return v is not None and isinstance(v, (int, float)) and math.isfinite(v)


def floor_ok(groups) -> tuple[bool, int, int]:
    """n floor of section 2: >= 30 units and >= 3 categories, after the >= 5-units rule."""
    c = Counter(groups)
    kept = {g: n for g, n in c.items() if n >= MIN_UNITS_PER_CATEGORY}
    n = sum(kept.values())
    return (n >= N_FLOOR_UNITS and len(kept) >= MIN_CATEGORIES), n, len(kept)


def band(value: float, ok: bool) -> str:
    """Separability bands on |value| (section 2)."""
    if not ok or not math.isfinite(value):
        return "UNDETERMINED"
    a = abs(value)
    if a >= SEP_FALS:
        return "FALSIFIED"
    return "CONFIRMED" if a <= SEP_CONF else "MARGINAL"


def s_test(scores: dict, a: str, b: str, n_perm: int = N_PERM, boot: bool = True) -> dict:
    """rho_w(a, b) on the pairwise-complete set; first-named (earlier) variable permuted."""
    a, b = pair_key(a, b)
    keys = sorted(u for u, s in scores.items() if _finite(s.get(a)) and _finite(s.get(b)))
    groups = [u[0] for u in keys]
    ok, n, ncat = floor_ok(groups)
    mask = R.keep_categories(np.asarray(groups)) if keys else np.array([], bool)
    x = np.array([scores[u][a] for u in keys], float)[mask] if keys else np.array([])
    y = np.array([scores[u][b] for u in keys], float)[mask] if keys else np.array([])
    g = np.asarray(groups)[mask] if keys else np.array([])
    rho = R.pooled_within_rho(x, y, g) if len(g) >= 3 else float("nan")
    seed = PAIR_SEEDS[(a, b)]
    p = R.perm_p(y, x, g, rho, seed, "two", n_perm) if (len(g) >= 3 and n_perm) else float("nan")
    ci = R.boot_ci(x, y, g, BOOT_SEED) if (boot and len(g) >= 3) else (float("nan"), float("nan"))
    return {"pair": [a, b], "rho": rho, "n": int(n), "categories": int(ncat), "p_perm": p,
            "perm_seed": seed, "ci90": list(ci), "verdict": band(rho, ok), "source": "Preview"}


def carry(own: dict, carried: dict | None) -> dict:
    """Section 6.2: a pair a Paper A has already tested keeps that verdict; the Preview's own
    statistic must equal the Paper A's (MQ_Parity) or the run halts."""
    if not carried:
        return own
    if not (math.isfinite(own["rho"]) and abs(own["rho"] - carried["rho"]) <= PARITY_TOL):
        raise Halt(f"MQ_Parity: pair {own['pair']} rho {own['rho']!r} != carried {carried['rho']!r} "
                   f"({carried.get('source')})")
    out = dict(own)
    out.update({"verdict": carried["verdict"], "source": carried.get("source", "Paper A")})
    return out


# ===========================================================================
# 6.1 Complete-profile set, 6.3 I-tests
# ===========================================================================
def rated_on(scores: dict, members: list[str]) -> list:
    """Units rated on every listed member (P defined)."""
    return sorted(u for u, s in scores.items() if all(_finite(s.get(m)) for m in members))


def incremental_set(scores: dict, K: list[str], x: str) -> tuple[list, list[str]]:
    """Section 6.1: U_<=X = units rated on X and on every member of K that precedes X.
    Returns (units, predecessors)."""
    preds = [m for m in K if ORDER.index(m) < ORDER.index(x)]
    return rated_on(scores, preds + [x]), preds


def complete_profile(scores: dict, K: list[str]) -> list:
    """Section 6.1: U_K = units rated on every member of K."""
    return rated_on(scores, K)


def _centred_matrix(scores: dict, keys: list, cols: list[str]) -> tuple[np.ndarray, np.ndarray]:
    groups = np.asarray([u[0] for u in keys])
    mask = R.keep_categories(groups)
    g = groups[mask]
    # always centred: the no-intercept regression needs zero-mean ranks within category, so the
    # uncentred sensitivity SB changes the S-tests only
    mat = np.column_stack([R.within_ranks(np.array([scores[u][c] for u in keys], float)[mask], g,
                                          centre=True) for c in cols])
    return mat, g


def _r2(y: np.ndarray, X: np.ndarray) -> float:
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    sst = float(y @ y)
    return 1.0 - float(resid @ resid) / sst if sst > 0 else float("nan")


def i_test(scores: dict, keys: list, target: str, preds: list[str], n_perm: int = N_PERM) -> dict:
    """Section 6.3: adjusted multiple correlation of target's centred within-category ranks on the
    predecessors' ranks, on U_<=X (keys); bands of section 2; one-sided permutation."""
    groups = [u[0] for u in keys]
    ok, n, c = floor_ok(groups)
    j = len(preds)
    if not ok or j == 0 or n - c - j <= 0:
        return {"target": target, "predecessors": preds, "n": int(n), "categories": int(c),
                "R2": float("nan"), "R2_adj": float("nan"), "R_adj": float("nan"),
                "p_perm": float("nan"), "verdict": "UNDETERMINED"}
    mat, g = _centred_matrix(scores, keys, [target] + preds)
    y, X = mat[:, 0], mat[:, 1:]
    r2 = _r2(y, X)
    r2a = 1.0 - (1.0 - r2) * (n - c) / (n - c - j)
    r_adj = math.sqrt(max(0.0, r2a))
    p = float("nan")
    if n_perm:
        rng = np.random.default_rng(I_SEEDS[target])
        gidx = [np.where(g == k)[0] for k in dict.fromkeys(g.tolist())]
        idx = np.arange(len(y))
        hits = 0
        for _ in range(n_perm):
            for gi in gidx:
                idx[gi] = rng.permutation(gi)
            hits += _r2(y[idx], X) >= r2 - 1e-12
        p = (hits + 1) / (n_perm + 1)
    return {"target": target, "predecessors": preds, "n": int(n), "categories": int(c), "R2": r2,
            "R2_adj": r2a, "R_adj": r_adj, "p_perm": p, "perm_seed": I_SEEDS[target],
            "verdict": band(r_adj, True)}


# ===========================================================================
# 6.4 Component status, 6.5 H_Structure, 6.6 wording class
# ===========================================================================
DISTINCT, PARTLY, NOT_DISTINCT = "DISTINCT", "PARTLY DISTINCT", "NOT DISTINCT"


def component_status(x: str, K: list[str], s_res: dict, i_res: dict) -> str:
    """Section 6.4; only S-tests with EARLIER members of K count (a FALSIFIED pair marks its later
    member); P is the anchor."""
    if x == "P":
        return DISTINCT
    earlier = [m for m in K if ORDER.index(m) < ORDER.index(x)]
    verdicts = [s_res[pair_key(m, x)]["verdict"] for m in earlier]
    iv = i_res.get(x, {}).get("verdict", "UNDETERMINED")
    allv = verdicts + [iv]
    if "FALSIFIED" in allv:
        return NOT_DISTINCT
    if all(v == "CONFIRMED" for v in allv):
        return DISTINCT
    if "UNDETERMINED" in allv:
        return "UNDETERMINED"
    return PARTLY


def h_structure(K: list[str], status: dict, panel_ok: bool = True) -> dict:
    """Section 6.5."""
    k = len(K)
    u = sum(1 for m in K if status.get(m) == "UNDETERMINED")
    d = sum(1 for m in K if status.get(m) in (DISTINCT, PARTLY))
    if not panel_ok or k < 3 or (k - u) < 3:
        verdict = "UNDETERMINED"
    elif all(status.get(m) == DISTINCT for m in K):
        verdict = "CONFIRMED"
    elif d <= 2 and u == 0:
        verdict = "FALSIFIED"
    else:
        verdict = "PARTIAL"
    return {"verdict": verdict, "k": k, "d": d, "u": u,
            "by_status": {s: [m for m in K if status.get(m) == s]
                          for s in (DISTINCT, PARTLY, NOT_DISTINCT, "UNDETERMINED")}}


def wording_class(verdict: str, k: int) -> str:
    """Section 6.6: A (CONFIRMED, k = 6), A_k (CONFIRMED, k < 6), B (PARTIAL), C (FALSIFIED: drafting
    pauses), U (UNDETERMINED)."""
    return {"CONFIRMED": "A" if k == 6 else "A_k", "PARTIAL": "B", "FALSIFIED": "C",
            "UNDETERMINED": "U"}[verdict]


# ===========================================================================
# 7.2 Descriptive composite check (v1.9's constraints, extended; never adopted)
# ===========================================================================
def composite_check(scores: dict, K: list[str], mentions: dict) -> dict:
    keys = sorted(u for u, s in scores.items() if _finite(s.get("P")))
    A = {u: float(np.mean([scores[u][m] for m in K if _finite(scores[u].get(m))])) for u in keys}
    groups = np.asarray([u[0] for u in keys])
    a = np.array([A[u] for u in keys])
    p = np.array([scores[u]["P"] for u in keys], float)
    mask = R.keep_categories(groups)
    rho_ap = R.pooled_within_rho(a[mask], p[mask], groups[mask]) if mask.sum() >= 3 else float("nan")
    low = [u for u in keys if 1 <= mentions.get(u, 0) <= 2]
    none = [u for u in keys if mentions.get(u, 0) == 0]
    if low and none:
        dA = float(np.mean([A[u] for u in low]) - np.mean([A[u] for u in none]))
        dP = float(np.mean([scores[u]["P"] for u in low]) - np.mean([scores[u]["P"] for u in none]))
    else:
        dA = dP = float("nan")
    return {"rho_A_P": rho_ap, "K2_passes": bool(math.isfinite(rho_ap) and abs(rho_ap) <= 0.95),
            "K3_dA": dA, "K3_dP_plus_5": dP + 5 if math.isfinite(dP) else float("nan"),
            "K3_passes": bool(math.isfinite(dA) and math.isfinite(dP) and dA <= dP + 5),
            "n_low": len(low), "n_never": len(none), "adopted": False}


# ===========================================================================
# Orchestration (pure; the r1 readers will build `scores`, `states` and `carried`)
# ===========================================================================
def structure(scores: dict, states: dict, carried: dict | None = None, panel_ok: bool = True,
              mentions: dict | None = None, n_perm: int = N_PERM, boot: bool = True) -> dict:
    """scores: {(substrate, brand): {"P": .., "C": .., "R": .., "S": .., "Cov": .., "G": ..}} with
    None for NOT RATED; states: gate state per component (R, S, Cov, G); carried: {(a, b): {"rho",
    "verdict", "source"}} for pairs a Paper A has tested (section 6.2)."""
    carried = carried or {}
    K = included_set(states)
    out = {"phase": PHASE_ID, "prereg_tag": PREREG_TAG, "K": K,
           "gate_states": {m: states.get(m, PASS if m in ("P", "C") else NOT_RUN) for m in ORDER},
           "labels": {m: LABELS.get(states.get(m)) for m in ORDER if m not in ("P", "C")}}
    if not panel_ok:
        out["H_Structure"] = h_structure(K, {}, panel_ok=False)
        out["wording_class"] = "U"
        return out
    s_res = {}
    for i, a in enumerate(K):
        for b in K[i + 1:]:
            key = pair_key(a, b)
            s_res[key] = carry(s_test(scores, a, b, n_perm, boot), carried.get(key))
    uk = complete_profile(scores, K)
    i_res = {}
    for x in K[1:]:
        keys_x, preds = incremental_set(scores, K, x)
        i_res[x] = i_test(scores, keys_x, x, preds, n_perm)
    status = {m: component_status(m, K, s_res, i_res) for m in K}
    hs = h_structure(K, status, panel_ok=True)
    out.update({"S_tests": {f"{a}x{b}": v for (a, b), v in s_res.items()},
                "H_PC_N3": s_res[("P", "C")]["verdict"],
                "U_K": {"n": len(uk), "units": [list(u) for u in uk]},
                "I_tests": i_res, "status": status, "H_Structure": hs,
                "wording_class": wording_class(hs["verdict"], hs["k"])})
    descriptive = {}
    for m in ORDER:                       # MARGINAL parts: their tests against K, descriptive only
        if states.get(m) == MARGINAL:
            for kmem in K:
                descriptive[f"{pair_key(kmem, m)[0]}x{pair_key(kmem, m)[1]}"] = s_test(
                    scores, kmem, m, 0, False)
    out["descriptive_marginal_pairs"] = descriptive
    if mentions is not None:
        out["composite_check"] = composite_check(scores, K, mentions)
    return out


# ===========================================================================
# Sensitivities SA, SB, SC (section 10; reported, never change a verdict). In a sensitivity
# every pair is computed by the Preview (a Paper A's carried verdict belongs to its own set).
# ===========================================================================
DENON = ("v0.19", "Denon")


def _verdicts_only(res: dict) -> dict:
    return {"H_Structure": res["H_Structure"]["verdict"], "H_PC_N3": res.get("H_PC_N3"),
            "status": res.get("status"),
            "S_tests": {k: (v["rho"], v["verdict"]) for k, v in res.get("S_tests", {}).items()}}


def sensitivities(scores: dict, states: dict, n_perm: int = 0, coi_unit=DENON) -> dict:
    out = {}
    without = {u: s for u, s in scores.items() if u != coi_unit}
    out["SA_without_coi_unit"] = _verdicts_only(structure(without, states, n_perm=n_perm, boot=False))
    with R.uncentred():
        out["SB_uncentred"] = _verdicts_only(structure(scores, states, n_perm=n_perm, boot=False))
    loo = {}
    for cat in sorted({u[0] for u in scores}):
        sub = {u: s for u, s in scores.items() if u[0] != cat}
        loo[cat] = _verdicts_only(structure(sub, states, n_perm=n_perm, boot=False))
    out["SC_leave_one_category_out"] = loo
    return out


# ===========================================================================
# Lock helpers (section 0, 11.2): manifest text, hashed reads from git, MQ_Blind
# ===========================================================================
import hashlib  # noqa: E402
import subprocess  # noqa: E402

PREVIEW = "osf/aias_6_0_preview"
LOCK_FILES = [f"{PREVIEW}/prereg/PRE_REGISTRATION_aias_6_0_preview.md",
              f"{PREVIEW}/prereg/precision_aias_6_0_preview.json",
              f"{PREVIEW}/scoping/precision_aias_6_0_preview.py",
              f"{PREVIEW}/scripts/score_aias_6_0_preview.py",
              f"{PREVIEW}/scripts/tests/test_score_aias_6_0_preview.py",
              f"{PREVIEW}/anchor/DEVIATIONS.md", f"{PREVIEW}/README.md",
              "scripts/score_v1_10.py", "scripts/score_v1_14.py"]


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git_blob_sha1(b: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def lock_manifest_text(files=LOCK_FILES, root: Path = ROOT) -> str:
    """'sha256  path' lines, sorted by path (the lock writes prereg/LOCK_MANIFEST_aias_6_0_preview.sha256)."""
    return "".join(f"{sha256_bytes((root / f).read_bytes())}  {f}\n" for f in sorted(files))


def _git(root: Path, *args) -> str:
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True,
                          text=True).stdout.strip()


def git_read(root: Path, ref: str, path: str, log: dict) -> bytes:
    """Read one input from a git ref (never the working tree) and log blob and SHA-256."""
    b = subprocess.run(["git", "-C", str(root), "show", f"{ref}:{path}"], check=True,
                       capture_output=True).stdout
    log[f"{ref}:{path}"] = {"git_blob": git_blob_sha1(b), "sha256": sha256_bytes(b)}
    return b


def read_score_csv(root: Path, ref: str, path: str, column: str, log: dict,
                   key=("substrate", "brand"), rated_col: str | None = None) -> dict:
    """{(substrate, brand): value or None}; blank, 'NA' or rated_col false -> None (NOT RATED)."""
    import csv
    import io
    rows = csv.DictReader(io.StringIO(git_read(root, ref, path, log).decode("utf-8")))
    out = {}
    for r in rows:
        v = (r.get(column) or "").strip()
        rated = True if rated_col is None else str(r.get(rated_col)).strip().lower() in ("1", "true", "yes")
        out[tuple(r[k] for k in key)] = float(v) if (v and v.upper() != "NA" and rated) else None
    return out


def tag_date(root: Path, tag: str) -> str:
    return _git(root, "for-each-ref", "--format=%(taggerdate:iso-strict)", f"refs/tags/{tag}")


def first_commit_date(root: Path, ref: str, path: str) -> str:
    """Committer date (ISO, strict) of the earliest commit reachable from ref that adds path."""
    lines = _git(root, "log", "--diff-filter=A", "--format=%cI", ref, "--", path).splitlines()
    return lines[-1] if lines else ""


def mq_blind(root: Path, tag: str, inputs: list[tuple[str, str]]) -> dict:
    """MQ_Blind (section 11.2): every t4-based input file must first appear after the lock tag.
    Returns {"ok": bool, "tag_date": .., "early": [(ref, path, date), ...]} (no halt: the
    affected tests are labelled exploratory and a DEVIATIONS entry is written)."""
    from datetime import datetime
    td = tag_date(root, tag)
    if not td:
        raise Halt(f"MQ_Lock: tag {tag} not found")
    t0 = datetime.fromisoformat(td)
    early = []
    for ref, path in inputs:
        d = first_commit_date(root, ref, path)
        if not d or datetime.fromisoformat(d) <= t0:
            early.append((ref, path, d))
    return {"ok": not early, "tag_date": td, "early": early}


# ===========================================================================
# Synthetic data (tests and --dry-run only; never program data)
# ===========================================================================
SIZES = {"v0.19": 16, "v0.20": 24, "v0.21": 24, "v0.22": 24, "v0.23": 24}   # 112 units


THRESHOLDS = {"C": -0.6, "R": -0.6, "S": -0.5, "Cov": -0.4, "G": -0.4}   # synthetic rating floors


def synthetic(seed: int = 600999, overlap: dict | None = None, thresholds: dict | None = None) -> tuple[dict, dict]:
    """112 synthetic units. Latent parts are independent unless `overlap` = {part: (source, w)}
    makes part = w * source + sqrt(1 - w^2) * noise (z units). One naming latent, driven by P,
    decides every rating floor (as the real floors all require mentions), so the rated sets are
    nested in the way the real ones are expected to be; P is always defined.
    Returns (scores, mentions)."""
    rng = np.random.default_rng(seed)
    overlap = overlap or {}
    thresholds = thresholds or THRESHOLDS
    scores, mentions = {}, {}
    for sub, n in SIZES.items():
        for i in range(n):
            z = {m: rng.standard_normal() for m in ORDER}
            for part, (src, w) in overlap.items():
                z[part] = w * z[src] + math.sqrt(max(0.0, 1 - w * w)) * z[part]
            named = z["P"] + 0.5 * rng.standard_normal()
            u = (sub, f"B{i:02d}")
            s = {"P": 50 + 15 * z["P"]}
            for m, t in thresholds.items():
                s[m] = 50 + 15 * z[m] if named + 0.3 * rng.standard_normal() > t else None
            scores[u] = s
            mentions[u] = int(max(0, round(3 + 3 * named)))
    return scores, mentions


def dry_run(out_dir: Path, n_perm: int = 500) -> dict:
    scores, mentions = synthetic()
    states = {"R": PASS_RETEST, "S": PASS_AI, "Cov": PASS, "G": PASS}
    res = structure(scores, states, mentions=mentions, n_perm=n_perm, boot=False)
    res["DRY_RUN"] = "synthetic data (seed 600999); not program data"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "dry_run_aias_6_0_preview.json").write_text(json.dumps(res, indent=1, default=str))
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--dry-run", action="store_true", help="synthetic data only; writes to --out")
    ap.add_argument("--run", action="store_true", help="score the locked inputs (r1; refuses in r0)")
    ap.add_argument("--out", default="/tmp/aias6_dry")
    ap.add_argument("--n-perm", type=int, default=500)
    ap.add_argument("--lock-manifest", metavar="PATH", help="write the lock manifest text to PATH (the lock "
                    "uses prereg/LOCK_MANIFEST_aias_6_0_preview.sha256)")
    a = ap.parse_args(argv)
    if a.lock_manifest:
        Path(a.lock_manifest).write_text(lock_manifest_text())
        print(f"lock manifest ({len(LOCK_FILES)} files) written to {a.lock_manifest}")
        return 0
    if a.run:
        print("refused: r0 skeleton. The input paths are pinned and wired at r1 (after the v1.12, v1.13 and "
              "v0.42 locks), and --run needs tag aias-6-0-preview-prereg-r1 and its anchor (section 11).")
        return 2
    if a.dry_run:
        res = dry_run(Path(a.out), a.n_perm)
        hs = res["H_Structure"]
        print(f"[dry run] K = {res['K']}; H_PC_N3 {res['H_PC_N3']}; H_Structure {hs['verdict']} "
              f"(k {hs['k']}, d {hs['d']}, u {hs['u']}); class {res['wording_class']}; "
              f"U_K n = {res['U_K']['n']}; written to {a.out}")
        return 0
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
