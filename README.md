# MULAN 沐岚 website

Static site for Foshan Mulan Zhijia Building Materials Co., Ltd. (佛山市沐岚智家建材有限公司), aging-friendly bathroom products. Deployed with GitHub Pages at https://touchigh.github.io/mulan/.

Built by ToucHigh with the seo-aeo-geo-website skill from MULAN's 2025 aging-friendly bathroom catalogue and the 10/29 client meeting (ToucHigh Pro workspace 5005 has no products or propositions yet, so positioning comes from the catalogue and the client's stated B2B targets).

## Pages

- `/` English home
- `/zh/` 中文首页
- Primary CTA: WhatsApp inquiry, +86 136 6003 9128

## Files

| Path | Purpose |
|---|---|
| `index.html`, `zh/index.html` | Home pages (one H1, canonical, hreflang en / zh-CN / x-default, JSON-LD: Organization, WebSite, WebPage + speakable, ItemList of Products, FAQPage) |
| `404.html` | Not-found page |
| `assets/` | `site.css`, product photos from the catalogue, OG image (1200×630), favicon, text logo placeholder |
| `robots.txt` | Allows search and AI crawlers, points to the sitemap |
| `sitemap.xml` | Both pages with hreflang alternates and image entries |
| `llms.txt`, `llms-full.txt`, `ai.txt` | Briefs and attribution for AI assistants |
| `feed.xml`, `humans.txt`, `site.webmanifest`, `.well-known/security.txt` | Discovery files |
| `.nojekyll` | Serve files as-is (no Jekyll) |

## Deployment

GitHub Pages from `main`, root folder. Push with git (the web uploader drops `.nojekyll` and `.well-known/`).

Known hosting limit: on the project path `touchigh.github.io/mulan/`, crawlers look for `robots.txt`, `llms.txt` and `security.txt` at `touchigh.github.io/`, not here. Moving to MULAN's own domain fixes this; rebuild with the domain as base URL and add a `CNAME` file.

## Open items (client to confirm)

- Domain and original logo file
- Whether retail prices are public (site quotes B2B prices only)
- Automatic shower machine: catalogue photo shows a third-party brand; confirm own product or distributed (no photo used)
- OEM, MOQ, lead times, certifications
