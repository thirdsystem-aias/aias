"""
AIAS v0.24 — B2B SaaS Pre-Registration Content
Locked at v0.24-prereg-r1
Methodology: v1.6

8th substrate family. Primary hypothesis: Discourse-Language carryforward
on high-marketing-language substrate.
"""

# ── Registry ────────────────────────────────────────────────────────────

REGISTRY = {
    # Cell A — Enterprise Incumbents (7)
    "A1": {"brand": "Salesforce",   "cell": "A", "label": "Enterprise Incumbents"},
    "A2": {"brand": "HubSpot",     "cell": "A", "label": "Enterprise Incumbents"},
    "A3": {"brand": "ServiceNow",  "cell": "A", "label": "Enterprise Incumbents"},
    "A4": {"brand": "Workday",     "cell": "A", "label": "Enterprise Incumbents"},
    "A5": {"brand": "SAP",         "cell": "A", "label": "Enterprise Incumbents"},
    "A6": {"brand": "Oracle",      "cell": "A", "label": "Enterprise Incumbents"},
    "A7": {"brand": "Zendesk",     "cell": "A", "label": "Enterprise Incumbents"},

    # Cell B — High-Identity Challengers (6)
    "B1": {"brand": "Notion",      "cell": "B", "label": "High-Identity Challengers"},
    "B2": {"brand": "Figma",       "cell": "B", "label": "High-Identity Challengers"},
    "B3": {"brand": "Linear",      "cell": "B", "label": "High-Identity Challengers"},
    "B4": {"brand": "Airtable",    "cell": "B", "label": "High-Identity Challengers"},
    "B5": {"brand": "Slack",       "cell": "B", "label": "High-Identity Challengers"},
    "B6": {"brand": "Miro",        "cell": "B", "label": "High-Identity Challengers"},

    # Cell C — Infrastructure / Developer Platform (6)
    "C1": {"brand": "Datadog",     "cell": "C", "label": "Infrastructure / Developer Platform"},
    "C2": {"brand": "Snowflake",   "cell": "C", "label": "Infrastructure / Developer Platform"},
    "C3": {"brand": "Stripe",      "cell": "C", "label": "Infrastructure / Developer Platform"},
    "C4": {"brand": "Twilio",      "cell": "C", "label": "Infrastructure / Developer Platform"},
    "C5": {"brand": "Cloudflare",  "cell": "C", "label": "Infrastructure / Developer Platform"},
    "C6": {"brand": "MongoDB",     "cell": "C", "label": "Infrastructure / Developer Platform"},

    # Cell D — Phantom Candidates (5)
    "D1": {"brand": "Quip",        "cell": "D", "label": "Phantom Candidates",
            "status": "Acquired by Salesforce 2016; absorbed, no standalone product"},
    "D2": {"brand": "Yammer",      "cell": "D", "label": "Phantom Candidates",
            "status": "Acquired by Microsoft 2012; rebranded Viva Engage 2023; brand name dead"},
    "D3": {"brand": "Wunderlist",  "cell": "D", "label": "Phantom Candidates",
            "status": "Acquired by Microsoft; shut down June 2020; replaced by To Do"},
    "D4": {"brand": "HipChat",    "cell": "D", "label": "Phantom Candidates",
            "status": "Atlassian; shut down Feb 2019; replaced by Stride"},
    "D5": {"brand": "Stride",     "cell": "D", "label": "Phantom Candidates",
            "status": "Atlassian HipChat replacement; shut down Feb 2019; double extinction"},
}

PANEL_SIZE = 24
CELL_COUNTS = {"A": 7, "B": 6, "C": 6, "D": 5}

# Cross-cell flag
CROSS_CELL_NOTE = (
    "Slack (B5) is a Salesforce (A1) subsidiary. Maintained as separate entries "
    "because Slack operates as a distinct brand identity. Parent-subsidiary "
    "relationship is analytically noted, not a confound at Recognition/Recall level."
)

# ── Model Panel (fixed from v0.17) ──────────────────────────────────────

MODEL_PANEL = [
    "Claude Opus 4.5",
    "Claude Sonnet 4.5",
    "GPT-4o",
    "GPT-4o-mini",
    "Gemini 2.5 Flash",
    "Gemini 2.5 Flash Lite",
]

# ── Marketing-Language Token (MLT) Dictionary ──────────────────────────
# Locked at pre-reg. No tokens added post-acquisition.

MLT_DICTIONARY = {
    "Salesforce":   ["Customer 360", "Trailblazer", "Einstein", "Ohana"],
    "HubSpot":      ["inbound marketing", "flywheel", "growth stack"],
    "ServiceNow":   ["Now Platform", "workflow automation"],
    "Snowflake":    ["Data Cloud", "data sharing economy"],
    "Notion":       ["all-in-one workspace", "connected workspace"],
    "Figma":        ["design in the browser", "multiplayer design"],
    "Airtable":     ["no-code", "spreadsheet-database"],
    "Linear":       ["issue tracking for modern teams"],
}

# ── Hypotheses ──────────────────────────────────────────────────────────

