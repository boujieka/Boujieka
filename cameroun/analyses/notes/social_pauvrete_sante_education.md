# Diagnostic SOC : pauvreté, santé, nutrition, éducation, protection sociale, eau, genre, démographie

Date de consultation : 2026-10-19. Domaine : SOC. Sources détaillées : `sources/registre_social_pauvrete_sante_education.csv`. Données : `data/raw/indicateurs_social_pauvrete_sante_education.csv`. Documents téléchargés : `sources/documents/SOC/`.

Niveaux d'accès. La plupart des chiffres ci-dessous viennent de documents primaires lus (`lu_document`) : ECAM5 (INS), EDS 2018 (rapport final), Cadre Harmonisé (CILSS), briefing IPM 2026 (PNUD/OPHI), CPD UNFPA 2026 et ISR de la Banque mondiale. La série WDI vient de l'API de la Banque mondiale (`lu_page_web`, base mise à jour le 2026-10-08). Les chiffres marqués « (moteur) » ne reposent que sur un résumé de moteur de recherche. Leur fiabilité est faible et ils doivent être re-vérifiés.

**Contexte statistique critique.** Il n'y a pas eu de recensement depuis 2005 (3e RGPH). Le 4e RGPH (décret de 2015) n'a toujours pas réalisé son dénombrement. En mai 2026, le BUCREP lançait encore un appel d'offres pour des logiciels de traitement financés par le budget du 4e RGPH (SOC-025, moteur). Tous les dénominateurs (population, taux de scolarisation, couvertures) reposent donc sur des projections. La dernière EDS date de 2018. La collecte de la MICS7 s'achevait mi-2026 (SOC-014) ; une dizaine de grappes du Nord-Ouest n'étaient pas entamées pour raisons de sécurité, et aucun résultat n'est publié à la date de consultation (non trouvé). Aucune nouvelle enquête de pauvreté n'a été publiée après l'ECAM5 : une image sur le site de l'INS (août 2026) mentionne la formation des formateurs de l'ECAM6, mais l'information n'a pas été vérifiée au-delà de l'intitulé du fichier.

---

## P1. Pauvreté monétaire élevée, stagnante sur 20 ans et très concentrée dans le Septentrion et le Nord-Ouest

**Le problème.** Près de 4 Camerounais sur 10 vivent sous le seuil national. Le nombre absolu de pauvres augmente, et l'écart régional va d'un facteur 1 à 8.

**Indicateurs**
- **Nouvelle série (ECAM5, méthode EHCVM, base de référence)**
  - Taux de pauvreté 2022 : 37,7 % (urbain 21,6 % ; rural 56,3 %) [SOC-002]. Profondeur : 13,0 %. Sévérité : 6,0 %.
  - Seuil : 813 FCFA par personne et par jour, soit 296 691 FCFA par an [SOC-003 p.7].
  - Nombre de pauvres : environ 10,1 millions sur environ 26,7 millions d'habitants [SOC-004].
- **Taux par strate d'enquête en 2022** [SOC-003 p.8, Figure 4] : Extrême-Nord 69,2 ; Nord-Ouest 66,8 ; Nord 61,1 ; Adamaoua 45,1 ; Est 41,5 ; Ouest 30,4 ; Littoral hors Douala 23,8 ; Sud-Ouest 20,4 ; Centre hors Yaoundé 19,1 ; Sud 14,9 ; Yaoundé 10,8 ; Douala 8,3.
- **Tendance (ancienne méthode, enquête témoin 2021)**
  - National : 40,2 % (2001), 37,5 % (2014), 38,6 % (2021) [SOC-001, SOC-002].
  - Urbain : 8,9 % (2014) puis 16,5 % (2021), soit une forte hausse. Rural : 56,8 % puis 58,3 %.
  - La cible SND30 est de 30,8 % en 2030 [SOC-001].
- **Seuils internationaux** : 26,7 % à 3,00 $/jour en PPA 2021 (2021) [SOC-006] ; 23 % à 2,15 $ en PPA 2017 (2021/22) [SOC-007]. Selon la Banque mondiale, ce dernier taux n'a baissé que de moins d'un point entre 2001 et 2021, et les 30 % les plus pauvres ont vu leur consommation diminuer [SOC-007].

