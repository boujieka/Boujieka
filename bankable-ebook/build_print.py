"""Print interior for KDP paperback (6 x 9 in, no bleed) from pandoc's HTML of the manuscript.

usage: build_print.py body.html fonts_dir out.pdf
body.html: pandoc -t html5 --section-divs with kindle.lua (BOOK_ISBN set) and print_notes.lua.
"""
import html
import os
import re
import sys

from weasyprint import HTML

body_path, fonts, out = sys.argv[1:4]
body = open(body_path, encoding="utf-8").read()

# ---- page classes: plain (title, copyright, contents), front (roman), main (arabic from Part I)
sections = list(re.finditer(r'<section(\s+id="[^"]*")?\s+class="level1([^"]*)"', body))
first_part = next(m.start() for m in sections if "part" in m.group(2))
out_parts, last, part_n = [], 0, 0
for m in sections:
    cls = m.group(2)
    if "hidden" in cls:
        pg = "pg-plain"
    elif m.start() < first_part:
        pg = "pg-front"
    else:
        pg = "pg-main"
    ident = m.group(1) or ""
    if "part" in cls:
        part_n += 1
        ident = f' id="part-{part_n}"'
        if part_n == 1:
            pg += " body-start"
    out_parts.append(body[last:m.start()])
    out_parts.append(f'<section{ident} class="level1{cls} {pg}"')
    last = m.end()
out_parts.append(body[last:])
body = "".join(out_parts)

F = lambda n: "file://" + os.path.abspath(os.path.join(fonts, n))
css = f"""
@font-face {{ font-family: Charis; src: url({F('CharisSIL-Regular.ttf')}); font-weight: normal; font-style: normal; }}
@font-face {{ font-family: Charis; src: url({F('CharisSIL-Italic.ttf')}); font-weight: normal; font-style: italic; }}
@font-face {{ font-family: Charis; src: url({F('CharisSIL-Bold.ttf')}); font-weight: bold; font-style: normal; }}
@font-face {{ font-family: Charis; src: url({F('CharisSIL-BoldItalic.ttf')}); font-weight: bold; font-style: italic; }}

@page {{ size: 6in 9in; margin: 0.8in 0.6in 0.8in 0.875in;
  @footnote {{ border-top: 0.5pt solid #000; padding-top: 4pt; margin-top: 8pt; }} }}
@page :left {{ margin-left: 0.6in; margin-right: 0.875in; }}
@page :right {{ margin-left: 0.875in; margin-right: 0.6in; }}

@page pg-front {{ @bottom-center {{ content: counter(page, lower-roman); font: 9pt Charis; }} }}
@page pg-front:left {{ @top-left {{ content: "BANKABLE IS NOT ENOUGH"; font: 7.5pt Charis; letter-spacing: 1.2pt; }} }}
@page pg-front:right {{ @top-right {{ content: string(runhead, first-except); font: italic 8.5pt Charis; }} }}
@page pg-main {{ @bottom-center {{ content: counter(page); font: 9pt Charis; }} }}
@page pg-main:left {{ @top-left {{ content: "BANKABLE IS NOT ENOUGH"; font: 7.5pt Charis; letter-spacing: 1.2pt; }} }}
@page pg-main:right {{ @top-right {{ content: string(runhead, first-except); font: italic 8.5pt Charis; }} }}
@page pg-front:blank {{ @top-left {{ content: none; }} @top-right {{ content: none; }} @bottom-center {{ content: none; }} }}
@page pg-main:blank {{ @top-left {{ content: none; }} @top-right {{ content: none; }} @bottom-center {{ content: none; }} }}
@page pg-plain:blank {{ @top-left {{ content: none; }} @top-right {{ content: none; }} @bottom-center {{ content: none; }} }}

html {{ font-family: Charis, serif; font-size: 10.5pt; line-height: 1.38; hyphens: auto; }}
body {{ margin: 0; }}
section.pg-plain {{ page: pg-plain; }}
section.pg-front {{ page: pg-front; }}
section.pg-main {{ page: pg-main; }}

p {{ margin: 0 0 0.55em 0; text-align: justify; orphans: 2; widows: 2; }}
h1, h2, h3, h4 {{ font-weight: bold; line-height: 1.2; break-after: avoid; text-align: left; hyphens: manual; }}
h3 {{ font-size: 12pt; margin: 1.3em 0 0.5em 0; }}
h4 {{ font-size: 10.5pt; margin: 1.1em 0 0.4em 0; }}

/* front matter and back matter openings */
section.level1 {{ break-before: page; }}
section.level1 > h1 {{ font-size: 20pt; margin: 0.6in 0 0.35in 0; string-set: runhead content(); }}
h1.hidden {{ display: none; }}

/* parts: a recto page of their own */
section.part {{ break-before: right; }}
h1.part {{ font-size: 22pt; text-align: center; margin: 2.4in 0 0 0; break-after: page; letter-spacing: 0.5pt; }}

/* chapters open on a recto */
section.chapter {{ break-before: right; }}
h2.chapter {{ font-size: 19pt; margin: 0.9in 0 0.12in 0; string-set: runhead content(); }}
div.kicker p {{ font-size: 8.5pt; text-transform: uppercase; letter-spacing: 1.2pt; color: #444; margin: 0 0 0.1in 0; text-align: left; }}
div.byline p {{ font-style: italic; color: #444; margin: 0 0 0.35in 0; text-align: left; }}

/* title and copyright */
div.titlepage {{ text-align: center; padding-top: 1.6in; }}
div.titlepage p {{ text-align: center; margin: 0 0 0.22in 0; }}
div.titlepage p:first-child {{ font-size: 24pt; line-height: 1.15; margin-bottom: 0.3in; }}
div.titlepage p:last-child {{ margin-top: 0.8in; font-size: 12pt; letter-spacing: 1pt; }}
div.copyright {{ font-size: 8pt; line-height: 1.35; padding-top: 3.2in; }}
div.copyright p {{ text-align: left; margin-bottom: 0.7em; }}

/* contents */
section.toc-page {{ break-before: right; }}
h1.toc-title {{ font-size: 20pt; margin: 0.6in 0 0.3in 0; }}
ul.toc {{ list-style: none; margin: 0; padding: 0; font-size: 10pt; }}
ul.toc li {{ margin: 0 0 3pt 0; }}
ul.toc a {{ color: #000; text-decoration: none; }}
ul.toc li a::after {{ content: leader('.') attr(data-p); }}
ul.toc li.fm a::after {{ content: leader('.') target-counter(attr(href), page, lower-roman); }}
ul.toc li.toc-part {{ font-weight: bold; margin-top: 9pt; }}
ul.toc li.toc-ch {{ padding-left: 1.2em; }}

/* tables */
table {{ border-collapse: collapse; width: 100%; margin: 0.6em 0 0.9em 0; font-size: 7.6pt; line-height: 1.25; }}
th, td {{ border: 0.5pt solid #555; padding: 2.5pt 3.5pt; vertical-align: top; text-align: left; hyphens: auto; }}
th {{ font-weight: bold; background: #eeeeee; }}
tr {{ break-inside: avoid; }}
td p, th p {{ margin: 0; text-align: left; }}
caption {{ font-size: 8.5pt; font-style: italic; }}

blockquote {{ margin: 0.6em 1.2em; font-size: 10pt; }}
ul, ol {{ margin: 0 0 0.6em 0; padding-left: 1.4em; }}
li {{ margin-bottom: 0.2em; }}
a {{ color: #000; text-decoration: none; overflow-wrap: anywhere; }}

/* footnotes at the foot of the page */
span.fn {{ float: footnote; font-size: 7.8pt; line-height: 1.3; text-align: left; font-style: normal; font-weight: normal; }}
::footnote-call {{ font-size: 70%; vertical-align: super; line-height: 0; }}
::footnote-marker {{ font-size: 7.8pt; }}
"""

