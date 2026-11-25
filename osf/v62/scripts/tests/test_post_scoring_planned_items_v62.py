"""Tests of post_scoring_planned_items_v62.py (DEVIATIONS Entry 7) on small synthetic inputs (no network, no model)."""
import sys
import unittest
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import post_scoring_planned_items_v62 as E  # noqa: E402
import score_v0_62 as S  # noqa: E402
from test_score_v0_62 import english, synth_rows, units  # noqa: E402


def rec(cid, lg="ko", m="gpt-6-astra", ph="B", status="ok", text="x", **kw):
    r = {"call_id": cid, "language": lg, "model_requested": m, "phase": ph, "status": status, "text": text,
         "error": None if status == "ok" else "ConnectTimeout", "served_model": m if status == "ok" else None,
         "finish_reason": "completed", "started_utc": "2026-11-25T06:00:00+00:00",
         "finished_utc": "2026-11-25T06:00:10+00:00", "usage_parts": [], "substrate": "v19"}
    r.update(kw)
    return r


class FinalRecords(unittest.TestCase):
    def test_last_answered_attempt_wins(self):
        lines = [rec("a", status="error", text=""), rec("a", text="answer"), rec("b", text="one"),
                 rec("b", status="error", text="")]
        f = E.final_records(lines)
        self.assertEqual(f["a"]["text"], "answer")
        self.assertEqual(f["b"]["text"], "one")          # a later failed attempt does not replace an answer
        self.assertTrue(E.answered(f["a"]))
        self.assertFalse(E.answered(rec("c", status="error", text="")))

    def test_unanswered_only(self):
        f = E.final_records([rec("a", status="error", text=""), rec("a", status="empty", text=" ")])
        self.assertEqual(f["a"]["status"], "empty")


class Rules(unittest.TestCase):
    def test_served(self):
        self.assertTrue(E.served_ok("gpt-6-astra", "gpt-6-astra"))
        self.assertTrue(E.served_ok("gpt-6-astra", "gpt-6-astra-2026-10-01"))
        self.assertTrue(E.served_ok("gemini-4-argon", "models/gemini-4-argon"))
        self.assertTrue(E.served_ok("claude-fable-5-2", "claude-fable-5-2-20261001"))
        self.assertFalse(E.served_ok("gpt-6-astra", "gpt-6-astra-mini"))
        self.assertFalse(E.served_ok("gpt-6-astra", "gpt-5"))
        self.assertIsNone(E.served_ok("gpt-6-astra", None))

    def test_truncation_and_refusal(self):
        for f in ("max_tokens", "FinishReason.MAX_TOKENS", "incomplete:max_output_tokens", "length"):
            self.assertTrue(E.truncated(f), f)
        for f in ("end_turn", "completed", "FinishReason.STOP", None, "lengthy"):
            self.assertFalse(E.truncated(f), f)
        self.assertTrue(E.refused("refusal"))
        self.assertTrue(E.refused("FinishReason.SAFETY"))
        self.assertFalse(E.refused("FinishReason.STOP"))

    def test_category_labels(self):
        self.assertEqual(E.category_label(0.80, [-0.01, 0.02]), "language-stable")
        self.assertEqual(E.category_label(0.70, [0.01, 0.02]), "level-shifted")
        self.assertEqual(E.category_label(0.95, [-0.05, -0.001]), "level-shifted")
        self.assertEqual(E.category_label(0.49, [-0.01, 0.02]), "language-sensitive")
        self.assertEqual(E.category_label(0.50, [-0.01, 0.02]), "intermediate")
        self.assertEqual(E.category_label(0.6999, [0.1, 0.2]), "intermediate")
        self.assertEqual(E.category_label(float("nan"), [0, 0]), "undetermined")

    def test_moved_share_strict(self):
        x = [0.0, 0.0, 0.0, 0.5]
        y = [1 / 6, 9 / 54, 10 / 54, 0.0]               # exactly 1/6 does not count
        share, n = E.moved_share(x, y)
        self.assertEqual(n, 2)
        self.assertAlmostEqual(share, 0.5)

    def test_rel3(self):
        self.assertAlmostEqual(E.rel3(0.5), 0.75)
        self.assertTrue(np.isnan(E.rel3(float("nan"))))


