#!/usr/bin/env python3
"""
Tests for osf/aias_3_0/scripts/score_aias_3_0.py. Synthetic data only: no AIAS 3.0 statistic exists and none is
computed; no program answer, score or verdict is read (the lock and pin checks read git metadata and hashes only).
Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 osf/aias_3_0/scripts/tests/test_score_aias_3_0.py -v
"""
import importlib.util
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np
from scipy.stats import rankdata

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import score_aias_3_0 as S  # noqa: E402

A = S.A
ROOT = S.ROOT
PY = sys.executable
SCORER = HERE.parent / "score_aias_3_0.py"
PRECISION_PY = ROOT / "osf/aias_3_0/prereg/precision_aias_3_0.py"
PRECISION_JSON = ROOT / "osf/aias_3_0/prereg/precision_aias_3_0.json"
V112_TESTS = ROOT / "osf/methodology/v1_12/scripts/tests"


def load_precision():
    spec = importlib.util.spec_from_file_location("precision_aias_3_0", str(PRECISION_PY))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def world_maps(seed, n_per=(16, 24, 24, 24, 24), overlap=0.0, missing=0.0):
    rng = np.random.default_rng(seed)
    P, C, cov = {}, {}, {}
    for c, n in zip(A.CATS, n_per):
        for i in range(n):
            u = (c, f"b{i:02d}")
            p, q = rng.normal(), rng.normal()
            v = math.sqrt(overlap) * (p + q) / math.sqrt(2) + math.sqrt(1 - overlap) * rng.normal()
            P[u], C[u], cov[u] = 50 + 10 * p, 50 + 10 * q, 50 + 10 * v
            if rng.random() < missing:
                cov[u] = None
    return P, C, cov


def ref_r_adj(cov, P, C):
    """Independent computation (the precision note's own method) of R_adj on U3 after the >= 5-units rule."""
    keys = sorted(u for u in cov if all(S._f(d.get(u)) for d in (cov, P, C)))
    cats = {c for c in {k[0] for k in keys} if sum(k[0] == c for k in keys) >= 5}
    keys = [k for k in keys if k[0] in cats]
    cat = np.array([k[0] for k in keys])

    def cr(v):
        out = np.empty(len(v))
        for c in np.unique(cat):
            m = cat == c
            out[m] = rankdata(v[m]) - (m.sum() + 1) / 2.0
        return out
    y = cr(np.array([cov[k] for k in keys]))
    X = np.column_stack([cr(np.array([d[k] for k in keys])) for d in (P, C)])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ beta
    r2 = 1 - (r @ r) / (y @ y)
    n, c = len(keys), len(cats)
    r2a = 1 - (1 - r2) * (n - c) / (n - c - 2)
    return math.sqrt(max(0.0, r2a)), n, c


# =========================================================================== bands, floors, the joint test
class TestBandsAndFloors(unittest.TestCase):
    def test_bands(self):
        self.assertEqual(S.band(0.30), "CONFIRMED")
        self.assertEqual(S.band(-0.30), "CONFIRMED")
        self.assertEqual(S.band(0.3000001), "MARGINAL")
        self.assertEqual(S.band(0.4999999), "MARGINAL")
        self.assertEqual(S.band(0.50), "FALSIFIED")
        self.assertEqual(S.band(-0.7), "FALSIFIED")
        self.assertEqual(S.band(float("nan")), "UNDETERMINED")
        self.assertEqual(S.band(0.1, ok=False), "UNDETERMINED")

    def test_constants_are_the_registered_ones(self):
        self.assertEqual((S.SEP_CONF, S.SEP_FALS, S.N_FLOOR_UNITS, S.N_FLOOR_CATS, S.MIN_PER_CAT), (0.30, 0.50, 30, 3, 5))
        self.assertEqual((S.N_PERM, S.N_BOOT, S.PARITY_TOL), (10_000, 10_000, 1e-9))
        self.assertEqual(S.SEEDS, {"H3_Cov_Joint": 330001, "H3_Cov_P_U3": 330002, "H3_Cov_C_U3": 330003,
                                   "D_PC_U3": 330004, "calibration_bootstrap": 330010,
                                   "dissociation_bootstrap": 330020, "bridge_bootstrap": 330021})
        self.assertEqual(S.SENS_SEEDS, {"SA": 330030, "S-COI": 330031, "SB": 330032, "SC": 330033, "SD": 330034,
                                        "SE": 330035, "SF": 330036})
        self.assertEqual((S.K1_MAX, S.K2_MAX, S.K3_POINTS, S.TIE), (0.50, 0.95, 5.0, 0.01))
        self.assertEqual((S.FLOOR, S.HALF_FLOOR, S.MIN_MODELS, S.KAPPA_FULL, S.KAPPA_HALF, S.SF_FLOORS),
                         (14, 7, 2, 14, 7, (6, 28)))
        self.assertEqual(S.N3, ["claude-fable-5-2", "gpt-6-astra", "gemini-4-argon"])
        self.assertEqual(len(S.CANDIDATES), 8)

    def test_below_floor(self):
        self.assertTrue(S.below_floor(29, 5))
        self.assertTrue(S.below_floor(40, 2))
        self.assertFalse(S.below_floor(30, 3))


