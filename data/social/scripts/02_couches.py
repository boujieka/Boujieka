"""Construction des couches GeoJSON (une par source et par thème) + contrôles internes.

Entrées : $TMP/osm_brut.parquet, $RAW/healthsites_cameroon.geojson, $RAW/maina_figshare.xlsx,
          $RAW/gb_cmr_adm3.geojson (filtre d'emprise uniquement)
Sorties : data/social/{sante,education,services}/*.geojson, $TMP/controles_couches.json
"""
import json

import geopandas as gpd
import numpy as np
import pandas as pd
from rapidfuzz import fuzz
from shapely.geometry import Point

from commun import (BBOX, DATE_HS, DATE_MAINA, DATE_OSM, RAW, SOCIAL, SRC_HS, SRC_MAINA,
                    SRC_OSM, TMP, charger_adm3, classer_education, classer_sante,
                    ecrire_geojson, masque_cameroun, norm)

SANTE_AMENITY = {"hospital", "clinic", "doctors", "pharmacy", "dentist"}
EDU_AMENITY = {"school", "college", "university", "kindergarten"}
CRS_M = 32633  # UTM 33N, pour les distances métriques

controles = {}
adm3 = charger_adm3()
MASQUES = {"strict": masque_cameroun(adm3, 0), "tol_1km": masque_cameroun(adm3)}


def filtrer_emprise(gdf, nom, masque):
    """Garde les points dans la bbox ET dans les limites du Cameroun (strict ou tolérance ~1 km)."""
    n0 = len(gdf)
    x, y = gdf.geometry.x, gdf.geometry.y
    in_bbox = (x >= BBOX[0]) & (x <= BBOX[2]) & (y >= BBOX[1]) & (y <= BBOX[3])
    in_cmr = gdf.geometry.intersects(MASQUES[masque])
    out = gdf[in_bbox & in_cmr].copy()
    controles.setdefault(nom, {})["emprise"] = {
        "entites_avant_filtre": int(n0),
        "hors_bbox": int((~in_bbox).sum()),
        "filtre_limites": masque,
        "hors_limites_cameroun": int((~in_cmr).sum()),
        "conservees": int(len(out)),
        "bbox_resultat": [round(v, 4) for v in out.total_bounds.tolist()] if len(out) else None,
    }
    return out


def doublons_internes(gdf, dist_m=100, seuil_nom=90):
    """Signale les paires (même couche) à < dist_m et noms normalisés similaires (>= seuil),
    ou de coordonnées identiques. Ne supprime rien."""
    g = gdf.to_crs(CRS_M)
    xy = np.c_[g.geometry.x.values, g.geometry.y.values]
    noms = [norm(v) for v in gdf["nom"].values]
    ids = gdf["source_id"].values
    idx = g.sindex
    flags = [[] for _ in range(len(g))]
    paires = 0
    paires_coord = 0
    q_in, q_tree = idx.query(g.geometry.buffer(dist_m), predicate="intersects")
    for i, j in zip(q_in, q_tree):
        if j <= i:
            continue
        meme_coord = xy[i, 0] == xy[j, 0] and xy[i, 1] == xy[j, 1]
        sim = fuzz.token_sort_ratio(noms[i], noms[j]) if noms[i] and noms[j] else 0
        if meme_coord or sim >= seuil_nom:
            paires += 1
            paires_coord += int(meme_coord)
            flags[i].append(ids[j])
            flags[j].append(ids[i])
    gdf = gdf.copy()
    gdf["doublon_interne_suspect"] = [";".join(f) if f else None for f in flags]
    return gdf, {"regle": f"distance < {dist_m} m et similarité de nom (token_sort_ratio) >= {seuil_nom}, "
                          "ou coordonnées identiques",
                 "paires_suspectes": paires, "dont_coordonnees_identiques": paires_coord,
                 "entites_concernees": int(sum(1 for f in flags if f))}


def comptes(gdf):
    return {str(k): int(v) for k, v in gdf["tg_type"].fillna("null").value_counts().items()}


