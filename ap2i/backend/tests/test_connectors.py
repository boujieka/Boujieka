from decimal import Decimal

from conftest import iati_connector, wb_connector

from app.connectors.base import SyncParams, parse_date, parse_decimal


def test_parse_helpers_never_guess():
    assert parse_date("6/30/2028 12:00:00 AM").isoformat() == "2028-06-30"
    assert parse_date("2024-06-14T00:00:00Z").isoformat() == "2024-06-14"
    assert parse_date("not a date") is None and parse_date("") is None
    assert parse_decimal("50,000,000") == Decimal("50000000")
    assert parse_decimal("") is None and parse_decimal("n/a") is None


def test_worldbank_normalization():
    c = wb_connector()
    raws = list(c.fetch(SyncParams(countries=["CMR"])))
    assert {r.source_identifier for r in raws} == {"P900001", "P900002", "P900003"}
    by = {r.source_identifier: c.normalize(r) for r in raws}
    p1 = by["P900001"]
    assert p1.sector_code == "ENERGY" and p1.status == "active" and p1.approval_date.isoformat() == "2018-03-15"
    agr = p1.agreements[0]
    assert agr.amount_original == Decimal("100000000") and agr.currency == "USD"
    assert agr.reported_cumulative_disbursed == Decimal("10000000") and agr.reported_undisbursed == Decimal("90000000")
    assert "44000-P900001" in p1.equivalent_identifiers
    assert by["P900002"].parent_identifier == "P900001"
    assert by["P900002"].agreements[0].commitments[0].kind == "additional"
    dropped = by["P900003"]
    assert dropped.agreements[0].amount_original is None  # 0 on a dropped project is not a zero-value loan
    assert dropped.agreements[0].commitments == []


def test_iati_normalization_hierarchy_and_transactions():
    c = iati_connector()
    raws = {r.source_identifier: r for r in c.fetch(SyncParams(countries=["CMR"]))}
    parent = c.normalize(raws["TEST-FR-3-CCM0001"])
    child = c.normalize(raws["TEST-FR-3-CCM000101"])
    assert parent.agreements == []  # parent with children and no transactions: no duplicate financing
    assert parent.title_language == "fr" and parent.sector_code == "WATER"
    assert child.parent_identifier == "TEST-FR-3-CCM0001"
    agr = child.agreements[0]
    assert agr.partner_code == "AFD" and agr.amount_original == Decimal("20000000") and agr.currency == "EUR"
    assert [f.amount for f in agr.flows] == [Decimal("3000000"), Decimal("2000000")]
    assert agr.instrument_code == "LOAN"
    assert child.locations[0]["lat"] == Decimal("9.30")
    wb = c.normalize(raws["44000-P900001"])
    assert wb.equivalent_identifiers == ["P900001"] and wb.agreements[0].partner_code == "WB"


def test_iati_multi_country_transactions_not_prorated():
    c = iati_connector()
    raw = next(r for r in c.fetch(SyncParams(countries=["CMR"])) if r.source_identifier == "TEST-REGIONAL-1")
    rec = c.normalize(raw)
    agr = rec.agreements[0]
    assert agr.commitments == []  # activity-level commitment covers 2 countries: not attributed
    assert [f.amount for f in agr.flows] == [Decimal("10000000")]  # transaction explicitly for CM
    assert any("Multi-country" in w for w in rec.warnings)


def test_connector_http_retry_then_error():
    import httpx
    import pytest

    from app.connectors.base import ConnectorError
    from app.connectors.worldbank import WorldBankProjectsConnector

    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        return httpx.Response(503)

    c = WorldBankProjectsConnector(client=httpx.Client(transport=httpx.MockTransport(handler)))
    c.min_interval_seconds = 0
    c.max_attempts = 2
    import app.connectors.base as base

    orig = base.time.sleep
    base.time.sleep = lambda s: None
    try:
        with pytest.raises(ConnectorError):
            list(c.fetch(SyncParams(countries=["CMR"])))
    finally:
        base.time.sleep = orig
    assert calls["n"] == 2


def test_placeholder_and_future_actual_dates_are_not_facts():
    from datetime import date, timedelta

    from lxml import etree

    from app.connectors.base import RawRecord

    assert parse_date("1900-01-01") is None and parse_date("1/1/1900 12:00:00 AM") is None
    future = (date.today() + timedelta(days=400)).isoformat()
    xml = (f'<iati-activity default-currency="USD"><iati-identifier>TEST-FUT-1</iati-identifier>'
           f'<title><narrative>SYNTHETIC future dates</narrative></title><recipient-country code="CM"/>'
           f'<activity-date iso-date="2020-01-01" type="2"/><activity-date iso-date="{future}" type="4"/></iati-activity>')
    from app.connectors.iati import IATIConnector

    rec = IATIConnector().normalize(RawRecord("TEST-FUT-1", "iati_activity", "CMR", {}, None, raw_text=xml, payload_format="xml"))
    assert rec.actual_end_date is None and rec.planned_end_date.isoformat() == future
    assert any("in the future" in w for w in rec.warnings)
    assert etree is not None
