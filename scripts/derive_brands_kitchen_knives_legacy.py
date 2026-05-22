#!/usr/bin/env python3
"""Derive registries/brands_kitchen_knives.json (legacy schema) from
brands_kitchen_knives_v0.16.json (new schema).

run_aias_v2.py expects:
    {"category": "...", "registry_version": "...",
     "brands": [{"canonical": "...", "aliases": [...]}, ...]}

brands_kitchen_knives_v0.16.json has:
    {"schema_version": "v1.2", "pivot": {...},
     "panel": [{"display_name": "...", "brand_id": "...", ...}],
     "alternates": [...]}

This adapter:
  - Combines panel + alternates into a single flat brands list
  - Drops brands in DROP list (EXCLUDED_E1a primaries — measurement
    pipeline shouldn't extract them; if extractor surfaces them in
    LLM responses they'd inflate unknowns; they're confirmed absent
    from Trends signal regardless)
  - Pulls canonical = display_name
  - Looks up aliases from CURATED_ALIASES dict
  - Adds tradition from tradition_cell (extractor uses it for scoping)
  - Writes the legacy-schema JSON

Run:
    cd ~/aias
    python3 scripts/derive_brands_kitchen_knives_legacy.py
"""
import json
import sys
from pathlib import Path

AIAS = Path.home() / "aias"
SRC = AIAS / "registries" / "brands_kitchen_knives_v0.16.json"
DST = AIAS / "registries" / "brands_kitchen_knives.json"

if not SRC.exists():
    sys.exit(f"ERROR: {SRC} not found")

# Curated aliases per the handoff doc proposal.
# Keyed by display_name (matches v0.16's display_name field exactly).
CURATED_ALIASES = {
    # Japanese cell (panel)
    "Shun":            ["Shun", "Shun Cutlery", "Shun Classic", "Shun Premier"],
    "Global":          ["Global", "Global Knives", "Yoshikin Global"],
    "Miyabi":          ["Miyabi", "Miyabi Birchwood", "Zwilling Miyabi"],
    "Mac":             ["Mac", "Mac Knife", "Mac Knives", "Mac Professional"],
    "Tojiro":          ["Tojiro", "Tojiro DP", "藤次郎"],
    "Yoshihiro":       ["Yoshihiro", "Yoshihiro Cutlery"],

    # German cell (panel) — Wüsthof is pivot but also extracted from LLM responses
    "Wüsthof":         ["Wüsthof", "Wusthof", "Wüsthof Classic",
                        "Wüsthof Trident", "Wüsthof Classic Ikon"],
    "Zwilling J.A. Henckels": ["Zwilling J.A. Henckels", "Zwilling", "Henckels",
                                "J.A. Henckels", "Zwilling JA Henckels", "JA Henckels"],
    "Messermeister":   ["Messermeister"],
    "Güde":            ["Güde", "Gude", "Franz Güde"],
    "Friedr. Dick":    ["Friedr. Dick", "Friedrich Dick", "F. Dick", "Dick"],

    # French cell (panel — including Au Nain activated from alternates)
    "Sabatier":        ["Sabatier", "K Sabatier", "Sabatier knife",
                        "Thiers-Issard Sabatier"],
    "Opinel":          ["Opinel"],
    "Laguiole":        ["Laguiole", "Forge de Laguiole"],
    "Au Nain":         ["Au Nain", "Au Nain knife", "Au Nain Coutellerie"],

    # American cell (panel)
    "Cutco":           ["Cutco", "Cutco Cutlery"],
    "Dalstrong":       ["Dalstrong", "Dalstrong Shogun", "Dalstrong Gladiator"],
    "Misen":           ["Misen", "Misen knife"],
    "New West KnifeWorks": ["New West KnifeWorks", "New West", "NWK"],
    "Made In":         ["Made In", "Made In Cookware", "Made In knife"],

    # Chinese cell (panel — including Hengtai activated from alternates)
    "Sunlong":         ["Sunlong", "Sunlong knife"],
    "ZHEN":            ["ZHEN", "Zhen knife", "Zhen cleaver"],
    "Hengtai":         ["Hengtai", "Hengtai knife"],

    # Remaining alternates (not activated but included for extraction
    # coverage — LLM responses may mention them; they're known knife brands)
    "Masamoto":        ["Masamoto", "正本"],
    "Misono":          ["Misono"],
    "Tadafusa":        ["Tadafusa", "ただふさ"],
    "Schmidt Brothers": ["Schmidt Brothers", "Schmidt Bros"],
    "Robert Herder":   ["Robert Herder", "Windmühlenmesser"],
    "Goyon-Chazeau Le Thiers": ["Goyon-Chazeau", "Goyon Chazeau", "Le Thiers"],
    "Bob Kramer":      ["Bob Kramer", "Kramer", "Kramer by Zwilling"],
    "Hammer Stahl":    ["Hammer Stahl"],
    "Hu Si Chao":      ["Hu Si Chao"],
    "Dengjia":         ["Dengjia"],
}

