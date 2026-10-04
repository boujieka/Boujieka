# Manual 7

- `MANUAL7_User_and_Methodology.md`: source (v1.0 release candidate 1).
- `build/MANUAL7_User_and_Methodology.pdf`: A4 house edition; `build/MANUAL7_User_and_Methodology.docx`: Word edition.

Rebuild: convert headings with the step in the session log (top-level sections become chapters), then
`python3 tools/house/publish_docs.py manual/build/manual7_render.md manual/build/MANUAL7_User_and_Methodology.pdf --title "MANUAL 7: User and Methodology Manual" --kicker "MANUAL 7" ...`
and `python3 tools/book7/build_docx7.py --src manual/build/manual7_render.md --out manual/build/MANUAL7_User_and_Methodology.docx --kicker "MANUAL 7" ...`.
