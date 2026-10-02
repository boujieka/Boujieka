"""Assemble the Volume 2 video course scripts (Modules 0 to 17) into one publication source and PDF.

Run: python tools/build_v2_course_scripts.py
Reads video-course/scripts/module_NN.md and the running times in video-course/audio/qa_report.json and in the
Module 17 video, writes video-course/AEF_V2_Video_Course_Scripts.md and publishes the PDF with publish_docs.py.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import av_common as A  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
VC = ROOT / "volumes/02-solar-home-systems/video-course"
M17 = VC / "AEF_V2_Module17_Model_Walkthrough.mp4"


def mmss(minutes):
    s = int(round(minutes * 60))
    return f"{s // 60}:{s % 60:02d}"


def narration_words(md):
    n = 0
    for block in re.split(r"^## ", md, flags=re.M)[1:]:
        head, _, body = block.partition("\n")
        if head.lower().startswith("scene"):
            for p in re.split(r"\n\s*\n", body):
                if p.strip() and not p.strip().startswith("On screen:"):
                    n += len(p.split())
    return n


def module_body(md, minutes):
    md = md.strip()
    # running time from the finished recording replaces the planning estimate
    md = re.sub(r"^Duration: about \d+ minutes\.", f"Running time: {mmss(minutes)}.", md, count=1, flags=re.M)
    md = re.sub(r"^## ", "### ", md, flags=re.M)
    md = re.sub(r"^On screen: (.+)$", r"> On screen: *\1*", md, flags=re.M)
    return md


def main():
    rep = json.loads((VC / "audio/qa_report.json").read_text())
    rows, bodies, total_min, total_words = [], [], 0.0, 0
    for n in range(18):
        src = VC / "scripts" / f"module_{n:02d}.md"
        md = src.read_text()
        title = re.search(r"^# (.+)$", md, re.M).group(1).split(". ", 1)[1]
        if n == 17:
            minutes, media = A.duration(M17) / 60, "Video, MP4, 1920 by 1080, subtitles and chapters"
        else:
            minutes, media = rep[f"{n:02d}"]["minutes"], f"Narration, AEF_V2_Module_{n:02d}.mp3"
        words = narration_words(md)
        total_min += minutes
        total_words += words
        rows.append(f"| {n} | {title} | {mmss(minutes)} | {words:,} | {media} |")
        bodies.append(module_body(md, minutes))

    front = f"""# About the course

The video course follows the book chapter by chapter. Module 0 explains how the course, the book, the model, the case study, the templates and the decision tools fit together. Modules 1 to 16 follow Chapters 1 to 16, each built around the decision its chapter supports. Module 17 is a screen walk through of the AEF SHS PAYGo model, step by step, in the order of the user manual.

This document holds the full narration of every module, with the screen direction for each scene set apart in italics. The scripts are the reference text for the recordings and for subtitles, and they can be read on their own as a spoken summary of the book.

## Running order

| Module | Title | Running time | Words narrated | Media |
|---|---|---|---|---|
{chr(10).join(rows)}
| | Total | {int(total_min // 60)} h {int(round(total_min % 60))} min | {total_words:,} | |

## Conventions

Every figure in the narration comes from the book, the model or the SolaraPay case, and the external figures keep the caveats the book attaches to them. SolaraPay Ltd and the Republic of Kivara are fictional, and their history is synthetic. The default model inputs describe a fictional market. Money is spoken in words with its currency, negative figures are spoken as a loss or as minus, and acronyms are said in full the first time they appear in a module.

Learning objectives are listed for the viewer and the instructor; they are not narrated. Each module closes with a recap and one practical exercise in the model, a template (T01 to T08) or a decision tool (D1 to D6).

## Recordings

The recordings of this edition use a British English narrator voice at a measured pace of about 130 words a minute, normalised to minus 16 LUFS for consistent loudness across modules. Each narration file carries its module title, author and track number. The Module 17 video is recorded from the model itself at 1920 by 1080 pixels, with chapter markers for each of the twelve steps and an English subtitle track, also supplied as a separate subtitle file.
"""
    out_md = VC / "AEF_V2_Video_Course_Scripts.md"
    out_md.write_text(front + "\n" + "\n\n".join(bodies) + "\n")
    subprocess.run([sys.executable, str(ROOT / "tools/publish_docs.py"), str(out_md), str(VC / "AEF_V2_Video_Course_Scripts.pdf"),
                    "--title", "Video Course Scripts", "--subtitle", "Solar Home Systems: PAYGo Business and Financial Models",
                    "--short", "Video Course Scripts"], check=True)
    print(f"{total_min:.1f} minutes, {total_words} words")


if __name__ == "__main__":
    main()
