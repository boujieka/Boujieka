"""Fichiers d'impression Amazon KDP (broché, encre couleur Premium, 8,5 × 11 pouces, sans fond perdu à l'intérieur).
usage: python3 kdp_build.py plates_dir plates.json cover.png out_dir"""
import sys, os, json
from PIL import Image, ImageFilter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdir, pj, cover, out = sys.argv[1:5]
os.makedirs(out, exist_ok=True)
tmp = out + '/_img'
os.makedirs(tmp, exist_ok=True)
LIB = '/usr/share/fonts/truetype/liberation/'
pdfmetrics.registerFont(TTFont('Serif', LIB + 'LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('SerifB', LIB + 'LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('SerifI', LIB + 'LiberationSerif-Italic.ttf'))

TW, TH = 8.5 * inch, 11 * inch          # format rogné
DPI = 300
plates = json.load(open(pj))
GOLD = (0.65, 0.49, 0.18)
INK = (0.15, 0.13, 0.12)


def hires(src, w_in, name):
    """Agrandit l'image à 300 dpi pour la taille d'impression (n'ajoute pas de détail réel)."""
    im = Image.open(src).convert('RGB')
    tw = int(w_in * DPI)
    th = int(im.height * tw / im.width)
    im = im.resize((tw, th), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    p = f'{tmp}/{name}.jpg'
    im.save(p, 'JPEG', quality=84, optimize=True, dpi=(DPI, DPI))
    return p


def clean(t):
    return t.replace(' — ', ' : ').replace('—', ':').replace(' [N2]', '').replace('’', '’')


# ---------------------------------------------------------------- intérieur
c = canvas.Canvas(f'{out}/KDP_interieur_Tome2_8.5x11.pdf', pagesize=(TW, TH), initialFontName='Serif', initialFontSize=10)
c.setTitle('Les mille visages de l’Égypte ancienne. Tome 2')
c.setAuthor('Courant Continental')
page = 0


def folio(n):
    c.setFont('Serif', 8); c.setFillColorRGB(0.45, 0.45, 0.45)
    x = TW - 0.55 * inch if n % 2 else 0.55 * inch
    c.drawCentredString(x, 0.32 * inch, str(n))


def nextpage():
    global page
    page += 1


# p.1 titre
nextpage()
LOGO_TITLE = os.environ.get('LOGO')
if LOGO_TITLE:
    c.drawImage(ImageReader(LOGO_TITLE), TW / 2 - 1.1 * inch, TH - 2.45 * inch, 2.2 * inch, 2.2 * inch)
else:
    c.setFillColorRGB(*GOLD); c.setFont('SerifB', 14); c.drawCentredString(TW / 2, TH - 2.2 * inch, 'COURANT CONTINENTAL')
c.setFillColorRGB(*INK); c.setFont('Serif', 12); c.drawCentredString(TW / 2, TH - 2.8 * inch, 'Bande dessinée documentaire')
c.setFont('SerifB', 30); c.drawCentredString(TW / 2, TH - 4.0 * inch, 'Les mille visages')
c.drawCentredString(TW / 2, TH - 4.5 * inch, 'de l’Égypte ancienne')
c.setFont('Serif', 18); c.drawCentredString(TW / 2, TH - 5.2 * inch, 'Tome 2')
c.setFont('Serif', 12)
c.drawCentredString(TW / 2, TH - 7.2 * inch, 'Scénario : [Nom de l’auteur à compléter]')
c.drawCentredString(TW / 2, TH - 7.5 * inch, 'Dessin : Emma B.')
c.showPage()

# p.2 mentions légales
nextpage()
c.setFillColorRGB(*INK); c.setFont('Serif', 9.5)
y = 2.6 * inch
for ln in ['Les mille visages de l’Égypte ancienne. Tome 2',
           'Collection Courant Continental',
           '',
           '© 2026 [Nom de l’auteur à compléter]. Tous droits réservés.',
           'Dessins : Emma B.',
           '',
           'ISBN : [à compléter]',
           'Dépôt légal : [à compléter]',
           '',
           'Les œuvres anciennes représentées sont conservées dans les musées cités dans les planches.',
           'Les scènes du passé sont des reconstitutions ; les personnages de Malik et d’Inès sont fictifs.',
           '',
           'Imprimé à la demande.']:
    c.drawString(0.9 * inch, y, ln); y -= 13
c.showPage()

# p.3 sommaire
nextpage()
c.setFillColorRGB(*INK); c.setFont('SerifB', 22); c.drawString(0.9 * inch, TH - 1.1 * inch, 'Sommaire')
first = 5
COLW = (TW - 1.8 * inch - 0.3 * inch) / 2
cols = [0.9 * inch, 0.9 * inch + COLW + 0.3 * inch]
col, y = 0, TH - 1.6 * inch
part = None
def short(t, n=44):
    return t if len(t) <= n else t[:n - 1] + '…'
for i, p in enumerate(plates):
    pt = clean(p['part'])
    if pt != part:
        if y < 1.4 * inch and col == 0:
            col, y = 1, TH - 1.6 * inch
        part = pt; y -= 6
        c.setFont('SerifB', 10); c.setFillColorRGB(*GOLD)
        for ln in simpleSplit(pt, 'SerifB', 10, COLW):
            c.drawString(cols[col], y, ln); y -= 12.5
        y -= 1
    if y < 0.9 * inch and col == 0:
        col, y = 1, TH - 1.6 * inch
    c.setFont('Serif', 9); c.setFillColorRGB(*INK)
    c.drawString(cols[col] + 8, y, short(f"{p['n']}. {clean(p['title'])}"))
    c.drawRightString(cols[col] + COLW, y, str(first + i)); y -= 12
folio(page)
c.showPage()

# p.4 blanche (les planches commencent sur une page impaire)
nextpage()
c.showPage()

# planches : une par page, pivotées d'un quart de tour (lecture à l'italienne)
IMG_W, IMG_H = 10 * inch, 7.5 * inch
for p in plates:
    nextpage()
    jp = hires(f"{pdir}/p{p['n']:02d}.png", 10, f"p{p['n']:02d}")
    w, h = Image.open(jp).size
    scale = min(IMG_W / w, IMG_H / h)
    dw, dh = w * scale, h * scale
    x_left = (TW - dh) / 2
    y_bot = (TH - dw) / 2
    c.saveState()
    c.translate(x_left + dh, y_bot)
    c.rotate(90)
    c.drawImage(ImageReader(jp), 0, 0, dw, dh)
    c.restoreState()
    folio(page)
    c.showPage()
c.save()
n_pages = page
print('intérieur :', n_pages, 'pages')

# ---------------------------------------------------------------- couverture
SPINE = n_pages * 0.002347 * inch          # papier blanc, encre couleur
BLEED = 0.125 * inch
CW = 2 * BLEED + 2 * TW + SPINE
CH = 2 * BLEED + TH
cc = canvas.Canvas(f'{out}/KDP_couverture_Tome2_8.5x11_{n_pages}p.pdf', pagesize=(CW, CH), initialFontName='Serif', initialFontSize=10)
# quatrième (gauche) : fond
cc.setFillColorRGB(0.98, 0.95, 0.88); cc.rect(0, 0, BLEED + TW + SPINE / 2, CH, fill=1, stroke=0)
# première (droite) : illustration, à fond perdu
fx = BLEED + TW + SPINE
fw = TW + BLEED
im = Image.open(cover).convert('RGB')
s = max(fw / im.width, CH / im.height)
cw_px, ch_px = int(im.width * s / inch * DPI), int(im.height * s / inch * DPI)
big = im.resize((cw_px, ch_px), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
need_w, need_h = int(fw / inch * DPI), int(CH / inch * DPI)
ox, oy = (cw_px - need_w) // 2, (ch_px - need_h) // 2
big = big.crop((ox, oy, ox + need_w, oy + need_h))
cp = f'{tmp}/cover_front.jpg'; big.save(cp, 'JPEG', quality=92, dpi=(DPI, DPI))
cc.drawImage(ImageReader(cp), fx, 0, fw, CH)
# dos : couleur unie (pas de texte sous 80 pages)
cc.setFillColorRGB(0.62, 0.45, 0.20); cc.rect(BLEED + TW, 0, SPINE, CH, fill=1, stroke=0)
# texte de quatrième
SAFE = BLEED + 0.5 * inch
x0 = SAFE
y = CH - BLEED - 1.0 * inch
cc.setFillColorRGB(*GOLD); cc.setFont('SerifB', 13); cc.drawString(x0, y, 'COURANT CONTINENTAL'); y -= 34
cc.setFillColorRGB(*INK); cc.setFont('SerifB', 20); cc.drawString(x0, y, 'Pourquoi Isis est-elle un serpent ?'); y -= 34
paras = [
    'Devant une stèle du musée de Leyde, Malik, 14 ans, pose une question toute simple. Avec Inès, dessinatrice, il part d’œuvre en œuvre : la palette de Narmer, le Scribe accroupi, le papyrus d’Ani, la stèle de Metternich, le buste de Néfertiti, le zodiaque de Dendérah…',
    'Une enquête en bande dessinée sur les images de l’Égypte ancienne : qui les a faites, à quoi elles servaient, comment elles ont changé, et ce que l’on ignore encore.',
    'Une règle guide le carnet : une ressemblance n’est pas une preuve. Les œuvres sont présentées avec leur musée et, quand il est connu, leur numéro d’inventaire.',
    'Dès 12 ans.',
]
cc.setFont('Serif', 12.5)
maxw = TW - 2 * (SAFE - BLEED) - 0.2 * inch
for para in paras:
    for ln in simpleSplit(para, 'Serif', 12.5, maxw):
        cc.drawString(x0, y, ln); y -= 17
    y -= 9
# zone code-barres KDP : 2 × 1,2 pouce, en bas à droite de la quatrième, laissée blanche
bx = BLEED + TW - 0.25 * inch - 2 * inch
by = BLEED + 0.25 * inch
cc.setFillColorRGB(1, 1, 1); cc.rect(bx, by, 2 * inch, 1.2 * inch, fill=1, stroke=0)
cc.save()
print('couverture :', round(CW / inch, 3), '×', round(CH / inch, 3), 'po ; dos', round(SPINE / inch, 4), 'po')
