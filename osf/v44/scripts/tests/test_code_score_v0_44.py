#!/usr/bin/env python3
"""
Tests for code_v0_44.py and score_v0_44.py. Synthetic data only (synth_v0_44.py) plus the locked t3 data for gate
P1. No model API is ever called; real v0.44 data is never read. unittest classes (pytest collects them too).

Run as a script or through run_all_v0_44.py (the scorer imports score_v0_42, which re-executes the entry script
once under a HOME shim so that ~/aias resolves to this worktree).
"""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import score_v0_44 as S       # noqa: E402  (bootstraps the HOME shim first)
import code_v0_44 as C        # noqa: E402
import synth_v0_44 as Y       # noqa: E402
import numpy as np            # noqa: E402

REG = C.load_registry()
CFG = S.Cfg(200, 200)
GATES = {"passed": True, "enforce": False}
OFFSET = {"claude-fable-5-2": -1, "gpt-6-astra": 0, "gemini-4-argon": 1}
BASE = {"L": 5, "C": 3, "S": 1, "G": 0}


def tier_k(m, run, ind, u):
    if u["tier"] == "G":
        return 0
    return max(0, min(6, BASE[u["tier"]] + OFFSET[m]))


def run(kfn, cfg=CFG, drop_run3=False, **kw):
    raw = Y.build(kfn, **kw)
    A, B, _ = C.code_calls(C.dedupe_calls(raw), REG, C.load_probe_map())
    out, rows = S.score(raw, A, B, REG, cfg, GATES, drop_run3=drop_run3)
    return out, rows, raw


def V(out):
    return out["verdicts"]


class TestCoder(unittest.TestCase):
    def test_strip_urls_is_a_byte_copy_of_v042(self):
        v42 = (C.ROOT / "osf/v42/scripts/code_t4_v0_42.py").read_text(encoding="utf-8")
        mine = (HERE.parent / "code_v0_44.py").read_text(encoding="utf-8")
        a = v42.index("# Markdown links [text](target)")
        b = v42.index("# --------------------------------------------------------------------------- call handling")
        self.assertIn(v42[a:b].rstrip("\n"), mine)

    def test_parser_is_the_certified_file(self):
        self.assertEqual(C.parser_sha256(), C.PARSER_SHA256)
        self.assertEqual(C.parse_yes_no("Yes, it is."), "yes")
        self.assertEqual(C.parse_yes_no("**No.** It is not."), "no")
        self.assertEqual(C.parse_yes_no("It depends."), "ambiguous")

    def test_registry_and_aliases(self):
        self.assertEqual(sum(len(v) for v in REG.values()), 159)
        self.assertEqual(C.alias_overlaps(REG), [])
        self.assertEqual({u["match_rule"] for v in REG.values() for u in v}, {"ci", "cs"})

    def test_whole_word_case_rules_and_normalisation(self):
        Mt = C.Matcher(REG)
        hits = lambda ind, t: {k for k, v in Mt.mentions(ind, t).items() if v}
        self.assertEqual(hits("APR", "Try the Gap store."), {"APR06"})
        self.assertEqual(hits("APR", "a gap in the market; Gapfill"), set())          # cs and whole word
        self.assertEqual(hits("QSR", "McDonald’s and chick‑fil‑a"), {"QSR01", "QSR03"})
        self.assertEqual(hits("QSR", "Subway sandwiches"), {"QSR09"})
        self.assertEqual(hits("QSR", "take the subway"), set())
        self.assertEqual(hits("FAS", "**Hermès** and CHANEL"), {"FAS01", "FAS03"})
        self.assertEqual(hits("FAS", "Hermès"), {"FAS01"})                   # decomposed accent (NFC)
        self.assertEqual(hits("FAS", "Coaches and coach"), set())
        self.assertEqual(hits("INS", "_Progressive_ insurance"), {"INS02"})        # underscore is a boundary
        self.assertEqual(hits("INS", "progressive rates"), set())
        self.assertEqual(hits("HOT", "Hiltonia"), set())

    def test_audit_exports_case_sensitive_matches_only(self):
        a = []
        C.Matcher(REG).mentions("QSR", "Subway is big. Also McDonald's.", audit=a, call_id="c1")
        self.assertEqual([(r["unit_id"], r["alias"], r["sentence"]) for r in a], [("QSR09", "Subway", "Subway is big.")])

    def test_urls_removed_before_matching(self):
        raw = Y.build(lambda m, r, i, u: 0)
        rec = next(r for r in raw if r["probe_id"] == "APR_B_q1" and r["run"] == 1)
        rec["text"] = "See [our list](https://www.gap.com/Gap) and https://Gap.example/Gap now."
        A, B, _ = C.code_calls([rec], REG)
        self.assertEqual({r["brand"] for r in B if r["mentioned"]}, set())
        rec["text"] = "See [Gap](https://x.example) now."
        A, B, _ = C.code_calls([rec], REG)
        self.assertEqual({r["brand"] for r in B if r["mentioned"]}, {"APR06"})

    def test_coder_reproduces_k_and_recognition(self):
        raw = Y.build(tier_k, recog=lambda m, i, u: int(u["tier"] != "G"))
        A, B, _ = C.code_calls(C.dedupe_calls(raw), REG, C.load_probe_map())
        self.assertEqual(len(A), 477)
        self.assertEqual(len(B), 3 * 3 * sum(6 * len(v) for v in REG.values()))
        k = {}
        for r in B:
            key = (r["model"], r["run"], r["substrate"], r["brand"])
            k[key] = k.get(key, 0) + r["mentioned"]
        for ind, units in REG.items():
            for u in units:
                for m in Y.MODELS:
                    self.assertEqual(k[(m, 2, ind, u["unit_id"])], tier_k(m, 2, ind, u))
        self.assertEqual(sum(r["recognized"] for r in A), 3 * 156)

    def test_dedupe_prefers_last_answered_attempt(self):
        a = {"call_id": "x", "status": "ok", "text": "first", "error": None}
        b = {"call_id": "x", "status": "error", "text": "", "error": "e"}
        c = {"call_id": "x", "status": "ok", "text": "third", "error": None}
        self.assertEqual(C.dedupe_calls([a, b])[0]["text"], "first")
        self.assertEqual(C.dedupe_calls([a, b, c])[0]["text"], "third")

    def test_real_raw_refused_without_tag(self):
        with mock.patch.object(C, "_ls_remote_tag", return_value=""):
            with self.assertRaises(C.Refused):
                C.read_raw(C.REAL_RAW)
            self.assertEqual(C.main([]), 3)

    def test_probe_parity(self):
        raw = Y.build(tier_k)
        sha = C.probe_parity(raw)["probe_sha256"]
        self.assertTrue(C.probe_parity(raw, locked_sha=sha)["passed"])
        self.assertFalse(C.probe_parity(raw, locked_sha=None)["passed"])
        raw[5]["prompt"] += " "
        r = C.probe_parity(raw, locked_sha=sha)
        self.assertEqual((r["passed"], r["prompt_mismatches"]), (False, 1))


