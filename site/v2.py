"""Redesigned pages (validated mock-up of 23/10/2026), published under /nouveau/.

    python site/v2.py --as-of 2026-10-23        (also called by build.py after write_api)

Accueil and the 13 country pages are rendered here (static HTML, no script needed); Marchés and
the security page (titre.html?isin=…) are rendered in the browser by nouveau/app.js from
nouveau/data.json. Every value is copied from the verified dataset (FACT); the few derived values
(totals, ratios, completeness) are labelled CALCUL. Nothing is estimated: an unpublished field is
shown as "non publié". XOF and XAF amounts are never added together.
"""

import argparse
import json
import shutil
from datetime import date, timedelta
from html import escape
from pathlib import Path

import dataset
import report

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
OUT = "nouveau"

COUNTRIES = {  # iso: (name, zone, currency, source)
    "BEN": ("Bénin", "UEMOA", "XOF", "UMOA-Titres"), "BFA": ("Burkina Faso", "UEMOA", "XOF", "UMOA-Titres"),
    "CIV": ("Côte d'Ivoire", "UEMOA", "XOF", "UMOA-Titres"), "GNB": ("Guinée-Bissau", "UEMOA", "XOF", "UMOA-Titres"),
    "MLI": ("Mali", "UEMOA", "XOF", "UMOA-Titres"), "NER": ("Niger", "UEMOA", "XOF", "UMOA-Titres"),
    "SEN": ("Sénégal", "UEMOA", "XOF", "UMOA-Titres"), "TGO": ("Togo", "UEMOA", "XOF", "UMOA-Titres"),
    "CMR": ("Cameroun", "CEMAC", "XAF", "BEAC"), "CAF": ("Centrafrique", "CEMAC", "XAF", "BEAC"),
    "COG": ("Congo", "CEMAC", "XAF", "BEAC"), "GAB": ("Gabon", "CEMAC", "XAF", "BEAC"),
    "GNQ": ("Guinée équatoriale", "CEMAC", "XAF", "BEAC"), "TCD": ("Tchad", "CEMAC", "XAF", "BEAC"),
}
MONTHS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]
KIND_LABEL = {"rendement": "rendement · UMOA-Titres", "prix": "prix % du nominal · BEAC", "précompté": "taux précompté · BEAC",
              "inconnu": "nature non reconnue"}


def kind(convention: str | None) -> str:
    """Nature of the published value, from the convention as published. Unknown is never a yield."""
    c = (convention or "").casefold()
    if "prix" in c:
        return "prix"
    if "précompté" in c or "precompte" in c:
        return "précompté"
    if "rendement" in c:
        return "rendement"
    return "inconnu"


def num(v) -> float | None:
    return None if v is None or v == "" else float(v)


def published_value(a: dict) -> float | None:
    return num(a["average_price"]) if kind(a["yield_convention"]) == "prix" else num(a["weighted_average_yield"])


def fr_num(v: float, dp: int = 2) -> str:
    s = f"{v:,.{dp}f}".replace(",", " ").replace(".", ",")
    return s.replace(" ", " ")


def fr_int(v: float) -> str:
    return f"{round(v):,}".replace(",", " ")


def fr_date(d: str, short: bool = True) -> str:
    y, m, j = d.split("-")
    return f"{j}/{m}/{y}" if short else f"{int(j)} {MONTHS[int(m) - 1]} {y}"


def md(v: float, cur: str) -> str:
    return f"{fr_num(v / 1e9)} Md {cur}"


def badge(b: str) -> str:
    cls = {"FAIT": "b-fact", "CALCUL": "b-calc"}.get(b, "b-nd")
    return f'<span class="badge {cls}">{escape(b)}</span>'


def instr_label(instr: str, zone: str) -> str:
    bill = instr == "treasury_bill"
    if instr not in ("treasury_bill", "treasury_bond"):
        return "Obligation cotée"
    return ("BTA (bon)" if bill else "OTA (obligation)") if zone == "CEMAC" else ("Bon du Trésor" if bill else "Obligation du Trésor")


def src_short(url: str) -> str:
    return "UMOA-Titres" if "umoatitres" in url else "BEAC" if "beac.int" in url else "BVMAC" if "bvm-ac" in url else "Source"


