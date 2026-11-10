#!/usr/bin/env python3
"""
Unit tests for acquire_v1_12.py --collect in mock mode (no provider SDK, no network, no API key, nothing spent).
The provider call functions, `git ls-remote`, the process list and the clock are replaced by fakes; the raw record,
the guard log, the anchor and the t4 completion record live in a temporary directory. Covered: the budget guard
($100 hard cap, pause at $80, approval), the window guard (windows, blackout, re-check before every request), the
t4-completion and one-collection-at-a-time guards, the anchor/tag check, and resumability (answered calls skipped,
at most two passes). Run from the repository root:

    python3 -m unittest discover -s osf/methodology/v1_12/scripts/tests -p "test_*.py" -v
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import acquire_v1_12 as A   # noqa: E402

UTC = timezone.utc
INSIDE = datetime(2026, 11, 14, 6, 0, tzinfo=UTC)
COMMIT = "c0ffee0000000000000000000000000000000001"
TAGOBJ = "7a90000000000000000000000000000000000002"


class FakeProvider:
    """Counts calls per model; answers with fixed token counts; optional failure rule (model_id, prompt) -> bool."""

    def __init__(self, tokens_out=500, fail=None):
        self.tokens_out, self.fail = tokens_out, fail
        self.calls = []
        self.lock = threading.Lock()

    def make(self):
        def fn(model_id, prompt, search, system=None):
            assert search is False and system is None
            with self.lock:
                self.calls.append((model_id, prompt))
            if self.fail and self.fail(model_id, prompt):
                raise ValueError("fake permanent error")
            return {"text": "Brand A and Brand B.", "served_model": model_id, "finish_reason": "stop",
                    "tokens_in": 80, "tokens_out": self.tokens_out, "tokens_thought": 0, "paused_continued": False}
        return fn


class CollectBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        self.saved = {k: getattr(A, k) for k in ("RAW_PATH", "GUARD_LOG", "ANCHOR_PATH", "T4_RECORD", "GUARD",
                                                  "_utcnow", "running_commands", "PAUSE", "CURRENT_DISPATCH")}
        self.saved_run = A.subprocess.run
        self.saved_env = {k: os.environ.get(k) for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY")}
        for k in self.saved_env:
            os.environ[k] = "fake-key-for-tests"
        A.RAW_PATH, A.GUARD_LOG = d / "data" / "v112_raw.jsonl", d / "data" / "v112_guard_log.jsonl"
        A.ANCHOR_PATH, A.T4_RECORD = d / "anchor" / "osf_anchor_v1_12.json", d / "anchor" / "t4_complete_v1_12.json"
        A.ANCHOR_PATH.parent.mkdir(parents=True)
        A.ANCHOR_PATH.write_text(json.dumps({"tag": A.PREREG_TAG, "commit": COMMIT}), encoding="utf-8")
        self.t4_raw = d / "t4_raw.jsonl"
        self.t4_raw.write_text(json.dumps({"call_id": "x", "finished_utc": "2026-11-13T20:00:00+00:00"}) + "\n",
                               encoding="utf-8")
        self.write_t4_record("2026-11-13T20:00:00+00:00")
        A.GUARD = A.Guard()
        A._utcnow = lambda: INSIDE
        A.running_commands = lambda: [(1, "/sbin/launchd"), (2, "python3 acquire_v1_12.py --dry-run")]
        A.PAUSE = {"anthropic": 0.0, "openai": 0.0, "google": 0.0}
        self.provider = FakeProvider()
        self.install(self.provider)
        self.remote = f"{TAGOBJ}\trefs/tags/{A.PREREG_TAG}\n{COMMIT}\trefs/tags/{A.PREREG_TAG}^{{}}\n"
        self.git_calls = []

        def fake_run(args, **kw):
            self.git_calls.append(args)
            if args[:2] == ["git", "ls-remote"]:
                return subprocess.CompletedProcess(args, 0, stdout=self.remote, stderr="")
            raise AssertionError(f"unexpected subprocess call {args}")
        A.subprocess.run = fake_run

    def tearDown(self):
        for k, v in self.saved.items():
            setattr(A, k, v)
        A.subprocess.run = self.saved_run
        for k, v in self.saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        self.tmp.cleanup()

    def install(self, provider):
        fn = provider.make()
        A.CURRENT_DISPATCH = {"anthropic": fn, "openai": fn, "google": fn}

    def write_t4_record(self, last, sha=None):
        sha = sha or hashlib.sha256(self.t4_raw.read_bytes()).hexdigest()
        A.T4_RECORD.parent.mkdir(parents=True, exist_ok=True)
        A.T4_RECORD.write_text(json.dumps({"t4_raw_path": str(self.t4_raw), "t4_raw_sha256": sha,
                                           "t4_last_call_utc": last, "recorded_by": "test"}), encoding="utf-8")

    def records(self):
        return A.read_raw()

    def collect(self, approval=None):
        A.GUARD = A.Guard()
        return A.collect(1, approval)


class TestAnchorAndTag(CollectBase):
    def test_refused_without_tag_on_origin(self):
        self.remote = ""
        with self.assertRaises(SystemExit) as cm:
            self.collect()
        self.assertIn("not found on origin", str(cm.exception))
        self.assertEqual(self.provider.calls, [])

    def test_refused_without_anchor(self):
        A.ANCHOR_PATH.unlink()
        with self.assertRaises(SystemExit) as cm:
            self.collect()
        self.assertIn("anchor file missing", str(cm.exception))

    def test_refused_when_anchor_names_another_commit(self):
        A.ANCHOR_PATH.write_text(json.dumps({"commit": "deadbeef" * 5}), encoding="utf-8")
        with self.assertRaises(SystemExit) as cm:
            self.collect()
        self.assertIn("does not name the commit", str(cm.exception))
        self.assertEqual(self.provider.calls, [])

    def test_accepts_peeled_commit(self):
        self.assertEqual(A.prereg_guard(), COMMIT)


class TestWindowAndOverlap(CollectBase):
    def test_window_edges(self):
        t = lambda *a: datetime(*a, tzinfo=UTC)
        self.assertFalse(A.in_window(t(2026, 11, 13, 23, 59, 59)))
        self.assertTrue(A.in_window(t(2026, 11, 14, 0, 0, 0)))
        self.assertTrue(A.in_window(t(2026, 11, 16, 23, 59, 59)))
        for day in (17, 18, 19, 20, 21):                         # v0.40 collects Nov 17-21: never
            self.assertFalse(A.in_window(t(2026, 11, day, 12, 0, 0)))
        self.assertFalse(A.in_window(t(2026, 11, 22, 11, 59, 59)))
        self.assertTrue(A.in_window(t(2026, 11, 22, 12, 0, 0)))
        self.assertTrue(A.in_window(t(2026, 11, 29, 23, 59, 59)))
        self.assertFalse(A.in_window(t(2026, 11, 30, 0, 0, 0)))

    def test_refused_outside_window(self):
        for now in (datetime(2026, 11, 13, 12, tzinfo=UTC), datetime(2026, 11, 18, 12, tzinfo=UTC)):
            A._utcnow = lambda now=now: now
            with self.assertRaises(SystemExit) as cm:
                self.collect()
            self.assertIn("outside the collection windows", str(cm.exception))
        self.assertEqual(self.provider.calls, [])

    def test_window_rechecked_before_every_request(self):
        n = {"i": 0}
        lock = threading.Lock()

        def clock():
            with lock:
                n["i"] += 1
                return INSIDE if n["i"] <= 11 else datetime(2026, 11, 17, 0, 0, 1, tzinfo=UTC)
        A._utcnow = clock
        self.assertEqual(self.collect(), 4)
        self.assertLessEqual(len(self.provider.calls), 10)
        self.assertIn("outside the collection windows", A.GUARD.stopped)
        self.assertEqual(len(self.records()), len(self.provider.calls))

    def test_refused_while_t4_not_recorded_complete(self):
        A.T4_RECORD.unlink()
        with self.assertRaises(SystemExit) as cm:
            self.collect()
        self.assertIn("t4 (v0.42) is not recorded as complete", str(cm.exception))
        self.assertEqual(self.provider.calls, [])

    def test_refused_when_t4_raw_changed(self):
        with open(self.t4_raw, "a", encoding="utf-8") as f:
            f.write(json.dumps({"call_id": "y", "finished_utc": "2026-11-13T21:00:00+00:00"}) + "\n")
        with self.assertRaises(SystemExit) as cm:
            self.collect()
        self.assertIn("t4 raw file changed", str(cm.exception))

    def test_refused_when_t4_call_after_recorded_last(self):
        self.write_t4_record("2026-11-13T19:00:00+00:00")
        with self.assertRaises(SystemExit) as cm:
            self.collect()
        self.assertIn("after the recorded last call", str(cm.exception))

    def test_refused_when_t4_last_call_not_past(self):
        self.write_t4_record("2026-11-14T07:00:00+00:00")
        with self.assertRaises(SystemExit) as cm:
            self.collect()
        self.assertIn("not in the past", str(cm.exception))

    def test_refused_while_other_paid_collection_runs(self):
        for cmd in ("python3 osf/v42/scripts/acquire_v0_42.py --collect",
                    "/usr/bin/python3 acquire_v0_40.py --collect --max-concurrency 2",
                    "python3 acquire_v1_12.py --collect"):
            A.running_commands = lambda cmd=cmd: [(99999, cmd)]
            with self.assertRaises(SystemExit) as cm:
                self.collect()
            self.assertIn("another paid collection is running", str(cm.exception))
        self.assertEqual(self.provider.calls, [])

    def test_other_collection_guard_ignores_self_and_non_collect(self):
        A.other_collection_guard([(os.getpid(), "python3 acquire_v1_12.py --collect"),
                                  (12, "python3 acquire_v0_42.py --dry-run"),
                                  (13, "python3 audit_v1_13.py --collect")])   # the audit makes no paid call


class TestBudgetGuard(CollectBase):
    def test_constants(self):
        self.assertEqual((A.CAP_USD, A.PAUSE_USD), (100.0, 80.0))

    def test_pause_at_80_then_hard_cap_at_100(self):
        self.install(FakeProvider(tokens_out=16384))             # every answer at the output cap (worst case)
        self.assertEqual(self.collect(), 4)
        spent1 = sum(r["usd_billed"] for r in self.records())
        self.assertGreaterEqual(spent1, A.PAUSE_USD)
        self.assertLess(spent1, A.PAUSE_USD + 4 * 0.83)          # at most one call in flight per model past $80
        self.assertIn("PAUSED", A.GUARD.stopped)
        log = [json.loads(l) for l in A.GUARD_LOG.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(log[-1]["event"], "stopped")
        n1 = len(self.provider.calls)
        self.assertEqual(self.collect(), 4)                      # resumed without approval: nothing is sent
        self.assertEqual(len(self.provider.calls), n1)
        self.assertEqual(self.collect(approval="Pablo, test"), 4)
        spent2 = sum(r["usd_billed"] for r in self.records())
        self.assertLessEqual(spent2, A.CAP_USD)
        self.assertIn("CAP", A.GUARD.stopped)
        self.assertGreater(spent2, A.CAP_USD - 1.0)              # stopped only when the next worst case no longer fit
        log = [json.loads(l) for l in A.GUARD_LOG.read_text(encoding="utf-8").splitlines()]
        self.assertIn("approval to spend past $80", [e["event"] for e in log])

    def test_guard_reserve_rules(self):
        g = A.Guard(spent=79.99)
        g.settle(g.reserve("gpt-6-astra", INSIDE), 0.5)
        with self.assertRaises(A.GuardStop):
            g.reserve("gpt-6-astra", INSIDE)                     # pause at $80 without approval
        g = A.Guard(spent=99.5, approved="Pablo")
        with self.assertRaises(A.GuardStop):
            g.reserve("gpt-6-astra", INSIDE)                     # 99.5 + 0.82 worst case > 100
        g = A.Guard(spent=99.5, approved="Pablo")
        g.settle(g.reserve("gemini-4-argon", INSIDE), 0.1)       # 99.5 + 0.16 <= 100
        self.assertAlmostEqual(g.spent, 99.6)
        g = A.Guard(spent=99.0, approved="Pablo")
        w = g.reserve("gpt-6-astra", INSIDE)                     # 99 + 0.82 <= 100: sent, and held in flight
        with self.assertRaises(A.GuardStop):
            g.reserve("claude-fable-5-2", INSIDE)                # 99 + 0.82 in flight + 0.66 > 100
        self.assertAlmostEqual(w, A.worst_usd("gpt-6-astra", INSIDE))


class TestResumability(CollectBase):
    def test_skips_answered_and_caps_passes(self):
        bad = {p["prompt"] for p in A.load_probes()[0][:5]}
        self.install(FakeProvider(fail=lambda m, pr: m == "gemini-4-argon" and pr in bad))
        self.assertEqual(self.collect(), 0)
        recs = self.records()
        self.assertEqual(len(recs), A.EXPECTED_TOTAL)
        self.assertEqual(sum(1 for r in recs if A.answered(r)), A.EXPECTED_TOTAL - 15)   # 5 probes x 3 runs
        self.assertEqual(sum(1 for r in recs if r["status"] == "error"), 15)
        # second invocation: only the 15 missing calls are sent (pass 2); they fail again
        p2 = FakeProvider(fail=lambda m, pr: m == "gemini-4-argon" and pr in bad)
        self.install(p2)
        self.assertEqual(self.collect(), 0)
        self.assertEqual(len(p2.calls), 15)
        self.assertEqual({r["pass"] for r in self.records() if r["status"] == "error"}, {1, 2})
        # third invocation: past the re-run cap, nothing is sent; those cells stay missing
        p3 = FakeProvider()
        self.install(p3)
        self.assertEqual(self.collect(), 0)
        self.assertEqual(p3.calls, [])

    def test_resume_completes_after_interruption(self):
        lim = {"n": 0}
        lock = threading.Lock()

        def clock():
            with lock:
                lim["n"] += 1
                return INSIDE if lim["n"] <= 41 else datetime(2026, 11, 20, tzinfo=UTC)
        A._utcnow = clock
        self.assertEqual(self.collect(), 4)                      # stopped by the window after <= 40 calls
        first = len(self.records())
        self.assertGreater(first, 0)
        self.assertLess(first, A.EXPECTED_TOTAL)
        A._utcnow = lambda: datetime(2026, 11, 22, 13, tzinfo=UTC)
        p2 = FakeProvider()
        self.install(p2)
        self.assertEqual(self.collect(), 0)
        self.assertEqual(len(p2.calls), A.EXPECTED_TOTAL - first)   # nothing answered is sent again
        recs = self.records()
        self.assertEqual(len({r["call_id"] for r in recs if A.answered(r)}), A.EXPECTED_TOTAL)
        self.assertEqual(len(recs), A.EXPECTED_TOTAL)

    def test_no_real_provider_or_network(self):
        self.assertTrue(all(fn.__name__ == "fn" for fn in A.CURRENT_DISPATCH.values()))
        for mod in ("anthropic", "openai", "google.genai"):
            self.assertNotIn(mod, sys.modules)


if __name__ == "__main__":
    unittest.main()
