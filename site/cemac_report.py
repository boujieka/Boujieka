"""CEMAC state of play ("État des lieux CEMAC"): every verified BEAC auction and every BVMAC listed
bond in ABM's data, with the coverage gaps stated, in French and English (HTML + PDF).

    python site/cemac_report.py --as-of 2026-10-11 [--pdf]

Why not a quarterly report like the WAEMU one: the verified BEAC archive is too thin per quarter
(0 to 9 auctions), so a quarterly comparison would mislead. This edition lists what is verified.
Each value keeps the measure the BEAC publishes: a weighted average DISCOUNT RATE (précompté) for
bills (BTA) and a weighted average PRICE in % of par for bonds (OTA). Neither is a yield, and no
yield is computed here. Amounts are XAF only. Everything else is a count or a sum (CALCULATION).
Free publication only (backend/app/ingest/data/authorisations.json).
"""

import argparse
import json
import shutil
from collections import defaultdict
from datetime import date
from decimal import Decimal
from html import escape
from pathlib import Path

import report
from report import BILLION, CSS, NAMES, fmt_date, fmt_num

ZONE = "CEMAC"
CEMAC = sorted((iso for iso, z in report.ZONES.items() if z == ZONE), key=lambda c: report._sortkey(NAMES[c]["fr"]))
ROWS_PER_PAGE = 20

T = {
    "fr": {
        "title": "État des lieux", "subtitle": "Titres publics de la CEMAC", "asof": "Données vérifiées au {d}",
        "edition": "Édition gratuite", "contents": "Ce que contiennent nos données", "country": "Pays",
        "auctions": "Adjudications vérifiées", "first": "Première", "last": "Dernière", "bills": "BTA", "bonds": "OTA",
        "alloc": "Montant retenu (Md FCFA XAF)", "bvmac": "Obligations cotées BVMAC", "trades": "Jours de transaction",
        "none": "aucune", "nd": "n.d.",
        "coverage": "Couverture : ces adjudications sont celles dont l'avis de résultats publié par la BEAC a pu être lu et vérifié (lecture optique double, contrôles stricts ; les valeurs ambiguës sont retenues, jamais devinées). Ce n'est pas l'historique complet du marché : les totaux sont des minimums et ne permettent pas de comparaison d'un trimestre à l'autre.",
        "bta": "Bons du Trésor (BTA) : taux moyen pondéré précompté", "ota": "Obligations du Trésor (OTA) : prix moyen pondéré",
        "bta_note": "Taux tel que publié par la BEAC : un taux précompté (d'escompte), qui n'est pas un rendement et ne se compare pas directement aux rendements de l'UMOA.",
        "ota_note": "Prix moyen pondéré en % du nominal, tel que publié par la BEAC. Ce n'est pas un rendement ; aucun rendement n'est calculé ici.",
        "date": "Date", "security": "Titre", "tenor": "Durée", "days": "{n} j", "years": "{n} an(s)",
        "rate": "Taux précompté", "price": "Prix (% du nominal)", "src": "Source",
        "secondary": "Marché secondaire : cote officielle de la BVMAC",
        "secondary_note": "Seuls les jours avec une transaction sont des observations ; un cours affiché sans transaction n'est pas repris. {n} obligation(s) cotée(s) sans transaction dans nos données.",
        "issuer": "Émetteur", "coupon": "Coupon", "last_trade": "Dernière transaction", "last_price": "Dernier cours (% du nominal)",
        "volume": "Volume", "method": "Méthode et limites",
        "method_list": ["Sources : avis de résultats des émissions de titres publics de la BEAC ; bulletins officiels de la cote de la BVMAC.",
                        "Nature : chaque valeur citée est un FAIT publié ; les nombres et sommes sont des CALCULS sur ces faits.",
                        "Mesures : les BTA sont publiés avec un taux précompté, les OTA avec un prix moyen pondéré. Nous ne convertissons ni l'un ni l'autre en rendement.",
                        "Montants en francs CFA de la CEMAC (XAF). Ils ne sont jamais additionnés à des montants de l'UMOA (XOF).",
                        "Une adjudication dont l'avis n'a pas pu être lu ou vérifié manque à ce document : son absence ne signifie pas qu'elle n'a pas eu lieu."],
        "sources_h": "Documents sources", "legal": "Publication indépendante de Africa Bonds Monitor, reprise avec l'autorisation des institutions sources pour une publication gratuite (revente non autorisée). Elle n'émane ni de la BEAC, ni de la BVMAC, ni d'aucun État, et n'est approuvée par aucun d'eux. Information uniquement : ni conseil en investissement, ni recommandation.",
        "page": "Page", "cont": "(suite)",
    },
    "en": {
        "title": "State of play", "subtitle": "CEMAC government securities", "asof": "Verified data as of {d}",
        "edition": "Free edition", "contents": "What our data contains", "country": "Country",
        "auctions": "Verified auctions", "first": "First", "last": "Last", "bills": "BTA", "bonds": "OTA",
        "alloc": "Amount allotted (XAF bn)", "bvmac": "BVMAC listed bonds", "trades": "Trade days",
        "none": "none", "nd": "n/a",
        "coverage": "Coverage: these are the auctions whose results notice published by the BEAC could be read and verified (double optical reading, strict checks; ambiguous values are held, never guessed). This is not the full market history: totals are lower bounds and do not support quarter-on-quarter comparison.",
        "bta": "Treasury bills (BTA): weighted average discount rate", "ota": "Treasury bonds (OTA): weighted average price",
        "bta_note": "Rate as published by the BEAC: a discount rate (précompté), which is not a yield and is not directly comparable with WAEMU yields.",
        "ota_note": "Weighted average price in % of par, as published by the BEAC. It is not a yield; no yield is computed here.",
        "date": "Date", "security": "Security", "tenor": "Tenor", "days": "{n} d", "years": "{n} yr",
        "rate": "Discount rate", "price": "Price (% of par)", "src": "Source",
        "secondary": "Secondary market: BVMAC official price list",
        "secondary_note": "Only days with a trade are observations; a price shown without a trade is not used. {n} listed bond(s) with no trade in our data.",
        "issuer": "Issuer", "coupon": "Coupon", "last_trade": "Last trade", "last_price": "Last price (% of par)",
        "volume": "Volume", "method": "Method and limits",
        "method_list": ["Sources: BEAC results notices for government securities issues; BVMAC official price lists.",
                        "Nature: every value quoted is a published FACT; counts and sums are CALCULATIONS on those facts.",
                        "Measures: BTA are published with a discount rate, OTA with a weighted average price. We convert neither into a yield.",
                        "Amounts in CEMAC CFA francs (XAF). They are never added to WAEMU (XOF) amounts.",
                        "An auction whose notice could not be read or verified is missing from this document: its absence does not mean it did not take place."],
        "sources_h": "Source documents", "legal": "Independent publication by Africa Bonds Monitor, reproduced with the source institutions' authorisation for free publication (resale not authorised). It is not issued or endorsed by the BEAC, the BVMAC or any State. Information only: neither investment advice nor a recommendation.",
        "page": "Page", "cont": "(continued)",
    },
}


