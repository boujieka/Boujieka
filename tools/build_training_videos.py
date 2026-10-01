"""Build the animated training videos (one per product and language) from the storyboards.

Usage: python tools/build_training_videos.py [--product p1|p2|p3] [--lang en|fr] [--shots-only] [--jobs N]

Step 1 renders every workbook view to PNG (sequential: LibreOffice cannot run twice on one profile).
Step 2 composes the frames with PIL and pipes them to ffmpeg (H.264, 1920x1080, 25 fps, no audio).
Outputs in marketing/videos/: {p}_{lang}.mp4, {p}_{lang}.srt and {p}_{lang}_script.md (voice-over script).
"""
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_listing_images as bli  # noqa: E402
from video_storyboards import STORYBOARDS  # noqa: E402

ROOT = bli.ROOT
OUT = ROOT / "marketing" / "videos"
CACHE = bli.TMP / "video_shots"
W, H, FPS = 1920, 1080, 25
NAVY, BG, INK, GREY = (31, 58, 95), (244, 246, 249), (33, 41, 52), (104, 116, 132)
ACCENT = {"p1": (27, 127, 121), "p2": (200, 129, 26), "p3": (107, 79, 160)}
F_BOLD, F_REG = bli.F_BOLD, bli.F_REG
AUTHOR = bli.AUTHOR_NAME

VIEW_BOX = (60, 128, 1240, 900)       # screenshot viewport
PANEL_X0, PANEL_X1 = 1290, 1860      # step panel
SUB_BOX = (0, 930, W, 1080)           # subtitle band
XFADE = int(0.4 * FPS)
ZOOM = 1.10
SS = 2                                # viewport supersampling

TXT = {
    "step": {"en": "STEP {n} OF {N}", "fr": "ÉTAPE {n} SUR {N}"},
    "training": {"en": "How to use the model", "fr": "Formation à l'utilisation du modèle"},
    "by": {"en": "By", "fr": "Par"},
    "kicker": "ENERGY ACCESS FINANCE TOOLKIT",
    "outro_head": {"en": "What you receive", "fr": "Ce que vous recevez"},
    "outro_points": {"en": ["Unlocked Excel workbook, no macros", "English and French versions", "PDF user manual with a worked example",
                            "Integrity checks built into the workbook"],
                     "fr": ["Classeur Excel déverrouillé, sans macro", "Versions française et anglaise", "Manuel PDF avec exemple commenté",
                            "Contrôles d'intégrité intégrés au classeur"]},
    "disclaimer": {"en": "Screening and pre-feasibility tool. Example values are illustrative.",
                   "fr": "Outil de présélection et de préfaisabilité. Valeurs d'exemple illustratives."},
}


def product_name(p, lg):
    g = bli.GUMROAD[p]
    return g["name"][lg], g.get("edition", {}).get(lg, "")


def title_narration(p, lg):
    name, ed = product_name(p, lg)
    full = f"{name}, {ed}" if ed else name
    if lg == "fr":
        return [f"Formation à l'utilisation du {full[0].lower() + full[1:]}.", f"Par {AUTHOR}."]
    return [f"How to use the {full}.", f"By {AUTHOR}."]


def outro_narration(p, lg):
    if lg == "fr":
        return ["Vous recevez le classeur en français et en anglais, le manuel PDF et les contrôles d'intégrité.",
                "Les valeurs de l'exemple sont illustratives : remplacez-les par les données de votre projet."]
    return ["You receive the workbook in English and French, the PDF manual and the integrity checks.",
            "The example values are illustrative: replace them with the data of your own project."]


def font(path, size, cache={}):
    key = (path, size)
    if key not in cache:
        cache[key] = ImageFont.truetype(path, size)
    return cache[key]


def mix(c1, c2, a):
    return tuple(int(round(x + (y - x) * a)) for x, y in zip(c1, c2))


def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


# ---------------------------------------------------------------- step 1: screenshots
def shot_path(p, lg, sheet, rng):
    return CACHE / f"{p}_{lg}_{sheet.replace(' ', '_').replace('&', 'and')}_{rng.replace(':', '-')}.png"


def drop_footer(img):
    """Remove the page footer (author line) at the bottom of a shot: the video header already names the author."""
    g = img.convert("L").point(lambda v: 255 if v < 235 else 0)
    rows = [g.crop((0, y, img.width, y + 1)).getbbox() is not None for y in range(img.height)]
    bottom = max(y for y, r in enumerate(rows) if r)
    top = bottom
    while top > 0 and rows[top - 1]:
        top -= 1
    gap = top
    while gap > 0 and not rows[gap - 1]:
        gap -= 1
    if bottom - top < 70 and top - gap > 40 and top > img.height * 0.85:
        return bli.crop(img.crop((0, 0, img.width, gap)))
    return img


