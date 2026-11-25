#!/usr/bin/env python3
"""coi_screen_v0_46_r1.py -- AIAS v0.46 (#76): DEVIATIONS Entry 0 r1, item (a). No model is called; no network.

Re-runs v0.62's registry string screen (osf/v62/scripts/coi_screen_v0_62.py, r3 term list: 70 terms, 30 r0 + 40 r3;
read from branch v0.62, commit f09068f, git blob b128979f61ae275042c62c46da9fdaa42f91c542) on the 90 live units of
#76: build_probes_v0_46.live_units() with Fisker in Cell D (D7 record of 2026-11-24; manuscript r4, commit 3c98818),
cross-checked against the LIST orders of the probe file osf/v46/prereg/probes_v0_46.jsonl. v0.62's own TERMS,
TERMS_R3 and screen() are imported unchanged (whole-word, case-sensitive match on names only; method limits as v0.62
DEVIATIONS Entry 0). v0.62's screen reads only registry names (its alias table); it has no OTHER-coding list, and
none is screened here (no OTHER text exists before collection).

Run: python3 osf/v46/scripts/coi_screen_v0_46_r1.py [--v62 PATH_TO_v0.62_WORKTREE]
  -> osf/v46/data/coi_screen_v0_46_r1.txt and .sha256
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
V46 = HERE.parent
sys.path.insert(0, str(HERE))
import build_probes_v0_46 as B  # noqa: E402

V62_BLOB = "b128979f61ae275042c62c46da9fdaa42f91c542"
V62_COMMIT = "f09068f"
V62_DEFAULT = Path.home() / "aias/_worktrees/v0.62"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--v62", default=str(V62_DEFAULT))
    a = ap.parse_args(argv)
    scr = Path(a.v62) / "osf/v62/scripts/coi_screen_v0_62.py"
    blob = subprocess.run(["git", "hash-object", str(scr)], capture_output=True, text=True, check=True).stdout.strip()
    if blob != V62_BLOB:
        sys.exit(f"[v46] coi screen: {scr} has git blob {blob}, expected {V62_BLOB}; halt")
    sha = hashlib.sha256(scr.read_bytes()).hexdigest()
    sys.path.insert(0, str(scr.parent))
    import coi_screen_v0_62 as S  # noqa: E402

    live = B.live_units()
    rows = [json.loads(l) for l in open(V46 / "prereg/probes_v0_46.jsonl", encoding="utf-8")]
    shown = {}
    for r in rows:
        if r.get("condition") == "LIST":
            shown.setdefault(r["category"], set()).update(r["order"])
    for cat, units in live.items():
        if set(units) != shown.get(cat, set()):
            sys.exit(f"[v46] coi screen: live units of {cat} differ from the probe file's LIST orders; halt")
    names = [(B.CAT_SUB[c], u) for c, us in live.items() for u in us]
    if len(names) != 90 or "Fisker" in {u for _, u in names}:
        sys.exit(f"[v46] coi screen: {len(names)} live units (expected 90, Fisker in Cell D); halt")
    terms = S.TERMS + S.TERMS_R3
    hits = S.screen(names, terms)
    lines = ["v0.46 (#76) DEVIATIONS Entry 0 r1 (a): v0.62 registry string screen re-run on the live units",
             "screen: %s (v0.62 commit %s; git blob %s; SHA-256 %s)" % (
                 "osf/v62/scripts/coi_screen_v0_62.py", V62_COMMIT, blob, sha),
             "units: %d live units (%s); Fisker in Cell D (D7 record 2026-11-24); checked against probes_v0_46.jsonl"
             % (len(names), ", ".join("%s %d" % (c, len(us)) for c, us in live.items())),
             "terms: %d (%d r0 + %d r3)" % (len(terms), len(S.TERMS), len(S.TERMS_R3)),
             "terms r0: " + "; ".join(S.TERMS), "terms r3: " + "; ".join(S.TERMS_R3),
             "matches: %d" % len(hits)]
    lines += ["  %s %s (term: %s)" % h for h in hits]
    lines += ["units screened: " + "; ".join("%s %s" % n for n in names)]
    out = V46 / "data/coi_screen_v0_46_r1.txt"
    body = ("\n".join(lines) + "\n").encode("utf-8")
    out.write_bytes(body)
    (V46 / "data/coi_screen_v0_46_r1.sha256").write_text("%s  %s\n" % (hashlib.sha256(body).hexdigest(), out.name))
    print("\n".join(lines[:4] + lines[6:7 + len(hits)]))
    print("sha256", hashlib.sha256(body).hexdigest())


if __name__ == "__main__":
    main()
