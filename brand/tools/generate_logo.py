"""Génère les fichiers SVG de la marque TasetyGrid.

Le symbole « Kodya » : une spirale de coquille d'escargot tracée sur une grille de
carrés de Fibonacci (la grille qui grandit comme une coquille), inscrite dans le
cercle du cosmogramme kongo, avec ses quatre points cardinaux.

Le texte est vectorisé (converti en tracés) : les SVG produits ne dépendent
d'aucune police installée.

Usage :
    python3 generate_logo.py --cinzel Cinzel-SemiBold.ttf --inter Inter-SemiBold.ttf --out ../logo
Polices (licence SIL OFL) : Cinzel et Inter, disponibles sur Google Fonts.
"""
import argparse
import math
import zlib
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

PALETTE = {
    "bleu_egyptien": "#1D3F8F",   # pigment bleu égyptien / lapis-lazuli
    "or_nubie": "#C9982E",        # or de Nubie
    "ocre_kerma": "#A6412B",      # céramique rouge de Kerma
    "noir_kemet": "#17130F",      # limon noir du Nil (kmt)
    "blanc_mpemba": "#F6F0E4",    # kaolin blanc kongo (mpemba)
    "turquoise_faience": "#2E8C83",
}

FIB_SPIRALE = 8    # carrés 1..21 portent la spirale
FIB_GRILLE = 11    # carrés 1..89 forment la grille, découpée par le cercle


def fib(n):
    a, b, out = 1, 1, []
    for _ in range(n):
        out.append(a)
        a, b = b, a + b
    return out


def fibonacci_squares(n=FIB_SPIRALE):
    """Carrés (x, y, s) et arcs (début, fin, centre) en coordonnées écran (y vers le bas)."""
    squares, arcs = [(0, 0, 1)], [((0, 0), (1, 1), (1, 0))]
    x0, y0, x1, y1 = 0, 0, 1, 1
    for i, s in enumerate(fib(n)[1:]):
        d = i % 4  # droite, haut, gauche, bas
        if d == 0:
            x, y = x1, y0
            arc = ((x, y + s), (x + s, y), (x, y))
        elif d == 1:
            x, y = x0, y0 - s
            arc = ((x + s, y + s), (x, y), (x, y + s))
        elif d == 2:
            x, y = x0 - s, y0
            arc = ((x + s, y), (x, y + s), (x + s, y + s))
        else:
            x, y = x0, y1
            arc = ((x, y), (x + s, y + s), (x + s, y))
        squares.append((x, y, s))
        arcs.append(arc)
        x0, y0, x1, y1 = min(x0, x), min(y0, y), max(x1, x + s), max(y1, y + s)
    return squares, arcs, (x0, y0, x1, y1)


def pole(n=12):
    """Pôle (œil) de la spirale : intersection des diagonales de deux rectangles successifs."""
    _, _, b1 = fibonacci_squares(n)
    _, _, b0 = fibonacci_squares(n - 1)

    def inter(p1, p2, p3, p4):
        d = (p1[0]-p2[0])*(p3[1]-p4[1]) - (p1[1]-p2[1])*(p3[0]-p4[0])
        if abs(d) < 1e-9:
            return None
        t = ((p1[0]-p3[0])*(p3[1]-p4[1]) - (p1[1]-p3[1])*(p3[0]-p4[0])) / d
        return (p1[0] + t*(p2[0]-p1[0]), p1[1] + t*(p2[1]-p1[1]))

    best = None
    for da in (((b1[0], b1[1]), (b1[2], b1[3])), ((b1[2], b1[1]), (b1[0], b1[3]))):
        for db in (((b0[0], b0[1]), (b0[2], b0[3])), ((b0[2], b0[1]), (b0[0], b0[3]))):
            pt = inter(*da, *db)
            if pt and b0[0] <= pt[0] <= b0[2] and b0[1] <= pt[1] <= b0[3]:
                # garder l'intersection la plus proche des petits carrés
                if best is None or math.hypot(*pt) < math.hypot(*best):
                    best = pt
    return best


def sweep(p, q, c):
    a1 = math.atan2(p[1] - c[1], p[0] - c[0])
    a2 = math.atan2(q[1] - c[1], q[0] - c[0])
    return 1 if (a2 - a1) % (2 * math.pi) < math.pi else 0


