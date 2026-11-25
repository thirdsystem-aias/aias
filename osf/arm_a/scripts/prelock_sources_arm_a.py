#!/usr/bin/env python3
"""Arm A pre-lock source fixing (pre-registration section 3.4 items 4-5; section 10.1 items 5-6). No paid call, no
DataForSEO call, and no sales value is read: only the identity of each source file is fixed.

  python3 osf/arm_a/scripts/prelock_sources_arm_a.py            -> osf/arm_a/prereg/prelock_sources_arm_a.json
                                                                  + osf/arm_a/registries/arm_a_sales_sources_r1.csv
What it reads (free public sources named in prereg/armA_prelock_notes_r1.md section 4, plus files on disk):
  * SEC EDGAR submissions index (data.sec.gov/submissions/CIK##########.json): form, report date, filing date and
    accession number of each software company's annual report. Financial data are not requested.
  * FDIC BankFind API (api.fdic.gov): for each certificate of the brand's v0.40 holder, the institution record
    (name, active flag) and whether a Call Report exists for 2025-12-31 (fields CERT and REPDTE only; deposits are
    not requested).
  * BTS T-100 Domestic Segment (U.S. Carriers) 2025, the file v0.40 downloaded (on disk): SHA-256, columns, the
    YEAR values and the number of rows per carrier code and month (coverage only; passengers are not summed).
  * ECB Data Portal, series EXR.A.USD.EUR.SP00.A (annual average USD per EUR): that a 2025 observation exists. The
    value is not stored.
"""
import csv
import hashlib
import io
import json
import os
import sys
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARM = HERE.parent
ROOT = ARM.parents[1]
REG = ARM / "registries"
OUT_JSON = ARM / "prereg" / "prelock_sources_arm_a.json"
OUT_CSV = REG / "arm_a_sales_sources_r1.csv"
UA = "AIAS-research-prelock-check/1.0"     # generic client name; no personal contact in the header
WT = ROOT.parent                            # ~/aias/_worktrees
V40_REG = WT / "v0.40-paper-r2/osf/v40/registries/out"   # frozen v0.40 registry (2026-11-12), read only
BTS_2025 = Path(os.path.expanduser("~/aias/osf/v40/data/raw/bts/T100D_SEGMENT_US_2025.zip"))  # read only

# Software: brand-master CIKs (pre-registration section 3.3) and the annual form each files.
SOFTWARE = [("BR-00418", "Salesforce", "0001108524", "10-K"), ("BR-00419", "HubSpot", "0001404655", "10-K"),
            ("BR-00420", "ServiceNow", "0001373715", "10-K"), ("BR-00421", "Workday", "0001327811", "10-K"),
            ("BR-00422", "SAP", "0001000184", "20-F"), ("BR-00423", "Oracle", "0001341439", "10-K"),
            ("BR-00425", "Figma", "0001579878", "10-K"), ("BR-00428", "Datadog", "0001561550", "10-K"),
            ("BR-00429", "Snowflake", "0001640147", "10-K"), ("BR-00431", "Twilio", "0001447669", "10-K"),
            ("BR-00432", "Cloudflare", "0001477333", "10-K"), ("BR-00433", "MongoDB", "0001441816", "10-K")]
FY_CUTOFF = "2025-12-31"

# Banks: brand-master ID -> v0.40 holder (RSSD, banks_current.csv). Discover is not a v0.40 current unit.
BANKS = [("BR-00463", "1039502"), ("BR-00464", "1073757"), ("BR-00465", "1120754"), ("BR-00466", "1951350"),
         ("BR-00467", "1119794"), ("BR-00468", "2277860"), ("BR-00469", "2162966"), ("BR-00470", "2380443"),
         ("BR-00471", "1069778"), ("BR-00472", "1074156"), ("BR-00473", "1238565"), ("BR-00474", "1026632"),
         ("BR-00475", "1070345"), ("BR-00476", "1068191"), ("BR-00477", "1231333"), ("BR-00478", "1132449"),
         ("BR-00479", "1075612"), ("BR-00480", "1037003"), ("BR-00481", "1275216"), ("BR-00482", "1068025"),
         ("BR-00483", "1562859"), ("BR-00484", "1857108"), ("BR-00485", "3242838"), ("BR-00486", "4795461"),
         ("BR-00487", "6073350")]

