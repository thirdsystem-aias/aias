# AIAS v0.40 probe set (FINAL)

Built by `osf/v40/scripts/build_probes_v0_40.py` from the registry outputs. 94 probes; 2,821 calls (registered design D7: on every probe, legacy 6 models x 3 runs + 1 Gemini 2.5 Flash pass at the v0.39 setting = 19, plus current 3 models x 3 runs search off = 9, so 28 x 94 = 2,632; search on, current 3 models x 1 run on the 63 recommendation and status probes, 3 x 63 = 189; i.e. 31 calls per recommendation or status probe and 28 per recognition probe). Locks at tag `v0.40-prereg-r1`.

Wording rules: one user turn, no system prompt; recommendation probes name no brand and say "US"; the generic probes feed RQ1; every ghost and every control gets one recognition (K) and one status (S) probe; a disambiguator from the FDIC institution record is added where another US bank uses the same name (D11).

## AG: Airline recommendation, generic (RQ1) (6)

| ID | Prompt |
|---|---|
| AG1 | What are the best airlines in the United States? |
| AG2 | Which airline should I fly for trips within the US? |
| AG3 | Can you recommend a few good US airlines? |
| AG4 | I'm booking a domestic flight in the US. Which airlines should I consider? |
| AG5 | What are the top US airlines for domestic travel? |
| AG6 | Which US airline would you recommend, and why? |

## AN: Airline recommendation, by need (6)

| ID | Prompt |
|---|---|
| AN1 | Which US airline is best for cheap fares? |
| AN2 | Which US airline has the best frequent flyer program? |
| AN3 | Which US airline is the most comfortable to fly in economy? |
| AN4 | Which US airline is the most reliable for on-time arrivals? |
| AN5 | Which US airline has the best customer service? |
| AN6 | Which US airline is best for flying with young children? |

## AR: Airline recommendation, by Census region (4)

| ID | Prompt |
|---|---|
| AR1 | I live in the Northeast of the United States. Which airline should I fly most of the time? |
| AR2 | I live in the Midwest of the United States. Which airline should I fly most of the time? |
| AR3 | I live in the South of the United States. Which airline should I fly most of the time? |
| AR4 | I live in the West of the United States. Which airline should I fly most of the time? |

## BG: Bank recommendation, generic (RQ1) (6)

| ID | Prompt |
|---|---|
| BG1 | What are the best banks in the United States? |
| BG2 | Which bank should I open a checking account with in the US? |
| BG3 | Can you recommend a few good US banks? |
| BG4 | I'm switching banks in the US. Which banks should I consider? |
| BG5 | What are the top US banks for everyday banking? |
| BG6 | Which US bank would you recommend, and why? |

## BN: Bank recommendation, by need (6)

| ID | Prompt |
|---|---|
| BN1 | Which US bank is best for a high-yield savings account? |
| BN2 | Which US bank has the lowest fees on checking accounts? |
| BN3 | Which US bank is best for a small business? |
| BN4 | Which US bank is best for a college student's first account? |
| BN5 | Which US bank is best for getting a mortgage? |
| BN6 | Which US bank has the most branches and ATMs across the country? |

## BR: Bank recommendation, by Census region (4)

| ID | Prompt |
|---|---|
| BR1 | I live in the Northeast of the United States. Which bank should I use? |
| BR2 | I live in the Midwest of the United States. Which bank should I use? |
| BR3 | I live in the South of the United States. Which bank should I use? |
| BR4 | I live in the West of the United States. Which bank should I use? |

## K: Recognition probe, one per ghost and per control (31)

| ID | Prompt |
|---|---|
| K_TZ | What is ATA Airlines? |
| K_NW | What is Northwest Airlines? |
| K_CO | What is Continental Airlines? |
| K_FL | What is AirTran Airways? |
| K_US | What is US Airways? |
| K_VX | What is Virgin America? |
| K_NK | What is Spirit Airlines? |
| K_HA | What is Hawaiian Airlines? |
| K_SY | What is Sun Country Airlines? |
| K_COMMERCE | What is Commerce Bank (Philadelphia)? |
| K_NORTHFORK | What is North Fork Bank? |
| K_LASALLE | What is LaSalle Bank? |
| K_WAMU | What is Washington Mutual? |
| K_COUNTRYWIDE | What is Countrywide Bank? |
| K_NATCITY | What is National City Bank? |
| K_WACHOVIA | What is Wachovia? |
| K_INGDIRECT | What is ING Direct? |
| K_SOVEREIGN | What is Sovereign Bank? |
| K_BBVACOMPASS | What is BBVA Compass? |
| K_SUNTRUST | What is SunTrust? |
| K_BBT | What is BB&T? |
| K_UNIONBANK | What is MUFG Union Bank? |
| K_SIGNATURE | What is Signature Bank (New York)? |
| K_FIRSTREPUBLIC | What is First Republic Bank? |
| K_BMOHARRIS | What is BMO Harris Bank? |
| K_SVB | What is Silicon Valley Bank? |
| K_DISCOVER | What is Discover Bank? |
| K_AA | What is American Airlines? |
| K_DL | What is Delta Air Lines? |
| K_JPMC | What is Chase Bank? |
| K_BAC | What is Bank of America? |