def load(as_of: date) -> dict:
    data = json.loads(report.DATA.read_text())
    rows = [r for r in report.load_rows(zone=ZONE) if r["date"] <= as_of and r["type"] not in report.NON_ISSUANCE]
    secs = {s["isin"]: s for s in data["securities"]}
    for r in rows:
        r["tenor_days"] = secs[r["isin"]].get("tenor_days")
    trades = defaultdict(list)
    for o in data.get("market_observations", []):
        if (o["kind"] == "secondary_market" and o["verification_status"] == "verified" and not o["is_synthetic"]
                and o.get("price") is not None and o.get("volume") is not None and o["observation_date"] <= as_of.isoformat()):
            trades[o["isin"]].append(o)
    bonds = [s for s in data["securities"] if "BVMAC" in (s.get("listing_status") or "")]
    return {"rows": sorted(rows, key=lambda r: (r["date"], r["country"], r["isin"]), reverse=True), "bonds": bonds, "trades": trades}


def by_country(d: dict) -> list[dict]:
    out = []
    for c in CEMAC:
        rs = [r for r in d["rows"] if r["country"] == c]
        bonds = [b for b in d["bonds"] if b["country"] == c]
        out.append({"c": c, "n": len(rs), "first": min((r["date"] for r in rs), default=None), "last": max((r["date"] for r in rs), default=None),
                    "bills": sum(1 for r in rs if r["instr"] == "treasury_bill"), "bonds": sum(1 for r in rs if r["instr"] != "treasury_bill"),
                    "alloc": sum((r["alloc"] for r in rs if r["alloc"] is not None), Decimal(0)) if rs else None,
                    "bvmac": len(bonds), "trade_days": sum(len(d["trades"].get(b["isin"], [])) for b in bonds)})
    return out


