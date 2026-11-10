#!/usr/bin/env python3
"""
Tests for acquire_v0_44.py, budget_v0_44.py and cost_estimate_v0_44.py. Every provider client is a local fake: no
request leaves the machine, nothing is billed. unittest classes (pytest collects them too).
"""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace as NS
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import acquire_v0_44 as AQ          # noqa: E402
import budget_v0_44 as BG           # noqa: E402
import cost_estimate_v0_44 as CE    # noqa: E402

V42_ACQ = AQ.ROOT / "osf/v42/scripts/acquire_v0_42.py"
FABLE, GPT, GEM = AQ.PANEL


def spec(model=FABLE, run=1, phase="B", pid="INS_B_q", i=0):
    return {"call_id": f"INS|{phase}|{pid}{i}|{model['model_id']}|S0|{run}", "substrate": "INS", "phase": phase,
            "probe_id": f"{pid}{i}", "brand_id": None, "frame_id": "q1", "model": model, "condition": "S0",
            "run": run, "block": 0, "system": None, "prompt": f"What are the best car insurance companies? {i}"}


def message(text="State Farm and GEICO.", stop="end_turn", tin=1000, tout=200, model="claude-fable-5-2"):
    return NS(content=[NS(type="text", text=text, citations=None)], stop_reason=stop, model=model,
              usage=NS(input_tokens=tin, output_tokens=tout))


class FakeBatches:
    def __init__(self, script):
        self.script, self.created, self.n = script, [], 0

    def create(self, requests):
        self.n += 1
        self.created.append(requests)
        return NS(id=f"batch_{self.n}", processing_status="in_progress")

    def retrieve(self, bid):
        return NS(id=bid, processing_status="ended", ended_at="2026-11-24T16:00:00+00:00")

    def results(self, bid):
        reqs = self.created[int(bid.split("_")[1]) - 1]
        return [NS(custom_id=r["custom_id"], result=self.script(r["custom_id"], r["params"], self.n)) for r in reqs]


class FakeClient:
    def __init__(self, script):
        self.batches = FakeBatches(script)
        self.messages = self


def ok(msg):
    return NS(type="succeeded", message=msg)


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.raw = Path(self.tmp.name) / "raw.jsonl"
        self.state = Path(self.tmp.name) / "state.json"
        self.written = []
        AQ.DEADLINE_UTC = None

    def tearDown(self):
        AQ.DEADLINE_UTC = None
        self.tmp.cleanup()

    def ledger(self, **kw):
        return BG.Ledger(self.raw, self.state, **kw)

    def write(self, rec):
        self.written.append(rec)
        with open(self.raw, "a") as f:
            f.write(json.dumps(rec) + "\n")


