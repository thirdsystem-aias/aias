#!/usr/bin/env python3
"""
v1_9_cross_check_v1_20.py -- dated post-hoc completion (Sun 2026-11-22) of a pre-registered check that v1.20's
scorer omitted: the P / C* cross-check of v1.11 section 2 / v1.20 section 5 item 3 ("P and C* are opened (join
check, P/C* cross-check, window counts)"). v1.11's Stage C writes it as the block `P_Cstar_v1_9_cross_check`
({"differences": [...], "rows_compared": n}); `score_v1_20.run_stage_c` does not. This script runs v1.11's own
comparison, copied verbatim from `score_v1_11.run_stage_c` (the nested `_differs`, tolerance 1e-9), on the same two
pinned inputs, and writes papers/v1_20/v1_9_cross_check_v1_20.json. It is never a verdict input and changes no
verdict. Because the v1.9 table stores P and C* to 4 decimals and the profiles table to 6, the exact rule flags
rounding; the script therefore also reports, as a descriptive beside it, the rows that still differ after
rounding the profiles value to the v1.9 table's printed precision (4 decimals) and the largest absolute difference.

Inputs (SHA-256 checked against v1.11's INPUTS_MANIFEST_v1_11.json; refuses on mismatch):
  osf/aias_2_0/aias_2_0_profiles.csv        (P and C*; as read by v1.11 / v1.20 Stage C via score_v1_10.parse_profiles)
  osf/methodology/v1_9/v1_9_unit_table.csv  (the cross-check table)
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import score_v1_11 as S  # noqa: E402  (read-only; its V is the pinned score_v1_10)

V = S.V
MANIFEST = ROOT / "osf/methodology/v1_11/registries/INPUTS_MANIFEST_v1_11.json"
OUT = HERE / "v1_9_cross_check_v1_20.json"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    pinned = {f["path"]: f["sha256"] for f in man["files"] if f.get("path") in (S.PROFILES_REL, S.V19_TABLE_REL)}
    inputs = {}
    for rel in (S.PROFILES_REL, S.V19_TABLE_REL):
        got = sha(ROOT / rel)
        if pinned.get(rel) != got:
            print(f"REFUSED: {rel} sha256 {got} != pinned {pinned.get(rel)}", file=sys.stderr)
            return 3
        inputs[rel] = {"sha256": got, "pinned_in": str(MANIFEST.relative_to(ROOT)), "matches_pin": True}

    prof = V._read_csv(ROOT / S.PROFILES_REL)
    P, C, NM = V.parse_profiles(prof)
    t19 = V._read_csv(ROOT / S.V19_TABLE_REL)

    # --- verbatim from score_v1_11.run_stage_c ---
    def _differs(r) -> bool:
        k = (r["substrate"], r["brand"])
        p = P.get(r["wave"], {}).get(k)
        if p is None or not math.isfinite(p) or abs(float(r["P"]) - p) > 1e-9:
            return True
        c19 = (r.get("C_star") or "").strip()
        c = C.get(r["wave"], {}).get(k)
        if (c19 == "") != (c is None):
            return True
        return c is not None and abs(float(c19) - c) > 1e-9

    diff = [r["wave"] + "|" + r["substrate"] + "|" + r["brand"] for r in t19 if _differs(r)]
    # --- end verbatim ---

    # descriptive beside it: the same comparison at the v1.9 table's printed precision (4 decimals)
    def _differs_4dp(r) -> list:
        why = []
        k = (r["substrate"], r["brand"])
        p = P.get(r["wave"], {}).get(k)
        if p is None or not math.isfinite(p):
            return ["P missing in profiles"]
        if round(p, 4) != round(float(r["P"]), 4):
            why.append("P")
        c19 = (r.get("C_star") or "").strip()
        c = C.get(r["wave"], {}).get(k)
        if (c19 == "") != (c is None):
            why.append("C* rated status")
        elif c is not None and round(c, 4) != round(float(c19), 4):
            why.append("C*")
        return why

    d4 = {}
    max_p = max_c = 0.0
    n_c_both = 0
    for r in t19:
        w = _differs_4dp(r)
        if w:
            d4[r["wave"] + "|" + r["substrate"] + "|" + r["brand"]] = w
        k = (r["substrate"], r["brand"])
        p = P.get(r["wave"], {}).get(k)
        if p is not None and math.isfinite(p):
            max_p = max(max_p, abs(float(r["P"]) - p))
        c19 = (r.get("C_star") or "").strip()
        c = C.get(r["wave"], {}).get(k)
        if c19 != "" and c is not None:
            n_c_both += 1
            max_c = max(max_c, abs(float(c19) - c))
    keys19 = {(r["wave"], r["substrate"], r["brand"]) for r in t19}
    keysp = {(r["wave"], r["substrate"], r["brand"]) for r in prof}

    doc = {
        "what": "P_Cstar_v1_9_cross_check (v1.11 section 2; v1.20 section 5 item 3), omitted by score_v1_20.run_stage_c",
        "status": "post-hoc completion of a pre-registered check the scorer omitted; dated 2026-11-22; never a verdict input",
        "run_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "code": "score_v1_11.run_stage_c _differs, copied verbatim (tolerance 1e-9)",
        "inputs": inputs,
        "P_Cstar_v1_9_cross_check": {"differences": diff, "rows_compared": len(t19)},
        "descriptive_at_v1_9_printed_precision_4dp": {
            "rows_differing": len(d4), "differences": d4,
            "max_abs_diff_P": max_p, "max_abs_diff_Cstar": max_c, "rows_with_Cstar_in_both": n_c_both},
        "keys": {"v1_9_rows": len(t19), "profiles_rows": len(prof), "keys_in_both": len(keys19 & keysp),
                 "only_v1_9": sorted("|".join(k) for k in keys19 - keysp),
                 "only_profiles": sorted("|".join(k) for k in keysp - keys19)},
    }
    OUT.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"rows {len(t19)}; exact-rule differences {len(diff)}; at 4 dp {len(d4)}; "
          f"max |dP| {max_p:.3g}; max |dC*| {max_c:.3g}; C* in both {n_c_both}; keys in both {len(keys19 & keysp)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
