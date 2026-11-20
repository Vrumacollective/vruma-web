#!/usr/bin/env python3
"""Genera el sitio estático de Vruma en /public a partir de /data.

Uso:  python3 src/build.py
Editá data/projects.json (proyectos) o data/i18n.json (textos) y volvé a correrlo.
"""
import json, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, DATA, OUT = ROOT / "src", ROOT / "data", ROOT / "public"
SITE = "https://vrumacollective.com"

P = json.loads((DATA / "projects.json").read_text())
T = json.loads((DATA / "i18n.json").read_text())
LOGO = (SRC / "logo.svg.html").read_text().strip()
SOCIAL = (SRC / "social.html").read_text().strip()
e = html.escape


def tr(key, tag="span", cls=""):
    """Texto en los dos idiomas; el CSS muestra solo el activo."""
    c = f' class="{cls}"' if cls else ""
    return (f'<{tag}{c} lang="en">{e(T["en"][key])}</{tag}>'
            f'<{tag}{c} lang="es">{e(T["es"][key])}</{tag}>')


def both(en, es, tag="span", cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c} lang="en">{e(en)}</{tag}><{tag}{c} lang="es">{e(es)}</{tag}>'


def kinds(p, lang):
    return " + ".join(T[lang][k] for k in p["k"])


def head(title, desc_en, path, image="/media/hero.jpg"):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc_en)}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc_en)}">
<meta property="og:image" content="{SITE}{image}">
<meta property="og:url" content="{SITE}{path}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1B1D20">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
<script>try{{var l=localStorage.getItem('vruma-lang');if(l==='es')document.documentElement.lang='es'}}catch(e){{}}</script>
</head>
<body>
<header>
  <a href="/" class="logo" aria-label="vruma">{LOGO}</a>
  <nav><a href="/">{tr("nav_work")}</a><a href="/about/">{tr("nav_about")}</a><a href="/about/#contact">{tr("nav_contact")}</a></nav>
  <div class="social">
    <button class="tgl" id="langBtn" aria-label="Language"><span class="en">EN</span>/<span class="es">ES</span></button>
    <i class="vsep"></i>
    {SOCIAL}
  </div>
</header>
"""


FOOT_CONTACT = """<div class="contact">
      <div><small>Mail</small><a href="mailto:vrumacollective@gmail.com">vrumacollective@gmail.com</a></div>
      <div><small>WhatsApp</small><a href="https://wa.me/5492235993532">+54 9 2235 99-3532</a> <span class="sep">/</span> <a href="https://wa.me/5492235853074">+54 9 2235 85-3074</a></div>
      <div><small>Instagram</small><a href="https://www.instagram.com/vruma.collective/">@vruma.collective</a></div>
    </div>
    <div class="legal"><span>vruma collective</span><span>Mar del Plata / Buenos Aires</span></div>"""

END = '<script src="/assets/site.js"></script>\n</body>\n</html>\n'


def card(p):
    meta_en = f'{p["c"]} · {kinds(p,"en")}' + (" · Spec" if p.get("spec") else "")
    meta_es = f'{p["c"]} · {kinds(p,"es")}' + (" · Spec" if p.get("spec") else "")
    return f"""<a class="card" href="/work/{p['id']}/">
    <div class="media"><img src="/media/{p['v']}.jpg" alt="" loading="lazy"><video data-src="/media/{p['v']}.mp4" muted loop playsinline preload="none"></video></div>
    <div class="meta"><h3>{e(p['t'])}</h3>{both(meta_en, meta_es, "p")}</div>
  </a>"""


def home():
    cards = "\n  ".join(card(p) for p in P)
    return head("vruma.", T["en"]["meta_desc"], "/") + f"""
<div class="player" id="player"><button class="close" id="close">{tr("close")}</button><video id="full" controls playsinline preload="none" src="/media/reel720.mp4"></video></div>

<div class="hero">
  <video id="reel" poster="/media/hero.jpg" autoplay muted loop playsinline preload="auto"></video>
  <button class="watch" id="watch"><i class="tri"></i>{tr("watch")}</button>
</div>

<main class="grid" id="grid">
  {cards}
</main>

<section class="spec">
  <ul class="words">
    <li>Commercials</li><li>Branded content</li><li>{tr("s_photo")}</li><li>{tr("s_ai")}</li>
  </ul>
  <div class="detail">
    <div><b>Commercials</b>{tr("d_com","p")}</div>
    <div><b>Branded content</b>{tr("d_bra","p")}</div>
    <div><b>{tr("s_photo")}</b>{tr("d_pho","p")}</div>
    <div><b>{tr("s_ai")}</b>{tr("d_ai","p")}</div>
  </div>
</section>

<footer class="homefoot">
    {FOOT_CONTACT}
</footer>
""" + END


def about():
    return head("About — vruma.", T["en"]["meta_desc"], "/about/", "/media/bts.jpg") + f"""
