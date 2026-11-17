"""Reconstruit le bandeau des planches (sans tiret cadratin, coquilles corrigées).
usage: python3 headers.py src_dir out_dir plates.json [n ...]"""
import sys, json, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont

src, out, pj = sys.argv[1:4]
only = set(int(x) for x in sys.argv[4:])
FB = '../fonts/oswald/package/files/oswald-latin-700-normal.woff'
FM = '../fonts/oswald/package/files/oswald-latin-600-normal.woff'
NAVY, RED, DARK, BADGE = (22, 52, 118), (112, 28, 22), (45, 32, 20), (249, 214, 112)

ROMAN = {'I': 'I', 'II': 'II', 'III': 'III'}


def part_lines(part):
    p = part.replace('’', "'")
    m = re.match(r"(Prologue|Épilogue|Chapitre \d+) — (.*)", part)
    head, title = m.group(1), m.group(2)
    return [head.upper(), title.upper()]


def plate_lines(n, title):
    t = title.replace(' [N2]', '')
    m = re.match(r"Seuil ([IV]+) « (.*) »", t)
    if m:
        t = f"SEUIL {m.group(1)} : {m.group(2)}"
    return [f'PLANCHE {n}', t.upper()]


def fit(draw, lines, box, font_path, max_size, line_gap=1.16):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    size = max_size
    while size > 8:
        f = ImageFont.truetype(font_path, size)
        # retour à la ligne si nécessaire
        wrapped = []
        for ln in lines:
            words, cur = ln.split(), ''
            for wd in words:
                t = (cur + ' ' + wd).strip()
                if draw.textlength(t, font=f) <= w:
                    cur = t
                else:
                    wrapped.append(cur); cur = wd
            wrapped.append(cur)
        lh = size * line_gap
        if lh * len(wrapped) <= h and all(draw.textlength(l, font=f) <= w for l in wrapped):
            return f, wrapped, lh
        size -= 1
    return f, wrapped, lh


def draw_block(draw, lines, box, font_path, color, max_size):
    f, wrapped, lh = fit(draw, lines, box, font_path, max_size)
    x0, y0, x1, y1 = box
    total = lh * len(wrapped)
    y = y0 + (y1 - y0 - total) / 2
    for ln in wrapped:
        l, t, r, b = draw.textbbox((0, 0), ln, font=f)
        draw.text(((x0 + x1) / 2 - (r - l) / 2 - l, y - t + (lh - (b - t)) / 2), ln, font=f, fill=color)
        y += lh


def header_bottom(a, W):
    white = (a.min(2) > 225)
    fr = white[:, int(W * 0.05):int(W * 0.95)].mean(1)
    for y in range(40, 220):
        if all(fr[y + k] < 0.35 for k in range(12)):
            return y
    raise RuntimeError('bordure introuvable')


def logo_sep(a, hb):
    top = a[6:hb - 8]
    nw = (np.abs(top - 255).sum(2) > 120).mean(0)
    for x in range(270, 500):
        if nw[x] > 0.55:
            w = 0
            while nw[x + w] > 0.55:
                w += 1
            if w <= 7:
                return x
    raise RuntimeError('séparateur du logo introuvable')


plates = json.load(open(pj))
for p in plates:
    n = p['n']
    if only and n not in only:
        continue
    im = Image.open(f"{src}/p{n:02d}.png").convert('RGB')
    a = np.asarray(im).astype(int)
    W, H = im.size
    hb = header_bottom(a, W)
    ls = logo_sep(a, hb)
    d = ImageDraw.Draw(im)
    top, bot = 2, hb - 6
    d.rectangle((ls + 6, 0, W - 1, bot), fill=(255, 255, 255))
    # trois cases
    x = ls + 18
    avail = W - 8 - x
    w1, w2 = int(avail * 0.30), int(avail * 0.31)
    pad = 6
    c1 = (x, top + pad, x + w1, bot - pad)
    s1 = x + w1 + 9
    c2 = (s1 + 10, top + pad, s1 + 10 + w2, bot - pad)
    s2 = c2[2] + 9
    c3 = (s2 + 12, top + 4, W - 8, bot - 3)
    for sx, col in ((s1, RED), (s2, RED)):
        d.line((sx, top + 8, sx, bot - 8), fill=col, width=3)
    hsize = int((bot - top) * 0.34)
    draw_block(d, ["LES MILLE VISAGES", "DE L'ÉGYPTE ANCIENNE"], c1, FB, NAVY, hsize)
    draw_block(d, part_lines(p['part']), c2, FB, RED, hsize)
    d.rounded_rectangle(c3, radius=int((c3[3] - c3[1]) * 0.18), fill=BADGE)
    inner = (c3[0] + 10, c3[1] + 4, c3[2] - 10, c3[3] - 4)
    draw_block(d, plate_lines(n, p['title']), inner, FB, DARK, hsize)
    im.save(f"{out}/p{n:02d}.png")
    print(n, 'hb', hb, 'logo', ls)
