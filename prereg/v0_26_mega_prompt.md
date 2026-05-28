# v0.26 — Amazon BSR Acquisition Protocol (Browser Automation)

> **This document replaces the standard LLM mega-prompt.** v0.26 does not run new LLM probes.
> C_P scores are reused from source phases. The acquisition target is Amazon Best Sellers Rank
> via automated browser extraction (Claude in Chrome).

---

## Overview

**Objective:** For each of 120 brands across 5 substrates, extract the Amazon Best Sellers Rank (BSR) of the brand's best-selling product in the pre-registered Amazon category.

**Method:** Claude in Chrome browser automation against amazon.com.

**Output:** One CSV per substrate + one master CSV. Schema: `substrate, brand, amazon_status, asin, product_title, bsr_rank, bsr_category, listing_url, acquisition_timestamp, notes`.

---

## Substrate × Category mapping

| Substrate | Source phase | Amazon category anchor | Search suffix |
|---|---|---|---|
| Kitchen Knives | v0.16 | Kitchen Knives & Accessories | kitchen knife |
| Premium Kitchenware | v0.17 | Cookware | cookware |
| Audiophile Headphones | v0.19 | Over-Ear Headphones | headphones |
| Skincare | v0.20 | Skin Care | skincare |
| Cosmetics | v0.21 | Makeup | makeup |

---

## Per-brand acquisition sequence

For each brand in the substrate registry:

### Step 1 — Search

Navigate to: `https://www.amazon.com/s?k={brand_name}+{search_suffix}`

Example: `https://www.amazon.com/s?k=Wüsthof+kitchen+knife`

### Step 2 — Identify best-selling product

From the search results page:
- Identify products attributed to the target brand (brand name in title or "by {brand}" attribution)
- If multiple products appear, note the first 3–5 results (Amazon default sort is "Featured" which correlates with sales velocity)
- Navigate to the product page of the top result

### Step 3 — Extract BSR

On the product detail page, locate the "Best Sellers Rank" field in the "Product information" or "Additional Information" section. Record:

- **ASIN:** from the URL or product information section
- **Product title:** full title as displayed
- **BSR rank:** numeric rank (e.g., `#1,247`)
- **BSR category:** the category string (e.g., `#1,247 in Kitchen Knives & Accessories`)
- **Listing URL:** the product page URL
- **Acquisition timestamp:** ISO 8601 UTC

### Step 4 — Best-of-N check

If the first product's BSR category doesn't match the pre-registered category anchor, or if a lower-ranked product in search results might have a better BSR:
- Check 1–2 additional products from the same brand
- Retain the single product with the lowest (best) BSR in the target category

### Step 5 — Absent-brand handling

If the search returns:
- Zero results → code as `amazon_status = absent`
- Only third-party/gray-market listings (not brand-authorized) → code as `absent`, note in `notes` field
- Results in a different category only (e.g., brand sells books but not knives) → code as `absent`

---

## Rate management

- **Delay between searches:** 3–5 seconds minimum
- **Delay between product page navigations:** 2–3 seconds
- **Session breaks:** If CAPTCHA triggers, pause and resume after clearing
- **Batch size:** Process one substrate at a time (24 brands), emit CSV, then proceed to next

---

## Output file naming

```
osf/v26/data/v26_bsr_kitchen_knives.csv
osf/v26/data/v26_bsr_premium_kitchenware.csv
osf/v26/data/v26_bsr_audiophile_headphones.csv
osf/v26/data/v26_bsr_skincare.csv
osf/v26/data/v26_bsr_cosmetics.csv
osf/v26/data/v26_bsr_master.csv          # all 5 merged, substrate column added
```

---

## Brand registries (source)

Brand lists are read from the locked registries of each source phase. No modifications.

| Substrate | Registry source |
|---|---|
| Kitchen Knives | `registries/v16_brand_registry.json` (or equivalent) |
| Premium Kitchenware | `registries/v17_brand_registry.json` |
| Audiophile Headphones | `registries/v19_brand_registry.json` |
| Skincare | `registries/v20_brand_registry.json` |
| Cosmetics | `registries/v21_brand_registry.json` |

The exact brand names used in search queries must match the registry entries verbatim to maintain traceability.

---

## Validation checks (post-acquisition)

1. **Completeness:** 24 rows per substrate CSV (listed + absent = 24)
2. **Schema compliance:** all 10 columns present; no nulls except `asin`, `product_title`, `bsr_rank`, `bsr_category`, `listing_url` for absent brands
3. **BSR plausibility:** no BSR = 0; all BSR > 0 for listed brands
4. **Category alignment:** BSR category string contains the pre-registered category anchor (fuzzy match acceptable — Amazon category strings vary)
5. **Timestamp continuity:** all timestamps within the declared 48-hour acquisition window
