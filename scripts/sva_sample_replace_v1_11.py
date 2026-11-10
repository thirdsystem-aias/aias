#!/usr/bin/env python3
"""v1.11 Paper B sample: replace the units whose target brand is a Samsung-group brand
(DEVIATIONS Entry 1, 2026-11-10).

Reads the locked v1.11 files read-only (`prereg/units_v1_11.csv`, `prereg/human_sample_v1_11.csv`,
both SHA-256 checked) and writes a new sample file under `paperB/`. The locked sample is not changed.

Rule (fixed here, seed 111025):
  1. Screen. A unit is EXCLUDED if its target brand (brand_display) is a Samsung-group brand (SG_TERMS:
     Samsung; Harman and its brands; the former Sound United brands). A unit whose text or question
     merely names such a brand is listed (`mention_only`) and kept.
  2. Stratum (as v1.11 `human_sample` defines its cells): F = category x wave x answering model;
     E = category x answering model; R = category (v1.11 draws R per brand; a Samsung-group R brand
     cannot be replaced from its own brand).
  3. Candidates: units of the frozen unit table in the same stratum that are judged, not in the
     sample (original or already drawn), whose target brand is not Samsung-group and whose text and
     question name no Samsung-group brand.
  4. Preference, in order: (a) brands still under v1.11's cap of 3 units per brand per category;
     if none, the brands with the fewest units in that category (the cap is relaxed by the least
     amount; recorded as `cap_relaxed`); (b) the excluded unit's frame, if any candidate has it;
     (c) a draw with random.Random(111025).choice over the remaining candidates sorted by unit_id.
  5. Excluded units are processed in unit_id order; counts are updated after each draw.
  No judge output, valence or score is read. Output rows are sorted by unit_id (as v1.11).
"""
import argparse, hashlib, json, random, re, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import score_v1_11 as S  # noqa: E402

V111 = ROOT / "osf" / "methodology" / "v1_11"
UNITS = V111 / "prereg" / "units_v1_11.csv"
SAMPLE = V111 / "prereg" / "human_sample_v1_11.csv"
UNITS_SHA256 = "1243e8e15e2dc6afc894197de9819d149d934e3883bc9f504e8fdfbbbb9c08b8"   # u0_v1_11.json
SAMPLE_SHA256 = "b80bd109cf92d66fa1eef50462255d3a694d2e03c03c804c44cd0d19ff44f307"
OUT_DIR = V111 / "paperB"
OUT_NAME = "human_sample_v1_11_paperB_r1.csv"
SEED = 111025
CAP = S.HUMAN_MAX_PER_BRAND          # 3

# Samsung-group brands (membership sources: DEVIATIONS Entry 1). Case-insensitive, word-bounded;
# the common words in CASE_SENSITIVE count only in their capitalised brand form.
SG_TERMS = {
    "Samsung": r"samsung", "Harman": r"harman", "Harman Kardon": r"harman\s*/?\s*kardon",
    "JBL": r"jbl", "AKG": r"akg", "Infinity": r"infinity", "Mark Levinson": r"mark\s+levinson",
    "Revel": r"revel", "Lexicon": r"lexicon", "Arcam": r"arcam", "Roon": r"roon",
    "Sound United": r"sound\s+united", "Denon": r"denon", "Marantz": r"marantz",
    "Bowers & Wilkins": r"bowers\s*(?:&|and)\s*wilkins|b\s*&\s*w", "Polk Audio": r"polk",
    "Definitive Technology": r"definitive\s+tech(?:nology)?", "Boston Acoustics": r"boston\s+acoustics",
    "Classe": r"class[eé]", "HEOS": r"heos",
}
CASE_SENSITIVE = {"Infinity": r"Infinity", "Revel": r"Revel", "Lexicon": r"Lexicon", "Classe": r"Class[eé]"}
_RX = {k: re.compile(r"(?<![A-Za-z0-9])(?:" + v + r")(?![A-Za-z0-9])", re.I) for k, v in SG_TERMS.items()}


def sha256_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def sg_terms_in(s: str) -> list:
    """Samsung-group terms named in a string (sorted, unique)."""
    out = set()
    for k, rx in _RX.items():
        for m in rx.finditer(s or ""):
            if k in CASE_SENSITIVE and not re.fullmatch(CASE_SENSITIVE[k], m.group(0)):
                continue
            out.add(k)
    return sorted(out)


def is_sg_brand(brand_display: str) -> bool:
    return bool(sg_terms_in(brand_display))


def names_sg(u: dict) -> list:
    return sorted(set(sg_terms_in(u["text"])) | set(sg_terms_in(u["question"])))


def stratum(u: dict) -> tuple:
    if u["block"] == "F":
        return ("F", u["category"], u["wave"], u["model"])
    if u["block"] == "E":
        return ("E", u["category"], u["model"])
    return ("R", u["category"])


def screen(sample: list) -> dict:
    subject = [u["unit_id"] for u in sample if is_sg_brand(u["brand_display"])]
    mention_only = {u["unit_id"]: names_sg(u) for u in sample
                    if u["unit_id"] not in subject and names_sg(u)}
    return {"subject": sorted(subject), "mention_only": dict(sorted(mention_only.items()))}


