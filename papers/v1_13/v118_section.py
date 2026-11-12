"""
v118_section.py -- the exploratory v1.18 section of Grounding Paper A (§3.8): four definitions of a brand's own share
of the sources AI answers cite. Exploratory: it gates nothing and changes none of v1.13's rules.

Inputs (copied from branch v1.18, osf/methodology/v1_18/outputs/, into papers/v1_13/inputs/v1_18/ and recorded with
their SHA-256 in INPUTS_v1_18.json): v1_18_results.json (analyse_v1_18.py --run, once, after tag v1.18-prereg-r1) and
descriptive_v1_18.json (descriptive_v1_18.py, DEVIATIONS Entry 1). load() refuses a copy whose SHA-256 differs from the
record, or a descriptive file that names a different results file. Every number of the section is a leaf of one of the
two files (sources "v118" and "v118d" of v113_values.Values) or a named function of such leaves.
"""
import hashlib
import json
from pathlib import Path

import v113_values as VV

HERE = Path(__file__).resolve().parent
INPUT_DIR = HERE / "inputs" / "v1_18"
RECORD = "INPUTS_v1_18.json"
FILES = {"v118": "v1_18_results.json", "v118d": "descriptive_v1_18.json"}
DEFS = [("K_own_domain", "K", "own domain"), ("P_any_company", "P", "any company"),
        ("Y_own_plus_listings", "Y", "own plus listings"), ("M_not_owned", "M", "not owned")]
PAIRS = [(a, b) for i, (a, _, _) in enumerate(DEFS) for (b, _, _) in DEFS[i + 1:]]
SHORT = {d: s for d, s, _ in DEFS}
SENS = [("S1_unresolved_out", "S1 unresolved domains in the denominator, outside every class"),
        ("S1_unresolved_in", "S1 unresolved domains inside P's and Y's classes"),
        ("S2_retailer_as_company", "S2 retailers counted as company"),
        ("S3_alias_focal", "S3 alias domains counted as own"),
        ("S4_floor_3", "S4 floor of 3 grounded answers"), ("S4_floor_10", "S4 floor of 10 grounded answers"),
        ("S5_sources_field", "S5 retrieved set (sources) instead of citations"),
        ("S6_without_denon", "S6 without Denon"),
        ("S6_COI_without_denon_and_agency_five", "S6-COI without Denon and the five agency-tie brands"),
        ("S7_without_gemini", "S7 without Gemini 4 Argon")]


class InputError(RuntimeError):
    pass


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(input_dir=None):
    """{"v118": results, "v118d": descriptive, "v118_inputs": record}; refuses a changed or mismatched copy."""
    d = Path(input_dir or INPUT_DIR)
    rec_path = d / RECORD
    if not rec_path.exists():
        raise InputError(f"{rec_path} not found")
    rec = json.loads(rec_path.read_text(encoding="utf-8"))
    out = {"v118_inputs": rec}
    for key, name in FILES.items():
        p = d / name
        want = (rec.get("files") or {}).get(name, {}).get("sha256")
        if not p.exists() or not want:
            raise InputError(f"{name}: copy or recorded SHA-256 missing in {d}")
        got = sha256(p)
        if got != want:
            raise InputError(f"{name}: SHA-256 {got} differs from the record {want}")
        out[key] = json.loads(p.read_text(encoding="utf-8"))
    if out["v118d"]["inputs"]["v1_18_results"] != rec["files"][FILES["v118"]]["sha256"]:
        raise InputError("descriptive_v1_18.json was computed from a different v1_18_results.json")
    return out


def _overlap(a, b):
    return not (a[1] < b[0] or b[1] < a[0])


def distinct_sentence(R):
    """§5 reporting rule of v1.18: definitions whose 90% intervals do not overlap are called different."""
    ci = R["primary_ci"]["program_pair_weighted"]
    diff, same = [], []
    for a, b in PAIRS:
        (diff if not _overlap(ci[a], ci[b]) else same).append(f"{SHORT[a]} and {SHORT[b]}")
    s = ("By v1.18's reporting rule (definitions whose 90% intervals do not overlap are called different), the "
         "program share differs between " + VV.joinand(diff) + "" if diff else
         "By v1.18's reporting rule no two definitions give program shares whose 90% intervals do not overlap")
    if same:
        s += ("; " if diff else ": ") + VV.joinand(same) + " are not distinguishable at this sample size"
    return s + "."


