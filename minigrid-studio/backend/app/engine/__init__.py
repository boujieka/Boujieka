"""Deterministic financial engine (no generative AI, no network, no randomness).

ENGINE_VERSION identifies the calculation code stored with every run.
RECONCILIATION states what has been verified for that version.
"""
ENGINE_VERSION = "1.0.0"
RECONCILIATION = {
    "reference": "CrossBoundary Access Open Source Model 1.0 (Oct 2023), sha256 fe0ecb16…bb33e",
    "S1_base": "46,860 cells + 920 table cells equal the Excel cached values within max(1e-9 relative, 1e-6 absolute); the 5 XIRR cells differ from Excel by ~2e-9 absolute",
    "S2_S5": "equal LibreOffice cross-check dumps cell by cell except rolling IRRs Model!372/429 and the EOMONTH(0) dates Inputs!J364/L364, Debt!F68; same for 10 feature scenarios; Excel benchmark values still to produce",
    "not_covered": "4,237 Graph sheet cells and 688 other cells (labels, parameter echoes, Inputs!413-430 intermediate demand rows, Dashboard!K37) of the 52,401 formulas; 47,476 are compared",
}
