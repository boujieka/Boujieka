import json
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]          # minigrid-studio/
REF_VALUES = ROOT / "reference_values"
WORKBOOK = ROOT / "reference" / "CrossBoundary-Access-Open-Source-Model-1.0-October-2023.xlsm"
LO_DUMPS = ROOT / "work" / "lo_out"
SCENARIOS = json.loads((ROOT / "tools" / "phase0" / "scenarios.json").read_text())["scenarios"]


@pytest.fixture(scope="session")
def base_assumptions():
    from app.engine.assumptions import from_dict
    return from_dict(json.loads((REF_VALUES / "S1_base_inputs.json").read_text()))


def needs_workbook():
    return pytest.mark.skipif(not WORKBOOK.exists(), reason="reference workbook not present (not redistributable)")
