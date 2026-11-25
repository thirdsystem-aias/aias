#!/usr/bin/env python3
"""Tests for stats_arm_a.py and analyze_arm_a.py, on hand-computed cases and simulated Google data only."""
import math
import sys
import unittest
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
import analyze_arm_a as A    # noqa: E402
import dry_run_arm_a as DR   # noqa: E402
import join_arm_a as J       # noqa: E402
import params_arm_a as P     # noqa: E402
import stats_arm_a as S      # noqa: E402


class TestStats(unittest.TestCase):
    def test_ranks_ties_average(self):
        self.assertEqual(list(S.rankdata([10, 20, 20, 5])), [2.0, 3.5, 3.5, 1.0])

    def test_spearman_and_pearson(self):
        self.assertAlmostEqual(S.spearman([1, 2, 3, 4], [1, 3, 2, 4]), 0.8)
        self.assertAlmostEqual(S.pearson([1, 2, 3], [2, 4, 6]), 1.0)
        self.assertTrue(math.isnan(S.pearson([1, 1, 1], [1, 2, 3])))

    def test_partial_corr_removes_z(self):
        rng = np.random.default_rng(1)
        z = rng.normal(size=400)
        x = z + rng.normal(scale=0.1, size=400)
        y = z + rng.normal(scale=0.1, size=400)
        self.assertGreater(S.pearson(x, y), 0.9)
        self.assertLess(abs(S.partial_corr(x, y, z)), 0.15)
        # hand case: x and y each equal z plus orthogonal parts
        z = np.array([1., 2., 3., 4.]); ex = np.array([1., -1., -1., 1.]); ey = np.array([1., -1., -1., 1.])
        self.assertAlmostEqual(S.partial_corr(z + ex, 2 * z + ey, z), 1.0)

    def test_fisher_pool(self):
        self.assertAlmostEqual(S.fisher_pool([0.5, 0.5], [10, 20]), 0.5)
        r = S.fisher_pool([0.2, 0.6], [13, 23])
        self.assertAlmostEqual(r, math.tanh((10 * math.atanh(0.2) + 20 * math.atanh(0.6)) / 30))

    def test_holm(self):
        self.assertEqual(S.holm([0.01, 0.04, 0.03]), [0.03, 0.06, 0.06])
        self.assertEqual(S.holm([0.02, None]), [0.02, None])

    def test_perm_p(self):
        self.assertAlmostEqual(S.perm_p(0.5, [0.1, 0.6, 0.5, 0.2]), 3 / 5)
        self.assertAlmostEqual(S.perm_p(0.9, [0.1, 0.2]), 1 / 3)

    def test_jonckheere(self):
        self.assertEqual(S.jonckheere([[1, 2], [3, 4], [5, 6]]), 12.0)
        self.assertEqual(S.jonckheere([[1], [1]]), 0.5)

    def test_within_group_permutation(self):
        rng = np.random.default_rng(0)
        g = ["a", "a", "b", "b", "b"]
        for _ in range(20):
            k = S.within_group_permutation(rng, g)
            self.assertEqual(sorted(k[:2]), [0, 1])
            self.assertEqual(sorted(k[2:]), [2, 3, 4])

    def test_norm_ranks_and_centre(self):
        self.assertEqual(list(S.norm_ranks_within([3, 1, 2, 9, 8], ["a", "a", "a", "b", "b"])), [1.0, 0.0, 0.5, 1.0, 0.0])
        self.assertEqual(list(S.centre_within([1., 3., 10., 20.], ["a", "a", "b", "b"])), [-1., 1., -5., 5.])

    def test_percentile_ci(self):
        lo, hi = S.percentile_ci(list(range(101)))
        self.assertAlmostEqual(lo, 2.5)
        self.assertAlmostEqual(hi, 97.5)


def series(level, months, slope=0.0):
    return {ym: {"etv": math.exp(level + slope * i), "g": math.log1p(math.exp(level + slope * i)), "count": 0.0,
                 "top10": 0.0} for i, ym in enumerate(months)}


