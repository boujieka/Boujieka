"""Assemble l'intérieur et la couverture KDP du Volume 1.

Format : broché KDP 8,25 x 6 po (paysage), couleur premium, avec fond perdu.
Usage : python3 build_kdp.py            -> sortie/interieur.pdf + sortie/couverture.pdf + aperçus
"""
import re
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

HERE = Path(__file__).resolve().parent
OUT = HERE / "sortie"
CACHE = HERE / "build"

IN = 72.0
TRIM_W, TRIM_H, BLEED = 8.25, 6.0, 0.125
PAGE_W, PAGE_H = TRIM_W + BLEED, TRIM_H + 2 * BLEED      # fond perdu : extérieur, haut, bas
MARGIN = 0.375                                             # intérieur et extérieur (KDP, 24-150 p., avec fond perdu)
SPINE_PER_PAGE = 0.002347                                  # couleur premium (KDP)
SPINE_TEXT_MIN_PAGES = 79                                  # KDP : pas de texte au dos en dessous

NAVY, NAVY_DARK = HexColor("#0e1830"), HexColor("#0a1124")
GOLD, CREAM, MUTED = HexColor("#d4a94f"), HexColor("#f3e6c8"), HexColor("#b9ad92")
TAG = {"H": HexColor("#2f6f4f"), "F": HexColor("#2c5d8a"), "S": HexColor("#8a4b2c")}

pdfmetrics.registerFont(TTFont("Cinzel", str(HERE / "fonts/Cinzel.ttf")))
pdfmetrics.registerFont(TTFont("Garamond", str(HERE / "fonts/EBGaramond.ttf")))
pdfmetrics.registerFont(TTFont("GaramondIt", str(HERE / "fonts/EBGaramond-Italic.ttf")))

TITLE = "Les Mystères du tombeau de Ramsès VI"
SUBTITLE = "Le Livre de la Terre — Le secret de la renaissance solaire"
AUTHOR = "Emma B."
MOTTO = ("« … comme si le dieu solaire allait d'un commencement à un autre sans jamais "
         "atteindre la “fin”. »")
MOTTO_SRC = "J. C. Darnell (2018, p. 498), paraphrasant J. A. Roberson (2012, p. 148)"


# ---------------------------------------------------------------- images

def prepared(src: Path, target_w_in=7.0, dpi=300) -> Path:
    """Agrandit l'image (Lanczos) pour atteindre 300 ppp à la taille imprimée, l'accentue légèrement ;
    JPEG haute qualité en cache. (Agrandir n'ajoute pas de détail : seule une source plus grande le fait.)"""
    CACHE.mkdir(exist_ok=True)
    dst = CACHE / (src.stem + f"_{dpi}ppp.jpg")
    if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
        im = Image.open(src).convert("RGB")
        scale = max(1.0, target_w_in * dpi / im.width)
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
        im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=55, threshold=2))
        im.save(dst, "JPEG", quality=92, subsampling=0, dpi=(dpi, dpi))
    return dst


def read_manifest():
    pages = []
    for line in (HERE / "manifest.txt").read_text(encoding="utf8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        path, _, label = (p.strip() for p in line.partition("|"))
        pages.append({"src": path, "label": label or None})
    return pages


# ---------------------------------------------------------------- mise en page

def trim_box(page_no):
    """Zone de coupe (x0, y0) en points. Page impaire = belle page : petit fond (reliure) à gauche."""
    x0 = 0 if page_no % 2 == 1 else BLEED * IN
    return x0, BLEED * IN


def content_box(page_no):
    x0, y0 = trim_box(page_no)
    return (x0 + MARGIN * IN, y0 + MARGIN * IN,
            (TRIM_W - 2 * MARGIN) * IN, (TRIM_H - 2 * MARGIN) * IN)


def background(c):
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W * IN, PAGE_H * IN, stroke=0, fill=1)


