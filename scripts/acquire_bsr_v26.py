#!/usr/bin/env python3
"""
v0.26 — Amazon BSR Acquisition Runner
AIAS Presence × Amazon Best Sellers Rank: Cross-Substrate Predictive Validity

Automated browser-based BSR extraction using Playwright.
Reads brand registries from source phases, searches Amazon, extracts BSR.

Usage:
    pip install playwright --break-system-packages
    playwright install chromium
    python3 scripts/acquire_bsr_v26.py [--substrate kitchen_knives] [--delay 4] [--dry-run]

Output:
    osf/v26/data/v26_bsr_{substrate}.csv   (per substrate)
    osf/v26/data/v26_bsr_master.csv        (merged)
"""

import argparse
import csv
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

AIAS_ROOT = Path(__file__).resolve().parent.parent  # ~/aias
OSF_DATA_DIR = AIAS_ROOT / "osf" / "v26" / "data"

SUBSTRATES = {
    "kitchen_knives": {
        "source_phase": "v0.16",
        "panel_source": {
            "type": "json_panel_array",
            "path": "registries/brands_kitchen_knives_v0.16.json",
            "json_path": ["panel"],
            "name_field": "display_name",
            "include_roles": ["panel", "alternate"],
        },
        "expected_n": 26,
        "verdicts_path": "osf/v16/v16_verdicts.json",
        "amazon_category": "Kitchen Knives & Accessories",
        "search_suffix": "kitchen knife",
    },
    "premium_kitchenware": {
        "source_phase": "v0.17",
        "panel_source": {
            "type": "json_cells_brands",
            "path": "registries/brands_kitchenware_v0.17.json",
            "name_field": "name",
        },
        "expected_n": 16,
        "verdicts_path": "osf/v17/v17_verdicts.json",
        "amazon_category": "Cookware",
        "search_suffix": "cookware",
    },
    "audiophile_headphones": {
        "source_phase": "v0.19",
        "panel_source": {
            "type": "csv_brand_column",
            "path": "osf/v19/panel_registry_v0_19.csv",
            "brand_column": "brand",
        },
        "expected_n": 16,
        "verdicts_path": "osf/v19/v19_verdicts.json",
        "amazon_category": "Over-Ear Headphones",
        "search_suffix": "headphones",
    },
    "skincare": {
        "source_phase": "v0.20",
        "panel_source": {
            "type": "csv_brand_column",
            "path": "osf/v20/phase_a_results.csv",
            "brand_column": "brand",
            "dedupe": True,
        },
        "expected_n": 24,
        "verdicts_path": "osf/v20/v20_verdicts.json",
        "amazon_category": "Skin Care",
        "search_suffix": "skincare",
    },
    "cosmetics": {
        "source_phase": "v0.21",
        "panel_source": {
            "type": "csv_brand_column",
            "path": "osf/v21/phase_a_results.csv",
            "brand_column": "brand",
            "dedupe": True,
        },
        "expected_n": 24,
        "verdicts_path": "osf/v21/v21_verdicts.json",
        "amazon_category": "Makeup",
        "search_suffix": "makeup",
    },
}

SEARCH_NAME_OVERRIDES = {
    # v0.16 — strip parenthetical disambiguation
    "Nogent (Goyon-Chazeau)": "Nogent Goyon-Chazeau",
    "Shibazi (Shi Ba Zi Zuo)": "Shibazi",
    "CCK Chan Chi Kee": "Chan Chi Kee",
    # v0.19 — prevent "ZMF Headphones headphones" doubling
    "ZMF Headphones": "ZMF",
}

CSV_FIELDNAMES = [
    "substrate",
    "brand",
    "amazon_status",
    "asin",
    "product_title",
    "bsr_rank",
    "bsr_category",
    "listing_url",
    "acquisition_timestamp",
    "notes",
]


# ---------------------------------------------------------------------------
# Registry loader
# ---------------------------------------------------------------------------

