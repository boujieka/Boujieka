"""PDF report of a calculation run (FR/EN), drawn with reportlab.

Contents: identification and status, alerts, indicators with their workbook
source, four charts, an annual summary table, workbook checks, key assumptions
and lots. Every figure comes from the stored run; nothing is recomputed here.
"""
from __future__ import annotations

import datetime as dt
import io
import math

from reportlab.graphics.shapes import Drawing, Line, PolyLine, Rect, String
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

from ..engine import ENGINE_VERSION
from .labels import (CHECKS_EN, CHECKS_FR, field_entries, kpi_label, labels, series_label, source_label,
                     translate_message, unit_label)

# reference data-viz palette (validated: categorical slots 1-3 on the light surface)
SERIES_COLORS = ["#2a78d6", "#eb6834", "#1baf7a"]
INK, INK2, MUTED = colors.HexColor("#0b0b0b"), colors.HexColor("#52514e"), colors.HexColor("#898781")
GRID, AXIS = colors.HexColor("#e1e0d9"), colors.HexColor("#c3c2b7")
GOOD, WARNING, CRITICAL = colors.HexColor("#0ca30c"), colors.HexColor("#fab219"), colors.HexColor("#d03b3b")
HEAD_BG = colors.HexColor("#eef2f6")

TXT = {
    "fr": dict(title="Rapport de calcul", project="Projet", country="Pays", scenario="Scénario", vstatus="Statut de la version",
               status="Statut du calcul", engine="Version du moteur", hash="Empreinte des hypothèses", generated="Généré le",
               reconciled="Moteur rapproché (options fidèles, solveur des macros)",
               variant="Variante : options ou solveur différents du classeur de référence",
               alerts="Alertes", none="Aucune", kpis="Indicateurs", label="Indicateur", value="Valeur", unit="Unité",
               source="Source", flag="Statut", derived="dérivé", experimental="expérimental", charts="Graphiques",
               c1="Recettes, charges et EBE", c2="CFADS et service de la dette", c3="Encours de dette et réserves",
               c4="DSCR annuel (dérivé) et cible", target="Cible", annual="Synthèse annuelle", checks="Contrôles du classeur",
               ok="OK", fail="ÉCHEC", assumptions="Hypothèses principales", lots="Sites et lots", page="Page",
               disclaimer="Outil d'analyse. Ni certification BAD, Banque mondiale ou CrossBoundary, ni avis juridique, "
                          "fiscal ou d'investissement. Les résultats dépendent des hypothèses saisies.",
               failed_check="Contrôle non satisfait", failed_run="Calcul en échec",
               thousands="Montants en milliers de la devise du modèle.", options="Options", solver="Solveur",
               note_amounts="Montants dans la devise du modèle."),
    "en": dict(title="Calculation report", project="Project", country="Country", scenario="Scenario", vstatus="Version status",
               status="Run status", engine="Engine version", hash="Inputs hash", generated="Generated on",
               reconciled="Reconciled engine (faithful options, macro solver)",
               variant="Variant: options or solver differ from the reference workbook",
               alerts="Alerts", none="None", kpis="Indicators", label="Indicator", value="Value", unit="Unit",
               source="Source", flag="Status", derived="derived", experimental="experimental", charts="Charts",
               c1="Revenue, opex and EBITDA", c2="CFADS and debt service", c3="Debt outstanding and reserves",
               c4="Annual DSCR (derived) and target", target="Target", annual="Annual summary", checks="Workbook checks",
               ok="OK", fail="FAIL", assumptions="Key assumptions", lots="Sites and lots", page="Page",
               disclaimer="Analysis tool. Not a certification by AfDB, the World Bank or CrossBoundary, nor legal, tax "
                          "or investment advice. Results depend on the assumptions entered.",
               failed_check="Check not satisfied", failed_run="Calculation failed",
               thousands="Amounts in thousands of the model currency.", options="Options", solver="Solver",
               note_amounts="Amounts in the model currency."),
}

