#!/usr/bin/env python3
"""
Integration test of the v1.19 real-data path (load_real, B-P0, B-P1, score once, not-run record) on SYNTHETIC files
laid out exactly as Paper A's scorer writes and reads them (raw record, coded mention rows, registry, verdict file,
unit table) and as v0.42's coded Phase B rows and probe file are laid out. No real answer is read.

    python3 -m unittest discover -s osf/methodology/v1_19/scripts/tests -p "test_*.py" -v
"""
import csv
import json
import shutil
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import score_v1_19 as B   # noqa: E402

A = B.A


def write_world(d, world, verdict="PASS", tamper=False):
    d = Path(d)
    (d / "t4/coded").mkdir(parents=True, exist_ok=True)
    raw, rows = [], []
    for (sub, m, pid, r), named in sorted(world["ans"].items()):
        cid = f"{sub}|{m}|{pid}|{r}"
        raw.append({"call_id": cid, "substrate": sub, "probe_id": pid, "model_requested": m, "served_model": m,
                    "run": r, "status": "ok", "error": None, "condition": "S0",
                    "text": world["texts"].get((sub, m, pid, r)) or "Some brands."})
        for b in world["brands"][sub]:
            rows.append({"call_id": cid, "substrate": sub, "probe_id": pid, "model": m, "run": r, "brand": b,
                         "mentioned": int(b in named)})
    (d / "v112_raw.jsonl").write_text("".join(json.dumps(x) + "\n" for x in raw), encoding="utf-8")
    registry = {s: {b: b for b in bs} for s, bs in world["brands"].items()}
    A.write_coded(rows, registry, {"synthetic": True}, d / "coded")
    panel = world["panel"]
    (d / "v112_verdicts.json").write_text(json.dumps({"paper_A_verdict": {"verdict": verdict, "legs": {}},
                                                      "primary_panel": "N3", "panels": {"N3": panel}}), encoding="utf-8")
    tab = A.coverage_table(world["ans"], world["brands"], world["design"]["ceps"], panel)
    cov = A.cov_star_map(tab, panel, A.FLOOR_FULL)
    with open(d / "v112_unit_table.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["substrate", "brand", "cov_star", "P_comparator"])
        w.writeheader()
        for i, (k, v) in enumerate(sorted(cov.items())):
            if tamper and i == 3 and v is not None:
                v = v + 1.0
            w.writerow({"substrate": k[0], "brand": k[1], "cov_star": "" if v is None else v,
                        "P_comparator": world["P"].get(k, "")})
    with open(d / "roster.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["substrate", "brand", "recall_floor_flag_F", "defunct_D"])
        w.writeheader()
        for (s, b), fl in sorted(world["flags"].items()):
            w.writerow({"substrate": s, "brand": b, "recall_floor_flag_F": int(fl), "defunct_D": int(b in B.DEFUNCT)})
    # t4: trio Phase B, 6 questions (q1-q3 R_cat, q4-q6 R_cult), N3, 3 runs; mention prob from the world's IL
    probes, t4raw = [], []
    for sub in B.TRIO:
        rs = A.RAW_SUB[sub]
        for q in range(1, 7):
            probes.append({"probe_id": f"q{q}", "substrate": rs, "phase": "B", "channel": "R_cat" if q <= 3 else "R_cult"})
        with open(d / f"t4/coded/{rs}_phase_b.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["call_id", "substrate", "brand", "model", "condition", "run", "probe_id",
                                              "frame_id", "mentioned"])
            w.writeheader()
            for m in A.T4_N3:
                for r in A.RUNS:
                    for q in range(1, 7):
                        cid = f"{rs}|B|q{q}|{m}|S0|{r}"
                        t4raw.append({"call_id": cid, "substrate": rs, "phase": "B", "probe_id": f"q{q}",
                                      "model_requested": m, "served_model": m, "condition": "S0", "run": r,
                                      "status": "ok", "error": None, "text": "x",
                                      "started_utc": "2026-11-11T00:00:00+00:00",
                                      "finished_utc": "2026-11-11T00:00:01+00:00"})
                        for b in world["brands"][sub]:
                            il = world["il"].get((sub, b), {"il": 0.0})["il"]
                            pi = world["il"].get((sub, b), {"pi_hat": 0.3})["pi_hat"]
                            lean = il if q > 3 else -il
                            u = (zlib.crc32(f"{cid}|{b}".encode()) % 1000) / 1000.0    # deterministic
                            mentioned = int(u < min(max(pi + lean, 0.02), 0.98))
                            w.writerow({"call_id": cid, "substrate": sub, "brand": b, "model": m, "condition": "S0",
                                        "run": r, "probe_id": f"q{q}", "frame_id": f"q{q}", "mentioned": mentioned})
    (d / "t4/t4_raw.jsonl").write_text("".join(json.dumps(x) + "\n" for x in t4raw), encoding="utf-8")
    (d / "t4/probes_v0_42.jsonl").write_text("".join(json.dumps(x) + "\n" for x in probes), encoding="utf-8")
    return {"a_raw": d / "v112_raw.jsonl", "a_coded": d / "coded", "a_verdicts": d / "v112_verdicts.json",
            "a_unit_table": d / "v112_unit_table.csv", "a_probes": A.PROBES_PATH, "roster": d / "roster.csv",
            "t4_raw": d / "t4/t4_raw.jsonl", "t4_coded": d / "t4/coded", "t4_probes": d / "t4/probes_v0_42.jsonl",
            "decision": d / "no_decision.json", "out": d / "outputs"}


class RealPathOnSyntheticFiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="v119_test_"))
        cls.world = B.synthetic_world(True, 21)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_loader_reproduces_the_answer_index(self):
        paths = write_world(self.tmp / "a", self.world)
        inp, rows, rec = B.load_real(paths)
        self.assertEqual(inp["ans"], self.world["ans"])
        self.assertEqual(inp["panel"], self.world["panel"])
        self.assertEqual(len(rows), 112)
        self.assertIsNotNone(inp["il"])
        self.assertEqual(len(inp["il"]), 72)
        self.assertEqual(rec["identity_load"], "t4 N3 S0 (v0.42)")

    def test_run_once_pass(self):
        paths = write_world(self.tmp / "b", self.world)
        doc = B.run_real(paths, n_perm=50, gap_b=10, guards=False)
        self.assertEqual(doc["status"], "RUN")
        self.assertTrue(doc["parity"]["B-P0"]["passed"])
        self.assertTrue(doc["parity"]["B-P1"]["passed"])
        self.assertTrue((paths["out"] / "v119_verdicts.json").exists())
        for k in ("H32_SetSampling", "H32_CueType", "H34_Floor_Signature", "H34_Defunct_Occupancy", "H35_IL_Coverage",
                  "H36_Profile_Replication", "H36_Typology_cell"):
            self.assertIn(k, doc["verdict_summary"])

    def test_b_p1_mismatch_refuses(self):
        paths = write_world(self.tmp / "c", self.world, tamper=True)
        with self.assertRaises(B.Refused):
            B.run_real(paths, n_perm=10, gap_b=5, guards=False)
        self.assertFalse((paths["out"] / "v119_verdicts.json").exists())

    def test_not_run_record_on_fail(self):
        paths = write_world(self.tmp / "d", self.world, verdict="FAIL")
        doc = B.run_real(paths, n_perm=10, gap_b=5, guards=False)
        self.assertEqual(doc["status"], "NOT RUN")
        rec = json.loads((paths["out"] / "v119_not_run.json").read_text(encoding="utf-8"))
        self.assertIsNone(rec["statistics"])
        self.assertFalse((paths["out"] / "v119_verdicts.json").exists())


if __name__ == "__main__":
    unittest.main()