class Statistics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.U = units()
        rng = np.random.default_rng(5)
        cls.pi = {u: float(rng.uniform(0.05, 0.95)) for u in cls.U}
        _pi_en, cls.en = english(cls.U)
        cls.B = synth_rows(cls.U, cls.pi, 11)

    def test_rel1_identical_runs_is_one(self):
        B1 = [dict(r, run=1) for r in self.B if int(r["run"]) == 1]
        B3 = [dict(r, run=k, call_id=r["call_id"].replace("|1|", f"|{k}|", 1)) for k in (1, 2, 3) for r in B1]
        self.assertAlmostEqual(E.rel1(B3, self.U, S.MODELS[0]), 1.0)

    def test_rel1_in_range(self):
        r = E.rel1(self.B, self.U, S.MODELS[1])
        self.assertTrue(0.0 < r < 1.0)

    def test_per_category_and_pairs(self):
        V = {lg: S.unit_values(self.U, self.B) for lg in S.LANGS}
        keys = S.unit_set(self.U, "A")
        cat = E.per_category(keys, self.en, V, n_boot=200)
        self.assertEqual(len(cat), 15)
        t = S.rank_test({u: self.en[u]["pi"] for u in self.en}, {u: V["es"][u]["pi"] for u in V["es"]}, keys, 1, 10, 10)
        for c, r in t["per_category_rho_c"].items():           # equals the locked per-category value
            self.assertAlmostEqual(cat[f"es|{c}"]["rho_c"], r, places=12)
        pairs = E.language_pairs(keys, V, n_perm=20, n_boot=20)
        self.assertAlmostEqual(pairs["ES-KO"]["rho_c"], 1.0)    # identical tables
        top = E.top_shifts(keys, self.en, V, {})
        self.assertEqual(len(top["es"]["top"]), 10)
        a = [r["abs_shift"] for r in top["es"]["top"]]
        self.assertEqual(a, sorted(a, reverse=True))

    def test_per_model_and_phi_pi(self):
        keys = S.unit_set(self.U, "A")
        lang_B = {lg: self.B for lg in S.LANGS}
        pm = E.per_model_rho(self.U, keys, self.en, self.B, lang_B)
        for m in S.MODELS:                                     # same rows in "English" and L -> 1
            self.assertAlmostEqual(pm[f"es|{m}"]["i_same_model_english"]["rho_c"], 1.0)
        f = E.phi_pi_flag(self.U, keys, self.en, lang_B)
        self.assertIn("flag_abs_ge_0.50", f["ko"]["phi_L_defined"])

    def test_sensitivity_exclusion_and_drop_rule(self):
        keys = S.unit_set(self.U, "A")
        t0 = E.presence_on(self.U, keys, self.en, self.B, "es", n_perm=20, n_boot=20)
        ids = sorted({r["call_id"] for r in self.B if r["model"] == S.MODELS[0]})
        t1 = E.presence_on(self.U, keys, self.en, E.exclude_calls(self.B, ids[:2]), "es", n_perm=20, n_boot=20)
        self.assertNotEqual(t1["verdict"], "UNDETERMINED")
        t2 = E.presence_on(self.U, keys, self.en, E.exclude_calls(self.B, ids[:20]), "es", n_perm=20, n_boot=20)
        self.assertEqual(t2["verdict"], "UNDETERMINED")             # 70 of 90 calls < 90%
        self.assertEqual(t0["n"], 112)


class Descriptives(unittest.TestCase):
    def test_recognition(self):
        A = [{"model": "gpt-6-astra", "condition": "S0", "substrate": "v0.19", "label": "yes", "recognized": "1"},
             {"model": "gpt-6-astra", "condition": "S0", "substrate": "v0.20", "label": "no", "recognized": "0"},
             {"model": "gpt-6-astra", "condition": "S0", "substrate": "v0.23", "label": "R3", "recognized": "1"},
             {"model": "gpt-6-astra", "condition": "S1", "substrate": "v0.19", "label": "yes", "recognized": "1"}]
        r = E.recognition(A, models=["gpt-6-astra"])["gpt-6-astra"]
        self.assertEqual((r["recognized"], r["coded_answers"]), (1, 2))
        self.assertAlmostEqual(r["share"], 0.5)

    def test_mention_scripts(self):
        import code_v0_62 as C
        rx = {("v0.19", "Sony"): [C.alias_regex("소니", "ko")]}
        prim = [{"call_id": c, "substrate": "v0.19", "brand": "Sony", "model": "gpt-6-astra", "mentioned": m}
                for c, m in (("a", "1"), ("b", "1"), ("c", "1"), ("d", "0"))]
        lat = [{"call_id": c, "substrate": "v0.19", "brand": "Sony", "mentioned": m}
               for c, m in (("a", "1"), ("b", "0"), ("c", "1"), ("d", "0"))]
        texts = {"a": "Sony WH-1000", "b": "소니의 헤드폰", "c": "소니 (Sony)", "d": "없음"}
        out = E.mention_scripts(prim, lat, texts, rx)["all_models"]
        self.assertEqual((out["latin_only"], out["native_only"], out["both"]), (1, 1, 1))
        self.assertAlmostEqual(out["share_with_latin_form"], 2 / 3)

    def test_manipulation_checks_small(self):
        lines = [rec("a", status="error", text="", usage_parts=[]),
                 rec("a", text="소니 헤드폰", usage_parts=[{"mode": "standard", "condition": "S0", "input_tokens": 10,
                                                        "output_tokens": 100}]),
                 rec("b", text="English only answer here", finish_reason="length")]
        final = E.final_records(lines)
        prepared = {"a": {"call_id": "a", "language": "ko", "phase": "B", "in_language": True, "zh_traditional": None},
                    "b": {"call_id": "b", "language": "ko", "phase": "B", "in_language": False, "zh_traditional": None}}
        mc = E.manipulation_checks(lines, final, prepared, {"approvals": {}}, [], ["2026-11-25", "2026-12-02"])
        self.assertEqual(mc["MC_Complete"]["answered"], 2)
        self.assertEqual(mc["MC_Language"]["per_model_language"]["ko|gpt-6-astra|B"]["in_language"], 1)
        self.assertTrue(mc["MC_Language"]["per_model_language"]["ko|gpt-6-astra|B"]["flag_below_95pct"])
        self.assertEqual(mc["MC_Truncation"]["per_model_language"]["ko|gpt-6-astra"]["at_cap"], 1)
        self.assertTrue(mc["MC_Served"]["pass"])
        self.assertAlmostEqual(mc["MC_Budget"]["spend_from_recorded_usage_usd"], (10 * 10 + 100 * 50) / 1e6)
        self.assertTrue(mc["MC_Window"]["pass_within_72h"])

    def test_no_collision_aliaser_removes_only_collision_prone(self):
        import code_v0_62 as C
        al, n = E.no_collision_aliaser()
        self.assertEqual(n, sum(1 for r in C.load_aliases() if r[4]))
        self.assertFalse(any(r[4] for r in al.rows))
        self.assertEqual(al.canonicalise("코스 헤드폰", "v19").strip(), "코스 헤드폰")   # Koss alias off


if __name__ == "__main__":
    unittest.main()
