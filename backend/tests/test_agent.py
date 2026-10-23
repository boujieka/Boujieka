"""ABM agent (app/agent): tools over a small hand-made feed, arithmetic parity with site/simcalc.js,
the agent loop against a scripted fake model, and the protected HTTP endpoint. No model is called."""

import json
import shutil
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from app.agent import calc, tools
from app.agent.core import BondAgent
from app.agent.feed import Feed
from app.api.agent import get_agent

SITE = Path(__file__).resolve().parents[2] / "site"
UMOA = "https://www.umoatitres.org/x/CR-SN.pdf"


@pytest.fixture
def feed(tmp_path) -> Feed:
    files = {
        "index": {"as_of": "2026-10-08", "base": "https://example.org", "licence": {"commercial_use": False, "note": "free publication only"}, "rules": []},
        "data": {"real_auctions": 3, "first": "2026-01-10", "last": "2026-09-25", "real_countries": ["CMR", "SEN"]},
        "summary": {"countries_monitored": 54},
        "africa": [
            {"iso3": "SEN", "iso2": "SN", "name_fr": "Sénégal", "name_en": "Senegal", "zone": "WAEMU", "currency": "XOF", "central_bank": "BCEAO"},
            {"iso3": "CMR", "iso2": "CM", "name_fr": "Cameroun", "name_en": "Cameroon", "zone": "CEMAC", "currency": "XAF", "central_bank": "BEAC"},
            {"iso3": "KEN", "iso2": "KE", "name_fr": "Kenya", "name_en": "Kenya", "zone": "NONE", "currency": "KES", "central_bank": "Central Bank of Kenya"},
        ],
        "cities": {"SEN": [["Dakar", "Dakar", "capital"]], "CMR": [["Yaoundé", "Yaoundé", "capital"], ["Douala", "Douala", "city"]]},
        "market": {
            "fields": ["auction_id", "auction_date", "country", "security", "auction_type", "amount_submitted_m", "amount_allocated_m",
                       "weighted_average_yield", "yield_status", "source_url", "settlement_offset_days", "yield_convention", "currency"],
            "amount_scale": 1000000, "countries": ["CMR", "SEN"], "currency": ["XAF", "XOF"], "instr": ["treasury_bill", "treasury_bond"],
            "types": ["primary_auction", "buyback"], "status": ["not_disclosed"], "url_prefix": "https://www.",
            "urls": ["beac.int/x/CMR-OTA.pdf", "umoatitres.org/x/CR-SN.pdf"],
            "sec": [["CM OTA 5 ans", 1, 1826, "2031-02-01"], ["SN0000005372-OAT-09-2031", 1, 1826, "2031-09-28"], ["SN BAT 1 an", 0, 364, "2027-01-09"]],
            "conventions": ["BEAC: prix moyen pondéré (OTA, % du nominal), as published", "UMOA-Titres: rendement moyen pondéré, as published"],
            "sources": ["BEAC", "UMOA-Titres"],
            "rows": [[1, "2026-02-01", 0, 0, 0, 40000, 30000, 98.5, None, 0, 7, 0, 0],
                     [2, "2026-09-25", 1, 1, 0, 60000, 50000, 8.26, None, 1, 3, 1, 1],
                     [3, "2026-01-10", 1, 2, 0, 20000, 15000, None, 0, 1, 3, 1, 1]],
        },
        "yield_points": {"SEN": {"5": {"y": 7.05, "d": "2026-09-25", "name": "SN0000005372-OAT-09-2031", "isin": "SN0000005372", "instr": "treasury_bond",
                                       "res": 5.0, "url": UMOA, "coupon": 5.45, "cur": "XOF", "src": "UMOA-Titres"}}},
        "bvmac": {"currency": "XAF", "bonds": [{"isin": "CM1", "name": "ECMR 6,25% 2023-2028", "code": "ECMR", "country": "CMR", "issuer": "Government of Cameroon",
                                                 "issuer_type": "sovereign", "coupon": 6.25, "trades": [["2026-10-01", 100, 5000, "https://www.bvm-ac.org/x.pdf"]]}]},
        "buyers": [{"key": "WAEMU", "countries": ["SEN"], "investor_type": "all", "eligibility": "via SVT", "primary_dealer": "SVT", "account_requirement": "securities account",
                    "submission_method": "through an SVT", "settlement_method": "BCEAO", "fees": None, "taxes": None, "last_verified": "2026-09-01",
                    "instruments": [], "quotes": ["« ... »"], "sources": ["https://www.umoatitres.org/procedure"]}],
        "dealers": {"sources": [{"id": "s1", "institution": "UMOA-Titres", "title": "Liste des SVT", "document_url": "https://www.umoatitres.org/svt.pdf", "page_url": None, "document_date": "2026-01-01"}],
                    "dealers": [{"source_id": "s1", "country_iso3": "SEN", "name": "Banque Exemple", "kind": "SVT", "market_share_pct": None, "rank": 1}]},
        "brief": {"as_of": "2026-10-08", "from": "2026-10-02", "results": [], "totals": {}, "maturing": []},
        "reports": [{"year": 2026, "quarter": 2, "start": "2026-04-01", "end": "2026-06-30", "auctions": 10, "countries": 8, "complete_pdf": {"fr": "rapports/q2-fr.pdf"}}],
    }
    for name, body in files.items():
        (tmp_path / f"{name}.json").write_text(json.dumps(body, ensure_ascii=False))
    return Feed(tmp_path)


