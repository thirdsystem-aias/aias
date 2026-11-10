#!/usr/bin/env python3
"""Synthetic tests for the clarification of 2026-11-10 (section 12 (f)-(h); SCORER_NOTES N16-N19): P and C* on
v0.42's own analysis set with "defined" partitions only (as v1.12), and H4 on v1.14's locked R*_S1 read from
v1.14's Stage 1 output, with v1.10's MNP beside it (non-gating) and the blindness guard; section 12 (x), N21: H6 on
v1.12's Cov* read from its scored unit table (format refusals, PENDING, C1/C2, hashes). No t4 data, no network.
Run:
    PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s osf/methodology/v1_13/scripts/tests -v
"""
import csv
import hashlib
import io
import json
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_v1_13 as S  # noqa: E402
from test_score_v1_13 import synthetic_t4  # noqa: E402

RANK_COLS = ["answer_id", "wave", "condition", "category", "model", "frame", "run_idx", "status", "n_named",
             "rankable", "list_structured", "rule", "brand", "k_mid", "k_min"]
UNITS = {("v20", "B3"): {"substrate": "v20", "brand_id": "B3", "brand": "B3", "coder_key": "B3", "status": "RESOLVED",
                         "domains": {"b3.test"}}}


def t4rec(cid, phase, cond, run, model=S.FABLE, served="same", status="ok", text="x"):
    return {"call_id": cid, "substrate": "v20", "phase": phase, "condition": cond, "run": run, "model_requested": model,
            "served_model": model if served == "same" else served, "status": status, "text": text, "error": None}


class TestAnalysisSet(unittest.TestCase):
    def test_t4_excluded_is_v042_set(self):
        recs = [t4rec("a_ok", "A", "S0", 1), t4rec("a_s1", "A", "S1", 1), t4rec("a_run2", "A", "S0", 2),
                t4rec("b_run4", "B", "S0", 4), t4rec("b_opus", "B", "S0", 1, model="claude-opus-5-5"),
                t4rec("b_other", "B", "S0", 1, served="gpt-5-other"), t4rec("b_snap", "B", "S0", 1,
                                                                            served="claude-fable-5-2-2026-10-01"),
                t4rec("b_noserved", "B", "S0", 2, served=None), t4rec("b_fail_other", "B", "S1", 3, served="x",
                                                                       status="error", text="")]
        self.assertEqual(S.t4_excluded(recs), {"a_s1", "a_run2", "b_run4", "b_opus", "b_other"})

    def test_dedupe_keeps_last_answered_attempt(self):
        recs = [t4rec("c", "B", "S0", 1, served="other"), t4rec("c", "B", "S0", 1, status="error", text="")]
        self.assertEqual(S.t4_excluded(recs), {"c"})          # the answered attempt (served by another ID) is kept

    def test_p_uses_analysis_set_not_answered_filter(self):
        bt = [{"substrate": "v0.20", "brand": "B3", "pi_N3_S0": "0.5", "phi_N3_S0": "", "phi_partition_N3_S0": "zero"}]
        rows = [{"call_id": "m1", "substrate": "v0.20", "brand": "B3", "model": S.FABLE, "condition": "S0", "run": "1",
                 "recognized": "1"},
                {"call_id": "m2", "substrate": "v0.20", "brand": "B3", "model": S.GPT6, "condition": "S0", "run": "1",
                 "recognized": "0"},
                {"call_id": "m3", "substrate": "v0.20", "brand": "B3", "model": S.GEM4, "condition": "S0", "run": "1",
                 "recognized": "0"}]
        recs = [t4rec("m1", "A", "S0", 1), t4rec("m2", "A", "S0", 1, model=S.GPT6, served=None),
                t4rec("m3", "A", "S0", 1, model=S.GEM4, served="gemini-other")]
        excl = S.t4_excluded(recs)
        self.assertEqual(excl, {"m3"})
        P = S.p_t4(bt, rows, UNITS, "S0", S.PANELS["N3"], excl)
        # m2 (no served ID) counts, as in v0.42 and v1.12; m3 (served by another ID) does not
        self.assertAlmostEqual(P[("v20", "B3")], 100 * (1 / 2 + 2 * 0.5) / 3)

    def test_blank_partition_not_rated(self):
        bt = [{"substrate": "v0.20", "brand": "B3", "phi_N3_S0": "4.5", "phi_partition_N3_S0": ""}]
        rows = [{"call_id": f"c{i}", "substrate": "v0.20", "brand": "B3", "model": S.FABLE, "condition": "S0",
                 "run": "1", "mentioned": "1"} for i in range(8)]
        self.assertIsNone(S.c_star_t4(bt, rows, UNITS, "S0", S.PANELS["N3"])[("v20", "B3")])
        bt[0]["phi_partition_N3_S0"] = "defined"
        self.assertAlmostEqual(S.c_star_t4(bt, rows, UNITS, "S0", S.PANELS["N3"])[("v20", "B3")], 50.0)
        excl = {f"c{i}" for i in range(3)}                     # 5 mentions left: below the floor of 6
        self.assertIsNone(S.c_star_t4(bt, rows, UNITS, "S0", S.PANELS["N3"], excl)[("v20", "B3")])
        rows4 = [dict(r, run="4") for r in rows]               # outside runs 1-3
        self.assertIsNone(S.c_star_t4(bt, rows4, UNITS, "S0", S.PANELS["N3"])[("v20", "B3")])


