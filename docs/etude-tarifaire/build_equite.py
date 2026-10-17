"""Génère analyse_equite_tarifaire.xlsx : tarifs réglementés vs coûts par segment (Cameroun, Congo).

Toutes les valeurs saisies proviennent des sources citées dans la colonne « Source » ou
dans un commentaire de cellule. Les rares hypothèses (consommations illustratives, coût
appliqué faute de coût par segment) sont signalées en jaune.

Usage : python build_equite.py [chemin_sortie.xlsx]
"""
import sys

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Font, PatternFill

FONT = "Arial"
F_IN = Font(name=FONT, color="0000FF")
F_CALC = Font(name=FONT, color="000000")
F_LINK = Font(name=FONT, color="008000")
F_BOLD = Font(name=FONT, bold=True)
F_TITLE = Font(name=FONT, bold=True, size=14)
F_SEC = Font(name=FONT, bold=True, color="FFFFFF")
F_NOTE = Font(name=FONT, italic=True, color="666666", size=9)
FILL_HYP = PatternFill("solid", fgColor="FFFF00")
FILL_SEC = PatternFill("solid", fgColor="1F3864")
FILL_HEAD = PatternFill("solid", fgColor="D9E1F2")

FCFA = '#,##0.0;(#,##0.0);"-"'
FCFA0 = '#,##0;(#,##0);"-"'
MDS = '#,##0.0;(#,##0.0);"-"'
GWH = '#,##0;(#,##0);"-"'
PCT = '0.0%;(0.0%);"-"'
RATIO = '0.00"x"'

S_COS = ("ARSEL / Banque mondiale, « Cameroun – Étude des coûts du service et des tarifs de "
         "l'électricité, R4 », MRC & Phoenix, déc. 2022, "
         "http://arsel-cm.org/wp-content/uploads/2026/02/CMR-142-CoSTariff-R4-revise_dec-2022.pdf")
S_ARSEL = ("ARSEL, décision n°0096/ARSEL/DG/DCEC/SDCT du 28 mai 2012 (tarifs HT en vigueur depuis "
           "le 1er juin 2012), https://arsel-cm.org/tarifs-basse-tension/")
S_CMR_PACTE = ("Compact énergétique du Cameroun (Mission 300), annexe II, "
               "https://thedocs.worldbank.org/en/doc/230ea6e10398ad291f50a89d2d458c8f-"
               "0010012025/original/Cameroon-National-Energy-Compact-Mission-300.pdf")
S_COG_PACTE = ("Pacte national énergétique de la République du Congo (Mission 300), "
               "https://thedocs.worldbank.org/en/doc/ce91545b5a0c9e201bc7622f58b26618-"
               "0010012025/original/Congo-National-Energy-Compact-Mission-300.pdf")
S_E2C = ("Arrêté n°681 du 19 mars 1994, tel que reproduit par E2C (https://e2c.cg/node/45) et "
         "l'ancienne SNE ; page consultée via index de recherche le 17/10/2026, site E2C "
         "inaccessible (HTTP 403) : à revérifier sur le texte de l'arrêté")


def put(ws, ref, value, font=F_CALC, fmt=None, fill=None, comment=None, wrap=False):
    c = ws[ref]
    c.value = value
    c.font = font
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    if comment:
        c.comment = Comment(comment, "Analyse")
    if wrap:
        c.alignment = Alignment(wrap_text=True, vertical="top")
    return c


def section(ws, row, text, width=10):
    for col in range(1, width + 1):
        ws.cell(row=row, column=col).fill = FILL_SEC
    put(ws, f"A{row}", text, F_SEC)


def header(ws, row, labels):
    for i, h in enumerate(labels):
        c = ws.cell(row=row, column=i + 1, value=h)
        c.font = F_BOLD
        c.fill = FILL_HEAD
        c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[row].height = 45


def widths(ws, w):
    for col, v in w.items():
        ws.column_dimensions[col].width = v


