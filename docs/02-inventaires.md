# 02 — Les inventaires

Le concept initial annonçait 8 inventaires, mais le 8ᵉ (« Digital Twin ») était le résultat de
l'intégration, pas un inventaire. Version affinée : **7 inventaires thématiques + 1 couche
transversale**. Les listes de types détaillées sont dans [`nomenclatures/`](../nomenclatures/).

Pour chaque inventaire, on précise : **l'unité d'observation**, **la source de vérité juridique**
(qui fait foi) et **la sensibilité** (S0 à S3, voir [05](05-gouvernance-et-cadre-juridique.md)).

---

## I1 — Population & habitat

| Élément | Unité | Fait foi | Sensibilité |
|---|---|---|---|
| Bâtiments (empreinte, usage, état, occupation) | Bâtiment | Observation (imagerie + terrain) | S0 (géométrie), S1 (usage détaillé) |
| Logements | Logement | Recensement | S1 |
| Ménages, personnes | Ménage / individu | **Institution de recensement** (secret statistique) | **S2** — jamais dans l'atlas |
| Population agrégée, densité, structure par âge/sexe | Unité territoriale ou maille | Institution de recensement / statistique | S0 si seuils de confidentialité respectés |
| Naissances, décès | Événement | **État civil** | S2 (nominatif), S0 (agrégé) |
| Migrations, déplacés internes, réfugiés | Agrégat | Statistique / organismes compétents | **S1 à S3** selon contexte sécuritaire |

> **Correction importante** : « résidents / non-résidents » et « migrations » ne peuvent pas être mis
> à jour en continu par la plateforme seule. La mise à jour continue de la population suppose un
> état civil à couverture élevée ; à défaut, entre deux recensements, la population est **estimée par
> modèle** (bâtiments × occupation × taille moyenne des ménages), avec un intervalle d'incertitude
> affiché. Le recensement reste nécessaire.

## I2 — Foncier & occupation des terres

Deux notions distinctes, souvent confondues :

