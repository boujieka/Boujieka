"""Engine vs committed reference values (runs without the source workbook).

S1: values Excel cached in the published workbook (genuine Excel results).
S2-S5: LibreOffice cross-check values (provisional, not Excel benchmarks).
"""
import json

import pytest

from app.engine.assumptions import apply_cells
from app.engine.solver import solve

from .conftest import REF_VALUES, SCENARIOS

TIMELINE = 69


def _value(L, ref):
    sh, addr = ref.split("!")
    if addr.startswith("I") and addr[1:].isdigit():
        return L.totals[f"{sh}!{addr[1:]}"]
    return L.s[ref]


def _compare(L, solved, ref, spec, rel=1e-9, abs_=1e-6):
    bad = []
    for k, (cell, _label, _unit) in spec["scalars"].items():
        exp, got = ref["scalars"][k], _value(L, cell)
        if k.startswith("check_"):
            ok = abs(exp - got) <= 1e-6   # Excel zeroes such residues (~1e-10) of cancelling sums
        else:
            ok = abs(exp - got) <= max(abs_, rel * abs(exp))
        if not ok:
            bad.append((k, exp, got))
    for k, (sh, row, _label) in spec["series"].items():
        for t, exp in enumerate(ref["series"][k]):
            got = L.v[f"{sh}!{row}"][t]
            if abs(exp - got) > max(abs_, rel * abs(exp)):
                bad.append((f"{k}[{t}]", exp, got))
    for k, cell in spec["pasted_values"].items():
        exp = ref["pasted_values"][k]
        got = {"funding_pasted": solved.pasted.funding, "dscr_pasted": solved.pasted.dscr_limit,
               "refi_pasted": solved.pasted.refi_limit, "dsra_pasted": solved.pasted.dsra_initial}[k]
        if abs(exp - got) > max(abs_, rel * abs(exp)):
            bad.append((k, exp, got))
    return bad


@pytest.fixture(scope="module")
def spec():
    return json.loads((REF_VALUES.parent / "tools" / "phase0" / "outputs_spec.json").read_text())


def test_s1_matches_excel_cached_values(base_assumptions, spec):
    ref = json.loads((REF_VALUES / "S1_base_excel_cached.json").read_text())
    solved, L, log = solve(base_assumptions)
    assert log.converged and log.rounds == 0     # the published state already passes the macro checks
    assert _compare(L, solved, ref, spec) == []


@pytest.mark.parametrize("sc", SCENARIOS, ids=[s["id"] for s in SCENARIOS])
def test_scenarios_match_libreoffice_crosscheck(base_assumptions, spec, sc):
    ref = json.loads((REF_VALUES / "provisional_libreoffice" / f"{sc['id']}_libreoffice.json").read_text())
    a = apply_cells(base_assumptions, sc["set"])
    solved, L, log = solve(a)
    assert log.converged
    assert _compare(L, solved, ref, spec) == []
