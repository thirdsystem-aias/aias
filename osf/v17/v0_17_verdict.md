# v0.17 Premium Kitchenware — Formal Substantive Verdicts

**Status.** Verdicts locked per pre-registration. Substantive hypothesis FALSIFIED on panel inadequacy; joint Identity-Load moderator verdict AMBIGUOUS pending v0.18.
**Locked at git commit.** `afa950c` (paired with `v0.17-phase-b-locked` tag).
**Pre-registration of record.** `v0.17-prereg-r1` (commit `3ebe426`).
**Phase B lock of record.** `osf/v17/phase_b_lock.md` at commit `afa950c`.
**Date locked.** 2026-05-20.

This document records the formal substantive verdicts for v0.17 Premium Kitchenware against the pre-registered hypotheses and decision rules. Verdicts follow mechanically from observed Phase A and Phase B outcomes applied to immutable pre-reg §2.1 decision rules and §2.2 conditional verdict matrix. No post-acquisition reframing per pre-reg line 259's pre-registration declaration.

---

## 1. Primary Hypothesis: `H_Regime4_kitchenware`

### Pre-registered decision rules (pre-reg §2.1)

- **C1 — Panel adequacy:** worldwide n ≥ 12 brands surviving the 14-day Trends floor and Phase A pivot validation per v1.3 §6.4.2.
- **C2 — Effect threshold:** (per pre-reg §2.1 — not invoked here; verdict resolves at C1)
- **C3 — Control persistence:** (per pre-reg §2.1 — not invoked here; verdict resolves at C1)

### Pre-registered verdict structure (pre-reg §2.1 lines 49–51)

- **CONFIRMED:** C1 ∧ C2 ∧ C3
- **PARTIAL:** C1 ∧ C2 ∧ ¬C3
- **FALSIFIED:** ¬C1 ∨ ¬C2

### Observed outcome

| Decision rule | Threshold | Observed | Status |
|---|---|---|---|
| C1 | worldwide n ≥ 12 | n = 10 | **¬C1 (BREACHED)** |
| C2 | — | not evaluated (resolves at C1) | — |
| C3 | — | not evaluated (resolves at C1) | — |

### Formal verdict

> **`H_Regime4_kitchenware`: FALSIFIED on panel inadequacy (¬C1; worldwide n = 10 < 12).**

Per pre-reg line 51: `FALSIFIED: ¬C1 ∨ ¬C2`. The verdict is mechanical from ¬C1.

Per pre-reg §3.2 line 85: "Worldwide panel adequacy holds even under full Japanese cell collapse (n_after_Japanese_collapse = 12, exactly at C1)." Observed outcome included full Japanese cell collapse (n_japanese = 0) *and* partial American cell attrition (Field Company, Smithey EXCLUDED_E1a). The combined attrition produced n = 10, below the worldwide-collapse boundary the pre-reg had calibrated against.

---

## 2. Secondary Hypothesis: `H_IdentityLoad_moderator` (Joint v0.16 / v0.17)

### Pre-registered joint verdict matrix (pre-reg §2.2 line 63)

| v0.16 verdict | v0.17 verdict | Joint outcome |
|---|---|---|
| ... | ... | ... |
| PARTIAL | FALSIFIED | **AMBIGUOUS** — kitchenware fails C1 or C2; `H_IdentityLoad_moderator` inconclusive pending v0.18 indie fragrance |

### Component verdicts

- **v0.16 (kitchen knives):** PARTIAL per `H_Regime4_replication_knives` verdict in v0.16 paper (SSRN 6791999, submitted 2026-05-18).
- **v0.17 (premium kitchenware):** FALSIFIED on panel inadequacy per §1 above.

### Formal joint verdict

> **`H_IdentityLoad_moderator`: AMBIGUOUS — joint v0.16/v0.17 cell `PARTIAL × FALSIFIED` per pre-reg line 63. Hypothesis inconclusive pending v0.18 indie fragrance.**