HYPOTHESES = {

    "H_Discourse_Language_SaaS": {
        "type": "primary",
        "statement": (
            "On the B2B SaaS substrate, LLM recall outputs exhibit elevated rates "
            "of marketing-originated category terminology (vendor-coined terms, "
            "positioning language, category-creation rhetoric) relative to the "
            "program's cumulative cross-substrate baseline."
        ),
        "operationalization": (
            "Code Phase B recall outputs for marketing-language tokens (MLTs) "
            "against the locked MLT_DICTIONARY. Compute Marketing-Language "
            "Coverage (MLC) as proportion of recall outputs containing >= 1 MLT. "
            "Compare MLC_SaaS to cumulative MLC across prior substrates (v0.16-v0.22)."
        ),
        "prediction": "MLC_SaaS > MLC_baseline",
        "falsification": (
            "MLC_SaaS <= MLC_baseline (SaaS shows no elevated marketing-language signal)"
        ),
        "confidence": "High",
    },

    "H_Regime4_saas": {
        "type": "standard_battery",
        "statement": (
            "The B2B SaaS substrate classifies into one of the four canonical "
            "regimes per the v1.2 taxonomy."
        ),
        "operationalization": (
            "C1 (panel adequacy >= 12 responding brands), "
            "C2 (distinct C_P >= 3 AND modal share <= 0.625 per v1.5), "
            "C3 (regime-specific distributional thresholds)."
        ),
        "prediction": "Regime 1 or 2 (uniform or near-uniform saturation)",
        "falsification": (
            "C1 fails (panel inadequacy, n < 12) => indeterminate per v0.17 precedent"
        ),
        "confidence": "Medium",
    },

    "H_Dissoc_substrate_generalization": {
        "type": "standard_battery",
        "statement": (
            "Recognition x Recall dissociation (Iwachu pattern) generalizes "
            "to the 8th substrate family."
        ),
        "operationalization": (
            "Per v1.4 multi-component construct. Brand exhibits dissociation "
            "when Recognition score (C_P) and Recall rate diverge by >= 2 cells "
            "in ordinal ranking. Count qualifying Iwachu cases; add to cumulative total."
        ),
        "prediction": ">= 2 new Iwachu cases; Cell C infrastructure brands most likely source",
        "falsification": "Zero Iwachu cases across all 24 brands",
        "confidence": "Medium",
    },

    "H_IL_direct": {
        "type": "standard_battery",
        "statement": (
            "Identity Load moderates AI Presence, with Cell B (high-identity "
            "challengers) exhibiting higher R_cult-lead ratio than Cell A "
            "(enterprise incumbents)."
        ),
        "operationalization": (
            "v1.6 R4-independent bootstrap. Compute R_cult-lead per cell; "
            "compare Cell A mean vs Cell B mean."
        ),
        "prediction": "Cell B R_cult-lead > Cell A R_cult-lead",
        "falsification": "Cell A R_cult-lead >= Cell B R_cult-lead",
        "confidence": "High",
    },

    "H_SubstrateRecognition": {
        "type": "standard_battery",
        "statement": (
            "The B2B SaaS substrate exhibits uniform vs differential Recognition "
            "saturation across the six-model panel."
        ),
        "operationalization": (
            "v1.6 Inc1 substrate pre-screen. Uniform = all main-cell brands "
            "achieve C_P = 6/6. Differential = variance in C_P across brands."
        ),
        "prediction": (
            "Uniform saturation for Cells A + C; possibly differential for Cell B "
            "(Linear, Miro may fail recognition on weaker models)"
        ),
        "falsification": "N/A — descriptive classification, not directional hypothesis",
        "confidence": "Medium-high",
    },

    "H_Phantom_SaaS": {
        "type": "standard_battery",
        "statement": (
            "Defunct or absorbed B2B SaaS brands (Cell D) exhibit Phantom Brand "
            "Persistence — non-zero recall rates despite brand death."
        ),
        "operationalization": (
            "Per v1.6 Inc3. Compute R_phantom for each Cell D brand. "
            "R_phantom > 0 = phantom persistence."
        ),
        "prediction": (
            ">= 3/5 Cell D brands show R_phantom > 0. Counter-prediction to "
            "v0.22 automotive (all 5 defunct brands R_phantom = 0). B2B SaaS "
            "phantoms expected to persist at higher rates due to long-tail tech "
            "content (blog posts, Stack Overflow, comparison articles, tutorials, "
            "migration guides) referencing defunct tools years after shutdown."
        ),
        "falsification": (
            "R_phantom = 0 for all 5 Cell D brands (replicates v0.22 null finding; "
            "would suggest Phantom Brand Persistence is domain-invariant)"
        ),
        "confidence": "Medium",
    },
}

# ── Methodology Lock ────────────────────────────────────────────────────

METHODOLOGY_VERSION = "v1.6"
METHODOLOGY_SSRN_IDS = [6761698, 6797679, 6799479, 6810758, 6816340]

# New for v0.24: MLC is a coded metric applied to Phase B outputs.
# Not a new construct (Discourse-Language carryforward observed in v0.16),
# but the first quantified operationalization. Runs under v1.6 — no
# methodology increment required.

# ── Deviations ──────────────────────────────────────────────────────────

DEVIATIONS = {}
# Entry 0 reserved for pre-acquisition methodology amendments (r1 -> r2).
# Empty at r1 lock.
