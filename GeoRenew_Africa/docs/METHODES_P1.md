# Méthode de calcul — screening P1 (moteur `screening-1.0.0`)

Implémentation : `backend/app/geo/engine.py`. Tests de référence : `backend/tests/test_engine.py`.

> Les formules et seuils du document `METHODES_ET_CALCULS.md` du kit d'origine **n'ont pas été
> reçus**. La méthode ci-dessous a été écrite pour P1 à partir des règles de `CLAUDE.md`. Elle devra
> être confrontée à ce document s'il est retrouvé.

## 1. Système de coordonnées de calcul

- Stockage et affichage : EPSG:4326. **Aucune mesure n'est faite dans ce SCR.**
- Calcul : zone UTM WGS 84 contenant le centroïde du site,
  `zone = floor((lon + 180) / 6) + 1`, EPSG `326zz` au nord de l'équateur, `327zz` au sud.
- Contrôle croisé : la surface brute UTM est comparée à la surface géodésique sur l'ellipsoïde
  WGS 84 (`pyproj.Geod.geometry_area_perimeter`). L'écart attendu est d'environ −0,08 % sur le
  méridien central (facteur d'échelle 0,9996, soit 0,9996² ≈ 0,9992 pour les aires). Il augmente
  vers le bord de la zone. Au-delà de 0,5 %, le contrôle échoue et un avertissement est émis.
  Un site qui déborde de plus de 3,5° du méridien central est aussi signalé.

**Limite.** La surface rapportée est la surface **planimétrique UTM**, pas la surface géodésique. Les
deux valeurs figurent dans le résultat.

## 2. Étapes

Notations : `S` = limite du site ; `r` = recul ; `Eᵢ` = entités de la règle stricte i,
de buffer `bᵢ` ; `Cⱼ` = entités de la contrainte indicative j, de buffer `cⱼ`.

| Grandeur | Définition |
|---|---|
| Surface brute | `aire(S)` |
| Zone aménageable `A` | `S ⊖ r` (buffer négatif de `r` m) ; `S` si `r = 0` |
| Bande de recul | `aire(S − A)` |
| Zone de la règle i `Zᵢ` | `(∪ buffer(Eᵢ, bᵢ)) ∩ S` |
| Exclusions strictes | `aire(A ∩ ∪ᵢ Zᵢ)` — **union** : un chevauchement n'est soustrait qu'une fois |
| Surface nette `N` | `A − ∪ᵢ Zᵢ` |
| Somme par règle | `Σᵢ aire(Zᵢ ∩ A)` (chevauchements compris, pour information) |
| Chevauchement non double-compté | somme par règle − exclusions strictes |
| Contraintes indicatives | `aire(N ∩ ∪ⱼ (∪ buffer(Cⱼ, cⱼ)))` — **jamais soustraites** |

Conventions :
- Tous les buffers utilisent `quad_segs = 16` (cercle ≈ 64 côtés, sous-estimation de l'aire d'un
  disque d'environ 0,16 %). Ils sont reproductibles à l'identique.
- Un point ou une ligne sans buffer n'a aucune emprise ; c'est signalé par un avertissement.
- Une entité est retenue si sa distance au site est ≤ son buffer.
- Contrôle de conservation : `brute − recul − exclusions − nette = 0` (tolérance 10⁻³ m² + 10⁻⁹ × brute).

## 3. Intervalle de sensibilité de la surface nette

Il n'est calculé **que si la précision de position est renseignée** pour la limite du site et pour
chaque couche d'exclusion stricte. Sinon, sa nature est « inconnu » et les couches manquantes sont
listées.

- Borne basse : site rétréci de `p_site`, buffers `bᵢ + pᵢ`.
- Borne haute : site élargi de `p_site`, buffers `bᵢ − pᵢ`. Un buffer négatif rétrécit un polygone ;
  une ligne ou un point perd alors toute emprise.

C'est une **sensibilité géométrique déterministe**, pas un intervalle statistique.

## 4. Puissance indicative

`MWp DC = surface nette (ha) × densité`. La densité est **fournie et justifiée par l'utilisateur**
(nature « hypothétique »). Sans densité, la valeur est « inconnu ». Le calcul ne tient compte ni
d'une implantation, ni de la pente, ni de l'ombrage, ni des allées, et ne donne aucune puissance en MW AC.

## 5. Reproductibilité et idempotence

- Les géométries sont stockées en WKB ou EWKB exact. Un aller-retour en base est identique bit à bit
  (test `test_storage.py`).
- L'empreinte des entrées est le SHA-256 du JSON canonique (clés triées) qui contient :
  - la version du moteur ;
  - l'empreinte WKB de la limite, sa source, sa précision et les statuts du site ;
  - les paramètres (recul, densité et leurs justifications) ;
  - pour chaque règle : type, buffer, justification, jeu de données, version, SHA-256 du fichier,
    licence, date et précision.
- Une demande dont l'empreinte est identique renvoie l'analyse existante. Avec `force=true`, l'analyse
  est recalculée : l'empreinte et les résultats sont identiques (test d'API).

## 6. Ce qui n'est PAS calculé en P1

Pente et orientation (pas de MNT), occupation du sol, ressource solaire ou éolienne, productible,
raccordement et corridors, BESS, finance, scoring multicritère (le champ `weight` existe mais n'est
pas utilisé).