def render_shots(p, lg):
    views = {}
    for sc in STORYBOARDS[p]:
        if isinstance(sc["view"], tuple):
            sheet, rng = sc["view"]
            if not shot_path(p, lg, sheet, rng).exists():
                views[f"v{len(views)}"] = (sheet, rng)
    if not views:
        return
    CACHE.mkdir(parents=True, exist_ok=True)
    for key, img in bli.render_views(p, lg, views=views, tag="vid").items():
        img.save(shot_path(p, lg, *views[key]))
        print("shot", p, lg, views[key], img.size, flush=True)


# ---------------------------------------------------------------- step 2: timing
def sentence_dur(s):
    return max(2.8, len(s) / 14.0 + 0.7)


def timeline(p, lg):
    """List of scenes with start, duration and timed sentences (seconds)."""
    scenes, t = [], 0.0
    board = STORYBOARDS[p]
    steps = [sc for sc in board if sc["view"] not in ("title", "outro")]
    n = 0
    for sc in board:
        v = sc["view"]
        if v == "title":
            sents = title_narration(p, lg)
        elif v == "outro":
            sents = outro_narration(p, lg)
        else:
            sents = sc["narration"][lg]
            n += 1
        lead = 0.6 if v not in ("title",) else 1.2
        cues, c = [], t + lead
        for s in sents:
            d = sentence_dur(s)
            cues.append((c, c + d, s))
            c += d
        dur = (c - t) + 0.9
        scenes.append({"sc": sc, "start": t, "dur": dur, "cues": cues, "n": n, "N": len(steps)})
        t += dur
    return scenes, t


