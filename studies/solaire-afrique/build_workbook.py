"""Génère etude_solaire_afrique.xlsx : gabarit de base de données (volets A, B, C),
journal des observations sourcées, registre des sources et modèle LCOE en formules Excel.

Seules les valeurs vérifiées dans une source citée sont saisies ; tout le reste est vide.
    python build_workbook.py
"""

from __future__ import annotations

import json
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = Path(__file__).with_name("etude_solaire_afrique.xlsx")
AS_OF = "2026-10-17"

HEAD = Font(bold=True, color="FFFFFF")
HEAD_FILL = PatternFill("solid", fgColor="1F4E79")
INPUT_FILL = PatternFill("solid", fgColor="FFF2CC")
NOTE = Font(italic=True, color="595959")

STATUTS = ["en service", "en construction", "attribué", "annoncé", "à vérifier", "abandonné"]
TYPES_DONNEE = ["observée", "déclarée", "modélisée", "non disponible"]
FIABILITE = ["A - document primaire", "B - institution/développeur", "C - presse spécialisée",
             "D - source secondaire non recoupée"]

PAYS = [
    ("Afrique du Nord", "MAR", "Maroc"), ("Afrique du Nord", "EGY", "Égypte"),
    ("Afrique du Nord", "TUN", "Tunisie"), ("Afrique du Nord", "DZA", "Algérie"),
    ("Afrique du Nord", "MRT", "Mauritanie"),
    ("Afrique de l'Ouest", "SEN", "Sénégal"), ("Afrique de l'Ouest", "CIV", "Côte d'Ivoire"),
    ("Afrique de l'Ouest", "GHA", "Ghana"), ("Afrique de l'Ouest", "BFA", "Burkina Faso"),
    ("Afrique de l'Ouest", "MLI", "Mali"), ("Afrique de l'Ouest", "NER", "Niger"),
    ("Afrique centrale", "CMR", "Cameroun"), ("Afrique centrale", "COG", "Congo"),
    ("Afrique centrale", "TCD", "Tchad"), ("Afrique centrale", "GAB", "Gabon"),
    ("Afrique centrale", "COD", "RDC"),
    ("Afrique de l'Est", "KEN", "Kenya"), ("Afrique de l'Est", "ETH", "Éthiopie"),
    ("Afrique de l'Est", "UGA", "Ouganda"), ("Afrique de l'Est", "RWA", "Rwanda"),
    ("Afrique de l'Est", "TZA", "Tanzanie"),
    ("Afrique australe", "ZAF", "Afrique du Sud"), ("Afrique australe", "ZMB", "Zambie"),
    ("Afrique australe", "NAM", "Namibie"), ("Afrique australe", "ZWE", "Zimbabwe"),
]

# (champ, unité, description) — communs puis spécifiques à chaque volet.
COMMUNS = [
    ("projet_id", "", "Identifiant unique (ex. A-ZMB-001)"),
    ("pays_iso3", "", "Code ISO 3166-1 alpha-3"),
    ("nom", "", "Nom de la centrale"),
    ("localisation", "", "Ville / région / coordonnées"),
    ("developpeur", "", "Développeur ou sponsor principal"),
    ("statut", "", "Voir liste : " + ", ".join(STATUTS)),
    ("annee_attribution", "année", ""),
    ("annee_mise_en_service", "année", "Date de mise en service commerciale (COD)"),
    ("puissance_mwp", "MWp", "Puissance crête DC"),
    ("puissance_mwac", "MWac", "Puissance AC (onduleurs / point d'injection)"),
    ("stockage_mwh", "MWh", "Capacité utile de stockage (0 si aucune)"),
    ("technologie", "", "Modules, onduleurs, fixe / tracker"),
    ("capex_total", "devise d'origine", "Investissement total"),
    ("capex_devise", "ISO 4217", "Devise du CAPEX"),
    ("capex_annee_prix", "année", "Année de valeur du CAPEX"),
    ("capex_usd_kwp", "USD/kWp", "Calculé, USD courants"),
    ("capex_usd_kwac", "USD/kWac", "Calculé, USD courants"),
    ("production_gwh_an", "GWh/an", "Production annuelle (préciser P50 attendue ou mesurée)"),
    ("facteur_charge_ac", "%", "Production / (MWac x 8 760 h)"),
    ("opex_usd_kw_an", "USD/kW/an", ""),
    ("dette_part", "%", "Part de la dette dans le financement"),
    ("dette_taux", "%", "Taux d'intérêt (ou marge + référence)"),
    ("dette_duree", "années", ""),
    ("wacc", "%", "Observé ou modélisé (préciser)"),
    ("tarif", "devise/kWh", "Tarif contractuel année 1"),
    ("tarif_devise", "ISO 4217", ""),
    ("tarif_indexation", "", "Fixe, indexé inflation, part indexée, etc."),
    ("ppa_duree", "années", ""),
    ("procedure", "", "Appel d'offres concurrentiel, FiT, négociation directe, EPC public"),
    ("garanties", "", "Garantie souveraine, IDA/MIGA, lettre de crédit, etc."),
    ("lcoe_usd_mwh", "USD/MWh", "Calculé par le modèle (jamais saisi comme observé)"),
    ("sources", "", "Identifiants du registre Sources, séparés par ;"),
    ("fiabilite_globale", "", "Voir liste"),
    ("notes", "", "Contradictions entre sources, hypothèses"),
]
SPEC_A = [
    ("acheteur", "", "Compagnie nationale ou acheteur"),
    ("raccordement_inclus_capex", "oui/non/inconnu", "Le CAPEX inclut-il ligne et poste ?"),
]
SPEC_B = [
    ("secteur", "", "Mines, forêt, agro-industrie, ciment, ZES, etc."),
    ("modele_commercial", "", "Autoproduction, leasing, PPA privé, ESCO"),
    ("cout_diesel_evite_usd_mwh", "USD/MWh", ""),
    ("taux_couverture_solaire", "%", "Part de la consommation couverte par le solaire"),
    ("tri_projet", "%", ""),
]
SPEC_C = [
    ("nb_clients", "", "Raccordements actifs"),
    ("conso_moyenne_kwh_client_mois", "kWh/mois", ""),
    ("cout_distribution_usd", "USD", "Réseau BT, branchements, compteurs"),
    ("tarif_client", "devise/kWh", "Ou forfait, préciser"),
    ("subvention_usd", "USD", "Subvention d'investissement ou par branchement"),
    ("operateur", "", "Privé, public, communautaire"),
    ("client_ancrage", "oui/non", ""),
]

