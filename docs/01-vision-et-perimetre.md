# 01 — Vision, périmètre et positionnement

## 1. Reformulation du concept

Le projet n'est plus une application de recensement de la population. C'est une
**infrastructure nationale de connaissance du territoire**, qui répond à cinq questions pour chaque
localité :

| Question | Inventaires concernés |
|---|---|
| **Qui** vit ici ? | Population & habitat |
| **Qu'est-ce qui** existe ici ? | Foncier, infrastructures sociales et physiques, activités économiques, ressources, patrimoine |
| **À qui / sous quel régime** ? | Droits fonciers, concessions, permis, statut coutumier — *seulement lorsqu'une source juridique l'établit* |
| **Dans quel état / comment est-ce utilisé** ? | Mesures d'état, de capacité, de fréquentation, de production |
| **Qu'est-ce qui manque** ? | Intelligence territoriale (déficits par rapport à des normes officielles) |

## 2. Ce que la plateforme est — et n'est pas

**Elle est :**
- un **registre géospatial intégré** de référence, alimenté par plusieurs sources ;
- un **outil de rapprochement** qui rend visibles les contradictions entre sources ;
- un **outil de planification** (déficits, accessibilité, priorisation des investissements).

**Elle n'est pas :**
- un **cadastre** : elle ne crée pas de droits fonciers, elle référence ceux qu'établissent les autorités compétentes ;
- un **état civil** : elle ne délivre pas d'actes ;
- un **fichier de surveillance** : les données nominatives du recensement ne sont pas consultables dans l'atlas ;
- au départ, un **jumeau numérique** au sens strict (simulation dynamique). C'est un horizon.

Cette distinction est un argument de vente, pas une limite : elle évite que la plateforme entre en
concurrence frontale avec les institutions qui détiennent des mandats légaux (recensement, cadastre,
statistique, cartographie), et en fait au contraire leur **outil commun**.

## 3. Architecture produit

| Module | Contenu | Utilisateurs principaux |
|---|---|---|
| **PEOPLE** | Habitat, ménages, population (agrégats), dynamique démographique | Institution de recensement, statistique, communes |
| **LAND** | Unités foncières, occupation du sol, droits et concessions référencés | Domaines/cadastre, agriculture, forêts, communes |
| **ASSETS** | Infrastructures sociales et physiques, patrimoine, chefferies | Ministères sectoriels, communes, chefferies |
| **RESOURCES** | Ressources naturelles, mines, forêts, eau, énergie, activités économiques | Mines, énergie, forêts, planification, investisseurs |
| **INTELLIGENCE** | Rapprochement, score de confiance, déficits, accessibilité, tableaux de bord | Planification, bailleurs, communes, Présidence/Primature |

Transversal : **Référentiel territorial** (découpage administratif versionné), **Gouvernance des
accès**, **Traçabilité des sources**.

## 4. Proposition de valeur par client

Un projet aussi large échoue s'il ne sait pas *qui paie et pourquoi*. Hypothèses à valider :

| Client | Douleur | Ce qu'il achète |
|---|---|---|
| Ministère de la planification | Pas de base fiable pour cibler les investissements publics | INTELLIGENCE + fiches territoriales |
| Institution de recensement | Préparation coûteuse de la cartographie censitaire | Cartographie des bâtiments et zones de dénombrement (PEOPLE) |
| Communes (décentralisation) | Pas d'inventaire de leur patrimoine ni de leur assiette fiscale locale | Fiche communale, inventaire des équipements |
| Ministères sectoriels | Cartes scolaire/sanitaire/électrique non à jour | Couches ASSETS sectorielles |
| Bailleurs / partenaires techniques | Ciblage et suivi des projets | Accès institutionnel aux indicateurs |
| Investisseurs privés | Manque d'information sur sites, accès, énergie | Couches publiques RESOURCES / ASSETS (pas de données personnelles) |

**Point faible à reconnaître :** un modèle où un acteur privé détient le « jumeau numérique » d'un
pays est politiquement difficile à vendre. Le modèle recommandé : **l'État est propriétaire des données
et de l'infrastructure d'hébergement ; l'opérateur fournit la technologie, la méthode et le service**,
avec réversibilité contractuelle.

## 5. Nom du produit

« POPGRID » : un **POPGRID Data Collaborative** existe, à ma connaissance, comme collectif international
de producteurs de données de population maillées (CIESIN / Université Columbia et partenaires).
**Cela n'a pas été vérifié dans cette session** ; si c'est confirmé, le nom expose à une confusion,
voire à un conflit de marque. Par ailleurs « POP » réduit le produit à la population, ce que le
concept affiné dépasse justement.

Pistes à tester (disponibilité de marque et de domaine non vérifiée) : un nom qui évoque le
territoire plutôt que la population, bilingue français/anglais, et prononçable localement.

## 6. Positionnement par rapport à l'existant

Initiatives et données comparables (à intégrer comme sources, pas à concurrencer) :
- **GRID3** (données géoréférencées d'infrastructures et de démographie, plusieurs pays africains) ;
- **WorldPop** (estimations maillées de population) ;
- **OpenStreetMap** et **Humanitarian OpenStreetMap Team** ;
- empreintes de bâtiments issues d'imagerie (Google Open Buildings, Microsoft Building Footprints) ;
- cartes d'occupation du sol (ex. ESA WorldCover) et de couvert forestier (Global Forest Watch) ;
- l'Atlas forestier interactif du Cameroun (WRI / ministère des forêts) ;
- les publications de l'ITIE si le pays y adhère (rapports sur les revenus extractifs).

La couverture précise de chacune de ces sources pour le Cameroun **n'a pas été vérifiée ici** et doit
faire l'objet d'un inventaire des sources en phase 0 (voir [07](07-pilote-cameroun.md)).

**Différenciation réaliste** : ce qui manque généralement n'est pas une carte de plus, mais
(1) l'intégration multi-sectorielle autour d'un référentiel territorial unique, (2) la validation
institutionnelle et communautaire, (3) la traçabilité de chaque information, (4) la mise à jour continue.