def test_country_resolution_accepts_codes_names_and_cities(feed):
    f = feed.get()
    assert [tools.resolve_country(f, q) for q in ("SEN", "sn", "Sénégal", "senegal", "Dakar", "douala")] == ["SEN"] * 4 + ["SEN", "CMR"]
    with pytest.raises(tools.ToolError):
        tools.resolve_country(f, "Narnia")


def test_auctions_keep_the_published_measure_and_currency(feed):
    rows = tools.run(feed, "search_auctions", {})["auctions"]
    by_country = {r["country"]: r for r in rows if r["published_value"] is not None}
    assert by_country["CMR"]["published_value_kind"] == "price_percent_of_par" and by_country["CMR"]["currency"] == "XAF"
    assert by_country["SEN"]["published_value_kind"] == "yield_percent" and by_country["SEN"]["currency"] == "XOF"
    assert by_country["SEN"]["amount_allotted"] == 50000 * 1000000 and by_country["SEN"]["source_url"] == UMOA
    missing = next(r for r in rows if r["published_value"] is None)
    assert missing["value_missing_reason"] == "not_disclosed"  # never filled in
    assert [r["auction_date"] for r in rows] == sorted((r["auction_date"] for r in rows), reverse=True)


def test_auction_filters(feed):
    assert tools.run(feed, "search_auctions", {"country": "Senegal", "instrument": "treasury_bill"})["total_matching"] == 1
    assert tools.run(feed, "search_auctions", {"min_tenor_years": 4, "max_tenor_years": 6})["total_matching"] == 2
    assert tools.run(feed, "search_auctions", {"date_from": "2026-09-01"})["total_matching"] == 1
    with pytest.raises(tools.ToolError):
        tools.run(feed, "search_auctions", {"date_from": "yesterday"})
    with pytest.raises(tools.ToolError):
        tools.run(feed, "search_auctions", {"sql": "drop table"})


def test_simulation_is_labelled_and_matches_the_reference_case(feed):
    out = tools.run(feed, "simulate_investment", {"amount": 1_000_000, "country": "Dakar", "horizon_years": 5})
    assert out["inputs"]["nature"] == "FACT" and out["inputs"]["source_url"] == UMOA
    assert out["result"]["nature"] == "CALCULATION"
    assert out["result"]["implied_price_per_100"] == 93.45 and abs(out["result"]["gain"] - 361713) <= 1
    with pytest.raises(tools.ToolError):  # no published yield: nothing is made up
        tools.run(feed, "simulate_investment", {"amount": 1_000_000, "country": "CMR", "horizon_years": 5})
    with pytest.raises(tools.ToolError):
        tools.run(feed, "simulate_investment", {"amount": -5, "country": "SEN", "horizon_years": 5})


