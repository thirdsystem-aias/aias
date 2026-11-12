#!/usr/bin/env python3
"""Unit tests for score_v1_16.py (AIAS v1.16, co-mention precedence). Everything that computes PREC runs on
SYNTHETIC data only. The parity test reads the real pinned inputs and checks counts and n's only (no PREC,
no correlation on real data), as the pre-registration allows before the lock.
Run: python3 -m unittest scripts/test_score_v1_16.py   (or python3 scripts/test_score_v1_16.py)"""
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_v1_10 as R  # noqa: E402
import score_v1_16 as V  # noqa: E402


def _rows(answers, cat="c1", wave="t1"):
    """answers: list of ordered brand lists (ties as tuples sharing a position) -> rank rows."""
    out = []
    for a, order in enumerate(answers):
        k = 1
        for item in order:
            group = item if isinstance(item, tuple) else (item,)
            for b in group:
                out.append({"panel": "X", "wave": wave, "category": cat, "answer_id": f"{cat}-{wave}-{a}",
                            "model": "m", "run_idx": 1, "brand": b, "k_mid": float(k), "k_min": k,
                            "n": sum(len(i) if isinstance(i, tuple) else 1 for i in order)})
            k += len(group)
        # competition min-rank: tied brands share the smallest position
    return out


class BradleyTerry(unittest.TestCase):
    def test_recovers_known_strengths(self):
        rng = np.random.default_rng(1)
        true = np.linspace(-1.5, 1.5, 8)
        W = np.zeros((8, 8))
        for _ in range(4000):
            i, j = rng.choice(8, 2, replace=False)
            p = 1 / (1 + np.exp(-(true[i] - true[j])))
            if rng.random() < p:
                W[i, j] += 1
            else:
                W[j, i] += 1
        th = V.fit_bt(W, prior=0.01)
        self.assertGreater(np.corrcoef(th - th.mean(), true)[0, 1], 0.99)
        self.assertLess(np.max(np.abs((th - th.mean()) - true)), 0.25)

    def test_finite_when_a_brand_always_wins(self):
        W = np.array([[0, 5, 5], [0, 0, 3], [0, 2, 0]], float)
        th = V.fit_bt(W)
        self.assertTrue(np.all(np.isfinite(th)))
        self.assertEqual(int(np.argmax(th)), 0)

    def test_gradient_zero_at_solution(self):
        rng = np.random.default_rng(2)
        W = rng.integers(0, 6, (6, 6)).astype(float)
        np.fill_diagonal(W, 0)
        th = V.fit_bt(W, prior=1.0)
        N = W + W.T
        s = 1 / (1 + np.exp(-(th[:, None] - th[None, :])))
        g = (W - N * s).sum(1) + 0.5 - 1 / (1 + np.exp(-th))
        self.assertLess(np.max(np.abs(g)), 1e-8)

    def test_no_comparisons_gives_zero(self):
        self.assertTrue(np.allclose(V.fit_bt(np.zeros((3, 3))), 0.0))


