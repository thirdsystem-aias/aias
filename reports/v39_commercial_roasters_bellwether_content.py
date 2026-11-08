"""
v0.39 — Commercial Coffee Roasters (Bellwether-focal) — brand-format report content module.
Third System(TM) managerial register, written for brand teams and prospective clients.

Register discipline (carried from v0.38):
  - No hypothesis labels (H_*) or test jargon in body text; plain brand-strategy voice.
  - Every number below is read from the locked outputs at import time (v39_verdicts.json, v39_tables.json,
    v39_coder_audit.json, v39_coded.csv); the asserts guard every figure the prose states in words.
  - Two supporting tests were FALSIFIED; they are reported as what they are and framed as findings.
  - No Samsung (commercial outputs omit it per brand JSON). The focal-brand disclosure (author met Bellwether
    staff; owns an Aillio Bullet R1; no relationship with any registry brand) is stated in the closing block.
  - Avoid glyphs Akkurat Pro lacks (arrows, >=, subscripts): write them out.
"""
import csv
import json
import os
from collections import Counter
from pathlib import Path

_ROOT = Path(os.environ.get("AIAS_ROOT", "/Users/pablou/aias"))
_V = json.loads((_ROOT / "osf/v39/v39_verdicts.json").read_text(encoding="utf-8"))
_T = json.loads((_ROOT / "osf/v39/data/v39_tables.json").read_text(encoding="utf-8"))
_A = json.loads((_ROOT / "osf/v39/data/v39_coder_audit.json").read_text(encoding="utf-8"))
_REG = json.loads((_ROOT / "osf/v39/registries/brands_commercial_roasters_v0.39.json").read_text(encoding="utf-8"))
with open(_ROOT / "osf/v39/data/v39_coded.csv", encoding="utf-8") as _f:
    _C = list(csv.DictReader(_f))
_NAMES = {b["id"]: b["brand"] for b in _REG["brands"]}
_STRATUM = {b["id"]: b["stratum"] for b in _REG["brands"]}
_P = _T["presence"]
_D = _T["descriptives"]
_FR = _A["frame_classification"]["summary"]


def _pc(x):
    return f"{round(100 * x)}%"


def _bw(cell):
    return _P[cell]["presence"]["B01"] or 0


def _first(arm, cond, tier="C"):
    rows = [r for r in _C if r["arm"] == arm and r["condition"] == cond and r["tier"] == tier and r["status"] == "ok"]
    return sum(1 for r in rows if r["brands_in_order"].split(";")[0] == "B01"), len(rows)


# ---------------- numbers used in the prose (all derived) ----------------
VENT_L, LESS_L = _V["H_Frame"]["vent_share"], _V["H_Frame"]["ventless_share"]
F_L = _FR["L|S0"]
F_REQ_L = F_L["counts"].get("venting required", 0)
LESS_S0, LESS_S1 = _FR["C|S0"]["ventless_raised"], _FR["C|S1"]["ventless_raised"]
N_F_C = _FR["C|S0"]["n"]
G_L, C_L = _V["H_CEP"]["presence_G"], _V["H_CEP"]["presence_C"]
K_C_L = round(C_L * _V["H_CEP"]["n_C"])
CEP_PTS = round(100 * _V["H_CEP"]["delta"])
CEP_P = _V["H_CEP"]["p_one_sided"]
MODELS_POS = _V["H_CEP"]["models_positive"]
RANK_L = _V["H_CEPDefault"]["rank"]
TOP_L = _V["H_CEPDefault"]["top5"]
FIRST_L, N_C_L = _first("L", "S0")
G_S0, C_S0, G_S1, C_S1 = _bw("C|S0|G"), _bw("C|S0|C"), _bw("C|S1|G"), _bw("C|S1|C")
FIRST_S0, N_C_S0 = _first("C", "S0")
FIRST_S1, N_C_S1 = _first("C", "S1")
S_S0, S_S1 = _V["H_Search"]["presence_S0"], _V["H_Search"]["presence_S1"]
S_B, S_C = _V["H_Search"]["b_s1_only"], _V["H_Search"]["c_s0_only"]
CR0 = _T["descriptives"]["D5_show_floor_vs_ai_shelf"]
D7 = _D["D7_retrieval"]
CITE_BW = round(D7["share_citing_bellwethercoffee"] * D7["n_s1"])
D3 = _A["D3_claim_reproduction"]
N_UNIQ = len(D3["reproduced_as_fact"]) + len(D3["reproduced_with_attribution"])
N_UNIQ_FACT = len(D3["reproduced_as_fact"])
D4 = _A["D4_ventless_attribution"]
STRONG_VENTLESS = D4["described_as_ventless_or_no_venting"]["Stronghold"] + D4["ventless_with_add_on_smoke_filter"]["Stronghold"]
STRONG_NEEDS = 7  # Claude Opus 5.5 with search (coder audit, D4 observations)
SF = {k: v["show_floor_presence"] for k, v in CR0.items()}
N_REC = sum(v["n"] for v in CR0.values())
D10 = _D["D10_five_model_sensitivity"]
LAB = _A["k_probe_labels"]
K3_WRONG_L = sum(1 for m in ("M1", "M2", "M3", "M4", "M5", "M6") if "(wrong)" in LAB["K3_venting"][m])
DK_K1_L = sum(1 for m in ("M1", "M2", "M3", "M4", "M5", "M6") if LAB["K1_newest"][m] == "Doesn't know")
MARK26 = D7["markers_2026_in_K1_K2"]
N26_S1 = sum(1 for k in MARK26 if k.endswith("|S1"))
N26_S0 = sum(1 for k in MARK26 if k.endswith("|S0"))
M5_CAP = round(D10["m5_capped_share"] * 30)
AUD = _A["overall_disagreement"]
CM = Counter()
for _r in _C:
    if _r["arm"] == "C" and _r["tier"] in ("G", "C"):
        CM[(_r["model_slot"], _r["condition"])] += int(_r["bellwether"])

