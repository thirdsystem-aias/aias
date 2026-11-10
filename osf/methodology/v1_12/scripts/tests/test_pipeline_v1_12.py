#!/usr/bin/env python3
"""
Unit tests for the parts of score_v1_12.py added before the lock: coding with v0.42's coder (section 2.3), the
comparators P_N3 / C*_N3 and parity gate P2 (sections 2.6, 7.2), the section 4 checks, the drop rule (7.3), the
hypothesis legs and gate wiring (3), the sensitivities (7.4), the descriptives (5) and an end-to-end synthetic run
from t4-shaped and Coverage-shaped raw files to the verdict file. Synthetic data only: no v1.12 or t4 answer exists,
none is read, and no API is called. Tests that need the coder run it in a subprocess (its HOME shim re-executes the
entry script). Run from the repository root:

    python3 -m unittest discover -s osf/methodology/v1_12/scripts/tests -p "test_*.py" -v
"""
import ast
import csv
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import score_v1_12 as S   # noqa: E402

PY = sys.executable
SCORER = HERE.parent / "score_v1_12.py"
UTC = timezone.utc
N3, C3, A4 = S.PANELS["N3"], S.PANELS["C3"], S.PANELS["A4"]


def ast_functions(path, names, ns):
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    defs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    exec(compile(ast.Module(body=defs, type_ignores=[]), str(path), "exec"), ns)
    return ns


def synth_registry():
    reg = {}
    for sub in S.CATS:
        n = 16 if sub == "v0.19" else 24
        names = [f"{sub[-2:]}brand{i:02d}" for i in range(n)]
        if sub == "v0.19":
            names[0] = "Denon"
        if sub == "v0.22":
            names[-5:] = list(S.DEFUNCT)
        reg[sub] = {b: b for b in names}
    return reg


def make_coverage(seed=0, registry=None, answer_share=None, same_sets=False, served_bad=0):
    """Coverage-shaped raw lines (acquire_v1_12 record fields) and the mention rows the coder would give."""
    registry = registry or synth_registry()
    probes = S.load_probes()
    design = S.probe_design(probes)
    sha = S.sha256_file(S.PROBES_PATH)
    settings = S._acquire().SETTINGS
    rng = np.random.default_rng(seed)
    base = {sub: rng.uniform(0.03, 0.4, len(registry[sub])) for sub in S.CATS}
    raw, rows, t = [], [], datetime(2026, 11, 14, 1, 0, tzinfo=UTC)
    bad_left = served_bad
    for m in S.MODELS4:
        for r in S.RUNS:
            for p in probes:
                sub, pid = p["substrate"], p["probe_id"]
                brands = list(registry[sub])
                j = design["ceps"][sub].index(pid) if p["role"] == "CEP" else -1
                if same_sets:
                    named = brands[:5]
                else:
                    pr = [0.8 if j >= 0 and (bi + j) % 5 == 0 else base[sub][bi] * (0.25 if j >= 0 else 1.0)
                          for bi in range(len(brands))]
                    named = [b for b, q in zip(brands, pr) if rng.random() < q]
                ok = not (answer_share and m in answer_share and rng.random() > answer_share[m])
                served = m
                if ok and bad_left and m == GPT6_ and p["role"] == "CEP":
                    served, bad_left = "gpt-5-other", bad_left - 1
                cid = f"{sub}|{pid}|{m}|S0|{r}"
                text = ("I would suggest " + ", ".join(named) + ".") if named else "Hard to say without more detail."
                raw.append({"phase": "v1.12", "call_id": cid, "substrate": sub, "category": p["category"],
                            "probe_id": pid, "role": p["role"], "w": p["w"], "half": p["half"], "model_requested": m,
                            "provider": "x", "served_model": served if ok else None, "condition": "S0", "run": r,
                            "pass": 1, "prompt": p["prompt"], "system": None, "text": text if ok else "",
                            "status": "ok" if ok else "error", "error": None if ok else "Transient: 503",
                            "finish_reason": "stop" if ok else None, "input_tokens": 80, "output_tokens": 600,
                            "thinking_tokens": 150, "settings": settings, "attempts": 1, "usd_billed": 0.01,
                            "probes_sha256": sha, "started_utc": t.isoformat(),
                            "finished_utc": (t + timedelta(seconds=12)).isoformat()})
                t += timedelta(seconds=20)
                if ok:
                    rows += [{"call_id": cid, "substrate": sub, "probe_id": pid, "model": m, "run": r, "brand": b,
                              "mentioned": int(b in named)} for b in brands]
    return raw, rows, registry


GPT6_ = S.GPT6


def make_t4(seed=1, registry=None):
    """t4-shaped raw lines (v0.42 fields), coded Phase A / B rows (coder table fields) and the brand table columns."""
    registry = registry or synth_registry()
    rng = np.random.default_rng(seed)
    raw, ca, cb, t = [], [], [], datetime(2026, 11, 12, 0, 0, tzinfo=UTC)

    def line(cid, sub, phase, pid, m, run):
        nonlocal t
        raw.append({"call_id": cid, "substrate": S.RAW_SUB[sub], "phase": phase, "probe_id": pid, "model_requested": m,
                    "served_model": m, "condition": "S0", "run": run, "text": "x", "status": "ok", "error": None,
                    "started_utc": t.isoformat(), "finished_utc": (t + timedelta(seconds=5)).isoformat()})
        t += timedelta(seconds=10)
    for sub in S.CATS:
        brands = list(registry[sub])
        rates = rng.uniform(0.0, 0.9, len(brands))
        rates[:2] = [0.0, 1.0]
        for m in S.T4_N3:
            for r in S.RUNS:
                for f in range(6):
                    cid = f"{S.RAW_SUB[sub]}|B|F{f}|{m}|S0|{r}"
                    line(cid, sub, "B", f"F{f}", m, r)
                    cb += [{"call_id": cid, "substrate": sub, "brand": b, "model": m, "condition": "S0", "run": r,
                            "probe_id": f"F{f}", "frame_id": f"F{f}", "mentioned": int(rng.random() < q)}
                           for b, q in zip(brands, rates)]
            for b in brands:
                cid = f"{S.RAW_SUB[sub]}|A|{b}|{m}|S0|1"
                line(cid, sub, "A", b, m, 1)
                rec = int(rng.random() < 0.7)
                ca.append({"call_id": cid, "substrate": sub, "brand": b, "brand_id": b, "model": m, "condition": "S0",
                           "run": 1, "probe_id": b, "label": "yes" if rec else "no", "recognized": rec})
    return raw, ca, cb


