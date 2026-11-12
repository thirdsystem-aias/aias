#!/usr/bin/env python3
"""AIAS v0.62: write the lock manifest, the SHA-256 of every file the pre-registration locks. No model is called.

  python3 osf/v62/lock/lock_manifest_v0_62.py            -> osf/v62/prereg/LOCK_MANIFEST_v0_62.sha256
  python3 osf/v62/lock/lock_manifest_v0_62.py --check    -> exit 1 if the manifest on disk differs from a rebuild, or a
                                                            dependency differs from its blob at tag v0.42-prereg-r1
Format `<sha256>  <path relative to the repository root>` (checkable with `shasum -a 256 -c`), as v0.42, v0.44, v0.45.
File list = pre-registration section 11, "r3 update" item 6: DEVIATIONS.md; PLAIN_SUMMARY_*.md; every file of
osf/v62/prereg/ except the manifest itself (incl. the final PRE_REGISTRATION_v0_62.md); osf/v62/inputs/;
osf/v62/translations/; every osf/v62/scripts/*.py, _acquire_tail_v0_62.py.txt and osf/v62/scripts/tests/*.py; and the
earlier-phase files v0.62 reads or imports unchanged (DEPENDENCIES; same git blobs as at tag v0.42-prereg-r1).
Not listed: __pycache__, osf/v62/data/ and osf/v62/anchor/ (written at and after the lock), this lock/ directory.
"""
import hashlib
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("AIAS_ROOT", str(Path(__file__).resolve().parents[3])))
V62 = ROOT / "osf/v62"
MANIFEST = V62 / "prereg/LOCK_MANIFEST_v0_62.sha256"
DEP_TAG = "v0.42-prereg-r1"
DEPENDENCIES = [
    "scripts/score_v20.py", "scripts/score_v21.py", "scripts/score_v22.py", "scripts/score_v0_23.py",
    "scripts/run_acquisition_v20.py", "scripts/run_acquisition_v21.py", "scripts/run_acquisition_v22.py",
    "osf/v19/acquire_v0_19.py",
]


def _walk(d, pattern="*"):
    return sorted(p for p in d.glob(pattern) if p.is_file() and not p.name.startswith("."))


def files():
    out = [V62 / "DEVIATIONS.md"] + _walk(V62, "PLAIN_SUMMARY_*.md")
    out += [p for p in _walk(V62 / "prereg") if p != MANIFEST]
    out += _walk(V62 / "inputs") + _walk(V62 / "translations")
    out += _walk(V62 / "scripts", "*.py") + _walk(V62 / "scripts", "*.py.txt") + _walk(V62 / "scripts/tests", "*.py")
    return [p.relative_to(ROOT).as_posix() for p in out] + DEPENDENCIES


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def build():
    return "".join(f"{sha(p)}  {p}\n" for p in files())


def dependency_problems():
    bad = []
    for p in DEPENDENCIES:
        at_tag = subprocess.run(["git", "-C", str(ROOT), "rev-parse", f"{DEP_TAG}:{p}"], capture_output=True, text=True).stdout.strip()
        here = subprocess.run(["git", "-C", str(ROOT), "hash-object", p], capture_output=True, text=True).stdout.strip()
        if not at_tag or at_tag != here:
            bad.append(f"{p}: blob here {here or '?'} vs at {DEP_TAG} {at_tag or '?'}")
    return bad


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    bad = dependency_problems()
    for b in bad:
        print("DEPENDENCY DIFFERS: " + b)
    text = build()
    if "--check" in argv:
        same = MANIFEST.exists() and MANIFEST.read_text(encoding="utf-8") == text
        print(("manifest up to date: " if same else "manifest DIFFERS from a rebuild: ") + str(MANIFEST.relative_to(ROOT)))
        return 0 if same and not bad else 1
    if bad:
        return 1
    MANIFEST.write_text(text, encoding="utf-8")
    print(f"{text.count(chr(10))} files -> {MANIFEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