class TestJoint(unittest.TestCase):
    def test_matches_independent_computation(self):
        for seed, ov in ((1, 0.0), (2, 0.2), (3, 0.6)):
            P, C, cov = world_maps(seed, overlap=ov, missing=0.3)
            r = S.joint_test(cov, P, C, n_perm=0)
            ref, n, c = ref_r_adj(cov, P, C)
            self.assertAlmostEqual(r["R_adj"], ref, places=12)
            self.assertEqual((r["n"], r["categories"]), (n, c))
            self.assertEqual(r["verdict"], S.band(ref))

    def test_r2_adj_formula(self):
        r2a, ra = S.r_adj_of(0.10, 47, 5)
        self.assertAlmostEqual(r2a, 1 - 0.9 * 42 / 40)
        self.assertAlmostEqual(ra, math.sqrt(1 - 0.9 * 42 / 40))
        r2a, ra = S.r_adj_of(0.04, 47, 5)
        self.assertLess(r2a, 0)
        self.assertEqual(ra, 0.0)                                     # sqrt(max(0, R2_adj))
        r2a, ra = S.r_adj_of(0.5, 47, 5)
        self.assertAlmostEqual(ra, math.sqrt(1 - 0.5 * 42 / 40))
        self.assertTrue(math.isnan(S.r_adj_of(0.5, 7, 5)[1]))

    def test_category_rule_and_floor(self):
        P, C, cov = world_maps(4, n_per=(4, 8, 8, 8, 8))
        r = S.joint_test(cov, P, C, n_perm=0)
        self.assertNotIn("v0.19", r["per_category"])            # 4 units: the category does not enter
        self.assertEqual((r["n"], r["categories"]), (32, 4))
        P, C, cov = world_maps(5, n_per=(5, 5, 5, 5, 5))
        self.assertEqual(S.joint_test(cov, P, C, n_perm=0)["verdict"], "UNDETERMINED")   # n = 25 < 30
        P, C, cov = world_maps(6, n_per=(20, 20, 0, 0, 0))
        self.assertEqual(S.joint_test(cov, P, C, n_perm=0)["verdict"], "UNDETERMINED")   # 2 categories

    def test_full_overlap_is_falsified(self):
        P, C, cov = world_maps(7)
        cov = {u: P[u] + C[u] for u in P}
        r = S.joint_test(cov, P, C, n_perm=0)
        self.assertGreater(r["R_adj"], 0.9)
        self.assertEqual(r["verdict"], "FALSIFIED")

    def test_permutation_p(self):
        P, C, cov = world_maps(8, overlap=0.5)
        r1 = S.joint_test(cov, P, C, seed=330001, n_perm=99)
        r2 = S.joint_test(cov, P, C, seed=330001, n_perm=99)
        self.assertEqual(r1["p_perm"], r2["p_perm"])
        self.assertAlmostEqual(r1["p_perm"] * 100, round(r1["p_perm"] * 100))
        self.assertLess(r1["p_perm"], 0.05)
        P, C, cov = world_maps(9, overlap=0.0)
        self.assertGreater(S.joint_test(cov, P, C, n_perm=199)["p_perm"], 0.01)


