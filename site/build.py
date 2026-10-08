"""Build the public Cartouche showcase site (static) from the platform's own API.

    python site/build.py --as-of 2026-10-03

Requires a seeded database (ABI_DATABASE_URL). Writes site/dist/: index.html (data embedded),
favicon.svg, netlify.toml, rapports/ (quarterly report previews, see site/report.py) and, when
--veille is given, veille.json. Normally run by
app.watch.daily, which refreshes the data and the source watch first.
"""

import argparse
import json
import os
import re
import shutil
import unicodedata
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from app.seed.africa import AFRICA  # noqa: E402

ROOT = Path(__file__).resolve().parent
LANGS = ("fr", "en", "pt", "es", "ar")
# Regional institutions: which member countries a source without a country speaks for.
REGIONAL = {"BCEAO": "WAEMU", "UMOA-Titres": "WAEMU", "BRVM": "WAEMU", "BEAC": "CEMAC", "BVMAC": "CEMAC"}
# Countries whose official sources are proposed and watched daily (app/seed/source_candidates.py).
PILOTS = {"CMR", "COG", "GAB", "CIV", "SEN", "KEN"}
DIST = ROOT / "dist"


def export(as_of: str) -> dict:
    client = TestClient(app)

    def get(path: str, **params):
        r = client.get(f"/api/v1{path}", params={"as_of": as_of, **params})
        r.raise_for_status()
        return r.json()

    summary = get("/dashboard/summary")
    grid = get("/market/heat-grid")
    opps = get("/opportunities", limit=500)
    walls = {r["country_iso3"]: get(f"/countries/{r['country_iso3']}/maturity-wall") for r in grid["rows"]}
    sources = [s for s in get("/sources") if not s["is_synthetic"]]
    countries = {c["iso3"]: c for c in get("/countries")}

    by_id = {c["country_id"]: c["iso3"] for c in countries.values()}
    members: dict[str, list[str]] = {}
    for a in AFRICA:
        members.setdefault(a.zone.value, []).append(a.iso3)
    every = [a.iso3 for a in AFRICA]
    page_scope: dict[str, list[str]] = {}
    for s in sources:
        if s["country_id"] is not None:
            s["scope"] = [by_id[s["country_id"]]]
        else:
            s["scope"] = members[REGIONAL[s["institution"]]] if s["institution"] in REGIONAL else every
        for c in s["candidates"]:
            page_scope[c["url"]] = s["scope"]

    for o in opps["items"]:
        ((o["evidence"].get("calculation") or {}).get("inputs") or {}).pop("peer_auction_ids", None)
    for s in sources:
        for key in ("last_checked_at", "last_error", "crawl_config"):
            s.pop(key, None)
    signals: dict[str, int] = {}
    for o in opps["items"]:
        signals[o["country_iso3"]] = signals.get(o["country_iso3"], 0) + 1

    africa = [
        {
            "iso3": a.iso3, "iso2": a.iso2, "name_en": a.name, "name_fr": a.name_fr, "currency": a.currency, "zone": a.zone.value,
            "central_bank": a.central_bank, "region": a.region, "tile": list(a.tile),
            "coverage": countries[a.iso3]["coverage_tier"], "signals": signals.get(a.iso3, 0),
            "pilot": a.iso3 in PILOTS,
        }
        for a in AFRICA
    ]
    # One buyer-access card per zone (CEMAC, WAEMU) or country (KEN), with its instruments.
    routes = get("/subscription-routes")
    buyers: dict[str, dict] = {}
    for r in routes:
        key = r["monetary_zone"] if r["monetary_zone"] in ("CEMAC", "WAEMU") else r["country_iso3"]
        card = buyers.setdefault(key, {
            "key": key, "countries": [], "instruments": [], "quotes": [],
            **{f: r[f] for f in ("investor_type", "eligibility", "primary_dealer", "account_requirement",
                                 "submission_method", "settlement_method", "fees", "taxes",
                                 "last_verified", "disclaimer")},
            "sources": [],
        })
        if r["country_iso3"] not in card["countries"]:
            card["countries"].append(r["country_iso3"])
        note = (r["instrument_type"], r["instrument_notes"])
        if note[1] not in [i[1] for i in card["instruments"]]:  # KEN bills and bonds share one note
            card["instruments"].append(list(note))
        for q in r["quotes"]:
            if q not in card["quotes"]:
                card["quotes"].append(q)
        if r["official_source_url"] not in card["sources"]:
            card["sources"].append(r["official_source_url"])

    return {"as_of": as_of, "data": data_mode(), "summary": summary, "grid": grid, "opportunities": opps,
            "walls": walls, "sources": sources, "page_scope": page_scope, "africa": africa,
            "buyers": list(buyers.values()), "dealers": get("/accredited-dealers"), "market": market(get, as_of),
            "i18n": load_i18n(list(buyers))}


