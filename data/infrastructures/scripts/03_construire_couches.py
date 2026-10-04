#!/usr/bin/env python3
"""Construit les couches publiées, la synthèse par arrondissement, les contrôles et le manifest.

Usage : python3 03_construire_couches.py RAW_DIR WORK_DIR OUT_DIR
  RAW_DIR  : sources téléchargées par 01_telecharger.sh
  WORK_DIR : GeoParquet produits par 02_extraire_osm.py
  OUT_DIR  : data/infrastructures
"""
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import shapely
from pyproj import Geod

RAW, WORK, OUT = (Path(p) for p in sys.argv[1:4])
OUT.mkdir(parents=True, exist_ok=True)
GEOD = Geod(ellps="WGS84")
TODAY = date.today().isoformat()
BBOX = (8.4, 1.6, 16.2, 13.1)
SIMPLIFY_TOL = 0.00005  # degrés (~5,5 m) ; longueurs calculées AVANT simplification
BUFFER_DEG = 0.01        # ~1,1 km de tolérance aux frontières (écarts geoBoundaries / OSM)
MANIFEST, CONTROLES = [], {}

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

SHA = {k: sha256(RAW / f) for k, f in {
    "osm": "cameroon-latest.osm.pbf", "oa": "airports.csv", "adm3": "adm3.geojson",
    "grid": "grid.gpkg", "wpi": "wpi.csv"}.items() if (RAW / f).exists()}
OSM_TS = (WORK / "osm_timestamp.txt").read_text().strip()
OSM_DATE = OSM_TS[:10]
OSM_CODE = f"OSM_OSMFR_{OSM_DATE}"
OSM_META = dict(producteur="Contributeurs OpenStreetMap, extrait download.openstreetmap.fr",
                url="https://download.openstreetmap.fr/extracts/africa/cameroon-latest.osm.pbf",
                licence="ODbL 1.0", attribution="© les contributeurs d'OpenStreetMap",
                date_situation=OSM_DATE, sha256_source=SHA["osm"])

# ---------- limites (jointure uniquement, non commitées) ----------
adm3 = gpd.read_file(RAW / "adm3.geojson")[["shapeID", "shapeName", "geometry"]]
adm3["geometry"] = adm3.geometry.make_valid()
pays = shapely.union_all(adm3.geometry.values)
pays_tol = pays.buffer(BUFFER_DEG)

def geod_len(g):
    return float(GEOD.geometry_length(g)) if g is not None and not g.is_empty else 0.0

def finalize(gdf, tg_type, source):
    gdf = gdf.copy()
    gdf.insert(0, "tg_type", tg_type)
    gdf["source"] = source
    gdf["statut"] = "IMPORTE"
    gdf["date_source"] = OSM_DATE if source == OSM_CODE else gdf.get("date_source")
    cols = ["tg_type", "nom", "source_id", "source", "statut", "date_source"]
    return gdf[cols + [c for c in gdf.columns if c not in cols + ["geometry"]] + ["geometry"]]

def write(gdf, name, meta, methode, limites, extra_ctrl=None):
    path = OUT / f"{name}.geojson"
    gdf = gdf.copy()
    gdf["geometry"] = shapely.set_precision(gdf.geometry.values, 1e-6)
    gdf = gdf[~gdf.geometry.is_empty]
    gdf.to_file(path, driver="GeoJSON", COORDINATE_PRECISION=6, WRITE_BBOX="NO")
    b = gdf.total_bounds
    ctrl = {
        "nb_entites": int(len(gdf)),
        "geometries_valides": bool(gdf.geometry.is_valid.all()),
        "emprise": [round(float(x), 4) for x in b] if len(gdf) else None,
        "dans_emprise_cameroun": bool(len(gdf) == 0 or (b[0] >= BBOX[0] and b[1] >= BBOX[1]
                                                        and b[2] <= BBOX[2] and b[3] <= BBOX[3])),
        "taille_mo": round(path.stat().st_size / 1e6, 2),
    }
    if extra_ctrl:
        ctrl.update(extra_ctrl)
    CONTROLES[name] = ctrl
    MANIFEST.append({"fichier": f"infrastructures/{name}.geojson", **meta,
                     "date_telechargement": TODAY, "sha256_fichier": sha256(path),
                     "nb_entites": int(len(gdf)), "methode": methode, "limites": limites,
                     "controle": json.dumps(ctrl, ensure_ascii=False)})
    print(name, ctrl)
    return gdf

