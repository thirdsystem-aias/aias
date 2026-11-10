#!/usr/bin/env python3
"""Synthetic tests for the clarification of 2026-11-10 (section 12 (f)-(h); SCORER_NOTES N16-N19): P and C* on
v0.42's own analysis set with "defined" partitions only (as v1.12), and H4 on v1.14's locked R*_S1 read from
v1.14's Stage 1 output, with v1.10's MNP beside it (non-gating) and the blindness guard. No t4 data, no network.
Run:
    PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s osf/methodology/v1_13/scripts/tests -v
"""
import csv
import hashlib
import io
import json
import random
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


def write_stage1(d, units, seed=3, dry_run=True, excluded_subs=(), r1_from=None):
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
           "gate_excluded_substrates": list(excluded_subs), "STAGE1_VERDICT": "FAIL",
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
        self.assertEqual(S.ACTIVATION_TAG["H4_Sep_Ranking"], "v1.14-prereg-r1")

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
        # R*_S1 identical in order to G*: FALSIFIED, and a PASS is re-issued as MARGINAL (downgrade only)
        gs = S.gstar_map(S.brand_stats(answers, self.inp["units"]))
        p2, _ = write_stage1(Path(self.tmp.name) / "c2", self.inp["units"], r1_from=gs)
        src = S.load_ranking_source(p2, "S1", allow_dry=True)
        doc_pass = dict(doc, gate=dict(doc["gate"], verdict="PASS"))
        c2 = S.stage_c2_ranking(doc_pass, answers, self.inp["units"], src, n_perm=49, n_boot=0)
        self.assertEqual(c2["H4_Sep_Ranking"], "FALSIFIED")
        self.assertEqual(c2["gate_reissued"], {"before": "PASS", "after": "MARGINAL", "rule": "downgrade only (section 3)"})
        doc_fail = dict(doc, gate=dict(doc["gate"], verdict="FAIL"))
        self.assertEqual(S.stage_c2_ranking(doc_fail, answers, self.inp["units"], src, 0, 0)["gate_reissued"]["after"],
                         "FAIL")


if __name__ == "__main__":
    unittest.main()
