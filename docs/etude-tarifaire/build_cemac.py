"""Étend analyse_equite_tarifaire.xlsx aux autres pays de la CEMAC (Gabon, Tchad, RCA, Guinée éq.).

Reconstruit tout le classeur (feuilles Cameroun/Congo de build_equite.py) puis ajoute une feuille
par pays et une feuille de comparaison CEMAC. Chaque valeur saisie porte sa source ; les choix
d'analyse (coût de référence retenu) sont surlignés en jaune.

Usage : python build_cemac.py [chemin_sortie.xlsx]
"""
import sys

from openpyxl import Workbook

from build_equite import (F_BOLD, F_CALC, F_IN, F_LINK, F_NOTE, F_TITLE, FCFA, FILL_HYP, PCT,
                          RATIO, build_cmr_residentiel, build_cmr_segments, build_cog,
                          build_readme, build_synthese, header, put, section, widths)

URL_GAB_PACTE = ("https://mission300africa.org/wp-content/uploads/2026/06/"
                 "Gabon-National-Energy-Compact-Mission-300.pdf")
URL_SEEG = "https://www.seeg-gabon.com/med/trf/Baremes_revises_1582277696894.pdf"
URL_GAB_PAD = ("https://documents.worldbank.org/curated/en/099011626102575716/pdf/"
               "BOSIB-a852726a-9c2e-4d4e-8903-33e9705339c0.pdf")
URL_TCD_PACTE = ("https://www.worldbank.org/content/dam/theworldbankgroupasset/document/2026/"
                 "m300-energy-compacts/Chad-M300-AES-Compact.pdf")
URL_TCD_PAD = ("https://documents1.worldbank.org/curated/en/860701648216750651/pdf/"
               "Chad-Energy-Access-Scale-Up-Project.pdf")
URL_TCD_2012 = ("https://tchadoscopie.over-blog.com/article-tchad-baisse-des-tarifs-de-l-"
                "electricite-pour-lutter-contre-la-fraude-110399447.html")
URL_CAF_PACTE = ("https://mission300africa.org/wp-content/uploads/2026/06/"
                 "CAR-National-Energy-Compact-Mission-300.pdf")
URL_CAF_GRILLE = ("https://tech-action.unepccc.org/wp-content/uploads/sites/2/2022/04/"
                  "rca-rapport-ii-abcp-attenuation-version-finale.pdf")
URL_WPS7788 = "https://documents1.worldbank.org/curated/en/182071470748085038/pdf/WPS7788.pdf"
URL_CAF_ICR = ("https://documents1.worldbank.org/curated/en/099121924112038518/pdf/"
               "BOSIB1dbdb1cd801919df014221470797fa.pdf")
URL_GNQ_LOI = "https://faolex.fao.org/docs/pdf/eqg199462.pdf"
URL_WDI = "https://data.worldbank.org (WDI, EG.ELC.ACCS.ZS / .RU / .UR, mise à jour 08/10/2026)"

