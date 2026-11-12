#!/usr/bin/env python3
"""
make_scenarios_aias6.py -- SYNTHETIC outputs of the AIAS 6.0 Preview scorer for the paper pipeline. SYNTHETIC ONLY.

Run scenarios: the locked scorer itself (osf/aias_6_0_preview/scripts/score_aias_6_0_preview.py, `run()`,
require_lock=False, the mode its own tests use) on a scratch git repository built by its own test fixture
(`Synth` in scripts/tests/test_score_aias_6_0_preview.py, imported read-only: invented brand names, random scores, a
stub of every component output at the refs the real run names). An "overlay" commit on top of the fixture changes
only what a scenario needs (a component's gate words, the hash records that chain them, an S_t4 table), and the
refs of the changed components are moved to it. The scorer writes its four files with its own schemas:
  gates_aias_6_0_preview.json  results_aias_6_0_preview.json  profile_aias_6_0_preview.csv  inputs_read_aias_6_0_preview.json
Beside them the generator copies the component files the paper reads to name a MARGINAL leg (`components/`:
v1.14 Stage 1, v1.12 and v1.13 verdict files, from the same refs; their SHA-256 are in inputs_read).

Derived scenarios copy a run scenario and give some S-test / I-test statistics other values; every verdict word is
recomputed with the scorer's own functions (band, component_status, h_structure, wording_class, composite_k1,
verdict_changes). Every JSON output gets "synthetic_fixture".

  python3 papers/aias_6_0_preview/tests/make_scenarios_aias6.py OUT [scenario ...]

Refuses any OUT under osf/. Scratch repositories live in a temporary directory and are deleted.
"""
import hashlib
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SDIR = ROOT / "osf/aias_6_0_preview/scripts"
sys.path.insert(0, str(SDIR))
sys.path.insert(0, str(SDIR / "tests"))
import score_aias_6_0_preview as S  # noqa: E402  (read-only)
import test_score_aias_6_0_preview as T  # noqa: E402  (read-only: its Synth fixture and git helpers)

MARK = "SYNTHETIC TEST DATA - NOT RESULTS (papers/aias_6_0_preview/tests/make_scenarios_aias6.py, scenario {s})"
OUT_NAMES = S.OUT_NAMES
COMPONENT_FILES = {"v1.14": "osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json",
                   "v1.12": "osf/methodology/v1_12/v112_verdicts.json",
                   "v1.13": "osf/methodology/v1_13/v1_13_verdicts.json"}
QUIET = lambda *a, **k: None  # noqa: E731
OVERLAY_DATE = "2026-11-21T12:00:00-06:00"

# run scenarios: (Synth options, overlay)
RUNS = {
    # the state of the inputs on Nov 11: v1.14 Stage 1 MARGINAL (Ranking under review; v1.12's H5 reported, not
    # gating), no S_t4 (Sentiment NOT RUN: legacy reading beside the profile), Coverage and Grounding PASS
    "ranking_marginal": ({"h5_gates": False}, {"stage1": {"STAGE1_VERDICT": "MARGINAL",
                                                          "H1_Sep_Presence": {"verdict": "MARGINAL", "rho": 0.41, "n": 70}}}),
    "retest_pending": ({}, {}),                                           # Stage 1 SEPARABLE: PASS, retest pending
    "six_parts": ({"stage2": True}, {"s_t4": True}),                      # Stage 2 GATE PASS; S_t4 -> S PASS_AI; k = 6
    "reduced_panel": ({"dropped_s0": True}, {}),                          # section 4.3: no structure test
    "parts_failed": ({"h5_gates": False}, {"stage1": {"STAGE1_VERDICT": "FAIL",
                                                      "H1_Sep_Presence": {"verdict": "FALSIFIED", "rho": 0.57, "n": 70}},
                                           "v112_gate": "MARGINAL", "v113_gate": "UNDETERMINED", "s_t4": True,
                                           "v111": {"H2": "FALSIFIED"},
                                           "v042": {"H_Gen_Presence": "FALSIFIED", "H_Gen_Phi": "UNDETERMINED"}}),
    "not_run": ({}, {"drop_refs": ["v1.14", "v1.12", "v1.13"]}),          # no component output by the data lock
}
# derived scenarios: (base run scenario, statistics changed); "*" = every other S-test / I-test of K
DERIVED = {
    "ranking_marginal_confirmed": ("ranking_marginal", {"S": {"*": 0.08}, "I": {"*": 0.10},
                                                       "v042": {"H_Gen_Presence": "MARGINAL"}}),
    "ranking_marginal_partial": ("ranking_marginal", {"S": {"*": 0.08, "PxCov": 0.38}, "I": {"*": 0.10}}),
    "six_confirmed": ("six_parts", {"S": {"*": 0.07}, "I": {"*": 0.12}}),
    "six_partial": ("six_parts", {"S": {"*": 0.07, "PxC": 0.36, "CxS": 0.33}, "I": {"*": 0.12, "G": 0.34}}),
    "six_falsified": ("six_parts", {"S": {"*": 0.07, "PxC": 0.55, "PxR": 0.58, "PxS": 0.61, "PxCov": 0.52,
                                          "PxG": 0.66}, "I": {"*": 0.12}}),
    "six_undetermined": ("six_parts", {"S": {"*": 0.07}, "n": {"PxC": 20},
                                       "I": {"*": 0.12, "R": None, "S": None, "Cov": None, "G": None}}),
}
SCENARIOS = list(RUNS) + list(DERIVED)


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode("utf-8")).hexdigest()


