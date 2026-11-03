#!/usr/bin/env python3
"""MULAN homepage draft generator (EN + 中文).
Usage: SITE_BASE=https://your-domain python3 build.py
Writes: docs/ (the static site GitHub Pages serves) and out/artifact.html (Claude Artifact preview).
Facts come only from the 2025 MULAN aging-friendly bathroom catalogue and the 10/29 client meeting notes.
"""
import os, json, base64, html

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.environ.get("IMG_DIR", os.path.join(HERE, "img"))
BASE = os.environ.get("SITE_BASE", "https://DOMAIN-TBD").rstrip("/")
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

WA_NUM = "+86 136 6003 9128"
WA_URL = "https://wa.me/8613660039128"

DEF_EN = ("MULAN (沐岚) is a Foshan manufacturer of aging-friendly bathroom products: seated showers, "
          "rise-assist toilet frames, grab bars and complete smart bathroom packages for distributors, "
          "OEM brands and elderly-care operators.")
DEF_ZH = ("沐岚（MULAN）是佛山的适老化卫浴制造商，提供坐式淋浴器、电动起身助力架、安全扶手和适老化智能卫浴空间套餐，"
          "服务经销商、OEM 品牌和养老机构。")


MODE = {"embed": True, "prefix": "", "only": None}


def img(name):
    if not MODE["embed"]:
        return MODE["prefix"] + "assets/img/" + name
    with open(os.path.join(IMG, name), "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()


def t(en, zh, tag="span", cls="", attrs=""):
    c = f' class="{cls}"' if cls else ""
    if MODE["only"]:
        txt = en if MODE["only"] == "en" else zh
        return f'<{tag}{c}{attrs}>{txt}</{tag}>'
    return (f'<{tag}{c} lang="en" data-l="en"{attrs}>{en}</{tag}>'
            f'<{tag}{c} lang="zh-CN" data-l="zh"{attrs}>{zh}</{tag}>')


# ---------- content ----------
DIFFS = [
    {
        "k": ("One supplier, whole bathroom", "一家供应，整间卫浴"),
        "p": ("The aging-friendly smart bathroom package plans the whole room in one go: presence sensor, warm lighting, "
              "smart bath heater, anti-slip handrails, SOS call button, seated shower, smart toilet with lift assist, "
              "and a wheelchair-accessible cabinet.",
              "适老化智能卫浴空间套餐一次规划整间卫浴：人体存在感应器、适老化温馨照明、智能浴霸、安全防滑扶手、"
              "SOS 紧急呼叫按钮、坐式淋浴器、智能马桶 + 升降辅助器，以及轮椅可入的智能浴室柜。"),
        "spec": [("9", ("features in one plan", "项功能一套方案"))],
    },
    {
        "k": ("Bathing seated, without strain", "坐着洗，不费力"),
        "p": ("The multifunctional seating shower lets users wash seated or standing. Eight adjustable outlets on the "
              "shower arms wrap the body in water, with shoulder spray and back massage. The armrests fold away to save space.",
              "多功能坐式淋浴器支持坐浴和站浴。淋浴臂两侧共 8 个出水嘴可调角度，水雾包裹全身，并可肩部出水、后背按摩；"
              "扶手可折叠收纳，节省空间。"),
        "spec": [("8", ("water outlets", "个出水嘴")), ("≤9 L/min", ("water flow", "节水流量")),
                 ("110 kg", ("max load", "最大承重"))],
    },
    {
        "k": ("Standing up, with a lift", "起身，有人“扶”一把"),
        "p": ("The electric rise-assist stand raises the seat at one touch, quietly and to any height, and holds it "
              "wherever the user stops. It is built for people whose knees make sitting down and getting up hard.",
              "电动起身助力架一键升降座圈，静音、无级调节、随时悬停，专为膝关节不适、如厕起身和下蹲困难的老年人设计。"),
        "spec": [("130 + 45 mm", ("front lift", "前沿抬升")), ("0–13°", ("seat angle", "座板角度")),
                 ("135 kg", ("max load", "最大载荷")), ("20,000", ("cycles service life", "次使用寿命"))],
    },
    {
        "k": ("Safety in the small details", "安全藏在细节里"),
        "p": ("Grab bars use anti-slip particles and a 36 mm grip with a built-in aluminium alloy tube. Luminous rings "
              "glow at night after absorbing light. The wall-mounted folding stool carries up to 250 kg.",
              "扶手采用防滑颗粒和 36 mm 管径（树脂外管内置铝合金管），夜光圈吸光后夜间可见；挂墙折叠凳最大承重 250 kg。"),
        "spec": [("36 mm", ("grip diameter", "扶手管径")), ("250 kg", ("folding stool load", "折叠凳承重"))],
    },
]

PRODUCTS = [
    ("hero.jpg", ("Multifunctional seating shower", "多功能坐式淋浴器"),
     ("Seated or standing bath, 8 outlets, back massage, folding armrests.", "坐浴 / 站浴，8 出水嘴，后背按摩，扶手可折叠。")),
    ("split.jpg", ("Multifunctional split shower", "多功能分体式淋浴器"),
     ("Rotating upper and lower spray arms; with or without top spray.", "上下摆臂可旋转，可选带顶喷 / 不带顶喷。")),
    ("lift.jpg", ("Electric rise-assist stand", "电动起身助力架"),
     ("One-touch silent seat lift for the toilet. IPX4, 100–240 VAC.", "如厕一键静音升降座圈，IPX4，100–240 VAC。")),
    ("chair.jpg", ("Wall-mounted shower chair", "挂墙淋浴椅"),
     ("PU seat pad, anti-slip feet, folds up when not in use.", "PU 座垫、防滑 TPR 脚，不用时上折收纳。")),
    ("stool.jpg", ("Wall-mounted folding stool", "挂墙折叠凳"),
     ("Flips 180°, anti-slip surface, ABS and stainless steel, 250 kg.", "180° 翻转，防滑颗粒面，ABS + 不锈钢，承重 250 kg。")),
    ("grab.jpg", ("Grab bars and armrests", "安全扶手系列"),
     ("L-shaped, U-shaped flip-up, side flip-up and washbasin armrests.", "L 型、U 型上翻、侧边上翻、洗脸台扶手。")),
    ("cabinet.jpg", ("Smart bathroom cabinet", "智能浴室柜"),
     ("Wheelchair accessible; mirror tilts 0–15° for users of any height.", "轮椅可入；镜子角度 0–15° 可调，适合不同身高。")),
    (None, ("Automatic shower machine", "自动洗澡机"),
     ("For care homes: about 4 minutes and 80–100 L of water per bather.", "面向养老机构：每位约 4 分钟、用水约 80–100 公升。")),
]

PACKAGE = [
    ("Human presence sensor", "人体存在感应器"), ("Aging-friendly warm lighting", "适老化温馨照明"),
    ("Smart bath heater", "智能浴霸"), ("Anti-slip safety handrails", "安全防滑扶手"),
    ("SOS emergency call button", "SOS 紧急呼叫按钮"), ("Seated shower", "坐式淋浴器"),
    ("Smart toilet + lift assist", "智能马桶 + 升降辅助器"), ("Smart bathroom cabinet", "智能浴室柜"),
    ("Wheelchair-accessible cabinet base", "浴室柜轮椅可入"),
]

BUYERS = [
    (("Distributors and importers", "经销商与进口商"),
     ("A full aging-friendly bathroom range from one factory, from grab bars to complete packages.",
      "一家工厂覆盖完整适老化卫浴产品线，从扶手到整体空间套餐。")),
    (("OEM brands", "OEM 品牌"),
     ("Products from our catalogue, made for your brand. Ask us about your requirements.",
      "图册内产品可为您的品牌生产，欢迎沟通具体需求。")),
    (("Elderly-care operators", "养老机构"),
     ("Room-by-room bathroom plans and care-home equipment such as the automatic shower machine.",
      "按房间配置的卫浴方案，以及自动洗澡机等机构护理设备。")),
]

FAQ = [
    (("What does MULAN make?", "沐岚生产哪些产品？"),
     ("MULAN (Foshan Mulan Zhijia Building Materials Co., Ltd.) makes aging-friendly bathroom products: multifunctional "
      "seating and split showers, an electric rise-assist stand for the toilet, wall-mounted shower chairs and folding "
      "stools, grab bars and armrests, a wheelchair-accessible smart bathroom cabinet, an automatic shower machine for "
      "care homes, and a complete aging-friendly smart bathroom package.",
      "沐岚（佛山市沐岚智家建材有限公司）生产适老化卫浴产品：多功能坐式和分体式淋浴器、电动起身助力架、挂墙淋浴椅和折叠凳、"
      "安全扶手系列、轮椅可入的智能浴室柜、面向养老机构的自动洗澡机，以及适老化智能卫浴空间套餐。")),
    (("Who are MULAN products for?", "沐岚的产品适合谁？"),
     ("The products are for older adults and people with limited mobility who want to bathe and use the toilet safely "
      "and on their own. MULAN sells to businesses: distributors and importers, OEM brands, and elderly-care "
      "institutions that furnish homes, apartments or care facilities.",
      "产品面向希望安全、独立完成洗浴和如厕的老年人及行动不便人士。沐岚主要服务企业客户：经销商与进口商、OEM 品牌，"
      "以及为家庭、公寓或养老设施做配置的养老机构。")),
    (("Can an older person shower sitting down?", "老人可以坐着洗澡吗？"),
     ("Yes. The multifunctional seating shower is a standalone unit with a seat, so the user can wash seated or "
      "standing. Eight outlets on the two shower arms adjust in angle to wrap the body in water, and it offers "
      "shoulder spray and back massage. It uses no more than 9 litres per minute and carries up to 110 kg.",
      "可以。多功能坐式淋浴器自带座椅，可坐浴也可站浴。两侧淋浴臂共 8 个出水嘴，角度可调，水雾包裹全身，并有肩部出水和后背按摩。"
      "节水流量不超过 9 升/分钟，最大承重 110 公斤。")),
    (("How does the electric rise-assist stand help at the toilet?", "电动起身助力架如何帮助如厕？"),
     ("It fits over the toilet and lifts the seat at one touch, silently and to any height, stopping wherever the "
      "user releases the button. The front edge rises 130 + 45 mm and the seat tilts 0–13°, helping people with "
      "knee problems sit down and stand up. It carries 135 kg, is rated IPX4 and lasts 20,000 cycles.",
      "助力架安装在马桶上，一键静音升降座圈，无级调节、随时悬停。前沿抬升 130 + 45 mm，座板角度 0–13°，帮助膝关节不适的老人坐下和起身。"
      "最大载荷 135 kg，防护等级 IPX4，使用寿命 20,000 次。")),
    (("What is in the aging-friendly smart bathroom package?", "适老化智能卫浴空间套餐包含什么？"),
     ("The package plans a whole bathroom around the idea of future elderly care and smart living. It combines a "
      "human presence sensor, warm aging-friendly lighting, a smart bath heater, anti-slip handrails, an SOS "
      "emergency call button, a seated shower, a smart toilet with lift assist, and a smart cabinet that a "
      "wheelchair can roll under.",
      "套餐以“未来养老，智慧生活”为核心理念规划整间卫浴，包括人体存在感应器、适老化温馨照明、智能浴霸、安全防滑扶手、"
      "SOS 紧急呼叫按钮、坐式淋浴器、智能马桶 + 升降辅助器，以及轮椅可入的智能浴室柜。")),
    (("Are the grab bars easy to find at night?", "夜间能看清扶手吗？"),
     ("The luminous versions of MULAN grab bars have glowing rings that light up in the dark after absorbing light, "
      "so the bar is easier to find at night. The bars also use raised anti-slip particles, and the L-shaped bar has "
      "a 36 mm resin grip with a built-in aluminium alloy tube.",
      "沐岚夜光款扶手带夜光圈，吸收光源后可在黑暗中发光，夜间更容易找到扶手。扶手表面有凸起防滑颗粒，"
      "L 型扶手为 36 mm 树脂外管内置铝合金管。")),
    (("How does the automatic shower machine help care homes?", "自动洗澡机对养老机构有什么帮助？"),
     ("A caregiver bathes a resident lying down. A standard wash takes about 4 minutes and about 80–100 litres of "
      "water, compared with about 400–600 litres for other bathing equipment. Body and disinfection nozzles run on "
      "separate pipes, and water supply stops automatically if the temperature is abnormal.",
      "护理人员可为卧姿老人洗浴。标准流程每人约 4 分钟，用水约 80–100 公升，其他淋浴设备约 400–600 公升。"
      "人体喷管与机器消毒喷管独立分开；水温异常时机器自动停止供水。")),
    (("Which markets does MULAN supply, and how do I get a quote?", "沐岚供应哪些市场？如何获取报价？"),
     ("MULAN already ships to the Middle East and West Asia and is now expanding to Japan. For B2B pricing, product "
      "details or OEM requests, message the MULAN team on WhatsApp at +86 136 6003 9128 with the products and "
      "quantities you need.",
      "沐岚已出口中东和西亚，目前重点拓展日本市场。如需 B2B 报价、产品资料或 OEM 合作，请通过 WhatsApp +86 136 6003 9128 "
      "联系沐岚团队，并说明所需产品和数量。")),
]


def faq_html():
    out = []
    for (qe, qz), (ae, az) in FAQ:
        out.append(f'<details class="qa"><summary>{t(qe, qz)}</summary>{t(ae, az, "p")}</details>')
    return "\n".join(out)


def jsonld(L=0, page_url=None):
    page_url = page_url or BASE + "/"
    org = {"@context": "https://schema.org", "@type": "Organization", "@id": BASE + "/#org",
           "name": "MULAN 沐岚", "legalName": "Foshan Mulan Zhijia Building Materials Co., Ltd.",
           "alternateName": ["沐岚", "佛山市沐岚智家建材有限公司", "Mulan Zhijia"],
           "url": BASE + "/", "logo": BASE + "/assets/logo.png", "description": DEF_EN,
           "address": {"@type": "PostalAddress", "streetAddress": "2F06a, Tao Li Fang, Ceramic Headquarters Base",
                       "addressLocality": "Chancheng District, Foshan", "addressRegion": "Guangdong",
                       "addressCountry": "CN"},
           "contactPoint": {"@type": "ContactPoint", "telephone": "+86-136-6003-9128", "contactType": "sales",
                            "availableLanguage": ["zh", "en"]}}
    site = {"@context": "https://schema.org", "@type": "WebSite", "name": "MULAN 沐岚", "url": BASE + "/",
            "inLanguage": ["en", "zh-CN"], "publisher": {"@id": BASE + "/#org"}}
    page = {"@context": "https://schema.org", "@type": "WebPage", "name": "MULAN aging-friendly bathroom products",
            "url": page_url, "inLanguage": ["en", "zh-CN"][L], "description": [DEF_EN, DEF_ZH][L], "about": {"@id": BASE + "/#org"},
            "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["#answer-box"]}}
    prods = {"@context": "https://schema.org", "@type": "ItemList", "name": "MULAN products",
             "itemListElement": [{"@type": "ListItem", "position": i + 1,
                                  "item": {"@type": "Product", "name": n[0], "description": d[0],
                                           "brand": {"@type": "Brand", "name": "MULAN"}}}
                                 for i, (_, n, d) in enumerate(PRODUCTS)]}
    faq = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q[L],
                           "acceptedAnswer": {"@type": "Answer", "text": a[L]}} for q, a in FAQ]}
    return "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>'
                     for x in (org, site, page, prods, faq))


