"""Bilingual labels (FR/EN) of groups, assumption fields, indicators, series and
checks. Single source for the exports and the web interface (GET /engine/labels).

English field labels are derived from the field name when no label is given;
French labels are written out. Units and workbook cells come from the engine.
"""
from __future__ import annotations

import dataclasses

from ..engine import assumptions as A
from ..engine.results import CHECKS, KPIS, SERIES

GROUPS = {
    "currency": ("Devise et montants", "Currency and amounts"),
    "timing": ("Calendrier", "Timing"),
    "technical": ("Technique", "Technical"),
    "build": ("Construction et montée en charge", "Build and ramp-up"),
    "demand": ("Demande et tarifs", "Demand and tariffs"),
    "opex": ("Charges d'exploitation et BFR", "Opex and working capital"),
    "replacement": ("Renouvellements", "Replacements"),
    "tax": ("Fiscalité et TVA", "Tax and VAT"),
    "funding": ("Financement", "Funding"),
    "debt": ("Dette senior", "Senior debt"),
    "refi": ("Refinancement", "Refinancing"),
    "reserves": ("Réserves (DSRA, MMRA)", "Reserves (DSRA, MMRA)"),
    "macro": ("Macroéconomie", "Macroeconomics"),
    "exit": ("Réseau national et sortie", "Grid arrival and exit"),
    "constants": ("Constantes", "Constants"),
    "pasted": ("Valeurs collées par les macros", "Values pasted by the macros"),
    "lots": ("Sites et lots", "Sites and lots"),
}