def write_stage1(d, units, seed=3, dry_run=True, excluded_subs=(), r1_from=None, verdict="FAIL"):
    """v1.14-shaped Stage 1 file (fields as score_v1_14.run_stage1 writes them) and its rank table, keyed on the
    coder substrate and brand. r1_from: {v1.13 unit: value} to set R*_S1."""
    rng = random.Random(seed)
    d = Path(d)
    d.mkdir(parents=True, exist_ok=True)
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(RANK_COLS)
    obs, out, aid = {}, [], 0
    for k in sorted(units):
        cs, b = S.CODER_SUB[k[0]], units[k]["coder_key"]
        n1, n0 = rng.randint(0, 14), rng.randint(0, 14)
        rows = []
        for cond, nn in (("S0", n0), ("S1", n1)):
            for _ in range(nn):
                n_named = rng.randint(2, 8)
                kmin = rng.randint(1, n_named)
                aid += 1
                w.writerow([f"a{aid}", "t4", cond, cs, S.GPT6, "F1", 1, "ok", n_named, 1, 1, "lead_item", b,
                            repr(float(kmin)), kmin])
                w.writerow([f"a{aid}", "t4", cond, cs, S.GPT6, "F1", 1, "ok", n_named, 1, 1, "first_mention", b,
                            repr(1.0), 1])
                if cond == "S1":
                    rows.append((float(kmin), n_named))
        obs[k] = rows
        r1 = float(r1_from[k]) if r1_from and r1_from.get(k) is not None else float(-rng.randint(1, 5))
        out.append({"substrate": cs, "brand": b, "n_ranked_S0": n0, "rated_S0": n0 >= 6,
                    "R_star_S0": float(-rng.randint(1, 5)) if n0 else None,
                    "n_ranked_S1": max(n1, 6) if r1_from and r1_from.get(k) is not None else n1,
                    "R_star_S1": r1 if (n1 or r1_from) else None})
    rt = buf.getvalue().encode("utf-8")
    (d / S.V114_RANK_TABLE).write_bytes(rt)
    doc = {"phase": "v1.14", "stage": "1", "prereg_tag": S.V114_PREREG_TAG, "created_utc": "2026-11-14T00:00:00+00:00",
           "dry_run": dry_run, "rank_table_t4_sha256": hashlib.sha256(rt).hexdigest(),
           "gate_excluded_substrates": list(excluded_subs), "STAGE1_VERDICT": verdict,
           "H1_Sep_Presence": {"verdict": "FALSIFIED"}, "H2_Sep_Consistency": {"verdict": "CONFIRMED"},
           "H4_Sep_Presence_S1": {"verdict": "MARGINAL"}, "component_legs": {"Grounding": "INACTIVE"}, "units": out}
    p = d / "stage1_v1_14.json"
    p.write_text(json.dumps(doc), encoding="utf-8")
    return p, obs


