#!/usr/bin/env python3
"""AIAS v0.62 (r1 draft): check the Japanese (and French) alias table against dated public sources.

No model is called. Two sources are opened for each unit, over plain HTTPS GET, and recorded with the UTC date:
  1. the brand's own Japanese site, where one is listed in OFFICIAL below (the page's HTML is searched for each
     alias, ignoring the separators ・ ･ and spaces);
  2. Wikipedia: the Japanese article linked from the English article of the brand (MediaWiki API, `langlinks`),
     whose title is compared with the aliases in the same way.
A unit is CONFIRMED if every alias in the table is found in at least one source (official site preferred), PARTIAL
if some but not all are, CHANGED if a source shows a katakana form that is not in the table (the form is reported;
the table is changed by hand, with the source, in brand_aliases_v0_62_r1.csv), UNCONFIRMED otherwise (no source
opened or none shows any alias). French: the table has no French-specific name, only unaccented spellings, which
need no source (they are spelling variants of the registry string).

Run: python3 osf/v62/scripts/check_aliases_v0_62.py -> osf/v62/translations/alias_check_v0_62_r1.csv
"""
import csv
import json
import os
import re
import sys
import unicodedata
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
V62 = os.path.normpath(os.path.join(HERE, '..'))
TABLE = os.path.join(V62, 'translations', 'brand_aliases_v0_62_r0.csv')
OUT = os.path.join(V62, 'translations', 'alias_check_v0_62_r1.csv')
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Safari/605.1.15',
      'Accept-Language': 'ja,en;q=0.5'}

OFFICIAL = {
    'Audio-Technica': 'https://www.audio-technica.co.jp/',
    'Denon': 'https://www.denon.jp/ja-jp',
    'Final Audio': 'https://snext-final.com/',
    'HiFiMan': 'https://hifiman.jp/',
    'Sennheiser': 'https://www.sennheiser.com/ja-jp',
    'Sony': 'https://www.sony.jp/',
    'Stax': 'https://stax.co.jp/',
    'Beyerdynamic': 'https://www.beyerdynamic.co.jp/',
    'Focal': 'https://www.focal.com/ja',
    'Estée Lauder': 'https://www.esteelauder.jp/',
    'Lancôme': 'https://www.lancome.jp/',
    'La Mer': 'https://www.cremedelamer.jp/',
    'Sisley': 'https://www.sisley-paris.com/ja-JP/',
    'Dior Beauty': 'https://www.dior.com/ja_jp/beauty',
    'Chanel Beauty': 'https://www.chanel.com/jp/',
    'La Prairie': 'https://www.laprairie.com/ja-jp',
    'Clé de Peau Beauté': 'https://www.cledepeau-beaute.com/jp/',
    'Drunk Elephant': 'https://www.drunkelephant.jp/',
    'Augustinus Bader': 'https://augustinusbader.jp/',
    'SkinCeuticals': 'https://www.skinceuticals.jp/',
    'La Roche-Posay': 'https://www.larocheposay.jp/',
    "Paula's Choice": 'https://www.paulaschoice.co.jp/',
    'CeraVe': 'https://www.cerave.jp/',
    'Cetaphil': 'https://www.cetaphil.jp/',
    'Eucerin': 'https://www.eucerin.jp/',
    'Bioderma': 'https://www.bioderma.jp/',
    'The Ordinary': 'https://theordinary.com/ja-jp/',
    'MAC Cosmetics': 'https://www.maccosmetics.jp/',
    'NARS': 'https://www.narscosmetics.jp/',
    'Bobbi Brown': 'https://www.bobbibrown.jp/',
    'Tom Ford Beauty': 'https://www.tomfordbeauty.jp/',
    'Giorgio Armani Beauty': 'https://www.armanibeauty.jp/',
    'Laura Mercier': 'https://www.lauramercier.jp/',
    'Charlotte Tilbury': 'https://www.charlottetilbury.com/jp',
    'Maybelline': 'https://www.maybelline.co.jp/',
    "L'Oréal Paris": 'https://www.loreal-paris.jp/',
    'Revlon': 'https://www.revlon.co.jp/',
    'NYX Professional Makeup': 'https://www.nyxcosmetics.jp/',
    'Rare Beauty': 'https://www.rarebeauty.com/ja-jp',
    'Mercedes-Benz': 'https://www.mercedes-benz.co.jp/',
    'Jaguar': 'https://www.jaguar.co.jp/',
    'Cadillac': 'https://www.cadillacjapan.com/',
    'Chevrolet': 'https://www.chevroletjapan.com/',
    'Rolls-Royce': 'https://www.rolls-roycemotorcars.com/ja_JP/home.html',
    'Bentley': 'https://www.bentleymotors.com/jp/ja.html',
    'Porsche': 'https://www.porsche.com/japan/jp/',
    'BMW': 'https://www.bmw.co.jp/ja/index.html',
    'Tesla': 'https://www.tesla.com/ja_jp',
    'Toyota': 'https://toyota.jp/',
    'Honda': 'https://www.honda.co.jp/',
    'Hyundai': 'https://www.hyundai.com/jp',
    'Volkswagen': 'https://www.volkswagen.co.jp/ja.html',
    'Nissan': 'https://www.nissan.co.jp/',
    'Polestar': 'https://www.polestar.com/jp/',
    'Johnnie Walker': 'https://www.johnniewalker.com/ja-jp/',
    'Hennessy': 'https://www.hennessy.com/ja-jp',
    "Jack Daniel's": 'https://www.jackdaniels.com/ja-jp',
    'Bacardi': 'https://www.bacardi.jp/',
    'Bombay Sapphire': 'https://www.bombaysapphire.com/jp/ja/',
    'Rémy Martin': 'https://www.remymartin.com/ja-jp/',
    'Nikka': 'https://www.nikka.com/',
    'The Balvenie': 'https://www.thebalvenie.com/ja-jp/',
    'Grey Goose': 'https://www.greygoose.com/ja-jp/',
    'Jameson': 'https://www.jamesonwhiskey.com/ja-jp/',
}

