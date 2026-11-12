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
        for opt, n in (("A", 1818), ("B", 1809), ("C", 1512)):
            probes = A.load_probes(option=opt)
            specs = A.build_specs(probes)
            self.assertEqual(len(specs), n, opt)
            self.assertEqual(A.expected_total(probes), n)
            self.assertEqual(len({s["call_id"] for s in specs}), n)
        self.assertEqual(A.expected_total(A.load_probes(option="A"), drop_phase_a=True), 810)
        self.assertEqual(A.expected_total(A.load_probes(option="A"), drop_run3=True), 1548)

    def test_option_b_and_c_remove_the_right_probes(self):
        b = A.build_specs(A.load_probes(option="B"))
        self.assertFalse([s for s in b if s["substrate"] == "v19" and s["phase"] == "A" and s["brand_id"] == "Denon"])
        self.assertTrue([s for s in b if s["substrate"] == "v19" and s["phase"] == "B"])
        c = A.build_specs(A.load_probes(option="C"))
        self.assertFalse([s for s in c if s["substrate"] == "v19"])

    def test_order_category_questions_first_es_ko_zh(self):
        specs = A.build_specs(A.load_probes(option="A"))
        kinds = [A.BLOCKS[s["block"]][0] for s in specs]
        self.assertEqual(kinds[:810], ["B"] * 810)
        self.assertEqual(set(kinds[810:]), {"A_yn", "A_open"})
        fable_b1 = [s for s in specs if s["block"] == 0 and s["model"]["model_id"] == "claude-fable-5-2"]
        self.assertEqual([s["language"] for s in fable_b1], ["es"] * 30 + ["ko"] * 30 + ["zh"] * 30)
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
        self.assertIn("TOTAL calls: 1818 (expected 1818) -> OK", out.stdout)
        # r3 update (section 9 item 7 (b)): the 88 yes/no brand questions (block 4) are collected, last
        self.assertIn("brand-question extras (params BRAND_EXTRAS): OFF; yes/no brand questions (params BRAND_YES_NO; "
                      "block 4, last): ON -> calls sent: 1602 (design core_plus_yn)", out.stdout)


def fake_rec(spec, usd_tokens=(1000, 1000), status="ok"):
    out = {"text": "réponse" if status == "ok" else "", "served_model": spec["model"]["model_id"], "finish_reason": "end",
           "tokens_in": usd_tokens[0], "tokens_out": usd_tokens[1], "tokens_thought": 0}
    parts = [A._part(out, spec["model"]["mode"], "S0")]
    return A._record(spec, out, status, None, 1, False, "2026-11-29T15:00:00+00:00", "2026-11-29T15:00:05+00:00", parts)


