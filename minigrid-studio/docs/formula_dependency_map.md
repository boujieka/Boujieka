# Carte des dépendances du classeur CrossBoundary (étape C)

Source : analyse statique de 52 401 formules et 258 500 dépendances cellule → cellule (`tools/phase0/inventory.py`). Le détail ligne à ligne est dans `docs/row_dependencies.csv` : pour chaque ligne de formules, les lignes dont elle dépend.

## 1. Flux entre feuilles

Nombre de références d'une feuille vers une autre. Le schéma montre les principaux flux (sélection) ; la liste complète est dans `work/inventory.json` (`sheet_edges`, non versionné).

```
 Names ───(976)──────────────────────────────┐
 Currency ─(22)─> Inputs <─(17)─ Portfolio    │
     ^ (78)          │  ^ (10) Dashboard      │
     └───────────────┤                        v
                     ├────────(32 826)──────> Model ──(3 553)──> FinStat
                     └────────(3 623)───────> Debt  ──(345)────> FinStat
                                   Model <──(1 174)── Debt
                                   Model ──(626)────> Debt
                         Model/Debt ──> Graph sheet (2 529 / 345)
                         Model/Inputs/Debt ──> Dashboard (24 / 43 / 3)
                         FinStat ──(138)──> Model  (EBT pour l'impôt)
                         Model ──(143)──> Inputs (zones de dimensionnement)
```

Les flux `Model → Inputs` (143) et `Debt → Inputs` (4) remontent les **valeurs calculées** du besoin de financement, de la capacité DSCR, du refinancement et de la DSRA vers les zones des macros. Les flux `FinStat → Model` (138) remontent l'EBT vers le calcul de l'impôt.

## 2. Chaîne de calcul principale (feuille *Model*, colonne d'une année donnée)

```
Calendrier, drapeaux (4–20)
  └─> Portefeuille : réseaux construits, achetés (décalage N+1), en service, retirés (23–27, 173–188)
        └─> Production PV brute (30–33 ← 590–604) ─> pertes (37–45) ─> production nette (48–49)
        └─> Consommation par connexion (52 ← Inputs!433, cas 1/2/3) × connexions (59) ─> kWh vendus (60)
              └─> Tarif × indices FX/inflation (63–75) ─> RECETTES (77, 87)
              └─> Frais OpCo : forfait réseau (97–101), forfait client (103–107), ratchet P50 (112–119) ─> 121
              └─> Diesel : ratio consommation/production par site (661–680) ─> seuil ─> litres ─> coût (684–707) ─> 124
              └─> Frais administratifs (127–130) ─> OPEX TOTAL (132)
        └─> BFR (135–150), TVA (152–168) ─> FLUX D'EXPLOITATION (170)
  └─> Emplois : achats de réseaux, intérêts intercalaires, frais, DSRA et MMRA initiales (199–204)
  └─> Ressources : subvention (215) ─> fonds propres (219) ─> dette senior (223) ─> fonds propres additionnels (226)
  └─> Cascade de trésorerie : flux d'exploitation (262) + financement (264) + capex courants (276 ← 269–274)
        ─> injection de fonds propres (281) ─> impôt payé (287 ← 481 ← FinStat!23) ─> libération de la MMRA
        ─> CFADS (291) ─> DSRA : intérêts et tirage (296–301) ─> service de la dette senior (305–307 ← Debt)
        ─> refinancement (310–324) ─> DSRA : dotation et libération (317–319) ─> MMRA (329–333)
        ─> injection (335) ─> sortie (341–347) ─> retenue sur dividendes (349) ─> DISTRIBUTIONS (405)
  └─> Rendements : projet (358–378, XIRR 375), hors achats (381–394), fonds propres (397–418), Owner (422–441)
  └─> Impôt (458–506), amortissements comptables (512–546) et fiscaux (548–583)
  └─> Extension, batteries et onduleurs : modules requis selon le déficit ou le diesel (606–623), coût (626–649),
      remplacements selon les durées de vie (714–776)
```

Sur la feuille *Debt*, chaque année :

```
Drapeaux de maturité et de grâce (21–27)
Solde (30–34) : tirage ← Model!246 ; remboursement = MIN(principal max) sauf à la dernière échéance (solde entier)
Intérêts (38–48) = taux × (solde d'ouverture + tirage)
Sculptage (52–60) : principal max = CFADS (Model!291) / DSCR cible − intérêts   ─> Inputs!E300 = Σ principal max
Refinancement (63–102), MMRA (105–152), DSRA (155–204) : cible = Σ service de la dette des N périodes suivantes × part
```

