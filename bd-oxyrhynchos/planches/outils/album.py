"""Assemble les planches du tome 2 en un PDF (couverture, sommaire, planches, extrait, variantes).
usage: python3 album.py dossier_sortie"""
import sys, os, shutil
from PIL import Image
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

U = '/root/.claude/uploads/5dea6e80-461c-5e41-9605-3557cec92eb1/'
REPO = '/home/user/Boujieka/bd-oxyrhynchos/planches/'
out = sys.argv[1]
os.makedirs(out + '/tome2', exist_ok=True)
os.makedirs(out + '/tome2/variantes', exist_ok=True)

pdfmetrics.registerFont(TTFont('Serif', '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('SerifB', '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('SerifI', '/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf'))

COVER = U + '7f1984cd-image.png'
PLANCHES = [  # (numéro, partie, titre, fichier)
    (1, 'Prologue — La question', 'La question', '9c6b04d7'),
    (2, 'Prologue — La question', 'Un serpent avec une barbe', 'af59904f'),
    (3, 'Chapitre 1 — Les premières images royales', 'Bien avant les rois', '5c8f4508'),
    (4, 'Chapitre 1 — Les premières images royales', 'Une palette pour quoi faire ?', '3706ccf1'),
    (5, 'Chapitre 1 — Les premières images royales', 'Le roi est grand (mais pas géant)', '245511d1'),
    (6, 'Chapitre 1 — Les premières images royales', 'Des chats-girafes et un porteur de sandales', '0d07522e'),
    (7, 'Chapitre 1 — Les premières images royales', 'Narmer, version Malik', '6cabb700'),
    (8, 'Chapitre 2 — Qui faisait les images ?', 'Le Scribe qui regarde', '4fd6c3e3'),
    (9, 'Chapitre 2 — Qui faisait les images ?', 'La grille', 'ee5fff33'),
    (10, 'Chapitre 2 — Qui faisait les images ?', 'Le village des artisans', '3a50aa22'),
    (11, 'Chapitre 2 — Qui faisait les images ?', 'Le village des faiseurs d’images', '78a40acb'),
    (12, 'Chapitre 2 — Qui faisait les images ?', 'Les cailloux qui parlent', '71b99610'),
    (13, 'Chapitre 2 — Qui faisait les images ?', 'Le peintre dans sa propre tombe / La grille qui agrandit', '660f380a'),
    (14, 'Chapitre 3 — La vie en images', 'La vie en images', 'baf9d858'),
    (15, 'Chapitre 3 — La vie en images', 'Labourer, moissonner, compter', '2001a0de'),
    (16, 'Chapitre 3 — La vie en images', 'Dans les marais', 'f756c234'),
    (17, 'Chapitre 3 — La vie en images', 'Musiciennes et danseuses', '32664b31'),
    (18, 'Chapitre 3 — La vie en images', 'Soigner par écrit / Ce ne sont pas des photos', '54a72007'),
    (19, 'Chapitre 4 — Isis, mille visages', 'Un trône pour nom', '0cb4604e'),
    (20, 'Chapitre 4 — Isis, mille visages', 'La reine et la déesse', 'e9746133'),
    (21, 'Chapitre 4 — Isis, mille visages', 'Des cornes, un disque, des ailes', '1789126a'),
    (22, 'Chapitre 4 — Isis, mille visages', 'Les visages d’Isis (1/2)', '294ee4ec'),
    (24, 'Chapitre 4 — Isis, mille visages', 'Seuil I « Le trône » [N2]', '887bddd5'),
    (25, 'Chapitre 5 — Osiris et le voyage des morts', 'Un livre qui n’en est pas un', '7aaa07cd'),
    (26, 'Chapitre 5 — Osiris et le voyage des morts', 'La pesée du cœur', '0acb9c2f'),
    (27, 'Chapitre 5 — Osiris et le voyage des morts', 'Qui a fait ce rouleau ?', '8d70fd49'),
    (28, 'Chapitre 5 — Osiris et le voyage des morts', 'Le gardien couché', '5f904ab8'),
    (29, 'Chapitre 5 — Osiris et le voyage des morts', 'Croire, étudier', 'e8500d65'),
    (30, 'Chapitre 6 — Les serpents : protéger, nourrir, menacer', 'Des serpents partout', '7d5730c8'),
    (31, 'Chapitre 6 — Les serpents : protéger, nourrir, menacer', 'Trois serpents, trois métiers', 'ce5c47f6'),
    (32, 'Chapitre 6 — Les serpents : protéger, nourrir, menacer', 'La nuit du soleil', 'c6f9e353'),
    (33, 'Chapitre 6 — Les serpents : protéger, nourrir, menacer', 'Une pierre couverte de formules', REPO + 'Tome2_planche_33_v5.png'),
    (34, 'Chapitre 6 — Les serpents : protéger, nourrir, menacer', 'Ni bons, ni mauvais', '87fd8a6e'),
    (35, 'Chapitre 6 — Les serpents : protéger, nourrir, menacer', 'Seuil II « La douzième heure » [N2]', '515fb4f2'),
    (36, 'Chapitre 7 — Amarna : quand l’image change', 'Berlin, la salle qui ne ressemble pas aux autres', '79ac36a9'),
    (37, 'Chapitre 7 — Amarna : quand l’image change', 'Une famille sous le soleil', '73943958'),
    (38, 'Chapitre 7 — Amarna : quand l’image change', 'Le buste et son voyage', '7eda70cb'),
    (39, 'Chapitre 7 — Amarna : quand l’image change', 'Le retour et la leçon', '2cfabbd3'),
    (40, 'Chapitre 8 — Grecs et Romains au bord du Nil', 'Après Alexandre', 'f85751ee'),
    (41, 'Chapitre 8 — Grecs et Romains au bord du Nil', 'Un ciel au plafond', '739a0fe2'),
    (42, 'Chapitre 8 — Grecs et Romains au bord du Nil', 'Retour à Leyde (les sept regards, 1)', 'b603a463'),
    (43, 'Chapitre 8 — Grecs et Romains au bord du Nil', 'Ce que dit la stèle (les sept regards, 2)', '97767062'),
    (44, 'Chapitre 8 — Grecs et Romains au bord du Nil', 'Seuil III « Les deux mondes » [N2]', '6842cce6'),
    (45, 'Épilogue — Ce qui reste des images', 'Ce qui reste des images', 'ae24c203'),
    (46, 'Épilogue — Ce qui reste des images', 'Une ressemblance n’est pas une preuve', 'e07d4cee'),
]
EXTRAIT = (33, 'Chapitre 6 — Les serpents : protéger, nourrir, menacer', 'Une pierre couverte de formules', REPO + 'Tome2_planche_33_v4.png')
VARIANTES = [  # (planche, description, fichier)
    (1, 'Première version, bandeau « Images d’Afrique »', '2c5b58b1'),
    (2, 'Première version, bandeau « Images d’Afrique »', 'a3371740'),
    (3, 'Première version, bandeau « Images d’Afrique »', 'f823dd17'),
    (3, 'Autre version « Courant Continental » (non retenue)', '5c088a01'),
    (12, 'Autre version (non retenue)', 'fa62237f'),
    (33, 'Version à emplacements vides (base de la version retenue)', 'aa68f44a'),
    (33, 'Version avec images : « XXVe dynastie » erroné, bulle 33.5 coupée, 33.7 non vérifiée', 'c6c26df6'),
    (34, 'Première version : date d’Apédémak non sourcée, ordre 34.7–34.8 inversé', 'bafa48b0'),
    (33, 'Version composée v4 (remplacée par la version illustrée corrigée)', REPO + 'Tome2_planche_33_v4.png'),
    (33, 'Version illustrée d’origine : 33.7 non vérifiée (« chancelier autrichien, 1828 »)', '85dd3616'),
    (34, 'Troisième version : « Ier siècle » non sourcé, coquille « din serpent »', '77e42714'),
]
src = lambda f: f if f.startswith('/') else U + f + '-image.png'
JT = '/tmp/claude-0/-home-user-Boujieka/5dea6e80-461c-5e41-9605-3557cec92eb1/scratchpad/jpg_album/'
os.makedirs(JT, exist_ok=True)


def jpg(path):
    dst = JT + os.path.basename(path).rsplit('.', 1)[0] + '.jpg'
    Image.open(path).convert('RGB').save(dst, 'JPEG', quality=90, optimize=True)
    return dst

P_W, P_H = A4            # portrait
L_W, L_H = landscape(A4)
c = canvas.Canvas(out + '/Tome2_Les_mille_visages_complet.pdf', pagesize=A4)
c.setTitle('Les mille visages de l’Égypte ancienne — Tome 2 — Planches 1 à 46')
c.setAuthor('Projet Courant Continental / Images d’Afrique')
page_no = [0]


def footer(text, w):
    c.setFont('SerifI', 8); c.setFillGray(0.45)
    c.drawCentredString(w / 2, 14, text)


def draw_image(path, w, h, margin=18, top=18, bottom=30):
    im = ImageReader(jpg(path))
    iw, ih = im.getSize()
    s = min((w - 2 * margin) / iw, (h - top - bottom) / ih)
    dw, dh = iw * s, ih * s
    c.drawImage(im, (w - dw) / 2, bottom + (h - top - bottom - dh) / 2, dw, dh)


def new_page(size):
    c.setPageSize(size)
    page_no[0] += 1


# 1. Couverture (pleine page)
new_page(A4)
im = ImageReader(jpg(COVER)); iw, ih = im.getSize(); s = max(P_W / iw, P_H / ih)
c.drawImage(im, (P_W - iw * s) / 2, (P_H - ih * s) / 2, iw * s, ih * s)
c.showPage()

# 2. Sommaire
new_page(A4)
c.setFillColorRGB(0.23, 0.18, 0.12)
c.setFont('SerifB', 22); c.drawString(60, P_H - 80, 'Les mille visages de l’Égypte ancienne')
c.setFont('Serif', 13); c.drawString(60, P_H - 102, 'Tome 2 — Planches 1 à 46 (version de travail, novembre 2026)')
first_page = 3
COLW = (P_W - 100) / 2
cols = [50, 50 + COLW + 10]
col, y = 0, P_H - 130
part = None
def short(t, n=46):
    return t if len(t) <= n else t[:n - 1] + '…'
for i, (n, pt, t, f) in enumerate(PLANCHES):
    if pt != part:
        need = 32
        if y - need < 70 and col == 0:
            col, y = 1, P_H - 130
        part = pt; y -= 6
        c.setFont('SerifB', 10.5); c.setFillColorRGB(0.65, 0.49, 0.18); c.drawString(cols[col], y, short(pt, 52)); y -= 14
    if y < 70 and col == 0:
        col, y = 1, P_H - 130
    x = cols[col]
    c.setFont('Serif', 9.5); c.setFillColorRGB(0.15, 0.13, 0.12)
    c.drawString(x + 10, y, short(f'{n}. {t}'))
    c.drawRightString(x + COLW, y, str(first_page + i)); y -= 12.5
y -= 14
c.setFont('SerifB', 10.5); c.setFillColorRGB(0.65, 0.49, 0.18); c.drawString(cols[col], y, 'Annexes'); y -= 14
c.setFont('Serif', 9.5); c.setFillColorRGB(0.15, 0.13, 0.12)
c.drawString(cols[col] + 10, y, 'Variantes non retenues'); c.drawRightString(cols[col] + COLW, y, str(first_page + len(PLANCHES))); y -= 12.5
c.drawString(cols[col] + 10, y, 'Planche manquante : 23 (à recevoir)')
c.setFont('SerifI', 8.5); c.setFillGray(0.35); y = 52
for line in ['Document de travail. Les images d’œuvres dessinées ou générées sont provisoires : elles seront remplacées ou contrôlées',
             'd’après les photographies et notices des institutions (registre iconographique). Les mentions [H], [I], [F] et [À VÉRIFIER]',
             'visibles sur certaines planches sont des repères de travail.']:
    c.drawString(50, y, line); y -= 11
footer('Sommaire', P_W)
c.showPage()

# 3. Planches
for n, pt, t, f in PLANCHES:
    new_page(landscape(A4))
    draw_image(src(f), L_W, L_H)
    footer(f'{pt} — Planche {n} — {t} — p. {page_no[0]}', L_W)
    c.showPage()
    shutil.copy(src(f), f'{out}/tome2/Tome2_planche_{n:02d}.png')

# 5. Variantes (titre puis une variante par page)
for k, (n, d, f) in enumerate(VARIANTES):
    im = Image.open(src(f)); size = landscape(A4) if im.width >= im.height else A4
    new_page(size); w, h = size
    if k == 0:
        c.setFont('SerifB', 13); c.setFillColorRGB(0.23, 0.18, 0.12)
        c.drawString(24, h - 22, 'Annexe — Variantes non retenues')
        draw_image(src(f), w, h, top=34)
    else:
        draw_image(src(f), w, h)
    footer(f'Variante — Planche {n} — {d} — p. {page_no[0]}', w)
    c.showPage()
    shutil.copy(src(f), f'{out}/tome2/variantes/Tome2_planche_{n:02d}_variante_{k + 1}.png')

shutil.copy(COVER, f'{out}/tome2/Tome2_couverture.png')
c.save()
print('ok', page_no[0], 'pages')
