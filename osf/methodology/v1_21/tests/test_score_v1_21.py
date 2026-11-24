#!/usr/bin/env python3
"""Tests of the v1.21 scorer (synthetic data only; no model call, no real data).

Run from the repository root:
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s osf/methodology/v1_21/tests -p "test_*.py" -v
Fixtures: osf/methodology/v1_21/tests/fixtures/<world>/ (built by fixtures/build_fixtures_v1_21.py).
Resampling draws are lowered to 99 in the fixture runs (the pre-registered 10,000 are checked as constants).
"""
from __future__ import annotations

import json
import math
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
import score_v1_21 as T  # noqa: E402

FX = HERE / "fixtures"
D = T.Draws(99, 99, 99)
_CACHE: dict = {}


def world(name: str, sensitivities: bool = False):
    key = (name, sensitivities)
    if key not in _CACHE:
        out = Path(tempfile.mkdtemp(prefix=f"v121_{name}_"))
        _CACHE[key] = T.run_fixture(FX / name, out, D, sensitivities=sensitivities) + (out,)
    return _CACHE[key]


def mk(answer, cat, brand, v=0, status="VALID", refers=True, ev=None, wave="t5", model="gpt-6-astra",
       provider="openai", v2=None):
    def j(val):
        ok = status == T.VALID
        return {"status": status, "valence": val if ok else None,
                "evaluative": bool((val != 0) if ev is None else ev) and ok and refers, "refers": refers and ok}
    return {"unit_id": f"{wave}|{answer}#{brand}", "wave": wave, "category": cat, "brand": brand,
            "answer_id": answer, "model": model, "provider": provider, "J1": j(v), "J2": j(v if v2 is None else v2),
            "J1att": j(v), "J2att": j(v if v2 is None else v2),
            "J1rep": {"status": None, "valence": None}, "J2rep": {"status": None, "valence": None}}


def comps(rows, **kw):
    return T.Comps(rows, **kw)


# ======================================================================================
# A. One fixture world per verdict branch
# ======================================================================================
class TestWorlds(unittest.TestCase):
    def test_confirmed_world_passes(self):
        sj, doc, _ = world("confirmed")
        for h in ("H1_t5", "H2_t5", "H3_t5", "H4", "H5_t4"):
            self.assertEqual(doc["VERDICTS"][h], "CONFIRMED", h)
        self.assertEqual(doc["GATE"], "PASS")
        self.assertEqual(doc["CONSEQUENCE"], T.CONSEQUENCE_PASS)
        self.assertFalse(doc["noise_guard_applied"])

    def test_falsified_world_fails(self):
        _, doc, _ = world("falsified")
        self.assertEqual(doc["VERDICTS"]["H2_t5"], "FALSIFIED")
        self.assertGreaterEqual(abs(doc["H2_t5_Sep_Presence"]["rho"]), 0.50)
        self.assertEqual(doc["GATE"], "FAIL")
        self.assertEqual(doc["CONSEQUENCE"], T.CONSEQUENCE_NOT_PASS)

    def test_marginal_world(self):
        _, doc, _ = world("marginal")
        r = abs(doc["H2_t5_Sep_Presence"]["rho"])
        self.assertTrue(0.30 < r < 0.50, r)
        self.assertEqual(doc["VERDICTS"]["H2_t5"], "MARGINAL")
        self.assertEqual(doc["GATE"], "MARGINAL")
        self.assertEqual(doc["CONSEQUENCE"], T.CONSEQUENCE_NOT_PASS)

    def test_retest_failure_triggers_noise_guard(self):
        _, doc, _ = world("retest_fail")
        self.assertEqual(doc["VERDICTS"]["H4"], "FALSIFIED")
        self.assertTrue(doc["noise_guard_applied"])
        for h in ("H2_t5", "H3_t5", "H5_t4"):
            self.assertEqual(doc["VERDICTS"][h], "UNDETERMINED")
            self.assertNotEqual(doc["verdicts_before_noise_guard"][h], "UNDETERMINED")
        self.assertEqual(doc["GATE"], "FAIL")

    def test_judge_disagreement_falsifies_h1_and_guards(self):
        _, doc, _ = world("judge_noise")
        self.assertEqual(doc["VERDICTS"]["H1_t5"], "FALSIFIED")
        self.assertTrue(doc["noise_guard_applied"])
        self.assertEqual(doc["VERDICTS"]["H2_t5"], "UNDETERMINED")
        self.assertEqual(doc["GATE"], "FAIL")

    def test_two_categories_undetermined(self):
        _, doc, _ = world("two_cats")
        for h in T.GATE_ROWS:
            self.assertEqual(doc["VERDICTS"][h], "UNDETERMINED", h)
        self.assertEqual(doc["GATE"], "UNDETERMINED")
        self.assertEqual(doc["CONSEQUENCE"], T.CONSEQUENCE_NOT_PASS)

    def test_sensitivities_never_change_a_verdict(self):
        _, plain, _ = world("confirmed")
        _, doc, _ = world("confirmed", sensitivities=True)
        self.assertEqual(doc["VERDICTS"], plain["VERDICTS"])
        self.assertEqual(doc["GATE"], plain["GATE"])
        self.assertEqual(set(doc["sensitivities"]), set(T.sensitivity_variants()))
        self.assertEqual(len(doc["sensitivities"]), 10)   # SD, S-COI, SU, S_w, S_prior x2, S_floor x2, TONE_J2, S-ATT
        for name, s in doc["sensitivities"].items():
            self.assertIn(s["GATE"], ("PASS", "FAIL", "MARGINAL", "UNDETERMINED"), name)
        for ch in doc["sensitivity_verdict_changes"]:
            self.assertNotEqual(ch["primary"], ch["under_sensitivity"])

    def test_secondaries_and_checks_reported(self):
        _, doc, _ = world("confirmed")
        self.assertEqual(set(doc["secondaries"]), {"CONTRAST", "S_ref", "S_cat", "TONE_NV", "S_res"})
        for k in ("CONTRAST", "S_ref", "S_cat", "TONE_NV"):
            self.assertIn("p_shuffle", doc["secondaries"][k]["H4"])
        self.assertTrue(doc["checks"]["Identity_S_cat_equals_S_ref"]["passes"])
        self.assertIn("flag_list_composition_driven", doc["checks"]["MQ7_negative_control"])
        self.assertIn("rho", doc["checks"]["MQ6_positive_control_rho_w_n_named_P_S0_t5"])

    def test_values_file_holds_every_scalar(self):
        _, doc, out = world("confirmed")
        vals = json.loads((out / T.VALUES_NAME).read_text())
        ver = json.loads((out / T.VERDICTS_NAME).read_text())
        self.assertEqual(vals["GATE"], ver["GATE"])
        self.assertEqual(vals["H2_t5_Sep_Presence.rho"], ver["H2_t5_Sep_Presence"]["rho"])
        self.assertEqual(len(vals), len(T.flatten_values(ver)))

    def test_stage_j_reads_no_presence(self):
        sj, _, _ = world("confirmed")
        txt = json.dumps(sj)
        self.assertNotIn("H2_t5", txt)
        self.assertIn("precision_at_realised_n", sj)
        self.assertGreater(sj["precision_at_realised_n"]["n"], 0)


