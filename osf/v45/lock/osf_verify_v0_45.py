#!/usr/bin/env python3
"""Verify an OSF deposit against local files by SHA-256 (read-only; osf/v45/LOCK_STEPS.md step 7).
Copied unchanged in code from osf/v42/lock/osf_verify_v0_42.py (v0.42 @ 58d1891), which added --ignore and --list to v1.12's.

Usage: python3 osf_verify_v0_45.py LOCAL_DIR OSF_PATH [--ignore PREFIX]   e.g. osf/v45/prereg v45/prereg --ignore scripts/
       python3 osf_verify_v0_45.py --list OSF_PATH                          (list what OSF holds there, read-only)
Lists OSF project ec6wh (osfstorage) at OSF_PATH through the v2 API (OSF_TOKEN), compares every local file (hidden
files and __pycache__ skipped, as scripts/osf_upload.py) with the stored sha256, and reports files missing on either
side. OSF files whose path under OSF_PATH starts with an --ignore prefix (e.g. the scripts deposited at
v45/prereg/scripts/) are listed but not counted. Exit 0 only if every local file is on OSF with the same SHA-256 and
OSF holds no other (non-ignored) file there.
"""
import hashlib
import os
import sys
from pathlib import Path

import requests

NODE = "ec6wh"
ROOT_URL = f"https://api.osf.io/v2/nodes/{NODE}/files/osfstorage/"
SKIP = {".DS_Store", ".git", ".gitignore", "__pycache__", "node_modules", ".ipynb_checkpoints"}
H = {"Authorization": "Bearer " + os.environ.get("OSF_TOKEN", "")}


def get_all(url):
    out = []
    while url:
        r = requests.get(url, headers=H, timeout=120)
        r.raise_for_status()
        j = r.json()
        out += j["data"]
        url = (j.get("links") or {}).get("next")
    return out


def find_folder(path):
    url = ROOT_URL
    for part in [p for p in path.split("/") if p]:
        hit = [e for e in get_all(url) if e["attributes"]["kind"] == "folder" and e["attributes"]["name"] == part]
        if not hit:
            sys.exit(f"OSF folder not found: {path} (missing '{part}')")
        url = hit[0]["relationships"]["files"]["links"]["related"]["href"]
    return url


def walk(url, prefix, out):
    for e in get_all(url):
        a = e["attributes"]
        if a["kind"] == "folder":
            walk(e["relationships"]["files"]["links"]["related"]["href"], prefix + a["name"] + "/", out)
        else:
            out[prefix + a["name"]] = ((a.get("extra") or {}).get("hashes") or {}).get("sha256")
    return out


def local_files(d):
    out = {}
    for p in sorted(Path(d).rglob("*")):
        rel = p.relative_to(d)
        if p.is_file() and not any(part in SKIP or part.startswith(".") for part in rel.parts):
            out[rel.as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def main():
    args, ignore = [], []
    it = iter(sys.argv[1:])
    for x in it:
        if x == "--ignore":
            ignore.append(next(it))
        else:
            args.append(x)
    if not os.environ.get("OSF_TOKEN"):
        sys.exit("OSF_TOKEN is not set")
    if len(args) == 2 and args[0] == "--list":
        for name, h in sorted(walk(find_folder(args[1]), "", {}).items()):
            print(f"{(h or 'no-sha256')[:16]}  {name}")
        return 0
    if len(args) != 2:
        sys.exit(__doc__)
    loc = local_files(args[0])
    remote = walk(find_folder(args[1]), "", {})
    skipped = sorted(n for n in remote if any(n.startswith(p) for p in ignore))
    for n in skipped:
        print(f"IGNORED (prefix): {n}")
        remote.pop(n)
    bad = 0
    for name, h in loc.items():
        r = remote.get(name)
        ok = r == h
        bad += not ok
        print(("OK   " if ok else "BAD  ") + f"{name}  local {h[:16]}  osf {(r or 'MISSING')[:16]}")
    for name in sorted(set(remote) - set(loc)):
        bad += 1
        print(f"EXTRA on OSF only: {name}")
    print(f"{len(loc) - sum(1 for n in loc if remote.get(n) != loc[n])} of {len(loc)} local files match; "
          f"{len(set(remote) - set(loc))} extra on OSF -> {'PASS' if not bad else 'FAIL'}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
