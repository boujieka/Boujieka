# 07 — Pilote Cameroun

## 1. Ce qui change par rapport au plan initial

Le plan initial enchaînait 7 étapes à l'échelle nationale (découpage → localités → foncier → actifs →
validation → recensement → intelligence). L'ordre est pertinent (cartographier avant de dénombrer),
mais l'exécuter d'emblée sur tout le pays revient à lancer le programme complet sans preuve de méthode
ni de coût.

**Proposition : deux vitesses.**
- **Socle national léger** : uniquement ce qui est peu coûteux et utile partout (N1 + imports N3).
- **Pilote de terrain approfondi** : toutes les couches, N0 à N3, dans **3 communes contrastées**.

Le pays compte **10 régions, 58 départements et 360 arrondissements** (INS), ainsi que **374 collectivités
territoriales décentralisées : 360 communes et 14 communautés urbaines**, auxquelles s'ajoutent les régions.
En décembre 2025, le MINAT a demandé aux gouverneurs des propositions de **nouveaux départements et
arrondissements** : le découpage est susceptible de changer pendant le projet. C'est une raison de plus
pour un référentiel territorial **versionné**.

> **Contexte recensement (octobre 2026)** : le **4ᵉ RGPH, couplé au recensement général de l'agriculture
> et de l'élevage (RGAE)**, a été conduit par le BUCREP à partir du 24 avril 2026. Il a été prolongé deux fois :
> au 31 juillet, puis par une période de rattrapage du 1ᵉʳ août au 15 septembre 2026. Selon la presse, le
> budget initial était de 13,3 milliards FCFA (État + appui de la Banque mondiale), avec 6 milliards FCFA
> supplémentaires mobilisés ensuite. Les retards ont été attribués à la logistique, à l'enclavement et à la
> rémunération des agents. **Les résultats ne sont pas encore publiés** à ma connaissance.
> Conséquence : la plateforme ne « prépare » plus ce recensement. Elle doit être conçue pour
> **recevoir ses agrégats et sa cartographie censitaire** (sous accord avec le BUCREP), et pour préparer les
> mises à jour intercensitaires. Les difficultés de terrain observées (enclavement, routes dégradées) sont
> précisément ce que les couches ASSETS/INF doivent documenter.

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

### Phase 5 — Intégration du recensement et mise à jour continue
- **Intégration du 4ᵉ RGPH/RGAE 2026** : import des agrégats publiés et, sous convention avec le BUCREP,
  de la cartographie censitaire (zones de dénombrement). Le volet agricole (RGAE) alimente directement la
  couche LAND/agriculture.
- **Prochain recensement** : la cartographie produite (zones de dénombrement, listes de bâtiments) le
  prépare, sous la responsabilité de l'institution compétente. C'est un **apport direct** au recensement,
  pas une substitution.
- **Visa statistique** (loi n° 2020/010) : toute enquête de terrain du pilote auprès des ménages ou des
  entreprises doit vérifier si elle y est soumise.
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
