"""Cadre financier du programme 2027-2029 : impact budgétaire net des 8 chantiers et financement.

python3 cameroun/models/cadre_financier_2027_2029.py
Sorties : cameroun/outputs/cadre_financier_2027_2029.csv (détail par mesure et scénario)
          cameroun/outputs/cadre_financier_synthese.csv  (soldes et besoin de financement)

Périmètre et limites
- Le modèle chiffre l'effet INCRÉMENTAL du programme par rapport au budget tendanciel. Ce n'est pas
  un TOFE complet : il ne remplace pas le cadrage macro-budgétaire du MINFI ni l'AVD FMI-BM.
- Toutes les valeurs sont des HYPOTHÈSES DE TRAVAIL (Mds FCFA courants), sourcées quand une base
  existe (identifiant du registre) et à recalibrer dès réception des données manquantes.
- Convention de signe : positif = amélioration du solde budgétaire (économie ou recette) ;
  négatif = dépense nouvelle.
- Chaque économie n'est comptée qu'une fois, dans le solde. Le financement n'enregistre que
  des ressources de financement (appuis budgétaires, emprunts, titrisation) : jamais une économie.
- Exclus du scénario central (aucune recette inscrite) : avoirs recouvrés à l'étranger, recettes de
  la bauxite avant la première exportation, monnaie nationale, Fonds souverain.
"""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
ANNEES = [2027, 2028, 2029]

# PIB nominal : INS 2025 (34 474 Mds, ECO-02) prolongé par une croissance nominale hypothétique.
PIB_2025 = 34_474
CROISSANCE_NOMINALE = {"central": 0.068, "defavorable": 0.050, "favorable": 0.085}


def pib(scenario):
    g = CROISSANCE_NOMINALE[scenario]
    out, v = {}, PIB_2025 * (1 + g)  # 2026
    for a in ANNEES:
        v *= 1 + g
        out[a] = v
    return out


# Subvention carburants tendancielle (sans réforme) : rythme de 2026 ≈ 48 Mds/mois en moyenne
# (VPL-03, ministre des Finances), soit ≈ 576 Mds/an ; varie avec le prix du pétrole.
SUBV_TENDANCIELLE = {"central": 576, "defavorable": 720, "favorable": 400}
PART_SUPPRIMEE = {"central": [0.35, 0.75, 1.00], "defavorable": [0.20, 0.50, 0.75], "favorable": [0.50, 0.90, 1.00]}

# Mesures : (chantier, libellé, {scenario: [2027, 2028, 2029]}, base / source)
MESURES = [
    (2, "Économie sur les subventions carburants",
     None, "Rythme 2026 ≈ 48 Mds/mois (VPL-03) × part supprimée par paliers trimestriels"),
    (2, "Transferts monétaires ciblés (25 000 FCFA/mois/ménage)",
     {"central": [-45, -75, -90], "defavorable": [-45, -75, -90], "favorable": [-45, -75, -90]},
     "150 000 → 250 000 → 300 000 ménages ; montant unitaire du Plan stratégique"),
    (2, "Tarif transporteur et compensation transport public",
     {"central": [-30, -20, -10], "defavorable": [-40, -30, -20], "favorable": [-25, -15, 0]},
     "Hypothèse ; à calibrer avec les syndicats et la CSPH"),
    (3, "Réduction du soutien budgétaire au secteur électrique (tarif, pertes, recouvrement)",
     {"central": [0, 40, 80], "defavorable": [0, 20, 40], "favorable": [20, 60, 120]},
     "Tarif ≈80 % du coût, 83,46 vs 105,46 FCFA/kWh (VFF-015) ; montant du soutien actuel à confirmer"),
    (3, "Tarif social pour les petites consommations d'électricité",
     {"central": [-15, -20, -20], "defavorable": [-15, -20, -20], "favorable": [-10, -15, -15]},
     "Hypothèse : protection des ménages sous un seuil de consommation"),
    (4, "Audits, appels à candidatures, cellule de recouvrement des avoirs",
     {"central": [-8, -6, -6], "defavorable": [-8, -6, -6], "favorable": [-8, -6, -6]},
     "Hypothèse de coût de fonctionnement"),
    (4, "Fin des subventions d'exploitation sans contrepartie aux entreprises publiques",
     {"central": [30, 80, 120], "defavorable": [10, 40, 60], "favorable": [50, 100, 120]},
     "Plan stratégique : 120 Mds/an à terme (non vérifié) ; montée progressive"),
    (5, "Rationalisation des dépenses fiscales (loi de 2013, TVA)",
     {"central": [80, 150, 200], "defavorable": [40, 80, 120], "favorable": [100, 200, 250]},
     "Plan : 200-250 Mds/an de dépenses fiscales (non vérifié) ; MAC-009 Tab. 11 partiel"),
    (5, "Administration fiscale numérique, cadastre, foncier (en % du PIB)",
     {"central": [0.001, 0.002, 0.003], "defavorable": [0.0, 0.001, 0.0015], "favorable": [0.0015, 0.003, 0.005]},
     "Gain en points de PIB ; hypothèse"),
    (6, "Investissements souveraineté alimentaire (riz, poisson, maïs)",
     {"central": [-40, -60, -60], "defavorable": [-30, -40, -40], "favorable": [-50, -70, -70]},
     "Hypothèse ; redéploiement partiel du PIISAH (ECO-25)"),
    (7, "Apurement de la dette due aux enseignants",
     {"central": [-40, -35, -30], "defavorable": [-40, -35, -30], "favorable": [-40, -35, -30]},
     "105 Mds restants en juin 2023 selon l'État (VPL-22), à actualiser"),
    (7, "Accises dédiées à la CSU (tabac, alcool, boissons sucrées)",
     {"central": [40, 60, 70], "defavorable": [25, 40, 50], "favorable": [50, 70, 90]},
     "Hypothèse ; recette affectée"),
    (7, "Dépenses CSU (gratuité maternelle et infantile, paiement des formations sanitaires)",
     {"central": [-40, -60, -70], "defavorable": [-40, -60, -70], "favorable": [-40, -60, -70]},
     "Égales aux accises dédiées en central (neutralité) ; en défavorable, l'écart pèse sur le solde"),
    (8, "Hausse nette de la DGD (au-delà des transferts de crédits sectoriels)",
     {"central": [-50, -100, -150], "defavorable": [-30, -60, -90], "favorable": [-60, -120, -180]},
     "Trajectoire vers le plancher légal ; DGD 2024 = 127,5 Mds selon la Chambre des comptes (GOV-025)"),
    (8, "Reconstruction NO/SO et Extrême-Nord (part budget national)",
     {"central": [-60, -80, -80], "defavorable": [-50, -60, -60], "favorable": [-60, -90, -100]},
     "Hypothèse ; s'ajoute aux financements des partenaires"),
    (8, "Statistique (exploitation RGPH4, enquête emploi, ECAM6) et mémoire nationale",
     {"central": [-12, -10, -8], "defavorable": [-12, -10, -8], "favorable": [-12, -10, -8]},
     "Hypothèse"),
]

