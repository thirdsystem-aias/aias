#!/usr/bin/env python3
"""
score_aias_6_0_preview.py - AIAS 6.0 Preview (provisional six-part synthesis): the structure scorer.

STATUS: r1 (2026-11-10), lock candidate, written with the pre-registration
(osf/aias_6_0_preview/prereg/PRE_REGISTRATION_aias_6_0_preview.md; sections cited inline).
r0: gate reading (section 4.1), inclusion (4.2), S-tests (6.2), incremental and complete-profile
sets (6.1), I-tests (6.3), component status (6.4), H_Structure (6.5), wording class (6.6), the
descriptive composite check (7.2), carried-pair parity (11.2 MQ_Parity), sensitivities SA-SC (10),
hashed reads from git refs, MQ_Blind (11.2), the lock-manifest text, a synthetic dry run.
r1 (section 16): the ONE pinned-input block (INPUTS) and its hash checks; readers of v0.42, v1.14,
v1.12, v1.13, v1.11, S_t4 and AIAS 2.0 wired to the pinned paths with the schemas their own locked
scorers write; MQ_Lock, MQ_Join, MQ_Parity (P_S0 and C*_S0 recomputed with score_v1_14.comparators),
MQ_Panel, MQ_Gate; descriptives D1-D9; sensitivities SD-SH; `--run` (once; refuses without
MQ_Lock, with a PENDING or non-matching pin, or when its output exists); `--lock-manifest`,
`--verify-lock`, `--write-anchor`, `--pin-report`. Tested on synthetic data only. No network, no
model call.

Reused unchanged: scripts/score_v1_10.py (tag v1.10-prereg-r2): centred pooled within-category
Spearman, within-category ranks, the >= 5-units category rule, permutation and bootstrap, v1.10's
MNP; scripts/score_v1_14.py (tag v1.14-prereg-r1): comparators (the shared P / C* definition),
read_coded, dedupe_calls, excluded_calls (v0.42's analysis set), _models_dropped (drop rule).

SCORER_NOTES (where the pre-registration is silent; none changes a test, band, floor, seed or rule)
 N1  Unit key = (substrate, brand) as v0.42's coder writes it ("v0.19".."v0.23"). v1.13 keys its
     units (its substrate "v19".., brand_id); they are mapped through the coder_key column of its
     own registries/brand_domains_v1_13.csv, as v1.13 maps v1.14's and v1.12's units (its N3, N17).
 N2  P_S0, C*_S0 (and P_S1, C*_S1 for SH, D7) = score_v1_14.comparators on v0.42's brand table and
     coded tables at the scored ref, with v0.42's analysis-set exclusions recomputed as v1.14 does
     (excluded_calls on the deduplicated raw file at v0.42-acquisition-locked). Mentions (K3, D9) =
     comparators()["mentions"] (N3 S0 Phase B mentions, runs 1-3).
 N3  R*_S0 = v1.14 Stage 1 units[].R_star_S0 where rated_S0; R*_S1 where n_ranked_S1 >= 6 (v1.14's
     floor); units of v1.14's gate_excluded_substrates NOT RATED (as v1.12 N32 and v1.13 N17 read
     them); a unit v1.14 does not list is NOT RATED. MNP (SF) = score_v1_10.units_cat_brand (floor
     6) on the lead-item S0 rows of v1.14's rank table, whose SHA-256 must equal the Stage 1 record.
 N4  Cov* = v1.12's unit table, column cov_star_N3 (blank = NOT RATED); gate = v112_verdicts.json
     paper_A_verdict.verdict; "reduced panel" if models_dropped_section_7_3 is not empty.
 N5  G* = v1.13's v1_13_verdicts.json units[].G_star where rated; gate as last issued
     (stage_C2.coverage.gate_reissued.after, else stage_C2.ranking.gate_reissued.after, else
     gate.verdict); "reduced panel" if dropped_models is not empty. H1/H2 legs are stored in the
     order (S1, S0) (score_v1_13.gate_statistics): the S0 leg is legs[...][1].
 N6  v1.11: gate from v1_11_verdicts.json VERDICTS (after its noise guard), H1-H5 mapped to
     H1_Judge_Agreement .. H5_Sep_Ranking; the legacy-panel S (section 3.4, SG) = stage_j_v1_11.json
     scores.J1["F|t3|<substrate>|<brand>"].S where rated (its SHA-256 must equal Stage C's record).
 N7  Carried pairs (6.2) need the same statistic: v1.14 H1/H2 always (N3, S0); v1.12 H1/H2 only when
     its primary panel is N3 and its comparators are not cross-panel, H5 only when it gated (in
     paper_A_verdict.legs); v1.13 H1/H2 (S0 leg), H6 when active and computed (C1 or C2). The
     Paper A's own set is the pairwise-complete set after its exclusions (categories < 5 dropped).
 N8  D3: rank-correlation matrix = Pearson of centred within-category ranks on U_K; parallel
     analysis permutes each part's ranks within category independently per draw (1,000 draws,
     seed 600040) and reports the mean and 95th percentile of each ordered eigenvalue and the
     number of observed eigenvalues above that 95th percentile.
 N9  D5 level shift = mean(P_N3,t4 - P_L6,t3) over units with both; 90% interval from 2,000
     within-category bootstrap draws (seed 600030). D6 retest bands: rho >= 0.50 stable, < 0.30 not.
 N10 D8 variance shares on U_K: member m's share = Cov_w(X_m / k, A_K) / Var_w(A_K) (within-category
     deviations; the shares add to 1). D9 Presence terciles: within-category average rank of P_S0
     over (n + 1): <= 1/3 low, <= 2/3 middle, else high. Registry cells from v0.41's three-wave
     table (column cell, wave t3), read at v0.42's scored ref.
 N11 MQ_Blind's t4-based score files: v0.42's brand table, v1.14's Stage 1 output, v1.12's unit
     table, v1.13's verdict file, S_t4's table. A late file labels the Preview's own tests on that
     part "exploratory (MQ_Blind)"; carried verdicts keep their source's label.
 N12 Every sensitivity computes all its pairs itself (no carried verdict) and never changes a
     verdict; the verdicts that differ from the primary ones are listed (verdict_changes).
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import score_v1_10 as R  # noqa: E402  (locked at tag v1.10-prereg-r2; imported unchanged)
import score_v1_14 as V14  # noqa: E402  (locked at tag v1.14-prereg-r1; imported unchanged)

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
BRIDGE = {"CONFIRMED": "continues the published series",                 # section 4.1 (H_Gen_Presence / _Phi)
          "MARGINAL": "partly continues the published series",
          "FALSIFIED": "new series on the newest models; not comparable with published values",
          "UNDETERMINED": "bridge not determined (section 4.3)"}
N_PA = 1_000                                           # D3 parallel analysis draws (section 10)
RETEST_STABLE, RETEST_NOT = 0.50, 0.30                 # D6 (descriptive retest bands, section 2)
K2_MAX, K3_POINTS = 0.95, 5.0                          # section 7.2

# ===========================================================================
# PINNED INPUTS (sections 3, 11.2, 16): THE ONE CONFIGURATION BLOCK OF r1.
# Every input is read with `git show REF:PATH` (never the working tree) and logged with its commit, git
# blob and SHA-256 (outputs/inputs_read_aias_6_0_preview.json). Pinned now: v1.14 (locked), v1.11
# (locked), AIAS 2.0 (locked) and the v0.42 coder. PENDING values exist only at the component's own lock
# (v0.42, v1.12, v1.13: Wed 2026-11-11, about 3 pm CT): the coordinator fills them with
# `--pin-report` output (LOCK_STEPS.md step 2) BEFORE the lock manifest; a blob or path that moved at
# a component's lock is re-pinned here, nowhere else. `--write-anchor` and `--run` refuse while any pin
# is PENDING or does not match the repository. Scorer blobs pinned now are those of the lock candidates
# (branch tips v0.42 61515b4, v1.12 5fd87f6, v1.13 e98055f) and are re-checked at the lock tags.
# A component that has not locked when the Preview locks is set to {"status": NOT_LOCKED} (NOT RUN).
# Output paths are those the component's locked scorer writes; the git ref that holds each scored output
# is given at the data lock (`--run --ref NAME=REF`), and the component's scorer at that ref must be
# byte-identical to the pinned blob (else the run halts: section 14, "a hash mismatch halts").
# ===========================================================================
PENDING = "PENDING"
NOT_LOCKED = "NOT_LOCKED"
INPUTS = {
    "v0.42": {   # t4: P_S0 / C*_S0 (recomputed, MQ_Parity), drop rule (MQ_Panel), bridge labels (4.1)
        "lock_tag": "v0.42-prereg-r1", "lock_commit": PENDING,
        "scorer": "osf/v42/scripts/score_v0_42.py", "scorer_blob": "3bbe58db0db26763e6d5f9f022c09fcaa13fef03",
        "coder": "osf/v42/scripts/code_t4_v0_42.py", "coder_blob": "2d36735d512cf9e13b74010ba5a7f655fc7de0bc",
        "raw_ref": "v0.42-acquisition-locked", "raw": "osf/v42/data/t4_raw.jsonl",
        "default_scored_ref": "v0.42-scoring-locked",       # named by v0.42 LOCK_STEPS.md step 11.2
        "brand_table": "osf/v42/v42_brand_table.csv", "verdicts": "osf/v42/v42_verdicts.json",
        "coded_dir": "osf/v42/data/coded",
        "cells": "osf/v41/v41_three_wave_table.csv", "cells_blob": "86168a6854ac6d901340ed218e2dc2713887dccf"},
    "v1.14": {   # Ranking: R*_S0 (R*_S1 for SH, MNP for SF), STAGE1_VERDICT, Stage 2 GATE; carried H1, H2
        "lock_tag": "v1.14-prereg-r2", "lock_commit": "a5feb4b1c4b9e9d19979129afcfd616a50b88c64",   # C3: r1 20fbc342
        "scorer": "scripts/score_v1_14.py", "scorer_blob": "7aeb18316a23c699a0a6a4358e52ab09f9546ca9",   # r1 c479004c
        "stage1": "osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json",
        "rank_table": "osf/methodology/v1_14/outputs/stage1/rank_table_t4_v1_14.csv",
        "stage2": "osf/methodology/v1_14/outputs/stage2/stage2_v1_14.json"},
    "v1.12": {   # Coverage: cov_star_N3, GATE; carried H1, H2 (and H5 when it gated)
        "lock_tag": "v1.12-prereg-r1", "lock_commit": PENDING,
        "scorer": "osf/methodology/v1_12/scripts/score_v1_12.py",
        "scorer_blob": "75aabfc94bb77423148a2a1d1a7f39594ce36a17",
        "unit_table": "osf/methodology/v1_12/v112_unit_table.csv", "column": "cov_star_N3",
        "verdicts": "osf/methodology/v1_12/v112_verdicts.json",
        "anchor": "osf/methodology/v1_12/anchor/osf_anchor_v1_12.json",
        "h5_active_at_lock": PENDING},                       # section 16 item 2 (from v1.12's anchor)
    "v1.13": {   # Grounding: G* (units of v1_13_verdicts.json), GATE as last issued; carried H1, H2, H6
        "lock_tag": "v1.13-prereg-r1", "lock_commit": PENDING,
        "scorer": "osf/methodology/v1_13/scripts/score_v1_13.py",
        "scorer_blob": "40c43cb8027ac2cbb47d9b4df65651dad8876a5e",
        "verdicts": "osf/methodology/v1_13/v1_13_verdicts.json",
        "unit_map": "osf/methodology/v1_13/registries/brand_domains_v1_13.csv",
        "unit_map_blob": "1143a404b00861a215ae848a164d3066658ceccc",
        "anchor": "osf/methodology/v1_13/anchor/git_anchor_v1_13.json",
        "h4_active_at_lock": PENDING, "h6_active_at_lock": PENDING},   # section 16 item 2
    "v1.11": {   # Sentiment instrument: H1-H5 (gate reading, 4.1); legacy-panel S at t3 (3.4, SG)
        "lock_tag": "v1.11-prereg-r1", "lock_commit": "62e2d3828cec232f9d0fa0e3af5f3ca5955d617f",
        "scorer": "scripts/score_v1_11.py", "scorer_blob": "5e46e8632044268b5d30a2184600718961caa838",
        "stage_j": "osf/methodology/v1_11/outputs/stage_j_v1_11.json",
        "verdicts": "osf/methodology/v1_11/outputs/v1_11_verdicts.json"},
    "sentiment_paper_b": None,   # Sentiment Paper B's verdict: not pre-registered at r1 (section 4.1, 4.4)
    "S_t4": None,                # the t4 Sentiment study (section 3.4): not pre-registered at r1 -> NOT RUN;
                                 # if it locks later its table is given at run time (--s-t4) and logged
    "aias_2_0": {"ref": "aias-2-0-data-locked", "commit": "94f66182beac37d620006b1be127d72f2c5e0e1e",
                 "path": "osf/aias_2_0/aias_2_0_profiles.csv",
                 "sha256": "022ef56ecad9ddb60ad9ce0a2129698fd84ee9656630500e30b05f1e4b7e8c6e"},
}
DEFUNCT_V022 = ("Pontiac", "Oldsmobile", "Plymouth", "Mercury", "Saturn")   # v0.22 cell D (v1.12 DEFUNCT)
CODER_SUB = {"v19": "v0.19", "v20": "v0.20", "v21": "v0.21", "v22": "v0.22", "v23": "v0.23"}   # v1.13's
OUT_REL = "osf/aias_6_0_preview/outputs"
OUT_NAMES = {"inputs": "inputs_read_aias_6_0_preview.json", "gates": "gates_aias_6_0_preview.json",
             "results": "results_aias_6_0_preview.json", "profile": "profile_aias_6_0_preview.csv"}
MANIFEST_REL = "osf/aias_6_0_preview/prereg/LOCK_MANIFEST_aias_6_0_preview.sha256"
ANCHOR_REL = "osf/aias_6_0_preview/anchor/git_anchor_aias_6_0_preview.json"
DEVIATIONS_REL = "osf/aias_6_0_preview/anchor/DEVIATIONS.md"
BRANCH = "aias-6.0-preview"


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
    out = {"rho_A_P": rho_ap, "K2_passes": bool(math.isfinite(rho_ap) and abs(rho_ap) <= K2_MAX),
           "K3_dA": dA, "K3_dP_plus_5": dP + K3_POINTS if math.isfinite(dP) else float("nan"),
           "K3_passes": bool(math.isfinite(dA) and math.isfinite(dP) and dA <= dP + K3_POINTS),
           "n_low": len(low), "n_never": len(none), "adopted": False}
    out.update(composite_floor_and_shares(scores, K))
    return out


def composite_k1(h_structure_verdict: str | None, h_pc: str | None) -> dict:
    """Section 7.2 K1_K: H_Structure not FALSIFIED and H_PC_N3 not FALSIFIED."""
    return {"K1_passes": bool(h_structure_verdict not in (None, "FALSIFIED") and h_pc not in (None, "FALSIFIED")),
            "H_Structure": h_structure_verdict, "H_PC_N3": h_pc}


def composite_floor_and_shares(scores: dict, K: list[str]) -> dict:
    """Section 7.2: A_K restricted to the complete-profile set (v1.9's FLOOR analogue) with K2 inside that set,
    and each member's share of A_K's within-category variance on that set (N10). Descriptive only."""
    uk = complete_profile(scores, K)
    g = np.asarray([u[0] for u in uk])
    mask = R.keep_categories(g) if len(uk) else np.array([], bool)
    keys = [u for u, m in zip(uk, mask) if m]
    g = g[mask] if len(uk) else g
    if len(keys) < 3:
        return {"floor_set": {"n": len(keys), "rho_A_P": float("nan"), "K2_passes": False},
                "variance_shares_U_K": {}}
    X = np.array([[scores[u][m] for m in K] for u in keys], float)
    A = X.mean(axis=1)
    rho = R.pooled_within_rho(A, X[:, 0], g)
    dev = X.copy()
    for c in dict.fromkeys(g.tolist()):
        idx = np.where(g == c)[0]
        dev[idx] -= dev[idx].mean(axis=0)
    a_dev = dev.mean(axis=1)
    va = float(a_dev @ a_dev)
    shares = {m: (float((dev[:, j] / len(K)) @ a_dev) / va if va > 0 else float("nan")) for j, m in enumerate(K)}
    return {"floor_set": {"n": len(keys), "rho_A_P": rho, "K2_passes": bool(math.isfinite(rho) and abs(rho) <= K2_MAX)},
            "variance_shares_U_K": shares}


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
            c = carried.get(key)
            if c and c.get("units") is not None:      # parity on the Paper A's own unit set
                sub = {tuple(u): scores[tuple(u)] for u in c["units"] if tuple(u) in scores}
                s_res[key] = carry(s_test(sub, a, b, n_perm, boot), c)
            else:
                s_res[key] = carry(s_test(scores, a, b, n_perm, boot), c)
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
        out["composite_check"].update(composite_k1(hs["verdict"], out["H_PC_N3"]))
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


def sensitivities(scores: dict, states: dict, n_perm: int = 0, coi_unit=DENON, extra: dict | None = None,
                  primary: dict | None = None) -> dict:
    """SA-SC (r0) always; SD-SH (r1) when `extra` is given: {"MNP": {unit: MNP_t4} or None, "S_legacy":
    {unit: S_t3} or None, "S_legacy_state": gate state of Sentiment read as if S_t4 existed, "S1": {"P", "C",
    "R"} maps or None}. `primary` (the reported primary result) is the reference of verdict_changes."""
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
    if extra is None:
        return out
    K = included_set(states)
    uk = set(complete_profile(scores, K))
    sub = {u: s for u, s in scores.items() if u in uk}
    out["SD_S_tests_on_U_K"] = {"n_U_K": len(uk), "S_tests": {
        f"{a}x{b}": (lambda t: (t["rho"], t["n"], t["verdict"]))(s_test(sub, a, b, 0, False))
        for i, a in enumerate(K) for b in K[i + 1:]}}
    if "S" in K:
        out["SE_without_Sentiment"] = _verdicts_only(structure(scores, dict(states, S=NOT_RUN), n_perm=n_perm,
                                                               boot=False))
    else:
        out["SE_without_Sentiment"] = {"status": "not applicable: Sentiment is not in K"}
    mnp = extra.get("MNP")
    if mnp is not None and "R" in K:
        sf = {u: dict(s, R=mnp.get(u)) for u, s in scores.items()}
        out["SF_Ranking_by_MNP"] = _verdicts_only(structure(sf, states, n_perm=n_perm, boot=False))
    else:
        out["SF_Ranking_by_MNP"] = {"status": "not applicable: " + ("Ranking is not in K" if mnp is not None
                                                                      else "v1.14's rank table not read")}
    leg = extra.get("S_legacy")
    st = extra.get("S_legacy_state")
    if leg is not None and st is not None:
        sg = {u: dict(s, S=leg.get(u)) for u, s in scores.items()}
        r = _verdicts_only(structure(sg, dict(states, S=st), n_perm=n_perm, boot=False))
        r.update(state_of_Sentiment=st, label="cross-panel (legacy six-model panel, t3); descriptive")
        out["SG_Sentiment_legacy_panel"] = r
    else:
        out["SG_Sentiment_legacy_panel"] = {"status": "not applicable: v1.11's legacy-panel S not read"}
    s1 = extra.get("S1")
    if s1 is not None:
        sh = {u: dict(s, P=s1["P"].get(u), C=s1["C"].get(u), R=s1["R"].get(u) if "R" in s1 else s.get("R"))
              for u, s in scores.items()}
        out["SH_search_on_variants"] = _verdicts_only(structure(sh, states, n_perm=n_perm, boot=False))
    else:
        out["SH_search_on_variants"] = {"status": "not applicable: S1 variants not read"}
    ref = _verdicts_only(primary) if primary is not None and "H_Structure" in primary else None
    out["verdict_changes"] = verdict_changes(ref, out) if ref else []
    return out


def verdict_changes(ref: dict, sens: dict) -> list:
    """Every verdict that differs from the primary one under a sensitivity (section 10: listed beside it)."""
    out = []

    def cmp(name, v):
        if not isinstance(v, dict) or "H_Structure" not in v:
            return
        if v["H_Structure"] != ref["H_Structure"]:
            out.append({"sensitivity": name, "test": "H_Structure", "primary": ref["H_Structure"],
                        "under_sensitivity": v["H_Structure"]})
        if v.get("H_PC_N3") != ref.get("H_PC_N3"):
            out.append({"sensitivity": name, "test": "H_PC_N3", "primary": ref.get("H_PC_N3"),
                        "under_sensitivity": v.get("H_PC_N3")})
        for m, s in (v.get("status") or {}).items():
            if (ref.get("status") or {}).get(m) != s:
                out.append({"sensitivity": name, "test": f"status {m}", "primary": (ref.get("status") or {}).get(m),
                            "under_sensitivity": s})
        for k, (_rho, verd) in (v.get("S_tests") or {}).items():
            pv = (ref.get("S_tests") or {}).get(k)
            if pv is not None and pv[1] != verd:
                out.append({"sensitivity": name, "test": f"S-test {k}", "primary": pv[1], "under_sensitivity": verd})
    for name, v in sens.items():
        if name == "SC_leave_one_category_out":
            for cat, vv in v.items():
                cmp(f"SC without {cat}", vv)
        elif name == "SD_S_tests_on_U_K":
            for k, (_rho, _n, verd) in v["S_tests"].items():
                pv = (ref.get("S_tests") or {}).get(k)
                if pv is not None and pv[1] != verd:
                    out.append({"sensitivity": name, "test": f"S-test {k}", "primary": pv[1],
                                "under_sensitivity": verd})
        else:
            cmp(name, v)
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
# r1 LOCK TOOLING (sections 0, 11.1, 11.2 MQ_Lock, 16 item 4): manifest check, pins, anchor
# ===========================================================================
SEP_VERDICTS = ("CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED")
VALIDATION_LINE = ("Presence is the published AIAS component and Consistency its second (AIAS 2.0). Ranking, "
                   "Sentiment, Coverage and Grounding are provisional: the profile shows each with the state of its "
                   "first test; none has completed its validation.")                      # section 5
TITLE = "AIAS™ 6.0 Preview (provisional)"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _git_ok(root: Path, *args) -> str:
    """git's output, or "" when the command fails (absent tag, ref or path)."""
    r = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def _git_show(root: Path, ref: str, path: str) -> bytes | None:
    r = subprocess.run(["git", "-C", str(root), "show", f"{ref}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def tag_exists(root: Path, tag: str) -> bool:
    return bool(_git_ok(root, "rev-parse", "-q", "--verify", f"refs/tags/{tag}"))


def _jsonable(o):
    if isinstance(o, dict):
        return {("|".join(map(str, k)) if isinstance(k, tuple) else str(k)): _jsonable(v) for k, v in o.items()}
    if isinstance(o, (set, frozenset)):
        return [_jsonable(v) for v in sorted(o)]
    if isinstance(o, (list, tuple)):
        return [_jsonable(v) for v in o]
    if isinstance(o, (bool, np.bool_)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (float, np.floating)):
        return float(o) if math.isfinite(float(o)) else None
    return o


def _write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_jsonable(obj), indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")


def manifest_entries(text: str) -> list[tuple[str, str]]:
    return [tuple(line.split("  ", 1)) for line in text.splitlines() if line.strip()]


def verify_manifest(root: Path = ROOT, manifest_rel: str = MANIFEST_REL, tag: str | None = None,
                    append_only=(DEVIATIONS_REL,)) -> list[str]:
    """MQ_Lock's file check (section 11.2 as clarified on 2026-11-10, DEVIATIONS C2): every file of the lock
    manifest is unchanged on disk. With `tag`: the manifest and every locked file at the tag must match too, and
    anchor/DEVIATIONS.md, which section 14 makes grow after the lock, passes if its locked bytes are an unchanged
    prefix of the current file (entries are appended, never edited)."""
    p = root / manifest_rel
    if not p.exists():
        return [f"lock manifest missing: {manifest_rel}"]
    text = p.read_text(encoding="utf-8")
    bad = []
    if tag is not None:
        at_tag = _git_show(root, tag, manifest_rel)
        if at_tag is None or at_tag.decode("utf-8") != text:
            bad.append(f"lock manifest differs from the one at tag {tag}")
    for h, f in manifest_entries(text):
        q = root / f
        locked = _git_show(root, tag, f) if tag is not None else None
        if tag is not None and (locked is None or sha256_bytes(locked) != h):
            bad.append(f"differs from the manifest at tag {tag}: {f}")
        if not q.exists():
            bad.append(f"missing on disk: {f}")
            continue
        cur = q.read_bytes()
        if sha256_bytes(cur) == h:
            continue
        if f in append_only and locked is not None and sha256_bytes(locked) == h and cur.startswith(locked):
            continue
        bad.append(f"changed since the lock: {f}")
    return bad


def mq_lock(root: Path = ROOT, tag: str = PREREG_TAG) -> dict:
    """MQ_Lock (section 11.2): the tag and the anchor file exist, the anchor names the tag's commit and the
    manifest, and every file in the lock manifest is unchanged (verify_manifest with the tag)."""
    why = []
    if not tag_exists(root, tag):
        why.append(f"git tag {tag} does not exist")
    ap = root / ANCHOR_REL
    if not ap.exists():
        why.append(f"anchor file {ANCHOR_REL} does not exist")
    if not why:
        a = json.loads(ap.read_text(encoding="utf-8"))
        if a.get("tag") != tag or a.get("commit") != _git_ok(root, "rev-parse", f"{tag}^{{commit}}"):
            why.append("the anchor does not name the tag's commit")
        mp = root / MANIFEST_REL
        if not mp.exists() or a.get("lock_manifest_sha256") != sha256_bytes(mp.read_bytes()):
            why.append("the anchor's lock-manifest SHA-256 differs from the manifest")
        why += verify_manifest(root, MANIFEST_REL, tag)
    return {"ok": not why, "why": why, "tag": tag}


PIN_BLOBS = (("scorer", "scorer_blob"), ("coder", "coder_blob"), ("unit_map", "unit_map_blob"),
             ("cells", "cells_blob"))


def pin_problems(root: Path = ROOT, inputs: dict = INPUTS) -> list[str]:
    """Every pinned value against the repository (section 16 items 1-2): lock-tag commits, blobs of the producing
    scorers (and coder, unit map, cell table) at the lock tags, AIAS 2.0's file; PENDING values are listed."""
    out = []
    for name, spec in inputs.items():
        if not isinstance(spec, dict) or spec.get("status") == NOT_LOCKED:
            continue
        out += [f"{name}.{k} is PENDING (re-pin after the component's lock: LOCK_STEPS step 2)"
                for k, v in spec.items() if v == PENDING]
        tag = spec.get("lock_tag")
        if tag:
            c = _git_ok(root, "rev-parse", "-q", "--verify", f"{tag}^{{commit}}")
            if not c:
                out.append(f"{name}: lock tag {tag} not found")
                continue
            if spec.get("lock_commit") not in (None, PENDING) and c != spec["lock_commit"]:
                out.append(f"{name}: {tag} -> commit {c}, pinned {spec['lock_commit']}")
            for fld, bfld in PIN_BLOBS:
                if spec.get(fld) and spec.get(bfld) not in (None, PENDING):
                    b = _git_ok(root, "rev-parse", "-q", "--verify", f"{tag}:{spec[fld]}")
                    if b != spec[bfld]:
                        out.append(f"{name}: {spec[fld]} at {tag} is {b or 'absent'}, pinned {spec[bfld]}")
        elif spec.get("ref"):
            c = _git_ok(root, "rev-parse", "-q", "--verify", f"{spec['ref']}^{{commit}}")
            if spec.get("commit") and c != spec["commit"]:
                out.append(f"{name}: {spec['ref']} -> commit {c or 'absent'}, pinned {spec['commit']}")
            b = _git_show(root, spec["ref"], spec["path"])
            if b is None or sha256_bytes(b) != spec["sha256"]:
                out.append(f"{name}: {spec['ref']}:{spec['path']} SHA-256 differs from the pin")
    return out


def pin_report(root: Path = ROOT, inputs: dict = INPUTS) -> dict:
    """For the coordinator after the Wed locks (LOCK_STEPS step 2): what each lock tag holds now against the pins,
    whether the output names are still in the tagged scorer, and the activation records of section 16 item 2."""
    rep = {}
    for name, spec in inputs.items():
        if not isinstance(spec, dict) or not spec.get("lock_tag"):
            continue
        tag = spec["lock_tag"]
        c = _git_ok(root, "rev-parse", "-q", "--verify", f"{tag}^{{commit}}")
        r = {"lock_tag": tag, "tag_commit": c or None, "pinned_lock_commit": spec.get("lock_commit")}
        for fld, bfld in PIN_BLOBS:
            if spec.get(fld):
                r[bfld] = {"at_tag": _git_ok(root, "rev-parse", "-q", "--verify", f"{tag}:{spec[fld]}") or None,
                           "pinned": spec.get(bfld)}
        src = _git_show(root, tag, spec["scorer"]) if c else None
        if src is not None:
            txt = src.decode("utf-8", "replace")
            r["output_names_in_tagged_scorer"] = {
                k: Path(spec[k]).name in txt for k in ("brand_table", "verdicts", "unit_table", "stage1", "rank_table",
                                                      "stage2", "stage_j") if spec.get(k)}
        if spec.get("anchor"):
            branch = name if name != "v0.42" else "v0.42"
            doc = None
            for ref in (f"origin/{branch}", branch, tag):
                b = _git_show(root, ref, spec["anchor"])
                if b is not None:
                    doc = json.loads(b.decode("utf-8"))
                    r["anchor_read_at"] = ref
                    break
            legs = (doc or {}).get("conditional_legs") or {}
            if doc is None:
                r["activation"] = "anchor not found yet"
            elif name == "v1.12":
                r["h5_active_at_lock"] = str((legs.get("H5_Sep_Ranking") or {}).get("status", "")).startswith("ACTIVE")
            else:
                r["h4_active_at_lock"] = bool((legs.get("H4_Sep_Ranking") or {}).get("pushed_before_lock"))
                r["h6_active_at_lock"] = bool((legs.get("H6_Sep_Coverage") or {}).get("pushed_before_lock"))
        rep[name] = r
    rep["problems"] = pin_problems(root, inputs)
    return rep


T4_SCORE_FILES = (("v0.42", "brand_table"), ("v1.14", "stage1"), ("v1.12", "unit_table"), ("v1.13", "verdicts"))


def t4_score_files_present(root: Path = ROOT, inputs: dict = INPUTS) -> list[dict]:
    """Commits on any ref of the repository that add a t4-based score file (section 11.1: none may exist yet)."""
    out = []
    for name, key in T4_SCORE_FILES:
        spec = inputs.get(name)
        if not isinstance(spec, dict) or not spec.get(key):
            continue
        for line in _git_ok(root, "log", "--all", "--diff-filter=A", "--format=%H %cI", "--", spec[key]).splitlines():
            h, d = line.split(" ", 1)
            out.append({"input": name, "path": spec[key], "commit": h, "committer_date": d})
    return out


def write_anchor(root: Path = ROOT, osf_note: str = "", remote: str = "origin", inputs: dict = INPUTS,
                 late_reason: str | None = None) -> dict:
    """Section 0 / 11.1: anchor/git_anchor_aias_6_0_preview.json, written right after tag aias-6-0-preview-prereg-r1
    is pushed and before the OSF deposit (LOCK_STEPS step 6), as v1.14's write_anchor. Refuses if the anchor exists,
    a pin is PENDING or wrong, the manifest does not verify on disk and at the tag, the tag is not on `remote` or
    differs from the local tag, HEAD is not the tagged commit, or a t4-based score file already exists in the
    repository (unless `late_reason` is given; it is recorded and section 11.2 MQ_Blind then applies)."""
    anchor = root / ANCHOR_REL
    if anchor.exists():
        raise Halt(f"anchor already written: {ANCHOR_REL}")
    probs = pin_problems(root, inputs)
    if probs:
        raise Halt("pins: " + "; ".join(probs))
    if not tag_exists(root, PREREG_TAG):
        raise Halt(f"tag {PREREG_TAG} does not exist")
    bad = verify_manifest(root, MANIFEST_REL, PREREG_TAG, append_only=())
    if bad:
        raise Halt("lock manifest does not verify: " + "; ".join(bad))
    remote_lines = [ln for ln in _git_ok(root, "ls-remote", "--tags", remote, PREREG_TAG).splitlines()
                    if ln.endswith(f"refs/tags/{PREREG_TAG}")]
    if not remote_lines:
        raise Halt(f"tag {PREREG_TAG} is not on {remote}")
    tag_obj = _git_ok(root, "rev-parse", f"refs/tags/{PREREG_TAG}")
    if remote_lines[0].split()[0] != tag_obj:
        raise Halt(f"the tag on {remote} ({remote_lines[0].split()[0]}) differs from the local tag ({tag_obj})")
    commit = _git_ok(root, "rev-parse", f"{PREREG_TAG}^{{commit}}")
    if _git_ok(root, "rev-parse", "HEAD") != commit:
        raise Halt("HEAD is not the tagged commit")
    t4 = t4_score_files_present(root, inputs)
    if t4 and not late_reason:
        raise Halt(f"a t4-based score file already exists ({t4[0]['path']} @ {t4[0]['commit'][:12]}): the lock is "
                   f"late (section 11.1); pass --late-reason to record it (MQ_Blind then applies)")
    mbytes = (root / MANIFEST_REL).read_bytes()
    files = {f: {"sha256": h, "git_blob": git_blob_sha1(_git_show(root, PREREG_TAG, f))}
             for h, f in manifest_entries(mbytes.decode("utf-8"))}
    comps = {}
    for name, spec in inputs.items():
        if isinstance(spec, dict) and spec.get("lock_tag"):
            comps[name] = {"tag": spec["lock_tag"], "tag_object": _git_ok(root, "rev-parse", f"refs/tags/{spec['lock_tag']}"),
                           "commit": _git_ok(root, "rev-parse", f"{spec['lock_tag']}^{{commit}}"),
                           "tagger_date": tag_date(root, spec["lock_tag"])}
    doc = {"phase": PHASE_ID, "tag": PREREG_TAG, "tag_object": tag_obj, "commit": commit,
           "tree": _git_ok(root, "rev-parse", f"{commit}^{{tree}}"), "branch": BRANCH,
           "tagger_date": tag_date(root, PREREG_TAG), "remote_tag_ref": remote_lines[0], "recorded_utc": _now(),
           "repository": _git_ok(root, "remote", "get-url", remote), "osf_deposit": osf_note,
           "lock_manifest": MANIFEST_REL, "lock_manifest_sha256": sha256_bytes(mbytes),
           "lock_manifest_git_blob": git_blob_sha1(mbytes), "locked_files": files,
           "pinned_inputs": inputs, "component_lock_tags": comps,
           "t4_based_score_files_in_repository": t4, "late_reason": late_reason}
    _write_json(anchor, doc)
    return doc


# ===========================================================================
# r1 READERS (sections 3, 11.2): each component's scored output, with the schema its own locked scorer writes
# ===========================================================================
class Reader:
    """Inputs read from git refs with `git show REF:PATH` (never the working tree); every read is logged with the
    ref, its commit, the git blob and the SHA-256 (section 11.2: outputs/inputs_read_aias_6_0_preview.json)."""

    def __init__(self, root: Path = ROOT):
        self.root, self.log = Path(root), {}

    def commit(self, ref: str) -> str:
        return _git_ok(self.root, "rev-parse", "-q", "--verify", f"{ref}^{{commit}}")

    def blob(self, ref: str, path: str) -> str:
        return _git_ok(self.root, "rev-parse", "-q", "--verify", f"{ref}:{path}")

    def exists(self, ref: str, path: str) -> bool:
        return bool(self.blob(ref, path))

    def read(self, ref: str, path: str) -> bytes:
        b = _git_show(self.root, ref, path)
        if b is None:
            raise Halt(f"cannot read {ref}:{path}")
        self.log[f"{ref}:{path}"] = {"ref": ref, "commit": self.commit(ref), "path": path,
                                     "git_blob": git_blob_sha1(b), "sha256": sha256_bytes(b), "bytes": len(b)}
        return b

    def text(self, ref: str, path: str) -> str:
        return self.read(ref, path).decode("utf-8")

    def json(self, ref: str, path: str):
        return json.loads(self.text(ref, path))

    def rows(self, ref: str, path: str) -> list[dict]:
        return list(csv.DictReader(io.StringIO(self.text(ref, path))))

    def check_blob(self, ref: str, path: str, pinned: str, what: str) -> None:
        b = self.blob(ref, path)
        if b != pinned:
            raise Halt(f"pinned input hash does not match: {what}: {ref}:{path} is {b or 'absent'}, pinned {pinned}")


class _RefSource:
    """The source interface score_v1_14.read_coded expects (exists / text), over one git ref of a Reader."""

    def __init__(self, rd: Reader, ref: str):
        self.rd, self.ref = rd, ref

    def exists(self, rel: str) -> bool:
        return self.rd.exists(self.ref, rel)

    def text(self, rel: str) -> str:
        return self.rd.text(self.ref, rel)


def _num(v):
    if v is None or (isinstance(v, str) and not v.strip()):
        return None
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if math.isfinite(f) else None


def read_v042(rd: Reader, spec: dict, scored_ref: str, raw_ref: str | None = None) -> dict:
    """v0.42 (t4): brand table, coded tables and verdicts at the scored ref; raw answers at the acquisition tag.
    P and C* (S0 and S1) by score_v1_14.comparators on v0.42's analysis set (N2)."""
    raw_ref = raw_ref or spec["raw_ref"]
    rd.check_blob(scored_ref, spec["scorer"], spec["scorer_blob"], "v0.42 scorer at the scored ref")
    rd.check_blob(raw_ref, spec["coder"], spec["coder_blob"], "v0.42 coder at the acquisition tag")
    raw_b = rd.read(raw_ref, spec["raw"])
    if rd.exists(scored_ref, spec["raw"]) and rd.blob(scored_ref, spec["raw"]) != git_blob_sha1(raw_b):
        raise Halt(f"{spec['raw']} at {scored_ref} differs from the file at {raw_ref}")
    excluded = V14.excluded_calls(V14.dedupe_calls(V14.read_jsonl_text(raw_b.decode("utf-8"))))
    bt = rd.rows(scored_ref, spec["brand_table"])
    A, B = V14.read_coded(_RefSource(rd, scored_ref), spec["coded_dir"])
    verd = rd.json(scored_ref, spec["verdicts"])
    if verd.get("phase") != "v0.42":
        raise Halt(f"{scored_ref}:{spec['verdicts']} is not v0.42's verdict file")
    comp = {c: V14.comparators(bt, A, B, excluded, c) for c in ("S0", "S1")}
    rd.check_blob(scored_ref, spec["cells"], spec["cells_blob"], "v0.41 three-wave table (registry cells)")
    cells = {(r["substrate"], r["brand"]): ((r.get("cell") or "").strip() or None)
             for r in rd.rows(scored_ref, spec["cells"]) if r.get("wave") == "t3"}
    hv = verd.get("verdicts") or {}
    return {"ref": scored_ref, "keys": [(r["substrate"], r["brand"]) for r in bt],
            "P_S0": comp["S0"]["P"], "C_S0": comp["S0"]["C"], "P_S1": comp["S1"]["P"], "C_S1": comp["S1"]["C"],
            "mentions_S0": comp["S0"]["mentions"], "dropped_S0": V14._models_dropped(verd, "S0"),
            "dropped_S1": V14._models_dropped(verd, "S1"),
            "H_Gen_Presence": (hv.get("H_Gen_Presence") or {}).get("verdict"),
            "H_Gen_Phi": (hv.get("H_Gen_Phi") or {}).get("verdict"), "n_excluded_calls": len(excluded),
            "cells": cells, "brand_table_sha256": rd.log[f"{scored_ref}:{spec['brand_table']}"]["sha256"]}


def mnp_from_rank_table(data: bytes, excluded_subs=(), condition: str = "S0") -> dict:
    """v1.10's MNP per unit (score_v1_10.units_cat_brand, floor 6) on the lead-item rankable rows of v1.14's rank
    table, as v1.14 computes it for its descriptives (SF; N3)."""
    rows = []
    for r in csv.DictReader(io.StringIO(data.decode("utf-8"))):
        if (r.get("rule") != "lead_item" or r.get("condition") != condition or r.get("status") != "ok"
                or str(r.get("rankable")) != "1" or not r.get("brand") or r.get("k_mid") in ("", None)):
            continue
        rows.append({"panel": "N3", "wave": "t4", "category": r["category"], "brand": r["brand"],
                     "k_mid": float(r["k_mid"]), "k_min": int(float(r["k_min"])), "n": float(r["n_named"])})
    ex = set(excluded_subs)
    return {k: (float(v["MNP"]) if v["rated"] and k[0] not in ex else None) for k, v in R.units_cat_brand(rows).items()}


def read_v114(rd: Reader, spec: dict, ref: str) -> dict:
    """v1.14: Stage 1 output (R*_S0, R*_S1, P_S0, C*_S0, STAGE1_VERDICT, H1, H2), its rank table (MNP, SF) and the
    Stage 2 output if it exists (GATE, H3)."""
    rd.check_blob(ref, spec["scorer"], spec["scorer_blob"], "v1.14 scorer at the scored ref")
    s1b = rd.read(ref, spec["stage1"])
    s1 = json.loads(s1b.decode("utf-8"))
    if s1.get("phase") != "v1.14" or str(s1.get("stage")) != "1" or s1.get("prereg_tag") != spec["lock_tag"]:
        raise Halt(f"{ref}:{spec['stage1']} is not v1.14's Stage 1 output")
    if s1.get("dry_run"):
        raise Halt(f"{ref}:{spec['stage1']} is a v1.14 dry run, not its Stage 1 on t4")
    excl = set(s1.get("gate_excluded_substrates") or [])
    keys, R0, R1, P, C = [], {}, {}, {}, {}
    for u in s1.get("units") or []:
        k = (u["substrate"], u["brand"])
        keys.append(k)
        R0[k] = _num(u.get("R_star_S0")) if (u.get("rated_S0") and k[0] not in excl) else None
        R1[k] = _num(u.get("R_star_S1")) if (int(u.get("n_ranked_S1") or 0) >= R.RATING_FLOOR
                                              and k[0] not in excl) else None
        P[k], C[k] = u.get("P_S0"), u.get("C_star_S0")
    rt = rd.read(ref, spec["rank_table"])
    if sha256_bytes(rt) != s1.get("rank_table_t4_sha256"):
        raise Halt("v1.14's rank table differs from the SHA-256 in its Stage 1 output")
    s2 = None
    if rd.exists(ref, spec["stage2"]):
        s2 = rd.json(ref, spec["stage2"])
        if s2.get("dry_run") or s2.get("stage1_sha256") != sha256_bytes(s1b):
            raise Halt("v1.14's Stage 2 output is a dry run or was computed on another Stage 1 file")
    h = {k: {"rho": _num((s1.get(k) or {}).get("rho")), "n": (s1.get(k) or {}).get("n"),
             "verdict": (s1.get(k) or {}).get("verdict")} for k in ("H1_Sep_Presence", "H2_Sep_Consistency")}
    return {"ref": ref, "keys": keys, "R_S0": R0, "R_S1": R1, "P_S0": P, "C_S0": C,
            "MNP_S0": mnp_from_rank_table(rt, excl), "STAGE1_VERDICT": s1.get("STAGE1_VERDICT"),
            "GATE": (s2 or {}).get("GATE"), "H1": h["H1_Sep_Presence"], "H2": h["H2_Sep_Consistency"],
            "H3_retest": (s2 or {}).get("H3_Retest_Reliability"), "gate_excluded_substrates": sorted(excl),
            "inputs_read": s1.get("inputs_read") or {}, "stage1_sha256": sha256_bytes(s1b)}


def read_v112(rd: Reader, spec: dict, ref: str) -> dict:
    """v1.12: unit table (cov_star_N3) and v112_verdicts.json (GATE = paper_A_verdict.verdict, legs, H5 source)."""
    rd.check_blob(ref, spec["scorer"], spec["scorer_blob"], "v1.12 scorer at the scored ref")
    doc = rd.json(ref, spec["verdicts"])
    if doc.get("phase") != "v1.12" or doc.get("prereg_tag") != spec["lock_tag"]:
        raise Halt(f"{ref}:{spec['verdicts']} is not v1.12's verdict file")
    if (((doc.get("parity_gates") or {}).get("P1") or {}).get("passed")) is not True:
        raise Halt(f"{ref}:{spec['verdicts']}: parity gate P1 not passed: not v1.12's scored record")
    rows = rd.rows(ref, spec["unit_table"])
    col = spec["column"]
    if not rows or col not in rows[0]:
        raise Halt(f"{ref}:{spec['unit_table']} has no column {col}")
    keys, cov = [], {}
    for r in rows:
        k = (r["substrate"], r["brand"])
        keys.append(k)
        v = _num(r.get(col))
        if (r.get(col) or "").strip() and (v is None or not 0.0 <= v <= 100.0):
            raise Halt(f"{ref}:{spec['unit_table']}: {col} = {r.get(col)!r} for {k} is not a Cov* value")
        cov[k] = v
    pa, legs, verd = doc.get("paper_A_verdict") or {}, doc.get("legs") or {}, doc.get("verdicts") or {}
    same = doc.get("primary_panel") == "N3" and not (doc.get("comparators") or {}).get("cross_panel")
    carried = {}
    if same:
        for pair, hyp in ((("P", "Cov"), "H1_Sep_Presence"), (("C", "Cov"), "H2_Sep_Consistency"),
                          (("R", "Cov"), "H5_Sep_Ranking")):
            if hyp == "H5_Sep_Ranking" and hyp not in (pa.get("legs") or {}):
                continue            # H5 did not gate (v1.14 Stage 1 not SEPARABLE): the Preview's own test (6.2)
            rho = _num((legs.get(hyp) or {}).get("rho_w"))
            if rho is not None and verd.get(hyp) in SEP_VERDICTS:
                carried[pair] = {"rho": rho, "verdict": verd[hyp], "source": f"v1.12 {hyp}"}
    return {"ref": ref, "keys": keys, "Cov": cov, "gate": pa.get("verdict"), "gate_label": pa.get("label"),
            "reduced_panel": bool(doc.get("models_dropped_section_7_3")), "carried": carried,
            "h5_active": "H5_Sep_Ranking" not in (pa.get("inactive") or []),
            "h5_stage1_sha256": (doc.get("H5_ranking_source") or {}).get("sha256"),
            "primary_panel": doc.get("primary_panel"), "verdicts": verd,
            "unit_table_sha256": rd.log[f"{ref}:{spec['unit_table']}"]["sha256"]}


def read_v113(rd: Reader, spec: dict, ref: str) -> dict:
    """v1.13: v1_13_verdicts.json (Stage C1, Stage C2 appended): G* per unit (mapped to coder keys, N1), the gate
    as last issued, legs (H1/H2 S0 legs, H6) and the H4 record printed beside R* x G* (6.2, seed 600013)."""
    rd.check_blob(ref, spec["scorer"], spec["scorer_blob"], "v1.13 scorer at the scored ref")
    rd.check_blob(ref, spec["unit_map"], spec["unit_map_blob"], "v1.13 brand_domains (unit map)")
    doc = rd.json(ref, spec["verdicts"])
    if doc.get("phase") != "v1.13" or doc.get("stage") != "C1":
        raise Halt(f"{ref}:{spec['verdicts']} is not v1.13's Stage C1 file")
    umap = {}
    for r in rd.rows(ref, spec["unit_map"]):
        umap[(r["substrate"].strip(), r["brand_id"].strip())] = (CODER_SUB.get(r["substrate"].strip(), r["substrate"]),
                                                                (r.get("coder_key") or "").strip())
    keys, G = [], {}
    for k, s in (doc.get("units") or {}).items():
        sub, bid = k.split("|", 1)
        if (sub, bid) not in umap:
            raise Halt(f"v1.13 unit {k} is not in its brand_domains file")
        u = umap[(sub, bid)]
        keys.append(u)
        G[u] = _num(s.get("G_star")) if s.get("rated") else None
    gate = (doc.get("gate") or {}).get("verdict")
    c2 = doc.get("stage_C2") or {}
    for blk in ("ranking", "coverage"):                    # C2 re-issues, in v1.13's order (downgrade only)
        after = ((c2.get(blk) or {}).get("gate_reissued") or {}).get("after")
        if after:
            gate = after
    legs, verd = doc.get("legs") or {}, doc.get("verdicts") or {}
    act = (doc.get("gate") or {}).get("active") or {}
    carried = {}
    for pair, hyp in ((("P", "G"), "H1_Sep_Presence"), (("C", "G"), "H2_Sep_Consistency")):
        lg = legs.get(hyp)
        rho = _num(lg[1].get("rho_w")) if isinstance(lg, list) and len(lg) == 2 else None
        if rho is not None and verd.get(hyp) in SEP_VERDICTS:
            carried[pair] = {"rho": rho, "verdict": verd[hyp],
                             "source": f"v1.13 {hyp} (S0 leg; its verdict covers both legs)"}

    def cond_leg(hyp, blk):
        if isinstance(legs.get(hyp), list) and legs[hyp]:
            return verd.get(hyp), _num(legs[hyp][0].get("rho_w")), (doc.get({"H4_Sep_Ranking": "H4_ranking_source",
                                                                              "H6_Sep_Coverage": "H6_coverage_source"}[hyp]) or {})
        b = c2.get(blk) or {}
        if b.get("leg"):
            src = b.get({"H4_Sep_Ranking": "H4_ranking_source", "H6_Sep_Coverage": "H6_coverage_source"}[hyp]) or {}
            return b.get(hyp), _num(b["leg"].get("rho_w")), src
        return verd.get(hyp), None, {}
    h4v, h4rho, h4src = cond_leg("H4_Sep_Ranking", "ranking") if act.get("H4_Sep_Ranking") else ("INACTIVE", None, {})
    h6v, h6rho, h6src = cond_leg("H6_Sep_Coverage", "coverage") if act.get("H6_Sep_Coverage") else ("INACTIVE", None, {})
    if h6rho is not None and h6v in SEP_VERDICTS:
        carried[("Cov", "G")] = {"rho": h6rho, "verdict": h6v, "source": "v1.13 H6_Sep_Coverage"}
    return {"ref": ref, "keys": keys, "G": G, "gate": gate, "reduced_panel": bool(doc.get("dropped_models")),
            "carried": carried, "active": {k: bool(v) for k, v in act.items()},
            "H4_printed": {"verdict": h4v, "rho_w": h4rho, "statistic": "v1.13 H4: G* x R*_S1 (search on)"},
            "h4_stage1_sha256": h4src.get("sha256"), "h6_unit_table_sha256": h6src.get("sha256")}


def read_v111(rd: Reader, spec: dict, ref: str) -> dict:
    """v1.11: Stage C verdicts (VERDICTS, after its noise guard) for the gate reading of 4.1, and Stage J's J1
    scores for the legacy-panel S at t3 (3.4, SG); Stage J's SHA-256 must equal Stage C's record."""
    rd.check_blob(ref, spec["scorer"], spec["scorer_blob"], "v1.11 scorer at the scored ref")
    v = rd.json(ref, spec["verdicts"])
    if (v.get("phase") != "v1.11" or v.get("stage") != "C" or v.get("prereg_tag") != spec["lock_tag"]
            or v.get("dry_run")):
        raise Halt(f"{ref}:{spec['verdicts']} is not v1.11's Stage C output")
    sjb = rd.read(ref, spec["stage_j"])
    if sha256_bytes(sjb) != v.get("stage_j_sha256"):
        raise Halt("v1.11's Stage J file differs from the SHA-256 recorded at its Stage C")
    sj = json.loads(sjb.decode("utf-8"))
    VV = v.get("VERDICTS") or {}
    H = {"H1_Judge_Agreement": VV.get("H1"), "H2_Sep_Presence": VV.get("H2"), "H3_Sep_Consistency": VV.get("H3"),
         "H4_Stability_Short": VV.get("H4"), "H5_Sep_Ranking": VV.get("H5")}
    keys, legacy = [], {}
    for key, s in ((sj.get("scores") or {}).get("J1") or {}).items():
        block, wave, cat, brand = key.split("|", 3)
        if block == "F" and wave == "t3":
            keys.append((cat, brand))
            legacy[(cat, brand)] = _num(s.get("S")) if s.get("rated") else None
    return {"ref": ref, "H": H, "keys": keys, "S_legacy_t3": legacy,
            "noise_guard_applied": v.get("noise_guard_applied")}


def read_s_t4(rd: Reader, ref: str, path: str, column: str, lock_tag: str, rated_col: str | None = None) -> dict:
    """The t4 Sentiment study's scored unit table (section 3.4), if it is locked and scored by the data lock: given
    at run time (--s-t4 REF:PATH:COLUMN[:RATED_COL] --s-t4-lock-tag TAG) because it is not pre-registered at r1."""
    if not tag_exists(rd.root, lock_tag):
        raise Halt(f"S_t4: its lock tag {lock_tag} does not exist")
    keys, S = [], {}
    for r in rd.rows(ref, path):
        k = (r["substrate"], r["brand"])
        keys.append(k)
        ok = rated_col is None or str(r.get(rated_col)).strip().lower() in ("1", "true", "yes")
        S[k] = _num(r.get(column)) if ok else None
    return {"ref": ref, "path": path, "lock_tag": lock_tag, "keys": keys, "S": S}


def read_aias20(rd: Reader, spec: dict) -> dict:
    """AIAS 2.0's published profiles (legacy panel), wave t3: P and C* (rated only) for the bridge (7.3, D5)."""
    b = rd.read(spec["ref"], spec["path"])
    if sha256_bytes(b) != spec["sha256"]:
        raise Halt(f"pinned input hash does not match: {spec['ref']}:{spec['path']}")
    keys, P, C = [], {}, {}
    for r in csv.DictReader(io.StringIO(b.decode("utf-8"))):
        if r.get("wave") != "t3":
            continue
        k = (r["substrate"], r["brand"])
        keys.append(k)
        P[k] = _num(r.get("P"))
        C[k] = _num(r.get("C_star")) if str(r.get("rated")).strip() == "1" else None
    return {"keys": keys, "P_t3": P, "C_t3": C}


# ===========================================================================
# r1 CHECKS AT THE DATA LOCK (section 11.2): MQ_Join, MQ_Parity (comparators), cross-records, MQ_Gate
# ===========================================================================
def mq_join(full: dict, partial: dict, expected: int = R.N_BRAND_UNITS) -> dict:
    """MQ_Join (section 11.2 as clarified on 2026-11-10, DEVIATIONS C1): every unit table (`full`, one row per
    unit) carries the same `expected` keys 1:1; a score map that lists only units with data (`partial`: v1.14's
    Stage 1 units[], which lists units with a rankable mention; v1.11's Stage J scores, which list units with judged
    windows) carries no key outside them and no duplicate, and a unit it omits is NOT RATED. Halts otherwise."""
    ref, rep, bad = None, {}, []
    for name, keys in full.items():
        c, s = Counter(keys), set(keys)
        ref = s if ref is None else ref
        dup = sorted(k for k, n in c.items() if n > 1)
        r = {"rows": len(keys), "unique": len(s), "duplicates": dup[:10], "missing": sorted(ref - s)[:10],
             "extra": sorted(s - ref)[:10]}
        r["one_to_one"] = not dup and s == ref and len(s) == expected
        bad += [] if r["one_to_one"] else [name]
        rep[name] = r
    for name, keys in partial.items():
        c, s = Counter(keys), set(keys)
        dup = sorted(k for k, n in c.items() if n > 1)
        r = {"rows": len(keys), "duplicates": dup[:10], "extra": sorted(s - (ref or set()))[:10],
             "units_not_listed": len((ref or set()) - s)}
        r["ok"] = not dup and not r["extra"]
        bad += [] if r["ok"] else [name]
        rep[name] = r
    if bad:
        raise Halt(f"MQ_Join: unit keys differ in {bad}: "
                   f"{json.dumps(_jsonable({k: rep[k] for k in bad}))[:1500]}")
    return {"expected_units": expected, "tables": rep}


def mq_parity_comparators(v042: dict, v114: dict) -> dict:
    """MQ_Parity (section 11.2): P_S0 and C*_S0 recomputed from v0.42's files with score_v1_14.comparators equal the
    values in v1.14's Stage 1 units exactly, on every unit v1.14 lists (None = not computed / NOT RATED)."""
    bad = []
    for k in v114["keys"]:
        for name, a, b in (("P_S0", v042["P_S0"].get(k), v114["P_S0"].get(k)),
                           ("C_star_S0", v042["C_S0"].get(k), v114["C_S0"].get(k))):
            if not ((a is None and b is None) or (a is not None and b is not None and float(a) == float(b))):
                bad.append({"unit": k, "score": name, "recomputed": a, "v1.14": b})
    if bad:
        raise Halt(f"MQ_Parity: P/C* recomputed from v0.42's files differ from v1.14's Stage 1 on {len(bad)} values: "
                   f"{json.dumps(_jsonable(bad[:5]))}")
    return {"units_compared": len(v114["keys"]), "mismatches": 0, "passes": True}


def cross_checks(v042: dict, v114: dict | None, v112: dict | None, v113: dict | None, inputs: dict) -> dict:
    """The components' own records name the files the Preview reads (a hash chain); a difference halts."""
    out = {}
    bt = inputs["v0.42"]["brand_table"]
    if v114:
        rec = [v for k, v in v114["inputs_read"].items() if k == bt or k.endswith(":" + bt)]
        if rec and rec[0].get("sha256") != v042["brand_table_sha256"]:
            raise Halt("v1.14's Stage 1 read another v0.42 brand table than the Preview")
        out["v1.14_stage1_read_the_same_v042_brand_table"] = bool(rec) or "not recorded"
    pairs = []
    if v112 and v114:
        pairs.append(("v1.12_H5_read_the_same_v114_stage1", v112.get("h5_stage1_sha256"), v114["stage1_sha256"]))
    if v113 and v114:
        pairs.append(("v1.13_H4_read_the_same_v114_stage1", v113.get("h4_stage1_sha256"), v114["stage1_sha256"]))
    if v113 and v112:
        pairs.append(("v1.13_H6_read_the_same_v112_unit_table", v113.get("h6_unit_table_sha256"),
                      v112["unit_table_sha256"]))
    for name, recorded, read in pairs:
        if recorded and recorded != read:
            raise Halt(f"{name}: recorded SHA-256 {recorded} differs from the file the Preview read ({read})")
        out[name] = True if recorded else "not recorded"
    return out


def check_activation(v112: dict | None, v113: dict | None, inputs: dict) -> dict:
    """Section 16 item 2: the activation pinned at r1 must equal the one the component's output records."""
    out = {}
    if v112 and isinstance(inputs.get("v1.12"), dict):
        out["v1.12_H5"] = (inputs["v1.12"].get("h5_active_at_lock"), v112["h5_active"])
    if v113 and isinstance(inputs.get("v1.13"), dict):
        out["v1.13_H4"] = (inputs["v1.13"].get("h4_active_at_lock"), v113["active"].get("H4_Sep_Ranking", False))
        out["v1.13_H6"] = (inputs["v1.13"].get("h6_active_at_lock"), v113["active"].get("H6_Sep_Coverage", False))
    bad = {k: v for k, v in out.items() if bool(v[0]) != bool(v[1])}
    if bad:
        raise Halt(f"activation recorded by the component differs from the pin (section 16 item 2): {bad}")
    return {k: {"pinned": v[0], "in_output": v[1]} for k, v in out.items()}


def read_gate_states(v114: dict | None, v111: dict | None, v112: dict | None, v113: dict | None,
                     s_t4_available: bool, paper_b: str | None = None) -> dict:
    """MQ_Gate (section 4.1): each component's gate state, read before any structure statistic."""
    return {"R": gate_ranking(v114.get("GATE"), v114.get("STAGE1_VERDICT")) if v114 else NOT_RUN,
            "S": gate_sentiment(v111["H"] if v111 else None, s_t4_available, paper_b),
            "Cov": gate_component(v112.get("gate")) if v112 else NOT_RUN,
            "G": gate_component(v113.get("gate")) if v113 else NOT_RUN}


def part_labels(states: dict, v042: dict, v112: dict | None, v113: dict | None, panel_ok: bool) -> dict:
    """Section 5: the label of every part (4.2 label column, 4.1 bridge labels, 4.3 'reduced panel')."""
    br = lambda v: BRIDGE.get(v or "UNDETERMINED", f"unrecognised v0.42 verdict {v!r}: no bridge label")  # noqa: E731
    lab = {"P": {"label": "published AIAS component", "bridge": br(v042.get("H_Gen_Presence"))},
           "C": {"label": "AIAS 2.0 component", "bridge": br(v042.get("H_Gen_Phi"))}}
    for m in ("R", "S", "Cov", "G"):
        st = states.get(m, NOT_RUN)
        lab[m] = {"state": st, "label": LABELS.get(st), "shown_in_profile": st in IN_K_STATES,
                  "band": "under review (below the profile)" if st == MARGINAL else None}
    if "S" in lab and states.get("S") == NOT_RUN:
        lab["S"]["note"] = "legacy panel; not on the Preview panel (section 3.4) unless S_t4 is locked and scored"
    if v112 and v112.get("reduced_panel"):
        lab["Cov"]["reduced_panel"] = True
    if v113 and v113.get("reduced_panel"):
        lab["G"]["reduced_panel"] = True
    if not panel_ok:
        lab["panel"] = "reduced: an N3 model failed v0.42's drop rule in S0 (section 4.3); no structure test"
    return lab


# ===========================================================================
# r1 DESCRIPTIVES D1-D9 (section 10; no verdicts)
# ===========================================================================
def _dist(vals) -> dict:
    v = np.asarray([x for x in vals if _finite(x)], float)
    if not len(v):
        return {"n_rated": 0}
    q25, q75 = (float(x) for x in np.quantile(v, [0.25, 0.75]))
    return {"n_rated": int(len(v)), "median": float(np.median(v)), "q25": q25, "q75": q75, "iqr": q75 - q25,
            "min": float(v.min()), "max": float(v.max())}


def d1_distributions(scores: dict, parts=ORDER) -> dict:
    cats = sorted({u[0] for u in scores})
    return {m: {"all": dict(_dist([s.get(m) for s in scores.values()]), units=len(scores)),
                "by_category": {c: dict(_dist([s.get(m) for u, s in scores.items() if u[0] == c]),
                                        units=sum(1 for u in scores if u[0] == c)) for c in cats}}
            for m in parts}


def rho_w_maps(xd: dict, yd: dict, boot: bool = True, seed: int = BOOT_SEED) -> dict:
    """rho_w (section 2) between two unit maps on the units with both, categories with >= 5 units."""
    keys = sorted(k for k in xd if _finite(xd.get(k)) and _finite(yd.get(k)))
    g = np.asarray([k[0] for k in keys])
    ok, n, c = floor_ok(g.tolist())
    if keys:
        m = R.keep_categories(g)
        keys, g = [k for k, mm in zip(keys, m) if mm], g[m]
    x = np.array([xd[k] for k in keys], float)
    y = np.array([yd[k] for k in keys], float)
    rho = R.pooled_within_rho(x, y, g) if len(keys) >= 3 else float("nan")
    ci = list(R.boot_ci(x, y, g, seed)) if (boot and len(keys) >= 3) else [float("nan")] * 2
    return {"rho": rho, "n": n, "categories": c, "below_n_floor": not ok, "ci90": ci}


def rho_matrix(scores: dict, parts: list[str], boot: bool = True, units=None) -> dict:
    """D2 / D7: rho_w for every pair of `parts` on its pairwise-complete set (or inside `units`)."""
    sub = scores if units is None else {u: scores[u] for u in units if u in scores}
    out = {}
    for i, a in enumerate(parts):
        for b in parts[i + 1:]:
            t = s_test(sub, a, b, n_perm=0, boot=boot)
            out[f"{t['pair'][0]}x{t['pair'][1]}"] = {
                "rho": t["rho"], "n": t["n"], "categories": t["categories"], "ci90": t["ci90"],
                "below_n_floor": t["n"] < N_FLOOR_UNITS or t["categories"] < MIN_CATEGORIES}
    return out


def d3_dimensions(scores: dict, K: list[str], n_draws: int = N_PA, seed: int = PA_SEED) -> dict:
    """D3 (N8): eigenvalues of the U_K rank-correlation matrix, participation ratio (sum l)^2 / sum l^2, and a
    parallel analysis with within-category permutations of each part. Descriptive only."""
    uk = complete_profile(scores, K)
    ok, n, c = floor_ok([u[0] for u in uk])
    if len(K) < 2 or not ok:
        return {"members": K, "n_U_K": len(uk), "status": "UNDETERMINED (below the n floor or k < 2)"}
    mat, g = _centred_matrix(scores, uk, K)
    lam = np.sort(np.linalg.eigvalsh(np.corrcoef(mat, rowvar=False)))[::-1]
    rng = np.random.default_rng(seed)
    gidx = [np.where(g == k)[0] for k in dict.fromkeys(g.tolist())]
    null = np.empty((n_draws, len(K)))
    for d in range(n_draws):
        perm = np.empty_like(mat)
        for j in range(mat.shape[1]):
            for gi in gidx:
                perm[gi, j] = mat[rng.permutation(gi), j]
        null[d] = np.sort(np.linalg.eigvalsh(np.corrcoef(perm, rowvar=False)))[::-1]
    p95 = np.quantile(null, 0.95, axis=0) if n_draws else np.full(len(K), np.nan)
    return {"members": K, "n_U_K": int(len(g)), "categories": c, "eigenvalues": lam.tolist(),
            "participation_ratio": float(lam.sum() ** 2 / (lam ** 2).sum()),
            "parallel_analysis": {"draws": n_draws, "seed": seed,
                                  "null_mean": null.mean(axis=0).tolist() if n_draws else [],
                                  "null_p95": p95.tolist(), "n_above_null_p95": int((lam > p95).sum())}}


def unit_flags(keys) -> dict:
    """Section 8 'reported apart': the COI-flagged v0.19 unit, the v0.22 Defunct cell, the two Rare Beauty units."""
    out = {}
    for u in keys:
        f = []
        if u == DENON:
            f.append("COI-flagged unit (Declarations; sensitivity SA)")
        if u[0] == "v0.22" and u[1] in DEFUNCT_V022:
            f.append("v0.22 Defunct cell (G* not rated by rule)")
        if u[1] == "Rare Beauty":
            f.append("Rare Beauty (two units, v0.20 and v0.21)")
        if f:
            out[u] = f
    return out


def d4_profile_rows(scores: dict, labels: dict, cells: dict) -> list[dict]:
    """D4: one row per unit: every part, its rated flag, its label and its within-category rank among rated units."""
    wr = {m: {} for m in ORDER}
    for m in ORDER:
        for c in sorted({u[0] for u in scores}):
            ks = sorted(u for u in scores if u[0] == c and _finite(scores[u].get(m)))
            if ks:
                for u, rv in zip(ks, R._rank_avg(np.array([scores[u][m] for u in ks], float))):
                    wr[m][u] = (float(rv), len(ks))
    flags = unit_flags(scores)
    rows = []
    for u in sorted(scores):
        row = {"substrate": u[0], "brand": u[1], "cell": cells.get(u) or ""}
        for m in ORDER:
            v = scores[u].get(m)
            row[m] = v if _finite(v) else ""
            row[f"{m}_rated"] = int(_finite(v))
            row[f"{m}_label"] = (labels.get(m) or {}).get("label") or ""
            row[f"{m}_rank_in_category"] = wr[m][u][0] if u in wr[m] else ""
            row[f"{m}_rated_in_category"] = wr[m][u][1] if u in wr[m] else ""
        row["flags"] = "; ".join(flags.get(u, []))
        rows.append(row)
    return rows


def d5_bridge(P_t4: dict, C_t4: dict, P_t3: dict, C_t3: dict, n_boot: int = N_BOOT, seed: int = BOOT_SEED) -> dict:
    """D5 / section 7.3: rho_w(P_L6,t3, P_N3,t4) with the mean level shift of P (bootstrap interval, N9), and
    rho_w(C*_L6,t3, C*_N3,t4) without a level comparison. Descriptive; never pooled."""
    keys = sorted(k for k in P_t4 if _finite(P_t4.get(k)) and _finite(P_t3.get(k)))
    d = np.array([P_t4[k] - P_t3[k] for k in keys], float)
    g = np.asarray([k[0] for k in keys])
    ci = [float("nan")] * 2
    if len(d) and n_boot:
        rng = np.random.default_rng(seed)
        gidx = [np.where(g == c)[0] for c in dict.fromkeys(g.tolist())]
        draws = [float(d[np.concatenate([rng.choice(gi, size=len(gi), replace=True) for gi in gidx])].mean())
                 for _ in range(n_boot)]
        ci = [float(np.quantile(draws, 0.05)), float(np.quantile(draws, 0.95))]
    return {"label": "legacy six-model panel t3 (AIAS 2.0) against N3 t4; printed beside, never pooled",
            "rho_P": rho_w_maps(P_t3, P_t4, boot=bool(n_boot)), "rho_C_star": rho_w_maps(C_t3, C_t4, boot=bool(n_boot)),
            "P_level_shift": {"mean_t4_minus_t3": float(d.mean()) if len(d) else float("nan"), "n": len(keys),
                              "ci90": ci, "bootstrap_draws": n_boot, "seed": seed},
            "C_star_level": "not compared: phi_max = 9 on N3 against 7.2 on the legacy panel (section 3.2)"}


def d6_retest(v114: dict | None, scores_t4: dict, t5: dict | None = None) -> dict:
    """D6: t4 -> t5 where t5 allows. R*: v1.14 H3 as issued (Stage 2). P, C*, G*: only if t5 values are supplied
    (t5 is not yet pre-registered, section 11.3). Cov*: none; S: none."""
    out = {"R": {"source": "v1.14 H3_Retest_Reliability as issued", "record": v114["H3_retest"]}
           if (v114 and v114.get("H3_retest")) else {"status": "v1.14 Stage 2 output not available"}}
    for m in ("P", "C", "G"):
        if t5 and t5.get(m):
            r = rho_w_maps({u: s.get(m) for u, s in scores_t4.items()}, t5[m], boot=False)
            r["band"] = ("stable" if r["rho"] >= RETEST_STABLE else "not stable" if r["rho"] < RETEST_NOT
                         else "between the bands") if _finite(r["rho"]) else "UNDETERMINED"
            out[m] = r
        else:
            out[m] = {"status": "t5 values not supplied (t5 is not yet pre-registered; section 11.3)"}
    out["Cov"] = {"status": "none unless Coverage is re-asked under its Paper B (section 10, D6)"}
    out["S"] = {"status": "none: no judge call on t5 answers (section 11.3)"}
    return out


PANEL_TABLE = {"legacy six-model panel, t1-t3": ["P", "C*", "v1.10's Ranking statistic (MNP; Paper A MARGINAL)",
                                                  "v1.11's Sentiment S"],
               "N3, t4 week": ["P", "C*", "R*", "S (only if S_t4 is locked and scored)", "Cov*", "G*"]}


def d9_coverage(scores: dict, states: dict, K: list[str], cells: dict, mentions: dict) -> dict:
    """D9 / section 8: rated parts per unit (0..k; 0..6 with MARGINAL parts) per category and registry cell, U_K by
    category, rated share by within-category Presence tercile (N10), U_K against the 112, units reported apart."""
    shown = [m for m in ORDER if m in K or states.get(m) == MARGINAL]
    cats = sorted({u[0] for u in scores})
    cnt = lambda u, parts: sum(1 for m in parts if _finite(scores[u].get(m)))  # noqa: E731
    out = {"rated_parts_per_unit": {
        "K": {c: dict(Counter(cnt(u, K) for u in scores if u[0] == c)) for c in cats},
        "K_and_MARGINAL": {c: dict(Counter(cnt(u, shown) for u in scores if u[0] == c)) for c in cats},
        "by_registry_cell": {f"{c}|{cell}": dict(Counter(cnt(u, K) for u in scores if u[0] == c and cells.get(u) == cell))
                             for c in cats for cell in sorted({cells.get(u) for u in scores if u[0] == c} - {None})}}}
    uk = complete_profile(scores, K)
    out["U_K"] = {c: [u[1] for u in uk if u[0] == c] for c in cats}
    out["six_part_set"] = out["U_K"] if len(K) == 6 else "k < 6"
    terc = {}
    for c in cats:
        ks = [u for u in scores if u[0] == c and _finite(scores[u].get("P"))]
        if ks:
            r = R._rank_avg(np.array([scores[u]["P"] for u in ks], float)) / (len(ks) + 1)
            for u, q in zip(ks, r):
                terc[u] = "low" if q <= 1 / 3 else ("middle" if q <= 2 / 3 else "high")
    out["rated_share_by_presence_tercile"] = {
        m: {t: (lambda us: (sum(1 for u in us if _finite(scores[u].get(m))) / len(us)) if us else None)(
            [u for u in terc if terc[u] == t]) for t in ("low", "middle", "high")} for m in ORDER}
    ukset = set(uk)
    out["U_K_against_all"] = {"P": {"U_K": _dist([scores[u]["P"] for u in uk]),
                                    "all": _dist([s.get("P") for s in scores.values()])},
                              "mentions_N3_S0": {"U_K": _dist([mentions.get(u, 0) for u in uk]),
                                                 "all": _dist([mentions.get(u, 0) for u in scores])}}
    out["reported_apart"] = {"|".join(u): {"flags": f, "in_U_K": u in ukset,
                                           "scores": {m: scores[u].get(m) for m in ORDER}}
                             for u, f in unit_flags(scores).items()}
    out["parts_by_panel"] = PANEL_TABLE
    return out


# ===========================================================================
# r1 RUN (section 11.4): once, after the data lock
# ===========================================================================
BLIND_PARTS = {"v0.42": ("P", "C"), "v1.14": ("R",), "v1.12": ("Cov",), "v1.13": ("G",), "S_t4": ("S",)}


def _label_exploratory(res: dict, late_parts: set) -> None:
    """MQ_Blind (no halt): the Preview's own tests on a late input are labelled exploratory (N11)."""
    for t in (res.get("S_tests") or {}).values():
        if t.get("source") == "Preview" and set(t["pair"]) & late_parts:
            t["label"] = "exploratory (MQ_Blind)"
    for x, t in (res.get("I_tests") or {}).items():
        if ({x} | set(t.get("predecessors") or [])) & late_parts:
            t["label"] = "exploratory (MQ_Blind)"


def run(root: Path = ROOT, refs: dict | None = None, out_dir: Path | None = None, inputs: dict = INPUTS,
        s_t4: dict | None = None, t5: dict | None = None, n_perm: int = N_PERM, n_boot: int = N_BOOT,
        n_pa: int = N_PA, require_lock: bool = True, log=print) -> dict:
    """Section 11.2-11.4. refs: {"v0.42": scored ref (default v0.42-scoring-locked), "v0.42-raw": raw ref (default
    v0.42-acquisition-locked), "v1.14", "v1.12", "v1.13", "v1.11": the refs holding their scored outputs}; a component
    without a ref (or NOT_LOCKED) is NOT RUN. require_lock=False only for synthetic tests (MQ_Lock not checked)."""
    root = Path(root)
    out_dir = Path(out_dir) if out_dir else root / OUT_REL
    for n in OUT_NAMES.values():
        if (out_dir / n).exists():
            raise Halt(f"scored once (section 11.4): {out_dir / n} already exists")
    lock = mq_lock(root) if require_lock else {"ok": None, "why": ["not checked: synthetic test run"]}
    if require_lock and not lock["ok"]:
        raise Halt("MQ_Lock: " + "; ".join(lock["why"]))
    probs = pin_problems(root, inputs)
    if probs:
        raise Halt("pins: " + "; ".join(probs))
    refs = dict(refs or {})
    rd = Reader(root)
    sp42 = inputs["v0.42"]
    v042 = read_v042(rd, sp42, refs.get("v0.42") or sp42["default_scored_ref"], refs.get("v0.42-raw"))
    log(f"[aias6] v0.42 read at {v042['ref']}: {len(v042['keys'])} units; {v042['n_excluded_calls']} calls excluded")

    def opt(name, fn):
        sp = inputs.get(name)
        if not isinstance(sp, dict) or sp.get("status") == NOT_LOCKED or not refs.get(name):
            return None
        return fn(rd, sp, refs[name])
    v114, v112, v113, v111 = (opt("v1.14", read_v114), opt("v1.12", read_v112), opt("v1.13", read_v113),
                              opt("v1.11", read_v111))
    a20 = read_aias20(rd, inputs["aias_2_0"])
    st4 = read_s_t4(rd, **s_t4) if s_t4 else None
    full = {"v0.42 brand table": v042["keys"], "AIAS 2.0 profiles (t3)": a20["keys"]}
    if v112:
        full["v1.12 unit table"] = v112["keys"]
    if v113:
        full["v1.13 units (via coder_key)"] = v113["keys"]
    if st4:
        full["S_t4 unit table"] = st4["keys"]
    partial = {"v1.14 Stage 1 units": v114["keys"]} if v114 else {}
    if v111:
        partial["v1.11 Stage J scores (F, t3)"] = v111["keys"]
    join = mq_join(full, partial)
    parity = mq_parity_comparators(v042, v114) if v114 else {"status": "not applicable: no v1.14 Stage 1 output"}
    xchk = cross_checks(v042, v114, v112, v113, inputs)
    act = check_activation(v112, v113, inputs)
    blind_in = [("v0.42", v042["ref"], sp42["brand_table"])]
    for name, obj, key in (("v1.14", v114, "stage1"), ("v1.12", v112, "unit_table"), ("v1.13", v113, "verdicts")):
        if obj:
            blind_in.append((name, obj["ref"], inputs[name][key]))
    if st4:
        blind_in.append(("S_t4", st4["ref"], st4["path"]))
    if tag_exists(root, PREREG_TAG):
        mb = mq_blind(root, PREREG_TAG, [(r, p) for _n, r, p in blind_in])
        late = sorted({n for n, r, p in blind_in for (er, ep, _d) in mb["early"] if (er, ep) == (r, p)})
        mb.update(late_inputs=late, rule="no halt: the Preview's own tests on a late input are exploratory; a "
                                         "DEVIATIONS entry records it and Pablo is told")
    else:
        mb, late = {"ok": None, "note": f"tag {PREREG_TAG} not found: not checked (synthetic test run)"}, []
    panel_ok = not v042["dropped_S0"]                                            # MQ_Panel (no halt)
    states = read_gate_states(v114, v111, v112, v113, st4 is not None, inputs.get("sentiment_paper_b"))
    K = included_set(states)
    labels = part_labels(states, v042, v112, v113, panel_ok)
    gates_doc = {"phase": PHASE_ID, "title": TITLE, "created_utc": _now(), "gate_states": states, "K": K,
                 "labels": labels, "MQ_Panel": {"ok": panel_ok, "dropped_S0": v042["dropped_S0"]},
                 "H_Gen_Presence": v042["H_Gen_Presence"], "H_Gen_Phi": v042["H_Gen_Phi"],
                 "v1.14": {"STAGE1_VERDICT": (v114 or {}).get("STAGE1_VERDICT"), "GATE": (v114 or {}).get("GATE")},
                 "v1.12_GATE": (v112 or {}).get("gate"), "v1.13_GATE": (v113 or {}).get("gate"),
                 "v1.11_H1_H5": (v111 or {}).get("H"), "S_t4": bool(st4)}
    _write_json(out_dir / OUT_NAMES["gates"], gates_doc)                         # MQ_Gate: before any statistic
    log(f"[aias6] gate states {states}; K = {K}; panel {'complete' if panel_ok else 'REDUCED (section 4.3)'}")
    scores = {u: {"P": v042["P_S0"].get(u), "C": v042["C_S0"].get(u),
                  "R": v114["R_S0"].get(u) if v114 else None, "S": st4["S"].get(u) if st4 else None,
                  "Cov": v112["Cov"].get(u) if v112 else None, "G": v113["G"].get(u) if v113 else None}
              for u in sorted(v042["keys"])}
    carried = {}
    if v114:
        for pair, h in ((("P", "R"), "H1"), (("C", "R"), "H2")):
            if _finite(v114[h]["rho"]) and v114[h]["verdict"] in SEP_VERDICTS:
                carried[pair] = {"rho": v114[h]["rho"], "verdict": v114[h]["verdict"],
                                 "source": f"v1.14 {'H1_Sep_Presence' if h == 'H1' else 'H2_Sep_Consistency'}"}
    for obj in (v112, v113):
        if obj:
            carried.update(obj["carried"])
    res = structure(scores, states, carried, panel_ok, v042["mentions_S0"], n_perm, boot=n_boot > 0)
    _label_exploratory(res, {p for n in late for p in BLIND_PARTS[n]})
    s1_scores = {u: {"P": v042["P_S1"].get(u), "C": v042["C_S1"].get(u),
                     "R": v114["R_S1"].get(u) if v114 else None, "G": scores[u]["G"]} for u in scores}
    uk = complete_profile(scores, K)
    rows = d4_profile_rows(scores, labels, v042["cells"])
    desc = {"D1_distributions": d1_distributions(scores),
            "D2_rho_matrix": {"pairwise_complete": rho_matrix(scores, K, n_boot > 0),
                              "on_U_K": rho_matrix(scores, K, n_boot > 0, uk)},
            "D3_dimensions": d3_dimensions(scores, K, n_pa) if panel_ok else {"status": "no structure (section 4.3)"},
            "D4_profile_table": {"file": OUT_NAMES["profile"], "rows": len(rows)},
            "D5_bridge": d5_bridge(v042["P_S0"], v042["C_S0"], a20["P_t3"], a20["C_t3"], n_boot),
            "D6_retest": d6_retest(v114, scores, t5),
            "D7_search_on_profile": {"parts": {"P": "P_S1", "C": "C*_S1", "R": "R*_S1", "G": "G* (S1)"},
                                     "matrix": rho_matrix(s1_scores, ["P", "C", "R", "G"], n_boot > 0)},
            "D8_composite_check": res.get("composite_check", {"status": "no structure (section 4.3)"}),
            "D9_coverage": d9_coverage(scores, states, K, v042["cells"], v042["mentions_S0"])}
    sens = {"status": "no structure test (section 4.3)"}
    if panel_ok:
        sens = sensitivities(scores, states, 0, DENON, primary=res, extra={
            "MNP": v114["MNP_S0"] if v114 else None,
            "S_legacy": v111["S_legacy_t3"] if v111 else None,
            "S_legacy_state": gate_sentiment(v111["H"], True, inputs.get("sentiment_paper_b")) if v111 else None,
            "S1": {"P": v042["P_S1"], "C": v042["C_S1"], "R": v114["R_S1"] if v114 else {}}})
    doc = {"phase": PHASE_ID, "title": TITLE, "prereg_tag": PREREG_TAG, "created_utc": _now(),
           "validation_status_line": VALIDATION_LINE,
           "refs": {n: {"ref": o["ref"], "commit": rd.commit(o["ref"])} for n, o in
                    (("v0.42", v042), ("v1.14", v114), ("v1.12", v112), ("v1.13", v113), ("v1.11", v111),
                     ("S_t4", st4)) if o},
           "MQ_Lock": lock, "pins": "all pinned values match", "MQ_Join": join, "MQ_Parity_comparators": parity,
           "cross_records": xchk, "activation": act, "MQ_Blind": mb, "MQ_Panel": gates_doc["MQ_Panel"],
           "gate_states": states, "labels": labels, "K": K, "structure": res,
           "printed_beside": {"R*xG*": (v113 or {}).get("H4_printed")},
           "descriptives": desc, "sensitivities": sens,
           "seeds": {"S_tests": PAIR_SEEDS, "I_tests": I_SEEDS, "bootstrap": BOOT_SEED, "parallel_analysis": PA_SEED},
           "draws": {"permutation": n_perm, "bootstrap": n_boot, "parallel_analysis": n_pa}}
    _write_json(out_dir / OUT_NAMES["results"], doc)
    with open(out_dir / OUT_NAMES["profile"], "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["substrate", "brand"])
        w.writeheader()
        w.writerows(rows)
    _write_json(out_dir / OUT_NAMES["inputs"], {"phase": PHASE_ID, "created_utc": _now(), "inputs_read": rd.log})
    hs = res["H_Structure"]
    log(f"[aias6] H_Structure {hs['verdict']} (k {hs['k']}); H_PC_N3 {res.get('H_PC_N3')}; class "
        f"{res.get('wording_class')}; written to {out_dir}")
    return doc


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
    ap.add_argument("--run", action="store_true", help="score the locked inputs once, after the data lock "
                    "(section 11.4); refuses without MQ_Lock, with a PENDING or wrong pin, or if its output exists")
    ap.add_argument("--ref", action="append", default=[], metavar="NAME=REF",
                    help="--run: git ref holding a component's scored output: v0.42 (default v0.42-scoring-locked), "
                         "v0.42-raw (default v0.42-acquisition-locked), v1.14, v1.12, v1.13, v1.11; a component "
                         "without one is NOT RUN")
    ap.add_argument("--s-t4", metavar="REF:PATH:COLUMN[:RATED_COL]",
                    help="--run: the t4 Sentiment study's scored unit table, if locked and scored (section 3.4)")
    ap.add_argument("--s-t4-lock-tag", metavar="TAG", help="--run: the t4 Sentiment study's lock tag")
    ap.add_argument("--out", default="/tmp/aias6_dry", help="--dry-run output directory")
    ap.add_argument("--n-perm", type=int, default=500, help="--dry-run permutation draws")
    ap.add_argument("--lock-manifest", nargs="?", const=MANIFEST_REL, metavar="PATH",
                    help=f"write the lock manifest (default {MANIFEST_REL})")
    ap.add_argument("--verify-lock", action="store_true",
                    help="MQ_Lock's file check: the manifest on disk (and at the tag once it exists)")
    ap.add_argument("--pin-report", action="store_true",
                    help="after the Wed locks: lock tags, blobs and activation against the INPUTS block")
    ap.add_argument("--write-anchor", action="store_true",
                    help="after the tag is pushed: anchor/git_anchor_aias_6_0_preview.json")
    ap.add_argument("--osf-note", default="", help="--write-anchor: OSF deposit location recorded in the anchor")
    ap.add_argument("--late-reason", default=None,
                    help="--write-anchor: record why a t4-based score file already exists (section 11.1)")
    a = ap.parse_args(argv)
    try:
        if a.lock_manifest:
            p = Path(a.lock_manifest)
            p = p if p.is_absolute() else ROOT / p
            p.write_text(lock_manifest_text())
            print(f"lock manifest ({len(LOCK_FILES)} files) written to {p}")
            return 0
        if a.verify_lock:
            tag = PREREG_TAG if tag_exists(ROOT, PREREG_TAG) else None
            bad = verify_manifest(ROOT, MANIFEST_REL, tag)
            print("\n".join(bad) if bad else "lock manifest OK " + (f"(on disk and at tag {tag})" if tag
                                                                    else "(on disk; the tag does not exist yet)"))
            if tag and (ROOT / ANCHOR_REL).exists():
                lk = mq_lock(ROOT)
                print("MQ_Lock OK (tag, anchor, manifest)" if lk["ok"] else "MQ_Lock FAILS: " + "; ".join(lk["why"]))
                bad = bad or ([] if lk["ok"] else lk["why"])
            return 0 if not bad else 1
        if a.pin_report:
            rep = pin_report(ROOT)
            print(json.dumps(_jsonable(rep), indent=1))
            return 0 if not rep["problems"] else 1
        if a.write_anchor:
            d = write_anchor(ROOT, a.osf_note, late_reason=a.late_reason)
            print(json.dumps({k: d[k] for k in ("tag", "tag_object", "commit", "tree", "tagger_date",
                                                "lock_manifest_sha256")}, indent=1))
            return 0
        if a.run:
            refs = dict(x.split("=", 1) for x in a.ref)
            s_t4 = None
            if a.s_t4:
                if not a.s_t4_lock_tag:
                    raise Halt("--s-t4 needs --s-t4-lock-tag")
                parts = a.s_t4.split(":")
                s_t4 = {"ref": parts[0], "path": parts[1], "column": parts[2],
                        "rated_col": parts[3] if len(parts) > 3 else None, "lock_tag": a.s_t4_lock_tag}
            run(ROOT, refs, s_t4=s_t4)
            return 0
    except Halt as e:
        print(f"[aias6] REFUSED / HALT: {e}", file=sys.stderr)
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
