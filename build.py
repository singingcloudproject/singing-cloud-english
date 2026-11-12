#!/usr/bin/env python3
"""
Page builder for the Singing Cloud websites.

It reads:
  content/site.json      -> settings (website address, Instagram handle, Formspree ID, languages, section order)
  content/<lang>.json    -> all the words on the page, one file per language

and writes the finished pages:
  index.html             -> English (main language)
  fa/index.html          -> Persian (right-to-left)
  ru/index.html          -> Russian
  sitemap.xml, robots.txt

Run it after every text change:   python build.py
"""
import html
import json
import pathlib
import urllib.parse

from mascot import mascot_svg  # the layered, animatable singing cloud for the hero

ROOT = pathlib.Path(__file__).resolve().parent
CONTENT = ROOT / "content"


def e(text):
    """Make text safe to put inside HTML."""
    return html.escape(str(text), quote=True)


# ---------------------------------------------------------------- icons
ICONS = {
    "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
    "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 13h18"/>',
    "award": '<circle cx="12" cy="9" r="6"/><path d="M8.5 14 7 22l5-3 5 3-1.5-8"/>',
    "star": '<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3l-5.5 2.9 1-6.2L3 9.6l6.2-.9z"/>',
    "film": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 4v16M17 4v16M3 9h4M3 15h4M17 9h4M17 15h4"/>',
    "sparkles": '<path d="M11 3l1.8 5.2L18 10l-5.2 1.8L11 17l-1.8-5.2L4 10l5.2-1.8z"/><path d="M19 14l.8 2.2L22 17l-2.2.8L19 20l-.8-2.2L16 17l2.2-.8z"/>',
    "pen": '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="m13 7 4 4"/>',
    "carousel": '<rect x="2" y="6" width="5" height="12" rx="1.5"/><rect x="8.5" y="4" width="7" height="16" rx="1.5"/><rect x="17" y="6" width="5" height="12" rx="1.5"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "music": '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>',
    "heart": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
    "cap": '<path d="m2 9 10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5"/>',
    "building": '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M9 7h1M14 7h1M9 11h1M14 11h1M9 15h1M14 15h1M10 21v-3h4v3"/>',
    "book": '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/><path d="M8 7h8M8 10.5h6"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "check": '<path d="m5 12 5 5 9-10"/>',
    "play": '<path d="M8 5v14l11-7z" fill="currentColor" stroke="none"/>',
    "image": '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="m21 16-5-5-9 9"/>',
    "quote": '<path d="M7 17c-2 0-3-1.5-3-3.5C4 10 6 7 9 6M17 17c-2 0-3-1.5-3-3.5 0-3.5 2-6.5 5-7.5"/>',
    "whatsapp": '<path d="M20.5 11.6a8.4 8.4 0 0 1-12.4 7.4L3.5 20.5 5 16.1a8.4 8.4 0 1 1 15.5-4.5z"/><path d="M9 8.5c0 3.5 3 6.5 6.5 6.5l1-1.6-2-1-1 .8a5 5 0 0 1-2.7-2.7l.8-1-1-2z" fill="currentColor" stroke="none"/>',
}


def icon(name, cls="icon"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICONS.get(name, ICONS["star"])}</svg>'


# The Singing Cloud logo: the 3D cloud from logo.png (copied from Singing Cloud Studio).
# Header/footer use the small transparent image (WebP = fast, PNG = backup for older browsers).
def logo(prefix):
    return (f'<picture><source srcset="{prefix}assets/logo-header.webp" type="image/webp">'
            f'<img class="logo" src="{prefix}assets/logo-header.png" alt="" width="48" height="35" decoding="async"></picture>')


def hero_logo(alt):
    """The hero's singing cloud (layered SVG from mascot.py) with its glow and a layer for the
    floating A B C D letters. Animated in assets/script.js."""
    return (
        '<div class="logo-stage">'
        '<span class="art-glow" aria-hidden="true"></span>'
        f"{mascot_svg(e(alt))}"
        '<div class="letters" aria-hidden="true"></div>'
        "</div>"
    )