def load_brand_list(substrate_key: str) -> list[str]:
    """Load the locked brand panel from the source phase's canonical registry.

    Panel sizes are non-uniform across phases (v0.16=26 panel+activated-alts,
    v0.17=16, v0.19=16, v0.20=24, v0.21=24). Three loader strategies handle the
    three source formats encountered in the AIAS repo.
    """
    cfg = SUBSTRATES[substrate_key]
    src = cfg["panel_source"]
    path = AIAS_ROOT / src["path"]
    if not path.exists():
        print(f"  ERROR: Panel source not found: {path}")
        sys.exit(1)
    print(f"  Source: {src['path']} ({src['type']})")

    fmt = src["type"]
    if fmt == "json_panel_array":
        with open(path) as f:
            data = json.load(f)
        node = data
        for key in src.get("json_path", []):
            node = node[key]
        include_roles = set(src.get("include_roles", ["panel"]))
        name_field = src["name_field"]
        brands = [
            entry[name_field]
            for entry in node
            if entry.get("role", "panel") in include_roles
        ]
    elif fmt == "json_cells_brands":
        with open(path) as f:
            data = json.load(f)
        name_field = src["name_field"]
        brands = [
            entry[name_field]
            for cell in data["cells"].values()
            for entry in cell["brands"]
        ]
    elif fmt == "csv_brand_column":
        brands = []
        seen = set()
        with open(path) as f:
            reader = csv.DictReader(f)
            col = src["brand_column"]
            for row in reader:
                name = row[col]
                if src.get("dedupe") and name in seen:
                    continue
                seen.add(name)
                brands.append(name)
    else:
        print(f"  ERROR: Unrecognized panel source type: {fmt}")
        sys.exit(1)

    expected = cfg.get("expected_n")
    if expected is not None and len(brands) != expected:
        print(f"  WARNING: Expected {expected} brands, got {len(brands)} for {substrate_key}")
    return brands


# ---------------------------------------------------------------------------
# BSR extraction
# ---------------------------------------------------------------------------

def extract_bsr_from_page(page) -> dict | None:
    """Extract BSR data from an Amazon product detail page."""
    result = {}

    # ASIN from URL
    asin_match = re.search(r"/dp/([A-Z0-9]{10})", page.url)
    if asin_match:
        result["asin"] = asin_match.group(1)
    else:
        result["asin"] = ""

    # Product title
    try:
        title_el = page.query_selector("#productTitle")
        result["product_title"] = title_el.inner_text().strip() if title_el else ""
    except Exception:
        result["product_title"] = ""

    # BSR — multiple possible locations on Amazon product pages
    bsr_text = ""
    try:
        # Location 1: Product information table
        bsr_selectors = [
            "#detailBulletsWrapper_feature_div",
            "#productDetails_detailBullets_sections1",
            "#prodDetails",
            "th:has-text('Best Sellers Rank')",
        ]
        page_text = page.content()

        # Regex extraction from raw HTML — most reliable across page layouts
        bsr_patterns = [
            r'Best\s*Sellers\s*Rank[:\s]*</(?:th|span|td)>\s*<(?:td|span)[^>]*>\s*(?:<[^>]*>)*\s*#?([\d,]+)\s+in\s+([^<]+)',
            r'#([\d,]+)\s+in\s+([^<\(]+)',
        ]
        for pattern in bsr_patterns:
            matches = re.findall(pattern, page_text)
            if matches:
                # Take the first match (usually the broadest category)
                rank_str, category = matches[0]
                result["bsr_rank"] = int(rank_str.replace(",", ""))
                result["bsr_category"] = category.strip()
                return result

    except Exception as e:
        result["notes"] = f"BSR extraction error: {e}"

    return result if "bsr_rank" in result else None


