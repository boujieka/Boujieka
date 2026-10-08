# Module 02 — MINERAL POTENTIAL · « Can we identify Cameroon's next gold target? »

**Africa Mineral Insights — édition Cameroun**
Livrable : **Cameroon Gold Prospectivity Map** (High / Medium / Low potential / Insufficient data)

> Version de travail du 2026-10-08. Contenu de formation et d'analyse. Ce n'est ni un conseil en
> investissement ni une déclaration de ressources minérales.
>
> **Conventions de statut** (appliquées partout dans ce document) :
> - **[F] Fait vérifié** : lu dans la source citée (page web consultée, RNS, ou résumé d'article
>   scientifique dont le DOI a été contrôlé dans Crossref).
> - **[F-e] Fait vérifié sur extrait seulement** : vu dans un extrait de moteur de recherche, sans
>   relecture complète de la page. À reconfirmer avant toute diffusion.
> - **[I] Inférence** : déduction raisonnée à partir de faits vérifiés.
> - **[H] Hypothèse ou choix de conception** : proposition pédagogique ou méthodologique, à
>   discuter et calibrer.
> - **[?] Inconnue / Non vérifié** : pas de source consultée qui l'établisse.
>
> Les identifiants entre crochets ([S3], [L7], [M2]…) renvoient à la section 12.
> **Limite de la recherche** : le quota de recherches web de la session a été atteint pendant le
> travail. Certains points (carte géologique nationale numérique, archives BRGM/PNUD, accès réel
> au SIGM, statut du cadastre) n'ont donc pas pu être vérifiés et figurent en section 11.

---

## 1. Résumé

- **Le contexte se prête à l'exercice [F].** L'or primaire du Cameroun est surtout associé à la
  ceinture panafricaine d'Afrique centrale (Central African Fold Belt, CAFB), au nord du craton du
  Congo. Il est contrôlé par des zones de cisaillement NE–SW à ENE–WSW (cisaillement
  Centre-Camerounais, faille de la Sanaga, cisaillement de Bétaré-Oya, cisaillement de
  Tcholliré-Banyo) et par leurs structures de second ordre. Plusieurs districts de l'Est sont
  classés dans la littérature comme de l'**or orogénique mésozonal**
  ([L5], [L6]) ; d'autres auteurs y voient un lien avec des granitoïdes de type I d'environ 620 Ma
  ([L11], [L30]).
- **Les ressources déclarées selon un code reconnu se trouvent hors du « goldfield » de l'Est [F].**
  Ce point est important pour la pédagogie. Selon Oriole Resources (RNS du 22/09/2026, [S13]) :
  - **Mbe** (licence de 312 km², « principalement dans la région de l'Adamaoua ») : ressource
    JORC *Inferred* de **50,60 Mt à 1,02 g/t Au pour 1,66 Moz** ;
  - **Bibemi** (région du Nord d'après des extraits de presse [F-e] ; licence de 177 km² [S13]) : MRE JORC 2012 de **6,96 Mt à 2,06 g/t pour
    environ 460 000 oz**, dont 100 000 oz *Indicated* ([S11]) ; la demande de permis
    d'exploitation (ELA) est toujours en cours au 22/09/2026 ([S13]).
  - Dans l'Est, l'activité est massivement artisanale et semi-mécanisée. Aucune ressource
    conforme à un code n'a été trouvée pour Kambélé/Batouri ([?]).
- **L'orpaillage pèse lourd mais reste mal mesuré [F].** SONAMINES a déclaré 859,92 kg d'or en
  2022 (353,63 kg en 2021). Batouri en fournit 37,3 %, Bétaré-Oya 20,29 % et Ngoura 15,50 %. Selon
  l'ITIE, 90 % de la production artisanale et semi-mécanisée échappe aux circuits formels ([S9]).
- **Les données publiques sont le point faible [F/?].** Le programme PRECASEM (Banque mondiale)
  prévoyait :
  - des levés aéroportés sur environ 160 000 km² ([S5]) ;
  - des cartes géologiques au 1/200 000 et une campagne géochimique, réalisées par le consortium
    BRGM–BEIG3–GTK ([S2], [S4]) ;
  - un SIG minier (SIGM) ([S4]).

  L'accès effectif à ces données, leurs conditions de réutilisation et leur couverture réelle
  restent **non vérifiés**.
- **Méthode proposée [H]** :
  1. un modèle **knowledge-driven** (indexation pondérée et logique floue), fondé sur l'approche
     « systèmes minéraux » appliquée à l'or orogénique ([M1], [M2], [M4]) ;
  2. un modèle **data-driven** de contrôle (*weights of evidence*, [M3]) à l'échelle d'un district
     ;
  3. une validation par **retrait spatial de districts entiers** et par courbes de succès et de
     prédiction ([M5], [M6]).

  Le test le plus parlant consiste à entraîner le modèle sur l'Est et à vérifier s'il « retrouve »
  Mbe et Bibemi.

## 2. Corrections au document de cadrage

| # | Affirmation du cadrage (AFRICA_MINERAL_INSIGHTS.md) | Constat | Correction proposée |
|---|---|---|---|
| C1 | SIGM : « campagne citée : 18 000 échantillons, 300 sites » | **Inexact et mal sourcé.** La source citée par le cadrage (Financial Afrik, 2025, [S1]) ne mentionne ni « SIGM », ni PRECASEM, ni 18 000, ni 300. Le chiffre 18 000 est un **objectif annoncé en janvier 2017** (« a sampling of a total of 18000 specimens », 13 cartes au 1/200 000, 30 mois) [S2]. Les « 300 nouveaux sites » sont un **résultat annoncé en juin 2019**, qui cumule les travaux 2014–2019 (géophysique aéroportée comprise) [S3]. Ce ne sont pas des chiffres d'une même campagne. | « Programme PRECASEM : campagne géochimique **prévue** de ~18 000 échantillons (annonce 2017, [S2]) ; 300 « nouveaux sites miniers » annoncés en 2019 pour 2014–2019 [S3]. Nombre d'échantillons réellement analysés : **non vérifié**. » |
| C2 | SIGM « financé par la Banque mondiale (PRECASEM) » | **Partiellement vérifié.** Une présentation du BRGM (IGF, 2018) décrit trois volets PRECASEM : 13,5 cartes au 1/200 000, une campagne géochimique et un SIG adapté. Elle montre aussi une « SIGM architecture proposition » [S4]. Aucune URL publique du SIGM n'a été trouvée. | Garder le lien PRECASEM–SIGM, mais remplacer la source par [S4]. Ajouter : « accès public non établi ». |
| C3 | « Une étude pour l'AMDC rapportée en 2025 juge les données en grande partie obsolètes et insuffisamment standardisées » | **Vérifié** [S1]. L'article parle du « système d'information géologique et minérale » (1929 à aujourd'hui), qui présente « quelques défaillances ». Les données y sont « jugées pour la plupart obsolètes ». L'article ne nomme pas le SIGM du PRECASEM. | Conserver, en précisant que l'article ne dit pas s'il s'agit du système livré par le PRECASEM. |
| C4 | Flux du module : « Géologie + Géochimie + Télédétection + Structures + **Occurrences connues** → matrice de prospectivité » | **Erreur de méthode.** Si les occurrences connues servent de couche de preuve *et* de jeu de validation, la validation est circulaire. Le flux oublie aussi la **géophysique** (aéromagnétisme PRECASEM ; gravimétrie EGM2008 utilisée par [L24], [L29]). | `Géologie + Structures (MNT/radar/aéromag) + Géochimie + Géophysique + Télédétection (savane) → modèle → carte`. Les occurrences servent à **entraîner et valider**, pas comme couche d'entrée. |
| C5 | Validation : « mettre de côté une partie des occurrences » | **Correct mais insuffisant.** Les occurrences d'or sont spatialement groupées : l'analyse de Fry et des quadrats le montre à Bétaré-Oya [L7]. Un retrait aléatoire de points laisse donc des voisins proches dans l'entraînement, ce qui gonfle la performance [I]. | Retrait **par blocs spatiaux ou par districts** (voir § 6.5) et courbes de succès et de prédiction [M5]. |
| C6 | « Ne pas confondre orpaillage alluvionnaire et gisement primaire » | **Correct, à nuancer.** Une partie de l'or exploité est **éluvial**, issu de filons proches (Batouri [L12], [L15]). La morphologie des grains permet d'estimer la distance à la source : moins de 5 km à Gamba [L22], 0–300 m ou plus de 1 000 m à Guiwa-Yangamo [L27]. | Distinguer trois classes d'occurrences : **primaire** (filon, roche en place), **éluviale/colluviale** (source proche) et **alluviale** (source à l'amont du bassin versant). Seules les deux premières servent de points d'entraînement. Les alluvions servent à construire une couche de bassins versants « en aval d'une source ». |
| C7 | Classes « High / Medium / Low / Insufficient data » | Le cadrage ne définit pas les classes. Le risque est de confondre « faible potentiel » et « pas de données » [I]. | Calculer **deux** grandeurs par cellule : un score de prospectivité et un **indice de couverture des données**. « Insufficient data » dépend uniquement du second (§ 8). |
| C8 | Régions aurifères implicites (Est, Adamaoua) | **Incomplet.** Des minéralisations primaires sont documentées dans le Nord : Bibemi ([S11] ; région du Nord [F-e] ; cible de télédétection [L18]), Poli [L21], Tcholliré [L20], [L23]. Des minéralisations sont aussi signalées dans le Sud (corridor Eséka–Lolodorf–Bipindi [L25]) et dans l'Ouest (Kékem, cisaillement Centre-Camerounais [L9]). | Carte nationale, avec un zoom sur district (§ 7). |
| C9 | Socle de données : USGS « année de référence 2018 » | **Vérifié** pour la carte GeoPDF OFR 2024-1041 [S8]. La page de la *data release* ne mentionne pas d'année de référence, mais indique la licence **CC0 1.0** et le DOI 10.5066/P97EQWXP [S7]. | Ajouter la licence CC0 : cela règle en partie le point ouvert n° 4 pour l'USGS. |
| C10 | Dépendance : « 02 utilise 01 » uniquement | **Incomplet [I].** Le module 02 a aussi besoin des occurrences et des projets (couches USGS, RNS des sociétés), qui relèvent en principe du module 03. Le module 02 renvoie par ailleurs vers le 01 (validation des cibles satellitaires). | Préciser que le 02 utilise le livrable du 01 **et** les couches d'occurrences de base, qu'il renvoie un retour au 01 et qu'il alimente le 03 et le 07 (§ 9). |

