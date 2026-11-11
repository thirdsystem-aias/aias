#!/usr/bin/env python3
"""AIAS v0.62 gate P2 (the language pre-step is inert on English), r3 draft. No model is called.

r1 open item 11, closed in code in r3. The pre-step maps typographic apostrophes (U+2018, U+2019, U+02BC, U+FF07) to "'"
(code_v0_62.normalise); the certified English matchers do not (score_v20/21/22.detect_mention lower-case and strip accents
only, so "Paula’s Choice" is not "Paula's Choice"). On an English t4 answer that writes a registry name with ’ the
pre-step + matcher would count a mention that v0.42's locked code did not, and P2 would fail for a reason that is not the
language pre-step. r1 fixed the rule (commit 4f3a226, a test with a fake matcher only): normalise BOTH sides. This module
implements the rule for the lock-time run and reports the apostrophe mapping's own effect beside P2 instead of hiding it:

  side PRE = code_v0_62.prepare_record (full pre-step: normalisation, URL removal, alias canonicalisation, script-boundary
             spacing; answer words for v0.19-v0.22 Phase A; v0.23 Phase A text unchanged);
  side REF = code_v0_62.normalise only (step 1 of the pre-step), on the same English records;
  both sides are coded by v0.42's coder, unchanged, as separate processes (as the study data are);
  P2 PASS = every coded cell (Phase B `mentioned`; Phase A `label`, `recognized`) is equal on the two sides, same rows.
  APOSTROPHE DELTA (reported, not a gate) = the cells where REF differs from v0.42's LOCKED coded tables. It can concern
  only Paula's Choice (v0.20) and L'Oréal Paris (v0.21): v0.19 has no registry name with an apostrophe and v0.23's
  patterns make it optional (jack\\s+daniel'?s?, hendrick'?s?). Handling: pre-registration r3 section 7.3.

Modes (run at the lock, on t4's English raw file; nothing here reads it before then):
  --prepare RAW OUT   write OUT/p2_pre.jsonl and OUT/p2_ref.jsonl (the input file is not changed); then code both with
                      python3 <v0.42>/osf/v42/scripts/code_t4_v0_42.py --raw OUT/p2_pre.jsonl --out OUT/pre   (and ref)
  --compare PRE REF [--locked DIR] [--json OUT]   compare the coded tables; exit 0 on PASS, 2 on FAIL.
"""
import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import code_v0_62 as C  # noqa: E402

VALUE_COLS = {"phase_a": ("label", "recognized"), "phase_b": ("mentioned",)}
APOSTROPHE_UNITS = {("v0.20", "Paula's Choice"), ("v0.21", "L'Oréal Paris"), ("v20", "Paula's Choice"),
                    ("v21", "L'Oréal Paris")}


def ref_record(rec):
    """Side REF: the same record with only step 1 of the pre-step (normalise) applied to its text. v0.23 Phase A text
    is left as written, as the pre-step leaves it (the recognition judge reads the answer as written)."""
    out = dict(rec)
    text = rec.get("text") or ""
    out["text_original"] = text
    v23a = rec.get("phase") == "A" and rec.get("substrate") in ("v23", "v0.23")
    out["text"] = text if v23a else C.normalise(text)
    return out


def pre_record(rec, aliaser=None):
    """Side PRE: the full pre-step, exactly as the study's coder prepares an answer (English: language 'en')."""
    return C.prepare_record(dict(rec, language=rec.get("language") or "en"), aliaser)


def prepare(raw_path, out_dir, aliaser=None):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    n = 0
    with open(raw_path, encoding="utf-8") as f, open(out_dir / "p2_pre.jsonl", "w", encoding="utf-8") as fp, \
            open(out_dir / "p2_ref.jsonl", "w", encoding="utf-8") as fr:
        for line in f:
            if not line.strip():
                continue
            rec = json.loads(line)
            fp.write(json.dumps(pre_record(rec, aliaser), ensure_ascii=False) + "\n")
            fr.write(json.dumps(ref_record(rec), ensure_ascii=False) + "\n")
            n += 1
    return n


def read_coded(d):
    """{(table, call_id, brand): (values...)} from a coder output directory (<sub>_phase_a.csv, <sub>_phase_b.csv)."""
    cells = {}
    for p in sorted(Path(d).glob("*_phase_[ab].csv")):
        kind = "phase_a" if p.stem.endswith("phase_a") else "phase_b"
        with open(p, encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                cells[(p.stem, r["call_id"], r["brand"])] = (r["substrate"],) + tuple(r[c] for c in VALUE_COLS[kind])
    return cells


def compare(a, b):
    """Cell-by-cell comparison of two read_coded() dicts -> summary with every difference counted by unit."""
    keys = set(a) | set(b)
    diff = [k for k in keys if a.get(k) != b.get(k)]
    by_unit = Counter((a.get(k) or b.get(k))[0] + " | " + k[2] for k in diff)
    return {"cells": len(keys), "only_in_first": sum(1 for k in keys if k not in b),
            "only_in_second": sum(1 for k in keys if k not in a), "different": len(diff),
            "by_unit": dict(sorted(by_unit.items())), "equal": not diff}


def p2(pre_dir, ref_dir, locked_dir=None):
    pre, ref = read_coded(pre_dir), read_coded(ref_dir)
    out = {"gate": "P2 (pre-step inert on English; both sides normalised)", "pre_vs_ref": compare(pre, ref)}
    out["result"] = "PASS" if out["pre_vs_ref"]["equal"] else "FAIL"
    if locked_dir:
        d = compare(ref, read_coded(locked_dir))
        units = {tuple(u.split(" | ", 1)) for u in d["by_unit"]}
        d["only_apostrophe_units"] = units <= APOSTROPHE_UNITS
        out["apostrophe_delta_ref_vs_locked"] = d
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="AIAS v0.62 gate P2 (r3)")
    ap.add_argument("--prepare", nargs=2, metavar=("RAW", "OUT"))
    ap.add_argument("--compare", nargs=2, metavar=("PRE_DIR", "REF_DIR"))
    ap.add_argument("--locked", default=None, help="v0.42's locked coded tables (for the apostrophe delta)")
    ap.add_argument("--json", default=None)
    a = ap.parse_args(argv)
    if a.prepare:
        n = prepare(*a.prepare)
        print(f"P2: {n} records -> {a.prepare[1]}/p2_pre.jsonl and p2_ref.jsonl; now code both with v0.42's coder")
        return 0
    if a.compare:
        r = p2(a.compare[0], a.compare[1], a.locked)
        if a.json:
            Path(a.json).write_text(json.dumps(r, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps(r, indent=1, ensure_ascii=False))
        return 0 if r["result"] == "PASS" else 2
    ap.error("--prepare RAW OUT or --compare PRE_DIR REF_DIR")


if __name__ == "__main__":
    sys.exit(main())
