#!/usr/bin/env python3
"""QA gate for a static SEO/AEO/GEO site. Usage: check_site.py <site_dir> [--definition "one line"]"""
import sys, os, re, json, argparse
from html.parser import HTMLParser
from xml.etree import ElementTree as ET

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.t=None; s.intitle=False; s.meta={}; s.links=[]; s.h1=0
        s.canon=None; s.lang=None; s.ld=[]; s.inld=False; s.buf=""; s.text=[]; s.inscript=False
    def handle_starttag(s,tag,a):
        a=dict(a)
        if tag=="html": s.lang=a.get("lang")
        if tag=="title": s.intitle=True
        if tag=="meta": s.meta[a.get("name") or a.get("property")]=a.get("content")
        if tag=="link" and a.get("rel")=="canonical": s.canon=a.get("href")
        if tag=="a" and a.get("href"): s.links.append(a["href"])
        if tag=="h1": s.h1+=1
        if tag=="script":
            s.inscript=True
            if a.get("type")=="application/ld+json": s.inld=True; s.buf=""
    def handle_endtag(s,tag):
        if tag=="title": s.intitle=False
        if tag=="script":
            if s.inld: s.ld.append(s.buf)
            s.inld=False; s.inscript=False
    def handle_data(s,d):
        if s.intitle: s.t=(s.t or "")+d
        if s.inld: s.buf+=d
        elif not s.inscript: s.text.append(d)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("site"); ap.add_argument("--definition")
    o=ap.parse_args(); root=o.site.rstrip("/"); errs=[]; pages=[]
    for d,_,fs in os.walk(root):
        for f in fs:
            if f.endswith(".html") and f!="404.html": pages.append(os.path.join(d,f))
    for f in ["robots.txt","sitemap.xml","llms.txt","llms-full.txt","ai.txt","feed.xml","site.webmanifest"]:
        if not os.path.exists(os.path.join(root,f)): errs.append(f"missing {f}")
    sm=set()
    try:
        for loc in ET.parse(os.path.join(root,"sitemap.xml")).iter():
            if loc.tag.endswith("loc") and loc.text: sm.add(re.sub(r"^https?://[^/]+","",loc.text.strip()))
    except Exception as e: errs.append(f"sitemap.xml invalid: {e}")
    for xf in ["feed.xml","blog/feed.xml"]:
        p=os.path.join(root,xf)
        if os.path.exists(p):
            try: ET.parse(p)
            except Exception as e: errs.append(f"{xf} invalid: {e}")
    for p in pages:
        rel=os.path.relpath(p,root); h=P(); html=open(p,encoding="utf-8").read(); h.feed(html)
        tag=lambda m: errs.append(f"{rel}: {m}")
        if not h.t or len(h.t.strip())>65: tag("title missing or >65 chars")
        if not h.meta.get("description") or len(h.meta["description"])>160: tag("meta description missing or >160")
        if not h.canon: tag("no canonical")
        if h.h1!=1: tag(f"{h.h1} H1s")
        if not h.lang: tag("no html lang")
        if not h.meta.get("og:image"): tag("no og:image")
        faq_q=[]
        for b in h.ld:
            try: j=json.loads(b)
            except Exception as e: tag(f"JSON-LD parse error: {e}"); continue
            for n in (j.get("@graph") if isinstance(j,dict) and "@graph" in j else (j if isinstance(j,list) else [j])):
                if "@type" not in n: tag("JSON-LD node without @type")
                if n.get("@type")=="FAQPage": faq_q+= [q.get("name","") for q in n.get("mainEntity",[])]
        body=" ".join(h.text)
        for q in faq_q:
            if q and q not in body: tag(f"FAQ schema question not visible on page: {q[:60]}")
        url="/"+rel.replace("index.html","")
        if not any(x==url or x.endswith(url if url!="/" else "/") and (url!="/" or x.count("/")<=2) for x in sm) and not any(x.endswith("/"+rel) for x in sm): tag("not in sitemap")
        for l in h.links:
            if l.startswith(("http","mailto:","tel:","#","javascript:")): continue
            l=l.split("#")[0].split("?")[0]
            t=os.path.normpath(os.path.join(root, l.lstrip("/")) if l.startswith("/") else os.path.join(os.path.dirname(p), l or "."))
            if os.path.isdir(t): t=os.path.join(t,"index.html")
            if not os.path.exists(t): tag(f"broken internal link {l}")
        if re.search(r"\b(TODO|lorem ipsum|TBD)\b",html,re.I): tag("placeholder text")
        if o.definition and rel=="index.html" and o.definition not in html: tag("one-line definition not on home page")
    if o.definition:
        for f in ["llms.txt","llms-full.txt"]:
            p=os.path.join(root,f)
            if os.path.exists(p) and o.definition not in open(p,encoding="utf-8").read(): errs.append(f"{f}: one-line definition differs")
    print(f"{len(pages)} pages checked")
    print("\n".join(errs) if errs else "PASS")
    sys.exit(1 if errs else 0)

if __name__=="__main__": main()
