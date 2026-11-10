#!/usr/bin/env python3
"""
Unit tests for the clarification of 2026-11-10 (section 12 (f); SCORER_NOTES N32-N34): H5 reads v1.14's locked R*
from v1.14's Stage 1 output (R*_S0, v1.14's rated set, SHA-256 recorded), v1.10's MNP is reported beside it as a
non-gating comparability figure from v1.14's hashed rank table, and the leg refuses to run before that output
exists (blindness guard). Synthetic Stage 1 files only: no t4 answer exists, none is read, no API is called. Run from
the repository root:

    python3 -m unittest discover -s osf/methodology/v1_12/scripts/tests -p "test_*.py" -v
"""
import csv
import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import score_v1_12 as S             # noqa: E402
from test_pipeline_v1_12 import inputs, synth_registry   # noqa: E402

RANK_COLS = ["answer_id", "wave", "condition", "category", "model", "frame", "run_idx", "status", "n_named",
             "rankable", "list_structured", "rule", "brand", "k_mid", "k_min"]


def write_stage1(d, registry=None, seed=7, dry_run=True, excluded_subs=(), r_from=None, phase="v1.14"):
    """A v1.14-shaped Stage 1 file (fields as score_v1_14.run_stage1 writes them) and its rank table. Returns
    (stage1 path, {unit: list of (k_mid, n) S0 lead-item rows})."""
    registry = registry or synth_registry()
    rng = np.random.default_rng(seed)
    d = Path(d)
    d.mkdir(parents=True, exist_ok=True)
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(RANK_COLS)
    obs, units = {}, []
    aid = 0
    for sub in S.CATS:
        for i, b in enumerate(registry[sub]):
            k = (sub, b)
            n_s0 = int(rng.integers(0, 15))
            n_s1 = int(rng.integers(0, 15))
            rows = []
            for cond, nn in (("S0", n_s0), ("S1", n_s1)):
                for _ in range(nn):
                    n_named = int(rng.integers(2, 9))
                    kmin = int(rng.integers(1, n_named + 1))
                    kmid = float(kmin) + (0.5 if rng.random() < 0.2 and kmin < n_named else 0.0)
                    aid += 1
                    base = [f"a{aid}", "t4", cond, sub, S.FABLE, "F1", 1, "ok", n_named, 1, 1]
                    w.writerow(base + ["lead_item", b, repr(kmid), kmin])
                    w.writerow(base + ["first_mention", b, repr(1.0), 1])          # must be ignored
                    if cond == "S0":
                        rows.append((kmid, n_named))
            obs[k] = rows
            r0 = float(r_from[k]) if r_from and k in r_from else float(-rng.integers(1, 6))
            units.append({"substrate": sub, "brand": b, "n_ranked_S0": n_s0, "rated_S0": n_s0 >= 6,
                          "R_star_S0": r0 if n_s0 else None, "n_ranked_S1": n_s1,
                          "R_star_S1": float(-rng.integers(1, 6)) if n_s1 else None, "P_S0": None, "C_star_S0": None,
                          "P_S1": None})
    w.writerow(["a_missing", "t4", "S0", "v0.20", S.GPT6, "F2", 2, "missing", 0, 0, 0, "", "", "", ""])
    rt = buf.getvalue().encode("utf-8")
    (d / S.V114_RANK_TABLE).write_bytes(rt)
    doc = {"phase": phase, "stage": "1", "created_utc": "2026-11-14T00:00:00+00:00", "prereg_tag": S.V114_PREREG_TAG,
           "dry_run": dry_run, "rank_table_t4_sha256": hashlib.sha256(rt).hexdigest(),
           "gate_excluded_substrates": list(excluded_subs), "STAGE1_VERDICT": "MARGINAL",
           "H1_Sep_Presence": {"verdict": "MARGINAL"}, "H2_Sep_Consistency": {"verdict": "CONFIRMED"},
           "H4_Sep_Presence_S1": {"verdict": "CONFIRMED"}, "component_legs": {"Coverage": "INACTIVE"}, "units": units}
    p = d / "stage1_v1_14.json"
    p.write_text(json.dumps(doc, indent=1), encoding="utf-8")
    return p, obs


