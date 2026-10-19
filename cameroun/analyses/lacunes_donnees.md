# Lacunes de données et documents à obtenir (étape 1)

Date de référence : 19/10/2026. Lacunes classées par effet sur la décision : **A** = bloque une
recommandation chiffrée ; **B** = fragilise un diagnostic ; **C** = complément utile.

## 1. Lacunes structurelles du système statistique

| # | Lacune | Effet | Conséquence |
|---|---|---|---|
| L1 | Aucun recensement depuis 2005 (4e RGPH non réalisé) | A | Tous les taux (scolarisation, couverture, pauvreté en effectifs) reposent sur des projections |
| L2 | Pas de mesure de la pauvreté après 2022 (ECAM6 en préparation, non vérifié) ; NO/SO non représentatifs | A | Impossible de mesurer l'effet des chocs 2023-2026 |
| L3 | Dernière EDS en 2018 ; MICS7 collectée mais non publiée | B | Santé et nutrition décrites avec des données de 8 ans |
| L4 | Dernière enquête emploi en 2021 (EESI3) ; NEET INS/OIT incompatibles | B | Emploi des jeunes non suivi |
| L5 | Ruptures de séries non documentées (électricité rurale BM 2024, extractives INS 2021) | B | Tendances non interprétables |

## 2. Lacunes bloquant le chiffrage des réformes (priorité A)

| # | Donnée manquante | Détenteur probable | Statut d'accès |
|---|---|---|---|
| L6 | Analyse de viabilité de la dette FMI-BM 2026 complète (CR 26/081) et rapport de la 8e revue (CR 25/222) | FMI | Bloqué depuis cet environnement (403/404) ; à obtenir par un autre canal |
| L7 | Série homogène de la dette et détail par créancier ; échéancier 2027-2030 | CAA | Site inaccessible (TLS puis 503) |
| L8 | Stock unique des arriérés, RAP et dette flottante, avec ancienneté et créanciers | MINFI/DGTCFM, CAA, Chambre des comptes | Trois chiffres incompatibles |
| L9 | Électricité : pertes techniques et commerciales officielles, taux de recouvrement, SAIDI/SAIFI, énergie non distribuée, coût de service, inventaire des dettes croisées, paiements take-or-pay Nachtigal | ARSEL, SOCADEL, SONATREL, MINEE, MINFI | Aucun rapport ARSEL post-2020 obtenu |
| L10 | Coût budgétaire effectif des subventions carburant 2022-2026 et leur incidence par décile | CSPH, MINFI, INS | Presse uniquement |
| L11 | Évaluation exhaustive des dépenses fiscales (en % du PIB) | DGI, DGD | Non trouvée |
| L12 | Loi de finances 2026 promulguée, LFR 2026 éventuelle | MINFI / Journal officiel | Projet lu, texte promulgué non lu |
| L13 | Inventaire des projets d'investissement inachevés (coût restant, avancement) | MINEPAT, Comité de suivi | Rapports intégraux non obtenus |
| L14 | Comptes des entreprises publiques (notes SONARA, CAMAIR-CO, CAMWATER, SOCADEL) | DGB/CTSE | CAMAIR-CO en PDF scanné |
| L15 | Registre social unifié : effectif, couverture régionale | MINAS | Non trouvé |

## 3. Lacunes fragilisant le diagnostic (priorité B)

- **Sécurité** : séries de victimes 2024-2026 pour le NO/SO et l'Extrême-Nord (ACLED non consulté,
  ICG bloqué) ; statistiques d'enlèvements dans l'Est et l'Adamaoua.
- **Plans spéciaux** : décaissements audités du PPRD NO/SO, du PSRDREN, du PLANUT et du PIISAH.
  Seuls des montants « mobilisés » sont publiés.
- **Rapport officiel de mi-parcours de la SND30** (présenté en décembre 2025, non obtenu).
- **CSU** : nombre d'enrôlés par région, financement, arriérés de remboursement.
- **Éducation** : annuaires MINEDUB/MINESEC, écoles fermées en 2026, enseignants contractuels, PASEC national.
- **Insécurité alimentaire** : Cadre Harmonisé par département ; projection juin-août 2026 non actualisée.
- **Banques** : données COBAC propres au Cameroun (créances en souffrance, exposition souveraine).
- **Institutions** : Journal officiel (révision constitutionnelle, vice-présidence, décrets électoraux),
  décision du Conseil constitutionnel du 27/10/2025, rapports intégraux de la Chambre des comptes et de la CONAC, PEFA 2023.
- **Transports et eau** : rapports MINTP, PAD, PAK, Camrail, CAMWATER.

## 4. Lacunes complémentaires (priorité C)

GFW 2024-2025 et FAO FRA 2025 ; part du territoire en aires protégées ; inondations 2025 et lac Tchad ;
données urbaines (Douala : drainage, déchets) ; versions officielles des stratégies sectorielles
(SSS, SSEF, SDSR, PDSE) ; données de l'ART sur le numérique ; Afrobarometer.

## 5. Accès bloqués constatés pendant cette exécution

| Site | Problème | Contournement |
|---|---|---|
| imf.org, elibrary.imf.org (rapports pays) | HTTP 403 / 404 | Communiqués de presse seulement |
| caa.cm | Certificat TLS rejeté, puis 503 | Données CAA via DPEB et presse |
| reliefweb.int | 403 (WebFetch) ; API avec identifiant requis | HNRP 2026 récupéré par curl |
| crisisgroup.org | 403 | Presse citant l'ICG |
| Tableau de bord GFW | JavaScript, redirection | Résumés |
| Divers sites INS/SNH | Liens renvoyant du HTML | URL alternatives partiellement trouvées |

**Recommandation pratique.** Les documents L6 à L9 doivent être obtenus par demande directe ou par un
partenaire disposant d'un accès institutionnel. Les recherches web supplémentaires ne suffiront pas.
