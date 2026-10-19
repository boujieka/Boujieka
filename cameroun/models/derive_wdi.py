"""Indicateurs dérivés à partir de data/clean/wdi_cmr.csv (aucune donnée externe).

python3 cameroun/models/derive_wdi.py  ->  cameroun/outputs/wdi_derives.csv
"""
import csv, collections, pathlib, statistics

ROOT = pathlib.Path(__file__).resolve().parents[1]
d = collections.defaultdict(dict)
for r in csv.DictReader(open(ROOT / "data/clean/wdi_cmr.csv", encoding="utf-8")):
    d[r["code"]][int(r["annee"])] = float(r["valeur"])

def mean(code, a, b):
    v = [d[code][y] for y in range(a, b + 1) if y in d[code]]
    return round(statistics.mean(v), 2), len(v)

out = []
for code, a, b in [("NY.GDP.MKTP.KD.ZG", 2010, 2019), ("NY.GDP.MKTP.KD.ZG", 2020, 2025),
                   ("NY.GDP.PCAP.KD.ZG", 2010, 2019), ("NY.GDP.PCAP.KD.ZG", 2020, 2025),
                   ("SP.POP.GROW", 2010, 2025), ("FP.CPI.TOTL.ZG", 2010, 2019), ("FP.CPI.TOTL.ZG", 2022, 2025)]:
    m, n = mean(code, a, b)
    out.append({"calcul": f"moyenne {code} {a}-{b}", "valeur": m, "n_annees": n})

# Croissance cumulée du PIB réel par habitant
g = d["NY.GDP.PCAP.KD.ZG"]
idx = 1.0
for y in range(2011, 2026):
    if y in g:
        idx *= 1 + g[y] / 100
out.append({"calcul": "PIB réel par habitant, indice 2025 (2010=100)", "valeur": round(idx * 100, 1),
            "n_annees": sum(1 for y in range(2011, 2026) if y in g)})
# Population supplémentaire
p = d["SP.POP.TOTL"]
out.append({"calcul": "Population additionnelle 2010-2025", "valeur": round(p[2025] - p[2010]), "n_annees": 2})

with open(ROOT / "outputs/wdi_derives.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["calcul", "valeur", "n_annees"]); w.writeheader(); w.writerows(out)
for r in out: print(r)
