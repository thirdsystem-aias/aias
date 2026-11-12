"""Tests for v1.17. Real-data tests check counts and the one published number only (no estimand on real data)."""
import json
import math
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import v1_17_lib as L          # noqa: E402
import analyze_v1_17 as A      # noqa: E402


class TestEstimators(unittest.TestCase):
    def test_unit_var_and_pooled(self):
        P = np.array([[0, 1 / 6, 2 / 6], [0.5, 0.5, 0.5]])
        s2 = L.unit_var(P)
        self.assertAlmostEqual(s2[0], 1 / 36)
        self.assertEqual(s2[1], 0.0)
        self.assertAlmostEqual(L.pooled_var(s2), 1 / 72)

    def test_runs_needed(self):
        self.assertEqual(L.runs_needed(0.0, 0.10), 1)
        self.assertEqual(L.runs_needed(0.04, 0.10), 5)      # SE(4) = 0.10 exactly is not below 0.10
        self.assertEqual(L.runs_needed(0.039, 0.10), 4)
        self.assertEqual(L.runs_needed(0.0225, 0.05), 10)   # SE(9) = 0.05 exactly -> 10
        for v in (0.003, 0.02, 0.05):
            for tau in L.TAUS:
                R = L.runs_needed(v, tau)
                self.assertLess(math.sqrt(v / R), tau)
                if R > 1:
                    self.assertGreaterEqual(math.sqrt(v / (R - 1)), tau)
        self.assertIsNone(L.runs_needed(float("nan"), 0.1))

    def test_se_projection_under_independence(self):
        rng = np.random.default_rng(1)
        x = rng.binomial(6, 0.4, size=(200_000, 24)) / 6
        sigma2 = 0.4 * 0.6 / 6
        for R in (1, 3, 7, 24):
            emp = x[:, :R].mean(axis=1).std()
            self.assertAlmostEqual(emp, L.se_at(sigma2, R), delta=0.01 * L.se_at(sigma2, R) + 1e-4)

    def test_chi2_interval_brackets(self):
        lo, hi = L.chi2_interval(0.02, 100)
        self.assertLess(lo, 0.02)
        self.assertGreater(hi, 0.02)

    def test_cluster_bootstrap_deterministic_and_brackets(self):
        rng = np.random.default_rng(2)
        s2 = rng.random(300) * 0.05
        cl = np.repeat(np.arange(30), 10).astype(str)
        a = L.cluster_bootstrap_var(s2, cl, 2000, 5)
        b = L.cluster_bootstrap_var(s2, cl, 2000, 5)
        self.assertEqual(a, b)
        self.assertLess(a[0], s2.mean())
        self.assertGreater(a[1], s2.mean())
        self.assertEqual(a[2], 30)
        one = L.cluster_bootstrap_var(s2[:10], cl[:10], 500, 5)
        self.assertAlmostEqual(one[0], one[1])            # one cluster: degenerate interval

    def test_bands(self):
        self.assertEqual(L.band_of(0, 18), "zero")
        self.assertEqual(L.band_of(18, 18), "full")
        self.assertEqual(L.band_of(5, 18), "low")
        self.assertEqual(L.band_of(6, 18), "middle")
        self.assertEqual(L.band_of(12, 18), "middle")
        self.assertEqual(L.band_of(13, 18), "high")

    def test_discordance(self):
        nb, nd, npairs = L.discordance([3, 2, 1], [1, 2, 3])
        self.assertEqual((nb, nd, npairs), (3, 3, 3))
        self.assertEqual(L.discordance([1, 1, 2], [1, 2, 3])[:2], (0, 0))   # tie -> strict is not a reversal
        self.assertEqual(L.discordance([2, 1, 0], [2, 1, 1])[:2], (0, 0))
        self.assertEqual(L.discordance([1, 2, 0], [2, 1, 0])[:2], (2, 1))

    def test_floor_integer_rule(self):
        self.assertTrue(L.below_floor(8, 54))
        self.assertFalse(L.below_floor(9, 54))             # 6 * 9/54 = 1 exactly: not below
        self.assertTrue(L.below_floor(2, 18))
        self.assertFalse(L.below_floor(3, 18))


