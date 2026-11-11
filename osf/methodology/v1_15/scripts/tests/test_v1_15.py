#!/usr/bin/env python3
"""Tests for v1.15 (synthetic data and temporary directories only; no network, no model call).
Run from the repository root: python3 -m unittest osf/methodology/v1_15/scripts/tests/test_v1_15.py"""
import ast
import inspect
import json
import random
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import score_v1_15 as T  # noqa: E402
import judge_v1_15 as JV  # noqa: E402

S, V, J = T.S, T.V, JV.J
UTC = timezone.utc
CTX = type("Ctx", (), {"path": staticmethod(lambda rel: T.ROOT / rel)})()
PREREG = T.PREREG_DIR / "PRE_REGISTRATION_v1_15.md"
AI_USE = ("## Use of AI tools {-}\n\nDuring the preparation of this work the author used AI tools (Anthropic's "
          "Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and "
          "takes full responsibility for it.")


def git(*a):
    return subprocess.run(["git", "-C", str(T.ROOT), *a], capture_output=True, text=True).stdout


def registries():
    out = {}
    for sub in V.OMNI:
        reg, unit, _ = V.load_registry(CTX, *V.OMNI_REG[sub])
        out[sub] = (reg, unit)
    return out


REGS = registries()
SHORT = {v: k for k, v in T.SUB_MAP.items()}


def synth_records(seed=1, per_model_answered=202, brands_per_answer=5, miss_brand=None):
    """t4-format raw records: S0 Phase B (30 questions x 3 runs) and Phase A (112) per N3 model."""
    rng = random.Random(seed)
    recs = []
    for m in T.N3:
        n = 0
        for sub in V.OMNI:
            reg, unit = REGS[sub]
            names = sorted(reg)
            for q in range(6):
                for run in (1, 2, 3):
                    pick = rng.sample(names, brands_per_answer)
                    text = "Here are options.\n\n" + "\n".join(
                        f"{i + 1}. **{b}**: {'excellent and well reviewed' if rng.random() < .5 else 'a known name'}."
                        for i, b in enumerate(pick))
                    if miss_brand:
                        text = text.replace(miss_brand, "")
                    n += 1
                    ok = n <= per_model_answered
                    recs.append({"call_id": f"{SHORT[sub]}|B|q{q}|{m}|S0|{run}", "substrate": SHORT[sub],
                                 "phase": "B", "probe_id": f"q{q}", "frame_id": f"q{q}", "brand_id": None,
                                 "model_requested": m, "served_model": m, "condition": "S0", "run": run,
                                 "prompt": f"Question {q} about {sub}?", "text": text if ok else "",
                                 "status": "ok" if ok else "error", "error": None if ok else "x", "_pick": pick})
        for i in range(112):
            n += 1
            ok = n <= per_model_answered
            recs.append({"call_id": f"A|{i}|{m}|S0|1", "substrate": "v19", "phase": "A", "probe_id": f"a{i}",
                         "frame_id": None, "model_requested": m, "served_model": m, "condition": "S0", "run": 1,
                         "prompt": "yes or no?", "text": "yes" if ok else "", "status": "ok" if ok else "error",
                         "error": None if ok else "x"})
    return recs


def synth_coded(recs):
    out = {sub: [] for sub in V.OMNI}
    for r in recs:
        if r["phase"] != "B" or r["status"] != "ok":
            continue
        sub = T.SUB_MAP[r["substrate"]]
        reg, unit = REGS[sub]
        for canon, key in unit.items():
            out[sub].append({"call_id": r["call_id"], "condition": "S0", "brand": key,
                             "mentioned": "1" if canon in r["_pick"] else "0"})
    return out


