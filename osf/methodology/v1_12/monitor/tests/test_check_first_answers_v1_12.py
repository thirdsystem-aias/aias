#!/usr/bin/env python3
"""
Unit tests for check_first_answers_v1_12.py, on synthetic records only (temporary files; no network, no model call,
no real v1.12 record). Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 /Users/pablou/aias/venv/bin/python -m unittest discover \
        -s osf/methodology/v1_12/monitor/tests -p "test_*.py" -v

The last class runs the checker in a subprocess with the locked coder (scripts/code_t4_v0_42.py) on synthetic capped
answers; that subprocess imports numpy, scipy and the anthropic SDK through the coder's certified modules (no client,
nothing sent). Set V112_CHECK_SKIP_CODER=1 to skip it.
"""
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import check_first_answers_v1_12 as CK   # noqa: E402

AQ = CK.load_acquire()
PARTS = CK.load_scorer_parts()
CAP = 16384
MODELS = {"claude-fable-5-2": "anthropic", "claude-opus-5-5": "anthropic", "gpt-6-astra": "openai",
          "gemini-4-argon": "google"}
# finish reasons as acquire_v1_12.py records them (normal values as in t4's raw record; length values per SDK)
NORMAL_FR = {"anthropic": "end_turn", "openai": "completed", "google": "FinishReason.STOP"}
LENGTH_FR = {"anthropic": "max_tokens", "openai": "incomplete:max_output_tokens", "google": "FinishReason.MAX_TOKENS"}
NORMAL = object()


def billed(out, think=None, error=None):
    return {"utc": "2026-11-14T00:01:00+00:00", "input_tokens": None if error else 80, "output_tokens": out,
            "thinking_tokens": think, "usd": 0.01, "estimated": False, "error": error}


def rec(model, n=1, text="For a new car, look at Toyota and Honda.", status="ok", fr=NORMAL, out=900, think=None,
        attempts=None, substrate="v0.22", **kw):
    prov = MODELS[model]
    r = {"phase": "v1.12", "call_id": f"{substrate}|T{n}|{model}|S0|1", "substrate": substrate, "probe_id": f"T{n}",
         "model_requested": model, "provider": prov, "served_model": model, "served_ok": True, "condition": "S0",
         "run": 1, "pass": 1, "text": text, "status": status, "error": None,
         "finish_reason": NORMAL_FR[prov] if fr is NORMAL else fr, "input_tokens": 80, "output_tokens": out,
         "thinking_tokens": think, "settings": dict(AQ.SETTINGS), "empty_retry": False,
         "billed_attempts": attempts if attempts is not None else [billed(out, think)]}
    r.update(kw)
    return r


def fake_detect(r):
    """Stands in for the coder in the fast tests: registry brands of the synthetic texts."""
    return sorted(b for b in ("Toyota", "Honda") if b in r["text"])


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "v112_raw.jsonl"

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, recs, tail=""):
        self.path.write_text("".join(json.dumps(r) + "\n" for r in recs) + tail, encoding="utf-8")

    def run_check(self, recs, tail=""):
        self.write(recs, tail)
        got, bad, incomplete = CK.read_record(self.path)
        rep = CK.check(got, AQ, PARTS)
        rep.update(unreadable_lines=bad, last_line_incomplete=incomplete)
        return CK.apply_brand_check(rep, fake_detect)

    def one(self, rep):
        self.assertEqual(len(rep["flagged"]), 1, rep["flagged"])
        return rep["flagged"][0]


