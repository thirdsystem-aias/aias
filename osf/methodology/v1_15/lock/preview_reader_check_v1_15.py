#!/usr/bin/env python3
"""Check that the AIAS 6.0 Preview's own reader accepts v1.15's S_t4 table. Lock helper (also run by the tests).

Never touches the Preview's worktree: the Preview scorer and the two scorers it imports are read from the git object
store at the Preview commit (`git show PREVIEW_COMMIT:...`) into a scratch tree under /tmp; the S_t4 table is
committed, with an annotated tag v1.15-prereg-r1, in a separate scratch git repository under /tmp; a subprocess
(PYTHONDONTWRITEBYTECODE=1) imports the copied scorer and calls its read_s_t4 (as `--run --s-t4
REF:PATH:S_t4:rated --s-t4-lock-tag v1.15-prereg-r1` does) and its mq_join against the 112 unit keys of the file the
Preview pins as v0.42's cells (osf/v41/v41_three_wave_table.csv, wave t3). Prints a JSON report; exit 0 iff accepted.

Usage: python3 osf/methodology/v1_15/lock/preview_reader_check_v1_15.py CSV_PATH [--preview-commit f59d4d4]
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PREVIEW_COMMIT = "f59d4d4"
PREVIEW_FILES = ["osf/aias_6_0_preview/scripts/score_aias_6_0_preview.py", "scripts/score_v1_10.py",
                 "scripts/score_v1_14.py"]
S_T4_PATH = "osf/methodology/v1_15/outputs/s_t4_v1_15.csv"
CELLS = "osf/v41/v41_three_wave_table.csv"
TAG = "v1.15-prereg-r1"

CHILD = r"""
import importlib.util, json, sys, csv, io
spec = importlib.util.spec_from_file_location("pv", sys.argv[1])
pv = importlib.util.module_from_spec(spec); spec.loader.exec_module(pv)
rd = pv.Reader(sys.argv[2])
st4 = pv.read_s_t4(rd, "HEAD", sys.argv[3], "S_t4", sys.argv[4], "rated")
cells = rd.rows("HEAD", sys.argv[5])
v042_keys = [(r["substrate"], r["brand"]) for r in cells if r["wave"] == "t3"]
join = pv.mq_join({"v0.42 cells (t3 keys)": v042_keys, "S_t4 unit table": st4["keys"]}, {})
rated = sum(v is not None for v in st4["S"].values())
print(json.dumps({"read_s_t4": "accepted", "rows": len(st4["keys"]), "rated": rated,
                  "mq_join": {k: v for k, v in join.items()}}, default=str))
"""


def git(*a, cwd=None, check=True):
    r = subprocess.run(["git", *a], cwd=cwd, capture_output=True)
    if check and r.returncode != 0:
        raise SystemExit(f"git {' '.join(a)}: {r.stderr.decode()[:300]}")
    return r.stdout


def check(csv_path: Path, preview_commit: str = PREVIEW_COMMIT) -> dict:
    tmp = Path(tempfile.mkdtemp(prefix="v115_preview_check_", dir="/tmp"))
    try:
        code = tmp / "code"
        for p in PREVIEW_FILES:
            (code / p).parent.mkdir(parents=True, exist_ok=True)
            (code / p).write_bytes(git("-C", str(ROOT), "show", f"{preview_commit}:{p}"))
        data = tmp / "data"
        (data / S_T4_PATH).parent.mkdir(parents=True, exist_ok=True)
        (data / S_T4_PATH).write_bytes(Path(csv_path).read_bytes())
        (data / CELLS).parent.mkdir(parents=True, exist_ok=True)
        (data / CELLS).write_bytes(git("-C", str(ROOT), "show", f"HEAD:{CELLS}"))
        env = dict(os.environ, GIT_AUTHOR_NAME="check", GIT_AUTHOR_EMAIL="check@example.invalid",
                   GIT_COMMITTER_NAME="check", GIT_COMMITTER_EMAIL="check@example.invalid")
        for a in (["init", "-q"], ["add", "-A"], ["commit", "-q", "-m", "scratch"], ["tag", "-a", TAG, "-m", "scratch"]):
            r = subprocess.run(["git", *a], cwd=data, env=env, capture_output=True)
            if r.returncode != 0:
                raise SystemExit(f"scratch git {a}: {r.stderr.decode()[:300]}")
        r = subprocess.run([sys.executable, "-c", CHILD, str(code / PREVIEW_FILES[0]), str(data), S_T4_PATH, TAG, CELLS],
                           capture_output=True, text=True, cwd=tmp, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        if r.returncode != 0:
            return {"accepted": False, "error": r.stderr[-1500:], "scratch": str(tmp)}
        out = json.loads(r.stdout.strip().splitlines()[-1])
        tables = out["mq_join"]["tables"]          # mq_join halts (child exits non-zero) on any key mismatch
        out["accepted"] = (out["rows"] == 112 and tables["S_t4 unit table"]["one_to_one"]
                           and tables["v0.42 cells (t3 keys)"]["one_to_one"])
        out["preview_commit"], out["scratch"] = preview_commit, str(tmp)
        return out
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    pc = argv[argv.index("--preview-commit") + 1] if "--preview-commit" in argv else PREVIEW_COMMIT
    res = check(Path(argv[0]), pc)
    print(json.dumps(res, indent=1, default=str))
    return 0 if res.get("accepted") else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
