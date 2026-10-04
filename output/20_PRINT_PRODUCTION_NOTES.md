# Print and Kindle production notes: PAYGo Solar Finance (Book 2), gate B9

Status: DRAFT, 3 October 2026. Production files for the proof stage, built from the v0.2 text. Nothing here is an upload file:
the ISBN line is a placeholder, the edition text is still "pre-publication", and no proof copy has been printed.
The checks below are automated file checks and a visual review of rendered pages by an AI agent. They are not a professional
prepress check, a proof copy review, or a Kindle Previewer test.

Defaults applied (output/12_AMAZON_PUBLISHING_PACK_draft.md, decisions D1 to D4 still open): paperback 7 x 10 in, black ink
on white paper, no bleed, figures redrawn to read in greyscale, KDP assigned ISBN placeholder, Kindle reflowable.

## 1. Specifications used

Direct access to kdp.amazon.com is blocked from this environment (and so are web.archive.org and the third party guides
tried). Every KDP figure below was therefore read in **search result snippets** only. Labels:
* **KDP snippet**: the snippet came from a kdp.amazon.com help page (secondary: search snippet, page not opened).
* **KDP snippet + guide**: also stated, with the same value, by an independent guide in a separate search (still secondary).
* None of the values is **confirmed** in the sense of the brief (document opened and read). All must be re-read in the KDP
  help pages and in the KDP file setup / cover calculator before upload.

| Item | Value used | Label | Source (help page as returned by search) |
|---|---|---|---|
| Trim size 7 x 10 in available | yes | KDP snippet | Set Trim Size, Bleed, and Margins, kdp.amazon.com/en_US/help/topic/GVBQ3CMEQW3W2VL6 |
| Inside (gutter) margin by page count | 24 to 150 p: 0.375 in; 151 to 300: 0.5; 301 to 500: 0.625; 501 to 700: 0.75; 701 to 828: 0.875 | KDP snippet + guide | same page; vappingo.com KDP formatting guides |
| Outside, top, bottom margins | at least 0.25 in without bleed; at least 0.375 in with bleed | KDP snippet + guide | same page |
| Bleed (interior) | if used: add 0.125 in to the width and 0.25 in to the height (0.125 in top, bottom, outside; none at the binding) | KDP snippet + guide | same page |
| Image resolution | at least 300 DPI; up to 600 DPI recommended maximum; file under 650 MB | KDP snippet | Paperback Submission Guidelines, help/topic/G201857950; Format Images, G202169030 |
| Fonts | all fonts fully embedded in interior and cover files; minimum 7 pt for interior text | KDP snippet | Paperback Submission Guidelines; Fix Paperback and Hardcover Formatting Issues, G201834260 |
| No crop marks, bookmarks, comments, annotations, placeholder text, metadata | applied (bookmarks and link annotations removed) | KDP snippet | Paperback Submission Guidelines |
| Spine width, black ink, white paper | page count x 0.002252 in (cream 0.0025; premium colour 0.002347) | KDP snippet + guide | Create a Paperback Cover, G201953020; KDP cover calculator |
| Full cover size | width = bleed + back + spine + front + bleed; height = bleed + trim height + bleed; bleed 0.125 in | KDP snippet + guide | Create a Paperback Cover |
| Spine text | only on books of more than 79 pages; at least 0.0625 in between text and spine edges | KDP snippet | Create a Paperback Cover |
| Barcode area | 2 x 1.2 in, at least 0.25 in from the spine and the trim, bottom right of the back cover | KDP snippet | Create a Paperback Cover; Barcodes, G5HDYGP4BXLX4RUW |
| Kindle images | 5 MB per image; images with text (graphs, diagrams) should fill at least 80% of the screen width; alt text on every image; 300 ppi recommended | secondary (search snippet; partly a third party summary of the Kindle Publishing Guidelines) | Kindle Publishing Guidelines, help/topic/G75V4YX5X8GRGXWV (snippet); goodreads.com author blog (5 MB) |
| Kindle tables | use HTML tables, not images (images cannot be paginated or read aloud); avoid tables wider than the screen and whole paragraphs in cells; under 100 rows and 10 columns; above 1,800 cells or 20,000 characters not supported | secondary (search snippet of the Kindle Publishing Guidelines) | help/topic/G200673210 and G75V4YX5X8GRGXWV (snippet) |
| Kindle cover image | 2,560 x 1,600 px ideal (1.6:1); JPEG preferred | KDP snippet | Cover Image Guidelines, G6GTK3T3NUHKLEFX |

Margins chosen for the interior (all above the minimums for any count up to 700 pages, so the layout survives copyedit
changes in length): inside 0.75 in, outside 0.6 in, top 0.85 in, bottom 0.8 in; running head baseline 0.5 in from the top,
folio 0.45 in from the bottom (both inside the 0.25 in minimum). Text block 5.65 x 8.35 in. No bleed: nothing prints to the edge.

