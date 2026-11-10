#!/usr/bin/env python3
"""Unit tests for score_v1_10.py on SYNTHETIC data only (no archive file is read).
Run: python3 -m pytest scripts/test_score_v1_10.py   or   python3 scripts/test_score_v1_10.py"""
import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_v1_10 as S  # noqa: E402

REG = {"Alpha": ["Alpha Co"], "Beta": [], "Gamma": ["Gamma-X"], "Estée Lauder": ["Estee Lauder"], "La Mer": []}
P = S.compile_registry(REG)


class Extraction(unittest.TestCase):
    def test_normalize_accents_case(self):
        self.assertEqual(S.normalize("Estée LAUDER"), "estee lauder")

    def test_word_boundary_and_accents(self):
        h = S.find_mentions(S.normalize("Summer picks: ESTÉE Lauder's serum."), P)
        self.assertIn("Estée Lauder", h)
        self.assertNotIn("La Mer", h)          # 'summer' must not match 'la mer'/'mer'

    def test_first_mention_and_repeats(self):
        r = S.rank_answer("Beta is good. Alpha too. Beta again, and Gamma.", P, "first_mention")
        self.assertEqual(r["named"], 3)
        self.assertEqual({b: v[0] for b, v in r["ranks"].items()}, {"Beta": 1, "Alpha": 2, "Gamma": 3})

    def test_lead_item_rule_ignores_comparison_mentions(self):
        txt = ("Top picks:\n1. **Alpha** - often compared with Gamma.\n"
               "2. **Beta** - solid.\n3. **Gamma** - premium.\n")
        prim = S.rank_answer(txt, P, "lead_item")
        sens = S.rank_answer(txt, P, "first_mention")
        self.assertTrue(prim["list_structured"])
        self.assertEqual({b: v[0] for b, v in prim["ranks"].items()}, {"Alpha": 1, "Beta": 2, "Gamma": 3})
        self.assertEqual({b: v[0] for b, v in sens["ranks"].items()}, {"Alpha": 1, "Gamma": 2, "Beta": 3})

    def test_nested_sub_bullets_belong_to_parent(self):
        txt = "- Alpha\n    - beats Gamma on price\n- Beta\n- Gamma\n"
        r = S.rank_answer(txt, P, "lead_item")
        self.assertEqual({b: v[0] for b, v in r["ranks"].items()}, {"Alpha": 1, "Beta": 2, "Gamma": 3})

    def test_headings_as_group_labels(self):
        txt = "## Budget\n**Beta** good\n**Alpha** fine\n## Premium\n**Gamma** best\n"
        r = S.rank_answer(txt, P, "lead_item")
        self.assertEqual({b: v[0] for b, v in r["ranks"].items()}, {"Beta": 1, "Alpha": 2, "Gamma": 3})

    def test_non_leading_brand_follows_lead_brands(self):
        txt = "1. Alpha\n2. Beta\n\nAlso consider Gamma for some uses."
        r = S.rank_answer(txt, P, "lead_item")
        self.assertEqual(r["ranks"]["Gamma"][0], 3)

    def test_prose_answer_first_mention(self):
        r = S.rank_answer("I would start with Gamma, then Alpha.", P, "lead_item")
        self.assertFalse(r["list_structured"])
        self.assertEqual(r["ranks"]["Gamma"][0], 1)

    def test_single_brand_not_rankable(self):
        r = S.rank_answer("Only Alpha is worth it.", P)
        self.assertEqual(r["named"], 1)
        self.assertEqual(r["ranks"], {})

    def test_tie_mid_rank_and_min_rank(self):
        reg = S.compile_registry({"Samsung": [], "Samsung SDI": [], "LG": []})
        r = S.rank_answer("Samsung SDI leads; LG follows.", reg, "first_mention")
        self.assertEqual(r["ranks"]["Samsung"], (1.5, 1))
        self.assertEqual(r["ranks"]["Samsung SDI"], (1.5, 1))
        self.assertEqual(r["ranks"]["LG"], (3.0, 3))

    def test_alias_counts_as_brand(self):
        r = S.rank_answer("Gamma-X first, then Alpha Co.", P, "first_mention")
        self.assertEqual(set(r["ranks"]), {"Gamma", "Alpha"})


