"""Financial calculations validated independently.

Expected values come from (a) hand-worked textbook examples and (b) an
exact rational-arithmetic reimplementation using fractions.Fraction, so the
tests do not merely re-run the code under test.
"""

from decimal import Decimal
from fractions import Fraction

import pytest

from app.analytics import calculations as calc

D = Decimal


def frac_price_simple(y_pct: str, days: int, basis: int) -> Fraction:
    return Fraction(100) / (1 + Fraction(y_pct) / 100 * Fraction(days, basis))


def frac_price_discount(d_pct: str, days: int, basis: int) -> Fraction:
    return 100 * (1 - Fraction(d_pct) / 100 * Fraction(days, basis))


def close(a: Decimal, b: Fraction, tol: str = "1e-20") -> bool:
    return abs(Fraction(a) - b) < Fraction(tol)


class TestTextbookExamples:
    def test_discount_bill_price(self):
        # 90-day bill at a 5% bank-discount rate, ACT/360:
        # P = 100 * (1 - 0.05 * 90/360) = 100 * (1 - 0.0125) = 98.75 exactly.
        assert calc.price_from_discount_rate(D("5"), 90, 360) == D("98.75")

    def test_discount_rate_from_price(self):
        assert calc.discount_rate_from_price(D("98.75"), 90, 360) == D("5")

    def test_money_market_yield_from_discount_price(self):
        # y = (100/98.75 - 1) * 360/90 = (0.0126582278...) * 4 = 5.0632911392...%
        y = calc.simple_yield_from_price(D("98.75"), 90, 360)
        assert y.quantize(D("1e-8")) == D("5.06329114")

    def test_discount_to_simple_yield_conversion(self):
        # Money-market yield always exceeds the discount rate for the same price.
        y = calc.discount_rate_to_simple_yield(D("5"), 90, 360)
        assert y > D("5")
        assert y.quantize(D("1e-8")) == D("5.06329114")

    def test_simple_price_182d(self):
        # P = 100 / (1 + 0.10 * 182/360) = 100 / 1.050555... = 95.18773...
        p = calc.price_from_simple_yield(D("10"), 182, 360)
        assert p.quantize(D("1e-5")) == D("95.18773")

    def test_basis_matters(self):
        p360 = calc.price_from_simple_yield(D("10"), 182, 360)
        p365 = calc.price_from_simple_yield(D("10"), 182, 365)
        # Longer year => less accrued interest => higher price.
        assert p365 > p360


@pytest.mark.parametrize("basis", [360, 365])
@pytest.mark.parametrize("days", [28, 91, 182, 273, 364])
@pytest.mark.parametrize("rate", ["0.5", "4.25", "9.875", "17.3", "35"])
class TestAgainstRationalArithmetic:
    def test_simple_price(self, rate, days, basis):
        assert close(calc.price_from_simple_yield(D(rate), days, basis), frac_price_simple(rate, days, basis))

    def test_discount_price(self, rate, days, basis):
        assert close(
            calc.price_from_discount_rate(D(rate), days, basis), frac_price_discount(rate, days, basis)
        )

    def test_simple_round_trip(self, rate, days, basis):
        price = calc.price_from_simple_yield(D(rate), days, basis)
        assert abs(calc.simple_yield_from_price(price, days, basis) - D(rate)) < D("1e-25")

    def test_discount_round_trip(self, rate, days, basis):
        price = calc.price_from_discount_rate(D(rate), days, basis)
        assert abs(calc.discount_rate_from_price(price, days, basis) - D(rate)) < D("1e-25")


class TestRatios:
    def test_bid_to_cover(self):
        assert calc.bid_to_cover(D("51.8"), D("23.4")) == D("51.8") / D("23.4")
        assert calc.bid_to_cover(D("30"), D("20")) == D("1.5")

    def test_ratios_return_none_when_missing_or_zero(self):
        assert calc.bid_to_cover(None, D("1")) is None
        assert calc.bid_to_cover(D("1"), None) is None
        assert calc.bid_to_cover(D("1"), D("0")) is None
        assert calc.allocation_rate(D("1"), D("0")) is None
        assert calc.acceptance_rate(D("1"), D("0")) is None
        assert calc.submitted_to_allocated(D("1"), None) is None

    def test_allocation_and_acceptance(self):
        assert calc.allocation_rate(D("18"), D("20")) == D("0.9")
        assert calc.acceptance_rate(D("18"), D("30")) == D("0.6")
        assert calc.submitted_to_allocated(D("30"), D("18")) == D("30") / D("18")

    def test_change_bps(self):
        assert calc.change_bps(D("10.25"), D("10.00")) == D("25.00")
        assert calc.change_bps(D("9.9"), D("10.15")) == D("-25.00")
        assert calc.change_bps(None, D("10")) is None


class TestValidation:
    @pytest.mark.parametrize("basis", [0, 252, 366])
    def test_rejects_unknown_basis(self, basis):
        with pytest.raises(ValueError):
            calc.price_from_simple_yield(D("5"), 91, basis)

    @pytest.mark.parametrize("days", [0, -1])
    def test_rejects_non_positive_days(self, days):
        with pytest.raises(ValueError):
            calc.price_from_discount_rate(D("5"), days, 360)

    def test_rejects_non_positive_price(self):
        with pytest.raises(ValueError):
            calc.simple_yield_from_price(D("0"), 91, 360)

    def test_quantize_bankers_rounding(self):
        assert calc.quantize(D("1.00005"), 4) == D("1.0000")
        assert calc.quantize(D("1.00015"), 4) == D("1.0002")
        assert calc.quantize(None) is None