def clip_lines(gdf):
    """Découpe des lignes à l'emprise Cameroun (+ tolérance) ; longueur géodésique avant simplification."""
    gdf = gdf.copy()
    gdf["geometry"] = gdf.geometry.intersection(pays_tol)
    gdf = gdf[~gdf.geometry.is_empty]
    gdf["geometry"] = gdf.geometry.apply(
        lambda g: shapely.line_merge(g) if g.geom_type == "MultiLineString" else g)
    gdf = gdf[gdf.geom_type.isin(["LineString", "MultiLineString"])]
    gdf["longueur_m"] = gdf.geometry.apply(geod_len).round(1)
    return gdf

def simplify(gdf):
    gdf = gdf.copy()
    gdf["geometry"] = gdf.geometry.simplify(SIMPLIFY_TOL, preserve_topology=True)
    return gdf

def clip_points(gdf):
    n0 = len(gdf)
    gdf = gdf[gdf.geometry.within(pays_tol)].copy()
    return gdf, n0 - len(gdf)

def dup_pairs(gdf, dist_m=200):
    """Nombre de paires d'objets de la même couche à moins de dist_m (doublons possibles)."""
    if len(gdf) < 2:
        return 0
    p = gdf.to_crs(3857)  # distance approximative, suffisante pour un signalement
    s = p.sindex.query(p.geometry.buffer(dist_m / np.cos(np.radians(6))), predicate="intersects")
    return int(((s[0] < s[1])).sum())

SYN = {}  # couche -> GeoDataFrame utilisé pour la synthèse (lignes non simplifiées / points)

# ---------- 1. routes ----------
routes = clip_lines(gpd.read_parquet(WORK / "routes.parquet"))
SYN_ROUTES = routes
lim_routes = ("Complétude OSM inégale (bonne sur les axes principaux, plus faible en zone rurale et dans "
              "l'Extrême-Nord/Est) ; classes OSM (motorway..tertiary) ≠ classement administratif "
              "MINTP (routes nationales/régionales/départementales) ; tag surface souvent absent "
              "(voir taux par classe dans controle) ; géométries simplifiées (tolérance 5e-5°, ~5 m) pour "
              "la publication, longueurs calculées avant simplification ; tronçons découpés à "
              "l'emprise Cameroun (geoBoundaries ADM3 + tampon ~1 km).")
for cl in ["motorway", "trunk", "primary", "secondary", "tertiary"]:
    sub = routes[routes.classe == cl]
    ctrl = {"longueur_totale_km": round(sub.longueur_m.sum() / 1000, 1),
            "longueur_bretelles_km": round(sub[sub.bretelle].longueur_m.sum() / 1000, 1),
            "part_longueur_avec_surface": round(float(sub[sub.surface.notna()].longueur_m.sum()
                                                      / max(sub.longueur_m.sum(), 1)), 3),
            "surface_km": {k: round(v / 1000, 1) for k, v in
                           sub.groupby(sub.surface.fillna("non_renseigne")).longueur_m.sum()
                           .sort_values(ascending=False).head(8).items()}}
    write(finalize(simplify(sub), "INF.ROUTE", OSM_CODE), f"routes_{cl}", {"source_code": OSM_CODE, **OSM_META},
          f"scripts/02_extraire_osm.py puis 03_construire_couches.py : ways highway={cl} et {cl}_link "
          "(bretelle=true), tags conservés name, ref, surface, lanes, oneway, bridge.", lim_routes, ctrl)