The pre-reg anticipated this outcome path explicitly and committed v0.18 as the deciding test. v0.17 fulfills its pre-registered role as the first half of an inconclusive joint test; the substantive Identity-Load question resolves at v0.18.

---

## 3. Pre-Registration Discipline

This verdict follows pre-reg §2.1 decision rules and §2.2 joint matrix mechanically. No post-acquisition decision rule modification, threshold adjustment, or interpretive reframing has been applied. Per pre-reg line 259's pre-registration declaration: "Decision rules C1, C2, C3 in §2.1 and the §2.2 conditional verdict matrix are immutable post-lock. ... No verdict reframing post-acquisition."

The C1 breach was a pre-registered outcome path with a pre-committed verdict. The discipline produces a clean, defensible verdict from an outcome that visually looked like a failure but is structurally the program working as designed: the pre-reg anticipated panel-inadequacy, specified the verdict, and routed the substantive question to v0.18.

---

## 4. What v0.17 Contributes Despite the FALSIFIED Verdict

The substantive hypothesis FALSIFIED, but v0.17 produced three findings of independent value that the SSRN paper Discussion will foreground:

**4.1 — Phase A C_P ↛ Phase B mention rate dissociation.** Iwachu's 6/6 Phase A C_P PASS combined with 0/18 Phase B mention rate is the strongest empirical demonstration in the AIAS programme that AI Availability is multi-component. Recognition anchoring (Phase A) and recall presence (Phase B) are dissociable cognitive properties of LLM-mediated retrieval. The AIAS composite (Presence, Ranking, Consistency, Coverage, Grounding, Sentiment) needs to formalize the recognition × recall distinction in the v1.4 Methodology paper. Theoretical implication for the Tri-System monograph: AI Availability is at least two-component; single-metric proxies are inadequate.

**4.2 — Substrate-substitution attrition.** LLM-substrate Phase B produced ~2× the pre-reg's worst-case Trends-substrate attrition estimate (5 brands observed vs 1–3 anticipated). The substrate substitution (DEVIATIONS Entry 7) had panel-survival consequences the pre-reg panel design wasn't calibrated against. Forward action for v1.4 Methodology paper: re-calibrate panel over-provisioning for the LLM-substrate regime; v0.18 panel design applies this lesson.

**4.3 — Cross-cultural confound on cross-cultural substrates.** The Japanese cell's full collapse despite high Identity Load (Iwachu ~400-year nambu-tekki heritage; Sori Yanagi designer-craft heritage; Noda Horo enamelware heritage) is hard to disambiguate from Western-language LLM training-data bias on this substrate. The pre-registered IL moderator hypothesis assumed an LL-substrate-bias-neutral measurement surface; the v0.17 outcome shows that assumption is invalidated for cross-cultural categories. v0.18 indie fragrance (entirely English-language category surface) is the clean same-language IL test required for hypothesis resolution.

---

## 5. Reportable Outcomes for v0.17 SSRN Paper

The v0.17 SSRN paper title and abstract framing remain consistent with the pre-reg-anticipated outcome path:

- Primary substantive result: H_Regime4_kitchenware FALSIFIED on panel inadequacy (C1 breach).
- Joint result: H_IdentityLoad_moderator AMBIGUOUS pending v0.18.
- Headline methodological contribution: Phase A / Phase B dissociation finding — AI Availability is multi-component.
- Forward implication: v0.18 indie fragrance becomes the IL-moderator-deciding test, with substrate-substitution-attrition lesson applied to panel design.

---

## 6. Transition

- **Phase D scoring:** proceeds on 10-brand panel for descriptive per-cell ρ where cell n ≥ 5 (European n=6 reportable; American n=4 reported as "cell n below ρ-reporting floor" per pre-reg §2.3.2). No primary-hypothesis decision rule reverification.
- **v0.17 paper:** draft Results around the formal verdicts (§§1–2 above); Discussion around §4 findings; Methods around DEVIATIONS Entries 4–8.
- **v0.18 acquisition:** begins on cascade-tested pipeline infrastructure with v0.17 lessons applied.

---

*End of v0.17 Verdict document.*
