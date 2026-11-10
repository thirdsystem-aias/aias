"""AIAS v0.44: write the lock manifest (SHA-256 of every file the pre-registration locks). No model is called.

  python3 osf/v44/scripts/lock_manifest_v0_44.py --draft   -> osf/v44/LOCK_MANIFEST_v0_44_DRAFT.sha256 (before the lock)
  python3 osf/v44/scripts/lock_manifest_v0_44.py           -> osf/v44/LOCK_MANIFEST_v0_44.sha256 (at the lock)
Format: `<sha256>  <path relative to the repository root>` (checkable with `shasum -a 256 -c`). The v0.44 files are
listed with the files they import or read from earlier phases. Untracked staging copies (_osf_stage*) and data are
not listed.
"""
import hashlib
import os
import sys
from pathlib import Path

ROOT = Path(os.environ.get("AIAS_ROOT", str(Path(__file__).resolve().parents[3])))
V44 = ROOT / "osf/v44"
DEPENDENCIES = [   # read or imported by the v0.44 scripts and tests (unchanged files of earlier phases)
    "osf/v42/scripts/score_v0_42.py", "osf/v42/scripts/code_t4_v0_42.py", "osf/v42/scripts/budget_v0_42.py",
    "osf/v42/scripts/acquire_v0_42.py", "osf/v42/prereg/cost_estimate_v0_42_r2.json",
    "osf/v42/prereg/PRE_REGISTRATION_v0_42.md", "osf/v42/prereg/feasibility_v0_42.json",
    "osf/v41/scripts/score_v41.py", "osf/v41/v41_three_wave_table.csv", "scripts/run_acquisition_v22.py",
]


def files():
    out = [V44 / "DEVIATIONS.md"]
    for sub, pat in (("prereg", "*"), ("registries", "*.csv"), ("scripts", "*.py"), ("scripts/tests", "*.py")):
        out += sorted(p for p in (V44 / sub).glob(pat) if p.is_file())
    out = [p.relative_to(ROOT).as_posix() for p in out]
    return out + DEPENDENCIES


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def main(argv=None):
    draft = "--draft" in (argv if argv is not None else sys.argv[1:])
    target = V44 / ("LOCK_MANIFEST_v0_44_DRAFT.sha256" if draft else "LOCK_MANIFEST_v0_44.sha256")
    lines = [f"{sha(p)}  {p}" for p in files()]
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(lines)} files -> {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
