"""Render the ARVI pilot dashboard (static HTML, no JavaScript) from backend/var/arvi/indicators.json.

Pages: /pilote/ (overview, latest year per country and resource) and /pilote/<iso>-<resource>/
(time series, unit values, export structure, partner-level cells with confidence).
No bulk download is offered: UN Comtrade data may not be re-disseminated as raw data without
UNSD permission (docs/arvi/DATA_SOURCES.md).
"""

from __future__ import annotations

import html
from decimal import Decimal
from pathlib import Path

E = html.escape
LEVEL_FR = {"high": ("🟢", "Élevée"), "medium": ("🟡", "Moyenne"), "low": ("🔴", "Faible")}
STATUS_FR = {"complete": "Appariée", "export_only": "Exportateur seul",
             "import_only": "Partenaire seul"}


def num(v: str | None) -> Decimal | None:
    return None if v is None else Decimal(v)


def _fr(x: Decimal, dp: int) -> str:
    s = f"{x:,.{dp}f}"
    return s.replace(",", " ").replace(".", ",")


def usd(v: str | Decimal | None) -> str:
    if v is None:
        return "—"
    d = Decimal(v)
    a = abs(d)
    if a >= Decimal("1e9"):
        return f"{_fr(d / Decimal('1e9'), 2)} Md$"
    if a >= Decimal("1e6"):
        return f"{_fr(d / Decimal('1e6'), 1)} M$"
    if a >= Decimal("1e3"):
        return f"{_fr(d / Decimal('1e3'), 0)} k$"
    return f"{_fr(d, 0)} $"


def declared(v: str | None) -> str:
    return "<small>Non déclaré</small>" if v is None else usd(v)


def pct(v: str | None, signed: bool = False) -> str:
    if v is None:
        return "—"
    d = Decimal(v) * 100
    s = _fr(d, 1)
    return f"{'+' if signed and d > 0 else ''}{s} %"


def per_t(v: str | None) -> str:
    return "—" if v is None else f"{_fr(Decimal(v), 0)} $/t"


def tonnes(v: str | None) -> str:
    return "—" if v is None else f"{_fr(Decimal(v), 0)} t"


def badge(level: str, score: int | None = None) -> str:
    icon, label = LEVEL_FR[level]
    sc = f" · {score}" if score is not None else ""
    return f'<span class="conf conf-{level}">{icon} {label}{sc}</span>'


