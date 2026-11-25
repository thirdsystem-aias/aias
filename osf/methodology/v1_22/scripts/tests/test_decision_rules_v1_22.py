import itertools
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import score_v1_22 as s  # noqa: E402

V = (s.C, s.M, s.F, s.U)


class Route(unittest.TestCase):
    def test_routes(self):
        self.assertEqual(s.paper_b_route("PASS", {"go": True, "date": "d", "text": "t"}), "REFUSED")
        self.assertEqual(s.paper_b_route("MARGINAL", None), "NOT_RUN_PENDING")
        self.assertEqual(s.paper_b_route("MARGINAL", {"go": True}), "NOT_RUN_PENDING")
        self.assertEqual(s.paper_b_route("MARGINAL", {"go": True, "date": "d", "text": "t"}), "RUN")
        self.assertEqual(s.paper_b_route("MARGINAL", {"go": False, "date": "d", "text": "t"}), "NOT_RUN_DECLINED")


class GateCompletion(unittest.TestCase):
    def test_exhaustive_single_outcome(self):
        for combo in itertools.product(V, repeat=4):
            self.assertIn(s.gate_completion(*combo), {"PASS", "FAIL", "MARGINAL", "UNDETERMINED"})

    def test_pass_requires_hb1_and_reliability(self):
        for combo in itertools.product(V, repeat=4):
            if s.gate_completion(*combo) == "PASS":
                hb1, hb2, hb3, hb4 = combo
                self.assertEqual(hb1, s.C)
                self.assertIn(s.C, (hb2, hb3))
                self.assertNotIn(s.F, (hb2, hb3, hb4))

    def test_any_falsification_without_confirmation_fails(self):
        self.assertEqual(s.gate_completion(s.F, s.C, s.C, s.C), "FAIL")
        self.assertEqual(s.gate_completion(s.C, s.F, s.U, s.C), "FAIL")
        self.assertEqual(s.gate_completion(s.C, s.C, s.U, s.F), "FAIL")
        self.assertEqual(s.gate_completion(s.C, s.C, s.F, s.C), "MARGINAL")  # MIXED
        self.assertEqual(s.gate_completion(s.C, s.U, s.U, s.M), "UNDETERMINED")
        self.assertEqual(s.gate_completion(s.M, s.C, s.U, s.C), "MARGINAL")


class Bands(unittest.TestCase):
    def test_retest(self):
        self.assertEqual(s.retest_verdict(0.6, 0.01, 29), s.U)
        self.assertEqual(s.retest_verdict(0.5, 0.049, 30), s.C)
        self.assertEqual(s.retest_verdict(0.5, 0.05, 30), s.M)
        self.assertEqual(s.retest_verdict(0.2999, 0.5, 40), s.F)

    def test_signed(self):
        self.assertEqual(s.signed_band_verdict(0.35, 0.01, True, +1), s.C)
        self.assertEqual(s.signed_band_verdict(-0.35, 0.01, True, +1), "CONFIRMED_REVERSED")
        self.assertEqual(s.signed_band_verdict(0.1, 0.5, True, +1), s.F)
        self.assertEqual(s.signed_band_verdict(0.2, 0.01, True, +1), s.M)
        self.assertEqual(s.signed_band_verdict(0.9, 0.0, False, +1), s.U)

    def test_channel_and_replication(self):
        self.assertEqual(s.channel_verdict(6, 0.01, 20, 3), s.C)
        self.assertEqual(s.channel_verdict(-3, 0.9, 25, 4), s.F)
        self.assertEqual(s.channel_verdict(3, 0.2, 25, 4), s.M)
        self.assertEqual(s.channel_verdict(9, 0.0, 19, 4), s.U)
        self.assertEqual(s.replication_verdict(0.2, 0.01, 30), s.C)
        self.assertEqual(s.replication_verdict(0.15, 0.2, 30), s.F)
        self.assertEqual(s.replication_verdict(0.15, 0.01, 30), s.M)

    def test_seeds_unique(self):
        self.assertEqual(len(set(s.SEEDS.values())), len(s.SEEDS))


if __name__ == "__main__":
    unittest.main()
