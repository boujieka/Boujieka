from decimal import Decimal

import pytest

AS_OF = "2026-10-03"
API = "/api/v1"


def get(client, path, **params):
    r = client.get(f"{API}{path}", params=params)
    assert r.status_code == 200, r.text
    return r.json()


def test_health_has_disclaimer(client):
    body = get(client, "/health")
    assert body["status"] == "ok"
    assert "Not investment advice" in body["disclaimer"]


def test_security_headers(client):
    r = client.get(f"{API}/health")
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert r.headers["X-Frame-Options"] == "DENY"


class TestCountries:
    def test_lists_six_mvp_countries(self, client):
        rows = get(client, "/countries")
        assert sorted(c["iso3"] for c in rows) == ["CIV", "CMR", "COG", "GAB", "KEN", "SEN"]

    def test_country_reference_is_flagged_unverified(self, client):
        c = get(client, "/countries/CMR", as_of=AS_OF)
        assert c["currency"] == "XAF"
        assert c["monetary_zone"] == "CEMAC"
        assert c["provenance"]["verification_status"] == "unverified"
        assert c["provenance"]["is_synthetic"] is False
        # Unknown fields are explained, never filled in.
        assert c["tax_notes"] is None
        assert c["field_status"]["tax_notes"] == "not_available"

    def test_regional_sources_attached(self, client):
        cmr = {s["institution"] for s in get(client, "/countries/CMR", as_of=AS_OF)["sources"]}
        civ = {s["institution"] for s in get(client, "/countries/CIV", as_of=AS_OF)["sources"]}
        assert "BEAC" in cmr and "BCEAO" not in cmr
        assert {"BCEAO", "UMOA-Titres", "BRVM"} <= civ and "BEAC" not in civ

    def test_case_insensitive_and_404(self, client):
        assert get(client, "/countries/ken", as_of=AS_OF)["iso3"] == "KEN"
        assert client.get(f"{API}/countries/XXX").status_code == 404

    def test_yield_curve_points_sorted_and_labelled(self, client):
        curve = get(client, "/countries/KEN/yield-curve", as_of=AS_OF)
        tenors = [p["tenor_days"] for p in curve["points"]]
        assert tenors == sorted(tenors) and len(tenors) >= 3
        assert all(p["is_synthetic"] for p in curve["points"])
        assert all(p["auction_date"] <= AS_OF for p in curve["points"])
        assert "no fitting" in curve["method"]


class TestAuctions:
    def test_filters(self, client):
        page = get(
            client,
            "/auctions",
            country="KEN",
            instrument_type="treasury_bill",
            status="completed",
            date_to=AS_OF,
            limit=500,
        )
        assert page["total"] > 0
        for a in page["items"]:
            assert a["security"]["country_iso3"] == "KEN"
            assert a["security"]["instrument_type"] == "treasury_bill"
            assert a["status"] == "completed"
            assert a["auction_date"] <= AS_OF

    def test_multi_country_and_currency(self, client):
        page = get(client, "/auctions", country="CMR,GAB", currency="XAF", limit=500)
        assert {a["security"]["country_iso3"] for a in page["items"]} == {"CMR", "GAB"}

    def test_tenor_filter(self, client):
        page = get(client, "/auctions", min_tenor_days=365, limit=500)
        assert page["items"] and all(a["security"]["tenor_days"] >= 365 for a in page["items"])

    def test_exclude_synthetic_returns_nothing_today(self, client):
        assert get(client, "/auctions", include_synthetic=False)["total"] == 0

    def test_pagination(self, client):
        p1 = get(client, "/auctions", limit=5, offset=0)
        p2 = get(client, "/auctions", limit=5, offset=5)
        assert p1["total"] == p2["total"]
        assert not {a["auction_id"] for a in p1["items"]} & {a["auction_id"] for a in p2["items"]}

    def test_bad_params_rejected(self, client):
        assert client.get(f"{API}/auctions", params={"limit": 0}).status_code == 422
        assert client.get(f"{API}/auctions", params={"status": "bogus"}).status_code == 422

    def test_official_calculated_provenance_are_separate(self, client):
        a = get(client, "/auctions", status="completed", limit=1)["items"][0]
        assert set(a) >= {"official", "calculated", "provenance", "field_status"}
        assert a["calculated"]["data_nature"] == "CALCULATION"
        assert a["provenance"]["data_nature"] == "SYNTHETIC"
        assert a["provenance"]["is_synthetic"] is True
        assert a["provenance"]["source"]["category"] == "synthetic"
        assert a["security"]["security_name"].startswith("[SYNTHETIC]")

    def test_calculated_bid_to_cover_matches_official_amounts(self, client):
        for a in get(client, "/auctions", status="completed", limit=50)["items"]:
            o = a["official"]
            expected = Decimal(o["amount_submitted"]) / Decimal(o["amount_offered"])
            assert abs(Decimal(a["calculated"]["bid_to_cover"]) - expected) <= Decimal("0.00005")
            assert a["calculated"]["bid_to_cover_definition"] == "amount_submitted / amount_offered"

    def test_upcoming_results_pending(self, client):
        page = get(client, "/auctions", status="announced", date_from=AS_OF, limit=500)
        assert page["total"] > 0
        for a in page["items"]:
            assert a["official"]["weighted_average_yield"] is None
            assert a["field_status"]["weighted_average_yield"] == "pending"
            assert a["calculated"]["bid_to_cover"] is None

    def test_not_disclosed_distinguished_from_not_available(self, client):
        items = get(client, "/auctions", status="completed", limit=500)["items"]
        statuses = {a["field_status"].get("number_of_bidders") for a in items}
        assert "not_disclosed" in statuses
        # Bonds' average price is not generated: explicitly "not_available".
        bonds = [a for a in items if a["security"]["instrument_type"] == "treasury_bond"]
        assert bonds and all(b["field_status"]["average_price"] == "not_available" for b in bonds)

    def test_detail_comparison(self, client):
        page = get(client, "/auctions", country="KEN", status="completed", order="desc", limit=1)
        latest = page["items"][0]
        d = get(client, f"/auctions/{latest['auction_id']}")
        cmp = d["comparison"]
        assert cmp["data_nature"] == "CALCULATION"
        assert 0 < cmp["peer_count"] <= 6
        assert "SYNTHETIC" in cmp["caveat"]
        prev = next(p for p in d["peers"] if p["auction_id"] == cmp["previous_auction_id"])
        assert prev["auction_date"] < d["auction_date"]
        assert prev["security"]["tenor_days"] == d["security"]["tenor_days"]
        expected = (
            Decimal(d["official"]["weighted_average_yield"])
            - Decimal(prev["official"]["weighted_average_yield"])
        ) * 100
        assert Decimal(cmp["yield_change_bps"]) == expected.quantize(Decimal("0.01"))

    def test_detail_404(self, client):
        assert client.get(f"{API}/auctions/999999").status_code == 404


