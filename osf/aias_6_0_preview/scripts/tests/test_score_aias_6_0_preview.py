#!/usr/bin/env python3
"""Synthetic-data tests for score_aias_6_0_preview.py (AIAS 6.0 Preview, r1).
No program data are read: every repository used here is a scratch git repository in a temporary directory, and
every output goes to a temporary directory. Run:
python3 -I osf/aias_6_0_preview/scripts/tests/test_score_aias_6_0_preview.py
"""
import copy
import csv
import hashlib
import io
import json
import math
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))
import score_aias_6_0_preview as S  # noqa: E402

R = S.R
V110_BLOB = "0f8b981b2895a325b50629c85f8e0e6ce8e876f5"   # scripts/score_v1_10.py at tag v1.10-prereg-r2


def git_blob(path: Path) -> str:
    b = path.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def units(n_per=(16, 24, 24, 24, 24)):
    return [(f"c{i}", f"b{j:02d}") for i, n in enumerate(n_per) for j in range(n)]


class TestBandsAndFloors(unittest.TestCase):
    def test_band_edges(self):
        self.assertEqual(S.band(0.30, True), "CONFIRMED")
        self.assertEqual(S.band(-0.30, True), "CONFIRMED")
        self.assertEqual(S.band(0.3000001, True), "MARGINAL")
        self.assertEqual(S.band(0.4999999, True), "MARGINAL")
        self.assertEqual(S.band(0.50, True), "FALSIFIED")
        self.assertEqual(S.band(-0.7, True), "FALSIFIED")
        self.assertEqual(S.band(float("nan"), True), "UNDETERMINED")
        self.assertEqual(S.band(0.1, False), "UNDETERMINED")

    def test_floor(self):
        self.assertEqual(S.floor_ok(["a"] * 10 + ["b"] * 10 + ["c"] * 10), (True, 30, 3))
        self.assertFalse(S.floor_ok(["a"] * 10 + ["b"] * 10 + ["c"] * 9)[0])      # 29 units
        self.assertFalse(S.floor_ok(["a"] * 20 + ["b"] * 20)[0])                    # 2 categories
        ok, n, c = S.floor_ok(["a"] * 15 + ["b"] * 15 + ["c"] * 4 + ["d"] * 6)      # c dropped (< 5)
        self.assertEqual((ok, n, c), (True, 36, 3))


