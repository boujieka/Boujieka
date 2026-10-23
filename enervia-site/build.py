"""Assemble les pages : remplace les marqueurs <!--HEAD--> etc. par les fragments partagés."""
import shutil
from pathlib import Path

root = Path(__file__).parent
out = root / "public"
shutil.rmtree(out, ignore_errors=True)
shutil.copytree(root / "assets", out / "assets")
parts = {
    "<!--HEAD-->": (root / "src/head.html").read_text(encoding="utf-8"),
    "<!--HEADER-->": (root / "partials/header.html").read_text(encoding="utf-8"),
    "<!--FOOTER-->": (root / "partials/footer.html").read_text(encoding="utf-8"),
    "<!--SCRIPTS-->": (root / "src/scripts.html").read_text(encoding="utf-8"),
}
for page in ("index", "diagnostic", "contact", "merci"):
    html = (root / f"src/{page}.html").read_text(encoding="utf-8")
    for marker, frag in parts.items():
        html = html.replace(marker, frag.strip())
    (out / f"{page}.html").write_text(html, encoding="utf-8")
    print("built", page)
