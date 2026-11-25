#!/usr/bin/env python3
"""
Tests for osf/v45/sensitivity/quotes_v0_45.py (sensitivity S-Q, DEVIATIONS Entry 2). Synthetic data and local
records only; no model is called (the v0.23 judge path is patched to fail if reached). One test reads t4's real
coded files when AIAS_T4_DIR points at a directory holding t4_raw.jsonl and coded/ (skipped otherwise).
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SENS = HERE.parent
sys.path.insert(0, str(SENS))
sys.path.insert(0, str(SENS.parent / "scripts"))
sys.path.insert(0, str(SENS.parent / "scripts" / "tests"))
import quotes_v0_45 as Q          # noqa: E402
import make_synthetic_t5 as MS    # noqa: E402
import score_v0_45 as SC          # noqa: E402

C, K, S = Q.C, Q.K, SC.S
ROOT = Q.ROOT
CFG = S.Cfg(200, 200)
T4_T0, T5_T0 = "2026-11-12T00:00:00+00:00", "2026-12-03T07:00:00+00:00"


def call(cid, sub, phase, text, model="gpt-6-astra", cond="S0", run=1, probe="p1", frame="f1", **kw):
    r = {"call_id": cid, "substrate": sub, "phase": phase, "status": "ok", "text": text, "model_requested": model,
         "condition": cond, "run": run, "probe_id": probe, "frame_id": frame}
    r.update(kw)
    return r


def named(B, cid, brand):
    return [r["mentioned"] for r in B if r["call_id"] == cid and r["brand"] == brand]


class TestMap(unittest.TestCase):
    def test_only_u2019_u2018_are_mapped(self):
        s = "Paula’s ‘x’ ʼ ′ ＇ “” ' \" L’Oréal"
        out = Q.normalise(s)
        self.assertEqual(out, "Paula's 'x' ʼ ′ ＇ “” ' \" L'Oréal")
        self.assertEqual(Q.QUOTE_MAP, {"’": "'", "‘": "'"})
        self.assertIsNone(Q.normalise(None))
        self.assertEqual(Q.normalise(""), "")

    def test_inputs_not_modified(self):
        calls = [call("c1", "v20", "B", "Paula’s Choice")]
        before = json.dumps(calls)
        out = Q.normalise_calls(calls)
        self.assertEqual(json.dumps(calls), before)
        self.assertEqual(out[0]["text"], "Paula's Choice")
        self.assertIsNot(out[0], calls[0])


class TestLocked(unittest.TestCase):
    def test_coder_pin(self):
        ok, blob = K.coder_blob_ok()
        self.assertTrue(ok, blob)

    def test_locked_files_keep_their_bytes(self):
        """Every file of the lock manifest except the append-only DEVIATIONS.md has its locked SHA-256."""
        bad = []
        for line in (ROOT / "osf/v45/prereg/LOCK_MANIFEST_v0_45.sha256").read_text(encoding="utf-8").splitlines():
            h, p = line.split("  ", 1)
            if p == "osf/v45/anchor/DEVIATIONS.md":
                continue
            if hashlib.sha256((ROOT / p).read_bytes()).hexdigest() != h:
                bad.append(p)
        self.assertEqual(bad, [])

    def test_wrapper_outside_locked_globs(self):
        """The wrapper and its tests live outside osf/v45/scripts (the manifest's globs) and outside prereg/."""
        self.assertNotIn("scripts", Path(Q.__file__).resolve().relative_to(ROOT).parts)


class TestCoding(unittest.TestCase):
    def setUp(self):
        self._judge = C.code_v23_phase_a

        def boom(*a, **k):
            raise AssertionError("S-Q must not reach the v0.23 judge")
        C.code_v23_phase_a = boom

    def tearDown(self):
        C.code_v23_phase_a = self._judge

    def test_curly_names_flip_straight_names_do_not(self):
        calls = [call("c1", "v20", "B", "Try Paula’s Choice and CeraVe."),
                 call("c2", "v20", "B", "Try Paula's Choice and CeraVe."),
                 call("c3", "v21", "B", "L’Oréal Paris and Maybelline.", model="gemini-4-argon"),
                 call("c4", "v21", "B", "L'Oréal Paris and Maybelline.", model="gemini-4-argon")]
        A0, B0 = C.code_calls(calls, {}, strip=True)
        A1, B1 = Q.code_sq(calls, {}, A0)
        self.assertEqual(named(B0, "c1", "Paula's Choice"), [0])
        self.assertEqual(named(B1, "c1", "Paula's Choice"), [1])
        self.assertEqual(named(B0, "c2", "Paula's Choice"), [1])
        self.assertEqual(named(B1, "c2", "Paula's Choice"), [1])
        self.assertEqual(named(B0, "c3", "L'Oréal Paris"), [0])
        self.assertEqual(named(B1, "c3", "L'Oréal Paris"), [1])
        self.assertEqual(named(B1, "c4", "L'Oréal Paris"), [1])
        d = Q.cell_diffs(A0, B0, A1, B1)
        self.assertEqual(d["n_cells_differ"], 2)
        self.assertEqual(d["by_direction"], {"0->1": 2})
        self.assertEqual(Q.curly_counts(calls), {"v0.20|phase_B": 1, "v0.21|phase_B": 1})

    def test_v23_phase_a_copied_never_judged(self):
        prim = [{"call_id": "a1", "substrate": "v0.23", "brand": "x", "brand_id": "x", "model": "gpt-6-astra",
                 "condition": "S0", "run": 1, "probe_id": "p", "label": "R2", "recognized": 1}]
        calls = [call("a1", "v23", "A", "Yes, it’s known.", brand_id="x", brand="X")]
        A1, B1 = Q.code_sq(calls, {}, prim)
        self.assertEqual(A1, prim)
        self.assertIsNot(A1[0], prim[0])


class TestSynthetic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="v45_sq_tests_", dir="/tmp"))
        b = MS.base_maps(S.load_t3_table())
        cls.t4 = MS.wave(lambda m, c, r: MS.noisy(b[m], m, c, r, 4), cls.tmp / "t4", "t4", T4_T0)
        cls.t5 = MS.wave(lambda m, c, r: MS.noisy(b[m], m, c, r, 5), cls.tmp / "t5", "t5", T5_T0)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_no_curly_quotes_means_identical_tables_and_verdicts(self):
        raw4, A4, B4 = self.t4
        raw5, A5, B5 = self.t5
        self.assertEqual(Q.curly_counts(C.dedupe_calls(raw4)), {})
        p4 = C.load_probe_map(Q.T4_PROBES)
        A4s, B4s = Q.roundtrip(*Q.code_sq(C.dedupe_calls(raw4), p4, A4), self.tmp / "sq4")
        self.assertEqual(Q.cell_diffs(A4, B4, A4s, B4s)["n_cells_differ"], 0)
        prim, _ = SC.score(self.t4, self.t5, CFG)
        sq, _, d5 = Q.run_sq(self.t4, (A4s, B4s), raw5, A5, B5, p4, CFG, {}, self.tmp / "sq5")
        self.assertEqual(d5["n_cells_differ"], 0)
        cmp_ = Q.compare(prim, sq)
        self.assertTrue(cmp_["all_verdicts_same"])
        self.assertEqual(Q.json_diff(prim["verdicts"], sq["verdicts"]), [])

    def test_curly_quote_in_t5_changes_cells_only_there(self):
        raw4, A4, B4 = self.t4
        raw5, A5, B5 = self.t5
        p4 = C.load_probe_map(Q.T4_PROBES)
        raw5c = [dict(r) for r in raw5]
        hit = None
        for r in raw5c:
            if r["substrate"] == "v20" and r["phase"] == "B" and C.is_answered(r) and "Paula's Choice" in r["text"]:
                r["text"] = r["text"].replace("Paula's Choice", "Paula’s Choice")
                hit = r["call_id"]
                break
        self.assertIsNotNone(hit, "synthetic t5 has a v0.20 answer naming Paula's Choice")
        A5c, B5c = Q.roundtrip(*C.code_calls(C.dedupe_calls(raw5c), p4, strip=True), self.tmp / "p5c")
        A5c = A5c + [r for r in A5 if r["substrate"] == "v0.23"]
        self.assertEqual(named(B5c, hit, "Paula's Choice"), [0])          # primary misses it
        _, _, d5 = Q.run_sq(self.t4, (A4, B4), raw5c, A5c, B5c, p4, CFG, {}, self.tmp / "sq5c")
        self.assertEqual(d5["n_cells_differ"], 1)
        self.assertEqual(d5["cells"][0]["call_id"], hit)
        self.assertEqual(d5["by_direction"], {"0->1": 1})


