"""Test EPUB (reflowable) of Book 2, PAYGo Solar Finance, for the Kindle conversion check.

Run: python tools/build_book2_kindle.py [--out output/20_BOOK2_KINDLE_test.epub] [--tables output/20_BOOK2_KINDLE_wide_tables.csv]
The text is the same as the print and A4 editions (tools/build_book2.py, assemble). One XHTML file per h1 section, the
15 colour figures from book/figures/ with their captions as visible captions and as alt text, contents (nav and NCX), and a
cover image cut from the front of the draft print cover (output/20_BOOK2_COVER_7x10_draft.pdf) when it exists.
Tables stay HTML tables, as the Kindle guidelines ask (an image of a table cannot be paginated or read aloud); the script
lists the tables that will not reflow well on a phone screen, with a proposed treatment, and runs epubcheck when installed.
This is a test file: it is not the upload file (the cover, the ISBN page and the edition text are still drafts).
"""
import argparse
import csv
import html as htmlmod
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown
from ebooklib import epub
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_book2  # noqa: E402
import publish_docs as pd  # noqa: E402

ROOT = build_book2.ROOT
FIG = build_book2.BOOK / "figures"
OUT = ROOT / "output/20_BOOK2_KINDLE_test.epub"
TABLES = ROOT / "output/20_BOOK2_KINDLE_wide_tables.csv"
COVER_PDF = ROOT / "output/20_BOOK2_COVER_7x10_draft.pdf"

CSS = """
body { font-family: serif; line-height: 1.4; }
h1 { font-size: 1.5em; margin: 0 0 0.8em 0; page-break-before: always; }
h2 { font-size: 1.2em; margin: 1.2em 0 0.4em 0; }
h3 { font-size: 1.05em; margin: 1em 0 0.3em 0; }
p { margin: 0 0 0.6em 0; text-indent: 0; }
table { border-collapse: collapse; width: 100%; margin: 0.6em 0 1em 0; font-size: 0.85em; }
th { text-align: left; border-bottom: 2px solid #000; padding: 0.2em 0.3em; vertical-align: bottom; }
td { text-align: left; border-bottom: 1px solid #999; padding: 0.2em 0.3em; vertical-align: top; }
blockquote { margin: 0.6em 1em; font-style: italic; }
figure { margin: 1em 0; }
figure img { width: 100%; max-width: 100%; }
figcaption { font-size: 0.85em; margin-top: 0.3em; }
pre, code { font-family: monospace; font-size: 0.85em; white-space: pre-wrap; }
"""

# phone portrait: about 30 to 40 characters of body text per line at a default font size; a table row that needs much more
# than that per column, or more than 4 columns, has to scroll sideways or wraps into very narrow columns
PHONE_CHARS = 36


def slug(i, name):
    return f"s{i:02d}_" + re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")[:40] + ".xhtml"


def split_sections(md_text):
    parts, cur = [], []
    for line in md_text.split("\n"):
        if line.startswith("# ") and cur:
            parts.append("\n".join(cur))
            cur = []
        cur.append(line)
    parts.append("\n".join(cur))
    return [p for p in parts if p.strip()]


def table_report(html_body, section, h2_before):
    rows_out = []
    for k, tb in enumerate(re.findall(r"<table>(.*?)</table>", html_body, flags=re.S)):
        rows = re.findall(r"<tr>(.*?)</tr>", tb, flags=re.S)
        cells = [[re.sub(r"<[^>]+>", "", c).strip() for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, flags=re.S)] for r in rows]
        ncol = max(len(r) for r in cells)
        col_max = [max((len(htmlmod.unescape(r[j])) for r in cells if j < len(r)), default=0) for j in range(ncol)]
        longest_cell = max(col_max)
        row_chars = max(sum(len(c) for c in r) for r in cells)
        pos = html_body.find(tb)
        h2 = [h for p, h in h2_before if p < pos]
        where = h2[-1] if h2 else ""
        header = " | ".join(cells[0])
        wide = ncol >= 5 or (ncol >= 4 and row_chars > 3 * PHONE_CHARS) or (ncol >= 3 and longest_cell > 3 * PHONE_CHARS)
        if not wide:
            continue
        numeric = sum(bool(re.fullmatch(r"[\(\)\d.,% x\-:+A-Z]*", c)) for r in cells[1:] for c in r[1:]) / max(1, sum(len(r) - 1 for r in cells[1:]))
        if numeric > 0.6 and ncol <= 7:
            treat = ("Keep as a table; shorten headers, drop or merge a column, or split by period/tier into two tables of at "
                     "most 4 columns; numbers right aligned.")
        elif ncol >= 5:
            treat = ("Convert to a stacked list: one block per row, the first column as a bold lead, the other columns as "
                     "'Header: value' lines (no information lost, reflows on any screen).")
        else:
            treat = ("Convert to a definition list or one short paragraph per row; keep the table only in print.")
        rows_out.append({"section": section, "near_heading": where, "table_no_in_section": k + 1, "columns": ncol,
                         "rows": len(cells) - 1, "longest_row_chars": row_chars, "longest_cell_chars": longest_cell,
                         "header": header, "proposed_treatment": treat})
    return rows_out