class Statistics(unittest.TestCase):
    def test_candidates_known_values(self):
        s = S.brand_scores([(1, 1, 3), (3, 3, 3), (2, 2, 5)])
        self.assertAlmostEqual(s["MNP"], 100 * (1 - (0 + 1 + 0.25) / 3))
        self.assertAlmostEqual(s["IRW"], (1 + 1 / 3 + 1 / 2) / 3)
        self.assertAlmostEqual(s["TOP3"], 1.0)
        self.assertAlmostEqual(s["TOP1"], 1 / 3)
        self.assertAlmostEqual(s["MR"], -2.0)
        self.assertEqual(s["MODE"], -1.0)       # all modes tie -> smallest rank

    def test_rating_floor(self):
        rows = [{"panel": "p", "wave": "t1", "category": "c", "brand": "A", "k_mid": 1, "k_min": 1, "n": 2}] * 6
        rows += [{"panel": "p", "wave": "t1", "category": "c", "brand": "B", "k_mid": 2, "k_min": 2, "n": 2}] * 5
        u = S.score_units(rows)
        self.assertTrue(u[("p", "t1", "c", "A")]["rated"])
        self.assertFalse(u[("p", "t1", "c", "B")]["rated"])

    def test_pooled_within_rho_ignores_level_shifts(self):
        x = [1, 2, 3, 101, 102, 103]
        y = [10, 20, 30, 1, 2, 3]
        g = ["a", "a", "a", "b", "b", "b"]
        self.assertAlmostEqual(S.pooled_within_rho(x, y, g), 1.0)

    def test_perm_p_reproducible_and_small_for_strong_signal(self):
        rng = np.random.default_rng(1)
        x = rng.normal(size=60)
        y = x + rng.normal(scale=0.2, size=60)
        g = np.repeat(["a", "b", "c"], 20)
        obs = S.pooled_within_rho(x, y, g)
        p1 = S.perm_p(x, y, g, obs, seed=7, sided="one", n_draws=500)
        p2 = S.perm_p(x, y, g, obs, seed=7, sided="one", n_draws=500)
        self.assertEqual(p1, p2)
        self.assertLess(p1, 0.01)

    def test_shuffle_keeps_named_sets(self):
        rows = [{"panel": "p", "wave": "t1", "category": "c", "answer_id": i, "brand": b,
                 "k_mid": k, "k_min": k, "n": 3} for i in range(4) for k, b in enumerate("ABC", 1)]
        out = S.shuffle_answer_ranks(rows, np.random.default_rng(3))
        for i in range(4):
            ks = sorted(r["k_mid"] for r in out if r["answer_id"] == i)
            self.assertEqual(ks, [1.0, 2.0, 3.0])

    def test_spearman_brown(self):
        self.assertAlmostEqual(S.spearman_brown(0.5), 2 / 3)


class Selection(unittest.TestCase):
    def test_highest_reliability_wins(self):
        self.assertEqual(S.select_statistic({"MNP": 0.60, "IRW": 0.75, "TOP3": 0.50})["selected"], "IRW")

    def test_tie_window_goes_to_order(self):
        self.assertEqual(S.select_statistic({"MNP": 0.74, "IRW": 0.75})["selected"], "MNP")

    def test_floor(self):
        out = S.select_statistic({"MNP": 0.49, "IRW": 0.20})
        self.assertIsNone(out["selected"])


class Verdicts(unittest.TestCase):
    def test_separability_bands(self):
        self.assertEqual(S.verdict_separability({"t1": (0.30, 50), "t2": (-0.10, 50), "t3": (0.2, 50)}), "CONFIRMED")
        self.assertEqual(S.verdict_separability({"t1": (0.31, 50), "t2": (0.10, 50)}), "MARGINAL")
        self.assertEqual(S.verdict_separability({"t1": (-0.50, 50), "t2": (0.10, 50)}), "FALSIFIED")
        self.assertEqual(S.verdict_separability({"t1": (0.10, 50), "t2": (0.10, 29)}), "UNDETERMINED")

    def test_stability_bands(self):
        self.assertEqual(S.verdict_stability(0.55, 0.001, 0.01, 40), "CONFIRMED")
        self.assertEqual(S.verdict_stability(0.45, 0.001, 0.01, 40), "MARGINAL")
        self.assertEqual(S.verdict_stability(0.55, 0.001, 0.20, 40), "FALSIFIED")
        self.assertEqual(S.verdict_stability(0.29, 0.001, 0.01, 40), "FALSIFIED")
        self.assertEqual(S.verdict_stability(0.90, 0.001, 0.01, 20), "UNDETERMINED")

    def test_gate(self):
        self.assertEqual(S.gate_verdict("CONFIRMED", "CONFIRMED", "CONFIRMED"), "PASS")
        self.assertEqual(S.gate_verdict("CONFIRMED", "CONFIRMED", "CONFIRMED", "FALSIFIED"), "MARGINAL")
        self.assertEqual(S.gate_verdict("CONFIRMED", "MARGINAL", "CONFIRMED"), "MARGINAL")
        self.assertEqual(S.gate_verdict("FALSIFIED", "UNDETERMINED", "CONFIRMED"), "FAIL")
        self.assertEqual(S.gate_verdict("CONFIRMED", "UNDETERMINED", "CONFIRMED"), "UNDETERMINED")


class Order(unittest.TestCase):
    def test_pc_refused_before_selection(self):
        if S.SELECTION_FILE.exists():
            self.skipTest("selection file present")
        with self.assertRaises(RuntimeError):
            S.open_presence_consistency(Path("/nonexistent.csv"))


if __name__ == "__main__":
    unittest.main(verbosity=1)
