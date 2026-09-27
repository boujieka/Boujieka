"""Build the motion-comic composition from scripts/storyboard.py.

Steps: synthesize each line (cached) -> lay out the timeline from the audio
lengths -> mix one narration track -> write captions.srt -> write index.html.

Run with a Python that has kokoro-onnx, soundfile and numpy:
    python scripts/build.py
"""
import hashlib, html, json, os, subprocess, sys
import numpy as np
import soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from storyboard import SHOTS, VOICES  # noqa: E402

W, H = 1920, 1080
SR = 24000
MODEL = os.path.expanduser("~/.cache/hyperframes/tts/models/kokoro-v1.0.onnx")
VOICEPACK = os.path.expanduser("~/.cache/hyperframes/tts/voices/voices-v1.0.bin")
LINES_DIR = os.path.join(ROOT, "assets", "audio", "lines")
PANELS = {int(k): v for k, v in json.load(open(os.path.join(ROOT, "scripts", "panels.json"))).items()}

MOVE = 1.0        # camera travel between panels
SPEECH_IN = 0.75  # first line starts this long after a shot begins
GAP = 0.3         # silence between lines
TAIL = 0.85       # hold after the last line
FIT = 0.94        # panel fills this share of the frame

SPEAKERS = {
    "BELPAU": ("BELPAU", "Analyst, KivoElec"),
    "ENILEC": ("ENILEC MOK", "Director of Public Debt, Ministry of Finance"),
    "KERBU": ("MINISTER KERBU", "Minister of Energy"),
    "EMSON": ("EMSON ANAHCT", "CEO, SunRiver Power"),
    "TIDIANIE": ("TIDIANIE EUGOM", "Investment Officer, development finance institution"),
    "PAUL": ("PAUL AHMAK", "Managing Director, KivoElec"),
    "RESIDENT": ("RESIDENT", "Kivona"),
}

_kokoro = None


def tts(voice_key, text):
    voice = VOICES[voice_key]
    key = hashlib.sha1(f"{voice}|{text}".encode()).hexdigest()[:16]
    path = os.path.join(LINES_DIR, f"{key}.wav")
    if not os.path.exists(path):
        global _kokoro
        if _kokoro is None:
            from kokoro_onnx import Kokoro
            _kokoro = Kokoro(MODEL, VOICEPACK)
        lang = "en-gb" if voice.startswith("b") else "en-us"
        samples, sr = _kokoro.create(text, voice=voice, speed=1.0, lang=lang)
        assert sr == SR
        sf.write(path, samples, sr)
    data, _ = sf.read(path, dtype="float32")
    return path, data


def rect_of(shot):
    kind, page = shot[0], shot[1]
    if kind == "panel":
        return PANELS[page][shot[2]]
    if kind == "group":
        bs = [PANELS[page][i] for i in shot[2]]
        x0 = min(b[0] for b in bs); y0 = min(b[1] for b in bs)
        x1 = max(b[0] + b[2] for b in bs); y1 = max(b[1] + b[3] for b in bs)
        return [x0, y0, x1 - x0, y1 - y0]
    raise ValueError(kind)


def cam(rect, zoom=1.0, fit=FIT):
    x, y, w, h = rect
    s = min(W * fit / w, H * fit / h) * zoom
    return {"x": round(W / 2 - s * (x + w / 2), 2), "y": round(H / 2 - s * (y + h / 2), 2),
            "scale": round(s, 5), "mw": round(s * w, 1), "mh": round(s * h, 1)}


def fmt_srt(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    os.makedirs(LINES_DIR, exist_ok=True)
    t = 0.0
    timeline = []   # dicts with start, dur, shot, lines[(speaker,text,start,dur,path)]
    for shot in SHOTS:
        lines = shot[-1]
        kind = shot[0]
        lead = 0.6 if kind == "card" else SPEECH_IN
        cur = t + lead
        placed = []
        for spk, text in lines:
            path, data = tts(spk, text)
            d = len(data) / SR
            placed.append((spk, text, cur, d, data))
            cur += d + GAP
        end = (cur - GAP + TAIL) if placed else t + 7.0
        dur = max(end - t, 3.0 if kind != "card" else 3.2)
        if kind == "card" and shot[1] == "title":
            dur = max(dur, 6.0)
        timeline.append({"start": round(t, 3), "dur": round(dur, 3), "shot": shot, "lines": placed})
        t += dur
    total = round(t, 3)

    # ---- narration mix ----
    mix = np.zeros(int((total + 1) * SR), dtype=np.float32)
    for seg in timeline:
        for _, _, st, _, data in seg["lines"]:
            i = int(round(st * SR)); mix[i:i + len(data)] += data
    peak = float(np.max(np.abs(mix))) or 1.0
    mix *= min(1.0, 0.89 / peak)
    wav = os.path.join(LINES_DIR, "_narration.wav")
    sf.write(wav, mix[: int(total * SR)], SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-c:a", "aac", "-b:a", "160k",
                    os.path.join(ROOT, "assets", "audio", "narration.m4a")], check=True)

    # ---- captions ----
    srt, n = [], 0
    for seg in timeline:
        for spk, text, st, d, _ in seg["lines"]:
            n += 1
            shown = text.replace("M-O-U", "MoU").replace("P-P-A", "PPA").replace("I-P-P", "IPP").replace("C.E.O.", "CEO")
            who = SPEAKERS[spk][0].title() + ": " if spk in SPEAKERS else ""
            srt.append(f"{n}\n{fmt_srt(st)} --> {fmt_srt(st + d)}\n{who}{shown}\n")
    open(os.path.join(ROOT, "captions.srt"), "w").write("\n".join(srt))

    write_html(timeline, total)
    print(f"shots={len(timeline)} lines={n} total={total:.1f}s")


