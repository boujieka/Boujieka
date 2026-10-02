"""Publish a Markdown document as a branded A4 PDF (Africa Energy Finance house style).

Run: python tools/publish_docs.py <source.md> <out.pdf> --title "..." --subtitle "..." [--kicker "..."]
Pipeline: Markdown -> HTML (brand CSS, cover page, table of contents) -> PDF with Chromium (page numbers in footer).
Images referenced in the Markdown are resolved relative to the source file.
"""
import argparse
import base64
import glob
from datetime import date
from pathlib import Path

import markdown
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
GREEN, GOLD, CREAM = "#0B3020", "#B07C0F", "#F7F3E8"
AUTHOR = "Emmanuel Boujieka Kamga"

CSS = f"""
@page {{ size: A4; margin: 22mm 18mm 20mm 18mm; }}
body {{ font-family: 'Liberation Sans', Arial, sans-serif; font-size: 10.2pt; line-height: 1.5; color: #1d1d1d; }}
h1 {{ color: {GREEN}; font-size: 20pt; border-bottom: 3px solid {GOLD}; padding-bottom: 4px; margin-top: 0; page-break-before: always; }}
h1.first {{ page-break-before: avoid; }}
h2 {{ color: {GREEN}; font-size: 14pt; margin-top: 18px; border-left: 4px solid {GOLD}; padding-left: 8px; }}
h3 {{ color: {GOLD}; font-size: 11.5pt; margin-top: 14px; margin-bottom: 4px; }}
h4 {{ color: {GREEN}; font-size: 10.5pt; margin-bottom: 2px; }}
p, li {{ text-align: justify; }}
table {{ border-collapse: collapse; width: 100%; margin: 8px 0 12px 0; font-size: 8.8pt; page-break-inside: avoid; }}
th {{ background: {GREEN}; color: white; padding: 4px 6px; text-align: left; font-weight: bold; }}
td {{ border-bottom: 1px solid #ddd; padding: 3px 6px; vertical-align: top; }}
tr:nth-child(even) td {{ background: #faf8f2; }}
code {{ background: #f2f2f2; padding: 0 3px; font-size: 9pt; }}
pre {{ background: #f6f6f6; padding: 8px; font-size: 8.5pt; overflow-x: hidden; white-space: pre-wrap; }}
blockquote {{ background: {CREAM}; border-left: 4px solid {GOLD}; margin: 10px 0; padding: 6px 12px; }}
img {{ max-width: 100%; display: block; margin: 8px auto; }}
.toc {{ page-break-after: always; }}
.toc ul {{ list-style: none; padding-left: 14px; }}
.toc > ul {{ padding-left: 0; }}
.toc a {{ color: {GREEN}; text-decoration: none; }}
.toc li {{ margin: 2px 0; text-align: left; }}
.cover {{ height: 247mm; position: relative; page-break-after: always; }}
.cover .logo {{ width: 120mm; margin: 6mm 0 0 0; }}
.cover .panel {{ position: absolute; top: 72mm; left: -18mm; right: -18mm; background: {GREEN}; color: white;
               padding: 14mm 18mm 12mm 18mm; border-top: 4px solid {GOLD}; border-bottom: 4px solid {GOLD}; }}
.cover .kicker {{ color: {GOLD}; font-weight: bold; letter-spacing: 1px; font-size: 11pt; }}
.cover .title {{ font-size: 28pt; font-weight: bold; margin: 6mm 0 3mm 0; line-height: 1.15; }}
.cover .subtitle {{ font-size: 15pt; margin-bottom: 8mm; }}
.cover .label {{ color: {GOLD}; font-size: 8.5pt; font-weight: bold; letter-spacing: 1px; margin-top: 6mm; }}
.cover .author {{ font-size: 14pt; font-weight: bold; }}
.cover .meta {{ color: #d9d9d9; font-size: 9.5pt; margin-top: 5mm; }}
.cover .foot {{ position: absolute; bottom: 0; font-size: 8pt; color: #666; text-align: left; }}
.note {{ font-size: 8.5pt; color: #555; font-style: italic; }}
"""


def build_html(md_path, title, subtitle, kicker):
    src = Path(md_path)
    text = src.read_text(encoding="utf-8")
    # Python-Markdown needs a blank line before a list that follows a paragraph line
    import re as _re
    lines, out = text.split("\n"), []
    is_item = lambda l: bool(_re.match(r"^\s*([-*]|\d+\.)\s+", l))
    for i, l in enumerate(lines):
        m_ = _re.match(r"^( {2,3})(?=([-*]|\d+\.)\s|\|)", l)
        if m_:  # nested items / tables under a list item need a 4-space indent
            l = "    " + l.lstrip(" ")
        if is_item(l) and out and out[-1].strip() and not is_item(out[-1]) and not out[-1].startswith(("|", "    ", "\t", ">")):
            out.append("")
        out.append(l)
    text = "\n".join(out)
    md = markdown.Markdown(extensions=["tables", "toc", "fenced_code", "attr_list", "sane_lists"],
                           extension_configs={"toc": {"toc_depth": "1-2"}})
    body = md.convert(text)
    body = body.replace("<h1", "<h1 class=\"first\"", 1)
    # inline images so Chromium can load them from a data URI
    for img in set(__import__("re").findall(r'src="([^"]+\.png)"', body)):
        p = (src.parent / img).resolve()
        if p.exists():
            body = body.replace(f'src="{img}"', f'src="data:image/png;base64,{base64.b64encode(p.read_bytes()).decode()}"')
    logo = base64.b64encode((ROOT / "brand" / "aef_logo.png").read_bytes()).decode()
    cover = f"""
<div class="cover">
  <img class="logo" src="data:image/png;base64,{logo}">
  <div class="panel">
    <div class="kicker">{kicker}</div>
    <div class="title">{title}</div>
    <div class="subtitle">{subtitle}</div>
    <div class="label">AUTHOR &amp; IDEATION</div>
    <div class="author">{AUTHOR}</div>
    <div class="meta">Africa Energy Finance - Business &amp; Financial Models &nbsp;|&nbsp; {date.today().strftime('%B %Y')}</div>
  </div>
  <div class="foot">(c) {date.today().year} {AUTHOR}. All rights reserved. Decision-support material - not investment, legal,
  tax or accounting advice. Default model inputs and the SolaraPay case are fictional and illustrative.</div>
</div>
<div class="toc"><h2 style="border:none;padding:0">Contents</h2>{md.toc}</div>
"""
    return f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{cover}{body}</body></html>"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--title", required=True); ap.add_argument("--subtitle", default=""); ap.add_argument("--kicker", default="VOLUME 2")
    a = ap.parse_args()
    html = build_html(a.src, a.title, a.subtitle, a.kicker)
    Path(a.out).with_suffix(".html").write_text(html, encoding="utf-8")
    exe = (glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome") or [None])[0]
    footer = (f"<div style='font-size:7pt;width:100%;padding:0 18mm;color:#777;font-family:Arial;display:flex;justify-content:space-between'>"
              f"<span>{a.title}</span><span><span class='pageNumber'></span> / <span class='totalPages'></span></span></div>")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        pg = b.new_page()
        pg.set_content(html, wait_until="load")
        pg.pdf(path=a.out, format="A4", print_background=True, display_header_footer=True,
               header_template="<div></div>", footer_template=footer,
               margin={"top": "20mm", "bottom": "18mm", "left": "18mm", "right": "18mm"})
        b.close()
    Path(a.out).with_suffix(".html").unlink()
    print(a.out)


if __name__ == "__main__":
    main()
