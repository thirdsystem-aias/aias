#!/usr/bin/env python3
"""
Unit tests for score_v1_12.py (v1.12 Coverage Paper A, scorer core). Synthetic data only: no v1.12 or t4
answer is read and no API is called. Run from the repository root:

    python3 -m unittest discover -s osf/methodology/v1_12/scripts/tests -p "test_*.py" -v
"""
import ast
import itertools
import math
import sys
import unittest
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import score_v1_12 as S   # noqa: E402

V41 = S.ROOT / "osf/v41/scripts/score_v41.py"


def load_v41_helpers():
    """The four rho helpers of the v0.41 scorer, compiled from its source (the module itself is not imported:
    its import re-executes the entry script under a HOME shim)."""
    tree = ast.parse(V41.read_text(encoding="utf-8"))
    want = {"_pearson", "within_ranks", "pooled_within_rho", "_group_index"}
    defs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in want]
    ns = {"np": np, "stats": stats}
    exec(compile(ast.Module(body=defs, type_ignores=[]), str(V41), "exec"), ns)
    return ns


def rand_groups(rng, sizes):
    return np.array([f"c{i}" for i, n in enumerate(sizes) for _ in range(n)])


def complete_slots(n_ceps=14, runs=3):
    return np.repeat(np.arange(n_ceps), runs)


class TestRhoW(unittest.TestCase):
    def test_pooled_within_rho_equals_v041_scorer(self):
        v41 = load_v41_helpers()
        rng = np.random.default_rng(1)
        for _ in range(200):
            g = rand_groups(rng, [16, 24, 24, 24, 24])
            x = rng.integers(0, 6, len(g)).astype(float)          # ties
            y = rng.normal(size=len(g))
            self.assertEqual(S.pooled_within_rho(x, y, g), v41["pooled_within_rho"](x, y, g))
            self.assertEqual(S.rho_w(x, y, g, centred=False), v41["pooled_within_rho"](x, y, g))   # S9
            np.testing.assert_array_equal(S.within_ranks(x, g), v41["within_ranks"](x, g))

    def test_within_category_ranks(self):
        rng = np.random.default_rng(2)
        g = rand_groups(rng, [10, 10, 10])
        x, y = rng.normal(size=30), rng.normal(size=30)
        shift = np.array([{"c0": 0, "c1": 100, "c2": -50}[c] for c in g])
        self.assertAlmostEqual(S.pooled_within_rho(x + shift, y, g), S.pooled_within_rho(x, y, g), places=12)
        self.assertNotAlmostEqual(S.spearman_brown_half(0.5), 0.5)
        self.assertAlmostEqual(S.rho_w(x + shift, y, g), S.rho_w(x, y, g), places=12)
        self.assertAlmostEqual(S.rho_w(x, y, g), S.rho_w(x, y, g, centred=False), places=12)   # equal sizes

    def test_centred_rho_unbiased_with_unequal_category_sizes(self):
        rng = np.random.default_rng(8)
        g = rand_groups(rng, [5, 40, 12])
        cen, unc = [], []
        for _ in range(3000):
            x, y = rng.normal(size=len(g)), rng.normal(size=len(g))
            cen.append(S.rho_w(x, y, g))
            unc.append(S.rho_w(x, y, g, centred=False))
        self.assertLess(abs(np.mean(cen)), 0.01)
        self.assertGreater(np.mean(unc), 0.2)              # the between-category component of S9
        np.testing.assert_allclose(S.centred_within_ranks(np.arange(5.0), np.zeros(5)), [-2, -1, 0, 1, 2])

    def test_paired_drops_small_categories_and_n_floor(self):
        xd, yd = {}, {}
        for c, n in (("v0.19", 4), ("v0.20", 10), ("v0.21", 10), ("v0.22", 12)):
            for i in range(n):
                xd[(c, f"b{i}")] = float(i)
                yd[(c, f"b{i}")] = float(i % 3)
        yd[("v0.22", "b0")] = float("nan")
        keys, x, y, g, info = S.paired(xd, yd)
        self.assertEqual(info["n"], 31)
        self.assertEqual(info["n_categories"], 3)
        self.assertEqual(info["dropped_categories"], {"v0.19": 4})
        self.assertFalse(S.below_n_floor(info))
        self.assertTrue(S.below_n_floor({"n": 29, "n_categories": 5}))
        self.assertTrue(S.below_n_floor({"n": 60, "n_categories": 2}))


