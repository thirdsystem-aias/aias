#!/usr/bin/env python3
"""
Tests for code_t4_v0_42.py and score_v0_42.py. Synthetic data only (make_synthetic_t4.py) plus the locked t3
data for the parity gates. No model API is ever called (the v0.23 judge is mocked); real t4 data is never read.

Run as a script (the scorer re-executes its entry script under a HOME shim so ~/aias resolves to the worktree):
    AIAS_ROOT=<worktree> python3 osf/v42/scripts/tests/test_score_v0_42.py
"""
import collections
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import make_synthetic_t4 as M      # noqa: E402  (imports code_t4_v0_42 -> bootstraps ROOT)
import code_t4_v0_42 as C          # noqa: E402
import score_v0_42 as S            # noqa: E402
import numpy as np                 # noqa: E402

T3 = S.load_t3_table()
L = {m: M.from_t3(T3, i) for m, i in zip(M.MODELS, (0, 2, 4))}   # fable<-opus4.5, gpt6<-gpt-4o, gem4<-flash
CFG = S.Cfg(200, 200)
GATES = {"passed": True, "enforce": False}
N3 = S.PANELS["N3"]


def run(kfn, cfg=CFG, **kw):
    raw, A, B = M.build(kfn, **kw)
    out, rows = S.score_t4(raw, A, B, T3, cfg, GATES)
    return out, raw, A, B


def copy_t3(m, c, r):
    return L[m]


def pi_rho(kfn):
    """Direct rho_pw(t3 pi_hat, N3 S0 pi_hat) for a k-map generator, without the permutation machinery."""
    raw, A, B = M.build(kfn)
    D = S.Data(list(T3), A, B)
    keys, x, y, g = S.pair_arrays({k: v["pi"] for k, v in T3.items()}, S.pi_hat(D, N3, "S0"))
    return S.pooled_within_rho(x, y, g)


class TestKernelAndHelpers(unittest.TestCase):
    def test_phi_m_equals_phi_of_for_six_models(self):
        rng = np.random.default_rng(1)
        vecs = [rng.integers(0, 7, 6).tolist() for _ in range(300)] + [[0] * 6, [6] * 6, [1, 0, 0, 0, 0, 0]]
        for v in vecs:
            self.assertEqual(S.phi_m(v), S.phi_of(v))

    def test_phi_m_three_models_formula(self):
        k = [4, 1, 2]
        pi = sum(k) / 18
        want = sum((x - 6 * pi) ** 2 for x in k) / (6 * pi * (1 - pi)) / 2
        phi, p, part = S.phi_m(k)
        self.assertAlmostEqual(phi, want, places=12)
        self.assertEqual(part, "defined")
        self.assertEqual(S.phi_m([0, 0, 0])[2], "zero")
        self.assertEqual(S.phi_m([6, 6, 6])[2], "saturated")

    def test_pi_hat_formula_t3(self):
        self.assertEqual(S.pi_from_counts([3, 2, 3, 3, 0, 4], 6, 1), 15 / 36)


class TestUrlStripping(unittest.TestCase):
    def test_strip_urls(self):
        self.assertEqual(C.strip_urls("See [Sennheiser](https://x.com/a?b=1) now"), "See Sennheiser now")
        self.assertNotIn("http", C.strip_urls("go to https://www.sennheiser.com/hd800 and http://a.b/c."))
        self.assertEqual(C.strip_urls("[w](https://en.wikipedia.org/wiki/A_(b))"), "w")
        self.assertEqual(C.strip_urls('[t](https://x.y "title") ok'), "t ok")
        self.assertEqual(C.strip_urls("plain text, no links"), "plain text, no links")
        self.assertEqual(C.strip_urls(""), "")

    def _calls(self, text):
        return [{"call_id": "c1", "substrate": "v19", "phase": "B", "probe_id": "phase_b__q1_audiophile",
                 "frame_id": "q1_audiophile", "model_requested": "claude-fable-5-2", "condition": "S1", "run": 1,
                 "text": text, "status": "ok", "error": None}]

    def test_brand_in_address_counts_only_without_stripping(self):
        text = "Read more at https://www.sennheiser.com/hd-800 or [here](https://sennheiser.com/x)."
        _, B_on = C.code_calls(self._calls(text), {}, strip=True)
        _, B_off = C.code_calls(self._calls(text), {}, strip=False)
        on = {r["brand"]: r["mentioned"] for r in B_on}
        off = {r["brand"]: r["mentioned"] for r in B_off}
        self.assertEqual(on["Sennheiser"], 0)
        self.assertEqual(off["Sennheiser"], 1)

    def test_link_text_naming_the_brand_still_counts(self):
        _, B = C.code_calls(self._calls("Try [Sennheiser](https://example.com/shop) first."), {}, strip=True)
        self.assertEqual({r["brand"]: r["mentioned"] for r in B}["Sennheiser"], 1)


