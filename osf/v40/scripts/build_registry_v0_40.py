#!/usr/bin/env python3
"""AIAS v0.40 registry builder (draft r1, for the v0.40-prereg-r1 lock).

Rebuilds every number in the v0.40 brand registry from public data plus two hand-sourced tables.

Data (public, official):
  BTS T-100 Domestic Segment (U.S. Carriers), CLASS F scheduled passenger service   -> airline shares (RPM)
  BTS On-Time: Marketing Carrier On-Time Performance (Beginning January 2018)        -> regional-to-brand allocation
  FDIC Summary of Deposits, api.fdic.gov/banks/sod                                    -> bank shares (deposits)
  FDIC BankFind /history and /failures                                                -> legal events, post-SOD status check

Hand-sourced tables (every row carries its source URLs; see the registry draft):
  registries/exit_events.csv     ghosts and living-brand controls: legal date, brand-retirement date, sources
  registries/model_cutoffs.csv   vendor-published knowledge cutoffs and lifecycle status
  registries/aliases_current.csv brand names and aliases for current brands (coding list, draft)
  registries/airline_scan_class.csv  brand vs regional classification for the T-100 exit scan
  registries/bank_scan_class.csv     class and reason for every SOD exit-scan candidate (>= 0.4%)
  registries/draft_template.md       registry draft text; `build` writes <out>/v0_40_registry_draft.md from it

Usage (paths resolve from the folder above scripts/, i.e. osf/v40):
  python3 osf/v40/scripts/build_registry_v0_40.py fetch t100 2007 2026
  python3 osf/v40/scripts/build_registry_v0_40.py fetch ontime 2025-08 2026-07
  python3 osf/v40/scripts/build_registry_v0_40.py fetch sod 2005 2026
  python3 osf/v40/scripts/build_registry_v0_40.py build --freeze 2026-11-08 [--status-check]
      [--registry-dir registries] [--data-dir data/raw] [--out registries/out]

No number in the outputs is typed by hand: shares, coverage, window membership, floor tests and
exit-to-cutoff gaps are all computed here. Dates come only from registries/exit_events.csv.
"""
import argparse, csv, glob, hashlib, json, re, sys, time, zipfile
import datetime as dt
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]

# ----------------------------------------------------------------------------------------------
# Rules (registry draft section 2)
# ----------------------------------------------------------------------------------------------
FLOOR_PCT = 0.5                                  # R3: inclusion floor, share of national total
WINDOW_START = pd.Timestamp("2008-01-01")        # R4: ghost window opens; closes at --freeze
CUSTODY = ("BANK OF NEW YORK MELLON", "NORTHERN TRUST", "STATE STREET")
# R9: EGRRCPA s.402 / 2019 SLR final rule "currently applies to only three institutions"
#     (FDIC fact sheet https://www.fdic.gov/news/fact-sheets/slr.pdf)
AIRLINE_HOLDER = {"HA": "AS"}                    # R8: Hawaiian folded into Alaska (T-100 reports HA inside AS from 2026-01)
AIRLINE_HOLDER_ALT = {"HA": "AS", "SY": "G4"}    # holding-company view: Allegiant owns Sun Country since 2026-05-13
AIRLINE_BRANDS = {"AA": "American Airlines", "DL": "Delta Air Lines", "UA": "United Airlines",
                  "WN": "Southwest Airlines", "AS": "Alaska Airlines", "HA": "Hawaiian Airlines",
                  "B6": "JetBlue", "F9": "Frontier Airlines", "G4": "Allegiant Air", "SY": "Sun Country Airlines",
                  "MX": "Breeze Airways", "NK": "Spirit Airlines"}
DAYS_PER_MONTH = 30.4375

# ----------------------------------------------------------------------------------------------
# Fetchers
# ----------------------------------------------------------------------------------------------
T100_URL = "https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FIM&QO_fu146_anzr=Nv4%20Pn44vr45"
T100_FIELDS = ["YEAR", "MONTH", "UNIQUE_CARRIER", "UNIQUE_CARRIER_NAME", "CLASS", "PASSENGERS", "DISTANCE"]
ONTIME_URL = ("https://transtats.bts.gov/PREZIP/"
              "On_Time_Marketing_Carrier_On_Time_Performance_Beginning_January_2018_{y}_{m}.zip")
SOD_API = "https://api.fdic.gov/banks/sod"
SOD_FIELDS = ["YEAR", "CERT", "NAMEFULL", "RSSDID", "RSSDHCR", "NAMEHCR", "DEPSUMBR", "BRSERTYP", "BKCLASS",
              "STALPBR", "UNINUMBR"]
HIST_API = "https://api.fdic.gov/banks/history"
FAIL_API = "https://api.fdic.gov/banks/failures"
UA = {"User-Agent": "AIAS-registry-builder/0.40 (research data download)"}


