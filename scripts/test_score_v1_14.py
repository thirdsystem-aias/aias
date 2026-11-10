#!/usr/bin/env python3
"""Unit tests for score_v1_14.py. Stage 1 / Stage 2 tests run on SYNTHETIC t4-shaped data only (no t4
or t5 answer exists, and none is read). The calibration test reads v1.10's hashed rank tables and the
locked P / C* table (archived waves, allowed before the lock) and checks that v1.10's sensitivity
check S3 (candidate MODE) is reproduced exactly.
Run: python3 -m unittest scripts/test_score_v1_14.py   (or python3 scripts/test_score_v1_14.py)"""
import csv
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_v1_10 as R  # noqa: E402
import score_v1_14 as S  # noqa: E402

RAWS = list(S.SUB_MAP)                       # v19 .. v23
SUBS = [S.SUB_MAP[r] for r in RAWS]          # v0.19 .. v0.23
BRANDS = {s: [f"Zq{i}{chr(97 + j)}x" for j in range(8)] for i, s in enumerate(SUBS)}
REGISTRIES = {s: ({b: [] for b in BRANDS[s]}, {b: b for b in BRANDS[s]}) for s in SUBS}
FRAMES = [f"f{j}" for j in range(1, 7)]


def _answer_text(rng, brands, pres, pos, with_url=False):
    named = [b for b in brands if rng.random() < pres[b]]
    order = sorted(named, key=lambda b: pos[b] + rng.normal(0, 0.6))
    lines = ["Here are some options:"]
    for k, b in enumerate(order, 1):
        lines.append(f"{k}. **{b}** - a fine choice.")
    if with_url:
        lines.append("Sources: [review](https://example.com/" + brands[-1].lower() + "-review) and https://x.org/"
                     + brands[-2].lower())
    return "\n".join(lines), set(named)


