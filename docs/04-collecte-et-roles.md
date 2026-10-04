# 04 — Collecte, niveaux de vérification et rôles

## 1. Trois niveaux de collecte (repris et précisés)

| Niveau | Méthode | Produit | Statut max. de l'assertion | Coût unitaire relatif |
|---|---|---|---|---|
| **N1 — Télédétection** | Imagerie satellite/drone, extraction automatique, données ouvertes | Empreintes de bâtiments, routes, occupation du sol, plans d'eau, changements | DÉTECTÉ | Faible |
| **N2 — Vérification terrain** | Agents avec application mobile hors-ligne, GPS, photos | Usage, occupation, état, nom, type d'établissement | OBSERVÉ | Moyen à élevé |
| **N3 — Vérification administrative** | Import et rapprochement de registres officiels, validation par l'autorité | Titres, concessions, permis, licences, statut juridique | VALIDÉ | Variable (dépend de la qualité des registres) |
| **N0 — Déclaration** *(ajouté)* | Chefs, communes, citoyens, entreprises | Signalements, nouveaux objets, contestations | DÉCLARÉ | Très faible |

**Ajout** : le niveau N0 (déclaration) est distinct et n'est pas une vérification. Il sert à
**prioriser** le travail N1/N2, pas à établir des faits.

**Principe d'échantillonnage** : le N2 n'a pas besoin d'être exhaustif partout. Là où N1 et N3
concordent, un **échantillon aléatoire** de vérification terrain suffit à mesurer la qualité ; la
vérification exhaustive est réservée aux zones de discordance, de changement rapide ou d'enjeu fort.
C'est le principal levier de maîtrise des coûts.

## 2. Rôles

| Rôle | Missions | Peut créer | Peut valider | Ne peut pas |
|---|---|---|---|---|
| **Agent SIG** | Cartographie N1, contrôle des extractions automatiques | Objets DÉTECTÉS | Qualité géométrique | Valider un statut juridique |
| **Agent de recensement** | Dénombrement ménages/personnes | Données de l'enclave statistique | — | Accéder aux données foncières nominatives |
| **Agent économique** | Unités économiques, exploitations | Objets OBSERVÉS | — | Valider un permis ou une licence |
| **Agent infrastructures** | Écoles, santé, eau, énergie, routes | Objets OBSERVÉS, mesures d'état | — | — |
| **Référent communautaire** | Signalement, accompagnement des agents | Déclarations (N0) | — | Valider des droits |
| **Point focal communal** *(ajouté)* | Inventaire du patrimoine communal, état civil, voirie | Déclarations, imports | Données relevant de la compétence communale | — |
| **Validateur sectoriel** *(ajouté)* | Agent habilité d'un ministère | Imports N3 | **Statuts juridiques de son secteur** | Valider hors de son secteur |
| **Superviseur territorial** | Contrôle qualité, arbitrage des anomalies, suivi des agents | — | Qualité des observations N2 | Valider des droits |

Cumul de fonctions en zone rurale : **oui**, mais avec deux garde-fous :
- **séparation des données** : un agent qui cumule recensement et cartographie utilise deux espaces
  applicatifs distincts (le cumul de rôles ne doit pas ouvrir de jointure entre microdonnées et foncier) ;
- **pas d'auto-contrôle** : un agent ne peut pas être le superviseur de ses propres observations.

## 3. Le chef de village comme « sentinelle territoriale »

> **Mise à jour (octobre 2026)** : depuis le 1ᵉʳ avril 2026, une lettre-circulaire du MINDCAF du
> 20 février 2026 permet aux chefs de 3ᵉ degré de **délivrer** des attestations foncières (ARDFC,
> AJPTER) qui valent « commencement de preuve » sur le domaine national. Le chef n'est donc plus
> seulement déclarant : il est aussi **autorité émettrice d'actes intermédiaires**. Ce ne sont pas des
> titres fonciers. Voir [05 §3.3](05-gouvernance-et-cadre-juridique.md#33-conséquences-de-la-circulaire-foncière-de-février-2026).
> Dans la plateforme, les deux rôles (sentinelle N0 / émetteur d'attestations N3) sont des comptes et
> des traces distincts.

L'idée est bonne et se défend bien, à condition de traiter les risques que la version initiale ne mentionnait pas.

**Interface proposée** : carte simplifiée de son territoire, pré-remplie par N1, avec trois actions
seulement : **« Il manque quelque chose »**, **« Ceci n'existe plus / a changé »**, **« Je signale un
problème »** (conflit, dégradation, risque). Utilisable hors-ligne, par photo + point + catégorie,
éventuellement par message vocal ou par l'intermédiaire d'un relais (téléphone simple, USSD) là où les
smartphones manquent.

| Risque | Description | Mesure |
|---|---|---|
| **Conflit d'intérêts** | Le chef est souvent partie prenante dans l'attribution coutumière des terres et dans les litiges ; ce risque augmente avec son pouvoir de délivrer des ARDFC/AJPTER | Ses signalements fonciers sont des **déclarations** affichées comme telles. Ses attestations sont enregistrées comme attestations, jamais comme titres. Détection automatique des attestations qui se chevauchent entre elles ou avec des titres et des concessions. Contradiction possible par d'autres acteurs |
| **Légitimité contestée** | Successions disputées, chefferies concurrentes sur un même territoire | Historisation, rattachement à l'acte officiel de reconnaissance ; pas de « chef unique » imposé par la plateforme |
| **Exposition** | Un chef qui signale une occupation illégale ou une exploitation minière informelle peut être menacé | Signalements sensibles en **S1**, transmis à l'autorité sans publication ; possibilité de signalement non public |
| **Incitations** | Pourquoi le chef consacrerait-il du temps ? Risque inverse : gonfler les chiffres pour obtenir des équipements | Retour visible (fiche du village, déficits identifiés) ; les chiffres déclarés n'alimentent **jamais directement** les calculs de besoins sans vérification |

## 4. Application de terrain — exigences minimales

- fonctionnement **hors-ligne** complet, synchronisation différée ;
- formulaires **paramétrés par nomenclature** (pas de codage en dur) ;
- capture GPS avec précision enregistrée, photo horodatée ;
- bilingue français/anglais (pays bilingue), extensible aux langues locales pour les interfaces simples ;
- chiffrement local des données, effacement à distance des terminaux perdus ;
- contrôles de cohérence à la saisie (doublons spatiaux, valeurs aberrantes).

Des outils open source existent pour la collecte (ex. ODK, KoboToolbox) et pourraient servir au pilote
avant de développer une application propre ; à évaluer en phase 0.
