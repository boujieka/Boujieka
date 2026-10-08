"""Data offer: the verified WAEMU (UMOA-Titres) and CEMAC (BEAC) auction history as a dataset.

    python site/dataset.py --as-of 2026-10-04

Public (deployed, site/dist/donnees/):  data dictionary + coverage page (dictionnaire.html) and a
                                        sample of the full schema (echantillon.csv, 25 rows).
Full files (auctions.csv, securities.csv, documents.csv): published in site/dist/donnees/ behind
the free account (free publication is what the source institutions authorised; no resale), with a
copy and LISEZMOI.txt in site/reports/data/.

Rows are copied as verified (FACT); nothing is computed or filled in. A missing value stays empty,
with its status (not_disclosed / not_available) in the *_status column.
Before any sale or licence, the reuse terms of UMOA-Titres' publications must be checked
(see docs/DATA_OFFER.md).
"""

import argparse
import csv
import io
import json
from collections import Counter
from datetime import date
from html import escape
from pathlib import Path

import report

AUCTION_COLS = ["isin", "country", "currency", "source", "auction_date", "settlement_date", "auction_type", "auction_reference",
                "amount_offered", "amount_submitted", "amount_allocated", "cutoff_yield", "weighted_average_yield",
                "average_price", "number_of_bidders", "yield_convention", "source_url", "document_sha256",
                "data_nature", "verification_status", "field_status", "provenance_notes"]
SECURITY_COLS = ["isin", "country", "issuer", "security_name", "instrument_type", "currency", "face_value",
                 "coupon_rate", "maturity_date", "tenor_days", "field_status", "source_url"]
DOC_COLS = ["url", "title", "publication_date", "content_sha256", "source"]
SAMPLE = 25

