"""LCOE et indicateurs simples pour l'étude « Coût de l'électricité solaire en Afrique ».

Convention : LCOE = somme actualisée des coûts / somme actualisée de la production,
investissement en année 0, exploitation et production des années 1 à n.
"""

from __future__ import annotations


def crf(rate: float, years: int) -> float:
    """Facteur de récupération du capital (annuité constante par unité investie)."""
    if rate == 0:
        return 1 / years
    return rate * (1 + rate) ** years / ((1 + rate) ** years - 1)


def lcoe(capex: float, opex: float, energy_mwh: float, rate: float, years: int,
         degradation: float = 0.0, opex_escalation: float = 0.0) -> float:
    """LCOE en USD/MWh.

    capex : investissement total (USD, année 0)
    opex : coût d'exploitation de l'année 1 (USD/an)
    energy_mwh : production de l'année 1 (MWh)
    degradation : perte de production annuelle (ex. 0.005)
    opex_escalation : indexation annuelle de l'OPEX (ex. 0.02)
    """
    costs = capex
    energy = 0.0
    for t in range(1, years + 1):
        d = (1 + rate) ** t
        costs += opex * (1 + opex_escalation) ** (t - 1) / d
        energy += energy_mwh * (1 - degradation) ** (t - 1) / d
    return costs / energy


def wacc(debt_share: float, cost_of_debt: float, cost_of_equity: float,
         tax_rate: float = 0.0) -> float:
    """WACC après impôt."""
    return debt_share * cost_of_debt * (1 - tax_rate) + (1 - debt_share) * cost_of_equity


def npv(rate: float, cashflows: list[float]) -> float:
    """VAN, premier flux en année 0."""
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(cashflows))


def irr(cashflows: list[float], lo: float = -0.99, hi: float = 1.0, tol: float = 1e-9) -> float:
    """TRI par dichotomie (un seul changement de signe supposé)."""
    if npv(lo, cashflows) * npv(hi, cashflows) > 0:
        raise ValueError("TRI non encadré entre lo et hi")
    while hi - lo > tol:
        mid = (lo + hi) / 2
        if npv(lo, cashflows) * npv(mid, cashflows) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


# --- Volet B : centrales captives ---------------------------------------------------------

def diesel_cost_mwh(fuel_price_l: float, litres_per_kwh: float, om_mwh: float = 0.0) -> float:
    """Coût variable de la production diesel/HFO en USD/MWh (carburant + O&M variable)."""
    return fuel_price_l * litres_per_kwh * 1000 + om_mwh


def captive_cashflows(capex: float, opex: float, solar_mwh: float, avoided_mwh_cost: float,
                      years: int, degradation: float = 0.0,
                      fuel_escalation: float = 0.0) -> list[float]:
    """Flux du point de vue de l'industriel : investissement, puis économies de carburant
    (production solaire x coût diesel évité) moins OPEX solaire."""
    flows = [-capex]
    for t in range(1, years + 1):
        saved = (solar_mwh * (1 - degradation) ** (t - 1)
                 * avoided_mwh_cost * (1 + fuel_escalation) ** (t - 1))
        flows.append(saved - opex)
    return flows


def simple_payback(capex: float, annual_net_saving: float) -> float:
    return float("inf") if annual_net_saving <= 0 else capex / annual_net_saving


# --- Volet C : mini-réseaux ---------------------------------------------------------------

def minigrid_cost_of_service(gen_capex: float, dist_capex: float, opex: float,
                             commercial_cost: float, generated_mwh: float, losses: float,
                             rate: float, years: int) -> dict[str, float]:
    """Coût complet par MWh vendu, décomposé en production, distribution et gestion commerciale.

    gen_capex : PV, batteries, groupe de secours ; dist_capex : réseau BT, branchements, compteurs
    opex : exploitation technique annuelle ; commercial_cost : facturation, recouvrement (USD/an)
    losses : pertes techniques et non techniques (part de la production non facturée)
    Les remplacements de batteries doivent être inclus dans opex en annuité équivalente.
    """
    sold = generated_mwh * (1 - losses)
    k = crf(rate, years)
    parts = {
        "production": (gen_capex * k + opex) / sold,
        "distribution": dist_capex * k / sold,
        "commercial": commercial_cost / sold,
    }
    parts["total"] = sum(parts.values())
    return parts


def minigrid_subsidy(cost_of_service_mwh: float, tariff_mwh: float, sold_mwh: float,
                     rate: float, years: int) -> float:
    """Subvention d'investissement (année 0) qui ramène le coût complet au tarif autorisé."""
    gap = max(0.0, cost_of_service_mwh - tariff_mwh) * sold_mwh
    return gap / crf(rate, years)


if __name__ == "__main__":
    # Cas illustratif de la proposition : 50 MWp, 50 M USD, 90 GWh/an, 0,75 M USD/an, 25 ans.
    base = lcoe(50e6, 750e3, 90_000, 0.04, 25)
    for r in (0.04, 0.06, 0.08, 0.10, 0.12, 0.14):
        v = lcoe(50e6, 750e3, 90_000, r, 25)
        v_deg = lcoe(50e6, 750e3, 90_000, r, 25, degradation=0.005, opex_escalation=0.02)
        print(f"WACC {r:.0%}: {v:5.1f} USD/MWh (+{v / base - 1:5.1%})   "
              f"avec dégradation 0,5 %/an et OPEX +2 %/an : {v_deg:5.1f}")