class TestRankingSource(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.inp = synthetic_t4()
        self.p, self.obs = write_stage1(self.tmp.name, self.inp["units"], excluded_subs=("v0.23",))

    def tearDown(self):
        self.tmp.cleanup()

    def test_activation_tag_is_v114(self):
        self.assertEqual(S.ACTIVATION_TAG["H4_Sep_Ranking"], "v1.14-prereg-r2")   # section 12 (y)

    def test_missing_stage1_is_blindness_guard(self):
        with self.assertRaises(S.BlindnessGuard):
            S.read_v114_stage1(Path(self.tmp.name) / "absent.json")
        self.assertTrue(issubclass(S.BlindnessGuard, S.Refused))

    def test_dry_run_refused_for_the_real_record(self):
        with self.assertRaises(SystemExit):
            S.read_v114_stage1(self.p, "S1", allow_dry=False)

    def test_s1_values_floor_and_mapping(self):
        src = S.load_ranking_source(self.p, "S1", allow_dry=True)
        doc = json.loads(self.p.read_text(encoding="utf-8"))
        self.assertEqual(src["sha256"], hashlib.sha256(self.p.read_bytes()).hexdigest())
        m = S.ranking_map(src, self.inp["units"])
        byc = {(S.CODER_SUB[k[0]], u["coder_key"]): k for k, u in self.inp["units"].items()}
        for u in doc["units"]:
            k = byc[(u["substrate"], u["brand"])]
            want = u["R_star_S1"] if (u["n_ranked_S1"] >= 6 and u["substrate"] != "v0.23") else None
            self.assertEqual(m[k], want)
        mnp = S.ranking_map(src["MNP"], self.inp["units"])
        for k, rows in self.obs.items():
            if len(rows) >= 6 and k[0] != "v23":
                self.assertAlmostEqual(mnp[k], 100 * (1 - sum((a - 1) / (n - 1) for a, n in rows) / len(rows)), places=12)

    def test_rank_table_hash_mismatch_halts(self):
        with self.assertRaises(SystemExit):
            S.mnp_from_rank_table(self.p.parent / S.V114_RANK_TABLE, "0" * 64, "S1")

    def test_stage_c1_with_h4(self):
        inp = dict(self.inp, active={"H4_Sep_Ranking": True, "H5_Sep_Sentiment": False, "H6_Sep_Coverage": False},
                   ranking_source=S.load_ranking_source(self.p, "S1", allow_dry=True))
        doc = S.stage_c1(inp, n_perm=99, n_boot=0, sensitivities=False)
        leg = doc["legs"]["H4_Sep_Ranking"][0]
        gs = {(k.split("|")[0], k.split("|")[1]): (v["G_star"] if v["rated"] else None) for k, v in doc["units"].items()}
        want = S.sep_leg(gs, S.ranking_map(inp["ranking_source"], self.inp["units"]), S.SEEDS["H4_Sep_Ranking"], 0, 0)
        self.assertEqual(leg["n"], want["n"])
        self.assertAlmostEqual(leg["rho_w"], want["rho_w"], places=12)
        self.assertTrue(leg["centred"])
        self.assertIn(doc["verdicts"]["H4_Sep_Ranking"], S.VERDICTS - {"INACTIVE"})
        rec = doc["H4_ranking_source"]
        self.assertEqual(rec["condition"], "S1")
        self.assertEqual(rec["stage1_verdict"], "FAIL")
        self.assertFalse(rec["MNP_comparability_non_gating"]["gating"])
        self.assertNotIn("values", rec)
        json.dumps(doc, default=str)

    def test_stage_c1_pending_then_c2(self):
        act = {"H4_Sep_Ranking": True, "H5_Sep_Sentiment": False, "H6_Sep_Coverage": False}
        doc = S.stage_c1(dict(self.inp, active=act, ranking_source=None), n_perm=0, n_boot=0, sensitivities=False)
        self.assertEqual(doc["verdicts"]["H4_Sep_Ranking"], "UNDETERMINED")
        self.assertTrue(doc["reasons"]["H4_Sep_Ranking"].startswith("PENDING"))
        self.assertEqual(doc["H4_ranking_source"]["status"], "PENDING")
        recs = S.dedupe_calls(self.inp["records"])
        answers = S.build_answers(S.select_calls(recs, doc["panel_models"], "S1", "B"),
                                  S.named_index(self.inp["coded_b"], self.inp["units"]), self.inp["units"],
                                  self.inp["classes"])
        none = S.stage_c2_ranking(doc, answers, self.inp["units"], None)
        self.assertEqual(none["H4_Sep_Ranking"], "UNDETERMINED")
        # R*_S1 identical in order to G*: FALSIFIED. With v1.14 SEPARABLE a PASS is re-issued as MARGINAL (downgrade
        # only); with v1.14 FAIL (or MARGINAL / UNDETERMINED) H4 is reported and does not downgrade (N19)
        gs = S.gstar_map(S.brand_stats(answers, self.inp["units"]))
        doc_pass = dict(doc, gate=dict(doc["gate"], verdict="PASS"))
        after = {}
        for v in ("SEPARABLE (Stage 2 pending)", "FAIL", "MARGINAL", "UNDETERMINED"):
            p2, _ = write_stage1(Path(self.tmp.name) / v[:4], self.inp["units"], r1_from=gs, verdict=v)
            src = S.load_ranking_source(p2, "S1", allow_dry=True)
            c2 = S.stage_c2_ranking(doc_pass, answers, self.inp["units"], src, n_perm=49, n_boot=0)
            self.assertEqual(c2["H4_Sep_Ranking"], "FALSIFIED")
            after[v] = c2["gate_reissued"]["after"]
            if v.startswith("SEPARABLE"):
                doc_fail = dict(doc, gate=dict(doc["gate"], verdict="FAIL"))
                self.assertEqual(S.stage_c2_ranking(doc_fail, answers, self.inp["units"], src, 0, 0)
                                 ["gate_reissued"]["after"], "FAIL")
        self.assertEqual(after, {"SEPARABLE (Stage 2 pending)": "MARGINAL", "FAIL": "PASS", "MARGINAL": "PASS",
                                 "UNDETERMINED": "PASS"})

    def test_gate_downgrade_only_when_separable(self):
        v = {"H1_Sep_Presence": "CONFIRMED", "H2_Sep_Consistency": "CONFIRMED", "H3_Run_Reliability": "CONFIRMED",
             "H4_Sep_Ranking": "FALSIFIED", "H5_Sep_Sentiment": "INACTIVE", "H6_Sep_Coverage": "INACTIVE"}
        act = {"H4_Sep_Ranking": True, "H5_Sep_Sentiment": False, "H6_Sep_Coverage": False}
        self.assertEqual(S.gate(v, act, {"H4_Sep_Ranking": True})["verdict"], "MARGINAL")
        g = S.gate(v, act, {"H4_Sep_Ranking": False})
        self.assertEqual(g["verdict"], "PASS")
        self.assertFalse(g["gating"]["H4_Sep_Ranking"])
        self.assertTrue(any("not downgrading" in n for n in g["notes"]))
        self.assertTrue(S.h4_gates({"stage1_verdict": "SEPARABLE (Stage 2 pending)"}))
        self.assertFalse(S.h4_gates({"stage1_verdict": "MARGINAL"}))
        self.assertFalse(S.h4_gates(None))

    def test_sentiment_leg_needs_t4_score(self):
        rec_ = {"conditional_legs": {"H5_Sep_Sentiment": {"tag": "v1.11-prereg-r1", "pushed_before_lock": True}}}
        self.assertFalse(S.activation(rec_)["H5_Sep_Sentiment"])          # archived-wave score: inactive (N20)
        rec_["conditional_legs"]["H5_Sep_Sentiment"]["t4_answers"] = True
        self.assertTrue(S.activation(rec_)["H5_Sep_Sentiment"])
        self.assertIsNone(S.ACTIVATION_TAG["H5_Sep_Sentiment"])


# =========================================================================== H6: v1.12's Cov* reader (section 12 (x), N21)
FAKE_V112_SCORER_SHA = "ab" * 32


def write_v112(d, units, values=None, seed=5, header=None, doc_over=None, row_over=None, extra_rows=()):
    """A v1.12-shaped scored output (unit table + v112_verdicts.json, as score_v1_12.write_outputs writes them).
    values: {v1.13 unit: Cov* or None}; otherwise random. row_over: {column: value} applied to the first row."""
    rng = random.Random(seed)
    d = Path(d)
    d.mkdir(parents=True, exist_ok=True)
    cols = list(header or S.V112_UNIT_COLUMNS)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cols, lineterminator="\r\n", extrasaction="ignore")
    w.writeheader()
    for i, k in enumerate(sorted(units)):
        v = values.get(k) if values is not None else (rng.uniform(0, 100) if rng.random() < 0.85 else None)
        r = {c: "" for c in cols}
        r.update(substrate=S.CODER_SUB[k[0]], brand=units[k]["coder_key"], primary_panel="N3",
                 cov_star="" if v is None else v, rated=int(v is not None), cov_star_N3="" if v is None else v,
                 cov_star_C3=rng.uniform(0, 100), comparator_source="t4 (v0.42, N3, S0)")
        if i == 0 and row_over:
            r.update(row_over)
        w.writerow(r)
    for r in extra_rows:
        w.writerow(r)
    p = d / "v112_unit_table.csv"
    p.write_text(buf.getvalue(), encoding="utf-8")
    doc = {"phase": "v1.12", "prereg_tag": "v1.12-prereg-r1", "primary_panel": "N3", "models_dropped_section_7_3": [],
           "paper_A_verdict": {"verdict": "PASS", "label": "PASS"},
           "parity_gates": {"P1": {"gate": "P1", "passed": True}, "P2": {"passed": True}, "P3": {"passed": True}},
           "inputs": {"raw": "osf/methodology/v1_12/data/v112_raw.jsonl", "raw_sha256": "cd" * 32,
                      "scorer_sha256": FAKE_V112_SCORER_SHA}}
    for k, v in (doc_over or {}).items():
        doc[k] = v
    (d / "v112_verdicts.json").write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    return p


