#!/usr/bin/env python3
"""Unit tests for score_v0_63.py on SYNTHETIC data (plus registry-only checks). No answer file is read.
Run: python3 -m unittest osf/v63/scripts/test_score_v0_63.py   (or: python3 osf/v63/scripts/test_score_v0_63.py)"""
import json
import math
import random
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_v0_63 as S  # noqa: E402


def U(cell, cp, rc, ru, cascade=1):
    return {"cell": cell, "cp": cp, "r_cat": rc, "r_cult": ru, "cascade": cascade}


def make_meta():
    m = {}
    m["v0.19"] = {f"h{c}{i}": {"cell": c, "cascade": i + 1, "flags": set()} for c in "AB" for i in range(8)}
    m["v0.19"]["hA2"]["flags"] = {"coi_flagged"}
    m["v0.19"]["hA6"]["flags"] = {"cross_cultural"}
    m["v0.19"]["hB1"]["flags"] = {"cross_cultural"}
    m["v0.19"]["hB2"]["flags"] = {"borderline"}
    for s in ("v0.20", "v0.21"):
        m[s] = {f"{s[-2:]}{c}{i}": {"cell": c, "cascade": i + 1, "flags": set()} for c in "ABC" for i in range(8)}
    m["v0.20"]["20B0"]["flags"] = {"borderline"}
    sizes = {"A": 7, "B": 5, "C": 7, "D": 5}
    m["v0.22"] = {f"a{c}{i}": {"cell": c, "cascade": i + 1, "flags": {"defunct"} if c == "D" else set()}
                  for c, n in sizes.items() for i in range(n)}
    m["v0.23"] = {f"S{i:02d}": {"cell": "-", "cascade": None, "flags": {"conglomerate"} if i % 2 else set()}
                  for i in range(1, 25)}
    m["v0.18"] = {f"f{c}{i}": {"cell": c, "cascade": i + 1, "flags": set()} for c in "ABC" for i in range(8)}
    m["v0.18"]["fA1"]["flags"] = {"borderline"}
    m["v0.18"]["fB3"]["flags"] = {"coi_flagged"}
    return m


def make_archive(meta, seed=1):
    rng = random.Random(seed)
    arch = {w: {} for w in S.WAVES}
    for w, s in S.substrate_waves():
        p = {}
        for b, v in meta[s].items():
            cp = rng.choice([3, 4, 5, 6, 6, 6])
            rc = rng.randint(0, 18)
            ru = 0 if s == "v0.18" else rng.randint(0, 18)
            p[b] = U(v["cell"], cp, rc, ru, v["cascade"])
            if s == "v0.18":
                p[b]["n_b"] = 18
        arch[w][s] = p
    return arch


class TestSpearmanAndStats(unittest.TestCase):
    def test_undefined(self):
        self.assertIsNone(S.spearman([1], [2]))
        self.assertIsNone(S.spearman([1, 1, 1], [1, 2, 3]))      # constant -> undefined
        self.assertIsNone(S.spearman([], []))

    def test_ties_match_scipy(self):
        from scipy.stats import spearmanr
        rng = random.Random(3)
        for _ in range(50):
            n = rng.randint(3, 12)
            x = [rng.randint(0, 3) for _ in range(n)]
            y = [rng.randint(0, 3) for _ in range(n)]
            r = S.spearman(x, y)
            ref = spearmanr(x, y)[0]
            if r is None:
                self.assertTrue(math.isnan(ref))
            else:
                self.assertAlmostEqual(r, ref, places=10)

    def test_binom_exact(self):
        from scipy.stats import binom
        for n, k in [(15, 12), (100, 80), (0, 0), (40, 0), (40, 41)]:
            self.assertAlmostEqual(S.binom_sf(k, n), float(binom.sf(k - 1, n, 0.6)) if n else 1.0, places=12)

    def test_percentile_matches_numpy(self):
        import numpy as np
        rng = random.Random(5)
        for _ in range(30):
            v = sorted(rng.random() for _ in range(rng.randint(1, 20)))
            for q in (25, 50, 75):
                self.assertAlmostEqual(S.percentile(v, q), float(np.percentile(v, q)), places=12)