def git_bytes(d, ref, rel):
    return subprocess.run(["git", "-C", str(d), "show", f"{ref}:{rel}"], capture_output=True, check=True).stdout


# --------------------------------------------------------------------------- run scenarios
def overlay(syn, ov):
    """One commit on top of the fixture with the scenario's changes; returns (refs, s_t4)."""
    d = syn.d
    refs = dict(syn.refs)
    moved = set()
    s1_text = syn.s1_text
    if "stage1" in ov:
        s1 = json.loads(syn.s1_text)
        for k, v in ov["stage1"].items():
            s1[k] = dict(s1.get(k) or {}, **v) if isinstance(v, dict) else v
        s1_text = json.dumps(s1, indent=1)
        T.write(d, COMPONENT_FILES["v1.14"], s1_text)
        moved.add("v1.14")
    if "stage1" in ov or "v112_gate" in ov:                       # v1.12 records the Stage 1 file it read
        v = json.loads(git_bytes(d, "v112-scored", COMPONENT_FILES["v1.12"]))
        v["H5_ranking_source"] = {"sha256": sha(s1_text)}
        if "stage1" in ov:                                        # Stage 1 not SEPARABLE: H5 reported, not gating
            v["paper_A_verdict"]["legs"].pop("H5_Sep_Ranking", None)
            v["paper_A_verdict"]["h5_reported_not_gating"] = True
        if ov.get("v112_gate"):
            v["paper_A_verdict"]["verdict"] = v["paper_A_verdict"]["label"] = ov["v112_gate"]
            if ov["v112_gate"] == "MARGINAL":
                v["paper_A_verdict"]["legs"]["H4_Reliability"] = "MARGINAL"
                v["verdicts"]["H4_Reliability"] = "MARGINAL"
        T.write(d, COMPONENT_FILES["v1.12"], json.dumps(v))
        moved.add("v1.12")
    if "stage1" in ov or "v113_gate" in ov:
        v = json.loads(git_bytes(d, "v113-scored", COMPONENT_FILES["v1.13"]))
        v["H4_ranking_source"] = {"sha256": sha(s1_text)}
        if ov.get("v113_gate"):
            v["gate"]["verdict"] = ov["v113_gate"]
        T.write(d, COMPONENT_FILES["v1.13"], json.dumps(v))
        moved.add("v1.13")
    if "v111" in ov:
        rel = "osf/methodology/v1_11/outputs/v1_11_verdicts.json"
        v = json.loads(git_bytes(d, "v111-scored", rel))
        v["VERDICTS"].update(ov["v111"])
        T.write(d, rel, json.dumps(v))
        moved.add("v1.11")
    if "v042" in ov:
        rel = "osf/v42/v42_verdicts.json"
        v = json.loads(git_bytes(d, "v0.42-scoring-locked", rel))
        for k, w in ov["v042"].items():
            v["verdicts"][k]["verdict"] = w
        T.write(d, rel, json.dumps(v))
        moved.add("v0.42")
    if ov.get("s_t4"):
        rng = np.random.default_rng(3)
        rows = [{"substrate": u[0], "brand": u[1], "rated": int(syn.ment[u] >= 2),
                 "S": round(float(rng.uniform(30, 90)), 4) if syn.ment[u] >= 2 else ""} for u in syn.units]
        T.write(d, "osf/s_t4/s_t4_unit_table.csv", T.csv_text(rows))
    s_t4 = None
    if moved or ov.get("s_t4"):
        T.commit(d, "scenario overlay", OVERLAY_DATE, "scenario-overlay")
        for name in moved:
            refs[name] = "scenario-overlay"
        if ov.get("s_t4"):
            T.git(d, "tag", "-a", "s-t4-prereg-r1", "-m", "S_t4 lock", "HEAD~1", date="2026-11-20T12:00:00-06:00")
            s_t4 = {"ref": "scenario-overlay", "path": "osf/s_t4/s_t4_unit_table.csv", "column": "S",
                    "rated_col": "rated", "lock_tag": "s-t4-prereg-r1"}
    for name in ov.get("drop_refs", []):
        refs.pop(name, None)
    return refs, s_t4