## 3. Contexte géologique

### 3.1 Architecture régionale [F]

- **Domaines tectoniques.** La CAFB borde le nord du craton du Congo. Toteu et al. (2022) y
  distinguent quatre ensembles ([L1]) :
  - le craton du Congo ;
  - les nappes de Yaoundé–Yangana, charriées sur le craton ;
  - le **bloc d'Adamawa-Yadé** ;
  - l'arc magmatique de **Poli–Léré** au nord.

  Leur chronologie ([L1]) : plutonisme pré-tectonique culminant entre 650 et 620 Ma, collision à
  partir de ~620 Ma, faciès granulite vers ~600 Ma, magmatisme syntectonique de 600 à 580 Ma (en
  partie contrôlé par des cisaillements transcurrents régionaux) et granitoïdes post-tectoniques
  vers ~550 Ma.
- **Socle ancien dans l'Adamawa-Yadé.** Tchakounté et al. (2017) y décrivent des TTG de 3,0 à
  2,5 Ga, retravaillés à l'Éburnéen (~2,07 Ga) puis au Panafricain. Pour eux, ce domaine est un
  microcontinent archéen/paléoprotérozoïque ([L3]). L'interprétation est discutée : un
  commentaire a été publié par Ngako & Njonfang (2018) ([L3]). [F] Pour la formation, c'est un
  exemple de modèle géologique non consensuel.
- **Cisaillements.** Le cisaillement Centre-Camerounais (CCSZ) et son relais, la faille de la
  Sanaga, ont d'abord joué en sénestre (D2), puis en dextre (D3). Le **bassin du Lom** s'est ouvert
  en *pull-apart* comme relais transtensif de la faille de la Sanaga ([L2]). Au sud, la marge du
  craton montre des chevauchements à faible pendage à l'est et le cisaillement décrochant de
  Kribi–Campo à l'ouest ([L4]).

### 3.2 Âge et contrôle de l'or

- **Âges [F].**
  - Les granitoïdes aurifères de Kambélé (Batouri) donnent des âges U–Pb sur zircon de
    619 ± 2 Ma et 624 ± 2 Ma ([L11]).
  - À Ngoura–Colomines, les granitoïdes sont datés de 629,8 à 633,0 Ma. Les filons aurifères les
    recoupent : la minéralisation est donc plus jeune que ~630 Ma ([L8]).
  - À Kékem, l'or serait surtout lié à l'épisode dextre D3, entre 570 et 552 Ma ([L9]).
- **Style [F].**
  - Woumbou–Colomine–Kette : or mésozonal orogénique. Il est contrôlé par des branches NE à E du
    cisaillement de la Sanaga et se trouve le long des contacts granite–gneiss. Les fluides sont
    aquo-carboniques peu salés (~7,5 % pds éq. NaCl), à ~300 °C, ~2 kbar et ~7 km de profondeur
    ([L5]).
  - Ceinture du Lom (Bétaré-Oya) : filons N à NE associés au cisaillement de Bétaré-Oya. Les
    conditions sont ~310 °C et 6 à 9 km de profondeur. La source des fluides est probablement
    métamorphique ([L6]).
- **Débat sur le modèle [F → I].** Plusieurs travaux soulignent le lien avec des granitoïdes de
  type I oxydés (série à magnétite) et évoquent un potentiel « granite-related » à fort tonnage
  ([L11], [L30], [L31]).
  - À Tcholliré, la chimie des grains (électrum, Cu élevé, cassitérite) suggère un système
    **magmatique-hydrothermal ou épithermal** possiblement lié à la Ligne volcanique du Cameroun
    ([L23]).
  - **[I]** Le modèle « orogénique » n'est donc pas universel. Les couches « granitoïdes » et
    « cisaillements » sont toutefois utiles pour les deux modèles, ce qui limite le risque de
    mauvais choix.
- **Contrôles structuraux quantifiés [F].**
  - Bétaré-Oya : les structures NE–SW de type P dominent le contrôle, devant les NNE–SSW. Les
    gîtes sont groupés et alignés ([L7]).
  - Batouri : la plus forte densité de linéaments coïncide avec la zone la plus minéralisée ; l'or
    se concentre dans des cisaillements NE–SW mylonitiques qui recoupent la granodiorite ([L28]).
  - Mbe : l'or est lié à des cisaillements raides NNE et NNW, aux intersections structurales et à
    un dyke felsique NE–SW dans des orthogneiss ([S12]).

### 3.3 Signatures d'exploration utiles [F]

- **Altérations.** On observe séricitisation, silicification, sulfuration/ferruginisation et
  altération potassique. Les teneurs atteignent 103,7 ppm Au dans des granitoïdes bréchifiés de
  Batouri ([L14]). Dans la zone Gankoumbol–Djouzami–Beka, les teneurs vont jusqu'à 1,8 g/t ([L32]).
