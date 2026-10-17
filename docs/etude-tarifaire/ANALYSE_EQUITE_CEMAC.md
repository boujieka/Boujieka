# Équité tarifaire de l'électricité dans la CEMAC

Cette note étend l'analyse Cameroun–Congo (`ANALYSE_EQUITE_TARIFAIRE.md`) au Gabon, au Tchad, à la Centrafrique et à la Guinée équatoriale.

- **Calculs** : `analyse_equite_tarifaire.xlsx`, feuilles `CEMAC_Comparaison`, `GAB`, `TCD`, `CAF` et `GNQ`. Le classeur est généré par `build_cemac.py`.
- **Vérification** : le 17/10/2026. Les chiffres clés ont été relus dans les documents sources (PDF des pactes, rapports d'évaluation de projet, barèmes, texte de loi).

> **Limite commune.** Le Cameroun est le seul pays de la CEMAC dont un coût du service **par segment** est publié (étude ARSEL, 2022). Ailleurs, la grille est rapportée à un **coût moyen**. Ces coûts moyens n'ont ni la même année, ni le même périmètre : production seule, coût de revient ou coût complet. Les ratios donnent des ordres de grandeur ; ils ne mesurent pas précisément les subventions.

## 1. Vue comparative

| | Cameroun | Congo | Gabon | Tchad | Centrafrique | Guinée éq. |
|---|---|---|---|---|---|---|
| Texte tarifaire | ARSEL 2012 | Arrêté 681 (1994) | Barème SEEG 2020, gelé depuis 2018 | Arrêté de 2012 | Grille de déc. 2016 | Loi du 21/05/2002 |
| Petit consommateur (FCFA/kWh) | 50 | 49,08 | 52,40 | 85 | 76,56 (TTC) | 60 |
| Gros consommateur résidentiel | 99 | 31,20 | 129,58 | 125 | 89,31 (TTC) | 160 |
| Rapport petit / gros | 0,51 | **1,57 (régressif)** | 0,40 | 0,68 | 0,86 | 0,38 |
| Coût moyen de référence (FCFA/kWh) | 69,8 | 97,8 | 79,8 (?) | 200 | ≈ 120 | n.d. |
| Petit consommateur / coût moyen | 0,72 | 0,50 | 0,66 | 0,43 | 0,64 | n.d. |
| Tarif social explicite | Oui | Non | Oui | Partiel | Non | Tranche de 1–150 kWh |
| Accès national | 63 % | 31 % (ménages) | 92,7 % | 11 % | 16,8 % | 65,1 % |
| Coût par segment publié | **Oui** | Non | Non | Non | Non (étude 2022 non publiée) | Non |

Le ratio du Cameroun utilise le coût moyen global de 69,8 FCFA/kWh. Rapporté au coût BT de 86,5 FCFA/kWh, il vaut 0,58.

## 2. Constats par pays

### Gabon : le plus équitable entre ménages, inconnu entre segments

Le barème de la SEEG (01/01/2020, HT) comporte :
- un **tarif social** à 52,40 FCFA/kWh pour un abonnement de 1 kW, et à 84,68 FCFA/kWh pour 2 kW ;
- un tarif général qui **augmente avec la puissance** souscrite, de 111,18 FCFA/kWh à 3 kW jusqu'à 129,58 FCFA/kWh à 15 kW.

L'accès atteint 92,7 % (53,6 % en milieu rural), un niveau que le pacte juge lui-même « optimiste ».

Trois réserves :
1. **Usagers sans compteur.** Environ 500 000 usagers sont alimentés par le compteur d'un voisin et ne peuvent pas bénéficier du tarif social.
2. **Prix de l'énergie MT et HTB.** En heures creuses, il va de 12 à 55 FCFA/kWh, soit moins que le tarif social, auquel s'ajoute une prime fixe. Sans coût par tension, impossible de dire si c'est justifié.
3. **Couverture des coûts.** Les chiffres se contredisent :
   - le pacte (p.41) donne un coût moyen de revient de 79,8 FCFA/kWh pour un prix moyen de 103,2 FCFA/kWh ;
   - le même pacte écrit que les tarifs ne couvrent pas les coûts de service ;
   - la Banque mondiale estime que 83 % des coûts d'exploitation et de maintenance sont couverts.

   Le coût de 79,8 FCFA/kWh est donc probablement partiel.

### Tchad : fortement inéquitable, d'abord par exclusion

La grille de 2012 n'a que deux niveaux : 85 FCFA/kWh jusqu'à 150 kWh par mois, 125 FCFA/kWh pour tout le reste, **MT comprise**. Elle ne reflète donc pas les coûts par tension.

Le coût de production est estimé à 200 FCFA/kWh par le pacte et à 0,22 USD/kWh (environ 126 FCFA) par la Banque mondiale. Selon le chiffre retenu, les tarifs couvrent entre 43 % et 99 % de ce coût.

Ce qui fait l'inéquité, c'est la distribution de la subvention (Banque mondiale, PAD 2022) :
- elle atteignait **84 M USD en 2019**, versée en nature sous forme de combustible ;
- elle représentait **environ 1 000 USD par client et par an** ;
- elle bénéficiait aux seuls clients raccordés, alors que **l'accès n'est que de 6 à 11 %** ;
- les **2 000 plus gros clients** fournissent plus de 60 % des recettes, donc captent l'essentiel de la subvention.

La gratuité de 2024 (jusqu'à 300 kWh par mois) et le remplacement de la SNE par TchadElec en 2025 ne sont connus que par des sources secondaires.

### Centrafrique : inéquitable

La grille de décembre 2016 (TVA incluse) n'a pas de tranche sociale. Sa progressivité dépend des **heures d'utilisation** de la puissance souscrite, pas du volume consommé.

Deux écarts ressortent :
- **Bangui et la province.** Les 15 centres secondaires paient **160,84 FCFA/kWh**, près du double de Bangui. Leur coût diesel est probablement plus élevé, mais aucune donnée ne permet de le vérifier.
- **MT et BT.** L'énergie MT coûte de 30 à 42 FCFA/kWh, plus une prime fixe.

Côté coûts, la donnée disponible date de 2014 : 0,20 USD/kWh, soit environ 120 FCFA. La Banque mondiale estime à 55 % le recouvrement effectif des coûts.

Avec 16,8 % d'accès, environ 83 % de la population est exclue de toute subvention.

### Guinée équatoriale : non jugeable

Le pays n'a pas de pacte Mission 300. La seule grille vérifiable est celle de la loi du 21 mai 2002 :

| Consommation mensuelle (milieu urbain, thermique) | Tarif (FCFA/kWh) |
|---|---|
| Jusqu'à 150 kWh | 60 |
| 501 à 2 500 kWh | 160 |
| Au-delà de 25 000 kWh | 120 |

La grille est donc progressive puis dégressive pour les très gros consommateurs. Les prix ruraux vont de 55 à 80 FCFA/kWh.

Aucun coût publié n'a été trouvé, et l'on ne sait pas si la grille est encore en vigueur. L'accès rural est de 5,1 % (WDI 2024).

## 3. Lecture régionale

1. **Le premier facteur d'inéquité est l'exclusion du réseau, pas la grille.** Au Tchad, en Centrafrique et au Congo, entre 69 % et 94 % de la population ne reçoit aucune subvention tarifaire. Comme le prévoit H2, les subventions généralisées profitent d'abord aux ménages déjà raccordés, et ce mécanisme domine dans ces pays.
2. **Le prix au kWh payé par le petit consommateur couvre entre 43 % et 72 % du coût moyen dans les cinq pays mesurables.** Partout, le petit consommateur raccordé est donc subventionné. La question d'équité porte sur **qui paie l'écart** : l'État, la dette de l'opérateur, ou d'autres segments comme la MT au Cameroun.
3. **Les structures tarifaires divergent.** Le Gabon et le Cameroun ont des grilles progressives avec un tarif social. Le Congo a une grille régressive. Le Tchad et la Centrafrique ont des grilles plates ou fondées sur les heures d'utilisation.
4. **Les tarifs sont figés.** La plupart des grilles ont entre 8 et 32 ans : 1994, 2002, 2012, 2016, et un gel au Gabon depuis 2018. Les pactes promettent des réformes entre 2025 et 2028, mais aucune n'a été confirmée par une source.
5. **Les coûts par segment manquent.** Hors Cameroun, on ne peut pas savoir si l'industrie MT et HT est subventionnée ou surtaxée. **H3 n'est testable qu'au Cameroun**, où le résultat est mixte : la MT est surtaxée, la HT (ALUCAM) subventionnée.

## 4. Données manquantes prioritaires

- **Gabon** : coût par tension. La couverture des coûts reste contradictoire (pacte contre Banque mondiale).
- **Tchad** : texte de l'arrêté de 2012 et grille de TchadElec ; réconciliation des coûts de production (200 FCFA contre 0,22 USD).
- **Centrafrique** : études tarifaires PURACEL de 2021–2022, non publiées ; statut de la grille de 2016.
- **Guinée équatoriale** : grille SEGESA actuelle (le site présente un certificat invalide) et tout coût de revient.
- **Tous les pays** : enquêtes ménages par quintile de revenu, pour passer de l'équité « par niveau de consommation » à l'équité « par revenu ».
