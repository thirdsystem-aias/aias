#!/usr/bin/env python3
"""Tests for pull_arm_a.py: every spending limit and check of pre-registration section 5.4, with a fake transport.
No request leaves the machine; no key is used; nothing is billed. unittest (pytest collects it too)."""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
import params_arm_a as P            # noqa: E402
import pull_arm_a as PL             # noqa: E402
import simulate_google_arm_a as SIM  # noqa: E402

DAY1 = date(2026, 12, 1)
PRICE = (0.12, 0.0012)


class Sandbox(unittest.TestCase):
    """Each test runs with RAW, ROOT and ANCHOR inside a temporary folder."""

    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.tmp = Path(self.td.name)
        self.saved = (P.ROOT, P.RAW, P.ANCHOR)
        P.ROOT, P.RAW, P.ANCHOR = self.tmp, self.tmp / "raw", self.tmp / "anchor.json"
        P.ANCHOR.write_text("{}")
        self.template = SIM.load_template()
        self.domains = PL.load_domains()
        self.sleeps = []
        t = [datetime(2026, 12, 1, 15, 0, tzinfo=timezone.utc)]

        def now():
            t[0] += timedelta(seconds=1)
            return t[0]
        self.now = now

    def tearDown(self):
        P.ROOT, P.RAW, P.ANCHOR = self.saved
        self.td.cleanup()

    def fake(self, cost=None, status=None, months_drop=(), raise_on=()):
        """Transport answering in the real response shape; per-call overrides by call number (1-based)."""
        calls = {"n": 0}

        def post(body):
            calls["n"] += 1
            k = calls["n"]
            if k in raise_on:
                raise TimeoutError("simulated timeout")
            t = body[0]
            y, m = self.day.year, self.day.month
            months = SIM.month_list(t["date_from"], y, m)
            etv = {ym: 1000.0 for ym in months}
            c = cost(k) if callable(cost) else None
            s = status(k) if callable(status) else "Ok."
            drop = months_drop(k) if callable(months_drop) else ()
            r = SIM.response(t["target"], t["date_from"], y, m, etv, self.template, seed=k, cost=c, status_message=s,
                             drop_months=drop)
            return 200, json.dumps(r).encode()
        post.calls = calls
        return post

    def run_pull(self, post, domains=None, pull=1, day=DAY1, price=PRICE, ps=()):
        self.day = day
        return PL.run_pull(pull, day, post, price, sleep=self.sleeps.append, now=self.now,
                           domains=self.domains if domains is None else domains, ps_lines=list(ps))


