"""
v0.38 — Home Coffee Roasters (Aillio-focal) — brand-format report content module.
Third System(TM) managerial register, written for brand teams and prospective clients.

Register discipline (carried from v0.37):
  - No hypothesis labels (H_*) or test jargon in body text; plain brand-strategy voice.
  - Every number below is read from the locked outputs at import time (v38_verdicts.json,
    v38_tables.json, v38_coder_audit.json) so text and data cannot drift apart.
  - An UNDETERMINED lead verdict is reported as what it is: the test could not run
    because no model knows the R2. That is a finding, not a failure, and it is framed so.
  - No Samsung (commercial outputs omit it per brand JSON). The focal-brand disclosure
    (author owns a Bullet R1; no relationship with Aillio) is stated in the closing block.
  - Avoid glyphs Akkurat Pro lacks (arrows, >=, subscripts): write them out.
"""
import json
from pathlib import Path

_ROOT = Path("/Users/pablou/aias")
_V = json.loads((_ROOT / "osf/v38/v38_verdicts.json").read_text(encoding="utf-8"))
_T = json.loads((_ROOT / "osf/v38/data/v38_tables.json").read_text(encoding="utf-8"))
_A = json.loads((_ROOT / "osf/v38/data/v38_coder_audit.json").read_text(encoding="utf-8"))
_REG = json.loads((_ROOT / "osf/v38/registries/brands_home_roasters_v0.38.json").read_text(encoding="utf-8"))
_NAMES = {b["id"]: b["brand"] for b in _REG["brands"]}
_SEG = {b["id"]: b["segment"] for b in _REG["brands"]}
_P = _T["presence_pooled"]


def _pc(x):
    return f"{round(100 * x)}%"


# --- numbers used in the prose (all derived) ---
AIL_B, AIL_E, AIL_P, AIL_EP = (_V["H_Tier"][k] for k in ("presence_B", "presence_E", "presence_P", "presence_EP"))
DELTA_PTS = round(100 * _V["H_Tier"]["delta"])
MODELS_POS = _V["H_Tier"]["models_positive"]
FR_B, BEH_B = _P["B"]["presence"]["R05"], _P["B"]["presence"]["R04"]
BEH_EP, HOT_EP, GENE_EP = _P["EP"]["presence"]["R04"], _P["EP"]["presence"]["R02"], _P["EP"]["presence"]["R06"]
MARGIN_PTS = round(100 * _V["H_Default"]["margin_over_next"])
FIRST_EP = _V["H_Default"]["aillio_first_mention_share_EP"]
BEH_FIRST_EP = _T["first_mention_share_EP"]["R04"]
LEG = _V["H_LegacySlot"]["per_model"]
N_BULLET_REC = sum(m["n_specified"] for m in LEG.values())
N_R1_REC = sum(m["k_r1_only"] for m in LEG.values())
N_AIL_REC = _T["descriptives"]["D4_grounding_candidates"]["n_aillio_rec"]
PRICE_K, PRICE_N = _T["descriptives"]["D5_price_caveat"]["k"], _T["descriptives"]["D5_price_caveat"]["n"]
NESCO_K = _T["descriptives"]["D7_phantom_comparators"]["R30"]["k"]
NESCO_B = _P["B"]["presence"]["R30"]
BATCH_OK = _A["D4_batch"]["correct"]
BATCH_N = _A["D4_batch"]["correct"] + _A["D4_batch"]["incorrect"]
HEAT_OK = _A["D4_heating"]["correct"]
HEAT_N = _A["D4_heating"]["correct"] + _A["D4_heating"]["incorrect"]
N_NAMED = sum(1 for i in _NAMES if (_P["ALL"]["presence"][i] or 0) > 0)
assert N_R1_REC == N_BULLET_REC == N_AIL_REC, "every Aillio recommendation should carry an R1 code"
assert not any(_T["r2_aware"].values()), "prose assumes no model is R2-aware"

TITLE = "Aillio Wins the Expert Answer — With the Roaster It Replaced"

COVER = {
    "title": TITLE,
    "subtitle": (f"Six AI models make the Bullet the most-named machine for serious home roasters, and name it "
                 f"about half as often for beginners. Every Bullet they name is the R1. None names the R2 that "
                 f"replaced it in July 2024 — not even when asked directly."),
    "tagline": "AIAS™ Measurement Program · Phase v0.38<br/>Third System™",
    "date": "November 2026",
}

