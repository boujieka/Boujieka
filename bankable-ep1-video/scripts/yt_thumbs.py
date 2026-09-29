"""YouTube thumbnails for THE MoU TRAP episodes.

usage: yt_thumbs.py <lang en|fr> <frames_dir> <out_root>
frames_dir holds ep1.png .. ep7.png (1920x1080 scene frames); writes
<out_root>/<lang>-16x9/episode-n/youtube/thumbnail.png (1280x720) and
<out_root>/<lang>-9x16/episode-n/youtube/cover.png (1080x1920).
"""
import base64
import os
import sys

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

TXT = {
    "en": {"series": "THE MoU TRAP", "ep": "EPISODE", "sub": "Power deals in Africa · 7-part series",
           "titles": ["Fourteen contracts, no power", "What an MoU really binds", "Why projects stall",
                      "Who is in the room?", "When the deal closes anyway", "Closing the trap", "Before you sign"]},
    "fr": {"series": "LE PIÈGE DU MoU", "ep": "ÉPISODE", "sub": "Série en 7 épisodes",
           "titles": ["Quatorze contrats, aucun mégawatt", "Ce qu'engage vraiment un MoU", "Pourquoi les projets s'enlisent",
                      "Qui est dans la salle ?", "Quand l'accord aboutit quand même", "Refermer le piège", "Avant de signer"]},
}


def b64(path):
    return base64.b64encode(open(path, "rb").read()).decode()


def page(W, H, frame, n, t, fx="30%"):
    font = lambda f: f"url(data:font/woff2;base64,{b64(os.path.join(ASSETS, 'fonts', f))})"
    logo = b64(os.path.join(ASSETS, "art", "courant-continental.png"))
    img = b64(frame)
    title = t["titles"][n - 1].upper().replace("MOU", "MoU")
    portrait = H > W
    if portrait:
        pic = "left:0;top:0;width:1080px;height:1060px;background-position:38% 50%;background-size:cover;"
        panel = "left:0;top:980px;width:1080px;height:940px;clip-path:polygon(0 80px,100% 0,100% 100%,0 100%);"
        txt = "left:70px;top:1130px;width:940px;"
        tsize, badge, logo_css = 150, 84, "right:50px;top:50px;height:170px;"
    else:
        pic = "left:0;top:0;width:820px;height:720px;background-position:30% 50%;background-size:cover;"
        panel = "left:560px;top:0;width:720px;height:720px;clip-path:polygon(160px 0,100% 0,100% 100%,0 100%);"
        txt = "left:750px;top:60px;width:500px;"
        tsize, badge, logo_css = 84, 44, "right:34px;bottom:28px;height:120px;"
    if len(title) > 24:  # long (mostly French) titles: keep the block clear of the logo and edges
        tsize = round(tsize * 0.84)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Bangers;src:{font('bangers-latin-400-normal.woff2')}}}
@font-face{{font-family:Poppins;font-weight:700;src:{font('poppins-latin-700-normal.woff2')}}}
@font-face{{font-family:Poppins;font-weight:600;src:{font('poppins-latin-600-normal.woff2')}}}
html,body{{margin:0;width:{W}px;height:{H}px;overflow:hidden;background:#1d2733}}
.pic{{position:absolute;{pic}background-image:url(data:image/png;base64,{img});background-repeat:no-repeat;background-position-x:{fx}}}
.panel{{position:absolute;{panel}background:#1d2733}}
.stripe{{position:absolute;{panel}background:#f2b632;transform:translateX(-14px);z-index:0}}
.panel{{z-index:1}}
.txt{{position:absolute;{txt}z-index:2;color:#fff}}
.series{{font:700 {badge * 0.62:.0f}px Poppins,sans-serif;letter-spacing:.12em;color:#f2b632}}
.badge{{display:inline-block;margin:14px 0 18px;padding:6px 22px;background:#c8372d;color:#fff;
  font:400 {badge}px/1.1 Bangers,sans-serif;letter-spacing:.06em;transform:rotate(-2deg)}}
.title{{font:400 {tsize}px/1.2 Bangers,sans-serif;letter-spacing:.02em;text-shadow:0 5px 0 #000}}
.sub{{margin-top:22px;font:600 {badge * 0.5:.0f}px Poppins,sans-serif;color:#cfd8e3}}
.logo{{position:absolute;{logo_css}z-index:3;background:#fff;padding:8px 14px;border-radius:10px}}
</style></head><body>
<div class="pic"></div><div class="stripe"></div><div class="panel"></div>
<div class="txt"><div class="series">{t['series']}</div>
<div class="badge">{t.get('badge') or f"{t['ep']} {n}/7"}</div>
<div class="title">{title}</div><div class="sub">{t['sub']}</div></div>
<img class="logo" src="data:image/png;base64,{logo}">
</body></html>"""


def main(lang, frames, out_root):
    t = TXT[lang]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        for n in range(1, 8):
            frame = os.path.join(frames, f"ep{n}.png")
            fxf = os.path.join(frames, f"ep{n}.fx")
            fx = open(fxf).read().strip() if os.path.exists(fxf) else "30%"
            for fmt, W, H, name in (("16x9", 1280, 720, "thumbnail.png"), ("9x16", 1080, 1920, "cover.png")):
                d = os.path.join(out_root, f"{lang}-{fmt}", f"episode-{n}", "youtube")
                os.makedirs(d, exist_ok=True)
                pg = b.new_page(viewport={"width": W, "height": H})
                pg.set_content(page(W, H, frame, n, t, fx))
                pg.wait_for_timeout(400)
                pg.screenshot(path=os.path.join(d, name))
                pg.close()
        b.close()


if __name__ == "__main__":
    main(*sys.argv[1:4])