class TestFamilies(unittest.TestCase):
    def test_prescreen_uniform(self):
        p = {f"{c}{i}": U(c, 6, i, 0) for c in "ABC" for i in range(6)}
        self.assertEqual(S.f1_regime4(p, True)["verdict"], "REGIME-4-UNAVAILABLE-AT-RECOGNITION")
        self.assertEqual(S.f1_regime4(p, True, prescreen=False)["verdict"], "FALSIFIED")

    def test_c1_inadequate_and_cells(self):
        p = {f"{c}{i}": U(c, i % 4 + 3, i, 0) for c in "AB" for i in range(5)}     # n = 10 < 12
        self.assertEqual(S.f1_regime4(p, False)["verdict"], "INADEQUATE")
        one = {f"A{i}": U("A", i % 4, i, 0) for i in range(12)}
        self.assertIsNone(S.f1_regime4(one, False)["verdict"])
        self.assertIsNone(S.f3_dissociation(one)["verdict"])

    def _varied(self, c, rc_fn):
        cps = [0, 1, 2, 3, 4, 5, 6, 6]                     # distinct 7, modal 0.25 -> C2 passes
        return {f"{c}{i}": U(c, cps[i], rc_fn(i), 0) for i in range(8)}

    def test_routing(self):
        good = {**self._varied("A", lambda i: i), **self._varied("B", lambda i: i), **self._varied("C", lambda i: i)}
        self.assertEqual(S.f1_regime4(good, False)["verdict"], "CONFIRMED")   # rho = 1 in every cell
        # IL guard: B top-2 share minus C top-2 share < 0.10 -> PARTIAL
        flatB = {**self._varied("A", lambda i: i), **self._varied("B", lambda i: 5), **self._varied("C", lambda i: i)}
        r = S.f1_regime4(flatB, True)
        self.assertEqual(r["verdict"], "PARTIAL")
        self.assertEqual(r["resolved_at"], "IL guard")
        # IL guard skipped when C is absent
        noC = {k: v for k, v in good.items() if v["cell"] != "C"}
        self.assertEqual(S.f1_regime4(noC, True)["verdict"], "CONFIRMED")
        # one failing cell -> PARTIAL; two -> FALSIFIED
        sat = {f"C{i}": U("C", 6, i, 0) for i in range(8)}
        one_fail = {**self._varied("A", lambda i: i), **self._varied("B", lambda i: i), **sat}
        self.assertEqual(S.f1_regime4(one_fail, False)["verdict"], "PARTIAL")
        satB = {f"B{i}": U("B", 6, i, 0) for i in range(8)}
        two_fail = {**self._varied("A", lambda i: i), **satB, **sat}
        self.assertEqual(S.f1_regime4(two_fail, False)["verdict"], "FALSIFIED")
        # C3: rho undefined (constant R_cat) fails the cell
        flat = {**self._varied("A", lambda i: 3), **self._varied("B", lambda i: 3), **self._varied("C", lambda i: i)}
        self.assertEqual(S.f1_regime4(flat, False)["verdict"], "PARTIAL")

    def test_type2(self):
        self.assertEqual(S.f2_type2({"A0": U("A", 6, 0, 9)})["verdict"], "UNDETERMINED")       # no cell B
        b4 = {f"B{i}": U("B", 6, 0, 9) for i in range(4)}
        self.assertEqual(S.f2_type2(b4)["verdict"], "UNDETERMINED")                           # n_B < 5
        for k, v in ((0, "FALSIFIED"), (1, "PARTIAL"), (2, "PARTIAL"), (3, "EMERGED")):
            p = {f"B{i}": U("B", 6, 0, 9 if i < k else 0) for i in range(6)}
            self.assertEqual(S.f2_type2(p)["verdict"], v)

    def test_dissociation(self):
        p = {"A0": U("A", 6, 0, 0), "A1": U("A", 6, 9, 0), "B0": U("B", 6, 9, 0)}
        self.assertEqual(S.f3_dissociation(p)["verdict"], "PARTIAL")
        p["B1"] = U("B", 5, 2, 0)
        self.assertEqual(S.f3_dissociation(p)["verdict"], "GENERALIZED")
        p = {"A0": U("A", 4, 0, 0), "B0": U("B", 6, 3, 0)}
        self.assertEqual(S.f3_dissociation(p)["verdict"], "NARROWED")

    def test_regimes(self):
        self.assertIsNone(S.composite(U("A", 4, 18, 18)))
        self.assertAlmostEqual(S.composite(U("A", 5, 18, 18)), 1.0)
        self.assertAlmostEqual(S.composite(U("A", 6, 0, 0)), 0.3)          # the Iwachu limit (v1.4 sec 7.3)
        few = {f"A{i}": U("A", 6, i, 0) for i in range(3)}
        self.assertTrue(all(v is None for v in S.f4_regimes(few).values()))
        ties = {f"A{i}": U("A", 6, 0, 0) for i in range(8)}
        self.assertEqual(set(S.f4_regimes(ties).values()), {"Dominant"})   # all tied at q75
        p = {f"A{i}": U("A", 6, i, 0) for i in range(8)}
        p["X"] = U("A", 2, 18, 18)                                         # descoped -> Absent
        r = S.f4_regimes(p)
        self.assertEqual(r["X"], "Absent")
        self.assertEqual(r["A7"], "Dominant")
        self.assertEqual(r["A0"], "Absent")

    def test_compare_uncomparable(self):
        rows = S.compare({"F1": "FALSIFIED", "F2": "EMERGED", "F3": None},
                         {"F1": "INADEQUATE", "F2": "EMERGED", "F3": "PARTIAL"})
        self.assertEqual([r["status"] for r in rows], ["uncomparable", "match", "uncomparable"])


