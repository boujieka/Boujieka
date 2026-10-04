"""Construit les données SIG par pays de TasetyGrid à partir de Natural Earth.

Sorties (site/static/data/) :
- index.json : liste triée des pays (iso3, noms EN/FR, continent, population, bbox) ;
- <iso3>.json : frontière, premier niveau administratif, aéroports, ports,
  chemins de fer, routes, villes, lacs et comptes (longueurs géodésiques en km) ;
- SOURCES.md : sources, licence, date de génération et limites.

Les données sont réelles (Natural Earth 1:10m, domaine public) : rien n'est
inventé ; une couche absente reste vide. Les entités sont rattachées au pays
par intersection spatiale avec la frontière (marge d'environ 0,1 degré pour
les points côtiers). Les téléchargements sont mis en cache hors du dépôt.

Dépendances : pip install shapely pyshp pyproj
Usage : python3 site/gis_build.py [--cache DOSSIER] [ISO3 ...]
"""
import argparse
import datetime
import io
import json
import math
import os
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

import shapefile
import shapely
from pyproj import Geod
from shapely.geometry import shape, mapping, Point, box
from shapely.strtree import STRtree

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "static" / "data"
BASE = "https://naciscdn.org/naturalearth/10m/"
COUCHES = {
    "countries": "cultural/ne_10m_admin_0_countries",
    "admin1": "cultural/ne_10m_admin_1_states_provinces",
    "airports": "cultural/ne_10m_airports",
    "ports": "cultural/ne_10m_ports",
    "rail": "cultural/ne_10m_railroads",
    "roads": "cultural/ne_10m_roads",
    "places": "cultural/ne_10m_populated_places_simple",
    "lakes": "physical/ne_10m_lakes",
}
GEOD = Geod(ellps="WGS84")
MARGE = 0.1  # degrés, rattachement des points côtiers


def telecharger(cache):
    cache.mkdir(parents=True, exist_ok=True)
    chemins = {}
    for cle, rel in COUCHES.items():
        nom = rel.split("/")[1]
        d = cache / nom
        if not list(d.glob("*.shp")):
            print("téléchargement", nom, flush=True)
            data = urllib.request.urlopen(BASE + rel + ".zip", timeout=300).read()
            zipfile.ZipFile(io.BytesIO(data)).extractall(d)
        chemins[cle] = d
    return chemins


def lire(d):
    r = shapefile.Reader(str(next(d.glob("*.shp"))), encoding="utf-8")
    noms = [f[0] for f in r.fields[1:]]
    for sr in r.iterShapeRecords():
        if sr.shape.shapeType == 0:
            continue
        try:
            g = shape(sr.shape.__geo_interface__)
        except Exception:
            continue
        if g.is_empty:
            continue
        if not g.is_valid:
            g = shapely.make_valid(g)
        yield dict(zip(noms, sr.record)), g


def arr(v, n=3):
    return [round(x, n) for x in v]


def coords(g):
    """Géométrie shapely -> GeoJSON arrondi à 3 décimales."""
    m = mapping(g)

    def r(c):
        if isinstance(c[0], (int, float)):
            return [round(c[0], 3), round(c[1], 3)]
        return [r(x) for x in c]
    return {"type": m["type"], "coordinates": r(m["coordinates"])}


def poly_only(g):
    if g.geom_type in ("Polygon", "MultiPolygon"):
        return g
    if g.geom_type == "GeometryCollection":
        ps = [x for x in g.geoms if x.geom_type in ("Polygon", "MultiPolygon")]
        if ps:
            return shapely.union_all(ps)
    return None


def lignes(g):
    if g.geom_type == "LineString":
        return [g]
    if g.geom_type in ("MultiLineString", "GeometryCollection"):
        return [x for p in g.geoms for x in lignes(p)]
    return []


def km(l):
    return GEOD.geometry_length(l) / 1000.0


def lc(l):
    return [[round(x, 3), round(y, 3)] for x, y in l.coords]


