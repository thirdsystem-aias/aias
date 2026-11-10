#!/usr/bin/env python3
"""Tests for judge_v1_11.py: request parameters, cost guard, windows, plan, resumable run with a fake
judge in a temporary folder, freeze. No network, no provider SDK import.
Run from the repo root:  python3 -m unittest scripts/test_score_v1_11.py scripts/test_judge_v1_11.py"""
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import judge_v1_11 as J  # noqa: E402
import score_v1_11 as S  # noqa: E402

UTC = timezone.utc


def tiny_units(n_r=6, n_f=40, n_e=60):
    units = []
    for blk, n, cat, wave, st in (("R", n_r, "v0.23", "t1", "R t1 v0.23"), ("F", n_f, "v0.20", "t1", "OMNI t1 v0.20"),
                                  ("E", n_e, "pm", "v0.9", "EARLY-6 v0.9 pm")):
        for i in range(n):
            u = {"unit_id": f"{blk}{i:03d}", "block": blk, "set": st, "panel": "P", "wave": wave, "category": cat,
                 "category_label": S.CATEGORY_LABELS[cat], "brand": f"b{i % 4}", "brand_display": f"Brand{i % 4}",
                 "model": f"m{i % 6}", "provider": "anthropic", "frame": f"f{i % 6}", "channel": "", "run_idx": "",
                 "answer_id": f"a{blk}{i}", "unit_type": "recognition" if blk == "R" else "mention",
                 "question": "Which brands?", "text": f"Brand{i % 4} is described here.", "chars": 30, "cut": False,
                 "bare": False, "judged": True, "j2": blk != "E" or i % 10 == 0, "selfcon": i % 10 == 1, "human": False}
            u["request_chars"] = len(S.build_request(u)["system"]) + len(S.build_request(u)["user"])
            units.append(u)
    return units


def temp_paths(d: Path, units) -> J.Paths:
    P = J.Paths(dry=True)
    for k, name in (("units", S.UNITS_NAME), ("u0", S.U0_NAME), ("raw", S.RAW_NAME), ("plan", J.PLAN_NAME),
                    ("roles", "roles_v1_11.json"), ("guard_log", J.GUARD_LOG_NAME), ("frozen", S.FROZEN_NAME),
                    ("dry_txt", "dry.txt"), ("cost_json", "cost.json"), ("batches", "batches.jsonl")):
        setattr(P, k, d / name)
    P.prereg = P.data = P.out = d
    b = S.units_csv_bytes(units)
    P.units.write_bytes(b)
    P.u0.write_text(json.dumps({"units_file": {"sha256": S.V.sha256_bytes(b)}}))
    return P