class TestDeterminism(unittest.TestCase):
    def test_same_inputs_same_outputs(self):
        outs = []
        for _ in range(2):
            out = Path(tempfile.mkdtemp(prefix="v121_det_"))
            sj, doc = T.run_fixture(FX / "marginal", out, D, sensitivities=False)
            outs.append(out)
        a, b = (json.loads((o / T.VERDICTS_NAME).read_text()) for o in outs)
        for d in (a, b):
            d.pop("created_utc")
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))
        for wn in T.WAVES:
            self.assertEqual(T.sha256_file(outs[0] / T.OUTCOMES_NAME[wn]), T.sha256_file(outs[1] / T.OUTCOMES_NAME[wn]))
        for o in outs:
            shutil.rmtree(o)

    def test_preregistered_constants(self):
        self.assertEqual(T.SEEDS, {"unit_order": 121000, "selfcon": 121003, "shuffle": 121010, "H4_perm": 121011,
                                   "boot": 121020})
        self.assertEqual((T.BAND_CONF, T.BAND_FALS), (0.30, 0.50))
        self.assertEqual((T.STAB_CONF, T.STAB_FALS), (0.50, 0.30))
        self.assertEqual((T.FLOOR, T.FLOOR_SENS, T.PRIOR, T.PRIOR_SENS), (6, (3, 10), 1.0, (0.1, 10.0)))
        self.assertEqual((T.N_PERM, T.N_SHUFFLE, T.N_BOOT, T.CI_LEVEL), (10_000, 10_000, 10_000, 0.95))
        self.assertEqual((T.MIN_UNITS_POOLED, T.MIN_GROUPS, T.MIN_UNITS_PER_GROUP), (20, 3, 4))
        self.assertEqual(T.JUDGE_FAIL_HALT_SHARE, 0.02)
        self.assertTrue(T.Draws().as_dict()["preregistered"])
        self.assertFalse(D.as_dict()["preregistered"])


