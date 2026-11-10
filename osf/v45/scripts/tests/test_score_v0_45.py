#!/usr/bin/env python3
"""
Tests for score_v0_45.py and code_t5_v0_45.py on SYNTHETIC data only (outputs under /tmp). No model is called: the
successor judge is exercised with local fakes.
"""
import csv
import itertools
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace as NS

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import make_synthetic_t5 as MS     # noqa: E402
import score_v0_45 as SC           # noqa: E402
import code_t5_v0_45 as K          # noqa: E402
import numpy as np                 # noqa: E402

S = SC.S
C = SC.C
CFG = S.Cfg(200, 200)
T4_T0, T5_T0 = "2026-11-12T00:00:00+00:00", "2026-12-03T07:00:00+00:00"
FAB, GPT, GEM = MS.MODELS


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="v45_tests_", dir="/tmp"))
        cls.base = MS.base_maps(S.load_t3_table())
        b = cls.base
        cls.t4 = MS.wave(lambda m, c, r: MS.noisy(b[m], m, c, r, 4), cls.tmp / "t4", "t4", T4_T0)
        cls.t5_same = MS.wave(lambda m, c, r: MS.noisy(b[m], m, c, r, 5), cls.tmp / "t5s", "t5", T5_T0)
        shuf = {m: MS.M4.shuffled(b[m], 11) for m in MS.MODELS}
        cls.t5_shuf = MS.wave(lambda m, c, r: MS.noisy(shuf[m], m, c, r, 5), cls.tmp / "t5x", "t5", T5_T0)
        mix = {m: MS.M4.mixed(b[m], 0.5, 12) for m in MS.MODELS}
        cls.t5_mix = MS.wave(lambda m, c, r: MS.noisy(mix[m], m, c, r, 5), cls.tmp / "t5m", "t5", T5_T0)
        cls.t5_drop1 = MS.wave(lambda m, c, r: MS.noisy(b[m], m, c, r, 5), cls.tmp / "t5d1", "t5", T5_T0,
                               fail=lambda s: s["model"] == GEM and s["condition"] == "S0")
        cls.t5_drop2 = MS.wave(lambda m, c, r: MS.noisy(b[m], m, c, r, 5), cls.tmp / "t5d2", "t5", T5_T0,
                               fail=lambda s: s["model"] in (GEM, GPT) and s["condition"] == "S0")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)


