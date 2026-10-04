"""Quarterly summary report ("synthèse trimestrielle") of WAEMU government securities auctions.

    python site/report.py --as-of 2026-10-04 [--pdf] [--purchase-url URL]

Everything is computed from the verified real auctions versioned in
backend/app/seed/data/verified_market_data.json (FACT rows from UMOA-Titres). Every figure in the
report is a CALCULATION on those rows; nothing is estimated or filled in. Quarters are calendar
quarters that ended on or before --as-of.

Two editions per quarter and language:
  * preview  (public)  -> site/dist/rapports/<slug>/   cover, regional summary, country table,
                          method, credits. Linked from the site's "Rapports" section.
  * complete           -> site/reports/<slug>/ (HTML + PDF); with --pdf the PDF is also published
                          in site/dist/rapports/<slug>/ behind the free account. It adds one page
                          per country (flag and coat of arms, key figures, 8-quarter history,
                          yields by residual maturity, largest operations) and the list of
                          source documents. Free publication only: the source institutions
                          authorised publication, not resale (backend/app/ingest/data/authorisations.json).
With --pdf, both editions are also printed to PDF with headless Chromium.

Flags and coats of arms come from brand/emblems/ (fetched by site/emblems.py, with licences).
"""

import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import unicodedata
from collections import defaultdict
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
sys.path.insert(0, str(REPO / "backend"))

from app.seed.africa import AFRICA  # noqa: E402

DATA = REPO / "backend" / "app" / "seed" / "data" / "verified_market_data.json"
EMBLEMS = REPO / "brand" / "emblems"
PRIVATE = ROOT / "reports"
NON_ISSUANCE = {"buyback", "switch"}  # same exclusion as the engine's issuance series
HISTORY = 8  # quarters shown in the history charts
BILLION = Decimal(10**9)
NAMES = {a.iso3: {"fr": a.name_fr, "en": a.name} for a in AFRICA}
# Residual maturity on the auction date, in years: (upper bound, key). None = open-ended.
BUCKETS = [(1, "b1"), (3, "b2"), (5, "b3"), (7, "b4"), (None, "b5")]

