#!/usr/bin/env python3
"""
Tests for osf/methodology/v1_12/sensitivity/quotes_v1_12.py (S-Q, AIAS 3.0 pre-registration section 10.2). Synthetic
answers only: no v1.12, v1.19 or t4 answer is read (the registry comes from v1.12's MC_BrandFree record; the locked
v1.19 scorer and its roster are read from git as code and design files). Tests that need the coder run the wrapper in
a subprocess (the coder's HOME shim re-executes the entry script). Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_12/sensitivity/tests/test_quotes_v1_12.py -v
"""
import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SENS = HERE.parent
sys.path.insert(0, str(SENS))
import quotes_v1_12 as Q   # noqa: E402

A, R3, ROOT = Q.A, Q.R3, Q.ROOT
PY = sys.executable
WRAPPER = SENS / "quotes_v1_12.py"
V112 = ROOT / "osf/methodology/v1_12/scripts"
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
UTC = timezone.utc
CURLY = "’"


def _tp():
    if str(V112 / "tests") not in sys.path:
        sys.path.insert(0, str(V112 / "tests"))
    import test_pipeline_v1_12 as TP   # noqa: E402
    return TP


def _run(args, timeout=900):
    return subprocess.run([PY] + [str(a) for a in args], capture_output=True, text=True, cwd=str(ROOT), env=ENV,
                          timeout=timeout)


class TestMap(unittest.TestCase):
    def test_only_u2019_u2018(self):
        s = "Paula’s ‘x’ ʼ ′ ＇ ‛ “” ' \" L’Oréal"
        self.assertEqual(Q.normalise(s), "Paula's 'x' ʼ ′ ＇ ‛ “” ' \" L'Oréal")
        self.assertEqual(Q.QUOTE_MAP, {"’": "'", "‘": "'"})
        self.assertIsNone(Q.normalise(None))

    def test_records_copied(self):
        recs = [{"call_id": "a", "text": "Paula’s Choice"}, {"call_id": "b", "text": None}]
        before = json.dumps(recs)
        out = Q.normalise_records(recs)
        self.assertEqual(json.dumps(recs), before)
        self.assertEqual(out[0]["text"], "Paula's Choice")
        self.assertIsNot(out[0], recs[0])

    def test_counts(self):
        recs = [{"substrate": "v0.20", "model_requested": "m", "text": "Paula’s ʼʼ", "call_id": "1",
                 "status": "ok"},
                {"substrate": "v0.21", "model_requested": "m", "text": "′", "call_id": "2", "status": "ok"},
                {"substrate": "v0.21", "model_requested": "m", "text": "plain", "call_id": "3", "status": "ok"}]
        c = Q.apostrophe_counts(recs)
        self.assertEqual(c["total_lines_with_U2019_or_U2018"], 1)
        self.assertEqual(c["other_apostrophe_like_not_mapped"]["U+02BC"], {"characters": 2, "lines": 1})
        self.assertEqual(c["other_apostrophe_like_not_mapped"]["U+2032"], {"characters": 1, "lines": 1})
        self.assertEqual(Q.answered_counts(recs)["total"], 1)