class TestSecurities:
    def test_list_and_detail(self, client):
        page = get(client, "/securities", country="SEN", instrument_type="treasury_bond")
        assert page["total"] > 0
        s = get(client, f"/securities/{page['items'][0]['security_id']}")
        assert s["currency"] == "XOF"
        assert s["field_status"]["isin"] == "not_available"
        assert s["auctions"], "bond should have at least its primary auction"
        dates = [a["auction_date"] for a in s["auctions"]]
        assert dates == sorted(dates)


class TestOverview:
    def test_dashboard_consistent_with_auction_list(self, client):
        summary = get(client, "/dashboard/summary", as_of=AS_OF)
        assert summary["countries_monitored"] == 6
        assert summary["synthetic_records_present"] is True
        assert summary["new_opportunities"] is None  # not built yet: must not be faked
        upcoming = get(
            client, "/auctions", status="announced", date_from=AS_OF, date_to="2026-10-10", limit=500
        )
        assert summary["upcoming_auctions_7d"] == upcoming["total"]
        recent = get(
            client, "/auctions", status="completed", date_from="2026-09-27", date_to=AS_OF, limit=500
        )
        assert summary["results_last_7d"] == recent["total"]
        assert summary["cancelled_or_postponed"] == 2

    def test_issuance_by_currency_not_summed_across_currencies(self, client):
        summary = get(client, "/dashboard/summary", as_of=AS_OF)
        currencies = [r["currency"] for r in summary["announced_issuance_by_currency"]]
        assert len(currencies) == len(set(currencies))
        assert set(currencies) <= {"XAF", "XOF", "KES"}

    def test_sources(self, client):
        rows = get(client, "/sources")
        assert rows[0]["priority"] == 1  # central banks first
        assert any(s["category"] == "synthetic" for s in rows)

    def test_data_quality(self, client):
        dq = get(client, "/data-quality", as_of=AS_OF)
        assert dq["synthetic_auctions"] > 0
        assert dq["unverified_records"] == 6  # the six country reference rows
        assert len(dq["sources_pending_configuration"]) == dq["sources_total"] - 1
        assert dq["duplicate_candidates"] == 0
        by_field = {m["field"]: m for m in dq["auction_missing_fields"]}
        nb = by_field["number_of_bidders"]
        assert nb["not_disclosed"] == nb["missing"] > 0
        assert by_field["weighted_average_yield"]["missing"] == 0


@pytest.mark.parametrize(
    "path",
    ["/dashboard/summary", "/auctions", "/countries", "/countries/KEN", "/sources", "/data-quality"],
)
def test_no_ranking_language(client, path):
    """The API must not label anything as a 'best' investment or a buy/sell call."""
    text = client.get(f"{API}{path}", params={"as_of": AS_OF}).text.lower()
    for word in ("best investment", "\"best\"", "strong buy", "guaranteed"):
        assert word not in text


def test_country_sources_ordered_by_priority(client):
    priorities = [s["priority"] for s in get(client, "/countries/KEN", as_of=AS_OF)["sources"]]
    assert priorities == sorted(priorities)
