# AIAS 3.0 (Coverage) release: dated schedule from the pre-registration lock to about Tue 2026-12-15 (DRAFT)

Written Thu 2026-11-26 on branch `aias-3.0-prereg`, with the release pre-registration r0 (`osf/aias_3_0/prereg/PRE_REGISTRATION_aias_3_0.md`). Fixed dates come from locked or dated records (cited); the others are derived from them with the step lengths in `papers/aias_3_0/STILL_NEEDS_aias_3_0.md` (`6f27101`). Not deposited. Re-dated at r0b the same day (dates only): Pablo, Thu 2026-11-26, 7:39 am CT, via the control chat (Preview public ~Thu 12/10; 3.0 data lock right after the Preview's; ship ~Tue 12/15; v0.40 launch Mon 11/30); steps 13–14 are estimates derived from those dates.

| # | Date | Step | Depends on | Needs Pablo | Risk to 12/15 |
|---|---|---|---|---|---|
| 1 | Thu 11/26 | r0 drafts committed (pre-registration with the v0.43 amendment as Appendix A; DEVIATIONS Entry 0; draft S-Q entries for v1.12 and v1.19; this schedule) | D1–D4 (given 6:52 am) | no | none |
| 2 | Fri 11/27, morning (expected) | Drafts reach Pablo (control panel); the 24 hours start | 1 | reads it; may hold it or change a default (§17) | none |
| 3 | Sat 11/28, morning | **Lock**: choices applied, lock manifest, commit, tag `aias-3-0-prereg-r1`, push, anchor, OSF deposit `ec6wh/aias_3_0/` (2026, OSF); v0.43 Coverage amendment deposited to `v43/prereg/` | 2 (no hold) | no (automatic after 24 h) | a hold past about Wed 12/2 breaks the plan below (row 7 must run before t5; fallback) |
| 4 | Sat 11/28 – Sun 11/29 | S-Q DEVIATIONS entries appended and committed: v1.12 Entry 2, v1.19 Entry 2; added to their OSF anchors | 3 | no (text reviewed with the pre-registration) | low |
| 5 | Sat 11/28 – Mon 11/30 | Write and test (synthetic only) the S-Q wrapper `osf/methodology/v1_12/sensitivity/quotes_v1_12.py` and `osf/aias_3_0/scripts/score_aias_3_0.py` | 3 | no | about 2 sessions; the precision note (§17 choice 4) adds about 1 before the lock |
| 6 | Tue 12/1 | S-Q run once (reproduction check first): v1.12 and v1.19 S-Q verdicts | 4, 5 | no | low |
| 7 | Tue 12/1 – Wed 12/2 | Calibration and dissociation runs, once each (primary and S-Q together) | 5, 6 | no | must finish before Thu 12/3: t5 collects 12/3 – 12/6 (`v0_45` pre-registration, `f827d9d`) and no heavy Mac job runs beside a locked collection. If missed: after t5 and the v1.21 judge that follows it (from Mon 12/7 06:00 UTC, v1.21 §13), which moves the data lock past ~12/6 and puts 12/15 at risk |
| 8 | Thu 12/3 – Sun 12/6 | t5 window (no release runs) | – | no | – |
| 9 | after 6, if a published value is wrong under S-Q | Dated OSF note beside the v1.12 / v1.19 paper and a corrections-log row the same day | 6 | yes (§17 choice 7: confirm) | low |
| 10 | ~Fri 12/4 – Sat 12/5 | AIAS 6.0 Preview data lock, the day v1.14 Stage 2 exists (control chat, Thu 11/26, 7:13 am; was Fri 12/11); its Coverage rows (G3) read once they exist | Preview (locked Nov 11); t5 collection (from Thu 12/3); v1.14 Stage 2 | no | if the Preview slips, the release goes ahead without G3 and adds it by dated addendum before the paper lock |
| 11 | ~Sat 12/5 – Sun 12/6, right after row 10 | **Release data lock** `aias-3-0-data-locked`: class computed mechanically (pre-registration §6.2) | 7, 10 | no; class C pauses drafting and goes to Pablo | class C (Coverage not separable from P and C\* together) stops the release for his decision |
| 12 | Mon 11/30; ~Thu 12/10 | v0.40 launch (Mon 11/30, was Mon 12/14) and the Preview's publication (~Thu 12/10, as soon as it is ready; was Tue 12/15) take precedence (control chat, Thu 11/26, 7:39 am) | – | – | Mac and review time used by them |
| 13 | Mon 12/7 – Fri 12/11 (estimate) | Charts, paper (`build_aias3.py --mode final`; W3 replaces the retest sentences), report, page-by-page visual pre-flight | 11 | yes: the full-size "Curved slats" cover file and the report code | missing cover file or report code delays the report |
| 14 | Sat 12/12 – Mon 12/14 (estimate) | Fable review of the full draft (milestone rule); fixes | 13 | no | Fable usage availability `[OPEN]` |
| 15 | **~Tue 12/15** | **Ship**: OSF deposit `ec6wh/aias_3_0/` (paper, report, outputs, data lock), website (study page `content/pending/aias-3-0.json`, keep-up lines, Claims Register rows), GitHub push | 14 | no (automatic) | a slip past Thu 12/31 moves the deposit to Zenodo (needs his Zenodo token and the December test deposit) |
| – | from Tue 12/1 (monthly, v0.43 §4.5) | v0.43 monthly snapshots continue (not analysed for Stage 2) | – | no | – |
| – | Wed 2027-03-10 → Fri 2027-03-12 at the earliest | v0.43 Stage 2 outcome pulls; Coverage predictive result (registered in 3.0, reported later) | 3 | no | not part of 3.0 by design |
| – | March 2027 | Keepa sales-rank month (separate amendment before the pull) | his go | **yes**: spend and account | not part of 3.0 |

**Cannot make 12/15, by design:** the Coverage predictive result (not before Fri 2027-03-12); Coverage over time (D2: no retest in 3.0; t5 carries no Coverage block; t6 targets 2027-02-12 and repeats t4's design); the Keepa sales-rank leg (needs his go; March 2027); #32b and #33 ("no, later").

**Can slip 12/15:** a hold of the pre-registration past about Wed 12/2; the release runs not done before Thu 12/3 and then delayed behind t5 and the v1.21 judge; the Preview's data lock slipping (handled by addendum, not by waiting); a class-C outcome (pause for his decision); the cover file or report code not arriving by about Mon 12/7; the Fable review not available 12/12 – 12/14.

**Fallback:** Fri 2027-01-08 (the control panel's forecast for AIAS 3.0, `STILL_NEEDS_aias_3_0.md`). A January release deposits on Zenodo under the deposit rule of Nov 25, which needs his Zenodo token and the December test deposit; the pre-registration and the v0.43 amendment stay on OSF (deposited in 2026).