def _num(v: str | None, scale: int = 1):
    """Exact decimal string -> compact JSON number (int when whole), divided by `scale`."""
    if v is None:
        return None
    d = (Decimal(v) / scale).normalize()
    return int(d) if d == d.to_integral_value() else float(d)


def market(get, as_of: str) -> dict:
    """Every real (non-synthetic) auction up to as_of, as compact rows for the market charts.

    Strings are stored once (countries, securities, URL suffixes, enum values) and rows point to them
    by index. Amounts are in millions of the security currency (exact: the source values are whole
    units). Nothing is derived here: the page computes sums and residual maturities from these rows.
    """
    items: list[dict] = []
    while True:
        page = get("/auctions", include_synthetic="false", date_to=as_of, order="asc", limit=500, offset=len(items))
        items += page["items"]
        if len(items) >= page["total"] or not page["items"]:
            break
    items = [a for a in items if not a["provenance"]["is_synthetic"]]
    countries: list[str] = sorted({a["security"]["country_iso3"] for a in items})
    instr = ["treasury_bill", "treasury_bond"]
    types: list[str] = []
    status: list[str] = []
    secs: dict[int, int] = {}
    sec_rows: list[list] = []
    urls: list[str] = sorted({a["provenance"]["source_url"] or "" for a in items})
    prefix = os.path.commonprefix(urls)
    prefix = prefix[: prefix.rfind("/") + 1]
    url_ix = {u: i for i, u in enumerate(urls)}
    rows = []
    for a in items:
        s, o = a["security"], a["official"]
        if s["security_id"] not in secs:
            secs[s["security_id"]] = len(sec_rows)
            it = s["instrument_type"]
            if it not in instr:
                instr.append(it)
            sec_rows.append([s["security_name"], instr.index(it), s["tenor_days"], s["maturity_date"]])
        if a["auction_type"] not in types:
            types.append(a["auction_type"])
        why = None
        if o["weighted_average_yield"] is None:
            reason = a["field_status"].get("weighted_average_yield", "not_available")
            if reason not in status:
                status.append(reason)
            why = status.index(reason)
        settle = None
        if a["settlement_date"]:
            settle = (date.fromisoformat(a["settlement_date"]) - date.fromisoformat(a["auction_date"])).days
        rows.append([
            a["auction_id"], a["auction_date"], countries.index(s["country_iso3"]), secs[s["security_id"]],
            types.index(a["auction_type"]), _num(o["amount_submitted"], 10**6), _num(o["amount_allocated"], 10**6),
            _num(o["weighted_average_yield"]), why, url_ix[a["provenance"]["source_url"] or ""], settle,
        ])
    return {
        "fields": ["auction_id", "auction_date", "country", "security", "auction_type", "amount_submitted_m",
                   "amount_allocated_m", "weighted_average_yield", "yield_status", "source_url", "settlement_offset_days"],
        "sec_fields": ["security_name", "instrument_type", "tenor_days", "maturity_date"],
        "amount_scale": 10**6, "countries": countries, "currency": sorted({a["security"]["currency"] for a in items}),
        "instr": instr, "types": types, "status": status, "url_prefix": prefix,
        "urls": [u[len(prefix):] for u in urls], "sec": sec_rows, "rows": rows,
        "conventions": sorted({a["official"]["yield_convention"] or "" for a in items}),
        "verification": sorted({a["provenance"]["verification_status"] for a in items}),
        "sources": sorted({a["provenance"]["source"]["institution"] for a in items if a["provenance"]["source"]}),
    }