# guards on every figure the prose states in words
assert _V["status"] == "FINAL"
assert (F_REQ_L, F_L["n"], F_L["ventless_raised"]) == (34, 36, 0)
assert (LESS_S0, LESS_S1, N_F_C) == (8, 13, 18)
assert (G_L, K_C_L, MODELS_POS, RANK_L) == (0.0, 9, 5, 7)
assert (FIRST_L, N_C_L, FIRST_S0, FIRST_S1, N_C_S0) == (2, 36, 15, 17, 18)
assert [n for n, _ in TOP_L[:2]] == ["Loring", "Diedrich"] and TOP_L[0][1] == 0.5 == TOP_L[1][1]
assert (S_B, S_C) == (2, 4) and _V["H_Search"]["verdict"] == "FALSIFIED"
assert (CM[("C1", "S0")], CM[("C1", "S1")], CM[("C3", "S0")], CM[("C3", "S1")]) == (10, 7, 12, 12)
assert (N26_S0, N26_S1, CITE_BW, D7["n_s1"]) == (0, 6, 43, 90)
assert (N_UNIQ, N_UNIQ_FACT, STRONG_VENTLESS, K3_WRONG_L, DK_K1_L) == (8, 4, 15, 3, 5)
assert SF["L|S0"]["Air-Motion Roasters"] == SF["C|S0"]["Air-Motion Roasters"] == SF["C|S1"]["Air-Motion Roasters"] == 0
assert N_REC == 216 and M5_CAP == 26 and D10["H_CEPDefault"]["rank"] == 8

TITLE = "Bellwether Owns the No-Vent Answer — On the Newest AI Assistants"

COVER = {
    "title": TITLE,
    "subtitle": ("Today's AI assistants name Bellwether first when a café can't vent. The 2024–25 models still behind "
                 "many tools tell cafés to vent, never raise a ventless option, and rank Bellwether seventh even when "
                 "asked for one. Web search adds currency, not presence."),
    "tagline": "AIAS™ Measurement Program · Phase v0.39<br/>Third System™",
    "date": "November 2026",
}

STANDFIRST = (
    "When a café owner asks an AI assistant whether to roast in-house, the answer decides whether Bellwether is "
    "ever in the conversation. On the 2024–25 models still running behind many tools, it almost never is: they tell "
    "cafés to plan for ductwork and permits and say nothing of roasters that need neither. Bellwether appears only "
    "when the owner names the barrier, and even then six other makers are named more often. On today's assistants the picture "
    "reverses: Bellwether is the first name for a café that can't vent, without any web search at all."
)

