#!/usr/bin/env python3
"""Synthetic-data tests for score_aias_6_0_preview.py (AIAS 6.0 Preview, r0 skeleton).
No program data are read. Run: python3 -I osf/aias_6_0_preview/scripts/tests/test_score_aias_6_0_preview.py
"""
import hashlib
import math
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))
import score_aias_6_0_preview as S  # noqa: E402

R = S.R
V110_BLOB = "0f8b981b2895a325b50629c85f8e0e6ce8e876f5"   # scripts/score_v1_10.py at tag v1.10-prereg-r2


def git_blob(path: Path) -> str:
    b = path.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def units(n_per=(16, 24, 24, 24, 24)):
    return [(f"c{i}", f"b{j:02d}") for i, n in enumerate(n_per) for j in range(n)]


class TestBandsAndFloors(unittest.TestCase):
    def test_band_edges(self):
        self.assertEqual(S.band(0.30, True), "CONFIRMED")
        self.assertEqual(S.band(-0.30, True), "CONFIRMED")
        self.assertEqual(S.band(0.3000001, True), "MARGINAL")
        self.assertEqual(S.band(0.4999999, True), "MARGINAL")
        self.assertEqual(S.band(0.50, True), "FALSIFIED")
        self.assertEqual(S.band(-0.7, True), "FALSIFIED")
        self.assertEqual(S.band(float("nan"), True), "UNDETERMINED")
        self.assertEqual(S.band(0.1, False), "UNDETERMINED")

    def test_floor(self):
        self.assertEqual(S.floor_ok(["a"] * 10 + ["b"] * 10 + ["c"] * 10), (True, 30, 3))
        self.assertFalse(S.floor_ok(["a"] * 10 + ["b"] * 10 + ["c"] * 9)[0])      # 29 units
        self.assertFalse(S.floor_ok(["a"] * 20 + ["b"] * 20)[0])                    # 2 categories
        ok, n, c = S.floor_ok(["a"] * 15 + ["b"] * 15 + ["c"] * 4 + ["d"] * 6)      # c dropped (< 5)
        self.assertEqual((ok, n, c), (True, 36, 3))