def brand_table_from(cb, excluded, registry):
    units = [(s, b) for s in S.CATS for b in registry[s]]
    k, ans = S.t4_counts(cb, excluded)
    pi, ph = S.pi_hat_t4(k, ans, units), S.phi_panel_t4(k, ans, units)
    return [{"substrate": s, "brand": b, "pi_N3_S0": pi[(s, b)], "phi_N3_S0": ph[(s, b)][0],
             "phi_partition_N3_S0": ph[(s, b)][1]} for (s, b) in units]


def t4_bundle(seed=1, registry=None, excluded_models=()):
    registry = registry or synth_registry()
    raw, ca, cb = make_t4(seed, registry)
    excl, window = S.t4_excluded(raw)
    return {"coded_a": ca, "coded_b": cb, "brand_table": brand_table_from(cb, excl, registry), "excluded": excl,
            "verdicts": {"models_excluded_condition": [f"{m}|S0" for m in excluded_models]}, "window": window}


def profiles_for(registry, seed=2):
    rng = np.random.default_rng(seed)
    return [{"wave": "t3", "substrate": s, "brand": b, "P": str(rng.uniform(10, 90)), "C_star": str(rng.uniform(0, 100)),
             "rated": "1"} for s in S.CATS for b in registry[s]]


def inputs(seed=0, **kw):
    t4kw = {k: kw.pop(k) for k in ("excluded_models",) if k in kw}
    raw, rows, reg = make_coverage(seed, **kw)
    t4 = t4_bundle(registry=reg, **t4kw)
    return {"raw": raw, "mentions": rows, "registry": reg, "probes": S.load_probes(), "t4": t4,
            "profiles": profiles_for(reg)}


# =========================================================================== coder pin and coding helpers
class TestCoderPin(unittest.TestCase):
    def test_vendored_coder_is_the_pinned_blob(self):
        v = S.verify_coder()
        self.assertTrue(v["match"], v)
        out = subprocess.run(["git", "hash-object", str(S.CODER_FILE)], capture_output=True, text=True)
        if out.returncode == 0:
            self.assertEqual(out.stdout.strip(), S.CODER_BLOB)

    def test_tampered_copy_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "code_t4_v0_42.py"
            p.write_bytes(S.CODER_FILE.read_bytes() + b"\n")
            self.assertFalse(S.verify_coder(p)["match"])
            with mock.patch.object(S, "CODER_FILE", p):
                with self.assertRaises(S.Refused):
                    S.load_coder()

    def test_dedupe_and_answered_equal_the_coder(self):
        ns = ast_functions(S.CODER_FILE, {"is_answered", "dedupe_calls"}, {})
        rng = np.random.default_rng(3)
        for _ in range(200):
            recs = [{"call_id": f"c{rng.integers(0, 4)}", "status": rng.choice(["ok", "error", "empty"]),
                     "text": rng.choice(["", " ", "Sennheiser"]), "error": rng.choice([None, "", "boom"]), "i": i}
                    for i in range(8)]
            self.assertEqual([S.is_answered(r) for r in recs], [ns["is_answered"](r) for r in recs])
            self.assertEqual(S.dedupe_calls(recs), ns["dedupe_calls"](recs))

    def test_served_ok_equals_acquire(self):
        AQ = S._acquire()
        for req, srv in (("gpt-6-astra", "gpt-6-astra"), ("gpt-6-astra", "gpt-6-astra-2026-11-01"),
                         ("gemini-4-argon", "models/gemini-4-argon"), ("gpt-6-astra", "gpt-6"), ("gpt-6-astra", None),
                         ("claude-fable-5-2", "claude-fable-5-2-20261101"), ("x", "x-latest")):
            self.assertEqual(S.served_ok(req, srv), AQ.served_ok(req, srv))

    def test_to_t4_record(self):
        r = S.to_t4_record({"call_id": "c", "substrate": "v0.23", "probe_id": "SP-WHY-A", "model_requested": "m",
                            "run": 2, "text": "t", "status": "ok", "error": None})
        self.assertEqual((r["substrate"], r["phase"], r["frame_id"], r["condition"]), ("v23", "B", "SP-WHY-A", "S0"))

    def test_run_code_refuses_real_record_when_tag_differs(self):
        with mock.patch.object(S, "coder_blob_at_tag", return_value={"match": False, "blob_at_tag": None}):
            with self.assertRaises(S.Refused):
                S.run_code(S.RAW_PATH, Path(tempfile.mkdtemp()))

    def test_run_score_refuses_before_the_lock(self):
        with mock.patch.object(S, "_ls_remote_tag", return_value=""):
            with self.assertRaises(S.Refused):
                S.run_score(S.RAW_PATH, S.CODED_DIR, S.T4_DEFAULTS, "/dev/null", "/dev/null", S.Cfg(9, 9), True)


