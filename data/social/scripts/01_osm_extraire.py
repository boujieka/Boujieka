"""Extraction des infrastructures sociales depuis l'extrait OSM du Cameroun.

Entrée  : $RAW/cameroon.osm.pbf (miroir openstreetmap.fr, ODbL)
Sortie  : $TMP/osm_brut.parquet (un point par objet ; centroïde pour les surfaces)

Objets retenus :
  santé     : amenity in {hospital, clinic, doctors, pharmacy, dentist} ou healthcare=*
  éducation : amenity in {school, college, university, kindergarten}
  services  : amenity in {townhall, marketplace}
Champs exclus volontairement (données personnelles) : user, uid, phone, contact:*,
email, addr:*, operator (peut contenir un nom de personne), website.
"""
import osmium
import pandas as pd
from shapely import wkb

from commun import RAW, TMP

AMENITY = {"hospital", "clinic", "doctors", "pharmacy", "dentist",
           "school", "college", "university", "kindergarten",
           "townhall", "marketplace"}
GARDER = ["name", "name:fr", "name:en", "amenity", "healthcare", "healthcare:speciality",
          "isced:level", "school", "operator:type", "operator_type", "religion",
          "townhall:type", "admin_level", "beds", "emergency", "opening_hours",
          "source", "check_date"]

wkbf = osmium.geom.WKBFactory()


def retenir(tags):
    a = tags.get("amenity")
    return a in AMENITY or "healthcare" in tags


lignes = []
ignores = {"way_non_ferme": 0, "geom_erreur": 0}

fp = (osmium.FileProcessor(str(RAW / "cameroon.osm.pbf"))
      .with_locations()
      .with_areas(osmium.filter.KeyFilter("amenity", "healthcare"))
      .with_filter(osmium.filter.KeyFilter("amenity", "healthcare")))

for o in fp:
    tags = dict(o.tags)
    if not retenir(tags):
        continue
    if o.is_node():
        otype, oid = "node", o.id
        try:
            geom = wkb.loads(wkbf.create_point(o), hex=True)
        except Exception:
            ignores["geom_erreur"] += 1
            continue
    elif o.is_area():
        otype = "way" if o.from_way() else "relation"
        oid = o.orig_id()
        try:
            geom = wkb.loads(wkbf.create_multipolygon(o), hex=True).centroid
        except Exception:
            ignores["geom_erreur"] += 1
            continue
    elif o.is_way():
        # Les ways fermés sont traités comme surfaces ; ici seulement les ways ouverts.
        if o.is_closed():
            continue
        ignores["way_non_ferme"] += 1
        continue
    else:
        continue  # relations brutes : traitées via les surfaces
    rec = {"source_id": f"{otype}/{oid}", "osm_type": otype,
           "date_maj_objet": o.timestamp.strftime("%Y-%m-%d"),
           "lon": geom.x, "lat": geom.y}
    for k in GARDER:
        rec[k] = tags.get(k)
    lignes.append(rec)

df = pd.DataFrame(lignes)
# Un même way fermé peut sortir à la fois comme way et comme surface : on dédoublonne par id.
avant = len(df)
df = df.drop_duplicates("source_id")
TMP.mkdir(parents=True, exist_ok=True)
df.to_parquet(TMP / "osm_brut.parquet", index=False)
print(f"objets retenus : {len(df)} (doublons d'id retirés : {avant - len(df)})")
print("ignorés :", ignores)
print(df["amenity"].value_counts(dropna=False).to_string())
print(df["healthcare"].value_counts(dropna=False).head(20).to_string())