SOURCES = [
    ("S01", "IRENA", "Renewable Power Generation Costs in 2024 — Summary", 2025,
     "https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2025/Jul/IRENA_TEC_RPGC_in_2024_Summary_2025.pdf",
     "A", "WACC supposé 3,8 % (Europe) à 12 % (Afrique) ; LCOE solaire mondial 0,043 USD/kWh"),
    ("S02", "pv magazine", "Global average solar LCOE stood at $0.043/kWh in 2024, says IRENA", 2025,
     "https://www.pv-magazine.com/2025/07/23/global-average-solar-lcoe-stood-at-0-043-kwh-in-2024-says-irena/",
     "C", "Coût d'installation moyen Afrique 2024 : 1 093 USD/kW (cite IRENA)"),
    ("S03", "Banque mondiale", "Unlocking low-cost, large-scale solar power in Zambia", 2019,
     "https://www.worldbank.org/en/news/feature/2019/05/14/unlocking-low-cost-large-scale-solar-power-in-zambia",
     "B", "Bangweulu 54 MW selon cette source"),
    ("S04", "pv-tech", "IFC Zambia solar auction sees record-low 6¢ price benchmark", 2016,
     "https://www.pv-tech.org/news/ifc-zambia-solar-auction-sees-record-low-6-price-benchmark",
     "C", "Tarifs 6,015 et 7,84 USc/kWh"),
    ("S05", "BloombergNEF Climatescope", "Zambia market profile", 2022,
     "https://2022.global-climatescope.org/markets/zm/",
     "C", "Ngonye 34 MW, Bangweulu 56 MW, mise en service 2019"),
    ("S06", "IFC", "Senegal Scaling Solar PPP brief", 2021,
     "https://www.ifc.org/content/dam/ifc/doc/2021/2021-senegal-scaling-solar-ppp-brief.pdf",
     "B", "Kahone 3,80 et Kael 3,98 c EUR/kWh, appel d'offres avril 2018"),
    ("S07", "IFC", "Scaling Solar: two PV plants bring clean energy to more than 500,000 in Senegal", 2021,
     "https://www.ifc.org/en/pressroom/2021/scaling-solar-two-pv-plants-bring-clean-energy-to-more-than-500000-in-senegal",
     "B", "Mise en service mai 2021, 60 MWac au total, Engie/Meridiam/FONSIS"),
    ("S08", "Mining Weekly", "B2Gold approves $38m hybrid energy project for Mali mine", 2019,
     "https://www.miningweekly.com/article/b2gold-approves-3m-hybrid-energy-project-for-mali-mine-2019-10-14",
     "C", "Fekola : budget approuvé 38 M USD ; 13,1 Ml de fioul lourd évités par an (prévision)"),
    ("S09", "Africa Energy Portal", "Malian gold mine powered by 30 MW/15.4 MWh solar-plus-storage", None,
     "https://africa-energy-portal.org/news/malian-gold-mine-powered-30-mw154-mwh-solar-plus-storage",
     "C", "Fekola : 30 MW / 15,4 MWh construits (13,5 MWh annoncés initialement)"),
    ("S10", "Mining Weekly", "Kinross makes $55m solar investment at Tasiast", 2022,
     "https://www.miningweekly.com/article/kinross-makes-55m-solar-investment-at-tasiast-2022-02-17",
     "C", "Tasiast : 55 M USD, 34 MW PV, batterie 18 MW, ~20 % des besoins du site"),
    ("S11", "Engineering News", "Tasiast solar project, Mauritania – update", 2024,
     "https://www.engineeringnews.co.za/article/tasiastsolar-project-mauritania-update-2024-02-23",
     "C", "Premier courant solaire en décembre 2023 ; mise en service batterie/EMS début 2024"),
    ("S12", "Afrik 21", "DRC: Nuru connects 1.3 MW solar off-grid hybrid in Goma", 2020,
     "https://afrik21.africa/en/drc-nuru-connects-1-3-mw-solar-off-grid-hybrid-in-goma",
     "C", "Goma (Ndosho) : 1,3 MW, batteries, ~364 kW de groupes de secours, inauguré le 4 février 2020"),
    ("S13", "BloombergNEF / SEforALL", "State of the Global Mini-grids Market Report 2020", 2020,
     "https://about.bnef.com/insights/clean-energy/solar-mini-grids-set-to-play-critical-role-in-achieving-universal-electricity-access-with-right-policy-support/",
     "B", "LCOE des mini-réseaux solaires hybrides isolés : 0,49 à 0,68 USD/kWh (6 pays étudiés)"),
    ("S14", "ESMAP / Banque mondiale", "Mini Grids for Half a Billion People (2019)", 2019,
     "https://www1.villanova.edu/content/dam/villanova/engineering/energy-workshop/ESMAP%20Mini%20Grids%20-%20Executive%20Summary.pdf",
     "B", "Objectif : 0,20 USD/kWh pour les mini-réseaux solaires hybrides d'ici 2030 (projection)"),
    ("S15", "IRENA", "Renewable Power Generation Costs in 2024 (rapport complet)", 2025,
     "https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2025/Jul/IRENA_TEC_RPGC_in_2024_2025.pdf",
     "A", "Afrique PV : LCOE 0,074 (2024) / 0,225 (2015) USD2024/kWh, Table 3.3 p. 106 ; "
          "coût d'installation 1 093 (2024) / 3 437 (2015) USD2024/kW, Table 3.1 p. 95 ; WACC PV 12 %, fig. 1.13 p. 41"),
    ("S16", "IRENA", "Renewable Power Generation Costs in 2025 (rapport complet)", 2026,
     "https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2026/Jul/IRENA_TEC_RPGC_in_2025_2026.pdf",
     "A", "Afrique PV : coût d'installation 837 (2025) / 3 520 (2015) USD2025/kW, Table 3.1 p. 62 ; "
          "LCOE 52 (2025) / 222 (2015) USD2025/MWh, Table 3.2 p. 71"),
]

