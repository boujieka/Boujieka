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