# ---------------------------------------------------------------- helpers
def head_block(kicker, title, intro=None):
    out = '<div class="section-head reveal">'
    if kicker:
        out += f'<p class="kicker">{e(kicker)}</p>'
    out += f"<h2>{e(title)}</h2>"
    if intro:
        out += f'<p class="lead">{e(intro)}</p>'
    return out + "</div>"


def placeholder(alt, label, icon_name="image", cls=""):
    return (
        f'<div class="ph {cls}" role="img" aria-label="{e(alt)}">'
        f'{icon(icon_name, "ph-icon")}<span>{e(label)}</span></div>'
    )


# ---------------------------------------------------------------- sections
def s_hero(sec, t, ctx):
    badges = "".join(f"<li>{icon('check')}{e(b)}</li>" for b in t.get("badges", []))
    secondary = ""
    if t.get("secondary"):
        secondary = f'<a class="btn btn-ghost" href="#{e(t.get("secondary_target", ""))}">{e(t["secondary"])}</a>'
    return f"""
<section class="hero" id="top">
  <div class="sky" aria-hidden="true"><span class="cloud c1"></span><span class="cloud c2"></span><span class="cloud c3"></span><span class="cloud c4"></span><span class="glow"></span></div>
  <div class="container hero-inner">
    <div class="hero-copy">
      <p class="kicker reveal">{e(t.get("eyebrow", ""))}</p>
      <h1 class="reveal" style="--d:100ms">{e(t["title"])}<span class="h1-sub">{e(t.get("title_sub", ""))}</span></h1>
      <p class="lead reveal" style="--d:200ms">{e(t["subtitle"])}</p>
      <div class="hero-actions reveal" style="--d:300ms">
        <a class="btn btn-gold" href="#contact">{e(t["cta"])}</a>
        {secondary}
      </div>
      <ul class="badges reveal" style="--d:400ms">{badges}</ul>
    </div>
    <div class="hero-art reveal" style="--d:250ms">
      {hero_logo(t.get("logo_alt", t["title"]))}
    </div>
  </div>
</section>"""


def s_cards(sec, t, ctx):
    cards = ""
    for i, it in enumerate(t["items"]):
        points = ""
        if it.get("points"):
            points = '<ul class="points">' + "".join(f"<li>{icon('check')}{e(p)}</li>" for p in it["points"]) + "</ul>"
        cards += f"""
      <article class="card reveal" style="--d:{i * 80}ms">
        <div class="card-icon">{icon(it.get("icon", "star"))}</div>
        <h3>{e(it["name"])}</h3>
        <p>{e(it["text"])}</p>{points}
      </article>"""
    variant = sec.get("variant", "")
    # optional closing line under the cards (e.g. "Every lesson is built around your level…")
    after = f'<p class="cards-after reveal">{e(t["after"])}</p>' if t.get("after") else ""
    return f"""
<section class="section {e(sec.get("bg", ""))}" id="{e(sec["id"])}">
  <div class="container">
    {head_block(t.get("kicker"), t["title"], t.get("intro"))}
    <div class="cards {e(variant)}">{cards}
    </div>
    {after}
  </div>
</section>"""



def s_club(sec, t, ctx):
    """Speaking Club highlight: a big headline, short text, the two prices and a button."""
    points = "".join(f"<li>{icon('check')}<span>{e(p)}</span></li>" for p in t.get("points", []))
    return f"""
<section class="section club" id="{e(sec["id"])}">
  <div class="container narrow club-inner">
    <div class="club-icon reveal">{icon("chat")}</div>
    <p class="kicker reveal">{e(t["kicker"])}</p>
    <h2 class="reveal">{e(t["title"])}</h2>
    <p class="lead reveal">{e(t["text"])}</p>
    <ul class="club-points reveal">{points}</ul>
    <a class="btn btn-gold reveal" href="#contact">{e(t["cta"])}</a>
  </div>
</section>"""