# Observations vérifiées : (projet_id, champ, valeur, unité, type, source, note)
OBSERVATIONS = [
    ("A-ZMB-001", "tarif", 0.06015, "USD/kWh", "observée", "S04", "Tarif fixe 25 ans (Neoen/First Solar)"),
    ("A-ZMB-001", "puissance_mwac", 54, "MW", "déclarée", "S03", "S05 indique 56 MW : à réconcilier"),
    ("A-ZMB-001", "annee_mise_en_service", 2019, "année", "déclarée", "S05", ""),
    ("A-ZMB-002", "tarif", 0.0784, "USD/kWh", "observée", "S04", "Enel"),
    ("A-ZMB-002", "puissance_mwac", 34, "MW", "déclarée", "S05", "AC ou DC non précisé"),
    ("A-ZMB-002", "annee_mise_en_service", 2019, "année", "déclarée", "S05", ""),
    ("A-SEN-001", "tarif", 0.0398, "EUR/kWh", "observée", "S06", "Engie/Meridiam/FONSIS"),
    ("A-SEN-001", "annee_mise_en_service", 2021, "année", "déclarée", "S07", ""),
    ("A-SEN-002", "tarif", 0.0380, "EUR/kWh", "observée", "S06", ""),
    ("A-SEN-002", "annee_mise_en_service", 2021, "année", "déclarée", "S07", ""),
    ("B-MLI-001", "puissance_mwp", 30, "MW", "déclarée", "S09", "DC/AC non précisé ; extension à 52 MW annoncée (phase II)"),
    ("B-MLI-001", "stockage_mwh", 15.4, "MWh", "déclarée", "S09", "13,5 MWh dans l'annonce de 2019 (S08)"),
    ("B-MLI-001", "capex_total", 38e6, "USD", "déclarée", "S08", "Budget approuvé en 2019, pas le coût final"),
    ("B-MLI-001", "fioul_evite", 13.1e6, "l/an", "déclarée", "S08", "Prévision ; ~13 Ml rapportés pour 2024 par la presse"),
    ("B-MRT-001", "puissance_mwp", 34, "MW", "déclarée", "S10", "DC/AC non précisé"),
    ("B-MRT-001", "batterie_mw", 18, "MW", "déclarée", "S10", "Puissance de la batterie, pas son énergie (MWh inconnus)"),
    ("B-MRT-001", "capex_total", 55e6, "USD", "déclarée", "S10", "Annonce de 2022, pas le coût final"),
    ("B-MRT-001", "annee_mise_en_service", 2023, "année", "déclarée", "S11", "Premier courant solaire déc. 2023"),
    ("C-COD-001", "puissance_mwp", 1.3, "MW", "déclarée", "S12", "DC/AC non précisé"),
    ("C-COD-001", "annee_mise_en_service", 2020, "année", "déclarée", "S12", "Inauguration le 4 février 2020"),
]

# Projets de la proposition. Les chiffres ne sont saisis qu'après vérification (onglet Observations).
PROJETS_A = [
    ("A-ZMB-001", "ZMB", "Bangweulu (Scaling Solar)", "Neoen / First Solar", "en service",
     2016, 2019, None, 54, 0.06015, "USD", "Appel d'offres concurrentiel", "S03;S04;S05",
     "Capacité 54 MW (S03) vs 56 MW (S05)"),
    ("A-ZMB-002", "ZMB", "Ngonye (Scaling Solar)", "Enel", "en service",
     2016, 2019, None, 34, 0.0784, "USD", "Appel d'offres concurrentiel", "S04;S05", ""),
    ("A-SEN-001", "SEN", "Kael (Scaling Solar)", "Engie / Meridiam / FONSIS", "en service",
     2018, 2021, None, None, 0.0398, "EUR", "Appel d'offres concurrentiel", "S06;S07",
     "Une source (AE-Africa) place ce tarif à Touba : erreur probable"),
    ("A-SEN-002", "SEN", "Kahone (Scaling Solar)", "Engie / Meridiam / FONSIS", "en service",
     2018, 2021, None, None, 0.0380, "EUR", "Appel d'offres concurrentiel", "S06;S07",
     "Kael + Kahone = 60 MWac au total (S07)"),
    ("A-EGY-001", "EGY", "Benban Solar Park (32 centrales)", "Multiples", "à vérifier",
     None, None, None, None, None, None, "Tarif d'achat garanti (FiT) rounds 1 et 2", "",
     "1 465 MW et ~1,9 Md USD selon presse égyptienne ; tarif round 2 non vérifié. "
     "À éclater en une ligne par centrale"),
    ("A-MAR-001", "MAR", "Noor Ouarzazate IV (PV)", "", "à vérifier",
     None, None, None, None, None, None, "", "", ""),
    ("A-BFA-001", "BFA", "Zagtouli", "", "à vérifier",
     None, None, None, None, None, None, "", "", ""),
    ("A-ZAF-001", "ZAF", "REIPPPP — projets PV (par fenêtre)", "Multiples", "à vérifier",
     None, None, None, None, None, None, "Appel d'offres concurrentiel", "",
     "À éclater en une ligne par projet à partir des documents du DMRE/IPP Office"),
]