EN_TITLE = {
    'Final Audio': 'Final Audio Design', 'Koss': 'Koss Corporation', 'Grado': 'Grado Labs', 'Meze': 'Meze Audio',
    'Focal': 'Focal-JMlab', 'Stax': 'Stax Ltd.', 'HiFiMan': 'HiFiMAN', 'Dior Beauty': 'Parfums Christian Dior',
    'Chanel Beauty': 'Chanel', 'Rhode': 'Rhode (company)', 'Goop': 'Goop (company)', 'Tower 28': 'Tower 28 Beauty',
    'Tom Ford Beauty': 'Tom Ford (brand)', 'Giorgio Armani Beauty': 'Armani', 'Hourglass': 'Hourglass Cosmetics',
    'Milani Cosmetics': 'Milani Cosmetics', 'Jaguar': 'Jaguar Cars', 'Lucid': 'Lucid Motors', 'Fisker': 'Fisker Inc.',
    'Ford': 'Ford Motor Company', 'Plymouth': 'Plymouth (automobile)', 'Mercury': 'Mercury (automobile)',
    'Saturn': 'Saturn Corporation', 'Lagavulin': 'Lagavulin distillery', 'The Balvenie': 'Balvenie distillery',
    'Nikka': 'Nikka Whisky Distilling', "Hendrick's": "Hendrick's Gin", 'Grey Goose': 'Grey Goose (vodka)',
    'Jameson': 'Jameson Irish Whiskey', 'Redbreast': 'Redbreast (whiskey)', 'Fortaleza': 'Tequila Fortaleza',
    'Patrón': 'Patrón', 'Clé de Peau Beauté': 'Clé de Peau Beauté', 'Rare Beauty': 'Rare Beauty',
    'Fenty Skin': 'Fenty Beauty', 'Fenty Beauty': 'Fenty Beauty', 'Kylie Cosmetics': 'Kylie Cosmetics',
    'Haus Labs': 'Haus Labs', 'Pat McGrath Labs': 'Pat McGrath', 'Spirit Torino': 'Spirit Torino',
    'Dan Clark Audio': 'Dan Clark Audio', 'MAC Cosmetics': 'MAC Cosmetics', 'e.l.f. Cosmetics': 'e.l.f.',
    'Wet n Wild': 'Wet n Wild (cosmetics)', 'NYX Professional Makeup': 'NYX Cosmetics', 'St. George Spirits':
    'St. George Spirits', 'Monkey 47': 'Monkey 47', 'Mezcal Vago': 'Mezcal Vago', 'Del Maguey': 'Del Maguey',
}