def data_mode() -> dict:
    """What market data the snapshot holds: synthetic count, and the span of real verified data."""
    from sqlalchemy import func, select

    from app.db import SessionLocal
    from app.models import Auction, Country, Security

    with SessionLocal() as s:
        syn = s.scalar(select(func.count()).select_from(Auction).where(Auction.is_synthetic)) or 0
        real = s.execute(select(func.count(), func.min(Auction.auction_date), func.max(Auction.auction_date))
                         .where(Auction.is_synthetic.is_(False))).one()
        countries = sorted(s.scalars(select(Country.iso3).join(Security, Security.country_id == Country.country_id)
                                     .where(Security.is_synthetic.is_(False)).distinct()))
    return {"synthetic_auctions": syn, "real_auctions": real[0], "first": real[1] and real[1].isoformat(),
            "last": real[2] and real[2].isoformat(), "real_countries": countries}


def load_i18n(buyer_keys: list[str]) -> dict:
    """Interface strings per language. Fails the build if a language misses or adds a key."""
    tables = {lang: json.loads((ROOT / "i18n" / f"{lang}.json").read_text()) for lang in LANGS}
    ref = tables["fr"]
    for lang, t in tables.items():
        missing, extra = set(ref) - set(t), set(t) - set(ref)
        if missing or extra:
            raise SystemExit(f"i18n/{lang}.json: missing {sorted(missing)}, extra {sorted(extra)}")
        for key in ("glossary", "strategy_levers", "strategy_limits", "strategy_coop", "guide_steps", "ask_list"):
            if len(t[key]) != len(ref[key]):
                raise SystemExit(f"i18n/{lang}.json: '{key}' has {len(t[key])} items, fr has {len(ref[key])}")
        for key, val in t.items():  # same {placeholders} as fr (Arabic singular forms may omit {n})
            if isinstance(val, str) and isinstance(ref.get(key), str):
                a, b = set(re.findall(r"\{(\w+)\}", val)), set(re.findall(r"\{(\w+)\}", ref[key]))
                if not a <= b or (a != b and not key.endswith(".one")):
                    raise SystemExit(f"i18n/{lang}.json: '{key}' placeholders {sorted(a)} differ from fr {sorted(b)}")
        shape = lambda tiers: [(x["id"], [f[0] for f in x["features"]]) for x in tiers]  # noqa: E731
        if shape(t["sub_tiers"]) != shape(ref["sub_tiers"]):
            raise SystemExit(f"i18n/{lang}.json: sub_tiers ids, features or availability differ from fr")
        if [g[0] for g in t["glossary"]] != [g[0] for g in ref["glossary"]]:
            raise SystemExit(f"i18n/{lang}.json: glossary terms differ from fr")
        if lang != "fr":
            for k in buyer_keys:
                if k not in t["buyer_cards"]:
                    raise SystemExit(f"i18n/{lang}.json: buyer_cards lacks '{k}'")
    return tables


# Horizons offered by the simulators (years) and the residual-maturity window used for each.
HORIZONS = {1: (0.9, 1.1), 3: (2.0, 4.0), 5: (4.0, 6.0), 7: (6.0, 8.5), 10: (8.5, 15.0)}