**Populations touchées**
- Le monde rural est le plus touché.
- Il en va de même des ménages dont le chef travaille dans le secteur primaire (59,0 % de pauvres ; ils représentent 64,9 % des pauvres) [SOC-002].
- Les ménages dirigés par un homme sont plus pauvres (39,0 %) que ceux dirigés par une femme (33,5 %). Selon l'INS, l'écart s'explique en partie par la taille plus réduite des ménages dirigés par une femme [SOC-003 p.8].
- Les chiffres du Nord-Ouest et du Sud-Ouest ne sont **pas représentatifs**, car la couverture a été partielle [SOC-003]. Le taux de 20,4 % au Sud-Ouest est donc très probablement sous-estimé : c'est une hypothèse d'analyste, non vérifiée.

**Causes avancées par l'INS** [SOC-001, SOC-003]
- Une croissance insuffisante : 2,6 % par an en moyenne sur 2020-2023, pour une démographie de 2,5 %.
- Des distorsions de redistribution.
- Des chocs : Boko Haram dans l'Extrême-Nord, crise dans le Nord-Ouest et le Sud-Ouest, réfugiés centrafricains à l'Est, COVID-19, guerre en Ukraine, inflation de 6,3 % entre 2021 et 2022.
- L'exode des jeunes et le changement climatique dans l'Extrême-Nord.

**Politiques et résultats.** La SND30 fixe la cible. Aucun résultat d'évaluation propre aux politiques n'a été trouvé.

**Contradictions et méthodes**
- **Deux séries non comparables coexistent** : 37,7 % (2022, nouvelle méthode) et 38,6 % (2021, ancienne méthode). L'INS explique que l'ancien seuil (1 053 FCFA par jour et par équivalent adulte) surestimait la consommation, car la collecte se faisait en un seul passage d'octobre à décembre [SOC-003 p.7].
- Les classements régionaux du communiqué de presse (Adamaoua et Est au-dessus de la moyenne) sont cohérents avec la Figure 4.

**Confiance : élevée** pour le niveau national et le milieu, car le document primaire a été lu. **Moyenne** pour les régions (Nord-Ouest et Sud-Ouest non représentatifs). **Faible** pour toute tendance après 2022, faute de données.

## P2. Inégalités de consommation élevées

**Indicateurs**
- Gini 2022 (nouvelle méthode) : 40,1 (urbain 37,2 ; rural 37,3). Rapport Q5/Q1 : 7,8 [SOC-002].
- Ancienne méthode : Gini 0,44 (2014) puis 0,43 (2021) ; Q5/Q1 10,1 puis 9,7 [SOC-003 p.6].
- Banque mondiale : Gini 42,2 pour 2021/22 et 46,6 pour 2014 [SOC-006, SOC-007].

**Contradictions**
- Trois valeurs différentes circulent pour la même période (40,1 ; 43 ; 42,2), selon l'agrégat et la méthode.
- Le communiqué de l'INS parle d'une consommation « dix fois » supérieure chez les plus riches, ce qui correspond à l'ancienne méthode. La nouvelle donne 7,8.

**Confiance : moyenne**, en raison de la divergence des méthodes.

## P3. Pauvreté multidimensionnelle supérieure à la pauvreté monétaire

**Indicateurs**
- IPM global : 43,6 % de pauvres multidimensionnels, soit 12,7 millions de personnes projetées pour 2024. Intensité : 53,2 %. IPM : 0,232. Vulnérables : 17,6 %. Pauvreté sévère : 24,6 %. Les données datent de **2018** (EDS) [SOC-008, Table A].
- Contribution des dimensions : niveau de vie 47,1 %, éducation 27,6 %, santé 25,2 %.
- Banque mondiale (définition propre) : 41 % en 2021/22 [SOC-007].

**Données manquantes** : aucune désagrégation régionale de l'IPM n'a été lue, et aucune donnée postérieure à 2018 n'existe pour l'IPM PNUD.

**Confiance : moyenne**, car les données sont anciennes.

