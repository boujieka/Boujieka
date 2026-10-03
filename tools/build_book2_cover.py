"""KDP paperback full wrap cover (draft) for Book 2, PAYGo Solar Finance, 7 x 10 in, white paper.

Run: python tools/build_book2_cover.py [--interior output/20_BOOK2_INTERIOR_7x10_draft.pdf]
The page count is read from the interior PDF; the spine width is page count x 0.002252 in (KDP multiplier for black ink on
white paper). Full cover = bleed + back + spine + front + bleed wide, bleed + trim height + bleed high, bleed 0.125 in.
Outputs: output/20_BOOK2_COVER_7x10_draft.pdf (vector, fonts embedded) and output/20_BOOK2_COVER_thumb160.png (front cover at
160 px wide, the size of a search result thumbnail, for the legibility check).
The back cover text is section 5 of output/12_AMAZON_PUBLISHING_PACK_draft.md. The barcode area (2 x 1.2 in, bottom right
of the back cover, at least 0.25 in from the spine and the trim) is left empty: KDP prints the barcode there.
Draft only: the final cover must be checked against the template that the KDP cover calculator produces for the final count.
"""
import argparse
import subprocess
import sys
from pathlib import Path

from PIL import Image
from pypdf import PdfReader
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
GREEN, GOLD, CREAM = "#0B3020", "#B07C0F", "#F7F3E8"
GOLD_LIGHT = "#E0B44A"  # lighter gold for small type on the green ground (contrast)
AUTHOR = "Emmanuel Boujieka Kamga"
TRIM_W, TRIM_H, BLEED = 7.0, 10.0, 0.125
WHITE_PAPER = 0.002252     # in per page, black ink on white paper (KDP)
SAFE = 0.5                 # text kept 0.5 in inside every trim edge (KDP asks at least 0.125 in; 0.5 in is margin for drift)
SPINE_GAP = 0.0625         # KDP: at least 0.0625 in between spine text and the spine edges
BARCODE_W, BARCODE_H, BARCODE_GAP = 2.0, 1.2, 0.25

FD = Path("/usr/share/fonts/truetype/liberation")
for name, f in (("Sans", "LiberationSans-Regular"), ("SansBold", "LiberationSans-Bold"), ("SansItalic", "LiberationSans-Italic")):
    pdfmetrics.registerFont(TTFont(name, str(FD / f"{f}.ttf")))

BACK_LEAD = ("A practical financial framework for deciding whether a PAYGo solar company can survive growth, absorb credit "
             "losses and attract sustainable capital.")
BACK_BULLETS = ["PAYGo unit economics, from the price plan to lifetime contribution",
                "Cohorts, repayment curves and the PAYGo PERFORM 2026 KPIs",
                "Credit losses, receivables and the borrowing base",
                "Equity, debt, receivables facilities and securitisation",
                "Stress testing and the investment committee decision"]
BACK_AUDIENCE = ("For founders, CFOs, lenders, development finance institutions, impact investors and energy access "
                 "professionals.")
BACK_SERIES = "Book 2 of the Africa Energy Finance collection."


