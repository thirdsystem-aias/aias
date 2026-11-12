"""Tests of code_v0_62.py (pre-step, answer words, MC_Language) on realistic Spanish, Korean and Chinese answer snippets (r2).
No network, no model. The certified English matchers are stood in for by fake_match, a whole-word, case- and
accent-insensitive matcher on the registry string (the rule of v0.19-v0.22's certified matchers)."""
import csv
import json
import re
import sys
import tempfile
import unicodedata
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import code_v0_62 as C  # noqa: E402

TABLE = HERE.parents[1] / "translations" / "brand_aliases_v0_62_r2.csv"
ROWS = list(csv.DictReader(open(TABLE, encoding="utf-8")))
UNITS = {}
for _r in ROWS:
    UNITS.setdefault(_r["substrate"], []).append(_r["brand"])


def _n(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def fake_match(text, substrate):
    t = _n(text)
    return {b for b in UNITS[substrate] if re.search(r"(?<![a-z0-9])" + re.escape(_n(b)) + r"(?:'s|s')?(?![a-z0-9])", t)}


def p2_reference_codes(text, substrate):
    """Gate P2's reference side: the matchers on the English answer after the same step-1 normalisation
    (typographic apostrophes etc.) that the pre-step applies, so both sides of the comparison are normalised."""
    return fake_match(C.normalise(text), substrate)


def code(text, substrate):
    return fake_match(C.prepare_text(text, substrate), substrate)


KO_HEADPHONES = """오디오파일에게 높은 평가를 받는 헤드폰 브랜드를 몇 가지 소개합니다.

1. **젠하이저(Sennheiser)**: HD 800 S는 해상도로 유명합니다.
2. **오디오 테크니카**의 ATH-ADX5000, **소니**의 MDR-Z1R.
3. 하이파이맨에서는 평판형 모델을 만듭니다. ＨｉＦｉＭａｎ 표기도 있습니다.
※ 코스메틱이나 코스트코와는 관계없지만, 코스의 Porta Pro도 유명합니다."""

ZH_SKINCARE = """以下是几个高端护肤品牌：

- **海蓝之谜（La Mer）**：经典面霜；
- 雅诗兰黛的小棕瓶、兰蔻的小黑瓶；
- 敏感肌可选理肤泉、贝德玛和适乐肤（CeraVe）；
- 肌肤之钥是资生堂旗下的奢华品牌。"""

ES_MAKEUP = "En maquillaje, L’Oréal París y Maybelline dominan el mercado masivo; NARS y M·A·C para profesionales."

ZH_AUTO = """豪华品牌有梅赛德斯-奔驰、ＢＭＷ（宝马）和保时捷。电动车方面有特斯拉和极星；现代汽车的IONIQ 5、
日产和丰田也很重要。大众市场的车型和现代设计、单说奔驰的通称都不计入。"""

KO_AUTO = "현대자동차와 토요타, 메르세데스 벤츠가 대표적입니다. 현대적인 디자인과 벤츠라는 통칭은 세지 않습니다. 재규어의 F-PACE."

ZH_SPIRITS = "尊尼获加、轩尼诗XO、百富和人头马都是代表性品牌。"


class PreStep(unittest.TestCase):
    def test_ko_headphones_snippet_particles(self):
        found = code(KO_HEADPHONES, "v19")
        self.assertEqual(found, {"Sennheiser", "Audio-Technica", "Sony", "HiFiMan", "Koss"})

    def test_ko_koss_not_inside_words(self):
        self.assertEqual(code("코스메틱 브랜드와 코스트코, 디스코스.", "v19"), set())

    def test_zh_skincare_snippet(self):
        self.assertEqual(code(ZH_SKINCARE, "v20"), {"La Mer", "Estée Lauder", "Lancôme", "La Roche-Posay", "Bioderma",
                                                    "CeraVe", "Clé de Peau Beauté"})

    def test_es_makeup_typographic_apostrophe_and_accent(self):
        found = code(ES_MAKEUP, "v21")
        self.assertIn("L'Oréal Paris", found)                 # París: accent stripping in the matcher
        self.assertIn("NARS", found)
        self.assertNotIn("MAC Cosmetics", found)              # English rule needs "MAC Cosmetics" (parity)

    def test_zh_auto_snippet_fullwidth_and_decoys(self):
        found = code(ZH_AUTO, "v22")
        self.assertEqual(found, {"Mercedes-Benz", "BMW", "Porsche", "Tesla", "Polestar", "Hyundai", "Nissan",
                                 "Toyota"})
        self.assertNotIn("Volkswagen", found)                 # 大众市场 is not Volkswagen

    def test_ko_auto_snippet(self):
        self.assertEqual(code(KO_AUTO, "v22"), {"Hyundai", "Toyota", "Mercedes-Benz", "Jaguar"})

    def test_bare_benz_is_not_mercedes(self):
        self.assertEqual(code("奔驰S级很受欢迎。", "v22"), set())
        self.assertEqual(code("벤츠의 S클래스가 인기입니다.", "v22"), set())

    def test_zh_spirits(self):
        self.assertEqual(code(ZH_SPIRITS, "v23"), {"Johnnie Walker", "Hennessy", "The Balvenie", "Rémy Martin"})

    def test_decoys_P4(self):
        for d, sub in (("현대적인", "v22"), ("코스메틱", "v19"), ("로드바이크", "v20"), ("파이널", "v19"), ("엘프", "v21"),
                       ("现代", "v22"), ("大众", "v22"), ("迪奥", "v20"), ("香奈儿", "v20"), ("欧莱雅", "v21"),
                       ("阿玛尼", "v21"), ("奔驰", "v22"), ("벤츠", "v22"), ("디올", "v20"), ("맥", "v21")):
            self.assertEqual(code(f"오늘은 {d} 이야기입니다. 今天说{d}。", sub), set(), d)

    def test_every_alias_reaches_its_unit_P4(self):
        bad = []
        for r in ROWS:
            for a in filter(None, r["ko_aliases"].split("|")):
                for tmpl in ("추천 브랜드는 {}입니다.", "1. **{}**: 대표적", "2위 {}(평점 4.5)", "{}의 제품", "{}, "):
                    got = code(tmpl.format(a), r["substrate"])
                    if got != {r["brand"]}:
                        bad.append((a, tmpl, sorted(got)))
            for a in filter(None, r["zh_aliases"].split("|")):
                for tmpl in ("推荐“{}”的产品。", "1. **{}**：经典", "第2名 {}（评分4.5）", "{}、"):
                    got = code(tmpl.format(a), r["substrate"])
                    if got != {r["brand"]}:
                        bad.append((a, tmpl, sorted(got)))
        self.assertEqual(bad, [])

    def test_mac_korean_alias_r3(self):
        # r3: the brand Korea site's form 맥 코스메틱스 (and the kept r2 transcription 맥 코스메틱) reach MAC Cosmetics
        for t in ("맥 코스메틱스의 립스틱", "추천: 맥 코스메틱스", "**맥 코스메틱스**와 나스", "맥 코스메틱은 인기입니다.",
                  "맥코스메틱스에서는"):
            self.assertIn("MAC Cosmetics", code(t, "v21"), t)
        for t in ("빅맥 코스메틱스", "맥 코스메틱스킨", "맥 립스틱", "맥 코스메틱스타일"):
            self.assertNotIn("MAC Cosmetics", code(t, "v21"), t)
        row = [r for r in ROWS if r["brand"] == "MAC Cosmetics"][0]
        self.assertEqual(row["ko_aliases"], "맥 코스메틱스|맥 코스메틱")
        self.assertEqual(row["ko_check_status"], "PARTLY")
        self.assertIn("https://www.maccosmetics.co.kr/", row["ko_check_source"])

    def test_alias_separator_variants(self):
        self.assertEqual(code("오디오테크니카와 오디오 테크니카", "v19"), {"Audio-Technica"})
        self.assertEqual(code("梅赛德斯·奔驰和梅赛德斯奔驰", "v22"), {"Mercedes-Benz"})

    def test_s_alias_switches_collision_prone_off(self):
        t = C.prepare_text("재규어의 F-PACE", "v22", collision=False)
        self.assertEqual(fake_match(t, "v22"), set())

    def test_english_text_unchanged_P2_shape(self):
        for sub, t in (("v20", "Top picks: La Mer, Estée Lauder and Paula's Choice."),
                       ("v22", "Mercedes-Benz, BMW and Rolls-Royce lead; Benz alone is a nickname."),
                       ("v19", "Sennheiser's HD 800 S and Audio-Technica's ATH-R70x.")):
            self.assertEqual(fake_match(C.prepare_text(t, sub), sub), fake_match(t, sub), t)

    def test_english_curly_apostrophes_P2(self):
        for sub, t, want in (("v20", "Top picks: La Mer and Paula’s Choice.", "Paula's Choice"),
                             ("v21", "Try L’Oréal Paris or e.l.f.", "L'Oréal Paris"),
                             ("v21", "LʼOréal Paris leads.", "L'Oréal Paris")):
            pre = fake_match(C.prepare_text(t, sub), sub)
            raw = p2_reference_codes(t, sub)
            self.assertIn(want, pre, t)
            self.assertEqual(pre, raw, t)

    def test_alias_audit_collects_collision_prone(self):
        hits = []
        C.prepare_text("재규어의 F-PACE와 야생의 재규어.", "v22", hits=hits)
        self.assertEqual(len(hits), 2)
        self.assertTrue(all(h[2] == "재규어" for h in hits))

    def test_strip_urls_copied_byte_for_byte(self):
        src = Path(C.ROOT).parent / "v0.42" / "osf" / "v42" / "scripts" / "code_t4_v0_42.py"
        if not src.exists():
            self.skipTest("v0.42 worktree not present")
        v42 = src.read_text(encoding="utf-8")
        mine = Path(C.__file__).read_text(encoding="utf-8")
        for name in ("MD_LINK_RE = re.compile(", "URL_RE = re.compile(", "def strip_urls(text):"):
            a, b = v42.index(name), mine.index(name)
            block = v42[a:v42.index("\n\n", a)]
            self.assertEqual(block, mine[b:b + len(block)], name)


class AnswerWords(unittest.TestCase):
    def test_es(self):
        self.assertEqual(C.map_answer_words("Sí, Sennheiser es reconocida.", "es"), "Yes, Sennheiser es reconocida.")
        self.assertEqual(C.map_answer_words("**No.** No realmente.", "es"), "**No.** No realmente.")
        self.assertEqual(C.map_answer_words("Si bien es conocida, no.", "es"), "Si bien es conocida, no.")
        self.assertEqual(C.map_answer_words("Si, es reconocida.", "es"), "Yes, es reconocida.")
        self.assertEqual(C.map_answer_words("Sin duda, sí.", "es"), "Sin duda, sí.")

    def test_ko(self):
        self.assertEqual(C.map_answer_words("네, 소니는 널리 인식됩니다.", "ko"), "Yes, 소니는 널리 인식됩니다.")
        self.assertEqual(C.map_answer_words("아니요. 그렇지 않습니다.", "ko"), "No. 그렇지 않습니다.")
        self.assertEqual(C.map_answer_words("**예**", "ko"), "**Yes**")
        self.assertEqual(C.map_answer_words("네이버에서는", "ko"), "네이버에서는")

    def test_zh(self):
        # pre-lock correction (2026-11-12): in ZH the mapped word is set off by spaces where it touches a character
        self.assertEqual(C.map_answer_words("是的，索尼被广泛认可。", "zh"), "Yes ,索尼被广泛认可。")
        self.assertEqual(C.map_answer_words("不是。", "zh"), "No 。")
        self.assertEqual(C.map_answer_words("“否”", "zh"), "“ No ”")
        self.assertEqual(C.map_answer_words("是一个知名品牌。", "zh"), "是一个知名品牌。")
        self.assertEqual(C.map_answer_words("不太常见。", "zh"), "不太常见。")

    def test_english_answer_untouched(self):
        self.assertEqual(C.map_answer_words("Yes, it is.", "ko"), "Yes, it is.")


def _certified_parsers():
    """The certified recognition parsers of this tree (the same git blobs as at tag v0.42-prereg-r1): v0.20-v0.22
    parse_yes_no and v0.19 parse_phase_a_response."""
    root = HERE.parents[3]
    for p in (root / "scripts", root / "osf" / "v19"):
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))
    import acquire_v0_19
    import run_acquisition_v20
    import run_acquisition_v21
    import run_acquisition_v22
    v19 = {1: "yes", 0: "no", None: "ambiguous"}
    return {"v20": run_acquisition_v20.parse_yes_no, "v21": run_acquisition_v21.parse_yes_no,
            "v22": run_acquisition_v22.parse_yes_no, "v19": lambda t: v19[acquire_v0_19.parse_phase_a_response(t)]}


