#!/usr/bin/env python3
"""v1.15 COI string screen of the five omnibus registries that t4 (v0.42) codes, with the term list of
v1.11 DEVIATIONS Entry 0 (unchanged). Reads the registries with v1.10's locked loader (score_v1_10.load_registry),
canonical names and aliases, accent-folded, case-insensitive, word-bounded. No model call; no answer text read.

Usage: python3 osf/methodology/v1_15/scripts/coi_screen_v1_15.py [--out prereg/coi_screen_v1_15.json]
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import score_v1_10 as V  # noqa: E402

TERMS = ["Samsung", "Harman", "JBL", "AKG", "Harman Kardon", "Infinity", "Mark Levinson", "Revel", "Lexicon",
         "Arcam", "Roon", "Sound United", "Masimo", "Denon", "Marantz", "Bowers & Wilkins", "B&W", "Polk",
         "Definitive Technology", "Classé", "Boston Acoustics", "HEOS"]   # v1.11 DEVIATIONS Entry 0


def fold(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)).lower()


def screen(registries):
    pats = {t: re.compile(r"(?<![a-z0-9])" + re.escape(fold(t)) + r"(?![a-z0-9])") for t in TERMS}
    hits, n = [], {}
    for sub, reg in registries.items():
        n[sub] = len(reg)
        for canon, aliases in reg.items():
            for name in [canon, *aliases]:
                for t, p in pats.items():
                    if p.search(fold(name)):
                        hits.append({"substrate": sub, "brand": canon, "matched_name": name, "term": t})
    return {"terms": TERMS, "brands_per_substrate": n, "brands_total": sum(n.values()), "matches": hits}


def main(argv):
    ctx = type("Ctx", (), {"path": staticmethod(lambda rel: ROOT / rel)})()
    regs = {sub: V.load_registry(ctx, rel, fmt)[0] for sub, (rel, fmt) in V.OMNI_REG.items()}
    res = screen(regs)
    print(json.dumps({k: v for k, v in res.items() if k != "terms"}, indent=1))
    if "--out" in argv:
        Path(argv[argv.index("--out") + 1]).write_text(json.dumps(res, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
