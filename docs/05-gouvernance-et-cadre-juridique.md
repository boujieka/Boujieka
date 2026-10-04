# 05 — Gouvernance des données, sensibilité et cadre juridique

C'est la partie la plus sous-estimée du concept initial, et probablement celle qui décidera de
l'acceptation du projet. Une base qui relie **personnes, terres, ressources, communautés et
infrastructures critiques** est un outil de planification puissant — et un outil de contrôle tout
aussi puissant si elle est mal gouvernée.

## 1. Classes de sensibilité

| Classe | Contenu typique | Accès | Diffusion |
|---|---|---|---|
| **S0 — Public** | Découpage administratif, routes, établissements publics, occupation du sol, agrégats de population respectant les seuils | Tous | Données ouvertes possibles |
| **S1 — Restreint** | Droits fonciers nominatifs (selon la loi), infrastructures critiques, signalements de conflits, localisation précise de certaines ressources | Administrations habilitées, par secteur | Non |
| **S2 — Confidentiel** | Microdonnées du recensement, données d'état civil nominatives | Institution responsable uniquement, dans l'enclave | Jamais ; agrégats seulement |
| **S3 — Protégé culturel** | Forêts sacrées, objets rituels, savoirs traditionnels désignés comme tels par la communauté | Selon accord avec la communauté | Selon accord ; par défaut non localisé publiquement |

## 2. Principes

1. **Finalité** : chaque catégorie de données a une finalité écrite ; un nouvel usage nécessite une décision formelle.
2. **Minimisation** : on ne collecte pas ce dont aucune finalité n'a besoin (ex. ethnie, religion des personnes : *ne pas collecter* dans l'atlas).
3. **Cloisonnement** : enclave statistique séparée ; pas de jointure individu ↔ droit foncier dans la base commune.
4. **Agrégation sûre** : seuils minimaux par cellule et contrôle du risque de ré-identification par croisement.
5. **Traçabilité des accès** : journal inaltérable de qui a consulté quoi ; audit par une instance indépendante.
6. **Souveraineté** : hébergement sur le territoire national ou dans un cadre juridique validé par l'État ; réversibilité contractuelle ; code et formats ouverts pour éviter l'enfermement propriétaire.
7. **Contestabilité** : toute personne ou communauté peut contester une information la concernant, avec un circuit de traitement.
8. **Neutralité juridique** : la plateforme n'établit aucun droit ; l'affichage d'une information foncière n'a pas valeur de preuve.

## 3. Cadre juridique et institutionnel camerounais

**Méthode et limites de la vérification (octobre 2026).** Chaque référence a été recoupée par recherche
web avec au moins une source secondaire identifiable : base LEAP/PNUE, FAOLEX, UNESCO, ITIE, INS,
revues juridiques, presse. **Les textes officiels eux-mêmes (Journal officiel) n'ont pas été consultés**,
et les sites de presse camerounais n'étaient pas accessibles en lecture directe depuis l'environnement
de travail. Une revue par un juriste reste nécessaire avant toute présentation institutionnelle.

Légende : ✅ confirmé par au moins une source fiable · ⚠️ corrigé par rapport à la version précédente · ❓ non confirmé

### 3.1 Textes

