#!/usr/bin/env python3
"""
Number provenance for the Ranking closing paper (v1.14 + v1.16).

Every number printed in the paper is listed here with the file it comes from and its key
(JSON path) or, for design constants and dates stated in a locked document, the exact text
it is quoted from. The script (1) re-reads every source and checks that the printed string
equals the source value at the printed precision, (2) scans the paper body (Abstract to
Limitations, tables included) for numeric tokens that are not covered by an entry, and
(3) writes NUMBERS_PROVENANCE.md. Exit code 1 on any mismatch or untraced number.

Usage: python3 papers/v1_14_16/provenance_v1_14_16.py
"""

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PAPER = HERE / "v1_14_16_ranking_close_paper_draft.md"
OUT = HERE / "NUMBERS_PROVENANCE.md"

FILES = {
    "R16": "osf/methodology/v1_16/outputs/results_v1_16.json",
    "S14": "osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json",
    "C14": "osf/methodology/v1_14/calibration/calibration_v1_14.json",
    "V10": "osf/methodology/v1_10/outputs/v1_10_verdicts.json",
    "A16": "osf/methodology/v1_16/anchor/git_anchor_v1_16.json",
    "A14": "osf/methodology/v1_14/anchor/git_anchor_v1_14.json",
    "P16": "osf/methodology/v1_16/prereg/PRE_REGISTRATION_v1_16.md",
    "P14": "osf/methodology/v1_14/prereg/PRE_REGISTRATION_v1_14.md",
    "D16": "osf/methodology/v1_16/anchor/DEVIATIONS.md",
    "L16": "osf/methodology/v1_16/outputs/run_v1_16.log",
    "PA10": "papers/v1_10/v1_10_ssrn_paper_draft.md",
}
CACHE = {}


def load(alias):
    if alias not in CACHE:
        p = ROOT / FILES[alias]
        CACHE[alias] = json.loads(p.read_text()) if p.suffix == ".json" else p.read_text()
    return CACHE[alias]


def resolve(obj, path):
    for part in path.split("/"):
        m = re.fullmatch(r"(.*)\[(.+)\]", part)
        if m:
            key, flt = m.groups()
            if key:
                obj = obj[key]
            if flt.isdigit():
                obj = obj[int(flt)]
            else:
                conds = dict(c.split("=") for c in flt.split(","))
                hits = [e for e in obj if all(str(e[k]) == v for k, v in conds.items())]
                assert len(hits) == 1, (path, len(hits))
                obj = hits[0]
        else:
            obj = obj[part]
    return obj


def fmt(v, f):
    if f == "int":
        s = f"{int(round(v)):,}"
    elif f == "p":
        s = f"{v:.4f}" if v < 0.001 else f"{v:.3f}"
    else:
        s = f"{v:.{int(f[1])}f}"
    return s.replace("-", "\u2212")


ENTRIES = []  # (shown, source alias, key or quoted text, kind, fmt)


def J(shown, alias, key, f="f3"):
    ENTRIES.append((shown, alias, key, "json", f))


def T(shown, alias, quote):
    ENTRIES.append((shown, alias, quote, "text", None))


# ---------------- v1.16 primary tests ----------------
W4 = ["t1", "t2", "t3", "t4"]
for h, nums in [("H1_Sep_Presence", ["0.255", "0.411", "0.434", "0.258"]),
                ("H2_Sep_Consistency", ["0.204", "0.071", "0.182", "0.139"])]:
    for w, s in zip(W4, nums):
        b = f"{h}/per_wave/{w}"
        J(s, "R16", f"{b}/rho")
        J(str(resolve(load("R16"), f"{b}/n")), "R16", f"{b}/n", "int")
        J(fmt(resolve(load("R16"), f"{b}/p_perm"), "p"), "R16", f"{b}/p_perm", "p")
        J(fmt(resolve(load("R16"), f"{b}/ci90")[0], "f3"), "R16", f"{b}/ci90[0]")
        J(fmt(resolve(load("R16"), f"{b}/ci90")[1], "f3"), "R16", f"{b}/ci90[1]")
