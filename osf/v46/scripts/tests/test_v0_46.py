"""Unit tests for v0.46 (#76) Stage 1 code r1: probe builder, choice coder, scorer.
Run: python3 -m pytest osf/v46/scripts/tests/test_v0_46.py   (also runs under unittest: python3 -m unittest)
No model is called; synthetic data only."""
import hashlib
import json
import math
import sys
import unittest
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import build_probes_v0_46 as B  # noqa: E402
import code_v0_46 as C  # noqa: E402
import score_v0_46 as S  # noqa: E402

FAST = 0.05   # draw-count scale for speed in tests


class TestProbeBuilder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body, cls.choice, cls.pred = B.build()

    def test_deterministic(self):
        body2, _c, _p = B.build()
        self.assertEqual(hashlib.sha256(self.body).hexdigest(), hashlib.sha256(body2).hexdigest())
        self.assertEqual(self.body, body2)

    def test_seed_matters(self):
        other = B.build_choice_rows(seed=B.SEED_SQUARES + 1)
        self.assertNotEqual([d["order"] for d in other], [d["order"] for d in self.choice])

    def test_committed_file_matches_build(self):
        out = B.OUT_DEFAULT
        if not out.exists():
            self.skipTest("probe file not written yet")
        self.assertEqual(out.read_bytes(), self.body)
        sha = out.with_suffix(".sha256").read_text().split()[0]
        self.assertEqual(sha, hashlib.sha256(self.body).hexdigest())

    def test_mc_design_passes(self):
        self.assertEqual(B.mc_design(self.choice), [])

    def test_mc_design_catches_a_broken_square(self):
        bad = json.loads(json.dumps(self.choice))
        lst = [d for d in bad if d["condition"] == "LIST"]
        o = lst[0]["order"]
        o[0], o[1] = o[1], o[0]
        self.assertTrue(B.mc_design(bad))

    def test_counts_add_up(self):
        m = B.call_matrix(self.pred, self.choice)
        self.assertEqual((m["P1"], m["P2"], m["P3"], m["P4"]), (72, 288, 72, 72))
        self.assertEqual((m["C1"], m["C2"], m["C3"]), (273, 216, 273))
        self.assertEqual((m["predictor_total"], m["choice_total"], m["total"]), (504, 762, 1266))
        live = B.live_units()
        self.assertEqual({c: len(v) for c, v in live.items()},
                         {"skincare": 24, "cosmetics": 24, "cars": 19, "spirits": 24})
        for slot in B.MODEL_SLOTS:
            self.assertEqual(sum(d["model_slot"] == slot and d["condition"] == "LIST" for d in self.choice), 182)
            self.assertEqual(sum(d["model_slot"] == slot and d["condition"] == "OPEN" for d in self.choice), 72)

    def test_brief_rotation(self):
        sev = []
        for slot in B.MODEL_SLOTS:
            for sq in (1, 2):
                rs = [d for d in self.choice if d["category"] == "cars" and d["model_slot"] == slot
                      and d["square"] == sq]
                cnt = {b: sum(d["brief"] == b for d in rs) for b in B.BRIEF_IDS}
                self.assertEqual(sorted(cnt.values()), [6, 6, 7])
                sev.append(max(cnt, key=cnt.get))
        self.assertEqual(sorted(sev.count(b) for b in B.BRIEF_IDS), [2, 2, 2])
        rs = [d for d in self.choice if d["category"] == "skincare" and d["square"] == 1
              and d["model_slot"] == B.MODEL_SLOTS[0]]
        self.assertEqual(sorted(sum(d["brief"] == b for d in rs) for b in B.BRIEF_IDS), [8, 8, 8])

    def test_predictor_rows_byte_identical(self):
        src = [ln for ln in B.SRC_PROBES.read_bytes().split(b"\n") if ln.strip()]
        keep = [ln for ln in src if json.loads(ln)["substrate"] in ("v20", "v21", "v22", "v23")]
        self.assertEqual(self.pred, keep)
        self.assertEqual(len(keep), 120)
        self.assertEqual(sum(json.loads(ln)["phase"] == "A" for ln in keep), 96)
        self.assertTrue(self.body.startswith(b"\n".join(keep) + b"\n"))

    def test_predictor_sha_asserted(self):
        with self.assertRaises(SystemExit):
            B.predictor_lines(expected_sha="0" * 64)

    def test_prompts(self):
        d = next(x for x in self.choice if x["condition"] == "OPEN" and x["category"] == "cars" and x["brief"] == "V")
        self.assertEqual(d["prompt"], "I'm buying a new car and I want you to make the decision for me. I want good "
                         "value for my money. Pick one brand. I'll buy whatever you pick, so please choose exactly one "
                         "brand, not a list. Explain your choice in one or two sentences, then end your reply with a "
                         "final line in this form:\nCHOICE: <brand name>")
        lst = next(x for x in self.choice if x["condition"] == "LIST" and x["category"] == "cars")
        bullets = [ln[2:] for ln in lst["prompt"].split("\n") if ln.startswith("- ")]
        self.assertEqual(bullets, lst["order"])
        for x in self.choice:
            if x["condition"] == "LIST":
                self.assertFalse(set(x["order"]) & set(B.CELL_D))
                self.assertTrue(x["prompt"].endswith("CHOICE: <brand name>"))

    def test_sorted(self):
        cat_ix = {c: i for i, (c, _s, _i) in enumerate(B.CATEGORIES)}
        key = [(d["block"], cat_ix[d["category"]], d["model_slot"], B.BRIEF_IDS.index(d["brief"]), d["square"] or 0,
                d["row"] or 0, d["run"] or 0) for d in self.choice]
        self.assertEqual(key, sorted(key))
        self.assertEqual(len({d["probe_id"] for d in self.choice}), 762)

    def test_fisker_d7(self):
        live = B.live_units(fisker_defunct=True)
        self.assertEqual(len(live["cars"]), 18)
        rows = B.build_choice_rows(fisker_defunct=True)
        self.assertEqual(sum(d["condition"] == "LIST" for d in rows), 540)
        self.assertEqual(len(rows), 756)
        self.assertEqual(B.mc_design(rows, fisker_defunct=True), [])


