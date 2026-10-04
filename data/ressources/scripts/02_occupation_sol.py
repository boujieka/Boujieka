"""Surfaces d'occupation du sol (ESA WorldCover 10 m 2021 v200) par arrondissement
(geoBoundaries CMR ADM3).

Méthode : pour chaque tuile WorldCover et par bandes de 600 lignes, les polygones des
arrondissements sont rasterisés sur la grille 10 m (pixel affecté à l'arrondissement qui
contient son centre) ; on compte les pixels par (arrondissement, classe) et on les convertit
en hectares avec l'aire géodésique d'un pixel au centre de la bande (ellipsoïde WGS84).
Les tuiles WorldCover sont jointives (3°x3°) : aucun pixel n'est compté deux fois.

Usage : RAW=/chemin/temp python3 data/ressources/scripts/02_occupation_sol.py
"""
import csv
import glob
import os
from concurrent.futures import ProcessPoolExecutor

import geopandas as gpd
import numpy as np
import rasterio
from pyproj import Geod
from rasterio import features
from rasterio.windows import Window, bounds as wbounds
from shapely.geometry import box

RAW = os.environ.get("RAW", "./raw_ressources")
OUT = os.path.join(os.path.dirname(__file__), "..")
BANDE = 600
GEOD = Geod(ellps="WGS84")
CLASSES = {  # code WorldCover -> colonne
    10: "foret_arboree_ha", 20: "arbustes_ha", 30: "prairie_savane_herbacee_ha",
    40: "cultures_ha", 50: "bati_ha", 60: "sol_nu_vegetation_clairsemee_ha",
    70: "neige_glace_ha", 80: "eau_permanente_ha", 90: "zone_humide_herbacee_ha",
    95: "mangroves_ha", 100: "mousses_lichens_ha",
}


def corrige_nom(n):
    """Répare le « mojibake » des noms geoBoundaries (UTF-8 lu en Latin-1)."""
    if n and ("Ã" in n or "Â" in n):
        try:
            return n.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            return n
    return n


def aire_pixel_ha(lat, res):
    lon0 = 0.0
    a, _ = GEOD.polygon_area_perimeter(
        [lon0, lon0 + res, lon0 + res, lon0], [lat - res / 2, lat - res / 2, lat + res / 2, lat + res / 2])
    return abs(a) / 1e4


def traite_tuile(args):
    f, geoms = args
    n = len(geoms) + 1
    acc = np.zeros((n, 256), dtype=np.float64)
    with rasterio.open(f) as r:
        tb = box(*r.bounds)
        sel = [(g, i) for g, i in geoms if g.intersects(tb)]
        if not sel:
            return acc
        res = r.res[0]
        for r0 in range(0, r.height, BANDE):
            h = min(BANDE, r.height - r0)
            win = Window(0, r0, r.width, h)
            wb = box(*wbounds(win, r.transform))
            gs = [(g, i) for g, i in sel if g.intersects(wb)]
            if not gs:
                continue
            ids = features.rasterize(gs, out_shape=(h, r.width), transform=r.window_transform(win),
                                     fill=0, dtype="int32")
            if not ids.any():
                continue
            cl = r.read(1, window=win)
            cnt = np.bincount((ids.astype(np.int64) * 256 + cl).ravel(), minlength=n * 256)
            lat_c = r.transform.f + r.transform.e * (r0 + h / 2)
            acc += cnt.reshape(n, 256) * aire_pixel_ha(lat_c, res)
    return acc


def main():
    adm3 = gpd.read_file(os.path.join(RAW, "gb_adm3.geojson")).reset_index(drop=True)
    adm3["uid"] = np.arange(1, len(adm3) + 1)
    geoms = list(zip(adm3.geometry, adm3.uid))
    tuiles = sorted(glob.glob(os.path.join(RAW, "wc", "ESA_WorldCover_10m_2021_v200_*_Map.tif")))
    total = np.zeros((len(adm3) + 1, 256))
    with ProcessPoolExecutor(max_workers=int(os.environ.get("NPROC", 4))) as ex:
        for f, acc in zip(tuiles, ex.map(traite_tuile, [(t, geoms) for t in tuiles])):
            print("tuile", os.path.basename(f), round(acc[1:].sum()), "ha")
            total += acc
    np.save(os.path.join(RAW, "wc_par_adm3.npy"), total)

    inattendues = sorted(set(np.nonzero(total[1:].sum(axis=0))[0]) - set(CLASSES) - {0})
    cols = ["arrondissement_id", "arrondissement_nom", "surface_classee_ha"] + list(CLASSES.values()) + [
        "non_classe_nodata_ha", "part_foret_arboree_pct", "part_cultures_pct", "part_bati_pct", "source"]
    rows = []
    for _, z in adm3.iterrows():
        v = total[z.uid]
        tot = v[list(CLASSES)].sum()
        row = {"arrondissement_id": z.shapeID, "arrondissement_nom": corrige_nom(z.shapeName),
               "surface_classee_ha": round(tot, 1)}
        for c, nom in CLASSES.items():
            row[nom] = round(v[c], 1)
        row["non_classe_nodata_ha"] = round(v[0], 1)
        row["part_foret_arboree_pct"] = round(100 * v[10] / tot, 2) if tot else ""
        row["part_cultures_pct"] = round(100 * v[40] / tot, 2) if tot else ""
        row["part_bati_pct"] = round(100 * v[50] / tot, 2) if tot else ""
        row["source"] = "ESA_WORLDCOVER_2021_V200"
        rows.append(row)
    with open(os.path.join(OUT, "occupation_sol_par_arrondissement.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    nat = {nom: round(total[1:, c].sum()) for c, nom in CLASSES.items()}
    print("classes inattendues:", inattendues)
    print("national ha:", nat, "total:", round(total[1:, list(CLASSES)].sum()), "nodata:", round(total[1:, 0].sum()))


if __name__ == "__main__":
    main()
