#!/usr/bin/env python3
"""post_fill_real_v0_42.py -- the hand-written text of the t4 paper, applied after fill_paper_v0_42.py.

Written on 2026-11-11 (US Central) from the real scorer outputs of commit 31c64c6 (v0.42 scoring, once):
osf/v42/v42_verdicts.json (sha256 b5094ced...) and osf/v42/v42_brand_table.csv (sha256 792e14ad...).
fill_paper_v0_42.py picks pre-written sentences by verdict case; this step replaces the generic Discussion
with one written for the observed results and adds the sentences the template could not anticipate. Every
number below is a leaf of v42_verdicts.json, formatted as the fill formats it (paths in the comments), or a
sum or difference of such leaves; the dates and the 72 judge calls come from osf/v42/data/code_v0_42.log and
the pre-registration. Run after the fill and before scripts/build_paper_v0_42.py:

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
    "the study's current Anthropic organization: a first coding attempt on 11 November 2026 returned a not-found "
    "error for every judge call, none of them billed, and its tables were set aside. With the pre-registrant's "
    "decision, the judge was called through the Anthropic organization that coded $t_1$--$t_3$, with the same "
    "model, code and prompts, and coded 72 of 72 answers."))

# §3.1: raw records per attempt. descriptives.6_cost.per_model_condition.*.records (sum 990) and
# .billed_requests; 990 - 876 = 114; 120 - 90 = 30; 208 - 202 = 6; 168 - 90 = 78.
EDITS.append((
    "No pause approval was recorded by the budget guard.",
    "No pause approval was recorded by the budget guard. The raw file holds one record per attempt: 990 records "
    "for the 876 calls. The 114 additional records (30 for Claude Fable 5.2 with search on, 6 for Gemini 4 Argon "
    "with search off and 78 for Gemini 4 Argon with search on) are attempts that ended without an answer and "
    "without billed usage and were re-sent under the call policy; each call is analysed once, from its answered "
    "attempt."))

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

The bridge is not uniform. Four substrates kept their order closely (per-substrate $\rho$ from 0.855 to 0.943 with search off), while premium spirits reached 0.607. The spirits substrate is also the one whose category questions use expert-acclaim and cultural-community frames rather than requests for the best brands (§2.3), which may leave a new generation more room to choose differently; the design does not test this. Per provider, the legacy pair against its new model gave $\rho_{\text{pw}} = 0.848$ for Anthropic, 0.715 for Google and 0.566 for OpenAI. These single-model comparisons are reported alongside and decide nothing, and one model's Presence rests on fewer answers than the panel's. Still, a user of one provider's newest model meets a brand order that departs further from that provider's legacy models than the three-model panel departs from the six-model panel, most of all for OpenAI.

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
              "a Gemini 4 Argon prompt was blocked (`osf/v42/DEVIATIONS.md`, Entry 1). The v0.23 recognition "
              "judge was called through a different Anthropic organization from the study's own, with the same "
              "model, code and prompts (§2.6).")
EDITS.append((LIMITS_OLD, LIMITS_NEW))


def main():
    if hashlib.sha256(VERDICTS.read_bytes()).hexdigest() != VERDICTS_SHA256:
        sys.exit("[post-fill v42] REFUSED: v42_verdicts.json is not the file this text was written for")
    t = DRAFT.read_text(encoding="utf-8")
    for old, new in EDITS:
        if t.count(old) != 1:
            sys.exit(f"[post-fill v42] REFUSED: anchor not found exactly once: {old[:70]!r}")
        t = t.replace(old, new)
    a, b = t.index("# 4. Discussion"), t.index("# 5. Limitations")
    t = t[:a] + DISCUSSION + t[b:]
    if t.count("Samsung") != t.split("# Declarations")[1].count("Samsung"):
        sys.exit("[post-fill v42] REFUSED: Samsung outside the Declarations")
    DRAFT.write_text(t, encoding="utf-8")
    print(f"[post-fill v42] applied {len(EDITS)} edits and the Discussion to {DRAFT}")


if __name__ == "__main__":
    main()
