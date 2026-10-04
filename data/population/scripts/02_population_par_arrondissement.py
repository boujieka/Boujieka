"""Agrège la population maillée WorldPop (R2025A, constrained, 100 m) par arrondissement
(geoBoundaries CMR ADM3).

Méthode : chaque pixel est affecté à l'arrondissement qui contient son CENTRE
(rasterisation des polygones sur la grille WorldPop), puis les valeurs sont sommées.
Aucun pixel n'est compté deux fois. Les pixels hors de tout polygone sont rapportés
dans le contrôle. Surface : aire géodésique (ellipsoïde WGS84) des polygones.

Usage : RAW=/chemin/temp python3 data/population/scripts/02_population_par_arrondissement.py
"""
import gzip
import csv
import json
import os

import geopandas as gpd
import numpy as np
import rasterio
from pyproj import Geod
from rasterio import features

RAW = os.environ.get("RAW", "./raw_population")
OUT = os.path.join(os.path.dirname(__file__), "..")
ANNEES = [2025, 2026]
GEOD = Geod(ellps="WGS84")


def aire_km2(geom):
    return abs(GEOD.geometry_area_perimeter(geom)[0]) / 1e6


def corrige_nom(n):
    """Les noms geoBoundaries CMR ADM3 contiennent du « mojibake » (UTF-8 lu en Latin-1,
    ex. « TignÃ¨re »). On le répare seulement si le ré-encodage est sans perte."""
    if n and ("Ã" in n or "Â" in n):
        try:
            return n.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            return n
    return n


def parents(adm3):
    """Département / région de chaque arrondissement par recouvrement maximal avec la
    couche « arrondissements » du paquet SIG 2018 de l'Atlas forestier (MINFOF/WRI)."""
    ref = gpd.read_file(os.path.join(RAW, "donnees_ouverts_fr.gdb"), layer="arrondissements")
    ref = ref[["nom_arr", "nom_dep", "nom_reg", "geometry"]].to_crs(6933)
    a = adm3[["shapeID", "geometry"]].to_crs(6933)
    inter = gpd.overlay(a, ref, how="intersection", keep_geom_type=True)
    inter["a"] = inter.area
    best = inter.sort_values("a", ascending=False).drop_duplicates("shapeID")
    best = best.merge(a.assign(tot=a.area)[["shapeID", "tot"]], on="shapeID")
    best["part_recouvrement"] = (best["a"] / best["tot"]).round(3)
    return best.set_index("shapeID")[["nom_arr", "nom_dep", "nom_reg", "part_recouvrement"]]