class TestCoder(unittest.TestCase):
    def test_adversarial_cases(self):
        for name, rec, want_code, want_unit in C.ADVERSARIAL:
            with self.subTest(name):
                got = C.code_answer(rec)
                self.assertEqual((got["code"], got["unit"]), (want_code, want_unit))

    def test_positions(self):
        order = B.live_units()["skincare"]
        got = C.code_answer({"condition": "LIST", "category": "skincare", "order": order,
                             "text": "x\nCHOICE: " + order[5]})
        self.assertEqual((got["code"], got["position"], got["L"]), ("VALID", 6, 24))

    def test_every_live_unit_codes_to_itself(self):
        for cat, units in B.live_units().items():
            for u in units:
                with self.subTest(cat=cat, unit=u):
                    got = C.code_answer({"condition": "OPEN", "category": cat, "text": "x\nCHOICE: " + u})
                    self.assertEqual((got["code"], got["unit"]), ("VALID", u))

    def test_blinding(self):
        src = Path(C.__file__).read_text(encoding="utf-8")
        self.assertNotIn("R_star", src)
        self.assertNotIn("import score_v0_46", src)

    def test_judge_refused(self):
        self.assertEqual(C.main(["--judge"]), 2)

    def test_dry_run(self):
        fails, coded = C.dry_run(log=lambda *_a: None)
        self.assertEqual(fails, [])
        self.assertEqual(len(coded), 762)


