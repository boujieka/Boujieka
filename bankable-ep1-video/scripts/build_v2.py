"""Build the v2 videos: training (16:9) and short (9:16).

    python scripts/build_v2.py training   ->  ../bankable-ep1-training/
    python scripts/build_v2.py short      ->  ../bankable-ep1-short/

Each output is its own HyperFrames project (assets symlinked to this one) with
index.html, audio/mix.m4a (voice + music), captions.srt and chapters.txt.
"""
import html, importlib, json, os, re, subprocess, sys
import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build import tts, SR, PANELS, puppet_layer, pid_for  # noqa: E402
from animate import place_puppets, animate_shot  # noqa: E402
from puppets import puppet_svg  # noqa: E402
from v2cards import ROLES  # noqa: E402
import music  # noqa: E402

ROOT = os.path.dirname(HERE)

CONFIGS = {
    "training": {"story": "story_training", "out": "bankable-ep1-training", "W": 1920, "H": 1080,
                 "region": (0, 64, 1920, 1016), "captions": False, "title": "Bankable Is Not Enough - Episode 1 (Training)"},
    "short": {"story": "story_short", "out": "bankable-ep1-short", "W": 1080, "H": 1920,
              "region": (0, 250, 1080, 880), "captions": True, "title": "Bankable Is Not Enough - Episode 1 (Short)"},
}

GAP, FIT = 0.3, 0.95


def spoken_to_text(t):
    for a, b in [("M-O-Us", "MoUs"), ("M-O-U", "MoU"), ("P-P-A", "PPA"), ("I-P-Ps", "IPPs"), ("I-P-P", "IPP"),
                 ("U.S. cents", "US cents"), ("C.E.O.", "CEO")]:
        t = t.replace(a, b)
    return t


def cam(rect, region, zoom=1.0, fit=FIT):
    rx, ry, rw, rh = region
    x, y, w, h = rect
    s = min(rw * fit / w, rh * fit / h) * zoom
    return {"x": round(rx + rw / 2 - s * (x + w / 2), 2), "y": round(ry + rh / 2 - s * (y + h / 2), 2),
            "scale": round(s, 5), "mw": round(s * w, 1), "mh": round(s * h, 1)}


