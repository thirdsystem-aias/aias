#!/usr/bin/env python3
"""Step 2 helper: exact comparison of a reproduced output with the published one.

  compare_outputs.py json PUBLISHED REPRODUCED [--key K]   deep equality (floats exact), lists diffs
  compare_outputs.py csv  PUBLISHED REPRODUCED             byte equality, else row-level diffs
Exit 0 iff identical."""
import csv
import json
import sys


def diffs(a, b, path=""):
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b), key=str):
            if k not in a or k not in b:
                out.append((f"{path}/{k}", a.get(k, "<absent>"), b.get(k, "<absent>")))
            else:
                out += diffs(a[k], b[k], f"{path}/{k}")
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            out += diffs(x, y, f"{path}[{i}]")
    elif a != b or type(a) is not type(b) and not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
        out.append((path, a, b))
    return out


def main():
    kind, p, r = sys.argv[1:4]
    key = sys.argv[sys.argv.index("--key") + 1] if "--key" in sys.argv else None
    if kind == "json":
        a, b = json.load(open(p)), json.load(open(r))
        if key:
            a, b = a[key], b[key]
        d = diffs(a, b)
        print(f"{'IDENTICAL' if not d else 'DIFFERENT'} ({len(d)} differing leaves){' key=' + key if key else ''}")
        for x in d[:40]:
            print("  ", x[0], "| published:", str(x[1])[:120], "| reproduced:", str(x[2])[:120])
        return 0 if not d else 1
    pa, pb = open(p, "rb").read(), open(r, "rb").read()
    if pa == pb:
        print("IDENTICAL (byte-equal)")
        return 0
    ra, rb = list(csv.DictReader(open(p, newline=""))), list(csv.DictReader(open(r, newline="")))
    n = sum(1 for x, y in zip(ra, rb) if x != y) + abs(len(ra) - len(rb))
    print(f"DIFFERENT: {len(ra)} vs {len(rb)} rows, {n} differing")
    return 1


if __name__ == "__main__":
    sys.exit(main())
