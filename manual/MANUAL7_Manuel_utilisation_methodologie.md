# MANUAL 7 : manuel d'utilisation et de méthodologie

## MODEL 7, modèle de développement et de financement de l'hydroélectricité

Version 1.0, version candidate 1 (release candidate 1). Ressource d'accompagnement du Livre 7, *Développement et financement de l'hydroélectricité*.

| Élément | Fichier |
|---|---|
| Classeur | `model/Bankable_Hydro_Model.xlsx` |
| Générateur (source unique de référence) | `model/build_model.py` |
| Carte des cellules écrite par le générateur | `model/model_map.json` |
| Résultats des scénarios sur le moteur complet | `model/snapshot_results.json` |
| Exécuteur de scénarios | `tools/run_snapshots.py` |
| Correction des guillemets pour Excel | `tools/model/excel_quote_fix.py` |
| Contrôle des références circulaires | `tools/model/check_cycles.py` |
| Rapport de test indépendant | `docs/MODEL7_TEST_REPORT.md` |
| Synthèse de la validation dans le livre | Livre 7, annexe K |

Ce manuel remplace `manual/USER_MANUAL.md`, qui décrit un modèle antérieur construit autour du cas Lumora Falls. Chaque nom de feuille, donnée d'entrée, formule et chiffre ci-dessous se rapporte au MODEL 7 actuel et à son cas Kasiri par défaut. Les chiffres présentés comme « cas de base » sont les valeurs du classeur avec les données d'entrée par défaut ; les chiffres présentés comme « instantané » (snapshot) proviennent de `model/snapshot_results.json`.

---

## 1. Ce que fait le modèle et sa place par rapport au Livre 7

### 1.1 La question

Le classeur s'ouvre sur une seule question : ce projet peut-il fournir une électricité bancable sans créer de passifs publics insoutenables ? Le Livre 7 décompose cette question en décisions prises entre le site sur la rivière et le bouclage financier, et MODEL 7 est le moteur qui chiffre chacune de ces décisions.

Le Livre 7 repose sur trois idées que le modèle reproduit.

1. Un projet hydroélectrique réunit trois investissements dans un seul actif : une option de développement (du site au bouclage), un contrat de construction (du bouclage à la mise en service commerciale) et une rente d'exploitation (de la mise en service commerciale à la fin de la concession). Le modèle valorise chacun d'eux : *01A_DEVELOPMENT* pour l'option, *05A_CONTRACTING*, *05_PLANT_CAPEX* et *06_CONSTRUCTION* pour la construction, et les feuilles d'exploitation pour la rente.
2. Trois parties doivent chacune accepter le projet : le développeur, les prêteurs et l'État. Le modèle présente côte à côte les indicateurs de chaque partie sur *32_DASHBOARD*.
3. Le Hydro Readiness Framework pose huit questions, testées par 23 portes de bouclage financier, et aboutit à une seule décision de bouclage. Le modèle applique les 23 portes sur *30A_CLOSE_READINESS* et les rattache au livre sur *34_FRAMEWORK_MAP*.

| Question | Doit être acceptée par | Portes sur 30A |
|---|---|---|
| Q1 Techniquement viable | Développeur, prêteurs | 1 à 4 |
| Q2 Développable | Développeur, État | 5 à 10 |
| Q3 Économique pour le système | État | 11, 12 |
| Q4 Investissable pour le développeur | Développeur | 19 |
| Q5 Bancable | Prêteurs | 17, 18, 20, 23 |
| Q6 Constructible dans le budget | Développeur, prêteurs | 13, 14, 22 |
| Q7 Abordable pour l'acheteur et l'État | État | 15, 16, 21 |
| Q8 Prêt pour le bouclage | Développeur, prêteurs, État | Les 23 |

### 1.2 Le moteur

Le classeur est un moteur unique et intégré qui s'exécute dans cet ordre : ressource hydraulique, centrale, transport, réseau, demande, compagnie d'électricité, régulation, CAE, financement, structure PPP ou PIE, soutien de l'État, exposition budgétaire et, enfin, les deux niveaux de portes. Toute modification, où qu'elle intervienne, se répercute sur tous les maillons suivants.

| Propriété | MODEL 7 |
|---|---|
| Feuilles | 40 |
| Formules actives | environ 11 260 |
| Périodicité | Annuelle, 40 périodes (t = 1 à 40), plus dix colonnes d'années de développement sur *01A_DEVELOPMENT* |
| Macros, tables de données, noms définis, fonctions volatiles, liens externes | Aucun |
| Références circulaires | Aucune (contrôlées avec `tools/model/check_cycles.py`) |
| Tableaux de scénarios | Écrits sous forme de valeurs fixes par `tools/run_snapshots.py` |

### 1.3 Le cas Kasiri

Le projet de référence est Kasiri River Hydro, une centrale au fil de l'eau de 60 MW avec une petite retenue journalière, sur la rivière Kasiri (fictive), dans la République de Navaria (fictive). Dans le Livre 7, il est développé par la société fictive Tamarind Hydro Ltd. L'acheteur est la société publique fictive Navaria Electricity Company. Toutes les données d'entrée sont illustratives : elles sont choisies pour rendre les mécanismes visibles et pour rester dans les fourchettes relevées dans des sources publiques. Remplacez toutes les données d'entrée avant d'utiliser le modèle sur un projet réel. L'aménagement de Lumora Falls, qui apparaît dans le Livre 7 comme point de comparaison, ne figure pas dans le classeur.

### 1.4 Versions

| Produit | Version |
|---|---|
| Livre 7 | v1.0, version candidate 1 |
| MODEL 7 | v1.0, version candidate 1 |
| MANUAL 7 (le présent document) | v1.0, version candidate 1 |
| Cas 7 (Kasiri River Hydro) | v1.0, version candidate 1 |

La version 1.0 sera arrêtée une fois le classeur testé dans Microsoft Excel et les points ouverts de `docs/BOOK7_V04_QA_SUMMARY.md` clos (*00_README*, rubrique *"Versions"*).

Rien dans le modèle ni dans ce manuel ne constitue un conseil en investissement, ni un conseil juridique, fiscal ou comptable.

---

## 2. Conventions

### 2.1 Couleurs et formats

| Convention | Signification |
|---|---|
| Police bleue | Donnée d'entrée saisie en dur |
| Remplissage jaune clair | Donnée d'entrée ordinaire |
| Remplissage jaune vif | Levier clé |
| Police noire | Formule |
| Police verte | Lien direct vers une cellule d'une autre feuille |
| Cellule ombrée de vert | Résultat clé |
| Bandeau bleu foncé | Titre et sous-titre de la feuille |
| Bandeau bleu clair | Titre de section |
| Couleurs des onglets | 00 bleu foncé ; 01 à 19 bleu ; 20 à 29 vert ; 30 à 35 rouge |

Les cellules de statut de *13_REGULATION*, *30_BANKABILITY*, *30A_CLOSE_READINESS*, *32_DASHBOARD*, *33_CHECKS* et *35_BOOK_CHECK* sont colorées par mise en forme conditionnelle : vert pour READY (prêt), MET (franchie), OK (correct) et PASS (réussi) ; ambre pour CONDITIONAL (sous conditions), PARTIAL (partielle) et CHECK (à vérifier) ; orange pour GAP (écart) et DEVELOPMENT GAP (écart de développement) ; rouge pour CRITICAL GAP (écart critique), NOT MET (non franchie) et ERROR (erreur) ; gris pour NO EVIDENCE (sans preuve).

Les données d'entrée de sélection sont protégées par une validation des données qui bloque toute saisie non valide avec un message d'erreur : *case* et *gen_case* acceptent 1 à 3, *lender_case* 1 à 4, *structure* 1 à 5, *debt_mode* 1 à 2, *backstop* et les neuf commutateurs de stress 0 ou 1. Les données d'entrée de statut de *13_REGULATION* et de *30A_CLOSE_READINESS* sont des listes déroulantes.

### 2.2 Unités

Les montants sont exprimés en millions USD (M USD), en termes nominaux, sauf si le libellé indique *"real 2026"* (termes réels 2026). Les données d'entrée réelles sont en dollars américains de 2026 et sont indexées sur l'indice des prix à la consommation (IPC) des États-Unis ou sur l'indice d'indexation du coût d'investissement. L'énergie est en GWh, la puissance en MW, les tarifs en USD/MWh. Les flux en monnaie locale de la compagnie d'électricité sont convertis en équivalents USD au taux de change du modèle (lire navarienne, NVL par USD). Les montants négatifs sont des coûts ou des sorties de trésorerie, sauf indication contraire du libellé ; sur *25_FISCAL_IMPACT*, une VAN budgétaire négative représente un coût net pour l'État.

### 2.3 Calendrier et présentation

Les feuilles de séries chronologiques partagent une même présentation : colonne A libellé, colonne B unité, colonne C total ou valeur clé, colonne D vide, colonnes E à AR périodes t = 1 à 40. Les lignes 4 et 5 indiquent l'année civile et l'année d'exploitation (0 pendant la construction et après la concession). Les volets sont figés en E6.

*06_CONSTRUCTION* est la feuille maîtresse du calendrier. Ses indicateurs pilotent toutes les autres feuilles de séries chronologiques :

```
year       = start_year+t-1
cons_eff   = cons_years+eff_delay
cod_year   = start_year+cons_eff
consflag   = IF(t<=cons_eff,1,0)
opflag     = IF(AND(t>cons_eff,t<=cons_eff+ops_years),1,0)
lastcons   = IF(t=cons_eff,1,0)
opyr       = IF(opflag=1,t-cons_eff,0)
```

La construction et la concession doivent tenir ensemble dans les 40 périodes ; *33_CHECKS* le vérifie.

### 2.4 Temps du modèle pour le cas Kasiri

Le cas Kasiri fonctionne en temps du modèle, et non en dates calendaires.