class TestClear(Base):
    def test_clear_all_models(self):
        recs = [rec(m, n) for n, m in enumerate(MODELS, 1)] + [rec("gpt-6-astra", 9, out=3000, think=1200)]
        rep = self.run_check(recs)
        self.assertEqual(rep["exit"], CK.EXIT_CLEAR)
        self.assertEqual(rep["flagged"], [])
        self.assertEqual({m: r["answered"] for m, r in rep["models"].items()},
                         {"claude-fable-5-2": 1, "claude-opus-5-5": 1, "gpt-6-astra": 2, "gemini-4-argon": 1})
        self.assertEqual(rep["models"]["gemini-4-argon"]["finish_reasons"], {"FinishReason.STOP": 1})
        self.assertIn("RESULT: CLEAR (exit 0)", CK.render(rep))

    def test_one_below_the_cap_is_clear(self):
        rep = self.run_check([rec("claude-opus-5-5", out=CAP - 1), rec("gemini-4-argon", 2, out=CAP - 2, think=1)])
        self.assertEqual(rep["exit"], CK.EXIT_CLEAR)


class TestCapped(Base):
    def test_capped_after_a_brand(self):
        r = rec("claude-opus-5-5", text="For a new car, look at Toyota and Honda. Toyota's hybrid", fr="max_tokens",
                out=CAP)
        f = self.one(self.run_check([r, rec("gpt-6-astra", 2)]))
        self.assertEqual(f["signals"], ["finish reason", "tokens at cap"])
        self.assertEqual(f["named"], ["Honda", "Toyota"])
        self.assertTrue(f["brand"].startswith("names 2 registry brand(s) before the cut"))

    def test_capped_before_any_brand(self):
        r = rec("gpt-6-astra", text="First, think about how you will use the car and", out=CAP, think=15800,
                fr=LENGTH_FR["openai"])
        rep = self.run_check([r])
        f = self.one(rep)
        self.assertEqual(rep["exit"], CK.EXIT_TRIGGER)
        self.assertEqual(f["named"], [])
        self.assertIn("stopped before naming any brand", f["brand"])
        self.assertIn("stopped before naming any brand 1, after naming one 0", CK.render(rep))

    def test_capped_empty_google_counts_thinking(self):
        r = rec("gemini-4-argon", text="", status="empty", fr=LENGTH_FR["google"], out=0, think=CAP)
        f = self.one(self.run_check([r]))
        self.assertEqual(f["signals"], ["finish reason", "tokens at cap"])
        self.assertEqual(f["brand"], "no visible text: stopped before naming any brand")

    def test_google_tokens_at_cap_without_a_length_reason(self):
        r = rec("gemini-4-argon", out=9000, think=CAP - 9000)        # output + thinking = cap, finish reason STOP
        f = self.one(self.run_check([r]))
        self.assertEqual(f["signals"], ["tokens at cap"])

    def test_length_reason_alone_triggers(self):
        f = self.one(self.run_check([rec("claude-fable-5-2", fr="max_tokens", out=None)]))
        self.assertEqual(f["signals"], ["finish reason"])
        self.assertEqual(f["missing"], ["output_tokens"])

    def test_earlier_attempt_at_cap_reasked_by_the_empty_retry(self):
        r = rec("claude-fable-5-2", out=1200, empty_retry=True, attempts=[billed(CAP), billed(1200)])
        rep = self.run_check([r])
        f = self.one(rep)
        self.assertEqual(f["signals"], ["billed attempt at cap"])
        self.assertEqual(f["brand"], CK.EARLIER_ATTEMPT)
        self.assertEqual(rep["models"]["claude-fable-5-2"]["earlier_attempt_at_cap"], 1)

    def test_length_rule_is_the_locked_scorers(self):
        t = PARTS["_truncated"]
        for v in list(LENGTH_FR.values()) + ["length", "MAX_TOKENS"]:
            self.assertTrue(t({"finish_reason": v}), v)
        for v in list(NORMAL_FR.values()) + [None, "stop", "refusal", "FinishReason.SAFETY"]:
            self.assertFalse(t({"finish_reason": v}), v)


