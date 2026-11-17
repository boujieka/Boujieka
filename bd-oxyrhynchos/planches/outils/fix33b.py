"""Planche 33 (version illustrée) : réplique 33.7 vérifiée + mentions « image provisoire »."""
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
src, out = sys.argv[1:3]
im = Image.open(src).convert('RGB')
FONT = 'fonts/kalam/package/files/kalam-latin-700-normal.woff'
ITAL = 'fonts/fontsource-comic-neue-5.3.0/package/files/comic-neue-latin-700-italic.woff'
INK = (28, 24, 22)

def mask(seed, box):
    x0, y0, x1, y1 = box
    a = (np.asarray(im.crop(box).convert('L')) > 185).astype(np.uint8) * 255
    b = Image.fromarray(a).copy(); ImageDraw.floodfill(b, (seed[0]-x0, seed[1]-y0), 128)
    r = np.asarray(b) == 128; m = np.zeros_like(r)
    for y in range(r.shape[0]):
        xs = np.where(r[y])[0]
        if len(xs): m[y, xs.min():xs.max()+1] = True
    return Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.MinFilter(5))

def fill(seed, box, text, size):
    x0, y0, x1, y1 = box
    mk = mask(seed, box); reg = im.crop(box)
    reg.paste(Image.new('RGB', reg.size, 'white'), (0, 0), mk)
    m = np.asarray(mk) > 0; ys = np.where(m.any(1))[0]; top, bot = ys.min(), ys.max()
    d = ImageDraw.Draw(reg)
    while True:
        f = ImageFont.truetype(FONT, size); mid = (top+bot)//2; xs = np.where(m[mid])[0]
        words, lines, cur = text.split(), [], ''
        for w in words:
            t = (cur+' '+w).strip()
            if d.textlength(t, font=f) <= (xs.max()-xs.min())*0.84: cur = t
            else: lines.append(cur); cur = w
        lines.append(cur); lh = size
        if lh*len(lines) <= (bot-top)*0.86 or size <= 12: break
        size -= 1
    y = (top+bot)//2 - lh*len(lines)//2
    for ln in lines:
        row = min(max(y+lh//2, top), bot); xs = np.where(m[row])[0]
        d.text(((xs.min()+xs.max())/2 - d.textlength(ln, font=f)/2, y), ln, font=f, fill=INK); y += lh
    im.paste(reg, (x0, y0)); return size

s = fill((1350, 795), (1250, 775, 1446, 985),
         'Non. C’est le nom d’un ancien propriétaire. Les objets portent parfois le nom de ceux qui les ont possédés.', 22)
d = ImageDraw.Draw(im); f = ImageFont.truetype(ITAL, 13)
for (x, y, t) in [(470, 690, 'Image provisoire — à remplacer par la photo du Met 50.85 (domaine public)'), (22, 1028, 'Image provisoire')]:
    w = d.textlength(t, font=f); d.rectangle((x-3, y-1, x+w+3, y+16), fill=(255, 248, 225)); d.text((x, y), t, font=f, fill=(120, 30, 20))
im.save(out); print('ok', s)
