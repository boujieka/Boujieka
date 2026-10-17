# Le coût de l'électricité solaire en Afrique (2016–2026)

Phase 1 de l'étude comparative : grandes centrales raccordées (volet A), centrales industrielles
captives (volet B) et mini-réseaux (volet C). Date d'arrêt : 17 octobre 2026.

Les trois volets sont **couverts et comparés séparément** : un onglet de données, un modèle et des
statistiques propres à chacun. Aucune moyenne ni aucun classement ne mélange deux volets, parce que
les indicateurs ne mesurent pas la même chose :

| Volet | Indicateur principal | Ce qu'il mesure | Modèle |
|---|---|---|---|
| A — réseau | LCOE et tarif PPA (USD/MWh) | Coût de production au point d'injection | `Modele_LCOE` |
| B — captif | Coût diesel évité, VAN, TRI, retour | Économie pour l'industriel | `Modele_B_captif` |
| C — mini-réseau | Coût complet du service (USD/MWh vendu), subvention | Production + distribution + gestion commerciale | `Modele_C_minireseau` |

| Fichier | Contenu |
|---|---|
| `etude_solaire_afrique.xlsx` | Base de données (3 volets), journal des observations sourcées, registre des sources, repères par segment, synthèse par volet, trois modèles en formules, vérification de la proposition |
| `build_workbook.py` | Régénère le classeur (`python build_workbook.py`) |
| `lcoe.py` | LCOE, CRF, WACC, VAN/TRI, comparaison solaire/diesel (B), coût du service et subvention (C) |
| `test_lcoe.py` | Tests (`python -m pytest test_lcoe.py`) |

Les modèles Excel et `lcoe.py` donnent les mêmes résultats, vérifiés après recalcul LibreOffice
(volet A : 70,0 USD/MWh à 10,1 % ; volet B : VAN, TRI et retour identiques ; volet C : coût complet
de 545 USD/MWh et subvention de 298 884 USD avec les valeurs par défaut). Les valeurs par défaut des
modèles B et C sont **illustratives et non calibrées** : le retour de moins de 2 ans du modèle B est
bien plus court que les 3 à 7 ans évoqués par la presse pour Fekola.

## Vérification des chiffres de la proposition

| Affirmation | Statut | Constat |
|---|---|---|
| WACC jusqu'à 12 % en Afrique (IRENA 2024) | Confirmé | Le résumé IRENA donne 3,8 % (Europe) à 12 % (Afrique) |
| LCOE solaire mondial 2024 : 43 USD/MWh | Confirmé | 0,043 USD/kWh |
| CAPEX Afrique 2024 : 1 093 USD/kW | Corroboré (source secondaire) | Repris par pv magazine d'après IRENA ; absent du résumé IRENA |
| LCOE Afrique 2024 : 74 USD/MWh | **Non vérifié** | Absent du résumé IRENA ; à contrôler dans le rapport complet |
| 2015 : 3 437 USD/kW et 225 USD/MWh | **Non vérifié** | Une source secondaire citant l'édition IRENA suivante donne 3 520 USD/kW et 222 USD/MWh : IRENA révise ses séries historiques d'une édition à l'autre |
| Tableau WACC 4–14 % | Confirmé (calcul) | 43,9 / 51,8 / 60,4 / 69,5 / 79,2 / 89,2 USD/MWh ; la proposition arrondit 3 valeurs à 0,1 près au-dessus |
| +80 % entre WACC 4 % et 12 % | Confirmé (calcul) | +80,4 % |

Règle qui en découle : citer une seule édition IRENA pour toute série temporelle, sans mélanger
les éditions.

## Projets déjà renseignés (valeurs sourcées uniquement)

| Projet | Tarif | Mise en service | Remarque |
|---|---|---|---|
| Bangweulu (Zambie) | 6,015 USc/kWh | 2019 | 54 MW (Banque mondiale) ou 56 MW (Climatescope) : à réconcilier |
| Ngonye (Zambie) | 7,84 USc/kWh | 2019 | 34 MW |
| Kael (Sénégal) | 3,98 c EUR/kWh | mai 2021 | Kael + Kahone = 60 MWac |
| Kahone (Sénégal) | 3,80 c EUR/kWh | mai 2021 | |

Benban, Noor Ouarzazate IV, Zagtouli et REIPPPP figurent comme candidats « à vérifier », sans chiffres.

### Volet B — centrales captives

| Projet | Configuration | CAPEX | Statut des données |
|---|---|---|---|
| Fekola, Mali (B2Gold) | 30 MW PV + 15,4 MWh (13,5 MWh annoncés) + HFO | 38 M USD **budget approuvé 2019** | Économie prévue : 13,1 Ml de fioul lourd/an ; année de mise en service à confirmer |
| Tasiast, Mauritanie (Kinross) | 34 MW PV + batterie 18 MW (MWh inconnus) | 55 M USD **annoncés en 2022** | Premier courant solaire en décembre 2023 ; couverture prévue ~20 % |