class Budget(unittest.TestCase):
    def test_judge_reserve_and_costs(self):
        self.assertAlmostEqual(BG.JUDGE_RESERVE_USD, 2.4624, places=4)
        spec = A.build_specs(A.load_probes())[0]               # Fable, batch
        r = fake_rec(spec, (1_000_000, 1_000_000))
        self.assertAlmostEqual(r["cost_usd"], 4.0 + 20.0)
        self.assertEqual(r["language"], "es")
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
            self.assertAlmostEqual(L.spent(), 79.0 + BG.JUDGE_RESERVE_USD, places=6)   # 81.46 >= 80
            self.assertAlmostEqual(L.calls_spent(), 79.0, places=6)
            self.assertEqual(L.reserve(0.5)[0], "pause")
            L2 = BG.Ledger(raw, st)
            L2.approve("past_80", "test")
            self.assertEqual(L2.reserve(0.5)[0], "ok")
            self.assertEqual(L2.reserve(18.2)[0], "wait")      # passes $100 only with the in-flight reservation
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
            # block 1 costs 270 x $0.10 = $27 > $80 / 5.3597: projection pause after block 1
            st, sent, ledger = self._run(specs, raw, state, 5.3597, 0.10)
            self.assertEqual(st, "pause")
            self.assertEqual(len(sent), 270)
            self.assertAlmostEqual(ledger.calls_spent(), 27.0, places=6)
            # approve the projection: resumes after block 1 (nothing re-sent)
            BG.Ledger(raw, state).approve("projection", "test")
            st, sent2, _ = self._run(specs, raw, state, 5.3597, 0.01)
            self.assertEqual(st, "done")
            self.assertEqual(len(sent2), 1818 - 270)
            self.assertFalse(set(sent) & set(sent2))

    def test_no_pause_at_expected_cost(self):
        specs = A.build_specs(A.load_probes())
        with tempfile.TemporaryDirectory() as d:
            st, sent, _ = self._run(specs, Path(d) / "raw.jsonl", Path(d) / "s.json", 5.3597, 0.04)
            self.assertEqual(st, "done")
            self.assertEqual(len(sent), 1818)

    def test_drop_phase_a_fallback(self):
        specs = A.build_specs(A.load_probes(), drop_phase_a=True)
        self.assertEqual(len(specs), 810)
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
        for mo, tot in (("nov", (89.36, 232.37)), ("dec", (98.59, 260.68))):
            d = CE.design(pc, mo)
            ph = sum(r["usd_central"] for r in d["rows"]), sum(r["usd_high"] for r in d["rows"])
            self.assertAlmostEqual(ph[0] + CE.judge_reserve(), d["central"], places=9)
            self.assertAlmostEqual(ph[1] + CE.judge_reserve(), d["high"], places=9)
            self.assertEqual((round(d["central"], 2), round(d["high"], 2)), tot)
        self.assertAlmostEqual(CE.judge_reserve(), BG.JUDGE_RESERVE_USD, places=12)
        self.assertEqual([CE.design(pc, "nov", option=o)["calls"] for o in "ABC"], [1818, 1809, 1512])
        b = CE.design(pc, "dec", a_runs=0)
        self.assertEqual((b["calls"], round(b["central"], 2), round(b["high"], 2)), (810, 55.50, 142.06))
        j = json.loads((Path(CE.PRE) / "cost_estimate_v0_62_r2.json").read_text(encoding="utf-8"))
        self.assertAlmostEqual(j["projection"]["A"]["nov"], 5.3597, places=4)                  # r2 record (kept)
        with mock.patch.object(P, "BRAND_YES_NO", False):                                       # core only
            self.assertEqual(A.projection_ratio(when_utc="2026-12-01T00:00:00", option="C"), 3.0)   # extras off
        self.assertEqual(Path(A.COST_PATH).name, "cost_estimate_v0_62_r3.json")                # r3: t4-based
        j3 = json.loads(Path(A.COST_PATH).read_text(encoding="utf-8"))
        # r3 update: core + block 4 (section 9 item 7 (b)) uses that design's central ratio
        self.assertAlmostEqual(A.projection_ratio(when_utc="2026-12-01T00:00:00", option="C"),
                               j3["projection_core_plus_yn"]["C"]["dec"])
        with mock.patch.object(P, "BRAND_EXTRAS", True):
            self.assertAlmostEqual(A.projection_ratio(when_utc="2026-12-01T00:00:00", option="C"), j3["projection"]["C"]["dec"])
            self.assertAlmostEqual(A.projection_ratio(when_utc="2026-11-29T06:00:00", option="A"), j3["projection"]["A"]["nov"])