# Chaque pays : références de coût (libellé, valeur, unité, XAF/USD, source), index du coût
# retenu (ou None), lignes tarifaires (libellé, tarif min, tarif max, note), faits (libellé,
# valeur, format, source), et métadonnées de comparaison.
COUNTRIES = [
    {
        "sheet": "GAB", "name": "Gabon", "operator": "SEEG",
        "title": "Gabon — grille SEEG (HT) vs coût moyen du pacte",
        "basis": "Barème SEEG « valable à compter du 01/01/2020 », hors taxes ; aucun texte "
                 "réglementaire cité. Tarifs gelés par décision gouvernementale depuis octobre "
                 "2018 (pacte p.40–41).",
        "costs": [
            ("Coût moyen de revient 2024 (pacte)", 79.8, "FCFA", None,
             f"Pacte Gabon p.41 ({URL_GAB_PACTE}). Probablement partiel : le pacte dit aussi que "
             "les tarifs ne couvrent pas les coûts de service."),
            ("Coût d'exploitation des centrales au gazole (plafond)", 250, "FCFA", None,
             "Pacte Gabon p.41 (« jusqu'à 250 FCFA/kWh »)."),
        ],
        "cost_pick": 0,
        "tariffs": [
            ("BT social S1 (1 kW, ≤ 120 kWh/mois)", 52.40, 52.40, "Barème p.6"),
            ("BT social S2+ER (2 kW, ≤ 240 kWh/mois)", 84.68, 84.68, "Barème p.6"),
            ("BT général 3 kW", 111.18, 111.18, "Barème p.7"),
            ("BT général 6 kW", 117.36, 117.36, "Barème p.7"),
            ("BT général 9 kW", 122.42, 122.42, "Barème p.7"),
            ("BT général 12 kW", 126.63, 126.63, "Barème p.7"),
            ("BT général 15 kW", 129.58, 129.58, "Barème p.7"),
            ("BT ≥ 18 kW longues utilisations (+ 5 602 F/kW/mois)", 71.59, 71.59, "Barème p.7"),
            ("BT ≥ 18 kW courtes utilisations (+ 2 435 F/kW/mois)", 90.19, 90.19, "Barème p.7"),
            ("MT Libreville, hors pointe (+ 7 552 à 17 311 F/kW/mois)", 16.86, 54.98,
             "Barème p.4 ; énergie seule, prime fixe en sus"),
            ("MT Libreville, pointe", 57.72, 248.12, "Barème p.4"),
            ("HTB Libreville, hors pointe (+ 5 214 à 11 970 F/kW/mois)", 12.18, 38.42,
             "Barème p.1 ; énergie seule, prime fixe en sus"),
        ],
        "small": 0, "large": 6,
        "facts": [
            ("Prix de vente moyen 2024", 103.2, FCFA, "Pacte p.41 (FCFA/kWh)"),
            ("Recouvrement des factures (y c. État)", 0.605, PCT, "Pacte p.41"),
            ("Pertes totales (non auditées)", 0.29, PCT, "Pacte p.40 et p.51"),
            ("Part des coûts d'exploitation et maintenance (O&M) couverte (électricité, déc. 2024)",
             0.83, PCT, f"Banque mondiale, PAD PASBAP p.37 ({URL_GAB_PAD})"),
            ("Accès national (réseau + mini-réseau)", 0.927, PCT,
             "Pacte p.15 (EDSG-III 2019–21) ; jugé « optimiste » par le pacte"),
            ("Accès rural", 0.536, PCT, "Pacte p.15"),
            ("Usagers sans compteur propre (alimentés par un voisin)", 500000, "#,##0",
             "Pacte (≈ 500 000)"),
        ],
        "social": "Oui : 1 kW à 52,40 et 2 kW à 84,68 FCFA/kWh",
        "access": (0.927, 0.536), "access_src": "Pacte p.15",
        "segment_cost": "Non (pacte : coût moyen seulement)",
        "verdict": "Le plus équitable de la CEMAC entre ménages : un tarif social explicite, des "
                   "prix qui montent avec la puissance souscrite, un accès élevé. Réserves : (1) "
                   "les quelque 500 000 usagers sans compteur ne bénéficient pas du tarif social ; "
                   "(2) en heures creuses, l'énergie MT et HT coûte de 12 à 55 FCFA/kWh, sous le "
                   "tarif social (prime fixe en sus) : impossible de trancher entre segments sans "
                   "coût par tension ; (3) la couverture des coûts est incertaine (79,8 < 103,2 "
                   "selon le pacte, mais 83 % des coûts O&M couverts selon la Banque mondiale).",
    },
    {
        "sheet": "TCD", "name": "Tchad", "operator": "SNE, devenue TchadElec (2025)",
        "title": "Tchad — grille de 2012 vs coût moyen de production",
        "basis": "Arrêté du ministère du Commerce d'août 2012 (numéro non trouvé), toujours la "
                 "référence selon le pacte (p.23). Grille connue par une dépêche Xinhua reprise "
                 "par Tchadoscopie (source secondaire) ; la fourchette 85–125 FCFA/kWh est "
                 "confirmée par la Banque mondiale (PAD 2022, p.18).",
        "costs": [
            ("Coût moyen de production (pacte)", 200, "FCFA", None,
             f"Pacte Tchad p.22 ({URL_TCD_PACTE}) : « 200 FCFA / NA »"),
            ("Coût moyen de production (Banque mondiale, 2022)", 0.22, "USD", 574.4,
             f"PAD P174495 p.18 et taux p.2 (CFAF 574,4 = 1 USD) ({URL_TCD_PAD})"),
            ("Coût du kWh moyen (pacte, nature ambiguë)", 0.175, "USD", 574.4,
             "Pacte p.23 : « Cout de kWh moyen : 0,175 USD » ; taux du PAD faute de taux dans le "
             "pacte"),
        ],
        "cost_pick": 0,
        "tariffs": [
            ("BT domestique 0–150 kWh/mois", 85, 85, URL_TCD_2012),
            ("BT domestique > 150 kWh/mois", 125, 125, "Idem"),
            ("Force motrice", 125, 125, "Idem"),
            ("Éclairage public", 125, 125, "Idem"),
            ("Moyenne tension (tranche unique)", 125, 125, "Idem"),
        ],
        "small": 0, "large": 1,
        "facts": [
            ("Subventions à la SNE 2019 (en nature : combustible)", 84, '#,##0" M USD"',
             "PAD p.19 (0,8 % du PIB, ≈ 1 000 USD par client et par an)"),
            ("Accès à l'électricité (pacte)", 0.11, PCT, "Pacte p.12 (rural < 1 %, urbain 20 %)"),
            ("Accès à l'électricité (Banque mondiale)", 0.064, PCT, "PAD p.40"),
            ("Pertes ATCC", 0.39, PCT, "Pacte p.23"),
            ("Taux de recouvrement actuel", 0.51, PCT, "Pacte p.23"),
            ("Part des recettes SNE venant des 2 000 plus gros clients", 0.60, PCT,
             "PAD p.21 (« more than 60 percent »)"),
            ("Ruraux ne pouvant payer plus de 10 USD/mois", 0.70, PCT, "Pacte p.24"),
        ],
        "social": "Partiel : tranche 0–150 kWh à 85 FCFA ; gratuité ≤ 300 kWh/mois en 2024 "
                  "(circulaire, source secondaire)",
        "access": (0.11, 0.01), "access_src": "Pacte p.12 (rural « moins de 1 % »)",
        "segment_cost": "Non",
        "verdict": "Fortement inéquitable, surtout par exclusion. 6 à 11 % d'accès, et une "
                   "subvention d'environ 1 000 USD par client et par an versée à quelque 70 000 "
                   "clients, surtout urbains. La subvention par kWh (coût 200 − tarif) bénéficie "
                   "d'abord aux 2 000 plus gros clients (plus de 60 % des recettes). La grille ne "
                   "distingue pas la MT de la BT à plus de 150 kWh (125 FCFA) : rien ne reflète "
                   "les coûts par tension.",
    },
    {
        "sheet": "CAF", "name": "Centrafrique", "operator": "ENERCA",
        "title": "Centrafrique — grille ENERCA (déc. 2016, TTC) vs coût moyen",
        "basis": "Tableau « Structure tarifaire de l'électricité (Décembre 2016) », source DPED "
                 "ébauche 2017, reproduit dans le rapport ONU Environnement-CCC (2020), p.54 "
                 f"({URL_CAF_GRILLE}). Prix TVA incluse. Aucune référence réglementaire. Pacte "
                 "p.28 : « absence d'ajustement tarifaire depuis trois décennies ».",
        "costs": [
            ("Coût de fourniture (données 2014, Banque mondiale)", 0.20, "USD", 600,
             f"Kojima & Trimble, WPS7788, tab. 6 ({URL_WPS7788}) ; repris par le PAD PURACEL "
             "2022 ; taux implicite du pacte RCA (≈ 600 XAF/USD, p.10–18)"),
        ],
        "cost_pick": 0,
        "tariffs": [
            ("BT éclairage, 50 premières heures", 76.56, 76.56, "Tranche 1 (heures d'utilisation)"),
            ("BT éclairage, au-delà de 100 h", 89.31, 89.31, "Tranche 3"),
            ("BT force motrice, 65 premières heures", 64.60, 64.60, "Tranche 1"),
            ("BT force motrice, au-delà de 95 h", 75.35, 75.35, "Tranche 3"),
            ("BT mixte, 65 premières heures", 75.53, 75.53, "Tranche 1"),
            ("BT mixte, au-delà de 130 h", 88.10, 88.10, "Tranche 3"),
            ("Éclairage public", 69.92, 69.92, ""),
            ("MT actif nuit / jour (+ 2 749,50 F/kW)", 30.38, 42.30, "Énergie seule"),
            ("Centres secondaires (15 centres)", 160.84, 160.84, "Hors réseau de Bangui"),
        ],
        "small": 0, "large": 1,
        "facts": [
            ("Accès national 2024", 0.168, PCT, "Pacte RCA p.3"),
            ("Recouvrement des factures", 0.862, PCT, "Pacte p.17 (contre 67 % en 2020, PAD)"),
            ("Pertes techniques et non techniques", 0.20, PCT, "Pacte p.28 (contre > 29 %, PAD)"),
            ("Recouvrement effectif des coûts", 0.55, PCT, f"Banque mondiale, ICR 2024 ({URL_CAF_ICR})"),
            ("Branchements directs non régularisés", 21000, "#,##0", "Pacte p.28"),
            ("Créances impayées fin 2024", 52, '#,##0" Md FCFA"', "Pacte p.28"),
        ],
        "social": "Non",
        "access": (0.168, None), "access_src": "Pacte p.3",
        "segment_cost": "Non (étude 2022 non publiée)",
        "verdict": "Inéquitable. Aucune tranche sociale. La progressivité ne porte que sur les "
                   "heures d'utilisation. Les 15 centres secondaires (villes de province) paient "
                   "160,84 FCFA/kWh, soit près du double de Bangui. L'énergie MT (30 à 42 FCFA) "
                   "est bien moins chère que la BT. Accès de 16,8 % : 83 % de la population ne "
                   "reçoit rien.",
    },
    {
        "sheet": "GNQ", "name": "Guinée équatoriale", "operator": "SEGESA",
        "title": "Guinée équatoriale — loi tarifaire du 21 mai 2002 (statut actuel inconnu)",
        "basis": f"Loi du 21 mai 2002, art. 7 à 9 (numéro non lisible) ({URL_GNQ_LOI}). Elle "
                 "abroge le décret-loi n°41/1994. Aucun texte postérieur trouvé. Pas de pacte "
                 "Mission 300.",
        "costs": [],
        "cost_pick": None,
        "tariffs": [
            ("Urbain thermique 1–150 kWh/mois", 60, 60, "Art. 7"),
            ("Urbain thermique 151–250", 90, 90, "Art. 7"),
            ("Urbain thermique 251–500", 115, 115, "Art. 7"),
            ("Urbain thermique 501–2 500", 160, 160, "Art. 7"),
            ("Urbain thermique 2 501–5 000", 150, 150, "Art. 7"),
            ("Urbain thermique 5 001–25 000", 140, 140, "Art. 7"),
            ("Urbain thermique > 25 000", 120, 120, "Art. 7 (« Mayor que 2.5001 », coquille)"),
            ("Haute tension urbaine (+ 1 500 F/kW)", 100, 100, "Art. 8"),
            ("Rural, producteurs indépendants", 55, 55, "Art. 9a"),
            ("Rural, diesel", 80, 80, "Art. 9b"),
            ("Rural, hydraulique", 60, 60, "Art. 9c"),
        ],
        "small": 0, "large": 3,
        "facts": [
            ("Accès national 2024", 0.651, PCT, URL_WDI),
            ("Accès urbain 2024", 0.893, PCT, URL_WDI),
            ("Accès rural 2024", 0.051, PCT, URL_WDI),
            ("Pertes de transport et distribution 2024", 0.1066, PCT, URL_WDI),
        ],
        "social": "Tranche 1–150 kWh à 60 FCFA (loi 2002)",
        "access": (0.651, 0.051), "access_src": "WDI 2024",
        "segment_cost": "Non (aucun coût publié)",
        "verdict": "Non jugeable faute de coût et de grille à jour. Sur le papier (2002), la "
                   "grille est progressive jusqu'à 2 500 kWh/mois puis dégressive pour les très "
                   "gros consommateurs, et prévoit des prix ruraux plus bas. Mais 95 % des ruraux "
                   "n'ont pas accès au réseau.",
    },
]