CSS = r"""
/* Layout: one calm column of white and tile-blue bands; specs set like a catalogue parameter table */
:root{
  --bg:#FBFCFD; --surface:#EEF3F7; --ink:#12263D; --muted:#4D6074; --line:#D3DEE8;
  --blue:#1F4E7A; --water:#5F88B0; --on-blue:#FFFFFF; --glow:#2FA36B;
  --f-display:"Jost","Noto Sans SC",system-ui,sans-serif;
  --f-body:"IBM Plex Sans","Noto Sans SC",system-ui,sans-serif;
  --f-mono:"IBM Plex Mono",ui-monospace,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#0E1A27; --surface:#15263A; --ink:#E6EEF6; --muted:#A3B5C7; --line:#28405A;
  --blue:#7FB0DC; --water:#8FB4D8; --on-blue:#0E1A27; --glow:#5CCB93; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0E1A27; --surface:#15263A; --ink:#E6EEF6; --muted:#A3B5C7; --line:#28405A;
  --blue:#7FB0DC; --water:#8FB4D8; --on-blue:#0E1A27; --glow:#5CCB93; color-scheme:dark}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--f-body);font-size:16px;line-height:1.6}
#site[data-lang="en"] [data-l="zh"]{display:none!important}
#site[data-lang="zh"] [data-l="en"]{display:none!important}
.wrap{max-width:1120px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
a{color:var(--blue)}
:focus-visible{outline:2px solid var(--water);outline-offset:3px}
.skip{position:absolute;left:-999px}.skip:focus{left:16px;top:16px;background:var(--bg);padding:8px;z-index:20}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--bg)}
header.top{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.bar{display:flex;align-items:center;gap:24px;padding-block:14px}
.mark{font-family:var(--f-display);font-weight:300;letter-spacing:.18em;font-size:20px;color:var(--ink);text-decoration:none;white-space:nowrap}
.mark b{font-weight:400;letter-spacing:.05em;margin-right:.5em}
nav.menu{display:flex;gap:20px;margin-left:auto;font-size:14px}
nav.menu a{color:var(--muted);text-decoration:none}nav.menu a:hover{color:var(--ink)}
.lang{display:inline-flex;border:1px solid var(--line);border-radius:999px;overflow:hidden;font-size:13px}
.lang button{all:unset;cursor:pointer;padding:4px 10px;color:var(--muted)}
.lang button[aria-pressed="true"]{background:var(--blue);color:var(--on-blue)}
.btn{display:inline-flex;align-items:center;gap:8px;font-weight:600;text-decoration:none;border-radius:6px;padding:12px 20px;font-size:15px}
.btn.primary{background:var(--blue);color:var(--on-blue)}
.btn.ghost{border:1px solid var(--line);color:var(--ink)}
.btn.sm{padding:8px 14px;font-size:14px}
.btn svg{width:18px;height:18px;fill:currentColor}
@media (max-width:760px){nav.menu{display:none}.bar{gap:12px}.bar .btn.sm{margin-left:auto}}

.hero{padding-block:56px 40px}
.hero-grid{display:grid;grid-template-columns:1.05fr .95fr;gap:48px;align-items:center}
.eyebrow{font-family:var(--f-mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--water)}
h1,h2,h3{font-family:var(--f-display);text-wrap:balance;margin:0}
h1{font-weight:400;font-size:clamp(34px,5vw,56px);line-height:1.08;letter-spacing:-.01em;margin-block:14px 18px}
h1 em{font-style:normal;font-weight:300;color:var(--blue)}
.lede{font-size:18px;color:var(--muted);max-width:34em;margin:0 0 28px}
.cta-row{display:flex;flex-wrap:wrap;gap:12px}
.hero figure{margin:0;border-radius:4px;overflow:hidden;background:var(--surface)}
.hero figure img{display:block;width:100%;height:auto}
.hero figcaption{font-size:12px;color:var(--muted);padding:8px 12px}
@media (max-width:860px){.hero-grid{grid-template-columns:1fr;gap:28px}.hero{padding-block:32px}}

#answer-box{border-block:1px solid var(--line);padding-block:22px;display:grid;grid-template-columns:160px 1fr;gap:24px}
#answer-box .eyebrow{padding-top:4px}
#answer-box p{margin:0;font-size:17px;max-width:62em}
#answer-box p+p{margin-top:8px;color:var(--muted);font-size:15px}
@media (max-width:640px){#answer-box{grid-template-columns:1fr;gap:8px}}

section{padding-block:72px}
.sec-head{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:end;gap:16px;margin-bottom:36px}
h2{font-weight:400;font-size:clamp(26px,3.4vw,38px);line-height:1.15}
.sec-head p{margin:0;color:var(--muted);max-width:30em}

.diffs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1px;background:var(--line);border:1px solid var(--line)}
.diff{background:var(--bg);padding:28px;display:flex;flex-direction:column;gap:14px;min-width:0}
.diff h3{font-size:22px;font-weight:500}
.diff p{margin:0;color:var(--muted)}
.specs{display:flex;flex-wrap:wrap;gap:8px 20px;margin-top:auto;padding-top:14px;border-top:1px dashed var(--line)}
.spec{display:flex;flex-direction:column}
.spec .v{font-family:var(--f-mono);font-size:18px;color:var(--blue);font-variant-numeric:tabular-nums;white-space:nowrap}
.spec .u{font-size:12px;color:var(--muted)}
@media (max-width:720px){.diffs{grid-template-columns:1fr}}

.band{background:var(--surface)}
.pkg{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center}
.pkg figure{margin:0;background:#FFFFFF;border-radius:4px;padding:12px}
.pkg figure img{display:block;width:100%;height:auto}
.pkg ul{list-style:none;padding:0;margin:20px 0 0;display:grid;grid-template-columns:1fr 1fr;gap:10px 20px}
.pkg li{padding-left:18px;position:relative;font-size:15px}
.pkg li::before{content:"";position:absolute;left:0;top:.6em;width:8px;height:8px;border-radius:50%;border:1.5px solid var(--blue)}
.pkg .quote{font-family:var(--f-display);font-size:20px;font-weight:300;color:var(--blue);margin:0 0 6px}
@media (max-width:860px){.pkg{grid-template-columns:1fr;gap:28px}}
@media (max-width:420px){.pkg ul{grid-template-columns:1fr}}

.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px}
.card{display:flex;flex-direction:column;gap:8px;min-width:0}
.card .ph{aspect-ratio:4/5;max-width:100%;background:var(--surface);border-radius:4px;overflow:hidden;display:grid;place-items:center}
.card .ph img{width:100%;height:100%;object-fit:cover;display:block}
.card .ph .noimg{font-family:var(--f-mono);font-size:12px;color:var(--muted);text-align:center;padding:16px;line-height:1.5}
.card h3{font-size:17px;font-weight:500;line-height:1.3}
.card p{margin:0;font-size:14px;color:var(--muted)}
.note{font-size:13px;color:var(--muted);margin-top:24px}
@media (max-width:960px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}

.buyers{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:32px}
.buyer h3{font-size:20px;font-weight:500;padding-top:14px;border-top:2px solid var(--blue);margin-bottom:8px}
.buyer p{margin:0;color:var(--muted)}
.markets{margin-top:36px;display:flex;flex-wrap:wrap;gap:10px;align-items:center;font-size:14px}
.chip{border:1px solid var(--line);border-radius:999px;padding:4px 12px;background:var(--bg)}
.chip.new{border-color:var(--glow);color:var(--glow)}
@media (max-width:760px){.buyers{grid-template-columns:1fr;gap:24px}}

.faq{max-width:820px}
.qa{border-bottom:1px solid var(--line)}
.qa summary{cursor:pointer;list-style:none;padding:18px 32px 18px 0;font-weight:500;font-size:17px;position:relative}
.qa summary::-webkit-details-marker{display:none}
.qa summary::after{content:"+";position:absolute;right:4px;top:14px;font-family:var(--f-mono);font-size:20px;color:var(--water)}
.qa[open] summary::after{content:"−"}
.qa p{margin:0 0 20px;color:var(--muted);max-width:65ch}

.contact{background:var(--blue);color:var(--on-blue)}
.contact h2{color:var(--on-blue)}
.contact-grid{display:grid;grid-template-columns:1.2fr 1fr;gap:40px;align-items:start}
.contact p{opacity:.88;margin:12px 0 24px;max-width:32em}
.contact .btn.primary{background:var(--on-blue);color:var(--blue)}
.num{font-family:var(--f-mono);font-size:22px;letter-spacing:.02em;user-select:all}
.copy{all:unset;cursor:pointer;font-size:13px;border:1px solid currentColor;border-radius:4px;padding:3px 10px;margin-left:10px;opacity:.85}
dl.info{margin:0;display:grid;gap:14px}
dl.info dt{font-family:var(--f-mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;opacity:.7}
dl.info dd{margin:2px 0 0}
@media (max-width:760px){.contact-grid{grid-template-columns:1fr}}

footer{padding-block:28px;font-size:13px;color:var(--muted)}
footer .wrap{display:flex;flex-wrap:wrap;gap:8px 24px;justify-content:space-between}
@media (prefers-reduced-motion:no-preference){.btn,.card .ph img{transition:transform .2s}.card:hover .ph img{transform:scale(1.03)}}
"""