# ======================================================================================
# B. Verdict rules, gate and noise guard
# ======================================================================================
class TestRules(unittest.TestCase):
    def _res(self, r, det=True):
        return {"abs_rho": abs(r), "determinable": det}

    def test_band_edges_unrounded(self):
        self.assertEqual(T.band(self._res(0.30)), "CONFIRMED")
        self.assertEqual(T.band(self._res(-0.30)), "CONFIRMED")
        self.assertEqual(T.band(self._res(0.3000001)), "MARGINAL")
        self.assertEqual(T.band(self._res(0.4999999)), "MARGINAL")
        self.assertEqual(T.band(self._res(0.50)), "FALSIFIED")
        self.assertEqual(T.band(self._res(-0.5013)), "FALSIFIED")
        self.assertEqual(T.band(self._res(0.1, det=False)), "UNDETERMINED")

    def test_stability_branches(self):
        sv = T.stability_verdict
        self.assertEqual(sv(0.50, 0.01, 0.01, True), "CONFIRMED")
        self.assertEqual(sv(0.40, 0.01, 0.01, True), "MARGINAL")
        self.assertEqual(sv(0.29, 0.01, 0.01, True), "FALSIFIED")
        self.assertEqual(sv(0.90, 0.05, 0.01, True), "FALSIFIED")
        self.assertEqual(sv(0.90, 0.01, 0.05, True), "FALSIFIED")
        self.assertEqual(sv(0.90, 0.01, 0.01, False), "UNDETERMINED")
        self.assertEqual(sv(0.90, 0.01, float("nan"), True), "UNDETERMINED")

    def test_gate_table(self):
        C, M, F, U = "CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED"

        def g(h1, h2, h3, h4, h5=C):
            return T.gate({"H1_t5": h1, "H2_t5": h2, "H3_t5": h3, "H4": h4, "H5_t4": h5})
        self.assertEqual(g(C, C, C, C), "PASS")
        self.assertEqual(g(C, C, C, C, F), "MARGINAL")        # H5_t4 downgrade only
        self.assertEqual(g(C, C, C, C, U), "PASS")
        self.assertEqual(g(C, C, C, C, M), "PASS")
        self.assertEqual(g(C, M, C, C), "MARGINAL")
        self.assertEqual(g(C, U, C, C), "UNDETERMINED")
        self.assertEqual(g(C, U, F, C), "FAIL")               # FALSIFIED outranks UNDETERMINED
        self.assertEqual(g(F, C, C, C), "FAIL")
        self.assertEqual(g(C, C, C, F), "FAIL")
        self.assertEqual(T.consequence("MARGINAL"), T.CONSEQUENCE_NOT_PASS)
        self.assertEqual(T.consequence("UNDETERMINED"), T.CONSEQUENCE_NOT_PASS)

    def test_noise_guard(self):
        base = {"H1_t5": "CONFIRMED", "H2_t5": "CONFIRMED", "H3_t5": "MARGINAL", "H4": "CONFIRMED",
                "H5_t4": "FALSIFIED"}
        out, on = T.apply_noise_guard(base)
        self.assertFalse(on)
        self.assertEqual(out, base)
        for trig in ("H1_t5", "H4"):
            out, on = T.apply_noise_guard({**base, trig: "FALSIFIED"})
            self.assertTrue(on)
            self.assertEqual([out[h] for h in ("H2_t5", "H3_t5", "H5_t4")], ["UNDETERMINED"] * 3)
            self.assertEqual(out[trig], "FALSIFIED")
        out, on = T.apply_noise_guard({**base, "H1_t5": "MARGINAL"})
        self.assertFalse(on)

    def test_pooled_floors(self):
        rng = np.random.default_rng(1)

        def det(sizes):
            g = sum(([f"c{i}"] * n for i, n in enumerate(sizes)), [])
            x = rng.normal(size=len(g))
            return T.ptest(x, x + rng.normal(size=len(g)), g, D, boot=False)
        self.assertTrue(det([7, 7, 6])["determinable"])           # 20 units, 3 categories
        self.assertFalse(det([7, 6, 6])["determinable"])          # 19 units
        self.assertFalse(det([10, 10])["determinable"])           # 2 categories
        r = det([8, 8, 8, 3])                                     # a 3-unit category does not enter
        self.assertEqual(r["n"], 24)
        self.assertNotIn("c3", r["units_per_category"])

    def test_precision_table_reproduces_v1_16_at_n71(self):
        tab = T.precision_table(71)["P_abs_rho_le_0.30"]
        self.assertEqual([round(tab[k], 2) for k in ("0.00", "0.10", "0.15", "0.20", "0.25", "0.30")],
                         [0.99, 0.96, 0.90, 0.81, 0.67, 0.50])


