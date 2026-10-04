#!/usr/bin/env python3
"""Produit unites_administratives.csv et manifest.json à partir des sorties de 02 et 03.

Superficie : calculée sur les géométries publiées, projetées en Lambert azimutale équivalente
(+proj=laea +lat_0=7 +lon_0=12.5, ellipsoïde WGS84). nb_localites_osm : nombre de localités de
localites_osm.geojson rattachées à l'unité (toutes valeurs de place confondues), avec détail par place.
"""
import hashlib, json, pathlib
import geopandas as gpd, pandas as pd

ICI = pathlib.Path(__file__).resolve().parent.parent
C = ICI / ".cache"
J = json.load(open(C / "journal_telechargement.json"))
CL = json.load(open(C / "controles_limites.json"))
CO = json.load(open(C / "controles_localites.json"))
loc = gpd.read_file(ICI / "localites_osm.geojson")
PLACES = ["city", "town", "village", "hamlet", "suburb", "neighbourhood"]

lignes = []
for lvl in range(4):
    a = gpd.read_file(ICI / f"limites_adm{lvl}.geojson")
    key = None if lvl == 0 else f"adm{lvl}_code"
    for _, r in a.iterrows():
        sel = loc if key is None else loc[loc[key] == r.code]
        d = {"niveau": f"ADM{lvl}", "code": r.code, "nom": r.nom,
             "parent_code": r.parent_code if lvl else "", "parent_nom": "",
             "superficie_km2": r.superficie_km2, "superficie_ocha_km2": r.superficie_ocha_km2,
             "nb_localites_osm": len(sel)}
        for p in PLACES:
            d[f"nb_{p}"] = int((sel.place == p).sum())
        lignes.append(d)
df = pd.DataFrame(lignes)
noms = dict(zip(df.code, df.nom))
df["parent_nom"] = df.parent_code.map(noms).fillna("")
df.to_csv(ICI / "unites_administratives.csv", index=False, encoding="utf-8")
assert df[df.niveau == "ADM3"].nb_localites_osm.sum() == len(loc[loc.adm3_code.notna()])


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


F = J["fichiers"]; oc = F["ocha"]; osm = F["osm"]
date_osm = CO["date_situation_osm"][:10]
METH_LIM = ("scripts/01_telecharger.py puis scripts/02_limites.py : lecture de cmr_admin{0..3}.geojson (version standard, "
            "pas « _em ») de cmr_admin_boundaries.geojson.zip ; nom = champ *_name1 (français), nom_en = *_name (anglais, "
            "vide aux niveaux 2-3 dans la source) ; coordonnées arrondies à 6 décimales (grille 1e-6°, ≈ 0,11 m) ; "
            "AUCUNE simplification (fichiers < 15 Mo) ; superficie_km2 recalculée en Lambert azimutale équivalente "
            "(lat_0=7, lon_0=12.5, WGS84), superficie_ocha_km2 = champ area_sqkm de la source.")
LIM_LIM = ("Découpage valide au 2019-01-04 (valid_on de la source, version v01) : ne reflète pas d'éventuelles "
           "créations d'unités postérieures. Noms des arrondissements souvent sans accents dans la source "
           "(ex. « Yaounde 1er », « Eseka »). tg_type = null : aucun code d'unité administrative dans nomenclatures/objets.yaml. "
           "Écarts avec geoBoundaries : voir comparaison_ocha_geoboundaries.csv et le champ comparaison_geoboundaries.")

