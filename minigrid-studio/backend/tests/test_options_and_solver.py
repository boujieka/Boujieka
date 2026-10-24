import pytest

from app.engine.options import EngineOptions
from app.engine.prepare import prepare
from app.engine.results import run_scenario
from app.engine.solver import solve
from app.engine.validation import ValidationError


def test_faithful_by_default(base_assumptions):
    r = run_scenario(base_assumptions)
    assert r.status == "reconciled-engine" and r.options == [] and r.failed_checks == []
    assert r.kpis["project_irr"].value == pytest.approx(0.12657422423362732, abs=1e-8)


@pytest.mark.parametrize("opt", [f for f in EngineOptions.__dataclass_fields__])
def test_option_marks_result_as_variant(base_assumptions, opt):
    r = run_scenario(base_assumptions, options=EngineOptions(**{opt: True}))
    assert r.status == "variant" and r.options == [opt]


def test_fix_ops_start_changes_date_only_for_multi_year_builds(base_assumptions):
    a = base_assumptions.replace(**{"timing.project_duration_years": 2})
    faithful = prepare(a).s["Inputs!E17"]
    fixed = prepare(a, EngineOptions(fix_ops_start=True)).s["Inputs!E17"]
    assert faithful == 45627 and fixed == 45658          # 2024-12-01 vs 2025-01-01
    assert prepare(base_assumptions).s["Inputs!E17"] == prepare(
        base_assumptions, EngineOptions(fix_ops_start=True)).s["Inputs!E17"]


def test_fixed_rate_by_year(base_assumptions):
    a = base_assumptions.replace(**{"debt.fixed_rate_by_period": [0.07, 0.08, 0.09, 0.10]})
    _, faithful, _ = solve(a)
    _, fixed, _ = solve(a, options=EngineOptions(fix_fixed_rate_by_year=True))
    assert set(r for r in faithful.v["Debt!45"] if r) == {0.07}       # workbook: always period 1
    assert set(r for r in fixed.v["Debt!45"] if r) == {0.07, 0.08, 0.09, 0.10}


def test_base_rate_2023_plus(base_assumptions):
    a = base_assumptions.replace(**{"debt.rate_choice": "Floating", "macro.base_rates": [0.02, 0.02, 0.05]})
    _, faithful, _ = solve(a)
    _, fixed, _ = solve(a, options=EngineOptions(fix_base_rate_lookup=True))
    assert max(faithful.v["Debt!38"]) == pytest.approx(0.02)   # "2023+" row never used
    assert max(fixed.v["Debt!38"]) == pytest.approx(0.05)


def test_principal_cap_prevents_negative_debt(base_assumptions):
    a = base_assumptions.replace(**{"debt.target_dscr": 0.6})
    r = run_scenario(a)
    assert min(r.series["senior_debt_balance"].values) < 0
    assert any("negative" in w for w in r.warnings)
    capped = run_scenario(a, options=EngineOptions(cap_principal_at_balance=True))
    assert min(capped.series["senior_debt_balance"].values) >= -1e-6


def test_expansion_racking_raises_capex(base_assumptions):
    _, a, _ = solve(base_assumptions)
    _, b, _ = solve(base_assumptions, options=EngineOptions(include_expansion_racking=True))
    modules = sum(a.v["Model!621"])
    assert modules > 0
    assert sum(b.v["Model!649"]) - sum(a.v["Model!649"]) == pytest.approx(2500 * modules, rel=1e-9)


def test_exact_solver_close_to_macros(base_assumptions):
    m = run_scenario(base_assumptions)
    e = run_scenario(base_assumptions, method="exact")
    assert e.status == "variant"
    assert abs(e.kpis["senior_debt"].value - m.kpis["senior_debt"].value) < 50_000
    assert abs(e.kpis["total_funding"].value - e.pasted_values["funding"]) < 1e-3


def test_validation_blocks_impossible_inputs(base_assumptions):
    a = base_assumptions.replace()
    for lot in a.lots:
        lot.included = 0
    with pytest.raises(ValidationError):
        run_scenario(a)
    with pytest.raises(ValidationError):
        run_scenario(base_assumptions.replace(**{"reserves.dsra_months": 13}))


def test_derived_dscr_and_lots(base_assumptions):
    r = run_scenario(base_assumptions, per_lot=True)
    assert r.kpis["min_dscr_repayment"].value == pytest.approx(1.2, abs=1e-9)
    assert r.kpis["min_dscr_repayment"].derived
    lots = [k for k, i in r.kpis.items() if i.experimental]
    assert len([k for k in lots if k.endswith("_project_irr")]) == 3