LEAD_DECK = (
    "v0.39 asked nine AI models 30 questions a café owner might ask: whether and how to roast in a café, which roaster "
    "to buy in general and under a stated constraint, which production roaster suits a growing roastery, and six "
    "direct questions about Bellwether. Six models are the program's fixed 2024–25 panel; three are current "
    "assistants — Claude Opus 5.5, GPT-6 Astra and Gemini 4 Argon — asked with and without web search. All 360 answers "
    "were scored against a 36-brand registry. The questions, brand list, coding rules and pass marks were deposited "
    "publicly before the first model was asked."
)

EXEC_SUMMARY = "\n\n".join([
    (f"<b>Older models frame in-café roasting as a venting job.</b> Asked whether and how a café should roast, the six "
     f"2024–25 models present ventilation as part of the job in {F_REQ_L} of {F_L['n']} answers and never mention a "
     f"roaster that needs none. Current assistants raise a ventless option in {_pc(LESS_S0 / N_F_C)} of those answers "
     f"without search and {_pc(LESS_S1 / N_F_C)} with it — and whenever they attach a brand, it is Bellwether."),
    (f"<b>On older models, Bellwether lives only inside its own entry point.</b> The fixed panel names Bellwether in "
     f"none of 36 generic café recommendations and in {_pc(C_L)} once the café says it has no gas line, cannot vent or "
     f"faces air-quality rules: a {CEP_PTS}-point gap that five of the six models share, and one that would arise by "
     f"chance fewer than two times in a thousand. Even then it ranks seventh; Loring and Diedrich appear in half of "
     f"those answers."),
    (f"<b>Current assistants have learned Bellwether; search keeps them current.</b> Without searching the web, Claude "
     f"Opus 5.5, GPT-6 Astra and Gemini 4 Argon name Bellwether in {_pc(C_S0)} of constraint answers, name it first in "
     f"{_pc(FIRST_S0 / N_C_S0)}, and name it in {_pc(G_S0)} of generic café recommendations. Search does not raise "
     f"that share ({_pc(S_S0)} without it, {_pc(S_S1)} with it); it updates the facts. With search, every lineup answer "
     f"names the Shop Roaster announced in October 2026 and every capacity answer gives its 1.5 kg batch; without "
     f"search, none does."),
    (f"<b>What to do.</b> Bellwether's AI problem has moved from absence to precision. On current assistants, protect "
     f"the claim the position rests on: Gemini 4 Argon describes Stronghold as ventless in {STRONG_VENTLESS} answers, "
     f"five of them with an add-on filter, while search-enabled Claude says Stronghold still needs an exhaust. On the older models still built into many tools, "
     f"the target is the frame itself: content that answers “should my café roast in-house?” with the ventless "
     f"route in the first paragraph, not after the venting checklist."),
])

WHAT_WE_MEASURED = "\n\n".join([
    ("v0.39 asked the questions a café owner asks before buying a roaster — 30 of them, in five sets of six. The first "
     "set asks whether and how to roast in a café, without naming a machine. The second asks for a café roaster in "
     "generic terms; the third asks the same with a constraint stated: no gas line, no ductwork, a lease that forbids "
     "roof vents, smoke, strict air-quality rules, or simply the best electric roaster. The fourth asks about "
     "production roasters, and the last six ask about Bellwether directly: its newest machine, its lineup, whether it "
     "needs venting, which model to buy, its batch size and how it differs."),
    ("Each question went once to nine models. Six are the program's fixed panel — Claude Opus 4.5 and Sonnet 4.5, "
     "GPT-4o and GPT-4o-mini, Gemini 2.5 Flash and Flash-Lite — released in 2024 and 2025 and still served through "
     "developer APIs and the tools built on them. Three are current assistants — Claude Opus 5.5, GPT-6 Astra and "
     "Gemini 4 Argon — each asked twice, without and with the provider's own web search. That is 360 answers, "
     "collected on 8 November 2026, three weeks after Bellwether debuted its new Shop Roaster at Coffee Fest "
     "Dallas-Fort Worth."),
    ("Every answer was scored against a registry of 36 roaster makers: the six exhibitors on the Coffee Fest floor, "
     "the makers AI models named in the program's previous phase, the manufacturers in a commercial-equipment index, "
     "and two more brands that claim in-store roasting. Everything — questions, brand list, coding rules, pass marks "
     "and scoring code — was deposited on the Open Science Framework before the first question was sent at 06:28 UTC. "
     "An analyst then checked the automated coding against every Bellwether and Stronghold mention, every direct "
     "question about Bellwether and every frame answer. The results below are what that locked procedure "
     "produced, including the two tests Bellwether did not pass."),
])