def srt_time(x):
    ms = int(round(x * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(scenes, path):
    lines, k = [], 1
    for s in scenes:
        for a, b, txt in s["cues"]:
            lines += [str(k), f"{srt_time(a)} --> {srt_time(b - 0.05)}", txt, ""]
            k += 1
    path.write_text("\n".join(lines), encoding="utf-8")


def write_script(p, lg, scenes, total, path):
    name, ed = product_name(p, lg)
    head = f"{name}, {ed}" if ed else name
    if lg == "fr":
        out = [f"# Script de narration : {head}", "",
               f"Durée : {int(total // 60)} min {int(total % 60):02d} s. Une ligne par sous-titre, avec son minutage.",
               "Pour enregistrer une voix off, lisez chaque phrase pendant qu'elle s'affiche à l'écran.", ""]
    else:
        out = [f"# Narration script: {head}", "",
               f"Length: {int(total // 60)} min {int(total % 60):02d} s. One line per subtitle, with its timing.",
               "To record a voice-over, read each sentence while it is shown on screen.", ""]
    for s in scenes:
        v = s["sc"]["view"]
        if v == "title":
            title = TXT["training"][lg]
        elif v == "outro":
            title = TXT["outro_head"][lg]
        else:
            title = f"{TXT['step'][lg].format(n=s['n'], N=s['N']).capitalize()} : {s['sc']['title'][lg]}" if lg == "fr" \
                else f"Step {s['n']} of {s['N']}: {s['sc']['title'][lg]}"
        out += [f"## {srt_time(s['start'])[:8]}  {title}", ""]
        for a, _, txt in s["cues"]:
            out.append(f"* `{srt_time(a)[3:8]}` {txt}")
        out.append("")
    path.write_text("\n".join(out), encoding="utf-8")


# ---------------------------------------------------------------- step 3: frames
def viewport(content):
    """Pre-render the viewport (screenshot card or manual pages) at SS x resolution on the background."""
    x0, y0, x1, y1 = VIEW_BOX
    vw, vh = (x1 - x0) * SS, (y1 - y0) * SS
    canvas = Image.new("RGB", (vw, vh), BG)
    m = 40 * SS
    if isinstance(content, list):
        gap = 36 * SS
        slot = (vw - 2 * m - gap * (len(content) - 1)) // len(content)
        for k, page in enumerate(content):
            px = m + k * (slot + gap)
            bli.card(canvas, page, (px, m, px + slot, vh - m))
    else:
        bli.card(canvas, content, (m, m, vw - m, vh - m))
    return canvas


def zoomed(vp, s, cy=0.5):
    vw, vh = vp.size
    cw, ch = vw / s, vh / s
    cx0 = (vw - cw) / 2
    cy0 = max(0.0, min(vh - ch, vh * cy - ch / 2))
    out = (VIEW_BOX[2] - VIEW_BOX[0], VIEW_BOX[3] - VIEW_BOX[1])
    return vp.resize(out, Image.BILINEAR, box=(cx0, cy0, cx0 + cw, cy0 + ch))


def header(d, p, lg, progress):
    name, ed = product_name(p, lg)
    d.rectangle((0, 0, W, 84), fill=NAVY)
    label = f"{name}  |  {ed}" if ed else name
    d.text((60, 26), label, font=bli.fit_font(d, label, F_BOLD, 30, 1150), fill="white")
    a = f"{TXT['by'][lg]} {AUTHOR}"
    f = font(F_REG, 28)
    d.text((W - 60 - d.textlength(a, font=f), 29), a, font=f, fill=(201, 214, 227))
    d.rectangle((0, 84, W, 92), fill=(214, 221, 230))
    d.rectangle((0, 84, int(W * progress), 92), fill=ACCENT[p])


def subtitle(d, txt, alpha):
    if not txt or alpha <= 0:
        return
    x0, y0, x1, y1 = SUB_BOX
    d.rectangle(SUB_BOX, fill=(24, 32, 44))
    f, lines = bli.fit_lines(d, txt, F_REG, 36, W - 260, 2)
    col = mix((24, 32, 44), (255, 255, 255), alpha)
    hh = len(lines) * (f.size + 12) - 12
    y = y0 + ((y1 - y0) - hh) // 2
    for line in lines:
        d.text(((W - d.textlength(line, font=f)) / 2, y), line, font=f, fill=col)
        y += f.size + 12


def cue_at(cues, t):
    for a, b, s in cues:
        if a <= t < b:
            return s, min(1.0, (t - a) / 0.25, (b - t) / 0.25)
    return None, 0


def step_base(p, lg, s):
    """Static part of a step frame: background, panel title. Bullets and viewport are drawn per frame."""
    sc = s["sc"]
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle((PANEL_X0 - 24, 128, W - 36, 900), fill="white", outline=(222, 228, 236))
    d.rectangle((PANEL_X0 - 24, 128, PANEL_X0 - 18, 900), fill=ACCENT[p])
    d.text((PANEL_X0 + 14, 164), TXT["step"][lg].format(n=s["n"], N=s["N"]), font=font(F_BOLD, 24), fill=ACCENT[p])
    f, lines = bli.fit_lines(d, sc["title"][lg], F_BOLD, 46, PANEL_X1 - PANEL_X0 - 20, 3)
    y = bli.draw_lines(d, (PANEL_X0 + 14, 210), lines, f, INK, 10)
    d.rectangle((PANEL_X0 + 14, y + 18, PANEL_X0 + 94, y + 23), fill=ACCENT[p])
    return im, y + 64


def draw_bullets(d, p, sc, lg, y, t, dur):
    f = font(F_REG, 32)
    bl = sc["bullets"][lg]
    for k, b in enumerate(bl):
        appear = 0.8 + k * min(2.2, (dur * 0.55) / max(1, len(bl)))
        a = ease((t - appear) / 0.5)
        if a <= 0:
            break
        dx = int((1 - a) * 24)
        d.rectangle((PANEL_X0 + 14 + dx, y + 13, PANEL_X0 + 28 + dx, y + 27), fill=mix((255, 255, 255), ACCENT[p], a))
        lines = bli.wrap(d, b, f, PANEL_X1 - PANEL_X0 - 70)
        y = bli.draw_lines(d, (PANEL_X0 + 50 + dx, y), lines, f, mix((255, 255, 255), INK, a), 8) + 26
    return y


def title_frame(p, lg, t, dur, progress, outro=False):
    im = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(im)
    acc = ACCENT[p]
    name, ed = product_name(p, lg)
    a1, a2, a3 = (ease((t - k) / 0.6) for k in (0.2, 0.7, 1.2))
    d.rectangle((0, 0, int(W * progress), 8), fill=acc)
    top, size, esize = (90, 60, 42) if outro else (150, 82, 52)
    d.text((140, top), TXT["kicker"], font=font(F_REG, 30), fill=mix(NAVY, (170, 190, 212), a1))
    d.rectangle((140, top + 50, 140 + int(140 * a1), top + 57), fill=acc)
    f, lines = bli.fit_lines(d, name, F_BOLD, size, W - 280, 2)
    y = bli.draw_lines(d, (140, top + 100), lines, f, mix(NAVY, (255, 255, 255), a1), 10)
    if ed:
        y = bli.draw_lines(d, (140, y + 6), [ed], font(F_BOLD, esize), mix(NAVY, mix((255, 255, 255), acc, 0.45), a1), 0)
    if not outro:
        d.text((140, y + 50), TXT["training"][lg], font=font(F_REG, 44), fill=mix(NAVY, (201, 214, 227), a2))
    else:
        f2 = font(F_REG, 34)
        yy = y + 36
        d.text((140, yy), TXT["outro_head"][lg], font=font(F_BOLD, 40), fill=mix(NAVY, (201, 214, 227), a2))
        yy += 62
        for k, pt in enumerate(TXT["outro_points"][lg]):
            a = ease((t - 1.0 - 0.45 * k) / 0.5)
            d.rectangle((146, yy + 12, 160, yy + 26), fill=mix(NAVY, acc, a))
            d.text((186, yy), pt, font=f2, fill=mix(NAVY, (255, 255, 255), a))
            yy += 50
        d.text((140, 862), TXT["disclaimer"][lg], font=font(F_REG, 28), fill=mix(NAVY, (150, 168, 190), a3))
    by = f"{TXT['by'][lg]} {AUTHOR}"
    fb = bli.fit_font(d, by, F_BOLD, 64, W - 280)
    d.rectangle((140, 742, 146, 820), fill=mix(NAVY, acc, a3))
    d.text((172, 744), by, font=fb, fill=mix(NAVY, (255, 255, 255), a3))
    return im


def build_video(p, lg):
    scenes, total = timeline(p, lg)
    OUT.mkdir(parents=True, exist_ok=True)
    write_srt(scenes, OUT / f"{p}_{lg}.srt")
    write_script(p, lg, scenes, total, OUT / f"{p}_{lg}_script.md")
    mp4 = OUT / f"{p}_{lg}.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p",
                           "-movflags", "+faststart", "-metadata", f"artist={AUTHOR}", str(mp4)], stdin=subprocess.PIPE)
    prev, frames = None, 0
    manual = None
    for s in scenes:
        sc, v = s["sc"], s["sc"]["view"]
        nf = int(round((s["start"] + s["dur"]) * FPS)) - int(round(s["start"] * FPS))
        if isinstance(v, tuple) or v == "manual":
            if v == "manual":
                manual = manual or bli.manual_strip(p, lg)
                vp = viewport(manual)
            else:
                vp = viewport(drop_footer(Image.open(shot_path(p, lg, *v)).convert("RGB")))
            base, by = step_base(p, lg, s)
        last = None
        for i in range(nf):
            t = i / FPS
            gt = s["start"] + t
            progress = gt / total
            if v in ("title", "outro"):
                im = title_frame(p, lg, t, s["dur"], progress, outro=(v == "outro"))
                d = ImageDraw.Draw(im)
            else:
                im = base.copy()
                d = ImageDraw.Draw(im)
                z = 1.0 + (ZOOM - 1.0) * ease(t / s["dur"])
                im.paste(zoomed(vp, z, 0.5 - 0.06 * ease(t / s["dur"])), VIEW_BOX[:2])
                draw_bullets(d, p, sc, lg, by, t, s["dur"])
                header(d, p, lg, progress)
            txt, a = cue_at(s["cues"], gt)
            subtitle(d, txt, a)
            if prev is not None and i < XFADE:
                im = Image.blend(prev, im, ease((i + 1) / XFADE))
            ff.stdin.write(im.tobytes())
            last = im
            frames += 1
        prev = last
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg failed for {p} {lg}")
    return f"{mp4.name}: {frames} frames, {total:.1f} s"


def main():
    args = sys.argv[1:]
    lang = args[args.index("--lang") + 1] if "--lang" in args else "all"
    prod = args[args.index("--product") + 1] if "--product" in args else "all"
    jobs = int(args[args.index("--jobs") + 1]) if "--jobs" in args else 3
    langs = ["en", "fr"] if lang == "all" else [lang]
    prods = list(STORYBOARDS) if prod == "all" else [prod]
    pairs = [(p, lg) for p in prods for lg in langs]
    for p, lg in pairs:
        render_shots(p, lg)
    if "--shots-only" in args:
        return
    for p, lg in pairs:  # manual pages are rendered once, before the parallel step
        bli.manual_strip(p, lg)
    with ProcessPoolExecutor(jobs) as ex:
        for msg in ex.map(build_video, *zip(*pairs)):
            print(msg, flush=True)


if __name__ == "__main__":
    main()