def replace(units: list, sample_ids: set, seed: int = SEED) -> dict:
    """Return {'sample': [unit dicts], 'out': [...], 'in': [...], 'draws': [...]} (deterministic)."""
    by_id = {u["unit_id"]: u for u in units}
    sample = [by_id[i] for i in sorted(sample_ids)]
    scr = screen(sample)
    rng = random.Random(seed)
    current = set(sample_ids)
    used = set(sample_ids)
    brand_n = Counter((by_id[i]["block"], by_id[i]["category"], by_id[i]["brand"]) for i in current)
    draws = []
    for uid in scr["subject"]:
        x = by_id[uid]
        current.discard(uid)
        brand_n[(x["block"], x["category"], x["brand"])] -= 1
        st = stratum(x)
        cand = [u for u in units if u["judged"] and stratum(u) == st and u["unit_id"] not in used
                and not is_sg_brand(u["brand_display"]) and not names_sg(u)]
        rec = {"out": uid, "stratum": list(st), "frame_out": x["frame"], "candidates": len(cand)}
        if not cand:
            rec.update({"in": None, "note": "no eligible candidate in the stratum: not replaced"})
            draws.append(rec)
            continue
        cnt = lambda u: brand_n[(u["block"], u["category"], u["brand"])]
        under = [u for u in cand if cnt(u) < CAP]
        if under:
            pool, relaxed = under, False
        else:
            lo = min(cnt(u) for u in cand)
            pool, relaxed = [u for u in cand if cnt(u) == lo], True
        same_frame = [u for u in pool if u["frame"] == x["frame"]]
        pool2 = same_frame or pool
        pick = rng.choice(sorted(pool2, key=lambda u: u["unit_id"]))
        rec.update({"in": pick["unit_id"], "cap_relaxed": relaxed, "brand_units_before_draw": cnt(pick),
                    "pool_after_cap_rule": len(pool), "pool_after_frame_rule": len(pool2),
                    "same_frame": bool(same_frame), "frame_in": pick["frame"], "brand_in": pick["brand_display"]})
        current.add(pick["unit_id"])
        used.add(pick["unit_id"])
        brand_n[(pick["block"], pick["category"], pick["brand"])] += 1
        draws.append(rec)
    new = sorted((by_id[i] for i in current), key=lambda u: u["unit_id"])
    return {"sample": new, "screen": scr, "draws": draws}


def stratum_counts(sample: list) -> dict:
    return {"|".join(k): v for k, v in sorted(Counter(stratum(u) for u in sample).items())}


def load_locked():
    for p, h in ((UNITS, UNITS_SHA256), (SAMPLE, SAMPLE_SHA256)):
        got = sha256_file(p)
        if got != h:
            sys.exit(f"{p.name}: SHA-256 {got} != locked {h}: stop")
    units = S.read_units(UNITS)
    sample_ids = {u["unit_id"] for u in units if u["human"]}
    return units, sample_ids


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-dir", default=str(OUT_DIR))
    ap.add_argument("--seed", type=int, default=SEED)
    a = ap.parse_args()
    units, sample_ids = load_locked()
    orig = sorted((u for u in units if u["unit_id"] in sample_ids), key=lambda u: u["unit_id"])
    if S.human_csv_bytes(orig) != SAMPLE.read_bytes():
        sys.exit("the unit table's human flags do not reproduce the locked sample byte for byte: stop")
    res = replace(units, sample_ids, a.seed)
    out = S.human_csv_bytes(res["sample"])
    od = Path(a.out_dir)
    od.mkdir(parents=True, exist_ok=True)
    (od / OUT_NAME).write_bytes(out)
    before, after = stratum_counts(orig), stratum_counts(res["sample"])
    changed = sorted(k for k in set(before) | set(after) if before.get(k, 0) != after.get(k, 0))
    cat_b = Counter(f"{u['block']} {u['category']}" for u in orig)
    cat_a = Counter(f"{u['block']} {u['category']}" for u in res["sample"])
    report = {
        "rule": "scripts/sva_sample_replace_v1_11.py (v1.11 DEVIATIONS Entry 1, 2026-11-10)", "seed": a.seed,
        "inputs": {"units_v1_11.csv": UNITS_SHA256, "human_sample_v1_11.csv": SAMPLE_SHA256},
        "output": {"path": OUT_NAME, "sha256": hashlib.sha256(out).hexdigest(), "rows": len(res["sample"])},
        "screen": res["screen"], "draws": res["draws"],
        "per_category_before": dict(sorted(cat_b.items())), "per_category_after": dict(sorted(cat_a.items())),
        "strata_changed": {k: {"before": before.get(k, 0), "after": after.get(k, 0)} for k in changed},
        "strata_before": before, "strata_after": after,
        "brands_in_category_after": {f"{d['stratum'][0]} {d['stratum'][1]}": dict(sorted(Counter(
            u["brand_display"] for u in res["sample"] if (u["block"], u["category"]) ==
            (d["stratum"][0], d["stratum"][1])).items())) for d in res["draws"]},
    }
    (od / "replace_report_v1_11_paperB_r1.json").write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n",
                                                           encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("seed", "output", "screen", "draws", "strata_changed",
                                             "per_category_after")}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
