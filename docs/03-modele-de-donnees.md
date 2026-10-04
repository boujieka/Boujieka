# 03 — Modèle de données

## 1. Pourquoi revoir le modèle

Le concept précédent annonçait six objets fondamentaux mais en listait cinq (Territory, People, Land,
Assets, Institutions), et attachait à chaque objet *un* propriétaire et *un* statut. Deux problèmes :

1. **Les catégories se chevauchent** : une école est un actif (bâtiment), une institution
   (établissement), et se trouve sur une parcelle (foncier). Une chefferie est à la fois une
   institution, un acteur et un territoire déclaré.
2. **La vérité est plurielle** : satellite, commune, chef et agent donnent des chiffres différents.
   Un modèle « un objet = une valeur » écrase ces divergences, alors que le rapprochement est
   précisément la valeur ajoutée du système.

## 2. Les six objets fondamentaux (version affinée)

```
                    ┌──────────────────────┐
                    │ 1. UNITÉ TERRITORIALE │  région → département → arrondissement
                    │   (référentiel versionné) │  → commune → village/quartier ; + territoires
                    └──────────┬───────────┘     traditionnels déclarés ; + mailles statistiques
                               │ contient (calcul spatial)
                    ┌──────────▼───────────┐
                    │ 2. OBJET SPATIAL      │  bâtiment, parcelle, établissement,
                    │   (ce qui existe)     │  infrastructure, site, ressource, exploitation
                    └──┬───────────────┬───┘
          lié par      │               │  décrit par
   ┌───────────────────▼──┐      ┌─────▼──────────────┐
   │ 4. DROIT / RELATION  │      │ 6. MESURE           │  capacité, effectifs, état,
   │ propriété, concession│      │ (série temporelle)  │  production, population agrégée
   │ permis, gestion,     │      └────────────────────┘
   │ exploitation, coutume│
   └──────────┬───────────┘
              │ détenu par
   ┌──────────▼───────────┐
   │ 3. ACTEUR            │  personne morale, administration, entreprise,
   │                      │  communauté, chefferie, (personne physique : S2)
   └──────────────────────┘

   5. ASSERTION : enveloppe TOUTES les informations ci-dessus
      = qui affirme quoi, sur quel objet, quand, par quelle méthode, avec quelle preuve,
        à quel niveau de vérification, et avec quel statut (validé, contesté…).
```

| # | Objet | Rôle | Norme de référence possible |
|---|---|---|---|
| 1 | **Unité territoriale** | Référentiel de rattachement, versionné (les découpages changent) | — |
| 2 | **Objet spatial** | Tout ce qui existe physiquement et se localise | — |
| 3 | **Acteur** | Tout ce qui peut détenir, gérer, exploiter, déclarer | ISO 19152 (LADM) « Party » |
| 4 | **Droit / relation** | Lien juridique ou fonctionnel acteur ↔ objet, avec dates | ISO 19152 (LADM) « RRR » (Rights, Restrictions, Responsibilities) |
| 5 | **Assertion** | Provenance et niveau de preuve de chaque information | W3C PROV (concepts) |
| 6 | **Mesure** | Valeurs quantitatives datées | — |

> **Recommandation** : aligner la partie foncière sur **LADM (ISO 19152)**, norme internationale du
> domaine foncier. Cela facilite l'interopérabilité avec un futur cadastre numérique et rassure les
> administrations domaniales. La compatibilité exacte avec les pratiques camerounaises reste à étudier.

## 3. Règles transverses

### 3.1 Identifiants
- Identifiant **interne stable** (UUID) pour chaque objet, jamais réutilisé.
- Identifiant **lisible** hiérarchique optionnel (ex. `CM-<région>-<dép>-<arr>-<type>-<n°>`), mais
  il ne doit pas servir de clé : si le découpage change, l'identifiant lisible devient faux.
- **Table de correspondance** avec les identifiants officiels sectoriels (code établissement scolaire,
  code formation sanitaire, n° de titre foncier, n° de permis minier, n° de registre de commerce).

