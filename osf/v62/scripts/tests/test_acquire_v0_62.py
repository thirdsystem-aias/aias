"""Tests of acquire_v0_62.py, budget_v0_62.py, params_v0_62.py and cost_estimate_v0_62.py on fakes.
No network, no model, no paid call: every runner and client below is a local fake."""
import json
import os
import subprocess
import sys
import tempfile
import types
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import acquire_v0_62 as A  # noqa: E402
import budget_v0_62 as BG  # noqa: E402
import params_v0_62 as P  # noqa: E402

CT = ZoneInfo("America/Chicago")


def ct(y, mo, d, h=12):
    return datetime(y, mo, d, h, tzinfo=CT).astimezone(timezone.utc)


class Matrix(unittest.TestCase):
    def test_totals_by_option(self):
        for opt, n in (("A", 1212), ("B", 1206), ("C", 1008)):
            probes = A.load_probes(option=opt)
            specs = A.build_specs(probes)
            self.assertEqual(len(specs), n, opt)
            self.assertEqual(A.expected_total(probes), n)
            self.assertEqual(len({s["call_id"] for s in specs}), n)
        self.assertEqual(A.expected_total(A.load_probes(option="A"), drop_phase_a=True), 540)
        self.assertEqual(A.expected_total(A.load_probes(option="A"), drop_run3=True), 1032)

    def test_option_b_and_c_remove_the_right_probes(self):
        b = A.build_specs(A.load_probes(option="B"))
        self.assertFalse([s for s in b if s["substrate"] == "v19" and s["phase"] == "A" and s["brand_id"] == "Denon"])
        self.assertTrue([s for s in b if s["substrate"] == "v19" and s["phase"] == "B"])
        c = A.build_specs(A.load_probes(option="C"))
        self.assertFalse([s for s in c if s["substrate"] == "v19"])

    def test_order_category_questions_first_fr_before_ja(self):
        specs = A.build_specs(A.load_probes(option="A"))
        kinds = [A.BLOCKS[s["block"]][0] for s in specs]
        self.assertEqual(kinds[:540], ["B"] * 540)
        self.assertEqual(set(kinds[540:]), {"A_yn", "A_open"})
        fable_b1 = [s for s in specs if s["block"] == 0 and s["model"]["model_id"] == "claude-fable-5-2"]
        self.assertEqual([s["language"] for s in fable_b1], ["fr"] * 30 + ["ja"] * 30)
        self.assertTrue(all(s["call_id"].startswith(s["language"] + "|") for s in specs))

    def test_prompts_are_the_probe_texts(self):
        probes = A.load_probes(option="A")
        by = {(p["language"], p["substrate"], p["phase"], p["probe_id"]): p["prompt"] for p in probes}
        for s in A.build_specs(probes):
            self.assertEqual(s["prompt"], by[(s["language"], s["substrate"], s["phase"], s["probe_id"])])
            self.assertIsNone(s["system"])
            self.assertEqual(s["condition"], "S0")


class CallSettings(unittest.TestCase):
    def test_no_sampling_params_and_output_cap(self):
        self.assertEqual(A.confirm_no_sampling_params(), [])
        self.assertEqual(A.CURRENT_MAX_TOKENS, 16384)
        self.assertEqual(BG.OUTPUT_CAP, 16384)
        spec = A.build_specs(A.load_probes())[0]
        kw = A.anthropic_params(spec)
        self.assertEqual(kw["max_tokens"], 16384)
        self.assertNotIn("tools", kw)
        self.assertNotIn("system", kw)

    def test_copied_block_byte_for_byte(self):
        src = Path(A.ROOT).parent / "v0.44" / "osf" / "v44" / "scripts" / "acquire_v0_44.py"
        if not src.exists():
            self.skipTest("v0.44 worktree not present")
        v44 = src.read_text(encoding="utf-8")
        mine = Path(A.__file__).read_text(encoding="utf-8")
        for a, b in (("class Transient(Exception):", "# ======================="),
                     ("S1_ANTHROPIC = {", "# ---- copied byte for byte")):
            blk = v44[v44.index(a):v44.index(b, v44.index(a))]
            self.assertIn(blk, mine, a)


