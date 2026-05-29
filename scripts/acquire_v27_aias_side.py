#!/usr/bin/env python3
"""
v0.27 — AIAS-side derivation (inherited from v0.24 Phase B corpus)

Locked under v0.27-prereg-r2 (DEVIATIONS Entry 1/3):
  recall_channel_som = R_cat_scaled = (R_cat/36)*100   (pooled /36, NOT per-model-averaged)
  aias_composite     = v0.25 presence_composite        = mean(C_P_scaled, R_cat_scaled, R_cult_scaled)
  Recognition C_P    = Null-control channel (ceiling-expected on B2B SaaS)
  R_cult             = excluded from convergent SOM; retained in identity_load = R_cult - R_cat

This script does NOT re-implement the scoring. It imports score_v0_25.load_v24_presence()
verbatim (which contains the canonical block at score_v0_25.py:88-130) so the AIAS-side
variables are bit-for-bit identical to the v0.25 anchor (rho_Trends = 0.74).

Output: osf/v27/data/v0.27_aias_side.csv

Usage:
  python3 scripts/acquire_v27_aias_side.py
"""

import sys
from pathlib import Path

import pandas as pd

# Import the canonical v0.25 loader verbatim (same directory).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from score_v0_25 import load_v24_presence, V24_DATA  # noqa: E402

PIPELINE_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = PIPELINE_ROOT / "osf" / "v27" / "data"
OUT_CSV = OUT_DIR / "v0.27_aias_side.csv"


def count_unmapped_brand_ids():
    """
    Verification gate (prereg r2): the canonical block silently skips any
    brands_mentioned id absent from the Phase-A id_to_brand map
    (score_v0_25.py:102-103). Re-derive that skip set here so the count is
    explicit rather than silent. Computation is read-only and does not feed
    the AIAS-side variables.
    """
    df_a = pd.read_csv(V24_DATA / "v24_phase_a.csv")
    df_b = pd.read_csv(V24_DATA / "v24_phase_b.csv")
    id_to_brand = dict(zip(df_a["brand_id"], df_a["brand"]))

    skipped = {}
    for _, row in df_b.iterrows():
        if pd.isna(row["brands_mentioned"]):
            continue
        for bid in str(row["brands_mentioned"]).split(";"):
            bid = bid.strip()
            if not bid:
                continue
            if id_to_brand.get(bid) is None:
                skipped[bid] = skipped.get(bid, 0) + 1
    return skipped


def main():
    # --- canonical AIAS-side computation (verbatim via import) ---
    df = load_v24_presence()

    # registry-consistent brand_id (verified: Phase A ids == v27_registry ids, 1:1)
    da = pd.read_csv(V24_DATA / "v24_phase_a.csv")
    brand_to_id = dict(zip(da["brand"], da["brand_id"]))

    # --- map prereg-named variables onto the canonical columns ---
    out = pd.DataFrame({
        "brand_id": df["brand"].map(brand_to_id),
        "brand_name": df["brand"],
        "cell": df["cell"],
        "C_P": df["C_P"],                            # recognition (Null control), 0-6
        "recall_channel_som": df["R_cat_scaled"],    # PRIMARY: R_cat_scaled = (R_cat/36)*100
        "aias_composite": df["presence_composite"],  # SECONDARY: v0.25 presence_composite
        # traceability (not test variables)
        "R_cat": df["R_cat"],
        "R_cult": df["R_cult"],
        "R_cult_scaled": df["R_cult_scaled"],
        "identity_load": df["identity_load"],
    }).sort_values(["cell", "recall_channel_som"], ascending=[True, False]).reset_index(drop=True)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_CSV, index=False)

    # ----------------------------------------------------------------
    # Verification gates (render before the CSV is committed)
    # ----------------------------------------------------------------
    pd.set_option("display.width", 160)
    pd.set_option("display.max_rows", None)

    print("\n" + "=" * 78)
    print("v0.27 AIAS-side per-brand table  (osf/v27/data/v0.27_aias_side.csv)")
    print("=" * 78)
    show = out[["brand_id", "brand_name", "cell", "C_P", "recall_channel_som",
                "aias_composite", "R_cat", "R_cult", "identity_load"]].copy()
    show["recall_channel_som"] = show["recall_channel_som"].round(2)
    show["aias_composite"] = show["aias_composite"].round(2)
    print(show.to_string(index=False))

    n = len(out)
    print("\n" + "-" * 78)
    print(f"GATE 1 — Recognition ceiling (expect ~6/6, supports H_CV3_Recognition_Null)")
    print(f"  C_P distribution: {dict(out['C_P'].value_counts().sort_index())}")
    print(f"  mean C_P = {out['C_P'].mean():.3f} / 6   |   brands at 6/6: {(out['C_P']==6).sum()}/{n}")

    som = out["recall_channel_som"]
    print("\n" + "-" * 78)
    print(f"GATE 2 — recall_channel_som spread (range-restriction check, PRIMARY variable)")
    print(f"  min={som.min():.2f}  max={som.max():.2f}  range={som.max()-som.min():.2f}  "
          f"mean={som.mean():.2f}  sd={som.std(ddof=1):.2f}")
    print(f"  at floor (0): {(som==0).sum()}/{n}   at ceiling (100): {(som==100).sum()}/{n}")
    print(f"  IQR: {som.quantile(.25):.2f} – {som.quantile(.75):.2f}  "
          f"({'COMPRESSED — review' if som.std(ddof=1) < 10 else 'spread looks usable'})")

    print("\n" + "-" * 78)
    skipped = count_unmapped_brand_ids()
    total_skipped = sum(skipped.values())
    print(f"GATE 3 — brand-id skip count (expect 0 or explained)")
    if total_skipped == 0:
        print("  0 unmapped ids — every brands_mentioned id resolves via Phase-A map.")
    else:
        print(f"  {total_skipped} mention(s) across {len(skipped)} unmapped id(s): {skipped}")

    print("\n" + "=" * 78)
    print(f"rows: {n}   |   CSV written (NOT yet git-committed): {OUT_CSV}")
    print("=" * 78)


if __name__ == "__main__":
    main()
