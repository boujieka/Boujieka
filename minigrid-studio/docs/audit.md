# Audit Phase 0 — Mini-Grid Financial Model Studio

*Version 1, 23 octobre 2026. Périmètre : Phase 0 du prompt maître (§10 du cahier des charges v0.1), qui couvre les étapes A à D du protocole de migration (§5).*

> **Statut.** Le moteur web **n'existe pas encore**. Aucune équivalence numérique avec le classeur n'est revendiquée. Le présent document décrit le classeur de référence et les documents contractuels. Il fixe aussi la méthode de calcul des valeurs étalons. Le passage en S1 (moteur) reste suspendu à la décision S0 « Audit et hypothèses approuvés » (§9) et aux questions de la section 9.

Livrables de la Phase 0 :

| Fichier | Contenu |
|---|---|
| `docs/audit.md` | Ce rapport. |
| `docs/variable_dictionary.csv` | 2 704 lignes de données : 197 entrées, 21 sélecteurs, 4 valeurs collées par macro, 3 constantes codées en dur dans les calculs, 1 624 cellules calculées isolées, 763 lignes calculées sur la chronologie, 92 cellules de sortie du tableau de bord. |
| `docs/formula_dependency_map.md` | Flux entre feuilles, chaînes de calcul, boucles rompues par macro, cycles, fonctions délicates. |
| `docs/row_dependencies.csv` | Pour chacune des 1 023 lignes portant des formules : les lignes dont elle dépend et le nombre de lignes qui en dépendent. |
| `docs/reference_scenarios.md` | Les 5 scénarios de référence, la procédure de calcul des valeurs étalons sous Excel et les tolérances. |
| `reference_values/` | Valeurs Excel du scénario S1 (lues dans le fichier) et valeurs **provisoires** LibreOffice pour S1 à S5. |
| `tools/phase0/` | Scripts reproductibles d'analyse statique et de recalcul de contrôle. |
| `reference/MANIFEST.md` | Empreintes SHA-256, provenance et état des droits des sources. |

Conventions de lecture : **[Fait]** = vérifié dans les fichiers ou par calcul. **[Inférence]** = déduction raisonnable, non vérifiée directement. **[À confirmer]** = nécessite Excel, un expert ou le commanditaire.

---

## 1. Méthode et garde-fous

- **[Fait]** Aucune macro n'a été exécutée. Le code VBA a été extrait statiquement avec `olevba` 0.60.2. Le p-code compilé a été décompilé avec `pcodedmp` 1.2.6 et comparé au code source : mêmes 4 procédures, mêmes noms de plages, aucune divergence, donc pas de « VBA stomping » apparent. Aucun appel système ni réseau, aucun appel à `Shell`, `CreateObject`, `Workbook_Open` ou `AutoOpen`. Les « Hex Strings » signalées par `olevba` sont les identifiants COM standard des classes Workbook et Worksheet (`00020819…`, `00020820…`).
- **[Fait]** Les formules et les valeurs mises en cache par Excel ont été lues avec `openpyxl` 3.1.5, sans recalcul. Le fichier a été enregistré par Microsoft Excel (`docProps/app.xml`, `calcId=191028`). Les valeurs en cache sont donc des résultats Excel authentiques pour l'état sauvegardé.
- **[Fait]** Le graphe des dépendances a été construit cellule par cellule : 52 401 formules et 258 500 arêtes. Les plages nommées et la formule nommée sont résolues. Chaque `OFFSET` est remplacé par la plage la plus large qu'il peut atteindre, ce qui donne une estimation prudente.
- **[Fait]** Un recalcul de contrôle a été fait dans LibreOffice 24.2.7 en mode sans échec, avec l'option `MacroExecutionMode = NEVER_EXECUTE` et sur une copie de travail. Les trois macros sont réimplémentées en Python à partir de leur source audité. Voir la section 6 : ce moteur **n'est pas** la référence.

## 2. Inventaire des fichiers

Le détail (empreintes, métadonnées, droits) est dans `reference/MANIFEST.md`. L'OSA a été reçu en double : deux fichiers identiques octet pour octet, une seule copie conservée.