# ---------------------------------------------------------------- HTML
def write_html(timeline, total):
    pages = sorted({seg["shot"][1] for seg in timeline if seg["shot"][0] != "card"})
    # page visibility windows (merge consecutive shots on one page)
    windows = []
    for i, seg in enumerate(timeline):
        s = seg["shot"]
        if s[0] == "card":
            continue
        if windows and windows[-1]["page"] == s[1] and windows[-1]["last"] == i - 1:
            windows[-1]["end"] = seg["start"] + seg["dur"]; windows[-1]["last"] = i
        else:
            windows.append({"page": s[1], "start": seg["start"], "end": seg["start"] + seg["dur"], "first": i, "last": i})

    body, js = [], []
    X = 0.6  # crossfade
    for k, w in enumerate(windows):
        st = max(0, w["start"] - X / 2); en = min(total, w["end"] + X / 2)
        w["id"] = f"p{k}"
        body.append(f'      <div id="{w["id"]}" class="clip page" data-start="{st:.3f}" data-duration="{en - st:.3f}" data-track-index="1">'
                    f'<div class="cam"><img src="assets/pages/pg-{w["page"]:03d}.jpg" alt="" /></div></div>')
        js.append(f'tl.fromTo("#{w["id"]}", {{opacity: 0}}, {{opacity: 1, duration: {X}, ease: "power1.inOut"}}, {st:.3f});')
        js.append(f'tl.to("#{w["id"]}", {{opacity: 0, duration: {X}, ease: "power1.inOut"}}, {en - X:.3f});')

    # camera + focus mask per shot
    prev_page = None
    for i, seg in enumerate(timeline):
        s = seg["shot"]; st, dur = seg["start"], seg["dur"]
        if s[0] == "card":
            prev_page = None
            continue
        win = next(w for w in windows if w["first"] <= i <= w["last"])
        sel = f'#{win["id"]} .cam'
        if s[0] == "pan":
            a = cam(s[2], fit=1.0); b = cam(s[3], fit=1.0)
            a["mw"], a["mh"] = a["mw"], H; b["mw"], b["mh"] = b["mw"], H
            start_state, hold_state = a, b
        else:
            r = rect_of(s)
            start_state, hold_state = cam(r, 1.0), cam(r, 1.035)
        if prev_page != win["id"]:
            intro = cam(rect_of(s), 0.93) if s[0] != "pan" else start_state
            js.append(f'tl.set("{sel}", {{x: {intro["x"]}, y: {intro["y"]}, scale: {intro["scale"]}}}, {max(0, st - X / 2):.3f});')
            js.append(f'tl.set(".focus", {{width: {intro["mw"]}, height: {intro["mh"]}}}, {max(0, st - X / 2):.3f});')
        move = MOVE
        js.append(f'tl.to("{sel}", {{x: {start_state["x"]}, y: {start_state["y"]}, scale: {start_state["scale"]}, duration: {move}, ease: "power2.inOut"}}, {st:.3f});')
        js.append(f'tl.to(".focus", {{width: {start_state["mw"]}, height: {start_state["mh"]}, duration: {move}, ease: "power2.inOut"}}, {st:.3f});')
        hold = max(0.1, dur - move - 0.02)  # end just before the next shot's tween
        ease = "sine.inOut" if s[0] == "pan" else "none"
        js.append(f'tl.to("{sel}", {{x: {hold_state["x"]}, y: {hold_state["y"]}, scale: {hold_state["scale"]}, duration: {hold:.3f}, ease: "{ease}"}}, {st + move:.3f});')
        js.append(f'tl.to(".focus", {{width: {hold_state["mw"]}, height: {hold_state["mh"]}, duration: {hold:.3f}, ease: "{ease}"}}, {st + move:.3f});')
        prev_page = win["id"]

    body.append(f'      <div id="focus-wrap" class="clip focus-wrap" data-start="0" data-duration="{total:.3f}" data-track-index="2"><div class="focus"></div></div>')

    # speaker tags
    for key, (name, role) in SPEAKERS.items():
        js.append(f'tl.set("#tag-{key}", {{opacity: 0, x: -24}}, 0);')
        body.append(f'      <div class="clip tag" id="tag-{key}" data-start="0" data-duration="{total:.3f}" data-track-index="3">'
                    f'<b>{html.escape(name)}</b><span>{html.escape(role)}</span></div>')
    for seg in timeline:
        if seg["shot"][0] == "card":
            continue
        for spk, _, st, d, _ in seg["lines"]:
            if spk in SPEAKERS:
                js.append(f'tl.to("#tag-{spk}", {{opacity: 1, x: 0, duration: 0.3, ease: "power2.out"}}, {st - 0.15:.3f});')
                js.append(f'tl.to("#tag-{spk}", {{opacity: 0, x: -24, duration: 0.25}}, {st + d + 0.05:.3f});')

    # cards
    for i, seg in enumerate(timeline):
        s = seg["shot"]
        if s[0] != "card":
            continue
        cid = f"c{i}"; st, dur = seg["start"], seg["dur"]
        body.append(card_html(cid, s[1], s[2], st, dur))
        js.append(f'tl.set("#{cid}", {{opacity: 0}}, 0);')
        js.append(f'tl.to("#{cid}", {{opacity: 1, duration: 0.5}}, {st:.3f});')
        if i < len(timeline) - 1:
            js.append(f'tl.to("#{cid}", {{opacity: 0, duration: 0.5}}, {st + dur - 0.5:.3f});')
        js.append(f'tl.from("#{cid} .in", {{y: 36, opacity: 0, duration: 0.7, stagger: 0.18, ease: "power3.out"}}, {st + 0.2:.3f});')
        js.append(f'tl.fromTo("#{cid} .bar", {{scaleX: 0}}, {{scaleX: 1, duration: 0.7, ease: "power3.inOut"}}, {st + 0.35:.3f});')

    body.append(f'      <audio id="vo" src="assets/audio/narration.m4a" data-start="0" data-duration="{total:.3f}" data-track-index="4" data-volume="1"></audio>')

    tpl = open(os.path.join(ROOT, "scripts", "template.html")).read()
    out = (tpl.replace("{{TOTAL}}", f"{total:.3f}")
              .replace("{{BODY}}", "\n".join(body))
              .replace("{{JS}}", "\n      ".join(js)))
    open(os.path.join(ROOT, "index.html"), "w").write(out)


