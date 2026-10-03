"""Build the narrated audio of the Book 2 video course (Modules 0 to 16) from the scripts.

Run: python tools/build_v2_course_audio.py [module numbers...]
For each scripts/module_NN.md: narration = every paragraph under a "## Scene" heading except "On screen:" lines.
Writes video-course/audio/AEF_V2_Module_NN.mp3 (loudness normalised, tagged) and a QA report comparing an automatic
transcription of each file with its script.
"""
import json
import re
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).parent))
import av_common as A  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
VC = ROOT / "volumes/02-solar-home-systems/video-course"
WORK = A.TTS_DIR.parent / "course_audio"


def parse(md):
    title = re.search(r"^# (.+)$", md, re.M).group(1).strip()
    scenes = []
    for block in re.split(r"^## ", md, flags=re.M)[1:]:
        head, _, body = block.partition("\n")
        if not head.lower().startswith("scene"):
            continue
        paras = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip() and not p.strip().startswith("On screen:")]
        scenes.append((head.strip(), [re.sub(r"\s+", " ", p) for p in paras]))
    return title, scenes


ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
US_UK = {"analyzed": "analysed", "behavior": "behaviour", "installment": "instalment", "installments": "instalments",
         "recognizes": "recognises", "recognize": "recognise", "organization": "organisation", "program": "programme",
         "programs": "programmes", "labor": "labour", "favor": "favour", "center": "centre", "percent": "per cent"}


def say(n):
    """British cardinal in words, used to compare a transcript that writes numbers as digits."""
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("" if n % 10 == 0 else " " + ONES[n % 10])
    if n < 1000:
        return ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " and " + say(n % 100))
    for unit, name in ((10 ** 9, "billion"), (10 ** 6, "million"), (1000, "thousand")):
        if n >= unit:
            rest = n % unit
            return say(n // unit) + " " + name + ("" if rest == 0 else (" and " if rest < 100 else " ") + say(rest))


def normalise(t):
    t = A.speakable(t)
    t = re.sub(r"(?<=\d)[ ,](?=\d{3}\b)", "", t)  # 52 560 or 52,560
    t = re.sub(r"\b(20)([1-3]\d)\b", r"twenty \2", t)
    t = re.sub(r"\b2000 and (\d{2})\b", r"twenty \1", t)
    t = re.sub(r"(\d+)\.(\d+)", lambda m: m.group(1) + " point " + " ".join(m.group(2)), t)
    t = re.sub(r"\d+", lambda m: say(int(m.group(0))), t)
    t = re.sub(r"[^a-z ]+", " ", t.lower())
    return " ".join(US_UK.get(w, w) for w in t.split()).split()


def words(t):
    return normalise(t)


def wer(ref, hyp):
    r, h = words(ref), words(hyp)
    d = np.zeros((len(r) + 1, len(h) + 1), dtype=np.int32)
    d[:, 0] = np.arange(len(r) + 1)
    d[0, :] = np.arange(len(h) + 1)
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            d[i, j] = min(d[i - 1, j] + 1, d[i, j - 1] + 1, d[i - 1, j - 1] + (r[i - 1] != h[j - 1]))
    return d[len(r), len(h)] / max(1, len(r))


def build(n):
    src = VC / "scripts" / f"module_{n:02d}.md"
    title, scenes = parse(src.read_text())
    WORK.mkdir(parents=True, exist_ok=True)
    parts, text_all = [], []
    for si, (head, paras) in enumerate(scenes):
        for pi, p in enumerate(paras):
            wav, key = WORK / f"m{n:02d}_{si:02d}_{pi:02d}.wav", WORK / f"m{n:02d}_{si:02d}_{pi:02d}.txt"
            if not (wav.exists() and key.exists() and key.read_text() == A.speakable(p)):
                A.tts(p, wav, lead=0.0, tail=0.0)
                key.write_text(A.speakable(p))
            a, _ = sf.read(wav, dtype="float32")
            parts.append(a)
            parts.append(np.zeros(int(0.55 * A.SR), np.float32))
            text_all.append((p, wav))
        parts.append(np.zeros(int(0.6 * A.SR), np.float32))
    audio = np.concatenate([np.zeros(int(0.5 * A.SR), np.float32)] + parts)
    raw = WORK / f"m{n:02d}.wav"
    sf.write(raw, audio, A.SR)
    out = VC / "audio" / f"AEF_V2_Module_{n:02d}.mp3"
    out.parent.mkdir(parents=True, exist_ok=True)
    A.run(["ffmpeg", "-y", "-i", str(raw), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-ac", "1",
           "-c:a", "libmp3lame", "-b:a", "128k", "-id3v2_version", "3", "-write_xing", "1",
           "-metadata", f"title={title}", "-metadata", f"artist={A.AUTHOR}",
           "-metadata", "album=Africa Energy Finance, Book 2: PAYGo Solar Finance, video course",
           "-metadata", f"track={n + 1}", "-metadata", "genre=Speech", "-fflags", "+bitexact", str(out)])
    return title, A.duration(out), text_all, raw


if __name__ == "__main__":
    mods = [int(x) for x in sys.argv[1:]] or list(range(0, 17))
    rep_path = VC / "audio" / "qa_report.json"
    rep = json.load(open(rep_path)) if rep_path.exists() else {}
    sys.path.insert(0, str(A.TTS_DIR))
    import asr  # noqa: E402  (speech recognition used only for quality control)
    for n in mods:
        title, dur, paras, raw = build(n)
        # each paragraph is transcribed on its own, so no word is lost at a recogniser window boundary
        errs = refs = 0
        worst = (0.0, "")
        for p, wav in paras:
            e = wer(p, asr.transcribe(str(wav)))
            r = len(words(p))
            errs, refs = errs + e * r, refs + r
            worst = max(worst, (e, p[:60]))
        text = " ".join(p for p, _ in paras)
        rep[f"{n:02d}"] = dict(title=title, minutes=round(dur / 60, 2), words=len(text.split()), wer=round(float(errs / refs), 4),
                               worst_paragraph=dict(wer=round(float(worst[0]), 3), starts=worst[1]))
        json.dump(rep, open(rep_path, "w"), indent=1)
        print(n, rep[f"{n:02d}"], flush=True)