class Guards(unittest.TestCase):
    def test_params(self):
        self.assertEqual(P.validate(), ("A", ("2026-11-29", "2026-12-02")))
        for bad in (("2026-11-16", "2026-11-18"), ("2026-11-21", "2026-11-23"), ("2026-11-15", "2026-11-25")):
            with self.assertRaises(ValueError):
                P.validate(window=bad)
        with self.assertRaises(ValueError):
            P.validate(option="D")
        self.assertEqual(P.validate(window=("2026-12-04", "2026-12-07"))[1], ("2026-12-04", "2026-12-07"))

    def test_window_and_blackout(self):
        with tempfile.TemporaryDirectory() as d:
            raw = Path(d) / "raw.jsonl"
            ok, _ = A.window_check(now=ct(2026, 11, 30), dates=P.WINDOW, raw_path=raw)
            self.assertTrue(ok)
            ok, why = A.window_check(now=ct(2026, 11, 28), dates=P.WINDOW, raw_path=raw)
            self.assertFalse(ok)
            ok, why = A.window_check(now=ct(2026, 11, 18), dates=("2026-11-10", "2026-11-30"), raw_path=raw)
            self.assertFalse(ok)
            self.assertIn("blackout", why)
            ok, _ = A.window_check(now=ct(2026, 12, 3, 1), dates=P.WINDOW, raw_path=raw)
            self.assertFalse(ok)
            raw.write_text(json.dumps({"started_utc": ct(2026, 11, 29, 9).isoformat()}) + "\n", encoding="utf-8")
            self.assertEqual(A.deadline(P.WINDOW, raw), ct(2026, 12, 2, 9))   # 72 h after the first call
            ok, _ = A.window_check(now=ct(2026, 12, 2, 10), dates=P.WINDOW, raw_path=raw)
            self.assertFalse(ok)

    def test_declared_window_refuses_blackout_overlap(self):
        with tempfile.TemporaryDirectory() as d:
            dev = Path(d) / "DEVIATIONS.md"
            dev.write_text("## Entry 1 — slip\nNew window 2026-11-20 to 2026-11-23.\n", encoding="utf-8")
            with self.assertRaises(SystemExit):
                A.declared_window("2026-11-20", "2026-11-23", 1, dev)
            dev.write_text("## Entry 1 — slip\nNew window 2026-12-04 to 2026-12-06.\n", encoding="utf-8")
            self.assertEqual(A.declared_window("2026-12-04", "2026-12-06", 1, dev), ("2026-12-04", "2026-12-06"))

    def test_one_collection_at_a_time(self):
        ps = ("  10     1 /usr/bin/python3 osf/v44/scripts/acquire_v0_44.py --collect\n"
              "  11     1 python3 acquire_v0_40.py --dry-run\n"
              "  12     1 zsh\n"
              "  13    12 python3 osf/v62/scripts/acquire_v0_62.py --collect\n")
        self.assertEqual([p for p, _ in A.other_collections(ps, me=13)], [10])
        self.assertEqual(A.other_collections(ps.replace("--collect\n", "--dry-run\n", 1), me=13), [])

    def test_collect_refuses_without_anchor(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.object(A, "ANCHOR_PATH", Path(d) / "none.json"), \
                mock.patch.object(A.subprocess, "run", side_effect=AssertionError("network/git must not be reached")):
            with self.assertRaises(SystemExit) as e:
                A.main(["--collect"])
            self.assertIn("anchor file missing", str(e.exception))

    def test_collect_refuses_without_tag_on_origin(self):
        with tempfile.TemporaryDirectory() as d:
            anchor = Path(d) / "anchor.json"
            anchor.write_text("{}", encoding="utf-8")
            fake = types.SimpleNamespace(returncode=0, stdout="", stderr="")
            with mock.patch.object(A, "ANCHOR_PATH", anchor), mock.patch.object(A.subprocess, "run", return_value=fake):
                with self.assertRaises(SystemExit) as e:
                    A.prereg_guard()
                self.assertIn("not found on origin", str(e.exception))

    def test_default_is_dry_run(self):
        out = subprocess.run([sys.executable, str(Path(A.__file__))], capture_output=True, text=True, timeout=60)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("nothing sent", out.stdout)
        self.assertIn("TOTAL calls: 1212 (expected 1212) -> OK", out.stdout)


def fake_rec(spec, usd_tokens=(1000, 1000), status="ok"):
    out = {"text": "réponse" if status == "ok" else "", "served_model": spec["model"]["model_id"], "finish_reason": "end",
           "tokens_in": usd_tokens[0], "tokens_out": usd_tokens[1], "tokens_thought": 0}
    parts = [A._part(out, spec["model"]["mode"], "S0")]
    return A._record(spec, out, status, None, 1, False, "2026-11-29T15:00:00+00:00", "2026-11-29T15:00:05+00:00", parts)


class Budget(unittest.TestCase):
    def test_judge_reserve_and_costs(self):
        self.assertAlmostEqual(BG.JUDGE_RESERVE_USD, 1.3176, places=4)
        spec = A.build_specs(A.load_probes())[0]               # Fable, batch
        r = fake_rec(spec, (1_000_000, 1_000_000))
        self.assertAlmostEqual(r["cost_usd"], 4.0 + 20.0)
        self.assertEqual(r["language"], "fr")
        gem = [s for s in A.build_specs(A.load_probes()) if s["model"]["model_id"] == "gemini-4-argon"][0]
        r = fake_rec(gem, (1_000_000, 0))
        self.assertAlmostEqual(r["cost_usd"], 2.0)             # November price
        r["started_utc"] = "2026-12-01T06:00:00+00:00"
        self.assertAlmostEqual(BG.record_cost(r), 4.0)         # December price

    def test_pause_at_80_and_stop_at_100(self):
        with tempfile.TemporaryDirectory() as d:
            raw, st = Path(d) / "raw.jsonl", Path(d) / "state.json"
            gpt = [s for s in A.build_specs(A.load_probes()) if s["model"]["model_id"] == "gpt-6-astra"][0]
            rec = fake_rec(gpt, (0, 1_580_000))                  # $79.00
            raw.write_text(json.dumps(rec) + "\n", encoding="utf-8")
            L = BG.Ledger(raw, st)
            self.assertAlmostEqual(L.spent(), 79.0 + BG.JUDGE_RESERVE_USD, places=6)   # 80.32 >= 80
            self.assertAlmostEqual(L.calls_spent(), 79.0, places=6)
            self.assertEqual(L.reserve(0.5)[0], "pause")
            L2 = BG.Ledger(raw, st)
            L2.approve("past_80", "test")
            self.assertEqual(L2.reserve(0.5)[0], "ok")
            self.assertEqual(L2.reserve(19.5)[0], "wait")      # passes $100 only with the in-flight reservation
            L3 = BG.Ledger(raw, st)
            self.assertEqual(L3.reserve(30.0)[0], "stop")


class Collection(unittest.TestCase):
    def _run(self, specs, raw, state, ratio, usd_per_call):
        sent = []

        def runner(group, ledger, write):
            for s in group:
                st, tok = ledger.reserve(0.01)
                if st != "ok":
                    return st
                rec = fake_rec(s, (0, int(usd_per_call / 50.0 * 1e6)) if s["model"]["model_id"] == "gpt-6-astra"
                               else (0, int(usd_per_call / (20.0 if s["model"]["mode"] == "batch" else 10.0) * 1e6)))
                sent.append(s["call_id"])
                write(rec)
                ledger.settle(tok, rec["cost_usd"])
            return "done"
        ledger = BG.Ledger(raw, state)
        st = A.run_collection(specs, ledger, raw, {"batch": runner, "standard": runner}, ratio, log=lambda *a: None)
        return st, sent, ledger

    def test_resumable_and_projection_pause(self):
        specs = A.build_specs(A.load_probes())
        with tempfile.TemporaryDirectory() as d:
            raw, state = Path(d) / "raw.jsonl", Path(d) / "state.json"
            # block 1 costs 180 x $0.10 = $18 > $14.98: projection pause after block 1
            st, sent, ledger = self._run(specs, raw, state, 5.3413, 0.10)
            self.assertEqual(st, "pause")
            self.assertEqual(len(sent), 180)
            self.assertAlmostEqual(ledger.calls_spent(), 18.0, places=6)
            # approve the projection: resumes after block 1 (nothing re-sent)
            BG.Ledger(raw, state).approve("projection", "test")
            st, sent2, _ = self._run(specs, raw, state, 5.3413, 0.01)
            self.assertEqual(st, "done")
            self.assertEqual(len(sent2), 1212 - 180)
            self.assertFalse(set(sent) & set(sent2))

    def test_no_pause_at_expected_cost(self):
        specs = A.build_specs(A.load_probes())
        with tempfile.TemporaryDirectory() as d:
            st, sent, _ = self._run(specs, Path(d) / "raw.jsonl", Path(d) / "s.json", 5.3413, 0.05)
            self.assertEqual(st, "done")
            self.assertEqual(len(sent), 1212)

    def test_drop_phase_a_fallback(self):
        specs = A.build_specs(A.load_probes(), drop_phase_a=True)
        self.assertEqual(len(specs), 540)
        self.assertEqual({s["phase"] for s in specs}, {"B"})

    def test_batch_runner_with_fake_client(self):
        specs = [s for s in A.build_specs(A.load_probes()) if s["model"]["mode"] == "batch"][:3]

        class Msg:
            def __init__(self):
                self.content = [types.SimpleNamespace(type="text", text="Sennheiser, Sony")]
                self.usage = types.SimpleNamespace(input_tokens=100, output_tokens=1000)
                self.model, self.stop_reason = "claude-fable-5-2", "end_turn"

        class Batches:
            def create(self, requests):
                self.ids = [r["custom_id"] for r in requests]
                assert all(r["params"]["max_tokens"] == 16384 for r in requests)
                return types.SimpleNamespace(id="b1")

            def retrieve(self, bid):
                return types.SimpleNamespace(id=bid, processing_status="ended", ended_at=None)

            def results(self, bid):
                return [types.SimpleNamespace(custom_id=c, result=types.SimpleNamespace(type="succeeded", message=Msg()))
                        for c in self.ids]

        client = types.SimpleNamespace(messages=types.SimpleNamespace(batches=Batches()))
        with tempfile.TemporaryDirectory() as d:
            ledger = BG.Ledger(Path(d) / "raw.jsonl", Path(d) / "s.json")
            recs = []
            self.assertEqual(A.run_anthropic_batch(specs, ledger, recs.append, client=client, poll=0), "done")
            self.assertEqual(len(recs), 3)
            self.assertAlmostEqual(recs[0]["cost_usd"], (100 * 4 + 1000 * 20) / 1e6)
            self.assertEqual(ledger.calls_spent(), sum(r["cost_usd"] for r in recs))


class CostEstimate(unittest.TestCase):
    def test_reconciliation_and_options(self):
        import cost_estimate_v0_62 as CE
        pc = CE.per_call()
        for mo, tot in (("nov", (54.42, 130.06)), ("dec", (60.06, 145.92))):
            d = CE.design(pc, mo)
            ph = sum(r["usd_central"] for r in d["rows"]), sum(r["usd_high"] for r in d["rows"])
            self.assertAlmostEqual(ph[0] + CE.judge_reserve(), d["central"], places=9)
            self.assertAlmostEqual(ph[1] + CE.judge_reserve(), d["high"], places=9)
            self.assertEqual((round(d["central"], 2), round(d["high"], 2)), tot)
        self.assertAlmostEqual(CE.judge_reserve(), BG.JUDGE_RESERVE_USD, places=12)
        self.assertEqual([CE.design(pc, "nov", option=o)["calls"] for o in "ABC"], [1212, 1206, 1008])
        j = json.loads((Path(CE.PRE) / "cost_estimate_v0_62_r1.json").read_text(encoding="utf-8"))
        self.assertAlmostEqual(j["projection"]["A"]["nov"], 5.3413, places=4)
        self.assertAlmostEqual(A.projection_ratio(when_utc="2026-12-01T00:00:00", option="C"), j["projection"]["C"]["dec"])


if __name__ == "__main__":
    unittest.main()
