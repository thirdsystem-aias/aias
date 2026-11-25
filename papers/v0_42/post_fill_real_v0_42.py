#!/usr/bin/env python3
"""post_fill_real_v0_42.py -- the hand-written text of the t4 paper, applied after fill_paper_v0_42.py.

Written on 2026-11-11 (US Central) from the real scorer outputs of commit 31c64c6 (v0.42 scoring, once):
osf/v42/v42_verdicts.json (sha256 b5094ced...) and osf/v42/v42_brand_table.csv (sha256 792e14ad...).
fill_paper_v0_42.py picks pre-written sentences by verdict case; this step replaces the generic Discussion
with one written for the observed results and adds the sentences the template could not anticipate. Every
number below is a leaf of v42_verdicts.json, formatted as the fill formats it (paths in the comments), or a
sum or difference of such leaves; the dates and the 72 judge calls come from osf/v42/data/code_v0_42.log and
the pre-registration. Revised on 2026-11-12 after an outside number check: the sentences on the 114 unanswered
attempts and on the two Anthropic organizations rest on osf/v42/data/t4_raw.jsonl (status, error, started_utc),
osf/v42/data/t4_batches.jsonl (batch creation times) and the notes in osf/v42/data/collect_v0_42.log and
code_v0_42.log; the per-provider sentence compares verdicts.H_Gen_Presence.rho with the three
per_provider_generation_pairs; the spirits sentence describes the Phase B prompts of osf/v42/prereg/probes_v0_42.jsonl.
Run after the fill and before scripts/build_paper_v0_42.py:

    PYTHONDONTWRITEBYTECODE=1 python3 papers/v0_42/fill_paper_v0_42.py
    PYTHONDONTWRITEBYTECODE=1 python3 papers/v0_42/post_fill_real_v0_42.py
    PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_paper_v0_42.py

It refuses unless the verdicts file is the one it was written for (SHA-256 below) and every anchor text matches.
"""
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DRAFT = ROOT / "papers/v0_42/v0_42_ssrn_paper_draft.md"
VERDICTS = ROOT / "osf/v42/v42_verdicts.json"
VERDICTS_SHA256 = "b5094ced5013315ca34d7d4a74a85d969f859f9707bc6bd3594334ee1fdb9f6e"

EDITS = []

# Abstract: H_Gen_Phi interval; H_Search_Presence per-model range and MC_Search share.
# verdicts.H_Gen_Phi.ci95_rho; verdicts.H_Search_Presence.per_model.*.rho; MC_Search.gemini-4-argon.share
EDITS.append((
    "(`H_Gen_Phi` MARGINAL: ρ = 0.310, p = 0.0056, n = 73).",
    "(`H_Gen_Phi` MARGINAL: ρ = 0.310, just above the falsification bar of 0.30, 95% interval 0.051 to 0.520, "
    "p = 0.0056, n = 73)."))
EDITS.append((
    "Turning on each provider's web search left the Presence ordering intact (search-robust: ρ = 0.909, 95% "
    "interval 0.827 to 0.945).",
    "Turning on each provider's web search left the Presence ordering of the three-model panel intact "
    "(search-robust: ρ = 0.909, 95% interval 0.827 to 0.945), although per model the correlation ranged from "
    "0.710 to 0.909 and Gemini 4 Argon searched in only 17.8% of its search-on calls."))

# §2.6: how the v0.23 judge was reached (osf/v42/data/code_v0_42.log, note of 2026-11-11T14:09:51Z).
EDITS.append((
    "(Claude Sonnet 4.5; 72 judge calls, which are coding, not acquisition).",
    "(Claude Sonnet 4.5; 72 judge calls, which are coding, not acquisition). Claude Sonnet 4.5 is not served to "
    "the Anthropic organization the study used from its re-run pass on (§3.1): a first coding attempt on 11 "
    "November 2026 returned a not-found error for every judge call, none of them billed, and its tables were set "
    "aside. With the pre-registrant's decision, the judge was called through the Anthropic organization that coded "
    "$t_1$--$t_3$ and had served the first six Claude Fable 5.2 batches, with the same model, code and prompts, and "
    "coded 72 of 72 answers."))