class TestPins(unittest.TestCase):
    def test_v111_files_byte_identical_to_tag(self):
        for p, blob in T.V111_BLOBS.items():
            self.assertEqual(git("hash-object", str(T.ROOT / p)).strip(), blob, p)
            self.assertEqual(git("rev-parse", f"{T.V111_TAG}:{p}").strip(), blob, p)

    def test_v042_functions_verbatim(self):
        for path, names in T.V042_FUNCS.items():
            src = git("show", f"{T.V042_PRELOCK_COMMIT}:{path}")
            self.assertTrue(src, f"cannot read {path} at {T.V042_PRELOCK_COMMIT}")
            tree = ast.parse(src)
            for name in names:
                node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
                self.assertEqual(ast.get_source_segment(src, node), inspect.getsource(getattr(T, name)).rstrip(), name)

    def test_v042_constants(self):
        src = git("show", f"{T.V042_PRELOCK_COMMIT}:osf/v42/scripts/score_v0_42.py")
        self.assertIn('EXPECTED_PER_MODEL_COND = {"S0": 30 * 3 + 112', src)
        self.assertRegex(src, r"\nDROP_SHARE = 0\.90\b")
        self.assertIn('PHASE_A_DESIGN = {("S0", 1)}', src)


class TestDropRule(unittest.TestCase):
    def test_threshold_90pct(self):
        self.assertEqual(T.drop_rule_s0(synth_records(per_model_answered=182))["dropped_S0"], [])
        self.assertEqual(T.drop_rule_s0(synth_records(per_model_answered=181))["dropped_S0"], sorted(T.N3))

    def test_served_mismatch_and_dedupe(self):
        recs = synth_records()
        bad = dict(recs[0], served_model="claude-opus-5-5")
        retry = dict(recs[1], status="error", text="", error="x")     # a later failed attempt does not replace
        dr = T.drop_rule_s0([bad] + recs[1:] + [retry])
        self.assertIn(recs[0]["call_id"], dr["served_mismatch"])
        self.assertTrue(T.served_ok("gpt-6-astra", "gpt-6-astra-2026-10-01"))
        ans, _ = T.t4_answers([bad] + recs[1:] + [retry])
        ids = {a["call_id"] for v in ans.values() for a in v}
        self.assertNotIn(recs[0]["call_id"], ids)
        self.assertIn(recs[1]["call_id"], ids)

    def test_only_s0_phase_b(self):
        ans, _ = T.t4_answers(synth_records())
        self.assertEqual({k: len(v) for k, v in ans.items()}, {s: 54 for s in V.OMNI})