# ---------- 2. voies ferrées, ponts ----------
rail = clip_lines(gpd.read_parquet(WORK / "voies_ferrees.parquet"))
SYN_RAIL = rail
write(finalize(simplify(rail), "INF.VOIE_FERREE", OSM_CODE), "voies_ferrees", {"source_code": OSM_CODE, **OSM_META},
      "ways railway=rail (usage, service, gauge, operator, electrified conservés).",
      "Inclut les voies de service/embranchements (service=*) : la longueur totale surestime le linéaire "
      "de lignes principales ; voies doublées en gare comptées autant de fois.",
      {"longueur_totale_km": round(rail.longueur_m.sum() / 1000, 1),
       "longueur_hors_service_km": round(rail[rail.service.isna()].longueur_m.sum() / 1000, 1),
       "longueur_par_usage_km": {str(k): round(v / 1000, 1) for k, v in
                                 rail.groupby(rail.usage.fillna("non_renseigne")).longueur_m.sum().items()}})

ponts = clip_lines(gpd.read_parquet(WORK / "ponts.parquet"))
write(finalize(simplify(ponts), "INF.PONT", OSM_CODE), "ponts_routes_principales", {"source_code": OSM_CODE, **OSM_META},
      "ways highway=trunk|primary (et _link) avec bridge≠no ; un objet = un tronçon de route sur ouvrage.",
      "Un ouvrage peut être découpé en plusieurs tronçons (chaussées séparées) ; ponts des routes secondaires "
      "et inférieures non inclus ; présence du tag bridge dépendante des contributeurs.",
      {"longueur_totale_km": round(ponts.longueur_m.sum() / 1000, 2),
       "nb_ponts_100m_et_plus": int((ponts.longueur_m >= 100).sum()),
       "par_classe": ponts.classe_route.value_counts().to_dict()})

# ---------- 3. points OSM ----------
def point_layer(src, tg, name, methode, limites, transform=None):
    g = gpd.read_parquet(WORK / f"{src}.parquet")
    g, hors = clip_points(g)
    if transform:
        g = transform(g)
    SYN[name] = g
    ctrl = {"exclus_hors_cameroun": hors, "paires_a_moins_de_200m_doublons_possibles_ou_densite": dup_pairs(g),
            "geometrie_source": g.geometrie_source.value_counts().to_dict()}
    return write(finalize(g, tg, OSM_CODE), name, {"source_code": OSM_CODE, **OSM_META},
                 methode, limites, ctrl)

COMMON_PT = ("Objets surfaciques ramenés à un point représentatif (geometrie_source indique la géométrie "
             "d'origine). ")
point_layer("gares", "INF.GARE", "gares",
            "nodes/ways/relations railway=station|halt ou public_transport=station + train=yes.",
            COMMON_PT + "Gares et haltes ; certaines peuvent être désaffectées ; doublons nœud/surface possibles.")
point_layer("ports", "INF.PORT", "ports_osm",
            "objets landuse=port, industrial=port, harbour=yes ou seamark:type=harbour.",
            COMMON_PT + "Mélange de ports maritimes, fluviaux et débarcadères ; complétude faible pour les "
            "ports fluviaux ; voir aussi ports_wpi.geojson.")
point_layer("aerodromes", "INF.AEROPORT", "aerodromes_osm",
            "objets aeroway=aerodrome (tags icao, iata, aerodrome:type, ele conservés).",
            COMMON_PT + "Croisement avec OurAirports dans controles.json.")
point_layer("centrales", "INF.ENERGIE.CENTRALE", "centrales_electriques",
            "objets power=plant (plant:source, plant:method, plant:output:electricity conservés).",
            COMMON_PT + "Recensement OSM incomplet (petites centrales thermiques isolées et mini-centrales "
            "sous-représentées) ; puissance souvent non renseignée.")
point_layer("barrages", "INF.EAU.BARRAGE", "barrages",
            "objets waterway=dam (lignes, surfaces ou nœuds) ramenés à un point représentatif.",
            COMMON_PT + "Inclut de petites retenues et digues ; un même barrage peut être décrit par plusieurs "
            "objets (voir paires_a_moins_de_200m).")

