# Rapport de livraison — phase P1

**Date :** 18/11/2026 · **Version :** `0.1.0-p1` · **Moteur :** `screening-1.0.0`

## 1. Contexte et réserve principale

Le prototype et les documents `CAHIER_DES_CHARGES`, `SOURCES_DONNEES`, `METHODES_ET_CALCULS` et
`BACKLOG_ET_RECETTE` n'ont **pas été reçus**. Le propriétaire a déclaré le prototype perdu. P1 a donc
été **reconstruite de zéro** d'après `PROMPT_CLAUDE_CODE.md` (§IV P1, §V) et `CLAUDE.md`.
Conséquences :

- **Aucun calcul « validé » n'a pu être préservé ni comparé** à l'ancien moteur. Les calculs de P1
  sont validés par des cas de référence calculables à la main (§3), pas par équivalence avec le
  prototype.
- Les critères de recette détaillés de `BACKLOG_ET_RECETTE.md` sont inconnus. La recette s'appuie sur
  les critères d'acceptation immédiats du prompt maître (§V).

## 2. Tableau de conformité P1

Légende : ✅ opérationnel et testé · ◐ partiel · ❌ non implémenté.

| Fonctionnalité (prompt §IV P1 / §V) | État | Tests | Limites |
|---|---|---|---|
| Base PostgreSQL/PostGIS + migrations Alembic | ✅ | migrations montée/descente et `alembic check` sur PostGIS 3.4 et SQLite ; suite complète exécutée sur les deux | une seule migration (schéma initial) |
| Projets multiples, sites multiples par projet | ✅ | `test_api` | pas d'organisations ni de droits appliqués |
| Création de site par tracé sur la carte | ✅ | E2E (tracé à la souris) | polygone simple ; pas d'édition des sommets (remplacement de géométrie via API) |
| Import de sites (un site par polygone, champ de nom) | ✅ | `test_site_import…` | — |
| Import GeoJSON, Shapefile ZIP, GPKG, KML, KMZ, CSV de points | ✅ | `test_importers` (18 cas) | ≤ 50 000 entités ; ≤ 50 Mo ; GeoTIFF/COG non géré (P2) |
| Contrôle du SCR (fichier, déclaré, implicite RFC 7946/KML, conflit, absence de .prj, coordonnées projetées sans SCR) | ✅ | `test_importers` | l'ordre des axes n'est pas détecté au-delà du contrôle de plage et de l'alerte « hors d'Afrique » |
| Validation des géométries (vides, invalides, Z, réparation explicite) | ✅ | `test_importers`, `test_api` | réparation seulement sur demande, signalée |
| Sécurité des imports (taille, extensions, ZIP : traversée de chemin, liens, bombes, nombre d'entrées ; URL de source jamais téléchargée) | ✅ | `test_importers`, `test_api` | pas d'antivirus ; pas de quotas par utilisateur |
| Provenance des jeux (source, URL, licence, producteur, date, précision, nature, fictif, versions, SHA-256, SCR source) | ✅ | `test_traceability…`, `test_new_dataset_version…` | fichiers sources non archivés (pas de S3) |
| Règles dures (exclusions strictes) et souples (contraintes indicatives) séparées et paramétrables | ✅ | `test_engine`, `test_api` | scoring multicritère pondéré non implémenté |
| Buffers justifiés (aucune valeur réglementaire fournie par le logiciel) | ✅ | `test_line_layer_requires_justified_buffer`, E2E | la référence citée n'est pas vérifiée par le logiciel |
| Recul de limite de parcelle | ✅ | `test_setback…` | recul uniforme |
| Surface nette en UTM, chevauchements soustraits une fois | ✅ | `test_overlapping…`, `test_acceptance_scenario` | surface planimétrique UTM (contrôle géodésique fourni) |
| Intervalle de sensibilité | ✅ | `test_interval…` | seulement si toutes les précisions sont renseignées ; non statistique |
| Reproductibilité stricte, idempotence | ✅ | `test_strict_reproducibility`, `test_rerun…`, `test_storage` | — |
| Résultats et couches enregistrés (`AnalysisRun`, `Layer`) avec entrées, empreinte, versions, durée | ✅ | `test_api` | analyses synchrones (pas de file de tâches) |
| Exports GeoJSON et CSV | ✅ | `test_fictional…`, `test_csv_export…`, E2E | GeoPackage et PDF non faits |
| Étiquettes « renseigné / calculé / hypothétique / inconnu » (UI et exports) | ✅ | `test_api`, E2E, `format.test.ts` | « renseigné » n'apparaît pas encore dans les indicateurs P1, tous calculés ou hypothétiques |
| « Foncier vérifié » et « raccordement confirmé » interdits sans pièce adéquate, non fictive | ✅ | `test_land_and_grid_labels…` | le contenu de la pièce n'est pas vérifié |
| Journal d'audit des créations, modifications, imports et analyses | ✅ | `test_audit_log…` | acteur déclaratif (`X-Actor`), sans authentification |
| Interface React/TypeScript (portefeuille, projet, carte MapLibre, légende, échelle, onglets) | ✅ | `tsc`, Vitest (4), E2E Playwright (12 contrôles) | bilingue préparé (FR complet, EN des libellés) ; pages Finance/Technique/Rapports/Administration absentes |
| Projet de démonstration explicitement fictif | ✅ | `test_demo`, E2E | voir §5, point 4 |
| Commande unique Docker Compose | ✅ | pile construite et démarrée ; E2E passé contre elle | voir §4 pour la construction derrière un proxy TLS |
| Option locale Python pour les tests | ✅ | 61 tests en SQLite | — |
| Authentification, RBAC, organisations | ❌ | — | **ne pas exposer P1 hors d'un poste local** |

## 3. Résultats des tests (exécutés le 18/11/2026)

| Suite | Résultat |
|---|---|
| Backend sur SQLite (`PYTHONPATH=. pytest -q`) | **61 réussis** |
| Backend sur PostGIS 3.4 / PostgreSQL 16 (`GEORENEW_TEST_DATABASE_URL=…`) | **61 réussis** |
| Front : `tsc --noEmit` | sans erreur |
| Front : Vitest | **4 réussis** |
| Front : `vite build` | réussi (avertissement : bundle > 500 ko, MapLibre) |
| E2E Playwright contre `uvicorn` + SQLite | **12/12 contrôles**, 0 erreur JavaScript |
| E2E Playwright contre la pile Docker Compose (nginx + API + PostGIS) | **12/12 contrôles**, 0 erreur JavaScript |

Cas de référence du moteur (valeurs attendues calculées à la main) :

| Cas | Attendu | Obtenu |
|---|---|---|
| Carré de 1 000 m | 100 ha | 100 ha (écart relatif < 10⁻⁹) |
| Recul de 50 m | 81 ha nets, 19 ha de recul | identique |
| Deux exclusions de 4 ha qui se chevauchent sur 1 ha | 7 ha soustraits | 7 ha |
| Route traversante, buffer 25 m | 5 ha | 5 ha |
| Écart UTM/géodésique au méridien central | ≈ 0,08 % | 0,080 % |

Le passage sur PostGIS a révélé une anomalie invisible sous SQLite : GeoAlchemy2 renvoyait un
`WKBElement` au lieu d'une géométrie. Elle a été corrigée (`GeomType.column_expression`), et le test
`test_storage.py` la verrouille désormais.

## 4. Commandes

Voir `README.md`. En résumé :
- `docker compose up --build`, puis http://localhost:8080 (API sur http://localhost:8001/docs) ;
- local : `alembic upgrade head && python -m app.demo load && uvicorn app.main:app` dans `backend/`.

Dans l'environnement de développement utilisé, le trafic sortant passe par un proxy TLS. Les images
ont donc été construites avec `docker build --network host --secret id=extra_ca,…`, puis lancées par
`docker compose up --no-build`. Sur un poste sans proxy, `docker compose up --build` suffit ; je ne
l'ai pas vérifié hors de cet environnement.

## 5. Synthèse « opérationnel / simulé / à implémenter / blocages »

1. **Opérationnel :** tout ce qui est marqué ✅ au §2.
2. **Simulé :** rien n'est simulé dans le code. Les seules données fictives sont celles du projet de
   démonstration et des tests, marquées « DONNÉES FICTIVES » ou `is_synthetic`.
3. **À implémenter (P2 et suivantes) :** authentification et RBAC ; GeoTIFF/COG, MNT, pente,
   orientation, courbes de niveau ; occupation du sol ; connecteurs Global Solar Atlas, Global Wind
   Atlas, NASA POWER, ESA WorldCover et OSM, avec leur licence ; scoring multicritère ; raccordement
   et corridors ; PV (pvlib), éolien, BESS ; modèle financier ; rapports PDF/Word/Excel ; export
   GeoPackage ; stockage objet ; file de tâches ; mode terrain ; traduction anglaise des valeurs
   d'énumération.
4. **Points d'attention :**
   - Le projet de démonstration est placé à des coordonnées réelles (province du Nord-Ouest/Gauteng,
     Afrique du Sud). Le fond OSM affiche donc de vrais toponymes sous des données inventées. Le
     bandeau « DONNÉES FICTIVES » est permanent, mais un lecteur pressé d'une capture d'écran pourrait
     se méprendre. Il est possible de déplacer la démonstration vers un lieu neutre ou de masquer le
     fond par défaut sur ce projet.
   - Le fond OSM dépend d'un serveur externe et de sa politique d'usage : il est réservé à la démonstration.
5. **Blocages :** aucun pour P1. Pour P2, il faudra les documents `SOURCES_DONNEES` et
   `METHODES_ET_CALCULS`, ou leur réécriture, pour cadrer les sources, les licences et les formules.

## 6. Prochaine tranche proposée (début P2)

1. Authentification et rôles par projet, prérequis à tout déploiement partagé.
2. Ingestion raster (GeoTIFF/COG) avec contrôle du NoData, de la résolution et du SCR ; pente et
   orientation à partir d'un MNT importé ; contraintes de pente comme règles souples ou strictes.
3. Catalogue de sources avec fiche de licence par jeu ; premier connecteur avec repli « données
   absentes » (candidat : NASA POWER, dont les conditions d'utilisation sont à vérifier avant
   intégration).
4. Préfiltrage spatial dans PostGIS (`ST_DWithin`) pour les grandes couches ; file de tâches pour les
   analyses longues.