class TestDesignAndAnalysisSet(unittest.TestCase):
    def test_probe_design(self):
        d = S.probe_design(S.load_probes())
        self.assertEqual({s: len(v) for s, v in d["ceps"].items()}, {s: 14 for s in S.CATS})
        for h in "AB":
            self.assertEqual({s: len(v) for s, v in d["half"][h].items()}, {s: 7 for s in S.CATS})
        self.assertEqual(len(d["control"]), 5)
        for s in S.CATS:
            ws = [d["w"][p] for p in d["ceps"][s]]
            self.assertEqual(sorted(set(ws)), sorted(S.W_TYPES))
            self.assertTrue(all(ws.count(w) == 2 for w in S.W_TYPES))
            self.assertEqual({d["w"][p] for p in d["half"]["A"][s]}, set(S.W_TYPES))

    def test_build_analysis_exclusions(self):
        d = S.probe_design(S.load_probes())
        pid, ctl = d["ceps"]["v0.20"][0], d["control"]["v0.20"]
        base = {"substrate": "v0.20", "condition": "S0", "status": "ok", "text": "a", "error": None}
        calls = [dict(base, call_id="ok", probe_id=pid, model_requested=S.FABLE, served_model=S.FABLE, run=1),
                 dict(base, call_id="ctl", probe_id=ctl, model_requested=S.FABLE, served_model=S.FABLE, run=1),
                 dict(base, call_id="srv", probe_id=pid, model_requested=S.GPT6, served_model="gpt-5", run=1),
                 dict(base, call_id="nosrv", probe_id=pid, model_requested=S.GEM4, served_model=None, run=1),
                 dict(base, call_id="err", probe_id=pid, model_requested=S.OPUS55, served_model=S.OPUS55, run=2,
                      status="error", text=""),
                 dict(base, call_id="run4", probe_id=pid, model_requested=S.FABLE, served_model=S.FABLE, run=4),
                 dict(base, call_id="odd", probe_id="ZZ", model_requested=S.FABLE, served_model=S.FABLE, run=1),
                 dict(base, call_id="uncoded", probe_id=pid, model_requested=S.OPUS55, served_model=S.OPUS55, run=3)]
        rows = [{"call_id": c, "brand": b, "mentioned": v} for c, b, v in
                (("ok", "X", 1), ("ok", "Y", 0), ("ctl", "Y", 1), ("srv", "X", 1), ("nosrv", "X", 1))]
        A = S.build_analysis(calls, rows, d)
        self.assertEqual(A["cep"], {("v0.20", S.FABLE, pid, 1): frozenset({"X"})})
        self.assertEqual(A["ctl"], {("v0.20", S.FABLE, 1): frozenset({"Y"})})
        self.assertEqual(sorted(x["call_id"] for x in A["served_mismatch"]), ["nosrv", "srv"])
        self.assertEqual(A["ok_without_served_id"], 1)
        self.assertEqual(sorted(A["outside_design"]), ["odd", "run4"])
        self.assertEqual(A["answered_not_coded"], ["uncoded"])

    def test_mc_complete_and_drop_rule(self):
        A = {"cep": {}, "ctl": {}}
        for m, n in ((S.FABLE, 225), (S.OPUS55, 202), (S.GPT6, 203), (S.GEM4, 225)):
            for i in range(n):
                A["cep"][("v0.20", m, f"p{i}", 1)] = frozenset()
        r = S.mc_complete(A)
        self.assertEqual(r["dropped_models"], [S.OPUS55])            # 202 / 225 = 0.898 < 0.90
        self.assertEqual(r["answered"], 855)
        self.assertFalse(r["pass"])                                   # 855 / 900 = 0.95 < 0.98
        self.assertEqual(S.select_panels([]), ("N3", {k: list(v) for k, v in S.PANELS.items()}))
        prim, pans = S.select_panels([S.FABLE])
        self.assertEqual((prim, pans["C3"]), ("C3", C3))
        prim, pans = S.select_panels([S.GPT6])
        self.assertEqual((prim, pans["N3"]), ("N3", [S.FABLE, S.GEM4]))


# =========================================================================== section 4 checks
class TestChecks(unittest.TestCase):
    def rec(self, cid, m, start, end=None, **kw):
        return dict({"call_id": cid, "model_requested": m, "started_utc": start, "finished_utc": end or start,
                     "settings": S._acquire().SETTINGS}, **kw)

    def test_mc_window(self):
        ok = [self.rec("a", S.FABLE, "2026-11-14T01:00:00+00:00"), self.rec("b", S.FABLE, "2026-11-15T01:00:00+00:00")]
        t4 = ("2026-11-12T00:00:00+00:00", "2026-11-13T12:00:00+00:00")
        self.assertTrue(S.mc_window(ok, t4)["pass"])
        long = ok + [self.rec("c", S.FABLE, "2026-11-22T13:00:00+00:00")]
        r = S.mc_window(long, t4)
        self.assertEqual((r["within_72h"], r["calls_outside_section_6_7_windows"], r["pass"]), (False, 0, False))
        blk = [self.rec("d", S.FABLE, "2026-11-17T03:00:00+00:00")]
        r = S.mc_window(blk, t4)
        self.assertEqual(r["calls_outside_section_6_7_windows"], 1)
        self.assertFalse(r["pass"])
        ov = S.mc_window(ok, ("2026-11-14T00:30:00+00:00", "2026-11-14T02:00:00+00:00"))
        self.assertEqual(ov["calls_overlapping_t4"], 1)
        self.assertFalse(ov["pass"])
        self.assertIsNone(S.mc_window(ok, None)["no_t4_overlap"])

    def test_mc_settings_and_truncation(self):
        recs = [self.rec(f"c{i}", S.GPT6, "x", status="ok", text="t", error=None, thinking_tokens=10, output_tokens=20,
                         finish_reason="length" if i < 2 else "stop") for i in range(20)]
        self.assertTrue(S.mc_settings(recs, recs)["pass"])
        self.assertEqual(S.mc_settings(recs, recs)["reasoning_tokens_per_model"][S.GPT6]["reasoning_tokens_total"], 200)
        bad = recs + [dict(recs[0], call_id="z", settings={"temperature": 0.2})]
        self.assertFalse(S.mc_settings(bad, recs)["pass"])
        t = S.mc_truncation(recs)[S.GPT6]
        self.assertEqual((t["at_cap"], t["flag_above_5pct"]), (2, True))       # 2 / 20 = 10% > 5%
        self.assertFalse(S.mc_truncation(recs[1:] + [dict(recs[5])] * 21)[S.GPT6]["flag_above_5pct"])

    def test_registry_share_defunct_positive(self):
        A = {"cep": {}}
        for i in range(20):
            A["cep"][("v0.22", S.FABLE, f"p{i}", 1)] = frozenset({"Pontiac"} if i == 0 else ({"Toyota"} if i < 9 else ()))
            A["cep"][("v0.20", S.FABLE, f"p{i}", 1)] = frozenset({"CeraVe"})
        rs = S.mc_registry_share(A, [S.FABLE])
        self.assertAlmostEqual(rs["v0.22"]["share_naming_registry_brand"], 0.45)
        self.assertTrue(rs["v0.22"]["flag_below_0_50"])
        self.assertFalse(rs["v0.20"]["flag_below_0_50"])
        d = S.mc_defunct(A, [S.FABLE])
        self.assertAlmostEqual(d["share_naming_any"], 0.05)
        self.assertFalse(d["flagged"])                                        # 5% is within the rule
        A["cep"][("v0.22", S.FABLE, "p1", 1)] = frozenset({"Saturn"})
        self.assertTrue(S.mc_defunct(A, [S.FABLE])["flagged"])
        x = {(c, f"b{i}"): float(i) for c in S.CATS for i in range(10)}
        self.assertFalse(S.mc_positive(x, x)["flagged"])
        self.assertFalse(S.mc_positive(x, {k: -v for k, v in x.items()})["flagged"])     # |rho| = 1
        self.assertTrue(S.mc_positive(x, {k: 1.0 for k in x})["flagged"])                # rho undefined
        y = {(c, f"b{i}"): float((i * 7) % 10) for c in S.CATS for i in range(10)}      # rho = 0.3
        r = S.mc_positive(x, y)
        self.assertLess(abs(r["rho_w_raw_cov_pi_cov"]), 0.5)
        self.assertTrue(r["flagged"])


