"""Cut the Playwright capture into the narration windows of retime_segments.json.

Usage: python3 retime.py capture.webm screen.mp4
Playwright records CSS pixels (390x844) in the top-left of the 780x1688 frame, so the
result is cropped to that area and upscaled 2x (lanczos).
"""
import json
import subprocess
import sys
from pathlib import Path

src, dst = sys.argv[1], sys.argv[2]
segs = json.loads((Path(__file__).parent / "retime_segments.json").read_text())
parts = [
    f"[0:v]trim={s['capture_in']}:{s['capture_out']},"
    f"setpts=(PTS-STARTPTS)*{(s['out_end'] - s['out_start']) / (s['capture_out'] - s['capture_in']):.5f},fps=30[v{i}]"
    for i, s in enumerate(segs)
]
graph = ";".join(parts) + ";" + "".join(f"[v{i}]" for i in range(len(segs)))
graph += f"concat=n={len(segs)}:v=1:a=0,crop=390:844:0:0,scale=780:1688:flags=lanczos[out]"
subprocess.run(
    ["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", graph, "-map", "[out]",
     "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", dst],
    check=True,
)