def anonymise_eau(g):
    g = g.copy()
    g["nom_renseigne_dans_source"] = g.nom != ""
    g["nom"] = ""  # certains noms de points d'eau OSM sont des noms de personnes -> retirés
    g["type_point"] = np.where(g.man_made == "water_well", "puits_forage", "eau_potable")
    return g

point_layer("points_eau", "INF.EAU.FORAGE", "points_eau",
            "objets man_made=water_well ou amenity=drinking_water ; champ nom vidé (données personnelles).",
            COMMON_PT + "COMPLÉTUDE TRÈS FAIBLE : quelques milliers d'objets alors que le pays compte bien davantage "
            "de points d'eau ; cartographie concentrée sur des zones de projets humanitaires/HOT. amenity=drinking_water "
            "inclut bornes-fontaines et robinets, classés INF.EAU.FORAGE faute de code plus précis (voir type_point). "
            "operational_status rarement renseigné. Le champ nom est vidé car certains noms désignent des particuliers.",
            transform=anonymise_eau)
point_layer("antennes", "INF.TELECOM.ANTENNE", "antennes_telecom",
            "objets man_made=mast|tower avec tower:type=communication ou communication:mobile_phone=yes.",
            COMMON_PT + "Très incomplet : une petite fraction des sites réels est cartographiée dans OSM. "
            "Les bases OpenCelliD / Mozilla Location Service n'ont pas été utilisées (licence/usage non retenus).")

# Postes électriques : INF.ENERGIE.POSTE = sensibilité S1_RESTREINT -> pas de couche ponctuelle publiée
postes = gpd.read_parquet(WORK / "postes.parquet")
postes, postes_hors = clip_points(postes)
SYN_POSTES = postes
CONTROLES["postes_electriques_non_publies"] = {
    "nb_entites": int(len(postes)), "exclus_hors_cameroun": postes_hors,
    "par_substation": postes.substation.fillna("non_renseigne").value_counts().to_dict()}

# Lignes électriques
lignes = clip_lines(gpd.read_parquet(WORK / "lignes_electriques.parquet"))
def vclass(v):
    try:
        kv = max(float(x) for x in str(v).split(";")) / 1000
    except ValueError:
        return "non_renseigne"
    return "THT_>=150kV" if kv >= 150 else "HT_60-149kV" if kv >= 60 else "MT_<60kV"
lignes["classe_tension"] = lignes.voltage.apply(vclass)
SYN_LIGNES = lignes
write(finalize(simplify(lignes), "INF.ENERGIE.LIGNE", OSM_CODE), "lignes_electriques", {"source_code": OSM_CODE, **OSM_META},
      "ways power=line (voltage, cables, circuits, operator) ; classe_tension dérivée de voltage.",
      "Lignes de transport HT/THT principalement ; réseau MT/BT quasi absent d'OSM (power=minor_line non "
      "retenu) ; tension souvent non renseignée.",
      {"longueur_totale_km": round(lignes.longueur_m.sum() / 1000, 1),
       "longueur_par_classe_tension_km": {k: round(v / 1000, 1) for k, v in
                                          lignes.groupby("classe_tension").longueur_m.sum().items()}})

# ---------- 4. OurAirports ----------
oa = pd.read_csv(RAW / "airports.csv", keep_default_na=False, na_values=[""])
oa = oa[oa.iso_country == "CM"].copy()
oa_g = gpd.GeoDataFrame(oa, geometry=gpd.points_from_xy(oa.longitude_deg, oa.latitude_deg), crs=4326)
oa_g = oa_g.rename(columns={"name": "nom", "type": "type_ourairports"})
oa_g["source_id"] = "ourairports/" + oa_g["id"].astype(str)
OA_CODE = f"OURAIRPORTS_{TODAY}"
keep = ["nom", "source_id", "ident", "type_ourairports", "elevation_ft", "municipality", "iso_region",
        "scheduled_service", "icao_code", "iata_code", "gps_code", "geometry"]
