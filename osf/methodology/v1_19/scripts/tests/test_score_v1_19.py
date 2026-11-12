#!/usr/bin/env python3
"""
Unit tests for score_v1_19.py (v1.19 Coverage Paper B re-analysis, scorer skeleton r0; r1 adds the classes
R1Descriptives and SC3). Synthetic data only: no v1.12 answer exists or is read, no t4 value is computed, no API is
called. Run from the repository root:

    python3 -m unittest discover -s osf/methodology/v1_19/scripts/tests -p "test_*.py" -v
"""
import itertools
import math
import sys
import unittest
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import score_v1_19 as B   # noqa: E402

A = B.A


class Conditionality(unittest.TestCase):
    def doc(self, v, legs=None):
        return {"paper_A_verdict": {"verdict": v, "legs": legs or {}}}

    def test_pass_runs(self):
        self.assertTrue(B.paper_b_decision(self.doc("PASS"))["run"])

    def test_marginal_needs_recorded_decision(self):
        d = B.paper_b_decision(self.doc("MARGINAL", {"H4_Reliability": "MARGINAL"}))
        self.assertFalse(d["run"])
        self.assertIn("pending", d["status"])
        d = B.paper_b_decision(self.doc("MARGINAL", {"H4_Reliability": "MARGINAL"}),
                               {"go": True, "date": "2026-11-20", "text": "run Paper B"})
        self.assertTrue(d["run"])
        self.assertEqual(d["marginal_legs"], ["H4_Reliability"])
        self.assertFalse(B.paper_b_decision(self.doc("MARGINAL"), {"go": True})["run"])   # undated: not a record

    def test_fail_paths_not_run_without_statistics(self):
        for v in ("FAIL", "UNDETERMINED", "INSTRUMENT FAIL"):
            d = B.paper_b_decision(self.doc(v))
            self.assertFalse(d["run"])
            rec = B.score_b({"a_doc": self.doc(v)})
            self.assertEqual(rec["status"], "NOT RUN")
            self.assertIsNone(rec["statistics"])

    def test_unknown_verdict_refused(self):
        with self.assertRaises(B.Refused):
            B.paper_b_decision(self.doc("PASS (H6 CONFIRMED cross-panel)"))
        with self.assertRaises(B.Refused):
            B.paper_b_decision({})


class ImportNotFork(unittest.TestCase):
    def test_imported_scorer_is_the_locked_file(self):
        self.assertEqual(Path(A.__file__).resolve(), (B.ROOT / "osf/methodology/v1_12/scripts/score_v1_12.py").resolve())
        self.assertTrue(B.parity_b_p0()["passed"])

    def test_paper_A_scorer_computes_no_paper_B_statistic(self):
        src = Path(A.__file__).read_text(encoding="utf-8").lower()
        for term in ("cliff", "silhouette", "adjusted rand", "identity", "il_direct", "phantom", "typolog",
                     "excess", "split_code", "v1.19", "v1_19"):
            self.assertNotIn(term, src, term)


