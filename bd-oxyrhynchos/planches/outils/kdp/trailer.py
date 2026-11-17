"""Bande-annonce verticale 1080x1920 (30 i/s) du tome 2, sans son.
usage: python3 trailer.py out.mp4"""
import sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = sys.argv[1]
W, H, FPS = 1080, 1920, 30
U = '/root/.claude/uploads/5dea6e80-461c-5e41-9605-3557cec92eb1/'
LOGO = Image.open(U + '9b5ba22e-image.jpg').convert('RGB')
SIGF = Image.open(U + '771787e7-image.jpg').convert('RGB')
COVER = Image.open('cover_new.png').convert('RGB')
FB = '../fonts/oswald/package/files/oswald-latin-700-normal.woff'
FM = '../fonts/oswald/package/files/oswald-latin-600-normal.woff'
GOLD = (236, 190, 80)


def plate(n):
    return Image.open(f'logo/p{n:02d}.png').convert('RGB')


def sig_rgba():
    a = np.asarray(SIGF).astype(float)
    al = np.clip((255 - a.min(2) - 18) / 42, 0, 1) * 255
    im = Image.fromarray(np.dstack([a, al]).astype(np.uint8), 'RGBA')
    return im.crop(im.getbbox())


SIG = sig_rgba()


def ease(t):
    return t * t * (3 - 2 * t)