# =========================================================================== comparators and P2 (sections 2.6, 7.2)
class TestComparators(unittest.TestCase):
    def test_phi_m_reduced_equals_score_v41(self):
        ns = ast_functions(S.ROOT / "osf/v41/scripts/score_v41.py", {"phi_m", "phi_of"}, {"np": np, "M": 6, "F": 6})
        rng = np.random.default_rng(4)
        for _ in range(300):
            k = rng.integers(0, 7, 3).tolist()
            self.assertEqual(S.phi_m_reduced(k), ns["phi_m"](k))
        self.assertEqual(S.phi_m_reduced([0, 0, 0])[2], "zero")
        self.assertEqual(S.phi_m_reduced([6, 6, 6])[2], "saturated")

    def test_pi_hat_and_phi_by_hand(self):
        cb, ms = [], S.T4_N3
        counts = {S.FABLE: [4, 3, 6], S.GPT6: [1, 0, 6], S.GEM4: [2, 3, 6]}       # per run, of 6 frames
        for m in ms:
            for r in S.RUNS:
                for f in range(6):
                    cb.append({"call_id": f"{m}{r}{f}", "substrate": "v0.20", "brand": "B", "model": m,
                               "condition": "S0", "run": r, "mentioned": int(f < counts[m][r - 1])})
        k, ans = S.t4_counts(cb, set())
        pi = S.pi_hat_t4(k, ans, [("v0.20", "B")])[("v0.20", "B")]
        self.assertEqual(pi, 31 / 54)
        phi, part, runs = S.phi_panel_t4(k, ans, [("v0.20", "B")])[("v0.20", "B")]
        want = np.mean([S.phi_m_reduced([4, 1, 2])[0], S.phi_m_reduced([3, 0, 3])[0]])
        self.assertEqual((phi, part, runs), (float(want), "defined", ["defined", "defined", "saturated"]))
        cb2 = [r for r in cb if not (r["model"] == S.GPT6 and r["run"] == 1 and r["call_id"].endswith("0"))]
        k2, ans2 = S.t4_counts(cb2, set())
        self.assertEqual(S.phi_panel_t4(k2, ans2, [("v0.20", "B")])[("v0.20", "B")][1], "undefined")

    def test_p_n3_and_c_star(self):
        bt = [{"substrate": "v0.20", "brand": b, "pi_N3_S0": pi, "phi_N3_S0": phi, "phi_partition_N3_S0": part}
              for b, pi, phi, part in (("D", 0.5, 1.8, "defined"), ("S", 1.0, None, "saturated"),
                                       ("Z", 0.0, None, "zero"), ("U", 0.2, None, "undefined"), ("F", 0.1, 2.7, "defined"))]
        ca = [{"call_id": f"a{b}{m}", "substrate": "v0.20", "brand": b, "model": m, "condition": "S0", "run": 1,
               "recognized": rec} for b, m, rec in (("D", S.FABLE, 1), ("D", S.GPT6, 0), ("D", S.GEM4, None),
                                                     ("S", S.FABLE, 1), ("S", S.GPT6, 1), ("S", S.GEM4, 1),
                                                     ("D", S.OPUS55, 1), ("F", S.FABLE, 1), ("F", S.GPT6, 1))]
        cb = [{"call_id": f"b{b}{i}", "substrate": "v0.20", "brand": b, "model": S.T4_N3[i % 3], "condition": "S0",
               "run": 1 + i % 3, "mentioned": 1} for b, n in (("D", 6), ("S", 54), ("Z", 0), ("U", 7), ("F", 5))
              for i in range(n)]
        c = S.comparators_t4(bt, ca, cb, excluded={"aFgpt-6-astra"} | set())
        u = lambda b: ("v0.20", b)      # noqa: E731
        self.assertAlmostEqual(c["P"][u("D")], 100 * (1 / 2 + 2 * 0.5) / 3)   # Gemini uncoded, Opus not N3
        self.assertAlmostEqual(c["P"][u("S")], 100 * (1 + 2) / 3)
        self.assertIsNone(c["P"][u("Z")])                                      # no coded Phase A answer
        self.assertAlmostEqual(c["C"][u("D")], 100 * (1 - 1.8 / 9))
        self.assertEqual(c["C"][u("S")], 100.0)
        self.assertIsNone(c["C"][u("Z")])
        self.assertIsNone(c["C"][u("U")])
        self.assertIsNone(c["C"][u("F")])                                      # 5 mentions < 6
        self.assertEqual(c["t4_mentions"][u("F")], 5)
        c2 = S.comparators_t4(bt, ca, cb, excluded={f"aF{S.GPT6}"})
        self.assertAlmostEqual(c2["P"][u("F")], 100 * (1 + 0.2) / 3)          # excluded call leaves the denominator

    def test_parity_p2(self):
        reg = synth_registry()
        t4 = t4_bundle(registry=reg)
        self.assertTrue(S.parity_p2(t4["brand_table"], t4["coded_b"], t4["excluded"])["passed"])
        bt = [dict(r) for r in t4["brand_table"]]
        bt[3]["pi_N3_S0"] = bt[3]["pi_N3_S0"] + 1e-15
        r = S.parity_p2(bt, t4["coded_b"], t4["excluded"])
        self.assertFalse(r["passed"])
        self.assertEqual(r["mismatches"], 1)

    def test_t4_excluded(self):
        base = {"substrate": "v20", "condition": "S0", "status": "ok", "text": "t", "error": None,
                "started_utc": "2026-11-12T00:00:00+00:00", "finished_utc": "2026-11-12T00:00:05+00:00"}
        raw = [dict(base, call_id="b", phase="B", run=1, model_requested=S.FABLE, served_model=S.FABLE),
               dict(base, call_id="srv", phase="B", run=1, model_requested=S.GPT6, served_model="gpt-5"),
               dict(base, call_id="nosrv", phase="B", run=1, model_requested=S.GPT6, served_model=None),
               dict(base, call_id="opus", phase="B", run=1, model_requested=S.OPUS55, served_model=S.OPUS55),
               dict(base, call_id="a2", phase="A", run=2, model_requested=S.FABLE, served_model=S.FABLE,
                    finished_utc="2026-11-13T00:00:00+00:00")]
        excl, win = S.t4_excluded(raw)
        self.assertEqual(excl, {"srv", "opus", "a2"})
        self.assertEqual(win, ("2026-11-12T00:00:00+00:00", "2026-11-13T00:00:00+00:00"))

    def test_fallback_rule(self):
        reg = synth_registry()
        prof = profiles_for(reg)
        c = S.choose_comparators(None, prof)
        self.assertTrue(c["cross_panel"])
        self.assertEqual(c["P"][("v0.20", "20brand03")], float(prof[16 + 3]["P"]))
        c = S.choose_comparators(t4_bundle(registry=reg, excluded_models=[S.GEM4]), prof)
        self.assertTrue(c["cross_panel"])
        self.assertIn("drop rule", c["reason"])
        t4 = t4_bundle(registry=reg)
        t4["verdicts"] = {"models_excluded_condition": [f"{S.GEM4}|S1"]}       # S1 only: t4 S0 values stand
        c = S.choose_comparators(t4, prof)
        self.assertFalse(c["cross_panel"])
        self.assertEqual(c["legacy_P"][("v0.20", "20brand03")], float(prof[16 + 3]["P"]))

    def test_parity_p3(self):
        raw, _rows, _reg = make_coverage(5)
        d = S.probe_design(S.load_probes())
        self.assertTrue(S.parity_p3(raw, d)["passed"])
        raw[7] = dict(raw[7], prompt=raw[7]["prompt"] + " ")
        self.assertFalse(S.parity_p3(raw, d)["passed"])


