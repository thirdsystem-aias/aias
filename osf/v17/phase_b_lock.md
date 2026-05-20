# Phase B Lock — v0.17 Premium Kitchenware

**Status.** Phase B complete; operational panel locked at 10 eligible brands; C1 worldwide-n floor BREACHED at n=10 < 12.
**Locked at git commit.** `afa950c` (tag: `v0.17-phase-b-locked`).
**Substrate.** Premium kitchenware (per pre-reg §1).
**Methodology.** v0.15 Phase B (Trends-substrate) as superseded by provisional v1.4 §5.2 (LLM-substrate) per DEVIATIONS Entry 7.
**Pre-registration of record.** `v0.17-prereg-r1` (commit `3ebe426`; §8 hash backfill at `04b624f`).
**Phase A lock of record.** `v0.17-phase-a-locked` (commit `8cdf0cd`).
**Date locked.** 2026-05-20.

This document closes Phase B. It records the per-brand mentionability tier verdicts, the per-cell breakdown, the Noda Horo borderline-classification resolution, the C1 breach status, the methodological dissociation finding between Phase A and Phase B, and the route to v0.18 indie fragrance per pre-reg line 63's joint-matrix specification. The pre-registration is unmodified — pre-regs are immutable post-lock per program discipline; ex-post outcomes are recorded in separate lock artifacts.

---

## 1. Phase B Mentionability Tier Verdicts

Per provisional v1.4 §5.2 (LLM-substrate Phase B; 3 unprompted category queries × 6-slot LLM reference set = 18 cells; mention detection via case-insensitive word-boundary regex against mechanically-generated aliases; tier thresholds PASS ≥ 1/6, PASS_E5 ∈ (0, 1/6), EXCLUDED_E1a = 0):

| Brand | Cell | Phase A role | Mentions / 18 | Mention rate | Phase B tier |
|---|---|---|---|---|---|
| Le Creuset | european | primary_pivot | 18 | 1.000 | PASS |
| Mauviel | european | alternate_2 | 18 | 1.000 | PASS |
| All-Clad | american | primary_pivot | 18 | 1.000 | PASS |
| Staub | european | alternate_1 | 17 | 0.944 | PASS |
| Demeyere | european | alternate_3 | 15 | 0.833 | PASS |
| Lodge | american | alternate_1 | 7 | 0.389 | PASS |
| de Buyer | european | alternate_5 | 6 | 0.333 | PASS |
| Hestan | american | alternate_5 | 6 | 0.333 | PASS |
| Made In | american | alternate_2 | 4 | 0.222 | PASS |
| Fissler | european | alternate_4 | 2 | 0.111 | PASS_E5 |
| Field Company | american | alternate_3 | 0 | 0.000 | **EXCLUDED_E1a** |
| Smithey | american | alternate_4 | 0 | 0.000 | **EXCLUDED_E1a** |
| Iwachu | japanese | alternate_1 | 0 | 0.000 | **EXCLUDED_E1a** |
| Sori Yanagi | japanese | alternate_2 | 0 | 0.000 | **EXCLUDED_E1a** |
| Noda Horo | japanese | alternate_3 (borderline) | 0 | 0.000 | **EXCLUDED_E1a** |

Canonical reference: `osf/v17/registries/topic_id_resolution_log_v0.17.csv`. Per-query × per-slot mention matrix preserved in the log's diagnostic columns (`q1_mentions_of_6`, `q2_mentions_of_6`, `q3_mentions_of_6`, `slot_1_mentions_of_3` through `slot_6_mentions_of_3`).

---

## 2. Per-Cell Breakdown

| Cell | Pre-Phase-B n | Phase-B PASS | Phase-B PASS_E5 | Phase-B EXCLUDED | Eligible n | Outcome |
|---|---|---|---|---|---|---|
| European | 6 | 6 | 0 | 0 | 6 | INTACT |
| American | 6 | 4 | 0 | 2 | 4 | partial attrition (Field Company, Smithey) |
| Japanese | 3 | 0 | 0 | 3 | **0** | **FULL COLLAPSE** |
| **Worldwide** | **15** | **9** | **1** | **5** | **10** | C1 BREACHED |

