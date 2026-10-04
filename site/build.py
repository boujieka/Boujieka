"""Construit les pages de la landing page TasetyGrid.

Sorties :
- site/index.html et site/en/index.html : publication en Artifact (la page
  française sans squelette, l'artifact l'ajoute ; la page anglaise complète) ;
- site/public/ : site statique complet et application web installable (PWA) :
  FR à la racine, EN sous en/, manifeste, service worker et icônes. Tous les
  liens sont relatifs : le site fonctionne à la racine d'un domaine (Netlify)
  comme dans un sous-dossier (GitHub Pages : /Boujieka/).

Usage : python3 site/build.py
"""
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
LOGO = ROOT.parent / "brand" / "logo"
sys.path.insert(0, str(ROOT))
from i18n_en import EN  # noqa: E402

# Indices de français restant dans la page anglaise (hors noms propres et sigles)
FRANCAIS = re.compile(r"[éèêàùçôîœ]|\b(le|la|les|des|du|une|est|et|pour|avec|sans|dans)\b", re.I)
AUTORISE = ("Afrique", "Antarctique", "Asie", "Amérique", "Océanie", "Océans", "Ta-Sety", "MINDCAF", "ARDFC", "AJPTER", "RGPH", "RGAE", "Kodya", "KODYA", "kodya", "tꜣ-stj")


def inner(svg_text):
    body = re.sub(r"^.*?<svg[^>]*>", "", svg_text, count=1, flags=re.S)
    body = re.sub(r"</svg>\s*$", "", body)
    return re.sub(r"<title>.*?</title>", "", body, flags=re.S).strip()


def themable(svg_body, prefix):
    for hexa, var in (("#1D3F8F", "--logo-bleu"), ("#C9982E", "--logo-or"), ("#A6412B", "--logo-ocre")):
        svg_body = svg_body.replace(f'fill="{hexa}"', f'style="fill:var({var})"')
        svg_body = svg_body.replace(f'stroke="{hexa}"', f'style="stroke:var({var})"')
    return re.sub(r"clip(\d+)", lambda m: f"{prefix}{m.group(1)}", svg_body)


def traduire(html):
    for fr in sorted(EN, key=len, reverse=True):
        if fr not in html:
            raise SystemExit(f"Clé de traduction introuvable dans le gabarit : {fr[:70]!r}")
        html = html.replace(fr, EN[fr])
    # Contrôle : texte visible et chaînes du script
    visible = re.sub(r"<style>.*?</style>|<svg.*?</svg>", " ", html, flags=re.S)
    textes = re.findall(r">([^<>]+)<", visible) + re.findall(r'"([^"]{3,})"', visible[visible.find("<script>"):])
    restes = [t.strip() for t in textes if FRANCAIS.search(t) and not any(a in t for a in AUTORISE)]
    restes = [t for t in restes if t and not t.startswith(("ligne", "conf", "data-", "aria-"))]
    if restes:
        raise SystemExit("Texte français restant dans la page anglaise :\n  " + "\n  ".join(restes[:20]))
    return html


def document(contenu, lang, alt_href, alt_lang, racine=None):
    """Document HTML complet (doctype, lang, hreflang). Avec `racine` (chemin relatif
    vers la racine du site), ajoute le manifeste, les icônes et le service worker."""
    i = contenu.index("<header")
    tete, corps = contenu[:i], contenu[i:]
    pwa, script = "", ""
    if racine is not None:
        pwa = (f'<link rel="manifest" href="{racine}manifest.webmanifest">\n'
               '<meta name="theme-color" content="#1D3F8F">\n'
               f'<link rel="apple-touch-icon" href="{racine}icons/apple-touch-icon.png">\n'
               '<meta name="apple-mobile-web-app-title" content="TasetyGrid">\n')
        script = ('<script>if ("serviceWorker" in navigator) { window.addEventListener("load", function () {'
                  f' navigator.serviceWorker.register("{racine}sw.js", {{ scope: "{racine}" }}).catch(function () {{}}); }}); }}</script>\n')
    return ("<!doctype html>\n"
            f'<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            f'<link rel="alternate" hreflang="{alt_lang}" href="{alt_href}">\n'
            + pwa + tete + "</head>\n<body>\n" + corps + "\n" + script + "</body>\n</html>\n")


