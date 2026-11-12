"""Build registries/domain_table_v1_18.csv from the blind domain list (outputs/prelock/domains_to_classify_v1_18.txt)
under the rules of registries/domain_rules_v1_18.md (T0-T3, classes C/L/R/E). The hand classifications below were
written by the coder (Claude, runner lane H, 2026-11-12) from the alphabetical list of cited domains only: no
count, model, answer, brand or Grounding share was visible. Anything not recognised from the domain and general
knowledge (no page was opened) is UNRESOLVED. Rows: domain, class, rule, retailer, alias_of, note.
"""
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import common_v1_18 as C  # noqa: E402

HAND = {
    "company": """alfaromeousa.com altamarbrands.com amraandelma.com arkansasdermatology.com astonmartin.com babor.com
barrellbourbon.com beamdistilling.com buffalotracedistillery.com camparigroup.com chopinimports.com clinique.com
diageo.com elcompanies.com eltamd.com ferrandcognac.com ferrari.com focal-naim.com fourpillarsgin.com
fourrosesbourbon.com genesisnewsusa.com heavenhill.com heavenhilldistillery.com hernogin.com hombo.co.jp kajabeauty.com
kavalanwhisky.com kinobigin.com laphroaig.com laroche-posay.us maltmarketing.com makeupforever.com marshall.com
mhwltd.com midwestwhiskeybuyer.com onlinemakeupacademy.com pmspirits.com proceragin.com roonlabs.com
sanovadermatology.com schweigerderm.com selfnamed.com sennheiser-hearing.com skurnik.com starward.com.au subaru.com
suntory.com suntoryglobalspirits.com tntfireworks.com truespot.com vanicream.com vinovest.co williamgrant.com
worthyparkestate.com""",
    "listing": """asos.com binnys.com christies.com cosmetify.com cultbeauty.com eneba.com flaskfinewines.com ipsy.com
makersrow.com sevenfifty.com sothebys.com spiritory.com tastersclub.com unicornauctions.com whisky.auction
worldwidestereo.com bloomaudio.com""",
    "review_social": """avforums.com consumeraffairs.com rumx.com""",
    "editorial_other": """aad.org aarp.org aiga.org ama-assn.org americansalon.com aol.com ascension.org ascotawards.com
audiophileon.com autonocion.com barbadostoday.bb bartenderspiritsawards.com beautymatter.com beautypackaging.com
bevnet.com buffalotracedaily.com bustle.com carcody.com caredge.com carpro.com cbinsights.com chowhound.com
clevelandclinic.org cluboenologique.com consumerhealthdigest.com cosmeticsbusiness.com coveteur.com dealershipguy.com
digiday.com digitaldealer.com dmagazine.com drinksint.com dw.com ecoustics.com elpais.com escholarship.org
fashionista.com globalbrandsmagazine.com grandviewresearch.com guideautoweb.com headphoneer.com headphonesaddict.com
headphonesty.com hellobeautiful.com hometheaterhifi.com huffpost.com ieee.org iheart.com imbibemagazine.com
insidehook.com internationalspiritschallenge.com itechguides.com iwsc.net jalopnik.com keyt.com kqed.org kybourbon.com
lemonde.fr marieclaire.co.uk marketingbrew.com maxim.com mensjournal.com mezcalistas.com motor1.com
mydigitalpublication.com nasdaq.com nationalgalleries.org nationalgeographic.com newbeauty.com newsnationnow.com
newswire.ca pagesuite.com peakofohio.com pickuptrucktalk.com popdust.com prnewswire.co.uk qz.com rankandstyle.com
rarebird101.com rd.com roadethos.com rumporter.com saveur.com scotchwhisky.com scotsman.com sfgate.com
smithsonianmag.com sociallifemagazine.com soundonsound.com soundstagehifi.com spglobal.com spiritsanddistilling.com
spritmuseum.se strongmocha.com t3.com tagspiritsawards.com talesofthecocktail.org tapeop.com teenvogue.com
tequilareport.com theautochannel.com thebourbonconcierge.com thedailymeal.com thedailypour.com thedailywhisky.com
thedermdigest.com thedrum.com thegoodtrade.com thehandbook.com thehill.com thespiritsbusiness.com
thetastingalliance.com thezoereport.com timesunion.com topspeed.com trillmag.com uproxx.com usc.edu case.edu
lsuhsc.edu edu.et visualcapitalist.com wallpaper.com warc.com wdrb.com wgauradio.com whiskymag.com whowhatwear.com
wineenthusiast.com womanandhome.com wwd.com yougov.com zinio.com""",
}
RETAILER = set("""asos.com binnys.com christies.com cosmetify.com cultbeauty.com eneba.com flaskfinewines.com ipsy.com
sevenfifty.com sothebys.com spiritory.com tastersclub.com unicornauctions.com whisky.auction worldwidestereo.com
bloomaudio.com""".split())
V113_MAP = {"retailer": "listing", "forum_ugc": "review_social", "news": "editorial_other",
            "review_editorial": "editorial_other", "reference": "editorial_other"}


def main():
    s = C.load_v113()
    classes = s.load_classes(C.V113_CLASSES)
    units = s.load_brand_domains(C.V113_DOMAINS)
    all_db = set().union(*[u["domains"] for u in units.values()])
    hand = {}
    for cls, body in HAND.items():
        for d in body.split():
            if d in hand:
                raise SystemExit(f"hand-classified twice: {d}")
            hand[d] = cls
    names = {}
    for u in units.values():                         # registry names only (no answer is read): alias candidates
        tok = re.sub(r"[^a-z0-9]", "", u["brand"].lower())
        if len(tok) >= 4:
            names.setdefault(tok, set()).add(f'{u["substrate"]}:{u["brand_id"]}')
    blind = (C.PHASE / "outputs" / "prelock" / "domains_to_classify_v1_18.txt").read_text().split()
    cited = set((C.PHASE / "outputs" / "prelock" / "domains_to_classify_cited_v1_18.txt").read_text().split())
    rows = []
    for d in sorted(all_db):                         # T0
        rows.append([d, "company", "T0", "", "", "registry D_b domain (v1.13, frozen): focal for its own unit"])
    for d in blind:
        if d in all_db:
            continue
        v113 = classes["plain"].get(d)
        tld = d.endswith((".gov", ".edu", ".mil")) or d.endswith((".gov.uk", ".ac.uk")) or d == "wikipedia.org"
        if v113 or tld:                              # T1
            cls, rule = (V113_MAP[v113] if v113 else "editorial_other"), "T1"
        elif d in hand:                              # T2
            cls, rule = hand[d], "T2"
        else:                                        # T3
            cls, rule = "UNRESOLVED", "T3"
        retailer = "1" if (d in RETAILER or v113 == "retailer") else ""
        alias = ";".join(sorted(x for t, xs in names.items() if t in re.sub(r"[^a-z0-9]", "", d) for x in xs))
        note = "cited" if d in cited else "sources-only: not hand-classified in r1 draft" if rule == "T3" else ""
        rows.append([d, cls, rule, retailer, alias, note])
    unused = sorted(set(hand) - set(blind))
    if unused:
        raise SystemExit(f"hand entries not in the blind list: {unused}")
    with open(C.DOMAIN_TABLE, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["domain", "class", "rule", "retailer", "alias_of", "note"])
        w.writerows(rows)
    print(len(rows), "rows")


if __name__ == "__main__":
    main()
