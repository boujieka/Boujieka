"""Deterministic financial engine (no generative AI, no network, no randomness).

ENGINE_VERSION identifies the calculation code stored with every run.
RECONCILIATION states what has been verified for that version.
"""
ENGINE_VERSION = "1.0.0"
RECONCILIATION = {
    "reference": "CrossBoundary Access Open Source Model 1.0 (Oct 2023), sha256 fe0ecb16…bb33e",
    "S1_base": "46,860 cells + 920 table cells equal the Excel cached values (1e-9 relative)",
    "S2_S5": "equal LibreOffice cross-check dumps cell by cell; Excel benchmark values still to produce",
    "not_covered": "labels, parameter echo cells, Graph sheet rows (charts only)",
}