def main():
    adm3 = gpd.read_file(os.path.join(RAW, "gb_adm3.geojson")).reset_index(drop=True)
    adm3["uid"] = np.arange(1, len(adm3) + 1, dtype=np.int32)
    adm3["superficie_km2"] = adm3.geometry.apply(aire_km2)
    par = parents(adm3)

    sommes, totaux_raster, hors = {}, {}, {}
    for an in ANNEES:
        f = os.path.join(RAW, f"cmr_pop_{an}_CN_100m_R2025A_v1.tif")
        with rasterio.open(f) as r:
            arr = r.read(1)
            nod = r.nodata
            ids = features.rasterize(
                zip(adm3.geometry, adm3.uid), out_shape=arr.shape, transform=r.transform,
                fill=0, dtype="int32", all_touched=False)
        v = np.where((arr == nod) | ~np.isfinite(arr), 0, arr).astype(np.float64)
        s = np.bincount(ids.ravel(), weights=v.ravel(), minlength=len(adm3) + 1)
        sommes[an] = s
        totaux_raster[an] = float(v.sum())
        hors[an] = float(s[0])

    cols = ["arrondissement_id", "arrondissement_nom", "nom_minfof_2018", "departement", "region",
            "part_recouvrement_minfof",
            "superficie_km2", "pop_2025", "densite_2025_hab_km2", "pop_2026",
            "densite_2026_hab_km2", "type_donnee", "source", "source_limites"]
    rows = []
    for _, z in adm3.iterrows():
        p = par.loc[z.shapeID] if z.shapeID in par.index else None
        row = {
            "arrondissement_id": z.shapeID,
            "arrondissement_nom": corrige_nom(z.shapeName),
            "nom_minfof_2018": p.nom_arr if p is not None else "",
            "part_recouvrement_minfof": p.part_recouvrement if p is not None else "",
            "departement": p.nom_dep if p is not None else "",
            "region": p.nom_reg if p is not None else "",
            "superficie_km2": round(z.superficie_km2, 2),
            "type_donnee": "ESTIMATION_MODELISEE",
            "source": "WORLDPOP_R2025A_CN_100M",
            "source_limites": "GEOBOUNDARIES_CMR_ADM3_9469f09",
        }
        for an in ANNEES:
            pop = sommes[an][z.uid]
            row[f"pop_{an}"] = int(round(pop))
            row[f"densite_{an}_hab_km2"] = round(pop / z.superficie_km2, 1)
        rows.append(row)
    rows.sort(key=lambda r: (r["region"], r["departement"], r["arrondissement_nom"]))
    with open(os.path.join(OUT, "population_par_arrondissement.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    # Seconde source : ONU WPP 2024, variante moyenne, population au 1er juillet (milliers)
    wpp = {}
    with gzip.open(os.path.join(RAW, "wpp2024_demo.csv.gz"), "rt", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            if r["ISO3_code"] == "CMR" and r["Time"] in {str(a) for a in ANNEES}:
                wpp[int(r["Time"])] = (float(r["TPopulation1Jan"]) * 1000,
                                       float(r["TPopulation1July"]) * 1000)
    sup_tot = float(adm3.superficie_km2.sum())
    comp = []
    for an in ANNEES:
        s_adm = float(sommes[an][1:].sum())
        comp.append({
            "annee": an,
            "worldpop_total_raster": int(round(totaux_raster[an])),
            "worldpop_somme_arrondissements": int(round(s_adm)),
            "worldpop_hors_arrondissements": int(round(hors[an])),
            "onu_wpp2024_moyenne_1er_janvier": int(round(wpp[an][0])),
            "onu_wpp2024_moyenne_1er_juillet": int(round(wpp[an][1])),
            "ecart_worldpop_moins_onu_1er_janvier": int(round(totaux_raster[an] - wpp[an][0])),
            "ecart_worldpop_moins_onu_1er_juillet": int(round(totaux_raster[an] - wpp[an][1])),
            "ecart_pct_1er_juillet": round(100 * (totaux_raster[an] - wpp[an][1]) / wpp[an][1], 3),
            "superficie_somme_arrondissements_km2": round(sup_tot, 1),
        })
    with open(os.path.join(OUT, "population_totaux_comparaison.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(comp[0]))
        w.writeheader()
        w.writerows(comp)

    ctrl = {
        "nb_arrondissements": len(adm3),
        "noms_dupliques": int(adm3.shapeName.duplicated().sum()),
        "noms_corriges_encodage": int(sum(corrige_nom(n) != n for n in adm3.shapeName)),
        "noms_encore_suspects": [corrige_nom(n) for n in adm3.shapeName if "Ã" in corrige_nom(n) or "\ufffd" in corrige_nom(n)],
        "emprise": [round(x, 4) for x in adm3.total_bounds],
        "superficie_totale_km2": round(sup_tot, 1),
        "rattachement_parent_recouvrement_min": float(par.part_recouvrement.min()),
        "rattachement_parent_recouvrement_lt_0_5": int((par.part_recouvrement < 0.5).sum()),
        "nb_regions": int(par.nom_reg.nunique()),
        "nb_departements": int(par.nom_dep.nunique()),
        "arrondissements_pop_nulle_2025": int(sum(1 for r in rows if r["pop_2025"] == 0)),
        "comparaison": comp,
    }
    print(json.dumps(ctrl, ensure_ascii=False, indent=1, default=str))
    with open(os.path.join(RAW, "controle_population.json"), "w") as fh:
        json.dump(ctrl, fh, ensure_ascii=False, indent=1, default=str)


if __name__ == "__main__":
    main()