# ======================================================================================
# C. Comparisons, floors and exclusions (sections 3.1-3.3, 9)
# ======================================================================================
class TestComparisons(unittest.TestCase):
    def test_pairs_decided_by_order_ties_half(self):
        rows = [mk("a1", "c", "A", 1), mk("a1", "c", "B", 0), mk("a1", "c", "C", 0)]
        c = comps(rows)
        W = c.win_matrix()
        i = c.idx
        self.assertEqual(W[i["A"], i["B"]], 1.0)
        self.assertEqual(W[i["B"], i["A"]], 0.0)
        self.assertEqual(W[i["B"], i["C"]], 0.5)
        self.assertEqual(W[i["C"], i["B"]], 0.5)
        self.assertEqual(len(c.ra), 3)                          # k(k-1)/2

    def test_size_of_difference_does_not_matter(self):
        a = comps([mk("a1", "c", "A", 2), mk("a1", "c", "B", -2)]).win_matrix()
        b = comps([mk("a1", "c", "A", 1), mk("a1", "c", "B", 0)]).win_matrix()
        self.assertTrue(np.array_equal(a, b))

    def test_excluded_units_and_single_brand_answers(self):
        rows = [mk("a1", "c", "A", 1), mk("a1", "c", "B", 0, refers=False),
                mk("a2", "c", "A", 1), mk("a2", "c", "C", 0, status=T.FAIL),
                mk("a3", "c", "A", 1), mk("a3", "c", "D", 0, status=T.UNJUDGED),
                mk("a4", "c", "A", 2)]
        c = comps(rows)
        self.assertEqual(c.brands, ["A"])                       # B, C, D give no valid window
        self.assertEqual(len(c.ra), 0)
        self.assertEqual(c.n_contrib[c.idx["A"]], 0)
        self.assertEqual(c.n_windows[c.idx["A"]], 4)            # single-brand windows still enter S_ref
        self.assertEqual(c.n_answers_ge2, 0)

    def test_pair_weight_sensitivity(self):
        rows = [mk("a1", "c", b, v) for b, v in (("A", 1), ("B", 0), ("C", -1))]
        self.assertTrue(np.allclose(comps(rows, weighting="per_answer").wt, 0.5))
        self.assertTrue(np.allclose(comps(rows).wt, 1.0))

    def test_tone_nv_uses_evaluative_pairs_only(self):
        rows = [mk("a1", "c", "A", 1), mk("a1", "c", "B", 0, ev=False), mk("a1", "c", "C", -1)]
        c = comps(rows, nv=True)
        self.assertEqual(c.brands, ["A", "C"])
        self.assertEqual(len(c.ra), 1)

    def test_duplicate_window_halts(self):
        with self.assertRaises(T.Halt):
            comps([mk("a1", "c", "A", 1), dict(mk("a1", "c", "A", 0), unit_id="other")])

    def _floor_rows(self, n_x):
        """Brand X co-named with R in n_x answers; R and S co-named in 10 more answers."""
        rows = []
        for i in range(n_x):
            rows += [mk(f"x{i}", "c", "X", i % 3 - 1), mk(f"x{i}", "c", "R", 0)]
        for i in range(10):
            rows += [mk(f"r{i}", "c", "R", 0), mk(f"r{i}", "c", "S", i % 2)]
        return rows

    def test_rating_floor_edge(self):
        for n_x, rated in ((6, True), (5, False)):
            U = T.cat_values(comps(self._floor_rows(n_x)), "TONE")
            self.assertEqual(U["X"]["n_contrib"], n_x)
            self.assertEqual(U["X"]["rated"], rated, n_x)
        U = T.cat_values(comps(self._floor_rows(5)), "TONE", floor=3)
        self.assertTrue(U["X"]["rated"])
        U = T.cat_values(comps(self._floor_rows(9)), "TONE", floor=10)
        self.assertFalse(U["X"]["rated"])

    def test_main_component_rule_and_mq9(self):
        rows = self._floor_rows(8)
        for i in range(7):                                      # an island: Y and Z only meet each other
            rows += [mk(f"y{i}", "c", "Y", 1), mk(f"y{i}", "c", "Z", 0)]
        c = comps(rows)
        U = T.cat_values(c, "TONE")
        self.assertTrue(U["X"]["rated"])
        self.assertFalse(U["Y"]["rated"])                       # 7 >= 6 answers, outside the main component
        self.assertFalse(U["Y"]["main_component"])
        w = T.Wave("t5", rows)
        m = T.mq9(w)
        self.assertEqual(m["outside_main_component"], 2)
        self.assertTrue(m["flag"])

    def test_judge_fail_halt_threshold(self):
        def rows(n_fail):
            out = []
            for i in range(100):
                st = T.FAIL if i < n_fail else T.VALID
                out.append(mk(f"a{i}", "c", "A", 0, status=st))
            return out
        ok = T.judge_fail_check({"t5": T.Wave("t5", rows(2))})
        self.assertEqual(ok["halt"], [])                        # 2 of 100 = 2%: not above
        bad = T.judge_fail_check({"t5": T.Wave("t5", rows(3))})
        self.assertEqual(bad["halt"], ["t5 J1 c", "t5 J2 c"])  # mk() fails the window for both judges
        waves = {"t4": T.Wave("t4", [dict(r, wave="t4", unit_id="t4" + r["unit_id"]) for r in rows(0)]),
                 "t5": T.Wave("t5", rows(3))}
        with self.assertRaises(T.Halt):
            T.stage_j_core(waves, {"J1": "claude-opus-5-5", "J2": "gpt-6.1-sol"}, D)

    def test_u0_extraction_miss_threshold(self):
        r = T.u0_miss_check({"c1": 100, "c2": 100}, {"c1": 5, "c2": 6})
        self.assertEqual(r["halt"], ["c2"])

    def test_denon_exclusion_leaves_the_fit(self):
        _, doc, _ = world("confirmed", sensitivities=True)
        sd = doc["sensitivities"]["SD_without_Denon"]["H2_t5_Sep_Presence"]
        prim = doc["H2_t5_Sep_Presence"]
        self.assertEqual(sd["units_per_category"]["v0.19"], prim["units_per_category"]["v0.19"] - 1)
        coi = doc["sensitivities"]["S-COI_without_Denon_and_five_agency_brands"]["H2_t5_Sep_Presence"]
        self.assertLessEqual(coi["n"], prim["n"] - 1)

    def test_n_named_counts_answers_with_a_window(self):
        rows = [mk("a1", "c", "A", 1), mk("a1", "c", "B", 0, status=T.FAIL), mk("a2", "c", "A", 0)]
        nn = T.n_named_t5(T.Wave("t5", rows), {("c", "B"): 2})
        self.assertEqual(nn[("c", "A")], 2.0)
        self.assertEqual(nn[("c", "B")], 3.0)

    def test_self_preference_groups(self):
        rows = []
        for i in range(25):
            rows.append(mk(f"o{i}", "c", "A", 1, v2=0, model="claude-fable-5-2", provider="anthropic"))
            rows.append(mk(f"p{i}", "c", "A", 0, v2=0))
        r = T.h7_t5(T.Wave("t5", rows), "claude-opus-5-5")
        self.assertEqual(r["delta_points"], 25.0)
        self.assertEqual(r["verdict"], "FALSIFIED")


