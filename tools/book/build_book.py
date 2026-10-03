"""Three-pass build of the book: DOCX + PDF with a static, page-accurate table of contents.

python tools/book/build_book.py
Outputs: book/Bankable_Hydro_Book.docx, book/Bankable_Hydro_Book.pdf
"""
import json, os, re, subprocess, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)
B = "book/build"
os.makedirs(B, exist_ok=True)


def sh(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print(r.stdout, r.stderr)
        raise SystemExit(f"failed: {cmd}")
    return r.stdout


def to_pdf(docx):
    sh(["soffice", "--headless", "--convert-to", "pdf", "--outdir", B, docx], timeout=300)
    return docx.replace(".docx", ".pdf")


sh(["python3", "tools/book/prepare.py"])
sh(["python3", "tools/book/figures.py"])
SRC = f"{B}/manuscript_resolved.md"

# pass 1: get the heading list
sh(["node", "tools/book/build_docx.js", SRC, f"{B}/p1.docx"])
entries = json.load(open(f"{B}/p1.tocentries.json"))
toc = [dict(e, page="000") for e in entries]
json.dump(toc, open(f"{B}/toc.json", "w"))

# pass 2: same layout with placeholder page numbers, then read real pages
sh(["node", "tools/book/build_docx.js", SRC, f"{B}/p2.docx", f"{B}/toc.json"])
pdf = to_pdf(f"{B}/p2.docx")
n = int(re.search(r"Pages:\s+(\d+)", sh(["pdfinfo", pdf])).group(1))
pages = [sh(["pdftotext", "-f", str(p), "-l", str(p), "-layout", pdf, "-"]) for p in range(1, n + 1)]
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
npages = [norm(p) for p in pages]
# skip front matter up to and including the contents pages
start = max(i for i, p in enumerate(npages) if "contents" in p[:40]) + 1
start = next(i for i in range(start, n) if "000" not in pages[i][:4000] or "contents" not in npages[i][:40])
cur = start
missing = []
for e in toc:
    key = norm(e["text"].split(": ", 1)[-1] if e["level"] == 0 else re.sub(r"^(Chapter \d+|Annex [A-Z])\.\s*", "", e["text"]))
    found = None
    for i in range(cur, n):
        if key[:60] in npages[i]:
            found = i
            break
    if found is None:
        missing.append(e["text"])
        e["page"] = ""
    else:
        e["page"] = str(found + 1)
        cur = found
json.dump(toc, open(f"{B}/toc.json", "w"), indent=1)
if missing:
    print("TOC entries not located:", missing)

# pass 3: final
sh(["node", "tools/book/build_docx.js", SRC, f"{B}/p3.docx", f"{B}/toc.json"])
pdf3 = to_pdf(f"{B}/p3.docx")
shutil.copy(f"{B}/p3.docx", "book/Bankable_Hydro_Book.docx")
shutil.copy(pdf3, "book/Bankable_Hydro_Book.pdf")
n3 = int(re.search(r"Pages:\s+(\d+)", sh(["pdfinfo", pdf3])).group(1))
print("pages:", n3, "(pass2:", n, ")")