PROJETS_B = [
    dict(projet_id="B-MLI-001", pays_iso3="MLI", nom="Fekola (mine d'or)", developpeur="B2Gold",
         statut="en service", puissance_mwp=30, stockage_mwh=15.4, technologie="PV + BESS + HFO",
         capex_total=38e6, capex_devise="USD", capex_annee_prix=2019, secteur="Mines",
         modele_commercial="Autoproduction", sources="S08;S09",
         fiabilite_globale="C - presse spécialisée",
         notes="CAPEX = budget approuvé, pas le coût final ; stockage 13,5 vs 15,4 MWh ; "
               "année de mise en service à confirmer"),
    dict(projet_id="B-MRT-001", pays_iso3="MRT", nom="Tasiast (mine d'or)", developpeur="Kinross",
         statut="en service", annee_mise_en_service=2023, puissance_mwp=34,
         technologie="PV + BESS (18 MW) + thermique", capex_total=55e6, capex_devise="USD",
         capex_annee_prix=2022, secteur="Mines", modele_commercial="Autoproduction",
         taux_couverture_solaire=0.20, sources="S10;S11",
         fiabilite_globale="C - presse spécialisée",
         notes="Couverture ~20 % = prévision ; CAPEX annoncé, pas le coût final"),
]
PROJETS_C = [
    dict(projet_id="C-COD-001", pays_iso3="COD", nom="Goma Ndosho (métro-réseau)", developpeur="Nuru",
         statut="en service", annee_mise_en_service=2020, puissance_mwp=1.3,
         technologie="PV + BESS + groupes de secours (~364 kW)", operateur="Privé",
         sources="S12", fiabilite_globale="C - presse spécialisée",
         notes="Coût, tarif et nombre de clients non publiés dans les sources consultées"),
]

# Repères agrégés par segment : jamais mélangés entre volets.
REPERES = [
    ("A", "LCOE moyen pondéré PV, monde", 43, "USD/MWh", 2024, "observée (agrégat)", "S01"),
    ("A", "IRENA RPGC 2024 — LCOE moyen pondéré PV, Afrique (USD 2024)", 74, "USD/MWh", 2024, "observée (agrégat)", "S15"),
    ("A", "IRENA RPGC 2024 — LCOE moyen pondéré PV, Afrique (USD 2024)", 225, "USD/MWh", 2015, "observée (agrégat)", "S15"),
    ("A", "IRENA RPGC 2024 — LCOE PV Afrique, 5e percentile", 49, "USD/MWh", 2024, "observée (agrégat)", "S15"),
    ("A", "IRENA RPGC 2024 — LCOE PV Afrique, 95e percentile", 186, "USD/MWh", 2024, "observée (agrégat)", "S15"),
    ("A", "IRENA RPGC 2024 — coût d'installation PV, Afrique (USD 2024)", 1093, "USD/kW", 2024, "observée (agrégat)", "S15"),
    ("A", "IRENA RPGC 2024 — coût d'installation PV, Afrique (USD 2024)", 3437, "USD/kW", 2015, "observée (agrégat)", "S15"),
    ("A", "IRENA RPGC 2024 — WACC réel supposé, PV Afrique", 0.12, "%", 2024, "hypothèse IRENA", "S15"),
    ("A", "IRENA RPGC 2025 — LCOE moyen pondéré PV, Afrique (USD 2025)", 52, "USD/MWh", 2025, "observée (agrégat)", "S16"),
    ("A", "IRENA RPGC 2025 — LCOE moyen pondéré PV, Afrique (USD 2025)", 222, "USD/MWh", 2015, "observée (agrégat)", "S16"),
    ("A", "IRENA RPGC 2025 — coût d'installation PV, Afrique (USD 2025)", 837, "USD/kW", 2025, "observée (agrégat)", "S16"),
    ("A", "IRENA RPGC 2025 — coût d'installation PV, Afrique (USD 2025)", 3520, "USD/kW", 2015, "observée (agrégat)", "S16"),
    ("C", "LCOE mini-réseaux solaires hybrides isolés (min)", 490, "USD/MWh", 2020, "observée (étude)", "S13"),
    ("C", "LCOE mini-réseaux solaires hybrides isolés (max)", 680, "USD/MWh", 2020, "observée (étude)", "S13"),
    ("C", "Objectif LCOE mini-réseaux 2030", 200, "USD/MWh", 2030, "projection", "S14"),
]


def header(ws, cols, row=1):
    for i, name in enumerate(cols, 1):
        c = ws.cell(row=row, column=i, value=name)
        c.font, c.fill = HEAD, HEAD_FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.column_dimensions[get_column_letter(i)].width = max(12, min(40, len(name) + 4))
    ws.freeze_panes = f"A{row + 1}"


def add_list(ws, col_letter, values, rows=2000):
    dv = DataValidation(type="list", formula1='"' + ",".join(values) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"{col_letter}2:{col_letter}{rows}")


def volet_sheet(wb, title, spec):
    ws = wb.create_sheet(title)
    fields = [f for f, _, _ in COMMUNS + spec]
    header(ws, fields)
    add_list(ws, get_column_letter(fields.index("statut") + 1), STATUTS)
    add_list(ws, get_column_letter(fields.index("fiabilite_globale") + 1), FIABILITE)
    return ws, fields


