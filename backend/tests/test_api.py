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
    def test_lists_all_54_countries_with_coverage(self, client):
        rows = get(client, "/countries")
        assert len(rows) == 54
        assert all(c["coverage_tier"] == "market_data" for c in rows)
        assert all(c["name_fr"] and c["region"] for c in rows)

    def test_extended_country_profile(self, client):
        c = get(client, "/countries/NGA", as_of=AS_OF)
        assert c["coverage_tier"] == "market_data"
        assert c["currency"] == "NGN" and c["completed_auction_count"] > 0
        assert c["provenance"]["verification_status"] == "unverified"
        assert any(s["category"] == "central_bank" for s in c["sources"])

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
        assert summary["countries_monitored"] == 54
        assert summary["countries_with_market_data"] == 54
        assert summary["synthetic_records_present"] is True
        assert isinstance(summary["new_opportunities"], int)
        upcoming = get(
            client, "/auctions", status="announced", date_from=AS_OF, date_to="2026-10-10", limit=500
        )
        assert summary["upcoming_auctions_7d"] == upcoming["total"]
        recent = get(
            client, "/auctions", status="completed", date_from="2026-09-27", date_to=AS_OF, limit=500
        )
        assert summary["results_last_7d"] == recent["total"]
        disrupted = get(client, "/auctions", status=["cancelled", "postponed"], date_from=AS_OF, limit=500)
        assert summary["cancelled_or_postponed"] == disrupted["total"]

    def test_issuance_by_currency_not_summed_across_currencies(self, client):
        summary = get(client, "/dashboard/summary", as_of=AS_OF)
        currencies = [r["currency"] for r in summary["announced_issuance_by_currency"]]
        assert len(currencies) == len(set(currencies))
        from app.seed.africa import AFRICA

        assert set(currencies) <= {c.currency for c in AFRICA}

    def test_sources(self, client):
        rows = get(client, "/sources")
        assert rows[0]["priority"] == 1  # central banks first
        assert any(s["category"] == "synthetic" for s in rows)

    def test_data_quality(self, client):
        dq = get(client, "/data-quality", as_of=AS_OF)
        assert dq["synthetic_auctions"] > 0
        assert dq["unverified_records"] == 54  # the 54 country reference rows
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


def test_sources_expose_unconfirmed_candidates(client):
    rows = {s["name"]: s for s in get(client, "/sources")}
    cbk = rows["Central Bank of Kenya — auction results"]
    assert cbk["base_url"] is None
    assert any(c["url"].startswith("https://www.centralbank.go.ke/") for c in cbk["candidates"])


class TestOpportunityRadar:
    @pytest.fixture(scope="class", autouse=True)
    def engine_run(self, seeded):
        from sqlalchemy.orm import Session

        from app.engine.opportunities import run

        with Session(seeded) as s:
            run(s, __import__("datetime").date(2026, 10, 3))
            s.commit()

    def test_list_and_country_filter(self, client):
        page = get(client, "/opportunities", country="KEN")
        assert page["total"] > 0
        assert set(page["by_country"]) == {"KEN"}
        assert "not recommendations" in page["disclaimer"]

    def test_criteria_matching(self, client):
        page = get(client, "/opportunities", min_yield="9", currency="KES", limit=500)
        assert page["criteria"] == {"min_yield": "9", "currency": "KES"}
        for o in page["items"]:
            meets = (o["yield_pct"] is not None and Decimal(o["yield_pct"]) >= 9 and o["currency"] == "KES")
            assert o["matches_criteria"] is meets
            assert bool(o["criteria_unmet"]) is (not meets)
        only = get(client, "/opportunities", min_yield="9", currency="KES", matching_only=True, limit=500)
        assert only["total"] == sum(o["matches_criteria"] for o in page["items"])

    def test_no_criteria_means_no_matching_flag(self, client):
        assert all(o["matches_criteria"] is None for o in get(client, "/opportunities")["items"])

    def test_heat_grid(self, client):
        grid = get(client, "/market/heat-grid", as_of=AS_OF)
        names = [r["country_name"] for r in grid["rows"]]
        assert len(names) == 54 and names == sorted(names)
        for row in grid["rows"]:
            buckets = [c["bucket"] for c in row["cells"]]
            assert len(buckets) == len(set(buckets))
            for c in row["cells"]:
                if c["demand_z"] is not None:
                    assert c["demand_peer_count"] >= 6

    def test_maturity_wall_shares_sum_to_100(self, client):
        wall = get(client, "/countries/CMR/maturity-wall", as_of=AS_OF)
        assert len(wall["months"]) == 12
        assert wall["data_nature"] == "SYNTHETIC"
        total = sum(Decimal(m["share_pct"]) for m in wall["months"])
        assert abs(total - 100) <= Decimal("0.1")

    def test_dashboard_counts_active_signals(self, client):
        summary = get(client, "/dashboard/summary", as_of=AS_OF)
        assert summary["new_opportunities"] == get(client, "/opportunities", limit=500)["total"]


