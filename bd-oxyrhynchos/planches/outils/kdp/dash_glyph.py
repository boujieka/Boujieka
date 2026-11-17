"""Repère les tirets longs par leur forme (sans OCR) : barre horizontale fine, isolée,
encadrée de texte à gauche et à droite, sur fond clair. Écrit dash_candidates.json et dash_contact_N.jpg."""
import sys, json
import numpy as np
from PIL import Image, ImageDraw

ind = sys.argv[1]
allf = []
for n in range(1, 47):
    im = Image.open(f'{ind}/p{n:02d}.png').convert('RGB')
    a = np.asarray(im).astype(int)
    L = a.mean(2)
    H, W = L.shape
    top = 112 if W == 1448 else 115  # sous le bandeau
    dark = L < 110
    light = L > 205
    found = []
    for y in range(top, H - 8):
        row = dark[y]
        x = 0
        while x < W:
            if not row[x]:
                x += 1; continue
            x0 = x
            while x < W and row[x]:
                x += 1
            x1 = x - 1
            w = x1 - x0 + 1
            if not (11 <= w <= 34):
                continue
            # épaisseur : lignes sombres consécutives sur toute la largeur
            t = 1
            while y + t < H and dark[y + t, x0 + 2:x1 - 1].mean() > 0.8:
                t += 1
            if t > 5 or w < 3 * t:
                continue
            if y > 0 and dark[y - 1, x0 + 2:x1 - 1].mean() > 0.3:
                continue  # pas le bord haut
            # fond clair juste au-dessus et au-dessous
            above = light[max(0, y - 4):y - 1, x0:x1 + 1]
            below = light[y + t + 1:y + t + 4, x0:x1 + 1]
            if above.size == 0 or below.size == 0 or above.mean() < 0.85 or below.mean() < 0.85:
                continue
            # extrémités : pas de prolongement (pas une ligne de tableau)
            if dark[y:y + t, max(0, x0 - 3):x0].mean() > 0.2 or dark[y:y + t, x1 + 1:x1 + 4].mean() > 0.2:
                continue
            # texte à gauche et à droite, à hauteur de ligne
            cy = y + t / 2
            hh = int(max(9, 4.5 * t))
            yA, yB = int(cy - hh), int(cy + hh)
            lw = dark[yA:yB, max(0, x0 - int(1.6 * w)):x0 - 3]
            rw = dark[yA:yB, x1 + 4:x1 + int(1.6 * w)]
            if lw.size == 0 or rw.size == 0:
                continue
            if not (0.06 < lw.mean() < 0.55 and 0.06 < rw.mean() < 0.55):
                continue
            # la colonne de texte doit dépasser au-dessus du tiret (lettres)
            if dark[yA:int(cy) - t - 1, max(0, x0 - int(1.6 * w)):x0 - 3].mean() < 0.04:
                continue
            bg = np.median(a[max(0, y - 4):y - 1, x0:x1 + 1].reshape(-1, 3), axis=0)
            found.append(dict(n=n, box=[x0, y, x1, y + t - 1], lh=2 * hh, bg=[int(v) for v in bg]))
    # dédoublonnage
    ded = []
    for f in found:
        if not any(abs(f['box'][0] - g['box'][0]) < 4 and abs(f['box'][1] - g['box'][1]) < 6 for g in ded):
            ded.append(f)
    allf += ded

json.dump(allf, open('dash_candidates.json', 'w'), ensure_ascii=False, indent=1)
print(len(allf), 'candidats')
CW = 260
for part in range(0, len(allf), 60):
    crops = []
    for i in range(part, min(part + 60, len(allf))):
        f = allf[i]
        im = Image.open(f'{ind}/p{f["n"]:02d}.png').convert('RGB')
        x0, y0, x1, y1 = f['box']
        c = im.crop((x0 - 90, y0 - 18, x1 + 90, y1 + 18)).resize((CW, 50))
        d = ImageDraw.Draw(c); d.rectangle((0, 0, 44, 11), fill='black'); d.text((2, 0), f'{i}/p{f["n"]}', fill=(255, 255, 0))
        crops.append(c)
    cols = 4; rows = (len(crops) + cols - 1) // cols
    sheet = Image.new('RGB', (CW * cols, 52 * rows), 'white')
    for k, c in enumerate(crops):
        sheet.paste(c, ((k % cols) * CW, (k // cols) * 52))
    sheet.save(f'dash_contact_{part // 60}.jpg', quality=88)