def build() -> Workbook:
    wb = Workbook()
    ws = wb.active
    ws.title = "Lisez-moi"
    lines = [
        "Le coût de l'électricité solaire en Afrique (2016–2026) — base de données et modèle",
        f"Version gabarit générée le {AS_OF} par build_workbook.py. Date d'arrêt de l'étude : 17 octobre 2026.",
        "",
        "Règles :",
        "1. Aucune valeur sans source : chaque chiffre est consigné dans Observations avec type, source et note.",
        "2. Types de donnée : observée (contrat, mesure), déclarée (annonce), modélisée (calcul), non disponible.",
        "3. Ne jamais mélanger USD/kWp (DC) et USD/kWac (AC). Conserver devise et année d'origine.",
        "4. Les projets en construction ou attribués restent hors des statistiques « en service ».",
        "5. Les trois volets sont comparés séparément : Synthese calcule chaque statistique dans un seul",
        "   volet, et les repères agrégés (Reperes) portent leur volet. Dans le volet A, PV+stockage et",
        "   solaire thermodynamique (CSP) sont analysés à part du PV seul.",
        "6. Modèles : Modele_LCOE (volet A), Modele_B_captif (solaire contre diesel),",
        "   Modele_C_minireseau (coût complet du service et subvention).",
        "7. Le LCOE est toujours calculé, jamais saisi comme donnée observée.",
        "",
        "État actuel : volet A, 4 projets partiellement renseignés (Zambie, Sénégal) et 4 candidats « à vérifier »",
        "sans chiffres ; volet B, 2 projets miniers (Mali, Mauritanie) ; volet C, 1 mini-réseau (RDC).",
        "Les cibles de 100 / 75 / 125 projets sont des objectifs de collecte, pas des projets identifiés.",
    ]
    for i, t in enumerate(lines, 1):
        ws.cell(row=i, column=1, value=t)
    ws["A1"].font = Font(bold=True, size=14)
    ws.column_dimensions["A"].width = 110

    ws = wb.create_sheet("Dictionnaire")
    header(ws, ["volet", "champ", "unité", "description"])
    for volet, spec in (("commun", COMMUNS), ("A", SPEC_A), ("B", SPEC_B), ("C", SPEC_C)):
        for f, u, d in spec:
            ws.append([volet, f, u, d])
    ws.column_dimensions["D"].width = 70

    ws = wb.create_sheet("Pays")
    header(ws, ["region", "iso3", "pays", "nb_projets_A", "nb_projets_B", "nb_projets_C"])
    for i, (reg, iso, nom) in enumerate(PAYS, 2):
        ws.append([reg, iso, nom] + [f'=COUNTIF(Volet_{v}!B:B,B{i})' for v in "ABC"])

    ws_a, fa = volet_sheet(wb, "Volet_A", SPEC_A)
    for (pid, iso, nom, dev, statut, attr, cod, mwp, mwac, tarif, dev_t, proc, src, note) in PROJETS_A:
        row = dict(projet_id=pid, pays_iso3=iso, nom=nom, developpeur=dev, statut=statut,
                   annee_attribution=attr, annee_mise_en_service=cod, puissance_mwp=mwp,
                   puissance_mwac=mwac, tarif=tarif, tarif_devise=dev_t, procedure=proc,
                   sources=src, notes=note)
        ws_a.append([row.get(f) for f in fa])
    for title, spec, rows in (("Volet_B", SPEC_B, PROJETS_B), ("Volet_C", SPEC_C, PROJETS_C)):
        ws_v, fields = volet_sheet(wb, title, spec)
        for row in rows:
            assert set(row) <= set(fields), set(row) - set(fields)
            ws_v.append([row.get(f) for f in fields])

    ws = wb.create_sheet("Observations")
    header(ws, ["projet_id", "champ", "valeur", "unité", "type_donnee", "source_id", "note"])
    for o in OBSERVATIONS:
        ws.append(list(o))
    add_list(ws, "E", TYPES_DONNEE)

    ws = wb.create_sheet("Sources")
    header(ws, ["source_id", "organisme", "titre", "année", "url", "fiabilité", "contenu utilisé"])
    for s in SOURCES:
        ws.append(list(s))
    ws.column_dimensions["E"].width = 60
    ws.column_dimensions["G"].width = 60

    ws = wb.create_sheet("Reperes")
    header(ws, ["volet", "indicateur", "valeur", "unité", "année", "type", "source_id"])
    for r in REPERES:
        ws.append(list(r))
    ws.column_dimensions["B"].width = 50

    research_sheets(wb)
    synthese_sheet(wb)
    lcoe_sheet(wb)
    captive_sheet(wb)
    minigrid_sheet(wb)
    verification_sheet(wb)
    return wb


