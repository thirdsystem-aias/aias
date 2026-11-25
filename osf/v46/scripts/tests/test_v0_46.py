"""Unit tests for v0.46 (#76) Stage 1 code r1: probe builder, choice coder, scorer.
Run: python3 -m pytest osf/v46/scripts/tests/test_v0_46.py   (also runs under unittest: python3 -m unittest)
No model is called; synthetic data only."""
import hashlib
import json
import math
import sys
import unittest
from collections import Counter
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
        # r4: D7 = cell_d (record of 2026-11-24): Fisker in Cell D (Fisker live it was 273 / 762 / 1,266, cars 19)
        self.assertEqual((m["C1"], m["C2"], m["C3"]), (270, 216, 270))
        self.assertEqual((m["predictor_total"], m["choice_total"], m["total"]), (504, 756, 1260))
        live = B.live_units()
        self.assertEqual({c: len(v) for c, v in live.items()},
                         {"skincare": 24, "cosmetics": 24, "cars": 18, "spirits": 24})
        for slot in B.MODEL_SLOTS:
            self.assertEqual(sum(d["model_slot"] == slot and d["condition"] == "LIST" for d in self.choice), 180)
            self.assertEqual(sum(d["model_slot"] == slot and d["condition"] == "OPEN" for d in self.choice), 72)

    def test_brief_rotation(self):
        sev = []
        live19 = B.build_choice_rows(fisker_defunct=False)    # r4: the uneven case (L = 19) needs Fisker live
        for slot in B.MODEL_SLOTS:
            for sq in (1, 2):
                rs18 = [d for d in self.choice if d["category"] == "cars" and d["model_slot"] == slot
                        and d["square"] == sq]
                self.assertEqual(sorted(sum(d["brief"] == b for d in rs18) for b in B.BRIEF_IDS), [6, 6, 6])
                rs = [d for d in live19 if d["category"] == "cars" and d["model_slot"] == slot
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
        self.assertEqual(len({d["probe_id"] for d in self.choice}), 756)

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
        self.assertEqual(len(coded), 756)

    def test_google_enum_finish_reasons(self):
        # r3 task 1: str(google FinishReason) is "FinishReason.MAX_TOKENS"; it must count as a length stop
        base = {"condition": "OPEN", "category": "cars"}
        for fr in ("MAX_TOKENS", "FinishReason.MAX_TOKENS"):
            with self.subTest(fr=fr):
                cut = C.code_answer(dict(base, text="Let me think about Toyota", finish_reason=fr))
                self.assertEqual((cut["code"], cut["reason"], cut["at_limit"]), ("MISSING", "cut_at_limit", True))
                kept = C.code_answer(dict(base, text="x\nCHOICE: Ford", finish_reason=fr))
                self.assertEqual((kept["code"], kept["unit"], kept["at_limit"]), ("VALID", "Ford", True))
        self.assertFalse(C.at_length_limit({"finish_reason": "FinishReason.STOP", "output_tokens": 99999}))
        self.assertTrue(C.is_refusal({"finish_reason": "FinishReason.SAFETY"}))
        self.assertEqual(C.norm_finish_reason("FinishReason.MAX_TOKENS"), "MAX_TOKENS")
        import acquire_v0_46 as A
        self.assertLessEqual(set(A.LENGTH_STOPS), C.LENGTH_STOPS)    # coder and acquisition agree

    def test_list_refusal_without_choice_line_is_off_list(self):
        # r3 task 2: LIST + explicit refusal in the text + no CHOICE line -> OFF_LIST (reason refusal_text)
        lst = {"condition": "LIST", "category": "cars", "order": ["Tesla", "Toyota", "Honda"]}
        for t in ("I'm sorry, but I can't choose a car for you.\nPlease weigh these yourself.",
                  "As an assistant I would rather not pick one brand.\nEach has strengths.",
                  "I am unable to make that decision for you.",
                  "I must respectfully decline.\n...",
                  "**I cannot select** a brand for you.\nGood luck."):
            with self.subTest(t=t):
                got = C.code_answer(dict(lst, text=t))
                self.assertEqual((got["code"], got["reason"], got["unit"]), ("OFF_LIST", "refusal_text", None))
        # not a refusal_text case: a CHOICE line is present, a registry unit is on the last line, OPEN, provider stop
        self.assertEqual(C.code_answer(dict(lst, text="I can't choose for you.\nCHOICE:"))["code"], "NONE")
        self.assertEqual(C.code_answer(dict(lst, text="I can't choose for you, but most pick:\nHonda"))["code"],
                         "VALID")
        self.assertEqual(C.code_answer({"condition": "OPEN", "category": "cars",
                                        "text": "I can't choose a car for you."})["code"], "OTHER")
        prov = C.code_answer(dict(lst, text="I can't choose.", finish_reason="refusal"))
        self.assertEqual((prov["code"], prov["reason"]), ("NONE", "refusal"))
        # a non-refusal sentence on a LIST answer without CHOICE line keeps the old path (OFF_LIST, no reason)
        plain = C.code_answer(dict(lst, text="Hard to say.\nIt depends on your needs."))
        self.assertEqual((plain["code"], plain["reason"]), ("OFF_LIST", None))


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


# =========================================================================== predictors (task 1, Stage 1 code r2)
import predictors_v0_46 as PR  # noqa: E402

SYN_MODELS = ["mA", "mB", "mC"]


def _raw_b(model, run, frame, text, status="ok"):
    return {"call_id": f"v20|B|{frame}|{model}|S0|{run}", "substrate": "v20", "phase": "B", "probe_id": frame,
            "frame_id": frame, "model_requested": model, "served_model": model, "condition": "S0", "run": run,
            "text": text, "status": status, "error": None}


def synthetic_predictor_world():
    """v0.20 only. 3 models x 3 runs x 2 frames = 18 Phase B answers. CeraVe is listed first in every answer,
    La Mer second in 17, Lancome third in the 9 q1 answers; Sisley second once (below the rating floor)."""
    raw, cb, ca = [], [], []
    for m in SYN_MODELS:
        for run in (1, 2, 3):
            for fr in ("q1", "q2"):
                if fr == "q1":
                    lines = ["1. CeraVe", "2. La Mer", "3. Lancôme"]
                else:
                    lines = ["1. CeraVe", "2. Sisley"] if (m, run) == ("mA", 1) else ["1. CeraVe", "2. La Mer"]
                text = "Here are my picks:\n" + "\n".join(lines)
                r = _raw_b(m, run, fr, text)
                raw.append(r)
                named = [ln.split(". ", 1)[1] for ln in lines]
                for b in ("CeraVe", "La Mer", "Lancôme", "Sisley", "La Prairie"):
                    cb.append({"call_id": r["call_id"], "substrate": "v0.20", "brand": b, "model": m,
                               "condition": "S0", "run": run, "probe_id": fr, "frame_id": fr,
                               "mentioned": int(b in named)})
    for m, recog in zip(SYN_MODELS, (1, 1, 0)):
        for b in ("CeraVe", "La Mer"):
            ca.append({"call_id": f"v20|A|{b}|{m}|S0|1", "substrate": "v0.20", "brand": b, "brand_id": b,
                       "model": m, "condition": "S0", "run": 1, "probe_id": b, "label": "yes",
                       "recognized": recog if b == "CeraVe" else 1})
    return raw, ca, cb


class TestSamsungGroupOpen(unittest.TestCase):
    """r6 (author's decision 2026-11-24; DEVIATIONS Entry 0 item (b)): an OPEN choice of any Samsung-group brand
    (Samsung, Harman and its brands) is coded and reported but excluded from every test."""

    @classmethod
    def setUpClass(cls):
        cls.recs, cls.pred, _t = S.synth_world(squares=2, seed=31)

    @staticmethod
    def open_rec(cat, line, cond="OPEN", **kw):
        return dict({"condition": cond, "category": cat, "text": f"A good pick.\nCHOICE: {line}"}, **kw)

    def test_terms_are_v062_samsung_and_harman_terms(self):
        # the r0 terms of v0.62's screen as recorded by the v0.46 re-run (osf/v46/data/coi_screen_v0_46_r1.txt):
        # Samsung, Harman and its audio brands, the Sound United brands (Masimo, the seller, left out), before Cheil
        txt = (HERE.parent.parent / "data" / "coi_screen_v0_46_r1.txt").read_text(encoding="utf-8")
        r0 = [ln for ln in txt.splitlines() if ln.startswith("terms r0: ")][0][len("terms r0: "):].split("; ")
        want = tuple(t for t in r0[:r0.index("Cheil")] if t != "Masimo")
        self.assertEqual(C.SAMSUNG_GROUP_TERMS, want)
        self.assertEqual(len(C.SAMSUNG_GROUP_TERMS), 21)

    def test_coder_flags_open_choices_and_keeps_the_code(self):
        cases = [("cars", "JBL", "OTHER", None, "JBL"), ("cosmetics", "Samsung", "OTHER", None, "Samsung"),
                 ("cars", "Harman Kardon", "OTHER", None, "Harman"),
                 ("spirits", "**Bowers & Wilkins**", "OTHER", None, "Bowers & Wilkins"),
                 ("skincare", "Classé", "OTHER", None, "Classé"),
                 ("cars", "Samsung SDI", "OTHER", None, "Samsung"),
                 ("cars", "BMW with the Harman Kardon sound system", "VALID", "BMW", "Harman"),
                 ("cars", "Denon (https://www.denon.com)", "OTHER", None, "Denon")]
        for cat, line, code, unit, term in cases:
            with self.subTest(line=line):
                got = C.code_answer(self.open_rec(cat, line))
                self.assertEqual((got["code"], got["unit"], got["samsung_group"]), (code, unit, term))

    def test_coder_does_not_flag(self):
        none_cases = [self.open_rec("cars", "Toyota"),
                      {"condition": "OPEN", "category": "cars", "text": "Samsung makes my phone.\nCHOICE: Toyota"},
                      self.open_rec("cars", "Polkadot Motors"), self.open_rec("cars", "denon"),
                      self.open_rec("cars", "Masimo"),
                      self.open_rec("cars", "JBL", cond="LIST", order=["Tesla", "Toyota"])]
        for rec in none_cases:
            with self.subTest(text=rec["text"], cond=rec["condition"]):
                self.assertIsNone(C.code_answer(rec)["samsung_group"])
        self.assertEqual(C.code_answer(none_cases[-1])["code"], "OFF_LIST")
        for cat, units in B.live_units().items():   # no live unit is a Samsung-group name (screen r1: 0 matches)
            for u in units:
                self.assertIsNone(C.samsung_group_term(u), (cat, u))

    def _flag(self, n):
        recs = [dict(r) for r in self.recs]
        k = 0
        for r in recs:
            if r["condition"] == "OPEN" and r["code"] == "VALID" and k < n:
                if k % 2:
                    r["samsung_group"] = "Harman"          # coder flag (r6)
                else:
                    r["choice_line"] = f"{r['unit']} with JBL audio"   # record coded before r6: no flag field
                k += 1
        return recs, k

    def test_scorer_excludes_from_every_test_and_reports(self):
        base = S.score(self.recs, self.pred, draws=0.01, with_sens=True)
        recs, k = self._flag(10)
        self.assertEqual(k, 10)
        res = S.score(recs, self.pred, draws=0.01, with_sens=True)
        self.assertEqual(res["tests"]["H2"]["n"], base["tests"]["H2"]["n"] - 10)
        self.assertEqual(res["tests"]["H1"]["n"], base["tests"]["H1"]["n"])
        flagged_by_model = Counter(S.mkey(r) for r in recs if S.samsung_group(r))
        for m, n in flagged_by_model.items():
            self.assertEqual(res["sensitivities"][f"S-Model-{m}"]["H2"]["n"],
                             base["sensitivities"][f"S-Model-{m}"]["H2"]["n"] - n)
        n_not_coi = sum(1 for r in recs if S.samsung_group(r) and (r["category"], r["unit"]) not in S.COI_UNITS)
        self.assertEqual(res["sensitivities"]["S-COI"]["H2"]["n"], base["sensitivities"]["S-COI"]["H2"]["n"] - n_not_coi)
        for c in res["categories"]:
            n_c = sum(1 for r in recs if S.samsung_group(r) and r["category"] != c)
            self.assertEqual(res["sensitivities"][f"S-LOCO-{c}"]["H2"]["n"],
                             base["sensitivities"][f"S-LOCO-{c}"]["H2"]["n"] - n_c)
        rep = res["descriptives"]["2_open_samsung_group"]
        self.assertEqual((rep["n"], rep["by_code"]), (10, {"VALID": 10}))
        self.assertEqual(sum(res["checks"]["exclusions_samsung_group"].values()), 10)
        self.assertEqual(res["drops"], base["drops"])   # drop rules unchanged (answered and codable as before)
        self.assertEqual(base["descriptives"]["2_open_samsung_group"]["n"], 0)

    def test_end_to_end_flagged_choice_left_out(self):
        raw, pred, _t = S.synth_world(squares=2, seed=21, as_text=True)
        coded0 = C.code_all(raw)
        i = next(j for j, r in enumerate(raw) if r["condition"] == "OPEN" and r["category"] == "cars"
                 and coded0[j]["code"] == "VALID")
        raw[i] = dict(raw[i], text=raw[i]["text"] + " with the Harman Kardon system")
        coded = C.code_all(raw)
        self.assertEqual((coded[i]["code"], coded[i]["samsung_group"]), ("VALID", "Harman"))
        a = S.score(coded, pred, draws=FAST, with_sens=False)
        b = S.score(coded0, pred, draws=FAST, with_sens=False)
        self.assertEqual(a["tests"]["H2"]["n"], b["tests"]["H2"]["n"] - 1)
        self.assertEqual(a["descriptives"]["2_open_samsung_group"]["records"][0]["call_id"], raw[i]["call_id"])


class TestPredictors(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.regs = PR.load_registries(("v0.20",))
        raw, ca, cb = synthetic_predictor_world()
        cls.pred, cls.meta = PR.compute(raw, ca, cb, SYN_MODELS, subs=("v0.20",), registries=cls.regs)

    def test_reference_code_pinned(self):
        self.assertEqual(PR.verify_reference(), [])
        self.assertEqual(PR.REF_COMMIT[:7], "3129674")
        self.assertEqual(PR.STAT, "MODE")
        self.assertEqual(PR.RATING_FLOOR, 6)

    def test_all_registries_hash_verified(self):
        regs = PR.load_registries(PR.V46_SUBS)
        self.assertEqual(sorted(len(u) for _r, u in regs.values()), [24, 24, 24, 24])

    def test_presence_formula(self):
        p = self.pred[("v0.20", "CeraVe")]
        self.assertAlmostEqual(p["pi_hat"], 1.0)
        self.assertEqual((p["recognized"], p["recognition_coded"]), (2, 3))
        self.assertAlmostEqual(p["P"], 100.0 * (2 / 3 + 2.0 * 1.0) / 3.0, places=12)
        lm = self.pred[("v0.20", "La Mer")]
        self.assertAlmostEqual(lm["pi_hat"], 17 / 18)
        self.assertAlmostEqual(lm["P"], 100.0 * (1.0 + 2.0 * 17 / 18) / 3.0, places=12)
        self.assertIsNone(self.pred[("v0.20", "Lancôme")]["P"])       # no coded recognition -> not computed
        self.assertEqual(self.pred[("v0.20", "La Prairie")]["pi_hat"], 0.0)
        self.assertEqual(self.pred[("v0.20", "La Prairie")]["pi_hat_by_model"], {m: 0.0 for m in SYN_MODELS})

    def test_ranking_mode_and_floor(self):
        self.assertEqual(self.pred[("v0.20", "CeraVe")]["R_star"], -1.0)
        self.assertEqual(self.pred[("v0.20", "La Mer")]["R_star"], -2.0)
        self.assertEqual(self.pred[("v0.20", "Lancôme")]["n_ranked"], 9)
        self.assertEqual(self.pred[("v0.20", "Lancôme")]["R_star"], -3.0)
        s = self.pred[("v0.20", "Sisley")]
        self.assertEqual((s["n_ranked"], s["rated"], s["R_star"]), (1, False, None))   # below the floor of 6
        self.assertGreater(self.pred[("v0.20", "CeraVe")]["R_star"], self.pred[("v0.20", "La Mer")]["R_star"])

    def test_missing_and_foreign_answers(self):
        raw, ca, cb = synthetic_predictor_world()
        raw.append(dict(_raw_b("mA", 1, "q3", ""), status="error"))
        raw.append(_raw_b("mZ", 1, "q1", "1. CeraVe\n2. La Mer"))                 # not in the panel
        raw.append(dict(_raw_b("mB", 2, "q4", "1. CeraVe\n2. La Mer"), served_model="other-model"))
        pred, meta = PR.compute(raw, ca, cb, SYN_MODELS, subs=("v0.20",), registries=self.regs)
        self.assertEqual(pred[("v0.20", "CeraVe")]["n_ranked"], 18)
        self.assertEqual(len(meta["excluded_call_ids"]), 2)

    def test_table_joins_probe_registry(self):
        regs = PR.load_registries(PR.V46_SUBS)
        names = {cb for cb in PR.unit_names(regs).values()}
        for cat, units in B.registry_units().items():
            for b, _cell in units:
                self.assertIn((cat, b), names)
        rows = PR.table_rows(self.pred, self.regs)
        self.assertEqual(len(rows), 24)
        r = [x for x in rows if x["brand"] == "CeraVe"][0]
        self.assertEqual((r["category"], float(r["R_star"])), ("skincare", -1.0))

    def test_bad_panel(self):
        with self.assertRaises(PR.PredictorHalt):
            PR.compute([], [], [], ["a", "a"], subs=("v0.20",), registries=self.regs)


# =========================================================================== gates G1/G2 (task 2)
import gates_v0_46 as G  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402


class TestGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.regs = PR.load_registries(("v0.20",))
        raw, ca, cb = synthetic_predictor_world()
        cls.pred, meta = PR.compute(raw, ca, cb, SYN_MODELS, subs=("v0.20",), registries=cls.regs)
        cls.rows = PR.V114.wave_rows(meta["_infos"], PR.RULE, PR.COND)
        cls.stored = [{"substrate": s, "brand": b, "P_S0": v["P"], "rated_S0": v["rated"],
                       "n_ranked_S0": v["n_ranked"], "R_star_S0": v["R_star"]}
                      for (s, b), v in cls.pred.items() if v["n_ranked"] > 0]

    def test_pass_on_identical(self):
        self.assertTrue(G.g1(self.pred, self.stored)["passes"])
        r = G.g2(self.pred, self.stored, self.rows)
        self.assertTrue(r["passes"])
        self.assertEqual(r["rated_units_compared"], 3)

    def test_g1_fails_on_drift(self):
        st = [dict(u) for u in self.stored]
        st[0]["P_S0"] = (st[0]["P_S0"] or 0.0) + 1e-6
        self.assertFalse(G.g1(self.pred, st)["passes"])
        st[0]["P_S0"] = self.stored[0]["P_S0"] + 1e-12 if self.stored[0]["P_S0"] is not None else None
        self.assertTrue(G.g1(self.pred, st)["passes"])

    def test_g2_fails_on_value_rated_set_or_orientation(self):
        st = [dict(u) for u in self.stored]
        k = [i for i, u in enumerate(st) if u["rated_S0"]][0]
        st[k]["R_star_S0"] = st[k]["R_star_S0"] - 1
        self.assertFalse(G.g2(self.pred, st, self.rows)["passes"])
        st = [dict(u) for u in self.stored]
        st[k]["rated_S0"] = False
        self.assertFalse(G.g2(self.pred, st, self.rows)["passes"])
        flipped = {u: dict(v, R_star=(-v["R_star"] if v["R_star"] is not None else None))
                   for u, v in self.pred.items()}
        st = [dict(u, R_star_S0=flipped[(u["substrate"], u["brand"])]["R_star"]) for u in self.stored]
        r = G.g2(flipped, st, self.rows)
        self.assertFalse(r["orientation"]["passes"])
        self.assertFalse(r["passes"])

    def test_green_refuses(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "gates.json"
            self.assertFalse(G.green(p)[0])                                   # no file
            p.write_text(json.dumps({"both_pass": False, "code_sha256": G.code_fingerprint()}))
            self.assertFalse(G.green(p)[0])                                   # a gate failed
            p.write_text(json.dumps({"both_pass": True, "code_sha256": {"x": "y"}}))
            self.assertFalse(G.green(p)[0])                                   # code changed since
            p.write_text(json.dumps({"both_pass": True, "code_sha256": G.code_fingerprint()}))
            self.assertTrue(G.green(p)[0])

    def test_gates_on_t4_archive(self):
        """G1/G2 on t4's archived files (git only; no API). Skipped if the tag is not in this clone."""
        r = subprocess.run(["git", "-C", str(G.ROOT), "rev-parse", "-q", "--verify", f"refs/tags/{G.T4_TAG}"],
                           capture_output=True)
        if r.returncode != 0:
            self.skipTest(f"tag {G.T4_TAG} not available")
        res = G.run_gates(log=lambda *_a: None)
        self.assertTrue(res["G1"]["passes"], res["G1"]["examples"])
        self.assertTrue(res["G2"]["passes"], res["G2"]["examples"])
        self.assertTrue(res["both_pass"])


# =========================================================================== acquisition (task 3; nothing is sent)
import contextlib  # noqa: E402
import io  # noqa: E402
import time  # noqa: E402
from collections import Counter  # noqa: E402
import acquire_v0_46 as A  # noqa: E402

QUIET = (lambda *_a, **_k: None)


def _fake_out(text="CHOICE: CeraVe", fr="end_turn", tout=40):
    return {"text": text, "served_model": None, "finish_reason": fr, "tokens_in": 300, "tokens_out": tout,
            "tokens_thought": None, "paused_continued": False, "search": None}


class TestAcquire(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.panel = A.make_panel(A.ORIENTATION_PANEL)
        cls.specs = A.build_specs(A.load_probes(), cls.panel)

    def test_refuses_run_before_lock(self):
        tmp = Path(tempfile.mkdtemp())
        raw = tmp / "raw.jsonl"
        old = A.RAW_PATH
        A.RAW_PATH = raw
        try:
            err = io.StringIO()
            with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
                code = A.main(["--run"])
        finally:
            A.RAW_PATH = old
        self.assertEqual(code, 2)
        self.assertIn("not locked", err.getvalue())
        self.assertFalse(raw.exists())
        self.assertFalse(A.RAW_PATH.exists())
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            A.main([])                                            # neither --run nor --dry-run

    def test_refuses_tampered_probe_file(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "probes.jsonl"
            p.write_bytes(A.PROBES_PATH.read_bytes() + b"\n")
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(A.Refused):
                A.verify_probes(p)
        self.assertEqual(A.verify_probes(), A.PROBES_SHA256)
        self.assertEqual(A.probes_sha_expected(), A.PROBES_SHA256)

    def test_lock_guard_with_tag_and_anchor(self):
        sha = "a" * 40
        with tempfile.TemporaryDirectory() as d:
            anc = Path(d) / "anchor.json"
            ls = f"{sha}\trefs/tags/{A.PREREG_TAG}\n"
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(A.Refused):
                    A.lock_guard(anchor=anc, ls_remote=ls)                # no anchor
                anc.write_text(json.dumps({"commit": "b" * 40}))
                with self.assertRaises(A.Refused):
                    A.lock_guard(anchor=anc, ls_remote=ls)                # anchor names another commit
                with self.assertRaises(A.Refused):
                    A.lock_guard(anchor=anc, ls_remote="")                # tag not on origin
            anc.write_text(json.dumps({"commit": sha}))
            self.assertEqual(A.lock_guard(anchor=anc, ls_remote=ls), sha)

    def test_dry_run_count_1260(self):
        out = A.dry_run(log=QUIET, cost=False)
        self.assertTrue(out["ok"])
        self.assertEqual(out["d7"], "Cell D")
        self.assertEqual(out["total_calls"], 1260)
        self.assertEqual({b: sum(v.values()) for b, v in out["by_block"].items()}, A.EXPECTED)
        self.assertEqual(len({s["call_id"] for s in self.specs}), 1260)
        self.assertEqual(Counter(s["condition"] for s in self.specs), {"S0": 504, "LIST": 540, "OPEN": 216})
        self.assertEqual([s["block"] for s in self.specs], sorted((s["block"] for s in self.specs),
                                                                  key=A.BLOCK_IDS.index))

    def test_dry_run_projected_cost(self):
        r = subprocess.run(["git", "-C", str(A.ROOT), "rev-parse", "-q", "--verify", "refs/tags/v0.42-scoring-locked"],
                           capture_output=True)
        if r.returncode != 0:
            self.skipTest("t4 tag not available")
        pc = A.projected_cost()
        self.assertEqual(pc["total"], {"central": 43.92, "high": 85.92})      # = manuscript r4 section 3.9
        self.assertEqual(pc["choice_calls"], 756)
        self.assertTrue(pc["d7_fisker_defunct"])
        self.assertEqual(pc["predictor_calls"], 504)

    def test_fork_chunks_verbatim(self):
        src = (A.ROOT / "osf/v45/scripts/acquire_v0_45.py").read_bytes()
        self.assertEqual(hashlib.sha256(src).hexdigest(), A.FORK_SOURCE_SHA256)
        lines = src.decode().split("\n")
        mine = Path(A.__file__).read_text()
        for a, b in A.FORK_MAP["ranges"]:
            ch = "\n".join(lines[a - 1:b])
            for old, new in A.FORK_MAP["substitutions"]:
                ch = ch.replace(old, new)
            self.assertIn(ch, mine, f"lines {a}-{b}")
        self.assertEqual(A.confirm_no_sampling_params(), [])

    def test_raw_fields_feed_coder_and_predictors(self):
        cho = [s for s in self.specs if s["condition"] == "LIST"][0]
        rec = A._record(cho, _fake_out(f"Good.\nCHOICE: {cho['v46']['order'][3]}"), "ok", None, 1, False,
                        "2026-12-02T00:00:00+00:00", "2026-12-02T00:00:01+00:00", [])
        for k in ("call_id", "condition", "category", "brief", "model", "model_slot", "square", "row", "order",
                  "block", "part", "text", "status", "finish_reason", "output_tokens", "model_requested"):
            self.assertIn(k, rec)
        coded = C.code_answer(rec)
        self.assertEqual((coded["code"], coded["position"]), ("VALID", 4))
        pre = [s for s in self.specs if s["block"] == "P3"][0]
        prec = A._record(pre, _fake_out("1. CeraVe\n2. La Mer"), "ok", None, 1, False, "t", "t", [])
        self.assertTrue(PR.V114.in_design(prec, [m["model_id"] for m in self.panel]))
        self.assertEqual((prec["condition"], prec["run"], prec["phase"]), ("S0", 2, "B"))

    def test_stop_rule_detection(self):
        base = {"part": "choice", "provider": "openai", "text": "long deliberation", "finish_reason": "length"}
        self.assertTrue(A.cut_before_outcome(base))
        self.assertFalse(A.cut_before_outcome(dict(base, text="x\n**CHOICE:** CeraVe")))
        self.assertFalse(A.cut_before_outcome(dict(base, finish_reason="stop")))
        self.assertTrue(A.cut_before_outcome({"part": "choice", "provider": "google", "text": "x",
                                              "finish_reason": None, "output_tokens": 16000, "thinking_tokens": 384}))
        self.assertTrue(A.cut_before_outcome({"part": "predictor", "text": "", "finish_reason": "max_tokens"}))
        self.assertFalse(A.cut_before_outcome({"part": "predictor", "text": "1. A", "finish_reason": "max_tokens"}))

    def _world(self, d, runner_texts=None, blocks=("P1", "C1", "C2")):
        """A miniature collection: 2 calls per model in each of `blocks`; fake runners write records."""
        specs = []
        for b in blocks:
            for m in self.panel:
                specs += [s for s in self.specs if s["block"] == b and s["model"]["slot"] == m["slot"]][:2]
        sent = []

        def runner(group, ledger, write):
            for s in group:
                while True:                                  # reserve >= the call's cost (<= $0.26 here)
                    st, tok = ledger.reserve(0.30)
                    if st != "wait":
                        break
                    time.sleep(0.001)
                if st != "ok":
                    return st
                sent.append(s["call_id"])
                txt = (runner_texts or {}).get(s["call_id"], "ok\nCHOICE: CeraVe")
                fr = "length" if txt == "CUT" else "end_turn"
                out = _fake_out("x" if txt == "CUT" else txt, fr, tout=5_000)
                rec = A._record(s, out, "ok", None, 1, False, "2026-12-02T00:00:00+00:00", "t", [
                    {"mode": "standard", "input_tokens": 1000, "output_tokens": 5_000, "n_searches": 0}])
                write(rec)
                ledger.settle(tok, rec["cost_usd"])
            return "done"
        raw, state = Path(d) / "raw.jsonl", Path(d) / "state.json"
        sr = A.StopRule(Path(d) / "stop.jsonl")
        return specs, sent, runner, raw, state, sr

    def test_collection_resumable_and_stop_rule(self):
        with tempfile.TemporaryDirectory() as d:
            specs, sent, runner, raw, state, sr = self._world(d)
            cut = [s for s in specs if s["block"] == "C1" and s["model"]["slot"] == "M2_openai"][0]["call_id"]
            specs, sent, runner, raw, state, sr = self._world(d, {cut: "CUT"})
            led = A.BG.Ledger(raw, state)
            st = A.run_collection(specs, led, raw, {"batch": runner, "standard": runner}, sr, self.panel, log=QUIET)
            self.assertEqual(st, "stop_rule")
            self.assertIn("M2_openai", sr.paused)
            m2_after = [c for c in sent if "gpt-6-astra" in c and c.startswith("OPEN")]
            self.assertEqual(m2_after, [])                               # paused model: no further request
            self.assertEqual(len([c for c in sent if c.startswith("OPEN")]), 4)   # the others go on
            n1 = len(sent)
            sr2 = A.StopRule(Path(d) / "stop.jsonl")                     # resume: still paused, nothing re-sent
            self.assertIn("M2_openai", sr2.paused)
            A.run_collection(specs, A.BG.Ledger(raw, state), raw, {"batch": runner, "standard": runner}, sr2,
                             self.panel, log=QUIET)
            self.assertEqual(len(sent), n1)                              # resume: nothing sent twice
            sr2.release("M2_openai", "author decision (test)")
            st = A.run_collection(specs, A.BG.Ledger(raw, state), raw, {"batch": runner, "standard": runner},
                                  A.StopRule(Path(d) / "stop.jsonl"), self.panel, log=QUIET)
            self.assertEqual(st, "done")
            self.assertEqual(len(sent), n1 + 3)        # M2's other C1 call and its 2 OPEN calls; the cut one is kept
            self.assertEqual(len(set(sent)), len(sent))
            ev = [json.loads(x) for x in (Path(d) / "stop.jsonl").read_text().splitlines()]
            self.assertEqual(ev[0]["event"], "trigger")
            self.assertEqual(ev[0]["call_id"], cut)

    def test_budget_cap_and_projection(self):
        with tempfile.TemporaryDirectory() as d:
            specs, sent, runner, raw, state, sr = self._world(d)
            led = A.BG.Ledger(raw, state, cap=2.5 + 0.30)           # judge reserve 2.50 + room for few calls
            st = A.run_collection(specs, led, raw, {"batch": runner, "standard": runner}, sr, self.panel, log=QUIET)
            self.assertEqual(st, "stop")
            self.assertLessEqual(led.spent(), led.cap + 1e-9)
            self.assertEqual(len(sent), 1)
        with tempfile.TemporaryDirectory() as d:
            specs, sent, runner, raw, state, sr = self._world(d)
            led = A.BG.Ledger(raw, state, cap=5.5, pause_at=99)      # P1 + C1 fit; C1 x 486/270 does not
            st = A.run_collection(specs, led, raw, {"batch": runner, "standard": runner}, sr, self.panel, log=QUIET)
            self.assertEqual(st, "pause")
            self.assertIn("projection", led.halt_reason)
            self.assertFalse(any(c.startswith("OPEN") for c in sent))    # paused before C2


# =========================================================================== descriptives 6 and 8 (task 4)
class TestDescriptives68(unittest.TestCase):
    def test_cannot_buy_patterns(self):
        yes = ["I can't actually buy it for you, but pick CeraVe.", "I'm not able to purchase anything; still: X",
               "I am unable to make purchases, but here is my pick", "As an AI, I can't shop for you.",
               "I don’t have the ability to buy products.", "I cannot complete the purchase myself."]
        no = ["I'll buy whatever you pick", "You can buy it at any pharmacy.", "I recommend CeraVe.",
              "If I could buy one, it would be this."]
        for t in yes:
            self.assertTrue(S.CANNOT_BUY_RE.search(t), t)
        for t in no:
            self.assertFalse(S.CANNOT_BUY_RE.search(t), t)

    def _raw_and_coded(self):
        panel = A.make_panel(A.ORIENTATION_PANEL)
        specs = A.build_specs(A.load_probes(), panel)
        c1 = [s for s in specs if s["block"] == "C1" and s["model"]["slot"] == "M2_openai"][:4]
        p1 = [s for s in specs if s["block"] == "P1" and s["model"]["slot"] == "M2_openai"][0]
        parts = [{"mode": "standard", "input_tokens": 1000, "output_tokens": 100, "n_searches": 0}]
        t0 = "2026-12-02T00:00:00+00:00"
        b0 = c1[0]["v46"]["order"][0]
        raw = [
            A._record(c1[0], _fake_out(f"Solid pick.\nCHOICE: {b0}", tout=100), "ok", None, 1, False, t0, t0, parts),
            A._record(c1[1], _fake_out("I can't actually buy it for you, but go with it.\nCHOICE: "
                                       + c1[1]["v46"]["order"][0], tout=100), "ok", None, 1, False, t0, t0, parts),
            A._record(c1[2], dict(_fake_out("", fr="refusal", tout=0)), "empty", None, 1, False, t0, t0, parts),
            A._record(c1[3], _fake_out("I would rather not choose for you.", tout=100), "ok", None, 1, False, t0, t0,
                      parts),
            A._record(p1, _fake_out("1. CeraVe 2. La Mer three four", tout=250), "ok", None, 1, False, t0, t0, parts),
        ]
        raw.insert(0, A._record(c1[0], None, "error", "transient: 500", 3, False, t0, t0, []))   # failed attempt
        coded = [C.code_answer(r) for r in raw if r["part"] == "choice"]
        return raw, coded

    def test_descriptive_6(self):
        raw, coded = self._raw_and_coded()
        fin = S.final_answers(raw)
        coded = [C.code_answer(fin[cid]) for cid in dict.fromkeys(r["call_id"] for r in raw if r["part"] == "choice")]
        d6 = S.descriptive_6(coded, raw)
        k = "gpt-6-astra/LIST"
        self.assertEqual(d6[k]["answered"], 4)
        self.assertEqual(d6[k]["refusal"], 1)
        self.assertEqual(d6[k]["decline"], 1 + int(coded[3]["code"] == "NONE"))
        self.assertEqual(d6[k]["hedge"], 1)
        self.assertAlmostEqual(d6[k]["hedge_share"], 0.25)

    def test_descriptive_8(self):
        raw, _coded = self._raw_and_coded()
        d8 = S.descriptive_8(raw)
        f = d8["form"]["gpt-6-astra/C1"]
        self.assertEqual(f["words"]["n"], 3)                 # answered final lines only (refusal not answered)
        self.assertEqual(f["output_tokens"]["sum"], 300)
        self.assertEqual(d8["form"]["gpt-6-astra/P1"]["words"]["mean"], 7.0)
        one = (1000 * 10.0 + 100 * 50.0) / 1e6               # gpt-6-astra $10 / $50 per M (budget_v0_45)
        self.assertAlmostEqual(d8["spend"]["gpt-6-astra/C1"]["usd"], 4 * one, places=6)
        self.assertEqual(d8["spend"]["gpt-6-astra/C1"]["lines"], 5)          # the failed attempt is a line too
        self.assertAlmostEqual(d8["spend_total_usd"], 5 * one, places=6)
        self.assertEqual(d8["calls"], 5)

    def test_score_attaches_6_and_8(self):
        recs, pred, _t = S.synth_world(squares=1)
        res = S.score(recs, pred, draws=FAST, with_sens=False, raw=[])
        self.assertIn("6_refusals_hedges", res["descriptives"])
        self.assertIn("8_answer_form_and_cost", res["descriptives"])
        self.assertNotIn("8_answer_form_and_cost", S.score(recs, pred, draws=FAST, with_sens=False)["descriptives"])


# =========================================================================== r3 task 3: v0.42's coder on v46_raw
import code_predictors_v0_46 as CP  # noqa: E402


class TestV42CoderOnV46Raw(unittest.TestCase):
    def test_locked_coder_pinned(self):
        self.assertEqual(CP.verify_coder(), "2d36735d512cf9e13b74010ba5a7f655fc7de0bc")
        tmp = Path(tempfile.mkdtemp()) / "code_t4_v0_42.py"
        tmp.write_bytes(CP.V42_CODER.read_bytes() + b"\n# edited\n")
        with self.assertRaises(CP.CoderHalt):
            CP.verify_coder(tmp)

    def test_keyless_env(self):
        env = CP.keyless_env({"PATH": "/bin", "ANTHROPIC_API_KEY": "x", "OPENAI_API_KEY": "y", "GEMINI_API_KEY": "z",
                              "GOOGLE_APPLICATION_CREDENTIALS": "f", "HF_TOKEN": "t", "HOME": "/h"})
        self.assertEqual(env, {"PATH": "/bin", "HOME": "/h"})

    def test_predictor_lines_only(self):
        raw = [{"part": "predictor", "phase": "A", "condition": "S0"},
               {"part": "choice", "phase": "v0.46", "condition": "LIST"},
               {"phase": "B", "condition": "S0"}, {"phase": "v0.46", "condition": "OPEN"}]
        self.assertEqual(len(CP.predictor_lines(raw)), 2)

    def test_judge_refused_and_no_api_import(self):
        self.assertEqual(CP.main(["--judge"]), 2)
        src = Path(CP.__file__).read_text(encoding="utf-8")
        self.assertNotIn("import anthropic", src)
        self.assertNotIn('"--judge"]', src)

    def test_dry_run_on_fixture(self):
        self.assertEqual(CP.dry_run(log=lambda *_a: None), [])


# =========================================================================== r3 task 4: spirits judge
import os  # noqa: E402
import judge_spirits_v0_46 as JS  # noqa: E402  (pure helpers only; the judge part runs in its own process)


class TestSpiritsJudge(unittest.TestCase):
    SCRIPT = str(Path(JS.__file__))

    def _j1(self, obj):
        p = Path(tempfile.mkdtemp()) / "j1.json"
        p.write_text(json.dumps(obj), encoding="utf-8")
        return p

    def test_select_judge_follows_j1(self):
        self.assertIsNone(JS.select_judge(Path(tempfile.mkdtemp()) / "missing.json")[0])
        self.assertIsNone(JS.select_judge(self._j1({"runs": [{"judge": "claude-sonnet-5-5"}]}))[0])  # no winner
        self.assertIsNone(JS.select_judge(self._j1({"judge": "claude-opus-9", "verdict": {"pass": True}}))[0])
        self.assertIsNone(JS.select_judge(self._j1({"judge": "claude-sonnet-4-6", "verdict": {"pass": False}}))[0])
        self.assertEqual(JS.select_judge(self._j1({"judge": "claude-sonnet-4-6", "verdict": {"pass": True}}))[0],
                         "claude-sonnet-4-6")

    def test_copies_match_v45_and_v42(self):
        v45 = (JS.V45_SCRIPTS / "code_t5_v0_45.py").read_text(encoding="utf-8")
        self.assertIn('CANDIDATES = ["claude-sonnet-5-5", "claude-sonnet-4-6"]', v45)
        v42 = CP.V42_CODER.read_text(encoding="utf-8")
        self.assertIn('A_FIELDS = ["call_id", "substrate", "brand", "brand_id", "model", "condition", "run", '
                      '"probe_id", "label", "recognized"]', v42)

    def test_selects_the_72_open_spirits_answers(self):
        raw, _panel = CP.fixture_raw()
        sel = JS.v23_phase_a_lines(raw)
        self.assertEqual(len(sel), JS.EXPECTED_ANSWERS)
        self.assertEqual({(r["substrate"], r["phase"], r["block"]) for r in sel}, {("v23", "A", "P2")})

    def test_fake_judge_is_local(self):
        f = JS.FakeJudge()
        r = f.messages.create(model="m", max_tokens=10, system="s",
                              messages=[{"role": "user", "content": "Response: I'm not familiar with it"}])
        self.assertEqual(r.content[0].text, "R0")
        self.assertEqual(len(f.requests), 1)

    def test_dry_run_subprocess_pass_and_keyless(self):
        env = dict(os.environ, ANTHROPIC_API_KEY="sk-test-not-a-key")
        r = subprocess.run([sys.executable, self.SCRIPT, "--dry-run"], capture_output=True, text=True, timeout=120,
                           env=env)
        self.assertEqual(r.returncode, 0, r.stderr[-800:])
        self.assertIn("spirits judge dry run PASS", r.stdout)
        self.assertIn("72 coded", r.stdout)

    def test_run_refused_before_lock(self):
        r = subprocess.run([sys.executable, self.SCRIPT, "--run", "--raw", "x", "--coded-dir", "y"],
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 3)
        self.assertIn("REFUSED", r.stderr)


# =========================================================================== r3 task 5: D7 (Fisker)
class TestD7Fisker(unittest.TestCase):
    GOOD = {"unit": "Fisker", "question": "Does Fisker sell new cars in the US as of the check date?",
            "checked_utc": "2026-12-01T15:00:00+00:00", "method": "ai_check_dated_source",
            "checker": "claude-fable-5-2", "sells_new_cars_us": False, "decision": "cell_d",
            "sources": [{"url": "https://example.org/fisker-status", "title": "t", "source_date": "2026-11-30"}]}

    def _write(self, rec):
        p = Path(tempfile.mkdtemp()) / "d7.json"
        p.write_text(json.dumps(rec), encoding="utf-8")
        return p

    def test_validate(self):
        self.assertEqual(B.validate_d7(self.GOOD), [])
        self.assertEqual(B.validate_d7(dict(self.GOOD, sells_new_cars_us=True, decision="live")), [])
        for bad in (dict(self.GOOD, method="manual"), dict(self.GOOD, sources=[]),
                    dict(self.GOOD, sources=[{"url": "ftp://x", "source_date": "2026-11-30"}]),
                    dict(self.GOOD, sources=[{"url": "https://x.org", "source_date": "Nov 30"}]),
                    dict(self.GOOD, checked_utc="2026-12-01T15:00:00"), dict(self.GOOD, decision="live"),
                    dict(self.GOOD, sells_new_cars_us="no"), dict(self.GOOD, checker=""), dict(self.GOOD, unit="X")):
            with self.subTest(bad=bad):
                self.assertNotEqual(B.validate_d7(bad), [])

    def test_outcome_and_pending(self):
        self.assertIsNone(B.d7_outcome(Path(tempfile.mkdtemp()) / "none.json")[0])
        self.assertIsNone(B.d7_outcome(self._write(dict(self.GOOD, method="manual")))[0])
        self.assertTrue(B.d7_outcome(self._write(self.GOOD))[0])
        self.assertFalse(B.d7_outcome(self._write(dict(self.GOOD, sells_new_cars_us=True, decision="live")))[0])
        if not B.D7_PATH.exists():                                           # Stage 1 code: D7 still pending
            self.assertIsNone(B.d7_outcome()[0])

    def test_guard(self):
        import acquire_v0_46 as A
        nores = Path(tempfile.mkdtemp()) / "raw.jsonl"
        with self.assertRaises(A.Refused):                                   # pending
            A.d7_guard(Path(tempfile.mkdtemp()) / "none.json", raw_path=nores)
        live = self._write(dict(self.GOOD, sells_new_cars_us=True, decision="live"))
        with self.assertRaises(A.Refused):                                   # r4: counts are for Cell D only
            A.d7_guard(live, raw_path=nores)
        self.assertTrue(A.d7_guard(self._write(self.GOOD), raw_path=nores))  # r4: committed probes have Cell D
        _b, cho_live, _p = B.build(fisker_defunct=False)
        with self.assertRaises(A.Refused):                                   # Cell D, but the probes show Fisker
            A.d7_guard(self._write(self.GOOD), probes=cho_live, raw_path=nores)
        _body, cho, _pred = B.build(fisker_defunct=True)
        self.assertFalse(B.fisker_in_probes(cho))
        self.assertTrue(A.d7_guard(self._write(self.GOOD), probes=cho, raw_path=nores))
        nores.write_text(json.dumps({"started_utc": "2026-12-01T14:00:00+00:00"}) + "\n", encoding="utf-8")
        with self.assertRaises(A.Refused):                                   # check dated after the first request
            A.d7_guard(self._write(self.GOOD), probes=cho, raw_path=nores)

    def test_coder_after_d7(self):
        rec = {"condition": "OPEN", "category": "cars", "text": "x\nCHOICE: Fisker"}
        self.assertEqual(C.code_answer(rec, live=B.live_units(fisker_defunct=False))["code"], "VALID")
        got = C.code_answer(rec, live=B.live_units(fisker_defunct=True))
        self.assertEqual((got["code"], got["unit"]), ("DEFUNCT", "Fisker"))
        self.assertEqual(C.code_answer(rec)["code"], "DEFUNCT")             # r4: the default follows the record
        self.assertEqual(len(B.live_units(True)["cars"]) + 1, len(B.live_units(False)["cars"]))

    def test_cell_d_applied_r4(self):
        """r4: the committed D7 record (cell_d), the probe file, the acquisition counts and the scorer agree."""
        import acquire_v0_46 as A
        defunct, rec, probs = B.d7_outcome()
        self.assertEqual((defunct, probs, rec["decision"]), (True, [], "cell_d"))
        self.assertTrue(B.FISKER_DEFUNCT_DEFAULT)
        self.assertNotIn("Fisker", B.live_units()["cars"])
        probes = A.load_probes()                                             # committed probe file
        cho = [p for p in probes if p.get("part") == "choice"]
        self.assertFalse(B.fisker_in_probes(cho))
        self.assertTrue(A.d7_guard(raw_path=Path(tempfile.mkdtemp()) / "raw.jsonl"))
        self.assertEqual(sum(len(v) for v in B.live_units().values()), 90)
        self.assertEqual((len(probes), len(cho), A.EXPECTED_TOTAL), (876, 756, 1260))
        self.assertEqual(A.EXPECTED, {"P1": 72, "P2": 288, "P3": 72, "P4": 72, "C1": 270, "C2": 216, "C3": 270})
        self.assertAlmostEqual(A.PROJECTION_FACTOR, 486 / 270)
        self.assertEqual((S.DESIGNED, S.DESIGNED_NO_SPIRITS, S.DESIGNED_CHOICE_CALLS),
                         ({"LIST": 180, "OPEN": 72}, {"LIST": 132, "OPEN": 54}, 756))
        self.assertEqual(S.MIN_VALID, {"H1": 450, "H2": 120, "H3": 200, "H4": 200})
        self.assertEqual(S.MIN_VALID_NO_SPIRITS, {"H1": 330, "H2": 90, "H3": 147, "H4": 147})
        # a probe file built with Fisker live (1,266-call design) is refused against this record
        _b, cho_live, _p = B.build(fisker_defunct=False)
        with self.assertRaises(A.Refused):
            A.d7_guard(probes=cho_live, raw_path=Path(tempfile.mkdtemp()) / "raw.jsonl")

    def test_run_calls_d7_guard_before_panel(self):
        import acquire_v0_46 as A
        import inspect
        src = inspect.getsource(A.run)
        self.assertLess(src.index("d7_guard()"), src.index("panel_guard()"))
        self.assertLess(src.index("d7_guard()"), src.index("require_keys_v46()"))


# =========================================================================== D7 and P1 AI checks (preparation)
class TestAIChecks(unittest.TestCase):
    SCRIPT = str(HERE.parent / "ai_checks_v0_46.py")

    def setUp(self):
        import ai_checks_v0_46 as K
        self.K = K

    def test_p1_quote_read_and_outcome_rule(self):
        K = self.K
        q = K.manuscript_p1_quote()
        self.assertTrue(q.startswith("In most categories"))
        self.assertEqual(K.p1_outcome(q.replace("'", "’") + "  ", q), "match")
        self.assertEqual(K.p1_outcome("Reinforcement. " + q, q), "contained")
        self.assertEqual(K.p1_outcome(q.replace("most", "many", 1), q), "mismatch")
        self.assertEqual(K.p1_outcome("", q, False), "not_found")
        self.assertEqual(set(K.P1_DECISION), {"match", "contained", "mismatch", "not_found"})

    def test_d7_reply_sources_must_come_from_search(self):
        K = self.K
        t = K.now_utc()
        src = {"url": "https://a.org/x", "title": "t", "source_date": t.date().isoformat()}
        body = json.dumps({"sells_new_cars_us": True, "finding": "f", "sources": [src]})
        rec, _p = K.d7_record_from_reply({"text": body, "search_urls": ["https://a.org/x/"]}, t, "m")
        self.assertEqual((rec["decision"], B.validate_d7(rec)), ("live", []))
        rec, p = K.d7_record_from_reply({"text": body, "search_urls": ["https://b.org/"]}, t, "m")
        self.assertIsNone(rec)
        later = dict(src, source_date="2999-01-01")
        rec, p = K.d7_record_from_reply({"text": json.dumps({"sells_new_cars_us": True, "sources": [later]}),
                                         "search_urls": ["https://a.org/x"]}, t, "m")
        self.assertIsNone(rec)
        self.assertIsNone(K.d7_record_from_reply({"text": "no json"}, t, "m")[0])

    def test_dry_run_subprocess_pass_and_keyless(self):
        env = dict(os.environ, OPENAI_API_KEY="sk-test-not-a-key")
        r = subprocess.run([sys.executable, self.SCRIPT, "--dry-run"], capture_output=True, text=True, timeout=120,
                           env=env)
        self.assertEqual(r.returncode, 0, r.stderr[-800:])
        self.assertIn("AI checks dry run PASS", r.stdout)

    def test_run_refused_without_key(self):
        # The real D7 record exists since 2026-11-24 (r3); a refused run must leave it as it was (or absent).
        before = B.D7_PATH.read_bytes() if B.D7_PATH.exists() else None
        env = {k: v for k, v in os.environ.items() if k != "OPENAI_API_KEY"}
        r = subprocess.run([sys.executable, self.SCRIPT, "--run", "d7"], capture_output=True, text=True, timeout=60,
                           env=env)
        self.assertEqual(r.returncode, 2)
        self.assertIn("REFUSED", r.stderr)
        self.assertEqual(B.D7_PATH.read_bytes() if B.D7_PATH.exists() else None, before)


if __name__ == "__main__":
    unittest.main()
