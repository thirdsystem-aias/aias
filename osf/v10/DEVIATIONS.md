# AIAS v0.10 — Deviations Log

This document records all deviations from the locked pre-registration (`PRE_REGISTRATION.md`, locked at git commit `8767f44`, tag `v0.10-prereg`, on 2026-05-09) per pre-reg §8.

Each entry records: date, pre-reg reference, description of the mismatch, resolution applied, and impact on the confirmatory/descriptive status of v0.10's claims.

---

## Deviation 1 — Classifier described as "keyword/phrase rule list"; actual v0.7 classifier is LLM-based

**Date logged.** 2026-05-09 (during analysis Step 2 setup, prior to first classifier run)
**Pre-reg reference.** §5 (Classifier Operationalization)
**Pre-reg statement.** "The classifier inherits the v0.7 keyword/phrase rule list and judge-LLM verification protocol unchanged."

**Reality.** Inspection of the v0.7 classifier (`/Users/pablou/aias/manual_review_bbb.py`) reveals that v0.7 does not contain a keyword/phrase rule list. The v0.7 classifier is a single call to gpt-5.4-mini at temperature 0, structured with a system prompt and a function-calling tool schema. The keyword elements in v0.7's code are an *alias screen* (`BBB_ALIASES`) used to identify which responses contain a phantom-brand mention worth sending to the classifier — not classification rules themselves.

**Resolution.** v0.10 honors the substantive pre-reg instruction ("inherit v0.7 unchanged") by using v0.7's actual classifier — the gpt-5.4-mini call with v0.7's system prompt and tool schema, parameterized for Mint instead of BBB. The system prompt + tool schema are reproduced verbatim (with brand parameter substitution) in `/v10/registries/v07_caveat_classifier.json`. Pre-reg §5's descriptive language was imprecise about v0.7's actual implementation; the substantive instruction is preserved unchanged.

**Impact on confirmatory status.** None. The instruction-level discipline of "inherit v0.7 unchanged" is preserved.

---

## Deviation 2 — No separate "judge-LLM verification" exists in v0.7

**Date logged.** 2026-05-09
**Pre-reg reference.** §5; §6 step 3; §5 E4 (adjudication)
**Pre-reg statement.** Pre-reg §6 lists "Apply v0.7 caveat-classifier" (step 2) and "Apply judge-LLM verification" (step 3) as separate steps; §5 references both; E4 specifies a procedure for resolving disagreement between the rule-based classifier and the judge-LLM.

**Reality.** v0.7 has only one LLM call. There is no separate judge-LLM. Steps 2 and 3 in pre-reg §6's analysis plan describe a verification structure that does not exist in v0.7.

**Resolution.** §6 steps 2 and 3 are collapsed into a single step: "Apply v0.7 classifier." E4 (classifier-judge disagreement adjudication) is structurally inapplicable — no two systems exist to disagree. The author's adjudication role specified in E4 is preserved as a manual review of any low-confidence or borderline classifications by inspection (not a formal LLM-disagreement adjudication), with all such adjudications still logged in `/v10/data/adjudication_log.csv`.

**Impact on confirmatory status.** None. The single-LLM classification was the actual v0.7 method. The deviation is in pre-reg description, not in v0.10's empirical work.

---

## Deviation 3 — v0.7 outputs 5-class valence; v0.10 pre-reg uses 2-class binary

**Date logged.** 2026-05-09
**Pre-reg reference.** §2 (Hypotheses), §5 (Classifier rule set)
**Pre-reg statement.** v0.10 hypotheses operate on `r_naive` (rate of naive-phantom presence) computed against a binary classification: naive vs caveated. §5 describes naive vs caveated criteria verbally.

**Reality.** v0.7 outputs five valence classes: `live_recommendation`, `live_with_caveat`, `status_correction`, `historical_reference`, `ambiguous`. The pre-reg's 2-class binary requires an explicit mapping that the pre-reg does not specify.

**Resolution.** The 5-to-2 mapping is locked at first classification and preserved across all v0.10 analyses:

| v0.7 valence            | v0.10 binary (primary) | v0.10 binary (E3 sensitivity) |
|-------------------------|------------------------|-------------------------------|
| live_recommendation     | naive                  | naive                         |
| live_with_caveat        | caveated               | caveated                      |
| status_correction       | caveated               | caveated                      |
| historical_reference    | caveated               | caveated                      |
| ambiguous               | naive                  | caveated                      |

The mapping is consistent with §5's verbal description: `live_with_caveat`, `status_correction`, and `historical_reference` all involve "explicit acknowledgment of decommissioning, shutdown, sunset, discontinuation, end-of-life, migration to successor product, or historical-reference framing." The treatment of `ambiguous` follows E3 (light-hedging convention): naive in primary analysis, caveated in sensitivity.

**Impact on confirmatory status.** None on H1/H2 directly, but the mapping is now part of the locked methodology and any post-hoc revision to it would constitute a substantive deviation requiring re-disclosure.

---

## Deviation 4 — E4 inapplicability cascade

**Date logged.** 2026-05-09
**Pre-reg reference.** §5 E4 (Classifier-judge disagreement)
**Pre-reg statement.** "Where the rule-based classifier and the judge-LLM verification disagree, the response is hand-adjudicated by the author against the v0.7 rule set as written."

**Reality.** E4 is structurally inapplicable given Deviations 1 and 2. There is no rule-based classifier and no separate judge-LLM. The intended safeguard — author adjudication where automated systems disagree — is preserved by retaining the author's right to re-adjudicate any classification on inspection, with all such re-adjudications logged in `/v10/data/adjudication_log.csv`.

**Resolution.** Author adjudication applies only to manually-flagged borderline cases (e.g., responses that produce `ambiguous` valence; responses where the source_quote does not appear faithful to the response text). Adjudication rate (% of automated classifications overridden by author) is reported alongside H1 outcome.

**Impact on confirmatory status.** None. The substantive safeguard (author oversight of edge cases) is preserved.

---

## Summary of impact on hypotheses

| Hypothesis           | Affected by deviations?                                                                | Status                     |
|----------------------|----------------------------------------------------------------------------------------|----------------------------|
| H1 (Stability)       | No — already routed to descriptive disclosure path due to floor breach (§3.4)           | Indeterminate / underpowered |
| H2 (Persistence)     | Mapping in Deviation 3 affects how `ambiguous` is counted, but not r_naive > 0 question | Evaluable as confirmatory  |
| H3 (Co-movement)     | No — diagnostic only                                                                    | Diagnostic                 |

The deviations affect the methodological description of the v0.10 study, not the empirical outcomes of its hypotheses. The descriptive-disclosure status that already applies to H1 absorbs any residual interpretive uncertainty introduced by the mapping in Deviation 3.

---

*This log is committed to OSF as part of the v0.10 deposit per pre-reg §10. The v0.10 SSRN paper carries an explicit deviations section in its declarations block summarizing this content.*