CHART_NAMES = {
    "fr": {"revenue": "Recettes", "total_opex": "Charges d'exploitation", "ebitda": "EBE", "cfads": "CFADS",
           "debt_service": "Service de la dette", "senior_debt_balance": "Dette senior", "refi_debt_balance": "Dette refinancée",
           "dsra_balance": "DSRA"},
    "en": {"revenue": "Revenue", "total_opex": "Opex", "ebitda": "EBITDA", "cfads": "CFADS", "debt_service": "Debt service",
           "senior_debt_balance": "Senior debt", "refi_debt_balance": "Refinanced debt", "dsra_balance": "DSRA"},
}

SUMMARY_ROWS = ["revenue", "total_opex", "ebitda", "npat", "cfads", "debt_service", "dscr", "senior_debt_balance",
                "dsra_balance", "distributions", "project_cash_flow"]
KEY_ASSUMPTIONS = ["currency.case", "timing.construction_start", "timing.lifetime_years", "debt.sizing_method",
                   "debt.gearing", "debt.target_dscr", "debt.tenor_years", "debt.grace_years", "debt.rate_choice",
                   "refi.on", "reserves.dsra_on", "reserves.dsra_months", "tax.corporate_rate", "tax.vat_rate",
                   "funding.wacc", "macro.inflation", "demand.consumption_case"]


def fmt_value(v, unit: str, lang: str) -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "–"
    if isinstance(v, str):
        return v
    if isinstance(v, bool):
        v = int(v)
    if abs(v) < 0.005 and not unit.startswith("%") and unit != "x":
        v = 0          # no "-0,00" for floating-point residues
    if isinstance(v, int) and not unit.startswith("%") and unit != "x":
        s = f"{v:,d}"
        return s.replace(",", " ") if lang == "fr" else s
    if unit.startswith("%"):
        s = f"{v * 100:,.2f} %"
    elif unit == "x":
        s = f"{v:,.2f} x"
    elif v == int(v) and abs(v) < 1e15 and unit not in ("currency",) and not unit.startswith("currency"):
        s = f"{int(v):,d}"
    elif unit in ("year", "date"):
        return str(v)
    elif abs(v) >= 100:
        s = f"{v:,.0f}"
    else:
        s = f"{v:,.2f}"
    if lang == "fr":
        s = s.replace(",", " ").replace(".", ",")
    return s


def _short(v: float, lang: str) -> str:
    a = abs(v)
    for div, suf in ((1e9, "G" if lang == "fr" else "B"), (1e6, "M"), (1e3, "k")):
        if a >= div:
            s = f"{v / div:.2f}".rstrip("0").rstrip(".") + suf
            return s.replace(".", ",") if lang == "fr" else s
    s = f"{v:.0f}" if a >= 10 else f"{v:.2f}".rstrip("0").rstrip(".")
    return s.replace(".", ",") if lang == "fr" else s


def _nice_ticks(lo: float, hi: float, n: int = 5) -> list[float]:
    if hi == lo:
        hi = lo + 1
    raw = (hi - lo) / n
    mag = 10 ** math.floor(math.log10(raw))
    step = min((s * mag for s in (1, 2, 2.5, 5, 10) if s * mag >= raw), default=10 * mag)
    ticks = [round(math.floor(lo / step) * step, 10)]
    while ticks[-1] < hi - 1e-12:           # the axis always reaches the data maximum
        ticks.append(round(ticks[-1] + step, 10))
    if len(ticks) == 1:
        ticks.append(round(ticks[0] + step, 10))
    return ticks