| Domaine | Référence | Statut | Conséquence pour le projet |
|---|---|---|---|
| Données personnelles | **Loi n° 2024/017 du 23 décembre 2024** relative à la protection des données à caractère personnel. Elle crée une Autorité de protection des données. Selon la presse spécialisée, **entrée en vigueur effective le 23 juin 2026** (délai de mise en conformité de 18 mois) | ✅ ⚠️ référence précisée | Le projet est soumis à cette loi **dès sa conception**. Base légale de chaque traitement, déclarations ou autorisations auprès de l'Autorité, règles de transfert hors du pays. Décrets d'application et installation effective de l'Autorité : ❓ à suivre |
| Cybersécurité | **Loi n° 2010/012 du 21 décembre 2010** relative à la cybersécurité et à la cybercriminalité. Régulateur : ANTIC | ✅ | Sécurité des systèmes, signature électronique, obligations de conservation pour les opérateurs |
| Statistique | **Loi n° 2020/010 du 20 juillet 2020** régissant l'activité statistique (remplace la loi de 1991). Visa statistique obligatoire pour les enquêtes nationales ou régionales | ✅ | **Toute collecte auprès des ménages ou des entreprises faite par la plateforme peut exiger un visa statistique.** À intégrer au plan du pilote. Dispositions exactes sur le secret statistique : ❓ à lire dans le texte |
| Foncier | **Ordonnance n° 74-1 du 6 juillet 1974** (régime foncier) et **n° 74-2 du 6 juillet 1974** (régime domanial), modifiées (ex. loi n° 83-19 du 26 novembre 1983). Les terres sont classées en domaine public, domaine privé de l'État, propriété privée et domaine national | ✅ | Les catégories de régime dans `nomenclatures/usages_et_regimes.yaml` sont cohérentes avec cette classification |
| Foncier coutumier (**nouveau**) | **Lettre-circulaire du MINDCAF du 20 février 2026**, applicable au **1ᵉʳ avril 2026**. Elle crée deux documents délivrés par les **chefs traditionnels de 3ᵉ degré** sur les dépendances du domaine national déjà occupées ou exploitées : **ARDFC** (Attestation de reconnaissance des droits fonciers coutumiers) et **AJPTER** (Attestation de jouissance paisible des terres). Ils sont présentés comme un **« commencement de preuve »** et des documents **intermédiaires** vers le titre foncier, **pas** comme des titres | ✅ (presse ; texte non consulté) ⚠️ **changement majeur** | Voir §3.3 |
| Chefferies | **Décret n° 77/245 du 15 juillet 1977** portant organisation des chefferies traditionnelles : organisation territoriale, **trois degrés** (1ᵉʳ, 2ᵉ, 3ᵉ). Tutelle : MINAT | ✅ | Champ « degré » de la chefferie ; le 3ᵉ degré correspond au niveau village, désormais concerné par la circulaire foncière de 2026 |
| Mines | **Loi n° 2023/014 du 19 décembre 2023 portant Code minier** (remplace le code de 2016). Un décret de 2024/2025 précise les conditions d'exploitation des carrières (référence exacte ❓) | ✅ ⚠️ précisé | Nomenclature des titres miniers à aligner sur le code de 2023 |
| Forêts et faune | **Loi n° 2024/008 du 24 juillet 2024 portant régime des forêts et de la faune**. Elle **abroge la loi n° 94/01 du 20 janvier 1994** et intègre les droits coutumiers et d'usage des communautés riveraines | ✅ ⚠️ **à ne plus citer la loi de 1994** | Catégories forestières (concessions, forêts communautaires et communales) à réaligner sur la loi de 2024 et ses décrets d'application (❓ publiés ?) |
| Pêche et aquaculture | **Loi n° 2024/019 du 23 décembre 2024** régissant la pêche et l'aquaculture (la pêche était auparavant couverte par la loi de 1994) | ✅ nouveau | Couche halieutique et pisciculture |
| Décentralisation | **Loi n° 2019/024 du 24 décembre 2019 portant Code général des collectivités territoriales décentralisées** | ✅ | Communes et régions comme contributeurs et utilisateurs ; compétences transférées (éducation de base, santé, développement local) |
| Patrimoine culturel | **Loi n° 2013/003 du 18 avril 2013** régissant le patrimoine culturel | ✅ nouveau | Base légale de la couche patrimoine et du classement S3 ; à articuler avec le registre des chefferies |
| Planification | **SND30**, Stratégie nationale de développement 2020-2030 (présentée en novembre 2020). Axes : transformation structurelle, capital humain, emploi, **gouvernance, décentralisation et gestion stratégique de l'État** | ✅ | Ancrage du module INTELLIGENCE. La presse (août 2026) fait état d'un bilan à mi-parcours inférieur à 50 % des objectifs : un argument pour un outil de suivi territorial |

### 3.2 Institutions