def _r3_map(text, language):
    """map_answer_words as it was before the pre-lock correction (r3, commit 0074bc1), for the unchanged-behaviour checks."""
    t = C.normalise(text)
    m = C.LEAD_RE[language].match(t)
    if not m:
        return t
    return t[:m.start(2)] + ("Yes" if m.group(2).lower() in C.YES else "No") + t[m.end(2):]


class ZhAnswerWordsCertifiedParsers(unittest.TestCase):
    """Pre-lock correction (coordinator, 2026-11-12): r3's mapping turned 否 / 不是 / 不 into "No" but kept the
    ideographic full stop or unspaced text after it, and v0.20-v0.22's certified parse_yes_no then read "ambiguous"
    (a non-answer) while the same forms of 是 were read as Yes. Section 4.4's rule: they are read as No."""
    NO = ["否。", "不是。", "不。", "否", "不是", "否，", "不是，这不是。", "否！", "“否”。", "“不是”", "（否）"]
    YES = ["是。", "是的。", "是", "是的", "是，", "是的，这是一个知名品牌。", "是！", "“是”。", "“是的”", "（是）"]
    # not mapped in either direction (section 4.4's lookahead does not list '*'): unchanged by the correction, symmetric
    NEITHER = ["是一个知名品牌。", "不太常见。", "这是一个德国音频品牌。是。", "否认", "不知道。", "**否**", "**是**"]

    def setUp(self):
        self.parse = _certified_parsers()

    def test_parsers_are_the_v042_locked_blobs(self):
        import subprocess
        root = HERE.parents[3]
        for f in ("scripts/run_acquisition_v20.py", "scripts/run_acquisition_v21.py", "scripts/run_acquisition_v22.py",
                  "osf/v19/acquire_v0_19.py"):
            a = subprocess.run(["git", "-C", str(root), "rev-parse", f"v0.42-prereg-r1:{f}"], capture_output=True, text=True)
            if a.returncode != 0:
                self.skipTest("tag v0.42-prereg-r1 not available")
            b = subprocess.run(["git", "-C", str(root), "hash-object", f], capture_output=True, text=True, check=True)
            self.assertEqual(a.stdout.strip(), b.stdout.strip(), f)

    def test_zh_no_forms_are_read_as_no(self):
        for t in self.NO:
            m = C.map_answer_words(t, "zh")
            for sub, f in self.parse.items():
                self.assertEqual(f(m), "no", (t, m, sub))

    def test_zh_yes_forms_are_read_as_yes(self):
        for t in self.YES:
            m = C.map_answer_words(t, "zh")
            for sub, f in self.parse.items():
                self.assertEqual(f(m), "yes", (t, m, sub))

    def test_r3_lost_the_no_forms(self):
        """The defect the correction removes: under r3's mapping v0.20-v0.22 read these as non-answers."""
        for t in ("否。", "不是。", "不。", "不是，这不是。"):
            self.assertEqual(self.parse["v20"](_r3_map(t, "zh")), "ambiguous", t)
            self.assertEqual(self.parse["v20"](C.map_answer_words(t, "zh")), "no", t)

    def test_zh_non_answer_words_untouched(self):
        for t in self.NEITHER:
            self.assertEqual(C.map_answer_words(t, "zh"), _r3_map(t, "zh"), t)

    def test_v019_reading_unchanged_in_zh(self):
        for t in self.NO + self.YES + self.NEITHER:
            self.assertEqual(self.parse["v19"](C.map_answer_words(t, "zh")), self.parse["v19"](_r3_map(t, "zh")), t)

    def test_es_and_ko_unchanged(self):
        samples = {"es": ["Sí.", "Sí, Sennheiser es reconocida.", "No.", "No, no es una marca de auriculares.", "**No.**",
                          "Si, es reconocida.", "Si bien es conocida, no.", "Sin duda, sí.", "Es una marca alemana. Sí.",
                          "Denon no es tan conocida como Sony, pero sí, la reconozco.", "¿Sí?", "NO"],
                   "ko": ["예.", "예, 널리 알려진 브랜드입니다.", "네, 소니는 널리 인식됩니다.", "아니요.", "아니요. 그렇지 않습니다.",
                          "아니오, 아닙니다.", "아니,", "**예**", "네이버에서는", "젠하이저는 독일의 오디오 브랜드입니다. 예."]}
        for lg, ts in samples.items():
            for t in ts:
                new, old = C.map_answer_words(t, lg), _r3_map(t, lg)
                self.assertEqual(new, old, (lg, t))                    # byte-identical mapping
                for sub, f in self.parse.items():
                    self.assertEqual(f(new), f(old), (lg, t, sub))     # so every certified reading is unchanged


