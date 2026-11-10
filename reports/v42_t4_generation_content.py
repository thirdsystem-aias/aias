"""
v0.42 - t4 wave on the newest models - Brand-format report content module.
Third System(TM) managerial register (P1-P5 propositional framing; no hypothesis labels, no employer disclosure:
that lives in the SSRN paper's Declarations).

Unlike earlier content modules, this one is written before the data exist. Every proposition has one wording per
pre-registered outcome, chosen from the verdicts at build time, and every number is read from the scorer's verdicts
JSON through papers/v0_42/v42_values.py (no number is typed here):

  P1  Presence standings carry over to the newest models          (H_Gen_Presence, primary)
  P2  Consistency standings carry over to the newest models       (H_Gen_Phi, secondary)
  P3  Web search leaves Presence standings intact                 (H_Search_Presence, secondary, two-sided)
  P4  Run-to-run variation on the newest models                   (pre-registered descriptive 1)
  P5  Brands below the recall floor before and after the switch   (pre-registered descriptive 3)

Inputs (environment, set by reports/build_report_v42.py from its --verdicts option):
  AIAS_V42_VERDICTS   default <repo>/osf/v42/v42_verdicts.json
Markup per build_report: <sub> subscripts, NBSP-wrapped arrows; Akkurat lacks the >= and Delta glyphs, so the
text says "at least" and "shift".
"""
import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "papers/v0_42"))
import v42_values as VV  # noqa: E402

_VERDICTS = Path(os.environ.get("AIAS_V42_VERDICTS", str(_ROOT / "osf/v42/v42_verdicts.json")))
_SRC = VV.load_sources(_VERDICTS)
V = _SRC["verdicts"]
SYNTHETIC = VV.is_synthetic(V)
G, PH, S = V["verdicts"]["H_Gen_Presence"], V["verdicts"]["H_Gen_Phi"], V["verdicts"]["H_Search_Presence"]
CG, CP, CS = VV.case_gen(V), VV.case_phi(V), VV.case_search(V)
DEC = ("CONFIRMED", "MARGINAL", "FALSIFIED")
MCC = V["manipulation_checks"]["MC_Complete"]
REL = V["descriptives"]["1_run_reliability"]
FL = V["descriptives"]["3_floor_persistence"]
r2, i0 = VV.r2, VV.i0


def _rel_range(key):
    vals = [d[key] for d in REL.values() if VV.has(d, [key])]
    return (r2(min(vals)), r2(max(vals))) if vals else ("--", "--")


REL1, REL3 = _rel_range("rel1"), _rel_range("rel3")
ANS, EXP = i0(MCC["answered"]), i0(MCC["expected"])

COVER = {
    "title": "New Models, Same Standings?",
    "subtitle": (
        "The same 112 brands and the same questions, put to the newest AI model of Anthropic, OpenAI and Google "
        "with web search off and on, and compared with the retiring models a few days earlier."
    ),
}

STANDFIRST = (
    "Every AI brand measure rests on the models that produce it, and those models are replaced. In November the "
    "six models behind the AIAS measurements since May 2026 begin to retire. We asked their successors, the "
    "newest flagship model of Anthropic, OpenAI and Google, the same questions about the same 112 brands, "
    "with and without their own web search, to see whether brand standings survive the switch, and how much the "
    "new models' answers vary when the same question is asked again."
)

_lead = []
if CG in DEC:
    _lead.append(f"Presence order, retiring models against newest: {r2(G['rho'])} across {i0(G['n'])} brands "
                 f"(registered bar 0.70).")
else:
    _lead.append("Presence order across the switch: not decided.")
if CP in DEC:
    _lead.append(f"Consistency order: {r2(PH['rho'])} across {i0(PH['n'])} brands (bar 0.50).")
else:
    _lead.append("Consistency order: not decided.")
if CS in ("ROBUST", "SENSITIVE", "DOMINATED"):
    _lead.append(f"Search off against search on: {r2(S['rho'])}, range {r2(S['ci95_rho'][0])} to {r2(S['ci95_rho'][1])}.")
_lead.append(f"{ANS} of {EXP} questions answered.")
LEAD_DECK = " ".join(_lead)

