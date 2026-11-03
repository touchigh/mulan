#!/usr/bin/env python3
"""Post-deploy live audit for a SEO/AEO/GEO site. Usage: live_audit.py https://example.com[/subpath]
Crawls every sitemap URL and checks what crawlers and answer engines actually receive."""
import sys, json, urllib.request, urllib.parse, concurrent.futures as cf
from html.parser import HTMLParser
from xml.etree import ElementTree as ET
B = sys.argv[1].rstrip("/")
HOST = "{0.scheme}://{0.netloc}".format(urllib.parse.urlparse(B))
def get(u):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 seo-live-audit"}), timeout=30)
        return r.status, r.read().decode("utf-8", "replace"), r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e: return e.code, "", ""
    except Exception as e: return 0, str(e), ""
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.d = {"title": "", "meta": {}, "alts": {}, "h1": 0, "ld": [], "imgs": [], "ids": set(), "lang": None, "canon": None}; s.t = s.l = 0; s.buf = ""
    def handle_starttag(s, t, a):
        a = dict(a); d = s.d
        if "id" in a: d["ids"].add(a["id"])
        if t == "html": d["lang"] = a.get("lang")
        if t == "title": s.t = 1
        if t == "meta": d["meta"][a.get("name") or a.get("property")] = a.get("content")
        if t == "link" and a.get("rel") == "canonical": d["canon"] = a.get("href")
        if t == "link" and a.get("rel") == "alternate" and a.get("hreflang"): d["alts"][a["hreflang"]] = a["href"]
        if t == "img": d["imgs"].append(a)
        if t == "h1": d["h1"] += 1
        if t == "script" and a.get("type") == "application/ld+json": s.l = 1; s.buf = ""
    def handle_endtag(s, t):
        if t == "title": s.t = 0
        if t == "script" and s.l: s.d["ld"].append(s.buf); s.l = 0
    def handle_data(s, x):
        if s.t: s.d["title"] += x
        if s.l: s.buf += x
issues, warn = [], []
# 1. host-root discovery files (crawlers only read robots.txt at the host root)
for f, need in [("robots.txt", "Sitemap:"), ("llms.txt", "#"), (".well-known/security.txt", "Contact:")]:
    c, body, _ = get(f"{HOST}/{f}")
    if c != 200 or need not in body:
        (issues if f == "robots.txt" else warn).append(f"host root /{f} -> HTTP {c}" + (" (site is on a subpath: use a custom domain or the <owner>.github.io repo)" if B != HOST else ""))
for f in ["robots.txt", "sitemap.xml", "llms.txt", "llms-full.txt", "ai.txt", "feed.xml", ".well-known/security.txt"]:
    c, _, ct = get(f"{B}/{f}")
    if c != 200: issues.append(f"{B}/{f} HTTP {c}" + (" (dot-folder missing: deploy with git push, not browser upload)" if f.startswith(".") else ""))
c, sm, _ = get(B + "/sitemap.xml")
urls = [l.text.strip() for l in ET.fromstring(sm).iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")] if c == 200 else []
res = {}
with cf.ThreadPoolExecutor(12) as ex:
    for u, r in zip(urls, ex.map(get, urls)): res[u] = r
titles, descs, ogs, types = {}, {}, set(), {}
REQ = {"Organization": ["name", "url", "logo"], "BlogPosting": ["headline", "datePublished", "author", "image", "publisher"],
       "FAQPage": ["mainEntity"], "BreadcrumbList": ["itemListElement"], "SoftwareApplication": ["name", "applicationCategory"], "WebSite": ["name", "url"]}
for u, (c, h, ct) in res.items():
    if c != 200: issues.append(f"{u} HTTP {c}"); continue
    p = P(); p.feed(h); d = p.d
    if d["canon"] != u: issues.append(f"{u} canonical -> {d['canon']}")
    titles.setdefault(d["title"].strip(), []).append(u); descs.setdefault(d["meta"].get("description"), []).append(u)
    if d["h1"] != 1: issues.append(f"{u} has {d['h1']} H1")
    if "max-snippet:-1" not in (d["meta"].get("robots") or ""): warn.append(f"{u} robots meta lacks max-snippet:-1")
    if d["alts"]:
        if "x-default" not in d["alts"]: issues.append(f"{u} hreflang without x-default")
        for lang, href in d["alts"].items():
            if lang in ("x-default", d["lang"]): continue
            if href not in res: issues.append(f"{u} hreflang {lang} target not in sitemap"); continue
            q = P(); q.feed(res[href][1])
            if q.d["alts"].get(d["lang"]) != u: issues.append(f"{u} hreflang {lang} not reciprocal")
    ogs.add(d["meta"].get("og:image"))
    for i in d["imgs"]:
        if i.get("alt") is None: issues.append(f"{u} <img> without alt")
        if not i.get("width"): warn.append(f"{u} <img> without width/height (CLS)")
    for b in d["ld"]:
        try: j = json.loads(b)
        except Exception as e: issues.append(f"{u} JSON-LD parse error {e}"); continue
        t = j.get("@type"); types[t] = types.get(t, 0) + 1
        for k in REQ.get(t, []):
            if k not in j: issues.append(f"{u} {t} missing {k}")
        if t == "SoftwareApplication" and "offers" in j and "price" not in j["offers"]: issues.append(f"{u} Offer without price (invalid for rich results)")
        if t == "SoftwareApplication" and "offers" not in j and "aggregateRating" not in j: warn.append(f"{u} {j.get('name')}: no price/rating, so no software rich result (fine if no public price)")
        if t == "BlogPosting" and j.get("author", {}).get("@type") != "Person": warn.append(f"{u} BlogPosting author is not a Person (weaker E-E-A-T)")
        if t == "FAQPage":
            for q in j["mainEntity"]:
                if q["name"] not in h: issues.append(f"{u} FAQ schema question not visible on page")
        if "speakable" in j:
            for sel in j["speakable"].get("cssSelector", []):
                if sel.lstrip("#") not in d["ids"]: issues.append(f"{u} speakable target {sel} missing")
for t, us in titles.items():
    if len(us) > 1: issues.append(f"duplicate <title> {t!r} on {len(us)} pages")
for t, us in descs.items():
    if len(us) > 1: issues.append(f"duplicate meta description on {len(us)} pages")
for o in ogs:
    if not o or get(o)[0] != 200: issues.append(f"og:image unreachable {o}")
c, body, _ = get(B + "/llms.txt")
for link in set(__import__("re").findall(r"\((https?://[^)]+)\)", body)):
    if get(link)[0] != 200: issues.append(f"llms.txt link dead {link}")
print(f"{len(res)} sitemap URLs crawled · JSON-LD types: {types}")
for w in sorted(set(warn), key=lambda x: (x.split(' ')[-1], x))[:25]: print("WARN ", w)
for i in sorted(set(issues)): print("FAIL ", i)
print("PASS" if not issues else f"{len(set(issues))} failing checks")
sys.exit(1 if issues else 0)