def build_wave(base: Path, seed=7, served_mismatch=True, s1_only=()):
    """A synthetic t4-shaped tree: osf/v42/data/t4_raw.jsonl, coded tables, brand table, verdicts, probes.
    Position propensity is independent of presence (separable by construction). Brands in `s1_only` are
    never named in a search-off (S0) answer (r2 test; the default leaves every answer unchanged)."""
    rng = np.random.default_rng(seed)
    raw, codedA, codedB, probes = [], [], [], []
    pres = {b: float(p) for s in SUBS for b, p in zip(BRANDS[s], rng.uniform(0.35, 0.95, 8))}
    pos = {b: float(p) for s in SUBS for b, p in zip(BRANDS[s], rng.permutation(8))}
    for raw_s, s in zip(RAWS, SUBS):
        for f in FRAMES:
            probes.append({"substrate": raw_s, "phase": "B", "probe_id": f, "frame_id": f, "prompt": f"Q {s} {f}?",
                           "system": None})
        for b in BRANDS[s]:
            probes.append({"substrate": raw_s, "phase": "A", "probe_id": f"A-{b}", "brand_id": b, "prompt": f"{b}?"})
        for m in S.N3:
            for b in BRANDS[s]:
                cid = f"{raw_s}|A|A-{b}|{m}|S0|1"
                raw.append({"call_id": cid, "substrate": raw_s, "phase": "A", "probe_id": f"A-{b}", "brand_id": b,
                            "frame_id": None, "model_requested": m, "served_model": m, "condition": "S0", "run": 1,
                            "text": "Yes.", "status": "ok", "error": None})
                codedA.append({"call_id": cid, "substrate": s, "brand": b, "brand_id": b, "model": m,
                               "condition": "S0", "run": 1, "probe_id": f"A-{b}", "label": "yes",
                               "recognized": int(rng.random() < 0.8)})
            for cond in S.CONDS:
                for run in S.RUNS:
                    for f in FRAMES:
                        cid = f"{raw_s}|B|{f}|{m}|{cond}|{run}"
                        brands = [b for b in BRANDS[s] if not (cond == "S0" and b in s1_only)]
                        txt, named = _answer_text(rng, brands, pres, pos, with_url=(cond == "S1"))
                        rec = {"call_id": cid, "substrate": raw_s, "phase": "B", "probe_id": f, "brand_id": None,
                               "frame_id": f, "model_requested": m, "served_model": m, "condition": cond,
                               "run": run, "text": txt, "status": "ok", "error": None}
                        raw.append({**rec, "text": "", "status": "error", "error": "overloaded"})   # failed attempt
                        raw.append(rec)
                        for b in BRANDS[s]:
                            codedB.append({"call_id": cid, "substrate": s, "brand": b, "model": m, "condition": cond,
                                           "run": run, "probe_id": f, "frame_id": f, "mentioned": int(b in named)})
    if served_mismatch:   # an answered call served by another model: excluded from the analysis set
        r = dict(raw[-1])
        r.update(call_id=r["call_id"] + "|x", run=4)              # outside the design
        raw.append(r)
        r2 = dict(raw[-2])
        r2.update(call_id=r2["call_id"] + "|y", served_model="some-other-model")   # served by another model
        raw.append(r2)
    d = base / "osf/v42"
    (d / "data/coded").mkdir(parents=True, exist_ok=True)
    (d / "prereg").mkdir(parents=True, exist_ok=True)
    (d / "data/t4_raw.jsonl").write_text("".join(json.dumps(r) + "\n" for r in raw))
    (d / "prereg/probes_v0_42.jsonl").write_text("".join(json.dumps(p) + "\n" for p in probes))
    for raw_s, s in zip(RAWS, SUBS):
        for rows, ph, fields in ((codedA, "a", ["call_id", "substrate", "brand", "brand_id", "model", "condition", "run",
                                                "probe_id", "label", "recognized"]),
                                 (codedB, "b", ["call_id", "substrate", "brand", "model", "condition", "run", "probe_id",
                                                "frame_id", "mentioned"])):
            with open(d / f"data/coded/{raw_s}_phase_{ph}.csv", "w", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=fields)
                w.writeheader()
                for x in rows:
                    if x["substrate"] == s:
                        w.writerow(x)
    # brand table: pi / phi / partition per condition, computed as v0.42 does (checked by MQ8)
    rows = []
    for s in SUBS:
        for b in BRANDS[s]:
            row = {"substrate": s, "brand": b}
            for cond in S.CONDS:
                bt = [{"substrate": s, "brand": b, f"pi_N3_{cond}": "", f"phi_N3_{cond}": "",
                       f"phi_partition_N3_{cond}": ""}]
                rec = S.comparator_parity(bt, codedB, set(), cond)["examples"][0]["recomputed"]
                row[f"pi_N3_{cond}"] = "" if rec[0] is None else repr(rec[0])
                row[f"phi_N3_{cond}"] = "" if rec[1] is None else repr(rec[1])
                row[f"phi_partition_N3_{cond}"] = rec[2]
            rows.append(row)
    with open(d / "v42_brand_table.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    (d / "v42_verdicts.json").write_text(json.dumps({"models_excluded_condition": []}))
    return base


class Statistic(unittest.TestCase):
    def test_modal_position_equals_v1_10_MODE(self):
        rng = np.random.default_rng(1)
        for _ in range(200):
            n = rng.integers(1, 15)
            obs = [(float(k), int(k), 8) for k in rng.integers(1, 8, n)]
            self.assertEqual(S.modal_position([o[1] for o in obs]), R.brand_scores(obs)["MODE"])

    def test_ties_take_the_smallest_mode_and_kmin(self):
        self.assertEqual(S.modal_position([1, 1, 2, 2, 3]), -1.0)
        self.assertEqual(S.modal_position([3, 3, 2, 2]), -2.0)
        self.assertEqual(S.modal_position([4]), -4.0)
        self.assertTrue(np.isnan(S.modal_position([])))
        # tied brands in one answer take the competition min-rank (E7): positions 2 and 2 -> mode 2
        self.assertEqual(R.brand_scores([(2.5, 2, 4), (2.5, 2, 4), (1.0, 1, 4)])["MODE"], -2.0)

    def test_degeneracy_rule(self):
        U = {(c, f"b{i}"): {"rated": True, "MODE": -1.0} for c in "abcde" for i in range(6)}
        self.assertTrue(S.degeneracy(U)["flag_degenerate"])               # one value everywhere
        U = {(c, f"b{i}"): {"rated": True, "MODE": float(-(i % 3) - 1)} for c in "abcde" for i in range(6)}
        d = S.degeneracy(U)
        self.assertFalse(d["flag_degenerate"])
        self.assertAlmostEqual(d["share_most_common_value"], 1 / 3)
        U = {(c, f"b{i}"): {"rated": True, "MODE": -1.0 if c in "abc" else float(-i)} for c in "abcde"
             for i in range(6)}
        self.assertTrue(S.degeneracy(U)["flag_degenerate"])               # no spread in 3 of 5 substrates

    def test_stat_constant_is_mode(self):
        self.assertEqual(S.STAT, "MODE")
        self.assertIn("MODE", R.CANDIDATES)


class T4Inputs(unittest.TestCase):
    def test_strip_urls(self):
        t = "See [Zq0ax review](https://zq0bx.com/x_(y)) and https://zq0cx.com/a. Zq0dx."
        out = S.strip_urls(t)
        self.assertIn("Zq0ax review", out)
        self.assertNotIn("zq0bx", out.lower())
        self.assertNotIn("zq0cx", out.lower())
        self.assertIn("Zq0dx", out)

    def test_url_patterns_equal_v0_42_coder(self):
        p = Path("/Users/pablou/aias/_worktrees/v0.42") / S.V042_CODER_PATH
        if not p.exists():
            self.skipTest("v0.42 worktree not present")
        src = p.read_text()
        self.assertIn(S.MD_LINK_RE.pattern, src)
        self.assertIn(S.URL_RE.pattern, src)

    def test_dedupe_keeps_last_answered_attempt(self):
        recs = [{"call_id": "a", "status": "ok", "text": "x", "error": None},
                {"call_id": "a", "status": "error", "text": "", "error": "e"},
                {"call_id": "b", "status": "error", "text": "", "error": "e"},
                {"call_id": "b", "status": "ok", "text": "y", "error": None},
                {"call_id": "b", "status": "ok", "text": "z", "error": None}]
        d = {r["call_id"]: r for r in S.dedupe_calls(recs)}
        self.assertEqual(d["a"]["text"], "x")
        self.assertEqual(d["b"]["text"], "z")

    def test_exclusions_served_and_design(self):
        base = {"phase": "B", "condition": "S0", "run": 1, "status": "ok", "text": "t", "error": None}
        calls = [{**base, "call_id": "1", "model_requested": "gpt-6-astra", "served_model": "gpt-6-astra-2026-10-01"},
                 {**base, "call_id": "2", "model_requested": "gpt-6-astra", "served_model": "gpt-5"},
                 {**base, "call_id": "3", "model_requested": "gpt-6-astra", "served_model": None},
                 {**base, "call_id": "4", "model_requested": "gpt-6-astra", "served_model": "gpt-6-astra", "run": 4},
                 {**base, "call_id": "5", "model_requested": "claude-opus-5-5", "served_model": "claude-opus-5-5"}]
        self.assertEqual(S.excluded_calls(calls), {"2", "4", "5"})

    def test_comparators_shared_definition(self):
        bt = [{"substrate": "v0.20", "brand": "A", "pi_N3_S0": "0.5", "phi_N3_S0": "1.8", "phi_partition_N3_S0": "defined"},
              {"substrate": "v0.20", "brand": "B", "pi_N3_S0": "1.0", "phi_N3_S0": "", "phi_partition_N3_S0": "saturated"},
              {"substrate": "v0.20", "brand": "C", "pi_N3_S0": "0.0", "phi_N3_S0": "", "phi_partition_N3_S0": "zero"},
              {"substrate": "v0.20", "brand": "D", "pi_N3_S0": "0.1", "phi_N3_S0": "2.0", "phi_partition_N3_S0": "defined"}]
        A = [{"call_id": f"a{m}{b}", "substrate": "v0.20", "brand": b, "model": m, "condition": "S0", "run": 1,
              "recognized": int(m != S.N3[2])} for m in S.N3 for b in "ABCD"]
        A.append({"call_id": "x", "substrate": "v0.20", "brand": "A", "model": S.N3[0], "condition": "S1", "run": 1,
                  "recognized": 0})                                        # S1 recognition never enters
        B = [{"call_id": f"b{i}", "substrate": "v0.20", "brand": b, "model": S.N3[0], "condition": "S0", "run": 1,
              "mentioned": 1} for i in range(10) for b in ("A", "B")]
        B += [{"call_id": "d1", "substrate": "v0.20", "brand": "D", "model": S.N3[0], "condition": "S0", "run": 1,
               "mentioned": 1}]
        c = S.comparators(bt, A, B, set(), "S0")
        self.assertAlmostEqual(c["P"][("v0.20", "A")], 100 * (2 / 3 + 2 * 0.5) / 3)
        self.assertAlmostEqual(c["C"][("v0.20", "A")], 100 * (1 - 1.8 / 9))
        self.assertEqual(c["C"][("v0.20", "B")], 100.0)
        self.assertIsNone(c["C"][("v0.20", "C")])                          # zero partition: NOT RATED
        self.assertIsNone(c["C"][("v0.20", "D")])                          # fewer than 6 mentions: NOT RATED


class Gate(unittest.TestCase):
    def test_final_gate_matrix(self):
        g = S.final_gate
        self.assertEqual(g("CONFIRMED", "CONFIRMED", "CONFIRMED", {}, "CONFIRMED"), "PASS")
        self.assertEqual(g("CONFIRMED", "CONFIRMED", "CONFIRMED", {}, "FALSIFIED"), "MARGINAL")
        self.assertEqual(g("MARGINAL", "CONFIRMED", "CONFIRMED", {}, None), "MARGINAL")
        self.assertEqual(g("CONFIRMED", "CONFIRMED", "FALSIFIED", {}, None), "FAIL")
        self.assertEqual(g("CONFIRMED", "UNDETERMINED", "CONFIRMED", {}, None), "UNDETERMINED")
        self.assertEqual(g("CONFIRMED", "CONFIRMED", "CONFIRMED", {"Coverage": "FALSIFIED"}, None), "FAIL")
        self.assertEqual(g("CONFIRMED", "CONFIRMED", "CONFIRMED", {"Coverage": "PENDING", "Grounding": "INACTIVE"},
                           None), "PASS")
        self.assertEqual(g("FALSIFIED", "UNDETERMINED", "CONFIRMED", {}, None), "FAIL")

    def test_stage1_verdict(self):
        v = S.stage1_verdict
        self.assertEqual(v("CONFIRMED", "CONFIRMED", {}, "CONFIRMED"), "SEPARABLE (Stage 2 pending)")
        self.assertEqual(v("CONFIRMED", "CONFIRMED", {}, "FALSIFIED"), "MARGINAL")
        self.assertEqual(v("MARGINAL", "CONFIRMED", {}, None), "MARGINAL")
        self.assertEqual(v("FALSIFIED", "CONFIRMED", {}, None), "FAIL")
        self.assertEqual(v("UNDETERMINED", "CONFIRMED", {}, None), "UNDETERMINED")

    def test_single_wave_bands_are_v1_10s(self):
        f = R.verdict_single_separability
        self.assertEqual(f(0.30, 40), "CONFIRMED")
        self.assertEqual(f(-0.30, 40), "CONFIRMED")
        self.assertEqual(f(0.3001, 40), "MARGINAL")
        self.assertEqual(f(-0.50, 40), "FALSIFIED")
        self.assertEqual(f(0.10, 29), "UNDETERMINED")


class Stages(unittest.TestCase):
    """Stage 1 and Stage 2 end to end on synthetic t4-shaped trees (dry run: no lock check)."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="v114test_"))
        cls.t4 = build_wave(cls.tmp / "t4", seed=7)
        cls.t5 = cls.tmp / "t5"
        shutil.copytree(cls.t4, cls.t5)            # t5 = t4 repeated exactly (retest ceiling)
        cls.out = cls.tmp / "out"
        cls.s1 = S.run_stage1(dry=True, t4_dir=cls.t4, registries=REGISTRIES, outdir=cls.out / "stage1",
                              expected_units=40, log=lambda *a: None, shuffle_draws=50, boot=False,
                              activation={"Coverage": {"active": True}})

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_analysis_set(self):
        meta = self.s1["analysis_set"]
        self.assertEqual(len(meta["excluded_call_ids"]), 2)           # run 4 + served by another model
        cnt = meta["counts"]
        for s in SUBS:
            for c in S.CONDS:
                self.assertEqual(cnt[f"{s}|{c}|answered"], S.EXPECTED_B_PER_SUB_COND)

    def test_parity_and_join(self):
        self.assertTrue(self.s1["unit_join"]["one_to_one"])
        for s in SUBS:
            self.assertEqual(self.s1["MQ2_mention_parity"]["per_substrate"][s]["agreement"], 1.0)
        self.assertTrue(all(v["passes"] for v in self.s1["MQ8_comparator_parity"].values()))

    def test_separable_by_construction(self):
        h1 = self.s1["H1_Sep_Presence"]
        self.assertGreaterEqual(h1["n"], 30)
        self.assertIn(h1["verdict"], S.VERDICTS)
        self.assertLess(abs(h1["rho"]), 0.5)
        self.assertEqual(self.s1["H_Sep_Components"]["Coverage"]["verdict"], "PENDING")
        self.assertEqual(self.s1["H_Sep_Components"]["Grounding"]["verdict"], "INACTIVE")
        self.assertIn(self.s1["STAGE1_VERDICT"], ("SEPARABLE (Stage 2 pending)", "MARGINAL", "FAIL", "UNDETERMINED"))

    def test_rank_order_reflects_position(self):
        # the generator orders brands by a fixed propensity: rated units' modal positions follow it
        u = [x for x in self.s1["units"] if x["rated_S0"]]
        self.assertTrue(all(x["R_star_S0"] <= -1 for x in u))
        rr = self.s1["D2_run_reliability_and_MQ7"]
        self.assertGreater(rr["rel3"], 0.5)
        self.assertLess(rr["shuffled_mean_rel3"], 0.2)
        self.assertFalse(rr["flag_list_composition_driven"])

    def test_stage1_once_only(self):
        with self.assertRaises(S.Halt):
            S.run_stage1(dry=True, t4_dir=self.t4, registries=REGISTRIES, outdir=self.out / "stage1",
                         expected_units=40, log=lambda *a: None)

    def test_stage2_identical_retest(self):
        s2 = S.run_stage2(dry=True, t4_dir=self.t4, t5_dir=self.t5, registries=REGISTRIES,
                          outdir=self.out / "stage2", stage1_file=self.out / "stage1/stage1_v1_14.json",
                          log=lambda *a: None, boot=False)
        h3 = s2["H3_Retest_Reliability"]
        self.assertAlmostEqual(h3["rho"], 1.0)
        self.assertEqual(h3["verdict"], "CONFIRMED")
        self.assertEqual(s2["models_in_retest"], S.N3)
        self.assertIn(s2["GATE"], ("PASS", "MARGINAL", "FAIL", "UNDETERMINED"))
        self.assertEqual(s2["component_legs_pending"], ["Coverage"])

    def test_stage2_refuses_without_stage1(self):
        with self.assertRaises(S.Halt):
            S.run_stage2(dry=True, t4_dir=self.t4, t5_dir=self.t5, registries=REGISTRIES,
                         outdir=self.tmp / "nowhere", stage1_file=self.tmp / "missing.json", log=lambda *a: None)

    def test_probe_parity_mismatch(self):
        t4p = (self.t4 / S.T4_FILES["probes"]).read_text()
        self.assertTrue(S.probe_parity(t4p, t4p)["identical"])
        self.assertFalse(S.probe_parity(t4p, t4p.replace("Q v0.20 f1?", "Q v0.20 f1 changed?"))["identical"])

    def test_mq2_mismatch_halts(self):
        raw = S.read_jsonl_text((self.t4 / S.T4_FILES["raw"]).read_text())
        src = S.Source(base=self.t4)
        _r, bt, ca, cb, v = S.load_t4(src, src)
        bad = [dict(x) for x in cb]
        for x in bad:
            if x["substrate"] == "v0.20":
                x["mentioned"] = 1 - x["mentioned"]
                break
        with self.assertRaises(S.Halt):
            S.stage1_core(raw, bt, ca, bad, v, REGISTRIES, log=lambda *a: None, boot=False, shuffle_draws=0,
                          expected_units=40)

    def test_join_must_be_one_to_one(self):
        raw = S.read_jsonl_text((self.t4 / S.T4_FILES["raw"]).read_text())
        src = S.Source(base=self.t4)
        _r, bt, ca, cb, v = S.load_t4(src, src)
        with self.assertRaises(S.Halt):
            S.stage1_core(raw, bt[:-1], ca, cb, v, REGISTRIES, log=lambda *a: None, boot=False, shuffle_draws=0,
                          expected_units=40)

    def test_drop_rule_makes_h1_h2_undetermined(self):
        raw = S.read_jsonl_text((self.t4 / S.T4_FILES["raw"]).read_text())
        src = S.Source(base=self.t4)
        _r, bt, ca, cb, _v = S.load_t4(src, src)
        res = S.stage1_core(raw, bt, ca, cb, {"models_excluded_condition": ["gpt-6-astra|S0"]}, REGISTRIES,
                            log=lambda *a: None, boot=False, shuffle_draws=0, expected_units=40)
        self.assertEqual(res["H1_Sep_Presence"]["verdict"], "UNDETERMINED")
        self.assertEqual(res["H2_Sep_Consistency"]["verdict"], "UNDETERMINED")


class R2Fixes(unittest.TestCase):
    """r2 (DEVIATIONS Entry 1): crash fixes made before any t4 answer existed; synthetic data only."""

    def test_brand_ranked_only_with_search_on(self):
        # A brand ranked in search-on (S1) answers but never named in a search-off (S0) answer. r1 raised KeyError
        # in Stage 1's unit listing (after every statistic, before any file was written). r2 lists it with
        # n_ranked_S0 0, rated_S0 False, R_star_S0 None; Stage 2's late component leg reads that listing.
        tmp = Path(tempfile.mkdtemp(prefix="v114r2_"))
        try:
            x = ("v0.20", BRANDS["v0.20"][0])
            t4 = build_wave(tmp / "t4", seed=7, s1_only=(x[1],))
            t5 = tmp / "t5"
            shutil.copytree(t4, t5)
            s1 = S.run_stage1(dry=True, t4_dir=t4, registries=REGISTRIES, outdir=tmp / "out/stage1",
                              expected_units=40, log=lambda *a: None, shuffle_draws=0, boot=False,
                              activation={"Coverage": {"active": True}})
            units = {(u["substrate"], u["brand"]): u for u in s1["units"]}
            self.assertEqual((units[x]["n_ranked_S0"], units[x]["rated_S0"], units[x]["R_star_S0"]), (0, False, None))
            self.assertGreater(units[x]["n_ranked_S1"], 0)
            self.assertIsNotNone(units[x]["R_star_S1"])
            self.assertTrue((tmp / "out/stage1/stage1_v1_14.json").exists())
            cov = tmp / "coverage.csv"
            with open(cov, "w", newline="") as fh:
                w = csv.writer(fh)
                w.writerow(["substrate", "brand", "value"])
                for i, (s, b) in enumerate(sorted(units)):
                    w.writerow([s, b, float(i % 7)])
            s2 = S.run_stage2(dry=True, t4_dir=t4, t5_dir=t5, registries=REGISTRIES, outdir=tmp / "out/stage2",
                              stage1_file=tmp / "out/stage1/stage1_v1_14.json", component_specs=[f"Coverage={cov}"],
                              log=lambda *a: None, boot=False)
            late = s2["component_legs_completed_at_stage2"]["Coverage"]
            per_sub = {}
            for (s, _b), u in units.items():
                per_sub[s] = per_sub.get(s, 0) + int(bool(u["rated_S0"]))
            self.assertEqual(late["n"], sum(n for n in per_sub.values() if n >= 5))   # S0-rated units only
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_lock_guards_name_r2(self):
        # Stage 1 / Stage 2 refusals and --write-anchor name the r2 tag; r1's anchor is kept under its own name, so
        # it cannot satisfy the anchor check (the r2 anchor is written by --write-anchor after the r2 tag is pushed)
        self.assertEqual(S.PREREG_TAG, "v1.14-prereg-r2")
        self.assertEqual(S.ANCHOR_FILE.name, "git_anchor_v1_14.json")
        r1 = S.ANCHOR_FILE.parent / "git_anchor_v1_14_r1.json"
        self.assertEqual(json.loads(r1.read_text())["tag"], "v1.14-prereg-r1")
        if S.ANCHOR_FILE.exists():
            self.assertEqual(json.loads(S.ANCHOR_FILE.read_text())["tag"], S.PREREG_TAG)


class Refusals(unittest.TestCase):
    def test_stage1_refuses_before_the_lock(self):
        keep = S.PREREG_TAG
        S.PREREG_TAG = "v1.14-test-tag-that-does-not-exist"
        try:
            ok, why = S.lock_status(anchor=Path("/nonexistent/anchor.json"))
            self.assertFalse(ok)
            self.assertTrue(any("does not exist" in w for w in why))
            with tempfile.TemporaryDirectory() as d:
                with self.assertRaises(S.Halt):
                    S.run_stage1(outdir=Path(d), scored_ref="HEAD", log=lambda *a: None)
        finally:
            S.PREREG_TAG = keep

    def test_stage2_refuses_before_the_lock(self):
        keep = S.PREREG_TAG
        S.PREREG_TAG = "v1.14-test-tag-that-does-not-exist"
        try:
            with tempfile.TemporaryDirectory() as d:
                f = Path(d) / "stage1.json"
                f.write_text("{}")
                with self.assertRaises(S.Halt):
                    S.run_stage2(outdir=Path(d) / "s2", stage1_file=f, t5_ref="v0.45-acquisition-locked",
                                 log=lambda *a: None)
        finally:
            S.PREREG_TAG = keep

    def test_write_anchor_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "git_anchor_v1_14.json"
            p.write_text("{}")
            with self.assertRaises(S.Halt):
                S.write_anchor("", anchor=p)

    def test_anchor_path_is_in_v1_14_anchor_folder(self):
        self.assertEqual(S.ANCHOR_FILE.parent, S.ROOT / S.V114 / "anchor")


class Calibration(unittest.TestCase):
    """Archived waves (calibration only): v1.10's sensitivity check S3, candidate MODE, reproduced exactly."""

    def test_reproduces_v1_10_S3_MODE(self):
        res = S.calibration(log=lambda *a: None, full=False)
        rep = res["reproduction_of_v1_10_S3_MODE"]
        self.assertTrue(rep["all_identical"], json.dumps(rep, indent=1)[:2000])
        v = json.loads(S.V110_VERDICTS.read_text())["sensitivities"]["S3_candidate_MODE"]["detail"]
        for w in R.WAVES:
            self.assertEqual(res["H1_Sep_Presence"]["per_wave"][w]["rho"], v["H1"]["per_wave"][w]["rho"])
            self.assertEqual(res["H2_Sep_Consistency"]["per_wave"][w]["rho"], v["H2"]["per_wave"][w]["rho"])
        self.assertEqual(res["H3_Rank_Stability"]["rho"], v["H3"]["rho"])

    def test_written_calibration_file(self):
        if not S.CAL_FILE.exists():
            self.skipTest("calibration not yet written")
        c = json.loads(S.CAL_FILE.read_text())
        self.assertTrue(c["reproduction_of_v1_10_S3_MODE"]["all_identical"])
        self.assertTrue(c["check_H4_MNP_equals_v1_10"]["identical"])
        self.assertTrue(c["StageS_split_half_reliability"]["identical"])

    def test_rank_table_hash_check_halts(self):
        with tempfile.TemporaryDirectory() as d:
            v = json.loads(S.V110_VERDICTS.read_text())
            name = next(iter(v["rank_tables"]))
            p = Path(d) / v["rank_tables"][name]["path"]
            p.parent.mkdir(parents=True)
            p.write_text("tampered\n")
            vp = Path(d) / "v.json"
            vp.write_text(json.dumps({"rank_tables": {name: v["rank_tables"][name]}}))
            with self.assertRaises(S.Halt):
                S.load_v110_tables(vp, Path(d))

    def test_precision_note_is_monotone(self):
        pn = S.precision_note(ns=(30, 90), rhos=(0.1,))
        a, b = pn["separability"]
        self.assertLess(a["P_confirmed"], b["P_confirmed"])


class LockManifest(unittest.TestCase):
    def test_locked_files_exist_or_are_listed(self):
        for f in S.LOCKED_FILES:
            self.assertTrue(isinstance(f, str) and not f.startswith("/"))
        self.assertIn("scripts/score_v1_10.py", S.LOCKED_FILES)
        self.assertIn("scripts/test_score_v1_14.py", S.LOCKED_FILES)


if __name__ == "__main__":
    unittest.main(verbosity=2)