_P1_SUMMARY = {
    "CONFIRMED": "First, Presence: the order of brands by how often they are named carried over from the retiring "
                 "models to the newest ones, above the bar registered in advance.",
    "MARGINAL": "First, Presence: the newest models order brands in a way related to the retiring models' order, "
                "but below the bar registered in advance for calling it the same.",
    "FALSIFIED": "First, Presence: the newest models order brands differently from the retiring ones; the "
                 "correlation fell below the bar registered in advance for a clear difference.",
    "UNDETERMINED_EXCLUDED": "First, Presence: the comparison could not be judged, because one of the new models "
                             "answered too few questions under the rules set in advance.",
    "UNDETERMINED_DEGENERATE": "First, Presence: the comparison could not be judged on these data.",
}
_P2_SUMMARY = {
    "CONFIRMED": "Second, Consistency: the brands the models agree on, and the ones they split on, stayed the same "
                 "across the switch.",
    "MARGINAL": "Second, Consistency: the pattern of agreement carried over only in part.",
    "FALSIFIED": "Second, Consistency: the pattern of agreement changed with the new models.",
    "UNDETERMINED_FLOOR": "Second, Consistency: too few brands could be scored on both sets of models to judge it.",
    "UNDETERMINED_EXCLUDED": "Second, Consistency: not judged, for the same reason.",
    "UNDETERMINED_DEGENERATE": "Second, Consistency: not judged on these data.",
}
_P3_SUMMARY = {
    "ROBUST": "Third, web search: switching on each model's own search left the order of brands intact.",
    "SENSITIVE": "Third, web search: switching on each model's own search reshuffled part of the order.",
    "DOMINATED": "Third, web search: switching on each model's own search rewrote the order.",
    "UNDETERMINED": "Third, web search: its effect could not be judged on these data.",
    "NOT_COMPUTED": "Third, web search: its effect could not be judged, because no model kept enough answers in "
                    "both settings.",
}
_IMPLICATION = {
    "CONFIRMED": "The implication for brand teams: a brand's standing measured on the older models remains a usable "
                 "reference on the new ones. What carries over is the order of brands, not necessarily how often "
                 "each is named.",
    "MARGINAL": "The implication for brand teams: standings measured on the older models are a guide to the new "
                "ones, not a substitute. Re-measure before comparing.",
    "FALSIFIED": "The implication for brand teams: standings measured on the older models do not carry over. A "
                 "brand's standing on the new models has to be measured afresh.",
    "UNDETERMINED_EXCLUDED": "The implication for brand teams: this wave cannot say whether older standings carry "
                             "over; it does set the baseline for the new models.",
    "UNDETERMINED_DEGENERATE": "The implication for brand teams: this wave cannot say whether older standings carry "
                               "over; it does set the baseline for the new models.",
}

EXEC_SUMMARY = (
    _P1_SUMMARY[CG] + " " + _P2_SUMMARY[CP] + " " + _P3_SUMMARY[CS]
    + " Fourth and fifth, we record how much the answers vary between repeated runs, the yardstick for the next "
      "waves, and which brands stay below the recall floor.\n\n" + _IMPLICATION[CG]
)

WHAT_WE_MEASURED = (
    "This is the fourth measurement of five category panels first measured in May 2026: audiophile headphones (16 "
    "brands), and skincare, cosmetics, automotive and premium spirits (24 each). The third measurement ran on 9 "
    "November on six models that are now retiring. This one put the same questions, word for word, to the newest "
    "flagship model of Anthropic, OpenAI and Google: Claude Fable 5.2, GPT-6 Astra and Gemini 4 Argon.\n\n"
    "The 30 category questions (\"What are the best skincare brands?\" and its equivalents) were asked three times "
    "each, once with each model's own web search switched off and once with it on; the 112 brand questions were "
    "asked once, without search: 876 questions in all. Presence measures how often a model names a brand when a "
    "buyer-style question is asked without prompting. Consistency measures whether the models agree about that "
    "brand. The tests, the pass marks and a spending cap of US$100 were registered publicly before the first "
    f"question was sent. {ANS} of the {EXP} questions returned an answer."
)

PATTERNS = ""

LIMITATIONS = (
    "A new model generation arrives with new default settings, newer training data and, here, one model per "
    "provider instead of two. The comparison is of the models as a user meets them, so it cannot say which of these "
    "changes moved a brand. Consistency is measured on three models instead of six, which makes it noisier.\n\n"
    "Answers with web search depend on what the web returned that day and can be reproduced only as recorded. The "
    "study covers one market and language (US English) and five mature consumer categories. Three runs per question "
    "give a first, coarse estimate of run-to-run variation. Stability here is stability of the measurement, not "
    "proof that it tracks sales or preference."
)

WHATS_NEXT = (
    "The same questions go to the same three models again in early December and in February, each time under its "
    "own registration and budget. The run-to-run figures in this report are the yardstick for those waves: a change "
    "smaller than the variation between repeated runs is not a change.\n\n"
    "The answers collected here are also the starting material for four further measures of AI availability "
    "(where a brand appears in a list, how it is described, and which sources and citations stand behind the "
    "answers), each tested in its own study."
)

