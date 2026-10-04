"""Synthèse par arrondissement : croise population (WorldPop 2025, data/population/),
occupation du sol (WorldCover 2021) et ressources forestières/minières (Atlas forestier
MINFOF/WRI, paquet 2018). Ne lit que les CSV déjà produits (aucune donnée brute).

Usage : python3 data/ressources/scripts/04_synthese.py
"""
import os

import pandas as pd

ICI = os.path.join(os.path.dirname(__file__), "..")
POP = os.path.join(ICI, "..", "population", "population_par_arrondissement.csv")


def main():
    p = pd.read_csv(POP)
    o = pd.read_csv(os.path.join(ICI, "occupation_sol_par_arrondissement.csv"))
    r = pd.read_csv(os.path.join(ICI, "ressources_forestieres_minieres_par_arrondissement.csv"))
    d = p[["arrondissement_id", "arrondissement_nom", "departement", "region", "superficie_km2",
           "pop_2025", "densite_2025_hab_km2"]].merge(
        o.drop(columns=["arrondissement_nom", "source"]), on="arrondissement_id", validate="1:1").merge(
        r.drop(columns=["arrondissement_nom", "source", "date_situation"]), on="arrondissement_id", validate="1:1")
    sup_ha = d.superficie_km2 * 100
    s = pd.DataFrame({
        "arrondissement_id": d.arrondissement_id,
        "arrondissement_nom": d.arrondissement_nom,
        "departement": d.departement,
        "region": d.region,
        "superficie_km2": d.superficie_km2,
        "pop_2025_estimee": d.pop_2025,
        "densite_2025_hab_km2": d.densite_2025_hab_km2,
        "foret_arboree_ha": d.foret_arboree_ha,
        "part_foret_arboree_pct": d.part_foret_arboree_pct,
        "savane_prairie_arbustes_ha": (d.prairie_savane_herbacee_ha + d.arbustes_ha).round(1),
        "cultures_ha": d.cultures_ha,
        "part_cultures_pct": d.part_cultures_pct,
        "bati_ha": d.bati_ha,
        "eau_permanente_ha": d.eau_permanente_ha,
        "zones_humides_mangroves_ha": (d.zone_humide_herbacee_ha + d.mangroves_ha).round(1),
        "cultures_ha_par_habitant": (d.cultures_ha / d.pop_2025).round(4),
        "foret_ha_par_habitant": (d.foret_arboree_ha / d.pop_2025).round(4),
        "ufa_ha": d.ufa_ha,
        "foret_communale_ha": d.foret_communale_ha,
        "foret_communautaire_ha": d.foret_communautaire_ha,
        "aire_protegee_ha": d.aire_protegee_ha,
        "part_aire_protegee_pct": (100 * d.aire_protegee_ha / sup_ha).round(2),
        "permis_recherche_miniere_ha": d.permis_recherche_miniere_ha,
        "permis_exploitation_miniere_ha": d.permis_exploitation_miniere_ha,
        "nb_ufa": d.ufa_nb,
        "nb_forets_communautaires": d.foret_communautaire_nb,
        "nb_aires_protegees": d.aire_protegee_nb,
        "nb_permis_miniers": d.permis_recherche_miniere_nb + d.permis_exploitation_miniere_nb,
        "sources": "WORLDPOP_R2025A_CN_100M;ESA_WORLDCOVER_2021_V200;MINFOF_WRI_ATLAS_FORESTIER_SIG_2018;GEOBOUNDARIES_CMR_ADM3_9469f09",
        "millesimes": "pop=2025 (estimation modélisée) ; occupation du sol=2021 ; atlas forestier=2015-2019",
    })
    s.to_csv(os.path.join(ICI, "synthese_par_arrondissement.csv"), index=False, encoding="utf-8")
    print(len(s), "lignes ;", s.isna().sum().sum(), "valeurs manquantes")
    print(s[["pop_2025_estimee", "foret_arboree_ha", "cultures_ha", "bati_ha", "aire_protegee_ha", "ufa_ha"]].sum())


if __name__ == "__main__":
    main()
