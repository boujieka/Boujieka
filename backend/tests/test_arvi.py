"""ARVI pilot: Comtrade normalisation, query splitting, mirror cells, confidence, indicators."""

import json
from decimal import Decimal

from app.arvi.comtrade import PREVIEW_CAP, Archive, Comtrade, Flow, normalise
from app.arvi.mirror import build_cells, indicators, level, score_cells

CODES = {180: "COD", 156: "CHN", 894: "ZMB", 757: "CHE"}


def rec(**kw):
    base = {"customsCode": "C00", "motCode": 0, "partner2Code": 0, "refYear": 2022,
            "cmdCode": "2603", "primaryValue": 100.0, "fobvalue": 100.0, "cifvalue": None,
            "netWgt": 1000.0, "isNetWgtEstimated": False}
    return {**base, **kw}


def flow(reporter, partner, fl, value, kg=None, hs="2603", year=2022):
    return Flow(reporter, partner, fl, hs, year, Decimal(value), "FOB" if fl == "X" else "CIF",
                None if kg is None else Decimal(kg), False, "sha")


def test_normalise_keeps_only_partner_totals():
    ok = normalise(rec(reporterCode=180, partnerCode=156, flowCode="X"), "s", CODES)
    assert ok.reporter == "COD" and ok.partner == "CHN" and ok.valuation == "FOB"
    assert ok.value_usd == Decimal("100.0") and ok.net_kg == Decimal("1000.0")
    # World total, transport breakdown, unknown area: dropped.
    assert normalise(rec(reporterCode=180, partnerCode=0, flowCode="X"), "s", CODES) is None
    assert normalise(rec(reporterCode=180, partnerCode=156, flowCode="X", motCode=2100), "s", CODES) is None
    assert normalise(rec(reporterCode=180, partnerCode=999, flowCode="X"), "s", CODES) is None
    imp = normalise(rec(reporterCode=156, partnerCode=180, flowCode="M", cifvalue=120.0, netWgt=0), "s", CODES)
    assert imp.valuation == "CIF" and imp.net_kg is None


def test_query_splits_when_preview_cap_is_hit(tmp_path):
    calls = []

    def fake_get(url):
        calls.append(url)
        n = PREVIEW_CAP if "cmdCode=2603,7403" in url else 3
        return json.dumps({"count": n, "data": [{"i": i} for i in range(n)]}).encode()

    api = Comtrade(Archive(tmp_path), get=fake_get, sleep=lambda s: None)
    rows = api.query(flow="X", cmd=["2603", "7403"], years=[2019, 2020], reporter=180)
    # One call per year (the preview takes one period); each is capped, then split by code.
    assert len(rows) == 12 and len(calls) == 6
    assert all("period=2019" in u or "period=2020" in u for u in calls)
    assert len(json.loads((tmp_path / "manifest.json").read_text())) == 6


def test_retries_when_rate_limited(tmp_path):
    answers = iter([b'{"statusCode": 429}', json.dumps({"count": 1, "data": [{}]}).encode()])
    api = Comtrade(Archive(tmp_path), get=lambda url: next(answers), sleep=lambda s: None)
    assert len(api.query(flow="M", cmd=["2603"], years=[2022], partner=180)) == 1


def test_mirror_cells_and_indicators():
    flows = [
        flow("COD", "CHN", "X", "1000", kg="1000"),
        flow("CHN", "COD", "M", "1080", kg="1000"),  # +8 %: inside the CIF/FOB band
        flow("COD", "ZMB", "X", "500", kg="400"),  # partner does not declare it
        flow("CHE", "COD", "M", "300", kg="10"),  # exporter does not declare it
        flow("COD", "CHN", "X", "200", kg="20", hs="7403"),
        flow("CHN", "COD", "M", "100", kg="10", hs="7403"),
    ]
    cells = build_cells(flows)
    score_cells(cells)
    chn = cells[("COD", "CHN", "2603", 2022)]
    assert chn.status == "complete" and chn.gap == Decimal("80")
    assert chn.in_cif_band() is True
    assert cells[("COD", "ZMB", "2603", 2022)].status == "export_only"
    assert cells[("COD", "CHE", "2603", 2022)].status == "import_only"
    for c in cells.values():
        assert 0 <= c.score <= 100
    assert chn.score > cells[("COD", "CHE", "2603", 2022)].score

    res = {(r["resource"], r["year"]): r for r in indicators(cells)}[("copper", 2022)]
    a1 = res["arvi1"]
    assert Decimal(a1["x_total"]) == 1700 and Decimal(a1["m_total"]) == 1480
    assert Decimal(a1["complete_positive"]) == 80 and Decimal(a1["complete_negative"]) == -100
    assert Decimal(a1["export_only"]) == 500 and Decimal(a1["import_only"]) == 300
    ore = res["arvi2"][0]
    assert ore["hs"] == "2603" and Decimal(ore["ratio"]) == Decimal("1.08")
    st = res["arvi3"]["by_stage"]
    assert Decimal(st[0]["x"]) == 1500 and Decimal(st[3]["x"]) == 200
    assert res["confidence"]["level"] in {"high", "medium", "low"}


def test_levels():
    assert (level(70), level(69), level(40), level(39)) == ("high", "medium", "medium", "low")
