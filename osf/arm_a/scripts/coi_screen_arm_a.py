#!/usr/bin/env python3
"""Arm A: conflict-of-interest screens for DEVIATIONS Entry 0, Part E (airlines, retail banks, B2B software). No model
is called and no web source is read.

  python3 osf/arm_a/scripts/coi_screen_arm_a.py   -> osf/arm_a/prereg/coi_screen_arm_a.txt

(1) String screen: every brand name of the 76-domain registry, every v0.40 holder name of the 26 banks and 11 airlines
    (frozen registry 2026-11-12) and every domain, whole-word and case-sensitive, against the 70 Samsung-group terms of
    the v0.62 r3 screen (TERMS + TERMS_R3, copied verbatim from coi_screen_v0_62.py at tag v0.62-prereg-r1; Iris is
    matched only as a whole word). Method limit (as v0.62 Part A): a name check, not an ownership filing per brand.
(2) Record screen: every DEVIATIONS file in the repository's worktrees (deduplicated by content) is searched for lines
    that name both an airline, bank or software brand of the sample and a Samsung-group term: a tie already on the
    programme's record. Method limit (as v0.40 Entry 0): it compares the sample with the programme's record of ties; it
    is not a new search of agency work, supply or partnerships for each brand.
"""
import csv
import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import params_arm_a as P   # noqa: E402

TERMS = ['Samsung', 'Harman', 'Harman Kardon', 'JBL', 'AKG', 'Infinity', 'Mark Levinson', 'Revel', 'Arcam', 'Lexicon',
         'Roon', 'Sound United', 'Masimo', 'Denon', 'Marantz', 'Bowers & Wilkins', 'B&W', 'Polk', 'Definitive Technology',
         'Boston Acoustics', 'Classé', 'HEOS', 'Cheil', 'Shilla', 'Bioepis', 'Samsung C&T', 'Ami', 'Maison Kitsuné',
         'Lemaire', 'Thom Browne']
TERMS_R3 = ['Samsung Electronics', 'Samsung SDI', 'Samsung Display', 'Samsung Electro-Mechanics', 'Samsung Biologics',
            'Samsung SDS', 'Samsung Life', 'Hotel Shilla', 'DFASS', 'Iris', 'McKinney', 'Barbarian', 'BMB', 'Pengtai',
            'Founded', 'LABEL C', 'Label C', 'BEAKER', '10 Corso Como', 'Ellis Brooklyn', 'Bamford', 'Maison Louis Marie',
            'J.Hannah', 'Absolution', 'Le Fournier', 'Sundays', 'Christophe Robin', 'Astier de Villatte', 'Margaret Howell',
            'Fitflop', 'Sandro', 'Maje', 'Claudie Pierlot', 'Fursac', 'Ganni', 'Studio Nicholson', 'Beanpole', '8Seconds',
            'Kuho', 'Galaxy']
RECORD_TERMS = ['Samsung', 'Harman', 'Cheil', 'Iris', 'McKinney', 'Barbarian', 'Shilla']
PART_E = ("airlines", "banks", "software")
V40_REG = P.ROOT.parent / "v0.40-paper-r2/osf/v40/registries/out"


def screen(names, terms):
    hits = []
    for label, name in names:
        for t in terms:
            if re.search(r'(?<![A-Za-z])' + re.escape(t) + r'(?![A-Za-z])', name):
                hits.append((label, name, t))
    return hits


def sample_names():
    with open(P.REG / "arm_a_domains_r1.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    names = [(r["category"], r["brand"]) for r in rows] + [(r["category"] + " domain", r["domain"]) for r in rows]
    for fn, col in (("banks_current.csv", "holder_name"), ("airlines_current.csv", "name")):
        p = V40_REG / fn
        if p.exists():
            with open(p, newline="", encoding="utf-8") as f:
                names += [(f"v0.40 {fn}", r[col]) for r in csv.DictReader(f)]
    part_e = sorted({r["brand"].split(",")[0].split(" / ")[0] for r in rows if r["category"] in PART_E} | {"Marcus"})
    return names, part_e, rows


# the programme's COI notes outside the study folders (master CLAUDE.md, read only)
EXTRA_RECORDS = [P.ROOT.parents[1] / "Try system book" / "CLAUDE.md"]


def record_screen(part_e, worktrees=None, extra=None):
    worktrees = Path(worktrees or P.ROOT.parent)
    extra = EXTRA_RECORDS if extra is None else extra
    seen, hits, files = set(), [], 0
    for p in sorted(worktrees.glob("*/osf/**/DEVIATIONS*.md")) + [Path(x) for x in extra if Path(x).exists()]:
        try:
            raw = p.read_bytes()
        except OSError:
            continue
        h = hashlib.sha256(raw).hexdigest()
        if h in seen:
            continue
        seen.add(h)
        files += 1
        for ln in raw.decode("utf-8", "replace").splitlines():
            terms = [t for t in RECORD_TERMS if re.search(r'(?<![A-Za-z])' + re.escape(t) + r'(?![A-Za-z])', ln)]
            brands = [b for b in part_e if re.search(r'(?<![A-Za-z])' + re.escape(b) + r'(?![A-Za-z])', ln)]
            if terms and brands:
                rel = p.relative_to(worktrees).as_posix() if p.is_relative_to(worktrees) else str(p)
                hits.append((rel, brands, terms, ln.strip()[:240]))
    return files, hits


def main(out=None):
    names, part_e, rows = sample_names()
    terms = TERMS + TERMS_R3
    hits = screen(names, terms)
    files, rec = record_screen(part_e)
    counts = {c: len({r["brand_id"] for r in rows if r["category"] == c}) for c in PART_E}
    lines = [f"Arm A COI screens (Entry 0, Part E): {len(names)} names (brands, domains, v0.40 holder names) x "
             f"{len(terms)} terms ({len(TERMS)} r0 + {len(TERMS_R3)} r3 of v0.62)",
             "Part E brands: " + "; ".join(f"{c} {n}" for c, n in counts.items()),
             f"string-screen matches: {len(hits)}"]
    lines += ["  %s | %s | term: %s" % h for h in hits]
    lines += [f"record screen: {files} distinct DEVIATIONS files under the worktrees; lines naming a Part E brand and "
              f"a Samsung-group term ({', '.join(RECORD_TERMS)}): {len(rec)}"]
    lines += ["  %s | brands %s | terms %s | %s" % (f, ",".join(b), ",".join(t), ln) for f, b, t, ln in rec]
    lines += ["S-COI (params_arm_a.COI_FLAGGED, from v0.62 Entry 0 Part F): " + ", ".join(P.COI_FLAGGED)]
    out = Path(out or (P.ARM / "prereg" / "coi_screen_arm_a.txt"))
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return hits, rec


if __name__ == "__main__":
    main()
