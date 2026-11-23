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
import hashlib
ASSET_V = hashlib.md5(((SRC / "site.css").read_text() + (SRC / "site.js").read_text()).encode()).hexdigest()[:8]


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
<link rel="stylesheet" href="/assets/site.css?v={ASSET_V}">
<script>try{{var l=localStorage.getItem('vruma-lang');if(l==='es')document.documentElement.lang='es'}}catch(e){{}}</script>
</head>
<body>
<header>
  <a href="/" class="logo" aria-label="vruma">{LOGO}</a>
  <nav><a href="/work/">{tr("nav_work")}</a><a href="/about/">{tr("nav_about")}</a><a href="/contact/">{tr("nav_contact")}</a></nav>
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

END = f'<script src="/assets/site.js?v={ASSET_V}"></script>\n</body>\n</html>\n'


FEATURED = {"runflex", "ford-bronco", "atomik-yoga"}  # los 3 que se ven en el home en celular


def med(name):
    """URL de un archivo de /media con versión según su contenido (evita caché vieja al reemplazarlo)."""
    f = OUT / "media" / name
    v = hashlib.md5(f.read_bytes()).hexdigest()[:8] if f.exists() else "0"
    return f"/media/{name}?v={v}"


def card(p):
    meta_en = f'{p["c"]} · {kinds(p,"en")}' + (" · Spec" if p.get("spec") else "")
    meta_es = f'{p["c"]} · {kinds(p,"es")}' + (" · Spec" if p.get("spec") else "")
    feat = " feat" if p["id"] in FEATURED else ""
    return f"""<a class="card{feat}" href="/work/{p['id']}/">
    <div class="media"><img src="{med(p['v'] + '.jpg')}" alt="" loading="lazy"><video data-src="{med(p['v'] + '.mp4')}" muted loop playsinline preload="none"></video></div>
    <div class="meta"><h3>{e(p['t'])}</h3>{both(meta_en, meta_es, "p")}</div>
  </a>"""


def home():
    cards = "\n  ".join(card(p) for p in P)
    return head("vruma.", T["en"]["meta_desc"], "/") + f"""
<div class="player" id="player"><button class="close" id="close">{tr("close")}</button><video id="full" controls playsinline preload="none" src="/media/reel720.mp4"></video></div>

<div class="hero">
  <p class="reellbl"><span>Recap 2025</span><i></i><span>2026</span></p>
  <video id="reel" poster="/media/hero.jpg" autoplay muted loop playsinline preload="auto"></video>
  <button class="watch" id="watch"><i class="tri"></i>{tr("watch")}</button>
</div>

<main class="grid homegrid" id="grid">
  {cards}
</main>
<a class="allwork" href="/work/">{tr("all_work")} →</a>

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


def work():
    cards = "\n  ".join(card(p) for p in P)
    return head("Work — vruma.", T["en"]["meta_desc"], "/work/") + f"""
<section class="workhead pagetop"><h1 class="big">{tr("nav_work")}</h1></section>
<main class="grid" id="grid">
  {cards}
</main>

<footer class="homefoot">
    {FOOT_CONTACT}
</footer>
""" + END


BACK = "".join(f'<img src="/media/back/back_{i:02d}.jpg" alt="" width="600" height="900" loading="lazy" decoding="async">' for i in range(1, 17))


def about():
    return head("About — vruma.", T["en"]["meta_desc"], "/about/", "/media/back/back_01.jpg") + f"""
<section class="about pagetop">
  <div class="atext">
    {tr("about","p")}
    <span class="base">Mar del Plata / Buenos Aires</span>
  </div>
</section>

<section class="bstrip" aria-label="Behind the scenes"><div class="btrack">{BACK}{BACK}</div></section>

<section class="team">
  <div class="who"><b>Alvaro Arano</b>{tr("r_alv")}<a class="tel" href="https://wa.me/5492235853074">+54 9 2235 85-3074</a></div>
  <div class="who"><b>Bruno Donofrio</b>{tr("r_bru")}<a class="tel" href="https://wa.me/5492235993532">+54 9 2235 99-3532</a></div>
</section>

<footer class="slimfoot">
    <a class="next" href="/contact/">{tr("talk")} →</a>
    <div class="legal"><span>vruma collective</span><span>Mar del Plata / Buenos Aires</span></div>