# §3.1: raw records per attempt. descriptives.6_cost.per_model_condition.*.records (sum 990) and
# .billed_requests; 990 - 876 = 114; 120 - 90 = 30; 208 - 202 = 6; 168 - 90 = 78.
EDITS.append((
    "No pause approval was recorded by the budget guard.",
    "No pause approval was recorded by the budget guard. The raw file holds one record per attempt: 990 records "
    "for the 876 calls. The 114 additional records (30 for Claude Fable 5.2 with search on, 6 for Gemini 4 Argon "
    "with search off and 78 for Gemini 4 Argon with search on) are attempts that the providers refused, without an "
    "answer and without billed usage, when an account balance ran out: Anthropic declined to create the seventh "
    "Claude Fable 5.2 batch (the 30 calls of the third search-on run) for insufficient credit, and Google refused "
    "84 Gemini 4 Argon calls because the prepaid credits were depleted. The main pass ended in block 7 with these "
    "calls unanswered. After the balances were restored, and with the study's Anthropic requests moved to a new "
    "organization, the one logged re-run pass (§2.4) answered all 114 between 09:05 and 09:50 UTC, so six Gemini 4 "
    "Argon recognition answers were completed after the search-on blocks had begun (§2.1). Each call is analysed "
    "once, from its answered attempt."))

# §3.5: descriptive 4 and DEVIATIONS Entry 1. descriptives.4_answer_form.*.non_answers (all 0).
EDITS.append((
    "and tokens, searches and spend per model and condition from the recorded usage (descriptive 6).",
    "and tokens, searches and spend per model and condition from the recorded usage (descriptive 6). Every "
    "v0.19--v0.22 Phase A answer contained a yes or a no, no answered call ended with a refusal finish reason, "
    "and no call ended unanswered, so the two categories into which `osf/v42/DEVIATIONS.md` (Entry 1) splits "
    "unanswered calls (a GPT-6 Astra answer that is empty, refusal or blank; a Gemini 4 Argon call with no "
    "candidate) are both empty. Refusal counts are lower bounds (Entry 1)."))

