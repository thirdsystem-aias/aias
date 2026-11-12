#!/usr/bin/env python3
"""
End to end with Paper A's own scorer: Paper A's test helpers make Coverage-shaped raw lines, the mention rows the coder
would give and a t4 bundle (osf/methodology/v1_12/scripts/tests/test_pipeline_v1_12.py, imported unchanged); Paper A's
score_coverage and write_outputs (imported unchanged) write v112_verdicts.json and v112_unit_table.csv; v1.19's
run_real then reads those files. Checks B-P1 against Paper A's own unit-table writer. The coder itself is not run here
(Paper A's helpers supply the rows it would give); its end-to-end run is an r1 step. Synthetic data only.

    python3 -m unittest discover -s osf/methodology/v1_19/scripts/tests -p "test_*.py" -v
"""
import csv
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import score_v1_19 as B   # noqa: E402

A = B.A
sys.path.insert(0, str(B.A_SCRIPTS / "tests"))
import test_pipeline_v1_12 as TP   # noqa: E402  (Paper A's test helpers)


class PaperAOutputsToPaperB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="v119_e2e_"))
        d = cls.tmp
        raw, rows, reg = TP.make_coverage(5)
        t4raw, ca, cb = TP.make_t4(6, reg)
        excl, window = A.t4_excluded(t4raw)
        t4 = {"coded_a": ca, "coded_b": cb, "brand_table": TP.brand_table_from(cb, excl, reg), "excluded": excl,
              "verdicts": {"models_excluded_condition": []}, "window": window}
        inp = {"raw": raw, "mentions": rows, "registry": reg, "probes": A.load_probes(), "t4": t4,
               "profiles": TP.profiles_for(reg)}
        doc, unit_rows = A.score_coverage(inp, A.Cfg(9, 9), {"enforce": True}, with_sensitivities=False)
        A.write_outputs(doc, unit_rows, d / "A/v112_verdicts.json", d / "A/v112_unit_table.csv")
        (d / "A/v112_raw.jsonl").write_text("".join(json.dumps(r) + "\n" for r in raw), encoding="utf-8")
        A.write_coded(rows, reg, {"synthetic": True}, d / "A/coded")
        (d / "t4/coded").mkdir(parents=True)
        (d / "t4/t4_raw.jsonl").write_text("".join(json.dumps(r) + "\n" for r in t4raw), encoding="utf-8")
        for sub, rs in A.RAW_SUB.items():
            with open(d / f"t4/coded/{rs}_phase_b.csv", "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=["call_id", "substrate", "brand", "model", "condition", "run",
                                                  "probe_id", "frame_id", "mentioned"])
                w.writeheader()
                w.writerows([r for r in cb if r["substrate"] == sub])
        # v0.42's channel labels: F0-F2 category, F3-F5 cultural, for the trio (as probes_v0_42.jsonl lays them out)
        (d / "t4/probes.jsonl").write_text("".join(
            json.dumps({"probe_id": f"F{f}", "substrate": A.RAW_SUB[s], "phase": "B",
                        "channel": "R_cat" if f < 3 else "R_cult"}) + "\n" for s in B.TRIO for f in range(6)),
            encoding="utf-8")
        with open(d / "roster.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["substrate", "brand", "recall_floor_flag_F", "defunct_D"])
            w.writeheader()
            for s in A.CATS:
                for i, b in enumerate(reg[s]):
                    w.writerow({"substrate": s, "brand": b, "recall_floor_flag_F": int(i % 2 == 0),
                                "defunct_D": int(b in A.DEFUNCT)})
        cls.a_doc = doc
        cls.paths = {"a_raw": d / "A/v112_raw.jsonl", "a_coded": d / "A/coded", "a_verdicts": d / "A/v112_verdicts.json",
                     "a_unit_table": d / "A/v112_unit_table.csv", "a_probes": A.PROBES_PATH, "roster": d / "roster.csv",
                     "t4_raw": d / "t4/t4_raw.jsonl", "t4_coded": d / "t4/coded", "t4_probes": d / "t4/probes.jsonl",
                     "decision": d / "none.json"}

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_paper_A_verdict_routes_paper_B(self):
        """Paper A's own synthetic verdict decides: PASS runs; anything else gives the not-run record or waits."""
        paths = dict(self.paths, out=self.tmp / "out_native")
        doc = B.run_real(paths, n_perm=20, gap_b=5, guards=False)
        v = self.a_doc["paper_A_verdict"]["verdict"]
        if v == "PASS":
            self.assertEqual(doc["status"], "RUN")
        else:
            self.assertTrue(doc["status"].startswith("NOT RUN"))
            self.assertIsNone(doc["statistics"])

    def test_b_p1_against_paper_A_unit_table(self):
        """With the verdict copy set to PASS (test manipulation only), B-P1 must reproduce Paper A's own unit table."""
        forced = json.loads(self.paths["a_verdicts"].read_text(encoding="utf-8"))
        forced["paper_A_verdict"]["verdict"] = "PASS"
        fp = self.tmp / "A/v112_verdicts_forced_PASS.json"
        fp.write_text(json.dumps(forced), encoding="utf-8")
        paths = dict(self.paths, a_verdicts=fp, out=self.tmp / "out_forced")
        doc = B.run_real(paths, n_perm=20, gap_b=5, guards=False)
        self.assertEqual(doc["status"], "RUN")
        self.assertTrue(doc["parity"]["B-P1"]["passed"])
        self.assertEqual(doc["parity"]["B-P1"]["units"], 112)
        self.assertEqual(doc["inputs"]["panel"], A.PANELS["N3"])
        self.assertEqual(doc["inputs"]["identity_load"], "t4 N3 S0 (v0.42)")
        self.assertGreater(doc["H35"]["eligible_il_units"], 0)
        self.assertIn("H36_Typology_cell", doc["verdict_summary"])


if __name__ == "__main__":
    unittest.main()