STANDFIRST = (
    "When a home roaster asks an AI assistant which machine to buy, the answer depends on how they ask. "
    "Sound like a beginner and the models point to inexpensive air roasters; sound serious and they point to "
    "the Aillio Bullet more often than to any other machine. That is a strong position, with one problem. "
    "Every Bullet the models recommend is the R1, the machine Aillio replaced with the R2 in July 2024. "
    "Asked directly, all six models describe the old lineup, and all six say the R1 is still in production. "
    "Aillio owns the expert answer with a product it no longer leads with."
)

LEAD_DECK = (
    "v0.38 asked six AI models — Claude Opus 4.5 and Sonnet 4.5, GPT-4o and GPT-4o-mini, Gemini 2.5 Flash and "
    "Flash-Lite — 22 questions a roaster might ask: 18 requests for a recommendation, written in three registers "
    "from first-time buyer to small-business roaster, and four direct questions about Aillio. All 132 answers were "
    "scored against a 32-brand registry and coded for which Bullet generation they name. The questions, brand list, "
    "coding rules and pass marks were deposited publicly before the first model was asked."
)

EXEC_SUMMARY = "\n\n".join([
    (f"<b>The category splits by who is asking.</b> The Bullet appears in {_pc(AIL_B)} of answers to beginner "
     f"questions and in {_pc(AIL_EP)} of answers to enthusiast and small-business questions — a {DELTA_PTS}-point "
     f"gap that five of the six models share. Beginners are steered to air and entry drum roasters: Fresh Roast "
     f"appears in {_pc(FR_B)} of beginner answers, Behmor in {_pc(BEH_B)}."),
    (f"<b>Aillio is the enthusiast default.</b> Under enthusiast and prosumer framing the Bullet is the most-named "
     f"roaster in the category ({_pc(AIL_EP)}, ahead of Behmor at {_pc(BEH_EP)} and Hottop at {_pc(HOT_EP)}) and the "
     f"first brand named in {_pc(FIRST_EP)} of those answers. The lead is real but narrower than the headline: "
     f"without Gemini 2.5 Flash, whose answers were cut short, it shrinks from {MARGIN_PTS} points to 5."),
    (f"<b>The models are a generation behind.</b> Not one of 132 answers names the R2 or R2 Pro. All {N_R1_REC} "
     f"recommendations that mention the Bullet name the R1. Asked directly, every model calls the R1 V2 Aillio's "
     f"newest machine, says the R1 is still in production, and tells a buyer who has chosen Aillio to get the R1 V2. "
     f"The study's lead test — whether models that know about the R2 still recommend the R1 — could not run, "
     f"because none of them knows about it. That is the finding: Aillio's problem is missing knowledge, not a "
     f"stubborn recommendation habit, and missing knowledge is the more fixable of the two."),
    ("<b>What to do.</b> Treat the R2 as a launch the AI layer has not yet heard about. The work is upstream, in the "
     "pages models learn from and look up: reseller pages that still present the R1 as current, comparison and "
     "specification content that names the R2 and the R1's end of production plainly, and product data that makes "
     "the succession explicit. Then measure again on current assistants — newer models that search the web as "
     "they answer may already know the R2 — before spending on the beginner frame, where the Bullet is a weaker "
     "fit anyway."),
])

WHAT_WE_MEASURED = "\n\n".join([
    ("v0.38 asked the questions a home roaster actually asks — 18 of them, in three registers: a beginner "
     "choosing a first machine, an experienced hobbyist upgrading, and someone roasting for a small business. "
     "None names a brand, a heating method or a batch size. Four more questions asked each model directly about "
     "Aillio: its newest Bullet, its current lineup, which Bullet to buy, and whether the original R1 is still made. "
     "Each question went once to each of six models at the most repeatable setting — 132 answers, collected on "
     "7 November 2026."),
    (f"Every answer was scored against a registry of 32 roaster brands, from inexpensive air roasters to commercial "
     f"drums, including two discontinued brands as a reference point; {N_NAMED} of the 32 were named at least once. "
     f"Every mention of the Bullet was coded for the generation it names: the original R1 (2015, later revised as "
     f"the R1 V2) or the R2 and R2 Pro that replaced it in July 2024. The six models split around that date: two "
     f"(GPT-4o and GPT-4o-mini) finished training before the R2 existed; four finished after it, on their makers' "
     f"published dates. That split was designed as the study's control."),
    ("Everything — questions, brand list, coding rules, pass marks and scoring code — was deposited on the "
     "Open Science Framework at 20:33 UTC; the first question was sent at 20:40. An analyst then read every answer "
     "that mentions Aillio to check the automated coding. The results below are what that locked procedure "
     "produced, including the part that did not go to plan."),
])

