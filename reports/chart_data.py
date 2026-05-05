"""
Data loader for all five Third System categories.
Loads the most-recent leaderboard CSV per category and provides a unified accessor.
"""

import csv
import glob
from collections import defaultdict


def _identify_category(brand_set):
    """Identify category by characteristic brand presence."""
    if "Asana" in brand_set or "Linear" in brand_set:
        return "PM"
    if "Nike" in brand_set or "Hoka" in brand_set:
        return "Running"
    if "California Olive Ranch" in brand_set or "Brightland" in brand_set:
        return "Olive Oil"
    if "CeraVe" in brand_set or "Drunk Elephant" in brand_set:
        return "Skincare"
    if "YNAB" in brand_set or "Monarch Money" in brand_set:
        return "Finance"
    return None


CATEGORY_LABELS = {
    "PM":        "Project Management Software",
    "Running":   "Running Shoes",
    "Olive Oil": "Premium Olive Oil",
    "Skincare":  "Premium Facial Skincare",
    "Finance":   "Personal Finance Apps",
}


def load_all_categories():
    """Returns dict: {category_key: [list of brand row dicts]}."""
    files = sorted(glob.glob("presence_index_v0.3_*.csv"))
    seen_categories = {}
    for path in reversed(files):
        with open(path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        if not rows:
            continue
        brand_set = {r["brand"] for r in rows}
        cat = _identify_category(brand_set)
        if cat and cat not in seen_categories:
            seen_categories[cat] = (path, rows)

    # Collapse to just rows
    result = {cat: data[1] for cat, data in seen_categories.items()}
    paths = {cat: data[0] for cat, data in seen_categories.items()}
    return result, paths


def load_enriched_for_category(category_key):
    """Find the most-recent enriched CSV matching the category."""
    enriched_files = sorted(glob.glob("results_enriched_*.csv"))
    target_brands = {
        "PM":        ["Asana", "Linear", "Notion"],
        "Running":   ["Nike", "Hoka", "Asics"],
        "Olive Oil": ["California Olive Ranch", "Brightland", "Cobram"],
        "Skincare":  ["CeraVe", "Drunk Elephant", "La Roche-Posay"],
        "Finance":   ["YNAB", "Monarch Money", "Empower"],
    }
    keywords = target_brands.get(category_key, [])

    for path in reversed(enriched_files):
        with open(path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        if not rows:
            continue
        sample = " ".join(r.get("brands_canonical", "") for r in rows[:20])
        if any(b in sample for b in keywords):
            return rows
    return None


def cep_brand_counts_for_category(category_key):
    """Returns ({cep: {brand: count}}, {cep: total_runs})."""
    rows = load_enriched_for_category(category_key)
    if not rows:
        return None, None

    cep_brand_counts = defaultdict(lambda: defaultdict(int))
    cep_runs = defaultdict(int)
    for r in rows:
        if not r.get("brands_canonical"):
            continue
        cep = r["cep"]
        cep_runs[cep] += 1
        seen = set()
        for b in r["brands_canonical"].split("|"):
            if b and b not in seen:
                seen.add(b)
                cep_brand_counts[cep][b] += 1
    return cep_brand_counts, cep_runs


if __name__ == "__main__":
    data, paths = load_all_categories()
    print("Found categories:")
    for cat, rows in data.items():
        print(f"  {cat}: {len(rows)} brands  ({paths[cat]})")
