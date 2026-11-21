#!/usr/bin/env python3
"""
audit_draw_v0_40.py -- AIAS(TM) v0.40, step 8: the scripted draw of the declared audit sample (pre-registration
section 5.5; DEVIATIONS entry of 2026-11-21).

Draws, with seed 4040 and before any verdict is read:
  * 100 recommendation answers that contain at least one ghost or control mention (all of them if fewer),
    stratified by arm and condition (L|S0, C|S0, C|S1);
  * 100 status (S) answers, stratified by arm, condition and role of the probe's subject (ghost, control, incumbent).
Allocation within each set: proportional to stratum size, largest remainder (ties: stratum key order); within a
stratum, random.Random(4040).sample over the stratum's sorted call IDs, strata taken in sorted key order, one
generator for the recommendation set and then the status set. Deterministic: the same inputs give the same sample.

Inputs: data/v40_coded_answers.csv and data/v40_mentions.csv written by code_only_v0_40.py (their SHA-256 must
match data/v40_coding_manifest.json), prereg/probes_v0_40.json (subject roles).
Outputs (osf/v40/audit/): v40_audit_sample.json, v40_audit_sample.csv, AUDIT_SAMPLE_v0_40.sha256 (manifest).
Refuses to run if any verdict file exists, and refuses to overwrite an existing sample with a different one.
Usage: python3 osf/v40/scripts/audit_draw_v0_40.py [--base DIR]
"""
import argparse
import csv
import hashlib
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import code_only_v0_40 as C  # noqa: E402

SEED = 4040
N_REC, N_STATUS = 100, 100
SUBJECT_KINDS = ("ghost", "control")      # mention kinds that put a recommendation answer in the frame
ROLES = ("ghost", "control", "incumbent")


def read_csv(p):
    with open(p, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def allocate(sizes, total):
    """Proportional allocation with largest remainder; all units when the frame is not larger than `total`."""
    keys = sorted(sizes)
    n = sum(sizes.values())
    if n <= total:
        return {k: sizes[k] for k in keys}
    quota = {k: sizes[k] * total / n for k in keys}
    out = {k: int(quota[k]) for k in keys}
    left = total - sum(out.values())
    order = sorted(keys, key=lambda k: (-(quota[k] - out[k]), keys.index(k)))
    for k in order[:left]:
        out[k] += 1
    return out


def draw(strata, total, rng):
    """strata: {key: [call_id, ...]} -> list of (key, call_id), keys in sorted order."""
    alloc = allocate({k: len(v) for k, v in strata.items()}, total)
    out = []
    for k in sorted(strata):
        ids = sorted(strata[k])
        for cid in sorted(rng.sample(ids, alloc[k])):
            out.append((k, cid))
    return out, alloc


def frames(coded, mentions, probes):
    role_of = {p["probe_id"]: p.get("subject_role") for p in probes}
    with_subject = {m["call_id"] for m in mentions if m["kind"] in SUBJECT_KINDS}
    rec, sta = defaultdict(list), defaultdict(list)
    for r in coded:
        if r["kind"] == "recommendation" and r["call_id"] in with_subject:
            rec[f"{r['arm']}|{r['condition']}"].append(r["call_id"])
        elif r["tier"] == "S":
            role = role_of.get(r["probe_id"])
            if role not in ROLES:
                raise SystemExit(f"[audit_draw] status probe {r['probe_id']} has no subject role in the probe set")
            sta[f"{r['arm']}|{r['condition']}|{role}"].append(r["call_id"])
    return rec, sta


def build_sample(coded, mentions, probes, seed=SEED):
    rec, sta = frames(coded, mentions, probes)
    rng = random.Random(seed)
    rec_s, rec_a = draw(rec, N_REC, rng)
    sta_s, sta_a = draw(sta, N_STATUS, rng)
    items = ([{"set": "recommendation", "stratum": k, "call_id": c} for k, c in rec_s]
             + [{"set": "status", "stratum": k, "call_id": c} for k, c in sta_s])
    return {"seed": seed, "frames": {"recommendation": {k: len(v) for k, v in sorted(rec.items())},
                                     "status": {k: len(v) for k, v in sorted(sta.items())}},
            "allocation": {"recommendation": rec_a, "status": sta_a}, "n": len(items), "items": items}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=str(C.V40), help="the study folder (default osf/v40)")
    a = ap.parse_args(argv)
    base = Path(a.base)
    vf = C.verdict_files(base)
    if vf:
        raise SystemExit(f"[audit_draw] refused: a verdict file exists ({', '.join(map(str, vf))})")
    data = base / "data"
    man = json.loads((data / "v40_coding_manifest.json").read_text(encoding="utf-8"))
    for name in ("v40_mentions.csv", "v40_coded_answers.csv"):
        if C.sha256_file(data / name) != man["outputs"][name]["sha256"]:
            raise SystemExit(f"[audit_draw] {name} differs from the coding-only manifest; re-run code_only_v0_40.py")
    probes = json.loads((base / "prereg" / "probes_v0_40.json").read_text(encoding="utf-8"))["probes"]
    sample = build_sample(read_csv(data / "v40_coded_answers.csv"), read_csv(data / "v40_mentions.csv"), probes)
    sample["inputs_sha256"] = {n: man["outputs"][n]["sha256"] for n in ("v40_mentions.csv", "v40_coded_answers.csv")}
    sample["inputs_sha256"]["probes_v0_40.json"] = C.sha256_file(base / "prereg" / "probes_v0_40.json")
    out = base / "audit"
    out.mkdir(parents=True, exist_ok=True)
    body = json.dumps(sample, indent=2, sort_keys=True) + "\n"
    jp = out / "v40_audit_sample.json"
    if jp.exists() and jp.read_text(encoding="utf-8") != body:
        raise SystemExit(f"[audit_draw] refused: {jp} exists and differs from this draw (the sample is drawn once)")
    jp.write_text(body, encoding="utf-8")
    cp = out / "v40_audit_sample.csv"
    with open(cp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["set", "stratum", "call_id"])
        w.writeheader()
        w.writerows(sample["items"])
    lines = [f"{C.sha256_file(p)}  osf/v40/{p.relative_to(base).as_posix()}" for p in (jp, cp)]
    lines += [f"{h}  osf/v40/data/{n}" if n != "probes_v0_40.json" else f"{h}  osf/v40/prereg/{n}"
              for n, h in sorted(sample["inputs_sha256"].items())]
    (out / "AUDIT_SAMPLE_v0_40.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[audit_draw] {sample['n']} answers drawn (seed {SEED}): "
          f"recommendation {sample['allocation']['recommendation']}, status {sample['allocation']['status']}")
    return sample


if __name__ == "__main__":
    main()