<section class="about pagetop">
  <div class="atext">
    {tr("about","p")}
    <span class="base">Mar del Plata / Buenos Aires</span>
  </div>
  <div class="aimg"><img src="/media/bts.jpg" alt="Vruma on set"></div>
</section>

<section class="team">
  <div><div class="who"><b>Alvaro Arano</b>{tr("r_alv")}<br><a href="https://wa.me/5492235993532">+54 9 2235 99-3532</a></div></div>
  <div><div class="who"><b>Bruno Donofrio</b>{tr("r_bru")}<br><a href="https://wa.me/5492235853074">+54 9 2235 85-3074</a></div></div>
</section>

<footer id="contact">
    <div class="big">{tr("talk")}</div>
    <div class="contact">
      <div><small>Mail</small><a href="mailto:vrumacollective@gmail.com">vrumacollective@gmail.com</a></div>
      <div><small>Alvaro Arano</small><a href="https://wa.me/5492235993532">+54 9 2235 99-3532</a></div>
      <div><small>Bruno Donofrio</small><a href="https://wa.me/5492235853074">+54 9 2235 85-3074</a></div>
      <div><small>Instagram</small><a href="https://www.instagram.com/vruma.collective/">@vruma.collective</a></div>
    </div>
    <div class="legal"><span>vruma collective</span><span>Mar del Plata / Buenos Aires</span></div>
</footer>
""" + END


def project(i):
    p = P[i]
    prev, nxt = P[(i - 1) % len(P)], P[(i + 1) % len(P)]
    spec_en = " · " + T["en"]["spec"] if p.get("spec") else ""
    spec_es = " · " + T["es"]["spec"] if p.get("spec") else ""
    vids = ""
    for vid, label in p.get("vm", []):
        lab = both(T["en"].get(label, label), T["es"].get(label, label)) if label in T["en"] else e(label)
        vids += f"""
  <figure class="embed"><div class="frame"><iframe src="https://player.vimeo.com/video/{vid}?dnt=1&title=0&byline=0&portrait=0" loading="lazy" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen title="{e(label)}"></iframe></div><figcaption>{lab}</figcaption></figure>"""
    gal = ""
    if p.get("gal"):
        imgs = "".join(f'<img loading="lazy" src="/media/trip/trip_{n:02d}.jpg" alt="">' for n in range(1, p["gal"] + 1))
        gal = f'<div class="gallery">{imgs}</div>'
    return head(f'{p["t"]} — vruma.', p.get("de", ""), f'/work/{p["id"]}/', f'/media/{p["v"]}.jpg') + f"""
<div class="phero"><video src="/media/{p['v']}.mp4" poster="/media/{p['v']}.jpg" autoplay muted loop playsinline></video></div>
<div class="ptitle">
  <h1>{e(p['t'])}</h1>
  <dl class="facts">
    <dt>{tr("client")}</dt><dd>{e(p['c'])}</dd>
    <dt>{tr("year")}</dt><dd>{e(p['y'])}</dd>
    <dt>{tr("type")}</dt><dd>{both(kinds(p,"en")+spec_en, kinds(p,"es")+spec_es)}</dd>
  </dl>
</div>
{both(p.get("de",""), p.get("d",""), "p", "pdesc")}
<div class="embeds">{vids}
</div>
{gal}
<div class="pnav"><a href="/work/{prev['id']}/">← {e(prev['t'])}</a><a href="/work/{nxt['id']}/">{e(nxt['t'])} →</a></div>
<footer>
    {FOOT_CONTACT}
</footer>
""" + END


def favicon():
    inner = LOGO[LOGO.index(">") + 1:LOGO.rindex("</svg>")].replace('fill="currentColor"', 'fill="#E0DFDA"')
    vb = LOGO.split('viewBox="')[1].split('"')[0].split()
    w, h = float(vb[2]), float(vb[3]); s = max(w, h) * 1.5
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s:.0f} {s:.0f}">'
            f'<rect width="{s:.0f}" height="{s:.0f}" rx="{s*0.22:.0f}" fill="#1B1D20"/>'
            f'<g transform="translate({(s-w)/2:.0f} {(s-h)/2:.0f})">{inner}</g></svg>')


def write(rel, text):
    f = OUT / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text)


write("index.html", home())
write("about/index.html", about())
for i, p in enumerate(P):
    write(f"work/{p['id']}/index.html", project(i))
write("assets/site.css", (SRC / "site.css").read_text())
write("assets/site.js", (SRC / "site.js").read_text())
write("favicon.svg", favicon())
write("404.html", head("vruma.", T["en"]["meta_desc"], "/404") + f"""
<section class="about pagetop"><div class="atext"><p>{both("This page doesn’t exist.", "Esta página no existe.")}</p>
<span class="base"><a href="/">{tr("nav_work")} →</a></span></div></section>
""" + END)
urls = ["/", "/about/"] + [f"/work/{p['id']}/" for p in P]
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
print(f"OK: {len(urls)} páginas")