FIELDS_FR = {
    "currency.case": "Devise du modèle (1 = USD, 2 = monnaie locale)",
    "currency.effective_year": "Année du taux de change appliqué",
    "currency.base_exchange_rate": "Taux de change de base (LCY/USD)",
    "currency.mmra_starting_balance": "Solde initial de la MMRA",
    "currency.all_in_cost_of_debt": "Coût tout compris de la dette (taux fixe)",
    "currency.capex_net_of_grant": "CAPEX net de subvention par raccordement",
    "currency.grant_per_connection": "Subvention par raccordement",
    "currency.battery_cost": "Coût des batteries",
    "currency.transfer_fee": "Frais de transfert par raccordement",
    "currency.fixed_fee_per_grid": "Redevance fixe par réseau",
    "currency.diesel_price": "Prix du diesel",
    "currency.pv_price": "Prix du PV",
    "currency.battery_racking": "Rayonnage des batteries",
    "currency.battery_installation": "Installation des batteries",
    "currency.battery_replacement_2023": "Remplacement des batteries (prix 2023)",
    "currency.inverter_price_2020": "Prix des onduleurs (2020)",
    "currency.expansion_racking": "Rayonnage d'extension par module",
    "currency.expansion_logistics": "Logistique d'extension par module",
    "currency.bnef_battery_2030": "Prix des batteries 2030 (BNEF)",
    "currency.inverter_2030": "Prix des onduleurs 2030",
    "currency.fee_per_customer": "Redevance par client et par mois",
    "currency.admin_costs": "Frais administratifs annuels",
    "currency.tariff": "Tarif",
    "currency.grid_arrival_tariff": "Tarif après arrivée du réseau national",
    "currency.amt_threshold": "Seuil de l'impôt minimum",
    "currency.sizing_rounding": "Arrondi des macros de dimensionnement (chiffres)",
    "timing.model_start": "Début du modèle",
    "timing.construction_start": "Début de la construction",
    "timing.project_duration_years": "Durée de construction d'un réseau",
    "timing.lifetime_years": "Durée de vie / d'exploitation",
    "technical.yield_kwh_per_kwp": "Productible (kWh/kWc/an)",
    "technical.self_consumption_kwh_day": "Autoconsommation (kWh/réseau/jour)",
    "technical.meter_consumption_kwh_day": "Consommation des compteurs (kWh/raccordement/jour)",
    "technical.distribution_losses": "Pertes de distribution",
    "technical.night_battery_share": "Part nocturne sur batterie",
    "technical.battery_discharge_limit": "Limite de décharge des batteries",
    "technical.inverter_sizing": "Dimensionnement des onduleurs (W/Wc)",
    "technical.diesel_kwh_per_litre": "Rendement diesel (kWh/litre, groupe 40 kW)",
    "technical.diesel_kwh_per_litre_10kw": "Rendement diesel (groupe 10 kW, inutilisé)",
    "technical.diesel_litres_per_hour": "Consommation diesel (litres/heure)",
    "technical.diesel_threshold": "Seuil diesel (consommation / production brutes)",
    "technical.diesel_share_below": "Part diesel sous le seuil",
    "technical.diesel_share_above": "Part diesel au-dessus du seuil",
    "technical.max_diesel_share": "Part diesel maximale (déclenche l'extension)",
    "build.build_profile": "Profil de construction (part des réseaux par année)",
    "build.ramp_up": "Montée en charge (années 1 à 4)",
    "build.ramp_discount": "Décote de montée en charge (année 1)",
    "demand.growth_base": "Croissance de la demande (cas escalade)",
    "demand.growth_sensitivity": "Sensibilité de croissance",
    "demand.tariff_sensitivity": "Sensibilité tarifaire",
    "demand.consumption_case": "Cas de consommation (1 plateau, 2 escalade, 3 plateau + revenu)",
    "demand.income_growth": "Croissance des revenus des ménages",
    "opex.ratchet_share": "Part « ratchet » des recettes au-delà du P50",
    "opex.fee_thresholds": "Seuils de redevance (années d'exploitation)",
    "opex.receivable_days": "Délai clients (jours)",
    "opex.payable_days": "Délai fournisseurs (jours)",
    "replacement.battery_life": "Durée de vie des batteries",
    "replacement.inverter_life": "Durée de vie des onduleurs",
    "replacement.stop_before_end": "Arrêt des renouvellements avant la fin",
    "replacement.pv_cost_decline": "Baisse annuelle du coût PV",
    "replacement.battery_cost_decline": "Baisse annuelle du coût des batteries",
    "replacement.battery_forecast": "Prévision du prix des batteries",
    "replacement.inverter_cost_decline": "Baisse annuelle du coût des onduleurs",
    "replacement.inverter_reference_year": "Année de référence des onduleurs",
    "tax.corporate_rate": "Taux d'impôt sur les sociétés",
    "tax.holiday_years": "Exonération fiscale (années)",
    "tax.nol_years": "Report des déficits (années)",
    "tax.vat_rate": "Taux de TVA",
    "tax.vat_capex": "TVA sur CAPEX (récupérable ou non)",
    "tax.vat_opex": "TVA sur OPEX (récupérable ou non)",
    "tax.vat_term_days": "Délai de remboursement de TVA (jours)",
    "tax.minimum_tax": "Impôt minimum (% des recettes)",
    "tax.dividend_wht": "Retenue à la source sur dividendes",
    "tax.book_life_initial": "Durée d'amortissement comptable",
    "tax.tax_life_initial": "Durée d'amortissement fiscal initiale",
    "tax.tax_life_replacement": "Durée d'amortissement fiscal des renouvellements",
    "tax.capital_allowance_limit": "Plafond des amortissements fiscaux",
    "funding.wacc": "CMPC (taux d'actualisation)",
    "funding.irr_period": "Horizon du TRI (années)",
    "funding.grant_drawdown_rate": "Part des emplois financée par subvention",
    "funding.developer_stake": "Participation du développeur",
    "funding.owner_equity_provision": "Apport en fonds propres du propriétaire",
    "debt.gearing": "Taux d'endettement",
    "debt.sizing_method": "Méthode de dimensionnement (Gearing ou DSCR)",
    "debt.debt_switch": "Dette activée (0/1)",
    "debt.margin": "Marge sur taux variable",
    "debt.rate_choice": "Type de taux (fixe ou variable)",
    "debt.arrangement_fee": "Commission d'arrangement",
    "debt.commitment_fee_share": "Commission d'engagement (% de la marge, jamais facturée)",
    "debt.repayment_start_ops_year": "Début du remboursement (année d'exploitation)",
    "debt.tenor_years": "Maturité (années)",
    "debt.grace_years": "Différé (années)",
    "debt.target_dscr": "DSCR cible",
    "debt.drawdown": "Ordre de tirage (fonds propres d'abord ou pari passu)",
    "debt.margin_by_period": "Marges par période (facultatif)",
    "debt.fixed_rate_by_period": "Taux fixes par période (facultatif)",
    "refi.tenor_year": "Année du refinancement (dans la maturité senior)",
    "refi.on": "Refinancement activé (0/1)",
    "refi.gearing": "Taux d'endettement du refinancement",
    "refi.sizing_rounding": "Arrondi du dimensionnement (chiffres)",
    "refi.sizing_method": "Méthode de dimensionnement",
    "refi.margin": "Marge",
    "refi.rate_choice": "Type de taux",
    "refi.upfront_fee": "Commission initiale (inutilisée)",
    "refi.commitment_fee_share": "Commission d'engagement (jamais facturée)",
    "refi.tenor_years": "Maturité (années)",
    "reserves.dsra_on": "DSRA activée (0/1)",
    "reserves.dsra_months": "DSRA (mois de service de la dette)",
    "reserves.dsra_deposit_rate": "Rémunération de la DSRA",
    "reserves.mmra_years": "MMRA (années de CAPEX batteries futures)",
    "reserves.mmra_on": "MMRA activée (0/1)",
    "macro.inflation": "Inflation",
    "macro.fx_case": "Cas de change (1 local, 2 USD vers LCY)",
    "macro.fx_depreciation": "Dépréciation annuelle de la monnaie locale",
    "macro.base_rate_years": "Années des taux de base",
    "macro.base_rates": "Taux de base",
    "exit.years_before_grid_arrival": "Années avant l'arrivée du réseau national",
    "exit.exit_wacc": "Taux d'actualisation de sortie",
    "exit.exit_lookforward_years": "Horizon de valorisation de sortie (années)",
    "exit.exit_ops_year": "Année d'exploitation de la sortie",
    "constants.days_per_year": "Jours par an",
    "constants.months_per_year": "Mois par an",
    "constants.thousand": "Mille",
    "pasted.funding": "Besoin de financement collé (Funding_paste)",
    "pasted.dscr_limit": "Capacité DSCR collée (DSCR_paste)",
    "pasted.refi_limit": "Capacité de refinancement collée (Refi_Paste)",
    "pasted.dsra_initial": "DSRA initiale collée (DSRA_Paste)",
    "lots.name": "Nom du lot", "lots.included": "Inclus (1/0)", "lots.country": "Pays",
    "lots.grids": "Nombre de réseaux", "lots.connections_per_grid": "Raccordements par réseau",
    "lots.kwp_per_grid": "kWc par réseau", "lots.people_per_connection": "Personnes par raccordement",
    "lots.baseline_kwh_month": "Consommation de base (kWh/mois)", "lots.peak_kwh_month": "Consommation de pointe (kWh/mois)",
    "lots.expansion_module_kw": "Module d'extension (kW)", "lots.tariff": "Tarif (sinon : portefeuille)",
    "lots.capex_net_of_grant": "CAPEX net de subvention (sinon : portefeuille)",
    "lots.transfer_fee": "Frais de transfert (sinon : portefeuille)",
    "lots.grant_per_connection": "Subvention par raccordement (sinon : portefeuille)",
    "lots.battery_cost": "Coût des batteries (sinon : portefeuille)",
    "lots.fixed_fee_per_grid": "Redevance fixe par réseau (sinon : portefeuille)",
    "lots.fee_per_customer": "Redevance par client (sinon : portefeuille)",
    "lots.ratchet_share": "Part « ratchet » (sinon : portefeuille)",
    "lots.diesel_price": "Prix du diesel (sinon : portefeuille)",
}