def lcoe_sheet(wb):
    ws = wb.create_sheet("Modele_LCOE")
    ws["A1"] = "Modèle LCOE — cellules jaunes modifiables. Investissement en année 0, flux en années 1..n."
    ws["A1"].font = Font(bold=True)
    inputs = [
        ("Puissance", 50, "MWp"),
        ("CAPEX spécifique", 1000, "USD/kWp"),
        ("Production spécifique année 1", 1800, "kWh/kWp/an"),
        ("OPEX année 1", 15, "USD/kWp/an"),
        ("Indexation OPEX", 0.0, "%/an"),
        ("Dégradation", 0.0, "%/an"),
        ("Durée de vie", 25, "années (max 40)"),
        ("Part de la dette", 0.7, "%"),
        ("Coût de la dette", 0.08, "%"),
        ("Coût des fonds propres", 0.15, "%"),
        ("Taux d'impôt", 0.0, "%"),
        ("WACC calculé", "=B10*B11*(1-B13)+(1-B10)*B12", "%"),
        ("WACC retenu (vide = calculé)", None, "%"),
    ]
    for i, (lab, val, unit) in enumerate(inputs, 3):
        ws.cell(row=i, column=1, value=lab)
        c = ws.cell(row=i, column=2, value=val)
        ws.cell(row=i, column=3, value=unit)
        if not (isinstance(val, str) and val.startswith("=")):
            c.fill = INPUT_FILL
    for r in (7, 8, 10, 11, 12, 13, 14, 15):
        ws.cell(row=r, column=2).number_format = "0.0%"

    ws["A17"], ws["B17"] = "Taux d'actualisation", "=IF(ISBLANK(B15),B14,B15)"
    ws["A18"], ws["B18"] = "CAPEX total (USD)", "=B3*1000*B4"
    ws["A19"], ws["B19"] = "Production année 1 (MWh)", "=B3*B5"
    ws["A20"], ws["B20"] = "OPEX année 1 (USD)", "=B3*1000*B6"
    ws["A21"], ws["B21"] = "Coûts actualisés (USD)", "=B18+SUMPRODUCT(F4:F43,H4:H43)"
    ws["A22"], ws["B22"] = "Production actualisée (MWh)", "=SUMPRODUCT(G4:G43,H4:H43)"
    ws["A23"], ws["B23"] = "LCOE (USD/MWh)", "=B21/B22"
    ws["A24"], ws["B24"] = "Facteur de charge DC", "=B5/8760"
    ws["B17"].number_format = ws["B24"].number_format = "0.0%"
    ws["B23"].number_format = "0.0"
    ws["A23"].font = ws["B23"].font = Font(bold=True)

    ws["E3"], ws["F3"], ws["G3"], ws["H3"] = "année", "OPEX (USD)", "production (MWh)", "facteur d'actualisation"
    for c in ("E3", "F3", "G3", "H3"):
        ws[c].font = Font(bold=True)
    for k, r in enumerate(range(4, 44), 1):
        ws[f"E{r}"] = k
        ws[f"F{r}"] = f"=IF(E{r}<=$B$9,$B$20*(1+$B$7)^(E{r}-1),0)"
        ws[f"G{r}"] = f"=IF(E{r}<=$B$9,$B$19*(1-$B$8)^(E{r}-1),0)"
        ws[f"H{r}"] = f"=1/(1+$B$17)^E{r}"

    ws["J3"] = "Sensibilité au WACC (sans dégradation ni indexation : (CAPEX x CRF + OPEX) / E)"
    ws["J3"].font = Font(bold=True)
    ws["J4"], ws["K4"], ws["L4"] = "WACC", "LCOE (USD/MWh)", "écart vs 4 %"
    for i, r in enumerate((0.04, 0.06, 0.08, 0.10, 0.12, 0.14), 5):
        ws[f"J{i}"] = r
        ws[f"J{i}"].number_format = "0%"
        ws[f"K{i}"] = f"=($B$18*J{i}*(1+J{i})^$B$9/((1+J{i})^$B$9-1)+$B$20)/$B$19"
        ws[f"K{i}"].number_format = "0.0"
        ws[f"L{i}"] = f"=K{i}/$K$5-1"
        ws[f"L{i}"].number_format = "0.0%"
    ws["J12"] = ("Valeurs par défaut = cas illustratif de la proposition (50 MWp, 50 M USD, 90 GWh, "
                 "0,75 M USD/an, 25 ans). Résultats illustratifs, pas des coûts observés.")
    ws["J12"].font = NOTE
    ws.column_dimensions["A"].width = 30
    for col in "EFGH":
        ws.column_dimensions[col].width = 16
    ws.column_dimensions["J"].width = 12
    ws.column_dimensions["K"].width = 16


RESEARCH = Path(__file__).with_name("recherche") / "donnees.json"
RESEARCH_COLS = ["tranche", "volet", "pays_iso3", "projet", "champ", "valeur", "unite", "type_donnee",
                 "annee_valeur", "fiabilite", "verification", "source_organisme", "source_titre", "url",
                 "date_source", "citation", "note"]


def research_sheets(wb):
    """Résultats des agents : retenus (vérifiés automatiquement) et à revoir, séparément."""
    if not RESEARCH.exists():
        return
    data = json.loads(RESEARCH.read_text())
    for title, keep, intro in (
        ("Recherche_retenue", ("retenu", "qualitatif"),
         "Valeurs collectées par les agents dont la citation a été retrouvée dans la source retéléchargée "
         "(et, pour les chiffres, dont la valeur figure dans la citation). Vérification automatique, "
         "pas une relecture humaine."),
        ("Recherche_a_revoir", ("a_revoir",),
         "Valeurs NON retenues : citation introuvable, valeur dérivée ou additionnée, ou source "
         "inaccessible au contrôle. À vérifier à la main avant tout usage."),
    ):
        ws = wb.create_sheet(title)
        ws["A1"] = intro
        ws["A1"].font = NOTE
        header(ws, ["usage"] + RESEARCH_COLS, row=2)
        for r in data["records"]:
            if r["usage"] in keep:
                ws.append([r["usage"]] + [r.get(c) for c in RESEARCH_COLS])
        ws.auto_filter.ref = f"A2:{get_column_letter(len(RESEARCH_COLS) + 1)}{ws.max_row}"
        ws.column_dimensions["E"].width = 34
        ws.column_dimensions["Q"].width = 80
    ws = wb.create_sheet("Conflits_lacunes")
    header(ws, ["type", "tranche", "description"])
    for c in data["conflits"]:
        ws.append(["conflit", c["tranche"], c["conflit"]])
    for n in data["non_trouve"]:
        ws.append(["non trouvé", n["tranche"], n["element"]])
    ws.column_dimensions["C"].width = 120


