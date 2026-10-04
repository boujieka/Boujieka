#!/usr/bin/env python3
"""Produit les couches ADM0-ADM3 à partir de l'OCHA COD-AB (référence) et compare avec geoBoundaries.

Entrée : .cache/ocha/cmr_admin{0..3}.geojson (version standard, pas « _em »), .cache/geoBoundaries-CMR-ADM*.geojson
Sortie : limites_adm{0..3}.geojson, comparaison_ocha_geoboundaries.csv, .cache/controles_limites.json
Géométries : coordonnées arrondies à 6 décimales (shapely.set_precision grille 1e-6 deg ≈ 0,11 m),
puis make_valid si nécessaire. Aucune simplification (tous les fichiers < 15 Mo).
"""
import json, pathlib, unicodedata, re
import geopandas as gpd, pandas as pd, shapely

ICI = pathlib.Path(__file__).resolve().parent.parent
C = ICI / ".cache"
SRC = "OCHA_CODAB_CMR_2019-01-04_v01"
DATE = "2019-01-04"  # champ valid_on de la source
LAEA = "+proj=laea +lat_0=7 +lon_0=12.5 +datum=WGS84 +units=m +no_defs"  # projection équivalente (Lambert azimutale)
BBOX = (8.4, 1.6, 16.2, 13.1)


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", s)


ROMAINS = {"1er": "i", "2e": "ii", "3e": "iii", "1st": "i", "2nd": "ii", "3rd": "iii", "2": "ii", "4e": "iv", "5e": "v", "6e": "vi", "7e": "vii"}


def demojibake(s):
    """Les noms geoBoundaries ADM3 sont en UTF-8 relu comme Latin-1 (ex. « YaoundÃ© »). Réparation si possible."""
    try:
        return s.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
        return s


def norm2(s):
    s = " ".join(ROMAINS.get(w.lower(), w) for w in str(s or "").split())
    return norm(s)


def type_ecart(a, b_list):
    """identique | orthographe (identique après normalisation accents/numéros, ou similarité >= 0.8) | nom_different"""
    import difflib
    if any(norm(a) == norm(b) for b in b_list):
        return "identique"
    if any(norm2(a) == norm2(b) or difflib.SequenceMatcher(None, norm2(a), norm2(b)).ratio() >= 0.8 for b in b_list):
        return "orthographe"
    return "nom_different"


def nom_fr(row, lvl):
    # lang=en, lang1=fr dans ces fichiers : *_name1 = nom français, *_name = nom anglais (souvent vide aux niveaux 2-3)
    return row.get(f"adm{lvl}_name1") or row.get(f"adm{lvl}_name")


ctrl = {}
couches = {}
for lvl in range(4):
    g = gpd.read_file(C / f"ocha/cmr_admin{lvl}.geojson").to_crs(4326)
    out = pd.DataFrame({
        "tg_type": None,  # pas de code d'unité administrative dans nomenclatures/objets.yaml
        "niveau": f"ADM{lvl}",
        "code": g[f"adm{lvl}_pcode"],
        "nom": [nom_fr(r, lvl) for _, r in g.iterrows()],
        "nom_en": g[f"adm{lvl}_name"] if lvl < 2 else None,
    })
    if lvl == 0:
        out["nom"] = "Cameroun"; out["nom_en"] = g["adm0_name"]
    out["parent_code"] = g[f"adm{lvl-1}_pcode"] if lvl else None
    for k in range(1, lvl):
        out[f"adm{k}_code"] = g[f"adm{k}_pcode"]
        out[f"adm{k}_nom"] = [nom_fr(r, k) for _, r in g.iterrows()]
    out["superficie_ocha_km2"] = g["area_sqkm"].round(2)
    geom = shapely.set_precision(g.geometry.values, 1e-6)
    inval = int((~shapely.is_valid(geom)).sum())
    geom = shapely.make_valid(geom)
    out["superficie_km2"] = gpd.GeoSeries(geom, crs=4326).to_crs(LAEA).area.div(1e6).round(2).values
    out["source"] = SRC; out["source_id"] = out["code"]; out["statut"] = "IMPORTE"; out["date_source"] = DATE
    gdf = gpd.GeoDataFrame(out, geometry=geom, crs=4326).sort_values("code").reset_index(drop=True)
    f = ICI / f"limites_adm{lvl}.geojson"
    f.unlink(missing_ok=True)
    gdf.to_file(f, driver="GeoJSON", COORDINATE_PRECISION=6, RFC7946="YES")
    b = gdf.total_bounds
    ctrl[f"ADM{lvl}"] = {
        "nb": len(gdf), "codes_uniques": gdf.code.is_unique, "noms_dupliques": sorted(gdf.nom[gdf.nom.duplicated(keep=False)].unique().tolist()),
        "invalides_apres_arrondi_avant_make_valid": inval, "invalides_final": int((~gdf.is_valid).sum()),
        "types": gdf.geom_type.value_counts().to_dict(),
        "emprise": [round(x, 4) for x in b], "dans_emprise_cameroun": bool(b[0] >= BBOX[0] and b[1] >= BBOX[1] and b[2] <= BBOX[2] and b[3] <= BBOX[3]),
        "ecart_max_superficie_vs_ocha_pct": float(((gdf.superficie_km2 - gdf.superficie_ocha_km2).abs() / gdf.superficie_ocha_km2 * 100).max().round(3)),
        "taille_mo": round(f.stat().st_size / 1e6, 2),
    }
    if lvl:
        par = couches[lvl - 1]
        ctrl[f"ADM{lvl}"]["parents_inconnus"] = int((~gdf.parent_code.isin(par.code)).sum())
        # cohérence emboîtement : le point représentatif de l'unité est dans son parent
        j = gpd.sjoin(gpd.GeoDataFrame(gdf[["code", "parent_code"]], geometry=gdf.representative_point(), crs=4326),
                      par[["code", "geometry"]].rename(columns={"code": "code_par"}), predicate="within")
        ctrl[f"ADM{lvl}"]["emboitement_incoherent"] = int((j.parent_code != j.code_par).sum()) + (len(gdf) - len(j))
    couches[lvl] = gdf