DICT = {
    "fr": {
        "title": "Données d'adjudications vérifiées (UEMOA et CEMAC)",
        "lede": "L'historique des résultats d'adjudication des titres publics vérifiés : les 8 États de l'UMOA (comptes rendus d'UMOA-Titres, en XOF) et les États de la CEMAC couverts (avis de résultats de la BEAC, en XAF). Chaque ligne est vérifiée contre le document source et porte sa monnaie, sa source, le lien vers le PDF officiel et l'empreinte SHA-256 du document.",
        "coverage": "Couverture", "files": "Fichiers de l'offre", "dict": "Dictionnaire des champs",
        "sample": "Échantillon gratuit ({n} lignes, même format que le fichier complet)",
        "country": "Pays", "n": "Adjudications", "first": "Première", "last": "Dernière",
        "f_auctions": "auctions.csv — une ligne par adjudication ({n} lignes)",
        "f_securities": "securities.csv — une ligne par titre ({n} lignes)",
        "f_documents": "documents.csv — les documents officiels sources ({n})",
        "update": "Mise à jour : quotidienne (collecte et vérification automatiques), données au {d}.",
        "free": "Gratuit : l'échantillon est libre ; les fichiers complets se téléchargent avec un compte gratuit. Publication autorisée par les institutions sources pour un usage gratuit : la revente des données n'est pas autorisée. Citez la source de chaque ligne (colonne source) : UMOA-Titres pour l'UEMOA, la BEAC pour la CEMAC.",
        "free_open": "Gratuit : l'échantillon et les fichiers complets se téléchargent librement. Publication autorisée par les institutions sources pour un usage gratuit : la revente des données n'est pas autorisée. Citez la source de chaque ligne (colonne source) : UMOA-Titres pour l'UEMOA, la BEAC pour la CEMAC.",
        "legal": "Les données proviennent des publications d'UMOA-Titres et de la BEAC. Africa Bonds Monitor n'est affiliée ni à UMOA-Titres, ni à la BCEAO, ni à la BEAC. Information uniquement, ni conseil ni recommandation.",
        "back": "Retour à la plateforme", "waitlist": "Être informé des mises à jour",
    },
    "en": {
        "title": "Verified auction data (WAEMU and CEMAC)",
        "lede": "The history of verified government securities auction results: the 8 WAEMU States (UMOA-Titres results reports, in XOF) and the CEMAC States covered (BEAC results notices, in XAF). Every row is checked against the source document and carries its currency, its source, the link to the official PDF and the SHA-256 hash of the document.",
        "coverage": "Coverage", "files": "Files in the offer", "dict": "Field dictionary",
        "sample": "Free sample ({n} rows, same format as the full file)",
        "country": "Country", "n": "Auctions", "first": "First", "last": "Last",
        "f_auctions": "auctions.csv — one row per auction ({n} rows)",
        "f_securities": "securities.csv — one row per security ({n} rows)",
        "f_documents": "documents.csv — the official source documents ({n})",
        "update": "Updated daily (automatic collection and verification); data as of {d}.",
        "free": "Free: the sample is open; the full files download with a free account. Publication is authorised by the source institutions for free use: reselling the data is not authorised. Cite each row's source (source column): UMOA-Titres for WAEMU, the BEAC for CEMAC.",
        "free_open": "Free: the sample and the full files download freely. Publication is authorised by the source institutions for free use: reselling the data is not authorised. Cite each row's source (source column): UMOA-Titres for WAEMU, the BEAC for CEMAC.",
        "legal": "The data come from the publications of UMOA-Titres and the BEAC. Africa Bonds Monitor is affiliated with neither UMOA-Titres, the BCEAO nor the BEAC. Information only, neither advice nor recommendation.",
        "back": "Back to the platform", "waitlist": "Get updates",
    },
}
FIELDS = {  # field: (fr, en)
    "isin": ("Code ISIN du titre", "Security ISIN"),
    "country": ("Pays émetteur (ISO 3166 alpha-3)", "Issuing country (ISO 3166 alpha-3)"),
    "currency": ("Monnaie des montants de la ligne : XOF (UEMOA) ou XAF (CEMAC) ; ne jamais additionner les deux", "Currency of the row's amounts: XOF (WAEMU) or XAF (CEMAC); never add the two"),
    "source": ("Institution source de la ligne, à citer", "Source institution of the row, to be cited"),
    "auction_date": ("Date de l'adjudication", "Auction date"),
    "settlement_date": ("Date de valeur (règlement)", "Settlement date"),
    "auction_type": ("primary_auction (émission) ou buyback (rachat)", "primary_auction (issue) or buyback"),
    "auction_reference": ("Numéro d'adjudication tel qu'imprimé (parfois tronqué dans le PDF officiel) ; distingue deux opérations le même jour", "Auction number as printed (sometimes cut off in the official PDF); tells two same-day operations apart"),
    "amount_offered": ("Montant mis en adjudication (monnaie de la ligne), si publié pour ce titre", "Amount offered (row currency), when published for this security"),
    "amount_submitted": ("Montant total des soumissions (monnaie de la ligne)", "Total amount bid (row currency)"),
    "amount_allocated": ("Montant retenu (monnaie de la ligne)", "Amount allotted (row currency)"),
    "cutoff_yield": ("Taux marginal (%)", "Marginal (cut-off) yield (%)"),
    "weighted_average_yield": ("Rendement moyen pondéré publié (%)", "Published weighted average yield (%)"),
    "average_price": ("Prix moyen pondéré (% du nominal)", "Weighted average price (% of par)"),
    "number_of_bidders": ("Nombre de participants", "Number of bidders"),
    "yield_convention": ("Convention de rendement, telle que publiée", "Yield convention, as published"),
    "source_url": ("Lien vers le compte rendu officiel (PDF)", "Link to the official results report (PDF)"),
    "document_sha256": ("Empreinte SHA-256 du document source", "SHA-256 hash of the source document"),
    "data_nature": ("FACT : valeur publiée, non calculée", "FACT: published value, not computed"),
    "verification_status": ("verified : contrôlée contre le document", "verified: checked against the document"),
    "field_status": ("Pour chaque champ vide : not_disclosed (non publié) ou not_available", "For each empty field: not_disclosed or not_available"),
    "provenance_notes": ("Historique de l'extraction, de la vérification et de toute correction", "History of extraction, verification and any correction"),
}


