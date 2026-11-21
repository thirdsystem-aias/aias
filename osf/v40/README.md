# AIAS v0.40 — US airlines and retail banks

OSF deposit for AIAS™ Presence Measurement Protocol, v0.40.

**Status:** pre-registration locked; data collected; scoring, audit, paper and report complete.

- **Pre-registration lock:** git tag `v0.40-prereg-r1` (tag object `164a2a9f6acc4c7c52f5013d1b934d27b52e17d1`, commit `a53d2b7c1fda8f62381d1cf9787f1e549941ee87`), 2026-11-16 19:00 CT.
- **OSF anchor:** project https://osf.io/ec6wh/ — `v40/prereg` (17 files) and `v40/registries` (18 files), deposited and verified by SHA-256 on 2026-11-17 (01:07–01:08 UTC). Anchor record: `anchor/osf_anchor_v0_40.json`.
- **Data collection:** 2026-11-17 to 2026-11-21 (collection started 2026-11-17; acquisition locked 2026-11-19 at tag `v0.40-acquisition-locked`, 2,821 of 2,821 calls ok, no re-runs; scoring and audit through 2026-11-21).
- **Deviations from the pre-registration:** see `DEVIATIONS.md`.

## Tree

- `data/` — acquisition outputs; `data/raw/` holds the public BTS and FDIC files the registry is built from (not in git)
- `prereg/` — locked pre-registration artifacts (content module + mega-prompt)
- `anchor/` — OSF anchor record written at collection start
- `audit/` — AI audit of the coded sample and its agreement statistics
- `scripts/` — registry builder, acquisition, scoring and audit code
- `registries/` — brand registry: hand-sourced inputs, builder outputs (`out/`) and raw-data checksums; frozen at the lock

## Files for the OSF results deposit (SHA-256)

Deposit target: OSF project `ec6wh`, path `v40/`. Deposit status at the time of this commit: not yet uploaded (OSF authentication was unavailable); the hashes below are of the local files to be deposited and must be re-verified after upload.

| File | SHA-256 |
|---|---|
| `data/v40_raw.jsonl` | `c43535e3d9f67e2686ea5d3b41f25e7bdc7bc4f980a350d51d06137c4f2d947f` |
| `data/v40_coded_answers.csv` | `cd5bd02643ee788064a8dca80b94df849643bcf5d3a6a75739aa6c21ca9a9468` |
| `data/v40_mentions.csv` | `0a83b397fa00401cef70570a35e3c443e318e52213752a261f79ac5de14dfffe` |
| `v40_verdicts.json` | `996614d1fda809720dea82e9f9fca88f979e447f87c3ca0dd2e89544222c0691` |
| `v40_values.json` | `9479b8f9b0f4747bd0f46bd14a5a498f16d3aa543fbc4d4c8d53006a9318937b` |
| `v40_postscore.json` | `aab2442f12e73f89cf0ba4b498f2aa8be3b3777dba91c8b961f6a918bb0cc00c` |
| `audit/v40_audit_agreement.json` | `8eccbe21074f9c81907de1b84db80b4552a576f1bf9dc8faa848f16c852ff11f` |
| `audit/v40_audit_agreement.md` | `c25ee13ab0592d415571e8c06425bff4fed247678d38fc608d26ef6da1c4038d` |
| `reports/TS-FL-v0.40-r1_leaders-challengers-and-ghosts.pdf` | `fb8b0fa4c0c5b0451e39f09410771b3189294ca989d9802ec44c83daae931562` |

The report PDF lives in `reports/output/` of the repo (built by `reports/build_report_v40.py`), not in this tree.
