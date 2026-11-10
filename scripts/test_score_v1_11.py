#!/usr/bin/env python3
"""Tests for score_v1_11.py on synthetic data only (no archive data, no model calls).
Run: python3 -m unittest scripts/test_score_v1_11.py   (from the repo root)"""
import json
import math
import os
import random
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import score_v1_11 as S  # noqa: E402

PROMPT_MD = os.path.join(HERE, "..", "osf", "methodology", "v1_11", "prereg", "judge_prompt_v1_11.md")


def ok(v=0, ev=False, mixed=False, ref=True, evidence=""):
    return json.dumps({"refers_to_brand": ref, "evaluative": ev, "mixed": mixed,
                       "valence": v, "evidence": evidence})


class TestWindow(unittest.TestCase):
    ANSWER = ("For small teams, these are the top picks:\n\n### Best overall: **ClickUp**\n"
              "- Very flexible\n- Can feel overwhelming at first\n\n### Simplest: **Trello**\n"
              "- Easy to learn\n- Limited for complex projects\n\nOverall, Trello and ClickUp both work.")

    def test_brand_block_takes_sub_bullets_and_stops_at_next_brand(self):
        w = S.build_window(self.ANSWER, ["ClickUp"], ["Trello"])
        self.assertIn("Very flexible", w)
        self.assertIn("overwhelming", w)
        self.assertNotIn("Easy to learn", w)
        self.assertIn("Overall, Trello and ClickUp both work.", w)  # second naming segment
        self.assertIn("[...]", w)

    def test_flattened_newlines(self):
        flat = self.ANSWER.replace("\n", "  ")
        self.assertEqual(S.build_window(flat, ["ClickUp"], ["Trello"]),
                         S.build_window(self.ANSWER, ["ClickUp"], ["Trello"]))

    def test_miss_returns_none_and_word_boundary(self):
        self.assertIsNone(S.build_window("Asana is fine.", ["Notion"]))
        self.assertIsNone(S.build_window("Notional limits apply.", ["Notion"]))

    def test_accent_folding_and_case(self):
        self.assertIsNotNone(S.build_window("I like WUSTHOF knives.", ["Wüsthof"]))

    def test_cap(self):
        long = "Brandx is good. " + " ".join(["Brandx again has a long sentence here."] * 100)
        w = S.build_window(long, ["Brandx"], cap=200)
        self.assertLessEqual(len(w), 200 + len(" [...]") + len("[...] "))
        self.assertTrue(w.endswith("[...]"))

    def test_recognition_cap(self):
        t, cut = S.recognition_text("a" * 20, cap=10)
        self.assertTrue(cut)
        self.assertEqual(S.recognition_text("short")[1], False)


class TestCapWindows(unittest.TestCase):
    def test_cap_is_seeded_and_model_balanced(self):
        units = [{"unit_id": f"u{i:03d}", "answer_set": "E1", "wave": "single", "brand": "B",
                  "model": f"m{i % 6}"} for i in range(120)]
        a = S.cap_windows(units, k=36)
        b = S.cap_windows(units, k=36)
        self.assertEqual([u["unit_id"] for u in a], [u["unit_id"] for u in b])
        self.assertEqual(len(a), 36)
        per_model = {m: sum(u["model"] == m for u in a) for m in {u["model"] for u in a}}
        self.assertEqual(set(per_model.values()), {6})

    def test_cap_noop_below_k(self):
        units = [{"unit_id": f"u{i}", "answer_set": "F", "wave": "t1", "brand": "B", "model": "m"}
                 for i in range(10)]
        self.assertEqual(len(S.cap_windows(units, k=36)), 10)