class ConservativeCounting(unittest.TestCase):
    """r2: the guard counts conservatively (task of 2026-11-10 evening)."""

    def _spec(self, model_id):
        return [s for s in A.build_specs(A.load_probes()) if s["model"]["model_id"] == model_id][0]

    def test_failed_attempts_costed_at_worst_case(self):
        spec = self._spec("gpt-6-astra")
        ok = {"text": "Sennheiser", "served_model": "gpt-6-astra", "finish_reason": "completed",
              "tokens_in": 100, "tokens_out": 100, "tokens_thought": 0}
        with mock.patch.object(A, "_invoke", return_value=(ok, 3, None)), mock.patch.object(A.time, "sleep"):
            rec = A.send_call(spec)
        wc = BG.worst_case("gpt-6-astra", "S0", "standard", rec["started_utc"])
        self.assertAlmostEqual(rec["cost_usd"], 2 * wc + (100 * 10 + 100 * 50) / 1e6)
        with mock.patch.object(A, "_invoke", return_value=(None, 3, "transient: ReadTimeout")), \
                mock.patch.object(A.time, "sleep"):
            rec = A.send_call(spec)
        self.assertAlmostEqual(rec["cost_usd"], 3 * wc)                     # timeouts at worst case
        with mock.patch.object(A, "_invoke", return_value=(None, 1, "BadRequestError: 400")), \
                mock.patch.object(A.time, "sleep"):
            rec = A.send_call(spec)
        self.assertAlmostEqual(rec["cost_usd"], 0.0)                         # a 4xx is not billed

    def test_empty_resend_chain_counts_both(self):
        spec = self._spec("gemini-4-argon")
        empty = {"text": "", "served_model": "gemini-4-argon", "finish_reason": "STOP", "tokens_in": 10,
                 "tokens_out": 0, "tokens_thought": 0}
        with mock.patch.object(A, "_invoke", side_effect=[(empty, 1, None), (None, 2, "transient: 503")]), \
                mock.patch.object(A.time, "sleep"):
            rec = A.send_call(spec)
        wc = BG.worst_case("gemini-4-argon", "S0", "standard", rec["started_utc"])
        self.assertAlmostEqual(rec["cost_usd"], 2 * wc + 10 * BG.prices("gemini-4-argon", "standard", rec["started_utc"])[0] / 1e6)

    def test_batch_errored_or_expired_costed_at_worst_case(self):
        specs = [s for s in A.build_specs(A.load_probes()) if s["model"]["mode"] == "batch"][:2]

        class Batches:
            def create(self, requests):
                self.ids = [r["custom_id"] for r in requests]
                return types.SimpleNamespace(id="b1")

            def retrieve(self, bid):
                return types.SimpleNamespace(id=bid, processing_status="ended", ended_at=None)

            def results(self, bid):
                return [types.SimpleNamespace(custom_id=c, result=types.SimpleNamespace(type="expired"))
                        for c in self.ids]

        client = types.SimpleNamespace(messages=types.SimpleNamespace(batches=Batches()))
        with tempfile.TemporaryDirectory() as d, mock.patch.object(A, "MAX_ATTEMPTS", 1):
            ledger = BG.Ledger(Path(d) / "raw.jsonl", Path(d) / "s.json")
            recs = []
            A.run_anthropic_batch(specs, ledger, recs.append, client=client, poll=0)
            self.assertEqual(len(recs), 2)
            self.assertAlmostEqual(recs[0]["cost_usd"], BG.worst_case("claude-fable-5-2", "S0", "batch"))

    def test_openai_page_opens_are_billed_searches(self):
        out = {"tokens_in": 0, "tokens_out": 0, "tokens_thought": 0,
               "search": {"n_searches": 2, "sources": [{"url": "u1", "action": "open_page"},
                                                       {"url": "u2", "action": "find_in_page"}, {"url": "u3"}]}}
        part = A._part(out, "standard", "S1")
        self.assertEqual(part["n_searches"], 4)
        self.assertAlmostEqual(BG.part_cost("gpt-6-astra", part, "2026-11-29"), 4 * 0.010)
        self.assertEqual(A._part(out, "standard", "S0")["n_searches"], 0)

    def test_gemini_tool_tokens_worst_when_missing(self):
        part = {"mode": "standard", "input_tokens": 0, "output_tokens": 0, "n_searches": 1, "tool_tokens": None}
        pin = BG.prices("gemini-4-argon", "standard", "2026-12-01")[0]
        self.assertAlmostEqual(BG.part_cost("gemini-4-argon", part, "2026-12-01"),
                               BG.WORST["S1_input_tokens"] * pin / 1e6 + 0.014)
        part["tool_tokens"] = 1000
        self.assertAlmostEqual(BG.part_cost("gemini-4-argon", part, "2026-12-01"), 1000 * pin / 1e6 + 0.014)

    def test_sync_call_reserves_two_worst_cases(self):
        spec = self._spec("gpt-6-astra")
        seen = []

        class L:
            def reserve(self, amount):
                seen.append(amount)
                return "stop", None
        A.run_sync([spec], L(), lambda r: None)
        self.assertAlmostEqual(seen[0], 2 * BG.worst_case("gpt-6-astra", "S0", "standard"))
        self.assertAlmostEqual(BG.sync_reservation("gemini-4-argon", "S0", "2026-12-01"), 2 * 0.3357, places=4)

    def test_extras_off_by_default(self):
        self.assertFalse(P.BRAND_EXTRAS)
        self.assertFalse(A.extras_on())
        self.assertEqual(P.LANGS, ("es", "ko", "zh"))