def _source_label(url: str | None) -> str:
    """Institution that published the document, from its host; an unknown host is shown as is."""
    host = (urlparse(url or "").hostname or "").lower()
    for dom, name in (("umoatitres.org", "UMOA-Titres"), ("beac.int", "BEAC")):
        if host == dom or host.endswith("." + dom):
            return name
    return host or "?"


def _embed(obj) -> str:
    """JSON for an inline <script> block: no NaN/Infinity, and no "<" that could close or comment the block."""
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"), allow_nan=False).replace("<", "\\u003c")


def prerender(html: str, table: dict, real: bool = False, names: dict | None = None) -> str:
    """Write the French strings into the static HTML (data-i text, data-ih trusted markup, data-country
    names) so the pages read without JavaScript; the scripts then replace them per language."""
    from html import escape

    def text(key: str) -> str | None:
        if real and isinstance(table.get(key + ".real"), str):
            key += ".real"
        v = table.get(key)
        return v if isinstance(v, str) else None

    def fill(m: re.Match, trusted: bool) -> str:
        v = text(m.group(3))
        return m.group(0) if v is None else m.group(1) + (v if trusted else escape(v, quote=False)) + m.group(4)

    parts = re.split(r"(<script\b.*?</script>)", html, flags=re.S)  # never touch script bodies
    for i in range(0, len(parts), 2):
        parts[i] = _prerender_markup(parts[i], fill, names)
    return "".join(parts)


def _prerender_markup(html: str, fill, names: dict | None) -> str:
    from html import escape

    for attr, trusted in (("data-i", False), ("data-ih", True)):
        html = re.sub(rf'(<(\w+)\b[^<>]*\s{attr}="([^"]+)"[^<>]*>)(</\2>)', lambda m, t=trusted: fill(m, t), html)
    if names:
        html = re.sub(r'(<(\w+)\b[^<>]*\sdata-country="([A-Z]{3})"[^<>]*>)(</\2>)',
                      lambda m: m.group(1) + escape(names.get(m.group(3), m.group(3))) + m.group(4), html)
    return html


def write_i18n(tables: dict) -> str:
    """Every language as its own file (dist/i18n/<lang>.json); the platform embeds French only and
    fetches the others when chosen. Returns a short content version for cache busting."""
    import hashlib

    out = DIST / "i18n"
    out.mkdir(parents=True, exist_ok=True)
    blobs = {lang: json.dumps(t, ensure_ascii=False, separators=(",", ":"), allow_nan=False) for lang, t in tables.items()}
    for lang, b in blobs.items():
        (out / f"{lang}.json").write_text(b)
    return hashlib.sha256("".join(blobs[k] for k in sorted(blobs)).encode()).hexdigest()[:12]


def yield_points(as_of: date) -> dict:
    """For each country and horizon: the latest verified issuance auction of the last 12 months whose
    residual maturity falls in the horizon's window, with its published yield (FACT) and source.
    The simulators apply arithmetic to these published rates; nothing is estimated."""
    import report

    data = json.loads((ROOT.parent / "backend" / "app" / "seed" / "data" / "verified_market_data.json").read_text())
    secs = {s["isin"]: s for s in data["securities"]}
    lo = as_of.toordinal() - 365
    out: dict = {}
    for r in report.load_rows():
        if r["type"] in report.NON_ISSUANCE or r["yld"] is None or not r["alloc"] or r["residual_years"] is None:
            continue
        if not (lo < r["date"].toordinal() <= as_of.toordinal()):
            continue
        for h, (a, b) in HORIZONS.items():
            if a < r["residual_years"] <= b:
                cur = out.setdefault(r["country"], {}).get(str(h))
                if cur is None or (r["date"].isoformat(), r["alloc"]) > (cur["d"], Decimal(cur["_alloc"])):
                    sec = secs.get(r["isin"], {})
                    if r["instr"] != "treasury_bill" and sec.get("coupon_rate") is None:
                        continue  # a bond without its coupon cannot be priced: no point rather than a bill-like guess
                    out[r["country"]][str(h)] = {
                        "y": float(r["yld"]), "d": r["date"].isoformat(), "name": r["name"], "isin": r["isin"],
                        "instr": r["instr"], "res": round(r["residual_years"], 1), "url": r["url"],
                        "coupon": _num(sec.get("coupon_rate")), "cur": r["currency"],
                        "src": _source_label(r["url"]), "_alloc": str(r["alloc"])}
    out = {c: pts for c, pts in out.items() if pts}
    for pts in out.values():
        for v in pts.values():
            v.pop("_alloc", None)
    return out


