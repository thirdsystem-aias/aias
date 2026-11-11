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
 'Sennheiser': {'ko': ('CONFIRMED', 'brand Korea site, title "젠하이저 — 헤드폰, 마이크 및 무선 시스템": https://www.sennheiser.com/ko-kr', '2026-11-11'), 'zh': ('CONFIRMED', 'Sennheiser press release (prezly CDN), dated 2025-04-10, uses 森海塞尔: https://cdn.uc.assets.prezly.com/708844ce-eb3e-4b8a-a5ce-a60153f7fc50/-/inline/no/InfoComm China 2025_PR_Final.pdf', '2026-11-11')},
 'Audio-Technica': {'ko': ('PARTLY', '오디오테크니카 on audio-technica.co.kr, but the page calls itself the Korean official importer (수입원), not the brand or its subsidiary; spaced form 오디오 테크니카 not seen: https://www.audio-technica.co.kr/', '2026-11-11'), 'zh': ('CONFIRMED', 'brand China site, footer 北京铁三角技术开发有限公司 and news 铁三角推出ATH-R30x: http://www.audio-technica.com.cn/', '2026-11-11')},
 'HiFiMan': {'zh': ('PARTLY', 'secondary: Bilibili article, 2025-10-25, "HIFIMAN海菲曼": https://www.bilibili.com/read/cv43491197 (brand site hifiman.com English only, 海菲曼 not seen there)', '2026-11-11')},
 'Beyerdynamic': {'zh': ('PARTLY', 'secondary: SMZDM, 2025-09-19, "拜雅（beyerdynamic）"; 拜亚动力 not seen: https://post.smzdm.com/p/a469v62k/', '2026-11-11')},
 'Denon': {'ko': ('PARTLY', 'secondary: ITWorld Korea, 2023-09-12, "데논(Denon)": https://www.itworld.co.kr/article/3549502/', '2026-11-11'), 'zh': ('UNCONFIRMED', 'brand zh-cn site writes Latin "Denon" only (company 上海电音马兰士电子有限公司); 天龙 not seen there: https://www.denon.com/zh-cn/', '2026-11-11')},
 'Sony': {'ko': ('CONFIRMED', 'brand Korea site, title "소니코리아", footer "소니코리아 (주)": https://www.sony.co.kr/', '2026-11-11'), 'zh': ('CONFIRMED', 'brand China site (Sony (China) Limited), 索尼在华业务与产品: https://www.sony.com.cn/', '2026-11-11')},
 'Porsche': {'ko': ('CONFIRMED', 'brand Korea site, "포르쉐코리아 ... 포르쉐 AG": https://www.porsche.com/korea/ko/porsche-korea-ltd', '2026-11-11'), 'zh': ('CONFIRMED', 'Porsche Newsroom CHN, dated 2025-11-06, "保时捷中国研发中心": https://newsroom.porsche.com/zh/2025/company/cn-porsche-china-research-development-hub-opening-shanghai-41043.html', '2026-11-11')},
 'Toyota': {'ko': ('PARTLY', 'brand Korea site, title "토요타 코리아", 토요타 many times; 도요타 not seen: https://www.toyota.co.kr/', '2026-11-11'), 'zh': ('CONFIRMED', 'brand China JV site (GAC Toyota), title "广汽丰田官网": https://www.gac-toyota.com.cn/', '2026-11-11')},
 'Mercedes-Benz': {'ko': ('CONFIRMED', 'brand Korea site, "메르세데스-벤츠" in description and footer "메르세데스-벤츠 코리아(주)"; spaced form follows from KO-1: https://www.mercedes-benz.co.kr/', '2026-11-11'), 'zh': ('CONFIRMED', 'brand China site, title "梅赛德斯-奔驰" and body "全新梅赛德斯-奔驰 长轴距GLE"; unhyphenated form follows from ZH-1 (earlier source Xinhua 2025-11-06 is secondary: https://www.news.cn/auto/20251106/666e43f159944af89d7ea3752d16d036/c.html): https://www.mercedes-benz.com.cn/', '2026-11-11')},
 'Hyundai': {'ko': ('CONFIRMED', 'brand Korea site, "현대자동차 공식 홈페이지 현대닷컴", keywords 현대차: https://www.hyundai.com/kr/ko/e', '2026-11-11'), 'zh': ('CONFIRMED', 'brand China site (Beijing Hyundai), title "北京现代汽车官方网站" and 现代汽车 in body: https://www.beijing-hyundai.com.cn/', '2026-11-11')},
 'Chevrolet': {'ko': ('CONFIRMED', 'brand Korea site, "쉐보레 코리아 공식 홈페이지": https://www.chevrolet.co.kr/', '2026-11-11')},
 'Cadillac': {'ko': ('CONFIRMED', 'brand Korea site, meta description "캐딜락 코리아": https://www.cadillac.co.kr/', '2026-11-11')},
 'Volkswagen': {'ko': ('CONFIRMED', 'brand Korea site, title "폭스바겐코리아 공식 홈페이지": https://www.volkswagen.co.kr/', '2026-11-11'), 'zh': ('PARTLY', 'brand China JV site (SAIC Volkswagen) shows 大众汽车 and 上汽大众; 一汽-大众 and 一汽大众 not seen: https://www.svw-volkswagen.com/', '2026-11-11')},
 'BMW': {'ko': ('UNCONFIRMED', 'brand Korea site writes Latin "BMW" only (title "BMW 코리아 공식 홈페이지"); 비엠더블유 not seen: https://www.bmw.co.kr/ko/index.html', '2026-11-11'), 'zh': ('CONFIRMED', 'brand China site, meta keywords 宝马官网, footer 宝马集团: https://www.bmw.com.cn/', '2026-11-11')},
 'Tesla': {'ko': ('UNCONFIRMED', 'brand Korea site writes Latin "Tesla는"; 테슬라 not seen on the page: https://www.tesla.com/ko_kr', '2026-11-11'), 'zh': ('CONFIRMED', 'brand China site, title "特斯拉中国": https://www.tesla.cn/', '2026-11-11')},
 'Nissan': {'ko': ('CONFIRMED', 'brand Korea site, "닛산 고객 케어 프로그램" and news items: https://www.nissan.co.kr/', '2026-11-11'), 'zh': ('CONFIRMED', 'brand China site (Dongfeng Nissan), "日产品牌", title "Nissan东风日产官方网站": https://www.dongfeng-nissan.com.cn/', '2026-11-11')},
 'Polestar': {'ko': ('CONFIRMED', 'brand Korea site, footer "폴스타오토모티브코리아 유한회사": https://www.polestar.com/kr/', '2026-11-11')},
 'Rolls-Royce': {'ko': ('CONFIRMED', 'brand Korea site, title "롤스로이스 모터카": https://www.rolls-roycemotorcars.com/ko_KR/home.html', '2026-11-11'), 'zh': ('CONFIRMED', 'brand China site, description "欢迎访问劳斯莱斯汽车官网": https://www.rolls-roycemotorcars.com.cn/', '2026-11-11')},
 'Estée Lauder': {'ko': ('CONFIRMED', 'brand Korea site, "에스티 로더 Estée Lauder 공식 온라인 몰": https://www.esteelauder.co.kr/', '2026-11-11'), 'zh': ('CONFIRMED', 'brand China site, title "雅诗兰黛官网", footer 雅诗兰黛(上海)商贸有限公司: https://www.esteelauder.com.cn/', '2026-11-11')},
 'MAC Cosmetics': {'ko': ('PARTLY', 'brand Korea site writes "맥 코스메틱스" and "맥 MAC Cosmetics"; the alias 맥 코스메틱 is a prefix of 맥 코스메틱스 and would fail KO-2 there; PROPOSED alias 맥 코스메틱스: https://www.maccosmetics.co.kr/', '2026-11-11'), 'zh': ('CONFIRMED', 'brand China site, meta keywords "MAC官网，魅可官网" (keywords only; body text not seen): https://www.maccosmetics.com.cn/', '2026-11-11')},
 'Cetaphil': {'ko': ('CONFIRMED', 'brand Korea site, "세타필 공식 웹사이트": https://www.cetaphil.co.kr/', '2026-11-11'), 'zh': ('CONFIRMED', 'brand China site, title "丝塔芙官网": https://www.cetaphil.com.cn/', '2026-11-11')},
 'Dior Beauty': {'ko': ('UNCONFIRMED', 'brand Korea site writes 크리스챤 디올 코스메틱 / 디올; 디올 뷰티 not seen: https://www.dior.com/ko_kr', '2026-11-11'), 'zh': ('CONFIRMED', 'brand China site, link text "克丽丝汀·迪奥美妆" (contains 迪奥美妆): https://www.dior.cn/zh_cn', '2026-11-11')},
 'Chanel Beauty': {'ko': ('UNCONFIRMED', 'brand Korea site writes 샤넬 (title, 샤넬코리아) and Latin "CHANEL BEAUTY"; 샤넬 뷰티 not seen: https://www.chanel.com/kr/', '2026-11-11'), 'zh': ('CONFIRMED', 'brand China site, menu "香奈儿美妆手册": https://www.chanel.cn/cn/', '2026-11-11')},
 'NARS': {'ko': ('CONFIRMED', 'brand Korea site, "나스 코스메틱 | 공식 홈페이지": https://www.narscosmetics.co.kr/', '2026-11-11')},
 'Bobbi Brown': {'ko': ('CONFIRMED', 'brand Korea site, "바비 브라운 Bobbi Brown 공식 온라인 몰": https://www.bobbibrown.co.kr/', '2026-11-11'), 'zh': ('CONFIRMED', 'brand China site, title "BOBBI BROWN芭比波朗": https://www.bobbibrown.com.cn/', '2026-11-11')},
 "L'Oréal Paris": {'ko': ('CONFIRMED', 'brand Korea site writes 로레알파리 (no space; spacing optional under KO-1): https://www.lorealparis.co.kr/', '2026-11-11'), 'zh': ('CONFIRMED', 'brand China site, title "巴黎欧莱雅": https://www.lorealparis.com.cn/', '2026-11-11')},
 'Maybelline': {'ko': ('CONFIRMED', 'brand Korea site, "메이블린 뉴욕" in banners: https://www.maybelline.co.kr/', '2026-11-11')},
 'Johnnie Walker': {'ko': ('CONFIRMED', 'brand Korea site, title "스카치 위스키 홈 | 조니워커 KR"; spaced form follows from KO-1: https://www.johnniewalker.com/ko-kr/', '2026-11-11')},
 'Ford': {'zh': ('CONFIRMED', 'brand China site, title "福特汽车官方网站": https://www.ford.com.cn/', '2026-11-11')},
 'Lancôme': {'zh': ('CONFIRMED', 'brand China site, title "Lancôme|兰蔻官网": https://www.lancome.com.cn/', '2026-11-11')},
 'La Mer': {'zh': ('CONFIRMED', 'brand China site, title "LAMER|海蓝之谜官网": https://www.lamer.com.cn/', '2026-11-11')},
 'La Roche-Posay': {'zh': ('CONFIRMED', 'brand China site, title "理肤泉官方网站": https://www.larocheposay.com.cn/', '2026-11-11')},
 'SkinCeuticals': {'zh': ('CONFIRMED', 'brand China site, title "修丽可官网": https://www.skinceuticals.com.cn/', '2026-11-11')},
 'La Prairie': {'ko': ('CONFIRMED', 'Beiersdorf Korea (brand owner, Korean corporate site) writes 라프레리 (no space; spacing optional under KO-1): https://www.beiersdorf.co.kr/', '2026-11-11'), 'zh': ('CONFIRMED', 'brand China site, 莱珀妮商贸（上海）有限公司 and 莱珀妮赏悦荟: https://www.laprairie.com.cn/', '2026-11-11')},
 "Paula's Choice": {'ko': ('CONFIRMED', 'brand Korea site, title "폴라초이스 공식 온라인몰": https://www.paulaschoice.co.kr/', '2026-11-11')},
 'Hennessy': {'zh': ('CONFIRMED', 'brand China site, 轩尼诗 in title and body: https://www.hennessy.cn/', '2026-11-11')},
 'Nikka': {'ko': ('UNCONFIRMED', 'brand site nikka.com offers only JP and EN, no Korean page; 닛카 not seen on a brand page: https://www.nikka.com/eng/', '2026-11-11'), 'zh': ('UNCONFIRMED', 'brand site nikka.com offers only JP and EN, no Chinese page; 一甲 not seen on a brand page: https://www.nikka.com/eng/', '2026-11-11')},
 'Tom Ford Beauty': {'zh': ('CONFIRMED', 'brand China site (tomfordbeauty.com.cn), title "TOMFORDBEAUTY|汤姆福特美妆官网"; the founder is written 汤姆·福特 with a middle dot in the description: https://www.tomfordbeauty.com.cn/', '2026-11-11')},
 'Jaguar': {'zh': ('CONFIRMED', 'brand China site, title "捷豹 | 超凡灵感 | 不循常规": https://www.jaguar.com.cn/', '2026-11-11')},
 'Honda': {'zh': ('CONFIRMED', 'brand China site, title "本田中国官网": https://www.honda.com.cn/', '2026-11-11')},
 'Chantecaille': {'zh': ('CONFIRMED', 'brand China site, "CHANTECAILLE 香缇卡" and 香缇卡商贸（上海）有限公司: https://www.chantecaille.com.cn/', '2026-11-11')},
 'Focal': {'ko': ('UNCONFIRMED', 'brand Korea site focal.com/ko writes Latin "Focal" throughout; 포칼 not seen: https://www.focal.com/ko', '2026-11-11'), 'zh': ('UNCONFIRMED', 'brand China site focal.cn writes Latin "Focal" throughout; 劲浪 not seen: https://www.focal.cn', '2026-11-11')},
 'Grey Goose': {'ko': ('UNCONFIRMED', 'brand site greygoose.com has no Korean version (English and European languages only); 그레이구스 not seen: https://www.greygoose.com/', '2026-11-11'), 'zh': ('UNCONFIRMED', 'brand site greygoose.com has no Chinese version; 灰雁 not seen: https://www.greygoose.com/', '2026-11-11')},
 "Hendrick's": {'ko': ('UNCONFIRMED', 'brand site hendricksgin.com English only; 헨드릭스 not seen: https://www.hendricksgin.com/', '2026-11-11'), 'zh': ('UNCONFIRMED', 'brand site hendricksgin.com English only; 亨利爵士 not seen: https://www.hendricksgin.com/', '2026-11-11')},
 'Woodford Reserve': {'ko': ('UNCONFIRMED', 'brand site woodfordreserve.com has no Korean version; 우드포드 리저브 not seen: https://www.woodfordreserve.com/', '2026-11-11'), 'zh': ('UNCONFIRMED', 'brand site woodfordreserve.com has no Chinese version; 活福 not seen: https://www.woodfordreserve.com/', '2026-11-11')},
 'Koss': {'ko': ('UNCONFIRMED', 'brand site koss.com English only; 코스 not seen: https://www.koss.com/', '2026-11-11'), 'zh': ('UNCONFIRMED', 'brand site koss.com English only; 高斯 not seen: https://www.koss.com/', '2026-11-11')},
 'Jameson': {'ko': ('CONFIRMED', 'Pernod Ricard Korea (local subsidiary) brand page, "제임슨은 아일랜드 더블린에 본사가 위치한": https://www.pernod-ricard-korea.com/brands/jameson', '2026-11-11')},
 'Monkey 47': {'ko': ('CONFIRMED', 'Pernod Ricard Korea (local subsidiary) brand page, "몽키 47" (also "몽키47" once): https://www.pernod-ricard-korea.com/brands/monkey-47', '2026-11-11')},
 'Eucerin': {'ko': ('CONFIRMED', 'Beiersdorf Korea (brand owner, Korean corporate site), meta description "... 니베아, 니베아 맨, 유세린, 라프레리 ...": https://www.beiersdorf.co.kr/', '2026-11-11'), 'zh': ('CONFIRMED', 'Beiersdorf China (brand owner, Chinese corporate site), brand list and brand page 优色林: https://www.zh.beiersdorf.cn/', '2026-11-11')},
}


def main():
    src = list(csv.DictReader(open(SRC, encoding='utf-8')))
    rows = []
    for r in src:
        b = r['brand']
        ko, kocp, zh, zhcp, note = A[b]
        ck = CHECKS.get(b, {})
        kst = ck.get('ko', ('UNCONFIRMED', '', '')) if ko else ck.get('ko', ('NO ALIAS', '', ''))
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