- **Éléments indicateurs (*pathfinders*).**
  - Au–As–Sb–W dans les sols de la plaine de Kambélé ([L-Etutu], voir § 12) ;
  - association Au–As–Hg–Zn–Pb–Sb–Mo dans les filons de Batouri ([L13]) ;
  - Bi comme élément le plus corrélé à l'or dans 550 sols à Tikondi ([L26]) ;
  - Au–S–Cu–Mn–Te–Fe–Mo–Bi à Gankoumbol–Djouzami–Beka ([L32]).
- **Tourmaline.** Les roches riches en tourmaline proches des plutons felsiques du Haut-Lom sont
  proposées comme cibles ([L10]).
- **Régolithe.**
  - L'or des sols de Batouri est **particulaire et résiduel**, sans remobilisation chimique.
    Beaucoup d'horizons de puits sont stériles ([L12]).
  - **[I]** Une géochimie « or seul » sur latérite peut donc manquer des cibles. L'échantillonnage
    de concentrés (or particulaire) et les éléments indicateurs sont nécessaires.
  - Le mercure des orpailleurs contamine les sols ([L15]) : **[I]** les anomalies en Hg ne sont
    pas des indicateurs fiables dans les zones d'orpaillage.

### 3.4 Régions aurifères (synthèse)

| Région / district | Contexte | Statut des connaissances | Sources |
|---|---|---|---|
| **Est** : Bétaré-Oya (Lom), Batouri/Kambélé, Ngoura–Colomines, Kette, Woumbou | Adamawa-Yadé, bassin du Lom, branches de la Sanaga et du cisaillement de Bétaré-Oya | Filons étudiés (inclusions fluides, isotopes, âges) ; exploitation artisanale et semi-mécanisée intense ; pas de ressource conforme trouvée | [L5]–[L8], [L11]–[L16], [S9] |
| **Est (marge NE)** : Borongo–Mborguéné | Transition subtropicale à aride ; télédétection exploitable | Cibles par Landsat-8/ASTER et logique floue, validées sur le terrain (filons à or, galène, pyrite, hématite) | [L17] |
| **Adamaoua** : Mbe ; Yopa/Boékini ; Meiganga | Orthogneiss, dykes felsiques, cisaillements NNE/NNW ; zone de Tcholliré-Banyo à proximité | **Mbe : 1,66 Moz *Inferred* (JORC)** ; Yopa : cibles aéromagnétiques | [S12], [S13], [L19], [L31] |
| **Nord** : Bibemi, Poli, Tcholliré, Gamba | Arc de Poli–Léré, ceintures volcano-sédimentaires de Poli et Bibemi, cisaillement de Tcholliré | **Bibemi : ~460 koz (JORC, Ind.+Inf.)** ; filons dans un cisaillement ENE–WSW à Poli ; or alluvial à source proche à Gamba | [S11], [S13], [L18], [L20]–[L24] |
| **Ouest / Centre** : Kékem (CCSZ) | Cisaillement Centre-Camerounais | Cible structurale proposée | [L9] |
| **Sud** : Eséka–Lolodorf–Bipindi | Plateau sud-camerounais, linéaments NE–SW et N–S | Décrit comme « an important gold mining site » ; analyse structurale seulement | [L25] |

## 4. Gisements, projets et occurrences documentés

### 4.1 Projets avec déclaration selon un code reconnu

