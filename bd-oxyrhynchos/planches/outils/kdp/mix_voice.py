"""Découpe la voix off en 6 phrases (détection des silences), les cale sur les scènes,
baisse la musique sous la voix et produit la vidéo finale.
usage: python3 mix_voice.py voix.mp3 musique.wav video_sans_son.mp4 sortie.mp4"""
import sys, subprocess, re

voice, music, video, out = sys.argv[1:5]
DUR = 43.6
# début souhaité de chaque phrase (s) ; la dernière est calée pour finir à 43,1 s
STARTS = [3.0, 7.1, 11.1, 27.2, 31.4, None]

txt = subprocess.run(['ffmpeg', '-hide_banner', '-i', voice, '-af', 'silencedetect=noise=-38dB:d=0.35', '-f', 'null', '-'],
                     capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', txt)]
ends = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', txt)]
total = float(re.search(r'Duration: (\d+):(\d+):([\d.]+)', txt).group(3)) + 60 * int(re.search(r'Duration: (\d+):(\d+)', txt).group(2))
gaps = sorted([(e - s, s, e) for s, e in zip(starts, ends) if 0.05 < s and e < total - 0.05], reverse=True)[:5]
cuts = sorted((s + e) / 2 for _, s, e in gaps)
if len(cuts) != 5:
    sys.exit(f'découpage impossible : {len(cuts) + 1} phrases trouvées au lieu de 6')
bounds = [0.0] + cuts + [total]
segs = list(zip(bounds[:-1], bounds[1:]))
dl = []
for i, (a, b) in enumerate(segs):
    st = STARTS[i] if STARTS[i] is not None else 43.1 - (b - a)
    dl.append(st)
    print(f'phrase {i + 1} : {a:.2f}–{b:.2f} s  →  {st:.2f} s')
filt = []
for i, ((a, b), st) in enumerate(zip(segs, dl)):
    filt.append(f'[1:a]atrim={a}:{b},asetpts=PTS-STARTPTS,adelay={int(st * 1000)}|{int(st * 1000)}[v{i}]')
filt.append(''.join(f'[v{i}]' for i in range(6)) + f'amix=inputs=6:normalize=0,apad=whole_dur={DUR},volume=1.6[vox]')
filt.append('[vox]asplit=2[vox1][vox2]')
filt.append('[2:a]volume=0.9[mus]')
filt.append('[mus][vox1]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[duck]')
filt.append(f'[duck][vox2]amix=inputs=2:normalize=0,alimiter=limit=0.95,atrim=0:{DUR}[a]')
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', video, '-i', voice, '-i', music, '-filter_complex', ';'.join(filt),
                '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', out], check=True)
print('ok', out)