T = {
    "fr": {
        "title": "Synthèse trimestrielle", "subtitle": "Marché des titres publics de l'UMOA",
        "q": "T{q} {y}", "period": "du {a} au {b}", "asof": "Données vérifiées au {d}",
        "preview": "Aperçu gratuit", "complete": "Édition complète",
        "summary": "Synthèse régionale", "countries": "Les pays du trimestre", "country": "Pays",
        "n": "Adjudications", "alloc": "Montant retenu", "sub": "Montant soumis", "ratio": "Soumis / retenu",
        "yld": "Rendement moyen pondéré", "bb": "Rachats", "share": "Part", "bills": "Bons (BAT)",
        "bonds": "Obligations (OAT)", "vs_prev": "vs {p}", "vs_year": "vs {p}", "bp": "pb", "nd": "n.d.",
        "unit": "Md FCFA", "hist_alloc": "Montant retenu par trimestre (Md FCFA)",
        "hist_yld": "Rendement moyen pondéré par trimestre (%)",
        "buckets": "Par maturité résiduelle à la date d'adjudication",
        "b1": "≤ 1 an", "b2": "1 à 3 ans", "b3": "3 à 5 ans", "b4": "5 à 7 ans", "b5": "> 7 ans",
        "bucket": "Maturité", "top": "Plus grosses opérations du trimestre", "date": "Date", "security": "Titre",
        "sources": "Documents sources", "no_data": "Aucune adjudication vérifiée ce trimestre.",
        "no_yield": "{n} adjudication(s) avec montant retenu mais sans rendement publié, exclue(s) des moyennes de rendement.",
        "unallotted": "Dont {n} adjudication(s) sans montant retenu (offres rejetées ou aucune offre) : comptées dans le nombre d'adjudications, sans effet sur les montants ni les rendements.",
        "inside": "Contenu de l'édition complète",
        "inside_list": ["Une fiche par pays : drapeau et armoiries, chiffres clés, comparaison au trimestre précédent et à l'année précédente",
                        "Historique sur 8 trimestres : montants retenus et rendements",
                        "Rendements par maturité résiduelle, bons et obligations séparés",
                        "Les plus grosses opérations du trimestre, avec lien vers le compte rendu officiel",
                        "Liste complète des documents sources (UMOA-Titres)"],
        "buy": "Obtenir l'édition complète",
        "method": "Méthode",
        "method_list": ["Source : comptes rendus d'adjudication publiés par UMOA-Titres, extraits puis vérifiés (contrôles automatiques stricts, audit indépendant, décisions documentées du propriétaire).",
                        "Nature : chaque chiffre de ce rapport est un CALCUL sur ces données officielles (FACT). Aucune donnée n'est estimée, complétée ou synthétique.",
                        "Couverture : seules les adjudications vérifiées sont comptées. Une adjudication encore en attente de vérification, ou dont le compte rendu n'a pas pu être lu, manque aux totaux, qui sont donc des minimums.",
                        "Montant retenu, soumis : sommes des adjudications d'émission du trimestre ; les rachats (et échanges) sont exclus et comptés à part.",
                        "Soumis / retenu : somme des montants soumis divisée par la somme des montants retenus, sur les adjudications où les deux sont publiés. Ce n'est pas le taux de couverture officiel (soumis / mis en adjudication), souvent non publié par titre.",
                        "Rendement moyen pondéré : moyenne des rendements moyens pondérés publiés, pondérée par le montant retenu. Il mélange des maturités différentes : voir la ventilation par maturité résiduelle.",
                        "Variations : en % pour les montants, en points de base (pb) pour les rendements. « n.d. » : non disponible dans les données vérifiées."],
        "legal": "Publication indépendante de Cartouche · African Bond Intelligence. Elle n'émane d'aucun État, ni de la BCEAO, ni d'UMOA-Titres, et n'est approuvée par aucun d'eux. Les drapeaux et armoiries sont reproduits uniquement pour identifier les pays. Ce document est informatif et ne constitue ni un conseil en investissement ni une recommandation.",
        "credits": "Crédits des emblèmes (Wikimedia Commons)", "flag": "Drapeau", "arms": "Armoiries",
        "license": "Licence", "author": "Auteur", "see_page": "voir la page Commons", "unchanged": "Reproduits sans modification, à taille réduite.",
        "lead": "Au {q}, les {k} États de l'UMOA ont levé {alloc} lors de {n} adjudications d'émission{delta}.",
        "lead_yld": " Le rendement moyen pondéré ressort à {y}{dy}.",
        "lead_top": " Premier émetteur : {c} ({s} du total).",
        "up": "en hausse de {v}", "down": "en baisse de {v}", "flat": "stable",
        "page": "Page", "per_country": "Fiche pays",
    },
    "en": {
        "title": "Quarterly review", "subtitle": "WAEMU government securities market",
        "q": "Q{q} {y}", "period": "{a} to {b}", "asof": "Verified data as of {d}",
        "preview": "Free preview", "complete": "Full edition",
        "summary": "Regional summary", "countries": "Countries this quarter", "country": "Country",
        "n": "Auctions", "alloc": "Amount allotted", "sub": "Amount bid", "ratio": "Bid / allotted",
        "yld": "Weighted average yield", "bb": "Buybacks", "share": "Share", "bills": "Bills (BAT)",
        "bonds": "Bonds (OAT)", "vs_prev": "vs {p}", "vs_year": "vs {p}", "bp": "bp", "nd": "n/a",
        "unit": "XOF bn", "hist_alloc": "Amount allotted per quarter (XOF bn)",
        "hist_yld": "Weighted average yield per quarter (%)",
        "buckets": "By residual maturity on the auction date",
        "b1": "≤ 1 yr", "b2": "1–3 yrs", "b3": "3–5 yrs", "b4": "5–7 yrs", "b5": "> 7 yrs",
        "bucket": "Maturity", "top": "Largest operations of the quarter", "date": "Date", "security": "Security",
        "sources": "Source documents", "no_data": "No verified auction this quarter.",
        "no_yield": "{n} auction(s) with an amount allotted but no published yield, left out of yield averages.",
        "unallotted": "Including {n} auction(s) with nothing allotted (bids rejected or none received): counted in the number of auctions, with no effect on amounts or yields.",
        "inside": "What the full edition contains",
        "inside_list": ["One page per country: flag and coat of arms, key figures, comparison with the previous quarter and the previous year",
                        "8-quarter history: amounts allotted and yields",
                        "Yields by residual maturity, bills and bonds shown separately",
                        "The largest operations of the quarter, linked to the official results report",
                        "Full list of source documents (UMOA-Titres)"],
        "buy": "Get the full edition",
        "method": "Method",
        "method_list": ["Source: auction results reports published by UMOA-Titres, extracted then verified (strict automatic checks, independent audit, documented owner decisions).",
                        "Nature: every figure in this report is a CALCULATION on these official data (FACT). Nothing is estimated, filled in or synthetic.",
                        "Coverage: only verified auctions are counted. An auction still awaiting verification, or whose results report could not be read, is missing from the totals, which are therefore lower bounds.",
                        "Amount allotted, bid: sums over the quarter's issuance auctions; buybacks (and switches) are excluded and counted separately.",
                        "Bid / allotted: sum of amounts bid divided by sum of amounts allotted, over auctions where both are published. It is not the official cover ratio (bid / offered), often not published per security.",
                        "Weighted average yield: the published weighted average yields, averaged with the amount allotted as weight. It mixes maturities: see the breakdown by residual maturity.",
                        "Changes: % for amounts, basis points (bp) for yields. \"n/a\": not available in the verified data."],
        "legal": "Independent publication by Cartouche · African Bond Intelligence. It is not issued or endorsed by any State, the BCEAO or UMOA-Titres. Flags and coats of arms are shown only to identify the countries. This document is for information only and is neither investment advice nor a recommendation.",
        "credits": "Emblem credits (Wikimedia Commons)", "flag": "Flag", "arms": "Coat of arms",
        "license": "Licence", "author": "Author", "see_page": "see the Commons page", "unchanged": "Reproduced unmodified, at reduced size.",
        "lead": "In {q}, the {k} WAEMU States raised {alloc} in {n} issuance auctions{delta}.",
        "lead_yld": " The weighted average yield was {y}{dy}.",
        "lead_top": " Largest issuer: {c} ({s} of the total).",
        "up": "up {v}", "down": "down {v}", "flat": "unchanged",
        "page": "Page", "per_country": "Country page",
    },
}


# ---------------------------------------------------------------- data

def _dec(v):
    return None if v is None else Decimal(v)


ZONES = {a.iso3: a.zone.value for a in AFRICA}
REPORT_ZONE = "WAEMU"  # the quarterly report covers the WAEMU States (one currency, XOF)


def load_rows(path: Path = DATA, zone: str | None = None) -> list[dict]:
    """Verified real auctions; `zone` (e.g. "WAEMU") keeps only that monetary zone's countries."""
    data = json.loads(path.read_text())
    secs = {s["isin"]: s for s in data["securities"]}
    rows = []
    for a in data["auctions"]:
        if a["is_synthetic"] or a["verification_status"] != "verified":
            continue
        s = secs[a["isin"]]
        if zone and ZONES.get(s["country"]) != zone:
            continue
        d = date.fromisoformat(a["auction_date"])
        mat = date.fromisoformat(s["maturity_date"]) if s["maturity_date"] else None
        rows.append({
            "country": s["country"], "date": d, "type": a["auction_type"], "isin": a["isin"],
            "name": s["security_name"], "instr": s["instrument_type"], "maturity": mat,
            "residual_years": (mat - d).days / 365.25 if mat else None,
            "alloc": _dec(a["amount_allocated"]), "sub": _dec(a["amount_submitted"]),
            "yld": _dec(a["weighted_average_yield"]), "url": a["source_url"], "currency": s["currency"],
        })
    return rows


