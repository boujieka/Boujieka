# Cartographie des problèmes — Cameroun (étape 1)

Version 1, date de référence **19 octobre 2026**. Registre détaillé : `registre_problemes.csv` (34 problèmes).
Notes sectorielles sources : `notes/*.md`. Sources : `../sources/registre_sources.csv` (223 entrées).

> **Statut de ce document.** Cartographie de premier passage. Les niveaux de gravité et d'urgence (1–5)
> sont des **appréciations analytiques** de l'équipe, pas des mesures ; ils servent à orienter
> l'approfondissement et seront remplacés à l'étape 6 par une méthode de priorisation explicite.
> Environ un tiers des sources n'est connu que par résumé de moteur de recherche (`resume_moteur`) :
> tout chiffre qui en dépend est signalé comme tel dans le registre et n'est pas décisionnel en l'état.

## 1. Taxonomie

| Domaine | Problèmes avérés | Risques émergents | À investiguer |
|---|---|---|---|
| Macroéconomie, finances publiques, dette | P01 croissance/hab., P02 recettes, P03 dette (aussi risque), P04 arriérés, P05 investissement public, P06 entreprises publiques, P07 subventions carburant | P03 refinancement 2027 sans programme FMI, P08 lien souverain–banques | — |
| Économie réelle, emploi, infrastructures | P09 électricité, P10 sous-emploi/informalité, P11 eau-assainissement, P13 agriculture, P14 climat des affaires | — | P12 transports et logistique |
| Social | P15 pauvreté, P16 santé, P17 nutrition/insécurité alimentaire, P18 éducation, P19 protection sociale, P21 genre | — | — |
| Sécurité, humanitaire | P22 NO/SO, P23 Extrême-Nord, P24 Est/réfugiés, P25 humanitaire sous-financé | — | — |
| Institutions et gouvernance | P27 libertés (faits contestés), P28 décentralisation, P29 corruption, P30 efficacité administrative, P34 écart stratégie/exécution | P26 succession, calendrier électoral, continuité | — |
| Environnement, climat, territoires | P31 forêts, P32 vulnérabilité du Septentrion | — | P33 risques urbains |
| Transversal | P20 système statistique | — | — |

**Symptômes vs causes.** Les problèmes P01 (croissance), P10 (emploi), P15 (pauvreté), P17 (nutrition)
et P25 (besoins humanitaires) sont classés **symptômes** : ce sont des résultats. Les réformes doivent
porter sur leurs causes, qui figurent dans le registre (électricité, trésorerie de l'État,
investissement public, sécurité, productivité agricole, capital humain).

## 2. Les constats les mieux établis (confiance élevée, documents primaires lus)

1. **Le revenu par habitant stagne.** Le PIB réel par habitant n'a progressé que d'environ 15 % entre 2010
   et 2025, soit environ 1 % par an (calcul sur WDI). Depuis 2020, la croissance (≈2,9 % par an) couvre à
   peine la croissance démographique (≈2,8 %). Source : `outputs/wdi_derives.csv`.
2. **La pauvreté ne recule pas depuis 20 ans.** Le taux était de 40,2 % en 2001 et de 38,6 % en 2021
   (ancienne méthode). Il est de 37,7 % en 2022 (nouvelle méthode). L'écart territorial va de 1 à 8 :
   69,2 % dans l'Extrême-Nord contre 8,3 % à Douala (INS, ECAM5).
3. **L'emploi est massivement informel.** 86,6 % des emplois sont informels et le secteur privé formel
   ne représente que 5,1 % des emplois. Le sous-emploi atteint 56,4 % (INS, EESI3 2021).
4. **La dette pèse de plus en plus sur le budget.** Le risque de surendettement est jugé « élevé » (FMI,
   mars 2026). Le service de la dette passe de 4,8 % à 8,5 % du PIB entre 2025 et 2026 (MINFI, DPEB juin 2026).
   L'Eurobond de janvier 2026 a été émis à environ 10,1 % de rendement.
