"""Build the narrative bible PDF of « Le Pays sous nos pieds » from bible.txt.

Usage: python build_bible.py [bible.txt] [output.pdf]

Markup of bible.txt (one directive per line, blank line = paragraph break):
  === PAGE            start a new page
  kicker: TEXT        small ochre caps line above the title
  title: TEXT         page title
  sub: TEXT           ochre subtitle under the title
  ## TEXT             section heading
  > TEXT              framed quote / key line
  ! PREFIX. TEXT      episode note (À retenir., Question citoyenne., Dossier / limites., Sources.)
  ~ TEXT              small grey note
  url: URL            source link (teal, small)
  tag: TEXT           status line of a source (bold, small)
  - TEXT              bullet item
  | a | b | c         table row (first row of a run is the header)
  any other line      body paragraph
The cover is built from a "=== COVER" block with keys author/series/tagline/volume/version/pitch,
followed by ## sections.
"""
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, PageBreak, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

HERE = Path(__file__).resolve().parent
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
pdfmetrics.registerFont(TTFont("DV", str(FONT_DIR / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DVB", str(FONT_DIR / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DVB", italic="DV", boldItalic="DVB")

TEAL = colors.HexColor("#173F3C")
OCHRE = colors.HexColor("#B0773A")
INK = colors.HexColor("#2B2B2B")
GREY = colors.HexColor("#5E5E5E")
LINK = colors.HexColor("#1F5F6B")
PALE = colors.HexColor("#F4EFE6")

FOOTER = "LE PAYS SOUS NOS PIEDS • Emmanuel Boujieka Kamga • Bible V2.1"

S = {
    "kicker": ParagraphStyle("kicker", fontName="DVB", fontSize=8, leading=11, textColor=OCHRE,
                             spaceAfter=6),
    "title": ParagraphStyle("title", fontName="DVB", fontSize=23, leading=28, textColor=TEAL,
                            spaceAfter=8),
    "sub": ParagraphStyle("sub", fontName="DVB", fontSize=8.5, leading=12, textColor=OCHRE,
                          spaceAfter=6),
    "h": ParagraphStyle("h", fontName="DVB", fontSize=10.5, leading=14, textColor=TEAL,
                        spaceBefore=7, spaceAfter=2),
    "p": ParagraphStyle("p", fontName="DV", fontSize=9.6, leading=14.2, textColor=INK,
                        spaceAfter=3, alignment=TA_LEFT),
    "li": ParagraphStyle("li", fontName="DV", fontSize=9.2, leading=13.2, textColor=INK,
                         leftIndent=11, bulletIndent=2, spaceAfter=1.5),
    "quote": ParagraphStyle("quote", fontName="DV", fontSize=10.6, leading=15, textColor=TEAL),
    "note": ParagraphStyle("note", fontName="DV", fontSize=7.6, leading=10.4, textColor=GREY,
                           spaceAfter=3),
    "small": ParagraphStyle("small", fontName="DV", fontSize=7.6, leading=10.4, textColor=GREY,
                            spaceAfter=3),
    "url": ParagraphStyle("url", fontName="DV", fontSize=7.4, leading=10, textColor=LINK,
                          spaceAfter=3),
    "tag": ParagraphStyle("tag", fontName="DVB", fontSize=7.4, leading=10, textColor=OCHRE,
                          spaceAfter=1),
    "cell": ParagraphStyle("cell", fontName="DV", fontSize=7.4, leading=9.6, textColor=INK),
    "cellh": ParagraphStyle("cellh", fontName="DVB", fontSize=7.4, leading=9.6,
                            textColor=colors.white),
    "c_author": ParagraphStyle("c_author", fontName="DVB", fontSize=8.5, leading=12,
                               textColor=OCHRE, spaceAfter=14),
    "c_series": ParagraphStyle("c_series", fontName="DVB", fontSize=27, leading=34,
                               textColor=TEAL, spaceAfter=4),
    "c_tag": ParagraphStyle("c_tag", fontName="DV", fontSize=10, leading=14, textColor=TEAL),
    "c_volume": ParagraphStyle("c_volume", fontName="DVB", fontSize=27, leading=32,
                               textColor=TEAL, spaceBefore=26, spaceAfter=8),
    "c_version": ParagraphStyle("c_version", fontName="DVB", fontSize=8.5, leading=12,
                                textColor=OCHRE, spaceAfter=8),
}


def esc(text):
    """Escape for reportlab mini-HTML, keep **bold** markers as <b>."""
    t = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # French typography: no line break inside « … » or before : ; ? !
    t = t.replace("« ", "«\u00a0").replace(" »", "\u00a0»")
    t = re.sub(r" ([:;?!])", "\u00a0\\1", t)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)


def boxed(flow, width, pad=8, bg=None):
    t = Table([[flow]], colWidths=[width])
    style = [("BOX", (0, 0), (-1, -1), 0.9, OCHRE),
             ("LEFTPADDING", (0, 0), (-1, -1), pad), ("RIGHTPADDING", (0, 0), (-1, -1), pad),
             ("TOPPADDING", (0, 0), (-1, -1), pad), ("BOTTOMPADDING", (0, 0), (-1, -1), pad + 2)]
    if bg:
        style.append(("BACKGROUND", (0, 0), (-1, -1), bg))
    t.setStyle(TableStyle(style))
    return t


def make_table(rows, width):
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    data = [[Paragraph(esc(c), S["cellh"] if i == 0 else S["cell"]) for c in r]
            for i, r in enumerate(rows)]
    # column widths follow the average text length of each column (bounded)
    weights = []
    for c in range(ncol):
        avg = sum(len(r[c]) for r in rows) / len(rows)
        weights.append(min(max(avg, 8), 70) ** 0.8)
    total = sum(weights)
    widths = [width * wt / total for wt in weights]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TEAL),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#C9BBA5")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    return t