class TestPlan(unittest.TestCase):
    def test_section_5_2_arithmetic(self):
        p1 = PL.plan(1, date(2026, 12, 1))
        self.assertEqual(P.PULLS[1]["planned"], "2026-12-01")          # r5: Tue 2026-12-01 (was Mon 2026-12-07)
        self.assertEqual(P.PULLS[1]["latest"], "2026-12-31")
        self.assertEqual((P.PULLS[2]["planned"], P.PULLS[3]["planned"]), ("2027-01-04", "2027-03-01"))
        p2 = PL.plan(2, date(2027, 1, 4))
        p3 = PL.plan(3, date(2027, 3, 1))
        self.assertEqual((p1["months"], p2["months"], p3["months"]), (26, 3, 29))
        self.assertAlmostEqual(p1["expected"], 11.4912, places=6)
        self.assertAlmostEqual(p2["expected"], 9.3936, places=6)
        self.assertAlmostEqual(p3["expected"], 11.7648, places=6)
        self.assertAlmostEqual(p1["expected"] + p2["expected"] + p3["expected"], 32.6496, places=6)

    def test_modes_and_fallbacks(self):
        full2 = 76 * PL.request_cost(PL.months_inclusive("2024-11-01", date(2027, 1, 4)))
        inc3 = 76 * PL.request_cost(PL.months_inclusive("2026-12-01", date(2027, 3, 1)))
        self.assertAlmostEqual(full2, 11.5824, places=6)          # 27 months (draft: $11.58)
        self.assertAlmostEqual(inc3, 9.4848, places=6)            # 4 months (draft: $9.48)
        self.assertAlmostEqual(11.4912 + full2 + 11.7648, 34.8384, places=6)   # mode A $34.84
        self.assertAlmostEqual(11.4912 + 9.3936 + inc3, 30.3696, places=6)     # mode B $30.37
        p3late = PL.plan(3, date(2027, 4, 5))
        self.assertEqual(p3late["months"], 30)
        self.assertAlmostEqual(p3late["expected"], 11.856, places=6)            # draft: $11.86
        self.assertAlmostEqual(11.4912 + 9.3936 + p3late["expected"], 32.7408, places=6)   # draft: $32.74
        self.assertAlmostEqual(80 * (0.1512 + 0.1236 + 0.1548), 34.368, places=6)          # draft: $34.37
        self.assertLess(34.8384 + 9.4848, P.HARD_STOP)                                     # D10: $44.32

    def test_limits_match_text(self):
        self.assertEqual((P.PER_PULL_LIMIT, P.HARD_STOP, P.FIRST_COST_TOL, P.MAX_REQUEST_COST, P.RETRY_WAIT_S,
                          P.MAX_RETRIES), (13.00, 48.00, 0.005, 0.20, 60, 1))
        self.assertEqual((P.PRICE_PER_REQUEST, P.PRICE_PER_MONTH), (0.12, 0.0012))

    def test_domains_in_pull_order(self):
        d = PL.load_domains()
        self.assertEqual(len(d), 76)
        cats = [r["category"] for r in d[:72]]
        order = ["cars", "airlines", "banks", "software", "spirits"]
        self.assertEqual(cats, sorted(cats, key=order.index))
        self.assertEqual([r["domain"] for r in d[72:]], ["mbusa.com", "bmwusa.com", "jaguarusa.com", "marcus.com"])

    def test_parse_price(self):
        html = '<div class="p">Historical Rank Overview</div><span>$0.12</span> + <b>$0.0012</b> per month'
        self.assertEqual(PL.parse_price(html), (0.12, 0.0012))
        self.assertIsNone(PL.parse_price("<html>no price here</html>"))
        self.assertEqual(PL.parse_price("$0.13 + $0.0012"), (0.13, 0.0012))

    def test_plan_cli_sends_nothing(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), mock.patch.object(PL, "live_post", side_effect=AssertionError):
            self.assertEqual(PL.main(["--pull", "1", "--plan"]), 0)
        self.assertIn('"months": 26', buf.getvalue())


class TestRefusals(Sandbox):
    def assertRefused(self, fragment, **kw):
        post = self.fake()
        with self.assertRaises(PL.Refuse) as cm:
            self.run_pull(post, **kw)
        self.assertIn(fragment, str(cm.exception))
        self.assertEqual(post.calls["n"], 0)                    # nothing sent

    def test_no_anchor(self):
        P.ANCHOR.unlink()
        self.assertRefused("anchor")

    def test_price_differs(self):
        self.assertRefused("differs", price=(0.13, 0.0012))
        self.assertRefused("differs", price=(0.12, 0.0013))

    def test_price_unreadable(self):
        self.assertRefused("could not be read", price=None)

    def test_date_outside_window(self):
        self.assertRefused("outside", day=date(2026, 11, 30))
        self.assertRefused("outside", day=date(2027, 1, 1))

    def test_other_paid_collection(self):
        ps = ["4242 python3 osf/v46/scripts/acquire_v0_46.py --collect"]
        self.assertRefused("another paid collection", ps=ps, day=date(2026, 12, 2))   # pull 1, any day but Dec 1
        self.assertRefused("another paid collection", ps=ps, pull=2, day=date(2027, 1, 4))

    def test_dec_1_exception_pull_1_only(self):
        """Section 5.4 one-off exception: pull 1 on Tue 2026-12-01 may run beside another paid collection."""
        self.assertEqual(P.CONCURRENT_OK, {1: "2026-12-01"})
        ps = ["4242 python3 osf/v62/scripts/acquire_v0_62.py --collect"]
        pl = PL.preflight(1, date(2026, 12, 1), PRICE, ps_lines=ps)
        self.assertEqual(pl["months"], 26)
        self.assertEqual(pl["concurrent_paid_collections"], ps)

    def test_per_pull_limit_before_start(self):
        many = self.domains + [dict(self.domains[0], domain=f"x{i}.com") for i in range(10)]   # 86 x 0.1512 = 13.0032
        self.assertRefused("per-pull limit", domains=many)

    def test_hard_stop_before_start(self):
        PL.write_manifest(1, [{"pull": 1, "cost": 38.7, "outcome": "OK"}])        # 38.70 + 9.3936 = 48.09 > 48
        self.assertRefused("hard stop", pull=2, day=date(2027, 1, 4))

    def test_existing_manifest(self):
        PL.write_manifest(1, [{"pull": 1, "cost": 0.15, "outcome": "OK"}])
        self.assertRefused("already has a manifest")

    def test_hard_stop_allows_exact_fit(self):
        PL.write_manifest(1, [{"pull": 1, "cost": 38.6, "outcome": "OK"}])        # 38.60 + 9.3936 = 47.99
        s = self.run_pull(self.fake(), pull=2, day=date(2027, 1, 4))
        self.assertIsNone(s["stopped"])
        self.assertAlmostEqual(s["cumulative_spent"], 47.9936, places=6)