WA_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2'
          'c-1.5 0-3-.4-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1'
          'l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.3-.4.8-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5'
          'a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.1 5.1 0 0 0 1.1 2.7 11.7 11.7 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6'
          ' 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>')


def body(lang="en"):
    L = 0 if lang == "en" else 1
    diffs = []
    for d in DIFFS:
        specs = "".join(f'<div class="spec"><span class="v">{v}</span>{t(u[0], u[1], "span", "u")}</div>'
                        for v, u in d["spec"])
        diffs.append(f'<article class="diff"><h3>{t(*d["k"])}</h3>{t(*d["p"], "p")}<div class="specs">{specs}</div></article>')
    cards = []
    for f, n, dsc in PRODUCTS:
        ph = (f'<img src="{img(f)}" alt="{html.escape(n[0])}" loading="lazy" width="600" height="750">' if f else
              t("Photo to come<br>(client to supply)", "图片待补充<br>（客户提供）", "span", "noimg"))
        cards.append(f'<article class="card"><div class="ph">{ph}</div><h3>{t(*n)}</h3>{t(*dsc, "p")}</article>')
    pkg = "".join(f"<li>{t(*p)}</li>" for p in PACKAGE)
    buyers = "".join(f'<div class="buyer"><h3>{t(*b[0])}</h3>{t(*b[1], "p")}</div>' for b in BUYERS)

    return f"""
<div id="site" data-lang="{lang}">
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap bar">
  <a class="mark" href="#top" aria-label="MULAN home"><b>沐岚</b>MU LAN</a>
  <nav class="menu" aria-label="Main">
    <a href="#why">{t("Why MULAN","为什么选沐岚")}</a><a href="#products">{t("Products","产品")}</a>
    <a href="#partners">{t("Partners","合作")}</a><a href="#faq">FAQ</a>
  </nav>
  <div class="lang" role="group" aria-label="Language"><button id="l-en" aria-pressed="true">EN</button><button id="l-zh" aria-pressed="false">中文</button></div>
  <a class="btn primary sm" href="{WA_URL}" target="_blank" rel="noopener">{WA_SVG}{t("Get a quote","询价")}</a>
</div></header>

<main id="main">
<div class="wrap hero" id="top"><div class="hero-grid">
  <div>
    {t("Aging-friendly bathroom manufacturer · Foshan, China","适老化卫浴制造商 · 中国佛山","div","eyebrow")}
    {t("Bathrooms that let older people <em>stay independent</em>","让老人在卫浴间<em>不求人</em>","h1")}
    {t("Seated showers, rise-assist toilet frames, grab bars and complete smart bathroom packages, supplied factory-direct to distributors, OEM brands and elderly-care operators.",
       "坐式淋浴器、电动起身助力架、安全扶手和整体适老化智能卫浴套餐，工厂直供经销商、OEM 品牌和养老机构。","p","lede")}
    <div class="cta-row">
      <a class="btn primary" href="{WA_URL}" target="_blank" rel="noopener">{WA_SVG}{t("Ask for B2B pricing on WhatsApp","WhatsApp 获取 B2B 报价")}</a>
      <a class="btn ghost" href="#products">{t("See the products","查看产品")}</a>
    </div>
  </div>
  <figure><img src="{img('hero.jpg')}" alt="MULAN multifunctional seating shower beside a toilet with flip-up armrests" width="1100" height="853">
    {t("Multifunctional seating shower: bathe seated or standing.","多功能坐式淋浴器：可坐浴，也可站浴。","figcaption")}</figure>
</div></div>

<div class="wrap"><div id="answer-box">
  {t("In one line","一句话了解沐岚","div","eyebrow")}
  <div>{t(DEF_EN, DEF_ZH, "p")}
  {t("The range is designed around one idea, “Future elderly care, smart living”: technology that makes home bathing safer and more comfortable. MULAN already ships to the Middle East and West Asia and is now focused on Japan.",
     "产品围绕“未来养老，智慧生活”的理念设计，用智能技术让居家洗浴更安全、更舒适。沐岚已出口中东和西亚，目前重点拓展日本市场。","p")}</div>
</div></div>

<section id="why"><div class="wrap">
  <div class="sec-head">{t("What sets MULAN apart","沐岚的四个不同","h2")}
    {t("Every figure below comes from the MULAN product catalogue.","以下数据均来自沐岚产品手册。","p")}</div>
  <div class="diffs">{''.join(diffs)}</div>
</div></section>

<section class="band" id="package"><div class="wrap pkg">
  <figure><img src="{img('space.jpg')}" alt="Diagram of the MULAN aging-friendly smart bathroom package with all components labelled" loading="lazy" width="900" height="803"></figure>
  <div>
    {t("Aging-friendly smart bathroom package","适老化智能卫浴空间套餐","div","eyebrow")}
    {t("“Future elderly care, smart living.”","“未来养老，智慧生活。”","p","quote")}
    {t("Plan the whole room, not one product","规划整间卫浴，而不只是一件产品","h2")}
    <ul>{pkg}</ul>
  </div>
</div></section>

<section id="products"><div class="wrap">
  <div class="sec-head">{t("Products","产品系列","h2")}
    {t("From a single grab bar to equipment for care homes.","从一根扶手到养老机构设备。","p")}</div>
  <div class="grid">{''.join(cards)}</div>
  {t("Prices, MOQ and lead times are quoted per order. Message us on WhatsApp for the full catalogue.",
     "价格、起订量和交期按订单报价，WhatsApp 联系我们获取完整图册。","p","note")}
</div></section>

<section class="band" id="partners"><div class="wrap">
  <div class="sec-head">{t("Who we work with","我们服务的客户","h2")}</div>
  <div class="buyers">{buyers}</div>
  <div class="markets">{t("Markets:","市场：")}<span class="chip">{t("Middle East","中东")}</span><span class="chip">{t("West Asia","西亚")}</span><span class="chip new">{t("Japan · new focus","日本 · 重点拓展")}</span></div>
</div></section>

<section id="faq"><div class="wrap faq">
  <div class="sec-head">{t("Questions buyers ask","采购常见问题","h2")}</div>
  {faq_html()}
</div></section>

<section class="contact" id="contact"><div class="wrap contact-grid">
  <div>
    {t("Tell us what you need to source","告诉我们您的采购需求","h2")}
    {t("Send the products and quantities you are looking for. The MULAN team replies with B2B pricing and the full catalogue.",
       "发送所需产品和数量，沐岚团队将回复 B2B 报价和完整产品图册。","p")}
    <a class="btn primary" href="{WA_URL}" target="_blank" rel="noopener">{WA_SVG}{t("Message us on WhatsApp","WhatsApp 联系我们")}</a>
  </div>
  <dl class="info">
    <div><dt>WhatsApp</dt><dd><span class="num" id="wa">{WA_NUM}</span><button class="copy" id="copy" type="button">{t("Copy","复制")}</button></dd></div>
    <div><dt>{t("Company","公司")}</dt><dd>{t("Foshan Mulan Zhijia Building Materials Co., Ltd.","佛山市沐岚智家建材有限公司")}</dd></div>
    <div><dt>{t("Marketing center","营销中心")}</dt><dd>{t("2F06a, Tao Li Fang, Ceramic Headquarters Base, Chancheng District, Foshan, Guangdong, China","广东省佛山市禅城区陶瓷总部基地陶立方 2F06a")}</dd></div>
    <div><dt>Xiaohongshu</dt><dd>沐岚适老化 · mulanzi827</dd></div>
  </dl>
</div></section>
</main>

<footer><div class="wrap"><span>© 2026 {t("Foshan Mulan Zhijia Building Materials Co., Ltd.","佛山市沐岚智家建材有限公司")}</span>
<span>{t("Aging-friendly bathroom products","适老化卫浴产品")}</span></div></footer>
</div>
<script>
(function(){{
  var site=document.getElementById('site');
  function set(l){{site.dataset.lang=l;document.getElementById('l-en').setAttribute('aria-pressed',l==='en');
    document.getElementById('l-zh').setAttribute('aria-pressed',l==='zh');try{{localStorage.setItem('mulan-lang',l)}}catch(e){{}}}}
  var EN=site.dataset.home==='1'?null:'{"./" if lang=="en" else "../"}', ZH='{"zh/" if lang=="en" else "./"}';
  document.getElementById('l-en').onclick=function(){{if(site.dataset.multi)location.href=EN;else set('en')}};
  document.getElementById('l-zh').onclick=function(){{if(site.dataset.multi)location.href=ZH;else set('zh')}};
  set(site.dataset.lang);
  document.getElementById('copy').onclick=function(){{var n=document.getElementById('wa');
    var b=this;var done=function(){{b.dataset.done=1;b.style.opacity=1}};
    if(navigator.clipboard)navigator.clipboard.writeText(n.textContent).then(done,function(){{sel(n)}});else sel(n)}};
  function sel(n){{var r=document.createRange();r.selectNodeContents(n);var s=getSelection();s.removeAllRanges();s.addRange(r)}}
}})();
</script>
{jsonld(L, BASE + ("/" if L == 0 else "/zh/"))}
"""


FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500'
         '&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400&family=Noto+Sans+SC:wght@300;400;500&display=swap">')

TITLE = "MULAN Aging-Friendly Bathrooms"

# 1) Artifact preview: one page, images embedded, in-page language toggle
MODE.update(embed=True, prefix="", only=None)
with open(os.path.join(OUT, "artifact.html"), "w", encoding="utf-8") as f:
    f.write(f'<title>{TITLE}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n{FONTS}\n<style>{CSS}</style>\n{body("en")}')

# 2) Static site: /index.html (EN) and /zh/index.html (中文); toggle links between the two URLs
SITE = os.path.join(HERE, "docs")
META = {
    "en": dict(path="/", prefix="", html_lang="en",
               title="MULAN | Aging-Friendly Bathroom Products, Foshan",
               desc="Seated showers, rise-assist toilet frames, grab bars and smart bathroom packages from Foshan, for distributors, OEM brands and care homes.",
               og="MULAN aging-friendly bathroom products", defn=DEF_EN),
    "zh": dict(path="/zh/", prefix="../", html_lang="zh-CN",
               title="沐岚 MULAN｜适老化卫浴产品 · 佛山工厂直供",
               desc="坐式淋浴器、电动起身助力架、安全扶手和适老化智能卫浴空间套餐，佛山工厂直供经销商、OEM 品牌和养老机构。",
               og="沐岚适老化卫浴产品", defn=DEF_ZH),
}
for lang, m in META.items():
    MODE.update(embed=False, prefix=m["prefix"], only=lang)
    b = body(lang).replace('<div id="site" ', '<div id="site" data-multi="1" ', 1)
    url = BASE + m["path"]
    head = f"""<!doctype html><html lang="{m['html_lang']}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{m['title']}</title>
<meta name="description" content="{m['desc']}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{BASE}/"><link rel="alternate" hreflang="zh-CN" href="{BASE}/zh/"><link rel="alternate" hreflang="x-default" href="{BASE}/">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta property="og:type" content="website"><meta property="og:site_name" content="MULAN 沐岚">
<meta property="og:title" content="{m['og']}"><meta property="og:description" content="{m['defn']}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/assets/og/home.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{m['prefix']}assets/favicon.png" type="image/png"><link rel="manifest" href="{m['prefix']}site.webmanifest">
<link rel="preload" as="image" href="{m['prefix']}assets/img/hero.jpg">
{FONTS}<link rel="stylesheet" href="{m['prefix']}assets/site.css"></head><body>"""
    d = os.path.join(SITE, m["path"].strip("/"))
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(head + b + "</body></html>")

