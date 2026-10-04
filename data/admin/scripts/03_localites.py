#!/usr/bin/env python3
"""Extrait les localités OSM (place=city/town/village/hamlet/suburb/neighbourhood) et les rattache aux ADM3 OCHA.

Entrée : .cache/cameroon-latest.osm.pbf, limites_adm3.geojson
Sortie : localites_osm.geojson, .cache/controles_localites.json
- Nœuds : position du nœud. Chemins/relations (surfaces) : point représentatif (point_on_surface).
- Seules les clés suivantes sont gardées (pas de données personnelles) :
  name, name:fr, name:en, place, population, population:date, source:population, wikidata.
- L'extrait OSM France déborde sur les pays voisins : on garde uniquement les localités situées dans la
  frontière OSM du Cameroun (relation/192830, admin_level=2, ISO3166-1=CM, lue dans le même extrait).
- Rattachement : jointure spatiale point-dans-polygone sur les ADM3 OCHA ; les localités dans la frontière OSM
  mais hors des polygones OCHA (écarts de tracé entre les deux sources, surtout côte et frontières) sont
  rattachées à l'ADM3 OCHA le plus proche si distance <= 5 km (champ rattachement), sinon laissées sans ADM.
"""
import json, pathlib
import geopandas as gpd, pandas as pd, shapely, osmium

ICI = pathlib.Path(__file__).resolve().parent.parent
C = ICI / ".cache"
PLACES = {"city", "town", "village", "hamlet", "suburb", "neighbourhood"}
CLES = {"name": "nom", "name:fr": "nom_fr", "name:en": "nom_en", "place": "place", "population": "population",
        "population:date": "population_date", "source:population": "population_source", "wikidata": "wikidata"}
LAEA = "+proj=laea +lat_0=7 +lon_0=12.5 +datum=WGS84 +units=m +no_defs"
BBOX = (8.4, 1.6, 16.2, 13.1)
etat = dict(l.split("=", 1) for l in open(C / "cameroon.state.txt").read().split())
DATE = etat["timestamp"].replace("\\", "")[:10]
SRC = f"OSM_OSMFR_{DATE}"

wkb = osmium.geom.WKBFactory()
rows = []
pays = []


class H(osmium.SimpleHandler):
    def _add(self, o, sid, geom):
        if o.tags.get("place") not in PLACES:
            return
        r = {v: o.tags.get(k) for k, v in CLES.items()}
        r["source_id"] = sid; r["geometry"] = geom
        rows.append(r)

    def node(self, n):
        if n.tags.get("place") in PLACES:
            self._add(n, f"node/{n.id}", shapely.Point(n.location.lon, n.location.lat))

    def area(self, a):
        if a.tags.get("boundary") == "administrative" and a.tags.get("admin_level") == "2" and a.tags.get("ISO3166-1") == "CM":
            pays.append(shapely.from_wkb(wkb.create_multipolygon(a)))
        if a.tags.get("place") in PLACES:
            sid = f"way/{a.orig_id()}" if a.from_way() else f"relation/{a.orig_id()}"
            try:
                g = shapely.from_wkb(wkb.create_multipolygon(a))
            except Exception:
                return
            self._add(a, sid, g.point_on_surface())


H().apply_file(str(C / "cameroon-latest.osm.pbf"), locations=True)
df = pd.DataFrame(rows)
g = gpd.GeoDataFrame(df, geometry="geometry", crs=4326)
g.insert(0, "tg_type", "POP.LOCALITE")
g["source"] = SRC; g["statut"] = "IMPORTE"; g["date_source"] = DATE
g["population"] = g.population  # valeur brute OSM (texte), non convertie
nb_brut = len(g)

# Emprise
b = g.geometry.bounds
dans = (b.minx >= BBOX[0]) & (b.maxx <= BBOX[2]) & (b.miny >= BBOX[1]) & (b.maxy <= BBOX[3])

# Frontière OSM du Cameroun
assert len(pays) == 1, "frontière OSM du Cameroun introuvable ou multiple"
dans_cm = g.within(pays[0])
exclues = g[~dans_cm]
g = g[dans_cm].copy()