class TestCoderRoundTrip(unittest.TestCase):
    def test_coder_reproduces_synthetic_codes_and_judge_is_off(self):
        raw, A, B = M.build(lambda m, c, r: L[m] if c == "S0" else M.mixed(L[m], 0.3, 5))
        probes = C.load_probe_map()
        with mock.patch("anthropic.Anthropic", side_effect=AssertionError("API must not be called")):
            A2, B2 = C.code_calls(raw, probes, strip=True, judge_client=None)
        self.assertFalse([r for r in A2 if r["substrate"] == "v0.23"])          # judge OFF -> v0.23 Phase A uncoded
        key = lambda r: (r["call_id"], r["brand"])
        self.assertEqual({key(r): r["mentioned"] for r in B}, {key(r): r["mentioned"] for r in B2})
        a1 = {key(r): r["recognized"] for r in A if r["substrate"] != "v0.23"}
        self.assertEqual(a1, {key(r): r["recognized"] for r in A2})

    def test_judge_path_with_mock_client(self):
        raw, A, B = M.build(lambda m, c, r: L[m])
        v23a = [r for r in raw if r["substrate"] == "v23" and r["phase"] == "A"][:30]

        class Fake:
            def __init__(self):
                self.messages = self
                self.n = 0

            def create(self, **kw):
                self.n += 1
                return type("M", (), {"content": [type("B", (), {"text": "R3"})()]})()
        fake = Fake()
        A2, _ = C.code_calls(v23a, C.load_probe_map(), judge_client=fake)
        self.assertEqual(fake.n, 30)
        self.assertTrue(all(r["recognized"] == 1 and r["label"] == "R3" for r in A2))
        self.assertEqual({r["brand"][0] for r in A2}, {"S"})          # v0.23 key = brand id

    def test_tables_roundtrip_on_disk(self):
        raw, A, B = M.build(lambda m, c, r: L[m])
        with tempfile.TemporaryDirectory() as d:
            C.write_tables(A, B, d)
            A2, B2 = C.read_tables(d)
        self.assertEqual(len(A2), len(A))
        self.assertEqual(len(B2), len(B))

    def test_dedupe_prefers_last_answered_attempt(self):
        r1 = {"call_id": "x", "status": "error", "text": "", "error": "e"}
        r2 = {"call_id": "x", "status": "ok", "text": "hi", "error": None}
        r3 = {"call_id": "x", "status": "error", "text": "", "error": "e2"}
        self.assertIs(C.dedupe_calls([r1, r2, r3])[0], r2)
        self.assertIs(C.dedupe_calls([r1, r3])[0], r3)


