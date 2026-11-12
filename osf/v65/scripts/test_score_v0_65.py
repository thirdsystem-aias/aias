#!/usr/bin/env python3
"""Unit tests for score_v0_65.py (pre-registration DRAFT r0). Synthetic data and the pinned v0.62 design files only:
no archive answer is read, no network, no model call. Run: python3 osf/v65/scripts/test_score_v0_65.py"""
import math
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_v0_65 as S  # noqa: E402

N_SMALL = 300


def row(cid, sub, brand, model, run, frame, m, cond="S0"):
    return {"call_id": cid, "substrate": sub, "brand": brand, "model": model, "condition": cond, "run": str(run),
            "probe_id": frame, "frame_id": frame, "mentioned": str(m)}


class DesignInputs(unittest.TestCase):
    def test_channel_map_trio(self):
        cm = S.channel_map()
        self.assertEqual(len(cm), 30)
        for s in S.TRIO:
            self.assertEqual([cm[(s, f"q{i}")] for i in range(1, 7)], ["cat"] * 3 + ["cult"] * 3)

    def test_channel_map_exploratory_categories(self):
        cm = S.channel_map()
        for s in S.EXPLORATORY:
            chans = [c for (ss, _f), c in cm.items() if ss == s]
            self.assertEqual(sorted(chans), ["cat"] * 3 + ["cult"] * 3)

    def test_drift_map_complete(self):
        dm = S.drift_map()
        self.assertEqual(len(dm), 90)
        self.assertTrue(set(dm.values()) <= {"equivalent", "minor drift", "meaning change"})

    def test_seeds_unique(self):
        flat = [v for v in S.SEEDS.values() if isinstance(v, int)] + list(S.SEEDS["dry_run"])
        self.assertIn(650161, flat)
        self.assertEqual(len(flat), len(set(flat)))

    def test_coi_set_imported_from_v062(self):
        trio_flagged = [u for u in S.P62.COI_FLAGGED if u[0] in S.TRIO]
        self.assertEqual(sorted(trio_flagged), [("v0.20", "Eucerin"), ("v0.22", "BMW"), ("v0.22", "Bentley"),
                                                ("v0.22", "Chevrolet")])


class Kernel(unittest.TestCase):
    def _tiny(self):
        cm = {("v0.20", "q1"): "cat", ("v0.20", "q2"): "cat", ("v0.20", "q3"): "cult", ("v0.20", "q4"): "cult"}
        rows = []
        for i, (fr, mb) in enumerate([("q1", 1), ("q2", 0), ("q3", 1), ("q4", 1)]):
            cid = f"c{i}"
            rows.append(row(cid, "v0.20", "B", S.MODELS[0], 1, fr, mb))
            rows.append(row(cid, "v0.20", "Z", S.MODELS[0], 1, fr, 0))
        rows.append(row("s1", "v0.20", "B", S.MODELS[0], 1, "q1", 1, cond="S1"))   # search-on row ignored
        return cm, rows

    def test_il_rate_and_count(self):
        cm, rows = self._tiny()
        v = S.il_values(rows, [("v0.20", "B"), ("v0.20", "Z")], cm)
        b = v[("v0.20", "B")]
        self.assertEqual((b["c_cat"], b["c_cult"], b["n_cat"], b["n_cult"]), (1, 2, 2, 2))
        self.assertAlmostEqual(b["il"], 2 / 2 - 1 / 2)
        self.assertEqual(b["il_count"], 1.0)
        self.assertAlmostEqual(b["pi"], 3 / 4)

    def test_frames_keep_and_excluded_calls(self):
        cm, rows = self._tiny()
        v = S.il_values(rows, [("v0.20", "B")], cm, frames_keep={("v0.20", "q1"), ("v0.20", "q3")})
        self.assertAlmostEqual(v[("v0.20", "B")]["il"], 0.0)
        v = S.il_values(rows, [("v0.20", "B")], cm, excluded_calls={"c0"})
        self.assertAlmostEqual(v[("v0.20", "B")]["il"], 1.0)
        v = S.il_values(rows, [("v0.20", "B")], cm, frames_keep={("v0.20", "q1")})
        self.assertTrue(math.isnan(v[("v0.20", "B")]["il"]))     # no cultural question left -> undefined

    def test_eligibility(self):
        cm, rows = self._tiny()
        v = S.il_values(rows, [("v0.20", "B"), ("v0.20", "Z")], cm)
        self.assertTrue(S.eligible(v[("v0.20", "B")]))
        self.assertFalse(S.eligible(v[("v0.20", "Z")]))          # pi = 0
        self.assertFalse(S.eligible({"il": 0.0, "pi": 1.0}))     # saturated
        self.assertFalse(S.eligible(None))

    def test_partial_matches_residual_method(self):
        rng = np.random.default_rng(1)
        g = np.repeat(["a", "b", "c"], 20)
        z = rng.normal(size=60)
        x = z + rng.normal(size=60)
        y = z + rng.normal(size=60)
        rx, ry, rz = (S.S62.centred_ranks(v, g) for v in (x, y, z))
        ex = rx - np.polyfit(rz, rx, 1)[0] * rz
        ey = ry - np.polyfit(rz, ry, 1)[0] * rz
        self.assertAlmostEqual(S.partial_rho_c(x, y, z, g), np.corrcoef(ex, ey)[0, 1], places=10)


