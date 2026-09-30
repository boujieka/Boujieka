# Bankable Is Not Enough: Kindle ebook build

Turns the Word manuscript into a reflowable EPUB 3 that Kindle Direct Publishing accepts.

    ./build.sh Bankable_Is_Not_Enough_Master_Manuscript.docx cover.jpg

What the filter (`kindle.lua`) changes for the ebook:
- removes the printed Contents (page numbers); Kindle uses the linked table of contents instead
- removes the line "[ISBN, paperback] [ISBN, hardcover] [ISBN or ASIN, ebook]" (KDP assigns an ASIN)
- turns the repeated "PART ..." running lines into one part page per part
- titles chapters "N. Title" (with "Chapter N · Test k: X" kept under Chapters 4 to 10) and appendices "Appendix X. Title"
- nests the table of contents: part > chapter; sections stay inside each chapter

The manuscript and the built EPUB are not stored in this repository.

## Paperback interior (KDP, 6 x 9 in, no bleed)

    ./build_paperback.sh Bankable_Is_Not_Enough_Master_Manuscript.docx path/to/CharisSIL-6.200

- 6 x 9 in pages; margins 0.875 in inside (gutter), 0.6 in outside, 0.8 in top and bottom
- Charis SIL (SIL Open Font License), embedded
- the paperback ISBN (BOOK_ISBN, default 9798178190425) replaces the ISBN placeholder line on the copyright page
- front matter numbered in roman; Part I starts at page 1 on a right-hand page; parts and chapters open on right-hand pages
- contents page with page numbers; running heads (book title left, section title right); footnotes at the foot of the page

## Paperback cover (KDP full wrap: back, spine, front; 0.125 in bleed)

    python build_cover.py front_cover.png <interior page count> path/to/CharisSIL-6.200 cover.pdf white

- spine = pages x 0.002252 in (white paper) or 0.0025 in (cream); check against KDP's cover calculator
- back-cover text is taken from the book (Key messages, Preface, About the Author); the lower right of the
  back is left clear for the barcode KDP adds

## Author's edits applied by kindle.lua (October 2026)
- removed "[Publisher or imprint, and address]" and the whole Declaration of Interests section
- preface signed "Brazzaville and Yaoundé, October 2026"