class TestPermutationBootstrap(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(3)
        self.g = rand_groups(rng, [12, 12, 12])
        self.x = rng.normal(size=36)

    def test_perfect_correlation_p_is_minimal(self):
        r = S.pooled_within_rho(self.x, self.x, self.g)
        self.assertAlmostEqual(r, 1.0, places=12)
        self.assertEqual(S.perm_p(self.x, self.x, self.g, r, 7, "one", 499), 1 / 500)
        self.assertEqual(S.perm_p(self.x, -self.x, self.g, -r, 7, "two", 499), 1 / 500)

    def test_two_sided_is_sign_symmetric(self):
        y = np.random.default_rng(4).normal(size=36)
        r = S.pooled_within_rho(self.x, y, self.g)
        self.assertEqual(S.perm_p(self.x, y, self.g, r, 9, "two", 300),
                         S.perm_p(self.x, -y, self.g, -r, 9, "two", 300))

    def test_rank_permutation_equals_rerank(self):
        """N6: permuting within-category ranks of y == re-ranking a within-category permutation of y."""
        y = np.random.default_rng(5).integers(0, 4, 36).astype(float)
        rng1, rng2 = np.random.default_rng(11), np.random.default_rng(11)
        gidx = S._group_index(self.g)
        rx, ry = S.within_ranks(self.x, self.g), S.within_ranks(y, self.g)
        idx = np.arange(36)
        for _ in range(50):
            for gi in gidx:
                idx[gi] = rng1.permutation(gi)
            a = S._pearson(rx, ry[idx])
            yp = y.copy()
            for gi in gidx:
                yp[gi] = y[rng2.permutation(gi)]
            self.assertAlmostEqual(a, S.pooled_within_rho(self.x, yp, self.g), places=12)

    def test_null_p_values_are_spread(self):
        rng = np.random.default_rng(6)
        ps = []
        for i in range(60):
            y = rng.normal(size=36)
            ps.append(S.perm_p(self.x, y, self.g, S.pooled_within_rho(self.x, y, self.g), 100 + i, "two", 199))
        self.assertTrue(0.3 < np.mean(ps) < 0.7)
        self.assertTrue(all(0 < p <= 1 for p in ps))

    def test_bootstrap_reproducible_and_brackets_estimate(self):
        y = self.x + np.random.default_rng(7).normal(scale=0.5, size=36)
        f = lambda i: {"rho_w": S.pooled_within_rho(self.x[i], y[i], self.g[i])}   # noqa: E731
        b1, b2 = S.bootstrap(self.g, 112020, 300, f), S.bootstrap(self.g, 112020, 300, f)
        self.assertEqual(b1, b2)
        lo, hi = b1["rho_w"]["ci95"]
        self.assertTrue(lo <= S.pooled_within_rho(self.x, y, self.g) <= hi)

    def test_rho_test_fields(self):
        xd = {(c, f"b{i}"): float(i) for c in S.CATS for i in range(8)}
        yd = {k: v + (1 if k[1] == "b0" else 0) for k, v in xd.items()}
        t = S.rho_test(xd, yd, 112003, "two", n_perm=99, n_boot=99)
        self.assertEqual(t["n"], 40)
        self.assertFalse(t["below_n_floor"])
        self.assertGreater(t["rho_w"], 0.9)
        self.assertEqual(t["p_perm"], 1 / 100)
        self.assertEqual(len(t["ci95_rho_w"]), 2)
        h = S.rho_test(xd, yd, 112004, "one", n_perm=99, n_boot=99, transform=S.spearman_brown_half)
        self.assertAlmostEqual(h["transformed"], 2 * h["rho_w"] / (1 + h["rho_w"]), places=12)


class TestCoverageCore(unittest.TestCase):
    def test_c_min_c_max(self):
        full = [3] * 14
        for n in range(1, 43):
            self.assertEqual(S.c_min_of(full, n), math.ceil(n / 3))
            self.assertEqual(S.c_max_of(full, n), min(14, n))
        s = [3, 3, 2, 1, 0]
        self.assertEqual([S.c_min_of(s, n) for n in range(1, 10)], [1, 1, 1, 2, 2, 2, 3, 3, 4])
        self.assertEqual([S.c_max_of(s, n) for n in (1, 3, 4, 5, 9)], [1, 3, 4, 4, 4])
        with self.assertRaises(ValueError):
            S.c_min_of(s, 10)

    def test_e_equal_matches_enumeration(self):
        s = [2, 1, 3, 0, 2]
        slots = [j for j, k in enumerate(s) for _ in range(k)]
        for n in range(1, len(slots) + 1):
            combos = list(itertools.combinations(range(len(slots)), n))
            want = np.mean([len({slots[i] for i in c}) for c in combos])
            self.assertAlmostEqual(S.e_equal(s, n), want, places=12)

    def test_exact_distribution_agrees_with_closed_form(self):
        for r in S.exact_equal_weight_beta(14, 3):
            self.assertAlmostEqual(r["sum_p"], 1.0, places=9)
            self.assertAlmostEqual(r["E"], r["E_closed_form"], places=6)

    def test_null_pmf_rasch_matches_enumeration(self):
        s, d = [2, 1, 3, 0, 2], np.array([0.5, -0.3, 0.1, 0.0, 0.8])
        slots = [j for j, k in enumerate(s) for _ in range(k)]
        for n in range(1, len(slots) + 1):
            tot = {}
            for c in itertools.combinations(range(len(slots)), n):
                k = len({slots[i] for i in c})
                tot[k] = tot.get(k, 0.0) + math.exp(sum(d[slots[i]] for i in c))
            Z = sum(tot.values())
            pmf = S.null_pmf_rasch(s, d, n)
            for k, v in tot.items():
                self.assertAlmostEqual(pmf.get(k, 0.0), v / Z, places=12)
            eq = S.null_pmf_rasch(s, np.zeros(5), n)
            ref = S.null_pmf_equal(s, n)
            for k in set(eq) | set(ref):
                self.assertAlmostEqual(eq.get(k, 0.0), ref.get(k, 0.0), places=12)

    def test_null_pmf_rasch_extreme_delta_is_finite(self):
        pmf = S.null_pmf_rasch([3] * 14, np.linspace(-20, 20, 14), 30)
        self.assertAlmostEqual(sum(pmf.values()), 1.0, places=9)
        self.assertTrue(all(math.isfinite(v) and v >= 0 for v in pmf.values()))

    def test_conditional_bernoulli_null_does_not_depend_on_theta(self):
        slots = complete_slots()
        d = np.linspace(-1, 1, 14)
        rng = np.random.default_rng(17)
        pmf = S.null_pmf_rasch([3] * 14, d, 16)
        for theta in (-0.8, -0.2):
            q = S._expit(theta + d[slots])
            Y = rng.random((150000, 42)) < q
            Y = Y[Y.sum(1) == 16][:20000]
            self.assertGreater(len(Y), 3000)
            touched = np.array([len(set(slots[row])) for row in Y])
            for k, p in pmf.items():
                self.assertAlmostEqual(np.mean(touched == k), p, delta=0.02)

    def test_fit_delta_recovers_cep_effects(self):
        rng = np.random.default_rng(18)
        slots = complete_slots()
        d = rng.uniform(-1, 1, 14)
        theta = rng.uniform(-2, 2, 400)
        Y = (rng.random((42, 400)) < S._expit(theta[None, :] + d[slots][:, None])).astype(np.int8)
        deltas, status = S.rasch_deltas(slots, Y, 14)
        self.assertEqual(set(status), {"ok"})
        self.assertLess(np.abs(deltas[0] - (d - d.mean())).max(), 0.2)
        self.assertAlmostEqual(deltas[0].sum(), 0.0, places=9)

    def test_leave_b_out_and_uninformative_brands(self):
        rng = np.random.default_rng(19)
        slots = complete_slots()
        Y = (rng.random((42, 12)) < 0.4).astype(np.int8)
        d1, st1 = S.rasch_deltas(slots, Y, 14)
        Y2 = Y.copy()
        Y2[:, 3] = 1 - Y2[:, 3]                               # brand 3's own answers do not enter delta^(-3)
        d2, _ = S.rasch_deltas(slots, Y2, 14)
        np.testing.assert_allclose(d1[3], d2[3], atol=1e-8)
        Y3 = np.hstack([Y, np.zeros((42, 1), np.int8), np.ones((42, 1), np.int8)])
        d3, st3 = S.rasch_deltas(slots, Y3, 14)
        np.testing.assert_allclose(d3[3], d1[3], atol=1e-8)   # never / always named brands carry no information
        self.assertEqual(st3[:12], st1)

    def test_fit_failure_sets_delta_to_zero(self):
        rng = np.random.default_rng(20)
        slots = complete_slots()
        Y = (rng.random((42, 10)) < 0.5).astype(np.int8)
        Y[slots == 0, :] = 0                                  # no brand is ever named in CEP 0: separation
        deltas, status = S.rasch_deltas(slots, Y, 14)
        self.assertEqual(set(status), {"not_converged"})
        self.assertTrue(np.all(deltas == 0))
        _d, st = S.rasch_deltas(slots, np.zeros((42, 4), np.int8), 14)
        self.assertEqual(set(st), {"no_informative_brands"})

    def test_linear_beta_and_mid_p_zero_null_mean_with_cep_effects(self):
        d = np.random.default_rng(21).normal(0, 1, 14)
        for s in ([3] * 14, [3] * 10 + [2, 2, 1, 0]):
            for n in range(1, sum(s) + 1):
                pmf = S.null_pmf_rasch(s, d, n)
                E = sum(k * p for k, p in pmf.items())
                cmax, cmin = S.c_max_of(s, n), S.c_min_of(s, n)
                self.assertAlmostEqual(sum(p * S.beta_of(k, E, cmax, cmin) for k, p in pmf.items()), 0.0, places=9)
                self.assertAlmostEqual(sum(p * S.beta_mid(k, null_pmf=pmf) for k, p in pmf.items()), 0.0, places=9)

    def test_beta_of_cases(self):
        self.assertEqual(S.beta_of(5, 5.0, 8, 2), 0.0)
        self.assertEqual(S.beta_of(3, 2.0, 3, 3), 0.0)
        self.assertAlmostEqual(S.beta_of(8, 6.0, 8, 2), 1 / 3)
        self.assertAlmostEqual(S.beta_of(2, 6.0, 8, 2), -2 / 3)
        self.assertAlmostEqual(S.beta_of(7, 6.0, 8, 2), 1 / 6)
        self.assertAlmostEqual(S.beta_of(4, 6.0, 8, 2), -1 / 3)

    def test_null_pmf_equal_matches_enumeration(self):
        s = [2, 1, 3, 0, 2]
        slots = [j for j, k in enumerate(s) for _ in range(k)]
        for n in range(1, len(slots) + 1):
            combos = list(itertools.combinations(range(len(slots)), n))
            cnt = np.bincount([len({slots[i] for i in c}) for c in combos], minlength=6) / len(combos)
            pmf = S.null_pmf_equal(s, n)
            for k in range(6):
                self.assertAlmostEqual(pmf.get(k, 0.0), cnt[k], places=12)

    def test_linear_beta_and_mid_p_have_zero_null_mean_exactly(self):
        for s in ([3] * 14, [3] * 10 + [2, 2, 1, 0]):
            S_ = sum(s)
            for n in range(1, S_ + 1):
                pmf = S.null_pmf_equal(s, n)
                E, cmax, cmin = S.e_equal(s, n), S.c_max_of(s, n), S.c_min_of(s, n)
                self.assertAlmostEqual(sum(k * p for k, p in pmf.items()), E, places=9)
                self.assertAlmostEqual(sum(p * S.beta_of(k, E, cmax, cmin) for k, p in pmf.items()), 0.0, places=9)
                self.assertAlmostEqual(sum(p * S.beta_mid(k, null_pmf=pmf) for k, p in pmf.items()), 0.0, places=9)
        for r in S.exact_equal_weight_beta(14, 3):
            self.assertAlmostEqual(r["E_beta_under_null"], 0.0, places=6)

    def test_beta_mid_bounds(self):
        self.assertEqual(S.beta_mid(5, null_counts=[1, 2, 3]), 1.0)
        self.assertEqual(S.beta_mid(0, null_counts=[1, 2, 3]), -1.0)
        self.assertEqual(S.beta_mid(4, null_counts=[4, 4]), 0.0)
        self.assertAlmostEqual(S.beta_mid(2, null_pmf={1: 0.25, 2: 0.5, 3: 0.25}), 0.0)

    def test_beta_bm_edges(self):
        slots = complete_slots()
        Y = np.zeros((42, 3), np.int8)
        Y[0, 0] = 1                                         # n = 1 -> beta 0
        Y[:6, 1] = 1                                        # CEPs 0 and 1, all runs: n = 6, c = 2 = c_min
        Y[::7, 2] = 1                                       # one run in 6 different CEPs: n = 6, c = 6 = c_max
        r0 = S.beta_bm(slots, Y, 0, 14)
        self.assertEqual((r0["n"], r0["c"], r0["beta"], r0["beta_mid"]), (1, 1, 0.0, 0.0))
        r1 = S.beta_bm(slots, Y, 1, 14)
        self.assertEqual((r1["n"], r1["c"], r1["cmin"], r1["cmax"]), (6, 2, 2, 6))
        self.assertAlmostEqual(r1["E"], S.e_equal([3] * 14, 6), places=9)
        self.assertAlmostEqual(r1["beta"], (2 - r1["E"]) / 4, places=12)
        self.assertTrue(-1 <= r1["beta"] < 0 and -1 <= r1["beta_mid"] < 0)
        r2 = S.beta_bm(slots, Y, 2, 14, np.linspace(-1, 1, 14))
        self.assertEqual((r2["n"], r2["c"], r2["cmin"], r2["cmax"]), (6, 6, 2, 6))
        self.assertAlmostEqual(r2["beta"], (6 - r2["E"]) / 4, places=12)
        self.assertTrue(0 < r2["beta"] <= 1 and 0 < r2["beta_mid"] <= 1)
        Y2 = np.ones((42, 1), np.int8)
        Y2[:2, 0] = 0                                       # n = 40: c_min = c_max = 14 -> beta 0
        self.assertEqual(S.beta_bm(slots, Y2, 0, 14)["beta"], 0.0)
        self.assertIsNone(S.beta_bm(slots, np.zeros((42, 1), np.int8), 0, 14)["beta"])

    def test_missing_cells_reduce_slots(self):
        slots = np.delete(complete_slots(), [0, 1, 5])      # CEP 0 has 1 answered run, CEP 1 has 2
        Y = np.zeros((39, 1), np.int8)
        Y[0, 0] = 1
        Y[1, 0] = 1
        r = S.beta_bm(slots, Y, 0, 14)
        self.assertEqual((r["slots"], r["n"], r["c"]), (39, 2, 2))
        s = np.bincount(slots, minlength=14)
        self.assertAlmostEqual(r["E"], S.e_equal(s, 2), places=12)


def tab_from(ns_betas, sub="v0.20", b="B"):
    return {(sub, b, m): {"n": n, "beta": beta, "slots": 42} for m, (n, beta) in ns_betas.items()}


class TestCovStarAndRates(unittest.TestCase):
    P = ["m1", "m2", "m3"]

    def test_floor_and_mean(self):
        t = tab_from({"m1": (10, 0.4), "m2": (5, -0.2), "m3": (0, None)})
        r = S.cov_star(t, "v0.20", "B", self.P)
        self.assertTrue(r["rated"])
        self.assertAlmostEqual(r["cov_star"], 50 * (1 + 0.1))
        for ns in ({"m1": (13, 0.1), "m2": (0, None), "m3": (0, None)},
                   {"m1": (12, 0.1), "m2": (1, 0.0), "m3": (0, None)},
                   {"m1": (14, 0.1), "m2": (0, None), "m3": (0, None)}):
            self.assertIsNone(S.cov_star(tab_from(ns), "v0.20", "B", self.P)["cov_star"])
        t = tab_from({"m1": (4, 0.5), "m2": (2, 0.0), "m3": (0, None)})
        self.assertIsNotNone(S.cov_star(t, "v0.20", "B", self.P, floor=6)["cov_star"])
        self.assertIsNone(S.cov_star(t, "v0.20", "B", self.P, floor=14)["cov_star"])
        t = tab_from({"m1": (10, 0.0), "m2": (10, 0.0), "m3": (7, 0.0)})
        self.assertIsNone(S.cov_star(t, "v0.20", "B", self.P, floor=28)["cov_star"])
        self.assertEqual(S.cov_star(t, "v0.20", "B", self.P)["cov_star"], 50.0)

    def test_pi_cov(self):
        t = {("v0.20", "B", "m1"): {"n": 10, "slots": 42}, ("v0.20", "B", "m2"): {"n": 5, "slots": 40},
             ("v0.20", "B", "m3"): {"n": 0, "slots": 41}}
        self.assertAlmostEqual(S.pi_cov(t, "v0.20", "B", self.P), 15 / 123)

    def test_raw_cov_majority_and_k(self):
        ceps = [f"J{j}" for j in range(14)]
        idx = {}
        for m in self.P:
            for j in ceps:
                for r in S.RUNS:
                    idx[("v0.20", m, j, r)] = frozenset()
        idx[("v0.20", "m1", "J0", 1)] = frozenset({"B"})
        idx[("v0.20", "m1", "J0", 2)] = frozenset({"B"})          # m1 covers J0 (2 of 3)
        idx[("v0.20", "m2", "J0", 1)] = frozenset({"B"})          # m2 does not (1 of 3)
        del idx[("v0.20", "m3", "J0", 3)]
        idx[("v0.20", "m3", "J0", 1)] = frozenset({"B"})          # m3: 1 of 2 answered -> not covered
        idx[("v0.20", "m2", "J1", 1)] = frozenset({"B"})
        del idx[("v0.20", "m2", "J1", 2)], idx[("v0.20", "m2", "J1", 3)]   # m2: 1 of 1 -> covers J1
        idx[("v0.20", "m3", "J1", 2)] = frozenset({"B"})
        idx[("v0.20", "m3", "J1", 3)] = frozenset({"B"})          # m3 covers J1
        self.assertTrue(S.model_covers(idx, "v0.20", "m1", "J0", "B"))
        self.assertFalse(S.model_covers(idx, "v0.20", "m3", "J0", "B"))
        self.assertTrue(S.model_covers(idx, "v0.20", "m2", "J1", "B"))
        self.assertAlmostEqual(S.raw_cov(idx, "v0.20", "B", self.P, ceps, k=1), 100 * 2 / 14)
        self.assertAlmostEqual(S.raw_cov(idx, "v0.20", "B", self.P, ceps, k=2), 100 * 1 / 14)
        self.assertEqual(S.raw_cov(idx, "v0.20", "B", self.P, ceps, k=3), 0.0)


def synthetic_answers(seed, cats=(("v0.19", 16), ("v0.20", 24), ("v0.21", 24)), models=("m1", "m2", "m3"),
                      drop=()):
    rng = np.random.default_rng(seed)
    answers, brands, ceps = [], {}, {}
    for sub, nb in cats:
        brands[sub] = [f"{sub}-b{i:02d}" for i in range(nb)]
        ceps[sub] = [f"{sub}-J{j:02d}" for j in range(14)]
        p = rng.uniform(0.05, 0.9, nb)
        for m in models:
            for j in ceps[sub]:
                for r in S.RUNS:
                    if (sub, m, j, r) in drop:
                        continue
                    named = {b for b, pb in zip(brands[sub], p) if rng.random() < pb}
                    answers.append({"substrate": sub, "model": m, "probe_id": j, "run": r, "brands": named})
    return answers, brands, ceps


class TestCoverageTable(unittest.TestCase):
    def test_deterministic_and_order_free(self):
        ans, brands, ceps = synthetic_answers(21)
        idx = S.index_answers(ans)
        t1 = S.coverage_table(idx, brands, ceps, ["m3", "m1", "m2"])
        t2 = S.coverage_table(S.index_answers(list(reversed(ans))), brands, ceps, ["m1", "m2", "m3"])
        self.assertEqual(t1, t2)
        self.assertEqual({v["delta_status"] for v in t1.values()}, {"ok"})
        t3 = S.coverage_table(idx, brands, ceps, ["m1", "m2", "m3"], null="equal")
        for (sub, b, m), v in t3.items():
            if v["n"]:
                self.assertAlmostEqual(v["E"], S.e_equal([3] * 14, v["n"]), places=9)
        with self.assertRaises(ValueError):
            S.coverage_table(idx, brands, ceps, ["m1"], null="weighted")

    def test_missing_call_and_duplicates(self):
        ans, brands, ceps = synthetic_answers(22, drop={("v0.20", "m1", "v0.20-J00", 1)})
        idx = S.index_answers(ans)
        t = S.coverage_table(idx, brands, ceps, ["m1", "m2", "m3"], null="equal")
        self.assertEqual(t[("v0.20", "v0.20-b00", "m1")]["slots"], 41)
        self.assertEqual(t[("v0.20", "v0.20-b00", "m2")]["slots"], 42)
        with self.assertRaises(ValueError):
            S.index_answers(ans + ans[:1])

    def test_end_to_end_ranges(self):
        ans, brands, ceps = synthetic_answers(23)
        idx = S.index_answers(ans)
        t = S.coverage_table(idx, brands, ceps, ["m1", "m2", "m3"])
        cov = S.cov_star_map(t, ["m1", "m2", "m3"])
        pi = S.pi_cov_map(t, ["m1", "m2", "m3"])
        vals = [v for v in cov.values() if v is not None]
        self.assertGreater(len(vals), 40)
        self.assertTrue(all(0 <= v <= 100 for v in vals))
        self.assertTrue(all(0 <= v <= 1 for v in pi.values()))
        test = S.rho_test(cov, pi, 112003, "two", n_perm=99, n_boot=99)
        self.assertIn(S.verdict_separability(test), S.VERDICTS)


class TestVerdicts(unittest.TestCase):
    def t(self, rho, p=0.01, floor=False):
        return {"rho_w": rho, "p_perm": p, "below_n_floor": floor}

    def test_separability_bands(self):
        V = S.verdict_separability
        self.assertEqual(V(self.t(0.30)), "CONFIRMED")
        self.assertEqual(V(self.t(-0.30)), "CONFIRMED")
        self.assertEqual(V(self.t(0.30000001)), "MARGINAL")
        self.assertEqual(V(self.t(-0.49)), "MARGINAL")
        self.assertEqual(V(self.t(0.50)), "FALSIFIED")
        self.assertEqual(V(self.t(-0.7)), "FALSIFIED")
        self.assertEqual(V(self.t(0.1, floor=True)), "UNDETERMINED")
        self.assertEqual(V(self.t(float("nan"))), "UNDETERMINED")

    def test_reliability_rule(self):
        V = S.verdict_reliability
        self.assertEqual(V(self.t(1 / 3, 0.01)), "CONFIRMED")            # rel = 0.50
        self.assertEqual(V(self.t(0.6, 0.06)), "FALSIFIED")              # p >= 0.05
        self.assertEqual(V(self.t(0.15, 0.01)), "FALSIFIED")             # rel = 0.26 < 0.30
        self.assertEqual(V(self.t(0.25, 0.01)), "MARGINAL")              # rel = 0.40
        self.assertEqual(V(self.t(0.6, 0.01, floor=True)), "UNDETERMINED")
        self.assertAlmostEqual(S.spearman_brown_half(1 / 3), 0.5)

    def test_replication_rule(self):
        V = S.verdict_replication
        self.assertEqual(V(self.t(0.70, 0.01)), "CONFIRMED")
        self.assertEqual(V(self.t(0.75, 0.20)), "MARGINAL")
        self.assertEqual(V(self.t(0.60, 0.01)), "MARGINAL")
        self.assertEqual(V(self.t(0.49, 0.01)), "FALSIFIED")
        self.assertEqual(V(self.t(0.9, 0.01, floor=True)), "UNDETERMINED")


class TestGate(unittest.TestCase):
    ALL = {"H1_Sep_Presence": "CONFIRMED", "H2_Sep_Consistency": "CONFIRMED", "H3_Sep_NamingRate": "CONFIRMED",
           "H4_Reliability": "CONFIRMED", "H5_Sep_Ranking": "INACTIVE", "H6_Sep_Sentiment": "INACTIVE",
           "H7_Sep_Presence_Legacy": "CONFIRMED", "H8_Panel_Replication": "CONFIRMED"}

    def v(self, **kw):
        d = dict(self.ALL)
        d.update(kw)
        return d

    def test_pass_and_instrument_fail(self):
        self.assertEqual(S.gate(True, self.v())["verdict"], "PASS")
        self.assertEqual(S.gate(False, self.v())["verdict"], "INSTRUMENT FAIL")

    def test_fail_beats_undetermined_and_secondaries(self):
        g = S.gate(True, self.v(H2_Sep_Consistency="FALSIFIED", H4_Reliability="UNDETERMINED"))
        self.assertEqual(g["verdict"], "FAIL")
        self.assertEqual(S.gate(True, self.v(H1_Sep_Presence="FALSIFIED"))["verdict"], "FAIL")

    def test_conditional_legs(self):
        act = {"H5_Sep_Ranking": True, "H6_Sep_Sentiment": False}
        self.assertEqual(S.gate(True, self.v(H5_Sep_Ranking="FALSIFIED"), act)["verdict"], "FAIL")
        self.assertEqual(S.gate(True, self.v(H5_Sep_Ranking="CONFIRMED"), act)["verdict"], "PASS")
        self.assertEqual(S.gate(True, self.v(H5_Sep_Ranking="CONFIRMED", H6_Sep_Sentiment="FALSIFIED"),
                                act)["verdict"], "PASS")                   # H6 inactive: ignored
        with self.assertRaises(ValueError):
            S.gate(True, self.v(), {"H5_Sep_Ranking": True})              # active leg with INACTIVE verdict
        with self.assertRaises(ValueError):
            S.gate(True, self.v(H1_Sep_Presence="PASS"))

    def test_undetermined_and_marginal(self):
        self.assertEqual(S.gate(True, self.v(H3_Sep_NamingRate="UNDETERMINED"))["verdict"], "UNDETERMINED")
        self.assertEqual(S.gate(True, self.v(H4_Reliability="MARGINAL"))["verdict"], "MARGINAL")

    def test_h7_downgrade_only(self):
        self.assertEqual(S.gate(True, self.v(H7_Sep_Presence_Legacy="FALSIFIED"))["verdict"], "MARGINAL")
        self.assertEqual(S.gate(True, self.v(H7_Sep_Presence_Legacy="UNDETERMINED"))["verdict"], "PASS")
        self.assertEqual(S.gate(True, self.v(H8_Panel_Replication="FALSIFIED"))["verdict"], "PASS")

    def test_two_model_cap_and_cross_panel_label(self):
        self.assertEqual(S.gate(True, self.v(), two_model=True)["verdict"], "MARGINAL")
        act = {"H6_Sep_Sentiment": True}
        g = S.gate(True, self.v(H6_Sep_Sentiment="CONFIRMED"), act, h6_cross_panel=True)
        self.assertEqual(g["verdict"], "PASS")
        self.assertIn("cross-panel", g["label"])


class TestMCSituation(unittest.TestCase):
    def build(self, fn, models=("m1", "m2", "m3"), subs=("v0.20", "v0.21")):
        cep, ctl = {}, {}
        for sub in subs:
            for m in models:
                for r in S.RUNS:
                    for j in range(14):
                        cep[(sub, m, f"J{j}", r)] = fn(sub, m, j, r)
                    ctl[(sub, m, r)] = {"A", "B", "C"}
        return cep, ctl

    def test_situations_change_sets_pass(self):
        cep, ctl = self.build(lambda s, m, j, r: {f"b{j}", f"b{j + 1}", "A"})
        res = S.mc_situation(cep, ctl, ["m1", "m2", "m3"])
        self.assertTrue(res["passed"])
        self.assertAlmostEqual(res["pooled_mean_J_within"], 1.0)
        self.assertLess(res["pooled_mean_J_between"], 0.3)
        self.assertEqual(res["cells_used"], 2 * 3 * 3)

    def test_same_set_everywhere_fails(self):
        cep, ctl = self.build(lambda s, m, j, r: {"A", "B", "C"})
        res = S.mc_situation(cep, ctl, ["m1", "m2", "m3"])
        self.assertFalse(res["passed"])
        self.assertAlmostEqual(res["pooled_mean_J_within_minus_J_between"], 0.0)
        self.assertAlmostEqual(res["mean_J_with_C0"], 1.0)

    def test_high_between_overlap_fails(self):
        common = {f"c{i}" for i in range(7)}
        cep, ctl = self.build(lambda s, m, j, r: common | {f"u{j}"})     # J_between = 7/9, J_within = 1
        res = S.mc_situation(cep, ctl, ["m1", "m2", "m3"])
        self.assertGreaterEqual(res["pooled_mean_J_within_minus_J_between"], 0.10)
        self.assertGreater(res["pooled_mean_J_between"], 0.60)
        self.assertFalse(res["passed"])

    def test_empty_pairs_skipped_and_panel_only(self):
        cep, ctl = self.build(lambda s, m, j, r: set() if j < 2 else {f"b{j}"})
        cep[("v0.20", "zz", "J0", 1)] = {"X"}
        res = S.mc_situation(cep, ctl, ["m1"])
        self.assertGreater(res["pairs_skipped_empty_union"], 0)
        self.assertEqual({c["model"] for c in res["cells"]}, {"m1"})
        self.assertTrue(res["passed"])


class TestCalibrationMachinery(unittest.TestCase):
    def test_small_run_reproducible(self):
        a = S.calibrate_n1(n_cats=3, seed=5, n_ref_perm=2)
        b = S.calibrate_n1(n_cats=3, seed=5, n_ref_perm=2)
        a.pop("runtime_seconds")
        b.pop("runtime_seconds")
        self.assertEqual(a, b)
        self.assertIn(a["statistic_r1"]["result"], ("PASS", "FAIL"))
        self.assertEqual(set(a["variants"]), {"primary", "S8_mid_p", "S3_equal_weights"})
        self.assertEqual(a["delta_fit"]["failures_set_to_zero"], 0)


if __name__ == "__main__":
    unittest.main()