### 3.2 Bitemporalité
Chaque information porte deux temps :
- **temps de validité** : période pendant laquelle c'est vrai sur le terrain (ex. concession 2019–2044) ;
- **temps d'enregistrement** : quand la plateforme l'a appris.
Cela permet de répondre à « que savait-on au 1ᵉʳ janvier ? » — indispensable pour l'audit et les litiges.

### 3.3 Statut de l'information (cycle de vie d'une assertion)

```
DÉTECTÉ (télédétection) ─┐
DÉCLARÉ (chef, commune) ─┼─► OBSERVÉ (agent terrain) ─► VALIDÉ (autorité compétente)
IMPORTÉ (base sectorielle)┘          │                         │
                                     ├─► CONTESTÉ ◄────────────┤
                                     └─► REJETÉ / OBSOLÈTE ◄───┘
```

Niveau de preuve requis selon le type d'information :

| Type d'information | Niveau maximal accessible sans autorité | Validation officielle requise pour |
|---|---|---|
| Existence d'un bâtiment, d'une route | OBSERVÉ | — |
| Usage d'un bâtiment, état d'une école | OBSERVÉ | — |
| Droit de propriété, titre foncier | DÉCLARÉ | **VALIDÉ** par l'administration domaniale |
| Concession, permis minier ou forestier | IMPORTÉ / DÉCLARÉ | **VALIDÉ** par le ministère compétent |
| Limite de territoire traditionnel | DÉCLARÉ | Reconnaissance par l'autorité administrative compétente (si elle existe) |
| Population | Estimation modélisée | Résultats officiels du recensement |

### 3.4 Sensibilité portée par la donnée
Chaque assertion porte une **classe de sensibilité** (S0–S3) qui détermine qui peut la voir.
Le contrôle d'accès est appliqué **au niveau de la ligne** (row-level security), pas seulement de l'écran.

### 3.5 Population : séparation stricte
Les microdonnées individuelles (ménages, personnes) vivent dans une **enclave statistique** distincte,
sous la responsabilité de l'institution de recensement. L'atlas ne reçoit que des **agrégats** par
unité territoriale ou maille, avec règles de suppression des petites cellules.
Les **détenteurs de droits fonciers** (personnes physiques) proviennent des registres fonciers, pas du
recensement : **aucune jointure personne-recensée ↔ propriétaire** dans la base commune.

## 4. Fiche territoriale (exemple de vue dérivée)

La fiche du concept initial devient une **vue calculée**, et chaque chiffre affiche sa source et son niveau de confiance :

```
VILLAGE : <nom>            Commune : <nom>      Référentiel v2026.1

POPULATION   ~1 840 hab. (intervalle 1 650–2 030)  [estimation modélisée, 2026]  ◐
             426 ménages                            [recensement 20XX]            ●
HABITAT      381 bâtiments détectés / 374 observés  [imagerie 2025 / terrain]     ●
FONCIER      1 245 ha (surface de l'unité)          [référentiel]                 ●
  usage      agricole 630 ha · forêt 420 ha · autre 195 ha  [classif. imagerie]   ◐
CHEFFERIE    1 chefferie (3ᵉ degré)  · 3 sites patrimoniaux (dont 1 protégé)       ●
ÉDUCATION    1 école primaire · 1 collège           [carte scolaire + terrain]     ●
SANTÉ        1 centre de santé (état : dégradé)     [terrain 03/2026]              ●
ÉCONOMIE     12 unités économiques observées        [terrain]                     ◐
RESSOURCES   1 carrière (titre : non trouvé ⚠)      [observé, non rapproché]      ○
INFRA        8,2 km routes (dont 3,1 km praticables toute l'année) · 1 pont · réseau MT

● validé/observé récent   ◐ estimé ou partiellement vérifié   ○ déclaratif   ⚠ anomalie
```

Le schéma SQL de référence est dans [`../schema/schema_postgis.sql`](../schema/schema_postgis.sql).
