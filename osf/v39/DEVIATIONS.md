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

## Note 3 — 2026-11-08 (after acquisition): section 3.3 audit and the single scoring run
- **Section 3.3 audit (binding).** 174 responses carry a Bellwether (B01) or Stronghold (B06) match: 668 matches (B01 532, B06 136). Matches followed by a brand-specific word or capitalised mid-sentence were confirmed as proper-noun uses by class, with a seeded spot-check of 40 read in context; the remaining 140 were read individually. No match is a common-noun use; nothing was removed. Record: `data/v39_audit_commonnoun.json`. Reading lists come from `scripts/audit_worklist_v0_39.py`, an analysis aid written after acquisition that imports the locked scorer and does not change any coding.
- **Scoring.** `scripts/score_v0_39.py` (unchanged; lock manifest 9/9 re-verified and `test_score_v0_39.py` passing immediately before) ran once on the acquired data with the complete audit; status FINAL. H_CEP CONFIRMED (delta 0.25, p 0.0015); H_CEPDefault FALSIFIED (Bellwether rank 7, margin -0.25); H_Frame CONFIRMED (venting 0.944, ventless 0.000); H_Search FALSIFIED (delta -0.056, p 0.891); MC_Constraint PASS (0.528); MC_Boundary PASS (neither pre-boundary model attributes any generation token).
- **Independent check.** `scripts/verify_v0_39.py`, written after acquisition, re-implements brand matching, the lexicons, the permutation test (own random stream, 20,000 permutations; p = 0.00135) and the McNemar test without importing the scorer. It agrees with every verdict input and with the per-response Bellwether and frame codes.

## Note 4 — 2026-11-08 (after scoring): section 5.7 coder audit
- **Agreement.** 11 of 132 audited codes disagree with the locked automated coding (8.3%: 1 frame code, 5 K1/K2/K4 generation codes, 2 K3 and 3 K5 candidates), below the 10% threshold; no sensitivity re-computation is required and no disagreement touches a confirmatory verdict. Shop-awareness agrees 12/12. Record: `data/v39_coder_audit.json`.
- **D4.** Every ventless attribution to a brand other than Bellwether is labelled unverifiable: the locked fact sheet (§3.5) carries a specification only for Air-Motion, which no answer names. Contradictions between the panel's own answers are reported descriptively.
