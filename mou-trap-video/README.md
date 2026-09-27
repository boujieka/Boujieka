# The MoU Trap — video

HyperFrames (HTML → MP4) composition built from the 9-panel storyboard in
`assets/storyboard.png`. Panel art is cropped into `assets/panels/`; all text is
re-set from the storyboard wording.

- Output: `renders/the-mou-trap.mp4` — 157 s, 1920×1080, 30 fps, with voiceover
  (`renders/the-mou-trap-preview.mp4` is a smaller copy)
- Voiceover: script in `narration/`, one line per scene; audio in `assets/audio/`,
  generated with `hyperframes tts` (local Kokoro-82M, voice `bm_george`). Scene
  lengths are set to fit each clip. To regenerate a line:
  `npx hyperframes tts narration/s03.txt -v bm_george -o assets/audio/s03.wav`
  (needs `pip install kokoro-onnx soundfile`)
- Structure: title card → scenes 1–9 (one per storyboard panel) → closing card
- GSAP and fonts (Archivo Black, Inter) are vendored under `assets/` so renders
  need no network access

```bash
npm run check    # lint + runtime checks
npm run render   # re-render (requires FFmpeg)
npm run dev      # live preview studio
```
