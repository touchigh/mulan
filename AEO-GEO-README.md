# SEO / AEO / GEO maintenance — MULAN 沐岚

## One-line definition (keep identical everywhere)

> MULAN (沐岚) is a Foshan manufacturer of aging-friendly bathroom products: seated showers, rise-assist toilet frames, grab bars and complete smart bathroom packages for distributors, OEM brands and elderly-care operators.

It lives in `build.py` as `DEF_EN` (Chinese: `DEF_ZH`) and is written from there into:
the `#answer-box` on the home page, the Organization `description` and WebPage `description` (JSON-LD), `og:description`, `llms.txt`, `llms-full.txt` and the suggested citation. Change it only in `build.py`, then rebuild.

## What each file does

| File | Purpose |
|---|---|
| `robots.txt` | Allows all search and AI crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended …) and points to the sitemap |
| `sitemap.xml` | Both language pages with hreflang alternates and product images |
| `llms.txt` | Short brief for AI assistants: definition, products, contact |
| `llms-full.txt` | Self-contained brief: differentiators, products, full FAQ (EN + 中文), suggested citation |
| `ai.txt` | AI usage and attribution string |
| JSON-LD | Organization, WebSite, WebPage (`speakable` → `#answer-box`), ItemList of Products, FAQPage |

## Rules

- Product facts come only from the MULAN catalogue or the client. No invented prices, ratings, certifications or awards.
- No `Offer` in JSON-LD unless a real public price is agreed with the client.
- Every FAQ question/answer in JSON-LD must also be visible on the page; `build.py` generates both from the same `FAQ` list.
- Each page has one H1, a unique title (≤60 characters) and description (≤155 characters).

## Checklist after each change

1. `SITE_BASE=https://<domain> python3 build.py`
2. `python3 scripts/check_site.py docs --definition "<one-line definition>"` → PASS
3. `git push`, wait for Pages, then `python3 scripts/live_audit.py https://<domain>` → PASS
4. After indexing, ask ChatGPT / Perplexity "What is MULAN aging-friendly bathroom?" and compare the answer with `llms-full.txt`.

## Next steps

- Product pages (`/products/<slug>/`) for the eight products, each with Product + FAQPage + BreadcrumbList.
- A blog with buyer questions (seated bathing, rise-assist toilets, care-home bathroom planning) linked to the product pages.
- Google Analytics / Tag Manager: install ToucHigh's IDs once provided.