class TestVerdictRules(unittest.TestCase):
    def test_h1(self):
        self.assertEqual(S.verdict_h1(10, 14)["verdict"], "UNDETERMINED")
        self.assertEqual(S.verdict_h1(0, 0)["verdict"], "UNDETERMINED")
        self.assertEqual(S.verdict_h1(50, 100)["verdict"], "FALSIFIED")
        self.assertEqual(S.verdict_h1(90, 100)["verdict"], "CONFIRMED")
        self.assertEqual(S.verdict_h1(12, 15)["verdict"], "MARGINAL")      # A = 0.80 but p >= 0.025
        self.assertEqual(S.verdict_h1(70, 100)["verdict"], "MARGINAL")

    def test_h2_h3_h4(self):
        self.assertEqual(S.verdict_h2(None, 0, None)["verdict"], "UNDETERMINED")
        self.assertEqual(S.verdict_h2(0.9, 9, 0.001)["verdict"], "UNDETERMINED")
        self.assertEqual(S.verdict_h2(0.9, 15, 0.001)["verdict"], "CONFIRMED")     # bars 0.90 / 0.75
        self.assertEqual(S.verdict_h2(0.89, 15, 0.001)["verdict"], "MARGINAL")
        self.assertEqual(S.verdict_h2(0.95, 15, 0.2)["verdict"], "MARGINAL")
        self.assertEqual(S.verdict_h2(0.75, 15, 0.001)["verdict"], "MARGINAL")
        self.assertEqual(S.verdict_h2(0.7499, 15, 0.001)["verdict"], "FALSIFIED")
        self.assertEqual(S.verdict_h3(0.3, 0.1, 0.001, 50)["verdict"], "CONFIRMED")
        self.assertEqual(S.verdict_h3(0.3, 0.1, 0.2, 50)["verdict"], "MARGINAL")
        self.assertEqual(S.verdict_h3(0.1, 0.1, 0.5, 50)["verdict"], "FALSIFIED")
        self.assertEqual(S.verdict_h3(0.3, 0.1, 0.001, 5)["verdict"], "UNDETERMINED")
        self.assertEqual(S.verdict_h4(0, 6, 19, 20)["verdict"], "CONFIRMED")
        self.assertEqual(S.verdict_h4(1, 6, 19, 20)["verdict"], "MARGINAL")
        self.assertEqual(S.verdict_h4(0, 6, 16, 20)["verdict"], "MARGINAL")
        self.assertEqual(S.verdict_h4(2, 6, 20, 20)["verdict"], "FALSIFIED")
        self.assertEqual(S.verdict_h4(0, 6, 14, 20)["verdict"], "FALSIFIED")
        self.assertEqual(S.verdict_h4(0, 0, 0, 0)["verdict"], "UNDETERMINED")


