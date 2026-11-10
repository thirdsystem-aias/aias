# AIAS v1.13 — Source classification rule (DRAFT r1, to be sent to Pablo for the 24-hour review, 2026-11-10; frozen at the Part I lock)

Applies to every retrieved URL (`search.sources`, the primary field) and every cited URL (`search.citations`, sensitivity S2) in a t4 S1 record [RE-ANALYSIS: t4]. Written before any t4 answer exists and before v0.42's own S1 domain descriptives are computed; no search-on answer was read to write it (the declared v0.39 pilot was dropped before it was run). The fenced `classes:` blocks below are the **machine copy**: `score_v1_13.py` reads them from this file, so the anchored SHA-256 of this file pins the rule. No domain is added, moved or removed after the first t4 S1 record is read; later additions run only as a labelled exploratory sensitivity.

## 1. URL normalisation (U1–U6)

- **U1.** Trim; a URL without a scheme gets `https://`. Parse with Python `urllib.parse.urlsplit`. No URL is fetched or resolved.
- **U2.** Host = lower-cased hostname, trailing dot removed, IDNA left as given. Drop leading labels `www`, `www2`, `m`, `amp`, `mobile` (one pass, left to right).
- **U3.** Path = lower-cased path; query and fragment dropped (removes `utm_*`, OpenAI's `?utm_source=openai`, `#:~:text=` fragments).
- **U4.** Registrable domain = the last two labels of the host, or the last three when the last two are in the `classes:multi_suffix` list below. IPv4 hosts and hosts without a dot → `unresolved`.
- **U5 (Google redirects).** If the host is in `classes:redirect_hosts`, the domain is taken from the record's `title` when `title` matches `^[a-z0-9-]+(\.[a-z0-9-]+)+$` after lower-casing and U2/U4; otherwise the source is `unresolved`. The redirect is never followed.
- **U6.** Within one answer, sources are de-duplicated by normalised URL (host + path) for counts of sources and by registrable domain for counts of domains and for class shares.

## 2. Class precedence (first match wins)

1. **brand_owned**: registrable domain ∈ D_b for any brand b of the answer's substrate (`registries/brand_domains_v1_13.csv`, rows with status RESOLVED: domain and aliases). For a brand's own-domain share, only that brand's D_b counts. A brand page on a third-party platform (e.g. a social profile, a marketplace storefront) is **not** brand-owned.
2. **reference**: `classes:reference` domains, any `*.wikipedia.org`, and the TLD rule: registrable domain ending `.gov`, `.edu`, `.gov.uk`, `.ac.uk`, `.mil`.
3. **forum_ugc**: `classes:forum_ugc` (forums, Q&A, social, video, user-review platforms).
4. **news**: `classes:news`.
5. **review_editorial**: `classes:review_editorial`, plus the path overrides in `classes:path_overrides` (checked before the domain lists: a host+path prefix match assigns its class).
6. **retailer**: `classes:retailer` (retailers, marketplaces, dealer/marketplace aggregators).
7. **Host-pattern rules** (on the full normalised host, in this order): host starts with `forum.`, `forums.`, `community.`, `discuss.` → forum_ugc; host contains `wiki` → reference; host starts with `shop.` or `store.` and the registrable domain is not in any D_b → retailer; host starts with `news.` → news.
8. **other**: everything else that resolved. **unresolved**: U4/U5 failures.

`other` and `unresolved` shares are reported (MQ3); they are never re-coded by hand in the confirmatory analysis.

## 3. Domain lists (machine copy)

```classes:multi_suffix
co.uk org.uk ac.uk gov.uk com.au net.au org.au co.jp ne.jp or.jp co.kr com.br com.cn com.mx co.nz co.za com.sg com.tw com.hk co.in com.tr com.ar co.il com.my com.ph
```

```classes:redirect_hosts
vertexaisearch.cloud.google.com
```

```classes:path_overrides
nytimes.com/wirecutter review_editorial
nytimes.com/athletic news
```

```classes:reference
wikipedia.org wikidata.org wikimedia.org wiktionary.org britannica.com investopedia.com statista.com merriam-webster.com dictionary.com worldcat.org archive.org ncbi.nlm.nih.gov nih.gov fda.gov epa.gov nhtsa.gov fueleconomy.gov ttb.gov sec.gov crunchbase.com bloomberg.com/profile
```

```classes:forum_ugc
reddit.com quora.com youtube.com youtu.be tiktok.com instagram.com facebook.com x.com twitter.com pinterest.com medium.com substack.com tumblr.com threads.net linkedin.com head-fi.org audiosciencereview.com superbestaudiofriends.org stackexchange.com trustpilot.com yelp.com makeupalley.com beautypedia.com influenster.com bimmerpost.com rennlist.com teslamotorsclub.com straightbourbon.com whiskybase.com distiller.com untappd.com fragrantica.com basenotes.com
```

```classes:news
nytimes.com wsj.com washingtonpost.com usatoday.com cnn.com cnbc.com bbc.com bbc.co.uk reuters.com apnews.com bloomberg.com forbes.com businessinsider.com theguardian.com ft.com economist.com time.com latimes.com npr.org nbcnews.com cbsnews.com abcnews.go.com foxnews.com fortune.com axios.com theatlantic.com newsweek.com nypost.com independent.co.uk telegraph.co.uk dailymail.co.uk yahoo.com msn.com fastcompany.com adage.com adweek.com marketwatch.com businesswire.com prnewswire.com globenewswire.com
```

```classes:review_editorial
rtings.com whathifi.com soundguys.com stereophile.com headphonecheck.com techradar.com tomsguide.com cnet.com theverge.com wired.com engadget.com pcmag.com digitaltrends.com zdnet.com androidauthority.com gearpatrol.com crutchfield.com/learn consumerreports.org caranddriver.com motortrend.com edmunds.com kbb.com jdpower.com topgear.com autoblog.com roadandtrack.com thedrive.com insideevs.com electrek.co autoweek.com autocar.co.uk carwow.co.uk whatcar.com iihs.org byrdie.com allure.com vogue.com harpersbazaar.com elle.com cosmopolitan.com glamour.com refinery29.com intothegloss.com healthline.com womenshealthmag.com menshealth.com goodhousekeeping.com marieclaire.com instyle.com self.com prevention.com verywellhealth.com who.com liquor.com vinepair.com whiskyadvocate.com thespruceeats.com foodandwine.com punchdrink.com diffordsguide.com breakingbourbon.com robbreport.com esquire.com gq.com bonappetit.com seriouseats.com tastingtable.com thewhiskeywash.com whiskyreviewer.com bourbonculture.com wine-searcher.com winemag.com decanter.com
```

```classes:retailer
amazon.com amazon.co.uk amazon.ca walmart.com target.com bestbuy.com crutchfield.com sweetwater.com bhphotovideo.com adorama.com headphones.com moon-audio.com audio46.com audioadvice.com ebay.com costco.com sephora.com ulta.com dermstore.com nordstrom.com macys.com bloomingdales.com saksfifthavenue.com neimanmarcus.com cvs.com walgreens.com lookfantastic.com cultbeauty.co.uk spacenk.com revolve.com credobeauty.com totalwine.com drizly.com reservebar.com masterofmalt.com thewhiskyexchange.com wine.com bevmo.com caskers.com flaviar.com klwines.com astorwines.com carvana.com carmax.com autotrader.com cars.com truecar.com cargurus.com
```

## 4. Notes

- Overlaps are resolved by precedence (§2): e.g. `bloomberg.com` is news, `crutchfield.com/learn` is review_editorial by path override only if listed in `path_overrides` (it is listed under review_editorial as a host+path entry and is treated as a path override by the scorer; plain `crutchfield.com` is retailer).
- Entries containing `/` in any list are host+path prefixes and are checked before plain domains (§2, item 5).
- Before the lock the runner may add domains to these lists from category knowledge only (no search-on answer is read; the v0.39 pilot was dropped); every addition is logged in the change log of the pre-registration. None after the first t4 S1 record is read. None was added between the draft and sending (2026-11-10).
