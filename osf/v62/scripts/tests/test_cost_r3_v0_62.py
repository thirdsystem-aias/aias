"""Tests of cost_estimate_r3_v0_62.py (r3: the cost re-based on t4's recorded usage). No network, no model.
The committed r3 JSON is checked for internal consistency; if the v0.42 repository is present, the computation is re-run
from the pinned tag (v0.42-acquisition-locked, SHA-256 checked) and must reproduce the committed JSON exactly."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import budget_v0_62 as BG  # noqa: E402
import cost_estimate_r3_v0_62 as R3  # noqa: E402

J = json.loads((HERE.parents[1] / "prereg" / "cost_estimate_v0_62_r3.json").read_text(encoding="utf-8"))
REPO = Path.home() / "aias" / "_worktrees" / "v0.42"


class Unit(unittest.TestCase):
    def test_usage_lines_keep_usage_fields_only(self):
        line = json.dumps({"call_id": "x", "model_requested": "gpt-6-astra", "substrate": "v20", "phase": "B",
                           "condition": "S0", "status": "ok", "text": "SECRET ANSWER", "prompt": "QUESTION",
                           "search": {"queries": ["q"]}, "usage_parts": [], "cost_usd": 0.0})
        out = R3.usage_lines((line + "\n").encode("utf-8"))
        self.assertEqual(len(out), 1)
        self.assertTrue(set(out[0]) <= set(R3.USAGE_FIELDS))
        for w in ("SECRET", "QUESTION", "queries"):
            self.assertNotIn(w, json.dumps(out))

    def test_p90_is_v042_rule(self):
        self.assertEqual(R3.p90([5]), 5.0)
        self.assertAlmostEqual(R3.p90(list(range(1, 11))), 9.1)          # inclusive deciles, as cost_estimate_v0_42

    def test_per_call_prices_and_resend(self):
        s = {"in_mean": 100, "out_mean": 1000, "think_mean": 0, "in_p90": 200, "out_p90": 2000, "think_p90": 0}
        b = {(m, "B"): s for m in R3.MODELS}
        self.assertAlmostEqual(R3.per_call(b, "gemini-4-argon", "B", "central", "nov"), (100 * 2 + 1000 * 10) / 1e6 * 1.02)
        self.assertAlmostEqual(R3.per_call(b, "gemini-4-argon", "B", "central", "dec"), (100 * 4 + 1000 * 20) / 1e6 * 1.02)
        self.assertAlmostEqual(R3.per_call(b, "gemini-4-argon", "B", "high", "dec"), (200 * 4 + 2000 * 20) / 1e6 * 1.10)
        self.assertAlmostEqual(R3.per_call(b, "claude-fable-5-2", "B", "central", "dec"), (100 * 4 + 1000 * 20) / 1e6 * 1.02)
        self.assertAlmostEqual(R3.per_call(b, "gpt-6-astra", "B", "high", "nov"), (200 * 10 + 2000 * 50) / 1e6 * 1.10)
        self.assertEqual(R3.FACTOR, {"central": {"es": 1.25, "ko": 1.75, "zh": 1.50},
                                     "high": {"es": 1.50, "ko": 2.50, "zh": 2.25}})


class Committed(unittest.TestCase):
    def test_reconciliation_with_the_t4_record(self):
        rc = J["reconciliation"]
        self.assertTrue(rc["matches_recorded_spend"])
        self.assertEqual(rc["recorded_plus_t4_judge_reserve"], 67.9551)
        self.assertLess(rc["s0_max_line_difference_usd"], 1e-9)
        self.assertEqual((rc["raw_lines"], rc["s0_answered_lines"], rc["s0_answered_with_resend_or_retry"]), (990, 606, 0))
        self.assertEqual(J["source"]["commit"], R3.TAG_COMMIT)
        self.assertFalse(J["source"]["answer_text_read"])

    def test_blocks_designs_and_headline(self):
        t, d = J["blocks"], J["designs"]
        self.assertEqual([t[k]["calls"] for k in "12345"], [270, 270, 270, 792, 216])
        for lv in ("central", "high"):
            for mo in ("nov", "dec"):
                core = sum(t[k][f"{lv}_{mo}"] for k in "123")
                self.assertAlmostEqual(core, d[f"core_{mo}"][lv])
                self.assertAlmostEqual(core + t["4"][f"{lv}_{mo}"] + t["5"][f"{lv}_{mo}"] + BG.JUDGE_RESERVE_USD,
                                       d[f"option_A_{mo}"][lv])
        self.assertEqual((d["core_nov"]["calls"], d["option_A_dec"]["calls"]), (810, 1818))
        self.assertEqual((round(d["core_nov"]["central"], 2), round(d["core_dec"]["central"], 2),
                          round(d["core_dec"]["high"], 2)), (33.44, 38.84, 121.80))

    def test_brand_question_option(self):
        o = J["brand_question_option"]
        self.assertFalse(o["any_fits"])
        self.assertAlmostEqual(o["core_high_dec"], J["designs"]["core_dec"]["high"])
        for r in o["subsets"]:
            self.assertFalse(r["fits_under_80_conservative_high"])
            self.assertAlmostEqual(r["smallest_budget_conservative_high"], o["core_high_dec"] + r["high_dec"])
        self.assertEqual([r["calls"] for r in o["subsets"]], [792, 216, 1008])

    def test_projection_and_guard(self):
        self.assertAlmostEqual(J["projection_by_design"]["core"]["nov"], 3.0)
        self.assertAlmostEqual(J["projection_by_design"]["core"]["dec"], 3.0)
        g = J["guard_core"]
        self.assertTrue(g["conservative_high_dec"]["projection_pause"])
        self.assertFalse(g["central_nov"]["projection_pause"])
        self.assertFalse(g["central_dec"]["projection_pause"])


class Reproduce(unittest.TestCase):
    def test_rerun_from_the_pinned_tag_reproduces_the_committed_json(self):
        if not REPO.exists():
            self.skipTest("v0.42 repository not present")
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "c"
            with contextlib.redirect_stdout(io.StringIO()):
                R3.main(["--repo", str(REPO), "--out", str(out)])
            self.assertEqual(json.loads(Path(str(out) + ".json").read_text(encoding="utf-8")), J)
            self.assertEqual(Path(str(out) + ".txt").read_text(encoding="utf-8"),
                             (HERE.parents[1] / "prereg" / "cost_estimate_v0_62_r3.txt").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
