"""Contrôles de cohérence chiffrée des documents programmatiques soumis le 20/10/2026.

python3 cameroun/models/coherence_plan.py  ->  cameroun/outputs/coherence_plan.csv

Chaque contrôle confronte un chiffre des documents à une grandeur de référence sourcée
(identifiant du registre) ou à un autre chiffre du même document. Les ordres de grandeur
marqués « hypothèse » sont des hypothèses de calcul explicites, pas des données.
"""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

# Grandeurs de référence (Mds FCFA sauf mention)
PIB_2025 = 34_474          # ECO-02 (INS, comptes provisoires 2025)
RECETTES_INTERNES_2025 = 5_008.1   # MAC-009 (DPEB, exécution 2025)
RECETTES_PETROLIERES_2025 = 567.2  # MAC-009
RECETTES_EXTRACTIVES_2023 = 1_035.85  # ECO-17 (ITIE 2023 via presse)
EXPORTATIONS_2025 = 3_084  # ECO-03 (INS)
BUDGET_LF2026 = 8_816.4    # MAC-010
MASSE_SALARIALE_LF2026 = 1_626.2   # MAC-010
CAPACITE_INSTALLEE_MW = 2_280      # ENV022 (revue mi-parcours SND30, presse)
RIZ_IMPORT_2025_T = 869_039        # ECO-03
BLE_IMPORT_2025_T = 1_139_403      # ECO-03
POISSON_IMPORT_2025_T = 267_259    # ECO-03

rows = []


def add(doc, controle, valeur_doc, reference, calcul, verdict):
    rows.append({"document": doc, "controle": controle, "valeur_document": valeur_doc,
                 "reference": reference, "calcul": calcul, "verdict": verdict})


# Programme politique : Fonds souverain Ouandié
f = 10_000
add("Programme politique", "Dotation annuelle du Fonds Ouandié (10 000 Mds/an issus des ressources naturelles)",
    f, "PIB 2025 ECO-02 ; recettes extractives 2023 ECO-17 ; exportations 2025 ECO-03 ; budget LF2026 MAC-010",
    f"{f/PIB_2025:.0%} du PIB ; {f/RECETTES_EXTRACTIVES_2023:.1f}x les recettes extractives ; "
    f"{f/EXPORTATIONS_2025:.1f}x les exportations totales ; {f/BUDGET_LF2026:.0%} du budget 2026",
    "INFAISABLE en l'état : ordre de grandeur supérieur à l'ensemble des ressources")

# Livre : +30 % des salaires publics
s = 0.30 * MASSE_SALARIALE_LF2026
add("Livre Libéralisme solidaire", "Hausse de 30 % des salaires des agents de l'État",
    "+30 %", "Masse salariale LF2026 MAC-010 ; PIB ECO-02",
    f"≈ {s:.0f} Mds/an, soit {s/PIB_2025:.1%} du PIB et {s/RECETTES_INTERNES_2025:.1%} des recettes internes 2025",
    "Coût non financé dans le document ; incompatible avec la trajectoire du Plan stratégique")

# Livre : capacité électrique
add("Livre Libéralisme solidaire", "10 000 MW de capacité additionnelle en 7 ans (2026-2033)",
    10_000, "Capacité installée ≈2 280 MW ENV022 (presse)",
    f"{10_000/CAPACITE_INSTALLEE_MW:.1f}x la capacité actuelle ; à 2-4 M USD/MW (hypothèse de coût unitaire) : 20 à 40 Md USD",
    "Irréaliste sans démonstration de la demande, du réseau et du financement")

# Plan stratégique : recettes du scénario central vs mesures fiscales chiffrées
central = [5_950, 6_700, 7_550]
reference = [5_550, 5_750, 5_950]
gain = sum(c - r for c, r in zip(central, reference))
add("Plan stratégique", "Recettes non pétrolières supplémentaires du scénario central vs mesures fiscales chiffrées (450 Mds)",
    "Tableau macro 2027-2029", "Tableau du plan (central vs référence)",
    f"Écart cumulé central - référence = {gain} Mds sur 3 ans, contre 450 Mds de « recettes de rationalisation » dans le schéma de financement",
    f"INCOHÉRENT : ≈{gain-450} Mds de recettes non expliquées par des mesures")

# Plan : recettes 2025 vs exécution MINFI
add("Plan stratégique", "Recettes budgétaires 2025 (5 350 Mds)", 5_350,
    "Recettes internes exécutées 2025 = 5 008,1 Mds MAC-009",
    f"Écart {5_350-RECETTES_INTERNES_2025:.0f} Mds (périmètre ou dons ?)", "À réconcilier")

# Plan : riz
add("Plan stratégique", "Riz : 400 000 t en 2029 = « plus de 50 % de la consommation »", 400_000,
    "Importations 2025 = 869 039 t ECO-03",
    f"Consommation ≥ importations seules = {RIZ_IMPORT_2025_T:,} t ; 400 000 t couvriraient au plus "
    f"{400_000/(RIZ_IMPORT_2025_T+133_000):.0%} si la production actuelle ≈133 000 t (valeur implicite du plan)".replace(",", " "),
    "INCOHÉRENT : la cible de 50 % suppose une consommation ≈ 800 000 t, inférieure aux seules importations")

# Plan : bauxite
bx_t, bx_prix_usd, fx = 5e6, 45, 600
val = bx_t * bx_prix_usd * fx / 1e9
add("Plan stratégique", "Croissance de 5,5 % en 2029 « stimulée par la bauxite » (5 Mt)", "5 Mt",
    "Hypothèse : 45 USD/t FOB, 600 FCFA/USD (à remplacer par les prix contractuels)",
    f"Valeur brute ≈ {val:.0f} Mds FCFA, soit {val/PIB_2025:.1%} du PIB 2025",
    "Contribution trop faible pour expliquer l'écart de 3,3 points entre scénario central (5,5 %) et scénario de référence (2,2 %) en 2029 ; scénario central optimiste")

# Programme utilisateur : arrêt des importations alimentaires
add("Ajout demandé", "Arrêt des importations de riz, blé, poisson",
    "Arrêt", "Importations 2025 ECO-03",
    f"Riz {RIZ_IMPORT_2025_T:,} t ; blé {BLE_IMPORT_2025_T:,} t ; poisson congelé {POISSON_IMPORT_2025_T:,} t".replace(",", " "),
    "Arrêt immédiat = pénurie et hausse de prix ; substitution progressive nécessaire")

# Plan : DGD
add("Plan stratégique", "DGD : +120 Mds/an (tableau d'arbitrage) vs 6,5 % du budget ≈ 550 Mds en 2027 (fiche 6.2)",
    "120 vs 550", "DGD 2026 citée par le plan : 292,7 Mds",
    "550 - 292,7 = +257 Mds en 2027, le double du montant annoncé", "INCOHÉRENT entre deux sections du plan ; et 12 % en 2029 reste sous le plancher légal de 15 % des recettes")

out = ROOT / "outputs/coherence_plan.csv"
with open(out, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"- {r['document']} | {r['controle']}\n    {r['calcul']}\n    => {r['verdict']}")