---

## P4. Mortalité maternelle et infanto-juvénile en baisse mais encore élevée, avec un gradient Nord/Est contre grandes villes

**Indicateurs**
- **Mortalité des moins de 5 ans (EDS 2018)** : 80 ‰, contre 151 ‰ en 1998 (urbain 65 ; rural 92) [SOC-005 p.157].
  - Sur 10 ans, par région : Nord 133, Est 122, Extrême-Nord 102, Adamaoua 96, Sud 90, Centre hors Yaoundé 85, Ouest 78, Nord-Ouest 57, Yaoundé 53, Douala 50, Littoral hors Douala 40 [SOC-005, Tab. 8.3 p.163].
  - Écart selon le bien-être : 111 ‰ dans le quintile le plus pauvre, 49 ‰ dans le plus riche.
- **Estimations modélisées (UN IGME)** : 78,9 ‰ en 2018 puis 64,8 ‰ en 2024. Mortalité néonatale : 24,8 ‰ en 2024 [SOC-006]. Selon l'EDS, la mortalité néonatale stagne : 29 ‰ en 2004, 28 ‰ en 2018 [SOC-013].
- **Mortalité maternelle**
  - EDS : 406 pour 100 000 naissances vivantes sur 2011-2018 (IC 309-504) [SOC-005, Tab. 16.5 p.384].
  - Estimation modélisée MMEIG : 258 en 2023, contre 342 en 2021 [SOC-006]. Le CPD de l'UNFPA date ce même chiffre de « 2025 » [SOC-012 §5], ce qui est une incohérence de date.
- **Accouchements assistés** : 69 % en 2018 [SOC-006], 40 % au Nord et 96 % dans le Littoral [SOC-012].