def mark(dest, name):
    for k in ("gates", "results", "inputs"):
        p = dest / OUT_NAMES[k]
        doc = json.loads(p.read_text(encoding="utf-8"))
        doc["synthetic_fixture"] = MARK.format(s=name)
        p.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def run_scenario(name, out, n_perm=200, n_boot=200, n_pa=100):
    opts, ov = RUNS[name]
    dest = out / name
    if dest.exists():
        shutil.rmtree(dest)
    with tempfile.TemporaryDirectory(prefix="aias6_scen_") as tmp:
        syn = T.Synth(tmp, **opts)
        refs, s_t4 = overlay(syn, ov)
        S.run(syn.d, refs, dest, syn.inputs(), s_t4=s_t4, n_perm=n_perm, n_boot=n_boot, n_pa=n_pa,
              require_lock=False, log=QUIET)
        comp = dest / "components"
        comp.mkdir()
        for cname, rel in COMPONENT_FILES.items():
            if cname in refs:
                (comp / Path(rel).name).write_bytes(git_bytes(syn.d, refs[cname], rel))
    mark(dest, name)
    return dest


# --------------------------------------------------------------------------- derived scenarios
def _ok(t):
    return (t.get("n") or 0) >= S.N_FLOOR_UNITS and (t.get("categories") or 0) >= S.MIN_CATEGORIES


def _f(x):
    return float("nan") if x is None else float(x)


def restructure(res):
    """Every verdict word of res["structure"] from its statistics, with the scorer's functions."""
    st = res["structure"]
    K = st["K"]
    s_res = {}
    for t in st["S_tests"].values():
        if t.get("source", "Preview") == "Preview":
            t["verdict"] = S.band(_f(t["rho"]), _ok(t))
        s_res[tuple(t["pair"])] = t
    for t in st["I_tests"].values():
        r = _f(t.get("R_adj"))
        t["verdict"] = S.band(r, True) if math.isfinite(r) else "UNDETERMINED"
    status = {m: S.component_status(m, K, s_res, st["I_tests"]) for m in K}
    hs = S.h_structure(K, status, bool(res["MQ_Panel"]["ok"]))
    st.update(status=status, H_Structure=hs, wording_class=S.wording_class(hs["verdict"], hs["k"]),
              H_PC_N3=s_res[("P", "C")]["verdict"])
    if "composite_check" in st:
        st["composite_check"].update(S.composite_k1(hs["verdict"], st["H_PC_N3"]))
        res["descriptives"]["D8_composite_check"] = st["composite_check"]
    sens = res.get("sensitivities") or {}
    if "verdict_changes" in sens:
        sens["verdict_changes"] = S.verdict_changes(S._verdicts_only(st), sens)


def derive(name, out):
    base, mods = DERIVED[name]
    dest = out / name
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(out / base, dest)
    rp, gp, ip = (dest / OUT_NAMES[k] for k in ("results", "gates", "inputs"))
    res, gates, ins = (json.loads(p.read_text(encoding="utf-8")) for p in (rp, gp, ip))
    st = res["structure"]
    for key, t in st["S_tests"].items():
        v = mods["S"].get(key, mods["S"].get("*"))
        if v is not None:
            sign = -1.0 if _f(t["rho"]) < 0 else 1.0
            t["rho"] = sign * v
            t["ci90"] = [t["rho"] - 0.2, t["rho"] + 0.2]
            t["source"] = "Preview"           # a changed statistic is no longer the Paper A's own (synthetic)
        if key in (mods.get("n") or {}):
            t["n"] = mods["n"][key]
            t["source"] = "Preview"
    for x, t in st["I_tests"].items():
        v = mods["I"].get(x, mods["I"].get("*", "keep"))
        if v is None:
            t.update(n=21, R2=None, R2_adj=None, R_adj=None, p_perm=None)
        elif v != "keep":
            t.update(R_adj=v, R2_adj=v * v, R2=v * v, n=max(t.get("n") or 0, 40))
    for k, w in (mods.get("v042") or {}).items():
        part = "P" if k == "H_Gen_Presence" else "C"
        gates[k] = w
        for doc in (res, gates):
            doc["labels"][part]["bridge"] = S.BRIDGE[w]
    restructure(res)
    for doc, p in ((res, rp), (gates, gp), (ins, ip)):
        doc["synthetic_fixture"] = MARK.format(s=name)
        p.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return dest


def make(out_root, scenarios=None):
    out_root = Path(out_root).resolve()
    if str(out_root).startswith(str((ROOT / "osf").resolve())):
        raise SystemExit(f"REFUSED: {out_root} is under osf/")
    out_root.mkdir(parents=True, exist_ok=True)
    want = scenarios or SCENARIOS
    need = [s for s in RUNS if s in want or any(DERIVED[x][0] == s for x in want if x in DERIVED)]
    for s in need:
        run_scenario(s, out_root)
    for s in want:
        if s in DERIVED:
            derive(s, out_root)
    done = {}
    for s in want:
        r = json.loads((out_root / s / OUT_NAMES["results"]).read_text(encoding="utf-8"))
        done[s] = (r["gate_states"], r["K"], r["structure"]["H_Structure"]["verdict"], r["structure"].get("H_PC_N3"),
                   r["structure"]["wording_class"])
    return done


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for s, v in make(sys.argv[1], sys.argv[2:] or None).items():
        print(f"{s:28s} {v}")
