# PROMPT MAÎTRE — Construire GeoRenew Africa dans Claude Code

> À copier dans Claude Code ouvert sur le dossier `GeoRenew_Africa_Claude_Code`.

Tu es une équipe senior composée d'un architecte SIG, d'un ingénieur électricien / énergie renouvelable, d'un analyste projet-finance, d'un spécialiste environnement/foncier et d'un développeur full-stack. Développe **GeoRenew Africa**, une application web destinée à générer des analyses spatiales de présélection et des **études de préfaisabilité vérifiables** pour les projets **solaires PV utility-scale, éoliens et BESS**, avec extensibilité vers mini-réseaux, C&I, hybride et électrification rurale.

## I. Lire d'abord et cadrer

Lis intégralement `CLAUDE.md`, `README.md`, `docs/CAHIER_DES_CHARGES.md`, `docs/METHODES_ET_CALCULS.md`, `docs/SOURCES_DONNEES.md`, `docs/BACKLOG_ET_RECETTE.md`, ainsi que le MVP existant. Utilise ces documents comme cahier des charges. L'annonce « GIS Specialist – Renewable Energy Projects » à Johannesburg est la source métier initiale, non une preuve d'existence de datasets africains ni de compétences de calcul financier.

**Périmètre MVP prioritaire :** application multi-projets, multi-pays (Afrique), robuste et locale d'abord, avec un projet de démonstration explicitement fictif; aucune dépendance à des API payantes nécessaire pour les tests.

## II. Construire les capacités métiers

1. **Portefeuille et scénarios** : comptes, organisations, projets, sites, pays, technologie, versions, scénarios et rôles. Historique et journal d'audit.
2. **Carte centrale** : visualiser fond de carte, limites AOI, données raster/vectorielles, réseau, zones d'exclusion, parcelles, sous-stations, voies d'accès, buffers, courbes de niveau, pente, orientation et surfaces. Dessiner et éditer polygones/corridors; afficher légendes et échelle; exporter GeoJSON, GeoPackage, PDF.
3. **Ingestion géospatiale** : importer GeoJSON, Shapefile ZIP, GPKG, KML/KMZ, CSV coordonnées et GeoTIFF/COG, puis valider CRS, géométries, noms, types, dates, sources, précision, champs, licences et empreintes. Reprojeter correctement.
4. **Sources et connecteurs** : mettre des adaptateurs explicites pour Global Solar Atlas, Global Wind Atlas, NASA POWER, ESA WorldCover, MNT utilisable sous licence, OpenStreetMap, et import manuel de cadastre / lignes/postes officiels / données d'études terrain. Toute connexion externe doit avoir un comportement de repli « données absentes ». Ne pas présumer API ou licences non documentées.
5. **Screening spatial** : appliquer contraintes dures (exclusion) et souples (scoring) selon une grille paramétrable ; calculer surfaces brute, potentiellement aménageable et nette, avec unions de buffers, intervalles d'incertitude et diagnostics géométriques. Garder une carte précise de ce qui a été soustrait et pourquoi.
6. **Raccordement** : mesurer les distances géométriques aux réseaux documentés, produire plusieurs scénarios de corridors et des estimations de coûts sous hypothèses explicites. Aucun calcul automatique ne doit conclure qu'une ligne a une capacité électrique disponible ; nécessité d'études réseau et accord du gestionnaire.
7. **Évaluation solaire** : calcul simplifié de MWp DC selon emprise nette paramétrée, puis, avec météo représentative et équipements renseignés, simulation de productible via pvlib ; distinguer estimation annuelle issue de PVOUT de simulation horaire. Implantation préliminaire de tables et chemins selon géométrie, modules et dégagements.
8. **Évaluation éolienne** : données de vent à hauteur connue, rugosité, topographie, zones interdites, options de turbines, distances et estimation préliminaire avec courbe constructeur; présenter les limites de la résolution des atlas et l'absence de mesures de terrain.
9. **BESS/hybrides** : puissance MW, capacité MWh, durée, SoC, DoD, rendement, vieillissement; simulations temporelles simples selon profils de charge et production explicitement fournis; ne pas optimiser sans profils fiables.
10. **Pré-faisabilité financière** : CAPEX par lot, OPEX, productible, revenus (PPA / autoconsommation), taxes et devises, dette/fonds propres, durée, dégradation, actualisation; calculer LCOE, VAN, TRI projet, TRI equity, DSCR annuel/minimum si données suffisantes; sensibilité P50/P90 uniquement si distribution de ressources justifiée. N'afficher aucun nombre financier sans jeux d'hypothèses.
11. **Rapports** : produire PDF, Word, Excel auditables, cartes SIG et annexes des couches, des hypothèses, des calculs et des limites; un rapport « non bancable » par défaut avec sections « données critiques manquantes » et « travaux terrain à réaliser ».
12. **Terrain** : mode collecte d'observations GPS avec horodatage, photographie et qualité de précision; import de traces ou relevés; préparation à mode hors-ligne (phase ultérieure).

