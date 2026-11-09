# AIAS™ v0.40 brand registry, draft r1

**Study.** Leaders, challengers and ghosts. Two US categories reshaped by mergers and failures.

**Status.** Decisions adopted, not frozen. Pablo adopted every recommendation in section 6 on 2026-11-08. The freeze date goes in at lock: tag `v0.40-prereg-r1`, OSF deposit ec6wh → `v40/prereg/`, before any study probe.

**Built.** 2026-11-08 with `osf/v40/scripts/build_registry_v0_40.py build --freeze 2026-11-08 --status-check`, which also assembles this draft. The builder computes every share, floor test, window test and gap below. Only dates and their sources are entered by hand (`registries/exit_events.csv`, `registries/model_cutoffs.csv`), each with a URL and a source type.

## 1. What the registry holds

| | Airlines | Banks |
|---|---|---|
| Share measure | Revenue passenger miles, BTS T-100, 2025-08 to 2026-07 | Deposits, FDIC Summary of Deposits, 2026-06-30 |
| Current units | 11 brands in 10 share units | 25 holders |
| Ghosts (brand retired 2008-01-01 to freeze) | 7 | 17 |
| Living-brand controls | Hawaiian, Sun Country | Discover |
| Incumbent controls | American, Delta | Chase, Bank of America |

- Exit-to-cutoff gaps run from −36.2 months (SVB, GPT-4o) to 219.7 months (North Fork, Claude Opus 5.5); the smallest positive gap is 0.9 months (BMO Harris, GPT-4o). 19 of the 216 ghost × model pairs are exits after the model's cutoff: Spirit (eight models, all but Opus 5.5), SVB (all nine) and First Republic (GPT-4o and GPT-4o mini).
- An FDIC check of the 36 charters held by the 25 bank holders found no merger, failure or legal name change between the SOD date (2026-06-30) and 2026-11-08. The only events are three branch sales (Capital One, Regions, BMO).

## 2. Rules

