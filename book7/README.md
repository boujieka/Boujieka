# Book 7: Hydropower Development and Finance

First edition, version 0.4 (pre-publication review draft). Author: Emmanuel Boujieka Kamga. Africa Energy Finance, Business & Financial Models.

The book follows the format of the collection's PAYGo solar book: one decision per chapter, a place in the analytical chain, points for the investment and credit committees, and a "Working with the model" section tied to MODEL 7 (`model/Bankable_Hydro_Model.xlsx`).

## Contents

- `src/ch00_front.md` front matter and introduction; `src/ch01.md` to `src/ch18.md` chapters; `src/ch99_annexes.md` annexes A to M.
- `src/figures/` figures drawn from the model.
- `build/Hydropower_Development_and_Finance.pdf` A4 house edition; `build/Hydropower_Development_and_Finance.docx` Word edition.

## Build

```
python3 model/build_model.py                       # rebuild the workbook
RECALC=<recalc.py> python3 tools/run_snapshots.py  # recalculate and run all scenarios (writes model/snapshot_results.json)
python3 tools/book7/figures7.py                    # figures
python3 tools/book7/prepare7.py                    # numbers, generated tables, sources, style lint -> build/book7_resolved.md
cd book7/build && python3 ../../tools/house/publish_docs.py book7_resolved.md Hydropower_Development_and_Finance.pdf \
  --title "Hydropower Development and Finance" --subtitle "From River to Financial Close: A Developer, Lender and Government Framework for Hydropower Projects in Africa" \
  --kicker "BOOK 7" --edition "First edition, version 0.4 (pre-publication review draft)" --case "Kasiri River Hydro case" \
  --keywords "hydropower; project development; project finance; Africa"
python3 tools/book7/build_docx7.py                 # Word edition
```

Every number in the text is a placeholder resolved from the workbook or the scenario runs; no figure is typed by hand.

## Open items before release

- Sources flagged "Search summary only" in Annex L must be read in full.
- Test the workbook in Microsoft Excel (tested in LibreOffice only).
- Practitioner review; 7 x 10 in print interior not yet produced for this book.
