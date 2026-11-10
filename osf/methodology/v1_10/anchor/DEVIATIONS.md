# DEVIATIONS — v1.10 (Ranking, Paper A)

## Entry 0 — ex ante (2026-11-10, before the lock)

**Type:** ex ante (COI screen, pre-lock record, anchor preamble). No rank statistic has been computed on confirmatory data.

**COI screen.** No new brand selection. Each substrate keeps the COI handling of its source phase, quoted verbatim from the source records:

- v0.19 audiophile headphones, `osf/v19/PRE_REGISTRATION_v0_19.md` §2.3: "**AKG removed from Cell A short-list; Denon substituted.** AKG is Samsung-owned since 2016. The author's COI declaration names Samsung; including AKG would invite the kind of reviewer suspicion AIAS™ 1.0 does not need to absorb. Denon carries comparable heritage stature (founded 1910; AH-D7000 → D9200 audiophile line) and removes the question. Decision rationale recorded here for audit trail."
- v0.22 automotive, `prereg/v0_22_mega_prompt.md`, DEVIATIONS Entry 0, Part B: "**Screen result:** Three of the 24 brands in the locked v0.22 registry have tier-2/3 supply relationships with Samsung Electronics America (author's primary employer) via Samsung subsidiaries: BMW (Harman audio + Samsung SDI batteries + Samsung Display infotainment), Mercedes-Benz (Harman audio + Samsung Display infotainment), and Volkswagen Group brands including Bentley and Porsche (Samsung SDI battery supply to Stellantis-adjacent platforms). Tesla and Polestar also have tangential Samsung-component exposure at the parts level."

The EARLY-6 and EARLY-2 registries (PM software, personal finance, olive oil, running shoes, skincare, household retail, knives, premium tea, kitchen knives) were string-screened on 2026-11-10 for Samsung and the brand names of its subsidiaries (Harman, JBL, AKG, Harman Kardon, Infinity, Mark Levinson, Revel, Lexicon, Arcam, and the Sound United brands): no match. v0.28's technology panel is pinned and parse-checked only, pending its own COI screen. The program's two held studies are excluded.

**COI re-check (2026-11-10).** The current ownership of the carried-forward registry brands was re-checked on 2026-11-10. The handling of its result awaits the author's decision; the result and its handling will be entered in this log, and in the paper's declarations, before any v1.10 result is reported. Sensitivity S7 reports every gate statistic without any brand that the re-check flags.

**Pre-lock record.** Development sample: v0.17 and v0.18 phase B (36 answers) were parsed for feasibility (`prereg/feasibility_v1_10.md`); both are excluded from every confirmatory analysis. Pre-lock parity on the real files (`prereg/parity_v1_10.json`, §9a): MQ1, MQ2 and the unit join only; the rank extractor was never called on a real answer file. Disclosed exposures during the schema survey: two rows of the published AIAS 2.0 profiles table (P and C\* of two v0.19 brands at t1) were printed once; the distinct values of the v0.9 PM `primary_recommendation` column (brand names, no counts) and the first distinct values of the v0.19 coded `rank` column (values not linked to brands) were printed. No rank statistic was computed from them.

**Anchor preamble.** Content lock → `prereg/LOCK_MANIFEST_v1_10.sha256` → commit → tag `v1.10-prereg-r2` → push → `anchor/git_anchor_v1_10.json` → OSF deposit of `prereg/`, `registries/`, `anchor/` with SHA-256 verified → only then `score_v1_10.py --stage S` (it refuses without the tag and the anchor file).

## Entry 1 — r1 superseded by r2 before any computation (2026-11-10)

**Type:** ex ante for r2 (no rank extraction, no statistic computed under r1).

**What happened.** Tag `v1.10-prereg-r1` (commit 672365b) was pushed and deposited on OSF at 07:50–07:55 CT. The first `score_v1_10.py --stage S` run halted at `verify_manifest()`: `INPUTS_MANIFEST_v1_10.json` pinned `registries/REGISTRY_CHOICES_v1_10.md` at its hash from before the content lock, when the runner had changed that file's header line from "Draft r1, 2026-11-10." to "r1, 2026-11-10 (locked with the pre-registration)." No loader reads that file; the halt is the designed response to any hash mismatch.

**Change.** r2 rebuilds the input manifest (and the parity record that carries the manifest hash), updates the tag named in the scorer's refusal check, and is tagged `v1.10-prereg-r2`. No rule, threshold, seed, input data file or analysis step changed. r1 stays in the record (tag and OSF versions).

