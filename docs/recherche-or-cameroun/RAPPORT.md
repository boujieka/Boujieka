# Importations d'or en provenance du Cameroun (2000–2026) : Émirats arabes unis et reste du monde

*Recherche documentaire. Version 2 du 31 octobre 2026 : couverture étendue à **tous les pays déclarants** de UN Comtrade et aux codes **SH 7108, 7112 et 7113**.*
*Données brutes : [`donnees_miroir_or_tous_declarants.csv`](donnees_miroir_or_tous_declarants.csv) (283 enregistrements non nuls).*

## 1. Méthode

- **Principe des données miroir** : on compare les importations que les pays partenaires *déclarent* comme venant du Cameroun aux exportations que le Cameroun déclare lui-même.
- **Source** : base UN Comtrade, via l'aperçu public de son API (`/public/v1/preview`), interrogé le 31/10/2026 par le connecteur Comtrade de Firecrawl (Alexandria).
  - Flux : importations (M).
  - Partenaire : Cameroun (code M49 120).
  - Fréquence : annuelle, de 2000 à 2025.
  - URL type : `https://comtradeapi.un.org/public/v1/preview/C/A/HS?reporterCode=784&period=2023&partnerCode=120&flowCode=M&cmdCode=7108`
- **Déclarants** : les 254 pays et territoires de la table de référence « Reporters » de Comtrade (groupes régionaux exclus, Cameroun exclu). Ils ont été interrogés par lots de 44 à 57 codes.
  - Chaque combinaison *code SH × lot de déclarants × période* a reçu une réponse valide. Les requêtes interrompues par un délai d'attente ont été relancées.
  - Aucune réponse n'a atteint le plafond de 500 enregistrements.
- **Codes SH** :
  - **7108** : or brut, mi-ouvré ou en poudre. C'est l'indicateur principal.
  - **7112** : déchets et débris de métaux précieux (or, argent, platine…). Le poids déclaré est la **masse brute du déchet**, pas le contenu en or.
  - **7113** : bijouterie en métaux précieux, or ou autre.

## 2. Or brut (SH 7108) : résultats annuels, tous déclarants confondus

| Année | Total monde (kg) | Total (M USD) | EAU (kg) | Principaux autres déclarants (kg) |
|---|---:|---:|---:|---|
| 2000 | 0 | 0 | – | – |
| 2001 | 5 | 0,04 | – | Suisse 5 |
| 2002 | 69 | 0,7 | – | Belgique 65, Suisse 4 |
| 2003 | 291 | 3,4 | – | Belgique 291 |
| 2004 | 130 | 1,7 | 66 | Belgique 64 |
| 2005 | 101 | 1,5 | 101 | Espagne 0,1 |
| 2006 | 293 | 5,7 | 292 | Afrique du Sud 1 |
| 2007 | 304 | 6,5 | 275 | États-Unis 20, Corée du Sud 5, Allemagne 3 |
| 2008 | 338 | 8,7 | 301 | Corée du Sud 26, Italie 7, Israël 3 |
| 2009 | 1 418 | 41,6 | 1 364 | Corée du Sud 44, Arabie saoudite 5, Belgique 3 |
| 2010 | 2 406 | 88,1 | 2 367 | Corée du Sud 38, Allemagne 1 |
| 2011 | 3 535 | 176,1 | 3 533 | France 2 |
| 2012 | 4 982 | 252,6 | 4 978 | Suisse 4 |
| 2013 | 11 490 | 507,4 | 9 568 | **Allemagne 1 881**, Corée du Sud 41 |
| 2014 | 8 839 | 340,0 | 8 672 | Suisse 101, Corée du Sud 58, Allemagne 8 |
| 2015 | 10 435 | 367,6 | 10 418 | Corée du Sud 10, Allemagne 7 |
| 2016 | 10 240 | 350,4 | 9 939 | Suisse 196, Espagne 105 |
| 2017 | 10 913 | 382,2 | 10 907 | Espagne 4, Allemagne 2 |
| 2018 | 11 712 | 415,3 | 11 712 | < 1 |
| 2019 | 11 414 | 452,9 | 9 988 | **Rwanda 1 424** |
| 2020 | 5 828 | 280,7 | 3 227 | **Rwanda 2 076**, États-Unis 525 |
| 2021 | 5 602 | 312,2 | 4 809 | **Rwanda 791** |
| 2022 | 4 820 | 278,8 | 4 708 | Rwanda 112 |
| 2023 | **18 255** | **1 145,3** | 14 048 | **Rwanda 3 060, Ouganda 1 145** |
| 2024 | 9 942* | 661,3* | *non publié* | **Rwanda 6 746, Ouganda 3 197** |
| 2025 | 5 139* | 497,4* | *non publié* | **Ouganda 3 323, Rwanda 1 817** |
| 2026 | aucune donnée | | | |