class TestCoverageSource(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.inp = synthetic_t4()
        self.units = self.inp["units"]
        self.n = 0

    def tearDown(self):
        self.tmp.cleanup()

    def _dir(self):
        self.n += 1
        return Path(self.tmp.name) / f"c{self.n}"

    def read(self, p, sha=FAKE_V112_SCORER_SHA):
        return S.read_v112_cov(p, sha, "f" * 40)

    def test_reads_values_and_records_hashes(self):
        vals = {k: (None if i % 5 == 0 else float(i)) for i, k in enumerate(sorted(self.units))}
        p = write_v112(self._dir(), self.units, vals)
        src = self.read(p)
        self.assertEqual(src["sha256"], hashlib.sha256(p.read_bytes()).hexdigest())
        self.assertEqual(src["verdicts_sha256"], hashlib.sha256((p.parent / "v112_verdicts.json").read_bytes()).hexdigest())
        self.assertEqual((src["v1_12_commit"], src["scorer_sha256"], src["column"], src["condition"]),
                         ("f" * 40, FAKE_V112_SCORER_SHA, "cov_star_N3", "S0"))
        self.assertEqual(S.ranking_map(src, self.units), vals)          # blank = NOT RATED (None)
        rec = S.coverage_record(src, self.units)
        self.assertNotIn("values", rec)
        self.assertEqual((rec["units_matched"], rec["units_matched_rated"]),
                         (len(vals), sum(v is not None for v in vals.values())))

    def test_format_errors_refused(self):
        u = self.units
        bad = {
            "header": dict(header=list(S.V112_UNIT_COLUMNS[:-1])),
            "header_order": dict(header=["brand", "substrate"] + list(S.V112_UNIT_COLUMNS[2:])),
            "phase": dict(doc_over={"phase": "v1.13"}),
            "tag": dict(doc_over={"prereg_tag": "v1.12-prereg-r0"}),
            "scorer": dict(doc_over={"inputs": {"scorer_sha256": "00" * 32}}),
            "synthetic_P1": dict(doc_over={"parity_gates": {"P1": {"status": "SKIPPED (not supplied)", "passed": None}}}),
            "substrate": dict(row_over={"substrate": "v19"}),
            "range": dict(row_over={"cov_star_N3": 100.5}),
            "text": dict(row_over={"cov_star_N3": "n/a"}),
            "nan": dict(row_over={"cov_star_N3": "nan"}),
            "panel": dict(row_over={"primary_panel": "C3"}),
            "rated": dict(row_over={"rated": "yes"}),
            "duplicate": dict(extra_rows=[{"substrate": S.CODER_SUB[sorted(u)[0][0]], "brand": u[sorted(u)[0]]["coder_key"],
                                           "primary_panel": "N3", "rated": 0}]),
        }
        for name, kw in bad.items():
            with self.subTest(name), self.assertRaises(S.Refused):
                self.read(write_v112(self._dir(), u, **kw))
        p = write_v112(self._dir(), u)
        (p.parent / "v112_verdicts.json").unlink()
        with self.assertRaises(S.Refused):
            self.read(p)                                                  # no verdict file beside it
        p = write_v112(self._dir(), u)
        p.write_bytes(b"\xff\xfe" + p.read_bytes())
        with self.assertRaises(S.Refused):
            self.read(p)                                                  # not UTF-8
        with self.assertRaises(S.Refused):
            self.read(write_v112(self._dir(), u), sha=None)               # no tagged scorer hash to compare
        with self.assertRaises(S.Refused):
            S.v112_scorer_sha256(None)                                    # lock record without v1.12's commit
        with self.assertRaises(S.Refused):
            self.read(Path(self.tmp.name) / "absent.csv")

    def test_load_coverage_source_uses_the_lock_record_commit(self):
        p = write_v112(self._dir(), self.units)
        anchor = {"conditional_legs": {"H6_Sep_Coverage": {"pushed_before_lock": True, "commit": "e" * 40}}}
        seen = []
        orig = S.v112_scorer_sha256
        S.v112_scorer_sha256 = lambda c: seen.append(c) or FAKE_V112_SCORER_SHA
        try:
            src = S.load_coverage_source(p, anchor)
            S.v112_scorer_sha256 = lambda c: "00" * 32                    # another scorer at the tag: refused
            with self.assertRaises(S.Refused):
                S.load_coverage_source(p, anchor)
        finally:
            S.v112_scorer_sha256 = orig
        self.assertEqual((seen, src["v1_12_commit"]), (["e" * 40], "e" * 40))
        with self.assertRaises(S.Refused):
            S.load_coverage_source(p, {"conditional_legs": {"H6_Sep_Coverage": {"pushed_before_lock": True}}})

    def _answers(self, doc):
        recs = S.dedupe_calls(self.inp["records"])
        return S.build_answers(S.select_calls(recs, doc["panel_models"], "S1", "B"),
                               S.named_index(self.inp["coded_b"], self.units), self.units, self.inp["classes"])

    def test_stage_c1_computed(self):
        src = self.read(write_v112(self._dir(), self.units))
        act = {"H4_Sep_Ranking": False, "H5_Sep_Sentiment": False, "H6_Sep_Coverage": True}
        doc = S.stage_c1(dict(self.inp, active=act, coverage_source=src), n_perm=99, n_boot=0, sensitivities=False)
        gs = {(k.split("|")[0], k.split("|")[1]): (v["G_star"] if v["rated"] else None) for k, v in doc["units"].items()}
        want = S.sep_leg(gs, S.ranking_map(src, self.units), S.SEEDS["H6_Sep_Coverage"], 0, 0)
        leg = doc["legs"]["H6_Sep_Coverage"][0]
        self.assertEqual(leg["n"], want["n"])
        self.assertAlmostEqual(leg["rho_w"], want["rho_w"], places=12)
        self.assertEqual(doc["verdicts"]["H6_Sep_Coverage"], S.sep_verdict([leg]))
        self.assertNotIn("H6_Sep_Coverage", doc["reasons"])
        self.assertEqual(doc["H6_coverage_source"]["sha256"], src["sha256"])
        c2 = S.stage_c2_coverage(doc, self._answers(doc), self.units, src)
        self.assertEqual(c2["note"], "computed at Stage C1")
        json.dumps(doc, default=str)

    def test_stage_c1_pending_then_c2(self):
        act = {"H4_Sep_Ranking": False, "H5_Sep_Sentiment": False, "H6_Sep_Coverage": True}
        doc = S.stage_c1(dict(self.inp, active=act), n_perm=0, n_boot=0, sensitivities=False)
        self.assertEqual(doc["verdicts"]["H6_Sep_Coverage"], "UNDETERMINED")
        self.assertTrue(doc["reasons"]["H6_Sep_Coverage"].startswith("PENDING"))
        self.assertEqual(doc["H6_coverage_source"]["status"], "PENDING")
        answers = self._answers(doc)
        none = S.stage_c2_coverage(doc, answers, self.units, None, unavailable="v1.12 halted at P1")
        self.assertEqual((none["H6_Sep_Coverage"], none["handed_to_paper_B"], none["reason"]),
                         ("UNDETERMINED", True, "v1.12 halted at P1"))
        self.assertIn("score not available", S.stage_c2_coverage(doc, answers, self.units, None)["reason"])
        # Cov* identical in order to G*: FALSIFIED; a PASS is re-issued as MARGINAL (downgrade only)
        gs = S.gstar_map(S.brand_stats(answers, self.units))
        top = max(v for v in gs.values() if v is not None) or 1.0
        src = self.read(write_v112(self._dir(), self.units, {k: (None if v is None else 100 * v / top)
                                                             for k, v in gs.items()}))
        doc_pass = dict(doc, gate=dict(doc["gate"], verdict="PASS"))
        c2 = S.stage_c2_coverage(doc_pass, answers, self.units, src, n_perm=49, n_boot=0)
        self.assertEqual(c2["H6_Sep_Coverage"], "FALSIFIED")
        self.assertEqual((c2["gate_reissued"]["before"], c2["gate_reissued"]["after"]), ("PASS", "MARGINAL"))
        self.assertEqual(c2["H6_coverage_source"]["sha256"], src["sha256"])
        for before in ("MARGINAL", "FAIL", "UNDETERMINED"):           # never upgrades; chains after H4's re-issue
            self.assertEqual(S.stage_c2_coverage(doc_pass, answers, self.units, src, before=before, n_perm=0,
                                                 n_boot=0)["gate_reissued"]["after"], before)
        inactive = dict(doc, gate=dict(doc["gate"], active=dict(act, H6_Sep_Coverage=False)))
        self.assertEqual(S.stage_c2_coverage(inactive, answers, self.units, src), {"H6_Sep_Coverage": "INACTIVE"})

    @unittest.skipUnless(subprocess.run(["git", "rev-parse", "--verify", "-q", "5fd87f6^{commit}"], cwd=str(S.PHASE),
                                        capture_output=True).returncode == 0, "v1.12 commit 5fd87f6 not in this clone")
    def test_scorer_hash_read_from_git(self):
        sha = S.v112_scorer_sha256("5fd87f6")
        blob = subprocess.run(["git", "show", f"5fd87f6:{S.V112_SCORER_REL}"], cwd=str(S.PHASE),
                              capture_output=True).stdout
        self.assertEqual(sha, hashlib.sha256(blob).hexdigest())
        with self.assertRaises(S.Refused):
            S.v112_scorer_sha256("0" * 40)


if __name__ == "__main__":
    unittest.main()
