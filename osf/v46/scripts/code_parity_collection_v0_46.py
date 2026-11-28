#!/usr/bin/env python3
"""
code_parity_collection_v0_46.py -- AIAS v0.46 (#76): regenerated code-parity record for the collection
(DEVIATIONS Entry 4; added after the lock, ex ante: no #76 data exist).

Why: the locked osf/v46/prereg/code_parity_v0_46.json fingerprints predictors_v0_46.py as it was before commit
9bbd96f ("docstrings cite stage1_manuscript_r2.md ..."; 7 files, 10 lines in, 10 out), so gates_v0_46.green() and
acquire_v0_46.py --run refuse. The locked file is kept unchanged under its name.

What it does (no model is called; t4 inputs are read from git by gates_v0_46, as at the lock):
  1. AST check: for each of the seven files 9bbd96f touched, the module parsed at 9bbd96f^ and at 9bbd96f, with every
     docstring removed (comments are not in the AST), is compared (ast.dump). Result on 2026-11-28: six files
     identical; acquire_v0_46.py differs in one string constant only, the argparse description (--help text,
     "stage1_manuscript_r1.md" -> "r2.md", line 1180). It stops (exit 3, nothing written) on any other difference,
     or on any difference in a file the gates fingerprint; the help-text difference is recorded and flagged for
     the author's decision (DEVIATIONS Entry 4).
  2. Runs gates_v0_46.run_gates() unchanged and writes its result, plus the AST check, to
     osf/v46/prereg/code_parity_v0_46_collection.json, which acquire_v0_46.gates_guard reads.
Check afterwards: python3 osf/v46/scripts/gates_v0_46.py --check --out osf/v46/prereg/code_parity_v0_46_collection.json
"""
import ast
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gates_v0_46 as GT  # noqa: E402

ROOT = GT.ROOT
COMMIT = "9bbd96f9699dee61b365d4143be4f51851039aba"
OUT = ROOT / "osf" / "v46" / "prereg" / "code_parity_v0_46_collection.json"


def _strip_docstrings(tree):
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            b = node.body
            if b and isinstance(b[0], ast.Expr) and isinstance(getattr(b[0], "value", None), ast.Constant) \
                    and isinstance(b[0].value.value, str):
                node.body = b[1:] or [ast.Pass()]
    return tree


def _diffs(ta, tb):
    """Where two docstring-free trees differ: walked in parallel; if only constants differ, list them (line, before,
    after); otherwise report a structural difference."""
    na, nb = list(ast.walk(ta)), list(ast.walk(tb))
    if len(na) != len(nb) or any(type(x) is not type(y) for x, y in zip(na, nb)):
        return [{"structural": True}]
    out = []
    for x, y in zip(na, nb):
        if isinstance(x, ast.Constant) and x.value != y.value:
            out.append({"line_before": x.lineno, "line_after": y.lineno, "before": x.value, "after": y.value})
        elif not isinstance(x, ast.Constant) and ast.dump(x, include_attributes=False) != ast.dump(y, include_attributes=False) \
                and not any(isinstance(c, ast.AST) for c in ast.iter_child_nodes(x)):
            out.append({"line_before": getattr(x, "lineno", None), "node": type(x).__name__, "structural": True})
    return out


def _show(rev, path):
    return subprocess.run(["git", "-C", str(ROOT), "show", f"{rev}:{path}"], capture_output=True, text=True,
                          check=True).stdout


def ast_check(commit=COMMIT):
    files = subprocess.run(["git", "-C", str(ROOT), "diff", "--name-only", f"{commit}^", commit], capture_output=True,
                           text=True, check=True).stdout.split()
    out = {"commit": commit, "files": {}, "method": "ast.dump of each module with docstrings removed, before vs after"}
    for f in files:
        ta, tb = _strip_docstrings(ast.parse(_show(f"{commit}^", f))), _strip_docstrings(ast.parse(_show(commit, f)))
        a, b = ast.dump(ta), ast.dump(tb)
        out["files"][f] = {"executable_code_identical": a == b}
        if a != b:
            out["files"][f]["differences"] = _diffs(ta, tb)
    out["all_identical"] = bool(files) and all(v["executable_code_identical"] for v in out["files"].values())
    out["n_files"] = len(files)
    # Classification (reported, the decision is the author's): a difference is "CLI help text only" when it is a
    # string constant on a line that builds argparse.ArgumentParser(description=...) in a file the gates do not
    # fingerprint. Anything else is a code change.
    gated = set(GT.code_fingerprint())
    help_only = True
    for f, v in out["files"].items():
        for d in v.get("differences", []):
            line = _show(commit, f).splitlines()[(d.get("line_after") or 1) - 1]
            ok = not d.get("structural") and "argparse.ArgumentParser(description=" in line and f not in gated
            d["classified"] = "CLI help text only" if ok else "code change"
            help_only = help_only and ok
    out["differences_are_cli_help_text_only"] = help_only
    out["gated_files_identical"] = all(out["files"].get(f, {"executable_code_identical": True})["executable_code_identical"]
                                       for f in gated)
    return out


def main():
    chk = ast_check()
    for f, v in chk["files"].items():
        print(f"  AST {f}: {'identical' if v['executable_code_identical'] else 'DIFFERS'}")
    if not chk["all_identical"] and not (chk["differences_are_cli_help_text_only"] and chk["gated_files_identical"]):
        print("STOP: 9bbd96f changed executable code; DEVIATIONS Entry 4 is not enough. Nothing written.")
        return 3
    if not chk["all_identical"]:
        for f, v in chk["files"].items():
            for d in v.get("differences", []):
                print(f"  NOTE {f}:{d['line_after']}: {d['classified']}: {d['before']!r} -> {d['after']!r}")
        print("  NOTE: not docstrings/comments only; CLI help text only, outside the gated files (author to accept)")
    res = GT.run_gates()
    res["ast_check_9bbd96f"] = chk
    res["record"] = ("regenerated for the collection (DEVIATIONS Entry 4); the locked code_parity_v0_46.json is kept "
                     "unchanged")
    OUT.write_text(json.dumps(res, indent=1, sort_keys=True, default=str) + "\n", encoding="utf-8")
    print(f"[v46 parity] both_pass={res['both_pass']} G1 {res['G1']['units_compared']}/{res['G1']['mismatches']} "
          f"G2 {res['G2']['rated_units_compared']}/{res['G2']['mismatches']} -> {OUT}")
    return 0 if res["both_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
