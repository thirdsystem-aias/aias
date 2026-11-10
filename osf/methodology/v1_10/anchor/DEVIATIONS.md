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