class TestThinking(Base):
    def test_thinking_at_half_the_cap_is_a_note_not_a_trigger(self):
        recs = [rec("gpt-6-astra", out=9500, think=9000), rec("gemini-4-argon", 2, out=700, think=CAP // 2),
                rec("gpt-6-astra", 3, out=3000, think=CAP // 2 - 1)]
        rep = self.run_check(recs)
        self.assertEqual(rep["exit"], CK.EXIT_CLEAR)
        self.assertEqual(rep["models"]["gpt-6-astra"]["thinking_half_cap"], 1)
        self.assertEqual(rep["models"]["gemini-4-argon"]["thinking_half_cap"], 1)
        self.assertIn("NOTE: 2 record(s) with thinking tokens >= 8,192", CK.render(rep))

    def test_thinking_on_a_billed_attempt(self):
        r = rec("gpt-6-astra", out=2000, think=100, attempts=[billed(9000, 8500), billed(2000, 100)])
        rep = self.run_check([r])
        self.assertEqual(rep["exit"], CK.EXIT_CLEAR)
        self.assertEqual(rep["models"]["gpt-6-astra"]["thinking_half_cap"], 1)


class TestMissingFields(Base):
    def test_answer_without_finish_reason_cannot_be_checked(self):
        f = self.one(self.run_check([rec("claude-opus-5-5", fr=None)]))
        self.assertEqual((f["signals"], f["missing"]), ([], ["finish_reason"]))
        self.assertEqual(f["brand"], "not checked: no stop at the cap seen (fields missing)")

    def test_google_none_string_is_missing(self):
        f = self.one(self.run_check([rec("gemini-4-argon", fr="None")]))
        self.assertEqual(f["missing"], ["finish_reason"])

    def test_answer_without_output_tokens_cannot_be_checked(self):
        rep = self.run_check([rec("gpt-6-astra", out=None, attempts=[billed(None)])])
        self.assertEqual(self.one(rep)["missing"], ["output_tokens"])
        self.assertEqual(rep["exit"], CK.EXIT_TRIGGER)

    def test_record_without_the_fields_at_all(self):
        r = rec("gemini-4-argon")
        for k in ("finish_reason", "output_tokens", "thinking_tokens", "billed_attempts", "settings"):
            del r[k]
        self.assertEqual(self.one(self.run_check([r]))["missing"], ["finish_reason", "output_tokens"])

    def test_error_record_and_missing_thinking_do_not_trigger(self):
        err = rec("claude-fable-5-2", 2, text="", status="error", fr=None, out=None,
                  attempts=[billed(None, error="APIStatusError")], error="APIStatusError: 400")
        rep = self.run_check([err, rec("claude-opus-5-5", think=None), rec("gemini-4-argon", 3, think=None)])
        self.assertEqual(rep["exit"], CK.EXIT_CLEAR)
        self.assertEqual(rep["models"]["claude-fable-5-2"]["answered"], 0)


class TestRecordHandling(Base):
    def test_incomplete_last_line_and_unreadable_line(self):
        self.write([rec("gpt-6-astra")], tail='not json\n{"call_id": "v0.22|T2|gpt-6')
        got, bad, incomplete = CK.read_record(self.path)
        self.assertEqual((len(got), bad, incomplete), (1, 1, True))

    def test_absent_record(self):
        self.assertEqual(CK.read_record(self.path), (None, 0, False))

    def test_main_never_modifies_the_record(self):
        self.write([rec("claude-opus-5-5", fr="max_tokens", out=CAP), rec("gpt-6-astra", 2)])
        before, mtime = self.path.read_bytes(), self.path.stat().st_mtime_ns
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = CK.main(["--raw", str(self.path), "--json", "--no-brand-check"])
        self.assertEqual(code, CK.EXIT_TRIGGER)
        self.assertEqual((self.path.read_bytes(), self.path.stat().st_mtime_ns), (before, mtime))
        out = json.loads(buf.getvalue())
        self.assertEqual(out["flagged"][0]["brand"], "not checked: --no-brand-check")
        self.assertEqual(sorted(os.listdir(self.tmp.name)), ["v112_raw.jsonl"])


class TestAfterAResume(Base):
    def test_reported_records_do_not_trigger_again(self):
        self.write([rec("claude-opus-5-5", fr="max_tokens", out=CAP), rec("gpt-6-astra", 2)])
        got, _bad, _inc = CK.read_record(self.path)
        rep = CK.apply_brand_check(CK.check(got, AQ, PARTS, reported_through=2), fake_detect)
        self.assertEqual(rep["exit"], CK.EXIT_CLEAR)
        self.assertEqual([f["new"] for f in rep["flagged"]], [False])
        self.assertTrue(rep["flagged"][0]["brand"].startswith("reported earlier"))
        self.assertIn("RESULT: CLEAR (exit 0): no record after record 2", CK.render(rep))
        got.append(rec("gemini-4-argon", 3, fr=LENGTH_FR["google"], out=100, think=CAP - 100))
        rep = CK.apply_brand_check(CK.check(got, AQ, PARTS, reported_through=2), fake_detect)
        self.assertEqual(rep["exit"], CK.EXIT_TRIGGER)
        self.assertEqual([f["new"] for f in rep["flagged"]], [False, True])
        self.assertIn("RESULT: TRIGGER (exit 3): 1 new record(s)", CK.render(rep))


class TestLockedCode(unittest.TestCase):
    def test_locked_files_match_the_manifest(self):
        self.assertEqual(CK.verify_locked(), [])

    def test_a_changed_locked_file_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            m = Path(d) / "manifest"
            m.write_text(f"{'0' * 64}  {CK.LOCKED[1]}\n", encoding="utf-8")
            self.assertEqual(CK.verify_locked(manifest=m), [CK.LOCKED[0], CK.LOCKED[1], CK.LOCKED[2]])

    def test_cap_is_16384_for_every_model(self):
        import inspect
        self.assertEqual((AQ.CURRENT_MAX_TOKENS, AQ.SETTINGS["max_output_tokens"], AQ.OUT_WORST), (CAP, CAP, CAP))
        for m in AQ.PANEL:
            src = inspect.getsource(AQ.CURRENT_DISPATCH[m["provider"]])
            self.assertIn("CURRENT_MAX_TOKENS}", src, m)
        self.assertEqual(sorted(m["model_id"] for m in AQ.PANEL), sorted(MODELS))


@unittest.skipIf(os.environ.get("V112_CHECK_SKIP_CODER"), "V112_CHECK_SKIP_CODER set")
class TestWithTheLockedCoder(Base):
    """The checker as the runner runs it (subprocess), with v0.42's coder on synthetic capped v0.22 answers."""

    def test_brand_check_with_the_coder(self):
        probe = next(p for p in map(json.loads, (CK.V112 / "prereg/probes_v1_12.jsonl").read_text(
            encoding="utf-8").splitlines()) if p["substrate"] == "v0.22" and p["role"] == "CEP")
        a = rec("claude-opus-5-5", 1, text="If you want a new car that holds its value, start with Toyota and Honda. "
                "Toyota's hybrid line is", fr="max_tokens", out=CAP, probe_id=probe["probe_id"])
        b = rec("gpt-6-astra", 2, text="Before choosing a brand to buy new, weigh how you will use the car, what "
                "you can spend each month and", fr=LENGTH_FR["openai"], out=CAP, probe_id=probe["probe_id"])
        self.write([a, b, rec("gemini-4-argon", 3)])
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        p = subprocess.run([sys.executable, str(CK.HERE / "check_first_answers_v1_12.py"), "--raw", str(self.path),
                            "--json"], capture_output=True, text=True, env=env, timeout=170)
        self.assertEqual(p.returncode, CK.EXIT_TRIGGER, p.stderr[-2000:])
        out = json.loads(p.stdout)
        self.assertEqual([f["named"] for f in out["flagged"]], [["Honda", "Toyota"], []], out["flagged"])


if __name__ == "__main__":
    unittest.main()