### 2.1 Classeur `CrossBoundary-Access-Open-Source-Model-1.0-October-2023.xlsm`

| Feuille | Rôle (d'après la feuille *Key*) | Formules | Constantes numériques | Dimensions |
|---|---|---:|---:|---|
| Disclaimer | Avertissement (zone de texte) | 0 | 0 | — |
| Currency | Point d'entrée des montants monétaires ; sélecteur USD/LCY (`F18`) | 80 | 30 | A1:M70 |
| Portfolio | Paramètres par lot (3 lots actifs et 3 emplacements de réserve) et moyennes pondérées (colonne `S`) | 263 | 48 | A1:AQ49 |
| Inputs | Toutes les autres hypothèses ; zones des macros de dimensionnement | 1 279 | 118 | A1:AM499 |
| Model | Calculs AssetCo : production, consommation, recettes, opex, BFR, TVA, financement, cascade de trésorerie, rendements, fiscalité, amortissements, extension, diesel, remplacements | 32 024 | 2 | A1:CA779 |
| Debt | Dette senior, refinancement, MMRA, DSRA | 8 250 | 1 | A1:CA207 |
| Dashboard | Indicateurs clés et contrôles | 92 | 0 | A1:AB63 |
| FinStat | Compte de résultat, bilan, flux de trésorerie | 6 174 | 0 | A1:CA138 |
| Graph sheet | Données des 5 graphiques | 4 237 | 4 | A1:BZ144 |
| Key / Legend / Names | Documentation, légende des styles, constantes | 2 | 16 | — |

Le classeur contient aussi quatre feuilles de séparation (`INPUTS>>`, `CALCULATIONS>>`, `OUTPUTS>>`, `DOCUMENTATION>>`), vides.

- **[Fait]** Chronologie : **annuelle**, 69 colonnes `J:BZ` couvrant 2023 à 2091. La colonne `I` porte les totaux de ligne et la date de début du modèle (31/12/2022). Phases du cas publié : construction en 2023, exploitation de 2024 à 2043 (20 ans).
- **[Fait]** 30 noms définis, dont une formule nommée (`Baseline_consumption`) qui n'est **utilisée nulle part**. La liste complète est dans `work/inventory.json`, régénérable.
- **[Fait]** Calcul automatique, **sans itération** : `calcPr` n'active pas `iterate`. Les bouclages sont rompus par des valeurs collées par macro (section 4).
- **[Fait]** Validations de données (listes) sur 21 cellules de sélection : méthode de dimensionnement `Gearing`/`DSCR`, ordre de tirage `Equity first`/`Pari Passu`, taux fixe ou variable, cas de consommation 1, 2 ou 3, devise 1 ou 2, interrupteurs 0/1 (dette, DSRA, MMRA, refinancement, lots).
- **[Fait]** Une note de cellule (`Currency!D47`) cite la source BNEF du coût batterie de 2023.
- **[Fait]** Trois boutons sont reliés aux macros `Debt_Sizing`, `Refi_Debt_Sizing` et `DSRA_resize_3`. La procédure `DSRA_Resizing_2` existe mais n'est reliée à aucun bouton.

### 2.2 Documents contractuels et méthodologiques

| Document | Structure | Paramètres laissés en blanc `[•]` à relier au modèle |
|---|---|---|
| PSA — Share Purchase | Engagement de l'Owner, développement par l'OpCo, présentation du projet, conditions préalables, cession des titres, prix, révision du prix, earn-out (optionnel), garanties, droit anglais / arbitrage LCIA. Annexe A : critères d'éligibilité. | Montant maximal d'engagement, durée d'engagement, prix par connexion, seuil d'ARPU (en % de la prévision, sur N mois), durée de garantie, TRI non endetté minimal en USD sur N années, investissement minimal, part minimale de clients résidentiels ou professionnels. |
| PSA — Asset Transfer | Même ossature, mais transfert **par lots** (*Batch Presentation Certificate* trimestriel, réseaux rejetés, révision du prix à mi-parcours). L'annexe A ajoute un critère ESMS conforme IFC. | Mêmes paramètres, dont un **TRI par lot** et un investissement minimal hors subventions. |
| OSA | Services, durée minimale, standards, **rémunération** (forfait par site et pourcentage variable des recettes, payés chaque trimestre en monnaie locale), diesel (seuil de production diesel), encaissement, disponibilité garantie avec pénalités, gros remplacements remboursés au coût réel, extensions. Annexe A : périmètre des services. | Durée, forfait par site, % variable des recettes, seuil diesel, disponibilité garantie et barème de pénalités, montant déclenchant un signalement HSES, horizon du plan de gros entretien. |
| ESMS | Politique E&S, organisation, intégration au cycle de projet (examen préalable, catégorisation, EIES/PGES, permis, suivi en construction et en exploitation, fin de vie), annexes thématiques (normes de performance IFC, plan de mobilisation des parties prenantes, mécanisme de gestion des plaintes, genre et inclusion sociale, déchets, GES…). | Pas de paramètres financiers. Il fournit des statuts documentaires : permis, EIES, plans d'action. |
| Rapport 2020 | Méthode Isolate / Allocate / Aggregate, contrats de long terme, hypothèses prudentes, risques résiduels, pistes d'évolution (dette au niveau HoldCo, re-gearing). | Contexte méthodologique, pour la Learning Academy. |

## 3. Entrées, calculs, résultats et conventions (étape B)

### 3.1 Entrées

La liste complète est dans `docs/variable_dictionary.csv` (colonnes `kind`, `section`, `label`, `unit`, `value_published`, `allowed_values`, `used_by_cells`).

- **[Fait]** **197 entrées modifiables** : Inputs 110, Portfolio 54, Currency 29, Names 4 (y compris les libellés d'option saisis en clair comme « Fixed » ou « Floating »). **21 sélecteurs** à liste fermée. **4 valeurs collées par macro** (`Inputs!G292`, `G300`, `G344`, `E372`).
- **[Fait]** Le tableau de bord ne contient **aucune saisie** : ses cellules sont des liens vers les autres feuilles, à trois calculs près (`K37 = E13*E17`, `K43`, `K55`). Mais `Inputs!E136` (nombre de réseaux à construire) lit `Dashboard!E7`, qui lit lui-même `Inputs!E24`. L'information fait donc un aller-retour par le tableau de bord, sans créer de cycle.
- **[Fait]** Montants monétaires : chaque montant est saisi deux fois dans *Currency* (colonne `H` en USD, colonne `I` en LCY), puis sélectionné par `INDEX` selon `Currency!F18`. Certains montants contractés en monnaie locale (frais OpCo, coûts logistiques, tarifs) sont saisis en `K` et convertis au taux de base `F16`.
- **[Fait]** Le portefeuille est **agrégé en un réseau moyen**. Les paramètres des lots (*Portfolio* `E:J`) sont ramenés à une moyenne pondérée (colonne `S`), par le nombre de connexions ou par le nombre de réseaux selon la ligne. Le modèle calcule ensuite un seul réseau moyen multiplié par le nombre de réseaux. **Il ne produit aucun flux, TRI ou contrôle par lot.**

### 3.2 Constantes codées en dur dans les feuilles de calcul (signalées)

| Cellule | Valeur | Effet |
|---|---|---|
| `Model!E41` | `1e-05` | La perte « Meters Consumption distribution losses » vaut la consommation des compteurs × (1 + 0,00001). Ce facteur n'est documenté nulle part. |
| `Model!J15` | `1` | Base de l'indice d'inflation en 2023 (convention normale). |
| `Graph sheet!E76` | `0.05` | Taux d'actualisation du LCOE du module d'extension, graphique uniquement. |

### 3.3 Hypothèses sans effet

- **[Fait]** Ces hypothèses ne sont lues par aucune formule :
  - `Inputs!E83` (rendement d'un groupe de 10 kW) ;
  - `Inputs!E359` (*Upfront Fee* du refinancement : **le refinancement ne porte aucun frais d'émission**) ;
  - `Names!F11`, `F14`, `F15`, `F18`.
- **[Fait]** Ces cellules calculées ne sont lues par aucune formule :
  - `Inputs!E321` et `E361` (*Commitment Fee* : **aucune commission d'engagement n'est imputée**, ni sur la dette senior ni sur le refinancement) ;
  - `Inputs!E65`, `E67`, `E70` (coûts de remplacement batterie) : le coût réellement utilisé est la prévision de la ligne 201 (152 $/kWh en 2023, en baisse de 10 % par an), plus 20 $/kWh de main-d'œuvre.

### 3.4 Résultats

**[Fait]** Le tableau de bord rassemble les indicateurs suivants :
- TRI projet (XIRR) et délai de récupération ;
- emplois et ressources ;
- ARPU moyen, consommation moyenne, tarif moyen pondéré dans le temps, population desservie ;
- 12 contrôles (`Dashboard!K42:K53`) et un contrôle global (`K55 = SUM(K42:K53)`).

D'autres indicateurs sont calculés dans *Model* : TRI fonds propres AssetCo et Owner avec et sans subvention, VAN (XNPV), VAN par connexion.

**[Fait]** Le modèle **ne calcule pas de série de DSCR effectif** ni de LLCR ou de PLCR. Le DSCR n'y apparaît que comme **cible** de sculptage (1,20 x). Un DSCR annuel peut être dérivé des lignes CFADS (`Model!291`) et service de la dette (`Model!305:306`), ce que fait `reference_scenarios.md`. Mais cet indicateur n'a pas d'équivalent Excel à rapprocher.

### 3.5 Conventions

| Sujet | Convention observée | Statut |
|---|---|---|
| Signe | Encaissements positifs, décaissements négatifs dans *Model*/*FinStat*. Les emplois (`Model!199:204`) sont négatifs, les ressources positives. | [Fait] |
| Périodes | Années civiles. Les drapeaux de phase comparent les dates de début et de fin de période aux dates de phase. | [Fait] |
| Dates des flux | `XIRR`, `XNPV` et `NPV` datent tous les flux au **31/12** de chaque année. Un flux de −1×10⁻⁷ au 31/12/2022 sert d'ancrage aux séries de TRI. | [Fait] |
| Achat des réseaux | Les réseaux construits en année N sont achetés et financés en N+1 (décalage d'une colonne, `Model!J179 = I176`, `I179` vide), soit la 1ʳᵉ année d'exploitation. Aucun flux en 2023 dans le cas publié. | [Fait] |
| Intérêts | Intérêts de l'année = taux × (solde d'ouverture + tirages de l'année). Les intérêts intercalaires (`Model!255`) ne portent que sur le solde d'ouverture, donc **0** quand la dette est tirée l'année d'achat. | [Fait] |
| Devise | Devise du modèle sélectionnable (USD ou LCY). Les indices de change sont libellés « Naira », ce qui suggère une origine nigériane du modèle ; la devise reste générique. Les TRI sont reconvertis en USD (`Model!370`). | [Fait] / [Inférence] sur l'origine |
| Unités | kWh, kWp, kVA, $/W, $/kWh, $/connexion/mois. Les constantes de la feuille *Names* servent aux conversions. | [Fait] |
| Arrondis | `ROUND`, `ROUNDUP`, `ROUNDDOWN` d'Excel : arrondi au plus loin de zéro. Une réimplémentation Python ou TypeScript doit **éviter l'arrondi bancaire**. | [Fait] / à respecter |
| Tolérance du bilan | `FinStat!67 = ROUND(Actif net − Capitaux propres, 3)` | [Fait] |

## 4. Dépendances, bouclages et macros (étape C)

La cartographie détaillée est dans `docs/formula_dependency_map.md`. L'essentiel :

- **[Fait]** **Aucune référence circulaire au sens d'Excel** dans l'état publié. Le graphe cellule à cellule ne contient aucun cycle, sauf une arête **conditionnelle** : `Model!J491` peut lire `Model!I485`, le total de ligne des pertes fiscales générées. Cette lecture n'est évaluée que si l'exploitation commence dès la première colonne du modèle, ce qui n'est pas le cas publié (`IF(J490=0, 0, …)`). Si on la retire, le graphe est acyclique. La plus longue chaîne compte 4 166 cellules.
- **[Fait]** **Quatre bouclages économiques sont rompus par des valeurs collées par macro :**

| Bouclage | Valeur calculée → valeur collée | Macro | Critère d'arrêt |
|---|---|---|---|
| Besoin de financement ↔ dette (frais, DSRA, plafond de gearing) | `Inputs!E292` → `G292` | `Debt_Sizing` (Module1) | `Funding_Delta = MIN(collé − calculé, ROUND(collé − calculé, −5)) = 0` |
| Capacité de dette sculptée au DSCR ↔ service de la dette | `Inputs!I300` (essai amorti) → `G300` | `Debt_Sizing` | `DSCR_Delta = MIN(calculé − collé, ROUND(calculé − collé, −5)) = 0` |
| Dette de refinancement ↔ CFADS | `Inputs!I344` → `G344` | `Refi_Debt_Sizing` (Module2) | `Refi_Delta` = 0, même règle |
| Dotation initiale de la DSRA ↔ service de la dette ↔ financement | `Inputs!E371` → `E372` | `DSRA_resize_3` (Module7) | Copie unique ; contrôle `E373` |

- **[Fait] Tolérance de convergence large et asymétrique.** `ROUND(x, −5)` ramène à 0 tout écart de moins de 50 000 unités monétaires. Avec `MIN`, l'écart n'est accepté que d'un côté (collé ≥ calculé pour le financement, calculé ≥ collé pour le DSCR). En LCY, l'arrondi passe à −7, soit 5 000 000 LCY ≈ 50 000 USD au taux de 100. Dans l'état publié :
  - financement collé 11 678 350,87 contre 11 677 906,99 calculé (écart de 443,88, soit 3,8×10⁻⁵) ;
  - capacité DSCR collée 6 132 616,89 contre 6 153 524,19 calculée (écart de 0,34 %).

  **Conséquence :** l'état Excel est un point fixe *approché*. Pour se rapprocher d'Excel au-delà de ces écarts, le moteur web devra **soit rejouer exactement la même procédure à partir des mêmes valeurs collées, soit accepter de partir des valeurs collées publiées**. Voir la section 7.
- **[Fait]** Les boucles `Do Until` n'ont **aucune limite d'itération**. En cas de non-convergence, Excel boucle sans fin. Le rejeu Python s'arrête à 500 itérations et le signale.

## 5. Fonctions et constructions difficiles à reproduire

| Construction | Volume | Difficulté |
|---|---:|---|
| `OFFSET` à **largeur négative** (fenêtres glissantes vers l'arrière : amortissements, pertes fiscales, durée de vie des réseaux, batteries, onduleurs, PV) | 759 appels sur 966 cellules `OFFSET` | Volatile et dynamique. **Rejeté par LibreOffice (Err:502)**, ce qui rend 33 280 cellules invalides. À réécrire en fenêtres glissantes explicites. |
| `OFFSET` vers l'avant (cible de MMRA sur 5 ans, valeur de sortie, DSRA sur N périodes) | 207 | Dépend d'entrées (`E140`, `E345`, `F165`). |
| `IRR` glissant (`Model!372`, `429`) | 138 | Excel trouve des TRI **négatifs** en début de vie ; LibreOffice échoue et `IFERROR` renvoie 0. Sans effet sur le délai de récupération (test `> 0`). |
| `XIRR` / `XNPV` / `NPV` | 5 / 4 / 69 | Le solveur dépend du point de départ et de la tolérance. Écart LibreOffice − Excel observé : 2,4×10⁻⁹ sur le TRI projet. |
| `LOOKUP` en correspondance approchée | 1 199 | Suppose des vecteurs triés. **[À confirmer sous Excel]** `Inputs!I406:K406` contient `2021`, `2022` et le texte `"2023+"`. Pour 2023 et au-delà, `LOOKUP` renverrait le taux de base de 2022, et non celui de « 2023+ ». C'est sans effet aujourd'hui (les trois taux valent 2 % et le taux fixe est sélectionné), mais c'est un piège dès qu'on modifie le taux variable. |
| `IFERROR` | 439 | Peut masquer des erreurs. Le moteur web doit lever les erreurs au lieu de les remplacer par 0. |
| `EOMONTH`, numéros de série de dates | 214 | Système de dates 1900. Attention au 29/02/1900 fictif si des dates très anciennes apparaissent (ex. `Debt!E75` = 29/12/1899 quand le refinancement est désactivé). |
| `ROUND`, `ROUNDUP`, `ROUNDDOWN` | 355 | Arrondi au plus loin de zéro. `ROUNDUP` dimensionne les modules d'extension : les effets de seuil sont discrets. |
| `AVERAGEIF(…, "<>0")`, `SUMPRODUCT` | 10 / 18 | Moyennes « hors zéros » : un zéro légitime est exclu. |
| Bruit de virgule flottante | — | Les recettes du « ratchet » valent ~1×10⁻¹⁰ au lieu de 0, et la trésorerie de clôture ~1×10⁻¹⁰. Il faut des tolérances absolues pour les quasi-zéros. |

## 6. Recalcul de contrôle (LibreOffice) et valeurs étalons (étape D)

- **[Fait]** LibreOffice 24.2 **ne reproduit pas** le classeur tel quel : `OFFSET` à largeur négative renvoie Err:502, ce qui propage des erreurs dans 33 280 cellules.
- **[Fait]** Sur une **copie de travail** où `OFFSET(réf,0,0,h,−w)` est réécrit en `OFFSET(réf,0,1−w,h,w)` (mêmes cellules), LibreOffice reproduit **52 173 des 52 401 formules à max(10⁻⁹ relatif, 10⁻⁶ absolu) près**, et les 211 cellules texte à l'identique. Il reste 17 écarts :
  - 14 TRI glissants négatifs (`Model!372` ×4, `Model!429` ×10 ; voir la section 5) ;
  - 3 dates décalées de 31 jours (`Inputs!J364`, `Inputs!L364`, `Debt!F68`) : `EOMONTH` de la date 0, lue différemment par LibreOffice.

  *Correction du 24/10/2026 : une version antérieure attribuait ces 3 écarts à des quasi-zéros.*

  Les 37 indicateurs et 22 séries annuelles retenus concordent avec un écart relatif maximal de 6×10⁻¹⁵ (`tools/phase0/compare_outputs.py`).
- **[Fait]** Les valeurs étalons Excel n'existent aujourd'hui **que pour S1** (état publié). Les scénarios S2 à S5 ont été calculés **provisoirement** dans LibreOffice avec rejeu des macros. **Ces valeurs ne sont pas des valeurs étalons** : elles doivent être confirmées sous Excel selon la procédure de `reference_scenarios.md`.

Indicateurs de référence (S1 = Excel ; S2 à S5 = LibreOffice, provisoires) :

| Indicateur | S1 base | S2 DSCR | S3 LCY | S4 refi | S5 stress |
|---|---:|---:|---:|---:|---:|
| TRI projet | 12,657 % | 12,691 % | 14,207 % | 12,804 % | 7,193 % |
| Délai de récupération (ans) | 8 | 8 | 7 | 8 | 12 |
| Dette senior | 5 838 732 | 6 001 281 | 592 000 000 LCY | 5 838 948 | 5 802 483 |
| Fonds propres Owner | 2 906 675 | 2 752 232 | 298 750 000 LCY | 2 906 448 | 2 873 799 |
| TRI Owner avec subvention | 11,18 % | 11,39 % | 18,58 % | 12,33 % | 1,73 % |
| TRI Owner sans subvention | 5,50 % | 5,51 % | 13,13 % | 5,66 % | −2,56 % |
| Contrôles en échec | aucun | aucun | injection de fonds propres | aucun | injection de fonds propres |

S3 est exprimé en monnaie locale ; ses TRI sont convertis en USD par le modèle. Le contrôle en échec dans S3 et S5 (« Equity injection not required ») traduit un résultat économique du cas (besoin d'apport en cours de vie), pas un défaut de convergence.

## 7. Observations à arbitrer avant le moteur

Ces points sont des **constats**, pas des corrections. Le moteur web devra d'abord reproduire le classeur tel qu'il est, puis proposer d'éventuels correctifs en option documentée, conformément à la règle « Ne remplace pas les calculs par des approximations sans signalement ».

1. **Date de début d'exploitation.** `Inputs!E17 = EOMONTH(Con_Start, E14*(Months_Yr−1))+1`. Ce n'est juste que pour `E14 = 1` : pour 2 ans, elle donne le 01/12/2024 au lieu du 01/01/2025. La fin d'exploitation (`E19`) part de la fin de construction (`E11`) et non du début d'exploitation. **[Inférence : anomalie probable ; à confirmer avec l'auteur.]**
2. **Agrégation du portefeuille en réseau moyen.** Pas de flux par lot. Or le PSA « Asset Transfer » exige un **TRI par lot**, et le cahier des charges demande des « paramètres propres à chaque lot ». **Un calcul par lot n'aurait pas de référence Excel** : il devra être marqué *expérimental*, ou validé par des propriétés (somme des lots = portefeuille sur les postes linéaires).
3. **Rémunération OSA ≠ modèle.** L'OSA prévoit un forfait par site et un pourcentage variable de **toutes** les recettes, payés chaque trimestre en monnaie locale. Le modèle prévoit un forfait par réseau (4 000/an) et un forfait par client (2/mois), plus un **ratchet de 30 % des recettes au-delà de la prévision P50**, calculé à l'année. Le rapprochement contrat–modèle de la matrice §7 n'est pas direct. **[À arbitrer par le commanditaire.]**
4. **TRI « projet ».** La ligne `Model!365` intègre la subvention et un **impôt calculé après intérêts**, donc l'économie d'impôt liée à la dette. Ce n'est pas un TRI « unlevered » au sens strict du critère d'éligibilité des PSA. **[À arbitrer : définir le TRI à comparer au seuil contractuel.]**
5. **Commissions non imputées.** Les commissions d'engagement (senior et refinancement) et la commission d'émission du refinancement sont saisies mais n'entrent dans aucun flux (section 3.3).
6. **Pas de covenant DSCR.** Le sculptage vise 1,20 x, mais aucune série de DSCR effectif, aucun test de distribution (lock-up) ni de défaut n'est calculé. L'année de grâce affiche un DSCR dérivé de 0,83 en S1 : la DSRA couvre l'écart (70 359 tirés). Le contrôle « senior debt fully repaid » ne peut pas échouer, car la dernière échéance rembourse tout le solde restant (`Debt!J32 = IF(J24=1, −J30, …)` ; `I32` est le total de ligne).
7. **Impôt comptable et impôt payé.** Au compte de résultat, l'impôt est de 30 % × max(EBT, 0), sans exonération temporaire ni report des pertes. L'impôt payé, lui, applique l'exonération, les pertes reportables et les amortissements fiscaux. L'écart s'accumule en « impôt différé passif ». **[À faire valider par un expert-comptable : une exonération temporaire crée en principe une différence permanente.]**
8. **Lecture d'un total de ligne.** `Model!J188` (réseaux en service en 2023) lit `Model!I183`, le total de toute la ligne des réseaux construits. Sans effet sur les flux (`MIN(…, 0)`), mais l'indicateur vaut 30 en 2023 au lieu de 0.
9. **Fonctions inactives dans le cas publié.** Arrivée du réseau national (année 30, hors durée de vie), sortie (année 45, hors durée de vie), BFR (0 jour), TVA (0 %), taux variable, refinancement. Elles ne peuvent être validées qu'avec des scénarios dédiés (S4 pour le refinancement). Arrivée du réseau, sortie, BFR et TVA restent **sans scénario de référence** à ce stade.

## 8. Correspondance financière–contractuelle (§7 du cahier des charges) : état préliminaire

| Variable ou résultat | Cellules du modèle | Document cible | État |
|---|---|---|---|
| Sites, lots, dates de mise en service | `Portfolio!E8:J16` ; `Inputs!I134:N143` ; `Model!176–188` | PSA AT (lots trimestriels) / PSA SP | Partiel : les lots du modèle sont des moyennes, et la chronologie annuelle ne connaît pas le trimestre. |
| Prix d'acquisition ou de transfert | `Portfolio!E29:E32` (capex net de subvention + frais de transfert, par connexion) ; `Model!191` | PSA (« cash payment per connection ») | Direct (prix par connexion × connexions). TVA : le PSA dit « includes VAT », le modèle traite la TVA à part (0 % aujourd'hui). |
| Durée, forfait, part variable | `Inputs!E173:E176` ; `Model!97–121` | OSA (forfait par site, % des recettes) | **Divergent** (observation 3). |
| Seuil de production diesel | `Inputs!E92:E99` (seuil de 75 % de consommation brute ; plafond de diesel de 5 % de la production solaire brute, déclencheur d'extension) | OSA « Diesel Generation Threshold [•]% » | À définir : quelle grandeur du modèle correspond au seuil contractuel. |
| Montant de dette, durée, DSCR | `Inputs!E296:E332` ; `Debt!21–60` | Term sheet dette (nouveau gabarit) | Paramètres disponibles. Covenants absents du modèle (observation 6). |
| TRI minimal d'éligibilité | `Model!E375` (TRI projet) | PSA annexe A (« unlevered [•]-year IRR in USD ») | Définition à arbitrer (observation 4) ; TRI par lot impossible (observation 2). |
| ARPU (condition préalable) | `Model!89–90`, `Model!113` (ARPU P50) | PSA, conditions préalables | Disponible annuellement ; le PSA raisonne sur N mois de données de paiement mobile. |
| Mesures E&S, permis | — | ESMS / conditions préalables | Hors modèle : statut documentaire et revue humaine. |

## 9. Questions bloquantes pour la décision S0

1. **Droits.** CrossBoundary a-t-il donné, ou peut-il donner, une **autorisation écrite** d'usage commercial et de redistribution du modèle et des gabarits PSA, OSA et ESMS ? Faut-il en attendant **retirer de ce dépôt public** les analyses qui citent leurs libellés, valeurs et formules, ou les déplacer vers un dépôt privé ?
2. **Valeurs étalons Excel.** Qui peut exécuter la procédure de `reference_scenarios.md`, avec quelle version d'Excel, et sur quel poste maîtrisé ? Sans cela, seul S1 a des valeurs étalons Excel.
3. **Rapprochement cible.** Le moteur doit-il (a) reproduire l'état Excel **y compris** la tolérance des macros (même procédure, mêmes valeurs collées de départ), ou (b) résoudre le point fixe exactement, avec des écarts documentés jusqu'à 0,34 % sur la capacité DSCR ? Nous recommandons (a) pour la validation et (b) en option signalée.
4. **Observations 1 à 7.** Pour chacune : reproduire à l'identique (recommandé pour la validation), corriger dans une variante, ou les deux ?
5. **Lots.** Le calcul par lot (exigé par le PSA AT et le cahier des charges) est-il un besoin du MVP ? Il n'aura pas de référence Excel.
6. **OSA.** Quelle structure de rémunération le Contract Studio doit-il paramétrer : celle de l'OSA, celle du modèle, ou les deux avec un contrôle d'écart ?

## 10. Limites de cet audit

- Le recalcul indépendant utilise LibreOffice, pas Excel. Les écarts de fonctions (IRR, LOOKUP mixte) n'ont été observés que sur S1.
- Le fichier fourni n'a pas été comparé à l'archive publiée par CrossBoundary.
- Les macros n'ont pas été exécutées. Leur comportement est déduit du code source et du p-code, et rejoué en Python.
- Les observations de la section 7 décrivent ce que font les formules. Elles ne jugent pas de l'intention de l'auteur, sauf mention [Inférence].

---

## Addendum (24/10/2026) — Phase 1

Reproduire le classeur a fait apparaître des constats supplémentaires, listés et qualifiés (test ou lecture de formule) dans `docs/phase1_report.md`, section 4. L'arbitrage des observations 1 à 7 est fait : le classeur est reproduit à l'identique, et les corrections sont proposées comme options désactivées par défaut (`backend/app/engine/options.py`).