**Causes documentées** [SOC-005, SOC-012, SOC-013] : faible accès aux soins obstétricaux de qualité, pénurie de personnel qualifié en zone rurale, fécondité précoce, intervalles intergénésiques courts (135 ‰ si l'intervalle est inférieur à 2 ans) et faible instruction de la mère.

**Contradictions et méthodes.** L'EDS donne des estimations directes avec de larges intervalles, tandis que l'IGME et le MMEIG sont des modèles. La baisse 2018-2024 n'est **pas observée** par enquête : la MICS7 n'est pas encore publiée.

**Confiance : élevée** pour 2018, **moyenne** pour les niveaux 2023-2024 (modélisés).

## P5. Couverture vaccinale insuffisante et flambées épidémiques (rougeole, choléra 2026)

**Indicateurs**
- Tous les vaccins de base à 12-23 mois : 52 % en 2018 (Nord 36 % ; Douala 74 %). 10 % des enfants n'avaient reçu aucun vaccin [SOC-005 p.195-199].
- WUENIC 2024 : DTC3 77 % (68 % en 2018) ; rougeole 1re dose 71 % (61 % en 2018) [SOC-006].
- **Choléra 2026** : épidémie confirmée le 29/06/2026. Au 12/09/2026, 2 683 cas cumulés et 77 décès (létalité 2,87 %) dans l'Extrême-Nord, le Nord et l'Ouest, avec 11 districts en foyer confirmé et le camp de Minawao touché [SOC-017, qui reprend la SitRep #5 publiée sur ReliefWeb, source primaire non lue].
- **Rougeole et choléra 2025** (moteur, OMS AFRO) : 3 153 cas suspects de rougeole, dont 2 428 confirmés, et 27 districts en épidémie ; 96 cas suspects de choléra [SOC-020]. À vérifier.

**Confiance** : moyenne pour la vaccination (estimations WUENIC), moyenne à faible pour le choléra 2026 (source secondaire).

## P6. Paludisme : charge stable et très élevée

**Indicateurs**
- Prévalence par TDR chez les 6-59 mois : 24 % en 2018 (30 % en 2011) ; 32 % en rural contre 14 % en urbain ; 31 % dans le quintile le plus pauvre contre 8 % dans le plus riche [SOC-005 p.267].
- Incidence : 260 pour 1 000 personnes à risque en 2024, sans baisse depuis 2017 (259) [SOC-006].

**Confiance : élevée** pour 2018, **moyenne** pour l'incidence modélisée.

## P7. Financement de la santé : charge écrasante pour les ménages et CSU embryonnaire

**Indicateurs**
- Paiements directs des ménages : 67,7 % de la dépense courante de santé en 2023, contre 72,3 % en 2018 [SOC-006, base GHED].
- Dépense publique intérieure : 14,7 % de la dépense courante de santé.
- Dépense courante de santé : 4,55 % du PIB, soit 79 USD par habitant en 2023 [SOC-006].
- La santé représente 5,5 % de la consommation des ménages en 2022 [SOC-002].

**État de la CSU**
- Phase 1 lancée le 12/04/2023 (moteur). À ce moment, seuls 6,46 % de la population étaient couverts par un mécanisme de protection sociale en santé, selon un chiffre « officiel » cité par la presse (moteur, non vérifié).
- En mai 2025, le ministre annonçait **3,9 millions d'enrôlés (91 % de l'objectif 2025)**, 281 000 accouchements, 110 000 séances de dialyse et plus de 6 millions de visites d'agents de santé communautaires [SOC-018, annonce non auditée].
- En avril 2026, le gouvernement a lui-même qualifié le bilan de « mitigé » [SOC-019]. Selon la presse, les mécanismes d'enrôlement, de cotisation et de remboursement restent « partiellement opérationnels » et le ministre reconnaît des retards d'enrôlement et de remboursement. Aucun chiffre 2026 n'a été trouvé.

**Confiance** : élevée pour les paiements directs (série GHED cohérente) ; faible pour la CSU (annonces, pas de rapport de mise en œuvre lu).

---

## P8. Malnutrition chronique et insécurité alimentaire aiguë concentrées au Septentrion et dans les zones de conflit

**Indicateurs**
- **Retard de croissance des moins de 5 ans** : 29 % en 2018 (31 % en 1991, 36 % en 2004) ; rural 36 % contre urbain 20 % [SOC-005 p.225].
  - Par région : Nord 41, Extrême-Nord 37, Est 37, Adamaoua 35, Yaoundé 11, Douala 9 [SOC-005 p.226].
  - Selon le bien-être : 40 % dans le quintile le plus pauvre, 9 % dans le plus riche.
- Émaciation : 4,3 % en 2018 [SOC-006].
- **Cadre Harmonisé**
  - Situation courante d'octobre à décembre 2025 : **3 120 294 personnes en phase 3 ou plus**, dont 249 306 en phase 4 [SOC-009 p.3].
  - Situation projetée de juin à août 2026 : **2 857 241 personnes (9,7 % de la population analysée)**, dont 249 559 en phase 4 ; 9 des 58 zones sont en phase 3 et aucune en phase 4 [SOC-010 p.3, Tableaux 1-2].
  - Pour le Cameroun, la projection a été **reconduite** du cycle d'octobre-novembre 2025 et non réactualisée [SOC-010 p.4].
- La FAO GIEWS donne un ordre de grandeur cohérent : environ 2,8 millions de personnes et environ 250 000 en phase 4. Elle cite le conflit (Extrême-Nord, Nord-Ouest, Sud-Ouest) et la fin précoce des pluies en septembre 2025 [SOC-026, moteur].
- Sous-alimentation (FAO) : 4,9 % en 2024 [SOC-006]. Ce faible niveau national contraste avec les poches de crise.

**Données manquantes** : aucune répartition régionale ou départementale du Cadre Harmonisé camerounais n'a été lue, car le rapport national MINADER n'a pas été obtenu. Il n'existe pas non plus de donnée anthropométrique postérieure à 2018 en attendant la MICS7.

**Confiance** : élevée pour le Cadre Harmonisé national et le retard de croissance 2018 ; faible pour la situation nutritionnelle actuelle.

---

## P9. Éducation : accès inégal, faible achèvement du secondaire, apprentissages faibles et système perturbé par les conflits et les conflits sociaux enseignants

**Indicateurs**
- **ECAM5 (2021-2022)** [SOC-002]
  - Taux net de scolarisation au primaire : 80,4 % (urbain 89,1 ; rural 72,3 ; filles 79,6 ; garçons 81,2).
  - Taux net au secondaire : 51,8 % (rural 32,4 ; urbain 65,3).
  - Alphabétisation des 15-24 ans : 83,3 % (rural 70,8).
- **UIS (administratif)** [SOC-006]
  - Achèvement du primaire : 75,3 % en 2024 (65,0 % en 2018).
  - Achèvement du premier cycle du secondaire : 35,0 % en 2023 (48,3 % en 2016), donc en recul.
  - Enfants non scolarisés en âge du primaire : 3,8 % en 2024.
  - Enseignants formés : 72,3 % en 2023 (82,7 % en 2022 : rupture de série ou erreur, non expliquée).
  - Dépense publique d'éducation : 2,84 % du PIB en 2023.
- **Apprentissages** : pauvreté des apprentissages de 71,9 % en 2019 (Banque mondiale, sur la base du PASEC 2019) [SOC-006]. Les scores nationaux du PASEC 2019 n'ont **pas été lus** ; le chiffre de 53,7 % de « réussite en lecture » ne vient que d'un mémoire cité par le moteur [SOC-030, faible].
- **Nord-Ouest et Sud-Ouest** (moteur) : 41 % des écoles fermées et 223 749 enfants hors de l'école en juin 2025, d'après une SitRep UNICEF citée par la presse [SOC-021]. D'autres chiffres plus anciens circulent : plus de 855 000 enfants, plus de 488 000, ou 90 % des écoles primaires publiques non fonctionnelles en 2020. **Aucun chiffre 2026 trouvé.** Pour l'Extrême-Nord, aucun décompte récent d'écoles fermées n'a été trouvé.
- **Grèves des enseignants (mouvement OTS / COREC)** (moteur) [SOC-022]
  - Opérations « craie morte » en 2022-2023.
  - Trêve à la rentrée 2024.
  - Appel à l'« école morte » à partir du 22/04/2025.
  - Revendications : statut de l'enseignant, apurement de la dette due aux enseignants, Forum national de l'éducation, rétablissement des salaires suspendus.
  - Aucune information sur 2025-2026 n'a été trouvée. Le nombre d'enseignants contractuels n'a pas été trouvé.

**Contradictions.** La part d'enfants hors école mesurée par l'UIS (3,8 %) est incompatible avec le taux net de l'ECAM (80,4 %, soit environ 20 % d'enfants de 6 à 11 ans non scolarisés dans le primaire) et avec les fermetures massives dans le Nord-Ouest et le Sud-Ouest. Les dénominateurs démographiques de l'UIS sont des projections sans recensement depuis 2005, et les données administratives couvrent mal les zones de conflit. Les taux d'achèvement de l'UIS sont donc à **utiliser avec prudence**.

