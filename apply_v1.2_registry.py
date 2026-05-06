"""
Apply registry v1.2 — add six additional traditional Japanese makers
discovered in v1.1 brands_unknown surfacing at material rates.

This is a registry-revision per protocol §2.4: the unknown-mentions list
from the v1.1 extraction surfaced these six makers with combined ~44
mentions. Each is unambiguously a traditional Japanese maker with limited
US-targeted English marketing — same boundary-condition profile as the
v1.1_added cohort. Adding them strengthens the H8 boundary set further.

Action:
  - Read registries/brands_knives.json (v1.1)
  - Archive as registries/brands_knives_v1.1.json (no overwrite if exists)
  - Add 6 brands to the brands array
  - Update metadata: registry_version, supersedes, v1_2_revision_notes
  - Write back to registries/brands_knives.json
"""

import json
import shutil
from pathlib import Path

BRANDS_PATH = Path("registries/brands_knives.json")
ARCHIVE_PATH = Path("registries/brands_knives_v1.1.json")

# The six additions, drawn from the v1.1 brands_unknown list with material counts.
# All are traditional Japanese makers per knife-domain knowledge.
ADDITIONS = [
    {
        "canonical": "Takeda",
        "tier": "challenger",
        "lineage": "japanese",
        "aliases": ["takeda", "takeda hamono"],
        "boundary_condition": "discourse_language_test",
        "boundary_set": "v1.2_added",
        "registry_note": "Boutique Japanese smith (Niimi/Okayama). Surfaced 10 times in v1.1 unknown-mentions list. Added in v1.2 as additional boundary-condition test."
    },
    {
        "canonical": "Yoshikane",
        "tier": "challenger",
        "lineage": "japanese",
        "aliases": ["yoshikane", "yoshikane hamono"],
        "boundary_condition": "discourse_language_test",
        "boundary_set": "v1.2_added",
        "registry_note": "Traditional Japanese maker (Sanjo). Surfaced 8 times in v1.1 unknown-mentions list."
    },
    {
        "canonical": "Kikuichi",
        "tier": "challenger",
        "lineage": "japanese",
        "aliases": ["kikuichi"],
        "boundary_condition": "discourse_language_test",
        "boundary_set": "v1.2_added",
        "registry_note": "Traditional Japanese maker (Nara). Surfaced 7 times in v1.1 unknown-mentions list."
    },
    {
        "canonical": "Nenox",
        "tier": "challenger",
        "lineage": "japanese",
        "aliases": ["nenox", "nenohi"],
        "boundary_condition": "discourse_language_test",
        "boundary_set": "v1.2_added",
        "registry_note": "Traditional Japanese maker (Sakai). Surfaced 7 times in v1.1 unknown-mentions list."
    },
    {
        "canonical": "Togiharu",
        "tier": "challenger",
        "lineage": "japanese",
        "aliases": ["togiharu"],
        "boundary_condition": "discourse_language_test",
        "boundary_set": "v1.2_added",
        "registry_note": "Traditional Japanese house brand (sold via Korin). Surfaced 6 times in v1.1 unknown-mentions list."
    },
    {
        "canonical": "Mazaki",
        "tier": "challenger",
        "lineage": "japanese",
        "aliases": ["mazaki"],
        "boundary_condition": "discourse_language_test",
        "boundary_set": "v1.2_added",
        "registry_note": "Boutique Japanese smith (Aichi). Surfaced 6 times in v1.1 unknown-mentions list."
    },
]


def main():
    if not BRANDS_PATH.exists():
        raise SystemExit(f"ERROR: registry not found at {BRANDS_PATH}")

    # Archive v1.1 if not already archived
    if not ARCHIVE_PATH.exists():
        shutil.copy(BRANDS_PATH, ARCHIVE_PATH)
        print(f"Archived v1.1 -> {ARCHIVE_PATH}")
    else:
        print(f"v1.1 archive already exists at {ARCHIVE_PATH} - skipping copy")

    with open(BRANDS_PATH) as f:
        registry = json.load(f)

    if registry.get("registry_version") != "knives_v1.1":
        raise SystemExit(f"ERROR: expected v1.1, found {registry.get('registry_version')}")

    existing_canonical = {b["canonical"] for b in registry["brands"]}
    new_additions = [a for a in ADDITIONS if a["canonical"] not in existing_canonical]
    skipped = [a["canonical"] for a in ADDITIONS if a["canonical"] in existing_canonical]

    if skipped:
        print(f"Already present, skipping: {', '.join(skipped)}")

    # Apply v1.2 metadata
    registry["registry_version"] = "knives_v1.2"
    registry["registry_date"] = "2026-05-06"
    registry["supersedes"] = (
        "knives_v1.1 (revised post-extraction per §2.4); "
        "knives_v1.0 (locked pre-registration)"
    )
    registry["v1_2_revision_notes"] = {
        "changed_from_v1_1": (
            f"Added {len(new_additions)} traditional Japanese makers as boundary-condition tests: "
            f"{', '.join(a['canonical'] for a in new_additions)}. "
            "Each surfaced in the v1.1 brands_unknown list at material rates "
            "(combined ~44 mentions). Per protocol §2.4, registry expansion is "
            "the standard response when unknown-mentions affect leaderboard interpretation."
        ),
        "preregistration_impact": (
            "H1-H7 thresholds and operational definitions unchanged. H8 v1.2 expanded "
            "set has 14 boundary-condition brands (vs v1.1's 8 and v1.0's 3). "
            "All three versions reported in v0.8 results for transparency. "
            "v1.0_locked remains the pre-registration anchor; v1.1 and v1.2 are "
            "post-registration revisions explicitly disclosed as such."
        )
    }

    # Append additions
    registry["brands"].extend(new_additions)

    with open(BRANDS_PATH, "w") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

    n_total = len(registry["brands"])
    n_japanese = sum(1 for b in registry["brands"] if b["lineage"] == "japanese")
    n_boundary = sum(1 for b in registry["brands"]
                      if b.get("boundary_condition") == "discourse_language_test")

    print()
    print("Registry upgraded to v1.2")
    print(f"  total brands:                {n_total}")
    print(f"  japanese:                    {n_japanese}")
    print(f"  boundary-condition tests:    {n_boundary}")
    print(f"  added in v1.2:               {len(new_additions)}")
    for a in new_additions:
        print(f"    + {a['canonical']}")


if __name__ == "__main__":
    main()
