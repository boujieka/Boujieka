"""Extrait 4 couches du paquet SIG 2018 de l'Atlas forestier interactif du Cameroun
(MINFOF / WRI, CC BY 4.0) en GeoJSON EPSG:4326, et calcule leurs surfaces par
arrondissement (geoBoundaries CMR ADM3).

Données personnelles : les champs nominatifs (attributaire, exploitant, société titulaire,
partenaire, utilisateurs d'édition) sont SUPPRIMÉS. Seuls restent la catégorie, le nom de
l'unité (forêt, aire protégée), les statuts, dates et surfaces administratives.

Usage : RAW=/chemin/temp python3 data/ressources/scripts/03_atlas_forestier.py
"""
import csv
import json
import os

import geopandas as gpd
import numpy as np
import pandas as pd

RAW = os.environ.get("RAW", "./raw_ressources")
OUT = os.path.join(os.path.dirname(__file__), "..")
GDB = os.path.join(RAW, "donnees_ouverts_fr.gdb")
SOURCE = "MINFOF_WRI_ATLAS_FORESTIER_SIG_2018"
EA = 6933  # équivalente (Lambert cylindrique, WGS84) pour les surfaces


def date_txt(s):
    s = pd.to_datetime(s, errors="coerce", utc=True)
    return s.dt.strftime("%Y-%m-%d").where(s.notna(), None)


def tg_ufa(row):
    return "FON.CONCESSION" if row["desc_type"] == "UFA" else "RES.FORET"


COUCHES = {
    "foret_ufa_et_communales": {
        "layer": "forets_production",
        "garder": ["desc_type", "nom_foret", "statu_class", "date_class", "rfa_ha", "sup_adm_ha", "sup_sig_ha"],
        "tg_type": tg_ufa,
        "regime_tg": lambda r: "FORET_COMMUNALE" if r["desc_type"] == "Forêt communale" else None,
        "categorie": lambda r: "ufa" if r["desc_type"] == "UFA" else "foret_communale",
    },
    "foret_communautaire": {
        "layer": "forets_communautaires",
        "garder": ["desc_type", "type_attr", "nom_fcom", "statu_conv", "statu_amgt", "date_con_p",
                   "date_con_d", "date_pgs", "sup_adm_ha", "sup_sig_ha"],
        "tg_type": lambda r: "RES.FORET",
        "regime_tg": lambda r: "FORET_COMMUNAUTAIRE",
        "categorie": lambda r: "foret_communautaire",
    },
    "aires_protegees_faune": {
        "layer": "aires_protegees_faune",
        "garder": ["desc_type", "nom_ap", "cat_uicn", "wdpaid", "statu_crea", "statu_amgt", "date_prop",
                   "date_crea", "date_amgt", "sup_adm_ha", "sup_sig_ha"],
        "tg_type": lambda r: "FON.AIRE_PROTEGEE",
        "regime_tg": lambda r: "AIRE_PROTEGEE",
        "categorie": lambda r: "aire_protegee",
    },
    "permis_miniers": {
        "layer": "permis_miniers",
        "garder": ["desc_type", "num_lic", "minerais", "date_attr", "date_expr", "sup_adm_km2", "sup_sig_km2"],
        "tg_type": lambda r: "FON.CONCESSION",
        "regime_tg": lambda r: None,
        "categorie": lambda r: "permis_exploitation_miniere" if r["desc_type"] == "Permis d'exploitation"
        else "permis_recherche_miniere",
    },
}


def corrige_nom(n):
    if n and ("Ã" in n or "Â" in n):
        try:
            return n.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            return n
    return n