def _hidden(html, name):
    m = (re.search(r'name="%s"[^>]*value="([^"]*)"' % re.escape(name), html)
         or re.search(r'id="%s"[^>]*value="([^"]*)"' % re.escape(name), html))
    return m.group(1) if m else ""


def fetch_t100(year, outdir):
    outdir = Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    s = requests.Session(); s.headers.update(UA)
    page = s.get(T100_URL, timeout=120).text
    data = {k: _hidden(page, k) for k in ["__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTVALIDATION"]}
    data.update({"cboGeography": "All", "cboYear": str(year), "cboPeriod": "All", "chkDownloadZip": "on",
                 "btnDownload": "Download"})
    data.update({f: "on" for f in T100_FIELDS})
    r = s.post(T100_URL, data=data, timeout=600)
    out = outdir / f"T100D_SEGMENT_US_{year}.zip"
    if r.content[:2] == b"PK":
        out.write_bytes(r.content); return out
    m = re.search(r'href="([^"]+\.zip)"', r.text, re.I)
    if m:
        out.write_bytes(s.get(requests.compat.urljoin(T100_URL, m.group(1)), timeout=600).content); return out
    raise RuntimeError(f"T-100 {year}: no zip returned (HTTP {r.status_code})")


def fetch_ontime(year, month, outdir):
    outdir = Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    url = ONTIME_URL.format(y=year, m=month)
    r = requests.get(url, headers=UA, timeout=600); r.raise_for_status()
    out = outdir / url.rsplit("/", 1)[1]; out.write_bytes(r.content); return out


def fetch_sod(year, outdir, page=10000):
    outdir = Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    rows, offset = [], 0
    while True:
        params = {"filters": f"YEAR:{year}", "fields": ",".join(SOD_FIELDS), "limit": page, "offset": offset,
                  "sort_by": "UNINUMBR", "sort_order": "ASC", "format": "json"}
        r = requests.get(SOD_API, params=params, headers=UA, timeout=180); r.raise_for_status()
        j = r.json(); batch = [d["data"] for d in j["data"]]
        rows += batch; offset += page
        if offset >= j["meta"]["total"] or not batch: break
        time.sleep(0.3)
    out = outdir / f"sod_{year}.csv.gz"; pd.DataFrame(rows).to_csv(out, index=False); return out


def fdic_history(filters, limit=500):
    params = {"filters": filters, "limit": limit, "sort_by": "EFFDATE", "sort_order": "ASC"}
    r = requests.get(HIST_API, params=params, headers=UA, timeout=120); r.raise_for_status()
    return pd.DataFrame([d["data"] for d in r.json()["data"]])

# ----------------------------------------------------------------------------------------------
# Loaders
# ----------------------------------------------------------------------------------------------
def load_t100(rawdir):
    frames = []
    for p in sorted(glob.glob(f"{rawdir}/T100D_SEGMENT_US_*.zip")):
        with zipfile.ZipFile(p) as z:
            frames.append(pd.read_csv(z.open("T_T100D_SEGMENT_US_CARRIER_ONLY.csv")))
    df = pd.concat(frames, ignore_index=True)
    df = df[df.CLASS == "F"].copy()
    df["RPM"] = df.PASSENGERS * df.DISTANCE
    df["ym"] = df.YEAR * 100 + df.MONTH
    m = df.groupby(["ym", "UNIQUE_CARRIER"]).RPM.sum().unstack(fill_value=0.0).sort_index()
    names = df.groupby("UNIQUE_CARRIER").UNIQUE_CARRIER_NAME.agg(lambda s: s.mode().iat[0])
    return m, names


def load_ontime(rawdir):
    cols = ["Year", "Month", "Marketing_Airline_Network", "Operating_Airline ", "Cancelled", "Distance"]
    parts, files = [], sorted(glob.glob(f"{rawdir}/*.zip"))
    for p in files:
        with zipfile.ZipFile(p) as z:
            n = [x for x in z.namelist() if x.endswith(".csv")][0]
            parts.append(pd.read_csv(z.open(n), usecols=cols, low_memory=False))
    df = pd.concat(parts, ignore_index=True).rename(columns={"Operating_Airline ": "Operating_Airline"})
    return df, files


def load_sod(year, rawdir, _cache={}):
    if year in _cache: return _cache[year]
    df = pd.read_csv(f"{rawdir}/sod_{year}.csv.gz", low_memory=False)
    df["DEPSUMBR"] = pd.to_numeric(df["DEPSUMBR"], errors="coerce").fillna(0)
    hc = pd.to_numeric(df["RSSDHCR"], errors="coerce").fillna(0).astype(int)
    own = pd.to_numeric(df["RSSDID"], errors="coerce").fillna(0).astype(int)
    df["HOLDER"] = hc.where(hc > 0, own)
    nm = df["NAMEHCR"].where(hc > 0, df["NAMEFULL"])
    df["HOLDER_NAME"] = nm.where(nm.notna() & (nm.astype(str).str.strip() != ""), df["NAMEFULL"])
    df["CERT"] = pd.to_numeric(df["CERT"], errors="coerce").astype(int)
    _cache[year] = df
    return df