PATTERNS = ""

HYPOTHESIS_SCORING = [
    {"id": "P1", "headline": "Before any brand, the frame says vent",
     "proposition": "Before any brand is named, AI answers to “should my café roast in-house?” present venting as part of the job and do not raise a ventless option.",
     "verdict": "CONFIRMED", "qualifier": f"{_pc(VENT_L)} venting, {_pc(LESS_L)} ventless (2024–25 models)", "status_class": "positive"},
    {"id": "P2", "headline": "Name the barrier, and Bellwether appears",
     "proposition": "Bellwether is named far more often when a café states the venting, gas or air-quality barrier than when it asks generically.",
     "verdict": "CONFIRMED", "qualifier": f"{_pc(G_L)} generic, {_pc(C_L)} with the barrier stated", "status_class": "positive"},
    {"id": "P3", "headline": "On older models, the barrier answer goes to drums",
     "proposition": "When a café states the barrier, Bellwether is the most-named roaster in the answer.",
     "verdict": "FALSIFIED", "qualifier": f"seventh at {_pc(C_L)}; first at {_pc(C_S0)} on current assistants", "status_class": "negative"},
    {"id": "P4", "headline": "Search adds currency, not presence",
     "proposition": "Web search raises Bellwether's presence when current assistants recommend café roasters.",
     "verdict": "FALSIFIED", "qualifier": f"{_pc(S_S0)} without search, {_pc(S_S1)} with", "status_class": "negative"},
    {"id": "P5", "headline": "Older models guess; current ones know the Shop Roaster",
     "proposition": "Current assistants know Bellwether's Shop Roaster and older models do not; only search finds the October 2026 model.",
     "verdict": "DESCRIPTIVE", "qualifier": f"2026 model in {N26_S1} of 6 lineup answers with search, {N26_S0} without", "status_class": "neutral"},
    {"id": "P6", "headline": "Six makers on the show floor, five on the AI shelf",
     "proposition": "Presence on the trade-show floor and presence in AI answers diverge.",
     "verdict": "DESCRIPTIVE", "qualifier": f"Air-Motion named in 0 of {N_REC} answers", "status_class": "neutral"},
]