def line_chart(years, lines, lang, width=250 * mm, height=70 * mm, ref=None, ref_label="", cap=None):
    """One-axis line chart: lines = [(label, values)], colours in fixed slot order. Values above ``cap``
    are drawn at the cap and labelled with their real value, so one outlier does not flatten the rest."""
    d = Drawing(width, height)
    over = []
    if cap is not None:
        clipped = []
        for label, vs in lines:
            over += [(i, v) for i, v in enumerate(vs) if v is not None and v > cap]
            clipped.append((label, [min(v, cap) if v is not None else None for v in vs]))
        lines = clipped
    left, right, top, bottom = 18 * mm, 30 * mm, 8 * mm, 10 * mm
    pw, ph = width - left - right, height - top - bottom
    vals = [v for _, vs in lines for v in vs if v is not None]
    if ref is not None:
        vals.append(ref)
    if not vals:
        return d
    lo, hi = min(0.0, min(vals)), max(0.0, max(vals))
    ticks = _nice_ticks(lo, hi)
    lo, hi = ticks[0], ticks[-1]
    n = len(years)
    x = lambda i: left + (pw * i / max(n - 1, 1))  # noqa: E731
    y = lambda v: bottom + ph * (v - lo) / (hi - lo)  # noqa: E731
    for tv in ticks:
        d.add(Line(left, y(tv), left + pw, y(tv), strokeColor=AXIS if tv == 0 else GRID, strokeWidth=0.8 if tv == 0 else 0.4))
        d.add(String(left - 2, y(tv) - 2.5, _short(tv, lang), fontName="Helvetica", fontSize=6.5, fillColor=MUTED,
                     textAnchor="end"))
    step = max(1, round(n / 12))
    for i in range(0, n, step):
        d.add(String(x(i), bottom - 9, str(years[i]), fontName="Helvetica", fontSize=6.5, fillColor=MUTED,
                     textAnchor="middle"))
    if ref is not None:
        d.add(Line(left, y(ref), left + pw, y(ref), strokeColor=INK2, strokeWidth=0.8, strokeDashArray=[3, 2]))
        d.add(String(left + pw + 3, y(ref) - 2.5, f"{ref_label} {fmt_value(ref, 'x', lang)}", fontName="Helvetica",
                     fontSize=7, fillColor=INK2))
    for i, v in over:
        d.add(String(x(i), y(hi) + 3, ("hors échelle : " if lang == "fr" else "off scale: ") + fmt_value(v, "x", lang), fontName="Helvetica", fontSize=6.5,
                     fillColor=INK2, textAnchor="middle"))
    label_y = []
    for k, (label, vs) in enumerate(lines):
        col = colors.HexColor(SERIES_COLORS[k % len(SERIES_COLORS)])
        seg = []
        for i, v in enumerate(vs):
            if v is None:
                if len(seg) > 1:
                    d.add(PolyLine(seg, strokeColor=col, strokeWidth=1.6))
                seg = []
            else:
                seg += [x(i), y(v)]
        if len(seg) > 1:
            d.add(PolyLine(seg, strokeColor=col, strokeWidth=1.6))
        last = next((i for i in range(n - 1, -1, -1) if vs[i] is not None), None)
        if last is not None:   # direct label at the line end (identity not by colour alone)
            ly = y(vs[last])
            while any(abs(ly - o) < 8 for o in label_y):
                ly += 8
            label_y.append(ly)
            d.add(Rect(x(last) + 3, ly - 1, 5, 2.2, fillColor=col, strokeColor=None))
            d.add(String(x(last) + 10, ly - 2.5, label, fontName="Helvetica", fontSize=7, fillColor=INK))
    return d


def dscr_repaying(series, a: int, b: int) -> list:
    """DSCR of repayment years only: a stub year with a tiny residual debt service would otherwise
    give a huge ratio and flatten the covenant breach into the axis."""
    d = series["dscr"]["values"][a:b + 1]
    flag = series.get("repayment_flag", {}).get("values")
    return d if flag is None else [v if f else None for v, f in zip(d, flag[a:b + 1])]


def _window(series) -> tuple[int, int]:
    """Years with activity (operations or debt), so charts skip the empty tail of the timeline."""
    active = [t for t, (o, c, b) in enumerate(zip(series["operations_flag"]["values"],
                                                   series["construction_flag"]["values"],
                                                   series["senior_debt_balance"]["values"]))
              if (o or c or (b or 0) > 1e-6)]
    return (active[0], active[-1]) if active else (0, len(series["year"]["values"]) - 1)


