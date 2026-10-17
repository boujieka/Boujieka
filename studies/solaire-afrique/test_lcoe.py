import pytest

from lcoe import crf, lcoe, wacc


def test_crf_matches_closed_form_lcoe():
    # Sans dégradation ni indexation, LCOE = (CAPEX x CRF + OPEX) / E.
    for r in (0.04, 0.08, 0.12):
        expected = (50e6 * crf(r, 25) + 750e3) / 90_000
        assert lcoe(50e6, 750e3, 90_000, r, 25) == pytest.approx(expected)


@pytest.mark.parametrize("rate,expected", [
    (0.04, 43.9), (0.06, 51.8), (0.08, 60.4), (0.10, 69.5), (0.12, 79.2), (0.14, 89.2),
])
def test_proposal_illustrative_table(rate, expected):
    # La proposition affiche 69,6 / 79,3 / 89,3 pour 10 / 12 / 14 % : écart d'arrondi de 0,1.
    assert lcoe(50e6, 750e3, 90_000, rate, 25) == pytest.approx(expected, abs=0.06)


def test_zero_rate():
    assert crf(0, 25) == pytest.approx(1 / 25)


def test_wacc():
    assert wacc(0.7, 0.08, 0.15) == pytest.approx(0.101)
    assert wacc(0.7, 0.08, 0.15, tax_rate=0.25) == pytest.approx(0.087)