for h in ["H3_Retest_t1_t2", "H5_Retest_t2_t3", "H4_Sep_Presence_t4_S1"]:
    d = resolve(load("R16"), h)
    J(fmt(d["rho"], "f3"), "R16", f"{h}/rho")
    J(str(d["n"]), "R16", f"{h}/n", "int")
    J(fmt(d["p_perm"], "p"), "R16", f"{h}/p_perm", "p")
    J(fmt(d["ci90"][0], "f3"), "R16", f"{h}/ci90[0]")
    J(fmt(d["ci90"][1], "f3"), "R16", f"{h}/ci90[1]")
    if "p_shuffle" in d:
        J(fmt(d["p_shuffle"], "p"), "R16", f"{h}/p_shuffle", "p")
J("0.0001", "R16", "MQ7_negative_control/shuffled_mean_rho_H3", "f4")
J("0.0034", "R16", "H5_Retest_t2_t3/shuffled_mean_rho", "f4")
J("0.20", "R16", "MQ7_negative_control/threshold", "f2")
J("0", "R16", "MQ9_identification/t1/at_floor_outside_main_component", "int")
for w, n in zip(W4, ["55", "54", "54", "71"]):
    J(n, "R16", f"D1_descriptives/{w}/units_rated", "int")
J("65", "R16", "D1_descriptives/t4_S1/units_rated", "int")
J("161", "R16", "D1_descriptives/t1/rankable_answers", "int")
T("180", "P16", "161 of 180")
T("36", "P16", "| 36 | 161 of 180")
for w, s in zip(["t1", "t2", "t3"], ["0.909", "0.901", "0.918"]):
    J(s, "R16", f"published_controls/MQ6_v1_10/per_wave/{w}/rho")
J("0.930", "R16", "published_controls/MQ6_v1_14_t4/rho")
J("112", "R16", "published_controls/MQ6_v1_14_t4/n", "int")
for w, a, b in zip(W4, ["0.923", "0.951", "0.939", "0.952"], ["0.717", "0.713", "0.781", "0.816"]):
    J(a, "R16", f"D2_PREC_vs_v1_10_and_v1_14_statistics/{w}/MNP/rho")
    J(b, "R16", f"D2_PREC_vs_v1_10_and_v1_14_statistics/{w}/MODE/rho")
J("0.786", "R16", "D3_PREC_S0_vs_S1_t4/rho")
J("60", "R16", "D3_PREC_S0_vs_S1_t4/n", "int")
J("0.687", "R16", "E3_early_panel_pi_hat/rho")
J("154", "R16", "E3_early_panel_pi_hat/n", "int")
for k in ["H1", "H2", "H3", "H4_S1", "H5", "SHUFFLE", "BOOT"]:
    J(str(resolve(load("R16"), f"seeds/{k}")), "R16", f"seeds/{k}", "int")
J("10,000", "R16", "draws/perm", "int")
T("2,000", "P16", "Bootstrap 90% percentile CIs (2,000 draws")

# ---------------- v1.16 sensitivities ----------------
SENS = ["S1_first_mention", "S2_floor_3", "S2_floor_10", "S7_without_Denon",
        "S_COI_without_Denon_and_Cheil_Iris", "S9_uncentred", "S_w_pair_weight_1_over_n_minus_1",
        "S_prior_0.1", "S_prior_10.0", "S4_leave_out_v0.19", "S4_leave_out_v0.20",
        "S4_leave_out_v0.21", "S4_leave_out_v0.22", "S4_leave_out_v0.23"]
for s in SENS:
    for h in ["H1", "H2"]:
        for w in W4:
            v = resolve(load("R16"), f"sensitivities/{s}/{h}/per_wave/{w}/rho")
            J(fmt(v, "f3"), "R16", f"sensitivities/{s}/{h}/per_wave/{w}/rho")
J("0.4995", "R16", "sensitivities/S4_leave_out_v0.20/H1/per_wave/t3/rho", "f4")
for w in W4:
    J(str(resolve(load("R16"), f"sensitivities/S2_floor_10/H1/per_wave/{w}/n")), "R16",
      f"sensitivities/S2_floor_10/H1/per_wave/{w}/n", "int")
