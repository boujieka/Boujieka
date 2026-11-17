"""Remplace le logo du bandeau et la signature « Emma B. » par les fichiers officiels.
usage: python3 logos.py in_dir out_dir logo.jpg signature.jpg cover_in cover_out"""
import sys
import numpy as np
from PIL import Image, ImageFilter

ind, outd, LOGO, SIG, cov_in, cov_out = sys.argv[1:7]
src_h = open('headers.py').read()
ns = {}
exec('import numpy as np\n' + 'def header_bottom' + src_h.split('def header_bottom')[1].split('plates = json.load')[0], ns)
header_bottom, logo_sep = ns['header_bottom'], ns['logo_sep']


def alpha_from_white(im, lo=18, hi=60):
    a = np.asarray(im.convert('RGB')).astype(float)
    d = 255 - a.min(2)
    al = np.clip((d - lo) / (hi - lo), 0, 1) * 255
    rgba = np.dstack([a, al]).astype(np.uint8)
    return Image.fromarray(rgba, 'RGBA')


def trim(im):
    a = np.asarray(im.convert('RGB')).astype(int)
    ys, xs = np.where(a.min(2) < 235)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


logo = Image.open(LOGO).convert('RGB')
# emblème (carte) et nom (deux lignes) extraits du logo officiel
emblem = trim(logo.crop((330, 60, 1400, 905)))
word = trim(logo.crop((90, 905, 1450, 1250)))
sig = alpha_from_white(trim(Image.open(SIG).convert('RGB')))


