# 06 — Intelligence territoriale

## 1. Moteur de rapprochement

Objectif : relier des enregistrements qui décrivent le même objet réel dans des sources différentes,
puis mesurer et expliquer les écarts.

Étapes :
1. **Normalisation** : nomenclatures communes, géométries projetées dans un même référentiel, noms normalisés (variantes orthographiques, langues).
2. **Appariement** : proximité spatiale + similarité des attributs (type, nom, code sectoriel). Les méthodes peuvent aller de règles simples à de l'apprentissage automatique ; **les règles explicables d'abord**, l'IA ensuite là où elle apporte un gain mesuré.
3. **Classement** : apparié / probable (à vérifier) / présent dans une seule source.
4. **File d'anomalies** : chaque écart significatif devient une tâche de vérification affectée (N2 ou N3).

L'IA intervient surtout à trois endroits : extraction depuis l'imagerie (N1), appariement flou de noms
et d'entités, priorisation des vérifications. Elle **ne valide jamais** une information juridique.

## 2. Score de confiance territorial — version explicable

Le concept initial produisait « 94/100 » sans méthode. Proposition : un score **par couche et par
unité territoriale**, décomposé en quatre composantes publiées avec le score.

| Composante | Question | Mesure possible |
|---|---|---|
| **C — Couverture** | Le territoire a-t-il été entièrement observé ? | Part de la surface couverte par une imagerie récente / visitée sur le terrain |
| **A — Accord entre sources** | Les sources concordent-elles ? | 1 − (écart relatif moyen entre sources indépendantes), ou taux d'appariement |
| **F — Fraîcheur** | Les données sont-elles récentes ? | Décroissance selon l'âge, avec une demi-vie propre à chaque couche (un bâtiment change plus vite qu'un pont) |
| **V — Vérification** | Quelle part est vérifiée sur le terrain ou validée ? | Part pondérée des objets OBSERVÉS/VALIDÉS ; taux d'erreur mesuré par échantillon |

`Score = 100 × (wC·C + wA·A + wF·F + wV·V)`, avec des poids **par défaut égaux** et **à calibrer**
pendant le pilote (en comparant le score au taux d'erreur réellement mesuré sur échantillon terrain).
Tant que cette calibration n'est pas faite, le score est un **indicateur de priorisation**, pas une
mesure de qualité certifiée.

### Exemple (reprise des chiffres du concept)

| Source | Bâtiments | Remarque |
|---|---|---|
| Extraction imagerie | 1 237 | date de l'image : à connaître |
| Couche SIG consolidée | 1 240 | |
| Commune | 1 180 | date et méthode inconnues |
| Chef de village | +31 constructions nouvelles | déclaratif |

Lecture correcte : imagerie et SIG concordent (écart 0,2 %) ; la commune est en retrait d'environ 5 %,
ce qui peut s'expliquer par l'**ancienneté** de son inventaire ; les 31 constructions signalées par le chef
**sont peut-être déjà comptées** dans l'imagerie si celle-ci est postérieure. On ne peut pas les additionner
sans connaître les dates. → Tâche générée : vérifier sur le terrain les 31 signalements et un échantillon
de bâtiments présents dans l'imagerie mais pas à la commune.

Affichage : `Habitat : 78/100 (C 0,95 · A 0,80 · F 0,70 · V 0,65) — 2 anomalies ouvertes`
*(valeurs illustratives, pas calculées)*.

## 3. « Qu'est-ce qui manque ? » — calcul des déficits

C'est la fonctionnalité la plus vendable. Elle est aussi la plus exposée à la critique si elle repose
sur des ratios inventés. Trois règles :

**Règle 1 — Normes officielles uniquement.** Le besoin est calculé à partir de **normes paramétrées et
sourcées** (carte scolaire, carte sanitaire, politiques d'eau et d'électricité, normes de desserte
routière), saisies par les ministères. Si aucune norme officielle n'existe, la plateforme l'indique et
peut proposer une norme de référence internationale **étiquetée comme telle**.

**Règle 2 — Accessibilité, pas seulement nombre.** « 1 école pour 4 800 habitants » ne dit rien si
l'école est à 12 km sans route praticable. Indicateur complémentaire : **part de la population à moins
de X minutes** d'un équipement fonctionnel, calculée sur le réseau routier réel (avec état et saisonnalité).

**Règle 3 — Capacité et état, pas seulement présence.** Une école en ruine ou un centre de santé sans
personnel ne couvre pas le besoin.

### Exemple corrigé

```
Village <nom> — population estimée 4 800 (intervalle 4 300–5 300)

ÉDUCATION PRIMAIRE
  Enfants d'âge scolaire estimés : [part officielle × population]   ← paramètre démographique
  Capacité existante : 1 école, 6 salles, état : dégradé
  Norme appliquée : [élèves/salle selon norme sectorielle]          ← paramètre à saisir par le ministère
  Déficit : N salles  (et non « 2 écoles » sans justification)
  Accès : 62 % des enfants à moins de 30 min à pied               ← illustratif

SANTÉ
  Formation sanitaire fonctionnelle la plus proche : 14 km (piste dégradée en saison des pluies)
  → déficit d'accès CRITIQUE selon seuil [à définir]

EAU POTABLE        38 % des ménages (source : [enquête/recensement, date])
ÉLECTRICITÉ        17 % des ménages (source : [ ], date)
ROUTES             12 km praticables toute l'année ; besoin : selon norme [ ]
```

Les pourcentages d'accès à l'eau et à l'électricité ne sont **pas observables par imagerie** : ils
proviennent du recensement ou d'enquêtes ménages, ou des fichiers clients des opérateurs (sous accord).

## 4. Du déficit à l'investissement

Sortie finale du module : une **liste priorisée** d'investissements par commune, avec pour chacun :
population bénéficiaire estimée, déficit couvert, coût unitaire de référence (fourni par le ministère),
niveau de confiance des données sous-jacentes. Les arbitrages restent politiques ; la plateforme rend
les critères explicites et comparables.

## 5. Horizon « jumeau numérique »

Une fois les couches stabilisées et mises à jour régulièrement, des fonctions de simulation deviennent
possibles : impact d'une nouvelle route sur l'accessibilité, projection démographique par localité,
scénarios d'électrification. C'est un objectif de phase ultérieure, à ne pas promettre dans le pilote.
