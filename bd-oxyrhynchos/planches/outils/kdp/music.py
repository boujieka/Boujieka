"""Musique originale de bande-annonce (43,6 s), synthétisée : nappe grave, percussions,
mélodie en mode hijaz (couleur « égyptienne »), souffles de transition, impact final.
usage: python3 music.py out.wav"""
import sys, wave
import numpy as np

SR = 44100
DUR = 43.6
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(7)
mix = np.zeros((N, 2))

# découpage de la vidéo (s)
CUTS = [2.6, 6.8, 10.8, 13.1, 15.4, 17.7, 20.0, 22.3, 24.6, 26.9, 31.1, 35.1, 38.1]
FINAL = 38.1


def env(x0, x1, a=0.02, r=0.3):
    e = np.zeros(N)
    i0, i1 = int(x0 * SR), min(N, int(x1 * SR))
    n = i1 - i0
    if n <= 0:
        return e
    k = np.ones(n)
    na, nr = max(1, int(a * SR)), max(1, int(r * SR))
    k[:na] = np.linspace(0, 1, na)[:n]
    k[-nr:] *= np.linspace(1, 0, nr)[-n:] if nr <= n else 1
    e[i0:i1] = k
    return e


def add(sig, gain=1.0, pan=0.0):
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    mix[:, 0] += sig * gain * l * 1.41
    mix[:, 1] += sig * gain * r * 1.41


def lowpass(x, cut):
    a = np.exp(-2 * np.pi * cut / SR)
    y = np.zeros_like(x); s = 0.0
    for i in range(len(x)):
        s = (1 - a) * x[i] + a * s; y[i] = s
    return y


def f(midi):
    return 440 * 2 ** ((midi - 69) / 12)


# 1. Nappe grave (ré) qui s'élargit
D2, A2, D3 = f(38), f(45), f(50)
pad = sum(np.sin(2 * np.pi * fr * t + 0.3 * np.sin(2 * np.pi * 0.11 * t)) * g for fr, g in [(D2, 0.55), (A2, 0.35), (D3, 0.28), (f(53), 0.12)])
pad *= np.clip(t / 4, 0, 1) * (0.55 + 0.45 * np.clip((t - 10) / 20, 0, 1))
pad *= np.where(t > FINAL - 0.6, np.clip((DUR - t) / 2.5, 0, 1) * 1.15 + 0.0, 1)
add(pad, 0.24)
# drone de quinte aigu, léger chorus stéréo
add(np.sin(2 * np.pi * f(62) * 1.003 * t) * 0.05 * np.clip((t - 6) / 6, 0, 1), 1, -0.6)
add(np.sin(2 * np.pi * f(62) * 0.997 * t) * 0.05 * np.clip((t - 6) / 6, 0, 1), 1, 0.6)

# 2. Percussions (tambour grave à hauteur descendante + claquement)
def drum(at, gain=1.0, low=True):
    n = int(0.6 * SR); i0 = int(at * SR)
    if i0 >= N:
        return
    tt = np.arange(min(n, N - i0)) / SR
    if low:
        fr = 55 + 90 * np.exp(-tt * 28)
        s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt * 7)
    else:
        s = rng.standard_normal(len(tt)) * np.exp(-tt * 38) * 0.6
    sig = np.zeros(N); sig[i0:i0 + len(tt)] = s
    add(sig, gain * (0.55 if low else 0.10), 0 if low else 0.25)


BPM = 96; beat = 60 / BPM
start = 6.8
x = start
k = 0
while x < FINAL - 0.2:
    intensity = 0.6 + 0.4 * min(1, (x - start) / 20)
    pat = k % 8
    if pat in (0, 3, 6):
        drum(x, intensity)
    if pat in (2, 6) and x > 10.8:
        drum(x, intensity, low=False)
    if x > 26.9 and pat in (5, 7):
        drum(x, intensity * 0.7)
    x += beat / 2; k += 1

# 3. Mélodie « pincée » (Karplus-Strong) en mode hijaz sur ré : ré mi♭ fa♯ sol la si♭ do
SCALE = [62, 63, 66, 67, 69, 70, 72, 74]


def pluck(at, midi, dur=0.9, gain=0.18, pan=0.2):
    fr = f(midi); per = int(SR / fr)
    n = int(dur * SR); i0 = int(at * SR)
    if i0 >= N:
        return
    buf = rng.uniform(-1, 1, per)
    out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % per]
        buf[i % per] = 0.5 * (buf[i % per] + buf[(i + 1) % per]) * 0.996
    out *= np.exp(-np.arange(n) / SR * 2.5)
    sig = np.zeros(N); m = min(n, N - i0); sig[i0:i0 + m] = out[:m]
    add(sig, gain, pan)


phrase = [0, 1, 2, 1, 0, 2, 3, 4, 3, 2, 1, 0]
x = 10.8; i = 0
while x < 26.9:
    deg = phrase[i % len(phrase)]
    pluck(x, SCALE[deg] + (12 if (i // len(phrase)) % 2 else 0), gain=0.16)
    x += beat * (1 if i % 3 else 0.5); i += 1
for j, deg in enumerate([4, 5, 6, 7, 6, 5, 4]):     # montée « questions »
    pluck(26.9 + j * 0.55, SCALE[deg], gain=0.2, pan=-0.2)
for j, deg in enumerate([7, 5, 4, 2, 1, 0]):        # phrase finale
    pluck(FINAL + 0.3 + j * 0.42, SCALE[deg] + 12 if j < 2 else SCALE[deg], dur=1.6, gain=0.2)

# 4. Souffles de transition aux coupes
noise = rng.standard_normal(N)
sw = np.zeros(N)
for c in CUTS:
    e = env(c - 0.45, c + 0.05, a=0.4, r=0.05)
    sw += noise * e
add(lowpass(lowpass(sw, 1400), 1400) * 0.6, 0.22)

# 5. Montée + impact sur le titre final
rise = noise * env(FINAL - 2.5, FINAL, a=2.4, r=0.05)
add(lowpass(lowpass(rise, 2200), 2200) * 0.8, 0.22)
drum(FINAL, 1.8)
boom = np.zeros(N); i0 = int(FINAL * SR); tt = np.arange(N - i0) / SR
boom[i0:] = np.sin(2 * np.pi * 40 * tt) * np.exp(-tt * 1.4)
add(boom, 0.5)
drum(DUR - 1.2, 1.2)

# normalisation douce
peak = np.abs(mix).max()
mix = np.tanh(mix / peak * 1.4) * 0.85
mix *= np.clip((DUR - t) / 0.4, 0, 1)[:, None]
pcm = (mix * 32767).astype(np.int16)
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok', DUR, 's')