class TestSTest(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(1)
        self.scores = {u: {"P": float(rng.normal()), "C": float(rng.normal())} for u in units()}

    def test_matches_v1_10_pooled_within_rho(self):
        res = S.s_test(self.scores, "P", "C", n_perm=0, boot=False)
        keys = sorted(self.scores)
        x = np.array([self.scores[u]["P"] for u in keys])
        y = np.array([self.scores[u]["C"] for u in keys])
        g = np.array([u[0] for u in keys])
        self.assertEqual(res["rho"], R.pooled_within_rho(x, y, g))
        self.assertEqual(res["n"], 112)
        self.assertEqual(res["categories"], 5)

    def test_monotone_within_category_falsified(self):
        sc = {u: {"P": float(i), "C": float(2 * i + 1)} for i, u in enumerate(units())}
        res = S.s_test(sc, "C", "P", n_perm=0, boot=False)
        self.assertAlmostEqual(res["rho"], 1.0)
        self.assertEqual(res["verdict"], "FALSIFIED")
        self.assertEqual(res["pair"], ["P", "C"])                                   # programme order

    def test_not_rated_units_leave_the_pair(self):
        sc = {u: dict(v) for u, v in self.scores.items()}
        for u in list(sc)[:90]:
            sc[u]["C"] = None
        res = S.s_test(sc, "P", "C", n_perm=0, boot=False)
        self.assertEqual(res["verdict"], "UNDETERMINED")                            # 22 units

    def test_carry_and_parity(self):
        own = S.s_test(self.scores, "P", "C", n_perm=0, boot=False)
        out = S.carry(own, {"rho": own["rho"], "verdict": "MARGINAL", "source": "v1.14 H1"})
        self.assertEqual((out["verdict"], out["source"]), ("MARGINAL", "v1.14 H1"))
        with self.assertRaises(S.Halt):
            S.carry(own, {"rho": own["rho"] + 1e-6, "verdict": "CONFIRMED", "source": "x"})


class TestITest(unittest.TestCase):
    def test_formula(self):
        rng = np.random.default_rng(2)
        sc = {u: {"P": float(rng.normal()), "C": float(rng.normal()), "R": float(rng.normal())}
              for u in units()}
        keys = sorted(sc)
        res = S.i_test(sc, keys, "R", ["P", "C"], n_perm=0)
        g = np.array([u[0] for u in keys])
        cols = [R.within_ranks(np.array([sc[u][m] for u in keys]), g) for m in ("R", "P", "C")]
        X = np.column_stack(cols[1:])
        beta, *_ = np.linalg.lstsq(X, cols[0], rcond=None)
        r2 = 1 - ((cols[0] - X @ beta) ** 2).sum() / (cols[0] ** 2).sum()
        r2a = 1 - (1 - r2) * (112 - 5) / (112 - 5 - 2)
        self.assertAlmostEqual(res["R2"], r2, places=12)
        self.assertAlmostEqual(res["R2_adj"], r2a, places=12)
        self.assertAlmostEqual(res["R_adj"], math.sqrt(max(0, r2a)), places=12)

    def test_catches_a_combination_the_pairs_miss(self):
        rng = np.random.default_rng(3)
        sc = {}
        for u in units():
            a = rng.normal()
            b = 0.95 * a + math.sqrt(1 - 0.95 ** 2) * rng.normal()
            sc[u] = {"P": a, "C": b, "R": a - b}
        s_pr = S.s_test(sc, "P", "R", n_perm=0, boot=False)
        s_cr = S.s_test(sc, "C", "R", n_perm=0, boot=False)
        self.assertNotEqual(s_pr["verdict"], "FALSIFIED")
        self.assertNotEqual(s_cr["verdict"], "FALSIFIED")
        res = S.i_test(sc, sorted(sc), "R", ["P", "C"], n_perm=200)
        self.assertEqual(res["verdict"], "FALSIFIED")
        self.assertLess(res["p_perm"], 0.01)

    def test_below_floor_undetermined(self):
        sc = {u: {"P": 1.0 * i, "C": 0.5 * i} for i, u in enumerate(units((6, 6, 6, 6, 5)))}
        self.assertEqual(S.i_test(sc, sorted(sc), "C", ["P"], n_perm=0)["verdict"], "UNDETERMINED")

    def test_incremental_set_ignores_later_members(self):
        sc = {u: {"P": 1.0, "C": 1.0, "R": 1.0, "G": None} for u in units()}
        keys, preds = S.incremental_set(sc, ["P", "C", "R", "G"], "R")
        self.assertEqual((len(keys), preds), (112, ["P", "C"]))
        self.assertEqual(len(S.complete_profile(sc, ["P", "C", "R", "G"])), 0)


class TestStatusAndStructure(unittest.TestCase):
    @staticmethod
    def sres(K, override=None):
        out = {}
        for i, a in enumerate(K):
            for b in K[i + 1:]:
                out[S.pair_key(a, b)] = {"verdict": "CONFIRMED"}
        for k, v in (override or {}).items():
            out[S.pair_key(*k)] = {"verdict": v}
        return out

    def test_component_status(self):
        K = ["P", "C", "R", "Cov"]
        ires = {m: {"verdict": "CONFIRMED"} for m in K[1:]}
        st = lambda x, s, i=ires: S.component_status(x, K, s, i)  # noqa: E731
        self.assertEqual(st("R", self.sres(K)), S.DISTINCT)
        self.assertEqual(st("R", self.sres(K, {("C", "R"): "MARGINAL"})), S.PARTLY)
        s_f = self.sres(K, {("R", "Cov"): "FALSIFIED"})
        self.assertEqual(st("Cov", s_f), S.NOT_DISTINCT)        # the later member is marked
        self.assertEqual(st("R", s_f), S.DISTINCT)              # the earlier one keeps its place
        i_u = dict(ires, R={"verdict": "UNDETERMINED"})
        self.assertEqual(st("R", self.sres(K), i_u), "UNDETERMINED")
        i_f = dict(ires, R={"verdict": "FALSIFIED"})
        self.assertEqual(st("R", self.sres(K, {("P", "R"): "UNDETERMINED"}), i_f), S.NOT_DISTINCT)
        self.assertEqual(st("P", self.sres(K, {("P", "C"): "FALSIFIED"})), S.DISTINCT)   # anchor

    def test_h_structure(self):
        K6 = S.ORDER
        allD = {m: S.DISTINCT for m in K6}
        self.assertEqual(S.h_structure(K6, allD)["verdict"], "CONFIRMED")
        self.assertEqual(S.h_structure(K6, dict(allD, G=S.PARTLY))["verdict"], "PARTIAL")
        self.assertEqual(S.h_structure(K6, dict(allD, G=S.NOT_DISTINCT))["verdict"], "PARTIAL")
        four_not = dict(allD, R=S.NOT_DISTINCT, S=S.NOT_DISTINCT, Cov=S.NOT_DISTINCT, G=S.NOT_DISTINCT)
        self.assertEqual(S.h_structure(K6, four_not)["verdict"], "FALSIFIED")            # d = 2
        self.assertEqual(S.h_structure(K6, dict(four_not, G="UNDETERMINED"))["verdict"], "PARTIAL")
        self.assertEqual(S.h_structure(["P", "C"], {"P": S.DISTINCT, "C": S.DISTINCT})["verdict"],
                         "UNDETERMINED")                                                   # k < 3
        three_u = dict(allD, C="UNDETERMINED", R="UNDETERMINED", S="UNDETERMINED", Cov="UNDETERMINED")
        self.assertEqual(S.h_structure(K6, three_u)["verdict"], "UNDETERMINED")          # k - u < 3
        self.assertEqual(S.h_structure(K6, allD, panel_ok=False)["verdict"], "UNDETERMINED")

    def test_wording_class(self):
        self.assertEqual(S.wording_class("CONFIRMED", 6), "A")
        self.assertEqual(S.wording_class("CONFIRMED", 5), "A_k")
        self.assertEqual(S.wording_class("PARTIAL", 6), "B")
        self.assertEqual(S.wording_class("FALSIFIED", 4), "C")
        self.assertEqual(S.wording_class("UNDETERMINED", 6), "U")


class TestGates(unittest.TestCase):
    def test_ranking(self):
        self.assertEqual(S.gate_ranking("PASS", "SEPARABLE (Stage 2 pending)"), S.PASS)
        self.assertEqual(S.gate_ranking(None, "SEPARABLE (Stage 2 pending)"), S.PASS_RETEST)
        self.assertEqual(S.gate_ranking(None, "MARGINAL"), S.MARGINAL)
        self.assertEqual(S.gate_ranking("FAIL", "SEPARABLE (Stage 2 pending)"), S.FAIL)
        self.assertEqual(S.gate_ranking(None, None), S.NOT_RUN)

    def test_sentiment(self):
        ok = {k: "CONFIRMED" for k in ("H1_Judge_Agreement", "H2_Sep_Presence", "H3_Sep_Consistency",
                                        "H4_Stability_Short", "H5_Sep_Ranking")}
        self.assertEqual(S.gate_sentiment(ok, True), S.PASS_AI)
        self.assertEqual(S.gate_sentiment(ok, True, "PASS"), S.PASS)
        self.assertEqual(S.gate_sentiment(ok, True, "FAIL"), S.FAIL)
        self.assertEqual(S.gate_sentiment(dict(ok, H5_Sep_Ranking="PENDING"), True), S.PASS_AI)
        self.assertEqual(S.gate_sentiment(dict(ok, H2_Sep_Presence="FALSIFIED"), True), S.FAIL)
        self.assertEqual(S.gate_sentiment(dict(ok, H4_Stability_Short="UNDETERMINED"), True), S.UNDET)
        self.assertEqual(S.gate_sentiment(dict(ok, H1_Judge_Agreement="MARGINAL"), True), S.MARGINAL)
        self.assertEqual(S.gate_sentiment(ok, False), S.NOT_RUN)                         # no S_t4

    def test_component_and_inclusion(self):
        self.assertEqual(S.gate_component("INSTRUMENT FAIL"), S.FAIL)
        self.assertEqual(S.gate_component(None), S.NOT_RUN)
        states = {"R": S.MARGINAL, "S": S.NOT_RUN, "Cov": S.PASS, "G": S.FAIL}
        self.assertEqual(S.included_set(states), ["P", "C", "Cov"])
        self.assertEqual(S.included_set({"R": S.PASS_RETEST, "S": S.PASS_AI}), ["P", "C", "R", "S"])


class TestEndToEndSynthetic(unittest.TestCase):
    ALL = {"R": S.PASS_RETEST, "S": S.PASS_AI, "Cov": S.PASS, "G": S.PASS}

    def test_independent_parts_confirmed(self):
        sc, men = S.synthetic(seed=600999)
        res = S.structure(sc, self.ALL, mentions=men, n_perm=200, boot=False)
        self.assertEqual(res["H_Structure"]["verdict"], "CONFIRMED")
        self.assertEqual(res["wording_class"], "A")
        self.assertFalse(res["composite_check"]["adopted"])

    def test_planted_overlap_marks_the_later_part(self):
        sc, men = S.synthetic(seed=600999, overlap={"Cov": ("P", 0.9)})
        res = S.structure(sc, self.ALL, mentions=men, n_perm=200, boot=False)
        self.assertEqual(res["S_tests"]["PxCov"]["verdict"], "FALSIFIED")
        self.assertEqual(res["status"]["Cov"], S.NOT_DISTINCT)
        self.assertEqual(res["status"]["P"], S.DISTINCT)
        self.assertEqual(res["H_Structure"]["verdict"], "PARTIAL")

    def test_copies_of_presence_falsified(self):
        ov = {m: ("P", 0.95) for m in ("R", "S", "Cov", "G")}
        sc, men = S.synthetic(seed=600999, overlap=ov)
        res = S.structure(sc, self.ALL, mentions=men, n_perm=200, boot=False)
        self.assertEqual(res["H_Structure"]["verdict"], "FALSIFIED")
        self.assertEqual(res["wording_class"], "C")

    def test_marginal_part_outside_k_and_descriptive(self):
        sc, men = S.synthetic(seed=600999)
        res = S.structure(sc, dict(self.ALL, G=S.MARGINAL), n_perm=0, boot=False)
        self.assertNotIn("G", res["K"])
        self.assertIn("PxG", res["descriptive_marginal_pairs"])
        self.assertEqual(res["labels"]["G"], "under review")

    def test_panel_incomplete(self):
        sc, _ = S.synthetic(seed=600999)
        res = S.structure(sc, self.ALL, panel_ok=False, n_perm=0, boot=False)
        self.assertEqual((res["H_Structure"]["verdict"], res["wording_class"]), ("UNDETERMINED", "U"))

    def test_deterministic(self):
        sc, men = S.synthetic(seed=600999)
        a = S.structure(sc, self.ALL, mentions=men, n_perm=100, boot=False)
        b = S.structure(sc, self.ALL, mentions=men, n_perm=100, boot=False)
        self.assertEqual(repr(a), repr(b))

    def test_carried_pair_parity_on_paper_a_units(self):
        sc, _ = S.synthetic(seed=600999)
        units_a = [u for u in sc if u[0] != "v0.19"]                 # a Paper A that dropped v0.19
        sub = {u: sc[u] for u in units_a}
        ref = S.s_test(sub, "P", "R", n_perm=0, boot=False)
        carried = {("P", "R"): {"rho": ref["rho"], "verdict": "CONFIRMED", "source": "v1.14 H1",
                                "units": [list(u) for u in units_a]}}
        res = S.structure(sc, self.ALL, carried=carried, n_perm=0, boot=False)
        self.assertEqual(res["S_tests"]["PxR"]["source"], "v1.14 H1")
        bad = {("P", "R"): dict(carried[("P", "R")], units=None)}   # all units: rho differs -> halt
        with self.assertRaises(S.Halt):
            S.structure(sc, self.ALL, carried=bad, n_perm=0, boot=False)

    def test_composite_equals_presence_when_nothing_else_rated(self):
        sc = {u: {"P": float(i), "C": None} for i, u in enumerate(units())}
        cc = S.composite_check(sc, ["P", "C"], {u: 0 for u in sc})
        self.assertAlmostEqual(cc["rho_A_P"], 1.0)
        self.assertFalse(cc["K2_passes"])


class TestCliAndLocks(unittest.TestCase):
    def test_run_refuses_without_the_lock(self):
        # r1: --run refuses before reading anything when tag and anchor are absent (MQ_Lock). A scratch repository
        # is used, never the program repository, so that this test can never score real data.
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["git", "-C", d, "init", "-q"], check=True)
            with self.assertRaises(S.Halt) as cm:
                S.run(root=Path(d), refs={}, out_dir=Path(d) / "out", log=lambda *a: None)
            self.assertIn("MQ_Lock", str(cm.exception))
            self.assertFalse((Path(d) / "out").exists())

    def test_dry_run_writes_only_to_out(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(S.main(["--dry-run", "--out", d, "--n-perm", "50"]), 0)
            self.assertTrue((Path(d) / "dry_run_aias_6_0_preview.json").exists())

    def test_imported_v1_10_is_the_locked_file(self):
        self.assertEqual(git_blob(Path(R.__file__)), V110_BLOB)


class TestSensitivitiesAndLockHelpers(unittest.TestCase):
    def test_sensitivities(self):
        sc, _ = S.synthetic(seed=600999)
        states = {"R": S.PASS, "S": S.PASS, "Cov": S.PASS, "G": S.PASS}
        out = S.sensitivities(sc, states, coi_unit=("v0.19", "B00"))
        self.assertEqual(set(out), {"SA_without_coi_unit", "SB_uncentred", "SC_leave_one_category_out"})
        self.assertEqual(len(out["SC_leave_one_category_out"]), 5)
        self.assertTrue(R.CENTRE_RANKS)                     # the uncentred context is restored
        prim = S.structure(sc, states, n_perm=0, boot=False)
        with R.uncentred():
            unc = S.structure(sc, states, n_perm=0, boot=False)
        self.assertEqual(prim["I_tests"]["G"]["R_adj"], unc["I_tests"]["G"]["R_adj"])   # I-tests stay centred

    def test_lock_manifest_text(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "b.txt").write_text("b")
            (root / "a.txt").write_text("a")
            text = S.lock_manifest_text(["b.txt", "a.txt"], root)
            lines = text.splitlines()
            self.assertEqual([ln.split("  ")[1] for ln in lines], ["a.txt", "b.txt"])
            self.assertEqual(lines[0].split("  ")[0], hashlib.sha256(b"a").hexdigest())

    def test_git_reads_and_mq_blind(self):
        import os
        import subprocess
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)

            def git(*args, date="2026-11-10T10:00:00-06:00"):
                env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.org",
                           GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.org",
                           GIT_AUTHOR_DATE=date, GIT_COMMITTER_DATE=date)
                subprocess.run(["git", "-C", d, *args], check=True, capture_output=True, env=env)
            git("init", "-q")
            (root / "early.csv").write_text("substrate,brand,x\nv0.20,A,1.5\n")
            git("add", "early.csv")
            git("commit", "-q", "-m", "early")
            git("tag", "-a", "lock", "-m", "lock", date="2026-11-11T15:00:00-06:00")
            (root / "late.csv").write_text("substrate,brand,x,rated\nv0.20,A,2.5,1\nv0.20,B,NA,0\n"
                                           "v0.21,C,7,0\n")
            git("add", "late.csv")
            git("commit", "-q", "-m", "late", date="2026-11-15T09:00:00-06:00")
            res = S.mq_blind(root, "lock", [("HEAD", "early.csv"), ("HEAD", "late.csv")])
            self.assertFalse(res["ok"])
            self.assertEqual([e[1] for e in res["early"]], ["early.csv"])
            self.assertTrue(S.mq_blind(root, "lock", [("HEAD", "late.csv")])["ok"])
            log = {}
            vals = S.read_score_csv(root, "HEAD", "late.csv", "x", log, rated_col="rated")
            self.assertEqual(vals, {("v0.20", "A"): 2.5, ("v0.20", "B"): None, ("v0.21", "C"): None})
            self.assertEqual(log["HEAD:late.csv"]["sha256"],
                             hashlib.sha256((root / "late.csv").read_bytes()).hexdigest())
            with self.assertRaises(S.Halt):
                S.mq_blind(root, "no-such-tag", [])