**Japanese cell collapse.** All three remaining Japanese brands post-Phase-A-cascade (Iwachu, Sori Yanagi, Noda Horo) received 0/18 mentions. This includes Iwachu, which had passed Phase A C_P at 6/6 — see §4 dissociation finding below.

---

## 3. Noda Horo Borderline-Classification Resolution

Per brand-registry `borderline_resolution_at: "phase_b_topic_id"`, Noda Horo's Phase B tier *is* the protocol-mandated resolution of whether it counts as in-scope cookware versus out-of-scope enamelware.

- **Phase B tier:** EXCLUDED_E1a (0/18 mentions in unprompted cookware-category queries)
- **Resolution:** OUT_OF_SCOPE (enamelware-only; not in-scope premium cookware)
- **Operational consequence:** Noda Horo descoped from the v0.17 operational panel. Japanese cell n drops from 3 to 2 nominal; combined with Iwachu and Sori Yanagi's Phase B EXCLUDED_E1a, Japanese cell post-Phase-B eligible n = 0.

Recorded in `osf/v17/registries/topic_id_resolution_log_v0.17.csv` row for Noda Horo, column `borderline_resolution`.

---

## 4. Methodological Finding — Phase A C_P ↛ Phase B Mention Rate Dissociation

The canonical case is Iwachu:

| Phase | Verdict | Interpretation |
|---|---|---|
| Phase A C_P (recognition anchoring) | 6/6 PASS | "Japanese cast iron cookware manufacturer" is the primary referent in all 6 LLMs' responses to "Who or what is Iwachu?" — substrate identity is unambiguous. |
| Phase B mention rate (recall presence) | 0/18 EXCLUDED_E1a | Never surfaces in any LLM's response to unprompted "What are the best premium cookware brands?" / "Recommend a high-quality cookware brand" / "What cookware brands do professional chefs use?" |

The dissociation is structurally robust: it holds across all 6 LLMs at Phase A (recognition) and all 6 LLMs × 3 queries at Phase B (recall). This is not classifier disagreement, prompt artifact, or measurement noise — it is a genuine cognitive-architectural property of LLM-mediated brand retrieval.

**Theoretical implication for AI Availability construct.** AI Availability is *not unidimensional*. At minimum two components are dissociable:

1. **Recognition anchoring:** given the brand name, does the LLM identify it as being in the substrate? (Measured by Phase A C_P.)
2. **Recall presence:** given the substrate category, does the LLM spontaneously surface the brand? (Measured by Phase B mention rate.)

The AIAS composite (Presence, Ranking, Consistency, Coverage, Grounding, Sentiment) needs to formalize this distinction. Current AIAS definitions implicitly treat Presence as unidimensional; the v0.17 result suggests Presence should aggregate over both recognition and recall components.

**Forward actions.**
1. v1.4 Methodology paper increment (successor to SSRN 6797679): formalize the recognition × recall distinction; specify how the composite Presence score aggregates across them.
2. Tri-System monograph (Routledge): the dissociation finding strengthens the Third System construct definition — AI Availability requires multi-component measurement, not single-metric proxies. Theoretical contribution worth a dedicated section in the chapter on AI Availability mechanics.
3. v0.17 SSRN paper Discussion: foreground this finding as the headline methodological contribution, even though the substantive hypothesis (H_Regime4_kitchenware) FALSIFIED on panel inadequacy.

---

## 5. C1 Floor Breach

Pre-reg line 43: "C1 — Panel adequacy: worldwide n ≥ 12 brands surviving the 14-day Trends floor and Phase A pivot validation per v1.3 §6.4.2."