def build_cmr_segments(wb):
    ws = wb.create_sheet("CMR_Segments")
    widths(ws, {"A": 34, "B": 13, "C": 13, "D": 13, "E": 13, "F": 13, "G": 14, "H": 13,
                "I": 13, "J": 60})
    put(ws, "A1", "Cameroun — tarifs réglementés et coût du service par segment", F_TITLE)
    put(ws, "A2", "Coût du service 2025 par niveau de tension (étude ARSEL, FCFA constants) ; "
        "tarifs moyens = grille ARSEL 2012 appliquée aux volumes projetés 2025 (statu quo).",
        F_NOTE)

    section(ws, 4, "1. TARIF vs COÛT PAR SEGMENT — 2025, statu quo tarifaire")
    header(ws, 5, ["Segment", "Tarif moyen (FCFA HT/kWh)", "Coût du service (FCFA/kWh)",
                   "Volumes (GWh)", "Tarif / coût", "Subvention (+) / surcharge (−) par kWh",
                   "Subvention nette (Md FCFA)", "Recettes (Md FCFA)",
                   "Part des subventions brutes", "Source"])
    rows = [
        ("BT — résidentiels", 73.8, "BT", 2620, "Tab. 29 ; coût BT unique (Tab. 25)"),
        ("BT — non résidentiels", 95.6, "BT", 814, "Tab. 29"),
        ("BT — éclairage public", 66.0, "BT", 228, "Tab. 29"),
        ("MT — moyenne industrie / tertiaire", 88.4, "MT", 1598, "Tab. 29"),
        ("HT — ALUCAM (aluminium)", 14.1, "HT", 1212,
         "Tarif 2020 (Tab. 17), supposé inchangé ; volume 2025 Tab. 20"),
        ("HT — autres grands industriels", 31.0, "HT", 755,
         "Tarif moyen 2020 (Tab. 17), supposé inchangé ; volume 2025 Tab. 20"),
    ]
    costs = {"BT": 86.5, "MT": 54.9, "HT": 51.0}
    r0 = 6
    cost_cells = {}
    r = r0
    # Coûts par tension, saisis une fois (Tab. 25)
    cost_row = r0 + len(rows) + 3
    put(ws, f"A{cost_row - 1}", "Coût unitaire du service par niveau de tension, 2025 "
        "(Tab. 25)", F_BOLD)
    for i, (lvl, v) in enumerate(costs.items()):
        put(ws, f"A{cost_row + i}", lvl)
        put(ws, f"B{cost_row + i}", v, F_IN, FCFA)
        put(ws, f"J{cost_row + i}", "Étude ARSEL, Tab. 25 (FCFA/kWh, 2025)", F_NOTE)
        cost_cells[lvl] = f"$B${cost_row + i}"
    put(ws, f"A{cost_row + 3}", "Global")
    put(ws, f"B{cost_row + 3}", 69.8, F_IN, FCFA)
    put(ws, f"J{cost_row + 3}", "Étude ARSEL, Tab. 25", F_NOTE)
    put(ws, f"A{cost_row + 4}", "Méthode d'allocation : coûts de production et de réseau "
        "répartis au prorata des ventes par tension, sans responsabilité de pointe (§5.2.2). "
        "La pointe (20 h) étant résidentielle (§3.4), le coût BT est probablement sous-estimé et "
        "les coûts MT/HT surestimés.", F_NOTE)

    seg_rows = []
    for label, tarif, lvl, vol, src in rows:
        put(ws, f"A{r}", label)
        put(ws, f"B{r}", tarif, F_IN, FCFA)
        put(ws, f"C{r}", f"={cost_cells[lvl]}", fmt=FCFA)
        put(ws, f"D{r}", vol, F_IN, GWH)
        put(ws, f"E{r}", f"=IFERROR(B{r}/C{r},0)", fmt=RATIO)
        put(ws, f"F{r}", f"=C{r}-B{r}", fmt=FCFA)
        put(ws, f"G{r}", f"=F{r}*D{r}/1000", fmt=MDS)
        put(ws, f"H{r}", f"=B{r}*D{r}/1000", fmt=MDS)
        put(ws, f"I{r}", f"=IFERROR(MAX(0,G{r})/SUMIF($G${r0}:$G${r0 + len(rows) - 1},\">0\"),0)",
            fmt=PCT)
        put(ws, f"J{r}", "Étude ARSEL : " + src, F_NOTE)
        seg_rows.append(r)
        r += 1
    put(ws, f"A{r}", "Total / moyenne", F_BOLD)
    put(ws, f"D{r}", f"=SUM(D{r0}:D{r - 1})", F_BOLD, GWH)
    put(ws, f"H{r}", f"=SUM(H{r0}:H{r - 1})", F_BOLD, MDS)
    put(ws, f"B{r}", f"=IFERROR(H{r}/D{r}*1000,0)", F_BOLD, FCFA)
    put(ws, f"G{r}", f"=SUM(G{r0}:G{r - 1})", F_BOLD, MDS)
    put(ws, f"J{r}", "Contrôle : l'étude donne 64,8 FCFA/kWh, 7 226 GWh, 468,0 Md et un déficit "
        "de 36,7 Md (Tab. 29).", F_NOTE)
    tot = r

    k = cost_row + 6
    section(ws, k, "2. QUI FINANCE QUI ? (2025, statu quo)")
    k += 1
    lines = [
        ("Subventions brutes reçues (segments sous le coût)",
         f"=SUMIF(G{r0}:G{tot - 1},\">0\")"),
        ("  dont ALUCAM", f"=MAX(0,G{seg_rows[4]})"),
        ("  dont ménages BT résidentiels", f"=MAX(0,G{seg_rows[0]})"),
        ("Surcharges payées (segments au-dessus du coût)",
         f"=-SUMIF(G{r0}:G{tot - 1},\"<0\")"),
        ("  dont MT", f"=-MIN(0,G{seg_rows[3]})"),
        ("Déficit restant (État / opérateur)", f"=G{tot}"),
        ("Part d'ALUCAM dans les subventions brutes", f"=IFERROR(B{k + 1}/B{k},0)"),
        ("Part des ménages résidentiels dans les subventions brutes",
         f"=IFERROR(B{k + 2}/B{k},0)"),
        ("Subvention par kWh : ALUCAM / ménages résidentiels",
         f"=IFERROR(F{seg_rows[4]}/F{seg_rows[0]},0)"),
    ]
    for i, (label, f) in enumerate(lines):
        put(ws, f"A{k + i}", label, F_BOLD if not label.startswith("  ") else F_CALC)
        fmt = PCT if "Part" in label else (RATIO if "par kWh" in label else MDS)
        put(ws, f"B{k + i}", f, fmt=fmt)
        put(ws, f"C{k + i}", "Md FCFA" if fmt == MDS else "", F_NOTE)

    k += len(lines) + 2
    section(ws, k, "3. CHIFFRES DU PACTE (MOYENNES SEULEMENT — AUCUN COÛT PAR SEGMENT)")
    k += 1
    pacte = [
        ("Coût moyen par kWh", 102.56, "FCFA/kWh", "Pilier I. Année et périmètre non précisés."),
        ("Tarif moyen MT/BT", 102.65, "FCFA/kWh", "Pilier V, 2025. HT/TTC non précisé."),
        ("Subventions pour la réflectivité des charges de l'opérateur", 67, "Md FCFA",
         "Pilier V, 2025 (estimation)."),
        ("Taux de recouvrement des factures", 0.72, "%", "Pilier V, exercice courant."),
        ("Pertes techniques", 0.15, "%", "Pilier V."),
        ("Pertes non techniques", 0.15, "%", "Pilier V."),
    ]
    for i, (label, v, unit, note) in enumerate(pacte):
        put(ws, f"A{k + i}", label)
        put(ws, f"B{k + i}", v, F_IN, PCT if unit == "%" else FCFA)
        put(ws, f"C{k + i}", unit, F_NOTE)
        put(ws, f"J{k + i}", "Compact Cameroun, annexe II, " + note, F_NOTE)
    put(ws, f"A{k + len(pacte)}", "Tarif moyen MT/BT / coût moyen (pacte)", F_BOLD)
    put(ws, f"B{k + len(pacte)}", f"=IFERROR(B{k + 1}/B{k},0)", F_BOLD, RATIO)
    put(ws, f"A{k + len(pacte) + 1}", "Ces moyennes (≈102,6 FCFA/kWh) ne sont pas comparables au "
        "coût de l'étude ARSEL (69,8 FCFA/kWh en monnaie constante 2022) : base monétaire, "
        "périmètre (pertes, taxes) et définition non précisés dans le pacte.", F_NOTE)
    ws.freeze_panes = "B6"
    return ws, seg_rows, cost_cells