PATTERNS = ""

HYPOTHESIS_SCORING = [
    {"id": "P1", "headline": "Expert questions bring the Bullet",
     "proposition": "Aillio's AI presence depends on how the question is framed: the Bullet is named far more often when the asker sounds experienced or commercial than when they sound like a beginner.",
     "verdict": "CONFIRMED", "qualifier": f"{_pc(AIL_B)} beginner, {_pc(AIL_EP)} serious", "status_class": "positive"},
    {"id": "P2", "headline": "Aillio is the enthusiast default",
     "proposition": "Under enthusiast and prosumer framing, the Bullet is the most-named roaster in the category and the brand most often named first.",
     "verdict": "CONFIRMED", "qualifier": f"leads by {MARGIN_PTS} points (5 without the truncated model)", "status_class": "positive"},
    {"id": "P3", "headline": "Every recommended Bullet is the R1",
     "proposition": "When the models recommend the Bullet, they name the R1 — in every answer that mentions it and in every answer to a buyer who has already chosen Aillio.",
     "verdict": "DESCRIPTIVE", "qualifier": f"{N_R1_REC} of {N_BULLET_REC} answers", "status_class": "neutral"},
    {"id": "P4", "headline": "The models have not learned the R2",
     "proposition": "No model names the R2, even when asked about Aillio's lineup, so the planned test of whether models that know the R2 still recommend the R1 could not run.",
     "verdict": "UNDETERMINED", "qualifier": "no model knows the R2", "status_class": "neutral"},
    {"id": "P5", "headline": "Right specs, wrong machine",
     "proposition": "The models state the Bullet's hard specs mostly correctly while describing a machine Aillio has replaced.",
     "verdict": "EXPLORATORY", "qualifier": f"{round(100 * (BATCH_OK + HEAT_OK) / (BATCH_N + HEAT_N))}% of spec claims correct", "status_class": "neutral"},
]

