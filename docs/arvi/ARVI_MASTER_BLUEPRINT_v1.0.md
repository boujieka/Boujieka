# ARVI — Africa Resource Value Intelligence
## Master Blueprint v1.0

*From Resources to Revenues. From Revenues to Investment.*
Signature méthodologique : **EXPORT → MIRROR → GAP → VALUE → INVESTMENT**

| | |
|---|---|
| Statut | Projet de conception. Aucune donnée ARVI n'a encore été collectée ni calculée. |
| Date | 2026-10-08 |
| Relation avec Cartouche | ARVI reprend les principes, le modèle de provenance et la pile technique de Cartouche (ce dépôt). Le choix entre un module de ce dépôt et un dépôt séparé reste ouvert (§14). |
| Avertissement | Information et analyse uniquement. Un écart statistique entre deux déclarations commerciales n'est ni une preuve de fraude, ni une perte avérée, ni une accusation visant une entreprise ou une personne. |

**Conventions de ce document**

- `[À VÉRIFIER]` signale un fait (code SH, licence, couverture d'une source) que l'équipe données
  doit confirmer sur la source primaire avant d'écrire du code qui en dépend.
- `[HYPOTHÈSE]` signale un choix de conception ou un paramètre provisoire, à calibrer sur données réelles.
- Aucun chiffre de résultat (écart, montant, part de marché) n'apparaît dans ce document : il n'y en a pas encore.

---

## Sommaire

1. Positionnement et limites
2. Principes non négociables (repris de Cartouche)
3. Modèle conceptuel et ses faiblesses connues
4. Architecture fonctionnelle : 12 modules
5. Sources de données internationales
6. Taxonomie produits et chaînes de transformation
7. Méthodologie de calcul
8. Modèle de confiance (ARVI Data Confidence)
9. Scorecard pays (ARVI-1 à ARVI-6)
10. Architecture de la base de données
11. Architecture technique
12. Modèle économique
13. Gouvernance, risques juridiques et règles de langage
14. Feuille de route et décisions ouvertes

---

## 1. Positionnement et limites

**Ce qu'ARVI est :** une infrastructure de mesure. Elle compare des déclarations commerciales
publiques, documente ce qui explique leurs écarts, isole un résidu non expliqué avec un niveau de
confiance, puis exprime ce résidu et le potentiel de transformation locale en ordres de grandeur
(recettes fiscales, équivalents d'investissement).

**Ce qu'ARVI n'est pas :**

- un détecteur de fraude ou de fuite illicite ;
- un outil d'enquête sur des entreprises (ARVI travaille au niveau pays × produit × partenaire × année,
  jamais au niveau d'une transaction ou d'une société) ;
- une prévision de ce qui « aurait été » investi.

**Phrase de positionnement proposée :**
> *ARVI measures how much of the value of Africa's natural resources is recorded, captured and
> transformed at home — and expresses the remaining gaps as fiscal and investment equivalents.*

---

## 2. Principes non négociables

Repris tels quels de Cartouche (`README.md`, `backend/app/models/enums.py`), car ils font la
crédibilité d'un produit de ce type.

| Principe | Application ARVI |
|---|---|
| **Source d'abord** | Chaque chiffre conserve sa lignée : source, jeu de données, version, URL, date de publication, date d'extraction, empreinte SHA-256 du fichier brut. |
| **Ne jamais inventer** | Un champ vide porte un statut : *Not disclosed* (la source ne le publie pas), *Not available* (pas de source), *Pending* (pas encore publié), *Confidential* (supprimé par le déclarant). |
| **Ne jamais mélanger les natures de valeur** | `FACT` = valeur déclarée (exports, imports miroir) ; `CALCULATION` = arithmétique déterministe sur des FACT (écart brut, valeur unitaire) ; `ESTIMATE` = tout ce qui dépend d'un paramètre modélisé (ajustement CAF/FAB, écart potentiel, fiscal, transformation, équivalents d'investissement, emplois) ; `AI_INTERPRETATION` = texte rédigé par un modèle, jamais une source. |
| **Langage neutre** | Aucun pays n'est « classé » ni « désigné ». Voir §13. |
| **Reproductibilité** | Chaque publication ARVI est liée à une version figée des données (`data_release`) et de la méthodologie (`methodology_version`). |

