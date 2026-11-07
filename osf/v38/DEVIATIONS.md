# v0.38 — DEVIATIONS log

Contemporaneous record of any departure from PRE_REGISTRATION_v0_38.md (tag `v0.38-prereg-r1`).

- **At lock (2026-11-07):** none.

## Entry 1 — 2026-11-07 (before acquisition): external anchor = OSF deposit only

- **What happened.** `git push origin v0.38-prereg-r1` failed: GitHub rejected the stored credential ("Invalid username or token"). The tag exists locally at commit `f893c74`.
- **Anchor used.** The full lock set — PRE_REGISTRATION_v0_38.md, probes_v0_38.json, LOCK_MANIFEST_v0_38.sha256, brands_home_roasters_v0.38.json, acquire_v0_38.py, score_v0_38.py, test_score_v0_38.py — was uploaded to OSF `ec6wh` (`v38/prereg`, `v38/registries`, `v38/scripts`); the upload step reported success for every file at 2026-11-07T20:33Z.
- **Decision.** Pre-registrant approved proceeding to acquisition on the OSF anchor alone (2026-11-07).
- **Remedy.** Push the unchanged tag `v0.38-prereg-r1` once the GitHub credential is refreshed; the tagged commit's file hashes match the OSF-deposited manifest.
- **Effect on verdicts.** None; no locked content changed.

## Note 1 — 2026-11-07 (during acquisition): Gemini 2.5 Flash answers truncated by the shared output cap

- **Observation.** Every Gemini 2.5 Flash (M5) call returned `finish_reason = MAX_TOKENS`. The model's internal "thinking" tokens count against the same 2,048-token output cap as the visible answer, so the visible answer is cut off mid-list.
- **Not a deviation.** Decoding is exactly as pre-registered (§4.4) and unchanged since v0.23; no configuration was changed mid-run.
- **Programme-level scope.** The same pattern is visible in v0.23 raw data, which does not store finish reasons: only 1 of 6 Phase B and 3 of 24 Phase A M5 answers end cleanly, and M5 answers average 1,546 / 2,170 characters against 2,297–8,761 for the other five models. Earlier phases that used this configuration likely under-observe M5 mentions late in an answer.
- **Handling in v0.38.** M5 Presence is a lower bound. Confirmatory statistics are computed as locked; the report flags M5 truncation and adds a descriptive five-model sensitivity check (excluding M5), labelled post hoc.
