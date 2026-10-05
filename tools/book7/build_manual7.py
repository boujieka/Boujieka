"""Build MANUAL 7 in the house style: A4 PDF and Word.

Run: python3 tools/book7/build_manual7.py
Top-level sections of the Markdown source become chapters (## -> #, ### -> ##), outside code blocks.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)
FR = os.environ.get("BOOK_LANG") == "fr"  # French manual from manual/MANUAL7_Manuel_utilisation_methodologie.md
SRC, BUILD = ("manual/MANUAL7_Manuel_utilisation_methodologie.md", "manual/build_fr") if FR else ("manual/MANUAL7_User_and_Methodology.md", "manual/build")
NAME = "MANUAL7_Manuel_utilisation_methodologie" if FR else "MANUAL7_User_and_Methodology"
TITLE = "MANUAL 7 : manuel d'utilisation et de méthodologie" if FR else "MANUAL 7: User and Methodology Manual"
SUB = ("MODEL 7, modèle de développement et de financement de l'hydroélectricité. Ressource d'accompagnement du Livre 7, "
       "De la rivière au bouclage financier") if FR else "MODEL 7, Hydropower Development and Finance Model. Companion to Book 7, From River to Financial Close"
EDITION = "Version 1.0 (release candidate 1)" if FR else "Version 1.0 release candidate 1"
os.makedirs(BUILD, exist_ok=True)
out, fence = [], False
for line in open(SRC, encoding="utf8").read().split("\n"):
    if line.strip().startswith("```"):
        fence = not fence
        out.append(line)
        continue
    if not fence:
        if line.startswith("# MANUAL 7"):
            continue
        if line.startswith("## MODEL 7, Hydropower") or line.startswith("## MODEL 7, modèle"):
            out.append("# À propos de ce manuel" if FR else "# About this manual")
            continue
        for old, new in (("#### ", "### "), ("### ", "## "), ("## ", "# ")):
            if line.startswith(old):
                line = new + line[len(old):]
                break
    out.append(line)
render = f"{BUILD}/manual7_render.md"
open(render, "w", encoding="utf8").write("\n".join(out))
subprocess.run([sys.executable, "tools/book7/build_docx7.py", "--src", render, "--out", f"{BUILD}/{NAME}.docx",
                "--title", TITLE, "--subtitle", SUB, "--kicker", "MANUAL 7", "--edition", EDITION], check=True)
subprocess.run([sys.executable, os.path.abspath("tools/house/publish_docs.py"), "manual7_render.md", f"{NAME}.pdf",
                "--title", TITLE, "--subtitle", SUB, "--kicker", "MANUAL 7", "--short", TITLE, "--edition", EDITION,
                "--case", "cas Kasiri River Hydro" if FR else "Kasiri River Hydro case",
                "--keywords", "hydroélectricité; modèle financier; manuel d'utilisation; méthodologie" if FR else "hydropower; financial model; user manual; methodology"], cwd=BUILD)