os.makedirs(os.path.join(SITE, "assets"), exist_ok=True)
with open(os.path.join(SITE, "assets", "site.css"), "w", encoding="utf-8") as f:
    f.write(CSS)

TODAY = os.environ.get("BUILD_DATE", "2026-11-03")
def w(name, text):
    p = os.path.join(SITE, name); os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f: f.write(text)

BOTS = ["Googlebot", "Bingbot", "GPTBot", "ChatGPT-User", "OAI-SearchBot", "ClaudeBot", "Claude-SearchBot",
        "Claude-User", "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot", "Applebot-Extended",
        "Amazonbot", "Meta-ExternalAgent", "CCBot", "DuckAssistBot", "MistralAI-User", "Bytespider", "YandexBot"]
w("robots.txt", "User-agent: *\nAllow: /\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in BOTS)
  + f"Sitemap: {BASE}/sitemap.xml\n")

IMGS = ["hero.jpg", "space.jpg", "split.jpg", "lift.jpg", "chair.jpg", "stool.jpg", "grab.jpg", "cabinet.jpg"]
def sm_url(path):
    alts = (f'<xhtml:link rel="alternate" hreflang="en" href="{BASE}/"/>'
            f'<xhtml:link rel="alternate" hreflang="zh-CN" href="{BASE}/zh/"/>'
            f'<xhtml:link rel="alternate" hreflang="x-default" href="{BASE}/"/>')
    ims = "".join(f"<image:image><image:loc>{BASE}/assets/img/{i}</image:loc></image:image>" for i in IMGS)
    return f"<url><loc>{BASE}{path}</loc><lastmod>{TODAY}</lastmod>{alts}{ims}</url>"
