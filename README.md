# MULAN 沐岚 官网

沐岚（佛山市沐岚智家建材有限公司）适老化卫浴官网，由 ToucHigh 制作。纯静态 HTML，不需要构建工具，可直接用 GitHub Pages 发布。

- 英文首页：`docs/index.html`
- 中文首页：`docs/zh/index.html`
- 主 CTA：WhatsApp 询价 `+86 136 6003 9128`

## 目录

```
build.py                 生成器：所有文案、产品、FAQ、结构化数据都在这里改
img/                     产品图（来自《2025沐岚适老化卫浴图册》）
brand/                   OG 分享图、favicon、logo（scripts/make_brand_assets.js 生成）
docs/                    生成好的网站（GitHub Pages 发布这个文件夹）
  index.html  zh/index.html  404.html
  robots.txt  sitemap.xml  llms.txt  llms-full.txt  ai.txt  humans.txt
  feed.xml  site.webmanifest  .well-known/security.txt  .nojekyll
  assets/  (site.css, img/, og/, favicon.png, logo.png)
scripts/check_site.py    上线前检查（标题、描述、canonical、H1、FAQ 与结构化数据一致、链接、sitemap）
scripts/live_audit.py    上线后检查（按爬虫视角抓取线上站点）
AEO-GEO-README.md        SEO / AEO / GEO 维护说明
```

## 修改与重新生成

1. 改 `build.py` 里的文案或产品数据（中英文成对写）。
2. 设置正式域名后生成：

```bash
SITE_BASE=https://www.客户域名.com python3 build.py
python3 scripts/check_site.py docs --definition "MULAN (沐岚) is a Foshan manufacturer of aging-friendly bathroom products: seated showers, rise-assist toilet frames, grab bars and complete smart bathroom packages for distributors, OEM brands and elderly-care operators."
```

设置了 `SITE_BASE` 后会自动生成 `docs/CNAME`。未设置时所有网址是占位 `https://DOMAIN-TBD`，检查脚本只会报这一项。

本地预览：

```bash
SITE_BASE=http://localhost:8766 python3 build.py
cd docs && python3 -m http.server 8766
python3 scripts/live_audit.py http://localhost:8766   # 应输出 PASS
```

## 发布（GitHub Pages）

1. 用 `git push` 推送（不要用网页上传，网页上传会丢掉 `.nojekyll` 和 `.well-known/`）。
2. 仓库 Settings → Pages → Source 选 `main` 分支、`/docs` 文件夹。
3. 在域名服务商处把域名 CNAME 指向 `touchigh.github.io`，Pages 里填自定义域名并开启 HTTPS。
4. 上线后在 Google Search Console 和 Bing Webmaster Tools 提交 `sitemap.xml`，并运行 `python3 scripts/live_audit.py https://正式域名`。

## 待客户确认

- 正式域名、logo 原文件（目前 logo 为文字版占位）
- 是否公开零售价（目前不放价格，统一 B2B 报价）
- 自动洗澡机：图册图片带第三方品牌，确认自产还是代理（目前无图）
- OEM、起订量、交期、认证
- 图册错误：挂墙淋浴椅参数与坐式淋浴器重复；智能浴室柜英文标题误写；折叠凳承重“250克”应为 250 kg
- 是否需要日文版