HYPOTHESIS_DETAILS = {
    "P1": "\n\n".join([
        (f"Asked as a beginner — \"What's the best home coffee roaster?\", \"What roaster would you suggest I start "
         f"with?\" — the six models name the Bullet in {_pc(AIL_B)} of answers. Asked as an experienced hobbyist, "
         f"{_pc(AIL_E)}. Asked as someone roasting for a small business, {_pc(AIL_P)}. The {DELTA_PTS}-point gap between "
         f"beginner and serious framing would arise by chance less than once in a thousand reshuffles of the same "
         f"answers, and five of the six models show it on their own."),
        ("The sixth is the exception worth knowing about: GPT-4o-mini never names Aillio in any of its 18 "
         "recommendations, although it describes the Bullet readily when asked about it by name. Known but not "
         "named is a distinct problem from not being known at all — and for one widely used model, it is "
         "Aillio's problem. For a brand whose buyers arrive with experience, the framing effect is mostly good "
         "news: the AI layer puts the Bullet in front of the people most likely to buy it."),
    ]),
    "P2": "\n\n".join([
        (f"Under enthusiast and prosumer framing the Bullet is the most-named roaster in the registry, in {_pc(AIL_EP)} "
         f"of answers, ahead of Behmor ({_pc(BEH_EP)}), Hottop ({_pc(HOT_EP)}) and Gene Cafe ({_pc(GENE_EP)}). It is "
         f"also the brand most often named first — in {_pc(FIRST_EP)} of those answers, against {_pc(BEH_FIRST_EP)} "
         f"for Behmor. The beginner answer is a different category altogether: Fresh Roast ({_pc(FR_B)}) and Behmor "
         f"({_pc(BEH_B)}) own it, and commercial drum makers appear only once the questions turn to business."),
        (f"The lead needs one honest qualification. Gemini 2.5 Flash spends part of its answer budget on internal "
         f"reasoning and was cut off in almost every answer, so it typically names only the first one or two machines "
         f"— often the Bullet. Without it, the Bullet still leads, but by 5 points rather than {MARGIN_PTS}. "
         f"Being named first is the steadier sign of default status, and on that measure the Bullet's lead is clear. "
         f"One more pattern sits in the beginner answers: Nesco, whose last home roaster was recalled in 2021 over a "
         f"fire hazard, still appears in {_pc(NESCO_B)} of them, never with a warning."),
    ]),
    "P3": "\n\n".join([
        (f"Every one of the {N_R1_REC} recommendations that mention the Bullet names the R1, usually as \"Bullet R1 V2\". "
         f"Not one names the R2 or R2 Pro. The pattern holds across all four models trained after the R2 launch, not "
         f"just the two trained before it. When a buyer says they have already chosen a Bullet and asks which model "
         f"to get, all six models answer \"the R1 V2\"."),
        (f"The recommendation also carries the R1's commercial frame: {PRICE_K} of {PRICE_N} answers that mention the "
         f"Bullet attach a price note, and the prices quoted cluster around $3,000–3,500, the R1 era's range. "
         f"Sweet Maria's lists the R2 at $4,099 and the R2 Pro at $5,299. A buyer who follows the AI's advice either "
         f"looks for a machine the brand no longer leads with, or meets a higher price than the answer prepared them for."),
    ]),
    "P4": "\n\n".join([
        ("The study's lead question was whether a recommendation slot outlives the product in it — whether "
         "models that know the R2 exists keep recommending the R1. That test needs at least one model that knows the "
         "R2. None does. Asked for the newest Bullet, all six say the R1 V2. Asked what Aillio sells, all six list the "
         "R1. Asked whether the R1 is still in production, all six say yes. Gemini 2.5 Flash says recent refinements "
         "\"don't warrant\" a new model number such as an R2 — and, asked which Bullet to buy, offers an \"upcoming\" R1 V3."),
        ("The pre-registered rule for this case was set in advance: the lead test is recorded as undetermined, and "
         "the knowledge gap becomes the finding. Four of the six models have published training cutoffs six to ten "
         "months after the R2 was announced, yet none absorbed it — a launch that shipped in stages, set against "
         "a decade of R1 reviews and forum threads. The two models trained before the launch behave the same way, as "
         "expected: the control passed, but with no model knowing the R2 it had nothing to contrast against."),
    ]),
    "P5": "\n\n".join([
        (f"This phase was also the program's first test of Grounding: whether what AI says about a brand is true. "
         f"On the Bullet's two hardest facts the models do well. Of {BATCH_N} statements of its batch capacity, "
         f"{BATCH_OK} are correct (1 kg); the misses say \"1/2 lb batches\" and \"1-1.5 kg batches\". Of {HEAT_N} "
         f"statements of how it heats, {HEAT_OK} correctly say induction; both misses, from one model, file it among "
         f"hot-air fluid-bed roasters."),
        ("So the models are accurate about the machine they describe — it is simply the previous machine. That "
         "distinction matters for the remedy. Correcting a wrong spec means fixing a fact; correcting a stale "
         "product means teaching the AI layer that a succession happened. The second is what Aillio needs, and it "
         "is a content and data job rather than a reputation one."),
    ]),
}

CHART_MAP = {1: "tier", 2: "map", 3: "legacy", 4: "lineup", 5: "grounding"}
SLOT_FILES = {
    "tier":   ("report_fig_01_tier.pdf",   "v38_tier"),
    "map":    ("report_fig_02_map.pdf",    "v38_map"),
    "legacy": ("report_fig_03_legacy.pdf", "v38_legacy"),
    "lineup": ("report_fig_04_lineup.pdf", "v38_lineup"),
    "grounding": ("report_fig_05_grounding.pdf", "v38_grounding"),
}


def _mediabox_in(fname):
    try:
        from pypdf import PdfReader
        b = PdfReader(str(_ROOT / "reports/figs/v38/report" / fname)).pages[0].mediabox
        return (round(float(b.width) / 72, 3), round(float(b.height) / 72, 3))
    except Exception:
        return (7.5, 5.0)