def build_cmr_residentiel(wb, cost_bt_ref):
    ws = wb.create_sheet("CMR_Residentiel")
    widths(ws, {"A": 36, "B": 14, "C": 14, "D": 15, "E": 15, "F": 15, "G": 15, "H": 15,
                "I": 60})
    put(ws, "A1", "Cameroun — équité à l'intérieur de la basse tension", F_TITLE)
    put(ws, "A2", "Grille ARSEL 2012 (HT). ENEO applique les tranches de façon EXCLUSIVE : toute "
        "la consommation du mois est facturée au prix de la tranche atteinte (étude ARSEL "
        "§2.2.2).", F_NOTE)

    section(ws, 4, "1. GRILLE BT EN VIGUEUR vs COÛT BT")
    header(ws, 5, ["Tranche (kWh/mois)", "Borne haute (kWh)", "Tarif (FCFA HT/kWh)",
                   "Coût BT 2025 (FCFA/kWh)", "Tarif / coût", "Subvention (+) par kWh", "", "",
                   "Source"])
    put(ws, "D3", "Coût BT appliqué :", F_BOLD)
    put(ws, "E3", f"=CMR_Segments!{cost_bt_ref}", F_LINK, FCFA)
    grid = [
        ("Résidentiel 0–110", 110, 50), ("Résidentiel 111–400", 400, 79),
        ("Résidentiel 401–800", 800, 94), ("Résidentiel 801–2000", 2000, 99),
        ("Non résidentiel 0–110", 110, 84), ("Non résidentiel 111–400", 400, 92),
        ("Non résidentiel 401–1000", 1000, 99), ("Éclairage public (tarif unique)", None, 66),
    ]
    g = {}
    for i, (label, hi, tarif) in enumerate(grid):
        r = 6 + i
        put(ws, f"A{r}", label)
        if hi:
            put(ws, f"B{r}", hi, F_IN, FCFA0)
        put(ws, f"C{r}", tarif, F_IN, FCFA)
        put(ws, f"D{r}", "=$E$3", fmt=FCFA)
        put(ws, f"E{r}", f"=IFERROR(C{r}/D{r},0)", fmt=RATIO)
        put(ws, f"F{r}", f"=D{r}-C{r}", fmt=FCFA)
        put(ws, f"I{r}", S_ARSEL if i == 0 else "Idem", F_NOTE)
        g[i] = r
    put(ws, "A14", "Le coût BT est un coût moyen unique pour tous les usages BT (l'étude ne "
        "distingue pas résidentiel et non résidentiel). Révision du 1/11/2024 (alignement du "
        "prépayé, bandes 111–220 / 221–400 rapportées par la presse) non retenue : aucune "
        "décision ARSEL publiée trouvée ; l'ARSEL affiche toujours la décision de 2012.", F_NOTE)

    def price(cref):
        return (f"IF({cref}<=$B${g[0]},$C${g[0]},IF({cref}<=$B${g[1]},$C${g[1]},"
                f"IF({cref}<=$B${g[2]},$C${g[2]},$C${g[3]})))")

    section(ws, 16, "2. FACTURES RÉSIDENTIELLES 2020 PAR TRANCHE (base de facturation ENEO)")
    header(ws, 17, ["Tranche", "Nb de factures", "Volumes (MWh)", "Conso. moyenne "
                    "(kWh/facture)", "Part des factures", "Part des volumes",
                    "Subvention totale (Md FCFA)", "Part des subventions positives", "Source"])
    dist = [("0–110", 9350605, 375873, g[0]), ("111–400", 2956507, 552134, g[1]),
            ("401–800", 246664, 131980, g[2]), ("801–2000", 98582, 226917, g[3])]
    for i, (lab, nb, mwh, gr) in enumerate(dist):
        r = 18 + i
        put(ws, f"A{r}", lab)
        put(ws, f"B{r}", nb, F_IN, FCFA0)
        put(ws, f"C{r}", mwh, F_IN, FCFA0)
        put(ws, f"D{r}", f"=IFERROR(C{r}*1000/B{r},0)", fmt=FCFA)
        put(ws, f"E{r}", f"=IFERROR(B{r}/SUM($B$18:$B$21),0)", fmt=PCT)
        put(ws, f"F{r}", f"=IFERROR(C{r}/SUM($C$18:$C$21),0)", fmt=PCT)
        put(ws, f"G{r}", f"=C{r}*$F${gr}/1E6", fmt=MDS)
        put(ws, f"H{r}", f"=IFERROR(MAX(0,G{r})/SUMIF($G$18:$G$21,\">0\"),0)", fmt=PCT)
        put(ws, f"I{r}", "Étude ARSEL, Tab. 4 (2020)" if i == 0 else "Idem", F_NOTE)
    put(ws, "A22", "Total", F_BOLD)
    for col, fmt in (("B", FCFA0), ("C", FCFA0), ("G", MDS)):
        put(ws, f"{col}22", f"=SUM({col}18:{col}21)", F_BOLD, fmt)
    put(ws, "D22", "=IFERROR(C22*1000/B22,0)", F_BOLD, FCFA)
    put(ws, "A23", "Incohérence de la source : le Tab. 11 de l'étude indique 727 GWh pour la "
        "tranche > 800 kWh (contre 226,9 GWh au Tab. 4). Le Tab. 4 est retenu car cohérent avec "
        "la consommation moyenne publiée (102 kWh/mois). Volumes 2020 valorisés au coût BT "
        "2025 : ordre de grandeur, pas une comptabilité.", F_NOTE)

    section(ws, 25, "3. SUBVENTION MENSUELLE PAR FACTURE SELON LA CONSOMMATION (facturation "
            "exclusive)")
    header(ws, 26, ["Consommation (kWh/mois)", "Prix appliqué (FCFA HT/kWh)", "Facture HT "
                    "(FCFA)", "Coût de fourniture (FCFA)", "Subvention (+) / surcharge (−) "
                    "(FCFA/mois)", "Prix moyen / coût", "", "", "Repère"])
    points = [(25, "Plafond du 3e décile de factures (Tab. 5)"),
              (54, "Médiane des factures 2020 (§3.1.2.2)"),
              (102, "Consommation moyenne résidentielle 2020 (Tab. 10)"),
              (110, "Dernier kWh de la tranche sociale"),
              (111, "Premier kWh de la tranche 2 : effet de seuil"),
              (204, "Plafond du 9e décile (Tab. 5)"), (400, "Fin de tranche 2"),
              (401, "Premier kWh de la tranche 3"), (800, "Fin de tranche 3"),
              (801, "Premier kWh de la tranche 4"), (1500, "Gros consommateur")]
    for i, (c, lab) in enumerate(points):
        r = 27 + i
        put(ws, f"A{r}", c, F_IN, FCFA0)
        put(ws, f"B{r}", "=" + price(f"A{r}"), fmt=FCFA)
        put(ws, f"C{r}", f"=A{r}*B{r}", fmt=FCFA0)
        put(ws, f"D{r}", f"=A{r}*$E$3", fmt=FCFA0)
        put(ws, f"E{r}", f"=D{r}-C{r}", fmt=FCFA0)
        put(ws, f"F{r}", f"=IFERROR(B{r}/$E$3,0)", fmt=RATIO)
        put(ws, f"I{r}", lab, F_NOTE)
    put(ws, "A39", "Effet de seuil à 110→111 kWh : (facture à 111) − (facture à 110), FCFA",
        F_BOLD)
    put(ws, "E39", "=C31-C30", F_BOLD, FCFA0)

    section(ws, 41, "4. SUBVENTION PAR DÉCILE DE FACTURES (consommation moyenne du décile, 2020)")
    header(ws, 42, ["Décile de factures", "Conso. moyenne (kWh/mois)", "Prix appliqué",
                    "Subvention (FCFA/mois)", "Prix / coût", "",
                    "", "", "Source"])
    dec = [0.6, 7.5, 18.3, 30.8, 45.7, 64.2, 86.0, 114.2, 163.9, 481.8]
    for i, v in enumerate(dec):
        r = 43 + i
        put(ws, f"A{r}", f"D{i + 1}")
        put(ws, f"B{r}", v, F_IN, FCFA)
        put(ws, f"C{r}", "=" + price(f"B{r}"), fmt=FCFA)
        put(ws, f"D{r}", f"=B{r}*($E$3-C{r})", fmt=FCFA0)
        put(ws, f"E{r}", f"=IFERROR(C{r}/$E$3,0)", fmt=RATIO)
        put(ws, f"I{r}", "Étude ARSEL, Tab. 6 (2020)" if i == 0 else "Idem", F_NOTE)
    put(ws, "A53", "Limite : déciles de CONSOMMATION des abonnés raccordés, pas de revenu. La "
        "moyenne de D10 (481,8 kWh) masque des factures très hétérogènes. Les ménages non "
        "raccordés (≈37 % de la population, 77 % en rural selon l'étude) ne reçoivent rien.",
        F_NOTE)
    ws.freeze_panes = "B6"


