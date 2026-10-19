"""Télécharge une sélection d'indicateurs WDI (Banque mondiale) pour le Cameroun, 2010-2025.

Reproductible : python3 cameroun/models/fetch_wdi.py
Sorties :
  cameroun/data/raw/wdi_cmr_<date>.json   réponse brute de l'API, non modifiée
  cameroun/data/clean/wdi_cmr.csv         format long : code, indicateur, annee, valeur, source_url, date_consultation

Les valeurs WDI sont des séries compilées par la Banque mondiale à partir de sources
nationales et d'estimations ; certaines sont modélisées (ex. chômage OIT). Chaque ligne
garde le code de l'indicateur pour retrouver la métadonnée sur
https://data.worldbank.org/indicator/<code>?locations=CM
"""

import csv
import datetime as dt
import json
import pathlib
import urllib.request

INDICATORS = {
    "NY.GDP.MKTP.KD.ZG": "Croissance du PIB réel (%)",
    "NY.GDP.PCAP.KD.ZG": "Croissance du PIB réel par habitant (%)",
    "NY.GDP.PCAP.CD": "PIB par habitant (USD courants)",
    "FP.CPI.TOTL.ZG": "Inflation, prix à la consommation (%)",
    "SP.POP.TOTL": "Population totale",
    "SP.POP.GROW": "Croissance démographique (%)",
    "SP.URB.TOTL.IN.ZS": "Population urbaine (% du total)",
    "SI.POV.DDAY": "Pauvreté à 2,15 USD/jour PPA (% population)",
    "SI.POV.NAHC": "Pauvreté seuil national (% population)",
    "SI.POV.GINI": "Indice de Gini",
    "SL.UEM.TOTL.ZS": "Chômage (% population active, estimation modélisée OIT)",
    "SL.UEM.1524.ZS": "Chômage des 15-24 ans (% , estimation modélisée OIT)",
    "SL.EMP.VULN.ZS": "Emploi vulnérable (% de l'emploi total, estimation modélisée OIT)",
    "EG.ELC.ACCS.ZS": "Accès à l'électricité (% population)",
    "EG.ELC.ACCS.RU.ZS": "Accès à l'électricité, rural (% population rurale)",
    "EG.ELC.ACCS.UR.ZS": "Accès à l'électricité, urbain (% population urbaine)",
    "SH.DYN.MORT": "Mortalité des moins de 5 ans (pour 1 000 naissances vivantes)",
    "SH.STA.MMRT": "Mortalité maternelle (pour 100 000 naissances vivantes, estimation modélisée)",
    "SH.STA.STNT.ME.ZS": "Retard de croissance, moins de 5 ans (%)",
    "SH.XPD.OOPC.CH.ZS": "Dépenses de santé à la charge des ménages (% des dépenses courantes de santé)",
    "SH.XPD.CHEX.GD.ZS": "Dépenses courantes de santé (% du PIB)",
    "SE.PRM.CMPT.ZS": "Taux d'achèvement du primaire (% du groupe d'âge)",
    "SE.XPD.TOTL.GD.ZS": "Dépenses publiques d'éducation (% du PIB)",
    "SP.DYN.LE00.IN": "Espérance de vie à la naissance (années)",
    "SP.DYN.TFRT.IN": "Indice synthétique de fécondité",
    "GC.REV.XGRT.GD.ZS": "Recettes publiques hors dons (% du PIB)",
    "GC.TAX.TOTL.GD.ZS": "Recettes fiscales (% du PIB)",
    "DT.DOD.DECT.GN.ZS": "Dette extérieure totale (% du RNB)",
    "DT.TDS.DECT.EX.ZS": "Service de la dette extérieure (% des exportations)",
    "BN.CAB.XOKA.GD.ZS": "Solde courant (% du PIB)",
    "NE.GDI.TOTL.ZS": "Formation brute de capital (% du PIB)",
    "NV.AGR.TOTL.ZS": "Agriculture, valeur ajoutée (% du PIB)",
    "NV.IND.MANF.ZS": "Industrie manufacturière, valeur ajoutée (% du PIB)",
    "IT.NET.USER.ZS": "Utilisateurs d'Internet (% population)",
    "AG.LND.FRST.ZS": "Superficie forestière (% du territoire)",
    "SH.H2O.BASW.ZS": "Accès au moins à un service d'eau de base (% population)",
    "SH.STA.BASS.ZS": "Accès au moins à un assainissement de base (% population)",
}

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = "https://api.worldbank.org/v2/country/CMR/indicator/{code}?format=json&date=2010:2025&per_page=100"


def fetch(code: str):
    url = BASE.format(code=code)
    with urllib.request.urlopen(url, timeout=60) as r:
        return url, json.loads(r.read().decode("utf-8"))


def main() -> None:
    today = dt.date.today().isoformat()
    raw, rows = {}, []
    for code, label in INDICATORS.items():
        url, payload = fetch(code)
        raw[code] = {"url": url, "payload": payload}
        if len(payload) < 2 or payload[1] is None:
            continue
        for obs in payload[1]:
            if obs["value"] is None:
                continue
            rows.append({
                "code": code,
                "indicateur": label,
                "libelle_bm": obs["indicator"]["value"],
                "annee": obs["date"],
                "valeur": obs["value"],
                "source_url": f"https://data.worldbank.org/indicator/{code}?locations=CM",
                "api_url": url,
                "date_consultation": today,
            })
    (ROOT / "data/raw").mkdir(parents=True, exist_ok=True)
    (ROOT / f"data/raw/wdi_cmr_{today}.json").write_text(json.dumps(raw, ensure_ascii=False, indent=1))
    rows.sort(key=lambda x: (x["code"], x["annee"]))
    with open(ROOT / "data/clean/wdi_cmr.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} observations, {len({r['code'] for r in rows})} indicateurs avec données")


if __name__ == "__main__":
    main()