def header_logo(h, w):
    """Logo horizontal : emblème à gauche, nom à droite, fond blanc."""
    eh = h
    e = emblem.resize((int(emblem.width * eh / emblem.height), eh), Image.LANCZOS)
    ww = w - e.width - 6
    wd = word.resize((ww, int(word.height * ww / word.width)), Image.LANCZOS)
    if wd.height > h * 0.82:
        wh = int(h * 0.82)
        wd = word.resize((int(word.width * wh / word.height), wh), Image.LANCZOS)
    canvas = Image.new('RGB', (w, h), 'white')
    total = e.width + 6 + wd.width
    x = (w - total) // 2
    canvas.paste(e, (x, 0))
    canvas.paste(wd, (x + e.width + 6, (h - wd.height) // 2))
    return canvas


# gabarit de l'ancienne signature (planche 1, sur fond blanc)
p1 = np.asarray(Image.open(f'{ind}/p01.png').convert('L')).astype(float)
H1, W1 = p1.shape
reg = p1[H1 - 80:H1, W1 - 300:W1]
ys, xs = np.where(reg < 90)
TPL = reg[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def ncc_best(region, tpl_base):
    best = (-1, None)
    for s in np.arange(0.75, 1.75, 0.05):
        th, tw = int(tpl_base.shape[0] * s), int(tpl_base.shape[1] * s)
        if th >= region.shape[0] or tw >= region.shape[1]:
            continue
        t = np.asarray(Image.fromarray(tpl_base.astype(np.uint8)).resize((tw, th))).astype(float)
        t = t - t.mean(); tn = np.sqrt((t ** 2).sum())
        R = region
        # corrélation par fenêtres (pas de 2 px)
        for y in range(0, R.shape[0] - th, 2):
            for x in range(0, R.shape[1] - tw, 2):
                w = R[y:y + th, x:x + tw]
                wm = w - w.mean(); wn = np.sqrt((wm ** 2).sum())
                if wn == 0:
                    continue
                v = (wm * t).sum() / (wn * tn)
                if v > best[0]:
                    best = (v, (x, y, tw, th))
    return best


def inpaint(arr, mask, iters=250):
    a = arr.astype(float).copy()
    m = mask.copy()
    ring = ~m
    for c in range(3):
        a[..., c][m] = a[..., c][ring].mean()
    for _ in range(iters):
        b = (np.roll(a, 1, 0) + np.roll(a, -1, 0) + np.roll(a, 1, 1) + np.roll(a, -1, 1)) / 4
        a[m] = b[m]
    return a.astype(np.uint8)


def replace_signature(im, region_box, min_px=60, width=None):
    """Efface l'ancienne signature (encre noire, coin bas droit) et pose la nouvelle."""
    x0, y0, x1, y1 = region_box
    a = np.asarray(im).astype(int)
    sub = a[y0:y1, x0:x1]
    lum = sub.mean(2); sat = sub.max(2) - sub.min(2)
    ink = (lum < 95) & (sat < 60)
    # retirer les longues lignes droites (bordures de case)
    for y in range(ink.shape[0]):
        if ink[y].mean() > 0.5:
            ink[y] = False
    for x in range(ink.shape[1]):
        if ink[:, x].mean() > 0.6:
            ink[:, x] = False
    if ink.sum() < min_px:
        return int(ink.sum()), None
    ys, xs = np.where(ink)
    bx0, by0, bx1, by1 = xs.min(), ys.min(), xs.max(), ys.max()
    m = np.asarray(Image.fromarray((ink * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))) > 0
    pad = 4
    Y0, Y1 = max(0, by0 - pad), min(sub.shape[0], by1 + pad + 1)
    X0, X1 = max(0, bx0 - pad), min(sub.shape[1], bx1 + pad + 1)
    region = sub[Y0:Y1, X0:X1].astype(np.uint8)
    fixed = inpaint(region, m[Y0:Y1, X0:X1])
    out = np.asarray(im).copy()
    out[y0 + Y0:y0 + Y1, x0 + X0:x0 + X1] = fixed
    out = Image.fromarray(out)
    tw = width or 150
    sg = sig.resize((tw, int(sig.height * tw / sig.width)), Image.LANCZOS)
    W, H = out.size
    px = min(W - sg.width - 8, int(x0 + (bx0 + bx1) / 2 - sg.width / 2))
    py = min(H - sg.height - 4, int(y0 + (by0 + by1) / 2 - sg.height / 2))
    out.paste(sg, (px, py), sg)
    return int(ink.sum()), out


import json
plates = json.load(open('plates.json'))
for p in plates:
    n = p['n']
    im = Image.open(f'{ind}/p{n:02d}.png').convert('RGB')
    W, H = im.size
    box = (W - 220, H - 62, W - 3, H - 3) if n == 35 else (W - 165, H - 48, W - 3, H - 3)
    score, new = replace_signature(im, box)
    if new is not None:
        im = new
    a = np.asarray(im).astype(int)
    hb = header_bottom(a, W)
    ls = logo_sep(a, hb)
    h = hb - 12
    im.paste(Image.new('RGB', (ls - 2, hb - 6), 'white'), (0, 0))
    im.paste(header_logo(h, ls - 20), (8, 3))
    im.save(f'{outd}/p{n:02d}.png')
    print(n, 'signature', 'remplacée' if new is not None else 'non trouvée', score)

# couverture
cv = Image.open(cov_in).convert('RGB')
a = np.asarray(cv).copy()
LB = (395, 52, 692, 280)          # ancien logo (sous « IMAGES D'AFRIQUE »)
x0, y0, x1, y1 = LB
sub = a[y0:y1, x0:x1]
m = np.ones(sub.shape[:2], bool); m[:3, :] = m[-3:, :] = False; m[:, :3] = m[:, -3:] = False
a[y0:y1, x0:x1] = inpaint(sub, m, iters=600)
cv = Image.fromarray(a)
L2 = alpha_from_white(trim(logo))
side = y1 - y0
L2 = L2.resize((side, side), Image.LANCZOS)
cv.paste(L2, ((x0 + x1) // 2 - side // 2, y0), L2)
W, H = cv.size
score, new = replace_signature(cv, (W - 200, H - 100, W - 3, H - 3), width=170)
if new is not None:
    cv = new
cv.save(cov_out)
print('couverture : signature', score)