class Comparisons(unittest.TestCase):
    def test_pairs_and_ties(self):
        rows = _rows([["A", "B", "C"], [("A", "B"), "C"]])
        pd = V.PairData(rows)
        W = pd.win_matrix()
        i = pd.idx
        self.assertEqual(W[i["A"], i["B"]], 1.5)     # answer 1: A before B; answer 2: tie (half each)
        self.assertEqual(W[i["B"], i["A"]], 0.5)
        self.assertEqual(W[i["A"], i["C"]], 2.0)
        self.assertEqual(W.sum(), 6.0)               # 3 + 3 pairs
        self.assertEqual(list(pd.count), [2, 2, 2])

    def test_per_answer_weighting(self):
        pd = V.PairData(_rows([["A", "B", "C"], ["A", "B"]]), weighting="per_answer")
        self.assertAlmostEqual(pd.win_matrix().sum(), 3 * 0.5 + 1.0)

    def test_shuffle_keeps_comparisons_and_breaks_ties(self):
        pd = V.PairData(_rows([[("A", "B"), "C", "D"], ["B", "A"], ["C", "D", "A"]]))
        ka, kb = pd.shuffled_keys(np.random.default_rng(3))
        W = pd.win_matrix(ka, kb)
        N0 = pd.win_matrix()
        self.assertTrue(np.allclose(W + W.T, N0 + N0.T))    # who meets whom is unchanged
        self.assertTrue(np.all((W == np.round(W))))          # no half wins after the shuffle

    def test_rating_needs_floor_and_main_component(self):
        ans = [["A", "B"]] * 6 + [["C", "D"]] * 7 + [["A", "B", "E"]]
        U = V.prec_units(_rows(ans))
        self.assertTrue(U[("c1", "A")]["rated"])
        self.assertFalse(U[("c1", "C")]["rated"])            # 7 mentions, but outside the main component
        self.assertFalse(U[("c1", "E")]["rated"])            # in the main component, below the floor
        self.assertGreater(U[("c1", "A")]["PREC"], U[("c1", "B")]["PREC"])

    def test_frequency_does_not_enter_direction(self):
        """Doubling every answer that names B (B named twice as often, same head-to-head proportions) changes
        PREC only through the prior's shrinkage: with a negligible prior the values stay. Counts are exactly
        Bradley-Terry with strengths 2 : 1 : 0.5, so the fit is the same at any scaling of a pair."""
        base = [["A", "B"]] * 2 + [["B", "A"]] + [["B", "C"]] * 2 + [["C", "B"]] + [["A", "C"]] * 4 + [["C", "A"]]
        more_b = base + [a for a in base if "B" in a]
        U1 = V.prec_units(_rows(base), floor=1, prior=1e-6)
        U2 = V.prec_units(_rows(more_b), floor=1, prior=1e-6)
        self.assertGreater(U2[("c1", "B")]["n_ranked"], U1[("c1", "B")]["n_ranked"])
        for b in "ABC":
            self.assertAlmostEqual(U1[("c1", b)]["PREC"] - U1[("c1", "C")]["PREC"],
                                   U2[("c1", b)]["PREC"] - U2[("c1", "C")]["PREC"], places=4)

    def test_list_length_does_not_enter(self):
        """Appending brands after the compared pair (longer lists) leaves A vs B's head-to-head and so the
        sign of PREC_A - PREC_B unchanged; MODE (absolute position) would move."""
        short = [["A", "B"], ["B", "A"], ["A", "B"]] * 3
        long = [x + ["X1", "X2", "X3"] for x in short]
        for ans in (short, long):
            U = V.prec_units(_rows(ans), floor=1)
            self.assertGreater(U[("c1", "A")]["PREC"], U[("c1", "B")]["PREC"])

    def test_first_position_concentration(self):
        f = V.first_position_concentration(_rows([["A", "B"], ["A", "C"], ["B", "A"], [("A", "B")]]))
        self.assertEqual(f["c1"]["modal_first_brand"], "A")
        self.assertAlmostEqual(f["c1"]["share"], 3 / 4)