class TestGuard(unittest.TestCase):
    def test_refuses_real_t4_without_tag(self):
        with mock.patch.object(C, "_ls_remote_tag", return_value=""):
            with self.assertRaises(C.Refused):
                C.read_raw(C.REAL_RAW)
            with mock.patch.object(sys, "argv", ["score_v0_42.py", "--run"]):
                self.assertEqual(S.main(), 3)

    def test_ls_remote_failure_refuses(self):
        with mock.patch.object(C, "_ls_remote_tag", side_effect=C.Refused("network")):
            with self.assertRaises(C.Refused):
                C.read_raw(C.REAL_RAW)

    def test_synthetic_path_bypasses_guard(self):
        with tempfile.TemporaryDirectory() as d:
            M.build(copy_t3, outdir=d)
            with mock.patch.object(C, "_ls_remote_tag", side_effect=AssertionError("must not be asked")):
                self.assertEqual(len(C.read_raw(Path(d) / "t4_raw.jsonl")), 876)

    def test_cli_synthetic_end_to_end(self):
        with tempfile.TemporaryDirectory() as d:
            M.build(copy_t3, outdir=d)
            with mock.patch.object(sys, "argv", ["score_v0_42.py", "--synthetic", d, "--draws", "100"]):
                self.assertEqual(S.main(), 0)
            v = json.load(open(Path(d) / "_score/v42_verdicts.json"))
            self.assertEqual(v["verdicts"]["H_Gen_Presence"]["verdict"], "CONFIRMED")
            self.assertTrue((Path(d) / "_score/v42_brand_table.csv").exists())


class TestPermutationFormula(unittest.TestCase):
    def test_p_formula_extremes(self):
        g = np.array(["a"] * 6 + ["b"] * 6)
        x = np.arange(12, dtype=float)
        self.assertEqual(S.perm_p_within(x, x.copy(), g, 1.0, 7, 100), 1 / 101)           # no draw reaches rho = 1
        self.assertEqual(S.perm_p_within(x, x.copy(), g, -2.0, 7, 100), 101 / 101)        # every draw is a hit
        self.assertEqual(S.perm_p_within(x, x.copy(), g, 1.0, 7, 10_000), 1 / 10_001)

    def test_p_is_count_based_with_ten_thousand_draws(self):
        rng = np.random.default_rng(3)
        g = np.array(["a"] * 20 + ["b"] * 20)
        x = rng.normal(size=40)
        y = x + rng.normal(size=40)
        obs = S.pooled_within_rho(x, y, g)
        p = S.perm_p_within(x, y, g, obs, 420041, 10_000)
        hits = round(p * 10_001) - 1
        self.assertAlmostEqual(p, (1 + hits) / 10_001, places=12)
        # independent recomputation of the same draws
        r = np.random.default_rng(420041)
        gi = [np.where(g == k)[0] for k in ("a", "b")]
        h = 0
        for _ in range(10_000):
            yp = y.copy()
            for i in gi:
                yp[i] = y[r.permutation(i)]
            h += S.pooled_within_rho(x, yp, g) >= obs - 1e-12
        self.assertEqual(hits, h)
        self.assertLess(p, 0.05)

    def test_shuffles_stay_within_substrate(self):
        # if the permutation leaked across substrates, a perfect within-substrate order with different
        # substrate levels could not reach the minimum p; here y = x + 100 * substrate: p stays minimal
        g = np.array(["a"] * 6 + ["b"] * 6)
        x = np.arange(12, dtype=float)
        y = x + np.where(g == "b", 100.0, 0.0)
        self.assertEqual(S.perm_p_within(x, y, g, S.pooled_within_rho(x, y, g), 1, 200), 1 / 201)


