# AIAS v0.62 — DEVIATIONS log

Non-English wave (French and Japanese) of the t₄ omnibus panel. Entries are numbered; Entry 0 is the pre-acquisition conflict-of-interest screen required for every phase. It documents how conflicts are handled; it is not a blanket "no affiliation" finding.

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
