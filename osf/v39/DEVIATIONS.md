# v0.39 — DEVIATIONS log

Contemporaneous record of any departure from PRE_REGISTRATION_v0_39.md (tag `v0.39-prereg-r1`).

- **At lock (2026-11-08):** none.
- **Declared at lock, not deviations:** the external anchor is the OSF deposit of `v39/prereg`, `v39/registries` and `v39/scripts`; the tag is pushed to `origin` once the GitHub credential is restored (v0.38 DEVIATIONS, Entry 1). Gemini 2.5 Flash answers that end at the 2,048-token cap are expected and handled by D10 (pre-registration §2.6, §6.6).

## Note 1 — 2026-11-08 (before acquisition): tag push attempted; anchor unchanged
- **What happened.** The pre-registrant's go to start acquisition was received at 06:24Z. At about 06:27Z `git push origin refs/tags/v0.39-prereg-r1` was attempted once and failed because no GitHub credential is stored ("could not read Username for 'https://github.com': terminal prompts disabled"). The tag remains local at commit `58196cc`; `origin` holds no v0.38 or v0.39 tag.
- **Not a deviation.** The OSF deposit of the lock set is the declared external anchor (pre-registration header; entry above). Before launch the lock manifest re-verified 9/9 (`shasum -a 256 -c`), and the copies in `osf/v39/scripts/` are byte-identical to `scripts/`.
- **Acquisition.** Launched 2026-11-08T06:28:43Z on the pre-registrant's Mac (`nohup caffeinate -ims python3 -u scripts/acquire_v0_39.py`; log `logs/v39/acquire_v0_39.log`, not deposited).

## Note 2 — 2026-11-08 (acquisition): completed as locked
- **Outcome.** 360/360 calls returned `ok` at the first attempt (no transient retries, no `pause_turn` continuations); first call 06:28:44Z, last 08:12:48Z. Every call was served by the snapshot recorded in pre-registration §4.3. Raw file `data/v39_raw.json`, sha256 `fbc3db92166dae7a7d9062ec0fcaebf0fe244251e83ecdab27bfabe8216f6e43`.
- **Expected truncation (§6.6, not a deviation).** Gemini 2.5 Flash (M5) ended 26 of its 30 answers at the 2,048-token cap (`MAX_TOKENS`); Gemini 2.5 Flash-Lite (M6) ended 1 of 30 there. Handled by D10.
- **Search behaviour (§6.2, kept as recorded).** In S1, Claude Opus 5.5 searched in 25 of 30 calls, GPT-6 Astra in 30 of 30, Gemini 4 Argon in 12 of 30. No search-tool errors were returned.