---

## 3. Modèle conceptuel et ses faiblesses connues

```
RESSOURCE NATURELLE → PRODUCTION → EXPORTS DÉCLARÉS → IMPORTS MIROIR
   → ÉCART COMMERCIAL OBSERVÉ → DÉCOMPOSITION (explications) → ÉCART RÉSIDUEL (Potential Value Gap)
   → ÉCART FISCAL ESTIMÉ ─┐
   → ÉCART DE TRANSFORMATION LOCALE (indépendant du miroir) ─┤
                                                             └→ ÉQUIVALENTS D'INVESTISSEMENT
```

Point de conception important : la chaîne linéaire du brief mélange **deux mesures de nature différente**.

1. **Écart de déclaration** (moteurs Trade Mirror + Value Gap) : la même marchandise est-elle déclarée
   pour la même valeur des deux côtés ?
2. **Écart de captation** (moteur Value Capture) : la marchandise est-elle exportée à un stade de
   transformation bas alors qu'un stade supérieur est techniquement possible ?

Elles ne s'additionnent pas. Les additionner dans un total unique compterait deux fois la même
tonne et mélangerait une question statistique avec une question de politique industrielle.
ARVI les présente donc côte à côte, jamais sommées.

**Faiblesses connues de la méthode miroir** (à documenter publiquement dans la note méthodologique) :

- Les imports sont généralement attribués au **pays d'origine**, les exports au **pays de dernière
  destination connue** : un minerai exporté vers un port de transit ou un négociant enregistré dans
  un hub (Suisse, Émirats, Pays-Bas, Singapour…) sera déclaré par un autre partenaire que celui attendu.
- Pétrole brut et GNL : la destination finale est souvent inconnue au chargement (cargaisons
  revendues en mer). La comparaison bilatérale y est structurellement faible ; ARVI s'appuiera
  davantage sur les volumes de production et les prix de référence que sur le miroir bilatéral.
- Or : distinction or monétaire / non monétaire, flux informels importants, données parfois
  confidentielles. Résultats à afficher avec une confiance par défaut plafonnée `[HYPOTHÈSE]`.
- La littérature a critiqué l'usage des écarts miroir comme mesure des flux financiers illicites
  (par exemple les travaux du Center for Global Development, 2018 `[À VÉRIFIER : référence exacte]`).
  ARVI doit citer ces critiques plutôt que les ignorer : c'est ce qui la distingue d'un chiffre militant.

---

## 4. Architecture fonctionnelle : 12 modules

| # | Module | Rôle | Nature des sorties |
|---|---|---|---|
| M01 | **Source Registry & Ingestion** | Registre des sources, téléchargement, empreinte SHA-256, archivage brut, extraction vers tables de staging, file de vérification | FACT (staging) |
| M02 | **Product Taxonomy** | Liste des ressources, codes SH par révision (HS2012/2017/2022), concordances, chaînes de transformation, teneurs en métal | Référentiel |
| M03 | **ARVI Trade Mirror** | Appariement export déclarant ↔ import partenaire par pays, produit, SH, année, partenaire ; écarts bruts valeur / quantité / valeur unitaire | CALCULATION |
| M04 | **Reconciliation Engine** | Décomposition de l'écart : CAF/FAB, décalage temporel, transit/réexport, classification, change, confidentialité → résidu | ESTIMATE |
| M05 | **Confidence Engine** | Score 0–100 et niveau 🟢/🟡/🔴 par cellule, avec raisons lisibles | CALCULATION (règles) |
| M06 | **Price & Unit Value Benchmarks** | Prix de référence internationaux, bandes de prix, valeur unitaire attendue | FACT (prix) + CALCULATION |
| M07 | **ARVI Value Capture** | Stade de transformation exporté, écart de valeur ajoutée locale (nette des coûts) | ESTIMATE |
| M08 | **Fiscal Engine** | Paramètres fiscaux par pays et ressource ; recettes associées à un écart (fourchette) | ESTIMATE |
| M09 | **ARVI Investment Translator** | Bibliothèque de coûts unitaires sourcés ; conversion en équivalents (MW, km, écoles…) et emplois | ESTIMATE |
| M10 | **Country & Resource Profiles / Scorecard** | Country Value Profile, Resource Cards, indicateurs ARVI-1 à ARVI-6 | Vue (mélange étiqueté) |
| M11 | **Reports, Monitor & Alerts** | Rapport trimestriel/mensuel, alertes sur nouvelles publications ou ruptures de série | Publication |
| M12 | **Access, API & Governance** | Clés API, rôles, offres (Public/Pro/Institutionnel), journal d'audit, versions de données et de méthode | Plateforme |