def build_country(wb, c):
    ws = wb.create_sheet(c["sheet"])
    widths(ws, {"A": 52, "B": 13, "C": 11, "D": 12, "E": 14, "F": 13, "G": 13, "H": 13,
                "I": 70})
    put(ws, "A1", c["title"], F_TITLE)
    put(ws, "A2", c["basis"], F_NOTE)

    section(ws, 4, "1. RÉFÉRENCES DE COÛT (moyennes ; aucun coût par segment publié)")
    header(ws, 5, ["Référence", "Valeur", "Unité", "XAF/USD", "Coût (FCFA/kWh)", "", "", "",
                   "Source"])
    for i, (lab, v, unit, rate, src) in enumerate(c["costs"]):
        r = 6 + i
        put(ws, f"A{r}", lab)
        put(ws, f"B{r}", v, F_IN, '0.000' if unit == "USD" else FCFA)
        put(ws, f"C{r}", unit, F_NOTE)
        if rate:
            put(ws, f"D{r}", rate, F_IN, FCFA)
            put(ws, f"E{r}", f"=B{r}*D{r}", fmt=FCFA)
        else:
            put(ws, f"E{r}", f"=B{r}", fmt=FCFA)
        put(ws, f"I{r}", src, F_NOTE)
    pick_row = 10
    put(ws, f"A{pick_row}", "Coût moyen retenu pour les ratios (choix de l'analyse)", F_BOLD)
    if c["cost_pick"] is None:
        put(ws, f"E{pick_row}", None, F_CALC, FCFA, FILL_HYP)
        put(ws, f"I{pick_row}", "Aucun coût publié trouvé : ratios non calculables.", F_NOTE)
    else:
        put(ws, f"E{pick_row}", f"=E{6 + c['cost_pick']}", F_BOLD, FCFA, FILL_HYP)
        put(ws, f"I{pick_row}", "Modifiable : pointer vers une autre ligne pour tester la "
            "sensibilité.", F_NOTE)
    cost = f"$E${pick_row}"

    section(ws, 12, "2. GRILLE TARIFAIRE vs COÛT MOYEN")
    header(ws, 13, ["Catégorie / tranche", "Tarif min (FCFA/kWh)", "", "Tarif max (FCFA/kWh)",
                    "Tarif min / coût", "Tarif max / coût", "Subvention par kWh (au tarif min)",
                    "", "Note / source"])
    t0 = 14
    for i, (lab, tmin, tmax, note) in enumerate(c["tariffs"]):
        r = t0 + i
        put(ws, f"A{r}", lab)
        put(ws, f"B{r}", tmin, F_IN, FCFA)
        put(ws, f"D{r}", tmax, F_IN, FCFA)
        put(ws, f"E{r}", f'=IF({cost}="","n.d.",B{r}/{cost})', fmt=RATIO)
        put(ws, f"F{r}", f'=IF({cost}="","n.d.",D{r}/{cost})', fmt=RATIO)
        put(ws, f"G{r}", f'=IF({cost}="","n.d.",{cost}-B{r})', fmt=FCFA)
        put(ws, f"I{r}", note, F_NOTE)
    t1 = t0 + len(c["tariffs"]) - 1
    r = t1 + 1
    put(ws, f"A{r}", "Prix au kWh : petit consommateur / gros consommateur résidentiel", F_BOLD)
    put(ws, f"B{r}", f"=B{t0 + c['small']}/B{t0 + c['large']}", F_BOLD, RATIO)
    put(ws, f"I{r}", f"Rapport « {c['tariffs'][c['small']][0]} » / « "
        f"{c['tariffs'][c['large']][0]} ». < 1 = progressif.", F_NOTE)
    ratio_row = r
    put(ws, f"A{r + 1}", "Les tarifs avec prime fixe (MT, HT, BT ≥ 18 kW) sont comparés sur leur "
        "seule part énergie : leur prix moyen réel dépend du taux d'utilisation de la puissance "
        "souscrite.", F_NOTE)

    f0 = r + 3
    section(ws, f0, "3. INDICATEURS DE CONTEXTE")
    for i, (lab, v, fmt, src) in enumerate(c["facts"]):
        rr = f0 + 1 + i
        put(ws, f"A{rr}", lab)
        put(ws, f"B{rr}", v, F_IN, fmt)
        put(ws, f"I{rr}", src, F_NOTE)
    put(ws, f"A{f0 + len(c['facts']) + 2}", "Jugement", F_BOLD)
    put(ws, f"A{f0 + len(c['facts']) + 3}", c["verdict"], F_CALC, wrap=True)
    ws.merge_cells(f"A{f0 + len(c['facts']) + 3}:I{f0 + len(c['facts']) + 3}")
    ws.row_dimensions[f0 + len(c['facts']) + 3].height = 75
    ws.freeze_panes = "B6"
    return {"cost": f"{c['sheet']}!{cost}", "small": f"{c['sheet']}!$B${t0 + c['small']}",
            "large": f"{c['sheet']}!$B${t0 + c['large']}",
            "ratio": f"{c['sheet']}!$B${ratio_row}",
            "small_cost": f"{c['sheet']}!$E${t0 + c['small']}"}