oa_g = oa_g[[c for c in keep if c in oa_g.columns]]
oa_g["date_source"] = None

# croisement OurAirports / OSM
osm_ad = SYN["aerodromes_osm"].to_crs(3857)
oa_m = oa_g.to_crs(3857)
oa_actifs = oa_m[~oa_m.type_ourairports.isin(["closed", "heliport"])]
nearest = gpd.sjoin_nearest(oa_actifs, osm_ad[["source_id", "icao", "geometry"]], how="left",
                            distance_col="dist_m", rsuffix="osm")
nearest = nearest[~nearest.index.duplicated()]
dist_corr = nearest.dist_m / np.cos(np.radians(6))  # correction grossière d'échelle Mercator (~lat 6°)
code_oa = nearest.icao_code.fillna(nearest.gps_code).fillna(nearest.ident)
icao_match = (code_oa == nearest.icao).sum()
match_5km = int((dist_corr <= 5000).sum())
oa_g["osm_correspondant"] = None
oa_g.loc[nearest.index[dist_corr <= 5000], "osm_correspondant"] = nearest.loc[dist_corr <= 5000, "source_id_osm"]
croisement = {
    "ourairports_total_CM": int(len(oa_g)),
    "ourairports_par_type": oa_g.type_ourairports.value_counts().to_dict(),
    "ourairports_actifs_hors_heliports": int(len(oa_actifs)),
    "osm_aerodromes": int(len(osm_ad)),
    "ourairports_actifs_avec_osm_a_moins_de_5km": match_5km,
    "codes_icao_concordants": int(icao_match),
    "osm_sans_ourairports_a_moins_de_5km": int((gpd.sjoin_nearest(osm_ad, oa_m[["geometry"]], distance_col="d")
                                                .groupby(level=0).d.min() / np.cos(np.radians(6)) > 5000).sum()),
}
SYN["aeroports_ourairports"] = oa_g
write(finalize(oa_g, "INF.AEROPORT", OA_CODE), "aeroports_ourairports",
      {"source_code": OA_CODE, "producteur": "OurAirports (David Megginson et contributeurs)",
       "url": "https://davidmegginson.github.io/ourairports-data/airports.csv",
       "licence": "Domaine public (Public Domain Dedication, voir ourairports.com/data)",
       "attribution": "OurAirports (ourairports.com)", "date_situation": None, "sha256_source": SHA["oa"]},
      "airports.csv filtré sur iso_country=CM ; type_ourairports conservé (y compris closed et heliport) ; "
      "osm_correspondant = aérodrome OSM le plus proche à moins de 5 km (hors closed/heliport).",
      "Base collaborative : statut d'exploitation et types (small/medium/large) non officiels ; "
      "aucune date de situation par enregistrement ; vérifier auprès de l'ANAC/CCAA.", croisement)
CONTROLES["croisement_aeroports"] = croisement

