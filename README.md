# BANKABLE HYDRO
### Structuring Hydropower Projects Without Creating Unsustainable Public Liabilities
*Africa Energy Finance Series, Product 7 (v1.0, 2026-10-03)*

> **Can this project actually deliver bankable power without creating unsustainable public liabilities?**
>
> Technical feasibility is not financial bankability. Financial bankability is not sustainable public finance.

## What is in this repository

| Component | Path | Status |
|---|---|---|
| A. Professional book (first-draft manuscript) | `book/BANKABLE_HYDRO_Manuscript.md` | 17 chapters + annexes |
| B. Integrated financial and bankability model | `model/Bankable_Hydro_Model.xlsx` | 35 sheets, ~9,800 live formulas, 0 errors, checks ALL OK |
| Model source code (single source of truth) | `model/build_model.py` | Python / openpyxl |
| Scenario / structure / sensitivity runner | `tools/run_snapshots.py` | 29 full-engine runs via LibreOffice |
| C. User manual | `manual/USER_MANUAL.md` | v1.0 |
| D. Video course (scripts) | `course/VIDEO_COURSE.md` | 8 modules, 32 lessons, capstone |
| E. Case study library | `case_library/README.md`, `research/case_studies/` | 21 African + 7 international cases |
| F. Research / source database | `research/source_database.md`, `.csv` | 85 sources, 31 benchmark ranges |
| Competitive intelligence | `research/competitive_intelligence.md` | 33 products, competitor and market-gap matrices |
| Product design and positioning | `docs/00_PRODUCT_DESIGN.md` | – |

## Rebuild and verify

```bash
pip install openpyxl                 # LibreOffice with Calc must be installed for recalculation
python model/build_model.py          # writes model/Bankable_Hydro_Model.xlsx (formulas only)
python <path>/recalc.py model/Bankable_Hydro_Model.xlsx 200   # LibreOffice recalculation, or open and save in Excel
RECALC=<path>/recalc.py python tools/run_snapshots.py   # refreshes snapshot tables (sheets 27, 17A, 28)
python tools/book/build_book.py      # builds book/Bankable_Hydro_Book.docx and .pdf
```

## Honesty notes

- The reference project **Lumora Falls / Republic of Navaria is entirely fictional**.
- Real projects appear only as public-source benchmarks, each with source IDs.
- Facts marked "snippet" or "search-result only" were not read in full text and must be verified before publication.
- Where data could not be verified, the files say **PUBLIC DATA NOT FOUND**.
- Gate thresholds, fiscal screening thresholds and call probabilities are **illustrative user inputs**, not sourced norms.
- The fiscal module is a *project-level screen*. It does not replace IMF/World Bank DSA or PFRAM.
- The brief for this product was received cut off in Part 20 (Case Study Engine). Later parts, if any, are not implemented.
- Nothing here is investment, legal, tax or accounting advice.