# =====================================================================================================
# r1: a synthetic repository holding every component's scored output at its own ref (no program data)
# =====================================================================================================
V114_BLOB = "c479004c58de79ef017b25c4725e433f74dc42b2"   # scripts/score_v1_14.py at tag v1.14-prereg-r1
MODELS3 = ["claude-fable-5-2", "gpt-6-astra", "gemini-4-argon"]
SUBS = {"v0.19": 16, "v0.20": 24, "v0.21": 24, "v0.22": 24, "v0.23": 24}
RAWSUB = {"v0.19": "v19", "v0.20": "v20", "v0.21": "v21", "v0.22": "v22", "v0.23": "v23"}
QUIET = lambda *a, **k: None  # noqa: E731


def git(d, *args, date="2026-11-10T09:00:00-06:00"):
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.org", GIT_COMMITTER_NAME="t",
               GIT_COMMITTER_EMAIL="t@example.org", GIT_AUTHOR_DATE=date, GIT_COMMITTER_DATE=date)
    return subprocess.run(["git", "-C", str(d), "-c", "commit.gpgsign=false", "-c", "tag.gpgsign=false", *args],
                          check=True, capture_output=True, text=True, env=env).stdout.strip()


def write(root, rel, data):
    p = Path(root) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))


def csv_text(rows, fields=None):
    fields = fields or list(rows[0])
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in fields})
    return buf.getvalue()


def sha(text):
    return hashlib.sha256(text.encode("utf-8") if isinstance(text, str) else text).hexdigest()


def commit(d, msg, date, tag=None):
    git(d, "add", "-A", date=date)
    git(d, "commit", "-q", "-m", msg, date=date)
    if tag:
        git(d, "tag", "-a", tag, "-m", tag, date=date)
    return git(d, "rev-parse", "HEAD")


def unit_names():
    out = []
    for s, n in SUBS.items():
        for i in range(n):
            b = f"B{i:02d}"
            if s == "v0.19" and i == 0:
                b = "Denon"
            if s == "v0.22" and i < 5:
                b = S.DEFUNCT_V022[i]
            if s in ("v0.20", "v0.21") and i == 0:
                b = "Rare Beauty"
            out.append((s, b))
    return out