# Rattachement ADM3
adm3 = gpd.read_file(ICI / "limites_adm3.geojson")[["code", "nom", "adm1_code", "adm1_nom", "adm2_code", "adm2_nom", "geometry"]]
adm3 = adm3.rename(columns={"code": "adm3_code", "nom": "adm3_nom"})
j = gpd.sjoin(g, adm3, how="left", predicate="within").drop(columns="index_right")
j = j[~j.index.duplicated(keep="first")]
hors = j.adm3_code.isna()
g_e = j[hors].to_crs(LAEA); a_e = adm3.to_crs(LAEA)
near = gpd.sjoin_nearest(g_e[["geometry"]], a_e, how="left", max_distance=5000, distance_col="dist_m")
near = near[~near.index.duplicated(keep="first")]
cols = ["adm3_code", "adm3_nom", "adm1_code", "adm1_nom", "adm2_code", "adm2_nom"]
j.loc[near.index, cols] = near[cols].values
j["rattachement"] = "dans_adm3"
j.loc[hors[hors].index, "rattachement"] = "adm3_le_plus_proche_<=5km"
j.loc[j.adm3_code.isna(), "rattachement"] = "non_rattachee_>5km"

# Doublons
j["_k"] = j.nom.fillna("").str.lower().str.strip()
xy = j.geometry.get_coordinates().round(6)
dup_id = int(j.source_id.duplicated().sum())
dup_xy = int(xy.duplicated(keep=False).sum())
je = j.to_crs(LAEA)
pairs = gpd.sjoin(je[["_k", "place", "geometry"]], je[["_k", "geometry"]].assign(geometry=je.buffer(500)), predicate="within")
pairs = pairs[(pairs.index < pairs.index_right) & (pairs._k_left == pairs._k_right) & (pairs._k_left != "")]
j["doublon_probable"] = j.index.isin(pairs.index) | j.index.isin(pairs.index_right)

ordre = ["tg_type", "nom", "nom_fr", "nom_en", "place", "population", "population_date", "population_source", "wikidata",
         "adm1_code", "adm1_nom", "adm2_code", "adm2_nom", "adm3_code", "adm3_nom", "rattachement", "doublon_probable",
         "source_id", "source", "statut", "date_source", "geometry"]
j = j[ordre].sort_values(["adm3_code", "place", "nom"], na_position="last").reset_index(drop=True)
f = ICI / "localites_osm.geojson"
f.unlink(missing_ok=True)
j.to_file(f, driver="GeoJSON", COORDINATE_PRECISION=6, RFC7946="YES")

ctrl = {
    "date_situation_osm": etat["timestamp"].replace("\\", ""), "nb_objets_place_extraits": nb_brut,
    "nb_hors_emprise_bbox": int((~dans).sum()), "nb_exclus_hors_frontiere_osm_cameroun": len(exclues),
    "exclus_par_place": exclues.place.value_counts().to_dict(),
    "nb_localites": len(j), "par_place": j.place.value_counts().to_dict(),
    "par_type_osm": j.source_id.str.split("/").str[0].value_counts().to_dict(),
    "par_rattachement": j.rattachement.value_counts().to_dict(),
    "distance_max_rattachement_proche_m": float(near.dist_m.max().round(1)) if len(near) else 0.0,
    "sans_nom": int(j.nom.isna().sum()), "avec_population": int(j.population.notna().sum()),
    "avec_population_et_date": int((j.population.notna() & j.population_date.notna()).sum()),
    "population_non_numerique": j.population[j.population.notna() & ~j.population.fillna("").str.fullmatch(r"\d+")].tolist(),
    "doublons_source_id": dup_id, "points_coordonnees_identiques": dup_xy,
    "paires_meme_nom_a_moins_de_500m": len(pairs), "localites_marquees_doublon_probable": int(j.doublon_probable.sum()),
    "adm3_sans_localite": sorted(set(adm3.adm3_code) - set(j.adm3_code)),
    "taille_mo": round(f.stat().st_size / 1e6, 2),
}
json.dump(ctrl, open(C / "controles_localites.json", "w"), indent=2, ensure_ascii=False, default=str)
print(json.dumps(ctrl, indent=2, ensure_ascii=False, default=str))