def page(title: str, desc: str, kicker: str, h1: str, lede: str, body: str, meta: dict,
         back: str = "/") -> str:
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="robots" content="noindex">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%230e2148'/%3E%3Cpath d='M6 24h20M9 24V15M16 24V10M23 24V6' stroke='%23c9a24a' stroke-width='3' stroke-linecap='round'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Marcellus&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css"></head><body>
<header class="hero"><div class="wrap">
<div class="kicker">{E(kicker)}</div><h1>{E(h1)}</h1><p>{lede}</p>
<div class="notice">Données déclarées à UN Comtrade, {meta['years'][0]}–{meta['years'][-1]}, consultées du {E(meta['first_fetch'][:10])} au {E(meta['last_fetch'][:10])}. Indicateurs CALCULÉS (aucun paramètre modélisé). Un écart entre deux déclarations n'est ni une preuve de fraude ni une perte avérée.</div>
<nav class="topnav" aria-label="Navigation"><a href="{back}">← Retour</a><a href="/pilote/">Vue d'ensemble du pilote</a><a href="/">Indicateurs pour la décision</a><a href="/blueprint/">Blueprint</a></nav>
</div></header>
<main class="wrap dec">{body}</main>
<footer><div class="wrap">Source : UN Comtrade, Division de statistique des Nations unies (<a href="https://comtradeplus.un.org/">comtradeplus.un.org</a>), API publique ; {meta['responses']} réponses archivées avec leur empreinte SHA-256. Méthode ARVI {E(meta['methodology_version'])}. Les données brutes ne sont pas redistribuées. Information et analyse uniquement.</div></footer>
</body></html>"""


def latest(results: list[dict], country: str, resource: str) -> dict | None:
    rs = [r for r in results if r["country"] == country and r["resource"] == resource]
    return max(rs, key=lambda r: r["year"]) if rs else None


def chart(series: list[dict]) -> str:
    """Grouped bars per year: exports declared by the country vs partners' mirror imports."""
    w, h, left, bottom, top = 640, 260, 86, 28, 12
    vals = [num(r["arvi1"][k]) or Decimal(0) for r in series for k in ("x_total", "m_total")]
    vmax = max(vals) if vals and max(vals) > 0 else Decimal(1)
    # Round the axis max up to a "nice" number.
    mag = Decimal(10) ** (len(str(int(vmax))) - 1)
    nice = next(m * mag for m in (Decimal(1), Decimal(2), Decimal("2.5"), Decimal(5), Decimal(10)) if m * mag >= vmax)
    plot_h, plot_w = h - bottom - top, w - left - 8
    slot = plot_w / len(series)
    bw = min(28.0, slot * 0.32)
    parts = [f'<svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-label="Exportations déclarées et importations miroir par année">']
    for i in range(5):
        v = nice * i / 4
        y = top + plot_h - float(v / nice) * plot_h
        parts.append(f'<line class="grid" x1="{left}" x2="{w - 8}" y1="{y:.1f}" y2="{y:.1f}"/>'
                     f'<text class="axis" x="{left - 8}" y="{y + 4:.1f}" text-anchor="end">{E(usd(v))}</text>')
    for i, r in enumerate(series):
        cx = left + slot * i + slot / 2
        for j, (key, cls, label) in enumerate((("x_total", "s1", "Exportations déclarées"),
                                               ("m_total", "s2", "Importations miroir"))):
            raw = r["arvi1"][key]
            if raw is None:  # not declared: no bar, never a zero
                continue
            v = num(raw)
            bh = float(v / nice) * plot_h
            x = cx - bw - 1 + j * (bw + 2)
            y = top + plot_h - bh
            # 4px rounded data end, square at the baseline.
            rr = min(4.0, bh / 2, bw / 2)
            path = (f"M{x:.1f},{top + plot_h:.1f} V{y + rr:.1f} Q{x:.1f},{y:.1f} {x + rr:.1f},{y:.1f} "
                    f"H{x + bw - rr:.1f} Q{x + bw:.1f},{y:.1f} {x + bw:.1f},{y + rr:.1f} V{top + plot_h:.1f} Z")
            parts.append(f'<g class="bar"><rect class="hit" x="{x - 2:.1f}" y="{top}" width="{bw + 4:.1f}" height="{plot_h}"/>'
                         f'<path class="{cls}" d="{path}"/><title>{r["year"]} · {label} : {E(usd(v))}</title></g>')
        parts.append(f'<text class="axis" x="{cx:.1f}" y="{h - 8}" text-anchor="middle">{r["year"]}</text>')
    parts.append(f'<line class="base" x1="{left}" x2="{w - 8}" y1="{top + plot_h}" y2="{top + plot_h}"/></svg>')
    legend = ('<div class="legend"><span><i class="sw s1"></i>Exportations déclarées par le pays</span>'
              '<span><i class="sw s2"></i>Importations déclarées par les partenaires (miroir)</span></div>')
    return legend + "".join(parts)


