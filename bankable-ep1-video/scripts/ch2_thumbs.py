"""Thumbnails for the Chapter 2 long-form videos (1280x720), reusing yt_thumbs.page.

usage: ch2_thumbs.py <frame.png> <fx%> <out_root>   -> <out_root>/<lang>/youtube/thumbnail.png
"""
import os
import sys

from playwright.sync_api import sync_playwright

from yt_thumbs import CHROME, page

TXT = {
    "en": {"series": "BANKABLE IS NOT ENOUGH", "badge": "CHAPTER 2", "titles": ["Two tests, one framework"],
           "sub": "Why a bankable power deal has passed only half its examination"},
    "fr": {"series": "BANCABLE NE SUFFIT PAS", "badge": "CHAPITRE 2", "titles": ["Deux tests, un cadre"],
           "sub": "Pourquoi un projet bancable n'a réussi que la moitié de son examen"},
}


def main(frame, fx, out_root):
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        for lang, t in TXT.items():
            d = os.path.join(out_root, lang, "youtube")
            os.makedirs(d, exist_ok=True)
            pg = b.new_page(viewport={"width": 1280, "height": 720})
            pg.set_content(page(1280, 720, frame, 1, t, fx))
            pg.wait_for_timeout(400)
            pg.screenshot(path=os.path.join(d, "thumbnail.png"))
            pg.close()
        b.close()


if __name__ == "__main__":
    main(*sys.argv[1:4])
