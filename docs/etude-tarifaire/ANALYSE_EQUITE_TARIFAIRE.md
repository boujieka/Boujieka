# Équité tarifaire de l'électricité — Cameroun et Congo

Analyse des tarifs réglementés en vigueur, segment par segment, rapportés au coût du service.
Calculs : `analyse_equite_tarifaire.xlsx` (généré par `build_equite.py`). Les données ont été vérifiées le 17/10/2026.

> **Limite principale.** Aucun des deux pactes Mission 300 ne publie de coût **par segment**.
> - Le pacte du Cameroun donne un coût moyen (102,56 FCFA/kWh) et un tarif moyen MT/BT (102,65 FCFA/kWh).
> - Le pacte du Congo donne un coût moyen (0,16 USD/kWh) et un tarif moyen (0,09 USD/kWh).
>
> Pour le Cameroun, le coût par niveau de tension provient de l'**étude de coût de service réalisée pour l'ARSEL** :
> Banque mondiale / MRC & Phoenix, décembre 2022, [PDF sur arsel-cm.org](http://arsel-cm.org/wp-content/uploads/2026/02/CMR-142-CoSTariff-R4-revise_dec-2022.pdf).
>
> Pour le Congo, aucun coût par segment n'existe dans les sources trouvées.

---

## 1. Cameroun

### 1.1 Tarifs en vigueur

La référence est la décision ARSEL n°0096 du 28 mai 2012, toujours affichée par le régulateur ([arsel-cm.org](https://arsel-cm.org/tarifs-basse-tension/)). Les tarifs sont hors taxes.

**Résidentiel**

| Consommation mensuelle | Tarif |
|---|---|
| ≤ 110 kWh | 50 FCFA/kWh |
| 111 à 400 kWh | 79 FCFA/kWh |
| 401 à 800 kWh | 94 FCFA/kWh |
| 801 à 2 000 kWh | 99 FCFA/kWh |

**Autres segments**

| Segment | Tarif |
|---|---|
| Non résidentiel | 84 / 92 / 99 FCFA/kWh selon la tranche |
| Éclairage public | 66 FCFA/kWh |
| Moyenne tension (MT) | Prime fixe de 3 700 FCFA par kW souscrit, plus 60 à 85 FCFA/kWh selon la durée d'utilisation et l'heure |
| Haute tension (HT) | Contrats négociés : ALUCAM paie 14,1 FCFA/kWh, les autres clients HT 31,0 FCFA/kWh en moyenne (2020) |

Deux évolutions ne sont pas intégrées aux calculs :
- **Moyenne tension.** Selon le pacte, les tarifs des clients MT de 3 à 10 MW sont relevés de 10 % par an depuis 2023 pour les « arrimer au coût de service ».
- **Prépayé.** La presse rapporte un alignement des tarifs prépayés au 1er novembre 2024 ([Investir au Cameroun](https://www.investiraucameroun.com/gestion-publique/1811-21410-accuse-d-augmenter-les-prix-d-electricite-eneo-clarifie-l-harmonisation-des-tarifs-exigee-par-l-arsel)). Je n'ai trouvé aucune décision ARSEL publiée sur ce point.

### 1.2 Tarif et coût par segment

Données de 2025, sans modification des tarifs, tirées de l'étude ARSEL (tableaux 17, 20, 25 et 29).

| Segment | Tarif (FCFA/kWh) | Coût (FCFA/kWh) | Tarif / coût | Subvention (+) ou surcharge (−), Md FCFA |
|---|---|---|---|---|
| BT résidentiels | 73,8 | 86,5 | 0,85 | +33,3 |
| BT non résidentiels | 95,6 | 86,5 | 1,11 | −7,4 |
| Éclairage public | 66,0 | 86,5 | 0,76 | +4,7 |
| **MT** (PME, tertiaire, industrie moyenne) | **88,4** | **54,9** | **1,61** | **−53,5** |
| **HT — ALUCAM** | **14,1** | **51,0** | **0,28** | **+44,7** |
| HT — autres grands industriels | 31,0 | 51,0 | 0,61 | +15,1 |
| Ensemble | 64,8 | 69,8 | 0,93 | déficit de 36,8 |

**Qui finance qui ?**
- Les segments facturés sous leur coût reçoivent 97,8 Md FCFA de subventions brutes.
- **ALUCAM, un seul client, en capte 45,7 %.** Les ménages résidentiels en captent 34 %.
- La subvention par kWh d'ALUCAM est **2,9 fois** celle des ménages.
- Ces subventions sont financées à 53,5 Md FCFA par la **moyenne tension**, qui paie 61 % au-dessus de son coût.
- Le reste (36,8 Md FCFA) est couvert par l'État ou se traduit par un déficit de l'opérateur.

### 1.3 Équité à l'intérieur de la basse tension

**Structure progressive.** Le prix au kWh de la tranche sociale vaut la moitié de celui de la tranche la plus haute (rapport de 0,51). Les ménages qui consomment plus de 400 kWh/mois paient plus que le coût BT.

**Ciblage.** Le calcul utilise les volumes 2020 valorisés au coût BT de 2025 :
- la tranche 0–110 kWh reçoit **77 %** des subventions résidentielles positives ;
- elle représente **74 %** des factures, avec une consommation moyenne de 40 kWh par facture.

**Effet de seuil.** ENEO facture tout le mois au prix de la tranche atteinte (facturation exclusive). Passer de 110 à 111 kWh augmente donc la facture de **3 269 FCFA** pour un seul kWh de plus. Conséquence : la subvention mensuelle passe de 4 015 à 833 FCFA.

**Par décile de factures** (consommation, pas revenu) :
- de D1 à D7, la subvention augmente avec la consommation, de 22 à 3 139 FCFA par mois ;
- D8 ne reçoit plus que 857 FCFA, à cause de l'effet de seuil ;
- D10 paie une surcharge de 3 614 FCFA par mois.

### 1.4 Jugement

**Entre ménages raccordés**, la grille est **plutôt équitable** : progressive, et la plupart des subventions vont aux petites consommations. Deux défauts la pénalisent :
- les effets de seuil, qui pénalisent les ménages juste au-dessus de 110 et de 400 kWh ;
- l'exclusion des non-raccordés. Selon l'étude, l'accès était de 63 %, et de 23 % en zone rurale.

**Entre segments**, le système est **nettement inéquitable** :
- le premier bénéficiaire de subvention est un fondeur d'aluminium, ALUCAM ;
- il est financé par les entreprises MT et par le budget public.

Cela **invalide H3 sous sa forme générale** (« les subventions croisées pèsent sur l'industrie »). Elles **pèsent sur l'industrie moyenne et le tertiaire (MT)** et **profitent à la grande industrie HT**.

**Réserves qui pourraient modifier ce jugement :**
1. **Méthode d'allocation des coûts.** L'étude répartit les coûts au prorata des ventes, sans tenir compte de la pointe. Or la pointe de 20 h est résidentielle. Une allocation selon la responsabilité dans la pointe augmenterait le coût BT et réduirait les coûts MT et HT. La subvention des ménages et la surcharge MT seraient alors en partie surévaluées. Le sens des écarts pour ALUCAM ne changerait probablement pas, vu leur ampleur. C'est une inférence, non chiffrée.
2. **Tarif d'ALUCAM.** Celui de 2020 est supposé inchangé en 2025. Je n'ai trouvé aucune source sur l'état actuel du contrat.
3. **Hausses MT.** Elles ont lieu depuis 2023 alors que l'étude juge la MT déjà au-dessus de son coût. Deux explications concurrentes :
   - les clients de 3 à 10 MW bénéficiaient de contrats spécifiques inférieurs à la grille ;
   - le coût retenu par le gouvernement diffère de celui de l'étude.

   Je ne peux pas trancher entre les deux.
4. **Chiffres du pacte.** Le coût de 102,56 et le tarif de 102,65 FCFA/kWh ne sont pas comparables aux 69,8 FCFA/kWh de l'étude, exprimés en monnaie constante de 2022. Base, périmètre et année ne sont pas précisés.

## 2. République du Congo

### 2.1 Tarifs en vigueur

La référence est l'arrêté n°681 du 19 mars 1994, inchangé selon le pacte. La grille ci-dessous est celle reproduite par E2C ([e2c.cg/node/45](https://e2c.cg/node/45)). Le site d'E2C était inaccessible le 17/10/2026 (erreur HTTP 403) : la grille est à revérifier sur le texte de l'arrêté.

| Abonnement BT | Tarif (FCFA/kWh) | Tarif / coût moyen |
|---|---|---|
| Monophasé 1,2 à 3 kW | 49,08 | 0,50 |
| Monophasé 5 et 9 kW | 44,64 | 0,46 |
| Mono ou triphasé ≥ 11,5 kW | 43,56 | 0,45 |
| Triphasé, au-delà de 900 kWh/mois | 31,20 | 0,32 |

**Coût moyen retenu : 97,8 FCFA/kWh.** Il correspond aux 0,16 USD/kWh du pacte, convertis au taux implicite du même pacte (110 000 XAF = 180 USD, soit 611 XAF/USD).

**Données manquantes :**
- les tarifs MT et HT ;
- les primes fixes mensuelles en basse tension.

### 2.2 Jugement

La structure est **régressive**. Le plus petit abonné paie son kWh **57 % plus cher** que le gros abonné triphasé. Avec les consommations illustratives retenues (hypothèses de l'analyse), la subvention mensuelle est la suivante :

| Profil illustratif | Subvention mensuelle |
|---|---|
| Gros abonné, 1 200 kWh/mois | ≈ 79 900 FCFA |
| Petit abonné, 100 kWh/mois | ≈ 4 870 FCFA |

Le gros abonné reçoit donc **16 fois** plus que le petit.

Le pacte le confirme : il parle d'une « structure tarifaire très régressive » et constate l'absence de tarif social. S'y ajoutent trois facteurs :
- 40 % des clients sont facturés au forfait ;
- seuls 31 % des ménages ont accès au réseau ;
- les tarifs couvrent 56 % des coûts.

**Conclusion : la tarification congolaise est inéquitable.** La subvention est générale, elle est la plus forte par kWh pour les plus gros consommateurs, et elle exclut près de 7 ménages sur 10.

Le pacte prévoit deux échéances, qui sont des **engagements et non des réalisations** :
- un tarif social en décembre 2025 ;
- une nouvelle grille reflétant les coûts en décembre 2026.

Je n'ai trouvé aucune source confirmant leur adoption.

## 3. Conséquences pour l'étude

- **Cameroun.** Une réforme équitable passe d'abord par la renégociation ou la compensation budgétaire explicite du contrat HT d'ALUCAM, et par l'arrêt de la surtaxation MT. Toucher en premier à la tranche sociale n'est pas la priorité. Il faut aussi passer d'une facturation exclusive à une facturation par paliers successifs, pour supprimer les effets de seuil.
- **Congo.** Il faut inverser la progressivité, introduire le tarif social prévu par le pacte, réduire la facturation au forfait et subventionner le raccordement (110 000 XAF), qui est la barrière principale.

**Données à obtenir pour fiabiliser l'analyse :**
- l'étude de coût de service du Congo, si elle existe ;
- la grille MT et HT de l'arrêté n°681 ;
- l'état actuel du contrat d'ALUCAM ;
- les décisions ARSEL postérieures à 2012 (MT, prépayé) ;
- une enquête ménages par quintile de revenu (feuille `Equite_H2` du modèle).