class R3ProjectionPauseCoreOnly(unittest.TestCase):
    """r3: with the extras off, the projection pause after block 1 (ratio 3.0) must stay on (section 6.5 rule 5).
    r2's collect() recorded a 'drop_phase_a' approval, and run_collection skips the projection pause once it exists.
    r3 update: these tests keep testing the core-only configuration (option (a) of section 9 item 7), so they switch
    params_v0_62.BRAND_YES_NO off; the adopted configuration (b) is tested in R3UpdateYesNoBlockLast below."""

    def setUp(self):
        patcher = mock.patch.object(P, "BRAND_YES_NO", False)
        patcher.start()
        self.addCleanup(patcher.stop)

    def _runner(self, usd_per_call, sent):
        def runner(group, ledger, write):
            for s in group:
                st, tok = ledger.reserve(0.01)
                if st != "ok":
                    return st
                m = s["model"]
                price = 50.0 if m["model_id"] == "gpt-6-astra" else (20.0 if m["mode"] == "batch" else 10.0)
                rec = fake_rec(s, (0, int(round(usd_per_call / price * 1e6))))
                sent.append(s["call_id"])
                write(rec)
                ledger.settle(tok, rec["cost_usd"])
            return "done"
        return runner

    def test_collection_specs_record_no_approval(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = BG.Ledger(Path(d) / "raw.jsonl", Path(d) / "s.json", judge_reserve=0.0)
            specs = A.collection_specs(ledger)
            self.assertEqual(len(specs), 810)
            self.assertEqual({A.BLOCKS[s["block"]][0] for s in specs}, {"B"})
            self.assertFalse(ledger.approved("drop_phase_a"))
            self.assertFalse((Path(d) / "s.json").exists())
            with mock.patch.object(P, "BRAND_EXTRAS", True):
                self.assertEqual(len(A.collection_specs(ledger)), 1818)
            ledger.approve("drop_phase_a", "pre-registrant's fallback F1")
            with mock.patch.object(P, "BRAND_EXTRAS", True):
                self.assertEqual(len(A.collection_specs(ledger)), 810)
        src = A.inspect.getsource(A.collect)
        self.assertIn("collection_specs(ledger)", src)
        self.assertNotIn('approve("drop_phase_a"', src)

    def test_core_only_projection_pause_after_block_1(self):
        with tempfile.TemporaryDirectory() as d:
            raw, state = Path(d) / "raw.jsonl", Path(d) / "s.json"
            ledger = BG.Ledger(raw, state, judge_reserve=0.0)
            specs = A.collection_specs(ledger)
            ratio = A.projection_ratio(when_utc="2026-12-01T00:00:00")
            self.assertEqual(ratio, 3.0)
            sent = []
            # block 1: 270 x $0.11 = $29.70; x 3.0 = $89.10 > $80 -> pause before block 2 (conservative-high shape)
            run = self._runner(0.11, sent)
            st = A.run_collection(specs, ledger, raw, {"batch": run, "standard": run}, ratio, log=lambda *a: None)
            self.assertEqual(st, "pause")
            self.assertEqual(len(sent), 270)
            self.assertIn("projection", ledger.halt_reason)
            self.assertAlmostEqual(ledger.calls_spent(), 29.70, places=4)

    def test_core_only_no_pause_at_central(self):
        with tempfile.TemporaryDirectory() as d:
            raw, state = Path(d) / "raw.jsonl", Path(d) / "s.json"
            ledger = BG.Ledger(raw, state, judge_reserve=0.0)
            specs = A.collection_specs(ledger)
            sent = []
            run = self._runner(0.0413, sent)          # about r3's central per call (block 1 $11.15 / 270)
            st = A.run_collection(specs, ledger, raw, {"batch": run, "standard": run}, 3.0, log=lambda *a: None)
            self.assertEqual(st, "done")
            self.assertEqual(len(sent), 810)

    def test_dry_run_prints_the_core_cost(self):
        lines = []
        A.dry_run(out=lines.append)
        text = "\n".join(lines)
        self.assertIn("cost estimate [core_nov]: 810 calls", text)
        self.assertIn("not counted: block 5 is not collected", text)
        self.assertIn("x 3.0000 (Nov) / x 3.0000 (Dec)", text)


class R3UpdateYesNoBlockLast(unittest.TestCase):
    """r3 update (pre-registrant's decision 2026-11-12 00:48 CT, section 9 item 7 (b)): the 88 yes/no brand questions
    (block 4) are collected LAST, after the three category-question runs, under the same $80 pause and $100 stop;
    block 5 (v0.23 open questions, recognition judge) is not collected. Local fakes only."""

    def _runner(self, usd, sent):
        """usd: {block kind: US$ per call}; every call reserves $0.01 like the r3 tests' runner."""
        def runner(group, ledger, write):
            for s in group:
                st, tok = ledger.reserve(0.01)
                if st != "ok":
                    return st
                m = s["model"]
                price = 50.0 if m["model_id"] == "gpt-6-astra" else (20.0 if m["mode"] == "batch" else 10.0)
                rec = fake_rec(s, (0, int(round(usd[A.BLOCKS[s["block"]][0]] / price * 1e6))))
                sent.append(s)
                write(rec)
                ledger.settle(tok, rec["cost_usd"])
            return "done"
        return runner

    def _ledger(self, d):
        return BG.Ledger(Path(d) / "raw.jsonl", Path(d) / "s.json", judge_reserve=0.0)

    def test_parameters_as_decided(self):
        self.assertTrue(P.BRAND_YES_NO)
        self.assertFalse(P.BRAND_EXTRAS)
        self.assertEqual((A.yes_no_on(), A.open_on(), A.design_key()), (True, False, "core_plus_yn"))
        src = A.inspect.getsource(A.collect)
        self.assertIn("JUDGE_RESERVE_USD if open_on() else 0.0", src)        # no judge reserve without block 5
        with mock.patch.object(P, "BRAND_YES_NO", False):
            self.assertEqual((A.yes_no_on(), A.design_key()), (False, "core"))
        with mock.patch.object(P, "BRAND_EXTRAS", True):
            self.assertEqual((A.yes_no_on(), A.open_on(), A.design_key()), (True, True, "full"))

    def test_collection_specs_block_4_last_no_block_5_no_approval(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = self._ledger(d)
            specs = A.collection_specs(ledger)
            self.assertEqual(len(specs), 1602)
            kinds = [A.BLOCKS[s["block"]][0] for s in specs]
            self.assertEqual(kinds, ["B"] * 810 + ["A_yn"] * 792)                 # block 4 strictly after blocks 1-3
            yn = specs[810:]
            self.assertEqual({s["substrate"] for s in yn}, {"v19", "v20", "v21", "v22"})
            self.assertFalse([s for s in specs if s["substrate"] == "v23" and s["phase"] == "A"])
            self.assertEqual(collections_count(yn), {(m["model_id"], lg): 88 for m in A.PANEL for lg in A.LANGS})
            self.assertEqual({s["run"] for s in yn}, {1})
            self.assertFalse((Path(d) / "s.json").exists())                      # no approval recorded
            self.assertEqual(A.expected_total(A.load_probes(), drop_open=True), 1602)
            ledger.approve("drop_run3", "fallback F2")
            self.assertEqual(len(A.collection_specs(ledger)), 1332)               # run 3 dropped, block 4 kept
            ledger.approve("drop_phase_a", "fallback F1")
            self.assertEqual(len(A.collection_specs(ledger)), 540)

    def test_projection_ratio_is_core_plus_block_4(self):
        j3 = json.loads(Path(A.COST_PATH).read_text(encoding="utf-8"))
        nov = A.projection_ratio(when_utc="2026-11-29T06:00:00")
        dec = A.projection_ratio(when_utc="2026-12-01T00:00:00")
        self.assertAlmostEqual(nov, j3["projection_core_plus_yn"]["A"]["nov"])
        self.assertAlmostEqual(dec, j3["projection_core_plus_yn"]["A"]["dec"])
        self.assertEqual((round(nov, 4), round(dec, 4)), (3.0975, 3.0887))       # pre-registration section 6.5
        self.assertAlmostEqual(j3["projection_core_plus_yn"]["A"]["nov"], j3["projection_by_design"]["core_plus_yn"]["nov"])

    def test_projection_pause_after_block_1(self):
        with tempfile.TemporaryDirectory() as d:
            raw, ledger = Path(d) / "raw.jsonl", self._ledger(d)
            specs, sent = A.collection_specs(ledger), []
            run = self._runner({"B": 0.11, "A_yn": 0.004}, sent)                    # block 1 $29.70 x 3.0887 > $80
            st = A.run_collection(specs, ledger, raw, {"batch": run, "standard": run},
                                  A.projection_ratio(when_utc="2026-12-01T00:00:00"), log=lambda *a: None)
            self.assertEqual((st, len(sent)), ("pause", 270))
            self.assertIn("projection", ledger.halt_reason)

    def test_central_completes_with_block_4_last(self):
        with tempfile.TemporaryDirectory() as d:
            raw, ledger = Path(d) / "raw.jsonl", self._ledger(d)
            specs, sent = A.collection_specs(ledger), []
            run = self._runner({"B": 0.0413, "A_yn": 0.00138}, sent)               # about r3's central per call
            st = A.run_collection(specs, ledger, raw, {"batch": run, "standard": run},
                                  A.projection_ratio(when_utc="2026-11-29T06:00:00"), log=lambda *a: None)
            self.assertEqual((st, len(sent)), ("done", 1602))
            kinds = [A.BLOCKS[s["block"]][0] for s in sent]
            self.assertLess(max(i for i, k in enumerate(kinds) if k == "B"), min(i for i, k in enumerate(kinds) if k == "A_yn"))
            self.assertLess(ledger.spent(), BG.PAUSE_AT_USD)

    def test_block_4_never_takes_budget_from_the_category_runs(self):
        """Conservative-high shape: the $100 stop falls inside block 3, so no yes/no question is sent."""
        with tempfile.TemporaryDirectory() as d:
            raw, ledger = Path(d) / "raw.jsonl", self._ledger(d)
            ledger.approve("projection", "test: continue after block 1")
            ledger.approve("past_80", "test: continue past $80")
            specs, sent = A.collection_specs(ledger), []
            self.assertEqual(len(specs), 1602)                                    # approvals drop nothing
            run = self._runner({"B": 0.15, "A_yn": 0.004}, sent)                    # $40.50 per category run
            st = A.run_collection(specs, ledger, raw, {"batch": run, "standard": run}, 3.0887, log=lambda *a: None)
            self.assertEqual(st, "stop")
            self.assertFalse([s for s in sent if A.BLOCKS[s["block"]][0] == "A_yn"])
            self.assertTrue([s for s in sent if s["block"] == 2])                 # the stop falls inside block 3

    def test_dry_run_prints_the_adopted_design(self):
        lines = []
        A.dry_run(out=lines.append)
        text = "\n".join(lines)
        self.assertIn("yes/no brand questions (params BRAND_YES_NO; block 4, last): ON -> calls sent: 1602", text)
        self.assertIn("cost estimate [core_plus_yn_nov]: 1602 calls, central $34.52", text)
        self.assertIn("cost estimate [core_plus_yn_dec]: 1602 calls, central $39.98, high $124.77", text)
        self.assertIn("x 3.0975 (Nov) / x 3.0887 (Dec)", text)
        self.assertIn("not counted: block 5 is not collected", text)


def _fable_msg():
    return types.SimpleNamespace(content=[types.SimpleNamespace(type="text", text="Sí.", citations=None)],
                                 usage=types.SimpleNamespace(input_tokens=100, output_tokens=1000),
                                 model="claude-fable-5-2", stop_reason="end_turn")


class FakeBatchClient:
    """Local fake of the Message Batches API (no network): every request succeeds with 100 / 1,000 tokens."""

    def __init__(self):
        self.n_created, self.store = 0, {}
        self.batches = types.SimpleNamespace(create=self._create, retrieve=self._retrieve, results=self._results)
        self.messages = types.SimpleNamespace(batches=self.batches)

    def _create(self, requests):
        self.n_created += 1
        bid = f"batch_{self.n_created}"
        self.store[bid] = [r["custom_id"] for r in requests]
        return types.SimpleNamespace(id=bid, processing_status="in_progress")

    def _retrieve(self, bid):
        return types.SimpleNamespace(id=bid, processing_status="ended", ended_at=None)

    def _results(self, bid):
        return [types.SimpleNamespace(custom_id=c, result=types.SimpleNamespace(type="succeeded", message=_fable_msg()))
                for c in self.store[bid]]


class PreLockBatchJournal(unittest.TestCase):
    """Pre-lock correction (coordinator, 2026-11-12): record of Message Batches in flight, ported from v0.42's
    acquire_v0_42.py (C26 (ii)) and its tests (test_interrupted_batch_is_recovered_once_and_costed,
    test_journal_marks_normal_batches_recorded): a stop mid-batch can neither re-send nor leave spend unrecorded."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.raw, self.journal = Path(self.tmp.name) / "raw.jsonl", Path(self.tmp.name) / "batches.jsonl"
        self.write = A.make_writer(self.raw, log=lambda *a: None)

    def ledger(self):
        return BG.Ledger(self.raw, Path(self.tmp.name) / "s.json", judge_reserve=0.0)

    def written(self):
        return [json.loads(x) for x in self.raw.read_text(encoding="utf-8").splitlines()] if self.raw.exists() else []

    def specs(self, n):
        return [s for s in A.build_specs(A.load_probes()) if s["model"]["mode"] == "batch"][:n]

    def test_journal_marks_normal_batches_recorded(self):
        st = A.run_anthropic_batch(self.specs(2), self.ledger(), self.write, client=FakeBatchClient(), poll=0,
                                   sleep=lambda s: None, journal=self.journal)
        self.assertEqual(st, "done")
        self.assertEqual([json.loads(x)["event"] for x in self.journal.read_text().splitlines()], ["created", "recorded"])
        self.assertEqual(A.open_batches(self.journal), [])
        self.assertEqual(len(self.written()), 2)

    def test_interrupted_batch_is_recovered_once_and_costed(self):
        client = FakeBatchClient()
        real_retrieve = client.batches.retrieve

        def killed(bid):
            raise KeyboardInterrupt("run stopped while the batch was in flight")
        client.batches.retrieve = killed
        specs = self.specs(3)
        with self.assertRaises(KeyboardInterrupt):
            A.run_anthropic_batch(specs, self.ledger(), self.write, client=client, poll=0, sleep=lambda s: None,
                                  journal=self.journal)
        self.assertEqual(self.written(), [])                            # billed, nothing recorded yet
        self.assertEqual([e["batch_id"] for e in A.open_batches(self.journal)], ["batch_1"])
        # a line of the batch already written before the stop is not written again
        client.batches.retrieve = real_retrieve
        first = A.open_batches(self.journal)[0]["requests"][0]
        self.write(A._record(specs[0], {"text": "x", "served_model": "claude-fable-5-2", "finish_reason": "end_turn",
                                        "tokens_in": 1000, "tokens_out": 200, "tokens_thought": None,
                                        "paused_continued": False, "search": None}, "ok", None, 1, False, "t0", "t1", [],
                             {"batch_id": "batch_1", "custom_id": first["custom_id"]}))
        L = self.ledger()
        n = A.recover_batches(specs, L, self.write, self.journal, self.raw, client=client, poll=0, sleep=lambda s: None,
                              log=lambda *a: None)
        self.assertEqual(n, 1)
        self.assertEqual(client.n_created, 1)                           # nothing re-sent
        recs = [r for r in self.written() if r.get("batch_id") == "batch_1"]
        self.assertEqual(len(recs), 3)
        self.assertEqual(len({r["custom_id"] for r in recs}), 3)
        self.assertAlmostEqual(L.calls_spent(), 2 * (100 * 4 + 1000 * 20) / 1e6, places=12)   # the two recovered lines
        self.assertEqual(A.open_batches(self.journal), [])
        self.assertEqual(A.recover_batches(specs, L, self.write, self.journal, self.raw, client=client, poll=0,
                                           sleep=lambda s: None, log=lambda *a: None), 0)
        self.assertTrue({s["call_id"] for s in specs} <= A.done_ids(self.raw))   # a resumed run sends none of them

    def test_collect_recovers_before_any_new_request(self):
        src = A.inspect.getsource(A.collect)
        self.assertIn("recover_batches(", src)
        self.assertLess(src.index("recover_batches("), src.index("run_collection("))
        self.assertIn("partial(run_anthropic_batch, journal=BATCH_LOG)", src)
        self.assertEqual(A.BATCH_LOG.name, "v62_batches.jsonl")


def collections_count(specs):
    out = {}
    for s in specs:
        k = (s["model"]["model_id"], s["language"])
        out[k] = out.get(k, 0) + 1
    return out


if __name__ == "__main__":
    unittest.main()
