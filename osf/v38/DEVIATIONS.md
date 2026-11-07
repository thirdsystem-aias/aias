# v0.38 — DEVIATIONS log

Contemporaneous record of any departure from PRE_REGISTRATION_v0_38.md (tag `v0.38-prereg-r1`).

- **At lock (2026-11-07):** none.

## Entry 1 — 2026-11-07 (before acquisition): external anchor = OSF deposit only

- **What happened.** `git push origin v0.38-prereg-r1` failed: GitHub rejected the stored credential ("Invalid username or token"). The tag exists locally at commit `f893c74`.
- **Anchor used.** The full lock set — PRE_REGISTRATION_v0_38.md, probes_v0_38.json, LOCK_MANIFEST_v0_38.sha256, brands_home_roasters_v0.38.json, acquire_v0_38.py, score_v0_38.py, test_score_v0_38.py — was uploaded to OSF `ec6wh` (`v38/prereg`, `v38/registries`, `v38/scripts`); the upload step reported success for every file at 2026-11-07T20:33Z.
- **Decision.** Pre-registrant approved proceeding to acquisition on the OSF anchor alone (2026-11-07).
- **Remedy.** Push the unchanged tag `v0.38-prereg-r1` once the GitHub credential is refreshed; the tagged commit's file hashes match the OSF-deposited manifest.
- **Effect on verdicts.** None; no locked content changed.