class TestRules(unittest.TestCase):
    def test_structural_variants_dedup_and_empty(self):
        meta = make_meta()
        v22 = S.structural_variants("v0.22", meta["v0.22"])
        ids = [v[1] for v in v22]
        self.assertIn("R1_DROP_DEFUNCT", ids)
        self.assertNotIn("R6_LEAVE_OUT_D", ids)                 # identical to R1 -> counted once
        v19 = S.structural_variants("v0.19", meta["v0.19"])
        r2 = [v for v in v19 if v[0] == "R2_DROP_COI_FLAGGED"][0]
        self.assertNotIn("hA2", r2[2])
        allflag = {b: {**v, "flags": {"borderline"}} for b, v in meta["v0.20"].items()}
        self.assertFalse([v for v in S.structural_variants("v0.20", allflag) if v[0] == "R4_DROP_BORDERLINE"])
        none = {b: {**v, "flags": set()} for b, v in meta["v0.21"].items()}
        self.assertFalse([v for v in S.structural_variants("v0.21", none) if v[0].startswith(("R1", "R2", "R3", "R4"))])
        top5 = [v for v in S.structural_variants("v0.20", meta["v0.20"]) if v[0] == "R5_CASCADE_TOP5"][0]
        self.assertEqual(len(top5[2]), 15)

    def test_data_variants(self):
        p = {"a": U("A", 6, 1, 0), "b": U("A", 4, 0, 0), "c": U("B", 6, 0, 0)}
        src = {"a": U("A", 6, 0, 0), "b": U("A", 4, 0, 1), "c": U("B", 6, 2, 0)}
        v = {x[0]: x[2] for x in S.data_variants("v0.20", p, src)}
        self.assertEqual(v["R7_RECOGNITION_ANCHORED"], ["a", "c"])
        self.assertEqual(v["R8_RECALL_SOURCED_XWAVE"], ["b", "c"])
        zero = {k: U(u["cell"], 6, 0, 0) for k, u in p.items()}
        self.assertEqual(S.data_variants("v0.20", zero, zero), [])  # R8 would empty the panel -> no variant

    def test_stratified_draw(self):
        import numpy as np
        meta = make_meta()
        p = make_archive(meta)["t1"]["v0.22"]
        k1 = S.stratified_draw(np.random.default_rng(7), p)
        k2 = S.stratified_draw(np.random.default_rng(7), p)
        self.assertEqual(k1, k2)
        sizes = {c: sum(1 for b in k1 if p[b]["cell"] == c) for c in "ABCD"}
        self.assertEqual(sizes, {"A": 6, "B": 4, "C": 6, "D": 4})