def synthese_sheet(wb):
    ws = wb.create_sheet("Synthese")
    ws["A1"] = "Synthèse par volet : chaque statistique est calculée à l'intérieur d'un seul volet."
    ws["A1"].font = Font(bold=True)
    ws["A2"] = ("Les moyennes ne portent que sur les projets « en service » renseignés. "
                "Avec si peu de projets, elles ne sont pas représentatives.")
    ws["A2"].font = NOTE
    cols = ["volet", "indicateur"] + STATUTS
    for i, c in enumerate(cols, 1):
        cell = ws.cell(row=4, column=i, value=c)
        cell.font, cell.fill = HEAD, HEAD_FILL
    r = 5
    for v in "ABC":
        ws.cell(row=r, column=1, value=v)
        ws.cell(row=r, column=2, value="nombre de projets")
        for j, st in enumerate(STATUTS, 3):
            ws.cell(row=r, column=j, value=f'=COUNTIF(Volet_{v}!F:F,"{st}")')
        r += 1
    r += 1
    for i, c in enumerate(["volet", "indicateur (projets en service)", "n", "moyenne", "min", "max"], 1):
        cell = ws.cell(row=r, column=i, value=c)
        cell.font, cell.fill = HEAD, HEAD_FILL
    r += 1
    fields_all = {v: [f for f, _, _ in COMMUNS + spec] for v, spec in
                  (("A", SPEC_A), ("B", SPEC_B), ("C", SPEC_C))}
    metrics = [("A", "capex_usd_kwac"), ("A", "lcoe_usd_mwh"), ("A", "facteur_charge_ac"),
               ("B", "capex_usd_kwp"), ("B", "cout_diesel_evite_usd_mwh"), ("B", "tri_projet"),
               ("C", "capex_usd_kwp"), ("C", "tarif_client"), ("C", "subvention_usd")]
    for v, f in metrics:
        col = get_column_letter(fields_all[v].index(f) + 1)
        rng, st = f"Volet_{v}!{col}2:{col}2000", f'Volet_{v}!F2:F2000,"en service"'
        ws.append([v, f, f"=COUNTIFS({st},{rng},\"<>\")",
                   f'=IFERROR(AVERAGEIFS({rng},{st}),"")',
                   f'=IF(C{r}=0,"",MINIFS({rng},{st}))',
                   f'=IF(C{r}=0,"",MAXIFS({rng},{st}))'])
        r += 1
    ws.column_dimensions["B"].width = 34
    ws.column_dimensions["A"].width = 8


def _inputs(ws, rows, start=3):
    for i, (lab, val, unit) in enumerate(rows, start):
        ws.cell(row=i, column=1, value=lab)
        c = ws.cell(row=i, column=2, value=val)
        ws.cell(row=i, column=3, value=unit)
        if not (isinstance(val, str) and val.startswith("=")):
            c.fill = INPUT_FILL
        if unit.startswith("%"):
            c.number_format = "0.0%"
    ws.column_dimensions["A"].width = 42
    ws.column_dimensions["C"].width = 18


def captive_sheet(wb):
    ws = wb.create_sheet("Modele_B_captif")
    ws["A1"] = ("Volet B — solaire captif contre diesel/HFO, du point de vue de l'industriel. "
                "Valeurs par défaut illustratives, à remplacer par celles du site.")
    ws["A1"].font = Font(bold=True)
    _inputs(ws, [
        ("Puissance PV", 10, "MWp"),                                   # B3
        ("CAPEX spécifique (PV + stockage éventuel)", 900, "USD/kWp"),  # B4
        ("Production spécifique année 1", 1700, "kWh/kWp/an"),          # B5
        ("Part de la production solaire consommée", 0.95, "% (écrêtage exclu)"),  # B6
        ("OPEX solaire", 15, "USD/kWp/an"),                             # B7
        ("Prix du carburant livré sur site", 1.10, "USD/l"),            # B8
        ("Consommation spécifique du groupe", 0.27, "l/kWh"),           # B9
        ("O&M variable du groupe", 25, "USD/MWh"),                      # B10
        ("Indexation du prix du carburant", 0.02, "%/an"),              # B11
        ("Dégradation PV", 0.005, "%/an"),                              # B12
        ("Durée d'analyse", 20, "années (max 30)"),                     # B13
        ("Taux d'actualisation de l'industriel", 0.12, "%"),            # B14
    ])
    ws["A16"], ws["B16"] = "CAPEX total (USD)", "=B3*1000*B4"
    ws["A17"], ws["B17"] = "Énergie solaire utile année 1 (MWh)", "=B3*B5*B6"
    ws["A18"], ws["B18"] = "Coût diesel évité (USD/MWh)", "=B8*B9*1000+B10"
    ws["A19"], ws["B19"] = "OPEX solaire (USD/an)", "=B3*1000*B7"
    ws["A20"], ws["B20"] = "Économie nette année 1 (USD)", "=B17*B18-B19"
    ws["A21"], ws["B21"] = "Temps de retour simple (années)", '=IF(B20<=0,"jamais",B16/B20)'
    ws["A22"], ws["B22"] = "VAN (USD)", "=NPV(B14,F5:F34)+F4"
    ws["A23"], ws["B23"] = "TRI", '=IFERROR(IRR(F4:F34),"n.d.")'
    ws["A24"], ws["B24"] = "LCOE solaire (USD/MWh utile)", "=(B16+SUMPRODUCT(D5:D34,H5:H34))/SUMPRODUCT(C5:C34,H5:H34)"
    ws["B23"].number_format = "0.0%"
    for c in ("B18", "B21", "B24"):
        ws[c].number_format = "0.0"
    for c in ("B16", "B20", "B22"):
        ws[c].number_format = "#,##0"
    for c, t in zip("EFCDGH", ["année", "flux net (USD)", "énergie utile (MWh)", "OPEX (USD)",
                               "économie carburant (USD)", "actualisation"]):
        ws[f"{c}3"] = t
        ws[f"{c}3"].font = Font(bold=True)
    ws["E4"], ws["F4"] = 0, "=-B16"
    for k, r in enumerate(range(5, 35), 1):
        ws[f"E{r}"] = k
        ws[f"C{r}"] = f"=IF(E{r}<=$B$13,$B$17*(1-$B$12)^(E{r}-1),0)"
        ws[f"D{r}"] = f"=IF(E{r}<=$B$13,$B$19,0)"
        ws[f"G{r}"] = f"=C{r}*$B$18*(1+$B$11)^(E{r}-1)"
        ws[f"F{r}"] = f"=G{r}-D{r}"
        ws[f"H{r}"] = f"=1/(1+$B$14)^E{r}"
    ws["A26"] = ("Limites : pas de coût de stockage spécifique, pas de valeur de la continuité de service "
                 "ni d'investissement évité dans les groupes ; à ajouter projet par projet. "
                 "Le TRI élevé obtenu par défaut n'est pas calibré : la presse évoque 3 à 7 ans de retour "
                 "pour Fekola (PV + stockage), contre moins de 2 ans ici.")
    ws["A26"].font = NOTE