# ---------- 5. World Port Index ----------
wpi_ok = (RAW / "wpi.csv").exists()
if wpi_ok:
    w = pd.read_csv(RAW / "wpi.csv", encoding="utf-8-sig")
    w = w[w["Country Code"] == "Cameroon"].copy()
    terminal = w["Main Port Name"].str.contains("Terminal", case=False)
    n_term = int(terminal.sum())
    w = w[~terminal]
    wg = gpd.GeoDataFrame({
        "nom": w["Main Port Name"].values,
        "source_id": ("wpi/" + w["World Port Index Number"].astype(int).astype(str)).values,
        "un_locode": w["UN/LOCODE"].values, "harbor_size": w["Harbor Size"].values,
        "harbor_type": w["Harbor Type"].values, "date_source": None},
        geometry=gpd.points_from_xy(w.Longitude, w.Latitude), crs=4326)
    # croisement : port OSM le plus proche
    near = gpd.sjoin_nearest(wg.to_crs(3857), SYN["ports_osm"].to_crs(3857)[["source_id", "geometry"]],
                             distance_col="d", rsuffix="osm")
    wg["distance_port_osm_km"] = (near.groupby(level=0).d.min() / np.cos(np.radians(4)) / 1000).round(1).values
    WPI_CODE = f"NGA_WPI_{TODAY}"
    write(finalize(wg, "INF.PORT", WPI_CODE), "ports_wpi",
          {"source_code": WPI_CODE, "producteur": "NGA (National Geospatial-Intelligence Agency), World Port Index Pub. 150",
           "url": "https://msi.nga.mil/api/publications/download?type=view&key=16920959/SFH00000/UpdatedPub150.csv",
           "licence": "Domaine public (œuvre du gouvernement fédéral des États-Unis)",
           "attribution": "NGA World Port Index (Pub. 150)", "date_situation": None, "sha256_source": SHA["wpi"]},
          "UpdatedPub150.csv filtré sur Country Code=Cameroon ; terminaux pétroliers exclus.",
          f"{n_term} terminaux pétroliers/marins ('Terminal') exclus de la couche : ils relèvent de "
          "ECO.HYDROCARBURES (sensibilité S1_RESTREINT). Coordonnées WPI approximatives (position de référence du port).",
          {"terminaux_exclus_S1": n_term})

# ---------- 6. Gridfinder (estimation) ----------
grid = gpd.read_file(RAW / "grid.gpkg", bbox=BBOX)
grid["geometry"] = grid.geometry.intersection(pays)
grid = grid[~grid.geometry.is_empty & grid.geom_type.isin(["LineString", "MultiLineString"])]
grid_km_total = sum(geod_len(g) for g in grid.geometry) / 1000
CONTROLES["gridfinder_estime"] = {"nb_troncons_decoupes": int(len(grid)),
                                  "longueur_totale_km_dans_cameroun": round(grid_km_total, 1)}

# ---------- 7. synthèse par arrondissement ----------
syn = adm3[["shapeID", "shapeName"]].copy().set_index("shapeID")

def km_par_adm(lines, col):
    inter = gpd.overlay(lines[["geometry"]].reset_index(drop=True), adm3[["shapeID", "geometry"]],
                        how="intersection", keep_geom_type=True)
    inter["km"] = inter.geometry.apply(geod_len) / 1000
    syn[col] = inter.groupby("shapeID").km.sum().reindex(syn.index).fillna(0).round(2)

for cl in ["motorway", "trunk", "primary", "secondary", "tertiary"]:
    km_par_adm(SYN_ROUTES[SYN_ROUTES.classe == cl], f"km_route_{cl}")
km_par_adm(SYN_RAIL, "km_voie_ferree_osm")
km_par_adm(SYN_LIGNES, "km_ligne_electrique_osm")
km_par_adm(grid, "km_reseau_mt_gridfinder_estime")

def nb_par_adm(pts, col):
    j = gpd.sjoin(pts[["geometry"]], adm3[["shapeID", "geometry"]], predicate="within")
    syn[col] = j.groupby("shapeID").size().reindex(syn.index).fillna(0).astype(int)
    return int(len(pts) - len(j))

hors_adm = {}
for name, col in [("gares", "nb_gares"), ("ports_osm", "nb_ports_osm"), ("aerodromes_osm", "nb_aerodromes_osm"),
                  ("aeroports_ourairports", "nb_aeroports_ourairports"),
                  ("centrales_electriques", "nb_centrales_electriques"), ("barrages", "nb_barrages"),
                  ("points_eau", "nb_points_eau"), ("antennes_telecom", "nb_antennes_telecom")]:
    hors_adm[col] = nb_par_adm(SYN[name], col)
hors_adm["nb_postes_electriques"] = nb_par_adm(SYN_POSTES, "nb_postes_electriques")
syn = syn.reset_index().rename(columns={"shapeID": "adm3_id_geoboundaries", "shapeName": "arrondissement"})
syn.to_csv(OUT / "synthese_par_arrondissement.csv", index=False, encoding="utf-8")
CONTROLES["synthese_par_arrondissement"] = {
    "nb_arrondissements": int(len(syn)),
    "points_hors_polygones_adm3_non_comptes": hors_adm,
    "totaux_km": {c: round(float(syn[c].sum()), 1) for c in syn.columns if c.startswith("km_")},
    "totaux_nb": {c: int(syn[c].sum()) for c in syn.columns if c.startswith("nb_")}}