def s_about(sec, t, ctx):
    cfg = ctx["site"]
    photo = cfg.get("about_photo")
    if photo:
        pic = f'<img class="about-photo" src="{ctx["prefix"]}{e(photo)}" alt="{e(t["photo_alt"])}" loading="lazy" width="600" height="750">'
    else:
        pic = placeholder(t["photo_alt"], t.get("photo_label", ""), "image", "about-photo")
    vid_id = cfg.get("intro_video_youtube_id")
    if vid_id:
        video = (
            f'<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{e(vid_id)}" '
            f'title="{e(t["video_label"])}" loading="lazy" allow="encrypted-media; picture-in-picture" allowfullscreen></iframe></div>'
        )
    else:
        video = f'<div class="video">{placeholder(t["video_label"], t["video_note"], "play", "video-ph")}</div>'
    bio = "".join(f"<p>{e(p)}</p>" for p in t["bio"])
    stats = "".join(f'<li><strong>{e(s["num"])}</strong><span>{e(s["label"])}</span></li>' for s in t.get("stats", []))
    return f"""
<section class="section bg-soft" id="{e(sec["id"])}">
  <div class="container about">
    <div class="about-media reveal">{pic}</div>
    <div class="about-text reveal">
      <p class="kicker">{e(t["kicker"])}</p>
      <h2>{e(t["title"])}</h2>
      <p class="about-name">{e(t["name"])} <span>· {e(t["role"])}</span></p>
      {bio}
      <ul class="stats">{stats}</ul>
    </div>
    <div class="about-video reveal">
      <h3>{e(t["video_label"])}</h3>
      {video}
    </div>
  </div>
</section>"""


def s_teachers(sec, t, ctx):
    """'Our Teachers': one card per country with its official flag (files in assets/flags/, from Wikimedia Commons)."""
    cards = ""
    for i, it in enumerate(t["items"]):
        flag = it["flag"]
        w, h = FLAG_SIZES[flag]
        cards += f"""
      <article class="card country reveal" style="--d:{i * 100}ms">
        <div class="flag-frame"><img class="flag" src="{ctx["prefix"]}assets/flags/{flag}.svg" alt="{e(it["alt"])}" width="{w}" height="{h}" loading="lazy" decoding="async"></div>
        <h3>{e(it["country"])}</h3>
        <p>{e(it["line"])}</p>
      </article>"""
    return f"""
<section class="section" id="{e(sec["id"])}">
  <div class="container">
    {head_block(t.get("kicker"), t["title"], t.get("intro"))}
    <div class="cards countries">{cards}
    </div>
    <div class="match reveal">
      <p>{e(t["match"])}</p>
      <a class="btn btn-gold" href="#contact">{e(t["cta"])}</a>
    </div>
    {f'<p class="teach-link reveal"><a href="#join">{e(t["teach_link"])}</a></p>' if t.get("teach_link") else ""}
  </div>
</section>"""


# real proportions of each official flag (width, height) — so they are never stretched
FLAG_SIZES = {"canada": (200, 100), "usa": (190, 100), "uk": (200, 100)}


def s_portfolio(sec, t, ctx):
    tiles = ""
    for i, it in enumerate(t["items"]):
        if it.get("image"):
            media = f'<img src="{ctx["prefix"]}{e(it["image"])}" alt="{e(it["alt"])}" loading="lazy" width="800" height="1000">'
        else:
            media = placeholder(it["alt"], t["placeholder_label"], "image")
        tags = f'<p class="muted">{e(it["tag"])}</p>' if it.get("tag") else ""
        tiles += f"""
      <figure class="work reveal {"work-wide" if i == 0 else ""}" style="--d:{i * 70}ms">
        <div class="work-media">{media}</div>
        <figcaption><h3>{e(it["title"])}</h3>{tags}</figcaption>
      </figure>"""
    return f"""
<section class="section bg-soft" id="{e(sec["id"])}">
  <div class="container">
    {head_block(t.get("kicker"), t["title"], t.get("intro"))}
    <div class="gallery">{tiles}
    </div>
  </div>
</section>"""