# ======================================================================================
# D. By-construction properties (section 13 step 1)
# ======================================================================================
class TestByConstruction(unittest.TestCase):
    def test_frequency_does_not_enter_direction(self):
        """X is co-named with R in 40 answers, Y in 8; each wins half of its head-to-heads. Naming frequency
        changes only the number of comparisons: TONE_X equals TONE_Y."""
        rows = []
        for i in range(40):
            rows += [mk(f"x{i}", "c", "X", 1 if i % 2 else -1), mk(f"x{i}", "c", "R", 0)]
        for i in range(8):
            rows += [mk(f"y{i}", "c", "Y", 1 if i % 2 else -1), mk(f"y{i}", "c", "R", 0)]
        U = T.cat_values(comps(rows), "TONE")
        self.assertAlmostEqual(U["X"]["value"], U["Y"]["value"], places=9)
        self.assertGreater(U["X"]["n_comparisons"], U["Y"]["n_comparisons"])

    def test_frequency_does_not_enter_direction_on_a_fixture(self):
        """Dropping every second answer of the most-named brand of each category (a lower naming frequency for
        that brand only) leaves the sign of its TONE unchanged."""
        _, rows, _, _ = T.read_fixture(FX / "confirmed")
        w = T.Wave("t5", rows["t5"])
        full = T.measure(w, "TONE")
        for cat in w.cats:
            c = w.comps()[cat]
            top = c.brands[int(np.argmax(c.n_contrib))]
            seen, keep = 0, []
            for r in w.by_cat[cat]:
                keep.append(r)
            ans = sorted({r["answer_id"] for r in keep if r["brand"] == top})
            drop = set(ans[::2])
            thinned = [r for r in keep if not (r["brand"] == top and r["answer_id"] in drop)]
            U = T.cat_values(T.Comps(thinned), "TONE")
            self.assertEqual(np.sign(U[top]["value"]), np.sign(full[(cat, top)]["value"]), (cat, top))

    def test_answer_register_does_not_enter(self):
        """Shifting every window of an answer by the same step (a warmer register) changes no comparison, so
        TONE is unchanged, while S_ref (the failed measure) moves."""
        rng = np.random.default_rng(7)
        base, warm = [], []
        for i in range(60):
            names = rng.choice(list("ABCDEFG"), size=3, replace=False)
            vals = rng.integers(-2, 2, size=3)                  # -2..1, so +1 stays on the scale
            shift = 1 if i % 2 else 0
            for b, v in zip(names, vals):
                base.append(mk(f"a{i}", "c", b, int(v)))
                warm.append(mk(f"a{i}", "c", b, int(v) + shift))
        Tb, Tw = T.cat_values(comps(base), "TONE"), T.cat_values(comps(warm), "TONE")
        for b in Tb:
            self.assertAlmostEqual(Tb[b]["value"], Tw[b]["value"], places=12)
        Sb, Sw = T.cat_values(comps(base), "S_ref"), T.cat_values(comps(warm), "S_ref")
        self.assertTrue(any(abs(Sb[b]["value"] - Sw[b]["value"]) > 1 for b in Sb if Sb[b]["rated"]))

    def test_s_cat_identity(self):
        _, rows, P, _ = T.read_fixture(FX / "marginal")
        w = T.Wave("t5", rows["t5"])
        a = T.sep(T.measure(w, "S_ref"), P["t5"], D, boot=False)
        b = T.sep(T.measure(w, "S_cat"), P["t5"], D, boot=False)
        self.assertEqual(a["rho"], b["rho"])
        self.assertEqual(a["n"], b["n"])

    def test_identity_failure_halts(self):
        _, rows, P, C = T.read_fixture(FX / "confirmed")
        waves = {wn: T.Wave(wn, rows[wn]) for wn in T.WAVES}
        sj = T.stage_j_core(waves, {"J1": "claude-opus-5-5", "J2": "gpt-6.1-sol"}, D)
        real = T.cat_values

        def broken(c, kind, floor=T.FLOOR, prior=T.PRIOR, u=None):
            out = real(c, kind, floor, prior, u)
            if kind == "S_cat":
                for v in out.values():
                    if v["rated"]:
                        v["value"] = -v["value"]
            return out
        with mock.patch.object(T, "cat_values", broken):
            with self.assertRaises(T.Halt):
                T.stage_c_core(waves, P, C, {"J1": "claude-opus-5-5"}, D, sj, sensitivities=False)

    def test_s_ref_equals_v1_11_brand_score(self):
        sj, _, _ = world("falsified")
        for wn in T.WAVES:
            self.assertTrue(sj["S_ref_vs_v1_11_brand_score"][wn]["matches_v1_11_brand_score"])

    def test_s_res_out_of_sample(self):
        rows4 = [mk(f"a{i}", "c", b, v, wave="t4") for i in range(6) for b, v in (("A", 1), ("B", 0), ("C", -1))]
        rows5 = [mk(f"a{i}", "c", b, v) for i in range(6) for b, v in (("A", 1), ("B", 0), ("C", -1))]
        waves = {"t4": T.Wave("t4", rows4), "t5": T.Wave("t5", rows5)}
        P = {"t4": {("c", "A"): 80.0, ("c", "B"): 50.0, ("c", "C"): 20.0},
             "t5": {("c", "A"): 80.0, ("c", "B"): 50.0, ("c", "C"): 20.0}}
        SR, fits = T.s_res(waves, P)
        self.assertTrue(fits["c"]["fitted"])
        self.assertAlmostEqual(fits["c"]["slope"], 50.0 / 60.0)
        for k in SR:
            self.assertAlmostEqual(SR[k]["value"], 0.0, places=9)
        P["t4"] = {("c", "A"): 50.0}
        SR, fits = T.s_res(waves, P)
        self.assertFalse(fits["c"]["fitted"])
        self.assertFalse(any(v["rated"] for v in SR.values()))