MONTHS1 = J.window((2026, 11), 25)          # Nov 2024 .. Nov 2026 (pull 1's complete months)


def synthetic_inputs(effect=True, seed=3):
    """Cars only: R, S and Gs built so that log R tracks log S beyond log Gs when effect=True."""
    rng = np.random.default_rng(seed)
    domains = J.load_domains()
    bd = J.brand_domains(domains)
    shift, panel, presence = {}, {}, {}
    groups = {"luxury": 7, "mass": 7, "electric": 4}
    cars = [b for b, (c, _) in sorted(bd.items()) if c == "cars"]
    gi = [g for g, n in groups.items() for _ in range(n)]
    for b, g in zip(cars, gi):
        lg = rng.normal(10, 1)
        ls = lg + rng.normal(0, 1)
        lm = (ls if effect else lg) + rng.normal(0, 0.3)
        shift[b] = {"group": g, "m_rec": int(round(math.exp(lm - 8))), "sales_usd": math.exp(ls + 10)}
        panel[bd[b][1]] = series(lg, MONTHS1)
        presence[("cars", b, "t1")] = float(rng.uniform())
        presence[("cars", b, "t3")] = float(rng.uniform())
    return {1: (panel, {}, (2026, 12))}, presence, shift, domains


class TestHypotheses(unittest.TestCase):
    def test_zero_rule_r_is_centred_log_of_m_plus_half(self):
        panels, pres, shift, dom = synthetic_inputs()
        b0 = sorted(shift)[0]
        shift[b0]["m_rec"] = 0
        I = A.Inputs(panels, pres, shift, domains=dom)
        rows = A.cars_t1(I)
        self.assertEqual(len(rows), 18)
        g = [r["group"] for r in rows]
        r = S.centre_within(np.log(np.array([x["m"] for x in rows], float) + 0.5), g)
        self.assertTrue(np.all(np.isfinite(r)))

    def test_h_a2_detects_a_built_effect_and_not_a_null(self):
        panels, pres, shift, dom = synthetic_inputs(effect=True)
        r = A.h_a2(A.Inputs(panels, pres, shift, domains=dom), n_perm=999)
        self.assertGreater(r["partial_r"], 0.3)
        self.assertLess(r["p"], 0.05)
        self.assertEqual(r["groups"], {"luxury": 7, "mass": 7, "electric": 4})
        self.assertEqual(set(r["sensitivity"]), {"i_ranks", "ii_per_group_slopes", "iii_offset_0.25", "iii_offset_1.0"})
        panels, pres, shift, dom = synthetic_inputs(effect=False, seed=5)
        r0 = A.h_a2(A.Inputs(panels, pres, shift, domains=dom), n_perm=999)
        self.assertLess(r0["partial_r"], 0.3)

    def test_verdict_rules(self):
        base = {"analysable_categories": 4, "rho_bar": 0.35, "ci95": (0.1, 0.6)}
        self.assertEqual(A.verdict_a1(base, 0.01), "CONFIRMED")
        self.assertEqual(A.verdict_a1(dict(base, rho_bar=0.2, ci95=(0.05, 0.29)), 0.01), "FALSIFIED")
        self.assertEqual(A.verdict_a1(dict(base, rho_bar=0.2), 0.01), "MARGINAL")
        self.assertEqual(A.verdict_a1(base, 0.2), "UNDETERMINED")
        self.assertEqual(A.verdict_a1(dict(base, analysable_categories=2), 0.001), "UNDETERMINED")
        self.assertEqual(A.verdict_a2({"partial_r": 0.31}, 0.04), "CONFIRMED")
        self.assertEqual(A.verdict_a2({"partial_r": 0.31}, 0.06), "UNDETERMINED")
        self.assertEqual(A.verdict_a2({"partial_r": -0.01}, 0.9), "FALSIFIED")
        self.assertEqual(A.verdict_a2({"partial_r": 0.0}, 0.9), "FALSIFIED")
        self.assertEqual(A.verdict_change({"rho": 0.2}, 0.01), "SUPPORTED")
        self.assertEqual(A.verdict_change({"rho": 0.2}, 0.06), "NOT SUPPORTED")
        r4 = {"p": 0.01, "spread_ci95": (0.1, 0.5), "best_band": 2, "baseline_a": {"diff_ci95": (0.01, 0.3)},
              "placebo_b": {"spread_ci95": (-0.1, 0.2)}}
        self.assertEqual(A.verdict_a4(r4, 0.01), "SUPPORTED")
        self.assertEqual(A.verdict_a4(dict(r4, best_band=1), 0.01), "PARTIAL")
        self.assertEqual(A.verdict_a4(dict(r4, baseline_a={"diff_ci95": (-0.1, 0.3)}), 0.01), "PARTIAL")
        self.assertEqual(A.verdict_a4(r4, 0.2), "NOT SUPPORTED")
        self.assertEqual(A.verdict_a4(dict(r4, placebo_b={"spread_ci95": (0.01, 0.2)}), 0.01),
                         "SUPPORTED (not distinguishable from trend)")

    def test_terciles(self):
        b = A.terciles({f"b{i:02d}": float(i) for i in range(18)})
        self.assertEqual([list(b.values()).count(k) for k in range(3)], [6, 6, 6])
        self.assertEqual(b["b17"], 2)
        self.assertEqual(b["b00"], 0)
        b = A.terciles({f"b{i:02d}": float(i) for i in range(17)})
        self.assertEqual([list(b.values()).count(k) for k in range(3)], [5, 7, 5])

    def test_headline_pair(self):
        rows = [{"group": "g", "m": 9, "S": 1.0, "G": 1.0}, {"group": "g", "m": 1, "S": 3.0, "G": 3.0},
                {"group": "g", "m": 0, "S": 5.0, "G": 1.0}]
        h = A.headline_pair(rows)
        self.assertEqual(h["ai_over_google"]["n"], 1)
        self.assertEqual(h["other"]["n"], 2)

    def test_h_a1_pooling_needs_n8_and_three_categories(self):
        panels, pres, shift, dom = synthetic_inputs()
        r = A.h_a1(A.Inputs(panels, pres, shift, domains=dom), n_perm=99, n_boot=99)
        self.assertEqual(r["pooled_categories"], ["cars"])
        self.assertEqual(A.verdict_a1(r, 0.0001), "UNDETERMINED")

    def test_s_coi_excludes_flagged_brands(self):
        panels, pres, shift, dom = synthetic_inputs()
        I = A.Inputs(panels, pres, shift, domains=dom, exclude=P.COI_FLAGGED)
        ids = {r["brand_id"] for r in A.cars_t1(I)}
        self.assertEqual(len(ids), 15)
        self.assertFalse(ids & set(P.COI_FLAGGED))

    def test_h_a7_undetermined_without_t6(self):
        panels, pres, shift, dom = synthetic_inputs()
        r = A.h_a7(A.Inputs(panels, pres, shift, domains=dom), n_perm=9)
        self.assertEqual(r["status"], "UNDETERMINED")


class TestDryRun(unittest.TestCase):
    def test_end_to_end_on_simulated_data(self):
        import json
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "dry.json"
            DR.main(["--perm", "99", "--boot", "99", "--out", str(out)])
            d = json.loads(out.read_text())
        self.assertEqual(set(d["primary"]["verdicts"]), {"H_A1", "H_A2", "H_A3", "H_A4", "H_A5", "H_A7",
                                                         "H_A6_airlines", "H_A6_banks", "H_A6_software"})
        s = d["pull_summaries"]
        self.assertAlmostEqual(s["3"]["cumulative_spent"] if "3" in s else s[3]["cumulative_spent"], 32.6496, places=6)
        self.assertIn("1", {str(k) for k in d["break_flags"]})


if __name__ == "__main__":
    unittest.main()
