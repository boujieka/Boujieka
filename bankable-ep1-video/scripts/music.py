"""Procedural score for the v2 videos (no external music available offline).

Layers are rendered over the whole timeline on one chord grid, then mixed by
mood with crossfades and ducked under the voice:
  theme    pad + bass + kalimba melody + shaker (title, lesson)
  bed      pad + bass + sparse kalimba (story scenes)
  tension  low drone + pulse (risks, stress test)
  drone    very low drone only (red team)
  silence  nothing (questions to the viewer)
Stingers mark act titles and risk reveals.
"""
import numpy as np
from scipy.signal import lfilter

SR = 24000
BPM = 84
BEAT = 60 / BPM
# i - VI - III - VII in D minor, two bars each
CHORDS = [[50, 53, 57], [46, 50, 53], [53, 57, 60], [48, 52, 55]]
BAR = 4 * BEAT
CHORD_LEN = 2 * BAR
PENTA = [62, 65, 67, 69, 72, 74, 77]  # D minor pentatonic, upper octave


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    return lfilter([1 - a], [1, -a], x)


def chord_at(t):
    return CHORDS[int(t // CHORD_LEN) % len(CHORDS)]


def layer_pad(n):
    t = np.arange(n) / SR
    out = np.zeros(n, np.float32)
    seg = int(CHORD_LEN * SR)
    for s in range(0, n, seg):
        e = min(n, s + seg + int(0.8 * SR))
        tt = t[s:e]
        ch = chord_at(s / SR)
        v = np.zeros(e - s)
        for m in ch + [ch[0] + 12]:
            for det in (-0.08, 0.08):
                f = hz(m) * (1 + det / 100)
                ph = (f * tt) % 1.0
                v += (2 * ph - 1) * 0.12            # detuned saws
        env = np.minimum(1, (tt - tt[0]) / 1.2) * np.minimum(1, (tt[-1] - tt) / 0.8 + 0.001)
        out[s:e] += (v * env).astype(np.float32)
    return lowpass(lowpass(out, 900), 1400).astype(np.float32) * 0.5


def layer_bass(n):
    t = np.arange(n) / SR
    out = np.zeros(n, np.float32)
    step = int(BAR * SR)
    for s in range(0, n, step):
        e = min(n, s + step)
        tt = t[s:e] - s / SR
        f = hz(chord_at(s / SR)[0] - 12)
        out[s:e] = (np.sin(2 * np.pi * f * tt) * np.exp(-tt * 0.9) * 0.35).astype(np.float32)
    return out


def kalimba_note(f, dur=1.6):
    tt = np.arange(int(dur * SR)) / SR
    v = (np.sin(2 * np.pi * f * tt) * np.exp(-tt * 3.2)
         + 0.35 * np.sin(2 * np.pi * f * 5.4 * tt) * np.exp(-tt * 14)
         + 0.12 * np.sin(2 * np.pi * f * 11.2 * tt) * np.exp(-tt * 30))
    v[:int(0.003 * SR)] *= np.linspace(0, 1, int(0.003 * SR))
    return v.astype(np.float32)


def layer_kalimba(n, density):
    """density 1 = melody every eighth note, 0.25 = sparse."""
    out = np.zeros(n, np.float32)
    step = BEAT / 2
    i = 0
    while i * step * SR < n:
        t0 = i * step
        pattern = (i * 5 + (i // 8) * 3) % 7
        if (i % int(round(1 / density))) == 0:
            ch = chord_at(t0)
            # prefer chord tones on strong beats, pentatonic passing notes elsewhere
            m = (ch[(i // 2) % 3] + 12) if i % 4 == 0 else PENTA[pattern]
            note = kalimba_note(hz(m)) * (0.55 if i % 4 == 0 else 0.4)
            s = int(t0 * SR); e = min(n, s + len(note))
            out[s:e] += note[:e - s]
        i += 1
    return out


def layer_shaker(n):
    rng = np.random.default_rng(7)
    out = np.zeros(n, np.float32)
    step = BEAT / 2
    burst = int(0.06 * SR)
    env = np.exp(-np.arange(burst) / (0.012 * SR)).astype(np.float32)
    i = 0
    while i * step * SR < n:
        s = int(i * step * SR); e = min(n, s + burst)
        noise = rng.standard_normal(burst).astype(np.float32)
        noise = noise - lowpass(noise, 4000).astype(np.float32)
        out[s:e] += (noise * env * (0.10 if i % 2 else 0.06))[:e - s]
        i += 1
    return out


def layer_drone(n):
    t = np.arange(n) / SR
    v = (np.sin(2 * np.pi * hz(38) * t) * 0.5 + np.sin(2 * np.pi * hz(45) * t) * 0.25
         + np.sin(2 * np.pi * hz(39) * t) * 0.12)          # b2 rub for unease
    wob = 0.75 + 0.25 * np.sin(2 * np.pi * 0.07 * t)
    return (lowpass(v * wob, 500) * 0.5).astype(np.float32)


def layer_pulse(n):
    t = np.arange(n) / SR
    out = np.zeros(n, np.float32)
    step = int(BEAT * SR)
    hit = np.sin(2 * np.pi * 55 * np.arange(int(0.35 * SR)) / SR) * np.exp(-np.arange(int(0.35 * SR)) / (0.08 * SR))
    for s in range(0, n, step):
        e = min(n, s + len(hit)); out[s:e] += (hit[:e - s] * 0.45).astype(np.float32)
    return out


def stinger(kind):
    tt = np.arange(int(2.2 * SR)) / SR
    if kind == "act":
        sweep = np.sin(2 * np.pi * (70 * tt - 12 * tt ** 2)) * np.exp(-tt * 1.6)
        rng = np.random.default_rng(3)
        air = lowpass(rng.standard_normal(len(tt)), 1800) * np.exp(-tt * 2.5) * 0.3
        return ((sweep * 0.7 + air) * 0.6).astype(np.float32)
    # "risk": low hit + dissonant bell
    hit = np.sin(2 * np.pi * 48 * tt) * np.exp(-tt * 3.0)
    bell = (np.sin(2 * np.pi * hz(74) * tt) + np.sin(2 * np.pi * hz(75) * tt)) * np.exp(-tt * 2.2) * 0.12
    return ((hit * 0.8 + bell) * 0.6).astype(np.float32)


MIX = {  # layer gains per mood
    "theme":   {"pad": 0.9, "bass": 0.8, "kal": 0.9, "kal_sparse": 0.0, "shaker": 0.6, "drone": 0.0, "pulse": 0.0},
    "bed":     {"pad": 0.7, "bass": 0.5, "kal": 0.0, "kal_sparse": 0.55, "shaker": 0.0, "drone": 0.0, "pulse": 0.0},
    "tension": {"pad": 0.2, "bass": 0.0, "kal": 0.0, "kal_sparse": 0.0, "shaker": 0.0, "drone": 0.8, "pulse": 0.55},
    "drone":   {"pad": 0.0, "bass": 0.0, "kal": 0.0, "kal_sparse": 0.0, "shaker": 0.0, "drone": 0.7, "pulse": 0.0},
    "silence": {"pad": 0.0, "bass": 0.0, "kal": 0.0, "kal_sparse": 0.0, "shaker": 0.0, "drone": 0.0, "pulse": 0.0},
}


def render_score(total, cues, stings, voice, level=0.16, duck_db=-11):
    """cues: [(start, end, mood)], stings: [(t, kind)], voice: mono voice track (SR).
    Returns the music track (mono, SR), ducked under the voice."""
    n = int(total * SR)
    layers = {"pad": layer_pad(n), "bass": layer_bass(n), "kal": layer_kalimba(n, 1.0),
              "kal_sparse": layer_kalimba(n, 0.25), "shaker": layer_shaker(n),
              "drone": layer_drone(n), "pulse": layer_pulse(n)}
    for k in layers:  # normalise each layer so MIX gains are comparable
        pk = float(np.max(np.abs(layers[k]))) or 1.0
        layers[k] /= pk
    out = np.zeros(n, np.float32)
    xf = int(0.9 * SR)
    for name, sig in layers.items():
        g = np.zeros(n, np.float32)
        for s, e, mood in cues:
            a, b = int(s * SR), min(n, int(e * SR))
            g[a:b] = MIX[mood][name]
        # smooth steps into crossfades
        ker = np.ones(xf, np.float32) / xf
        g = np.convolve(g, ker, mode="same").astype(np.float32)
        out += sig[:n] * g
    for t, kind in stings:
        st = stinger(kind); s = int(t * SR); e = min(n, s + len(st))
        out[s:e] += st[:e - s] * 1.4
    out *= level / (float(np.percentile(np.abs(out), 99.5)) or 1.0)
    # duck under speech
    v = np.abs(voice[:n]) if len(voice) >= n else np.pad(np.abs(voice), (0, n - len(voice)))
    env = lowpass(lowpass(v, 3), 3)
    env = env / (np.percentile(env[env > 0], 95) if np.any(env > 0) else 1)
    duck = 1 - (1 - 10 ** (duck_db / 20)) * np.clip(env * 3, 0, 1)
    return (out * duck).astype(np.float32)