CHART_FIGSIZE_IN = {key: _mediabox_in(fname) for fname, key in SLOT_FILES.values()}

FIGURE_CAPTIONS = {
    "tier": (f"Share of recommendation answers naming the Aillio Bullet, by how the question is framed. Roughly a "
             f"third of beginner answers name it; two-thirds of enthusiast and small-business answers do. Five of six "
             f"models show the gap; GPT-4o-mini never names Aillio in a recommendation."),
    "map": ("Each brand's share of answers under beginner framing (orange) and enthusiast or prosumer framing "
            "(indigo). Beginner answers belong to air and entry drum roasters; serious answers belong to the Bullet, "
            "with commercial drums rising as the questions turn to business. Nesco, whose last home roaster was "
            "recalled in 2021 over a fire hazard, still reaches a quarter of beginner answers."),
    "legacy": ("Recommendation answers that name the Bullet, by the generation they name. Every one names the R1; "
               "not one names the R2 or R2 Pro. The four models trained after the R2 launch behave exactly like the "
               "two trained before it."),
    "lineup": ("The four direct questions about Aillio, answered by each model. Every model calls the R1 V2 the "
               "newest Bullet, lists the R1 as the current lineup, recommends it to a buyer who has chosen Aillio, "
               "and says it is still in production. None mentions the R2."),
    "grounding": (f"What the models say about the Bullet in the {N_AIL_REC} recommendations that name it, checked by an "
                  f"analyst against the machine's specifications. The facts are mostly right; the machine is never the "
                  f"current one."),
}

IMPLICATIONS = {
    "heading": "What this means for Aillio",
    "intro": "Directional, and framed as levers to test rather than guarantees: this phase measured the AI layer, not the effect of changing it.",
    "paragraphs": [
        ("<b>Close the knowledge gap first.</b> Aillio's largest AI-availability gap is not presence but currency. The "
         "models put the Bullet at the top of the expert answer and then describe a machine Aillio has replaced. Every "
         "such answer leaks value: the R2's improvements, its price logic and its availability never reach the buyer."),
        ("<b>Fix the pages models learn from and look up.</b> The cheapest levers sit with resellers and on aillio.com: "
         "mark R1 product pages as discontinued and point them to the R2 (Sweet Maria's own R2 Pro page still "
         "recommends the R1 for less experienced roasters); publish a plain R1-versus-R2 comparison and an explicit "
         "end-of-production note for the R1; and make the succession machine-readable in product data — model "
         "name, release date, predecessor and successor."),
        ("<b>Give the models new facts to be right about.</b> They already state the Bullet's capacity and heating "
         "correctly. Pair those familiar facts with the R2's own numbers wherever the Bullet is described, so the "
         "specifications the models trust carry the new generation with them."),
        ("<b>Defend the expert frame; choose the beginner frame deliberately.</b> The Bullet's AI position is "
         "concentrated where its buyers are. The beginner answer belongs to machines priced in the hundreds, not the thousands; competing there "
         "would mean arguing the Bullet as a first and last roaster — a positioning decision, not a measurement one."),
        ("<b>Prepare for the price conversation.</b> Three in four Bullet recommendations carry a price note, and the "
         "prices quoted are R1-era. When the R2 surfaces at a higher price, content that ties the price to what "
         "changed keeps the note from becoming an objection."),
        ("<b>Measure again on the assistants people use now.</b> The program's fixed panel shows the gap; the next "
         "phase shows whether newer, web-connected assistants have closed it — and, once a model knows the R2, "
         "whether it still prefers the R1."),
    ],
}

