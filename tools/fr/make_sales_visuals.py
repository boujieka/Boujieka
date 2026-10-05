"""Sales visuals for the French edition (Gumroad, Chariow, Etsy): front cover, square thumbnail, wide banner.

python3 tools/fr/make_sales_visuals.py   (after the French cover: book7/publishing_fr/LIVRE7_COUVERTURE_6x9_FR.pdf)
Writes book7/publishing_fr/visuels/: couverture_1800x2700.jpg, vignette_1200x1200.jpg, banniere_1280x720.jpg, etsy_2000x1600.jpg.
"""
import base64
import glob
import os
import subprocess
import tempfile

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)
COVER = "book7/publishing_fr/LIVRE7_COUVERTURE_6x9_FR.pdf"
OUT = "book7/publishing_fr/visuels"
os.makedirs(OUT, exist_ok=True)
GREEN, GOLD, GOLDL, CREAM = "#0B3020", "#B07C0F", "#E0B44A", "#F7F3E8"

# front cover: the right-hand trim box of the full wrap (6 x 9 in front, 0.125 in bleed)
with tempfile.TemporaryDirectory() as td:
    subprocess.run(["pdftoppm", "-r", "300", "-png", "-singlefile", COVER, f"{td}/wrap"], check=True)
    wrap = Image.open(f"{td}/wrap.png").convert("RGB")
W, H = wrap.size
ppi = H / 9.25
front = wrap.crop((int(W - (6 + 0.125) * ppi), int(0.125 * ppi), int(W - 0.125 * ppi), int(H - 0.125 * ppi)))
front = front.resize((1800, 2700), Image.LANCZOS)
front.save(f"{OUT}/couverture_1800x2700.jpg", quality=92)
b64 = base64.b64encode(open(f"{OUT}/couverture_1800x2700.jpg", "rb").read()).decode()


def page(w, h, body):
    return f"""<html><head><meta charset='utf-8'><style>
body {{ margin:0; width:{w}px; height:{h}px; background:{CREAM}; font-family:'Liberation Sans', Arial, sans-serif; overflow:hidden;
        display:flex; align-items:center; gap:{int(w * 0.04)}px; padding:0 {int(w * 0.06)}px; box-sizing:border-box; }}
img {{ box-shadow: 0 {int(h * 0.02)}px {int(h * 0.05)}px rgba(0,0,0,.35); }}
.k {{ color:{GOLD}; font-weight:700; letter-spacing:2px; }}
h1 {{ color:{GREEN}; margin:.25em 0 .3em 0; line-height:1.1; }}
.r {{ width:{int(w * 0.12)}px; height:5px; background:{GOLD}; margin:.4em 0 .8em 0; }}
li {{ color:#1d1d1d; margin:.25em 0; }}
.f {{ color:#555; }}
</style></head><body>{body}</body></html>"""


def shot(html_s, w, h, out):
    exe = (sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome")) or [None])[0]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.set_content(html_s, wait_until="load")
        pg.screenshot(path=out.replace(".jpg", ".png"))
        b.close()
    Image.open(out.replace(".jpg", ".png")).convert("RGB").save(out, quality=92)
    os.remove(out.replace(".jpg", ".png"))


IMG = f"<img src='data:image/jpeg;base64,{b64}' style='height:88%'>"
LIST = ("<ul><li>Le Hydro Readiness Framework™ : 8 questions, 23 portes, 1 décision</li><li>Développeur, prêteurs et État</li>"
        "<li>Cas complet de 60 MW et modèle Excel en français</li></ul>")
shot(page(1280, 720, IMG + f"<div style='font-size:22px'><div class='k'>LIVRE 7 · ÉDITION FRANÇAISE</div>"
                          f"<h1 style='font-size:44px'>Développement et financement de l'hydroélectricité</h1>"
                          f"<div class='r'></div><div style='font-size:24px;color:{GREEN}'>De la rivière au bouclage financier</div>{LIST}"
                          f"<div class='f'>Emmanuel Boujieka Kamga · Africa Energy Finance</div></div>"), 1280, 720, f"{OUT}/banniere_1280x720.jpg")
shot(page(1200, 1200, f"<div style='width:100%;text-align:center'><img src='data:image/jpeg;base64,{b64}' style='height:1000px'></div>"),
     1200, 1200, f"{OUT}/vignette_1200x1200.jpg")
shot(page(2000, 1600, IMG + f"<div style='font-size:34px'><div class='k'>LIVRE PDF · MODÈLE EXCEL · VIDÉO</div>"
                           f"<h1 style='font-size:68px'>Développement et financement de l'hydroélectricité</h1>"
                           f"<div class='r'></div><div style='font-size:38px;color:{GREEN}'>De la rivière au bouclage financier</div>{LIST}"
                           f"<div class='f'>Produit numérique · Édition française</div></div>"), 2000, 1600, f"{OUT}/etsy_2000x1600.jpg")
print("visuals written:", sorted(os.listdir(OUT)))
