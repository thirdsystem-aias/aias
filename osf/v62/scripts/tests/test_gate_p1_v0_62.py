"""Gate P1 (kernel parity against v0.42's locked kernels, tag v0.42-prereg-r1) on synthetic tables. No model, no
network; reads the pinned kernel source with `git show` (skipped if the v0.42 worktree is absent)."""
import sys
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import gate_p1_v0_62 as G  # noqa: E402
import score_v0_62 as S  # noqa: E402

REPO = Path.home() / "aias" / "_worktrees" / "v0.42"


@unittest.skipUnless(REPO.exists(), "v0.42 worktree not present")
class GateP1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ns, cls.pin = G.pinned_namespace(REPO)
        cls.U = G.units()

    def test_pinned_to_tag_commit(self):
        self.assertEqual(self.pin["commit"], G.TAG_COMMIT)

    def test_parity_complete_and_missing(self):
        for scen, seed in (("complete", 620151), ("missing", 620152)):
            bad, parts = G.compare(self.ns, self.U, G.synth(self.U, seed, scen))
            self.assertEqual(bad, [], scen)
            self.assertGreater(parts.get("defined", 0), 50)

    def test_gate_detects_a_wrong_kernel(self):
        def wrong_phi_m(k):
            phi, pi, part = S.phi_m.__wrapped__(k) if hasattr(S.phi_m, "__wrapped__") else ORIG(k)
            return (None if phi is None else phi * 1.000001), pi, part
        ORIG = S.phi_m
        with mock.patch.object(S, "phi_m", wrong_phi_m):
            bad, _ = G.compare(self.ns, self.U, G.synth(self.U, 620151, "complete"))
        self.assertTrue(bad)

    def test_gate_detects_a_wrong_denominator(self):
        rows = G.synth(self.U, 620152, "missing")
        orig = S.unit_values

        def wrong(units, B, models=S.MODELS):
            out = orig(units, B, models)
            for u in out:
                out[u]["pi"] = out[u]["pi"] * 54 / 54.0000001
            return out
        with mock.patch.object(S, "unit_values", wrong):
            bad, _ = G.compare(self.ns, self.U, rows)
        self.assertTrue(bad)


if __name__ == "__main__":
    unittest.main()
