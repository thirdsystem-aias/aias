# Arm A (SEO) r1: pre-lock notes (runner lane, 2026-11-24)

Notes only. The pre-registration text (`arm_a_seo_prereg_draft_r1.md`) is not changed. No paid call was made. Recommendations below that touch hypotheses, sample, calendar or limits are marked [CLOCK] (would restart Pablo's 24 h review).

## 1. The 8 TO CONFIRM domains (checked 2026-11-24, free HTTP requests from a cloud container + web search)

| Domain | Finding | Recommendation |
|---|---|---|
| mbusa.com | https://mbusa.com/ 301 to https://www.mbusa.com/, final https://www.mbusa.com/en/home (200); company, press, recall pages under it | keep (US extra) |
| bmwusa.com | no answer to plain requests (timeout, likely bot filter); search index shows the US site at https://www.bmwusa.com/ (dealer.html, accessibility.html, byo) and BMW Group press (press.bmwgroup.com/usa) | keep (US extra); live-HTTP check not possible from here |
| jaguarusa.com | https://jaguarusa.com/ 301 to www, then 302 to https://www.jaguarusa.com/en-us/index.html; search shows current offers pages on jaguarusa.com | keep (US extra); note some US dealer pages now sit under jaguar.com/en-us |
| marcus.com | HTTP 403 / timeout to scripts; search shows https://www.marcus.com/us/en/savings and /online-banking (Marcus: by Goldman Sachs) | keep as primary for BR-00470 |
| td.com | https://www.td.com/ 301 to /us/en/personal-banking/ (from the container; the redirect may be geo-dependent); https://www.tdbank.com/ redirects to https://www.td.com/us/en/personal-banking | keep td.com (tdbank.com is only a redirect); US content is a path, not a separate domain; flag as mixed US/Canada (already in §7) |
| bmo.com | https://bmo.com/ 301 to https://www.bmo.com/en-us/main/personal/; bmoharris.com no answer | keep bmo.com; US site is a path; mixed US/Canada |
| hsbc.com / us.hsbc.com | hsbc.com 301 to www.hsbc.com (global, 200); https://www.us.hsbc.com/ 200 | keep hsbc.com; us.hsbc.com only if DataForSEO documents subdomain targets (its doc does not, see §3) |
| firstcitizens.com | https://firstcitizens.com/ 301 to https://www.firstcitizens.com/ (200, title "Personal Banking, Credit Cards & Loans / First Citizens Bank") | keep |

All 8 resolve; none needs replacing. The blind non-Anthropic cross-check (§3.4 item 3) is still open (paid; not run).

## 2. Power simulation

Script `prereg/armA_power_sim.py`, output `prereg/armA_power_sim_out.txt`. Seed 20261124 (outside the proposed 610001+ range). 16,000 reps (H_A1, H_A5/H_A7), 4,000 reps x 2,000 within-group permutations (H_A2); 100,000-draw exact-shape permutation nulls. Runtime 30.4 s on the Mac (nice 19). Assumptions are listed in the script header (latent normal, no ties, equal effect in every category, all brands analysable, H_A2 size links).

See the output file for all rows. Key: H_A1 P(CONFIRMED) 0.504 at true rho 0.30, 0.807 at 0.40, 0.961 at 0.50 (draft approximation: about 0.5 and 0.95, confirmed). H_A2 P(CONFIRMED, Holm first step .025) 0.187 at partial 0.30, 0.411 at 0.50 (base case). H_A5/H_A7 power at 0.30: 0.215 at alpha .025, 0.136 at .0125.

Finding: H_A2's test as written (raw R permuted within group, partial on within-group ranks) rejects too often under the null: 0.037 at nominal .025 and 0.072 at .05 (base), 0.068 and 0.113 when size drives R, S and Gs strongly; mean partial at a true 0 is 0.04 to 0.08. A Freedman-Lane permutation (permute residuals of R on Gs within group) is the standard remedy. [CLOCK, probably: analysis-method change for a primary test; coordinator to decide.]

## 3. DataForSEO documentation (read 2026-11-24)

Sources: https://docs.dataforseo.com/v3/dataforseo_labs/google/historical_rank_overview/live/ and https://dataforseo.com/pricing/dataforseo-labs/historical-rank

- Endpoint and parameters match §4.1: `target` "without https:// and www.", `location_code` 2840, `language_code` "en", `date_from` yyyy-mm-dd, "if you don't specify this field, the data will be provided for the previous 6 months" (matches the 6-month test), "minimal possible value: 2020-10-01".
- Price: "$0.12 + $0.0012", per task + per item, "each item representing a month's worth of data"; the page's example (1,000 domains x 6 months = $127.2) matches. The §5.2 arithmetic is correct (76 x 0.1512 = 11.4912; 76 x 0.1236 = 9.3936; 76 x 0.1548 = 11.7648; total 32.6496).
- D5: history is documented back to 2020-10-01. Starting there instead of 2024-11-01 adds 49 months per full pull: 76 x 49 x 0.0012 = $4.47 per full pull (two full pulls in mode C: $8.94; total about $41.59). Not recommended inside this review; [CLOCK] if adopted.
- `date_to` exists (default today). Not needed; the draft's "no other parameter" and charged partial month stand.
- `include_clickstream_data` (default false) "you will be charged double the price for the request". This explains the null `clickstream_etv` in the test JSON. The §2.1 robustness measure cannot be non-null without doubling cost (mode C would be about $65.30, above the ceiling); the draft's 80% rule already drops it. No change needed; the reason can be stated.
- `correlate` (default true, "we recommend always setting correlate to true") and `ignore_synonyms` (default false) are left at defaults by "no other parameter".
- Not documented on the endpoint page: whether `target` may be a subdomain (us.hsbc.com) or whether subdomains are counted in a root target. Incremental mode: `date_from` is "starting date of the time range", which supports the assumption; the first-response month check in §5.4 still covers it.

## 4. Sales sources

| Category | Source in draft | Access check 2026-11-24 | Gap |
|---|---|---|---|
| Cars | Shift doc (`claude/shift-public-numbers-nov19.md`): per-brand named sources + KBB ATP | not re-checked here (checked 2026-11-19 per the draft) | several units are estimates (Cox, Automotive News) |
| Airlines | BTS T-100 Domestic Segment (U.S. Carriers), TranStats | free download page answers 200; "Latest Available Data: August 2026", so CY2025 is complete | carrier codes open; Alaska and Hawaiian got a single FAA operating certificate in late Oct 2025 (news.alaskaair.com release; airlinegeeks.com 2025-10-29), so Hawaiian may not report separately for Nov-Dec 2025 |
| Banks | FDIC BankFind, deposits at 2025-12-31 | free public API, no key (https://api.fdic.gov/banks/institutions, moved from banks.data.fdic.gov); test: First-Citizens Bank & Trust Company CERT 11063, active | certificates per bank open; UBS, HSBC, TD, BMO US deposits are small or subsidiary-only versus their global sites |
| B2B software | SEC EDGAR 10-K / 20-F by CIK | data.sec.gov API answers 200 (free; needs a User-Agent) | euro-rate source for SAP open (e.g. ECB reference rates, not checked) |
| Spirits | Impact Databank figures via Whisky Advocate, Vinetur, Market Watch | not checked; article URLs still open | descriptive only; Impact Databank itself may be paid (not verified) |

## 5. COI Entry 0: draft text (for DEVIATIONS Entry 0 at lock; not inserted into the pre-registration)

Based only on the r1 draft (§6.5, §8) and CLAUDE.md's COI section. Items marked TO CONFIRM are not findings.

> **DEVIATIONS Entry 0: pre-acquisition conflict-of-interest screen (Arm A).** This entry documents the COI handling for this arm's sample; it is not a finding that no brand is Samsung-affiliated.
> **Part A (categories).** The author's employer's categories are out of the sample: the technology-brands category (CAT-1020) is not pulled, and no phones, TVs, appliances, semiconductors or displays enter any test.
> **Part B (automotive, carried forward).** In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands: Harman International (audio systems), Samsung SDI (battery cells) and Samsung Display (infotainment), characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; v0.22 DEVIATIONS Entry 0, Part B). Carried forward unchanged.
> **Part C (agency work, carried forward).** Samsung's agency Cheil Worldwide, or its Iris unit, has worked for four brands in this sample: Chevrolet, BMW, Bentley and Jack Daniel's (v0.62 DEVIATIONS Entry 0, Part F). They are kept; every result is also reported without them (S-COI, §6.5).
> **Part D (registries not used).** The audiophile-headphones registry (AKG substituted with Denon before the v0.19 lock; Denon a Samsung-group brand since Harman's acquisition of Masimo's Sound United brands on September 23, 2025) and the brand Eucerin are not in this arm's sample.
> **Part E (airlines, retail banks, B2B software; first screen).** TO CONFIRM: result of the screen of the 11 airline, 26 bank and 12 software brands for Samsung-group relationships and Cheil Worldwide / Iris agency work, with sources. A flagged brand is kept and reported with and without it, unless Pablo decides otherwise (§6.5).
> Source records conformed: TO CONFIRM against the v0.22 locked Declarations and the v0.62 DEVIATIONS Entry 0, Part F (CLAUDE.md rule: conform from the locked record, not memory).
