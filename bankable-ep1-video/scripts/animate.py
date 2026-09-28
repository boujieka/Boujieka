"""Puppet placement and animation helpers shared by build.py and proto.py.

- place_puppets(page, panel): which characters stand in a panel, where, and
  which way they look (from scripts/faces.json + manual corrections).
- lip_keys(wav): mouth-open keyframes from the loudness of a voice clip.
- bubble_mask(page): PNG alpha mask of the white speech bubbles on a page, so
  bubbles can be drawn back on top of the puppets.
All timing is precomputed here; the page runtime only replays GSAP tweens.
"""
import json, os, zlib
import numpy as np
from PIL import Image
from scipy import ndimage

from puppets import puppet_svg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACES = {int(k): v for k, v in json.load(open(os.path.join(ROOT, "scripts", "faces.json"))).items()}
PANELS = {int(k): v for k, v in json.load(open(os.path.join(ROOT, "scripts", "panels.json"))).items()}

# Corrections where clothing colour misled the detector: (page, panel, rounded cx) -> who
FIX = {(6, 0, 851): "KERBU", (10, 0, 1817): "PAUL", (10, 1, 624): "BELPAU", (22, 2, 1578): "ENILEC"}

# Expressions matching the book's drawings: (page, panel, who) -> mood
MOODS = {
    (7, 0, "EMSON"): "happy", (8, 0, "EMSON"): "happy", (8, 2, "KERBU"): "happy",
    (9, 1, "KERBU"): "angry", (9, 2, "PAUL"): "worried", (10, 0, "BELPAU"): "worried",
    (10, 1, "BELPAU"): "worried", (11, 1, "BELPAU"): "worried", (11, 2, "PAUL"): "worried",
    (12, 1, "PAUL"): "worried", (12, 1, "BELPAU"): "worried", (13, 0, "ENILEC"): "worried",
    (13, 1, "ENILEC"): "angry", (15, 0, "ENILEC"): "angry", (15, 0, "BELPAU"): "worried",
    (15, 2, "ENILEC"): "angry", (16, 1, "ENILEC"): "angry", (16, 2, "TIDIANIE"): "worried",
    (16, 3, "ENILEC"): "angry", (17, 1, "ENILEC"): "angry", (17, 2, "BELPAU"): "worried",
    (18, 0, "KERBU"): "angry", (18, 0, "ENILEC"): "angry", (18, 1, "BELPAU"): "angry",
    (20, 0, "EMSON"): "happy", (20, 0, "KERBU"): "happy",
}
for _k in [(19, i, w) for i in range(5) for w in ("PAUL", "BELPAU", "TIDIANIE", "ENILEC", "EMSON", "KERBU")] + \
          [(22, i, w) for i in range(4) for w in ("PAUL", "BELPAU", "TIDIANIE", "ENILEC", "EMSON", "KERBU")] + \
          [(21, 0, w) for w in ("PAUL", "BELPAU", "ENILEC")]:
    MOODS.setdefault(_k, "happy")

# Panels where the book draws a raised hand: (page, panel, who)
ARMS = {(11, 1, "BELPAU"), (18, 1, "BELPAU")}

PUPPET_VIEW = (-290, -270, 580, 750)  # x, y, w, h in puppet units (head radius 100)
FPS_LIP = 15


def place_puppets(page, panel):
    px, py, pw, ph = PANELS[page][panel]
    out = []
    faces = [f for f in FACES.get(page, []) if f["panel"] == panel]
    for f in faces:
        who = FIX.get((page, panel, int(round(f["cx"]))), f["who"])
        others = [g["cx"] for g in faces if g is not f]
        target = (sum(others) / len(others)) if others else (px + pw / 2)
        look = 0.0 if abs(target - f["cx"]) < 40 else (1.0 if target > f["cx"] else -1.0)
        out.append({"who": who, "cx": f["cx"], "cy": f["cy"], "k": f["r"] / 100 * 1.05, "look": look,
                    "mood": MOODS.get((page, panel, who), "neutral"), "arm": (page, panel, who) in ARMS})
    return out


def puppet_markup(pid, p, panel_rect, mood=None):
    """Absolutely-positioned <svg> for one puppet, in panel-local pixels."""
    px, py, _, _ = panel_rect
    vx, vy, vw, vh = PUPPET_VIEW
    k = p["k"]
    left = p["cx"] - px + vx * k
    top = p["cy"] - py + vy * k
    return (f'<svg class="puppet" style="left:{left:.1f}px;top:{top:.1f}px" width="{vw * k:.1f}" height="{vh * k:.1f}" '
            f'viewBox="{vx} {vy} {vw} {vh}">{puppet_svg(pid, p["who"], p["look"], mood or p["mood"], p.get("arm", False))}</svg>')


def lip_keys(samples, sr):
    """[(t, open)] at FPS_LIP from RMS loudness; open in 0..1."""
    hop = sr // FPS_LIP
    n = len(samples) // hop
    if n == 0:
        return []
    rms = np.array([np.sqrt(np.mean(samples[i * hop:(i + 1) * hop] ** 2)) for i in range(n)])
    ref = np.percentile(rms, 90) or 1.0
    lvl = np.clip(rms / ref, 0, 1) ** 0.7
    lvl[lvl < 0.18] = 0.0
    # vary shape so sustained vowels do not look frozen
    out, prev = [], -1.0
    for i, v in enumerate(lvl):
        v = round(float(v) * (0.85 + 0.15 * ((i * 7) % 3) / 2), 2)
        if abs(v - prev) >= 0.08 or i == n - 1:
            out.append((i / FPS_LIP, v)); prev = v
    out.append((n / FPS_LIP, 0.0))
    return out


