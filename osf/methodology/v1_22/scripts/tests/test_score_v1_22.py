"""v1.22 r1 tests: imported pins, frozen design inputs, every statistic against a brute-force or hand-built value,
HB2 = v0.45's own leg, the decision tables, the refusal guards and the not-run paths. Offline; synthetic data only."""
import itertools
import json
import random
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import score_v1_22 as s  # noqa: E402

A = s.A
V = (s.C, s.M, s.F, s.U)


def src(dom, cls="other"):
    return {"key": (dom, "/"), "domain": dom, "cls": cls, "redirect": False, "via_title": False}


def mini_units(cats=("v20", "v21", "v22"), per=6):
    return {(c, f"b{i}"): {"substrate": c, "brand_id": f"b{i}", "brand": f"B{i}", "coder_key": f"b{i}",
                           "status": "RESOLVED", "domains": {f"{c}b{i}.com"}} for c in cats for i in range(per)}


def ans(sub, named, srcs, ch="cat", run=1, model="m", wave="t4", cid=None):
    return {"call_id": cid or f"{wave}{sub}{ch}{run}{model}{random.random()}", "substrate": sub, "model": model,
            "run": run, "named": set(named), "sources": srcs, "channel": ch, "wave": wave, "source": "wave"}


class Pins(unittest.TestCase):
    def test_v113_scorer_pinned_and_manifest(self):
        self.assertEqual(s.sha256_file(s.V113_SCORER), s.V113_SCORER_SHA256)
        checks = s.b_p0()
        self.assertTrue(all(v["match"] for v in checks.values()))

    def test_roster_hash_refused_if_changed(self):
        raw = s.git_show(*s.ROSTER_REF)
        with self.assertRaises(s.Refused):
            s.load_roster(raw + b"\n")