| Institution | Élément vérifié | Statut |
|---|---|---|
| **BUCREP** | Établissement public administratif créé par décret n° 99/230 du 4 octobre 1999, réorganisé par décret n° 2005/309 du 1ᵉʳ septembre 2005 | ✅ |
| **INS** | Institut national de la statistique ; applique la loi 2020/010 (visa statistique) | ✅ |
| **INC** | Institut national de cartographie, créé par décret n° 92/049 du 24 mars 1992, réorganisé par décret n° 2018/665 du 5 novembre 2018. Missions : géodésie, photogrammétrie, télédétection, carte de base du Cameroun | ✅ |
| **MINDDEVEL** | Ministère de la Décentralisation et du Développement local, créé par décret n° 2018/190 du 2 mars 2018 | ✅ |
| **MINDCAF** | Domaines, cadastre et affaires foncières ; auteur de la circulaire du 20 février 2026 | ✅ |
| **MINAT** | Administration territoriale, tutelle des chefferies. En décembre 2025, il a demandé aux gouverneurs des propositions de **nouveaux départements et arrondissements** | ✅ |
| **ITIE** | Le Cameroun met en œuvre l'ITIE depuis 2005 (candidat en 2007, conforme en 2013). Validation la plus récente lancée le 1ᵉʳ octobre 2023, rapport final de février 2024 | ✅ |
| MINMIDT, MINFOF, MINEPAT, MINAC | Ministères sectoriels cités | ❓ dénominations actuelles non revérifiées individuellement |

### 3.3 Conséquences de la circulaire foncière de février 2026

La version précédente posait comme principe que le chef « ne valide pas juridiquement » les droits fonciers.
**Ce principe doit être nuancé** : depuis le 1ᵉʳ avril 2026, le chef de 3ᵉ degré **délivre** des
attestations (ARDFC, AJPTER) qui ont une valeur administrative de **commencement de preuve**.

Conséquences pour le modèle :
1. ARDFC et AJPTER deviennent des **types de droit** à part entière (`DROIT.ARDFC`, `DROIT.AJPTER`), distincts
   du titre foncier, avec leur numéro, la chefferie émettrice et la date.
2. Leur enregistrement à partir du registre officiel des attestations est une source N3 : l'assertion
   « une attestation a été délivrée » peut être VALIDÉE. Ce qui est validé, c'est **l'existence du document**,
   pas un droit de propriété. L'interface doit l'afficher clairement.
3. Le chef a désormais **deux casquettes** dans la plateforme :
   - **sentinelle** : déclarations N0, comme avant ;
   - **autorité émettrice** d'attestations, qui sont des actes.
   
   Ces deux rôles doivent rester séparés dans les droits d'accès et dans la traçabilité.
4. Risque accru de **conflit d'intérêts** et de **délivrances concurrentes** sur une même parcelle. La
   détection de chevauchements entre attestations, titres et concessions devient une fonction prioritaire du
   moteur de rapprochement. C'est aussi un argument de valeur fort auprès du MINDCAF.
5. Incertitudes ❓ :
   - la presse titre « titres fonciers provisoires », alors que la circulaire parle d'attestations : c'est le
     vocabulaire de la circulaire qui doit prévaloir ;
   - une circulaire est un texte de rang inférieur à une ordonnance, et une partie de la presse discute sa
     compatibilité avec l'ordonnance de 1974. Sa stabilité juridique est donc incertaine ;
   - modalités pratiques (registre, formulaires, contrôle par le sous-préfet ou les services domaniaux) : non confirmées.

### 3.4 Sources consultées (secondaires)