class TestDiffs(unittest.TestCase):
    def test_mention_diffs(self):
        p = [{"call_id": "c1", "substrate": "v0.20", "brand": "Paula's Choice", "model": "gpt-6-astra",
              "probe_id": "SK-01", "run": 1, "mentioned": 0},
             {"call_id": "c1", "substrate": "v0.20", "brand": "CeraVe", "model": "gpt-6-astra", "probe_id": "SK-01",
              "run": 1, "mentioned": 1}]
        q = [dict(p[0], mentioned=1), dict(p[1])]
        d = Q.mention_diffs(p, q)
        self.assertEqual(d["n_cells_differ"], 1)
        self.assertEqual(d["by_direction"], {"0->1": 1})
        self.assertEqual(d["cells"][0]["panels"], ["N3", "C3", "A4"])
        self.assertEqual(d["cells"][0]["cep"], "SK-01")
        self.assertEqual(Q.mention_diffs(p, p)["n_cells_differ"], 0)

    def test_json_leaf_diff_ignores_only_local_paths(self):
        a = {"inputs": {"raw": "/x/raw", "raw_sha256": "aa", "t4": {"raw": "/x"}}, "H5_ranking_source": {"file": "/x"},
             "legs": {"H1": {"rho_w": 0.1}}}
        b = json.loads(json.dumps(a))
        b["inputs"]["raw"], b["inputs"]["t4"]["raw"], b["H5_ranking_source"]["file"] = "/y", "/y", "/y"
        self.assertEqual(Q.json_leaf_diff(a, b), [])
        b["inputs"]["raw_sha256"] = "bb"
        b["legs"]["H1"]["rho_w"] = 0.1000001
        self.assertEqual(len(Q.json_leaf_diff(a, b)), 2)

    def test_csv_cell_diff(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            for name, v in (("a.csv", "1"), ("b.csv", "2")):
                with open(tmp / name, "w", newline="") as f:
                    w = csv.writer(f)
                    w.writerows([["substrate", "brand", "x"], ["v0.19", "Grado", v]])
            self.assertEqual(Q.csv_cell_diff(tmp / "a.csv", tmp / "a.csv"), [])
            self.assertEqual(Q.csv_cell_diff(tmp / "a.csv", tmp / "b.csv"), [[["v0.19", "Grado"], "x", "1", "2"]])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestV114Check(unittest.TestCase):
    def test_counts_typographic_only_answers(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            base = {"substrate": "v20", "phase": "B", "condition": "S0", "model_requested": "gpt-6-astra", "status": "ok",
                    "error": None, "run": 1}
            raw = [dict(base, call_id="t1", text="Try Paula’s Choice."),
                   dict(base, call_id="t2", text="Try Paula's Choice."),
                   dict(base, call_id="t3", text="Try Paula’s Choice.", model_requested="claude-opus-5-5"),
                   dict(base, call_id="t4", substrate="v21", text="L’Oréal Paris")]
            with open(tmp / "rank.csv", "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["answer_id", "brand"])
                w.writerows([["t1", "CeraVe"], ["t2", "Paula's Choice"], ["t4", "L'Oréal Paris"]])
            r = Q.v114_check(raw, tmp / "rank.csv")
            self.assertEqual(r["answers_typographic_only"], 2)            # t1, t4 (t2 straight; t3 not N3)
            self.assertEqual(r["answers_in_rank_table"], 2)
            self.assertEqual(r["brand_listed_for_answer"], 1)              # t4 listed, t1 missed
            self.assertEqual(Q.v114_check(raw, None)["status"], "NOT CHECKED: v1.14 rank table not supplied")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestGuards(unittest.TestCase):
    def test_deviations_entries_not_yet_committed(self):
        """Today (2026-11-28) the S-Q entries are drafts only: the guard must say so, and the real run must refuse."""
        r = Q.deviations_guard(ROOT)
        self.assertFalse(r["ok"])
        for name in ("v1.12", "v1.19"):
            self.assertTrue(r["entries"][name]["locked_prefix_unchanged"], r)

    def test_real_run_refuses_and_writes_nothing(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            with self.assertRaises(Q.Refused):
                Q.real_guards(ROOT, tmp)
            self.assertEqual(list(tmp.iterdir()), [])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_guard_accepts_an_appended_entry(self):
        locked = R3._git_show(ROOT, "v1.12-prereg-r1", "osf/methodology/v1_12/anchor/DEVIATIONS.md")
        added = locked + b"\n## Entry 2 (ex ante): S-Q, U+2019 read as an apostrophe\n"
        spec = {"x": {"ref": "R", "path": "P", "lock_tag": "T"}}
        from unittest import mock
        with mock.patch.object(Q.R3, "_git_show", lambda root, ref, path: added if ref == "R" else locked):
            self.assertTrue(Q.deviations_guard(ROOT, spec)["ok"])
        with mock.patch.object(Q.R3, "_git_show", lambda root, ref, path: b"edited" + added if ref == "R" else locked):
            self.assertFalse(Q.deviations_guard(ROOT, spec)["ok"])

    def test_outputs_are_never_overwritten(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            (tmp / Q.OUTPUTS["flips"]).write_text("{}")
            with self.assertRaises(Q.Refused):
                Q.sq_pipeline({}, tmp)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


# =========================================================================== end to end with the coder (subprocesses)
def _registry():
    bf = json.loads((ROOT / "osf/methodology/v1_12/anchor/mc_brandfree_v1_12.json").read_text(encoding="utf-8"))
    return bf["registry"]


def _curl(text, rng, share=0.6):
    """Some straight apostrophes of the two registry names written as U+2019 (as some models do)."""
    for name in ("Paula's Choice", "L'Oréal Paris"):
        if name in text and rng.random() < share:
            text = text.replace(name, name.replace("'", CURLY))
    return text


def build_synthetic(d: Path, seed=31) -> dict:
    """Synthetic v1.12 and t4 records coded by the locked coder, 'published' v1.12 outputs made by v1.12's own
    --synthetic run, t4 S-Q tables made by coding the mapped t4 text; returns the wrapper's input map."""
    TP = _tp()
    reg = _registry()
    rng = np.random.default_rng(seed)
    (d / "t4").mkdir(parents=True)
    raw, _rows, _ = TP.make_coverage(seed, registry={s: dict(v) for s, v in reg.items()})
    for r in raw:
        if r["text"].startswith("I would suggest "):
            ks = r["text"][len("I would suggest "):-1].split(", ")
            r["text"] = _curl("I would suggest " + ", ".join(reg[r["substrate"]][k] for k in ks) + ".", rng)
    Q.write_jsonl(raw, d / "v112_raw.jsonl")
    t4raw, t = [], datetime(2026, 11, 12, 0, 0, tzinfo=UTC)
    for sub, raw_sub in A.RAW_SUB.items():
        keys = list(reg[sub])
        rates = rng.uniform(0.05, 0.8, len(keys))
        for m in A.T4_N3:
            for run in A.RUNS:
                for f in range(6):
                    nm = [reg[sub][k] for k, q in zip(keys, rates) if rng.random() < q]
                    t4raw.append({"call_id": f"{raw_sub}|B|F{f}|{m}|S0|{run}", "substrate": raw_sub, "phase": "B",
                                  "probe_id": f"F{f}", "frame_id": f"F{f}", "model_requested": m, "served_model": m,
                                  "condition": "S0", "run": run, "status": "ok", "error": None,
                                  "text": _curl("Consider " + ", ".join(nm) + ".", rng) if nm else "No idea.",
                                  "started_utc": t.isoformat(), "finished_utc": t.isoformat()})
                    t += timedelta(seconds=10)
            for k in keys:
                yes = rng.random() < 0.7
                t4raw.append({"call_id": f"{raw_sub}|A|{k}|{m}|S0|1", "substrate": raw_sub, "phase": "A",
                              "probe_id": f"A-{k}", "brand": reg[sub][k], "brand_id": k, "model_requested": m,
                              "served_model": m, "condition": "S0", "run": 1, "status": "ok", "error": None,
                              "spirit_type": "whisky",
                              "text": (f"Yes, I am familiar with {reg[sub][k]}." if yes
                                       else f"No, I am not familiar with {reg[sub][k]}."),
                              "started_utc": t.isoformat(), "finished_utc": t.isoformat()})
                t += timedelta(seconds=10)
    Q.write_jsonl(t4raw, d / "t4/t4_raw.jsonl")
    Q.write_jsonl(Q.normalise_records(t4raw), d / "t4_sq/t4_raw_SQ.jsonl")
    helper = V112 / "tests/code_t4_synthetic_v1_12.py"
    for rawp, out in ((d / "t4/t4_raw.jsonl", d / "t4/coded"), (d / "t4_sq/t4_raw_SQ.jsonl", d / "t4_sq/coded")):
        r = _run([helper, rawp, out])
        assert r.returncode == 0, r.stderr[-2000:]
    excl, _w = A.t4_excluded(t4raw)
    for side in ("t4", "t4_sq"):
        _ca, cb = A.read_t4_coded(d / side / "coded")
        bt = TP.brand_table_from(cb, excl, reg)
        with open(d / side / "v42_brand_table.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(bt[0]))
            w.writeheader()
            for row in bt:
                w.writerow({k: ("" if v is None or (isinstance(v, float) and not np.isfinite(v)) else v)
                            for k, v in row.items()})
        (d / side / "v42_verdicts.json").write_text(json.dumps({"models_excluded_condition": []}), encoding="utf-8")
    r = _run([V112 / "score_v1_12.py", "--code", "--raw", d / "v112_raw.jsonl", "--coded", d / "coded"])
    assert r.returncode == 0, r.stderr[-2000:]
    r = _run([V112 / "score_v1_12.py", "--synthetic", d, "--draws", 30])
    assert r.returncode == 0, r.stderr[-3000:]
    # the locked v1.19 scorer and its roster, read from git as code (v1.19's own tree layout)
    tree = d / "v119_tree"
    s19 = tree / Q.SQ_PINS["v1.19"]["scorer"]
    s19.parent.mkdir(parents=True)
    s19.write_bytes(R3._git_show(ROOT, Q.SQ_PINS["v1.19"]["ref"], Q.SQ_PINS["v1.19"]["scorer"]))
    man = tree / R3.PINS["v1.12"]["manifest"]
    man.parent.mkdir(parents=True)
    man.write_bytes(R3._git_show(ROOT, "v1.12-prereg-r1", R3.PINS["v1.12"]["manifest"]))
    roster = d / "phantom_roster_v1_19.csv"
    roster.write_bytes(R3._git_show(ROOT, Q.SQ_PINS["v1.19"]["ref"], Q.SQ_PINS["v1.19"]["roster"]))
    probes42 = d / "probes_v0_42.jsonl"
    probes42.write_bytes(R3._git_show(ROOT, Q.SQ_PINS["v0.42_probes"]["ref"], Q.SQ_PINS["v0.42_probes"]["path"]))
    src = {"v112_raw": str(d / "v112_raw.jsonl"), "v112_probes": str(A.PROBES_PATH), "v112_coded": str(d / "coded"),
           "v112_verdicts": str(d / "_score/v112_verdicts.json"), "v112_unit_table": str(d / "_score/v112_unit_table.csv"),
           "brandfree": str(A.BRANDFREE_PATH), "profiles": str(A.PROFILES_PATH), "t4_raw": str(d / "t4/t4_raw.jsonl"),
           "t4": {"primary": {"coded": str(d / "t4/coded"), "brand_table": str(d / "t4/v42_brand_table.csv"),
                              "verdicts": str(d / "t4/v42_verdicts.json")},
                  "SQ": {"coded": str(d / "t4_sq/coded"), "brand_table": str(d / "t4_sq/v42_brand_table.csv"),
                         "verdicts": str(d / "t4_sq/v42_verdicts.json")}},
           "require_p1": False,
           "v119": {"scorer": str(s19), "roster": str(roster), "t4_probes": str(probes42), "il_t1": ""}}
    S19 = Q.load_v119(s19)
    _doc, f19 = Q.run_v119(S19, src, src["v112_raw"], src["v112_coded"], src["v112_verdicts"], src["v112_unit_table"],
                           src["t4"]["primary"]["coded"], d / "pub119", 30, 3)
    src["v119"]["verdicts"] = str(f19)
    (d / "src.json").write_text(json.dumps(src, indent=1), encoding="utf-8")
    return src


class TestEndToEnd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="v112_sq_test_"))
        cls.src = build_synthetic(cls.tmp / "in")
        cls.out = cls.tmp / "out"
        cls.r = _run([WRAPPER, "--synthetic", cls.tmp / "in/src.json", "--out", cls.out, "--draws", 30])

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_run_and_outputs(self):
        self.assertEqual(self.r.returncode, 0, self.r.stderr[-3000:])
        for n in Q.OUTPUTS.values():
            self.assertTrue((self.out / n).exists(), n)

    def test_reproduction_was_exact(self):
        rec = json.loads((self.out / Q.OUTPUTS["record"]).read_text(encoding="utf-8"))
        rep = rec["reproduction"]
        self.assertEqual((rep["coded_cells_differ"], rep["v112_verdict_leaves_differ"],
                          rep["v112_unit_table_cells_differ"], rep["v119_verdict_leaves_differ"]), (0, 0, 0, 0))
        self.assertTrue(rep["registry_same"])
        self.assertTrue(R3.mq_sq(rec)["ok"])

    def test_flips_are_the_typographic_names_only(self):
        fl = json.loads((self.out / Q.OUTPUTS["flips"]).read_text(encoding="utf-8"))
        self.assertGreater(fl["n_cells_differ"], 0)
        self.assertEqual(set(fl["by_direction"]), {"0->1"})
        self.assertEqual({c["brand"] for c in fl["cells"]}, {"Paula's Choice", "L'Oréal Paris"})
        self.assertGreater(fl["answers_with_U2019_or_U2018"]["total"], 0)
        raw = A.read_jsonl(self.src["v112_raw"])
        curly_ids = {r["call_id"] for r in raw if CURLY in (r.get("text") or "")}
        self.assertTrue({c["call_id"] for c in fl["cells"]} <= curly_ids)

    def test_sq_tables_and_comparison(self):
        rows, _reg = A.read_coded(self.out / Q.OUTPUTS["coded"])
        pub, _ = A.read_coded(self.src["v112_coded"])
        self.assertEqual(len(rows), len(pub))
        doc = json.loads((self.out / Q.OUTPUTS["v112_verdicts"]).read_text(encoding="utf-8"))
        self.assertEqual(doc["comparators"]["source"], "t4 (v0.42, N3, S0)")
        self.assertTrue(doc["parity_gates"]["P2"]["passed"])           # S-Q comparators: S-Q t4 tables, both sides
        rec = json.loads((self.out / Q.OUTPUTS["record"]).read_text(encoding="utf-8"))
        tests = [r["test"] for r in rec["comparison"]["v1_12"]]
        self.assertIn("H1_Sep_Presence", tests)
        self.assertIn("v1_19", rec["comparison"])
        self.assertIn("other_apostrophe_like_not_mapped", rec["counts"]["raw_lines"])

    def test_v119_full_path_runs_on_the_sq_tables(self):
        """The synthetic Paper A does not pass, so the wrapper's v1.19 step took v1.19's NOT RUN path. Here the S-Q
        verdict file is copied with Paper A set to PASS (synthetic only) so that score_v1_19.run_real scores Paper B on
        the S-Q tables through the wrapper's paths."""
        doc = json.loads((self.out / Q.OUTPUTS["v112_verdicts"]).read_text(encoding="utf-8"))
        doc["paper_A_verdict"]["verdict"] = "PASS"
        fake = self.tmp / "v112_verdicts_SQ_PASS.json"
        fake.write_text(json.dumps(doc), encoding="utf-8")
        S19 = Q.load_v119(self.src["v119"]["scorer"])
        raw_sq = self.tmp / "raw_sq.jsonl"
        Q.write_jsonl(Q.normalise_records(A.read_jsonl(self.src["v112_raw"])), raw_sq)
        d19, f19 = Q.run_v119(S19, self.src, raw_sq, self.out / Q.OUTPUTS["coded"], fake,
                              self.out / Q.OUTPUTS["v112_unit_table"], self.src["t4"]["SQ"]["coded"],
                              self.tmp / "v119_full", 20, 2)
        self.assertEqual(f19.name, "v119_verdicts.json")
        self.assertTrue(d19["parity"]["B-P0"]["passed"])
        self.assertTrue(d19["parity"]["B-P1"]["passed"])             # Cov* from the S-Q tables = S-Q unit table
        self.assertIn("H32_SetSampling", d19["verdict_summary"])

    def test_second_run_refuses(self):
        r = _run([WRAPPER, "--synthetic", self.tmp / "in/src.json", "--out", self.out, "--draws", 30])
        self.assertEqual(r.returncode, 3, r.stderr[-2000:])

    def test_tampered_published_file_refuses_and_writes_nothing(self):
        src = json.loads(json.dumps(self.src))
        doc = json.loads(Path(src["v112_verdicts"]).read_text(encoding="utf-8"))
        doc["legs"]["H1_Sep_Presence"]["rho_w"] = (doc["legs"]["H1_Sep_Presence"]["rho_w"] or 0) + 1e-6
        bad = self.tmp / "bad_v112_verdicts.json"
        bad.write_text(json.dumps(doc), encoding="utf-8")
        src["v112_verdicts"] = str(bad)
        sp = self.tmp / "src_bad.json"
        sp.write_text(json.dumps(src), encoding="utf-8")
        out = self.tmp / "out_bad"
        r = _run([WRAPPER, "--synthetic", sp, "--out", out, "--draws", 30])
        self.assertEqual(r.returncode, 3, r.stderr[-2000:])
        self.assertIn("reproduction failed", r.stderr)
        self.assertFalse(out.exists() and any(out.iterdir()))


if __name__ == "__main__":
    unittest.main()
