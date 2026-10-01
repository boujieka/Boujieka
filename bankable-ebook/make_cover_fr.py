"""French front cover: replace the English title block of the cover art with French typography.

usage: make_cover_fr.py cover_src.png fonts_dir out.png
Works at 2x (2048 x 3072). The English lettering (rows ~100-655 of the 1024 x 1536 art, right of the
hieroglyph column) is replaced by a per-column blend of the parchment above and the sky below.
"""
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

src, fonts, out = sys.argv[1:4]
S = 2
im = Image.open(src).convert("RGB").resize((1024 * S, 1536 * S), Image.LANCZOS)
a = np.asarray(im).astype(np.float32)

x0, y0, y1 = 135 * S, 96 * S, 676 * S          # patch: columns x0.., rows y0..y1
top = a[y0 - 12 * S:y0, x0:].mean(axis=0)       # parchment just above the title
bot = a[y1:y1 + 10 * S, x0:].mean(axis=0)       # sky just below the tagline box
t = np.linspace(0, 1, y1 - y0)[:, None, None]
t = t ** 1.6                                      # stay parchment-coloured longer, warm towards the sky
patch = top[None] * (1 - t) + bot[None] * t
# smooth the column profile so no vertical streaks survive, then add a light paper grain
patch_img = Image.fromarray(patch.clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(18 * S))
patch = np.asarray(patch_img).astype(np.float32)
rng = np.random.default_rng(7)
grain = rng.normal(0, 3.2, patch.shape[:2])[..., None]
patch = (patch + grain).clip(0, 255)
# feather the left edge into the hieroglyph column and the bottom edge into the sky
fx = np.clip(np.arange(patch.shape[1]) / (10 * S), 0, 1)[None, :, None]
fy = np.clip((y1 - y0 - np.arange(y1 - y0)) / (10 * S), 0, 1)[:, None, None]
w = fx * fy
a[y0:y1, x0:] = a[y0:y1, x0:] * (1 - w) + patch * w
im = Image.fromarray(a.astype(np.uint8))

d = ImageDraw.Draw(im)
F = lambda name, size: ImageFont.truetype(f"{fonts}/{name}", size * S)
navy, gold, brown = (20, 33, 61), (176, 124, 38), (128, 84, 20)
cx = 578 * S


def center(text, y, font, fill, spacing=0):
    if spacing:
        widths = [d.textlength(c, font=font) for c in text]
        total = sum(widths) + spacing * S * (len(text) - 1)
        x = cx - total / 2
        for c, wdt in zip(text, widths):
            d.text((x, y), c, font=font, fill=fill)
            x += wdt + spacing * S
        return
    d.text((cx - d.textlength(text, font=font) / 2, y), text, font=font, fill=fill)


center("BANCABLE", 128 * S, F("CharisSIL-Bold.ttf", 118), navy)
center("NE SUFFIT PAS", 262 * S, F("CharisSIL-Bold.ttf", 82), brown)
# rule with a gold dot
d.line([(cx - 330 * S, 392 * S), (cx - 30 * S, 392 * S)], fill=gold, width=3 * S)
d.line([(cx + 30 * S, 392 * S), (cx + 330 * S, 392 * S)], fill=gold, width=3 * S)
d.ellipse([cx - 14 * S, 378 * S, cx + 14 * S, 406 * S], fill=gold)
center("Boucler les contrats électriques de l'Afrique", 428 * S, F("CharisSIL-Regular.ttf", 37), navy)
center("sans ouvrir de passifs publics", 476 * S, F("CharisSIL-Regular.ttf", 37), navy)
center("LE CADRE DU BOUCLAGE FINANCIER SOUTENABLE", 548 * S, F("CharisSIL-Regular.ttf", 21), navy, spacing=2.2)
# tagline box
tag = "7 TESTS. 45 QUESTIONS. 3 ÉTAPES DE CONTRÔLE. 1 DÉCISION."
tf = F("CharisSIL-Regular.ttf", 19)
tw = sum(d.textlength(c, font=tf) for c in tag) + 1.6 * S * (len(tag) - 1)
d.rectangle([cx - tw / 2 - 22 * S, 590 * S, cx + tw / 2 + 22 * S, 634 * S], fill=navy)
center(tag, 600 * S, tf, (240, 228, 205), spacing=1.6)
im.save(out)
print("wrote", out, im.size)
