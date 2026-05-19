# Phase A Lock — v0.17 Premium Kitchenware

**Status.** Phase A complete; operational panel locked for Phase B onward.
**Locked at git commit.** `7aabb53` (tag: `v0.17-phase-a-locked`).
**Substrate.** Premium kitchenware (per pre-reg §1).
**Methodology.** AIAS Presence Measurement Protocol v1.3 §6.4.2 (operator-judgement classification) as superseded for Phase A by provisional v1.4 §6.4.2 (automated LLM classifier) per DEVIATIONS Entries 4–5.
**Pre-registration of record.** `v0.17-prereg-r1` (commit `3ebe426`; §8 hash backfill at `04b624f`).
**Date locked.** 2026-05-19.

This document closes Phase A. It records the C_P verdicts, the cascade event, the resulting locked panel for downstream phases, and the audit chain from pre-registration through measurement. The pre-registration itself is unmodified — pre-regs are immutable post-lock per program discipline; ex-post outcomes are recorded in separate lock artifacts.

---

## 1. Phase A C_P Verdicts

Per v1.3 §6.4.2 + provisional v1.4 §6.4.2 (automated classifier, claude-opus-4-7, model-default sampling, locked prompt template):

| Cell | Pivot | Anchoring count | Verdict |
|---|---|---|---|
| European | Le Creuset | 6/6 | **C_P PASSED** |
| American | All-Clad | 6/6 | **C_P PASSED** |
| Japanese (primary, ordinal 1) | Vermicular | 4/6 | **C_P FAILED** |
| Japanese (alternate, ordinal 2) | Iwachu | 6/6 | **C_P PASSED** |

Supermajority threshold: `anchored ≥ 5/6` passes; `≤ 4/6` fails. Full row-level rationales preserved in `osf/v17/classification_ledger.csv` (committed at `9042dea` for the original 18 rows; extended at `d09182c` for the Iwachu cascade rows).

---

## 2. Cascade Event Summary

Per v1.3 §6.4.7.1, Vermicular's C_P FAILURE triggered activation of Japanese cell ordinal 2 (Iwachu). Iwachu C_P PASSED at 6/6, locking the Japanese cell pivot. No further cascade required.

Full event record: `osf/v17/DEVIATIONS.md` Entry 6 (committed at `d09182c`; HASH backfill at `1304237`).

**Vermicular slot-level pattern** (preserved for v1.4 Methodology paper case study):
- Slots 1, 2, 3, 6 (claude-opus-4-5, claude-sonnet-4-5, gpt-4o, gemini-2.5-flash-lite): anchored to cookware brand identity.
- Slot 4 (gpt-4o-mini): non-anchored — framed "vermicular" as a multi-meaning term.
- Slot 5 (gemini-2.5-flash): non-anchored — framed "vermicular" as an adjective meaning worm-like.

Pattern is not tier-monotonic across vendors (gemini-2.5-flash-lite anchored while gemini-2.5-flash did not). Reflects training-set sparsity for the Vermicular brand on the LLM identity surface rather than model-capacity correlation. This is the structural property the C_P rule is designed to detect.

---

## 3. Locked Operational Panel for Phase B Onward

15 brands across 3 cells. Vermicular descoped per cascade outcome. Pivots indicated; pivots are not measured differently from other cell members downstream — pivot role is exhausted by Phase A.

### European cell (n=6, pivot = Le Creuset)
1. **Le Creuset** (pivot)
2. Staub
3. Mauviel
4. Demeyere
5. Fissler
6. de Buyer

### American cell (n=6, pivot = All-Clad)
1. **All-Clad** (pivot)
2. Lodge
3. Made In
4. Field Company
5. Smithey
6. Hestan

### Japanese cell (n=3, pivot = Iwachu)
1. **Iwachu** (pivot)
2. Sori Yanagi
3. Noda Horo (borderline per pre-reg §2.3.2)

~~Vermicular~~ — descoped per cascade outcome; preserved in `osf/v17/data/phase_a/vermicular/` for audit trail and v1.4 Methodology paper case study.

**Worldwide n = 15.** US sub-panel composition unchanged from pre-reg §3.2 (specified independently of cascade outcome).

---

## 4. C1 Floor Check

Pre-reg §6.2 specifies the C1 boundary floor for the v0.17 decision rule structure: worldwide `n ≥ 12`. Post-cascade `n = 15 ≥ 12`. **C1 floor HOLDS with margin of 3 brands above floor.** Decision-rule precision is therefore not attenuated by the descope.

Had the entire Japanese cell collapsed (all 4 alternates C_P FAILING — Vermicular → Iwachu → Sori Yanagi → Noda Horo), worldwide n would have dropped to 12 (exactly at floor). That scenario is not realized; recording for completeness.

