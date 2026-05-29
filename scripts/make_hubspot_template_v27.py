#!/usr/bin/env python3
"""
v0.27 I1 (HubSpot AEO Grader) manual-entry TEMPLATE generator.

Emits a BLIND per-brand entry sheet: brand_id + brand_name prefilled from the
canonical 24-brand list, all HubSpot fields blank. Deliberately omits every
AIAS-side value (recall_channel_som, R_cat/R_cult, cell, type-2 flag) so the
manual pull cannot be anchored to known AIAS scores. Cell / type-2 / AIAS joins
happen at SCORING time, against the registry + v0.27_aias_side.csv -- never on
the entry sheet.

I1 convergent variable (per r3 construct_alignment_rule): I1_sov (Share of Voice,
the category-competitive field). The /100 composite is brand-absolute -> recorded,
NOT correlated. Free Grader runs its own prompt set (no category scoping in the
free tier), so SoV is tool-default-frame -> I1 construct_match = 'loose', as
pre-registered.

Source of the brand list: v0.27_aias_side.csv (its verified projection of the
locked registry; we read brand_id + brand_name ONLY). Swap SRC to the registry
if preferred -- the 24 ids must match either way.
"""
import csv, sys, os

SRC = sys.argv[1] if len(sys.argv) > 1 else "osf/v27/data/v0.27_aias_side.csv"
OUT = sys.argv[2] if len(sys.argv) > 2 else "osf/v27/data/v0.27_I1_hubspot_entry_TEMPLATE.csv"

# Column order: identity (prefilled) -> fields (blank). I1_ prefix disambiguates
# from I2/I3 columns at join time. I1_sov is the convergent variable.
COLUMNS = [
    "brand_id",            # prefilled (blind key)
    "brand_name",          # prefilled (blind key)
    "I1_sov",              # CONVERGENT VARIABLE: Share of Voice (record as displayed)
    "I1_sov_form",         # 'percent' or 'subscore_0_10' -- which form I1_sov is in
    "I1_market_competition",
    "I1_sentiment",        # -100..+100 (or /40 subscore -- note form in I1_notes)
    "I1_presence_quality",
    "I1_brand_recognition",
    "I1_composite_100",    # brand-absolute /100 grade -- recorded, NOT convergent
    "I1_engines",          # default cross-validated panel
    "pull_timestamp",      # ISO; for +/-7d mutual window logging
    "null_flag",           # TRUE if grader returned no/insufficient data for the brand
    "I1_notes",
]

def load_brands(path):
    with open(path, newline="") as f:
        r = csv.DictReader(f)
        cols = r.fieldnames or []
        for need in ("brand_id", "brand_name"):
            if need not in cols:
                sys.exit(f"ERROR: source {path} missing required column '{need}'. "
                         f"Found: {cols}")
        rows = [(row["brand_id"], row["brand_name"]) for row in r]
    if not rows:
        sys.exit(f"ERROR: no brand rows read from {path}")
    return rows

def main():
    if not os.path.exists(SRC):
        sys.exit(f"ERROR: source not found: {SRC}")
    brands = load_brands(SRC)
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    with open(OUT, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(COLUMNS)
        for bid, bname in brands:
            row = [bid, bname] + [""] * (len(COLUMNS) - 2)
            row[COLUMNS.index("I1_engines")] = "GPT/Perplexity/Gemini (cross-validated)"
            w.writerow(row)
    print(f"wrote {OUT}: {len(brands)} brands, {len(COLUMNS)} columns")
    print("BLIND check -> no AIAS-side columns present:",
          not any(c in COLUMNS for c in
                  ("recall_channel_som", "R_cat", "R_cult", "cell",
                   "aias_composite", "type2_flag")))
    print("convergent variable column:", "I1_sov")

if __name__ == "__main__":
    main()