5. **L'État paie ses fournisseurs de plus en plus tard.** Le délai moyen de paiement est passé de 120 jours
   en 2023 à plus de 200 jours en 2025. 37 % des paiements de l'année sont effectués en décembre.
6. **L'investissement public est mal exécuté.** Les taux d'exécution sont de 73 % en 2025, et de 57 %
   seulement pour les projets financés de l'extérieur. Au premier trimestre 2026, 2,5 % de l'investissement
   prévu avait été exécuté.
7. **Les besoins humanitaires sont élevés et la réponse est sous-financée.** 2,9 millions de personnes
   sont dans le besoin. Le plan 2026 est financé à environ 32 % au 19/10/2026. 3,1 millions de personnes
   étaient en insécurité alimentaire de phase 3 ou plus fin 2025.

## 3. Couverture territoriale et par groupe

Légende : ● donnée régionale disponible (année), ◐ partielle ou non représentative, ○ nationale seulement, ✕ absente.

| Problème | Ada. | Cen. | Est | EN | Lit. | Nord | NO | Ouest | Sud | SO | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P15 Pauvreté (2022) | ● | ● | ● | ● | ● | ● | ◐ | ● | ● | ◐ | NO/SO non représentatifs |
| P16 Mortalité <5 ans (2018) | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | Ancienne (EDS 2018) |
| P17 Retard de croissance (2018) | ● | ◐ | ● | ● | ◐ | ● | ◐ | ◐ | ◐ | ◐ | 6 strates lues |
| P17 Insécurité alimentaire aiguë (2025-26) | ✕ | ✕ | ✕ | ✕ | ✕ | ✕ | ✕ | ✕ | ✕ | ✕ | Total national seulement ; rapport CH par département non obtenu |
| P18 Écoles non fonctionnelles | ✕ | — | ✕ | ✕ | — | ✕ | ● | — | — | ● | ≈45 % NO/SO (OCHA 2026) |
| P09 Accès à l'électricité | ✕ | ✕ | ✕ | ✕ | ✕ | ✕ | ✕ | ✕ | ✕ | ✕ | Urbain/rural seulement |
| P22-P24 Déplacements | ● | — | ● | ● | ● | ● | ● | ● | — | ● | OCHA/HCR, chiffres divergents |
| P05 Exécution du BIP (2024) | ● | ◐ | ◐ | ● | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ | Taux régionaux partiels (presse) |
| P28 Transferts aux CTD | ✕ | ✕ | ✕ | ✕ | ✕ | ✕ | ✕ | ✕ | ✕ | ✕ | National seulement |

**Concentration territoriale.** Les régions septentrionales (Extrême-Nord, Nord, Adamaoua), l'Est et le
Nord-Ouest cumulent les indicateurs les plus défavorables : pauvreté, mortalité, malnutrition,
insécurité, climat. Selon la Banque mondiale, 80 % des pauvres vivent dans les régions septentrionales
et le Nord-Ouest (MAC-007). **Le Littoral, le Centre, l'Ouest et le Sud** sont surtout concernés par
l'emploi urbain, l'électricité industrielle et les risques urbains, mais restent peu documentés dans ce
premier passage.

**Groupes de population.** Les données désagrégées existent pour le milieu (urbain/rural), le sexe du chef
de ménage, le quintile de bien-être et l'âge (emploi). Elles sont **absentes ou non lues** pour le handicap
(seul le taux de 6,7 % est connu), le statut de déplacé (pauvreté) et les ménages de réfugiés.

## 4. Relations entre problèmes (premier passage, étape 3 à approfondir)

Niveau de preuve : **[É]** causalité étayée par une source qui la documente explicitement ;
**[M]** mécanisme plausible décrit par une source sans mesure d'effet ; **[C]** simple corrélation ou
co-occurrence ; **[H]** hypothèse de l'équipe, à tester.