class TestPull(Sandbox):
    def test_full_pull_records_everything(self):
        s = self.run_pull(self.fake())
        self.assertIsNone(s["stopped"])
        self.assertEqual(s["requests"], 76)
        self.assertAlmostEqual(s["pull_spent"], 11.4912, places=6)
        rows = PL.read_manifest(1)
        self.assertEqual(len(rows), 76)
        self.assertEqual(set(PL.MANIFEST_COLS), set(rows[0]))
        for r in rows:
            raw = (P.ROOT / r["file"]).read_bytes()
            import hashlib
            self.assertEqual(hashlib.sha256(raw).hexdigest(), r["sha256"])
            self.assertEqual(r["months_returned"], "26")
            self.assertEqual(json.loads(r["request_body"])[0]["date_from"], "2024-11-01")
            self.assertEqual(json.loads(r["request_body"])[0]["location_code"], 2840)
            self.assertEqual(r["price_per_request"], "0.12")
        self.assertEqual(rows[0]["domain"], "mercedes-benz.com")
        self.assertTrue((P.RAW / "pull1" / "summary_pull1.json").exists())

    def test_request_body_has_no_other_parameter(self):
        seen = []
        post = self.fake()

        def spy(body):
            seen.append(body)
            return post(body)
        self.run_pull(spy, domains=self.domains[:2])
        self.assertEqual(set(seen[0][0]), {"target", "location_code", "language_code", "date_from"})
        self.assertEqual(seen[0][0]["language_code"], "en")

    def test_one_retry_after_60s_cost_counts(self):
        s = self.run_pull(self.fake(status=lambda k: "Internal Error." if k == 2 else "Ok."), domains=self.domains[:3])
        self.assertEqual(self.sleeps, [60])
        rows = PL.read_manifest(1)
        self.assertEqual([r["outcome"] for r in rows], ["OK", "FAILED", "OK", "OK"])
        self.assertEqual(rows[1]["domain"], rows[2]["domain"])
        self.assertAlmostEqual(s["pull_spent"], 4 * 0.1512, places=6)

    def test_fail_twice_is_pull_failed_and_pull_continues(self):
        s = self.run_pull(self.fake(status=lambda k: "Internal Error." if k in (2, 3) else "Ok."),
                          domains=self.domains[:3])
        rows = PL.read_manifest(1)
        self.assertEqual([r["outcome"] for r in rows], ["OK", "FAILED", "PULL_FAILED", "OK"])
        self.assertEqual(s["pull_failed"], [self.domains[1]["domain"]])
        self.assertIsNone(s["stopped"])

    def test_no_items_is_a_failure(self):
        allm = SIM.month_list("2024-11-01", 2026, 12)
        s = self.run_pull(self.fake(months_drop=lambda k: allm if k == 2 else ()), domains=self.domains[:2])
        self.assertEqual([r["outcome"] for r in PL.read_manifest(1)], ["OK", "FAILED", "OK"])

    def test_transport_error_retried_and_counted_at_expected(self):
        s = self.run_pull(self.fake(raise_on=(1,)), domains=self.domains[:1])
        rows = PL.read_manifest(1)
        self.assertEqual([r["outcome"] for r in rows], ["FAILED", "OK"])
        self.assertAlmostEqual(float(rows[0]["cost"]), 0.1512, places=6)

    def test_first_request_cost_off_stops(self):
        s = self.run_pull(self.fake(cost=lambda k: 0.1512 + 0.0051 if k == 1 else None))
        self.assertIn("first request cost", s["stopped"])
        self.assertEqual(s["requests"], 1)

    def test_first_request_cost_within_tolerance_continues(self):
        s = self.run_pull(self.fake(cost=lambda k: 0.1512 + 0.0049 if k == 1 else None), domains=self.domains[:3])
        self.assertIsNone(s["stopped"])

    def test_first_request_months_off_stops(self):
        s = self.run_pull(self.fake(months_drop=lambda k: [(2024, 11)] if k == 1 else ()))
        self.assertIn("months", s["stopped"])
        self.assertEqual(s["requests"], 1)

    def test_later_months_difference_recorded_not_stopped(self):
        s = self.run_pull(self.fake(months_drop=lambda k: [(2024, 11)] if k == 2 else ()), domains=self.domains[:3])
        self.assertIsNone(s["stopped"])
        self.assertEqual(PL.read_manifest(1)[1]["outcome"], "OK_MONTHS_DIFFER")

    def test_request_above_020_stops(self):
        s = self.run_pull(self.fake(cost=lambda k: 0.2001 if k == 3 else None))
        self.assertIn("> $0.20", s["stopped"])
        self.assertEqual(s["requests"], 3)

    def test_per_pull_limit_checked_before_every_request(self):
        s = self.run_pull(self.fake(cost=lambda k: 0.1512 if k == 1 else 0.19))
        self.assertIn("per-pull limit", s["stopped"])
        self.assertLessEqual(s["pull_spent"], P.PER_PULL_LIMIT)
        self.assertEqual(s["requests"], 68)                    # 0.1512 + 67 x 0.19 = 12.8812; next would pass 13

    def test_hard_stop_checked_before_every_request(self):
        PL.write_manifest(1, [{"pull": 1, "cost": 38.5, "outcome": "OK"}])
        s = self.run_pull(self.fake(cost=lambda k: 0.1236 if k == 1 else 0.19), pull=2, day=date(2027, 1, 4))
        self.assertIn("hard stop", s["stopped"])
        self.assertLessEqual(s["cumulative_spent"], P.HARD_STOP)

    def test_raw_never_overwritten(self):
        f = P.RAW / "pull1"
        f.mkdir(parents=True)
        when = datetime(2026, 12, 1, 15, 0, 1, tzinfo=timezone.utc)
        a, _ = PL.save_raw(f, "x.com", when, b"one")
        b, _ = PL.save_raw(f, "x.com", when, b"two")
        self.assertNotEqual(a, b)
        self.assertEqual(a.read_bytes(), b"one")

    def test_key_only_in_header_never_written(self):
        captured = {}

        class Resp:
            status = 200

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def read(self):
                return b"{}"

        def fake_urlopen(req, timeout=0):
            captured["auth"] = req.get_header("Authorization")
            captured["body"] = req.data
            return Resp()
        with mock.patch.dict(os.environ, {"DATAFORSEO_LOGIN": "SENTINEL_LOGIN", "DATAFORSEO_PASSWORD": "SENTINEL_PW"}), \
                mock.patch.object(PL.urllib.request, "urlopen", fake_urlopen):
            PL.live_post([{"target": "x.com"}])
        self.assertTrue(captured["auth"].startswith("Basic "))
        self.assertNotIn(b"SENTINEL", captured["body"])
        src = (HERE.parent / "scripts" / "pull_arm_a.py").read_text()
        self.assertNotIn("SENTINEL", src)
        self.assertNotIn("write_text(os.environ", src)


if __name__ == "__main__":
    unittest.main()
