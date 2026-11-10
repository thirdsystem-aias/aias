# AIAS v1.13 — Structured-data audit protocol (DRAFT r1, 2026-11-10) [NEW WEB DATA: audit]

Part II of the v1.13 pre-registration. **New web data**: runs only after its own lock (tag `v1.13-audit-r1`), the OSF anchor, and **24 hours after Pablo receives the locked text**. No paid model, no API key, no spend. Nothing in this file has been run; no website has been fetched while drafting it.

## 1. Units

The 112 brand units of the five omnibus registries (v0.19–v0.23), unchanged. v0.40's airline and retail-bank brands are **not** in Paper A; Paper B may add them under its own pre-registration. Phantom brands of the registries (if any carry a registry flag) are audited only for (6)–(8) (no domain is expected); their result is reported apart and never enters H7.

## 2. Official domain (D_b) — declared lookup rule

Built **before** the Part I lock and without fetching any brand page (it feeds Part I's own-domain class):

1. The runner writes, for each brand, the canonical official domain it serves to US visitors as known from the registry's source records and the runner's own knowledge, with a one-line source note; aliases (US-market variants, e.g. `…usa.com`; parent-brand domains only when the brand has no own site) are listed separately.
2. A second pass by a different agent session re-derives the list blind; disagreements are adjudicated by Pablo and logged before the freeze.
3. Frozen as `registries/brand_domains_v1_13.csv` (columns: `substrate, brand_id, domain, aliases, source_note, adjudicated`), SHA-256 in the Part I anchor.

During the audit (Stage A), each domain's home-page fetch records the final URL after redirects; the registrable domain of that final URL and Wikidata P856 are added as **verified aliases** for sensitivity S6 only.

## 3. Pages fetched (at most 3 per brand)

- **P1 home page**: `https://{domain}/`, following at most 5 redirects.
- **P2 about page**: the first same-site link in P1's HTML (document order) whose path matches `about|about-us|our-story|company|heritage|history|who-we-are`.
- **P3 product page**: the first same-site link in P1's HTML whose path matches `product|products|shop|collections|models|vehicles|lineup|spirits|whisky|whiskey|skincare|makeup|headphones`.
- No other page is fetched. Missing P2/P3 is recorded, not searched for.

## 4. Fetch rules

- **User agent:** `AIAS-StructuredDataAudit/1.13 (+https://osf.io/ec6wh)`; the same string is used to read `robots.txt`.
- **robots.txt:** fetched once per host before any page; parsed with Python `urllib.robotparser`; a disallowed page is not fetched and is recorded `robots_disallowed`. An unreachable `robots.txt` (4xx) means allowed; 5xx or timeout means **not fetched** (`robots_unavailable`).
- **Rate:** one request at a time per host, at least 10 s between requests to the same host, at most 1 request per second overall; timeout 20 s; one retry after 60 s on 5xx or timeout; no retry on 4xx; 403/429 recorded as `blocked`.
- **No rendering:** static HTML only (no JavaScript, no headless browser, no cookies, no login, no form submission, no consent clicks).
- **Window:** all fetches within 72 hours; start and end recorded. A second pass 7 days later re-fetches P1 only (stability descriptive).
- **Wikidata / Wikipedia:** the public Wikidata API (`wbsearchentities`, `wbgetentities`) at ≤ 1 request/s with the same user agent. QID rule: candidates for the exact brand name (en); keep candidates whose P31 includes brand, business, company, enterprise or a category-specific type (automobile manufacturer, cosmetics brand, distillery …; the QIDs are pinned in `registries/wikidata_types_v1_13.csv` before the lock); prefer the candidate whose P856 domain ∈ D_b; otherwise the candidate with an enwiki sitelink whose description names the category; ties or no candidate → `qid = none` after a logged adjudication by the runner, before SDRI is computed.

## 5. What is recorded and the index

Per page: requested and final URL, HTTP status, fetch time (UTC), SHA-256 of the HTML, robots decision. Raw HTML is kept locally and **not** deposited (copyright); the deposit holds the extracted structured data and hashes.

Extraction (deterministic, `score_v1_13.extract_structured_data`): JSON-LD `<script type="application/ld+json">` blocks (including `@graph` and nested nodes; `@type` as string or list; schema.org prefixes stripped), microdata `itemtype`, RDFa `typeof`. Recorded: the set of types, every `sameAs` URL on Organization/Brand nodes.

Indicators (binary, per brand):

| # | Indicator | Source |
|---|---|---|
| 1 | Organization or subtype (Corporation, LocalBusiness, OnlineStore, AutoDealer …: `classes` list pinned in the scorer) on P1 | P1 |
| 2 | Brand on P1–P3 | P1–P3 |
| 3 | Product or subtype (ProductModel, ProductGroup, Car, Vehicle, IndividualProduct) on P1–P3 | P1–P3 |
| 4 | ≥ 1 `sameAs` on an Organization/Brand node | P1–P3 |
| 5 | a `sameAs` to `wikidata.org` or `*.wikipedia.org` | P1–P3 |
| 6 | Wikidata item exists (adjudicated QID) | Wikidata |
| 7 | P856 of that item has its registrable domain in D_b | Wikidata |
| 8 | the item has an `enwiki` sitelink | Wikidata |

**SDRI** = 100 × (sum of 1–8)/8; **SDRI_site** = 100 × (sum of 1–5)/5; **SDRI_kg** = 100 × (sum of 6–8)/3. A brand whose P1 could not be fetched (blocked, robots, error) has SDRI_site = NOT RATED and enters H7 only through sensitivity (SDRI_kg alone); the share of such brands is reported (> 0.20 flagged).

## 6. Checks

AQ1 every brand has a domain row; AQ2 share of P1 fetched with status 200 (reported; < 0.80 flagged); AQ3 parse errors in JSON-LD (counted; a block that does not parse contributes nothing); AQ4 P1 re-fetch after 7 days: share of brands whose indicator set changed (reported).

## 7. Limitations

Static HTML misses structured data injected by JavaScript or tag managers; country redirects (geo-IP) may serve a non-US page; robots and bot protection can block the audit while allowing search crawlers; Wikidata is edited by the public and changes over time (snapshot date recorded).

## 8. TODO before the Part II lock

`audit_v1_13.py` (fetcher; must refuse to run without the `v1.13-audit-r1` tag, the anchor and a recorded receipt time ≥ 24 h old); `registries/wikidata_types_v1_13.csv`; dry run on a synthetic local HTTP fixture only.