def compute(val, Cells, md_table, dash="--"):
    """Put every value of §3.8 into val (sources "v118", "v118d" and "registry" must be in val.src)."""
    R, D = val.src["v118"], val.src["v118d"]
    val.put("V118_N_ANSWERS", "v118", ["inputs", "n_answers"], VV.i0)
    val.put("V118_N_PAIRS", "v118", ["primary", "program", "n_pairs"], VV.i0)
    val.put("V118_N_RATED", "v118", ["primary", "program", "n_rated"], VV.i0)
    val.put("V118_N_BOOT", "v118", ["primary_ci", "n_boot"], VV.i0)
    for d, s, _ in DEFS:
        val.put(f"V118_{s}", "v118", ["primary", "program", "pair_weighted", d], VV.r2)
        val.put(f"V118_{s}_LO", "v118", ["primary_ci", "program_pair_weighted", d, 0], VV.r2)
        val.put(f"V118_{s}_HI", "v118", ["primary_ci", "program_pair_weighted", d, 1], VV.r2)
    val.word("V118_DISTINCT_SENTENCE", distinct_sentence(R),
             ["v118", "primary_ci", "program_pair_weighted (interval overlap, v1.18 prereg §5 reporting rule)"])
    # E3 / E4: how far brand-level readings move between definitions
    ag = R["primary"]["agreement"]
    cl = Cells(val)
    rows = []
    for a, b in PAIRS:
        k = f"{a}~{b}"
        ap, cp = ["primary", "agreement", k], ["primary_ci"]
        label = f"{SHORT[a]}--{SHORT[b]}" + (" (identity: M = 100 minus K)" if ag[k].get("identity") else "")
        rows.append([label, cl.f("v118", ap + ["rho_w"], VV.r3),
                     cl.f("v118", cp + ["rho_w", k, 0], VV.r3) + " to " + cl.f("v118", cp + ["rho_w", k, 1], VV.r3),
                     cl.f("v118", ap + ["share_changed"], VV.pct0),
                     cl.f("v118", cp + ["share_changed", k, 0], VV.pct0) + " to " +
                     cl.f("v118", cp + ["share_changed", k, 1], VV.pct0)])
    val.table("TABLE_V118_PAIRS", md_table(["Pair", "$\\rho_w$", "90% interval", "Brands moving > 25 points",
                                            "90% interval"], rows, ["l", "r", "r", "r", "r"]), cl.cells)
    kpy = [(a, b) for a, b in PAIRS if "M_not_owned" not in (a, b)]
    rr = [("v118", ["primary", "agreement", f"{a}~{b}", "rho_w"]) for a, b in kpy]
    sr = [("v118", ["primary", "agreement", f"{a}~{b}", "share_changed"]) for a, b in kpy]
    val.derive("V118_RHO_LO", VV.d_min, rr, VV.r3)
    val.derive("V118_RHO_HI", VV.d_max, rr, VV.r3)
    val.derive("V118_MOVE_LO", VV.d_min, sr, VV.pct0)
    val.derive("V118_MOVE_HI", VV.d_max, sr, VV.pct0)
    # S1-S7 in one table (pair-weighted program shares)
    cl = Cells(val)
    rows = []
    for key, label in [(None, "Primary")] + SENS:
        p = ["primary", "program"] if key is None else ["sensitivities", key, "program"]
        rows.append([label] + [cl.f("v118", p + ["pair_weighted", d], VV.r2) for d, _, _ in DEFS] +
                    [cl.f("v118", p + ["n_pairs"], VV.i0), cl.f("v118", p + ["n_rated"], VV.i0)])
    val.table("TABLE_V118_SENS", md_table(["Analysis", "K", "P", "Y", "M", "Pairs", "Rated"], rows,
                                          ["l", "r", "r", "r", "r", "r", "r"]), cl.cells)
    # UNRESOLVED shares (descriptive, DEVIATIONS Entry 1 of v1.18)
    for nm, f in (("CIT", "citations_field"), ("SRC", "sources_field_S5")):
        val.put(f"V118_UNRES_{nm}", "v118d", [f, "pooled", "pair_weighted_all_pairs"], VV.f1)
        refs = [("v118d", [f, "brands", b, "unresolved_share"]) for b in sorted(D[f]["brands"])]
        val.derive(f"V118_UNRES_{nm}_LO", VV.d_min, refs, VV.f1)
        val.derive(f"V118_UNRES_{nm}_HI", VV.d_max, refs, VV.f1)
    # brands with a bootstrap value in fewer than half of the draws
    bd = D["bootstrap_draws"]
    cl = Cells(val)
    names = []
    for b in bd["flagged"]:
        reg = val.src["registry"].get(b.replace(":", "|", 1))
        nm = reg["brand"] if reg else b
        names.append(f"{nm} ({cl.f('v118d', ['bootstrap_draws', 'brands', b, 'min_draws'], VV.i0)} of "
                     f"{cl.f('v118d', ['bootstrap_draws', 'n_boot'], VV.i0)} draws)")
    txt = ("One rated brand had a value in fewer than half of the bootstrap draws, and its brand-level interval is "
           "flagged: " if len(names) == 1 else
           f"{len(names)} rated brands had a value in fewer than half of the bootstrap draws, and their brand-level "
           "intervals are flagged: ") + VV.joinand(names) + "." if names else \
        "Every rated brand had a value in at least half of the bootstrap draws."
    val.table("V118_FLAG_SENTENCE", txt, cl.cells)
    rec = val.src["v118_inputs"]["files"]
    val.word("V118_SHA_RESULTS", rec[FILES["v118"]]["sha256"][:12], ["v118_inputs", FILES["v118"], "sha256"])
    val.word("V118_SHA_DESC", rec[FILES["v118d"]]["sha256"][:12], ["v118_inputs", FILES["v118d"], "sha256"])