- **Occupation / usage du sol** (ce qu'on observe) : agricole, forestier, pastoral, résidentiel,
  commercial, industriel, minier, plan d'eau, zone humide, etc. → observable par imagerie, vérifiable sur le terrain.
- **Régime juridique** (ce que dit le droit) : domaine public, domaine privé de l'État, domaine
  national, propriété privée titrée, terres coutumières, aire protégée, concession, permis… →
  **seule l'administration compétente fait foi**.

Une même parcelle peut être « agricole » (usage) sur une « concession forestière » (régime) revendiquée
par une communauté (droit coutumier déclaré). Le modèle doit pouvoir porter les trois sans les fusionner.

Champs « propriétaire / détenteur / concessionnaire / durée / superficie / statut » : **uniquement
lorsqu'une source juridique les établit**, avec référence de l'acte. Les déclarations communautaires
sont conservées comme *déclarations*, distinctes des droits validés.

## I3 — Chefferies, patrimoine et communautés

Structure par chefferie (affinée) :

```
CHEFFERIE
├── identification : nom, degré/classement officiel, rattachement administratif
├── autorité : titulaire actuel (S1), date d'intronisation, acte de reconnaissance
├── territoire traditionnel : géométrie DÉCLARÉE (≠ limites administratives, souvent contestée)
├── population desservie (agrégat dérivé, pas déclaratif)
├── patrimoine matériel : palais, sites historiques, lieux de mémoire, objets
├── patrimoine naturel : forêts sacrées, sources, rochers, bois rituels
├── patrimoine immatériel : fêtes, rites, langues, savoir-faire
└── niveau de diffusion par élément : public / restreint / protégé (décidé AVEC la communauté)
```

Points d'attention :
- les **limites des territoires traditionnels** ne coïncident pas avec le découpage administratif et
  peuvent se chevaucher → stocker comme couche déclarative distincte, ne jamais la publier comme limite officielle ;
- la **succession** à la tête d'une chefferie peut être contestée → historiser, ne pas trancher ;
- certains savoirs ou lieux ne doivent pas être localisés publiquement (risque de pillage d'objets, de
  profanation, d'exploitation) → classe **S3** avec consentement communautaire.

## I4 — Activités économiques

- **Industrie** : usines, unités de transformation, zones industrielles/économiques, entrepôts, plateformes logistiques, centrales, installations pétrolières et gazières.
- **Mines et carrières** : sites, titres miniers (référencés au cadastre minier), substances, titulaires, statut d'exploitation, production déclarée.
- **Agriculture, élevage, pêche** : plantations, exploitations, cultures, élevage, pisciculture, agro-industries, périmètres irrigués.
- **Commerce et services** : marchés, commerces, services financiers (agences, points de mobile money), hôtellerie.
- **Économie informelle** : à recenser de manière agrégée (nombre d'unités par type et par zone) plutôt qu'unité par unité — le coût et la volatilité rendent un registre nominatif peu réaliste.

Fait foi : registres d'entreprises, administrations sectorielles (permis, licences, agréments).
Observation terrain = existence et activité constatées, pas statut légal.

## I5 — Ressources naturelles

Chaîne de valeur à modéliser (reprise du concept, avec la notion de statut de connaissance) :

```
Ressource identifiée (indice / gisement estimé / réserve prouvée)
  → localisation (précision connue)
  → statut juridique (domaine, aire protégée…)
  → titre/concession (référence, titulaire, dates)
  → opérateur
  → exploitation (statut, production déclarée)
  → infrastructures associées
  → revenus déclarés (sources fiscales / ITIE)
```

**Correction** : « revenus potentiels » est une projection, pas une donnée. Elle relève de l'analyse
(module INTELLIGENCE), avec hypothèses explicites, et ne doit pas être stockée comme attribut factuel.

Sensibilité : la localisation précise de certains gisements ou de certaines ressources stratégiques
peut relever de S1 (accès restreint) — décision à prendre avec les ministères concernés.

## I6 — Infrastructures sociales

Éducation, santé, mais aussi (manquants dans la version précédente) : **état civil** (centres),
**administration** (sous-préfectures, mairies), **sécurité** (selon règles de confidentialité),
**lieux de culte**, **marchés**, **équipements sportifs et culturels**, **cimetières**.

Fiche standard par établissement (affinée) :

| Bloc | Champs | Remarque |
|---|---|---|
| Identification | nom, type, niveau, statut public/privé/confessionnel/communautaire, code officiel sectoriel | Le code sectoriel (carte scolaire, carte sanitaire) est la clé de rapprochement |
| Localisation | point, adresse, unité territoriale | |
| Capacité | places, lits, salles | |
| Personnel | effectifs par catégorie | Agrégé, pas nominatif |
| Fréquentation | élèves inscrits, consultations | Source sectorielle |
| Équipements | eau, électricité, sanitaires, internet | |
| État | bon / dégradé / hors service, date de constat | |
| Desserte | population dans un rayon / temps d'accès | **Calculé**, pas saisi |

## I7 — Infrastructures physiques

Transport (routes par classe et état, pistes rurales, ponts, ports, aéroports, gares, voies ferrées,
bacs), énergie (centrales, postes, lignes par tension, mini-réseaux, solaire), eau (barrages, forages,
réseaux, stations, réservoirs), télécommunications (antennes, fibre, centres de données, couverture).

Spécificité : beaucoup d'infrastructures sont **linéaires** (routes, lignes, réseaux) → le modèle doit
supporter des géométries linéaires segmentées avec un état par tronçon.

**Sensibilité** : les infrastructures critiques (postes électriques, nœuds télécoms, centres de données)
peuvent nécessiter un niveau S1 — à arbitrer avec les autorités de sécurité.

## T — Couche transversale : risques & environnement

Manquait dans le concept initial :
- zones inondables, glissements de terrain, érosion côtière, sécheresse ;
- déforestation et dégradation (détection de changements) ;
- pollution, sites contaminés ;
- zones d'insécurité (S1/S2, usage strictement opérationnel) ;
- conflits fonciers signalés (S1, transmis aux autorités compétentes).

Ces données sont indispensables au calcul des besoins (une école en zone inondable n'est pas une école disponible toute l'année).
