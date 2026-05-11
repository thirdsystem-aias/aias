#!/usr/bin/env python3
"""osf_upload.py — Recursive upload to OSF project ec6wh.

Direct calls to the WaterButler file API. No osfclient dependency.

Setup (one-time):
    1. Create OSF token at https://osf.io/settings/tokens with scope osf.full_write
    2. Export it:  export OSF_TOKEN='<token>'
    3. Install requests:  pip install requests

Usage:
    # Dry run (shows what would be uploaded, makes no changes)
    python osf_upload.py ~/aias/osf/v11 v11 --dry-run

    # Actual upload
    python osf_upload.py ~/aias/osf/v11 v11

    # Different project / deposit folder
    python osf_upload.py ~/aias/osf/v12 v12

The script recursively walks the local directory and replicates the structure
on OSF. Existing files are overwritten (PUT to the existing wb path).
Hidden files (.DS_Store, etc.) and __pycache__ folders are skipped.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from urllib.parse import quote

import requests

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

PROJECT_ID = "ec6wh"
WB_BASE = f"https://files.osf.io/v1/resources/{PROJECT_ID}/providers/osfstorage"
API_BASE = f"https://api.osf.io/v2/nodes/{PROJECT_ID}"

SKIP_NAMES = {".DS_Store", ".git", ".gitignore", "__pycache__", "node_modules", ".ipynb_checkpoints"}

DRY_RUN = False


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
    r = requests.get(API_BASE + "/", headers=headers(), timeout=30)
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
# WaterButler operations
# ----------------------------------------------------------------------------

def list_contents(wb_path: str = "/") -> dict:
    """List contents of an OSF folder. Returns {name: {kind, path}}."""
    url = WB_BASE + wb_path
    r = requests.get(url, headers=headers(), timeout=30)
    if r.status_code == 404:
        return {}
    r.raise_for_status()
    items = r.json().get("data", [])
    return {
        item["attributes"]["name"]: {
            "kind": item["attributes"]["kind"],
            "path": item["attributes"]["path"],
        }
        for item in items
    }


def create_or_find_folder(name: str, parent_wb_path: str = "/") -> str:
    """Create folder at parent_wb_path. If exists, return existing wb_path."""
    existing = list_contents(parent_wb_path)
    if name in existing and existing[name]["kind"] == "folder":
        return existing[name]["path"]

    if DRY_RUN:
        # Simulate a wb_path for dry-run traversal
        return f"{parent_wb_path}{name}-DRYRUN/"

    url = WB_BASE + parent_wb_path + f"?kind=folder&name={quote(name)}"
    r = requests.put(url, headers=headers(), timeout=30)
    if r.status_code == 409:
        # Race or quirk — re-fetch
        existing = list_contents(parent_wb_path)
        if name in existing:
            return existing[name]["path"]
    if not r.ok:
        sys.exit(f"Failed to create folder {name}: {r.status_code} {r.text[:200]}")
    return r.json()["data"]["attributes"]["path"]


def upload_file(local: Path, parent_wb_path: str) -> None:
    """Upload local file to parent_wb_path. Overwrites if exists."""
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

    with local.open("rb") as f:
        r = requests.put(url, data=f, headers=headers(), timeout=300)

    if r.ok:
        print(f"  {action}: {name} ({size_kb:.1f} KB)")
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
                    help="Local directory to upload (e.g. ~/aias/osf/v11)")
    ap.add_argument("remote_folder",
                    help="Top-level OSF folder name (e.g. v11)")
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