def shell(title: str, body: str, active: str = "", depth: int = 1, scripts: str = "") -> str:
    up = "../" * depth
    nav = [("marches", "Marchés", f"{up}{OUT}/marches.html"), ("comparer", "Comparer", f"{up}plateforme.html#comparer"),
           ("acces", "Accès officiel", f"{up}plateforme.html#acces"), ("methode", "Données &amp; méthode", f"{up}donnees/fr.html")]
    current = ' aria-current="page"'
    links = "".join(f'<a href="{href}"{current if key == active else ""}>{label}</a>' for key, label, href in nav)
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} — Africa Bonds Monitor</title>
<meta name="description" content="Adjudications UEMOA et CEMAC, cote BVMAC : chaque chiffre relié à son document officiel. Information uniquement.">
<link rel="icon" href="{up}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&amp;family=IBM+Plex+Sans:wght@400;500;600&amp;family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&amp;display=swap">
<link rel="stylesheet" href="{up}{OUT}/app.css">
{scripts}
</head>
<body>
<a class="skip" href="#contenu">Aller au contenu</a>
<header class="top">
<div class="wrap top-in">
<a class="brand" href="{up}{OUT}/"><span class="mark" aria-hidden="true">A</span><span>Africa Bonds Monitor</span></a>
<nav class="nav" aria-label="Navigation principale">{links}
<details class="more"><summary>Plus</summary><div class="more-menu">
<a href="{up}plateforme.html#rapports">Rapports</a><a href="{up}plateforme.html#simulateur">Simulateur</a>
<a href="{up}plateforme.html#brief">Brief du jour</a><a href="{up}plateforme.html#offres">Pilote institutionnel</a>
<a href="{up}plateforme.html">Plateforme complète (version actuelle)</a></div></details>
</nav>
</div>
</header>
<main id="contenu">
{body}
</main>
<footer class="foot"><div class="wrap foot-in">
<p>Information uniquement — aucun conseil en investissement. Africa Bonds Monitor n'est affilié à aucune institution source (UMOA-Titres, BEAC, BVMAC). Données publiées avec l'autorisation de publication gratuite des sources ; la revente n'est pas autorisée.</p>
<p><a href="{up}plateforme.html#methode">Méthode</a> · <a href="{up}plateforme.html#sources">Sources</a> · <a href="{up}api/v1/index.json">API JSON</a> · <a href="{up}donnees/fr.html">Données CSV</a></p>
</div></footer>
</body>
</html>
"""


def dots_chart(points: list[tuple[float, float, str]], x_max: float, y_min: float, y_max: float, y_step: float,
               x_ticks: list[float], label: str, y_fmt) -> str:
    """Observed points only, never joined (no interpolation). CSS-positioned, no script."""
    grid = "".join(f'<div class="gy" style="bottom:{100 * (v - y_min) / (y_max - y_min):.2f}%"><span>{y_fmt(v)}</span></div>'
                   for v in frange(y_min, y_max, y_step))
    xt = "".join(f'<span class="gx" style="left:{100 * v / x_max:.2f}%">{fr_num(v, 0)} a</span>' for v in x_ticks)
    pts = "".join(f'<div class="pt" style="left:{100 * x / x_max:.2f}%;bottom:{100 * (y - y_min) / (y_max - y_min):.2f}%">'
                  f'<span class="dot"></span><span class="pl">{escape(t)}</span></div>' for x, y, t in points)
    return f'<div class="chart" role="img" aria-label="{escape(label)}">{grid}{xt}{pts}</div>'


def frange(a: float, b: float, step: float) -> list[float]:
    out, v = [], a
    while v <= b + 1e-9:
        out.append(round(v, 6))
        v += step
    return out


def build_data(as_of: date, tb: dict, bvmac: dict, yield_points: dict) -> dict:
    data = json.loads(report.DATA.read_text())
    all_secs = {s["isin"]: s for s in data["securities"]}
    urls: list[str] = []
    uix: dict[str, int] = {}

    def u(url: str) -> int:
        if url not in uix:
            uix[url] = len(urls)
            urls.append(url)
        return uix[url]

    rows = []
    for a in sorted(tb["auctions"], key=lambda a: (a["auction_date"], a["isin"]), reverse=True):
        rows.append([a["auction_date"], a["country"], a["currency"], a["isin"], 1 if a["auction_type"] == "buyback" else 0,
                     num(a["amount_offered"]), num(a["amount_submitted"]), num(a["amount_allocated"]),
                     published_value(a), kind(a["yield_convention"]), num(a["cutoff_yield"]), num(a["number_of_bidders"]),
                     u(a["source_url"])])
    wanted = {r[3] for r in rows} | {b["isin"] for b in bvmac["bonds"]}
    secs = {}
    for isin in sorted(wanted):
        s = all_secs.get(isin)
        if not s:
            continue
        secs[isin] = [s["security_name"], s["instrument_type"], s["country"], s["currency"], s.get("issuer"),
                      num(s.get("face_value")), num(s.get("coupon_rate")), s.get("coupon_frequency"), s.get("issue_date"),
                      s.get("maturity_date"), s.get("tenor_days"), s.get("amortization"), s.get("listing_status"),
                      sorted(k for k, v in (s.get("field_status") or {}).items() if v == "not_disclosed"), u(s["source_url"])]
    return {"as_of": as_of.isoformat(), "countries": COUNTRIES,
            "fields": ["date", "iso", "cur", "isin", "buyback", "offered", "submitted", "allocated", "value", "kind", "cutoff", "bidders", "url"],
            "sec_fields": ["name", "instr", "iso", "cur", "issuer", "face", "coupon", "freq", "issue", "maturity", "tenor", "amort", "listing", "not_disclosed", "url"],
            "rows": rows, "secs": secs, "urls": urls, "bvmac": bvmac["bonds"], "yield_points": yield_points}


def home(d: dict, bvmac: dict) -> str:
    rows = d["rows"]
    n = len(rows)
    isos = sorted({r[1] for r in rows})
    n_uemoa = sum(1 for i in isos if COUNTRIES[i][1] == "UEMOA")
    first = min(r[0] for r in rows)
    kpis = [(fr_int(n), f"adjudications vérifiées depuis le {fr_date(first)}"),
            (str(len(isos)), f"pays avec résultats ({n_uemoa} UEMOA, {len(isos) - n_uemoa} CEMAC)"),
            (str(len(bvmac["bonds"])), "obligations cotées à la BVMAC"),
            (fr_date(d["as_of"], short=False), "date des données")]
    kp = "".join(f'<a class="kpi" href="marches.html"><span class="kv">{v}{badge("FAIT")}</span><span class="kl">{escape(l)}</span></a>' for v, l in kpis)
    latest = "".join(
        f'<tr><td class="mono">{fr_date(r[0])}</td><td><a href="pays/{r[1]}.html">{escape(COUNTRIES[r[1]][0])}</a></td>'
        f'<td><a href="titre.html?isin={r[3]}">{escape(instr_label(d["secs"].get(r[3], ["", ""])[1], COUNTRIES[r[1]][1]))}</a>'
        f'{" · rachat" if r[4] else ""}</td>'
        f'<td class="num">{"non publié" if r[8] is None else fr_num(r[8]) + " %"}<br><span class="kind">{KIND_LABEL[r[9]]}</span></td>'
        f'<td class="num">{md(r[7], r[2])}</td>'
        f'<td><a href="{escape(d["urls"][r[12]])}" aria-label="{escape(src_short(d["urls"][r[12]]))}, adjudication {escape(COUNTRIES[r[1]][0])} du {fr_date(r[0])} (PDF)">{src_short(d["urls"][r[12]])} (PDF)</a></td></tr>'
        for r in rows[:6])
    body = f"""