# §4 Discussion, written for the observed results. Sources (verdicts.*):
#   H_Gen_Presence: rho, ci95_rho, delta, per_substrate.*.rho, reported_alongside.per_provider_generation_pairs
#   H_Gen_Phi: rho, ci95_rho, p_perm, per_substrate (rho, n), reported_alongside.mean_independence_S0.N3.abs
#   H_Search_Presence: rho, ci95_rho[0], per_model.*.(rho, delta); MC_Search.gemini-4-argon.share
#   descriptives.1_run_reliability (rel1, rel3); 4_answer_form.*.registry_brands_named_per_phase_B_answer;
#   3_floor_persistence (58, 43, 74%, 49, 11%)
DISCUSSION = r"""# 4. Discussion

The primary result is that the ordering of brands by recall Presence carried over from the retiring model generation to the newest flagship models ($\rho_{\text{pw}} = 0.828$, 95% interval 0.722 to 0.890). Under the pre-registered rationale, the programme's record on the legacy panel can therefore be bridged to the new panel for Presence: the brand standings measured since May 2026 remain interpretable on current models. The bridge is an ordering, not a level. The newest models named the average brand in a larger share of category answers ($\Delta = +0.046$), so comparisons of absolute Presence across the change of panel would need to account for the shift. The study does not explain it: answer length is a descriptive of the $t_4$ answers only (Table 8), not of the legacy answers.

The bridge is not uniform. Four substrates kept their order closely (per-substrate $\rho$ from 0.855 to 0.943 with search off), while premium spirits reached 0.607. The spirits substrate is also the only one whose category questions include no direct request for the best (the other four each open with "What are the best ...?"): its six questions ask which brands critics, competitions, bartenders and enthusiast communities favour, which have become cultural phenomena and which are hidden gems not yet mainstream (§2.3). Such frames may leave a new generation more room to choose differently; the design does not test this. Per provider, the legacy pair against its new model gave $\rho_{\text{pw}} = 0.848$ for Anthropic, 0.715 for Google and 0.566 for OpenAI. These single-model comparisons are reported alongside and decide nothing, and one model's Presence rests on fewer answers than the panel's. Still, for OpenAI and Google a user of the provider's newest model meets a brand order that departs further from that provider's legacy models (0.566 and 0.715) than the three-model panel departs from the six-model panel (0.828), most of all for OpenAI; for Anthropic the pair agrees slightly more closely than the panels (0.848).

For Consistency the result is intermediate and close to the falsification bar: $\rho_{\text{pw}} = 0.310$ against a bar of 0.30, with a 95% interval (0.051 to 0.520) that reaches below the falsification bar and above the confirmation bar. The permutation $p$-value (0.0056) indicates more agreement between the two generations' $\varphi$ orderings than chance would give, but the pre-registered effect-size rule decides, and the data neither support nor rule out a quantitative bridge for $\varphi$. The per-substrate correlations range widely, from 0.058 (cosmetics) and 0.075 (skincare) to 0.809 (automotive), each on 10 to 17 brands. With three models $\varphi$ carries less information per brand than with six (§2.8), so part of the shortfall may reflect the smaller panel rather than the change of generation; the design cannot separate the two. On the new panel $\varphi$ did not track Presence ($|\rho_{\text{pw}}(\varphi, \hat\pi)| = 0.101$), so the weak carry-over is not a by-product of the Presence result.

Web search left the panel's Presence ordering intact ($\rho_S = 0.909$; the interval's lower bound, 0.827, clears the 0.80 bar). Two qualifications bound this reading. First, it describes the three-model mean. Per model, the correlation between search off and search on was 0.909 for Gemini 4 Argon, 0.858 for GPT-6 Astra and 0.710 for Claude Fable 5.2. For Claude Fable 5.2 this is well below the reliability of a three-run mean in either condition (rel3 0.969 with search off and 0.963 with search on), which suggests that its search reorders brands beyond run-to-run noise. Second, Gemini 4 Argon searched in 17.8% of its search-on calls, so most of its search-on answers are close to a further search-off run; it contributes the highest per-model correlation and the smallest level shift ($\Delta = -0.012$). Where search was used on most calls, it lowered Presence ($\Delta = -0.052$ for Claude Fable 5.2 and $-0.058$ for GPT-6 Astra) and the number of registry brands named per category answer (from 6.2 to 5.0 and from 5.5 to 4.2). The pre-registered label therefore holds for the panel as collected, not for every model's use of search.

The run-to-run reliabilities of §3.5 set the noise floor of the new panel's series: rel1 from 0.845 to 0.915 and rel3 from 0.942 to 0.970 across models and conditions. A correlation between the three-run means of two waves in the range of rel3 would be consistent with no change in brand order beyond the variation recorded here between runs of the same model on the same questions; the $t_5$ and $t_6$ waves are to be read against these values.

Brands with little Presence mostly stayed so: of the 58 brands below the recall floor on the retiring panel, 43 (74%) were still below it on the newest models, and 11% of the brands above the floor fell below it. Fewer brands were below the floor at $t_4$ (49) than at $t_3$ (58), in line with the upward level shift.

"""

LIMITS_OLD = "The search-on results of Gemini 4 Argon rest on calls that rarely searched."
LIMITS_NEW = ("The search-on results of Gemini 4 Argon rest on calls that rarely searched, so the search-on "
              "condition tests search mainly through Claude Fable 5.2 and GPT-6 Astra. The per-provider generation "
              "pairs and the per-model search correlations are single-model figures reported alongside, without "
              "verdicts, and the pooled results can hide differences between models. Refusal counts are lower "
              "bounds: the raw record cannot distinguish a GPT-6 Astra refusal from a blank answer, nor record why "
              "a Gemini 4 Argon prompt was blocked (`osf/v42/DEVIATIONS.md`, Entry 1). The study's Anthropic "
              "requests went through two organizations: the first six Claude Fable 5.2 batches and the v0.23 "
              "recognition judge through the organization that had coded $t_1$--$t_3$, and the seventh batch, the "
              "30 calls of the third search-on run, through a new one, with the same model, parameters, code and "
              "prompts (§2.6, §3.1).")