class Design(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.units = A.load_brand_domains()

    def test_roster_maps_all_units(self):
        fl = s.roster_flags(self.units)
        self.assertEqual(len(fl), 112)
        self.assertEqual(sum(v["F"] for v in fl.values()), 57)
        self.assertEqual(sorted(self.units[k]["brand"] for k, v in fl.items() if v["D"]), sorted(s.DEFUNCT))
        self.assertTrue(all(self.units[k]["status"] == "NONE" for k, v in fl.items() if v["D"]))

    def test_channel_map_against_probe_file(self):
        ch, labels = s.load_channels()
        self.assertEqual(len(ch), 30)
        for sub in A.SUBSTRATES:
            got = sorted(v for (sb, _), v in ch.items() if sb == sub)
            self.assertEqual(got, ["cat"] * 3 + ["cult"] * 3, sub)
        self.assertEqual({labels[k] for k in labels if k[0] in s.TRIO}, {"R_cat", "R_cult"})

    def test_coi_units(self):
        self.assertEqual(len(s.coi_keys(self.units)), 6)


class Statistics(unittest.TestCase):
    def test_cliffs_delta_brute_force(self):
        rng = np.random.default_rng(1)
        for _ in range(20):
            v = rng.integers(0, 5, 30).astype(float)
            f = rng.random(30) < 0.4
            g = np.repeat(["a", "b", "c"], 10)
            num = den = 0
            for c in "abc":
                for i in range(30):
                    for j in range(30):
                        if g[i] == c == g[j] and f[i] and not f[j]:
                            num += np.sign(v[i] - v[j])
                            den += 1
            self.assertAlmostEqual(s.cliffs_delta_within(v, f, g), num / den if den else float("nan"))

    def test_signflip_against_enumeration(self):
        rng = np.random.default_rng(2)
        for n in (6, 9, 12):
            d = rng.normal(1.0, 2.0, n)
            exact = s.signflip_p_exact(d)
            mc = s.signflip_p(d, 5, 20000)
            self.assertLess(abs(mc - exact), 0.02, (n, mc, exact))
        self.assertAlmostEqual(s.signflip_p_exact([1, 2, 3]), 1 / 8)

    def test_pool_arithmetic(self):
        u = mini_units()
        k = ("v20", "b0")
        a4 = [ans("v20", [k], [src("v20b0.com", "brand_owned"), src("x.com")]),
              ans("v20", [k], [src("x.com")])]
        a5 = [ans("v20", [k], [src("v20b0.com", "brand_owned")], wave="t5")]
        _, st = s.gstar(a4 + a5, u, floor=1)
        self.assertEqual((st[k]["o"], st[k]["g"]), (2, 3))
        self.assertAlmostEqual(st[k]["G_star"], 200 / 3)

    def test_channel_counts_and_hb47(self):
        u = mini_units(per=8)
        answers = []
        for (c, b) in u:
            k = (c, b)
            for _ in range(4):                    # cat: own domain in 3 of 4; cult: in 1 of 4 -> d = 50 points
                answers.append(ans(c, [k], [src(f"{c}{b}.com", "brand_owned")], "cat"))
                answers.append(ans(c, [k], [src(f"{c}{b}.com", "brand_owned") if _ == 0 else src("y.com")],
                                   "cult"))
            answers.append(ans(c, [k], [src("z.com")], "cat"))
            answers[-1]["sources"] = [src("z.com")]
        cnt = s.channel_counts(answers, u)
        self.assertEqual(cnt[("v20", "b0")], (5, 4, 4, 1))
        r = s.hb47(answers, u, n_perm=200)
        self.assertAlmostEqual(r["dbar"], 100 * (4 / 5 - 1 / 4))
        self.assertEqual(r["verdict"], s.C)
        self.assertEqual(r["n"], 24)

    def test_hb47_floor(self):
        u = mini_units(per=6)
        answers = [ans(c, [(c, b)], [src("q.com")], ch) for (c, b) in u for ch in ("cat", "cult") for _ in range(3)]
        r = s.hb47(answers, u, n_perm=50)
        self.assertEqual(r["n"], 18)
        self.assertEqual(r["verdict"], s.U)        # n < 20

    def test_hb46_signature_and_floors(self):
        keys = [(c, f"b{i}") for c in ("v20", "v21", "v22") for i in range(8)]
        flags = {k: {"F": int(k[1][1:]) < 4, "D": False} for k in keys}
        g = {k: (90.0 if flags[k]["F"] else 10.0) + int(k[1][1:]) for k in keys}
        r = s.hb46(g, flags, 1, 500)
        self.assertAlmostEqual(r["delta"], 1.0)
        self.assertEqual(r["verdict"], s.C)
        few = {k: {"F": k[1] == "b0", "D": False} for k in keys}
        self.assertEqual(s.hb46(g, few, 1, 50)["verdict"], s.U)
        rev = {k: {"F": not flags[k]["F"], "D": False} for k in keys}
        self.assertEqual(s.hb46(g, rev, 1, 500)["verdict"], "CONFIRMED_REVERSED")

    def test_hb48_identical_profiles_replicate(self):
        rng = np.random.default_rng(3)
        keys = [(c, f"b{i}") for c in ("v20", "v21", "v22", "v23", "v19") for i in range(8)]
        prof = {k: {"x": list(rng.random(6))} for k in keys}
        g = {k: 1.0 for k in keys}
        r = s.hb48(prof, prof, g, g, 1, 200)
        self.assertAlmostEqual(r["R"], 1.0)
        self.assertEqual(r["verdict"], s.C)
        shuffled = {k: prof[keys[(i + 7) % len(keys)]] for i, k in enumerate(keys)}
        self.assertIn(s.hb48(prof, shuffled, g, g, 1, 200)["verdict"], (s.F, s.M))

    def test_hb48b_structure_path(self):
        """The k >= 2 branch (gap, silhouette null, ARI vs Presence tiers, residual arm, typology cell)."""
        rng = np.random.default_rng(6)
        centres = np.array([[.6, 0, 0, .6, 0, 0], [0, 0, 0, 0, .6, .6], [0, .6, .6, 0, 0, 0]])
        keys = [(c, f"b{i}") for c in ("v19", "v20", "v21", "v22", "v23") for i in range(12)]
        prof = {k: {"x": list(centres[i % 3] + rng.normal(0, 0.02, 6))} for i, k in enumerate(keys)}
        gp = {k: float(rng.random()) for k in keys}
        P = {k: float(rng.random()) for k in keys}
        Cs = {k: float(rng.random()) for k in keys}
        r = s.hb48b(prof, gp, P, Cs, s.C, n_perm=30, B=20)
        self.assertGreaterEqual(r["full"]["k"], 2)
        self.assertIsNotNone(r["full"]["silhouette"])
        self.assertEqual(r["full"]["n_null"], 30)
        self.assertIn(r["cell"], ("LAYERED", "BORROWED", "AUTONOMOUS", "PRESENCE-DEPENDENT", "RESIDUAL-ONLY",
                                  "UNSTRUCTURED"))
        self.assertEqual(s.hb48b(prof, gp, P, Cs, s.F)["cell"], "NO TYPOLOGY")

    def test_profiles_shares(self):
        u = mini_units()
        k = ("v20", "b0")
        p = s.profiles([ans("v20", [k], [src("r.org", "reference"), src("n.com", "news"), src("o.com", "other")])],
                       u)
        self.assertEqual(p[k]["x"], [0.0, 1 / 3, 0.0, 1 / 3, 0.0, 0.0])
        self.assertAlmostEqual(p[k]["other"], 1 / 3)

    def test_silhouette_matches_loop(self):
        rng = np.random.default_rng(4)
        X = rng.normal(size=(25, 4))
        lab = rng.integers(1, 4, 25)
        D = np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1))
        sv = []
        for i in range(25):
            same = lab == lab[i]
            if same.sum() <= 1:
                sv.append(0.0)
                continue
            a = D[i, same].sum() / (same.sum() - 1)
            b = min(D[i, lab == k].mean() for k in set(lab.tolist()) if k != lab[i])
            sv.append((b - a) / max(a, b))
        self.assertAlmostEqual(s.silhouette(X, lab), float(np.mean(sv)))

    def test_il_from_coded(self):
        u = mini_units(cats=("v20",), per=2)
        ch = {("v20", "q1"): "cat", ("v20", "q2"): "cult"}
        rows = []
        for m in s.N3:
            for q in ("q1", "q2"):
                rows.append({"call_id": f"{m}{q}", "substrate": "v0.20", "brand": "b0", "model": m, "condition": "S0",
                             "probe_id": q, "mentioned": "1" if q == "q2" else "0"})
        il = s.il_from_coded(rows, ch, u)
        self.assertAlmostEqual(il[("v20", "b0")]["il"], 1.0)
        self.assertAlmostEqual(il[("v20", "b0")]["pi_hat"], 0.5)