| Projet | Localisation | Opérateur / détention | Stade (date) | Ressource déclarée | Code | Source | Statut |
|---|---|---|---|---|---|---|---|
| **Mbe** (MB01-S + MB01-N) | Licence de 312 km², « mainly in the Adamawa Region » ; incluse dans le paquet Eastern CLP de 2 266 km² ([S12]) | Oriole Resources 50 %, BCM International 50 % ([S13]) | Exploration avancée (RNS du 22/09/2026) | **Total : 50,60 Mt à 1,02 g/t = 1,66 Moz (*Inferred*)**. MB01-S (mise à jour du 23/07/2026) : 40,10 Mt à 1,01 g/t = 1,30 Moz. MB01-N (avril 2026) : 10,50 Mt à 1,05 g/t = 360 koz. Coupure 0,40 g/t ; prix de 3 200 US$/oz ; contraintes de fosse | JORC | [S13] | [F] |
| Mbe, estimation initiale de MB01-S | idem | idem | Octobre 2025 | 870 koz à 1,09 g/t (*Inferred*) | JORC | [S12], [S13] | [F] (dépassé) |
| **Bibemi** (Bakassi Zone 1) | Licence de 177 km², région du Nord ([S13] pour la surface ; région du Nord d'après des extraits [F-e]) | Oriole 50 % / BCM 50 % ([S13]) | Demande de permis d'exploitation (ELA) **en cours** au 22/09/2026 ; EIES approuvée ([S10]) | **6,96 Mt à 2,06 g/t ≈ 460 koz**, dont 100 koz *Indicated* à 2,05 g/t et 360 koz *Inferred* à 2,06 g/t. Coupure 0,40 g/t ; fosse à 2 750 US$/oz (mai 2025) | JORC 2012 ; personne compétente : R. Davies (Forge International) | [S11] | [F] |
| Bibemi : *Exploration Target* | Bakassi Z1, Z2, Lawa Est/Ouest | idem | — | 3–5 Mt à 1,5–2,5 g/t = 145–400 koz. **Conceptuel : ne s'ajoute pas aux ressources** | JORC (Exploration Target) | [S11] | [F] |
| Bibemi : PEA interne | idem | idem | Décembre 2025 | Mine à ciel ouvert de petite taille ; ~89 koz in situ à 2,20 g/t ; 10 koz/an sur 7 ans ; VAN après impôt de 12,8 M US$ à 3 200 US$/oz | PEA interne (moins de 20 % des ressources) | [S13], [S14] | [F] |

**Points pédagogiques [I]** :
- les deux seuls projets dotés d'une ressource conforme se trouvent hors des districts
  artisanaux les plus productifs ;
- Mbe est passé d'une anomalie de sols à une ressource de 1,66 Moz entre 2021 et 2026
  ([S12], [S13]). C'est un cas d'école pour l'exercice de rétro-prédiction (§ 6.5).

### 4.2 Projets ou sites sans ressource conforme

| Site | Localisation | Ce qui est documenté | Statut |
|---|---|---|---|
| Kambélé / permis de Batouri | Batouri, Est | Sondages d'African Aura Resources avec « visible gold in three drill holes » (article de Northern Miner, non daté, payant) [S15]. Granitoïdes aurifères datés à ~620 Ma [L11]. Site fermé depuis neuf mois selon un article de 2025 [S16] | Ressource conforme : **non trouvée** [?] ; opérateur actuel : **non vérifié** |
| Eastern CLP : Ndom, Pokor, Niambaram, Tenekou | Contigus à Mbe (Adamaoua/Nord) | Prélèvements de roche jusqu'à 17,00 g/t (Ndom), 1,24 g/t (Pokor), 28,40 g/t (Niambaram) ; anomalie de sol PK01 à 120 ppb [S13] | Exploration précoce [F] |
| Bindiba | Lom, Est | Trois corps polarisables par tomographie électrique et polarisation provoquée, près d'un chantier semi-mécanisé [L33] | Recherche académique [F] |
| Tikondi | Est | 550 sols ; Au de 1 à 2 480 ppb [L26] | Recherche académique [F] |
| Dourou Tchaga (SW de Poli) | Nord | Filons laminés dans un cisaillement sénestre ENE–WSW (D3) [L21] | Recherche académique [F] |

### 4.3 Orpaillage et exploitation semi-mécanisée : ampleur documentée

| Indicateur | Valeur | Source | Statut |
|---|---|---|---|
| Production déclarée par SONAMINES | 353,63 kg (2021) ; **859,92 kg (2022)**, soit ~27,45 Md FCFA | ITIE, via Ecomatin (26/03/2025) [S9] | [F] (source secondaire de presse) |
| Répartition 2022 par site | Batouri 37,3 % (332,2 kg) ; Bétaré-Oya 20,29 % ; Ngoura 15,50 % ; ensuite Kette, Meiganga, Mbotoro ; enfin Bombe, Dir, Gari-Gombo, Garoua-Boulaï, Rey-Bouba, Yokadouma | [S9] | [F] |
| Part informelle | « 90 % de la production issue des exploitations artisanales et semi-mécanisées échappe aux circuits formels » (ITIE) | [S9] | [F] |
| Part de l'artisanal dans la production nationale | 95 % | [S1] | [F] |
| Or remis à l'État (taxe ad valorem/synthétique) | 170,9 kg en 2023 ; 420 kg sur 2023 et le 1er semestre 2024 | [S1] | [F] |
| Titres | 122 permis miniers industriels ; plus de 1 000 permis artisanaux et semi-mécanisés | [S1] | [F] |
| Sociétés illégales | ~200 dans l'Est et l'Adamaoua, à plus de 95 % étrangères (Ministère des Mines, mai 2026) | Extraits Arab News / AllAfrica | [F-e] |
| Début de la semi-mécanisation | vers 2004 dans l'Est (artisanat depuis ~1934) | Extrait de l'article [L35] | [F-e] |
| Expansion de Kambélé | Hausse des surfaces minières et habitées de 2016 à 2024 | [L34] (titre vérifié dans Crossref ; chiffres non lus) | [F-e] |

**[I]** Pour la prospectivité, la localisation des chantiers artisanaux est un **indice fort de
présence d'or**, mais elle est biaisée :
- vers l'or alluvial et éluvial ;
- vers les zones accessibles ;
- vers les zones déjà connues.

Ces chantiers ne doivent pas servir de points d'entraînement « primaires » sans tri (§ 6.3).

## 5. Inventaire des données

| Jeu de données | Contenu | Échelle / résolution | Accès et licence | Statut | Limites |
|---|---|---|---|---|---|
| **PRECASEM : cartes géologiques** | « 13 geological maps at 1/200 000 » [S2] (13,5 selon [S4]) | 1/200 000 | **Non vérifié** (pas de portail trouvé) | [F] objectif ; [?] livraison | Couverture limitée aux régions du programme (Adamaoua, Centre, Est, Littoral, Nord-Ouest, Sud-Ouest selon [S2]) |
| **PRECASEM : géochimie** | ~18 000 échantillons **prévus** [S2] ; « interprétation en cours » (mars–avril 2018) [S4] | ? | **Non vérifié** | [F] objectif ; [?] résultats | Nombre réel, milieu échantillonné, éléments dosés et seuils de détection : inconnus |
| **PRECASEM : géophysique aéroportée** | ~160 000 km², six régions ; seuls 40 % des 475 000 km² du pays déjà couverts auparavant [S5] | ? | **Non vérifié** | [F] annonce | Espacement des lignes, capteurs et livrables inconnus |
| **SIGM** | « SIGM architecture proposition », serveur [S4] | — | **Non vérifié** | [F] conception ; [?] mise en ligne | Données jugées « pour la plupart obsolètes » [S1] |
| Aéromagnétisme ancien (années 1970, coopération Canada) | Cartes isomagnétiques utilisées dans des mémoires universitaires | ? | Dépôt DICAMES (mémoires) | [F-e] | Données brutes non localisées |
| **USGS Africa GIS** | Installations, sites d'exploration et de développement, occurrences et gisements, infrastructures [S7] | Points/lignes | **CC0 1.0** ; DOI 10.5066/P97EQWXP [S7] | [F] | Référence 2018 [S8] : n'inclut ni Mbe (découvert après 2021) ni les ressources de Bibemi publiées en 2024–2025 [I] |
| **Littérature scientifique** (§ 12, [L*]) | Occurrences, structures, âges, géochimie locale | Locale (districts) | Articles, souvent payants | [F] | Coordonnées à numériser à partir des figures ; biais vers l'Est |
| **RNS d'Oriole Resources** | Ressources, intersections, anomalies de sols et de sédiments | Licences | Public (AIM) | [F] | Données de société : non indépendantes |
| **ITIE / SONAMINES** | Production par localité (2022) | Localités | Public (rapports ITIE) | [F] via [S9] | Production formelle uniquement (~10 %) |
| Sentinel-2, Landsat 8/9, ASTER | Indices d'altération (argiles, oxydes de fer) | 10–30 m | Libre | [F] (utilisés dans [L17], [L18]) | Inexploitables sous forêt dense et latérite (voir module 01) |
| SRTM / Copernicus DEM, Sentinel-1, Radarsat | Linéaments | 30 m | Libre (Radarsat : selon licence) | [F] (utilisés dans [L17], [L25]) | Linéaments ≠ failles : il faut valider sur le terrain |
| Gravimétrie EGM2008 | Structures profondes | Régionale | Libre | [F] ([L24], [L29]) | Résolution faible pour cibler |
| Cadastre minier (Flexicadastre) | Titres | — | À vérifier (module 03) | [?] | Hors périmètre du module 02 |
| Archives BRGM / PNUD (avant 2000) | Prospection historique | — | **Non trouvé** | [?] | Recherche à faire auprès de la bibliothèque du BRGM et du MINMIDT |
| Carte géologique nationale numérique | Lithologie nationale | ? | **Non vérifié** | [?] | Édition, échelle et format inconnus |

**Conclusion sur les données [I]** :
- sans accès au SIGM ni aux livrables PRECASEM, une carte **nationale** reste qualitative ;
- l'exercice quantitatif (*weights of evidence*) ne se justifie qu'à l'échelle d'un **district**
  où la littérature fournit assez d'occurrences géoréférencées (Bétaré-Oya, Batouri) ;
- la priorité n° 1 avant l'édition pilote est une demande formelle de données au MINMIDT, à
  l'unité PRECASEM et à SONAMINES (§ 11).

## 6. Méthode de prospectivité et validation

### 6.1 Modèle de gîte et système minéral

Cadre de référence : la classification de l'or orogénique ([M1]) et la traduction du « système
minéral » en critères cartographiables ([M2]). Un exemple publié d'application en Afrique (Ahafo,
Ghana) suit le même raisonnement : chemins de fluides, pièges physiques, pièges chimiques ([M6]).

| Composante du système | Critère cartographiable au Cameroun | Justification locale |
|---|---|---|
| Source / fertilité | Granitoïdes syn-tectoniques de type I (~640–600 Ma), oxydés | [L8], [L11], [L31] |
| Chemins (*pathways*) | Proximité des cisaillements d'échelle crustale (CCSZ, Sanaga, Bétaré-Oya, Tcholliré-Banyo) | [L2], [L5], [L6], [L20] |
| Pièges physiques | Structures de 2e ordre NE–SW (type P), ENE et NNE/NNW ; intersections ; contacts granite–gneiss ; dykes felsiques | [L5], [L7], [S12] |
| Pièges chimiques / dépôt | Altérations (séricite, silice, sulfures) ; anomalies Au + As, Sb, W, Bi, Te | [L13], [L14], [L26], [L32] |
| Préservation / détection | Épaisseur de latérite, couvert forestier, sédiments crétacés (fossé de la Bénoué) | [L12], [L24] |

### 6.2 Couches de preuve et pondérations (modèle knowledge-driven) [H]

