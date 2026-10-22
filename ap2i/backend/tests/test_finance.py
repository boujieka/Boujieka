from datetime import date
from decimal import Decimal

from sqlalchemy import select

import app.models as m
from app.finance.fx import FX
from app.finance.indicators import agreement_position, project_financials, ratio
from app.finance.portfolio import compute_portfolio, snapshot_portfolio


def add_rate(db, base, quote, rate, year):
    db.add(m.ExchangeRate(base_currency=base, quote_currency=quote, rate=Decimal(rate), period=str(year), period_type="annual_avg",
                          source="TEST synthetic rate"))
    db.commit()


def test_ratio_never_divides_by_missing_or_zero():
    assert ratio(Decimal(1), None) is None and ratio(None, Decimal(1)) is None and ratio(Decimal(1), Decimal(0)) is None
    assert ratio(Decimal(1), Decimal(3)) == Decimal("0.3333")


def test_fx_uses_year_specific_rate_and_refuses_missing(db):
    add_rate(db, "USD", "XAF", "600", 2020)
    add_rate(db, "USD", "EUR", "0.9", 2020)
    add_rate(db, "XDR", "USD", "1.4", 2020)
    fx = FX(db)
    assert fx.convert(Decimal(600), "XAF", "USD", 2020).value == Decimal("1.00")
    assert fx.convert(Decimal(90), "EUR", "XAF", 2020).value == Decimal("60000.00")
    assert fx.convert(Decimal(10), "XDR", "USD", 2020).value == Decimal("14.00")
    missing = fx.convert(Decimal(600), "XAF", "USD", 2021)
    assert missing.value is None and "2021" in missing.reason  # no substitution with another year
    assert fx.convert(Decimal(5), "XAF", "USD", None).value is None


def test_agreement_positions_from_sources(loaded):
    db = loaded
    wb = db.scalar(select(m.FinancingAgreement).where(m.FinancingAgreement.source_identifier == "P900001"))
    pos = agreement_position(db, wb)
    assert pos.currency == "USD" and pos.committed == Decimal("100000000") and pos.disbursed == Decimal("10000000")
    assert "World Bank" in pos.disbursed_basis  # published cumulative preferred over summed transactions
    afd = db.scalar(select(m.FinancingAgreement).where(m.FinancingAgreement.source_identifier == "TEST-FR-3-CCM000101"))
    pos2 = agreement_position(db, afd)
    assert pos2.committed == Decimal("20000000") and pos2.disbursed == Decimal("5000000") and pos2.undisbursed == Decimal("15000000")


def test_project_indicators_transparent(loaded):
    db = loaded
    p = db.scalar(select(m.Project).join(m.ProjectIdentifier).where(m.ProjectIdentifier.identifier == "TEST-FR-3-CCM0001"))
    fin = project_financials(db, p, today=date(2023, 1, 1))
    ind = {i["code"]: i for i in fin["indicators"]}
    assert ind["disbursement_rate"]["value"] == "0.2500"
    assert ind["disbursement_rate"]["formula"]
    assert ind["cost_overrun"]["value"] is None and "original estimated cost" in ind["cost_overrun"]["missing_inputs"]
    assert ind["financing_gap"]["value"] is None
    assert fin["totals_by_currency"]["EUR"]["committed"] == "20000000.0000"


def test_annual_portfolio_counts_projects_once_and_dates_flows(loaded):
    db = loaded
    add_rate(db, "USD", "EUR", "0.9", 2020)
    pf = compute_portfolio(db, "CMR", 2018, 2021)
    years = {y["year"]: y for y in pf["years"]}
    # P900001 approved 2018; its Additional Financing (2021) must not create a second approved project.
    assert years[2018]["counts"]["approved"] == 1
    assert years[2021]["counts"]["approved"] == 0
    assert years[2020]["disbursements"]["by_currency"] == {"EUR": "3000000.0000", "USD": "6000000.0000"}
    assert years[2020]["disbursements"]["usd_equivalent"] == "9333333.33"
    assert years[2021]["disbursements"]["usd_complete"] is False  # no 2021 EUR rate stored
    ids_2020 = years[2020]["project_ids"]["active"]
    assert len(ids_2020) == len(set(ids_2020))


def test_snapshots_are_reproducible_and_never_deleted(loaded):
    db = loaded
    s1 = snapshot_portfolio(db, "CMR", 2019, 2020)
    s2 = snapshot_portfolio(db, "CMR", 2019, 2020)
    assert [s.id for s in s1] == [s.id for s in s2]  # same inputs -> same snapshot
    p = db.scalar(select(m.Project).limit(1))
    p.status = "suspended"
    db.commit()
    s3 = snapshot_portfolio(db, "CMR", 2019, 2020, note="correction")
    assert s3[0].id != s1[0].id and s3[0].is_current
    old = db.get(m.AnnualFinancialSnapshot, s1[0].id)
    assert old is not None and old.is_current is False
