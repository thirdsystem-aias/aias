# v0.46 (proposed) "From named to chosen" — DEVIATIONS

DRAFT r1 (Entry 0 r1, 2026-11-24) — for Pablo's review; not locked. Entries are written ex ante; Entry 0 r1 completes to-do item (a) below; items (b) and (c) await the pre-registrant's decision.

## Entry 0 — Pre-acquisition COI screen of the registries used (ex ante, r0 2026-11-11; r1 2026-11-24)

**Subject.** The author's employer, Samsung Electronics America, and the Samsung group (Samsung Electronics and its subsidiaries, including Harman International; Samsung affiliates including Cheil Worldwide and its Iris agency). Registries used: v0.20 skincare, v0.21 cosmetics, v0.22 automotive, v0.23 premium spirits (90 live units: skincare 24, cosmetics 24, cars 18, spirits 24). r0 said 91; the count is 90 since the D7 record of 2026-11-24 moved Fisker to Cell D (manuscript r4, commit 3c98818: 90 live units, 756 choice calls, 1,260 calls in all). Not used: v0.19 audiophile headphones.

**Handling carried forward from the source phases (conformed to their locked records, not paraphrased from memory).**
- v0.20 skincare: the v0.20 Entry 0 screen found "none of the 24 brands in the locked registry is affiliated with Samsung" (`papers/v0_20/v0_20_ssrn_paper_draft.md`, Entry 0, 2026-05-21).
- v0.21 cosmetics: "no brand in the v0.21 registry is affiliated with Samsung Electronics America" (`papers/v0_21/v0_21_ssrn_paper_draft.md`, pre-acquisition observations).
- v0.22 automotive: Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands — Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) — characterized as non-competitive with no brand-level overlap; no operational restriction on registry composition (v0.22 Declarations; v0.22 DEVIATIONS Entry 0, Part B). Wording as carried by v0.42 §8.
- v0.23 premium spirits: no tie of record in v0.23's own screen. Note for r1: the conflict-of-interest paragraph of `papers/v0_23/v0_23_ssrn_paper_draft.md` (l. 315) describes automotive supply relationships (Mercedes-Benz, BMW, Bentley, Porsche, Tesla, Polestar) under the words "the v0.23 registry"; those brands are v0.22's, so the paragraph appears to have been carried over from v0.22. It is flagged here and not repeated; the pre-registrant decides whether v0.23 needs an erratum note.

**Findings after the source phases (v0.62 DEVIATIONS Entry 0, Part F, r3 working draft on branch v0.62, f09068f; sources read there on 2026-11-11).**
- Cheil Worldwide or its Iris agency has done agency work for Chevrolet (GM Korea, 2017), BMW (BMW Group UK consumer PR, 2018), Bentley (Americas experiential, 2021), Jack Daniel's (UK digital, 2022) and Eucerin (Beiersdorf search marketing, 2024). Proposed handling, as v0.62: units kept; every result also reported without them (S-COI). The handling of these ties beyond v0.62 waits for the pre-registrant's call (CLAUDE.md, COI notes of 2026-11-11).
- Supply relationships beyond v0.22's record: Tesla (Samsung Electronics semiconductor contract, 2025) and Hyundai (Samsung SDI battery supply agreement, 2023). v0.22's handling applies (disclosed, non-competitive, no restriction on registry composition), as v1.10 DEVIATIONS Entry 2 ruled for supply relationships.
- Samsung-affiliated retail (Hotel Shilla duty-free): a retail channel, not treated as a tie.

**Category exclusion.** Audiophile headphones (v0.19) are excluded because the Samsung group competes in the category: Harman International owns AKG and JBL and, since September 23, 2025, the Sound United brands Bowers & Wilkins, Denon, Marantz, Polk Audio and others (What Hi-Fi, 2025-09-23, opened 2026-11-11). The v0.19 registry holds Denon, a Samsung-group brand (programme correction of 2026-11-10), and an OPEN choice could name any Harman brand.

**To do in r1 (before the lock), as written in r0.** Re-run v0.62's string screen (`coi_screen_v0_62.py`, 70 terms) on the 91 live units and on the OTHER-coding exclusion list; add a rule that an OPEN choice of any Samsung-group brand (Samsung, Harman and its brands) is coded and reported but excluded from every test. Conform the final wording to the v0.62 record once v0.62 is locked.

**r1 (2026-11-24, Tue), item (a): string screen re-run — done.**
- *Script.* v0.62's `osf/v62/scripts/coi_screen_v0_62.py` as committed on branch v0.62 at f09068f (git blob `b128979f61ae275042c62c46da9fdaa42f91c542`, SHA-256 `853c89eb9a981b22afe4be75d22b477f66907f4a47ba243a4e2bd66ca16a14ff`; the same file in the v0.62, v0.62-nohand and v0.65 worktrees). Its own term lists and match function are imported unchanged by `osf/v46/scripts/coi_screen_v0_46_r1.py`, which halts if the blob differs. Run offline; no model called, no key used.
- *Terms.* 70 (30 r0 + 40 r3), whole-word, case-sensitive, names only.
- *Units.* The 90 live units (`build_probes_v0_46.live_units()`, Fisker in Cell D), checked to equal the units on the LIST orders of `osf/v46/prereg/probes_v0_46.jsonl` (SHA-256 `1b6a4bc9…db30e01`).
- *Result.* **0 hits** (`matches: 0`). Output `osf/v46/data/coi_screen_v0_46_r1.txt`, SHA-256 `65a752eb2c8ed66eed4f57084217e6b7a4bd696e88a7919b0576f414c36c26d2` (also in `coi_screen_v0_46_r1.sha256`). Meaning: no live unit's name contains a Samsung-group name of record. v0.62's single match (Denon) belongs to v0.19, which #76 does not use. A name check is not an ownership check; the five agency ties found by sources (Chevrolet, BMW, Bentley, Jack Daniel's, Eucerin) and the supply ties above are not string matches and stand as recorded above.
- *OTHER-coding exclusion list.* Not screened. v0.62's screen reads registry names only (its alias table) and has no OTHER list; #76 has no OTHER-coding exclusion list in the prereg, the r5 manuscript or the code, and OTHER text exists only after collection. Whether such a list is to be screened belongs with item (b).

**Pending author decision (1) — item (b), not done in r1.** A rule that an OPEN choice of any Samsung-group brand (Samsung, Harman and its brands) is coded and reported but excluded from every test. Awaits the pre-registrant; manuscript and code unchanged on this point.

**Pending author decision (2) — item (c), not done in r1.** Whether the supply ties beyond v0.22's record (Tesla, Hyundai; above) are added to the manuscript's conflict-of-interest declaration. Awaits the pre-registrant; the Declarations carry no Tesla/Hyundai line.

The final wording is still to be conformed to the v0.62 record once v0.62 is locked.
