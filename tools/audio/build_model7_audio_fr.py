"""French audio guide to MODEL 7 (« Utiliser MODEL 7, pas à pas »), from the French narration of the video guide.

python3 tools/audio/build_model7_audio_fr.py
Needs Kokoro-82M (pip install kokoro) with the ff_siwis voice, and ffmpeg.
Output: course/audio/model7_walkthrough_fr/MODEL7_Guide_audio_FR.mp3 (chapters in the ID3 tags) and script_audio_fr.md.
"""
import os
import re
import subprocess

import numpy as np
import soundfile as sf
from kokoro import KPipeline

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)
OUT = "course/audio/model7_walkthrough_fr"
WORK = os.environ.get("AUDIO_WORK", "/tmp/model7_audio_fr")
os.makedirs(OUT, exist_ok=True)
os.makedirs(WORK, exist_ok=True)
SR, SPEED = 24000, 0.94
AUDIO_EDITS = [("Bienvenue dans le guide vidéo de MODEL 7", "Bienvenue dans le guide audio de MODEL 7"),
               ("Pendant les seize prochaines minutes, nous allons", "Dans ce guide, nous allons"),
               ("et gardez-le à côté de la vidéo", "et gardez-le à côté de vous pendant l'écoute"),
               ("Mettez la vidéo en pause", "Mettez l'enregistrement en pause")]
SAY = [("Hydropower Development and Finance, From River to Financial Close",
        "Haïdropaweur Dévelopmeunt ènde Faïnance, Frome Riveur tou Faïnancheul Clôze"),
       ("Hydro Readiness Framework", "Haïdro Rédinesse Framework"), ("Kasiri River Hydro", "Kasiri Riveur Haïdro"),
       ("Read me", "Rîd mî"), ("Start here", "Start hir"), ("Close readiness", "Clôze rédinesse"),
       ("Development", "Dévelopmeunt"), ("Contracting", "Contractinng"), ("Book check", "Bouk tchèk"),
       ("lignes check", "lignes tchèk"), ("MODEL 7", "Modèle 7"), ("MANUAL 7", "Manuel 7")]

src = open("course/video/script_fr.md", encoding="utf8").read()
chapters = []
for num, title, body in re.findall(r"^## (\d+)\. (.+?)\n(.*?)(?=^## |\Z)", src, re.S | re.M):
    paras = [p.strip() for p in body.strip().split("\n\n") if p.strip()]
    for a, b in AUDIO_EDITS:
        paras = [p.replace(a, b) for p in paras]
    chapters.append((int(num), title, paras))
open(f"{OUT}/script_audio_fr.md", "w", encoding="utf8").write(
    "# MODEL 7, guide audio : script de la narration en français\n\nNarration du guide audio « Utiliser MODEL 7, pas à pas », "
    "adaptée du script du guide vidéo (course/video/script_fr.md). Chiffres du cas Kasiri par défaut de MODEL 7 v1.0 RC1.\n\n"
    + "\n\n".join(f"## {n:02d}. {t}\n\n" + "\n\n".join(ps) for n, t, ps in chapters) + "\n")

kp = KPipeline(lang_code="f", repo_id="hexgrad/Kokoro-82M")


def say(text):
    for a, b in SAY:
        text = text.replace(a, b)
    parts = []
    for sent in re.split(r"(?<=[.!?;:])\s+", text.strip()):
        audio = [x.numpy() if hasattr(x, "numpy") else x for _, _, x in kp(sent, voice="ff_siwis", speed=SPEED)]
        if audio:
            parts += [np.concatenate(audio), np.zeros(int(SR * (0.32 if sent[-1] in ".!?" else 0.18)))]
    return np.concatenate(parts)


track, marks, t = [], [], 0.0
for n, title, paras in chapters:
    marks.append((t, f"{n}. {title}"))
    seg = [np.zeros(int(SR * 0.6))]
    if n > 1:
        seg += [say(f"Partie {n}. {title}."), np.zeros(int(SR * 0.45))]
    for p in paras:
        seg += [say(p), np.zeros(int(SR * 0.55))]
    seg.append(np.zeros(int(SR * 0.9)))
    a = np.concatenate(seg)
    track.append(a)
    t += len(a) / SR
wav = f"{WORK}/guide_fr.wav"
sf.write(wav, np.concatenate(track), SR)
meta = [";FFMETADATA1", "title=Utiliser MODEL 7, pas à pas (guide audio)", "artist=Emmanuel Boujieka Kamga",
        "album=Africa Energy Finance : ressources du Livre 7", "comment=Guide audio de MODEL 7 v1.0 RC1. Narration : voix de synthèse."]
for i, (st, name) in enumerate(marks):
    end = marks[i + 1][0] if i + 1 < len(marks) else t
    meta += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={int(st * 1000)}", f"END={int(end * 1000)}", f"title={name}"]
open(f"{WORK}/chapters.txt", "w", encoding="utf8").write("\n".join(meta) + "\n")
mp3 = f"{OUT}/MODEL7_Guide_audio_FR.mp3"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", wav, "-i", f"{WORK}/chapters.txt", "-map", "0:a", "-map_metadata", "1",
                "-map_chapters", "1", "-af", "highpass=f=60,loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-c:a", "libmp3lame",
                "-b:a", "160k", "-id3v2_version", "3", mp3], check=True)
print(mp3, f"{t / 60:.1f} min, {len(marks)} chapters")