def build_pdf_report(*, project: dict, version: dict, run: dict, lang: str = "fr") -> bytes:
    t, lab = TXT[lang], labels(lang)
    res = run.get("result") or {}
    series, kpis = res.get("series", {}), res.get("kpis", {})
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["BodyText"], fontName="Helvetica", fontSize=8.5, leading=11, textColor=INK)
    small = ParagraphStyle("s", parent=body, fontSize=7.5, leading=9.5, textColor=INK2)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=16, textColor=INK)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, textColor=INK,
                        spaceBefore=8, spaceAfter=4)
    esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")  # noqa: E731

    def table(rows, widths, head=True, align_right=()):
        tb = Table(rows, colWidths=widths, repeatRows=1 if head else 0)
        st = [("FONT", (0, 0), (-1, -1), "Helvetica", 7.5), ("TEXTCOLOR", (0, 0), (-1, -1), INK),
              ("LINEBELOW", (0, 0), (-1, -1), 0.3, GRID), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
              ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
        if head:
            st += [("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 7.5), ("BACKGROUND", (0, 0), (-1, 0), HEAD_BG)]
        for c in align_right:
            st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
        tb.setStyle(TableStyle(st))
        return tb

    story = [Paragraph(f"Mini-Grid Financial Model Studio — {t['title']}", h1)]
    ident = [[t["project"], esc(project.get("name", ""))], [t["country"], esc(project.get("country", ""))],
             [t["scenario"], f"{esc(version['scenario'])} v{version['version']}"],
             [t["vstatus"], version.get("status", "")], [t["status"], run.get("status", "")],
             [t["options"], ", ".join(res.get("options") or []) or t["none"]],
             [t["solver"], res.get("solver", {}).get("method", "")],
             [t["engine"], run.get("engine_version", ENGINE_VERSION)], [t["hash"], run.get("inputs_hash", "")],
             [t["generated"], dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")]]
    story.append(table(ident, [50 * mm, 200 * mm], head=False))
    story.append(Spacer(1, 4))
    status_text = {"reconciled-engine": t["reconciled"], "variant": t["variant"]}.get(run.get("status"), t["failed_run"])
    story.append(Paragraph(f"<b>{status_text}</b>", body))
    story.append(Paragraph(esc(t["disclaimer"]), small))

    # alerts: icon + label, never colour alone
    story.append(Paragraph(t["alerts"], h2))
    alerts = [("!", CRITICAL, f"{t['failed_check']} : {(CHECKS_FR if lang == 'fr' else CHECKS_EN).get(k, k)}")
              for k in res.get("failed_checks", [])]
    alerts += [("i", WARNING, translate_message(w, lang)) for w in res.get("warnings", [])
               if not w.startswith("Workbook checks not passed")]
    if run.get("status") == "failed":
        alerts.insert(0, ("!", CRITICAL, translate_message(run.get("error") or "failed", lang)))
    if not alerts:
        story.append(Paragraph(t["none"], body))
    for icon, col, text in alerts:
        story.append(Paragraph(f'<font color="#{col.hexval()[2:]}"><b>[{icon}]</b></font> {esc(text)}', body))

    # indicators
    if kpis:
        story.append(Paragraph(t["kpis"], h2))
        rows = [[t["label"], t["value"], t["unit"], t["source"], t["flag"]]]
        for k, i in kpis.items():
            if i.get("value") is None and "error" in k:
                continue
            flag = t["experimental"] if i.get("experimental") else t["derived"] if i.get("derived") else ""
            rows.append([Paragraph(esc(kpi_label(k, i["label"], lang)), small), fmt_value(i["value"], i["unit"], lang),
                         unit_label(i["unit"], lang), Paragraph(esc(source_label(i["source"], lang)), small), flag])
        story.append(table(rows, [95 * mm, 32 * mm, 30 * mm, 70 * mm, 22 * mm], align_right=(1,)))
        story.append(Paragraph(esc(t["note_amounts"]), small))

    # charts
    if series:
        a, b = _window(series)
        years = series["year"]["values"][a:b + 1]
        sl = lambda k: series[k]["values"][a:b + 1] if k in series else [None] * len(years)  # noqa: E731
        name = lambda k: series_label(k, series[k]["label"] if k in series else k, lang)  # noqa: E731
        story += [PageBreak(), Paragraph(t["charts"], h2)]
        cn = lambda k: CHART_NAMES[lang].get(k, name(k))  # noqa: E731
        charts = [
            (t["c1"], [(cn("revenue"), sl("revenue")), (cn("total_opex"), [-(v or 0) for v in sl("total_opex")]),
                       (cn("ebitda"), sl("ebitda"))], None),
            (t["c2"], [(cn("cfads"), sl("cfads")), (cn("debt_service"), sl("debt_service"))], None),
            (t["c3"], [(cn("senior_debt_balance"), sl("senior_debt_balance")),
                       (cn("refi_debt_balance"), sl("refi_debt_balance")), (cn("dsra_balance"), sl("dsra_balance"))], None),
            (t["c4"], [("DSCR", dscr_repaying(series, a, b))], (version.get("assumptions") or {}).get("debt", {}).get("target_dscr")),
        ]
        for title, lines, ref in charts:
            story.append(KeepTogether([Paragraph(f"<b>{esc(title)}</b>", body),
                                       line_chart(years, [(l[:34], v) for l, v in lines], lang, ref=ref,
                                                  ref_label=t["target"], cap=max(3 * (ref or 1), 3) if ref else None),
                                       Spacer(1, 4)]))
        # annual summary in blocks of 12 years
        story += [PageBreak(), Paragraph(t["annual"], h2)]
        big = max((abs(v) for k in SUMMARY_ROWS if k in series and series[k]["unit"] == "currency"
                   for v in sl(k) if v is not None), default=0) >= 1e7
        # local-currency amounts are shown in thousands so 12 columns stay readable
        story.append(Paragraph(esc(t["thousands"] if big else t["note_amounts"]), small))
        cell = lambda v, u: fmt_value(None if v is None else (v / 1000 if big and u == "currency" else v), u, lang)  # noqa: E731
        for start in range(0, len(years), 12):
            ys = years[start:start + 12]
            rows = [[""] + [str(y) for y in ys]]
            for k in SUMMARY_ROWS:
                if k in series:
                    rows.append([Paragraph(esc(name(k)), small)] +
                                [cell(v, series[k]["unit"]) for v in sl(k)[start:start + 12]])
            story.append(table(rows, [52 * mm] + [16.5 * mm] * len(ys), align_right=tuple(range(1, len(ys) + 1))))
            story.append(Spacer(1, 6))

    # checks
    if res.get("checks"):
        names = CHECKS_FR if lang == "fr" else CHECKS_EN
        failed = set(res.get("failed_checks", []))
        rows = [[t["checks"], t["value"], t["flag"]]]
        for k, v in res["checks"].items():
            rows.append([names.get(k, k), fmt_value(v, "", lang), f"[!] {t['fail']}" if k in failed else t["ok"]])
        story += [Paragraph(t["checks"], h2), table(rows, [110 * mm, 40 * mm, 30 * mm], align_right=(1,))]

    # assumptions and lots
    A = version.get("assumptions") or {}
    units = {e["path"]: e["unit"] for e in field_entries()}
    rows = [[t["assumptions"], t["value"], t["unit"]]]
    for path in KEY_ASSUMPTIONS:
        g, f = path.split(".")
        v = A.get(g, {}).get(f)
        if isinstance(v, dict):
            v = v.get("value")
        u = units.get(path, "")
        unit = "%" if u.startswith("%") else "x" if u == "x" else ""
        rows.append([lab["fields"].get(path, path), fmt_value(v, unit, lang), unit_label(u, lang)])
    story += [Paragraph(t["assumptions"], h2), table(rows, [120 * mm, 40 * mm, 50 * mm], align_right=(1,))]
    lots = A.get("lots") or []
    if lots:
        fields = ["included", "country", "grids", "connections_per_grid", "kwp_per_grid", "baseline_kwh_month", "tariff"]
        rows = [[""] + [esc(l.get("name") or f"Lot {i + 1}") for i, l in enumerate(lots)]]
        for f in fields:
            rows.append([lab["fields"].get(f"lots.<i>.{f}", f)] + [fmt_value(l.get(f), "", lang) for l in lots])
        story += [Paragraph(t["lots"], h2),
                  table(rows, [70 * mm] + [min(30, 180 / len(lots)) * mm] * len(lots), align_right=tuple(range(1, len(lots) + 1)))]

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(MUTED)
        canvas.drawString(15 * mm, 8 * mm, f"{project.get('name', '')} · {version['scenario']} v{version['version']} · "
                                           f"{run.get('status', '')}")
        canvas.drawRightString(landscape(A4)[0] - 15 * mm, 8 * mm, f"{t['page']} {doc.page}")
        canvas.restoreState()

    out = io.BytesIO()
    doc = SimpleDocTemplate(out, pagesize=landscape(A4), leftMargin=15 * mm, rightMargin=15 * mm, topMargin=12 * mm,
                            bottomMargin=14 * mm, title=f"{project.get('name', '')} — {t['title']}",
                            author="Mini-Grid Financial Model Studio")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return out.getvalue()