class Splits(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.design = A.probe_design(A.load_probes())

    def test_64_balanced_complementary_splits(self):
        codes = B.split_codes()
        self.assertEqual(len(codes), 64)
        seen = set()
        for c in codes:
            p1, p2 = B.split_parts(self.design, c)
            for s in self.design["ceps"]:
                self.assertEqual(sorted(p1[s] + p2[s]), sorted(self.design["ceps"][s]))
                self.assertEqual(sorted(self.design["w"][p] for p in p1[s]), sorted(B.W))
                self.assertEqual(sorted(self.design["w"][p] for p in p2[s]), sorted(B.W))
            key = frozenset(frozenset(v) for v in (tuple(sorted(sum(p1.values(), []))),
                                                   tuple(sorted(sum(p2.values(), [])))))
            self.assertNotIn(key, seen)
            seen.add(key)

    def test_code_0_is_paper_A_split(self):
        p1, p2 = B.split_parts(self.design, 0)
        for s in self.design["ceps"]:
            self.assertEqual(sorted(p1[s]), sorted(self.design["half"]["A"][s]))
            self.assertEqual(sorted(p2[s]), sorted(self.design["half"]["B"][s]))


class Statistics(unittest.TestCase):
    def test_cliffs_delta_equals_brute_force(self):
        rng = np.random.default_rng(1)
        v = rng.integers(0, 6, 40).astype(float)
        f = rng.random(40) < 0.4
        g = np.array(["a"] * 20 + ["b"] * 20)
        num = den = 0
        for grp in ("a", "b"):
            idx = np.where(g == grp)[0]
            for i in idx[f[idx]]:
                for j in idx[~f[idx]]:
                    num += int(v[i] > v[j]) - int(v[i] < v[j])
                    den += 1
        self.assertAlmostEqual(B.cliffs_delta_within(v, f, g), num / den, places=12)

    def test_inclusion_probs_exact(self):
        slot = np.array([0, 0, 1, 2, 2, 2])
        delta = np.array([0.3, -0.5, 0.1])
        n = 2
        w = np.exp(delta[slot])
        tot = 0.0
        acc = np.zeros(len(slot))
        for comb in itertools.combinations(range(len(slot)), n):
            p = np.prod(w[list(comb)])
            tot += p
            acc[list(comb)] += p
        np.testing.assert_allclose(B.inclusion_probs(slot, delta, n), acc / tot, rtol=1e-12)
        np.testing.assert_allclose(B.inclusion_probs(slot, np.zeros(3), 3), np.full(6, 0.5), rtol=1e-12)
        self.assertAlmostEqual(B.inclusion_probs(slot, delta, 4).sum(), 4.0, places=10)

    def test_excess_profiles_sum_to_zero(self):
        w = B.synthetic_world(True, 7)
        prof = B.excess_profiles(w["ans"], w["brands"], w["design"]["ceps"], w["design"], w["panel"])
        sums = [v[0].sum() for v in prof.values() if v[1] > 0]
        self.assertTrue(sums)
        self.assertLess(max(abs(s) for s in sums), 1e-9)

    def test_ari_and_silhouette(self):
        a = [1, 1, 2, 2, 3, 3]
        self.assertAlmostEqual(B.ari(a, ["x", "x", "y", "y", "z", "z"]), 1.0)
        X = np.array([[0.0], [0.1], [5.0], [5.1]])
        s = B.silhouette(X, [1, 1, 2, 2])
        self.assertGreater(s, 0.9)
        self.assertTrue(math.isnan(B.silhouette(X, [1, 1, 1, 1])))

    def test_band_signed(self):
        self.assertEqual(B.band_signed(-0.4, 0.01, 0.30, 0.15), "CONFIRMED")
        self.assertEqual(B.band_signed(0.4, 0.01, 0.30, 0.15), "CONFIRMED_REVERSED")
        self.assertEqual(B.band_signed(0.4, 0.20, 0.30, 0.15), "MARGINAL")
        self.assertEqual(B.band_signed(0.1, 0.01, 0.30, 0.15), "FALSIFIED")
        self.assertEqual(B.band_signed(float("nan"), 0.01, 0.30, 0.15), "UNDETERMINED")

    def test_typology_matrix_exhaustive(self):
        cells = set()
        for rep in ("CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED"):
            for i, a, r in itertools.product((True, False), repeat=3):
                c = B.typology_cell(rep, i, a, r)
                self.assertTrue(c)
                cells.add(c.split(" [")[0])
        self.assertEqual(cells, {"LAYERED", "BORROWED", "AUTONOMOUS", "PRESENCE-DEPENDENT", "RESIDUAL-ONLY",
                                 "UNSTRUCTURED", "NO TYPOLOGY (profiles do not replicate); structure reported descriptively"})

    def test_il_matrix_exhaustive(self):
        for v in ("CONFIRMED", "CONFIRMED_REVERSED", "FALSIFIED", "MARGINAL"):
            for pr, band in ((0.4, "CONFIRMED"), (0.2, "MIDDLE"), (0.05, "NULL")):
                self.assertTrue(B.il_matrix(v, pr, band))

    def test_il_from_t4(self):
        rows = []
        for i, (ch, pid) in enumerate((("R_cat", "q1"), ("R_cat", "q2"), ("R_cult", "q4"), ("R_cult", "q5"))):
            rows.append({"call_id": f"c{i}", "substrate": "v0.20", "brand": "X", "model": "m", "condition": "S0",
                         "run": 1, "probe_id": pid, "mentioned": "1" if ch == "R_cult" or i == 0 else "0"})
        il = B.il_from_t4(rows, {"q1": "R_cat", "q2": "R_cat", "q4": "R_cult", "q5": "R_cult"}, [("v0.20", "X")], ["m"])
        self.assertAlmostEqual(il[("v0.20", "X")]["il"], 1.0 - 0.5)
        self.assertAlmostEqual(il[("v0.20", "X")]["pi_hat"], 0.75)

    def test_defunct_floor(self):
        w = B.synthetic_world(False, 3)
        empty = {k: frozenset(v - set(B.DEFUNCT)) for k, v in w["ans"].items()}
        r = B.h34_defunct(empty, w["design"], w["panel"], B.DEFUNCT, n_draws=100)
        self.assertEqual(r["verdict"], "UNDETERMINED")


class R1Descriptives(unittest.TestCase):
    """r1: D34 (Fisker beside D; naive / caveated by W and per brand) and D36 (category and type mean profiles)."""
    DESIGN = {"w": {"c1": "when", "c2": "why", "c3": "with whom"}}

    def test_caveat_window_rule(self):
        self.assertTrue(B.is_caveated("Pontiac" + " " * 140 + "defunct", "Pontiac"))
        self.assertFalse(B.is_caveated("Pontiac" + " " * 150 + "defunct", "Pontiac"))
        self.assertTrue(B.is_caveated("The DISCONTINUED " + "x" * 100 + " pontiac", "Pontiac"))   # case-insensitive
        self.assertFalse(B.is_caveated("A defunct brand.", "Pontiac"))                           # name absent: naive
        self.assertFalse(B.is_caveated(None, "Pontiac"))

    def test_d34_fisker_beside_d(self):
        ans = {("v0.22", "m", "c1", 1): frozenset({"Pontiac", "Fisker", "Ford"}),
               ("v0.22", "m", "c1", 2): frozenset({"Saturn"}),
               ("v0.22", "m", "c2", 1): frozenset({"Fisker"}),
               ("v0.22", "m", "c3", 1): frozenset({"Ford"})}
        texts = {("v0.22", "m", "c1", 1): "Pontiac (no longer made). Ford. " + "y" * 200 + " Fisker.",
                 ("v0.22", "m", "c1", 2): "Saturn is great.",
                 ("v0.22", "m", "c2", 1): "Fisker went bankrupt."}
        keys = sorted(ans)
        d = B.d34_counts(ans, keys, B.DEFUNCT, texts, self.DESIGN)
        self.assertEqual(d["answers_naming_any"], 2)
        self.assertEqual(d["answers_naming_any_by_W"]["when"], 2)
        self.assertEqual(d["per_brand"]["Pontiac"], {"answers": 1, "by_W": {x: int(x == "when") for x in B.W},
                                                     "naive": 0, "caveated": 1})
        self.assertEqual(d["per_brand"]["Saturn"]["naive"], 1)
        self.assertEqual(d["mentions_by_W"]["caveated"]["when"], 1)
        self.assertEqual(d["mentions_by_W"]["naive"]["when"], 1)
        f = B.d34_counts(ans, keys, ["Fisker"], texts, self.DESIGN)
        self.assertEqual(f["per_brand"]["Fisker"]["answers"], 2)
        self.assertEqual(f["per_brand"]["Fisker"]["by_W"]["when"], 1)
        self.assertEqual(f["per_brand"]["Fisker"]["by_W"]["why"], 1)
        self.assertEqual((f["per_brand"]["Fisker"]["naive"], f["per_brand"]["Fisker"]["caveated"]), (1, 1))
        self.assertNotIn("mentions_by_W", B.d34_counts(ans, keys, ["Fisker"], None, self.DESIGN))

    def test_fisker_does_not_enter_the_defunct_test(self):
        w = B.synthetic_world(True, 119390)
        base = B.h34_defunct(w["ans"], w["design"], w["panel"], B.DEFUNCT, texts=w["texts"], n_draws=200)
        withf = B.h34_defunct(w["ans"], w["design"], w["panel"], B.DEFUNCT, texts=w["texts"], n_draws=200,
                              fisker="v0.22-b00")
        for k in ("verdict", "p_mc", "max_W_share", "null_W_shares", "answers_naming_defunct", "by_W", "caveat"):
            self.assertEqual(base.get(k), withf.get(k))
        self.assertIn("note", base["D34"]["Fisker_beside_D"])
        self.assertEqual(withf["D34"]["Fisker_beside_D"]["brands"], ["v0.22-b00"])
        self.assertEqual(withf["D34"]["D"]["mentions_by_W"], {lab: {x: base["caveat"][lab].get(x, 0) for x in B.W}
                                                             for lab in ("naive", "caveated")})
        doc = B.score_b(dict(w, fisker="v0.22-b00"), 20, 5, ("34",))
        self.assertEqual(doc["H34_Defunct_Occupancy"]["D34"]["Fisker_beside_D"]["per_brand"]["v0.22-b00"]["answers"],
                         sum(1 for k in w["ans"] if k[0] == "v0.22" and k[1] in w["panel"] and "v0.22-b00" in w["ans"][k]))

    def test_d36_profiles(self):
        keys = [("v0.20", "a"), ("v0.20", "b"), ("v0.21", "c"), ("v0.21", "d")]
        X = np.arange(28, dtype=float).reshape(4, 7)
        d = B.d36_profiles(X, keys, np.array([1, 2, 1, 2]), 2)
        np.testing.assert_allclose(list(d["category_mean_profiles"]["v0.20"]["mean_excess"].values()), X[:2].mean(0))
        np.testing.assert_allclose(list(d["category_mean_profiles"]["v0.21"]["mean_excess"].values()), X[2:].mean(0))
        self.assertEqual(d["type_mean_profiles"]["type 1"]["n"], 2)
        self.assertEqual(d["type_mean_profiles"]["type 1"]["n_by_category"], {"v0.20": 1, "v0.21": 1})
        np.testing.assert_allclose(list(d["type_mean_profiles"]["type 2"]["mean_excess"].values()), X[[1, 3]].mean(0))
        self.assertEqual(list(d["type_mean_profiles"]["type 2"]["mean_excess"]), B.W)
        d1 = B.d36_profiles(X, keys, np.ones(4, int), 1)
        self.assertIsNone(d1["type_mean_profiles"])
        w = B.synthetic_world(True, 119390)
        st = B.score_b(w, 20, 5, ("36",))["H36_Structure"]
        self.assertEqual(st["D36_profiles"]["units"], st["n"])
        self.assertEqual(sum(v["n"] for v in st["D36_profiles"]["category_mean_profiles"].values()), st["n"])


class SC3(unittest.TestCase):
    """r1: S-C3 (Claude Opus 5.5 in place of Claude Fable 5.2) exercised on a world holding Paper A's four models."""

    def test_c3_panel_as_recorded(self):
        w = B.synthetic_world_a4(5)
        self.assertEqual(B.c3_panel(w), list(A.PANELS["C3"]))
        w["a_doc"]["panels"] = A.select_panels([A.GEM4])[1]
        self.assertEqual(B.c3_panel(w), [A.OPUS55, A.GPT6])        # a model dropped under v1.12 7.3 stays out
        w["a_doc"]["panels"] = A.select_panels([A.OPUS55])[1]
        self.assertIsNone(B.c3_panel(w))                             # Opus 5.5 dropped: no S-C3
        self.assertIsNone(B.c3_panel(B.synthetic_world(True, 5)))   # N3-only answers: no S-C3

    def test_s_c3_runs_end_to_end(self):
        w = B.synthetic_world_a4(119390)
        self.assertEqual(w["panel"], list(A.PANELS["N3"]))
        self.assertEqual({k[1] for k in w["ans"]}, set(A.PANELS["A4"]))
        base = B.score_b(w, 10, 5)
        s = B.sensitivities(w, base["verdict_summary"], 10, 5, only=("S-C3",))
        self.assertEqual(list(s), ["S-C3"])
        self.assertEqual(s["S-C3"]["panel"], list(A.PANELS["C3"]))
        self.assertEqual(set(s["S-C3"]["verdicts"]), set(base["verdict_summary"]))
        direct = B.score_b(dict(w, panel=list(A.PANELS["C3"])), 10, 5)
        self.assertEqual(s["S-C3"]["verdicts"], direct["verdict_summary"])
        self.assertEqual(direct["panel"], list(A.PANELS["C3"]))
        self.assertGreater(direct["rated_units"], 0)
        self.assertTrue(all(v for v in direct["verdict_summary"].values()))


class Guards(unittest.TestCase):
    def test_real_run_refused_before_lock(self):
        orig = B.tag_on_origin
        try:
            B.tag_on_origin = lambda tag: False
            with self.assertRaises(B.Refused):
                B.real_run_guards()
        finally:
            B.tag_on_origin = orig

    def test_parity_b_p1(self):
        cov = {("v0.20", "X"): 61.0, ("v0.20", "Y"): None}
        ok = [{"substrate": "v0.20", "brand": "X", "cov_star": "61.0"}, {"substrate": "v0.20", "brand": "Y", "cov_star": ""}]
        self.assertTrue(B.parity_b_p1(cov, ok)["passed"])
        bad = [{"substrate": "v0.20", "brand": "X", "cov_star": "60.0"}]
        self.assertFalse(B.parity_b_p1(cov, bad)["passed"])

    def test_cov_star_is_paper_A_function(self):
        w = B.synthetic_world(True, 11)
        _t, cov = B.cov_map_for(w["ans"], w["brands"], w["design"]["ceps"], w["panel"], A.FLOOR_FULL)
        tab = A.coverage_table(w["ans"], w["brands"], w["design"]["ceps"], w["panel"])
        self.assertEqual(cov, A.cov_star_map(tab, w["panel"], A.FLOOR_FULL))


if __name__ == "__main__":
    unittest.main()
