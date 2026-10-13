"""Three page project summary (PDF), built only from a stored model run, its sensitivities and the project score."""
from __future__ import annotations

import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .exports import ACCOUNTING_NOTE, STATUS_TEXT, _money, _pct, _stamp

NAVY = colors.HexColor("#0B1F3A")


_CELL = ParagraphStyle("cell", fontName="Helvetica", fontSize=7.5, leading=9)
_HEAD = ParagraphStyle("head", parent=_CELL, fontName="Helvetica-Bold", textColor=colors.white)


def _tbl(rows, widths, head=True):
    """Every cell is a wrapped paragraph, so long labels never overflow into the next column."""
    from xml.sax.saxutils import escape
    rows = [[Paragraph(escape(str(v)), _HEAD if (head and i == 0) else _CELL) for v in r] for i, r in enumerate(rows)]
    t = Table(rows, colWidths=widths, repeatRows=1 if head else 0)
    style = [("FONTSIZE", (0, 0), (-1, -1), 7.5), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.HexColor("#D0D5DD"))]
    if head:
        style += [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white)]
    t.setStyle(TableStyle(style))
    return t


def _x(d):
    """DSCR style multiple with negatives in parentheses."""
    if d is None:
        return ""
    return f"{d:.2f}x" if d >= 0 else f"({-d:.2f})x"


def _num(x, fmt="{:,.0f}"):
    if x is None:
        return "Not available"
    return fmt.format(x) if x >= 0 else "(" + fmt.format(-x) + ")"


