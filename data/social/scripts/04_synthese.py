"""Synthèse : nombre d'établissements par arrondissement, source et type.

Jointure spatiale point-dans-polygone avec geoBoundaries CMR ADM3 (gbOpen, commit 9469f09,
360 unités ; limites non commitées). Les points hors de tout polygone (tolérance d'emprise de
~1 km dans 02_couches.py) sont comptés sur la ligne gb_shape_id = HORS_LIMITES.

Format long : une ligne par (arrondissement, source, couche, tg_type), zéros compris pour les
combinaisons présentes dans la couche. tg_type vide = entité non classée (valeur brute
conservée dans la couche). NE PAS additionner les sources santé entre elles : elles se
recouvrent (voir sante/rapprochement_sources_sante.csv).
"""
import json

import geopandas as gpd
import pandas as pd

from commun import SOCIAL, TMP, charger_adm3

COUCHES = {
    "sante_osm": "sante/etablissements_sante_osm.geojson",
    "sante_healthsites": "sante/etablissements_sante_healthsites.geojson",
    "sante_maina": "sante/etablissements_sante_publics_maina2019.geojson",
    "education_osm": "education/etablissements_education_osm.geojson",
    "mairies_osm": "services/mairies_osm.geojson",
    "marches_osm": "services/marches_osm.geojson",
}

adm3 = charger_adm3()
blocs = []
hors = {}
for nom, fichier in COUCHES.items():
    g = gpd.read_file(SOCIAL / fichier)
    j = gpd.sjoin(g, adm3, how="left", predicate="within")
    # Un point exactement sur une limite peut tomber dans deux polygones : on garde le premier.
    j = j[~j.index.duplicated(keep="first")]
    j["gb_shape_id"] = j["gb_shape_id"].fillna("HORS_LIMITES")
    j["arrondissement"] = j["arrondissement"].fillna("")
    j["tg_type"] = j["tg_type"].fillna("")
    hors[nom] = int((j["gb_shape_id"] == "HORS_LIMITES").sum())
    types = sorted(j["tg_type"].unique())
    base = adm3[["gb_shape_id", "arrondissement"]].drop_duplicates()
    if hors[nom]:
        base = pd.concat([base, pd.DataFrame([{"gb_shape_id": "HORS_LIMITES", "arrondissement": ""}])])
    grille = base.merge(pd.DataFrame({"tg_type": types}), how="cross")
    c = j.groupby(["gb_shape_id", "tg_type"]).size().rename("nombre").reset_index()
    out = grille.merge(c, on=["gb_shape_id", "tg_type"], how="left").fillna({"nombre": 0})
    out["source"] = g["source"].iloc[0]
    out["couche"] = fichier
    blocs.append(out)
    assert int(out["nombre"].sum()) == len(g), nom

S = pd.concat(blocs, ignore_index=True)
S["nombre"] = S["nombre"].astype(int)
S = S[["gb_shape_id", "arrondissement", "source", "couche", "tg_type", "nombre"]]
S = S.sort_values(["arrondissement", "gb_shape_id", "couche", "tg_type"]).reset_index(drop=True)
S.to_csv(SOCIAL / "synthese_par_arrondissement.csv", index=False)

ctl = {"lignes": int(len(S)), "arrondissements": int(adm3["gb_shape_id"].nunique()),
       "points_hors_limites_adm3": hors,
       "arrondissements_sans_aucun_etablissement_osm_sante":
           int((S[S.couche == COUCHES["sante_osm"]].groupby("gb_shape_id")["nombre"].sum() == 0).sum()),
       "arrondissements_sans_aucune_ecole_osm":
           int((S[S.couche == COUCHES["education_osm"]].groupby("gb_shape_id")["nombre"].sum() == 0).sum()),
       "arrondissements_sans_mairie_osm":
           int((S[S.couche == COUCHES["mairies_osm"]].groupby("gb_shape_id")["nombre"].sum() == 0).sum()),
       "noms_arrondissement_dupliques": int(adm3["arrondissement"].duplicated().sum())}
with open(TMP / "controles_synthese.json", "w") as fh:
    json.dump(ctl, fh, ensure_ascii=False, indent=2)
print(json.dumps(ctl, ensure_ascii=False, indent=1))