def _csv(rows: list[dict], cols: list[str]) -> str:
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(cols)
    for r in rows:
        w.writerow(["" if r.get(c) is None else json.dumps(r[c], ensure_ascii=False, sort_keys=True)
                    if isinstance(r.get(c), (dict, list)) else r.get(c) for c in cols])
    return "﻿" + buf.getvalue()  # BOM: opens correctly in Excel


def tables(as_of: date | None = None) -> dict:
    data = json.loads(report.DATA.read_text())
    secs = {s["isin"]: s for s in data["securities"]}
    auctions = [{**a, "country": secs[a["isin"]]["country"], "currency": secs[a["isin"]]["currency"]} for a in data["auctions"]
                if not a["is_synthetic"] and a["verification_status"] == "verified"
                and (as_of is None or a["auction_date"] <= as_of.isoformat())]
    auctions.sort(key=lambda a: (a["auction_date"], a["country"], a["isin"], a["auction_type"], a["auction_reference"] or ""))
    docs = [{**d, "content_sha256": d["content_sha256"]} for d in data["documents"]]
    return {"auctions": auctions, "securities": sorted(secs.values(), key=lambda s: s["isin"]), "documents": docs}


def coverage(auctions: list[dict]) -> list[tuple]:
    by = Counter(a["country"] for a in auctions)
    out = []
    for c in sorted(by):
        ds = [a["auction_date"] for a in auctions if a["country"] == c]
        out.append((c, by[c], min(ds), max(ds)))
    return out


def page(t: dict, lang: str, tb: dict, as_of: date, gated: bool = False) -> str:
    cov = "".join(f'<tr><td>{escape(report.NAMES[c][lang])}</td><td class="r">{n}</td><td>{escape(report.fmt_date(date.fromisoformat(a), lang))}</td>'
                  f'<td>{escape(report.fmt_date(date.fromisoformat(b), lang))}</td></tr>' for c, n, a, b in coverage(tb["auctions"]))
    fields = "".join(f"<tr><td><code>{escape(k)}</code></td><td>{escape(v[0 if lang == 'fr' else 1])}</td></tr>" for k, v in FIELDS.items())
    other = "en" if lang == "fr" else "fr"
    return f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Africa Bonds Monitor · {escape(t["title"])}</title>