def summary_pdf(project, run, sensitivity: dict, score: dict | None, milestones) -> bytes:
    inp, M = run.inputs_snapshot, run.metrics
    fx, ccy = inp["macro"]["fx_lcy_per_usd"], inp["currency"]
    st = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=st["Normal"], fontSize=8.5, leading=11)
    small = ParagraphStyle("s", parent=st["Normal"], fontSize=7, leading=9)
    h1 = ParagraphStyle("h1", parent=st["Title"], fontSize=15, alignment=0, textColor=NAVY)
    h2 = ParagraphStyle("h2", parent=st["Heading2"], fontSize=10.5, textColor=NAVY, spaceBefore=6, spaceAfter=3)
    ok = run.status in ("validated", "warning")
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=14 * mm, rightMargin=14 * mm, topMargin=12 * mm, bottomMargin=12 * mm,
                            title=f"Project summary: {project.name}")
    el = [Paragraph(f"<b>{project.name}</b>: project summary", h1)]
    if run.is_demo:
        el.append(Paragraph("<font color='#B00020'><b>SYNTHETIC DEMO DATA: not a real project and not an offer</b></font>", body))
    el.append(Paragraph(f"Model status: <b>{STATUS_TEXT.get(run.status, run.status)}</b>", small))

    # ---------------------------------------------------------------- page 1: project and financing
    el.append(Paragraph("1. Project", h2))
    tech = inp["technical"]
    rows = [["Item", "Value"],
            ["Country, stage", f"{project.country}, {project.stage}"],
            ["System", f"PV {tech['pv_kwp']:g} kWp; battery {tech['battery_kwh']:g} kWh; diesel {tech['diesel_kw']:g} kW; network {tech['network_km']:g} km"],
            ["Deliverable energy (design study)", f"{tech['deliverable_energy_kwh_pa']:,.0f} kWh a year"],
            ["Connections at target", f"{M.get('connections_target', 0):,.0f}"],
            ["Initial capex", f"{_money(M['capex_total'], ccy)} ({_money(M['capex_total_usd'])})"],
            ["Cost per connection", f"{_money(M.get('cost_per_connection'), ccy)} ({_money(M.get('cost_per_connection_usd'))})"]]
    el.append(_tbl(rows, [55 * mm, 127 * mm]))
    el.append(Paragraph("Customer classes", h2))
    rows = [["Class", "Category", "Connections", "kWh a month", "Tariff (LCY/kWh)", "Fixed charge"]]
    for c in inp["customers"]:
        rows.append([c["name"], c["category"], f"{c['connections_target']:,}", f"{c['kwh_per_connection_month']:g}",
                     f"{c['tariff_per_kwh']:,.0f}", f"{c['fixed_charge_month']:,.0f}"])
    el.append(_tbl(rows, [50 * mm, 25 * mm, 25 * mm, 25 * mm, 30 * mm, 27 * mm]))
    el.append(Paragraph("Sources and uses (construction)", h2))
    su = run.sources_uses
    rows = [["Uses", ccy, "Sources", ccy],
            ["Capex", _num(su["capex"]), "Debt", _num(su["debt"])],
            ["Interest during construction", _num(su["interest_during_construction"]), "Grants in construction", _num(su["grants_in_construction"])],
            ["Financing fees", _num(su["financing_fees"]), "Equity", _num(su["equity"])],
            ["Initial DSRA", _num(su["dsra_initial"]), "", ""],
            ["Tax during construction", _num(su.get("tax_during_construction", 0)), "", ""],
            ["Total uses", _num(su["uses_total"]), "Total sources", _num(su["sources_total"])]]
    el.append(_tbl(rows, [50 * mm, 41 * mm, 50 * mm, 41 * mm]))
    el.append(Paragraph("Debt", h2))
    rows = [["Tranche", "Currency", "Share of basis", "Rate", "Tenor", "Grace", "Repayment"]]
    for d in inp["financing"]["debt"]:
        rows.append([d["name"], d["currency"], f"{d['share_of_capex']:.0%}", f"{d['rate_pa']:.1%}", f"{d['tenor_years']:g} years",
                     f"{d['grace_quarters']} quarters", d["amortisation"].replace("_", " ")])
    el.append(_tbl(rows, [46 * mm, 18 * mm, 24 * mm, 16 * mm, 22 * mm, 24 * mm, 32 * mm]))
    sub = inp["subsidies"]
    el.append(Paragraph(f"Subsidies: capital grant {_money(sub['capital_grant'], ccy)}; RBF {_money(sub['rbf_per_connection'], ccy)} per verified connection"
                        + (f" (cap {_money(sub['rbf_cap'], ccy)})" if sub.get("rbf_cap") else "")
                        + (f"; tariff support {sub['tariff_support_per_kwh']:g} {ccy}/kWh for {sub['tariff_support_years']:g} years" if sub["tariff_support_per_kwh"] else "")
                        + ".", body))
    el.append(PageBreak())

    # ---------------------------------------------------------------- page 2: results and sensitivities
    el.append(Paragraph("2. Financial results", h2))
    if ok:
        rows = [["Metric", "Value", "Metric", "Value"],
                ["Project IRR before subsidy", _pct(M.get("project_irr_pre_subsidy")), "Project IRR after subsidy", _pct(M.get("project_irr_post_subsidy"))],
                ["Equity IRR", _pct(M.get("equity_irr")), "Minimum annual DSCR", "Not applicable" if M.get("dscr_min") is None else _x(M["dscr_min"])],
                ["LLCR at COD", "Not applicable" if M.get("llcr_cod") is None else f"{M['llcr_cod']:.2f}x", "Payback", "Not reached" if M.get("payback_years") is None else f"{M['payback_years']:.2f} years"],
                ["LCOE per kWh sold", f"{_num(M.get('lcoe_per_kwh_sold'), '{:,.1f}')} {ccy} ({_num(M.get('lcoe_per_kwh_sold_usd'), '{:,.3f}')} USD)",
                 "Viability gap per connection", _money(M.get("viability_gap_per_connection"), ccy)],
                ["Subsidy per connection (nominal)", _money(M.get("subsidy_per_connection"), ccy), "Peak equity", _money(M.get("equity_peak"), ccy)]]
        el.append(_tbl(rows, [46 * mm, 45 * mm, 46 * mm, 45 * mm]))
    else:
        el.append(Paragraph("Results are not shown: the model has failed checks or incomplete inputs.", body))
    el.append(Paragraph("Annual figures (first ten operating years)", h2))
    A = run.annual
    rows = [["Year", "Energy sold (kWh)", "Revenue", "EBITDA", "CFADS", "Debt service", "DSCR"]]
    for i in range(min(10, len(A["year"]))):
        d = A["dscr"][i]
        rows.append([A["year"][i], f"{A['energy_sold_kwh'][i]:,.0f}", _num(A["revenue"][i]), _num(A["ebitda"][i]), _num(A["cfads"][i]),
                     _num(A["debt_service"][i]), _x(d)])
    el.append(_tbl(rows, [12 * mm, 30 * mm, 30 * mm, 28 * mm, 28 * mm, 28 * mm, 26 * mm]))
    el.append(Paragraph(f"Amounts in {ccy}. DSCR = CFADS / scheduled debt service.", small))
    el.append(Paragraph("Sensitivities (each case reruns the full model with its checks)", h2))
    rows = [["Case", "Project IRR after subsidy", "Equity IRR", "Project NPV after subsidy", "Min DSCR", "Checks"]]
    for r in sensitivity["rows"]:
        rows.append([r["case"], _pct(r["project_irr_post_subsidy"]), _pct(r["equity_irr"]), _num(r["project_npv_post_subsidy"]),
                     _x(r["dscr_min"]), "OK" if r["checks_passed"] else "FAIL"])
    el.append(_tbl(rows, [62 * mm, 27 * mm, 22 * mm, 34 * mm, 18 * mm, 19 * mm]))
    el.append(PageBreak())

    # ---------------------------------------------------------------- page 3: risks, readiness, sources
    el.append(Paragraph("3. Risks, readiness and assumptions", h2))
    risks = [[w["code"], w["label"], w.get("detail", "")] for w in run.warnings]
    el.append(_tbl([["Code", "Warning from the model", "Detail"]] + (risks or [["", "No warning", ""]]), [22 * mm, 110 * mm, 50 * mm]))
    if score:
        el.append(Paragraph(f"Electrification Acceleration Score: <b>{score['score']:.1f} / 100</b>"
                            f"{' (partial: data unavailable for ' + ', '.join(score['missing_criteria']) + ')' if score['score_is_partial'] else ''}."
                            f" Decision: <b>{score['decision'].replace('_', ' ')}</b>. {score['decision_explanation']}.", body))
        rows = [["Mandatory gate", "State"]] + [[g["label"], g["state"].replace("_", " ")] for g in score["gates"]]
        el.append(_tbl(rows, [120 * mm, 62 * mm]))
        el.append(Paragraph(score["note"], small))
    el.append(Paragraph("Milestones", h2))
    rows = [["Milestone", "Category", "Due", "Status"]] + [[m.title, m.category, m.due_date.isoformat() if m.due_date else "", m.status] for m in milestones]
    el.append(_tbl(rows if len(rows) > 1 else rows + [["No milestones recorded", "", "", ""]], [86 * mm, 32 * mm, 32 * mm, 32 * mm]))
    el.append(Paragraph("Sources and assumptions", h2))
    el.append(Paragraph(f"Input provenance: {inp.get('provenance', 'user_estimate').replace('_', ' ')}. "
                        + ("Assumptions reviewed by " + inp["review"]["reviewed_by"] + " on " + inp["review"]["reviewed_on"] + ". " if inp.get("review") else "Assumptions not reviewed by a named person. ")
                        + f"Exchange rate at financial close {fx:,.2f} {ccy} per USD. {ACCOUNTING_NOTE} This summary is information, not an offer of securities and not investment advice.", body))
    el.append(Paragraph("; ".join(f"{k}: {v}" for k, v in _stamp(project, run)), small))
    doc.build(el)
    return buf.getvalue()