def fmt_srt(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def layout(shots):
    """Assign times to every shot, part and line."""
    t, out, chapter = 0.0, [], None
    for shot in shots:
        seg = {"shot": shot, "start": t, "lines": []}
        if shot.get("chapter") is not None:
            chapter = shot["chapter"]
        seg["chapter"] = chapter
        if shot["kind"] in ("panel", "pan"):
            cut = shot.get("cut")
            cur = t + (0.35 if cut else 0.8)
            for spk, text in shot["lines"]:
                d = len(tts(spk, text)[1]) / SR
                seg["lines"].append((spk, text, cur, d)); cur += d + GAP
            seg["dur"] = max(2.2, cur - GAP + 0.7 - t)
        else:
            cur = t + 0.45
            seg["parts"] = []
            for p in shot["parts"]:
                ps = cur
                if p["lines"]:
                    cur += 0.3
                    for spk, text in p["lines"]:
                        d = len(tts(spk, text)[1]) / SR
                        seg["lines"].append((spk, text, cur, d)); cur += d + GAP
                    cur += p["hold"] - GAP
                elif p["countdown"]:
                    cur += 0.3 + p["countdown"]
                else:
                    cur += max(0.3, p["hold"])
                seg["parts"].append((ps, cur))
            seg["dur"] = cur + shot.get("tail", 0.9) - t
        seg["dur"] = round(seg["dur"], 3)
        out.append(seg); t += seg["dur"]
    return out, round(t, 3)


def music_plan(segs):
    cues, stings = [], []
    for seg in segs:
        sh, st, en = seg["shot"], seg["start"], seg["start"] + seg["dur"]
        if sh["kind"] == "screen" and sh["layout"] == "stop":
            # drone while the situation is read; silence for the question and the pause
            parts = seg["parts"]; opt_i = next(i for i, p in enumerate(sh["parts"]) if "stop-opts" in p["html"])
            after = next((i for i, p in enumerate(sh["parts"]) if "stop-after" in p["html"]), None)
            cues.append((st, parts[opt_i - 1][0], "drone"))
            cues.append((parts[opt_i - 1][0], parts[after][0] if after else en, "silence"))
            if after:
                cues.append((parts[after][0], en, "bed"))
            continue
        cues.append((st, en, sh.get("music", "bed")))
        if sh.get("sting"):
            stings.append((st + (0.25 if sh["kind"] == "screen" and sh["layout"] in ("act", "title", "lesson", "redteam") else 0.6),
                           "act" if sh["sting"] == "act" else "risk"))
    return cues, stings


def main(which):
    cfg = CONFIGS[which]
    W, H, region = cfg["W"], cfg["H"], cfg["region"]
    story = importlib.import_module(cfg["story"])
    segs, total = layout(story.SHOTS)
    out = os.path.join(os.path.dirname(ROOT), cfg["out"])
    os.makedirs(os.path.join(out, "audio"), exist_ok=True)
    link = os.path.join(out, "assets")
    if not os.path.islink(link):
        os.symlink("../bankable-ep1-video/assets", link)

    # ---------------- audio: voice + music -> stereo 48 kHz AAC
    voice = np.zeros(int((total + 1) * SR), np.float32)
    for seg in segs:
        for spk, text, st, _ in seg["lines"]:
            _, d = tts(spk, text); i = int(round(st * SR)); voice[i:i + len(d)] += d
    voice = voice[:int(total * SR)]
    voice *= 0.89 / (float(np.max(np.abs(voice))) or 1)
    cues, stings = music_plan(segs)
    score = music.render_score(total, cues, stings, voice)
    mix = voice + score[:len(voice)]
    mix *= min(1.0, 0.97 / float(np.max(np.abs(mix))))
    st48 = resample_poly(mix, 2, 1).astype(np.float32)
    wav = os.path.join(out, "audio", "_mix.wav")
    sf.write(wav, np.stack([st48, st48], axis=1), 48000)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-c:a", "aac", "-b:a", "192k",
                    os.path.join(out, "audio", "mix.m4a")], check=True)
    os.remove(wav)

    # ---------------- captions + chapters
    srt, n = [], 0
    for seg in segs:
        for spk, text, st, d in seg["lines"]:
            n += 1
            who = ROLES[spk][0].title() + ": " if spk in ROLES else ""
            srt.append(f"{n}\n{fmt_srt(st)} --> {fmt_srt(st + d)}\n{who}{spoken_to_text(text)}\n")
    open(os.path.join(out, "captions.srt"), "w").write("\n".join(srt))
    chap = []
    names = {"title": "Title", "ladder": "Bankable vs sustainable", "checklist": "Before you sign",
             "redteam": "Red team", "lesson": "The lesson"}
    for seg in segs:
        sh = seg["shot"]
        if sh["kind"] != "screen" or sh["layout"] not in ("act", *names):
            continue
        if sh["layout"] == "act":
            label = " ".join(re.sub("<[^>]+>", " ", sh["parts"][0]["html"] + " - " + sh["parts"][1]["html"]).split()).title()
        else:
            label = names[sh["layout"]]
        m, s_ = divmod(int(seg["start"]), 60)
        chap.append(f"{m:02d}:{s_:02d} {label}")
    if not chap or not chap[0].startswith("00:00"):
        chap.insert(0, "00:00 Cold open")
    open(os.path.join(out, "chapters.txt"), "w").write("\n".join(chap) + "\n")

    write_html(cfg, story, segs, total, out)
    for f, src in [("package.json", None), ("hyperframes.json", None)]:
        p = os.path.join(ROOT, f)
        txt = open(p).read().replace("bankable-ep1-video", cfg["out"])
        open(os.path.join(out, f), "w").write(txt)
    json.dump({"id": cfg["out"], "name": cfg["title"]}, open(os.path.join(out, "meta.json"), "w"), indent=2)
    print(f"{which}: shots={len(segs)} lines={n} total={total:.1f}s -> {out}")