def _tenor(days, t) -> str:
    if days is None:
        return t["nd"]
    return t["days"].format(n=days) if days < 360 else t["years"].format(n=round(days / 365))


def _value(v, lang, t) -> str:
    return t["nd"] if v is None else fmt_num(v, lang, 2)


def _page(inner: str, n: int, t: dict, cls: str = "page") -> str:
    return f'<section class="{cls}">{inner}<div class="foot"><span>Africa Bonds Monitor · {escape(t["subtitle"])}</span><span>{t["page"]} {n}</span></div></section>'


def _chunks(items: list, size: int) -> list[list]:
    return [items[i:i + size] for i in range(0, len(items), size)] or [[]]


def render(d: dict, as_of: date, lang: str, em: dict, embed: bool) -> str:
    t = T[lang]
    pages, n = [], 1
    flags = "".join(f"<figure>{report.img(c, 'flag', 'f', embed, em, lang)}{escape(NAMES[c][lang])}</figure>" for c in CEMAC)
    pages.append(f'<section class="page cover"><div class="brand">Africa Bonds Monitor</div><h1>{escape(t["title"])}</h1>'
                 f'<div class="q">{escape(t["subtitle"])}</div><div>{escape(t["asof"].format(d=fmt_date(as_of, lang)))}</div>'
                 f'<p><span class="edition">{escape(t["edition"])}</span></p><div class="flags">{flags}</div>'
                 f'<p class="legal">{escape(t["legal"])}</p></section>')
    nd = t["nd"]
    rows_c = "".join(
        f'<tr><td>{report.img(r["c"], "flag", "mini", embed, em, lang)}{escape(NAMES[r["c"]][lang])}</td><td class="r num">{r["n"] or t["none"]}</td>'
        f'<td class="num">{fmt_date(r["first"], lang) if r["first"] else nd}</td><td class="num">{fmt_date(r["last"], lang) if r["last"] else nd}</td>'
        f'<td class="r num">{r["bills"]}</td><td class="r num">{r["bonds"]}</td>'
        f'<td class="r num">{nd if r["alloc"] is None else fmt_num(r["alloc"] / BILLION, lang)}</td>'
        f'<td class="r num">{r["bvmac"]}</td><td class="r num">{r["trade_days"]}</td></tr>' for r in by_country(d))
    pages.append(_page(f'<h2>{escape(t["contents"])}</h2><table><tr><th>{t["country"]}</th><th class="r">{t["auctions"]}</th><th>{t["first"]}</th><th>{t["last"]}</th>'
                       f'<th class="r">{t["bills"]}</th><th class="r">{t["bonds"]}</th><th class="r">{escape(t["alloc"])}</th><th class="r">{escape(t["bvmac"])}</th>'
                       f'<th class="r">{escape(t["trades"])}</th></tr>{rows_c}</table><div class="box small">{escape(t["coverage"])}</div>', n, t))
    n += 1
    for key, instr, col in (("bta", "treasury_bill", "rate"), ("ota", "treasury_bond", "price")):
        rs = [r for r in d["rows"] if (r["instr"] == "treasury_bill") == (instr == "treasury_bill")]
        for i, chunk in enumerate(_chunks(rs, ROWS_PER_PAGE)):
            body = "".join(
                f'<tr><td class="num">{fmt_date(r["date"], lang)}</td><td>{escape(NAMES[r["country"]][lang])}</td><td class="small">{escape(r["name"])}</td>'
                f'<td class="num">{_tenor(r["tenor_days"], t)}</td><td class="r num">{nd if r["alloc"] is None else fmt_num(r["alloc"] / BILLION, lang)}</td>'
                f'<td class="r num">{_value(r["yld"], lang, t)}</td><td class="small"><a href="{escape(r["url"] or "")}">PDF</a></td></tr>' for r in chunk)
            head = f'<h2>{escape(t[key])}{" " + t["cont"] if i else ""}</h2>' + ("" if i else f'<p class="small muted">{escape(t[key + "_note"])}</p>')
            pages.append(_page(f'{head}<table><tr><th>{t["date"]}</th><th>{t["country"]}</th><th>{t["security"]}</th><th>{t["tenor"]}</th>'
                               f'<th class="r">{escape(t["alloc"])}</th><th class="r">{t[col]}</th><th>{t["src"]}</th></tr>{body}</table>', n, t))
            n += 1
    traded = sorted((b for b in d["bonds"] if d["trades"].get(b["isin"])), key=lambda b: max(o["observation_date"] for o in d["trades"][b["isin"]]), reverse=True)
    quiet = len(d["bonds"]) - len(traded)
    for i, chunk in enumerate(_chunks(traded, ROWS_PER_PAGE)):
        body = ""
        for b in chunk:
            last = max(d["trades"][b["isin"]], key=lambda o: o["observation_date"])
            body += (f'<tr><td class="small">{escape(b["security_name"])}</td><td class="small">{escape(b["issuer"])}</td>'
                     f'<td class="r num">{nd if b.get("coupon_rate") is None else fmt_num(Decimal(str(b["coupon_rate"])), lang, 2)}</td>'
                     f'<td class="num">{fmt_date(date.fromisoformat(last["observation_date"]), lang)}</td><td class="r num">{fmt_num(Decimal(str(last["price"])), lang, 2)}</td>'
                     f'<td class="r num">{fmt_num(Decimal(str(last["volume"])), lang, 0)}</td><td class="r num">{len(d["trades"][b["isin"]])}</td>'
                     f'<td class="small"><a href="{escape(last["source_url"] or "")}">PDF</a></td></tr>')
        head = f'<h2>{escape(t["secondary"])}{" " + t["cont"] if i else ""}</h2>' + ("" if i else f'<p class="small muted">{escape(t["secondary_note"].format(n=quiet))}</p>')
        pages.append(_page(f'{head}<table><tr><th>{t["security"]}</th><th>{t["issuer"]}</th><th class="r">{t["coupon"]}</th><th>{escape(t["last_trade"])}</th>'
                           f'<th class="r">{escape(t["last_price"])}</th><th class="r">{t["volume"]}</th><th class="r">{escape(t["trades"])}</th><th>{t["src"]}</th></tr>{body}</table>', n, t))
        n += 1
    docs = sorted({r["url"] for r in d["rows"] if r["url"]} | {o["source_url"] for os in d["trades"].values() for o in os if o.get("source_url")})
    method = "".join(f"<li>{escape(x)}</li>" for x in t["method_list"])
    pages.append(_page(f'<h2>{escape(t["method"])}</h2><ul class="tight">{method}</ul><h3>{escape(t["sources_h"])}</h3>'
                       f'<div class="docs">{"".join(f"<div><a href={chr(34)}{escape(u)}{chr(34)}>{escape(u)}</a></div>" for u in docs)}</div>'
                       f'<p class="small muted">{escape(t["legal"])}</p>', n, t))
    title = f"Africa Bonds Monitor · {t['title']} · {t['subtitle']}"
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{escape(title)}</title><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Marcellus&family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Mono:wght@400;600&display=swap">'
            f"<style>{CSS}</style></head><body>{''.join(pages)}</body></html>")