---

## 5. Tradition-Cell Richness (Descriptive, Non-Pre-Registered)

Per pre-reg §2.3.2 commitment to report tradition-cell richness post-Phase A:

| Cell | Pre-Phase A | Post-Phase A | Cascade depth used |
|---|---|---|---|
| European | n=6 | n=6 | 0 (primary passed) |
| American | n=6 | n=6 | 0 (primary passed) |
| Japanese | n=4 | n=3 | 1 (alternate 1 passed) |

Japanese cell entered Phase A with the thinnest depth (4 brands vs 6 in the other two) and exited with the thinnest post-cascade panel (3 brands). This is reportable as a structural property of the substrate in LLM identity space — there are simply fewer Western-LLM-anchorable Japanese premium cookware brands than European or American ones at the time of measurement.

---

## 6. Methodological Observations (Non-Pre-Registered, Exploratory)

These observations surfaced during Phase A and are recorded for the v0.17 paper's Discussion section. None are pre-registered hypotheses; all are post-hoc interpretation candidates.

**Identity-Load signal embedded in C_P outcomes.** Iwachu's 6/6 versus Vermicular's 4/6, despite both being Japanese premium cast iron cookware brands, suggests an Identity-Load gradient correlated with brand heritage age and training-data density: Iwachu's ~400-year Iwate nambu-tekki provenance produces a denser, more stable LLM identity surface than Vermicular's 13-year-old Aichi Dobby brand. This is consistent with the Identity-Load moderator at the heart of the Third System architecture (Tri-System MSI WP §4.2): higher-IL categories (where heritage and provenance carry symbolic weight in the purchase) anchor more stably across LLM training surfaces. Note the framing is correlational and exploratory; a causal Identity-Load test is outside v0.17's scope.

**Audit-trail richness as a transparency upgrade.** Every row in the classification ledger carries a one-sentence rationale from the automated classifier. External reviewers can audit the Vermicular FAILED verdict in detail (slot 4: "multiple meanings"; slot 5: "adjective meaning worm-like") rather than receiving a summary verdict with opaque operator notes. This is the credibility property that motivates the operator → automated classifier substitution in DEVIATIONS Entry 4 and the v1.4 Methodology paper increment.

---

## 7. Audit Chain — Phase A

Full git commit trace, in order:

| Step | Event | Commit | Tag |
|---|---|---|---|
| 1 | Pre-registration locked (r0) | `c013ac1` | `v0.17-prereg` (preserved) |
| 2 | Pre-reg revised to r1 (Trends → C_P framing correction) | `3ebe426` | `v0.17-prereg-r1` |
| 3 | Pre-reg §8 hash backfill | `04b624f` | — |
| 4 | acquire_phase_a_v1_3.py — slot files written for 3 primary pivots | `2b31253` | — |
| 5 | classify_phase_a_v17.py v1 — original ledger generated | `2b31253` | — |
| 6 | DEVIATIONS Entry 2 (Google SDK migration) | `12e66db` | — |
| 7 | DEVIATIONS Entry 3 (gemini-2.0-flash → gemini-2.5-flash-lite) | `b5efea3` | — |
| 8 | DEVIATIONS Entry 4 (operator-judgement → LLM classifier substitution) + classifier script created | `2097c9f` → `a6974e6` | — |
| 9 | DEVIATIONS Entry 5 (temperature deprecation patch) + filled ledger for 18 rows | `9042dea` → `8fc966c` | — |
| 10 | DEVIATIONS Entry 6 (Vermicular C_P FAILED → Iwachu cascade) + script upgrade + Iwachu slot files + extended ledger | `d09182c` → `1304237` | — |
| 11 | Phase A lock (this document) | `7aabb53` | `v0.17-phase-a-locked` |

---

## 8. Transition to Phase B

Phase B (topic-ID resolution per Protocol v1.2 §4) operates on the 15-brand locked operational panel above. Phase B output: per-brand canonical topic ID with disambiguation log at `osf/v17/registries/topic_id_resolution_log_v0.17.csv`. Phase B brand list is identical to §3 above (not the Phase A 4-brand pivot subset).

Phase B script — `scripts/phaseB_resolve_v17.py` — to be derived from `scripts/phaseB_resolve_v15.py` template with substrate parameterisation. Phase B pre-registration commitments per pre-reg §6.3 remain unchanged from r1 lock.

The Phase A pipeline (acquire → classify → cascade-as-needed → lock) is now battle-tested. Cascade plumbing handled the Japanese cell event end-to-end without protocol violation. v0.18 and subsequent phases inherit this infrastructure.

---

*End of Phase A Lock document.*
