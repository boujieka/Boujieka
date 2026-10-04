#!/usr/bin/env python3
"""Extraction des infrastructures physiques du Cameroun depuis l'extrait OSM (.osm.pbf).

Usage : python3 02_extraire_osm.py RAW_DIR WORK_DIR
Produit dans WORK_DIR des GeoParquet NON simplifiés (étape intermédiaire, non commitée) :
  routes, voies_ferrees, ponts, lignes_electriques (lignes) ;
  gares, ports, aerodromes, centrales, postes, barrages, points_eau, antennes (points).
Seule une liste blanche de tags est conservée (aucun contact, téléphone, courriel, etc.).
"""
import sys
from pathlib import Path

import geopandas as gpd
import osmium
import shapely.wkb

RAW, WORK = Path(sys.argv[1]), Path(sys.argv[2])
WORK.mkdir(parents=True, exist_ok=True)
PBF = RAW / "cameroon-latest.osm.pbf"

ROAD_CLASSES = {"motorway", "trunk", "primary", "secondary", "tertiary"}
WKB = osmium.geom.WKBFactory()

def tags_of(o, keys):
    return {k.replace(":", "_"): o.tags.get(k) for k in keys}

def classify_point(t):
    """Retourne la liste des couches ponctuelles auxquelles appartient un objet (tags dict)."""
    out = []
    g = t.get
    if g("railway") in ("station", "halt") or (g("public_transport") == "station" and g("train") == "yes"):
        out.append("gares")
    if g("landuse") == "port" or g("industrial") == "port" or g("harbour") == "yes" \
            or g("seamark:type") == "harbour":
        out.append("ports")
    if g("aeroway") == "aerodrome":
        out.append("aerodromes")
    if g("power") == "plant":
        out.append("centrales")
    if g("power") == "substation":
        out.append("postes")
    if g("waterway") == "dam":
        out.append("barrages")
    if g("man_made") == "water_well" or g("amenity") == "drinking_water":
        out.append("points_eau")
    if (g("man_made") in ("mast", "tower")) and (
            g("tower:type") == "communication" or g("communication:mobile_phone") == "yes"):
        out.append("antennes")
    return out

KEEP = {
    "gares": ["railway", "public_transport", "operator", "uic_ref"],
    "ports": ["landuse", "industrial", "harbour", "seamark:type", "operator"],
    "aerodromes": ["aeroway", "aerodrome", "aerodrome:type", "icao", "iata", "ele", "operator"],
    "centrales": ["plant:source", "plant:method", "plant:output:electricity", "operator", "start_date"],
    "postes": ["substation", "voltage", "operator"],
    "barrages": ["waterway", "operator", "height", "start_date"],
    "points_eau": ["man_made", "amenity", "pump", "drinking_water", "operational_status", "operator",
                   "access", "seasonal"],
    "antennes": ["man_made", "tower:type", "communication:mobile_phone", "height", "operator"],
}

class H(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.rows = {k: [] for k in ["routes", "voies_ferrees", "ponts", "lignes_electriques",
                                     *KEEP.keys()]}

    def _point_rows(self, oid, t, geom_fn):
        layers = classify_point(t)
        if not layers:
            return
        try:
            geom = geom_fn()
        except Exception:
            return
        if geom is None or geom.is_empty:
            return
        pt = geom if geom.geom_type == "Point" else geom.representative_point()
        for L in layers:
            r = {"source_id": oid, "nom": t.get("name") or "", "geometrie_source": geom.geom_type}
            r.update({k.replace(":", "_"): t.get(k) for k in KEEP[L]})
            r["geometry"] = pt
            self.rows[L].append(r)

    def node(self, n):
        if not n.tags:
            return
        t = dict(n.tags)
        if classify_point(t):
            self._point_rows(f"node/{n.id}", t, lambda: shapely.wkb.loads(WKB.create_point(n), hex=True))

    def way(self, w):
        t = dict(w.tags)
        if not t:
            return
        oid = f"way/{w.id}"

        def line():
            return shapely.wkb.loads(WKB.create_linestring(w), hex=True)

        hw = t.get("highway", "")
        base = hw[:-5] if hw.endswith("_link") else hw
        if base in ROAD_CLASSES:
            try:
                g = line()
            except Exception:
                g = None
            if g is not None:
                self.rows["routes"].append({
                    "source_id": oid, "nom": t.get("name") or "", "classe": base,
                    "bretelle": hw.endswith("_link"), "ref": t.get("ref"), "surface": t.get("surface"),
                    "lanes": t.get("lanes"), "oneway": t.get("oneway"), "bridge": t.get("bridge"),
                    "geometry": g})
                if base in ("trunk", "primary") and t.get("bridge") not in (None, "no"):
                    self.rows["ponts"].append({
                        "source_id": oid, "nom": t.get("bridge:name") or t.get("name") or "",
                        "classe_route": base, "ref": t.get("ref"), "bridge": t.get("bridge"),
                        "bridge_structure": t.get("bridge:structure"), "geometry": g})
        if t.get("railway") == "rail":
            try:
                self.rows["voies_ferrees"].append({
                    "source_id": oid, "nom": t.get("name") or "", "usage": t.get("usage"),
                    "service": t.get("service"), "gauge": t.get("gauge"), "operator": t.get("operator"),
                    "electrified": t.get("electrified"), "geometry": line()})
            except Exception:
                pass
        if t.get("power") == "line":
            try:
                self.rows["lignes_electriques"].append({
                    "source_id": oid, "nom": t.get("name") or "", "voltage": t.get("voltage"),
                    "cables": t.get("cables"), "circuits": t.get("circuits"),
                    "operator": t.get("operator"), "geometry": line()})
            except Exception:
                pass
        # objets ponctuels portés par un chemin (fermé ou non) -> point représentatif
        if classify_point(t):
            def geom():
                g = line()
                if w.is_closed() and len(w.nodes) >= 4:
                    from shapely.geometry import Polygon
                    return Polygon(g.coords)
                return g
            self._point_rows(oid, t, geom)

    def area(self, a):
        # uniquement les multipolygones issus de relations (les chemins fermés sont traités dans way())
        if a.from_way():
            return
        t = dict(a.tags)
        if classify_point(t):
            self._point_rows(f"relation/{a.orig_id()}", t,
                             lambda: shapely.wkb.loads(WKB.create_multipolygon(a), hex=True))


h = H()
h.apply_file(str(PBF), locations=True, idx="flex_mem")

hdr = osmium.io.Reader(str(PBF), osmium.osm.osm_entity_bits.NOTHING).header()
ts = hdr.get("osmosis_replication_timestamp", "")
print("horodatage de l'extrait :", ts)
(WORK / "osm_timestamp.txt").write_text(ts)

for name, rows in h.rows.items():
    gdf = gpd.GeoDataFrame(rows, geometry="geometry", crs="EPSG:4326")
    gdf.to_parquet(WORK / f"{name}.parquet")
    print(f"{name}: {len(gdf)}")