EDITS.append((LIMITS_OLD, LIMITS_NEW))


# ---------------------------------------------------------------------------------------------------------------
# Revision r2 (25 November 2026): the apostrophe correction. The paper is filled from the re-coded verdicts and
# brand table (papers/v0_42/corrected_2026-11-25/, copies of OSF v45/sensitivity/t4_SQ/v42_verdicts_SQ.json and
# v42_brand_table_SQ.csv, v0.45 commit 47f1748; the table is OSF v42/v42_brand_table_corrected_2026-11-25.csv):
#
#   python3 papers/v0_42/fill_paper_v0_42.py --verdicts papers/v0_42/corrected_2026-11-25/v42_verdicts_SQ.json \
#       --table papers/v0_42/corrected_2026-11-25/v42_brand_table_SQ.csv
#   python3 papers/v0_42/post_fill_real_v0_42.py --verdicts papers/v0_42/corrected_2026-11-25/v42_verdicts_SQ.json
#
# The hand-written text above is reused with the numbers that moved replaced (R2_SUBS). Every replacement number is
# checked against a leaf of the corrected verdicts at run time (the paths beside each substitution); the published
# values quoted in the correction paragraph are the leaves of osf/v42/v42_verdicts.json and v42_brand_table.csv and
# are checked the same way. The published mode (no --verdicts) is unchanged and still reproduces r1.
CORRECTED_VERDICTS = ROOT / "papers/v0_42/corrected_2026-11-25/v42_verdicts_SQ.json"
CORRECTED_TABLE = ROOT / "papers/v0_42/corrected_2026-11-25/v42_brand_table_SQ.csv"
CORRECTED_SHA256 = "093825a90d42c1117a923586d210246969dabb0a748f0be73cdd13cdbbc57162"
CORRECTED_TABLE_SHA256 = "de8559cbe21db91e8922337c7ab5bdfaa7d1d2325f6bbe0870e6abcd812a5c4d"
PUBLISHED_TABLE = ROOT / "osf/v42/v42_brand_table.csv"
ERRATUM_URL = "https://osf.io/ec6wh/files/osfstorage/6b067ee7bf5e720c41dfd9cb"

GP = ("verdicts", "H_Gen_Presence")
GF = ("verdicts", "H_Gen_Phi")
SP = ("verdicts", "H_Search_Presence")
PAIRS = GP + ("reported_alongside", "per_provider_generation_pairs")
REL = ("descriptives", "1_run_reliability")
FLOOR = ("descriptives", "3_floor_persistence")
FORM = ("descriptives", "4_answer_form")
F3 = "{:.3f}".format
FS = "{:+.3f}".format
F4 = "{:.4f}".format
F1 = "{:.1f}".format
PCT = lambda x: f"{100 * x:.0f}%"
INT = "{:d}".format

# Abstract edits for r2: the fill's anchors carry the corrected numbers, so the two tuples are restated in full.
R2_ABSTRACT = [
    ("(`H_Gen_Phi` MARGINAL: ρ = 0.304, p = 0.0070, n = 73).",
     "(`H_Gen_Phi` MARGINAL: ρ = 0.304, just above the falsification bar of 0.30, 95% interval 0.047 to 0.516, "
     "p = 0.0070, n = 73).",
     [(GF + ("rho",), F3), (GF + ("ci95_rho", 0), F3), (GF + ("ci95_rho", 1), F3), (GF + ("p_perm",), F4)]),
    ("Turning on each provider's web search left the Presence ordering intact (search-robust: ρ = 0.910, 95% "
     "interval 0.829 to 0.945).",
     "Turning on each provider's web search left the Presence ordering of the three-model panel intact "
     "(search-robust: ρ = 0.910, 95% interval 0.829 to 0.945), although per model the correlation ranged from "
     "0.710 to 0.915 and Gemini 4 Argon searched in only 17.8% of its search-on calls.",
     [(SP + ("rho",), F3), (SP + ("ci95_rho", 0), F3), (SP + ("ci95_rho", 1), F3),
      (SP + ("per_model", "claude-fable-5-2", "rho"), F3), (SP + ("per_model", "gemini-4-argon", "rho"), F3),
      (("manipulation_checks", "MC_Search", "gemini-4-argon", "share"), lambda x: f"{100 * x:.1f}%")]),
]