**Confiance** : élevée pour l'ECAM 2022, moyenne pour l'UIS, faible pour le Nord-Ouest, le Sud-Ouest et les grèves.

---

## P10. Protection sociale : couverture très faible ; filets sociaux en montée lente

**Indicateurs**
- **Projet Filets sociaux adaptatifs et inclusion économique (P175363)**
  - Financement IDA de 160 M USD, approuvé le 09/03/2022, clôture prévue le 30/03/2028 [SOC-016].
  - En décembre 2024, **44 500 ménages** avaient reçu des transferts et 47 500 étaient en cours d'enregistrement, pour une cible de 150 500 ménages en 2028. 15 000 jeunes étaient en cours de sélection pour l'inclusion économique, sur une cible de 65 000 [SOC-015 §4.1].
  - Décaissement : 35,70 M USD, soit 23,9 % du montant révisé de 148,43 M USD [SOC-015 §7.2].
  - Notes : progrès vers l'objectif « satisfaisant », mise en œuvre « modérément satisfaisante ».
  - Paiements numériques lancés fin mai 2024. Le registre social national (géré par le MINAS) figure parmi les indicateurs, mais son état chiffré ne ressort pas du texte extrait.
- Selon le MINEPAT, l'enveloppe totale serait de 146,752 Mds FCFA pour 356 000 bénéficiaires, dont 138 500 financés par l'État (annonce, moteur) [SOC-028]. Un financement additionnel de 38,6 M USD (P510425, août 2025) a été signalé par le moteur et n'a pas été vérifié.
- **CNPS** : 1 658 989 travailleurs actifs immatriculés au 31/12/2025, et 16 % de nouvelles immatriculations salariées en moins (94 556 en 2025 contre 112 263) [SOC-023]. La presse en déduit un taux de couverture d'environ 15 % de la population active, un calcul indicatif.

