"""Table de rapprochement des établissements de santé entre sources.

Aucune source n'en écrase une autre : la table relie des identifiants, chaque couche reste intacte.

Étapes
 1. OSM <-> healthsites : healthsites.io est alimenté par OSM, chaque entrée porte son
    identifiant OSM (osm_type/osm_id). Lien direct par identifiant identique.
 2. OSM <-> healthsites (résidus) : distance < 500 m ET similarité de nom >= SEUIL, appariement 1-1.
 3. Maina 2019 <-> entités OSM/healthsites issues de 1-2 : distance < 500 m ET similarité de
    nom >= SEUIL ET types compatibles (hôpital<->hôpital, centre<->clinique, type inconnu
    compatible avec tout), appariement 1-1 glouton (meilleure similarité puis plus courte distance).
Similarité : moyenne de rapidfuzz.token_set_ratio et token_sort_ratio sur les noms normalisés
(minuscules, sans accents) dont on retire les termes génériques (centre, santé, intégré, CSI,
hôpital, district...). Un nom vide ou purement générique ne peut pas être apparié
(l'identité ne peut pas être vérifiée).

Sortie : data/social/sante/rapprochement_sources_sante.csv, $TMP/controles_rapprochement.json
"""
import json

import geopandas as gpd
import numpy as np
import pandas as pd
from rapidfuzz import fuzz

from commun import SOCIAL, TMP, norm

DIST_M = 500
SEUIL = 85
CRS_M = 32633

GENERIQUES = set("""
centre center centres sante health integre integree integrated csi cma cmi medical medicale
medico d de du des la le les l et and of the hopital hospital hopitaux district regional
regionale general generale clinique clinic dispensaire poste case post annexe arrondissement
publique public hd hr cs dist reg h c s
""".split())


def nom_court(s):
    toks = [t for t in norm(s).split() if t not in GENERIQUES]
    return " ".join(toks)


def sim(a, b):
    """Similarité 0-100 ; 0 si un nom est vide ou purement générique."""
    na, nb = norm(a), norm(b)
    if not na or not nb:
        return 0.0
    ca, cb = nom_court(a), nom_court(b)
    if ca and cb:
        # moyenne set/sort : token_set seul donne 100 dès qu'un nom est inclus dans l'autre
        # (« Soa » vs « Soa Université »), token_sort pénalise ces inclusions.
        return (fuzz.token_set_ratio(ca, cb) + fuzz.token_sort_ratio(ca, cb)) / 2
    # Nom purement générique (« Centre de santé intégré ») d'un côté au moins : identité invérifiable.
    return 0.0


FAMILLE = {"SOC.SANTE.HOPITAL": "HOP", "SOC.SANTE.CENTRE": "CS", "SOC.SANTE.CLINIQUE": "CS",
           "SOC.SANTE.PHARMACIE": "PHA", "SOC.SANTE.LABORATOIRE": "LAB"}


def types_compatibles(ta, tb):
    """Hôpital <-> hôpital ; centre <-> clinique ; type inconnu compatible avec tout."""
    fa, fb = FAMILLE.get(ta), FAMILLE.get(tb)
    return fa is None or fb is None or fa == fb


def apparier(ga, gb, dist_m=DIST_M, seuil=SEUIL):
    """Appariement 1-1 glouton. Retourne une liste (i, j, distance_m, similarite)."""
    a = ga.to_crs(CRS_M)
    b = gb.to_crs(CRS_M)
    ia, ib = b.sindex.query(a.geometry.buffer(dist_m), predicate="intersects")
    cands = []
    for i, j in zip(ia, ib):
        d = a.geometry.iloc[i].distance(b.geometry.iloc[j])
        if d >= dist_m or not types_compatibles(ga["tg_type"].iloc[i], gb["tg_type"].iloc[j]):
            continue
        s = sim(ga["nom"].iloc[i], gb["nom"].iloc[j])
        if s >= seuil:
            cands.append((i, j, d, s))
    cands.sort(key=lambda t: (-t[3], t[2]))
    pris_a, pris_b, out = set(), set(), []
    for i, j, d, s in cands:
        if i in pris_a or j in pris_b:
            continue
        pris_a.add(i)
        pris_b.add(j)
        out.append((i, j, d, s))
    return out


