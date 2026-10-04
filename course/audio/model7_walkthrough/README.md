# MODEL 7 audio guide: "How to use MODEL 7, step by step"

- `MODEL7_Audio_Guide.mp3` (192 kbps, 44.1 kHz, mono) and `MODEL7_Audio_Guide.m4a` (AAC 160 kbps): 12 min 35 s, 13 chapters with chapter markers, loudness normalised to about -16 LUFS, peaks at -1.7 dBFS.
- `script.md`: the narration, chapter by chapter; figures are those of the default Kasiri case in MODEL 7 v1.0 release candidate 1.
- Voice: synthetic British English neural voice (Piper text to speech, voice "en_GB-cori-high"). Replace with a recorded narrator for the commercial edition if preferred; the script is ready to read.
- Rebuild: render each chapter with Piper (`--length-scale 1.06 --sentence-silence 0.45`), join with 1.6 s gaps, then `highpass=f=60,loudnorm=I=-16:TP=-1.5:LRA=11` in ffmpeg. Intermediate WAV files are not kept in the repository.

Chapters: 1 Introduction; 2 The cover sheet; 3 Read me and the colour code; 4 The control panel; 5 Check before you read; 6 Read the dashboard; 7 Why the decision is STOP; 8 The developer's view; 9 Stress the river; 10 Stress the buyer; 11 Compare structures and contracts; 12 Use it on your own project; 13 Closing.