## S: Status probe, one per ghost and per control (31)

| ID | Prompt |
|---|---|
| S_TZ | Can I still book a flight with ATA Airlines? |
| S_NW | Can I still book a flight with Northwest Airlines? |
| S_CO | Can I still book a flight with Continental Airlines? |
| S_FL | Can I still book a flight with AirTran Airways? |
| S_US | Can I still book a flight with US Airways? |
| S_VX | Can I still book a flight with Virgin America? |
| S_NK | Can I still book a flight with Spirit Airlines? |
| S_HA | Can I still book a flight with Hawaiian Airlines? |
| S_SY | Can I still book a flight with Sun Country Airlines? |
| S_COMMERCE | Can I still open an account with Commerce Bank (Philadelphia)? |
| S_NORTHFORK | Can I still open an account with North Fork Bank? |
| S_LASALLE | Can I still open an account with LaSalle Bank? |
| S_WAMU | Can I still open an account with Washington Mutual? |
| S_COUNTRYWIDE | Can I still open an account with Countrywide Bank? |
| S_NATCITY | Can I still open an account with National City Bank? |
| S_WACHOVIA | Can I still open an account with Wachovia? |
| S_INGDIRECT | Can I still open an account with ING Direct? |
| S_SOVEREIGN | Can I still open an account with Sovereign Bank? |
| S_BBVACOMPASS | Can I still open an account with BBVA Compass? |
| S_SUNTRUST | Can I still open an account with SunTrust? |
| S_BBT | Can I still open an account with BB&T? |
| S_UNIONBANK | Can I still open an account with MUFG Union Bank? |
| S_SIGNATURE | Can I still open an account with Signature Bank (New York)? |
| S_FIRSTREPUBLIC | Can I still open an account with First Republic Bank? |
| S_BMOHARRIS | Can I still open an account with BMO Harris Bank? |
| S_SVB | Can I still open an account with Silicon Valley Bank? |
| S_DISCOVER | Can I still open an account with Discover Bank? |
| S_AA | Can I still book a flight with American Airlines? |
| S_DL | Can I still book a flight with Delta Air Lines? |
| S_JPMC | Can I still open an account with Chase Bank? |
| S_BAC | Can I still open an account with Bank of America? |

## Subjects of the K and S probes

| ID | Category | Role | Name in probe | Source of the name |
|---|---|---|---|---|
| TZ | airline | ghost | ATA Airlines | registry brand |
| NW | airline | ghost | Northwest Airlines | registry brand |
| CO | airline | ghost | Continental Airlines | registry brand |
| FL | airline | ghost | AirTran Airways | registry brand |
| US | airline | ghost | US Airways | registry brand |
| VX | airline | ghost | Virgin America | registry brand |
| NK | airline | ghost | Spirit Airlines | registry brand |
| HA | airline | control | Hawaiian Airlines | registry brand |
| SY | airline | control | Sun Country Airlines | registry brand |
| COMMERCE | bank | ghost | Commerce Bank (Philadelphia) | FDIC CERT 21140: Commerce Bank, National Association, Philadelphia, PA; https://api.fdic.gov/banks/institutions?filters=CERT:21140 |
| NORTHFORK | bank | ghost | North Fork Bank | registry brand |
| LASALLE | bank | ghost | LaSalle Bank | registry brand |
| WAMU | bank | ghost | Washington Mutual | registry brand |
| COUNTRYWIDE | bank | ghost | Countrywide Bank | registry alias |
| NATCITY | bank | ghost | National City Bank | registry alias |
| WACHOVIA | bank | ghost | Wachovia | registry brand |
| INGDIRECT | bank | ghost | ING Direct | registry brand |
| SOVEREIGN | bank | ghost | Sovereign Bank | registry brand |
| BBVACOMPASS | bank | ghost | BBVA Compass | registry brand |
| SUNTRUST | bank | ghost | SunTrust | registry brand |
| BBT | bank | ghost | BB&T | registry brand |
| UNIONBANK | bank | ghost | MUFG Union Bank | FDIC CERT 22826: MUFG Union Bank, National Association, San Francisco, CA; https://api.fdic.gov/banks/institutions?filters=CERT:22826 |
| SIGNATURE | bank | ghost | Signature Bank (New York) | FDIC CERT 57053: Signature Bank, New York, NY; https://api.fdic.gov/banks/institutions?filters=CERT:57053 |
| FIRSTREPUBLIC | bank | ghost | First Republic Bank | registry brand |
| BMOHARRIS | bank | ghost | BMO Harris Bank | registry alias |
| SVB | bank | ghost | Silicon Valley Bank | registry brand |
| DISCOVER | bank | control | Discover Bank | registry alias |
| AA | airline | incumbent | American Airlines | registry brand |
| DL | airline | incumbent | Delta Air Lines | registry brand |
| JPMC | bank | incumbent | Chase Bank | consumer name of the JPMorgan Chase holder |
| BAC | bank | incumbent | Bank of America | registry brand |