# =========================================================================== legs, verdict branches, gate wiring
def maps(seed, noise, n_per=24, cats=S.CATS, sign=1.0):
    rng = np.random.default_rng(seed)
    x, y = {}, {}
    for c in cats:
        for i in range(n_per):
            a = rng.normal()
            x[(c, f"b{i}")] = a
            y[(c, f"b{i}")] = sign * a + noise * rng.normal()
    return x, y


class TestLegBranches(unittest.TestCase):
    def test_separability_branches(self):
        self.assertEqual(S.run_leg("sep", *maps(1, 0.0), 1, 0, 0)["verdict"], "FALSIFIED")
        self.assertEqual(S.run_leg("sep", *maps(1, 0.0, sign=-1.0), 1, 0, 0)["verdict"], "FALSIFIED")
        t = S.run_leg("sep", *maps(1, 1.6), 1, 0, 0)
        self.assertTrue(0.30 < abs(t["rho_w"]) < 0.50)
        self.assertEqual(t["verdict"], "MARGINAL")
        t = S.run_leg("sep", *maps(1, 1e6), 1, 0, 0)
        self.assertEqual(t["verdict"], "CONFIRMED")
        self.assertEqual(S.run_leg("sep", *maps(1, 0.0, n_per=5, cats=S.CATS[:3]), 1, 0, 0)["verdict"], "UNDETERMINED")
        t = S.run_leg("sep", *maps(1, 0.0), 112001, 99, 99)                   # with p and bootstrap
        self.assertEqual((t["verdict"], t["p_perm"], len(t["ci95_rho_w"])), ("FALSIFIED", 1 / 100, 2))

    def test_reliability_branches(self):
        self.assertEqual(S.run_leg("rel", *maps(1, 0.0), 2, 199, 0)["verdict"], "CONFIRMED")
        t = S.run_leg("rel", *maps(1, 2.5), 2, 199, 0)
        self.assertTrue(0.30 <= t["transformed"] < 0.50 and t["p_perm"] < 0.05)
        self.assertEqual(t["verdict"], "MARGINAL")
        self.assertEqual(S.run_leg("rel", *maps(1, 1e6), 2, 199, 0)["verdict"], "FALSIFIED")
        self.assertEqual(S.run_leg("rel", *maps(1, 0.0, n_per=5, cats=S.CATS[:3]), 2, 199, 0)["verdict"], "UNDETERMINED")
        self.assertEqual(S.run_leg("rel", *maps(1, 0.0), 2, 0, 0)["verdict"], "UNDETERMINED")   # no p, no verdict

    def test_replication_branches(self):
        self.assertEqual(S.run_leg("rep", *maps(1, 0.0), 3, 199, 0)["verdict"], "CONFIRMED")
        t = S.run_leg("rep", *maps(1, 1.0), 3, 199, 0)
        self.assertTrue(0.50 <= t["rho_w"] < 0.70)
        self.assertEqual(t["verdict"], "MARGINAL")
        self.assertEqual(S.run_leg("rep", *maps(1, 1.6), 3, 199, 0)["verdict"], "FALSIFIED")
        self.assertEqual(S.run_leg("rep", *maps(1, 0.0, n_per=5, cats=S.CATS[:3]), 3, 199, 0)["verdict"], "UNDETERMINED")

    def test_exclude_and_room_to_vary(self):
        x, y = maps(2, 1.0)
        a = S.run_leg("sep", x, y, 1, 0, 0)
        b = S.run_leg("sep", x, y, 1, 0, 0, exclude=(("v0.19", "b3"),))
        self.assertEqual(b["n"], a["n"] - 1)
        tab = {("v0.20", "B", "m1"): {"n": 10, "beta": 0.4, "cmax": 10, "cmin": 4, "slots": 42},
               ("v0.20", "B", "m2"): {"n": 5, "beta": 0.0, "cmax": 2, "cmin": 2, "slots": 42},
               ("v0.20", "B", "m3"): {"n": 0, "beta": None, "cmax": 0, "cmin": 0, "slots": 42}}
        self.assertAlmostEqual(S.cov_star_room(tab, "v0.20", "B", ["m1", "m2", "m3"]), 70.0)
        self.assertAlmostEqual(S.cov_star(tab, "v0.20", "B", ["m1", "m2", "m3"])["cov_star"], 60.0)
        tab[("v0.20", "B", "m1")].update(cmax=4)
        self.assertIsNone(S.cov_star_room(tab, "v0.20", "B", ["m1", "m2", "m3"]))

    def test_conditional_legs(self):
        x, y = maps(3, 1e6)
        comp = {"P": y, "C": y, "legacy_P": y}
        mp = {"cov": x, "covA": x, "covB": y, "pi": y}
        cfg = S.Cfg(49, 0)
        legs = S.legs_for(mp, comp, cfg)
        self.assertEqual((legs["H5_Sep_Ranking"]["verdict"], legs["H6_Sep_Sentiment"]["verdict"]), ("INACTIVE", "INACTIVE"))
        legs = S.legs_for(mp, comp, cfg, active={"H5_Sep_Ranking": True, "H6_Sep_Sentiment": True},
                          extra={"H5_Sep_Ranking": x})
        self.assertEqual(legs["H5_Sep_Ranking"]["verdict"], "FALSIFIED")
        self.assertEqual(legs["H6_Sep_Sentiment"]["verdict"], "UNDETERMINED")