def quarter(d: date) -> tuple[int, int]:
    return d.year, (d.month - 1) // 3 + 1


def shift(q: tuple[int, int], k: int) -> tuple[int, int]:
    i = q[0] * 4 + q[1] - 1 + k
    return i // 4, i % 4 + 1


def bounds(q: tuple[int, int]) -> tuple[date, date]:
    start = date(q[0], 3 * q[1] - 2, 1)
    nxt = shift(q, 1)
    return start, date(nxt[0], 3 * nxt[1] - 2, 1) - timedelta(days=1)


def slug(q: tuple[int, int]) -> str:
    return f"{q[0]}-T{q[1]}"


def stats(rows: list[dict]) -> dict:
    """CALCULATION over FACT rows. Returns None for a figure the rows cannot support."""
    prim = [r for r in rows if r["type"] not in NON_ISSUANCE]
    bb = [r for r in rows if r["type"] in NON_ISSUANCE]
    alloc = sum((r["alloc"] for r in prim if r["alloc"] is not None), Decimal(0))
    pairs = [r for r in prim if r["alloc"] and r["sub"] is not None]
    pa = sum((r["alloc"] for r in pairs), Decimal(0))
    ratio = sum((r["sub"] for r in pairs), Decimal(0)) / pa if pa else None

    def wavg(rs):
        w = [r for r in rs if r["yld"] is not None and r["alloc"]]
        tot = sum((r["alloc"] for r in w), Decimal(0))
        return (sum((r["yld"] * r["alloc"] for r in w), Decimal(0)) / tot) if tot else None

    buckets = {}
    for upper, key in BUCKETS:
        lower = {"b1": None, "b2": 1, "b3": 3, "b4": 5, "b5": 7}[key]
        rs = [r for r in prim if r["residual_years"] is not None
              and r["residual_years"] > (lower or 0) and (upper is None or r["residual_years"] <= upper)]
        if rs:
            buckets[key] = {"n": len(rs), "alloc": sum((r["alloc"] or 0 for r in rs), Decimal(0)), "yld": wavg(rs)}
    return {
        "n": len(prim), "alloc": alloc if prim else None,
        "sub": sum((r["sub"] for r in prim if r["sub"] is not None), Decimal(0)) if prim else None,
        "ratio": ratio, "yld": wavg(prim),
        "no_yield": sum(1 for r in prim if r["yld"] is None and r["alloc"]),
        "unallotted": sum(1 for r in prim if not r["alloc"]),
        "bills": sum((r["alloc"] or 0 for r in prim if r["instr"] == "treasury_bill"), Decimal(0)),
        "bonds": sum((r["alloc"] or 0 for r in prim if r["instr"] != "treasury_bill"), Decimal(0)),
        "bb_n": len(bb), "bb_amount": sum((r["alloc"] or 0 for r in bb), Decimal(0)),
        "buckets": buckets,
        "top": sorted((r for r in prim if r["alloc"]), key=lambda r: (-r["alloc"], r["date"], r["isin"]))[:5],
        "docs": sorted({r["url"] for r in rows if r["url"]}),
    }


def complete_quarters(rows: list[dict], as_of: date) -> list[tuple[int, int]]:
    """Quarters that ended on or before as_of and hold at least one verified issuance auction."""
    have = {quarter(r["date"]) for r in rows if r["type"] not in NON_ISSUANCE}
    return sorted(q for q in have if bounds(q)[1] <= as_of)


# ---------------------------------------------------------------- formatting

def fmt_num(v, lang: str, digits: int = 1) -> str:
    v = Decimal(str(v)).quantize(Decimal(1).scaleb(-digits), rounding=ROUND_HALF_UP)  # 0,25 -> 0,3 (not banker's)
    s = f"{v:,.{digits}f}"
    return s.replace(",", " ").replace(".", ",") if lang == "fr" else s


def fmt_bn(v, lang: str) -> str:
    return T[lang]["nd"] if v is None else f"{fmt_num(Decimal(v) / BILLION, lang)} {T[lang]['unit']}"


def fmt_pct(v, lang: str, digits: int = 2) -> str:
    return T[lang]["nd"] if v is None else f"{fmt_num(v, lang, digits)} %" if lang == "fr" else f"{fmt_num(v, lang, digits)}%"


def fmt_ratio(v, lang: str) -> str:
    return T[lang]["nd"] if v is None else f"{fmt_num(v, lang, 2)}×"


def fmt_date(d: date, lang: str) -> str:
    return d.strftime("%d/%m/%Y") if lang == "fr" else d.isoformat()


def _sortkey(name: str) -> str:
    """Alphabetical order ignoring accents (Bénin before Burkina Faso)."""
    return "".join(ch for ch in unicodedata.normalize("NFD", name) if not unicodedata.combining(ch)).lower()


def ql(q, lang):
    return T[lang]["q"].format(q=q[1], y=q[0])


def delta_amount(cur, prev, lang) -> str | None:
    if cur is None or not prev:
        return None
    ch = ((Decimal(cur) - Decimal(prev)) / Decimal(prev) * 100).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    sign = "+" if ch > 0 else "−" if ch < 0 else "±"
    return f"{sign}{fmt_num(abs(ch), lang, 1)} %" if lang == "fr" else f"{sign}{fmt_num(abs(ch), lang, 1)}%"


def delta_bp(cur, prev, lang) -> str | None:
    if cur is None or prev is None:
        return None
    bp = int(((cur - prev) * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP))
    sign = "+" if bp > 0 else "−" if bp < 0 else "±"
    return f"{sign}{abs(bp)} {T[lang]['bp']}"


# ---------------------------------------------------------------- emblems