# ======================================================================================
# E. Pins, stage order, inputs, lock manifest
# ======================================================================================
class TestPinsAndOrder(unittest.TestCase):
    def test_fit_bt_is_v1_16s(self):
        self.assertIn(T.V116_TAG, T.fit_bt.__code__.co_filename)
        W = np.array([[0, 3, 1], [1, 0, 2], [2, 1, 0]], float)
        th = T.fit_bt(W)
        self.assertEqual(th.shape, (3,))
        self.assertGreater(th[0], th[1])

    def test_v1_16_blob_mismatch_halts(self):
        with mock.patch.object(T, "V116_BLOB", "0" * 40):
            with self.assertRaises(T.Halt):
                T.load_v116()

    def test_code_pins(self):
        got = T.verify_code_pins()
        self.assertEqual(len(got), len(T.CODE_PINS) + 1)

    def test_real_stages_refuse_before_lock(self):
        if T.tag_exists():
            self.skipTest("tag exists")
        out = Path(tempfile.mkdtemp(prefix="v121_lock_"))
        with self.assertRaises(T.Halt):
            T.run_stage_j(out, out, out, T.Draws())
        with self.assertRaises(T.Halt):
            T.run_stage_c(out, out, out, T.Draws())
        with self.assertRaises(T.Halt):
            T.run_exploratory(out, T.Draws())
        self.assertEqual(T.main(["--stage", "J", "--out", str(out)]), 3)
        self.assertEqual(T.main(["--stage", "J", "--draws", "5", "--out", str(out)]), 3)

    def test_stage_c_needs_stage_j_and_unchanged_outcomes(self):
        out = Path(tempfile.mkdtemp(prefix="v121_order_"))
        with self.assertRaises(T.Halt):
            T.read_stage_j(out)
        _, rows, _, _ = T.read_fixture(FX / "two_cats")
        T.write_stage_j(out, rows, lambda ws: T.stage_j_core(ws, {"J1": "claude-opus-5-5", "J2": "x"}, D))
        T.read_stage_j(out)
        p = out / T.OUTCOMES_NAME["t5"]
        p.write_text(p.read_text().replace("VALID,1,", "VALID,2,", 1))
        with self.assertRaises(T.Halt):
            T.read_stage_j(out)

    def test_canonical_table_round_trip(self):
        _, rows, _, _ = T.read_fixture(FX / "confirmed")
        b = T.unit_rows_csv_bytes(rows["t5"])
        again = T.parse_unit_rows(b.decode())
        self.assertEqual(T.unit_rows_csv_bytes(again), b)

    def test_build_unit_rows_v1_20_rule_and_s_att(self):
        """Attempt 1 is a prose-wrapped JSON object (counts under v1.20's rule, not under v1.11's); attempt 2 is a
        clean object with another valence. Primary = attempt 1; S-ATT (v1.11 first) = attempt 2."""
        obj = {"refers_to_brand": True, "evaluative": True, "mixed": False, "valence": 1, "evidence": "good"}
        obj2 = dict(obj, valence=2)
        roles = {"J1": "claude-opus-5-5", "J2": "gpt-6.1-sol"}
        recs = [{"role": "J1", "unit_id": "u1", "pass": "main", "judge_model": roles["J1"], "attempt": 1,
                 "status": "ok", "served_ok": True, "finish_reason": "end_turn", "text": "Here: " + json.dumps(obj)},
                {"role": "J1", "unit_id": "u1", "pass": "main", "judge_model": roles["J1"], "attempt": 2,
                 "status": "ok", "served_ok": True, "finish_reason": "end_turn", "text": json.dumps(obj2)},
                {"role": "J2", "unit_id": "u1", "pass": "main", "judge_model": roles["J2"], "attempt": 1,
                 "status": "ok", "served_ok": True, "finish_reason": "completed", "text": json.dumps(obj)}]
        units = [{"unit_id": "u1", "wave": "t5", "category": "v0.19", "brand": "A", "answer_id": "a1",
                  "model": "gpt-6-astra", "provider": "openai", "judged": "1", "j2": "1", "selfcon": "0"},
                 {"unit_id": "u2", "wave": "t5", "category": "v0.19", "brand": "B", "answer_id": "a1",
                  "model": "gpt-6-astra", "provider": "openai", "judged": "0", "j2": "0", "selfcon": "0"}]
        rows = T.build_unit_rows(units, recs, roles, "t5")
        self.assertEqual(len(rows), 1)                          # judged = 0 is not a scored window
        self.assertEqual((rows[0]["J1"]["status"], rows[0]["J1"]["valence"]), (T.VALID, 1))
        self.assertEqual((rows[0]["J1att"]["status"], rows[0]["J1att"]["valence"]), (T.VALID, 2))
        self.assertEqual(rows[0]["J2"]["valence"], 1)
        with self.assertRaises(T.Halt):
            T.build_unit_rows(units, recs, roles, "t4")

    def test_presence_t5_reading(self):
        d = Path(tempfile.mkdtemp(prefix="v121_p5_"))
        p = d / "v45_unit_table.csv"
        p.write_text("substrate,brand,P_t5_S0,phi_t5_S0,phi_partition_t5_S0\n"
                     "v0.19,A,50.0,3.0,defined\nv0.19,B,20.0,,saturated\nv0.19,C,,,undefined\n")
        P, C, _ = T.presence_t5(p)
        self.assertEqual(P, {("v0.19", "A"): 50.0, ("v0.19", "B"): 20.0})
        self.assertAlmostEqual(C[("v0.19", "A")], 100 * (1 - 3 / 9))
        self.assertEqual(C[("v0.19", "B")], 100.0)
        self.assertNotIn(("v0.19", "C"), C)

    def test_exploratory_core_describes_without_verdicts(self):
        _, rows, P, C = T.read_fixture(FX / "confirmed")
        w = T.Wave("t1", [dict(r, wave="t1") for r in rows["t4"]])
        doc = T.exploratory_core({"t1": w}, {"t1": P["t4"]}, {"t1": C["t4"]}, D)
        self.assertIn("EXPLORATORY", doc["label"])
        row = doc["per_wave"]["t1"]["TONE"]
        self.assertNotIn("verdict", row["rho_w_with_P"])
        self.assertGreater(row["rated"], 0)

    def test_lock_manifest_format(self):
        txt = T.lock_manifest_text()
        lines = txt.splitlines()
        self.assertTrue(all(re.fullmatch(r"[0-9a-f]{64}  \S.*", ln) for ln in lines))
        paths = [ln.split("  ", 1)[1] for ln in lines]
        self.assertIn(T.PREREG_REL, paths)
        self.assertIn("osf/methodology/v1_21/scripts/score_v1_21.py", paths)
        self.assertIn("osf/methodology/v1_21/tests/test_score_v1_21.py", paths)
        self.assertFalse(any("__pycache__" in x for x in paths))



def _git_t(cwd, *args):
    import subprocess
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "init.defaultBranch=main",
                    "-c", "tag.gpgSign=false", "-c", "commit.gpgSign=false", *args],
                   cwd=cwd, check=True, capture_output=True)


