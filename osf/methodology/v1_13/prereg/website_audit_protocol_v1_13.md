# AIAS v1.13 — Structured-data audit protocol (DRAFT r1, to be sent to Pablo for the 24-hour review, 2026-11-10) [NEW WEB DATA: audit]

Part II of the v1.13 pre-registration. **New web data**: runs only after its own lock (tag `v1.13-audit-r1`), the OSF anchor, and **24 hours after Pablo receives the locked text**. No paid model, no API key, no spend. Nothing in this file has been run against the web; no website has been fetched while drafting it. The script is `osf/methodology/v1_13/scripts/audit_v1_13.py`; its dry run reads synthetic fixtures only (§8).

## 1. Units

The 112 brand units of the five omnibus registries (v0.19–v0.23), unchanged. v0.40's airline and retail-bank brands are **not** in Paper A; Paper B may add them under its own pre-registration. The registries' phantom units are the five v0.22 cell D "Defunct" brands (Pontiac, Oldsmobile, Plymouth, Mercury, Saturn; `prereg/v0_22_registry.json`, tested as phantom brands by v0.22's H_Phantom_Defunct); they are audited only for indicators (6)–(8) (no own site is expected), reported apart, and never enter H7. Denon (v0.19), a Samsung-group brand since September 23, 2025 (pre-registration §11), is audited like every other brand: same pages, same rules.

## 2. Official domain (D_b) — frozen offline list

Built before the Part I lock, offline, and never looked up at analysis time (runner decision 1, 2026-11-10):

1. For each registry unit, the registrable domain (U2/U4 of `source_classes_v1_13.md`) of the brand's official-site URL as given by a dated, citable public record, by the decision rules D1–D6 of the pre-registration (§2.3): Wikidata P856 of the brand's own item; else the English Wikipedia infobox website; else web-search results listing pages on the brand's own domain (results read, not opened), corroborated where needed by a third-party directory. Each row carries its source and access date. URLs that occur only inside model answers are not records. No brand page (and no robots.txt) is fetched to build or check the list.
2. A unit with no such record is **UNRESOLVED**; ambiguous units are listed with the reason, not guessed. The runner decides every UNRESOLVED and flagged row before the pre-registration is sent: a domain with its source, or **NONE** (no own domain). Each decision is written in the row's `runner_decision` column and logged in the pre-registration's change log.
3. Frozen as `registries/brand_domains_v1_13.csv` (columns: `substrate, brand_id, brand, coder_key, status, domain, aliases, source, ambiguity, runner_decision`; aliases `;`-separated), SHA-256 in the pre-registration (§2.3) and in both anchors. Status after the runner's decisions (2026-11-10; pre-registration §2.3, §12): 107 RESOLVED, 5 NONE (the five v0.22 cell D brands), 0 UNRESOLVED; SHA-256 `38198fdfa92ccff58dbba3fcc2e06930310a8df55d5933c9ca6d77646f9a855a`.

During the audit (Stage A), the registrable domain of P1's final URL after redirects and the domains of Wikidata P856 are recorded as **verified aliases** for sensitivity S6 only.

## 3. Pages fetched (at most 3 per brand)

- **P1 home page**: `https://{domain}/` for the unit's `domain` (aliases are not fetched), following at most 5 redirects.
- **P2 about page**: the first same-site link in P1's HTML (document order) whose path matches `about|about-us|our-story|company|heritage|history|who-we-are`.
- **P3 product page**: the first same-site link in P1's HTML, other than P2, whose path matches `product|products|shop|collections|models|vehicles|lineup|spirits|whisky|whiskey|skincare|makeup|headphones`.
- Details (fixed now): links are the `href` of `<a>` elements, resolved against P1's final URL, fragment dropped; same-site = same registrable domain as P1's final URL; a path matches when one of its segments equals a listed word or starts with it followed by `-`, `_` or `.`; links to `mailto:`, `tel:`, `javascript:` and paths matching `login|log-in|signin|sign-in|account|cart|checkout|register` are never selected.
- No other page is fetched. Missing P2/P3 is recorded, not searched for.

## 4. Fetch rules

- **User-Agent:** `AIAS research crawler; https://thirdsystem.ai` (it names the project and its site; no personal e-mail); the same string is used to read `robots.txt` and to call the Wikidata API.
- **robots.txt:** fetched once per scheme and host before any other request to that host (following at most 5 redirects); parsed with Python `urllib.robotparser` for this User-Agent; a disallowed page is not fetched and is recorded `robots_disallowed`. A 4xx answer for `robots.txt` means allowed; 5xx, timeout or error means **nothing is fetched from that host** (`robots_unavailable`). Every redirect hop is a request under the robots and rate rules of its own host.
- **Rate:** one request at a time; at least **10 s between requests to the same host** and at least 1 s between any two requests; timeout 20 s; one retry after 60 s on 5xx, timeout or connection error; no retry on 4xx; 403/429 recorded as `blocked`. At most the first 5,000,000 bytes of a response are read (truncation recorded); only `text/html` or `application/xhtml+xml` is parsed.
- **Public pages only:** GET requests only; no JavaScript, no headless browser, no cookies, no login, no form submission, no consent clicks.
- **Wikidata:** the public API (`wbsearchentities`, `wbgetentities`) is an API, not crawled pages: at most 3 requests per brand, each retried once at most (search; the candidates' claims, sitelinks and English descriptions; the English labels of their P31 values), one at a time, at most 1 per second, with the same User-Agent. QID rule: candidates whose English label (or matched alias) equals the registry name (after Unicode NFKC, case folding and straight apostrophes); kept if an English label of one of their P31 values contains a word listed in `registries/wikidata_types_v1_13.csv` (kind `p31_word`: brand, company, business, enterprise, manufacturer, distillery, marque); among them, exactly one whose P856 registrable domain is in D_b → that QID; otherwise exactly one with an `enwiki` sitelink whose English description has a word beginning with a category word of the unit's substrate (kind `description_word`) → that QID; several → **tie**, adjudicated by the runner (a QID among the tied, or none) and logged in `audit/qid_adjudication_v1_13.csv` (columns `substrate, brand_id, decision`) before SDRI is computed; none → `qid = none`. A failed API call after its retry leaves (6)–(8) NOT RATED for that brand (recorded).
- **Run window (declared now).** Pass 1 (P1–P3 and Wikidata) starts no sooner than 24 hours after Pablo receives the locked Part II text, and only if its 72-hour window ends before **2026-11-17 00:00 UTC**; otherwise it starts at or after **2026-11-22 12:00 UTC**. No request is sent between 2026-11-17 00:00 UTC and 2026-11-22 12:00 UTC (v0.40 collects Nov 17–21; this covers those days in any US time zone). Pass 2 re-fetches P1 only, 7 days after pass 1 started (stability descriptive); if that falls inside the blocked period, it runs at its end. Start and end of each pass are recorded (`audit/window_pass<k>.json`).
- **Mac load plan.** The audit runs on the collection Mac as one process, launched with `nice -n 10`: one connection at a time, at most 1 request per second, no model API and no API key, writing only under `osf/methodology/v1_13/audit/`. Its volume is at most 3 pages per brand (each with at most 5 redirects), one `robots.txt` per host and at most 3 Wikidata requests per brand. It makes no paid call and shares no files, keys or rate limits with a collection, so it may run while t4 (v0.42, Nov 11–13) or v1.12 (from Nov 14) collects. It can be stopped at any time without affecting a collection; a stopped pass is re-run from its start inside its window.

## 5. What is recorded and the index

Per page: requested and final URL, every redirect hop with its status and time (UTC), outcome (`ok`, `robots_disallowed`, `robots_unavailable`, `blocked`, `http_<code>`, `error`, `not_html`, `too_many_redirects`, `not_found` for a missing P2/P3), SHA-256 of the HTML. Raw HTML is kept locally under `audit/raw/` (git-ignored by a file the script writes there) and **not** deposited (copyright); the deposit holds the extracted structured data, the hashes and the Wikidata snapshot record (QID, rule, P856 values, sitelinks, time).

Extraction (deterministic, `audit_v1_13.extract_structured_data`): JSON-LD `<script type="application/ld+json">` blocks (including `@graph` and nested nodes; `@type` as string or list; schema.org prefixes stripped), microdata `itemscope`/`itemtype` and RDFa `typeof`. Recorded: the set of types, every `sameAs` URL on Organization/Brand nodes (JSON-LD properties, and microdata `itemprop` or RDFa `property` `sameAs` inside an Organization/Brand scope).

Indicators (binary, per brand):

| # | Indicator | Source |
|---|---|---|
| 1 | Organization or subtype (Corporation, LocalBusiness, OnlineStore, OnlineBusiness, AutoDealer, AutomotiveBusiness, Store, NGO, EducationalOrganization, SportsOrganization: the list pinned in the script) on P1 | P1 |
| 2 | Brand on P1–P3 | P1–P3 |
| 3 | Product or subtype (ProductModel, ProductGroup, IndividualProduct, SomeProducts, Car, Vehicle, Motorcycle) on P1–P3 | P1–P3 |
| 4 | ≥ 1 `sameAs` on an Organization/Brand node | P1–P3 |
| 5 | a `sameAs` whose host is `wikidata.org`, `wikipedia.org` or a subdomain of either | P1–P3 |
| 6 | Wikidata item exists (adjudicated QID) | Wikidata |
| 7 | P856 of that item has its registrable domain in D_b | Wikidata |
| 8 | the item has an `enwiki` sitelink | Wikidata |

**SDRI** = 100 × (sum of 1–8)/8; **SDRI_site** = 100 × (sum of 1–5)/5; **SDRI_kg** = 100 × (sum of 6–8)/3. A brand whose P1 could not be fetched (blocked, robots, error, too many redirects) has SDRI_site and SDRI NOT RATED and enters H7 only through sensitivity (SDRI_kg alone); the share of such brands is reported (> 0.20 flagged). Output: `audit/v1_13_sdri.csv` (`audit_v1_13.py --sdri`, offline, after the adjudications).

## 6. Checks

AQ1 every brand has a domain row, and none is UNRESOLVED; AQ2 share of P1 fetched with status 200 (reported; < 0.80 flagged); AQ3 parse errors in JSON-LD (counted; a block that does not parse contributes nothing); AQ4 P1 re-fetch after 7 days: share of brands whose indicator set (1)–(5) changed (reported).

## 7. Limitations

Static HTML misses structured data injected by JavaScript or tag managers; country redirects (geo-IP) may serve a non-US page; robots and bot protection can block the audit while allowing search crawlers; the audit reads only three pages per brand; Wikidata is edited by the public and changes over time (snapshot time recorded).

## 8. Run conditions and dry run

`audit_v1_13.py --collect` refuses unless: tag `v1.13-audit-r1` exists locally and on `origin`; `anchor/audit_anchor_v1_13.json` names the tag's commit and the SHA-256 of `brand_domains_v1_13.csv`, and the file matches it; `anchor/audit_receipt_v1_13.json` records when Pablo received the locked text, at least 24 hours earlier; no D_b row is UNRESOLVED; the clock is inside the window of §4. The local conditions are checked before the network is touched. `--dry-run` runs the whole audit on synthetic fixtures (`scripts/fixtures/audit/`: seven units under the reserved `.test` top-level domain and Wikidata items with impossible IDs) with every socket connection and name lookup refused; its record is `prereg/dry_run_audit_v1_13.txt` (2026-11-10: 0 network attempts, minimum gaps 10 s per site host and 1 s overall, every indicator as the fixtures expect). Tests: `scripts/tests/test_audit_v1_13.py`.