Les poids ci-dessous sont une **proposition pédagogique** fondée sur les critères du § 6.1. Ils
ne viennent d'aucune source publiée pour le Cameroun. Ils doivent être affichés avant le calcul
(règle du cadrage, point ouvert n° 5) et testés en analyse de sensibilité.

| Couche | Construction | Poids | Raison du poids |
|---|---|---|---|
| E1. Distance aux cisaillements majeurs | Tampons de 0–2 / 2–5 / 5–10 / > 10 km | 0,20 | Contrôle de premier ordre dans tous les districts étudiés |
| E2. Structures de 2e ordre (densité et intersections) | Linéaments MNT/radar/aéromagnétisme ; densité ; nœuds | 0,15 | Contrôle démontré à Bétaré-Oya [L7] et Batouri [L28] ; intersections à Mbe [S12] |
| E3. Contacts granitoïde–encaissant | Tampon autour des contacts | 0,15 | Woumbou–Colomine–Kette [L5] ; Haut-Lom [L10] |
| E4. Géochimie (Au + indicateurs) | Score multi-élément (ACP ou somme de rangs) ; anomalies par fractale C-A | 0,25 | Preuve la plus directe, mais couverture inégale (alimente l'indice de couverture) |
| E5. Géophysique | Gradients et signal analytique aéromagnétiques ; contacts | 0,10 | Cibles à Yopa [L19] et Tcholliré [L20] |
| E6. Altération (télédétection) | Ratios et ACP Landsat/ASTER/Sentinel-2 | 0,05 (savane) / 0 (forêt) | Utile en savane [L17], [L18] ; inopérant sous forêt |
| E7. Bassins versants « en aval d'une source » | Bassins contenant des chantiers alluviaux, pondérés par l'indice de transport des grains s'il est connu | 0,10 | Indice indirect : on localise le bassin, pas la source [L22], [L27] |

Deux variantes de calcul :
- **(a) Indexation pondérée** : somme des poids × scores de classe (0–1).
- **(b) Logique floue** ([M4]) : fonctions d'appartenance continues, par exemple
  μ(distance au cisaillement) = 1 jusqu'à 1 km, puis décroissance linéaire jusqu'à 0 à 10 km
  [H]. On combine ensuite par blocs :
  - chemins (E1, E2) : *fuzzy OR* ;
  - pièges (E3, E5) : *fuzzy OR* ;
  - dépôt (E4, E6, E7) : *fuzzy OR* ;
  - puis **fuzzy gamma** (γ ≈ 0,8–0,9 à tester) entre les trois blocs. Un système minéral exige
    en effet que chemin, piège et dépôt soient présents ensemble.

### 6.3 Modèle data-driven de contrôle : weights of evidence [H sur paramètres ; F sur méthode]

Méthode de Bonham-Carter, Agterberg & Wright ([M3]) :
- pour chaque couche binaire B et les occurrences D, on calcule
  W⁺ = ln[P(B|D)/P(B|¬D)], W⁻ = ln[P(¬B|D)/P(¬B|¬D)] et le contraste C = W⁺ − W⁻ ;
- on retient les classes dont le contraste studentisé (C / s(C)) dépasse ~1,5–2 [H] ;
- la probabilité a posteriori se calcule en log-odds : logit(prior) + Σ W ;
- on vérifie l'**indépendance conditionnelle** entre couches (par exemple E1 et E2 sont
  corrélées) ; à défaut, on fusionne les couches ou on se rabat sur la régression logistique
  ([M7] compare ces variantes).

Paramètres et précautions :
- **Points d'entraînement** : uniquement des occurrences **primaires ou éluviales** géoréférencées
  (filons, puits sur roche en place, sondages). Les chantiers alluviaux sont exclus.
- **Taille de cellule** : ~1 km² à l'échelle nationale ; 100 × 100 m à l'échelle du district
  [H]. Une seule occurrence par cellule.
- **Échelle d'application** : le district seulement (Bétaré-Oya ou Batouri), là où la
  littérature fournit assez de points. À l'échelle nationale, le nombre d'occurrences primaires
  fiables est trop faible et trop groupé [I].

### 6.4 Primaire, éluvial, alluvial : règles de tri [H]

| Type | Critère d'identification | Usage dans le modèle |
|---|---|---|
| Primaire | Filon ou roche en place minéralisée ; sondage ; datation, inclusions fluides | Entraînement et validation |
| Éluvial / colluvial | Puits dans le saprolite ou la latérite sur socle ; grains anguleux ou irréguliers ; inclusions de quartz ou de sulfures | Entraînement (poids réduit) et validation |
| Alluvial | Graviers de cours d'eau ; grains arrondis ou martelés | **Jamais en entraînement.** Sert à construire la couche E7 par bassin versant |
| Inconnu | Chantier sans description | Exclu de l'entraînement ; affiché sur la carte |

### 6.5 Protocole de validation [H, fondé sur M5 et M6]

1. **Retrait spatial plutôt qu'aléatoire.** On découpe la zone en blocs (par exemple 25 × 25 km).
   On retire 25 à 30 % des blocs contenant des occurrences [H]. Motif : les occurrences sont
   groupées [L7].
2. **Test de transfert entre districts.** On calibre sur l'Est (Bétaré-Oya, Batouri,
   Colomine), puis on applique le modèle à l'Adamaoua et au Nord.
3. **Rétro-prédiction de Mbe et de Bibemi.**
   - On construit le modèle **sans** les données publiées par Oriole (anomalies, sondages,
     ressources).
   - On vérifie ensuite si les licences de Mbe et de Bibemi tombent dans les classes High ou
     Medium.
   - Mbe et Bibemi sont les seuls gisements dotés d'une ressource conforme ([S11], [S13]). C'est
     le test le plus proche de la question du module.
4. **Courbes.**
   - Courbe de succès : occurrences d'entraînement captées en fonction du pourcentage de surface
     classée en ordre décroissant de score.
   - Courbe de prédiction : même calcul avec les occurrences retirées ([M5]).
   - Indicateurs : aire sous la courbe ; graphique *prediction-area* ([M6]). Exemple de résultat
     publié : 76 % des occurrences captées dans 24 % de la surface à Ahafo [M6].
5. **Référence nulle.** Une carte aléatoire capte x % des occurrences dans x % de la surface. Un
   modèle utile doit faire nettement mieux sur les occurrences **retirées**.
6. **Sensibilité.**
   - On fait varier chaque poids de ± 50 %, puis on retire une couche à la fois.
   - Une cible qui ne reste High que dans une seule configuration est rétrogradée en Medium [H].

## 7. Déroulé de l'étude de cas

Durée indicative : 5 demi-journées [H].

| Séance | Contenu | Production des participants |
|---|---|---|
| 1. Géologie de l'or au Cameroun | Domaines de la CAFB, cisaillements, âges, débat orogénique / lié aux intrusions (§ 3) ; lecture guidée de [L5] ou [L7] | Tableau « système minéral » (§ 6.1) rempli pour un district |
| 2. Inventaire et tri des données | Couches USGS ([S7]), points numérisés depuis la littérature, ITIE ([S9]), livrable du module 01 ; tri des occurrences (§ 6.4) | Base d'occurrences typée avec source par point ; carte de couverture des données |
| 3. Couches de preuve | Tampons, densité de linéaments, score géochimique, bassins versants | 5 à 7 rasters normalisés de 0 à 1 |
| 4. Modélisation | Indexation pondérée et logique floue au niveau national ; *weights of evidence* sur un district | Deux cartes continues et tableau des poids publié |
| 5. Validation et classement | Retrait de blocs, rétro-prédiction de Mbe et Bibemi, courbes, sensibilité ; classement en 4 classes | Carte livrable + note de 2 pages sur les cibles « à valider » |

