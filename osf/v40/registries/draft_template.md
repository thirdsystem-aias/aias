# AIAS™ v0.40 brand registry, draft r3 (frozen 2026-11-12)

**Study.** Leaders, challengers and ghosts. Two US categories reshaped by mergers and failures.

**Status.** Decisions adopted; frozen on 2026-11-12. The ghost window closes at the freeze date, and every brand's status was re-checked up to it (section 5, r3). Pablo adopted every recommendation in section 6 on 2026-11-08. The registry locks with tag `v0.40-prereg-r1` and the OSF deposit (ec6wh → `v40/prereg/`), before any study probe.

**Built.** 2026-11-08 (r1) and 2026-11-09 (r2, sources only) with `--freeze 2026-11-08`; frozen 2026-11-12 (r3) with `osf/v40/scripts/build_registry_v0_40.py build --freeze 2026-11-12 --status-check`, which also assembles this draft. The builder computes every share, floor test, window test and gap below. Only dates and their sources are entered by hand (`registries/exit_events.csv`, `registries/model_cutoffs.csv`), each with a URL and a source type.

## 1. What the registry holds

| | Airlines | Banks |
|---|---|---|
| Share measure | Revenue passenger miles, BTS T-100, 2025-08 to 2026-07 | Deposits, FDIC Summary of Deposits, 2026-06-30 |
| Current units | 11 brands in 10 share units | 25 holders |
| Ghosts (brand retired 2008-01-01 to freeze) | 7 | 17 |
| Living-brand controls | Hawaiian, Sun Country | Discover |
| Incumbent controls | American, Delta | Chase, Bank of America |

- Exit-to-cutoff gaps run from −36.2 months (SVB, GPT-4o) to 219.7 months (North Fork, Claude Opus 5.5); the smallest positive gap is 0.9 months (BMO Harris, GPT-4o). 19 of the 216 ghost × model pairs are exits after the model's cutoff: Spirit (eight models, all but Opus 5.5), SVB (all nine) and First Republic (GPT-4o and GPT-4o mini).
- An FDIC check of the 36 charters held by the 25 bank holders, re-run at the freeze, found no merger, failure or legal name change between the SOD date (2026-06-30) and 2026-11-12. The only events are three branch sales (Capital One, Regions, BMO). A re-check of every airline and bank brand found no status change between 2026-11-08 and the freeze (section 5, r3).

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

{{TABLES}}

## 5. Changes

**r3, 2026-11-12 (freeze)**