class TestPhiRule(unittest.TestCase):
    def _D(self, drop):
        raw, A, B = M.build(copy_t3, drop=drop)
        return S.Data(list(T3), A, B)

    def test_two_of_three_runs_mean(self):
        gpt_run3_v20 = lambda s: s["model"] == M.MODELS[1] and s["condition"] == "S0" and s["run"] == 3 and s["substrate"] == "v20" and s["phase"] == "B"
        D = self._D(gpt_run3_v20)
        ph = S.phi_panel(D, N3, "S0")
        full = S.phi_panel(self._D(None), N3, "S0")
        n_def = 0
        for (s, b), (phi, part, runs) in ph.items():
            if s == "v0.20":
                self.assertEqual(runs[2], "missing")
                base = full[(s, b)]
                if base[1] == "defined":                      # identical runs -> mean of two equal values
                    n_def += 1
                    self.assertAlmostEqual(phi, base[0], places=12)
                    self.assertEqual(part, "defined")
            else:
                self.assertEqual(runs, full[(s, b)][2])
        self.assertGreater(n_def, 3)

    def test_fewer_than_two_runs_is_undefined(self):
        d = lambda s: s["model"] == M.MODELS[1] and s["condition"] == "S0" and s["run"] in (2, 3) and s["substrate"] == "v20" and s["phase"] == "B"
        ph = S.phi_panel(self._D(d), N3, "S0")
        for (s, b), (phi, part, runs) in ph.items():
            if s == "v0.20":
                self.assertIsNone(phi)
                self.assertEqual(part, "undefined")

    def test_exactly_two_defined_runs_of_differing_values(self):
        # run 1 and run 2 differ for one brand; run 3 missing -> mean of the two defined phis
        base = dict(L[M.MODELS[0]])
        bkey = next(k for k, v in T3.items() if k[0] == "v0.20" and v["phi"] is not None)

        def kfn(m, c, r):
            if m == M.MODELS[0] and r == 2:
                k = dict(base)
                k[bkey] = min(6, base[bkey] + 1) if base[bkey] < 6 else base[bkey] - 1
                return k
            return L[m]
        raw, A, B = M.build(kfn, drop=lambda s: s["model"] == M.MODELS[2] and s["condition"] == "S0" and s["run"] == 3
                            and s["substrate"] == "v20" and s["phase"] == "B")
        D = S.Data(list(T3), A, B)
        phi, part, runs = S.phi_panel(D, N3, "S0")[bkey]
        v1 = S.phi_m([D.kk("S0", m, 1, *bkey) for m in N3])[0]
        v2 = S.phi_m([D.kk("S0", m, 2, *bkey) for m in N3])[0]
        self.assertEqual(runs[2], "missing")
        self.assertNotEqual(v1, v2)
        self.assertAlmostEqual(phi, (v1 + v2) / 2, places=12)


class TestMissingCallsAndDropRule(unittest.TestCase):
    def test_rates_use_answered_calls(self):
        gone = lambda s: (s["model"] == M.MODELS[0] and s["condition"] == "S0" and s["run"] == 1 and s["substrate"] == "v20"
                          and s["probe_id"] in ("q5", "q6"))
        raw, A, B = M.build(copy_t3, drop=gone)
        D = S.Data(list(T3), A, B)
        self.assertEqual(D.n("S0", M.MODELS[0], 1, "v0.20"), 4)
        self.assertEqual(D.n("S0", M.MODELS[0], 2, "v0.20"), 6)
        bkey = next(k for k, v in T3.items() if k[0] == "v0.20" and 1 <= v["k"][0] <= 4)  # not listed in the dropped frames q5/q6
        pi = S.pi_hat(D, N3, "S0")[bkey]
        num = sum(D.kk("S0", m, r, *bkey) for m in N3 for r in (1, 2, 3))
        den = 6 * 3 * 3 - 2
        self.assertEqual(pi, num / den)
        full = S.pi_hat(S.Data(list(T3), *M.build(copy_t3)[1:]), N3, "S0")[bkey]
        self.assertNotEqual(pi, full)

    def test_model_drop_boundary_90_percent(self):
        def failing(n):
            seen = collections.Counter()

            def f(s):
                if s["model"] == M.MODELS[0] and s["condition"] == "S0":
                    seen["n"] += 1
                    return seen["n"] <= n
                return False
            return f
        out42, *_ = run(copy_t3, fail=failing(20))      # 182/202 = 90.10 %: retained
        out43, *_ = run(copy_t3, fail=failing(21))      # 181/202 = 89.6 %: excluded
        self.assertNotIn("claude-fable-5-2|S0", out42["models_excluded_condition"])
        self.assertIn("claude-fable-5-2|S0", out43["models_excluded_condition"])
        self.assertEqual(out42["verdicts"]["H_Gen_Presence"]["panel_used"], "N3")

    def test_any_n3_model_excluded_makes_gen_undetermined(self):
        for victim in M.MODELS:                       # r2: no fallback panel (C3 removed)
            out, *_ = run(copy_t3, fail=lambda s, v=victim: s["model"] == v and s["condition"] == "S0")
            self.assertEqual(out["verdicts"]["H_Gen_Presence"]["verdict"], "UNDETERMINED")
            self.assertEqual(out["verdicts"]["H_Gen_Phi"]["verdict"], "UNDETERMINED")
            self.assertIn(victim, out["verdicts"]["H_Gen_Presence"]["reason"])

    def test_s1_exclusion_leaves_primary_on_n3(self):
        out, *_ = run(copy_t3, fail=lambda s: s["model"] == M.MODELS[0] and s["condition"] == "S1")
        self.assertEqual(out["verdicts"]["H_Gen_Presence"]["panel_used"], "N3")
        al = out["verdicts"]["H_Gen_Presence"]["reported_alongside"]["variants"]["N3_S1"]
        self.assertTrue(al["reduced_panel"])


