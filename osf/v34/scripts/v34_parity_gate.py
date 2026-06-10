#!/usr/bin/env python3
"""
v34_parity_gate.py — OFFLINE t1-side parity gate for v0.34.

Recomputes per-model recall (and recognition) from the FROZEN t1 inputs through the
locked extraction (score_v0_31 / score_v33 reuse). HARD GATE — must pass before any
t2 acquisition API call.

  - v0.20/0.21/0.22: recomputed recall MUST reproduce
    osf/methodology/v1_7/data/v1_7_cpc.csv 'r_per_model' BIT-FOR-BIT (citeable anchor).
  - v0.19/0.23: reproduce the frozen per-model inputs as consumed by the v0.31->v0.33
    arc (counts_v19 / counts_v23). No external anchor; provenance-only. Brand counts
    must be 16 / 24 and every vector well-formed (length-6, integer 0..6).

Exit 0 = PASS (acquisition may proceed). Exit 1 = HALT.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / "aias" / "scripts"))
import score_v33 as S33

EXPECT_BRANDS = {"v0.19": 16, "v0.20": 24, "v0.21": 24, "v0.22": 24, "v0.23": 24}


def main() -> int:
    print("=== v0.34 offline t1-side parity gate ===\n")
    recall = S33.recall_counts()
    recog, v23_levels = S33.recognition_vectors()

    # --- anchored leg: v0.20/0.21/0.22 bit-for-bit vs v1.7 r_per_model -----------
    gate = S33.reconciliation_gate(recall)
    print(f"[anchored leg] v0.20/0.21/0.22 recall vs v1_7_cpc.csv r_per_model (by model)")
    print(f"  checked {gate['checked']} brand-units | mismatches {len(gate['mismatches'])} | "
          f"PASS={gate['passed']}")
    if not gate["passed"]:
        for m in gate["mismatches"][:5]:
            print(f"   MISMATCH {m['substrate']}/{m['brand']}: "
                  f"mine={m['mine_panel_order']} v1.7={m['v1_7_sorted_order']}")
        print("\nGATE FAILED (anchored leg). HALTING — no API call.")
        return 1

    # --- provenance leg: v0.19/0.23 frozen-input reproduction --------------------
    print(f"\n[provenance leg] v0.19/0.23 frozen per-model input reproduction "
          f"(counts_v19/counts_v23)")
    ok = True
    for k in ("v0.19", "v0.23"):
        counts, cells = recall[k]
        n = len(counts)
        wellformed = all(
            len(v) == 6 and all(isinstance(x, (int,)) or float(x).is_integer() for x in v)
            and all(0 <= x <= 6 for x in v)
            for v in counts.values()
        )
        good = (n == EXPECT_BRANDS[k]) and wellformed
        ok &= good
        print(f"  {k}: brands={n} (expect {EXPECT_BRANDS[k]}) | vectors well-formed "
              f"(len-6, int 0..6)={wellformed} | {'OK' if good else 'FAIL'}")
    print(f"  v0.23 recognition r_level set observed: {v23_levels}")

    # --- all-substrate brand-count sanity (the 112-unit omnibus) -----------------
    print(f"\n[omnibus sanity] per-substrate brand counts:")
    total = 0
    for k in ("v0.19", "v0.20", "v0.21", "v0.22", "v0.23"):
        counts, _ = recall[k]
        total += len(counts)
        flag = "" if len(counts) == EXPECT_BRANDS[k] else "  <-- UNEXPECTED"
        print(f"  {k}: {len(counts)}{flag}")
    print(f"  TOTAL brand units: {total} (expect 112)")
    ok &= (total == 112)

    if gate["passed"] and ok:
        print("\nPARITY GATE: PASS. Acquisition may proceed.")
        return 0
    print("\nGATE FAILED (provenance leg / brand counts). HALTING — no API call.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