def parse(path, width):
    story = []
    lines = Path(path).read_text(encoding="utf-8").split("\n")
    first_page = True
    i = 0
    cover = None
    table_rows = []

    def flush_table():
        if table_rows:
            story.append(Spacer(1, 3))
            story.append(make_table(list(table_rows), width))
            story.append(Spacer(1, 5))
            table_rows.clear()

    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        i += 1
        if not line.startswith("|"):
            flush_table()
        if not line or line.startswith("#!"):
            continue
        if line == "=== COVER":
            cover = {}
            first_page = False
            continue
        if line == "=== PAGE":
            if cover is not None:
                cover = None
            if not first_page:
                story.append(PageBreak())
            first_page = False
            continue
        if cover is not None and re.match(r"^(author|series|tagline|volume|version|pitch):", line):
            key, val = line.split(":", 1)
            val = val.strip()
            if key == "author":
                story.append(Spacer(1, 6))
                story.append(Paragraph(esc(val), S["c_author"]))
            elif key == "series":
                story.append(Paragraph(esc(val).replace(" / ", "<br/>"), S["c_series"]))
            elif key == "tagline":
                story.append(boxed(Paragraph(esc(val), S["c_tag"]), width, pad=8))
            elif key == "volume":
                story.append(Paragraph(esc(val), S["c_volume"]))
            elif key == "version":
                story.append(Paragraph(esc(val), S["c_version"]))
            elif key == "pitch":
                story.append(Paragraph(esc(val), S["p"]))
                story.append(Spacer(1, 18))
            continue
        if line.startswith("kicker:"):
            story.append(Paragraph(esc(line[7:].strip()), S["kicker"]))
        elif line.startswith("title:"):
            story.append(Paragraph(esc(line[6:].strip()), S["title"]))
        elif line.startswith("sub:"):
            story.append(Paragraph(esc(line[4:].strip()), S["sub"]))
        elif line.startswith("## "):
            # keep heading with the next flowable
            head = Paragraph(esc(line[3:]), S["h"])
            nxt = []
            while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith(
                    ("## ", "=== ", "|")):
                nxt.append(lines[i].strip())
                i += 1
                break
            flows = [head] + [block_for(n, width) for n in nxt]
            story.append(KeepTogether(flows))
        elif line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            table_rows.append(cells)
        else:
            story.append(block_for(line, width))
    flush_table()
    return story


def block_for(line, width):
    if line.startswith("> "):
        return KeepTogether([Spacer(1, 4), boxed(Paragraph(esc(line[2:]), S["quote"]), width),
                             Spacer(1, 5)])
    if line.startswith("! "):
        body = line[2:]
        m = re.match(r"^([^.]+\.)\s*(.*)$", body)
        if m:
            return Paragraph(f"<b>{esc(m.group(1))}</b> {esc(m.group(2))}", S["note"])
        return Paragraph(esc(body), S["note"])
    if line.startswith("~ "):
        return Paragraph(esc(line[2:]), S["small"])
    if line.startswith("url:"):
        u = line[4:].strip()
        return Paragraph(f'<link href="{esc(u)}">{esc(u)}</link>', S["url"])
    if line.startswith("tag:"):
        return Paragraph(esc(line[4:].strip()), S["tag"])
    if line.startswith("- "):
        return Paragraph(esc(line[2:]), S["li"], bulletText="•")
    return Paragraph(esc(line), S["p"])


def decorate(canvas, doc):
    w, h = A4
    canvas.saveState()
    canvas.setFillColor(TEAL)
    canvas.rect(0, h - 11, w, 11, stroke=0, fill=1)
    canvas.setStrokeColor(OCHRE)
    canvas.setLineWidth(0.8)
    canvas.line(18 * mm - 3, 17 * mm, w - 18 * mm + 3, 17 * mm)
    canvas.setFont("DV", 6.2)
    canvas.setFillColor(TEAL)
    canvas.drawString(18 * mm - 3, 13.5 * mm, FOOTER)
    canvas.drawRightString(w - 18 * mm, 13.5 * mm, str(doc.page))
    canvas.restoreState()


def build(src, out):
    w, h = A4
    margin = 18 * mm
    doc = BaseDocTemplate(str(out), pagesize=A4, leftMargin=margin, rightMargin=margin,
                          topMargin=19 * mm, bottomMargin=22 * mm,
                          title="Le Pays sous nos pieds — La rentrée des promesses — Bible V2.1",
                          author="Emmanuel Boujieka Kamga",
                          subject="Bible narrative et dossier de sources, volume 1 / Cameroun")
    frame = Frame(margin, 22 * mm, w - 2 * margin, h - 19 * mm - 22 * mm, id="f",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=decorate)])
    doc.build(parse(src, w - 2 * margin))


if __name__ == "__main__":
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "bible.txt"
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "Le_Pays_sous_nos_pieds_Bible_V2.1.pdf"
    build(src, out)
    print(out)