# Discussion for r2: (published text, corrected text, leaves of the corrected verdicts that the corrected text prints).
R2_SUBS = [
    (r"($\rho_{\text{pw}} = 0.828$, 95% interval 0.722 to 0.890)",
     r"($\rho_{\text{pw}} = 0.827$, 95% interval 0.718 to 0.889)",
     [(GP + ("rho",), F3), (GP + ("ci95_rho", 0), F3), (GP + ("ci95_rho", 1), F3)]),
    (r"($\Delta = +0.046$)", r"($\Delta = +0.051$)", [(GP + ("delta",), FS)]),
    ("(per-substrate $\\rho$ from 0.855 to 0.943 with search off)",
     "(per-substrate $\\rho$ from 0.845 to 0.943 with search off)",
     [(GP + ("per_substrate", "v0.21", "rho"), F3), (GP + ("per_substrate", "v0.22", "rho"), F3)]),
    ("0.715 for Google and 0.566 for OpenAI", "0.707 for Google and 0.588 for OpenAI",
     [(PAIRS + ("Google: legacy pair -> gemini-4-argon", "rho"), F3),
      (PAIRS + ("OpenAI: legacy pair -> gpt-6-astra", "rho"), F3)]),
    ("(0.566 and 0.715) than the three-model panel departs from the six-model panel (0.828)",
     "(0.588 and 0.707) than the three-model panel departs from the six-model panel (0.827)",
     [(PAIRS + ("OpenAI: legacy pair -> gpt-6-astra", "rho"), F3),
      (PAIRS + ("Google: legacy pair -> gemini-4-argon", "rho"), F3), (GP + ("rho",), F3)]),
    ("the panels (0.848)", "the panels (0.848)",
     [(PAIRS + ("Anthropic: legacy pair -> claude-fable-5-2", "rho"), F3)]),
    (r"$\rho_{\text{pw}} = 0.310$ against a bar of 0.30, with a 95% interval (0.051 to 0.520)",
     r"$\rho_{\text{pw}} = 0.304$ against a bar of 0.30, with a 95% interval (0.047 to 0.516)",
     [(GF + ("rho",), F3), (GF + ("ci95_rho", 0), F3), (GF + ("ci95_rho", 1), F3)]),
    ("The permutation $p$-value (0.0056)", "The permutation $p$-value (0.0070)", [(GF + ("p_perm",), F4)]),
    ("from 0.058 (cosmetics) and 0.075 (skincare) to 0.809 (automotive)",
     "from 0.049 (cosmetics) and 0.057 (skincare) to 0.809 (automotive)",
     [(GF + ("per_substrate", "v0.21", "rho"), F3), (GF + ("per_substrate", "v0.20", "rho"), F3),
      (GF + ("per_substrate", "v0.22", "rho"), F3)]),
    (r"|\rho_{\text{pw}}(\varphi, \hat\pi)| = 0.101$)", r"|\rho_{\text{pw}}(\varphi, \hat\pi)| = 0.103$)",
     [(GF + ("reported_alongside", "mean_independence_S0", "N3", "abs"), F3)]),
    ("($\\rho_S = 0.909$; the interval's lower bound, 0.827, clears",
     "($\\rho_S = 0.910$; the interval's lower bound, 0.829, clears",
     [(SP + ("rho",), F3), (SP + ("ci95_rho", 0), F3)]),
    ("was 0.909 for Gemini 4 Argon, 0.858 for GPT-6 Astra and 0.710 for Claude Fable 5.2",
     "was 0.915 for Gemini 4 Argon, 0.860 for GPT-6 Astra and 0.710 for Claude Fable 5.2",
     [(SP + ("per_model", "gemini-4-argon", "rho"), F3), (SP + ("per_model", "gpt-6-astra", "rho"), F3),
      (SP + ("per_model", "claude-fable-5-2", "rho"), F3)]),
    ("(rel3 0.969 with search off and 0.963 with search on)", "(rel3 0.969 with search off and 0.963 with search on)",
     [(REL + ("claude-fable-5-2|S0", "rel3"), F3), (REL + ("claude-fable-5-2|S1", "rel3"), F3)]),
    ("searched in 17.8% of its search-on calls", "searched in 17.8% of its search-on calls",
     [(("manipulation_checks", "MC_Search", "gemini-4-argon", "share"), lambda x: f"{100 * x:.1f}%")]),
    (r"($\Delta = -0.012$)", r"($\Delta = -0.016$)", [(SP + ("per_model", "gemini-4-argon", "delta"), F3)]),
    (r"($\Delta = -0.052$ for Claude Fable 5.2 and $-0.058$ for GPT-6 Astra)",
     r"($\Delta = -0.052$ for Claude Fable 5.2 and $-0.062$ for GPT-6 Astra)",
     [(SP + ("per_model", "claude-fable-5-2", "delta"), F3), (SP + ("per_model", "gpt-6-astra", "delta"), F3)]),
    ("(from 6.2 to 5.0 and from 5.5 to 4.2)", "(from 6.2 to 5.0 and from 5.6 to 4.2)",
     [(FORM + ("claude-fable-5-2|S0", "registry_brands_named_per_phase_B_answer"), F1),
      (FORM + ("claude-fable-5-2|S1", "registry_brands_named_per_phase_B_answer"), F1),
      (FORM + ("gpt-6-astra|S0", "registry_brands_named_per_phase_B_answer"), F1),
      (FORM + ("gpt-6-astra|S1", "registry_brands_named_per_phase_B_answer"), F1)]),
    ("rel1 from 0.845 to 0.915 and rel3 from 0.942 to 0.970", "rel1 from 0.850 to 0.916 and rel3 from 0.944 to 0.970",
     [(REL + ("gpt-6-astra|S1", "rel1"), F3), (REL + ("gemini-4-argon|S1", "rel1"), F3),
      (REL + ("gpt-6-astra|S1", "rel3"), F3), (REL + ("gemini-4-argon|S1", "rel3"), F3)]),
    ("of the 58 brands below the recall floor on the retiring panel, 43 (74%) were still below it",
     "of the 58 brands below the recall floor on the retiring panel, 42 (72%) were still below it",
     [(FLOOR + ("below_floor_t3",), INT), (FLOOR + ("below_both",), INT),
      (FLOOR + ("share_below_t3_still_below_t4",), PCT)]),
    ("and 11% of the brands above the floor fell below it", "and 11% of the brands above the floor fell below it",
     [(FLOOR + ("share_above_t3_now_below_t4",), PCT)]),
    ("at $t_4$ (49) than at $t_3$ (58)", "at $t_4$ (48) than at $t_3$ (58)",
     [(FLOOR + ("below_floor_t4",), INT), (FLOOR + ("below_floor_t3",), INT)]),
]

