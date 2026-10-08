"""Build the static ARVI blueprint page from docs/arvi/ARVI_MASTER_BLUEPRINT_v1.0.md.

Usage: python site/arvi/build.py   (needs the `markdown` package; writes site/arvi/dist/)
Deploy site/arvi/dist/ to the Netlify project "arvi-africa".
"""

from __future__ import annotations

import html
import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs" / "arvi" / "ARVI_MASTER_BLUEPRINT_v1.0.md"
HERE = Path(__file__).resolve().parent
DIST = HERE / "dist"


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    # The hero already shows the title and the sidebar the contents: drop both from the body.
    text = text.replace("## Master Blueprint v1.0\n", "", 1)
    text = re.sub(r"## Sommaire\n.*?\n---\n", "", text, count=1, flags=re.S)
    md = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "sane_lists"],
                           extension_configs={"toc": {"toc_depth": "2-2"}})
    body = md.convert(text)
    # Tag review markers so they stand out.
    body = body.replace("[À VÉRIFIER", '<span class="flag verify">[À VÉRIFIER').replace(
        "[HYPOTHÈSE]", '<span class="flag hyp">[HYPOTHÈSE]</span>')
    body = re.sub(r'(<span class="flag verify">\[À VÉRIFIER[^\]]*\])', r"\1</span>", body)
    body = body.replace("<table>", '<div class="table-scroll"><table>').replace("</table>", "</table></div>")
    page = (HERE / "template.html").read_text(encoding="utf-8")
    page = page.replace("{{TOC}}", md.toc).replace("{{BODY}}", body).replace(
        "{{SOURCE}}", html.escape(SOURCE.relative_to(ROOT).as_posix()))
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    (DIST / "index.html").write_text(page, encoding="utf-8")
    shutil.copy(HERE / "netlify.toml", DIST / "netlify.toml")
    shutil.copy(SOURCE, DIST / SOURCE.name)
    print(f"wrote {DIST / 'index.html'}")


if __name__ == "__main__":
    main()
