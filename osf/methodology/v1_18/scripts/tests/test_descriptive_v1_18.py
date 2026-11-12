"""Tests for the ex-post descriptive (synthetic data only).
Run: python3 -m unittest discover -s osf/methodology/v1_18/scripts/tests -v"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import common_v1_18 as C  # noqa: E402
import descriptive_v1_18 as D  # noqa: E402

T = {"e.ex": {"cls": "editorial_other", "retailer": False, "alias_of": ""},
     "l.ex": {"cls": "listing", "retailer": False, "alias_of": ""},
     "u1.ex": {"cls": "UNRESOLVED", "retailer": False, "alias_of": ""},
     "u2.ex": {"cls": "UNRESOLVED", "retailer": False, "alias_of": ""}}
UNITS = {("v19", "A"): {"status": "RESOLVED", "domains": {"a.ex"}},
         ("v19", "B"): {"status": "RESOLVED", "domains": {"b.ex"}},
         ("v19", "N"): {"status": "NONE", "domains": set()}}


def ans(i, named, doms):
    return C.make_answer(f"c{i}", "v19", "m", ("v19", "m", "p", "f"), 1, named, doms)


ANSWERS = [ans(0, {("v19", "A")}, {"a.ex", "u1.ex"}),                      # A: 1/2 unresolved
           ans(1, {("v19", "A"), ("v19", "B")}, {"e.ex", "l.ex", "u1.ex", "u2.ex"}),  # A, B: 2/4
           ans(2, {("v19", "B"), ("v19", "N")}, {"e.ex", "l.ex", "b.ex"}),  # B: 0/3; N never a pair
           ans(3, {("v19", "A")}, {"u1.ex"})]                               # A: 1/1 (counted under 'out')


class TestDescriptive(unittest.TestCase):
    def test_per_brand_and_pooled(self):
        r = D.unresolved_shares(ANSWERS, UNITS, T, {"v19:A", "v19:B"})
        self.assertAlmostEqual(r["brands"]["v19:A"]["unresolved_share"], 100 * (0.5 + 0.5 + 1.0) / 3)
        self.assertAlmostEqual(r["brands"]["v19:B"]["unresolved_share"], 100 * (0.5 + 0.0) / 2)
        self.assertEqual(r["pooled"]["n_pairs_all"], 5)
        self.assertAlmostEqual(r["pooled"]["pair_weighted_all_pairs"], 100 * 2.5 / 5)
        self.assertAlmostEqual(r["pooled"]["brand_weighted_rated_brands"], (100 * 2 / 3 + 25) / 2)
        self.assertAlmostEqual(r["pooled"]["domain_weighted_answers"], 100 * 4 / 10)

    def test_unrated_brand_excluded_from_brand_list_not_from_all_pairs(self):
        r = D.unresolved_shares(ANSWERS, UNITS, T, {"v19:A"})
        self.assertNotIn("v19:B", r["brands"])
        self.assertEqual(r["pooled"]["n_pairs_rated"], 3)
        self.assertEqual(r["pooled"]["n_pairs_all"], 5)

    def test_pooled_equals_program_level_S1_mix(self):
        all_db = {"a.ex", "b.ex"}
        stats, pairs = C.brand_shares(ANSWERS, UNITS, all_db, T, {"unresolved": "out"}, floor=1)
        prog = C.program_level(stats, pairs)
        r = D.unresolved_shares(ANSWERS, UNITS, T, {"v19:A", "v19:B"})
        self.assertAlmostEqual(r["pooled"]["pair_weighted_all_pairs"], prog["mix_pair_weighted"]["UNRESOLVED"])

    def test_draw_counts_flag(self):
        res = {"primary": {"brands": {"v19:A": {"rated": True}, "v19:B": {"rated": True},
                                      "v19:C": {"rated": False}}},
               "primary_ci": {"n_boot": 2000, "brand": {}}}
        for d in C.DEF_ORDER:
            res["primary_ci"]["brand"][f"v19:A|{d}"] = [0, 1, 1999]
            res["primary_ci"]["brand"][f"v19:B|{d}"] = [0, 1, 999 if d == "P_any_company" else 1500]
        r = D.draw_counts(res)
        self.assertEqual(r["flagged"], ["v19:B"])
        self.assertEqual(r["brands"]["v19:B"]["min_draws"], 999)
        self.assertNotIn("v19:C", r["brands"])
        self.assertFalse(r["brands"]["v19:A"]["below_flag"])
        self.assertEqual(D.draw_counts(res, flag=999)["flagged"], [])     # strictly below


if __name__ == "__main__":
    unittest.main()
