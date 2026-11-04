# -*- coding: utf-8 -*-
"""Static site generator for the MULAN 沐岚 SEO/AEO/GEO site (adapted from the seo-aeo-geo-website reference build).
Usage:  python -I build/build.py        (SITE_BASE env var overrides the base URL, e.g. for a local audit)
Writes into the repo root (= site root). Content: build/static_content.py, data/*.json, content/*.json."""
import json, os, re, html, glob, shutil, datetime, sys, urllib.parse
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from static_content import PRODUCTS, GROUPS, PILLARS, UI, HOME_FAQ, ABOUT, WHY, SRC, SRC_ZH

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = ROOT
BASE = os.environ.get("SITE_BASE", "https://touchigh.github.io/mulan").rstrip("/")
TODAY = "2026-11-04"
BRAND = json.load(open(os.path.join(SITE, "data/brand.json"), encoding="utf-8"))
ONE = {"en": BRAND["one_line_en"], "zh": BRAND["one_line_zh"]}
LANGS = ("en", "zh")
E = html.escape
PBY = {p["slug"]: p for p in PRODUCTS}
def pname(p, lang): return p["name_zh"] if lang == "zh" else p["name"]

POSTS = sorted([json.load(open(f, encoding="utf-8")) for f in glob.glob(os.path.join(SITE, "content/*.json"))], key=lambda p: p["n"])

def wa(text): return f"https://wa.me/{BRAND['whatsapp_digits']}?text={urllib.parse.quote(text)}"
def other(lang): return "zh" if lang == "en" else "en"
def pre(lang): return "zh/" if lang == "zh" else ""

# ---------- paths ----------
def page_path(kind, lang, slug=None):
    p = pre(lang)
    return {"home": p, "product": f"{p}products/{slug}/", "blog": f"{p}blog/", "post": f"blog/{slug}/", "about": f"{p}about/"}[kind]
def url(path): return f"{BASE}/{path}"
def rel(frm, to):
    depth = frm.count("/")
    return ("../" * depth) + to if depth else (to or "./")
def fix_links(body, frm):
    return re.sub(r'href="(/[^"]*)"', lambda m: f'href="{rel(frm, m.group(1).lstrip("/"))}"', body)

# ---------- shared chunks ----------
WORDMARK = '<span class="wm">沐岚 <b>MU LAN</b></span>'

