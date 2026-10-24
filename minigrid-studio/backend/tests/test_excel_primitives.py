import datetime as dt

import pytest

from app.engine import excel as X


def test_round_half_away_from_zero():
    assert X.xround(2.5) == 3 and X.xround(-2.5) == -3 and X.xround(0.5) == 1
    assert X.xround(2.675, 2) == 2.68          # Excel, not binary-float 2.67
    assert X.xround(443.88, -5) == 0 and X.xround(-50000, -5) == -100000 and X.xround(49999.9, -5) == 0


def test_roundup_rounddown():
    assert X.roundup(2.0000001) == 3 and X.roundup(-2.1) == -3 and X.roundup(2.0) == 2
    assert X.rounddown(2.9) == 2 and X.rounddown(-2.9) == -2


def test_eomonth_and_serials():
    s = X.to_serial(dt.date(2023, 1, 1))
    assert s == 44927
    assert X.from_serial(X.eomonth(s, 11)) == dt.date(2023, 12, 31)
    assert X.from_serial(X.eomonth(s, 1)) == dt.date(2023, 2, 28)
    # Excel's serial 0 is 1900-01-00: EOMONTH(0, 143) = 1911-12-31 (cached in Inputs!J364)
    assert X.from_serial(X.eomonth(0, 143)) == dt.date(1911, 12, 31)


def test_lookup_approximate_and_mixed_types():
    assert X.lookup(2024, [2021, 2022, "2023+"], [1, 2, 3]) == 2   # text key skipped
    assert X.lookup(5, [0, 5, 10, 15], ["a", "b", "c", "d"]) == "b"
    assert X.lookup(99, [0, 5, 10, 15], ["a", "b", "c", "d"]) == "d"
    with pytest.raises(X.ExcelNA):
        X.lookup(-1, [0, 5], [1, 2])


def test_irr_family():
    assert X.npv(0.1, [110]) == pytest.approx(100)
    assert X.irr([-100, 110]) == pytest.approx(0.1, abs=1e-12)
    assert X.irr([-100, 1, 1]) == pytest.approx(1 / ((-1 + 401 ** 0.5) / 2) - 1, abs=1e-9)  # negative IRR, as Excel finds
    d = [X.to_serial(dt.date(2023, 12, 31)), X.to_serial(dt.date(2024, 12, 31))]
    assert X.xirr([-100, 110], d) == pytest.approx(1.1 ** (365 / 366) - 1, abs=1e-10)
    assert X.iferror(lambda: X.irr([1, 2]), 0.0) == 0.0