class TestGenPresenceBranches(unittest.TestCase):
    def test_confirmed_when_n3_copies_t3(self):
        out, *_ = run(copy_t3)
        v = out["verdicts"]["H_Gen_Presence"]
        self.assertEqual(v["verdict"], "CONFIRMED")
        self.assertGreaterEqual(v["rho"], 0.70)
        self.assertLess(v["p_perm"], 0.05)
        self.assertEqual(v["n"], 112)
        self.assertAlmostEqual(v["p_perm"] * (CFG.n_perm + 1), round(v["p_perm"] * (CFG.n_perm + 1)), places=6)

    def test_falsified_when_shuffled(self):
        kfn = lambda m, c, r: M.shuffled(L[m], 100 + M.MODELS.index(m))
        out, *_ = run(kfn)
        v = out["verdicts"]["H_Gen_Presence"]
        self.assertEqual(v["verdict"], "FALSIFIED")
        self.assertLess(v["rho"], 0.50)

    def test_marginal_when_in_between(self):
        for frac in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0):
            kfn = lambda m, c, r, f=frac: M.mixed(L[m], f, 10 + M.MODELS.index(m))
            rho = pi_rho(kfn)
            if 0.50 <= rho < 0.70:
                break
        else:
            self.fail("no mixing fraction produced 0.50 <= rho < 0.70")
        out, *_ = run(kfn)
        self.assertEqual(out["verdicts"]["H_Gen_Presence"]["verdict"], "MARGINAL")

    def test_threshold_rules(self):
        self.assertEqual(S.verdict_gen(0.70, 0.04), "CONFIRMED")
        self.assertEqual(S.verdict_gen(0.95, 0.05), "MARGINAL")       # p not < 0.05
        self.assertEqual(S.verdict_gen(0.499, 0.001), "FALSIFIED")
        self.assertEqual(S.verdict_gen(0.50, 0.001), "MARGINAL")
        self.assertEqual(S.verdict_gen(float("nan"), 0.5), "UNDETERMINED")

    def test_alongside_items_present(self):
        out, *_ = run(copy_t3)
        al = out["verdicts"]["H_Gen_Presence"]["reported_alongside"]
        self.assertEqual(set(al["variants"]), {"N3_S1"})
        self.assertEqual(len(al["per_provider_generation_pairs"]), 3)       # Fable 5.2, GPT-6 Astra, Gemini 4 Argon
        self.assertIsNotNone(al["level_shift_delta"]["ci95"])
        self.assertEqual(set(al["per_substrate_rho"]), set(S.OMNI))

    def test_level_shift(self):
        kfn = lambda m, c, r: {k: min(6, v + 1) for k, v in L[m].items()}
        out, *_ = run(kfn)
        self.assertGreater(out["verdicts"]["H_Gen_Presence"]["delta"], 0.0)