class TestU0Misses(unittest.TestCase):
    """n_named (H6_t5) takes U0's extraction misses; U0's record is required at t5 (no default of 0)."""

    def _u0(self, d, misses, sha="abc", per_set=None):
        (d / "prereg").mkdir(parents=True, exist_ok=True)
        doc = {"units_file": {"path": "units_v1_21.csv", "sha256": sha}, "extraction_misses": misses}
        if per_set is not None:
            doc["per_set"] = per_set
        (d / T.U0_T5_REL).write_text(json.dumps(doc))

    def test_misses_counted_per_unit_and_zero_explicit(self):
        d = Path(tempfile.mkdtemp(prefix="v121_u0_"))
        self._u0(d, [{"set": "F t5 v0.19", "answer_id": "a1", "brand": "A"},
                     {"set": "F t5 v0.19", "answer_id": "a2", "brand": "A"},
                     {"set": "F t5 v0.20", "answer_id": "a3", "brand": "B"}],
                 per_set={"F t5 v0.19": {"mentions": 100, "misses": 2}, "F t5 v0.20": {"mentions": 100, "misses": 1}})
        r = T.load_u0_misses(d, "abc")
        self.assertEqual(r["by_unit"], {"v0.19|A": 2, "v0.20|B": 1})
        self.assertEqual(r["n_misses"], 3)
        self.assertEqual(T.misses_from_stage_j({"t5_u0": r}), {("v0.19", "A"): 2, ("v0.20", "B"): 1})
        self._u0(d, [])
        self.assertEqual(T.load_u0_misses(d, "abc")["n_misses"], 0)

    def test_refusals(self):
        d = Path(tempfile.mkdtemp(prefix="v121_u0_"))
        with self.assertRaisesRegex(T.Halt, "missing"):
            T.load_u0_misses(d, "abc")
        self._u0(d, [], sha="other")
        with self.assertRaisesRegex(T.Halt, "another unit table"):
            T.load_u0_misses(d, "abc")
        (d / T.U0_T5_REL).write_text(json.dumps({"units_file": {"sha256": "abc"}}))
        with self.assertRaisesRegex(T.Halt, "no extraction_misses"):
            T.load_u0_misses(d, "abc")
        self._u0(d, [{"set": "F t4 v0.19", "answer_id": "a1", "brand": "A"}])
        with self.assertRaises(T.Halt):
            T.load_u0_misses(d, "abc")
        self._u0(d, [], per_set={"F t5 v0.19": {"mentions": 100, "misses": 6}})
        with self.assertRaisesRegex(T.Halt, "above 5%"):
            T.load_u0_misses(d, "abc")
        with self.assertRaisesRegex(T.Halt, "no t5 U0 record"):
            T.misses_from_stage_j({})

    def test_misses_enter_n_named(self):
        _, rows, _, _ = T.read_fixture(FX / "two_cats")
        w5 = T.Wave("t5", rows["t5"])
        k = (w5.rows[0]["category"], w5.rows[0]["brand"])
        base = T.n_named_t5(w5)
        self.assertEqual(T.n_named_t5(w5, {k: 2})[k], base[k] + 2)

    def test_stage_c_passes_u0_misses(self):
        """run_stage_c (lock, pins and P mocked) feeds Stage J's U0 misses into n_named and refuses without them."""
        meta, rows, P, C = T.read_fixture(FX / "two_cats")
        k = (rows["t5"][0]["category"], rows["t5"][0]["brand"])
        for with_u0 in (True, False):
            out = Path(tempfile.mkdtemp(prefix="v121_c_"))
            extra = {"t5_u0": {"by_unit": {f"{k[0]}|{k[1]}": 3}, "n_misses": 3}} if with_u0 else {}
            T.write_stage_j(out, rows, lambda ws: T.stage_j_core(ws, meta["roles"], D, extra))
            seen = {}
            real = T.stage_c_core

            def spy(*a, **kw):
                seen["misses"] = kw.get("misses")
                return real(*a, **dict(kw, sensitivities=False))

            with mock.patch.object(T, "tag_exists", return_value=True), \
                    mock.patch.object(T, "verify_code_pins", return_value={}), \
                    mock.patch.object(T, "v45_pins", return_value={"files": {}}), \
                    mock.patch.object(T, "presence_t4", return_value=(P["t4"], C["t4"], "h4")), \
                    mock.patch.object(T, "presence_t5", return_value=(P["t5"], C["t5"], "h5")), \
                    mock.patch.object(T, "v120_h2", return_value=None), \
                    mock.patch.object(T, "stage_c_core", side_effect=spy):
                if with_u0:
                    doc = T.run_stage_c(out, out / "s1.json", out / "p.csv", D, log=lambda *_: None)
                    self.assertEqual(seen["misses"], {k: 3})
                    self.assertEqual(doc["inputs"]["t5_u0_misses"]["n_misses"], 3)
                else:
                    with self.assertRaisesRegex(T.Halt, "no t5 U0 record"):
                        T.run_stage_c(out, out / "s1.json", out / "p.csv", D, log=lambda *_: None)