O = gpd.read_parquet(TMP / "sante_osm.parquet").reset_index(drop=True)
H = gpd.read_parquet(TMP / "sante_healthsites.parquet").reset_index(drop=True)
M = gpd.read_parquet(TMP / "sante_maina.parquet").reset_index(drop=True)
ctl = {"parametres": {"distance_max_m": DIST_M, "seuil_similarite_nom": SEUIL,
                      "fonction": "moyenne(token_set_ratio, token_sort_ratio) rapidfuzz sur noms sans termes génériques ; noms vides ou génériques non appariables",
                      "projection_distances": f"EPSG:{CRS_M}",
                      "compatibilite_types": "HOPITAL<->HOPITAL ; CENTRE<->CLINIQUE ; PHARMACIE<->PHARMACIE ; LABORATOIRE<->LABORATOIRE ; null compatible avec tout"}}

# --- 1. lien par identifiant OSM
o_idx = {sid: i for i, sid in enumerate(O["source_id"])}
lien_oh = {}  # i_osm -> (j_hs, methode, dist, sim)
for j, sid in enumerate(H["source_id"]):
    if sid in o_idx:
        lien_oh[o_idx[sid]] = (j, "id_osm", None, None)
n_id = len(lien_oh)
# contrôle : écart de position entre l'objet OSM actuel et sa copie healthsites
_om, _hm = O.to_crs(CRS_M).geometry, H.to_crs(CRS_M).geometry
d_id = np.array([_om.iloc[i].distance(_hm.iloc[v[0]]) for i, v in lien_oh.items()])
ctl["ecart_position_liens_id_osm_m"] = {
    "mediane": round(float(np.median(d_id)), 1), "max": round(float(d_id.max()), 1),
    "nb_ecart_sup_100m": int((d_id > 100).sum())} if len(d_id) else None

# --- 2. résidus : distance + nom
o_rest = [i for i in range(len(O)) if i not in lien_oh]
h_lies = {v[0] for v in lien_oh.values()}
h_rest = [j for j in range(len(H)) if j not in h_lies]
for i, j, d, s in apparier(O.iloc[o_rest], H.iloc[h_rest]):
    lien_oh[o_rest[i]] = (h_rest[j], "distance_nom", d, s)
n_dn = len(lien_oh) - n_id

# --- entités OSM/healthsites
ent = []
h_lies = {}
for i in range(len(O)):
    r = {"osm": i, "hs": None, "methode_osm_hs": None}
    if i in lien_oh:
        r["hs"], r["methode_osm_hs"] = lien_oh[i][0], lien_oh[i][1]
        h_lies[lien_oh[i][0]] = True
    ent.append(r)
for j in range(len(H)):
    if j not in h_lies:
        ent.append({"osm": None, "hs": j, "methode_osm_hs": None})


def ref(e):
    """Position et nom de référence d'une entité OSM/HS (OSM prioritaire, HS si nom OSM vide)."""
    if e["osm"] is not None:
        g, n = O.geometry.iloc[e["osm"]], O["nom"].iloc[e["osm"]]
        if not n and e["hs"] is not None:
            n = H["nom"].iloc[e["hs"]]
        return g, n
    return H.geometry.iloc[e["hs"]], H["nom"].iloc[e["hs"]]


def type_ref(e):
    t = O["tg_type"].iloc[e["osm"]] if e["osm"] is not None else None
    if t is None and e["hs"] is not None:
        t = H["tg_type"].iloc[e["hs"]]
    return t


E = gpd.GeoDataFrame({"nom": [ref(e)[1] for e in ent], "tg_type": [type_ref(e) for e in ent]},
                     geometry=[ref(e)[0] for e in ent], crs=4326)

# --- 3. Maina <-> entités
lien_m = {}
for k, m, d, s in apparier(E, M):
    lien_m[k] = (m, d, s)

# sensibilité (information seulement)
sens = {}
for dm, se in [(250, 85), (500, 75), (500, 85), (500, 95), (1000, 85), (2000, 85), (5000, 85)]:
    sens[f"dist<{dm}m_sim>={se}"] = len(apparier(E, M, dm, se))
ctl["sensibilite_maina_vs_osm_hs_nb_paires"] = sens

# --- table
lignes = []
for k, e in enumerate(ent):
    r = {}
    i, j = e["osm"], e["hs"]
    r["osm_source_id"] = O["source_id"].iloc[i] if i is not None else None
    r["healthsites_source_id"] = H["source_id"].iloc[j] if j is not None else None
    m = lien_m.get(k)
    r["maina_source_id"] = M["source_id"].iloc[m[0]] if m else None
    r["nom_osm"] = O["nom"].iloc[i] if i is not None else None
    r["nom_healthsites"] = H["nom"].iloc[j] if j is not None else None
    r["nom_maina"] = M["nom"].iloc[m[0]] if m else None
    r["tg_type_osm"] = O["tg_type"].iloc[i] if i is not None else None
    r["tg_type_healthsites"] = H["tg_type"].iloc[j] if j is not None else None
    r["tg_type_maina"] = M["tg_type"].iloc[m[0]] if m else None
    r["methode_osm_healthsites"] = e["methode_osm_hs"]
    r["distance_m_maina"] = round(m[1], 1) if m else None
    r["similarite_nom_maina"] = round(m[2], 1) if m else None
    g = E.geometry.iloc[k]
    r["position_source"] = "OSM" if i is not None else "HEALTHSITES"
    r["lon"], r["lat"] = round(g.x, 6), round(g.y, 6)
    lignes.append(r)
