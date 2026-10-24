"""Cell-by-cell reconciliation against the source workbook and LibreOffice
cell dumps. Skipped when those files are absent (they are not redistributed)."""
import json

import pytest

from app.engine import reconcile as R
from app.engine.assumptions import apply_cells
from app.engine.loader import load_assumptions
from app.engine.model import run_model
from app.engine.prepare import prepare
from app.engine.solver import solve

from .conftest import FEATURE_SCENARIOS, LO_DUMPS, LO_FEATURE_DUMPS, SCENARIOS, WORKBOOK, needs_workbook


@needs_workbook()
def test_loader_matches_committed_inputs(base_assumptions):
    from app.engine.assumptions import to_dict
    assert to_dict(load_assumptions(WORKBOOK)) == to_dict(base_assumptions)


@needs_workbook()
def test_every_reproduced_cell_matches_excel():
    a = load_assumptions(WORKBOOK)
    p = prepare(a)
    L = run_model(a, p)
    values = R.workbook_values(str(WORKBOOK))
    rep = R.reconcile(L, values)
    assert rep.compared > 46000
    assert rep.ok, rep.summary()
    tables = R.reconcile_tables(p.tables, values)
    assert tables.ok, tables.summary()


# Model!372/429 (rolling IRR): LibreOffice returns 0 where Excel finds negative IRRs.
# Inputs!J364: LibreOffice reads date serial 0 differently from Excel (EOMONTH(0, 143)).
LO_SKIP = {"Model!372", "Model!429", "Inputs!J364"}


ALL_LO = [(s, LO_DUMPS) for s in SCENARIOS] + [(s, LO_FEATURE_DUMPS) for s in FEATURE_SCENARIOS]


@pytest.mark.parametrize("sc,folder", ALL_LO, ids=[s["id"] for s, _ in ALL_LO])
def test_every_reproduced_cell_matches_libreoffice(base_assumptions, sc, folder):
    dump = folder / f"{sc['id']}_cells.json"
    if not dump.exists():
        pytest.skip("LibreOffice cell dumps not generated (tools/phase0/lo_scenarios.py --dump-cells)")
    solved, L, _ = solve(apply_cells(base_assumptions, sc["set"]))
    rep = R.reconcile(L, R.json_values(str(dump)), skip_rows=LO_SKIP)
    rep.mismatches = [m for m in rep.mismatches if m.key not in LO_SKIP]
    assert rep.compared > 46000
    assert rep.ok, rep.summary()