class Synth:
    """Every input of the Preview, synthetic, committed at the refs the real run will name."""
    LOCK_DATE, A_DATE, S_DATE = "2026-11-11T15:00:00-06:00", "2026-11-14T12:00:00-06:00", "2026-11-15T12:00:00-06:00"

    def __init__(self, d, seed=11, preview_tag="before", h5_gates=True, h6_at_c2=False, cross_panel=False,
                 dropped_s0=False, stage2=False):
        self.d = Path(d)
        rng = np.random.default_rng(seed)
        U = self.units = unit_names()
        git(self.d, "init", "-q")
        for rel, t in {"osf/v42/scripts/score_v0_42.py": "# stub: v42_brand_table.csv v42_verdicts.json\n",
                       "osf/v42/scripts/code_t4_v0_42.py": "# stub coder\n",
                       "scripts/score_v1_14.py": "# stub: stage1_v1_14.json rank_table_t4_v1_14.csv stage2_v1_14.json\n",
                       "osf/methodology/v1_12/scripts/score_v1_12.py": "# stub: v112_unit_table.csv v112_verdicts.json\n",
                       "osf/methodology/v1_13/scripts/score_v1_13.py": "# stub: v1_13_verdicts.json\n",
                       "scripts/score_v1_11.py": "# stub: stage_j_v1_11.json v1_11_verdicts.json\n"}.items():
            write(self.d, rel, t)
        cells, dom, prof = [], [], []
        for i, (s, b) in enumerate(U):
            cell = "" if s in ("v0.19", "v0.23") else ("D" if b in S.DEFUNCT_V022 else "ABC"[i % 3])
            cells.append({"substrate": s, "brand": b, "cell": cell, "wave": "t3"})
            dom.append({"substrate": RAWSUB[s], "brand_id": f"id{i:03d}", "brand": b, "coder_key": b,
                        "status": "NONE" if b in S.DEFUNCT_V022 else "RESOLVED"})
        self.bid = {u: f"{RAWSUB[u[0]]}|id{i:03d}" for i, u in enumerate(U)}
        for w in ("t1", "t2", "t3"):
            for s, b in U:
                rated = int(rng.random() < 0.5)
                prof.append({"wave": w, "substrate": s, "brand": b, "P": round(float(rng.uniform(10, 90)), 6),
                             "C_star": round(float(rng.uniform(10, 90)), 6) if rated else "", "rated": rated})
        write(self.d, "osf/v41/v41_three_wave_table.csv", csv_text(cells))
        write(self.d, "osf/methodology/v1_13/registries/brand_domains_v1_13.csv", csv_text(dom))
        self.prof_text = csv_text(prof)
        write(self.d, "osf/aias_2_0/aias_2_0_profiles.csv", self.prof_text)
        write(self.d, "osf/methodology/v1_12/anchor/osf_anchor_v1_12.json", json.dumps(
            {"conditional_legs": {"H5_Sep_Ranking": {"status": "ACTIVE (tag pushed before this lock)"}}}))
        write(self.d, "osf/methodology/v1_13/anchor/git_anchor_v1_13.json", json.dumps(
            {"conditional_legs": {"H4_Sep_Ranking": {"pushed_before_lock": True},
                                  "H6_Sep_Coverage": {"pushed_before_lock": True}}}))
        self.lock_commit = commit(self.d, "component locks", self.LOCK_DATE)
        for t in ("v0.42-prereg-r1", "v1.14-prereg-r2", "v1.12-prereg-r1", "v1.13-prereg-r1", "v1.11-prereg-r1",
                  "aias-2-0-data-locked"):
            git(self.d, "tag", "-a", t, "-m", t, date=self.LOCK_DATE)
        if preview_tag == "before":
            git(self.d, "tag", "-a", S.PREREG_TAG, "-m", "preview lock", date="2026-11-11T18:00:00-06:00")
        # --- t4 raw (acquisition tag) ---
        A_rows, B_rows, raw = [], [], []
        p_b = {u: float(rng.uniform(0.05, 0.8)) for u in U}
        for s in SUBS:
            brands = [u for u in U if u[0] == s]
            for cond in ("S0", "S1"):
                for m in MODELS3:
                    for run in (1, 2, 3):
                        for f in (1, 2):
                            cid = f"B|{cond}|{m}|{run}|{s}|{f}"
                            raw.append({"call_id": cid, "phase": "B", "condition": cond, "run": run,
                                        "model_requested": m, "served_model": m, "status": "ok", "text": "answer"})
                            B_rows += [{"call_id": cid, "substrate": s, "condition": cond, "model": m, "run": run,
                                        "brand": u[1], "mentioned": int(rng.random() < p_b[u])} for u in brands]
            for m in MODELS3:
                for u in brands:
                    cid = f"A|{m}|{s}|{u[1]}"
                    raw.append({"call_id": cid, "phase": "A", "condition": "S0", "run": 1, "model_requested": m,
                                "served_model": m, "status": "ok", "text": "answer"})
                    A_rows.append({"call_id": cid, "substrate": s, "condition": "S0", "model": m, "run": 1,
                                   "brand": u[1], "recognized": int(rng.random() < 0.7)})
        raw[0]["served_model"] = "another-model"            # one served-ID mismatch: v0.42's analysis set drops it
        write(self.d, "osf/v42/data/t4_raw.jsonl", "".join(json.dumps(r) + "\n" for r in raw))
        commit(self.d, "t4 raw", self.A_DATE, "v0.42-acquisition-locked")
        # --- v0.42 scoring (coded tables, brand table, verdicts) ---
        for s in SUBS:
            write(self.d, f"osf/v42/data/coded/{RAWSUB[s]}_phase_a.csv", csv_text([r for r in A_rows if r["substrate"] == s]))
            write(self.d, f"osf/v42/data/coded/{RAWSUB[s]}_phase_b.csv", csv_text([r for r in B_rows if r["substrate"] == s]))
        bt = []
        for u in U:
            row = {"substrate": u[0], "brand": u[1]}
            for cond in ("S0", "S1"):
                x = rng.random()
                part = "defined" if x < 0.75 else ("saturated" if x < 0.8 else ("zero" if x < 0.9 else "undefined"))
                row.update({f"pi_N3_{cond}": round(float(rng.uniform(0, 0.6)), 6),
                            f"phi_N3_{cond}": round(float(rng.uniform(0.2, 3.0)), 6) if part == "defined" else "",
                            f"phi_partition_N3_{cond}": part})
            bt.append(row)
        self.bt_text = csv_text(bt)
        write(self.d, "osf/v42/v42_brand_table.csv", self.bt_text)
        write(self.d, "osf/v42/v42_verdicts.json", json.dumps({
            "phase": "v0.42", "verdicts": {"H_Gen_Presence": {"verdict": "CONFIRMED"}, "H_Gen_Phi": {"verdict": "MARGINAL"}},
            "models_excluded_condition": ["gemini-4-argon|S0"] if dropped_s0 else []}))
        commit(self.d, "t4 scored", self.S_DATE, "v0.42-scoring-locked")
        excluded = S.V14.excluded_calls(S.V14.dedupe_calls(raw))
        bt_read = list(csv.DictReader(io.StringIO(self.bt_text)))
        comp = S.V14.comparators(bt_read, A_rows, B_rows, excluded, "S0")
        self.P, self.C, self.ment = comp["P"], comp["C"], comp["mentions"]
        # --- v1.14 Stage 1 (and Stage 2) ---
        listed = [u for u in U if self.ment[u] >= 1]          # v1.14 lists units with a rankable mention
        self.R = {u: None for u in U}
        rank_rows, units_json = [], []
        for u in listed:
            r0 = float(-rng.integers(1, 6)) if self.ment[u] >= 6 else None
            self.R[u] = r0
            units_json.append({"substrate": u[0], "brand": u[1], "n_ranked_S0": int(self.ment[u]),
                               "rated_S0": r0 is not None, "R_star_S0": r0, "n_ranked_S1": int(self.ment[u]),
                               "R_star_S1": r0, "P_S0": self.P[u], "C_star_S0": self.C[u], "P_S1": None})
            if r0 is not None:
                for j in range(6):
                    k = int(rng.integers(1, 6))
                    rank_rows.append({"answer_id": f"t4::{u[1]}{j}", "wave": "t4", "condition": "S0",
                                      "category": u[0], "model": MODELS3[j % 3], "frame": "q1", "run_idx": 1 + j % 3,
                                      "status": "ok", "n_named": 5, "rankable": 1, "list_structured": 1,
                                      "rule": "lead_item", "brand": u[1], "k_mid": repr(float(k)), "k_min": k})
        self.rt_text = csv_text(rank_rows, S.V14.RANK_COLS)
        sc = {u: {"P": self.P[u], "C": self.C[u], "R": self.R[u]} for u in U}
        h = {n: S.s_test(sc, a, "R", 0, False) for n, a in (("H1_Sep_Presence", "P"), ("H2_Sep_Consistency", "C"))}
        s1 = {"phase": "v1.14", "stage": "1", "prereg_tag": "v1.14-prereg-r2", "dry_run": False,
              "inputs_read": {"v0.42-scoring-locked:osf/v42/v42_brand_table.csv": {"sha256": sha(self.bt_text)}},
              "rank_table_t4_sha256": sha(self.rt_text), "gate_excluded_substrates": [],
              "STAGE1_VERDICT": "SEPARABLE (Stage 2 pending)", "units": units_json,
              **{n: {"rho": t["rho"], "n": t["n"], "verdict": t["verdict"]} for n, t in h.items()}}
        self.s1_text = json.dumps(s1, indent=1)
        write(self.d, "osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json", self.s1_text)
        write(self.d, "osf/methodology/v1_14/outputs/stage1/rank_table_t4_v1_14.csv", self.rt_text)
        if stage2:
            write(self.d, "osf/methodology/v1_14/outputs/stage2/stage2_v1_14.json", json.dumps(
                {"stage": "2", "dry_run": False, "stage1_sha256": sha(self.s1_text), "GATE": "PASS",
                 "H3_Retest_Reliability": {"verdict": "CONFIRMED", "rho": 0.71, "n": 50}}))
        commit(self.d, "v1.14 stage 1", "2026-11-16T12:00:00-06:00", "v114-scored")
        # --- v1.12 ---
        self.Cov = {u: (float(rng.uniform(20, 80)) if (self.ment[u] >= 3 and rng.random() < 0.85) else None) for u in U}
        self.ut_text = csv_text([{"substrate": u[0], "brand": u[1], "primary_panel": "N3", "cov_star": self.Cov[u],
                                  "rated": int(self.Cov[u] is not None), "cov_star_N3": self.Cov[u]} for u in U])
        sc2 = {u: dict(sc[u], Cov=self.Cov[u]) for u in U}
        t12 = {n: S.s_test(sc2, a, "Cov", 0, False) for n, a in (("H1_Sep_Presence", "P"), ("H2_Sep_Consistency", "C"),
                                                                  ("H5_Sep_Ranking", "R"))}
        pa_legs = {"H1_Sep_Presence": t12["H1_Sep_Presence"]["verdict"], "H3_Sep_NamingRate": "CONFIRMED",
                   "H2_Sep_Consistency": t12["H2_Sep_Consistency"]["verdict"], "H4_Reliability": "CONFIRMED"}
        if h5_gates:
            pa_legs["H5_Sep_Ranking"] = t12["H5_Sep_Ranking"]["verdict"]
        write(self.d, "osf/methodology/v1_12/v112_unit_table.csv", self.ut_text)
        write(self.d, "osf/methodology/v1_12/v112_verdicts.json", json.dumps({
            "phase": "v1.12", "prereg_tag": "v1.12-prereg-r1", "parity_gates": {"P1": {"passed": True}},
            "primary_panel": "N3", "comparators": {"cross_panel": cross_panel}, "models_dropped_section_7_3": [],
            "paper_A_verdict": {"verdict": "PASS", "label": "PASS", "legs": pa_legs, "inactive": ["H6_Sep_Sentiment"]},
            "verdicts": {n: t["verdict"] for n, t in t12.items()}, "legs": {n: {"rho_w": t["rho"]} for n, t in t12.items()},
            "H5_ranking_source": {"sha256": sha(self.s1_text)}}))
        commit(self.d, "v1.12 scored", "2026-11-17T12:00:00-06:00", "v112-scored")
        # --- v1.13 ---
        self.G = {u: (float(rng.uniform(0, 100)) if (u[1] not in S.DEFUNCT_V022 and self.ment[u] >= 2
                                                     and rng.random() < 0.9) else None) for u in U}
        sc3 = {u: dict(sc2[u], G=self.G[u]) for u in U}
        t13 = {n: S.s_test(sc3, a, "G", 0, False) for n, a in (("H1_Sep_Presence", "P"), ("H2_Sep_Consistency", "C"),
                                                                ("H6_Sep_Coverage", "Cov"))}
        legs = {"H1_Sep_Presence": [{"rho_w": 0.05}, {"rho_w": t13["H1_Sep_Presence"]["rho"]}],
                "H2_Sep_Consistency": [{"rho_w": 0.04}, {"rho_w": t13["H2_Sep_Consistency"]["rho"]}],
                "H4_Sep_Ranking": [{"rho_w": 0.11}]}
        verd = {"H1_Sep_Presence": t13["H1_Sep_Presence"]["verdict"], "H3_Run_Reliability": "CONFIRMED",
                "H2_Sep_Consistency": t13["H2_Sep_Consistency"]["verdict"], "H4_Sep_Ranking": "CONFIRMED",
                "H5_Sep_Sentiment": "INACTIVE", "H6_Sep_Coverage": t13["H6_Sep_Coverage"]["verdict"]}
        doc = {"phase": "v1.13", "stage": "C1", "verdicts": verd, "legs": legs, "dropped_models": [],
               "gate": {"verdict": "PASS", "active": {"H4_Sep_Ranking": True, "H5_Sep_Sentiment": False,
                                                      "H6_Sep_Coverage": True}},
               "units": {self.bid[u]: {"G_star": self.G[u], "rated": self.G[u] is not None} for u in U},
               "H4_ranking_source": {"sha256": sha(self.s1_text)}, "H6_coverage_source": {"sha256": sha(self.ut_text)}}
        if h6_at_c2:
            verd["H6_Sep_Coverage"] = "UNDETERMINED"
            doc["H6_coverage_source"] = {"status": "PENDING"}
            doc["stage_C2"] = {"ranking": {"H4_Sep_Ranking": "CONFIRMED", "note": "computed at Stage C1"},
                               "coverage": {"H6_Sep_Coverage": "FALSIFIED", "leg": {"rho_w": t13["H6_Sep_Coverage"]["rho"]},
                                            "H6_coverage_source": {"sha256": sha(self.ut_text)},
                                            "gate_reissued": {"before": "PASS", "after": "MARGINAL"}}}
        else:
            legs["H6_Sep_Coverage"] = [{"rho_w": t13["H6_Sep_Coverage"]["rho"]}]
        write(self.d, "osf/methodology/v1_13/v1_13_verdicts.json", json.dumps(doc))
        commit(self.d, "v1.13 scored", "2026-11-18T12:00:00-06:00", "v113-scored")
        # --- v1.11 (legacy waves) ---
        sj = {"phase": "v1.11", "stage": "J", "scores": {"J1": {
            **{f"F|t3|{s}|{b}": {"S": float(rng.uniform(40, 90)), "rated": True} for (s, b) in U if self.ment[(s, b)] >= 2},
            "F|t2|v0.19|Denon": {"S": 50.0, "rated": True}}}}
        self.sj_text = json.dumps(sj)
        write(self.d, "osf/methodology/v1_11/outputs/stage_j_v1_11.json", self.sj_text)
        write(self.d, "osf/methodology/v1_11/outputs/v1_11_verdicts.json", json.dumps({
            "phase": "v1.11", "stage": "C", "prereg_tag": "v1.11-prereg-r1", "dry_run": False,
            "VERDICTS": {"H1": "CONFIRMED", "H2": "CONFIRMED", "H3": "CONFIRMED", "H4": "CONFIRMED", "H5": "PENDING"},
            "stage_j_sha256": sha(self.sj_text), "noise_guard_applied": False}))
        commit(self.d, "v1.11 scored", "2026-11-19T12:00:00-06:00", "v111-scored")
        if preview_tag == "late":
            git(self.d, "tag", "-a", S.PREREG_TAG, "-m", "late preview lock", date="2026-11-20T12:00:00-06:00")
        self.refs = {"v0.42": "v0.42-scoring-locked", "v1.14": "v114-scored", "v1.12": "v112-scored",
                     "v1.13": "v113-scored", "v1.11": "v111-scored"}

    def inputs(self):
        I = copy.deepcopy(S.INPUTS)
        for name in ("v0.42", "v1.14", "v1.12", "v1.13", "v1.11"):
            sp = I[name]
            sp["lock_commit"] = self.lock_commit
            for fld, bfld in S.PIN_BLOBS:
                if sp.get(fld):
                    sp[bfld] = git(self.d, "rev-parse", f"{sp['lock_tag']}:{sp[fld]}")
        I["v1.12"]["h5_active_at_lock"] = True
        I["v1.13"]["h4_active_at_lock"] = I["v1.13"]["h6_active_at_lock"] = True
        I["aias_2_0"].update(commit=self.lock_commit, sha256=sha(self.prof_text))
        return I