<section class="hero"><div class="wrap hero-in">
<p class="eyebrow">UEMOA · CEMAC · BVMAC — sources officielles</p>
<h1>Adjudications UEMOA et CEMAC, cote BVMAC — chaque chiffre relié à son document officiel.</h1>
<p class="lede">Pour les trésoreries, la gestion actif-passif et la gestion d'actifs : coûts d'émission des États, échéances connues, rendements du marché primaire. Information uniquement, sans recommandation.</p>
<div class="ctas"><a class="btn btn-gold" href="marches.html">Ouvrir les marchés →</a><a class="btn btn-ghost" href="../plateforme.html#offres">Rejoindre le pilote institutionnel</a></div>
</div></section>
<section class="wrap" aria-label="Indicateurs"><div class="kpis">{kp}</div>
<p class="small">Indicateurs calculés à chaque mise à jour à partir des données vérifiées — aucun chiffre saisi à la main.</p></section>
<section class="wrap block"><div class="row-head"><h2>Dernières adjudications</h2><a href="marches.html">Voir toutes les adjudications →</a></div>
<div class="table-box"><table><thead><tr><th scope="col">Date</th><th scope="col">Pays</th><th scope="col">Instrument</th><th scope="col" class="num">Valeur publiée</th><th scope="col" class="num">Montant retenu</th><th scope="col">Source</th></tr></thead>
<tbody>{latest}</tbody></table></div></section>
<section class="wrap block"><h2>Ce que la plateforme apporte à votre métier</h2><div class="cards3">
<div class="card"><h3>Trésorerie</h3><p>Suivre le coût d'emprunt des États adjudication par adjudication, avec le document officiel de chaque résultat.</p><a href="marches.html">Adjudications par pays →</a></div>
<div class="card"><h3>Gestion actif-passif</h3><p>Repérer les échéances connues et les maturités émises, pays par pays, sans confondre titres observés et encours total.</p><a href="pays/CIV.html">Échéances par pays →</a></div>
<div class="card"><h3>Gestion d'actifs</h3><p>Comparer les rendements publiés du marché primaire UEMOA par maturité ; prix et taux précomptés CEMAC présentés à part.</p><a href="pays/SEN.html">Rendements publiés →</a></div>
</div></section>
<section class="wrap block"><div class="card trust">
<div><h3>Sources officielles</h3><p>UMOA-Titres (UEMOA), BEAC et BVMAC (CEMAC). Chaque valeur renvoie au PDF publié et à son empreinte SHA-256.</p></div>
<div><h3>Contrôles automatiques</h3><p>Une valeur ambiguë est mise en attente, jamais devinée. Les valeurs calculées portent la mention CALCUL.</p></div>
<div><h3>Limites</h3><p>Couverture CEMAC partielle. La BEAC publie des prix (OTA) et des taux précomptés (BTA), pas des rendements. XOF et XAF ne sont jamais additionnés.</p></div>
</div></section>
<section class="wrap block"><div class="pilot">
<div><p class="eyebrow">Programme pilote institutionnel</p><h2>Trois mois gratuits pour une dizaine d'institutions de l'UEMOA et de la CEMAC.</h2>
<p>La plateforme complète, un rapport sur mesure et un point mensuel. En retour : deux entretiens. Sans engagement d'achat. Les données officielles restent gratuites.</p></div>
<a class="btn btn-gold" href="../plateforme.html#offres">Demander à rejoindre le pilote</a></div></section>
<section class="wrap block"><h2>Pays couverts</h2><div class="chips">{"".join(f'<a class="chip" href="pays/{i}.html">{escape(COUNTRIES[i][0])} <span>{COUNTRIES[i][1]}</span></a>' for i in isos)}</div></section>
"""
    return shell("Accueil", body, depth=1)


COMPLETENESS = [(5, "Montant offert"), (6, "Montant soumis"), (7, "Montant retenu"), (8, "Valeur publiée (rendement, prix ou taux)"),
                (10, "Taux marginal"), (11, "Nombre de soumissionnaires")]


def country_page(iso: str, d: dict, as_of: date) -> str:
    name, zone, cur, source = COUNTRIES[iso]
    rows = [r for r in d["rows"] if r[1] == iso]
    n = len(rows)
    first, last = min(r[0] for r in rows), max(r[0] for r in rows)
    since = (as_of - timedelta(days=365)).isoformat()
    year = [r for r in rows if r[0] > since and not r[4]]
    alloc12 = sum(r[7] or 0 for r in year)
    buybacks = sum(1 for r in rows if r[4])
    kp = [(fr_int(n), f"adjudications vérifiées (du {fr_date(first)} au {fr_date(last)})", "FAIT"),
          (fr_date(last), "dernière adjudication", "FAIT"),
          (md(alloc12, cur), f"retenu en émission sur 12 mois ({len(year)} adjudications, rachats exclus)", "CALCUL"),
          (fr_int(buybacks), "opérations de rachat enregistrées", "FAIT")]
    kpis = "".join(f'<div class="kpi"><span class="kv">{v}{badge(b)}</span><span class="kl">{escape(l)}</span></div>' for v, l, b in kp)
    yp = d["yield_points"].get(iso) or {}
    if yp:
        pts = sorted(((p["res"], p["y"], f'{fr_num(p["y"])} % · {fr_num(p["res"], 1)} a') for p in yp.values()), key=lambda t: t[0])
        ys = [p[1] for p in pts]
        y_min, y_max = max(0, int(min(ys)) - 1), int(max(ys)) + 1
        last_d = max(p["d"] for p in yp.values())
        curve = (dots_chart(pts, 10, y_min, y_max, 1, [0, 1, 3, 5, 7, 10],
                            "Rendements publiés : " + ", ".join(f"{fr_num(x, 1)} an(s) {fr_num(y)} %" for x, y, _ in pts),
                            lambda v: f"{fr_num(v, 0)} %")
                 + f'<p class="small">Maturité résiduelle en années (abscisse) · dernier rendement moyen pondéré publié par maturité, en % (ordonnée). '
                   f'Plus récente observation : {fr_date(last_d)}. Les points ne sont pas reliés : aucune valeur n\'est interpolée.</p>'
                 + "<ul class=\"srclist\">" + "".join(f'<li><a href="{escape(p["url"])}">{escape(p["src"])}, {fr_date(p["d"])} (PDF)</a> — {escape(p["name"])}</li>'
                                                     for p in sorted(yp.values(), key=lambda p: p["res"])) + "</ul>")
    else:
        curve = ('<div class="notice"><strong>Courbe non affichée.</strong> ' +
                 ("La BEAC publie un prix en % du nominal pour les OTA et un taux précompté pour les BTA, pas des rendements. "
                  "Les convertir supposerait des conditions de titre que la plateforme n'a pas toutes : aucune courbe n'est tracée."
                  if zone == "CEMAC" else "Pas assez de rendements publiés récents pour ce pays.") + "</div>")
    comp = ""
    for i, label in COMPLETENESS:
        pct = 100 * sum(1 for r in rows if r[i] is not None) / n
        tone = "hi" if pct >= 90 else "mid" if pct >= 40 else "lo"
        comp += (f'<div class="cp"><div class="cp-h"><span>{label}</span><span class="mono">{fr_num(pct, 1)} %</span></div>'
                 f'<div class="bar" aria-hidden="true"><div class="fill {tone}" style="width:{pct:.1f}%"></div></div></div>')
    offered = 100 * sum(1 for r in rows if r[5] is not None) / n
    comp_note = (f"Le montant offert n'est publié que pour {fr_num(offered, 1)} % des adjudications : le taux de couverture n'est calculé que dans ces cas."
                 if offered < 90 else "Couverture CEMAC partielle : seules les adjudications dont l'avis BEAC a pu être lu et vérifié figurent ici."
                 if zone == "CEMAC" else "")
    auc = "".join(
        f'<tr><td class="mono">{fr_date(r[0])}</td><td><a href="../titre.html?isin={r[3]}">{escape(instr_label(d["secs"].get(r[3], ["", ""])[1], zone))}</a>{" · rachat" if r[4] else ""}</td>'
        f'<td class="mono">{fr_date(d["secs"][r[3]][9]) if r[3] in d["secs"] and d["secs"][r[3]][9] else "—"}</td>'
        f'<td class="num">{"non publié" if r[8] is None else fr_num(r[8]) + " %"}<br><span class="kind">{KIND_LABEL[r[9]]}</span></td>'
        f'<td class="num">{md(r[7], cur)}</td>'
        f'<td><a href="{escape(d["urls"][r[12]])}" aria-label="{source}, adjudication {escape(name)} du {fr_date(r[0])} (PDF)">{source} (PDF)</a></td></tr>'
        for r in rows[:10])
    mats = sorted({(s[9], isin) for isin, s in d["secs"].items() if s[2] == iso and s[9] and s[9] >= as_of.isoformat()})[:8]
    mat = "".join(f'<li><a href="../titre.html?isin={isin}"><span>{escape(instr_label(d["secs"][isin][1], zone))}'
                  f'{(" " + fr_num(d["secs"][isin][6]) + " %") if d["secs"][isin][6] is not None else ""}</span>'
                  f'<span class="mono small">{isin}</span></a><span class="mono">{fr_date(m)}</span></li>' for m, isin in mats) or "<li>Aucune échéance future connue.</li>"
    bonds = [b for b in d["bvmac"] if b["country"] == iso]
    bv = ""
    if bonds:
        bv = ('<section class="block"><h2>Obligations cotées à la BVMAC</h2><ul class="mlist">' +
              "".join(f'<li><a href="../titre.html?isin={b["isin"]}"><span>{escape(b["name"])}</span><span class="mono small">{b["isin"]}</span></a>'
                      f'<span class="small">{len(b["trades"])} jour(s) de transaction</span></li>' for b in bonds) + "</ul></section>")
    method = ("Comptes rendus d'adjudication publiés par UMOA-Titres, lus automatiquement et vérifiés ; une valeur ambiguë est mise en attente. Les rendements sont ceux publiés, jamais recalculés."
              if zone == "UEMOA" else
              "Communiqués de résultats publiés par la BEAC, lus automatiquement (OCR si nécessaire) et vérifiés. Les valeurs sont des prix (OTA) ou des taux précomptés (BTA), affichés tels que publiés.")
    body = f"""