# Financement (ressources de trésorerie, pas des économies)
FINANCEMENT = [
    ("Appuis budgétaires FMI, Banque mondiale, BAD", {"central": [300, 300, 300], "defavorable": [0, 0, 0],
     "favorable": [450, 450, 450]}, "DPEB 2027-2029 : 300 Mds en 2027 conditionnés à un programme (MAC-009)"),
    ("Titrisation d'arriérés certifiés (opération de trésorerie)", {"central": [150, 150, 0],
     "defavorable": [100, 100, 0], "favorable": [200, 100, 0]},
     "Les RAP de plus de 3 mois sont déjà dans l'encours de la dette (MAC-009) : effet neutre sur la dette"),
]
# Emplois de trésorerie hors solde : paiement cash des arriérés certifiés
APUREMENT_CASH = {"central": [150, 150, 150], "defavorable": [100, 100, 100], "favorable": [200, 200, 150]}


def main():
    detail, synth = [], []
    for sc in ["central", "defavorable", "favorable"]:
        p = pib(sc)
        totaux = {a: 0.0 for a in ANNEES}
        for ch, lib, vals, base in MESURES:
            if vals is None:  # carburants
                v = [SUBV_TENDANCIELLE[sc] * s for s in PART_SUPPRIMEE[sc]]
            elif "en % du PIB" in lib:
                v = [vals[sc][i] * p[a] for i, a in enumerate(ANNEES)]
            else:
                v = vals[sc]
            for i, a in enumerate(ANNEES):
                totaux[a] += v[i]
            detail.append({"scenario": sc, "chantier": ch, "mesure": lib,
                           **{str(a): round(v[i]) for i, a in enumerate(ANNEES)}, "base": base})
        fin = {a: 0.0 for a in ANNEES}
        for lib, vals, base in FINANCEMENT:
            for i, a in enumerate(ANNEES):
                fin[a] += vals[sc][i]
            detail.append({"scenario": sc, "chantier": "F", "mesure": lib,
                           **{str(a): vals[sc][i] for i, a in enumerate(ANNEES)}, "base": base})
        for i, a in enumerate(ANNEES):
            besoin = -totaux[a] + APUREMENT_CASH[sc][i]  # besoin de trésorerie créé par le programme
            synth.append({"scenario": sc, "annee": a, "pib_nominal_hyp": round(p[a]),
                          "effet_net_programme_sur_solde": round(totaux[a]),
                          "effet_en_pct_pib": round(100 * totaux[a] / p[a], 2),
                          "apurement_cash_arrieres": APUREMENT_CASH[sc][i],
                          "ressources_de_financement": round(fin[a]),
                          "solde_tresorerie_programme": round(fin[a] - besoin)})
    with open(ROOT / "outputs/cadre_financier_2027_2029.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(detail[0].keys()))
        w.writeheader(); w.writerows(detail)
    with open(ROOT / "outputs/cadre_financier_synthese.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(synth[0].keys()))
        w.writeheader(); w.writerows(synth)
    for r in synth:
        print(r)


if __name__ == "__main__":
    main()