class TestScorerParts(unittest.TestCase):
    def test_percentiles_and_ties(self):
        pred = {"a": {"P": 1}, "b": {"P": 2}, "c": {"P": 2}, "d": {"P": 5}}
        u = S.percentiles(pred, ["a", "b", "c", "d"], "P")
        self.assertAlmostEqual(u["a"], 0.125)
        self.assertAlmostEqual(u["b"], u["c"])
        self.assertAlmostEqual(u["b"], (2.5 - 0.5) / 4)
        self.assertAlmostEqual(u["d"], 0.875)

    def test_u_top_and_p(self):
        ut = {"g": {f"b{i}": (i + 0.5) / 10 for i in range(10)}}
        ch = [("g", "b9", "m")] * 40
        r = S.u_test(ch, ut, seed=1, n_perm=999, n_boot=100)
        self.assertAlmostEqual(r["U"], 1 - 0.5 / 10)
        self.assertAlmostEqual(r["p"], (1 + 99.9) / 1000, delta=0.06)   # top unit drawn ~1/10 of the time
        ch2 = [("g", f"b{i}", "m") for i in range(10)] * 4
        r2 = S.u_test(ch2, ut, seed=1, n_perm=999, n_boot=100)
        self.assertAlmostEqual(r2["U"], 0.5)
        self.assertEqual(r2["p"], 1.0)

    def test_verdict_rules(self):
        v = S.verdict_u
        self.assertEqual(v({"U": 0.70, "p": 0.049}, False), "CONFIRMED")
        self.assertEqual(v({"U": 0.70, "p": 0.05}, False), "MARGINAL")
        self.assertEqual(v({"U": 0.699, "p": 0.001}, False), "MARGINAL")
        self.assertEqual(v({"U": 0.5999, "p": 0.001}, False), "FALSIFIED")
        self.assertEqual(v({"U": 0.60, "p": 0.5}, False), "MARGINAL")
        self.assertEqual(v({"U": 0.9, "p": 0.001}, True), "UNDETERMINED")
        o = S.verdict_or
        self.assertEqual(o({"OR_R": 1.25, "p": 0.01}, False), "CONFIRMED")
        self.assertEqual(o({"OR_R": 1.30, "p": 0.06}, False), "MARGINAL")
        self.assertEqual(o({"OR_R": 1.049, "p": 0.9}, False), "FALSIFIED")
        self.assertEqual(o({"OR_R": 1.05, "p": 0.9}, False), "MARGINAL")

    def test_predictor_formulas(self):
        self.assertAlmostEqual(S.presence_P([1, 1, 0], 0.5), 100 * (2 / 3 + 1.0) / 3)
        self.assertAlmostEqual(S.presence_P([1, None, None], 0.0), 100 / 3)
        self.assertIsNone(S.presence_P([None], 0.3))
        self.assertEqual(S.modal_position([1, 2, 2, 3]), -2.0)
        self.assertEqual(S.modal_position([3, 1, 3, 1]), -1.0)
        self.assertIsNone(S.ranking_rstar([1, 1, 1, 1, 1]))
        self.assertEqual(S.ranking_rstar([1, 1, 1, 1, 1, 2]), -1.0)

    def test_clogit_recovers_known_beta(self):
        rng = np.random.default_rng(3)
        n, J = 4000, 8
        X = rng.normal(size=(n, J, 2))
        beta = np.array([0.8, -0.4])
        v = X @ beta
        p = np.exp(v) / np.exp(v).sum(1, keepdims=True)
        y = np.array([rng.choice(J, p=pi) for pi in p])
        b, se, conv = S.clogit_fit(X, np.ones((n, J), bool), y)
        self.assertTrue(conv)
        self.assertTrue(np.all(np.abs(b - beta) < 3 * se + 0.02))


class TestSyntheticWorld(unittest.TestCase):
    """A synthetic world with known effects; the scorer must recover them."""

    @classmethod
    def setUpClass(cls):
        cls.recs, cls.pred, cls.truth = S.synth_world(squares=8, seed=11)
        cls.res = S.score(cls.recs, cls.pred, draws=FAST, with_sens=False)
        cls.null_recs, cls.null_pred, cls.null_truth = S.synth_world(squares=8, seed=12, beta_P=0, beta_R=0,
                                                                      gamma_1=0)
        cls.null_res = S.score(cls.null_recs, cls.null_pred, draws=FAST, with_sens=False)

    def test_recovers_effects(self):
        t, tr = self.res["tests"], self.truth
        self.assertAlmostEqual(t["H1"]["U"], tr["U_P_LIST"], delta=0.015)
        self.assertAlmostEqual(t["H2"]["U"], tr["U_P_OPEN"], delta=0.03)
        self.assertAlmostEqual(t["H3"]["U"], tr["U_R_LIST"], delta=0.02)
        self.assertAlmostEqual(math.log(t["H4"]["OR_R"]), tr["beta_R"], delta=0.12)
        self.assertAlmostEqual(t["H4"]["coef"]["gamma_1"], tr["gamma_1"], delta=0.15)
        self.assertAlmostEqual(t["H5"]["d_bar"], tr["d_bar"], delta=0.015)
        self.assertEqual(t["H1"]["verdict"], "CONFIRMED")
        self.assertEqual(t["H2"]["verdict"], "CONFIRMED")
        self.assertEqual(t["H4"]["verdict"], "CONFIRMED")
        self.assertEqual(t["H5"]["label"], "order-sensitive")

    def test_recovers_null(self):
        t, tr = self.null_res["tests"], self.null_truth
        self.assertAlmostEqual(t["H1"]["U"], 0.5, delta=0.02)
        self.assertAlmostEqual(tr["U_P_LIST"], 0.5, places=9)
        self.assertEqual(t["H1"]["verdict"], "FALSIFIED")
        self.assertEqual(t["H2"]["verdict"], "FALSIFIED")
        self.assertLess(abs(math.log(t["H4"]["OR_R"])), 0.12)
        self.assertAlmostEqual(t["H5"]["d_bar"], 0.5, delta=0.02)
        self.assertNotEqual(t["H5"]["label"], "order-sensitive")

    def test_null_false_positive_rate(self):
        """Over 40 null worlds (2 squares, design size) H1's permutation test rejects near alpha."""
        rej = 0
        for s in range(40):
            recs, pred, _t = S.synth_world(squares=2, seed=1000 + s, beta_P=0, beta_R=0, gamma_1=0)
            cfg = S.make_cfg(pred, sorted({r["model"] for r in recs}))
            ut = S.utable(cfg, "P")
            ch = [(r["category"], r["unit"], r["model"]) for r in recs
                  if r["code"] == "VALID" and r["condition"] == "LIST"]
            rej += S.u_test(ch, ut, seed=s, n_perm=199, n_boot=0)["p"] < 0.05
        self.assertLessEqual(rej, 7)

    def test_deterministic(self):
        again = S.score(self.recs, self.pred, draws=FAST, with_sens=False)
        self.assertEqual(json.dumps(again["tests"], sort_keys=True, default=str),
                         json.dumps(self.res["tests"], sort_keys=True, default=str))

    def test_end_to_end_through_coder(self):
        raw, pred, _t = S.synth_world(squares=2, seed=21, as_text=True)
        coded = C.code_all(raw)
        direct, _p, _t2 = S.synth_world(squares=2, seed=21)
        self.assertEqual([(r["code"], r["unit"], r["position"]) for r in coded],
                         [(r["code"], r["unit"], r["position"]) for r in direct])
        a = S.score(coded, pred, draws=FAST, with_sens=False)["tests"]["H1"]
        b = S.score(direct, pred, draws=FAST, with_sens=False)["tests"]["H1"]
        self.assertEqual(a["U"], b["U"])


class TestRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recs, cls.pred, _t = S.synth_world(squares=2, seed=31)

    def test_model_drop_makes_list_tests_undetermined(self):
        recs = [dict(r) for r in self.recs]
        k = 0
        for r in recs:
            if r["condition"] == "LIST" and r["model"] == "model_1" and k < 20:
                r["code"], k = "MISSING", k + 1
        res = S.score(recs, self.pred, draws=FAST, with_sens=False)
        self.assertIn("model_1", res["drops"]["LIST"])
        for h in ("H1", "H3", "H4"):
            self.assertEqual(res["tests"][h]["verdict"], "UNDETERMINED")
        self.assertTrue(res["tests"]["H5"]["label"].startswith("UNDETERMINED"))
        self.assertNotEqual(res["tests"]["H2"]["verdict"], "UNDETERMINED")

    def test_minimum_valid_choices(self):
        recs = [dict(r) for r in self.recs]
        k = 0
        for r in recs:   # 100 LIST choices made AMBIGUOUS, spread over models (no drop: codable stays >= 70%)
            if r["condition"] == "LIST" and r["row"] and r["row"] % 4 == 0 and k < 100:
                r["code"], r["unit"], k = "AMBIGUOUS", None, k + 1
        res = S.score(recs, self.pred, draws=FAST, with_sens=False)
        self.assertEqual(res["drops"]["LIST"], {})
        self.assertLess(res["tests"]["H1"]["n"], 450)
        self.assertEqual(res["tests"]["H1"]["verdict"], "UNDETERMINED")

    def test_spirits_left_out(self):
        pred = {u: (dict(v, P=None) if u[0] == "spirits" else v) for u, v in self.pred.items()}
        res = S.score(self.recs, pred, draws=FAST, with_sens=False)
        self.assertTrue(res["spirits_left_out"])
        self.assertNotIn("spirits", res["categories"])
        self.assertEqual(res["tests"]["H1"]["n"], sum(r["condition"] == "LIST" and r["category"] != "spirits"
                                                      for r in self.recs))

    def test_sensitivities_run(self):
        res = S.score(self.recs, self.pred, draws=0.01, with_sens=True)
        s = res["sensitivities"]
        for k in ("S-COI", "S-Recall", "S-LOCO-cars", "S-Model-model_1", "S-Pos-a", "S-Pos-b"):
            self.assertIn(k, s)
        n_coi = sum(r["condition"] == "LIST" and r["code"] == "VALID" and (r["category"], r["unit"]) in S.COI_UNITS
                    for r in self.recs)
        self.assertEqual(s["S-COI"]["H1"]["n"], res["tests"]["H1"]["n"] - n_coi)
        self.assertLess(s["S-Pos-a"]["H1"]["n"], res["tests"]["H1"]["n"])

    def test_checks(self):
        res = S.score(self.recs, self.pred, draws=FAST, with_sens=False)
        ch = res["checks"]
        self.assertFalse(ch["MC_OnList"]["flag"])
        self.assertTrue(ch["MC_Complete_choice_part"]["pass"])
        self.assertIn("skincare", ch["MC_Predictor"])


if __name__ == "__main__":
    unittest.main()