# =========================================================================== pipeline in process (no coder)
class TestPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inp = inputs(0, served_bad=3)
        cls.doc, cls.rows = S.score_coverage(cls.inp, S.Cfg(49, 49), {"enforce": True})

    def test_structure_and_gates(self):
        d = self.doc
        self.assertEqual(set(d["verdicts"]), set(S.ALL_LEGS))
        self.assertTrue(set(d["verdicts"].values()) <= S.VERDICTS)
        self.assertIn(d["paper_A_verdict"]["verdict"], {"PASS", "FAIL", "MARGINAL", "UNDETERMINED", "INSTRUMENT FAIL"})
        self.assertTrue(d["parity_gates"]["P2"]["passed"])
        self.assertTrue(d["parity_gates"]["P3"]["passed"])
        self.assertEqual(d["comparators"]["source"], "t4 (v0.42, N3, S0)")
        self.assertEqual(set(d["MC"]), {"MC_BrandFree", "MC_Complete", "MC_Served", "MC_Settings", "MC_Truncation",
                                        "MC_RegistryShare", "MC_Situation", "MC_Defunct", "MC_Positive", "MC_Window"})
        self.assertEqual(d["MC"]["MC_Served"]["n_mismatched"], 3)
        self.assertEqual(d["analysis_set"]["answered_calls_analysed"], 897)
        self.assertTrue(d["MC"]["MC_Window"]["pass"])
        self.assertTrue(d["MC"]["MC_Settings"]["pass"])
        self.assertTrue(d["MC"]["MC_Situation"]["passed"])
        self.assertEqual(d["primary_panel"], "N3")
        self.assertEqual(set(d["gate_repeated_on"]), {"C3", "A4"})
        self.assertEqual(len(self.rows), 112)
        json.dumps(S._clean(d), allow_nan=False)

    def test_sensitivities_present(self):
        s = self.doc["sensitivities"]
        want = {"S1_raw_Cov_k2", "S2_floor_6", "S2_floor_28", "S3_equal_weight_null", "S4_room_to_vary",
                "S5_leave_one_category_out", "S6_leave_one_W_out", "S7_presence_alternatives", "S8_mid_p",
                "S9_uncentred_rho_w", "S10_without_Denon"}
        self.assertEqual(set(s), want)
        self.assertEqual(set(s["S3_equal_weight_null"]["verdicts"]), set(S.H14))
        self.assertEqual(set(s["S1_raw_Cov_k2"]["verdicts"]), set(S.H13))
        self.assertEqual(set(s["S5_leave_one_category_out"]["per_category_left_out"]), set(S.CATS))
        self.assertEqual(set(s["S6_leave_one_W_out"]["per_W_left_out"]), set(S.W_TYPES))
        h1 = self.doc["legs"]["H1_Sep_Presence"]
        self.assertAlmostEqual(s["S9_uncentred_rho_w"]["rho_w"]["H1_Sep_Presence"],
                               S.rho_w(*S.paired(*self._h1_maps())[1:4], centred=False), places=12)
        keys = S.paired(*self._h1_maps())[0]
        self.assertEqual(s["S10_without_Denon"]["n"]["H1_Sep_Presence"], h1["n"] - int(S.DENON in keys))

    def _h1_maps(self):
        cov = {(r["substrate"], r["brand"]): r["cov_star"] for r in self.rows}
        P = {(r["substrate"], r["brand"]): r["P_comparator"] for r in self.rows}
        return cov, P

    def test_unit_rows_agree_with_legs(self):
        cov, P = self._h1_maps()
        _k, x, y, g, info = S.paired(cov, P)
        self.assertEqual(S.rho_w(x, y, g), self.doc["legs"]["H1_Sep_Presence"]["rho_w"])
        for r in self.rows:
            self.assertEqual(r["rated"], int(r["cov_star"] is not None))

    def test_descriptives(self):
        d = self.doc["descriptives"]
        self.assertEqual(len(d["per_category_model"]), 20)
        cell = d["per_category_model"][f"v0.21|{S.GPT6}"]
        self.assertEqual(cell["missing_cells"], 0)
        self.assertEqual(cell["cep_answers"] + cell["control_answers"], 45)
        self.assertEqual(d["per_category_model"][f"v0.19|{S.GPT6}"]["missing_cells"], 3)   # the 3 served mismatches
        self.assertEqual(set(d["run_to_run_reliability"]), set(S.MODELS4))
        self.assertAlmostEqual(d["tokens_and_spend"]["total_usd"], 9.0)
        self.assertEqual(len(d["per_W_coverage_primary_panel"]), 112)
        self.assertIn("NOT COMPUTED", d["non_registry_brand_mentions"])

    def test_run_reliability_identical_runs(self):
        A = {"cep": {}}
        rng = np.random.default_rng(9)
        units = [(c, f"b{i}") for c in S.CATS[:3] for i in range(10)]
        for c in S.CATS[:3]:
            for j in range(14):
                s = frozenset(f"b{i}" for i in range(10) if rng.random() < (i + 1) / 11)
                for r in S.RUNS:
                    A["cep"][(c, "m", f"J{j}", r)] = s
        rr = S.run_reliability(A, units, None, "m")
        self.assertAlmostEqual(rr["rel1"], 1.0)
        self.assertAlmostEqual(rr["rel3"], 1.0)


