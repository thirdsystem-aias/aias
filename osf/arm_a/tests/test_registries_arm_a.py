#!/usr/bin/env python3
"""Tests for the registries, the pre-lock source record, the inputs builder, the COI screen and fetch_sales_arm_a.py
(fakes only; no request leaves the machine)."""
import csv
import io
import json
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
import build_inputs_arm_a as BI     # noqa: E402
import coi_screen_arm_a as COI      # noqa: E402
import fetch_sales_arm_a as FS      # noqa: E402
import params_arm_a as P            # noqa: E402
import prelock_sources_arm_a as PS  # noqa: E402

PREREG = P.ROOT / "prereg" / "arm_a_seo_prereg_draft_r4.md"


def rows(name):
    with open(P.REG / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class TestDomains(unittest.TestCase):
    def setUp(self):
        self.d = rows("arm_a_domains_r1.csv")

    def test_counts(self):
        self.assertEqual(len(self.d), 76)
        self.assertEqual(len({r["domain"] for r in self.d}), 76)
        self.assertEqual(len({r["brand_id"] for r in self.d}), 72)
        by = {c: sum(r["category"] == c for r in self.d) for c in ("cars", "airlines", "banks", "software", "spirits")}
        self.assertEqual(by, {"cars": 21, "airlines": 11, "banks": 27, "software": 12, "spirits": 5})
        self.assertTrue(all(r["status"] == "RESOLVED" for r in self.d))
        self.assertEqual(sorted(int(r["pull_order"]) for r in self.d), list(range(1, 77)))
        self.assertEqual(sorted(r["row"] for r in self.d), sorted(str(i) for i in range(1, 77)))

    def test_one_primary_per_brand(self):
        prim = [r["brand_id"] for r in self.d if r["role"] == "primary"]
        self.assertEqual(len(prim), 72)
        self.assertEqual(len(set(prim)), 72)
        sens = {r["domain"] for r in self.d if r["role"] == "sensitivity"}
        self.assertEqual(sens, {"mercedes-benz.com", "bmw.com", "jaguar.com", "goldmansachs.com"})

    def test_domains_match_the_preregistration_table(self):
        text = PREREG.read_text(encoding="utf-8")
        table = {}
        for ln in text.splitlines():
            m = re.match(r"\|\s*(\d+)\s*\|(.+)\|", ln)
            if not m or not (1 <= int(m.group(1)) <= 76):
                continue
            cells = [c.strip() for c in ln.strip("|").split("|")]
            doms = [c for c in cells if re.fullmatch(r"[a-z0-9.-]+\.(com|net)", c)]
            if doms:
                table[int(m.group(1))] = doms[0]
        self.assertEqual(len(table), 76)
        for r in self.d:
            self.assertEqual(table[int(r["row"])], r["domain"], r["row"])

    def test_cars_and_spirits_match_v1_13_registry(self):
        raw = subprocess.run(["git", "-C", str(P.ROOT), "show", "a8680f3:osf/methodology/v1_13/registries/"
                              "brand_domains_v1_13.csv"], capture_output=True, check=True).stdout.decode("utf-8")
        v113 = {(r["substrate"], r["brand"]): r["domain"] for r in csv.DictReader(io.StringIO(raw))}
        ours = {r["brand"]: r["domain"] for r in self.d if r["category"] in ("cars", "spirits") and "site" not in r["brand"]}
        found = 0
        for (sub, brand), dom in v113.items():
            if sub in ("v22", "v23") and brand in ours:
                self.assertEqual(ours[brand], dom, brand)
                found += 1
        self.assertEqual(found, 23)

    def test_blind_crosscheck_agrees_with_every_primary(self):
        with open(P.ROOT / "prereg/armA_crosscheck/crosscheck_20261124T133629Z.csv", encoding="utf-8") as f:
            cc = list(csv.DictReader(f))
        self.assertEqual(len(cc), 72)
        self.assertTrue(all(r["rule_outcome"] == "RESOLVED" for r in cc))
        ours = {(r["brand_id"], r["domain"]) for r in self.d}
        for r in cc:
            self.assertIn((r["brand_id"], r["our_primary"]), ours)

    def test_coi_flagged_ids_exist(self):
        ids = {r["brand_id"]: r["brand"] for r in self.d if "site" not in r["brand"]}
        self.assertEqual([ids[b] for b in P.COI_FLAGGED], ["Chevrolet", "BMW", "Bentley", "Jack Daniel's"])


class TestInputs(unittest.TestCase):
    def test_cars_sales_match_shift_group_totals(self):
        t = {}
        for r in rows("arm_a_cars_sales_r1.csv"):
            t[r["group"]] = t.get(r["group"], 0) + int(r["units_2025"]) * int(r["price_usd"])
        self.assertEqual({k: round(v / 1e9, 1) for k, v in t.items()}, {"luxury": 77.3, "mass": 430.4, "electric": 36.9})

    def test_shift_counts_match_the_shift_doc(self):
        s = {r["brand"]: r for r in rows("arm_a_shift_r1.csv")}
        lux = sum(int(r["m_rec"]) for r in s.values() if r["group"] == "luxury")
        self.assertEqual(round(100 * int(s["BMW"]["m_rec"]) / lux), 33)
        self.assertEqual(round(100 * int(s["Mercedes-Benz"]["m_rec"]) / lux), 28)
        self.assertEqual(round(100 * int(s["Porsche"]["m_rec"]) / lux), 39)
        for b in ("Rolls-Royce", "Bentley", "Jaguar", "Cadillac", "Chevrolet"):
            self.assertEqual(s[b]["m_rec"], "0", b)
        self.assertEqual(s["Ford"]["m_rec"], "2")
        mass = sum(int(r["m_rec"]) for r in s.values() if r["group"] == "mass")
        self.assertEqual(round(100 * int(s["Toyota"]["m_rec"]) / mass, 1), 33.3)

    def test_presence_registry_rebuilds_from_locked_sources(self):
        rebuilt = [tuple(str(x) if not isinstance(x, float) else repr(x) for x in r) for r in BI.presence_rows()]
        saved = [(r["category"], r["brand_id"], r["wave"], r["P"], r["source_unit"], r["source"])
                 for r in rows("arm_a_presence_r1.csv")]
        self.assertEqual(len(rebuilt), len(saved))
        for a, b in zip(rebuilt, saved):
            self.assertEqual(a[:3] + a[4:], b[:3] + b[4:])
            self.assertAlmostEqual(float(a[3]), float(b[3]), places=12)

    def test_presence_coverage(self):
        pr = rows("arm_a_presence_r1.csv")
        cnt = {}
        for r in pr:
            cnt[(r["category"], r["wave"])] = cnt.get((r["category"], r["wave"]), 0) + 1
        self.assertEqual(cnt, {("cars", "t1"): 18, ("cars", "t3"): 18, ("cars", "t4"): 18, ("airlines", "v0.40"): 10,
                               ("banks", "v0.40"): 25, ("software", "v0.24"): 12})
        ids = {r["brand_id"] for r in pr}
        self.assertNotIn("BR-00497", ids)          # Hawaiian: inside the Alaska unit in v0.40
        self.assertNotIn("BR-00521", ids)          # Discover: v0.40 living-brand control

    def test_locked_sha_is_enforced(self):
        bad = {k: dict(v) for k, v in BI.SOURCES.items()}
        bad["v41"]["sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            BI.read_locked("v41", bad)

    def test_sales_sources_fixed(self):
        s = rows("arm_a_sales_sources_r1.csv")
        self.assertEqual(len(s), 49)
        st = {r["brand"]: r["status"] for r in s}
        self.assertEqual(st.pop("Discover"), "NO_PRESENCE")
        self.assertTrue(all(v == "FIXED" for v in st.values()), st)
        for r in s:
            if r["category"] == "software":
                self.assertRegex(r["identifier"], r"^accession \d{10}-\d{2}-\d{6}$")
                self.assertLessEqual(r["period"][-10:], "2025-12-31")
        rec = json.loads((P.ARM / "prereg" / "prelock_sources_arm_a.json").read_text())
        self.assertEqual(rec["airlines"]["years"], ["2025"])
        self.assertTrue(all(len(m) == 12 for m in rec["airlines"]["months_by_carrier"].values()))
        self.assertEqual(rec["ecb"]["obs_2025"], 1)
        self.assertNotIn("OBS_VALUE", json.dumps(rec["ecb"]))     # the rate itself is not stored before the lock

    def test_pick_annual(self):
        sub = {"filings": {"recent": {"form": ["10-K", "10-Q", "10-K", "10-K/A"],
                                      "reportDate": ["2024-12-31", "2025-09-30", "2025-12-31", "2025-12-31"],
                                      "filingDate": ["2025-02-01", "2025-10-30", "2026-02-10", "2026-03-01"],
                                      "accessionNumber": ["a1", "q", "a2", "amend"],
                                      "primaryDocument": ["x", "y", "z", "w"]}}}
        self.assertEqual(PS.pick_annual(sub, "10-K")["accessionNumber"], "a2")
        self.assertEqual(PS.pick_annual(sub, "10-K", cutoff="2025-06-30")["accessionNumber"], "a1")
        self.assertIsNone(PS.pick_annual(sub, "20-F"))


class TestFetchSales(unittest.TestCase):
    def test_sec_revenue_rules(self):
        facts = {"facts": {"us-gaap": {"Revenues": {"units": {"USD": [
            {"accn": "A", "start": "2025-10-01", "end": "2025-12-31", "val": 1},          # a quarter: skipped
            {"accn": "B", "start": "2025-01-01", "end": "2025-12-31", "val": 2},          # other filing: skipped
            {"accn": "A", "start": "2025-01-01", "end": "2025-12-31", "val": 3}]}}}}}
        self.assertEqual(FS.sec_revenue(facts, "A", "2025-12-31"), (3.0, "USD", "us-gaap:Revenues"))
        self.assertEqual(FS.sec_revenue(facts, "C", "2025-12-31"), (None, None, None))
        ifrs = {"facts": {"ifrs-full": {"Revenue": {"units": {"EUR": [
            {"accn": "S", "start": "2025-01-01", "end": "2025-12-31", "val": 10}]}}}}}
        self.assertEqual(FS.sec_revenue(ifrs, "S", "2025-12-31"), (10.0, "EUR", "ifrs-full:Revenue"))

    def test_fdic_and_bts(self):
        fake = lambda url: {"data": [{"data": {"CERT": 1, "REPDTE": "20251231", "DEP": 5.5}}]}   # noqa: E731
        self.assertEqual(FS.fdic_deposits(["1", "2"], fake), 11.0)
        with tempfile.TemporaryDirectory() as td:
            z = Path(td) / "t.zip"
            with zipfile.ZipFile(z, "w") as zf:
                zf.writestr("Documentation.csv", "x\n")
                zf.writestr("T.csv", "PASSENGERS,UNIQUE_CARRIER,YEAR,MONTH\n10,AA,2025,1\n5,AA,2025,2\n7,DL,2025,1\n"
                                     "9,AA,2024,12\n")
            import hashlib
            h = hashlib.sha256(z.read_bytes()).hexdigest()
            self.assertEqual(FS.bts_passengers(z, ["AA", "DL"], h), {"AA": 15.0, "DL": 7.0})
            with self.assertRaises(ValueError):
                FS.bts_passengers(z, ["AA"], "0" * 64)

    def test_refuses_before_the_lock(self):
        saved = P.ANCHOR
        P.ANCHOR = Path(tempfile.gettempdir()) / "no_such_anchor_arm_a.json"
        try:
            self.assertEqual(FS.main(fetch=lambda u: (_ for _ in ()).throw(AssertionError("no fetch"))), 2)
        finally:
            P.ANCHOR = saved


QUOTES = [
    ("v0.22-acquisition-locked", "prereg/v0_22_mega_prompt.md", [
        "**Screen result:** Three of the 24 brands in the locked v0.22 registry have tier-2/3 supply relationships with "
        "Samsung Electronics America (author's primary employer) via Samsung subsidiaries: BMW (Harman audio + Samsung "
        "SDI batteries + Samsung Display infotainment), Mercedes-Benz (Harman audio + Samsung Display infotainment), and "
        "Volkswagen Group brands including Bentley and Porsche (Samsung SDI battery supply to Stellantis-adjacent "
        "platforms). Tesla and Polestar also have tangential Samsung-component exposure at the parts level.",
        "These are all tier-2/3 non-competitive supply relationships, not brand-level competition. Samsung Electronics "
        "America does not produce or market passenger car brands. The COI relationship does not affect brand recognition "
        "or recall measurement by LLM panel and does not impose operational restriction on registry composition.",
        "**Disposition:** No deviation from pre-registration warranted. COI disclosed in §COI of the v0.22 SSRN paper per "
        "program standard."]),
    ("de2223c", "papers/v0_22/v0_22_ssrn_paper_draft.md", [
        "Samsung subsidiaries hold tier-2/3 component supply relationships with several brands in the v0.22 registry: "
        "Harman International (audio systems) supplies Mercedes-Benz, BMW, and other premium automotive OEMs; Samsung SDI "
        "(battery cells) supplies BMW (i-series), Volkswagen Group brands including Bentley and Porsche "
        "(Stellantis-adjacent platforms), and others; Samsung Display (infotainment) supplies Mercedes-Benz and BMW. Tesla "
        "and Polestar also have tangential Samsung-component exposure at the parts level. These are non-competitive supply "
        "relationships; Samsung Electronics America does not produce or market passenger car brands and has no "
        "brand-level competitive overlap with any v0.22 registry entry. The COI was screened and documented in DEVIATIONS "
        "Entry 0 (Part B) of the pre-registration module; no operational restriction on registry composition was "
        "imposed."]),
    ("v0.62-prereg-r1", "osf/v62/DEVIATIONS.md", [
        "Tesla and Hyundai (supply) and Hotel Shilla (retail) stay disclosed, not flagged.",
        "**Tesla** — \"Samsung Electronics has entered into a $16.5 billion contract for supplying semiconductors to "
        "Tesla\" (AI6 chips; effective 2025-07-26 to 2033-12-31), larger than the \"tangential\" exposure of v0.22's "
        "record (NBC News, undated page, https://www.nbcnews.com/business/business-news/elon-musk-confirms-tesla-signed-"
        "16point5-billion-chip-contract-samsung-rcna221512); **Hyundai** — Samsung SDI \"has signed its first supply "
        "agreement with Hyundai Motor Co.\", a seven-year battery deal (KED Global, 2023-10-23, "
        "https://www.kedglobal.com/newsView/ked202310230001).",
        "**Cheil Worldwide** made a Chevrolet Spark spot for GM Korea (\"created by Cheil for their client General "
        "Motors\"; credits: agency Cheil Worldwide, client GM Korea), 2017. Cheil lists General Motors among its major "
        "clients. Current status not established.",
        "**Iris** (Iris Culture) retained as \"consumer PR agency for BMW Group, including work across the BMW and MINI "
        "brands in the UK\", 2018. Later status not established.",
        "**Iris** renamed \"Experiential Agency of Record\" of Bentley Motors, Inc. (Americas) \"for the next three "
        "years\", 2021; Bentley is listed among Iris's clients on Iris's agency profile (read 2026-11-11).",
        "**Iris**, \"the Cheil-owned agency\", hired as Jack Daniel's UK digital agency for three years, 2022; later "
        "replaced (\"Iris was the incumbent\" when Five by Five was picked; that page is undated)."]),
]


class TestEntry0Conformed(unittest.TestCase):
    def test_quotes_are_verbatim_in_the_source_records_and_in_entry_0(self):
        entry0 = (P.ARM / "DEVIATIONS.md").read_text(encoding="utf-8")
        for ref, path, snippets in QUOTES:
            src = subprocess.run(["git", "-C", str(P.ROOT), "show", f"{ref}:{path}"], capture_output=True,
                                 check=True).stdout.decode("utf-8")
            for s in snippets:
                self.assertIn(s, src, f"not verbatim in {ref}:{path}: {s[:60]}")
                self.assertIn(s, entry0, f"not in Entry 0: {s[:60]}")


class TestCOIAndSeeds(unittest.TestCase):
    def test_string_screen_finds_terms_whole_word(self):
        hits = COI.screen([("x", "Samsung Pay"), ("x", "Irish Bank"), ("x", "Iris agency")], COI.TERMS + COI.TERMS_R3)
        self.assertIn(("x", "Samsung Pay", "Samsung"), hits)
        self.assertIn(("x", "Iris agency", "Iris"), hits)
        self.assertFalse(any(h[1] == "Irish Bank" for h in hits))
        self.assertEqual(len(COI.TERMS) + len(COI.TERMS_R3), 70)

    def test_seeds_distinct_in_range(self):
        v = list(P.SEEDS.values())
        self.assertEqual(len(v), len(set(v)))
        self.assertTrue(all(610001 <= s <= 610099 for s in v))


if __name__ == "__main__":
    unittest.main()