class Verdicts(unittest.TestCase):
    def test_h1_bands(self):
        self.assertEqual(S.verdict_h1(60, 0.50, 0.01), "CONFIRMED")
        self.assertEqual(S.verdict_h1(60, 0.50, 0.05), "MARGINAL")
        self.assertEqual(S.verdict_h1(60, 0.4999, 0.001), "MARGINAL")
        self.assertEqual(S.verdict_h1(60, 0.30, 0.2), "MARGINAL")
        self.assertEqual(S.verdict_h1(60, 0.2999, 0.2), "FALSIFIED")
        self.assertEqual(S.verdict_h1(44, 0.9, 0.0001), "UNDETERMINED")
        self.assertEqual(S.verdict_h1(45, 0.9, 0.0001), "CONFIRMED")
        self.assertEqual(S.verdict_h1(60, float("nan"), 0.01), "UNDETERMINED")

    def test_h2_bands(self):
        self.assertEqual(S.verdict_h2(60, -0.30, 0.01, 0.99), ("CONFIRMED", None))
        self.assertEqual(S.verdict_h2(60, -0.30, 0.06, 0.94), ("MARGINAL", None))
        self.assertEqual(S.verdict_h2(60, -0.15, 0.2, 0.8), ("MARGINAL", None))
        self.assertEqual(S.verdict_h2(60, -0.1499, 0.2, 0.8), ("FALSIFIED", None))
        self.assertEqual(S.verdict_h2(60, 0.35, 0.99, 0.01), ("FALSIFIED", "REVERSED"))
        self.assertEqual(S.verdict_h2(60, 0.35, 0.9, 0.10), ("FALSIFIED", None))
        self.assertEqual(S.verdict_h2(40, -0.9, 0.0001, 1.0), ("UNDETERMINED", None))

    def test_h3_bands(self):
        e = S.H3_SESOI
        self.assertEqual(S.verdict_h3(60, 0.0, [-e / 2, e / 2]), ("FALSIFIED", "equivalent within the bound"))
        self.assertEqual(S.verdict_h3(60, 2 * e, [e, 3 * e]), ("CONFIRMED", "toward cultural"))
        self.assertEqual(S.verdict_h3(60, -2 * e, [-3 * e, -e / 2]), ("CONFIRMED", "toward category"))
        self.assertEqual(S.verdict_h3(60, e / 2, [e / 4, 3 * e / 4]), ("FALSIFIED", "equivalent within the bound"))
        self.assertEqual(S.verdict_h3(60, e / 2, [e / 4, 1.2 * e]), ("MARGINAL", None))
        self.assertEqual(S.verdict_h3(60, 0.0, [-2 * e, 2 * e]), ("MARGINAL", None))
        self.assertEqual(S.verdict_h3(10, 1.0, [0.5, 1.5]), ("UNDETERMINED", None))

    def test_joint_reading(self):
        self.assertEqual(S.joint_reading({"es": "CONFIRMED", "ko": "CONFIRMED", "zh": "CONFIRMED"}), "IL-portable")
        self.assertEqual(S.joint_reading({"es": "CONFIRMED", "ko": "FALSIFIED", "zh": "MARGINAL"}),
                         "IL-language-bound (KO)")
        self.assertEqual(S.joint_reading({"es": "CONFIRMED", "ko": "UNDETERMINED", "zh": "MARGINAL"}),
                         "Partly portable")

    def test_perm_two_tails(self):
        rng = np.random.default_rng(3)
        g = np.repeat(["a", "b"], 25)
        y = rng.normal(size=50)
        x = -y + 0.3 * rng.normal(size=50)
        stat = (lambda xx: S.S62.rho_c(xx, y, g))
        lo, hi = S.perm_two_tails(stat, x, g, 7, 400)
        self.assertLess(lo, 0.01)
        self.assertGreater(hi, 0.99)


