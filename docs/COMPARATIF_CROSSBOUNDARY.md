# Comparatif : CrossBoundary Access Open Source Model 1.0 (oct. 2023) et nos produits

**Méthode.** Le fichier `.xlsm` fourni par l'utilisateur a été ouvert avec openpyxl. J'ai extrait les libellés texte des 16 onglets (environ 2 600 cellules), puis je les ai fouillés par mots-clés. J'ai aussi lu la documentation interne (onglet *Key*). Les macros VBA ont été listées, mais pas exécutées.
**Limite.** C'est une analyse des libellés et de la structure, pas un audit de chaque formule. Une fonction implémentée sans libellé explicite a pu m'échapper.

## Ce que le modèle CrossBoundary contient (vérifié dans le fichier)
- **Onglets :** Currency (gestion de scénarios de change), Portfolio (jusqu'à 3 lots + 3 lots de réserve de mini-grids), Inputs, Model, Debt, Dashboard, FinStat (états financiers), Graph sheet, Key, Legend, Names.
- **Logique :** un modèle **AssetCo / portefeuille**. On achète un ensemble de mini-grids à un prix « capex net of grant » par connexion, et un OpCo exploite contre une redevance.
- **Grant :** exprimé en **$ par connexion** et versé à l'AssetCo. Le CAPEX est saisi « net of grant ». Un libellé mentionne « Initial Equity (net of Grant, First Loss) ».
- **Subvention d'exploitation :** une ligne « Subsidy » en **$/kWh** ajoutée au tarif (onglet Model, ligne 68).
- **Dette :** dimensionnement par gearing **ou** par DSCR, dette **sculptée**, frais, refinancement, **DSRA**, **MMRA** (réserve de maintenance), macros de résolution des circularités.
- **Autres :** fiscalité poussée (exonération temporaire, report des pertes, TVA, impôt minimum, retenue à la source sur dividendes), change et inflation, BFR, extension de capacité, arrivée du réseau national, valeur de sortie, courbes de consommation (plateau, log, croissance des revenus), LCOE, IRR et NPV, ARPU, personnes desservies.

## Nos éléments différenciants : présents ou absents chez CrossBoundary ?
| Élément | CrossBoundary | Verdict |
|---|---|---|
| RBF payé par connexion **vérifiée**, avec décalage de vérification | Non. Grant $/connexion versé à l'achat, sans vérification ni décalage. Aucun libellé « RBF », « results » ou « verification ». | **Différenciant, mais partiellement.** L'économie d'un grant par connexion est proche. Ne pas prétendre qu'ils n'ont « aucune subvention ». |
| RBF différencié par segment de clientèle | Non (un grant moyen par connexion, par lot) | Différenciant |
| **Viability gap** (subvention nécessaire pour NPV = 0) | Non. Aucun libellé « viability » ou « gap ». | **Différenciant** |
| Calibrage du grant ou du RBF nécessaire (IRR cible ou NPV = 0) | Non. Le grant est une hypothèse saisie, pas une sortie. | **Différenciant** (c'est le cœur de notre P2) |
| Segments de clientèle (ménages, usages productifs, commerces, institutions) | Non. Une consommation moyenne par connexion. | Différenciant |
| Usages productifs (inventaire d'équipements) | Non (0 occurrence) | Différenciant |
| Affordability (facture en % du revenu) | Non (0 occurrence). ARPU calculé, mais pas comparé au revenu. | Différenciant |
| Courbe de charge horaire pour dimensionner la batterie et le diesel | Non. Une part nocturne est saisie directement. | Différenciant modeste |
| MRV et impact (CO₂, emplois, connexions vérifiées) | Non. Seulement le nombre de personnes desservies. Aucun libellé CO₂, émission, MRV ou emplois. | **Différenciant** |
| Ratios coût-efficacité (subvention par connexion, par tCO₂, levier capital privé) | Non | Différenciant |
| Dette concessionnelle distincte de la dette senior (blended finance) | Non. Une seule dette senior (avec refinancement). Le mot « Blended » désigne seulement une moyenne de portefeuille. | Différenciant |
| Tornado de sensibilité | Non. Seulement quelques cellules « Sensitivity » sur la consommation et le tarif. | Différenciant |
| Note de demande de financement générée automatiquement | Non | Différenciant |
| Allocation d'un fonds entre projets (P3) | Non. Le « Portfolio » regroupe des mini-grids d'un même investisseur, pas des candidatures à un fonds. | Différenciant pour P3, mais attention au chevauchement du mot « portfolio » |

## Là où CrossBoundary est PLUS complet que nous (à ne pas cacher)
- Dette sculptée, refinancement, frais bancaires, dimensionnement de la dette par macro.
- Change, inflation, TVA, BFR, états financiers complets (bilan), exonération fiscale, retenue à la source.
- Extension de capacité, arrivée du réseau national, valeur de sortie, courbes de consommation sophistiquées.
- Crédibilité de la marque (acteur reconnu du secteur), et c'est gratuit.

## Conséquences pour le positionnement
1. **Ne pas** se vendre comme « le modèle de project finance mini-grid le plus complet ». CrossBoundary est gratuit et plus profond sur la dette, la fiscalité et le change.
2. **Se vendre** comme l'outil qui répond à **« combien de subvention, sous quelle forme, pour quel impact ? »** : viability gap, calibrage du RBF, segments, affordability, MRV, blended finance, note de financement.
3. **Cible naturelle :** développeurs en phase de candidature à un programme RBF ou de subvention, équipes de programmes et de fonds, consultants. CrossBoundary cible plutôt l'investisseur AssetCo.
4. **Message d'annonce possible (factuel) :** « Complements full project-finance models: focuses on subsidy sizing (viability gap, RBF per connection), affordability and MRV ». Pas de dénigrement, et pas de mention de CrossBoundary dans l'annonce sans relecture juridique.
5. **Licence :** je n'ai pas trouvé de texte de licence dans les libellés (l'onglet Disclaimer contient probablement une image). Ne réutiliser **aucune** formule ni structure du fichier CrossBoundary dans nos produits, et ne pas le redistribuer.
