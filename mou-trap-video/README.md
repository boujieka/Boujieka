# The MoU Trap — video

HyperFrames (HTML → MP4) composition built from the 9-panel storyboard in
`assets/storyboard.png`. Panel art is cropped into `assets/panels/`; all text is
re-set from the storyboard wording.

- Output: `renders/the-mou-trap.mp4` — 83 s, 1920×1080, 30 fps, no audio
- Structure: title card → scenes 1–9 (one per storyboard panel) → closing card
- GSAP and fonts (Archivo Black, Inter) are vendored under `assets/` so renders
  need no network access

```bash
npm run check    # lint + runtime checks
npm run render   # re-render (requires FFmpeg)
npm run dev      # live preview studio
```