<style>body{{margin:0;background:#f2ead8;color:#1a1712;font:15px/1.55 "IBM Plex Sans",Helvetica,Arial,sans-serif}}main{{max-width:880px;margin:0 auto;padding:28px 16px 48px}}
h1,h2{{font-family:Marcellus,Georgia,serif;font-weight:400;color:#13306b}}h1{{font-size:30px;margin:6px 0}}h2{{font-size:20px;border-bottom:2px solid #c9a24a;padding-bottom:4px;margin-top:28px}}
.brand{{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#8a6a1f}}table{{border-collapse:collapse;width:100%;font-size:14px;background:#fbf7ee}}
th{{text-align:left;font-size:12px;color:#5e5546;border-bottom:2px solid #c9a24a;padding:6px 8px}}td{{border-bottom:1px solid #ddd2bb;padding:6px 8px;vertical-align:top}}.r{{text-align:right;font-family:Menlo,monospace}}
code{{font-size:13px}}a{{color:#13306b}}.btn{{display:inline-block;background:#13306b;color:#fbf7ee;text-decoration:none;padding:9px 16px;border-radius:2px;margin:6px 8px 0 0}}.note{{color:#5e5546;font-size:13px}}.scroll{{overflow-x:auto}}</style></head>
<body><main><div class="brand">Africa Bonds Monitor</div>
<h1>{escape(t["title"])}</h1><p>{escape(t["lede"])}</p>
<p><a class="btn" href="../plateforme.html#offres">{escape(t["waitlist"])}</a><a class="btn" href="echantillon.csv" download>{escape(t["sample"].format(n=SAMPLE))}</a><a class="btn" href="auctions.csv" download>auctions.csv</a> · <a href="{other}.html" lang="{other}">{"English" if other == "en" else "Français"}</a></p>
<p class="note">{escape(t["free" if gated else "free_open"])}</p>
<h2>{escape(t["coverage"])}</h2><div class="scroll"><table><tr><th>{escape(t["country"])}</th><th class="r">{escape(t["n"])}</th><th>{escape(t["first"])}</th><th>{escape(t["last"])}</th></tr>{cov}</table></div>
<p class="note">{escape(t["update"].format(d=report.fmt_date(as_of, lang)))}</p>
<h2>{escape(t["files"])}</h2><ul><li>{escape(t["f_auctions"].format(n=len(tb["auctions"])))}</li><li>{escape(t["f_securities"].format(n=len(tb["securities"])))}</li><li>{escape(t["f_documents"].format(n=len(tb["documents"])))}</li></ul>
<h2>{escape(t["dict"])} (auctions.csv)</h2><div class="scroll"><table>{fields}</table></div>
<p class="note">{escape(t["legal"])}</p><p><a href="../plateforme.html">{escape(t["back"])}</a></p></main></body></html>"""


def write(as_of: date, dist: Path, private: Path = report.PRIVATE / "data", gated: bool = False) -> dict:
    tb = tables(as_of)
    pub = dist / "donnees"
    pub.mkdir(parents=True, exist_ok=True)
    # Sample: the most recent rows (one per country first, then by date), same columns as the full file.
    latest = sorted(tb["auctions"], key=lambda a: a["auction_date"], reverse=True)
    seen, sample = set(), []
    for a in latest:
        if a["country"] not in seen:
            seen.add(a["country"])
            sample.append(a)
    sample += [a for a in latest if a not in sample][: SAMPLE - len(sample)]
    (pub / "echantillon.csv").write_text(_csv(sample, AUCTION_COLS))
    for lang, t in DICT.items():
        (pub / f"{lang}.html").write_text(page(t, lang, tb, as_of, gated))
    # Free publication (authorisation scope): the full files are published too, behind the free
    # account (site/edge/gate.js covers /donnees/*.csv); a copy stays in the private folder.
    for name, rows, cols in (("auctions.csv", tb["auctions"], AUCTION_COLS), ("securities.csv", tb["securities"], SECURITY_COLS),
                             ("documents.csv", tb["documents"], DOC_COLS)):
        (pub / name).write_text(_csv(rows, cols))
    private.mkdir(parents=True, exist_ok=True)
    (private / "auctions.csv").write_text(_csv(tb["auctions"], AUCTION_COLS))
    (private / "securities.csv").write_text(_csv(tb["securities"], SECURITY_COLS))
    (private / "documents.csv").write_text(_csv(tb["documents"], DOC_COLS))
    (private / "LISEZMOI.txt").write_text(
        f"Africa Bonds Monitor - donnees d'adjudications UEMOA verifiees, au {as_of.isoformat()}.\n"
        "Source : comptes rendus officiels d'UMOA-Titres (lien et SHA-256 sur chaque ligne).\n"
        "Champs : voir dictionnaire.html sur la plateforme (donnees/fr.html).\n"
        "Valeurs : publiees (FACT), jamais calculees ni completees ; champ vide = statut dans field_status.\n")
    return {"auctions": len(tb["auctions"]), "securities": len(tb["securities"]), "documents": len(tb["documents"]),
            "countries": len(coverage(tb["auctions"])), "sample": len(sample), "page": {l: f"donnees/{l}.html" for l in DICT}}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--as-of", required=True, type=date.fromisoformat)
    p.add_argument("--dist", type=Path, default=report.ROOT / "dist")
    a = p.parse_args()
    print(write(a.as_of, a.dist))


if __name__ == "__main__":
    main()