class TestDesign(unittest.TestCase):
    def test_matrix_909_and_order(self):
        specs = AQ.build_specs(AQ.load_probes())
        self.assertEqual(len(specs), 909)
        self.assertEqual(AQ.expected_total(), 909)
        self.assertEqual([m["model_id"] for m in AQ.PANEL], ["claude-fable-5-2", "gpt-6-astra", "gemini-4-argon"])
        self.assertEqual({m["model_id"]: m["mode"] for m in AQ.PANEL},
                         {"claude-fable-5-2": "batch", "gpt-6-astra": "standard", "gemini-4-argon": "standard"})
        self.assertEqual({s["condition"] for s in specs}, {"S0"})
        a = [s for s in specs if s["phase"] == "A"]
        self.assertEqual((len(a), {s["run"] for s in a}), (477, {1}))
        b = [s for s in specs if s["phase"] == "B"]
        self.assertEqual((len(b), sorted({s["run"] for s in b})), (432, [1, 2, 3]))
        blocks = [s["block"] for s in specs]
        self.assertEqual(blocks, sorted(blocks))
        per_ind = {i: sum(1 for s in specs if s["substrate"] == i) for i in ("INS", "PHA", "FAS")}
        self.assertEqual(per_ind, {"INS": 3 * (18 + 23), "PHA": 3 * (18 + 16), "FAS": 3 * (18 + 24)})

    def test_model_ids_are_v042_r2_ids(self):
        txt = (AQ.ROOT / "osf/v42/prereg/PRE_REGISTRATION_v0_42.md").read_text(encoding="utf-8")
        for m in AQ.PANEL:
            self.assertIn(f"`{m['model_id']}`", txt)

    def test_drop_run3_and_counts_from_industry_list(self):
        self.assertEqual(len(AQ.build_specs(AQ.load_probes(), drop_run3=True)), 765)
        self.assertEqual(AQ.expected_counts(), (48, 159))
        seven = [i for i in AQ.load_industries() if i["industry"] != "PHA"]
        self.assertEqual(AQ.expected_counts(seven), (42, 143))

    def test_probe_file_must_match_industry_list(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "probes.jsonl"
            lines = AQ.PROBES_PATH.read_text(encoding="utf-8").splitlines()[:-1]
            p.write_text("\n".join(lines) + "\n", encoding="utf-8")
            with self.assertRaises(SystemExit):
                AQ.load_probes(p)

    def test_no_sampling_params_cap_and_tag(self):
        self.assertEqual(AQ.confirm_no_sampling_params(), [])
        self.assertEqual(AQ.CURRENT_MAX_TOKENS, 16384)
        self.assertEqual(BG.OUTPUT_CAP, 16384)
        self.assertEqual(AQ.PREREG_TAG, "v0.44-prereg-r1")
        self.assertEqual(AQ.anthropic_params(spec()), {"model": "claude-fable-5-2", "max_tokens": 16384,
                                                       "messages": [{"role": "user", "content": spec()["prompt"]}]})

    def test_copied_block_is_byte_identical_to_v042(self):
        v42 = V42_ACQ.read_text(encoding="utf-8")
        mine = (HERE.parent / "acquire_v0_44.py").read_text(encoding="utf-8")
        a, b = v42.index("class Transient"), v42.index("# ======================= v0.42 wrapper")
        self.assertIn(v42[a:b].rstrip("\n") + "\n", mine)
        c, d = v42.index("# S1 tool configurations"), v42.index("MAX_ATTEMPTS = 3")
        self.assertIn(v42[c:d], mine)

    def test_batch_params_equal_sync_call_kwargs(self):
        s = spec()
        captured = {}

        class Cl:
            def __init__(self):
                self.messages = self

            def create(self, **kw):
                captured.update(kw)
                return message()
        with mock.patch("anthropic.Anthropic", return_value=Cl()):
            AQ.call_anthropic_current(s["model"]["model_id"], s["prompt"], False, None)
        self.assertEqual(AQ.anthropic_params(s), captured)

    def test_default_mode_is_dry_run_and_sends_nothing(self):
        def boom(*a, **k):
            raise AssertionError("a provider call was attempted")
        buf = io.StringIO()
        with mock.patch.dict(AQ.CURRENT_DISPATCH, {"anthropic": boom, "openai": boom, "google": boom}), \
                mock.patch.object(AQ, "run_anthropic_batch", boom), mock.patch.object(AQ, "run_sync", boom), \
                mock.patch.object(AQ, "_ps", return_value=""), contextlib.redirect_stdout(buf):
            rc = AQ.main([])
        self.assertEqual(rc, 0)
        self.assertIn("TOTAL calls: 909 (expected 909) -> OK", buf.getvalue())
        self.assertIn("nothing sent.", buf.getvalue())

    def test_approvals_need_collect(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            AQ.main(["--approve-past-80", "x"])


class TestGuards(Base):
    def test_collect_refused_without_anchor_before_any_network(self):
        with mock.patch.object(AQ, "ANCHOR_PATH", Path(self.tmp.name) / "missing.json"), \
                mock.patch.object(AQ.subprocess, "run", side_effect=AssertionError("git called")):
            with self.assertRaises(SystemExit) as cm:
                AQ.prereg_guard()
        self.assertIn("anchor file missing", str(cm.exception))
        with mock.patch.object(AQ, "ANCHOR_PATH", Path(self.tmp.name) / "missing.json"), \
                mock.patch.object(AQ, "require_keys", side_effect=AssertionError("keys read")):
            with self.assertRaises(SystemExit):
                AQ.collect()

    def test_collect_refused_without_tag_or_wrong_commit(self):
        anchor = Path(self.tmp.name) / "anchor.json"
        anchor.write_text(json.dumps({"commit": "abc123"}))
        with mock.patch.object(AQ, "ANCHOR_PATH", anchor):
            with mock.patch.object(AQ.subprocess, "run", return_value=NS(returncode=0, stdout="", stderr="")):
                with self.assertRaises(SystemExit):
                    AQ.prereg_guard()
            out = "deadbeef\trefs/tags/v0.44-prereg-r1\n"
            with mock.patch.object(AQ.subprocess, "run", return_value=NS(returncode=0, stdout=out, stderr="")):
                with self.assertRaises(SystemExit):
                    AQ.prereg_guard()
            out = "abc123\trefs/tags/v0.44-prereg-r1\n"
            with mock.patch.object(AQ.subprocess, "run", return_value=NS(returncode=0, stdout=out, stderr="")):
                self.assertEqual(AQ.prereg_guard(), "abc123")

    def test_window_bounds_and_checks(self):
        s, e = AQ.window_bounds()
        self.assertEqual(s.isoformat(), "2026-11-24T06:00:00+00:00")       # midnight US Central (CST, UTC-6)
        self.assertEqual(e.isoformat(), "2026-11-29T06:00:00+00:00")
        no_raw = Path(self.tmp.name) / "none.jsonl"
        self.assertFalse(AQ.window_check(datetime(2026, 11, 24, 5, 59, tzinfo=timezone.utc), raw_path=no_raw)[0])
        self.assertTrue(AQ.window_check(datetime(2026, 11, 24, 6, 0, tzinfo=timezone.utc), raw_path=no_raw)[0])
        self.assertFalse(AQ.window_check(datetime(2026, 11, 29, 6, 0, tzinfo=timezone.utc), raw_path=no_raw)[0])
        self.assertFalse(AQ.window_check(datetime(2026, 11, 10, 19, 0, tzinfo=timezone.utc), raw_path=no_raw)[0])

    def test_72_hour_deadline_from_first_call(self):
        self.write({"call_id": "x", "started_utc": "2026-11-24T12:00:00+00:00"})
        self.assertEqual(AQ.deadline(raw_path=self.raw).isoformat(), "2026-11-27T12:00:00+00:00")
        self.assertFalse(AQ.window_check(datetime(2026, 11, 27, 12, 0, tzinfo=timezone.utc), raw_path=self.raw)[0])
        self.assertTrue(AQ.window_check(datetime(2026, 11, 27, 11, 59, tzinfo=timezone.utc), raw_path=self.raw)[0])

    def test_declared_window_needs_a_deviations_entry(self):
        dev = Path(self.tmp.name) / "DEVIATIONS.md"
        dev.write_text("# log\n\n## Entry 0 - COI\ntext\n\n## Entry 1 - window moved\nNew window 2026-12-01 to "
                       "2026-12-04 because v0.40 overran.\n", encoding="utf-8")
        self.assertEqual(AQ.declared_window("2026-12-01", "2026-12-04", "1", dev), ("2026-12-01", "2026-12-04"))
        for args in (("2026-12-01", "2026-12-05", "1"), ("2026-12-01", "2026-12-04", "2")):
            with self.assertRaises(SystemExit):
                AQ.declared_window(*args, deviations_path=dev)

    def test_other_collections_detected_ancestors_ignored(self):
        ps = ("  1     0 /sbin/launchd\n"
              "100     1 zsh -ic nohup caffeinate -i python3 osf/v44/scripts/acquire_v0_44.py --collect\n"
              "101   100 caffeinate -i python3 osf/v44/scripts/acquire_v0_44.py --collect\n"
              "102   101 python3 osf/v44/scripts/acquire_v0_44.py --collect\n"
              "200     1 python3 osf/v40/scripts/acquire_v0_40.py --collect\n"
              "300     1 python3 osf/v42/scripts/acquire_v0_42.py --dry-run\n"
              "400     1 python3 scripts/run_acquisition_v22.py\n"
              "500     1 vim acquire_notes.txt\n")
        hits = AQ.other_collections(ps, me=102)
        self.assertEqual(sorted(p for p, _ in hits), [200, 400])
        self.assertEqual(AQ.other_collections("", me=1), [])

    def test_record_window_into_state(self):
        st = AQ.record_window(("2026-11-24", "2026-11-28"), None, self.state)
        self.assertEqual(json.loads(self.state.read_text())["window"], ["2026-11-24", "2026-11-28"])
        self.assertIsNone(st["window_deviation_entry"])


class TestBatchPath(Base):
    def test_happy_path_costs_at_batch_prices(self):
        client = FakeClient(lambda cid, p, n: ok(message()))
        L = self.ledger()
        st = AQ.run_anthropic_batch([spec(i=i) for i in range(3)], L, self.write, client=client, poll=0,
                                    sleep=lambda s: None)
        self.assertEqual(st, "done")
        r = self.written[0]
        self.assertEqual((r["status"], r["mode"], r["attempts"], r["batch_id"]), ("ok", "batch", 1, "batch_1"))
        want = (1000 * 4 + 200 * 20) / 1e6
        self.assertAlmostEqual(r["cost_usd"], want, places=12)
        self.assertAlmostEqual(L.actual, 3 * want, places=12)
        self.assertEqual(L.reserved, {})
        for req in client.batches.created[0]:
            self.assertRegex(req["custom_id"], r"^v44-[0-9]{4}-a1$")
            self.assertNotIn("tools", req["params"])

    def test_empty_resent_once_transient_retried_invalid_not(self):
        def script(cid, params, n):
            i = int(params["messages"][0]["content"].split()[-1])
            if i == 0:
                return ok(message(text=""))
            if i == 1:
                if n < 3:
                    return NS(type="errored", error=NS(type="error", error=NS(type="overloaded_error")))
                return ok(message(text="fine"))
            if i == 2:
                return NS(type="errored", error=NS(type="error", error=NS(type="invalid_request_error")))
            return NS(type="expired")
        st = AQ.run_anthropic_batch([spec(i=i) for i in range(4)], self.ledger(), self.write,
                                    client=FakeClient(script), poll=0, sleep=lambda s: None)
        self.assertEqual(st, "done")
        by = {}
        for r in self.written:
            by.setdefault(r["probe_id"], []).append(r)
        self.assertEqual([r["status"] for r in by["INS_B_q0"]], ["empty", "empty"])
        self.assertEqual([r["status"] for r in by["INS_B_q1"]], ["error", "error", "ok"])
        self.assertEqual([r["status"] for r in by["INS_B_q2"]], ["error"])
        self.assertEqual(len(by["INS_B_q3"]), AQ.MAX_ATTEMPTS)
        self.assertEqual(AQ.done_ids(self.raw), {by["INS_B_q1"][0]["call_id"]})

    def test_batch_is_split_to_fit_under_the_cap(self):
        client = FakeClient(lambda cid, p, n: ok(message()))
        per = BG.worst_case("claude-fable-5-2", "S0", "batch")
        L = self.ledger(cap=2.5 * per, pause_at=1000)
        st = AQ.run_anthropic_batch([spec(i=i) for i in range(5)], L, self.write, client=client, poll=0,
                                    sleep=lambda s: None)
        self.assertEqual(st, "done")
        self.assertEqual(len(client.batches.created[0]), 2)
        self.assertEqual(len(self.written), 5)
        self.assertLessEqual(L.spent(), L.cap)

    def test_deadline_stops_batches(self):
        AQ.DEADLINE_UTC = datetime(2000, 1, 1, tzinfo=timezone.utc)
        client = FakeClient(lambda cid, p, n: ok(message()))
        self.assertEqual(AQ.run_anthropic_batch([spec()], self.ledger(), self.write, client=client, poll=0,
                                                sleep=lambda s: None), "stop")
        self.assertEqual(client.batches.created, [])


class TestSyncPath(Base):
    def test_send_call_bills_the_empty_first_answer(self):
        empty = {"text": "", "served_model": "gpt-6-astra", "finish_reason": "completed", "tokens_in": 10,
                 "tokens_out": 5, "tokens_thought": 2, "paused_continued": False, "search": None}
        full = dict(empty, text="Yes.", tokens_in=11, tokens_out=6)
        with mock.patch.object(AQ, "_invoke", side_effect=[(empty, 1, None), (full, 1, None)]), \
                mock.patch.object(AQ.time, "sleep"):
            r = AQ.send_call(spec(model=GPT))
        self.assertEqual((r["status"], r["attempts"], r["empty_retry"]), ("ok", 2, True))
        self.assertAlmostEqual(r["cost_usd"], ((10 + 11) * 10 + (5 + 6) * 50) / 1e6, places=12)

    def test_run_sync_stops_before_the_cap_and_at_deadline(self):
        per = BG.worst_case("gpt-6-astra", "S0")
        L = self.ledger(cap=3.5 * per, pause_at=1000)

        def sender(s):
            return {"call_id": s["call_id"], "cost_usd": per, "condition": "S0", "status": "ok"}
        st = AQ.run_sync([spec(model=GPT, i=i) for i in range(10)], L, self.write, sender=sender, sleep=lambda s: None)
        self.assertEqual((st, len(self.written)), ("stop", 3))
        AQ.DEADLINE_UTC = datetime(2000, 1, 1, tzinfo=timezone.utc)
        self.assertEqual(AQ.run_sync([spec(model=GPT)], self.ledger(), self.write, sender=sender), "stop")


class TestLedger(Base):
    def test_pause_at_80_and_approvals(self):
        rec = {"model_requested": "gpt-6-astra", "condition": "S0", "started_utc": "2026-11-24T18:00:00+00:00",
               "usage_parts": [{"mode": "standard", "input_tokens": 0, "output_tokens": 1_600_000, "n_searches": 0}]}
        self.write(rec)                                    # $80.00 of output, no judge reserve in v0.44
        L = self.ledger()
        self.assertAlmostEqual(L.spent(), 80.0)
        self.assertEqual(L.reserve(0.01)[0], "pause")
        L2 = self.ledger()
        L2.approve("past_80", "test approval")
        self.assertEqual(L2.reserve(0.01)[0], "ok")
        L2.approve("drop_run3", "drop")
        self.assertTrue(L2.approved("drop_run3"))
        with self.assertRaises(ValueError):
            L2.approve("anything", "x")

    def test_hard_stop(self):
        L = self.ledger(cap=10.0, pause_at=1000)
        st, t1 = L.reserve(6.0)
        self.assertEqual(L.reserve(6.0)[0], "wait")
        L.settle(t1, 5.0)
        self.assertEqual(L.reserve(6.0)[0], "stop")

    def test_prices_november_december(self):
        rec = {"model_requested": "gemini-4-argon", "condition": "S0", "started_utc": "2026-11-30T23:00:00+00:00",
               "usage_parts": [{"mode": "standard", "input_tokens": 1000, "output_tokens": 100, "thinking_tokens": 50}]}
        self.assertAlmostEqual(BG.record_cost(rec), (1000 * 2 + 150 * 10) / 1e6, places=12)
        rec["started_utc"] = "2026-12-01T00:00:00+00:00"
        self.assertAlmostEqual(BG.record_cost(rec), (1000 * 4 + 150 * 20) / 1e6, places=12)
        self.assertEqual(BG.prices("claude-fable-5-2", "batch"), (4.0, 20.0))
        self.assertEqual(BG.prices("gpt-6-astra", "standard"), (10.0, 50.0))
        self.assertEqual(BG.JUDGE_RESERVE_USD, 0.0)


class TestCollectionFlow(Base):
    def _specs(self, **kw):
        return AQ.build_specs(AQ.load_probes(), **kw)

    def _runner(self, cost_of):
        def r(specs, ledger, write):
            for s in specs:
                st, tok = ledger.reserve(cost_of(s))
                if st != "ok":
                    return st
                rec = {"call_id": s["call_id"], "phase": s["phase"], "condition": s["condition"], "run": s["run"],
                       "model_requested": s["model"]["model_id"], "status": "ok", "text": "x", "error": None,
                       "output_tokens": 1, "finish_reason": "end_turn", "usage_parts": [], "cost_usd": cost_of(s)}
                write(rec)
                ledger.settle(tok, rec["cost_usd"])
            return "done"
        return r

    def test_projection_pause_then_drop_run3(self):
        # block 1: 144 x 0.13 = $18.72, x 4.59 > $80 -> pause; later calls cheap so the $80 pause is not reached
        cost = lambda s: 0.13 if (s["phase"], s["run"]) == ("B", 1) else 0.01
        ratio = AQ.projection_ratio()
        runners = {"batch": self._runner(cost), "standard": self._runner(cost)}
        with mock.patch.object(BG, "record_cost", side_effect=lambda r: r.get("cost_usd", 0.0)):
            L = self.ledger()
            st = AQ.run_collection(self._specs(), L, self.raw, runners, ratio, log=lambda *a: None)
            self.assertEqual(st, "pause")
            self.assertIn("projection", L.halt_reason)
            self.assertEqual(len(self.raw.read_text().splitlines()), 144)
            L2 = self.ledger()
            L2.approve("drop_run3", "pre-registrant: drop run 3")
            st2 = AQ.run_collection(self._specs(drop_run3=True), L2, self.raw, runners, ratio, log=lambda *a: None)
        self.assertEqual(st2, "done")
        recs = [json.loads(l) for l in self.raw.read_text().splitlines()]
        self.assertEqual(len(recs), 765)
        self.assertNotIn(3, {r["run"] for r in recs if r["phase"] == "B"})

    def test_no_projection_pause_at_central_estimate(self):
        cost = lambda s: 0.03
        L = self.ledger()
        runners = {"batch": self._runner(cost), "standard": self._runner(cost)}
        with mock.patch.object(BG, "record_cost", side_effect=lambda r: r.get("cost_usd", 0.0)):
            self.assertEqual(AQ.run_collection(self._specs(), L, self.raw, runners, AQ.projection_ratio(),
                                               log=lambda *a: None), "done")
        n = len(self.raw.read_text().splitlines())
        self.assertEqual(n, 909)
        self.assertEqual(AQ.run_collection(self._specs(), self.ledger(), self.raw, runners, 4.6, log=lambda *a: None),
                         "done")
        self.assertEqual(len(self.raw.read_text().splitlines()), n)          # resume: nothing re-sent

    def test_projection_ratio_by_date(self):
        ce = AQ.cost_estimate()
        self.assertAlmostEqual(AQ.projection_ratio(when_utc="2026-11-24T10:00:00+00:00"),
                               ce["designs"]["adopted"]["central"] / ce["designs"]["block1"]["central"])
        self.assertAlmostEqual(AQ.projection_ratio(when_utc="2026-12-02T10:00:00+00:00"),
                               ce["designs"]["adopted_december"]["central"] / ce["designs"]["block1_december"]["central"])


class TestCostEstimate(unittest.TestCase):
    def test_estimates_reproduce_and_fit(self):
        inds = list(__import__("csv").DictReader(open(AQ.INDUSTRIES_PATH, encoding="utf-8")))
        out = CE.build(inds, CE.per_call())
        d = out["designs"]
        self.assertEqual(d["adopted"]["calls"], 909)
        self.assertEqual((round(d["adopted"]["central"], 2), round(d["adopted"]["high"], 2)), (27.24, 52.44))
        self.assertEqual((round(d["adopted_december"]["central"], 2), round(d["adopted_december"]["high"], 2)),
                         (30.10, 59.00))
        self.assertLess(d["adopted_december"]["high"], BG.PAUSE_AT_USD)
        self.assertEqual(d["pharmacies_dropped"]["calls"], 807)
        self.assertEqual(sum(v["calls"] for v in out["by_industry"].values()), 909)
        locked = json.loads(AQ.COST_PATH.read_text(encoding="utf-8"))
        self.assertAlmostEqual(locked["designs"]["adopted"]["central"], d["adopted"]["central"], places=9)


if __name__ == "__main__":
    unittest.main(verbosity=1)
