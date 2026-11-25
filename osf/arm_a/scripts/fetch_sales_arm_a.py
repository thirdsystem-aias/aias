#!/usr/bin/env python3
"""Arm A: read the airline, bank and software sales values from the sources fixed before the lock
(registries/arm_a_sales_sources_r1.csv, prereg/prelock_sources_arm_a.json). Runs only after the lock anchor exists.

  python3 osf/arm_a/scripts/fetch_sales_arm_a.py   -> osf/arm_a/data/sales/arm_a_sales_values.csv

Rules (section 3.3, 3.4 item 5; unit-tested with fakes in tests/test_registries_arm_a.py):
  * Airlines: PASSENGERS summed over every 2025 row of the brand's UNIQUE_CARRIER code (all service classes) in the
    BTS T-100 Domestic Segment file whose SHA-256 was fixed before the lock.
  * Banks: FDIC BankFind financials, DEP (thousands of US$) at REPDTE 20251231, summed over the fixed certificates.
  * Software: SEC XBRL company facts of the fixed accession number; the first of the tags Revenues,
    RevenueFromContractWithCustomerExcludingAssessedTax (us-gaap) or Revenue (ifrs-full, SAP) with a fact of that
    accession whose period ends on the report date and lasts 330-380 days; SAP's EUR value times the ECB annual average
    USD per EUR for 2025 (EXR.A.USD.EUR.SP00.A).
"""
import csv
import io
import json
import sys
import zipfile
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import params_arm_a as P                  # noqa: E402
import prelock_sources_arm_a as PS        # noqa: E402

TAGS = [("us-gaap", "Revenues"), ("us-gaap", "RevenueFromContractWithCustomerExcludingAssessedTax"),
        ("ifrs-full", "Revenue")]
OUT = P.DATA / "sales"


def bts_passengers(path, codes, fixed_sha):
    import hashlib
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != fixed_sha:
        raise ValueError("BTS file differs from the one fixed before the lock")
    tot = {c: 0.0 for c in codes}
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        member = max((i for i in z.infolist() if i.filename.lower().endswith(".csv")
                      and "documentation" not in i.filename.lower()), key=lambda i: i.file_size).filename
        with z.open(member) as fh:
            for r in csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8", errors="replace")):
                if r["YEAR"] == "2025" and r["UNIQUE_CARRIER"] in tot:
                    tot[r["UNIQUE_CARRIER"]] += float(r["PASSENGERS"] or 0)
    return tot


def fdic_deposits(certs, fetch=None):
    total = 0.0
    for c in certs:
        d = PS.get_json("https://api.fdic.gov/banks/financials?filters=CERT:%s%%20AND%%20REPDTE:20251231"
                        "&fields=CERT,REPDTE,DEP" % c, fetch)
        vals = [x["data"]["DEP"] for x in d.get("data", []) if str(x["data"].get("REPDTE")) == "20251231"]
        if len(vals) != 1:
            raise ValueError(f"CERT {c}: {len(vals)} Call Report rows for 2025-12-31")
        total += float(vals[0])
    return total


def sec_revenue(facts, accession, report_date):
    end = date.fromisoformat(report_date)
    for ns, tag in TAGS:
        units = facts.get("facts", {}).get(ns, {}).get(tag, {}).get("units", {})
        for unit, rows in units.items():
            for f in rows:
                if f.get("accn") != accession or f.get("end") != report_date or not f.get("start"):
                    continue
                days = (end - date.fromisoformat(f["start"])).days
                if 330 <= days <= 380:
                    return float(f["val"]), unit, f"{ns}:{tag}"
    return None, None, None


def ecb_rate_2025(fetch=None):
    txt = PS.get_text("https://data-api.ecb.europa.eu/service/data/EXR/A.USD.EUR.SP00.A"
                      "?startPeriod=2025&endPeriod=2025&format=csvdata", fetch)
    rows = [r for r in csv.DictReader(io.StringIO(txt)) if r.get("TIME_PERIOD") == "2025"]
    if len(rows) != 1:
        raise ValueError("ECB 2025 annual average not found")
    return float(rows[0]["OBS_VALUE"])


def main(fetch=None, bts_path=None, out=OUT):
    if not P.ANCHOR.exists():
        print("REFUSED: the lock anchor does not exist; sales values are read only after the lock")
        return 2
    rec = json.loads((P.ARM / "prereg" / "prelock_sources_arm_a.json").read_text(encoding="utf-8"))
    values = []
    codes = dict(PS.AIRLINES)
    import os
    path = bts_path or os.path.expanduser(rec["airlines"]["file"])
    pax = bts_passengers(path, list(codes.values()), rec["airlines"]["sha256"])
    values += [(b, "airlines", pax[c], "passengers") for b, c in codes.items()]
    for b in rec["banks"]:
        certs = [c["cert"] for c in b["certs"] if c["call_report_20251231"]]
        values.append((b["brand_id"], "banks", fdic_deposits(certs, fetch), "deposits_thousand_usd"))
    rate = None
    for s in rec["software"]:
        cik = s["cik"]
        facts = PS.get_json(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", fetch)
        v, unit, tag = sec_revenue(facts, s["filing"]["accessionNumber"], s["filing"]["reportDate"])
        if v is None:
            raise ValueError(f"{s['brand']}: no revenue fact for the fixed accession")
        if unit == "EUR":
            rate = rate or ecb_rate_2025(fetch)
            v, unit = v * rate, "USD (EUR x ECB 2025 annual average)"
        values.append((s["brand_id"], "software", v, f"revenue {unit} {tag}"))
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "arm_a_sales_values.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["brand_id", "category", "value", "measure"])
        w.writerows(values)
    print(f"{len(values)} sales values -> {out / 'arm_a_sales_values.csv'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