1. **Frozen 2026-11-12; nothing moved.** Rebuilt with `build --freeze 2026-11-12 --status-check` from the same inputs and the same raw-data snapshot (all 54 files match `registries/RAW_DATA_SHA256.txt`, checked 2026-11-11). Against the 2026-11-08 outputs, `airlines_current.csv`, `banks_current.csv`, `exits_and_controls.csv`, `exit_cutoff_gaps.csv`, both exit scans, the regional allocation and the model table are byte-identical, so every share, floor test, window test and gap is unchanged. No brand date falls between 2026-11-09 and the freeze. The manifest differs only in `freeze` and `run_utc`, and the tables only in their timestamp.
2. **FDIC check to the freeze.** The builder re-queried BankFind on 2026-11-12 at 00:01 CT for the 36 charters of the 25 holders. It found the same three branch sales as on 2026-11-08 (Capital One 2026-09-21, Regions 2026-07-08, BMO 2026-09-08), no merger, failure or legal name change, and no query errors; `data/raw/fdic/status_check_2026-11-12.csv` is byte-identical to the 2026-11-08 file. No bank has failed since 2026-07-17 (FDIC failures: https://api.fdic.gov/banks/failures?sort_by=FAILDATE&sort_order=DESC&limit=5&fields=NAME,CERT,FAILDATE,CITYST,ACQUIRER_NAME). The two ghost successors outside the 25 holders have no event after 2026-11-08: Santander Bank, N.A., Sovereign's successor (last event 2026-09-11: https://api.fdic.gov/banks/history?filters=CERT:29950&sort_by=EFFDATE&sort_order=DESC&limit=8&fields=INSTNAME,CERT,EFFDATE,PROCDATE,CHANGECODE,CHANGECODE_DESC,FRM_INSTNAME,OUT_INSTNAME,SUR_INSTNAME), and Flagstar Bank, N.A., Signature's (last event 2026-06-29: https://api.fdic.gov/banks/history?filters=CERT:32541&sort_by=EFFDATE&sort_order=DESC&limit=6&fields=INSTNAME,CERT,EFFDATE,PROCDATE,CHANGECODE,CHANGECODE_DESC). BankFind posts events days to weeks after they happen, so the filings and news below cover the last days.
3. **Every airline and bank brand re-checked for status changes since 2026-11-08: none found.** Checked from 2026-11-11, 11 pm CT, to the freeze build:
   - *SEC filings* from 2026-11-08 to the latest listed (2026-11-10), from `https://data.sec.gov/submissions/CIK<CIK, 10 digits>.json`, for the parent of every current unit (airlines: CIK 6201, 27904, 100517, 92380, 766421, 1158463, 1670076, 1362468; banks: 19617, 70858, 72971, 831001, 36104, 927628, 895421, 886982, 713676, 92230, 947263, 316709, 35527, 49196, 927971, 759944, 798941, 36270, 4962, 91576, 40729, 1089113, 1281761, 1610520, 2082866), for Sun Country (1743907) and Spirit (1498710), and for Flagstar (910073) and Santander Holdings USA (811830). None reports a merger, acquisition, rename, charter change, failure, bankruptcy or cessation. The only 8-K is Capital One's of 2026-11-10, a conference notice under Item 7.01 (https://www.sec.gov/Archives/edgar/data/927628/000092762826000157/cof-20261110.htm). Breeze files no periodic reports.
   - *Regulators.* Federal Reserve press releases: one since 2026-11-08, the approval of applications by Mutual Federal Bancorp, MHC and MFB Bancorp (https://www.federalreserve.gov/feeds/press_all.xml). OCC news releases: the latest is NR 2026-98 of 2026-11-05 (https://occ.gov/news-events/newsroom/news-issuances-by-year/news-releases/2026-news-releases.html).
   - *Issuers.* The Hawaiian brand is in use on 2026-11-10 (Alaska Air Group newsroom: https://news.alaskaair.com/). Allegiant: "in the near-term Sun Country will continue to operate as it does today" and "Booking systems remain separate for now" (https://www.allegiantair.com/together-we-fly). Discover: "© 2026 Discover, a division of Capital One, N.A., Member FDIC" (https://www.discover.com/online-banking/).
   - *News.* AirlineGeeks headlines of 2026-11-09 to 2026-11-11 (https://airlinegeeks.com/), Aviation Week's routes log for the week of 2026-11-09 (https://aviationweek.com/air-transport/airports-networks/routes-networks-latest-rolling-daily-updates-wc-nov-9-2026) and American Banker's M&A items of 2026-11-09 and 2026-11-10 (https://www.americanbanker.com/tag/mergers-and-acquisitions). None reports a merger, rename, closure or cessation for a registry brand.
   - *Not verified on the issuer's own site:* suncountry.com (bot check), spirit.com and Discover's application pages (robots exclusion). Spirit's last own SEC filing is the 8-K of 2026-05-04, and no report of resumed flying was found.
4. **SEC rechecks: both confirmed.** Truist's FY2021 10-K (accession 0000092230-22-000008, accepted 2022-02-22 17:33:55: https://www.sec.gov/Archives/edgar/data/92230/000009223022000008/tfc-20211231.htm) says: "We recently completed the core bank conversion in February 2022 for heritage SunTrust clients." UBS's first-quarter 2026 report (6-K of 2026-04-29, accession 0001610520-26-000044: https://www.sec.gov/Archives/edgar/data/1114446/000161052026000044/edgar1q26ubsgroup.htm, table "Customer deposits, by currency") gives sweep deposits of USD 41.5bn at 31.12.25, all in USD (39.9bn at 31.3.26). The same Truist paragraph puts the migration of heritage BB&T clients "to the Truist ecosystem" in October 2021. BB&T keeps the February 2022 final conversion it shares with SunTrust; moving it would lengthen BB&T's gaps by four to five months and change no window, floor or sign.
5. **Found in the check, dated before 2026-11-08; nothing changed; for Pablo (section 7, item 7).**
   - *Discover (control).* Capital One says "Your Discover checking account is becoming a Capital One checking account" (https://www.capitalone.com/updates/discover/checking/) and that Discover savings accounts move to Capital One at different times (https://www.capitalone.com/updates/discover/savings/); neither page gives a date. Secondary reports say Discover stopped taking new deposit applications in late January 2026 (Doctor of Credit, 2026-02-04: https://www.doctorofcredit.com/discover-savings-accounts-to-become-capital-one-savings-accounts/) and that a customer email set 2026-08-23 for some Discover savings accounts to become Capital One 360 Performance Savings (Frequent Miler, 2026-06-30: https://frequentmiler.com/some-discover-savings-accounts-will-become-capital-one-360-performance-savings-on-8-23-26/). The row's source still says "The Discover brand and Discover accounts are not going away" (https://www.capitalonediscover.com/integration-faqs). The deposit brand is being retired, which bears on Discover's role as a control and on the correct answer to S_DISCOVER.
   - *Sun Country (control).* Allegiant's page says "The combined company will operate under the Allegiant brand". An Allegiant executive put the change after the single operating certificate, 18 to 24 months out (AirlineGeeks, 2026-07-11, citing USA Today: https://airlinegeeks.com/2026/07/11/allegiant-executive-says-sun-country-brand-will-be-phased-out-completely/). The brand is live at the freeze, so the control stands.
   - *Santander (D16) and Sovereign's successor.* Santander completed its acquisition of Webster on 2026-08-20 and merged Webster Bank into Santander Bank, N.A. (SHUSA 8-K: https://www.sec.gov/Archives/edgar/data/811830/000095010326012673/dp251673_8k.htm). That is after the SOD date, so R3 keeps the two apart (Santander 0.415% and Webster Bank 0.371% at SOD 2026), both below the floor. Both brands continue "for now" (the 8-K's Exhibit 99.1).
6. **Probe set rebuilt** from the frozen outputs: byte-identical to the draft (94 probes; `prereg/probes_v0_40.json` sha256 93aee03f655cb8c4c6b04211e941b854bd921c3dbd31a9f5ffbaa91249be38ca, `prereg/probes_v0_40.md` sha256 45f1f3871f6fb60cd39840253cc6834fb918aadb160fd489c260ba50876bc92f).

**r2, 2026-11-09**

1. **Primary sources for four D17 dates; no date moved.** The US Airways cutover (American Airlines Group's third-quarter 2015 release, 8-K Exhibit 99.1: "On Oct. 17, the Company completed its transition to a single reservations system"), ING Direct's rebrand (Capital One 2012 Annual Report: Capital One 360 launched on February 1, 2013), Spirit's cessation (Spirit Aviation Holdings release of 2026-05-02, 8-K Exhibit 99.1) and the Northwest certificate (Delta FY2009 10-K: NWA merged into Delta on 2009-12-31; Delta's 2009 results release: certificate received at year end).
2. **Month now primary, day still secondary** for LaSalle (Bank of America's first-quarter 2008 release: LaSalle converts to the Bank of America brand in May), Washington Mutual (JPMorgan 8-K deck: the October wave covers California, Arizona, Nevada and Colorado) and Truist (FY2021 10-K, accepted 2022-02-22: final core bank conversion completed in February 2022).
3. **Context source upgraded.** Spirit's second Chapter 11 petition (2025-08-29) is now cited from Spirit's own 8-K instead of a third-party copy.
4. **D4 checked against each holder's own filing.** Only Schwab's shows most of its deposits swept from brokerage accounts (section 6, D4). Pablo chose the brokerage and wealth set on 2026-11-09: Morgan Stanley, Schwab and UBS.
5. **Rebuilt.** Every share, floor test, window test and gap is unchanged; only source text changed.

**r1, 2026-11-08**

1. **Decisions adopted.** Pablo adopted every recommendation in section 6 (D1 to D19). No share, floor, window or gap changes.
2. **GPT-4o and GPT-4o mini lifecycle confirmed (D18).** OpenAI's deprecations page (notice of 2026-10-14) sets the shutdown of `gpt-4o-2024-08-06`, `gpt-4o-2024-11-20` and `gpt-4o-mini-2024-07-18` for 2027-01-14. The page lists dated snapshots, not the `gpt-4o` and `gpt-4o-mini` aliases, so every call logs the snapshot it returns.
3. **Sun Country moved to primary sources (D15).** Allegiant's release of 2026-05-13 (IR site, and Exhibit 99.1 of an SEC filing) confirms the close and says both airlines keep their brands for now.
4. **The builder now assembles this draft** from `registries/draft_template.md` and the generated tables, into `registries/out/v0_40_registry_draft.md`.
5. **Moved into the pipeline** under `osf/v40/` (scripts, registries, data), following the v0.39 layout. The conflict-of-interest disclosure moved from the front matter to section 9, per the program's conflict-of-interest rule.
6. **Commerce Bank's label** now carries its FDIC main-office city, Philadelphia, instead of "NJ", which had no source. The probes use the same name (D11).

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
- **D4 Brokerage-sweep holders.** Morgan Stanley (2.52%), Goldman Sachs (2.48%), Charles Schwab (1.36%) and UBS (0.57%) enter by the deposit rule, hold their deposits in one to five offices and are seldom named as retail banks. Their AI share will sit far below their deposit share and pull the log-log slope down. *Adopted:* keep them by rule and pre-register the slope with and without these four. *Checked 2026-11-09 against each holder's own filing:* Charles Schwab, 90.9% of bank deposits swept from brokerage accounts ($232.4bn of $255.7bn; FY2025 10-K, note 12). Morgan Stanley, 35.0% brokerage sweep deposits ($145.2bn of $415.5bn), with time deposits (mostly brokered CDs) at 24.0%; its FY2025 10-K says deposits are primarily sourced from Wealth Management clients. UBS, sweep deposits of USD 41.5bn at 2025-12-31 (all in USD; UBS first-quarter 2026 report) against $104.6bn of deposits at UBS Bank USA (FDIC): at most 39.7%. Goldman Sachs, deposit sweep programs 6.9% ($34.4bn of $501.4bn; FY2025 10-K), while consumer deposits (Marcus and Apple Card) are 41.5%; at GS Bank USA on 2026-06-30, sweep is 8% and consumer 39% of $500bn. The criterion as worded holds for Schwab only. The office count does not separate the four either: American Express (0.90%) and Ally (0.82%) also hold their deposits in one office. *Decided 2026-11-09:* the sensitivity excludes Morgan Stanley, Charles Schwab and UBS, whose deposits come mainly from their own brokerage and wealth-management clients. Goldman Sachs stays in, like Ally and American Express, because its largest source is consumer deposits (Marcus, D12). UBS is excluded on its sweep program; its filings do not give UBS Bank USA's full deposit mix.
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
- **D17 Secondary-only dates.** LaSalle (2008-05-05), the US Airways cutover (2015-10-17), ING Direct (2013-02-01), Spirit's cessation (statement quoted by the press), the Northwest certificate (2009-12-31), and the day (not the month) of the final Washington Mutual and Truist conversions. None of them changes a window or floor decision. *Adopted:* upgrade any for which a primary turns up; otherwise lock with the source type shown. *Done 2026-11-09 (r2):* primaries for the US Airways cutover, ING Direct, Spirit and the Northwest certificate; for LaSalle, Washington Mutual and Truist the month is now primary and the day stays secondary. No date moved.
- **D18 Model lifecycle.** Opus 4.5 retires not sooner than 2026-11-24, and Sonnet 4.5 retires on 2026-11-30. GPT-4o and GPT-4o mini shut down on 2027-01-14 (OpenAI deprecations page, notice of 2026-10-14, re-confirmed in r1); the page names dated snapshots only, so every call logs the snapshot it returns. Gemini 2.5 Flash and Flash-Lite are not deprecated on the Gemini API, but access is limited to prior users; Vertex AI's October 2026 retirement does not apply if the run stays on the Developer API with the v0.39 project. *Adopted:* keep the legacy arm finishing before 2026-11-24, with Gemini on the Developer API and the v0.39 project. Closed in r1.
- **D19 Probe budget.** SVB (ghost) and Sun Country (control) add four probes if controls receive the recognition and status pair. That is about 150 calls (about 37 per probe), taking the study to roughly 90 probes and 3,350 calls. *Adopted:* accept.

## 7. Before lock

1. Pablo's calls on D1 to D19: done on 2026-11-08, every recommendation adopted.
2. Done on 2026-11-08: v0.40 scaffolded, cloned v0.39 content removed, registry placed in `osf/v40/`.
3. D17 done in r2. D4 decided 2026-11-09: the sensitivity excludes Morgan Stanley, Schwab and UBS. D15 and D18 closed in r1.
4. Set the freeze date, re-run `build --freeze <date> --status-check`, and commit inputs, outputs and the manifest. *Done 2026-11-12 (r3):* frozen 2026-11-12; inputs unchanged; outputs, manifest and the FDIC check committed.
5. Tag `v0.40-prereg-r1` and deposit to OSF (ec6wh → `v40/prereg/`).
6. Finish the legacy arm before 2026-11-24 (Opus 4.5's earliest retirement; Sonnet 4.5 retires 2026-11-30).
7. *Open for Pablo (r3):* Discover's deposit accounts are moving to Capital One (section 5, r3, item 5). Decide whether Discover stays the bank living-brand control and how S_DISCOVER is coded.

## 8. Reproduce

```
python3 osf/v40/scripts/build_registry_v0_40.py fetch t100 2007 2026
python3 osf/v40/scripts/build_registry_v0_40.py fetch ontime 2025-08 2026-07
python3 osf/v40/scripts/build_registry_v0_40.py fetch sod 2005 2026
python3 osf/v40/scripts/build_registry_v0_40.py build --freeze 2026-11-12 --status-check
```

Run from `~/aias`. Paths resolve from the folder above `scripts/`, which is `osf/v40/`: inputs in `registries/`, data in `data/raw/`, outputs and this draft in `registries/out/`. Use `--registry-dir`, `--data-dir` and `--out` for another layout. The 54 data files total about 502 MB; the snapshot used for this draft ships with SHA-256 checksums. `--status-check` queries FDIC; the result is cached in `data/raw/fdic/status_check_<freeze>.csv`, and the run used for this draft ships with the registry. Two lines differ between runs on the same inputs: the timestamp at the top of the tables and `run_utc` in the manifest.

## 9. Declarations

- **Conflict of interest.** The pre-registrant is employed by Samsung Electronics America (standing declaration). Samsung does not compete in US airlines or US retail banking. Banking has an adjacency through Samsung Wallet; it is disclosed here and in the paper's Declarations.
- **Independence.** No focal brand, no lessons addressed to a brand, and no brand contacted. Public, official data only.