MANIFEST.append({
    "fichier": "infrastructures/synthese_par_arrondissement.csv",
    "source_code": f"{OSM_CODE} ; {OA_CODE} ; GRIDFINDER_ZENODO_3628142 ; GEOBOUNDARIES_CMR_ADM3_9469f09",
    "producteur": "Calcul TasetyGrid à partir des couches ci-dessus, de Gridfinder et de geoBoundaries",
    "url": "voir les autres entrées du manifest",
    "licence": "ODbL 1.0 (base de données dérivée d'OSM et de geoBoundaries CMR ADM3, elle-même sous ODbL) ; "
               "colonne Gridfinder : CC BY 4.0",
    "attribution": "© les contributeurs d'OpenStreetMap ; OurAirports ; Arderne et al. 2020 (Gridfinder, CC BY 4.0) ; "
                   "geoBoundaries (Runfola et al. 2020) — CMR ADM3 issu d'OSM/Wambacher",
    "date_telechargement": TODAY, "date_situation": OSM_DATE, "sha256_source": None,
    "sha256_fichier": sha256(OUT / "synthese_par_arrondissement.csv"), "nb_entites": int(len(syn)),
    "methode": "Lignes : intersection géométrique avec les polygones ADM3 et longueur géodésique WGS84 (géométries "
               "NON simplifiées). Points : jointure spatiale 'within'. nb_postes_electriques compté à partir de "
               "power=substation (couche ponctuelle non publiée, S1).",
    "limites": "Limites geoBoundaries CMR ADM3 (année représentée 2017, source OSM/Wambacher) : noms et contours "
               "non officiels, peuvent différer du découpage légal (360 arrondissements) ; points situés hors des "
               "polygones (côte, frontière) non comptés (voir controles.json) ; les km par arrondissement sont découpés au contour ADM3 exact, d'où des totaux légèrement inférieurs à ceux des couches publiées (découpées avec un tampon ~1 km). km_reseau_mt_gridfinder_estime est "
               "une ESTIMATION PAR MODÈLE (Gridfinder 2020, lumières nocturnes + OSM), pas un réseau observé. "
               "Toutes les colonnes héritent de la complétude inégale d'OSM.",
    "controle": json.dumps(CONTROLES["synthese_par_arrondissement"], ensure_ascii=False)})