T("106", "P16", "S-COI, 106 units")
T("1/(k − 1)", "P16", "weight 1/(k − 1)")
T("0.1", "P16", "λ = 0.1 and λ = 10 are sensitivities")
T("10", "P16", "λ = 0.1 and λ = 10 are sensitivities")
T("3", "P16", "Floors 3 and 10 are sensitivity S2")

# ---------------- v1.16 exploratory E1 ----------------
CATS = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
for c in CATS:
    for w in W4:
        base = f"E1_moderators/cells[wave={w},category={c}]"
        J(fmt(resolve(load("R16"), base + "/first_position_concentration"), "f3"), "R16",
          base + "/first_position_concentration")
        J(fmt(resolve(load("R16"), base + "/rho_PREC_P"), "f3"), "R16", base + "/rho_PREC_P")
    b = f"E1_moderators/retest_by_category[category={c}]"
    J(fmt(resolve(load("R16"), b + "/retest_rho_t1_t2"), "f3"), "R16", b + "/retest_rho_t1_t2")
    J(str(resolve(load("R16"), b + "/n")), "R16", b + "/n", "int")
J("16", "R16", "E1_moderators/cells[wave=t1,category=v0.19]/category_size", "int")
J("24", "R16", "E1_moderators/cells[wave=t1,category=v0.20]/category_size", "int")
J("20", "R16", "E1_moderators/spearman_across_cells/cells", "int")
J("0.055", "R16", "E1_moderators/spearman_across_cells/abs_rho_PREC_P_vs_fpc")
J("\u22120.520", "R16", "E1_moderators/spearman_across_cells/abs_rho_PREC_P_vs_category_size")
J("8", "R16", "E1_moderators/cells[wave=t1,category=v0.19]/n", "int")
J("18", "R16", "E1_moderators/cells[wave=t4,category=v0.23]/n", "int")

# ---------------- v1.14 Stage 1 ----------------
for h in ["H1_Sep_Presence", "H2_Sep_Consistency", "H4_Sep_Presence_S1"]:
    d = resolve(load("S14"), h)
    J(fmt(d["rho"], "f3"), "S14", f"{h}/rho")
    J(str(d["n"]), "S14", f"{h}/n", "int")
    J(fmt(d["p_perm"], "p"), "S14", f"{h}/p_perm", "p")
    J(fmt(d["ci90"][0], "f3"), "S14", f"{h}/ci90[0]")
    J(fmt(d["ci90"][1], "f3"), "S14", f"{h}/ci90[1]")
J("1.0000", "S14", "MQ2_mention_parity/per_substrate/v0.20/agreement", "f4")
J("0.9988", "S14", "MQ2_mention_parity/per_substrate/v0.23/agreement", "f4")
J("2,589", "S14", "MQ2_mention_parity/per_substrate/v0.23/agree", "int")
J("2,592", "S14", "MQ2_mention_parity/per_substrate/v0.23/cells", "int")
J("0.98", "S14", "MQ2_mention_parity/per_substrate/v0.23/required", "f2")
J("112", "S14", "unit_join/matched", "int")
J("0.930", "S14", "MQ6_positive_control/rho")
J("0.211", "S14", "MQ9_degeneracy/share_most_common_value")
J("0.868", "S14", "D2_run_reliability_and_MQ7/rel3")
J("0.045", "S14", "D2_run_reliability_and_MQ7/shuffled_mean_rel3")
J("0.792", "S14", "D3_R_S0_vs_R_S1/rho")
J("60", "S14", "D3_R_S0_vs_R_S1/n", "int")
J("0.834", "S14", "D4_MODE_vs_MNP_S0/rho")
J("0.292", "S14", "sensitivities/S2_floor_10/H1/rho")
J("58", "S14", "sensitivities/S2_floor_10/H1/n", "int")
J("0.284", "S14", "sensitivities/S3_candidate_TOP1/H1/rho")
J("0.312", "S14", "sensitivities/S3_candidate_MNP/H1/rho")
J("0.326", "S14", "sensitivities/S3_candidate_TOP3/H1/rho")
J("0.367", "S14", "sensitivities/S1_first_mention/H1/rho")
J("0.333", "S14", "sensitivities/S4_leave_out_v0.19/H1/rho")
J("0.407", "S14", "sensitivities/S4_leave_out_v0.20/H1/rho")
J("0.414", "S14", "sensitivities/S9_uncentred/H1/rho")
J("540", "S14", "analysis_set/counts", "sum54")
T("30", "P14", "the 30 category questions (Phase B; 6 per substrate)")
T("54", "P14", "54 answers per substrate and condition, 540 Phase B answers in all")
T("01:43", "S14", '"created_utc": "2026-11-12T01:43')
T("10 November 2026", "A14", '"tagger_date": "2026-11-10T18:05')
T("7 December 2026", "P16", "Stage 2 (t5 retest, about Dec 7)")