class TestBuyers:
    # Countries documented on 2026-10-04 and the instruments their official sources describe.
    NEW_ROUTES = {
        "NGA": {"treasury_bond"},
        "GHA": {"treasury_bill", "treasury_bond"},
        "ZAF": {"treasury_bond"},
        "TZA": {"treasury_bill", "treasury_bond"},
        "UGA": {"treasury_bill", "treasury_bond"},
        "RWA": {"treasury_bond"},
    }
    OFFICIAL_HOSTS = {
        "www.beac.int", "www.umoatitres.org", "www.centralbank.go.ke", "www.dmo.gov.ng", "www.bog.gov.gh",
        "www.rsaretailbonds.gov.za", "www.bot.go.tz", "bou.or.ug", "www.bnr.rw",
    }

    def test_routes_cover_pilot_zones(self, client):
        rows = get(client, "/subscription-routes")
        # 6 CEMAC + 8 WAEMU countries x 2 instruments, Kenya x 2, then 9 routes for the six new countries.
        assert len(rows) == 39
        assert {r["country_iso3"] for r in rows if r["monetary_zone"] == "CEMAC"} == {"CMR", "CAF", "TCD", "COG", "GNQ", "GAB"}
        assert len({r["country_iso3"] for r in rows if r["monetary_zone"] == "WAEMU"}) == 8
        assert {r["instrument_type"] for r in get(client, "/subscription-routes", country="KEN")} == {"treasury_bill", "treasury_bond"}

    def test_new_countries_have_only_documented_instruments(self, client):
        for iso3, instruments in self.NEW_ROUTES.items():
            rows = get(client, "/subscription-routes", country=iso3)
            assert {r["instrument_type"] for r in rows} == instruments, iso3
            assert all(r["last_verified"] == "2026-10-04" for r in rows)

    def test_every_route_is_sourced_and_quoted(self, client):
        from urllib.parse import urlparse

        for r in get(client, "/subscription-routes"):
            assert r["official_source_url"].startswith("https://")
            assert urlparse(r["official_source_url"]).hostname in self.OFFICIAL_HOSTS
            assert r["last_verified"] in {"2026-10-03", "2026-10-04"}
            assert r["quotes"] and all(len(q) > 40 for q in r["quotes"])
            assert len(set(r["quotes"])) == len(r["quotes"])
            assert len(r["investor_type"]) <= 64  # subscription_route.investor_type is VARCHAR(64)
            assert r["fees"] is None and r["taxes"] is None  # never filled from the sources: not invented
            assert "not advice" in r["disclaimer"]

    def test_new_quotes_are_verbatim_shaped(self):
        # Quotes are copied from English-language sources: no paraphrase markers or French text.
        from app.seed.subscription_routes import COUNTRY_ROUTES, VERIFIED_ON_2

        new = [r for r in COUNTRY_ROUTES if r.get("verified_on") == VERIFIED_ON_2]
        assert {r["iso3"] for r in new} == set(self.NEW_ROUTES)
        for r in new:
            assert r["source_url"].startswith("https://")
            for q in r["quotes"]:
                assert len(q) > 40 and q == q.strip() and "  " not in q
                assert not any(w in q for w in (" les ", " des ", "...", "[", "]"))

    def test_country_without_route_returns_empty(self, client):
        assert get(client, "/subscription-routes", country="MAR") == []


