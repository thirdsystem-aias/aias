"""Copy v1.18's two outputs from branch v1.18 (git show, so the paper worktree never reads a working tree) into
papers/v1_13/inputs/v1_18/ and record their SHA-256, the branch commit and the source paths in INPUTS_v1_18.json.
Usage: python3 papers/v1_13/inputs/make_inputs_v1_18.py [COMMIT]   (default: the tip of branch v1.18)"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "v1_18"
SRC = "osf/methodology/v1_18/outputs/"
NAMES = ["v1_18_results.json", "descriptive_v1_18.json"]


def git(*a):
    return subprocess.run(["git", "-C", str(ROOT), *a], check=True, capture_output=True).stdout


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    commit = git("rev-parse", argv[0] if argv else "v1.18").decode().strip()
    OUT.mkdir(parents=True, exist_ok=True)
    rec = {"branch": "v1.18", "commit": commit, "files": {}}
    for n in NAMES:
        data = git("show", f"{commit}:{SRC}{n}")
        (OUT / n).write_bytes(data)
        rec["files"][n] = {"source": SRC + n, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
    (OUT / "INPUTS_v1_18.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(rec, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