def finaliser(gdf, nom_couche, chemin, colonnes, masque="strict"):
    gdf = filtrer_emprise(gdf, nom_couche, masque)
    gdf, dbl = doublons_internes(gdf)
    gdf = gdf[colonnes + ["doublon_interne_suspect", "geometry"]]
    gdf = gdf.sort_values("source_id").reset_index(drop=True)
    controles[nom_couche].update({"fichier": str(chemin.relative_to(SOCIAL)),
                                  "nb_entites": int(len(gdf)),
                                  "comptes_par_tg_type": comptes(gdf),
                                  "doublons_internes": dbl})
    ecrire_geojson(gdf, chemin)
    gdf.to_parquet(TMP / f"{nom_couche}.parquet", index=False)
    return gdf


# ---------------------------------------------------------------- OSM
osm = pd.read_parquet(TMP / "osm_brut.parquet")
osm = gpd.GeoDataFrame(osm, geometry=gpd.points_from_xy(osm.lon, osm.lat), crs=4326)
osm["nom"] = osm["name"].fillna("")
osm["source"] = SRC_OSM
osm["statut"] = "IMPORTE"
osm["date_source"] = DATE_OSM
osm["operator_type"] = osm["operator:type"].fillna(osm["operator_type"])
osm = osm.rename(columns={"healthcare:speciality": "healthcare_speciality",
                          "isced:level": "isced_level", "townhall:type": "townhall_type",
                          "name:fr": "nom_fr", "name:en": "nom_en",
                          "source": "source", "check_date": "check_date"})
# Un objet n'appartient qu'à un thème : l'amenity prime, healthcare=* sinon.
is_edu = osm["amenity"].isin(EDU_AMENITY)
is_srv = osm["amenity"].isin({"townhall", "marketplace"})
is_sante = osm["amenity"].isin(SANTE_AMENITY) | (osm["healthcare"].notna() & ~is_edu & ~is_srv)
controles["osm_repartition_themes"] = {
    "sante": int(is_sante.sum()), "education": int(is_edu.sum()),
    "mairies": int((osm.amenity == "townhall").sum()),
    "marches": int((osm.amenity == "marketplace").sum()),
    "objets_edu_ou_service_avec_tag_healthcare": int((osm["healthcare"].notna() & (is_edu | is_srv)).sum()),
}

COMMUNS = ["tg_type", "nom", "source_id", "source", "statut", "date_source"]

s = osm[is_sante].copy()
cls = s.apply(lambda r: classer_sante({"amenity": r["amenity"] or "",
                                       "healthcare": r["healthcare"] or "",
                                       "name": r["nom"]}), axis=1)
s["tg_type"] = [c[0] for c in cls]
s["classement_regle"] = [c[1] for c in cls]
sante_osm = finaliser(s, "sante_osm", SOCIAL / "sante/etablissements_sante_osm.geojson",
                      COMMUNS + ["classement_regle", "amenity", "healthcare", "healthcare_speciality",
                                 "operator_type", "beds", "emergency", "nom_fr", "nom_en",
                                 "osm_type", "date_maj_objet"])

e = osm[is_edu].copy()
cls = e.apply(lambda r: classer_education({"amenity": r["amenity"] or "",
                                           "isced:level": r["isced_level"] or "",
                                           "name": r["nom"]}), axis=1)
e["tg_type"] = [c[0] for c in cls]
e["classement_regle"] = [c[1] for c in cls]
finaliser(e, "education_osm", SOCIAL / "education/etablissements_education_osm.geojson",
          COMMUNS + ["classement_regle", "amenity", "isced_level", "school", "operator_type",
                     "religion", "nom_fr", "nom_en", "osm_type", "date_maj_objet"])

m = osm[osm.amenity == "townhall"].copy()
m["tg_type"] = "SOC.ADMIN.MAIRIE"
finaliser(m, "mairies_osm", SOCIAL / "services/mairies_osm.geojson",
          COMMUNS + ["amenity", "townhall_type", "admin_level", "nom_fr", "nom_en",
                     "osm_type", "date_maj_objet"])

k = osm[osm.amenity == "marketplace"].copy()
k["tg_type"] = "ECO.MARCHE"
finaliser(k, "marches_osm", SOCIAL / "services/marches_osm.geojson",
          COMMUNS + ["amenity", "opening_hours", "nom_fr", "nom_en", "osm_type", "date_maj_objet"])