def seed(*parts):
    return zlib.crc32("|".join(map(str, parts)).encode())


def blink_times(pid, start, end):
    t, i, out = start + 0.6 + (seed(pid) % 17) / 10, 0, []
    while t < end - 0.3:
        out.append(t)
        t += 2.6 + (seed(pid, i) % 23) / 10   # every 2.6-4.8 s
        i += 1
    return out


def bubble_mask(page, out_path):
    """Alpha mask (white bubbles + their outlines) for a page, saved as PNG."""
    img = np.asarray(Image.open(os.path.join(ROOT, "assets", "pages", f"pg-{page:03d}.jpg")).convert("RGB"))
    white = img.min(axis=2) > 246
    lab, _ = ndimage.label(white)
    sizes = ndimage.sum(white, lab, range(lab.max() + 1))
    keep = sizes > 9000                      # bubbles are big; eye whites are tiny
    keep[0] = False
    mask = keep[lab]
    # drop the page margin (the huge white area outside the panels)
    border = np.zeros_like(mask)
    for x, y, w, h in PANELS[page]:
        border[y + 8:y + h - 8, x + 8:x + w - 8] = True
    mask &= border
    mask = ndimage.binary_fill_holes(mask)   # include the text inside bubbles
    mask = ndimage.binary_dilation(mask, iterations=9)  # and the outline
    alpha = Image.fromarray((mask * 255).astype(np.uint8), "L").resize(
        (img.shape[1] // 2, img.shape[0] // 2), Image.BILINEAR)
    rgba = Image.new("RGBA", alpha.size, (0, 0, 0, 0))
    rgba.putalpha(alpha)                      # CSS masks read the alpha channel
    rgba.save(out_path, optimize=True)


def animate_shot(js, puppets, lines, t0, t1, sr):
    """Append GSAP tweens for one shot.

    puppets: [(pid, placement)], lines: [(speaker, start, samples)].
    Speakers move their mouth and head; listeners blink and turn to them.
    """
    by_who = {p["who"]: pid for pid, p in puppets}
    for pid, p in puppets:
        js.append(f'tl.set("#{pid}-head", {{rotation: 0, y: 0, svgOrigin: "0 110"}}, {t0:.3f});')
        for bt in blink_times(pid, t0, t1):
            js.append(f'tl.to("#{pid}-lids", {{scaleY: 1, svgOrigin: "0 -24", duration: 0.07, ease: "power1.in"}}, {bt:.3f});')
            js.append(f'tl.to("#{pid}-lids", {{scaleY: 0.001, svgOrigin: "0 -24", duration: 0.1, ease: "power1.out"}}, {bt + 0.08:.3f});')
    for spk, st, samples in lines:
        pid = by_who.get(spk)
        dur = len(samples) / sr
        if pid:
            for t, v in lip_keys(samples, sr):
                js.append(f'tl.to("#{pid}-mouth", {{scaleY: {0.14 + 0.86 * v:.2f}, svgOrigin: "0 46", duration: {1 / FPS_LIP - 0.004:.3f}, ease: "none"}}, {st + t:.3f});')
            # head: gentle nods and tilts through the line
            n = max(1, int(dur / 0.55))
            for i in range(n):
                a = ((seed(pid, st, i) % 5) - 2) * 1.1
                js.append(f'tl.to("#{pid}-head", {{rotation: {a:.2f}, y: {-4 if i % 2 == 0 else 0}, svgOrigin: "0 110", '
                          f'duration: {dur / n - 0.01:.3f}, ease: "sine.inOut"}}, {st + i * dur / n:.3f});')
            js.append(f'tl.to("#{pid}-head", {{rotation: 0, y: 0, svgOrigin: "0 110", duration: 0.25, ease: "sine.inOut"}}, {st + dur:.3f});')
            arm = next((p for q, p in puppets if q == pid and p.get("arm")), None)
            if arm:  # a small emphatic wave of the raised hand
                m = max(1, int(dur / 0.8))
                for i in range(m):
                    js.append(f'tl.to("#{pid}-arm", {{rotation: {6 if i % 2 == 0 else -2}, svgOrigin: "110 262", '
                              f'duration: {dur / m - 0.01:.3f}, ease: "sine.inOut"}}, {st + i * dur / m:.3f});')
                js.append(f'tl.to("#{pid}-arm", {{rotation: 0, svgOrigin: "110 262", duration: 0.25}}, {st + dur:.3f});')
        # listeners lean slightly toward the speaker
        for lpid, p in puppets:
            if lpid == pid:
                continue
            tilt = 2.5 * (p["look"] or 1)
            js.append(f'tl.to("#{lpid}-head", {{rotation: {tilt:.2f}, svgOrigin: "0 110", duration: 0.5, ease: "sine.inOut"}}, {st:.3f});')
            js.append(f'tl.to("#{lpid}-head", {{rotation: 0, svgOrigin: "0 110", duration: 0.25, ease: "sine.inOut"}}, {st + dur:.3f});')