class TestPipelineBranches(unittest.TestCase):
    CFG = S.Cfg(29, 0)

    def test_fable_dropped_c3_replaces_n3(self):
        doc, _ = S.score_coverage(inputs(1, answer_share={S.FABLE: 0.8}), self.CFG, {}, with_sensitivities=False)
        self.assertEqual(doc["models_dropped_section_7_3"], [S.FABLE])
        self.assertEqual(doc["primary_panel"], "C3")
        self.assertEqual(doc["verdicts"]["H8_Panel_Replication"], "UNDETERMINED")
        self.assertEqual(set(doc["gate_repeated_on"]), {"A4"})

    def test_gpt_dropped_two_model_cap_and_fallback_label(self):
        inp = inputs(2, answer_share={S.GPT6: 0.85})
        inp["t4"] = None
        doc, _ = S.score_coverage(inp, self.CFG, {}, with_sensitivities=False)
        self.assertEqual(doc["panels"]["N3"], [S.FABLE, S.GEM4])
        self.assertIn("two-model", doc["paper_A_verdict"]["label"])
        self.assertNotEqual(doc["paper_A_verdict"]["verdict"], "PASS")
        self.assertTrue(doc["comparators"]["cross_panel"])
        self.assertIn("cross-panel", doc["paper_A_verdict"]["label"])
        self.assertIsNone(doc["parity_gates"]["P2"]["passed"])

    def test_instrument_fail(self):
        doc, _ = S.score_coverage(inputs(3, same_sets=True), self.CFG, {}, with_sensitivities=False)
        self.assertFalse(doc["MC"]["MC_Situation"]["passed"])
        self.assertEqual(doc["paper_A_verdict"]["verdict"], "INSTRUMENT FAIL")

    def test_fail_when_a_comparator_tracks_cov_star(self):
        inp = inputs(4)
        d = S.probe_design(inp["probes"])
        A = S.build_analysis(S.dedupe_calls(inp["raw"]), inp["mentions"], d)
        tabs = S.build_tables(A, d, {s: list(v) for s, v in inp["registry"].items()})
        cov = S.cov_star_map(tabs["rasch"]["full"], N3)
        comp = dict(S.choose_comparators(inp["t4"], inp["profiles"]), P=cov)
        r = S.evaluate_panel("N3", N3, tabs["rasch"], comp, A, self.CFG, {}, {})
        self.assertEqual(r["verdicts"]["H1_Sep_Presence"], "FALSIFIED")
        self.assertEqual(r["gate"]["verdict"], "FAIL" if r["MC_Situation"]["passed"] else "INSTRUMENT FAIL")

    def test_halts(self):
        inp = inputs(5)
        inp["t4"]["brand_table"][0] = dict(inp["t4"]["brand_table"][0], phi_partition_N3_S0="defined", phi_N3_S0=0.5)
        with self.assertRaises(S.Halt):
            S.score_coverage(inp, self.CFG, {})
        inp = inputs(5)
        inp["raw"][0] = dict(inp["raw"][0], probes_sha256="0" * 64)
        with self.assertRaises(S.Halt):
            S.score_coverage(inp, self.CFG, {})
        with self.assertRaises(S.Halt):
            S.score_coverage(inputs(5), self.CFG, {"require_p1": True})
        with self.assertRaises(S.Halt):
            S.score_coverage(inputs(5), self.CFG, {"P1": {"passed": False}})


# =========================================================================== with the coder (subprocesses)
def _run(args, cwd=None, timeout=300):
    r = subprocess.run([PY] + [str(a) for a in args], capture_output=True, text=True, cwd=cwd or str(S.ROOT),
                       timeout=timeout)
    return r