def centered(c, text, y, font, size, color, x_center):
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawCentredString(x_center, y, text)


def wrap(text, font, size, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if pdfmetrics.stringWidth(test, font, size) <= width:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def paragraph(c, text, x, y, width, font="Garamond", size=10, color=CREAM, leading=None):
    leading = leading or size * 1.3
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrap(text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


def gold_rule(c, x_center, y, half):
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.line(x_center - half, y, x_center + half, y)


def page_image(c, page_no, src):
    bx, by, bw, bh = content_box(page_no)
    img = prepared(HERE / src)
    w, h = Image.open(img).size
    s = min(bw / w, bh / h)
    dw, dh = w * s, h * s
    x, y = bx + (bw - dw) / 2, by + (bh - dh) / 2
    c.drawImage(str(img), x, y, dw, dh)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    c.rect(x - 2, y - 2, dw + 4, dh + 4, stroke=1, fill=0)
    return 1448 / (dw / IN)          # résolution réelle de la source (ppp)


def page_titre(c, page_no):
    bx, by, bw, bh = content_box(page_no)
    xc = bx + bw / 2
    top = by + bh
    centered(c, f"{AUTHOR.upper()} PRÉSENTE", top - 30, "Cinzel", 11, GOLD, xc)
    gold_rule(c, xc, top - 52, 150)
    centered(c, "LES MYSTÈRES DU", top - 105, "Cinzel", 26, GOLD, xc)
    centered(c, "TOMBEAU DE RAMSÈS VI", top - 148, "Cinzel", 36, GOLD, xc)
    gold_rule(c, xc, top - 172, 150)
    centered(c, "Le Livre de la Terre", top - 205, "GaramondIt", 20, CREAM, xc)
    centered(c, "Le secret de la renaissance solaire", top - 228, "GaramondIt", 15, CREAM, xc)
    centered(c, "VOLUME 1", top - 275, "Cinzel", 14, GOLD, xc)
    centered(c, "Une aventure archéologique du Dr Kerbu", by + 20, "Garamond", 12, MUTED, xc)


def page_mentions(c, page_no):
    bx, by, bw, bh = content_box(page_no)
    x, w = bx + 20, bw - 40
    y = by + bh - 20
    blocks = [
        ("Cinzel", 10, GOLD, f"{TITLE} — Volume 1"),
        ("GaramondIt", 10, CREAM, SUBTITLE),
        None,
        ("Garamond", 9.5, CREAM, f"© 2026 {AUTHOR} Tous droits réservés."),
        ("Garamond", 9.5, CREAM, "ISBN : [à compléter avant publication]"),
        ("Garamond", 9.5, CREAM, "Dépôt légal : [mois année]"),
        ("Garamond", 9.5, CREAM, "Impression à la demande. Le lieu d'impression figure sur la dernière page."),
        None,
        ("Cinzel", 9, GOLD, "Avertissement"),
        ("Garamond", 9.5, CREAM,
         "Cette bande dessinée est une œuvre de fiction appuyée sur des sources historiques. Les "
         "personnages contemporains (le Dr Kerbu, Nefertari Hassan, Adel Mansour, Maya, Julien Marsac), "
         "la mission scientifique et l'accès nocturne au tombeau sont imaginaires ; toute ressemblance "
         "avec des personnes existantes serait fortuite. Les reconstitutions de l'Antiquité et les "
         "scènes mythologiques sont des interprétations visuelles, et non des copies exactes des parois."),
        None,
        ("Garamond", 9.5, CREAM,
         "Les illustrations ont été réalisées à l'aide d'un outil de génération d'images par "
         f"intelligence artificielle, sous la direction éditoriale d'{AUTHOR}"),
    ]
    for b in blocks:
        if b is None:
            y -= 12
            continue
        font, size, color, text = b
        y = paragraph(c, text, x, y, w, font, size + 1, color) - 3


def page_lecture(c, page_no):
    bx, by, bw, bh = content_box(page_no)
    xc = bx + bw / 2
    top = by + bh
    centered(c, "COMMENT LIRE CETTE BANDE DESSINÉE", top - 26, "Cinzel", 14, GOLD, xc)
    gold_rule(c, xc, top - 40, 170)
    y = top - 72
    rows = [
        ("H", "Histoire documentée", "Monuments, inscriptions, dates et faits vérifiables, sourcés dans les "
              "pages documentaires."),
        ("F", "Fiction", "Personnages d'aujourd'hui, dialogues, mission scientifique et péripéties."),
        ("S", "Symbolisme", "Interprétations philosophiques ou poétiques, présentées comme telles."),
    ]
    for tag, name, text in rows:
        c.setFillColor(TAG[tag])
        c.roundRect(bx + 30, y - 6, 30, 20, 4, stroke=0, fill=1)
        centered(c, f"[{tag}]", y, "Cinzel", 10, CREAM, bx + 45)
        c.setFont("Cinzel", 10.5)
        c.setFillColor(GOLD)
        c.drawString(bx + 75, y + 2, name)
        paragraph(c, text, bx + 75, y - 13, bw - 120, size=10)
        y -= 62
    y -= 4
    y = paragraph(c, "Les cases bordées d'un liseré doré sont des reconstitutions : le passé ou le "
                     "monde des dieux, tel que les images le racontent — pas un événement réel.",
                  bx + 30, y, bw - 60, "GaramondIt", 10.5)
    paragraph(c, "Les salles du tombeau sont désignées par les lettres du Theban Mapping Project "
                 "(de A, l'entrée, à K, au bout de l'axe).", bx + 30, y - 8, bw - 60, "GaramondIt", 10.5)


def page_sommaire(c, page_no, entries):
    bx, by, bw, bh = content_box(page_no)
    xc = bx + bw / 2
    top = by + bh
    centered(c, "SOMMAIRE", top - 26, "Cinzel", 16, GOLD, xc)
    gold_rule(c, xc, top - 40, 120)
    y = top - 80
    x1, x2 = bx + 70, bx + bw - 70
    for label, no in entries:
        c.setFont("Garamond", 13)
        c.setFillColor(CREAM)
        c.drawString(x1, y, label)
        c.drawRightString(x2, y, str(no))
        lw = pdfmetrics.stringWidth(label, "Garamond", 13)
        c.setFillColor(MUTED)
        c.setFont("Garamond", 13)
        dots_x = x1 + lw + 8
        while dots_x < x2 - 22:
            c.drawString(dots_x, y, ".")
            dots_x += 5
        y -= 30


def page_a_suivre(c, page_no, heading="À SUIVRE…"):
    bx, by, bw, bh = content_box(page_no)
    xc = bx + bw / 2
    yc = by + bh / 2
    centered(c, heading, yc + 60, "Cinzel", 24, GOLD, xc)
    gold_rule(c, xc, yc + 40, 110)
    y = yc + 5
    for line in wrap(MOTTO, "GaramondIt", 14, bw - 140):
        centered(c, line, y, "GaramondIt", 14, CREAM, xc)
        y -= 19
    centered(c, MOTTO_SRC, y - 8, "Garamond", 9.5, MUTED, xc)


GENERATED = {"@titre": page_titre, "@mentions": page_mentions, "@lecture": page_lecture,
             "@a_suivre": page_a_suivre,
             "@fin": lambda c, n: page_a_suivre(c, n, "FIN DU VOLUME 1")}


def build_interior():
    pages = read_manifest()
    entries = [(p["label"], i + 1) for i, p in enumerate(pages) if p["label"]]
    OUT.mkdir(exist_ok=True)
    c = canvas.Canvas(str(OUT / "interieur.pdf"), pagesize=(PAGE_W * IN, PAGE_H * IN), initialFontName="Garamond")
    c.setTitle(f"{TITLE} — Volume 1")
    c.setAuthor(AUTHOR)
    report = []
    for i, p in enumerate(pages, start=1):
        background(c)
        if p["src"] == "@sommaire":
            page_sommaire(c, i, entries)
        elif p["src"] in GENERATED:
            GENERATED[p["src"]](c, i)
        else:
            dpi = page_image(c, i, p["src"])
            report.append((i, p["src"], dpi))
        c.showPage()
    c.save()
    return len(pages), report


# ---------------------------------------------------------------- couverture

def split_wrap(path):
    """Sépare 4e de couverture / dos / 1re de couverture dans la maquette (repère : colonnes bleu nuit du dos)."""
    im = Image.open(path).convert("RGB")
    w, h = im.size
    navy = []
    for x in range(int(w * 0.40), int(w * 0.60)):
        col = [im.getpixel((x, y)) for y in range(0, h, 6)]
        r = sum(c[0] for c in col) / len(col)
        b = sum(c[2] for c in col) / len(col)
        if b - r > 20:
            navy.append(x)
    left, right = min(navy), max(navy)
    return im.crop((0, 0, left - 1, h)), im.crop((right + 3, 0, w, h))


def erase_barcode(back):
    """Efface le code-barres (ISBN invalide) : cadre blanc en bas à droite, remplacé par un flou sombre."""
    w, h = back.size
    g = back.convert("L")
    # lignes et colonnes majoritairement blanches = cadre du code-barres (le texte clair, lui, est clairsemé)
    x0, y0 = int(w * 0.55), int(h * 0.70)
    white = lambda x, y: g.getpixel((x, y)) > 238
    rows = [y for y in range(y0, h) if sum(white(x, y) for x in range(x0, w)) > (w - x0) * 0.35]
    if not rows:
        return back
    cols = [x for x in range(x0, w) if sum(white(x, y) for y in range(min(rows), max(rows) + 1)) > len(rows) * 0.5]
    xs, ys = cols or [x0], rows
    box = (max(min(xs) - 6, 0), max(min(ys) - 6, 0), min(max(xs) + 6, w), min(max(ys) + 6, h))
    blurred = ImageEnhance.Brightness(back.filter(ImageFilter.GaussianBlur(60))).enhance(0.32)
    out = back.copy()
    out.paste(blurred.crop(box), box)
    return out


def panel(art, trim_left_px, px_w, px_h, dpi):
    """Panneau paysage : fond = l'illustration floutée ; au centre de la zone de coupe, l'illustration nette."""
    bg_scale = max(px_w / art.width, px_h / art.height)
    bg = art.resize((round(art.width * bg_scale), round(art.height * bg_scale)), Image.LANCZOS)
    bg = bg.crop(((bg.width - px_w) // 2, (bg.height - px_h) // 2,
                  (bg.width - px_w) // 2 + px_w, (bg.height - px_h) // 2 + px_h))
    bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(28))).enhance(0.45)
    fh = round((TRIM_H - 0.30) * dpi)                       # marge de sécurité > 0,125 po
    fw = round(art.width * fh / art.height)
    fg = art.resize((fw, fh), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.4, percent=50, threshold=2))
    x = trim_left_px + (round(TRIM_W * dpi) - fw) // 2
    y = (px_h - fh) // 2
    bg.paste(fg, (x, y))
    return bg, (x, y, fw, fh)


def build_cover(npages, dpi=300):
    spine = npages * SPINE_PER_PAGE
    W = 2 * BLEED + 2 * TRIM_W + spine
    H = PAGE_H
    pw, ph = round((TRIM_W + BLEED) * dpi), round(H * dpi)
    face, dos = HERE / "sources/couverture_face.png", HERE / "sources/couverture_dos.png"
    if face.exists() and dos.exists():
        # couverture paysage définitive : chaque image remplit son panneau (fond perdu compris)
        def fill(path):
            im = Image.open(path).convert("RGB")
            s = max(pw / im.width, ph / im.height)
            im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
            return im.crop(((im.width - pw) // 2, (im.height - ph) // 2,
                            (im.width - pw) // 2 + pw, (im.height - ph) // 2 + ph))
        back_img, front_img, back_box, front_box = fill(dos), fill(face), None, None
    else:
        # épreuve provisoire : illustration portrait centrée sur son propre fond flou
        back, front = split_wrap(HERE / "sources/00_couverture_portrait_source.png")
        back = erase_barcode(back)
        back_img, back_box = panel(back, round(BLEED * dpi), pw, ph, dpi)
        front_img, front_box = panel(front, 0, pw, ph, dpi)
    full = Image.new("RGB", (round(W * dpi), ph), (14, 24, 48))
    full.paste(back_img, (0, 0))
    fx = round((BLEED + TRIM_W + spine) * dpi)
    full.paste(front_img, (fx, 0))
    OUT.mkdir(exist_ok=True)
    jpg = CACHE / "couverture.jpg"
    full.save(jpg, "JPEG", quality=94, subsampling=0, dpi=(dpi, dpi))
    c = canvas.Canvas(str(OUT / "couverture.pdf"), pagesize=(W * IN, H * IN), initialFontName="Garamond")
    c.setTitle(f"{TITLE} — Volume 1 — couverture")
    c.drawImage(str(jpg), 0, 0, W * IN, H * IN)
    # liserés dorés autour des illustrations nettes
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    for off, box in ((0, back_box), (fx, front_box)):
        if box is None:
            continue
        x, y, w, h = box
        c.rect((off + x) / dpi * IN - 2, (ph - y - h) / dpi * IN - 2, w / dpi * IN + 4, h / dpi * IN + 4)
    # dos : bleu nuit, deux filets ; texte seulement à partir de 79 pages (règle KDP)
    sx = (BLEED + TRIM_W) * IN
    c.setFillColor(NAVY_DARK)
    c.rect(sx, 0, spine * IN, H * IN, stroke=0, fill=1)
    if npages >= SPINE_TEXT_MIN_PAGES:
        c.saveState()
        c.translate(sx + spine * IN / 2 + 3, H * IN / 2)
        c.rotate(-90)
        c.setFont("Cinzel", min(8, spine * IN * 0.55))
        c.setFillColor(GOLD)
        c.drawCentredString(0, 0, f"{TITLE.upper()} · 1")
        c.restoreState()
    c.save()
    full.resize((full.width // 4, full.height // 4), Image.LANCZOS).save(OUT / "apercu_couverture.jpg", quality=88)
    return W, spine


def previews():
    import subprocess
    subprocess.run(["pdftoppm", "-jpeg", "-r", "40", str(OUT / "interieur.pdf"), str(CACHE / "p")], check=True)
    files = sorted(CACHE.glob("p-*.jpg"))
    ims = [Image.open(f) for f in files]
    w, h = ims[0].size
    cols = 4
    sheet = Image.new("RGB", (w * cols, h * ((len(ims) + cols - 1) // cols)), "white")
    for k, im in enumerate(ims):
        sheet.paste(im, ((k % cols) * w, (k // cols) * h))
    sheet.save(OUT / "apercu_interieur.jpg", quality=85)
    for f in files:
        f.unlink()


if __name__ == "__main__":
    n, report = build_interior()
    W, spine = build_cover(n)
    previews()
    print(f"Intérieur : {n} pages, {PAGE_W} x {PAGE_H} po (fond perdu)")
    print(f"Couverture : {W:.3f} x {PAGE_H} po, dos {spine:.3f} po")
    low = min(d for _, _, d in report)
    print(f"Résolution réelle des planches : {low:.0f} ppp (KDP recommande 300)")
    if n < 24:
        print(f"ATTENTION : {n} pages < 24, minimum KDP en couleur premium")
