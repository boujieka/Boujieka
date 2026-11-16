"""Complète la planche 33 (version dessinée) :
- emplacements photo 33.3 et 33.4 remplis avec l'image de la stèle de la variante B (provisoire) ;
- bulles 33.5 (complétée) et 33.7 (réplique vérifiée).
usage: python3 complete_planche.py planche.png varianteB.png out.png"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

src, srcB, out = sys.argv[1:4]
im = Image.open(src).convert('RGB')
B = Image.open(srcB).convert('RGB')
FD = 'fonts/fontsource-comic-neue-5.3.0/package/files/'
BOLD = 'fonts/kalam/package/files/kalam-latin-700-normal.woff'
ITAL = FD + 'comic-neue-latin-700-italic.woff'
INK = (28, 24, 22)


def region_mask(seed, box, test):
    """Zone connexe depuis seed (pixels qui vérifient test), comblée ligne à ligne."""
    x0, y0, x1, y1 = box
    a = np.asarray(im.crop(box))
    ok = test(a).astype(np.uint8) * 255
    b = Image.fromarray(ok).copy()
    sx, sy = seed[0] - x0, seed[1] - y0
    assert ok[sy, sx] == 255, ('graine hors zone', seed)
    from PIL import ImageDraw as D
    D.floodfill(b, (sx, sy), 128)
    reg = np.asarray(b) == 128
    m = np.zeros_like(reg)
    for y in range(reg.shape[0]):
        xs = np.where(reg[y])[0]
        if len(xs):
            m[y, xs.min():xs.max() + 1] = True
    return m


def placeholder_test(a):
    r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    grey = (abs(r - g) < 10) & (abs(g - b) < 10)
    return grey & (r > 120)  # gris clair + texte gris du gabarit


def paste_photo(seed, box, picture, mode='cover', label=None, label_size=13, rect=None, bgpic=None):
    x0, y0, x1, y1 = box
    if rect:
        m = np.zeros((y1 - y0, x1 - x0), bool); m[rect[1] - y0:rect[3] - y0, rect[0] - x0:rect[2] - x0] = True
    else:
        m = region_mask(seed, box, placeholder_test)
    mi = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3))
    ys, xs = np.where(m)
    bx0, by0, bx1, by1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    w, h = bx1 - bx0, by1 - by0
    canvas = Image.new('RGB', (x1 - x0, y1 - y0))
    if mode == 'cover':
        s = max(w / picture.width, h / picture.height)
        p = picture.resize((int(picture.width * s) + 1, int(picture.height * s) + 1), Image.LANCZOS)
        ox, oy = (p.width - w) // 2, (p.height - h) // 2
        canvas.paste(p.crop((ox, oy, ox + w, oy + h)), (bx0, by0))
    else:  # contain sur fond flouté
        s = max(w / picture.width, h / picture.height)
        src_bg = bgpic or picture
        s = max(w / src_bg.width, h / src_bg.height)
        bg = src_bg.resize((int(src_bg.width * s) + 1, int(src_bg.height * s) + 1)).filter(ImageFilter.GaussianBlur(6))
        ox, oy = (bg.width - w) // 2, (bg.height - h) // 2
        canvas.paste(bg.crop((ox, oy, ox + w, oy + h)), (bx0, by0))
        s2 = min(w / picture.width, h / picture.height)
        fg = picture.resize((int(picture.width * s2), int(picture.height * s2)), Image.LANCZOS)
        canvas.paste(fg, (bx0 + (w - fg.width) // 2, by0 + (h - fg.height) // 2))
    if label:
        d = ImageDraw.Draw(canvas)
        f = ImageFont.truetype(ITAL, label_size)
        tw = d.textlength(label, font=f)
        tx, ty = bx0 + 6, by0 + 4
        d.rectangle((tx - 3, ty - 1, tx + tw + 3, ty + label_size + 4), fill=(255, 248, 225))
        d.text((tx, ty), label, font=f, fill=(120, 30, 20))
    reg = im.crop(box)
    reg.paste(canvas, (0, 0), mi)
    im.paste(reg, (x0, y0))


# --- 33.3 : écran de l'ordinateur ---------------------------------------------
vitrine = B.crop((470, 262, 890, 750))          # vitrine et stèle de la variante B
salle = B.crop((10, 262, 1440, 750))
paste_photo(seed=None, box=(150, 405, 1300, 640), picture=vitrine, mode='contain', rect=(236, 438, 1224, 621), bgpic=salle,
            label='Image provisoire — à remplacer par la photo du Met 50.85 (domaine public)', label_size=12)

# --- 33.4 : détail des mains -------------------------------------------------
mains = B.crop((12, 860, 355, 985))
paste_photo(seed=(60, 990), box=(5, 880, 345, 1050), picture=mains, mode='cover',
            label='Image provisoire', label_size=11)


# --- bulles ------------------------------------------------------------------
def bubble_test(a):
    return np.asarray(Image.fromarray(a).convert('L')) > 185


def wrap(d, text, font, maxw):
    out, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            out.append(cur); cur = w
    out.append(cur)
    return out


def fill_bubble(seed, box, blocks, size, widthf=0.86):
    x0, y0, x1, y1 = box
    m = region_mask(seed, box, bubble_test)
    mask = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(5))
    reg = im.crop(box)
    reg.paste(Image.new('RGB', reg.size, (255, 255, 255)), (0, 0), mask)
    mm = np.asarray(mask) > 0
    ys = np.where(mm.any(axis=1))[0]
    top, bot = ys.min(), ys.max()
    d = ImageDraw.Draw(reg)
    while True:
        lines = []
        for txt, fp in blocks:
            f = ImageFont.truetype(fp, size)
            mid = (top + bot) // 2
            xs = np.where(mm[mid])[0]
            for ln in wrap(d, txt, f, (xs.max() - xs.min()) * widthf):
                lines.append((ln, f))
        lh = int(size * 1.0)
        if lh * len(lines) <= (bot - top) * 0.86 or size <= 12:
            break
        size -= 1
    y = (top + bot) // 2 - lh * len(lines) // 2
    for ln, f in lines:
        row = min(max(y + lh // 2, top), bot)
        xs = np.where(mm[row])[0]
        cx = (xs.min() + xs.max()) / 2
        d.text((cx - d.textlength(ln, font=f) / 2, y), ln, font=f, fill=INK)
        y += lh
    im.paste(reg, (x0, y0))
    return size


s5 = fill_bubble((560, 880), (515, 722, 745, 925), [
    ('Elle a été commandée par un prêtre, Esatum. Elle venait sans doute d’Héliopolis, du temple des taureaux Mnévis. On l’a retrouvée à Alexandrie.', BOLD)], 25)
s7 = fill_bubble((1270, 830), (1250, 752, 1446, 962), [
    ('INÈS (off) :', BOLD),
    ('Non. C’est le nom d’un ancien propriétaire. Les objets portent parfois le nom de ceux qui les ont possédés.', BOLD)], 25)
im.save(out)
print('ok', s5, s7)
