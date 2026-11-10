"""Tests of score_v0_62.py on synthetic coded tables (no network, no model)."""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import score_v0_62 as S  # noqa: E402

SIZES = {"v0.19": 16, "v0.20": 24, "v0.21": 24, "v0.22": 24, "v0.23": 24}


def units():
    u = [("v0.19", "Denon")] + [("v0.19", f"h{i}") for i in range(15)]
    for s, n in list(SIZES.items())[1:]:
        u += [(s, f"{s}-b{i}") for i in range(n)]
    return u


def synth_rows(U, pi, seed, drop_model=None):
    """Coded Phase B rows: per (model, run, category) 6 answered calls; brand mentioned with probability pi[unit]."""
    rng = np.random.default_rng(seed)
    rows = []
    for m in S.MODELS:
        for r in S.RUNS:
            for s in SIZES:
                for q in range(6):
                    cid = f"{m}|{r}|{s}|q{q}"
                    if drop_model == m and q > 0:
                        continue
                    for u in U:
                        if u[0] == s:
                            rows.append({"call_id": cid, "substrate": s, "brand": u[1], "model": m, "condition": "S0",
                                         "run": r, "mentioned": int(rng.random() < pi[u])})
    return rows


def english(U, seed=1):
    rng = np.random.default_rng(seed)
    pi = {u: float(rng.uniform(0.05, 0.95)) for u in U}
    rows = synth_rows(U, pi, seed + 100)
    V = S.unit_values(U, rows)
    return pi, {u: {"pi": V[u]["pi"], "phi": V[u]["phi"]} for u in U}


class Statistic(unittest.TestCase):
    def test_rho_c_single_category_is_spearman(self):
        x, y = np.array([1, 2, 3, 4, 5.0]), np.array([2, 1, 4, 3, 5.0])
        self.assertAlmostEqual(S.rho_c(x, y, np.array(["a"] * 5)), 0.8)

    def test_rho_c_is_within_category(self):
        rng = np.random.default_rng(0)
        g = np.array(["a"] * 16 + ["b"] * 24)
        x = rng.random(40)
        y = rng.random(40)
        base = S.rho_c(x, y, g)
        self.assertAlmostEqual(S.rho_c(x + (g == "b") * 10, y - (g == "b") * 5, g), base)
        # unequal sizes: the uncentred statistic carries a between-category term, the centred one does not
        ind = np.arange(40.0)
        self.assertAlmostEqual(S.rho_c(np.r_[ind[:16], ind[16:]], np.r_[ind[:16][::-1], ind[16:][::-1]], g), -1.0)
        self.assertGreater(S.rho_uncentred(np.r_[ind[:16], ind[16:]], np.r_[ind[:16][::-1], ind[16:][::-1]], g), -1.0)

    def test_ties_rounded(self):
        g = np.array(["a"] * 4)
        self.assertAlmostEqual(S.rho_c(np.array([0.1 + 0.2, 0.3, 1, 2]), np.array([1, 1, 2, 3.0]), g), 1.0)

    def test_perm_p_bounds(self):
        g = np.array(["a"] * 20)
        x = np.arange(20.0)
        self.assertAlmostEqual(S.perm_p(x, x, g, 1.0, 1, 999), 1 / 1000)
        p = S.perm_p(x, -x, g, -1.0, 1, 999)
        self.assertEqual(p, 1.0)

    def test_phi_kernel(self):
        self.assertEqual(S.phi_m([0, 0, 0])[2], "zero")
        self.assertEqual(S.phi_m([6, 6, 6])[2], "saturated")
        self.assertAlmostEqual(S.phi_m([3, 3, 3])[0], 0.0)
        self.assertAlmostEqual(S.phi_m([6, 0, 0])[0], 9.0)            # phi_max = 6M/(M-1)


