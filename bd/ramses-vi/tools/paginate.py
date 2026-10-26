"""Lit un rendu PDF et retrouve la page de chaque titre du sommaire.

Usage : paginate.py rendu.pdf toc.json pages.json
"""
import json
import re
import subprocess
import sys
import unicodedata


def norm(t):
    t = unicodedata.normalize("NFKC", t).lower()
    t = re.sub(r"[’'`«»\"“”]", "", t)
    return re.sub(r"\s+", " ", t).strip()


def main(pdf, toc_path, out_path):
    npages = int(re.search(r"Pages:\s+(\d+)", subprocess.run(
        ["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
    pages = []
    for p in range(1, npages + 1):
        txt = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), "-layout", pdf, "-"],
                             capture_output=True, text=True).stdout
        pages.append(txt)
    # Pages du sommaire : nombreuses lignes terminées par « 00 » (premier passage)
    toc_pages = {i for i, t in enumerate(pages) if len(re.findall(r"\.\s*00\s*$", t, re.M)) >= 5}
    start = max(toc_pages) + 1 if toc_pages else 1
    normed = [norm(t) for t in pages]
    entries = json.load(open(toc_path, encoding="utf8"))
    result, cur, missing = {}, start, []
    for e in entries:
        needle = norm(e["text"])[:45]
        found = None
        for i in range(cur, npages):
            if needle in normed[i]:
                found = i
                break
        if found is None:
            missing.append(e["text"])
            continue
        result[e["key"]] = str(found + 1)
        cur = found
    json.dump(result, open(out_path, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    print(f"{len(result)}/{len(entries)} titres paginés")
    for m in missing:
        print("  introuvable :", m)


if __name__ == "__main__":
    main(*sys.argv[1:4])