**Données manquantes** : nombre de ménages inscrits au Registre social unifié (non trouvé), dépense publique de protection sociale, ISR 2025-2026 du projet (non trouvé).

**Confiance : moyenne.**

---

## P11. Eau, assainissement, énergie et logement : progrès lents, fracture rurale massive

**Indicateurs**
- **Eau** : source améliorée en saison sèche pour 81,9 % de la population en 2022 (76,7 % en 2014 ; rural 69,6) [SOC-001, SOC-002]. Selon le JMP, au moins un service de base pour 71,4 % en 2024 [SOC-006].
- **Assainissement** : toilettes améliorées non partagées pour 47,7 % en 2022 (40,4 % en 2014 ; rural 28,2) [SOC-001]. JMP, assainissement de base : 47,1 % en 2024. Défécation à l'air libre : 4,4 % [SOC-006].
- **Énergie** : électricité pour 60,2 % de la population en 2022 (urbain 87,6 ; rural 28,4). Combustibles propres pour la cuisson : 23,4 %. Évacuation adéquate des ordures : 39,4 % [SOC-001].
- **Logement** : 47,0 % des ménages vivent dans un logement en matériaux définitifs (17,4 % des pauvres contre 57,6 % des non-pauvres) et 56,8 % sont propriétaires [SOC-002]. Bidonvilles : 32,7 % de la population urbaine en 2022 (49 % en 2010) [SOC-006].

**Contradictions.** Les définitions ECAM et JMP diffèrent (eau : 81,9 contre 71,4). Pour l'électricité, l'ECAM donne 60,2 % en 2022 et la Banque mondiale 71 % en 2022, avec des sources et des unités différentes (population ou ménages).

**Confiance : moyenne à élevée.**

## P12. Inégalités de genre et santé reproductive

