# AIAS 3.0 (Coverage release) — DEVIATIONS

Every change after the lock (tag `aias-3-0-prereg-r1`) gets an entry: id, date, ex ante or ex post, what, why, effect on inference. Tests, bands, floors, seeds, candidates, constraints, the selection rule and the wording rules do not change after the lock; anything added later is exploratory. Entries are appended, never edited.

## Entry 0 (ex ante, draft written with pre-registration r0, 2026-11-26)

**State of the data.** No output of the release exists: no file under `osf/aias_3_0/outputs/`, no release scorer, no quotes-normalised (S-Q) table of v1.12 or v1.19. Nothing was called, collected, pushed or deposited.

**What the drafting lane read** (beyond the records in pre-registration §0.1): `~/aias/Try system book/CLAUDE.md` (identity and COI rules, pre-registration discipline, AI-use statement, collection budget, Amazon data, Denon / Harman, S&P lessons); `aias_roadmap_ssot.md` (fast track and release names; Phase Q list); the project doc `claude/control-chat-handoff.md` (standing rule on sales rank) through the project search; the value lines printed by `papers/aias_3_0/sources_aias3.py` and `tokens_aias3.py` (`6f27101`); the headers of `v112_unit_table.csv` (`949be61`) and `v42_brand_table.csv` (`31c64c6`); the `H_Gen_Presence` and `H_Gen_Phi` entries of `v42_verdicts.json` (`31c64c6`) and `v42_verdicts_SQ.json` (`47f1748`); `git grep` for the seeds 330000–330099 and 430051. No Coverage answer, mention or score was opened or computed by the drafting lane; the counts of affected answers quoted in pre-registration §10.2 come from the pre-build's read-only count (`STILL_NEEDS_aias_3_0.md`, `6f27101`).

**Conflict-of-interest handling.** The release selects no brand; it carries forward Paper A's declaration (v1.12 paper, `86b929a`), quoted verbatim in the pre-registration's §15, including the November 10, 2026 Denon correction and the five agency-work brands. All six flagged units stay in every analysis; every statistic is also reported without them (SA, S-COI).

**Anchor sequence.** Pre-registration §0 ("Locks on") and §16.
