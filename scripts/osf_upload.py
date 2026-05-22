#!/usr/bin/env python3
"""osf_upload.py — Recursive upload to OSF project ec6wh.

Direct calls to the WaterButler file API. No osfclient dependency.

v0.12-patched: adds retry-with-backoff (3 attempts: 5s, 15s, 45s) on
ReadTimeout/ConnectionError, bumps timeouts to 180s for folder ops and
600s for file uploads, and caches folder listings so that uploading 20
files into one folder makes 1 list_contents call instead of 20.

Setup (one-time):
    1. Create OSF token at https://osf.io/settings/tokens with scope osf.full_write
    2. Export it:  export OSF_TOKEN='<token>'
    3. Install requests:  pip install requests

Usage:
    # Dry run (shows what would be uploaded, makes no changes)
    python osf_upload.py ~/aias/osf/v12 v12 --dry-run

    # Actual upload
    python osf_upload.py ~/aias/osf/v12 v12

The script recursively walks the local directory and replicates the structure
on OSF. Existing files are overwritten (PUT to the existing wb path).
Hidden files (.DS_Store, etc.) and __pycache__ folders are skipped.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path
from urllib.parse import quote

import requests

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

PROJECT_ID = "ec6wh"
WB_BASE = f"https://files.osf.io/v1/resources/{PROJECT_ID}/providers/osfstorage"
API_BASE = f"https://api.osf.io/v2/nodes/{PROJECT_ID}"

SKIP_NAMES = {".DS_Store", ".git", ".gitignore", "__pycache__",
              "node_modules", ".ipynb_checkpoints"}

# Timeouts (seconds)
TIMEOUT_AUTH = 30
TIMEOUT_FOLDER = 180   # GET (list_contents), PUT (create folder)
TIMEOUT_FILE_UPLOAD = 600  # PUT (file content)

# Retry policy on transient network errors
MAX_ATTEMPTS = 3
BACKOFFS = [5, 15, 45]  # seconds between attempts 1→2, 2→3, 3→4

DRY_RUN = False

# Cache: wb_path -> {name: {kind, path}}. Populated by list_contents.
# Invalidated by _invalidate_cache when a folder's contents change.
_folder_cache: dict[str, dict] = {}


# ----------------------------------------------------------------------------
# Auth
# ----------------------------------------------------------------------------

def headers() -> dict:
    token = os.environ.get("OSF_TOKEN")
    if not token:
        sys.exit(
            "Error: OSF_TOKEN environment variable is not set.\n"
            "  1. Create a token at https://osf.io/settings/tokens (scope: osf.full_write)\n"
            "  2. export OSF_TOKEN='<token>'\n"
            "  3. Re-run this script."
        )
    return {"Authorization": f"Bearer {token}"}


def verify_auth() -> str:
    """Confirm token works and project is reachable. Returns project title."""
    r = requests.get(API_BASE + "/", headers=headers(), timeout=TIMEOUT_AUTH)
    if r.status_code == 401:
        sys.exit("Auth failed (401). The OSF_TOKEN value is invalid or expired.")
    if r.status_code == 403:
        sys.exit(
            f"Auth failed (403). The token owner does not have write access to "
            f"project {PROJECT_ID}. Verify the token was created from the account "
            f"that owns or has write rights to the project."
        )
    if r.status_code == 404:
        sys.exit(f"Project {PROJECT_ID} not found (404). Check PROJECT_ID in script.")
    r.raise_for_status()
    return r.json()["data"]["attributes"]["title"]


# ----------------------------------------------------------------------------
# Retry helper (folder ops only — file uploads handle their own retry due to
# the data=f stream needing re-open per attempt)
# ----------------------------------------------------------------------------

TRANSIENT_ERRORS = (
    requests.exceptions.ReadTimeout,
    requests.exceptions.ConnectionError,
    requests.exceptions.ChunkedEncodingError,
)


def _request_with_retry(method: str, url: str, timeout: int,
                         label: str = "", **kwargs) -> requests.Response:
    """Wrap requests.request with bounded retry-on-transient-network-error."""
    last_err = None
    for attempt in range(MAX_ATTEMPTS):
        try:
            return requests.request(method, url, timeout=timeout,
                                    headers=headers(), **kwargs)
        except TRANSIENT_ERRORS as e:
            last_err = e
            if attempt == MAX_ATTEMPTS - 1:
                raise
            wait = BACKOFFS[attempt]
            prefix = f"    [retry"
            if label:
                prefix += f" {label}"
            prefix += "]"
            print(f"{prefix} {type(e).__name__}; waiting {wait}s "
                  f"before attempt {attempt + 2}/{MAX_ATTEMPTS}", flush=True)
            time.sleep(wait)
    # unreachable, but mypy-friendly
    raise last_err  # type: ignore


def _invalidate_cache(wb_path: str) -> None:
    _folder_cache.pop(wb_path, None)


# ----------------------------------------------------------------------------
# WaterButler operations
# ----------------------------------------------------------------------------

def list_contents(wb_path: str = "/") -> dict:
    """List contents of an OSF folder. Returns {name: {kind, path}}.

    Cached per wb_path for the duration of the script run. Cache is
    invalidated by create_or_find_folder and upload_file when the folder
    is modified.
    """
    if wb_path in _folder_cache:
        return _folder_cache[wb_path]

    url = WB_BASE + wb_path
    r = _request_with_retry("GET", url, TIMEOUT_FOLDER, label=f"list {wb_path}")
    if r.status_code == 404:
        contents: dict = {}
    else:
        r.raise_for_status()
        items = r.json().get("data", [])
        contents = {
            item["attributes"]["name"]: {
                "kind": item["attributes"]["kind"],
                "path": item["attributes"]["path"],
            }
            for item in items
        }
    _folder_cache[wb_path] = contents
    return contents


def create_or_find_folder(name: str, parent_wb_path: str = "/") -> str:
    """Create folder at parent_wb_path. If exists, return existing wb_path."""
    existing = list_contents(parent_wb_path)
    if name in existing and existing[name]["kind"] == "folder":
        return existing[name]["path"]

    if DRY_RUN:
        return f"{parent_wb_path}{name}-DRYRUN/"

    url = WB_BASE + parent_wb_path + f"?kind=folder&name={quote(name)}"
    r = _request_with_retry("PUT", url, TIMEOUT_FOLDER, label=f"mkdir {name}")
    if r.status_code == 409:
        # Race or quirk — invalidate cache and re-fetch
        _invalidate_cache(parent_wb_path)
        existing = list_contents(parent_wb_path)
        if name in existing:
            return existing[name]["path"]
    if not r.ok:
        sys.exit(f"Failed to create folder {name}: {r.status_code} {r.text[:200]}")

    new_path = r.json()["data"]["attributes"]["path"]
    _invalidate_cache(parent_wb_path)  # parent now contains a new folder
    return new_path


def upload_file(local: Path, parent_wb_path: str) -> None:
    """Upload local file to parent_wb_path. Overwrites if exists.

    File upload retry is handled inline rather than via _request_with_retry,
    because data=f exhausts the stream on attempt 1 and must be re-opened
    per attempt.
    """
    name = local.name
    existing = list_contents(parent_wb_path)

    if name in existing and existing[name]["kind"] == "file":
        url = WB_BASE + existing[name]["path"]
        action = "updated"
    else:
        url = WB_BASE + parent_wb_path + f"?kind=file&name={quote(name)}"
        action = "uploaded"

    size_kb = local.stat().st_size / 1024
    if DRY_RUN:
        print(f"  [dry-run] would {action[:6]} {name} ({size_kb:.1f} KB)")
        return

    last_err = None
    r = None
    for attempt in range(MAX_ATTEMPTS):
        try:
            with local.open("rb") as f:
                r = requests.put(url, data=f, headers=headers(),
                                 timeout=TIMEOUT_FILE_UPLOAD)
            break
        except TRANSIENT_ERRORS as e:
            last_err = e
            if attempt == MAX_ATTEMPTS - 1:
                print(f"  FAILED: {name}: {type(e).__name__} after "
                      f"{MAX_ATTEMPTS} attempts")
                sys.exit(1)
            wait = BACKOFFS[attempt]
            print(f"    [retry upload {name}] {type(e).__name__}; "
                  f"waiting {wait}s before attempt {attempt + 2}/{MAX_ATTEMPTS}",
                  flush=True)
            time.sleep(wait)

    if r is None:
        sys.exit(f"upload_file: unexpected None response for {name}")

    if r.ok:
        print(f"  {action}: {name} ({size_kb:.1f} KB)", flush=True)
        # Parent folder's contents changed (new or updated file); invalidate cache
        _invalidate_cache(parent_wb_path)
    else:
        print(f"  FAILED: {name}: {r.status_code} {r.text[:200]}")
        sys.exit(1)


def upload_tree(local_dir: Path, remote_wb_path: str, depth: int = 0) -> None:
    """Recursively upload local_dir to remote_wb_path."""
    indent = "  " * depth
    for item in sorted(local_dir.iterdir()):
        if item.name in SKIP_NAMES or item.name.startswith("."):
            continue
        if item.is_file():
            upload_file(item, remote_wb_path)
        elif item.is_dir():
            print(f"{indent}-> {item.name}/")
            sub_path = create_or_find_folder(item.name, remote_wb_path)
            upload_tree(item, sub_path, depth + 1)


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main() -> None:
    global DRY_RUN
    ap = argparse.ArgumentParser(
        description="Upload a local directory to OSF project ec6wh.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("local_dir", type=Path,
                    help="Local directory to upload (e.g. ~/aias/osf/v12)")
    ap.add_argument("remote_folder",
                    help="Top-level OSF folder name (e.g. v12)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Show what would be uploaded, no changes made")
    args = ap.parse_args()

    DRY_RUN = args.dry_run

    if not args.local_dir.is_dir():
        sys.exit(f"Not a directory: {args.local_dir}")

    print(f"OSF project: {PROJECT_ID}")
    print(f"Verifying auth... ", end="", flush=True)
    title = verify_auth()
    print(f"OK ('{title}')")
    print()

    if DRY_RUN:
        print("** DRY RUN — no changes will be made **\n")

    print(f"Top-level folder: /{args.remote_folder}/")
    top_path = create_or_find_folder(args.remote_folder, "/")
    print(f"  wb path: {top_path}")
    print()

    print(f"Uploading {args.local_dir} -> osf:/{args.remote_folder}/")
    print()
    upload_tree(args.local_dir, top_path)
    print()
    print(f"Done. View at: https://osf.io/{PROJECT_ID}/files/osfstorage/")


if __name__ == "__main__":
    main()