# The dated correction paragraph (after "Paper status"). Corrected values: leaves of the corrected verdicts and table;
# published values: leaves of osf/v42/v42_verdicts.json and v42_brand_table.csv (CORRECTION_CHECKS).
CORRECTION_ANCHOR = "Part of the AIAS measurement programme.\n"
CORRECTION = (
    "\n**Correction (25 November 2026).** This is revision r2 of the paper. It corrects a coding error found after "
    "publication. The brand matchers looked for the only two registry names that contain an apostrophe, Paula's "
    "Choice (skincare) and L'Oréal Paris (cosmetics), with a straight apostrophe (U+0027) only, so an answer that "
    "wrote either name with a typographic apostrophe (U+2019) was coded as not naming the brand: 46 of the 12,096 "
    "brand-answer cells "
    "of the category questions, all in these two brands' rows; no recognition code changed. The answers were "
    "re-coded with the typographic apostrophe read as an apostrophe and the locked coder otherwise unchanged; no "
    "model was called. Every number in this revision comes from the re-coded verdicts and brand table. No verdict "
    "changes. Corrected values, with the published ones in brackets: `H_Gen_Presence` ρ = 0.827, 95% interval "
    "0.718 to 0.889 [0.828, 0.722 to 0.890], CONFIRMED; `H_Gen_Phi` ρ = 0.304, p = 0.0070 [0.310, p = 0.0056], "
    "MARGINAL; `H_Search_Presence` ρ = 0.910, 95% interval 0.829 to 0.945 [0.909, 0.827 to 0.945], search-robust. "
    "Other figures move slightly, among them the level shift $\\Delta$ of the newest models against the retiring "
    "panel (+0.051 [+0.046]) and of search on against search off ($-0.043$ [$-0.041$]), the OpenAI and Google "
    "generation pairs (0.588 [0.566]; 0.707 [0.715]), the range of rel1 (0.850 to 0.916 [0.845 to 0.915]) and floor "
    "persistence (42 of 58, 72% [43 of 58, 74%]). The two brands' own rows change substantially: the three models "
    "named Paula's Choice in a share $\\hat\\pi$ = 0.759 [0.315] of their search-off answers, and GPT-6 Astra named "
    "it in 13 of its 18 search-off answers, not in none. Figures 1 to 5 are redrawn from the corrected table. The "
    "erratum on OSF (`v42/ERRATUM_2026-11-25.md`)^[\\url{" + ERRATUM_URL + "}] lists the changes. The published "
    "`v42_verdicts.json` and `v42_brand_table.csv` and the first version of this paper stay on OSF unchanged, beside "
    "`v42_brand_table_corrected_2026-11-25.csv`; the corrected verdicts and the list of all 74 changed values are in "
    "`v45/sensitivity/t4_SQ/`.\n")
