"""The agent's tools: read-only questions over the published feed (app/agent/feed.py).

Each tool returns plain JSON. Published values carry "nature": "FACT" and their source document;
arithmetic on them carries "nature": "CALCULATION" with its inputs and assumptions. A missing value
is returned as null with a reason, never estimated. The same functions back the HTTP endpoint, the
command line and the MCP server, so every surface answers from the same verified rows.
"""

from __future__ import annotations

import unicodedata
from datetime import date
from typing import Any, Callable

from app.agent import calc
from app.agent.feed import Feed

HORIZONS = (1, 3, 5, 7, 10)
MAX_ROWS = 50
DISCLAIMER = "Information only, not investment advice. Published values are FACTs from the cited official documents."


class ToolError(ValueError):
    """A bad or unanswerable request; shown to the model as an error result it can recover from."""


# ---------- helpers

def _fold(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", str(s)) if not unicodedata.combining(c)).casefold().strip()


def _countries(f: dict) -> dict[str, dict]:
    return {a["iso3"]: a for a in f["africa"]}


def resolve_country(f: dict, text: str | None) -> str | None:
    """ISO3 code from an ISO2/ISO3 code, a French or English country name, or a listed city."""
    if text is None or not str(text).strip():
        return None
    q = _fold(text)
    cs = _countries(f)
    for a in cs.values():
        if q in (a["iso3"].casefold(), a["iso2"].casefold(), _fold(a["name_fr"]), _fold(a["name_en"])):
            return a["iso3"]
    for iso, cities in (f.get("cities") or {}).items():
        if any(q in (_fold(fr), _fold(en)) for fr, en, _ in cities):
            return iso
    partial = [a["iso3"] for a in cs.values() if q and (q in _fold(a["name_fr"]) or q in _fold(a["name_en"]))]
    if len(partial) == 1:
        return partial[0]
    hint = f" Did you mean one of: {', '.join(cs[i]['name_en'] for i in partial[:6])}?" if partial else ""
    raise ToolError(f"Unknown country '{text}'. Use an ISO3 code (e.g. SEN) or a country name.{hint}")


def _date(s: str | None, field: str) -> str | None:
    if s in (None, ""):
        return None
    try:
        return date.fromisoformat(str(s)[:10]).isoformat()
    except ValueError as e:
        raise ToolError(f"{field} must be a date YYYY-MM-DD, got '{s}'") from e


def _horizon(h: Any) -> int:
    if h not in HORIZONS:
        raise ToolError(f"horizon_years must be one of {list(HORIZONS)}")
    return int(h)


def _amount(a: Any, field: str = "amount") -> float:
    if not isinstance(a, (int, float)) or isinstance(a, bool) or not 0 < a <= 1e12:
        raise ToolError(f"{field} must be a number above 0 and at most 1e12")
    return float(a)


def _round(v: float | None, d: int = 2) -> float | None:
    return None if v is None else round(v, d)


def _value_kind(convention: str) -> str:
    c = convention.casefold()
    if "prix" in c or "price" in c:
        return "price_percent_of_par"
    if "précompté" in c or "precompte" in c:
        return "discount_rate_percent"
    return "yield_percent"


def _market_rows(f: dict) -> list[dict]:
    """Expand the compact market.json rows (see site/build.py market())."""
    m = f["market"]
    ix = {k: i for i, k in enumerate(m["fields"])}
    scale = m.get("amount_scale", 1)
    has_conv = "yield_convention" in ix
    cs = _countries(f)
    out = []
    for r in m["rows"]:
        sec = m["sec"][r[ix["security"]]]
        country = m["countries"][r[ix["country"]]]
        url = m["url_prefix"] + m["urls"][r[ix["source_url"]]]
        conv = m["conventions"][r[ix["yield_convention"]]] if has_conv else None
        cur = m["currency"][r[ix["currency"]]] if "currency" in ix else cs.get(country, {}).get("currency")
        val = r[ix["weighted_average_yield"]]
        why = r[ix["yield_status"]]
        out.append({
            "auction_date": r[ix["auction_date"]], "country": country, "security": sec[0],
            "instrument": m["instr"][sec[1]], "tenor_days": sec[2], "maturity_date": sec[3],
            "auction_type": m["types"][r[ix["auction_type"]]], "currency": cur,
            "amount_submitted": None if r[ix["amount_submitted_m"]] is None else r[ix["amount_submitted_m"]] * scale,
            "amount_allotted": None if r[ix["amount_allocated_m"]] is None else r[ix["amount_allocated_m"]] * scale,
            "published_value": val, "published_value_kind": _value_kind(conv) if conv else "unknown",
            "published_convention": conv,
            "value_missing_reason": None if why is None else m["status"][why],
            "source_url": url, "nature": "FACT",
        })
    return out


# ---------- tools

def data_status(f: dict) -> dict:
    """What the feed covers and how fresh it is."""
    idx, d = f["index"], f["data"]
    return {
        "as_of": idx.get("as_of"), "verified_auctions": d.get("real_auctions"), "first_auction": d.get("first"),
        "last_auction": d.get("last"), "countries_with_market_data": d.get("real_countries"),
        "countries_monitored": f["summary"].get("countries_monitored"),
        "sources": f["market"].get("sources"), "published_value_conventions": f["market"].get("conventions"),
        "licence": idx.get("licence"), "rules": idx.get("rules"),
        "note": "CEMAC (BEAC) results publish weighted average prices for bonds (OTA) and discount rates for bills (BTA); WAEMU (UMOA-Titres) results publish yields.",
    }


def country_overview(f: dict, country: str) -> dict:
    iso = resolve_country(f, country)
    a = _countries(f)[iso]
    rows = [r for r in _market_rows(f) if r["country"] == iso]
    issued = [r for r in rows if r["auction_type"] == "primary_auction"]
    card = next((b for b in f["buyers"] if iso in b["countries"]), None)
    dealers = {d["name"] for d in f["dealers"]["dealers"] if d["country_iso3"] == iso}
    bonds = [b for b in f["bvmac"]["bonds"] if b["country"] == iso]
    return {
        "country": iso, "name_en": a["name_en"], "name_fr": a["name_fr"], "zone": a["zone"], "currency": a["currency"],
        "central_bank": a["central_bank"],
        "verified_auctions": len(rows), "primary_auctions": len(issued),
        "first_auction": min((r["auction_date"] for r in rows), default=None),
        "last_auction": max((r["auction_date"] for r in rows), default=None),
        "latest_published_yields": yield_points(f, iso)["points"] if iso in f["yield_points"] else None,
        "access_procedure_available": card is not None, "listed_intermediaries": len(dealers),
        "bvmac_listed_bonds": len(bonds),
        "coverage_note": None if rows else "No verified auction data for this country in the feed.",
    }


def search_auctions(f: dict, country: str | None = None, date_from: str | None = None, date_to: str | None = None,
                    instrument: str | None = None, auction_type: str | None = None,
                    min_tenor_years: float | None = None, max_tenor_years: float | None = None,
                    limit: int = 20) -> dict:
    iso = resolve_country(f, country)
    lo, hi = _date(date_from, "date_from"), _date(date_to, "date_to")
    if instrument not in (None, "", "treasury_bill", "treasury_bond"):
        raise ToolError("instrument must be treasury_bill or treasury_bond")
    if auction_type not in (None, "", "primary_auction", "buyback"):
        raise ToolError("auction_type must be primary_auction or buyback")
    limit = max(1, min(int(limit or 20), MAX_ROWS))
    rows = []
    for r in _market_rows(f):
        if iso and r["country"] != iso or lo and r["auction_date"] < lo or hi and r["auction_date"] > hi:
            continue
        if instrument and r["instrument"] != instrument or auction_type and r["auction_type"] != auction_type:
            continue
        years = None if r["tenor_days"] is None else r["tenor_days"] / 365.25
        if (min_tenor_years is not None or max_tenor_years is not None) and years is None:
            continue
        if min_tenor_years is not None and years < min_tenor_years or max_tenor_years is not None and years > max_tenor_years:
            continue
        rows.append(r)
    rows.sort(key=lambda r: (r["auction_date"], r["security"]), reverse=True)
    return {"total_matching": len(rows), "returned": min(len(rows), limit), "auctions": rows[:limit],
            "note": "Most recent first. Amounts are in the row's currency (XOF and XAF are never added together)."}


def yield_points(f: dict, country: str | None = None) -> dict:
    """Latest verified published yield per country and horizon (last 12 months), as used by the simulators."""
    yp = f["yield_points"]
    iso = resolve_country(f, country)
    keep = {iso: yp.get(iso)} if iso else yp
    out = {c: {h: {"published_yield_percent": p["y"], "auction_date": p["d"], "security": p["name"], "isin": p["isin"],
                   "instrument": p["instr"], "residual_years_at_auction": p["res"], "coupon_percent": p["coupon"],
                   "currency": p["cur"], "source": p["src"], "source_url": p["url"], "nature": "FACT"}
               for h, p in sorted(pts.items(), key=lambda kv: int(kv[0]))}
           for c, pts in keep.items() if pts}
    res = {"as_of": f["index"].get("as_of"), "points": out.get(iso) if iso else out,
           "method": "For each horizon, the latest verified issuance auction of the last 12 months whose residual maturity falls in the horizon window (1y: 0.9-1.1, 3y: 2-4, 5y: 4-6, 7y: 6-8.5, 10y: 8.5-15 years)."}
    if iso and not out:
        res["points"] = None
        res["reason"] = "No published yield in the last 12 months for this country (CEMAC results publish prices or discount rates, not comparable yields)."
    return res


def simulate_investment(f: dict, amount: float, country: str, horizon_years: int) -> dict:
    amount, h = _amount(amount), _horizon(horizon_years)
    iso = resolve_country(f, country)
    p = (f["yield_points"].get(iso) or {}).get(str(h))
    if not p:
        raise ToolError(f"No published yield for {iso} at {h} years in the last 12 months; try yield_points to see the available horizons.")
    r = calc.hold(amount, p["y"], p["coupon"], h)
    if r is None:
        raise ToolError("The calculation is undefined for these inputs.")
    sens = calc.sensitivity(p["y"], p["coupon"], h)
    return {
        "inputs": {"nature": "FACT", "published_yield_percent": p["y"], "coupon_percent": p["coupon"], "auction_date": p["d"],
                   "security": p["name"], "currency": p["cur"], "source": p["src"], "source_url": p["url"]},
        "result": {"nature": "CALCULATION", "amount": amount, "horizon_years": h,
                   "implied_price_per_100": _round(r["price"]), "nominal_bought": _round(r["nominal"], 0),
                   "annual_income": _round(r["annual_income"], 0), "repaid_at_maturity": _round(r["repaid"], 0),
                   "total_received": _round(r["total"], 0), "gain": _round(r["gain"], 0),
                   "value_if_coupons_reinvested": _round(calc.reinvested(amount, p["y"], h), 0),
                   "resale_change_if_yields_rise_1pt_percent": None if not sens else _round(sens["if_yields_rise"] * 100, 1),
                   "resale_change_if_yields_fall_1pt_percent": None if not sens else _round(sens["if_yields_fall"] * 100, 1)},
        "assumptions": ["held to maturity", "annual coupons", "bought at the price implied by the published yield",
                        "no fees, no taxes", "bills: simple interest, renewed at the same rate" if p["coupon"] is None else "bond priced over whole years",
                        "not a forecast; repayment is not guaranteed by this calculation"],
    }


def compare_countries(f: dict, countries: list[str], horizon_years: int, amount: float) -> dict:
    if not isinstance(countries, list) or not 1 <= len(countries) <= 5:
        raise ToolError("countries must be a list of 1 to 5 countries")
    out = []
    for c in countries:
        try:
            out.append({"country": resolve_country(f, c), **simulate_investment(f, amount, c, horizon_years)})
        except ToolError as e:
            out.append({"country": c, "unavailable": str(e)})
    return {"horizon_years": horizon_years, "amount": amount, "comparison": out,
            "note": "Same amount and horizon; no ranking, rating or recommendation. A higher rate usually pays for a higher risk."}


def savings_goal(f: dict, capital: float, target: float, years: int, rate_percent: float) -> dict:
    if not isinstance(years, int) or not 1 <= years <= 40:
        raise ToolError("years must be a whole number from 1 to 40")
    g = calc.goal(float(capital), _amount(target, "target"), float(rate_percent), years)
    if g is None:
        raise ToolError("Inputs out of range: capital >= 0, target > 0, rate 0-40 %.")
    return {"nature": "CALCULATION", "monthly_saving": _round(g["monthly"], 0), "months": g["months"],
            "already_reached": g["already_reached"], "assumption": "constant rate, monthly compounding; real rates will change"}


def access_procedure(f: dict, country: str) -> dict:
    iso = resolve_country(f, country)
    b = next((b for b in f["buyers"] if iso in b["countries"]), None)
    if not b:
        return {"country": iso, "procedure": None,
                "reason": f"No sourced access procedure for this country yet. The central bank ({_countries(f)[iso]['central_bank']}) or the Treasury publishes it."}
    keys = ("investor_type", "eligibility", "primary_dealer", "account_requirement", "submission_method",
            "settlement_method", "fees", "taxes", "last_verified")
    return {"country": iso, "zone_or_card": b["key"], "covers": b["countries"], "nature": "FACT (procedure summarised from the sources; quotes are authoritative)",
            **{k: b.get(k) for k in keys}, "minimum_amount": None, "minimum_amount_reason": "not stated by the sources",
            "instruments": b.get("instruments"), "verbatim_quotes": b.get("quotes"), "sources": b.get("sources")}


def intermediaries(f: dict, country: str | None = None, kind: str | None = None, name: str | None = None,
                   limit: int = 30) -> dict:
    iso = resolve_country(f, country)
    src = {s["id"]: s for s in f["dealers"]["sources"]}
    q = _fold(name) if name else None
    rows = [d for d in f["dealers"]["dealers"] if (not iso or d["country_iso3"] == iso)
            and (not kind or d["kind"] == kind) and (not q or q in _fold(d["name"]))]
    limit = max(1, min(int(limit or 30), MAX_ROWS))
    return {
        "total_matching": len(rows), "returned": min(len(rows), limit),
        "intermediaries": [{"name": d["name"], "kind": d["kind"], "country": d["country_iso3"], "status": "official_listing",
                            "rank": d.get("rank"), "market_share_percent": d.get("market_share_pct"),
                            "listed_by": src.get(d["source_id"], {}).get("institution"),
                            "list_title": src.get(d["source_id"], {}).get("title"),
                            "list_date": src.get(d["source_id"], {}).get("document_date"),
                            "source_url": src.get(d["source_id"], {}).get("document_url") or src.get(d["source_id"], {}).get("page_url")}
                           for d in rows[:limit]],
        "kinds": sorted({d["kind"] for d in f["dealers"]["dealers"]}),
        "note": "Being on an official list is neither a ranking of quality nor a recommendation; check the licence with the regulator.",
    }


def bvmac_bonds(f: dict, query: str | None = None, country: str | None = None) -> dict:
    iso = resolve_country(f, country)
    q = _fold(query) if query else None
    out = []
    for b in f["bvmac"]["bonds"]:
        if iso and b["country"] != iso or q and q not in _fold(f"{b['isin']} {b['name']} {b.get('code') or ''} {b['issuer']}"):
            continue
        out.append({"isin": b["isin"], "name": b["name"], "code": b.get("code"), "issuer": b["issuer"],
                    "issuer_type": b.get("issuer_type"), "country": b["country"], "coupon_percent": b.get("coupon"),
                    "currency": f["bvmac"].get("currency", "XAF"),
                    "trades": [{"date": t[0], "price_percent_of_par": t[1], "volume": t[2], "source_url": t[3], "nature": "FACT"}
                               for t in b["trades"][:10]],
                    "trade_days_known": len(b["trades"])})
    return {"bonds": out, "count": len(out), "note": "Only days with a trade are observations; a quoted price without a trade is not shown."}


def weekly_brief(f: dict) -> dict:
    b = f["brief"]
    return {"as_of": b["as_of"], "from": b["from"], "results": b["results"], "totals_by_currency": b["totals"],
            "maturing_next_days": b["maturing"], "nature": "FACT (results); totals are CALCULATION per currency"}


def quarterly_reports(f: dict) -> dict:
    base = f["index"].get("base", "https://cartouche-africa.netlify.app").rstrip("/")
    def absu(u):
        if isinstance(u, dict):
            return {k: absu(v) for k, v in u.items()}
        return u if not isinstance(u, str) or u.startswith("http") else f"{base}/{u.lstrip('/')}"
    return {"reports": [{"quarter": f"{r['year']}-Q{r['quarter']}", "period": [r["start"], r["end"]], "auctions": r["auctions"],
                         "countries": r["countries"], "pdf": absu(r.get("complete_pdf") or r.get("preview_pdf"))}
                        for r in f["reports"]]}


# ---------- registry: name -> (function, description, JSON schema)

def _obj(props: dict, required: list[str] | None = None) -> dict:
    return {"type": "object", "properties": props, "required": required or [], "additionalProperties": False}


_S = {"type": "string"}
_COUNTRY = {"type": "string", "description": "ISO3 code (SEN), country name in French or English, or a capital/main city"}
_H = {"type": "integer", "enum": list(HORIZONS), "description": "Horizon in years"}

TOOLS: dict[str, tuple[Callable[..., dict], str, dict]] = {
    "data_status": (data_status, "Coverage and freshness of the verified data: as_of date, number of auctions, countries, sources, licence and the conventions of published values. Call first when unsure what the data covers.", _obj({})),
    "country_overview": (country_overview, "Summary for one country: zone, currency, central bank, verified auction counts and dates, latest published yields, whether an access procedure and listed intermediaries exist.", _obj({"country": _COUNTRY}, ["country"])),
    "search_auctions": (search_auctions, "Verified auction results (FACTs) with their official source PDF, most recent first. Filters are optional. The 'published_value' is a yield, a discount rate or a price depending on 'published_value_kind'.", _obj({
        "country": _COUNTRY, "date_from": {"type": "string", "description": "YYYY-MM-DD"}, "date_to": {"type": "string", "description": "YYYY-MM-DD"},
        "instrument": {"type": "string", "enum": ["treasury_bill", "treasury_bond"]}, "auction_type": {"type": "string", "enum": ["primary_auction", "buyback"]},
        "min_tenor_years": {"type": "number"}, "max_tenor_years": {"type": "number"},
        "limit": {"type": "integer", "minimum": 1, "maximum": MAX_ROWS}})),
    "yield_points": (yield_points, "Latest verified published yield per horizon (1, 3, 5, 7, 10 years) for one or all countries, with the auction, coupon and source PDF.", _obj({"country": _COUNTRY})),
    "simulate_investment": (simulate_investment, "Illustrative hold-to-maturity calculation for an amount, a country and a horizon, from the latest published yield: income, total received, gain, reinvested value and ±1 point resale sensitivity.", _obj({"amount": {"type": "number"}, "country": _COUNTRY, "horizon_years": _H}, ["amount", "country", "horizon_years"])),
    "compare_countries": (compare_countries, "Same calculation for 1 to 5 countries with the same amount and horizon, side by side (no ranking).", _obj({"countries": {"type": "array", "items": _S, "minItems": 1, "maxItems": 5}, "horizon_years": _H, "amount": {"type": "number"}}, ["countries", "horizon_years", "amount"])),
    "savings_goal": (savings_goal, "Monthly saving needed to reach a target from a starting capital at a constant annual rate (textbook calculation).", _obj({"capital": {"type": "number"}, "target": {"type": "number"}, "years": {"type": "integer", "minimum": 1, "maximum": 40}, "rate_percent": {"type": "number"}}, ["capital", "target", "years", "rate_percent"])),
    "access_procedure": (access_procedure, "Official procedure to subscribe to government securities in a country: who may subscribe, through whom, account, order submission, settlement, with source links and verbatim quotes.", _obj({"country": _COUNTRY}, ["country"])),
    "intermediaries": (intermediaries, "Institutions on official lists (primary dealers, SVT, etc.) by country, kind or name, with the list they appear on.", _obj({"country": _COUNTRY, "kind": _S, "name": _S, "limit": {"type": "integer", "minimum": 1, "maximum": MAX_ROWS}})),
    "bvmac_bonds": (bvmac_bonds, "Bonds listed on the BVMAC (CEMAC stock exchange) with their verified trade days (price in % of par, volume, official price list).", _obj({"query": {"type": "string", "description": "ISIN, name, code or issuer"}, "country": _COUNTRY})),
    "weekly_brief": (weekly_brief, "Auction results of the last 7 days, totals per currency and maturities in the next 14 days.", _obj({})),
    "quarterly_reports": (quarterly_reports, "Published quarterly WAEMU reports with their PDF links.", _obj({})),
}


def definitions() -> list[dict]:
    """Tool definitions for the Messages API, in a fixed order (keeps the prompt cache stable)."""
    return [{"name": n, "description": d, "input_schema": s} for n, (_, d, s) in TOOLS.items()]


def run(feed: Feed, name: str, args: dict | None) -> dict:
    """Run one tool. Unknown tools and bad arguments raise ToolError."""
    if name not in TOOLS:
        raise ToolError(f"Unknown tool '{name}'")
    fn, _, schema = TOOLS[name]
    args = dict(args or {})
    extra = set(args) - set(schema["properties"])
    if extra:
        raise ToolError(f"Unexpected arguments: {sorted(extra)}")
    missing = [k for k in schema["required"] if args.get(k) in (None, "")]
    if missing:
        raise ToolError(f"Missing arguments: {missing}")
    try:
        return fn(feed.get(), **args)
    except (TypeError, KeyError) as e:
        raise ToolError(f"Invalid arguments for {name}: {e}") from e