<div class="wrap page">
<p class="crumbs"><a href="../">Accueil</a> / <a href="../marches.html">Marchés</a> / {escape(name)}</p>
<div class="row-head"><div><h1>{escape(name)}</h1><p class="sub">{zone} · monnaie {cur} · source {source}</p></div>
<a class="btn btn-line" href="../marches.html?pays={iso}">Toutes les adjudications du pays</a></div>
<div class="kpis kpis-in">{kpis}</div>
<div class="two">
<section class="card grow"><div class="row-head"><h2>Rendements publiés par maturité</h2><span class="small">Points observés, non interpolés</span></div>{curve}</section>
<section class="card side"><h2>Complétude des données</h2><p class="small">Part des adjudications où la source publie le champ. {badge("CALCUL")}</p>{comp}<p class="small">{comp_note}</p></section>
</div>
<div class="two">
<section class="grow"><h2>Dernières adjudications</h2><div class="table-box"><table><thead><tr><th scope="col">Date</th><th scope="col">Instrument</th><th scope="col">Échéance</th><th scope="col" class="num">Valeur publiée</th><th scope="col" class="num">Retenu</th><th scope="col">Source</th></tr></thead><tbody>{auc}</tbody></table></div></section>
<section class="card side"><h2>Prochaines échéances connues</h2><p class="small">Titres observés dans les adjudications publiées. Ce n'est pas l'encours total de la dette : les montants restant dus ne sont pas publiés ici.</p><ul class="mlist">{mat}</ul></section>
</div>
{bv}
<div class="notice"><strong>Sources et méthode.</strong> {method}</div>
</div>
"""
    return shell(f"Marché {name}", body, active="marches", depth=2)


def write(as_of: date, dist: Path, bvmac: dict, yield_points: dict) -> dict:
    tb = dataset.tables(as_of)
    d = build_data(as_of, tb, bvmac, yield_points)
    out = dist / OUT
    if out.exists():
        shutil.rmtree(out)
    (out / "pays").mkdir(parents=True)
    (out / "data.json").write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":"), allow_nan=False))
    shutil.copy(ROOT / "nouveau" / "app.css", out / "app.css")
    shutil.copy(ROOT / "nouveau" / "app.js", out / "app.js")
    (out / "index.html").write_text(home(d, bvmac))
    isos = sorted({r[1] for r in d["rows"]})
    for iso in isos:
        (out / "pays" / f"{iso}.html").write_text(country_page(iso, d, as_of))
    js = '<script src="app.js" defer></script>'
    (out / "marches.html").write_text(shell("Marchés", '<div id="app" class="wrap page" data-page="marches"><p>Chargement des adjudications…</p>'
                                            '<noscript>Cette page a besoin de JavaScript. Les fichiers complets sont disponibles en <a href="../donnees/fr.html">CSV</a>.</noscript></div>',
                                            active="marches", depth=1, scripts=js))
    (out / "titre.html").write_text(shell("Fiche titre", '<div id="app" class="wrap page" data-page="titre"><p>Chargement du titre…</p>'
                                          '<noscript>Cette page a besoin de JavaScript.</noscript></div>', active="marches", depth=1, scripts=js))
    return {"pages": 4 + len(isos) - 1, "countries": len(isos), "auctions": len(d["rows"]), "securities": len(d["secs"])}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--as-of", required=True)
    a = p.parse_args()
    as_of = date.fromisoformat(a.as_of)
    import build
    print(write(as_of, DIST, build.bvmac_quotes(as_of), build.yield_points(as_of)))


if __name__ == "__main__":
    main()