HYPOTHESIS_DETAILS = {
    "P1": "\n\n".join([
        (f"Asked “Should we start roasting our own coffee in-house?”, “What do I need to start roasting inside my "
         f"café?” and four similar questions, the six 2024–25 models describe a venting job in {F_REQ_L} of "
         f"{F_L['n']} answers: exhaust ducting to the outside, a hood, often an afterburner, sometimes a gas line, and the "
         f"permits to match. The other two do not mention venting at all. None of the 36 mentions that a roaster "
         f"exists that needs no external venting. For a brand whose proposition is the removal of that barrier, this is "
         f"the costliest part of the answer: it arrives before any brand is named, and it tells the café the barrier is real."),
        (f"The current assistants describe the same job, but no longer as the only option. Without search they raise a "
         f"ventless option in {LESS_S0} of {N_F_C} answers; with search, in {LESS_S1}. Every time a ventless option comes "
         f"with a brand name, Bellwether is that name: Claude and GPT name it on its own, while Gemini 4 Argon usually adds "
         f"Stronghold. Gemini 4 Argon raises the option in every frame answer; GPT-6 Astra does so only after searching."),
    ]),
    "P2": "\n\n".join([
        (f"On the fixed panel, Bellwether does not appear in any of 36 generic café recommendations — “What's the best "
         f"coffee roaster for a café?”, “Which roaster should I buy?” and four more. State the constraint — no gas line, "
         f"no ductwork, a lease that forbids roof vents, smoke, air-quality rules, an electric roaster — and it appears in "
         f"{K_C_L} of 36 answers. A gap of {CEP_PTS} points would arise by chance fewer than two times in a thousand "
         f"reshuffles of the same answers, and five of the six models show it on their own; Claude Opus 4.5 names "
         f"Bellwether in half of its constraint answers. GPT-4o-mini never names it in any recommendation."),
        (f"The current assistants show the same direction from a much higher base: {_pc(G_S0)} generic and {_pc(C_S0)} "
         f"constraint without search, {_pc(G_S1)} and {_pc(C_S1)} with it. This is what a defining entry point looks "
         f"like: the barrier Bellwether removes is the question that reliably retrieves it. On the older models it is "
         f"close to the only one."),
    ]),
    "P3": "\n\n".join([
        (f"Being retrieved is not the same as winning the answer. On the fixed panel, a café that cannot vent hears first "
         f"about Loring and Diedrich (each in {_pc(TOP_L[0][1])} of constraint answers), Probat ({_pc(TOP_L[2][1])}), the "
         f"Aillio Bullet ({_pc(TOP_L[3][1])}), Giesen ({_pc(TOP_L[4][1])}) and Mill City, and only then Bellwether "
         f"({_pc(C_L)}, seventh). Bellwether is named first in {FIRST_L} of {N_C_L} of those answers. The older models "
         f"answer the constraint with the industry's familiar drum makers. The pre-registered test was that Bellwether "
         f"would lead these answers; on the fixed panel it does not."),
        (f"On current assistants it does, and clearly. Without search Bellwether is in {_pc(C_S0)} of constraint answers "
         f"and named first in {FIRST_S0} of {N_C_S0}; Stronghold follows at "
         f"{_pc(_P['C|S0|C']['presence']['B06'])}, the Aillio Bullet at {_pc(_P['C|S0|C']['presence']['B02'])}. With "
         f"search, {_pc(C_S1)} and first in {FIRST_S1} of {N_C_S1}. Which answer a café owner meets depends on the model "
         f"behind the tool they use."),
    ]),
    "P4": "\n\n".join([
        (f"The retrieval test asked whether web search raises Bellwether's presence when current assistants recommend "
         f"café roasters. It does not: across 36 paired generic and constraint questions, Bellwether appears in "
         f"{_pc(S_S0)} of answers without search and {_pc(S_S1)} with it; {S_B} answers gain it and {S_C} lose it. "
         f"Claude Opus 5.5 accounts for the drop: with search it names Bellwether in one of its six generic "
         f"recommendations, against four of six without. Gemini 4 Argon names Bellwether in all 24 of its answers to "
         f"these questions, with or without search."),
        (f"Search changes what the answers know rather than whether Bellwether is in them. With search, all {N26_S1} "
         f"answers about Bellwether's newest machine and lineup name the Shop Roaster announced on 15 October 2026 — "
         f"the deep-bronze finish, Q1 2027 deliveries — and none of the six without search does. All three capacity "
         f"answers give the Shop Roaster's 1.5 kg batch; without search, none does. Bellwether's own site is the "
         f"most-cited source, in {CITE_BW} of {D7['n_s1']} search-enabled answers. And {N_UNIQ} answers repeat the "
         f"company's claim to be the only commercial ventless roaster, {N_UNIQ_FACT} of them as fact; one answer "
         f"disputes it."),
    ]),
    "P5": "\n\n".join([
        (f"Asked directly about Bellwether, the six older models know the brand but not the product. None names the "
         f"Shop Roaster, launched in March 2024, although four of them finished training after it. Five say they do not "
         f"know Bellwether's newest machine; the sixth, Gemini 2.5 Flash, names a “Series 3” that does not exist, and "
         f"Gemini 2.5 Flash-Lite calls the Series 1 — unsupported since January 2026 — Bellwether's flagship and the most "
         f"common choice for cafés. "
         f"Three of the six read the lineup question as one about coffee beans."),
        ("On the facts that decide a purchase, the older models are unreliable. Three of the six say the roaster needs "
         f"ventilation — one specifies a 6-inch duct to the outside, another says it burns natural gas or propane — and "
         f"none gives the Shop Roaster's batch size. The current assistants answer the ventilation question correctly in "
         f"all six answers, with or without search. Without search, two of the three lead with the 2.7 kg batch of the "
         f"older Series 2 and the third gives a 1–3 kg range; with search, all three give the Shop Roaster's 1.5 kg."),
    ]),
    "P6": "\n\n".join([
        (f"Six roaster makers exhibited at Coffee Fest Dallas-Fort Worth in October 2026: Bellwether, Aillio, Air-Motion "
         f"Roasters, Loring, Mill City Roasters and Stronghold. On the AI shelf they fare very differently. Loring and "
         f"Mill City are visible with every model generation (Loring in {_pc(SF['L|S0']['Loring'])} of recommendation "
         f"answers on the fixed panel, Mill City in {_pc(SF['L|S0']['Mill City Roasters'])}). Bellwether and Stronghold "
         f"are nearly absent from the older models ({_pc(SF['L|S0']['Bellwether'])} and {_pc(SF['L|S0']['Stronghold'])}) "
         f"and prominent on current ones ({_pc(SF['C|S0']['Bellwether'])} and {_pc(SF['C|S0']['Stronghold'])} without "
         f"search). The Aillio Bullet, a 1 kg machine, sits near 30% throughout. Air-Motion is named in none of the "
         f"{N_REC} recommendation answers."),
        (f"With search, Stronghold falls from {_pc(SF['C|S0']['Stronghold'])} to {_pc(SF['C|S1']['Stronghold'])} and "
         f"Bellwether from {_pc(SF['C|S0']['Bellwether'])} to {_pc(SF['C|S1']['Bellwether'])}; Diedrich, the most-named "
         f"brand outside the show floor, holds at {_pc(CR0['C|S1']['top_non_show_floor'][0][1])}. Physical presence at "
         f"the show and presence in AI answers are separate assets: a booth reaches the people in the hall, an answer "
         f"reaches everyone who asks."),
    ]),
}