class TestStability(Base):
    def test_stable_waves_confirm(self):
        out, rows = SC.score(self.t4, self.t5_same, CFG)
        v = out["verdicts"]
        self.assertEqual(v["H_Stab_Presence"]["verdict"], "CONFIRMED")
        self.assertEqual(v["H_Stab_Presence"]["n"], 112)
        self.assertEqual(v["H_Stab_Drift"]["verdict"], "CONFIRMED")
        self.assertEqual(v["H_Stab_Drift"]["n_splits"], 8000)
        self.assertIn(v["H_Stab_Consistency"]["verdict"], ("CONFIRMED", "PARTIAL"))
        self.assertEqual(len(rows), 112)
        self.assertEqual(out["parts"]["Ranking"]["verdict"], "PENDING")
        self.assertEqual(out["parts"]["Coverage"]["verdict"], "NOT MEASURED")

    def test_shuffled_t5_falsifies(self):
        out, _ = SC.score(self.t4, self.t5_shuf, CFG)
        v = out["verdicts"]
        self.assertEqual(v["H_Stab_Presence"]["verdict"], "FALSIFIED")
        self.assertEqual(v["H_Stab_Drift"]["verdict"], "FALSIFIED")
        self.assertLess(v["H_Stab_Drift"]["p_exact"], 0.01)

    def test_partial_order_change_is_drift_beyond_noise(self):
        out, _ = SC.score(self.t4, self.t5_mix, CFG)
        d = out["verdicts"]["H_Stab_Drift"]
        self.assertLess(d["p_exact"], 0.05)
        self.assertLess(d["SR"], 1.0)
        self.assertLess(out["verdicts"]["H_Stab_Presence"]["rho"], SC.score(self.t4, self.t5_same, CFG)[0]["verdicts"]["H_Stab_Presence"]["rho"])

    def test_one_model_dropped_reduced_panel(self):
        out, _ = SC.score(self.t4, self.t5_drop1, CFG)
        v = out["verdicts"]
        self.assertEqual(v["H_Stab_Presence"]["panel"], "reduced panel")
        self.assertEqual(v["H_Stab_Presence"]["models"], [FAB, GPT])
        self.assertEqual(v["H_Stab_Consistency"]["verdict"], "UNDETERMINED")
        self.assertIn("gemini-4-argon|S0", out["models_excluded"]["t5"])

    def test_two_models_dropped_undetermined(self):
        out, _ = SC.score(self.t4, self.t5_drop2, CFG)
        self.assertEqual(out["verdicts"]["H_Stab_Presence"]["verdict"], "UNDETERMINED")
        self.assertEqual(out["verdicts"]["H_Stab_Drift"]["verdict"], "UNDETERMINED")
        self.assertNotEqual(out["verdicts"]["H_Stab_Search_Presence"]["verdict"], "UNDETERMINED")

    def test_probe_parity_halts_on_changed_prompt(self):
        raw, A, B = self.t5_same
        raw2 = [dict(r) for r in raw]
        raw2[0]["prompt"] = raw2[0]["prompt"] + " (changed)"
        with self.assertRaises(SC.Halt):
            SC.score(self.t4, (raw2, A, B), CFG)

    def test_g3_t4_parity_against_v042_brand_table(self):
        w4 = SC.Wave(*self.t4, SC.brands_list(), "t4")
        rows = S.brand_rows(w4.D, S.load_t3_table(), w4.excl)     # v0.42's own brand-table writer
        d = self.tmp / "bt"
        S.write_outputs({"synthetic": True}, rows, d / "v.json", d / "bt.csv")
        out, _ = SC.score(self.t4, self.t5_same, CFG, extras={"t4_brand_table": d / "bt.csv"})
        self.assertTrue(out["manipulation_checks_t5"]["G3_t4_parity"]["pass"])
        with open(d / "bt.csv", newline="") as f:
            rd = list(csv.DictReader(f))
        rd[0]["pi_N3_S0"] = str(float(rd[0]["pi_N3_S0"]) + 0.01)
        with open(d / "bad.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rd[0]))
            w.writeheader()
            w.writerows(rd)
        with self.assertRaises(SC.Halt):
            SC.score(self.t4, self.t5_same, CFG, extras={"t4_brand_table": d / "bad.csv"})

    def test_mc_gap(self):
        out, _ = SC.score(self.t4, self.t5_same, CFG)
        g = out["manipulation_checks_t5"]["MC_Gap"]
        self.assertAlmostEqual(g["days"], 21 + 7 / 24, places=6)
        self.assertTrue(g["pass"])


class TestRules(unittest.TestCase):
    def test_verdict_rules(self):
        self.assertEqual(SC.verdict_stab(0.70, 0.049), "CONFIRMED")
        self.assertEqual(SC.verdict_stab(0.70, 0.05), "PARTIAL")
        self.assertEqual(SC.verdict_stab(0.69, 0.001), "PARTIAL")
        self.assertEqual(SC.verdict_stab(0.4999, 0.001), "FALSIFIED")
        self.assertEqual(SC.verdict_stab(float("nan"), 0.01), "UNDETERMINED")
        self.assertEqual(SC.verdict_phi(39, 0.9, 0.001), "UNDETERMINED")
        self.assertEqual(SC.verdict_phi(40, 0.50, 0.01), "CONFIRMED")
        self.assertEqual(SC.verdict_phi(40, 0.29, 0.01), "FALSIFIED")
        self.assertEqual(SC.verdict_drift(0.30, 0.95, 0.6), "CONFIRMED")
        self.assertEqual(SC.verdict_drift(0.01, 0.70, 0.6), "FALSIFIED")
        self.assertEqual(SC.verdict_drift(0.01, 0.85, 0.6), "PARTIAL")
        self.assertEqual(SC.verdict_drift(0.30, 0.85, 0.6), "PARTIAL")
        self.assertEqual(SC.verdict_drift(0.30, 0.99, 0.29), "UNDETERMINED")
        self.assertEqual(SC.verdict_component(29, 0.9, 0.001), "UNDETERMINED")
        self.assertEqual(SC.verdict_component(30, 0.5, 0.01), "CONFIRMED")
        self.assertEqual(SC.verdict_component(30, 0.29, 0.01), "FALSIFIED")
        self.assertEqual(SC.verdict_component(30, 0.4, 0.01), "PARTIAL")

    def test_exact_drift_enumeration(self):
        self.assertEqual(len(SC.SPLITS), 20)
        d = [np.arange(20, dtype=float)] * 3
        p, n = SC.exact_drift_p(d, 19.0)
        self.assertEqual(n, 8000)
        self.assertAlmostEqual(p, 1 / 8000)
        M = np.ones((6, 6))
        np.fill_diagonal(M, np.nan)
        for A in SC.SPLITS:
            self.assertAlmostEqual(SC.split_stats(M, A)[0], 0.0)
        # the observed split and its mirror give the same D, so with real data p >= 8/8000 = 0.001
        M2 = np.random.default_rng(1).uniform(0.3, 0.9, (6, 6))
        M2 = (M2 + M2.T) / 2
        self.assertAlmostEqual(SC.split_stats(M2, (0, 1, 2))[0], SC.split_stats(M2, (3, 4, 5))[0])


class TestLegs(Base):
    def _csv(self, name, vals):
        p = self.tmp / name
        with open(p, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["substrate", "brand", "value"])
            for (s, b), v in vals.items():
                w.writerow([s, b, "" if v is None else v])
        return p

    def test_component_leg_rules(self):
        brands = SC.brands_list()
        rng = np.random.default_rng(3)
        x = {k: float(rng.normal()) for k in brands}
        y = {k: x[k] + float(rng.normal(0, 0.3)) for k in brands}
        f4, f5 = self._csv("g4.csv", x), self._csv("g5.csv", y)
        r = SC.component_leg("Grounding", f4, f5, "PASS", CFG, brands)
        self.assertEqual(r["verdict"], "CONFIRMED")
        self.assertEqual(r["n"], 112)
        r = SC.component_leg("Grounding", f4, f5, "FAIL", CFG, brands)
        self.assertEqual(r["verdict"], "DESCRIPTIVE")
        few = {k: (v if i < 20 else None) for i, (k, v) in enumerate(x.items())}
        r = SC.component_leg("Grounding", self._csv("g4f.csv", few), f5, "PASS", CFG, brands)
        self.assertEqual(r["verdict"], "UNDETERMINED")
        self.assertEqual(SC.component_leg("Coverage", None, None, None, CFG, brands)["verdict"], "NOT MEASURED")

    def test_carried_ranking(self):
        p = self.tmp / "stage2.json"
        p.write_text(json.dumps({"verdicts": {"H3_Retest_Reliability": {"verdict": "CONFIRMED", "rho": 0.71, "n": 44,
                                                                           "p_perm": 0.0001, "p_shuffle": 0.0002}}}))
        r = SC.carried_ranking(p)
        self.assertEqual((r["verdict"], r["rho"], r["n"]), ("CONFIRMED", 0.71, 44))
        out, _ = SC.score(self.t4, self.t5_same, CFG, extras={"ranking_stage2": p})
        self.assertEqual(out["parts"]["Ranking"]["verdict"], "CONFIRMED")


class FakeInner:
    """Anthropic-like fake: records requests; returns a thinking block then a text block."""

    def __init__(self, level_for=lambda kw: "R2"):
        self.requests, self.level_for = [], level_for
        self.messages = self

    def create(self, **kw):
        self.requests.append(kw)
        return NS(content=[NS(type="thinking", thinking="..."), NS(type="text", text=self.level_for(kw))],
                  usage=NS(input_tokens=900, output_tokens=3), stop_reason="end_turn")


class TestJudge(unittest.TestCase):
    def test_coder_blob_pinned(self):
        ok, blob = K.coder_blob_ok()
        self.assertTrue(ok, blob)

    def test_sonnet_5_5_request_and_text_block(self):
        inner = FakeInner()
        cl = K.SuccessorJudgeClient(inner, "claude-sonnet-5-5")
        m = cl.messages.create(model="claude-sonnet-4-5", max_tokens=10, temperature=0.0, system="SYS",
                               messages=[{"role": "user", "content": "x"}])
        req = inner.requests[0]
        self.assertEqual(req["model"], "claude-sonnet-5-5")
        self.assertNotIn("temperature", req)
        self.assertEqual(req["extra_body"]["thinking"], {"type": "between_tools"})
        self.assertEqual(req["extra_body"]["output_config"], {"effort": "low"})
        self.assertEqual((req["max_tokens"], req["system"]), (10, "SYS"))
        self.assertEqual(m.content[0].text, "R2")
        self.assertEqual(cl.log[0]["input_tokens"], 900)

    def test_sonnet_4_6_request_unchanged_but_model(self):
        inner = FakeInner()
        cl = K.SuccessorJudgeClient(inner, "claude-sonnet-4-6")
        kw = dict(model="claude-sonnet-4-5", max_tokens=10, temperature=0.0, system="SYS",
                  messages=[{"role": "user", "content": "x"}])
        cl.messages.create(**kw)
        self.assertEqual(inner.requests[0], {**kw, "model": "claude-sonnet-4-6"})
        with self.assertRaises(ValueError):
            K.SuccessorJudgeClient(inner, "claude-opus-5-5")

    def test_j1_on_locked_t3_answers_with_fake(self):
        t3 = K.t3_v23_records()
        self.assertEqual(len(t3), 144)
        locked = {}
        for r in t3:
            locked.setdefault((r["brand_name"], r["response"][:3000]), r["_locked"])
        S23 = C._modules()["S23"]

        def echo(kw):     # a fake judge that returns the locked level for the same prompt
            content = kw["messages"][0]["content"]
            for (bn, resp), lvl in locked.items():
                if S23.JUDGE_USER_TEMPLATE.format(brand_name=bn, spirit_type=next(
                        x["spirit_type"] for x in t3 if x["brand_name"] == bn), response=resp) == content:
                    return lvl
            return "R0"
        t4 = [dict(r, _call_id=f"c{i}") for i, r in enumerate(t3[:72])]
        res = K.run_j1("claude-sonnet-5-5", FakeInner(echo), t3, t4)
        self.assertEqual(res["t3"]["binary_share"], 1.0)
        self.assertTrue(res["verdict"]["pass"])
        bad = K.run_j1("claude-sonnet-5-5", FakeInner(lambda kw: "R0"), t3, t4)
        self.assertFalse(bad["verdict"]["pass"])

    def test_agreement_and_rule(self):
        a = K.agreement([("R2", "R3"), ("R0", "R0"), ("R1", "R0"), ("R_ERR", "R2")])
        self.assertEqual((a["n"], a["binary_agree"], a["exact_agree"]), (3, 2, 1))
        t3 = {"n": 144, "binary_agree": 140, "r_err": 0}
        t4 = {"n": 72, "binary_agree": 66, "binary_share": 66 / 72, "r_err": 0}
        self.assertTrue(K.j1_verdict(t3, t4)["pass"])            # 206/216 = 0.954; t4 0.917
        t4b = {"n": 72, "binary_agree": 64, "binary_share": 64 / 72, "r_err": 0}
        self.assertFalse(K.j1_verdict(t3, t4b)["pass"])          # t4 0.889 < 0.90

    def test_code_t5_with_fake_judge(self):
        tmp = Path(tempfile.mkdtemp(prefix="v45_code_", dir="/tmp"))
        try:
            base = MS.base_maps(S.load_t3_table())
            raw, _, _ = MS.wave(lambda m, c, r: base[m], tmp, "t5", T5_T0)
            inner = FakeInner(lambda kw: "R3")
            A, B = K.code_t5(C.dedupe_calls(raw), "claude-sonnet-5-5", inner)
            v23 = [r for r in A if r["substrate"] == "v0.23"]
            self.assertEqual(len(v23), 72)
            self.assertTrue(all(r["recognized"] == 1 for r in v23))
            self.assertEqual(len(inner.requests), 72)
            A0, B0 = K.code_t5(C.dedupe_calls(raw))
            self.assertEqual(len([r for r in A0 if r["substrate"] == "v0.23"]), 0)
            self.assertEqual(len(B0), len(B))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=1)