KPIS_FR = {
    "project_irr": "TRI projet (XIRR, subvention incluse)", "payback_years": "Délai de récupération",
    "project_npv": "VAN projet (XNPV au CMPC)", "project_npv_ex_purchases": "VAN hors achats de réseaux, subvention incluse",
    "npv_per_connection": "VAN par raccordement", "equity_irr_incl_grant": "TRI fonds propres AssetCo, subvention incluse",
    "equity_irr_excl_grant": "TRI fonds propres AssetCo, hors subvention",
    "owner_irr_incl_grant": "TRI du propriétaire, subvention incluse", "owner_irr_excl_grant": "TRI du propriétaire, hors subvention",
    "senior_debt": "Dette senior tirée", "grant": "Subvention à l'AssetCo", "owner_equity": "Fonds propres du propriétaire",
    "total_funding": "Besoin de financement total", "dscr_capacity": "Capacité de dette (sculptage DSCR)",
    "dsra_initial": "Dotation initiale de la DSRA", "mean_monthly_arpu": "ARPU mensuel moyen",
    "mean_monthly_consumption": "Consommation mensuelle moyenne", "avg_tariff": "Tarif moyen (pondéré dans le temps)",
    "people_served": "Personnes desservies", "connections": "Raccordements", "grids": "Nombre de réseaux",
    "min_dscr_repayment": "DSCR minimum (années de remboursement)", "avg_dscr_repayment": "DSCR moyen (années de remboursement)",
    "min_dscr_grace": "DSCR minimum (différé)", "llcr_first_repayment": "LLCR à la première année de remboursement",
    "project_irr_unlevered_pretax": "TRI projet non endetté avant impôt (hors subvention)",
    "project_irr_unlevered_pretax_grant": "TRI projet non endetté avant impôt (subvention incluse)",
}

