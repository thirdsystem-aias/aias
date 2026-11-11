#!/usr/bin/env python3
"""
audit_checks_v1_13.py -- Part II computations the protocol specifies and no locked script performs
(postlock/DEVIATIONS_continued_v1_13.md, Entries 1 and 2). NOT a locked file; it imports the locked scripts read-only
and changes no hypothesis, threshold, verdict rule or collected datum.

  AQ1  every brand has a D_b row and none is UNRESOLVED (protocol section 6)                     -> counts
  AQ2  share of P1 fetched with status 200: P1 whose final response after redirects has HTTP status 200 (outcome ok),
       over the units with an own domain (defunct units excluded); the share with outcome ok is reported beside it
  AQ3  JSON-LD blocks that did not parse: sum of ld_errors (and ld_blocks) over every fetched page of pass 1
  AQ4  pass 2 (P1 only, 7 days later): share of brands, among those with P1 ok in both passes, whose indicator set
       (1)-(5) computed from P1 alone changed (pass 1 is recomputed from its P1 record so both sides use P1 only)
  S-KG H7 sensitivity named in protocol section 5 ("enters H7 only through sensitivity (SDRI_kg alone)"):
       rho_w(SDRI_kg, G*), one-sided, every non-defunct unit with SDRI_kg and a rated G* (including those whose P1
       could not be fetched), seed 113009 (pre-registration section 3: "S-sensitivities"), 10,000 permutations,
       2,000 bootstrap draws; reported with the H7 band reading beside it, never a verdict

Inputs (Stage A outputs): audit/v1_13_audit_records.jsonl (pass 1), audit/v1_13_audit_records_pass2.jsonl (pass 2,
optional), audit/v1_13_sdri.csv, and v1_13_verdicts.json (Stage C1, for G*; optional: S-KG is skipped without it).
Writes audit/v1_13_audit_checks.json once, with the SHA-256 of every input and of this script.

  python3 osf/methodology/v1_13/postlock/audit_checks_v1_13.py [--pass2] [--verdicts PATH] [--out PATH]
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PHASE = HERE.parent
sys.path.insert(0, str(PHASE / "scripts"))
sys.dont_write_bytecode = True
import score_v1_13 as S  # noqa: E402
import audit_v1_13 as A  # noqa: E402

AUDIT = PHASE / "audit"
LOCKED_DIRS = ("prereg", "registries", "anchor", "lock", "scripts", "data")
SEED_SENS = S.SEEDS["sensitivities"]


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read_jsonl(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()]


def refuse_locked(out):
    rel = Path(out).resolve()
    if any(str(rel).startswith(str((PHASE / d).resolve()) + "/") for d in LOCKED_DIRS):
        sys.exit(f"REFUSED: {out} is inside a locked directory")
    if rel.exists():
        sys.exit(f"REFUSED: {out} exists (written once; remove it only under a logged deviation)")


def aq1(units):
    return {"units": len(units), "unresolved": len(S.unresolved_units(units)),
            "none": sum(1 for u in units.values() if u["status"] == "NONE"),
            "passed": not S.unresolved_units(units)}


def _p1(r):
    return (r.get("pages") or {}).get("P1") or {}


def aq2(records):
    own = [r for r in records if not r.get("phantom") and r.get("domain")]
    ok = [r for r in own if _p1(r).get("outcome") == "ok"]
    s200 = [r for r in ok if _p1(r).get("status") == 200]
    n = len(own)
    share = len(s200) / n if n else None
    return {"units_with_domain": n, "p1_status_200": len(s200), "share_status_200": share,
            "p1_outcome_ok": len(ok), "share_outcome_ok": len(ok) / n if n else None,
            "flag_below_0_80": share is not None and share < 0.80,
            "outcomes": {o: sum(1 for r in own if str(_p1(r).get("outcome")) == o)
                         for o in sorted({str(_p1(r).get("outcome")) for r in own})}}


def aq3(records):
    blocks = errors = pages = 0
    for r in records:
        for pg in (r.get("pages") or {}).values():
            if pg.get("outcome") == "ok":
                pages += 1
                blocks += int(pg.get("ld_blocks") or 0)
                errors += int(pg.get("ld_errors") or 0)
    return {"pages_parsed": pages, "ld_blocks": blocks, "ld_parse_errors": errors}


def p1_indicators(r):
    """(1)-(5) from the P1 record alone (types, same_as stored by audit_unit), or None if P1 was not ok."""
    p = _p1(r)
    if p.get("outcome") != "ok":
        return None
    home = {"types": set(p.get("types") or []), "same_as": list(p.get("same_as") or [])}
    return A.site_indicators(home, [home])


def aq4(records1, records2):
    by2 = {(r["substrate"], r["brand_id"]): r for r in records2}
    both, changed = 0, []
    for r in records1:
        k = (r["substrate"], r["brand_id"])
        if k not in by2:
            continue
        a, b = p1_indicators(r), p1_indicators(by2[k])
        if a is None or b is None:
            continue
        both += 1
        if a != b:
            changed.append(f"{k[0]}|{k[1]}")
    return {"basis": "indicators (1)-(5) from P1 alone in both passes", "units_ok_in_both": both,
            "changed": len(changed), "share_changed": len(changed) / both if both else None, "units_changed": changed}


def skg_sensitivity(sdri_rows, verdicts, n_perm=S.N_PERM, n_boot=S.N_BOOT):
    units = verdicts["units"]
    gs = {tuple(k.split("|", 1)): (u["G_star"] if u["rated"] else None) for k, u in units.items()}
    kg = {}
    for r in sdri_rows:
        if str(r.get("phantom", "0")) == "1":
            continue
        kg[(r["substrate"], r["brand_id"])] = S._num(r.get("SDRI_kg"))
    leg = S.sep_leg(kg, gs, SEED_SENS, n_perm, n_boot, sided="one")
    return {"statistic": "rho_w(SDRI_kg, G*), one-sided; units with SDRI_kg and a rated G* (P1 failures included)",
            "seed": SEED_SENS, "leg": leg, "band_reading_H7": S.struct_gap_verdict(leg, True),
            "gating": False, "note": "sensitivity named in protocol section 5; reported beside H7, never a verdict"}


def run(records, records2, sdri_rows, verdicts, units, n_perm=S.N_PERM, n_boot=S.N_BOOT):
    out = {"AQ1": aq1(units), "AQ2": aq2(records), "AQ3": aq3(records)}
    out["AQ4"] = aq4(records, records2) if records2 is not None else {"status": "NOT_COMPUTED",
                                                                      "reason": "pass 2 records not given"}
    out["S_KG"] = skg_sensitivity(sdri_rows, verdicts, n_perm, n_boot) if verdicts else {
        "status": "NOT_COMPUTED", "reason": "verdict file (Stage C1) not given"}
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="v1.13 Part II checks AQ1-AQ4 and the SDRI_kg-only H7 sensitivity")
    ap.add_argument("--records", type=Path, default=AUDIT / "v1_13_audit_records.jsonl")
    ap.add_argument("--pass2", nargs="?", const=AUDIT / "v1_13_audit_records_pass2.jsonl", type=Path, default=None)
    ap.add_argument("--sdri", type=Path, default=AUDIT / "v1_13_sdri.csv")
    ap.add_argument("--verdicts", type=Path, default=None)
    ap.add_argument("--domains", type=Path, default=S.DOMAINS_CSV, help="testing only; default the frozen D_b list")
    ap.add_argument("--perm", type=int, default=S.N_PERM)
    ap.add_argument("--boot", type=int, default=S.N_BOOT)
    ap.add_argument("--out", type=Path, default=AUDIT / "v1_13_audit_checks.json")
    a = ap.parse_args(argv)
    refuse_locked(a.out)
    records = read_jsonl(a.records)
    records2 = read_jsonl(a.pass2) if a.pass2 else None
    sdri_rows = S.read_csv(a.sdri)
    verdicts = json.loads(a.verdicts.read_text(encoding="utf-8")) if a.verdicts else None
    units = S.load_brand_domains(a.domains)
    doc = run(records, records2, sdri_rows, verdicts, units, a.perm, a.boot)
    doc["inputs"] = {"records": [str(a.records), sha256(a.records)], "sdri": [str(a.sdri), sha256(a.sdri)],
                     "pass2": [str(a.pass2), sha256(a.pass2)] if a.pass2 else None,
                     "verdicts": [str(a.verdicts), sha256(a.verdicts)] if a.verdicts else None,
                     "domains": [str(a.domains), sha256(a.domains)], "script_sha256": sha256(__file__),
                     "test_only": a.domains.resolve() != S.DOMAINS_CSV.resolve() or a.perm != S.N_PERM}
    doc["written_utc"] = datetime.now(timezone.utc).isoformat()
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(doc, indent=2, default=str), encoding="utf-8")
    print(f"AQ2 {doc['AQ2']['share_status_200']}; AQ3 errors {doc['AQ3']['ld_parse_errors']}; "
          f"AQ4 {doc['AQ4'].get('share_changed', doc['AQ4'].get('status'))} -> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
