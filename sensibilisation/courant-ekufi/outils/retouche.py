"""Outils de retouche des planches « Courant Ekufi ! » : aplat de couleur + texte réécrit."""
import sys
from PIL import Image, ImageDraw, ImageFont

D = sys.argv[1] if len(sys.argv) > 1 else '.'
F = {
    'comic': D + '/Comic_Neue_wght_700.ttf',
    'bold': D + '/Open_Sans_wght_700.ttf',
    'reg': D + '/Open_Sans_wght_400.ttf',
    'cond': D + '/Roboto_Condensed_wght_700.ttf',
}
NAVY, RED, GREEN, BLACK, WHITE = (24, 42, 92), (214, 40, 40), (30, 110, 60), (25, 25, 25), (255, 255, 255)


def sample(im, xy):
    px = [im.getpixel((xy[0] + dx, xy[1] + dy)) for dx in (-2, 0, 2) for dy in (-2, 0, 2)]
    return tuple(sorted(c[i] for c in px)[4] for i in range(3))


def patch(im, box, lines, fill=None, at=None, align='center', valign='center', radius=0, pad=4, gap=2):
    """Couvre box d'un aplat puis écrit lines = [(texte, police, taille, couleur), ...] en réduisant si besoin."""
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = box
    col = fill if fill else sample(im, at or (x0 + 3, y0 + 3))
    d.rounded_rectangle(box, radius=radius, fill=col) if radius else d.rectangle(box, fill=col)
    scale = 1.0
    while True:
        fonts = [ImageFont.truetype(F[f], max(8, int(s * scale))) for _, f, s, _ in lines]
        sizes = [d.textbbox((0, 0), t, font=fo) for (t, *_), fo in zip(lines, fonts)]
        w = max(b[2] - b[0] for b in sizes)
        h = sum(b[3] - b[1] for b in sizes) + gap * (len(lines) - 1)
        if (w <= x1 - x0 - 2 * pad and h <= y1 - y0 - 2 * pad) or scale < .5:
            break
        scale -= .04
    y = y0 + pad if valign == 'top' else y0 + (y1 - y0 - h) / 2
    for (t, _, _, c), fo, b in zip(lines, fonts, sizes):
        lw = b[2] - b[0]
        x = x0 + pad if align == 'left' else x0 + (x1 - x0 - lw) / 2
        d.text((x - b[0], y - b[1]), t, font=fo, fill=c)
        y += b[3] - b[1] + gap