class Language(unittest.TestCase):
    def test_mc_language(self):
        self.assertTrue(C.in_language(KO_HEADPHONES, "ko"))
        self.assertFalse(C.in_language("Sennheiser and Sony are the best known brands.", "ko"))
        self.assertTrue(C.in_language(ZH_SKINCARE, "zh"))
        self.assertFalse(C.in_language(KO_HEADPHONES, "zh"))
        self.assertTrue(C.in_language("Las mejores marcas son La Mer y Lancôme, por su calidad.", "es"))
        self.assertFalse(C.in_language("The best brands are La Mer and Lancôme, for their quality.", "es"))

    def test_mc_script_traditional(self):
        self.assertTrue(C.zh_traditional("這些品牌們"))
        self.assertFalse(C.zh_traditional(ZH_SKINCARE))


class Records(unittest.TestCase):
    def test_prepare_record_and_guard(self):
        b = {"call_id": "ko|v19|B|q1|gpt-6-astra|S0|1", "language": "ko", "substrate": "v19", "phase": "B",
             "text": "젠하이저", "status": "ok"}
        a23 = {"call_id": "zh|v23|A|x|gpt-6-astra|S0|1", "language": "zh", "substrate": "v23", "phase": "A",
               "text": "是的，轩尼诗是干邑品牌。", "status": "ok"}
        a19 = {"call_id": "es|v19|A|x|gpt-6-astra|S0|1", "language": "es", "substrate": "v19", "phase": "A",
               "text": "Sí, es reconocida.", "status": "ok"}
        self.assertIn("Sennheiser", C.prepare_record(b)["text"])
        self.assertEqual(C.prepare_record(b)["text_original"], "젠하이저")
        self.assertEqual(C.prepare_record(a23)["text"], a23["text"])
        self.assertEqual(C.prepare_record(a19)["text"], "Yes, es reconocida.")
        with tempfile.TemporaryDirectory() as d:
            raw = Path(d) / "raw.jsonl"
            raw.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in (b, a23, a19)) + "\n", encoding="utf-8")
            n, _h = C.prepare_raw(raw, Path(d) / "out")
            self.assertEqual(n, {"es": 1, "ko": 1, "zh": 1})
        orig = C._ls_remote_tag
        C._ls_remote_tag = lambda: ""
        try:
            with self.assertRaises(C.Refused):
                C.guard_real_raw(C.REAL_RAW)
        finally:
            C._ls_remote_tag = orig


if __name__ == "__main__":
    unittest.main()