def home_page(payload: dict) -> str:
    """Home page: key figures, entry points, newsletter per market (Netlify form) and account links.
    The market checkboxes are written into the HTML here so that Netlify detects every field."""
    from html import escape

    zones = {"WAEMU": "UEMOA", "CEMAC": "CEMAC"}
    by_zone: dict[str, list] = {}
    for a in payload["africa"]:
        if a["iso3"] in payload["data"]["real_countries"] and a["zone"] in zones:
            by_zone.setdefault(a["zone"], []).append(a)
    blocks = []
    for z, label in zones.items():
        boxes = "".join(f'<label class="chk"><input type="checkbox" name="pays_{a["iso3"]}" value="oui" data-market data-zone="{z}">'
                        f'<span data-country="{a["iso3"]}"></span></label>' for a in sorted(by_zone.get(z, []), key=lambda a: unicodedata.normalize("NFD", a["name_fr"]).encode("ascii", "ignore").lower()))
        blocks.append(f'<p style="margin:10px 0 6px"><label class="chk zone"><input type="checkbox" name="marche_{escape(label)}" value="oui" data-market data-zone-box="{z}">'
                      f'<span data-i="home.nl.zone.{z}"></span></label></p><div class="grid">{boxes}</div>')
    blocks.append('<p style="margin:12px 0 0"><label class="chk"><input type="checkbox" name="marche_autres_pays" value="oui" data-market>'
                  '<span data-i="home.nl.zone.other"></span></label></p>')
    used = {a["iso3"] for zs in by_zone.values() for a in zs}
    home = {
        "as_of": payload["as_of"], "auctions": payload["data"]["real_auctions"], "last": payload["data"]["last"],
        "countries_with_data": len(payload["data"]["real_countries"]), "bonds": len(payload["bvmac"]["bonds"]),
        "countries": {a["iso3"]: {"iso2": a["iso2"], "name_fr": a["name_fr"], "name_en": a["name_en"]} for a in payload["africa"] if a["iso3"] in used | set(payload["yield_points"])},
        "i18n": {lang: {k: v for k, v in table.items() if k.startswith("home.") or k.startswith("sim2.")} for lang, table in payload["i18n"].items()},
        "points": payload["yield_points"],
        "sim_countries": sorted(payload["yield_points"]),
    }
    data = _embed(home)
    page = (ROOT / "home.html").read_text().replace("__MARKETS__", "\n".join(blocks))
    page = prerender(page, payload["i18n"]["fr"], names={k: v["name_fr"] for k, v in home["countries"].items()})
    return page.replace("__HOME__", data)


