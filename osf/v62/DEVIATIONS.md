# AIAS v0.62 — DEVIATIONS log

Non-English wave of the t₄ omnibus panel (r0/r1: French and Japanese; from r2: Spanish, Korean and Chinese; Part E). Entries are numbered; Entry 0 is the pre-acquisition conflict-of-interest screen required for every phase. It documents how conflicts are handled; it is not a blanket "no affiliation" finding.

---

## Entry 0 — Samsung-group conflict-of-interest screen (pre-acquisition; written 2026-11-10, DRAFT r0, PROPOSED, before any study call)

**Context.** The pre-registrant is Director, Corporate Brand Creative and Governance at Samsung Electronics America. v0.62 makes no new brand selection: it re-asks, translated, the questions of the five omnibus registries (v0.19–v0.23, 112 units) exactly as the English t₄ wave (v0.42 r2) does, because its hypotheses compare the French and Japanese values with t₄'s English values on the same units. It is nevertheless a **new paid collection**, and one of its categories, audiophile headphones (v0.19), is a category in which Samsung-group companies sell products: Samsung Electronics (wireless earbuds under its own name) and Harman International, a wholly owned Samsung subsidiary, whose brands include JBL, AKG and Harman Kardon and, since 2025-09-23, the Sound United brands (Denon, Marantz, Bowers & Wilkins, Polk Audio and others). Programme rules applied: categories where Samsung competes are excluded or get this screen before anything else (CLAUDE.md, Industry breadth); Samsung appears only in the paper's Declarations §COI; when a phase carries a registry forward, its COI language conforms to the source phase's locked record; the Denon correction of 2026-11-10 is stated in every COI declaration that carries the v0.19 disclosure.

### Part A — Registry units (string screen)

`python3 osf/v62/scripts/coi_screen_v0_62.py` → `osf/v62/prereg/coi_screen_v0_62_r0.txt`: the 112 registry names checked, whole-word, against 30 Samsung-group names of record (Samsung; Harman and its audio brands; the Sound United brands and Masimo; Cheil, Shilla, Bioepis, Samsung C&T and the fashion brands named in v0.44 DEVIATIONS Entry 0). **One match: Denon (v0.19).** This agrees with v1.11 DEVIATIONS Entry 0's registry string screen (branch v1.11, `osf/methodology/v1_11/anchor/DEVIATIONS.md`: "Only match: Denon (v0.19)"). Method limit: a name check, not an ownership filing per brand.

### Part B — Relationships carried forward unchanged

- **v0.19 headphones.** AKG was substituted with Denon before the v0.19 lock (AKG's parent, Harman International, is a Samsung subsidiary). Correction of 2026-11-10 (verbatim in the pre-registration's COI paragraph): Denon has itself been owned by Harman International since 2025-09-23; the registry therefore includes one Samsung-group brand.
- **v0.22 automotive.** Tier-2/3 component supply relationships of Samsung subsidiaries (Harman International, audio systems; Samsung SDI, battery cells; Samsung Display, infotainment) with several registry brands; non-competitive, no brand-level overlap, no operational restriction on registry composition (v0.22 DEVIATIONS Entry 0, Part B).
- v0.20, v0.21, v0.23: no relationship of record.

### Part C — Handling of the headphones category in this new collection (proposed; the pre-registrant decides)