def s_prices(sec, t, ctx):
    """Price cards. Each language file has its own prices and currency (USD or rubles).
    "best": true highlights a card as "Best value"."""
    cards = ""
    for i, it in enumerate(t["items"]):
        best = it.get("best")
        badge = f'<span class="tag-gold popular">{e(t["best_value"])}</span>' if best else ""
        cards += f"""
      <article class="card price reveal {"featured" if best else ""}" style="--d:{(i % 4) * 80}ms">
        {badge}
        <p class="price-for">{e(it["for"])}</p>
        <h3>{e(it["name"])}</h3>
        <p class="amount">{e(it["price"])}</p>
        <p class="muted price-per">{e(it["per"])}</p>
        <a class="btn {"btn-gold" if best else "btn-ghost"} btn-sm" href="#contact">{e(t["choose"])}</a>
      </article>"""
    return f"""
<section class="section {e(sec.get("bg", ""))}" id="{e(sec["id"])}">
  <div class="container">
    {head_block(t.get("kicker"), t["title"], t.get("intro"))}
    <p class="price-range reveal">{e(t["range"])}</p>
    <div class="cards cards-4 price-grid">{cards}
    </div>
    <div class="unsure reveal">
      <p>{e(t["unsure"])}</p>
      <a class="btn btn-gold" href="#contact">{e(t["unsure_cta"])}</a>
    </div>
  </div>
</section>"""


def s_join(sec, t, ctx):
    """'Teach with us': invitation for teachers + an application form (Formspree, its own form ID)."""
    cfg = ctx["site"]
    f = t["form"]
    form_id = cfg.get("formspree_teachers_id", "YOUR_TEACHER_FORM_ID")
    connected = "YOUR_" not in form_id
    checks = "".join(
        f'<label class="check"><input type="checkbox" value="{e(o)}" data-join="lessons"><span>{e(o)}</span></label>'
        for o in f["lesson_options"]
    )
    perks = "".join(f"<li>{icon('check')}{e(p)}</li>" for p in t.get("perks", []))
    return f"""
<section class="section {e(sec.get("bg", ""))}" id="{e(sec["id"])}">
  <div class="container contact join">
    <div class="contact-text reveal">
      <p class="kicker">{e(t["kicker"])}</p>
      <h2>{e(t["title"])}</h2>
      <p class="lead">{e(t["intro"])}</p>
      <ul class="points join-perks">{perks}</ul>
    </div>
    <form class="form card reveal" action="https://formspree.io/f/{e(form_id)}" method="POST"
          data-connected="{str(connected).lower()}" data-sending="{e(f["sending"])}" data-success="{e(f["success"])}"
          data-error="{e(f["error"])}" data-not-connected="{e(f["not_connected"])}">
      <p class="form-or">{e(f["heading"])}</p>
      <input type="hidden" name="_subject" value="{e(f["subject"])}">
      <input type="hidden" name="_language" value="{e(ctx["lang"]["code"])}">
      <input type="hidden" name="lessons" value="">
      <div class="hp" aria-hidden="true"><label>Leave empty <input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label></div>
      <div class="form-row">
        <label>{e(f["name"])}<input type="text" name="name" required autocomplete="name"></label>
        <label>{e(f["email"])}<input type="email" name="email" required autocomplete="email" dir="ltr"></label>
      </div>
      <div class="form-row">
        <label>{e(f["country"])}<input type="text" name="country" required autocomplete="country-name"></label>
        <label>{e(f["native_language"])}<input type="text" name="native_language" required></label>
      </div>
      <label>{e(f["experience"])}<input type="number" name="experience_years" min="0" max="60" step="1" required inputmode="numeric"></label>
      <fieldset class="checks"><legend>{e(f["lessons"])}</legend>{checks}</fieldset>
      <label>{e(f["availability"])}<textarea name="availability" rows="2" required placeholder="{e(f["availability_hint"])}"></textarea></label>
      <label>{e(f["video"])}<input type="url" name="intro_video" placeholder="https://" dir="ltr"></label>
      <label>{e(f["message"])}<textarea name="message" rows="3"></textarea></label>
      <button class="btn btn-gold" type="submit">{e(f["send"])}</button>
      <p class="form-status" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>"""