w("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
  'xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
  + sm_url("/") + "\n" + sm_url("/zh/") + "\n</urlset>\n")

CITE = f"MULAN (沐岚), Foshan Mulan Zhijia Building Materials Co., Ltd. — {BASE}/"
prod_lines = "\n".join(f"- {n[0]} ({n[1]}): {d[0]}" for _, n, d in PRODUCTS)
w("llms.txt", f"# MULAN 沐岚\n\n> {DEF_EN}\n\n{DEF_ZH}\n\n## Key pages\n- [Home (English)]({BASE}/)\n- [首页（中文）]({BASE}/zh/)\n"
  f"- [Full brief for AI assistants]({BASE}/llms-full.txt)\n\n## Products\n{prod_lines}\n\n## Contact\n"
  f"- WhatsApp: {WA_NUM} ({WA_URL})\n")
faq_txt = "\n\n".join(f"### {q[0]}\n{a[0]}\n\n### {q[1]}\n{a[1]}" for q, a in FAQ)
diff_txt = "\n".join(f"- {d['k'][0]}: {d['p'][0]}" for d in DIFFS)
w("llms-full.txt", f"# MULAN 沐岚 — full brief\n\n{DEF_EN}\n\n{DEF_ZH}\n\nLegal name: Foshan Mulan Zhijia Building Materials Co., Ltd. (佛山市沐岚智家建材有限公司)\n"
  "Marketing center: 2F06a, Tao Li Fang, Ceramic Headquarters Base, Chancheng District, Foshan, Guangdong, China\n"
  "Design concept: \"Future elderly care, smart living\" (未来养老，智慧生活)\n"
  "Markets: ships to the Middle East and West Asia; Japan is the new focus.\n"
  "Buyers: distributors and importers, OEM brands, elderly-care operators.\n\n"
  f"## What sets MULAN apart\n{diff_txt}\n\n## Products\n{prod_lines}\n\n## FAQ\n\n{faq_txt}\n\n"
  f"## Source\nAll product figures come from the MULAN 2025 aging-friendly bathroom product manual.\n\n"
  f"## Suggested citation\n{CITE}\n")