Les modules M01, M05 et M12 réutilisent directement le code Cartouche (`app/ingest`, `app/security`,
modèle de provenance). M03–M09 sont nouveaux.

---

## 5. Sources de données internationales

Statut de chaque source à confirmer en phase 0 : couverture africaine réelle, granularité, fréquence,
délai de publication et **licence de redistribution** (déterminante pour le modèle économique, §12).

### 5.1 Commerce bilatéral (cœur du miroir)

| Source | Contenu | Usage ARVI | Points d'attention |
|---|---|---|---|
| **UN Comtrade** (ONU, Division de statistique) | Commerce déclaré par pays, partenaire, code SH (jusqu'à 6 chiffres), valeur et quantité, annuel et mensuel | Source primaire FACT des deux côtés du miroir | Beaucoup de pays africains déclarent tard ou pas toutes les années ; conditions d'usage et limites de l'API `[À VÉRIFIER]` |
| **CEPII BACI** | Commerce bilatéral SH6 **réconcilié** à partir de Comtrade (valeurs FAB, flux miroir harmonisés) | Référence de comparaison et estimation des coûts CAF/FAB ; **pas** pour mesurer l'écart brut, puisqu'elle le réduit par construction | Licence `[À VÉRIFIER]` |
| **WITS** (Banque mondiale) | Interface vers Comtrade et données tarifaires | Accès alternatif, tarifs | Mêmes données sous-jacentes |
| **Statistiques nationales des partenaires** : Eurostat Comext, US Census, douanes chinoises (GACC), Office fédéral de la douane suisse, Inde, Émirats, etc. | Imports détaillés, parfois mensuels, parfois plus fins que SH6 | Améliorer la fraîcheur et la précision côté miroir | Formats et accès hétérogènes ; vérifier chaque source |
| **Instituts nationaux et douanes africaines** (dont pays utilisant SYDONIA/ASYCUDA) | Exports détaillés | Côté déclarant ; accès surtout via l'offre institutionnelle | Accès sous convention |

### 5.2 Production et volumes physiques

| Source | Contenu |
|---|---|
| **USGS** (Minerals Yearbook, Mineral Commodity Summaries) | Production minière par pays |
| **British Geological Survey** (World Mineral Statistics) | Production et commerce de minéraux |
| **Rapports ITIE / EITI** des pays membres | Production, exportations, paiements des entreprises et recettes de l'État, par ressource ; **source clé pour le moteur fiscal** |
| **JODI** (Oil et Gas) | Production, exportations pétrole et gaz, mensuel |
| **Energy Institute — Statistical Review of World Energy** | Production et commerce énergétiques annuels |
| **FAOSTAT Forestry** et **OIBT / ITTO** | Production et commerce de bois |
| **Processus de Kimberley** | Production et commerce de diamants bruts (volumes et valeurs) |
| Ministères des mines / du pétrole, banques centrales | Statistiques nationales |

### 5.3 Prix de référence

Banque mondiale (Pink Sheet), FMI (Primary Commodity Prices), cotations de place (LME, LBMA,
références pétrole) — **licences des cotations de place `[À VÉRIFIER]`** : certaines ne sont pas
redistribuables ; ARVI peut alors publier des valeurs dérivées sans republier la série brute.

### 5.4 Coûts de transport et d'assurance

**OCDE — base ITIC** (International Transport and Insurance Costs) `[À VÉRIFIER : couverture
et dernière année disponible]` ; à défaut, une convention forfaitaire CAF/FAB documentée (§7.2).

### 5.5 Coûts unitaires d'investissement (moteur M09)

IRENA (coûts de production d'électricité renouvelable), AIE, rapports de projets de la Banque
mondiale et de la BAD, données nationales de construction scolaire et sanitaire. Chaque coût
unitaire est stocké avec **source, année, région, devise, fourchette basse/centrale/haute**.
Aucun coût unitaire ne sera saisi sans source.

---

## 6. Taxonomie produits et chaînes de transformation

### 6.1 Familles et codes SH de départ

Codes indicatifs au niveau SH4/SH6, **à valider ligne par ligne contre la nomenclature SH en vigueur
et ses révisions `[À VÉRIFIER]`**. Une ressource couvre plusieurs codes (un par stade de transformation).

| Famille | Ressource | Stades et codes SH indicatifs |
|---|---|---|
| 🟤 Minerais | Cuivre | minerais et concentrés 2603 → mattes / cuivre de cément 7401 → cuivre non affiné 7402 → cathodes affinées 7403 |
| | Cobalt | minerais 2605 → oxydes et hydroxydes 2822 → mattes et produits intermédiaires 8105 |
| | Or | minerais de métaux précieux 2616 → or non monétaire 7108 |
| | Lithium | minerais (spodumène, classement `[À VÉRIFIER]`) → carbonate 283691 → oxyde/hydroxyde 282520 |
| | Bauxite / aluminium | bauxite 2606 → alumine 281820 → aluminium brut 7601 |
| | Fer | minerai 2601 → fonte et acier 72 |
| | Manganèse | minerai 2602 → ferro-alliages 7202 |
| | Nickel | minerai 2604 → mattes 7501 → nickel brut 7502 |
| | Uranium | minerais 261210 → composés 2844 `[À VÉRIFIER]` |
| | Diamants | 7102 (brut / taillé distingués au niveau SH6) |
| | Terres rares | classement dispersé (2805, 2846, minerais divers) `[À VÉRIFIER]` |
| | Étain, coltan (à ajouter) | 2609, 2615 |
| ⚫ Pétrole et gaz | Brut | 2709 |
| | Gaz naturel liquéfié / gazeux | 271111 / 271121 |
| | GPL | 271112, 271113 |
| | Produits raffinés | 2710 |
| 🌳 Forêt | Grumes → sciages → placages → contreplaqués → pâte → meubles | 4403 → 4407 → 4408 → 4412 → 47 → 9403 |
| 🌾 Agricole (phase 2) | Cacao → pâte/beurre/poudre → chocolat | 1801 → 1803–1805 → 1806 |
| | Café, coton, cajou, sésame, caoutchouc | 0901 ; 5201 ; 080131/080132 ; 120740 ; 4001 |

### 6.2 Chaîne de transformation (Processing Ladder)

Pour chaque ressource, M02 stocke une table de stades :

```
stage_order | stage_name | hs_codes | metal_content_or_grade | conversion_yield | price_reference
```

La **teneur** (ex. % de cuivre contenu dans un concentré) est indispensable : comparer des tonnes
de concentré à des tonnes de cathode sans la convertir en métal contenu n'a pas de sens.
Quand la teneur n'est pas publiée, elle est un paramètre `ESTIMATE` avec fourchette.

---

## 7. Méthodologie de calcul

Notation pour une cellule *(déclarant r, partenaire p, produit k, année t)* :
`X` = exports déclarés par r vers p (FAB, FACT) ; `M` = imports déclarés par p depuis r (souvent CAF, FACT) ;
`Qx`, `Qm` = quantités correspondantes (unité normalisée, ex. tonnes).

### 7.1 ARVI Trade Mirror (M03) — CALCULATION

| Indicateur | Formule |
|---|---|
| Écart de valeur brut | `G = M − X` |
| Écart relatif | `g = (M − X) / max(M, X)` (borné entre −1 et 1, comparable entre cellules) |
| Écart de quantité | `GQ = Qm − Qx` |
| Valeur unitaire export / import | `UVx = X / Qx` ; `UVm = M / Qm` |
| Écart de valeur unitaire | `GUV = UVm − UVx` |

Règle d'agrégation : les écarts sont calculés **au niveau de la cellule**, puis agrégés en trois totaux
séparés — **positifs bruts**, **négatifs bruts**, **net**. Le net seul masquerait des écarts opposés
qui se compensent. Les cellules où un côté est absent (non déclaré, confidentiel) ne sont **pas**
traitées comme un écart égal à la valeur de l'autre côté : elles sont marquées « miroir incomplet ».

### 7.2 Décomposition de l'écart (M04) — ESTIMATE

L'écart brut est décomposé en cascade, chaque étape avec son paramètre, sa source et sa fourchette :

```
Écart brut observé (G)
 − Ajustement CAF/FAB         M_fab = M / (1 + c)   c issu d'ITIC par produit et route ;
                               à défaut convention forfaitaire documentée [HYPOTHÈSE]
 − Décalage temporel          comparaison sur moyenne mobile 3 ans et, si mensuel disponible,
                               fenêtre de transit selon le mode de transport [HYPOTHÈSE]
 − Transit / réexport / hubs  réaffectation via flux du pays hub (imports du hub depuis r vs
                               réexports du hub) ; drapeau « hub » sur le partenaire
 − Classification SH          réconciliation entre codes d'une même chaîne (ex. 2603 ↔ 7402)
                               et entre révisions SH
 − Change                     conversion à un taux annuel moyen documenté ; écart si déclarations
                               en devises différentes
 − Confidentialité            part de flux en code confidentiel ou partenaire « non spécifié »
 = Écart résiduel non expliqué → « Potential Value Gap » (PVG), fourchette basse–haute
```

Le PVG est publié **avec sa fourchette et son niveau de confiance**, jamais comme un point unique.
Une explication possible non quantifiée (ex. qualité du produit) est listée comme « non quantifiée »
plutôt qu'ignorée.

### 7.3 Test de valeur unitaire (M06) — CALCULATION + ESTIMATE

Méthode des filtres de prix : comparer `UVx` (convertie en métal contenu si nécessaire) à une bande
autour du prix de référence de l'année. Écart de prix implicite :

```
PVG_prix = Qx × (P_ref_ajusté − UVx)     si UVx < borne basse de la bande
```

`P_ref_ajusté` tient compte de la teneur, des décotes de qualité et des frais de traitement usuels
(paramètres ESTIMATE). Ce test est **indépendant du miroir** : il reste utilisable quand le partenaire
ne déclare pas (cas fréquent du pétrole).

### 7.4 Value Capture (M07) — ESTIMATE

Pour une tonne de métal contenu exportée au stade *s* alors qu'un stade *s+1* existe :

```
Valeur ajoutée potentielle = Q_contenu × (P_{s+1} − P_s) × rendement de conversion
                              − coûts de transformation (énergie, réactifs, capital annualisé, logistique)
```

**Point critique du brief :** l'exemple « 500 M$ de minerai contre 3 Md$ de produits raffinés »
compare une valeur brute aval à une valeur amont. La valeur aval inclut de l'énergie, du capital,
d'autres matières et parfois du minerai d'autres pays. Ce qu'un pays peut capter est la **valeur ajoutée
nette**, pas la valeur brute aval. ARVI ne publie donc jamais la différence brute comme « valeur perdue ».

Chaque estimation de transformation est accompagnée d'une **note de faisabilité** (disponibilité et
coût de l'énergie, échelle minimale d'une unité, accès aux réactifs, marché) en trois niveaux,
renseignée par analyste, pas calculée automatiquement.

### 7.5 Fiscal (M08) — ESTIMATE

```
Recettes associées = assiette × taux effectif
```

- Redevances et droits à l'exportation : proportionnels à la valeur → applicables au PVG.
- Impôt sur les sociétés : dépend du bénéfice, pas de la valeur → appliqué seulement via une marge
  supposée, avec fourchette large.
- Paramètres par pays, ressource et année, sourcés (code minier, loi de finances, rapports ITIE).
- Résultat publié en fourchette ; jamais présenté comme « recettes perdues ».

### 7.6 Investment Translator (M09) — ESTIMATE

```
Équivalent = Montant (PVG, recettes fiscales ou valeur ajoutée) / coût unitaire sourcé
```

- Trois scénarios (bas / central / haut) selon la fourchette du montant et celle du coût unitaire.
- Le montant source est toujours indiqué (« équivalent de l'écart fiscal estimé », pas de « l'écart »
  en général).
- Emplois : multiplicateurs par secteur et pays, sourcés, en fourchette ; emplois indirects affichés
  séparément et signalés comme les plus incertains.
- Mention fixe sous chaque équivalent : *« Ordre de grandeur indicatif. Ne signifie pas que ce montant
  était disponible ni qu'il aurait été investi ainsi. »*

---

## 8. Modèle de confiance — ARVI Data Confidence

Score 0–100 par cellule, calculé par règles transparentes (pas d'apprentissage automatique en v1,
pour qu'un utilisateur puisse refaire le calcul). **Pondérations initiales `[HYPOTHÈSE]`**, à calibrer
sur le pilote et à publier.

| Composante | Poids initial | Mesure |
|---|---|---|
| Disponibilité du miroir | 15 | Les deux côtés déclarent, valeur et quantité |
| Cohérence des quantités | 15 | `|GQ| / max(Qx, Qm)` faible |
| Cohérence de valeur unitaire | 10 | `UVx` et `UVm` dans la bande de prix de référence |
| Qualité historique du déclarant | 10 | Régularité, délais, révisions fréquentes |
| Qualité historique du partenaire | 10 | Idem |
| Pas de hub / transit | 10 | Partenaire non marqué « hub », pays non enclavé ou route connue |
| Part expliquée de l'écart | 10 | Proportion de G expliquée par M04 de façon robuste |
| Stabilité temporelle | 10 | L'écart persiste sur plusieurs années (vs pic isolé) |
| Corroboration indépendante | 10 | Cohérence avec ITIE, production USGS/BGS, statistiques nationales |

Niveaux : 🟢 **High** ≥ 70 · 🟡 **Medium** 40–69 · 🔴 **Low** < 40.
Plafonds par ressource `[HYPOTHÈSE]` : or et pétrole brut plafonnés à Medium tant que la méthode
spécifique n'est pas validée. Chaque score s'affiche avec ses **trois principales raisons** en clair.

---

## 9. Scorecard pays : ARVI-1 à ARVI-6

Six indicateurs indépendants, **aucun score composite, aucun classement**.

| Indicateur | Définition | Nature | Unité |
|---|---|---|---|
| ARVI-1 Trade Gap | Écart miroir brut (positif / négatif / net) | CALCULATION | USD et % |
| ARVI-2 Unit Value Gap | Écart de valeur unitaire vs miroir et vs prix de référence | CALCULATION / ESTIMATE | USD par unité de contenu |
| ARVI-3 Processing Gap | Part des volumes exportés au stade le plus bas de la chaîne | CALCULATION | % des volumes |
| ARVI-4 Fiscal Capture Gap | Recettes associées au PVG | ESTIMATE | USD, fourchette |
| ARVI-5 Local Value Addition Gap | Valeur ajoutée nette potentielle (§7.4) | ESTIMATE | USD, fourchette |
| ARVI-6 Investment Equivalent | Traduction de ARVI-4 ou ARVI-5 en équivalents physiques | ESTIMATE | MW, km, écoles…, fourchette |

Remarque : le brief définissait ARVI-3 comme « valeur potentiellement perdue ». Elle est scindée ici
entre ARVI-3 (structure des exports, factuelle) et ARVI-5 (valeur ajoutée, estimée), pour séparer
ce qui est observé de ce qui est modélisé.

**Country Value Profile** et **Resource Cards** : vues construites sur ces indicateurs, chaque
chiffre avec badge de nature (FACT/CALCULATION/ESTIMATE), badge de confiance, et lien vers sa lignée.

---

## 10. Architecture de la base de données

PostgreSQL. Les tables reprennent le `ProvenanceMixin` de Cartouche (source, document, URL,
dates, statut de vérification, nature, confiance, statut de champ vide).

### 10.1 Référentiels

```
country(iso3 PK, name, region, landlocked, eiti_member, …)
partner(iso3 PK, name, is_hub, …)                      -- tous pays, pas seulement l'Afrique
resource(id PK, family, name)
hs_code(code, hs_revision, description, unit, PK(code, hs_revision))
hs_concordance(from_code, from_rev, to_code, to_rev, weight)
processing_stage(resource_id, stage_order, name, hs_code, grade_typical, conversion_yield)
source(id PK, name, publisher, authority_rank, licence, redistribution_allowed, url)
source_document(id PK, source_id, url, sha256 UNIQUE, fetched_at, published_at, dataset_version)
```

### 10.2 Faits

```
trade_flow(id PK, reporter, partner, hs_code, hs_revision, year, month NULL,
           flow ∈ {export, import, re_export, re_import},
           value_usd, valuation ∈ {FOB, CIF, other}, quantity, quantity_unit,
           field_status_value, field_status_quantity,
           + provenance)
UNIQUE(reporter, partner, hs_code, hs_revision, year, month, flow, source_document_id)

production(country, resource_id, year, quantity, unit, + provenance)
price_benchmark(resource_id, stage, year, month NULL, price, unit, currency, + provenance)
fiscal_parameter(country, resource_id, instrument, rate, base, valid_from, valid_to, + provenance)
unit_cost(category, item, region, year, currency, low, central, high, unit, + provenance)
```

### 10.3 Calculs et estimations (jamais mélangés aux faits)

```
methodology_version(id PK, label, published_at, document_url, params_json)
data_release(id PK, cut_off_date, methodology_version_id, frozen_at)

mirror_cell(id PK, data_release_id, reporter, partner, resource_id, hs_code, year,
            export_flow_id, import_flow_id,            -- liens vers les faits
            gap_value, gap_rel, gap_qty, uv_export, uv_import, gap_uv,
            mirror_status ∈ {complete, export_only, import_only, confidential})

gap_component(mirror_cell_id, component ∈ {cif_fob, timing, transit, classification,
              fx, confidentiality, unexplained}, low, central, high, parameter_refs_json)

confidence_score(mirror_cell_id, score, level, components_json, top_reasons_json)

value_capture_estimate(data_release_id, country, resource_id, year, stage_exported,
                       stage_target, low, central, high, feasibility_note, params_json)

fiscal_estimate(…, basis ∈ {pvg, value_capture}, low, central, high, params_json)
investment_equivalent(…, basis_ref, unit_cost_id, low, central, high)
```

Chaque ligne de calcul référence `data_release_id` : un rapport publié peut toujours être recalculé
à l'identique.

---

## 11. Architecture technique

| Couche | Choix proposé | Justification |
|---|---|---|
| API | FastAPI, SQLAlchemy 2, Alembic, PostgreSQL 16 | Déjà en place et testé dans Cartouche |
| Calcul | Python, `Decimal` pour les montants (comme `app/analytics`) ; Polars ou DuckDB pour les gros volumes de flux `[HYPOTHÈSE]` | Comtrade SH6 bilatéral = volumes bien supérieurs aux enchères Cartouche |
| Ingestion | Connecteurs par source (M01), stockage brut objet (S3-compatible), file de vérification | Repris de `app/ingest` |
| Planification | Tâche quotidienne de veille des publications (comme `docs/DAILY_WATCH.md`), recalcul à chaque nouvelle `data_release` | — |
| Frontend | Next.js, TypeScript, Tailwind, Recharts | Repris de Cartouche |
| Sécurité | Clés API hachées, rôles, limitation de débit, journal d'audit | Repris de `docs/SECURITY.md` ; ajout de rôles par offre |
| Publication | Site statique pour l'offre Public (comme `site/build.py`), API pour Pro/Institutionnel | — |

---

## 12. Modèle économique

| Offre | Contenu | Hypothèses à tester |
|---|---|---|
| **ARVI Public** (gratuit) | Country profiles, Resource Cards, ARVI-1 à ARVI-6 agrégés, note méthodologique complète, rapport trimestriel en version résumée | La crédibilité vient de la méthode publique ; l'offre gratuite est le canal d'acquisition |
| **ARVI Professional** (abonnement) | Détail par cellule, historique, exports CSV, API, décomposition complète, alertes | Cible : analystes, banques, chercheurs, médias spécialisés |
| **ARVI Institutional** (licence) | Tableaux de bord privés, intégration de données douanières nationales sous convention, analyses sur mesure, formation | Cible : ministères, douanes, banques centrales, DFI ; cycles de vente longs |
| **ARVI Reports** | Monitor trimestriel (version complète payante, comme le rapport Cartouche) | — |

**Contrainte déterminante :** les licences des sources (§5) fixent ce qui peut être revendu. Si une
source interdit la redistribution brute, l'offre Pro vend l'analyse dérivée et renvoie l'utilisateur à
la source pour la donnée brute. **Aucun prix n'est proposé ici** : pas de donnée de marché disponible
pour les étayer.

---

## 13. Gouvernance, risques juridiques et règles de langage

**Gouvernance**
- Comité méthodologique (statisticiens du commerce, fiscalistes des industries extractives,
  économistes miniers) qui valide chaque `methodology_version`.
- Droit de réponse : chaque pays ou institution peut signaler une erreur ; correction tracée et publiée.
- Publication systématique des limites et des critiques de la méthode miroir.

**Règles de langage** (appliquées automatiquement par une liste de termes interdits dans les gabarits)

| À éviter | À utiliser |
|---|---|
| fraude, vol, fuite, pillage, pertes | écart, écart non expliqué, écart potentiel |
| « l'Afrique a perdu X » | « un écart de X, dont Y non expliqué, confiance Moyenne » |
| « aurait pu construire N écoles » | « équivalent indicatif de N écoles » |
| classement des pays | profils par pays, indicateurs séparés |
| nom d'entreprise associé à un écart | aucun nom d'entreprise dans les analyses d'écart |

**Risques**
- Diffamation : nul tant qu'ARVI reste au niveau pays × produit × partenaire et utilise ce langage.
- Usage politique : un chiffre sorti de son contexte. Mitigation : badges, fourchettes et lien vers
  la lignée sur chaque export, y compris les images partagées.
- Données nationales confidentielles (offre Institutionnelle) : séparation stricte, jamais publiées.

---

## 14. Feuille de route et décisions ouvertes

### 14.1 Phases

| Phase | Contenu | Critère de sortie |
|---|---|---|
| **0 — Méthode et sources** | Vérifier chaque `[À VÉRIFIER]` ; obtenir les licences ; rédiger la note méthodologique v0.1 ; choisir le pilote | Registre des sources avec licences confirmées |
| **1 — Pilote** | 1 à 2 pays × 3 ressources ; M01–M05 ; profils internes | Écarts reproductibles, décomposition et confiance relues par un expert externe |
| **2 — Valeur** | M06–M08 sur le pilote ; Resource Cards | Paramètres fiscaux et de transformation sourcés pour les ressources pilotes |
| **3 — Traduction et publication** | M09–M11 ; ARVI Public ; premier Monitor | Note méthodologique v1.0 publiée |
| **4 — Extension** | Pétrole et gaz, forêt sur davantage de pays ; offres Pro et Institutionnelle | — |
| **5 — Agricole** | Cacao, café, coton, cajou, sésame, caoutchouc | — |

### 14.2 Pilote : options

| Option | Intérêt | Limite |
|---|---|---|
| Congo (Brazzaville) — pétrole, bois | Couvre deux familles ; pays membre de l'ITIE `[À VÉRIFIER : statut actuel]` | Pétrole : miroir bilatéral faible (§3) |
| RDC — cuivre, cobalt | Chaîne de transformation riche, enjeu minerais critiques | Pays enclavé côté exportations, transit important |
| Ghana — or, cacao | Or et cacao très documentés | Or : flux informels et hubs |

Recommandation provisoire : commencer par une ressource **à miroir fiable** (cuivre ou bois) pour valider
la méthode, avant le pétrole et l'or, où la méthode miroir est la plus fragile.

### 14.3 Décisions ouvertes (à trancher par le porteur du projet)

1. ARVI dans ce dépôt (module à côté de Cartouche) ou dépôt séparé ?
2. Pays et ressources du pilote.
3. Marque : ARVI sous l'ombrelle Cartouche ou marque autonome ?
4. Constitution du comité méthodologique.
5. Budget pour les données sous licence payante éventuelles.