- **R1 Unit.** Airlines: the consumer brand that sells the ticket. Banks: the FDIC top holder (RSSDHCR, or the charter's own RSSDID when it has no holding company), labelled with its consumer brand.
- **R2 Share.** Airlines: revenue passenger miles (passengers × distance) in BTS T-100 Domestic Segment (U.S. carriers), scheduled passenger service (CLASS F), latest 12 months. Banks: deposits in the FDIC Summary of Deposits, latest year.
- **R3 Floor.** At least 0.5% of the national total. Current units are measured at the latest count. Exits are measured at the last count before the exit: the carrier's last 12 months of separate T-100 reporting, or the last SOD in which the charter still carried the brand's stem.
- **R4 Window.** Brand-retirement date from 2008-01-01 to the freeze date, inclusive.
- **R5 Two dates per exit.** Legal date: the day the operating entity ended or changed its legal name. For banks that is the FDIC charter event (merger, failure, name change). For airlines it is the FAA single operating certificate, or the day operations ceased. Brand-retirement date: the day the issuer names for the brand's cutover or final conversion, or the final operation when none is named. The brand date is primary and the legal date is the sensitivity. Deal closings are kept as context only.
- **R6 Renames and charters.** A rename is an exit only when the distinctive name stem is dropped. Legal-form changes and internal consolidations that keep the stem are not exits. A brand's share sums every same-parent charter that carried its stem at that SOD; the builder sweeps for unlisted charters and found none.
- **R7 Regionals.** Operators never marketed under their own code in the BTS On-Time Marketing Carrier file for the same 12 months are regionals: 9E, C5, G7, MQ, OH, OO, PT, QX, YV and YX, 7.92% of RPM. Their RPM goes to the marketing brands in proportion to flight-miles. Exits of capacity-purchase regionals are not brand exits.
- **R8 Airline share units.** Hawaiian sits inside Alaska, because T-100 reports HA inside AS from 2026-01. Every other brand stands alone.
- **R9 Custody banks.** Excluded. EGRRCPA §402 and the 2019 SLR final rule apply only to BNY Mellon, Northern Trust and State Street (FDIC fact sheet, https://www.fdic.gov/news/fact-sheets/slr.pdf).
- **R10 Controls.** Living brands that went through a legal or ownership change, plus the top two incumbents in each category.
- **R11 Cutoffs.** Vendor-published only. For Claude, the training-data cutoff is primary and the reliable-knowledge cutoff is the alternative. A month-only cutoff means the last day of that month. Gap = cutoff minus exit date, in months of 30.4375 days; a negative gap means the exit came after the cutoff.
- **R12 Sources.** Every date carries a URL and a source type: primary is the issuer, a regulator or a filing; secondary is press or a reference work. Where the primary text survives only as a reproduction, the row says so.

## 3. Data and reproducibility

- BTS T-100 Domestic Segment (U.S. Carriers), 2007-01 to 2026-07: https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FIM&QO_fu146_anzr=Nv4%20Pn44vr45
- BTS On-Time: Marketing Carrier On-Time Performance (Beginning January 2018), monthly files 2025-08 to 2026-07: https://transtats.bts.gov/PREZIP/
- FDIC Summary of Deposits, 2005 to 2026: https://api.fdic.gov/banks/sod
- FDIC BankFind history and failures: https://api.fdic.gov/banks/history and https://api.fdic.gov/banks/failures
- Re-download test, 2026-11-08: SOD 2026, T-100 2026 and On-Time 2026-07 were fetched a second time. All three match the stored copies (same rows and totals; identical file for On-Time).

## 4. Registry tables (generated by the builder)

<!-- generated by build_registry_v0_40.py at 2026-11-09T00:09:08 UTC; do not edit by hand -->

#### Airlines: current brands (window 2025-08..2026-07)

| Code | Brand | Brand share % | Operating share % | Holder | Holder share % | Holder share % (SY in G4) | Status |
|---|---|---|---|---|---|---|---|
| AA | American Airlines | 21.11 | 17.74 | AA | 21.11 | 21.11 | current |
| DL | Delta Air Lines | 19.80 | 17.90 | DL | 19.80 | 19.80 | current |
| UA | United Airlines | 19.22 | 17.17 | UA | 19.22 | 19.22 | current |
| WN | Southwest Airlines | 17.08 | 17.08 | WN | 17.08 | 17.08 | current |
| AS | Alaska Airlines | 7.72 | 7.12 | AS | 8.51 | 8.51 | current |
| B6 | JetBlue | 4.63 | 4.63 | B6 | 4.63 | 4.63 | current |
| F9 | Frontier Airlines | 3.86 | 3.86 | F9 | 3.86 | 3.86 | current |
| G4 | Allegiant Air | 2.12 | 2.12 | G4 | 2.12 | 2.67 | current |
| MX | Breeze Airways | 0.80 | 0.80 | MX | 0.80 | 0.80 | current |
| HA | Hawaiian Airlines | 0.79 | 0.79 | AS | 8.51 | 8.51 | living control (brand retained, ownership/legal change) |
| SY | Sun Country Airlines | 0.55 | 0.55 | SY | 0.55 | 2.67 | living control (brand retained, ownership/legal change) |

Regional operators allocated: 9E, C5, G7, MQ, OH, OO, PT, QX, YV, YX (7.92% of RPM). On-Time months match T-100 window: True. Hawaiian's brand share covers 2025-08 to 2025-12 only, because T-100 reports it inside Alaska from 2026-01; use the holder share. The last column puts Sun Country inside Allegiant (sensitivity, D2).


#### Airlines: T-100 exit scan (stopped reporting, share >= 0.2% in last 12 months)

| Code | Carrier | First | Last | Share % (last 12 mo) | Class | Basis |
|---|---|---|---|---|---|---|
| HP | America West Airlines Inc. | 2007-01 | 2007-09 | 3.673 | brand | Stopped separate reporting 2007-09, before the window. |
| AQ | Aloha Airlines Inc. | 2007-01 | 2008-03 | 0.329 | brand | Share 0.329% < floor. |
| TZ | ATA Airlines d/b/a ATA | 2007-01 | 2008-04 | 0.686 | brand | Ghost. |
| YX (1) | Midwest Airline, Inc. | 2007-01 | 2009-09 | 0.212 | brand | Share 0.212% < floor. |
| NW | Northwest Airlines Inc. | 2007-01 | 2009-12 | 6.202 | brand | Ghost. |
| CO | Continental Air Lines Inc. | 2007-01 | 2011-12 | 7.368 | brand | Ghost. |
| XE (1) | ExpressJet Airlines Inc. | 2007-01 | 2011-12 | 1.462 | regional | Capacity-purchase operator for mainline partners. Lead to verify: some own-brand service in 2007-08. |
| XJ | Mesaba Airlines | 2007-01 | 2011-12 | 0.547 | regional | Capacity-purchase operator (verify partner brand from sources if challenged). |
| OH (1) | Comair Inc. | 2007-01 | 2012-09 | 0.328 | regional | Capacity-purchase operator (verify). |
| FL | AirTran Airways Corporation | 2007-01 | 2014-12 | 0.879 | brand | Ghost. |
| US | US Airways Inc. | 2007-01 | 2015-06 | 8.093 | brand | Ghost. |
| S5 | Shuttle America Corp. | 2007-01 | 2016-12 | 0.369 | regional | Capacity-purchase operator (verify). |
| VX | Virgin America | 2007-08 | 2018-03 | 1.868 | brand | Ghost. |
| CP (2) | Compass Airlines | 2007-05 | 2020-04 | 0.364 | regional | Capacity-purchase operator (verify). |
| HA | Hawaiian Airlines Inc. | 2007-01 | 2025-12 | 1.898 | brand | Living brand; T-100 reporting folded into AS from 2026-01 (control). |
| NK | Spirit Air Lines | 2007-01 | 2026-05 | 2.660 | brand | Ghost. |

#### Banks: current holders (SOD 2026, total deposits $19.05tn)

| Holder (FDIC) | Brand | Share % | Offices | Charters (CERT) |
|---|---|---|---|---|
| JPMORGAN CHASE & CO. | Chase (JPMorgan Chase) | 11.689 | 5142 | 628, 21761 |
| BANK OF AMERICA CORPORATION | Bank of America | 10.476 | 3599 | 3510, 25178 |
| WELLS FARGO & COMPANY | Wells Fargo | 8.206 | 4159 | 3511, 5146, 27389 |
| CITIGROUP INC. | Citi | 4.729 | 667 | 7213 |
| U.S. BANCORP | U.S. Bank | 2.797 | 2097 | 6548 |
| CAPITAL ONE FINANCIAL CORPORATION | Capital One | 2.690 | 245 | 4297 |
| MORGAN STANLEY | Morgan Stanley | 2.522 | 2 | 32992, 34221 |
| GOLDMAN SACHS GROUP, INC., THE | Goldman Sachs / Marcus | 2.484 | 5 | 33124 |
| PNC FINANCIAL SERVICES GROUP, INC., THE | PNC | 2.399 | 2401 | 6384 |
| TRUIST FINANCIAL CORPORATION | Truist | 2.201 | 1928 | 9846 |
| TORONTO-DOMINION BANK, THE | TD Bank | 1.600 | 1051 | 18409, 33947 |
| CHARLES SCHWAB CORPORATION, THE | Charles Schwab | 1.362 | 3 | 33497, 57450, 59108 |
| FIFTH THIRD BANCORP | Fifth Third | 1.262 | 1513 | 6672 |
| HUNTINGTON BANCSHARES INCORPORATED | Huntington | 1.192 | 1452 | 6560 |
| BANK OF MONTREAL | BMO | 1.019 | 989 | 16571, 58216 |
| CITIZENS FINANCIAL GROUP, INC. | Citizens | 0.991 | 971 | 57957 |
| FIRST CITIZENS BANCSHARES, INC. | First Citizens | 0.913 | 518 | 11063 |
| M&T BANK CORPORATION | M&T Bank | 0.904 | 998 | 588, 34069 |
| AMERICAN EXPRESS COMPANY | American Express | 0.901 | 1 | 27471 |
| KEYCORP | KeyBank | 0.832 | 951 | 17534 |
| ALLY FINANCIAL INC. | Ally | 0.822 | 1 | 57803 |
| HSBC HOLDINGS PLC | HSBC | 0.707 | 22 | 57890, 58188 |
| REGIONS FINANCIAL CORPORATION | Regions | 0.692 | 1245 | 12368 |
| UBS GROUP AG | UBS | 0.574 | 1 | 57565 |
| PINNACLE FINANCIAL PARTNERS, INC. | Pinnacle | 0.537 | 389 | 35583 |

Excluded by the custody rule (R9): BANK OF NEW YORK MELLON CORPORATION, THE 1.481%; STATE STREET CORPORATION 1.271%.


Just under the floor (0.40-0.50%): UNITED SERVICES AUTOMOBILE ASSOCIATION 0.483%; ROYAL BANK OF CANADA 0.473%; SYNCHRONY FINANCIAL 0.451%; WESTERN ALLIANCE BANCORPORATION 0.432%; BANCO SANTANDER, S.A. 0.415%; Zions Bancorporation, N.A. 0.402%.


#### Banks: SOD exit scan (renames and exits, share >= 0.4% at the last SOD under the old identity)

| Type | CERT | Old legal name | New legal name | Last SOD | Share % | Class | Reason / ghost ID |
|---|---|---|---|---|---|---|---|
| rename | 33143 | Treasury Bank, National Association | Countrywide Bank, National Association | 2005 | 0.516 | outside window | Rename in 2005. |
| rename | 33318 | MBNA America Bank, National Association | FIA Card Services, National Association | 2005 | 0.492 | below floor | MBNA America Bank -> FIA Card Services; 2005. |
| rename | 33143 | Countrywide Bank, National Association | Countrywide Bank, FSB | 2006 | 0.785 | not an exit | Legal-form change; stem 'Countrywide' kept (R6). |
| exit | 57443 | Citibank (West), FSB |  | 2006 | 0.617 | not an exit | Internal consolidation; stem 'Citibank' kept (R6); 2006. |
| exit | 26800 | AmSouth Bank |  | 2006 | 0.555 | outside window | Branches converted to Regions during 2007 (Regions 10-K FY2007 https://www.sec.gov/Archives/edgar/data/0001281761/000119312508038935/d10k.htm); last conversion 2007-12-06 (secondary). |
| rename | 27076 | World Savings Bank, FSB | Wachovia Mortgage, FSB | 2007 | 1.093 | outside window (edge) | World Savings: deposits moved to Wachovia and branches rebranded 2007-10-11 (secondary https://localwiki.org/davis/World_Savings_Bank); thrift renamed 2007-12-31 (FDIC). Decision D9. |
| exit | 21140 | Commerce Bank, National Association |  | 2007 | 0.599 | ghost | COMMERCE |
| exit | 15985 | North Fork Bank |  | 2007 | 0.568 | ghost | NORTHFORK |
| rename | 18409 | TD BankNorth, National Association | TD Bank, National Association | 2007 | 0.419 | below floor | TD Banknorth -> TD Bank (2008-05-31). |
| exit | 32633 | Washington Mutual Bank |  | 2008 | 2.612 | ghost | WAMU |
| exit | 33143 | Countrywide Bank, FSB |  | 2008 | 0.902 | ghost | COUNTRYWIDE |
| rename | 22826 | Union Bank of California, National Association | Union Bank, National Association | 2008 | 0.581 | not an exit | Union Bank of California -> Union Bank; stem 'Union Bank' kept (R6). |
| rename | 639 | The Bank of New York | The Bank of New York Mellon | 2008 | 0.492 | custody rule | The Bank of New York -> BNY Mellon (R9). |
| rename | 32992 | Morgan Stanley Bank | Morgan Stanley Bank, National Association | 2008 | 0.424 | not an exit | Legal-form change. |
| exit | 15407 | LaSalle Bank National Association |  | 2008 | 0.421 | ghost | LASALLE (with 22488) |
| exit | 33869 | Wachovia Bank, National Association |  | 2009 | 5.214 | ghost | WACHOVIA |
| exit | 6557 | National City Bank |  | 2009 | 1.338 | ghost | NATCITY |
| exit | 27374 | Merrill Lynch Bank USA |  | 2009 | 0.764 | brand persists | Merrill Lynch Bank USA merged into BofA 2009-07-01 (FDIC); the Merrill brand continues. Decision D10. |
| exit | 993 | Fifth Third Bank |  | 2009 | 0.548 | not an exit | Fifth Third charter consolidation; stem kept (verify FDIC record). |
| rename | 29950 | Sovereign Bank | Sovereign Bank, National Association | 2011 | 0.578 | not an exit | Legal-form change. |
| rename | 16571 | Harris National Association | BMO Harris Bank National Association | 2011 | 0.443 | not an exit | Harris -> BMO Harris; stem 'Harris' kept. |
| exit | 1020 | M&I Marshall and Ilsley Bank |  | 2011 | 0.411 | below floor | M&I merged into BMO Harris 2011-07-05 (FDIC). |
| exit | 35489 | ING Bank, fsb |  | 2012 | 0.963 | ghost | INGDIRECT |
| rename | 57957 | RBS Citizens, National Association | Citizens Bank, National Association | 2013 | 0.805 | not an exit | RBS Citizens -> Citizens Bank; stem 'Citizens' kept (R6). |
| rename | 29950 | Sovereign Bank, National Association | Santander Bank, N.A. | 2013 | 0.525 | ghost | SOVEREIGN |
| exit | 33318 | FIA Card Services, National Association |  | 2014 | 1.094 | not a consumer brand | FIA Card Services: Bank of America's card charter (verify). |
| rename | 22826 | Union Bank, National Association | MUFG Union Bank, National Association | 2014 | 0.803 | not an exit | Union Bank -> MUFG Union Bank; stem kept. |
| rename | 19048 | Compass Bank | BBVA USA | 2018 | 0.573 | ghost | BBVACOMPASS |
| rename | 2270 | ZB, National Association | Zions Bancorporation, N.A. | 2018 | 0.438 | below floor | ZB -> Zions Bancorporation. |
| rename | 57450 | Charles Schwab Bank | Charles Schwab Bank, SSB | 2019 | 1.524 | not an exit | Legal-form change. |
| rename | 9846 | Branch Banking and Trust Company | Truist Bank | 2019 | 1.314 | ghost | BBT |
| exit | 867 | SunTrust Bank |  | 2019 | 1.269 | ghost | SUNTRUST |
| rename | 6672 | Fifth Third Bank | Fifth Third Bank, National Association | 2019 | 1.014 | not an exit | Legal-form change. |
| rename | 27471 | American Express National  Bank | American Express National Bank | 2019 | 0.565 | not an exit | Spelling of the legal name. |
| exit | 19048 | Bbva Usa |  | 2021 | 0.477 | below floor | BBVA USA merged into PNC 2021-10-08 (FDIC); covered by the BBVA Compass ghost (D7). |
| exit | 30746 | E*trade Bank |  | 2021 | 0.409 | below floor | E*TRADE Bank. |
| exit | 24735 | Silicon Valley Bank |  | 2022 | 0.964 | ghost | SVB |
| exit | 59017 | First Republic Bank |  | 2022 | 0.913 | ghost | FIRSTREPUBLIC |
| rename | 27471 | American Express National Bank | American Express National  Bank | 2022 | 0.576 | not an exit | Spelling of the legal name. |
| exit | 57053 | Signature Bank |  | 2022 | 0.574 | ghost | SIGNATURE |
| exit | 22826 | Mufg Union Bank, National Association |  | 2022 | 0.509 | ghost | UNIONBANK |
| exit | 33954 | Capital One Bank (Usa), National Association |  | 2022 | 0.469 | below floor | Capital One charter consolidation. |
| exit | 3514 | Bank of The West |  | 2022 | 0.442 | below floor | Bank of the West merged into BMO Harris 2023-02-02 (FDIC). |
| rename | 16571 | BMO Harris Bank National Association | BMO Bank National Association | 2023 | 1.171 | ghost | BMOHARRIS |
| exit | 5649 | Discover Bank |  | 2024 | 0.644 | control | DISCOVER (brand retained). |
| rename | 57565 | UBS Bank USA | UBS Bank USA, National Association | 2025 | 0.544 | not an exit | Legal-form change. |

#### Airline ghosts

| ID | Brand | Share % | Legal date | Brand-retirement date | Successor | Brand-date source | In registry |
|---|---|---|---|---|---|---|---|
| TZ | ATA Airlines | 0.686 | 2008-04-03 | 2008-04-03 | none (ceased operations) | primary (reproduced) + secondary | True |
| NW | Northwest Airlines | 6.202 | 2009-12-31 | 2010-01-31 | Delta Air Lines | primary + secondary | True |
| CO | Continental Airlines | 7.368 | 2011-11-30 | 2012-03-03 | United Airlines | primary | True |
| FL | AirTran Airways | 0.879 | 2012-03-01 | 2014-12-28 | Southwest Airlines | primary | True |
| US | US Airways | 8.093 | 2015-04-08 | 2015-10-17 | American Airlines | secondary (issuer notice reproduced) | True |
| VX | Virgin America | 1.868 | 2018-01-11 | 2018-04-25 | Alaska Airlines | primary + secondary | True |
| NK | Spirit Airlines | 2.660 | 2026-05-02 | 2026-05-02 | none (wind-down) | secondary (issuer statement quoted) | True |

#### Bank ghosts

| ID | Brand | Share % | Legal date | Brand-retirement date | Successor | Brand-date source | In registry |
|---|---|---|---|---|---|---|---|
| COMMERCE | Commerce Bank (NJ) | 0.666 | 2008-05-31 | 2008-11-01 | TD Bank | primary | True |
| NORTHFORK | North Fork Bank | 0.568 | 2007-08-01 | 2008-03-10 | Capital One | primary | True |
| LASALLE | LaSalle Bank | 0.777 | 2008-10-17 | 2008-05-05 | Bank of America | secondary | True |
| WAMU | Washington Mutual | 2.680 | 2008-09-25 | 2009-10-25 | JPMorgan Chase | primary (reproduced, month) + secondary (day) | True |
| COUNTRYWIDE | Countrywide | 0.902 | 2009-04-27 | 2009-04-27 | Bank of America | primary (reproduced) + secondary | True |
| NATCITY | National City | 1.338 | 2009-11-06 | 2010-06-14 | PNC | primary | True |
| WACHOVIA | Wachovia | 5.404 | 2010-03-20 | 2011-10-15 | Wells Fargo | primary | True |
| INGDIRECT | ING Direct | 0.963 | 2012-11-01 | 2013-02-01 | Capital One 360 / Capital One | secondary (issuer FAQ quoted for month) | True |
| SOVEREIGN | Sovereign Bank | 0.525 | 2013-10-17 | 2013-10-17 | Santander Bank | primary | True |
| BBVACOMPASS | BBVA Compass | 0.573 | 2019-06-10 | 2019-06-10 | BBVA USA, then PNC (2021) | primary | True |
| SUNTRUST | SunTrust | 1.269 | 2019-12-07 | 2022-02-22 | Truist | secondary (issuer statement quoted) + primary (quarter) | True |
| BBT | BB&T | 1.314 | 2019-12-07 | 2022-02-22 | Truist | secondary + primary | True |
| UNIONBANK | Union Bank (MUFG Union Bank) | 0.509 | 2023-05-26 | 2023-05-30 | U.S. Bank | primary | True |
| SIGNATURE | Signature Bank | 0.574 | 2023-03-12 | 2023-03-20 | Flagstar Bank | primary | True |
| FIRSTREPUBLIC | First Republic Bank | 0.913 | 2023-05-01 | 2024-05-25 | JPMorgan Chase | primary | True |
| BMOHARRIS | BMO Harris | 1.171 | 2023-09-03 | 2023-09-03 | BMO | primary + secondary | True |
| SVB | Silicon Valley Bank | 0.964 | 2023-03-10 | 2026-10-06 | First Citizens Innovation Banking (First Citizens Bank) | primary | True |

#### Living-brand controls

| Category | ID | Brand | Share % (last separate count) | Legal/ownership date | Owner now |
|---|---|---|---|---|---|
| airline | HA | Hawaiian Airlines | 1.898 | 2025-10-29 | Alaska Air Group (brand kept) |
| airline | SY | Sun Country Airlines | 0.545 | 2026-05-13 | Allegiant Travel Co. (brand kept for now) |
| bank | DISCOVER | Discover | 0.644 | 2025-05-18 | Capital One (brand kept) |

#### Model cutoffs (vendor pages, retrieved 2026-11-08)

| Arm | Model | API ID | Primary cutoff | Date | Alt (reliable) | Lifecycle |
|---|---|---|---|---|---|---|
| legacy | Claude Opus 4.5 | claude-opus-4-5 | Training data cutoff | 2025-08 | 2025-05 | Active (legacy); retirement not sooner than 2026-11-24 |
| legacy | Claude Sonnet 4.5 | claude-sonnet-4-5 | Training data cutoff | 2025-07 | 2025-01 | Deprecated; retires 2026-11-30 |
| legacy | GPT-4o | gpt-4o | Knowledge cutoff | 2023-10-01 |  | Deprecated (notice 2026-10-14); shutdown 2027-01-14 |
| legacy | GPT-4o mini | gpt-4o-mini | Knowledge cutoff | 2023-10-01 |  | Deprecated (notice 2026-10-14); shutdown 2027-01-14 |
| legacy | Gemini 2.5 Flash | gemini-2.5-flash | Knowledge cutoff | 2025-01 |  | Not deprecated; no shutdown date; access limited to prior users (Gemini API) |
| legacy | Gemini 2.5 Flash-Lite | gemini-2.5-flash-lite | Knowledge cutoff | 2025-01 |  | Not deprecated; no shutdown date; access limited to prior users (Gemini API) |
| current | Claude Opus 5.5 | claude-opus-5-5 | Training data cutoff | 2026-06 | 2026-06 | Active (latest); released 2026-09-22 |
| current | GPT-6 Astra | gpt-6-astra | Knowledge cutoff | 2026-04-30 |  | Current |
| current | Gemini 4 Argon | gemini-4-argon | Knowledge cutoff | 2026-03 |  | Stable (model page, latest update Oct 2026) |

#### Exit-to-cutoff gap, months (model cutoff minus brand-retirement date; negative = exit after cutoff)

| category | ghost | Claude Opus 4.5 | Claude Sonnet 4.5 | GPT-4o | GPT-4o mini | Gemini 2.5 Flash | Gemini 2.5 Flash-Lite | Claude Opus 5.5 | GPT-6 Astra | Gemini 4 Argon |
|---|---|---|---|---|---|---|---|---|---|---|
| airline | TZ | 208.9 | 207.9 | 185.9 | 185.9 | 202.0 | 202.0 | 218.9 | 216.9 | 215.9 |
| airline | NW | 187.0 | 186.0 | 164.0 | 164.0 | 180.0 | 180.0 | 196.9 | 194.9 | 193.9 |
| airline | CO | 161.9 | 160.9 | 138.9 | 138.9 | 155.0 | 155.0 | 171.9 | 169.9 | 168.9 |
| airline | FL | 128.1 | 127.1 | 105.1 | 105.1 | 121.1 | 121.1 | 138.1 | 136.0 | 135.1 |
| airline | US | 118.5 | 117.5 | 95.5 | 95.5 | 111.5 | 111.5 | 128.4 | 126.4 | 125.4 |
| airline | VX | 88.2 | 87.2 | 65.2 | 65.2 | 81.2 | 81.2 | 98.2 | 96.2 | 95.2 |
| airline | NK | -8.0 | -9.0 | -31.0 | -31.0 | -15.0 | -15.0 | 1.9 | -0.1 | -1.1 |
| bank | COMMERCE | 202.0 | 200.9 | 179.0 | 179.0 | 195.0 | 195.0 | 211.9 | 209.9 | 208.9 |
| bank | NORTHFORK | 209.7 | 208.7 | 186.7 | 186.7 | 202.7 | 202.7 | 219.7 | 217.7 | 216.7 |
| bank | LASALLE | 207.9 | 206.9 | 184.9 | 184.9 | 200.9 | 200.9 | 217.8 | 215.8 | 214.8 |
| bank | WAMU | 190.2 | 189.2 | 167.2 | 167.2 | 183.2 | 183.2 | 200.1 | 198.1 | 197.2 |
| bank | COUNTRYWIDE | 196.1 | 195.1 | 173.1 | 173.1 | 189.2 | 189.2 | 206.1 | 204.1 | 203.1 |
| bank | NATCITY | 182.6 | 181.6 | 159.6 | 159.6 | 175.6 | 175.6 | 192.5 | 190.5 | 189.5 |
| bank | WACHOVIA | 166.5 | 165.5 | 143.5 | 143.5 | 159.6 | 159.6 | 176.5 | 174.5 | 173.5 |
| bank | INGDIRECT | 150.9 | 149.9 | 127.9 | 127.9 | 144.0 | 144.0 | 160.9 | 158.9 | 157.9 |
| bank | SOVEREIGN | 142.5 | 141.4 | 119.5 | 119.5 | 135.5 | 135.5 | 152.4 | 150.4 | 149.4 |
| bank | BBVACOMPASS | 74.7 | 73.7 | 51.7 | 51.7 | 67.7 | 67.7 | 84.7 | 82.7 | 81.7 |
| bank | SUNTRUST | 42.3 | 41.2 | 19.3 | 19.3 | 35.3 | 35.3 | 52.2 | 50.2 | 49.2 |
| bank | BBT | 42.3 | 41.2 | 19.3 | 19.3 | 35.3 | 35.3 | 52.2 | 50.2 | 49.2 |
| bank | UNIONBANK | 27.1 | 26.1 | 4.1 | 4.1 | 20.1 | 20.1 | 37.0 | 35.0 | 34.0 |
| bank | SIGNATURE | 29.4 | 28.4 | 6.4 | 6.4 | 22.4 | 22.4 | 39.4 | 37.4 | 36.4 |
| bank | FIRSTREPUBLIC | 15.2 | 14.2 | -7.8 | -7.8 | 8.2 | 8.2 | 25.2 | 23.2 | 22.2 |
| bank | BMOHARRIS | 23.9 | 22.9 | 0.9 | 0.9 | 17.0 | 17.0 | 33.9 | 31.9 | 30.9 |
| bank | SVB | -13.2 | -14.2 | -36.2 | -36.2 | -20.1 | -20.1 | -3.2 | -5.2 | -6.2 |

Ghost x model pairs with the exit after the cutoff (brand date): 19 of 216.


#### Sources by row (from registries/exit_events.csv and registries/model_cutoffs.csv)

- **TZ ATA Airlines** (ghost). Legal 2008-04-03 [primary (reproduced) + secondary]: ATA press release 2008-04-03 (original http://www.ata.com/about_ata/news/20080403.pdf, text reproduced at https://www.flyertalk.com/forum/southwest-airlines-rapid-rewards/808525-ata-ceases-operations-eff-04-03-2008-a.html); https://money.cnn.com/2008/04/03/news/companies/ata_bankruptcy/ Brand 2008-04-03 [primary (reproduced) + secondary]: same as legal_source
- **NW Northwest Airlines** (ghost). Legal 2009-12-31 [secondary]: https://www.mprnews.org/story/2009/12/31/nwa-delta Brand 2010-01-31 [primary + secondary]: https://ir.delta.com/news/news-details/2010/Delta-Completes-Integration-of-Northwest-Airport-and-Reservations-Systems-Northwest-Flight-Numbers-and-nwacom-Retired/default.aspx; https://www.eturbonews.com/27640/goodbye-northwest-airlines-web-site
- **CO Continental Airlines** (ghost). Legal 2011-11-30 [primary]: https://www.prnewswire.com/news-releases/faa-issues-single-operating-certificate-to-united-airlines-and-continental-airlines-134746913.html Brand 2012-03-03 [primary]: https://prnewswire.com/news-releases/united-airlines-issues-update-on-computer-system-conversion-141486943.html
- **FL AirTran Airways** (ghost). Legal 2012-03-01 [primary]: https://investors.southwest.com/news-events/press-releases/detail/1225/faa-issues-single-operating-certificate-to-southwest-airlines-and-airtran-airways Brand 2014-12-28 [primary]: https://investors.southwest.com/news-events/press-releases/detail/857/southwest-airlines-celebrates-final-scheduled-airtran-airways-flight
- **US US Airways** (ghost). Legal 2015-04-08 [primary]: https://news.aa.com/news/news-details/2015/American-Airlines-Receives-Single-Operating-Certificate/default.aspx Brand 2015-10-17 [secondary (issuer notice reproduced)]: https://flightglobal.com/american-reservations-integration-proceeds-smoothly/118571.article; https://csmonitor.com/layout/set/amphtml/Business/2015/1017/End-of-an-era-The-final-flight-of-US-Airways; American's customer notice reproduced at https://loyaltylobby.com/2015/07/13/american-airlines-us-airways-integration-update/
- **VX Virgin America** (ghost). Legal 2018-01-11 [primary]: https://news.alaskaair.com/newsroom/alaska-airlines-receives-single-operating-certificate-from-faa/ Brand 2018-04-25 [primary + secondary]: https://news.alaskaair.com/alaska-airlines/company-news/exciting-changes-are-touching-down; https://www.travelweekly.com/Travel-News/Airline-News/Final-Virgin-America-flights-departing-April-24
- **NK Spirit Airlines** (ghost). Legal 2026-05-02 [secondary (issuer statement quoted)]: Spirit statement quoted by https://fox35orlando.com/news/spirit-airlines-shuts-down-operations-all-flights-canceled and https://www.ctpublic.org/2026-05-02/spirit-airlines-ceases-operations-after-escalating-financial-struggles; https://www.ch-aviation.com/news/166772 Brand 2026-05-02 [secondary (issuer statement quoted)]: same as legal_source
- **HA Hawaiian Airlines** (control). Legal 2025-10-29 [primary]: https://www.prnewswire.com/news-releases/alaska-and-hawaiian-airlines-reach-major-integration-milestone-a-single-operating-certificate-302597953.html Brand retained [primary]: same
- **SY Sun Country Airlines** (control). Legal 2026-05-13 [primary]: Allegiant release of 2026-05-13: https://www.sec.gov/Archives/edgar/data/1362468/000114036126021056/ef20073018_ex99-1.htm (SEC filing, Exhibit 99.1); https://ir.allegiantair.com/news/news-details/2026/Allegiant-Completes-Acquisition-of-Sun-Country-Airlines-Creating-the-Leading-Leisure-Focused-U-S--Airline/default.aspx Brand retained [primary]: https://newsroom.allegiantair.com/press-releases/press-release-details/2026/Allegiant-Completes-Acquisition-of-Sun-Country-Airlines-Creating-the-Leading-Leisure-Focused-U-S--Airline/default.aspx
- **COMMERCE Commerce Bank (NJ)** (ghost). Legal 2008-05-31 [primary]: https://api.fdic.gov/banks/history?filters=CERT:21140 Brand 2008-11-01 [primary]: https://stories.td.com/ca/en/news/2008-10-31-video-b-roll-via-on-demand-and-satellite---welcome-to-td-ban
- **NORTHFORK North Fork Bank** (ghost). Legal 2007-08-01 [primary]: https://api.fdic.gov/banks/history?filters=CERT:15985 Brand 2008-03-10 [primary]: https://ir-capitalone.gcs-web.com/news-releases/news-release-details/capital-one-bank-comes-new-york-region
- **LASALLE LaSalle Bank** (ghost). Legal 2008-10-17 [primary]: https://api.fdic.gov/banks/history?filters=CERT:15407; https://api.fdic.gov/banks/history?filters=CERT:22488 Brand 2008-05-05 [secondary]: https://www.taipeitimes.com/News/worldbiz/archives/2008/05/06/2003411152 (Bloomberg)
- **WAMU Washington Mutual** (ghost). Legal 2008-09-25 [primary]: https://api.fdic.gov/banks/failures?filters=CERT:32633; https://jpmorganchaseco.gcs-web.com/news-releases/news-release-details/jpmorgan-chase-acquires-deposits-assets-and-certain-liabilities Brand 2009-10-25 [primary (reproduced, month) + secondary (day)]: JPM release reproduced at https://www.globalcustodian.com/?p=22131 ('13 months after'); day from https://daviswiki.org/Chase
- **COUNTRYWIDE Countrywide** (ghost). Legal 2009-04-27 [primary]: https://api.fdic.gov/banks/history?filters=CERT:33143 Brand 2009-04-27 [primary (reproduced) + secondary]: BofA release reproduced at https://www.rismedia.com/2009/04/27/35805; AP at https://thedailyrecord.com/2009/04/27/bank-of-america-rebrands-mortgage-operations/
- **NATCITY National City** (ghost). Legal 2009-11-06 [primary]: https://api.fdic.gov/banks/history?filters=CERT:6557 Brand 2010-06-14 [primary]: https://d1io3yog0oux5.cloudfront.net/_9e4ec6c033f1f02c2d63ad141e3261a4/pnc/news/2010-04-19_PNC_Completes_Largest_Phase_of_National_City_277.pdf; https://investor.pnc.com/news-events/financial-press-releases/detail/274/pnc-successfully-converts-6-million-customers-and-1300-branches-from-national-city-in-seven-months
- **WACHOVIA Wachovia** (ghost). Legal 2010-03-20 [primary]: https://api.fdic.gov/banks/history?filters=CERT:33869 Brand 2011-10-15 [primary]: https://www.sec.gov/Archives/edgar/data/0000072971/000119312511272251/d243657dex991.htm
- **INGDIRECT ING Direct** (ghost). Legal 2012-11-01 [primary]: https://api.fdic.gov/banks/history?filters=CERT:35489 Brand 2013-02-01 [secondary (issuer FAQ quoted for month)]: https://thefinancialbrand.com/26299/ing-direct-brand-capital-one-360/; ING DIRECT FAQ ('only until February, 2013') quoted at https://www.depositaccounts.com/blog/2012/11/ing-directs-new-name-will-be-capital-one-360.html
- **SOVEREIGN Sovereign Bank** (ghost). Legal 2013-10-17 [primary]: https://api.fdic.gov/banks/history?filters=CERT:29950 Brand 2013-10-17 [primary]: https://prnewswire.com/news-releases/top-25-us-bank-changes-name-to-santander-today-228186111.html; https://www.sec.gov/Archives/edgar/data/0000891478/000119312513413819/d616978d6k.htm
- **BBVACOMPASS BBVA Compass** (ghost). Legal 2019-06-10 [primary]: https://api.fdic.gov/banks/history?filters=CERT:19048 Brand 2019-06-10 [primary]: https://www.bbva.com/es/us/bbva-comienza-a-desplegar-su-nueva-marca-en-ee-uu/; https://www.sec.gov/Archives/edgar/data/1409775/000140977519000043/bbvausa20190630x10q.htm
- **SUNTRUST SunTrust** (ghost). Legal 2019-12-07 [primary]: https://api.fdic.gov/banks/history?filters=CERT:867 Brand 2022-02-22 [secondary (issuer statement quoted) + primary (quarter)]: Truist statement quoted at https://richmondbizsense.com/2022/02/23/truist-bank-shutters-more-local-branches-as-bbt-suntrust-merger-continues/; Q1-2022 10-Q https://www.sec.gov/Archives/edgar/data/92230/000009223022000057/tfc-20220331.htm
- **BBT BB&T** (ghost). Legal 2019-12-07 [primary]: https://api.fdic.gov/banks/history?filters=CERT:9846 Brand 2022-02-22 [secondary + primary]: same as SUNTRUST
- **UNIONBANK Union Bank (MUFG Union Bank)** (ghost). Legal 2023-05-26 [primary]: https://api.fdic.gov/banks/history?filters=CERT:22826 Brand 2023-05-30 [primary]: https://www.usbank.com/dam/documents/pdf/union-bank/fsgs/UnionBank-Consumer-FSG-F_ADA.pdf
- **SIGNATURE Signature Bank** (ghost). Legal 2023-03-12 [primary]: https://www.fdic.gov/resources/resolutions/bank-failures/failed-bank-list/signature-ny.html Brand 2023-03-20 [primary]: https://www.fdic.gov/news/press-releases/2023/pr23021.html
- **FIRSTREPUBLIC First Republic Bank** (ghost). Legal 2023-05-01 [primary]: https://api.fdic.gov/banks/failures?filters=CERT:59017 Brand 2024-05-25 [primary]: https://digital.jpmorgan.com/firstrepublicintegration/welcomecenter/chase-connect-faq/index.html
- **BMOHARRIS BMO Harris** (ghost). Legal 2023-09-03 [primary]: https://api.fdic.gov/banks/history?filters=CERT:16571 Brand 2023-09-03 [primary + secondary]: https://about-us.bmo.com/our-legal-and-brand-name-are-changing; https://www.slash.com/routing-numbers/bmo
- **SVB Silicon Valley Bank** (ghost). Legal 2023-03-10 [primary]: https://api.fdic.gov/banks/failures?filters=CERT:24735 Brand 2026-10-06 [primary]: https://www.prnewswire.com/news-releases/first-citizens-bank-launches-new-innovation-banking-brand-302899195.html; https://www.firstcitizens.com/innovation
- **DISCOVER Discover** (control). Legal 2025-05-18 [primary]: https://api.fdic.gov/banks/history?filters=CERT:5649 Brand retained [primary]: https://www.capitalonediscover.com/integration-faqs
- **Claude Opus 4.5** cutoff: https://platform.claude.com/docs/zh-CN/models/opus-4-5/overview; lifecycle: same
- **Claude Sonnet 4.5** cutoff: https://platform.claude.com/docs/en/models/sonnet-4-5/overview.md; lifecycle: https://platform.claude.com/docs/fr/models/sonnet-4-5/overview.md
- **GPT-4o** cutoff: https://developers.openai.com/api/docs/models/gpt-4o.md; lifecycle: https://developers.openai.com/api/docs/deprecations (entry 2026-10-14: GPT-4 series model deprecations)
- **GPT-4o mini** cutoff: https://developers.openai.com/api/docs/models/gpt-4o-mini.md; lifecycle: https://developers.openai.com/api/docs/deprecations (entry 2026-10-14: GPT-4 series model deprecations)
- **Gemini 2.5 Flash** cutoff: https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash; lifecycle: https://ai.google.dev/gemini-api/docs/deprecations (last updated 2026-10-22)
- **Gemini 2.5 Flash-Lite** cutoff: https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-lite; lifecycle: https://ai.google.dev/gemini-api/docs/deprecations (last updated 2026-10-22)
- **Claude Opus 5.5** cutoff: https://platform.claude.com/docs/en/models/opus-5-5/overview; lifecycle: same
- **GPT-6 Astra** cutoff: https://developers.openai.com/api/docs/models/gpt-6-astra.md; lifecycle: same
- **Gemini 4 Argon** cutoff: https://deepmind.google/models/model-cards/gemini-4-argon/; lifecycle: https://ai.google.dev/gemini-api/docs/models/gemini-4-argon

#### FDIC status check after the SOD date (36 charters of the current holders)

| CERT | Date | Code | Change | Institution | From | Out | Survivor |
|---|---|---|---|---|---|---|---|
| 4297 | 2026-09-21 | 712 | Branch Purchased |  |  | Capital One, National Association |  |
| 12368 | 2026-07-08 | 712 | Branch Purchased |  |  | Regions Bank |  |
| 16571 | 2026-09-08 | 712 | Branch Purchased |  |  | BMO Bank National Association |  |

## 5. Changes

**r1, 2026-11-08**

1. **Decisions adopted.** Pablo adopted every recommendation in section 6 (D1 to D19). No share, floor, window or gap changes.
2. **GPT-4o and GPT-4o mini lifecycle confirmed (D18).** OpenAI's deprecations page (notice of 2026-10-14) sets the shutdown of `gpt-4o-2024-08-06`, `gpt-4o-2024-11-20` and `gpt-4o-mini-2024-07-18` for 2027-01-14. The page lists dated snapshots, not the `gpt-4o` and `gpt-4o-mini` aliases, so every call logs the snapshot it returns.
3. **Sun Country moved to primary sources (D15).** Allegiant's release of 2026-05-13 (IR site, and Exhibit 99.1 of an SEC filing) confirms the close and says both airlines keep their brands for now.
4. **The builder now assembles this draft** from `registries/draft_template.md` and the generated tables, into `registries/out/v0_40_registry_draft.md`.
5. **Moved into the pipeline** under `osf/v40/` (scripts, registries, data), following the v0.39 layout. The Samsung disclosure moved from the front matter to section 9, per the program's conflict-of-interest rule.

**r0, 2026-11-08, against the earlier draft**

1. **SVB moved from living control to ghost.** First Citizens launched First Citizens Innovation Banking on 2026-10-06, retiring the Silicon Valley Bank division brand.
2. **Sun Country added as a living control.** Allegiant closed its acquisition on 2026-05-13; the brand is kept for now.
3. **Rule R6 applied to every multi-charter bank brand:** Commerce 0.599% → 0.666%, Washington Mutual 2.612% → 2.680%, Wachovia 5.214% → 5.404%. No floor decision changes.
4. **Airline legal date is now the FAA certificate for every merger.** For the two cessations (ATA, Spirit) it is the day operations ended. ATA moves from 2008-04-02 (Chapter 11 petition) to 2008-04-03.
5. **Virgin America brand date** moves from 2018-04-24 (last flights) to 2018-04-25, the cutover Alaska names.
6. **Upgraded from secondary to primary sources:** Northwest brand date (Delta), AirTran deal close (SEC), Virgin America (Alaska), Wachovia's final conversion weekend (Wells Fargo 8-K), First Republic (JPMorgan), BMO Harris (BMO). The BMO Harris brand date moves from 2023-09-05, which had no source, to 2023-09-03, the date BMO names.
7. **Both exit scans now run inside the builder**, each with a classification table; every candidate at or above 0.4% (banks) or 0.2% (airlines) has a class and a reason.
8. **Newly checked and excluded:** World Savings (window edge, D9) and AmSouth (branches converted to Regions during 2007, per the Regions FY2007 10-K).
9. **Model cutoffs and lifecycle** taken from vendor pages (section 4). Third-party sites give Claude Opus 4.5 a March 2025 cutoff; the vendor page says training data to August 2025 (reliable knowledge to May 2025), and the vendor page governs.

## 6. Decisions, adopted 2026-11-08

Each item gives the issue, what the data shows and the decision. Pablo adopted every recommendation on 2026-11-08. Items with work left say *Open before lock*.

- **D1 Airline share basis.** Allocated brand share (regional flying credited to the brand that sells it) puts American first: 21.11% against Delta's 19.80%. Operating-carrier share puts Delta first: 17.90% against American's 17.74%. *Adopted:* allocated share as primary, operating share as a pre-registered sensitivity. Name American as the leader for H_Amplify, and Delta in the sensitivity.
- **D2 Airline share units.** Hawaiian inside Alaska is forced by the data. Sun Country still reports on its own, although Allegiant has owned it since 2026-05-13. *Adopted:* Sun Country separate in the primary analysis and inside Allegiant as a sensitivity (Allegiant 2.12% → 2.67%). A retained brand's mentions count toward its share unit.
- **D3 North Fork enters by its brand date only** (legal 2007-08-01, brand 2008-03-10). *Adopted:* keep; it drops out in the legal-date sensitivity.
- **D4 Brokerage-sweep holders.** Morgan Stanley (2.52%), Goldman Sachs (2.48%), Charles Schwab (1.36%) and UBS (0.57%) enter by the deposit rule, hold their deposits in one to five offices and are seldom named as retail banks. Their AI share will sit far below their deposit share and pull the log-log slope down. *Adopted:* keep them by rule and pre-register the slope with and without these four. *Open before lock:* a citation for each of the four for the exclusion criterion (deposits held as brokerage sweep deposits).
- **D5 Multi-charter shares (R6).** Changes three shares (section 5, item 3) and no floor decision. *Adopted:* adopt.
- **D6 Silicon Valley Bank.** Every model cutoff falls between SVB's legal exit (2023-03-10) and its brand exit (2026-10-06). SVB therefore changes sign between the primary and legal-date analyses for all nine models: brand gaps run from −36.2 to −3.2 months, legal gaps from +6.7 to +39.7. *Adopted:* keep SVB as a ghost and analyse it with Spirit as a post-cutoff exit in the primary run; the legal-date sensitivity treats it as a pre-cutoff failure. Note that this leaves Discover as the only living-brand control for banks.
- **D7 BBVA Compass chain.** Compass Bank became BBVA USA on 2019-06-10, and BBVA USA merged into PNC on 2021-10-08 (0.477% at its last SOD, below the floor). The brand rollout began 2019-06-10; its completion date was not found. *Adopted:* one ghost, BBVA Compass, with BBVA USA and Compass Bank as aliases. The correct status answer today is PNC.
- **D8 BMO Harris.** The successor keeps "BMO". *Adopted:* keep it as a ghost, because the stem "Harris" is dropped (R6). Code "BMO Harris, now BMO" as a gone-flag, and count "BMO" alone toward the current holder.
- **D9 World Savings sits at the window edge.** It had 1.093% at SOD 2007. Deposits moved to Wachovia and branches were rebranded on 2007-10-11 (secondary), and the thrift was renamed Wachovia Mortgage, FSB on 2007-12-31 (FDIC), one day before the window opens. *Adopted:* exclude it, and note it as the first candidate if the window ever opens earlier.
- **D10 Merrill Lynch Bank USA** (0.764%) merged into Bank of America on 2009-07-01, but the Merrill brand continues. *Adopted:* exclude it, because the brand persists.
- **D11 Name collisions.** Living banks also use the names Commerce Bank (Commerce Bancshares, Kansas City), Union Bank and Signature Bank. Several airline names are common words: Spirit, Continental, Northwest, United, Frontier, Breeze, Southwest, Alaska. *Adopted:* probes name each ghost with a disambiguator (city or former parent); coders mark bare collisions as "ambiguous"; presence is reported with and without ambiguous mentions.
- **D12 Current-brand aliases** (`registries/aliases_current.csv`). Marcus counts for Goldman Sachs; Apple Card and Apple Savings do not. Discover counts toward the Capital One holder's share and also stands as a control. "TD" alone does not count. *Adopted:* approve the list as drafted.
- **D13 Airline legal date** is the FAA single operating certificate, the airline counterpart of an FDIC charter merger. For cessations it is the day operations ended, so Spirit's Chapter 11 filing of 2025-08-29 is context, not an exit. *Adopted:* adopt.
- **D14 Brand date** is the issuer-named cutover, or the final operation when none is named. One-day choices fall below the month resolution of the cutoffs. *Adopted:* adopt.
- **D15 Sun Country as a living control.** *Adopted:* add it. Closed in r1: Allegiant's release of 2026-05-13 confirms the close and says both airlines keep their brands for now.
- **D16 Near-floor holders.** USAA (0.483%), RBC (0.473%), Synchrony (0.451%), Western Alliance (0.432%), Santander (0.415%) and Zions (0.402%) fall below the floor. *Adopted:* keep the floor and code their mentions as "other". USAA will be named often; say so in the paper.
- **D17 Secondary-only dates.** LaSalle (2008-05-05), the US Airways cutover (2015-10-17), ING Direct (2013-02-01), Spirit's cessation (statement quoted by the press), the Northwest certificate (2009-12-31), and the day (not the month) of the final Washington Mutual and Truist conversions. None of them changes a window or floor decision. *Adopted:* upgrade any for which a primary turns up; otherwise lock with the source type shown. *Open before lock:* the search for primaries.
- **D18 Model lifecycle.** Opus 4.5 retires not sooner than 2026-11-24, and Sonnet 4.5 retires on 2026-11-30. GPT-4o and GPT-4o mini shut down on 2027-01-14 (OpenAI deprecations page, notice of 2026-10-14, re-confirmed in r1); the page names dated snapshots only, so every call logs the snapshot it returns. Gemini 2.5 Flash and Flash-Lite are not deprecated on the Gemini API, but access is limited to prior users; Vertex AI's October 2026 retirement does not apply if the run stays on the Developer API with the v0.39 project. *Adopted:* keep the legacy arm finishing before 2026-11-24, with Gemini on the Developer API and the v0.39 project. Closed in r1.
- **D19 Probe budget.** SVB (ghost) and Sun Country (control) add four probes if controls receive the recognition and status pair. That is about 150 calls (about 37 per probe), taking the study to roughly 90 probes and 3,350 calls. *Adopted:* accept.

## 7. Before lock

1. Pablo's calls on D1 to D19: done on 2026-11-08, every recommendation adopted.
2. Done on 2026-11-08: v0.40 scaffolded, cloned v0.39 content removed, registry placed in `osf/v40/`.
3. Upgrade secondary dates where a primary turns up (D17), and cite the brokerage-sweep criterion (D4). D15 and D18 closed in r1.
4. Set the freeze date, re-run `build --freeze <date> --status-check`, and commit inputs, outputs and the manifest.
5. Tag `v0.40-prereg-r1` and deposit to OSF (ec6wh → `v40/prereg/`).
6. Finish the legacy arm before 2026-11-24 (Opus 4.5's earliest retirement; Sonnet 4.5 retires 2026-11-30).

## 8. Reproduce

```
python3 osf/v40/scripts/build_registry_v0_40.py fetch t100 2007 2026
python3 osf/v40/scripts/build_registry_v0_40.py fetch ontime 2025-08 2026-07
python3 osf/v40/scripts/build_registry_v0_40.py fetch sod 2005 2026
python3 osf/v40/scripts/build_registry_v0_40.py build --freeze 2026-11-08 --status-check
```

Run from `~/aias`. Paths resolve from the folder above `scripts/`, which is `osf/v40/`: inputs in `registries/`, data in `data/raw/`, outputs and this draft in `registries/out/`. Use `--registry-dir`, `--data-dir` and `--out` for another layout. The 54 data files total about 502 MB; the snapshot used for this draft ships with SHA-256 checksums. `--status-check` queries FDIC; the result is cached in `data/raw/fdic/status_check_<freeze>.csv`, and the run used for this draft ships with the registry. Two lines differ between runs on the same inputs: the timestamp at the top of the tables and `run_utc` in the manifest.

## 9. Declarations

- **Conflict of interest.** The pre-registrant is employed by Samsung Electronics America (standing declaration). Samsung does not compete in US airlines or US retail banking. Banking has an adjacency through Samsung Wallet; it is disclosed here and in the paper's Declarations.
- **Independence.** No focal brand, no lessons addressed to a brand, and no brand contacted. Public, official data only.