def build_cog(wb):
    ws = wb.create_sheet("COG_Segments")
    widths(ws, {"A": 42, "B": 14, "C": 14, "D": 14, "E": 14, "F": 15, "G": 15, "H": 15,
                "I": 60})
    put(ws, "A1", "Congo — tarifs réglementés (1994) et coût du service", F_TITLE)
    put(ws, "A2", "Le pacte ne donne qu'un coût MOYEN du service ; aucun coût par segment n'est "
        "publié. Grille MT/HT et primes fixes BT non trouvées.", F_NOTE)

    section(ws, 4, "1. COÛT DU SERVICE (moyenne, pacte national énergétique)")
    put(ws, "A5", "Coût de fourniture du service")
    put(ws, "B5", 0.16, F_IN, '0.00 "USD/kWh"')
    put(ws, "I5", "Pacte Congo, p. 15 : tarifs recouvrant 56 % du coût (0,09 vs 0,16 USD/kWh).",
        F_NOTE)
    put(ws, "A6", "Tarif moyen")
    put(ws, "B6", 0.09, F_IN, '0.00 "USD/kWh"')
    put(ws, "I6", "Pacte Congo, p. 15 et annexe (« 0,091 $/kWh depuis 1994 »).", F_NOTE)
    put(ws, "A7", "Taux de change implicite du pacte (XAF par USD)")
    put(ws, "B7", "=110000/180", F_CALC, FCFA)
    put(ws, "I7", "Pacte Congo, p. 13 : frais de raccordement « 110 000 XAF (180 USD) ». "
        "Taux implicite, à remplacer par le taux de l'année de référence.", F_NOTE)
    ws["B7"].fill = FILL_HYP
    put(ws, "A8", "Coût du service en FCFA/kWh", F_BOLD)
    put(ws, "B8", "=B5*B7", F_BOLD, FCFA)
    put(ws, "A9", "Tarif moyen en FCFA/kWh")
    put(ws, "B9", "=B6*B7", fmt=FCFA)
    put(ws, "A10", "Taux de couverture du coût (pacte : 56 %)")
    put(ws, "B10", "=IFERROR(B6/B5,0)", fmt=PCT)
    put(ws, "A11", "Référence secondaire : coût moyen 94 FCFA/kWh, recette unitaire ≈48 FCFA/kWh "
        "(2016), étude ICEA-Ricardo 2017 citée par icea-consulting.com — page non consultable "
        "directement, non retenue dans les calculs.", F_NOTE)
    put(ws, "A12", "Pertes totales 45 % (2022), recouvrement 73 %, 40 % des clients facturés au "
        "forfait, accès des ménages 31 % (pacte, p. 13–15, 22).", F_NOTE)

    section(ws, 14, "2. GRILLE BASSE TENSION (arrêté n°681 du 19 mars 1994) vs COÛT MOYEN")
    header(ws, 15, ["Catégorie d'abonnement", "Tarif (FCFA/kWh)", "Coût moyen (FCFA/kWh)",
                    "Tarif / coût", "Subvention par kWh", "Conso. illustrative (kWh/mois)",
                    "Subvention mensuelle (FCFA)", "Rabais vs petit abonné", "Source"])
    rows = [("Monophasé 1,2 à 3 kW (T1–T3)", 49.08, 100),
            ("Monophasé 5 et 9 kW", 44.64, 300),
            ("Mono/triphasé ≥ 11,5 kW", 43.56, 600),
            ("Triphasé, au-delà de 900 kWh/mois", 31.20, 1200),
            ("Éclairage public (T12, + 7 272 FCFA/mois)", 43.56, None)]
    for i, (lab, t, c) in enumerate(rows):
        r = 16 + i
        put(ws, f"A{r}", lab)
        put(ws, f"B{r}", t, F_IN, FCFA)
        put(ws, f"C{r}", "=$B$8", fmt=FCFA)
        put(ws, f"D{r}", f"=IFERROR(B{r}/C{r},0)", fmt=RATIO)
        put(ws, f"E{r}", f"=C{r}-B{r}", fmt=FCFA)
        if c:
            put(ws, f"F{r}", c, F_IN, FCFA0, FILL_HYP)
            put(ws, f"G{r}", f"=F{r}*E{r}", fmt=FCFA0)
        put(ws, f"H{r}", f"=IFERROR(1-B{r}/$B$16,0)", fmt=PCT)
        put(ws, f"I{r}", S_E2C if i == 0 else "Idem", F_NOTE)
    put(ws, "A21", "Consommations illustratives (jaune) : hypothèses de l'analyse, non tirées "
        "d'une source. Primes fixes mensuelles BT (« droit à la consommation ») non trouvées : "
        "elles réduisent ou accentuent la régressivité selon leur niveau.", F_NOTE)
    put(ws, "A22", "Rapport subvention mensuelle gros abonné / petit abonné", F_BOLD)
    put(ws, "G22", "=IFERROR(G19/G16,0)", F_BOLD, RATIO)
    ws.freeze_panes = "B5"