class VerdictRules(unittest.TestCase):
    def test_multi_wave_separability(self):
        f = V.verdict_sep_multi
        self.assertEqual(f({"t1": (0.1, 50), "t2": (-0.2, 50), "t3": (0.3, 50), "t4": (0.05, 70)}), "CONFIRMED")
        self.assertEqual(f({"t1": (0.1, 50), "t2": (0.31, 50), "t3": (0.2, 50), "t4": (0.05, 70)}), "MARGINAL")
        self.assertEqual(f({"t1": (0.1, 50), "t2": (-0.5, 50), "t3": (0.2, 50), "t4": (0.05, 70)}), "FALSIFIED")
        self.assertEqual(f({"t1": (0.1, 50), "t2": (0.1, 29), "t3": (0.9, 10), "t4": (0.05, 70)}), "UNDETERMINED")
        self.assertEqual(f({"t1": (0.1, 50), "t2": (0.1, 29), "t3": (0.2, 30), "t4": (0.05, 70)}), "CONFIRMED")

    def test_gate_and_consequence(self):
        g = V.gate
        self.assertEqual(g("CONFIRMED", "CONFIRMED", "CONFIRMED", "CONFIRMED"), "PASS")
        self.assertEqual(g("CONFIRMED", "CONFIRMED", "CONFIRMED", "MARGINAL"), "PASS")
        self.assertEqual(g("CONFIRMED", "CONFIRMED", "CONFIRMED", "FALSIFIED"), "MARGINAL")
        self.assertEqual(g("MARGINAL", "CONFIRMED", "CONFIRMED", None), "MARGINAL")
        self.assertEqual(g("CONFIRMED", "UNDETERMINED", "CONFIRMED", None), "UNDETERMINED")
        self.assertEqual(g("CONFIRMED", "UNDETERMINED", "FALSIFIED", None), "FAIL")
        for v in ("FAIL", "MARGINAL", "UNDETERMINED"):
            self.assertIn("reported as part of Presence", V.consequence(v))
            self.assertIn("no further Ranking redesign", V.consequence(v))
        self.assertNotIn("part of Presence", V.consequence("PASS"))

    def test_bands_are_v1_10s(self):
        self.assertEqual((V.SEP_CONF, V.SEP_FALS, V.STAB_CONF, V.STAB_FALS, V.N_FLOOR_UNITS), (0.30, 0.50, 0.50, 0.30, 30))
        self.assertEqual(R.verdict_stability(0.6, 0.01, 0.01, 40), "CONFIRMED")
        self.assertEqual(R.verdict_stability(0.6, 0.01, 0.06, 40), "FALSIFIED")


class Pipeline(unittest.TestCase):
    def test_synthetic_worlds_known_answers(self):
        """Small-draw version of the recorded dry run: world A passes, B fails on H1, C fails on H3."""
        for world, exp in V.EXPECTED.items():
            with tempfile.TemporaryDirectory() as td:
                pins = V.build_synthetic(Path(td), world)
                inp = V.load_inputs(Path(td), pins)
                res = V.analyse(inp, log=lambda m: None, n_shuffle=60, n_perm=200, boot=False, sensitivities=False)
                got = {"GATE": res["GATE"], "H1": res["H1_Sep_Presence"]["verdict"],
                       "H3": res["H3_Retest_t1_t2"]["verdict"]}
                for k, v in exp.items():
                    self.assertEqual(got[k], v, f"{world}: {k}")

    def test_pins_halt_on_change(self):
        with tempfile.TemporaryDirectory() as td:
            pins = V.build_synthetic(Path(td), "C_noise_order")
            p = Path(td) / V.PROFILES_REL
            p.write_text(p.read_text() + "\n")
            with self.assertRaises(V.Halt):
                V.load_inputs(Path(td), pins)

    def test_t4_rank_table_must_match_v1_14_record(self):
        with tempfile.TemporaryDirectory() as td:
            pins = V.build_synthetic(Path(td), "C_noise_order")
            sp = Path(td) / V.T4_STAGE1_REL
            d = json.loads(sp.read_text())
            d["rank_table_t4_sha256"] = "0" * 64
            sp.write_text(json.dumps(d))
            pins[V.T4_STAGE1_REL] = V.sha256_file(sp)
            with self.assertRaises(V.Halt):
                V.load_inputs(Path(td), pins)

    def test_run_path_on_synthetic(self):
        """run() end to end (bootstrap on, sensitivities on) with its inputs redirected to a synthetic set and
        its lock checks stubbed; draws reduced. No real answer is scored."""
        orig = {k: getattr(V, k) for k in ("lock_status", "input_parity", "load_inputs", "analyse",
                                           "RESULTS_FILE", "OUT_DIR", "ANCHOR_FILE")}
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            pins = V.build_synthetic(td / "in", "A_independent_precedence")
            (td / "anchor.json").write_text("{}")
            try:
                V.lock_status = lambda: []
                V.input_parity = lambda log=print: {"checks": {"all_pass": True}}
                V.load_inputs = lambda root=None, pins_=None: orig["load_inputs"](td / "in", pins)
                V.analyse = lambda inp, log=print: orig["analyse"](inp, log=lambda m: None, n_shuffle=5, n_perm=20)
                V.RESULTS_FILE, V.OUT_DIR, V.ANCHOR_FILE = td / "out/results.json", td / "out", td / "anchor.json"
                res = V.run(log=lambda m: None)
            finally:
                for k, v in orig.items():
                    setattr(V, k, v)
            out = json.loads((td / "out/results.json").read_text())
            self.assertEqual(out["GATE"], res["GATE"])
            self.assertIn("CONSEQUENCE", out)
            self.assertIn("S_COI_without_Denon_and_Cheil_Iris", out["sensitivities"])
            self.assertEqual(len(out["E1_moderators"]["cells"]), 20)
            self.assertTrue(np.isfinite(out["H1_Sep_Presence"]["per_wave"]["t1"]["ci90"][0]))

    def test_dry_run_record_matches_expected(self):
        d = json.loads((V.DRY_DIR / "dryrun_v1_16.json").read_text())
        self.assertTrue(d["all_match_expected"])
        self.assertEqual(d["draws"], {"perm": 10000, "shuffle": 10000})

    def test_run_refuses_before_lock(self):
        if V.tag_exists():
            self.skipTest("tag exists")
        with self.assertRaises(V.Halt):
            V.run(log=lambda m: None)


