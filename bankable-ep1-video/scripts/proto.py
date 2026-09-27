"""One-panel prototype of the animated puppets (page 19, panel 1)."""
import os, subprocess, sys
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import tts, cam, SR, W, H          # noqa: E402
from animate import PANELS, place_puppets, puppet_markup, animate_shot, bubble_mask, ROOT  # noqa: E402

PAGE, PANEL = 18, 0
LINES = [("KERBU", "Are you trying to kill my project?!"), ("ENILEC", "No, Minister. We are trying to save it.")]


def main():
    rect = PANELS[PAGE][PANEL]
    os.makedirs(os.path.join(ROOT, "assets", "masks"), exist_ok=True)
    mask = f"assets/masks/bubbles-{PAGE:03d}.png"
    bubble_mask(PAGE, os.path.join(ROOT, mask))
    t, placed = 1.0, []
    for spk, text in LINES:
        _, data = tts(spk, text)
        placed.append((spk, t, data)); t += len(data) / SR + 0.45
    total = round(t + 1.0, 2)
    mix = np.zeros(int(total * SR), np.float32)
    for _, st, d in placed:
        mix[int(st * SR):int(st * SR) + len(d)] += d
    sf.write("/tmp/proto.wav", mix, SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "/tmp/proto.wav", "-c:a", "aac", "-b:a", "160k",
                    os.path.join(ROOT, "assets", "audio", "proto.m4a")], check=True)

    pups = [(f"pp{i}", p) for i, p in enumerate(place_puppets(PAGE, PANEL))]
    moods = {"KERBU": "angry", "ENILEC": "neutral"}
    x, y, w, h = rect
    svgs = "".join(puppet_markup(pid, p, rect, moods.get(p["who"], "neutral")) for pid, p in pups)
    a, b = cam(rect, 1.0), cam(rect, 1.03)
    js = [f'tl.set(".cam", {{x: {a["x"]}, y: {a["y"]}, scale: {a["scale"]}}}, 0);',
          f'tl.to(".cam", {{x: {b["x"]}, y: {b["y"]}, scale: {b["scale"]}, duration: {total}, ease: "none"}}, 0);']
    animate_shot(js, pups, placed, 0, total, SR)
    tpl = open(os.path.join(ROOT, "scripts", "proto_template.html")).read()
    html = (tpl.replace("{{TOTAL}}", str(total)).replace("{{PAGE}}", f"{PAGE:03d}").replace("{{MASK}}", mask)
               .replace("{{PX}}", str(x + 6)).replace("{{PY}}", str(y + 6)).replace("{{PW}}", str(w - 12)).replace("{{PH}}", str(h - 12))
               .replace("{{SVGS}}", svgs.replace(f'left:', 'left:').replace('px;top:', 'px;top:'))
               .replace("{{JS}}", "\n      ".join(js)))
    # puppet coords are panel-local; the clip box is inset 6px
    html = html.replace('class="puppet" style="left:', 'class="puppet" style="margin:-6px 0 0 -6px;left:')
    open(os.path.join(ROOT, "proto.html"), "w").write(html)
    print("total", total, "puppets", [(p["who"], round(p["k"], 2), p["look"]) for _, p in pups])


if __name__ == "__main__":
    main()
