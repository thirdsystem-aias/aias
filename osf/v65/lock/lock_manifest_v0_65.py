#!/usr/bin/env python3
"""AIAS v0.65: write the lock manifest, the SHA-256 of every file the pre-registration locks. No model is called.

  python3 osf/v65/lock/lock_manifest_v0_65.py            -> osf/v65/prereg/LOCK_MANIFEST_v0_65.sha256
  python3 osf/v65/lock/lock_manifest_v0_65.py --check    -> exit 1 if the manifest on disk differs from a rebuild, the
                                                            final text is not a byte copy of the r0 draft, or a file
                                                            read from v0.62's lock differs from its blob at tag
                                                            v0.62-prereg-r1
Adapted from osf/v62/lock/lock_manifest_v0_62.py. Format `<sha256>  <path relative to the repository root>` (checkable
with `shasum -a 256 -c`), as v0.42, v0.45 and v0.62; the lines are written by score_v0_65.write_manifest (imported
unchanged), so `score_v0_65.py --verify-lock` reads the same file.
File list (as v0.62's: the final pre-registration and every other file of prereg/ except the manifest itself, the
DEVIATIONS file, the study's own documents and scripts, and the earlier-phase files it reads): the final text
osf/v65/prereg/PRE_REGISTRATION_v0_65.md (byte copy of PRE_REGISTRATION_v0_65_DRAFT_r0.md, section 11); the
pre-registered list score_v0_65.MANIFEST_FILES (the 14 files of the draft manifest: the r0 draft, anchor/DEVIATIONS.md,
README.md, the scorer and its tests, the dry-run and power records, and the seven files read from v0.62's lock and
t1, which must be the same git blobs as at tag v0.62-prereg-r1, v0.65's base); and the draft manifest
prereg/LOCK_MANIFEST_v0_65_DRAFT_r0.sha256.
Not listed: __pycache__, osf/v65/outputs/ (written by the single --run), osf/v65/anchor/osf_anchor_v0_65.json (written
after the lock), this lock/ directory.
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("AIAS_ROOT", str(Path(__file__).resolve().parents[3])))
sys.path.insert(0, str(ROOT / "osf/v65/scripts"))
import score_v0_65 as S  # noqa: E402  (the locked scorer, imported unchanged)

MANIFEST = ROOT / "osf/v65/prereg/LOCK_MANIFEST_v0_65.sha256"
FINAL = "osf/v65/prereg/PRE_REGISTRATION_v0_65.md"
DRAFT = "osf/v65/prereg/PRE_REGISTRATION_v0_65_DRAFT_r0.md"
DRAFT_MANIFEST = "osf/v65/prereg/LOCK_MANIFEST_v0_65_DRAFT_r0.sha256"
DEP_TAG = "v0.62-prereg-r1"
DEPENDENCIES = [p for p in S.MANIFEST_FILES if not p.startswith("osf/v65/")]


def files():
    return [FINAL] + list(S.MANIFEST_FILES) + [DRAFT_MANIFEST]


def problems():
    bad = []
    if (ROOT / FINAL).read_bytes() != (ROOT / DRAFT).read_bytes():
        bad.append(f"{FINAL} is not a byte copy of {DRAFT}")
    if MANIFEST.relative_to(ROOT) != S.MANIFEST.relative_to(S.ROOT):
        bad.append(f"manifest path {MANIFEST} differs from score_v0_65.MANIFEST {S.MANIFEST}")
    for p in DEPENDENCIES:
        at_tag = subprocess.run(["git", "-C", str(ROOT), "rev-parse", f"{DEP_TAG}:{p}"], capture_output=True, text=True).stdout.strip()
        here = subprocess.run(["git", "-C", str(ROOT), "hash-object", p], capture_output=True, text=True).stdout.strip()
        if not at_tag or at_tag != here:
            bad.append(f"{p}: blob here {here or '?'} vs at {DEP_TAG} {at_tag or '?'}")
    return bad


def build():
    return "".join(f"{S._sha(ROOT / p)}  {p}\n" for p in files())


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    bad = problems()
    for b in bad:
        print("DIFFERS: " + b)
    text = build()
    if "--check" in argv:
        same = MANIFEST.exists() and MANIFEST.read_text(encoding="utf-8") == text
        print(("manifest up to date: " if same else "manifest DIFFERS from a rebuild: ") + str(MANIFEST.relative_to(ROOT)))
        return 0 if same and not bad else 1
    if bad:
        return 1
    lines = S.write_manifest(MANIFEST, files(), root=ROOT)
    if MANIFEST.read_text(encoding="utf-8") != text:
        print("written manifest differs from build(): stop")
        return 1
    print(f"{len(lines)} files -> {MANIFEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
