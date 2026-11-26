#!/usr/bin/env python3
"""
tokens_aias3.py -- the token map for the AIAS 3.0 (Coverage) release drafts: paper template, Third System report
content and website study page. DRAFT, pre-data (branch aias-3.0-draft, Nov 26, 2026). Nothing public.

Two kinds of token, one syntax for all three documents:

  {{L:KEY}}  a value that exists today in a locked or published record. Resolved by sources_aias3.py from the cited
             file at the cited commit (git show COMMIT:PATH). Never typed by hand.
  {{P:KEY}}  a value that depends on an input that does not exist yet. Every KEY is in PENDING below, which names
             the future input that fills it (INPUTS), where in that input it is read, and the step that writes it.
             A final build reads the values file written at the release data lock and refuses any {{P:KEY}} it
             cannot fill and any token left in its output.

A content dict with "requires": [FLAG, ...] is kept only when every FLAG (or "!FLAG" negated) holds in the values
file's "flags"; in a draft build every item is kept and marked.

  python3 papers/aias_3_0/tokens_aias3.py                 # table: token -> input -> source -> earliest date
  python3 papers/aias_3_0/tokens_aias3.py --inputs        # the future inputs and their dates
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import sources_aias3 as S  # noqa: E402

TOKEN = re.compile(r"\{\{([LP]):([A-Za-z0-9_.]+)\}\}")
ANY_TEMPLATE = re.compile(r"\{\{|\{%")
VALUES_DEFAULT = ROOT / "osf" / "aias_3_0" / "outputs" / "aias_3_0_values.json"   # written at the data lock

# ---------------------------------------------------------------------------------------------------------------
# The future inputs. "earliest" is the earliest date the input can exist, with the reason; "prereg" says whether a
# locked pre-registration already defines it; "pablo" says what needs Pablo's go before it can exist.
# Dates come from locked or dated records (cited), never from a guess; where a date depends on a decision not yet
# taken, it says so.
INPUTS = {
    "I0_release_prereg": {
        "what": "AIAS 3.0 release pre-registration: outline with outcome-contingent headline wording (as the AIAS 2.0 "
                "outline, tag aias-2-0-outline-locked), the calibration and dissociation analyses with their rules, "
                "seeds and scorer, and the panel/score-set decision",
        "file": "osf/aias_3_0/prereg/PRE_REGISTRATION_aias_3_0.md; tag aias-3-0-prereg-r1; anchor osf/aias_3_0/anchor/",
        "step": "draft -> Pablo -> lock 24 h after he receives it (CLAUDE.md operating mode) -> OSF ec6wh aias_3_0/prereg "
                "(a December lock still deposits to ec6wh; from January new pre-registrations go to OSF Registries)",
        "prereg": "NOT DRAFTED",
        "pablo": "new pre-registration (his go on scope: panel N3 vs AIAS 2.0 legacy set, whether a Coverage retest "
                 "wave is part of it, how the predictive leg is reported)",
        "earliest": "lock about 24 h after he receives the draft; it must lock before the AIAS 6.0 Preview scoring "
                    "run (data lock Fri 2026-12-11) if the release reads the Preview's Coverage tests blind",
    },
    "I1_calibration": {
        "what": "Two -> three-score calibration (the N -> N+1 step, as v1.9 did for two scores): Cov* scale and "
                "rating rule kept or changed, candidate combined scores against the no-composite rules, share of "
                "brands rated, and the bridge to the AIAS 2.0 score set",
        "file": "osf/aias_3_0/outputs/aias_3_0_calibration.json (score_aias_3_0.py --calibration, once)",
        "step": "re-analysis after I0's lock; reads v0.42 (t4) brand table, v1.12 unit table, AIAS 2.0 profiles",
        "prereg": "NOT PRE-REGISTERED (to be fixed in I0)",
        "pablo": "inside I0",
        "earliest": "same day as I0's lock (all inputs exist: v0.42 31c64c6, v1.12 949be61, aias-2-0-data-locked); "
                    "after I5 if the apostrophe correction is applied first",
    },
    "I2_dissociation": {
        "what": "Three-score dissociation study: Presence, Consistency and Coverage on the same brands, models and "
                "week, pairwise and each against the other two together",
        "file": "osf/aias_3_0/outputs/aias_3_0_dissociation.json (score_aias_3_0.py --dissociation, once)",
        "step": "after I0's lock; if I0 adopts the Preview's locked Coverage tests as its confirmatory reading, after "
                "I3",
        "prereg": "NOT PRE-REGISTERED (to be fixed in I0); the AIAS 6.0 Preview (tag aias-6-0-preview-prereg-r1) "
                  "already locks the pairwise and all-earlier-parts tests that include Coverage, on t4",
        "pablo": "inside I0",
        "earliest": "same day as I0's lock on t4 data alone; Fri 2026-12-11 if it reads the Preview's outputs",
    },
    "I3_preview_outputs": {
        "what": "AIAS 6.0 Preview scorer outputs (results/gates/inputs JSON), with the Coverage pairs and its "
                "all-earlier-parts test",
        "file": "osf/aias_6_0_preview/outputs/results_aias_6_0_preview.json",
        "step": "score_aias_6_0_preview.py --run, once, at the Preview data lock",
        "prereg": "LOCKED (aias-6-0-preview-prereg-r1, Nov 11, 2026)",
        "pablo": "no",
        "earliest": "Fri 2026-12-11 (Preview data lock: after v1.14 Stage 2 if it exists by then, else Dec 11 with "
                    "Stage 2 by addendum; control panel, Pablo Tue 11/24, 11:15 pm); public Tue 2026-12-15",
    },
    "I4_cov_retest": {
        "what": "OPTIONAL: a second Coverage wave (v1.12's 75 probes re-asked to panel N3) for the temporal "
                "reliability of Cov*, which no study yet measures (t5 carries no Coverage block; v1.12 §10 left "
                "the re-ask to Paper B, and v1.19 did not include it)",
        "file": "osf/aias_3_0/outputs/aias_3_0_cov_retest.json",
        "step": "own pre-registration (or a section of I0) -> paid collection (one paid job at a time; never during "
                "t5 or the v1.21 judge) -> score once",
        "prereg": "NOT PRE-REGISTERED",
        "pablo": "YES: new paid collection (cost to re-estimate at Dec prices; v1.12 recorded 17.08 USD on four "
                 "models at November prices) and a scope change",
        "earliest": "after t5's window (opens Thu 2026-12-03 06:00 UTC, 72 h) and the v1.21 judge that follows it; "
                    "scored a day after its collection",
    },
    "I5_apostrophe_sensitivity": {
        "what": "v1.12 and v1.19 re-coded with the typographic apostrophe read as an apostrophe (the v0.42 erratum "
                "of Nov 25 covers t4 only; v1.12 uses v0.42's coder unchanged and its comparators come from t4)",
        "file": "osf/methodology/v1_12/sensitivity/ (as v0.45's t4_SQ), with a dated note",
        "step": "a labelled sensitivity by the locked scorers on re-coded mentions; a corrections-log row if a "
                "published value changes",
        "prereg": "n/a (sensitivity of locked studies; DEVIATIONS note first)",
        "pablo": "YES: choose how to handle it, as for t4 (the Nov 24 options A/B/C)",
        "earliest": "about one working session after his decision",
    },
    "I6_predictive_coverage": {
        "what": "Predictive-validity update: Cov* added to v0.43 Stage 2 by the dated amendment its §2.6 provides "
                "for (outcome: search-interest change to the four weeks ending 2027-03-06)",
        "file": "amendment: osf/v43/prereg/ (before the first Stage 2 outcome pull); result: v0.43 Stage 2 verdicts",
        "step": "amendment deposited before 2027-03-10; three outcome pulls from 2027-03-10, at least 24 h apart; "
                "Stage 2 scoring",
        "prereg": "RULE LOCKED (v0.43 §2.6: each component's hypothesis added by dated amendment, outcome, windows, "
                  "statistic and verdict rule unchanged); the Coverage amendment itself NOT DRAFTED",
        "pablo": "YES: whether AIAS 3.0 ships with this leg registered and its result pending, or waits for it",
        "earliest": "amendment: any day before 2027-03-10; result: not before the third outcome pull, i.e. not "
                    "before Fri 2027-03-12",
    },
    "I7_t5_scored": {
        "what": "t5 (v0.45) scored outputs: Presence and Consistency on N3 three weeks after t4 (used only if I0 "
                "makes the calibration's confirmation read them)",
        "file": "osf/v45/ outputs of score_v0_45.py",
        "step": "t5 collection, acquisition lock, coding (Sonnet 5.5 judge), scoring once",
        "prereg": "LOCKED (v0.45-prereg-r1)",
        "pablo": "no",
        "earliest": "collection from Thu 2026-12-03; stability paper ~12/10 (control panel milestones)",
    },
    "I8_build": {
        "what": "Build facts: PDFs, page counts, report code, cover photo, abstract as published, plain summary, "
                "deposit location and IDs, deviations count, Fable review",
        "file": "the built PDFs and the deposit receipts",
        "step": "charts -> paper -> report (after the paper) -> page-by-page pre-flight -> Fable review -> deposit "
                "-> website",
        "prereg": "n/a",
        "pablo": "cover photo full-size file (photo library: 'Curved slats' is the AIAS 3.0 image); report code; "
                 "Zenodo token if anything deposits in January (deposit rule of Nov 25)",
        "earliest": "after the data lock (I1, I2 and whichever of I4/I6 the release waits for)",
    },
}

# ---------------------------------------------------------------------------------------------------------------
# PENDING tokens: KEY -> (input, where in it, what it prints)
PENDING = {
    # pre-registration and lock record
    "PREREG_TAG": ("I0_release_prereg", "tag name", "the release pre-registration tag"),
    "PREREG_COMMIT": ("I0_release_prereg", "tag object -> commit (10 hex)", "commit the tag names"),
    "PREREG_DATE": ("I0_release_prereg", "tagger date (UTC)", "lock date"),
    "DATA_LOCK_TAG": ("I8_build", "tag aias-3-0-data-locked", "data-lock tag name"),
    "DEVIATIONS_COUNT": ("I8_build", "count of dated entries in osf/aias_3_0/anchor/DEVIATIONS.md", "number"),
    # the headline (outcome-contingent wording fixed in I0, chosen mechanically from I1/I2)
    "CLASS": ("I0_release_prereg", "values.class (rule in I0's wording table, applied to I1/I2 verdicts)",
              "wording class"),
    "HEADLINE": ("I0_release_prereg", "values.headline (I0 wording table, row for CLASS)", "headline sentence"),
    "REPORT_HEADLINE": ("I0_release_prereg", "values.report_headline (managerial form of HEADLINE, fixed in I0)",
                        "report headline"),
    # calibration (I1)
    "CAL_RULE": ("I1_calibration", "selected.rule", "Cov* scale and rating rule as selected"),
    "CAL_SHARE_RATED": ("I1_calibration", "selected.share_rated_112 (3 decimals)", "share of 112 brands rated"),
    "CAL_N_CANDIDATES": ("I1_calibration", "candidates (count)", "number of candidate combined scores"),
    "CAL_COMPOSITE_SENTENCE": ("I1_calibration", "composite.verdict -> I0 sentence", "whether any combination passed"),
    "CAL_RHO_AP": ("I1_calibration", "composite.best.rho_A_P (3 decimals)", "best candidate's rho with Presence"),
    "CAL_BRIDGE_SENTENCE": ("I1_calibration", "bridge.* -> I0 sentence", "how the N3 scores relate to AIAS 2.0's"),
    "FIG_CALIBRATION": ("I1_calibration", "figure built by build_charts_aias3.py from calibration.json",
                        "figure (paper) / chart path (report)"),
    # dissociation (I2, I3)
    "DIS_VERDICT": ("I2_dissociation", "verdicts.H_* (word as the scorer writes it)", "dissociation verdict"),
    "DIS_RHO_P_COV": ("I2_dissociation", "pairs.P_Cov.rho (3 decimals)", "rho of Presence with Coverage"),
    "DIS_RHO_C_COV": ("I2_dissociation", "pairs.C_Cov.rho (3 decimals)", "rho of Consistency with Coverage"),
    "DIS_JOINT": ("I2_dissociation", "joint.statistic (3 decimals)", "Coverage against P and C together"),
    "DIS_N": ("I2_dissociation", "joint.n", "brands rated on all three"),
    "DIS_PREVIEW_SENTENCE": ("I3_preview_outputs", "structure.S_tests / I_tests rows with Cov -> I0 sentence",
                             "the Preview's locked Coverage tests, as read"),
    "FIG_DISSOCIATION": ("I2_dissociation", "figure built from dissociation.json", "figure / chart path"),
    # Coverage over time (I4, optional)
    "RETEST_SENTENCE": ("I4_cov_retest", "verdict -> I0 sentence, or the 'not measured' sentence if not run",
                        "Cov* retest result or its absence"),
    "RETEST_RHO": ("I4_cov_retest", "rho (3 decimals)", "Cov* retest rho"),
    "RETEST_N": ("I4_cov_retest", "n", "brands rated at both waves"),
    "RETEST_DAYS": ("I4_cov_retest", "days between the waves' first calls", "interval"),
    # coding correction (I5)
    "APOS_SENTENCE": ("I5_apostrophe_sensitivity", "sensitivity verdict file -> dated sentence",
                      "effect of the apostrophe re-coding on v1.12/v1.19 values and verdicts"),
    # predictive validity (I6)
    "PRED_SENTENCE": ("I6_predictive_coverage", "amendment status, or Stage 2 Coverage verdict -> sentence",
                      "predictive-validity status for Coverage"),
    "PRED_AMENDMENT_DATE": ("I6_predictive_coverage", "deposit date of the v0.43 Coverage amendment", "date"),
    # build and hand-off (I8)
    "MONTH": ("I8_build", "release month", "e.g. for the Studies entry"),
    "PAPER_PAGES": ("I8_build", "pdfinfo of the paper PDF", "page count"),
    "REPORT_PAGES": ("I8_build", "pdfinfo of the report PDF", "page count"),
    "REPORT_CODE": ("I8_build", "report_catalogue entry (TS-SY-... form; Pablo's call as for the Preview)",
                    "report code"),
    "REPORT_FILE": ("I8_build", "report PDF file name", "file name"),
    "COVER_IMAGE": ("I8_build", "photo library series image for AIAS 3.0 (full-size file from Pablo)",
                    "cover image id"),
    "DEPOSIT": ("I8_build", "deposit receipt (ec6wh path, or Zenodo DOI from January 2027)", "where the record is"),
    "ABSTRACT_VERBATIM": ("I8_build", "the paper's abstract as published", "abstract for content/abstracts.json"),
    "PLAIN_FOUND": ("I8_build", "drawn only from the published abstract (CLAUDE.md step 7)", "plain 'found' line"),
    "PLAIN_SHORT": ("I8_build", "drawn only from the published abstract", "plain 'short' paragraph"),
}

# flags a content item may require (set in the values file at the data lock)
FLAGS = {
    "RETEST_RUN": "I4 ran and was scored",
    "PRED_RESULT": "v0.43 Stage 2 has a Coverage verdict (not before 2027-03-12)",
    "COMPOSITE_ADOPTED": "I1 adopted a combined score (else the scores are reported side by side)",
}


class TokenError(KeyError):
    pass


def keys_in(obj):
    """All (kind, key) tokens in a string, list or dict (dict keys starting with '_' are notes, not content)."""
    if isinstance(obj, str):
        return set(TOKEN.findall(obj))
    if isinstance(obj, dict):
        out = set()
        for k, v in obj.items():
            if k != "requires" and not str(k).startswith("_"):
                out |= keys_in(v)
        return out
    if isinstance(obj, (list, tuple)):
        out = set()
        for v in obj:
            out |= keys_in(v)
        return out
    return set()


def load_values(path):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    for k in ("synthetic", "values", "flags"):
        if k not in d:
            raise TokenError(f"values file {path} has no '{k}'")
    return d


def resolve(kind, key, mode, values=None):
    """mode 'draft': L filled, P shown as a visible placeholder. mode 'final': both filled or an error."""
    if kind == "L":
        return S.resolve(key)
    if key not in PENDING:
        raise TokenError(f"unmapped placeholder {{{{P:{key}}}}}")
    if mode == "draft":
        return f"[[P:{key}]]"
    v = (values or {}).get("values", {}).get(key)
    if v is None or v == "":
        raise TokenError(f"placeholder {{{{P:{key}}}}} has no value in the values file ({PENDING[key][0]})")
    return str(v)


def holds(req, values):
    neg = req.startswith("!")
    r = req[1:] if neg else req
    if r not in FLAGS:
        raise TokenError(f"unknown flag {r}")
    ok = bool((values or {}).get("flags", {}).get(r, False))
    return ok != neg


def fill_text(s, mode, values=None, used=None):
    def rep(m):
        if used is not None:
            used.add((m.group(1), m.group(2)))
        return resolve(m.group(1), m.group(2), mode, values)
    out = TOKEN.sub(rep, s)
    if mode == "final" and ANY_TEMPLATE.search(out):
        raise TokenError(f"template syntax left after fill: {out[:90]}")
    return out


def fill_content(obj, mode, values=None, used=None):
    if isinstance(obj, str):
        return fill_text(obj, mode, values, used)
    if isinstance(obj, dict):
        reqs = obj.get("requires", [])
        if mode == "final" and not all(holds(r, values) for r in reqs):
            return None
        out = {k: fill_content(v, mode, values, used) for k, v in obj.items()
               if k != "requires" and not str(k).startswith("_")}
        if mode == "draft" and reqs:
            out["_draft_requires"] = reqs
        return out
    if isinstance(obj, (list, tuple)):
        return [x for x in (fill_content(v, mode, values, used) for v in obj) if x is not None]
    return obj


def table():
    rows = []
    for k, (inp, where, what) in PENDING.items():
        i = INPUTS[inp]
        rows.append((k, inp, i["file"].split(";")[0], where, i["prereg"], i["earliest"]))
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description="AIAS 3.0 token map")
    ap.add_argument("--inputs", action="store_true")
    a = ap.parse_args(argv)
    if a.inputs:
        for k, i in INPUTS.items():
            print(f"{k}\n  file: {i['file']}\n  prereg: {i['prereg']}\n  Pablo: {i['pablo']}\n  earliest: {i['earliest']}")
        return 0
    for r in table():
        print("\t".join(r))
    print(f"\n{len(PENDING)} placeholder keys, {len(INPUTS)} future inputs, {len(S.LOCKED)} locked keys")
    return 0


if __name__ == "__main__":
    sys.exit(main())