class Verdicts(unittest.TestCase):
    def test_rules(self):
        self.assertEqual(S.verdict_presence(0.70, 0.01), "CONFIRMED")
        self.assertEqual(S.verdict_presence(0.70, 0.06), "MARGINAL")
        self.assertEqual(S.verdict_presence(0.49, 0.01), "FALSIFIED")
        self.assertEqual(S.verdict_presence(0.55, 0.01), "MARGINAL")
        self.assertEqual(S.verdict_phi(39, 0.9, 0.001), "UNDETERMINED")
        self.assertEqual(S.verdict_phi(40, 0.5, 0.01), "CONFIRMED")
        self.assertEqual(S.verdict_phi(40, 0.29, 0.01), "FALSIFIED")
        self.assertEqual(S.verdict_rank(29, 0.9, 0.001), "UNDETERMINED")
        self.assertEqual(S.verdict_rank(30, 0.6, 0.06), "FALSIFIED")
        self.assertEqual(S.verdict_rank(30, 0.6, 0.01, degenerate=True), "UNDETERMINED")
        self.assertEqual(S.verdict_rank(30, 0.4, 0.01), "MARGINAL")

    def test_joint_reading(self):
        self.assertEqual(S.joint_reading("CONFIRMED", "CONFIRMED"), "Language-robust")
        self.assertEqual(S.joint_reading("CONFIRMED", "FALSIFIED"), "Language-dependent (JA)")
        self.assertEqual(S.joint_reading("MARGINAL", "CONFIRMED"), "Partly robust")


class EndToEnd(unittest.TestCase):
    def test_synthetic_languages(self):
        U = units()
        pi, en = english(U)
        fr = synth_rows(U, pi, 7)                                      # same orderings as English
        rev = {u: 1.0 - pi[u] for u in U}
        ja = synth_rows(U, rev, 8)                                     # reversed orderings
        v = S.score(U, en, {"fr": fr, "ja": ja}, n_perm=199, n_boot=199, option="A")
        self.assertEqual(v["n_units"], 112)
        self.assertEqual(v["tests"]["H_Lang_Presence_fr"]["verdict"], "CONFIRMED")
        self.assertEqual(v["tests"]["H_Lang_Presence_ja"]["verdict"], "FALSIFIED")
        self.assertEqual(v["joint_reading"], "Language-dependent (JA)")
        self.assertEqual(v["tests"]["H_Lang_Rank_fr"]["verdict"], "NOT TESTED")
        self.assertIn(v["tests"]["H_Lang_Phi_fr"]["verdict"], ("CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED"))
        self.assertEqual(v["sensitivities"]["S-Denon_fr"]["n"], 111)
        self.assertEqual(v["sensitivities"]["S-Headphones_fr"]["n"], 96)
        lo, hi = v["tests"]["H_Lang_Presence_fr"]["delta_L_ci95"]
        self.assertLess(lo, hi)

    def test_options_b_c_and_drop_rule(self):
        U = units()
        pi, en = english(U)
        fr = synth_rows(U, pi, 7)
        ja = synth_rows(U, pi, 9, drop_model="gemini-4-argon")
        vb = S.score(U, en, {"fr": fr, "ja": ja}, n_perm=99, n_boot=99, option="B")
        self.assertEqual(vb["n_units"], 111)
        self.assertEqual(vb["tests"]["H_Lang_Presence_fr"]["n"], 111)
        self.assertIn("void", vb["sensitivities"]["S-Denon_fr"])
        self.assertEqual(vb["tests"]["H_Lang_Presence_ja"]["verdict"], "UNDETERMINED")   # Gemini below 90% in JA
        vc = S.score(U, en, {"fr": fr, "ja": ja}, n_perm=99, n_boot=99, option="C")
        self.assertEqual(vc["n_units"], 96)
        self.assertIn("void", vc["sensitivities"]["S-Headphones_ja"])

    def test_rank_conditional(self):
        U = units()
        pi, en = english(U)
        rows = synth_rows(U, pi, 7)
        rk = {"en": {u: float(i % 5) for i, u in enumerate(U)}}
        rk["fr"] = dict(rk["en"])
        rk["ja"] = dict(rk["en"])
        v = S.score(U, en, {"fr": rows, "ja": rows}, rank=rk, rank_status="PASS", n_perm=99, n_boot=99, option="A")
        self.assertEqual(v["tests"]["H_Lang_Rank_fr"]["verdict"], "CONFIRMED")

    def test_run_once_guard(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "v.json"
            out.write_text("{}")
            with self.assertRaises(SystemExit) as e:
                S.main(["--run", "--out", str(out), "--english", "x.csv"])
            self.assertIn("runs once", str(e.exception))
            with mock.patch.object(S, "tag_on_origin", return_value=False):
                with self.assertRaises(SystemExit) as e:
                    S.main(["--run", "--out", str(Path(d) / "new.json"), "--english", "x.csv"])
                self.assertIn("not on origin", str(e.exception))


if __name__ == "__main__":
    unittest.main()