class HB2IsV045(unittest.TestCase):
    """C4: HB2 is v0.45 section 2.6's Grounding leg, called through v0.45's own code at tag v0.45-prereg-r1."""

    @classmethod
    def setUpClass(cls):
        cls.units = A.load_brand_domains()
        rng = np.random.default_rng(5)
        keys = sorted(cls.units)
        x = rng.normal(size=len(keys))
        cls.g4 = {k: float(50 + 20 * x[i]) if i % 3 else None for i, k in enumerate(keys)}
        cls.g5 = {k: float(50 + 20 * (0.7 * x[i] + 0.7 * rng.normal())) if i % 4 else None
                  for i, k in enumerate(keys)}

    def test_equal_to_component_leg(self):
        SC = s.load_v045()
        d = Path(tempfile.mkdtemp())
        r = s.hb2_retest(self.g4, self.g5, self.units, 300, 300, out_dir=d)
        leg = SC.component_leg("Grounding", str(d / "g_star_t4_v1_22.csv"), str(d / "g_star_t5_v1_22.csv"),
                               "MARGINAL", SC.S.Cfg(300, 300), SC.brands_list())
        self.assertEqual(r["n"], leg["n"])
        self.assertEqual(r["rho_pw"], float(leg["rho"]))
        self.assertEqual(r["p_perm_one_sided"], float(leg["p_perm"]))
        self.assertEqual(r["verdict"], s.from_v045(leg["verdict"]))
        self.assertEqual(r["verdict"], r["v122_band_check"])
        self.assertEqual(r["seed"], 450046)

    def test_retest_leg_same_statistic(self):
        r = s.hb2_retest(self.g4, self.g5, self.units, 300, 300)
        t = s.retest_leg(self.g4, self.g5, self.units, s.SEEDS["HB2"], 300, 0)
        self.assertEqual((r["n"], r["rho_pw"], r["p_perm_one_sided"]), (t["n"], t["rho_pw"], t["p_perm_one_sided"]))

    def test_stage2_identical_maps(self):
        g = {k: v for k, v in self.g4.items()}
        r = s.retest_leg(g, g, self.units, s.SEEDS["HB45_t5t6"], 200, 0)
        self.assertAlmostEqual(r["rho_pw"], 1.0)
        self.assertEqual(r["verdict"], s.C)

    def test_stage2_panel_rules(self):
        g = {k: v for k, v in self.g4.items()}
        r = s.stage2(g, g, g, self.units, 100, 0, t6_models=("claude-fable-5-2",))
        self.assertEqual(r["verdicts"], {"HB45_t5t6": s.NM, "HB45_t4t6": s.NM})
        r = s.stage2(g, g, g, self.units, 100, 0, t6_models=("claude-fable-5-2", "some-newer-model"))
        self.assertEqual(r["label"], "model changed")
        self.assertEqual(r["verdicts"]["HB45_t4t6"], s.C)
        self.assertIsNone(s.stage2(g, g, g, self.units, 100, 0)["label"])


