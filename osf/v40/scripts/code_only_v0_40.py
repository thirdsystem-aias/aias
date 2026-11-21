#!/usr/bin/env python3
"""
code_only_v0_40.py -- AIAS(TM) v0.40, step 8: the coding-only step of DEVIATIONS entry "Coding-only step, scripted
audit draw and AI-only audit analyst" (2026-11-21).

Applies the locked coding rules of score_v0_40.py UNCHANGED and writes the coded mentions only; it computes and writes
no verdict, no test statistic, no sensitivity and no descriptive. It imports the locked module and calls exactly the
code path that score_v0_40.main() uses before scoring (load_registry, switch_controls, Scorer.__init__, which codes
every answer, and Scorer.mention_rows); Scorer.run() (the six tests) is never called. score_v0_40.py is not edited:
its SHA-256 is checked against the lock manifest before anything is read.

Outputs (in --out-dir, default osf/v40):
  data/v40_mentions.csv         byte-identical to the mentions file a full score_v0_40.py run writes (same rows, same
                                order, same writer); step 9's full run rewrites it, and its SHA-256 must not change
  data/v40_coded_answers.csv    one row per answer the coder kept (call ID, arm, slot, condition, kind, tier, category,
                                probe subject, number of mentions), the frame from which audit_draw_v0_40.py draws
  data/v40_coding_manifest.json SHA-256 of the inputs, of the locked scorer and of both outputs; counts
Refuses to run if a verdict file exists (osf/v40/v40_verdicts.json or any *verdict* file under the output dir).
Usage: python3 osf/v40/scripts/code_only_v0_40.py [--raw PATH] [--out-dir DIR]
"""
import argparse
import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import score_v0_40 as S  # noqa: E402  (the locked scorer; imported, never modified)

V40 = S.V40
LOCK_MANIFEST = V40 / "prereg" / "LOCK_MANIFEST_v0_40.sha256"
CODED_FIELDS = ["call_id", "arm", "slot", "condition", "run", "kind", "tier", "category", "probe_id", "brand_id",
                "n_mentions"]


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def locked_sha(name, manifest=LOCK_MANIFEST):
    """The SHA-256 the lock manifest records for a file whose path ends with `name` (None if not listed)."""
    for line in Path(manifest).read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[-1].lstrip("*").endswith(name):
            return parts[0]
    return None


def verdict_files(out_dir):
    """Every verdict file the run must not follow: the scorer's output and anything named *verdict* under out_dir."""
    out = Path(out_dir)
    found = [p for p in out.rglob("*verdict*") if p.is_file()]
    if (V40 / "v40_verdicts.json").exists():
        found.append(V40 / "v40_verdicts.json")
    return sorted(set(found))


def check_locked(manifest=LOCK_MANIFEST):
    """The scorer and its stop-rule module must be the locked bytes (lock manifest of tag v0.40-prereg-r1)."""
    for name in ("scripts/score_v0_40.py", "scripts/stoprule_v0_40.py"):
        want = locked_sha(name, manifest)
        have = sha256_file(HERE / Path(name).name)
        if want is None or want != have:
            raise SystemExit(f"[code_only] {name}: SHA-256 {have} does not match the lock manifest ({want}); stop")


def code(records):
    """Exactly score_v0_40.main()'s coding path: registry, Discover switch, Scorer.__init__ (codes every answer)."""
    units, subjects, gaps = S.load_registry()
    subjects = subjects + S.switch_controls(subjects)
    return S.Scorer(records, units, subjects, gaps, perms=0)


def write_mentions(sc, path):
    """Written exactly as score_v0_40.main() writes it (same fieldnames rule, newline and encoding)."""
    rows = list(sc.mention_rows())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["call_id"])
        w.writeheader()
        w.writerows(rows)
    return len(rows)


def write_coded_answers(sc, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CODED_FIELDS)
        w.writeheader()
        for r in sc.ok:
            w.writerow({"call_id": r["call_id"], "arm": r.get("arm"), "slot": r["slot"], "condition": r["condition"],
                        "run": r.get("run"), "kind": r["kind"], "tier": r["tier"], "category": r["category"],
                        "probe_id": r["probe_id"], "brand_id": r.get("brand_id") or "", "n_mentions": len(r["_m"])})
    return len(sc.ok)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=str(V40 / "data" / "v40_raw.jsonl"))
    ap.add_argument("--out-dir", default=str(V40))
    ap.add_argument("--manifest", default=str(LOCK_MANIFEST))
    a = ap.parse_args(argv)
    vf = verdict_files(a.out_dir)
    if vf:
        raise SystemExit(f"[code_only] refused: a verdict file exists ({', '.join(map(str, vf))})")
    check_locked(a.manifest)
    sc = code(S.load_raw(a.raw))
    out = Path(a.out_dir)
    (out / "data").mkdir(parents=True, exist_ok=True)
    mp, cp = out / "data" / "v40_mentions.csv", out / "data" / "v40_coded_answers.csv"
    n_m = write_mentions(sc, mp)
    n_a = write_coded_answers(sc, cp)
    man = {"step": "v0.40 step 8, coding only (DEVIATIONS 2026-11-21)", "written_utc": datetime.now(timezone.utc).isoformat(),
           "inputs": {"raw": {"path": str(a.raw), "sha256": sha256_file(a.raw)}},
           "locked_scorer_sha256": {"score_v0_40.py": sha256_file(HERE / "score_v0_40.py"),
                                    "stoprule_v0_40.py": sha256_file(HERE / "stoprule_v0_40.py")},
           "outputs": {"v40_mentions.csv": {"sha256": sha256_file(mp), "rows": n_m},
                       "v40_coded_answers.csv": {"sha256": sha256_file(cp), "rows": n_a}},
           "records_read": len(sc.all), "answers_coded": len(sc.ok), "cut_before_first_brand_missing": len(sc.cut_before),
           "verdicts_computed": False}
    (out / "data" / "v40_coding_manifest.json").write_text(json.dumps(man, indent=2), encoding="utf-8")
    print(f"[code_only] {n_a} answers coded, {n_m} mentions -> {mp}; no verdict computed")
    print(f"[code_only] v40_mentions.csv sha256 {man['outputs']['v40_mentions.csv']['sha256']}")
    return man


if __name__ == "__main__":
    main()