def emblems() -> dict:
    p = EMBLEMS / "emblems.json"
    return json.loads(p.read_text())["countries"] if p.exists() else {}


def img(iso3: str, kind: str, cls: str, embed: bool, em: dict, lang: str) -> str:
    e = em.get(iso3, {}).get(kind)
    if not e or not (EMBLEMS / e["file"]).exists():
        return ""
    src = ("data:image/svg+xml;base64," + base64.b64encode((EMBLEMS / e["file"]).read_bytes()).decode()
           if embed else f"../emblems/{e['file']}")
    alt = f"{T[lang]['flag' if kind == 'flag' else 'arms']} — {NAMES[iso3][lang]}"
    return f'<img class="{cls}" src="{src}" alt="{escape(alt)}">'


# ---------------------------------------------------------------- charts (inline SVG, one series each)

def bar_chart(points: list[tuple[str, Decimal | None]], lang: str, w=330, h=150) -> str:
    """Single-series column chart: amount allotted per quarter (XOF bn)."""
    vals = [float(v / BILLION) if v is not None else None for _, v in points]
    top = max([v for v in vals if v is not None] or [1]) or 1
    pad_l, pad_b, pad_t = 6, 22, 16
    bw = (w - pad_l * 2) / len(points)
    out = [f'<svg class="chart" viewBox="0 0 {w} {h}" role="img"><line class="axis" x1="{pad_l}" x2="{w - pad_l}" y1="{h - pad_b}" y2="{h - pad_b}"/>']
    for i, ((label, _), v) in enumerate(zip(points, vals)):
        x = pad_l + i * bw + bw * 0.18
        bwi = bw * 0.64
        out.append(f'<text class="tick" x="{x + bwi / 2:.1f}" y="{h - 7}" text-anchor="middle">{escape(label)}</text>')
        if v is None:
            out.append(f'<text class="tick" x="{x + bwi / 2:.1f}" y="{h - pad_b - 4}" text-anchor="middle">–</text>')
            continue
        bh = max((h - pad_b - pad_t) * v / top, 1)
        y = h - pad_b - bh
        last = i == len(points) - 1
        r = min(4, bwi / 2, bh)
        path = (f"M{x:.1f},{h - pad_b} V{y + r:.1f} Q{x:.1f},{y:.1f} {x + r:.1f},{y:.1f} H{x + bwi - r:.1f} "
                f"Q{x + bwi:.1f},{y:.1f} {x + bwi:.1f},{y + r:.1f} V{h - pad_b} Z")
        out.append(f'<path class="bar{" hi" if last else ""}" d="{path}"><title>{escape(label)} : {fmt_num(v, lang)} {T[lang]["unit"]}</title></path>')
        if last or v == top:
            out.append(f'<text class="val" x="{x + bwi / 2:.1f}" y="{y - 4:.1f}" text-anchor="middle">{fmt_num(v, lang, 0)}</text>')
    out.append("</svg>")
    return "".join(out)


def line_chart(points: list[tuple[str, Decimal | None]], lang: str, w=330, h=150) -> str:
    """Single-series line: weighted average yield per quarter (%). Gaps stay gaps."""
    vals = [float(v) if v is not None else None for _, v in points]
    known = [v for v in vals if v is not None]
    if not known:
        return ""
    lo, hi = min(known), max(known)
    span = max(hi - lo, 0.5)
    lo, hi = lo - span * 0.25, hi + span * 0.25
    pad_l, pad_b, pad_t = 6, 22, 16
    step = (w - pad_l * 2) / len(points)
    xs = [pad_l + step * (i + 0.5) for i in range(len(points))]
    ys = [None if v is None else pad_t + (h - pad_b - pad_t) * (1 - (v - lo) / (hi - lo)) for v in vals]
    out = [f'<svg class="chart" viewBox="0 0 {w} {h}" role="img"><line class="axis" x1="{pad_l}" x2="{w - pad_l}" y1="{h - pad_b}" y2="{h - pad_b}"/>']
    seg: list[str] = []
    for x, y in zip(xs, ys):
        if y is None:
            if len(seg) > 1:
                out.append(f'<polyline class="line" points="{" ".join(seg)}"/>')
            seg = []
        else:
            seg.append(f"{x:.1f},{y:.1f}")
    if len(seg) > 1:
        out.append(f'<polyline class="line" points="{" ".join(seg)}"/>')
    imax = vals.index(max(known))
    for i, ((label, _), x, y, v) in enumerate(zip(points, xs, ys, vals)):
        out.append(f'<text class="tick" x="{x:.1f}" y="{h - 7}" text-anchor="middle">{escape(label)}</text>')
        if y is None:
            continue
        last = i == len(points) - 1
        out.append(f'<circle class="dot{" hi" if last else ""}" cx="{x:.1f}" cy="{y:.1f}" r="{4 if last else 3}"><title>{escape(label)} : {fmt_pct(v, lang)}</title></circle>')
        if last or i == imax:
            out.append(f'<text class="val" x="{x:.1f}" y="{y - 8:.1f}" text-anchor="middle">{fmt_num(v, lang, 2)}</text>')
    out.append("</svg>")
    return "".join(out)


# ---------------------------------------------------------------- HTML

CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
:root { --paper:#fbf7ee; --ink:#1a1712; --muted:#5e5546; --line:#ddd2bb; --lapis:#13306b; --gold:#c9a24a; --gold-ink:#8a6a1f; --carnelian:#a8432a; --faience:#1f7a73; }
html { background:#e9e2d0; }
body { margin:0; color:var(--ink); font:10.5pt/1.45 "IBM Plex Sans", "Helvetica Neue", Arial, sans-serif; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
.page { width:210mm; min-height:297mm; margin:12px auto; padding:16mm 16mm 20mm; background:var(--paper); position:relative; break-after:page; box-shadow:0 1px 6px rgba(0,0,0,.12); }
.page:last-child { break-after:auto; }
@media print { html { background:none; } .page { margin:0; box-shadow:none; height:297mm; overflow:hidden; } }
h1,h2,h3 { font-family:Marcellus, Georgia, serif; font-weight:400; color:var(--lapis); margin:0 0 8px; }
h1 { font-size:30pt; line-height:1.1; } h2 { font-size:17pt; border-bottom:2px solid var(--gold); padding-bottom:4px; margin-bottom:12px; } h3 { font-size:12pt; margin-top:14px; }
.num { font-family:"IBM Plex Mono", Menlo, monospace; font-variant-numeric:tabular-nums; }
.muted { color:var(--muted); } .small { font-size:8.5pt; }
.brand { font-family:Marcellus, Georgia, serif; letter-spacing:.08em; text-transform:uppercase; color:var(--gold-ink); font-size:10pt; }
.cover { display:flex; flex-direction:column; background:var(--lapis); color:#f2ead8; }
.cover h1 { color:#f2ead8; margin-top:40mm; } .cover .brand { color:var(--gold); }
.cover .q { font-family:Marcellus, Georgia, serif; font-size:40pt; color:var(--gold); margin:6mm 0 2mm; }
.cover .flags { display:grid; grid-template-columns:repeat(4,1fr); gap:8mm 6mm; margin-top:auto; margin-bottom:14mm; }
.cover .flags figure { margin:0; text-align:center; font-size:9pt; color:#d9cfb8; }
.cover .flags img { height:26mm; width:auto; max-width:100%; border:1px solid rgba(255,255,255,.35); display:block; margin:0 auto 4px; }  /* true proportions: flags differ (2:1, 7:6, 3:2...) */
.cover .edition { display:inline-block; border:1px solid var(--gold); color:var(--gold); padding:2px 10px; border-radius:2px; font-size:9pt; letter-spacing:.06em; text-transform:uppercase; }
.cover .legal { color:#b9ae97; font-size:7.5pt; }
.kpis { display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin:10px 0 14px; }
.kpi { border:1px solid var(--line); background:#fff; padding:8px 10px; border-radius:3px; }
.kpi b { display:block; font:600 13pt/1.2 "IBM Plex Mono", Menlo, monospace; color:var(--ink); margin:2px 0; }
.kpi span { font-size:8pt; color:var(--muted); display:block; }
.kpi .lbl { font-size:8pt; text-transform:uppercase; letter-spacing:.04em; color:var(--muted); }
.lead { font-size:11.5pt; border-left:3px solid var(--gold); padding-left:10px; margin:8px 0 14px; }
table { width:100%; border-collapse:collapse; font-size:9pt; }
th { text-align:left; font-weight:600; color:var(--muted); border-bottom:1.5px solid var(--ink); padding:4px 5px; font-size:8pt; }
td { border-bottom:1px solid var(--line); padding:4px 5px; vertical-align:middle; }
td.r, th.r { text-align:right; }
td img.mini { height:16px; width:auto; vertical-align:middle; margin-right:6px; border:1px solid var(--line); }
.chead { display:flex; align-items:center; gap:14px; margin-bottom:10px; }
.chead .flag { height:44px; width:auto; border:1px solid var(--line); }
.chead .arms { height:62px; width:auto; max-width:80px; object-fit:contain; }
.chead h2 { flex:1; margin:0; border:none; padding:0; font-size:22pt; }
.charts { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin:6px 0; }
.charts figure { margin:0; border:1px solid var(--line); background:#fff; padding:6px 8px; border-radius:3px; }
.charts figcaption { font-size:8pt; color:var(--muted); margin-bottom:2px; }
svg.chart { width:100%; height:auto; display:block; }
svg .axis { stroke:#b9ae97; stroke-width:1; } svg .tick { font:7.5px "IBM Plex Sans", Arial, sans-serif; fill:#5e5546; }
svg .val { font:600 8px "IBM Plex Mono", Menlo, monospace; fill:#1a1712; }
svg .bar { fill:#9db0d6; } svg .bar.hi { fill:#13306b; }
svg .line { fill:none; stroke:#8a6a1f; stroke-width:2; } svg .dot { fill:#8a6a1f; stroke:#fff; stroke-width:2; } svg .dot.hi { fill:#a8432a; }
.foot { position:absolute; left:16mm; right:16mm; bottom:8mm; display:flex; justify-content:space-between; font-size:7.5pt; color:var(--muted); border-top:1px solid var(--line); padding-top:4px; }
ul.tight { margin:4px 0 8px; padding-left:18px; } ul.tight li { margin:2px 0; }
.cta { display:inline-block; background:var(--lapis); color:#f2ead8; text-decoration:none; padding:8px 16px; border-radius:3px; font-weight:600; margin-top:6px; }
.box { border:1px solid var(--gold); background:#fff; padding:10px 14px; border-radius:3px; margin-top:12px; }
.docs { columns:2; column-gap:14px; font-size:7pt; line-height:1.35; word-break:break-all; }
.docs a { color:var(--lapis); text-decoration:none; }
a { color:var(--lapis); }
.credits td { font-size:7.5pt; vertical-align:top; }
.tag { font-size:7pt; border:1px solid var(--faience); color:var(--faience); padding:0 4px; border-radius:2px; letter-spacing:.04em; }
"""


def kpi(label: str, value: str, notes: list[str | None]) -> str:
    n = " · ".join(x for x in notes if x)
    return f'<div class="kpi"><span class="lbl">{escape(label)}</span><b>{escape(value)}</b><span>{escape(n)}</span></div>'


def kpis(cur: dict, prev: dict | None, year: dict | None, qp: str, qy: str, lang: str) -> str:
    t = T[lang]

    def d(fn, key):
        return [f"{x} {t[k].format(p=lbl)}" for x, lbl, k in
                ((fn(cur[key], p[key], lang) if p else None, q, k) for p, q, k in ((prev, qp, "vs_prev"), (year, qy, "vs_year"))) if x]

    return '<div class="kpis">' + "".join([
        kpi(t["alloc"], fmt_bn(cur["alloc"], lang), d(delta_amount, "alloc")),
        kpi(t["yld"], fmt_pct(cur["yld"], lang), d(delta_bp, "yld")),
        kpi(t["n"], str(cur["n"]), [f"{t['bb']} : {cur['bb_n']} · {fmt_bn(cur['bb_amount'], lang)}" if cur["bb_n"] else None]),
        kpi(t["ratio"], fmt_ratio(cur["ratio"], lang), [f"{t['sub']} : {fmt_bn(cur['sub'], lang)}"]),
    ]) + "</div>"


def lead(q, cur, prev, by_country, lang) -> str:
    t = T[lang]
    delta = delta_amount(cur["alloc"], prev["alloc"], lang) if prev else None
    dtxt = ""
    if delta:
        dtxt = ", " + (t["up"] if delta[0] == "+" else t["down"] if delta[0] == "−" else t["flat"]).format(v=delta[1:]) + \
               " " + t["vs_prev"].format(p=ql(shift(q, -1), lang))
    s = t["lead"].format(q=ql(q, lang), k=len(by_country), alloc=fmt_bn(cur["alloc"], lang), n=cur["n"], delta=dtxt)
    if cur["yld"] is not None:
        dy = delta_bp(cur["yld"], prev["yld"], lang) if prev else None
        s += t["lead_yld"].format(y=fmt_pct(cur["yld"], lang), dy=f" ({dy} {t['vs_prev'].format(p=ql(shift(q, -1), lang))})" if dy else "")
    ranked = sorted(((c, st["alloc"] or 0) for c, st in by_country.items()), key=lambda x: -x[1])
    if ranked and cur["alloc"]:
        c, v = ranked[0]
        s += t["lead_top"].format(c=NAMES[c][lang], s=fmt_pct(Decimal(v) / cur["alloc"] * 100, lang, 1))
    return f'<p class="lead">{escape(s)}</p>'


def author(e: dict, t: dict) -> str:
    """Author as Commons states it; a pointer to the page when Commons gives no usable name."""
    a = (e.get("author") or "").strip()
    if not a or a.lower().startswith(("see ", "this vector image")):
        return t["see_page"]
    return a[:120]


def notes(st: dict, t: dict) -> str:
    out = [t[k].format(n=st[k]) for k in ("unallotted", "no_yield") if st[k]]
    return "".join(f'<p class="small muted">{escape(x)}</p>' for x in out)


def footer(q, edition: str, lang: str) -> str:
    t = T[lang]
    return (f'<div class="foot"><span>Cartouche · {escape(t["title"])} · {escape(ql(q, lang))} · {escape(edition)}</span>'
            f'<span>{escape(t["subtitle"])}</span></div>')


def render(q, rows, as_of: date, lang: str, edition: str, purchase_url: str | None, em: dict, embed: bool) -> str:
    t = T[lang]
    start, end = bounds(q)
    in_q = lambda rs, qq: [r for r in rs if quarter(r["date"]) == qq]  # noqa: E731
    cur_rows = in_q(rows, q)
    cur, prev_rows, year_rows = stats(cur_rows), in_q(rows, shift(q, -1)), in_q(rows, shift(q, -4))
    prev = stats(prev_rows) if prev_rows else None
    year = stats(year_rows) if year_rows else None
    qp, qy = ql(shift(q, -1), lang), ql(shift(q, -4), lang)
    countries = sorted({r["country"] for r in cur_rows if r["type"] not in NON_ISSUANCE}, key=lambda c: _sortkey(NAMES[c][lang]))
    by_country = {c: stats([r for r in cur_rows if r["country"] == c]) for c in countries}
    ed_label = t["complete"] if edition == "complete" else t["preview"]
    pages = []

    # Cover
    flags = "".join(f'<figure>{img(c, "flag", "", embed, em, lang)}{escape(NAMES[c][lang])}</figure>' for c in countries)
    pages.append(f"""<section class="page cover">
<div class="brand">Cartouche · African Bond Intelligence</div>
<h1>{escape(t["title"])}<br><span style="font-size:18pt">{escape(t["subtitle"])}</span></h1>
<div class="q">{escape(ql(q, lang))}</div>
<div>{escape(t["period"].format(a=fmt_date(start, lang), b=fmt_date(end, lang)))} · {escape(t["asof"].format(d=fmt_date(as_of, lang)))}</div>
<p><span class="edition">{escape(ed_label)}</span> <span class="tag" style="color:#5cc9bd;border-color:#5cc9bd">CALCULATION · FACT UMOA-Titres</span></p>
<div class="flags">{flags}</div>
<p class="legal">{escape(t["legal"])}</p>
</section>""")

    # Regional summary
    hist_q = [shift(q, -k) for k in range(HISTORY - 1, -1, -1)]
    hist = [(ql(h, lang).replace(" 20", " "), stats(in_q(rows, h)) if in_q(rows, h) else None) for h in hist_q]
    charts = (f'<div class="charts"><figure><figcaption>{escape(t["hist_alloc"])}</figcaption>'
              f'{bar_chart([(lbl, s["alloc"] if s else None) for lbl, s in hist], lang)}</figure>'
              f'<figure><figcaption>{escape(t["hist_yld"])}</figcaption>'
              f'{line_chart([(lbl, s["yld"] if s else None) for lbl, s in hist], lang)}</figure></div>')
    bucket_rows = "".join(
        f'<tr><td>{escape(t[k])}</td><td class="r num">{b["n"]}</td><td class="r num">{escape(fmt_bn(b["alloc"], lang))}</td>'
        f'<td class="r num">{escape(fmt_pct(b["yld"], lang))}</td></tr>'
        for k, b in ((k, cur["buckets"].get(k)) for _, k in BUCKETS) if b)
    nyl = notes(cur, t)
    pages.append(f"""<section class="page"><h2>{escape(t["summary"])} · {escape(ql(q, lang))}</h2>
{lead(q, cur, prev, by_country, lang)}
{kpis(cur, prev, year, qp, qy, lang)}
{charts}
<h3>{escape(t["buckets"])}</h3>
<table><thead><tr><th>{escape(t["bucket"])}</th><th class="r">{escape(t["n"])}</th><th class="r">{escape(t["alloc"])}</th><th class="r">{escape(t["yld"])}</th></tr></thead><tbody>{bucket_rows}</tbody></table>
<p class="small muted">{escape(t["bills"])} : {escape(fmt_bn(cur["bills"], lang))} · {escape(t["bonds"])} : {escape(fmt_bn(cur["bonds"], lang))}</p>{nyl}
{footer(q, ed_label, lang)}</section>""")

    # Country table
    trs = "".join(
        f'<tr><td>{img(c, "flag", "mini", embed, em, lang)}{escape(NAMES[c][lang])}</td><td class="r num">{s["n"]}</td>'
        f'<td class="r num">{escape(fmt_bn(s["alloc"], lang))}</td>'
        f'<td class="r num">{escape(fmt_pct(Decimal(s["alloc"] or 0) / cur["alloc"] * 100, lang, 1) if cur["alloc"] else t["nd"])}</td>'
        f'<td class="r num">{escape(fmt_pct(s["yld"], lang))}</td><td class="r num">{escape(fmt_ratio(s["ratio"], lang))}</td>'
        f'<td class="r num">{s["bb_n"] or ""}</td></tr>' for c, s in by_country.items())
    extra = ""
    if edition == "preview":
        items = "".join(f"<li>{escape(x)}</li>" for x in t["inside_list"])
        cta = f'<p><a class="cta" href="{escape(purchase_url)}" rel="noopener">{escape(t["buy"])}</a></p>' if purchase_url else ""
        extra = f'<div class="box"><h3 style="margin-top:0">{escape(t["inside"])}</h3><ul class="tight">{items}</ul>{cta}</div>'
    pages.append(f"""<section class="page"><h2>{escape(t["countries"])}</h2>
<table><thead><tr><th>{escape(t["country"])}</th><th class="r">{escape(t["n"])}</th><th class="r">{escape(t["alloc"])}</th><th class="r">{escape(t["share"])}</th><th class="r">{escape(t["yld"])}</th><th class="r">{escape(t["ratio"])}</th><th class="r">{escape(t["bb"])}</th></tr></thead><tbody>{trs}</tbody></table>
{extra}
{footer(q, ed_label, lang)}</section>""")

    # Country pages (complete edition only)
    if edition == "complete":
        for c in countries:
            s = by_country[c]
            crow = lambda qq: [r for r in rows if r["country"] == c and quarter(r["date"]) == qq]  # noqa: E731
            cp = stats(crow(shift(q, -1))) if crow(shift(q, -1)) else None
            cy = stats(crow(shift(q, -4))) if crow(shift(q, -4)) else None
            ch = [(ql(h, lang).replace(" 20", " "), stats(crow(h)) if crow(h) else None) for h in hist_q]
            ccharts = (f'<div class="charts"><figure><figcaption>{escape(t["hist_alloc"])}</figcaption>'
                       f'{bar_chart([(lbl, x["alloc"] if x else None) for lbl, x in ch], lang)}</figure>'
                       f'<figure><figcaption>{escape(t["hist_yld"])}</figcaption>'
                       f'{line_chart([(lbl, x["yld"] if x else None) for lbl, x in ch], lang)}</figure></div>')
            brow = "".join(
                f'<tr><td>{escape(t[k])}</td><td class="r num">{b["n"]}</td><td class="r num">{escape(fmt_bn(b["alloc"], lang))}</td>'
                f'<td class="r num">{escape(fmt_pct(b["yld"], lang))}</td></tr>'
                for k, b in ((k, s["buckets"].get(k)) for _, k in BUCKETS) if b)
            top = "".join(
                f'<tr><td class="num">{escape(fmt_date(r["date"], lang))}</td><td>{escape(r["name"])}</td>'
                f'<td class="r num">{escape(fmt_bn(r["alloc"], lang))}</td><td class="r num">{escape(fmt_bn(r["sub"], lang))}</td>'
                f'<td class="r num">{escape(fmt_pct(r["yld"], lang))}</td>'
                f'<td><a href="{escape(r["url"])}">PDF</a></td></tr>' for r in s["top"])
            cnyl = notes(s, t)
            pages.append(f"""<section class="page">
<div class="chead">{img(c, "flag", "flag", embed, em, lang)}<h2>{escape(NAMES[c][lang])}</h2>{img(c, "arms", "arms", embed, em, lang)}</div>
<div class="small muted" style="margin-bottom:6px">{escape(t["per_country"])} · {escape(ql(q, lang))}</div>
{kpis(s, cp, cy, qp, qy, lang)}
{ccharts}
<h3>{escape(t["buckets"])}</h3>
<table><thead><tr><th>{escape(t["bucket"])}</th><th class="r">{escape(t["n"])}</th><th class="r">{escape(t["alloc"])}</th><th class="r">{escape(t["yld"])}</th></tr></thead><tbody>{brow}</tbody></table>
<p class="small muted">{escape(t["bills"])} : {escape(fmt_bn(s["bills"], lang))} · {escape(t["bonds"])} : {escape(fmt_bn(s["bonds"], lang))}</p>{cnyl}
<h3>{escape(t["top"])}</h3>
<table><thead><tr><th>{escape(t["date"])}</th><th>{escape(t["security"])}</th><th class="r">{escape(t["alloc"])}</th><th class="r">{escape(t["sub"])}</th><th class="r">{escape(t["yld"])}</th><th></th></tr></thead><tbody>{top}</tbody></table>
{footer(q, ed_label, lang)}</section>""")

    # Method, legal, credits
    meth = "".join(f"<li>{escape(x)}</li>" for x in t["method_list"])
    cred = []
    for c in countries:
        for kind in ("flag", "arms"):
            e = em.get(c, {}).get(kind)
            if e:
                cred.append(f'<tr><td>{escape(NAMES[c][lang])} — {escape(t[kind])}</td><td><a href="{escape(e["page"])}">{escape(e["commons_title"])}</a></td>'
                            f'<td>{escape(e["license"] or "")}</td><td>{escape(author(e, t))}</td></tr>')
    pages.append(f"""<section class="page"><h2>{escape(t["method"])}</h2>
<ul class="tight">{meth}</ul>
<p class="small">{escape(t["legal"])}</p>
{footer(q, ed_label, lang)}</section>
<section class="page"><h2>{escape(t["credits"])}</h2>
<p class="small muted">{escape(t["unchanged"])}</p>
<table class="credits"><thead><tr><th></th><th>Commons</th><th>{escape(t["license"])}</th><th>{escape(t["author"])}</th></tr></thead><tbody>{"".join(cred)}</tbody></table>
{footer(q, ed_label, lang)}</section>""")

    if edition == "complete":
        docs = "".join(f'<div><a href="{escape(u)}">{escape(u.rsplit("/", 1)[-1])}</a></div>' for u in cur["docs"])
        pages.append(f"""<section class="page" style="height:auto;min-height:297mm"><h2>{escape(t["sources"])} ({len(cur["docs"])})</h2>
<div class="docs">{docs}</div></section>""")

    title = f"Cartouche · {t['title']} {ql(q, lang)}"
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{escape(title)}</title><meta name="robots" content="{"noindex" if edition == "complete" else "index"}">'
            f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Marcellus&family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Mono:wght@400;600&display=swap">'
            f"<style>{CSS}</style></head><body>{''.join(pages)}</body></html>")


# ---------------------------------------------------------------- output

def chromium() -> str | None:
    for p in (os.environ.get("CHROMIUM"), "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
              shutil.which("chromium"), shutil.which("chromium-browser"), shutil.which("google-chrome")):
        if p and Path(p).exists():
            return p
    return None


def to_pdf(html_path: Path, pdf_path: Path) -> bool:
    exe = chromium()
    if not exe:
        print("no Chromium found: PDF skipped")
        return False
    r = subprocess.run([exe, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                        "--virtual-time-budget=8000", f"--print-to-pdf={pdf_path}", html_path.resolve().as_uri()],
                       capture_output=True, text=True, timeout=180)
    return r.returncode == 0 and pdf_path.exists()


def build(as_of: date, dist: Path, pdf: bool = False, purchase_url: str | None = None,
          private: Path = PRIVATE, langs=("fr", "en"), publish_complete: bool = True) -> list[dict]:
    """Write every complete quarter's editions. Returns the index embedded in the site."""
    rows = load_rows(zone=REPORT_ZONE)
    em = emblems()
    out_root = dist / "rapports"
    if out_root.exists():
        shutil.rmtree(out_root)
    (out_root / "emblems").mkdir(parents=True)
    for e in em.values():
        for v in e.values():
            shutil.copy(EMBLEMS / v["file"], out_root / "emblems" / v["file"])
    index = []
    for q in complete_quarters(rows, as_of):
        s = slug(q)
        cur = stats([r for r in rows if quarter(r["date"]) == q])
        entry = {"slug": s, "year": q[0], "quarter": q[1], "start": bounds(q)[0].isoformat(), "end": bounds(q)[1].isoformat(),
                 "auctions": cur["n"], "allotted": str(cur["alloc"]), "countries": sorted({r["country"] for r in rows if quarter(r["date"]) == q and r["type"] not in NON_ISSUANCE}),
                 "flags": sorted(c for c, e in em.items() if "flag" in e),
                 "preview": {}, "preview_pdf": {}, "complete_pdf": {}}
        (out_root / s).mkdir()
        (private / s).mkdir(parents=True, exist_ok=True)
        for lang in langs:
            prev_html = out_root / s / f"apercu-{lang}.html"
            prev_html.write_text(render(q, rows, as_of, lang, "preview", purchase_url, em, embed=False))
            entry["preview"][lang] = f"rapports/{s}/{prev_html.name}"
            full_html = private / s / f"cartouche-{s}-complet-{lang}.html"
            full_html.write_text(render(q, rows, as_of, lang, "complete", purchase_url, em, embed=True))
            if pdf:
                pp = out_root / s / f"cartouche-{s}-apercu-{lang}.pdf"
                if to_pdf(prev_html, pp):
                    entry["preview_pdf"][lang] = f"rapports/{s}/{pp.name}"
                if to_pdf(full_html, full_html.with_suffix(".pdf")) and publish_complete:
                    # Free publication (authorisation scope): the complete PDF is published too, behind
                    # the free account (site/edge/gate.js covers /rapports/*.pdf).
                    cp = out_root / s / full_html.with_suffix(".pdf").name
                    shutil.copy(full_html.with_suffix(".pdf"), cp)
                    entry["complete_pdf"][lang] = f"rapports/{s}/{cp.name}"
        index.append(entry)
    return index[::-1]  # newest first


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--as-of", required=True, type=date.fromisoformat)
    p.add_argument("--dist", type=Path, default=ROOT / "dist")
    p.add_argument("--pdf", action="store_true")
    p.add_argument("--purchase-url", default=os.environ.get("CARTOUCHE_REPORT_PURCHASE_URL"))
    args = p.parse_args()
    index = build(args.as_of, args.dist, args.pdf, args.purchase_url)
    for e in index:
        print(e["slug"], e["auctions"], "auctions", e["preview"])
    print(f"public previews: {args.dist / 'rapports'} · complete editions (private): {PRIVATE}")


if __name__ == "__main__":
    main()