CHART_MAP = {1: "frame", 2: "constraint", 3: "ranking", 4: "search", 5: "lineup", 6: "showfloor"}
SLOT_FILES = {
    "frame":      ("report_fig_01_frame.pdf",      "v39_frame"),
    "constraint": ("report_fig_02_constraint.pdf", "v39_constraint"),
    "ranking":    ("report_fig_03_ranking.pdf",    "v39_ranking"),
    "search":     ("report_fig_04_search.pdf",     "v39_search"),
    "lineup":     ("report_fig_05_lineup.pdf",     "v39_lineup"),
    "showfloor":  ("report_fig_06_showfloor.pdf",  "v39_showfloor"),
}


def _mediabox_in(fname):
    try:
        from pypdf import PdfReader
        b = PdfReader(str(_ROOT / "reports/figs/v39/report" / fname)).pages[0].mediabox
        return (round(float(b.width) / 72, 3), round(float(b.height) / 72, 3))
    except Exception:
        return (7.5, 5.0)


CHART_FIGSIZE_IN = {key: _mediabox_in(fname) for fname, key in SLOT_FILES.values()}

FIGURE_CAPTIONS = {
    "frame": (f"How answers to six “should my café roast in-house?” questions treat venting, as classified by an analyst. "
              f"The 2024–25 models present venting as part of the job in {F_REQ_L} of {F_L['n']} answers and never raise a "
              f"ventless option; current assistants raise one in {LESS_S0} of {N_F_C} answers without search and "
              f"{LESS_S1} of {N_F_C} with it, and the brand they name is Bellwether."),
    "constraint": ("Share of café roaster recommendations naming Bellwether, generic versus constraint-framed questions. On "
                   "the 2024–25 models Bellwether appears only when the café states the barrier; on current assistants it "
                   "appears in most answers either way."),
    "ranking": (f"Brands named in constraint-framed answers. The 2024–25 models answer a café that cannot vent with drum "
                f"makers and rank Bellwether seventh; current assistants without search name Bellwether in "
                f"{_pc(C_S0)} of those answers and first in {FIRST_S0} of {N_C_S0}."),
    "search": ("Top: Bellwether's share of café recommendations for each current assistant, without and with web search "
               "(12 paired questions each). Bottom: what the answers say about Bellwether. Search leaves the share flat and "
               "brings in the facts that changed after the models were trained."),
    "lineup": ("Four direct questions about Bellwether, answered by each model as read by an analyst. The 2024–25 models do "
               "not know the Shop Roaster, and three say it needs venting. Current assistants know it; with search they "
               "name the October 2026 model and its 1.5 kg batch."),
    "showfloor": (f"The six roaster makers that exhibited at Coffee Fest Dallas-Fort Worth 2026, by share of recommendation "
                  f"answers naming them. Loring and Mill City are visible on every panel; Bellwether and Stronghold only on "
                  f"current assistants; Air-Motion in none of {N_REC} answers."),
}