\* *Pour 2024–2025, les EAU n'ont publié aucune donnée dans Comtrade au 31/10/2026 : ces totaux excluent donc le principal importateur. Selon la Sonamines, les EAU auraient enregistré environ 12,2 t en 2024 (voir § 5).*

**Cumuls SH 7108 (Comtrade, 2000–2025, tous déclarants)** : **≈ 138,5 t pour ≈ 6,58 milliards USD**.

| Déclarant | Poids cumulé | Valeur cumulée | Années couvertes |
|---|---:|---:|---|
| Émirats arabes unis | 111,3 t | 4,81 Md USD | 2004–2023 |
| Rwanda | 16,0 t | 0,95 Md USD | 2019–2025 |
| Ouganda | 7,7 t | 0,70 Md USD | 2023–2025 |
| Allemagne | 1,9 t | 82 M USD | surtout 2013 |
| États-Unis | 0,55 t | 21 M USD | |
| Suisse | 0,31 t | 10 M USD | |
| Corée du Sud | 0,22 t | 6 M USD | |
| Belgique | 0,42 t | 5 M USD | |

### Exportations d'or déclarées par le Cameroun (SH 7108, Comtrade, monde)

| Année | Poids déclaré | Valeur déclarée |
|---|---:|---:|
| 2012 | 184 kg | |
| 2013 | 214 kg | |
| 2014 | 78 kg | |
| 2015 | 10 kg | |
| 2016 | 9 kg | |
| 2017 | 5 kg | |
| 2018 | 13 kg | |
| 2019 | 82 kg | |
| 2020 | 5 kg | |
| 2021 | 40 kg | |
| 2022 | 3,5 kg | |
| 2023 | non renseigné | 0,67 M USD |

Les années 2000–2011 n'ont pas été interrogées côté Cameroun.

## 3. Déchets de métaux précieux (SH 7112)

Total cumulé 2000–2025 : **≈ 32 M USD**. Deux profils très différents apparaissent :

- **EAU, 2007–2009 : 99 kg, 441 kg et 94 kg, pour 2,2 M, 10,6 M et 2,2 M USD.** Cela fait environ 22 000 à 24 000 USD/kg, proche du cours de l'or de l'époque. Il s'agit donc vraisemblablement d'or quasi pur déclaré comme « débris » : **environ 0,63 t d'or supplémentaire** à ajouter aux EAU pour ces années. C'est une inférence tirée de la valeur unitaire.
  - Faibles montants également en 2014 (2,75 kg, 65 000 USD) et 2018 (1,5 kg, 61 000 USD).
- **Allemagne, Belgique, Tchéquie, Singapour, Suède** : des dizaines de tonnes de masse brute, mais avec des valeurs unitaires de quelques dizaines à quelques centaines d'USD/kg. Ce sont des déchets industriels ou électroniques à faible teneur en métal précieux, et non de l'or.
  - Exemple : Allemagne 2021, 49 t pour 3,5 M USD.
  - Ces poids **ne doivent pas être additionnés** au tonnage d'or.

## 4. Bijouterie (SH 7113)

Total cumulé 2000–2025 : **≈ 5,5 M USD**, ce qui est marginal.

- Premiers déclarants : EAU (2,2 M USD, dont 2,1 M en 2012), États-Unis (0,95 M), Hong Kong (0,49 M en 2013), Allemagne (0,46 M), Royaume-Uni (0,27 M).
- Une partie relève de bijoux fantaisie ou en argent, comme le montrent les valeurs unitaires très basses. Exemple : Royaume-Uni 2025, 297 kg pour 3 648 USD.
- La bijouterie **ne modifie pas** les conclusions.