def mark(size=512, ring=None, grid=None, spiral=None, dots=None, bg=None,
         min_square=1, grid_opacity=0.55, simple=False):
    """Retourne le contenu SVG (sans balise <svg>) du symbole centré dans un carré `size`."""
    ring = ring or PALETTE["ocre_kerma"]
    grid = grid or PALETTE["bleu_egyptien"]
    spiral = spiral or PALETTE["or_nubie"]
    dots = dots or ring
    squares, arcs, _ = fibonacci_squares(FIB_SPIRALE)
    grid_squares, _, _ = fibonacci_squares(FIB_GRILLE)
    # Le cercle est le prolongement du dernier tour de la coquille :
    # il a le même centre et le même rayon que le dernier arc de la spirale.
    (px, py), r_last = arcs[-1][2], squares[-1][2]
    R = size * 0.44                       # rayon du cercle
    cx = cy = size / 2
    k = R / r_last

    def tr(p):
        return (cx + (p[0] - px) * k, cy + (p[1] - py) * k)

    sw_grid, sw_spiral, sw_ring = size * 0.010, size * 0.040, size * 0.040
    if simple:  # petites tailles : ni grille ni points, traits épaissis
        sw_spiral = sw_ring = size * 0.085
        R = size * 0.40
        k = R / r_last
    out = []
    if bg:
        out.append(f'<rect width="{size}" height="{size}" rx="{size*0.18:.1f}" fill="{bg}"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{R:.2f}" fill="none" stroke="{ring}" stroke-width="{sw_ring:.2f}"/>')
    g = []
    for (x, y, s) in ([] if simple else grid_squares):
        if s < min_square:
            continue
        (ax, ay), (bx, by) = tr((x, y)), tr((x + s, y + s))
        g.append(f'<rect x="{ax:.2f}" y="{ay:.2f}" width="{bx-ax:.2f}" height="{by-ay:.2f}"/>')
    clip = f"clip{zlib.crc32(repr((ring, grid, spiral, bg, min_square)).encode()) % 10**6}"
    out.append(f'<clipPath id="{clip}"><circle cx="{cx}" cy="{cy}" r="{R - sw_ring/2:.2f}"/></clipPath>')
    out.append(f'<g clip-path="url(#{clip})" fill="none" stroke="{grid}" stroke-width="{sw_grid:.2f}" opacity="{grid_opacity}">{"".join(g)}</g>')
    d, started = [], False
    for (p, q, c), (_, _, s) in zip(arcs, squares):
        if s < min_square:
            continue
        P, Q = tr(p), tr(q)
        r = s * k
        if not started:
            d.append(f"M{P[0]:.2f},{P[1]:.2f}")
            started = True
        d.append(f"A{r:.2f},{r:.2f} 0 0 {sweep(p, q, c)} {Q[0]:.2f},{Q[1]:.2f}")
    out.append(f'<path d="{" ".join(d)}" fill="none" stroke="{spiral}" stroke-width="{sw_spiral:.2f}" stroke-linecap="round"/>')
    # quatre moments du soleil (dikenga), par-dessus la coquille
    for ang in (() if simple else (0, 90, 180, 270)):
        a = math.radians(ang)
        out.append(f'<circle cx="{cx + R*math.cos(a):.2f}" cy="{cy + R*math.sin(a):.2f}" r="{size*0.036:.2f}" fill="{dots}"/>')
    # cœur de la coquille : la vie (zinga) qui commence
    sx, sy = tr(arcs[fib(FIB_SPIRALE).index(min_square)][0])
    if not simple:
        out.append(f'<circle cx="{sx:.2f}" cy="{sy:.2f}" r="{size*0.024:.2f}" fill="{spiral}"/>')
    return "\n".join(out)


def text_path(font_path, text, height, tracking=0.0):
    """Texte vectorisé : (chemin SVG, largeur) pour une hauteur de capitale `height`."""
    font = TTFont(font_path)
    gs, cmap = font.getGlyphSet(), font.getBestCmap()
    cap = font["OS/2"].sCapHeight or font["head"].unitsPerEm * 0.7
    scale = height / cap
    pen, x = SVGPathPen(gs), 0.0
    hmtx = font["hmtx"]
    for i, ch in enumerate(text):
        name = cmap[ord(ch)]
        gs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x, height)))
        x += hmtx[name][0] * scale
        if i < len(text) - 1:
            x += tracking * height
    return pen.getCommands(), x