man = {
    "theme": "admin",
    "description": "Limites administratives (ADM0-ADM3) et localités du Cameroun",
    "date_collecte": J["date_telechargement"],
    "sources": {
        "OCHA_CODAB_CMR_2019-01-04_v01": {
            "producteur": "OCHA (Bureau de la coordination des affaires humanitaires des Nations unies), Common Operational Dataset - Administrative Boundaries, Cameroun, via HDX",
            "page": "https://data.humdata.org/dataset/cod-ab-cmr", "url": oc["url"], "licence": oc["licence"],
            "attribution": "OCHA, COD-AB Cameroun (HDX), CC BY-IGO", "derniere_modification_hdx": oc["last_modified"],
            "sha256_source": oc["sha256"], "role": "référence pour les limites ADM0-ADM3"},
        "OSM_OSMFR_" + date_osm: {
            "producteur": "Contributeurs OpenStreetMap, extrait Cameroun publié par OpenStreetMap France",
            "url": osm["url"], "licence": osm["licence"], "attribution": "© les contributeurs d'OpenStreetMap",
            "etat_replication": osm.get("state", "").strip(), "sha256_source": osm["sha256"],
            "role": "localités (place=*) et frontière OSM du Cameroun (relation/192830) pour filtrer l'extrait"},
        "GEOBOUNDARIES_GBOPEN_CMR": {
            "producteur": "geoBoundaries (William & Mary geoLab), gbOpen CMR, build Dec 12, 2023",
            "page": "https://www.geoboundaries.org/api/current/gbOpen/CMR/",
            "fichiers": {k: {"url": v["url"], "url_api": v["url_api"], "sha256_source": v["sha256"], "licence": v["licence"],
                             "source_amont": v["source"], "annee_representee": v["annee"], "nb_unites": v["nb"]}
                         for k, v in F.items() if k.startswith("gb_")},
            "role": "comparaison uniquement ; aucune géométrie geoBoundaries n'est redistribuée ici",
            "remarque_licence": "Licences hétérogènes selon le niveau (CC BY 3.0 pour ADM0-1, CC BY 4.0 pour ADM2, ODbL 1.0 pour ADM3) : raison supplémentaire de ne pas la retenir comme référence."},
    },
    "sources_inaccessibles": [
        {"url": "https://download.geofabrik.de/africa/cameroon-latest.osm.pbf",
         "constat": "Connexion coupée (tunnel fermé) depuis l'environnement de collecte le " + J["date_telechargement"] + " ; remplacée par l'extrait équivalent d'OpenStreetMap France (mêmes données OSM, même licence ODbL)."},
        {"url": "https://overpass-api.de/api/", "constat": "Connexion coupée depuis l'environnement de collecte ; non utilisée."},
        {"url": "https://github.com/wmgeolab/geoBoundaries/raw/...", "constat": "HTTP 403 depuis l'environnement de collecte ; fichiers identiques (même commit 9469f09) lus sur media.githubusercontent.com."},
    ],
    "fichiers": [],
}
for lvl in range(4):
    f = f"limites_adm{lvl}.geojson"; c = CL[f"ADM{lvl}"]
    man["fichiers"].append({
        "fichier": f"admin/{f}", "source_code": "OCHA_CODAB_CMR_2019-01-04_v01",
        "producteur": man["sources"]["OCHA_CODAB_CMR_2019-01-04_v01"]["producteur"], "url": oc["url"],
        "licence": oc["licence"], "attribution": "OCHA, COD-AB Cameroun (HDX), CC BY-IGO",
        "date_telechargement": J["date_telechargement"], "date_situation": "2019-01-04",
        "sha256_source": oc["sha256"], "sha256_fichier": sha(ICI / f), "nb_entites": c["nb"],
        "methode": METH_LIM, "tolerance_simplification": "aucune simplification ; arrondi des coordonnées à 1e-6°",
        "limites": LIM_LIM,
        "controle": c,
    })
