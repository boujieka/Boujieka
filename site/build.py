"""Construit les pages de la landing page TasetyGrid.

Sorties :
- site/index.html et site/en/index.html : publication en Artifact (la page
  française sans squelette, l'artifact l'ajoute ; la page anglaise complète) ;
- site/public/ : site statique complet (FR à la racine, EN sous /en/), à déployer
  tel quel sur Netlify ou tout hébergeur statique.

Usage : python3 site/build.py
"""
import re
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
LOGO = ROOT.parent / "brand" / "logo"
sys.path.insert(0, str(ROOT))
from i18n_en import EN  # noqa: E402

# Indices de français restant dans la page anglaise (hors noms propres et sigles)
FRANCAIS = re.compile(r"[éèêàùçôîœ]|\b(le|la|les|des|du|une|est|et|pour|avec|sans|dans)\b", re.I)
AUTORISE = ("Ta-Sety", "MINDCAF", "ARDFC", "AJPTER", "RGPH", "RGAE", "Kodya", "KODYA", "kodya", "tꜣ-stj")


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


def document(contenu, lang, alt_href, alt_lang):
    """Document HTML complet (doctype, lang, liens hreflang)."""
    i = contenu.index("<header")
    tete, corps = contenu[:i], contenu[i:]
    return ("<!doctype html>\n"
            f'<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            f'<link rel="alternate" hreflang="{alt_lang}" href="{alt_href}">\n'
            + tete + "</head>\n<body>\n" + corps + "\n</body>\n</html>\n")


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
        ROOT / "index.html": page(t, "en/index.html", "en", "EN"),
        ROOT / "en" / "index.html": document(page(t_en, "../", "fr", "FR"), "en", "../", "fr"),
        # Site statique
        ROOT / "public" / "index.html": document(page(t, "/en/", "en", "EN"), "fr", "/en/", "en"),
        ROOT / "public" / "en" / "index.html": document(page(t_en, "/", "fr", "FR"), "en", "/", "fr"),
    }
    for chemin, html in sorties.items():
        chemin.parent.mkdir(parents=True, exist_ok=True)
        chemin.write_text(html, encoding="utf-8")
        print("écrit", chemin.relative_to(ROOT.parent), f"({len(html) // 1024} Ko)")


if __name__ == "__main__":
    main()