for m in sorted(set(range(len(M))) - {v[0] for v in lien_m.values()}):
    g = M.geometry.iloc[m]
    lignes.append({"maina_source_id": M["source_id"].iloc[m], "nom_maina": M["nom"].iloc[m],
                   "tg_type_maina": M["tg_type"].iloc[m], "position_source": "MAINA2019",
                   "lon": round(g.x, 6), "lat": round(g.y, 6)})

T = pd.DataFrame(lignes)
cols = ["osm_source_id", "healthsites_source_id", "maina_source_id"]
T["dans_osm"] = T["osm_source_id"].notna()
T["dans_healthsites"] = T["healthsites_source_id"].notna()
T["dans_maina2019"] = T["maina_source_id"].notna()
T["nb_sources"] = T[["dans_osm", "dans_healthsites", "dans_maina2019"]].sum(axis=1)
T["sources"] = T.apply(lambda r: ";".join(n for n, f in [("OSM", r.dans_osm),
                                                         ("HEALTHSITES", r.dans_healthsites),
                                                         ("MAINA2019", r.dans_maina2019)] if f), axis=1)
T = T.sort_values(["nb_sources", "osm_source_id", "healthsites_source_id", "maina_source_id"],
                  ascending=[False, True, True, True], na_position="last").reset_index(drop=True)
T.insert(0, "etablissement_id", [f"RAPP_{n:06d}" for n in range(1, len(T) + 1)])
ordre = ["etablissement_id", "nb_sources", "sources", "dans_osm", "dans_healthsites", "dans_maina2019",
         "osm_source_id", "healthsites_source_id", "maina_source_id", "nom_osm", "nom_healthsites",
         "nom_maina", "tg_type_osm", "tg_type_healthsites", "tg_type_maina",
         "methode_osm_healthsites", "distance_m_maina", "similarite_nom_maina",
         "position_source", "lon", "lat"]
T = T[ordre]
T.to_csv(SOCIAL / "sante/rapprochement_sources_sante.csv", index=False)


def pct(a, b):
    return round(100 * a / b, 1) if b else None


o_pub = O["tg_type"].isin(["SOC.SANTE.CENTRE", "SOC.SANTE.HOPITAL"])
osm_avec_m = {ent[k]["osm"] for k in lien_m if ent[k]["osm"] is not None}
ctl.update({
    "nb_lignes_table": int(len(T)),
    "repartition_par_combinaison_de_sources": {k: int(v) for k, v in T["sources"].value_counts().items()},
    "osm_healthsites": {
        "liens_par_identifiant_osm": n_id, "liens_par_distance_et_nom": n_dn,
        "pct_osm_present_dans_healthsites": pct(len(lien_oh), len(O)),
        "pct_healthsites_present_dans_osm": pct(len(lien_oh), len(H)),
        "healthsites_sans_correspondant_osm_actuel": int(len(H) - len(lien_oh)),
        "avertissement": "healthsites.io est dérivé d'OSM : ce recouvrement mesure la synchronisation "
                         "entre deux copies d'OSM, pas une confirmation indépendante.",
    },
    "maina_vs_osm_healthsites": {
        "maina_apparies": len(lien_m),
        "pct_maina_retrouves_dans_osm_ou_healthsites": pct(len(lien_m), len(M)),
        "pct_osm_centres_et_hopitaux_retrouves_dans_maina":
            pct(len(osm_avec_m & set(np.where(o_pub)[0])), int(o_pub.sum())),
        "accord_tg_type_sur_paires_osm_maina": None,
        "distance_mediane_m": round(float(np.median([v[1] for v in lien_m.values()])), 1) if lien_m else None,
    },
})
paires = T[T.dans_osm & T.dans_maina2019]
if len(paires):
    ctl["maina_vs_osm_healthsites"]["accord_tg_type_sur_paires_osm_maina"] = pct(
        int((paires.tg_type_osm == paires.tg_type_maina).sum()), len(paires))
with open(TMP / "controles_rapprochement.json", "w") as fh:
    json.dump(ctl, fh, ensure_ascii=False, indent=2)
print(json.dumps(ctl, ensure_ascii=False, indent=1))
