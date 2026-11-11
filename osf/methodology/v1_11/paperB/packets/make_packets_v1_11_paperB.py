#!/usr/bin/env python3
"""Sentiment Paper B (SVA student labels): build per-student label packets from the v1.11 sample.

r2, 2026-11-11 (branch v1.11-paperB), from _runner_tmp/sva_labels/make_packets.py r1 of 2026-11-10.
Changed only: the sample path (relative to this file), the default variant (b: Pablo, 2026-11-10,
5:12 pm), the "rule" and "sample" strings of packet_design.json, and this docstring. Reads the
Paper B sample read-only; writes only under --out. Deterministic: same sample + N + seed + variant
-> byte-identical outputs.

Rule (PRE_REGISTRATION_v1_11_paperB.md, section 6):
  * Input: osf/methodology/v1_11/paperB/human_sample_v1_11_paperB_r1.csv, SHA-256 checked (566
    units); variant b drops the 48 recognition answers (518 units).
  * Capacity: N volunteers x CAP items each (CAP = 60). If capacity >= 2 x units, every unit is
    labelled by 2 different students (full double coding). Otherwise every unit gets 1 label and a
    seeded, category-stratified subset of (capacity - units) units gets a second label; if that
    subset would be < MIN_DOUBLE (200) units, the script stops (decision for Pablo: fallback).
  * Assignment: units are processed recognition answers first, then mention windows, each group in
    a seeded order. Each unit goes to the pair of students (or single student) that keeps the
    packets most even: fewest items of the unit's type, then fewest items overall, then the pair
    that has shared the fewest units so far, then a seeded random tie-break.
  * Each student's items are shuffled into their own seeded order. Students see random item codes,
    never the unit_id, answering model, wave, study or any score.
"""
import argparse, csv, hashlib, itertools, json, os, random, string, sys
from collections import Counter, defaultdict

# r1 (2026-11-10): the Samsung-group-free sample of v1.11 DEVIATIONS Entry 1 (commit 95c3fa1).
SAMPLE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir,
                                      "human_sample_v1_11_paperB_r1.csv"))
SAMPLE_SHA256 = "94d120f4a752d72f4fe96f90523fb3be663b3feba92fc3ff0dcdd2a11da0295e"
VARIANTS = {"a": None,              # (a) all 566 units
            "b": "recognition"}     # (b) without the 48 v0.23 recognition (brand-description) answers
SEED = 111023          # packet seed (pre-registration section 6; next free number after v1.11's 111022)
CAP = 60               # max items per student (566 x 2 / 19 = 59.6)
MIN_DOUBLE = 200       # fewest double-coded units for a usable human-human agreement estimate
CODE_ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"   # no 0/O, 1/I/L

PUBLIC_COLS = ["student_id", "position", "n_items", "item_id", "target_brand", "category",
               "question", "text_type", "text"]
KEY_COLS = ["item_id", "unit_id", "block", "category_label", "wave", "model", "frame",
            "brand_display", "unit_type", "bare", "n_coders", "coders"]


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def load_sample(path, exclude_brands, drop_unit_type=None, expected=SAMPLE_SHA256):
    got = sha256(path)
    if got != expected:
        sys.exit(f"sample SHA-256 {got} != expected {expected}: stop")
    csv.field_size_limit(sys.maxsize)
    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
    if exclude_brands:
        rows = [r for r in rows if r["brand_display"] not in exclude_brands]
    if drop_unit_type:
        rows = [r for r in rows if r["unit_type"] != drop_unit_type]
    return sorted(rows, key=lambda r: r["unit_id"]), got


def coding_depth(units, n_students, cap, rng):
    """Return {unit_id: 1 or 2}. Full double coding when capacity allows; else a stratified
    seeded subset is double coded (round-robin over categories in seeded order)."""
    n = len(units)
    capacity = n_students * cap
    if capacity >= 2 * n:
        return {u["unit_id"]: 2 for u in units}, "full double coding"
    n_double = capacity - n
    if n_double < MIN_DOUBLE:
        sys.exit(f"N={n_students}: capacity {capacity} allows only {max(n_double, 0)} double-coded "
                 f"units (< {MIN_DOUBLE}). Stop: Pablo decides (raise the load with a revised "
                 f"statement, or the paid-annotator fallback).")
    by_cat = defaultdict(list)
    for u in units:
        by_cat[(u["block"], u["category_label"])].append(u["unit_id"])
    cats = sorted(by_cat)
    for c in cats:
        rng.shuffle(by_cat[c])
    rng.shuffle(cats)
    chosen, i = [], 0
    while len(chosen) < n_double:
        c = cats[i % len(cats)]
        if by_cat[c]:
            chosen.append(by_cat[c].pop())
        i += 1
    depth = {u["unit_id"]: 1 for u in units}
    for uid in chosen:
        depth[uid] = 2
    return depth, f"partial double coding ({n_double} of {n} units)"


