# Boujieka: Energy Access Finance Toolkit

Excel financial models for energy-access projects (mini-grids, RBF, viability gap), sold on Etsy and Gumroad.

| Path | Content |
|---|---|
| `product/01-entry-calculator/` | P1: Mini-Grid Financial Feasibility Calculator, EN + FR (.xlsx) + user guides |
| `product/02-developer-edition/` | P2: Energy Access Project Financial Model, Developer Edition, EN + FR (.xlsx) + user guides |
| `product/03-fund-manager/` | P3: Energy Access Fund Manager Model, RBF & Portfolio Edition, EN + FR (.xlsx) + user guides |
| `docs/COMPARATIF_CROSSBOUNDARY.md` | Feature comparison with the free CrossBoundary Access model (FR) |
| `docs/STRATEGIE_POSITIONNEMENT.md` | Positioning analysis and product roadmap (FR) |
| `marketing/LISTINGS.md` / `LISTINGS_FR.md` | Etsy and Gumroad listing copy (EN / FR) |
| `tools/build_entry_calculator.py` | Rebuilds the P1 workbook (`pip install openpyxl`) |
| `tools/build_developer_edition.py` | Rebuilds the P2 workbook |
| `tools/build_fund_manager.py` | Rebuilds the P3 workbook |
| `tools/i18n.py`, `tools/i18n_fr.py` | Language layer and French dictionary used by both builders |
| `tools/check_listing.py` | Checks Etsy title and tag length limits (`python3 tools/check_listing.py marketing/LISTINGS_FR.md`) |

Rebuild from the repository root: `python3 tools/build_entry_calculator.py [--lang fr]` `python3 tools/build_developer_edition.py [--lang fr]` and `python3 tools/build_fund_manager.py [--lang fr]`. Then open each file in Excel (or recalculate with LibreOffice) so cached values are refreshed. French builds print any untranslated string to stderr.