def build_synthese(wb, seg_rows):
    ws = wb["Synthese_equite"]
    widths(ws, {"A": 48, "B": 22, "C": 22, "D": 70})
    put(ws, "A1", "Jugement d'équité tarifaire — grille de lecture", F_TITLE)
    header(ws, 3, ["Critère", "Cameroun", "Congo", "Lecture"])
    s = "CMR_Segments!"
    rows = [
        ("Couverture moyenne du coût par le tarif",
         f"=IFERROR({s}B{seg_rows[-1] + 1}/{s}B{seg_rows[-1] + 7},0)", "=COG_Segments!B10",
         "< 1 : le tarif ne couvre pas le coût ; l'écart est payé par l'État, la dette "
         "ou la dégradation du service.", RATIO),
        ("Tarif/coût — ménages résidentiels", f"={s}E{seg_rows[0]}",
         "=COG_Segments!D16", "Congo : petit abonné monophasé.", RATIO),
        ("Tarif/coût — MT (PME, tertiaire, industrie moyenne)", f"={s}E{seg_rows[3]}",
         "n.d.", "Congo : grille MT non trouvée.", RATIO),
        ("Tarif/coût — plus gros consommateur", f"={s}E{seg_rows[4]}",
         "=COG_Segments!D19", "Cameroun : ALUCAM. Congo : triphasé > 900 kWh/mois.", RATIO),
        ("Écart de traitement entre segments (max/min du ratio)",
         f"=MAX({s}E{seg_rows[0]}:E{seg_rows[-1]})/MIN({s}E{seg_rows[0]}:E{seg_rows[-1]})",
         "=MAX(COG_Segments!D16:D19)/MIN(COG_Segments!D16:D19)",
         "Plus il est élevé, plus le tarif s'éloigne du coût de manière différenciée.", RATIO),
        ("Part des subventions brutes captée par le plus gros consommateur",
         f"={s}I{seg_rows[4]}", "n.d.",
         "Cameroun : un seul client industriel (ALUCAM).", PCT),
        ("Prix au kWh : petit consommateur / gros consommateur",
         "=CMR_Residentiel!C6/CMR_Residentiel!C9", "=COG_Segments!B16/COG_Segments!B19",
         "< 1 = progressif (le petit paie moins) ; > 1 = régressif.", RATIO),
        ("Part de la subvention résidentielle allant à la tranche sociale (0–110 kWh)",
         "=CMR_Residentiel!H18", "n.d.", "Cameroun : part des subventions positives, volumes 2020, coût BT 2025.", PCT),
        ("Effet de seuil au 111e kWh (FCFA/mois)", "=CMR_Residentiel!E39", "n.d.",
         "Facture qui augmente de plus de 3 000 FCFA pour 1 kWh de plus.", FCFA0),
    ]
    for i, (lab, a, b, note, fmt) in enumerate(rows):
        r = 4 + i
        put(ws, f"A{r}", lab, wrap=True)
        put(ws, f"B{r}", a, F_LINK, fmt)
        put(ws, f"C{r}", b, F_LINK if b.startswith("=") else F_NOTE, fmt)
        put(ws, f"D{r}", note, F_NOTE, wrap=True)


