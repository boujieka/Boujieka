# Bankable Is Not Enough — Episode 1: The Signing (motion comic)

A voiced motion-comic video of the story pages (book pages 4–24) of
*Bankable Is Not Enough, Episode 1: The Signing* by Emmanuel Boujieka Kamga,
built with [HyperFrames](https://github.com/heygen-com/hyperframes).

- Output: `renders/bankable-ep1-1080p.mp4` (1920×1080, 82 MB) and
  `renders/bankable-ep1-720p.mp4` (1280×720, 27 MB, for messaging) — 30 fps, 13 min 40 s.
  The full-quality master (~512 MB) is not committed; re-render it with the command below.
- Captions: `captions.srt` (upload alongside the video on YouTube, LinkedIn, etc.)

## What's in it

Title card → Meet the cast → chapters 1–7 (every panel, in reading order) →
the ten questions → closing line → credits and disclaimer.

The camera moves from panel to panel on the original page art (extracted at
300 dpi from the book PDF, never redrawn) and dims the rest of the page. Every
speech bubble, caption, Decision Note and Red Team question is voiced; a name
tag shows who is speaking.

| Role | Voice (Kokoro-82M) |
|---|---|
| Narrator, Decision Notes, Red Team | `bm_george` |
| Belpau | `af_heart` |
| Enilec Mok | `bf_emma` |
| Tidianie Eugom | `af_bella` |
| Minister Kerbu | `am_fenrir` |
| Emson Anahct | `am_michael` |
| Paul Ahmak | `bm_lewis` |
| Resident (page 6) | `am_puck` |

## Files

- `scripts/storyboard.py` — the shot list: which panel, who speaks, what they say. **Edit this.**
- `scripts/template.html` — styling, cards, speaker tags.
- `scripts/build.py` — synthesizes the lines, times every shot to its audio,
  mixes `assets/audio/narration.m4a`, writes `captions.srt` and generates `index.html`.
- `scripts/detect_panels.py` → `scripts/panels.json` — panel boxes on each page.
- `assets/pages/` — book pages used by the video (`pg-NNN.jpg` = book page NNN+1).

## Rebuild

```bash
pip install kokoro-onnx soundfile numpy        # plus ffmpeg on PATH
npx hyperframes tts "warm up" -o /tmp/x.wav    # downloads the Kokoro model once
python scripts/build.py                        # regenerates index.html, audio, captions
npm run check && npm run render -- -o renders/bankable-is-not-enough-ep1.mp4
```