class TestPrecisionNote(unittest.TestCase):
    """The scorer's statistic on the precision note's own generator (osf/aias_3_0/prereg/precision_aias_3_0.py, seed
    330040): identical values draw by draw, and the locked json reproduced cell by cell."""

    @classmethod
    def setUpClass(cls):
        cls.M = load_precision()
        cls.locked = json.loads(PRECISION_JSON.read_text(encoding="utf-8"))

    def _ours(self, rng, n, k, r2):
        C = self.M.C
        sizes = [n // C + (1 if i < n % C else 0) for i in range(C)]
        cat = np.repeat(np.arange(C), sizes)
        z = rng.standard_normal((n, k))
        s = z.sum(axis=1) / np.sqrt(k)
        x = np.sqrt(r2) * s + np.sqrt(1.0 - r2) * rng.standard_normal(n)
        keys = [(f"c{cat[i]}", f"u{i:03d}") for i in range(n)]
        cov = dict(zip(keys, x))
        P = dict(zip(keys, z[:, 0]))
        Cs = dict(zip(keys, z[:, 1]))
        return S.joint_test(cov, P, Cs, n_perm=0)["R_adj"]

    def test_draw_by_draw(self):
        a, b = np.random.default_rng(330040), np.random.default_rng(330040)
        for n in (40, 47):
            for r2 in (0.0, 0.09, 0.49):
                for _ in range(150):
                    self.assertAlmostEqual(self.M.r_adj_once(a, n, 2, r2), self._ours(b, n, 2, r2), places=12)

    def test_locked_json_reproduced(self):
        if os.environ.get("AIAS3_SKIP_FULL_PRECISION"):
            self.skipTest("full reproduction skipped by AIAS3_SKIP_FULL_PRECISION")
        rng = np.random.default_rng(self.locked["seed"])
        rows = []
        for n in (40, 47):
            for r2 in (0.0, 0.04, 0.09, 0.25, 0.49):
                v = np.array([self._ours(rng, n, 2, r2) for _ in range(self.locked["reps_per_cell"])])
                rows.append({"n": n, "k_predecessors": 2, "true_R2": r2,
                             "P_CONFIRMED_bands_030_050": float((v <= 0.30).mean()),
                             "P_FALSIFIED_bands_030_050": float((v >= 0.50).mean()),
                             "P_CONFIRMED_bands_050_070": float((v <= 0.50).mean()),
                             "P_FALSIFIED_bands_050_070": float((v >= 0.70).mean()),
                             "median_R_adj": float(np.median(v))})
        for mine, lk in zip(rows, self.locked["rows"]):
            for k, v in lk.items():
                self.assertAlmostEqual(mine[k], v, places=10, msg=f"{k} n={lk['n']} R2={lk['true_R2']}")
        # the figures section 5.2 quotes
        r40 = next(r for r in rows if r["n"] == 40 and r["true_R2"] == 0.0)
        r47 = next(r for r in rows if r["n"] == 47 and r["true_R2"] == 0.0)
        self.assertEqual(round(r40["P_CONFIRMED_bands_030_050"], 3), 0.912)
        self.assertEqual(round(r47["P_CONFIRMED_bands_030_050"], 3), 0.945)
        self.assertEqual(round(r40["P_FALSIFIED_bands_030_050"], 3), 0.002)
        self.assertLess(abs(r47["P_FALSIFIED_bands_030_050"] - 0.0003), 0.00006)


# =========================================================================== pairwise rows and the H2 carry rule
class TestPairs(unittest.TestCase):
    def test_first_named_is_permuted(self):
        P, C, cov = world_maps(11, overlap=0.3)
        r = S.pair_row(cov, P, 330002, n_perm=199)
        keys, x, y, g, info = A.paired(cov, P)
        self.assertEqual(r["p_perm"], A.perm_p(y, x, g, A.rho_w(x, y, g), 330002, "two", 199))   # Cov* permuted
        self.assertAlmostEqual(r["rho_w"], S.pair_row(P, cov, 1, 0)["rho_w"], places=14)
        self.assertEqual(r["verdict"], S.band(r["rho_w"]))

    def test_uncentred_variant(self):
        P, C, cov = world_maps(12)
        r = S.pair_row(cov, P, 1, 0, centred=False)
        keys, x, y, g, info = A.paired(cov, P)
        self.assertAlmostEqual(r["rho_w"], A.pooled_within_rho(x, y, g), places=14)

    def test_carry_rule(self):
        P, C, cov = world_maps(13)
        base = S.dissociation(P, C, cov, n_perm=0)
        cc = base["pairs"]["C_Cov"]
        carried = {"units": cc["units"], "rho_w": cc["rho_w"], "verdict": "CARRIED-WORD"}
        d = S.dissociation(P, C, cov, n_perm=0, carried_h2=carried)
        self.assertEqual(d["verdicts"]["H3_Cov_C_U3"], "CARRIED-WORD")
        self.assertTrue(d["pairs"]["C_Cov"]["U3_equals_v112_H2_set"])
        with self.assertRaises(S.Halt):
            S.dissociation(P, C, cov, n_perm=0, carried_h2=dict(carried, rho_w=cc["rho_w"] + 1e-6))
        d = S.dissociation(P, C, cov, n_perm=0, carried_h2=dict(carried, units=cc["units"][1:]))
        self.assertEqual(d["verdicts"]["H3_Cov_C_U3"], S.band(cc["rho_w"]))
        self.assertFalse(d["pairs"]["C_Cov"]["U3_equals_v112_H2_set"])

    def test_u3_needs_all_three(self):
        P, C, cov = world_maps(14)
        P[("v0.20", "b00")], C[("v0.21", "b00")], cov[("v0.22", "b00")] = None, None, None
        U3 = S.u3_units(P, C, cov)
        for u in (("v0.20", "b00"), ("v0.21", "b00"), ("v0.22", "b00")):
            self.assertNotIn(u, U3)
        self.assertEqual(len(U3), 109)

    def test_bootstrap_reported(self):
        P, C, cov = world_maps(15, overlap=0.2)
        b = S.dissociation_bootstrap(P, C, cov, n_boot=50)
        self.assertEqual(b["seed"], 330020)
        self.assertEqual(set(b["intervals"]), {"R_adj", "rho_Cov_P", "rho_Cov_C", "rho_P_C"})


# =========================================================================== calibration
def tiny_table():
    """One category, one brand per case, three models: (n, beta, beta_mid) per model."""
    tab = {}
    for m, (n, b, bm) in zip(S.N3, ((10, 0.2, 0.1), (5, -0.4, -0.2), (0, None, None))):
        tab[("v0.20", "X", m)] = {"n": n, "beta": b, "beta_mid": bm, "slots": 42}
    for m, n in zip(S.N3, (3, 0, 0)):
        tab[("v0.20", "Y", m)] = {"n": n, "beta": 0.5 if n else None, "beta_mid": 0.4 if n else None, "slots": 42}
    for m in S.N3:
        tab[("v0.20", "Z", m)] = {"n": 0, "beta": None, "beta_mid": None, "slots": 42}
    return tab


class TestCalibrationParts(unittest.TestCase):
    def test_floor_and_shrink(self):
        tab, units = tiny_table(), [("v0.20", "X"), ("v0.20", "Y"), ("v0.20", "Z")]
        fl = S.cov_from_table(tab, units, "Cov*", "FLOOR", 14)
        self.assertAlmostEqual(fl[("v0.20", "X")], 50 * (1 + (0.2 - 0.4) / 2))   # n_b 15 >= 14, 2 models
        self.assertIsNone(fl[("v0.20", "Y")])
        sh = S.cov_from_table(tab, units, "Cov*", "SHRINK", kappa=14)
        cu = 50 * (1 + (0.2 - 0.4) / 2)
        self.assertAlmostEqual(sh[("v0.20", "X")], 15 / 29 * cu + 14 / 29 * 50)
        self.assertAlmostEqual(sh[("v0.20", "Y")], 3 / 17 * 75 + 14 / 17 * 50)      # one model is enough under SHRINK
        self.assertIsNone(sh[("v0.20", "Z")])
        mid = S.cov_from_table(tab, units, "Cov*_mid", "FLOOR", 14)
        self.assertAlmostEqual(mid[("v0.20", "X")], 50 * (1 + (0.1 - 0.2) / 2))
        self.assertIsNone(S.cov_from_table(tab, units, "Cov*", "FLOOR", 28)[("v0.20", "X")])

    def test_composites(self):
        P, C, cov = {1: 60.0, 2: 40.0, 3: None}, {1: 80.0, 2: None, 3: 50.0}, {1: None, 2: 70.0, 3: 50.0}
        add = S.composite(P, C, cov, "ADD3")
        self.assertAlmostEqual(add[1], 70.0)
        self.assertAlmostEqual(add[2], 55.0)
        self.assertIsNone(add[3])
        mod = S.composite(P, C, cov, "MOD3")
        self.assertAlmostEqual(mod[1], 60 * 0.9 * 0.5)
        self.assertAlmostEqual(mod[2], 40 * 0.5 * 0.85)

    def test_k3(self):
        Am = {1: 30.0, 2: 32.0, 3: 20.0, 4: 22.0, 5: 99.0}
        P = {1: 20.0, 2: 22.0, 3: 18.0, 4: 18.0, 5: 99.0}
        ment = {1: 1, 2: 2, 3: 0, 4: 0, 5: 12}
        k = S.k3_windfall(Am, P, ment)
        self.assertAlmostEqual(k["dA"], 10.0)
        self.assertAlmostEqual(k["dP"], 3.0)
        self.assertFalse(k["passes"])                                # 10 > 3 + 5
        Am[1], Am[2] = 26.0, 27.0
        self.assertTrue(S.k3_windfall(Am, P, ment)["passes"])        # 5.5 <= 8

    def _row(self, stat, low, form, rel, passes=True, rap=0.9):
        return {"candidate": S.cand_name((stat, low, form)), "coverage_statistic": stat, "low_count_rule": low,
                "form": form, "passes_all": passes, "reliability": {"stepped_up": rel}, "K2_3": {"rho_w": rap}}

    def test_selection_and_ties(self):
        rows = [self._row("Cov*_mid", "FLOOR", "ADD3", 0.80), self._row("Cov*", "SHRINK", "MOD3", 0.795),
                self._row("Cov*", "FLOOR", "MOD3", 0.70), self._row("Cov*", "FLOOR", "ADD3", 0.95, passes=False)]
        s = S.select(rows)
        self.assertEqual(s["verdict"], "CANDIDATE COMPOSITE")
        self.assertEqual(s["selected"], "MOD3 | Cov* | SHRINK")       # tied within 0.01; Cov* before Cov*_mid
        self.assertEqual(set(s["tied"]), {"ADD3 | Cov*_mid | FLOOR", "MOD3 | Cov* | SHRINK"})
        self.assertFalse(s["adopted"])
        rows = [self._row("Cov*", "SHRINK", "ADD3", 0.80), self._row("Cov*", "FLOOR", "MOD3", 0.80)]
        self.assertEqual(S.select(rows)["selected"], "MOD3 | Cov* | FLOOR")          # FLOOR before SHRINK
        rows = [self._row("Cov*", "FLOOR", "MOD3", 0.80), self._row("Cov*", "FLOOR", "ADD3", 0.79)]
        self.assertEqual(S.select(rows)["selected"], "ADD3 | Cov* | FLOOR")          # ADD3 before MOD3
        rows = [self._row("Cov*", "FLOOR", "MOD3", 0.80), self._row("Cov*", "FLOOR", "ADD3", 0.7899)]
        self.assertEqual(S.select(rows)["selected"], "MOD3 | Cov* | FLOOR")          # outside the 0.01 tie

    def test_no_composite(self):
        rows = [self._row("Cov*", "FLOOR", "ADD3", 0.9, False, 0.97), self._row("Cov*", "FLOOR", "MOD3", 0.9, False, -0.96)]
        s = S.select(rows)
        self.assertEqual(s["verdict"], "NO COMPOSITE")
        self.assertAlmostEqual(s["best"]["rho_A_P"], -0.96)
        self.assertTrue(s["sentence"].startswith("No combination of the three scores"))


class TestCalibrationWorld(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.w = S.synthetic_world(41)
        cls.cal = S.calibration(cls.w, n_boot=30)

    def test_eight_rows_all_computed(self):
        self.assertEqual(self.cal["candidates"], 8)
        self.assertEqual([r["candidate"] for r in self.cal["table"]], [S.cand_name(c) for c in S.CANDIDATES])
        for r in self.cal["table"]:
            self.assertIn("rho_A_P", r["bootstrap"])
            self.assertEqual(r["bootstrap"]["seed"], 330010)
            self.assertEqual(r["passes_all"], r["K1_3"]["passes"] and r["K2_3"]["passes"] and r["K3_3"]["passes"])

    def test_cal_rule(self):
        rule = self.cal["CAL_RULE"]["selected"]
        self.assertEqual(rule["rule"], "Cov* (v1.12 section 2.4), floor 14, >= 2 models")
        self.assertAlmostEqual(rule["share_rated_112"], sum(S._f(v) for v in self.w["Cov"].values()) / 112)
        self.assertEqual(set(self.cal["CAL_RULE"]["descriptive_beside"]), {"floor_6", "floor_28", "Cov*_mid_floor_14"})

    def test_floor_candidate_equals_unit_cov(self):
        cov = S.cov_from_table(self.w["tabs"]["full"], self.w["units"], "Cov*", "FLOOR", 14)
        self.assertEqual(cov, self.w["Cov"])

    def test_k2_is_over_all_units_with_A(self):
        r = self.cal["table"][0]
        self.assertEqual(r["K2_3"]["n"], sum(1 for v in self.w["P"].values() if S._f(v)))


# =========================================================================== class, sensitivities, descriptives
class TestClass(unittest.TestCase):
    def test_table(self):
        W = S.wording_class
        self.assertEqual(W("CONFIRMED", None)["class"], "A")
        self.assertEqual(W("CONFIRMED", "DISTINCT")["class"], "A")
        self.assertEqual(W("MARGINAL", None)["class"], "B")
        self.assertEqual(W("CONFIRMED", "PARTLY DISTINCT")["class"], "B")
        self.assertEqual(W("MARGINAL", "DISTINCT")["class"], "B")
        self.assertEqual(W("FALSIFIED", None)["class"], "C")
        self.assertEqual(W("CONFIRMED", "NOT DISTINCT")["class"], "C")        # the less favourable of the two
        self.assertTrue(W("CONFIRMED", "NOT DISTINCT")["drafting_pauses"])
        self.assertTrue(W("CONFIRMED", "NOT DISTINCT")["both_stated"])
        self.assertEqual(W("UNDETERMINED", None)["class"], "U")
        self.assertEqual(W("UNDETERMINED", "DISTINCT")["class"], "U")
        self.assertEqual(W("UNDETERMINED", "NOT DISTINCT")["class"], "C")
        self.assertEqual(W("UNDETERMINED", "PARTLY DISTINCT")["class"], "U")  # N11
        self.assertEqual(W("CONFIRMED", "UNDETERMINED")["class"], "A")         # N11: read as not issued
        with self.assertRaises(ValueError):
            W("SOMETHING", None)


class TestSensitivities(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.w = S.synthetic_world(42)
        cls.doc = S.dissociation_doc(cls.w, None, {"status": "not issued", "G3": None},
                                     (cls.w["P_t3_legacy"], dict(cls.w["C"])), n_perm=20, n_boot=20)

    def test_all_seven_in_order(self):
        self.assertEqual(list(self.doc["sensitivities"]), S.SENS_ORDER)
        self.assertEqual(set(self.doc["sensitivities"]["SF"]), {"floor_6", "floor_28"})
        self.assertEqual(len(self.doc["sensitivities"]["SC"]["leave_one_category_out"]), 5)
        self.assertNotIn("calibration", self.doc["sensitivities"]["SA"])

    def test_exclusions(self):
        w = S._world_without(self.w, list(S.COI_UNITS))
        self.assertEqual(len(w["units"]), 112 - sum(1 for u in S.COI_UNITS if u in self.w["units"]))
        w = S._world_without(self.w, cats=["v0.20", "v0.21"])
        self.assertEqual({u[0] for u in w["units"]}, {"v0.20", "v0.21"})
        self.assertEqual(S.DENON, ("v0.19", "Denon"))

    def test_changes_listed_never_applied(self):
        prim = self.doc["verdicts"]
        sens = {"SX": {"dissociation": {t: {"verdict": "FALSIFIED"} for t in prim}}}
        ch = S.verdict_changes(prim, sens)
        self.assertEqual({c["test"] for c in ch}, {t for t, v in prim.items() if v != "FALSIFIED"})
        self.assertEqual(self.doc["verdicts"], prim)

    def test_descriptives(self):
        d = self.doc["descriptives"]
        self.assertEqual(sum(v["units"] for v in d["D2_rated"]["per_category"].values()), 112)
        self.assertAlmostEqual(d["D2_rated"]["U3_share_of_112"], self.doc["U3"]["n"] / 112)
        self.assertIn("mean_level_shift_N3_minus_t3", d["D3_bridge"]["P"])
        self.assertIn("level_comparison", d["D3_bridge"]["C_star"])
        self.assertEqual(self.doc["class"]["G3"], "not issued")
        rows = S.profile_rows(self.w)
        self.assertEqual(len(rows), 112)
        self.assertEqual(sum(r["in_U3"] for r in rows), self.doc["U3"]["n"])

    def test_terciles(self):
        P = {("c", i): float(i) for i in range(9)}
        t = S.terciles(P)
        self.assertEqual([t[("c", i)] for i in range(9)], ["low"] * 3 + ["middle"] * 3 + ["high"] * 3)

    def test_compare_sq(self):
        c = S.compare_sq({}, {}, {"H3_Cov_Joint": ("CONFIRMED", "MARGINAL", 0.2, 0.31)})
        self.assertFalse(c["all_labels_same"])
        self.assertEqual(c["tests"][0]["flag"], "coding-sensitive")


# =========================================================================== lock, pins, refusals
class TestLockAndPins(unittest.TestCase):
    def test_lock_holds(self):
        r = S.mq_lock(ROOT)
        self.assertTrue(r["ok"], r["why"])
        self.assertEqual(r["commit"], S.PREREG_COMMIT)

    def test_manifest_lists_the_five_locked_files(self):
        ent = S.manifest_entries((ROOT / S.MANIFEST_REL).read_text(encoding="utf-8"))
        self.assertEqual(len(ent), 5)
        self.assertNotIn("osf/aias_3_0/scripts/score_aias_3_0.py", [f for _h, f in ent])

    def test_append_only_deviations(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            locked = (ROOT / S.DEVIATIONS_REL).read_bytes()
            for _h, f in S.manifest_entries((ROOT / S.MANIFEST_REL).read_text(encoding="utf-8")):
                (tmp / f).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / f, tmp / f)
            (tmp / S.MANIFEST_REL).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / S.MANIFEST_REL, tmp / S.MANIFEST_REL)
            real_show = S._git_show
            with mock.patch.object(S, "_git_show", lambda root, ref, path: real_show(ROOT, ref, path)):
                self.assertEqual(S.verify_manifest(tmp), [])
                (tmp / S.DEVIATIONS_REL).write_bytes(locked + b"\n## Entry 1 (ex post)\nappended\n")
                self.assertEqual(S.verify_manifest(tmp), [])
                (tmp / S.DEVIATIONS_REL).write_bytes(locked.replace(b"Entry 0", b"Entry O"))
                self.assertTrue(any("DEVIATIONS" in x for x in S.verify_manifest(tmp)))
                p = tmp / "osf/aias_3_0/prereg/precision_aias_3_0.json"
                (tmp / S.DEVIATIONS_REL).write_bytes(locked)
                p.write_bytes(p.read_bytes() + b" ")
                self.assertTrue(any("precision_aias_3_0.json" in x for x in S.verify_manifest(tmp)))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_scorer_is_the_locked_file(self):
        r = S.check_scorer(ROOT)
        self.assertTrue(r["passed"], r)

    def test_pins_resolve(self):
        r = S.pin_report(ROOT)
        self.assertEqual(r["problems"], [])

    def test_run_refuses_without_sq_outputs(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            with mock.patch.object(S, "load_world", side_effect=AssertionError("no data may be read")):
                with self.assertRaises(S.Refused):
                    S.run("calibration", ROOT, sq_ref=None, out_dir=tmp, log=lambda *_: None)
            self.assertEqual(list(tmp.iterdir()), [])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_run_refuses_to_overwrite(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            (tmp / S.OUT_NAMES["dissociation"]).write_text("{}")
            with self.assertRaises(S.Refused):
                S.run("dissociation", ROOT, sq_ref="HEAD", out_dir=tmp, log=lambda *_: None)
            (tmp / S.OUT_NAMES["dissociation"]).unlink()
            (tmp / S.OUT_NAMES["inputs"]).write_text(json.dumps({"dissociation": {}}))
            with self.assertRaises(S.Refused):
                S.run("dissociation", ROOT, sq_ref="HEAD", out_dir=tmp, log=lambda *_: None)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_mq_sq(self):
        ok = {"reproduction": {"coded_cells_differ": 0, "v112_verdict_leaves_differ": 0,
                               "v112_unit_table_cells_differ": 0, "v119_verdict_leaves_differ": 0}}
        self.assertTrue(S.mq_sq(ok)["ok"])
        self.assertFalse(S.mq_sq(None)["ok"])
        bad = json.loads(json.dumps(ok))
        bad["reproduction"]["v119_verdict_leaves_differ"] = None
        self.assertFalse(S.mq_sq(bad)["ok"])

    def test_mq_blind_no_outputs_yet(self):
        r = S.mq_blind(ROOT)
        self.assertTrue(r["ok"], r)

    def test_cli_refusals(self):
        r = subprocess.run([PY, str(SCORER), "--calibration", "--draws", "10"], capture_output=True, text=True,
                           env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        self.assertEqual(r.returncode, 3, r.stderr)
        r = subprocess.run([PY, str(SCORER), "--verify-lock"], capture_output=True, text=True,
                           env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        self.assertEqual(r.returncode, 0, r.stderr)


# =========================================================================== end to end through v1.12's own pipeline
def _v112_helpers():
    if str(V112_TESTS) not in sys.path:
        sys.path.insert(0, str(V112_TESTS))
    import test_pipeline_v1_12 as TP   # noqa: E402  (v1.12's synthetic generators; locked test file, imported unchanged)
    return TP


class TestEndToEndV112(unittest.TestCase):
    """Coverage-shaped raw answers and t4-shaped tables (v1.12's own synthetic generators) -> v1.12's scorer ->
    a unit table and a verdict file -> this scorer: parity, calibration and dissociation. Synthetic only."""

    @classmethod
    def setUpClass(cls):
        TP = _v112_helpers()
        cls.inp = TP.inputs(21)
        cls.doc, cls.rows = A.score_coverage(cls.inp, A.Cfg(30, 30), {"enforce": False}, with_sensitivities=False)
        cls.tmp = Path(tempfile.mkdtemp(prefix="aias30_e2e_"))
        A.write_outputs(cls.doc, cls.rows, cls.tmp / "v112_verdicts.json", cls.tmp / "v112_unit_table.csv")
        cls.table = A.read_csv_rows(cls.tmp / "v112_unit_table.csv")            # as the real run reads it (strings)
        cls.vdoc = json.loads((cls.tmp / "v112_verdicts.json").read_text(encoding="utf-8"))
        cls.world = S.world_from_rows(cls.table)
        cls.world["tabs"] = S.v112_tables(cls.inp["raw"], cls.inp["mentions"], cls.inp["probes"], cls.inp["registry"])
        t4 = cls.inp["t4"]
        cls.comp = A.comparators_t4(t4["brand_table"], t4["coded_a"], t4["coded_b"], t4["excluded"])

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_parity_passes(self):
        par = S.mq_parity(self.world, self.comp, self.world["tabs"], self.vdoc)
        self.assertTrue(par["passed"], par["mismatches"])
        self.assertTrue(par["rho"]["H1_Sep_Presence"]["equal"])
        self.assertTrue(par["rho"]["H2_Sep_Consistency"]["equal"])
        self.assertEqual(par["rated_112"], sum(1 for r in self.table if r["rated"] == "1"))

    def test_parity_halts_on_a_changed_value(self):
        w = dict(self.world, P=dict(self.world["P"]))
        u = next(k for k, v in w["P"].items() if S._f(v))
        w["P"][u] += 1e-6
        self.assertFalse(S.mq_parity(w, self.comp, self.world["tabs"], self.vdoc)["passed"])
        w = dict(self.world, Cov=dict(self.world["Cov"]))
        u = next(k for k, v in w["Cov"].items() if S._f(v))
        w["Cov"][u] = None
        self.assertFalse(S.mq_parity(w, self.comp, self.world["tabs"], self.vdoc)["passed"])

    def test_join(self):
        reg = [(s, b) for s in self.inp["registry"] for b in self.inp["registry"][s]]
        P_t3, _C = A.legacy_t3(self.inp["profiles"])
        self.assertTrue(S.mq_join(self.world, reg, P_t3)["passed"])
        bad = dict(self.world, units=self.world["units"][:-1])
        self.assertFalse(S.mq_join(bad, reg, P_t3)["passed"])

    def test_dissociation_carries_h2_on_its_own_set(self):
        par = S.mq_parity(self.world, self.comp, self.world["tabs"], self.vdoc)
        d = S.dissociation_doc(self.world, par["carried_h2"], {"status": "not issued", "G3": None}, None, 30, 30)
        cc = d["pairs"]["C_Cov"]
        if cc["U3_equals_v112_H2_set"]:
            self.assertEqual(cc["verdict"], self.vdoc["legs"]["H2_Sep_Consistency"]["verdict"])
            self.assertAlmostEqual(cc["rho_w"], self.vdoc["legs"]["H2_Sep_Consistency"]["rho_w"], places=12)
        self.assertEqual(d["U3"]["n"], len(S.u3_units(self.world["P"], self.world["C"], self.world["Cov"])))
        self.assertIn(d["verdicts"]["H3_Cov_Joint"], {"CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED"})
        self.assertIn(d["class"]["class"], {"A", "B", "C", "U"})

    def test_calibration_on_the_v112_tables(self):
        cal = S.calibration(self.world)
        self.assertEqual(cal["candidates"], 8)
        floor_row = cal["table"][0]
        self.assertEqual(floor_row["candidate"], "ADD3 | Cov* | FLOOR")
        self.assertEqual(floor_row["n_cov_rated"], sum(1 for r in self.table if r["rated"] == "1"))
        # the FLOOR half scores equal v1.12's own H4 halves
        ha = S.cov_from_table(self.world["tabs"]["A"], self.world["units"], "Cov*", "FLOOR", S.HALF_FLOOR)
        for r in self.table:
            u = (r["substrate"], r["brand"])
            self.assertTrue(S._same(ha[u], A._num(r["cov_star_A"]), 1e-9), u)
        self.assertIn(cal["composite"]["verdict"], {"NO COMPOSITE", "CANDIDATE COMPOSITE"})


class TestDryRunCLI(unittest.TestCase):
    def test_dry_run(self):
        tmp = Path(tempfile.mkdtemp(prefix="aias30_dry_"))
        try:
            r = subprocess.run([PY, str(SCORER), "--dry-run", str(tmp), "--draws", "25"], capture_output=True, text=True,
                               env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"), timeout=300)
            self.assertEqual(r.returncode, 0, r.stderr[-2000:])
            for n in ("calibration", "dissociation", "profile"):
                self.assertTrue((tmp / S.OUT_NAMES[n]).exists(), n)
            d = json.loads((tmp / S.OUT_NAMES["dissociation"]).read_text(encoding="utf-8"))
            self.assertIn("synthetic", d["DRY_RUN"])
            self.assertIn("SQ", d)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