## 2. Files

| File | What it is |
|---|---|
| tools/build_book2_figures.py (changed) | New flag `--print`: greyscale figures to book/figures_print/. Default output unchanged (checked: all 15 PNGs pixel identical to the previous script with the same workbooks) |
| volumes/02-solar-home-systems/book/figures_print/fig01 to fig15 | Greyscale figures, 8 bit grey PNG, 450 ppi, built from scratchpad lo/s10out/fm.xlsx and fc.xlsx (recalculated workbooks) |
| tools/build_book2.py (changed) | Same behaviour; the assembly is now a function (`assemble`) behind a main guard, so the print and Kindle builders read exactly the same text (checked: identical to the current v0.2 Markdown) |
| tools/build_book2_print.py (new) | KDP interior builder (helpers of tools/publish_docs.py, same browser engine) |
| output/20_BOOK2_INTERIOR_7x10_draft.pdf | Interior, **178 pages** (15 blank versos and end pad), 504 x 720 pt, 4.6 MB |
| tools/build_book2_cover.py (new) | Full wrap cover builder; reads the page count from the interior |
| output/20_BOOK2_COVER_7x10_draft.pdf | Cover, 14.6509 x 10.25 in (372.1 x 260.3 mm), spine 0.4009 in |
| output/20_BOOK2_COVER_thumb160.png | Front cover at 160 px wide |
| tools/build_book2_kindle.py (new) | Test EPUB builder and wide table report |
| output/20_BOOK2_KINDLE_test.epub | EPUB 3, 27 sections, 15 colour figures, cover image, 2.1 MB |
| output/20_BOOK2_KINDLE_wide_tables.csv | The 28 tables flagged for phones, with a proposed treatment for each |

Rebuild order: `build_book2_figures.py <fm> <fc> --print`, then `build_book2_print.py`, then `build_book2_cover.py`
(the spine depends on the page count), then `build_book2_kindle.py` (takes its cover image from the cover PDF).

## 3. What was done and checked

### 3.1 Figures (greyscale)
* Palette replaced by greys; every distinction that colour carried is carried by something else: line styles plus hollow
  markers and end labels with the marker repeated (Figures 3, 5); hatching (6, 10, 13); outlines and dashed borders (2, 7, 9,
  14, 15); fills in three separated grey levels (12, 14). Contrast check in the script: every text and fill pair is
  converted to grey and must reach 4.5:1 (WCAG AA); lowest pair white on mid grey 5.3:1.
* Layout fixes in print mode only: Figure 12 case names wrapped and the figure narrowed so its type is not shrunk below
  about 7 pt; Figure 14 labels shortened to "Manual" with a key line, columns respaced; Figure 15 right edge no longer cut;
  Figure 5 end labels clear of the markers; Figure 4 threshold label on a white ground; Figures 5 and 8 narrowed.
* Every figure was rendered and inspected at reading size. After placement at the text width, the smallest figure text is
  about 6.8 to 7.0 pt (Figures 3, 10 and 14); body text figures are above the 7 pt interior minimum. Proof check needed.
* Figures are placed at their natural size and never enlarged: lowest effective resolution in the PDF 449 ppi (pdfimages);
  all 16 images are single channel grey (the browser stores them as RGB; the builder writes them back as DeviceGray,
  lossless, and checks that the 15 placed figures are pixel for pixel identical to the files in figures_print/).

### 3.2 Interior
* Title page (no cover page), copyright page, contents (chapters and sections, with page numbers), then the text. Every
  chapter, the front matter sections and every annex open on a right hand page; a blank verso is inserted where needed.
* Mirrored margins: the page is rendered with the mean margin and shifted 0.075 in towards the outside on each page.
* Running heads: verso "PAYGo Solar Finance", recto the chapter title (shortened to fit); folios at the outside foot; no
  head on chapter openings, none on the title page, the copyright page or blank pages.