def head(lang, path, title, desc, alt_path, og_img, ld, ogtype="website"):
    hl = ""
    if alt_path is not None:
        en_p, zh_p = (path, alt_path) if lang == "en" else (alt_path, path)
        hl = (f'<link rel="alternate" hreflang="en" href="{url(en_p)}">\n<link rel="alternate" hreflang="zh-CN" href="{url(zh_p)}">\n'
              f'<link rel="alternate" hreflang="x-default" href="{url(en_p)}">')
    ld_s = "\n".join(f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>' for b in ld)
    hlang = "zh-CN" if lang == "zh" else "en"
    return f"""<!doctype html>
<html lang="{hlang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<link rel="canonical" href="{url(path)}">
{hl}
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="MULAN 沐岚">
<meta property="og:locale" content="{UI[lang]['locale']}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url(path)}">
<meta property="og:image" content="{url(og_img)}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(desc)}">
<meta name="twitter:image" content="{url(og_img)}">
<meta name="theme-color" content="#1F4E7A">
<link rel="icon" href="{rel(path, 'favicon.svg')}" type="image/svg+xml">
<link rel="apple-touch-icon" href="{rel(path, 'assets/icon-192.png')}">
<link rel="manifest" href="{rel(path, 'site.webmanifest')}">
<link rel="alternate" type="application/rss+xml" title="MULAN blog" href="{rel(path, 'blog/feed.xml')}">
<link rel="stylesheet" href="{rel(path, 'assets/site.css')}">
{ld_s}
</head>"""

def header(lang, path, alt_path):
    u = UI[lang]; p = pre(lang); o = other(lang)
    sw = f'<a class="lang" href="{rel(path, alt_path)}" hreflang="{"zh-CN" if o=="zh" else "en"}" lang="{"zh-CN" if o=="zh" else "en"}">{"中文" if o=="zh" else "EN"}</a>' if alt_path is not None else ""
    return f"""<body>
<a class="skip" href="#main">{u['skip']}</a>
<header class="nav" role="banner"><div class="wrap navin">
<a class="brand" href="{rel(path, p)}" aria-label="MULAN home">{WORDMARK}</a>
<nav aria-label="Main"><ul>
<li><a href="{rel(path, p)}#products">{u['nav_products']}</a></li>
<li><a href="{rel(path, p + 'blog/')}">{u['nav_blog']}</a></li>
<li class="hide-s"><a href="{rel(path, p)}#faq">{u['nav_faq']}</a></li>
<li class="hide-s"><a href="{rel(path, p + 'about/')}">{u['nav_about']}</a></li>
</ul></nav>
<div class="navr">{sw}<a class="btn btn-red" href="{wa(u['wa_home'])}" rel="noopener">{u['cta']}</a></div>
</div></header>"""

def footer(lang, path):
    u = UI[lang]; p = pre(lang)
    prods = "".join(f'<li><a href="{rel(path, p + "products/" + x["slug"] + "/")}">{E(pname(x, lang))}</a></li>' for x in PRODUCTS)
    addr = BRAND["address_zh"] if lang == "zh" else BRAND["address_en"]
    legal = BRAND["legal_name_zh"] if lang == "zh" else BRAND["legal_name"]
    return f"""<footer class="foot" role="contentinfo"><div class="wrap fgrid">
<div><a class="brand light" href="{rel(path, p)}">{WORDMARK}</a><p>{u['footer_tag']}</p>
<address>{E(legal)}<br>{E(addr)}<br>WhatsApp <a href="{wa(u['wa_home'])}" rel="noopener">{BRAND['whatsapp']}</a></address></div>
<div><h2>{u['all_apps']}</h2><ul>{prods}</ul></div>
<div><h2>{u['nav_blog']}</h2><ul><li><a href="{rel(path, p + 'blog/')}">{u['blog_all']}</a></li><li><a href="{rel(path, p + 'about/')}">{u['nav_about']}</a></li><li><a href="{rel(path, 'llms.txt')}">llms.txt</a></li><li><a href="{rel(path, 'sitemap.xml')}">Sitemap</a></li></ul></div>
<div><h2>{u['nav_about']}</h2><ul><li>{E(BRAND['markets_zh'] if lang=='zh' else BRAND['markets_en'])}</li></ul></div>
</div><div class="wrap fine"><p>{u['disc']}</p><p>© 2026 {E(legal)}</p></div></footer>
</body></html>"""

def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": url(p)} for i, (n, p) in enumerate(items)]}
def crumbs_html(items, path):
    out = [f'<li><a href="{rel(path, p)}">{E(n)}</a></li>' if i < len(items) - 1 else f'<li aria-current="page">{E(n)}</li>' for i, (n, p) in enumerate(items)]
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(out)}</ol></nav>'
def faq_ld(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
def faq_html(faq, h, hid="faq"):
    items = "".join(f'<details><summary><h3>{E(q)}</h3></summary><p>{E(a)}</p></details>' for q, a in faq)
    return f'<section class="sec" id="{hid}" aria-labelledby="{hid}-h"><div class="wrap narrow"><h2 id="{hid}-h">{h}</h2><div class="faq">{items}</div></div></section>'

ORG = {"@context": "https://schema.org", "@type": "Organization", "@id": f"{BASE}/#org", "name": "MULAN", "alternateName": "沐岚",
       "legalName": BRAND["legal_name"], "url": f"{BASE}/", "logo": f"{BASE}/assets/icon-512.png", "description": BRAND["one_line_en"],
       "slogan": BRAND["concept_en"],
       "address": {"@type": "PostalAddress", **BRAND["address"]},
       "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "telephone": BRAND["whatsapp"], "url": wa(UI["en"]["wa_home"]),
                        "availableLanguage": ["English", "Chinese"], "areaServed": ["Middle East", "West Asia", "JP"]},
       "knowsAbout": ["aging-friendly bathroom products", "elderly bathroom safety", "seated showers", "toilet lift assist", "grab bars"]}

def product_ld(p, lang, path):
    c = p[lang]
    return {"@context": "https://schema.org", "@type": "Product", "name": pname(p, lang), "url": url(path), "description": c["answer"],
            "image": url("assets/img/products/" + p["img"]), "brand": {"@type": "Brand", "name": "MULAN"}, "manufacturer": {"@id": f"{BASE}/#org"},
            "category": GROUPS[p["group"]][lang], "inLanguage": "zh-CN" if lang == "zh" else "en",
            "additionalProperty": [{"@type": "PropertyValue", "name": a, "value": b} for a, b in c["proof"]]}

