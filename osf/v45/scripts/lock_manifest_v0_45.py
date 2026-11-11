#!/usr/bin/env python3
"""AIAS v0.45 (t5): write the lock manifest, the SHA-256 of every file the pre-registration locks. No model is called.

  python3 osf/v45/scripts/lock_manifest_v0_45.py            -> osf/v45/prereg/LOCK_MANIFEST_v0_45.sha256
  python3 osf/v45/scripts/lock_manifest_v0_45.py --check    -> exit 1 if the manifest on disk differs from a rebuild
Format: `<sha256>  <path relative to the repository root>` (checkable with `shasum -a 256 -c`), as v0.42 and v0.44.
Listed (pre-registration section 9): DEVIATIONS.md; every file in osf/v45/prereg/ except the manifest itself; the
v0.45 scripts and tests; and the files of earlier phases they import or read (DEPENDENCIES; unchanged files, at the
versions of t4's locked code, tag v0.42-prereg-r1). Not listed: data (osf/v45/data/, written after the lock), the lock
helpers in osf/v45/lock/ (they write and check the anchor; v0.42 and v0.44 did not lock theirs), __pycache__.
"""
import hashlib
import os
import sys
from pathlib import Path

ROOT = Path(os.environ.get("AIAS_ROOT", str(Path(__file__).resolve().parents[3])))
V45 = ROOT / "osf/v45"
MANIFEST = V45 / "prereg/LOCK_MANIFEST_v0_45.sha256"
DEPENDENCIES = [   # imported or read by the v0.45 scripts and tests (files of earlier phases, unchanged)
    "osf/v42/scripts/acquire_v0_42.py",        # fork source of acquire_v0_45.py (= its version at v0.42-prereg-r1)
    "osf/v42/scripts/budget_v0_42.py",         # imported by score_v0_42; budget_v0_45's functions equal it (C28)
    "osf/v42/scripts/code_t4_v0_42.py",        # the certified coder, git blob 2d36735d... (section 5.1)
    "osf/v42/scripts/score_v0_42.py",          # scoring functions imported by score_v0_45
    "osf/v42/prereg/probes_v0_42.jsonl",       # t4's probe file (MC_Probe_Parity, G1)
    "osf/v41/scripts/score_v41.py",            # imported by score_v0_42
    "osf/v41/v41_three_wave_table.csv",        # read by score_v0_42
    "osf/v41/data/v23/v23_phase_a_scored.json",  # t3 v0.23 answers with their locked Sonnet 4.5 codes (J1)
    "scripts/score_v0_23.py",                  # v0.23 judge prompt, template, truncation, R0-R3 parser (section 5.1)
    "scripts/score_v0_31.py",                  # imported by the coder (mention counting)
    "osf/v39/data/v39_raw.json",               # token basis of r0's estimate (cost_estimate_v0_45.py)
]


def files():
    out = [V45 / "anchor/DEVIATIONS.md"]
    out += sorted(p for p in (V45 / "prereg").glob("*") if p.is_file() and p != MANIFEST and not p.name.startswith("."))
    for sub in ("scripts", "scripts/tests"):
        out += sorted(p for p in (V45 / sub).glob("*.py") if p.is_file())
    return [p.relative_to(ROOT).as_posix() for p in out] + DEPENDENCIES


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def build():
    return "".join(f"{sha(p)}  {p}\n" for p in files())


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    text = build()
    if "--check" in argv:
        same = MANIFEST.exists() and MANIFEST.read_text(encoding="utf-8") == text
        print(("manifest up to date: " if same else "manifest DIFFERS from a rebuild: ") + str(MANIFEST.relative_to(ROOT)))
        return 0 if same else 1
    MANIFEST.write_text(text, encoding="utf-8")
    print(f"{text.count(chr(10))} files -> {MANIFEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