class TestVersionRemoved(unittest.TestCase):
    def test_version_hypothesis_and_opus_removed(self):
        out, *_ = run(copy_t3)
        self.assertEqual(set(out["verdicts"]), {"H_Gen_Presence", "H_Gen_Phi", "H_Search_Presence"})
        self.assertNotIn(420042, S.SEEDS.values())
        self.assertEqual(S.MODELS, ["claude-fable-5-2", "gpt-6-astra", "gemini-4-argon"])
        self.assertEqual(set(out["panels"]), {"L6", "N3"})
        self.assertIn("revision r2", out["prereg"])


class TestPhiBranches(unittest.TestCase):
    def test_confirmed_when_n3_copies_t3(self):
        out, *_ = run(copy_t3)
        v = out["verdicts"]["H_Gen_Phi"]
        self.assertEqual(v["verdict"], "CONFIRMED")
        self.assertGreaterEqual(v["n"], 40)
        self.assertGreaterEqual(v["rho"], 0.5)

    def test_falsified_when_shuffled(self):
        out, *_ = run(lambda m, c, r: M.shuffled(L[m], 300 + M.MODELS.index(m)))
        v = out["verdicts"]["H_Gen_Phi"]
        self.assertGreaterEqual(v["n"], 40)
        self.assertEqual(v["verdict"], "FALSIFIED")
        self.assertLess(v["rho"], 0.30)

    def test_marginal_in_between(self):
        for frac in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8):
            kfn = lambda m, c, r, f=frac: M.mixed(L[m], f, 21 + M.MODELS.index(m))
            raw, A, B = M.build(kfn)
            D = S.Data(list(T3), A, B)
            y = {k: v[0] for k, v in S.phi_panel(D, N3, "S0").items()}
            keys, x, yy, g = S.pair_arrays({k: v["phi"] for k, v in T3.items()}, y)
            rho = S.pooled_within_rho(x, yy, g)
            if len(keys) >= 40 and 0.30 <= rho < 0.50:
                break
        else:
            self.skipTest("no mixing fraction landed in [0.30, 0.50) -- branch covered by test_threshold_rules")
        out, *_ = run(kfn)
        self.assertEqual(out["verdicts"]["H_Gen_Phi"]["verdict"], "MARGINAL")

    def test_undetermined_when_n_below_40(self):
        keep = {k for k in T3 if T3[k]["phi"] is not None}
        few = sorted(keep)[:20]

        def sparse(m, c, r):
            base = L[m]
            return {k: (base[k] if k in few else 0) for k in base}
        out, *_ = run(sparse)
        v = out["verdicts"]["H_Gen_Phi"]
        self.assertLess(v["n"], 40)
        self.assertEqual(v["verdict"], "UNDETERMINED")

    def test_threshold_rules(self):
        self.assertEqual(S.verdict_phi(39, 0.9, 0.001), "UNDETERMINED")
        self.assertEqual(S.verdict_phi(40, 0.50, 0.049), "CONFIRMED")
        self.assertEqual(S.verdict_phi(40, 0.60, 0.05), "MARGINAL")
        self.assertEqual(S.verdict_phi(40, 0.299, 0.01), "FALSIFIED")
        self.assertEqual(S.verdict_phi(40, 0.30, 0.01), "MARGINAL")

    def test_alongside_mean_independence_and_partitions(self):
        out, *_ = run(copy_t3)
        al = out["verdicts"]["H_Gen_Phi"]["reported_alongside"]
        self.assertEqual(set(al["mean_independence_S0"]), {"N3"})
        self.assertIn("flag_ge_0_50", al["mean_independence_S0"]["N3"])
        self.assertEqual(set(al["partition_counts"]), {"N3_S0", "N3_S1", "L6_t3"})
        pc = al["partition_counts"]["N3_S0"]["brand_level"]
        self.assertEqual(sum(pc.values()), 112)
        self.assertEqual(al["variants"], {})