# Airlines: brand-master ID -> BTS carrier code (v0.40 airlines_current.csv `code`).
AIRLINES = [("BR-00488", "AA"), ("BR-00489", "DL"), ("BR-00490", "UA"), ("BR-00491", "WN"), ("BR-00492", "AS"),
            ("BR-00493", "B6"), ("BR-00494", "F9"), ("BR-00495", "G4"), ("BR-00496", "MX"), ("BR-00497", "HA"),
            ("BR-00498", "SY")]


def get_json(url, fetch=None):
    if fetch is not None:
        return fetch(url)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)


def get_text(url, fetch=None):
    if fetch is not None:
        return fetch(url)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace")


def pick_annual(submissions, form, cutoff=FY_CUTOFF):
    """Latest original annual report of `form` whose report date (fiscal year end) is on or before `cutoff`."""
    rec = submissions["filings"]["recent"]
    rows = [dict(zip(rec.keys(), vals)) for vals in zip(*rec.values())]
    rows = [r for r in rows if r.get("form") == form and r.get("reportDate") and r["reportDate"] <= cutoff]
    if not rows:
        return None
    rows.sort(key=lambda r: (r["reportDate"], r["filingDate"]))
    r = rows[-1]
    return {k: r.get(k) for k in ("form", "reportDate", "filingDate", "accessionNumber", "primaryDocument")}


def v40_holders():
    with open(V40_REG / "banks_current.csv", newline="", encoding="utf-8") as f:
        return {r["HOLDER"]: r for r in csv.DictReader(f)}


def fdic_cert(cert, fetch=None):
    inst = get_json(f"https://api.fdic.gov/banks/institutions?filters=CERT:{cert}&fields=CERT,NAME,ACTIVE", fetch)
    fin = get_json("https://api.fdic.gov/banks/financials?filters=CERT:%s%%20AND%%20REPDTE:20251231"
                   "&fields=CERT,REPDTE" % cert, fetch)
    idata = [d["data"] for d in inst.get("data", [])]
    fdata = [d["data"] for d in fin.get("data", [])]
    return {"cert": cert, "name": idata[0].get("NAME") if idata else None,
            "active_now": idata[0].get("ACTIVE") if idata else None,
            "call_report_20251231": any(str(d.get("REPDTE")) == "20251231" for d in fdata)}


def bts_coverage(path=BTS_2025, codes=None):
    codes = set(codes or [c for _, c in AIRLINES])
    h = hashlib.sha256(path.read_bytes()).hexdigest()
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        member = max((i for i in z.infolist() if i.filename.lower().endswith(".csv")
                      and "documentation" not in i.filename.lower()), key=lambda i: i.file_size).filename
        cov, years, header = {}, set(), None
        with z.open(member) as fh:
            rdr = csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"))
            header = rdr.fieldnames
            for r in rdr:
                years.add(r.get("YEAR"))
                c = r.get("UNIQUE_CARRIER")
                if c in codes:
                    cov.setdefault(c, {}).setdefault(r.get("MONTH"), 0)
                    cov[c][r.get("MONTH")] += 1
    months = {c: sorted(int(m) for m in cov.get(c, {})) for c in sorted(codes)}
    shown = str(path).replace(os.path.expanduser("~"), "~", 1)
    return {"file": shown, "sha256": h, "bytes": path.stat().st_size, "member": member, "columns": header,
            "years": sorted(years), "months_by_carrier": months}


def ecb_series_exists(fetch=None):
    url = ("https://data-api.ecb.europa.eu/service/data/EXR/A.USD.EUR.SP00.A"
           "?startPeriod=2025&endPeriod=2025&format=csvdata")
    txt = get_text(url, fetch)
    rows = list(csv.DictReader(io.StringIO(txt)))
    return {"series": "EXR.A.USD.EUR.SP00.A", "url": url,
            "obs_2025": sum(1 for r in rows if r.get("TIME_PERIOD") == "2025")}   # value deliberately not stored