def chaine(o):
    return "" if o is None else str(o).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=os.path.join(tempfile.gettempdir(), "tasety_ne"))
    ap.add_argument("only", nargs="*")
    a = ap.parse_args()
    ch = telecharger(Path(a.cache))
    OUT.mkdir(parents=True, exist_ok=True)

    # Pays
    pays = []
    for rec, g in lire(ch["countries"]):
        iso = rec["ADM0_A3"]
        if not iso or iso == "-99":
            continue
        pays.append((iso, rec, g))
    isos = [p[0] for p in pays]
    pgeoms = [p[2] for p in pays]
    ptree = STRtree(pgeoms)

    def attribuer(pt):
        """Indice du pays contenant le point, sinon le plus proche dans la marge."""
        for i in ptree.query(pt, predicate="intersects"):
            return int(i)
        i = ptree.nearest(pt)
        if i is not None and pgeoms[int(i)].distance(pt) <= MARGE:
            return int(i)
        return None

    par = {i: {"airports": [], "ports": [], "cities": [], "admin1": [], "lakes": []} for i in isos}

    for rec, g in lire(ch["airports"]):
        i = attribuer(g)
        if i is not None:
            par[isos[i]]["airports"].append([round(g.x, 3), round(g.y, 3), chaine(rec["name"]), chaine(rec["type"])])
    for rec, g in lire(ch["ports"]):
        i = attribuer(g)
        if i is not None:
            par[isos[i]]["ports"].append([round(g.x, 3), round(g.y, 3), chaine(rec["name"])])
    for rec, g in lire(ch["places"]):
        i = attribuer(g)
        if i is not None:
            par[isos[i]]["cities"].append([round(g.x, 3), round(g.y, 3), chaine(rec["name"]),
                                            int(rec["pop_max"] or 0), bool(rec["adm0cap"] == 1)])
    for rec, g in lire(ch["admin1"]):
        iso = rec["adm0_a3"]
        if iso in par and chaine(rec["name"]):
            par[iso]["admin1"].append((chaine(rec["name"]), g))
    lacs = list(lire(ch["lakes"]))
    lgeoms = [g for _, g in lacs]
    ltree = STRtree(lgeoms)
    rails = list(lire(ch["rail"]))
    rtree = STRtree([g for _, g in rails])
    roads = list(lire(ch["roads"]))
    dtree = STRtree([g for _, g in roads])

    index = []
    total = 0
    for iso, rec, g in sorted(pays, key=lambda p: p[0]):
        if a.only and iso not in a.only:
            continue
        d = par[iso]
        w, s, e, n = g.bounds
        bbox = [round(w, 3), round(s, 3), round(e, 3), round(n, 3)]
        # Cadrage initial : les territoires éloignés (outre-mer, îles lointaines) ne doivent pas écraser le pays.
        parts = list(g.geoms) if hasattr(g, "geoms") else [g]
        poids = [q.area * math.cos(math.radians(q.centroid.y)) for q in parts]
        gros = [q for q, a_ in zip(parts, poids) if a_ >= 0.25 * max(poids)]
        vw, vs, ve, vn = (min(q.bounds[0] for q in gros), min(q.bounds[1] for q in gros),
                          max(q.bounds[2] for q in gros), max(q.bounds[3] for q in gros))
        if ve >= 179.9 and vw > -150:  # pays à cheval sur l'antiméridien : la partie est repasse en longitudes négatives
            est = [q for q in parts if q.bounds[2] < -150 and q.bounds[1] <= vn and q.bounds[3] >= vs]
            if est:
                ve = max(q.bounds[2] for q in est) + 360
        view = [round(vw, 3), round(vs, 3), round(ve, 3), round(vn, 3)]
        span = max(e - w, n - s)
        grand = span > 12
        budget = 600_000 if grand else 150_000
        tol = min(max(span * 0.0012, 0.0005), 0.02)
        zone = g.buffer(0.01).simplify(min(tol, 0.005))


        # Lignes (découpées à la zone du pays) et longueurs géodésiques
        rail_l, rail_km = [], 0.0
        for k in rtree.query(zone, predicate="intersects"):
            for l in lignes(rails[int(k)][1].intersection(zone)):
                rail_km += km(l)
                rail_l.append(l)
        road_l, road_km = [], 0.0
        for k in dtree.query(zone, predicate="intersects"):
            r, geo = roads[int(k)]
            for l in lignes(geo.intersection(zone)):
                road_km += km(l)
                road_l.append((l, chaine(r["type"]), int(r["scalerank"] or 9)))
        # Lacs
        lak = []
        for k in ltree.query(zone, predicate="intersects"):
            c = poly_only(lgeoms[int(k)].intersection(zone))
            if c is not None and not c.is_empty:
                lak.append(c)

        villes = sorted(d["cities"], key=lambda c: (-int(c[4]), -c[3]))
        adm1 = d["admin1"]
        facteur = 1.0
        for essai in range(12):
            t = tol * facteur
            border = poly_only(g.simplify(t, preserve_topology=True))
            a1 = []
            for nom, ag in adm1:
                sg = poly_only(ag.simplify(t * 2, preserve_topology=True))
                if sg is not None and not sg.is_empty:
                    a1.append({"name": nom, "geometry": coords(sg)})
            rl = []
            for l in rail_l:
                sl = l.simplify(t * 2)
                if sl.length > t * 3 and sl.geom_type == "LineString":
                    rl.append(lc(sl))
            rd = []
            for l, k, sr in road_l:
                sl = l.simplify(t * 2)
                if sl.length > t * 3 and sl.geom_type == "LineString":
                    rd.append({"c": lc(sl), "k": k})
            lk = []
            for c in lak:
                sc = poly_only(c.simplify(t * 2))
                if sc is not None and not sc.is_empty and sc.area > t * t * 20:
                    lk.append(coords(sc))
            nv = max(25, int(len(villes) / (1 + essai * 0.6))) if essai else len(villes)
            doc = {
                "iso3": iso, "name_en": chaine(rec["NAME_EN"]) or chaine(rec["NAME"]),
                "name_fr": chaine(rec["NAME_FR"]), "pop_est": int(rec["POP_EST"] or 0), "bbox": bbox, "view": view,
                "border": coords(border), "admin1": a1,
                "layers": {"airports": d["airports"], "ports": d["ports"], "railways": rl, "roads": rd,
                           "cities": villes[:nv], "lakes": lk},
                "counts": {"airports": len(d["airports"]), "ports": len(d["ports"]),
                           "railways_km": round(rail_km), "roads_km": round(road_km),
                           "cities": len(d["cities"])},
            }
            txt = json.dumps(doc, ensure_ascii=False, separators=(",", ":"))
            if len(txt.encode()) <= budget:
                break
            facteur *= 1.8
        (OUT / (iso + ".json")).write_text(txt, encoding="utf-8")
        total += len(txt.encode())
        index.append({"iso3": iso, "name_en": doc["name_en"], "name_fr": doc["name_fr"],
                      "continent": chaine(rec["CONTINENT"]), "pop_est": doc["pop_est"],
                      "bbox": bbox, "files": iso + ".json"})
    if not a.only:
        index.sort(key=lambda x: x["name_en"])
        (OUT / "index.json").write_text(json.dumps(index, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        ver = chaine(next(iter(ch["countries"].glob("*.VERSION.txt")), None) and
                     next(iter(ch["countries"].glob("*.VERSION.txt"))).read_text())
        (OUT / "SOURCES.md").write_text(f"""# Sources des données SIG

- Source : Natural Earth, jeux vectoriels 1:10m (https://www.naturalearthdata.com/).
- Téléchargement : {BASE} (cultural : admin_0_countries, admin_1_states_provinces, airports, ports, railroads, roads, populated_places_simple ; physical : lakes).
- Licence : domaine public (https://www.naturalearthdata.com/about/terms-of-use/). Attribution non requise, citée par courtoisie.
- Version des fichiers (admin_0_countries) : {ver}
- Généré le : {datetime.date.today().isoformat()} par site/gis_build.py.
- Traitement : rattachement par intersection spatiale avec la frontière (marge 0,1 degré pour les points), lignes découpées à la frontière, longueurs géodésiques WGS84, coordonnées arrondies à 3 décimales, géométries simplifiées.

## Limites

- Échelle 1:10m : généralisation forte, les tracés ne conviennent pas à la mesure précise ni à la navigation.
- Couverture inégale selon les pays et les couches (routes et chemins de fer = réseaux principaux seulement ; certains pays n'ont aucune entité sur une couche).
- Aucune garantie de données récentes : Natural Earth est mis à jour de façon irrégulière.
- Les longueurs sont celles des tracés généralisés, pas des réseaux réels.
- Les frontières suivent les choix cartographiques de Natural Earth (de facto), sans portée juridique.
- Pour les grands pays, des villes peu peuplées peuvent être omises pour respecter le budget de taille ; le compteur "cities" indique le nombre total.
""", encoding="utf-8")
    print("pays:", len(index), "octets:", total)


if __name__ == "__main__":
    main()
