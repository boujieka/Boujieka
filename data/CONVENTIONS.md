# Conventions de collecte des données TasetyGrid

Ces règles s'appliquent à toute donnée ajoutée sous `data/`. Elles traduisent le modèle
de [docs/03](../docs/03-modele-de-donnees.md) : chaque information est une **assertion
importée**, sourcée et datée, jamais une vérité.

## 1. Ce qui est accepté
- **Uniquement des sources publiques identifiables**, téléchargées réellement pendant la collecte
  (pas de chiffres recopiés de mémoire, pas de valeurs estimées « à la main »).
- **Licence connue et compatible** avec la redistribution dans un dépôt public
  (ex. CC BY 4.0, CC BY-IGO, ODbL, CC0, domaine public). Si la licence interdit la redistribution
  (ex. WDPA), **ne pas copier la donnée** : documenter seulement la source et le moyen d'y accéder.
- **Pas de données personnelles** : pas de noms de personnes (chefs, propriétaires, agents),
  pas de numéros de téléphone ni d'adresses de particuliers. Les noms d'établissements publics sont acceptés.
- Les **sites sacrés ou culturellement sensibles** ne sont pas collectés.

## 2. Format
- Vecteur : **GeoJSON** (EPSG:4326, coordonnées à 6 décimales max), un fichier par couche.
  Si un fichier dépasse 15 Mo : simplifier les géométries, découper par région, ou compresser en `.geojson.gz`.
- Tableaux : **CSV UTF-8**, séparateur virgule, en-tête en snake_case.
- Raster : **ne pas commiter de raster brut**. Publier des agrégats (CSV par unité administrative)
  et documenter le raster source.
- Taille totale par thème : viser < 50 Mo.

## 3. Champs minimaux par entité (couches vecteur)
| champ | contenu |
|---|---|
| `tg_type` | code de la nomenclature `nomenclatures/objets.yaml` (ex. `SOC.SANTE.HOPITAL`) ou `null` si non classable |
| `nom` | nom tel que dans la source (peut être vide) |
| `source_id` | identifiant de l'entité dans la source (ex. `node/123456` pour OSM) |
| `source` | code de la source dans `manifest.json` |
| `statut` | toujours `IMPORTE` (rien n'est validé à ce stade) |
| `date_source` | date de situation de la source (AAAA-MM-JJ si connue) |
| autres | attributs utiles de la source, renommés en snake_case |

## 4. Traçabilité obligatoire : `data/<theme>/manifest.json`
Pour chaque fichier produit :
```json
{
  "fichier": "sante/etablissements_sante_osm.geojson",
  "source_code": "OSM_GEOFABRIK_2026-10",
  "producteur": "Contributeurs OpenStreetMap, extrait Geofabrik",
  "url": "https://...",
  "licence": "ODbL 1.0",
  "attribution": "© les contributeurs d'OpenStreetMap",
  "date_telechargement": "2026-10-04",
  "date_situation": "2026-10-03",
  "sha256_source": "...",
  "sha256_fichier": "...",
  "nb_entites": 1234,
  "methode": "commande(s) ou script utilisés, filtres appliqués",
  "limites": "couverture inégale, doublons possibles, etc.",
  "controle": "contrôles faits et résultats (comptes, bornes géographiques, doublons)"
}
```
Les scripts de collecte sont commités dans `data/<theme>/scripts/` pour que la collecte soit **reproductible**.

## 5. Contrôles avant commit
- Toutes les géométries dans l'emprise du Cameroun (environ lon 8,4 à 16,2 ; lat 1,6 à 13,1).
- Comptes vérifiés et rapportés ; doublons signalés.
- Croisement avec une seconde source quand elle existe (ex. nombre d'unités administratives : 10 régions, 58 départements, 360 arrondissements).
- Tout écart ou doute est écrit dans `limites`, jamais masqué.