def assign(units, depth, students, rng):
    load = Counter()
    tload = defaultdict(Counter)       # per unit_type
    pair = Counter()
    coders = {}
    rec = [u for u in units if u["unit_type"] == "recognition"]
    men = [u for u in units if u["unit_type"] != "recognition"]
    rng.shuffle(rec)
    rng.shuffle(men)
    for u in rec + men:
        t = u["unit_type"]
        k = depth[u["unit_id"]]
        cands = list(itertools.combinations(students, k))
        tb = {c: rng.random() for c in cands}
        def key(c):
            return (sum(tload[t][s] for s in c), sum(load[s] for s in c),
                    max(load[s] for s in c), pair[c] if k == 2 else 0, tb[c])
        best = min(cands, key=key)
        for s in best:
            load[s] += 1
            tload[t][s] += 1
        if k == 2:
            pair[best] += 1
        coders[u["unit_id"]] = list(best)
    return coders, load, tload, pair


def item_codes(units, rng):
    codes, used = {}, set()
    for u in units:
        while True:
            c = "".join(rng.choice(CODE_ALPHABET) for _ in range(5))
            if c not in used:
                used.add(c)
                codes[u["unit_id"]] = c
                break
    return codes


def write_csv(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n", type=int, default=19, help="number of volunteers (after sign-ups close)")
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--cap", type=int, default=CAP)
    ap.add_argument("--sample", default=SAMPLE)
    ap.add_argument("--exclude-brand", action="append", default=[],
                    help="NOT the default: only if Pablo decides to drop a brand (a recorded deviation)")
    ap.add_argument("--sample-sha256", default=SAMPLE_SHA256)
    ap.add_argument("--variant", choices=sorted(VARIANTS), default="b",
                    help="b (pre-registered) = drop the recognition (brand-description) answers; a = all units")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    units, digest = load_sample(a.sample, set(a.exclude_brand), VARIANTS[a.variant], a.sample_sha256)
    rng = random.Random(a.seed)
    students = [f"R{i:02d}" for i in range(1, a.n + 1)]
    depth, mode = coding_depth(units, a.n, a.cap, rng)
    coders, load, tload, pair = assign(units, depth, students, rng)
    codes = item_codes(units, rng)
    by_id = {u["unit_id"]: u for u in units}

    os.makedirs(os.path.join(a.out, "packets"), exist_ok=True)
    os.makedirs(os.path.join(a.out, "key_PRIVATE"), exist_ok=True)
    packets = defaultdict(list)
    for uid, ss in coders.items():
        for s in ss:
            packets[s].append(uid)
    all_rows, out_hashes = [], {}
    for s in students:
        items = sorted(packets[s])          # canonical before the seeded shuffle
        rng.shuffle(items)
        rows = []
        for pos, uid in enumerate(items, 1):
            u = by_id[uid]
            rows.append({"student_id": s, "position": pos, "n_items": len(items), "item_id": codes[uid],
                         "target_brand": u["brand_display"], "category": u["category_label"],
                         "question": u["question"], "text_type": u["text_type"], "text": u["text"]})
        p = os.path.join(a.out, "packets", f"packet_{s}.csv")
        write_csv(p, PUBLIC_COLS, rows)
        out_hashes[os.path.relpath(p, a.out)] = sha256(p)
        all_rows += rows
    p = os.path.join(a.out, "packets", "packets_all.csv")
    write_csv(p, PUBLIC_COLS, all_rows)
    out_hashes[os.path.relpath(p, a.out)] = sha256(p)
    key_rows = []
    for u in units:
        key_rows.append({"item_id": codes[u["unit_id"]], **{c: u[c] for c in KEY_COLS[1:10]},
                         "n_coders": len(coders[u["unit_id"]]), "coders": ";".join(coders[u["unit_id"]])})
    p = os.path.join(a.out, "key_PRIVATE", "item_key.csv")
    write_csv(p, KEY_COLS, sorted(key_rows, key=lambda r: r["unit_id"]))
    out_hashes[os.path.relpath(p, a.out)] = sha256(p)

    pc = Counter(pair[c] for c in itertools.combinations(students, 2))
    design = {
        "rule": "make_packets_v1_11_paperB.py r2 (PRE_REGISTRATION_v1_11_paperB.md, section 6)",
        "sample": os.path.basename(a.sample), "sample_sha256": digest, "units": len(units),
        "excluded_brands": sorted(a.exclude_brand), "variant": a.variant,
        "dropped_unit_type": VARIANTS[a.variant], "seed": a.seed, "n_students": a.n, "cap": a.cap,
        "mode": mode, "labels_total": sum(load.values()),
        "units_double": sum(1 for v in depth.values() if v == 2),
        "units_single": sum(1 for v in depth.values() if v == 1),
        "items_per_student": {s: load[s] for s in students},
        "recognition_per_student": {s: tload["recognition"][s] for s in students},
        "pairs_sharing_k_units": {str(k): v for k, v in sorted(pc.items())},
        "outputs_sha256": out_hashes,
    }
    with open(os.path.join(a.out, "packet_design.json"), "w", encoding="utf-8") as f:
        json.dump(design, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(json.dumps({k: v for k, v in design.items() if k != "outputs_sha256"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
