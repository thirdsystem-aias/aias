"""Tests of code_v0_62.py (pre-step, answer words, MC_Language) on realistic French and Japanese answer snippets.
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

TABLE = HERE.parents[1] / "translations" / "brand_aliases_v0_62_r1.csv"
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


def code(text, substrate):
    return fake_match(C.prepare_text(text, substrate), substrate)


JA_HEADPHONES = """オーディオマニアに評価の高いヘッドホンブランドをいくつか挙げます。

1. **ゼンハイザー（Sennheiser）**：HD 800 Sは解像度の高さで定番です。
2. **オーディオ・テクニカ**：ATH-ADX5000など、日本ブランドらしい作り込み。
3. **ソニー**のMDR-Z1R、**スタックス**の静電型イヤースピーカー。
4. ファイナル・オーディオのD8000、ＨｉＦｉＭａｎ（ハイファイマン）の平面駆動型。
※ コスメやコスプレとは関係ありませんが、ファイナルファンタジーのコラボモデルもあります。"""

FR_SKINCARE = """Voici quelques marques de soins haut de gamme :

- **La Mer** – la Crème de la Mer est emblématique ;
- **Estee Lauder** (Advanced Night Repair) ;
- **Lancome** et sa gamme Génifique ;
- **Clé de Peau Beauté**, la marque de luxe de Shiseido ;
- Pour les peaux sensibles, La Roche-Posay, Bioderma et Avène (non listée ici)."""

FR_MAKEUP = "Côté maquillage, L’Oréal Paris et Maybelline dominent le marché grand public ; NARS et M·A·C pour les pros."

JA_AUTO = """高級車ブランドなら、メルセデス・ベンツ、ＢＭＷ、ﾎﾟﾙｼｪが代表的です。EVではテスラのモデルS、ルシード・モータースの
ルシード・エア、ヒョンデのIONIQ 5も注目されています。日産とトヨタ（レクサス）も外せません。ジャガーの動物的なデザイン。
ロードバイクやベンツという通称だけの記述は数えません。"""

JA_SPIRITS = "ニッカウヰスキーの竹鶴、ジョニーウォーカー、ヘネシーXO、そしてザ・バルヴェニーが挙げられます。"


class PreStep(unittest.TestCase):
    def test_ja_headphones_snippet(self):
        found = code(JA_HEADPHONES, "v19")
        self.assertEqual(found, {"Sennheiser", "Audio-Technica", "Sony", "Stax", "Final Audio", "HiFiMan"})
        self.assertNotIn("Koss", found)                       # コスメ, コスプレ are not コス

    def test_fr_skincare_snippet(self):
        self.assertEqual(code(FR_SKINCARE, "v20"), {"La Mer", "Estée Lauder", "Lancôme", "Clé de Peau Beauté",
                                                    "La Roche-Posay", "Bioderma"})

    def test_fr_makeup_typographic_apostrophe(self):
        found = code(FR_MAKEUP, "v21")
        self.assertIn("L'Oréal Paris", found)
        self.assertIn("NARS", found)
        self.assertNotIn("MAC Cosmetics", found)              # English rule needs "MAC Cosmetics" (parity)

    def test_ja_auto_snippet_fullwidth_halfwidth(self):
        found = code(JA_AUTO, "v22")
        self.assertEqual(found, {"Mercedes-Benz", "BMW", "Porsche", "Tesla", "Lucid", "Hyundai", "Nissan", "Toyota",
                                 "Jaguar"})

    def test_bare_benz_is_not_mercedes(self):
        self.assertEqual(code("ベンツのSクラスが人気です。", "v22"), set())

    def test_ja_spirits_compounds(self):
        self.assertEqual(code(JA_SPIRITS, "v23"), {"Nikka", "Johnnie Walker", "Hennessy", "The Balvenie"})

    def test_beauty_cosmetics_spelling_variants(self):
        self.assertEqual(code("レア ビューティとカイリーコスメティックス、フェンティ・ビューティ", "v21"),
                         {"Rare Beauty", "Kylie Cosmetics", "Fenty Beauty"})

    def test_decoys_P4(self):
        for d, sub in (("コスメ", "v19"), ("コスプレ", "v19"), ("ロードバイク", "v20"), ("ファイナル", "v19"),
                       ("マック", "v21"), ("エルフ", "v21"), ("ポーラ", "v20"), ("本田さん", "v22"), ("ミラニ", "v21")):
            self.assertEqual(code(f"今日は{d}の話です。", sub), set(), d)

    def test_every_alias_reaches_its_unit_P4(self):
        bad = []
        for r in ROWS:
            for a in filter(None, r["ja_aliases"].split("|")):
                for tmpl in ("おすすめは「{}」の製品です。", "1. **{}**：定番", "第2位 {}（評価4.5）", "{}、"):
                    got = code(tmpl.format(a), r["substrate"])
                    if got != {r["brand"]}:
                        bad.append((a, tmpl, sorted(got)))
            for a in filter(None, r["fr_aliases"].split("|")):
                got = code(f"La marque {a}, très connue.", r["substrate"])
                if got != {r["brand"]}:
                    bad.append((a, "fr", sorted(got)))
        self.assertEqual(bad, [])

    def test_english_text_unchanged_P2_shape(self):
        for sub, t in (("v20", "Top picks: La Mer, Estée Lauder and Paula's Choice."),
                       ("v22", "Mercedes-Benz, BMW and Rolls-Royce lead; Benz alone is a nickname."),
                       ("v19", "Sennheiser's HD 800 S and Audio-Technica's ATH-R70x.")):
            self.assertEqual(fake_match(C.prepare_text(t, sub), sub), fake_match(t, sub), t)

    def test_alias_audit_collects_collision_prone(self):
        hits = []
        C.prepare_text("ジャガーのF-PACEと、野生のジャガー。", "v22", hits=hits)
        self.assertEqual(len(hits), 2)
        self.assertTrue(all(h[2] == "ジャガー" for h in hits))

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
    def test_fr(self):
        self.assertEqual(C.map_answer_words("Oui, Sennheiser est reconnue.", "fr"), "Yes, Sennheiser est reconnue.")
        self.assertEqual(C.map_answer_words("**Non.** Pas vraiment.", "fr"), "**No.** Pas vraiment.")
        self.assertEqual(C.map_answer_words("Nonobstant sa taille, oui.", "fr"), "Nonobstant sa taille, oui.")

    def test_ja(self):
        self.assertEqual(C.map_answer_words("はい。ソニーは広く認知されています。", "ja"), "Yes。ソニーは広く認知されています。")
        self.assertEqual(C.map_answer_words("「いいえ」です。", "ja"), "「No」です。")

    def test_english_answer_untouched(self):
        self.assertEqual(C.map_answer_words("Yes, it is.", "fr"), "Yes, it is.")


class Language(unittest.TestCase):
    def test_mc_language(self):
        self.assertTrue(C.in_language(JA_HEADPHONES, "ja"))
        self.assertFalse(C.in_language("Sennheiser and Sony are the best known brands.", "ja"))
        self.assertTrue(C.in_language(FR_SKINCARE, "fr"))
        self.assertFalse(C.in_language("The best brands are La Mer and Lancôme, for their quality.", "fr"))


class Records(unittest.TestCase):
    def test_prepare_record_and_guard(self):
        b = {"call_id": "ja|v19|B|q1|gpt-6-astra|S0|1", "language": "ja", "substrate": "v19", "phase": "B",
             "text": "ゼンハイザー", "status": "ok"}
        a23 = {"call_id": "fr|v23|A|x|gpt-6-astra|S0|1", "language": "fr", "substrate": "v23", "phase": "A",
               "text": "Oui, Hennessy est une marque de cognac.", "status": "ok"}
        self.assertIn("Sennheiser", C.prepare_record(b)["text"])
        self.assertEqual(C.prepare_record(b)["text_original"], "ゼンハイザー")
        self.assertEqual(C.prepare_record(a23)["text"], a23["text"])
        with tempfile.TemporaryDirectory() as d:
            raw = Path(d) / "raw.jsonl"
            raw.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in (b, a23)) + "\n", encoding="utf-8")
            n, _h = C.prepare_raw(raw, Path(d) / "out")
            self.assertEqual(n, {"fr": 1, "ja": 1})
        orig = C._ls_remote_tag
        C._ls_remote_tag = lambda: ""
        try:
            with self.assertRaises(C.Refused):
                C.guard_real_raw(C.REAL_RAW)
        finally:
            C._ls_remote_tag = orig


if __name__ == "__main__":
    unittest.main()