SERIES_FR = {
    "year": "Année", "construction_flag": "Période de construction", "operations_flag": "Période d'exploitation",
    "operational_grids": "Réseaux en service (fin d'année)", "connections": "Raccordements en service",
    "consumption_kwh": "Consommation des clients", "gross_production_kwh": "Production PV brute",
    "diesel_production_kwh": "Production diesel", "revenue": "Recettes", "opco_fees": "Redevance d'exploitation OpCo",
    "diesel_cost": "Coût du diesel", "admin_costs": "Frais administratifs", "total_opex": "Total des charges d'exploitation",
    "ebitda": "EBE (EBITDA)", "depreciation": "Amortissements", "ebit": "Résultat d'exploitation (EBIT)",
    "interest": "Intérêts senior (compte de résultat)", "ebt": "Résultat avant impôt", "npat": "Résultat net",
    "grid_purchases": "Achats de réseaux", "ongoing_capex": "CAPEX courant", "tax_paid": "Impôt payé",
    "cfads": "Flux disponible pour le service de la dette (CFADS)", "senior_interest": "Intérêts senior payés",
    "senior_principal": "Principal senior remboursé", "senior_debt_balance": "Encours de dette senior",
    "refi_debt_balance": "Encours de dette refinancée", "dsra_balance": "Solde de la DSRA", "mmra_balance": "Solde de la MMRA",
    "distributions": "Distributions nettes de retenue", "project_cash_flow": "Flux de trésorerie du projet",
    "cash_balance": "Trésorerie de clôture", "total_assets_current": "Actif circulant", "fixed_assets": "Immobilisations",
    "liabilities": "Passif", "net_assets": "Actif net", "equity": "Capitaux propres",
    "balance_check": "Contrôle d'équilibre du bilan (0 = OK)", "period_end": "Date de fin de période",
    "npv_cash_flow": "Flux du projet pour la VAN", "irr_cash_flow": "Flux du projet pour le TRI",
    "debt_service": "Service de la dette senior et refinancée", "dscr": "DSCR = CFADS / service de la dette",
    "dscr_below_target": "DSCR sous la cible (année de remboursement)",
}