# Drop list: EXCLUDED_E1a panel brands (confirmed absent from Trends).
# Note: these are panel members in the v0.16 registry but were excluded at
# Phase B E1a; their LLM mentions should still be valid (brand exists in
# the world even if Trends doesn't surface it), so we INCLUDE them with
# aliases. The pipeline filters at the rescale/scoring stage, not at
# extraction time.
INCLUDE_E1A_EXCLUDED = {
    "Nogent (Goyon-Chazeau)": ["Nogent", "Nogent Goyon-Chazeau",
                                "Goyon-Chazeau Nogent"],
    "CCK Chan Chi Kee":       ["CCK Chan Chi Kee", "CCK", "Chan Chi Kee",
                                "陳枝記", "Chan Chi Kee Cutlery"],
    "Shibazi (Shi Ba Zi Zuo)": ["Shibazi", "Shi Ba Zi Zuo", "十八子作", "18子作"],
}
CURATED_ALIASES.update(INCLUDE_E1A_EXCLUDED)

# Load v0.16 source
with SRC.open() as f:
    v16 = json.load(f)

print(f"Source: {SRC.name}")
print(f"  schema_version: {v16.get('schema_version')}")
print(f"  panel: {len(v16['panel'])} brands")
print(f"  alternates: {len(v16['alternates'])} brands")
print()

# Build flat brands list
brands_out = []
missing_aliases = []

for source_arr, role_label in [(v16["panel"], "panel"),
                                (v16["alternates"], "alternate")]:
    for b in source_arr:
        display_name = b["display_name"]
        tradition = b.get("tradition_cell", "unknown")

        if display_name in CURATED_ALIASES:
            aliases = CURATED_ALIASES[display_name]
        else:
            # Fallback: aliases = [display_name] only. Flag for review.
            aliases = [display_name]
            missing_aliases.append(f"{display_name} ({role_label})")

        brands_out.append({
            "canonical": display_name,
            "aliases": aliases,
            "tradition": tradition,
        })

if missing_aliases:
    print("⚠ Brands with only display_name as alias (no curation):")
    for m in missing_aliases:
        print(f"  - {m}")
    print()

# Construct legacy-schema output
legacy = {
    "category": "kitchen_knives",
    "registry_version": "kitchen_knives_v0.16_legacy_adapter_v1",
    "source_canonical": "brands_kitchen_knives_v0.16.json",
    "adapter_note": ("Derived from brands_kitchen_knives_v0.16.json "
                     "(new schema with panel/alternates) for compatibility "
                     "with run_aias_v2.py's legacy reader. v0.16 file "
                     "remains the canonical source; this file is a "
                     "regenerable build artifact."),
    "brands": brands_out,
}

# Verify Wüsthof present (must be — it's both pivot and panel member)
canonicals = [b["canonical"] for b in brands_out]
assert "Wüsthof" in canonicals, "Wüsthof missing from derived brands"

# If the symlink exists at DST, remove it first
if DST.is_symlink():
    DST.unlink()
    print(f"Removed existing symlink at {DST}")

with DST.open("w") as f:
    json.dump(legacy, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"Wrote: {DST}")
print(f"  brands: {len(brands_out)}")
print(f"  total aliases across all brands: {sum(len(b['aliases']) for b in brands_out)}")
print()
print("Verification — first 3 brands:")
for b in brands_out[:3]:
    print(f"  {b['canonical']:30s} aliases: {b['aliases']}")

print()
print("=" * 60)
print("Adapter run complete. Next: re-fire run_aias_v2.py.")
print()
print("If you re-edit brands_kitchen_knives_v0.16.json later, re-run")
print("this adapter to regenerate the legacy file.")