class TestRequests(unittest.TestCase):
    def test_no_sampling_parameters_and_lowest_effort(self):
        for key in ("J1", "J2", "ALT"):
            m = S.JUDGES[key]["model_id"]
            kw = J.request_kwargs(m, S.JUDGES[key]["provider"], "SYS", "USER")
            self.assertEqual(J.sampling_params_sent(kw), [])
            flat = json.dumps(kw)
            for w in ("temperature", "top_p", "top_k"):
                self.assertNotIn(w, flat)
            self.assertIn('"low"', flat)
            self.assertIn(str(S.MAX_OUTPUT_TOKENS), flat)
            self.assertIn("SYS", flat)
        a = J.request_kwargs("claude-opus-5-5", "anthropic", "S", "U")
        self.assertEqual(a["output_config"], {"effort": "low"})
        self.assertEqual(a["max_tokens"], 4096)
        o = J.request_kwargs("gpt-6.1-sol", "openai", "S", "U")
        self.assertEqual(o["reasoning"], {"effort": "low"})
        self.assertEqual(o["max_output_tokens"], 4096)
        g = J.request_kwargs("gemini-4-argon", "google", "S", "U")
        self.assertEqual(g["config"]["thinking_config"], {"thinking_level": "low"})

    def test_params_record_keeps_every_parameter_but_the_texts(self):
        kw = J.request_kwargs("claude-opus-5-5", "anthropic", "SYSTEM TEXT", "USER TEXT")
        r = J.params_record(kw)
        self.assertNotIn("USER TEXT", json.dumps(r))
        self.assertEqual(r["max_tokens"], S.MAX_OUTPUT_TOKENS)
        self.assertEqual(r["output_config"], {"effort": "low"})
        self.assertEqual(r["system"]["chars"], len("SYSTEM TEXT"))

    def test_worst_case_bounds_and_served_ok(self):
        when = datetime(2026, 11, 25, tzinfo=UTC)
        kw = J.request_kwargs("gpt-6.1-sol", "openai", "S" * 100, "U" * 4000)
        w = J.worst_usd("gpt-6.1-sol", "openai", kw, when, batch=True)
        self.assertGreater(w, J.actual_usd("gpt-6.1-sol", "openai", when, 1100, 500, 300, batch=True))
        self.assertAlmostEqual(J.worst_usd("gpt-6.1-sol", "openai", kw, when), 2 * w)          # batch = 50%
        self.assertAlmostEqual(w, (len(json.dumps(kw).encode()) * 1.0 + 4096 * 5.0) / 1e6)
        g = J.request_kwargs("gemini-4-argon", "google", "S", "U")
        self.assertGreater(J.worst_usd("gemini-4-argon", "google", g, when), 2 * 4096 * 10 / 1e6 - 1e-9)
        self.assertAlmostEqual(J.actual_usd("gemini-4-argon", "google", when, 0, 100, 50), 150 * 10 / 1e6)
        self.assertTrue(J.served_ok("gpt-6.1-sol", "gpt-6.1-sol"))
        self.assertTrue(J.served_ok("claude-opus-5-5", "claude-opus-5-5-20261020"))
        self.assertFalse(J.served_ok("gpt-6.1-sol", "gpt-6-astra"))
        self.assertFalse(J.served_ok("gpt-6.1-sol", None))
        self.assertTrue(J.is_batch("claude-opus-5-5") and J.is_batch("gpt-6.1-sol"))
        self.assertFalse(J.is_batch("gemini-4-argon"))

    def test_batch_parsers_and_custom_id(self):
        a = J.parse_anthropic_message({"model": "claude-opus-5-5", "stop_reason": "end_turn",
                                       "content": [{"type": "thinking", "thinking": "x"}, {"type": "text", "text": "{}"}],
                                       "usage": {"input_tokens": 10, "cache_read_input_tokens": 5, "output_tokens": 70}})
        self.assertEqual((a["text"], a["tokens_in"], a["tokens_out"], a["thinking_blocks"]), ("{}", 15, 70, 1))
        o = J.parse_openai_response({"model": "gpt-6.1-sol", "status": "incomplete",
                                     "incomplete_details": {"reason": "max_output_tokens"},
                                     "output": [{"type": "reasoning"}, {"type": "message", "content": [
                                         {"type": "output_text", "text": "{\"a\""}]}],
                                     "usage": {"input_tokens": 9, "output_tokens": 4096,
                                               "output_tokens_details": {"reasoning_tokens": 4090}}})
        self.assertEqual((o["text"], o["finish_reason"], o["tokens_thought"]),
                         ('{"a"', "incomplete:max_output_tokens", 4090))
        cid = J.custom_id("J2", "EARLY-6 v0.9 pm::gpt-5.5|p1|1#Asana", "repeat", 3)
        self.assertRegex(cid, r"^[A-Za-z0-9_-]{1,64}$")
        self.assertNotEqual(cid, J.custom_id("J2", "EARLY-6 v0.9 pm::gpt-5.5|p1|1#Asana", "repeat", 2))

    def test_batch_blackout_window(self):
        self.assertIsNotNone(J.blackout_within(datetime(2026, 11, 10, 18, tzinfo=UTC)))   # t4 starts within 24 h
        self.assertIsNotNone(J.blackout_within(datetime(2026, 11, 21, 12, tzinfo=UTC)))
        self.assertIsNone(J.blackout_within(datetime(2026, 11, 22, 6, tzinfo=UTC)))
        g = J.Guard(0.0, 0, None)
        with self.assertRaises(J.GuardStop):
            g.reserve_batch([0.01], datetime(2026, 11, 10, 18, tzinfo=UTC))
        self.assertIn("blackout", g.stopped)

    def test_real_batch_client_builds_no_network_object_at_init(self):
        bc = J.RealBatchClient()
        self.assertEqual(bc._c, {})
        for m in ("anthropic", "openai"):
            self.assertNotIn(m, sys.modules)

    def test_call_functions_send_no_sampling_parameter(self):
        import inspect
        for f in list(J.DISPATCH.values()) + [J.RealBatchClient, J.batch_worker, J.collect_batch]:
            src = inspect.getsource(f)
            for w in ("temperature", "top_p", "top_k"):
                self.assertNotIn(w, src)