def wrap(c, text, font, size, width):
    lines, line = [], ""
    for w in text.split():
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
    # BOOK 2 mark: gold block at the top right
    c.setFillColor(HexColor(GOLD))
    bw, bh = 1.15 * I, 0.42 * I
    c.rect(right - bw, top - 31, bw, bh, stroke=0, fill=1)
    c.setFillColor(white)
    c.setFont("SansBold", 15)
    c.drawCentredString(right - bw / 2, top - 31 + bh / 2 - 5.2, "BOOK 2")
    # dominant title, three lines; each line set as large as the width allows
    y = top - 1.35 * I
    for word, colour in (("PAYGo", white), ("SOLAR", white), ("FINANCE", HexColor(GOLD_LIGHT))):
        size = min(110, (right - left) / c.stringWidth(word, "SansBold", 1))
        c.setFont("SansBold", size)
        c.setFillColor(colour)
        y -= size * 0.74
        c.drawString(left - size * 0.04, y, word)
        y -= size * 0.18
    c.setStrokeColor(HexColor(GOLD))
    c.setLineWidth(1.5)
    y -= 10
    c.line(left, y, left + 1.6 * I, y)
    # subtitle
    y -= 30
    c.setFillColor(white)
    for ln in wrap(c, "Business Models, Credit Risk and Financial Structuring for Solar Home Systems", "Sans", 19, right - left - 0.4 * I):
        c.setFont("Sans", 19)
        c.drawString(left, y, ln)
        y -= 25
    # author at the foot
    c.setFont("SansBold", 21)
    c.setFillColor(white)
    c.drawString(left, (fy + SAFE) * I + 22, AUTHOR)
    c.setStrokeColor(HexColor(GOLD))
    c.setLineWidth(3)
    c.line(left, (fy + SAFE) * I + 8, right, (fy + SAFE) * I + 8)

    # ---- spine (between the back and the front trim)
    sx = BLEED + TRIM_W
    # no colour block on the spine: KDP allows the fold to drift by about 0.0625 in, which would show a band edge on the boards
    usable = (spine - 2 * SPINE_GAP) * I
    size = min(13, usable / 0.72)        # cap height of Liberation Sans is about 0.72 em
    c.saveState()
    c.translate((sx + spine / 2) * I, (BLEED + TRIM_H) * I)
    c.rotate(-90)                        # reads top to bottom, as on books sold in the US and the UK
    baseline = -size * 0.36
    c.setFillColor(HexColor(GOLD_LIGHT))
    c.setFont("SansBold", size)
    c.drawString(0.5 * I, baseline, "BOOK 2")
    c.setFillColor(white)
    c.drawString(1.9 * I, baseline, "PAYGo SOLAR FINANCE")
    c.setFont("Sans", size * 0.85)
    c.drawRightString((TRIM_H - 0.45) * I, baseline, AUTHOR)
    c.restoreState()
    spine_box = (sx + SPINE_GAP, sx + spine - SPINE_GAP, size)

    # ---- back cover
    bx = BLEED
    left = (bx + SAFE) * I
    right = (bx + TRIM_W - SAFE) * I
    y = (BLEED + TRIM_H - SAFE) * I - 6
    c.setFillColor(HexColor(GOLD_LIGHT))
    c.setFont("SansBold", 10)
    c.drawString(left, y, "AFRICA ENERGY FINANCE  |  BOOK 2")
    y -= 34
    c.setFillColor(white)
    for ln in wrap(c, BACK_LEAD, "SansBold", 17, right - left):
        c.setFont("SansBold", 17)
        c.drawString(left, y, ln)
        y -= 23
    y -= 16
    c.setFont("SansBold", 12.5)
    c.setFillColor(HexColor(GOLD_LIGHT))
    c.drawString(left, y, "Inside the book:")
    y -= 24
    for b in BACK_BULLETS:
        lines = wrap(c, b, "Sans", 12.5, right - left - 18)
        c.setFillColor(HexColor(GOLD))
        c.rect(left, y + 3, 6, 6, stroke=0, fill=1)
        c.setFillColor(white)
        for ln in lines:
            c.setFont("Sans", 12.5)
            c.drawString(left + 18, y, ln)
            y -= 18
        y -= 6
    y -= 14
    for ln in wrap(c, BACK_AUDIENCE, "Sans", 12.5, right - left):
        c.setFont("Sans", 12.5)
        c.drawString(left, y, ln)
        y -= 18
    y -= 12
    c.setFont("SansItalic", 12.5)
    c.setFillColor(HexColor(GOLD_LIGHT))
    c.drawString(left, y, BACK_SERIES)
    text_bottom = y
    # barcode area: bottom right of the back cover, 0.25 in from the spine fold and from the bottom trim; nothing printed
    bc = ((bx + TRIM_W - BARCODE_GAP - BARCODE_W), BLEED + BARCODE_GAP)
    return W, H, text_bottom / I, bc, spine_box


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--interior", default=str(ROOT / "output/20_BOOK2_INTERIOR_7x10_draft.pdf"))
    ap.add_argument("--out", default=str(ROOT / "output/20_BOOK2_COVER_7x10_draft.pdf"))
    ap.add_argument("--thumb", default=str(ROOT / "output/20_BOOK2_COVER_thumb160.png"))
    ap.add_argument("--preview", default=None, help="optional PNG of the whole wrap, 1400 px wide, for review")
    a = ap.parse_args()
    pages = len(PdfReader(a.interior).pages)
    spine = pages * WHITE_PAPER
    W = 2 * BLEED + 2 * TRIM_W + spine
    H = 2 * BLEED + TRIM_H
    c = canvas.Canvas(a.out, pagesize=(W * 72, H * 72), initialFontName="Sans")
    c.setTitle("PAYGo Solar Finance, paperback cover (draft)")
    c.setAuthor(AUTHOR)
    x0_front = BLEED + TRIM_W + spine
    W, H, text_bottom, bc, spine_box = draw(c, spine, x0_front)
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
