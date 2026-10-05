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