def write(as_of: date, dist: Path, pdf: bool = False) -> dict:
    """dist/rapports/cemac/etat-des-lieux-{fr,en}.html (+ .pdf). Call after report.build (it resets dist/rapports)."""
    d = load(as_of)
    em = report.emblems()
    out = dist / "rapports" / "cemac"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    entry = {"as_of": as_of.isoformat(), "auctions": len(d["rows"]), "bonds": len(d["bonds"]),
             "trade_days": sum(len(v) for v in d["trades"].values()), "html": {}, "pdf": {}}
    for lang in T:
        html = out / f"africa-bonds-monitor-cemac-etat-des-lieux-{lang}.html"
        html.write_text(render(d, as_of, lang, em, embed=True))
        entry["html"][lang] = f"rapports/cemac/{html.name}"
        if pdf and report.to_pdf(html, html.with_suffix(".pdf")):
            entry["pdf"][lang] = f"rapports/cemac/{html.with_suffix('.pdf').name}"
    return entry


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--as-of", required=True, type=date.fromisoformat)
    p.add_argument("--dist", type=Path, default=report.ROOT / "dist")
    p.add_argument("--pdf", action="store_true")
    a = p.parse_args()
    print(json.dumps(write(a.as_of, a.dist, a.pdf), indent=1))


if __name__ == "__main__":
    main()