_P1_HEAD = {"CONFIRMED": "Brand standings carried over to the newest models",
            "MARGINAL": "Brand standings carried over only in part",
            "FALSIFIED": "The newest models rank brands differently",
            "UNDETERMINED_EXCLUDED": "The switch of models could not be judged",
            "UNDETERMINED_DEGENERATE": "The switch of models could not be judged"}
_P2_HEAD = {"CONFIRMED": "The models still agree about the same brands",
            "MARGINAL": "Agreement patterns carried over only in part",
            "FALSIFIED": "Agreement patterns changed with the new models",
            "UNDETERMINED_FLOOR": "Too few brands to judge agreement",
            "UNDETERMINED_EXCLUDED": "Agreement could not be judged",
            "UNDETERMINED_DEGENERATE": "Agreement could not be judged"}
_P3_HEAD = {"ROBUST": "Web search left the order intact",
            "SENSITIVE": "Web search reshuffled part of the order",
            "DOMINATED": "Web search rewrote the order",
            "UNDETERMINED": "The effect of web search could not be judged",
            "NOT_COMPUTED": "The effect of web search could not be judged"}


def _q1():
    if CG in DEC:
        return f"rank correlation {r2(G['rho'])} across {i0(G['n'])} brands; registered bar 0.70"
    return "not decided under the rules registered in advance"


def _q2():
    if CP in DEC:
        return f"rank correlation {r2(PH['rho'])} across {i0(PH['n'])} brands; registered bar 0.50"
    if CP == "UNDETERMINED_FLOOR":
        return f"{i0(PH['n'])} brands scored on both, below the registered minimum of 40"
    return "not decided under the rules registered in advance"


def _q3():
    if CS in ("ROBUST", "SENSITIVE", "DOMINATED"):
        return f"rank correlation {r2(S['rho'])}, plausible range {r2(S['ci95_rho'][0])} to {r2(S['ci95_rho'][1])}"
    return "no plausible range could be computed"


def _q5():
    if FL.get("status") == "NOT_COMPUTED":
        return "not computed"
    return f"{i0(FL['below_both'])} of {i0(FL['below_floor_t3'])} brands below the floor stayed below it; descriptive"


def _status(case):
    st = VV.REPORT_STATUS[case]
    return st, VV.REPORT_STATUS_CLASS[st]


HYPOTHESIS_SCORING = [
    {"id": "P1", "headline": _P1_HEAD[CG], "proposition": "Presence standings carry over from the retiring AI models "
     "to the newest ones.", "verdict": _status(CG)[0], "qualifier": _q1(), "status_class": _status(CG)[1]},
    {"id": "P2", "headline": _P2_HEAD[CP], "proposition": "Consistency standings carry over to the newest models.",
     "verdict": _status(CP)[0], "qualifier": _q2(), "status_class": _status(CP)[1]},
    {"id": "P3", "headline": _P3_HEAD[CS], "proposition": "Switching on the models' own web search leaves Presence "
     "standings intact.", "verdict": _status(CS)[0], "qualifier": _q3(), "status_class": _status(CS)[1]},
    {"id": "P4", "headline": "How much the answers vary from run to run",
     "proposition": "The newest models give the same brand order when asked the same questions again.",
     "verdict": "OBSERVED", "qualifier": f"one run against another {REL1[0]} to {REL1[1]}; average of three runs "
     f"{REL3[0]} to {REL3[1]}; descriptive", "status_class": "neutral"},
    {"id": "P5", "headline": "Who stays below the recall floor",
     "proposition": "Brands rarely named by the retiring models are still rarely named by the newest ones.",
     "verdict": "OBSERVED", "qualifier": _q5(), "status_class": "neutral"},
]


