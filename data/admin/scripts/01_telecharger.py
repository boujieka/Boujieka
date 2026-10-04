#!/usr/bin/env python3
"""Télécharge les sources brutes (non commitées) dans data/admin/.cache/ et note leur sha256.

Sources :
  - OCHA COD-AB Cameroun (HDX, dataset cod-ab-cmr), CC BY-IGO  -> référence des limites
  - geoBoundaries gbOpen CMR ADM0-3 (API current)               -> comparaison
  - Geofabrik africa/cameroon-latest.osm.pbf, ODbL 1.0           -> localités OSM
"""
import datetime, hashlib, json, pathlib, urllib.request

ICI = pathlib.Path(__file__).resolve().parent.parent
CACHE = ICI / ".cache"
CACHE.mkdir(exist_ok=True)


def get(url, dest):
    dest = CACHE / dest
    if not dest.exists():
        print("GET", url)
        req = urllib.request.Request(url, headers={"User-Agent": "TasetyGrid-collecte/1.0"})
        with urllib.request.urlopen(req, timeout=600) as r, open(dest.with_suffix(".part"), "wb") as f:
            while chunk := r.read(1 << 20):
                f.write(chunk)
        dest.with_suffix(".part").rename(dest)
    return dest


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while b := f.read(1 << 20):
            h.update(b)
    return h.hexdigest()


journal = {"date_telechargement": datetime.date.today().isoformat(), "fichiers": {}}

# OCHA COD-AB (HDX CKAN API)
meta = json.load(open(get("https://data.humdata.org/api/3/action/package_show?id=cod-ab-cmr", "hdx_cod-ab-cmr.json")))["result"]
for r in meta["resources"]:
    if r["name"] == "cmr_admin_boundaries.geojson.zip":
        p = get(r["url"], r["name"])
        journal["fichiers"]["ocha"] = {"url": r["url"], "last_modified": r["last_modified"], "sha256": sha256(p),
                                        "licence": meta["license_title"], "dataset_date": meta.get("dataset_date")}

# geoBoundaries
for lvl in ["ADM0", "ADM1", "ADM2", "ADM3"]:
    m = json.load(open(get(f"https://www.geoboundaries.org/api/current/gbOpen/CMR/{lvl}/", f"gb_{lvl}_meta.json")))
    # github.com/.../raw/ renvoie 403 via le proxy de l'environnement de collecte :
    # on lit le même fichier (même commit) sur media.githubusercontent.com (stockage Git LFS).
    url = m["gjDownloadURL"].replace("https://github.com/wmgeolab/geoBoundaries/raw/",
                                     "https://media.githubusercontent.com/media/wmgeolab/geoBoundaries/")
    p = get(url, f"geoBoundaries-CMR-{lvl}.geojson")
    journal["fichiers"][f"gb_{lvl}"] = {"url": url, "url_api": m["gjDownloadURL"], "sha256": sha256(p), "licence": m["boundaryLicense"],
                                        "source": m["boundarySource"], "annee": m["boundaryYearRepresented"],
                                        "nb": m["admUnitCount"], "buildDate": m["buildDate"]}

# OSM : Geofabrik (download.geofabrik.de) et overpass-api.de étaient injoignables depuis
# l'environnement de collecte du 2026-10-04 (tunnel fermé). On utilise l'extrait équivalent
# publié par OpenStreetMap France (mêmes données OSM, ODbL 1.0). Ordre d'essai ci-dessous.
OSM = [("https://download.geofabrik.de/africa/cameroon-latest.osm.pbf", None),
       ("https://download.openstreetmap.fr/extracts/africa/cameroon-latest.osm.pbf",
        "https://download.openstreetmap.fr/extracts/africa/cameroon.state.txt")]
for url, state in OSM:
    try:
        p = get(url, "cameroon-latest.osm.pbf")
    except Exception as e:  # source injoignable : on passe à la suivante
        print("ECHEC", url, e)
        continue
    journal["fichiers"]["osm"] = {"url": url, "sha256": sha256(p), "licence": "ODbL 1.0"}
    if state:
        journal["fichiers"]["osm"]["state"] = open(get(state, "cameroon.state.txt")).read()
    break

json.dump(journal, open(CACHE / "journal_telechargement.json", "w"), indent=2, ensure_ascii=False)
print(json.dumps(journal, indent=2, ensure_ascii=False))