def cover_image(tmpdir):
    if not COVER_PDF.exists():
        return None
    from pypdf import PdfReader
    page = PdfReader(str(COVER_PDF)).pages[0]
    w_in = float(page.mediabox.width) / 72
    h_in = float(page.mediabox.height) / 72
    dpi = 260
    base = Path(tmpdir) / "cov"
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-singlefile", str(COVER_PDF), str(base)], check=True)
    full = Image.open(f"{base}.png").convert("RGB")
    s = full.size[0] / w_in
    bleed, trim_w, trim_h = 0.125, 7.0, 10.0
    x0 = w_in - bleed - trim_w
    front = full.crop((int(x0 * s), int(bleed * s), int((x0 + trim_w) * s), int((bleed + trim_h) * s)))
    front = front.resize((1792, 2560), Image.LANCZOS)  # 7 x 10 proportion at 2560 px high (KDP ideal height)
    out = Path(tmpdir) / "cover.jpg"
    front.save(out, "JPEG", quality=90)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--tables", default=str(TABLES))
    a = ap.parse_args()
    book = epub.EpubBook()
    book.set_identifier("aef-book2-paygo-solar-finance-test-v0.2")
    book.set_title(build_book2.TITLE)
    book.set_language("en-GB")
    book.add_author(pd.AUTHOR)
    book.add_metadata("DC", "description", build_book2.SUBTITLE)
    book.add_metadata("DC", "publisher", pd.HOUSE)
    css = epub.EpubItem(uid="css", file_name="style/book.css", media_type="text/css", content=CSS)
    book.add_item(css)
    with tempfile.TemporaryDirectory() as td:
        cov = cover_image(td)
        if cov:
            book.set_cover("cover.jpg", cov.read_bytes())
        title = epub.EpubHtml(title="Title page", file_name="title.xhtml", lang="en-GB")
        title.content = (f"<h1 style='page-break-before:avoid'>{build_book2.TITLE}</h1><p><b>{build_book2.SUBTITLE}</b></p>"
                         f"<p>{pd.AUTHOR}</p><p>{pd.HOUSE}: {pd.SERIES.replace('&', '&amp;')}, Book 2</p>"
                         f"<p>Test conversion of the first edition, version 0.2 (pre-publication).</p>")
        title.add_item(css)
        book.add_item(title)
        spine, toc, wide, figs = ["nav", title], [], [], 0
        for i, sec in enumerate(split_sections(build_book2.assemble()), 1):
            md = markdown.Markdown(extensions=["tables", "fenced_code", "attr_list", "sane_lists", "toc"])
            body = md.convert(pd._prep_markdown(sec))
            name = htmlmod.unescape(re.sub(r"<[^>]+>", "", re.search(r"<h1[^>]*>(.*?)</h1>", body, flags=re.S).group(1)))
            for img in sorted(set(re.findall(r'src="(figures/[^"]+\.png)"', body))):
                p = FIG / Path(img).name
                book.add_item(epub.EpubItem(uid=p.stem, file_name=f"images/{p.name}", media_type="image/png", content=p.read_bytes()))
                body = body.replace(f'src="{img}"', f'src="images/{p.name}"')
                figs += 1
            body = re.sub(r'<p>(<img [^>]*alt="([^"]+)"[^>]*/?>)</p>', r"<figure>\1<figcaption>\2</figcaption></figure>", body)
            h2_before = [(m.start(), htmlmod.unescape(re.sub(r"<[^>]+>", "", m.group(1)))) for m in re.finditer(r"<h2[^>]*>(.*?)</h2>", body, flags=re.S)]
            wide += table_report(body, name, h2_before)
            ch = epub.EpubHtml(title=name, file_name=slug(i, name), lang="en-GB")
            ch.content = body
            ch.add_item(css)
            book.add_item(ch)
            spine.append(ch)
            toc.append(ch)
        book.toc = toc
        book.spine = spine
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        epub.write_epub(a.out, book)
    size = Path(a.out).stat().st_size
    print(f"{a.out}: {len(toc)} sections, {figs} figures, {size / 1e6:.2f} MB")
    with open(a.tables, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(wide[0].keys()))
        w.writeheader()
        w.writerows(wide)
    print(f"{len(wide)} tables flagged as too wide for a phone: {a.tables}")
    try:  # EPUBCheck (W3C) as bundled by the epubcheck Python package; needs Java
        import epubcheck
        jar = Path(epubcheck.__file__).parent / "epubcheck.jar"
    except ImportError:
        jar = None
    if jar and jar.exists() and shutil.which("java"):
        r = subprocess.run(["java", "-jar", str(jar), a.out], capture_output=True, text=True)
        msgs = [l for l in (r.stdout + r.stderr).split("\n") if l.startswith(("Validating", "Messages", "ERROR", "WARNING", "FATAL"))]
        print("epubcheck:", "; ".join(msgs[:12]))
    else:
        print("epubcheck not available (pip install epubcheck, needs Java)")


if __name__ == "__main__":
    main()
