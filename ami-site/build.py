"""Build the static Africa Mineral Insights site (concept note + Cameroon modules) into ami-site/dist/.

Usage: python ami-site/build.py
Needs the `markdown` package (pip install markdown).
"""
import html
import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = Path(__file__).resolve().parent / "dist"
TEMPLATE = (Path(__file__).resolve().parent / "template.html").read_text(encoding="utf-8")

MODULES = [
    ("01-geospatial-intelligence", "01", "Geo-Spatial Intelligence"),
    ("02-mineral-potential", "02", "Mineral Potential"),
    ("03-mining-sector-intelligence", "03", "Mining Sector Intelligence"),
    ("04-legal-regulatory", "04", "Legal & Regulatory Insights"),
    ("05-value-chains", "05", "Mineral Products & Value Chains"),
    ("06-market-trade", "06", "Market & Trade Intelligence"),
    ("07-investment-intelligence", "07", "Mineral Investment Intelligence"),
    ("08-financing-intelligence", "08", "Mineral Financing Intelligence"),
    ("09-value-strategy", "09", "Value Addition & National Strategy"),
]


def rewrite_links(text: str) -> str:
    # Markdown references to module files become links to the generated pages.
    for slug, _, _ in MODULES:
        text = text.replace(f"`cameroon/{slug}.md`", f"[{slug}](cameroon/{slug}.html)")
        text = text.replace(f"`docs/cameroon/{slug}.md`", f"[{slug}](cameroon/{slug}.html)")
    return text


LIST_ITEM = re.compile(r"^(\s*(?:>\s*)*)([-*+]|\d+\.)\s")


def blank_before_lists(md_text: str) -> str:
    # Python-Markdown needs a blank line between a paragraph and a list (GitHub does not).
    out, prev = [], ""
    in_code = False
    for line in md_text.split("\n"):
        if line.lstrip().startswith("```"):
            in_code = not in_code
        m = LIST_ITEM.match(line)
        if (not in_code and m and prev.strip() and not LIST_ITEM.match(prev)
                and not prev.lstrip().startswith("|") and not prev.startswith((" ", "\t"))):
            out.append(m.group(1).rstrip())
        out.append(line)
        prev = line
    return "\n".join(out)


def render(md_text: str) -> str:
    md_text = blank_before_lists(md_text)
    body = markdown.markdown(md_text, extensions=["tables", "fenced_code", "toc", "sane_lists"])
    # Bare URLs become clickable.
    return re.sub(r'(?<![">=])(https?://[^\s<)]+)', r'<a href="\1" rel="noopener">\1</a>', body)


def nav(prefix: str, current: str) -> str:
    items = [f'<a href="{prefix}index.html"{" aria-current=page" if current == "index" else ""}>Cadrage</a>']
    for slug, num, title in MODULES:
        cur = " aria-current=page" if current == slug else ""
        items.append(f'<a href="{prefix}cameroon/{slug}.html"{cur} title="{html.escape(title)}">{num}</a>')
    return "\n".join(items)


def page(title: str, body: str, prefix: str, current: str) -> str:
    return (TEMPLATE.replace("{{TITLE}}", html.escape(title))
            .replace("{{NAV}}", nav(prefix, current))
            .replace("{{BODY}}", body))


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "cameroon").mkdir(parents=True)

    concept = rewrite_links((DOCS / "AFRICA_MINERAL_INSIGHTS.md").read_text(encoding="utf-8"))
    cards = "\n".join(
        f'<a class="card" href="cameroon/{slug}.html"><span class="num">{num}</span>{html.escape(title)}</a>'
        for slug, num, title in MODULES)
    index_body = f'<section class="cards" aria-label="Modules de l\'édition Cameroun">{cards}</section>\n' + render(concept)
    (OUT / "index.html").write_text(page("Africa Mineral Insights", index_body, "", "index"), encoding="utf-8")

    for slug, num, title in MODULES:
        md_text = (DOCS / "cameroon" / f"{slug}.md").read_text(encoding="utf-8")
        body = render(md_text)
        (OUT / "cameroon" / f"{slug}.html").write_text(
            page(f"{num} · {title} — Cameroun", body, "../", slug), encoding="utf-8")

    shutil.copy(ROOT / "brand" / "favicon.svg", OUT / "favicon.svg")
    print(f"Wrote {OUT} ({len(MODULES) + 1} pages)")


if __name__ == "__main__":
    main()