class TestPinsAndReaders(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.syn = Synth(cls.tmp.name)
        cls.I = cls.syn.inputs()

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_imported_v1_14_is_the_locked_file(self):
        self.assertEqual(git_blob(Path(S.V14.__file__)), V114_BLOB)

    def test_real_pins_pending_only_for_the_wednesday_locks(self):
        # r1 leaves exactly these six values PENDING; the coordinator fills them after the Nov 11 locks
        pend = {f"{n}.{k}" for n, sp in S.INPUTS.items() if isinstance(sp, dict) for k, v in sp.items() if v == S.PENDING}
        self.assertLessEqual(pend, {"v0.42.lock_commit", "v1.12.h5_active_at_lock", "v1.12.lock_commit",
                                    "v1.13.h4_active_at_lock", "v1.13.h6_active_at_lock", "v1.13.lock_commit"})
        for name in ("v1.14", "v1.11"):                               # locked components: fully pinned now
            self.assertNotIn(S.PENDING, S.INPUTS[name].values())
        self.assertIsNone(S.INPUTS["S_t4"])                            # not pre-registered at r1 (section 3.4)

    def test_pins(self):
        root = self.syn.d
        self.assertEqual(S.pin_problems(root, self.I), [])
        bad = copy.deepcopy(self.I)
        bad["v1.12"]["scorer_blob"] = "0" * 40
        bad["v1.13"]["lock_commit"] = S.PENDING
        probs = S.pin_problems(root, bad)
        self.assertEqual(len(probs), 2)
        self.assertTrue(any("score_v1_12.py" in p for p in probs) and any("PENDING" in p for p in probs))
        rep = S.pin_report(root, self.I)
        self.assertTrue(rep["v1.12"]["h5_active_at_lock"])
        self.assertTrue(rep["v1.13"]["h4_active_at_lock"] and rep["v1.13"]["h6_active_at_lock"])
        self.assertTrue(all(rep["v1.12"]["output_names_in_tagged_scorer"].values()))
        self.assertEqual(rep["problems"], [])

    def test_read_v042_recomputes_comparators_on_the_analysis_set(self):
        rd = S.Reader(self.syn.d)
        v = S.read_v042(rd, self.I["v0.42"], "v0.42-scoring-locked")
        self.assertEqual(v["n_excluded_calls"], 1)                    # the served-ID mismatch
        self.assertEqual(v["P_S0"], self.syn.P)
        self.assertEqual(v["C_S0"], self.syn.C)
        self.assertEqual(len(v["keys"]), 112)
        self.assertEqual(v["cells"][("v0.22", "Pontiac")], "D")
        self.assertTrue(all(k.split(":", 1)[0] in ("v0.42-scoring-locked", "v0.42-acquisition-locked") for k in rd.log))
        with self.assertRaises(S.Halt):                               # scorer blob at the ref must equal the pin
            S.read_v042(S.Reader(self.syn.d), dict(self.I["v0.42"], scorer_blob="1" * 40), "v0.42-scoring-locked")

    def test_read_v114(self):
        v = S.read_v114(S.Reader(self.syn.d), self.I["v1.14"], "v114-scored")
        self.assertEqual(v["STAGE1_VERDICT"], "SEPARABLE (Stage 2 pending)")
        self.assertIsNone(v["GATE"])
        self.assertEqual(S.gate_ranking(v["GATE"], v["STAGE1_VERDICT"]), S.PASS_RETEST)
        rated = {u for u, x in self.syn.R.items() if x is not None}
        self.assertEqual({u for u, x in v["R_S0"].items() if x is not None}, rated)
        self.assertEqual({u for u, x in v["MNP_S0"].items() if x is not None}, rated)   # 6 rankable rows each
        self.assertLess(len(v["keys"]), 112)                          # v1.14 lists only units with a mention

    def test_read_v112_carried_rules(self):
        v = S.read_v112(S.Reader(self.syn.d), self.I["v1.12"], "v112-scored")
        self.assertEqual(set(v["carried"]), {("P", "Cov"), ("C", "Cov"), ("R", "Cov")})
        self.assertEqual(v["gate"], "PASS")
        self.assertTrue(v["h5_active"])

    def test_read_v113_maps_units_and_carries_s0_legs(self):
        v = S.read_v113(S.Reader(self.syn.d), self.I["v1.13"], "v113-scored")
        self.assertEqual(sorted(v["keys"]), sorted(self.syn.units))    # (v19, id) -> (v0.19, coder key)
        self.assertEqual(v["G"], self.syn.G)
        self.assertEqual(set(v["carried"]), {("P", "G"), ("C", "G"), ("Cov", "G")})
        self.assertNotEqual(v["carried"][("P", "G")]["rho"], 0.05)    # the S0 leg (index 1), not the S1 leg
        self.assertEqual(v["H4_printed"]["rho_w"], 0.11)

    def test_read_v111(self):
        v = S.read_v111(S.Reader(self.syn.d), self.I["v1.11"], "v111-scored")
        self.assertEqual(S.gate_sentiment(v["H"], True), S.PASS_AI)   # H5 PENDING does not block
        self.assertEqual(S.gate_sentiment(v["H"], False), S.NOT_RUN)  # no S_t4: not on N3
        self.assertTrue(all(k in self.syn.units for k in v["keys"]))
        self.assertNotIn(("v0.19", "Denon"), [k for k in v["keys"] if self.syn.ment[k] < 2])

    def test_aias20_pin(self):
        a = S.read_aias20(S.Reader(self.syn.d), self.I["aias_2_0"])
        self.assertEqual(len(a["keys"]), 112)
        with self.assertRaises(S.Halt):
            S.read_aias20(S.Reader(self.syn.d), dict(self.I["aias_2_0"], sha256="0" * 64))


class TestReaderVariants(unittest.TestCase):
    def test_v112_no_h5_carry_unless_it_gated_and_none_cross_panel(self):
        with tempfile.TemporaryDirectory() as d:
            syn = Synth(d, h5_gates=False)
            v = S.read_v112(S.Reader(syn.d), syn.inputs()["v1.12"], "v112-scored")
            self.assertEqual(set(v["carried"]), {("P", "Cov"), ("C", "Cov")})
        with tempfile.TemporaryDirectory() as d:
            syn = Synth(d, cross_panel=True)
            self.assertEqual(S.read_v112(S.Reader(syn.d), syn.inputs()["v1.12"], "v112-scored")["carried"], {})

    def test_v113_gate_as_last_issued_and_h6_from_stage_c2(self):
        with tempfile.TemporaryDirectory() as d:
            syn = Synth(d, h6_at_c2=True)
            v = S.read_v113(S.Reader(syn.d), syn.inputs()["v1.13"], "v113-scored")
            self.assertEqual(v["gate"], "MARGINAL")
            self.assertEqual(v["carried"][("Cov", "G")]["verdict"], "FALSIFIED")

    def test_dry_run_or_tampered_stage1_halts(self):
        with tempfile.TemporaryDirectory() as d:
            syn = Synth(d)
            I = syn.inputs()
            s1 = json.loads(syn.s1_text)
            write(syn.d, "osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json", json.dumps(dict(s1, dry_run=True)))
            commit(syn.d, "dry", "2026-11-21T12:00:00-06:00", "v114-dry")
            with self.assertRaises(S.Halt):
                S.read_v114(S.Reader(syn.d), I["v1.14"], "v114-dry")
            write(syn.d, "osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json", syn.s1_text)
            write(syn.d, "osf/methodology/v1_14/outputs/stage1/rank_table_t4_v1_14.csv", syn.rt_text + "x\n")
            commit(syn.d, "tampered", "2026-11-21T13:00:00-06:00", "v114-tampered")
            with self.assertRaises(S.Halt):
                S.read_v114(S.Reader(syn.d), I["v1.14"], "v114-tampered")


class TestDataLockChecks(unittest.TestCase):
    def test_mq_join(self):
        U = unit_names()
        rep = S.mq_join({"a": U, "b": list(reversed(U))}, {"v1.14": U[:50]})
        self.assertEqual(rep["tables"]["v1.14"]["units_not_listed"], 62)
        with self.assertRaises(S.Halt):
            S.mq_join({"a": U, "b": U[:-1]}, {})                       # a unit missing
        with self.assertRaises(S.Halt):
            S.mq_join({"a": U, "b": U + [U[0]]}, {})                   # a duplicate
        with self.assertRaises(S.Halt):
            S.mq_join({"a": U}, {"v1.11": U[:3] + [("v0.19", "Unknown")]})   # a key outside the 112

    def test_mq_parity_comparators_is_exact(self):
        k = [("v0.19", "A"), ("v0.19", "B")]
        mine = {"P_S0": {k[0]: 40.0, k[1]: 50.0}, "C_S0": {k[0]: None, k[1]: 70.0}}
        theirs = {"keys": k, "P_S0": {k[0]: 40.0, k[1]: 50.0}, "C_S0": {k[0]: None, k[1]: 70.0}}
        self.assertTrue(S.mq_parity_comparators(mine, theirs)["passes"])
        with self.assertRaises(S.Halt):
            S.mq_parity_comparators(mine, dict(theirs, P_S0={k[0]: 40.0, k[1]: 50.0 + 1e-12}))
        with self.assertRaises(S.Halt):
            S.mq_parity_comparators(mine, dict(theirs, C_S0={k[0]: 10.0, k[1]: 70.0}))

    def test_activation_and_cross_records(self):
        I = copy.deepcopy(S.INPUTS)
        I["v1.12"]["h5_active_at_lock"] = True
        with self.assertRaises(S.Halt):
            S.check_activation({"h5_active": False}, None, I)
        v042 = {"brand_table_sha256": "a"}
        v114 = {"inputs_read": {"x:osf/v42/v42_brand_table.csv": {"sha256": "b"}}, "stage1_sha256": "s"}
        with self.assertRaises(S.Halt):
            S.cross_checks(v042, v114, None, None, I)
        ok = S.cross_checks({"brand_table_sha256": "b"}, v114, {"h5_stage1_sha256": "s", "unit_table_sha256": "u"},
                            {"h4_stage1_sha256": None, "h6_unit_table_sha256": "u"}, I)
        self.assertEqual(ok["v1.13_H4_read_the_same_v114_stage1"], "not recorded")


class TestDescriptivesAndSensitivities(unittest.TestCase):
    ALL = {"R": S.PASS_RETEST, "S": S.PASS_AI, "Cov": S.PASS, "G": S.PASS}

    def test_d3_dimensions(self):
        sc, _ = S.synthetic(seed=600999, overlap={"C": ("P", 0.99)})
        d = S.d3_dimensions(sc, ["P", "C", "R", "Cov"], n_draws=50)
        self.assertAlmostEqual(sum(d["eigenvalues"]), 4.0, places=9)
        self.assertGreater(d["eigenvalues"][0], 1.7)                   # P and C nearly one dimension
        self.assertTrue(1.0 <= d["participation_ratio"] < 4.0)
        self.assertGreaterEqual(d["parallel_analysis"]["n_above_null_p95"], 1)

    def test_d5_bridge_and_d6(self):
        U = unit_names()
        rng = np.random.default_rng(5)
        p3 = {u: float(rng.uniform(0, 90)) for u in U}
        p4 = {u: v + 3.0 for u, v in p3.items()}
        b = S.d5_bridge(p4, {u: None for u in U}, p3, {u: None for u in U}, n_boot=200)
        self.assertAlmostEqual(b["P_level_shift"]["mean_t4_minus_t3"], 3.0)
        self.assertAlmostEqual(b["P_level_shift"]["ci90"][0], 3.0)
        self.assertAlmostEqual(b["rho_P"]["rho"], 1.0)
        self.assertTrue(b["rho_C_star"]["below_n_floor"])
        d6 = S.d6_retest(None, {u: {"P": p4[u]} for u in U}, {"P": p3})
        self.assertEqual(d6["P"]["band"], "stable")
        self.assertIn("not supplied", d6["G"]["status"])

    def test_d9_and_profile(self):
        sc, men = S.synthetic(seed=600999)
        u0 = sorted(sc)[0]
        sc[("v0.19", "Denon")] = sc.pop(u0)
        K = ["P", "C", "R", "Cov", "G"]
        d9 = S.d9_coverage(sc, dict(self.ALL, S=S.NOT_RUN), K, {}, men)
        self.assertIn("v0.19|Denon", d9["reported_apart"])
        self.assertEqual(sum(sum(v.values()) for v in d9["rated_parts_per_unit"]["K"].values()), 112)
        sh = d9["rated_share_by_presence_tercile"]["P"]
        self.assertEqual(sh, {"low": 1.0, "middle": 1.0, "high": 1.0})
        rows = S.d4_profile_rows(sc, {"P": {"label": "published AIAS component"}}, {})
        self.assertEqual(len(rows), 112)
        self.assertEqual(rows[0]["P_rated"], 1)

    def test_composite_extensions(self):
        sc, men = S.synthetic(seed=600999)
        res = S.structure(sc, self.ALL, mentions=men, n_perm=0, boot=False)
        cc = res["composite_check"]
        self.assertAlmostEqual(sum(cc["variance_shares_U_K"].values()), 1.0, places=9)
        self.assertTrue(cc["K1_passes"])
        self.assertEqual(cc["floor_set"]["n"], res["U_K"]["n"])

    def test_sensitivities_sd_to_sh(self):
        sc, _ = S.synthetic(seed=600999)
        prim = S.structure(sc, self.ALL, n_perm=0, boot=False)
        mnp = {u: (s["R"] + 1.0 if s["R"] is not None else None) for u, s in sc.items()}   # same order as R*
        out = S.sensitivities(sc, self.ALL, extra={
            "MNP": mnp, "S_legacy": {u: s["S"] for u, s in sc.items()}, "S_legacy_state": S.PASS_AI,
            "S1": {"P": {u: s["P"] for u, s in sc.items()}, "C": {u: s["C"] for u, s in sc.items()},
                   "R": {u: s["R"] for u, s in sc.items()}}}, primary=prim)
        for k in ("SD_S_tests_on_U_K", "SE_without_Sentiment", "SF_Ranking_by_MNP", "SG_Sentiment_legacy_panel",
                  "SH_search_on_variants"):
            self.assertIn(k, out)
        self.assertEqual(out["SF_Ranking_by_MNP"]["S_tests"]["PxR"][0], prim["S_tests"]["PxR"]["rho"])
        self.assertEqual(out["SH_search_on_variants"]["H_Structure"], prim["H_Structure"]["verdict"])
        self.assertNotIn("S", out["SE_without_Sentiment"]["status"])
        self.assertIsInstance(out["verdict_changes"], list)
        ov = S.sensitivities(sc, self.ALL, extra={"MNP": {u: (sc[u]["P"] if sc[u]["R"] is not None else None)
                                                          for u in sc}}, primary=prim)
        self.assertTrue(any(c["sensitivity"] == "SF_Ranking_by_MNP" for c in ov["verdict_changes"]))


class TestRunEndToEnd(unittest.TestCase):
    def test_full_run_on_a_synthetic_repository(self):
        with tempfile.TemporaryDirectory() as d:
            syn = Synth(d, stage2=True)
            out = Path(d) / "out"
            doc = S.run(syn.d, syn.refs, out, syn.inputs(), n_perm=50, n_boot=0, n_pa=20, require_lock=False, log=QUIET)
            self.assertEqual(sorted(p.name for p in out.iterdir()), sorted(S.OUT_NAMES.values()))
            self.assertEqual(doc["K"], ["P", "C", "R", "Cov", "G"])      # S: no S_t4 -> NOT RUN
            self.assertEqual(doc["gate_states"]["R"], S.PASS)            # Stage 2 GATE exists
            src = {k: v["source"] for k, v in doc["structure"]["S_tests"].items()}
            self.assertEqual(src["PxR"], "v1.14 H1_Sep_Presence")
            self.assertEqual(src["RxCov"], "v1.12 H5_Sep_Ranking")
            self.assertTrue(src["PxG"].startswith("v1.13 H1_Sep_Presence"))
            self.assertEqual(src["RxG"], "Preview")
            self.assertTrue(doc["MQ_Parity_comparators"]["passes"])
            self.assertTrue(doc["MQ_Blind"]["ok"])
            self.assertIn(doc["structure"]["H_Structure"]["verdict"], ("CONFIRMED", "PARTIAL", "FALSIFIED", "UNDETERMINED"))
            self.assertEqual(doc["descriptives"]["D6_retest"]["R"]["record"]["verdict"], "CONFIRMED")
            self.assertEqual(doc["labels"]["P"]["bridge"], "continues the published series")
            gates = json.loads((out / S.OUT_NAMES["gates"]).read_text())
            self.assertEqual(gates["K"], doc["K"])
            ins = json.loads((out / S.OUT_NAMES["inputs"]).read_text())["inputs_read"]
            self.assertIn("v114-scored:osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json", ins)
            with self.assertRaises(S.Halt):                               # scored once
                S.run(syn.d, syn.refs, out, syn.inputs(), n_perm=0, n_boot=0, n_pa=0, require_lock=False, log=QUIET)
            bad = syn.inputs()
            bad["v1.13"]["unit_map_blob"] = "2" * 40
            with self.assertRaises(S.Halt):                               # a pin that does not match
                S.run(syn.d, syn.refs, Path(d) / "out2", bad, n_perm=0, n_boot=0, n_pa=0, require_lock=False, log=QUIET)

    def test_late_inputs_are_exploratory_and_dropped_model_stops_structure(self):
        with tempfile.TemporaryDirectory() as d:
            syn = Synth(d, preview_tag="late")
            doc = S.run(syn.d, syn.refs, Path(d) / "o", syn.inputs(), n_perm=0, n_boot=0, n_pa=0,
                        require_lock=False, log=QUIET)
            self.assertFalse(doc["MQ_Blind"]["ok"])
            self.assertEqual(doc["structure"]["S_tests"]["RxG"].get("label"), "exploratory (MQ_Blind)")
            self.assertNotIn("label", doc["structure"]["S_tests"]["PxR"])   # carried: keeps its source's label
        with tempfile.TemporaryDirectory() as d:
            syn = Synth(d, dropped_s0=True)
            doc = S.run(syn.d, syn.refs, Path(d) / "o", syn.inputs(), n_perm=0, n_boot=0, n_pa=0,
                        require_lock=False, log=QUIET)
            self.assertEqual(doc["structure"]["H_Structure"]["verdict"], "UNDETERMINED")
            self.assertEqual(doc["structure"]["wording_class"], "U")

    def test_sentiment_joins_k_when_s_t4_is_locked_and_scored(self):
        with tempfile.TemporaryDirectory() as d:
            syn = Synth(d)
            rng = np.random.default_rng(3)
            rows = [{"substrate": u[0], "brand": u[1], "rated": int(syn.ment[u] >= 2),
                     "S": round(float(rng.uniform(30, 90)), 4) if syn.ment[u] >= 2 else ""} for u in syn.units]
            write(syn.d, "osf/s_t4/s_t4_unit_table.csv", csv_text(rows))
            commit(syn.d, "S_t4 scored", "2026-12-01T12:00:00-06:00", "s-t4-scored")
            git(syn.d, "tag", "-a", "s-t4-prereg-r1", "-m", "S_t4 lock", "HEAD~1", date="2026-11-21T12:00:00-06:00")
            s_t4 = {"ref": "s-t4-scored", "path": "osf/s_t4/s_t4_unit_table.csv", "column": "S", "rated_col": "rated",
                    "lock_tag": "s-t4-prereg-r1"}
            doc = S.run(syn.d, syn.refs, Path(d) / "o", syn.inputs(), s_t4=s_t4, n_perm=0, n_boot=0, n_pa=0,
                        require_lock=False, log=QUIET)
            self.assertEqual(doc["K"], S.ORDER)
            self.assertEqual(doc["gate_states"]["S"], S.PASS_AI)          # v1.11 H1-H4 CONFIRMED, H5 PENDING
            self.assertEqual(doc["structure"]["S_tests"]["SxG"]["source"], "Preview")
            self.assertNotIn("S", doc["sensitivities"]["SE_without_Sentiment"]["status"])
            self.assertEqual(doc["sensitivities"]["SG_Sentiment_legacy_panel"]["state_of_Sentiment"], S.PASS_AI)
            with self.assertRaises(S.Halt):                               # an S_t4 without its lock tag
                S.run(syn.d, syn.refs, Path(d) / "o2", syn.inputs(), s_t4=dict(s_t4, lock_tag="no-such-tag"),
                      n_perm=0, n_boot=0, n_pa=0, require_lock=False, log=QUIET)

    def test_parity_failure_halts(self):
        with tempfile.TemporaryDirectory() as d:
            syn = Synth(d)
            s1 = json.loads(syn.s1_text)
            s1["units"][0]["P_S0"] = (s1["units"][0]["P_S0"] or 0.0) + 1e-9
            write(syn.d, "osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json", json.dumps(s1))
            commit(syn.d, "off", "2026-11-21T12:00:00-06:00", "v114-off")
            with self.assertRaises(S.Halt) as cm:
                S.run(syn.d, dict(syn.refs, **{"v1.14": "v114-off"}), Path(d) / "o", syn.inputs(), n_perm=0,
                      n_boot=0, n_pa=0, require_lock=False, log=QUIET)
            self.assertIn("MQ_Parity", str(cm.exception))


def preview_repo(d):
    """A scratch repository with the Preview's lock files at their real relative paths and a bare origin."""
    root = Path(d) / "repo"
    root.mkdir()
    git(root, "init", "-q")
    files = [S.DEVIATIONS_REL, f"{S.PREVIEW}/prereg/PRE_REGISTRATION_aias_6_0_preview.md"]
    write(root, files[0], "# DEVIATIONS\n\n## Entry 0\n")
    write(root, files[1], "pre-registration\n")
    write(root, S.MANIFEST_REL, S.lock_manifest_text(files, root))
    commit(root, "content lock", "2026-11-11T17:00:00-06:00")
    git(root, "tag", "-a", S.PREREG_TAG, "-m", "lock", date="2026-11-11T17:05:00-06:00")
    origin = Path(d) / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", str(origin)], check=True)
    git(root, "remote", "add", "origin", str(origin))
    return root, files


class TestLockTooling(unittest.TestCase):
    def test_verify_manifest_and_deviations_append_only(self):
        with tempfile.TemporaryDirectory() as d:
            root, files = preview_repo(d)
            self.assertEqual(S.verify_manifest(root, S.MANIFEST_REL, S.PREREG_TAG), [])
            p = root / files[0]
            p.write_text(p.read_text() + "\n## Entry 1\n")              # a post-lock entry (section 14)
            self.assertEqual(S.verify_manifest(root, S.MANIFEST_REL, S.PREREG_TAG), [])
            self.assertTrue(S.verify_manifest(root, S.MANIFEST_REL, None))   # without the tag: exact only
            p.write_text("# DEVIATIONS (edited)\n")                    # the locked text edited: refused
            self.assertTrue(S.verify_manifest(root, S.MANIFEST_REL, S.PREREG_TAG))
            p.write_text("# DEVIATIONS\n\n## Entry 0\n")
            (root / files[1]).write_text("changed\n")
            self.assertTrue(any("PRE_REGISTRATION" in b for b in S.verify_manifest(root, S.MANIFEST_REL, S.PREREG_TAG)))

    def test_write_anchor_and_mq_lock(self):
        with tempfile.TemporaryDirectory() as d:
            root, files = preview_repo(d)
            self.assertFalse(S.mq_lock(root)["ok"])                     # no anchor yet
            with self.assertRaises(S.Halt):                             # tag not pushed yet
                S.write_anchor(root, "osf note", inputs={})
            git(root, "push", "-q", "origin", "HEAD:refs/heads/aias-6.0-preview")
            git(root, "push", "-q", "origin", f"refs/tags/{S.PREREG_TAG}")
            late = {"v0.42": {"brand_table": files[1]}}                 # a "t4 score file" already in the repo
            with self.assertRaises(S.Halt) as cm:
                S.write_anchor(root, "osf note", inputs=late)
            self.assertIn("late", str(cm.exception))
            doc = S.write_anchor(root, "osf note", inputs={})
            self.assertEqual(doc["commit"], git(root, "rev-parse", "HEAD"))
            self.assertEqual(set(doc["locked_files"]), set(files))
            self.assertEqual(doc["lock_manifest_sha256"], sha((root / S.MANIFEST_REL).read_bytes()))
            self.assertEqual(doc["t4_based_score_files_in_repository"], [])
            with self.assertRaises(S.Halt):
                S.write_anchor(root, "osf note", inputs={})             # written once
            self.assertTrue(S.mq_lock(root)["ok"])
            (root / files[1]).write_text("changed after the lock\n")
            self.assertFalse(S.mq_lock(root)["ok"])

    def test_lock_files_cover_section_16(self):
        self.assertEqual(sorted(Path(f).name for f in S.LOCK_FILES), sorted([
            "PRE_REGISTRATION_aias_6_0_preview.md", "precision_aias_6_0_preview.json",
            "precision_aias_6_0_preview.py", "score_aias_6_0_preview.py", "test_score_aias_6_0_preview.py",
            "DEVIATIONS.md", "README.md", "score_v1_10.py", "score_v1_14.py"]))


if __name__ == "__main__":
    unittest.main(verbosity=1)