class TestKernel(unittest.TestCase):
    def test_phi_max_and_c_phi(self):
        self.assertEqual(S.PHI_MAX, 9.0)
        phi, pi, part = S.phi_m([6, 0, 0])
        self.assertAlmostEqual(phi, 9.0)
        self.assertAlmostEqual(S.c_phi(phi), 0.0)
        phi, pi, part = S.phi_m([0, 0, 3])
        self.assertAlmostEqual(phi, 3.6)
        self.assertAlmostEqual(S.c_phi(phi), 60.0)
        self.assertEqual(S.phi_m([0, 0, 0])[2], "zero")
        self.assertEqual(S.phi_m([6, 6, 6])[2], "saturated")
        k = [4, 1, 2]
        p = sum(k) / 18
        self.assertAlmostEqual(S.phi_m(k)[0], sum((x - 6 * p) ** 2 for x in k) / (6 * p * (1 - p)) / 2)

    def test_rho_pw_centred(self):
        rng = np.random.default_rng(7)
        g_eq = np.repeat(["a", "b", "c"], 10)
        x, y = rng.random(30), rng.random(30)
        self.assertAlmostEqual(S.rho_pw(x, y, g_eq), S.sv.pooled_within_rho(x, y, g_eq), places=12)   # equal sizes
        g = np.array(["a"] * 5 + ["b"] * 25)
        y_flat = np.ones(30)
        self.assertFalse(np.isfinite(S.rho_pw(rng.random(30), y_flat, g)))          # no within-industry variation
        self.assertTrue(np.isfinite(S.sv.pooled_within_rho(rng.random(30), y_flat, g)))   # uncentred: spurious value
        x, y = rng.random(30), rng.random(30)
        self.assertAlmostEqual(S.rho_pw(x, -y, g), -S.rho_pw(x, y, g), places=12)    # sign property
        self.assertAlmostEqual(S.perm_p(x, x, g, S.rho_pw(x, x, g), 1, 99), 0.01)

    def test_verdict_rules(self):
        self.assertEqual([S._verdict_spread(n) for n in (8, 6, 5, 4, 3, 0)],
                         ["CONFIRMED", "CONFIRMED", "MARGINAL", "MARGINAL", "FALSIFIED", "FALSIFIED"])
        self.assertEqual((S.spread_thresholds(8), S.spread_thresholds(7)), ((6, 3), (5, 3)))
        self.assertEqual([S._verdict_spread(n, 7) for n in (7, 5, 4, 3)],
                         ["CONFIRMED", "CONFIRMED", "MARGINAL", "FALSIFIED"])
        self.assertEqual(S.verdict_tier(0.40, 0.049), "CONFIRMED")
        self.assertEqual(S.verdict_tier(0.40, 0.05), "MARGINAL")
        self.assertEqual(S.verdict_tier(0.39, 0.001), "MARGINAL")
        self.assertEqual(S.verdict_tier(0.199, 0.001), "FALSIFIED")
        self.assertEqual(S.verdict_tier(float("nan"), 0.5), "UNDETERMINED")
        self.assertEqual(S.verdict_sep(39, 0.0, [-0.1, 0.1]), "UNDETERMINED")
        self.assertEqual(S.verdict_sep(40, 0.50, [-0.69, 0.69]), "CONFIRMED")
        self.assertEqual(S.verdict_sep(40, -0.3, [-0.70, 0.1]), "MARGINAL")
        self.assertEqual(S.verdict_sep(40, 0.51, [0.3, 0.7]), "FALSIFIED")
        self.assertEqual(S.verdict_sep(40, -0.51, [-0.8, -0.3]), "FALSIFIED")


