"""Report content builder (format-independent).

Produces the 14 required sections from a snapshot. Every numeric cell in a result table
carries the snapshot path it was read from ("Source" column), so each reported figure is
traceable to the model output that produced it.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.optimization.system import SCENARIOS
from src.snapshot import get_path


@dataclass
class Table:
    caption: str
    header: list[str]
    rows: list[list[str]]


@dataclass
class Section:
    title: str
    paragraphs: list[str] = field(default_factory=list)
    bullets: list[str] = field(default_factory=list)
    tables: list[Table] = field(default_factory=list)
    charts: list[str] = field(default_factory=list)


L = {
    "fr": {
        "title": "Étude préliminaire d'optimisation énergétique et d'investissement",
        "sections": ["Résumé exécutif", "Profil du site industriel", "Système énergétique existant", "Évaluation de la demande",
                     "Alternatives technologiques", "Résultats de simulation technique", "Comparaison économique", "Analyse financière",
                     "Analyse de sensibilité", "Évaluation des risques", "Solution recommandée", "Feuille de route de mise en œuvre",
                     "Sources de données", "Hypothèses et limites"],
        "indicator": "Indicateur", "value": "Valeur", "source": "Source (sortie du modèle)", "scenario": "Scénario",
        "synthetic_banner": "DONNÉES SYNTHÉTIQUES - document de démonstration ; les résultats ne décrivent aucun site réel.",
        "na": "n.d.",
    },
    "en": {
        "title": "Preliminary energy optimisation and investment study",
        "sections": ["Executive summary", "Industrial site profile", "Existing energy system", "Energy demand assessment",
                     "Technology alternatives", "Technical simulation results", "Economic comparison", "Financial analysis",
                     "Sensitivity analysis", "Risk assessment", "Recommended solution", "Implementation roadmap",
                     "Data sources", "Assumptions and limitations"],
        "indicator": "Indicator", "value": "Value", "source": "Source (model output)", "scenario": "Scenario",
        "synthetic_banner": "SYNTHETIC DATA - demonstration document; results do not describe any real site.",
        "na": "n/a",
    },
}


def fmt(v, kind: str = "num", d: int = 0, na: str = "n/a") -> str:
    if v is None:
        return na
    if kind == "pct":
        return f"{v * 100:.1f} %"
    if kind == "x":
        return f"{v:.2f}x"
    return f"{v:,.{d}f}".replace(",", " ")


def _row(snap, label, path, kind="num", d=0, unit="", na="n/a"):
    v = get_path(snap, path)
    return [label, (fmt(v, kind, d, na) + (f" {unit}" if unit and v is not None else "")), path]


def scenario_label(key: str, lang: str) -> str:
    s = SCENARIOS.get(key)
    return (s.label_fr if lang == "fr" else s.label_en) if s else key


def build_sections(snap: dict, lang: str = "fr") -> list[Section]:
    t = L["fr" if lang == "fr" else "en"]
    fr = lang == "fr"
    na = t["na"]
    ccy = snap["meta"]["currency"]
    names = t["sections"]
    rec = snap.get("recommended")
    fin = snap.get("finance")
    p = snap.get("project", {})
    hdr = [t["indicator"], t["value"], t["source"]]
    sec: list[Section] = []

    # 1 Executive summary
    s1 = Section(names[0])
    if snap["data_flags"].get("project_synthetic"):
        s1.paragraphs.append(t["synthetic_banner"])
    if rec:
        s1.paragraphs.append((f"Configuration recommandée : {scenario_label(rec, lang)} (coût annuel équivalent le plus bas parmi les scénarios "
                              f"respectant la contrainte de fiabilité dans la simulation horaire de vérification)." if fr else
                              f"Recommended configuration: {scenario_label(rec, lang)} (lowest equivalent annual cost among scenarios meeting "
                              f"the reliability constraint in the hourly verification simulation)."))
    rows = [_row(snap, "Consommation annuelle" if fr else "Annual consumption", "demand.annual_kwh", unit="kWh", na=na),
            _row(snap, "Pointe" if fr else "Peak demand", "demand.peak_kw", unit="kW", na=na),
            _row(snap, "Coût d'exploitation de référence" if fr else "Baseline operating cost", "baseline.metrics.annual_operating_cost", unit=f"{ccy}/yr", na=na)]
    if rec:
        base = f"scenarios.{rec}.check.metrics"
        rows += [_row(snap, "Investissement" if fr else "Investment", f"{base}.total_investment", unit=ccy, na=na),
                 _row(snap, "Part renouvelable" if fr else "Renewable share", f"{base}.renewable_share", "pct", na=na),
                 _row(snap, "Énergie non servie" if fr else "Unserved energy", f"{base}.unserved_fraction", "pct", na=na)]
    if fin:
        rows += [_row(snap, "VAN projet" if fr else "Project NPV", "finance.npv_project", unit=ccy, na=na),
                 _row(snap, "TRI projet" if fr else "Project IRR", "finance.irr_project", "pct", na=na),
                 _row(snap, "TRI fonds propres" if fr else "Equity IRR", "finance.irr_equity", "pct", na=na),
                 _row(snap, "DSCR minimum" if fr else "Minimum DSCR", "finance.min_dscr", "x", na=na),
                 _row(snap, "LCOE système" if fr else "System LCOE", "finance.lcoe_per_kwh", d=1, unit=f"{ccy}/kWh", na=na),
                 _row(snap, "Retour simple" if fr else "Simple payback", "finance.payback_years", d=1, unit="yr", na=na)]
    s1.tables.append(Table("Indicateurs clés" if fr else "Key indicators", hdr, rows))
    sec.append(s1)

    # 2 Site profile
    s2 = Section(names[1])
    fields = [("code", "ID"), ("company_name", "Entreprise" if fr else "Company"), ("sector", "Secteur" if fr else "Sector"),
              ("country", "Pays" if fr else "Country"), ("region", "Région" if fr else "Region"), ("latitude", "Latitude"),
              ("longitude", "Longitude"), ("installed_capacity_kw", "Capacité installée (kW)" if fr else "Installed capacity (kW)"),
              ("existing_technologies", "Technologies existantes" if fr else "Existing technologies"),
              ("data_quality", "Qualité des données (A-D)" if fr else "Data quality (A-D)")]
    s2.tables.append(Table("Site", [t["indicator"], t["value"], t["source"]],
                           [[lbl, ", ".join(p[k]) if isinstance(p.get(k), list) else str(p.get(k, na)), f"project.{k}"] for k, lbl in fields]))
    if p.get("notes"):
        s2.paragraphs.append(p["notes"])
    sec.append(s2)

    # 3 Existing system
    s3 = Section(names[2])
    s3.paragraphs.append((f"Système de référence simulé : {scenario_label(snap['baseline']['scenario'], lang)}, capacités existantes, sans nouvel investissement."
                          if fr else f"Simulated baseline: {scenario_label(snap['baseline']['scenario'], lang)}, existing capacities, no new investment."))
    s3.tables.append(Table("Référence et coûts diesel" if fr else "Baseline and diesel costs", hdr, [
        _row(snap, "Consommation de gazole" if fr else "Diesel consumption", "baseline.metrics.fuel_l", unit="L/yr", na=na),
        _row(snap, "Émissions CO2 diesel" if fr else "Diesel CO2 emissions", "baseline.metrics.co2_t", unit="t/yr", na=na),
        _row(snap, "Coût d'exploitation annuel" if fr else "Annual operating cost", "baseline.metrics.annual_operating_cost", unit=ccy, na=na),
        _row(snap, "Diesel : coût d'exploitation/kWh (parc existant)" if fr else "Diesel: operating cost/kWh (existing fleet)", "diesel_module.operating_cost_per_kwh", d=1, unit=f"{ccy}/kWh", na=na),
        _row(snap, "Diesel : coût économique complet/kWh" if fr else "Diesel: full economic cost/kWh", "diesel_module.economic_cost_per_kwh", d=1, unit=f"{ccy}/kWh", na=na),
        _row(snap, "Diesel : coût actualisé (LCOE)" if fr else "Diesel: levelised cost (LCOE)", "diesel_module.lcoe_per_kwh", d=1, unit=f"{ccy}/kWh", na=na),
        _row(snap, "Diesel : facteur de capacité" if fr else "Diesel: capacity factor", "diesel_module.capacity_factor", "pct", na=na),
    ]))
    sec.append(s3)

    # 4 Demand
    s4 = Section(names[3])
    flags = snap["data_flags"]
    s4.paragraphs.append(("Source du profil de charge : " if fr else "Load profile source: ") + flags.get("load_source", ""))
    if flags.get("load_synthetic"):
        s4.bullets += flags.get("load_assumptions", [])
    s4.tables.append(Table("Demande" if fr else "Demand", hdr, [
        _row(snap, "Consommation annuelle" if fr else "Annual consumption", "demand.annual_kwh", unit="kWh", na=na),
        _row(snap, "Pointe" if fr else "Peak", "demand.peak_kw", unit="kW", na=na),
        _row(snap, "Facteur de charge" if fr else "Load factor", "demand.load_factor", "pct", na=na)]))
    s4.charts.append("monthly_demand")
    sec.append(s4)

    # 5 Alternatives
    s5 = Section(names[4])
    for key, scn in SCENARIOS.items():
        st = (snap.get("scenarios", {}).get(key, {}).get("lp") or {}).get("status", "not run")
        s5.bullets.append(f"{scenario_label(key, lang)} - {st}")
    sec.append(s5)

    # 6 Technical results
    s6 = Section(names[5])
    s6.paragraphs.append(("Dimensionnement par programmation linéaire (8 760 h), puis vérification par simulation horaire à règles "
                          "(charge minimale des groupes, engagement des unités). Les valeurs ci-dessous sont celles de la vérification."
                          if fr else "Sizing by linear programming (8,760 h), then verification by rule-based hourly simulation (generator "
                          "minimum loading, unit commitment). Values below are from the verification run."))
    rows6 = []
    for key, sc in (snap.get("scenarios") or {}).items():
        c = sc["check"].get("capacities", {})
        e = sc["check"].get("annual_energy", {})
        m = sc["check"].get("metrics", {})
        if not sc["check"].get("feasible") and sc["check"].get("status") != "Simulated":
            rows6.append([scenario_label(key, lang), sc["check"].get("status", ""), "", "", "", "", "", f"scenarios.{key}.check"])
            continue
        rows6.append([scenario_label(key, lang), fmt(c.get("pv_kwp")), f"{fmt(c.get('battery_kwh'))}/{fmt(c.get('battery_kw'))}",
                      fmt(c.get("diesel_existing_kw", 0) + c.get("diesel_new_kw", 0)), fmt(c.get("biomass_kw")),
                      fmt(e.get("diesel")), fmt(m.get("unserved_fraction"), "pct"), f"scenarios.{key}.check"])
    s6.tables.append(Table("Capacités et production" if fr else "Capacities and generation",
                           [t["scenario"], "PV kWp", "BESS kWh/kW", "Diesel kW", "Bio kW", "Diesel kWh/yr", "Unserved", t["source"]], rows6))
    s6.charts.append("energy_mix")
    sec.append(s6)

    # 7 Economic comparison
    s7 = Section(names[6])
    rows7 = []
    for key, sc in (snap.get("scenarios") or {}).items():
        m = sc["check"].get("metrics") or {}
        if not m:
            continue
        rows7.append([scenario_label(key, lang), fmt(m.get("annual_cost")), fmt(m.get("annual_operating_cost")), fmt(m.get("lcoe_per_kwh"), d=1),
                      fmt(m.get("total_investment")), fmt(m.get("renewable_share"), "pct"), f"scenarios.{key}.check.metrics"])
    s7.tables.append(Table(f"Coûts ({ccy})" if fr else f"Costs ({ccy})",
                           [t["scenario"], "EAC/yr" if not fr else "Coût annuel équiv.", "OPEX/yr", "LCOE/kWh", "CAPEX", "RE", t["source"]], rows7))
    s7.paragraphs.append(("Coût annuel équivalent = annuités de capital (FRC sur la durée de vie de chaque technologie) + coûts d'exploitation."
                          if fr else "Equivalent annual cost = capital annuities (CRF over each technology lifetime) + operating costs."))
    s7.charts.append("scenario_costs")
    sec.append(s7)

    # 8 Finance
    s8 = Section(names[7])
    if fin:
        s8.paragraphs.append((f"Scénario analysé : {scenario_label(snap.get('finance_scenario'), lang)}. Flux nominaux ; revenus = coûts évités de la référence. "
                              "Le TRI projet est calculé sans flux de financement (pas de double comptage)." if fr else
                              f"Scenario analysed: {scenario_label(snap.get('finance_scenario'), lang)}. Nominal cash flows; revenue = avoided baseline costs. "
                              "The project IRR excludes financing flows (no double counting)."))
        s8.tables.append(Table("Indicateurs financiers" if fr else "Financial indicators", hdr, [
            _row(snap, "VAN projet" if fr else "Project NPV", "finance.npv_project", unit=ccy, na=na),
            _row(snap, "VAN fonds propres" if fr else "Equity NPV", "finance.npv_equity", unit=ccy, na=na),
            _row(snap, "TRI projet" if fr else "Project IRR", "finance.irr_project", "pct", na=na),
            _row(snap, "TRI fonds propres" if fr else "Equity IRR", "finance.irr_equity", "pct", na=na),
            _row(snap, "LCOE" , "finance.lcoe_per_kwh", d=1, unit=f"{ccy}/kWh", na=na),
            _row(snap, "Retour simple" if fr else "Payback", "finance.payback_years", d=1, unit="yr", na=na),
            _row(snap, "Retour actualisé" if fr else "Discounted payback", "finance.discounted_payback_years", d=1, unit="yr", na=na),
            _row(snap, "DSCR minimum" if fr else "Minimum DSCR", "finance.min_dscr", "x", na=na),
            _row(snap, "DSCR moyen" if fr else "Average DSCR", "finance.avg_dscr", "x", na=na),
            _row(snap, "LLCR", "finance.llcr", "x", na=na),
            _row(snap, "Besoin de financement total" if fr else "Total financing requirement", "finance.total_financing_requirement", unit=ccy, na=na),
            _row(snap, "Dette" if fr else "Debt", "finance.debt_amount", unit=ccy, na=na),
            _row(snap, "Économies cumulées" if fr else "Cumulative savings", "finance.cumulative_savings", unit=ccy, na=na)]))
        s8.charts.append("cash_flow")
        if snap.get("structures"):
            s8.tables.append(Table("Structures de financement" if fr else "Financing structures",
                                   ["Structure", "Investisseur" if fr else "Investor", "Exploitant" if fr else "Operator",
                                    "VAN client" if fr else "Client NPV", "TRI investisseur" if fr else "Investor IRR"],
                                   [[r["label_fr"] if fr else r["label_en"], r["investor"], r["operator"],
                                     (("termes manquants" if fr else "terms missing") if r.get("terms_missing") else fmt(r.get("client_npv"))),
                                     fmt(r.get("investor_irr"), "pct") if r.get("investor_irr") is not None else na] for r in snap["structures"]]))
    else:
        s8.paragraphs.append("Analyse financière non disponible." if fr else "Financial analysis not available.")
    sec.append(s8)

    # 9 Sensitivity
    s9 = Section(names[8])
    sens = snap.get("sensitivity") or {}
    if sens.get("tornado"):
        tor = sens["tornado"]
        s9.paragraphs.append((f"Variation d'un paramètre à la fois ; capacités fixes ; indicateur : {tor['metric']}." if fr
                              else f"One-at-a-time variation; capacities held fixed; metric: {tor['metric']}."))
        s9.tables.append(Table("Tornade" if fr else "Tornado", ["Paramètre" if fr else "Parameter", "Bas" if fr else "Low", "Haut" if fr else "High", "Écart" if fr else "Swing"],
                               [[r["parameter"], fmt(r["low"]), fmt(r["high"]), fmt(r["swing"])] for r in tor["rows"]]))
        s9.charts.append("tornado")
    if sens.get("scenarios"):
        s9.tables.append(Table("Cas de base / optimiste / prudent" if fr else "Base / optimistic / conservative",
                               ["Cas" if fr else "Case", "NPV", "IRR", "LCOE", "min DSCR"],
                               [[k, fmt(v["metrics"].get("npv_project")), fmt(v["metrics"].get("irr_project"), "pct"),
                                 fmt(v["metrics"].get("lcoe_per_kwh"), d=1), fmt(v["metrics"].get("min_dscr"), "x")] for k, v in sens["scenarios"].items()]))
    if "break_even_diesel" in sens:
        be = sens["break_even_diesel"]
        s9.paragraphs.append((f"Point mort (VAN = 0) : prix du gazole x{be:.2f} par rapport au cas de base." if be else "Point mort sur le prix du gazole non atteint dans l'intervalle x0,1-x5.")
                             if fr else (f"Break-even (NPV = 0): diesel price x{be:.2f} of the base case." if be else "No diesel-price break-even within x0.1-x5."))
    if not sens:
        s9.paragraphs.append("Analyse de sensibilité non exécutée." if fr else "Sensitivity analysis not run.")
    sec.append(s9)

    # 10 Risks (generic register, qualitative)
    s10 = Section(names[9])
    s10.paragraphs.append("Registre de risques générique (qualitatif), à compléter par le porteur de projet." if fr
                          else "Generic, qualitative risk register, to be completed by the project sponsor.")
    risks = [("Prix et approvisionnement du gazole", "Diesel price and supply", "Contrats d'approvisionnement, stockage", "Supply contracts, storage"),
             ("Change (équipements importés)", "Exchange rate (imported equipment)", "Prix en XAF/EUR, couverture", "XAF/EUR pricing, hedging"),
             ("Évolution de la demande", "Demand change", "Dimensionnement modulaire", "Modular sizing"),
             ("Performance technique", "Technical performance", "Garanties EPC, O&M avec pénalités", "EPC warranties, O&M with penalties"),
             ("Qualité des données", "Data quality", "Mesures sur site avant décision", "On-site measurements before decision"),
             ("Fiabilité du réseau", "Grid reliability", "Secours et stockage dimensionnés", "Sized backup and storage"),
             ("Risque de contrepartie", "Counterparty risk", "Garanties, assurance-crédit", "Guarantees, credit insurance")]
    s10.tables.append(Table("Risques" if fr else "Risks", ["Risque" if fr else "Risk", "Atténuation" if fr else "Mitigation"],
                            [[r[0] if fr else r[1], r[2] if fr else r[3]] for r in risks]))
    sec.append(s10)

    # 11 Recommended solution
    s11 = Section(names[10])
    if rec:
        c = snap["scenarios"][rec]["check"]["capacities"]
        s11.paragraphs.append(f"{scenario_label(rec, lang)}: PV {fmt(c.get('pv_kwp'))} kWp, BESS {fmt(c.get('battery_kwh'))} kWh / {fmt(c.get('battery_kw'))} kW, "
                              f"diesel {fmt(c.get('diesel_existing_kw', 0) + c.get('diesel_new_kw', 0))} kW, biomass {fmt(c.get('biomass_kw'))} kW "
                              f"[scenarios.{rec}.check.capacities].")
        s11.paragraphs.append(("Recommandation préliminaire, à confirmer par une étude de faisabilité détaillée avec données mesurées et devis."
                               if fr else "Preliminary recommendation, to be confirmed by a detailed feasibility study with measured data and quotations."))
    else:
        s11.paragraphs.append("Aucune configuration ne satisfait les critères." if fr else "No configuration meets the criteria.")
    sec.append(s11)

    # 12 Roadmap
    s12 = Section(names[11])
    steps_fr = ["Collecte de données mesurées (charge, gazole, irradiation, coupures)", "Étude de faisabilité détaillée et conception",
                "Consultation EPC / fournisseurs et devis", "Structuration du financement et due diligence prêteurs",
                "Autorisations et contrats (EPC, O&M, PPA le cas échéant)", "Construction et mise en service", "Exploitation, suivi de performance"]
    steps_en = ["Measured data collection (load, fuel, irradiation, outages)", "Detailed feasibility study and design",
                "EPC / supplier consultation and quotations", "Financing structuring and lender due diligence",
                "Permits and contracts (EPC, O&M, PPA where relevant)", "Construction and commissioning", "Operation and performance monitoring"]
    s12.bullets = steps_fr if fr else steps_en
    s12.paragraphs.append("Séquence indicative ; les durées dépendent du projet et ne sont pas estimées par le modèle." if fr
                          else "Indicative sequence; durations depend on the project and are not estimated by the model.")
    sec.append(s12)

    # 13 Data sources
    s13 = Section(names[12])
    s13.bullets = [f"Project: {p.get('data_sources', '')}", f"Load: {flags.get('load_source')}", f"Solar: {flags.get('solar_source')}"]
    if flags.get("grid_outages_synthetic"):
        s13.bullets.append("Grid outages: SYNTHETIC calendar from assumed availability and outage duration")
    s13.bullets += flags.get("notes", [])
    sec.append(s13)

    # 14 Assumptions and limitations
    s14 = Section(names[13])
    a = snap.get("assumptions", {})
    rows14 = []
    for group in ("diesel", "pv", "battery", "biomass", "grid", "reliability", "finance"):
        for k, v in (a.get(group) or {}).items():
            if isinstance(v, (int, float, str, bool)) or v is None:
                rows14.append([f"{group}.{k}", str(v), f"assumptions.{group}.{k}"])
    s14.tables.append(Table("Hypothèses" if fr else "Assumptions", ["Paramètre" if fr else "Parameter", t["value"], t["source"]], rows14))
    s14.bullets = (["Modèle horaire sur une année représentative (8 760 h), sans croissance de la demande.",
                    "Optimisation linéaire : charge minimale et courbes de consommation des groupes non représentées dans l'optimiseur ; vérifiées par simulation.",
                    "Solaire : modèle simplifié (GHI utilisé comme irradiation du plan), non certifiable.",
                    "Biomasse : présélection préliminaire à valider avec des données d'équipement.",
                    "Pas de valeur résiduelle en fin de projet ; amortissement linéaire ; report de pertes illimité.",
                    "Aucun taux de change de marché n'est supposé : seuls les taux saisis par l'utilisateur (et la parité fixe EUR/XAF) sont utilisés."]
                   if fr else
                   ["Hourly model over one representative year (8,760 h), no demand growth.",
                    "Linear optimisation: generator minimum loading and fuel curves are not represented in the optimiser; checked by simulation.",
                    "Solar: simplified model (GHI used as plane-of-array irradiance), not bankable.",
                    "Biomass: preliminary screening to be validated with equipment data.",
                    "No residual value at project end; straight-line depreciation; unlimited loss carry-forward.",
                    "No market exchange rate is assumed: only user-entered rates (and the fixed EUR/XAF parity) are used."])
    sec.append(s14)
    return sec


def report_title(snap: dict, lang: str) -> str:
    t = L["fr" if lang == "fr" else "en"]
    return f"{t['title']} - {snap['project'].get('company_name', '')}"