class TestReader(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.p, self.obs = write_stage1(self.tmp.name, excluded_subs=("v0.23",))
        self.doc = json.loads(self.p.read_text(encoding="utf-8"))

    def tearDown(self):
        self.tmp.cleanup()

    def test_s0_rated_set_and_sha(self):
        src = S.read_v114_stage1(self.p, "S0", allow_dry=True)
        self.assertEqual(src["sha256"], hashlib.sha256(self.p.read_bytes()).hexdigest())
        self.assertEqual(src["stage1_verdict"], "MARGINAL")
        self.assertEqual(src["v1_14_verdicts"]["H1_Sep_Presence"], "MARGINAL")
        for u in self.doc["units"]:
            k = (u["substrate"], u["brand"])
            want = u["R_star_S0"] if (u["rated_S0"] and u["substrate"] != "v0.23") else None
            self.assertEqual(src["values"][k], want)
        self.assertEqual(src["rated_units"], sum(v is not None for v in src["values"].values()))
        self.assertTrue(all(v is None for k, v in src["values"].items() if k[0] == "v0.23"))

    def test_s1_uses_v114_floor(self):
        src = S.read_v114_stage1(self.p, "S1", allow_dry=True)
        for u in self.doc["units"]:
            k = (u["substrate"], u["brand"])
            want = u["R_star_S1"] if (u["n_ranked_S1"] >= 6 and u["substrate"] != "v0.23") else None
            self.assertEqual(src["values"][k], want)

    def test_dry_run_refused_for_the_real_record(self):
        with self.assertRaises(S.Halt):
            S.read_v114_stage1(self.p, "S0", allow_dry=False)

    def test_not_a_v114_file(self):
        p, _ = write_stage1(Path(self.tmp.name) / "x", phase="v1.10")
        with self.assertRaises(S.Halt):
            S.read_v114_stage1(p, "S0", allow_dry=True)

    def test_mnp_from_rank_table(self):
        m = S.mnp_from_rank_table(self.p.parent / S.V114_RANK_TABLE, self.doc["rank_table_t4_sha256"], "S0", ("v0.23",))
        self.assertEqual(m["status"], "COMPUTED")
        for k, rows in self.obs.items():
            if len(rows) >= 6 and k[0] != "v0.23":
                want = 100.0 * (1.0 - np.mean([(km - 1.0) / (n - 1.0) for km, n in rows]))
                self.assertAlmostEqual(m["values"][k], want, places=12)
            elif k in m["values"]:
                self.assertIsNone(m["values"][k])

    def test_rank_table_hash_mismatch_halts(self):
        with self.assertRaises(S.Halt):
            S.mnp_from_rank_table(self.p.parent / S.V114_RANK_TABLE, "0" * 64, "S0")
        m = S.mnp_from_rank_table(self.p.parent / "absent.csv", "0" * 64, "S0")
        self.assertEqual(m["status"], "NOT_COMPUTED")


class TestBlindnessGuard(unittest.TestCase):
    def test_missing_stage1_refuses(self):
        with self.assertRaises(S.BlindnessGuard):
            S.read_v114_stage1("/nonexistent/stage1_v1_14.json")
        self.assertTrue(issubclass(S.BlindnessGuard, S.Refused))

    def test_activation(self):
        self.assertEqual(S.h5_inputs(None, real=False), (False, None, None))
        with mock.patch.object(S, "local_tag_exists", return_value=True):
            with self.assertRaises(S.BlindnessGuard):
                S.h5_inputs(None, real=True)
            self.assertEqual(S.h5_inputs("/nonexistent.json", real=True, unavailable="Stage 1 halted"),
                             (True, None, None))
        with mock.patch.object(S, "local_tag_exists", return_value=False):
            self.assertEqual(S.h5_inputs(None, real=True), (False, None, None))

    def test_real_run_refuses_before_reading_any_record(self):
        with mock.patch.object(S, "tag_on_origin", return_value=True), \
                mock.patch.object(S, "local_tag_exists", return_value=True):
            with self.assertRaises(S.BlindnessGuard):
                S.run_score("/nonexistent/raw.jsonl", "/nonexistent/coded", S.T4_DEFAULTS, "/dev/null", "/dev/null",
                            S.Cfg(9, 9), True)

    def test_v110_csv_route_removed(self):
        """H5 no longer takes v1.10's MNP as a CSV: an H5 entry in extra_paths is ignored by run_score."""
        import inspect
        src = inspect.getsource(S.run_score)
        self.assertIn('extra_paths.pop("H5_Sep_Ranking", None)', src)


class TestScoreWithH5(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.inp = inputs(0)
        p, _ = write_stage1(cls.tmp.name, cls.inp["registry"])
        cls.src = S.load_ranking_source(p, "S0", allow_dry=True)
        cls.inp.update(active={"H5_Sep_Ranking": True}, extra={"H5_Sep_Ranking": cls.src["values"]},
                       h5_source=cls.src)
        cls.doc, cls.rows = S.score_coverage(cls.inp, S.Cfg(49, 0), {"enforce": True}, with_sensitivities=False)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_h5_uses_v114_r_star_and_gates(self):
        leg = self.doc["legs"]["H5_Sep_Ranking"]
        cov = {(r["substrate"], r["brand"]): r["cov_star"] for r in self.rows}
        _k, x, y, g, info = S.paired(cov, self.src["values"])
        self.assertEqual(leg["n"], info["n"])
        self.assertAlmostEqual(leg["rho_w"], S.rho_w(x, y, g), places=12)
        self.assertTrue(leg["centred"])
        self.assertIn("H5_Sep_Ranking", self.doc["paper_A_verdict"]["legs"])

    def test_source_record_and_mnp_non_gating(self):
        rec = self.doc["H5_ranking_source"]
        self.assertEqual(rec["sha256"], self.src["sha256"])
        self.assertEqual(rec["condition"], "S0")
        self.assertEqual(rec["stage1_verdict"], "MARGINAL")
        self.assertNotIn("values", rec)
        m = rec["MNP_comparability_non_gating"]
        self.assertFalse(m["gating"])
        cov = {(r["substrate"], r["brand"]): r["cov_star"] for r in self.rows}
        _k, x, y, g, _i = S.paired(cov, self.src["MNP"]["values"])
        self.assertAlmostEqual(m["rho_w"], S.rho_w(x, y, g), places=12)
        self.assertNotIn("MNP", self.doc["paper_A_verdict"]["legs"])
        json.dumps(S._clean(self.doc), allow_nan=False)

    def test_unavailable_is_undetermined(self):
        inp = inputs(1)
        inp.update(active={"H5_Sep_Ranking": True}, extra={}, h5_source=None, h5_unavailable="Stage 1 halted (test)")
        doc, _ = S.score_coverage(inp, S.Cfg(19, 0), {"enforce": True}, with_sensitivities=False)
        self.assertEqual(doc["verdicts"]["H5_Sep_Ranking"], "UNDETERMINED")
        self.assertEqual(doc["H5_ranking_source"]["status"], "NOT_AVAILABLE")
        self.assertIn("Stage 1 halted", doc["H5_ranking_source"]["reason"])


if __name__ == "__main__":
    unittest.main()
