# MULAN 沐岚 website

Static site for Foshan Mulan Zhijia Building Materials Co., Ltd. (佛山市沐岚智家建材有限公司), aging-friendly bathroom products. Deployed with GitHub Pages at https://touchigh.github.io/mulan/ (branch `main`, root).

Built by ToucHigh with the `seo-aeo-geo-website` skill on top of the `somin-brand-deck` run in ToucHigh Pro workspace 5107 (API twin 5005), Nov 2025 – Oct 2026. Product facts come only from MULAN's 2025 aging-friendly bathroom product manual (适老化卫浴产品手册).

## Pages (34)

- `/` English home, `/zh/` 中文首页
- `/products/<slug>/` and `/zh/products/<slug>/`: 8 product pages each
- `/blog/` and `/zh/blog/` hubs; `/blog/<slug>/`: 12 English articles
- `/about/`, `/zh/about/`
- Primary CTA: WhatsApp (wa.me link with the enquiry message pre-filled per page), +86 136 6003 9128

## Rebuild

```
python -I build/build.py                       # writes the site into the repo root
python -I build/check_site.py . --definition "<one-line definition from data/brand.json>"
```

Set `SITE_BASE` to build for another host (e.g. `SITE_BASE=http://127.0.0.1:8767` for a local `build/live_audit.py` run). After deploying, run `python -I build/live_audit.py https://touchigh.github.io/mulan`.

| Path | Purpose |
|---|---|
| `build/build.py` | Generator (pages, JSON-LD, sitemap, feeds, llms/ai/robots, OG images) |
| `build/static_content.py` | Product, FAQ, about and UI copy in EN + 中文 |
| `data/brand.json` | Company facts and the one-line definition |
| `data/blog-plan.json` | Blog topics with the SOMIN whitespace theme, moment and trigger IDs behind each |
| `content/*.json` | Blog articles (body, FAQ, verified sources) |
| `assets/img/products/` | Real product photos from the 2025 manual |
| `assets/img/blog/` | Abstract AI backgrounds (no products, people, text or logo) |

## Maintenance (AEO/GEO)

- The one-line definition in `data/brand.json` must stay identical in the meta description, Organization description, `#answer-box`, `llms.txt` and the suggested citation. Edit it only there and rebuild.
- Every new product fact needs a source in MULAN's own material; never add prices, certificates, MOQs or lead times until the client confirms them.
- New articles: add an entry to `data/blog-plan.json` (with its SOMIN theme/moment) and a `content/NN-slug.json`, rebuild, run the QA gate.
- After indexing, ask ChatGPT / Perplexity "What is MULAN 沐岚?" and compare the answer with `llms-full.txt`.

## Open items (client / admin)

- Custom domain: on the project path `touchigh.github.io/mulan/`, crawlers look for `robots.txt`, `llms.txt` and `security.txt` at `touchigh.github.io/`, not here. Moving to MULAN's own domain fixes this: rebuild with `SITE_BASE=https://<domain>` and add a `CNAME` file. Then submit `sitemap.xml` in Google Search Console and Bing Webmaster Tools.
- Original logo file (the site uses a text wordmark placeholder).
- Public prices: the manual lists RMB prices, but the site quotes B2B on request until the client confirms.
- Automatic shower machine: catalogue photos show a third-party product name; confirm it is MULAN's own before adding it.
- Folding stool load: the manual says 250 kg in English, "250克" in Chinese and "500 pounds" on the image; the site uses 250 kg. Confirm.
- Named author with credentials for the blog (currently "MULAN editorial team").