class TestAccreditedDealers:
    def test_counts_match_official_documents(self, client):
        data = get(client, "/accredited-dealers")
        by_src: dict[str, int] = {}
        for d in data["dealers"]:
            by_src[d["source_id"]] = by_src.get(d["source_id"], 0) + 1
        # UMOA-Titres: 24 SVT over 8 states (45 state/SVT pairs); BEAC table 29 (Gabon duplicate removed);
        # DMO 14 PDMM; BoG 15 PD; National Treasury 10 PD; Morocco top 3 only; BoU 8 PD banks (T-bill
        # tender 1235); BoT 51 registered CDPs (2022 guidelines); BoM 4 PD (2017 notice).
        assert by_src == {"umoa_rank_2024": 45, "beac_shares_2021": 76, "beac_list_2022": 94,
                          "dmo_pdmm_2023": 14, "bog_pd_2026": 15, "ntsa_pd_2025": 10, "mef_ivt_2025": 3,
                          "bou_pd_2026": 8, "bot_cdp_2022": 51, "bom_pd_2017": 4}
        assert len({d["name"] for d in data["dealers"] if d["source_id"] == "bot_cdp_2022"}) == 51
        assert len({d["name"] for d in data["dealers"] if d["source_id"] == "umoa_rank_2024"}) == 24
        assert "not a recommendation" in data["disclaimer"]

    def test_every_source_is_official_and_dated(self, client):
        for s in get(client, "/accredited-dealers")["sources"]:
            assert s["page_url"].startswith("https://") and s["quote"] and s["document_date"]
            assert s["verified_on"] == "2026-10-04" and s["data_nature"] == "FACT"
            assert s["measure"] in {"list", "rank", "share"}

    def test_shares_only_where_published_and_sum_to_100(self, client):
        data = get(client, "/accredited-dealers")
        totals: dict[str, float] = {}
        for d in data["dealers"]:
            if d["source_id"] != "beac_shares_2021":
                assert d["market_share_pct"] is None  # no other source publishes per-institution shares
                continue
            totals[d["country_iso3"]] = totals.get(d["country_iso3"], 0) + float(d["market_share_pct"])
        assert set(totals) == {"CMR", "CAF", "COG", "GAB", "GNQ", "TCD"}
        assert all(abs(v - 100) <= 0.2 for v in totals.values()), totals

    def test_ranks_are_contiguous_per_country(self, client):
        ranks: dict[tuple[str, str], list[int]] = {}
        for d in get(client, "/accredited-dealers")["dealers"]:
            if d["rank"] is not None:
                ranks.setdefault((d["source_id"], d["country_iso3"]), []).append(d["rank"])
        assert ranks and all(sorted(v) == list(range(1, len(v) + 1)) for v in ranks.values())

    def test_country_filter(self, client):
        sen = get(client, "/accredited-dealers", country="sen")
        assert [s["id"] for s in sen["sources"]] == ["umoa_rank_2024"]
        assert {d["country_iso3"] for d in sen["dealers"]} == {"SEN"} and len(sen["dealers"]) == 6
        uga = get(client, "/accredited-dealers", country="UGA")
        assert [s["id"] for s in uga["sources"]] == ["bou_pd_2026"] and len(uga["dealers"]) == 8
        assert get(client, "/accredited-dealers", country="KEN") == {**get(client, "/accredited-dealers", country="KEN"), "sources": [], "dealers": []}