Les CAPEX/kW de ces projets ne sont pas calculés : budgets non définitifs, stockage inclus,
base DC/AC non précisée.

### Volet C — mini-réseaux

| Projet | Configuration | Données manquantes |
|---|---|---|
| Goma Ndosho, RDC (Nuru) | 1,3 MW PV + batteries + ~364 kW de groupes, inauguré le 4 février 2020 | Coût, tarif, nombre de clients |

Repères de segment (onglet `Reperes`) : LCOE de 0,49 à 0,68 USD/kWh pour des mini-réseaux solaires
hybrides isolés dans six pays (BNEF/SEforALL, 2020) ; objectif de 0,20 USD/kWh en 2030 (ESMAP, 2019,
projection). Ces ordres de grandeur sont 6 à 15 fois le LCOE du volet A : c'est la raison de ne pas
les comparer dans un même classement.
Le tarif de 7,8 USc/kWh souvent cité pour le round 2 de Benban n'a pas été confirmé.

## Points de méthode à trancher

1. **Les tarifs ne sont pas comparables tels quels.** Kael/Kahone sont en EUR et Scaling Solar
   Zambie en USD ; la part indexée, la durée et les garanties (IDA, MIGA) diffèrent. Une conversion
   en USD constants exige une règle explicite (taux à la date de signature ou à la mise en service).
2. **CAPEX des IPP rarement publiés.** Pour les projets privés, les montants de financement (dette
   DFI + fonds propres) servent souvent de proxy ; ils incluent frais de développement, intérêts
   intercalaires et parfois le raccordement. Ils seront classés « déclarés », pas « observés ».
3. **Échantillon biaisé.** Les projets bien documentés sont surtout ceux financés par des DFI ou
   issus de programmes comme Scaling Solar : ce sont probablement les moins chers. Le benchmark
   risque de sous-estimer les coûts réels moyens si ce biais n'est pas signalé.
4. **Objectifs de 300 projets.** Pour les volets B et C, les données contractuelles sont rarement
   publiques ; des sources agrégées (rapports ESMAP/Banque mondiale sur les mini-réseaux) seront
   probablement nécessaires en complément de fiches projet par projet.
5. **Question 6 (« coût justifiable » par pays).** Elle relève de la modélisation, pas de
   l'observation : chaque résultat devra afficher ses hypothèses (ensoleillement, CAPEX, WACC pays).

## Sources

- IRENA, *Renewable Power Generation Costs in 2024 — Summary* (2025) : https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2025/Jul/IRENA_TEC_RPGC_in_2024_Summary_2025.pdf
- pv magazine (23/07/2025) : https://www.pv-magazine.com/2025/07/23/global-average-solar-lcoe-stood-at-0-043-kwh-in-2024-says-irena/
- Banque mondiale (14/05/2019) : https://www.worldbank.org/en/news/feature/2019/05/14/unlocking-low-cost-large-scale-solar-power-in-zambia
- pv-tech : https://www.pv-tech.org/news/ifc-zambia-solar-auction-sees-record-low-6-price-benchmark
- Climatescope 2022, Zambie : https://2022.global-climatescope.org/markets/zm/
- IFC, Senegal Scaling Solar PPP brief (2021) : https://www.ifc.org/content/dam/ifc/doc/2021/2021-senegal-scaling-solar-ppp-brief.pdf
- IFC, communiqué (2021) : https://www.ifc.org/en/pressroom/2021/scaling-solar-two-pv-plants-bring-clean-energy-to-more-than-500000-in-senegal
- Mining Weekly, Fekola (2019) : https://www.miningweekly.com/article/b2gold-approves-3m-hybrid-energy-project-for-mali-mine-2019-10-14
- Africa Energy Portal, Fekola : https://africa-energy-portal.org/news/malian-gold-mine-powered-30-mw154-mwh-solar-plus-storage
- Mining Weekly, Tasiast (2022) : https://www.miningweekly.com/article/kinross-makes-55m-solar-investment-at-tasiast-2022-02-17
- Engineering News, Tasiast (2024) : https://www.engineeringnews.co.za/article/tasiastsolar-project-mauritania-update-2024-02-23
- Afrik 21, Nuru Goma (2020) : https://afrik21.africa/en/drc-nuru-connects-1-3-mw-solar-off-grid-hybrid-in-goma
- BNEF/SEforALL (2020) : https://about.bnef.com/insights/clean-energy/solar-mini-grids-set-to-play-critical-role-in-achieving-universal-electricity-access-with-right-policy-support/
- ESMAP, *Mini Grids for Half a Billion People*, résumé (2019) : https://www1.villanova.edu/content/dam/villanova/engineering/energy-workshop/ESMAP%20Mini%20Grids%20-%20Executive%20Summary.pdf
