#!/usr/bin/env python3
"""AIAS v0.62 gate P1 (kernel parity), r2 draft. No model is called; no v0.42 answer is read.

The v0.62 scorer carries transcriptions of v0.42's pi-hat and phi kernels (score_v0_62.unit_values, phi_m). This
gate checks them against v0.42's LOCKED kernels, pinned to tag v0.42-prereg-r1 (commit 58d1891...): the kernel
functions are read from the tag with `git show` (score_v0_42.pi_hat, phi_runs, phi_panel; score_v41.phi_m, phi_of
and the constants they use) and executed unchanged in an isolated namespace, so v0.42's import machinery (certified
matchers, ROOT shim) is not needed and nothing in the v0.42 worktree is written.

Input: synthetic English-shaped coded Phase B tables (112 registry units, 3 models x 3 runs x 6 questions per
category, seed 620151), with zero, saturated and partly missing cells, and a model-run with 5 of 6 answers (phi
'missing' for that run). v0.42's REAL t4 answers are not read (programme rule for this lane); the same comparison on
t4's coded tables is the lock-time half of P1 (pre-registration r2 section 7.3).

PASS = for every unit, pi equal (==) and (phi, partition) equal (== / both None), on every scenario.
Run: python3 osf/v62/scripts/gate_p1_v0_62.py [--repo ~/aias/_worktrees/v0.42] -> osf/v62/prereg/gate_P1_v0_62_r2.json
"""
import argparse
import ast
import collections
import csv
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
V62 = HERE.parent
sys.path.insert(0, str(HERE))
import score_v0_62 as S  # noqa: E402

TAG, TAG_COMMIT = "v0.42-prereg-r1", "58d1891bf2fa65b2a0f2f1e2adfcffc93fd56e0f"
FILES = {"v42": "osf/v42/scripts/score_v0_42.py", "v41": "osf/v41/scripts/score_v41.py"}
WANT = {"v42": ["pi_hat", "phi_runs", "phi_panel"], "v41": ["phi_m", "phi_of"]}
CONSTS = {"v42": ["F", "RUNS"], "v41": ["M", "F"]}
SUBMAP = {"v19": "v0.19", "v20": "v0.20", "v21": "v0.21", "v22": "v0.22", "v23": "v0.23"}


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout


def pinned_namespace(repo):
    commit = git(repo, "rev-parse", TAG + "^{commit}").strip()
    if commit != TAG_COMMIT:
        raise SystemExit(f"tag {TAG} -> {commit}, expected {TAG_COMMIT}")
    src = {k: git(repo, "show", f"{TAG}:{p}") for k, p in FILES.items()}
    ns41 = {"np": np, "math": math}
    ns42 = {"np": np, "math": math, "NAN": float("nan")}
    for key, ns in (("v41", ns41), ("v42", ns42)):
        tree = ast.parse(src[key])
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in CONSTS[key] for t in node.targets):
                exec(compile(ast.Module([node], []), FILES[key], "exec"), ns)
            if isinstance(node, ast.FunctionDef) and node.name in WANT[key]:
                exec(compile(ast.Module([node], []), FILES[key], "exec"), ns)
    ns42["phi_m"] = ns41["phi_m"]
    missing = [f for k in WANT for f in WANT[k] if f not in (ns41 if k == "v41" else ns42)]
    if missing:
        raise SystemExit(f"pinned functions not found: {missing}")
    return ns42, {"commit": commit, "files": FILES, "functions": WANT}


class D42:
    """The interface v0.42's kernels read (brands, n(cond, model, run, sub), kk(cond, model, run, sub, brand))."""

    def __init__(self, units, rows):
        self.brands = list(units)
        self.ans, self.k = collections.defaultdict(set), collections.defaultdict(int)
        for r in rows:
            self.ans[("S0", r["model"], int(r["run"]), r["substrate"])].add(r["call_id"])
            self.k[("S0", r["model"], int(r["run"]), r["substrate"], r["brand"])] += int(r["mentioned"])

    def n(self, cond, model, run, sub):
        return len(self.ans.get((cond, model, run, sub), ()))

    def kk(self, cond, model, run, sub, brand):
        return self.k.get((cond, model, run, sub, brand), 0)


def units():
    rows = list(csv.DictReader(open(V62 / "translations" / "brand_aliases_v0_62_r2.csv", encoding="utf-8")))
    return [(SUBMAP[r["substrate"]], r["brand"]) for r in rows]


def synth(U, seed, scenario):
    rng = np.random.default_rng(seed)
    rows = []
    by_sub = collections.defaultdict(list)
    for s, b in U:
        by_sub[s].append(b)
    p = {u: rng.uniform(0, 1) for u in U}
    special = {U[0]: 0.0, U[1]: 1.0, U[20]: 0.0, U[45]: 1.0}
    for m in S.MODELS:
        for r in S.RUNS:
            for s, bs in by_sub.items():
                nq = 6
                if scenario == "missing" and m == "gpt-6-astra" and r == 2 and s == "v0.20":
                    nq = 5
                if scenario == "missing" and m == "gemini-4-argon" and s == "v0.22" and r in (1, 3):
                    nq = 4
                for q in range(nq):
                    cid = f"en|{s}|B|q{q + 1}|{m}|S0|{r}"
                    for b in bs:
                        pr = special.get((s, b), p[(s, b)])
                        rows.append({"call_id": cid, "model": m, "run": r, "substrate": s, "brand": b,
                                     "condition": "S0", "mentioned": int(rng.uniform() < pr)})
    return rows


def compare(ns, U, rows):
    D = D42(U, rows)
    pi42 = ns["pi_hat"](D, S.MODELS, "S0")
    ph42 = ns["phi_panel"](D, S.MODELS, "S0")
    mine = S.unit_values(U, rows)
    bad = []
    for u in U:
        a, b = pi42[u], mine[u]["pi"]
        if not (a == b or (math.isnan(a) and math.isnan(b))):
            bad.append((u, "pi", a, b))
        phi_a, part_a = ph42[u][0], ph42[u][1]
        if (phi_a, part_a) != (mine[u]["phi"], mine[u]["partition"]):
            bad.append((u, "phi", (phi_a, part_a), (mine[u]["phi"], mine[u]["partition"])))
    parts = collections.Counter(mine[u]["partition"] for u in U)
    return bad, dict(parts)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=str(Path.home() / "aias" / "_worktrees" / "v0.42"))
    ap.add_argument("--out", default=str(V62 / "prereg" / "gate_P1_v0_62_r2.json"))
    a = ap.parse_args(argv)
    ns, pin = pinned_namespace(a.repo)
    U = units()
    res, ok = {}, True
    for scen, seed in (("complete", 620151), ("missing", 620152), ("complete_b", 620153)):
        bad, parts = compare(ns, U, synth(U, seed, scen))
        res[scen] = {"seed": seed, "units": len(U), "mismatches": len(bad), "first": [str(x) for x in bad[:5]],
                     "partitions": parts}
        ok &= not bad
    out = {"gate": "P1 kernel parity (synthetic English-shaped tables; v0.42 real answers not read)",
           "pinned": pin, "scenarios": res, "result": "PASS" if ok else "FAIL"}
    Path(a.out).write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
