#!/usr/bin/env python3
"""
End to end with Paper A's coder in the loop, following v1.12's own test_end_to_end_synthetic step by step: Paper A's
--brandfree (registry from the certified detectors), Coverage-shaped raw lines written with registry names, Paper A's
--code (v0.42's coder), t4-shaped raw coded by Paper A's code_t4_synthetic_v1_12.py, Paper A's --synthetic (scorer) ->
v112_verdicts.json and v112_unit_table.csv; then v1.19's run_real on those files. Synthetic data only; no network.

    python3 -m unittest discover -s osf/methodology/v1_19/scripts/tests -p "test_*.py" -v
"""
import csv
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import score_v1_19 as B   # noqa: E402

A = B.A
sys.path.insert(0, str(B.A_SCRIPTS / "tests"))
import test_pipeline_v1_12 as TP   # noqa: E402

PY = sys.executable
A_SCORER = B.A_SCRIPTS / "score_v1_12.py"
A_T4CODER = B.A_SCRIPTS / "tests/code_t4_synthetic_v1_12.py"
UTC = timezone.utc


def run(args):
    return subprocess.run([PY] + [str(a) for a in args], capture_output=True, text=True, timeout=600, cwd=str(B.ROOT))


class CoderInTheLoop(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="v119_coder_"))
        d = cls.tmp / "e2e"
        (d / "t4").mkdir(parents=True)
        r = run([A_SCORER, "--brandfree", "--out", cls.tmp / "bf.json"])
        assert r.returncode == 0, r.stderr[-2000:]
        reg = json.loads((cls.tmp / "bf.json").read_text(encoding="utf-8"))["registry"]
        raw, _rows, _ = TP.make_coverage(11, registry={s: dict(v) for s, v in reg.items()})
        for x in raw:                                     # as v1.12's test: answers use registry names
            if x["text"].startswith("I would suggest "):
                ks = x["text"][len("I would suggest "):-1].split(", ")
                x["text"] = "I would suggest " + ", ".join(reg[x["substrate"]][k] for k in ks) + "."
        (d / "v112_raw.jsonl").write_text("".join(json.dumps(x) + "\n" for x in raw), encoding="utf-8")
        t4raw, t = [], datetime(2026, 11, 12, 0, 0, tzinfo=UTC)
        rng = np.random.default_rng(12)
        for sub, rs in A.RAW_SUB.items():
            keys = list(reg[sub])
            rates = rng.uniform(0.05, 0.8, len(keys))
            for m in A.T4_N3:
                for run_ in A.RUNS:
                    for f in range(6):
                        nm = [reg[sub][k] for k, q in zip(keys, rates) if rng.random() < q]
                        t4raw.append({"call_id": f"{rs}|B|F{f}|{m}|S0|{run_}", "substrate": rs, "phase": "B",
                                      "probe_id": f"F{f}", "frame_id": f"F{f}", "model_requested": m, "served_model": m,
                                      "condition": "S0", "run": run_, "status": "ok", "error": None,
                                      "text": "Consider " + ", ".join(nm) + "." if nm else "No idea.",
                                      "started_utc": t.isoformat(), "finished_utc": t.isoformat()})
                        t += timedelta(seconds=10)
                for k in keys:
                    yes = rng.random() < 0.7
                    t4raw.append({"call_id": f"{rs}|A|{k}|{m}|S0|1", "substrate": rs, "phase": "A",
                                  "probe_id": f"A-{k}", "brand": reg[sub][k], "brand_id": k, "model_requested": m,
                                  "served_model": m, "condition": "S0", "run": 1, "status": "ok", "error": None,
                                  "spirit_type": "whisky",
                                  "text": (f"Yes, I am familiar with {reg[sub][k]}." if yes
                                           else f"No, I am not familiar with {reg[sub][k]}."),
                                  "started_utc": t.isoformat(), "finished_utc": t.isoformat()})
                    t += timedelta(seconds=10)
        (d / "t4/t4_raw.jsonl").write_text("".join(json.dumps(x) + "\n" for x in t4raw), encoding="utf-8")
        r = run([A_T4CODER, d / "t4/t4_raw.jsonl", d / "t4/coded"])
        assert r.returncode == 0, r.stderr[-2000:]
        _ca, cb = A.read_t4_coded(d / "t4/coded")
        excl, _w = A.t4_excluded(t4raw)
        bt = TP.brand_table_from(cb, excl, reg)
        with open(d / "t4/v42_brand_table.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(bt[0]))
            w.writeheader()
            for row in bt:
                w.writerow({k: ("" if v is None or (isinstance(v, float) and not np.isfinite(v)) else v)
                            for k, v in row.items()})
        (d / "t4/v42_verdicts.json").write_text(json.dumps({"models_excluded_condition": []}), encoding="utf-8")
        r = run([A_SCORER, "--code", "--raw", d / "v112_raw.jsonl", "--coded", d / "coded"])
        assert r.returncode == 0, r.stderr[-2000:]
        r = run([A_SCORER, "--synthetic", d, "--draws", 99])
        assert r.returncode == 0, r.stderr[-3000:]
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
        cls.d = d
        cls.a_doc = json.loads((d / "_score/v112_verdicts.json").read_text(encoding="utf-8"))
        cls.paths = {"a_raw": d / "v112_raw.jsonl", "a_coded": d / "coded", "a_verdicts": d / "_score/v112_verdicts.json",
                     "a_unit_table": d / "_score/v112_unit_table.csv", "a_probes": A.PROBES_PATH,
                     "roster": d / "roster.csv", "t4_raw": d / "t4/t4_raw.jsonl", "t4_coded": d / "t4/coded",
                     "t4_probes": d / "t4/probes.jsonl", "decision": d / "none.json", "only_sens": ("S-F-noD",)}

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_b_p1_on_coder_output(self):
        forced = dict(self.a_doc)
        forced["paper_A_verdict"] = dict(self.a_doc["paper_A_verdict"], verdict="PASS")   # test manipulation only
        fp = self.d / "_score/v112_verdicts_forced_PASS.json"
        fp.write_text(json.dumps(forced), encoding="utf-8")
        doc = B.run_real(dict(self.paths, a_verdicts=fp, out=self.d / "out"), n_perm=20, gap_b=5, guards=False)
        self.assertEqual(doc["status"], "RUN")
        self.assertTrue(doc["parity"]["B-P1"]["passed"], doc["parity"]["B-P1"])
        self.assertEqual(doc["parity"]["B-P1"]["units"], 112)
        self.assertEqual(doc["inputs"]["identity_load"], "t4 N3 S0 (v0.42)")

    def test_native_verdict_routes(self):
        doc = B.run_real(dict(self.paths, out=self.d / "out_native"), n_perm=20, gap_b=5, guards=False)
        v = self.a_doc["paper_A_verdict"]["verdict"]
        self.assertEqual(doc["status"] == "RUN", v == "PASS")


if __name__ == "__main__":
    unittest.main()