class TestWithCoder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="v112_test_"))
        r = _run([SCORER, "--brandfree", "--out", cls.tmp / "bf.json"])
        cls.bf_rc, cls.bf_err = r.returncode, r.stderr
        cls.bf = json.loads((cls.tmp / "bf.json").read_text(encoding="utf-8")) if (cls.tmp / "bf.json").exists() else None

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_brandfree_on_the_75_probes(self):
        self.assertEqual(self.bf_rc, 0, self.bf_err[-2000:])
        self.assertTrue(self.bf["passed"])
        self.assertEqual((self.bf["probes"], self.bf["detector_runs"]), (75, 375))
        self.assertEqual(self.bf["registry_sizes"], {"v0.19": 16, "v0.20": 24, "v0.21": 24, "v0.22": 24, "v0.23": 24})

    def test_code_step(self):
        reg = self.bf["registry"]
        p = S.load_probes()[0]
        base = {"substrate": "v0.19", "probe_id": p["probe_id"], "condition": "S0", "status": "ok", "error": None}
        recs = [dict(base, call_id="c1", model_requested=S.FABLE, run=1,
                     text="Try Sennheiser, or see [this](https://www.audeze.com/x) and https://focal.com/a."),
                dict(base, call_id="c2", model_requested=S.GPT6, run=1, status="error", text=""),
                dict(base, call_id="c2", model_requested=S.GPT6, run=1, text="Grado and Audeze."),
                dict(base, call_id="c3", model_requested=S.GEM4, run=1, status="error", text="", error="boom"),
                dict(base, call_id="c4", substrate="v0.23", probe_id="SP-C0", model_requested=S.FABLE, run=2,
                     text=f"{reg['v0.23']['S02']} is lovely.")]
        raw = self.tmp / "code_raw.jsonl"
        raw.write_text("".join(json.dumps(r) + "\n" for r in recs), encoding="utf-8")
        r = _run([SCORER, "--code", "--raw", raw, "--coded", self.tmp / "coded_small"])
        self.assertEqual(r.returncode, 0, r.stderr[-2000:])
        rows, registry = S.read_coded(self.tmp / "coded_small")
        named = {(x["call_id"], x["brand"]) for x in rows if x["mentioned"]}
        self.assertEqual(named, {("c1", "Sennheiser"), ("c2", "Grado"), ("c2", "Audeze"), ("c4", "S02")})
        self.assertEqual({x["call_id"] for x in rows}, {"c1", "c2", "c4"})        # c3 unanswered: no rows
        self.assertEqual(len([x for x in rows if x["call_id"] == "c1"]), 16)
        rec = json.loads((self.tmp / "coded_small/coding_record_v1_12.json").read_text())
        self.assertTrue(rec["coder"]["match"])
        self.assertTrue(rec["url_removal"])
        self.assertEqual(registry, reg)

    def test_end_to_end_synthetic(self):
        """t4-shaped raw (coded by v0.42's coder) and Coverage-shaped raw (coded by --code) -> --synthetic -> verdicts."""
        reg = self.bf["registry"]
        d = self.tmp / "e2e"
        (d / "t4").mkdir(parents=True)
        raw, src_rows, _ = make_coverage(11, registry={s: {k: n for k, n in v.items()} for s, v in reg.items()})
        names = {s: v for s, v in reg.items()}
        for r in raw:                                    # answers name brands by their registry names (v0.23 ids)
            if r["text"].startswith("I would suggest "):
                ks = r["text"][len("I would suggest "):-1].split(", ")
                r["text"] = "I would suggest " + ", ".join(names[r["substrate"]][k] for k in ks) + "."
        (d / "v112_raw.jsonl").write_text("".join(json.dumps(r) + "\n" for r in raw), encoding="utf-8")
        t4raw, t = [], datetime(2026, 11, 12, 0, 0, tzinfo=UTC)
        rng = np.random.default_rng(12)
        for sub, raw_sub in S.RAW_SUB.items():
            keys = list(reg[sub])
            rates = rng.uniform(0.05, 0.8, len(keys))
            for m in S.T4_N3:
                for run in S.RUNS:
                    for f in range(6):
                        nm = [reg[sub][k] for k, q in zip(keys, rates) if rng.random() < q]
                        t4raw.append({"call_id": f"{raw_sub}|B|F{f}|{m}|S0|{run}", "substrate": raw_sub, "phase": "B",
                                      "probe_id": f"F{f}", "frame_id": f"F{f}", "model_requested": m, "served_model": m,
                                      "condition": "S0", "run": run, "status": "ok", "error": None,
                                      "text": "Consider " + ", ".join(nm) + "." if nm else "No idea.",
                                      "started_utc": t.isoformat(), "finished_utc": t.isoformat()})
                        t += timedelta(seconds=10)
                for k in keys:
                    yes = rng.random() < 0.7
                    t4raw.append({"call_id": f"{raw_sub}|A|{k}|{m}|S0|1", "substrate": raw_sub, "phase": "A",
                                  "probe_id": f"A-{k}", "brand": reg[sub][k] if sub != "v0.23" else reg[sub][k],
                                  "brand_id": k, "model_requested": m, "served_model": m, "condition": "S0", "run": 1,
                                  "status": "ok", "error": None, "spirit_type": "whisky",
                                  "text": (f"Yes, I am familiar with {reg[sub][k]}." if yes
                                           else f"No, I am not familiar with {reg[sub][k]}."),
                                  "started_utc": t.isoformat(), "finished_utc": t.isoformat()})
                    t += timedelta(seconds=10)
        (d / "t4/t4_raw.jsonl").write_text("".join(json.dumps(r) + "\n" for r in t4raw), encoding="utf-8")
        r = _run([HERE / "code_t4_synthetic_v1_12.py", d / "t4/t4_raw.jsonl", d / "t4/coded"])
        self.assertEqual(r.returncode, 0, r.stderr[-2000:])
        ca, cb = S.read_t4_coded(d / "t4/coded")
        self.assertGreater(len(ca), 200)
        excl, _w = S.t4_excluded(t4raw)
        bt = brand_table_from(cb, excl, reg)              # stands in for v0.42's brand table (same transcription)
        with open(d / "t4/v42_brand_table.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(bt[0]))
            w.writeheader()
            for row in bt:
                w.writerow({k: ("" if v is None or (isinstance(v, float) and not np.isfinite(v)) else v)
                            for k, v in row.items()})
        (d / "t4/v42_verdicts.json").write_text(json.dumps({"models_excluded_condition": []}), encoding="utf-8")
        r = _run([SCORER, "--code", "--raw", d / "v112_raw.jsonl", "--coded", d / "coded"])
        self.assertEqual(r.returncode, 0, r.stderr[-2000:])
        r = _run([SCORER, "--synthetic", d, "--draws", 99])
        self.assertEqual(r.returncode, 0, r.stderr[-3000:])
        doc = json.loads((d / "_score/v112_verdicts.json").read_text(encoding="utf-8"))
        self.assertTrue(doc["parity_gates"]["P2"]["passed"])
        self.assertTrue(doc["parity_gates"]["P3"]["passed"])
        self.assertEqual(doc["comparators"]["source"], "t4 (v0.42, N3, S0)")
        self.assertEqual(set(doc["verdicts"]), set(S.ALL_LEGS))
        self.assertIn(doc["paper_A_verdict"]["verdict"], {"PASS", "FAIL", "MARGINAL", "UNDETERMINED", "INSTRUMENT FAIL"})
        self.assertEqual(doc["analysis_set"]["answered_calls_analysed"], 900)
        self.assertTrue(doc["inputs"]["coder"]["match"])
        rows = S.read_csv_rows(d / "_score/v112_unit_table.csv")
        self.assertEqual(len(rows), 112)
        p_rows = [x for x in rows if x["substrate"] != "v0.23" and x["P_comparator"] != ""]
        self.assertEqual(len(p_rows), 88)                 # v0.23 recognition needs the judge (OFF): P not computed
        coded = S.read_coded(d / "coded")[0]
        names = {(x["call_id"], x["brand"]) for x in coded if x["mentioned"]}
        src = {(r["call_id"], r["brand"]) for r in src_rows if r["mentioned"]}
        agree = len(names & src) / max(len(src), 1)
        self.assertGreater(agree, 0.95)                   # the certified detectors find the names written


if __name__ == "__main__":
    unittest.main()