class TestSynthetic(unittest.TestCase):
    def test_recovers_known_variance(self):
        for sc in ("A", "B"):
            t, truth = A.make_synthetic(42, sc, n_runs=40)
            s2 = L.unit_var(L.per_run(t))
            self.assertAlmostEqual(L.pooled_var(s2), truth["all"], delta=0.05 * truth["all"])

    def test_analysis_runs_end_to_end(self):
        t, truth = A.make_synthetic(7, "A")
        res = A.analyse_t4(t, coi_keys=(("v0.19", "B00"),), n_boot=200)
        self.assertEqual(res["n_units"], 672)
        self.assertIn("size_16", res["primary"])
        self.assertTrue(res["primary"]["size_16"]["few_clusters_flag"])
        self.assertFalse(res["primary"]["all"]["few_clusters_flag"])
        self.assertEqual(res["alongside"]["S_COI_all"]["n_units"], 672 - 6)
        ovt = res["once_vs_three"]["published_floor_N3"]["S0"]
        self.assertEqual(ovt["n_brands"], 112)

    def test_charts_and_note_on_synthetic(self):
        import build_charts_v1_17 as BC
        import write_note_v1_17 as WN
        t, _ = A.make_synthetic(11, "B")
        res = {"t4": A.analyse_t4(t, coi_keys=(("v0.19", "B00"),), n_boot=200),
               "omnibus": A.analyse_omni(A.make_synthetic_omni(11), coi_keys=(), n_boot=200)}
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "r.json"
            src.write_text(json.dumps(res))
            BC.main([str(src), d, "--synthetic"])
            self.assertEqual(len(list(Path(d).glob("chart_0*.png"))), 4)
            WN.main([str(src), str(Path(d) / "n.md"), "--v040-runs", "3", "--v040-brands", "20",
                     "--v040-questions", "8", "--synthetic"])
            txt = (Path(d) / "n.md").read_text()
            self.assertIn("SYNTHETIC", txt)
            self.assertIn("assuming independent runs", txt)
            self.assertNotIn("nan", txt.lower().replace("panel", ""))

    def test_separate_waves_never_pooled(self):
        o = L.Omni(np.array([[0, 0.5, 1.0], [0.5, 0.5, 0.5]]), [("v0.19", "a", "m"), ("v0.19", "b", "m")])
        res = A.analyse_omni(o, coi_keys=(), n_boot=50)
        self.assertNotIn("R_needed_se_below_0.10", res["strata"]["all"])
        self.assertAlmostEqual(res["strata"]["all"]["pooled_var"], 0.125)


class TestRealDataLoaders(unittest.TestCase):
    """Counts per cell and the one published number; nothing estimated."""

    @classmethod
    def setUpClass(cls):
        cls.t4 = L.load_t4()
        cls.o = L.load_omni()

    def test_t4_counts(self):
        self.assertEqual(self.t4.n_rows, 12096)
        self.assertEqual(len(self.t4.units), 672)
        self.assertEqual(self.t4.X.shape, (672, 3, 6))
        self.assertFalse(np.isnan(self.t4.X).any())
        self.assertEqual(sorted(set(self.t4.size.tolist())), [16, 24])
        self.assertEqual(int((self.t4.size == 16).sum()), 96)
        self.assertEqual(len(set(self.t4.cluster.tolist())), 30)

    def test_omni_counts(self):
        self.assertEqual(len(self.o.units), 672)
        self.assertEqual(self.o.W.shape, (672, 3))
        self.assertEqual(self.o.max_pi_hat_abs_diff, 0.0)

    def test_coi_mapping(self):
        keys = L.coi_brand_keys()
        self.assertIn(("v0.23", "S03"), keys)
        present = sum(1 for c, b in keys if ((self.t4.cat == c) & (self.t4.brand == b)).any())
        self.assertEqual(present, 6)

    def test_published_floor_reproduced(self):
        with open(L.T4_VERDICTS, encoding="utf-8") as fh:
            pub = json.load(fh)["descriptives"]["3_floor_persistence"]["below_floor_t4"]
        self.assertEqual(L.published_floor_count(self.t4, "S0"), pub)
        self.assertEqual(pub, 49)


class TestGates(unittest.TestCase):
    def test_manifest_detects_change(self):
        with tempfile.TemporaryDirectory(dir=L.V117) as d:
            f = Path(d) / "x.txt"
            f.write_text("a")
            rel = f.relative_to(L.ROOT)
            m = Path(d) / "m.sha256"
            m.write_text(f"# draft\n{L.sha256(f)}  {rel}\n")
            self.assertEqual(A.manifest_problems(m), [])
            f.write_text("b")
            self.assertEqual(A.manifest_problems(m), [f"changed {rel}"])

    def test_run_refuses_before_anchor(self):
        if A.tag_on_origin():
            self.skipTest("tag already on origin")
        self.assertEqual(A.main(["--run"]), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