def main():
    adm3 = gpd.read_file(os.path.join(RAW, "gb_adm3.geojson"))[["shapeID", "shapeName", "geometry"]]
    adm3["shapeName"] = adm3.shapeName.map(corrige_nom)
    adm3_ea = adm3.to_crs(EA)
    stats, controle, toutes = [], {}, []
    for nom, c in COUCHES.items():
        g = gpd.read_file(GDB, layer=c["layer"])
        n0 = len(g)
        g = g[g.geometry.notna() & ~g.geometry.is_empty].copy()
        g["geometry"] = g.geometry.make_valid()
        g = g.to_crs(4326)
        out = gpd.GeoDataFrame(geometry=g.geometry, crs=4326)
        out["tg_type"] = g.apply(c["tg_type"], axis=1)
        nomcol = [k for k in c["garder"] if k.startswith("nom_")]
        out["nom"] = g[nomcol[0]] if nomcol else None
        out["source_id"] = g["globalid"].str.strip("{}")
        out["source"] = SOURCE
        out["statut"] = "IMPORTE"
        out["date_source"] = date_txt(g["last_edited_date"])
        out["regime_tg"] = g.apply(c["regime_tg"], axis=1)
        out["categorie"] = g.apply(c["categorie"], axis=1)
        for k in c["garder"]:
            if k in nomcol:
                continue
            v = g[k]
            out[k] = date_txt(v) if str(v.dtype).startswith("datetime") else v
        out = out[[x for x in out.columns if x != "geometry"] + ["geometry"]]
        b = out.total_bounds
        f = os.path.join(OUT, f"{nom}_minfof2018.geojson")
        out.to_file(f, driver="GeoJSON", COORDINATE_PRECISION=6, RFC7946="YES")
        controle[nom] = {
            "nb_source": n0, "nb_exporte": len(out),
            "doublons_source_id": int(out.source_id.duplicated().sum()),
            "doublons_geometrie": int(out.geometry.to_wkb().duplicated().sum()),
            "emprise": [round(x, 4) for x in b],
            "dans_emprise_cameroun": bool(b[0] >= 8.3 and b[2] <= 16.3 and b[1] >= 1.5 and b[3] <= 13.2),
            "date_source_min": out.date_source.min(), "date_source_max": out.date_source.max(),
            "categories": out.categorie.value_counts().to_dict(),
            "taille_octets": os.path.getsize(f),
        }
        toutes.append(out[["categorie", "geometry"]])

    # Surfaces par arrondissement : union par catégorie (pas de double compte des chevauchements)
    tous = pd.concat(toutes).to_crs(EA)
    for cat, sub in tous.groupby("categorie"):
        u = gpd.GeoDataFrame(geometry=[sub.geometry.buffer(0).union_all()], crs=EA)
        inter = gpd.overlay(adm3_ea, u, how="intersection", keep_geom_type=True)
        inter["ha"] = inter.area / 1e4
        nb = gpd.sjoin(adm3_ea, sub, predicate="intersects").groupby("shapeID").size()
        for _, r in inter.iterrows():
            stats.append((r.shapeID, cat, r.ha, int(nb.get(r.shapeID, 0))))
        controle.setdefault("surface_nationale_union_ha", {})[cat] = round(float(u.area.iloc[0] / 1e4))
        controle.setdefault("surface_dans_arrondissements_ha", {})[cat] = round(float(inter.ha.sum()))

    df = pd.DataFrame(stats, columns=["shapeID", "categorie", "ha", "nb"])
    cats = ["ufa", "foret_communale", "foret_communautaire", "aire_protegee",
            "permis_recherche_miniere", "permis_exploitation_miniere"]
    ha = df.pivot_table(index="shapeID", columns="categorie", values="ha", aggfunc="sum").reindex(columns=cats)
    nb = df.pivot_table(index="shapeID", columns="categorie", values="nb", aggfunc="sum").reindex(columns=cats)
    adm3["superficie_ha"] = adm3_ea.area / 1e4
    rows = []
    for _, z in adm3.iterrows():
        row = {"arrondissement_id": z.shapeID, "arrondissement_nom": z.shapeName}
        for k in cats:
            h = ha[k].get(z.shapeID, np.nan) if k in ha else np.nan
            n = nb[k].get(z.shapeID, np.nan) if k in nb else np.nan
            row[f"{k}_ha"] = round(float(h), 1) if pd.notna(h) else 0.0
            row[f"{k}_nb"] = int(n) if pd.notna(n) else 0
        rows.append(row)
    for row in rows:
        row["source"] = SOURCE
        row["date_situation"] = "paquet publié 2019-03 ; dernières éditions 2015-06 à 2019-03"
    with open(os.path.join(OUT, "ressources_forestieres_minieres_par_arrondissement.csv"), "w",
              newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(json.dumps(controle, ensure_ascii=False, indent=1, default=str))
    with open(os.path.join(RAW, "controle_atlas.json"), "w") as fh:
        json.dump(controle, fh, ensure_ascii=False, indent=1, default=str)


if __name__ == "__main__":
    main()
