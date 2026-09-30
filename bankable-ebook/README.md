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