man["fichiers"].append({
    "fichier": "admin/localites_osm.geojson", "source_code": "OSM_OSMFR_" + date_osm,
    "producteur": "Contributeurs OpenStreetMap, extrait OpenStreetMap France", "url": osm["url"],
    "licence": "ODbL 1.0", "attribution": "© les contributeurs d'OpenStreetMap",
    "date_telechargement": J["date_telechargement"], "date_situation": date_osm,
    "sha256_source": osm["sha256"], "sha256_fichier": sha(ICI / "localites_osm.geojson"), "nb_entites": CO["nb_localites"],
    "methode": ("scripts/03_localites.py (pyosmium) : nœuds, chemins et relations portant place=city|town|village|hamlet|suburb|"
                "neighbourhood ; surfaces ramenées à un point intérieur (point_on_surface) ; clés gardées : name, name:fr, name:en, "
                "place, population, population:date, source:population, wikidata ; exclusion des objets hors de la frontière OSM "
                "du Cameroun (relation/192830) ; rattachement ADM1/2/3 OCHA par point-dans-polygone, ou ADM3 le plus proche "
                "(<= 5 km) pour les points dans la frontière OSM mais hors des polygones OCHA (champ rattachement)."),
    "limites": ("Couverture OSM inégale : 2 arrondissements sans aucune localité (Nkongsamba 1er et 2e). Les villages "
                "et hameaux non cartographiés dans OSM manquent ; la classe place est celle des contributeurs, pas une "
                "catégorie officielle. population : texte brut OSM, renseigné pour très peu d'objets et rarement daté "
                "(une valeur non numérique « i dont know » conservée telle quelle) — ne pas l'utiliser comme statistique. "
                f"{CO['nb_exclus_hors_frontiere_osm_cameroun']} objets de l'extrait exclus car hors frontière OSM du Cameroun "
                "(l'extrait OSM France déborde sur les pays voisins). Les tracés de frontière OSM et OCHA diffèrent "
                "légèrement : quelques localités proches de la frontière peuvent être exclues ou attribuées au mauvais côté. "
                "Doublons possibles : champ doublon_probable (même nom à moins de 500 m), non supprimés."),
    "controle": CO,
})
man["fichiers"].append({
    "fichier": "admin/unites_administratives.csv", "source_code": ["OCHA_CODAB_CMR_2019-01-04_v01", "OSM_OSMFR_" + date_osm],
    "licence": "CC BY-IGO (limites OCHA) et ODbL 1.0 (comptes de localités dérivés d'OSM)",
    "attribution": "OCHA, COD-AB Cameroun (HDX) ; © les contributeurs d'OpenStreetMap",
    "date_telechargement": J["date_telechargement"], "sha256_fichier": sha(ICI / "unites_administratives.csv"),
    "nb_entites": len(df), "methode": "scripts/04_tableau_et_manifest.py",
    "limites": "nb_localites_osm compte les objets OSM, pas les localités réelles ; voir les limites de localites_osm.geojson.",
    "controle": {"lignes_par_niveau": df.niveau.value_counts().sort_index().to_dict(),
                 "somme_localites_adm3_egale_total": bool(df[df.niveau == "ADM3"].nb_localites_osm.sum() == CO["nb_localites"] - CO["par_rattachement"].get("non_rattachee_>5km", 0))},
})
man["fichiers"].append({
    "fichier": "admin/comparaison_ocha_geoboundaries.csv", "source_code": ["OCHA_CODAB_CMR_2019-01-04_v01", "GEOBOUNDARIES_GBOPEN_CMR"],
    "licence": "CC BY-IGO / CC BY 3.0 / CC BY 4.0 / ODbL 1.0 (noms et identifiants issus des deux sources)",
    "sha256_fichier": sha(ICI / "comparaison_ocha_geoboundaries.csv"),
    "methode": ("scripts/02_limites.py : pour chaque unité OCHA, unité geoBoundaries de plus grand recouvrement "
                "(intersection en projection équivalente) ; recouvrement_iou = intersection / union ; noms geoBoundaries "
                "réparés de l'encodage (UTF-8 lu en Latin-1) ; type_ecart_nom = identique | orthographe (accents, "
                "numéros 1er/I/1st, similarité >= 0,8) | nom_different."),
})
man["comparaison_geoboundaries"] = {k: v for k, v in CL.items() if k.startswith("comparaison_")}
man["comparaison_geoboundaries"]["synthese"] = (
    "ADM1 : 10/10, noms identiques (gB en anglais, OCHA fournit aussi l'anglais). "
    "ADM2 : 58 (OCHA) contre 60 (gB) : gB découpe Ndian et Sanaga-Maritime en deux entités chacune (une pièce principale + "
    "une pièce de 3,5 km² et 1,3 km²), soit 58 départements distincts ; 12 départements ont un recouvrement < 0,8, "
    "surtout les petits départements urbains et de l'Ouest/Nord-Ouest (Mfoundi, Wouri, Mifi, Koung-Khi...) : le tracé gB ADM2 (Open Africa, 2016) est plus grossier. "
    "ADM3 : 360/360, géométries quasi identiques (IoU médian 1,0 : les deux dérivent d'OSM/Wambacher) mais "
    "noms différents pour une partie des arrondissements, souvent nom de l'arrondissement (OCHA) contre nom du chef-lieu (gB), "
    "ex. Assamba/Olanguina, Dja/Mindourou, West-Coast/Idenau ; liste dans noms_differents.")
json.dump(man, open(ICI / "manifest.json", "w"), indent=2, ensure_ascii=False, default=str)
print(df.groupby("niveau").agg(n=("code", "size"), km2=("superficie_km2", "sum"), loc=("nb_localites_osm", "sum")))