def build_readme(wb):
    ws = wb.active
    ws.title = "LISEZMOI"
    ws.column_dimensions["A"].width = 130
    lines = [
        ("Analyse de l'équité tarifaire — électricité, Cameroun et Congo", F_TITLE),
        ("Objet : comparer les tarifs réglementés en vigueur au coût du service de chaque segment, "
         "puis juger l'équité (entre segments, entre petits et gros consommateurs, envers les "
         "non-raccordés).", F_CALC),
        ("", F_CALC),
        ("SOURCES", F_BOLD),
        ("• " + S_ARSEL, F_CALC), ("• " + S_COS, F_CALC), ("• " + S_CMR_PACTE, F_CALC),
        ("• " + S_COG_PACTE, F_CALC), ("• " + S_E2C, F_CALC),
        ("", F_CALC),
        ("POINT DE MÉTHODE ESSENTIEL", F_BOLD),
        ("Les deux pactes ne publient qu'un coût MOYEN, pas de coût par segment. Pour le Cameroun, "
         "le coût par niveau de tension provient de l'étude de coût de service commandée pour "
         "l'ARSEL (2022). Pour le Congo, seul le coût moyen du pacte est disponible : le jugement "
         "porte sur la structure de la grille, pas sur un coût par segment.", F_CALC),
        ("", F_CALC),
        ("CODE COULEUR", F_BOLD),
        ("Bleu : donnée saisie depuis une source. Noir : formule. Vert : lien entre feuilles. "
         "Fond jaune : hypothèse de l'analyse (pas une donnée source).", F_CALC),
    ]
    for i, (t, f) in enumerate(lines, start=1):
        put(ws, f"A{i}", t, f, wrap=True)


def main(out):
    wb = Workbook()
    build_readme(wb)
    wb.create_sheet("Synthese_equite")
    _, seg_rows, cost_cells = build_cmr_segments(wb)
    build_cmr_residentiel(wb, cost_cells["BT"])
    build_cog(wb)
    build_synthese(wb, seg_rows)
    wb.save(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "analyse_equite_tarifaire.xlsx")