# Couverture : somme des ADM3 vs ADM0
a0 = couches[0].superficie_km2.sum(); a3 = couches[3].superficie_km2.sum()
ctrl["couverture_adm3_sur_adm0_pct"] = round(a3 / a0 * 100, 3)

# ---- Comparaison geoBoundaries ----
rows = []
for lvl in range(1, 4):
    gb = gpd.read_file(C / f"geoBoundaries-CMR-ADM{lvl}.geojson").to_crs(4326)
    gb["geometry"] = shapely.make_valid(gb.geometry.values)
    gb["shapeName"] = gb.shapeName.map(demojibake)
    oc = couches[lvl]
    # appariement spatial : pour chaque unité OCHA, l'unité geoBoundaries de plus grand recouvrement
    oc_e = oc[["code", "nom", "geometry"]].to_crs(LAEA); gb_e = gb[["shapeID", "shapeName", "geometry"]].to_crs(LAEA)
    inter = gpd.overlay(oc_e, gb_e, how="intersection", keep_geom_type=True)
    inter["a"] = inter.area
    best = inter.sort_values("a", ascending=False).drop_duplicates("code")
    best = best.merge(oc_e.assign(a_oc=oc_e.area)[["code", "a_oc"]], on="code").merge(gb_e.assign(a_gb=gb_e.area)[["shapeID", "a_gb"]], on="shapeID")
    best["iou"] = best.a / (best.a_oc + best.a_gb - best.a)
    nb_ocha_par_gb = best.shapeID.value_counts()
    for _, r in oc.iterrows():
        b = best[best.code == r.code]
        if len(b):
            b = b.iloc[0]
            rows.append({"niveau": f"ADM{lvl}", "code_ocha": r.code, "nom_ocha": r.nom, "shape_id_gb": b.shapeID, "nom_gb": b.shapeName,
                         "nom_en_ocha": r.nom_en,
                         "type_ecart_nom": type_ecart(b.shapeName, [r.nom] + ([r.nom_en] if isinstance(r.nom_en, str) else [])),
                         "recouvrement_iou": round(b.iou, 3),
                         "nb_unites_ocha_sur_meme_unite_gb": int(nb_ocha_par_gb[b.shapeID])})
        else:
            rows.append({"niveau": f"ADM{lvl}", "code_ocha": r.code, "nom_ocha": r.nom})
    non_app = sorted(set(gb.shapeID) - set(best.shapeID))
    for sid in non_app:
        rows.append({"niveau": f"ADM{lvl}", "shape_id_gb": sid, "nom_gb": gb.set_index("shapeID").shapeName[sid], "remarque": "unité geoBoundaries sans unité OCHA de plus grand recouvrement"})
    cmp = pd.DataFrame([x for x in rows if x["niveau"] == f"ADM{lvl}"])
    ctrl[f"comparaison_ADM{lvl}"] = {
        "nb_ocha": len(oc), "nb_geoboundaries": len(gb),
        "noms_geoboundaries_dupliques": sorted(gb.shapeName[gb.shapeName.duplicated(keep=False)].unique().tolist()),
        "type_ecart_nom": cmp.type_ecart_nom.value_counts().to_dict(),
        "noms_differents": [f"{a} (OCHA) / {b} (gB)" for a, b in cmp[cmp.type_ecart_nom == "nom_different"][["nom_ocha", "nom_gb"]].values],
        "iou_median": float(cmp.recouvrement_iou.median()), "nb_iou_inf_0_8": int((cmp.recouvrement_iou < 0.8).sum()),
        "iou_inf_0_8": cmp[cmp.recouvrement_iou < 0.8].nom_ocha.tolist(),
        "unites_ocha_partageant_une_unite_gb": int((cmp.nb_unites_ocha_sur_meme_unite_gb > 1).sum()),
        "unites_gb_non_appariees": [gb.set_index("shapeID").shapeName[s] for s in non_app],
    }
pd.DataFrame(rows).to_csv(ICI / "comparaison_ocha_geoboundaries.csv", index=False)
json.dump(ctrl, open(C / "controles_limites.json", "w"), indent=2, ensure_ascii=False, default=str)
print(json.dumps(ctrl, indent=2, ensure_ascii=False, default=str))