def s_steps(sec, t, ctx):
    steps = ""
    for i, st in enumerate(t["steps"]):
        num = ctx["digits"][i + 1] if i + 1 < len(ctx["digits"]) else i + 1
        steps += f"""
      <li class="step reveal" style="--d:{i * 100}ms">
        <span class="step-num">{e(num)}</span>
        <h3>{e(st["title"])}</h3>
        <p>{e(st["text"])}</p>
      </li>"""
    return f"""
<section class="section bg-deep" id="{e(sec["id"])}">
  <div class="container">
    {head_block(t.get("kicker"), t["title"], t.get("intro"))}
    <ol class="steps steps-{len(t["steps"])}">{steps}
    </ol>
  </div>
</section>"""


def s_testimonials(sec, t, ctx):
    items = ""
    for it in t["items"]:
        items += f"""
      <figure class="testimonial reveal">
        {icon("quote", "quote-icon")}
        <blockquote><p>{e(it["quote"])}</p></blockquote>
        <figcaption><strong>{e(it["name"])}</strong><span>{e(it["role"])}</span></figcaption>
      </figure>"""
    return f"""
<section class="section" id="{e(sec["id"])}">
  <div class="container narrow">
    {head_block(t.get("kicker"), t["title"], t.get("intro"))}
    {items}
  </div>
</section>"""


def s_faq(sec, t, ctx):
    items = "".join(
        f'<details class="faq-item reveal"><summary>{e(it["q"])}</summary><p>{e(it["a"])}</p></details>'
        for it in t["items"]
    )
    return f"""
<section class="section bg-soft" id="{e(sec["id"])}">
  <div class="container narrow">
    {head_block(t.get("kicker"), t["title"], t.get("intro"))}
    <div class="faq">{items}</div>
  </div>
</section>"""


def s_contact(sec, t, ctx):
    cfg = ctx["site"]
    f = t["form"]
    ig = f'https://ig.me/m/{cfg["instagram_handle"]}'
    options = "".join(f"<option>{e(o)}</option>" for o in f["topic_options"])
    connected = "YOUR_" not in cfg["formspree_id"]
    return f"""
<section class="section contact-section" id="{e(sec["id"])}">
  <div class="sky sky-soft" aria-hidden="true"><span class="cloud c2"></span><span class="cloud c4"></span></div>
  <div class="container contact">
    <div class="contact-text reveal">
      <p class="kicker">{e(t["kicker"])}</p>
      <h2>{e(t["title"])}</h2>
      <p class="lead">{e(t["intro"])}</p>
      <a class="btn btn-instagram" href="{e(ig)}" target="_blank" rel="noopener"><img class="ig-logo" src="{ctx["prefix"]}assets/icons/color/instagram.svg" alt="" width="22" height="22" decoding="async">{e(t["instagram_btn"])}</a>
      <p class="muted small">{e(t.get("instagram_note", ""))}</p>
    </div>
    <form class="form card reveal" action="https://formspree.io/f/{e(cfg["formspree_id"])}" method="POST"
          data-connected="{str(connected).lower()}" data-sending="{e(f["sending"])}" data-success="{e(f["success"])}"
          data-error="{e(f["error"])}" data-not-connected="{e(f["not_connected"])}">
      <p class="form-or">{e(t["or"])}</p>
      <input type="hidden" name="_subject" value="{e(f["subject"])}">
      <input type="hidden" name="_language" value="{e(ctx["lang"]["code"])}">
      <div class="hp" aria-hidden="true"><label>Leave empty <input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label></div>
      <label>{e(f["name"])}<input type="text" name="name" required autocomplete="name"></label>
      <label>{e(f["email"])}<input type="email" name="email" required autocomplete="email" dir="ltr"></label>
      <label>{e(f["phone"])}<input type="tel" name="phone" autocomplete="tel" dir="ltr"></label>
      <label>{e(f["topic"])}<select name="topic">{options}</select></label>
      <label>{e(f["message"])}<textarea name="message" rows="4" required></textarea></label>
      <button class="btn btn-gold" type="submit">{e(f["send"])}</button>
      <p class="form-status" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>"""


RENDERERS = {
    "hero": s_hero,
    "cards": s_cards,
    "about": s_about,
    "club": s_club,
    "teachers": s_teachers,
    "portfolio": s_portfolio,
    "prices": s_prices,
    "steps": s_steps,
    "testimonials": s_testimonials,
    "faq": s_faq,
    "contact": s_contact,
    "join": s_join,
}

PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
LATIN_DIGITS = "0123456789"


# ---------------------------------------------------------------- page
OG_LOCALES = {"en": "en_US", "fa": "fa_IR", "ru": "ru_RU", "hy": "hy_AM"}
LANG_NAMES = {"en": "English", "fa": "Persian", "ru": "Russian", "hy": "Armenian"}


def build_schema(site, lang, t, langs, base, url):
    """Structured data for Google: the English school (an educational organisation) with its lessons and
    prices, the website, this page, and the FAQ."""
    currency = "RUB" if lang["code"] == "ru" else "USD"

    def amount(price):
        digits = "".join(ch for ch in price if ch.isdigit())
        return digits or None

    offers = []
    for it in t["prices"]["items"]:
        if it["price"].strip().startswith("+"):
            continue  # an add-on, not a lesson on its own
        offers.append({"@type": "Offer", "name": f'{it["name"]} — {it["for"]}', "description": it["per"],
                       "price": amount(it["price"]), "priceCurrency": currency, "url": url + "#prices"})
    school = {
        "@type": "EducationalOrganization",
        "@id": base + "#school",
        "name": site["brand"],
        "url": base,
        "logo": base + "assets/logo-hero.png",
        "image": base + "assets/og-image.jpg",
        "description": t["meta"]["description"],
        "slogan": t["hero"]["title"],
        "areaServed": "Worldwide",
        "availableLanguage": [LANG_NAMES[l["code"]] for l in langs],
        "knowsAbout": [it["name"] for it in t["lessons"]["items"]],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": t["prices"]["title"], "itemListElement": offers},
    }
    website = {"@type": "WebSite", "@id": base + "#website", "url": base, "name": site["brand"],
               "inLanguage": [l["code"] for l in langs], "publisher": {"@id": base + "#school"}}
    webpage = {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": t["meta"]["title"],
               "description": t["meta"]["description"], "inLanguage": lang["code"],
               "isPartOf": {"@id": base + "#website"}, "about": {"@id": base + "#school"}}
    faq = {"@type": "FAQPage", "@id": url + "#faq", "inLanguage": lang["code"],
           "mainEntity": [{"@type": "Question", "name": it["q"],
                           "acceptedAnswer": {"@type": "Answer", "text": it["a"]}} for it in t["faq"]["items"]]}
    return {"@context": "https://schema.org", "@graph": [school, website, webpage, faq]}