class TestSearchBranches(unittest.TestCase):
    def test_robust(self):
        out, *_ = run(copy_t3)
        v = out["verdicts"]["H_Search_Presence"]
        self.assertEqual(v["label"], "search-robust")
        self.assertAlmostEqual(v["rho"], 1.0)
        self.assertAlmostEqual(v["delta"], 0.0)

    def test_dominated(self):
        kfn = lambda m, c, r: L[m] if c == "S0" else M.shuffled(L[m], 900 + M.MODELS.index(m))
        out, *_ = run(kfn)
        v = out["verdicts"]["H_Search_Presence"]
        self.assertEqual(v["label"], "search-dominated")
        self.assertLess(v["ci95_rho"][1], 0.50)

    def test_sensitive(self):
        for frac in (0.3, 0.4, 0.5, 0.6, 0.7, 0.8):
            kfn = lambda m, c, r, f=frac: L[m] if c == "S0" else M.mixed(L[m], f, 40 + M.MODELS.index(m))
            out, *_ = run(kfn)
            if out["verdicts"]["H_Search_Presence"]["label"] == "search-sensitive":
                break
        else:
            self.fail("no mixing fraction produced search-sensitive")
        v = out["verdicts"]["H_Search_Presence"]
        self.assertLess(v["ci95_rho"][0], 0.80)
        self.assertGreaterEqual(v["ci95_rho"][1], 0.50)
        self.assertNotIn("C3", v["reported_alongside"])
        self.assertEqual(set(v["per_model"]), set(N3))

    def test_label_rule(self):
        self.assertEqual(S.label_search([0.80, 0.9]), "search-robust")
        self.assertEqual(S.label_search([0.79, 0.9]), "search-sensitive")
        self.assertEqual(S.label_search([0.0, 0.499]), "search-dominated")
        self.assertEqual(S.label_search([0.0, 0.50]), "search-sensitive")