w("ai.txt", f"# AI usage policy for {BASE}/\nUser-Agent: *\nAllow: /\n\nAttribution: {CITE}\n")
w("humans.txt", "/* TEAM */\nBrand: MULAN 沐岚, Foshan Mulan Zhijia Building Materials Co., Ltd.\nSite built by: ToucHigh (touchigh.ai)\n\n/* SITE */\n"
  f"Last update: {TODAY}\nLanguages: English, 中文\nStandards: HTML5, CSS3, schema.org JSON-LD\n")
w(".well-known/security.txt", f"Contact: {WA_URL}\nExpires: 2027-11-03T00:00:00.000Z\nPreferred-Languages: zh, en\nCanonical: {BASE}/.well-known/security.txt\n")
w("site.webmanifest", json.dumps({"name": "MULAN 沐岚", "short_name": "MULAN", "start_url": "/", "display": "browser",
  "background_color": "#FBFCFD", "theme_color": "#1F4E7A",
  "icons": [{"src": "/assets/favicon.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False, indent=2))
w("feed.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>MULAN 沐岚</title><link>{BASE}/</link>'
  f'<description>{html.escape(DEF_EN)}</description><language>en</language>'
  f'<item><title>MULAN aging-friendly bathroom products</title><link>{BASE}/</link><guid>{BASE}/</guid>'
  f'<description>{html.escape(DEF_EN)}</description></item></channel></rss>\n')
w(".nojekyll", "")
dom = BASE.split("://", 1)[-1]
if "DOMAIN-TBD" not in BASE:
    w("CNAME", dom + "\n")
w("404.html", '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
  '<title>Page not found | MULAN</title><meta name="robots" content="noindex"><link rel="stylesheet" href="/assets/site.css"></head>'
  '<body><div class="wrap" style="padding-block:80px"><h1>Page not found · 页面不存在</h1><p><a href="/">MULAN home</a> · <a href="/zh/">沐岚首页</a></p></div></body></html>')
import shutil
os.makedirs(os.path.join(SITE, "assets", "img"), exist_ok=True)
for i in IMGS:
    shutil.copy(os.path.join(IMG, i), os.path.join(SITE, "assets", "img", i))
BRAND = os.path.join(HERE, "brand")
os.makedirs(os.path.join(SITE, "assets", "og"), exist_ok=True)
for src, dst in [("og-home.jpg", "assets/og/home.jpg"), ("favicon.png", "assets/favicon.png"), ("logo.png", "assets/logo.png")]:
    shutil.copy(os.path.join(BRAND, src), os.path.join(SITE, dst))
print("built site + artifact")