IMPLICATIONS = {
    "heading": "What this means for Bellwether",
    "intro": "Directional, and framed as levers to test rather than guarantees: this phase measured the AI layer, not the effect of changing it.",
    "paragraphs": [
        ("<b>Own the first paragraph of the frame answer.</b> The decisive moment comes before any brand is named: older "
         "models tell a café that roasting means ducts and permits, and current ones place the ventless option after the "
         "checklist. Content that answers “should my café roast in-house?” and “what does it take?” with the ventless "
         "route stated up front — what it removes, what it still needs (a 30 A circuit, room air conditioning), what "
         "installation costs — is the material that answer is assembled from."),
        ("<b>Keep the uniqueness claim exact.</b> Bellwether's position rests on being the roaster that needs no external "
         f"venting. Gemini 4 Argon describes Stronghold as ventless in {STRONG_VENTLESS} answers; search-enabled "
         f"Claude says, in {STRONG_NEEDS} answers, that Stronghold still requires an exhaust. Specific, sourced "
         "comparisons of what each competitor needs to install, model by model, protect the claim better than “the "
         "only” language, which answers repeat and one already disputes."),
        ("<b>Make the new Shop Roaster as findable as the old one.</b> With search, assistants already find the October "
         "2026 machine; without it, they describe the 2024 Shop Roaster or the Series 2's 2.7 kg batch. Model memories "
         "update slowly; pages that state current specifications, prices and delivery dates plainly, in one place, "
         "shorten the lag for every assistant that searches."),
        ("<b>Widen the entry points.</b> On older models Bellwether exists only behind its own entry point: name the "
         "constraint and it appears; ask generically and it does not. Generic café-roaster questions are where most "
         "buyers start. Comparisons and guides that place Bellwether in the general “best roaster for a café” "
         "conversation, on its merits as a café roaster rather than only as a ventless one, are the lever for that gap."),
        ("<b>Retire the old facts deliberately.</b> One older model calls the Series 1, unsupported since January 2026, "
         "Bellwether's flagship; three say the roaster needs venting. Support and resale pages that state "
         "plainly what is current, what is supported and what each machine needs remove the material those answers are "
         "built from."),
        ("<b>Measure again after first deliveries.</b> The same 30 questions run again in April–May 2027 on both panels. "
         "That re-run shows whether the new machine has entered the models' memories, whether the frame has moved, and "
         "whether any competitor has taken a share of the ventless answer."),
    ],
}

LIMITATIONS = "\n\n".join([
    ("This is one category in one market on one day. Each question was asked once, in English, without a location. The "
     "fixed panel runs at the most repeatable setting; the current assistants were asked at their providers' default "
     "settings, so their answers may vary more from run to run. The fixed panel is the program's 2024–25 reference "
     "generation, and the two panels bracket rather than represent what a given café owner sees."),
    (f"Gemini 2.5 Flash spends part of its answer budget on internal reasoning; {M5_CAP} of its 30 answers stopped at "
     f"the shared length cap, so its brand counts are a floor. Without it, the constraint gap is "
     f"{round(100 * D10['H_CEP']['delta'])} points (p = {D10['H_CEP']['p_one_sided']:.3f}) and Bellwether ranks "
     f"{['', 'first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth'][D10['H_CEPDefault']['rank']]}; "
     f"both readings hold. Gemini 4 Argon chose to search in 12 of its 30 search-enabled answers, so for that model the "
     f"search arm partly measures its own memory, and search results depend on the day's web."),
    ("Brand coding is automated. An analyst reviewed all 668 Bellwether and Stronghold mentions to rule out the common nouns "
     "“bellwether” and “stronghold” (none needed removal) and checked 132 further codes, of which 11 were corrected — "
     "none touching a test result. Claims about competitors' venting are reported as the models made them and are not "
     "verified against manufacturers' specifications. The registry holds 36 brands; unregistered commercial makers, "
     "led by Coffee Crafters, Typhoon and IMF, surfaced in the check."),
])

