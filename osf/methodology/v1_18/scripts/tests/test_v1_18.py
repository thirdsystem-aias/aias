"""Tests for v1.18 (synthetic data only; the domain-table test reads only the table and the blind domain list).
Run: python3 -m unittest discover -s osf/methodology/v1_18/scripts/tests -v"""
import random
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import analyse_v1_18 as A  # noqa: E402
import common_v1_18 as C  # noqa: E402

T = {"c.ex": {"cls": "company", "retailer": False, "alias_of": "v19:X"},
     "l.ex": {"cls": "listing", "retailer": True, "alias_of": ""},
     "r.ex": {"cls": "review_social", "retailer": False, "alias_of": ""},
     "e.ex": {"cls": "editorial_other", "retailer": False, "alias_of": ""},
     "u.ex": {"cls": "UNRESOLVED", "retailer": False, "alias_of": ""}}
ALL_DB = {"own.ex", "rival.ex"}


class TestV118(unittest.TestCase):
    def test_four_definitions_on_one_answer(self):
        ps = C.pair_shares({"own.ex", "rival.ex", "c.ex", "l.ex", "r.ex", "e.ex", "u.ex"}, "v19:B", {"own.ex"},
                           ALL_DB, T, {})
        self.assertAlmostEqual(ps["K_own_domain"], 1 / 6)
        self.assertAlmostEqual(ps["P_any_company"], 3 / 6)      # own + rival (registry D_b) + c.ex
        self.assertAlmostEqual(ps["Y_own_plus_listings"], 2 / 6)
        self.assertAlmostEqual(ps["M_not_owned"], 5 / 6)
        self.assertAlmostEqual(ps["K_own_domain"] + ps["M_not_owned"], 1.0)   # identity (common denominator)

    def test_unresolved_modes(self):
        d = {"own.ex", "u.ex"}
        self.assertEqual(C.pair_shares(d, "v19:B", {"own.ex"}, ALL_DB, T, {})["K_own_domain"], 1.0)
        out = C.pair_shares(d, "v19:B", {"own.ex"}, ALL_DB, T, {"unresolved": "out"})
        self.assertEqual((out["K_own_domain"], out["P_any_company"], out["M_not_owned"]), (0.5, 0.5, 0.5))
        inn = C.pair_shares(d, "v19:B", {"own.ex"}, ALL_DB, T, {"unresolved": "in"})
        self.assertEqual((inn["P_any_company"], inn["Y_own_plus_listings"], inn["K_own_domain"]), (1.0, 1.0, 0.5))
        self.assertIsNone(C.pair_shares({"u.ex"}, "v19:B", {"own.ex"}, ALL_DB, T, {}))

    def test_focal_is_brand_relative(self):
        self.assertEqual(C.domain_class("rival.ex", {"own.ex"}, ALL_DB, T, {}), "company")
        self.assertEqual(C.domain_class("own.ex", {"own.ex"}, ALL_DB, T, {}), "focal")

    def test_retailer_and_alias_sensitivities(self):
        self.assertEqual(C.domain_class("l.ex", set(), ALL_DB, T, {"retailer_as_company": True}), "company")
        self.assertEqual(C.domain_class("c.ex", set(), ALL_DB, T, {"alias_focal": True, "unit": "v19:X"}), "focal")
        self.assertEqual(C.domain_class("c.ex", set(), ALL_DB, T, {"alias_focal": True, "unit": "v19:Y"}), "company")

    def test_missing_domain_halts(self):
        with self.assertRaises(KeyError):
            C.domain_class("nowhere.ex", set(), ALL_DB, T, {})

    def test_rho_w_matches_v113_convention(self):
        s = C.load_v113()
        rng = random.Random(7)
        xd, yd, xs, ys, gs = {}, {}, [], [], []
        for sub in ("v19", "v20", "v21"):
            for i in range(8):
                x, y = rng.choice([0, 1, 2, 3, 5]), rng.random()
                xd[(sub, str(i))], yd[(sub, str(i))] = x, y
                xs.append(x), ys.append(y), gs.append(sub)
        mine, n = C.rho_w(xd, yd)
        self.assertEqual(n, 24)
        self.assertAlmostEqual(mine, s.rho_w(xs, ys, gs), places=12)

    def test_synthetic_known_answer(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(A.dry_run(d, n_boot=50), 0)

    def test_gate_refuses_without_tag_or_with_manifest_mismatch(self):
        with self.assertRaises(A.Refused):
            A.gate(tag_check=lambda: (False, "absent"), manifest_check=lambda: (True, []))
        with self.assertRaises(A.Refused):
            A.gate(tag_check=lambda: (True, "x"), manifest_check=lambda: (False, ["f"]))
        self.assertTrue(A.gate(tag_check=lambda: (True, "x"), manifest_check=lambda: (True, [])))

    def test_real_gate_refuses_now(self):
        ok, _ = A.tag_on_origin()
        if not ok:
            with self.assertRaises(A.Refused):
                A.main(["--run", "--t4", "x", "--coded", "y"])

    def test_real_loader_path_on_fake_records(self):
        s = C.load_v113()
        classes = s.load_classes(C.V113_CLASSES)
        recs = [{"call_id": "c1", "substrate": "v19", "model_requested": "gpt-6-astra", "probe_id": "p1",
                 "frame_id": "f1", "run": "2", "search": {"citations": [
                     {"url": "https://www.own.test/a?utm_source=openai", "title": None},
                     {"url": "https://shop.own.test/b", "title": None},
                     {"url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/x", "title": "rival.test"},
                     {"url": "not a url", "title": None}]}}]
        ans = C.answers_from_records(recs, {"c1": {("v19", "B")}}, classes, s, "citations")
        self.assertEqual(ans[0]["domains"], {"own.test", "rival.test"})
        self.assertEqual((ans[0]["cell"], ans[0]["run"]), (("v19", "gpt-6-astra", "p1", "f1"), 2))
        units = {("v19", "B"): {"status": "RESOLVED", "domains": {"own.test"}},
                 ("v19", "R"): {"status": "RESOLVED", "domains": {"rival.test"}}}
        st, pairs = C.brand_shares(ans, units, {"own.test", "rival.test"}, {}, floor=1)
        self.assertEqual((st[("v19", "B")]["K_own_domain"], st[("v19", "B")]["P_any_company"]), (50.0, 100.0))

    def test_domain_table_is_valid_and_complete(self):
        table = C.load_domain_table()
        blind = (C.PHASE / "outputs" / "prelock" / "domains_to_classify_v1_18.txt").read_text().split()
        self.assertTrue(all(d in table for d in blind))
        self.assertTrue(all(v["cls"] in C.TABLE_STATUSES for v in table.values()))


if __name__ == "__main__":
    unittest.main()