class TestJudgeOutput(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(S.parse_judge_output(ok(1, True, evidence="well regarded"))["valence"], 1)
        self.assertEqual(S.parse_judge_output("```json\n" + ok() + "\n```")["valence"], 0)

    def test_invalid(self):
        bad = ["not json", ok(3, True), ok(1, False), ok(0, False, True), ok(1, True, ref=False),
               json.dumps({"valence": 0}), ok(0).replace("false", "0", 1)]
        for b in bad:
            with self.assertRaises(S.JudgeOutputError, msg=b):
                S.parse_judge_output(b)

    def test_request_is_blind(self):
        unit = {"unit_id": "x", "brand_display": "Acme", "category": "widgets", "question": "Best widgets?",
                "unit_type": "mention", "text": "Acme is fine.", "model": "secret-model", "wave": "t2"}
        r = S.build_request(unit)
        self.assertNotIn("secret-model", r["user"] + r["system"])
        self.assertNotIn("t2", r["user"])
        self.assertEqual(r["params"]["temperature"], 0)

    def test_prompt_md_matches_script(self):
        with open(PROMPT_MD, encoding="utf-8") as f:
            md = f.read()
        for name, value in (("SYSTEM_PROMPT", S.SYSTEM_PROMPT), ("USER_TEMPLATE", S.USER_TEMPLATE)):
            block = re.search(rf"<!-- BEGIN {name} -->\n```text\n(.*?)\n```\n<!-- END {name} -->", md, re.S)
            self.assertIsNotNone(block, name)
            self.assertEqual(block.group(1), value, name)
        schema = re.search(r"<!-- BEGIN OUTPUT_SCHEMA -->\n```json\n(.*?)\n```", md, re.S).group(1)
        self.assertEqual(json.loads(schema), S.OUTPUT_SCHEMA)


class TestScore(unittest.TestCase):
    def test_unit_score(self):
        self.assertEqual([S.unit_score(v) for v in S.VALENCES], [0, 25, 50, 75, 100])

    def test_floor_and_neutral_kept(self):
        j = [S.parse_judge_output(ok(0)) for _ in range(4)] + \
            [S.parse_judge_output(ok(2, True, evidence="the best")) for _ in range(2)]
        bs = S.brand_score(j)
        self.assertEqual(bs.n, 6)
        self.assertAlmostEqual(bs.S, (4 * 50 + 2 * 100) / 6)
        self.assertAlmostEqual(bs.E, 2 / 6)
        self.assertIsNone(bs.NV)  # only 2 evaluative units < 3
        self.assertIsNone(S.brand_score(j[:5]).S)  # n = 5 < 6 -> not rated

    def test_excluded_units(self):
        j = [S.parse_judge_output(ok(ref=False))] + [None] + [S.parse_judge_output(ok(1, True))] * 6
        bs = S.brand_score(j)
        self.assertEqual((bs.n, bs.n_excluded), (6, 2))
        self.assertAlmostEqual(bs.S, 75.0)


class TestStats(unittest.TestCase):
    def test_spearman_ties(self):
        self.assertAlmostEqual(S.spearman([1, 2, 3, 4], [10, 20, 30, 40]), 1.0)
        self.assertAlmostEqual(S.spearman([1, 2, 3, 4], [4, 3, 2, 1]), -1.0)
        self.assertEqual(S.average_ranks([5, 5, 1]), [2.5, 2.5, 1.0])

    def test_within_group_removes_level_differences(self):
        g = ["a"] * 5 + ["b"] * 5
        x = [1, 2, 3, 4, 5, 101, 102, 103, 104, 105]
        y = [5, 4, 3, 2, 1, 15, 14, 13, 12, 11]
        self.assertGreater(S.spearman(x, y), 0.5)          # pooled raw: driven by group level
        self.assertAlmostEqual(S.rho_within(g, x, y), -1.0)  # within-group: perfectly inverse

    def test_bands(self):
        self.assertEqual(S.band_verdict(0.30), "CONFIRMED")
        self.assertEqual(S.band_verdict(0.31), "MARGINAL")
        self.assertEqual(S.band_verdict(0.50), "FALSIFIED")
        self.assertEqual(S.separability_verdict([0.1, 0.2, 0.3]), "CONFIRMED")
        self.assertEqual(S.separability_verdict([0.1, 0.55, 0.6]), "FALSIFIED")
        self.assertEqual(S.separability_verdict([0.1, 0.55, 0.2]), "MARGINAL")
        self.assertEqual(S.separability_verdict([0.1, float("nan"), 0.2]), "UNDETERMINED")

    def test_permutation_seeded_and_detects_signal(self):
        rng = random.Random(7)
        g = [s for s in "abcde" for _ in range(12)]
        x = [rng.random() for _ in g]
        y = [v + rng.gauss(0, 0.1) for v in x]
        r1, p1 = S.perm_test_within(g, x, y, n_perm=500, seed=1)
        r2, p2 = S.perm_test_within(g, x, y, n_perm=500, seed=1)
        self.assertEqual((r1, p1), (r2, p2))
        self.assertGreater(r1, 0.8)
        self.assertLess(p1, 0.01)
        self.assertEqual(S.stability_verdict(r1, p1), "CONFIRMED")
        self.assertEqual(S.stability_verdict(0.6, 0.2), "FALSIFIED")
        self.assertEqual(S.stability_verdict(0.4, 0.01), "MARGINAL")

    def test_alpha(self):
        perfect = [(v, v) for v in S.VALENCES for _ in range(5)]
        self.assertAlmostEqual(S.krippendorff_alpha_ordinal(perfect), 1.0)
        rng = random.Random(3)
        noise = [(rng.choice(S.VALENCES), rng.choice(S.VALENCES)) for _ in range(2000)]
        self.assertLess(abs(S.krippendorff_alpha_ordinal(noise)), 0.1)
        self.assertEqual(S.judge_agreement_verdict(0.70, 0.85), "CONFIRMED")
        self.assertEqual(S.judge_agreement_verdict(0.70, 0.55), "FALSIFIED")
        self.assertEqual(S.judge_agreement_verdict(0.60, 0.85), "MARGINAL")
        self.assertAlmostEqual(S.cohen_kappa([1, 0, 1, 0], [1, 0, 1, 0]), 1.0)


class TestCost(unittest.TestCase):
    def test_projection_and_cap(self):
        g = S.CostGuard(price_in_per_mtok=5.0, price_out_per_mtok=25.0)
        plan = [(432, 2100, 100), (3350, 1000, 100), (12700, 1000, 100)]
        self.assertTrue(g.check_plan(plan))
        g2 = S.CostGuard(price_in_per_mtok=15.0, price_out_per_mtok=75.0)
        self.assertFalse(g2.check_plan(plan + [(5052, 1100, 100)]))
        g3 = S.CostGuard(1.0, 1.0, cap_usd=0.002)
        g3.charge(1000, 0)
        with self.assertRaises(RuntimeError):
            g3.charge(1000, 1000)
        self.assertTrue(math.isclose(g3.spent_usd, 0.001))

    def test_judge_call_is_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            S.judge_call({}, "any")


if __name__ == "__main__":
    unittest.main()