CHECKS_FR = {
    "balance_sheet_balances": "Le bilan est équilibré", "equity_required": "Fonds propres requis couverts",
    "senior_debt_repaid": "Dette senior entièrement remboursée", "funding_optimised": "Financement optimisé (macro)",
    "senior_debt_sized": "Dette senior dimensionnée (macro)", "refi_debt_repaid": "Dette refinancée remboursée",
    "refi_debt_sized": "Dette refinancée dimensionnée (macro)", "no_additional_equity": "Pas de fonds propres additionnels",
    "no_equity_injection": "Pas d'injection de fonds propres", "grids_built": "Tous les réseaux sont construits",
    "mmra_end_balance": "Solde final de la MMRA", "dsra_funded": "DSRA dotée (macro)",
}
CHECKS_EN = {
    "balance_sheet_balances": "Balance sheet balances", "equity_required": "Required equity covered",
    "senior_debt_repaid": "Senior debt fully repaid", "funding_optimised": "Funding optimised (macro)",
    "senior_debt_sized": "Senior debt sized (macro)", "refi_debt_repaid": "Refinanced debt repaid",
    "refi_debt_sized": "Refinanced debt sized (macro)", "no_additional_equity": "No additional equity",
    "no_equity_injection": "No equity injection", "grids_built": "All grids built",
    "mmra_end_balance": "MMRA end balance", "dsra_funded": "DSRA funded (macro)",
}


def _en(name: str) -> str:
    return name.replace("_", " ").capitalize()


def field_entries() -> list[dict]:
    """Every editable assumption: path, group, labels, unit, workbook cell, doc."""
    out = []
    for g in dataclasses.fields(A.Assumptions):
        if g.name == "lots":
            for name, row in A.LOT_ROWS.items():
                out.append({"path": f"lots.<i>.{name}", "group": "lots", "fr": FIELDS_FR.get(f"lots.{name}", _en(name)),
                            "en": _en(name), "unit": "", "cell": f"Portfolio!E{row}:J{row}", "doc": ""})
            continue
        cls = getattr(A, g.type) if isinstance(g.type, str) else g.type
        for f in dataclasses.fields(cls):
            path = f"{g.name}.{f.name}"
            out.append({"path": path, "group": g.name, "fr": FIELDS_FR.get(path, _en(f.name)),
                        "en": _en(f.name) if not f.metadata.get("doc") or len(f.metadata["doc"]) > 60
                        else f"{_en(f.name)} ({f.metadata['doc']})",
                        "unit": f.metadata.get("unit", ""), "cell": f.metadata.get("cell", ""),
                        "doc": f.metadata.get("doc", ""), "type": str(f.type)})
    return out


DERIVED_KPIS_EN = {
    "min_dscr_repayment": "Minimum DSCR over repayment years", "avg_dscr_repayment": "Average DSCR over repayment years",
    "min_dscr_grace": "Minimum DSCR during grace period", "llcr_first_repayment": "LLCR at first repayment year",
    "project_irr_unlevered_pretax": "Unlevered pre-tax project IRR (no grant, no tax)",
    "project_irr_unlevered_pretax_grant": "Unlevered pre-tax project IRR incl. grant",
}
DERIVED_SERIES_EN = {
    "debt_service": "Senior + refinanced debt service", "dscr": "DSCR = CFADS / debt service",
    "dscr_below_target": "DSCR below target (repayment year)",
}


def labels(lang: str) -> dict:
    fr = lang == "fr"
    kpis_en = {k: label for k, (_r, _u, label) in KPIS.items()} | DERIVED_KPIS_EN
    series_en = {k: label for k, (_r, _u, label) in SERIES.items()} | DERIVED_SERIES_EN
    return {
        "groups": {k: v[0] if fr else v[1] for k, v in GROUPS.items()},
        "kpis": {k: KPIS_FR.get(k, v) for k, v in kpis_en.items()} if fr else kpis_en,
        "series": {k: SERIES_FR.get(k, v) for k, v in series_en.items()} if fr else series_en,
        "checks": CHECKS_FR if fr else CHECKS_EN,
        "fields": {e["path"]: e["fr" if fr else "en"] for e in field_entries()},
        "units": UNITS_FR if fr else {},
        "message_rules": MESSAGE_RULES_FR if fr else [],
    }


def kpi_label(key: str, default: str, lang: str) -> str:
    if lang != "fr":
        return default
    if key.startswith("lot_") and key.endswith("_project_irr"):
        return f"TRI projet du lot {key.split('_')[1]} seul (expérimental)"
    return KPIS_FR.get(key, default)


def series_label(key: str, default: str, lang: str) -> str:
    return SERIES_FR.get(key, default) if lang == "fr" else default


assert set(CHECKS_FR) == set(CHECKS) == set(CHECKS_EN)


