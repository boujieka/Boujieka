# Training videos

One video per product and language, built from real renders of the delivered workbooks.

| File | Product | Language |
|---|---|---|
| `p1_en.mp4`, `p1_fr.mp4` | Mini-Grid Financial Feasibility Calculator | EN, FR |
| `p2_en.mp4`, `p2_fr.mp4` | Energy Access Project Financial Model, Developer Edition | EN, FR |
| `p3_en.mp4`, `p3_fr.mp4` | Energy Access Fund Manager Model, RBF & Portfolio Edition | EN, FR |

Each video comes with:

* `{p}_{lang}.srt`: the subtitles, also burned into the image. Upload it as a separate track on platforms that accept SRT.
* `{p}_{lang}_script.md`: the narration script, with the timing of each sentence, for recording a voice-over.

Format: MP4 (H.264), 1920x1080, 25 fps, no soundtrack. To add a voice-over, record it from the script and mix it in any video editor, or with ffmpeg:

```
ffmpeg -i p1_fr.mp4 -i voix_p1_fr.m4a -c:v copy -c:a aac -shortest p1_fr_voix.mp4
```

Rebuild: `python tools/build_training_videos.py [--product p1] [--lang fr]`. Scenes and narration are in `tools/video_storyboards.py`.

Example values shown are illustrative. Platform limits on video length and size (Etsy, Gumroad) are not verified here: check them before upload.