def gb_reference(hb1, hb2, hb3, hb4):
    """Section 3.5 written out independently (top to bottom)."""
    if C in (hb2, hb3) and F in (hb2, hb3):
        R = "MIXED"
    elif C in (hb2, hb3):
        R = "MET"
    elif F in (hb2, hb3):
        R = "FAILED"
    else:
        R = "OPEN"
    if hb1 == F or R == "FAILED" or hb4 == F:
        return "FAIL"
    if hb1 == C and R == "MET":
        return "PASS"
    if hb1 == U or (R == "OPEN" and hb2 == U and hb3 == U):
        return "UNDETERMINED"
    return "MARGINAL"


C, M, F, U = s.C, s.M, s.F, s.U


class Tables(unittest.TestCase):
    def test_gb_against_reference(self):
        for combo in itertools.product(V, repeat=4):
            self.assertEqual(s.gate_completion(*combo), gb_reference(*combo), combo)

    def test_not_measured_enters_gb_as_undetermined(self):
        self.assertEqual(s.gate_completion(*(s._gb_in(v) for v in (s.C, s.NM, s.C, s.C))), "PASS")
        self.assertEqual(s._gb_in(s.NM), s.U)

    def test_typology_cells(self):
        self.assertTrue(s.typology_cell(s.F, True, True, True).startswith("NO TYPOLOGY"))
        self.assertEqual(s.typology_cell(s.C, True, False, True), "LAYERED")
        self.assertEqual(s.typology_cell(s.C, True, False, False), "BORROWED")
        self.assertEqual(s.typology_cell(s.C, False, True, True), "AUTONOMOUS")
        self.assertEqual(s.typology_cell(s.C, False, True, False), "PRESENCE-DEPENDENT")
        self.assertEqual(s.typology_cell(s.C, False, False, True), "RESIDUAL-ONLY")
        self.assertTrue(s.typology_cell(s.M, False, False, False).startswith("UNSTRUCTURED [provisional"))

    def test_v045_partial(self):
        self.assertEqual(s.from_v045("PARTIAL"), s.M)
        self.assertEqual(s.retest_verdict(0.6, None, 40), s.U)


class GuardsAndRoutes(unittest.TestCase):
    def setUp(self):
        self._orig = s.tag_commit_on_origin
        s.tag_commit_on_origin = lambda tag: None       # offline: nothing is on origin
        s._GUARD["passed"] = None

    def tearDown(self):
        s.tag_commit_on_origin = self._orig
        s._GUARD["passed"] = None

    def test_guard_refuses_without_lock(self):
        with self.assertRaises(s.Refused) as cm:
            s.guard_stage(1, "0" * 40)
        self.assertIn("not on origin", str(cm.exception))

    def test_main_stage1_refuses_before_reading(self):
        with self.assertRaises(s.Refused):
            s.main(["--stage", "1", "--t5", "/nonexistent/t5_raw.jsonl"])

    def test_t5_not_read_without_guard(self):
        with self.assertRaises(s.Refused):
            s.load_wave_real("t5", "/nonexistent", "/nonexistent", "/nonexistent", {}, {}, {})

    def test_decision_record_routes_to_run(self):
        verdict, _ = s.paper_a_verdict()
        self.assertEqual(verdict, "MARGINAL")
        dec = s.read_decision()
        self.assertIsNotNone(dec)
        self.assertTrue(dec["go"])
        self.assertEqual(s.paper_b_route(verdict, dec), "RUN")

    def test_not_run_paths(self):
        inp = {"paper_a_verdict": "MARGINAL", "decision": None}
        self.assertEqual(s.stage1(inp)["status"], "NOT_RUN_PENDING")
        self.assertIsNone(s.stage1(inp)["statistics"])
        inp["decision"] = {"go": False, "date": "d", "text": "t"}
        self.assertEqual(s.stage1(inp)["status"], "NOT_RUN_DECLINED")
        with self.assertRaises(s.Refused):
            s.stage1({"paper_a_verdict": "PASS", "decision": {"go": True, "date": "d", "text": "t"}})


if __name__ == "__main__":
    unittest.main()