def overview(data: dict) -> str:
    meta, res = data["meta"], data["results"]
    rows = []
    for iso, c in data["countries"].items():
        for rk in c["resources"]:
            r = latest(res, iso, rk)
            if r is None:
                rows.append(f"<tr><td>{E(c['name_fr'])}</td><td>{E(data['resources'][rk]['name_fr'])}</td>"
                            f"<td colspan='8'>Aucune déclaration disponible pour {meta['years'][0]}–{meta['years'][-1]}</td></tr>")
                continue
            a1, a3 = r["arvi1"], r["arvi3"]
            rows.append(
                f"<tr><td><a href='/pilote/{iso.lower()}-{rk}/'>{E(c['name_fr'])}</a></td>"
                f"<td>{E(data['resources'][rk]['name_fr'])}</td><td class='n'>{r['year']}</td>"
                f"<td class='n'>{declared(a1['x_total'])}</td><td class='n'>{declared(a1['m_total'])}</td>"
                f"<td class='n'>{usd(a1['gap_total'])}<br><small>{pct(a1['rel_gap_total'], True)}</small></td>"
                f"<td class='n'>{pct(a1['complete_share'])}</td>"
                f"<td class='n'>{pct(a3['lowest_share_x'])} / {pct(a3['lowest_share_m'])}</td>"
                f"<td>{badge(r['confidence']['level'], r['confidence']['score'])}</td></tr>")
    body = f"""
<section><h2>Dernière année disponible, par pays et ressource</h2>
<p class="lede">X = exportations déclarées par le pays (FAB). M = importations déclarées par ses partenaires en provenance de ce pays (le plus souvent CAF, donc normalement un peu plus élevées). Cliquez sur un pays pour le détail par année et par partenaire.</p>
<div class="table-scroll"><table>
<thead><tr><th>Pays</th><th>Ressource</th><th>Année</th><th>X déclaré (ARVI-1)</th><th>M miroir (ARVI-1)</th><th>Écart M − X</th><th>Part appariée</th><th>Stade brut X / M (ARVI-3)</th><th>Confiance</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
<p class="lede"><b>Part appariée</b> : part de la valeur des flux où les deux côtés déclarent. <b>Stade brut</b> : part de la valeur au stade le moins transformé (minerai, grumes), selon l'exportateur (X) et selon les partenaires (M).</p>
</section>
<section><h2>Comment lire ces chiffres</h2><ul class="rules">
<li><b>Un écart positif modéré est attendu</b> : les importations incluent fret et assurance (CAF). Un écart relatif entre 0 et +10 % est signalé comme compatible avec ces coûts <span class="flag hyp">[HYPOTHÈSE]</span>.</li>
<li><b>Exportateur seul / partenaire seul</b> : un seul des deux pays déclare le flux. C'est d'abord une lacune de données, pas un écart.</li>
<li><b>Confiance faible : aucune conclusion.</b> Elle signale surtout des déclarations manquantes, des quantités incohérentes ou des pays de transit.</li>
<li><b>Pays enclavés et plateformes de négoce</b> (Suisse, Émirats, Pays-Bas, Belgique, Singapour, Hong Kong) : le partenaire déclaré diffère souvent d'un côté à l'autre.</li>
</ul></section>
<section><h2>Indicateurs non publiés</h2>
<p class="lede">ARVI-4 (enjeu fiscal), ARVI-5 (valeur ajoutée locale) et ARVI-6 (équivalents d'investissement) exigent des paramètres sourcés (taux fiscaux, coûts de transformation, teneurs, coûts unitaires) qui ne sont pas encore collectés. Ils ne sont pas publiés plutôt qu'estimés sans source.</p></section>"""
    return page("ARVI Pilote", "Résultats du pilote ARVI : écarts miroir, structure des exportations et confiance, à partir des déclarations UN Comtrade.",
                "ARVI · Pilote · données réelles", "Résultats du pilote",
                f"{len(data['countries'])} pays, {len(data['resources'])} ressources, {meta['flows']} flux déclarés, {meta['cells']} paires exportateur–partenaire–produit–année.",
                body, meta)