class TestHypotheses(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tier, cls.tier_rows, _ = run(tier_k, recog=lambda m, i, u: int(u["tier"] != "G"),
                                         extra_text="\n- **Zzyzx Mart** - not in any registry.")

    def test_tier_pattern_confirms_spread_and_tier(self):
        v = V(self.tier)
        self.assertEqual(v["H_Spread"]["n_with_spread"], 8)
        self.assertEqual(v["H_Spread"]["verdict"], "CONFIRMED")
        self.assertGreater(v["H_Tier"]["rho"], 0.9)
        self.assertEqual(v["H_Tier"]["verdict"], "CONFIRMED")
        self.assertIn("without_FAS", v["H_Tier"]["reported_alongside"])
        self.assertEqual(v["H_Tier"]["reported_alongside"]["without_pharmacy_units_from_other_metric"]["units_removed"],
                         ["Health Mart", "Good Neighbor Pharmacy"])
        self.assertEqual(v["H_Tier"]["n"], 156)

    def test_separation_computed_on_rated_units(self):
        v = V(self.tier)["H_Separation"]
        self.assertEqual(v["n_rated"], 156)                    # L, C and S units rated; ghosts at zero
        self.assertEqual(v["verdict"], S.verdict_sep(v["n_rated"], v["rho"], v["ci95_rho"]))
        self.assertAlmostEqual(v["reported_alongside"]["rho_with_raw_phi"], -v["rho"], places=12)
        row = next(r for r in self.tier_rows if r["unit_id"] == "INS01")
        self.assertAlmostEqual(row["phi_b"], 1.2)              # k = [4, 5, 6] in every run
        self.assertAlmostEqual(row["c_phi"], 100 * (1 - 1.2 / 9))

    def test_manipulation_checks_pass_on_clean_data(self):
        mc = self.tier["manipulation_checks"]
        self.assertTrue(mc["MC_Complete"]["pass"])
        self.assertEqual(mc["MC_Complete"]["answered"], 909)
        self.assertTrue(mc["MC_Served"]["pass"])
        self.assertTrue(mc["MC_Window"]["pass"])
        self.assertTrue(mc["MC_Budget"]["pass"])

    def test_descriptives_present(self):
        d = self.tier["descriptives"]
        self.assertEqual(set(k.split("_")[0] for k in d if k[0].isdigit()), {str(i) for i in range(1, 10)})
        # 54 INS answers; the 9 q6 answers of Fable and GPT name no unit (k <= 5) and carry no extra text
        self.assertIn(["Zzyzx Mart", 45], [list(x) for x in d["6_non_registry_names_in_phase_b"]["INS"]["top10"]])
        self.assertEqual(set(d["7_units_in_two_industries"]["Kroger"]), {"GRO:Kroger", "PHA:Kroger Pharmacy"})
        self.assertEqual(len(d["3_ghosts"]), 3)

    def test_reversed_tier_falsifies(self):
        out, _, _ = run(lambda m, r, i, u: 0 if u["tier"] == "G" else {"L": 1, "C": 3, "S": 5}[u["tier"]])
        self.assertEqual(V(out)["H_Tier"]["verdict"], "FALSIFIED")

    def test_flat_presence_falsifies_spread(self):
        out, _, _ = run(lambda m, r, i, u: 3)
        self.assertEqual(V(out)["H_Spread"]["n_with_spread"], 0)
        self.assertEqual(V(out)["H_Spread"]["verdict"], "FALSIFIED")
        self.assertEqual(V(out)["H_Tier"]["verdict"], "UNDETERMINED")       # constant Presence: rho undefined

    def test_spread_in_four_industries_is_marginal(self):
        four = {"INS", "HOT", "GRO", "QSR"}
        out, _, _ = run(lambda m, r, i, u: tier_k(m, r, i, u) if i in four else 3)
        self.assertEqual(V(out)["H_Spread"]["n_with_spread"], 4)
        self.assertEqual(V(out)["H_Spread"]["verdict"], "MARGINAL")

    def test_dispersion_falling_with_presence_falsifies_separation(self):
        pat = {"L": {-1: 5, 0: 5, 1: 5}, "C": {-1: 2, 0: 3, 1: 4}, "S": {-1: 0, 0: 0, 1: 3}}
        out, _, _ = run(lambda m, r, i, u: 0 if u["tier"] == "G" else pat[u["tier"]][OFFSET[m]])
        v = V(out)["H_Separation"]
        self.assertGreater(v["rho"], 0.5)
        self.assertEqual(v["verdict"], "FALSIFIED")

    def test_fewer_than_40_rated_is_undetermined(self):
        few = {"INS", "HOT", "GRO"}
        out, _, _ = run(lambda m, r, i, u: tier_k(m, r, i, u) if (i in few and u["tier"] == "L") else 0)
        v = V(out)["H_Separation"]
        self.assertEqual(v["n_rated"], 18)
        self.assertEqual(v["verdict"], "UNDETERMINED")

    def test_drop_rule_phase_b_makes_primaries_undetermined(self):
        # 24 of Fable's 144 Phase B calls missing (q1-q3 of run 1 in all 8 industries): 120/144 = 0.83 < 0.90
        out, _, _ = run(tier_k, drop=lambda s: s["model"] == "claude-fable-5-2" and s["phase"] == "B"
                        and s["probe_id"].endswith(("q1", "q2", "q3")) and s["run"] == 1)
        mc = out["manipulation_checks"]["MC_Complete"]
        self.assertEqual(mc["per_model_phase"]["claude-fable-5-2|B"]["answered"], 144 - 24)
        self.assertEqual(mc["dropped_models"]["B"], ["claude-fable-5-2"])
        for h in ("H_Spread", "H_Tier", "H_Separation"):
            self.assertEqual(V(out)[h]["verdict"], "UNDETERMINED")

    def test_boundary_90_percent_keeps_model(self):
        n = 0

        def drop(s):
            nonlocal n
            if s["model"] == "gpt-6-astra" and s["phase"] == "B" and s["run"] == 3 and n < 14:
                n += 1
                return True
            return False
        out, _, _ = run(tier_k, drop=drop)
        mc = out["manipulation_checks"]["MC_Complete"]
        self.assertEqual(mc["per_model_phase"]["gpt-6-astra|B"]["answered"], 130)       # 130/144 = 0.903
        self.assertEqual(mc["dropped_models"]["B"], [])
        self.assertNotEqual(V(out)["H_Tier"]["verdict"], "UNDETERMINED")

    def test_served_mismatch_excluded_dated_snapshot_accepted(self):
        def served(s):
            if s["model"] == "gpt-6-astra" and s["phase"] == "A" and s["industry"] == "INS":
                return "gpt-6-astra-2026-11-01"
            if s["model"] == "gemini-4-argon" and s["phase"] == "A" and s["industry"] == "FAS":
                return "gemini-3-pro"
            return s["model"]
        out, _, _ = run(tier_k, served=served)
        mc = out["manipulation_checks"]
        self.assertEqual(mc["MC_Served"]["n_mismatched"], 24)
        self.assertFalse(mc["MC_Served"]["pass"])
        self.assertEqual(mc["MC_Complete"]["per_model_phase"]["gemini-4-argon|A"]["answered"], 159 - 24)

    def test_window_checks(self):
        out, _, _ = run(tier_k, hours=80)
        self.assertFalse(out["manipulation_checks"]["MC_Window"]["pass"])
        out, _, _ = run(tier_k, t0="2026-11-20T15:00:00+00:00")
        self.assertFalse(out["manipulation_checks"]["MC_Window"]["all_starts_inside_window"])

    def test_drop_run3_design(self):
        out, rows, raw = run(tier_k, runs=(1, 2), drop_run3=True)
        self.assertEqual(len(raw), 765)
        mc = out["manipulation_checks"]["MC_Complete"]
        self.assertEqual((mc["expected"], mc["answered"]), (765, 765))
        self.assertTrue(mc["pass"])
        self.assertEqual(V(out)["H_Separation"]["n_rated"], 156)
        row = next(r for r in rows if r["unit_id"] == "INS01")
        self.assertEqual(json.loads(row["phi_run_partitions"]), ["defined", "defined", "missing"])

    def test_pharmacies_dropped_registry_needs_no_code_change(self):
        reg7 = {k: v for k, v in REG.items() if k != "PHA"}
        raw = [r for r in Y.build(tier_k) if r["substrate"] != "PHA"]
        A, B, _ = C.code_calls(C.dedupe_calls(raw), reg7, C.load_probe_map())
        out, _ = S.score(raw, A, B, reg7, CFG, GATES)
        self.assertEqual(out["design"]["expected_total"], 807)
        self.assertEqual(V(out)["H_Spread"]["n_industries"], 7)
        self.assertEqual(V(out)["H_Spread"]["thresholds"], {"confirmed_at_least": 5, "falsified_at_most": 3})
        self.assertEqual(V(out)["H_Tier"]["n"], 141)
        self.assertNotIn("without_pharmacy_units_from_other_metric", V(out)["H_Tier"]["reported_alongside"])
        self.assertTrue(out["manipulation_checks"]["MC_Complete"]["pass"])


class TestGatesAndCli(unittest.TestCase):
    def test_parity_gate_blocks_scoring(self):
        raw = Y.build(tier_k)
        with self.assertRaises(S.Halt):
            S.score(raw, [], [], REG, CFG, {"passed": False, "enforce": True})

    def test_p1_on_locked_t3(self):
        r = S.parity_p1(out_path=None)
        self.assertTrue(r["passed"])
        self.assertEqual((r["brands_compared"], r["pi_hat_exact"], r["phi_exact"]), (112, 112, 112))

    def test_real_run_refused_without_tag_or_when_already_scored(self):
        with mock.patch.object(C, "_ls_remote_tag", return_value=""), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(S.main(["--run"]), 3)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "v44_verdicts.json"
            p.write_text("{}")
            with mock.patch.object(S, "VERDICTS", p), mock.patch.object(C, "_ls_remote_tag",
                                                                         side_effect=AssertionError("not reached")), \
                    contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(S.main(["--run"]), 3)

    def test_cli_synthetic_end_to_end(self):
        with tempfile.TemporaryDirectory() as d:
            Y.write(Y.build(tier_k), d)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(C.main(["--raw", str(Path(d) / "v44_raw.jsonl"), "--out", str(Path(d) / "coded")]), 0)
                self.assertEqual(S.main(["--synthetic", d, "--draws", "100"]), 0)
            out = json.loads((Path(d) / "_score/v44_verdicts.json").read_text())
            self.assertEqual(out["verdicts"]["H_Tier"]["verdict"], "CONFIRMED")
            self.assertTrue((Path(d) / "_score/v44_unit_table.csv").exists())
            self.assertTrue((Path(d) / "coded/v44_alias_audit.csv").exists())


if __name__ == "__main__":
    unittest.main(verbosity=1)