class TestScoring(unittest.TestCase):
    KW = dict(n_draws=15, n_perm=40, n_mc=25)

    def test_end_to_end_reproducible(self):
        meta = make_meta()
        arch = make_archive(meta, seed=11)
        r1 = S.score_all(arch, meta, log=lambda *a: None, **self.KW)
        r2 = S.score_all(arch, meta, log=lambda *a: None, **self.KW)
        self.assertEqual(json.dumps(S._clean(r1), sort_keys=True), json.dumps(S._clean(r2), sort_keys=True))
        self.assertEqual(set(r1["verdicts"]), {"H1_SubstrateVerdictStability", "H2_RegimeAssignmentStability",
                                               "H3_PurposiveVsRandom", "H4_DisclosedHandlingNeutral"})
        for v in r1["verdicts"].values():
            self.assertIn(v, ("CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED"))
        h1 = r1["H1_SubstrateVerdictStability"]
        det = [c for c in r1["comparisons"] if c["rule"] in S.DETERMINISTIC_RULES]
        self.assertEqual(h1["n"] + h1["uncomparable"], len(det))
        self.assertNotIn("R11_INDEPENDENT_ONLY", {c["rule"] for c in r1["comparisons"]})
        self.assertIn("sensitivity_S1_without_COI_flagged", r1)
        s2 = r1["sensitivity_S2_uncomparable_as_flip"]
        self.assertEqual(s2["H1_SubstrateVerdictStability"]["n"], len(det))
        self.assertLessEqual(s2["H1_SubstrateVerdictStability"]["A"], h1["A"])
        self.assertEqual(sum(s2["uncomparable_by_rule"].values()), h1["uncomparable"])
        self.assertEqual({c["wave"] for c in r1["comparisons"] if c["substrate"] == "v0.18"}, {"t1"})
        self.assertNotIn("R8_RECALL_SOURCED_XWAVE",
                         {c["rule"] for c in r1["comparisons"] if c["substrate"] == "v0.18"})
        self.assertFalse([c for c in r1["comparisons"] if c["substrate"] == "v0.18" and c["family"] == "F2"])

    def test_identical_panels_are_perfectly_stable(self):
        meta = make_meta()
        arch = make_archive(meta, seed=2)
        for w in S.WAVES:                       # every brand identical -> every subset gives the same verdicts
            for s, p in arch[w].items():
                for b in p:
                    p[b] = U(p[b]["cell"], 6, 9, 9, p[b]["cascade"])
        r = S.score_core(arch, meta, do_h3=False, **self.KW)
        h1 = r["H1_SubstrateVerdictStability"]
        self.assertEqual(h1["A"], 1.0)
        self.assertEqual(r["H4_DisclosedHandlingNeutral"]["verdict"], "CONFIRMED")
        self.assertEqual(r["H2_RegimeAssignmentStability"]["S"], 1.0)

    def test_all_descoped_is_undetermined(self):
        meta = make_meta()
        arch = make_archive(meta, seed=4)
        for w in S.WAVES:
            for s, p in arch[w].items():
                for b in p:
                    p[b]["cp"] = 2                # every brand fails recognition -> no regime defined
        r = S.score_core(arch, meta, do_h3=False, **self.KW)
        self.assertEqual(r["H2_RegimeAssignmentStability"]["verdict"], "UNDETERMINED")

    def test_brand_set_mismatch_halts(self):
        meta = make_meta()
        arch = make_archive(meta)
        del arch["t2"]["v0.21"]["21A0"]
        with self.assertRaises(S.Halt):
            S.score_core(arch, meta, do_h2=False, do_h3=False)

    def test_dry_run_scores_once(self):
        meta = make_meta()
        arch = make_archive(meta, seed=9)
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "synthetic.json"
            f.write_text(json.dumps({"archive": arch,
                                     "meta": {s: {b: {**v, "flags": sorted(v["flags"])} for b, v in ms.items()}
                                              for s, ms in meta.items()}}))
            S.run_dry(f, log=lambda *a: None, **self.KW)
            self.assertTrue((Path(d) / "_score/v0_63_verdicts.json").exists())
            self.assertTrue((Path(d) / "_score/v0_63_comparisons.csv").exists())
            with self.assertRaises(S.Halt):
                S.run_dry(f, log=lambda *a: None, **self.KW)


class TestCOISensitivity(unittest.TestCase):
    def test_s1_removes_every_flagged_brand(self):
        meta = make_meta()
        arch = make_archive(meta, seed=5)
        seen = []
        orig = S.score_core

        def spy(a, m, **kw):
            seen.append({s: set(ms) for s, ms in m.items()})
            return orig(a, m, **kw)
        S.score_core = spy
        try:
            S.score_all(arch, meta, log=lambda *x: None, n_draws=5, n_perm=10, n_mc=5)
        finally:
            S.score_core = orig
        self.assertEqual(len(seen), 2)
        self.assertIn("hA2", seen[0]["v0.19"])
        self.assertNotIn("hA2", seen[1]["v0.19"])
        self.assertNotIn("fB3", seen[1]["v0.18"])
        r2 = [v for v in S.structural_variants("v0.18", meta["v0.18"]) if v[0] == "R2_DROP_COI_FLAGGED"]
        self.assertEqual(len(r2), 1)
        self.assertNotIn("fB3", r2[0][2])


