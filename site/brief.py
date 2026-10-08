"""Daily auction brief ("Brief des adjudications"): a short, factual digest of the verified data.

    python site/brief.py --as-of 2026-10-04          # prints the brief as JSON

Built from backend/app/seed/data/verified_market_data.json only (FACT rows from UMOA-Titres):
  * results of the last 7 days (auction date in [as_of - 6, as_of]), issuance and buybacks;
  * totals for those 7 days next to the 7 days before (CALCULATION);
  * securities in our data that mature in the next 14 days.
No opinion, ranking or recommendation. site/build.py embeds it in the site (section "Brief") and
writes an e-mail-ready page per language to dist/brief/.
"""

import argparse
import json
from datetime import date, timedelta
from decimal import Decimal
from html import escape
from pathlib import Path

import report  # same data loader, formats and names as the quarterly report

WINDOW = 7
MATURITY_DAYS = 14


def build(as_of: date) -> dict:
    rows = report.load_rows()
    data = json.loads(report.DATA.read_text())
    start = as_of - timedelta(days=WINDOW - 1)
    prev_start = start - timedelta(days=WINDOW)

    def total(lo, hi):
        """Issuance totals per currency: XOF (WAEMU) and XAF (CEMAC) are never added together."""
        out = {}
        for r in rows:
            if lo <= r["date"] <= hi and r["type"] not in report.NON_ISSUANCE:
                t = out.setdefault(r["currency"], {"n": 0, "allotted": Decimal(0)})
                t["n"] += 1
                t["allotted"] += r["alloc"] or 0
        return {c: {"n": v["n"], "allotted": str(v["allotted"])} for c, v in sorted(out.items())}

    recent = sorted((r for r in rows if start <= r["date"] <= as_of),
                    key=lambda r: (r["date"], r["country"], r["name"]), reverse=True)
    secs = {s["isin"]: s for s in data["securities"]}
    maturing = sorted(
        ({"isin": s["isin"], "name": s["security_name"], "country": s["country"], "maturity": s["maturity_date"],
          "instrument": s["instrument_type"]}
         for s in secs.values() if s["maturity_date"]
         and as_of < date.fromisoformat(s["maturity_date"]) <= as_of + timedelta(days=MATURITY_DAYS)),
        key=lambda m: (m["maturity"], m["country"], m["name"]))
    last = max((r["date"] for r in rows), default=None)
    return {
        "as_of": as_of.isoformat(), "from": start.isoformat(), "window_days": WINDOW, "maturity_days": MATURITY_DAYS,
        "last_result": last.isoformat() if last else None,
        "results": [{"date": r["date"].isoformat(), "country": r["country"], "name": r["name"], "type": r["type"],
                     "instrument": r["instr"], "currency": r["currency"], "allotted": None if r["alloc"] is None else str(r["alloc"]),
                     "submitted": None if r["sub"] is None else str(r["sub"]),
                     "yield": None if r["yld"] is None else str(r["yld"]), "url": r["url"]} for r in recent],
        "totals": {"current": total(start, as_of), "previous": total(prev_start, start - timedelta(days=1))},
        "maturing": maturing,
    }


T = {
    "fr": {"title": "Brief des adjudications", "sub": "Titres publics UEMOA et CEMAC · données vérifiées",
           "period": "Résultats du {a} au {b}", "results": "Résultats publiés", "none": "Aucun résultat sur la période.",
           "totals": "Émissions sur 7 jours : {n} adjudications, {v} (7 jours précédents : {pn}, {pv}).",
           "maturing": "Échéances des {d} prochains jours (titres présents dans nos données)", "nomat": "Aucune.",
           "issue": "Émission", "buyback": "Rachat", "alloc": "Retenu", "sub": "Soumis", "yld": "Rendement",
           "country": "Pays", "security": "Titre", "date": "Date", "legal": "Faits publiés par UMOA-Titres (UEMOA) et la BEAC (CEMAC), vérifiés par Africa Bonds Monitor ; publication autorisée. Information uniquement, ni conseil ni recommandation.",
           "site": "Voir la plateforme"},
    "en": {"title": "Auction brief", "sub": "WAEMU and CEMAC government securities · verified data",
           "period": "Results from {a} to {b}", "results": "Published results", "none": "No result over the period.",
           "totals": "Issuance over 7 days: {n} auctions, {v} (previous 7 days: {pn}, {pv}).",
           "maturing": "Maturities in the next {d} days (securities in our data)", "nomat": "None.",
           "issue": "Issue", "buyback": "Buyback", "alloc": "Allotted", "sub": "Bid", "yld": "Yield",
           "country": "Country", "security": "Security", "date": "Date", "legal": "Facts published by UMOA-Titres (WAEMU) and the BEAC (CEMAC), verified by Africa Bonds Monitor; publication authorised. Information only, neither advice nor recommendation.",
           "site": "Open the platform"},
}