## 5. Recoupements avec les sources institutionnelles

| Source et affirmation | Comtrade (tous déclarants) | Verdict |
|---|---|---|
| ITIE 2021 : 5,6 t déclarées par les partenaires, contre 73 kg exportés officiellement ([source](https://www.joshuatberglan.com/cameroon-gold-gap-22-3kg-vs-15-2-tonnes-shadow-files)) | EAU 4,81 t + Rwanda 0,79 t = **5,60 t** | **Concordance exacte**. L'écart relevé dans la version 1 venait du Rwanda, qui n'avait pas été interrogé. |
| ITIE 2022 : 4,8 t déclarées par les partenaires, contre 47,88 kg déclarés ([Mongabay](https://fr.mongabay.com/2026/01/cameroun-polemique-autour-des-quantites-dor-exportees-en-2023/)) | EAU 4,71 t + Rwanda 0,11 t = **4,82 t** | **Concordance**. |
| ITIE 2023 : ≈ 15,2 t, dont plus de 90 % pour les EAU, contre 22,3 kg exportés officiellement ([EITI](https://eiti.org/impact-story/cameroons-gold-gap-how-eiti-data-driving-reforms), [EcoMatin](https://ecomatin.net/cameroun-15-tonnes-dor-echappent-aux-circuits-formels-dexportation-itie)) | EAU 14,05 + Ouganda 1,14 = 15,19 t. En ajoutant le Rwanda (3,06 t), on obtient **18,25 t**. | **Partielle.** Le chiffre ITIE correspond à EAU + Ouganda. L'enregistrement rwandais 2023 a peut-être été publié après l'extraction de l'ITIE, mais ce n'est pas vérifié. |
| Interpol (2021) : importations des EAU de 0,3 t (2008) à 11,7 t (2018) ([source secondaire](https://www.joshuatberglan.com/cameroon-gold-gap-22-3kg-vs-15-2-tonnes-shadow-files)) | EAU 301 kg (2008) et 11 712 kg (2018) | **Concordance**. |
| Sonamines, 25/05/2026 : ≈ 44 t enregistrées à Dubaï en 2021–2025, contre 148 kg déclarés. Pour 2024 : 12,2 t, contre 3,8 kg ([Sikafinance](https://www.sikafinance.com/marches/cameroun-entre-2021-et-2025-44-tonnes-dor-ont-ete-exportees-vers-duba%C3%AF-en-dehors-des-circuits-officiels_61973), [Capmad](https://www.capmad.com/article/cameroun-sonamines-chiffre-a-44-tonnes-lor-evapore-vers-dubai-entre-2021-et-2025)) | EAU 2021–2023 = 23,6 t. Pas de données EAU 2024–2025 dans Comtrade. | Impossible à vérifier pour 2024–2025. |
| Interpol/ENACT : 186 t d'or exportées du Cameroun, du Tchad et de la RDC vers les EAU ([EcoMatin](https://ecomatin.net/cameroun-tchad-rdc-186-tonnes-dor-exportees-illegalement-vers-les-emirats-interpol)) | – | Agrégat multi-pays, non comparable. |

## 6. Inférences (calculs de l'auteur, à vérifier)

1. **2024, flux probable tous partenaires** : environ 12,2 t (EAU, Sonamines) + 9,9 t (Rwanda et Ouganda, Comtrade) ≈ **22 t**. Ce serait l'année record de la série, à condition que le chiffre Sonamines soit exact et ne recouvre pas les flux rwandais et ougandais.
2. **2025, EAU** : 44 t (Sonamines 2021–2025) − 23,6 t (Comtrade 2021–2023) − 12,2 t (2024) ≈ **8 t**. En y ajoutant Rwanda et Ouganda (5,1 t), on obtient environ 13 t. Ce calcul est fragile : il mélange deux sources et dépend des arrondis.
3. **Cumul 2000–2025, ordre de grandeur** : 138,5 t (Comtrade) + 0,6 t (débris SH 7112 des EAU) + environ 20 t (EAU 2024–2025, estimation Sonamines) ≈ **160 t**.
4. **Le Rwanda et l'Ouganda sont devenus des destinations importantes à partir de 2019 et 2023.** Ces deux pays exportent eux-mêmes de grandes quantités d'or, en grande partie vers les EAU. Une partie de l'or camerounais pourrait donc rejoindre Dubaï *via* ces pays, auquel cas il serait compté comme origine Rwanda ou Ouganda à Dubaï. Cette hypothèse n'est pas vérifiée.
5. **Valeurs unitaires plausibles** : 2023, EAU, 62,6 USD/g. 2025, Ouganda, 113,5 USD/g. Ces niveaux sont cohérents avec la hausse du cours de l'or en 2025. Les poids déclarés correspondent donc vraisemblablement à de l'or presque pur.

## 7. Limites et explications concurrentes

- **Origine ou provenance ?** Le partenaire « Cameroun » est attribué par le pays déclarant. L'or peut avoir été extrait ailleurs, par exemple en République centrafricaine ou au Tchad, puis avoir transité par le Cameroun. À l'inverse, de l'or camerounais peut être enregistré sous une autre origine.
- **Erreurs de code pays possibles.** Elles concernent surtout les enregistrements rwandais et ougandais, d'apparition récente, et l'enregistrement allemand de 2013 (1 881 kg). Rien n'est vérifié : seuls les douanes ou les instituts statistiques de ces pays pourraient confirmer.
- **Un écart n'est pas une preuve de fraude.** Il peut venir de la contrebande, de la sous-déclaration, d'or transporté par des voyageurs sans enregistrement douanier (« hand-carry »), d'erreurs de code ou de conventions statistiques différentes.
- **Séries camerounaises divergentes** entre Comtrade et l'ITIE : 2021, 40 kg contre 73 kg ; 2022, 3,5 kg contre 47,88 kg.
- **2000–2003** : aucun enregistrement des EAU. On ne peut pas distinguer une absence d'importations d'une absence de déclaration à Comtrade.
- **2024–2025** : les données Comtrade sont incomplètes (EAU absents) et révisables.
- **Aperçu public de l'API** : il ne renvoie que les agrégats « tous modes de transport » et « tous régimes douaniers ». Il plafonne à 500 enregistrements par requête, plafond jamais atteint ici.

## 8. Contexte et réponse des autorités (2025–2026)

- Le rapport ITIE 2023 a été présenté le 10/12/2025. Le ministère des Mines a annoncé des mesures contre la contrebande le 29/12/2025 ([Agence Ecofin](https://www.agenceecofin.com/actualites/3012-134590-le-cameroun-annonce-des-mesures-contre-la-contrebande-dor-vers-les-emirats-arabes-unis)).
- En mai 2026, environ 200 sociétés minières artisanales illégales ont été identifiées dans l'Est et l'Adamaoua ([Business in Cameroon](https://www.businessincameroon.com/mining/1805-16183-cameroon-tightens-pressure-on-illegal-gold-miners-over-missing-export-revenue), [Pan African Visions](https://panafricanvisions.com/2026/05/cameroon-mines-ministry-cracks-down-on-illegal-artisanal-gold-mining/)).
- En juillet 2026, une campagne de recouvrement de plus de 500 M USD d'impôts et de droits a été annoncée, à partir du 1er août 2026 ([GNA](https://gna.org.gh/2026/07/cameroon-launches-push-to-recover-more-than-500-million-u-s-dollars-in-unpaid-gold-taxes/)).
- Contexte régional : selon SWISSAID, les EAU ont importé 2 569 t d'or africain non déclaré entre 2012 et 2022 ([SWISSAID](https://www.swissaid.ch/en/media/press-release-gold-study-2024/)) et 748 t d'or africain en 2024 ([Ecofin](https://www.ecofinagency.com/news-industry/0611-50175-uae-gold-imports-from-africa-rise-18-in-2024-says-swissaid)).

## 9. Pistes pour compléter

1. Vérifier dans les statistiques nationales du Rwanda (NISR) et de l'Ouganda (UBOS) les importations d'or attribuées au Cameroun.
2. Obtenir les données 2024–2025 des EAU auprès du Federal Competitiveness and Statistics Centre ou des douanes de Dubaï.
3. Se procurer les annexes « or » des rapports ITIE Cameroun et le rapport original Interpol/ENACT.
4. Ventiler par mode de transport (aérien, routier) et par code SH à 6 chiffres. Cela nécessite l'API Comtrade avec une clé.
