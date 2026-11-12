#!/usr/bin/env python3
"""
Tests for acquire_v0_42.py (r2 design, Anthropic Message Batches path, budget guard), budget_v0_42.py and
cost_estimate_v0_42.py. Every provider client is a local fake: no request leaves the machine, nothing is billed.
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import acquire_v0_42 as AQ          # noqa: E402
import budget_v0_42 as BG           # noqa: E402
import cost_estimate_v0_42 as CE    # noqa: E402

FABLE = AQ.PANEL[0]
GPT = AQ.PANEL[1]


def spec(model=FABLE, cond="S1", run=1, phase="B", pid="q1", i=0):
    return {"call_id": f"v20|{phase}|{pid}{i}|{model['model_id']}|{cond}|{run}", "substrate": "v20", "phase": phase,
            "probe_id": f"{pid}{i}", "brand_id": None, "frame_id": f"{pid}{i}", "model": model, "condition": cond,
            "run": run, "block": 0, "system": None, "prompt": f"What are the best skincare brands? {i}"}


def blocks_s1():
    return [NS(type="server_tool_use", name="web_search", input={"query": "best skincare"}),
            NS(type="web_search_tool_result", content=[NS(url="https://a.example/x", title="A", page_age="1d")]),
            NS(type="text", text="CeraVe and ", citations=[NS(url="https://a.example/x", title="A")]),
            NS(type="text", text="La Roche-Posay.", citations=None)]


def message(blocks, stop="end_turn", tin=1000, tout=200, model="claude-fable-5-2"):
    return NS(content=blocks, stop_reason=stop, model=model, usage=NS(input_tokens=tin, output_tokens=tout))


class FakeBatches:
    """messages.batches of a fake Anthropic client; `script(custom_id, params, n)` -> result object."""

    def __init__(self, script):
        self.script, self.created, self.n = script, [], 0

    def create(self, requests):
        self.n += 1
        self.created.append(requests)
        return NS(id=f"batch_{self.n}", processing_status="in_progress")

    def retrieve(self, bid):
        return NS(id=bid, processing_status="ended", ended_at="2026-11-12T01:00:00+00:00")

    def results(self, bid):
        reqs = self.created[int(bid.split("_")[1]) - 1]
        return [NS(custom_id=r["custom_id"], result=self.script(r["custom_id"], r["params"], self.n)) for r in reqs]


class FakeClient:
    def __init__(self, script, sync_reply=None):
        self.batches = FakeBatches(script)
        self.sync_calls = []
        self.sync_reply = sync_reply
        self.messages = self

    def create(self, **kw):          # messages.create (pause_turn continuation)
        self.sync_calls.append(kw)
        return self.sync_reply


def ok(msg):
    return NS(type="succeeded", message=msg)


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.raw = Path(self.tmp.name) / "raw.jsonl"
        self.state = Path(self.tmp.name) / "state.json"
        self.written = []

    def tearDown(self):
        self.tmp.cleanup()

    def ledger(self, **kw):
        return BG.Ledger(self.raw, self.state, **kw)

    def write(self, rec):
        self.written.append(rec)
        with open(self.raw, "a") as f:
            f.write(json.dumps(rec) + "\n")


class TestDesign(unittest.TestCase):
    def test_matrix_and_order(self):
        specs = AQ.build_specs(AQ.load_probes())
        self.assertEqual(len(specs), 876)
        self.assertEqual([m["model_id"] for m in AQ.PANEL], ["claude-fable-5-2", "gpt-6-astra", "gemini-4-argon"])
        self.assertEqual({m["model_id"]: m["mode"] for m in AQ.PANEL}["claude-fable-5-2"], "batch")
        a = [s for s in specs if s["phase"] == "A"]
        self.assertEqual(len(a), 336)
        self.assertEqual({(s["condition"], s["run"]) for s in a}, {("S0", 1)})
        b = [s for s in specs if s["phase"] == "B"]
        self.assertEqual(len(b), 540)
        self.assertEqual(sorted({(s["condition"], s["run"]) for s in b}), [(c, r) for c in ("S0", "S1") for r in (1, 2, 3)])
        blocks = [s["block"] for s in specs]
        self.assertEqual(blocks, sorted(blocks))                         # collection order = block order
        self.assertEqual(AQ.BLOCKS[specs[0]["block"]], ("B", "S0", 1))
        self.assertEqual(AQ.BLOCKS[specs[-1]["block"]], ("B", "S1", 3))
        self.assertNotIn("claude-opus-5-5", {s["model"]["model_id"] for s in specs})

    def test_no_sampling_params_and_cap(self):
        self.assertEqual(AQ.confirm_no_sampling_params(), [])
        self.assertEqual(AQ.CURRENT_MAX_TOKENS, 16384)
        self.assertEqual(AQ.PREREG_TAG, "v0.42-prereg-r1")

    def test_batch_params_equal_sync_call_kwargs(self):
        for cond in ("S0", "S1"):
            s = spec(cond=cond)
            captured = {}

            class C:
                def __init__(self):
                    self.messages = self

                def create(self, **kw):
                    captured.update(kw)
                    return message([NS(type="text", text="x", citations=None)])
            with mock.patch("anthropic.Anthropic", return_value=C()):
                AQ.call_anthropic_current(s["model"]["model_id"], s["prompt"], cond == "S1", None)
            self.assertEqual(AQ.anthropic_params(s), captured)

    def test_batch_parse_equals_sync_parse(self):
        msg = message(blocks_s1())

        class C:
            def __init__(self):
                self.messages = self

            def create(self, **kw):
                return msg
        with mock.patch("anthropic.Anthropic", return_value=C()):
            sync = AQ.call_anthropic_current("claude-fable-5-2", "p", True, None)
        text, srec = AQ.parse_anthropic_blocks(msg.content, True)
        self.assertEqual(text, sync["text"])
        self.assertEqual(srec, sync["search"])
        self.assertEqual(srec["n_searches"], 1)


class TestBatchPath(Base):
    def test_happy_path_costs_at_batch_prices_plus_search_fee(self):
        client = FakeClient(lambda cid, p, n: ok(message(blocks_s1())))
        L = self.ledger()
        st = AQ.run_anthropic_batch([spec(i=i) for i in range(3)], L, self.write, client=client, poll=0, sleep=lambda s: None)
        self.assertEqual(st, "done")
        self.assertEqual(len(self.written), 3)
        r = self.written[0]
        self.assertEqual((r["status"], r["mode"], r["attempts"], r["batch_id"]), ("ok", "batch", 1, "batch_1"))
        self.assertEqual(r["text"], "CeraVe and La Roche-Posay.")
        want = (1000 * 4 + 200 * 20) / 1e6 + 1 * 0.010
        self.assertAlmostEqual(r["cost_usd"], want, places=12)
        self.assertAlmostEqual(L.actual, 3 * want, places=12)
        self.assertEqual(L.reserved, {})
        self.assertEqual(client.batches.created[0][0]["params"], AQ.anthropic_params(spec(i=0)))
        for req in client.batches.created[0]:
            self.assertRegex(req["custom_id"], r"^[a-zA-Z0-9_-]{1,64}$")

    def test_empty_resent_once_transient_retried_invalid_not(self):
        def script(cid, params, n):
            i = int(params["messages"][0]["content"].split()[-1])
            if i == 0:                                     # always empty -> one re-send only
                return ok(message([NS(type="text", text="", citations=None)]))
            if i == 1:                                     # overloaded twice, then fine
                if n < 3:
                    return NS(type="errored", error=NS(type="error", error=NS(type="overloaded_error")))
                return ok(message([NS(type="text", text="fine", citations=None)]))
            if i == 2:
                return NS(type="errored", error=NS(type="error", error=NS(type="invalid_request_error")))
            return NS(type="expired")                      # always expired -> MAX_ATTEMPTS attempts
        client = FakeClient(script)
        st = AQ.run_anthropic_batch([spec(cond="S0", i=i) for i in range(4)], self.ledger(), self.write, client=client,
                                    poll=0, sleep=lambda s: None)
        self.assertEqual(st, "done")
        by = {}
        for r in self.written:
            by.setdefault(r["probe_id"], []).append(r)
        self.assertEqual([r["status"] for r in by["q10"]], ["empty", "empty"])
        self.assertTrue(by["q10"][1]["empty_retry"])
        self.assertEqual([r["status"] for r in by["q11"]], ["error", "error", "ok"])
        self.assertEqual([r["status"] for r in by["q12"]], ["error"])
        self.assertEqual(len(by["q13"]), AQ.MAX_ATTEMPTS)
        self.assertEqual(AQ.done_ids(self.raw), {by["q11"][0]["call_id"]})

    def test_pause_turn_continued_synchronously_with_same_tools(self):
        first = message([NS(type="server_tool_use", name="web_search", input={"query": "q"})], stop="pause_turn")
        second = message([NS(type="text", text="done", citations=None)], tin=500, tout=100)
        client = FakeClient(lambda cid, p, n: ok(first), sync_reply=second)
        AQ.run_anthropic_batch([spec()], self.ledger(), self.write, client=client, poll=0, sleep=lambda s: None)
        r = self.written[0]
        self.assertTrue(r["paused_continued"])
        self.assertEqual([p["mode"] for p in r["usage_parts"]], ["batch", "standard"])
        kw = client.sync_calls[0]
        self.assertEqual(kw["tools"], [AQ.S1_ANTHROPIC])
        self.assertEqual(kw["messages"][-1], {"role": "assistant", "content": first.content})
        want = (1000 * 4 + 200 * 20) / 1e6 + 0.010 + (500 * 8 + 100 * 40) / 1e6
        self.assertAlmostEqual(r["cost_usd"], want, places=12)

    def test_batch_is_split_to_fit_under_the_cap(self):
        client = FakeClient(lambda cid, p, n: ok(message(blocks_s1())))
        per = BG.worst_case("claude-fable-5-2", "S1", "batch")
        L = self.ledger(cap=BG.JUDGE_RESERVE_USD + 2.5 * per, pause_at=1000)
        st = AQ.run_anthropic_batch([spec(i=i) for i in range(5)], L, self.write, client=client, poll=0, sleep=lambda s: None)
        self.assertEqual(st, "done")
        self.assertEqual([len(b) for b in client.batches.created][:1], [2])   # only 2 worst cases fit at first
        self.assertEqual(len(self.written), 5)
        self.assertLessEqual(L.spent(), L.cap)


class TestSyncPath(Base):
    def test_send_call_bills_the_empty_first_answer(self):
        empty = {"text": "", "served_model": "gpt-6-astra", "finish_reason": "completed", "tokens_in": 10,
                 "tokens_out": 5, "tokens_thought": 2, "paused_continued": False, "search": None}
        full = dict(empty, text="Yes.", tokens_in=11, tokens_out=6)
        with mock.patch.object(AQ, "_invoke", side_effect=[(empty, 1, None), (full, 1, None)]), \
                mock.patch.object(AQ.time, "sleep"):
            r = AQ.send_call(spec(model=GPT, cond="S0"))
        self.assertEqual((r["status"], r["attempts"], r["empty_retry"]), ("ok", 2, True))
        self.assertEqual(len(r["usage_parts"]), 2)
        self.assertAlmostEqual(r["cost_usd"], ((10 + 11) * 10 + (5 + 6) * 50) / 1e6, places=12)

    def test_run_sync_stops_before_the_cap(self):
        per = BG.worst_case("gpt-6-astra", "S1")
        L = self.ledger(cap=BG.JUDGE_RESERVE_USD + 3.5 * per, pause_at=1000)

        def sender(s):
            return {"call_id": s["call_id"], "cost_usd": per, "condition": "S1", "status": "ok"}
        st = AQ.run_sync([spec(model=GPT, i=i) for i in range(10)], L, self.write, sender=sender, sleep=lambda s: None)
        self.assertEqual(st, "stop")
        self.assertEqual(len(self.written), 2)       # C28: each sync call reserves 2 worst cases (was 3 written)
        self.assertLessEqual(L.spent(), L.cap)


class TestLedger(Base):
    def test_pause_at_80_from_recorded_usage_and_approval(self):
        rec = {"model_requested": "gpt-6-astra", "condition": "S0", "started_utc": "2026-11-12T00:00:00+00:00",
               "usage_parts": [{"mode": "standard", "input_tokens": 0, "output_tokens": 1_600_000, "n_searches": 0}]}
        self.write(rec)                                    # $80.00 of output
        L = self.ledger()
        self.assertAlmostEqual(L.spent(), 80.0 + BG.JUDGE_RESERVE_USD)
        self.assertEqual(L.reserve(0.01)[0], "pause")
        L2 = self.ledger()
        L2.approve("past_80", "test approval")
        self.assertEqual(L2.reserve(0.01)[0], "ok")
        self.assertTrue(json.loads(self.state.read_text())["approvals"]["past_80"]["note"] == "test approval")

    def test_hard_stop_and_wait(self):
        L = self.ledger(cap=10.0, pause_at=1000, judge_reserve=0.0)
        st, t1 = L.reserve(6.0)
        self.assertEqual(st, "ok")
        self.assertEqual(L.reserve(6.0)[0], "wait")         # fits once the in-flight 6.0 settles cheaper
        L.settle(t1, 5.0)
        self.assertEqual(L.reserve(6.0)[0], "stop")         # 5 + 6 > 10
        self.assertEqual(L.halted, "stop")

    def test_fit_counts(self):
        L = self.ledger(cap=10.0, pause_at=1000, judge_reserve=1.0)
        st, k, tok = L.fit(2.0, 30)
        self.assertEqual((st, k), ("ok", 4))
        self.assertAlmostEqual(L.committed(), 9.0)

    def test_record_cost_legacy_and_parts_and_gemini_december(self):
        legacy = {"model_requested": "gemini-4-argon", "condition": "S1", "input_tokens": 1000, "output_tokens": 100,
                  "thinking_tokens": 50, "search": {"n_searches": 3}, "started_utc": "2026-11-12T00:00:00+00:00"}
        self.assertAlmostEqual(BG.record_cost(legacy), (1000 * 2 + 150 * 10) / 1e6 + 3 * 0.014, places=12)
        dec = dict(legacy, started_utc="2026-12-03T00:00:00+00:00")
        self.assertAlmostEqual(BG.record_cost(dec), (1000 * 4 + 150 * 20) / 1e6 + 3 * 0.014, places=12)
        self.assertEqual(BG.record_cost({"model_requested": "gpt-6-astra", "condition": "S0"}), 0.0)
        with self.assertRaises(KeyError):
            BG.prices("gemini-4-argon", "batch")             # no Gemini batch price on Google's pages

    def test_worst_case_values(self):
        self.assertAlmostEqual(BG.worst_case("claude-fable-5-2", "S1", "batch"),
                               (150_000 * 4 + 16384 * 20) / 1e6 + 10 * 0.010, places=12)
        self.assertAlmostEqual(BG.worst_case("gpt-6-astra", "S0"), (2000 * 10 + 16384 * 50) / 1e6, places=12)


class TestCollectionFlow(Base):
    def _specs(self):
        return AQ.build_specs(AQ.load_probes())

    def _runner(self, cost_of):
        def r(specs, ledger, write):
            for s in specs:
                st, tok = ledger.reserve(cost_of(s))         # fake worst case = its actual cost
                if st != "ok":
                    return st
                rec = {"call_id": s["call_id"], "phase": s["phase"], "condition": s["condition"], "run": s["run"],
                       "model_requested": s["model"]["model_id"], "status": "ok", "text": "x", "error": None,
                       "output_tokens": 1, "finish_reason": "end_turn", "search": None,
                       "usage_parts": [], "cost_usd": cost_of(s)}
                write(rec)
                ledger.settle(tok, rec["cost_usd"])
            return "done"
        return r

    def test_projection_pause_after_s1_run_1(self):
        cost = lambda s: 0.40 if s["condition"] == "S1" else 0.01      # S1 block = 90 x 0.40 = $36 -> projection > 100
        L = self.ledger(pause_at=1000)
        with mock.patch.object(BG, "record_cost", side_effect=lambda r: r.get("cost_usd", 0.0)):
            st = AQ.run_collection(self._specs(), L, self.raw, {"batch": self._runner(cost), "standard": self._runner(cost)},
                                   log=lambda *a: None)
            self.assertEqual(st, "pause")
            self.assertIn("projection", L.halt_reason)
            blocks_done = {(r["phase"], r["condition"], r["run"]) for r in map(json.loads, self.raw.read_text().splitlines())}
            self.assertNotIn(("B", "S1", 2), blocks_done)
            L2 = self.ledger(pause_at=1000)
            L2.approve("projection", "ok")
            st2 = AQ.run_collection(self._specs(), L2, self.raw, {"batch": self._runner(cost), "standard": self._runner(cost)},
                                    log=lambda *a: None)
        self.assertEqual(st2, "stop")                      # continues, then the $100 hard stop ends it
        self.assertLessEqual(L2.spent(), 100.0 + 1e-9)

    def test_full_run_under_budget_and_resume_skips_done(self):
        cost = lambda s: 0.05
        L = self.ledger()
        runners = {"batch": self._runner(cost), "standard": self._runner(cost)}
        self.assertEqual(AQ.run_collection(self._specs(), L, self.raw, runners, log=lambda *a: None), "done")
        n = len(self.raw.read_text().splitlines())
        self.assertEqual(n, 876)
        self.assertEqual(AQ.run_collection(self._specs(), self.ledger(), self.raw, runners, log=lambda *a: None), "done")
        self.assertEqual(len(self.raw.read_text().splitlines()), n)

    def test_collect_refused_without_tag(self):
        with mock.patch.object(AQ.subprocess, "run", return_value=NS(returncode=0, stdout="", stderr="")):
            with self.assertRaises(SystemExit):
                AQ.prereg_guard()


class TestCollectionGuardsC26(Base):
    """Clarification C26 (2026-11-10, before the lock): one paid collection at a time, interrupted-batch recovery,
    collection window."""

    def test_one_paid_collection_family_excluded(self):
        rows = {1: (0, "/sbin/launchd"),
                10: (1, "zsh -ic cd /x && caffeinate -dimsu python3 osf/v42/scripts/acquire_v0_42.py --collect"),
                11: (10, "/Library/.../Python osf/v42/scripts/acquire_v0_42.py --collect"),          # this process
                12: (11, "caffeinate -dimsu python3 osf/v42/scripts/acquire_v0_42.py --collect"),     # its caffeinate
                13: (1, "python3 osf/v42/scripts/acquire_v0_42.py --dry-run"),
                14: (1, "python3 osf/methodology/v1_12/scripts/acquire_v1_12.py --dry-run")}
        self.assertEqual(AQ.other_collection_guard(rows, me=11), [1, 10, 11, 12])
        for other in ("python3 osf/methodology/v1_12/scripts/acquire_v1_12.py --collect",
                      "python3 osf/v40/scripts/acquire_v0_40.py --collect --workers 4",
                      "/Library/.../Python /Users/pablou/aias/_worktrees/v0.42/osf/v42/scripts/acquire_v0_42.py --collect"):
            with self.assertRaises(SystemExit) as cm:
                AQ.other_collection_guard({**rows, 20: (1, other)}, me=11)
            self.assertIn("another paid collection", str(cm.exception))

    def test_window_deadline_and_stop_before_sending(self):
        self.assertEqual(AQ.collection_deadline(self.raw).tzinfo is not None, True)
        self.write({"call_id": "x", "started_utc": "2026-11-12T00:00:00+00:00"})
        self.write({"call_id": "y", "started_utc": "2026-11-11T22:00:00+00:00"})
        self.assertEqual(AQ.collection_deadline(self.raw).isoformat(), "2026-11-14T22:00:00+00:00")
        late = Path(self.tmp.name) / "late.jsonl"
        late.write_text(json.dumps({"started_utc": "2026-11-15T00:00:00+00:00"}) + "\n")
        self.assertEqual(AQ.collection_deadline(late), AQ.WINDOW_HARD_END)
        client = FakeClient(lambda cid, p, n: ok(message(blocks_s1())))
        with mock.patch.object(AQ, "DEADLINE", AQ.datetime(2026, 11, 1, tzinfo=AQ.timezone.utc)):
            L = self.ledger()
            self.assertEqual(AQ.run_anthropic_batch([spec()], L, self.write, client=client, poll=0, sleep=lambda s: None), "stop")
            self.assertEqual(client.batches.created, [])
            self.assertIn("window", L.halt_reason)
            sent = []
            self.assertEqual(AQ.run_sync([spec(model=GPT)], self.ledger(), self.write, sender=sent.append), "stop")
            self.assertEqual(sent, [])

    def test_interrupted_batch_is_recovered_once_and_costed(self):
        journal = Path(self.tmp.name) / "batches.jsonl"
        client = FakeClient(lambda cid, p, n: ok(message(blocks_s1())))
        real_retrieve = client.batches.retrieve

        def killed(bid):
            raise KeyboardInterrupt("run stopped while the batch was in flight")
        client.batches.retrieve = killed
        specs = [spec(i=i) for i in range(3)]
        with self.assertRaises(KeyboardInterrupt):
            AQ.run_anthropic_batch(specs, self.ledger(), self.write, client=client, poll=0, sleep=lambda s: None,
                                   journal=journal)
        self.assertEqual(self.written, [])                              # billed, nothing recorded yet
        self.assertEqual([e["batch_id"] for e in AQ.open_batches(journal)], ["batch_1"])
        # a line of the batch already written before the stop is not written again
        client.batches.retrieve = real_retrieve
        first = AQ.open_batches(journal)[0]["requests"][0]
        partial = AQ._record(specs[0], {"text": "x", "served_model": "claude-fable-5-2", "finish_reason": "end_turn",
                                        "tokens_in": 1000, "tokens_out": 200, "tokens_thought": None,
                                        "paused_continued": False, "search": None}, "ok", None, 1, False,
                             "t0", "t1", [], {"batch_id": "batch_1", "custom_id": first["custom_id"]})
        self.write(partial)
        L = self.ledger()
        n = AQ.recover_batches(specs, L, self.write, journal, self.raw, client=client, poll=0, sleep=lambda s: None,
                               log=lambda *a: None)
        self.assertEqual(n, 1)
        self.assertEqual(len(client.batches.created), 1)                # nothing re-sent
        recs = [r for r in self.written if r.get("batch_id") == "batch_1"]
        self.assertEqual(len(recs), 3)
        self.assertEqual(len({r["custom_id"] for r in recs}), 3)
        want = (1000 * 4 + 200 * 20) / 1e6 + 0.010
        self.assertAlmostEqual(L.actual, 2 * want, places=12)          # the two recovered lines are costed
        self.assertEqual(AQ.open_batches(journal), [])
        self.assertEqual(AQ.recover_batches(specs, L, self.write, journal, self.raw, client=client, poll=0,
                                            sleep=lambda s: None, log=lambda *a: None), 0)

    def test_projection_not_reapplied_once_a_later_block_started(self):
        """Fake rehearsal finding: after an $80 pause in block 7, the resumed run re-applied the projection rule with
        the spend of blocks 6-7 included and paused again. The rule applies once, before block 6 starts."""
        specs = AQ.build_specs(AQ.load_probes())
        flow = TestCollectionFlow()
        cost = lambda s: 0.40 if s["condition"] == "S1" else 0.01          # projection would exceed $100 now
        with mock.patch.object(BG, "record_cost", side_effect=lambda r: r.get("cost_usd", 0.0)):
            for s in specs:                                                # blocks 1-5 done, block 6 begun
                if s["block"] <= 4 or (s["block"] == 5 and s["model"]["model_id"] == "gpt-6-astra"):
                    self.write({"call_id": s["call_id"], "phase": s["phase"], "condition": s["condition"],
                                "run": s["run"], "status": "ok", "text": "x", "error": None, "cost_usd": cost(s)})
            L = self.ledger(pause_at=1000)
            runner = flow._runner(cost)
            st = AQ.run_collection(specs, L, self.raw, {"batch": runner, "standard": runner}, log=lambda *a: None)
        self.assertNotIn("projection", L.halt_reason or "")
        self.assertIn(("B", "S1", 3), AQ.blocks_started(self.raw))
        self.assertIn(st, ("done", "stop"))

    def test_journal_marks_normal_batches_recorded(self):
        journal = Path(self.tmp.name) / "batches.jsonl"
        client = FakeClient(lambda cid, p, n: ok(message(blocks_s1())))
        AQ.run_anthropic_batch([spec(i=i) for i in range(2)], self.ledger(), self.write, client=client, poll=0,
                               sleep=lambda s: None, journal=journal)
        ev = [json.loads(l)["event"] for l in journal.read_text().splitlines()]
        self.assertEqual(ev, ["created", "recorded"])
        self.assertEqual(AQ.open_batches(journal), [])


def _fake_vendor_modules(openai_response=None, gemini_response=None):
    """sys.modules entries for local fake `openai` and `google.genai` SDKs (C28 tests; nothing leaves the machine)."""
    import types as T

    class _E(Exception):
        status_code = 400
    oa = T.ModuleType("openai")
    for n in ("RateLimitError", "APIConnectionError", "APITimeoutError", "APIStatusError"):
        setattr(oa, n, type(n, (_E,), {}))
    oa.OpenAI = lambda *a, **k: NS(responses=NS(create=lambda **kw: openai_response))
    g, ge, gerr, gty = T.ModuleType("google"), T.ModuleType("google.genai"), T.ModuleType("google.genai.errors"), \
        T.ModuleType("google.genai.types")
    gerr.ServerError, gerr.ClientError = type("ServerError", (Exception,), {}), type("ClientError", (Exception,), {})
    gty.Tool = gty.GoogleSearch = gty.GenerateContentConfig = lambda **kw: NS(**kw)
    ge.Client = lambda api_key=None, **k: NS(models=NS(generate_content=lambda **kw: gemini_response))
    ge.errors, ge.types, g.genai = gerr, gty, ge
    return {"openai": oa, "google": g, "google.genai": ge, "google.genai.errors": gerr, "google.genai.types": gty}


class TestUsageC28(Base):
    """Clarification C28 (2026-11-11): recorded usage and the guard count conservatively."""

    def test_openai_open_page_and_find_in_page_are_billed_searches(self):
        item = lambda a: NS(model_dump=lambda: {"type": "web_search_call", "action": a})   # noqa: E731
        r = NS(output=[item({"type": "search", "query": "q", "sources": [{"type": "url", "url": "https://a.example/"}]}),
                       item({"type": "open_page", "url": "https://a.example/p"}),
                       item({"type": "find_in_page", "url": "https://a.example/p", "pattern": "x"}),
                       NS(model_dump=lambda: {"type": "message", "content": [{"type": "output_text", "annotations": []}]})],
               output_text="CeraVe.", model="gpt-6-astra", status="completed", incomplete_details=None,
               usage=NS(input_tokens=1000, output_tokens=100, output_tokens_details=NS(reasoning_tokens=40)))
        with mock.patch.dict(sys.modules, _fake_vendor_modules(openai_response=r)):
            out = AQ.call_openai_current("gpt-6-astra", "p", True)
        self.assertEqual(out["search"]["n_searches"], 1)            # the scientific search count is unchanged
        self.assertEqual(out["billed_searches"], 3)
        part = AQ._part(out, "standard", "S1")
        self.assertEqual(part["n_searches"], 3)
        self.assertAlmostEqual(BG.part_cost("gpt-6-astra", part), (1000 * 10 + 100 * 50) / 1e6 + 3 * 0.010, places=12)
        self.assertEqual(AQ._part(out, "standard", "S0")["n_searches"], 0)

    def test_gemini_tool_use_prompt_tokens_recorded_and_priced_as_input(self):
        gm = NS(web_search_queries=[], grounding_chunks=[NS(web=NS(uri="https://vertexaisearch.cloud.google.com/x",
                                                                       title="dior.com"))], grounding_supports=[])
        r = NS(candidates=[NS(finish_reason="STOP", grounding_metadata=gm)], text="Dior.", model_version="gemini-4-argon",
               usage_metadata=NS(prompt_token_count=200, candidates_token_count=300, thoughts_token_count=50,
                                 tool_use_prompt_token_count=5000))
        with mock.patch.dict(sys.modules, _fake_vendor_modules(gemini_response=r)), \
                mock.patch.dict("os.environ", {"GOOGLE_API_KEY": "fake"}):
            out = AQ.call_google_current("gemini-4-argon", "p", True)
        self.assertEqual(out["tokens_tool_prompt"], 5000)
        self.assertEqual(out["billed_searches"], 1)                 # chunks without a recorded query: one query
        part = AQ._part(out, "standard", "S1")
        self.assertEqual((part["input_tokens"], part["tool_use_prompt_tokens"], part["n_searches"]), (5200, 5000, 1))
        rec = AQ._record(spec(AQ.PANEL[2]), out, "ok", None, 1, False, "2026-11-12T00:00:00+00:00",
                         "2026-11-12T00:00:01+00:00", [part])
        self.assertEqual((rec["input_tokens"], rec["tool_use_prompt_tokens"]), (200, 5000))   # new recorded field
        self.assertAlmostEqual(rec["cost_usd"], (5200 * 2 + 350 * 10) / 1e6 + 0.014, places=12)
        legacy = dict(rec, usage_parts=None)
        self.assertEqual(BG.legacy_part(legacy)["input_tokens"], 5200)

    def test_anthropic_billed_searches_from_usage_server_tool_use(self):
        m = message(blocks_s1())
        m.usage.server_tool_use = NS(web_search_requests=4)
        client = FakeClient(lambda cid, p, n: ok(m))
        ledger = BG.Ledger(self.raw, self.state)
        out, parts, _note = AQ._batch_message_out(spec(), m, client, ledger)
        self.assertEqual(out["search"]["n_searches"], 1)
        self.assertEqual(parts[0]["n_searches"], 4)

    def test_sync_reservation_covers_the_empty_resend(self):
        seen = []

        class L:
            def reserve(self, amount):
                seen.append(amount)
                return "stop", None
        self.assertEqual(AQ.run_sync([spec(GPT)], L(), lambda r: None), "stop")
        self.assertAlmostEqual(seen[0], 2 * BG.worst_case("gpt-6-astra", "S1", "standard"), places=12)


class TestCostEstimate(unittest.TestCase):
    def test_adopted_design_and_hand_check(self):
        basis = CE.load_basis()
        d = CE.cost_of(CE.DESIGNS[next(iter(CE.DESIGNS))], basis, "t4")
        self.assertEqual(d["calls"], 876)
        b = basis[("gpt-6-astra", "S1", "list")]
        want = ((b["in_mean"] * 10 + b["out_mean"] * 50) / 1e6 + b["srch_mean"] * 0.010) * CE.RETRY["central"]
        self.assertAlmostEqual(CE.per_call(basis, "gpt-6-astra", "S1", "B", "central", "standard", "2026-11-11"), want, places=12)
        self.assertLess(d["central"], BG.PAUSE_AT_USD)
        r1 = CE.cost_of(CE.DESIGNS["r1 as drafted: 4 models, 142 probes x S0/S1 x 3 runs, synchronous"], basis, "t4")
        self.assertEqual(r1["calls"], 3408)


if __name__ == "__main__":
    unittest.main(verbosity=1)