```
                 P26 incertitude institutionnelle ──[H]──► tous (horizon des réformes, attentisme)
                                    │
P02 recettes ─┐                     ▼
P07 subventions ─┼─► P03 dette / P04 arriérés ──[M]──► P05 investissement public ──[M]──► P01 croissance
P06 entreprises ─┘        │  (trésorerie de l'État)         │
publiques                 ├──[É]──► P09 électricité (dettes croisées État–distributeur–producteurs)
                          ├──[M]──► P14 secteur privé (délais >200 j) ──[M]──► P10 emploi formel
                          ├──[M]──► P08 banques
                          └──[H]──► P16 CSU (remboursements), P18 (dette due aux enseignants)

P09 électricité ──[É]──► P01, P14 (contrainte n°1 citée par BM/IFC/FMI) ──► P10
P22/P23 conflits ──[É]──► P25 humanitaire, P18 écoles fermées, P17 insécurité alimentaire ──[C]──► P15
P32 climat ──[É]──► P23 (≈45 % des nouveaux déplacements, OIM/OCHA), P17, P13
P20 statistiques ──[M]──► P19 ciblage, mesure de P15/P16/P10 et de toute réforme
P29/P30 redevabilité ──[M]──► P05, P34 (exécution des plans)
P28 décentralisation ──[H]──► P11 eau, P18, services locaux
```

**Blocages transversaux candidats** (dont la résolution faciliterait plusieurs réformes) :

1. **Trésorerie de l'État et arriérés (P03, P04, P07, P06).** Ce blocage touche directement l'électricité,
   les entreprises, les banques, l'investissement public et plusieurs services sociaux.
   Preuve : [É] pour l'électricité, [M] pour le reste.
2. **Électricité (P09).** C'est la contrainte de production citée par toutes les sources économiques lues.
3. **Sécurité dans le NO/SO et l'Extrême-Nord (P22, P23).** Elle conditionne les résultats sociaux dans
   les régions les plus pauvres.
4. **Système statistique (P20).** Sans mesure fiable, aucune cible de réforme n'est vérifiable.
   Le dernier recensement exploité date de 2005 ; les résultats du RGPH4 (collecté en 2026) sont attendus début 2027.
5. **Capacité d'exécution et redevabilité (P05, P34, P29).** Les plans annoncés (SND30, PLANUT, PPRD,
   PSRDREN, PIISAH) n'ont pas de bilan audité.

## 5. Contradictions majeures relevées (non résolues)

| Sujet | Valeurs | Cause probable |
|---|---|---|
| Croissance 2025 | 3,1 % (FMI), 3,4 % (BM), 3,5 % (INS), 3,4 ou 3,6 % (MINFI, incohérence interne au DPEB) | Estimations ou comptes provisoires |
| Stock d'arriérés | 485 / 752 / 926 Mds FCFA | Définitions : RAP, dette flottante, arriérés |
| Dette/PIB 2025 | 40,3 % (FMI), 43,7 % (BM), 43,5 % (MINFI) | Périmètres et PIB retenus |
| DGD 2024 | 292,7 Mds inscrits (MINFI) vs 127,5 Mds (Chambre des comptes) | Périmètre et inscription vs exécution |
| PDI NO/SO | 334 000 (HNRP, données 2024) vs 493 402 (HCR, 2026) | Dates et méthodes d'évaluation |
| NEET 15-24 ans (2021) | 3,6 % (INS) vs 23,2 % (OIT, mêmes microdonnées) | Définition |
| Accès rural à l'électricité | 23,3 % (INS 2021) ; BM : 26 % (2023) → 42,7 % (2024) | Rupture de série BM probable |
| Morts post-électoraux | 16 / ≥48 / 55 | Sources (gouvernement, ONU via Reuters, opposition) |
| Enfants hors école | 3,8 % (UIS) vs ≈20 % implicite (ECAM5) | Dénominateurs projetés sans recensement |