## III. Architecture souhaitée

- Monorepo `frontend/` React + TypeScript + Vite + MapLibre GL JS ; `backend/` FastAPI Python + Pydantic ; `db/` PostgreSQL/PostGIS ; tâches lourdes via Celery/RQ ; traitement spatial GeoPandas/Shapely/pyproj/GDAL/rasterio ; stockage objet S3 compatible ; migrations Alembic ; pytest et Playwright ; Docker Compose dev.
- API structurée `/api/v1/projects`, `/sites`, `/datasets`, `/constraints`, `/analyses`, `/scenarios`, `/financial-models`, `/reports` ; OpenAPI auto-généré.
- Modèle relationnel incluant : `Organization`, `User`, `Project`, `Site`, `Dataset`, `DatasetVersion`, `ConstraintRule`, `AnalysisRun`, `Layer`, `EnergyScenario`, `GridScenario`, `FinancialScenario`, `Report`, `AuditLog`.
- Tâches et analyses idempotentes, erreurs traitées, métriques visibles.
- Chaque `AnalysisRun` conserve versions des inputs, hash et paramètres, sortie géographique, tables agrégées, horodatage, avertissements, version logicielle.
- Sécurité : RBAC, secrets en environnement, contrôle uploads, anti-SSRF, séparation projets, règles de stockage/suppression de données sensibles.
- UI moderne, professionnelle, bilingue FR/EN, pages Dashboard, Portfolio, Étude d'un site, Couches et données, Analyse multicritère, Technique, Finance, Rapports et Administration.

## IV. Ordre d'exécution obligatoire

**Phase P0** : inspecte le code existant ; crée une matrice existant/manquant ; exécute les tests ; relève les incohérences ; garde la fonctionnalité de calcul de surface reproductible.

**Phase P1 (à réaliser en priorité)** : transforme la démo en MVP multi-projets : base PostGIS, migrations, schémas site/projet, import de fichiers et contrôle CRS, gestion des règles dures/souples, cartes et résultats persistés, exports GeoJSON/CSV, tests. Utiliser une UI React/TypeScript. Fournir une commande unique Docker Compose et une option local Python pour les tests.

**Phase P2** : catalogue data et adaptateurs par pays avec provenance, métadonnées, licences ; rasters MNT, pente, occupation du sol, ressources solaires ; calculs et visualisations contrôlés.

**Phase P3** : scénarios PV, raccordement et BESS; tests de validation sur cas de référence ; rapports PDF/Word/Excel.

**Phase P4** : éolien, modèle financier complet, scoring de portefeuille, fonctions avancées de droits et collaboration.

À chaque phase, montre un tableau de conformité (fonctionnalité, implémenté, testé, limites), la commande de lancement et les résultats des tests. Ne prétends jamais avoir ajouté des données réelles si elles ne sont pas effectivement importées.

## V. Critères d'acceptation immédiats

- L'utilisateur peut créer un projet et plusieurs sites, importer un GeoJSON, afficher les couches, définir des exclusions et reculs, puis générer une surface nette calculée dans une projection métrique appropriée.
- Les résultats varient quand on modifie les contraintes et restent strictement reproductibles quand on relance la même entrée.
- Les exclusions qui se chevauchent ne sont soustraites qu'une seule fois.
- Les jeux de données et les hypothèses sont traçables avec dates, unités et sources.
- Un site sans couche cadastrale ne porte pas l'étiquette « foncier vérifié » ; un site sans étude réseau ne porte pas « raccordable confirmé ».
- L'interface et le rapport différencient « renseigné », « calculé », « hypothétique » et « inconnu ».
- Suite de tests verts ; aucune clé secrète en git ; erreurs de données compréhensibles.

## VI. Instructions opérationnelles

Travaille directement dans le dépôt : crée/édite le code, exécute installation, tests et builds dans les limites de l'environnement. **Commence par la phase P1** au lieu de seulement proposer une architecture sur papier. Si un service externe ou un paquet n'est pas disponible, crée un adaptateur explicite et des tests locaux, explique la limitation et poursuis ce qui est faisable. Aucune donnée inventée. Priorité : exactitude géospatiale, traçabilité et expérience utilisateur. À la fin, fournis une liste claire des fonctions qui marchent réellement, des commandes et de la prochaine tranche.
