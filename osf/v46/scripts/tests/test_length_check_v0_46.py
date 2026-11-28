"""Tests for length_check_v0_46.py and the collection-time additions (price overlay, parity record path, length-check
spend carried into the Ledger). Fake senders only; no network, no model.
Run: python3 -m unittest discover -s osf/v46/scripts/tests -p 'test_length_check_v0_46.py'"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import acquire_v0_46 as A  # noqa: E402
import length_check_v0_46 as LC  # noqa: E402

NEW = [{"slot": "M2_openai", "model_id": "gpt-6.2-astra", "provider": "openai", "mode": "standard"},
       {"slot": "M3_google", "model_id": "gemini-4-carbon", "provider": "google", "mode": "standard"}]
QUIET = lambda *a, **k: None  # noqa: E731


def fake_sender(limit_on=None, text="I recommend Counter Culture Coffee."):
    def send(spec):
        cut = limit_on is not None and spec["model"]["model_id"] == limit_on
        out = {"text": "" if cut else text, "served_model": spec["model"]["model_id"],
               "finish_reason": ("MAX_TOKENS" if cut else "STOP") if spec["model"]["provider"] == "google"
               else ("incomplete:max_output_tokens" if cut else "completed"),
               "tokens_in": 100, "tokens_out": 16384 - 1000 if cut else 300,
               "tokens_thought": (1000 if cut else 200) if spec["model"]["provider"] == "google" else 50,
               "paused_continued": False, "search": None}
        return A._record(spec, out, "ok" if not cut else "empty", None, 1, False, "2026-11-28T11:00:00+00:00",
                         "2026-11-28T11:00:05+00:00", [A._part(out, "standard", "S0")])
    return send


class TestLengthCheck(unittest.TestCase):
    def test_plan(self):
        specs = LC.build_plan(models=NEW)
        self.assertEqual(len(specs), 48)
        self.assertEqual(len({s["call_id"] for s in specs}), 48)
        self.assertTrue(all(s["condition"] == "S0" and s["system"] is None for s in specs))
        qs = {p["prompt"] for p in LC.load_questions()}
        self.assertTrue(all(s["prompt"] in qs for s in specs))

    def test_prices_overlay(self):
        self.assertEqual(A.BG.PROVIDER["gpt-6.2-astra"], "openai")
        self.assertEqual(A.BG.prices("gpt-6.2-astra", "standard"), (8.0, 40.0))
        self.assertEqual(A.BG.prices("gemini-4-carbon", "standard", "2026-11-30T23:59:00+00:00"), (2.0, 10.0))
        self.assertEqual(A.BG.prices("gemini-4-carbon", "standard", "2026-12-01T00:00:00+00:00"), (4.0, 20.0))
        self.assertEqual(A.BG.prices("gemini-4-argon", "standard", "2026-12-01T00:00:00+00:00"), (4.0, 20.0))
        # Google worst case: output at the 16,384 cap, inside which Gemini counts thinking (max_output_tokens)
        self.assertAlmostEqual(A.BG.worst_case("gemini-4-carbon", "S0", "standard", "2026-12-01T00:00:00+00:00"),
                               (2000 * 4 + 16384 * 20) / 1e6)

    def test_run_pass_and_spend(self):
        with tempfile.TemporaryDirectory() as d:
            raw = Path(d) / "lc.jsonl"
            specs = LC.build_plan(models=NEW)
            res, paused = LC.run(log=QUIET, specs=specs, sender=fake_sender(), raw=raw,
                                 stop_path=Path(d) / "stop.jsonl", guards=False)
            self.assertEqual(sorted(res), ["done", "done"])
            self.assertEqual(paused, [])
            ev = LC.evaluate(raw=raw, specs=specs, named_fn=lambda t: 1 if t else 0, write=False, prior=[])
            self.assertEqual(ev["verdict"], "PASS")
            self.assertEqual(ev["models"]["gemini-4-carbon"]["billed_output"]["max"], 500)
            self.assertGreater(A.length_check_spend(raw), 0)
            self.assertAlmostEqual(A.length_check_spend(raw), ev["spend_usd"], places=5)

    def test_run_stops_model_at_limit(self):
        with tempfile.TemporaryDirectory() as d:
            raw = Path(d) / "lc.jsonl"
            specs = LC.build_plan(models=NEW)
            res, paused = LC.run(log=QUIET, specs=specs, sender=fake_sender(limit_on="gemini-4-carbon"), raw=raw,
                                 stop_path=Path(d) / "stop.jsonl", guards=False)
            self.assertEqual(paused, ["M3_google"])
            lines = [json.loads(l) for l in raw.read_text().splitlines()]
            self.assertEqual(sum(1 for r in lines if r["model_requested"] == "gemini-4-carbon"), 1)
            self.assertEqual(sum(1 for r in lines if r["model_requested"] == "gpt-6.2-astra"), 24)
            ev = LC.evaluate(raw=raw, specs=specs, named_fn=lambda t: 1 if t else 0, write=False, prior=[])
            self.assertEqual(ev["verdict"], "STOP")

    def test_parity_path(self):
        self.assertEqual(A.PARITY_PATH.name, "code_parity_v0_46_collection.json")


if __name__ == "__main__":
    unittest.main()