# ---------------- v1.14 calibration and v1.10 (background) ----------------
for w, s in zip(["t1", "t2", "t3"], ["0.093", "0.247", "0.206"]):
    J(s, "C14", f"H1_Sep_Presence/per_wave/{w}/rho")
J("0.858", "C14", "H3_Rank_Stability/rho")
for w, s in zip(["t1", "t2", "t3"], ["0.275", "0.366", "0.307"]):
    J(s, "V10", f"H1_Sep_Presence/per_wave/{w}/rho")
J("0.897", "V10", "H3_Rank_Stability/rho")
J("0.663", "V10", "H4_Sep_Presence_Early/rho")
J("0.951", "V10", "selection/reliability/MNP")

# ---------------- design constants and dates quoted from locked documents ----------------
T("0.30", "P16", "\\|ρ\\| ≤ 0.30 at **every** determined wave")
T("90", "P16", "Bootstrap 90% percentile CIs")
T("100", "P16", "In 20 of the 100 product and service categories")
T("0.186", "R16", '"p_perm": 0.1857814218578142')
T("0.50", "P16", "\\|ρ\\| ≥ 0.50 at **any** determined wave")
T(".05", "P16", "p_perm < 0.05")
T("30", "P16", "its n ≥ 30 units")
T("six", "P16", "**≥ 6 rankable mentions**")
T("0.38", "P16", "H1 is CONFIRMED with probability 0.38")
T("0.77", "P16", "0.38 if the four waves were independent and 0.77 if they were fully dependent")
T("0.93", "P16", "at 0.10, 0.77 and 0.93")
T("0.10", "P16", "at 0.10, 0.77 and 0.93")
T("0.20", "P16", "if the true |ρ| between PREC and Presence is 0.20")
T("1 in 100", "P16", "fewer than 1 in 100 answers")
T("1,000", "P16", "about 1 in 1,000")
T("0.327", "P16", "(Jaccard) 0.327–0.477")
T("0.477", "P16", "(Jaccard) 0.327–0.477")
T("seven", "P16", "at least 7 runs per prompt per day")
T("20 of 100", "P16", "In 20 of the 100 product and service categories")
T("three quarters", "P16", "more than three quarters of responses")
T("13", "A16", "13 files SHA-256 verified 2026-11-12T09:12:34Z")
T("09:10:50", "A16", "pushed to origin 2026-11-12T09:10:50Z")
T("09:12:34", "A16", "verified 2026-11-12T09:12:34Z")
T("09:12:42", "A16", '"written_utc": "2026-11-12T09:12:42')
T("09:13:48", "R16", '"created_utc": "2026-11-12T09:13:48')
T("11 November 2026", "D16", "Pablo, Wed Nov 11, 2026, 11:22 pm")
T("28.43%", "P16", "Samsung Electronics holds 28.43%")
T("0.0001", "PA10", "0.0001 is the smallest value 10,000 draws can return")