## 3. Boucles économiques rompues par macro

Aucune n'est une référence circulaire Excel, car chacune passe par une **valeur collée** :

```
(1) Gearing / financement
    Inputs!G292 (collé) ─> plafond de dette E297 ─> E304 ─> frais d'arrangement (Model!258) ─> emplois (Model!204)
    ─> Inputs!E292 (calculé) ─> I292 ─> [Debt_Sizing colle I292 → G292]

(2) Dimensionnement DSCR (si Inputs!E302 = "DSCR")
    Inputs!G300 (collé) ─> E304 ─> dette tirée ─> intérêts ─> impôt ─> CFADS ─> principal max ─> Debt!I60
    ─> Inputs!E300 ─> I300 (essai : collé + delta ou collé + 0,5 × delta) ─> [Debt_Sizing colle I300 → G300]
    (Dans le cas « Gearing », G300 n'agit pas sur la dette, mais la macro boucle quand même jusqu'à DSCR_Delta = 0.)

(3) Refinancement : Inputs!G344 ─> E348 ─> Debt!75 ─> intérêts ─> CFADS ─> Debt!I102 ─> E344 ─> I344 ─> [Refi_Debt_Sizing]

(4) DSRA : Inputs!E372 (collé) ─> Debt!194 ─> emplois (Model!202) ─> financement ─> dette ─> service de la dette
    ─> cible DSRA (Debt!165) ─> Debt!F169 ─> Inputs!E371 ─> [DSRA_resize_3 colle E371 → E372]
```

Ordre d'exécution prescrit par le classeur (feuilles *Key* et *Currency*) : calcul automatique, puis `Debt_Sizing`, puis `DSRA_resize_3`, à répéter « jusqu'à ce que les contrôles soient Ok ». Le refinancement se dimensionne avec `Refi_Debt_Sizing` quand il est activé.

## 4. Cycles détectés par l'analyse statique

| Constat | Détail |
|---|---|
| Composante fortement connexe brute | 6 220 cellules sur 92 lignes (dette, impôt, pertes fiscales, cascade de trésorerie). |
| Origine | Une seule arête conditionnelle, `Model!I485 → Model!J491` : la fenêtre `OFFSET` des pertes reportables peut atteindre la colonne `I`, où se trouve le total de ligne. Elle n'est évaluée que si l'exploitation commence dans la colonne `J` (première année du modèle). Dans tous les autres cas, `IF(J490=0, 0, …)` court-circuite la lecture. |
| Sans cette arête | Graphe acyclique ; chaîne la plus longue : 4 166 cellules. |
| Lecture d'un total de ligne sans cycle | `Model!J188` lit `Model!I183` (total des réseaux construits), voir audit §7, observation 8. |

**Conséquence pour le moteur web.** Le calcul peut être organisé **année par année, dans l'ordre** : chaque année ne dépend que des années précédentes, plus des fenêtres vers l'avant pour la MMRA, la DSRA et la valeur de sortie. Les quatre boucles ci-dessus restent à résoudre explicitement. Le scénario « exploitation dès la première colonne » doit être interdit, ou traité comme une configuration non couverte par le classeur.

## 5. Fenêtres `OFFSET` (966 cellules, 14 motifs)

| Ligne | Motif (colonne J) | Sens | Usage |
|---|---|---|---|
| Model!188 | `OFFSET(I183,0,0,1,-J187)` | arrière | Réseaux en service sur la durée de vie |
| Model!491 | `OFFSET(I485,0,0,1,-J490)` | arrière | Pertes fiscales encore reportables |
| Model!520, 529, 538 | `OFFSET(I515…,0,0,1,-J519…)` | arrière | Bases amortissables (comptable) |
| Model!557, 566, 575 | idem | arrière | Bases amortissables (fiscal) |
| Model!599 | `OFFSET(J591,0,0,3,-J598)` | arrière, 3 lignes | Capacité PV encore en vie |
| Model!726 | `OFFSET(J743,0,0,3,-J725)` | arrière, 3 lignes | Capacité batterie encore en vie |
| Model!770 | `OFFSET(J759,0,0,3,-J769)` | arrière, 3 lignes | Capacité onduleur encore en vie |
| Model!345 | `NPV(WACC, OFFSET(K344,,,1,E345))` | avant | Valeur de sortie |
| Debt!140 | `SUM(OFFSET(K136,,,1,E140))` | avant | Cible MMRA (capex de batteries des N prochaines années) |
| Debt!165 | `SUM(K162:OFFSET(K162,0,$F165-1))` | avant | Cible DSRA (service de la dette des N prochaines périodes) |