def bvmac_quotes(as_of: date | None = None) -> dict:
    """BVMAC listed bonds and their verified trade observations (FACT), from the versioned verified
    data. Only days with a trade exist: a price shown without a trade (NC) is never an observation."""
    data = json.loads((ROOT.parent / "backend" / "app" / "seed" / "data" / "verified_market_data.json").read_text())
    issuers = {i["name"]: i for i in data.get("issuers", [])}
    bonds = [s for s in data["securities"] if "BVMAC" in (s.get("listing_status") or "")]
    trades: dict[str, list] = {}
    for o in data.get("market_observations", []):
        # A trade without a published price or volume is skipped rather than shown as 0; nothing after as_of.
        if (o["kind"] == "secondary_market" and o["verification_status"] == "verified" and not o["is_synthetic"]
                and o.get("price") is not None and o.get("volume") is not None
                and (as_of is None or o["observation_date"] <= as_of.isoformat())):
            trades.setdefault(o["isin"], []).append([o["observation_date"], _num(o["price"]), _num(o["volume"]), o["source_url"]])
    rows = []
    for b in bonds:
        t = sorted(trades.get(b["isin"], []), reverse=True)
        rows.append({"isin": b["isin"], "name": b["security_name"], "code": b.get("local_code"), "country": b["country"],
                     "issuer": b["issuer"], "issuer_type": issuers.get(b["issuer"], {}).get("issuer_type"),
                     "coupon": _num(b["coupon_rate"]), "trades": t})
    rows.sort(key=lambda r: (r["trades"][0][0] if r["trades"] else "", r["name"]), reverse=True)
    first = min((o[0] for r in rows for o in r["trades"]), default=None)
    return {"bonds": rows, "first": first, "currency": "XAF"}


def auth_config() -> dict | None:
    """Free accounts (Supabase Auth): on only when the project URL and its public key are in the
    environment. The key is the publishable/anon key, meant to be public; never the service key."""
    url = (os.environ.get("SUPABASE_URL") or "").rstrip("/")
    key = os.environ.get("SUPABASE_PUBLISHABLE_KEY") or os.environ.get("SUPABASE_ANON_KEY") or ""
    if not url or not key:
        return None
    u = urlparse(url)
    if u.scheme != "https" or not u.hostname or u.path or u.params or u.query or u.fragment or u.username \
            or any(c in url for c in " \"'<>;,\\"):
        raise SystemExit("SUPABASE_URL must be exactly https://<host>")
    if key.startswith("sb_secret_") or _jwt_role(key) not in (None, "anon"):
        raise SystemExit("The key must be the public (publishable/anon) key, never the service key")
    return {"url": url, "key": key}


def _jwt_role(key: str) -> str | None:
    """Role claim of a legacy Supabase JWT key (anon or service_role); None for non-JWT keys."""
    import base64

    parts = key.split(".")
    if not key.startswith("eyJ") or len(parts) != 3:
        return None
    try:
        claims = json.loads(base64.urlsafe_b64decode(parts[1] + "=" * (-len(parts[1]) % 4)))
    except ValueError:
        return "unreadable"
    return claims.get("role", "missing") if isinstance(claims, dict) else "unreadable"


def _replace_once(text: str, old: str, new: str) -> str:
    """Fail the build rather than silently ship a CSP or config without the change."""
    if text.count(old) != 1:
        raise SystemExit(f"netlify.toml: expected exactly one {old!r}")
    return text.replace(old, new, 1)


def inline_script_hashes() -> list[str]:
    """CSP hashes of every inline executable <script> in the built pages, so the policy can drop
    'unsafe-inline' for scripts (JSON data blocks are not executed and need none)."""
    import base64
    import hashlib

    out = set()
    for page in DIST.rglob("*.html"):
        for attrs, body in re.findall(r"<script\b([^>]*)>(.*?)</script>", page.read_text(), re.S):
            if "src=" in attrs or "application/json" in attrs:
                continue
            out.add("'sha256-" + base64.b64encode(hashlib.sha256(body.encode()).digest()).decode() + "'")
    return sorted(out)


