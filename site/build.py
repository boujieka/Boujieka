"""Construit site/index.html à partir de site/template.html et des SVG de la marque.

Usage : python3 site/build.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOGO = ROOT.parent / "brand" / "logo"


def inner(svg_text):
    """Contenu d'un SVG sans la balise racine ni le <title>."""
    body = re.sub(r"^.*?<svg[^>]*>", "", svg_text, count=1, flags=re.S)
    body = re.sub(r"</svg>\s*$", "", body)
    return re.sub(r"<title>.*?</title>", "", body, flags=re.S).strip()


def themable(svg_body, prefix):
    """Remplace les couleurs de la marque par des variables CSS (thème clair/sombre)
    et rend les identifiants de découpe uniques dans la page."""
    for hexa, var in (("#1D3F8F", "--logo-bleu"), ("#C9982E", "--logo-or"), ("#A6412B", "--logo-ocre")):
        svg_body = svg_body.replace(f'fill="{hexa}"', f'style="fill:var({var})"')
        svg_body = svg_body.replace(f'stroke="{hexa}"', f'style="stroke:var({var})"')
    return re.sub(r'clip(\d+)', lambda m: f"{prefix}{m.group(1)}", svg_body)


def main():
    horizontal = (LOGO / "tasetygrid-logo-horizontal.svg").read_text(encoding="utf-8")
    symbole = (LOGO / "tasetygrid-symbole.svg").read_text(encoding="utf-8")
    favicon = (LOGO / "tasetygrid-favicon.svg").read_text(encoding="utf-8")

    hero = themable(inner(symbole), "clipHero")
    # La spirale (le seul tracé or, arrondi) se dessine au chargement
    hero = hero.replace('stroke-linecap="round"', 'stroke-linecap="round" pathLength="1" class="kodya"', 1)

    html = (ROOT / "template.html").read_text(encoding="utf-8")
    html = html.replace("{{LOGO_HEADER}}", themable(inner(horizontal), "clipHead"))
    html = html.replace("{{LOGO_FOOTER}}", themable(inner(horizontal), "clipFoot"))
    html = html.replace("{{SYMBOLE_HERO}}", hero)
    from urllib.parse import quote
    html = html.replace("{{FAVICON}}", "data:image/svg+xml," + quote(favicon))
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print("écrit", ROOT / "index.html", f"({len(html) // 1024} Ko)")


if __name__ == "__main__":
    main()