def brand_names():
    with open(REG / "arm_a_domains_r1.csv", newline="", encoding="utf-8") as f:
        return {r["brand_id"]: r["brand"] for r in csv.DictReader(f) if "site" not in r["brand"]}


def main(fetch=None, bts_path=BTS_2025):
    run = datetime.now(timezone.utc).isoformat(timespec="seconds")
    names = brand_names()
    out = {"run_utc": run, "script": "osf/arm_a/scripts/prelock_sources_arm_a.py", "software": [], "banks": [],
           "airlines": None, "ecb": None}
    rows = []
    for bid, brand, cik, form in SOFTWARE:
        sub = get_json(f"https://data.sec.gov/submissions/CIK{cik}.json", fetch)
        pick = pick_annual(sub, form)
        out["software"].append({"brand_id": bid, "brand": brand, "cik": cik, "form": form, "filing": pick})
        acc = pick["accessionNumber"] if pick else ""
        rows.append({"brand_id": bid, "brand": brand, "category": "software",
                     "measure": "total revenue, latest fiscal year ended on or before 2025-12-31",
                     "period": f"fiscal year ended {pick['reportDate']}" if pick else "",
                     "source": f"SEC EDGAR {form}, CIK {cik}", "identifier": f"accession {acc}",
                     "status": "FIXED" if pick else "NOT_FOUND",
                     "note": "EUR, converted at ECB EXR.A.USD.EUR.SP00.A for 2025" if form == "20-F" else ""})
    holders = v40_holders()
    for bid, rssd in BANKS:
        h = holders[rssd]
        certs = [c for c in h["certs"].split("|") if c]
        checks = [fdic_cert(c, fetch) for c in certs]
        out["banks"].append({"brand_id": bid, "holder_rssd": rssd, "holder_name": h["holder_name"], "certs": checks})
        filed = [c["cert"] for c in checks if c["call_report_20251231"]]
        rows.append({"brand_id": bid, "brand": names.get(bid, h["brand"]), "category": "banks",
                     "measure": "total deposits (DEP), summed over the holder's certificates that filed",
                     "period": "Call Report 2025-12-31",
                     "source": "FDIC BankFind Suite API, financials, REPDTE 20251231",
                     "identifier": "CERT " + "|".join(filed) + f" (v0.40 holder RSSD {rssd})",
                     "status": "FIXED" if filed else "NOT_FOUND", "note": ""})
    rows.append({"brand_id": "BR-00521", "brand": "Discover", "category": "banks", "measure": "", "period": "",
                 "source": "", "identifier": "", "status": "NO_PRESENCE",
                 "note": "not a v0.40 current unit (living-brand control); no v0.40 AI share; descriptive only"})
    cov = bts_coverage(bts_path)
    out["airlines"] = cov
    for bid, code in AIRLINES:
        months = cov["months_by_carrier"].get(code, [])
        rows.append({"brand_id": bid, "brand": names.get(bid, code), "category": "airlines",
                     "measure": "passengers (PASSENGERS), summed over all 2025 rows of the carrier",
                     "period": "calendar 2025", "source": "BTS T-100 Domestic Segment (U.S. Carriers), TranStats",
                     "identifier": f"UNIQUE_CARRIER {code}; file sha256 {cov['sha256'][:16]}",
                     "status": "FIXED" if len(months) == 12 else f"PARTIAL_{len(months)}_MONTHS",
                     "note": "months present: " + ",".join(str(m) for m in months)})
    out["ecb"] = ecb_series_exists(fetch)
    OUT_JSON.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    cols = ["brand_id", "brand", "category", "measure", "period", "source", "identifier", "status", "note"]
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} rows -> {OUT_CSV.relative_to(ROOT)}; record -> {OUT_JSON.relative_to(ROOT)}")
    return out


if __name__ == "__main__":
    main()
    sys.exit(0)