def card_html(cid, kind, data, st, dur):
    a = f'id="{cid}" class="clip card {kind}" data-start="{st:.3f}" data-duration="{dur:.3f}" data-track-index="5"'
    if kind == "title":
        inner = ('<div class="kicker in">A CAPACITY BUILDING SERIES ON AFRICA\'S POWER DEALS</div>'
                 '<div class="t1 in">BANKABLE</div><div class="t2 in">IS NOT ENOUGH</div>'
                 '<div class="bar"></div><div class="ep in">EPISODE 1: THE SIGNING</div>'
                 '<img class="lineup in" src="assets/art/cast-lineup.png" alt="" />'
                 '<div class="author in">EMMANUEL BOUJIEKA KAMGA</div>')
    elif kind == "chapter":
        inner = (f'<div class="num in">{html.escape(data["n"])}</div><div class="bar"></div>'
                 f'<div class="ct in">{html.escape(data["title"])}</div>'
                 '<div class="series in">BANKABLE IS NOT ENOUGH | EPISODE 1</div>')
    elif kind == "section":
        inner = (f'<div class="ct in">{html.escape(data["title"])}</div><div class="bar"></div>'
                 '<div class="series in">BANKABLE IS NOT ENOUGH | EPISODE 1</div>')
    elif kind == "end":
        inner = ('<div class="q in">Bankable is the start.</div><div class="q in accent">Sustainable is the goal.</div>'
                 '<div class="bar"></div><div class="series in">END OF EPISODE 1: THE SIGNING</div>')
    elif kind == "credits":
        inner = ('<div class="ct small in">BANKABLE IS NOT ENOUGH</div>'
                 '<div class="series in">EPISODE 1: THE SIGNING</div><div class="bar"></div>'
                 '<p class="in">Story, text and illustrations &copy; 2026 Emmanuel Boujieka Kamga. All rights reserved.</p>'
                 '<p class="in">This is a work of fiction. Kivona, KivoElec, SunRiver Power and all characters are invented.'
                 ' All figures are illustrative.</p>'
                 '<p class="in">For education and capacity building. Not legal, financial or investment advice.</p>'
                 '<p class="in dim">Voices are synthetic (Kokoro-82M).</p>')
    else:
        raise ValueError(kind)
    return f'      <section {a}><div class="inner">{inner}</div></section>'


if __name__ == "__main__":
    main()