**Choix de la zone de district [H]** :
- Bétaré-Oya / Lom : littérature la plus dense ([L6], [L7]) ;
- ou Borongo–Mborguéné : savane, cohérente avec l'exercice spectral du module 01 ([L17]).

**Jeu de secours** (exigence du cadrage) : base d'occurrences et couches préparées par
l'équipe pédagogique, à partir des seules sources publiques du § 12 [H].

**Règles de communication** (reprises du cadrage) :
- on parle de **cibles d'exploration à valider** ;
- on n'emploie jamais « gisement » ou « ressource » pour une zone High.

## 8. Spécification du livrable : Cameroon Gold Prospectivity Map

| Élément | Spécification [H sauf mention] |
|---|---|
| Format | GeoTIFF (score continu et classe) + GeoPackage (occurrences, cibles, couverture) + carte PDF + note méthodologique |
| Projection | WGS 84 (EPSG:4326) pour l'échange ; calculs en UTM (le Cameroun s'étend sur les fuseaux 32N et 33N) ou dans une projection équivalente unique |
| Résolution | National : 1 km. District : 100 m |
| Champs par cellule | `score` (0–1), `classe`, `couverture` (0–1), `n_couches` (nombre de couches présentes), `modele` (indexation / flou / WofE), `version`, `date` |
| **Classes** | **High** : 5 % supérieurs de la surface couverte ET couverture ≥ 0,6. **Medium** : 15 % suivants ET couverture ≥ 0,6. **Low** : reste de la surface ET couverture ≥ 0,6. **Insufficient data** : couverture < 0,6, quel que soit le score. Seuils à ajuster sur la courbe de succès |
| Indice de couverture | Moyenne pondérée de la présence (0/1) des couches E1–E7, pondérée comme le modèle. Par exemple, une cellule sans géochimie ni géophysique plafonne à 0,65 |
| Couche « cibles » | Polygones High contigus de plus de N km², avec identifiant, couches dominantes, distance à l'occurrence primaire connue la plus proche et recommandation de suivi (sols, concentrés, cartographie) |
| Métadonnées obligatoires | Source et date de chaque couche ; tableau des poids ; courbes de succès et de prédiction ; résultat de la rétro-prédiction Mbe/Bibemi ; mention « carte de prospectivité pédagogique — pas une estimation de ressources » |
| Revue | Relecture par un géologue indépendant avant toute diffusion externe (point ouvert n° 2 du cadrage) |

## 9. Sorties vers les autres modules

| Vers | Ce que le module 02 transmet | Format |
|---|---|---|
| **01 Geo-Spatial** (retour) | Les cibles satellitaires du 01 sont confrontées aux occurrences et aux autres couches. Pour chaque cible : confirmée, neutre ou contredite. Le 02 transmet aussi la liste des couches les plus discriminantes (contraste C) pour orienter le traitement d'image | Table `cible_01_id`, `classe_02`, `commentaire` |
| **01 → 02** (entrée) | Linéaments (MNT/radar), indices d'altération (savane), cibles du 01, utilisés comme couches E2 et E6 | Raster et vecteur |
| **03 Mining Ecosystem** | Couche des zones de prospectivité (polygones High/Medium) ; base d'occurrences typée ; liste des projets avec déclaration conforme (§ 4.1) | GeoPackage |
| **07 Investment Pipeline** | Pour le critère « Geology » : classe et score de prospectivité de chaque opportunité. Pour le critère « Resource » : ressources **avec le code** (Mbe 1,66 Moz *Inferred* JORC ; Bibemi ~460 koz *Indicated* + *Inferred* JORC 2012), la mention « exploration target, conceptuel » le cas échéant, ou « aucune ressource conforme » (Kambélé/Batouri) | Fiche par site + table |
| 09 National Strategy | Message de synthèse : le déficit de données géoscientifiques publiques est le premier frein à l'évaluation du potentiel aurifère | Texte |

## 10. Tableau de vérification

