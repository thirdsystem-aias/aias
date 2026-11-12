# AIAS v1.18 — Domain table: classification rules (r1 draft, frozen at the v1.18 lock)

Applies to every distinct registrable domain (v1.13 rule U1–U5, unchanged) found in `search.citations` or `search.sources` of t4's answered S1 category answers on N3. The table is `domain_table_v1_18.csv`, built by `build_domain_table_v1_18.py`; columns `domain, class, rule, retailer, alias_of, note`.

## Order of writing (declared honestly)

The classes, precedence T0–T3 and the class definitions C/L/R/E below were fixed in the lane's working plan and in the build script's docstring before any domain was hand-classified (2026-11-12, about 04:22–04:25 CT); the hand classification followed (about 04:25 CT); this document writes the same rules out in full afterwards (about 04:31 CT). No rule was changed after the classification was seen. The coordinator should weigh the audit (§5) with that order in mind.

## 1. Blindness

The coder saw only `outputs/prelock/domains_to_classify_cited_v1_18.txt`: the cited domains not in any registry D_b, sorted alphabetically, one per line, with no count, model, substrate, answer, brand, field label or v1.13 class. The coded brand rows (which answer names which brand) were not read by any v1.18 script before the lock, and no Grounding share (v1.13's G\* per brand, or any v1.18 estimand) was looked at. Registry brand names were used only by the automatic `alias_of` string match (§4), which reads the registry, not the answers.

## 2. Precedence (first match wins)

- **T0.** The domain is in D_b of any registry unit (`osf/methodology/v1_13/registries/brand_domains_v1_13.csv`, frozen at v1.13's lock; RESOLVED rows, domain and aliases): class `company`. For a given brand b, a domain in D_b is `focal`; this is computed per (answer, brand) pair, not stored in the table.
- **T1.** The domain is in one of v1.13's frozen class lists (`source_classes_v1_13.md`, plain domains): `retailer` → `listing` (and `retailer` = 1); `forum_ugc` → `review_social`; `news`, `review_editorial`, `reference` → `editorial_other`. Also the TLD rule: `.gov`, `.edu`, `.mil`, `.gov.uk`, `.ac.uk` and `wikipedia.org` → `editorial_other`. Mechanical; consistent with v1.13 (e.g. `wine-searcher.com` is `editorial_other` because v1.13 lists it as review/editorial).
- **T2.** Hand classification by the definitions in §3, from the domain and the coder's general knowledge only; no page was opened, nothing was searched.
- **T3.** Not recognised with confidence: `UNRESOLVED`. Never guessed. A domain that only appears in `sources` (not in `citations`) was not hand-classified in r1 and is `UNRESOLVED` with the note "sources-only" (§6).

## 3. Class definitions (T2)

- **company (C).** A site operated by a commercial business to present its own products, services or corporate information: producers and brand owners (including parent groups and importers or distributors presenting their portfolio), service businesses (clinics, agencies, software firms), and their newsrooms and blogs on their own domain. Not: retailers or marketplaces selling many brands (L); publishers, research or data firms, ratings or award businesses whose product is the content (E).
- **listing (L).** A third-party page that lists a business or its products with data the business supplies or can manage: multi-brand retailers and marketplaces, auction houses, subscription boxes, price or availability aggregators, directories, app stores and maps. `retailer` = 1 for retailers, marketplaces and auction houses (used by sensitivity S2).
- **review or social (R).** User-generated platforms: consumer review sites, forums, Q&A, social networks, video platforms and user-blog hosts.
- **editorial or other (E).** News and magazines, professional review publications and independent review blogs, trade media, newswires (press releases are company-written but published by the wire, as in v1.13's news list), reference works, government, universities, hospitals and other non-profits, trade associations, competitions and awards, research and data publishers, museums, digital-edition hosts; anything else that is clearly not C, L or R.
- **UNRESOLVED.** Anything the coder could not place with confidence, including hosting domains whose owner cannot be told from the domain (`amazonaws.com`, `squarespace.com`).

## 4. Aliases (`alias_of`)

An automatic, case-insensitive string match of each registry brand name (letters and digits only, at least 4 characters) inside the domain. It marks candidates only (e.g. `sennheiser-hearing.com` → Sennheiser; it also matches clubs and group sites that v1.13's rule D2 excludes). The primary analysis uses the frozen D_b and ignores `alias_of`; sensitivity S3 counts a domain as focal for a unit only when the domain's class is `company` and the unit is in its `alias_of`.

## 5. Audit (declared)

`draw_audit_sample_v1_18.py` draws 60 rows (seed 118003): 50 from the T2 rows, proportional to class (editorial_other 32, company 13, listing 4, review_social 1), and 10 from the T1 rows. `audit_sheet_v1_18.csv` gives the second coder (Pablo or a person he names) the domains only; `audit_key_v1_18.csv` holds the first coder's classes. The second coder classifies the 60 under §3 without the key and may open a domain's own home page (no answer, brand link or share is shown). The second coder is also given the 59 cited UNRESOLVED domains and may resolve any of them with a stated reason. Reported: raw agreement and Cohen's κ on the 60. If raw agreement on the 50 T2 rows is below 0.85, every T2 row is re-coded by the second coder before the lock and disagreements go to Pablo. Changes after the audit are logged in DEVIATIONS before the lock and change the table's SHA-256 in the manifest.

## 6. Coverage of the r1 draft

1,345 distinct domains appear in either field (339 in `citations`, 1,344 in `sources`); 33 of them are D_b domains (21 cited), and the table also carries the 104 D_b domains not seen (137 T0 rows in all). 1,312 domains outside D_b were listed. Of the 318 cited domains outside D_b: 55 by T1, 204 by T2, 59 UNRESOLVED; by class editorial_other 172, company 54, listing 27, review_social 6, UNRESOLVED 59 (17.4% of the 339 distinct cited domains). Of the 994 sources-only domains, 67 received T1 and 927 remain UNRESOLVED. The primary analysis (citations) needs only the cited rows; the `sources` sensitivity S5 is reported with its unresolved share unless the sources-only rows are classified before the lock.