WHATS_NEXT = "\n\n".join([
    ("The same 30 questions run again in April–May 2027 on both panels, after Bellwether's first Q1 2027 deliveries; "
     "the second wave is pre-registered as an addendum before it runs. It answers three questions this phase cannot: "
     "whether the new Shop Roaster enters the models' memories without search, whether the venting frame keeps moving "
     "on current assistants, and whether a competitor takes a share of the ventless answer. Any fixed-panel model "
     "retired by then is reported as missing, not replaced."),
    ("For a brand team, that is the useful shape of AI-availability work: a baseline, a lever, and a re-measure. For "
     "the program, this phase adds two instruments — a frame audit that scores what a category's answers say before any "
     "brand appears, and a paired search arm that separates what models remember from what they find — which carry to "
     "any category whose leader sells the removal of a barrier."),
])

_SRC = {"S": "show floor", "A": "named in v0.38", "M": "equipment index", "D": "in-store claim"}
_RP = {c: _P[f"{c}|REC"]["presence"] for c in ("L|S0", "C|S0", "C|S1")}
LEADERBOARD = {
    "heading": "Appendix: the full category leaderboard",
    "intro": ("Share of recommendation answers naming each registry brand (generic café, constraint and production "
              "roastery questions: 108 answers on the 2024–25 panel, 54 per current-assistant condition)."),
    "columns": ["Brand", "Registry source", "2024–25 models", "Current, no search", "Current, with search"],
    "col_widths": [0.30, 0.22, 0.16, 0.16, 0.16],
    "rows": [[_NAMES[i], _SRC[_STRATUM[i]], _pc(_RP["L|S0"][i] or 0), _pc(_RP["C|S0"][i] or 0), _pc(_RP["C|S1"][i] or 0)]
             for i in sorted(_NAMES, key=lambda k: (-((_RP["C|S0"][k] or 0) + (_RP["C|S1"][k] or 0) + (_RP["L|S0"][k] or 0)), _NAMES[k]))
             if max(_RP[c][i] or 0 for c in _RP) > 0],
    "note": ("Not named in any recommendation answer: "
             + ", ".join(sorted(_NAMES[i] for i in _NAMES if not max(_RP[c][i] or 0 for c in _RP)))
             + ". Presence is the share of answers that name a brand at least once. Gemini 2.5 Flash answers were "
               "often truncated, so its contributions are a floor. Unregistered makers noticed in the audit: Coffee "
               "Crafters (Valenta), Typhoon, IMF, Bühler, Neuhaus Neotec and others."),
}

FOCAL_NAME = "Bellwether"

DISCLOSURE = ("Independent research by Third System, not a commissioned diagnostic. Third System has no commercial "
              "relationship with Bellwether Coffee or with any brand in the registry, and Bellwether did not commission, "
              "fund or review this study. The author met Bellwether staff at Coffee Fest Dallas-Fort Worth 2026 and "
              "receives Bellwether marketing email. He owns an Aillio Bullet R1; Aillio is a registry brand.")

CITATION = ("González Castro, P. U. (2026). <i>Bellwether Owns the No-Vent Answer — On the Newest AI Assistants: "
            "A Pre-Registered Focal-Brand Study of Commercial Coffee Roasters (AIAS™ v0.39)</i>. Third System. "
            "Pre-registration: osf.io/ec6wh (v39/prereg; tag v0.39-prereg-r1).")

CLOSING = {
    "byline_long": ["Pablo Ulpiano González Castro",
                    "School of Visual Arts, MPS Branding Program, New York, NY",
                    "Third System™ (research entity)"],
    "datasets": ["Pre-registration, registry and scoring code: osf.io/ec6wh/v39/ (deposited before acquisition)",
                 "Verdicts: v39/v39_verdicts.json · Audits: v39/data/v39_audit_commonnoun.json, v39_coder_audit.json",
                 "Responses and coding: v39/data/v39_raw.json, v39_coded.csv, v39_mentions.csv",
                 "Deviations log: v39/DEVIATIONS.md"],
    "methodology_log": "v0.39 (Presence protocol v1.2; SSRN paper in preparation)",
    "closing_text": ("The AI layer has caught up with Bellwether on the assistants people are adopting now, and not on the "
                     "models already built into many tools. The next gains are less about being found than about being "
                     "described exactly — and the program now has the instrument to watch both."),
}

RUNNING_HEAD = "AIAS™ Focal-Brand Study · v0.39 · November 2026"
PDF_TITLE = TITLE + " — AIAS v0.39"