MANIFESTE = {
    "name": "TasetyGrid — Atlas des personnes, des terres et des ressources",
    "short_name": "TasetyGrid",
    "description": "Savoir ce qui existe sur chaque territoire, et ce qui manque.",
    "lang": "fr",
    "dir": "ltr",
    "id": "./",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "background_color": "#F6F0E4",
    "theme_color": "#1D3F8F",
    "icons": [
        {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
    "shortcuts": [
        {"name": "English version", "short_name": "English", "url": "./en/", "lang": "en"},
    ],
}


def ecrire_pwa(public):
    """Manifeste, icônes et service worker (versionné par le contenu du site)."""
    shutil.copytree(ROOT / "static" / "icons", public / "icons", dirs_exist_ok=True)
    cible = public / "atlas"
    cible.mkdir(parents=True, exist_ok=True)
    for f in ("atlas-map.js", "atlas-map.css", "atlas-dashboard.js"):
        shutil.copy2(ROOT / "static" / f, cible / f)
    shutil.copytree(ROOT / "static" / "data", cible / "data", dirs_exist_ok=True)
    (public / "manifest.webmanifest").write_text(json.dumps(MANIFESTE, ensure_ascii=False, indent=2), encoding="utf-8")
    fichiers = sorted(p for p in public.rglob("*") if p.is_file() and p.name != "sw.js")
    empreinte = hashlib.sha256()
    for f in fichiers:
        empreinte.update(f.relative_to(public).as_posix().encode())
        empreinte.update(f.read_bytes())
    # Les fichiers par pays (≈ 10 Mo) ne sont pas préchargés : ils entrent dans le cache à la première consultation.
    def precharge(f):
        r = f.relative_to(public).as_posix()
        return f.name != "index.html" and not (r.startswith("atlas/data/") and r not in ("atlas/data/index.json", "atlas/data/CMR.json"))
    precache = ["./", "./en/"] + [f.relative_to(public).as_posix() for f in fichiers if precharge(f)]
    sw = (ROOT / "sw.template.js").read_text(encoding="utf-8")
    sw = sw.replace("{{VERSION}}", empreinte.hexdigest()[:12]).replace("{{PRECACHE}}", json.dumps(precache))
    (public / "sw.js").write_text(sw, encoding="utf-8")
    return len(precache)


ATLAS = re.compile(r"<!--ATLAS-->.*?<!--/ATLAS-->\n?", re.S)


def atlas(html, racine):
    """Avec `racine` (site statique) : garde la carte et les pays, chemins relatifs. Sans (Artifact, un seul
    fichier, aucune ressource externe possible) : retire toute la section."""
    if racine is None:
        return ATLAS.sub("", html)
    return html.replace("<!--ATLAS-->", "").replace("<!--/ATLAS-->", "").replace("{{ROOT}}", racine)


def page(template, switch_href, switch_lang, switch_label):
    lien = f'<a class="langue" href="{switch_href}" hreflang="{switch_lang}" lang="{switch_lang}">{switch_label}</a>'
    return template.replace("{{LANG_SWITCH}}", lien)


def main():
    horizontal = (LOGO / "tasetygrid-logo-horizontal.svg").read_text(encoding="utf-8")
    symbole = (LOGO / "tasetygrid-symbole.svg").read_text(encoding="utf-8")
    favicon = (LOGO / "tasetygrid-favicon.svg").read_text(encoding="utf-8")
    hero = themable(inner(symbole), "clipHero")
    hero = hero.replace('stroke-linecap="round"', 'stroke-linecap="round" pathLength="1" class="kodya"', 1)

    t = (ROOT / "template.html").read_text(encoding="utf-8")
    t = t.replace("{{LOGO_HEADER}}", themable(inner(horizontal), "clipHead"))
    t = t.replace("{{LOGO_FOOTER}}", themable(inner(horizontal), "clipFoot"))
    t = t.replace("{{SYMBOLE_HERO}}", hero)
    t = t.replace("{{FAVICON}}", "data:image/svg+xml," + quote(favicon))
    t_en = traduire(t)

    sorties = {
        # Artifact : liens relatifs entre les deux fichiers publiés
        ROOT / "index.html": atlas(page(t, "en/index.html", "en", "EN"), None),
        ROOT / "en" / "index.html": document(atlas(page(t_en, "../", "fr", "FR"), None), "en", "../", "fr"),
        # Site statique + PWA (liens relatifs)
        ROOT / "public" / "index.html": document(atlas(page(t, "en/", "en", "EN"), ""), "fr", "en/", "en", racine=""),
        ROOT / "public" / "en" / "index.html": document(atlas(page(t_en, "../", "fr", "FR"), "../"), "en", "../", "fr", racine="../"),
    }
    for chemin, html in sorties.items():
        chemin.parent.mkdir(parents=True, exist_ok=True)
        chemin.write_text(html, encoding="utf-8")
        print("écrit", chemin.relative_to(ROOT.parent), f"({len(html) // 1024} Ko)")
    n = ecrire_pwa(ROOT / "public")
    print(f"écrit site/public/manifest.webmanifest, icons/, sw.js ({n} ressources mises en cache)")


if __name__ == "__main__":
    main()
