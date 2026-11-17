"""Corrige les coquilles en re-lettrant la bulle (ou le cartouche) entière.
usage: python3 typos.py in_dir out_dir [probe]"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ind, outd = sys.argv[1:3]
probe = len(sys.argv) > 3
REG = '../fonts/kalam/package/files/kalam-latin-700-normal.woff'
INK = (28, 24, 22)

# (planche, graine (x, y) à l'intérieur de la bulle, boîte englobante maximale, blocs de texte)
# un bloc commençant par '§' est un intitulé (INÈS :, RÉCIT :) écrit sur sa propre ligne
FIX = [
    (27, None, (135, 100, 365, 178), ['§RÉCIT :', 'Qui a fait ce rouleau ? On ne connaît pas leurs noms.']),
    (27, None, (1060, 88, 1425, 245), ['§INÈS (hors champ) :', 'Certains rouleaux étaient peut-être préparés à l’avance, avec une place pour le nom. Pour celui d’Ani, on ne sait pas.']),
    (27, None, (690, 440, 965, 578), ['§INÈS (hors champ) :', 'Osiris, souverain du monde des morts. Celui qu’Isis a pleuré.']),
    (32, None, (85, 110, 322, 302), ['Les Égyptiens imaginaient que le soleil, chaque soir, entrait dans le monde souterrain, la Douat, et le traversait en douze heures avant de renaître au matin.']),
    (32, None, (318, 360, 512, 520), ['§INÈS (off) :', 'C’est ce livre-là que je voulais te montrer sur les murs de la tombe de Thoutmosis III.']),
    (32, None, (1112, 280, 1432, 345), ['Croquis d’Inès : RECONSTITUTION, d’après les livres de l’au-delà (Nouvel Empire)']),
    (36, None, (1200, 360, 1505, 512), ['Ce roi, Akhénaton, donne une place centrale à Aton, le disque du soleil. On le représente souvent ainsi.']),
    (39, None, (432, 112, 628, 322), ['Quelques années plus tard, sous Toutânkhamon, on revient au culte d’Amon et aux anciennes capitales.']),
    (41, None, (655, 930, 835, 1022), ['Bonne question. Je vérifie avant de répondre.']),
    (45, None, (1212, 108, 1442, 332), ['Ça, c’est la question de la fin. Ce qui reste des images quand on ne les prie plus.']),
    (45, None, (1232, 672, 1447, 945), ['Attends… Celle-là : une mère assise qui allaite son bébé… J’ai déjà vu presque la même dans mon livre d’histoire de l’art. Mais c’était Marie, avec Jésus.']),
    (46, None, (788, 88, 1002, 278), ['Les mêmes ? Attention. Ça, c’est une vraie question de spécialistes, et ils ne sont pas d’accord.']),
    (46, None, (1278, 648, 1412, 762), ['Comme on vient de regarder Isis.']),
    (29, None, (95, 92, 352, 262), ['Mais alors… est-ce que ça marchait ? Le cœur, la balance, tout ça. Ani est passé ?']),
    (41, None, (1388, 580, 1534, 775), ['Le musée s’appuie sur des travaux de spécialistes. Leur méthode, je te la mettrai au propre à la fin du livre.']),
    (41, None, (1165, 540, 1385, 676), ['Le musée le date de l’été 50 av. J.-C.']),
]


def auto_seed(a, box):
    """Graine donnant la plus grande zone claire dans la moitié centrale de la boîte."""
    x0, y0, x1, y1 = box
    best, bs = 0, None
    for fy in (0.3, 0.4, 0.5, 0.6, 0.7):
        for fx in (0.3, 0.4, 0.5, 0.6, 0.7):
            sd = (int(x0 + (x1 - x0) * fx), int(y0 + (y1 - y0) * fy))
            m = mask_from(a, sd, box)
            if m is not None and m.sum() > best:
                best, bs = m.sum(), sd
    return bs


def mask_from(a, seed, box):
    if seed is None:
        seed = auto_seed(a, box)
        if seed is None:
            return None
    x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1].mean(2)
    ok = ((sub > 175).astype(np.uint8) * 255)
    b = Image.fromarray(ok).copy()
    sx, sy = seed[0] - x0, seed[1] - y0
    if ok[sy, sx] != 255:
        return None
    ImageDraw.floodfill(b, (sx, sy), 128)
    reg = np.asarray(b) == 128
    m = np.zeros_like(reg)
    for y in range(reg.shape[0]):
        xs = np.where(reg[y])[0]
        if len(xs):
            m[y, xs.min():xs.max() + 1] = True
    return m


def wrap(d, text, f, maxw):
    out, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            out.append(cur); cur = w
    out.append(cur)
    return out


by = {}
for f in FIX:
    by.setdefault(f[0], []).append(f)
report = []
for n in range(1, 47):
    im = Image.open(f'{ind}/p{n:02d}.png').convert('RGB')
    for (_, seed, box, blocks) in by.get(n, []):
        a = np.asarray(im).astype(int)
        m = mask_from(a, seed, box)
        if m is None:
            report.append(f'p{n} graine {seed} hors bulle'); continue
        ys, xs = np.where(m)
        bw, bh = xs.max() - xs.min(), ys.max() - ys.min()
        touches = (xs.min() == 0) + (ys.min() == 0) + (xs.max() == m.shape[1] - 1) + (ys.max() == m.shape[0] - 1)
        report.append(f'p{n} {seed} masque {bw}x{bh} bords touchés {touches} remplissage {m.mean():.2f}')
        if probe:
            continue
        x0, y0 = box[0], box[1]
        mk = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(5))
        reg = im.crop(box)
        bg = tuple(int(v) for v in np.median(a[y0:box[3], x0:box[2]][m].reshape(-1, 3), axis=0))
        reg.paste(Image.new('RGB', reg.size, bg), (0, 0), mk)
        mm = np.asarray(mk) > 0
        yy = np.where(mm.any(1))[0]
        top, bot = yy.min(), yy.max()
        d = ImageDraw.Draw(reg)
        size = 26
        while True:
            f = ImageFont.truetype(REG, size)
            lines = []
            mid = (top + bot) // 2
            row = np.where(mm[mid])[0]
            maxw = (row.max() - row.min()) * 0.80
            for b in blocks:
                if b.startswith('§'):
                    lines.append(b[1:])
                else:
                    lines += wrap(d, b, f, maxw)
            lh = size * 1.0
            if lh * len(lines) <= (bot - top) * 0.84 and all(d.textlength(l, font=f) <= maxw * 1.02 for l in lines) or size <= 11:
                break
            size -= 1
        y = (top + bot) / 2 - lh * len(lines) / 2
        for ln in lines:
            r = int(min(max(y + lh / 2, top), bot))
            row = np.where(mm[r])[0]
            cx = (row.min() + row.max()) / 2 if len(row) else reg.size[0] / 2
            d.text((cx - d.textlength(ln, font=f) / 2, y), ln, font=f, fill=INK)
            y += lh
        im.paste(reg, (x0, y0))
    if not probe:
        im.save(f'{outd}/p{n:02d}.png')
print('\n'.join(report))
