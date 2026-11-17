"""Repère les tirets longs (cadratins / demi-cadratins) placés entre deux mots dans les cases,
et les remplace par deux-points. Mode 'detect' : écrit dash_candidates.json + planche contact ;
mode 'apply' : applique les candidats retenus.
usage: python3 dashes.py detect|apply in_dir out_dir"""
import sys, csv, json, re
import numpy as np
from PIL import Image, ImageDraw

mode, ind, outd = sys.argv[1:4]
WORD = re.compile(r"^[«“\"(]?[A-Za-zÀ-ÿŒœ'’0-9.,)]{2,}[»”\")]?[.,:;!?]?$")


def lines_of(n):
    rows = list(csv.DictReader(open(f'up/ocr_p{n:02d}.tsv'), delimiter='\t', quoting=csv.QUOTE_NONE))
    L = {}
    for r in rows:
        if r['level'] != '5' or not r['text'].strip():
            continue
        k = (r['block_num'], r['par_num'], r['line_num'])
        L.setdefault(k, []).append(dict(t=r['text'], x=int(r['left']) // 2, y=int(r['top']) // 2, w=int(r['width']) // 2, h=int(r['height']) // 2, c=float(r['conf'])))
    return [sorted(v, key=lambda d: d['x']) for v in L.values()]


def components(mask):
    """Composantes connexes (4-connexité) d'un petit masque booléen : liste de boîtes."""
    H, W = mask.shape
    seen = np.zeros_like(mask)
    out = []
    for y in range(H):
        for x in range(W):
            if mask[y, x] and not seen[y, x]:
                st = [(y, x)]; seen[y, x] = True; ys = []; xs = []
                while st:
                    cy, cx = st.pop(); ys.append(cy); xs.append(cx)
                    for ny, nx in ((cy + 1, cx), (cy - 1, cx), (cy, cx + 1), (cy, cx - 1)):
                        if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True; st.append((ny, nx))
                out.append((min(xs), min(ys), max(xs), max(ys), len(xs)))
    return out


def detect(n):
    im = Image.open(f'{ind}/p{n:02d}.png').convert('RGB')
    a = np.asarray(im).astype(int)
    found = []
    for words in lines_of(n):
        words = [w for w in words if re.search(r'[A-Za-zÀ-ÿ0-9]', w['t'])]
        for w1, w2 in zip(words, words[1:]):
            if not (WORD.match(w1['t']) and WORD.match(w2['t'])) or min(w1['c'], w2['c']) < 45:
                continue
            gap0, gap1 = w1['x'] + w1['w'], w2['x']
            lh = max(w1['h'], w2['h'])
            if not (lh * 0.6 <= gap1 - gap0 <= lh * 3.5) or abs(w1['y'] - w2['y']) > lh * 0.6:
                continue
            y0 = min(w1['y'], w2['y']); y1 = max(w1['y'] + w1['h'], w2['y'] + w2['h'])
            if y0 < 4 or y1 > a.shape[0] - 5:
                continue
            reg = a[y0:y1 + 1, gap0:gap1]
            if reg.size == 0:
                continue
            bg = np.median(np.concatenate([a[y0 - 3, gap0:gap1], a[y1 + 3, gap0:gap1]]), axis=0)
            lum = reg.mean(2); bgl = bg.mean()
            if bgl < 150:  # texte clair sur fond sombre : ignoré
                continue
            mask = lum < bgl - 80
            for (cx0, cy0, cx1, cy1, area) in components(mask):
                cw, ch = cx1 - cx0 + 1, cy1 - cy0 + 1
                mid = (cy0 + cy1) / 2 / max(1, (y1 - y0))
                if cw >= lh * 0.45 and ch <= max(3, lh * 0.22) and 0.3 <= mid <= 0.8 and area >= cw * ch * 0.6:
                    found.append(dict(n=n, box=[gap0 + cx0, y0 + cy0, gap0 + cx1, y0 + cy1], lh=lh,
                                      ctx=f"{w1['t']} — {w2['t']}", bg=[int(v) for v in bg]))
    return found


plates = range(1, 47)
if mode == 'detect':
    allf = []
    for n in plates:
        allf += detect(n)
    json.dump(allf, open('dash_candidates.json', 'w'), ensure_ascii=False, indent=1)
    # planche contact
    crops = []
    for i, f in enumerate(allf):
        im = Image.open(f'{ind}/p{f["n"]:02d}.png').convert('RGB')
        x0, y0, x1, y1 = f['box']; lh = f['lh']
        c = im.crop((x0 - lh * 5, y0 - lh, x1 + lh * 5, y1 + lh)).resize((300, int(300 * (y1 - y0 + 2 * lh) / (x1 - x0 + 10 * lh))))
        d = ImageDraw.Draw(c); d.text((2, 0), str(i), fill=(255, 0, 0))
        crops.append(c)
    if crops:
        cols = 3; rows = (len(crops) + cols - 1) // cols; hh = max(c.height for c in crops)
        sheet = Image.new('RGB', (300 * cols, hh * rows), 'white')
        for i, c in enumerate(crops):
            sheet.paste(c, ((i % cols) * 300, (i // cols) * hh))
        sheet.save('dash_contact.jpg', quality=85)
    for i, f in enumerate(allf):
        print(i, f['n'], f['ctx'], f['box'])
else:
    keep = json.load(open('dash_keep.json'))
    allf = json.load(open('dash_candidates.json'))
    by = {}
    for i in keep:
        by.setdefault(allf[i]['n'], []).append(allf[i])
    for n in plates:
        im = Image.open(f'{ind}/p{n:02d}.png').convert('RGB')
        a = np.asarray(im).astype(int)
        d = ImageDraw.Draw(im)
        for f in by.get(n, []):
            x0, y0, x1, y1 = f['box']
            ink = tuple(int(v) for v in np.median(a[y0:y1 + 1, x0:x1 + 1].reshape(-1, 3), axis=0))
            d.rectangle((x0 - 1, y0 - 2, x1 + 1, y1 + 2), fill=tuple(f['bg']))
            t = y1 - y0 + 1; r = min(2.4, max(1.4, t * 0.6)); cx = (x0 + x1) / 2; cy = (y0 + y1) / 2
            sp = max(3.2, min(5.0, (x1 - x0 + 1) * 0.22))
            for dy in (-sp, sp):
                d.ellipse((cx - r, cy + dy - r, cx + r, cy + dy + r), fill=ink)
        im.save(f'{outd}/p{n:02d}.png')
    print('appliqué :', sum(len(v) for v in by.values()))