def build_comparison(wb, refs):
    ws = wb.create_sheet("CEMAC_Comparaison", 1)
    widths(ws, {"A": 34, "B": 18, "C": 18, "D": 18, "E": 18, "F": 18, "G": 18})
    put(ws, "A1", "CEMAC — équité tarifaire de l'électricité, vue comparative", F_TITLE)
    put(ws, "A2", "Tous les prix en FCFA (XAF), monnaie commune. Coûts moyens de sources "
        "hétérogènes (années et périmètres différents) : comparer les ordres de grandeur, pas "
        "les décimales.", F_NOTE)
    countries = ["Cameroun", "Congo", "Gabon", "Tchad", "Centrafrique", "Guinée éq."]
    header(ws, 4, ["Indicateur"] + countries)
    by = {c["name"]: c for c in COUNTRIES}
    cmr_res, cog = "CMR_Residentiel!", "COG_Segments!"

    def link(v):
        return "=" + v

    rows = [
        ("Opérateur", ["ENEO", "E2C", "SEEG", by["Tchad"]["operator"], "ENERCA", "SEGESA"],
         None),
        ("Texte tarifaire de référence",
         ["ARSEL, décision 0096 (2012)", "Arrêté 681 (1994)", "Barème SEEG (2020), gel 2018",
          "Arrêté de 2012", "Grille déc. 2016", "Loi du 21/05/2002"], None),
        ("Tarif du plus petit consommateur résidentiel (FCFA/kWh)",
         [link(f"{cmr_res}C6"), link(f"{cog}B16"), link(refs["GAB"]["small"]),
          link(refs["TCD"]["small"]), link(refs["CAF"]["small"]), link(refs["GNQ"]["small"])],
         FCFA),
        ("Tarif du gros consommateur résidentiel (FCFA/kWh)",
         [link(f"{cmr_res}C9"), link(f"{cog}B19"), link(refs["GAB"]["large"]),
          link(refs["TCD"]["large"]), link(refs["CAF"]["large"]), link(refs["GNQ"]["large"])],
         FCFA),
        ("Petit / gros (< 1 = progressif ; > 1 = régressif)",
         [f"={cmr_res}C6/{cmr_res}C9", f"={cog}B16/{cog}B19", link(refs["GAB"]["ratio"]),
          link(refs["TCD"]["ratio"]), link(refs["CAF"]["ratio"]), link(refs["GNQ"]["ratio"])],
         RATIO),
        ("Coût moyen de référence (FCFA/kWh)",
         ["=CMR_Segments!B18", f"={cog}B8", link(refs["GAB"]["cost"]),
          link(refs["TCD"]["cost"]), link(refs["CAF"]["cost"]), "n.d."], FCFA),
        ("Nature du coût de référence",
         ["Coût du service 2025 (étude ARSEL)", "Coût du service (pacte)",
          "Coût de revient 2024 (pacte, partiel ?)", "Coût de production (pacte)",
          "Coût de fourniture 2014 (Banque mondiale)", "—"], None),
        ("Tarif du petit consommateur / coût moyen",
         [f"={cmr_res}C6/CMR_Segments!B18", f"={cog}D16", link(refs["GAB"]["small_cost"]),
          link(refs["TCD"]["small_cost"]), link(refs["CAF"]["small_cost"]), "n.d."], RATIO),
        ("Tranche ou tarif social explicite",
         ["Oui (≤ 110 kWh, 50 FCFA)", "Non", by["Gabon"]["social"], by["Tchad"]["social"],
          "Non", by["Guinée équatoriale"]["social"]], None),
        ("Accès national", [0.63, 0.31, 0.927, 0.11, 0.168, 0.651], PCT),
        ("Accès rural", [0.23, None, 0.536, 0.01, None, 0.051], PCT),
        ("Source de l'accès",
         ["Étude ARSEL 2022 (§1.1)", "Pacte Congo p.13 (ménages)", "Pacte p.15", "Pacte p.12",
          "Pacte p.3", "WDI 2024"], None),
        ("Coût par segment publié ?",
         ["Oui (par tension, étude ARSEL)", "Non", "Non", "Non", "Non (étude 2022 non publiée)",
          "Non"], None),
        ("Jugement d'équité",
         ["Équitable entre ménages raccordés ; inéquitable entre segments (ALUCAM, MT)",
          "Inéquitable (régressif, sans tarif social)",
          "Relativement équitable entre ménages ; inconnu entre segments",
          "Fortement inéquitable (exclusion)", "Inéquitable (sans tarif social, écart "
          "Bangui / province)", "Non jugeable (données de 2002)"], None),
    ]
    for i, (lab, vals, fmt) in enumerate(rows):
        r = 5 + i
        put(ws, f"A{r}", lab, F_BOLD, wrap=True)
        for j, v in enumerate(vals):
            col = chr(ord("B") + j)
            is_formula = isinstance(v, str) and v.startswith("=")
            font = F_LINK if is_formula else (F_IN if isinstance(v, (int, float)) else F_CALC)
            put(ws, f"{col}{r}", v, font, fmt if (is_formula or isinstance(v, (int, float)))
                else None, wrap=not is_formula)
    for r in range(5, 5 + len(rows)):
        ws.row_dimensions[r].height = 48
    ws.row_dimensions[5 + len(rows) - 1].height = 80
    n = 5 + len(rows) + 1
    put(ws, f"A{n}", "Accès Cameroun : chiffre de l'étude ARSEL (63 %, rural 23 %). Accès Congo : "
        "part des ménages (31 %), le chiffre de population diffère. Accès Tchad : 11 % (pacte) "
        "contre 6,4 % (Banque mondiale 2022). Tarifs RCA TTC, les autres HT. Cameroun : coût "
        "moyen global (69,8) retenu pour la comparabilité ; rapporté au coût BT (86,5), le ratio "
        "du petit consommateur est 0,58.", F_NOTE)
    ws.freeze_panes = "B5"


def main(out):
    wb = Workbook()
    build_readme(wb)
    wb.create_sheet("Synthese_equite")
    _, seg_rows, cost_cells = build_cmr_segments(wb)
    build_cmr_residentiel(wb, cost_cells["BT"])
    build_cog(wb)
    build_synthese(wb, seg_rows)
    refs = {c["sheet"]: build_country(wb, c) for c in COUNTRIES}
    build_comparison(wb, refs)
    ws = wb["LISEZMOI"]
    r = ws.max_row + 2
    put(ws, f"A{r}", "EXTENSION CEMAC", F_BOLD)
    put(ws, f"A{r + 1}", "Feuilles GAB, TCD, CAF, GNQ et CEMAC_Comparaison : grilles en vigueur "
        "rapportées au seul coût MOYEN disponible (aucun pays ne publie de coût par segment, "
        "sauf le Cameroun). Sources en colonne I de chaque feuille.", F_CALC, wrap=True)
    wb.save(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "analyse_equite_tarifaire.xlsx")
