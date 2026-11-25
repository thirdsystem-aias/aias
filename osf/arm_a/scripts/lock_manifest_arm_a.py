#!/usr/bin/env python3
"""Arm A: write the lock manifest (SHA-256 of every file the pre-registration locks). No API call.

  python3 osf/arm_a/scripts/lock_manifest_arm_a.py --draft   -> osf/arm_a/LOCK_MANIFEST_arm_a_DRAFT.sha256 (before the lock)
  python3 osf/arm_a/scripts/lock_manifest_arm_a.py --at-lock -> osf/arm_a/LOCK_MANIFEST_arm_a.sha256 (at the lock only)
Format: `<sha256>  <path relative to the repository root>` (checkable with `shasum -a 256 -c`), as v0.44. Files read
from other refs (locked wave files, the v0.40 and v0.25 files, the website explorer data) are fixed by SHA-256 inside
build_inputs_arm_a.py and are listed below by ref so the manifest names them too.
"""
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_inputs_arm_a as BI   # noqa: E402
import params_arm_a as P          # noqa: E402

PREREG_FILES = ["prereg/arm_a_seo_prereg_draft_r4.md", "prereg/armA_prelock_notes_r1.md",
                "prereg/armA_power_sim_r3.py", "prereg/armA_power_sim_out_r3.txt",
                "prereg/armA_crosscheck/armA_domain_crosscheck.py",
                "prereg/armA_crosscheck/crosscheck_20261124T133629Z.csv",
                "prereg/armA_crosscheck/raw_responses_20261124T133629Z.jsonl",
                "prereg/armA_crosscheck/summary_20261124T133629Z.json"]


def files():
    arm = P.ARM
    out = [arm / "DEVIATIONS.md"]
    for sub, pat in (("prereg", "*"), ("registries", "*.csv"), ("scripts", "*.py"), ("tests", "*.py"),
                     ("tests/fixtures", "*.json")):
        out += sorted(p for p in (arm / sub).glob(pat) if p.is_file())
    rel = [p.relative_to(P.ROOT).as_posix() for p in out]
    return rel + [f for f in PREREG_FILES if (P.ROOT / f).exists()]


def main(argv=None):
    draft = "--draft" in (argv if argv is not None else sys.argv[1:])
    if not draft and "--at-lock" not in (argv if argv is not None else sys.argv[1:]):
        print("refused: the final manifest is written only at the lock (--at-lock); use --draft before it")
        return 2
    target = P.ARM / ("LOCK_MANIFEST_arm_a_DRAFT.sha256" if draft else "LOCK_MANIFEST_arm_a.sha256")
    lines = [f"{hashlib.sha256((P.ROOT / f).read_bytes()).hexdigest()}  {f}" for f in files()]
    for k, s in BI.SOURCES.items():
        lines.append(f"{s['sha256']}  {s['ref']}:{s['path']}" + ("  (website repository)" if s["repo"] else ""))
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(lines)} entries -> {target.relative_to(P.ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
