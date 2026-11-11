#!/usr/bin/env python3
"""Samsung-group string screen of a Paper B sample (2026-11-10, AIAS runner lane 3).
Prints counts and unit ids / matched terms only; never prints answer text."""
import csv, json, re, sys
from collections import Counter

TERMS = {  # display term -> regex (case-insensitive, word-bounded)
    "Samsung": r"samsung", "Harman": r"harman(?!\s*kardon)", "Harman Kardon": r"harman\s*/?\s*kardon",
    "JBL": r"jbl", "AKG": r"akg", "Infinity": r"infinity", "Mark Levinson": r"mark\s+levinson",
    "Revel": r"revel", "Lexicon": r"lexicon", "Arcam": r"arcam", "Roon": r"roon",
    "Sound United": r"sound\s+united", "Masimo": r"masimo", "Denon": r"denon", "Marantz": r"marantz",
    "Bowers & Wilkins": r"bowers\s*(?:&|and)\s*wilkins|b\s*&\s*w", "Polk": r"polk",
    "Definitive Technology": r"definitive\s+technology|definitive\s+tech", "Definitive (bare)": r"definitive",
    "Boston Acoustics": r"boston\s+acoustics", "Classe": r"class[eé]", "HEOS": r"heos",
}
RX = {k: re.compile(r"(?<![A-Za-z0-9])(?:" + v + r")(?![A-Za-z0-9])", re.I) for k, v in TERMS.items()}
# a hit counts as a brand mention only when the case-sensitive form is the brand's (common words:
# infinity, revel, lexicon, definitive, classe). Reported separately for manual decision.
CASE = {"Infinity": r"Infinity", "Revel": r"Revel", "Lexicon": r"Lexicon", "Definitive (bare)": r"Definitive",
        "Classe": r"Class[eé]"}


def screen(rows):
    subj, ment = [], []
    for r in rows:
        b = r["brand_display"]
        sh = [k for k, rx in RX.items() if rx.fullmatch(b.strip()) or rx.search(b)]
        if sh:
            subj.append({"unit_id": r["unit_id"], "brand": b, "category": r["category_label"], "terms": sh})
        hits = {}
        for field in ("text", "question"):
            for k, rx in RX.items():
                for m in rx.finditer(r[field]):
                    tok = m.group(0)
                    if k in CASE and not re.fullmatch(CASE[k], tok.split()[0] if k != "Classe" else tok):
                        continue
                    hits.setdefault(k, Counter())[tok] += 1
        if hits:
            ment.append({"unit_id": r["unit_id"], "brand": b, "category": r["category_label"],
                         "block": r["block"], "hits": {k: dict(v) for k, v in hits.items()}})
    return subj, ment


if __name__ == "__main__":
    csv.field_size_limit(sys.maxsize)
    rows = list(csv.DictReader(open(sys.argv[1], newline="", encoding="utf-8")))
    s, m = screen(rows)
    print(json.dumps({"rows": len(rows), "subject_hits": s, "mention_hits": m}, ensure_ascii=False, indent=1))