class DryRunScenarios(unittest.TestCase):
    """End to end on synthetic v0.62-shaped worlds (small numbers of draws; the dry-run file uses 2,000)."""

    @classmethod
    def setUpClass(cls):
        cls.cm, cls.dm = S.channel_map(), S.drift_map()
        cls.units = S.synthetic_units()

    def _run(self, seed, spec, drop=None):
        en, lr = S.synthetic_world(seed, self.units, self.cm, spec, drop)
        return S.score(self.units, en, lr, self.cm, self.dm, n_perm=N_SMALL, n_boot=N_SMALL)

    def test_units_shape(self):
        self.assertEqual(len(self.units), 112)
        self.assertEqual(sum(1 for u in self.units if u[0] in S.TRIO), 72)

    def test_portable(self):
        r = self._run(650151, {})
        self.assertEqual(r["joint_reading"], "IL-portable")
        for lg in S.LANGS:
            self.assertNotEqual(r["tests"][f"H2_IL_Moderates_Language_{lg}"]["verdict"], "CONFIRMED")
            self.assertNotEqual(r["tests"][f"H3_IL_Shift_{lg}"]["verdict"], "CONFIRMED")
            self.assertEqual(r["sensitivities"][lg]["S-COI"]["n_units"], 68)
            mc = r["descriptives"]["D5_counts"][lg]["MC_Channel_answered_calls"]
            self.assertEqual(set(mc.values()), {27})
            self.assertEqual(len(mc), 6)

    def test_language_bound_ko(self):
        r = self._run(650152, {"ko": {"r": 0.0}})
        self.assertEqual(r["tests"]["H1_IL_Order_ko"]["verdict"], "FALSIFIED")
        self.assertIn("KO", r["joint_reading"])

    def test_shift_zh(self):
        r = self._run(650153, {"zh": {"shift": 1.0}})
        t = r["tests"]["H3_IL_Shift_zh"]
        self.assertEqual((t["verdict"], t["direction"]), ("CONFIRMED", "toward cultural"))

    def test_moderation_es(self):
        r = self._run(650154, {"es": {"kappa": -1.0}})
        self.assertEqual(r["tests"]["H2_IL_Moderates_Language_es"]["verdict"], "CONFIRMED")

    def test_drop_rule_es(self):
        r = self._run(650155, {}, {"es": ("gemini-4-argon", 0.20)})
        for h in ("H1_IL_Order_es", "H2_IL_Moderates_Language_es", "H3_IL_Shift_es"):
            self.assertEqual(r["tests"][h]["verdict"], "UNDETERMINED")
        for sens in ("S-COI", "S-Drift", "S-Count"):
            self.assertEqual(r["sensitivities"]["es"][sens]["H1"]["verdict"], "UNDETERMINED")
        self.assertNotEqual(r["tests"]["H1_IL_Order_ko"]["verdict"], "UNDETERMINED")

    def test_s_drift_keeps_only_equivalent_frames(self):
        r = self._run(650151, {})
        for lg in S.LANGS:
            kept = r["sensitivities"][lg]["S-Drift"]["frames_kept"]
            for k in kept:
                s, f = k.split("/")
                self.assertEqual(self.dm[(lg, s, f)], "equivalent")

    def test_unavailable_sensitivities_reported(self):
        r = self._run(650151, {})
        self.assertEqual(r["sensitivities"]["es"]["S-Alias"]["status"], "not applicable")
        self.assertEqual(r["sensitivities"]["ko"]["S-Language"]["status"], "NOT AVAILABLE")
        self.assertEqual(r["sensitivities"]["es"]["S-Script"]["status"], "not applicable")

    def test_deterministic(self):
        a, b = self._run(650151, {}), self._run(650151, {})
        self.assertEqual(a["tests"]["H1_IL_Order_es"]["rho_c"], b["tests"]["H1_IL_Order_es"]["rho_c"])
        self.assertEqual(a["tests"]["H1_IL_Order_es"]["p_perm_one_sided"],
                         b["tests"]["H1_IL_Order_es"]["p_perm_one_sided"])


class LockAndGuard(unittest.TestCase):
    def test_guard_refuses(self):
        self.assertEqual(len(S.guard_run(False, False, True, False)), 4)
        self.assertEqual(S.guard_run(True, True, False, True), [])
        self.assertIn("v0.62 not yet scored (osf/v62/v62_verdicts.json missing)", S.guard_run(True, False, False, True))

    def test_manifest_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "a.txt").write_text("x")
            m = Path(d) / "m.sha256"
            S.write_manifest(m, ["a.txt"], root=d)
            self.assertEqual(S.verify_manifest(m, root=d), [])
            (Path(d) / "a.txt").write_text("y")
            self.assertEqual(S.verify_manifest(m, root=d), ["changed a.txt"])

    def test_en_blobs_pinned(self):
        """Metadata only: the blob ids of t4's coded tables at v0.42-scoring-locked equal the pinned ids."""
        self.assertEqual(S.en_blob_ids(), S.EN_BLOBS)

    def test_t1_il_hash_matches_v037_baseline_if_present(self):
        base = S.ROOT / "osf/v37/.v37_il_direct_baseline.sha256"
        if not base.exists():
            self.skipTest("v0.37 baseline file not in this tree")
        _il, h = S.read_t1_il()
        self.assertEqual(h, base.read_text().strip())


if __name__ == "__main__":
    unittest.main(verbosity=2)