def search_and_extract(page, brand: str, search_suffix: str, delay: float) -> dict:
    """Search Amazon for a brand and extract BSR from the best result."""
    brand_query = SEARCH_NAME_OVERRIDES.get(brand, brand)
    query = f"{brand_query} {search_suffix}"
    search_url = f"https://www.amazon.com/s?k={query.replace(' ', '+')}"

    record = {
        "brand": brand,
        "amazon_status": "absent",
        "asin": "",
        "product_title": "",
        "bsr_rank": "",
        "bsr_category": "",
        "listing_url": "",
        "acquisition_timestamp": datetime.now(timezone.utc).isoformat(),
        "notes": "",
    }

    try:
        # Step 1: Search
        page.goto(search_url, wait_until="domcontentloaded", timeout=15000)
        time.sleep(delay)

        # Check for CAPTCHA
        if "captcha" in page.url.lower() or page.query_selector("form[action*='captcha']"):
            record["notes"] = "CAPTCHA encountered — manual intervention needed"
            print(f"    ⚠ CAPTCHA for {brand} — pausing")
            input("    Press Enter after solving CAPTCHA in the browser...")
            page.goto(search_url, wait_until="domcontentloaded", timeout=15000)
            time.sleep(delay)

        # Step 2: Extract ASINs from search result cards
        result_cards = page.query_selector_all('[data-component-type="s-search-result"][data-asin]')
        asins = []
        for card in result_cards[:5]:
            asin = card.get_attribute('data-asin')
            if asin and asin.strip():
                asins.append(asin.strip())

        if not asins:
            record["notes"] = "No search results found"
            return record

        # Step 3: Visit product pages by ASIN, find best BSR
        best_bsr = None
        best_record = None

        for asin in asins[:3]:
            product_url = f"https://www.amazon.com/dp/{asin}"
            try:
                page.goto(product_url, wait_until="networkidle", timeout=15000)
            except Exception:
                page.goto(product_url, wait_until="domcontentloaded", timeout=15000)
            time.sleep(delay)

            bsr_data = extract_bsr_from_page(page)
            if bsr_data and "bsr_rank" in bsr_data:
                if best_bsr is None or bsr_data["bsr_rank"] < best_bsr:
                    best_bsr = bsr_data["bsr_rank"]
                    best_record = {
                        "amazon_status": "listed",
                        "asin": asin,
                        "product_title": bsr_data.get("product_title", ""),
                        "bsr_rank": bsr_data["bsr_rank"],
                        "bsr_category": bsr_data.get("bsr_category", ""),
                        "listing_url": product_url,
                        "notes": bsr_data.get("notes", ""),
                    }

            time.sleep(delay * 0.5)

        if best_record:
            record.update(best_record)
            record["acquisition_timestamp"] = datetime.now(timezone.utc).isoformat()
        else:
            record["notes"] = "Products found but no BSR extracted"

    except Exception as e:
        record["notes"] = f"Error: {e}"

    return record


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_substrate(substrate_key: str, delay: float, dry_run: bool) -> list[dict]:
    """Acquire BSR for every brand in the substrate's locked panel."""
    cfg = SUBSTRATES[substrate_key]
    print(f"\n{'='*60}")
    print(f"Substrate: {substrate_key} ({cfg['source_phase']})")
    print(f"Amazon category: {cfg['amazon_category']}")
    print(f"Search suffix: {cfg['search_suffix']}")
    print(f"{'='*60}")

    brands = load_brand_list(substrate_key)
    print(f"  Loaded {len(brands)} brands")

    if dry_run:
        print("  [DRY RUN] Would search Amazon for:")
        for b in brands:
            b_query = SEARCH_NAME_OVERRIDES.get(b, b)
            note = f"  (override: {b!r})" if b_query != b else ""
            print(f"    {b_query} {cfg['search_suffix']}{note}")
        return []

    # Launch browser
    from playwright.sync_api import sync_playwright

    records = []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,  # Visible browser — helps with CAPTCHA if needed
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 900},
        )
        page = context.new_page()

        # Initial Amazon visit to establish session
        page.goto("https://www.amazon.com", wait_until="domcontentloaded")
        time.sleep(3)

        n_brands = len(brands)
        for i, brand in enumerate(brands):
            print(f"\n  [{i+1}/{n_brands}] {brand}")
            record = search_and_extract(page, brand, cfg["search_suffix"], delay)
            record["substrate"] = substrate_key
            records.append(record)

            status = record["amazon_status"]
            bsr = record.get("bsr_rank", "—")
            print(f"    Status: {status} | BSR: {bsr}")

            # Longer delay every 8 brands to reduce detection risk
            if (i + 1) % 8 == 0 and i < n_brands - 1:
                pause = delay * 3
                print(f"    (cooling off {pause:.0f}s)")
                time.sleep(pause)

        browser.close()

    return records


def write_csv(records: list[dict], path: Path):
    """Write records to CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        writer.writerows(records)
    print(f"  Wrote {len(records)} rows → {path}")


def main():
    parser = argparse.ArgumentParser(description="v0.26 Amazon BSR acquisition")
    parser.add_argument(
        "--substrate",
        choices=list(SUBSTRATES.keys()) + ["all"],
        default="all",
        help="Which substrate to acquire (default: all)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=4.0,
        help="Base delay between requests in seconds (default: 4)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be searched without launching browser",
    )
    args = parser.parse_args()

    print(f"v0.26 BSR Acquisition Runner")
    print(f"Delay: {args.delay}s | Dry run: {args.dry_run}")
    print(f"Output dir: {OSF_DATA_DIR}")

    substrates_to_run = (
        list(SUBSTRATES.keys()) if args.substrate == "all" else [args.substrate]
    )

    all_records = []
    for sub in substrates_to_run:
        records = run_substrate(sub, args.delay, args.dry_run)
        if records:
            # Per-substrate CSV
            csv_path = OSF_DATA_DIR / f"v26_bsr_{sub}.csv"
            write_csv(records, csv_path)
            all_records.extend(records)

    # Master CSV
    if all_records:
        master_path = OSF_DATA_DIR / "v26_bsr_master.csv"
        write_csv(all_records, master_path)

    # Summary
    if all_records:
        listed = sum(1 for r in all_records if r["amazon_status"] == "listed")
        absent = sum(1 for r in all_records if r["amazon_status"] == "absent")
        print(f"\n{'='*60}")
        print(f"ACQUISITION COMPLETE")
        print(f"  Total brands: {len(all_records)}")
        print(f"  Listed: {listed} | Absent: {absent}")
        print(f"  Output: {OSF_DATA_DIR}")
        print(f"{'='*60}")


if __name__ == "__main__":
    main()
