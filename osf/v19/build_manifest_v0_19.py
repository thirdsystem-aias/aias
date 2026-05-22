#!/usr/bin/env python3
"""
build_manifest_v0_19.py — Generate MANIFEST.md for the v0.19 OSF deposit.

Walks osf/v19/, computes SHA-256 for every file (skipping MANIFEST.md itself
and any caches), records git HEAD state at generation time, and writes the
manifest to osf/v19/MANIFEST.md.

Run from project root:
    cd ~/aias
    python3 osf/v19/build_manifest_v0_19.py

Or from osf/v19/:
    cd ~/aias/osf/v19
    python3 build_manifest_v0_19.py

Output is fully reproducible: hashing identical files at the same commit
yields identical MANIFEST.md content. Commit the MANIFEST.md update after
running; the OSF deposit upload (via ~/aias/scripts/osf_upload.py) reads
the same file set.

Skips:
  - MANIFEST.md itself (would self-reference its own hash)
  - build_manifest_v0_19.py itself (script provenance is in git, not the manifest)
  - __pycache__/ and .pyc files
  - .DS_Store and other macOS metadata
  - Hidden files (starting with .)
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PHASE = "v0.19"
PHASE_TAG = "v0.19-prereg-r1"
PHASE_PREREG_COMMIT = "2cbd36c"
PHASE_ACQUIRED_COMMIT = "c56ea8b"
PHASE_REPORT_COMMIT = "cbecd3c"
PHASE_PAPER_COMMIT = "08664e7"

SKIP_NAMES = {
    "MANIFEST.md",
    "build_manifest_v0_19.py",
    ".DS_Store",
    "Thumbs.db",
}
SKIP_DIR_NAMES = {"__pycache__", ".git", ".ipynb_checkpoints"}
SKIP_SUFFIXES = {".pyc", ".pyo", ".swp"}

# ---------------------------------------------------------------------------
# Path resolution — works whether invoked from project root or osf/v19/
# ---------------------------------------------------------------------------

def resolve_deposit_root() -> Path:
    """Locate the osf/v19/ directory regardless of CWD."""
    script_dir = Path(__file__).resolve().parent
    if script_dir.name == "v19" and script_dir.parent.name == "osf":
        return script_dir
    # Invoked from project root, script at osf/v19/build_manifest_v0_19.py
    candidate = Path.cwd() / "osf" / "v19"
    if candidate.exists():
        return candidate
    # Last resort: relative to script
    sys.exit(
        f"ERROR: cannot locate osf/v19/ deposit root. "
        f"Script at {script_dir}, CWD {Path.cwd()}."
    )


# ---------------------------------------------------------------------------
# File enumeration
# ---------------------------------------------------------------------------

def enumerate_deposit_files(root: Path) -> list[Path]:
    """Walk the deposit root, returning sorted paths that should be hashed."""
    files = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            continue
        if path.name in SKIP_NAMES:
            continue
        if path.suffix in SKIP_SUFFIXES:
            continue
        if path.name.startswith("."):
            continue
        files.append(path)
    return files


# ---------------------------------------------------------------------------
# SHA-256
# ---------------------------------------------------------------------------

def sha256_of(path: Path) -> str:
    """Compute SHA-256 hex digest of a file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Git state
# ---------------------------------------------------------------------------

def git_head_state() -> dict:
    """Capture git HEAD commit, branch, and dirty status."""
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        return {
            "commit": commit,
            "short_commit": commit[:7],
            "branch": branch,
            "dirty": bool(status),
            "dirty_files": [line[3:] for line in status.splitlines()] if status else [],
        }
    except (FileNotFoundError, subprocess.CalledProcessError):
        return {"commit": "UNKNOWN", "short_commit": "UNKNOWN", "branch": "UNKNOWN",
                "dirty": False, "dirty_files": []}


# ---------------------------------------------------------------------------
# Manifest emission
# ---------------------------------------------------------------------------

