"""
v0.40 — US airlines and retail banks — brand-format report content module (skeleton).
Third System(TM) managerial register.

Scaffolded by aias_new_phase.py from the v0.39 module; every v0.39 value was removed on 2026-11-08.
Each attribute keeps the shape build_report_v40.py reads. Text is written after scoring, from the
locked v0.40 outputs only. Kickoff rules: no focal brand, no lessons addressed to a brand, and no
Samsung in commercial outputs (COI goes in the paper's Declarations section only).
"""

TBD = "TBD (v0.40)"

TITLE = TBD
PDF_TITLE = TBD
RUNNING_HEAD = TBD
CITATION = TBD
COVER = {"title": TBD, "subtitle": TBD, "tagline": TBD, "date": TBD}
STANDFIRST = TBD
LEAD_DECK = TBD
EXEC_SUMMARY = TBD
WHAT_WE_MEASURED = TBD
PATTERNS = ""
HYPOTHESIS_SCORING = []   # one dict per proposition: id, headline, proposition, verdict, qualifier, status_class
HYPOTHESIS_DETAILS = {}   # proposition id -> paragraph
IMPLICATIONS = {"heading": TBD, "intro": TBD, "paragraphs": []}  # for marketers in any category, never addressed to a brand
LIMITATIONS = TBD
WHATS_NEXT = TBD
LEADERBOARD = {"heading": TBD, "intro": TBD, "columns": [], "col_widths": [], "rows": [], "note": TBD}
CLOSING = {"byline_long": [], "datasets": [], "methodology_log": TBD, "closing_text": TBD}
DISCLOSURE = TBD          # independence statement
FOCAL_NAME = None         # v0.40 has no focal brand
CHART_MAP = {}            # figure number -> slot key, set when the figures are defined
SLOT_FILES = {}           # slot key -> (chart PDF file name, figsize key)
CHART_FIGSIZE_IN = {}     # figsize key -> (width, height) in inches, read from the chart PDFs
FIGURE_CAPTIONS = {}      # slot key -> caption
