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

## Correction to Note 1 — 2026-11-07 (after acquisition)
- 19 of 22 Gemini 2.5 Flash calls ended at the cap (`MAX_TOKENS`), not every call: all 18 recommendation answers and K3. The three short answers (K1, K2, K4) ended normally. One Gemini 2.5 Flash-Lite answer (E1) also reached the cap.

## Entry 2 — 2026-11-07 (after scoring): D2 reported from the audited reading
- **What happened.** The coder audit (§5.6) agreed with the automated generation code on 86 of 86 responses, but the K4 regex mis-coded 2 of 6 answers (Sonnet 4.5: "Superseded" → audited "Current"; Gemini 2.5 Flash: "Unclear" → audited "Current"). Overall disagreement 2 of 92 audited codes (2.2%), under the 10% threshold.
- **Handling.** D2 is descriptive; the report shows the audited reading (all six models say the R1 is still in production) and discloses the automated codes. No confirmatory verdict uses K4.
- **Record.** `osf/v38/data/v38_coder_audit.json`.

## Entry 3 — 2026-11-07 (after scoring): post hoc five-model sensitivity (excluding Gemini 2.5 Flash)
- **Why.** Note 1: Gemini 2.5 Flash recommendation answers are truncated (1.5 registry brands per answer vs 3.9–6.2 for the other models).
- **Result (descriptive, not a verdict).** Aillio Presence: beginner 43.3%, enthusiast/prosumer 71.7% (Δ = 0.283). Behmor enthusiast/prosumer 66.7%, so Aillio's margin narrows from 0.111 (locked, six models) to 0.050 (five models). The locked verdicts stand; the report states the five-model margin.