class TestV45Pins(unittest.TestCase):
    """Section 9, Pins: v0.45's raw record (blob at v0.45-acquisition-locked), coded tables and scored unit table."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="v121_v45_"))
        self.repo = self.tmp / "v45"
        _git_t(self.tmp, "init", str(self.repo))
        raw = self.repo / T.V45_RAW_REL
        raw.parent.mkdir(parents=True)
        raw.write_text('{"id": 1}\n')
        _git_t(self.repo, "add", "-A")
        _git_t(self.repo, "commit", "-m", "acq")
        _git_t(self.repo, "tag", "-a", T.V45_ACQ_TAG, "-m", "acq")
        for rel in T.V45_CODED_REL:
            p = self.repo / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("substrate,brand\n")
        (self.repo / T.V45_TABLE_REL).write_text("substrate,brand,P_t5_S0\n")
        _git_t(self.repo, "add", "-A")
        _git_t(self.repo, "commit", "-m", "coded and scored")
        self.table = self.repo / T.V45_TABLE_REL

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_records_every_file(self):
        r = T.v45_pins(self.table)
        self.assertEqual(set(r["files"]), {T.V45_RAW_REL, T.V45_TABLE_REL, *T.V45_CODED_REL})
        self.assertEqual(len(r["files"]), 12)
        self.assertEqual(r["files"][T.V45_RAW_REL]["sha256"], T.sha256_bytes(b'{"id": 1}\n'))
        self.assertEqual(r["files"][T.V45_RAW_REL]["tag"], T.V45_ACQ_TAG)

    def test_uncommitted_change_halts(self):
        (self.repo / T.V45_CODED_REL[3]).write_text("changed\n")
        with self.assertRaisesRegex(T.Halt, "committed at HEAD"):
            T.v45_pins(self.table)

    def test_missing_coded_file_halts(self):
        (self.repo / T.V45_CODED_REL[0]).unlink()
        with self.assertRaisesRegex(T.Halt, "missing v0.45 file"):
            T.v45_pins(self.table)

    def test_raw_changed_after_acquisition_tag_halts(self):
        (self.repo / T.V45_RAW_REL).write_text('{"id": 2}\n')
        _git_t(self.repo, "commit", "-am", "edit raw")
        with self.assertRaisesRegex(T.Halt, "at tag"):
            T.v45_pins(self.table)

    def test_presence_path_must_be_v45_table(self):
        with self.assertRaisesRegex(T.Halt, "must be"):
            T.v45_pins(self.tmp / "elsewhere.csv")


class TestWriteAnchor(unittest.TestCase):
    """--write-anchor on a throwaway repository with a bare remote (no network)."""

    def _git(self, cwd, *args):
        import subprocess
        subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "init.defaultBranch=main",
                        "-c", "tag.gpgSign=false", "-c", "commit.gpgSign=false", *args],
                       cwd=cwd, check=True, capture_output=True)

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.remote = self.tmp / "remote.git"
        self.repo = self.tmp / "repo"
        self._git(self.tmp, "init", "--bare", str(self.remote))
        self._git(self.tmp, "init", str(self.repo))
        pre = self.repo / T.V121 / "prereg"
        pre.mkdir(parents=True)
        (pre / "PRE.md").write_text("prereg\n")
        (self.repo / T.V121 / "anchor").mkdir()
        (self.repo / T.V121 / "anchor" / "DEVIATIONS.md").write_text("Entry 0\n")
        rel = T.V121 + "/prereg/PRE.md"
        (self.repo / T.MANIFEST_REL).write_text(f"{T.sha256_file(pre / 'PRE.md')}  {rel}\n")
        self._git(self.repo, "add", "-A")
        self._git(self.repo, "commit", "-m", "lock")
        self._git(self.repo, "remote", "add", "origin", str(self.remote))
        self._git(self.repo, "push", "origin", "HEAD:main")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _tag(self, annotated=True):
        if annotated:
            self._git(self.repo, "tag", "-a", T.PREREG_TAG, "-m", "lock")
        else:
            self._git(self.repo, "tag", T.PREREG_TAG)

    def test_refuses_before_tag(self):
        with self.assertRaises(T.Halt):
            T.write_anchor("osf", root=self.repo)

    def test_refuses_unpushed_tag(self):
        self._tag()
        with self.assertRaisesRegex(T.Halt, "push the tag"):
            T.write_anchor("osf", root=self.repo)

    def test_refuses_lightweight_tag(self):
        self._tag(annotated=False)
        self._git(self.repo, "push", "origin", T.PREREG_TAG)
        with self.assertRaisesRegex(T.Halt, "lightweight"):
            T.write_anchor("osf", root=self.repo)

    def test_refuses_without_osf_deposit(self):
        self._tag()
        self._git(self.repo, "push", "origin", T.PREREG_TAG)
        with self.assertRaisesRegex(T.Halt, "osf-deposit"):
            T.write_anchor("  ", root=self.repo)

    def test_writes_once_with_v1_20_fields(self):
        self._tag()
        self._git(self.repo, "push", "origin", T.PREREG_TAG)
        p = T.write_anchor("https://osf.io/x/", root=self.repo)
        rec = json.loads(p.read_text())
        for k in ("tag", "tag_object", "commit", "tree", "branch", "tagger_date", "remote_tag_ref",
                  "recorded_utc", "repository", "osf_deposit", "locked_files"):
            self.assertIn(k, rec)
        self.assertEqual(rec["tag"], T.PREREG_TAG)
        self.assertEqual(set(rec["locked_files"]),
                         {T.V121 + "/prereg/PRE.md", T.MANIFEST_REL, T.DEVIATIONS_REL})
        self.assertEqual(rec["locked_files"][T.V121 + "/prereg/PRE.md"]["sha256"],
                         T.sha256_bytes(b"prereg\n"))
        with self.assertRaisesRegex(T.Halt, "written once"):
            T.write_anchor("https://osf.io/x/", root=self.repo)

    def test_refuses_manifest_mismatch(self):
        (self.repo / T.V121 / "prereg" / "PRE.md").write_text("changed\n")
        self._git(self.repo, "commit", "-am", "edit")
        self._tag()
        self._git(self.repo, "push", "origin", T.PREREG_TAG)
        with self.assertRaisesRegex(T.Halt, "manifest says"):
            T.write_anchor("osf", root=self.repo)


if __name__ == "__main__":
    unittest.main()