class TestUnits(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recs = synth_records()
        cls.ans, _ = T.t4_answers(cls.recs)
        cls.res = T.build_units_t4(cls.ans, synth_coded(cls.recs), CTX, log=lambda *a: None)

    def test_one_window_per_certified_mention(self):
        self.assertEqual(len(self.res["misses"]), 0)
        self.assertEqual(len(self.res["units"]), 270 * 5)
        u = self.res["units"][0]
        self.assertEqual((u["block"], u["wave"], u["panel"]), ("F", "t4", "N3"))

    def test_cap_36_and_samples(self):
        from collections import Counter
        judged = [u for u in self.res["units"] if u["judged"]]
        c = Counter((u["set"], u["brand"]) for u in judged)
        self.assertLessEqual(max(c.values()), 36)
        self.assertTrue(all(u["j2"] for u in judged))
        self.assertFalse(any(u["human"] for u in self.res["units"]))
        self.assertEqual(sum(u["selfcon"] for u in judged), S._k_of(0.05, len(judged)))

    def test_extraction_miss_halt(self):
        recs = synth_records()
        coded = synth_coded(recs)
        for r in recs:                                   # certified record names a brand the text no longer holds
            if r["phase"] == "B" and r["status"] == "ok" and r["substrate"] == "v20":
                r["text"] = "No brands named here."
        ans, _ = T.t4_answers(recs)
        with self.assertRaises(S.Halt):
            T.build_units_t4(ans, coded, CTX, log=lambda *a: None)

    def test_incomplete_coded_table_halts(self):
        coded = synth_coded(self.recs)
        coded["v0.21"] = coded["v0.21"][:-1]
        with self.assertRaises(S.Halt):
            T.build_units_t4(self.ans, coded, CTX, log=lambda *a: None)

    def test_request_is_v111s(self):
        u = self.res["units"][0]
        self.assertEqual(S.build_request(u), S.build_request(dict(u)))
        self.assertIn(u["brand_display"], S.build_request(u)["user"])


class TestCost(unittest.TestCase):
    def test_reproduces_preview_section_12(self):
        rep = T.cost_report()
        got = {(r["scenario"], r["tokens_in_o200k"], r["reasoning"]): round(r["usd_with_overhead"], 2) for r in rep["rows"]}
        self.assertEqual(got[("archived density", 768.0, 270)], 14.09)
        self.assertEqual(got[("archived density", 1050, 375)], 18.49)
        self.assertEqual(got[("cap binds for all 112 units", 768.0, 270)], 40.86)
        self.assertEqual(got[("cap binds for all 112 units", 1050, 375)], 53.61)
        self.assertEqual(rep["rows"][0]["calls_per_judge"], 1460)

    def test_prices_are_the_batch_prices_of_nov_10(self):
        self.assertEqual(S.PRICES_BATCH["claude-opus-5-5"], (2.0, 10.0))
        self.assertEqual(S.PRICES_BATCH["gpt-6.1-sol"], (1.0, 5.0))
        self.assertEqual((S.HARD_CAP_USD, S.PAUSE_USD), (100.0, 80.0))


class TestWindows(unittest.TestCase):
    def ok(self, when, t4=None, t5=None):
        J.BLACKOUTS[:] = JV.blackouts(t4, t5)
        return J.blackout_within(when) is None

    def setUp(self):
        self.keep = list(J.BLACKOUTS)

    def tearDown(self):
        J.BLACKOUTS[:] = self.keep

    def test_window_a(self):
        t4 = datetime(2026, 11, 12, 6, tzinfo=UTC)
        self.assertFalse(self.ok(datetime(2026, 11, 12, 5, tzinfo=UTC), t4))
        self.assertTrue(self.ok(datetime(2026, 11, 12, 7, tzinfo=UTC), t4))
        self.assertFalse(self.ok(datetime(2026, 11, 13, 1, tzinfo=UTC), t4))   # 24 h would reach Coverage
        self.assertFalse(self.ok(datetime(2026, 11, 12, 7, tzinfo=UTC)))         # t4 not complete

    def test_never_between_or_nov_17_21(self):
        t4, t5 = datetime(2026, 11, 12, tzinfo=UTC), datetime(2026, 12, 7, tzinfo=UTC)
        for d in (datetime(2026, 11, 15, tzinfo=UTC), datetime(2026, 11, 19, tzinfo=UTC),
                  datetime(2026, 11, 23, tzinfo=UTC), datetime(2026, 12, 1, tzinfo=UTC)):
            self.assertFalse(self.ok(d, t4, t5), d)

    def test_window_b(self):
        t5 = datetime(2026, 12, 7, 3, tzinfo=UTC)
        self.assertTrue(self.ok(datetime(2026, 12, 7, 4, tzinfo=UTC), None, t5))
        self.assertFalse(self.ok(datetime(2026, 12, 9, 1, tzinfo=UTC), None, t5))  # results by Dec 10 00:00 UTC
        self.assertFalse(self.ok(datetime(2026, 12, 8, tzinfo=UTC)))              # t5 not complete
        early = datetime(2026, 12, 4, tzinfo=UTC)                                   # t5 ends before Dec 6
        self.assertFalse(self.ok(datetime(2026, 12, 5, tzinfo=UTC), None, early))
        self.assertTrue(self.ok(datetime(2026, 12, 6, 1, tzinfo=UTC), None, early))

    def test_other_judge_process_blocks(self):
        ps = "11 python3 scripts/judge_v1_11.py --run\n12 python3 osf/methodology/v1_15/scripts/judge_v1_15.py --run\n" \
             "13 python3 osf/v42/scripts/acquire_v0_42.py --collect\n"
        hits = JV.other_collections(ps, me="12")
        self.assertEqual(len(hits), 2)
        self.assertFalse(any("judge_v1_15" in h for h in hits))


class TestVerdicts(unittest.TestCase):
    def test_single_wave_band(self):
        rng = random.Random(3)
        Smap, P = {}, {}
        for sub in V.OMNI:
            for i in range(10):
                k = f"{sub}|b{i}"
                Smap[k] = {"S": rng.random() * 100, "rated": True}
                P[k] = Smap[k]["S"] * 2 + 1                   # identical order -> rho 1 -> FALSIFIED
        self.assertEqual(T.single_wave(Smap, P)["verdict"], "FALSIFIED")
        few = {k: v for k, v in list(Smap.items())[:12]}
        self.assertEqual(T.single_wave(few, P)["verdict"], "UNDETERMINED")   # < 20 units / < 3 substrates

    def test_gate_reading_and_noise_guard(self):
        self.assertEqual(T.verdicts_t4("CONFIRMED", "CONFIRMED", "CONFIRMED", "CONFIRMED")["gate_reading_t4"],
                         "UNDETERMINED")                       # H4 not testable on one wave
        v = T.verdicts_t4("FALSIFIED", "CONFIRMED", "CONFIRMED", "CONFIRMED")
        self.assertTrue(v["noise_guard_on"])
        self.assertEqual(v["after_noise_guard"]["H2"], "UNDETERMINED")
        self.assertEqual(v["gate_reading_t4"], "FAIL")

    def test_own_checks(self):
        mk = lambda v, halt=False: {"fail_check": {"halt": halt}, "H1_t4": {"verdict": v}}  # noqa: E731
        self.assertEqual(T.own_checks(mk("CONFIRMED")), "OK")
        self.assertEqual(T.own_checks(mk("MARGINAL")), "FLAGGED")
        self.assertEqual(T.own_checks(mk("UNDETERMINED")), "FAILED")
        self.assertEqual(T.own_checks(mk("CONFIRMED", True)), "FAILED")

    def test_mnp_t4_v110_code(self):
        ans, _ = T.t4_answers(synth_records())
        R = T.mnp_t4(ans, CTX)
        self.assertTrue(R and all(0 <= v["R"] <= 100 for v in R.values()))
        self.assertTrue(any(v["rated"] for v in R.values()))


class TestEndToEnd(unittest.TestCase):
    def test_simulated_run_freeze_stage_j(self):
        recs = synth_records()
        ans, drop = T.t4_answers(recs)
        res = T.build_units_t4(ans, synth_coded(recs), CTX, log=lambda *a: None)
        with tempfile.TemporaryDirectory() as d:
            T.write_u0(res, drop, [], Path(d), log=lambda *a: None)
            out = JV.simulate(Path(d), log=lambda *a: None)
            self.assertEqual(out["rc"][-1], 0, out)
            self.assertFalse(out["resent"])
            P = JV.Paths(dry=True, base=Path(d))
            units = S.read_units(P.units)
            sj = T.stage_j(units, J.read_raw(P.raw), J.current_roles(P))
            self.assertIn(sj["H1_t4"]["verdict"], ("CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED"))
            self.assertTrue(sj["S_t4"])
            self.assertIn("v0.19|Denon", sj["S_t4"])


class TestPrereg(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = PREREG.read_text(encoding="utf-8")

    def test_ai_use_statement_verbatim_after_ethics(self):
        self.assertIn(AI_USE, self.text)
        self.assertLess(self.text.index("### Ethics"), self.text.index("## Use of AI tools {-}"))

    def test_samsung_only_in_coi(self):
        coi = self.text.index("### Conflict of interest")
        end = self.text.index("### Funding")
        outside = self.text[:coi] + self.text[end:]
        self.assertNotIn("Samsung", outside)
        self.assertIn("Samsung", self.text[coi:end])

    def test_canonical_denon_wording(self):
        self.assertIn("Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been "
                      "owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September "
                      "23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones "
                      "registry therefore includes one Samsung-group brand. The substitution did not achieve its "
                      "purpose, and this was not noticed until November 10, 2026.", self.text)


if __name__ == "__main__":
    unittest.main()