def svg(width, height, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} {height:.0f}" '
            f'width="{width:.0f}" height="{height:.0f}" role="img" aria-label="{title}">\n'
            f'<title>{title}</title>\n{body}\n</svg>\n')


def wordmark(cinzel, inter, cap, c1, c2):
    p1, w1 = text_path(cinzel, "TASETY", cap, tracking=0.08)
    p2, w2 = text_path(inter, "GRID", cap, tracking=0.14)
    gap = cap * 0.22
    body = (f'<path d="{p1}" fill="{c1}"/>'
            f'<g transform="translate({w1 + gap:.2f},0)"><path d="{p2}" fill="{c2}"/></g>')
    return body, w1 + gap + w2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cinzel", required=True)
    ap.add_argument("--inter", required=True)
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent.parent / "logo"))
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    P = PALETTE

    files = {
        "tasetygrid-symbole.svg": svg(512, 512, mark(), "TasetyGrid — symbole"),
        "tasetygrid-symbole-inverse.svg": svg(512, 512, mark(
            bg=P["noir_kemet"], grid=P["blanc_mpemba"], grid_opacity=0.35), "TasetyGrid — symbole sur fond sombre"),
        "tasetygrid-symbole-mono.svg": svg(512, 512, mark(
            ring=P["noir_kemet"], grid=P["noir_kemet"], spiral=P["noir_kemet"], grid_opacity=0.45), "TasetyGrid — symbole monochrome"),
        "tasetygrid-icone.svg": svg(512, 512, mark(
            bg=P["bleu_egyptien"], ring=P["or_nubie"], grid=P["blanc_mpemba"], spiral=P["or_nubie"],
            dots=P["ocre_kerma"], min_square=2, grid_opacity=0.30), "TasetyGrid — icône d'application"),
        "tasetygrid-favicon.svg": svg(512, 512, mark(
            bg=P["bleu_egyptien"], ring=P["ocre_kerma"], spiral=P["or_nubie"], min_square=3, simple=True),
            "TasetyGrid — favicon"),
    }

    # Logo horizontal
    S, cap = 512, 150
    wm, wmw = wordmark(a.cinzel, a.inter, cap, P["bleu_egyptien"], P["or_nubie"])
    W = S + 60 + wmw + 40
    files["tasetygrid-logo-horizontal.svg"] = svg(W, S, mark() +
        f'\n<g transform="translate({S + 60:.1f},{(S - cap) / 2:.1f})">{wm}</g>', "TasetyGrid")
    wm_i, _ = wordmark(a.cinzel, a.inter, cap, P["blanc_mpemba"], P["or_nubie"])
    files["tasetygrid-logo-horizontal-inverse.svg"] = svg(W, S,
        f'<rect width="{W:.0f}" height="{S}" fill="{P["noir_kemet"]}"/>' +
        mark(grid=P["blanc_mpemba"], grid_opacity=0.35) +
        f'\n<g transform="translate({S + 60:.1f},{(S - cap) / 2:.1f})">{wm_i}</g>', "TasetyGrid")

    # Logo vertical avec signature
    cap2 = 96
    wm2, wmw2 = wordmark(a.cinzel, a.inter, cap2, P["bleu_egyptien"], P["or_nubie"])
    tag, tagw = text_path(a.inter, "ATLAS DES PERSONNES, DES TERRES ET DES RESSOURCES", 22, tracking=0.35)
    W2 = max(wmw2, tagw, S) + 80
    H2 = S + 40 + cap2 + 50 + 22 + 40
    body = (f'<g transform="translate({(W2 - S) / 2:.1f},0)">{mark()}</g>'
            f'<g transform="translate({(W2 - wmw2) / 2:.1f},{S + 40})">{wm2}</g>'
            f'<g transform="translate({(W2 - tagw) / 2:.1f},{S + 40 + cap2 + 50})"><path d="{tag}" fill="{P["ocre_kerma"]}"/></g>')
    files["tasetygrid-logo-vertical.svg"] = svg(W2, H2, body, "TasetyGrid — Atlas des personnes, des terres et des ressources")

    for name, content in files.items():
        (out / name).write_text(content, encoding="utf-8")
        print("écrit", out / name)


if __name__ == "__main__":
    main()