# (which file, path or brand-table cell, formatter): every value printed in CORRECTION.
CORRECTION_CHECKS = [
    ("C", GP + ("rho",), F3), ("C", GP + ("ci95_rho", 0), F3), ("C", GP + ("ci95_rho", 1), F3),
    ("P", GP + ("rho",), F3), ("P", GP + ("ci95_rho", 0), F3), ("P", GP + ("ci95_rho", 1), F3),
    ("C", GF + ("rho",), F3), ("C", GF + ("p_perm",), F4), ("P", GF + ("rho",), F3), ("P", GF + ("p_perm",), F4),
    ("C", SP + ("rho",), F3), ("C", SP + ("ci95_rho", 0), F3), ("C", SP + ("ci95_rho", 1), F3),
    ("P", SP + ("rho",), F3), ("P", SP + ("ci95_rho", 0), F3), ("P", SP + ("ci95_rho", 1), F3),
    ("C", GP + ("delta",), FS), ("P", GP + ("delta",), FS), ("C", SP + ("delta",), F3), ("P", SP + ("delta",), F3),
    ("C", PAIRS + ("OpenAI: legacy pair -> gpt-6-astra", "rho"), F3),
    ("P", PAIRS + ("OpenAI: legacy pair -> gpt-6-astra", "rho"), F3),
    ("C", PAIRS + ("Google: legacy pair -> gemini-4-argon", "rho"), F3),
    ("P", PAIRS + ("Google: legacy pair -> gemini-4-argon", "rho"), F3),
    ("C", REL + ("gpt-6-astra|S1", "rel1"), F3), ("C", REL + ("gemini-4-argon|S1", "rel1"), F3),
    ("P", REL + ("gpt-6-astra|S1", "rel1"), F3), ("P", REL + ("gemini-4-argon|S1", "rel1"), F3),
    ("C", FLOOR + ("below_both",), INT), ("C", FLOOR + ("share_below_t3_still_below_t4",), PCT),
    ("P", FLOOR + ("below_both",), INT), ("P", FLOOR + ("share_below_t3_still_below_t4",), PCT),
    ("C", FLOOR + ("below_floor_t3",), INT),
    ("CT", ("v0.20", "Paula's Choice", "pi_N3_S0"), F3), ("PT", ("v0.20", "Paula's Choice", "pi_N3_S0"), F3),
    ("CT", ("v0.20", "Paula's Choice", "pi_gpt-6-astra_S0"), lambda x: f"{round(18 * x):d} of its 18"),
    ("PT", ("v0.20", "Paula's Choice", "pi_gpt-6-astra_S0"), lambda x: "not in none" if x == 0 else "MISMATCH"),
]


def _leaf(obj, path):
    for k in path:
        obj = obj[k]
    return obj