Observed worldwide eligible n = 10. **C1 BREACHED with deficit of 2 brands below floor.**

Pre-reg line 51 (decision rules): "FALSIFIED: ¬C1 ∨ ¬C2". Pre-reg line 63 (joint v0.16/v0.17 verdict matrix): "PARTIAL × FALSIFIED → AMBIGUOUS — kitchenware fails C1 or C2; H_IdentityLoad_moderator inconclusive pending v0.18 indie fragrance."

The pre-reg explicitly anticipated and committed to this outcome path. No verdict reframing or pre-reg amendment is required. The formal v0.17 substantive verdict is recorded in `osf/v17/v0_17_verdict.md`.

**Note on substrate-substitution attrition.** Pre-reg §3.2 line 85 anticipated 1–3 brands of *Trends*-substrate Phase B attrition. DEVIATIONS Entry 7 substituted LLM-substrate Phase B. Observed attrition: 5 brands (~2× the pre-reg's worst-case estimate). The substrate substitution increased Phase B attrition beyond what the pre-reg panel over-provisioning was calibrated against. This is a documented methodological finding (DEVIATIONS Entry 8 §observation 1) and a forward action for v1.4 Methodology paper; it does NOT modify the v0.17 verdict, which stands at the pre-registered FALSIFIED on panel inadequacy.

---

## 6. Locked Operational Panel for Phase D

10 brands across 2 cells. Japanese cell descoped per full Phase B collapse. American cell partial: Field Company and Smithey descoped.

### European cell (n=6)
1. **Le Creuset** (pivot, mention rate 1.000)
2. Staub (0.944)
3. Mauviel (1.000)
4. Demeyere (0.833)
5. Fissler (0.111, PASS_E5)
6. de Buyer (0.333)

### American cell (n=4)
1. **All-Clad** (pivot, mention rate 1.000)
2. Lodge (0.389)
3. Made In (0.222)
4. Hestan (0.333)

### Japanese cell (n=0)
~~Iwachu, Sori Yanagi, Noda Horo~~ — all EXCLUDED_E1a at Phase B; cell collapsed.

Phase D scoring will proceed on the 10-brand worldwide panel under the FALSIFIED-on-panel-inadequacy verdict, *for the purpose of producing per-cell ρ where cell n ≥ 5 per pre-reg §2.3.2 (European n=6 ≥ 5 — reportable; American n=4 < 5 — reportable as "cell n below ρ-reporting floor"). No primary-hypothesis decision rule reverification.*

---

## 7. Audit Chain — Phase B

| Step | Event | Commit |
|---|---|---|
| 1 | DEVIATIONS Entry 7 (substrate substitution: Trends → LLM) + `phaseB_resolve_v17.py` + 18 cached LLM responses + resolution log CSV | `55e28ed` |
| 2 | DEVIATIONS Entry 7 HASH_AUTO_7 backfill | `9174d10` |
| 3 | DEVIATIONS Entry 8 (Phase B outcome event record) | `1b560d2` |
| 4 | DEVIATIONS Entry 8 HASH_AUTO_8 backfill | (post-commit) |
| 5 | Phase B lock (this document) + v0.17 verdict document | `afa950c` |
| 6 | Phase B lock HASH backfill | (post-commit) |

---

## 8. Transition to Phase D and v0.18

Phase D scoring proceeds on the 10-brand panel for descriptive ρ analysis (no primary-hypothesis decision rule reverification — already FALSIFIED on panel inadequacy). v0.18 indie fragrance acquisition begins on the cascade-tested pipeline infrastructure with: substrate-substitution attrition lesson applied (panel over-provisioning re-calibrated for LLM-substrate regime) and same-language IL test as the methodological focus.

Pre-reg line 63's joint verdict matrix routes the H_IdentityLoad_moderator hypothesis to v0.18 for resolution; v0.17 fulfills its pre-registered role as the AMBIGUOUS first half of the joint test.

---

*End of Phase B Lock document.*
