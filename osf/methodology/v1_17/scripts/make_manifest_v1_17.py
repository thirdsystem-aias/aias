"""Writes LOCK_MANIFEST_v1_17.sha256: SHA-256 of every input, script, test and document of the v1.17 lock.
Paths are relative to the repository root. Run after the last edit and before the lock commit."""
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v1_17_lib as L   # noqa: E402

M = "osf/methodology/v1_17/"
FILES = (
    # inputs (read by --run)
    [f"osf/v42/data/coded/{s}_phase_b.csv" for s in L.CATEGORIES.values()]
    + ["osf/v41/v41_three_wave_table.csv", "osf/v42/v42_verdicts.json", "osf/v42/prereg/probes_v0_42.jsonl"]
    # code and tests
    + [M + "scripts/" + f for f in ("v1_17_lib.py", "analyze_v1_17.py", "build_charts_v1_17.py",
                                    "write_note_v1_17.py", "make_manifest_v1_17.py")]
    + [M + "tests/test_v1_17.py", M + "tests/run_tests_v1_17.sh", M + "tests/test_log_prelock.txt"]
    # documents and pre-lock records
    + [M + "PRE_REGISTRATION_v1_17.md", M + "README.md", M + "DEVIATIONS.md",
       M + "outputs/prelock/loader_check_v1_17.json", M + "outputs/dry_run/dry_run_v1_17.json"])


def main():
    lines = [f"# v1.17 lock manifest (sha256  path from repository root). Written "
             f"{datetime.now(timezone.utc).isoformat(timespec='seconds')} by make_manifest_v1_17.py."]
    for rel in FILES:
        lines.append(f"{L.sha256(L.ROOT / rel)}  {rel}")
    out = L.V117 / "LOCK_MANIFEST_v1_17.sha256"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(FILES)} files)")


if __name__ == "__main__":
    main()