UNITS_FR = {
    "years": "ans", "year": "année", "currency": "devise", "connections": "raccordements", "people": "personnes",
    "grids": "réseaux", "currency/connection": "devise/raccordement", "currency/month": "devise/mois",
    "currency/kWh": "devise/kWh", "kWh/month": "kWh/mois", "flag": "indicateur", "date": "date",
    "days": "jours", "months of debt service": "mois de service de la dette", "% p.a.": "% par an",
    "%/year": "%/an", "operations year": "année d'exploitation", "currency/year": "devise/an",
    "currency/grid/year": "devise/réseau/an", "currency/connection/month": "devise/raccordement/mois",
    "currency/litre": "devise/litre", "litre/hour": "litre/heure", "kWh/litre": "kWh/litre",
}


def unit_label(unit: str, lang: str) -> str:
    return UNITS_FR.get(unit, unit) if lang == "fr" else unit


# Engine messages are written in English; these rules give their French form.
MESSAGE_RULES_FR = [
    (r"^Variant run: options (.+) depart from the reference workbook\.$",
     r"Calcul en variante : les options \1 s'écartent du classeur de référence."),
    (r"^Exact solver: sizing differs from Excel by up to the macros' tolerance \(50,000\)\.$",
     "Solveur exact : le dimensionnement diffère d'Excel au plus de la tolérance des macros (50 000)."),
    (r"^Workbook checks not passed: (.+)$", r"Contrôles du classeur non satisfaits : \1"),
    (r"^Derived DSCR falls to ([\d.]+)x in a repayment year, below the ([\d.]+)x target "
     r"\(the workbook has no DSCR covenant test\)\.$",
     r"Le DSCR dérivé descend à \1x une année de remboursement, sous la cible de \2x "
     r"(le classeur ne teste aucun covenant de DSCR)."),
    (r"^Senior debt balance becomes negative: .*$",
     "L'encours de dette senior devient négatif : le classeur rembourse plus que dû (Debt!32 n'est pas plafonné). "
     "L'option cap_principal_at_balance l'évite."),
    (r"^Refinanced debt balance becomes negative\.$", "L'encours de dette refinancée devient négatif."),
    (r"^(.*)Between 1 and (\d+) lots are supported .*$",
     r"\1De 1 à \2 lots sont possibles (le format du classeur compte 6 colonnes de lots, E à J)."),
    (r"^(.*)No included lot with grids .*$", r"\1Aucun lot inclus ne compte de réseau (Portfolio!S14 vaudrait #DIV/0!)."),
    (r"^(.*)Included flag must be 0 or 1\.$", r"\1L'indicateur « inclus » doit valoir 0 ou 1."),
    (r"^(.*)Included lot needs connections\.$", r"\1Un lot inclus doit avoir des raccordements."),
    (r"^(.*)Build shares cannot be negative\.$", r"\1Les parts de construction ne peuvent être négatives."),
    (r"^(.*)Build shares sum to ([\d.]+), not 1: .*$",
     r"\1Les parts de construction totalisent \2 et non 1 : le contrôle Inputs!G141 signalera des réseaux non construits."),
    (r"^(.*)DSRA provision above 12 months .*$", r"\1DSRA supérieure à 12 mois (#N/A dans Inputs!E375)."),
    (r"^(.*)Construction must start after the model start date.*$",
     r"\1La construction doit commencer après le début du modèle."),
    (r"^(.*)Inputs!E17 is only exact for a 1-year build; consider option fix_ops_start\.$",
     r"\1Inputs!E17 n'est exact que pour une construction d'un an ; voir l'option fix_ops_start."),
    (r"^(.*)Must be (.+)\.$", r"\1Valeur attendue : \2."),
    (r"^(.*)Target DSCR must be positive\.$", r"\1Le DSCR cible doit être positif."),
]


def translate_message(text: str, lang: str) -> str:
    """French form of an engine message (each '; '-separated part); unknown text is returned unchanged."""
    if lang != "fr" or not text:
        return text
    import re
    parts = []
    for part in text.split("; "):
        for pat, rep in MESSAGE_RULES_FR:
            new, n = re.subn(pat, rep, part)
            if n:
                part = new
                break
        parts.append(part)
    return "; ".join(parts)
