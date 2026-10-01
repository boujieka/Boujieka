# Boujieka: Energy Access Finance Toolkit

Excel financial models for energy-access projects (mini-grids, RBF, viability gap), sold on Etsy and Gumroad.

| Path | Content |
|---|---|
| `product/01-entry-calculator/` | P1: Mini-Grid Financial Feasibility Calculator (.xlsx) + user guide |
| `product/02-developer-edition/` | P2: Energy Access Project Financial Model, Developer Edition (.xlsx) + user guide |
| `docs/COMPARATIF_CROSSBOUNDARY.md` | Feature comparison with the free CrossBoundary Access model (FR) |
| `docs/STRATEGIE_POSITIONNEMENT.md` | Positioning analysis and product roadmap (FR) |
| `marketing/LISTINGS.md` | Etsy and Gumroad listing copy (EN) |
| `tools/build_entry_calculator.py` | Rebuilds the P1 workbook (`pip install openpyxl`) |
| `tools/build_developer_edition.py` | Rebuilds the P2 workbook |
| `tools/check_listing.py` | Checks Etsy title and tag length limits |

Rebuild: `python3 tools/build_entry_calculator.py`, then open the file in Excel (or recalculate with LibreOffice) so cached values are refreshed.
