"""Build the public Cartouche showcase site (static) from the platform's own API.

    python site/build.py --as-of 2026-10-03

Requires a seeded database (ABI_DATABASE_URL). Writes site/dist/: index.html (data embedded),
favicon.svg, netlify.toml and, when --veille is given, veille.json. Normally run by
app.watch.daily, which refreshes the data and the source watch first.
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

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

    return {"as_of": as_of, "summary": summary, "grid": grid, "opportunities": opps,
            "walls": walls, "sources": sources, "page_scope": page_scope, "africa": africa,
            "buyers": list(buyers.values()), "dealers": get("/accredited-dealers"), "i18n": load_i18n(list(buyers))}


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
        if [g[0] for g in t["glossary"]] != [g[0] for g in ref["glossary"]]:
            raise SystemExit(f"i18n/{lang}.json: glossary terms differ from fr")
        if lang != "fr":
            for k in buyer_keys:
                if k not in t["buyer_cards"]:
                    raise SystemExit(f"i18n/{lang}.json: buyer_cards lacks '{k}'")
    return tables


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--veille", type=Path, help="veille.json from app.watch.daily (optional)")
    args = parser.parse_args()

    payload = export(args.as_of)
    if args.veille and args.veille.exists():
        veille = json.loads(args.veille.read_text())
        # Embed the report only; the comparison state stays in the downloadable veille.json.
        payload["veille"] = {k: v for k, v in veille.items() if k != "state"}
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    html = (ROOT / "template.html").read_text().replace("__DATA__", data.replace("</", "<\\/"))
    DIST.mkdir(exist_ok=True)
    (DIST / "index.html").write_text(html)
    shutil.copy(ROOT.parent / "brand" / "favicon.svg", DIST / "favicon.svg")
    shutil.copy(ROOT / "netlify.toml", DIST / "netlify.toml")
    if args.veille and args.veille.exists() and args.veille.resolve() != (DIST / "veille.json").resolve():
        shutil.copy(args.veille, DIST / "veille.json")
    print(f"Built {DIST / 'index.html'} ({len(html) // 1024} KB)")


if __name__ == "__main__":
    main()
