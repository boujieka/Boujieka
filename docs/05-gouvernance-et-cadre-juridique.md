# 05 — Gouvernance des données, sensibilité et cadre juridique

C'est la partie la plus sous-estimée du concept initial, et probablement celle qui décidera de
l'acceptation du projet. Une base qui relie **personnes, terres, ressources, communautés et
infrastructures critiques** est un outil de planification puissant — et un outil de contrôle tout
aussi puissant si elle est mal gouvernée.

## 1. Classes de sensibilité

| Classe | Contenu typique | Accès | Diffusion |
|---|---|---|---|
| **S0 — Public** | Découpage administratif, routes, établissements publics, occupation du sol, agrégats de population respectant les seuils | Tous | Données ouvertes possibles |
| **S1 — Restreint** | Droits fonciers nominatifs (selon la loi), infrastructures critiques, signalements de conflits, localisation précise de certaines ressources | Administrations habilitées, par secteur | Non |
| **S2 — Confidentiel** | Microdonnées du recensement, données d'état civil nominatives | Institution responsable uniquement, dans l'enclave | Jamais ; agrégats seulement |
| **S3 — Protégé culturel** | Forêts sacrées, objets rituels, savoirs traditionnels désignés comme tels par la communauté | Selon accord avec la communauté | Selon accord ; par défaut non localisé publiquement |

## 2. Principes

1. **Finalité** : chaque catégorie de données a une finalité écrite ; un nouvel usage nécessite une décision formelle.
2. **Minimisation** : on ne collecte pas ce dont aucune finalité n'a besoin (ex. ethnie, religion des personnes : *ne pas collecter* dans l'atlas).
3. **Cloisonnement** : enclave statistique séparée ; pas de jointure individu ↔ droit foncier dans la base commune.
4. **Agrégation sûre** : seuils minimaux par cellule et contrôle du risque de ré-identification par croisement.
5. **Traçabilité des accès** : journal inaltérable de qui a consulté quoi ; audit par une instance indépendante.
6. **Souveraineté** : hébergement sur le territoire national ou dans un cadre juridique validé par l'État ; réversibilité contractuelle ; code et formats ouverts pour éviter l'enfermement propriétaire.
7. **Contestabilité** : toute personne ou communauté peut contester une information la concernant, avec un circuit de traitement.
8. **Neutralité juridique** : la plateforme n'établit aucun droit ; l'affichage d'une information foncière n'a pas valeur de preuve.

## 3. Cadre juridique et institutionnel camerounais — à vérifier

Les éléments ci-dessous sont **de mémoire** et **n'ont pas été vérifiés sur les textes officiels** dans
le cadre de ce document. Ils doivent faire l'objet d'une revue juridique avant toute présentation
institutionnelle.

| Domaine | Élément pertinent (à vérifier) | Conséquence pour le projet |
|---|---|---|
| Recensement | Le **BUCREP** (Bureau central des recensements et des études de population) est chargé des recensements généraux | L'enclave population doit être sous sa responsabilité ou en partenariat formel |
| Statistique | L'**INS** (Institut national de la statistique) ; loi régissant l'activité statistique et le secret statistique (référence exacte à vérifier) | Respect du secret statistique, conditions de diffusion des agrégats |
| Données personnelles | Le Cameroun aurait adopté **fin 2024 une loi sur la protection des données à caractère personnel** (numéro, date et décrets d'application à vérifier) ; loi de 2010 sur la cybersécurité et la cybercriminalité | Base légale des traitements, autorité de contrôle, transferts hors du pays |
| Foncier | Régime foncier et domanial issu des **ordonnances de 1974** (à vérifier) ; administration : **MINDCAF** | Seul le titre foncier/l'administration fait foi ; statut des terres coutumières non titrées à traiter avec prudence |
| Cartographie officielle | **INC** (Institut national de cartographie) | Référentiel géodésique et cartographique ; limites officielles |
| Chefferies traditionnelles | Organisation des chefferies par décret de **1977** (classement en degrés — à vérifier) ; tutelle : **MINAT** | Attributs officiels de la chefferie = acte de reconnaissance |
| Mines | Code minier (révisé récemment — version en vigueur à vérifier) ; **MINMIDT**, cadastre minier | Les titres miniers sont importés de la source officielle |
| Forêts / faune | **MINFOF** ; régime des forêts communautaires et concessions | Idem |
| Décentralisation | Code général des collectivités territoriales décentralisées (2019, à vérifier) ; **MINDDEVEL** | Rôle des communes et régions comme utilisateurs et contributeurs |
| Planification | **MINEPAT** ; Stratégie nationale de développement **SND30** (2020-2030) | Ancrage stratégique du module INTELLIGENCE |
| Patrimoine culturel | **MINAC** | Classement et protection du patrimoine |

## 4. Gouvernance proposée

- **Comité de pilotage interministériel** (planification, territoire, domaines, statistique, cartographie, décentralisation, secteurs).
- **Propriétaire des données** : chaque couche a un *propriétaire institutionnel* (ex. carte scolaire → ministère de l'éducation) qui valide et fixe la diffusion.
- **Opérateur technique** : exploite la plateforme, sans droit de propriété sur les données ni droit de réutilisation commerciale non autorisée.
- **Comité éthique et patrimoine** incluant des représentants des autorités traditionnelles pour la classe S3.
- **Audit indépendant** des accès et de la sécurité.

## 5. Données ouvertes et licences des sources

- Les données OpenStreetMap sont sous licence **ODbL** (partage à l'identique pour les bases dérivées) :
  l'intégration doit être conçue pour respecter cette obligation (ex. couche séparée), ce qui peut entrer
  en tension avec une diffusion restreinte.
- Les jeux d'empreintes de bâtiments et de population maillée ont chacun leur licence : **à inventorier** en phase 0.