class TestSingleWave(unittest.TestCase):
    def test_single_wave_extra_wave_flagged(self):
        meta = make_meta()
        arch = make_archive(meta)
        arch["t2"]["v0.18"] = dict(arch["t1"]["v0.18"])
        self.assertTrue([b for b in S.check_archive(arch, meta) if "single-wave" in b])

    def test_composite_uses_phase_b_cells(self):
        self.assertAlmostEqual(S.composite({**U("A", 6, 9, 0), "n_b": 18}), 0.3 + 0.7 * 0.5)
        self.assertAlmostEqual(S.composite(U("A", 6, 9, 9)), 0.3 + 0.7 * 0.5)

    def test_cell_letter(self):
        self.assertEqual([S._cell_letter(x) for x in ("A_Heritage", "Cell_B_Disruptor", "cell_c_mass_prestige", "C")],
                         ["A", "B", "C", "C"])


class TestLockAndRegistries(unittest.TestCase):
    def test_run_refuses_before_lock(self):
        if S.tag_exists():
            self.skipTest("tag exists: the refusal path is not reachable")
        ok, why = S.lock_status()
        self.assertFalse(ok)
        self.assertTrue(any(S.PREREG_TAG in w for w in why))
        self.assertEqual(S.main(["--run"]), 3)
        self.assertFalse((S.OUT_DIR / "v0_63_verdicts.json").exists())

    def test_manifest_detects_change(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "a.txt").write_text("x")
            man = root / "m.sha256"
            man.write_text(S.lock_manifest_text(["a.txt"], root))
            self.assertFalse([b for b in S.verify_lock_manifest(man, root) if "changed" in b])
            (root / "a.txt").write_text("y")
            self.assertTrue([b for b in S.verify_lock_manifest(man, root) if "changed" in b])

    def test_real_registries_structure(self):
        meta = S.load_registry_meta()            # registries only; no answer file
        self.assertEqual({s: len(m) for s, m in meta.items()}, S.EXPECTED_BRANDS)
        self.assertEqual(sorted(b for b, v in meta["v0.18"].items() if "borderline" in v["flags"]),
                         ["Byredo", "Frederic Malle", "Le Labo"])
        self.assertEqual(dict(Counter(v["cell"] for v in meta["v0.18"].values())), {"A": 8, "B": 8, "C": 8})
        self.assertEqual(meta["v0.19"]["Denon"]["flags"], {"coi_flagged"})
        self.assertEqual(sorted((s, b) for s, ms in meta.items() for b, v in ms.items() if "coi_flagged" in v["flags"]),
                         [("v0.18", "Ellis Brooklyn"), ("v0.19", "Denon")])
        self.assertEqual(sorted(b for b, v in meta["v0.22"].items() if "defunct" in v["flags"]),
                         ["Mercury", "Oldsmobile", "Plymouth", "Pontiac", "Saturn"])

    def test_frozen_rules_file_matches_registries(self):
        if not S.RULES_FILE.exists():
            self.skipTest("rules file not written yet")
        frozen = json.loads(S.RULES_FILE.read_text())
        fresh = S.build_rules_doc()
        self.assertEqual(frozen["substrates"], json.loads(json.dumps(S._clean(fresh["substrates"]))))
        self.assertEqual(frozen["structural_comparisons_upper_bound_H1"], fresh["structural_comparisons_upper_bound_H1"])

    def test_v19_output_parser(self):
        txt = ("  A_Heritage:\n    C_P modal share = 0.500 (FAIL)\n  B_Boutique:\n    C_P modal share = 0.875 (FAIL)\n"
               "    ZMF Headphones (B_Boutique): C_P=6/6, mentions=1/18\n"
               "    Audeze (B_Boutique): category=13/18, cultural=2/18\n")
        p = S._parse_v19_output(txt)
        self.assertEqual(p["iwachu"], {"ZMF Headphones": (6, 1)})
        self.assertEqual(p["type1"], {"Audeze": (13, 2)})
        self.assertEqual(p["cp_modal_share"], {"A": 0.5, "B": 0.875})

    def test_power_check_runs(self):
        r = S.power_check(reps=20, h2_draws=3)
        self.assertTrue(r["H1_operating_characteristics"])
        for row in r["H1_operating_characteristics"]:
            self.assertAlmostEqual(row["P_CONFIRMED"] + row["P_MARGINAL"] + row["P_FALSIFIED"], 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
