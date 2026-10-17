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


if __name__ == "__main__":
    # Cas illustratif de la proposition : 50 MWp, 50 M USD, 90 GWh/an, 0,75 M USD/an, 25 ans.
    base = lcoe(50e6, 750e3, 90_000, 0.04, 25)
    for r in (0.04, 0.06, 0.08, 0.10, 0.12, 0.14):
        v = lcoe(50e6, 750e3, 90_000, r, 25)
        v_deg = lcoe(50e6, 750e3, 90_000, r, 25, degradation=0.005, opex_escalation=0.02)
        print(f"WACC {r:.0%}: {v:5.1f} USD/MWh (+{v / base - 1:5.1%})   "
              f"avec dégradation 0,5 %/an et OPEX +2 %/an : {v_deg:5.1f}")