# ======================================================================== HTML
def write_html(cfg, story, segs, total, out):
    W, H, region = cfg["W"], cfg["H"], cfg["region"]
    body, js = [], []
    X = 0.5

    # page windows: consecutive panel shots on one page share a layer
    wins = []
    for i, seg in enumerate(segs):
        sh = seg["shot"]
        if sh["kind"] == "screen":
            continue
        if wins and wins[-1]["page"] == sh["page"] and wins[-1]["last"] == i - 1:
            wins[-1]["end"] = seg["start"] + seg["dur"]; wins[-1]["last"] = i
        else:
            wins.append({"page": sh["page"], "start": seg["start"], "end": seg["start"] + seg["dur"], "first": i, "last": i})
    for k, w in enumerate(wins):
        w["id"] = f"p{k}"
        st = max(0, w["start"] - X / 2); en = min(total, w["end"] + X / 2)
        body.append(f'<div id="{w["id"]}" class="clip page" data-start="{st:.3f}" data-duration="{en - st:.3f}" data-track-index="1">'
                    f'<div class="cam"><img src="assets/pages/pg-{w["page"]:03d}.jpg" alt="" />{puppet_layer(w["id"], w["page"])}</div></div>')
        js.append(f'tl.set("#{w["id"]}", {{opacity: 0}}, 0);')
        js.append(f'tl.to("#{w["id"]}", {{opacity: 1, duration: {X}, ease: "power1.inOut"}}, {st:.3f});')
        js.append(f'tl.to("#{w["id"]}", {{opacity: 0, duration: {X}, ease: "power1.inOut"}}, {en - X:.3f});')

    rx, ry, rw, rh = region
    body.append(f'<div id="focus-wrap" class="clip focus-wrap" data-start="0" data-duration="{total:.3f}" data-track-index="2">'
                f'<div class="focus" style="left:{rx + rw / 2}px;top:{ry + rh / 2}px"></div></div>')

    prev = None
    for i, seg in enumerate(segs):
        sh = seg["shot"]; st, dur = seg["start"], seg["dur"]
        if sh["kind"] == "screen":
            prev = None
            continue
        win = next(w for w in wins if w["first"] <= i <= w["last"])
        sel = f'#{win["id"]} .cam'
        if sh["kind"] == "pan":
            a = cam(sh["a"], region, fit=1.0); b = cam(sh["b"], region, fit=1.0)
            a["mh"] = b["mh"] = rh
            s0, s1 = a, b
        else:
            r = PANELS[sh["page"]][sh["panel"]]
            s0, s1 = cam(r, region), cam(r, region, 1.035)
        move = 0.001 if sh.get("cut") else 1.0
        if prev != win["id"]:
            intro = s0 if sh["kind"] == "pan" or sh.get("cut") else cam(PANELS[sh["page"]][sh["panel"]], region, 0.93)
            t0 = max(0, st - X / 2)
            js.append(f'tl.set("{sel}", {{x: {intro["x"]}, y: {intro["y"]}, scale: {intro["scale"]}}}, {t0:.3f});')
            js.append(f'tl.set(".focus", {{width: {intro["mw"]}, height: {intro["mh"]}}}, {t0:.3f});')
        if sh.get("cut"):
            js.append(f'tl.set("{sel}", {{x: {s0["x"]}, y: {s0["y"]}, scale: {s0["scale"]}}}, {st:.3f});')
            js.append(f'tl.set(".focus", {{width: {s0["mw"]}, height: {s0["mh"]}}}, {st:.3f});')
        else:
            js.append(f'tl.to("{sel}", {{x: {s0["x"]}, y: {s0["y"]}, scale: {s0["scale"]}, duration: {move}, ease: "power2.inOut"}}, {st:.3f});')
            js.append(f'tl.to(".focus", {{width: {s0["mw"]}, height: {s0["mh"]}, duration: {move}, ease: "power2.inOut"}}, {st:.3f});')
        hold = max(0.1, dur - move - 0.03)
        ease = "sine.inOut" if sh["kind"] == "pan" else "none"
        js.append(f'tl.to("{sel}", {{x: {s1["x"]}, y: {s1["y"]}, scale: {s1["scale"]}, duration: {hold:.3f}, ease: "{ease}"}}, {st + move + 0.01:.3f});')
        js.append(f'tl.to(".focus", {{width: {s1["mw"]}, height: {s1["mh"]}, duration: {hold:.3f}, ease: "{ease}"}}, {st + move + 0.01:.3f});')
        prev = win["id"]
        if sh["kind"] == "panel":
            pups = [(pid_for(win["id"], sh["page"], sh["panel"], j), p) for j, p in enumerate(place_puppets(sh["page"], sh["panel"]))]
            if pups:
                lines = [(spk, lst, tts(spk, text)[1]) for spk, text, lst, _ in seg["lines"]]
                animate_shot(js, pups, lines, st, st + dur, SR)

    # ---------------- screens
    for i, seg in enumerate(segs):
        sh = seg["shot"]
        if sh["kind"] != "screen":
            continue
        sid = f"s{i}"; st, dur = seg["start"], seg["dur"]
        parts_html = []
        for j, p in enumerate(sh["parts"]):
            h = p["html"]
            h = re.sub(r'<div class="pup" data-who="(\w+)"></div>',
                       lambda m: f'<svg class="pup" viewBox="-290 -270 580 690">{puppet_svg(f"{sid}{m.group(1)}", m.group(1), 0, "neutral")}</svg>', h)
            if '<div class="lineup"></div>' in h:
                h = h.replace('<div class="lineup"></div>', '<div class="lineup">' + "".join(
                    f'<svg viewBox="-290 -270 580 690">{puppet_svg(f"{sid}t{k}", w, 0, "happy")}</svg>'
                    for k, w in enumerate(["BELPAU", "ENILEC", "KERBU", "EMSON", "TIDIANIE", "PAUL"])) + '</div>')
            if p["countdown"]:
                h += f'<div class="count" id="{sid}c">' + "".join(
                    f'<span id="{sid}c{k}">{k}</span>' for k in range(p["countdown"], 0, -1)) + '</div>'
            parts_html.append(f'<div class="part {p["cls"]}" id="{sid}p{j}">{h}</div>')
        body.append(f'<section id="{sid}" class="clip screen l-{sh["layout"]} c-{sh["code"] or "none"}" '
                    f'data-start="{max(0, st - 0.3):.3f}" data-duration="{dur + min(st, 0.3):.3f}" data-track-index="5">'
                    f'<div class="inner">{"".join(parts_html)}</div></section>')
        js.append(f'tl.set("#{sid}", {{opacity: 0}}, 0);')
        js.append(f'tl.to("#{sid}", {{opacity: 1, duration: 0.35}}, {max(0, st - 0.3):.3f});')  # overlap the outgoing shot
        if i < len(segs) - 1:
            js.append(f'tl.to("#{sid}", {{opacity: 0, duration: 0.35}}, {st + dur - 0.35:.3f});')
        for j, (ps, pe) in enumerate(seg["parts"]):
            js.append(f'tl.set("#{sid}p{j}", {{opacity: 0, y: 26}}, 0);')
            js.append(f'tl.to("#{sid}p{j}", {{opacity: 1, y: 0, duration: 0.45, ease: "power2.out"}}, {max(st, ps):.3f});')
            p = sh["parts"][j]
            if p["countdown"]:
                for k in range(p["countdown"]):
                    cs = ps + 0.3 + k
                    js.append(f'tl.set("#{sid}c{p["countdown"] - k}", {{opacity: 0, scale: 1.4}}, 0);')
                    js.append(f'tl.to("#{sid}c{p["countdown"] - k}", {{opacity: 1, scale: 1, duration: 0.25}}, {cs:.3f});')
                    js.append(f'tl.to("#{sid}c{p["countdown"] - k}", {{opacity: 0, duration: 0.2}}, {cs + 0.78:.3f});')
        if sh["layout"] == "ladder":
            # the yes/no marks land after each step is read
            pass

    # ---------------- chapter indicator
    chapters = story.CHAPTERS
    changes = []
    for seg in segs:
        if seg["chapter"] is not None and (not changes or changes[-1][1] != seg["chapter"]):
            changes.append((seg["start"], seg["chapter"]))
    first = changes[0][0] if changes else total
    items = "".join(f'<div class="ch" id="ch{k}"><span>{k + 1:02d}</span>{html.escape(c)}</div>' for k, c in enumerate(chapters))
    body.append(f'<div id="chapbar" class="clip chapbar" data-start="{first:.3f}" data-duration="{total - first:.3f}" data-track-index="3">{items}</div>')
    js.append('tl.set("#chapbar", {opacity: 0}, 0);')
    js.append(f'tl.to("#chapbar", {{opacity: 1, duration: 0.6}}, {first:.3f});')
    for k in range(len(chapters)):
        js.append(f'tl.set("#ch{k}", {{opacity: 0.4}}, 0);')
    last = None
    for t, c in changes:
        if last is not None:
            js.append(f'tl.to("#ch{last}", {{opacity: 0.4, duration: 0.4}}, {t:.3f});')
            js.append(f'tl.to("#ch{last} span", {{backgroundColor: "rgba(255,255,255,0.12)", color: "#fdfbf5", duration: 0.4}}, {t:.3f});')
        js.append(f'tl.to("#ch{c}", {{opacity: 1, duration: 0.4}}, {t + 0.01:.3f});')
        js.append(f'tl.to("#ch{c} span", {{backgroundColor: "#f0b429", color: "#1d2230", duration: 0.4}}, {t + 0.01:.3f});')
        last = c

    # ---------------- speaker tags (with the character's risk role) + captions
    for key, (name, role) in ROLES.items():
        js.append(f'tl.set("#tag-{key}", {{opacity: 0, x: -24}}, 0);')
        body.append(f'<div class="clip tag" id="tag-{key}" data-start="0" data-duration="{total:.3f}" data-track-index="4">'
                    f'<b>{html.escape(name)}</b><span>{html.escape(role)}</span></div>')
    cap_n = 0
    for seg in segs:
        panel_shot = seg["shot"]["kind"] != "screen"
        for spk, text, st, d in seg["lines"]:
            dd = d
            if panel_shot and spk in ROLES:
                js.append(f'tl.to("#tag-{spk}", {{opacity: 1, x: 0, duration: 0.3, ease: "power2.out"}}, {st - 0.15:.3f});')
                js.append(f'tl.to("#tag-{spk}", {{opacity: 0, x: -24, duration: 0.25}}, {st + dd + 0.05:.3f});')
            if cfg["captions"] and panel_shot:
                cap_n += 1
                body.append(f'<div class="clip cap" id="cap{cap_n}" data-start="{st - 0.1:.3f}" data-duration="{dd + 0.2:.3f}" data-track-index="6">'
                            f'<p>{html.escape(spoken_to_text(text))}</p></div>')

    body.append(f'<audio id="mix" src="audio/mix.m4a" data-start="0" data-duration="{total:.3f}" data-track-index="7" data-volume="1"></audio>')
    tpl = open(os.path.join(HERE, "template_v2.html")).read()
    orient = "portrait" if H > W else "landscape"
    page = (tpl.replace("{{W}}", str(W)).replace("{{H}}", str(H)).replace("{{ORIENT}}", orient)
               .replace("{{TOTAL}}", f"{total:.3f}").replace("{{BODY}}", "\n".join(body))
               .replace("{{JS}}", "\n      ".join(js)))
    open(os.path.join(out, "index.html"), "w").write(page)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "training")