| Événement | Année du modèle | Source |
|---|---|---|
| Début du développement (reconnaissance) | 2021 | Six étapes d'une durée totale de 72 mois, qui s'achèvent au bouclage financier |
| Bouclage financier, début du modèle (t = 1) | 2027 | `start_year` sur *02_PROJECT_INPUTS* |
| Construction | 2027 à 2029 | `cons_years` = 3 |
| Mise en service commerciale (première année d'exploitation complète) | 2030 | `cod_year` |
| Fin de la durée de 25 ans du CAE | 2054 | `ops_years` = 25 |
| Fin de l'horizon du modèle | 2066 | t = 40 |
| Année de base des prix pour les données d'entrée réelles | 2026 | `base_year` |

Quand le Livre 7 indique que Tamarind est « au début de la phase des permis », il désigne l'étape atteinte (étape 4 sur *01A_DEVELOPMENT*), et non une date calendaire.

---

## 3. Carte des feuilles

Les 41 feuilles : la feuille de couverture, puis les 40 feuilles de travail, regroupées comme sur *00_README*.

**Orientation et pilotage**

| Feuille | Objet |
|---|---|
| COVER | Titre, version, statut en temps réel (décision de bouclage, portes franchies, filtre à neuf portes, filtre budgétaire, contrôles, contrôle de cohérence avec le livre) et liens vers les principales feuilles |
| 00_README | Objet, philosophie, utilisateurs, code couleur, unités, circularité, versions, limites, carte des feuilles |
| 01_CONTROL_PANEL | Cas, cas de production, cas des prêteurs, structure, mode de la dette, garantie budgétaire, neuf commutateurs de stress, cinq variations de sensibilité (flexes) et un affichage du scénario actif |
| 01A_DEVELOPMENT | Six étapes de développement, budget, attrition, VAN du développeur pondérée par le risque, prime au point mort, valeur par étape, revalorisations, cession partielle (sell-down), TRI du développeur |

**Projet (02 à 07, avec 05A)**

| Feuille | Objet |
|---|---|
| 02_PROJECT_INPUTS | Identité du projet, calendrier, taille de la centrale, hypothèses macroéconomiques et taux d'actualisation |
| 03_HYDROLOGY | Hydraulique de la centrale, passage des débits mensuels à la puissance et à l'énergie mensuelles, P50, P75, P90 à un an et P90 à dix ans |
| 04_GENERATION | Énergie installée, disponible, produite, évacuable, livrée et contractée ; production du cas des prêteurs |
| 05_PLANT_CAPEX | Décomposition des coûts, y compris coûts de développement, prime de l'entrepreneur et provisions pour aléas ; comparaison avec les références |
| 05A_CONTRACTING | Structure clés en main, en lots séparés ou multicontrats : prime de l'entrepreneur et part des dépassements et des retards supportée par le maître d'ouvrage |
| 06_CONSTRUCTION | Feuille maîtresse du calendrier, indices IPC et de change, indexation, phasage en courbe en S du coût de la centrale |
| 07_OPEX | O&M, assurance, réserve de gros entretien, frais généraux et administratifs (G&A), O&M de la ligne de transport du projet, redevance sur l'eau |

**Système électrique (08 à 10)**

| Feuille | Objet |
|---|---|
| 08_TRANSMISSION | Coût de la ligne, du poste et des renforcements, maîtrise d'ouvrage, mise en service du transport, écart de maturité |
| 09_GRID | Pointe du système, limite d'absorption à la charge minimale, capacité d'évacuation, part de la pointe |
| 10_DEMAND | Demande par segment, demande potentielle, commerciale, contractée et bancable |

**Acheteur et compagnie d'électricité (11, 12)**

| Feuille | Objet |
|---|---|
| 11_OFFTAKER | Répartition des achats, garantie de paiement en mois de facturation |
| 12_UTILITY | Modèle de trésorerie simplifié de la compagnie d'électricité, paiement maximal soutenable au titre du CAE, écart de paiement, scénario contrefactuel sans projet |

**Régulation, CAE, tarif et recettes (13 à 16)**

| Feuille | Objet |
|---|---|
| 13_REGULATION | Matrice de maturité réglementaire (16 éléments) et données d'entrée de maturité environnementale et sociale (E&S) |
| 14_PPA | Redevances de capacité et d'énergie, indexation, part en devises, énergie réputée livrée, take-or-pay, prime de résiliation |
| 15_TARIFF | Tarif indexé, tarif moyen pondéré, ligne du LCOE, marge d'accessibilité tarifaire |
| 16_REVENUE | Énergie payée, recettes facturées, affectation du déficit de la compagnie d'électricité, recettes encaissées, recettes du cas des prêteurs, qualité des recettes |

**Financement (17 à 21, avec 17A)**

| Feuille | Objet |
|---|---|
| 17_PROJECT_FINANCE | Base de financement, ressources et emplois, capacité d'endettement, besoin de financement non couvert, principaux résultats |
| 17A_STRUCTURES | Cinq structures pour le même projet, comparaison en temps réel par formules fermées, instantané du moteur complet |
| 18_DEBT | Données d'entrée du mode figé, facteurs d'intérêts intercalaires (IDC) en formule fermée, flux de trésorerie disponibles pour le service de la dette (CFADS) du cas des prêteurs, sculptage, deux tranches, cible du DSRA |
| 19_EQUITY | Totaux des fonds propres, rendements par détenteur, valeur terminale des fonds propres privés |
| 20_CASH_FLOW | Financement de la construction, cascade des flux d'exploitation, mouvements du DSRA, distributions, flux de trésorerie des fonds propres, séries du LCOE |
| 21_TAX | Amortissements, report des déficits, exonération fiscale temporaire, impôt hors effet de levier |

**Finances publiques (22 à 26)**

| Feuille | Objet |
|---|---|
| 22_GOVERNMENT_SUPPORT | Exposition directe de l'État en trésorerie |
| 23_GUARANTEES | Exposition par instrument, année par année |
| 24_CONTINGENT_LIABILITIES | Exposition simultanée maximale, appels déterministes, perte attendue |
| 25_FISCAL_IMPACT | Flux budgétaire net, VAN budgétaire centrale et consolidée |
| 26_DEBT_SUSTAINABILITY | Filtre de l'exposition budgétaire au niveau du projet (pas une analyse de soutenabilité de la dette) |

**Scénarios et risques (27 à 29)**

| Feuille | Objet |
|---|---|
| 27_SCENARIOS | Tableau des cas, paramètres de stress, leviers effectifs, instantané des scénarios sur le moteur complet |
| 28_SENSITIVITY | Diagramme en tornade du LCOE en temps réel par formules fermées, instantané des sensibilités sur le moteur complet |
| 29_RISK_ALLOCATION | 16 risques face à 8 parties, possibilité d'atténuation et instruments |

**Portes, résultats et assurance qualité (30 à 35)**

| Feuille | Objet |
|---|---|
| 30_BANKABILITY | Filtre de bancabilité à neuf portes pour la phase de développement, notation selon le maillon le plus faible, actions classées par priorité |
| 30A_CLOSE_READINESS | 23 portes de bouclage financier, la preuve d'abord ; échelle de décision ; synthèse par question du cadre |
| 31_CASE_STUDY | Kasiri comparé à 15 cas de référence publics (coût unitaire tel que publié, sans ajustement) |
| 32_DASHBOARD | Résultats principaux pour le projet, le financement, le développeur, le système électrique, la compagnie d'électricité et les finances publiques ; les deux niveaux de portes ; les cinq principaux écarts et actions ; quatre graphiques |
| 33_CHECKS | 14 contrôles d'intégrité |
| 34_FRAMEWORK_MAP | Chacune des 23 portes rattachée à sa question, à la partie qui l'accepte, à la feuille du modèle, à l'indicateur et aux chapitres du livre ; le filtre à neuf portes rattaché aux questions |
| 35_BOOK_CHECK | Modèle en temps réel comparé aux chiffres du cas Kasiri imprimés dans le Livre 7 |

---

## 4. Prise en main rapide (15 minutes) sur le cas Kasiri

Ouvrez le classeur avec les données d'entrée par défaut. S'il a été enregistré en dernier par LibreOffice, exécutez `tools/model/excel_quote_fix.py` sur ce fichier avant de l'ouvrir dans Excel (section 7.6).

**Étape 1. Vérifier les valeurs par défaut (2 minutes).** Sur *01_CONTROL_PANEL* :

| Donnée d'entrée | Valeur par défaut | Signification |
|---|---|---|
| `case` | 1 | Cas de base |
| `gen_case` | 1 | P50 dans les flux de trésorerie |
| `lender_case` | 4 | Dette dimensionnée sur le P90 à dix ans |
| `structure` | 2 | PIE (IPP, BOOT privé) |
| `debt_mode` | 1 | Dette sculptée dans le modèle |
| `backstop` | 1 | Le budget couvre tout déficit de la compagnie d'électricité au titre du CAE |
| `bs_share` | 100 % | Part du déficit couverte par le budget |
| Neuf commutateurs de stress | 0 | Aucun stress |
| Cinq variations de sensibilité | 0 % | Aucune sensibilité |

Sur *05A_CONTRACTING*, `epc_struct` = 2 (lots séparés de génie civil et d'équipements électromécaniques).

**Étape 2. Confirmer l'intégrité (1 minute).** *33_CHECKS* doit afficher ALL OK (tous les contrôles corrects) et *35_BOOK_CHECK* ALL PASS (tous les contrôles réussis). Ne lisez aucun résultat tant que ces deux conditions ne sont pas réunies.

**Étape 3. Lire le tableau de bord (4 minutes).** La ligne 4 de *32_DASHBOARD* donne les trois verdicts : le filtre à neuf portes affiche NOT BANKABLE (non bancable : un écart critique doit être comblé), la maturité pour le bouclage selon les 23 portes affiche *"STOP: a critical gate is not met"* (arrêt : une porte critique n'est pas franchie) et le filtre budgétaire affiche *"LOW additional fiscal pressure"* (pression budgétaire supplémentaire faible). Les blocs situés en dessous présentent :

| Bloc | Valeurs du cas de base |
|---|---|
| Projet | 60 MW ; P50 292 GWh ; facteur de charge 55,6 % ; coût de la centrale 156,9 M USD en termes réels ; 2 614 USD/kW ; mise en service commerciale 2030 ; tarif moyen pondéré en 2e année d'exploitation 117,8 USD/MWh ; LCOE de la centrale 105,9 USD/MWh ; LCOE du système livré 108,1 USD/MWh |
| Financement | TRI du projet 11,2 % ; TRI des fonds propres privés 13,8 % (cible 15,0 %) ; VAN du projet 16,3 M USD ; DSCR minimum 1,53x ; DSCR moyen 1,60x ; LLCR 1,59x ; capacité d'endettement 147,8 M USD ; dette levée 145,4 M USD ; besoin de financement non couvert 4,1 M USD |
| Développeur | Budget 9,0 M USD en termes réels sur 6,0 ans ; probabilité de bouclage 14,6 % ; VAN pondérée par le risque -0,95 M USD ; TRI sur le scénario de succès 16,0 % ; multiple de trésorerie 4,97x ; prime au point mort 18,9 % du coût de la centrale ; revalorisation des fonds propres entre le bouclage et la mise en service commerciale 18,3 M USD |
| Système électrique | Aucun écart sur le transport ; capacité d'évacuation de 120 MW à la mise en service commerciale ; 3,3 % de la pointe du système ; aucun écrêtement |
| Compagnie d'électricité | Taux de recouvrement 88 % ; délai de recouvrement des créances d'environ 120 jours ; capacité de paiement égale à 5,96 fois la facture du CAE la plus défavorable des dix premières années ; aucun écart de paiement |
| Finances publiques | Aucune contribution initiale ; exposition éventuelle maximale 225,4 M USD (0,56 % du PIB) ; valeur actuelle de la perte attendue 20,4 M USD ; VAN budgétaire de 34,8 M USD (centrale) et de -27,6 M USD (consolidée) |
| 23 portes | 6 portes franchies sur 23 ; 7 portes critiques non franchies |

Les listes des cinq premiers classent les neuf portes du filtre par score : porte 6 (écart critique), portes 1 et 5 (écarts de développement), puis portes 3 et 7.

**Étape 4. Comprendre pourquoi la décision de bouclage est STOP (2 minutes).** Sur *30A_CLOSE_READINESS*, les sept portes critiques non franchies sont les portes 1 (série de débits et revue), 3 (validation de l'étude de faisabilité bancable), 5 (EIES conforme aux normes des prêteurs), 8 (droits fonciers), 15 (six mois de garantie de paiement), 17 (plan de financement engagé) et 19 (TRI des fonds propres à la cible). La synthèse par question en bas de la feuille, reprise sur le tableau de bord, montre quelle partie attend quoi.

**Étape 5. Stresser la rivière (2 minutes).** Mettez `st_drought` à 1. Le dimensionnement de la dette ne change pas, car le cas des prêteurs exclut par construction la fenêtre de sécheresse (section 6.9). Le DSCR minimum passe sous 1,0 (instantané : 0,69x, avec tirage sur le DSRA) et le déficit des années de sécheresse apparaît sur *20_CASH_FLOW*. Remettez-le à 0.

**Étape 6. Stresser l'acheteur (2 minutes).** Mettez `st_offtaker` à 1. La capacité de paiement tombe à zéro en moins de dix ans ; avec la garantie budgétaire activée, le projet est payé intégralement et le coût est transféré au budget (instantané : VAN budgétaire consolidée d'environ -125 millions USD). Mettez ensuite `backstop` à 0 : la garantie du CAE de douze mois est épuisée, le reste devient des arriérés dus au projet et le DSCR minimum devient négatif (instantané : -0,53x). Remettez les deux paramètres à leurs valeurs par défaut.

**Étape 7. Comparer les structures (2 minutes).** Mettez successivement `structure` à 1, 3, 4 et 5 et lisez *17A_STRUCTURES*, le tableau de bord et *30A_CLOSE_READINESS*. Remettez-la à 2. Dès qu'une valeur s'écarte des valeurs par défaut, *35_BOOK_CHECK* affiche des lignes CHECK (à vérifier) ; c'est normal.

---

## 5. Parcours par utilisateur

Chaque parcours part de la question du cadre à laquelle l'utilisateur doit répondre et désigne les feuilles qui y répondent. Tous les utilisateurs doivent terminer sur *33_CHECKS* (ALL OK) et consigner les données d'entrée qu'ils ont modifiées.

### 5.1 Développeur (Q1, Q2, Q4, avec Q6)

1. Remplacez l'hydrologie sur *03_HYDROLOGY* (débits mensuels, hauteur de chute, débit d'équipement, rendements, débit réservé, disponibilité, coefficient de variation (CV), longueur de la série, maturité de l'étude). Q1 dépend de `rec_years` et de `hyd_study`.
2. Remplacez la décomposition des coûts sur *05_PLANT_CAPEX* et choisissez la structure contractuelle sur *05A_CONTRACTING*.
3. Saisissez les six étapes sur *01A_DEVELOPMENT* (durée, budget réel, probabilité de succès) et les conditions du développeur (prime, participation, taux d'actualisation, part cédée).
4. Lisez la section D : la VAN pondérée par le risque indique s'il faut se lancer ; la VAN sur le scénario de succès indique si le projet crée de la valeur, même s'il atteint le bouclage ; la prime et la probabilité au point mort indiquent ce qui justifierait de se lancer. Si la VAN sur le scénario de succès est négative, la probabilité au point mort affiche *"n/a: negative on the success path"* (sans objet : négative sur le scénario de succès) ; corrigez la valeur au bouclage (tarif, prime, coût) avant de dépenser pour améliorer les probabilités.
5. Lisez la section F : TRI sur le scénario de succès, multiple de trésorerie et pic de trésorerie à risque.
6. Utilisez `fx_tariff` sur *01_CONTROL_PANEL* pour trouver le tarif qui porte le TRI des fonds propres à la cible de *17A_STRUCTURES* (`str_hurdle`) et comble le besoin de financement non couvert. Vérifiez l'effet sur la compagnie d'électricité (*12_UTILITY*) et sur la VAN budgétaire consolidée (*25_FISCAL_IMPACT*).
7. Saisissez sur *30A_CLOSE_READINESS* les statuts de preuve des portes sans test automatique et conservez la référence du document en colonne G.

### 5.2 Co-développeur (Q4, Q2)

1. Identifiez l'étape à laquelle vous entreriez. La section D2 de *01A_DEVELOPMENT* donne, pour chaque étape sur le point de commencer, la probabilité de bouclage à partir de ce point (colonne B), la valeur actuelle de la valeur au bouclage (C), la valeur actuelle des dépenses restantes (D) et la valeur pondérée par le risque de l'ensemble de la position (E).
2. Fixez le prix d'entrée à partir de la colonne E à votre étape, jamais à partir des coûts irrécupérables du développeur. Pour Kasiri au début de la phase des permis (étape 4) : probabilité de bouclage 57,8 %, valeur actuelle de la valeur au bouclage 3,34 millions USD, valeur actuelle des dépenses restantes 2,06 millions USD, valeur de la position 1,28 million USD.
3. Le Livre 7 (chapitre 18) calcule la part équitable d'un co-développeur qui finance toutes les dépenses restantes comme la colonne D divisée par la colonne C à l'étape d'entrée, soit environ 62 % pour Kasiri à l'étape 4. Relancez le calcul avec votre propre taux d'actualisation (`dev_rate`) et vos propres probabilités.
4. Testez les leviers utilisés par le livre (exécutions de l'instantané *"Dev: ..."*) : taux d'actualisation du développement, prime, probabilités par étape, subvention pour l'étape de faisabilité, tarif.

### 5.3 Prêteur ou IFD (Q5, avec Q1 et Q6)

1. Choisissez le cas des prêteurs sur *01_CONTROL_PANEL* : `lender_case` 1 (P50), 2 (P75), 3 (P90 à un an) ou 4 (P90 à dix ans, valeur par défaut). Conservez `gen_case` = 1 pour la vision du promoteur, ou mettez-le à 3 pour voir le P90 dans chaque année des flux de trésorerie.
2. Lisez *18_DEBT* (CFADS du cas des prêteurs, sculptage, tranches) et *17_PROJECT_FINANCE* (capacité d'endettement, contrainte déterminante, taux d'endettement (gearing), ratios). Pour Kasiri, c'est le plafond du taux d'endettement qui est déterminant : dette de 145,4 millions USD pour une capacité sculptée de 147,8 millions USD.
3. Figez le montage avant de le stresser. Mettez `debt_mode` = 2 après avoir saisi les valeurs du cas de base de `debt_m`, `debt_c`, `s_grant` et `s_goveq` dans les cellules C6 à C9 de *18_DEBT*, ainsi que le principal commercial du cas de base par année d'exploitation à la ligne 12 (colonne E = année d'exploitation 1). Les valeurs livrées dans ces cellules (90 millions USD et un échéancier nul) sont des valeurs provisoires, et non le cas de base ; avec un échéancier nul, la dette commerciale est remboursée en une seule échéance in fine (balloon) et le contrôle de l'échéance in fine sur *33_CHECKS* affiche WARNING (avertissement). L'exécuteur de l'instantané remplit automatiquement ces données d'entrée dans ses propres copies.
4. Lancez les stress un par un, puis combinés (section 7). Lisez le DSCR minimum, le LLCR, le déficit cumulé de service de la dette (`kpi_short`), les mouvements du DSRA sur *20_CASH_FLOW* et le besoin de financement non couvert.
5. Vérifiez les portes 17, 18, 20 et 23 sur *30A_CLOSE_READINESS* et les portes 1, 4, 5 et 7 du filtre sur *30_BANKABILITY*.

### 5.4 Ministère des Finances ou cellule PPP (Q7, avec Q3)

1. Remplacez les données pays sur *26_DEBT_SUSTAINABILITY* par les dernières données publiées des analyses de soutenabilité de la dette (DSA) du FMI et de la Banque mondiale, et fixez les quatre seuils du filtre selon votre politique de gestion des risques budgétaires.
2. Saisissez vos propres probabilités d'appel et pertes en cas d'appel sur *24_CONTINGENT_LIABILITIES*. Ce sont des jugements, pas des prévisions.
3. Choisissez la structure sur *01_CONTROL_PANEL* et lisez *22_GOVERNMENT_SUPPORT* (trésorerie directe), *23_GUARANTEES* (exposition par instrument), *24_CONTINGENT_LIABILITIES* (exposition simultanée maximale, appels, perte attendue), *25_FISCAL_IMPACT* (VAN budgétaire centrale et consolidée, besoin de trésorerie maximal) et *26_DEBT_SUSTAINABILITY* (filtre).
4. Testez l'affectation d'un déficit avec `st_offtaker`, `backstop` et `bs_share`, et le montant de la garantie du CAE avec `ppag_months` sur *23_GUARANTEES*.
5. Utilisez la VAN budgétaire consolidée comme indicateur principal pour le secteur public : elle intègre la compagnie publique d'électricité au moyen du scénario contrefactuel sans projet.
6. La porte 21 de *30A_CLOSE_READINESS* est franchie quand le filtre n'affiche pas HIGH (élevé) ; l'approbation du ministère elle-même est une preuve à consigner en dehors du modèle.

### 5.5 Compagnie d'électricité (Q7, Q3)

1. Remplacez les données d'entrée de *12_UTILITY* par des chiffres audités : clients, tarif, répercussion des coûts, pertes techniques et commerciales, recouvrement, coût des autres sources d'approvisionnement et sa part en USD, coûts d'exploitation, transferts, service de la dette existante, créances.
2. Remplacez la demande par segment et les autres sources d'approvisionnement sur *10_DEMAND*, ainsi que les données du système sur *09_GRID*.
3. Lisez le paiement maximal soutenable au titre du CAE comparé à la facture du CAE, le ratio de capacité de paiement, la demande non satisfaite, le DSCR de la compagnie sur sa dette existante, le délai de recouvrement des créances et la trésorerie supplémentaire générée par le projet (`f_soe`).
4. Sur *15_TARIFF*, comparez le tarif moyen pondéré du CAE avec les recettes encaissées par MWh injecté. Une marge négative signifie que chaque MWh acheté coûte de la trésorerie à la compagnie.

### 5.6 Conseiller en transaction (Q8)

1. Parcourez la chaîne dans l'ordre du livre et tenez un journal de chaque donnée d'entrée modifiée et de sa source.
2. Exécutez le moteur complet avec `tools/run_snapshots.py` (section 7.5) pour obtenir les tableaux des scénarios, des structures, des sensibilités, des structures contractuelles et du développeur, le tarif requis par structure et le débit au point mort.
3. Utilisez *29_RISK_ALLOCATION* pour convenir de qui porte quoi, *30_BANKABILITY* pour la liste d'actions de la phase de développement, et *30A_CLOSE_READINESS* avec *34_FRAMEWORK_MAP* pour transformer les portes ouvertes en un programme de travail par partie.
4. Avant toute note destinée à un comité, confirmez que *33_CHECKS* affiche ALL OK et consignez l'horodatage de l'instantané.

---
## 6. Méthodologie et formules clés

Les formules sont reprises de `model/build_model.py`, en remplaçant les références du gabarit par les noms de cellules simples du modèle. Un nom tel que `p50` est celui utilisé dans `model/model_map.json`. Dans une formule de série chronologique, « ligne » désigne la valeur de la même année.

### 6.1 Hydrologie et valeurs P (03_HYDROLOGY)

Débits moyens mensuels de long terme (janvier à décembre, m³/s) : 24, 20, 28, 52, 70, 58, 40, 28, 22, 30, 46, 36. Février compte 28,25 jours, l'année compte donc 365,25 jours. Pour chaque mois :

```
usable flow = MIN(MAX(flow-eflow,0),q_design)
power (MW)  = MIN(rho*grav*usable*head*eta_t*eta_g/1000000,inst_mw)
energy gross= power*days*24/1000
energy net  = energy gross*avail
spill       = MAX(flow-eflow-q_design,0)
```

Statistiques annuelles :

```
p50    = sum of monthly net energy
p75    = p50*(1-z75*cv)                 z75 = 0.6745
p90    = p50*(1-z90*cv)                 z90 = 1.2816 (one-year P90)
p90_10 = p50*(1-z90*cv*SQRT((1+rho1)/(1-rho1)/10))
cf     = p50/(inst_mw*8.76)
firm_mw= lowest monthly power*avail
```

Le P90 à dix ans est le P90 de l'énergie moyenne sur dix ans. La corrélation d'une année sur l'autre `rho1` (0,3 par défaut) traduit la persistance des années sèches : elle augmente la variance de la moyenne par le facteur (1+ρ)/(1−ρ)/n. Avec un coefficient de variation de 15 %, les valeurs de Kasiri sont : P50 292,5 GWh, P75 262,9, P90 à un an 236,3 et P90 à dix ans 268,3 GWh ; le rapport P90/P50 est de 0,81 et le facteur de charge de 55,6 %. La ligne de contrôle « puissance théorique au débit d'équipement » (*« theoretical power at design flow »*, 60,5 MW) doit être au moins égale à la puissance installée.

La feuille signale que l'énergie calculée à partir des débits moyens mensuels de long terme surestime la production lorsque, certaines années, les débits dépassent le débit d'équipement ; il faut la remplacer par une simulation sur l'ensemble de la série de débits lorsqu'elle existe.

### 6.2 Énergie (04_GENERATION)

```
p_sel     = CHOOSE(gen_case,p50,p75,p90)
p_len     = CHOOSE(lender_case,p50,p75,p90,p90_10)
drought   = IF(AND(st_drought=1,opyr>=p_drought_start,opyr<p_drought_start+p_drought_len),p_drought,1)
climate   = (1+eff_climate)^((year-base_year)/10)
rampf     = IF(opyr=1,ramp,1)
gen       = opflag*p_sel*eff_flow*drought*climate*rampf
gen_p50   = opflag*p50*eff_flow*climate*rampf
evacuable = gen*evac_ratio
delivered = MIN(evacuable,d_absorb)
gen_len   = opflag*p_len*eff_flow*climate*rampf
```

Le modèle distingue l'énergie installée, disponible, produite, évacuable, livrée et contractée. L'écrêtement dû au transport ou au réseau est `gen-evacuable` ; l'écrêtement dû à l'insuffisance de la demande est `evacuable-delivered`. L'énergie contractée est la référence P50 `gen_p50`. La production du cas prêteurs `gen_len` n'intègre pas le facteur de sécheresse : la sécheresse est testée à part.

Le ratio d'évacuation provient de *09_GRID* :

```
peak       = peak0*d_dom/base-year domestic demand
absorb_mw  = MAX(0,peak*minload-mustrun)+ic_mw
line_mw    = IF(tx_ready=1,tx_mw,tx_interim)
evac_mw    = MIN(line_mw,absorb_mw)
evac_ratio = MIN(1,evac_mw/inst_mw)
```

Sur *10_DEMAND*, la demande croît par segment au taux de croissance du cas, augmenté de `eff_demg`, et elle est multipliée par `eff_dem` à partir de la date de mise en service commerciale (COD). L'énergie du projet absorbable est égale au déficit d'offre, plus la production thermique substituable, plus les exportations contractées. La demande bancable est `opflag*MIN(contracted,absorbable*commercial/(domestic+exp_con))` ; le plus faible rapport entre demande bancable et demande contractée sur les années d'exploitation 1 à 5 alimente la porte 2.

### 6.3 Construction du coût d'investissement (05_PLANT_CAPEX, 06_CONSTRUCTION, 08_TRANSMISSION)

Coût de la centrale en USD constants de 2026 :

| Poste | Kasiri (M USD) | Formule ou source |
|---|---|---|
| Génie civil | 68,0 | Donnée d'entrée |
| Équipements hydromécaniques | 9,0 | Donnée d'entrée |
| Équipements électromécaniques | 33,0 | Donnée d'entrée |
| Environnement et social | 5,0 | Donnée d'entrée |
| Ingénierie et supervision | 8,0 | Donnée d'entrée |
| Coûts du maître d'ouvrage | 4,0 | Donnée d'entrée |
| Coûts de développement remboursés au bouclage | 9,0 | `cx_dev = dev_total` depuis *01A_DEVELOPMENT* |
| Prime de risque de l'entrepreneur | 6,6 | `cx_epcprem = (cx_civil+cx_hm+cx_em)*epc_prem` |
| Sous-total | 142,6 | Somme |
| Provision pour aléas physiques 10 % | 14,3 | `capex_base = cx_sub*(1+cont)` |
| Coût de base de la centrale | 156,9 | 2 614 USD/kW ; 1,04 fois la référence de 2 515 USD/kW |

Le coût effectif de la centrale applique le cas, le stress de dépassement de coûts, la part des dépassements et des coûts de retard supportée par le maître d'ouvrage, ainsi que l'ajustement (flex) :

```
eff_capex  = case_capex*(1+st_capex*p_overrun*epc_owner)*(1+fx_capex)
capex_real = capex_base*eff_capex*(1+delay_cost*eff_delay*epc_owner_d)
```

L'échelonnement suit une courbe en S sinusoïdale sur la durée effective de construction N, dont la somme vaut exactement un quel que soit N, avec une indexation au taux `capex_esc` :

```
share_t   = IF(consflag=1,SIN(PI()*(t-0.5)/N)*SIN(PI()/(2*N)),0)
capex_nom = capex_real*share*escidx       escidx = (1+capex_esc)^(year-base_year)
```

Le coût de transport est `(tx_km*tx_cost_km+tx_sub+tx_reinf)*eff_capex` (16,7 millions USD constants pour Kasiri), dépensé sur `tx_build` années avant la date prévue de mise en service de la ligne, avec une pénalité de retard `(1+delay_cost*eff_tdelay)` répartie sur `tx_build+eff_tdelay` années. `tx_party` = 1 met la dépense à la charge de l'État, 2 à la charge du projet. La date de mise en service de la ligne est `start_year+cons_years+tx_lag+eff_tdelay` ; l'écart de préparation est la date de mise en service de la ligne moins la COD de la centrale.

### 6.4 Contractualisation de la construction (05A_CONTRACTING)

`epc_struct` sélectionne une colonne de paramètres indicatifs :

| Paramètre | 1 EPC clés en main | 2 Lots séparés | 3 Multicontrats |
|---|---|---|---|
| Prime de l'entrepreneur sur le génie civil, l'hydromécanique et l'électromécanique (`epc_prem`) | 12 % | 6 % | 0 % |
| Part d'un dépassement de coûts supportée par le maître d'ouvrage (`epc_owner`) | 30 % | 55 % | 90 % |
| Part du coût de retard supportée par le maître d'ouvrage après pénalités forfaitaires (`epc_owner_d`) | 35 % | 60 % | 90 % |
| Risque d'interface (1 faible à 3 élevé) | 1 | 2 | 3 |

La prime entre dans le coût de base ; les parts du maître d'ouvrage modulent les stress de dépassement et de retard dans `eff_capex` et `capex_real`. Un contrat clés en main coûte donc plus cher dans le cas de base et moins cher en cas de dépassement. Les simulations figées (snapshot) *« EPC 1/2/3 base »* et *« EPC 1/2/3 overrun 96% »* comparent les trois structures, la dette étant redimensionnée pour chacune.

### 6.5 Coûts d'exploitation (07_OPEX)

Les données d'entrée en termes réels sont indexées sur l'indice des prix à la consommation américain (US CPI) :

```
o_fix  = opflag*om_fix*eff_opex*uscpi
o_var  = gen*om_var*eff_opex*uscpi/1000
o_ins  = opflag*capex_real*ins*uscpi
o_mmr  = opflag*capex_real*mmr*uscpi
o_oth  = opflag*om_other*eff_opex*uscpi
o_txprj= IF(tx_party=2,tx_omc,0)+tx_wheelc
opex   = o_fix+o_var+o_ins+o_mmr+o_oth+o_txprj
o_roy  = delivered*royalty*uscpi/1000        (water royalty, paid to government)
```

La réserve pour gros entretien est comptée comme un coût d'exploitation, et non comme un compte de réserve distinct.

### 6.6 CAE, tarif et revenus (14_PPA, 15_TARIFF, 16_REVENUE)

Le tarif de Kasiri rémunère uniquement l'énergie : paiement de capacité nul, prix de l'énergie de 112 USD/MWh (2026), indexé pour moitié sur l'US CPI, entièrement libellé en USD, avec paiement de l'énergie réputée livrée en cas d'écrêtement non imputable au vendeur.

```
fxfac   = (1-lc_share)+lc_share*lccpi/fxidx/uscpi
capc    = cap_chg*((1-cap_idx)+cap_idx*uscpi)*fxfac*eff_tariff
enc     = en_chg*((1-en_idx)+en_idx*uscpi)*fxfac*eff_tariff
deemed  = deemed flag*(curt_tx+curt_dem)
topshort= MAX(0,top*contracted-delivered-deemed)
epaid   = delivered+deemed+topshort
rev_cap = opflag*capc*inst_mw*12/1000*avail_ratio*rampf
rev_en  = enc*delivered/1000
rev_deem= enc*(deemed+topshort)/1000
rev_bill= rev_cap+rev_en+rev_deem
```

Le défaut de paiement de la compagnie d'électricité est couvert par trois mécanismes successifs :

```
cov_backstop = IF(backstop=1,u_gap*bs_share,0)
ppag_lim     = str_ppag*ppag_months/12*rev_util
ppag_reimb   = opflag*MIN(previous ppag_out,MAX(0,u_maxppa-u_ppa))
cov_guar     = MIN(u_gap-cov_backstop,MAX(0,ppag_lim-previous ppag_out+ppag_reimb))
ppag_out     = previous ppag_out+cov_guar-ppag_reimb
unpaid       = u_gap-cov_backstop-cov_guar
rev_cash     = rev_bill-unpaid
```

La garantie est plafonnée à `ppag_months` mois de facturation de la compagnie d'électricité (12 par défaut) et la compagnie la rembourse sur sa capacité de paiement excédentaire ; tout montant au-delà devient un arriéré envers le projet.

Les revenus du cas prêteurs utilisent le cas de production des prêteurs :

```
rev_len = rev_cap+enc*IF(deemed=1,gen_len,MIN(gen_len*evac_ratio,d_absorb))/1000
```

Indicateurs de qualité des revenus : part fixe des revenus facturés (`rev_fixed`, 0 % pour Kasiri), revenus à risque entre P50 et P90 la 2e année d'exploitation, part des revenus provenant de la compagnie d'électricité, et soutien nécessaire sur la durée de vie pour maintenir les paiements au titre du CAE. Sur *15_TARIFF*, la marge d'accessibilité tarifaire est égale aux revenus encaissés par la compagnie d'électricité par MWh injecté, moins le tarif moyen pondéré du CAE.

### 6.7 Module de développement (01A_DEVELOPMENT)

**Étapes.** Six étapes, chacune avec sa durée, son budget en termes réels et sa probabilité de succès jusqu'à l'étape suivante :

| Étape | Mois | Budget (M USD constants) | P(succès) |
|---|---|---|---|
| 1 Identification du site et reconnaissance | 6 | 0,10 | 60 % |
| 2 Préfaisabilité et début du jaugeage des débits | 12 | 0,60 | 60 % |
| 3 Étude de faisabilité, EIES, études géotechniques et de réseau | 18 | 4,50 | 70 % |
| 4 Licences, droits d'eau, foncier et permis | 12 | 0,80 | 85 % |
| 5 CAE, convention de mise en œuvre et approbation du tarif | 12 | 0,80 | 80 % |
| 6 Financement : conseillers, juristes, assurances, bouclage | 12 | 2,20 | 85 % |
| Total | 72 | 9,00 | 14,6 % |

```
dev_total = sum of budgets
dev_years = sum of months/12
dev_pfc   = PRODUCT(p1:p6)
dev_pct   = dev_total/capex_real
```

**Profil de dépenses.** Les étapes s'enchaînent sans interruption et s'achèvent au bouclage financier. Le budget de chaque étape est réparti uniformément sur ses mois et affecté aux dix colonnes d'années de développement précédant le bouclage (2017 à 2026), puis indexé par `(1+us_cpi)^(year-base_year)`. Pour Kasiri, les dépenses courent de 2021 à 2026 et totalisent 8,6 millions USD courants.

**P(en vie).** Pour chaque année de développement, la probabilité que le projet soit encore en vie au moment de la dépense est la moyenne, pondérée par les dépenses de chaque étape, de la probabilité d'atteindre cette étape, `PRODUCT(p1:pk)/pk`.

**VAN pondérée par le risque.** Avec r = `dev_rate` (25 %) et toutes les valeurs actuelles calculées au début du développement :

```
dev_reimb        = total nominal development spend
dev_prem         = dev_prem_pct*capex_real
dev_eq_npv_fc    = dev_stake*NPV(r_fc,eq_priv_cf)
dev_success_value= dev_reimb+dev_prem+dev_eq_npv_fc
dev_pv_cost_unw  = NPV(r,spend)*(1+r)^(10-dev_months/12)
dev_pv_cost_rw   = SUMPRODUCT(spend,P(alive),1/(1+r)^column)*(1+r)^(10-dev_months/12)
dev_pv_success   = dev_success_value/(1+r)^(dev_months/12)
dev_npv_success  = dev_pv_success-dev_pv_cost_unw
dev_enpv         = dev_pfc*dev_pv_success-dev_pv_cost_rw
```

Kasiri : valeur au bouclage sur le scénario de succès de 11,27 millions USD ; VAN sur le scénario de succès de -1,00 million USD ; VAN pondérée par le risque de -0,95 million USD.

**Prime et probabilité de point mort.**

```
dev_be_prem = MAX(0,dev_prem-dev_enpv*(1+r)^(dev_months/12)/dev_pfc)
dev_be_p    = IF(dev_npv_success<=0,"n/a: negative on the success path",dev_pv_cost_rw/dev_pv_success)
```

Kasiri a besoin d'une prime de 29,7 millions USD (18,9 % du coût de la centrale) pour obtenir une VAN pondérée par le risque nulle, et n'a pas de probabilité de point mort, car le scénario de succès lui-même détruit de la valeur à 25 %.

**Valeur par étape (section D2).** Pour l'étape k sur le point de commencer, avec des budgets réels c, des durées d et un mois de début s :

```
B (P close from here) = PRODUCT(pk:p6)
C (PV value at close) = B*dev_success_value/(1+r)^((dev_months-s_k)/12)
D (PV remaining spend)= sum over j>=k of c_j*PRODUCT(pk:p(j-1))/(1+r)^((s_j-s_k+0.5*d_j)/12)
E (position value)    = C-D
```

| Étape sur le point de commencer | P(bouclage) | Valeur au bouclage | Dépenses restantes | Valeur de la position |
|---|---|---|---|---|
| 1 | 14,6 % | 0,43 | 1,63 | -1,20 |
| 2 | 24,3 % | 0,80 | 2,86 | -2,06 |
| 3 | 40,5 % | 1,67 | 4,84 | -3,17 |
| 4 | 57,8 % | 3,34 | 2,06 | 1,28 |
| 5 | 68,0 % | 4,91 | 1,98 | 2,93 |
| 6 | 85,0 % | 7,67 | 1,97 | 5,70 |

La VAN de la section D (dépenses courantes, année par année) et la valeur à l'étape 1 de la section D2 (budgets réels en milieu d'étape) répondent à la même question par deux voies différentes ; le Livre 7 utilise la première pour la décision de lancer le projet et la seconde pour fixer le prix d'entrée.

**Revalorisations (section E), fonds propres privés à 100 %.**

```
val_fc       = NPV(r_fc,eq_priv_cf)+NPV(r_fc,eq_priv_in)
val_step_fc  = NPV(r_fc,eq_priv_cf)
val_cod      = SUMPRODUCT(opflag,eq_priv_cf,1/(1+r_cod)^(t-cons_eff))/(1+r_fc)^cons_eff
val_step_cod = val_cod-SUMPRODUCT(opflag,eq_priv_cf,1/(1+r_fc)^t)
```

Kasiri : valeur créée au bouclage de -5,1 millions USD (le TRI des fonds propres est inférieur au taux de 15 % retenu au stade du bouclage) ; revalorisation liée à la réduction des risques entre le bouclage et la COD de 18,3 millions USD.

**Cession partielle (section F).**

```
v_cod_nom     = SUMPRODUCT(opflag,eq_priv_cf,1/(1+r_cod)^(t-cons_eff))
sell_proceeds = sell_pct*dev_stake*v_cod_nom
```

Le flux de trésorerie du développeur s'étend sur 50 colonnes (dix années de développement et les 40 années du modèle) : les dépenses de développement en négatif ; à t = 1, le remboursement plus la prime ; chaque année du modèle, `dev_stake` fois le flux de trésorerie des fonds propres privés, réduit de `(1-sell_pct)` pendant les années d'exploitation ; et le produit de cession la dernière année de construction. Kasiri : produit de cession de 19,5 millions USD, multiple de trésorerie de 4,97x, pic de trésorerie cumulée à risque de 10,2 millions USD.

**TRI du développeur avec trois valeurs de départ.**

```
dev_irr = IF(ISNUMBER(IRR(cf,0.15)),IF(ABS(IRR(cf,0.15))<1,IRR(cf,0.15),-1),
          IF(ISNUMBER(IRR(cf,0.05)),IF(ABS(IRR(cf,0.05))<1,IRR(cf,0.05),-1),
          IF(ISNUMBER(IRR(cf,-0.05)),IF(ABS(IRR(cf,-0.05))<1,IRR(cf,-0.05),-1),-1)))
```

Le flux de trésorerie du développeur change plusieurs fois de signe ; la valeur de départ a donc une importance. La formule essaie 15 %, puis 5 %, puis -5 %, et ne passe à la valeur suivante que si la précédente renvoie une erreur ; un résultat de valeur absolue supérieure ou égale à 1 est considéré comme aberrant et affiché à -1 (-100 %). Kasiri : 16,0 %. Les intéressements des promoteurs (promote) et le carried interest ne sont pas modélisés.

### 6.8 Structures de financement (17A_STRUCTURES)

La colonne C lit la structure sélectionnée dans les colonnes E à I avec `INDEX(E:I,structure)`.

| Paramètre | 1 Public | 2 PIE | 3 PPP | 4 Hybride | 5 Mixte |
|---|---|---|---|---|---|
| Fonds propres de l'État | 15 % | 0 % | 10 % | 0 % | 5 % |
| Subventions, financement de l'écart de viabilité (VGF), capital public | 0 % | 0 % | 5 % | 35 % | 8 % |
| Dette concessionnelle | 55 % | 0 % | 30 % | 25 % | 35 % |
| Plafond d'endettement (dette senior totale) | 85 % | 70 % | 75 % | 55 % | 72 % |
| Fonds propres privés maximum | 0 % | 35 % | 20 % | 25 % | 25 % |
| Apporteur des fonds propres résiduels | État | Privé | Privé | Privé | Privé |
| Dette senior garantie par l'État | 100 % | 0 % | 40 % | 20 % | 15 % |
| Dette senior comptabilisée en dette publique | 100 % | 0 % | 0 % | 0 % | 0 % |
| Garantie souveraine du CAE | Non | Oui | Oui | Oui | Oui |
| Obligation d'indemnité de résiliation | Non | Oui | Oui | Oui | Oui |
| Couverture du risque de convertibilité des devises | 0 % | 100 % | 100 % | 100 % | 50 % |
| Taux concessionnel / différé / durée | 2,0 % / 5 / 20 | 3,0 % / 5 / 20 | 3,0 % / 5 / 20 | 3,0 % / 5 / 20 | 2,5 % / 5 / 20 |
| Taux commercial / maturité | 7,5 % / 15 | 8,0 % / 16 | 7,5 % / 16 | 7,5 % / 16 | 7,2 % / 18 |
| DSCR de dimensionnement | 1,20 | 1,35 | 1,30 | 1,30 | 1,30 |
| TRI cible des fonds propres privés | 10 % | 15 % | 14 % | 14 % | 13 % |

Les pourcentages s'entendent en proportion de la base de financement. Conditions communes : DSCR de blocage des distributions (lock-up) de 1,10x, commissions de mise en place et d'engagement de 2 % de la dette senior, DSRA égal à six mois du service de la dette de l'année suivante. Un contrôle de structure vérifie que les subventions, les fonds propres de l'État, la dette maximale et les fonds propres privés maximum peuvent couvrir 100 % du besoin.

La comparaison analytique en temps réel est un filtre, elle ne remplace pas le moteur de calcul complet :

```
WACC     = (goveq+govx)*gov_disc+conc*rc+comm*rm+priv*hurdle/(1-tax_rate)
WACC_ex  = WACC/(1-grant)
CRF      = WACC_ex/(1-(1+WACC_ex)^-ops_years)
tariff   = (fund_base*(1+maxdebt*(idc_km+upfront_fee))*(1-grant)*CRF+opex_y2)/p50*1000
exposure = public capital+on-budget debt+MAX(guaranteed debt+PPA guarantee,termination)
```

où la dette commerciale est supposée égale au plafond d'endettement moins la dette concessionnelle. Les chiffres à citer sont ceux de la simulation figée du moteur complet sur la même feuille et du tarif requis calculé par le programme d'exécution pour les structures 2 à 5.
### 6.9 Dimensionnement de la dette (17_PROJECT_FINANCE, 18_DEBT)

**Assiette de financement et emplois.**

```
fund_base = u_capex+u_tx+u_devprem        (coût de la centrale en nominal, transport du projet pendant la construction, prime de développement)
uses      = fund_base+u_idc+u_fee+u_dsra
u_fee     = upfront_fee*(debt_c+debt_m)
```

Kasiri : 164,8 + 17,8 + 4,7 = assiette de financement de 187,3 ; intérêts intercalaires (IDC) 17,4 ; commissions 2,9 ; dotation initiale du compte de réserve du service de la dette (DSRA) 7,3 ; total des emplois 215,0.

**Facteurs d'IDC sous forme fermée.** La dette est tirée au prorata de la part de dépenses de la centrale, et les intérêts courent sur le solde d'ouverture augmenté de la moitié du tirage de l'année. Les IDC par dollar de chaque tranche sont donc une constante :

```
idc_kc = str_rc*SUMPRODUCT(consflag,cumsh-0.5*share)
idc_km = rm_eff*SUMPRODUCT(consflag,cumsh-0.5*share)
rm_eff = str_rm+eff_rate_add*(1-hedge)
```

Pour Kasiri, la somme vaut 1,5, d'où `idc_km` = 0,12.

**Flux de trésorerie disponibles pour le service de la dette (CFADS) du cas prêteurs et sculptage.** Le cas prêteurs retient l'impôt et l'amortissement hors effet de levier, sans IDC ni commissions, ce qui évite toute circularité dans le dimensionnement :

```
cfads_len = rev_len-opex-o_roy_len-IF(opyr>tax_hol,tax_rate*MAX(0,rev_len-opex-o_roy_len-dep_len),0)
inloan    = IF(AND(opyr>=1,opyr<=str_nm),1,0)
dfm       = IF(opyr>=1,1/(1+rm_eff)^opyr,0)
sculpt    = inloan*MAX(0,cfads_len/str_dscr-c_ds)
comm_cap  = SUMPRODUCT(sculpt,dfm)
```

Le service de la dette commerciale est sculpté sur le ratio de couverture du service de la dette (DSCR) cible, après le service de la dette concessionnelle, et la capacité d'emprunt est sa valeur actualisée au taux commercial, ramenée à la date de mise en service commerciale (COD).

**Plafond du taux d'endettement (gearing).** La dette senior totale ne peut dépasser le plafond multiplié par l'assiette de financement augmentée des IDC et commissions financés par la dette. En résolvant pour la dette commerciale, on obtient une forme fermée :

```
gearing amount = MAX(0,(str_maxdebt*(fund_base+debt_c*(idc_kc+upfront_fee))-debt_c)/(1-str_maxdebt*(idc_km+upfront_fee)))
debt_c (sized) = MIN(str_conc,str_maxdebt)*fund_base
debt_m (sized) = MIN(comm_cap,gearing amount)
```

Kasiri : montant au plafond de gearing 0,70 × 187,3 / (1 − 0,70 × 0,14) = 145,4, juste sous la capacité sculptée de 147,8 ; c'est donc le plafond de gearing qui s'applique. Le taux d'endettement rapporté au total des emplois est de 67,6 %.

**Mode verrouillé (`debt_mode` = 2).** Les subventions, les fonds propres de l'État et la dette concessionnelle prennent les valeurs verrouillées `lock_grant`, `lock_goveq` et `lock_c`. La dette commerciale vaut `MIN(lock_m,gearing amount)`, et son service de la dette cible suit l'échéancier de principal verrouillé par année d'exploitation, mis à l'échelle si le montant diffère :

```
m_target = IF(inloan=1,IF(debt_mode=1,IF(comm_cap>0,sculpt*debt_m/comm_cap,0),
           IF(lock_m>0,INDEX(lock_ds,1,opyr)*debt_m/lock_m,0)+m_int),0)
m_prin   = IF(inloan=1,MAX(0,MIN(m_open,IF(opyr=str_nm,m_open,m_target-m_int))),0)
```

Le taux n'est variable que sur la part non couverte, via `rm_eff`. Les fonds propres absorbent tout écart sur les emplois.

**Tranches.**

```
c_draw = debt_c*share       c_int = str_rc*(c_open+0.5*c_draw*consflag)
c_prin = IF(AND(opyr>str_gc,opyr<=str_gc+str_nc),MIN(c_open,debt_c/str_nc),0)
m_draw = debt_m*share       m_int = rm_eff*(m_open+0.5*m_draw*consflag)
ds     = c_ds+m_ds          c_ds, m_ds = opflag*(interest+principal)
idc    = consflag*(c_int+m_int)
```

**DSRA.** La cible est `IF(OR(opflag=1,lastcons=1),dsra_m/12*next-year ds,0)`. Le solde initial est financé à la fin de la construction par les fonds propres (il figure dans les emplois).

**Ratios.**

```
kpi_min_dscr = IF(COUNT(dscr)=0,99,MIN(dscr))
kpi_avg_dscr = IF(COUNT(dscr)=0,99,AVERAGE(dscr))
kpi_llcr     = SUMPRODUCT(cfads,dfw,inloan_all)/(debt_c+debt_m)
kpi_plcr     = SUMPRODUCT(cfads,dfm)/(debt_c+debt_m)
```

`dfw` actualise au taux senior pondéré ; `inloan_all` couvre la durée de la tranche la plus longue. La valeur 99 signifie qu'il n'y a pas de service de la dette.

### 6.10 Cascade des flux (20_CASH_FLOW)

**Financement de la construction.** Les emplois de chaque année sont le coût de la centrale, le transport du projet, les IDC, les commissions et la prime à t = 1, ainsi que la dotation initiale du DSRA. Les subventions et la dette sont tirées au prorata de la part de dépenses ; les fonds propres constituent le solde, réparti entre l'État et les actionnaires privés selon leurs parts.

**Exploitation.**

```
ebitda     = rev_cash-opex-o_roy
cfads      = opflag*(ebitda-tax-tx_spend_prj)
dscr       = IF(ds>0.001,cfads/ds,"")
avail0     = cfads-ds+cash_bf
dsra_draw  = opflag*MIN(previous dsra_act,MAX(0,-avail0))
dsra_relx  = opflag*MAX(0,previous dsra_act-dsra_draw-dsra_tgt)
dsra_top   = opflag*MIN(MAX(0,dsra_tgt-previous dsra_act+dsra_draw),MAX(0,avail0))
cash_avail = cfads-ds+dsra_draw+dsra_relx-dsra_top
shortfall  = MAX(0,-(cash_avail+cash_bf))
lock_ok    = IF(opflag=1,IF(ds>0.001,IF(dscr>=lockup,1,0),1),0)
pool       = cash_avail+cash_bf+shortfall
grepay     = IF(OR(lock_ok=1,opyr=ops_years),MIN(previous gclaim,MAX(0,pool)),0)
dist       = IF(OR(lock_ok=1,opyr=ops_years),MAX(0,pool-grepay),0)
cash_cf    = pool-grepay-dist
```

En cas d'insuffisance, le DSRA est mobilisé en premier ; il ne libère que son excédent au-delà de la cible et n'est reconstitué qu'à partir de la trésorerie disponible. L'insuffisance restante est couverte par la garantie souveraine (part `str_guar`) et par les promoteurs (le reste). La créance de l'État est remboursée sur la trésorerie ultérieure, avant les distributions. La trésorerie est bloquée quand le DSCR est inférieur au seuil de blocage (lock-up), puis libérée lors de la dernière année d'exploitation.

### 6.11 Impôt (21_TAX)

```
dep_base = fund_base+u_idc+u_fee-s_grant
dep      = IF(AND(opyr>=1,opyr<=dep_yrs),dep_base/dep_yrs,0)
taxable  = ebitda-dep-interest in operations
loss_use = IF(AND(taxable>0,opyr>tax_hol),MIN(taxable,loss_bf),0)
tax      = IF(opyr>tax_hol,tax_rate*MAX(0,taxable-loss_use),0)
tax_unlev= IF(opyr>tax_hol,tax_rate*MAX(0,ebitda-dep),0)
```

Les pertes sont reportées et ne sont pas imputées pendant l'exonération fiscale. L'impôt auquel l'État renonce du fait de l'exonération est indiqué (8,6 millions USD en nominal pour Kasiri).

### 6.12 Rentabilité (17_PROJECT_FINANCE, 19_EQUITY)

```
ucf      = -capex_nom-tx_spend_prj-premium at t=1+opflag*(ebitda-tax_unlev)
kpi_pirr = IFERROR(IRR(ucf,0.08),"n/a")
kpi_npv  = NPV(disc_rate,ucf)
kpi_eirr = IF(s_priv>0,IFERROR(IRR(eq_priv_cf,0.1),IFERROR(IRR(eq_priv_cf,-0.1),IFERROR(IRR(eq_priv_cf,-0.5),-1))),"n/a")
eq_priv_cf = -eq_priv_in+(dist-sf_eq)*(1-gov_eq_share)
lcoe     = NPV(disc_rate,lc_cost)/NPV(disc_rate,delivered+deemed)*1000
lcoe_sys = NPV(disc_rate,lc_cost_sys)/NPV(disc_rate,delivered*(1-tx_loss))*1000
```

`lc_cost` regroupe les dépenses de la centrale et du transport du projet, la prime, les charges d'exploitation (OPEX) et la redevance ; `lc_cost_sys` y ajoute les dépenses de transport public et leur exploitation et maintenance (O&M). La valeur actuelle nette (VAN) suit la convention d'Excel (le premier flux est actualisé d'une période).

Pour la résiliation, *19_EQUITY* calcule par récurrence à rebours la valeur des distributions privées restantes au taux de rendement interne (TRI) cible, `e_pvfwd = (next e_out+next e_pvfwd)/(1+str_hurdle)`, ainsi que les fonds propres privés non récupérés, `e_unrec = MAX(0,-cumulative private equity cash flow)`.

Le besoin de financement non couvert (écart de financement) correspond aux fonds propres privés requis au-delà de ceux qui sont disponibles :

```
priv_avail = str_privmax*fund_base
fin_gap    = IF(str_resid=1,MAX(0,s_priv-priv_avail),0)
```

Kasiri : fonds propres privés de 69,6 pour 65,6 disponibles, soit un écart de 4,1 millions USD (1,9 % des emplois).

### 6.13 Capacité de paiement de la compagnie d'électricité et scénario contrefactuel (12_UTILITY)

Le modèle de la compagnie d'électricité vérifie que l'acheteur peut payer, au lieu de le supposer.

**Bilan énergétique.** La demande adressée à la compagnie d'électricité est la demande intérieure, diminuée de la charge minière éventuellement desservie directement par le projet. Le projet fournit sa part destinée à la compagnie, nette des pertes de transport ; les autres approvisionnements sont plafonnés à l'offre disponible (`d_sup`) ; la demande au-delà de ce plafond n'est pas servie.

**Trésorerie et capacité.**

```
u_tar     = previous tariff*(1+lc_cpi*IF(AND(opyr>=1,opyr<=eff_freeze),0,ut_pt))
u_bill    = u_sales*u_tar/fx
u_collr   = MAX(0,MIN(1,ut_coll+IF(year>=cod_year,eff_coll_adj,0)))
u_subs    = ut_sub*IF(year>=cod_year,eff_sub,1)*lccpi/fxidx
u_opex    = -ut_opex*lccpi/fxidx*(0.5+0.5*u_sales/base-year demand)
u_supcost = -u_other*ut_supc*(ut_supusd*uscpi+(1-ut_supusd)*lccpi/fxidx)/1000
u_cash_pre= u_bill*u_collr+u_subs+u_opex+u_supcost-ut_ds
u_maxppa  = MAX(0,u_cash_pre)/ut_cov
u_gap     = opflag*MAX(0,u_ppa-u_maxppa)
u_ratio   = IF(u_ppa>0,u_maxppa/u_ppa,99)
```

`ut_ratio10` est le ratio le plus défavorable des années d'exploitation 1 à 10 (5,96 x pour Kasiri). Le taux de change vaut `fx0*(1+fx_dep)^(year-base_year)`, multiplié par `(1+eff_fxshock)` à partir de la COD.

**Scénario contrefactuel.** Le modèle recalcule la trésorerie de la compagnie d'électricité sans le projet (`u_cash_np`), celle-ci achetant alors aux autres sources dans la limite de leur plafond. La trésorerie supplémentaire de la compagnie publique est :

```
f_soe = u_cash_post-u_cash_np-unpaid
```

de sorte que les nouveaux arriérés sont comptés comme un coût pour le secteur public. Ce terme intègre la compagnie d'électricité dans la VAN budgétaire consolidée.

### 6.14 Soutien de l'État, garanties et passifs éventuels (22 à 24)

**Soutien direct** (*22_GOVERNMENT_SUPPORT*) : fonds propres de l'État, subventions, investissement et O&M du transport public, et garantie budgétaire couvrant l'insuffisance de paiement au titre du contrat d'achat d'électricité (CAE, PPA).

**Exposition par instrument** (*23_GUARANTEES*) :

```
x_debt  = (1-str_onbud)*str_guar*debt_bal
x_ppa   = str_ppag*ppag_months/12*rev_util
x_term  = str_term*(opflag+consflag>0)*(debt_bal+MAX(e_unrec*(1+term_prem),e_pvfwd))
x_fx    = str_fxg*(ds+e_out)
x_mrg   = opflag*MAX(0,mrg*rev_cap/MAX(0.0001,rampf)-rev_cash)
x_onbud = str_onbud*debt_bal
```

**L'exposition simultanée maximale** (*24_CONTINGENT_LIABILITIES*) évite d'additionner l'indemnité de résiliation et les garanties qu'elle remplacerait :

```
cl_max = MAX(x_term,x_debt+x_ppa+x_fx)
```

**Les appels déterministes** du scénario actif sont les appels de la garantie du CAE, les appels de la garantie de la dette (insuffisance multipliée par la part garantie) et les appels de la garantie de revenu minimum.

**La perte attendue** repose sur des probabilités fixées à dire d'expert par l'utilisateur et sur une perte en cas d'appel :

```
el = (pr_debt*x_debt+pr_ppa*MAX(0,x_ppa-cov_guar)+pr_term*MAX(0,x_term-x_debt))*lgd
cl_pv_el = SUMPRODUCT(el,gdf)          gdf = 1/(1+gov_disc)^t
```

Kasiri : exposition maximale de 225,4 millions USD, constituée pour l'essentiel de l'indemnité de résiliation ; valeur actualisée de la perte attendue de 20,4 millions USD avec les probabilités par défaut (2 %, 8 % et 0,5 % par an ; perte en cas d'appel (LGD) de 60 %).

### 6.15 VAN budgétaire, centrale et consolidée (25_FISCAL_IMPACT)

```
f_direct  = -g_direct
f_calls   = -call_tot
f_tax     = tax
f_roy     = o_roy
f_div     = e_g_out-sf_eq*gov_eq_share
f_grep    = grepay+ppag_reimb
f_net     = f_direct+f_calls+f_tax+f_roy+f_div+f_grep
f_net_cons= f_net+f_soe
fis_npv      = SUMPRODUCT(f_net,gdf)
fis_npv_cons = SUMPRODUCT(f_net_cons,gdf)
fis_npv_el   = fis_npv-cl_pv_el
```

Kasiri à 8 % : VAN de l'administration centrale de +34,8 millions USD, grâce aux impôts et aux redevances ; VAN consolidée de −27,6 millions USD, car la compagnie d'électricité paie l'énergie de Kasiri plus cher qu'elle n'encaisse par MWh. La feuille indique aussi le besoin de trésorerie annuel maximal, ce besoin maximal en part des recettes publiques, la sortie de fonds cumulée la plus profonde et l'impôt auquel l'État renonce.

### 6.16 Filtre budgétaire (26_DEBT_SUSTAINABILITY)

Le filtre cherche à savoir si ce seul projet crée une pression budgétaire supplémentaire significative. Il ne s'agit pas d'une analyse de soutenabilité de la dette (DSA).

```
s_onbud = x_onbud/gdp          s_cl   = cl_max/gdp
s_cash  = f_need/gov_rev       s_cumout = MAX(0,-f_cum)/gdp
s_arr   = u_arrears/gdp        s_inc  = s_onbud+s_cumout+s_arr
sc_debt = MAX(s_inc)   sc_cl = MAX(s_cl)   sc_cash = MAX(s_cash)
sc_post = debt_gdp+sc_debt
sc_flags= (sc_debt>th_incr)+(sc_cl>th_cl)+(sc_cash>th_cash)+AND(sc_post>th_debt,debt_gdp<=th_debt)
```

Seuils par défaut : augmentation significative à 1 % du PIB, exposition éventuelle significative à 2 % du PIB, besoin de trésorerie significatif à 1 % des recettes, référence d'endettement à 55 % du PIB. Le résultat :

| Condition | Résultat |
|---|---|
| Aucune alerte et note DSA de 1 ou 2 | *LOW additional fiscal pressure* (pression budgétaire supplémentaire faible) |
| Trois alertes ou plus, ou au moins une alerte avec une note DSA de 3 ou 4 ou une dette publique déjà supérieure à la référence | *HIGH additional fiscal pressure* (pression budgétaire supplémentaire élevée), avec l'instruction de saisir le ministère des Finances et l'équipe DSA |
| Autres cas | *MODERATE additional fiscal pressure* (pression budgétaire supplémentaire modérée) |

Kasiri : aucune alerte, note DSA de 2, résultat LOW.

### 6.17 Le filtre de développement à neuf portes (30_BANKABILITY)

Chaque test associe un indicateur à une note au moyen de trois seuils explicites et modifiables. Le sens H signifie que plus la valeur est élevée, mieux c'est :

```
H: score = IF(metric>=READY,3,IF(metric>=COND,2,IF(metric>=DEV,1,0)))
L: score = IF(metric<=READY,3,IF(metric<=COND,2,IF(metric<=DEV,1,0)))
```

Les notes correspondent à READY (prêt, 3), CONDITIONAL (sous conditions, 2), DEVELOPMENT GAP (lacune de développement, 1) et CRITICAL GAP (lacune critique, 0). La note d'une porte est le minimum de ses tests : ni moyenne, ni pondération.

| Porte | Test | Sens | READY | COND. | DEV. GAP | Kasiri |
|---|---|---|---|---|---|---|
| 1 Ressource | Série de débits fiable (années) | H | 25 | 15 | 8 | 12 |
| | Ratio d'énergie P90/P50 | H | 0,85 | 0,78 | 0,70 | 0,81 |
| | Maturité de l'étude hydrologique (1 à 3) | H | 3 | 2 | 1 | 2 |
| 2 Demande | Demande bancable ou contractée, pire des années 1 à 5 | H | 1,0 | 0,9 | 0,7 | 1,0 |
| | Part de la pointe du système à la COD | L | 15 % | 25 % | 35 % | 3,3 % |
| 3 Configuration | Coût unitaire / référence | L | 1,00 | 1,25 | 1,50 | 1,04 |
| | Facteur de charge (P50) | H | 45 % | 35 % | 25 % | 55,6 % |
| | Maturité de la faisabilité (1 à 3) | H | 3 | 2 | 1 | 2 |
| 4 Transport | Capacité d'évacuation à la COD / puissance installée | H | 1,0 | 0,8 | 0,5 | 2,0 |
| | Retard du transport (années) | L | 0 | 1 | 2 | 0 |
| | Financement du transport acquis | H | 1 | 1 | 0 | 1 |
| 5 Acheteur | Capacité de paiement / CAE, pire des années 1 à 10 | H | 1,2 | 1,0 | 0,8 | 5,96 |
| | Taux de recouvrement | H | 95 % | 90 % | 80 % | 88 % |
| | Garantie de paiement (mois) | H | 6 | 3 | 1 | 3 |
| 6 Réglementation/CAE | Éléments en CRITICAL GAP | L | 0 | 0 | 0 | 0 |
| | Éléments en GAP | L | 1 | 3 | 5 | 4 |
| | Part fixe (capacité) du chiffre d'affaires | H | 60 % | 40 % | 20 % | 0 % |
| 7 Financement | DSCR minimum, cas réel | H | `str_dscr` | `lockup` | 1,0 | 1,53 |
| | Écart de financement / emplois | L | 0 % | 5 % | 15 % | 1,9 % |
| | TRI des fonds propres privés par rapport à la cible | H | cible | cible −2 pts | cible −5 pts | 13,8 % |
| 8 Finances publiques | Besoin de trésorerie maximal / recettes | L | 0,5 % | 1 % | 2 % | 0 % |
| | Exposition éventuelle maximale / PIB | L | 1 % | 2 % | 4 % | 0,56 % |
| | Augmentation budgétaire maximale / PIB | L | 0,5 % | 1 % | 2 % | 0 % |
| | VAN budgétaire consolidée / PIB | H | 0 % | −0,5 % | −2 % | −0,08 % |
| | Note de risque DSA (1 à 4) | L | 1 | 2 | 3 | 2 |
| 9 E&S | EIES et conformité aux normes des prêteurs | H | 3 | 2 | 1 | 2 |
| | État du plan de réinstallation | H | 3 | 2 | 1 | 2 |
| | Questions transfrontalières | H | 3 | 2 | 1 | 3 |

Le test du TRI des fonds propres utilise `IF(ISNUMBER(kpi_eirr),kpi_eirr,IF(s_priv>0,-1,str_hurdle))`, de sorte qu'une structure sans fonds propres privés le réussit. Le verdict global :

| Condition | Verdict |
|---|---|
| Une porte au moins en CRITICAL GAP | NOT BANKABLE (non bancable : la ou les lacunes critiques doivent être comblées) |
| Sinon, au moins une DEVELOPMENT GAP | NOT YET BANKABLE (pas encore bancable : des lacunes de développement subsistent) |
| Sinon, note la plus basse égale à 2 | BANKABLE SUBJECT TO CONDITIONS (bancable sous conditions) |
| Toutes les portes READY | READY FOR FINANCIAL CLOSE (prêt pour le bouclage financier) |

Chaque porte comporte une action prérédigée : une action corrective quand la note vaut 0 ou 1, une action conditionnelle quand elle vaut 2. Le tableau de bord classe les portes selon une clé égale à la note augmentée du numéro de la porte divisé par 100, de sorte que les égalités sont départagées dans l'ordre des portes, et affiche les cinq portes les moins bien notées avec leurs actions.

Note de lecture pour Kasiri : la porte 6 est en CRITICAL GAP uniquement parce que le tarif rémunère uniquement l'énergie ; la part fixe du chiffre d'affaires est donc de 0 %, sous le seuil de lacune de développement de 20 %. Ce seuil est illustratif : un tarif rémunérant uniquement l'énergie peut être bancable si le risque hydrologique est couvert par ailleurs, et l'utilisateur doit calibrer ce test selon l'appréciation des prêteurs.

### 6.18 Les 23 portes de maturité pour le bouclage et l'échelle de décision (30A_CLOSE_READINESS)

Chaque porte comporte un domaine, un indicateur de porte critique et soit un test automatique du modèle, soit un statut de preuve saisi par l'utilisateur (MET (franchie), PARTIAL (partielle), NOT MET (non franchie) ou NO EVIDENCE (sans preuve)). Les tests automatiques renvoient MET ou NOT MET.

| N° | Porte | Critique | Test ou preuve par défaut | Question |
|---|---|---|---|---|
| 1 | Série de débits d'au moins 15 ans et revue hydrologique indépendante | Oui | `AND(rec_years>=15,hyd_study=3)` | Q1 |
| 2 | Énergie P90 confirmée par le conseiller technique des prêteurs | Oui | PARTIAL | Q1 |
| 3 | Étude de faisabilité bancable validée par le conseiller technique des prêteurs | Oui | `fs_level=3` | Q1 |
| 4 | Reconnaissances géotechniques suffisantes pour un rapport de référence | Oui | PARTIAL | Q1 |
| 5 | EIES approuvée et conforme aux normes des prêteurs | Oui | `es_level=3` | Q2 |
| 6 | Plan d'action de réinstallation (PAR) approuvé et financé | Oui | `rap_level>=2` | Q2 |
| 7 | Licence de production et permis d'utilisation de l'eau accordés | Oui | PARTIAL | Q2 |
| 8 | Droits fonciers acquis pour toutes les emprises du projet | Oui | NOT MET | Q2 |
| 9 | CAE signé et approuvé par le régulateur | Oui | PARTIAL | Q2 |
| 10 | Convention de mise en œuvre ou de concession signée | Oui | PARTIAL | Q2 |
| 11 | Contrat de raccordement au réseau signé et transport financé | Oui | `tx_fin=1` | Q3 |
| 12 | Transport en service au plus tard à la COD de la centrale | Non | `tx_gap_yrs<=0` | Q3 |
| 13 | Contrat(s) EPC signé(s) avec prix ferme, date d'achèvement et pénalités forfaitaires | Oui | PARTIAL | Q6 |
| 14 | Dispositif d'O&M et équipe du maître d'ouvrage en place | Non | PARTIAL | Q6 |
| 15 | Garantie de paiement d'au moins 6 mois en place | Oui | `lc_months>=6` | Q7 |
| 16 | Capacité de paiement de l'acheteur au moins égale à 1,2 x la facture du CAE (pire des 10 premières années) | Oui | `ut_ratio10>=1.2` | Q7 |
| 17 | Plan de financement entièrement engagé (aucun écart de financement) | Oui | `fin_gap<=0.5` | Q5 |
| 18 | DSCR minimum égal ou supérieur à la cible de dimensionnement dans le cas sélectionné | Oui | `AND(debt_m+debt_c>0,kpi_min_dscr>=str_dscr)` | Q5 |
| 19 | Engagements en fonds propres signés et TRI des fonds propres égal ou supérieur à la cible | Oui | `IF(ISNUMBER(kpi_eirr),kpi_eirr>=str_hurdle,s_priv<=0)` | Q4 |
| 20 | Assurance contre le risque politique ou garanties signées | Non | NO EVIDENCE | Q5 |
| 21 | Soutien de l'État approuvé par le ministère des Finances ; filtre budgétaire autre que HIGH | Oui | `LEFT(sc_result,4)<>"HIGH"` | Q7 |
| 22 | Programme d'assurances placé (tous risques chantier, pertes d'exploitation anticipées (DSU)) | Non | PARTIAL | Q6 |
| 23 | Audit indépendant du modèle réalisé | Non | NO EVIDENCE | Q5 |

La porte 17 tolère un écart de financement allant jusqu'à 0,5 million USD. La porte 18 exige l'existence d'une dette, de sorte qu'une structure sans dette senior ne la franchit pas grâce au DSCR de substitution de 99. La porte 18 lit le cas sélectionné ; elle évolue donc avec les tests de résistance.

**Échelle de décision**, évaluée dans cet ordre :

```
IF fc_crit_fail>0     "STOP: a critical gate is not met"
ELSE IF fc_crit_noev>0 "STOP: critical evidence missing"
ELSE IF fc_crit_part>0 "NOT READY: critical gates partly met"
ELSE IF fc_met=fc_n    "GO: evidence complete for a close decision"
ELSE                   "CONDITIONAL GO: all critical gates met"
```

Dans l'ordre, ces libellés signifient : STOP (arrêt), une porte critique n'est pas franchie ; STOP, une preuve critique manque ; NOT READY (non prêt), des portes critiques sont partiellement franchies ; GO (feu vert), le dossier de preuves est complet pour une décision de bouclage ; CONDITIONAL GO (feu vert sous conditions), toutes les portes critiques sont franchies. Un GO indique que le dossier de preuves est complet pour que les prêteurs et les promoteurs décident ; ce n'est pas une recommandation d'investissement. Kasiri : 6 portes franchies sur 23, 7 portes critiques non franchies, 6 portes critiques partiellement franchies, décision STOP.

Le récapitulatif au bas de la feuille compte, pour chaque question, les portes, les portes franchies et les portes critiques non franchies ou sans preuve. Q8 correspond au total. Pour Kasiri : Q1 0 sur 4 franchie (2 critiques ouvertes), Q2 1 sur 6 (2), Q3 2 sur 2 (0), Q4 0 sur 1 (1), Q5 1 sur 4 (1), Q6 0 sur 3 (0), Q7 2 sur 3 (1), Q8 6 sur 23 (7).

---
## 7. Scénarios, stress, sensibilités et script d'instantanés

### 7.1 Cas (mutuellement exclusifs)

Le cas se choisit avec `case` sur *01_CONTROL_PANEL* ; ses paramètres figurent sur *27_SCENARIOS*.

| Paramètre | Base (*Base*) | Bas (*Low*) | Haut (*High*) |
|---|---|---|---|
| Facteur de débit | 1,00 | 0,93 | 1,04 |
| Facteur de CAPEX (coût d'investissement) | 1,00 | 1,10 | 0,95 |
| Ajustement de la croissance de la demande | 0,0 pt | −1,5 pt | +1,0 pt |
| Facteur d'OPEX (charges d'exploitation) | 1,00 | 1,10 | 0,95 |

Les taux de croissance des segments de demande changent aussi selon le cas. Dans ce manuel, « pt » désigne un point de pourcentage et « pb » un point de base.

### 7.2 Commutateurs de stress (cumulables)

| Commutateur | Paramètre par défaut | Effet dans le moteur de calcul | Fondement indiqué dans le modèle |
|---|---|---|---|
| `st_drought` | Débit × 0,55 pendant 3 ans à partir de la 4e année d'exploitation | Facteur `drought` appliqué à la production (pas à la production du cas prêteurs) | Réduction d'environ 47 % de l'allocation de Kariba en 2024 [CL-04] |
| `st_capex` | +27 % | `eff_capex`, proportionné à la part supportée par le maître d'ouvrage, `epc_owner` | Dépassement réel médian selon Ansar et al. 2014 [HY-08] ; moyenne de +96 % |
| `st_delay` | +2 ans | Construction plus longue ; coût du retard de 4 % par an, proportionné à `epc_owner_d` | Retard moyen de 2,3 ans selon Ansar et al. 2014 [HY-08] |
| `st_demand` | Niveau de la demande × 0,80 à partir de la COD | `eff_dem` | Hypothèse |
| `st_offtaker` | Recouvrement −8 pt, transferts −30 %, tarif de détail gelé pendant 5 ans à partir de la COD | `eff_coll_adj`, `eff_sub`, `eff_freeze` | Hypothèse |
| `st_fx` | Dévaluation ponctuelle de 50 %, en une seule fois, à la COD | `eff_fxshock` | Fortes dévaluations récentes |
| `st_rate` | +300 pb sur la dette commerciale | Appliqué à la seule part non couverte | Dette concessionnelle à taux fixe |
| `st_trans` | Ligne livrée avec 2 ans de retard | `eff_tdelay` ; pénalité de coût | Hypothèse |
| `st_climate` | −3 % du débit moyen par décennie | Facteur `climate` | Valeur illustrative ; une étude de bassin est nécessaire |

### 7.3 Variations de sensibilité

`fx_capex`, `fx_gen`, `fx_tariff`, `fx_opex` et `fx_rate`, sur *01_CONTROL_PANEL*, s'appliquent en plus du cas et des stress. Les leviers effectifs utilisés par le moteur de calcul sont listés au bas de *27_SCENARIOS*.

### 7.4 Diagramme en tornade dynamique (28_SENSITIVITY)

Il s'agit d'un coût actualisé de l'énergie (LCOE) de présélection, calculé par formule fermée sur l'assiette de financement augmentée des intérêts intercalaires (IDC), au taux d'actualisation du projet et sur la durée du contrat d'achat d'électricité (CAE) :

```
lc_crf  = disc_rate/(1-(1+disc_rate)^-ops_years)
lc_base = ((fund_base+u_idc)*lc_crf+opex_y2)/p50*1000
```

Chaque facteur varie dans les deux sens : CAPEX ±20 %, production ±10 %, taux d'actualisation ±2 pt, OPEX ±20 %, part livrée (écrêtement de 0 à 15 %). Le LCOE de présélection de Kasiri est de 97,8 USD/MWh, et le CAPEX produit l'écart le plus large. Le diagramme en tornade ignore la fiscalité, le financement et le calendrier ; les résultats de financement proviennent du moteur de calcul complet.

### 7.5 Le script d'instantanés

`tools/run_snapshots.py` (le script d'instantanés, *snapshot runner*) recalcule l'intégralité du classeur pour chaque cas, en recalculant à chaque fois une copie temporaire dans LibreOffice sans interface (mode headless), et enregistre les résultats sous forme de tableaux statiques datés. Les formules dynamiques ne sont pas modifiées.

**Ce qu'il exécute.**

| Groupe | Exécutions | Dette |
|---|---|---|
| Base | Dette dimensionnée dans le modèle ; dette figée | Dimensionnée ; figée |
| Scénarios | Bas, Haut, Sécheresse, Dépassement de 27 %, Dépassement de 96 %, Retard, Demande faible, Acheteur, Acheteur sans garantie budgétaire, Choc de change, Taux élevé, Retard de la ligne de transport, Climat, Combiné (dépassement, retard, acheteur, change) | Figée |
| Structures | Structures 1 à 5 | Dimensionnée |
| Sensibilités | CAPEX ±20 %, production ±10 %, tarif ±10 %, OPEX +20 %, taux +200 pb, P90 dans les flux de trésorerie | Figée |
| Contrats | EPC 1, 2 et 3, en base et avec un dépassement de 96 % | Dimensionnée |
| Développeur | Taux d'actualisation de 18 %, prime de 6 %, probabilités par étape +10 pt, subvention de la moitié de la faisabilité, tarif +10 %, les quatre leviers ensemble | Dimensionnée |
| Cas prêteurs | P90 à un an | Dimensionnée |
| Résolutions | Variation de tarif qui donne à chaque structure son TRI cible des fonds propres (structures 2 à 5, neuf itérations de dichotomie) ; variation de débit à laquelle le DSCR minimum avec dette figée atteint 1,0 | Comme ci-dessus |

Pour les exécutions à dette figée, le script exécute d'abord la base avec la dette dimensionnée, puis inscrit les valeurs de base de `debt_m`, `debt_c`, `s_grant`, `s_goveq` et le principal commercial par année d'exploitation dans les données d'entrée figées de chaque copie.

**Ce qu'il enregistre.** Des tableaux statiques dans *27_SCENARIOS* (scénarios), *17A_STRUCTURES* (structures) et *28_SENSITIVITY* (sensibilités), chacun avec la date d'exécution, ainsi que `model/snapshot_results.json`, qui contient tous les résultats clés, les statuts des portes et une sélection de séries temporelles pour chaque exécution. Les résultats sont indexés par des noms courts (par exemple `base_sized`, `drought`, `offtaker_nobs`, `s3`, `epc2_ov`, `dev_all`, `len1`) ; les variations de tarif requises sont stockées sous `req_tariff_flex` dans `s2` à `s5`, et la variation de débit au point mort sous `be_flow_flex` dans `base_locked`.

**Sélection de résultats des instantanés (dette figée sauf mention contraire).**

| Exécution | TRI des fonds propres | DSCR minimum | Besoin de financement non couvert (M USD) | VAN budgétaire consolidée (M USD) |
|---|---|---|---|---|
| Base | 13,8 % | 1,53 | 4,1 | −28 |
| Sécheresse | 11,0 % | 0,69 | 4,1 | −27 |
| Dépassement de 96 % | 5,7 % | 1,49 | 68,3 | −37 |
| Acheteur, avec garantie budgétaire | 13,8 % | 1,53 | 4,1 | −125 |
| Acheteur, sans garantie budgétaire | −100 % | −0,53 | 4,1 | −152 |
| Choc de change | 13,8 % | 1,53 | 4,1 | −111 |
| Combiné | 7,8 % | 1,54 | 43,1 | −157 |
| Cas prêteurs P90 à un an (dette dimensionnée) | 13,2 % | 1,76 | 18,7 | −27 |

La variation de débit au point mort est d'environ −28 %. La variation de tarif qui donne à la structure de producteur indépendant d'électricité (PIE) son objectif de 15 % est d'environ +3,9 % (environ 116 USD/MWh contre 112).

**Comment relancer les calculs.** Depuis la racine du dépôt, avec LibreOffice (Calc), Python 3 et openpyxl installés, ainsi qu'un script de recalcul LibreOffice (`recalc.py`) qui prend en argument un fichier et un délai maximal et affiche un statut JSON :

```
python3 model/build_model.py                                  # facultatif : reconstruire à partir du générateur
RECALC=/path/to/recalc.py python3 tools/run_snapshots.py       # relancer tous les cas, écrire les tableaux et le JSON
python3 tools/model/check_cycles.py model/Bankable_Hydro_Model.xlsx
```

Le script s'arrête si un recalcul signale une erreur de formule. À la fin, il recalcule lui-même le classeur dans LibreOffice, puis lui applique `tools/model/excel_quote_fix.py`.

### 7.6 Le recalcul LibreOffice et la correction des apostrophes pour Excel

Lorsqu'il enregistre un classeur recalculé, LibreOffice écrit sans apostrophes les références aux feuilles dont le nom commence par un chiffre (par exemple `17_PROJECT_FINANCE!$C$31` au lieu de `'17_PROJECT_FINANCE'!$C$31`). La syntaxe des formules d'Excel exige ces apostrophes. `tools/model/excel_quote_fix.py` réécrit chaque formule, nom défini, validation de données et mise en forme conditionnelle du fichier pour les rétablir, sans modifier les valeurs en cache :

```
python3 tools/model/excel_quote_fix.py model/Bankable_Hydro_Model.xlsx
```

Exécutez-le après chaque recalcul LibreOffice qui enregistre le fichier livré, y compris un recalcul manuel. Le script d'instantanés le fait automatiquement en fin d'exécution. Un classeur écrit directement par `build_model.py` (openpyxl) comporte déjà les apostrophes et est paramétré pour un recalcul complet à l'ouverture.

---

## 8. Les deux niveaux de portes et la carte du cadre

### 8.1 Deux niveaux, deux étapes

| | Filtre à neuf portes | Maturité pour le bouclage à 23 portes |
|---|---|---|
| Feuille | *30_BANKABILITY* | *30A_CLOSE_READINESS* |
| Étape | Développement : faut-il continuer à dépenser ? | Transaction : le dossier de preuves justifie-t-il le bouclage financier ? |
| Fondement | Indicateurs comparés à trois seuils | Tests automatiques et statuts des preuves |
| Notation | Le test le plus faible détermine la porte ; la porte la plus faible détermine le verdict | Indicateurs critiques et échelle de décision |
| Résultat | De NOT BANKABLE (non bancable) à READY FOR FINANCIAL CLOSE (prêt pour le bouclage financier), avec des actions classées par priorité | STOP (arrêt), NOT READY (non prêt), CONDITIONAL GO (feu vert sous conditions) ou GO (feu vert) |
| Kasiri | NOT BANKABLE (porte 6) | STOP (7 portes critiques non franchies) |

Les deux niveaux peuvent diverger, et c'est instructif. Le filtre peut donner un résultat favorable alors que le test de bouclage indique STOP, car ce dernier ne compte que les preuves qui existent. Le tableau de bord affiche les deux à la ligne 4, et côte à côte dans ses blocs inférieurs.

### 8.2 La carte du cadre (34_FRAMEWORK_MAP)

Pour chacune des 23 portes, la carte indique la porte, la question du cadre à laquelle elle se rattache, la partie qui doit l'accepter, son caractère critique ou non, la ou les feuilles du modèle qui la testent (déduites des noms utilisés dans le test automatique, ou du domaine de la porte pour les portes de preuve), l'indicateur ou la preuve requis, le type (automatique ou preuve), le statut dynamique issu de *30A_CLOSE_READINESS* et les chapitres du livre qui traitent la question :

| Question | Chapitres du livre |
|---|---|
| Q1 | 2, 3, 9, annexes N à P |
| Q2 | 5, 7, 8, annexe R |
| Q3 | 3, 4 |
| Q4 | 6, 14 |
| Q5 | 12, 13 |
| Q6 | 9, 10, annexes O et Q |
| Q7 | 15 |
| Q8 | 17, 18 |

Le second tableau de la feuille rattache chaque porte du filtre à sa question principale, avec son statut dynamique : portes 1 et 3 à Q1 ; portes 6 et 9 à Q2 ; portes 2 et 4 à Q3 ; porte 7 à Q5 ; portes 5 et 8 à Q7.

Utilisez le filtre pendant le développement pour décider s'il faut continuer à dépenser, et les 23 portes au stade de la transaction pour décider si les preuves justifient le bouclage.

---

## 9. Contrôles d'intégrité et contrôle de cohérence avec le livre

### 9.1 33_CHECKS

| N° | Contrôle | Niveau en cas d'échec |
|---|---|---|
| 1 | Ressources = emplois (à 0,01 près) | ERROR (erreur) |
| 2 | Équilibre du financement de la construction (emplois = subventions + dette + fonds propres) | ERROR |
| 3 | Le phasage du CAPEX totalise 100 % | ERROR |
| 4 | Dette concessionnelle entièrement remboursée à la fin de l'horizon | ERROR |
| 5 | Dette commerciale entièrement remboursée à la fin de l'horizon | ERROR |
| 6 | Différé et durée de la dette concessionnelle compris dans la concession | ERROR |
| 7 | Maturité de la dette commerciale comprise dans la concession | ERROR |
| 8 | Construction et concession comprises dans 40 périodes | ERROR |
| 9 | Énergie livrée non supérieure à la production | ERROR |
| 10 | Montants impayés non négatifs | ERROR |
| 11 | Pas de remboursement in fine forcé lors de la dernière année de remboursement commercial (principal forcé supérieur à l'objectif de moins de 0,5 million USD) | WARNING (avertissement) |
| 12 | Solde du DSRA jamais négatif | ERROR |
| 13 | Ligne de transport financée par le projet entièrement financée (construction et CFADS) | ERROR |
| 14 | Contrôle des structures sur *17A_STRUCTURES* | WARNING |

`chk_all` affiche ALL OK (tout est correct) ou « n issue(s) » (n problème(s)). Lors du test indépendant, chaque contrôle a été forcé en échec sur une copie, et chacun s'est déclenché. Les contrôles confirment la cohérence interne, pas le réalisme des données d'entrée. N'utilisez pas les résultats tant que ALL OK ne s'affiche pas.

### 9.2 35_BOOK_CHECK

La feuille compare le modèle dynamique aux chiffres de Kasiri publiés dans le Livre 7 : 24 chiffres, chacun avec sa tolérance, et deux résultats textuels.

| Chiffre | Publié | Tolérance |
|---|---|---|
| Puissance installée (MW) | 60 | 0,5 |
| Production P50 (GWh) | 292 | 0,5 |
| Facteur de charge | 55,6 % | 0,05 pt |
| P90 à un an / à dix ans (GWh) | 236 / 268 | 0,5 |
| Coût de la centrale en termes réels 2026 (M USD) / coût unitaire (USD/kW) | 157 / 2 614 | 0,5 |
| Total des emplois / dette senior (M USD) | 215 / 145 | 0,5 |
| Taux d'endettement (gearing) sur le total des emplois | 68 % | 0,5 pt |
| LCOE (USD/MWh) | 106 | 0,5 |
| TRI des fonds propres privés / TRI du développeur | 13,8 % / 16,0 % | 0,05 pt |
| DSCR minimum / LLCR | 1,53 / 1,59 | 0,005 |
| Besoin de financement non couvert (M USD) | 4,1 | 0,05 |
| VAN du développeur pondérée par le risque (M USD) | −0,95 | 0,005 |
| Probabilité de bouclage | 15 % | 0,5 pt |
| Valeur de la position au stade des permis (M USD) | 1,28 | 0,005 |
| VAN budgétaire centrale / consolidée (M USD) | 35 / −28 | 0,5 |
| Exposition maximale aux passifs éventuels (M USD) | 225 | 0,5 |
| Capacité de paiement de l'acheteur, plus mauvaise des premières années | 6,0x | 0,05 |
| Portes franchies (sur 23) | 6 | 0 |
| Décision de bouclage financier | *"STOP: a critical gate is not met"* (STOP : une porte critique n'est pas franchie) | exacte |
| Filtre budgétaire | *"LOW additional fiscal pressure"* (pression budgétaire supplémentaire FAIBLE) | exacte |

Chaque ligne affiche PASS (conforme) ou CHECK (à vérifier), et la feuille affiche ALL PASS (tout est conforme) ou « n TO CHECK » (n à vérifier). Le contrôle n'est valable qu'avec les données d'entrée par défaut (cas de base, structure PIE, dette dimensionnée dans le modèle). Après une modification des données d'entrée, des lignes CHECK sont normales.

---

## 10. Liste de contrôle d'audit pour les relecteurs

1. *33_CHECKS* affiche ALL OK dans le cas examiné, et *35_BOOK_CHECK* affiche ALL PASS avec les données d'entrée par défaut.
2. Le classeur s'ouvre dans Excel sans réparation. S'il a été enregistré par LibreOffice, `excel_quote_fix.py` lui a été appliqué.
3. `check_cycles.py` ne signale aucun cycle après toute modification de `build_model.py`.
4. Chaque donnée d'entrée en bleu a une source ou une note d'hypothèse explicite ; les valeurs fictives (données pays de Navaria, coût unitaire de référence, coût de la ligne, comptes de la compagnie d'électricité, statuts réglementaires, étapes de développement) ont été remplacées.
5. Le cas prêteurs correspond au cas convenu avec le conseiller technique des prêteurs (LTA), et une sécheresse pluriannuelle a été testée séparément.
6. Les résultats des stress ont été lus avec le financement figé, et les données d'entrée figées de *18_DEBT* (C6 à C9 et ligne 12) contiennent les valeurs du cas de base, et non les valeurs provisoires livrées avec le fichier.
7. La contrainte qui dimensionne la dette (taux d'endettement ou couverture) est indiquée, avec le plafond d'endettement et le DSCR de dimensionnement.
8. Les données d'entrée de la compagnie d'électricité concordent avec ses comptes audités ; le scénario contrefactuel est compris ; la VAN budgétaire consolidée est présentée à côté de la VAN centrale.
9. Les probabilités d'appel sur *24_CONTINGENT_LIABILITIES*, les probabilités par étape, la prime de développement et les taux d'actualisation sont documentés comme des jugements.
10. Les seuils budgétaires de *26_DEBT_SUSTAINABILITY* et les seuils des portes de *30_BANKABILITY* ont été revus au regard de la politique du client et de la term sheet (feuille de modalités) des prêteurs.
11. Chaque statut de preuve saisi comme MET (franchie) sur *30A_CLOSE_READINESS* est assorti d'un document, d'un signataire et d'une date en colonne G.
12. Les tableaux d'instantanés ont été régénérés après la dernière modification des données d'entrée ; l'horodatage est consigné.
13. Le TRI du développeur n'est pas de −100 %, sauf si le flux de trésorerie n'admet réellement aucun taux ; si c'est le cas, examinez le flux de trésorerie sur *01A_DEVELOPMENT*, section F.
14. Le DSCR minimum et le DSCR moyen ne sont pas égaux à la valeur provisoire 99 (absence de service de la dette).

---

## 11. Limites connues

### 11.1 Ce que le modèle ne fait pas (Livre 7, annexe K)

- Il est annuel : pas de tirages mensuels pendant la construction, pas de dispatching saisonnier, pas de prix différenciés en heures pleines et heures creuses.
- La dette et les fonds propres sont tirés au prorata des dépenses, et non les fonds propres en premier, ce qui embellit légèrement le rendement des fonds propres.
- Il n'y a ni intéressement du développeur (promote ou carried interest) ni prêts d'actionnaires.
- Il n'y a pas de refinancement ; la revalorisation après la mise en service commerciale est évaluée directement.
- Le choc de change est permanent en termes réels, sans répercussion sur les prix locaux.
- Le modèle de la compagnie d'électricité ne comporte pas de bilan.
- Les stress sont déterministes : pas de simulation de Monte-Carlo sur l'hydrologie et le change, pas de distribution conjointe de la sécheresse, du change et des difficultés de la compagnie d'électricité.
- Les probabilités par étape, la prime de développement et le taux d'actualisation du développeur relèvent du jugement de l'utilisateur ; aucune donnée publique n'a été trouvée pour les calibrer pour l'hydroélectricité en Afrique.
- Le modèle a été recalculé dans LibreOffice et reproduit par un second moteur de calcul ; un test dans Microsoft Excel reste à faire.

### 11.2 Autres simplifications

- Les valeurs P sont obtenues par approximation normale à partir du coefficient de variation (CV). L'énergie est calculée à partir des débits mensuels moyens de long terme, ce qui surestime l'énergie lorsque les débits dépassent le débit d'équipement certaines années.
- Le P90 à dix ans utilise le facteur de persistance des grands échantillons (1+ρ)/(1−ρ)/n ; le facteur exact pour un échantillon fini avec n = 10 et ρ = 0,3 donne environ 0,3 % d'énergie en plus, de sorte que le modèle est légèrement prudent.
- L'écrêtement est proportionnel : l'énergie livrée est égale à la production multipliée par MIN(1, MW d'évacuation / MW installés).
- Le cas prêteurs utilise un impôt et des amortissements hors effet de levier, sans IDC ni commissions.
- L'impôt est calculé sur les recettes encaissées, et non sur les recettes facturées.
- Les charges d'exploitation de la compagnie d'électricité sont pour moitié fixes et pour moitié liées aux volumes ; le coût des autres approvisionnements est pour moitié indexé sur l'USD.
- Les appels de garantie sont déterministes dans un scénario donné ; la perte attendue ne vaut que ce que valent les probabilités saisies.
- L'indemnité de résiliation est simplifiée : dette plus le plus élevé de deux montants, les fonds propres non récupérés majorés d'une prime ou la valeur des distributions restantes au TRI cible.
- Le filtre budgétaire est un filtre au niveau du projet et ne remplace pas l'analyse de viabilité de la dette (DSA) du FMI et de la Banque mondiale ni le PFRAM. Les autres CAE et garanties du même gouvernement ne sont pas agrégés.
- Q3 (intérêt économique pour le système) n'est testée que par les portes relatives au réseau et au transport ; la comparaison avec le plan de développement au moindre coût de la compagnie d'électricité se fait hors du modèle (Livre 7, chapitre 17).
- Les coûts de développement entrent dans le coût de la centrale à leur budget réel (9,0 millions USD), phasés et indexés avec les dépenses de construction, tandis que le flux de trésorerie du développeur reçoit au bouclage la dépense nominale sur le scénario de succès (8,6 millions USD) ; les deux montants ne sont pas rapprochés.
- La marge de paiement de la compagnie d'électricité par MWh sur *17A_STRUCTURES* (environ 956 USD/MWh pour Kasiri) divise toute la capacité de paiement soutenable de la compagnie par l'énergie du projet ; elle est élevée pour une petite centrale et mesure une capacité, pas un prix.

### 11.3 Points mineurs ouverts issus du test indépendant

Le test indépendant (`docs/MODEL7_TEST_REPORT.md`) a relevé cinq anomalies, qui ont été corrigées (apostrophes pour Excel, valeurs de repli du TRI du développeur, validation des sélecteurs, valeur provisoire du DSCR dans la porte 18, erreur sur le DSCR moyen). Points restant ouverts :

1. Avec un débit nul de la rivière, le modèle ne se dégrade pas proprement : des erreurs de division apparaissent (P90/P50, LCOE, porte 1 et classement du tableau de bord).
2. Le débit d'équipement n'est lié ni à la puissance installée ni au coût : l'augmenter ne change rien, car la puissance est plafonnée aux MW installés, et le réduire diminue l'énergie sans diminuer le coût. La ligne « puissance théorique au débit d'équipement » (*"theoretical power at design flow"*) de *03_HYDROLOGY* ne fait pas partie de *33_CHECKS*.
3. Avec un tarif nul et une dette figée, les promoteurs financent indéfiniment l'insuffisance de service de la dette ; le modèle ne déclenche jamais lui-même de défaut ni de résiliation.
4. En l'absence de service de la dette, le DSCR minimum et le DSCR moyen affichent la valeur provisoire 99. La porte 18 est protégée par son test sur la dette, mais le test de DSCR de la porte 7 du filtre la noterait READY (prêt).
5. Le TRI du développeur renvoie −1 si la première valeur de départ converge vers un taux de valeur absolue supérieure ou égale à 1, sans essayer les deux autres.

Le quatrième point ouvert cité dans l'annexe K, le libellé de la porte 18, est réglé dans le classeur : le libellé indique désormais « dans le cas sélectionné » (*"in the selected case"*).

### 11.4 Points ouverts dans cette version candidate (4 octobre 2026)

1. *35_BOOK_CHECK* renvoie `#VALUE!` sur la ligne du TRI des fonds propres privés lorsque ce TRI vaut « n/a » (sans objet), c'est-à-dire pour la structure 1, qui ne comporte pas de fonds propres privés. Comme le script d'instantanés s'arrête à la moindre erreur de recalcul, une réexécution complète s'arrête à « Structure 1 ». Les tableaux de scénarios de *27_SCENARIOS*, *17A_STRUCTURES* et *28_SENSITIVITY* sont vides dans le classeur actuel, et `model/snapshot_results.json` provient de la dernière exécution complète, antérieure à l'ajout de *34_FRAMEWORK_MAP* et de *35_BOOK_CHECK* ; ses résultats de base concordent avec le contrôle de cohérence avec le livre.
2. Le classeur livré a été enregistré en dernier par LibreOffice et ses formules ne comportent pas les apostrophes ; exécutez `excel_quote_fix.py` avant de l'ouvrir dans Excel.
3. L'en-tête du tableau d'instantanés écrit par le script décrit la dette commerciale figée comme un « profil d'annuités » (*"annuity profile"*) ; l'échéancier figé est en réalité le principal sculpté du cas de base.

---

## 12. Reconstruire ou étendre le modèle

### 12.1 Le générateur

`model/build_model.py` est la source unique de référence. Exécutez-le depuis la racine du dépôt ; il écrit `model/Bankable_Hydro_Model.xlsx`, avec des formules uniquement (pas de valeurs en cache, recalcul complet à l'ouverture), ainsi que `model/model_map.json`.

Chaque cellule est créée par l'une de trois fonctions utilitaires :

| Fonction | Crée | Enregistre |
|---|---|---|
| `inp(ws, r, name, label, value, unit, note, fmt, key)` | Une donnée d'entrée en bleu dans la colonne C (fond jaune si `key`) | Nom scalaire |
| `calc(ws, r, name, label, template, unit, fmt, note, out)` | Une formule dans la colonne C (fond vert si `out`) | Nom scalaire |
| `ts(ws, r, name, label, unit, template, fmt, total, bold)` | Une formule dans chacune des colonnes E à AR, avec un total facultatif en C (`sum`, `max`, `min` ou une formule) | Nom de série temporelle |

Les formules sont écrites une seule fois sous forme de modèles et résolues une fois toutes les feuilles construites, de sorte que les feuilles peuvent se référer les unes aux autres quel que soit l'ordre de construction :

| Modèle | Se résout en |
|---|---|
| `{name}` | Référence absolue à une cellule scalaire |
| `[name]` | Cellule de la même colonne d'une ligne de série temporelle |
| `[name@p]` / `[name@n]` | Colonne précédente / suivante d'une ligne de série temporelle |
| `[RNG:name]` | Plage absolue complète E à AR d'une ligne de série temporelle |
| `[C:name]` | Colonne C (total ou valeur clé) d'une ligne de série temporelle |
| `#T#` | Indice de période t de la colonne courante |

Les noms sont uniques : les fonctions utilitaires lèvent une erreur en cas de doublon. Les formules qui renvoient à une seule cellule d'une autre feuille sont automatiquement colorées en vert.

### 12.2 Ajouter ou modifier une ligne

1. Ajoutez un appel `inp()`, `calc()` ou `ts()` sur la bonne feuille, en utilisant des noms existants dans le modèle de formule.
2. Si la ligne alimente une porte, ajoutez-la à la liste `GATES` (filtre) ou à `GATES_FC` et `GATE_Q` (maturité pour le bouclage) ; la carte du cadre est générée à partir de ces listes.
3. Si la ligne doit être suivie par le script d'instantanés, ajoutez son nom à `KPIS`, `EXTRA` ou `TS_SAVE` dans `tools/run_snapshots.py`.
4. Si un chiffre publié pour Kasiri change, mettez à jour la liste `BOOK_CHECKS` qui construit *35_BOOK_CHECK*, ainsi que le livre.
5. Reconstruisez le classeur, puis exécutez `tools/model/check_cycles.py` sur le nouveau fichier pour vérifier qu'il n'y a pas de référence circulaire.
6. Recalculez (LibreOffice via le script d'instantanés, ou ouverture et enregistrement dans Excel), exécutez `excel_quote_fix.py` si LibreOffice a enregistré le fichier, et vérifiez que *33_CHECKS* affiche ALL OK et *35_BOOK_CHECK* ALL PASS.
7. Relancez les instantanés et consignez la date.

### 12.3 Règles de conception à respecter

- Pas de macros, pas de tables de données, pas de références circulaires. Les intérêts intercalaires et les commissions restent calculés par formule fermée ; le DSRA reste financé par les fonds propres ; le cas prêteurs conserve un impôt hors effet de levier.
- Données d'entrée uniquement dans les cellules bleues ; aucun nombre saisi en dur dans les formules, sauf les constantes physiques et les conventions identifiées par un libellé.
- Tout nouveau résultat qu'un lecteur pourrait citer doit être défini sur la feuille et, s'il est publié dans le Livre 7, faire l'objet d'une ligne sur *35_BOOK_CHECK*.
- N'utilisez que des fonctions disponibles dans Excel 2010 et LibreOffice ; évitez les tableaux dynamiques, LET, LAMBDA, XLOOKUP et les fonctions volatiles.

---

*Le cas Kasiri River Hydro, la République de Navaria, Tamarind Hydro et la Navaria Electricity Company sont fictifs. Rien dans MODEL 7 ni dans ce manuel ne constitue un conseil en investissement, ni un conseil juridique, fiscal ou comptable.*