* Figure captions are printed under each figure (in the Markdown they are alt text only).
* Checks run by the builder, all passed: every contents entry found on its listed page; 27 openings on recto; every word
  inside the live area (pdftotext word boxes, 1.5 pt tolerance); pdffonts: 296 font objects, 0 not embedded (Liberation
  Sans, TrueType subsets; the running heads use the same embedded font, no base 14 fonts); text scan clean (dashes and
  banned words, the A4 pipeline's scan).
* KDP clean up: bookmarks and link annotations removed; document information limited to title and author.

### 3.3 Cover
* 178 pages x 0.002252 = 0.4009 in spine; 0.125 + 7 + 0.4009 + 7 + 0.125 = 14.6509 in by 10.25 in.
* Front: AFRICA ENERGY FINANCE brand line, BOOK 2 mark, PAYGo / SOLAR / FINANCE in three dominant lines, subtitle, author.
  Back: section 5 text of the Amazon pack, word for word. Spine: BOOK 2, PAYGo SOLAR FINANCE, author, 13 pt, reading top to
  bottom, inside the 0.0625 in spine margins; no colour block on the spine (fold drift would show its edge).
* Text kept 0.5 in inside every trim edge. Barcode area (2 x 1.2 in at 0.25 in from spine and bottom trim) left empty and
  clear of text. Fonts embedded (3, all embedded). Brand green #0B3020 and gold #B07C0F; a lighter gold (#E0B44A) is used
  for small type on green for contrast.
* Thumbnail at 160 px: the three title lines and the BOOK 2 mark read clearly; the subtitle and author are barely legible
  at that size, which is normal for a thumbnail. Looked at by eye, not tested with readers.
* Draft only: built from the formula, not from the KDP template file for the final count.

### 3.4 Kindle test EPUB
* EPUBCheck 5.3.0 (W3C, via the epubcheck Python package, Java): 0 fatals, 0 errors, 0 warnings.
* **Kindle Previewer is not available** in this environment (not installed, no Linux build used here), so the Kindle
  rendering itself has not been checked.
* Figures: colour PNGs at 300 dpi, set at 100% of the screen width, captions visible and repeated as alt text.
* Wide tables: 28 tables flagged (more than 4 columns, or rows far beyond a phone line). Rendered at a 390 px phone viewport
  in a browser, the 8 column funding instrument table (11.1) needs 617 px: it scrolls sideways. Full list with the proposed
  treatment in output/20_BOOK2_KINDLE_wide_tables.csv. Summary:
  * convert to stacked lists (one block per row, "Header: value" lines): funding instruments (11.1, 8 columns), borrowing
    base (11.5, 9), SolaraPay price plans (4.7, 8; 16.1, 6), Annex G sources (5 columns, long cells);
  * keep as numeric tables but cut to 4 columns or split by period or tier: stress tables (10.7, 14.3, 14.8, 16.7), unit
    tables (9.3, 9.6, 16.5), receivables by year (10.1), tranching (12.2), calibration (16.3, 16.4, 16.6);
  * text tables of 3 or 4 columns with long cells (About this book, Introduction, 1.1, 7.2, 7.6, 10.3, 11.1 stages, 16.10,
    Annex A twice, Annex D): definition lists or one paragraph per row.
  * Alternative for all of them (decision D3): a fixed layout or Print Replica edition, whose eligibility and royalty
    treatment must be read in KDP first. Images of tables are not recommended by the Kindle guidelines.

## 4. Findings for the lead (outside this gate's files)

1. The A4 edition (output/01_BOOK_PAYGO_SOLAR_FINANCE_v0.2.pdf) prints **no figure captions**: the captions exist only as
   alt text, and pdftotext finds no "Figure N." in it. The print and Kindle builders print them; publish_docs.py may want
   the same change (not made here).
2. Text inside the figures is not covered by the PDF text scan: Figure 12 shows workbook case names with hyphens
   ("repayment-linked", "sales volume -20%") and the axes of Figures 3 and 12 show negatives with a minus sign, not in
   parentheses. Same in the colour figures. A house style decision for chart labels is needed.
3. Figure 3 (both versions): the leader line of "All three end at LCY 11,832" crosses the "14" of the month label.
4. Some pages end short because figures and table rows are kept whole, and a few pages are nearly empty before a long
   table. Acceptable for a proof; a typesetter would rebalance.

## 5. Open decisions

* **D1 trim**: 7 x 10 in used. At 6 x 9 in the count would rise and the wide tables would need the treatments of 3.4 in print too.
* **D2 colour**: black ink used; the greyscale figures are ready. Standard colour would use the colour figures unchanged.
* **D4 ISBN**: the copyright page carries a visible placeholder line, which KDP rejects as placeholder text. Replace with
  the ISBN (KDP assigned, imprint "Independently published", or the author's own with "Africa Energy Finance") before upload;
  the barcode is placed by KDP in either case.
* **D3 Kindle layout**: reflowable test built; decide after a Kindle Previewer check and the table conversions.
* Edition text (gate 5 of the pack): "pre-publication", version 0.2 and the "Status of this edition" section are still in.

## 6. What still needs a proof copy (or KDP's own tools)

* Upload the interior and cover to KDP's previewer: margin, gutter and spine warnings; cover against the KDP template for
  the final page count (spine 0.4009 in at 178 pages; any change in count changes the cover width).
* Printed proof: grey levels of the figures on KDP paper (hatching and 0.5 pt rules can fill in or vanish), the light
  table shading (#F1F1F1 and #DCDCDC may print lighter or darker), the smallest figure text near 7 pt, the gutter on a
  178 page binding, the green and gold of the cover on the KDP cover stock, and spine text alignment.
* Kindle Previewer on phone, tablet and e-reader for the EPUB, after the table conversions.
* A professional prepress check is advised before the commercial release; this note is not one.