class TestManipulationChecksAndDescriptives(unittest.TestCase):
    def test_served_mismatch_excluded_and_dated_snapshot_accepted(self):
        self.assertTrue(S.served_ok("gpt-6-astra", "gpt-6-astra-2026-11-01"))
        self.assertTrue(S.served_ok("claude-fable-5-2", "claude-fable-5-2-20261109"))
        self.assertTrue(S.served_ok("gemini-4-argon", "models/gemini-4-argon"))
        self.assertFalse(S.served_ok("gpt-6-astra", "gpt-6-sol"))
        bad = lambda s: "gpt-6-sol" if (s["model"] == "gpt-6-astra" and s["condition"] == "S1" and s["run"] == 1) else s["model"]
        out, *_ = run(copy_t3, served=bad)
        mc = out["manipulation_checks"]["MC_Served"]
        self.assertEqual(mc["n_mismatched"], 30)
        self.assertFalse(mc["pass"])
        self.assertEqual(out["manipulation_checks"]["MC_Complete"]["per_model_condition"]["gpt-6-astra|S1"]["answered"], 60)

    def test_mc_all_pass_on_clean_data(self):
        out, *_ = run(copy_t3)
        mc = out["manipulation_checks"]
        self.assertTrue(mc["MC_Complete"]["pass"])
        self.assertEqual(mc["MC_Complete"]["answered"], 876)
        self.assertEqual(mc["MC_Complete"]["per_model_condition"]["claude-fable-5-2|S0"]["expected"], 202)
        self.assertEqual(mc["MC_Complete"]["per_model_condition"]["claude-fable-5-2|S1"]["expected"], 90)
        self.assertEqual(mc["MC_Complete"]["outside_design"]["n"], 0)
        self.assertTrue(mc["MC_Served"]["pass"])
        self.assertTrue(mc["MC_Window"]["pass"])
        self.assertEqual(mc["MC_Search"]["gpt-6-astra"]["share"], 1.0)
        self.assertFalse(mc["MC_Truncation"]["gpt-6-astra|S0"]["flag_above_5pct"])

    def test_window_over_72_hours_fails(self):
        out, *_ = run(copy_t3, t0="2026-11-01T00:00:00+00:00")
        self.assertFalse(out["manipulation_checks"]["MC_Window"]["pass"])

    def test_completeness_below_98_percent(self):
        first = collections.Counter()

        def f(s):
            if s["model"] == M.MODELS[2] and s["condition"] == "S1":
                first["n"] += 1
                return first["n"] <= 30                       # 30 of 876 = 3.4 % lost
            return False
        out, *_ = run(copy_t3, fail=f)
        self.assertFalse(out["manipulation_checks"]["MC_Complete"]["pass"])
        self.assertAlmostEqual(out["manipulation_checks"]["MC_Complete"]["share"], 846 / 876)
        self.assertIn("gemini-4-argon|S1", out["models_excluded_condition"])        # 60/90 = 66.7 % < 90 %

    def test_calls_outside_design_not_counted(self):
        out, raw, A, B = run(copy_t3, phase_a_everywhere=True)
        mc = out["manipulation_checks"]["MC_Complete"]
        self.assertEqual(len(raw), 876 + 3 * 112 * 5)               # Phase A in the five other condition-runs
        self.assertEqual(mc["answered"], 876)
        self.assertEqual(mc["outside_design"]["n"], 3 * 112 * 5)
        self.assertTrue(mc["pass"])

    def test_parity_gate_blocks_scoring(self):
        raw, A, B = M.build(copy_t3)
        with self.assertRaises(S.Halt):
            S.score_t4(raw, A, B, T3, CFG, {"passed": False, "enforce": True})

    def test_descriptives_cost_and_search(self):
        out, *_ = run(copy_t3)
        d = out["descriptives"]
        c = d["6_cost"]["per_model_condition"]
        self.assertEqual(c["claude-fable-5-2|S0"]["input_tokens"], 202 * 100)
        self.assertAlmostEqual(c["claude-fable-5-2|S0"]["usd"], 202 * 100 * 8 / 1e6 + 202 * 50 * 40 / 1e6, places=9)
        self.assertEqual(c["gemini-4-argon|S0"]["output_tokens_billed"], 202 * 60)       # thinking billed as output
        self.assertAlmostEqual(c["gpt-6-astra|S1"]["usd"], 90 * (100 * 10 + 50 * 50) / 1e6 + 90 * 2 * 0.010, places=9)
        self.assertAlmostEqual(c["gemini-4-argon|S1"]["usd"], 90 * (100 * 2 + 60 * 10) / 1e6 + 90 * 2 * 0.014, places=9)
        self.assertIn("BASIS", d["6_cost"])
        s = d["5_search"]["claude-fable-5-2"]
        self.assertEqual(s["searches_per_call"], 2.0)
        self.assertEqual(s["top20_cited_domains"][0][0], "cited.example")                 # www. dropped
        self.assertEqual(d["1_run_reliability"]["claude-fable-5-2|S0"]["rel1"], 1.0)
        self.assertIsNone(d["1_run_reliability"]["claude-fable-5-2|S0"]["recognition_pairwise_agreement"])
        self.assertEqual(d["2_recognition"]["t4"]["claude-fable-5-2|S0"]["share"], 1.0)
        fp = d["3_floor_persistence"]
        self.assertGreater(fp["share_below_t3_still_below_t4"], 0.5)
        self.assertIn("4_answer_form", d)


class TestParityGates(unittest.TestCase):
    def test_p1_on_t3(self):
        r = S.parity_p1(out_path=None)
        self.assertTrue(r["passed"], r["problems"])
        self.assertEqual((r["brands_compared"], r["k_per_model_exact"], r["pi_hat_exact"], r["phi_exact"]),
                         (112, 112, 112, 112))

    def test_p2_on_t3_raw(self):
        with tempfile.TemporaryDirectory() as d:
            with mock.patch("anthropic.Anthropic", side_effect=AssertionError("API must not be called")):
                r = C.parity_p2(out_path=Path(d) / "p2.json")
        self.assertTrue(r["passed"])
        off = r["url_removal_off"]
        self.assertEqual(off["total_mention_mismatches"], 0)
        self.assertEqual(off["total_recognition_mismatches"], 0)
        self.assertEqual(r["total_calls"], 852)


if __name__ == "__main__":
    unittest.main(verbosity=1)