**Indicateurs**
- Indice d'inégalité de genre (IIG) : 0,558 en 2023, rang 148 [SOC-012 §9].
- Part des femmes : 33,9 % des sièges parlementaires [SOC-006], 20 % des postes ministériels [SOC-012].
- **Violences (EDS 2018, cité par l'UNFPA)** : 32 % des femmes de 15-49 ans ont subi des violences conjugales, 39 % des violences physiques depuis l'âge de 15 ans et 13 % des violences sexuelles.
- Prévalence contraceptive moderne : 15,4 % ; besoins non satisfaits : 23 % [SOC-012], année non précisée.
- **Fécondité des adolescentes** : 105 ‰ en 2024 selon la Banque mondiale [SOC-006], 98 ‰ selon l'UNFPA. Par région selon l'UNFPA : Est 173, Nord 125, Extrême-Nord 95 [SOC-012 §8].
- 20 % des adolescentes de 15-19 ans sont en union (EDS 2018, d'après SOC-013).
- Jeunes ni en emploi, ni en études, ni en formation (NEET) : environ 30 % des jeunes femmes contre 15 à 18 % des jeunes hommes [SOC-012].

**Confiance : moyenne**, car il s'agit surtout de données secondaires de l'UNFPA ou de 2018.

## P13. Démographie, urbanisation et crises humanitaires

**Indicateurs**
- **Population** : 29,9 millions en 2025 (estimation de la Banque mondiale) [SOC-006] ; environ 29 millions selon l'UNFPA [SOC-012] et environ 29 millions en 2023 selon le BUCREP (moteur) [SOC-024].
- **Fécondité** : indice synthétique de 4,26 en 2024 (modèle) [SOC-006], 4,8 selon l'UNFPA, 5,1 sur 7 ans selon l'EDS 2018.
- **Urbanisation** : 55,7 % de population urbaine en 2025, croissance urbaine de 3,0 % par an [SOC-006].
- Personnes en situation de handicap : 6,7 % (ECAM 2022, cité par l'UNFPA) [SOC-012].
- **Humanitaire (HNRP 2026)** [SOC-011, SOC-012]
  - 2,9 millions de personnes dans le besoin, 1,9 million ciblées et environ 1 million priorisées.
  - Besoins de 319 M USD, avec une enveloppe priorisée de 171 M USD.
  - Environ 845 000 déplacés internes, 790 000 retournés et 404 000 réfugiés.
  - Financement de 19,4 % selon la Sida (mars 2026) ; 20 % au 31/03/2026 selon OCHA (moteur).
  - En 2025, l'UNICEF comptait 3,3 millions de personnes dans le besoin (moteur) [SOC-027].

**Confiance** : faible pour les effectifs de population (aucun recensement depuis 21 ans) ; moyenne pour le HNRP (document primaire OCHA non lu, accès 403).

---

## Lacunes de données
1. **Recensement** : le 4e RGPH n'est pas réalisé. Tous les taux reposent sur des dénominateurs projetés depuis 2005.
2. **Pauvreté** : aucune mesure après 2022, faute d'ECAM6. Pas de taux fiables pour le Nord-Ouest et le Sud-Ouest. Pas de désagrégation par handicap, statut de déplacé ou âge lue dans le rapport complet.
3. **Santé et nutrition** : aucune enquête après 2018 tant que la MICS7 n'est pas publiée. Les données DHIS2 ou les annuaires MINSANTE n'ont pas été obtenus. Les chiffres du choléra 2026 et de la rougeole 2025-2026 ne sont pas vérifiés à la source primaire.
4. **CSU** : aucun rapport officiel de mise en œuvre (enrôlés par région, financement, arriérés de remboursement).
5. **Éducation** : annuaires statistiques MINEDUB/MINESEC récents non obtenus. Pas de chiffre 2025-2026 sur les écoles fermées (Nord-Ouest, Sud-Ouest, Extrême-Nord). Effectifs d'enseignants contractuels non trouvés. Scores nationaux PASEC 2019 non lus. Aucune information sur les grèves OTS après avril 2025.
6. **Protection sociale** : effectif du Registre social unifié, ISR 2025-2026 du projet P175363 et rapport annuel CNPS non obtenus.
7. **Cadre Harmonisé** : pas de répartition régionale ou départementale camerounaise ; la projection juin-août 2026 n'a pas été actualisée.
8. **HNRP 2026** : le document OCHA original n'a pas été lu (ReliefWeb renvoie 403).

## Documents à obtenir
- Rapport principal ECAM5 (INS), avec tableaux régionaux et de vulnérabilité, ainsi que les microdonnées.
- Rapport des résultats clés de la MICS7 (INS/UNICEF), annoncé pour le T4 2026 (à confirmer).
- Calendrier officiel et budget du 4e RGPH (BUCREP / MINEPAT).
- Rapport national du Cadre Harmonisé du Cameroun (MINADER), cycles de novembre 2025 et mars 2026, par département.
- Cameroon HNRP 2026 (OCHA), en PDF, et le dernier Humanitarian Update.
- SitReps choléra 2026 (MINSANTE/OMS/UNICEF), y compris la SitRep #5 du 14/09/2026.
- Rapport de bilan des 3 ans de la CSU (MINSANTE, avril 2026) et texte de loi CSU s'il existe.
- Annuaires statistiques du MINEDUB, du MINESEC et du MINSANTE (2023-2025).
- PASEC2019, rapport international (CONFEMEN, 2020), section Cameroun.
- ISR 2025-2026 et Restructuring Paper (janvier 2025) du projet P175363 ; document du financement additionnel P510425.
- Rapport annuel 2025 de la CNPS.
- Cameroon Poverty Assessment 2025 (Banque mondiale), en texte intégral.
- Situation reports UNICEF Cameroun 2026 (éducation dans le Nord-Ouest et le Sud-Ouest).
