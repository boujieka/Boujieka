"""KDP paperback interior for Book 7, Hydropower Development and Finance: 7 x 10 in (BOOK_TRIM=6x9 for 6 x 9), black ink on white paper, no bleed.

Run: python tools/book7/build_print7.py [--out book7/build/Hydropower_Development_and_Finance_7x10.pdf]
Before: python tools/book7/prepare7.py (text) and PRINT=1 python tools/book7/figures7.py (greyscale figures, figures_print/)

The text is the same as the A4 edition (book7/build/book7_resolved.md). The Markdown is converted with the helpers of
tools/house/publish_docs.py and rendered by the same browser engine, with a print stylesheet.

Pipeline
1. HTML: title page, copyright page, contents (h1 and h2 with page numbers), then the chapters; figures from figures_print/,
   each set at its natural size at 450 ppi (never enlarged), capped at the text width.
2. Render at the trim size with a symmetric margin equal to the mean of the inside and outside margins.
3. Locate every heading (hidden markers), plan a blank verso before every chapter that would open on a left hand page,
   and render again with the final page numbers in the contents; repeat until the plan is stable.
4. Insert the blank pages, shift each page sideways so that the inside (gutter) margin is wider than the outside margin
   (recto pages move right, verso pages move left), pad the page count to an even number.
5. Running heads (verso: book title; recto: chapter title) and folios at the outside corner, set in an embedded TrueType font.
   No heads on the title page, the copyright page, blank pages; folio only on chapter openings.
6. KDP clean up: no bookmarks, no link annotations, minimal document information.
7. Checks: every word inside the live area, fonts embedded (pdffonts), image resolution (pdfimages), text scan for dashes and
   banned words (tools/publish_docs.py).
"""
import argparse
import os
import base64
import html as htmlmod
import io
import re
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

import markdown
from PIL import Image
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import NameObject, NumberObject
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "house"))
import publish_docs as pd  # noqa: E402

BOOK = ROOT / "book7" / "build"
SRC = BOOK / "book7_resolved.md"
FIG_PRINT = BOOK / "figures_print"
# BOOK_TRIM=6x9 builds the 6 x 9 in edition (default 7x10); both meet the KDP minimum margins
TRIM_TAG = os.environ.get("BOOK_TRIM", "7x10")
OUT = BOOK / f"Hydropower_Development_and_Finance_{TRIM_TAG}.pdf"

# ---- page geometry (inches). KDP minimums for a paperback without bleed: outside, top and bottom at least 0.25 in;
# inside (gutter) 0.375 in for 24 to 150 pages, 0.5 in for 151 to 300, 0.625 in for 301 to 500, 0.75 in for 501 to 700,
# 0.875 in for 701 to 828. The values below exceed every minimum up to 700 pages, so a change in page count during copyedit
# does not force a new layout. See output/20_PRINT_PRODUCTION_NOTES.md for sources.
TRIM_W, TRIM_H = (6.0, 9.0) if TRIM_TAG == "6x9" else (7.0, 10.0)
INSIDE, OUTSIDE, TOP, BOTTOM = (0.75, 0.5, 0.75, 0.7) if TRIM_TAG == "6x9" else (0.75, 0.6, 0.85, 0.8)
HEAD_Y, FOLIO_Y = 0.5, 0.45          # baseline of the running head from the top edge, of the folio from the bottom edge
SIDE = (INSIDE + OUTSIDE) / 2         # symmetric render margin before the gutter shift
SHIFT = (INSIDE - OUTSIDE) / 2
TEXT_W = TRIM_W - INSIDE - OUTSIDE
FIG_PPI = 450
KDP_GUTTER = [(150, 0.375), (300, 0.5), (500, 0.625), (700, 0.75), (828, 0.875)]