def bg_of(img):
    b = img.resize((W, int(img.height * W / img.width)) if img.width / img.height < W / H else (int(img.width * H / img.height), H))
    b = b.crop(((b.width - W) // 2, (b.height - H) // 2, (b.width - W) // 2 + W, (b.height - H) // 2 + H))
    b = b.filter(ImageFilter.GaussianBlur(28))
    return Image.blend(b, Image.new('RGB', (W, H), (12, 14, 26)), 0.45)


def text_block(draw, lines, y, size, font=FB, fill='white', box=True, maxw=W - 120):
    f = ImageFont.truetype(font, size)
    # retour à la ligne
    out = []
    for ln in lines:
        cur = ''
        for w in ln.split():
            t = (cur + ' ' + w).strip()
            if draw.textlength(t, font=f) <= maxw:
                cur = t
            else:
                out.append(cur); cur = w
        out.append(cur)
    lh = int(size * 1.22)
    if box:
        bw = max(draw.textlength(l, font=f) for l in out) + 70
        draw.rounded_rectangle(((W - bw) / 2, y - 22, (W + bw) / 2, y + lh * len(out) + 10), radius=26, fill=(10, 12, 24, 200))
    for i, ln in enumerate(out):
        tw = draw.textlength(ln, font=f)
        draw.text(((W - tw) / 2, y + i * lh), ln, font=f, fill=fill, stroke_width=2, stroke_fill=(0, 0, 0))
    return y + lh * len(out)


def scene_plate(img, dur, top_text=None, bottom_text=None, focus=(0.5, 0.5), z0=1.0, z1=1.35, sub=None):
    """Planche horizontale : fond flou, planche agrandie au centre avec zoom lent vers un point."""
    bg = bg_of(img)
    n = int(dur * FPS)
    pw = W - 40
    base_h = int(img.height * pw / img.width)
    for i in range(n):
        t = ease(i / max(1, n - 1))
        z = z0 + (z1 - z0) * t
        # fenêtre de la planche visible (zoom vers le point focal)
        cw, ch = img.width / z, img.height / z
        cx = img.width * (0.5 + (focus[0] - 0.5) * t * (1 - 1 / z) * 2)
        cy = img.height * (0.5 + (focus[1] - 0.5) * t * (1 - 1 / z) * 2)
        x0 = min(max(0, cx - cw / 2), img.width - cw); y0 = min(max(0, cy - ch / 2), img.height - ch)
        win = img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((pw, base_h), Image.BILINEAR)
        fr = bg.copy()
        py = (H - base_h) // 2 + 40
        fr.paste(win, (20, py))
        d = ImageDraw.Draw(fr, 'RGBA')
        d.rectangle((18, py - 2, 20 + pw + 1, py + base_h + 1), outline=GOLD, width=4)
        alpha = min(1, i / 8, (n - i) / 8)
        if top_text:
            text_block(d, top_text, 210, 78)
        if sub:
            text_block(d, [sub], 210 + 78 * 1.22 * len(top_text or []) + 40, 44, font=FM, fill=GOLD, box=False)
        if bottom_text:
            text_block(d, bottom_text, py + base_h + 90, 62)
        yield fade(fr, alpha)


def fade(fr, a):
    if a >= 1:
        return fr
    return Image.blend(Image.new('RGB', (W, H), 'black'), fr, max(0, a))


def scene_cover(dur, texts, final=False):
    img = COVER
    bg = bg_of(img)
    n = int(dur * FPS)
    ch = int(H * (0.55 if final else 0.62)); cw = int(img.width * ch / img.height)
    for i in range(n):
        t = ease(i / max(1, n - 1))
        z = 1.0 + 0.08 * t
        c = img.resize((int(cw * z), int(ch * z)), Image.BILINEAR)
        fr = bg.copy()
        y = 120 if final else 300
        fr.paste(c, ((W - c.width) // 2, y))
        d = ImageDraw.Draw(fr, 'RGBA')
        yy = y + c.height + 60
        for k, (ln, size, col, font) in enumerate(texts):
            yy = text_block(d, [ln], yy, size, font=font, fill=col, box=False) + 18
        if final:
            s = SIG.resize((330, int(SIG.height * 330 / SIG.width)))
            fr.paste(s, (W - 370, H - 150), s)
        yield fade(fr, min(1, i / 8, (n - i) / 10))


def scene_logo(dur):
    n = int(dur * FPS)
    L = LOGO.resize((860, 860))
    for i in range(n):
        fr = Image.new('RGB', (W, H), 'white')
        z = 1 + 0.05 * ease(i / n)
        l = L.resize((int(860 * z), int(860 * z)))
        fr.paste(l, ((W - l.width) // 2, (H - l.height) // 2 - 80))
        d = ImageDraw.Draw(fr)
        f = ImageFont.truetype(FM, 46)
        tx = 'présente'
        d.text(((W - d.textlength(tx, font=f)) / 2, (H + l.height) // 2 - 20), tx, font=f, fill=(20, 40, 90))
        yield fade(fr, min(1, i / 8, (n - i) / 8))


scenes = [
    scene_logo(2.6),
    scene_plate(plate(42), 4.2, ['Pourquoi Isis', 'est-elle un serpent ?'], focus=(0.48, 0.47), z1=1.6),
    scene_cover(4.0, [('Malik a 14 ans. Inès dessine les musées.', 56, 'white', FB),
                      ('Une question devient une enquête.', 50, GOLD, FM)]),
]
works = [(4, 'La palette de Narmer', (0.5, 0.45)), (8, 'Le Scribe accroupi', (0.5, 0.5)),
         (16, 'Nebamon dans les marais', (0.5, 0.5)), (26, 'La pesée du cœur', (0.5, 0.5)),
         (33, 'La stèle de Metternich', (0.5, 0.42)), (38, 'Le buste de Néfertiti', (0.75, 0.3)),
         (41, 'Le zodiaque de Dendérah', (0.5, 0.45))]
for k, (n, name, foc) in enumerate(works):
    scenes.append(scene_plate(plate(n), 2.3, ['D’œuvre en œuvre'] if k == 0 else None, [name], focus=foc, z1=1.25))
scenes += [
    scene_plate(plate(43), 4.2, ['Qui les a faites ?', 'À quoi servaient-elles ?'], ['Que sait-on vraiment ?'], focus=(0.6, 0.55), z1=1.5),
    scene_plate(plate(46), 4.0, ['Une ressemblance', 'n’est pas une preuve.'], focus=(0.5, 0.45), z1=1.3),
    scene_plate(plate(35), 3.0, ['46 planches', '8 chapitres'], focus=(0.5, 0.5), z1=1.2),
    scene_cover(5.5, [('Les mille visages', 66, 'white', FB), ('de l’Égypte ancienne', 66, 'white', FB),
                      ('Tome 2  ·  Bande dessinée documentaire', 44, GOLD, FM), ('Dès 12 ans  ·  Bientôt disponible', 44, 'white', FM)], final=True),
]

p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
count = 0
for sc in scenes:
    for fr in sc:
        p.stdin.write(fr.convert('RGB').tobytes()); count += 1
p.stdin.close(); p.wait()
print('images', count, 'durée', round(count / FPS, 1), 's')