def page(site, lang, t, langs):
    depth = lang["path"].count("/")
    prefix = "../" * depth
    base = site["site_url"].rstrip("/") + "/"
    url = base + lang["path"]
    ctx = {
        "site": site,
        "lang": lang,
        "prefix": prefix,
        "digits": PERSIAN_DIGITS if lang["code"] == "fa" else LATIN_DIGITS,
    }

    # nav links: every section that has a label in t["nav"]["links"]
    # "Teach with us" is for teachers, not students: it lives in the footer and the Teachers section, not the top menu
    nav_links = "".join(
        f'<li><a href="#{e(sid)}">{e(label)}</a></li>' for sid, label in t["nav"]["links"].items() if sid != "join"
    )
    join_link = (f'<a class="footer-join" href="#join">{e(t["nav"]["links"]["join"])}</a>'
                 if "join" in t["nav"]["links"] else "")
    switch = "".join(
        f'<a href="{prefix}{l["path"]}index.html" hreflang="{l["code"]}" lang="{l["code"]}"'
        + (' aria-current="true"' if l["code"] == lang["code"] else "")
        + f'>{e(l["label"])}</a>'
        for l in langs
    )
    alternates = "\n".join(
        f'  <link rel="alternate" hreflang="{l["code"]}" href="{base}{l["path"]}">' for l in langs
    )
    alternates += f'\n  <link rel="alternate" hreflang="x-default" href="{base}">'

    body = "".join(RENDERERS[sec["type"]](sec, t[sec["id"]], ctx) for sec in site["sections"])

    schema = build_schema(site, lang, t, langs, base, url)
    # "noindex" keeps the site out of Google until it is final (set "noindex": false in content/site.json to go live)
    robots = '  <meta name="robots" content="noindex">\n' if site.get("noindex") else ""
    og_alt_locales = "".join(f'  <meta property="og:locale:alternate" content="{OG_LOCALES[l["code"]]}">\n'
                             for l in langs if l["code"] != lang["code"])
    fonts = (
        "https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800"
        "&family=Noto+Sans+Armenian:wght@400;600;700;800&display=swap"
    )
    draft = f"\n<!-- DRAFT: {e(t['_draft_note'])} -->" if t.get("_draft_note") else ""
    return f"""<!doctype html>{draft}
<html lang="{lang["code"]}" dir="{lang["dir"]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(t["meta"]["title"])}</title>
  <meta name="description" content="{e(t["meta"]["description"])}">
  <link rel="canonical" href="{url}">
{alternates}
{robots}  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{e(site["brand"])}">
  <meta property="og:title" content="{e(t["meta"].get("og_title", t["meta"]["title"]))}">
  <meta property="og:description" content="{e(t["meta"]["description"])}">
  <meta property="og:url" content="{url}">
  <meta property="og:locale" content="{e(t["meta"]["og_locale"])}">
{og_alt_locales}  <meta property="og:image" content="{base}assets/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{e(t["meta"].get("og_image_alt", site["brand"]))}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(t["meta"].get("og_title", t["meta"]["title"]))}">
  <meta name="twitter:description" content="{e(t["meta"]["description"])}">
  <meta name="twitter:image" content="{base}assets/og-image.jpg">
  <meta name="theme-color" content="#fbf6ec">
  <link rel="icon" href="{prefix}assets/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="{prefix}assets/favicon-180.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="{fonts}">
  <link rel="stylesheet" href="{prefix}assets/styles.css">
  <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">{e(t["nav"]["skip"])}</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="#top" aria-label="{e(site["brand"])}">{logo(prefix)}<span>{e(site["brand"])}</span></a>
    <nav class="nav" id="site-nav" aria-label="{e(t["nav"]["menu"])}">
      <ul>{nav_links}</ul>
    </nav>
    <div class="header-actions">
      <div class="lang-switch" role="navigation" aria-label="{e(t["nav"]["language"])}">{switch}</div>
      <a class="btn btn-gold btn-sm header-cta" href="#contact">{e(t["nav"]["cta"])}</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="{e(t["nav"]["menu"])}"><span></span><span></span></button>
    </div>
  </div>
</header>
<main id="main">{body}
</main>
<footer class="site-footer">
  <div class="container footer-inner">
    <a class="brand" href="#top">{logo(prefix)}<span>{e(site["brand"])}</span></a>
    <p>{e(t["footer"]["tagline"])}</p>
    {join_link}
    <div class="lang-switch">{switch}</div>
    <p class="muted small">© <span data-year></span> {e(site["brand"])}. {e(t["footer"]["rights"])}</p>
  </div>
</footer>
<script src="{prefix}assets/script.js" defer></script>
</body>
</html>
"""


def main():
    site = json.loads((CONTENT / "site.json").read_text(encoding="utf-8"))
    langs = [l for l in site["languages"] if l.get("enabled", True)]
    for lang in langs:
        src = CONTENT / f'{lang["code"]}.json'
        t = json.loads(src.read_text(encoding="utf-8"))
        out = ROOT / lang["path"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(site, lang, t, langs), encoding="utf-8")
        print("built", out.relative_to(ROOT))

    base = site["site_url"].rstrip("/") + "/"
    urls = ""
    for l in langs:
        alts = "".join(
            f'\n    <xhtml:link rel="alternate" hreflang="{a["code"]}" href="{base}{a["path"]}"/>' for a in langs
        )
        urls += f"\n  <url>\n    <loc>{base}{l['path']}</loc>\n    <lastmod>{__import__('datetime').date.today().isoformat()}</lastmod>{alts}\n  </url>"
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'
        f"{urls}\n</urlset>\n",
        encoding="utf-8",
    )
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {base}sitemap.xml\n", encoding="utf-8")
    print("built sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()
