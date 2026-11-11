#!/usr/bin/env python3
"""Read-only OSF listing (GET only) of the program node, to check that a study folder name is free.

Usage: python3 osf/methodology/v1_15/lock/osf_list_v1_15.py [folder/sub ...]
Lists the root of osfstorage on node ec6wh and, for each argument, that folder path (if it exists).
Needs OSF_TOKEN in the environment. Never writes, uploads or deletes anything.
"""
import json
import os
import sys
import urllib.request

NODE = "ec6wh"
ROOT_URL = f"https://api.osf.io/v2/nodes/{NODE}/files/osfstorage/"


def get(url):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {os.environ['OSF_TOKEN']}"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)


def listing(url):
    out = []
    while url:
        d = get(url)
        out += [(x["attributes"]["kind"], x["attributes"]["name"],
                 x.get("relationships", {}).get("files", {}).get("links", {}).get("related", {}).get("href"))
                for x in d["data"]]
        url = d["links"].get("next")
    return out


def main(argv):
    root = listing(ROOT_URL)
    print(f"root ({len(root)}):", ", ".join(sorted(n for _k, n, _h in root)))
    for path in argv:
        items, ok = root, True
        for part in path.strip("/").split("/"):
            hit = [h for k, n, h in items if n == part and k == "folder"]
            if not hit:
                print(f"{path}: not found (stopped at '{part}')")
                ok = False
                break
            items = listing(hit[0])
        if ok:
            print(f"{path} ({len(items)}):", ", ".join(sorted(n for _k, n, _h in items)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