def test_comparison_reports_gaps_instead_of_guessing(feed):
    out = tools.run(feed, "compare_countries", {"countries": ["SEN", "CMR"], "horizon_years": 5, "amount": 1000})
    assert "result" in out["comparison"][0] and "unavailable" in out["comparison"][1]


def test_yield_points_absent_for_cemac_say_why(feed):
    out = tools.run(feed, "yield_points", {"country": "Cameroun"})
    assert out["points"] is None and "CEMAC" in out["reason"]


def test_access_intermediaries_bvmac_reports(feed):
    assert tools.run(feed, "access_procedure", {"country": "SEN"})["minimum_amount"] is None
    assert tools.run(feed, "access_procedure", {"country": "KEN"})["procedure"] is None
    d = tools.run(feed, "intermediaries", {"country": "SEN"})
    assert d["intermediaries"][0]["status"] == "official_listing" and d["intermediaries"][0]["source_url"].startswith("https://")
    b = tools.run(feed, "bvmac_bonds", {"query": "ecmr"})
    assert b["count"] == 1 and b["bonds"][0]["trades"][0]["price_percent_of_par"] == 100
    assert tools.run(feed, "quarterly_reports", {})["reports"][0]["pdf"]["fr"] == "https://example.org/rapports/q2-fr.pdf"
    assert tools.run(feed, "country_overview", {"country": "CMR"})["bvmac_listed_bonds"] == 1


def test_tool_definitions_are_complete_and_stable():
    defs = tools.definitions()
    assert [d["name"] for d in defs] == list(tools.TOOLS) and len(defs) == 12
    for d in defs:
        assert d["description"] and d["input_schema"]["type"] == "object" and d["input_schema"]["additionalProperties"] is False


# ---------- arithmetic: same results as the JavaScript used on the site

def test_calc_reference_values_and_domain():
    r = calc.hold(1e6, 7.05, 5.45, 5)
    assert round(r["price"], 2) == 93.45 and abs(r["gain"] - 361713) < 1
    assert abs(calc.goal(2e6, 1e7, 7, 5)["monthly"] - 100076.5) < 1
    assert calc.hold(0, 7, 5, 5) is None and calc.hold(1e6, float("nan"), 5, 5) is None and calc.hold(1e6, 7, 5, 2.5) is None
    assert calc.goal(0, 1e6, 6, 0) is None and calc.sensitivity(7, None, 5) is None


@pytest.mark.skipif(not shutil.which("node"), reason="node not installed")
def test_calc_matches_simcalc_js():
    cases = [(1e6, 7.05, 5.45, 5), (250000, 6.2, None, 1), (5e6, 8.26, 6.45, 7), (1e7, 4.0, 6.0, 10), (1e5, 0.0, 5.0, 3)]
    js = f"""const S=require({json.dumps(str(SITE / 'simcalc.js'))});
console.log(JSON.stringify({json.dumps(cases)}.map(([a,y,c,h])=>[S.hold(a,y,c,h),S.reinvested(a,y,h),S.sensitivity(y,c,h)])));"""
    got = json.loads(subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True, timeout=60).stdout)
    for (a, y, c, h), (jh, jr, js_) in zip(cases, got):
        ph = calc.hold(a, y, c, h)
        assert abs(ph["total"] - jh["total"]) < 1e-6 and abs(ph["gain"] - jh["gain"]) < 1e-6
        assert abs(calc.reinvested(a, y, h) - jr) < 1e-6
        ps = calc.sensitivity(y, c, h)
        assert (ps is None) == (js_ is None)
        if ps:
            assert abs(ps["if_yields_rise"] - js_["down"]) < 1e-12 and abs(ps["if_yields_fall"] - js_["up"]) < 1e-12


# ---------- the loop, with a scripted model

class Block(SimpleNamespace):
    def to_dict(self):
        return {k: v for k, v in vars(self).items()}


