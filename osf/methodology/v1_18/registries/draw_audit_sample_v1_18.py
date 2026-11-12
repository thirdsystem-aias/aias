"""Draw the declared audit sample of the domain table (prereg section 4.4): 50 rows from the hand-classified rows
(rule T2), proportional to class, plus 10 rows from the mechanically mapped rows (rule T1), seed 118003.
Rows are drawn from the sorted table, so the draw is reproducible. The sheet for the second coder holds the
domain only (no class, no rule, no count); the key file holds the first coder's class for comparison."""
import csv
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import common_v1_18 as C  # noqa: E402


def main():
    rows = list(csv.DictReader(open(C.DOMAIN_TABLE, newline="", encoding="utf-8")))
    rng = random.Random(C.SEEDS["audit_sample"])
    t2 = sorted((r for r in rows if r["rule"] == "T2"), key=lambda r: r["domain"])
    t1 = sorted((r for r in rows if r["rule"] == "T1"), key=lambda r: r["domain"])
    by = {}
    for r in t2:
        by.setdefault(r["class"], []).append(r)
    quota = {c: round(50 * len(v) / len(t2)) for c, v in by.items()}
    while sum(quota.values()) != 50:                       # fix rounding on the largest class
        big = max(quota, key=lambda c: len(by[c]))
        quota[big] += 1 if sum(quota.values()) < 50 else -1
    sample = []
    for c in sorted(by):
        sample += rng.sample(by[c], min(quota[c], len(by[c])))
    sample += rng.sample(t1, 10)
    rng.shuffle(sample)
    out = C.PHASE / "registries"
    with open(out / "audit_sheet_v1_18.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["domain", "second_coder_class", "second_coder_note"])
        for r in sorted(sample, key=lambda r: r["domain"]):
            w.writerow([r["domain"], "", ""])
    with open(out / "audit_key_v1_18.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["domain", "first_coder_class", "rule"])
        for r in sorted(sample, key=lambda r: r["domain"]):
            w.writerow([r["domain"], r["class"], r["rule"]])
    print(len(sample), "rows;", quota)


if __name__ == "__main__":
    main()