def minigrid_sheet(wb):
    ws = wb.create_sheet("Modele_C_minireseau")
    ws["A1"] = ("Volet C — coût complet du service d'un mini-réseau (production, distribution, gestion "
                "commerciale) et subvention nécessaire. Valeurs par défaut illustratives.")
    ws["A1"].font = Font(bold=True)
    _inputs(ws, [
        ("Puissance PV", 100, "kWp"),                                    # B3
        ("CAPEX production (PV, batteries, groupe)", 2500, "USD/kWp"),   # B4
        ("Production utile année 1", 1400, "kWh/kWp/an"),                # B5
        ("Nombre de clients", 500, "branchements"),                      # B6
        ("CAPEX distribution par client", 400, "USD/client"),            # B7
        ("OPEX technique (y c. annuité de remplacement des batteries)", 60, "USD/kWp/an"),  # B8
        ("Coût de gestion commerciale par client", 12, "USD/client/an"), # B9
        ("Pertes et impayés", 0.15, "% de la production"),              # B10
        ("Taux d'actualisation", 0.10, "%"),                            # B11
        ("Durée d'analyse", 20, "années"),                              # B12
        ("Tarif autorisé", 0.25, "USD/kWh"),                            # B13
    ])
    ws["A15"], ws["B15"] = "CRF", "=B11*(1+B11)^B12/((1+B11)^B12-1)"
    ws["A16"], ws["B16"] = "Énergie vendue (MWh/an)", "=B3*B5*(1-B10)/1000"
    ws["A17"], ws["B17"] = "Consommation par client (kWh/mois)", "=B16*1000/B6/12"
    ws["A18"], ws["B18"] = "Coût de production (USD/MWh vendu)", "=(B3*B4*B15+B3*B8)/B16"
    ws["A19"], ws["B19"] = "Coût de distribution (USD/MWh vendu)", "=B6*B7*B15/B16"
    ws["A20"], ws["B20"] = "Coût commercial (USD/MWh vendu)", "=B6*B9/B16"
    ws["A21"], ws["B21"] = "Coût complet du service (USD/MWh)", "=B18+B19+B20"
    ws["A22"], ws["B22"] = "Subvention d'investissement nécessaire (USD)", "=MAX(0,B21-B13*1000)*B16/B15"
    ws["A23"], ws["B23"] = "Subvention par branchement (USD)", "=B22/B6"
    ws["A21"].font = ws["B21"].font = Font(bold=True)
    for c in ("B15",):
        ws[c].number_format = "0.0000"
    for c in ("B16", "B17", "B18", "B19", "B20", "B21"):
        ws[c].number_format = "0.0"
    for c in ("B22", "B23"):
        ws[c].number_format = "#,##0"
    ws["A25"] = ("La consommation par client (B17) pèse sur le coût de distribution et le coût commercial : "
                 "c'est le principal levier de la question économique du volet C.")
    ws["A25"].font = NOTE


def verification_sheet(wb):
    ws = wb.create_sheet("Verif_proposition")
    header(ws, ["affirmation de la proposition", "statut", "constat", "source"])
    rows = [
        ("WACC jusqu'à 12 % en Afrique dans l'analyse IRENA 2024", "confirmé",
         "IRENA : hypothèses de WACC de 3,8 % (Europe) à 12 % (Afrique), conditions 2023", "S01"),
        ("LCOE solaire mondial 2024 : 43 USD/MWh", "confirmé", "0,043 USD/kWh", "S01;S02"),
        ("CAPEX Afrique 2024 : 1 093 USD/kW", "confirmé", "Rapport complet IRENA 2024, Table 3.1 p. 95", "S15"),
        ("LCOE Afrique 2024 : 74 USD/MWh", "confirmé", "Rapport complet IRENA 2024, Table 3.3 p. 106", "S15"),
        ("CAPEX Afrique 2015 : 3 437 USD/kW ; LCOE 2015 : 225 USD/MWh", "confirmé",
         "Rapport complet IRENA 2024 (USD 2024). L'édition 2025 donne 3 520 USD/kW et 222 USD/MWh pour "
         "2015 en USD 2025 : ne pas mélanger les éditions", "S15;S16"),
        ("(nouveau) Afrique 2025 : 837 USD/kW et 52 USD/MWh", "confirmé",
         "Rapport complet IRENA 2025, Tables 3.1 et 3.2 ; -76 % et -77 % depuis 2015", "S16"),
        ("Tableau WACC 4–14 % (43,9 à 89,3 USD/MWh)", "confirmé (calcul)",
         "Reproduit : 43,9 / 51,8 / 60,4 / 69,5 / 79,2 / 89,2 ; écarts d'arrondi ≤ 0,1", "lcoe.py"),
        ("+80 % de LCOE entre WACC 4 % et 12 %", "confirmé (calcul)", "+80,4 %", "lcoe.py"),
        ("Ngonye / Bangweulu", "précisé",
         "Bangweulu = 6,015 USc/kWh (Neoen/First Solar) ; Ngonye = 7,84 USc/kWh (Enel)", "S04;S05"),
        ("Kael et Kahone", "confirmé", "3,98 et 3,80 c EUR/kWh, mise en service mai 2021", "S06;S07"),
    ]
    for r in rows:
        ws.append(list(r))
    ws.column_dimensions["A"].width = 55
    ws.column_dimensions["C"].width = 80


if __name__ == "__main__":
    build().save(OUT)
    print(f"écrit : {OUT}")