SEP = re.compile(r'[・･\s　＝=]')


def norm(s):
    return SEP.sub('', unicodedata.normalize('NFKC', s or ''))


def get(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read(3_000_000)
        enc = r.headers.get_content_charset() or 'utf-8'
        return r.status, raw.decode(enc, 'replace')


def official(brand):
    url = OFFICIAL.get(brand)
    if not url:
        return None
    try:
        st, html = get(url)
        return {'url': url, 'status': st, 'text': norm(html)}
    except Exception as e:
        return {'url': url, 'status': f'ERR {type(e).__name__}', 'text': ''}


def wiki_titles(brands):
    out = {}
    titles = {b: EN_TITLE.get(b, b) for b in brands}
    inv = {}
    for b, t in titles.items():
        inv.setdefault(t, []).append(b)
    names = list(inv)
    for i in range(0, len(names), 40):
        chunk = names[i:i + 40]
        q = urllib.parse.urlencode({'action': 'query', 'titles': '|'.join(chunk), 'prop': 'langlinks', 'lllang': 'ja',
                                    'lllimit': 'max', 'redirects': 1, 'format': 'json'})
        url = 'https://en.wikipedia.org/w/api.php?' + q
        try:
            _st, txt = get(url, 30)
            j = json.loads(txt)
        except Exception as e:
            for t in chunk:
                for b in inv[t]:
                    out[b] = (None, f'ERR {type(e).__name__}', None)
            continue
        q = j.get('query', {})
        redir = {}
        for k in ('normalized', 'redirects'):
            for r in q.get(k, []):
                redir[r['from']] = r['to']
        pages = {p.get('title'): p for p in q.get('pages', {}).values()}
        for t in chunk:
            final = t
            while final in redir:
                final = redir[final]
            p = pages.get(final, {})
            ll = (p.get('langlinks') or [{}])[0].get('*')
            en_url = 'https://en.wikipedia.org/wiki/' + urllib.parse.quote(final.replace(' ', '_'))
            for b in inv[t]:
                out[b] = (ll, 'missing' if 'missing' in p else 'ok', en_url)
    return out


def main():
    rows = list(csv.DictReader(open(TABLE, encoding='utf-8')))
    today = datetime.now(timezone.utc).date().isoformat()
    brands = list(dict.fromkeys(r['brand'] for r in rows))
    with ThreadPoolExecutor(8) as ex:
        off = dict(zip(brands, ex.map(official, brands)))
    wk = wiki_titles(brands)
    out = []
    for r in rows:
        b = r['brand']
        aliases = [a for a in r['ja_aliases'].split('|') if a]
        o = off.get(b)
        ja_title, wst, en_url = wk.get(b, (None, 'n/a', None))
        found_off = [a for a in aliases if o and norm(a) in o['text']]
        found_wiki = [a for a in aliases if ja_title and norm(a) in norm(ja_title)]
        found = set(found_off) | set(found_wiki)
        kata_title = ja_title if ja_title and re.search(r'[゠-ヿ一-鿿]', ja_title) else None
        if not aliases:
            status = 'no alias (Latin only)'
        elif found and len(found) == len(aliases):
            status = 'CONFIRMED'
        elif found:
            status = 'PARTIAL'
        elif kata_title:
            status = 'CHANGED?'
        else:
            status = 'UNCONFIRMED'
        out.append({'substrate': r['substrate'], 'brand': b, 'ja_aliases': r['ja_aliases'], 'status': status,
                    'found_official': '|'.join(found_off), 'official_url': o['url'] if o else '',
                    'official_http': o['status'] if o else '', 'found_wikipedia': '|'.join(found_wiki),
                    'ja_wikipedia_title': ja_title or '', 'wikipedia_via': en_url or '', 'wikipedia_status': wst,
                    'accessed_utc': today})
    with open(OUT, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    from collections import Counter
    print(Counter(o['status'] for o in out))
    for o in out:
        if o['status'] != 'CONFIRMED':
            print(o['substrate'], o['brand'], o['ja_aliases'], o['status'], 'off:', o['official_http'], o['found_official'],
                  'wiki:', o['ja_wikipedia_title'])
    print('wrote', OUT)


if __name__ == '__main__':
    sys.exit(main())
