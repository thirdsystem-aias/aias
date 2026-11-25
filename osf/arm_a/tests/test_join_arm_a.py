#!/usr/bin/env python3
"""Tests for join_arm_a.py and simulate_google_arm_a.py on simulated Google data only (section 6.3)."""
import json
import math
import sys
import tempfile
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
import join_arm_a as J              # noqa: E402
import params_arm_a as P            # noqa: E402
import pull_arm_a as PL             # noqa: E402
import simulate_google_arm_a as SIM  # noqa: E402


def keyshape(o):
    if isinstance(o, dict):
        return {k: keyshape(v) for k, v in o.items()}
    if isinstance(o, list):
        return [keyshape(o[0])] if o else []
    return type(o).__name__ if o is not None else "null"


class TestSimulatedShape(unittest.TestCase):
    def test_same_keys_and_nesting_as_the_real_response(self):
        real = SIM.load_template()
        sim = SIM.response("example-sim.com", "2024-11-01", 2026, 12, {}, real, seed=1)
        a, b = keyshape(real), keyshape(sim)
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))

    def test_items_newest_first_and_cost_formula(self):
        sim = SIM.response("example-sim.com", "2024-11-01", 2026, 12, {}, seed=1)
        items = sim["tasks"][0]["result"][0]["items"]
        self.assertEqual(len(items), 26)
        self.assertEqual((items[0]["year"], items[0]["month"]), (2026, 12))
        self.assertEqual((items[-1]["year"], items[-1]["month"]), (2024, 11))
        self.assertAlmostEqual(sim["cost"], 0.1512, places=6)
        self.assertEqual(sim["tasks"][0]["data"]["target"], "example-sim.com")

    def test_real_fixture_cost_matches_price(self):
        real = SIM.load_template()
        n = len(real["tasks"][0]["result"][0]["items"])
        self.assertEqual(n, 25)
        self.assertAlmostEqual(real["cost"], 0.12 + 0.0012 * n, places=6)