def _p1_detail():
    if CG not in DEC:
        why = ("one of the three new models answered fewer than 90% of its questions without search, and the rules "
               "registered in advance then leave the test undecided." if CG == "UNDETERMINED_EXCLUDED"
               else "the statistic could not be computed on these data.")
        return f"The comparison was not decided: {why}"
    txt = (f"Across the {i0(G['n'])} brands, the order by Presence on the newest models, without web search, "
           f"correlated with the order on the retiring models at {r2(G['rho'])} (plausible range "
           f"{r2(G['ci95_rho'][0])} to {r2(G['ci95_rho'][1])}). The bar registered in advance was 0.70 to call the "
           f"order the same, and below 0.50 to call it different. ")
    lo, hi = G["ci95_delta"]
    if lo > 0:
        txt += "On average the newest models named a brand in a larger share of answers than the retiring models."
    elif hi < 0:
        txt += "On average the newest models named a brand in a smaller share of answers than the retiring models."
    else:
        txt += "On average the newest models named brands about as often as the retiring models did."
    pp = (G.get("reported_alongside") or {}).get("per_provider_generation_pairs") or {}
    bits = [f"{prov} {r2(pp[VV.PAIR_KEY[prov]]['rho'])}" for prov in VV.PROVIDERS
            if VV.has(pp.get(VV.PAIR_KEY[prov]) or {}, ["rho"])]
    if bits:
        txt += (" Provider by provider, comparing each provider's two retiring models with its new one: "
                + ", ".join(bits) + ".")
    return txt


def _p2_detail():
    if CP in DEC:
        return (f"Consistency could be scored on both sets of models for {i0(PH['n'])} brands. Their order correlated "
                f"at {r2(PH['rho'])} (plausible range {r2(PH['ci95_rho'][0])} to {r2(PH['ci95_rho'][1])}); the bar "
                "registered in advance was 0.50, and below 0.30 counts as a change. With three models instead of "
                "six, each brand's score rests on fewer opinions, so some movement is expected from that alone.")
    if CP == "UNDETERMINED_FLOOR":
        return (f"Only {i0(PH['n'])} brands could be scored on both sets of models; the minimum registered in "
                "advance was 40, so the comparison is not decided.")
    return "The comparison was not decided under the rules registered in advance."


def _p3_detail():
    if CS not in ("ROBUST", "SENSITIVE", "DOMINATED"):
        return "The effect of web search could not be judged on these data."
    pm = S.get("per_model") or {}
    bits = [f"{VV.MODEL_NAME[m]} {r2(pm[m]['rho'])}" for m in VV.N3 if VV.has(pm.get(m) or {}, ["rho"])]
    txt = (f"With search on, the brand order by Presence correlated with the order without search at {r2(S['rho'])} "
           f"(plausible range {r2(S['ci95_rho'][0])} to {r2(S['ci95_rho'][1])}). The reading registered in advance: "
           "unchanged if the whole range is at least 0.80, rewritten if it is entirely below 0.50, partly changed "
           "otherwise. ")
    if bits:
        txt += "Model by model: " + ", ".join(bits) + "."
    return txt


def _p4_detail():
    return (f"Each category question was asked three times with search off and three times with search on. From one "
            f"run to the next, the brand order agreed at {REL1[0]} to {REL1[1]} across models and settings; averaged "
            f"over three runs, as the scores are, the agreement is {REL3[0]} to {REL3[1]}. No pass mark was set: "
            "these figures are the yardstick for the next waves.")


def _p5_detail():
    if FL.get("status") == "NOT_COMPUTED":
        return "Not computed: one of the new models was excluded without search."
    return (f"The recall floor is fewer than one mention per model on average. Of the {i0(FL['below_floor_t3'])} "
            f"brands below it on the retiring models, {i0(FL['below_both'])} were still below it on the newest "
            f"models; of the {i0(FL['below_floor_t4'])} below it on the newest models, "
            f"{i0(FL['below_floor_t4'] - FL['below_both'])} had been above it before. No pass mark was set.")


HYPOTHESIS_DETAILS = {"P1": _p1_detail(), "P2": _p2_detail(), "P3": _p3_detail(), "P4": _p4_detail(),
                      "P5": _p5_detail()}

FIGURE_CAPTIONS = {
    "p1": ("Each brand's Presence (the share of category answers that name it) on the six retiring models against "
           "the newest model of each provider, without web search. On the dashed line a brand is named equally "
           "often by both."),
    "p2": ("Each brand's Consistency score on the retiring models against the newest models; lower means the "
           "models agree more. Only brands that could be scored on both sets are shown."),
    "p3": ("Left: each brand's Presence on the newest models without and with their own web search. Right: how "
           "closely the two brand orders agree, overall with its plausible range, and by model and category."),
    "p4": ("How closely the brand order repeats when the same model answers the same questions again, for each "
           "model with search off and on."),
    "p5": ("Brands named less than once per model on average: how many were below that floor on the retiring "
           "models, on the newest models, and on both."),
}

CLOSING = (
    "The first three waves showed that AI brand standings hold for months on one set of models. This wave asks "
    "the question every tracking metric eventually faces: what happens when the instrument itself is replaced. "
    "Its answer, and the run-to-run baseline it sets, decide how the next waves on the new models are read."
)