class TestSTest(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(1)
        self.scores = {u: {"P": float(rng.normal()), "C": float(rng.normal())} for u in units()}

    def test_matches_v1_10_pooled_within_rho(self):
        res = S.s_test(self.scores, "P", "C", n_perm=0, boot=False)
        keys = sorted(self.scores)
        x = np.array([self.scores[u]["P"] for u in keys])
        y = np.array([self.scores[u]["C"] for u in keys])
        g = np.array([u[0] for u in keys])
        self.assertEqual(res["rho"], R.pooled_within_rho(x, y, g))
        self.assertEqual(res["n"], 112)
        self.assertEqual(res["categories"], 5)

    def test_monotone_within_category_falsified(self):
        sc = {u: {"P": float(i), "C": float(2 * i + 1)} for i, u in enumerate(units())}
        res = S.s_test(sc, "C", "P", n_perm=0, boot=False)
        self.assertAlmostEqual(res["rho"], 1.0)
        self.assertEqual(res["verdict"], "FALSIFIED")
        self.assertEqual(res["pair"], ["P", "C"])                                   # programme order

    def test_not_rated_units_leave_the_pair(self):
        sc = {u: dict(v) for u, v in self.scores.items()}
        for u in list(sc)[:90]:
            sc[u]["C"] = None
        res = S.s_test(sc, "P", "C", n_perm=0, boot=False)
        self.assertEqual(res["verdict"], "UNDETERMINED")                            # 22 units

    def test_carry_and_parity(self):
        own = S.s_test(self.scores, "P", "C", n_perm=0, boot=False)
        out = S.carry(own, {"rho": own["rho"], "verdict": "MARGINAL", "source": "v1.14 H1"})
        self.assertEqual((out["verdict"], out["source"]), ("MARGINAL", "v1.14 H1"))
        with self.assertRaises(S.Halt):
            S.carry(own, {"rho": own["rho"] + 1e-6, "verdict": "CONFIRMED", "source": "x"})


class TestITest(unittest.TestCase):
    def test_formula(self):
        rng = np.random.default_rng(2)
        sc = {u: {"P": float(rng.normal()), "C": float(rng.normal()), "R": float(rng.normal())}
              for u in units()}
        keys = sorted(sc)
        res = S.i_test(sc, keys, "R", ["P", "C"], n_perm=0)
        g = np.array([u[0] for u in keys])
        cols = [R.within_ranks(np.array([sc[u][m] for u in keys]), g) for m in ("R", "P", "C")]
        X = np.column_stack(cols[1:])
        beta, *_ = np.linalg.lstsq(X, cols[0], rcond=None)
        r2 = 1 - ((cols[0] - X @ beta) ** 2).sum() / (cols[0] ** 2).sum()
        r2a = 1 - (1 - r2) * (112 - 5) / (112 - 5 - 2)
        self.assertAlmostEqual(res["R2"], r2, places=12)
        self.assertAlmostEqual(res["R2_adj"], r2a, places=12)
        self.assertAlmostEqual(res["R_adj"], math.sqrt(max(0, r2a)), places=12)

    def test_catches_a_combination_the_pairs_miss(self):
        rng = np.random.default_rng(3)
        sc = {}
        for u in units():
            a = rng.normal()
            b = 0.95 * a + math.sqrt(1 - 0.95 ** 2) * rng.normal()
            sc[u] = {"P": a, "C": b, "R": a - b}
        s_pr = S.s_test(sc, "P", "R", n_perm=0, boot=False)
        s_cr = S.s_test(sc, "C", "R", n_perm=0, boot=False)
        self.assertNotEqual(s_pr["verdict"], "FALSIFIED")
        self.assertNotEqual(s_cr["verdict"], "FALSIFIED")
        res = S.i_test(sc, sorted(sc), "R", ["P", "C"], n_perm=200)
        self.assertEqual(res["verdict"], "FALSIFIED")
        self.assertLess(res["p_perm"], 0.01)

    def test_below_floor_undetermined(self):
        sc = {u: {"P": 1.0 * i, "C": 0.5 * i} for i, u in enumerate(units((6, 6, 6, 6, 5)))}
        self.assertEqual(S.i_test(sc, sorted(sc), "C", ["P"], n_perm=0)["verdict"], "UNDETERMINED")

    def test_incremental_set_ignores_later_members(self):
        sc = {u: {"P": 1.0, "C": 1.0, "R": 1.0, "G": None} for u in units()}
        keys, preds = S.incremental_set(sc, ["P", "C", "R", "G"], "R")
        self.assertEqual((len(keys), preds), (112, ["P", "C"]))
        self.assertEqual(len(S.complete_profile(sc, ["P", "C", "R", "G"])), 0)


class TestStatusAndStructure(unittest.TestCase):
    @staticmethod
    def sres(K, override=None):
        out = {}
        for i, a in enumerate(K):
            for b in K[i + 1:]:
                out[S.pair_key(a, b)] = {"verdict": "CONFIRMED"}
        for k, v in (override or {}).items():
            out[S.pair_key(*k)] = {"verdict": v}
        return out

    def test_component_status(self):
        K = ["P", "C", "R", "Cov"]
        ires = {m: {"verdict": "CONFIRMED"} for m in K[1:]}
        st = lambda x, s, i=ires: S.component_status(x, K, s, i)  # noqa: E731
        self.assertEqual(st("R", self.sres(K)), S.DISTINCT)
        self.assertEqual(st("R", self.sres(K, {("C", "R"): "MARGINAL"})), S.PARTLY)
        s_f = self.sres(K, {("R", "Cov"): "FALSIFIED"})
        self.assertEqual(st("Cov", s_f), S.NOT_DISTINCT)        # the later member is marked
        self.assertEqual(st("R", s_f), S.DISTINCT)              # the earlier one keeps its place
        i_u = dict(ires, R={"verdict": "UNDETERMINED"})
        self.assertEqual(st("R", self.sres(K), i_u), "UNDETERMINED")
        i_f = dict(ires, R={"verdict": "FALSIFIED"})
        self.assertEqual(st("R", self.sres(K, {("P", "R"): "UNDETERMINED"}), i_f), S.NOT_DISTINCT)
        self.assertEqual(st("P", self.sres(K, {("P", "C"): "FALSIFIED"})), S.DISTINCT)   # anchor

    def test_h_structure(self):
        K6 = S.ORDER
        allD = {m: S.DISTINCT for m in K6}
        self.assertEqual(S.h_structure(K6, allD)["verdict"], "CONFIRMED")
        self.assertEqual(S.h_structure(K6, dict(allD, G=S.PARTLY))["verdict"], "PARTIAL")
        self.assertEqual(S.h_structure(K6, dict(allD, G=S.NOT_DISTINCT))["verdict"], "PARTIAL")
        four_not = dict(allD, R=S.NOT_DISTINCT, S=S.NOT_DISTINCT, Cov=S.NOT_DISTINCT, G=S.NOT_DISTINCT)
        self.assertEqual(S.h_structure(K6, four_not)["verdict"], "FALSIFIED")            # d = 2
        self.assertEqual(S.h_structure(K6, dict(four_not, G="UNDETERMINED"))["verdict"], "PARTIAL")
        self.assertEqual(S.h_structure(["P", "C"], {"P": S.DISTINCT, "C": S.DISTINCT})["verdict"],
                         "UNDETERMINED")                                                   # k < 3
        three_u = dict(allD, C="UNDETERMINED", R="UNDETERMINED", S="UNDETERMINED", Cov="UNDETERMINED")
        self.assertEqual(S.h_structure(K6, three_u)["verdict"], "UNDETERMINED")          # k - u < 3
        self.assertEqual(S.h_structure(K6, allD, panel_ok=False)["verdict"], "UNDETERMINED")

    def test_wording_class(self):
        self.assertEqual(S.wording_class("CONFIRMED", 6), "A")
        self.assertEqual(S.wording_class("CONFIRMED", 5), "A_k")
        self.assertEqual(S.wording_class("PARTIAL", 6), "B")
        self.assertEqual(S.wording_class("FALSIFIED", 4), "C")
        self.assertEqual(S.wording_class("UNDETERMINED", 6), "U")


class TestGates(unittest.TestCase):
    def test_ranking(self):
        self.assertEqual(S.gate_ranking("PASS", "SEPARABLE (Stage 2 pending)"), S.PASS)
        self.assertEqual(S.gate_ranking(None, "SEPARABLE (Stage 2 pending)"), S.PASS_RETEST)
        self.assertEqual(S.gate_ranking(None, "MARGINAL"), S.MARGINAL)
        self.assertEqual(S.gate_ranking("FAIL", "SEPARABLE (Stage 2 pending)"), S.FAIL)
        self.assertEqual(S.gate_ranking(None, None), S.NOT_RUN)

    def test_sentiment(self):
        ok = {k: "CONFIRMED" for k in ("H1_Judge_Agreement", "H2_Sep_Presence", "H3_Sep_Consistency",
                                        "H4_Stability_Short", "H5_Sep_Ranking")}
        self.assertEqual(S.gate_sentiment(ok, True), S.PASS_AI)
        self.assertEqual(S.gate_sentiment(ok, True, "PASS"), S.PASS)
        self.assertEqual(S.gate_sentiment(ok, True, "FAIL"), S.FAIL)
        self.assertEqual(S.gate_sentiment(dict(ok, H5_Sep_Ranking="PENDING"), True), S.PASS_AI)
        self.assertEqual(S.gate_sentiment(dict(ok, H2_Sep_Presence="FALSIFIED"), True), S.FAIL)
        self.assertEqual(S.gate_sentiment(dict(ok, H4_Stability_Short="UNDETERMINED"), True), S.UNDET)
        self.assertEqual(S.gate_sentiment(dict(ok, H1_Judge_Agreement="MARGINAL"), True), S.MARGINAL)
        self.assertEqual(S.gate_sentiment(ok, False), S.NOT_RUN)                         # no S_t4

    def test_component_and_inclusion(self):
        self.assertEqual(S.gate_component("INSTRUMENT FAIL"), S.FAIL)
        self.assertEqual(S.gate_component(None), S.NOT_RUN)
        states = {"R": S.MARGINAL, "S": S.NOT_RUN, "Cov": S.PASS, "G": S.FAIL}
        self.assertEqual(S.included_set(states), ["P", "C", "Cov"])
        self.assertEqual(S.included_set({"R": S.PASS_RETEST, "S": S.PASS_AI}), ["P", "C", "R", "S"])


class TestEndToEndSynthetic(unittest.TestCase):
    ALL = {"R": S.PASS_RETEST, "S": S.PASS_AI, "Cov": S.PASS, "G": S.PASS}

    def test_independent_parts_confirmed(self):
        sc, men = S.synthetic(seed=600999)
        res = S.structure(sc, self.ALL, mentions=men, n_perm=200, boot=False)
        self.assertEqual(res["H_Structure"]["verdict"], "CONFIRMED")
        self.assertEqual(res["wording_class"], "A")
        self.assertFalse(res["composite_check"]["adopted"])

    def test_planted_overlap_marks_the_later_part(self):
        sc, men = S.synthetic(seed=600999, overlap={"Cov": ("P", 0.9)})
        res = S.structure(sc, self.ALL, mentions=men, n_perm=200, boot=False)
        self.assertEqual(res["S_tests"]["PxCov"]["verdict"], "FALSIFIED")
        self.assertEqual(res["status"]["Cov"], S.NOT_DISTINCT)
        self.assertEqual(res["status"]["P"], S.DISTINCT)
        self.assertEqual(res["H_Structure"]["verdict"], "PARTIAL")

    def test_copies_of_presence_falsified(self):
        ov = {m: ("P", 0.95) for m in ("R", "S", "Cov", "G")}
        sc, men = S.synthetic(seed=600999, overlap=ov)
        res = S.structure(sc, self.ALL, mentions=men, n_perm=200, boot=False)
        self.assertEqual(res["H_Structure"]["verdict"], "FALSIFIED")
        self.assertEqual(res["wording_class"], "C")

    def test_marginal_part_outside_k_and_descriptive(self):
        sc, men = S.synthetic(seed=600999)
        res = S.structure(sc, dict(self.ALL, G=S.MARGINAL), n_perm=0, boot=False)
        self.assertNotIn("G", res["K"])
        self.assertIn("PxG", res["descriptive_marginal_pairs"])
        self.assertEqual(res["labels"]["G"], "under review")

    def test_panel_incomplete(self):
        sc, _ = S.synthetic(seed=600999)
        res = S.structure(sc, self.ALL, panel_ok=False, n_perm=0, boot=False)
        self.assertEqual((res["H_Structure"]["verdict"], res["wording_class"]), ("UNDETERMINED", "U"))

    def test_deterministic(self):
        sc, men = S.synthetic(seed=600999)
        a = S.structure(sc, self.ALL, mentions=men, n_perm=100, boot=False)
        b = S.structure(sc, self.ALL, mentions=men, n_perm=100, boot=False)
        self.assertEqual(repr(a), repr(b))

    def test_composite_equals_presence_when_nothing_else_rated(self):
        sc = {u: {"P": float(i), "C": None} for i, u in enumerate(units())}
        cc = S.composite_check(sc, ["P", "C"], {u: 0 for u in sc})
        self.assertAlmostEqual(cc["rho_A_P"], 1.0)
        self.assertFalse(cc["K2_passes"])


class TestCliAndLocks(unittest.TestCase):
    def test_run_refuses_in_r0(self):
        self.assertEqual(S.main(["--run"]), 2)

    def test_dry_run_writes_only_to_out(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(S.main(["--dry-run", "--out", d, "--n-perm", "50"]), 0)
            self.assertTrue((Path(d) / "dry_run_aias_6_0_preview.json").exists())

    def test_imported_v1_10_is_the_locked_file(self):
        self.assertEqual(git_blob(Path(R.__file__)), V110_BLOB)


if __name__ == "__main__":
    unittest.main(verbosity=1)
