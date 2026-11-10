#!/usr/bin/env python3
"""Build osf/v43/registries/units_v0_43.csv (112 units) and the parity file
osf/v43/prereg/parity_units_v0_43.json (PRE_REGISTRATION_v0_43 section 3.1 / 5.4).

All values are copied as the exact source strings; the parity check re-reads the
output and the frozen inputs independently and compares string-exact and float-exact.
Usage: python3 build_units_v0_43.py [--root REPO_ROOT]
"""
import argparse
import csv
import json
import os
import sys

SUBSTRATES = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
EXPECTED_N = {"v0.19": 16, "v0.20": 24, "v0.21": 24, "v0.22": 24, "v0.23": 24}
WAVES = ["t1", "t2", "t3"]
COLS = (["substrate", "unit", "search_name", "cell"]
        + [f"{f}_{w}" for w in WAVES for f in ("P", "C_star", "mentions", "pi_hat")])


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def build(root):
    inp = os.path.join(root, "osf/v43/registries/inputs")
    v19 = read_csv(os.path.join(inp, "v1_9_unit_table.csv"))
    v41 = read_csv(os.path.join(inp, "v41_three_wave_table.csv"))
    names = {r["code"]: r["brand"] for r in read_csv(os.path.join(inp, "v23_registry_names.csv"))}

    a = {(r["wave"], r["substrate"], r["brand"]): r for r in v19}
    b = {(r["wave"], r["substrate"], r["brand"]): r for r in v41}
    assert len(a) == len(v19) and len(b) == len(v41), "duplicate keys in inputs"

    order, seen = [], set()
    for r in v41:
        k = (r["substrate"], r["brand"])
        if k not in seen:
            seen.add(k)
            order.append(k)
    order.sort(key=lambda k: SUBSTRATES.index(k[0]))  # stable: keeps v41 file order within substrate
    rows = []
    for sub, unit in order:
        cells = {b[(w, sub, unit)]["cell"] for w in WAVES}
        assert len(cells) == 1, f"cell differs across waves for {sub} {unit}"
        row = {"substrate": sub, "unit": unit,
               "search_name": names[unit] if sub == "v0.23" else unit,
               "cell": cells.pop()}
        for w in WAVES:
            s = a[(w, sub, unit)]
            row[f"P_{w}"] = s["P"]
            row[f"C_star_{w}"] = s["C_star"]
            row[f"mentions_{w}"] = s["mentions"]
            row[f"pi_hat_{w}"] = b[(w, sub, unit)]["pi_hat"]
        rows.append(row)
    return rows, v19, v41, names


def write_units(root, rows):
    path = os.path.join(root, "osf/v43/registries/units_v0_43.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    return path


def same_float(x, y):
    if x == "" and y == "":
        return True
    if x == "" or y == "":
        return False
    return float(x) == float(y)


def parity(root):
    """Independent re-read of the output against the frozen inputs."""
    inp = os.path.join(root, "osf/v43/registries/inputs")
    out = read_csv(os.path.join(root, "osf/v43/registries/units_v0_43.csv"))
    v19 = read_csv(os.path.join(inp, "v1_9_unit_table.csv"))
    v41 = read_csv(os.path.join(inp, "v41_three_wave_table.csv"))
    names = {r["code"]: r["brand"] for r in read_csv(os.path.join(inp, "v23_registry_names.csv"))}
    res = {"n_units": len(out), "units_per_substrate": {}, "fields": {}, "mismatches": [],
           "unit_set_equal_v19_v41": None, "rare_beauty_substrates": []}
    for s in SUBSTRATES:
        res["units_per_substrate"][s] = sum(1 for r in out if r["substrate"] == s)
    res["substrate_counts_as_expected"] = res["units_per_substrate"] == EXPECTED_N
    res["unit_set_equal_v19_v41"] = (
        {(r["substrate"], r["brand"]) for r in v19} == {(r["substrate"], r["brand"]) for r in v41}
        == {(r["substrate"], r["unit"]) for r in out})
    res["rare_beauty_substrates"] = sorted(r["substrate"] for r in out if r["unit"] == "Rare Beauty")
    res["v23_names_match_registry"] = all(
        r["search_name"] == names[r["unit"]] for r in out if r["substrate"] == "v0.23")
    res["non_v23_search_name_equals_unit"] = all(
        r["search_name"] == r["unit"] for r in out if r["substrate"] != "v0.23")
    a = {(r["wave"], r["substrate"], r["brand"]): r for r in v19}
    b = {(r["wave"], r["substrate"], r["brand"]): r for r in v41}
    src_for = {"P": (a, "P"), "C_star": (a, "C_star"), "mentions": (a, "mentions"), "pi_hat": (b, "pi_hat")}
    for fld in ("P", "C_star", "mentions", "pi_hat"):
        tab, col = src_for[fld]
        n = ns = nf = 0
        blank = 0
        for r in out:
            for w in WAVES:
                src = tab[(w, r["substrate"], r["unit"])][col]
                got = r[f"{fld}_{w}"]
                n += 1
                blank += (got == "")
                es = got == src
                ef = same_float(got, src)
                ns += es
                nf += ef
                if not (es and ef):
                    res["mismatches"].append([r["substrate"], r["unit"], w, fld, got, src])
        res["fields"][fld] = {"n_checked": n, "n_string_exact": ns, "n_float_exact": nf, "n_blank": blank}
    nc = ncs = 0
    for r in out:
        for w in WAVES:
            nc += 1
            ncs += (r["cell"] == b[(w, r["substrate"], r["unit"])]["cell"])
    res["fields"]["cell"] = {"n_checked": nc, "n_string_exact": ncs}
    res["all_exact"] = (not res["mismatches"] and res["n_units"] == 112
                        and res["substrate_counts_as_expected"] and res["unit_set_equal_v19_v41"]
                        and res["v23_names_match_registry"]
                        and all(f["n_checked"] == f["n_string_exact"] for f in res["fields"].values()))
    return res


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
    args = ap.parse_args(argv)
    rows, *_ = build(args.root)
    write_units(args.root, rows)
    res = parity(args.root)
    with open(os.path.join(args.root, "osf/v43/prereg/parity_units_v0_43.json"), "w") as fh:
        json.dump(res, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps({k: res[k] for k in ("n_units", "units_per_substrate", "fields", "all_exact")}, indent=1))
    return 0 if res["all_exact"] else 1


if __name__ == "__main__":
    sys.exit(main())