| # | Affirmation | Source | Statut |
|---|---|---|---|
| 1 | Campagne PRECASEM 2017 : 6 régions, 13 cartes au 1/200 000, 18 000 échantillons, 30 mois, BRGM–BEIG3–GTK, ~4,5 Md FCFA | [S2] | Vérifié (objectif annoncé) |
| 2 | 300 nouveaux sites miniers (2014–2019) dans l'Est, l'Ouest, le Nord, le Centre et l'Adamaoua | [S3] | Vérifié (annonce) |
| 3 | « 18 000 échantillons, 300 sites » relèvent d'une même campagne du SIGM | Cadrage ; absent de [S1] | **Faux / mal attribué** |
| 4 | Environ 1 800 échantillons (rapport APA de 2019) | camer.be (page en 404) | Non vérifié |
| 5 | Le SIGM a été conçu dans le cadre du PRECASEM | [S4] | Vérifié (conception) |
| 6 | Accès public au SIGM | — | Non vérifié |
| 7 | Données géologiques « pour la plupart obsolètes » (étude AMDC) | [S1] | Vérifié |
| 8 | Levé aéroporté d'environ 160 000 km² ; 40 % du territoire couvert auparavant | [S5] | Vérifié (annonce, non datée) |
| 9 | PRECASEM = projet P122153, crédit IDA de 30 M US$ ; financement additionnel P160917 de 26,9 M US$ | [S6] ; pages World Bank vues en extrait | Titre vérifié ; montants [F-e] |
| 10 | USGS Africa GIS : CC0, DOI 10.5066/P97EQWXP | [S7] | Vérifié |
| 11 | USGS : année de référence 2018 | [S8] | Vérifié |
| 12 | Domaines de la CAFB et chronologie de 650 à 550 Ma | [L1] | Vérifié (résumé) |
| 13 | CCSZ et Sanaga : D2 sénestre puis D3 dextre ; Lom = *pull-apart* | [L2] | Vérifié (résumé) |
| 14 | Woumbou–Colomine–Kette : orogénique mésozonal, ~300 °C, ~2 kbar | [L5] | Vérifié (résumé) |
| 15 | Ceinture du Lom : orogénique mésozonal, ~310 °C, 6–9 km | [L6] | Vérifié (résumé) |
| 16 | Bétaré-Oya : contrôle NE–SW (type P), gîtes groupés | [L7] | Vérifié (résumé) |
| 17 | Granitoïdes de Kambélé à 619 ± 2 et 624 ± 2 Ma | [L11] | Vérifié (résumé) |
| 18 | Minéralisation de Ngoura–Colomines postérieure à ~630 Ma | [L8] | Vérifié (résumé) |
| 19 | Or des sols de Batouri particulaire et résiduel | [L12] | Vérifié (résumé) |
| 20 | Mbe : 50,60 Mt à 1,02 g/t, 1,66 Moz *Inferred* JORC | [S13] (RNS 6596V) | Vérifié |
| 21 | Mbe principalement dans la région de l'Adamaoua | [S12] | Vérifié |
| 22 | Bibemi : 6,96 Mt à 2,06 g/t, ~460 koz (100 koz *Ind.* + 360 koz *Inf.*), JORC 2012 | [S11] | Vérifié |
| 23 | Bibemi : demande de permis non accordée au 22/09/2026 | [S13] | Vérifié (à cette date) |
| 24 | Bibemi : PEA à 89 koz, 2,20 g/t, 10 koz/an, 7 ans, VAN de 12,8 M US$ | [S13], [S14] | Vérifié |
| 25 | Bibemi dans la région du Nord | Extraits Mining Weekly / Ecomatin | [F-e] |
| 26 | Kambélé : ressource conforme | — | Non trouvé |
| 27 | SONAMINES : 859,92 kg en 2022 ; Batouri 37,3 % | [S9] | Vérifié (presse citant l'ITIE) |
| 28 | 90 % de la production artisanale hors circuits formels | [S9] | Vérifié (presse citant l'ITIE) |
| 29 | 95 % de la production nationale est artisanale | [S1] | Vérifié (presse) |
| 30 | ~200 sociétés illégales dans l'Est et l'Adamaoua (mai 2026) | Extraits Arab News / AllAfrica | [F-e] |
| 31 | Gamba : grains d'or à source proche (< 5 km) | [L22] | Vérifié (résumé) |
| 32 | Tcholliré : signature possiblement épithermale | [L23] | Vérifié (résumé) |
| 33 | Poids des couches E1–E7 | — | Hypothèse de conception |

## 11. Inconnues

1. **SIGM** : existence d'un portail public, URL, contenu effectivement chargé, conditions de
   réutilisation (y compris l'usage commercial).
2. **Livrables PRECASEM** : nombre réel d'échantillons géochimiques analysés (18 000 prévus ;
   ~1 800 évoqués sans vérification), éléments dosés, milieu échantillonné, cartes au 1/200 000
   publiées, données aéroportées brutes (espacement, capteurs) et rapport de fin de projet de la
   Banque mondiale.
3. **Carte géologique nationale numérique** : édition, échelle, disponibilité vectorielle.
4. **Archives BRGM / PNUD** et prospection d'avant 2000 : inventaire à faire.
5. **Kambélé/Batouri** : détenteur actuel, existence éventuelle d'une estimation de ressources,
   statut d'exploitation en 2026.
6. **Bibemi** : délivrance du permis d'exploitation après le 22/09/2026.
7. **Coordonnées** des occurrences : la plupart sont à numériser depuis les figures d'articles,
   avec une erreur de position à documenter.
8. **Production artisanale réelle** : seule la production formelle est connue. Les statistiques
   miroirs des importateurs relèvent du module 06.
9. **Nombre d'orpailleurs** et cartographie exhaustive des chantiers : aucune source consultée.
10. **Modèle génétique** : orogénique ou lié aux intrusions, et rôle éventuel de la Ligne
    volcanique du Cameroun au nord. La question reste ouverte dans la littérature.

## 12. Sources

Toutes les URL ci-dessous ont été consultées le 2026-10-08. Pour les articles scientifiques, le
DOI a été contrôlé dans Crossref et le contenu lu dans le résumé (moteur Consensus), sauf mention
contraire. Pour les articles sans DOI confirmé, l'URL est celle de la fiche consultée.

### Sources institutionnelles, presse et sociétés

- [S1] Financial Afrik (10/07/2025), « Au Cameroun, l'urgence d'actualiser le potentiel minier… » — https://www.financialafrik.com/2025/07/10/au-cameroun-lurgence-dactualiser-le-potentiel-minier-pour-ameliorer-les-recettes-etude
- [S2] Business in Cameroon (28/01/2017), « Cameroon launches new prospection campaign of mining sites in six regions » — https://www.businessincameroon.com/mining/2801-6852-cameroon-launches-new-prospection-campaign-of-mining-sites-in-six-regions-of-the-country
- [S3] Business in Cameroon (17/06/2019), « 300 new mining sites discovered in 5 regions in 2014-2019… Precasem » — https://www.businessincameroon.com/index.php/mining/1706-9219-cameroon-300-new-mining-sites-discovered-in-5-regions-in-2014-2019-in-the-framework-of-world-bank-backed-programme-precasem
- [S4] F. Prognon (BRGM), « Generating and accessing geological information », IGF, 2018 (PDF) — https://www.igfmining.org/wp-content/uploads/2018/11/Session-4-_-Geological-Information-_-2.pdf
- [S5] PANA via Africa in Harlem, « Cameroon to conduct aerial geophysical survey » (non daté) — https://africainharlem.nyc/en/cameroon-cameroon-to-conduct-aerial-geophysical-survey-le-cameroun-va-lancer-ce-mois-une-campagne-de-levee-geophysique-aeroportee/
- [S6] Banque mondiale, Cameroon Mining Sector Technical Assistance Project (P122153) — https://projects.worldbank.org/en/projects-operations/project-detail/P122153 ; extraits : https://www.worldbank.org/en/news/loans-credits/2011/12/15/cameroon-mining-sector-capacity-building-project et https://www.worldbank.org/en/news/loans-credits/2017/03/31/cameroon-mining-sector-capacity-building-project-additional-financing
- [S7] USGS (2021), Compilation of Geospatial Data (GIS) for the Mineral Industries and Related Infrastructure of Africa, doi:10.5066/P97EQWXP — https://www.usgs.gov/data/compilation-geospatial-data-gis-mineral-industries-and-related-infrastructure-africa
- [S8] USGS Open-File Report 2024-1041 — https://pubs.usgs.gov/publication/ofr20241041
- [S9] Ecomatin (26/03/2025), « Au Cameroun, la production d'or a doublé depuis l'entrée en scène de la Sonamines (ITIE) » — https://www.ecomatin.net/au-cameroun-la-production-dor-a-double-depuis-lentree-en-scene-de-la-sonamines-itie
- [S10] Ecofin Agency (21/11/2025), « Oriole eyes mid-2026 permit for Cameroon's Bibemi gold project » — https://www.ecofinagency.com/news-industry/2111-50708-oriole-eyes-mid-2026-permit-for-cameroon-s-bibemi-gold-project
- [S11] Oriole Resources, Interim Results (RNS, 23/09/2025) — https://www.investegate.co.uk/announcement/rns/oriole-resources--orr/interim-results/9124477
- [S12] Oriole Resources, « Further Gold Mineralisation at Mbe South Deposit » (RNS, 20/05/2026) — https://www.investegate.co.uk/announcement/rns/oriole-resources--orr/further-gold-mineralisation-at-mbe-south-deposit/9576481
- [S13] Oriole Resources, Interim Results for the six-month period ended 30 June 2026 (RNS 6596V, 22/09/2026), PDF — https://www.directorstalkinterviews.com/wp-content/uploads/2026/09/ORR-News-1.pdf
- [S14] Share Talk (16/12/2025), « Oriole Resources confirms Bibemi gold project potential with preliminary economic assessment » — https://www.share-talk.com/oriole-resources-confirms-bibemi-gold-project-potential-with-preliminary-economic-assessment/
- [S15] Northern Miner, « African Aura finds the glow in Cameroon » (extrait, non daté) — https://northernminer.com/news/african-aura-finds-the-glow-in-cameroon/1000081660
- [S16] Cameroun24, « Batouri en ébullition… » (2025) — https://cameroun24.net/article/69181-Batouri_en_ebullition___colere_populaire_contre_un.html
- Extraits de recherche seulement ([F-e]), à relire : https://www.arabnews.com/node/2643473/ ; https://fr.allafrica.com/stories/202605140542.html ; https://www.miningweekly.com/article/explorer-focuses-on-cameroon-prospects-2024-07-26 ; https://ecomatin.net/oriole-resources-veut-profiter-de-la-flambee-des-cours-pour-lancer-sa-mine-dor-dans-le-nord-cameroun

### Littérature scientifique (contexte et districts)

- [L1] Toteu, de Wit, Penaye et al. (2022), Gondwana Research — https://doi.org/10.1016/j.gr.2022.03.010
- [L2] Ngako, Affaton, Nnange et al. (2003), Journal of African Earth Sciences — https://doi.org/10.1016/s0899-5362(03)00023-x
- [L3] Tchakounté et al. (2017), Precambrian Research (DOI non confirmé) — https://consensus.app/papers/details/db25f5081de953a597adfc69d6d658e0/ ; commentaire : Ngako & Njonfang (2018) — https://doi.org/10.1016/j.precamres.2017.12.004
- [L4] Kankeu et al. (2017), Journal of African Earth Sciences — https://consensus.app/papers/details/a33136eada2450c9a1ea56c1d25a92ce/
- [L5] Azeuda Ndonfack, Xie, Goldfarb et al. (2021), Mineralium Deposita (Woumbou–Colomine–Kette) — https://doi.org/10.1007/s00126-021-01050-7
- [L6] Azeuda Ndonfack, Xie, Goldfarb et al. (2021), Ore Geology Reviews (Lower Lom Belt) — https://doi.org/10.1016/j.oregeorev.2021.104586
- [L7] Nguemhe Fils, Mimba, Nyeck et al. (2020), Natural Resources Research (Bétaré-Oya) — https://doi.org/10.1007/s11053-020-09695-3
- [L8] Takodjou Wambo, Roy, Ganno et al. (2024), Lithos (Ngoura–Colomines) — https://doi.org/10.1016/j.lithos.2024.107553
- [L9] Tchato Tchaptchet et al. (2020), China Geology (Kékem) — https://doi.org/10.31035/cg2020058
- [L10] Fontem, Suh, Ngatcha et al. (2023), SN Applied Sciences (Haut-Lom) — https://doi.org/10.1007/s42452-023-05358-z
- [L11] Asaah, Zoheir, Lehmann et al. (2014, en ligne), International Geology Review (Batouri) — https://doi.org/10.1080/00206814.2014.951003
- [L12] Vishiti, Suh, Lehmann et al. (2015), Journal of African Earth Sciences — https://doi.org/10.1016/j.jafrearsci.2015.07.010
- [L13] Vishiti, Etame, Suh et al. (2019), Episodes — https://doi.org/10.18814/epiiugs/2019/019016
- [L14] Tata, Suh, Vishiti et al. (2018), Geochemistry: Exploration, Environment, Analysis — https://doi.org/10.1144/geea2016-017
- [L15] Vishiti, Suh, Ngatcha et al. (2024), Minerals — https://doi.org/10.3390/min14060567
- [L16] Takodjou Wambo, Ganno, Djonthu Lahe et al. (2018), Journal of African Earth Sciences — https://doi.org/10.1016/j.jafrearsci.2018.03.015
- [L17] Takodjou Wambo, Nomo Negue, Traore et al. (2024), Advances in Space Research (Borongo–Mborguéné) — https://doi.org/10.1016/j.asr.2024.07.026
- [L18] Ousmanou et al. (2023), Heliyon (Bibemi, Landsat 9, logique floue) — https://consensus.app/papers/details/c1e38b431c9d53ff96dfc53e25c6936f/
- [L19] Zanga Essomba et al. (2023), Pure and Applied Geophysics (Yopa, Adamaoua) — https://doi.org/10.1007/s00024-023-03259-1
- [L20] Anaba Fotze, Palai, Bi-Alou et al. (2023), Acta Geophysica (Tcholliré) — https://doi.org/10.1007/s11600-023-01166-6
- [L21] Ngounouno, Negue, Kolb et al. (2022), Journal of African Earth Sciences (SW de Poli) — https://doi.org/10.1016/j.jafrearsci.2022.104579
- [L22] Dong et al. (2021), Ore Geology Reviews (Gamba) — https://consensus.app/papers/details/55303b1137e75327b0dd58548158afbe/
- [L23] Ngatcha et al. (2024), Journal of the Cameroon Academy of Sciences (Tcholliré) — https://consensus.app/papers/details/c093937501195f8d9a67e1b93cb26774/
- [L24] Marcel et al. (2019), Natural Resources Research (gravimétrie, Nord-Centre) — https://consensus.app/papers/details/8b16040547895bb28cd6635389b6bc99/
- [L25] Fils, Mongo, Mimba et al. (2024), Journal of Geovisualization and Spatial Analysis (Eséka–Lolodorf–Bipindi) — https://doi.org/10.1007/s41651-024-00183-3
- [L26] Boroh et al. (2024), Arabian Journal of Geosciences (Tikondi) — https://consensus.app/papers/details/6f9d629040845fe7b83484722ac5d963/
- [L27] Nomo Negue et al. (2021), Arabian Journal of Geosciences (Guiwa-Yangamo) — https://consensus.app/papers/details/1284c71234535fdfa7434fa64a9d447b/
- [L28] Bissegue et al. (2019), Journal of Geographic Information System (Batouri) — https://consensus.app/papers/details/3f958ed181815959ad78e78677bdb0b3/
- [L29] Fomat Tandjong et al. (2026), Results in Earth Sciences (Batouri, gravimétrie) — https://consensus.app/papers/details/c14c53585c905593945c11e6013e2d5e/
- [L30] Ngatcha et al. (2018), revue sur l'or lié aux granitoïdes de l'Est — https://consensus.app/papers/details/16c05e6ecf4759aea0ba58f1968c1d91/
- [L31] Embui et al. (2024), Ore and Energy Resource Geology (chimie des zircons) — https://consensus.app/papers/details/cecbb7696b025b03a24e500899cf02c9/
- [L32] Fontem et al. (2025), International Journal of Geosciences (Gankoumbol–Djouzami–Beka) — https://consensus.app/papers/details/81be10bfd5305a818c1a776a63d0a5d1/
- [L33] Ledoux et al. (2025), International Journal of Geophysics (Bindiba) — https://consensus.app/papers/details/e7fb5518972a5d4d9cf873ea5905350b/
- [L34] Mimba, Fils, Tibang et al. (2026), Discover Geoscience (Kambélé ; titre seul vérifié) — https://doi.org/10.1007/s44288-026-00468-8
- [L35] Kamga, Nguemhe Fils et al. (2019), GeoJournal (occupation du sol, 1987–2017 ; titre vérifié, contenu vu en extrait) — https://doi.org/10.1007/s10708-019-10002-8
- [L-Etutu] Etutu et al. (2022), sols multi-élémentaires de la plaine de Kambélé — https://consensus.app/papers/details/7235ec04eade5a40b0ba797bba164228/

### Méthode

- [M1] Groves, Goldfarb, Gebre-Mariam, Hagemann (1998), « Orogenic gold deposits… », Ore Geology Reviews — https://doi.org/10.1016/S0169-1368(97)00012-7
- [M2] McCuaig, Beresford, Hronsky (2010), « Translating the mineral systems approach into an effective exploration targeting system », Ore Geology Reviews — https://doi.org/10.1016/j.oregeorev.2010.05.008
- [M3] Bonham-Carter, Agterberg, Wright (1990), « Weights of evidence modelling: a new approach to mapping mineral potential », Commission géologique du Canada — https://doi.org/10.4095/128059
- [M4] Porwal, Carranza, Hale (2003), « Knowledge-Driven and Data-Driven Fuzzy Models for Predictive Mineral Potential Mapping », Natural Resources Research — https://doi.org/10.1023/a:1022693220894
- [M5] Chung & Fabbri (2003), « Validation of Spatial Prediction Models for Landslide Hazard Mapping », Natural Hazards — https://doi.org/10.1023/B:NHAZ.0000007172.62651.2b
- [M6] Boadi, Sunder Raju, Wemegah et al. (2022), « Analysing multi-index overlay and fuzzy logic models for lode-gold prospectivity mapping in the Ahafo gold district », Ore Geology Reviews — https://doi.org/10.1016/j.oregeorev.2022.105059
- [M7] Zhang, Agterberg, Cheng et al. (2013), Mathematical Geosciences (comparaison WofE flou et régression logistique) — https://doi.org/10.1007/s11004-013-9496-8