# ---- split: front matter (roman) and body from Part I (arabic, starts at 1)
split_at = body.index('<section id="part-1"')
front_html, main_html = body[:split_at], body[split_at:]

def render(fragment):
    doc = f"""<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8"/>
<title>Bankable Is Not Enough</title><style>{css}</style></head><body>{fragment}</body></html>"""
    return HTML(string=doc, base_url=os.path.dirname(os.path.abspath(body_path))).render(), doc

def toc_html(page_of):
    items = []
    for m in re.finditer(r'<section\s+id="([^"]*)"\s+class="(level1|level2)([^"]*)"[^>]*>\s*<h[12][^>]*>(.*?)</h[12]>', body, re.S):
        ident, level, cls, title = m.groups()
        if "hidden" in cls:
            continue
        text = re.sub(r"<[^>]+>", "", title).strip()
        kind = "toc-part" if "part" in cls else ("toc-ch" if level == "level2" else ("toc-fm" if "pg-front" in cls else "toc-top"))
        if ident in page_of:
            items.append(f'<li class="{kind}"><a href="#{ident}" data-p="{page_of[ident]}">{text}</a></li>')
        else:
            items.append(f'<li class="{kind} fm"><a href="#{ident}">{text}</a></li>')
    return ('<section id="contents" class="level1 pg-plain toc-page"><h1 class="toc-title">Contents</h1><ul class="toc">'
            + "".join(items) + "</ul></section>")

main_doc, main_src = render(main_html)
page_of = {}
for i, pg in enumerate(main_doc.pages, 1):
    for a in pg.anchors:
        page_of.setdefault(a, i)
cp = front_html.index('<section id="preface"')
front_html = front_html[:cp] + toc_html(page_of) + front_html[cp:]
front_doc, front_src = render(front_html)
open(out.replace(".pdf", ".html"), "w", encoding="utf-8").write(front_src + main_src)

from pypdf import PdfReader, PdfWriter
import io
w = PdfWriter()
for part in (front_doc, main_doc):
    buf = io.BytesIO(); part.write_pdf(buf); buf.seek(0)
    r = PdfReader(buf)
    for p in r.pages:
        w.add_page(p)
    if part is front_doc and len(r.pages) % 2:
        w.add_blank_page(width=6 * 72, height=9 * 72)  # Part I must open on a right-hand page
w.add_metadata({"/Title": "Bankable Is Not Enough", "/Author": "Emmanuel Boujieka Kamga"})
with open(out, "wb") as f:
    w.write(f)
print("wrote", out, "front", len(front_doc.pages), "main", len(main_doc.pages))