def _table_cell(csv_path, substrate, brand, column):
    import csv
    with open(csv_path, encoding="utf-8", newline="") as fh:
        rows = [r for r in csv.DictReader(fh) if r.get("substrate") == substrate and r.get("brand") == brand]
    if len(rows) != 1:
        sys.exit(f"[post-fill v42] REFUSED: brand-table row {substrate}/{brand} found {len(rows)} times")
    return float(rows[0][column])


def r2_texts(corrected, published):
    """The r2 edits and Discussion, after checking every printed number against its leaf."""
    def check(text, checks, src):
        for path, fmt in checks:
            s = fmt(_leaf(src, path))
            if s not in text:
                sys.exit(f"[post-fill v42] REFUSED: {'.'.join(map(str, path))} = {s!r} is not in {text[:60]!r}")
    edits = []
    for old, new, checks in R2_ABSTRACT:
        check(new, checks, corrected)
        edits.append((old, new))
    edits += EDITS[2:]
    disc = DISCUSSION
    for old, new, checks in R2_SUBS:
        if disc.count(old) != 1:
            sys.exit(f"[post-fill v42] REFUSED: Discussion text not found exactly once: {old[:60]!r}")
        check(new, checks, corrected)
        disc = disc.replace(old, new)
    for which, path, fmt in CORRECTION_CHECKS:
        if which in ("C", "P"):
            v = _leaf(corrected if which == "C" else published, path)
        else:
            v = _table_cell(CORRECTED_TABLE if which == "CT" else PUBLISHED_TABLE, *path)
        s = fmt(v)
        if s not in CORRECTION:
            sys.exit(f"[post-fill v42] REFUSED: correction paragraph lacks {which}:{path} = {s!r}")
    edits.append((CORRECTION_ANCHOR, CORRECTION_ANCHOR + CORRECTION))
    return edits, disc


def main(argv=None):
    import argparse
    import json
    ap = argparse.ArgumentParser(description="Hand-written text of the v0.42 paper, applied after the fill")
    ap.add_argument("--verdicts", type=Path, default=VERDICTS,
                    help="osf/v42/v42_verdicts.json (r1, as published) or the corrected file of 25 Nov 2026 (r2)")
    a = ap.parse_args(argv)
    sha = hashlib.sha256(a.verdicts.read_bytes()).hexdigest()
    if sha == VERDICTS_SHA256:
        edits, discussion = EDITS, DISCUSSION
    elif sha == CORRECTED_SHA256:
        if hashlib.sha256(CORRECTED_TABLE.read_bytes()).hexdigest() != CORRECTED_TABLE_SHA256:
            sys.exit("[post-fill v42] REFUSED: the corrected brand table is not the file of 25 November 2026")
        if hashlib.sha256(VERDICTS.read_bytes()).hexdigest() != VERDICTS_SHA256:
            sys.exit("[post-fill v42] REFUSED: osf/v42/v42_verdicts.json is not the published file")
        edits, discussion = r2_texts(json.loads(a.verdicts.read_text(encoding="utf-8")),
                                     json.loads(VERDICTS.read_text(encoding="utf-8")))
    else:
        sys.exit("[post-fill v42] REFUSED: the verdicts file is neither the published nor the corrected one")
    t = DRAFT.read_text(encoding="utf-8")
    for old, new in edits:
        if t.count(old) != 1:
            sys.exit(f"[post-fill v42] REFUSED: anchor not found exactly once: {old[:70]!r}")
        t = t.replace(old, new)
    a_, b_ = t.index("# 4. Discussion"), t.index("# 5. Limitations")
    t = t[:a_] + discussion + t[b_:]
    if t.count("Samsung") != t.split("# Declarations")[1].count("Samsung"):
        sys.exit("[post-fill v42] REFUSED: Samsung outside the Declarations")
    DRAFT.write_text(t, encoding="utf-8")
    print(f"[post-fill v42] applied {len(edits)} edits and the Discussion to {DRAFT}"
          f" ({'r2, corrected' if sha == CORRECTED_SHA256 else 'r1, published'} verdicts)")


if __name__ == "__main__":
    main()