def email_html(b: dict, lang: str, site_url: str = "https://cartouche-africa.netlify.app/") -> str:
    """Self-contained page with inline styles, usable as the body of an e-mail."""
    t = T[lang]
    d = lambda s: report.fmt_date(date.fromisoformat(s), lang)  # noqa: E731
    def bn(v, cur="XOF"):
        if v is None:
            return report.T[lang]["nd"]
        x = report.fmt_num(Decimal(v) / report.BILLION, lang)
        return f"{x} Md {cur}" if lang == "fr" else f"{cur} {x} bn"
    cur, prev = b["totals"]["current"], b["totals"]["previous"]
    empty = {"n": 0, "allotted": "0"}
    totals = " ".join(t["totals"].format(n=cur.get(c, empty)["n"], v=bn(cur.get(c, empty)["allotted"], c),
                                         pn=prev.get(c, empty)["n"], pv=bn(prev.get(c, empty)["allotted"], c))
                      for c in sorted(set(cur) | set(prev)))
    td = 'style="padding:6px 8px;border-bottom:1px solid #ddd2bb;font-size:13px"'
    tdr = 'style="padding:6px 8px;border-bottom:1px solid #ddd2bb;font-size:13px;text-align:right;font-family:Menlo,monospace"'
    rows = "".join(
        f'<tr><td {td}>{escape(d(r["date"]))}</td><td {td}>{escape(report.NAMES[r["country"]][lang])}</td>'
        f'<td {td}><a href="{escape(r["url"])}" style="color:#13306b">{escape(r["name"])}</a> · {escape(t["buyback"] if r["type"] in report.NON_ISSUANCE else t["issue"])}</td>'
        f'<td {tdr}>{escape(bn(r["allotted"], r.get("currency", "XOF")))}</td><td {tdr}>{escape(report.fmt_pct(None if r["yield"] is None else Decimal(r["yield"]), lang))}</td></tr>'
        for r in b["results"])
    mats = "".join(f'<li>{escape(d(m["maturity"]))} · {escape(report.NAMES[m["country"]][lang])} · {escape(m["name"])}</li>'
                   for m in b["maturing"]) or f"<li>{escape(t['nomat'])}</li>"
    th = 'style="text-align:left;padding:6px 8px;font-size:11px;color:#5e5546;border-bottom:2px solid #c9a24a"'
    table = (f'<table style="border-collapse:collapse;width:100%"><tr><th {th}>{t["date"]}</th><th {th}>{t["country"]}</th>'
             f'<th {th}>{t["security"]}</th><th {th}>{t["alloc"]}</th><th {th}>{t["yld"]}</th></tr>{rows}</table>'
             if rows else f"<p>{escape(t['none'])}</p>")
    return f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Africa Bonds Monitor · {escape(t["title"])} · {escape(d(b["as_of"]))}</title></head>
<body style="margin:0;background:#f2ead8;font-family:Helvetica,Arial,sans-serif;color:#1a1712">
<div style="max-width:680px;margin:0 auto;background:#fbf7ee;padding:24px 20px">
<div style="font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#8a6a1f">Africa Bonds Monitor</div>
<h1 style="font-family:Georgia,serif;font-weight:400;color:#13306b;font-size:26px;margin:6px 0 2px">{escape(t["title"])} · {escape(d(b["as_of"]))}</h1>
<div style="color:#5e5546;font-size:13px">{escape(t["sub"])} · {escape(t["period"].format(a=d(b["from"]), b=d(b["as_of"])))}</div>
<p style="border-left:3px solid #c9a24a;padding-left:10px;font-size:14px">{escape(totals)}</p>
<h2 style="font-family:Georgia,serif;font-weight:400;color:#13306b;font-size:18px">{escape(t["results"])}</h2>
{table}
<h2 style="font-family:Georgia,serif;font-weight:400;color:#13306b;font-size:18px">{escape(t["maturing"].format(d=b["maturity_days"]))}</h2>
<ul style="font-size:13px;padding-left:18px">{mats}</ul>
<p><a href="{escape(site_url)}" style="display:inline-block;background:#13306b;color:#fbf7ee;padding:9px 16px;text-decoration:none;border-radius:2px">{escape(t["site"])}</a></p>
<p style="font-size:11px;color:#5e5546">{escape(t["legal"])}</p>
</div></body></html>"""


def write(as_of: date, dist: Path) -> dict:
    b = build(as_of)
    out = dist / "brief"
    out.mkdir(parents=True, exist_ok=True)
    for lang in T:
        (out / f"{lang}.html").write_text(email_html(b, lang))
    (out / "brief.json").write_text(json.dumps(b, ensure_ascii=False, indent=1))
    return b


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--as-of", required=True, type=date.fromisoformat)
    print(json.dumps(build(p.parse_args().as_of), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