class PullSandbox(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.tmp = Path(self.td.name)
        self.saved = (P.ROOT, P.RAW, P.ANCHOR)
        P.ROOT, P.RAW, P.ANCHOR = self.tmp, self.tmp / "raw", self.tmp / "anchor.json"
        P.ANCHOR.write_text("{}")

    def tearDown(self):
        P.ROOT, P.RAW, P.ANCHOR = self.saved
        self.td.cleanup()

    def pull(self, etv_fn, domains, status=lambda d, k: "Ok.", pull=1, day=date(2026, 12, 7)):
        tpl = SIM.load_template()
        t = [datetime(day.year, day.month, day.day, 15, tzinfo=timezone.utc)]
        n = {"k": 0}

        def now():
            t[0] += timedelta(seconds=1)
            return t[0]

        def post(body):
            n["k"] += 1
            d = body[0]["target"]
            months = SIM.month_list(body[0]["date_from"], day.year, day.month)
            r = SIM.response(d, body[0]["date_from"], day.year, day.month, {ym: etv_fn(d, ym) for ym in months}, tpl,
                             seed=n["k"], status_message=status(d, n["k"]))
            return 200, json.dumps(r).encode()
        rows = [{"brand_id": f"B{i}", "domain": d, "category": "x", "pull_order": i + 1} for i, d in enumerate(domains)]
        PL.run_pull(pull, day, post, (0.12, 0.0012), sleep=lambda s: None, now=now, domains=rows, ps_lines=[])
        return J.load_pull(pull, raw_root=P.RAW, root=P.ROOT)


class TestLoadPull(PullSandbox):
    def test_pull_month_dropped_and_measures(self):
        panel, status, pm = self.pull(lambda d, ym: 99.0, ["a.com", "b.com"])
        self.assertEqual(pm, (2026, 12))
        self.assertNotIn((2026, 12), panel["a.com"])
        self.assertEqual(len(panel["a.com"]), 25)                     # Nov 2024 .. Nov 2026 complete
        v = panel["a.com"][(2026, 11)]
        self.assertAlmostEqual(v["g"], math.log1p(99.0))
        self.assertEqual(status, {"a.com": "OK", "b.com": "OK"})

    def test_sha_mismatch_refused(self):
        self.pull(lambda d, ym: 5.0, ["a.com"])
        row = J.read_manifest(P.RAW / "pull1" / "manifest_pull1.csv")[0]
        (P.ROOT / row["file"]).write_bytes(b"{}")
        with self.assertRaises(ValueError):
            J.load_pull(1, raw_root=P.RAW, root=P.ROOT)

    def test_pull_failed_has_no_series(self):
        panel, status, _ = self.pull(lambda d, ym: 5.0, ["a.com", "b.com"],
                                     status=lambda d, k: "Internal Error." if d == "b.com" else "Ok.")
        self.assertEqual(status["b.com"], "PULL_FAILED")
        self.assertNotIn("b.com", panel)


def mk(series):
    return {ym: {"etv": v, "g": math.log1p(v), "count": 0.0, "top10": 0.0} for ym, v in series.items()}


class TestRules(unittest.TestCase):
    def test_break_by_median(self):
        months = SIM.month_list("2025-01-01", 2025, 6)
        panel = {f"d{i}": mk({ym: (100.0 if ym < (2025, 4) else 200.0) * (1 + 0.01 * i) for ym in months})
                 for i in range(10)}
        fl = J.break_flags(panel)
        self.assertTrue(fl[(2025, 4)]["flagged"])                    # median dg = ln 2 > 0.40
        self.assertFalse(fl[(2025, 5)]["flagged"])

    def test_break_by_share_moving(self):
        months = [(2025, 1), (2025, 2)]
        panel = {}
        for i in range(10):                                          # 8 of 10 up by 0.3, 2 down by 0.5: median 0.3
            f = math.exp(0.3) if i < 8 else math.exp(-0.5)
            panel[f"d{i}"] = mk({(2025, 1): 1000.0, (2025, 2): 1000.0 * f})
        fl = J.break_flags(panel)
        self.assertLess(abs(fl[(2025, 2)]["median_dg"]), 0.40)
        self.assertTrue(fl[(2025, 2)]["flagged"])
        panel["d7"] = mk({(2025, 1): 1000.0, (2025, 2): 1000.0})     # now 7 of 10 move up: not flagged
        self.assertFalse(J.break_flags(panel)[(2025, 2)]["flagged"])

    def test_window_two_of_three(self):
        s = mk({(2026, 3): 10.0, (2026, 5): 30.0})
        self.assertAlmostEqual(J.window_mean(s, (2026, 5)), (math.log1p(10) + math.log1p(30)) / 2)
        self.assertIsNone(J.window_mean(mk({(2026, 5): 30.0}), (2026, 5)))
        self.assertEqual(J.window((2026, 1)), [(2025, 11), (2025, 12), (2026, 1)])

    def test_window_with_flagged_months_dropped(self):
        s = mk({ym: 1.0 for ym in SIM.month_list("2026-01-01", 2026, 5)})
        months = J.window_months(sorted(s), (2026, 5), flagged=frozenset({(2026, 4)}))
        self.assertEqual(months, [(2026, 2), (2026, 3), (2026, 5)])

    def test_usable_half_rule(self):
        w = [J.window((2026, 5)), J.window((2026, 11))]                # 6 months
        s = mk({(2026, 3): 1, (2026, 4): 0, (2026, 5): 0, (2026, 9): 1, (2026, 10): 1})
        self.assertTrue(J.usable(s, w))                                  # 3 bad of 6: not more than half
        del s[(2026, 10)]
        self.assertFalse(J.usable(s, w))                                 # 4 bad of 6

    def test_brand_domains_and_shared_domains(self):
        rows = J.load_domains()
        prim = J.brand_domains(rows)
        sens = J.brand_domains(rows, "sensitivity")
        self.assertEqual(len(prim), 72)
        self.assertEqual(prim["BR-00370"], ("cars", "mbusa.com"))
        self.assertEqual(sens["BR-00370"], ("cars", "mercedes-benz.com"))
        self.assertEqual(prim["BR-00470"], ("banks", "marcus.com"))
        self.assertEqual(sens["BR-00463"], ("banks", "chase.com"))
        dup = rows + [dict(rows[0], brand_id="BR-X", role="primary", domain="cadillac.com")]
        out = J.brand_domains(dup)
        self.assertNotIn("BR-X", out)
        self.assertNotIn("BR-00372", out)                                # Cadillac shares cadillac.com: both out

    def test_demeaning(self):
        out = J.demeaned_change({"a": 1.0, "b": 2.0, "c": 4.0, "d": None}, {"a": "x", "b": "x", "c": "x", "d": "x"})
        self.assertEqual(out, {"a": -1.0, "b": 0.0, "c": 2.0, "d": None})

    def test_restatement(self):
        a = {"d": mk({(2025, 1): 100.0, (2025, 2): 100.0, (2025, 3): 100.0, (2025, 4): 100.0, (2025, 5): 100.0})}
        b = {"d": mk({(2025, 1): 100.5, (2025, 2): 105.0, (2025, 3): 120.0, (2025, 4): 100.0, (2025, 5): 100.0})}
        r = J.restatement(a, b)
        self.assertEqual(r["domain_months"], 5)
        self.assertAlmostEqual(r["share_gt_1pct"], 2 / 5)
        self.assertAlmostEqual(r["share_gt_10pct"], 1 / 5)
        self.assertFalse(r["rerun_on_pull3"])                            # 20% is not more than 20%


if __name__ == "__main__":
    unittest.main()