def write_netlify(auth: dict | None) -> None:
    """netlify.toml for the deployed folder; with accounts on, the CSP lets the page reach Supabase
    and the download gate (site/edge/gate.js) is added as an edge function."""
    toml = (ROOT / "netlify.toml").read_text()
    toml = _replace_once(toml, "script-src 'self' 'unsafe-inline';", "script-src 'self' " + " ".join(inline_script_hashes()) + ";")
    edge = DIST / "netlify"
    if edge.exists():
        shutil.rmtree(edge)
    if auth:
        toml = _replace_once(toml, "default-src 'self';", f"default-src 'self'; connect-src 'self' {auth['url']};")
        (edge / "edge-functions").mkdir(parents=True)
        code = (ROOT / "edge" / "gate.js").read_text().replace("__CONFIG__", json.dumps(auth))
        (edge / "edge-functions" / "gate.js").write_text(code)
        toml = _replace_once(toml, '  publish = "."', '  publish = "."\n  edge_functions = "netlify/edge-functions"')
    (DIST / "netlify.toml").write_text(toml)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--veille", type=Path, help="veille.json from app.watch.daily (optional)")
    parser.add_argument("--pdf", action="store_true", help="also print the quarterly reports to PDF (needs Chromium)")
    args = parser.parse_args()

    payload = export(args.as_of)
    # Quarterly reports: public previews into dist/rapports, complete editions into site/reports (never deployed).
    import report
    purchase = os.environ.get("CARTOUCHE_REPORT_PURCHASE_URL") or None
    auth_scope = json.loads((ROOT.parent / "backend" / "app" / "ingest" / "data" / "authorisations.json").read_text())
    if purchase and not auth_scope.get("commercial_use"):
        # The source institutions authorised free publication only: no purchase button.
        print("CARTOUCHE_REPORT_PURCHASE_URL ignored: authorisations cover free publication only")
        purchase = None
    payload["reports"] = report.build(date.fromisoformat(args.as_of), DIST, pdf=args.pdf, purchase_url=purchase)
    payload["reports_purchase_url"] = purchase
    # Daily auction brief (section "Brief" + e-mail-ready pages) and the data offer (dictionary, sample).
    import brief
    import dataset
    payload["brief"] = brief.write(date.fromisoformat(args.as_of), DIST)
    payload["auth"] = auth_config()
    if not payload["auth"]:
        print("Accounts off (no SUPABASE_URL / public key): reports and CSV files are downloadable without an account")
    offer = dataset.write(date.fromisoformat(args.as_of), DIST, gated=bool(payload["auth"]))
    payload["data_offer"] = {k: offer[k] for k in ("auctions", "securities", "documents", "countries")}
    payload["bvmac"] = bvmac_quotes(date.fromisoformat(args.as_of))
    payload["yield_points"] = yield_points(date.fromisoformat(args.as_of))
    if args.veille and args.veille.exists():
        veille = json.loads(args.veille.read_text())
        # Embed the report only; the comparison state stays in the downloadable veille.json.
        payload["veille"] = {k: v for k, v in veille.items() if k != "state"}
    DIST.mkdir(exist_ok=True)
    home = home_page(payload)  # needs every language (small subset); written below
    tables = payload["i18n"]
    payload["i18n_v"] = write_i18n(tables)
    payload["i18n"] = {"fr": tables["fr"]}
    real = (payload.get("data") or {}).get("synthetic_auctions") == 0
    html = prerender((ROOT / "template.html").read_text(), tables["fr"], real=real)
    html = html.replace("__DATA__", _embed(payload))
    DIST.mkdir(exist_ok=True)
    # The platform (all sections) lives at /plateforme.html; / is the home page (site/home.html).
    (DIST / "plateforme.html").write_text(html)
    (DIST / "index.html").write_text(home)
    shutil.copy(ROOT.parent / "brand" / "favicon.svg", DIST / "favicon.svg")
    write_netlify(payload["auth"])
    shutil.copy(ROOT / "simcalc.js", DIST / "simcalc.js")  # simulator arithmetic shared by both pages
    shutil.copy(ROOT / "merci.html", DIST / "merci.html")  # waiting-list form fallback page (no JavaScript)
    if args.veille and args.veille.exists() and args.veille.resolve() != (DIST / "veille.json").resolve():
        shutil.copy(args.veille, DIST / "veille.json")
    print(f"Built {DIST / 'plateforme.html'} ({len(html) // 1024} KB) and the home page {DIST / 'index.html'}")


if __name__ == "__main__":
    main()