| Option | What it does | Effect on the study |
|---|---|---|
| **A (proposed)** | Registry unchanged, Denon included, in both languages; disclosed in Declarations §COI; two pre-registered sensitivities beside every test: **S-Denon** (111 units, Denon removed) and **S-Headphones** (96 units; r1 correction of r0's 88, the v0.19 category removed); if a primary verdict differs under either, both are reported in the abstract. Brands named in answers outside the registries (including JBL, AKG, Harman Kardon or Samsung's own) are not coded or reported. | Keeps exact comparability with the English t₄ values (same 112 units), which the primary hypothesis needs; the conflict is visible and its weight on every verdict is shown. Denon was never rated in Ranking on the archived waves (v1.14 calibration, S7), so it carries little weight there. |
| B | As A, but the Denon brand question (Phase A) is not asked in either language (−6 calls) and Denon is dropped from all tests. | No question names a Samsung-group brand; the English comparator must also drop Denon, so the primary set becomes 111 units. Phase B answers still mention Denon when models name it; the category questions do not name brands. |
| C | The headphones category is not collected (−2 × 3 × (6 × 3 + 16) = −204 calls). | Removes the category in which Samsung competes; the primary test runs on 96 units (r1 correction of r0's 88) in four categories; the "full panel" of studies #52/#53 is then incomplete, and the comparison with t₄ loses one of its five categories. |

**Why A.** The study selects no brand and its question is whether the same registry orders alike across languages; removing a unit or a category changes the object being compared and should be the exception, as v1.11 Entry 0 ruled for the same registry ("Denon stays in the registry"). The conflict is mitigated by disclosure, by full automation of acquisition, coding and scoring against locked registries, by the two sensitivities, and by the independence rule (no brand-level lesson, no brand contacted). Option C would be the conservative choice if the pre-registrant prefers that no category where Samsung competes is newly collected.

### Part D — Other checks

- **Translation and markets.** No French or Japanese brand is added; no market is targeted. No Samsung-group company is known to sell in the v0.20, v0.21 or v0.23 categories.
- **Cheil Worldwide** (Samsung affiliate, sells AI-visibility work) is not a registry unit or a probe; whether it serves any registry brand was not screened (client lists are not public); disclosed generally.
- **Independence rule.** No unit is focal; no lesson is addressed to a brand; no brand has been or will be contacted.

**Samsung in the paper.** Samsung appears only in the Declarations §COI of the v0.62 paper (draft text in PRE_REGISTRATION_v0_62_DRAFT_r0.md §10).


### Part E — r2 (2026-11-10/11): languages changed; option A decided

- **Languages.** The pre-registrant decided (2026-11-10, 20:44 CT) that the wave runs in Spanish, Korean and Chinese (Simplified, Mainland usage), replacing French and Japanese. The registries do not change: they are t₄'s 112 units.
- **Headphones option A** is the decision of record (default (3) of 2026-11-10): Denon kept and disclosed, every result also shown without Denon (S-Denon, 111 units) and without the headphones category (S-Headphones, 96 units). `params_v0_62.HEADPHONES_OPTION = "A"`.
- **Korean.** South Korea is Samsung Electronics' home market. Answers in Korean (as in any language) may name Samsung-group brands that are not registry units; such names are never coded or scored (coding counts only the 112 registry units; the r2 alias table adds no alias for any non-registry brand). The pre-registration states this in its Declarations §COI, the only place Samsung is named in the paper.
- **Part D update.** No Spanish, Korean or Chinese brand is added; no market is targeted.


### Part F — r3 (2026-11-11): Samsung-group screen of all 112 units, with Korea in mind (ex ante, before any study call; PROPOSED handling, the pre-registrant decides)

**Scope and method.** The 112 registry units (names as the alias table and the t₄ probe file carry them) were screened on 2026-11-11 (sources read between about 14:55 and 15:15 UTC) for four kinds of Samsung-group tie: (1) **ownership** — the owner as found on the owner's brand page or a dated report (tables below), and the string screen re-run with an extended term list (`coi_screen_v0_62.py` → `osf/v62/prereg/coi_screen_v0_62_r3.txt`: 70 terms; one match, Denon); (2) **distribution or licensing in Korea by a Samsung affiliate** — Samsung C&T's fashion division, its LABEL C and BEAKER shops and 10 Corso Como Seoul (searches in Korean and English; the division's portfolio as reported on 2025-03-17 and 2026-10-12); (3) **Harman brands**, Denon included since 2025-09-23; (4) **Cheil Worldwide and its agencies** — Cheil's client list, the client pages of Iris, McKinney and Barbarian, and searches for agency work for the registry brands and their owners in each category. Two further kinds were met and are recorded for the pre-registrant: Samsung-affiliated retail, and supply relationships beyond v0.22's record. "No tie found" means only that none appeared in the sources checked; it is not a finding that a brand is unaffiliated. Agency accounts change and are not fully public, so check (4) is not exhaustive.

**Carried forward verbatim (source phases' locked handling).**
- v0.19 audiophile headphones, `osf/v19/PRE_REGISTRATION_v0_19.md` §2.3: "**AKG removed from Cell A short-list; Denon substituted.** AKG is Samsung-owned since 2016. The author's COI declaration names Samsung; including AKG would invite the kind of reviewer suspicion AIAS™ 1.0 does not need to absorb. Denon carries comparable heritage stature (founded 1910; AH-D7000 → D9200 audiophile line) and removes the question. Decision rationale recorded here for audit trail." With the correction of record: "Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026." (Primary source of record: HARMAN press release, Business Wire, 2025-09-23, https://www.businesswire.com/news/home/20250923135384/en/HARMAN-Completes-Sound-United-Acquisition-to-Expand-Premium-Audio-Leadership, as cited in v1.10 DEVIATIONS Entry 2.) Handling of record: Denon kept (option A), disclosed, S-Denon and S-Headphones (Part E).
- v0.22 automotive, `prereg/v0_22_mega_prompt.md`, DEVIATIONS Entry 0, Part B: "**Screen result:** Three of the 24 brands in the locked v0.22 registry have tier-2/3 supply relationships with Samsung Electronics America (author's primary employer) via Samsung subsidiaries: BMW (Harman audio + Samsung SDI batteries + Samsung Display infotainment), Mercedes-Benz (Harman audio + Samsung Display infotainment), and Volkswagen Group brands including Bentley and Porsche (Samsung SDI battery supply to Stellantis-adjacent platforms). Tesla and Polestar also have tangential Samsung-component exposure at the parts level. These are all tier-2/3 non-competitive supply relationships, not brand-level competition. Samsung Electronics America does not produce or market passenger car brands. The COI relationship does not affect brand recognition or recall measurement by LLM panel and does not impose operational restriction on registry composition. **Disposition:** No deviation from pre-registration warranted. COI disclosed in §COI of the v0.22 SSRN paper per program standard."
- v0.20, v0.21, v0.23: no relationship of record (Part B).

**Result: five new ties, all agency work by Cheil Worldwide or its Iris agency (handled like Denon, below); two supply relationships beyond v0.22's record; one retail channel.**

| Unit | Samsung-group tie found | Source (read 2026-11-11) |
|---|---|---|
| Chevrolet (v0.22) | **Cheil Worldwide** made a Chevrolet Spark spot for GM Korea ("created by Cheil for their client General Motors"; credits: agency Cheil Worldwide, client GM Korea), 2017. Cheil lists General Motors among its major clients. Current status not established. | Branding in Asia, 2017-05-23, https://brandinginasia.com/korea-chevrolet-cheil; https://en.wikipedia.org/wiki/Cheil_Worldwide (owner "Samsung Electronics (28.43%)", parent "Samsung Group"; major clients include General Motors) |
| BMW (v0.22) | **Iris** (Iris Culture) retained as "consumer PR agency for BMW Group, including work across the BMW and MINI brands in the UK", 2018. Later status not established. | Holmes Report, 2018-04-02, https://www.holmesreport.com/latest/article/iris-culture-retains-bmw-group-s-uk-lifestyle-pr-account |
| Bentley (v0.22) | **Iris** renamed "Experiential Agency of Record" of Bentley Motors, Inc. (Americas) "for the next three years", 2021; Bentley is listed among Iris's clients on Iris's agency profile (read 2026-11-11). | lbbonline, 2021-05-27, https://lbbonline.com/news/bentley-motors-inc-renames-iris-experiential-agency-of-record; https://www.creativebrief.com/agency/iris/info |
| Jack Daniel's (v0.23) | **Iris**, "the Cheil-owned agency", hired as Jack Daniel's UK digital agency for three years, 2022; later replaced ("Iris was the incumbent" when Five by Five was picked; that page is undated). | The Drum, 2022-11-01, https://www.thedrum.com/insight/2022/11/01/jack-daniel-s-plans-double-down-live-music-activations-with-iris-appointment; https://www.mediapost.com/publications/article/397556/jack-daniels-picks-five-by-five-as-uk-digital-soc.html |
| Eucerin (v0.20) | **Iris with Cheil Brazil, Cheil Chile and Cheil UAE** appointed lead **search** (SEO, PPC) partners for Beiersdorf's "skincare brands including NIVEA and Eucerin" in LATAM, Brazil and MENAT, 2024; Iris "currently handles the Beiersdorf search business in Europe and North America" (undated page); Beiersdorf is listed among Iris's clients on Iris's agency profile (read 2026-11-11). | lbbonline, 2024-12-19, https://lbbonline.com/news/beiersdorf-appoints-iris-worldwide-and-cheil-agencies-as-lead-search-partners-for-emerging-markets; https://www.mediapost.com/publications/article/402029/iris-worldwide-adds-to-beiersdorf-portfolio-wins.html; creativebrief (above) |
| Denon (v0.19) | Owned by Harman International (Samsung) since 2025-09-23 (of record). | Harman release of record (above) |

Agency membership: Iris is "the Cheil-owned agency" (The Drum, 2022-11-01); McKinney and Barbarian are "part of the Cheil Agency Network" (https://www.agencycompile.com/agencies/mckinney, https://agencycompile.com/agencies/barbarian; neither client list names a registry brand). Same owner, not named in any agency source opened (not flagged; listed for the pre-registrant): Cadillac and the discontinued Pontiac, Oldsmobile and Saturn (General Motors); La Prairie (Beiersdorf); Woodford Reserve (Brown-Forman); Rolls-Royce (BMW Group); Volkswagen and Porsche (Volkswagen Group).

**Supply relationships beyond v0.22's record** (not flagged; v0.22's handling applies: disclosed, non-competitive, no restriction on registry composition, as v1.10 DEVIATIONS Entry 2 ruled for supply relationships; listed for the pre-registrant): **Tesla** — "Samsung Electronics has entered into a $16.5 billion contract for supplying semiconductors to Tesla" (AI6 chips; effective 2025-07-26 to 2033-12-31), larger than the "tangential" exposure of v0.22's record (NBC News, undated page, https://www.nbcnews.com/business/business-news/elon-musk-confirms-tesla-signed-16point5-billion-chip-contract-samsung-rcna221512); **Hyundai** — Samsung SDI "has signed its first supply agreement with Hyundai Motor Co.", a seven-year battery deal (KED Global, 2023-10-23, https://www.kedglobal.com/newsView/ked202310230001).

**Samsung-affiliated retail** (general disclosure, not a per-brand flag; listed for the pre-registrant): Hotel Shilla "is an affiliate of Samsung" and a "South Korean operator of luxury hotels and duty-free shops" (https://en.wikipedia.org/wiki/Hotel_Shilla); Moodie Davitt reports (undated page) Shilla's acquisition of a 44% stake in The DFASS Group, which holds "distribution agreements with brand owners for liquor, beauty and watches" (https://moodiedavittreport.com/korean-travel-retail-powerhouse-shilla-to-acquire-44-stake-in-dfass/); no registry brand is named and the stake's current status was not checked. Duty-free shops sell brands of several registry categories among many others; a retail channel is not treated as a tie.

**Korean distribution by Samsung C&T: no registry brand found.** Sources: LABEL C's brands (Absolution, Le Fournier, Maison Louis Marie, Allure Korea 2020-04-10; Maison Louis Marie, J.Hannah, Bamford, Allure Korea 2024-04-16; Bamford, Maison Louis Marie, Samsung C&T newsroom 2020-11-25, https://news.samsungcnt.com/en/features/fashion/2020-11-fashions-expansion-lifestyle-label-curated-clean-beauty/; Ellis Brooklyn, Asia Economy 2022-12-28, the tie v0.63 records); LABEL C withdrawn after four years (Dealsite, 2025-03-17, https://dealsite.co.kr/articles/138084); Maison Louis Marie at LABEL C and SSF Shop, Astier de Villatte and Frédéric Malle at 10 Corso Como Seoul (Seoul Shinmun, 2023-12-28, https://m.seoul.co.kr/news/2023/12/28/20231228500054); the division's 2026 portfolio (Sandro, Maje, Claudie Pierlot, Fursac, Margaret Howell, Fitflop and its own brands; no beauty brand) (CEO Score Daily, 2026-10-12, https://ceoscoredaily.com/page/view/2026101215473529793); searches for the Korean distribution of the registry's smaller beauty brands (Augustinus Bader, Tower 28, Glossier and goop paired with Samsung C&T; Charlotte Tilbury, Hourglass, Chantecaille, Laura Mercier, Rare Beauty, Haus Labs, Pat McGrath Labs and Huda Beauty by their Korean names) showed no Samsung-affiliate relationship; they did not establish each brand's Korean distributor. MAC Cosmetics' Korean site is operated by 이엘씨에이한국(유), the Korean entity of its owner (https://www.maccosmetics.co.kr/, re-opened for the alias check).

**All 112 units.** Owner as found (source key below; "not established" = no owner source opened in r3) and the Samsung-group tie. "No tie found" = no tie appeared in the sources checked (string screen; Samsung C&T Korean-distribution sources; Cheil-network sources; Samsung-affiliated retail; supply sources).

| v0.19 headphones | Owner as found | Tie |
|---|---|---|
| Audeze | Sony Interactive Entertainment (agreement to acquire, 2023) [SIE] | no tie found |
| Audio-Technica · Beyerdynamic · Dan Clark Audio · Final Audio · Focal · Grado · HiFiMan · Koss · Meze · Sennheiser · Spirit Torino · Stax · ZMF Headphones | not established | no tie found |
| Sony | the brand's own group (not separately sourced) | no tie found |
| **Denon** | Harman International (Samsung) since 2025-09-23 [H] | **ownership (of record)** |

| v0.20 skincare | Owner as found | Tie |
|---|---|---|
| Estée Lauder · La Mer · The Ordinary | The Estée Lauder Companies [ELC] | no tie found |
| Lancôme · SkinCeuticals · La Roche-Posay · CeraVe | L'Oréal [LOR] | no tie found |
| Dior Beauty | LVMH (Parfums Christian Dior) [LVP] | no tie found |
| Chanel Beauty | Chanel (v0.63 Entry 0 record) | no tie found |
| La Prairie | Beiersdorf [BDF] | no tie found (owner is an Iris client; La Prairie not named) |
| **Eucerin** | Beiersdorf [BDF] | **agency (search): Iris and Cheil, 2024** |
| Clé de Peau Beauté · Drunk Elephant | Shiseido [SHI] | no tie found |
| Rhode | e.l.f. Beauty (acquired, 2025) [ELF] | no tie found |
| Fenty Skin | not established (LVMH lists "Fenty Beauty by Rihanna", not Fenty Skin) [LVP] | no tie found |
| Cetaphil | Galderma [GAL] | no tie found |
| Sisley · Rare Beauty · Goop · Glossier · Augustinus Bader · Tower 28 · Paula's Choice · Bioderma | not established | no tie found |

| v0.21 cosmetics | Owner as found | Tie |
|---|---|---|
| MAC Cosmetics · Bobbi Brown · Tom Ford Beauty | The Estée Lauder Companies [ELC] (MAC's Korean site: 이엘씨에이한국(유) [MACKR]) | no tie found |
| NARS | Shiseido [SHI] | no tie found |
| Giorgio Armani Beauty · Maybelline · L'Oréal Paris · NYX Professional Makeup | L'Oréal [LOR] | no tie found |
| Fenty Beauty | LVMH maison "Fenty Beauty by Rihanna" [LVP] | no tie found |
| e.l.f. Cosmetics | e.l.f. Beauty [ELF] | no tie found |
| Hourglass · Chantecaille · Laura Mercier · Rare Beauty · Haus Labs · Pat McGrath Labs · Charlotte Tilbury · Huda Beauty · Kylie Cosmetics · Anastasia Beverly Hills · CoverGirl · Revlon · Wet n Wild · Milani Cosmetics | not established | no tie found |

| v0.22 automotive | Owner as found | Tie |
|---|---|---|
| **Chevrolet** | General Motors [GM] | **agency: Cheil Worldwide (GM Korea), 2017**; supply: none of record |
| Cadillac · Pontiac (last built 2010) · Oldsmobile (discontinued 2004) · Saturn (defunct 2010) | General Motors [GM] | no tie found (owner is a Cheil client; these brands not named) |
| **Bentley** | Volkswagen Group [VW] | **agency: Iris, 2021–2024 (Americas experiential)**; supply of record (v0.22) |
| Porsche · Volkswagen | Volkswagen Group [VW] | supply of record (v0.22); no other tie found |
| **BMW** | BMW Group [BMW] | **agency: Iris Culture, 2018 (UK consumer PR)**; supply of record (v0.22) |
| Rolls-Royce | BMW Group [BMW] | no tie found (owner's other brands served by Iris in 2018) |
| Mercedes-Benz | not established | supply of record (v0.22); no other tie found |
| Tesla | not established | supply: of record as "tangential" (v0.22); r3 found Samsung Electronics' $16.5 billion chip contract (2025–2033) [NBC] |
| Polestar | not established | supply of record as "tangential" (v0.22); no other tie found |
| Hyundai | not established | supply: Samsung SDI battery agreement, 2023 [KED] (not in v0.22's record) |
| Jaguar · Rivian · Lucid · Fisker · Toyota · Honda · Ford · Nissan · Plymouth · Mercury | not established | no tie found |

| v0.23 spirits | Owner as found | Tie |
|---|---|---|
| Johnnie Walker · Lagavulin · Casamigos | Diageo [DIA] | no tie found |
| Hennessy | LVMH (Wines & Spirits maison) [LVW] | no tie found |
| **Jack Daniel's** | Brown-Forman [BF] | **agency: Iris, 2022 (UK digital; since replaced)** |
| Woodford Reserve | Brown-Forman [BF] | no tie found (owner's Jack Daniel's served by Iris) |
| Patrón · Grey Goose · Bacardi · Bombay Sapphire | Bacardi Limited [BAC] | no tie found |
| Jameson · Redbreast · Monkey 47 · Del Maguey | Pernod Ricard [PR] | no tie found |
| Hendrick's · The Balvenie | William Grant & Sons, "a family-owned company" [WG] | no tie found |
| Rémy Martin | Rémy Cointreau [RC] | no tie found |
| Nikka | Asahi Group Holdings [NIK] | no tie found |
| Clase Azul · Fortaleza · Compass Box · Fernet-Branca · St. George Spirits · Mezcal Vago | not established | no tie found |

Source keys (all read 2026-11-11): [H] Harman release of record (above); [SIE] Business Wire, 2023-08-24, https://www.businesswire.com/news/home/20230824336695/en/Sony-Interactive-Entertainment-to-Acquire-Audeze-a-Leader-in-Audio-Technology-and-Developer-of-Award-winning-Headphones-for-Gaming; [ELC] https://www.elcompanies.com/en/our-brands; [LOR] L'Oréal Shareholder Guide 2026/2027, "Our portfolio of 40 global brands", https://www.loreal-finance.com/eng/shareholders-guide-2026/en/article/12/; [LVP] https://www.lvmh.com/en/our-maisons/perfumes-cosmetics; [LVW] https://www.lvmh.com/en/our-maisons/wines-spirits; [SHI] https://corp.shiseido.com/en/brands/; [BDF] https://www.beiersdorf.com/brands; [GAL] https://www.galderma.com/our-brands; [ELF] ABC News, 2025-05-28, https://abcnews.com/style/story/hailey-bieber-closes-1b-rhode-deal-elf-beauty-122287153; [MACKR] https://www.maccosmetics.co.kr/; [GM] https://en.wikipedia.org/wiki/General_Motors; [VW] https://en.wikipedia.org/wiki/Volkswagen_Group; [BMW] https://en.wikipedia.org/wiki/BMW; [NBC] and [KED] as above; [DIA] https://www.diageo.com/en/our-brands/brand-explorer; [BF] https://www.brown-forman.com/brands/; [BAC] https://www.bacardilimited.com/our-brands/; [PR] https://www.pernod-ricard.com/en/brands; [WG] https://en.wikipedia.org/wiki/William_Grant_%26_Sons; [RC] https://www.remy-cointreau.com/en/brands/; [NIK] https://en.wikipedia.org/wiki/Nikka_Whisky.

**Handling (proposed; listed for the pre-registrant, §9 of the r3 draft).**
1. **New ties handled like Denon.** Chevrolet, BMW, Bentley, Jack Daniel's and Eucerin stay in the registry, in coding and in every primary statistic and verdict (the comparison with English t₄ needs the same 112 units). A check without them is added: sensitivity **S-COI** removes the six units with a tie (Denon and these five; `params_v0_62.COI_FLAGGED`) from H_Lang_Presence in each language, beside S-Denon and S-Headphones; it never changes a verdict; if a primary verdict differs under S-COI, the paper reports both in its abstract (as default (3) of 2026-11-10 does for S-Denon and S-Headphones). Implemented in `score_v0_62.py` (unit-tested).
2. **Supply relationships** (Tesla, Hyundai): v0.22's handling (disclosed; no restriction); not in S-COI unless the pre-registrant adds them (a one-line change of `COI_FLAGGED`).
3. **Retail** (Hotel Shilla's duty-free business; DFASS): disclosed generally in the Declarations; no per-brand flag.
4. **Declarations.** The pre-registration's §COI keeps the v0.19 and v0.22 wording of record and adds the agency ties, the supply relationships and the retail channel (r3 draft §10). Samsung, Cheil and Iris are named only there and in this log.
5. **Independence rule** unchanged: no unit is focal; no lesson is addressed to a brand; no brand, agency or Samsung company has been or will be contacted.


### Part G — r3 update (2026-11-12): the pre-registrant's decisions (ex ante, before any study call)

- **Handling of Part F decided** (pre-registrant, 2026-11-12, 00:48 CT, "as you suggest"; pre-registration §9 item 8): the default as proposed, the programme's Cheil/Iris option (b). Chevrolet, BMW, Bentley, Jack Daniel's and Eucerin stay in every analysis, as Denon does, and every Presence result is also reported without them and Denon (S-COI, 106 units; `params_v0_62.COI_FLAGGED` unchanged). Tesla and Hyundai (supply) and Hotel Shilla (retail) stay disclosed, not flagged.
- **Brand questions** (§9 item 7 (b), same decision): the 88 yes/no brand questions of v0.19–v0.22 (block 4) are collected last; the v0.23 open brand questions (block 5) are not. No registry unit is added or removed; the COI handling above applies unchanged to block 4's descriptive.
