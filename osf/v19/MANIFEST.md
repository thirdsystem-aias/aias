# MANIFEST — AIAS v0.19 OSF Deposit

**Phase:** v0.19
**Pre-reg tag:** `v0.19-prereg-r1`
**Pre-reg commit:** `2cbd36c6ed53b99c65490765d3d9f1a2eb49b890`
**Deposit state:** PRE-ACQUISITION

SHA256 hashes are computed against the locked artifacts at git commit and filled in below. Post-acquisition artifacts append rows as they are produced.

---

## Pre-registration artifacts (locked)

| File | Purpose | SHA256 | Size |
|---|---|---|---|
| `PRE_REGISTRATION_v0_19.md` | Canonical pre-registration document | `<HASH_TBD>` | `<SIZE_TBD>` |
| `panel_registry_v0_19.csv` | Locked 16-brand panel | `<HASH_TBD>` | `<SIZE_TBD>` |
| `thresholds_v0_19.json` | Locked decision-rule thresholds | `<HASH_TBD>` | `<SIZE_TBD>` |
| `score_v0_19.py` | Pre-registered scoring pipeline | `<HASH_TBD>` | `<SIZE_TBD>` |
| `acquire_v0_19.py` | Pre-registered acquisition tooling | `<HASH_TBD>` | `<SIZE_TBD>` |

## Operations log

| File | Purpose | SHA256 | Size |
|---|---|---|---|
| `DEVIATIONS.md` | Departures from pre-registered protocol | `<HASH_TBD>` | `<SIZE_TBD>` |
| `README.md` | Deposit documentation | `<HASH_TBD>` | `<SIZE_TBD>` |
| `MANIFEST.md` | This file | (self-reference) | — |

## Query batches (generated at pre-reg state for transparency)

| File | Purpose | SHA256 | Size |
|---|---|---|---|
| `phase_a_queries.jsonl` | 96 Phase A queries (16 brands × 6 panel models) | `<HASH_TBD>` | `<SIZE_TBD>` |
| `phase_b_queries.jsonl` | 36 Phase B queries (6 frames × 6 panel models) | `<HASH_TBD>` | `<SIZE_TBD>` |

## Acquisition data (post-acquisition)

| File | Purpose | SHA256 | Size |
|---|---|---|---|
| `phase_a_responses.jsonl` | Raw Phase A model responses | (post-acquisition) | (post-acquisition) |
| `phase_b_responses.jsonl` | Raw Phase B model responses | (post-acquisition) | (post-acquisition) |
| `phase_a_results.csv` | Parsed Phase A C_P data | (post-acquisition) | (post-acquisition) |
| `phase_b_results.csv` | Parsed Phase B mention data | (post-acquisition) | (post-acquisition) |

## Post-acquisition shipping artifacts

| File | Purpose | SHA256 | Size |
|---|---|---|---|
| `scoring_output_v0_19.txt` | Canonical scoring output | (post-acquisition) | (post-acquisition) |
| `Third_System_brand_format_report_v0_19.pdf` | Brand-format report | (post-acquisition) | (post-acquisition) |
| `v0_19_ssrn_paper_draft.md` | SSRN paper draft | (post-acquisition) | (post-acquisition) |
| `figures/chart_01_*.pdf` | Scoring-output figures | (post-acquisition) | (post-acquisition) |

---

## Hash computation

To populate the hashes for the locked artifacts at commit time:

```bash
for f in PRE_REGISTRATION_v0_19.md panel_registry_v0_19.csv thresholds_v0_19.json score_v0_19.py acquire_v0_19.py README.md DEVIATIONS.md phase_a_queries.jsonl phase_b_queries.jsonl; do
  hash=$(sha256sum "$f" | awk '{print $1}')
  size=$(wc -c < "$f")
  echo "$f  $hash  $size bytes"
done
```

Update the table above with computed values, commit, then tag `v0.19-prereg-r1`.
