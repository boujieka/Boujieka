# Demo video (OpenMontage)

A vertical 9:16 demo of the simulation build (France → Cameroon, 1 000 €), about 54 s, with a French voice-over.
The video shows the app exactly as it is: fictional profiles, a fictional counterparty, simulated payouts and the
"Mode simulation — aucun argent réel" banner on every screen. The end card repeats that no real money moves.

The video is produced with [OpenMontage](https://github.com/calesthio/OpenMontage) (GNU AGPL-3.0), an agent-driven
video production toolkit. OpenMontage is **not** vendored here: it is cloned next to this repository and run from
there. Only our own inputs live in this folder. Remotion (used for the composition) has its own licence: check it
before commercial use (companies above a size threshold need a company licence).

## Files

| File | Role |
|---|---|
| `record-demo.cjs` | Playwright: drives the exported web build through the flow and records `capture.webm` + step `marks.json` |
| `retime.py` | ffmpeg: cuts the capture into the narration windows of `retime_segments.json` → `screen.mp4` |
| `narration_fr.txt` | Voice-over text (numbers written out for text-to-speech) |
| `props.json` | Caption timings (from the voice-over's word timestamps, ×1/1.1), chapter chips, highlight boxes |
| `DiaspoSwapDemo.tsx` | Remotion composition (1080×1920, 30 fps), DiaspoSwap colours from `docs/DESIGN_SYSTEM.md` |

## Reproduce

```bash
# 1. OpenMontage, next to this repo (Python 3.10+, Node 22+, FFmpeg)
git clone https://github.com/calesthio/OpenMontage.git ../../OpenMontage && (cd ../../OpenMontage && make setup)

# 2. Capture (from diasposwap/)
npm run mobile:web:export
node video/record-demo.cjs apps/mobile/dist /tmp/dsw   # needs Playwright + Chromium
python3 video/retime.py /tmp/dsw/capture.webm /tmp/dsw/screen.mp4
```

3. Voice-over: `narration_fr.txt` read with the ElevenLabs voice "Aquilas" (`eleven_multilingual_v2`), then
   `ffmpeg -i take.mp3 -af "atempo=1.1,loudnorm=I=-16:TP=-1.5:LRA=11" -ar 48000 narration.wav`.
   This is a **paid** service (it used 752 credits per take); ask before generating. A new take has different
   timings: re-transcribe it and rebuild the captions and `retime_segments.json`.
4. Copy `screen.mp4`, `narration.wav`, `props.json` and `docs/brand/mark-light.svg` into
   `OpenMontage/remotion-composer/public/diasposwap/`, copy `DiaspoSwapDemo.tsx` into `remotion-composer/src/`,
   register it in `src/Root.tsx` (id `DiaspoSwapDemo`, 1080×1920, 30 fps, `durationInFrames = ceil(duration × 30)`),
   then:

```bash
npx remotion render src/index.tsx DiaspoSwapDemo out/diasposwap-demo.mp4 --props=public/diasposwap/props.json --codec=h264 --crf=18
```

The rendered MP4 is not committed. Do not publish it without the owner's approval (see `CLAUDE.md`).