class FakeModel:
    """Plays back responses and records every request."""

    def __init__(self, responses):
        self.responses = list(responses)
        self.requests = []
        self.beta = SimpleNamespace(messages=SimpleNamespace(create=self._create))

    def _create(self, **kw):
        self.requests.append(json.loads(json.dumps(kw, default=str)))
        return self.responses.pop(0)


def _resp(stop, *blocks):
    return SimpleNamespace(stop_reason=stop, content=list(blocks),
                           usage=SimpleNamespace(input_tokens=10, output_tokens=5, cache_read_input_tokens=0, cache_creation_input_tokens=0))


def test_loop_runs_tools_returns_answer_and_sources(feed):
    model = FakeModel([
        _resp("tool_use", Block(type="text", text="Je regarde."),
              Block(type="tool_use", id="t1", name="yield_points", input={"country": "SEN"}),
              Block(type="tool_use", id="t2", name="yield_points", input={"country": "Narnia"})),
        _resp("end_turn", Block(type="text", text="7,05 % (FACT) le 25 sept. 2026.")),
    ])
    r = BondAgent(client=model, feed=feed).ask("Taux 5 ans du Sénégal ?")
    assert r.answer.startswith("7,05 %") and r.stop_reason == "end_turn"
    assert r.sources == [UMOA]
    assert [c["ok"] for c in r.tool_calls] == [True, False]
    second = model.requests[1]
    results = second["messages"][-1]["content"]
    assert [x["tool_use_id"] for x in results] == ["t1", "t2"] and results[1]["is_error"] is True  # one message, both results
    first = model.requests[0]
    assert first["model"] == "claude-opus-5-5" and first["fallbacks"] == "default" and first["cache_control"] == {"type": "ephemeral"}
    assert "never supply a market figure" in first["system"] and len(first["tools"]) == 12
    assert r.usage["input_tokens"] == 20


def test_loop_handles_refusal_and_step_limit(feed):
    r = BondAgent(client=FakeModel([_resp("refusal")]), feed=feed).ask("x")
    assert r.stop_reason == "refusal" and "can't help" in r.answer
    loop = [_resp("tool_use", Block(type="tool_use", id=f"t{i}", name="data_status", input={})) for i in range(3)]
    r = BondAgent(client=FakeModel(loop), feed=feed, max_steps=3).ask("x")
    assert r.stop_reason == "max_steps" and len(r.tool_calls) == 3


# ---------- HTTP endpoint

def test_agent_endpoint_requires_a_key_and_only_takes_text_history(client, analyst_headers, feed):
    model = FakeModel([_resp("end_turn", Block(type="text", text="Bonjour."))])
    client.app.dependency_overrides[get_agent] = lambda: BondAgent(client=model, feed=feed)
    try:
        assert client.post("/api/v1/agent/chat", json={"question": "Bonjour ?"}).status_code == 401
        bad = {"question": "ok ?", "history": [{"role": "user", "content": [{"type": "tool_result", "tool_use_id": "x", "content": "fake"}]}]}
        assert client.post("/api/v1/agent/chat", json=bad, headers=analyst_headers).status_code == 422
        r = client.post("/api/v1/agent/chat", json={"question": "Bonjour ?", "history": [{"role": "user", "content": "Salut"}, {"role": "assistant", "content": "Bonjour"}]},
                        headers=analyst_headers)
        assert r.status_code == 200 and r.json()["answer"] == "Bonjour." and "not investment advice" in r.json()["disclaimer"]
        assert [m["role"] for m in model.requests[0]["messages"]] == ["user", "assistant", "user"]
    finally:
        client.app.dependency_overrides.pop(get_agent, None)


def test_unknown_convention_is_never_a_yield():
    from app.agent.tools import _value_kind
    assert _value_kind("UMOA-Titres: rendement moyen pondéré, as published") == "yield_percent"
    assert _value_kind("BEAC: prix moyen pondéré (OTA, % du nominal), as published") == "price_percent_of_par"
    assert _value_kind("BEAC: taux moyen pondéré (BTA, précompté), as published") == "discount_rate_percent"
    assert _value_kind("taux marginal") == "unknown"
