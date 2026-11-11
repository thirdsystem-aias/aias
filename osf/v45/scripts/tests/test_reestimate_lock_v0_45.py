#!/usr/bin/env python3
"""Tests for reestimate_t4_v0_45.py (r1: t5 cost from t4's recorded usage) and lock_manifest_v0_45.py. No model is
called. The test on t4's real file reads it at tag v0.42-acquisition-locked through the script's own field allowlist
(usage and call metadata only) and is skipped where the tag is absent."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import budget_v0_45 as BG             # noqa: E402
import lock_manifest_v0_45 as LM      # noqa: E402
import reestimate_t4_v0_45 as RE      # noqa: E402

ROOT = HERE.parents[3]


def synthetic_lines(scale=1.0):
    """Two calls per model x block (block 4: one yes/no v0.20 and one open v0.23 question); t4 dates; one error line."""
    out = []
    for m, mode in (("claude-fable-5-2", "batch"), ("gpt-6-astra", "standard"), ("gemini-4-argon", "standard")):
        for label, ph, cond, run in RE.BLOCKS:
            for i in range(2):
                sub = ("v23" if i else "v20") if ph == "A" else "v20"
                part = {"mode": mode, "input_tokens": int(1000 * (i + 1) * scale), "output_tokens": int(500 * scale),
                        "thinking_tokens": 100 if m == "gemini-4-argon" else 0, "n_searches": 2 if cond == "S1" else 0}
                rec = {"call_id": f"{sub}|{ph}|q{i}|{m}|{cond}|{run}", "substrate": sub, "phase": ph, "condition": cond,
                       "run": run, "model_requested": m, "mode": mode, "status": "ok", "served_model": m,
                       "started_utc": "2026-11-11T03:00:00+00:00", "usage_parts": [part],
                       "text": "ANSWER TEXT", "prompt": "PROMPT", "search": {"queries": ["q"]}, "error": None}
                rec["cost_usd"] = BG.record_cost(rec)
                out.append(rec)
    err = dict(out[0], status="error", usage_parts=[], cost_usd=0.0, error="overloaded")
    return [err] + out


class TestReestimate(unittest.TestCase):
    def test_only_usage_fields_are_kept(self):
        data = "\n".join(json.dumps(r) for r in synthetic_lines()).encode()
        lines = RE.usage_lines(data)
        self.assertTrue(all(set(r) == set(RE.USAGE_FIELDS) for r in lines))
        for f in RE.FORBIDDEN:
            self.assertNotIn(f, RE.USAGE_FIELDS)
            self.assertTrue(all(f not in r for r in lines))

    def test_refuses_a_raw_file_with_another_sha256(self):
        with tempfile.NamedTemporaryFile(suffix=".jsonl") as f:
            f.write(b'{"call_id": "x"}\n')
            f.flush()
            with self.assertRaises(SystemExit) as cm:
                RE.read_t4_bytes(f.name)
            self.assertIn("REFUSED", str(cm.exception))

    def test_method_on_synthetic_usage(self):
        res = RE.estimate(RE.usage_lines("\n".join(json.dumps(r) for r in synthetic_lines()).encode()))
        self.assertEqual(res["checks"]["calls"], 42)
        self.assertEqual(res["checks"]["error_lines_with_billed_parts"], 0)
        self.assertAlmostEqual(res["checks"]["max_abs_recorded_minus_repriced_t4"], 0.0, places=12)
        c = res["cells"]["gemini-4-argon|1 B-S0 run 1"]       # Gemini doubles on the t5 date; tokens incl. thinking
        want_t5 = ((1000 + 2000) * 4 + (600 + 600) * 20) / 1e6
        self.assertAlmostEqual(c["t5_central_usd"], want_t5, places=12)
        self.assertAlmostEqual(c["t4_usd"], want_t5 / 2, places=12)
        f = res["cells"]["claude-fable-5-2|5 B-S1 run 1"]      # batch tokens, search fee in full
        self.assertAlmostEqual(f["t5_central_usd"], f["t4_usd"], places=12)
        self.assertAlmostEqual(f["t5_central_usd"], ((1000 + 2000) * 4 + 1000 * 20) / 1e6 + 4 * 0.010, places=12)
        p = res["p90_per_call"]["gpt-6-astra|B-S0"]
        g = res["cells"]["gpt-6-astra|2 B-S0 run 2"]
        self.assertAlmostEqual(g["t5_high_usd"], 2 * p["p90_t5"] * RE.RESEND_HIGH, places=12)
        a = res["cells"]["gpt-6-astra|4 A-S0 run 1"]           # A mixes the yes/no and the open question types
        self.assertAlmostEqual(a["t5_high_usd"], (res["p90_per_call"]["gpt-6-astra|A-yn"]["p90_t5"]
                                                  + res["p90_per_call"]["gpt-6-astra|A-open"]["p90_t5"]) * RE.RESEND_HIGH, places=12)
        t = res["totals"]
        self.assertAlmostEqual(t["central_with_reserve"], res["blocks"][-1]["cumulative_central"], places=9)
        self.assertAlmostEqual(t["central"], sum(x["t5_central_usd"] for x in res["cells"].values()), places=9)

    def test_guard_path(self):
        rows = [{"block": b[0], "central": c, "high": 2 * c} for b, c in zip(RE.BLOCKS, (5, 5, 5, 10, 20, 20, 20))]
        cum = {"central": BG.JUDGE_RESERVE_USD, "high": BG.JUDGE_RESERVE_USD}
        for r in rows:
            for k in cum:
                cum[k] += r[k]
                r[f"cumulative_{k}"] = cum[k]
        g = RE.guard_path(rows, "central")                    # 2.5 + 85: crosses $80 in block 7; projection 47.5 + 40
        self.assertEqual(g["pause_80_in_block"], "7 B-S1 run 3")
        self.assertFalse(g["projection_after_block_5"]["pauses"])
        self.assertEqual(len(g["blocks_before_any_pause"]), 6)
        h = RE.guard_path(rows, "high")                       # block 5 ends at 92.5; projection pauses
        self.assertTrue(h["projection_after_block_5"]["pauses"])
        self.assertEqual(h["pause_80_in_block"], "5 B-S1 run 1")
        self.assertEqual([b.split(" ")[0] for b in h["blocks_before_any_pause"]], ["1", "2", "3", "4"])

    def test_on_t4_locked_raw_file(self):
        r = subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", f"{RE.T4_TAG}:{RE.T4_RAW_PATH}"], capture_output=True)
        if r.returncode:
            self.skipTest(f"{RE.T4_TAG} not available")
        res = RE.estimate(RE.usage_lines(RE.read_t4_bytes()))
        c, t = res["checks"], res["totals"]
        self.assertEqual((c["lines"], c["calls"], c["calls_answered"]), (990, 876, 876))
        self.assertAlmostEqual(c["recorded_calls_usd"], RE.T4_RECORDED_CALLS_USD, places=4)
        self.assertLess(c["max_abs_recorded_minus_repriced_t4"], 1e-9)
        self.assertEqual((c["error_lines_with_billed_parts"], c["served_differs_from_requested"]), (0, 0))
        self.assertEqual((round(t["central"], 2), round(t["high"], 2)), (70.40, 149.55))     # section 4.5, r1
        self.assertEqual((round(t["central_with_reserve"], 2), round(t["high_with_reserve"], 2)), (72.90, 152.05))
        self.assertIsNone(res["guard"]["central"]["pause_80_in_block"])
        self.assertTrue(res["guard"]["high"]["projection_after_block_5"]["pauses"])
        txt = (ROOT / "osf/v45/prereg/cost_estimate_v0_45_r1.txt").read_text(encoding="utf-8")
        self.assertEqual(txt, RE.report(res))                 # the deposited text is what the script prints


class TestJ1Usage(unittest.TestCase):
    def test_j1_records_usage_and_cost_inside_the_reserve(self):
        import code_t5_v0_45 as K
        log = [{"input_tokens": 1200, "output_tokens": 3}, {"input_tokens": 800, "output_tokens": None}]
        u = K.j1_usage("claude-sonnet-5-5", log)
        self.assertEqual((u["requests"], u["input_tokens"], u["output_tokens"]), (2, 2000, 3))
        self.assertAlmostEqual(u["usd"], (2000 * 2 + 3 * 10) / 1e6, places=12)
        worst = K.j1_usage("claude-sonnet-4-6", [{"input_tokens": 1500, "output_tokens": 10}] * (144 + 72 + 72))
        best = K.j1_usage("claude-sonnet-5-5", [{"input_tokens": 1500, "output_tokens": 10}] * (144 + 72 + 72))
        self.assertLessEqual(worst["usd"] + best["usd"], BG.JUDGE_RESERVE_USD)     # both candidates: $2.23 <= $2.50


class TestLockManifest(unittest.TestCase):
    def test_lists_v45_files_and_dependencies_not_itself(self):
        fs = LM.files()
        self.assertEqual(len(fs), len(set(fs)))
        for must in ("osf/v45/anchor/DEVIATIONS.md", "osf/v45/prereg/PRE_REGISTRATION_v0_45.md",
                     "osf/v45/prereg/probes_v0_45.jsonl", "osf/v45/prereg/cost_estimate_v0_45_r1.txt",
                     "osf/v45/scripts/acquire_v0_45.py", "osf/v45/scripts/reestimate_t4_v0_45.py",
                     "osf/v45/scripts/tests/test_reestimate_lock_v0_45.py", "osf/v42/scripts/code_t4_v0_42.py",
                     "scripts/score_v0_23.py"):
            self.assertIn(must, fs)
        self.assertNotIn(LM.MANIFEST.relative_to(LM.ROOT).as_posix(), fs)
        self.assertFalse([p for p in fs if "__pycache__" in p or p.startswith("osf/v45/data") or p.startswith("osf/v45/lock")])
        self.assertTrue(all((LM.ROOT / p).is_file() for p in fs))

    def test_format_is_shasum_checkable(self):
        with mock.patch.object(LM, "files", return_value=["osf/v45/prereg/probes_v0_45.jsonl"]):
            line = LM.build()
        h, p = line.rstrip("\n").split("  ", 1)
        self.assertEqual(h, hashlib.sha256((LM.ROOT / p).read_bytes()).hexdigest())
        self.assertEqual(h, "7aa246ee1b28a9bf4f55b8a5c124f099a75bb4ca029c0e42bf2ba1459c6323aa")   # = t4's probe file


if __name__ == "__main__":
    unittest.main(verbosity=1)
