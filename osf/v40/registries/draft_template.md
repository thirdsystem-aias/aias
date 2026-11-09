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

{{TABLES}}

## 5. Changes

**r1, 2026-11-08**

1. **Decisions adopted.** Pablo adopted every recommendation in section 6 (D1 to D19). No share, floor, window or gap changes.
2. **GPT-4o and GPT-4o mini lifecycle confirmed (D18).** OpenAI's deprecations page (notice of 2026-10-14) sets the shutdown of `gpt-4o-2024-08-06`, `gpt-4o-2024-11-20` and `gpt-4o-mini-2024-07-18` for 2027-01-14. The page lists dated snapshots, not the `gpt-4o` and `gpt-4o-mini` aliases, so every call logs the snapshot it returns.
3. **Sun Country moved to primary sources (D15).** Allegiant's release of 2026-05-13 (IR site, and Exhibit 99.1 of an SEC filing) confirms the close and says both airlines keep their brands for now.
4. **The builder now assembles this draft** from `registries/draft_template.md` and the generated tables, into `registries/out/v0_40_registry_draft.md`.
5. **Moved into the pipeline** under `osf/v40/` (scripts, registries, data), following the v0.39 layout. The Samsung disclosure moved from the front matter to section 9, per the program's conflict-of-interest rule.
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