- Données personnelles : [CIO Mag — loi du 23 décembre 2024](https://cio-mag.com/?p=59861) ; [Droit Médias Finance — entrée en vigueur au 23 juin 2026](https://droitmediasfinance.com/index.php/actualites/droit-tech-fintech/1297-cameroun-la-loi-sur-la-protection-des-donnees-a-caractere-personnel-entre-en-vigueur-ce-23-juin-2026)
- Cybersécurité : [Digwatch — loi 2010/012](https://dig.watch/resource/the-law-no-2010-012-of-21-december-2010-on-cybersecurity-and-cybercriminality-in-cameroon)
- Statistique : [INS — loi 2020/010 et visa statistique](https://ins-cameroun.cm/en/according-to-law-no-2020-010-of-20-july-2020-the-statistical-visa-becomes-mandatory-2/) ; [AFRISTAT — texte de la loi](https://www.afristat.org/wp-content/uploads/2023/02/CM01_LOI-STATISTIQUE.pdf)
- Foncier : [FAOLEX](https://faolex.fao.org/docs/pdf/cmr50068.pdf) ; [Réseau FAR — accès au foncier au Cameroun](https://reseau-far.com/fileadmin/user_upload/Rencontres/Colloque_insertion_juin_2014/Acces_au_foncier_au_Cameroun_C_Mbira_Abouem.pdf)
- Circulaire 2026 : [Investir au Cameroun](https://www.investiraucameroun.com/gestion-publique/2402-23133-cadastre-des-le-1er-avril-2026-les-chefs-traditionnels-de-3e-degre-pourront-delivrer-des-titres-fonciers-provisoires) ; [Journal du Cameroun](https://fr.journalducameroun.com/foncier-les-chefferies-traditionnelles-desormais-au-coeur-des-transactions-au-cameroun/) ; [Cameroon Concord News](https://www.cameroonconcordnews.com/yaounde-grants-traditional-chiefs-power-to-issue-provisional-land-certificates/) ; [AllAfrica — « La réforme qui défie l'ordre juridique établi »](https://fr.allafrica.com/stories/202603180266.html)
- Chefferies : [Revue générale de droit (Érudit)](https://www.erudit.org/fr/revue/rgd/2002/v32/n2/1028073ar.pdf)
- Mines : [LEAP/PNUE — loi 2023/014](https://leap.unep.org/en/countries/cm/national-legislation/loi-ndeg-2023-014-du-19-decembre-2023-portant-code-minier)
- Forêts : [LEAP/PNUE — loi 2024/008](https://leap.unep.org/en/countries/cm/national-legislation/loi-ndeg-2024-008-du-24-juillet-2024-portant-regime-des-forets-et) ; [PFBC — analyse de la nouvelle loi](https://pfbc-cbfp.org/fileadmin/user_upload/pfbc-cbfp/Actualites/2024/2024-12/Analyse_de_la_nouvelle_loi_forestiere.pdf)
- Pêche : [LEAP/PNUE — loi 2024/019](https://leap.unep.org/en/countries/cm/national-legislation/loi-ndeg-2024019-du-23-decembre-2024-regissant-la-peche-et)
- Décentralisation : [LEAP/PNUE — loi 2019/024](https://leap.unep.org/en/countries/cm/national-legislation/loi-ndeg-2019024-du-24-decembre-2019-portant-code-general-des)
- Patrimoine : [UNESCO — législations du Cameroun](https://whc.unesco.org/en/statesparties/cm/laws/)
- SND30 : [ONU Cameroun](https://cameroon.un.org/en/node/134598) ; [Financial Afrik, août 2026](https://www.financialafrik.com/2026/08/25/cameroun-la-snd30-na-pas-atteint-50-de-ses-objectifs-a-mi-parcours/)
- Institutions : [INC (UNGEGN 2023)](https://unstats.un.org/unsd/ungegn/sessions/3rd_session_2023/documents/GEGN.2_2023_16_CRP16.pdf) ; [INS — organisation administrative](https://ins-cameroun.cm/wp-content/uploads/2021/02/0-CHAPITRE-2_ORGANISATION-INSTITUTIONNELLE-ADMINISTRATIVE-ET-POLITIQUE.pdf) ; [ITIE — validation 2023](https://eiti.org/sites/default/files/2024-02/FR%20EITI%20Validation%20of%20Cameroon%20%282023%29%20-%20FInal%20Validation%20report%20%28February%202024%29.pdf) ; [Journal du Cameroun — nouveaux départements](https://fr.journalducameroun.com/cameroun-le-minat-entend-creer-de-nouveaux-departements-et-arrondissements/)

## 4. Gouvernance proposée

- **Comité de pilotage interministériel** (planification, territoire, domaines, statistique, cartographie, décentralisation, secteurs).
- **Propriétaire des données** : chaque couche a un *propriétaire institutionnel* (ex. carte scolaire → ministère de l'éducation) qui valide et fixe la diffusion.
- **Opérateur technique** : exploite la plateforme, sans droit de propriété sur les données ni droit de réutilisation commerciale non autorisée.
- **Comité éthique et patrimoine** incluant des représentants des autorités traditionnelles pour la classe S3.
- **Audit indépendant** des accès et de la sécurité.

## 5. Données ouvertes et licences des sources

- Les données OpenStreetMap sont sous licence **ODbL** (partage à l'identique pour les bases dérivées) :
  l'intégration doit être conçue pour respecter cette obligation (ex. couche séparée), ce qui peut entrer
  en tension avec une diffusion restreinte.
- Les jeux d'empreintes de bâtiments et de population maillée ont chacun leur licence : **à inventorier** en phase 0.
