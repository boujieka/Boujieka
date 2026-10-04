# 07 — Pilote Cameroun

## 1. Ce qui change par rapport au plan initial

Le plan initial enchaînait 7 étapes à l'échelle nationale (découpage → localités → foncier → actifs →
validation → recensement → intelligence). L'ordre est pertinent (cartographier avant de dénombrer),
mais l'exécuter d'emblée sur tout le pays revient à lancer le programme complet sans preuve de méthode
ni de coût.

**Proposition : deux vitesses.**
- **Socle national léger** : uniquement ce qui est peu coûteux et utile partout (N1 + imports N3).
- **Pilote de terrain approfondi** : toutes les couches, N0 à N3, dans **3 communes contrastées**.

Le pays compte 10 régions et, à ma connaissance, 58 départements et environ 360 arrondissements/communes
(chiffres à confirmer sur le référentiel officiel en vigueur).

## 2. Phases

### Phase 0 — Cadrage (préalable)
- Inventaire des **sources existantes** : couverture, date, licence, qualité (imagerie, empreintes de bâtiments, OSM, cartes sectorielles, cadastre minier, atlas forestier, carte scolaire et sanitaire, résultats et cartographie censitaire disponibles).
- **Revue juridique** (voir [05](05-gouvernance-et-cadre-juridique.md) §3).
- Désignation des **propriétaires institutionnels** de chaque couche ; accords de partage de données.
- Choix des 3 communes pilotes ; protocole d'évaluation.

### Phase 1 — Socle national
1. **Référentiel territorial** : régions → départements → arrondissements → communes → villages/quartiers, versionné, aligné sur l'INC et l'administration territoriale. *Livrable vérifiable : liste et géométries officielles avec écarts documentés.*
2. **Cartographie des établissements humains** : localités, empreintes de bâtiments (N1), routes principales.
3. **Imports sectoriels** (N3) : établissements scolaires et sanitaires, titres miniers, concessions forestières, aires protégées, réseau électrique HT, ports, aéroports, gares et voies ferrées.

### Phase 2 — Pilote de terrain (3 communes)
Profils suggérés :
- **Urbaine** (un arrondissement de grande ville) : densité, informel, foncier titré ;
- **Rurale agricole** : chefferies, terres coutumières, pistes rurales ;
- **Rurale forestière ou minière** : concessions, ressources, communautés, enjeux de droits superposés.

Dans chacune : N2 sur tous les inventaires, interface chef de village, point focal communal,
validation par les services déconcentrés, fiche territoriale et calcul des déficits.

**Critère de choix sécuritaire** : écarter du pilote les zones où la présence d'agents de terrain ou la
collecte de certaines données pourrait exposer les personnes à des risques (l'appréciation relève des
autorités compétentes et des partenaires sur place).

### Phase 3 — Évaluation et décision de passage à l'échelle
Mesurer, avant toute extension :

| Indicateur | Pourquoi |
|---|---|
| Coût par km², par bâtiment, par établissement vérifié | Construire un budget national crédible |
| Taux d'erreur de N1 mesuré par échantillon N2 | Décider où N2 peut être échantillonné plutôt qu'exhaustif |
| Taux de rapprochement avec les registres sectoriels | Mesurer la qualité des sources officielles |
| Délai moyen de validation N3 | Le goulot d'étranglement probable est administratif, pas technique |
| Utilisation effective (nombre de décisions s'appuyant sur la plateforme) | La vraie preuve de valeur |
| Taux de participation des chefs et réponse à leurs signalements | Viabilité de la « sentinelle » |
| Calibration du score de confiance | Rendre le score défendable |

### Phase 4 — Extension progressive
Par vagues régionales, en commençant par la cartographie (N1 + N3), le terrain N2 étant ciblé par la
file d'anomalies et l'échantillonnage.

### Phase 5 — Recensement et mise à jour continue
- Le **recensement de la population** utilise la cartographie produite (zones de dénombrement, listes
  de bâtiments), sous la responsabilité de l'institution compétente. C'est un **apport direct** au
  recensement, pas une substitution.
- Mise à jour continue : détection de changements par imagerie, signalements N0, imports périodiques
  des registres, et état civil lorsque sa couverture le permettra.

## 3. Calendrier et budget

**Non estimés dans ce document.** Toute donnée chiffrée à ce stade serait inventée. Les principaux
facteurs de coût sont connus : imagerie (achat ou accès), nombre d'agents × jours terrain, terminaux,
hébergement souverain, développement, formation, et surtout le temps institutionnel de validation.
La phase 2 a précisément pour objet de produire des coûts unitaires réels.

## 4. Ancrage stratégique

Le module INTELLIGENCE peut être présenté comme un outil de mise en œuvre et de suivi territorial de la
stratégie nationale de développement (SND30) et de la décentralisation, ce qui donne au projet un
« propriétaire » politique naturel (planification) en plus des institutions techniques.