# ---------------------------------------------------------- healthsites.io
hs = gpd.read_file(RAW / "healthsites_cameroon.geojson")
controles["sante_healthsites"] = {"geometries_source": {str(k): int(v) for k, v in
                                                        hs.geom_type.value_counts().items()}}
hs = hs.set_crs(4326, allow_override=True)
hs["geometry"] = [g if g.geom_type == "Point" else g.centroid for g in hs.geometry]  # centroïde des surfaces
hs["nom"] = hs["name"].fillna("")
hs["source_id"] = hs["osm_type"].astype(str) + "/" + hs["osm_id"].astype("Int64").astype(str)
hs["source"] = SRC_HS
hs["statut"] = "IMPORTE"
hs["date_source"] = DATE_HS
hs["healthsites_uuid"] = hs["uuid"]
hs["date_maj_objet"] = hs["changeset_timestamp"].astype(str).str[:10]
cls = hs.apply(lambda r: classer_sante({"amenity": r["amenity"] or "",
                                        "healthcare": r["healthcare"] or "",
                                        "name": r["nom"]}), axis=1)
hs["tg_type"] = [c[0] for c in cls]
hs["classement_regle"] = [c[1] for c in cls]
for c in ["healthcare", "operator_type", "operational_status", "beds", "emergency", "amenity"]:
    hs[c] = hs[c].replace("", None)
finaliser(hs, "sante_healthsites", SOCIAL / "sante/etablissements_sante_healthsites.geojson",
          COMMUNS + ["classement_regle", "amenity", "healthcare", "operator_type",
                     "operational_status", "beds", "emergency", "completeness",
                     "healthsites_uuid", "date_maj_objet"], masque="tol_1km")

# ------------------------------------------------------------- Maina 2019
mx = pd.read_excel(RAW / "maina_figshare.xlsx", sheet_name="SSA MFL")
mx["ligne_excel"] = mx.index + 2  # ligne 1 = en-tête
mc = mx[mx["Country"] == "Cameroon"].copy()
sans_coord = mc["Lat"].isna() | mc["Long"].isna()
controles["sante_maina"] = {"lignes_cameroun_source": int(len(mc)),
                            "lignes_sans_coordonnees_exclues": int(sans_coord.sum())}
mc = mc[~sans_coord]
TYPE_MAINA = {
    "Centre de Santé Intégré": "SOC.SANTE.CENTRE", "Health Centre": "SOC.SANTE.CENTRE",
    "Centre Medical d’Arrondissement": "SOC.SANTE.CENTRE", "Dispensaire": "SOC.SANTE.CENTRE",
    "Hôpital de District": "SOC.SANTE.HOPITAL", "Hôpital Régional": "SOC.SANTE.HOPITAL",
    "Hôpital Général": "SOC.SANTE.HOPITAL", "Hôpital Centraux": "SOC.SANTE.HOPITAL",
    "Clinic": "SOC.SANTE.CLINIQUE",
}
mg = gpd.GeoDataFrame(mc, geometry=[Point(xy) for xy in zip(mc["Long"], mc["Lat"])], crs=4326)
mg["tg_type"] = mg["Facility type"].map(TYPE_MAINA)
mg["classement_regle"] = np.where(mg["tg_type"].notna(), "type_source", "non_classe")
mg["nom"] = mg["Facility name"].fillna("")
mg["source_id"] = "SSA_MFL/ligne_" + mg["ligne_excel"].astype(str)
mg["source"] = SRC_MAINA
mg["statut"] = "IMPORTE"
mg["date_source"] = DATE_MAINA
mg = mg.rename(columns={"Facility type": "type_source", "Ownership": "gestionnaire",
                        "Admin1": "region_source", "LL source": "source_coordonnees"})
finaliser(mg, "sante_maina", SOCIAL / "sante/etablissements_sante_publics_maina2019.geojson",
          COMMUNS + ["classement_regle", "type_source", "gestionnaire", "region_source",
                     "source_coordonnees"], masque="tol_1km")

with open(TMP / "controles_couches.json", "w") as fh:
    json.dump(controles, fh, ensure_ascii=False, indent=2)
print(json.dumps(controles, ensure_ascii=False, indent=1))