class TestGuardAndWindows(unittest.TestCase):
    def test_blackouts(self):
        self.assertIsNotNone(J.in_blackout(datetime(2026, 11, 12, tzinfo=UTC)))
        self.assertIsNotNone(J.in_blackout(datetime(2026, 11, 15, 12, tzinfo=UTC)))
        self.assertIsNotNone(J.in_blackout(datetime(2026, 11, 19, tzinfo=UTC)))
        self.assertIsNotNone(J.in_blackout(datetime(2026, 11, 22, 3, tzinfo=UTC)))     # Nov 21, 9 pm CT
        self.assertIsNone(J.in_blackout(datetime(2026, 11, 22, 12, tzinfo=UTC)))
        self.assertIsNone(J.in_blackout(datetime(2026, 11, 10, 20, tzinfo=UTC)))

    def test_guard_refuses_in_blackout_unless_simulated(self):
        g = J.Guard(0.0, 0, None)
        with self.assertRaises(J.GuardStop):
            g.reserve(0.01, datetime(2026, 11, 19, tzinfo=UTC))
        g2 = J.Guard(0.0, 0, None, sim=True)
        g2.reserve(0.01, datetime(2026, 11, 19, tzinfo=UTC))

    def test_guard_pause_at_80_and_cap_at_100(self):
        g = J.Guard(79.99, 0, None, sim=True)
        g.reserve(0.5, datetime(2026, 11, 25, tzinfo=UTC))
        g.settle(0.5, 0.02)
        with self.assertRaises(J.GuardStop):
            g.reserve(0.5, datetime(2026, 11, 25, tzinfo=UTC))
        self.assertIn("PAUSED", g.stopped)
        g3 = J.Guard(99.5, 0, "Pablo, test", sim=True)
        with self.assertRaises(J.GuardStop):
            g3.reserve(0.9, datetime(2026, 11, 25, tzinfo=UTC))
        self.assertIn("CAP", g3.stopped)

    def test_batch_reservation_cuts_to_the_cap_and_waits_for_flight(self):
        when = datetime(2026, 11, 25, tzinfo=UTC)
        g = J.Guard(90.0, 0, "Pablo, test", sim=True)
        self.assertEqual(g.reserve_batch([0.03125] * 500, when), 320)     # 90 + 320 / 32 = 100 (exact in binary)
        self.assertEqual(g.reserve_batch([0.03125] * 10, when), 0)        # none fits; a batch is in flight: wait
        self.assertIsNone(g.stopped)
        g.settle(10.0, 0.5)                                               # that batch is collected
        self.assertGreater(g.reserve_batch([0.03125] * 10, when), 0)
        g2 = J.Guard(99.99, 0, "Pablo, test", sim=True)
        with self.assertRaises(J.GuardStop):                             # nothing in flight: the cap stops it
            g2.reserve_batch([0.04], when)
        self.assertIn("CAP", g2.stopped)
        g3 = J.Guard(80.0, 0, None, sim=True)
        with self.assertRaises(J.GuardStop):
            g3.reserve_batch([0.01], when)
        self.assertIn("PAUSED", g3.stopped)

    def test_other_collection_pattern(self):
        self.assertTrue(J.OTHER_COLLECTION.search("python3 osf/v42/scripts/acquire_v0_42.py --collect"))
        self.assertTrue(J.OTHER_COLLECTION.search("python3 osf/methodology/v1_12/scripts/acquire_v1_12.py --collect"))
        self.assertFalse(J.OTHER_COLLECTION.search("python3 scripts/judge_v1_11.py --run"))