def sod_years(rawdir):
    return sorted(int(re.search(r"sod_(\d{4})", p).group(1)) for p in glob.glob(f"{rawdir}/sod_[0-9][0-9][0-9][0-9].csv.gz"))

# ----------------------------------------------------------------------------------------------
# Airline computations
# ----------------------------------------------------------------------------------------------
def ym_label(ym):
    return f"{ym // 100}-{ym % 100:02d}"


def airline_current(m, ontime, holder_map):
    """Brand shares over the latest 12 T-100 months. Regional operators (never marketed under their own
    code in the On-Time Marketing Carrier file) are allocated to marketing brands by flight-miles."""
    W = list(m.index[-12:])
    rpm = m.loc[W].sum()
    total = rpm.sum()
    d = ontime[ontime.Cancelled == 0]
    fm = d.groupby(["Operating_Airline", "Marketing_Airline_Network"]).Distance.sum()
    frac = (fm / fm.groupby(level=0).transform("sum")).rename("frac").reset_index()
    frac.columns = ["op", "mkt", "frac"]
    own = frac[frac.op == frac.mkt].set_index("op").frac
    regional = sorted(o for o in frac.op.unique() if own.get(o, 0.0) == 0.0)
    brand = rpm.drop([c for c in regional if c in rpm.index]).astype(float)
    alloc_rows = []
    for o in regional:
        if o not in rpm.index: continue
        for r in frac[frac.op == o].itertuples():
            brand[r.mkt] = brand.get(r.mkt, 0.0) + rpm[o] * r.frac
            alloc_rows.append(dict(operator=o, operator_name="", brand=r.mkt, flight_mile_share=round(r.frac, 4),
                                   rpm_allocated=rpm[o] * r.frac))
    ontime_months = sorted(set(zip(ontime.Year, ontime.Month)))
    t100_months = [(w // 100, w % 100) for w in W]
    coverage_ok = ontime_months == t100_months
    out = pd.DataFrame({"code": brand.index, "brand_rpm": brand.values})
    out["brand_share_pct"] = 100 * out.brand_rpm / total
    out["operating_share_pct"] = [100 * rpm.get(c, 0.0) / total for c in out.code]
    out["reports_latest_month"] = [bool(m.loc[W[-1]].get(c, 0) > 0) for c in out.code]
    out["holder"] = [holder_map.get(c, c) for c in out.code]
    hold = out.groupby("holder").brand_rpm.sum()
    out["holder_share_pct"] = [100 * hold[h] / total for h in out.holder]
    reg_share = 100 * sum(rpm.get(o, 0.0) for o in regional) / total
    meta = dict(window=f"{ym_label(W[0])}..{ym_label(W[-1])}", total_rpm=float(total), regional_ops=regional,
                regional_share_pct=reg_share, ontime_months_match_t100=coverage_ok,
                ontime_months=[f"{y}-{mm:02d}" for y, mm in ontime_months])
    return out.sort_values("brand_share_pct", ascending=False), pd.DataFrame(alloc_rows), meta


def airline_scan(m, names, min_share=0.2):
    """Every T-100 carrier that stopped reporting before the latest month, with its share over its
    last 12 reporting months (operating-carrier basis)."""
    tot = m.sum(axis=1); idx = list(m.index); latest = idx[-1]; rows = []
    for c in m.columns:
        nz = m[c][m[c] > 0]
        if nz.empty: continue
        li = idx.index(nz.index.max()); win = idx[max(0, li - 11): li + 1]
        share = 100 * m.loc[win, c].sum() / tot.loc[win].sum()
        rows.append(dict(code=c, name=names.get(c, ""), first=ym_label(nz.index.min()), last=ym_label(nz.index.max()),
                         share_last12_pct=share, stopped=nz.index.max() < latest))
    s = pd.DataFrame(rows)
    return s[s.stopped & (s.share_last12_pct >= min_share)].sort_values("last").drop(columns="stopped")


def airline_unit_share(m, codes):
    tot = m.sum(axis=1); idx = list(m.index)
    col = sum(m[c] for c in codes if c in m.columns)
    nz = col[col > 0]
    li = idx.index(nz.index.max()); win = idx[max(0, li - 11): li + 1]
    return 100 * col.loc[win].sum() / tot.loc[win].sum(), ym_label(win[0]), ym_label(win[-1])

# ----------------------------------------------------------------------------------------------
# Bank computations
# ----------------------------------------------------------------------------------------------
def bank_current(sod, aliases):
    total = sod.DEPSUMBR.sum()
    g = sod.groupby("HOLDER").agg(deposits_k=("DEPSUMBR", "sum"),
                                  holder_name=("HOLDER_NAME", lambda s: s.mode().iat[0]),
                                  certs=("CERT", lambda s: "|".join(map(str, sorted(set(s))))),
                                  offices=("UNINUMBR", "nunique")).reset_index()
    g["share_pct"] = 100 * g.deposits_k / total
    g["custody_rule"] = g.holder_name.str.upper().str.contains("|".join(CUSTODY))
    g = g.sort_values("share_pct", ascending=False)
    al = aliases[aliases.category == "bank"].set_index("unit")
    g["brand"] = [al.brand.get(str(h), "") for h in g.HOLDER]
    g["aliases"] = [al.aliases.get(str(h), "") for h in g.HOLDER]
    return g, total


def bank_unit_share(rawdir, years, certs, main, stem):
    """Share at the last SOD under the old identity: last year in which the main charter is present and its
    legal name still carries the stem. Sums every listed charter carrying the stem that year (rule R6) and
    sweeps for same-holder charters with the stem that are not listed."""
    st = stem.lower(); last = None
    for y in years:
        d = load_sod(y, rawdir)
        nm = d.loc[d.CERT == main, "NAMEFULL"]
        if not nm.empty and nm.astype(str).str.lower().str.contains(st, regex=False).any():
            last = y
    if last is None:
        return dict(sod_year=None)
    d = load_sod(last, rawdir); tot = d.DEPSUMBR.sum()
    has = d.NAMEFULL.astype(str).str.lower().str.contains(st, regex=False)
    listed = d[d.CERT.isin(certs) & has]
    main_holder = d.loc[d.CERT == main, "HOLDER"].mode().iat[0]
    sweep = d[has & (d.HOLDER == main_holder) & ~d.CERT.isin(certs)]
    names = listed.groupby("CERT").NAMEFULL.agg(lambda s: s.mode().iat[0])
    return dict(sod_year=last, share_pct=100 * listed.DEPSUMBR.sum() / tot,
                share_main_pct=100 * d.loc[d.CERT == main, "DEPSUMBR"].sum() / tot,
                legal_names="; ".join(f"{c}: {n}" for c, n in names.items()),
                sweep_unlisted="; ".join(sorted(set(f"{r.CERT}: {r.NAMEFULL}" for r in sweep.itertuples()))))


def bank_scan(rawdir, years, min_share=0.4):
    """Mechanical scan of the SOD panel: (a) renames, i.e. a charter's legal name changes between consecutive
    SOD years; (b) exits, i.e. a charter's last SOD year is before the latest. Share at the last SOD under the
    old identity."""
    rows, panel = [], []
    for y in years:
        d = load_sod(y, rawdir); tot = d.DEPSUMBR.sum()
        g = d.groupby("CERT").agg(name=("NAMEFULL", lambda s: s.mode().iat[0]), dep=("DEPSUMBR", "sum"),
                                  holder=("HOLDER_NAME", lambda s: s.mode().iat[0])).reset_index()
        g["year"] = y; g["share_pct"] = 100 * g.dep / tot; panel.append(g)
    p = pd.concat(panel, ignore_index=True); latest = years[-1]
    for cert, g in p.sort_values("year").groupby("CERT"):
        g = g.reset_index(drop=True)
        for i in range(1, len(g)):
            if (str(g.loc[i, "name"]).strip().lower() != str(g.loc[i - 1, "name"]).strip().lower()
                    and g.loc[i, "year"] == g.loc[i - 1, "year"] + 1):
                r = g.loc[i - 1]
                rows.append(dict(type="rename", cert=int(cert), old_name=r["name"], new_name=g.loc[i, "name"],
                                 last_sod_old=int(r.year), share_pct=r.share_pct, holder=r.holder))
        last = g.iloc[-1]
        if last.year < latest:
            rows.append(dict(type="exit", cert=int(cert), old_name=last["name"], new_name="", last_sod_old=int(last.year),
                             share_pct=last.share_pct, holder=last.holder))
    s = pd.DataFrame(rows)
    return s[s.share_pct >= min_share].sort_values(["last_sod_old", "share_pct"], ascending=[True, False])


def status_check(sod, holders, after, cache):
    """FDIC /history events after the SOD date for every charter of the current holders (primary status check)."""
    rows = []
    certs = sorted(set(int(c) for h in holders for c in sod.loc[sod.HOLDER == h, "CERT"].unique()))
    if Path(cache).exists():                     # reuse a same-day check; delete the file to re-query
        return pd.read_csv(cache), len(certs)
    for c in certs:
        for flt in (f"CERT:{c}", f"OUT_CERT:{c}"):
            try:
                e = fdic_history(flt)
            except Exception as ex:
                rows.append(dict(cert=c, query=flt, error=str(ex)[:120])); continue
            if e.empty: continue
            e = e[pd.to_datetime(e.EFFDATE, errors="coerce") > pd.Timestamp(after)]
            for r in e.itertuples():
                rows.append(dict(cert=c, query=flt, effdate=str(r.EFFDATE)[:10], changecode=getattr(r, "CHANGECODE", ""),
                                 change=getattr(r, "CHANGECODE_DESC", ""), inst=getattr(r, "INSTNAME", ""),
                                 frm=getattr(r, "FRM_INSTNAME", ""), out=getattr(r, "OUT_INSTNAME", ""),
                                 sur=getattr(r, "SUR_INSTNAME", "")))
            time.sleep(0.15)
    df = pd.DataFrame(rows, columns=["cert", "query", "effdate", "changecode", "change", "inst", "frm", "out", "sur", "error"])
    df.to_csv(cache, index=False)
    return df, len(certs)

# ----------------------------------------------------------------------------------------------
# Dates and gaps
# ----------------------------------------------------------------------------------------------
def cutoff_date(s):
    """'YYYY-MM' -> last day of that month (vendor says 'knowledge through <month>'); 'YYYY-MM-DD' -> as given."""
    s = str(s).strip()
    if not s or s == "nan": return pd.NaT
    if re.fullmatch(r"\d{4}-\d{2}", s): return pd.Timestamp(s + "-01") + pd.offsets.MonthEnd(0)
    return pd.Timestamp(s)


def gap_months(cut, exit_date):
    if pd.isna(cut) or pd.isna(exit_date): return None
    return round((cut - exit_date).days / DAYS_PER_MONTH, 1)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]

# ----------------------------------------------------------------------------------------------
# Build
# ----------------------------------------------------------------------------------------------
def build(args):
    reg = ROOT / args.registry_dir; raw = ROOT / args.data_dir; out = ROOT / args.out; out.mkdir(parents=True, exist_ok=True)
    freeze = pd.Timestamp(args.freeze)
    ev = pd.read_csv(reg / "exit_events.csv", dtype=str).fillna("")
    cut = pd.read_csv(reg / "model_cutoffs.csv", dtype=str).fillna("")
    aliases = pd.read_csv(reg / "aliases_current.csv", dtype=str).fillna("")
    scan_class = pd.read_csv(reg / "airline_scan_class.csv", dtype=str).fillna("")

    # ---- airlines
    m, names = load_t100(raw / "bts")
    ontime, ontime_files = load_ontime(raw / "bts" / "ontime_mkt")
    air, alloc, ameta = airline_current(m, ontime, AIRLINE_HOLDER)
    air_alt, _, _ = airline_current(m, ontime, AIRLINE_HOLDER_ALT)
    air["name"] = [AIRLINE_BRANDS.get(c, names.get(c, "")) for c in air.code]
    air["holder_share_alt_pct"] = air_alt.set_index("code").holder_share_pct.reindex(air.code).values
    alloc["operator_name"] = [names.get(o, "") for o in alloc.operator]
    living_controls = set(ev[(ev.category == "airline") & (ev.role == "control")].id)
    ghosts_air = set(ev[(ev.category == "airline") & (ev.role == "ghost")].id)
    air["in_registry"] = [(c not in ghosts_air) and (r.brand_share_pct >= FLOOR_PCT) and (r.reports_latest_month or c in living_controls)
                          for c, r in zip(air.code, air.itertuples())]
    air_cur = air[air.in_registry].copy()
    al_air = aliases[aliases.category == "airline"].set_index("unit")
    air_cur["aliases"] = [al_air.aliases.get(c, "") for c in air_cur.code]
    air_cur["status"] = ["living control (brand retained, ownership/legal change)" if c in living_controls else "current"
                         for c in air_cur.code]
    scan = airline_scan(m, names).merge(scan_class[["code", "class", "basis"]], on="code", how="left")

    # ---- banks
    years = sod_years(raw / "fdic"); latest = years[-1]
    sod = load_sod(latest, raw / "fdic")
    bk, bank_total = bank_current(sod, aliases)
    bk["in_registry"] = (bk.share_pct >= FLOOR_PCT) & ~bk.custody_rule
    bk_cur = bk[bk.in_registry].copy()
    custody_excl = bk[(bk.share_pct >= FLOOR_PCT) & bk.custody_rule]
    near_floor = bk[(bk.share_pct < FLOOR_PCT) & (bk.share_pct >= 0.4)]
    bclass = pd.read_csv(reg / "bank_scan_class.csv")
    bscan = bank_scan(raw / "fdic", years).merge(bclass, on=["type", "cert", "last_sod_old"], how="left")
    bscan["class"] = bscan["class"].fillna("UNCLASSIFIED")

    # ---- events: shares, window, floor
    rows = []
    for r in ev.itertuples():
        units = [u for u in r.units.split("|") if u]
        brand_d = pd.Timestamp(r.brand_date) if r.brand_date else pd.NaT
        legal_d = pd.Timestamp(r.legal_date) if r.legal_date else pd.NaT
        rec = dict(category=r.category, role=r.role, id=r.id, brand=r.brand, aliases=r.aliases, successor=r.successor,
                   exit_type=r.exit_type, legal_date=r.legal_date, brand_date=r.brand_date)
        if r.category == "airline":
            sh, w0, w1 = airline_unit_share(m, units)
            rec.update(share_pct=sh, share_basis=f"T-100 RPM, operating carrier, {w0}..{w1}", units=r.units)
        else:
            b = bank_unit_share(raw / "fdic", years, [int(u) for u in units], int(r.main_unit), r.stem)
            rec.update(share_pct=b.get("share_pct"), share_basis=f"SOD {b.get('sod_year')} deposits, charters {r.units}",
                       share_main_pct=b.get("share_main_pct"), legal_names=b.get("legal_names", ""),
                       sweep_unlisted=b.get("sweep_unlisted", ""), units=r.units)
        rec["passes_floor"] = rec.get("share_pct") is not None and rec["share_pct"] >= FLOOR_PCT
        rec["in_window_brand"] = bool(pd.notna(brand_d) and WINDOW_START <= brand_d <= freeze)
        rec["in_window_legal"] = bool(pd.notna(legal_d) and WINDOW_START <= legal_d <= freeze)
        rec["brand_before_legal"] = bool(pd.notna(brand_d) and pd.notna(legal_d) and brand_d < legal_d)
        rec["legal_source_type"] = r.legal_source_type; rec["brand_source_type"] = r.brand_source_type
        rec["legal_source"] = r.legal_source; rec["brand_source"] = r.brand_source; rec["notes"] = r.notes
        rows.append(rec)
    E = pd.DataFrame(rows)
    E["in_registry"] = (E.role == "control") | (E.passes_floor & E.in_window_brand)

    # ---- gaps: ghost x model
    G = []
    for g in E[(E.role == "ghost") & E.in_registry].itertuples():
        bd = pd.Timestamp(g.brand_date); ld = pd.Timestamp(g.legal_date)
        for c in cut.itertuples():
            cp, ca = cutoff_date(c.cutoff_primary), cutoff_date(c.cutoff_alt)
            G.append(dict(category=g.category, ghost=g.id, brand=g.brand, model=c.model, arm=c.arm,
                          cutoff_primary=c.cutoff_primary, gap_brand_m=gap_months(cp, bd), gap_legal_m=gap_months(cp, ld),
                          cutoff_alt=c.cutoff_alt, gap_brand_alt_m=gap_months(ca, bd)))
    G = pd.DataFrame(G)

    # ---- status check (network, optional)
    status = None
    if args.status_check:
        status, ncerts = status_check(sod, list(bk_cur.HOLDER), f"{latest}-06-30",
                                      raw / "fdic" / f"status_check_{args.freeze}.csv")

    # ---- write
    air_cur.to_csv(out / "airlines_current.csv", index=False, float_format="%.4f")
    alloc.to_csv(out / "airline_regional_allocation.csv", index=False, float_format="%.4f")
    scan.to_csv(out / "airline_exit_scan.csv", index=False, float_format="%.4f")
    bscan.to_csv(out / "bank_exit_scan.csv", index=False, float_format="%.4f")
    bk_cur.to_csv(out / "banks_current.csv", index=False, float_format="%.4f")
    E.to_csv(out / "exits_and_controls.csv", index=False, float_format="%.4f")
    G.to_csv(out / "exit_cutoff_gaps.csv", index=False)
    cut.to_csv(out / "model_cutoffs.csv", index=False)

    man = dict(builder="build_registry_v0_40.py", run_utc=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
               freeze=args.freeze, floor_pct=FLOOR_PCT, window_start=str(WINDOW_START.date()),
               t100_months=f"{ym_label(m.index[0])}..{ym_label(m.index[-1])}", airline_window=ameta["window"],
               ontime_files=[Path(p).name for p in ontime_files], ontime_months_match_t100=ameta["ontime_months_match_t100"],
               regional_operators=ameta["regional_ops"], regional_share_pct=round(ameta["regional_share_pct"], 3),
               sod_years=f"{years[0]}..{latest}", sod_total_deposits_tn=round(bank_total / 1e9, 3),
               counts=dict(airline_brands=int(len(air_cur)), airline_holders=int(air_cur.holder.nunique()),
                           airline_ghosts=int(((E.category == "airline") & (E.role == "ghost") & E.in_registry).sum()),
                           bank_holders=int(len(bk_cur)),
                           bank_ghosts=int(((E.category == "bank") & (E.role == "ghost") & E.in_registry).sum()),
                           controls=int((E.role == "control").sum())),
               inputs={p: sha(reg / p) for p in ["exit_events.csv", "model_cutoffs.csv", "aliases_current.csv", "airline_scan_class.csv",
                                                 "bank_scan_class.csv"]},
               bank_scan_unclassified=int((bscan["class"] == "UNCLASSIFIED").sum()),
               scan_ghosts_match_events=dict(
                   airline=sorted(scan.loc[scan["class"].eq("brand") & scan.basis.str.startswith("Ghost"), "code"]) ==
                           sorted(E.loc[(E.category == "airline") & (E.role == "ghost"), "id"]),
                   bank=sorted(set(bscan.loc[bscan["class"].eq("ghost"), "reason"].str.split().str[0])) ==
                        sorted(E.loc[(E.category == "bank") & (E.role == "ghost"), "id"])),
               status_check=None if status is None else dict(charters=ncerts, events_after_sod=int(status.effdate.notna().sum()),
                                                             errors=int(status.error.notna().sum())))
    (out / "build_manifest.json").write_text(json.dumps(man, indent=2))
    write_tables(out, air_cur, ameta, scan, bk_cur, custody_excl, near_floor, E, G, cut, status, man, bscan)
    write_draft(reg, out)
    print(json.dumps(man, indent=2))


def md_table(df, cols, heads, fmt=None):
    fmt = fmt or {}
    lines = ["| " + " | ".join(heads) + " |", "|" + "|".join("---" for _ in heads) + "|"]
    for r in df.to_dict("records"):
        vals = []
        for c in cols:
            v = r.get(c)
            if c in fmt and v is not None and not (isinstance(v, float) and pd.isna(v)): v = fmt[c].format(v)
            vals.append("" if v is None or (isinstance(v, float) and pd.isna(v)) else str(v).replace("|", ", "))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def write_tables(out, air_cur, ameta, scan, bk_cur, custody_excl, near_floor, E, G, cut, status, man, bscan):
    p2 = {"brand_share_pct": "{:.2f}", "operating_share_pct": "{:.2f}", "holder_share_pct": "{:.2f}",
          "holder_share_alt_pct": "{:.2f}", "share_pct": "{:.3f}", "share_last12_pct": "{:.3f}", "share_main_pct": "{:.3f}"}
    s = [f"<!-- generated by build_registry_v0_40.py at {man['run_utc']} UTC; do not edit by hand -->\n"]
    s.append(f"### Airlines: current brands (window {ameta['window']})\n")
    s.append(md_table(air_cur, ["code", "name", "brand_share_pct", "operating_share_pct", "holder", "holder_share_pct",
                                "holder_share_alt_pct", "status"],
                      ["Code", "Brand", "Brand share %", "Operating share %", "Holder", "Holder share %",
                       "Holder share % (SY in G4)", "Status"], p2))
    s.append(f"\nRegional operators allocated: {', '.join(ameta['regional_ops'])} "
             f"({ameta['regional_share_pct']:.2f}% of RPM). On-Time months match T-100 window: {ameta['ontime_months_match_t100']}. "
             "Hawaiian's brand share covers 2025-08 to 2025-12 only, because T-100 reports it inside Alaska from 2026-01; "
             "use the holder share. The last column puts Sun Country inside Allegiant (sensitivity, D2).\n")
    s.append("\n### Airlines: T-100 exit scan (stopped reporting, share >= 0.2% in last 12 months)\n")
    s.append(md_table(scan, ["code", "name", "first", "last", "share_last12_pct", "class", "basis"],
                      ["Code", "Carrier", "First", "Last", "Share % (last 12 mo)", "Class", "Basis"], p2))
    s.append(f"\n### Banks: current holders (SOD {man['sod_years'][-4:]}, total deposits ${man['sod_total_deposits_tn']}tn)\n")
    s.append(md_table(bk_cur, ["holder_name", "brand", "share_pct", "offices", "certs"],
                      ["Holder (FDIC)", "Brand", "Share %", "Offices", "Charters (CERT)"], p2))
    s.append("\nExcluded by the custody rule (R9): " + "; ".join(f"{r.holder_name} {r.share_pct:.3f}%" for r in custody_excl.itertuples()) + ".\n")
    s.append("\nJust under the floor (0.40-0.50%): " + "; ".join(f"{r.holder_name} {r.share_pct:.3f}%" for r in near_floor.itertuples()) + ".\n")
    s.append("\n### Banks: SOD exit scan (renames and exits, share >= 0.4% at the last SOD under the old identity)\n")
    s.append(md_table(bscan, ["type", "cert", "old_name", "new_name", "last_sod_old", "share_pct", "class", "reason"],
                      ["Type", "CERT", "Old legal name", "New legal name", "Last SOD", "Share %", "Class", "Reason / ghost ID"], p2))
    for cat in ["airline", "bank"]:
        g = E[(E.category == cat) & (E.role == "ghost")]
        s.append(f"\n### {cat.title()} ghosts\n")
        s.append(md_table(g, ["id", "brand", "share_pct", "legal_date", "brand_date", "successor", "brand_source_type", "in_registry"],
                          ["ID", "Brand", "Share %", "Legal date", "Brand-retirement date", "Successor", "Brand-date source", "In registry"], p2))
    s.append("\n### Living-brand controls\n")
    s.append(md_table(E[E.role == "control"], ["category", "id", "brand", "share_pct", "legal_date", "successor"],
                      ["Category", "ID", "Brand", "Share % (last separate count)", "Legal/ownership date", "Owner now"], p2))
    s.append("\n### Model cutoffs (vendor pages, retrieved 2026-11-08)\n")
    s.append(md_table(cut, ["arm", "model", "api_id", "cutoff_primary_label", "cutoff_primary", "cutoff_alt", "lifecycle"],
                      ["Arm", "Model", "API ID", "Primary cutoff", "Date", "Alt (reliable)", "Lifecycle"]))
    if not G.empty:
        piv = G.pivot_table(index=["category", "ghost"], columns="model", values="gap_brand_m", sort=False).reset_index()
        order = list(cut.model)
        piv = piv[["category", "ghost"] + [c for c in order if c in piv.columns]]
        s.append("\n### Exit-to-cutoff gap, months (model cutoff minus brand-retirement date; negative = exit after cutoff)\n")
        s.append(md_table(piv, list(piv.columns), list(piv.columns)))
        neg = G[G.gap_brand_m < 0]
        s.append(f"\nGhost x model pairs with the exit after the cutoff (brand date): {len(neg)} of {len(G)}.\n")
    s.append("\n### Sources by row (from registries/exit_events.csv and registries/model_cutoffs.csv)\n")
    for r in E.to_dict("records"):
        s.append(f"- **{r['id']} {r['brand']}** ({r['role']}). Legal {r['legal_date']} [{r['legal_source_type']}]: {r['legal_source']}"
                 + (f" Brand {r['brand_date']} [{r['brand_source_type']}]: {r['brand_source']}" if r['brand_date'] else
                    f" Brand retained [{r['brand_source_type']}]: {r['brand_source']}"))
    for r in cut.to_dict("records"):
        s.append(f"- **{r['model']}** cutoff: {r['cutoff_source']}; lifecycle: {r['lifecycle_source']}")
    if status is not None:
        ev_after = status[status.effdate.notna()]
        s.append(f"\n### FDIC status check after the SOD date ({man['status_check']['charters']} charters of the current holders)\n")
        s.append("No structure-change events found.\n" if ev_after.empty else
                 md_table(ev_after, ["cert", "effdate", "changecode", "change", "inst", "frm", "out", "sur"],
                          ["CERT", "Date", "Code", "Change", "Institution", "From", "Out", "Survivor"]))
    (out / "registry_tables.md").write_text("\n".join(s) + "\n")


def write_draft(reg, out):
    """Assemble <out>/v0_40_registry_draft.md: the template with the generated tables in place of {{TABLES}}."""
    tpl = reg / "draft_template.md"
    if not tpl.exists():
        return None
    tables = re.sub(r"(?m)^### ", "#### ", (out / "registry_tables.md").read_text()).rstrip("\n")
    dst = out / "v0_40_registry_draft.md"
    dst.write_text(tpl.read_text().replace("{{TABLES}}", tables))
    return dst


# ----------------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch"); f.add_argument("what", choices=["t100", "ontime", "sod"]); f.add_argument("start"); f.add_argument("end")
    f.add_argument("--data-dir", default="data/raw")
    b = sub.add_parser("build")
    b.add_argument("--freeze", default=dt.date.today().isoformat(), help="registry freeze date (window closes)")
    b.add_argument("--status-check", action="store_true", help="query FDIC /history for post-SOD events (network)")
    b.add_argument("--registry-dir", default="registries"); b.add_argument("--data-dir", default="data/raw")
    b.add_argument("--out", default="registries/out")
    a = ap.parse_args()
    if a.cmd == "build":
        return build(a)
    raw = ROOT / a.data_dir
    if a.what in ("t100", "sod"):
        for y in range(int(a.start), int(a.end) + 1):
            p = fetch_t100(y, raw / "bts") if a.what == "t100" else fetch_sod(y, raw / "fdic")
            print(p); time.sleep(1)
    else:
        y, mth = map(int, a.start.split("-")); y2, m2 = map(int, a.end.split("-"))
        while (y, mth) <= (y2, m2):
            print(fetch_ontime(y, mth, raw / "bts" / "ontime_mkt")); time.sleep(1)
            y, mth = (y + (mth == 12), 1 if mth == 12 else mth + 1)


if __name__ == "__main__":
    main()