</footer>
""" + END


def contact():
    return head("Contact — vruma.", T["en"]["meta_desc"], "/contact/") + f"""
<section class="cpage pagetop">
  <h1 class="big">{tr("talk")}</h1>
  <form class="cform" id="cform" data-endpoint="https://api.web3forms.com/submit" data-key="51b8f973-8580-45d8-b80f-20eabc7caee2">
    <label><small>{both("Name", "Nombre")}</small><input name="name" required autocomplete="name"></label>
    <label><small>Email</small><input name="email" type="email" required autocomplete="email"></label>
    <label class="msg"><small>{both("Message", "Mensaje")}</small><textarea name="message" rows="4" required></textarea></label>
    <input name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
    <div class="fend">
      <button type="submit" class="send"><span class="lbl">{both("Send", "Enviar")} →</span><span class="ing">{both("Sending…", "Enviando…")}</span></button>
      <p class="fstat err" hidden>{both("Couldn’t send it. Write to us at vrumacollective@gmail.com", "No se pudo enviar. Escribinos a vrumacollective@gmail.com")}</p>
    </div>
    <div class="sent" hidden>
      <p class="sentbig">{both("Message sent.", "Mensaje enviado.")}</p>
      <p class="sentsub">{both("Thanks for writing. We’ll get back to you soon.", "Gracias por escribirnos. Te respondemos a la brevedad.")}</p>
      <button type="button" class="send again">{both("Send another", "Enviar otro")}</button>
    </div>
  </form>
  <div class="cgrid">
    <div><small>Mail</small><a href="mailto:vrumacollective@gmail.com">vrumacollective@gmail.com</a></div>
    <div><small>Alvaro Arano · {tr("r_alv_s")}</small><a href="https://wa.me/5492235853074">+54 9 2235 85-3074</a></div>
    <div><small>Bruno Donofrio · {tr("r_bru_s")}</small><a href="https://wa.me/5492235993532">+54 9 2235 99-3532</a></div>
    <div><small>{tr("follow")}</small><a href="https://www.instagram.com/vruma.collective/">Instagram</a><a href="https://vimeo.com/user235217933">Vimeo</a><a href="https://www.linkedin.com/company/vrumacollective/">LinkedIn</a></div>
  </div>
</section>


<footer class="slimfoot">
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
        gdir, gpre = p.get("galdir", "trip"), p.get("galpre", "trip")
        files = p["gal"] if isinstance(p["gal"], list) else [f"{gpre}_{n:02d}.jpg" for n in range(1, p["gal"] + 1)]
        def wide(f):
            try:
                from PIL import Image
                w, h = Image.open(OUT / "media" / gdir / f).size
                return w > h
            except Exception:
                return False
        mix = p.get("galcols") == "mix"
        imgs = "".join(f'<img loading="lazy" src="{med(gdir + "/" + f)}" alt=""{" class=\"w\"" if mix and wide(f) else ""}>' for f in files)
        cols = " gal2" if p.get("galcols") == 2 else (" galmix" if mix else "")
        gal = f'<div class="gallery{cols}">{imgs}</div>'
    return head(f'{p["t"]} — vruma.', p.get("de", ""), f'/work/{p["id"]}/', f'/media/{p["v"]}.jpg') + f"""
<div class="ptitle pagetop">
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
write("work/index.html", work())
write("about/index.html", about())
write("contact/index.html", contact())
for i, p in enumerate(P):
    write(f"work/{p['id']}/index.html", project(i))
write("assets/site.css", (SRC / "site.css").read_text())
write("assets/site.js", (SRC / "site.js").read_text())
write("favicon.svg", favicon())
write("404.html", head("vruma.", T["en"]["meta_desc"], "/404") + f"""
<section class="about pagetop"><div class="atext"><p>{both("This page doesn’t exist.", "Esta página no existe.")}</p>
<span class="base"><a href="/work/">{tr("nav_work")} →</a></span></div></section>
""" + END)
urls = ["/", "/work/", "/about/", "/contact/"] + [f"/work/{p['id']}/" for p in P]
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
print(f"OK: {len(urls)} páginas")