# ---------- 8. sources documentées sans fichier publié ----------
MANIFEST += [
    {"fichier": None, "source_code": "GRIDFINDER_ZENODO_3628142",
     "producteur": "Arderne C., Zorn C., Nicolas C., Koks E.E. (2020), Predictive mapping of the global power system "
                   "using open data, Scientific Data 7:19 ; données Zenodo record 3628142",
     "url": "https://zenodo.org/records/3628142 (grid.gpkg)", "licence": "CC BY 4.0",
     "attribution": "Arderne et al. 2020, Gridfinder (CC BY 4.0)", "date_telechargement": TODAY,
     "date_situation": "2020-01-16 (publication)", "sha256_source": SHA.get("grid"), "sha256_fichier": None,
     "nb_entites": int(len(grid)),
     "methode": "grid.gpkg (mondial, md5 Zenodo vérifié e5d0e9bd8ce4de851e65c6adae1af386) lu sur l'emprise "
                "Cameroun, découpé au contour geoBoundaries, agrégé en km par arrondissement dans "
                "synthese_par_arrondissement.csv (colonne km_reseau_mt_gridfinder_estime). Aucune géométrie publiée.",
     "limites": "ESTIMATION PAR MODÈLE du réseau moyenne tension (et transport) à partir de lumières nocturnes "
                "VIIRS et d'OSM ; précision ~ 75 % selon les auteurs sur des pays de validation ; situation "
                "antérieure à 2020 ; ne doit pas être présenté comme un réseau observé.",
     "controle": json.dumps(CONTROLES["gridfinder_estime"], ensure_ascii=False)},
    {"fichier": None, "source_code": "GEOBOUNDARIES_CMR_ADM3_9469f09",
     "producteur": "geoBoundaries (William & Mary geoLab), gbOpen CMR ADM3, boundaryID CMR-ADM3-9386221",
     "url": "https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/gbOpen/CMR/ADM3/geoBoundaries-CMR-ADM3.geojson",
     "licence": "ODbL 1.0 (licence déclarée par l'API geoBoundaries pour CMR ADM3 ; et non CC BY 4.0)",
     "attribution": "geoBoundaries ; source OpenStreetMap/Wambacher", "date_telechargement": TODAY,
     "date_situation": "2017 (année représentée) ; source mise à jour 2023-01-19 ; build 2023-12-12",
     "sha256_source": SHA["adm3"], "sha256_fichier": None, "nb_entites": int(len(adm3)),
     "methode": "Téléchargé pour la jointure uniquement, non commité. sha256 identique à l'oid Git LFS du commit 9469f09.",
     "limites": "Limites non officielles ; 360 unités (cohérent avec les 360 arrondissements).",
     "controle": json.dumps({"nb_unites": int(len(adm3)), "shapeID_uniques": bool(adm3.shapeID.is_unique)})},
    {"fichier": None, "source_code": "POSTES_ELECTRIQUES_OSM_NON_PUBLIES", **OSM_META, "source_code_osm": OSM_CODE,
     "date_telechargement": TODAY, "sha256_fichier": None, "nb_entites": int(len(postes)),
     "methode": "power=substation extrait (02_extraire_osm.py) mais NON publié en couche ponctuelle : le code "
                "INF.ENERGIE.POSTE porte la sensibilité S1_RESTREINT dans nomenclatures/objets.yaml (accès restreint, "
                "non public selon docs/05). Seul le compte par arrondissement est publié.",
     "limites": "Décision de prudence à confirmer par la gouvernance du projet (la donnée est publique dans OSM).",
     "controle": json.dumps(CONTROLES["postes_electriques_non_publies"], ensure_ascii=False)},
    {"fichier": None, "source_code": "TELECOM_SOURCES_NON_RETENUES",
     "producteur": "OpenCelliD (Unwired Labs), données d'opérateurs, ANTIC/ART",
     "url": None, "licence": "OpenCelliD : CC BY-SA 4.0 (compatible en principe mais clé API requise, non testée) ; "
                             "données opérateurs/ART : non ouvertes",
     "attribution": None, "date_telechargement": None, "sha256_fichier": None, "nb_entites": 0,
     "methode": "Non collecté. Seule la couche OSM (antennes_telecom.geojson) est publiée.",
     "limites": "Couverture télécom réelle non représentée ; fibre optique (INF.TELECOM.FIBRE) non collectée faute de "
                "source ouverte identifiée."},
]
for name in ["Geofabrik"]:
    MANIFEST.append({"fichier": None, "source_code": "OSM_GEOFABRIK_INACCESSIBLE",
                     "url": "https://download.geofabrik.de/africa/cameroon-latest.osm.pbf",
                     "methode": "Inaccessible depuis l'environnement de collecte (connexion réinitialisée, 2026-10-04) ; "
                                "remplacé par le miroir download.openstreetmap.fr (mêmes données OSM, ODbL).",
                     "limites": "L'extrait openstreetmap.fr est découpé avec une marge au-delà des frontières : "
                                "objets hors Cameroun retirés par découpage au contour geoBoundaries + ~1 km."})

(OUT / "manifest.json").write_text(json.dumps(MANIFEST, ensure_ascii=False, indent=2) + "\n")
(OUT / "controles.json").write_text(json.dumps(CONTROLES, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(CONTROLES, ensure_ascii=False, indent=1))