## Entry 2 — COI re-check result and its handling (Tue Nov 10, 2026)

**Type:** ex ante for Stage C. Written after Stage S (commit 0399a0b) and before Stage C: no Stage C statistic has been computed, and `anchor/coi_flags_v1_10.json` did not exist before this entry. Stage S is unaffected (it used EARLY-6 data only, whose registries contain no flagged brand).

**Result.** The re-check of registry-brand ownership that Entry 0 announced and sensitivity S7 (§10) requires found one flagged brand: **Denon**, in the v0.19 audiophile-headphones registry (`osf/v19/panel_registry_v0_19.csv`, Cell A_Heritage), chosen before the v0.19 lock in place of AKG.

Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026.

Primary source: HARMAN press release, Business Wire, September 23, 2025, "HARMAN Completes Sound United Acquisition to Expand Premium Audio Leadership", https://www.businesswire.com/news/home/20250923135384/en/HARMAN-Completes-Sound-United-Acquisition-to-Expand-Premium-Audio-Leadership. The release describes HARMAN as "a wholly-owned subsidiary of Samsung Electronics Co., Ltd." and lists Denon among the Sound United brands acquired from Masimo Corporation.

**Other registry brands.** The 112 brands of the v0.19–v0.23 registries (16 + 4 × 24), canonical names and aliases as the scorer loads them, were screened on 2026-11-10 against Samsung, Harman and Harman's brands (JBL, AKG, Harman Kardon, Infinity, Mark Levinson, Revel, Lexicon, Arcam) and the Sound United brands named in the release (Bowers & Wilkins, Denon, Marantz, Definitive Technology, Polk Audio, HEOS, Classé, Boston Acoustics). Denon is the only match (a string hit on "Martin" is Rémy Martin, a cognac brand). No other registry brand is owned by Harman, Sound United or another Samsung-group company, to the runner's knowledge after reviewing the list; no per-brand ownership filings were consulted beyond the source above. The EARLY-6 and EARLY-2 registries were screened in Entry 0 (no match).

**v0.22 automotive.** The registry carries the disclosed tier-2/3 supply relationships of its source phase (Harman International audio systems, Samsung SDI battery cells, Samsung Display infotainment; non-competitive, no brand-level overlap, no restriction on registry composition; v0.22 DEVIATIONS Entry 0 Part B and v0.22 Declarations, quoted in Entry 0). These are supply relationships, not ownership: S7 removes brands that the ownership re-check flags, and no v0.22 brand is owned by a Samsung-group company. No v0.22 brand is therefore flagged or removed; the relationship keeps its source-phase handling (disclosed, no restriction) and is disclosed again in the paper's declarations.

**Handling (as S7 prescribes, plus one addition).**

1. Primary analysis unchanged. Denon stays in the locked v0.19 registry, in extraction, in the Stage S rank tables (hashed) and in every primary statistic and verdict (H1–H6, MQ6, baseline). Nothing locked changes (§13 rule 4).
2. S7 as pre-registered. `anchor/coi_flags_v1_10.json` lists the unit (v0.19, Denon). The scorer recomputes H1–H3 with that unit removed from every correlation at every wave; answers are not re-ranked (the other brands keep the positions they hold with Denon in the answer). S7 never changes a verdict; any verdict that differs under S7 is listed next to the primary verdict.
3. Addition (Pablo's go, Tue Nov 10, 2026, 7:21 am CT): headphone results are also reported without Denon. Every v0.19 result the paper reports (the §8 baseline rows for v0.19 at each wave and any per-substrate value) is given a second time without the Denon unit, on the S7 rule (unit removed, answers not re-ranked). Because it is added after the lock, it is labelled descriptive and exploratory, is computed outside the locked scorer from the Stage C outputs and the hashed rank tables, and changes no verdict.
4. Declarations. The paper's conflict-of-interest section carries the v0.19 disclosure from its locked record followed by the correction above, and the v0.22 disclosure from its locked record. This entry precedes every v1.10 Stage C result, as Entry 0 requires.

**Effect on inference.** None on the primary analysis or on any verdict. S7 shows how the gate statistics move without the one Samsung-group brand. The flags file is not a frozen input (decision 12, §15); `--stage C` records its SHA-256 in `v1_10_verdicts.json`. This log is append-only: the r2 lock state of this file is the hash in `prereg/LOCK_MANIFEST_v1_10.sha256` at tag `v1.10-prereg-r2`.
