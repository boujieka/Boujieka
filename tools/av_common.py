"""Shared audio and video helpers for the Book 2 video course: narration synthesis, pronunciation lexicon, loudness,
subtitles and metadata. Narration uses the Kokoro neural voice model (Apache 2.0), run locally.
"""
import re
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf

TTS_DIR = Path("/tmp/claude-0/-home-user-Boujieka/5b078838-abd3-5f75-bf1a-e73c18413f2f/scratchpad/tts")
VOICE, SPEED, LANG, SR = "bm_george", 0.95, "en-gb", 24000
AUTHOR = "Emmanuel Boujieka Kamga"

# Pronunciation lexicon: applied to the text sent to the voice, never to the published scripts.
LEXICON = [
    (r"\bPAYGo\b", "pay go"), (r"\bPAR30\b", "PAR thirty"), (r"\bPAR90\b", "PAR ninety"),
    (r"\b30\+ DPD\b", "thirty plus D P D"), (r"\b90\+ DPD\b", "ninety plus D P D"), (r"\b180\+ DPD\b", "one eighty plus D P D"),
    (r"\bDPD\b", "D P D"), (r"\bECL\b", "E C L"), (r"\bESMAP\b", "E S M A P"), (r"\bSICR\b", "S I C R"),
    (r"\bSHS\b", "S H S"), (r"\bCGAP\b", "C GAP"), (r"\bGOGLA\b", "go gla"), (r"\bMTF\b", "M T F"),
    (r"\bKivara\b", "Kivahra"), (r"\bSolaraPay\b", "Solara Pay"), (r"\bLCY\b", "local currency"),
    (r"\bkWp\b", "kilowatt peak"), (r"\bWp\b", "watt peak"), (r"\bkWh\b", "kilowatt hours"), (r"\bWh\b", "watt hours"),
    (r"(\d)x\b", r"\1 times"), (r"\bIFRS\b", "I F R S"), (r"\bSPV\b", "S P V"), (r"\bDSCR\b", "D S C R"),
    (r"\bCAC\b", "C A C"), (r"\bLTV\b", "L T V"), (r"\bRBF\b", "R B F"), (r"\bAPR\b", "A P R"), (r"\bIRR\b", "I R R"),
    (r"\bFX\b", "F X"), (r"\bEBITDA\b", "ebit da"), (r"\bDCF\b", "D C F"), (r"\bKPIs?\b", "K P I"),
    (r"\bT0(\d)\b", r"T \1"), (r"\bD(\d)\b", r"D \1"), (r"\bM(\d{1,2})\b", r"month \1"), (r"\bY(\d)\b", r"year \1"),
    (r"\bMODEL 2\b", "Model two"), (r"\bPERFORM_2026\b", "PERFORM twenty twenty six"),
    (r"\bCONDITIONAL GO\b", "conditional go"), (r"\bSTOP\b", "stop"), (r"\bGO\b", "go"),
    (r"\b20([1-3]\d)\b(?![,.]\d)", r"twenty \1"),  # years in the British reading: twenty twenty four
    (r"%", " per cent"), (r"\s+", " "),
]


def speakable(text):
    t = text
    for pat, rep in LEXICON:
        t = re.sub(pat, rep, t)
    return t.strip()


_K = None


def tts(text, out_wav, lead=0.35, tail=0.55):
    """Synthesise one passage; returns duration in seconds (including lead and tail silence)."""
    global _K
    if _K is None:
        from kokoro_onnx import Kokoro
        _K = Kokoro(str(TTS_DIR / "kokoro-v1.0.onnx"), str(TTS_DIR / "voices-v1.0.bin"))
    chunks, buf = [], []
    for sent in re.split(r"(?<=[.!?])\s+", speakable(text)):
        if not sent:
            continue
        s, sr = _K.create(sent, voice=VOICE, speed=SPEED, lang=LANG)
        buf.append(s)
        buf.append(np.zeros(int(0.18 * sr), dtype=np.float32))
    audio = np.concatenate([np.zeros(int(lead * SR), np.float32)] + buf + [np.zeros(int(tail * SR), np.float32)])
    sf.write(out_wav, audio, SR)
    return len(audio) / SR


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s]


def srt_time(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"


def srt_blocks(text, start, dur, lead=0.35, tail=0.55):
    """Split narration into subtitle lines timed in proportion to their length."""
    sents = sentences(text)
    span = max(0.1, dur - lead - tail)
    total = sum(len(s) for s in sents) or 1
    t = start + lead
    out = []
    for s in sents:
        d = span * len(s) / total
        out.append((t, t + d, s))
        t += d
    return out


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"command failed: {' '.join(cmd[:6])}...\n{r.stderr[-2000:]}")
    return r


def duration(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)])
    return float(r.stdout.strip())
