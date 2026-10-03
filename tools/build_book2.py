"""Assemble and publish Book 2, PAYGo Solar Finance (first edition, version 0.2).

Run: python tools/build_book2.py
Concatenates the chapter sources in reading order into book/book2_paygo_solar_finance_v0.2.md and publishes
output/01_BOOK_PAYGO_SOLAR_FINANCE_v0.2.pdf with tools/publish_docs.py (contents with page numbers, running header and footer,
bookmarks, text scan). Figures are produced beforehand by tools/build_book2_figures.py.
"""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "volumes/02-solar-home-systems/book"
ORDER = ["ch00_front.md", "ch00b_intro.md"] + [f"ch{k:02d}.md" for k in range(1, 17)] + ["ch99_annexes.md"]
SRC = BOOK / "book2_paygo_solar_finance_v0.2.md"
OUT = ROOT / "output/01_BOOK_PAYGO_SOLAR_FINANCE_v0.2.pdf"

SRC.write_text("\n\n".join((BOOK / f).read_text().strip() for f in ORDER) + "\n")
r = subprocess.run([sys.executable, str(ROOT / "tools/publish_docs.py"), str(SRC), str(OUT),
                    "--title", "PAYGo Solar Finance",
                    "--subtitle", "Business Models, Credit Risk and Financial Structuring for Solar Home Systems",
                    "--kicker", "BOOK 2", "--short", "PAYGo Solar Finance",
                    "--edition", "First edition, version 0.2 (pre-publication)"])
if r.returncode == 0:
    shutil.copy(OUT, BOOK / "Book2_PAYGo_Solar_Finance_First_Edition_v0.2.pdf")
sys.exit(r.returncode)