def detail(data: dict, iso: str, rk: str) -> str:
    meta = data["meta"]
    c, resource = data["countries"][iso], data["resources"][rk]
    series = sorted((r for r in data["results"] if r["country"] == iso and r["resource"] == rk),
                    key=lambda r: r["year"])
    name = f"{c['name_fr']} · {resource['name_fr']}"
    if not series:
        return page(f"ARVI {name}", name, "ARVI · Pilote", name, "Aucune déclaration disponible.", "", meta, "/pilote/")
    yrows = "".join(
        f"<tr><td class='n'>{r['year']}</td><td class='n'>{declared(r['arvi1']['x_total'])}</td><td class='n'>{declared(r['arvi1']['m_total'])}</td>"
        f"<td class='n'>{usd(r['arvi1']['gap_total'])}</td><td class='n'>{pct(r['arvi1']['rel_gap_total'], True)}</td>"
        f"<td class='n'>{usd(r['arvi1']['complete_positive'])}</td><td class='n'>{usd(r['arvi1']['complete_negative'])}</td>"
        f"<td class='n'>{usd(r['arvi1']['export_only'])}</td><td class='n'>{usd(r['arvi1']['import_only'])}</td>"
        f"<td class='n'>{pct(r['arvi1']['complete_share'])}</td><td>{badge(r['confidence']['level'], r['confidence']['score'])}</td></tr>"
        for r in series)
    last = series[-1]
    a2 = "".join(
        f"<tr><td class='n'>{r['year']}</td><td>{E(u['stage'])} <small>SH {E(u['hs'])}</small></td><td class='n'>{per_t(u['uv_x'])}</td>"
        f"<td class='n'>{per_t(u['uv_m'])}</td><td class='n'>{pct(str(Decimal(u['ratio']) - 1), True)}</td><td class='n'>{u['cells']}</td></tr>"
        for r in series for u in r["arvi2"]) or "<tr><td colspan='6'>Aucune paire avec quantités déclarées des deux côtés.</td></tr>"
    a3 = "".join(
        f"<tr><td>{s['order']}. {E(s['stage'])}</td>" + "".join(
            f"<td class='n'>{pct(r['arvi3']['by_stage'][s['order'] - 1]['share_x'])}<br><small>{pct(r['arvi3']['by_stage'][s['order'] - 1]['share_m'])}</small></td>"
            for r in series) + "</tr>"
        for s in last["arvi3"]["by_stage"])
    partners = data["partners"]
    cells = [x for x in last["cells"]][:20]
    crow = "".join(
        f"<tr><td>{E(partners.get(x['partner'], x['partner']))}</td><td>SH {E(x['hs'])}</td><td>{STATUS_FR[x['status']]}</td>"
        f"<td class='n'>{usd(x['x'])}</td><td class='n'>{usd(x['m'])}</td><td class='n'>{pct(x['rel_gap'], True)}"
        f"{' <small>(CAF/FAB)</small>' if x['cif_fob_band'] else ''}</td><td class='n'>{tonnes(x['x_t'])}<br><small>{tonnes(x['m_t'])}</small></td>"
        f"<td>{badge(x['level'], x['score'])}<br><small>{E(' · '.join(x['reasons']))}</small></td></tr>"
        for x in cells)
    body = f"""
<section><h2>ARVI-1 · Écart miroir par année</h2>
<p class="lede">Exportations déclarées par {E(c['name_fr'])} et importations déclarées par ses partenaires, toutes étapes de la chaîne confondues. Survolez une barre pour sa valeur.</p>
{chart(series)}
<div class="table-scroll"><table><thead><tr><th>Année</th><th>X déclaré</th><th>M miroir</th><th>Écart M − X</th><th>%</th><th>Écarts + (appariés)</th><th>Écarts − (appariés)</th><th>Exportateur seul</th><th>Partenaire seul</th><th>Part appariée</th><th>Confiance</th></tr></thead><tbody>{yrows}</tbody></table></div>
<p class="lede">Les écarts positifs et négatifs des paires appariées sont additionnés séparément : un total net masquerait des écarts opposés qui se compensent.</p></section>
<section><h2>ARVI-2 · Prix unitaire (USD par tonne)</h2>
<p class="lede">Sur les seules paires où les deux pays déclarent valeur et poids. Un prix miroir supérieur de 0 à 10 % est cohérent avec le fret et l'assurance. Sans la teneur en métal, un prix bas peut refléter un produit moins riche.</p>
<div class="table-scroll"><table><thead><tr><th>Année</th><th>Stade</th><th>Prix déclaré à l'export</th><th>Prix miroir</th><th>Écart</th><th>Paires</th></tr></thead><tbody>{a2}</tbody></table></div></section>
<section><h2>ARVI-3 · Structure des exportations le long de la chaîne</h2>
<p class="lede">Part de la valeur exportée à chaque stade, selon {E(c['name_fr'])} (chiffre du haut) et selon ses partenaires (en petit). Part en valeur, pas en métal contenu : les teneurs ne sont pas encore collectées.</p>
<div class="table-scroll"><table><thead><tr><th>Stade</th>{''.join(f'<th>{r["year"]}</th>' for r in series)}</tr></thead><tbody>{a3}</tbody></table></div></section>
<section><h2>Par partenaire · {last['year']}</h2>
<p class="lede">Les 20 paires partenaire–produit les plus importantes. Poids : déclaré par {E(c['name_fr'])} (haut) et par le partenaire (bas). La confiance indique jusqu'où un écart peut fonder une action ; ses trois principales raisons sont affichées.</p>
<div class="table-scroll"><table><thead><tr><th>Partenaire</th><th>Produit</th><th>Déclaration</th><th>X</th><th>M</th><th>Écart</th><th>Poids</th><th>Confiance</th></tr></thead><tbody>{crow}</tbody></table></div></section>"""
    return page(f"ARVI {name}", f"ARVI pilote : {name}, écarts miroir {meta['years'][0]}–{meta['years'][-1]}.",
                f"ARVI · Pilote · {c['name_fr']}", name,
                f"Confiance {last['year']} : {badge(last['confidence']['level'], last['confidence']['score'])}",
                body, meta, "/pilote/")


def render(data: dict, dist: Path) -> int:
    out = dist / "pilote"
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(overview(data), encoding="utf-8")
    n = 1
    for iso, c in data["countries"].items():
        for rk in c["resources"]:
            d = out / f"{iso.lower()}-{rk}"
            d.mkdir(exist_ok=True)
            (d / "index.html").write_text(detail(data, iso, rk), encoding="utf-8")
            n += 1
    return n