def check():
    rows, bad = [], []
    for shown, alias, key, kind, f in ENTRIES:
        if kind == "json":
            if f == "sum54":
                v = sum(resolve(load(alias), key).values())
                got = f"{v:,}"
            else:
                v = resolve(load(alias), key)
                got = fmt(v, f) if f != "int" else f"{int(v):,}"
            ok = got == shown or got.replace(",", "") == shown
            rows.append((shown, FILES[alias], key,
                         repr(v) if f != "sum54" else f"{v} (sum of answered calls, S0 and S1)", ok))
        else:
            ok = key in (ROOT / FILES[alias]).read_text()
            rows.append((shown, FILES[alias], f"text: \u201c{key}\u201d", "", ok))
        if not ok:
            bad.append((shown, alias, key))
    return rows, bad


STRIP = [r"`[^`]*`", r"\$[^$]*\$", r"!\[[^\]]*\]\([^)]*\)", r"\{width=[^}]*\}",
         r"\b[A-Za-z_]+\d[\w.]*", r"§\d+(\.\d+)*", r"\b(Figure|Table) \d", r"\b20\d\d\b",
         r"\b\d+ (January|February|March|April|May|June|July|August|September|October|November|December)\b",
         r"\d\d:\d\d(:\d\d)?", r"SSRN \d+", r"No\. 26-\d+", r"\\[a-zA-Z]+(\{[^}]*\})?", r"^#+ \d+(\.\d+)*",
         r"\bv\d+\.\d+", r"AIAS \d\.\d", r"\b(19|20)\d\d\b", r"Claude Fable 5\.2|GPT-6 Astra|Gemini 4 Argon",
         r"SHA-256", r"top-1"]


def scan(shown_set):
    text = PAPER.read_text()
    body = text[text.index("# Abstract"):text.index("# Declarations")]
    body = re.sub(r"\*\*(Keywords|JEL codes):\*\*.*", "", body)
    untraced = []
    for line in body.splitlines():
        s = line
        for pat in STRIP:
            s = re.sub(pat, " ", s, flags=re.M)
        for tok in re.findall(r"[\u2212-]?\d[\d,]*(?:\.\d+)?", s):
            t = tok.rstrip(",").replace("-", "\u2212")
            if t in shown_set or t.lstrip("\u2212") in shown_set:
                continue
            if re.fullmatch(r"\d", t):  # single digits: ordinals, counts written as figures
                continue
            untraced.append((t, line.strip()[:90]))
    return untraced


def main():
    rows, bad = check()
    shown = {r[0] for r in rows}
    untraced = scan(shown)
    lines = ["# Numbers provenance: Ranking closing paper (v1.14 + v1.16)", "",
             "Generated by `provenance_v1_14_16.py` from the locked output files. Every number printed "
             "in the paper body (Abstract to Limitations, tables included) is listed with its file and "
             "JSON key, or with the exact text of the locked document it is quoted from. Values in the "
             "paper are the source values rounded to the printed precision (minus signs as U+2212).", "",
             f"Entries: {len(rows)}. Mismatches: {len(bad)}. Untraced numeric tokens in the body: {len(untraced)}.", "",
             "| Printed | File | Key or quoted text | Source value | Check |", "|---|---|---|---|---|"]
    for shown_s, f, key, val, ok in rows:
        lines.append(f"| {shown_s} | `{f}` | `{key}` | {val} | {'OK' if ok else 'MISMATCH'} |")
    if untraced:
        lines += ["", "## Untraced tokens", ""] + [f"- {t}: {ctx}" for t, ctx in untraced]
    lines += ["", "Single digits (1 to 9) are not scanned: in the body they are wave, figure, table, hypothesis "
              "or section labels, or small counts written as figures; their sources are the pre-registrations.",
              "Dates, times, SSRN IDs, tags and commits are checked by entries where they carry a result "
              "(run and lock times); bibliographic data are in the References."]
    OUT.write_text("\n".join(lines) + "\n")
    print(f"entries {len(rows)}; mismatches {len(bad)}; untraced {len(untraced)}")
    for b in bad:
        print("MISMATCH", b)
    for u in untraced:
        print("UNTRACED", u)
    return 1 if bad or untraced else 0


if __name__ == "__main__":
    sys.exit(main())