class TestPlanAndRun(unittest.TestCase):
    def test_jobs_order_and_membership(self):
        units = tiny_units()
        jobs, by = J.jobs_for(units, S.DEFAULT_PLAN)
        self.assertEqual(jobs, J.jobs_for(units, S.DEFAULT_PLAN)[0])
        a = [j for j in jobs if j["phase"] == "A"]
        self.assertTrue(all(by[j["unit_id"]]["block"] in ("R", "F") for j in a))
        self.assertTrue(all(by[j["unit_id"]]["j2"] for j in jobs if j["role"] == "J2"))
        self.assertTrue(all(by[j["unit_id"]]["selfcon"] and j["pass"] == "repeat" for j in jobs if j["phase"] in ("A2", "B2")))
        self.assertEqual(len([j for j in jobs if j["phase"] == "B" and j["role"] == "J1"]), 60)
        self.assertEqual([j["phase"] for j in jobs], sorted([j["phase"] for j in jobs], key=J.PHASES.index))

    def test_choose_plan_applies_reductions_in_order(self):
        units = tiny_units(n_e=600)
        ipc = {"J1": 0.25, "J2": 0.25}
        p = J.choose_plan(units, J.DEFAULT_ROLES, ipc, {"J1": 100, "J2": 100}, datetime(2026, 11, 25, tzinfo=UTC))
        self.assertEqual(p["reductions_applied"], [])
        tight = J.choose_plan(units, J.DEFAULT_ROLES, ipc, {"J1": 100, "J2": 100}, datetime(2026, 11, 25, tzinfo=UTC),
                              cap=p["steps"][0]["usd_with_overhead"] * 0.6)
        self.assertGreater(len(tight["reductions_applied"]), 0)
        self.assertEqual(tight["reductions_applied"], [f"{k}={v}" for k, v in S.REDUCTION_ORDER][:len(tight["reductions_applied"])])

    def test_resumable_run_retry_freeze_and_refusal(self):
        with tempfile.TemporaryDirectory() as d:
            units = tiny_units()
            P = temp_paths(Path(d), units)
            fake = J.FakeJudge()
            disp = {k: fake(k) for k in ("anthropic", "openai", "google")}
            bc = J.FakeBatchClient(fake)
            with self.assertRaises(RuntimeError):                        # batch judges need a batch client
                J.run(P, disp, sim=True, max_new_calls=1, log=lambda *a: None)
            for p in (P.raw, P.batches, P.guard_log):
                if p.exists():
                    p.unlink()
            rc1 = J.run(P, disp, sim=True, max_new_calls=30, log=lambda *a: None, bc=bc)
            self.assertEqual(rc1, 4)
            n1 = len(J.read_raw(P.raw))
            self.assertEqual(n1, 30)
            rc2 = J.run(P, disp, sim=True, log=lambda *a: None, bc=bc)
            self.assertEqual(rc2, 0)
            self.assertTrue(all(r["mode"] == "batch" for r in J.read_raw(P.raw)))
            self.assertEqual(J.open_batches(P), [])
            recs = J.read_raw(P.raw)
            jobs, by = J.jobs_for(units, json.loads(P.plan.read_text())["params"])
            st = J.state_from(recs, J.DEFAULT_ROLES)
            self.assertTrue(all(J.done(st[(j["role"], j["unit_id"], j["pass"])]) for j in jobs))
            keys = [(r["role"], r["unit_id"], r["pass"], r["attempt"]) for r in recs]
            self.assertEqual(len(keys), len(set(keys)))                      # no call sent twice
            self.assertTrue(all(r["sampling_parameters_sent"] == [] for r in recs))
            self.assertTrue(all("request" in r and "max_tokens" in json.dumps(r["request"]) or
                                "max_output_tokens" in json.dumps(r["request"]) for r in recs))
            self.assertEqual(J.run(P, disp, sim=True, log=lambda *a: None, bc=bc), 0)   # nothing left: no new call
            self.assertEqual(len(J.read_raw(P.raw)), len(recs))
            self.assertEqual(J.freeze(P, log=lambda *a: None), 0)
            fr = json.loads(P.frozen.read_text())
            self.assertEqual(fr["raw_sha256"], S.V.sha256(P.raw))
            self.assertEqual(fr["batches_sha256"], S.V.sha256(P.batches))
            self.assertEqual(J.run(P, disp, sim=True, log=lambda *a: None, bc=bc), 3)   # frozen -> refused
            oc = S.outcomes(recs, fr["roles"])
            self.assertTrue(all(v["status"] in (S.VALID, S.FAIL, S.UNJUDGED) for v in oc.values()))
            self.assertLessEqual(sum(v["status"] == S.UNJUDGED for v in oc.values()), 1)

    def test_interrupted_batch_is_reattached_not_resent(self):
        with tempfile.TemporaryDirectory() as d:
            units = tiny_units()
            P = temp_paths(Path(d), units)
            fake = J.FakeJudge()
            disp = {k: fake(k) for k in ("anthropic", "openai", "google")}
            bc = J.FakeBatchClient(fake, polls=3, interrupt_after=1)
            self.assertEqual(J.run(P, disp, sim=True, log=lambda *a: None, bc=bc), 4)
            self.assertGreaterEqual(len(J.open_batches(P)), 1)            # left in flight
            self.assertEqual(J.freeze(P, log=lambda *a: None), 3)       # cannot freeze with a batch in flight
            self.assertEqual(J.run(P, disp, sim=True, log=lambda *a: None), 5)   # in flight, no client: refused
            self.assertEqual(J.run(P, disp, sim=True, log=lambda *a: None, bc=bc), 0)
            self.assertEqual(J.open_batches(P), [])
            sent = [cid for cid in bc.submitted]
            self.assertEqual(len(sent), len(set(sent)))                 # no request id submitted twice
            recs = J.read_raw(P.raw)
            self.assertEqual(len(recs), len(sent))                      # one record per submitted request
            self.assertIn("re-attached in-flight batches", P.guard_log.read_text())

    def test_pause_and_approval_in_batch_mode(self):
        with tempfile.TemporaryDirectory() as d:
            units = tiny_units()
            P = temp_paths(Path(d), units)
            P.raw.write_text(json.dumps({"role": "J1", "judge_model": "claude-opus-5-5", "unit_id": "zz",
                                         "pass": "main", "attempt": 1, "status": "ok", "valid": False,
                                         "usd": 80.0, "plan_phase": "A"}) + "\n")   # recorded spend at the pause
            fake = J.FakeJudge()
            disp = {k: fake(k) for k in ("anthropic", "openai", "google")}
            bc = J.FakeBatchClient(fake)
            self.assertEqual(J.run(P, disp, sim=True, log=lambda *a: None, bc=bc), 4)
            self.assertEqual(bc.n_submits, 0)
            self.assertIn("PAUSED", P.guard_log.read_text())
            self.assertEqual(J.run(P, disp, approval="Pablo, test", sim=True, log=lambda *a: None, bc=bc), 0)
            self.assertLessEqual(sum(float(r.get("usd") or 0) for r in J.read_raw(P.raw)), S.HARD_CAP_USD)

    def test_replacement_is_recorded_and_old_outputs_unused(self):
        with tempfile.TemporaryDirectory() as d:
            P = temp_paths(Path(d), tiny_units())
            J.replace(P, "J2=ALT", "test", log=lambda *a: None)
            self.assertEqual(J.current_roles(P)["J2"], "gemini-4-argon")
            self.assertEqual(json.loads(P.roles.read_text())["replacements"][0]["from"], "gpt-6.1-sol")

    def test_dry_run_imports_no_sdk(self):
        with tempfile.TemporaryDirectory() as d:
            P = temp_paths(Path(d), tiny_units())
            J.dry_run(P, log=lambda *a: None)
            for m in ("anthropic", "openai", "google.genai"):
                self.assertNotIn(m, sys.modules)
            cj = json.loads(P.cost_json.read_text())
            self.assertIn("break_even_reasoning_tokens_pause", cj)
            self.assertIn("CHOSEN, batch: J1 claude-opus-5-5 + J2 gpt-6.1-sol (J2: R, F and 10% of E)", cj["designs"])
            self.assertEqual(cj["endpoints"], {"J1": "batch", "J2": "batch"})


if __name__ == "__main__":
    unittest.main()