class TestRefusals(unittest.TestCase):
    def test_t4_correction_refuses_existing_outdir(self):
        d = Path(tempfile.mkdtemp(prefix="v45_sq_out_", dir="/tmp"))
        try:
            with self.assertRaises(Q.Refused):
                Q.t4_correction(d, d)
        finally:
            shutil.rmtree(d, ignore_errors=True)

    def test_t5_refuses_before_primary_run(self):
        if Q.PRIMARY_VERDICTS.exists():
            self.skipTest("primary run exists")
        rc = Q.main(["--t5", "--t4-dir", "/nonexistent", "--t4-sq-dir", "/nonexistent", "--j1", "/nonexistent"])
        self.assertEqual(rc, 3)


@unittest.skipUnless(os.environ.get("AIAS_T4_DIR"), "AIAS_T4_DIR not set (real t4 files)")
class TestRealT4(unittest.TestCase):
    def test_t4_flips(self):
        d = Path(os.environ["AIAS_T4_DIR"])
        calls = C.dedupe_calls(C.read_raw(d / "t4_raw.jsonl"))
        A0, B0 = C.read_tables(d / "coded")
        A1, B1 = Q.code_sq(calls, C.load_probe_map(Q.T4_PROBES), A0)
        r = Q.cell_diffs(A0, B0, A1, B1)
        self.assertEqual(r["n_cells_differ"], 46)
        self.assertEqual(r["by_direction"], {"0->1": 46})
        self.assertEqual(r["by_cell"], {"B|v0.20|Paula's Choice|gpt-6-astra|S0": 13,
                                        "B|v0.20|Paula's Choice|gemini-4-argon|S0": 11,
                                        "B|v0.20|Paula's Choice|gemini-4-argon|S1": 7,
                                        "B|v0.21|L'Oréal Paris|gemini-4-argon|S0": 6,
                                        "B|v0.20|Paula's Choice|gpt-6-astra|S1": 6,
                                        "B|v0.21|L'Oréal Paris|gemini-4-argon|S1": 3})


if __name__ == "__main__":
    unittest.main()