def write(path, content):
    fp = os.path.join(SITE, path, "index.html") if (path == "" or path.endswith("/")) else os.path.join(SITE, path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w", encoding="utf-8").write(content)
def wordcount(h): return len(re.sub(r"<[^>]+>", " ", h).split())

# ---------- images ----------
F = r"C:\Windows\Fonts"
def font(name, s):
    for n in ([name] if isinstance(name, str) else name):
        try: return ImageFont.truetype(os.path.join(F, n), s)
        except Exception: pass
    return ImageFont.load_default()
F_B = ["msyhbd.ttc", "segoeuib.ttf"]; F_R = ["msyh.ttc", "segoeui.ttf"]
def wrap_txt(d, text, f, maxw):
    toks = text.split() if " " in text else list(text)
    sep = " " if " " in text else ""
    lines, cur = [], ""
    for w in toks:
        t = (cur + sep + w) if cur else w
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines
def og(out, title, eyebrow, img=None):
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), "#EEF3F7"); d = ImageDraw.Draw(im)
    if img and os.path.exists(img):
        src = Image.open(img).convert("RGB"); src.thumbnail((470, 560))
        panel = Image.new("RGB", (500, H), "#FFFFFF"); panel.paste(src, ((500 - src.width) // 2, (H - src.height) // 2)); im.paste(panel, (W - 500, 0))
    tw = 600 if img else 1060
    d.text((64, 56), "沐岚", font=font(F_R, 34), fill="#12263D"); d.text((150, 58), "M U  L A N", font=font(F_B, 30), fill="#12263D")
    d.text((64, 150), eyebrow.upper(), font=font(F_B, 24), fill="#5F88B0")
    size = 58
    while size > 30:
        f = font(F_B, size); lines = wrap_txt(d, title, f, tw)
        if len(lines) <= 4: break
        size -= 4
    y = 196
    for ln in lines: d.text((64, y), ln, font=f, fill="#12263D"); y += int(size * 1.2)
    d.rounded_rectangle([64, H - 70, 124, H - 62], radius=4, fill="#1F4E7A")
    os.makedirs(os.path.dirname(out), exist_ok=True); im.save(out, "JPEG", quality=84, optimize=True)
def blog_imgs(slug):
    src = os.path.join(SITE, f"assets/img/blog/{slug}.png")
    if not os.path.exists(src): return os.path.exists(os.path.join(SITE, f"assets/img/blog/{slug}.jpg"))
    im = Image.open(src).convert("RGB")
    for w, h, suf in [(1536, 864, ""), (720, 405, "-card")]:
        r = max(w / im.width, h / im.height); t = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
        l, tp = (t.width - w) // 2, (t.height - h) // 2
        t.crop((l, tp, l + w, tp + h)).save(os.path.join(SITE, f"assets/img/blog/{slug}{suf}.jpg"), "JPEG", quality=82, optimize=True, progressive=True)
    return True
def img_size(rel_img):
    with Image.open(os.path.join(SITE, rel_img)) as im: return im.size

# ---------- pages ----------
def post_card(p, lang, frm):
    c = p["en"]; img = f'assets/img/blog/{p["slug"]}-card.jpg'
    im = f'<img src="{rel(frm, img)}" width="720" height="405" alt="{E(p.get("image_alt_en", ""))}" loading="lazy">' if os.path.exists(os.path.join(SITE, img)) else ""
    return f'<li class="pc" data-p="{p["pillar"]}"><a class="card post" href="{rel(frm, "blog/" + p["slug"] + "/")}" hreflang="en">{im}<span class="tag t-{p["pillar"]}">{PILLARS[p["pillar"]][lang]}</span><h3 lang="en">{E(c["title"])}</h3><p lang="en">{E(c["description"])}</p></a></li>'

def contact_band(lang, text=None):
    u = UI[lang]
    return f'<section class="sec"><div class="wrap"><div class="band"><h2>{u["contact_h"]}</h2><p>{u["contact_p"]}</p><a class="btn btn-red" style="background:#fff;color:#12263D" href="{wa(text or u["wa_home"])}" rel="noopener">{u["cta"]} · {BRAND["whatsapp"]}</a></div></div></section>'

def home(lang):
    u = UI[lang]; path = page_path("home", lang); alt = page_path("home", other(lang)); p = pre(lang)
    webpage = {"@context": "https://schema.org", "@type": "WebPage", "name": u["home_title"], "url": url(path), "inLanguage": "zh-CN" if lang == "zh" else "en",
               "description": u["home_desc"], "about": {"@id": f"{BASE}/#org"}, "dateModified": TODAY,
               "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["#answer-box"]}}
    website = {"@context": "https://schema.org", "@type": "WebSite", "@id": f"{BASE}/#site", "name": "MULAN 沐岚", "url": f"{BASE}/",
               "inLanguage": ["en", "zh-CN"], "publisher": {"@id": f"{BASE}/#org"}}
    itemlist = {"@context": "https://schema.org", "@type": "ItemList", "name": u["apps_h"],
                "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": url(page_path("product", lang, x["slug"])), "name": pname(x, lang)} for i, x in enumerate(PRODUCTS)]}
    ld = [ORG, website, webpage, itemlist, faq_ld(HOME_FAQ[lang]), crumbs_ld([(u["breadcrumb_home"], path)])]
    cards = "".join(f'<li><a class="card app" href="{rel(path, p + "products/" + x["slug"] + "/")}"><img src="{rel(path, "assets/img/products/" + x["img"])}" width="{img_size("assets/img/products/" + x["img"])[0]}" height="{img_size("assets/img/products/" + x["img"])[1]}" alt="{E(pname(x, lang))}" loading="lazy"><span class="tag">{GROUPS[x["group"]][lang]}</span><h3>{E(pname(x, lang))}</h3><p>{E(x[lang]["lead"])}</p><span class="more">{u["read"]} →</span></a></li>' for x in PRODUCTS)
    why = "".join(f'<li class="card why"><h3>{E(q)}</h3><p>{E(a)}</p><a href="{rel(path, p + "products/" + s + "/")}">{E(pname(PBY[s], lang))} →</a></li>' for q, a, s in WHY[lang])
    figs = [("135 kg", {"en": "rise-assist stand maximum load", "zh": "起身助力架最大载荷"}), ("20,000", {"en": "rise-assist lift cycles", "zh": "助力架使用寿命（次）"}),
            ("≤9 L/min", {"en": "seating shower water flow", "zh": "坐式淋浴器节水流量"}), ("250 kg", {"en": "folding stool maximum load", "zh": "折叠凳最大承重"})]
    figs_h = "".join(f'<li><b>{v}</b><span>{l[lang]}</span></li>' for v, l in figs)
    pcards = "".join(post_card(x, lang, path) for x in POSTS[:6])
    hw, hh = img_size("assets/img/products/seating-shower-scene.jpg")
    body = f"""<main id="main">
<section class="hero" aria-labelledby="hero-h"><div class="wrap"><div class="heropanel">
<div class="herotxt"><p class="eyebrow">{u['hero_eyebrow']}</p><h1 id="hero-h">{u['hero_h1']}</h1><p class="sub">{u['hero_sub']}</p>
<p class="ctas"><a class="btn btn-red" href="{wa(u['wa_home'])}" rel="noopener">{u['cta']}</a> <a class="btn btn-ghost" href="#products">{u['hero_cta2']}</a></p></div>
<div class="heroimg"><img src="{rel(path, 'assets/img/products/seating-shower-scene.jpg')}" width="{hw}" height="{hh}" alt="{E(pname(PBY['seating-shower'], lang))}" fetchpriority="high"></div>
</div></div></section>
<section class="sec answer" id="answer-box" aria-label="{u['answer_label']}"><div class="wrap narrow"><p class="eyebrow dark">{u['answer_label']}</p><p class="lead">{E(ONE[lang])}</p><p>{u['answer_more']}</p></div></section>
<section class="sec" aria-labelledby="figs-h"><div class="wrap"><h2 id="figs-h" class="center">{u['proof_h']}</h2><ul class="figs">{figs_h}</ul><p class="note center">{SRC_ZH if lang=='zh' else SRC}.</p></div></section>
<section class="sec tint" id="products" aria-labelledby="apps-h"><div class="wrap"><h2 id="apps-h" class="center">{u['apps_h']}</h2><p class="center sub2">{u['apps_sub']}</p><ul class="grid g4">{cards}</ul></div></section>
<section class="sec" aria-labelledby="why-h"><div class="wrap"><h2 id="why-h" class="center">{u['why_h']}</h2><ul class="grid g3">{why}</ul></div></section>
{faq_html(HOME_FAQ[lang], u['faq_h'])}
<section class="sec tint" aria-labelledby="blog-h"><div class="wrap"><h2 id="blog-h" class="center">{u['blog_h']}</h2><ul class="grid g3">{pcards}</ul><p class="center"><a class="btn btn-ghost" href="{rel(path, p + 'blog/')}">{u['blog_all']}</a></p></div></section>
{contact_band(lang)}
</main>"""
    write(path, head(lang, path, u["home_title"], u["home_desc"], alt, f"assets/og/home-{lang}.jpg", ld) + header(lang, path, alt) + body + footer(lang, path))
    og(os.path.join(SITE, f"assets/og/home-{lang}.jpg"), u["hero_h1"], u["hero_eyebrow"], os.path.join(SITE, "assets/img/products/seating-shower-scene.jpg"))

def product(x, lang):
    u = UI[lang]; c = x[lang]; p = pre(lang)
    path = page_path("product", lang, x["slug"]); alt = page_path("product", other(lang), x["slug"])
    items = [(u["breadcrumb_home"], p), (u["breadcrumb_products"], p + "#products"), (pname(x, lang), path)]
    page = {"@context": "https://schema.org", "@type": "WebPage", "name": c["title"], "url": url(path), "inLanguage": "zh-CN" if lang == "zh" else "en", "dateModified": TODAY,
            "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["#answer-box"]}, "about": {"@type": "Product", "name": pname(x, lang)}}
    ld = [ORG, product_ld(x, lang, path), page, faq_ld(c["faq"]), crumbs_ld(items)]
    who = "".join(f"<li>{E(i)}</li>" for i in c["who"]); prob = "".join(f"<li>{E(i)}</li>" for i in c["problems"])
    feats = "".join(f'<li class="card feat"><h3>{E(a)}</h3><p>{E(b)}</p></li>' for a, b in c["features"])
    specs = "".join(f'<li><b>{E(b)}</b><span>{E(a)}</span></li>' for a, b in c["proof"])
    rel_posts = [q for q in POSTS if q["product"] == x["slug"]] or [q for q in POSTS if q["pillar"] == ("projects" if x["group"] in ("space", "storage") else "safety")][:3]
    rp = "".join(post_card(q, lang, path) for q in rel_posts[:3])
    others = "".join(f'<li><a href="{rel(path, p + "products/" + o["slug"] + "/")}">{E(pname(o, lang))}</a></li>' for o in PRODUCTS if o["slug"] != x["slug"])
    iw, ih = img_size("assets/img/products/" + x["img"])
    watext = u["wa_product"].format(name=pname(x, lang))
    body = f"""<main id="main">
<section class="phero"><div class="wrap">{crumbs_html(items, path)}<div class="heropanel"><div class="herotxt"><p class="eyebrow">{GROUPS[x['group']][lang]}</p><h1>{E(c['h1'])}</h1><p class="sub">{E(c['lead'])}</p>
<p class="ctas"><a class="btn btn-red" href="{wa(watext)}" rel="noopener">{u['cta']}</a></p></div>
<div class="heroimg"><img src="{rel(path, 'assets/img/products/' + x['img'])}" width="{iw}" height="{ih}" alt="{E(pname(x, lang))}" fetchpriority="high"></div></div></div></section>
<section class="sec answer" id="answer-box" aria-label="{u['answer_label']}"><div class="wrap narrow"><p class="eyebrow dark">{u['answer_label']}</p><p class="lead">{E(c['answer'])}</p></div></section>
<section class="sec"><div class="wrap two"><div><h2>{u['who_h']}</h2><ul class="ticks">{who}</ul></div><div><h2>{u['problems_h']}</h2><ul class="ticks red">{prob}</ul></div></div></section>
<section class="sec tint"><div class="wrap"><h2 class="center">{u['features_h']}</h2><ul class="grid g3">{feats}</ul></div></section>
<section class="sec"><div class="wrap"><h2 class="center">{u['proof2_h']}</h2><ul class="specs">{specs}</ul><p class="note center">{u['source']}.</p></div></section>
{faq_html(c['faq'], u['faq_h'])}
{('<section class="sec tint"><div class="wrap"><h2 class="center">' + u['related_h'] + '</h2><ul class="grid g3">' + rp + '</ul></div></section>') if rp else ''}
<section class="sec"><div class="wrap"><h2 class="center">{u['all_apps']}</h2><ul class="chips">{others}</ul></div></section>
{contact_band(lang, watext)}
</main>"""
    write(path, head(lang, path, c["title"], c["desc"], alt, f"assets/og/{x['slug']}-{lang}.jpg", ld) + header(lang, path, alt) + body + footer(lang, path))
    og(os.path.join(SITE, f"assets/og/{x['slug']}-{lang}.jpg"), c["h1"], pname(x, lang), os.path.join(SITE, "assets/img/products/" + x["img"]))

def blog_hub(lang):
    u = UI[lang]; p = pre(lang)
    path = page_path("blog", lang); alt = page_path("blog", other(lang))
    items = [(u["breadcrumb_home"], p), (u["nav_blog"], path)]
    blog_ld = {"@context": "https://schema.org", "@type": "Blog", "name": u["blog_h1"], "url": url(path), "inLanguage": "zh-CN" if lang == "zh" else "en",
               "publisher": {"@id": f"{BASE}/#org"},
               "blogPost": [{"@type": "BlogPosting", "headline": q["en"]["title"], "url": url(page_path("post", "en", q["slug"])), "datePublished": q["date"], "inLanguage": "en"} for q in POSTS]}
    filt = f'<button class="f on" data-f="all">{u["filter_all"]}</button>' + "".join(f'<button class="f" data-f="{k}">{v[lang]}</button>' for k, v in PILLARS.items())
    cards = "".join(post_card(q, lang, path) for q in POSTS)
    js = "<script>document.querySelectorAll('.filters .f').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('.filters .f').forEach(x=>x.classList.toggle('on',x===b));const f=b.dataset.f;document.querySelectorAll('.pc').forEach(c=>c.hidden=!(f==='all'||c.dataset.p===f));}));</script>"
    body = f"""<main id="main"><section class="phero"><div class="wrap">{crumbs_html(items, path)}<h1 class="pageh">{u['blog_h1']}</h1><p class="sub2">{u['blog_desc']}</p>
<div class="filters" role="group" aria-label="Filter">{filt}</div><ul class="grid g3">{cards}</ul></div></section>{contact_band(lang)}</main>{js}"""
    write(path, head(lang, path, u["blog_title"], u["blog_desc"], alt, f"assets/og/blog-{lang}.jpg", [ORG, blog_ld, crumbs_ld(items)]) + header(lang, path, alt) + body + footer(lang, path))
    og(os.path.join(SITE, f"assets/og/blog-{lang}.jpg"), u["blog_h1"], u["nav_blog"])

def post(q):
    lang = "en"; u = UI[lang]; c = q["en"]
    path = page_path("post", lang, q["slug"])
    items = [(u["breadcrumb_home"], ""), ("Blog", "blog/"), (c["title"], path)]
    has_img = blog_imgs(q["slug"])
    imgurl = url(f"assets/img/blog/{q['slug']}.jpg") if has_img else url(f"assets/og/post-{q['slug']}.jpg")
    wc = wordcount(c["body_html"])
    prod = PBY[q["product"]]
    bp = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": c["title"], "description": c["description"], "inLanguage": "en",
          "url": url(path), "mainEntityOfPage": url(path), "datePublished": q["date"], "dateModified": TODAY, "image": [imgurl], "wordCount": wc,
          "author": {"@type": "Organization", "name": "MULAN editorial team", "url": f"{BASE}/about/"}, "publisher": {"@id": f"{BASE}/#org"},
          "about": [{"@type": "Thing", "name": PILLARS[q["pillar"]]["en"]}, {"@type": "Product", "name": prod["name"]}],
          "citation": [s["url"] for s in c["sources"]], "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["#answer-box"]}}
    faq = [(f["q"], f["a"]) for f in c["faq"]]
    ld = [ORG, bp, faq_ld(faq), crumbs_ld(items)]
    src = "".join(f'<li><a href="{E(s["url"])}" rel="noopener">{E(s["title"])}</a></li>' for s in c["sources"])
    rel_posts = [x for x in POSTS if x["slug"] != q["slug"] and x["pillar"] == q["pillar"]][:3]
    rp = "".join(post_card(x, lang, path) for x in rel_posts)
    hero = f'<figure class="phimg"><img src="{rel(path, "assets/img/blog/" + q["slug"] + ".jpg")}" width="1536" height="864" alt="{E(q.get("image_alt_en", ""))}" fetchpriority="high"></figure>' if has_img else ""
    mins = max(3, round(wc / 220))
    watext = u["wa_product"].format(name=prod["name"])
    body = f"""<main id="main"><article class="post">
<header class="wrap narrow ph">{crumbs_html(items, path)}<p class="eyebrow dark"><span class="tag t-{q['pillar']}">{PILLARS[q['pillar']]['en']}</span></p>
<h1>{E(c['title'])}</h1>
<p class="meta">{u['updated']} <time datetime="{TODAY}">{datetime.date.fromisoformat(TODAY).strftime('%d %b %Y')}</time> · {mins} {u['minread']} · MULAN editorial team</p></header>
<div class="wrap">{hero}</div>
<div class="wrap narrow prose">
<div class="answer-inline" id="answer-box"><p class="eyebrow dark">In short</p><p>{E(c['answer'])}</p></div>
{fix_links(c['body_html'], path)}
<aside class="cta-inline"><h2>{E(prod['name'])}</h2><p>{E(prod['en']['lead'])}</p><a class="btn btn-red" style="background:#fff;color:#12263D" href="{rel(path, 'products/' + prod['slug'] + '/')}">{u['read']} →</a> <a class="btn btn-ghost" style="color:#fff;border-color:#fff" href="{wa(watext)}" rel="noopener">WhatsApp {BRAND['whatsapp']}</a></aside>
</div></article>
{faq_html(faq, u['faq_h'], 'post-faq')}
<section class="sec"><div class="wrap narrow prose"><h2>{u['sources_h']}</h2><ol class="sources">{src}</ol></div></section>
{('<section class="sec tint"><div class="wrap"><h2 class="center">' + u['related_h'] + '</h2><ul class="grid g3">' + rp + '</ul></div></section>') if rp else ''}
</main>"""
    ogp = f"assets/og/post-{q['slug']}.jpg"
    write(path, head(lang, path, c["title"], c["description"], None, ogp, ld, ogtype="article") + header(lang, path, None) + body + footer(lang, path))
    og(os.path.join(SITE, ogp), c["title"], PILLARS[q["pillar"]]["en"])

def about(lang):
    u = UI[lang]; p = pre(lang)
    path = page_path("about", lang); alt = page_path("about", other(lang))
    items = [(u["breadcrumb_home"], p), (u["nav_about"], path)]
    ap = {"@context": "https://schema.org", "@type": "AboutPage", "name": u["about_title"], "url": url(path), "inLanguage": "zh-CN" if lang == "zh" else "en", "about": {"@id": f"{BASE}/#org"}}
    paras = "".join(f"<p>{E(i)}</p>" for i in ABOUT[lang])
    addr = BRAND["address_zh"] if lang == "zh" else BRAND["address_en"]; legal = BRAND["legal_name_zh"] if lang == "zh" else BRAND["legal_name"]
    body = f"""<main id="main"><section class="phero"><div class="wrap narrow">{crumbs_html(items, path)}<h1 class="pageh">{u['about_h1']}</h1></div></section>
<section class="sec"><div class="wrap narrow prose">{paras}
<h2>{u['address_h']}</h2><address>{E(legal)}<br>{E(addr)}</address>
<p>WhatsApp: <a href="{wa(u['wa_home'])}" rel="noopener">{BRAND['whatsapp']}</a></p></div></section>{contact_band(lang)}</main>"""
    write(path, head(lang, path, u["about_title"], u["about_desc"], alt, f"assets/og/about-{lang}.jpg", [ORG, ap, crumbs_ld(items)]) + header(lang, path, alt) + body + footer(lang, path))
    og(os.path.join(SITE, f"assets/og/about-{lang}.jpg"), u["about_h1"], "Foshan · 佛山", os.path.join(SITE, "assets/img/products/package.jpg"))

# ---------- machine-readable files ----------
def all_pages():
    pages = []
    for lang in LANGS:
        pages.append((page_path("home", lang), lang, "home", None))
        for x in PRODUCTS: pages.append((page_path("product", lang, x["slug"]), lang, "product", x["slug"]))
        pages.append((page_path("blog", lang), lang, "blog", None))
        pages.append((page_path("about", lang), lang, "about", None))
    for q in POSTS: pages.append((page_path("post", "en", q["slug"]), "en", "post", q["slug"]))
    return pages

def sitemap():
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for path, lang, kind, slug in all_pages():
        alts = ""
        if kind != "post":
            a = page_path(kind, other(lang), slug); en_p, zh_p = (path, a) if lang == "en" else (a, path)
            alts = (f'<xhtml:link rel="alternate" hreflang="en" href="{url(en_p)}"/><xhtml:link rel="alternate" hreflang="zh-CN" href="{url(zh_p)}"/>'
                    f'<xhtml:link rel="alternate" hreflang="x-default" href="{url(en_p)}"/>')
        img = ""
        if kind == "post" and os.path.exists(os.path.join(SITE, f"assets/img/blog/{slug}.jpg")): img = f"<image:image><image:loc>{url('assets/img/blog/' + slug + '.jpg')}</image:loc></image:image>"
        if kind == "product": img = f"<image:image><image:loc>{url('assets/img/products/' + PBY[slug]['img'])}</image:loc></image:image>"
        if kind == "home": img = f"<image:image><image:loc>{url('assets/img/products/seating-shower-scene.jpg')}</image:loc></image:image>"
        pr = {"home": "1.0", "product": "0.9", "blog": "0.7", "post": "0.7", "about": "0.5"}[kind]
        out.append(f'<url><loc>{url(path)}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority>{alts}{img}</url>')
    out.append("</urlset>")
    open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(out))

def feeds():
    d = "Wed, 04 Nov 2026 11:00:00 +0000"
    def rss(items, path, title, link, desc):
        it = "".join(f"<item><title>{E(t)}</title><link>{url(l)}</link><guid>{url(l)}</guid><pubDate>{d}</pubDate><description>{E(ds)}</description></item>" for t, l, ds in items)
        x = f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>{E(title)}</title><link>{url(link)}</link><description>{E(desc)}</description><language>en</language><lastBuildDate>{d}</lastBuildDate><atom:link href="{url(path)}" rel="self" type="application/rss+xml"/>{it}</channel></rss>'
        fp = os.path.join(SITE, path); os.makedirs(os.path.dirname(fp), exist_ok=True); open(fp, "w", encoding="utf-8").write(x)
    rss([(q["en"]["title"], page_path("post", "en", q["slug"]), q["en"]["description"]) for q in POSTS], "blog/feed.xml", "MULAN blog", "blog/", UI["en"]["blog_desc"])
    rss([(x["name"], page_path("product", "en", x["slug"]), x["en"]["desc"]) for x in PRODUCTS] + [(q["en"]["title"], page_path("post", "en", q["slug"]), q["en"]["description"]) for q in POSTS], "feed.xml", "MULAN 沐岚", "", UI["en"]["home_desc"])

def text_files():
    bots = ["Googlebot", "Googlebot-Image", "Bingbot", "DuckDuckBot", "Applebot", "Applebot-Extended", "GPTBot", "ChatGPT-User", "OAI-SearchBot",
            "ClaudeBot", "Claude-User", "Claude-SearchBot", "anthropic-ai", "PerplexityBot", "Perplexity-User", "Google-Extended", "GoogleOther",
            "Amazonbot", "Meta-ExternalAgent", "FacebookBot", "CCBot", "cohere-ai", "DuckAssistBot", "MistralAI-User", "YouBot", "Baiduspider", "Bytespider", "YandexBot"]
    r = "# MULAN 沐岚 — robots.txt\n# Search engines and AI answer engines are welcome to read and cite this site.\n\nUser-agent: *\nAllow: /\n\n" + \
        "".join(f"User-agent: {b}\nAllow: /\n" for b in bots) + f"\n# LLM-readable briefs: {BASE}/llms.txt and {BASE}/llms-full.txt\nSitemap: {BASE}/sitemap.xml\n"
    open(os.path.join(SITE, "robots.txt"), "w", encoding="utf-8").write(r)
    cite = f'MULAN 沐岚 ({BRAND["legal_name"]}, Foshan). "{BRAND["one_line_en"]}" {BASE}/'
    L = ["# MULAN 沐岚", "", f"> {BRAND['one_line_en']}", "", f"> {BRAND['one_line_zh']}", "",
         f"{BRAND['legal_name']} ({BRAND['legal_name_zh']}), {BRAND['address_en']}. {BRAND['markets_en']} B2B and OEM enquiries: WhatsApp {BRAND['whatsapp']}.", "",
         "## Products"] + [f"- [{x['name']}]({url(page_path('product','en',x['slug']))}): {x['en']['answer'].split('. ')[0]}." for x in PRODUCTS] + \
        ["", "## Key pages", f"- [Home]({url('')})", f"- [中文首页]({url('zh/')})", f"- [Blog]({url('blog/')})", f"- [About]({url('about/')})", f"- [Full brief]({url('llms-full.txt')})",
         "", "## Blog"] + [f"- [{q['en']['title']}]({url(page_path('post','en',q['slug']))}): {q['en']['description']}" for q in POSTS] + ["", "## Suggested citation", cite, ""]
    open(os.path.join(SITE, "llms.txt"), "w", encoding="utf-8").write("\n".join(L))
    Fl = ["# MULAN 沐岚 — full brief for language models", f"Last updated: {TODAY}", "", "## Definition", BRAND["one_line_en"], "", BRAND["one_line_zh"], "",
          UI["en"]["answer_more"], "", "## Company", f"- Legal name: {BRAND['legal_name']} ({BRAND['legal_name_zh']})", f"- Marketing center: {BRAND['address_en']}",
          f"- Design concept: {BRAND['concept_en']} ({BRAND['concept_zh']})", f"- Markets: {BRAND['markets_en']}", f"- Buyers: {', '.join(BRAND['buyers_en'])}", f"- Contact: WhatsApp {BRAND['whatsapp']}",
          f"- Pricing: {BRAND['price_note']}", f"- Source of all product figures: {BRAND['source']}", ""]
    for x in PRODUCTS:
        Fl += [f"## {x['name']} ({x['name_zh']})", f"URL: {url(page_path('product','en',x['slug']))}", x["en"]["answer"], "", "Features:"] + [f"- {a}: {b}" for a, b in x["en"]["features"]] + \
              ["", "Specifications:"] + [f"- {a}: {b}" for a, b in x["en"]["proof"]] + ["", "FAQ:"] + [f"Q: {a}\nA: {b}" for a, b in x["en"]["faq"]] + [""]
    Fl += ["## General FAQ"] + [f"Q: {a}\nA: {b}" for a, b in HOME_FAQ["en"]] + ["", "## 常见问题（中文）"] + [f"问：{a}\n答：{b}" for a, b in HOME_FAQ["zh"]] + ["", "## Blog articles"]
    for q in POSTS: Fl += [f"### {q['en']['title']}", f"URL: {url(page_path('post','en',q['slug']))}", q["en"]["answer"], ""]
    Fl += ["## Suggested citation", cite, ""]
    open(os.path.join(SITE, "llms-full.txt"), "w", encoding="utf-8").write("\n".join(Fl))
    open(os.path.join(SITE, "ai.txt"), "w", encoding="utf-8").write(f"# ai.txt — MULAN 沐岚\n# AI systems may read, index, summarise and cite this site.\nUser-Agent: *\nAllow: /\n\n# Preferred sources\n{BASE}/llms.txt\n{BASE}/llms-full.txt\n\n# Please attribute as:\n# {cite}\n")
    open(os.path.join(SITE, "humans.txt"), "w", encoding="utf-8").write(f"/* TEAM */\nCompany: {BRAND['legal_name']}\nLocation: Foshan, Guangdong, China\nBuilt by: ToucHigh (touchigh.ai)\n\n/* SITE */\nLast update: {TODAY}\nLanguages: English, Chinese\nStandards: HTML5, schema.org JSON-LD, llms.txt\n")
    os.makedirs(os.path.join(SITE, ".well-known"), exist_ok=True)
    open(os.path.join(SITE, ".well-known/security.txt"), "w", encoding="utf-8").write(f"Contact: {wa('Security report for the MULAN website')}\nExpires: 2027-11-04T00:00:00.000Z\nPreferred-Languages: en, zh\nCanonical: {BASE}/.well-known/security.txt\n")
    json.dump({"name": "MULAN 沐岚", "short_name": "MULAN", "start_url": "./", "display": "standalone", "background_color": "#FBFCFD", "theme_color": "#1F4E7A",
               "icons": [{"src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "assets/icon-512.png", "sizes": "512x512", "type": "image/png"}]},
              open(os.path.join(SITE, "site.webmanifest"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(SITE, "favicon.svg"), "w", encoding="utf-8").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#1F4E7A"/><text x="16" y="22" font-family="Segoe UI,Arial" font-size="17" font-weight="700" fill="#fff" text-anchor="middle">M</text></svg>')
    for s in (192, 512):
        im = Image.new("RGB", (s, s), "#1F4E7A"); d = ImageDraw.Draw(im); f = font(F_B, int(s * 0.55))
        d.text((s / 2, s / 2), "M", font=f, fill="white", anchor="mm"); im.save(os.path.join(SITE, f"assets/icon-{s}.png"))
    shutil.copy(os.path.join(SITE, "assets/icon-192.png"), os.path.join(SITE, "assets/favicon.png"))
    open(os.path.join(SITE, ".nojekyll"), "w").write("")
    open(os.path.join(SITE, "404.html"), "w", encoding="utf-8").write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found | MULAN</title><style>body{{font-family:Segoe UI,Arial,sans-serif;background:#EEF3F7;color:#12263D;display:grid;place-items:center;min-height:100vh;margin:0;text-align:center;padding:16px}}a{{color:#fff;background:#1F4E7A;padding:12px 22px;border-radius:999px;text-decoration:none}}</style></head><body><main><h1>Page not found</h1><p>The page you are looking for has moved.</p><p><a href="{BASE}/">Go to the home page</a></p></main></body></html>')

def clean_old():
    for f in ["index.html", "zh/index.html", "feed.xml"]:
        fp = os.path.join(SITE, f)
        if os.path.exists(fp): os.remove(fp)
    for d in ["products", "zh/products", "blog", "zh/blog", "about", "zh/about"]:
        shutil.rmtree(os.path.join(SITE, d), ignore_errors=True)

def main():
    clean_old()
    os.makedirs(os.path.join(SITE, "assets/og"), exist_ok=True)
    shutil.copy(os.path.join(ROOT, "build/site.css"), os.path.join(SITE, "assets/site.css"))
    text_files()
    for lang in LANGS:
        home(lang); blog_hub(lang); about(lang)
        for x in PRODUCTS: product(x, lang)
    for q in POSTS: post(q)
    sitemap(); feeds()
    print(f"built: {len(all_pages())} pages, {len(POSTS)} posts, base {BASE}")

if __name__ == "__main__":
    main()