class RealInputParity(unittest.TestCase):
    """Counts and n's only on the real pinned inputs (allowed before the lock)."""

    def test_parity_reproduces_published_counts(self):
        out = V.input_parity(log=lambda m: None)
        self.assertTrue(out["checks"]["all_pass"], out["checks"])
        self.assertEqual(out["waves"]["t4"]["rankable_rows_S0"], 1641)
        self.assertEqual(out["waves"]["t4"]["rankable_rows_S1"], 1375)
        self.assertEqual(out["waves"]["t4"]["units_at_floor_S0"], 71)
        txt = json.dumps(out)
        self.assertNotIn('"PREC"', txt)                 # no precedence value on real data
        self.assertNotIn("rho", txt)                    # no correlation on real data

    def test_pins_are_filled_and_coi_keys_exist(self):
        for rel, h in V.INPUT_PINS.items():
            self.assertRegex(h, r"^[0-9a-f]{64}$", rel)
        import csv
        with open(V.ROOT / V.PROFILES_REL, encoding="utf-8") as fh:
            keys = {(r["substrate"], r["brand"]) for r in csv.DictReader(fh)}
        for k in (V.DENON,) + V.COI_CHEIL:
            self.assertIn(k, keys)
        reg = json.loads((V.ROOT / "osf/methodology/v1_10/registries/v0_23_registry_v1_10.json").read_text())
        self.assertIn('"id": "S03", "brand": "Jack Daniel\'s"', json.dumps(reg))


class LockManifest(unittest.TestCase):
    def test_locked_files_listed(self):
        for f in V.LOCKED_FILES:
            self.assertFalse(f.startswith("/"))
        for f in ("scripts/score_v1_16.py", "scripts/test_score_v1_16.py", "scripts/score_v1_10.py",
                  "scripts/score_v1_14.py", V.T4_RANK_REL, V.T4_STAGE1_REL):
            self.assertIn(f, V.LOCKED_FILES)
        self.assertEqual(sum(1 for f in V.LOCKED_FILES if "/rank_tables/OMNI_" in f), 15)


if __name__ == "__main__":
    unittest.main(verbosity=2)
