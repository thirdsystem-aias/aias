"""AIAS v0.62 r2: build the Korean / Chinese / Spanish coding-alias table (brand_aliases_v0_62_r2.csv).

Aliases are the runner's drafts (Claude Opus 5.5, 2026-11-10/11), each with a check status:
  CONFIRMED  the form was seen on the brand's own Korean/Chinese site, or a dated authoritative page the runner opened;
  PARTLY     one of several forms was seen, or the form was seen only on a secondary source;
  UNCONFIRMED no source was opened (or none showed the form). Unconfirmed aliases stay in force as spelling
             transcriptions and are flagged for the native check.
The check record (CHECKS below) lists URL and access date for every CONFIRMED / PARTLY row; nothing else is claimed.

Rules (pre-registration r2, section 4.2):
  - parity with the certified English matchers: an alias may not be looser than the English rule, which counts only
    the full registry string (e.g. Mercedes-Benz, Dior Beauty, Tom Ford Beauty); bare 奔驰 / 벤츠, 迪奥 / 디올,
    香奈儿 / 샤넬, 阿玛尼 / 아르마니, 汤姆福特 / 톰 포드, 欧莱雅 / 로레알 are therefore NOT aliases;
  - words that are also common words are either excluded (ZH 现代 'modern', 大众 'the public'; KO 현대 'modern')
    or kept as collision-prone (audited; switched off in S-Alias);
  - Spanish keeps the registry names; accent variants are already handled by the certified matchers (accent
    stripping), so no Spanish alias is needed (checked brands: Bacardi/Bacardi, Patron/Patron, Remy Martin,
    L'Oreal Paris/Paris, Fernet-Branca; see ES_NOTES).
Run: python3 osf/v62/scripts/make_alias_table_r2_v0_62.py
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..', 'translations', 'brand_aliases_v0_62_r2.csv'))
SRC = os.path.normpath(os.path.join(HERE, '..', 'translations', 'brand_aliases_v0_62_r1.csv'))

# brand: (ko aliases, ko collision-prone?, zh aliases, zh collision-prone?, note)
A = {
 # v19 audiophile headphones
 'Audeze': ('오디지', 0, '', 0, ''),
 'Audio-Technica': ('오디오테크니카|오디오 테크니카', 0, '铁三角', 0, ''),
 'Beyerdynamic': ('베이어다이나믹', 0, '拜雅|拜亚动力', 0, ''),
 'Dan Clark Audio': ('댄 클락 오디오', 0, '', 0, ''),
 'Denon': ('데논', 0, '天龙', 0, 'unit flagged in DEVIATIONS Entry 0'),
 'Final Audio': ('파이널 오디오', 0, '', 0, 'bare 파이널 (= final) is not an alias'),
 'Focal': ('포칼', 0, '劲浪', 0, ''),
 'Grado': ('그라도', 0, '歌德', 1, 'ZH 歌德 is also the usual name of Goethe'),
 'HiFiMan': ('하이파이맨', 0, '海菲曼', 0, ''),
 'Koss': ('코스', 1, '高斯', 1, 'KO 코스 = course / COS; ZH 高斯 = Gauss'),
 'Meze': ('메제', 0, '', 0, ''),
 'Sennheiser': ('젠하이저', 0, '森海塞尔', 0, ''),
 'Sony': ('소니', 0, '索尼', 0, ''),
 'Spirit Torino': ('스피릿 토리노', 0, '', 0, ''),
 'Stax': ('스탁스', 0, '', 0, ''),
 'ZMF Headphones': ('', 0, '', 0, 'no alias (Latin script in both languages)'),
 # v20 skincare
 'Estée Lauder': ('에스티 로더', 0, '雅诗兰黛', 0, ''),
 'Lancôme': ('랑콤', 0, '兰蔻', 0, ''),
 'La Mer': ('라 메르', 0, '海蓝之谜', 0, ''),
 'Sisley': ('시슬리', 0, '希思黎', 0, ''),
 'Dior Beauty': ('디올 뷰티', 0, '迪奥美妆', 0, 'parity: bare 디올 / 迪奥 not aliases'),
 'Chanel Beauty': ('샤넬 뷰티', 0, '香奈儿美妆', 0, 'parity: bare 샤넬 / 香奈儿 not aliases'),
 'La Prairie': ('라 프레리', 0, '莱珀妮', 0, ''),
 'Clé de Peau Beauté': ('끌레드뽀 보떼', 0, '肌肤之钥', 0, 'ZH 肌肤之钥 is the full Chinese brand name (parity kept)'),
 'Rare Beauty': ('레어 뷰티', 0, '', 0, ''),
 'Rhode': ('로드', 1, '', 0, 'KO 로드 = road / load'),
 'Fenty Skin': ('펜티 스킨', 0, '', 0, ''),
 'Goop': ('구프', 0, '', 0, ''),
 'Drunk Elephant': ('드렁크 엘리펀트', 0, '醉象', 0, ''),
 'Glossier': ('글로시에', 0, '', 0, ''),
 'Augustinus Bader': ('어거스티누스 바더', 0, '', 0, ''),
 'Tower 28': ('타워 28', 0, '', 0, ''),
 'SkinCeuticals': ('스킨수티컬즈', 0, '修丽可', 0, ''),
 'La Roche-Posay': ('라로슈포제', 0, '理肤泉', 0, ''),
 "Paula's Choice": ('폴라초이스', 0, '宝拉珍选', 0, ''),
 'CeraVe': ('세라비', 0, '适乐肤', 0, ''),
 'The Ordinary': ('디 오디너리', 0, '', 0, ''),
 'Cetaphil': ('세타필', 0, '丝塔芙', 0, ''),
 'Eucerin': ('유세린', 0, '优色林', 0, ''),
 'Bioderma': ('바이오더마', 0, '贝德玛', 0, ''),
 # v21 cosmetics
 'MAC Cosmetics': ('맥 코스메틱', 0, '魅可', 0, 'parity: bare 맥 not an alias; ZH 魅可 is the brand Chinese name (parity to be checked against the v0.21 matcher)'),
 'NARS': ('나스', 1, '娜斯', 0, 'KO 나스 also = NAS (storage)'),
 'Bobbi Brown': ('바비 브라운', 0, '芭比波朗', 0, ''),
 'Tom Ford Beauty': ('톰 포드 뷰티', 0, '汤姆福特美妆', 0, 'parity: bare 톰 포드 / 汤姆福特 not aliases'),
 'Giorgio Armani Beauty': ('조르지오 아르마니 뷰티', 0, '阿玛尼美妆', 0, 'parity: bare 아르마니 / 阿玛尼 not aliases'),
 'Hourglass': ('아워글래스', 0, '', 0, ''),
 'Chantecaille': ('샹테카이', 0, '香缇卡', 0, ''),
 'Laura Mercier': ('로라 메르시에', 0, '罗拉玛斯亚', 0, ''),
 'Fenty Beauty': ('펜티 뷰티', 0, '', 0, ''),
 'Haus Labs': ('하우스 랩스', 0, '', 0, ''),
 'Pat McGrath Labs': ('팻 맥그래스 랩스', 0, '', 0, ''),
 'Charlotte Tilbury': ('샬롯 틸버리', 0, '', 0, ''),
 'Huda Beauty': ('후다 뷰티', 0, '', 0, ''),
 'Kylie Cosmetics': ('카일리 코스메틱', 0, '', 0, ''),
 'Anastasia Beverly Hills': ('아나스타샤 베버리힐즈', 0, '', 0, ''),
 'Maybelline': ('메이블린', 0, '美宝莲', 0, ''),
 "L'Oréal Paris": ('로레알 파리', 0, '巴黎欧莱雅', 0, 'parity: bare 로레알 / 欧莱雅 not aliases'),
 'CoverGirl': ('커버걸', 0, '封面女郎', 0, ''),
 'Revlon': ('레브론', 0, '露华浓', 0, ''),
 'NYX Professional Makeup': ('닉스 프로페셔널 메이크업', 0, '', 0, ''),
 'e.l.f. Cosmetics': ('엘프 코스메틱', 0, '', 0, 'bare 엘프 (= elf) not an alias'),
 'Wet n Wild': ('웻앤와일드', 0, '', 0, ''),
 'Milani Cosmetics': ('밀라니 코스메틱', 0, '', 0, 'parity: bare 밀라니 not an alias'),
 # v22 automotive
 'Mercedes-Benz': ('메르세데스-벤츠|메르세데스 벤츠', 0, '梅赛德斯-奔驰|梅赛德斯奔驰', 0, 'parity: bare 벤츠 / 奔驰 not aliases'),
 'Jaguar': ('재규어', 1, '捷豹', 0, 'KO 재규어 = the animal'),
 'Cadillac': ('캐딜락', 0, '凯迪拉克', 0, ''),
 'Rolls-Royce': ('롤스로이스', 0, '劳斯莱斯', 0, ''),
 'Bentley': ('벤틀리', 0, '宾利', 0, ''),
 'Porsche': ('포르쉐', 0, '保时捷', 0, ''),
 'BMW': ('비엠더블유', 0, '宝马', 0, ''),
 'Tesla': ('테슬라', 0, '特斯拉', 0, ''),
 'Rivian': ('리비안', 0, '', 0, ''),
 'Lucid': ('루시드', 0, '', 0, ''),
 'Polestar': ('폴스타', 0, '极星', 0, ''),
 'Fisker': ('피스커', 0, '菲斯克', 0, ''),
 'Toyota': ('토요타|도요타', 0, '丰田', 0, ''),
 'Honda': ('혼다', 0, '本田', 0, ''),
 'Ford': ('포드', 0, '福特', 0, ''),
 'Chevrolet': ('쉐보레', 0, '雪佛兰', 0, ''),
 'Hyundai': ('현대자동차|현대차', 0, '现代汽车|北京现代', 0, 'bare 현대 / 现代 (= modern) excluded'),
 'Volkswagen': ('폭스바겐', 0, '大众汽车|上汽大众|一汽-大众|一汽大众', 0, 'bare 大众 (= the public, mass market) excluded'),
 'Nissan': ('닛산', 0, '日产', 1, 'ZH 日产 can also mean made in Japan'),
 'Pontiac': ('폰티악', 0, '庞蒂亚克', 0, ''),
 'Oldsmobile': ('올즈모빌', 0, '奥兹莫比尔', 0, ''),
 'Plymouth': ('플리머스', 0, '普利茅斯', 1, 'ZH 普利茅斯 is also the city'),
 'Mercury': ('머큐리', 1, '水星', 1, 'planet / Freddie Mercury'),
 'Saturn': ('새턴', 1, '土星', 1, 'planet'),
 # v23 premium spirits
 'Johnnie Walker': ('조니워커|조니 워커', 0, '尊尼获加', 0, ''),
 'Hennessy': ('헤네시', 0, '轩尼诗', 0, ''),
 "Jack Daniel's": ('잭다니엘|잭 다니엘', 0, '杰克丹尼', 0, ''),
 'Patrón': ('패트론', 0, '培恩', 0, ''),
 'Grey Goose': ('그레이구스|그레이 구스', 0, '灰雁', 0, ''),
 'Bacardi': ('바카디', 0, '百加得', 0, ''),
 'Bombay Sapphire': ('봄베이 사파이어', 0, '孟买蓝宝石', 0, ''),
 'Jameson': ('제임슨', 0, '尊美醇', 0, ''),
 'Lagavulin': ('라가불린', 0, '乐加维林', 0, ''),
 'Clase Azul': ('클라세 아줄', 0, '', 0, ''),
 "Hendrick's": ('헨드릭스', 0, '亨利爵士', 0, ''),
 'Woodford Reserve': ('우드포드 리저브', 0, '活福', 0, ''),
 'Monkey 47': ('몽키 47', 0, '', 0, ''),
 'The Balvenie': ('발베니', 0, '百富', 0, ''),
 'Rémy Martin': ('레미 마르탱', 0, '人头马', 0, ''),
 'Casamigos': ('카사미고스', 0, '', 0, ''),
 'Fortaleza': ('포르탈레자', 0, '', 0, ''),
 'Compass Box': ('컴퍼스 박스', 0, '', 0, ''),
 'Nikka': ('닛카', 0, '一甲', 0, ''),
 'Del Maguey': ('델 마과이', 0, '', 0, ''),
 'Fernet-Branca': ('페르넷 브랑카', 0, '菲奈特布兰卡', 0, ''),
 'Redbreast': ('레드브레스트', 0, '知更鸟', 1, 'ZH 知更鸟 = robin (the bird)'),
 'St. George Spirits': ('세인트 조지 스피릿', 0, '', 0, ''),
 'Mezcal Vago': ('메스칼 바고|메즈칼 바고', 0, '', 0, ''),
}

ES_NOTES = {
 'Bacardi': 'ES often writes Bacardí; the certified matcher strips accents (no alias needed).',
 'Patrón': 'the registry form is already Spanish; unaccented Patron matched by accent stripping.',
 'Rémy Martin': 'ES writes Rémy Martin; no Spanish-specific form.',
 "L'Oréal Paris": 'ES writes L\'Oréal París; accent stripping maps it to the registry string.',
 'Fernet-Branca': 'Argentine usage often Fernet Branca (no hyphen); whether the v0.23 matcher counts it is a parity check before the lock; no alias added.',
}

# check record: brand -> {lang: (status, source, accessed)}; filled only from pages actually opened (r2)
D = '2026-11-11'   # UTC access date (2026-11-10 evening US Central)
CHECKS = {
 'Sennheiser': {'zh': ('CONFIRMED', 'Sennheiser press release (prezly CDN), dated 2025-04-10, uses 森海塞尔: https://cdn.uc.assets.prezly.com/708844ce-eb3e-4b8a-a5ce-a60153f7fc50/-/inline/no/InfoComm China 2025_PR_Final.pdf', D),
                'ko': ('PARTLY', 'secondary: Gamemeca, 2011-10-04, uses 젠하이저 (sennheiserkorea.co.kr refused robots): https://www.gamemeca.com/view.php?gid=112942', D)},
 'Audio-Technica': {'zh': ('CONFIRMED', 'brand China site, footer 北京铁三角技术开发有限公司 and news 铁三角推出ATH-R30x: http://www.audio-technica.com.cn/', D)},
 'HiFiMan': {'zh': ('PARTLY', 'secondary: Bilibili article, 2025-10-25, "HIFIMAN海菲曼": https://www.bilibili.com/read/cv43491197', D)},
 'Beyerdynamic': {'zh': ('PARTLY', 'secondary: SMZDM, 2025-09-19, "拜雅（beyerdynamic）"; 拜亚动力 not seen: https://post.smzdm.com/p/a469v62k/', D)},
 'Denon': {'ko': ('PARTLY', 'secondary: ITWorld Korea, 2023-09-12, "데논(Denon)": https://www.itworld.co.kr/article/3549502/', D),
           'zh': ('UNCONFIRMED', 'brand zh-cn site writes Latin "Denon" only (company 上海电音马兰士电子有限公司); 天龙 not seen there: https://www.denon.com/zh-cn/', D)},
 'Sony': {'ko': ('PARTLY', 'secondary: ITWorld Korea, 2024-04-15, 소니 / 소니코리아: https://www.itworld.co.kr/article/3585417/', D)},
}


def main():
    src = list(csv.DictReader(open(SRC, encoding='utf-8')))
    rows = []
    for r in src:
        b = r['brand']
        ko, kocp, zh, zhcp, note = A[b]
        ck = CHECKS.get(b, {})
        kst = ck.get('ko', ('UNCONFIRMED', '', ''))
        zst = ck.get('zh', ('UNCONFIRMED', '', '')) if zh else ck.get('zh', ('NO ALIAS', '', ''))
        rows.append({'substrate': r['substrate'], 'brand': b, 'ko_aliases': ko, 'ko_collision_prone': 'yes' if kocp else 'no',
                     'zh_aliases': zh, 'zh_collision_prone': 'yes' if zhcp else 'no', 'es_aliases': '',
                     'es_note': ES_NOTES.get(b, ''), 'note': note,
                     'ko_check_status': kst[0], 'ko_check_source': kst[1], 'ko_check_accessed': kst[2],
                     'zh_check_status': zst[0], 'zh_check_source': zst[1], 'zh_check_accessed': zst[2]})
    with open(OUT, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    from collections import Counter
    for lg in ('ko', 'zh'):
        print(lg, dict(Counter(r[lg + '_check_status'] for r in rows)),
              'aliases', sum(len(list(filter(None, r[lg + '_aliases'].split('|')))) for r in rows),
              'units with alias', sum(1 for r in rows if r[lg + '_aliases']))
    print('rows', len(rows), '->', OUT)


if __name__ == '__main__':
    main()