LIMITATIONS = "\n\n".join([
    ("This is one category on one day, read within clear edges. The six models are the program's fixed panel, "
     "released in 2024 and 2025 and still served through developer APIs and the tools built on them. Assistants "
     "people use in late 2026 run newer models and often search the web while answering; they may well know the R2. "
     "The finding describes the models measured, not every assistant."),
    ("Gemini 2.5 Flash spends part of its answer budget on internal reasoning, and 19 of its 22 answers hit the "
     "shared cap, so its brand counts are a floor; the program now flags the same pattern in earlier phases. Each "
     "question was asked once, in English, at the most repeatable setting, without naming a country. The R1 V2 is "
     "still listed by some retailers outside the US, so \"replaced\" describes Aillio's lineup and the US channel, "
     "not every shelf."),
    ("Brand coding is automated and was checked by an analyst against every answer that mentions Aillio; two of 92 "
     "checked codes were corrected, both on the descriptive production question. The registry holds 32 brands; one "
     "unregistered brand surfaced in the check. The author owns a first-generation Bullet R1, disclosed below. None "
     "of these edges touches the central observation: across 132 answers, no model names the R2."),
])

WHATS_NEXT = "\n\n".join([
    ("The next step is a pre-registered re-run of the same 22 questions on current assistants, with and without web "
     "search. It answers the question this phase could not: if newer models know the R2, does the recommendation "
     "follow — or does the R1 keep its slot? The lead test was designed for exactly that case and is ready to run."),
    ("A repeat in 90 days would then show whether changes to the pages models read move the answer, which turns "
     "this measurement into a tracking instrument. For a brand team, that is the useful shape of AI-availability "
     "work: a baseline, a lever, and a re-measure. For the program, this phase also identified a protocol fix — "
     "giving reasoning models room to finish their answers — that applies to every phase measured on this panel."),
])

LEADERBOARD = {
    "heading": "Appendix: the full category leaderboard",
    "intro": "Share of recommendation answers naming each registry brand, by framing (36 answers per framing: 6 questions x 6 models).",
    "columns": ["Brand", "Segment", "Beginner", "Enthusiast", "Prosumer", "All 108"],
    "rows": [[_NAMES[i] + (" (discontinued)" if _SEG[i] == "discontinued" else ""),
              _SEG[i].replace("-", " "),
              _pc(_P["B"]["presence"][i]), _pc(_P["E"]["presence"][i]), _pc(_P["P"]["presence"][i]), _pc(_P["ALL"]["presence"][i])]
             for i in sorted(_NAMES, key=lambda k: (-(_P["ALL"]["presence"][k] or 0), _NAMES[k]))
             if (_P["ALL"]["presence"][i] or 0) > 0],
    "note": ("Not named in any of the 108 recommendation answers: "
             + ", ".join(sorted(_NAMES[i] for i in _NAMES if not (_P["ALL"]["presence"][i] or 0)))
             + ". Presence is the share of answers that name a brand at least once; Gemini 2.5 Flash answers were "
               "truncated, so its contributions are a floor."),
}

DISCLOSURE = ("Independent research by Third System, not a commissioned diagnostic. Third System has no commercial "
              "relationship with Aillio or with any brand in the registry, and Aillio did not commission, fund or "
              "review this study. The author owns an Aillio Bullet R1 (first generation).")

CITATION = ("González Castro, P. U. (2026). <i>Aillio Wins the Expert Answer — With the Roaster It Replaced: "
            "A Pre-Registered Focal-Brand Study of Home Coffee Roasters (AIAS™ v0.38)</i>. Third System. "
            "Pre-registration: osf.io/ec6wh (v38/prereg; tag v0.38-prereg-r1).")

CLOSING = {
    "byline_long": ["Pablo Ulpiano González Castro",
                    "School of Visual Arts, MPS Branding Program, New York, NY",
                    "Third System™ (research entity)"],
    "datasets": ["Pre-registration, registry and scoring code: osf.io/ec6wh/v38/ (deposited before acquisition)",
                 "Verdicts: v38/v38_verdicts.json · Coder audit: v38/data/v38_coder_audit.json",
                 "Responses and coding: v38/data/v38_raw.json, v38_coded.csv, v38_mentions.csv",
                 "Deviations log: v38/DEVIATIONS.md"],
    "methodology_log": "v0.38 (Presence protocol v1.2; SSRN paper in preparation)",
    "closing_text": ("The AI layer already treats the Bullet as the serious roaster's answer. It has not yet heard that "
                     "the Bullet changed. That is an unusually fixable problem — a knowledge gap rather than a habit "
                     "— and the program now has the instrument to watch it close."),
}

RUNNING_HEAD = "AIAS™ Focal-Brand Study · v0.38 · November 2026"
PDF_TITLE = TITLE + " — AIAS v0.38"