FONT_DIR = Path("/usr/share/fonts/truetype/liberation")
pdfmetrics.registerFont(TTFont("LibSans", str(FONT_DIR / "LiberationSans-Regular.ttf")))
pdfmetrics.registerFont(TTFont("LibSansBold", str(FONT_DIR / "LiberationSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("LibSansItalic", str(FONT_DIR / "LiberationSans-Italic.ttf")))

INK, GREY, RULE, SHADE, SHADE2 = "#000000", "#555555", "#9A9A9A", "#DCDCDC", "#F1F1F1"
TITLE = "Hydropower Development and Finance"
SUBTITLE = "From River to Financial Close: A Developer, Lender and Government Framework for Hydropower Projects in Africa"
TAGLINE = "The Hydro Readiness Framework\u2122: 8 Questions \u00b7 23 Gates \u00b7 1 Financial Close Decision"
PARTIES = "Developer \u00b7 Lender \u00b7 Government"
EDITION = "First edition, version 1.0 release candidate 1 (pre-publication; print proof)"
ISBN_LINE = "ISBN-13: 979-8178961780 (paperback)"
IMPRINT = "Independently published"  # KDP-assigned ISBN; the imprint must read exactly as registered with KDP text

CSS = f"""
@page {{ size: {TRIM_W}in {TRIM_H}in; margin: {TOP}in {SIDE}in {BOTTOM}in {SIDE}in; }}
html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ font-family: 'Liberation Sans', Arial, sans-serif; font-size: 9.8pt; line-height: 1.45; color: {INK}; margin: 0; overflow-wrap: break-word; }}
h1 {{ font-size: 19pt; line-height: 1.2; border-bottom: 1.5pt solid {INK}; padding: 0.55in 0 5pt 0; margin: 0 0 12pt 0;
     break-before: page; page-break-before: always; }}
h2 {{ font-size: 13pt; margin: 16pt 0 6pt 0; border-left: 3pt solid {RULE}; padding-left: 7pt; break-after: avoid; page-break-after: avoid; }}
h3 {{ font-size: 11pt; margin: 12pt 0 4pt 0; color: {GREY}; break-after: avoid; page-break-after: avoid; }}
h4 {{ font-size: 10pt; margin: 8pt 0 2pt 0; break-after: avoid; }}
p, li {{ text-align: justify; hyphens: none; }}
p {{ orphans: 3; widows: 3; margin: 0 0 7pt 0; }}
table {{ border-collapse: collapse; width: 100%; margin: 6pt 0 10pt 0; font-size: 8.2pt; line-height: 1.3; }}
tr, img, blockquote {{ break-inside: avoid; page-break-inside: avoid; }}
thead {{ display: table-header-group; }}
th {{ background: {SHADE}; color: {INK}; padding: 3pt 4pt; text-align: left; font-weight: bold; border-bottom: 0.8pt solid {INK}; }}
td {{ border-bottom: 0.5pt solid #BDBDBD; padding: 2.5pt 4pt; vertical-align: top; overflow-wrap: anywhere; }}
td, th {{ text-align: left; hyphens: none; }}
tr:nth-child(even) td {{ background: {SHADE2}; }}
code {{ background: {SHADE2}; padding: 0 2pt; font-size: 8.6pt; }}
table.wide {{ font-size: 7pt; }}
table.wide th, table.wide td {{ overflow-wrap: anywhere; padding-left: 2pt; padding-right: 2pt; }}
pre {{ background: {SHADE2}; padding: 6pt; font-size: 8pt; white-space: pre-wrap; overflow-wrap: anywhere; }}
blockquote {{ background: {SHADE2}; border-left: 3pt solid {RULE}; margin: 8pt 0; padding: 4pt 10pt; }}
img {{ display: block; margin: 8pt auto 4pt auto; max-width: 100%; }}
figure {{ margin: 6pt 0 10pt 0; break-inside: avoid; page-break-inside: avoid; }}
figcaption {{ font-size: 8.4pt; line-height: 1.35; color: {INK}; text-align: left; margin-top: 3pt; }}
.mk {{ font-size: 1pt; color: white; }}
.titlepage {{ height: {TRIM_H - TOP - BOTTOM - 0.3}in; position: relative; break-after: page; page-break-after: always; text-align: left; }}
.titlepage .logo {{ width: 2.3in; }}
.titlepage .brand {{ letter-spacing: 2pt; font-weight: bold; font-size: 10pt; margin-top: 0.9in; color: {GREY}; }}
.titlepage .kicker {{ font-weight: bold; letter-spacing: 1.5pt; font-size: 10pt; margin-top: 0.25in; }}
.titlepage .title {{ font-size: 32pt; font-weight: bold; line-height: 1.08; margin: 0.15in 0 0.15in 0; border-top: 2pt solid {INK}; padding-top: 0.15in; }}
.titlepage .subtitle {{ font-size: 14pt; line-height: 1.3; max-width: 4.8in; }}
.titlepage .tagline {{ font-size: 10.5pt; font-weight: bold; margin-top: 0.22in; letter-spacing: 0.3pt; }}
.titlepage .parties {{ font-size: 10pt; letter-spacing: 1.2pt; margin-top: 0.08in; color: {GREY}; }}
.titlepage .author {{ font-size: 15pt; font-weight: bold; margin-top: 0.6in; }}
.titlepage .foot {{ position: absolute; bottom: 0; font-size: 9pt; color: {GREY}; }}
.copyright {{ height: {TRIM_H - TOP - BOTTOM - 0.3}in; position: relative; break-after: page; page-break-after: always; }}
.copyright .block {{ position: absolute; bottom: 0; font-size: 8.4pt; line-height: 1.45; }}
.copyright p {{ text-align: left; margin: 0 0 6pt 0; }}
.toc {{ break-after: page; page-break-after: always; }}
.toc h2 {{ border: none; padding: 0.55in 0 0 0; font-size: 19pt; margin: 0 0 10pt 0; }}
.toc .row {{ display: flex; align-items: baseline; margin: 1.5pt 0; }}
.toc .row a {{ color: {INK}; text-decoration: none; }}
.toc .row .dots {{ flex: 1; border-bottom: 0.6pt dotted #777; margin: 0 4pt; transform: translateY(-2.5pt); }}
.toc .row .pg {{ min-width: 16pt; text-align: right; }}
.toc .l1 {{ font-weight: bold; margin-top: 6pt; font-size: 9.6pt; }}
.toc .l2 {{ padding-left: 14pt; font-size: 8.8pt; }}
"""


def _img_tag_size(path):
    """Width in inches at which a print figure is set: natural size at FIG_PPI, never enlarged, capped at the text width."""
    w_px, _ = Image.open(path).size
    return min(w_px / FIG_PPI, TEXT_W)


def _grey_logo():
    im = Image.open(ROOT / "brand/aef_logo.png").convert("RGBA")
    bg = Image.new("RGBA", im.size, "white")
    bg.alpha_composite(im)
    buf = io.BytesIO()
    bg.convert("L").save(buf, "PNG", dpi=(600, 600))
    return base64.b64encode(buf.getvalue()).decode()


def build_html(md_text, pages=None, markers=False):
    md = markdown.Markdown(extensions=["tables", "toc", "fenced_code", "attr_list", "sane_lists"],
                           extension_configs={"toc": {"toc_depth": "1-2"}})
    body = md.convert(pd._prep_markdown(md_text))
    heads = [h for h in pd._flatten(md.toc_tokens) if h[0] <= 2]
    if markers:
        for i, (_, hid, _) in enumerate(heads):
            body = re.sub(rf'(<h[12][^>]*id="{re.escape(hid)}"[^>]*>)', rf'\1<span class="mk">QQH{i:03d}QQ</span>', body, count=1)
    missing = []
    for img in sorted(set(re.findall(r'src="([^"]+\.png)"', body))):
        p = FIG_PRINT / Path(img).name
        if not p.exists():
            missing.append(img)
            continue
        w_in = _img_tag_size(p)
        body = body.replace(f'src="{img}"', f'style="width:{w_in:.3f}in" src="data:image/png;base64,{base64.b64encode(p.read_bytes()).decode()}"')
    # very wide tables (8 columns or more) set smaller and may break long words, so that no table is wider than the text
    # block (Chromium would otherwise shrink every page to fit the widest element)
    def _wide(m):
        head = re.search(r"<tr>(.*?)</tr>", m.group(0), re.S)
        n = len(re.findall(r"<th", head.group(1))) if head else 0
        return m.group(0).replace("<table>", '<table class="wide">', 1) if n >= 8 else m.group(0)
    body = re.sub(r"<table>.*?</table>", _wide, body, flags=re.S)
    # the figure caption lives in the Markdown alt text: print it under the figure (alt text alone is invisible on paper)
    body = re.sub(r'<p>(<img [^>]*alt="([^"]+)"[^>]*>)</p>',
                  lambda m: f'<figure>{m.group(1)}<figcaption>{m.group(2)}</figcaption></figure>', body)
    if missing:
        raise SystemExit(f"print figures missing (run PRINT=1 tools/book7/figures7.py): {missing}")
    rows = []
    for i, (lvl, hid, name) in enumerate(heads):
        pg = str(pages[i]) if pages else "00"
        rows.append(f'<div class="row l{lvl}"><a href="#{hid}">{htmlmod.escape(name)}</a><span class="dots"></span><span class="pg">{pg}</span></div>')
    year = date.today().year
    front = f"""
<div class="titlepage">
  <img class="logo" src="data:image/png;base64,{_grey_logo()}">
  <div class="brand">AFRICA ENERGY FINANCE</div>
  <div class="kicker">BOOK 7</div>
  <div class="title">{htmlmod.escape(TITLE)}</div>
  <div class="subtitle">{htmlmod.escape(SUBTITLE)}</div>
  <div class="tagline">{htmlmod.escape(TAGLINE)}</div>
  <div class="parties">{htmlmod.escape(PARTIES)}</div>
  <div class="author">{pd.AUTHOR}</div>
  <div class="foot">{pd.HOUSE} &nbsp;|&nbsp; {pd.SERIES.replace('&', '&amp;')}</div>
</div>
<div class="copyright"><div class="block">
  <p><b>{htmlmod.escape(TITLE)}</b><br>{htmlmod.escape(SUBTITLE)}</p>
  <p>{htmlmod.escape(EDITION)}</p>
  <p>&copy; {year} {pd.AUTHOR}. All rights reserved. No part of this publication may be reproduced, stored or transmitted
  in any form without the prior written permission of the author, except for short quotations in reviews and scholarly work.</p>
  <p>Decision support material; not investment, legal, tax or accounting advice. The default model inputs and the Kasiri
  River Hydro case are fictional and illustrative. Hydro Readiness Framework is used as a trademark of the author; registration
  status to be confirmed before publication.</p>
  <p>{htmlmod.escape(ISBN_LINE)}<br>{htmlmod.escape(IMPRINT)}</p>
  <p>{pd.HOUSE}: {pd.SERIES.replace('&', '&amp;')}, Book 7</p>
</div></div>
<div class="toc"><h2>Contents</h2>{''.join(rows)}</div>
"""
    doc = f"<html><head><meta charset='utf-8'><title>{htmlmod.escape(TITLE)}</title><style>{CSS}</style></head><body>{front}{body}</body></html>"
    return doc, heads


def render(doc, out_pdf):
    exe = (sorted(Path("/opt/pw-browsers").glob("chromium-*/chrome-linux/chrome")) or [None])[0]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=str(exe)) if exe else p.chromium.launch()
        pg = b.new_page()
        pg.set_content(doc, wait_until="load")
        pg.pdf(path=str(out_pdf), width=f"{TRIM_W}in", height=f"{TRIM_H}in", print_background=True,
               display_header_footer=False, prefer_css_page_size=True)
        b.close()


def plan_blanks(heads, pages):
    """Pages (in the rendered PDF, 1 based) before which a blank verso is inserted so that every h1 opens on a recto."""
    blanks, offset = [], 0
    for (lvl, _, _), p in sorted(zip(heads, pages), key=lambda t: t[1]):
        if lvl == 1 and (p + offset) % 2 == 0 and p not in blanks:
            blanks.append(p)
            offset += 1
    return blanks


def final_pages(pages, blanks):
    return [p + sum(1 for b in blanks if b <= p) for p in pages]


def assemble_pdf(src_pdf, blanks):
    """Insert blank versos, pad to an even count; returns the writer and the list of physical pages that are blank."""
    reader = PdfReader(str(src_pdf))
    w = PdfWriter()
    blank_pages = []
    for i, page in enumerate(reader.pages):
        if (i + 1) in blanks:
            w.add_blank_page(TRIM_W * 72, TRIM_H * 72)
            blank_pages.append(len(w.pages))
        w.add_page(page)
    if len(w.pages) % 2:
        w.add_blank_page(TRIM_W * 72, TRIM_H * 72)
        blank_pages.append(len(w.pages))
    return w, blank_pages


def _fit(c, text, font, size, width):
    if c.stringWidth(text, font, size) <= width:
        return text
    words = text.split()
    while words and c.stringWidth(" ".join(words) + "…", font, size) > width:
        words.pop()
    return " ".join(words).rstrip(",:;") + "…"


def stamp(writer, blank_pages, heads, fpages):
    h1 = sorted((p, name) for (lvl, _, name), p in zip(heads, fpages) if lvl == 1)
    openings = {p for p, _ in h1}
    first_body = h1[0][0]
    for i, page in enumerate(writer.pages):
        n = i + 1
        recto = n % 2 == 1
        tx = SHIFT * 72 if recto else -SHIFT * 72
        if n not in blank_pages:
            page.add_transformation(Transformation().translate(tx, 0))
        if n <= 2 or n in blank_pages:
            continue
        w, h = TRIM_W * 72, TRIM_H * 72
        left = (INSIDE if recto else OUTSIDE) * 72
        right = w - (OUTSIDE if recto else INSIDE) * 72
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=(w, h), initialFontName="LibSans", initialFontSize=8.5)
        c.setFillColor(HexColor(INK))
        c.setFont("LibSans", 8.5)
        folio = str(n)
        if recto:
            c.drawRightString(right, FOLIO_Y * 72, folio)
        else:
            c.drawString(left, FOLIO_Y * 72, folio)
        if n not in openings:
            if n < first_body:
                head = "Contents"
            else:
                head = TITLE if not recto else next(name for p, name in reversed(h1) if p <= n)
            font = "LibSansItalic"
            c.setFillColor(HexColor(GREY))
            c.setFont(font, 8)
            text = _fit(c, head, font, 8, right - left)
            if recto:
                c.drawRightString(right, h - HEAD_Y * 72, text)
            else:
                c.drawString(left, h - HEAD_Y * 72, text)
            c.setStrokeColor(HexColor(RULE))
            c.setLineWidth(0.4)
            c.line(left, h - (HEAD_Y + 0.09) * 72, right, h - (HEAD_Y + 0.09) * 72)
        c.save()
        buf.seek(0)
        page.merge_page(PdfReader(buf).pages[0])
    for page in writer.pages:
        for img in page.images:  # the browser stores the grey figures as RGB: put them back to one grey channel
            pil = img.image
            if pil.mode in ("RGB", "RGBA"):
                rgb = pil.convert("RGB")
                r, g, b = rgb.split()
                if r.tobytes() == g.tobytes() == b.tobytes():
                    obj = img.indirect_reference.get_object()
                    obj.pop("/DecodeParms", None)
                    obj[NameObject("/Filter")] = NameObject("/FlateDecode")
                    obj[NameObject("/ColorSpace")] = NameObject("/DeviceGray")
                    obj[NameObject("/BitsPerComponent")] = NumberObject(8)
                    obj.set_data(r.tobytes())  # pypdf encodes with the stream's own filter: lossless, one channel
        if "/Annots" in page:
            del page["/Annots"]
    writer._root_object.pop("/Outlines", None)
    writer.add_metadata({"/Title": TITLE, "/Author": pd.AUTHOR, "/Creator": pd.HOUSE, "/Producer": pd.HOUSE})


def live_area_check(pdf):
    """Every word must sit inside the live area: text block plus the running head and folio lines; returns problems.
    Tolerance 1.5 pt: pdftotext word boxes include the glyph side bearings of justified text set flush to the margin."""
    out = subprocess.run(["pdftotext", "-bbox", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    problems, n = [], 0
    for page in re.findall(r"<page [^>]*>(.*?)</page>", out, flags=re.S):
        n += 1
        recto = n % 2 == 1
        lo = (INSIDE if recto else OUTSIDE) * 72 - 1.5
        hi = (TRIM_W - (OUTSIDE if recto else INSIDE)) * 72 + 1.5
        for x0, y0, x1, y1, word in re.findall(r'xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)<', page):
            x0, y0, x1, y1 = map(float, (x0, y0, x1, y1))
            if word.startswith("QQH"):
                continue
            if x0 < lo or x1 > hi or y0 < 0.3 * 72 or y1 > (TRIM_H - 0.3) * 72:
                problems.append(f"p{n} '{word}' x {x0:.0f} to {x1:.0f}")
    return problems


def fonts_check(pdf):
    out = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True, check=True).stdout
    lines = out.strip().split("\n")[2:]
    not_emb = [l for l in lines if l.split()[-5] != "yes"]
    return len(lines), not_emb, out


def images_check(pdf):
    out = subprocess.run(["pdfimages", "-list", str(pdf)], capture_output=True, text=True, check=True).stdout
    rows = [l.split() for l in out.strip().split("\n")[2:]]
    res = []
    for r in rows:
        if r[2] in ("image",):
            res.append((int(r[0]), r[5], int(r[3]), int(r[4]), int(r[12]), int(r[13])))  # page, colour, w, h, x-ppi, y-ppi
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    md_text = SRC.read_text(encoding="utf-8")
    md_text = re.sub(r'\{: style="[^"]*"\}', "", md_text)  # print sets every figure at its natural size
    with tempfile.TemporaryDirectory() as td:
        p1 = Path(td) / "pass1.pdf"
        doc, heads = build_html(md_text, markers=True)
        render(doc, p1)
        raw = pd.locate(p1, len(heads))
        blanks = plan_blanks(heads, raw)
        fp = final_pages(raw, blanks)
        for attempt in range(3):
            p2 = Path(td) / f"pass{attempt + 2}.pdf"
            doc, _ = build_html(md_text, pages=fp)
            render(doc, p2)
            texts = pd.page_texts(p2)
            norm = lambda s: re.sub(r"\s+", " ", s)
            ok = all(norm(name)[:40] in norm(texts[p - 1]) for (_, _, name), p in zip(heads, raw))
            if ok:
                break
            # the contents changed length or the flow moved: locate again with markers and replan
            doc_m, _ = build_html(md_text, pages=fp, markers=True)
            render(doc_m, p1)
            raw = pd.locate(p1, len(heads))
            blanks = plan_blanks(heads, raw)
            fp = final_pages(raw, blanks)
        else:
            raise SystemExit("page plan did not converge")
        writer, blank_pages = assemble_pdf(p2, blanks)
        stamp(writer, blank_pages, heads, fp)
        for page in writer.pages:
            page.compress_content_streams(level=9)
        writer.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)
        with open(a.out, "wb") as f:
            writer.write(f)
    n = len(PdfReader(a.out).pages)
    print(a.out, f"{n} pages ({len(blank_pages)} blank), trim {TRIM_W} x {TRIM_H} in")
    need = next(g for top, g in KDP_GUTTER if n <= top)
    print(f"gutter {INSIDE} in (KDP minimum for {n} pages: {need} in); outside {OUTSIDE} in, top {TOP} in, bottom {BOTTOM} in")
    assert INSIDE >= need and min(OUTSIDE, TOP, BOTTOM, HEAD_Y, FOLIO_Y) >= 0.25
    texts = pd.page_texts(a.out)
    norm = lambda s: re.sub(r"\s+", " ", s)
    bad = [name for (_, _, name), p in zip(heads, fp) if norm(name)[:40] not in norm(texts[p - 1])]
    print("contents page numbers:", "all headings on their listed page" if not bad else f"MISMATCH {bad[:5]}")
    opens = [p for (lvl, _, _), p in zip(heads, fp) if lvl == 1]
    print("chapter openings on recto:", all(p % 2 == 1 for p in opens), f"({len(opens)} openings)")
    live = live_area_check(a.out)
    print("live area:", "every word inside the margins" if not live else f"{len(live)} words outside: {live[:8]}")
    nf, not_emb, _ = fonts_check(a.out)
    print(f"fonts: {nf} font objects, not embedded: {len(not_emb)}")
    imgs = images_check(a.out)
    low = [i for i in imgs if min(i[4], i[5]) < 300]
    print(f"images: {len(imgs)}, colour spaces {sorted(set(i[1] for i in imgs))}, lowest ppi {min(min(i[4], i[5]) for i in imgs)}"
          + (f", BELOW 300: {low}" if low else ""))
    front_ok = "All rights reserved" in texts[1] and "Contents" in texts[2] and not texts[0].count("All rights reserved")
    print("front matter: title p1, copyright p2, contents p3:", front_ok)
    figs = {Image.open(f).size: f for f in FIG_PRINT.glob("*.png")}
    same, checked = 0, 0
    for page in PdfReader(a.out).pages:
        for im in page.images:
            if im.image.size in figs:
                checked += 1
                same += im.image.convert("L").tobytes() == Image.open(figs[im.image.size]).convert("L").tobytes()
    expected = len(set(re.findall(r"!\[[^\]]*\]\(([^)]+)\)", md_text)))
    print(f"figures placed pixel for pixel identical to figures_print/: {same} of {checked} (expected {expected})")
    issues = pd.scan(a.out)
    if issues or bad or live or not_emb or low or not front_ok or same != expected:
        print("TEXT SCAN:", "; ".join(issues) if issues else "clean")
        sys.exit(2)
    print("text scan clean")


if __name__ == "__main__":
    main()