def write_manifest(deposit_root: Path, files: list[Path], git_state: dict) -> Path:
    """Write MANIFEST.md to the deposit root."""
    manifest_path = deposit_root / "MANIFEST.md"
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines = []
    lines.append(f"# MANIFEST — AIAS™ {PHASE} OSF Deposit\n")
    lines.append(f"Generated: {now_iso}  ")
    lines.append(f"Git HEAD at generation: `{git_state['short_commit']}` ({git_state['commit']})  ")
    lines.append(f"Branch: `{git_state['branch']}`  ")
    if git_state["dirty"]:
        lines.append(f"**WARNING:** working tree had uncommitted changes at generation:")
        for f in git_state["dirty_files"]:
            lines.append(f"  - `{f}`")
        lines.append("")
        lines.append("Re-run after committing for a clean manifest.")
    else:
        lines.append(f"Working tree: clean")
    lines.append("")
    lines.append("## Lock state")
    lines.append("")
    lines.append(f"- Pre-registration: tag `{PHASE_TAG}` at commit `{PHASE_PREREG_COMMIT}`")
    lines.append(f"- Acquired (Phase A + Phase B): commit `{PHASE_ACQUIRED_COMMIT}`")
    lines.append(f"- Brand-format report rendered: commit `{PHASE_REPORT_COMMIT}`")
    lines.append(f"- SSRN paper compiled: commit `{PHASE_PAPER_COMMIT}`")
    lines.append("")
    lines.append("## File hashes (SHA-256)")
    lines.append("")
    lines.append("| Path | Size (bytes) | SHA-256 |")
    lines.append("|---|---:|---|")

    total_bytes = 0
    for path in files:
        rel = path.relative_to(deposit_root).as_posix()
        size = path.stat().st_size
        total_bytes += size
        digest = sha256_of(path)
        lines.append(f"| `{rel}` | {size:,} | `{digest}` |")

    lines.append(f"| **TOTAL ({len(files)} files)** | **{total_bytes:,}** | |")
    lines.append("")
    lines.append("## Verification")
    lines.append("")
    lines.append("Regenerate this manifest and diff against the committed version:")
    lines.append("")
    lines.append("```bash")
    lines.append("cd ~/aias")
    lines.append("python3 osf/v19/build_manifest_v0_19.py")
    lines.append("git diff osf/v19/MANIFEST.md")
    lines.append("```")
    lines.append("")
    lines.append("A clean diff confirms file integrity at the recorded commit. ")
    lines.append("If any hash differs from the committed manifest, either the underlying ")
    lines.append("file was modified or the build pipeline produced a non-deterministic ")
    lines.append("output (e.g. PDF metadata embedding a build timestamp); investigate ")
    lines.append("before re-uploading to OSF.")
    lines.append("")
    lines.append("## OSF deposit")
    lines.append("")
    lines.append(f"OSF project: `ec6wh` · path: `osf.io/ec6wh/v19/`")
    lines.append("")
    lines.append("Upload via `~/aias/scripts/osf_upload.py` (WaterButler API; `OSF_TOKEN` env var; ")
    lines.append("`osf.full_write` scope). Web UI drag-and-drop is the fallback path.")

    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return manifest_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    deposit_root = resolve_deposit_root()
    print(f"[build_manifest_v0_19] deposit root: {deposit_root}")

    files = enumerate_deposit_files(deposit_root)
    print(f"[build_manifest_v0_19] files to hash: {len(files)}")

    git_state = git_head_state()
    print(f"[build_manifest_v0_19] git HEAD: {git_state['short_commit']} "
          f"({git_state['branch']}{' — DIRTY' if git_state['dirty'] else ''})")

    manifest_path = write_manifest(deposit_root, files, git_state)
    print(f"[build_manifest_v0_19] ✓ MANIFEST.md written: {manifest_path}")
    print(f"[build_manifest_v0_19] file size: {manifest_path.stat().st_size:,} bytes")

    if git_state["dirty"]:
        print(f"[build_manifest_v0_19] WARNING: working tree was dirty at generation; "
              f"re-run after committing for a clean manifest.")


if __name__ == "__main__":
    main()
