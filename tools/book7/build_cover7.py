"""KDP paperback full wrap cover (draft) for Book 7, Hydropower Development and Finance, 7 x 10 in (BOOK_TRIM=6x9 for 6 x 9), white paper.

Run: python tools/book7/build_cover7.py [--interior book7/build/Hydropower_Development_and_Finance_7x10.pdf]
The page count is read from the interior PDF; the spine width is page count x 0.002252 in (KDP multiplier for black ink on
white paper). Full cover = bleed + back + spine + front + bleed wide, bleed + trim height + bleed high, bleed 0.125 in.
Outputs: book7/publishing/BOOK7_COVER_7x10_draft.pdf (vector, fonts embedded) and book7/publishing/BOOK7_COVER_thumb160.png (front cover at
160 px wide, the size of a search result thumbnail, for the legibility check).
The back cover text is section 5 of book7/publishing/AMAZON_PUBLISHING_PACK_BOOK7.md. The barcode area (2 x 1.2 in, bottom right
of the back cover, at least 0.25 in from the spine and the trim) is left empty: KDP prints the barcode there.
Draft only: the final cover must be checked against the template that the KDP cover calculator produces for the final count.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image
from pypdf import PdfReader
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[2]
GREEN, GOLD, CREAM = "#0B3020", "#B07C0F", "#F7F3E8"
GOLD_LIGHT = "#E0B44A"  # lighter gold for small type on the green ground (contrast)
AUTHOR = "Emmanuel Boujieka Kamga"
TRIM_TAG = os.environ.get("BOOK_TRIM", "7x10")  # 6x9 or 7x10, to match the interior
TRIM_W, TRIM_H = (6.0, 9.0) if TRIM_TAG == "6x9" else (7.0, 10.0)
BLEED = 0.125
WHITE_PAPER = 0.002252     # in per page, black ink on white paper (KDP)
SAFE = 0.5                 # text kept 0.5 in inside every trim edge (KDP asks at least 0.125 in; 0.5 in is margin for drift)
SPINE_GAP = 0.0625         # KDP: at least 0.0625 in between spine text and the spine edges
BARCODE_W, BARCODE_H, BARCODE_GAP = 2.0, 1.2, 0.25
ISBN = "9798178961780"          # KDP-assigned paperback ISBN (imprint: Independently published)
ISBN_DISPLAY = "ISBN 979-8178961780"


def draw_barcode(c, x_in, y_in):
    """EAN-13 of the ISBN, vector, on a white panel filling the KDP barcode area (2 x 1.2 in)."""
    from reportlab.graphics.barcode import createBarcodeDrawing
    from reportlab.graphics import renderPDF
    from reportlab.graphics import shapes
    shapes.STATE_DEFAULTS["fontName"] = "Sans"   # the renderer's default font would otherwise be an unembedded Times-Roman
    I = 72
    c.setFillColor(white)
    c.rect(x_in * I, y_in * I, BARCODE_W * I, BARCODE_H * I, stroke=0, fill=1)
    d = createBarcodeDrawing("EAN13", value=ISBN[:12], barWidth=0.0135 * I, barHeight=0.62 * I, humanReadable=True,
                             fontName="Sans", fontSize=8)
    bx = x_in * I + (BARCODE_W * I - d.width) / 2
    renderPDF.draw(d, c, bx, y_in * I + 0.16 * I)
    c.setFillColor(HexColor("#000000"))
    c.setFont("Sans", 8.5)
    c.drawCentredString((x_in + BARCODE_W / 2) * I, (y_in + BARCODE_H - 0.2) * I, ISBN_DISPLAY)

FD = Path("/usr/share/fonts/truetype/liberation")
for name, f in (("Sans", "LiberationSans-Regular"), ("SansBold", "LiberationSans-Bold"), ("SansItalic", "LiberationSans-Italic")):
    pdfmetrics.registerFont(TTFont(name, str(FD / f"{f}.ttf")))

BACK_LEAD = ("Should this hydropower project keep being developed, who should fund the next stage, who should carry "
             "each risk, and is it actually ready for financial close?")
BACK_BULLETS = ["Three investments in one asset: development option, construction contract, operating annuity",
                "Developer economics: risk-weighted value, success-path return, co-developer entry",
                "Debt sizing on the river: P50, one-year and ten-year P90, drought tests and reserves",
                "The buyer and the state: payment capacity, guarantees, contingent liabilities",
                "The Hydro Readiness Framework: 8 questions, 23 evidence gates, one close decision",
                "A technical due-diligence reference and a worked 60 MW case, from site to close"]
BACK_AUDIENCE = ("For developers, lenders, development finance institutions, investors and government decision-makers, "
                 "with questions for the investment and credit committees at the end of every chapter. "
                 "A companion financial model applies the method.")
BACK_SERIES = "Book 7 of the Africa Energy Finance collection."
GROUPS = [4, 6, 2, 1, 4, 3, 3]  # gates per framework question Q1 to Q7
FR = os.environ.get("BOOK_LANG") == "fr"  # French edition: French texts, no barcode until a French ISBN exists
TX = {"book": "BOOK 7", "spine": "HYDROPOWER DEVELOPMENT AND FINANCE", "inside": "Inside the book:", "series_line": "AFRICA ENERGY FINANCE  |  BOOK 7",
      "title": (("HYDROPOWER", 0), ("DEVELOPMENT", 0), ("AND FINANCE", 1)), "sub1": "From River to Financial Close",
      "sub2": "A Developer, Lender and Government Framework for Hydropower Projects in Africa",
      "fw1": "THE HYDRO READINESS FRAMEWORK\u2122", "fw2": "8 Questions \u00b7 23 Gates \u00b7 1 Financial Close Decision",
      "parties": "DEVELOPER  \u00b7  LENDER  \u00b7  GOVERNMENT"}
if FR:
    TX = {"book": "LIVRE 7", "spine": "DÉVELOPPEMENT ET FINANCEMENT DE L'HYDROÉLECTRICITÉ", "inside": "Dans ce livre :",
          "series_line": "AFRICA ENERGY FINANCE  |  LIVRE 7",
          "title": (("DÉVELOPPEMENT", 0), ("ET FINANCEMENT DE", 0), ("L'HYDROÉLECTRICITÉ", 1)), "sub1": "De la rivière au bouclage financier",
          "sub2": "Un cadre pour les développeurs, les prêteurs et les États, appliqué aux projets hydroélectriques en Afrique",
          "fw1": "LE HYDRO READINESS FRAMEWORK\u2122", "fw2": "8 questions \u00b7 23 portes \u00b7 1 décision de bouclage financier",
          "parties": "DÉVELOPPEUR  \u00b7  PRÊTEUR  \u00b7  ÉTAT"}
    BACK_LEAD = ("Faut-il poursuivre le développement de ce projet hydroélectrique, qui doit financer l'étape suivante, "
                 "qui doit porter chaque risque, et le projet est-il vraiment prêt pour le bouclage financier\u00a0?")
    BACK_BULLETS = ["Trois investissements dans un même actif : option de développement, contrat de construction, rente d'exploitation",
                    "L'économie du développeur : valeur pondérée par le risque, rendement en cas de succès, entrée d'un co-développeur",
                    "Le dimensionnement de la dette sur la rivière : P50, P90 à un an et à dix ans, sécheresses et réserves",
                    "L'acheteur et l'État : capacité de paiement, garanties, passifs éventuels",
                    "Le Hydro Readiness Framework : 8 questions, 23 portes de preuve, une décision de bouclage",
                    "Un référentiel de due diligence technique et un cas complet de 60\u00a0MW, du site au bouclage"]
    BACK_AUDIENCE = ("Pour les développeurs, les prêteurs, les institutions de financement du développement, les investisseurs "
                     "et les décideurs publics, avec des questions pour les comités d'investissement et de crédit à la fin de chaque "
                     "chapitre. Un modèle financier d'accompagnement applique la méthode.")
    BACK_SERIES = "Livre 7 de la collection Africa Energy Finance."


def wrap(c, text, font, size, width):
    lines, line = [], ""
    for w in text.split(" "):  # split on plain spaces only: no-break spaces hold "60 MW" together
        t = (line + " " + w).strip()
        if c.stringWidth(t, font, size) > width and line:
            lines.append(line)
            line = w
        else:
            line = t
    return lines + [line]


def draw(c, spine, x0_front):
    W = 2 * BLEED + 2 * TRIM_W + spine
    H = 2 * BLEED + TRIM_H
    I = 72
    c.setFillColor(HexColor(GREEN))
    c.rect(0, 0, W * I, H * I, stroke=0, fill=1)

    # ---- front cover (trim box starts at x0_front, y = BLEED)
    fx, fy = x0_front, BLEED
    left = (fx + SAFE) * I
    right = (fx + TRIM_W - SAFE) * I
    top = (fy + TRIM_H - SAFE) * I
    c.setFillColor(HexColor(GOLD_LIGHT))
    c.setFont("SansBold", 13)
    c.drawString(left, top - 13, "AFRICA ENERGY FINANCE")
    c.setFillColor(white)
    c.setFont("Sans", 9.5)
    c.drawString(left, top - 28, "Business & Financial Models")
    c.setStrokeColor(HexColor(GOLD))
    c.setLineWidth(3)
    c.line(left, top - 42, right, top - 42)
    # BOOK 7 mark: gold block at the top right
    c.setFillColor(HexColor(GOLD))
    bw, bh = 1.15 * I, 0.42 * I
    c.rect(right - bw, top - 31, bw, bh, stroke=0, fill=1)
    c.setFillColor(white)
    c.setFont("SansBold", 15)
    c.drawCentredString(right - bw / 2, top - 31 + bh / 2 - 5.2, TX["book"])
    # dominant title, three lines, each as large as the width allows (capped so the three lines balance)
    y = top - 1.15 * I
    for word, gold in TX["title"]:
        colour, cap = (HexColor(GOLD_LIGHT) if gold else white), (56 if FR else 74)
        size = min(cap, (right - left) / c.stringWidth(word, "SansBold", 1))
        c.setFont("SansBold", size)
        c.setFillColor(colour)
        y -= size * 0.74
        c.drawString(left - size * 0.03, y, word)
        y -= size * 0.22
    c.setStrokeColor(HexColor(GOLD))
    c.setLineWidth(1.5)
    y -= 6
    c.line(left, y, left + 1.6 * I, y)
    # subtitle in two levels
    y -= 34
    c.setFillColor(white)
    sub = min(24, (right - left) / c.stringWidth(TX["sub1"], "SansBold", 1))
    c.setFont("SansBold", sub)
    c.drawString(left, y, TX["sub1"])
    y -= 26
    for ln in wrap(c, TX["sub2"], "Sans", 15 * min(1, TRIM_W / 7.0 + 0.08), right - left):
        c.setFont("Sans", 15 * min(1, TRIM_W / 7.0 + 0.08))
        c.drawString(left, y, ln)
        y -= 20
    # framework panel: the 23 gates as squares grouped by question
    y -= 30
    c.setFillColor(HexColor(GOLD_LIGHT))
    c.setFont("SansBold", 12.5)
    c.drawString(left, y, TX["fw1"])
    y -= 19
    c.setFillColor(white)
    c.setFont("Sans", 12.5)
    c.drawString(left, y, TX["fw2"])
    y -= 30
    K = TRIM_W / 7.0  # the gate row and the subtitle scale with the trim width (1 at 7 x 10)
    sq, gap, ggap = 0.15 * I * K, 0.045 * I * K, 0.15 * I * K
    x = left
    for gi, n in enumerate(GROUPS):
        for k in range(n):
            c.setStrokeColor(HexColor(GOLD))
            c.setLineWidth(1.1)
            c.setFillColor(HexColor(GOLD))
            c.rect(x, y, sq, sq, stroke=1, fill=0)
            x += sq + gap
        x += ggap - gap
    c.setFillColor(white)
    c.rect(x + 0.04 * I * K, y - 0.03 * I * K, 0.21 * I * K, 0.21 * I * K, stroke=0, fill=1)  # the close decision
    assert x + 0.25 * I * K <= right, "gate row outside the safe area"
    y -= 34
    c.setFillColor(HexColor(GOLD_LIGHT))
    c.setFont("SansBold", 11)
    c.drawString(left, y, TX["parties"])
    # author at the foot
    c.setFont("SansBold", 21)
    c.setFillColor(white)
    c.drawString(left, (fy + SAFE) * I + 22, AUTHOR)
    c.setStrokeColor(HexColor(GOLD))
    c.setLineWidth(3)
    c.line(left, (fy + SAFE) * I + 8, right, (fy + SAFE) * I + 8)
    front_bottom_text = y

    # ---- spine (between the back and the front trim)
    sx = BLEED + TRIM_W
    # no colour block on the spine: KDP allows the fold to drift by about 0.0625 in, which would show a band edge on the boards
    usable = (spine - 2 * SPINE_GAP) * I
    size = min(13, usable / 0.72)        # cap height of Liberation Sans is about 0.72 em
    c.saveState()
    c.translate((sx + spine / 2) * I, (BLEED + TRIM_H) * I)
    c.rotate(-90)                        # reads top to bottom, as on books sold in the US and the UK
    baseline = -size * 0.36
    # the title must end before the author's name: shrink the spine type if the title is long (French edition)
    room = (TRIM_H - 0.45 - 1.5) * I - c.stringWidth(AUTHOR, "Sans", size * 0.85) - 0.3 * I
    size = min(size, size * room / c.stringWidth(TX["spine"], "SansBold", size))
    c.setFillColor(HexColor(GOLD_LIGHT))
    c.setFont("SansBold", size)
    c.drawString(0.5 * I, baseline, TX["book"])
    c.setFillColor(white)
    c.drawString(1.5 * I, baseline, TX["spine"])
    c.setFont("Sans", size * 0.85)
    c.drawRightString((TRIM_H - 0.45) * I, baseline, AUTHOR)
    c.restoreState()
    spine_box = (sx + SPINE_GAP, sx + spine - SPINE_GAP, size)

    # ---- back cover (French text runs longer: set about 8 percent smaller so it clears the barcode area)
    BK = 0.92 if FR else 1.0
    bx = BLEED
    left = (bx + SAFE) * I
    right = (bx + TRIM_W - SAFE) * I
    y = (BLEED + TRIM_H - SAFE) * I - 6
    c.setFillColor(HexColor(GOLD_LIGHT))
    c.setFont("SansBold", 10 * BK)
    c.drawString(left, y, TX["series_line"])
    y -= 34 * BK
    c.setFillColor(white)
    for ln in wrap(c, BACK_LEAD, "SansBold", 16 * BK, right - left):
        c.setFont("SansBold", 16 * BK)
        c.drawString(left, y, ln)
        y -= 22 * BK
    y -= 16 * BK
    c.setFont("SansBold", 12.5 * BK)
    c.setFillColor(HexColor(GOLD_LIGHT))
    c.drawString(left, y, TX["inside"])
    y -= 24 * BK
    for b in BACK_BULLETS:
        lines = wrap(c, b, "Sans", 12 * BK, right - left - 18)
        c.setFillColor(HexColor(GOLD))
        c.rect(left, y + 3, 6, 6, stroke=0, fill=1)
        c.setFillColor(white)
        for ln in lines:
            c.setFont("Sans", 12 * BK)
            c.drawString(left + 18, y, ln)
            y -= 16.5 * BK
        y -= 5 * BK
    y -= 14 * BK
    for ln in wrap(c, BACK_AUDIENCE, "Sans", 12.5 * BK, right - left):
        c.setFont("Sans", 12.5 * BK)
        c.drawString(left, y, ln)
        y -= 18 * BK
    y -= 12 * BK
    c.setFont("SansItalic", 12.5 * BK)
    c.setFillColor(HexColor(GOLD_LIGHT))
    c.drawString(left, y, BACK_SERIES)
    text_bottom = y
    # barcode area: bottom right of the back cover, 0.25 in from the spine fold and from the bottom trim; nothing printed
    bc = ((bx + TRIM_W - BARCODE_GAP - BARCODE_W), BLEED + BARCODE_GAP)
    return W, H, text_bottom / I, bc, spine_box


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--interior", default=str(ROOT / f"book7/build/Hydropower_Development_and_Finance_{TRIM_TAG}.pdf"))
    ap.add_argument("--out", default=str(ROOT / f"book7/publishing/BOOK7_COVER_{TRIM_TAG}_draft.pdf"))
    ap.add_argument("--thumb", default=str(ROOT / ("book7/publishing/BOOK7_COVER_thumb160.png" if TRIM_TAG == "7x10" else f"book7/publishing/BOOK7_COVER_{TRIM_TAG}_thumb160.png")))
    ap.add_argument("--preview", default=None, help="optional PNG of the whole wrap, 1400 px wide, for review")
    ap.add_argument("--no-barcode", action="store_true", help="leave the barcode area empty so that KDP prints its own")
    a = ap.parse_args()
    pages = len(PdfReader(a.interior).pages)
    spine = pages * WHITE_PAPER
    W = 2 * BLEED + 2 * TRIM_W + spine
    H = 2 * BLEED + TRIM_H
    c = canvas.Canvas(a.out, pagesize=(W * 72, H * 72), initialFontName="Sans")
    c.setTitle("Hydropower Development and Finance, paperback cover (draft)")
    c.setAuthor(AUTHOR)
    x0_front = BLEED + TRIM_W + spine
    W, H, text_bottom, bc, spine_box = draw(c, spine, x0_front)
    if not a.no_barcode and not FR:  # the English ISBN must never appear on the French edition
        draw_barcode(c, bc[0], bc[1])
    c.showPage()
    c.save()
    print(f"{a.out}: {pages} pages, spine {spine:.4f} in, full cover {W:.4f} x {H:.4f} in "
          f"({W * 25.4:.1f} x {H * 25.4:.1f} mm)")
    ok_text = text_bottom > bc[1] + BARCODE_H + 0.1
    print(f"barcode area {BARCODE_W} x {BARCODE_H} in at x {bc[0]:.3f} in, y {bc[1]:.3f} in from the bottom left: "
          f"{'clear of back cover text' if ok_text else 'OVERLAPS back cover text'}")
    print(f"spine text {spine_box[2]:.1f} pt between x {spine_box[0]:.3f} and {spine_box[1]:.3f} in "
          f"(spine text allowed: {'yes' if pages > 79 else 'no, 79 pages or fewer'})")
    fonts = subprocess.run(["pdffonts", a.out], capture_output=True, text=True).stdout.strip().split("\n")[2:]
    print(f"fonts: {len(fonts)}, not embedded: {sum(1 for l in fonts if l.split()[-5] != 'yes')}")
    # thumbnail of the front cover (trim box only) at 160 px wide
    tmp = Path(a.thumb).with_suffix(".full.png")
    subprocess.run(["pdftoppm", "-r", "150", "-png", "-singlefile", a.out, str(tmp.with_suffix(""))], check=True)
    full = Image.open(tmp)
    s = full.size[0] / W
    front = full.crop((int(x0_front * s), int(BLEED * s), int((x0_front + TRIM_W) * s), int((BLEED + TRIM_H) * s)))
    front.resize((160, round(160 * TRIM_H / TRIM_W)), Image.LANCZOS).save(a.thumb)
    if a.preview:
        full.resize((1400, round(1400 * H / W)), Image.LANCZOS).save(a.preview)
    tmp.unlink()
    print(a.thumb, "160 px wide")
    if not ok_text or pages <= 79:
        sys.exit(2)


if __name__ == "__main__":
    main()
