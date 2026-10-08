# Audit de cohérence — Africa Mineral Insights, édition Cameroun

> Rapport d'audit du 2026-10-08. Périmètre : les modules `docs/cameroon/01` à `09` et le document
> de cadrage `docs/AFRICA_MINERAL_INSIGHTS.md`, **dans l'état où ils se trouvaient à la lecture**
> (d'autres agents peuvent les modifier en parallèle). Aucun module ni le cadrage n'ont été modifiés.
> Aucune recherche web n'a été faite pour ce rapport : chaque valeur citée vient des modules
> eux-mêmes, avec la source qu'ils indiquent. Quand deux modules divergent et qu'aucun ne permet de
> trancher, le rapport le signale par « arbitrage nécessaire : oui » au lieu de choisir.
>
> Abréviations : M01…M09 = modules ; BIC = Business in Cameroon ; RG = Railway Gazette ;
> EN = Engineering News (Reuters).

---

## 1. Synthèse

1. **Les modules sont solides un par un, mais ils ne parlent pas encore d'une même voix.** Chaque
   module a été écrit sur sa propre recherche du 2026-10-08. Les mêmes faits apparaissent donc avec
   des dates d'information, des sources et des statuts de vérification différents. Sur environ
   35 points comparés, **une douzaine sont de vraies contradictions** : deux valeurs incompatibles
   pour la même chose à la même date. Les autres sont des **décalages de date** (un module a une
   information plus récente) ou des **écarts de statut** (le même fait est « vérifié » ici et
   « non vérifié » là).
2. **Les trois contradictions les plus visibles pour un participant** :
   - **Minim-Martap, première cargaison** : cinq formulations différentes. « Fin septembre 2026 »
     (M06), « T4 2026 » (M03), « S1 2026, date retirée » (M08), « reportée sine die depuis le
     24/08/2026 » (M05), « calendrier retiré sans nouvelle date » (M07, M09). L'information la plus
     récente (M07 et M09, AlCircle du 29/09/2026) doit faire foi.
   - **Alucam** : M05 établit la capacité de 100 kt/an et l'importation de l'alumine. M07 et M09
     écrivent pourtant « capacité non indiquée » ou « non vérifiée », et « origine de l'alumine non
     vérifiée ». La part de l'État vaut 93,4 % (M03), 79,68 % (M05) ou « non vérifié » (M07).
   - **Origine de l'alumine** : M05 écrit que la part guinéenne de 2023-2025 est « inconnue ». M06
     donne pourtant les importations 2023 **déclarées par le Cameroun** : Guinée 57 % en valeur,
     puis Irlande, Australie, États-Unis.
3. **Retards de mise à jour entre modules** :
   - le cadastre (fermeture de Landfolio le 03/11/2025, établie par M03) reste « inconnu » dans
     M02, M04, M07 et M09 ;
   - l'inventaire des décrets d'application (8 décrets, lus par M04) est réduit à « cinq décrets »
     dans M07, à « non lus » dans M08 et à « inventaire à faire » dans M09 ;
   - le chiffre « 18 000 échantillons » est vérifié comme objectif 2017 dans M01 et M02, mais
     « non vérifié » dans M03 et M09 ;
   - la suspension ITIE est datée du 29/02/2024 (M03, M04), de « mars 2024 » (M09), et laissée
     « non vérifiée » par M06.
4. **Chaîne pédagogique : quatre ruptures structurelles.**
   - Zones et projections : M01 travaille en Z1 Tcholliré (EPSG:32633), M02 sur Bétaré-Oya ou
     Borongo–Mborguéné (EPSG:4326 ou UTM 32N/33N), M03 en EPSG:32632.
   - Les projets or de M07 (Mbe, Bibemi, Wapouzé) **sont absents de l'inventaire de M03**.
   - Les notes « Market » de M07 ne reprennent pas les scores de la matrice de M06, et les échelles
     de notation diffèrent d'un module à l'autre.
   - M08 renvoie à M07 un « score de finançabilité à intégrer à l'IOS », ce que la règle 3.6 de
     M07 interdit. En revanche, le projet stylisé de M08 (« Bauxite-Nord ») suit bien la
     recommandation de M07 (paramètres de Minim-Martap) : ce lien fonctionne.
5. **Cadrage** : 22 passages à corriger, détaillés en section 4. Les plus importants : le cadastre
   en ligne (hors service), « 18 000 échantillons / 300 sites » (deux chiffres de nature et de date
   différentes, mal attribués à Financial Afrik), l'organisme public (SONAMINES), Alucam (capacité
   existante, aucune raffinerie d'alumine), les décrets (inventaire fait) et la suspension ITIE
   (absente du cadrage).
6. **Homogénéité** : il existe sept systèmes de statut différents, trois formats de source, au
   moins quatre formats de date et deux copies différentes du Code minier (AMLA et FAOLEX). M01 et
   M03 n'ont pas d'avertissement « pas un conseil ». Une convention commune est proposée en
   section 5.

---

## 2. Tableau des contradictions

Légende de la colonne « Cause » : **D** = dates d'information différentes ; **E** = erreur ou
reprise d'une source dépassée ; **A** = ambiguïté (périmètre, unité ou définition différents) ;
**S** = écart de statut de vérification pour un même fait.

### 2.1 Projets

| # | Fait | Valeurs et fichiers (source citée) | Cause | Formulation de référence proposée | Arbitrage nécessaire |
|---|---|---|---|---|---|
| P1 | **Minim-Martap : première cargaison** | M06 §1, §5.2, V21 : « visée fin septembre 2026 », non confirmée (AlCircle, 18/06/2026). M03 §1, §5 n° 8, §10 : « visée au T4 2026 via Douala » (RG, 15/07/2026). M08 §7 : « 1re expédition prévue au S1 2026, date retirée » (BIC, août 2026). M05 §1.3, §3.2 : « reportées sine die (24/08/2026) » (EcoMatin, 24/08/2026). M07 O1 : « calendrier retiré sans nouvelle date (septembre 2026) » (AlCircle, 29/09/2026), avec un objectif antérieur « T3 2026 » (S1). M09 §10 : « plus de date de première expédition » (AlCircle, 29/09/2026) | D (chaque module s'arrête à une source différente) ; E pour M08 (« S1 2026 » ne correspond à aucune autre source) | « Première expédition visée d'abord au T3 2026, fin septembre (AlCircle, 18/06/2026), puis au T4 2026 (Railway Gazette, 15/07/2026). Après la suspension des tirages AFG Bank le 24/08/2026, le calendrier a été retiré sans nouvelle date (EcoMatin, 24/08/2026 ; AlCircle, 29/09/2026). Aucune expédition confirmée au 08/10/2026. » | Non pour la formulation. Oui pour la mention « S1 2026 » de M08 : à vérifier dans BIC (août 2026) ou à supprimer |
| P2 | Minim-Martap : ressources | M05 §1.3, §3.2 : 1 102 Mt à 45,3 % Al₂O₃ (394 mesurées, 502 indiquées, 206 présumées ; DFS du 02/09/2025, MarketScreener). M07 O1 : 1 027 Mt à 45,3 % (382 / 597 / 48 ; ASX, avril 2025), avec une divergence signalée sur l'inclusion de Makan et Ngaoundal | D et A (deux annonces, périmètre peut-être différent) | Réserve **144,0 Mt à 51,2 % Al₂O₃, 1,7 % SiO₂ (JORC 2012, DFS du 02/09/2025)** : concordant partout. Ressource : retenir le chiffre de la DFS de septembre 2025 et préciser le périmètre (Minim-Martap seul, ou avec Makan et Ngaoundal) | **Oui** : annonce ASX de la DFS (02/09/2025) |
| P3 | Minim-Martap : part réservée à la transformation ou au marché local | M05 §3.2 : « convention du 30-07-2024, qui impose une transformation locale d'au moins 15 % » (EcoMatin, 28/07/2025). M07 O1 et V6 : « 30 % de la production de bauxite ou d'alumine à mettre à disposition de l'industrie locale » (EcoMatin, 19/08/2024). M04 : plancher légal de 15 % (art. 40(4)) | A ou E (une source confond peut-être les 15 % légaux et une clause conventionnelle) | « Code 2023 : au moins 15 % (art. 40(4)). Clause de la convention Camalco : 15 % ou 30 % selon la presse ; texte de la convention non public. » | **Oui** (texte de la convention ou communiqué Canyon) |
| P4 | Minim-Martap : capex | M05 : 446 M$ au total, dont 348 M$ pour le rail. M07 : capex Stage 1 de 96 M$, VAN6 835 M$, TRI 29 %. M08 : les deux | A (périmètres différents, sans contradiction) | Toujours écrire « 96 M$ jusqu'à la 1re expédition ; 446 M$ pour le développement par étapes à 10 Mt/an (DFS 09/2025) » | Non |
| P5 | Minim-Martap : coût C1 | M05 : 34,71 $/t humide. M08 §5 : 38,56 USD/dmt (tableau 2 de la DFS), avec une incohérence d'unités signalée | A (t humide ou t sèche) | Citer les deux, avec l'unité | Oui (DFS complète) |
| P6 | Minim-Martap : montant tiré sur la facilité AFG | M07 O1 : environ 57 M$ (A2MP, juillet 2026) contre environ 75 M$ (AlCircle, septembre 2026). M08 §3.1 : environ 75 M$ au 31/07/2026 (BIC) ; 57 M$ non vérifié | D possible | « Environ 75 M$ tirés au 31/07/2026 (BIC) ; A2MP indique environ 57 M$ (date de référence inconnue). » | Oui (communiqué ASX de Canyon) |
| P7 | Camalco : détention | M05 et M07 : « filiale à 100 % de Canyon ». M07 : 10 % gratuits pour l'État et 10 % ouverts aux nationaux selon la convention. M03 : SONAMINES dit avoir intégré « CAMALCO MINING SA » (lien non vérifié) | A (société d'exploration ou société d'exploitation ?) | « Camalco Cameroon SA, filiale de Canyon ; l'État doit détenir 10 % de la société d'exploitation (convention 2024) ; lien avec "CAMALCO MINING SA" (SONAMINES) non établi » | Oui |
| P8 | **Mbalam : statut** | M03 §1, §5 : exportations annoncées pour le T1 2026, non confirmées au 07/04/2026. M07 O3 : idem, et non confirmées au 08/10/2026. M08 : idem. M09 Inconnue 9 : « des sources se contredisent sur 2026 et 2027 » (sans source pour 2027) | D | « Exportations annoncées pour le T1 2026 (BIC, 13/12/2025 ; EcoMatin, 04/12/2025), non confirmées au 08/10/2026 ; projet décrit comme "stalled" (Reuters, 27/07/2026). » | Non (M09 doit citer sa source « 2027 » ou retirer la mention) |
| P9 | Mbalam : sentence CCI d'environ 616 M$ | M03 : « source secondaire, à confirmer » (Discovery Alert, 27/07/2026). M05, M07, M08 : vérifiée sur Reuters via EN (27/07/2026) | S | « Sundance annonce avoir obtenu une sentence CCI d'environ 616 M$ contre le Cameroun (Reuters, 27/07/2026) ; sentence non publiée ; paiement inconnu. » Remplacer Discovery Alert par Reuters dans M03 | Non |
| P10 | Mbalam : titulaire et convention | M03 : « Cameroon Mining Company » (ITIE) ou « Cameroon Mining Corporation » (BIC). M03 n° 12 cite aussi une « Cameroon Mining Corporation » sur un permis Co-Ni (Messok Est). M05 : groupe Coconut Logic. M07 : convention de février 2022 (S11) ou du 05/10/2023 (S12) | A | « Cameroon Mining Company Sarl (CMC), PEMI 00007 du 17/08/2022 (ITIE 2023) ; date de la convention divergente selon la presse » | Oui (date de la convention) |
| P11 | Mbalam : ressources | M05 : réserve de 517 Mt à 62,2 % Fe (2015, Mbalam + Nabeba) et itabirites d'environ 4,05 Gt à 36,3 % (2014). M07 : 775,4 Mt d'hématite à 57,2 % (2012), réserve de 517 Mt, itabirites d'environ 2,3 Gt à 38 % « pour Mbarga » | A (périmètres différents : gisement Mbarga seul ou ensemble du projet) | Statut « historique (JORC, ancien titulaire Sundance) » partout ; toujours préciser le périmètre (Mbarga / Mbalam / Mbalam + Nabeba) | Oui pour les itabirites |
| P12 | Rail Mbalam-Kribi : stade | M03 §6.2 : conditions suspensives à lever, début des travaux inconnu (bougna.net, 14/07/2025). M07 O3 : « en construction selon la presse », coût supérieur à 8 Md$ (Afrik, 07/04/2026) | D | « PPP signé ; comité de suivi installé le 10/07/2025 ; "en construction" selon la presse d'avril 2026, sans confirmation officielle de l'avancement » | Oui (source officielle) |
| P13 | **Kribi-Lobé** | Report à juillet 2027 : concordant (M03, M05, M07, M09). Investissement : M03 « 120 Md FCFA sur environ 420 Md » ; M05 et M07 « 200 M$ sur 700 M$ » (même article EcoMatin du 11/03/2026). Superficie : 138 km² (M03, annexe 30) ou 132 km² (M03, M05 d'après EcoMatin). Teneur du concentré : « > 60 % Fe » (M05) ou « > 62 % Fe » (M07). Date du permis : 01/07/2022 (ITIE) ou 01/07/2024 (BIC, signalé par M03) | A (FCFA ou USD, même source) ; D pour la teneur | « Premières exportations reportées à juillet 2027 ; environ 120 Md FCFA (≈ 200 M$) investis sur environ 420 Md FCFA (≈ 700 M$) (EcoMatin, 11/03/2026) ; PEMI 00006 du 01/07/2022 » | Non pour le report. Oui pour la superficie et la teneur |
| P14 | **Grand Zambi : capacité visée** | M03 §5 et M07 O5 : 6 Mt/an de concentré (EcoMatin, 23/09/2025). M05 §4.2 et M08 §5 : 1,3 Mt/an de concentré (BIC, 17/02/2026, dossier de financement). M07 signale l'incohérence | A ou D (objectif de long terme et première phase financée ?) | « Objectif annoncé à l'inauguration : 6 Mt/an de concentré (2025) ; le financement bancaire de 2026 porte sur 1,3 Mt/an. » Afficher les deux, datées | Oui |
| P15 | Grand Zambi : statut | Inaugurée le 22/09/2025 : concordant. Exportation : « attendue en février 2026 » (M06, Financial Afrik) ; « aucune exportation confirmée » (M03, M07) | D | « Mine inaugurée le 22/09/2025 ; aucune exportation confirmée au 08/10/2026 » | Non |
| P16 | **Nkout : calendrier** | M03 §5 : « démarrage visé début 2027 » (EcoMatin, 06/04/2026). M05 §4.2 : « repoussé au S2 2026 ; différend avec Caisse Capital » (BIC, décembre 2025). M07 W1 : « repoussé au S2 2026 » (EcoMatin, 22/12/2025) | D (M05 et M07 utilisent une source plus ancienne) | « Démarrage visé début 2027 ; convention et permis non signés (EcoMatin, 06/04/2026) » | Non |
| P17 | **Nkamouna : retrait du permis** | M03 : décret n° 2025/040 du 12/02/2025. M07 V15 : 12/02/2025, mais « une autre source donne le 25/02/2025 » | A | « Décret n° 2025/040 du 12/02/2025 (date à confirmer au Journal officiel) » | Oui (JO) |
| P18 | Nkamouna : ressources | M03 : ressources mesurées et indiquées d'environ 121 Mt à 0,23 % Co, 0,65 % Ni, 1,35 % Mn (BIC). M07 : réserves historiques NI 43-101 de 68,1 Mt à 0,26 % Co (BFS 2011), ressource historique de 323 Mt ; SONAMINES : plus de 100 Mt et environ 226 Mt sans code | A (catégories et dates différentes) | Retenir la classification de M07 (« historique NI 43-101, 2011 ») ; ne pas citer le chiffre BIC sans sa catégorie ni son code | Oui (pièce SEC Geovic 2011) |
| P19 | Nkamouna : appel à partenaires | Infructueux le 18/08/2026 : concordant (M03, M07, M09) ; lancé en janvier 2026 (M07, M09) | — | Concordant | Non |
| P20 | **Akonolinga** | M03 : « retrait d'Eramet en octobre 2023 : non vérifié ». M07 : sortie d'Eramet le 26/10/2023 (BIC, 30/10/2023), reprise par SONAMINES en mai 2025, filiale dissoute le 06/01/2026 | S | Reprendre M07 | Non |
| P21 | Colomine (Codias) : production | M03 : environ 54,5 kg entre 02/2023 et 12/2025 (EcoMatin, 30/06/2026). M07 O9 : 16,7 kg, « année couverte incertaine » (BIC, fin 2025) | D et A (périodes différentes) | « Environ 54,5 kg de 02/2023 à 12/2025 (EcoMatin, 30/06/2026), pour 500 kg/an prévus par la convention » | Non |
| P22 | Mborguéné (Caminco) | M03 : permis « partiellement vérifié » (résumé non ouvert). M07 : permis du 18/08/2025, vérifié (EcoMatin et Financial Afrik, août 2025) | S | Reprendre M07 | Non |
| P23 | Bibemi : étude économique | M02 §4.1 : PEA interne de décembre 2025 (environ 89 koz in situ, 10 koz/an sur 7 ans, VAN de 12,8 M$ à 3 200 $/oz) [S13, S14]. M07 O8 : « capex non publié (pas de PEA/PFS publiée) », d'où E = 1 (ND) | E (M07 n'a pas vu le RNS) | « PEA interne (décembre 2025), résumée dans le RNS du 22/09/2026 ; pas d'étude publiée en intégralité » ; revoir la note E de O8 (M07 §5.3 indique que E = 3 la ferait passer à 63) | Non (la source primaire est déjà dans M02) |
| P24 | Kambélé (Batouri) | M02 §4.2 : opérateur actuel « non vérifié », site fermé depuis neuf mois (2025). M07 X2 : arrêté du 13/08/2025 interdisant l'exploitation industrielle, zone réservée aux artisans | D (lacune de M02) | Reprendre M07 dans M02 | Non |
| P25 | Clinker de Figuil | M06 §4.4 : usine Cimencam de 1 000 t/jour, démarrage en mars 2024 (non vérifié, résultats de recherche). M07 O10 : 500 000 t/an, inaugurée le 12/06/2025 (EcoMatin, Financial Afrik 17/06/2025 ; l'URL EcoMatin dit « 1000 tonnes/jour ») | E ou A (1 000 t/jour ≈ 365 kt/an, pas 500 kt/an) | « Première usine de clinker du Cameroun à Figuil, inaugurée le 12/06/2025 ; capacité annoncée de 1 000 t/jour (EcoMatin) ou 500 kt/an (Financial Afrik) » | Oui |

### 2.2 Alucam et aluminium

| # | Fait | Valeurs et fichiers (source citée) | Cause | Formulation de référence proposée | Arbitrage nécessaire |
|---|---|---|---|---|---|
| A1 | **Capacité d'Edéa** | M05 : 100 kt/an nominaux, **vérifié** (USGS MYB 2017-18 ; ASI 2024 ; Wood Mackenzie) ; valeurs isolées écartées : 50 kt (Climate TRACE), 290 000 t (Daba Finance). M09 C3 et §10 : 100 kt/an « selon des listes secondaires », non vérifié en source primaire. M07 O2 : « capacité nominale non indiquée [?] » ; Inconnue 15. M03 : « non vérifié » | S | « Capacité nominale de 100 kt/an (USGS MYB 2017-18 ; ASI) » | Non |
| A2 | **Production d'Alucam** | M05 : 73 759 t (2017), 34 431 t (2021), 59 540 t (2022), −35 % de 2023 à 2024 (EcoMatin, 30/01/2026) ; −40,8 % au T1 2025 (Ecofin). M07 : 53 675 t en 2025 (Chambre des comptes via BIC, 14/07/2026). M06 : **exportations** de 43 916 t (2023) et 26 851 t (2024, −38,9 %) (INS) | A (production et exportations mélangées) ; D | Série unique : « Production : 73 759 t (2017) ; 34 431 t (2021) ; 59 540 t (2022) ; 2023-2024 : seulement des variations publiées ; 53 675 t (2025). Exportations de lingots : 43 916 t (2023) ; 26 851 t (2024). » | Oui pour la production 2023-2024 en tonnes |
| A3 | **Part de l'État dans Alucam** | M03 : 93,4 % (USGS 2018). M05 : État 79,68 %, SNI 14,32 %, AFD 5,05 % (Ecofin, 31/10/2025), contre État 93,3 % et AFD 5,6 % selon l'ASI. M07 : « non vérifié » ; conversion de 92,5 Md FCFA de créances en capital (BIC, 14/07/2026) | D et A (93 % = État + SNI ? La conversion de 2026 a pu changer la répartition) | « État majoritaire (direct et via la SNI ; environ 94 % à eux deux selon Ecofin 2025) ; répartition après la conversion de créances de 2026 inconnue » | **Oui** |
| A4 | **Origine de l'alumine** | M05 : importée ; Guinée majoritaire en 2021-2022 (déclarations du Cameroun) ; pour 2023-2025, données miroirs seulement (Irlande, Pays-Bas, Jamaïque), donc « part guinéenne inconnue ». M06 §4.4 : importations 2023 **déclarées par le Cameroun** de 135 347 t ; Guinée 34,3 M$ (76,7 kt, 57 % en valeur), Irlande 9,9 M$, Australie 9,3 M$, États-Unis 5,9 M$ ; INS 2024 : 134 119 t. M07 et M09 : origine « non vérifiée » | E (M05 n'a pas interrogé la déclaration camerounaise de 2023) ; S pour M07 et M09 | « Alumine entièrement importée ; aucune raffinerie au Cameroun. 2023 (Comtrade, déclarant Cameroun) : 135 kt, dont 57 % en valeur de Guinée, puis Irlande, Australie, États-Unis. 2024 (INS) : 134 kt. » | Non (refaire la requête Comtrade utilisée par M06 pour confirmer) |
| A5 | Électricité d'Alucam | M05 : forfait d'environ 130 MW depuis 2020. M07 : environ 130 MW, environ 13 % de la production nationale | — | Concordant | Non |
| A6 | Réhabilitation et reprise | M05 : réhabilitation à plus de 40 Md FCFA (EcoMatin, 01/2026) ; Eagle Eye : 70 % pour 475 M$. M07 : injection de 30 à 45 Md FCFA (Chambre des comptes) ; Bathco : 80 % pour plus de 78 Md FCFA ; Naxya : 100 Md FCFA | D et A (sources différentes, non contradictoires) | Afficher les montants avec leur source et leur date | Non |
| A7 | Part de l'UE dans les ventes 2023 | M05 §7 : 94 % de la valeur, France 36,1 % du volume. M06 : 94,5 % (quatre pays de l'UE, calcul Comtrade) ; France 16 071 t sur 43 916 t, soit 36,6 % | A (arrondis et sources différents) | « Environ 94 % vers l'UE (INS ; 94,5 % selon Comtrade) » | Non |

### 2.3 Gouvernance, institutions, cadre légal

| # | Fait | Valeurs et fichiers (source citée) | Cause | Formulation de référence proposée | Arbitrage nécessaire |
|---|---|---|---|---|---|
| G1 | **Suspension ITIE : date** | M03 et M04 : décision du Conseil 2024-17 du **29/02/2024** (api.eiti.org). M09 §1 et C6 : « depuis mars 2024 », « annoncée le 1/03/2024 » (BIC, 01/03/2024). M06 V28 : « non vérifié (lecture automatique ambiguë) » | A (date de la décision ou de l'annonce) ; S pour M06 | « Suspendu par la décision 2024-17 du Conseil d'administration de l'ITIE du 29/02/2024 (annoncée le 01/03/2024) ; score de 53 ; exigence 1.3 ; prochaine Validation à partir du 01/04/2027 » | Non |
| G2 | Rapport ITIE 2023 : date de publication | M03, M06 : décembre 2025. M09 : BIC du 12/12/2025. M04 Inconnue 9 : « rapport pays publié le 30 décembre 2025, contenu non analysé ». M07 V23 : rapport non consulté directement | A | « Rapport ITIE 2023 publié en décembre 2025 (eiti.org/document/25588) » ; M04 et M07 peuvent renvoyer à M03 et M06, qui l'ont lu | Non |
| G3 | **SONAMINES : nom et rôle** | M03, M04 : SONAMINES S.A., décret 2020/749 du 14/12/2020 (statuts : décret 2020/750) ; capital de 10 Md FCFA ; « SOCAMINES » ne figure dans aucune source. Exclusivité de l'achat et de la commercialisation de l'or et du diamant (art. 4(3)). M04 relève la tension avec les comptoirs privés agréés (décret 05251). M09 : réforme de juillet 2026, « SONAMINES assure la commercialisation, le MINMIDT garde la régulation ». M08 : vise 35 % des projets (mai 2026) | — (concordant) ; A sur l'exclusivité face aux comptoirs | « SONAMINES S.A. (Société Nationale des Mines), organisme public dûment mandaté au sens du Code 2023 (désigné par les décrets 2024/05061 et 05062) ; exclusivité légale de l'achat et de la commercialisation de l'or et du diamant (art. 4(3)), à concilier avec les comptoirs agréés du décret 2024/05251 » | Non (sauf l'avis juridique sur la tension, M04) |
| G4 | **Décrets d'application du Code 2023** | M04 : **8 décrets** des 18 et 19/11/2024 (05061, 05062, 05248, 05249, 05250, 05251, 05252, 05253), copies certifiées lues ; plus un arrêté du 09/06/2025 et des décrets du 25/06/2025 (rapportés). M07 C11 et V27 : « cinq décrets (05062, 05248, 05249, 05252, 05253) » (Chambers). M08 C8 : « listés par l'USGS, non lus ». M09 : « inventaire complet [?] », indicateur « inventaire à faire (module 04) » ; arrêté du 15/04/2026 sur les échantillons | S et E (M07 reprend une liste partielle) | Reprendre l'inventaire de M04, en ajoutant l'arrêté du 15/04/2026 signalé par M09 | Non |
| G5 | **Art. 47 : part supplémentaire de l'État** | M04 : +10 % (petite mine) ou +25 % (industrielle), « à titre onéreux et d'accord parties » (art. 47(4)). M09 : « à titre onéreux ». M08 C3 : « le texte lu ne précise pas si cette part supplémentaire est payante » ; numérotation « Section 59 » dans la DFS de Canyon | E ou A (lecture différente, ou copie différente du texte : AMLA ou FAOLEX) | « Option de +25 % (industrielle) ou +10 % (petite mine), à titre onéreux et d'accord parties (art. 47(4), version AMLA) » | Oui, seulement pour la numérotation (Journal officiel) |
| G6 | Taux du Code minier | Ad valorem 8 / 5 / 3 / 2 / 10 % (art. 132) ; 10 % gratuits non diluables ; partage de production 1-5 % (précieux) et 2-15 % (autres) (art. 48) ; transformation locale ≥ 15 % (art. 40(4)) ; stabilité jusqu'à un TRI de 15 %, 15 ans au plus (art. 149) ; capacités locales 0,5-1 % (art. 193) : **concordant** dans M04, M08 et M09 | — | Concordant. Signaler seulement que M07 cite des paramètres **conventionnels** propres à chaque projet (partage de production de 5 % et taxe à l'export de 2 % pour Minim-Martap ; 3 % de production, 1 % SONAMINES, 5 % ad valorem et 5 % à l'export pour Mborguéné), et M06 une taxe à l'export de l'or de 3,75 % (ITIE) que M04 ne mentionne pas | Oui pour les taxes à l'exportation (base légale : CGI ou loi de finances) |
| G7 | **Cadastre minier** | M03 : portail Landfolio (ex-Flexicadastre) **hors service depuis le 03/11/2025** (page de maintenance) ; republication interdite ; aucun export ouvert (ITIE 2023). M04 C4 et Inconnue 5 : « état en ligne actuel inconnu » (budget épuisé). M07 C9 : « en cours d'établissement et d'opérationnalisation » (Chambers, 27/01/2026), aucune URL trouvée. M02 et M09 : statut non vérifié | D et S | « Le portail public Landfolio du MINMIDT est hors service depuis le 03/11/2025 ; aucun remplaçant public identifié au 08/10/2026 ; titres disponibles : situation au 31/12/2023 (Rapport ITIE 2023, annexe 30, sans coordonnées) » | Non |
| G8 | Accès aux titres pour la carte | M03 : 261 titres actifs au 31/12/2023 ; 66 permis de recherche d'or. M07 et M08 : 53 permis de recherche d'or retirés le 30/06/2026 (Financial Afrik ; Trésor) | D | Afficher les deux, datés | Non |
| G9 | **Règles de change BEAC** | M04 : rapatriement de 35 % aujourd'hui, 50 % au 01/01/2027, 70 % au 01/01/2028 (Instruction 001/GR/2026 du 23/04/2026) ; fonds RES exclus ; aucune convention de séquestre au 30/04/2026 ; sanction de 150 % « non vérifiée ». M08 : mêmes taux, mais parle de **« taux de rétrocession »** (35 % contre 70 % pour les autres agents) ; exemption des prêts adossés aux ressources ; sanction jusqu'à 150 % (presse) ; règlement 2018 en vigueur le 01/03/2019 | A (terminologie : « rapatriement » ou « rétrocession », deux notions distinctes du droit des changes CEMAC) ; S (150 %) | « Instruction BEAC n° 001/GR/2026 du 23/04/2026 (rapportée par DG Trésor et droitmediasfinance) : obligation des entreprises extractives portée de 35 % à 50 % au 01/01/2027, puis à 70 % au 01/01/2028 ; fonds RES exclus. » Utiliser le terme exact de l'instruction partout. Sanction de 150 % : « rapportée, non vérifiée » | **Oui** (texte de l'instruction et du règlement 01/2021) |
| G10 | Règlement extractif de 2021 | M04 : « Règlement n° 01/CEMAC/UMAC/CM du 23/12/2021 », plus un règlement n° 02 du même jour. M08 : numérotation « 01/CEMAC/UMAC/CM » ou « 01/21 », non vérifiée | A | « Règlement n° 01/CEMAC/UMAC/CM du 23/12/2021 (numérotation à confirmer sur le texte officiel) » | Oui |
| G11 | « 18 000 échantillons / 300 sites » | M01 C4 et M02 C1 : deux chiffres différents, **vérifiés**. 18 000 = objectif annoncé en janvier 2017 (BIC, 28/01/2017) ; 300 = bilan de 2014-2019 annoncé en juin 2019 (BIC, 17/06/2019). M03 C11 et M09 C7 : « 18 000 échantillons non vérifié » | S (M03 et M09 n'ont pas consulté BIC 2017) | Reprendre M02 C1 : « Programme PRECASEM : campagne géochimique **prévue** d'environ 18 000 échantillons (annonce de 2017) ; 300 "nouveaux sites miniers" annoncés en 2019 pour 2014-2019 ; nombre d'échantillons réellement analysés non vérifié » | Non |
| G12 | Étude AMDC (SIGM « obsolète ») | Cadrage, M01, M02, M03 : Financial Afrik du 10/07/2025. M09 : BIC du 09/07/2025 (même étude) | — | Concordant ; citer les deux articles | Non |

### 2.4 Or

| # | Fait | Valeurs et fichiers (source citée) | Cause | Formulation de référence proposée | Arbitrage nécessaire |
|---|---|---|---|---|---|
| O1 | Production d'or | M02 : SONAMINES, 353,63 kg (2021) et 859,92 kg (2022) (ITIE via Ecomatin, 26/03/2025). M03, M06 : 952,77 kg en 2023 (Rapport ITIE 2023, tableau 7). M07, M09 : 953 kg (presse) | D (années différentes) ; S (presse ou rapport) | Série : « 353,63 kg (2021) ; 859,92 kg (2022) ; 952,77 kg (2023), production artisanale et semi-mécanisée formelle (ITIE) » | Non |
| O2 | **Production industrielle en 2023** | M03 §4 : « Pas de production minière industrielle » (ITIE 2023, tableau 7). M06 §6.2 : selon l'ITIE, « environ 1 t de production artisanale formelle et environ 30 kg de production industrielle ne figurent dans aucun flux d'exportation formel » | A ou E (lecture de deux passages différents du même rapport ; Colomine, petite mine semi-mécanisée, compte-t-elle comme « industrielle » ?) | À trancher par lecture du rapport (tableau 7 et p. 145-146) | **Oui** |
| O3 | Exportations officielles | M06 : 32,7 kg (2020), 73,0 kg (2021), 47,9 kg (2022), 22,31 kg (2023) (DGD/ITIE) ; 175,8 kg sur 2020-2023. M04 §4.10 : **1,897 t sur 2021-2025** (chiffres gouvernementaux, BIC 28/07/2026) | A ou E (sur 2021-2023, l'ITIE donne 143 kg ; il faudrait environ 1,75 t en 2024-2025, ce qui n'est documenté nulle part ; périmètre peut-être différent) | Ne pas additionner ni comparer ces séries sans explication : « ITIE/DGD : 22,31 kg en 2023. Le gouvernement annonce 1,897 t d'exportations officielles sur 2021-2025 (BIC, 28/07/2026) : périmètre et années non détaillés » | **Oui** |
| O4 | **Écart miroir 2023** | M06 : 15 195 kg déclarés par les partenaires (Comtrade) ; ITIE : 15 194 kg et 951 M$ ; EAU 14 048 kg (92 %), Ouganda 1 145 kg ; ratio de 681. M03 : 15,2 t, « environ 90 % aux EAU » (RFI). M09 : « plus de 15 t », « essentiellement vers les Émirats ». M07 : 15 194 kg. Presse : « les EAU seuls > 15 t » (BIC, 15/12/2025), inexact selon M06 | A (arrondis) ; E dans la presse | « En 2023 : 22,31 kg exportés officiellement (DGD/ITIE), contre 15,19 t déclarées importées par les partenaires (Comtrade, repris par l'ITIE), dont 14,05 t par les EAU (92 %) et 1,14 t par l'Ouganda ; rapport d'environ 680. » | Non |
| O5 | Exportations « probables » et pertes fiscales | M04 : exportations probables de 46,219 t sur 2021-2025 ; manque à gagner de 577,51 Md FCFA (gouvernement, BIC 28/07/2026). M06 et M09 : pertes fiscales potentielles d'environ 165 Md FCFA (ITIE 2023). M09 : « autres estimations : 560 et 900 Md » | A (périodes et méthodes différentes) | Toujours donner la période et l'auteur : « 165 Md FCFA (ITIE, rapport 2023) ; 577,51 Md FCFA sur 2021-2025 (gouvernement, 15/07/2026) » | Non |
| O6 | Or remis à l'État | M02, M09 : 170,9 kg en 2023 (Financial Afrik ; presse citant l'ITIE) | — | Concordant | Non |
| O7 | Suisse comme destination | M06 : aucune importation suisse d'or du Cameroun dans Comtrade (2020-2024) | — | Pas de contradiction, mais ne pas citer la Suisse comme exemple d'écart miroir | Non |
| O8 | Ressources JORC (or) | Mbe : 50,60 Mt à 1,02 g/t = 1,66 Moz présumées (M02 : RNS du 22/09/2026 ; M07 : RNS du 23/07/2026). Bibemi : 6,96 Mt à 2,06 g/t ≈ 460 koz, dont 100 koz indiquées (M02 ; M07). **Concordant** | — | Concordant. Ajouter dans M07 la personne compétente et la date pour Bibemi (mai 2025, M02) | Non |

### 2.5 Prix et données de marché

| # | Fait | Valeurs et fichiers (source citée) | Cause | Formulation de référence proposée | Arbitrage nécessaire |
|---|---|---|---|---|---|
| X1 | Prix de référence de septembre 2026 | Pink Sheet du 02/10/2026 : aluminium 3 283 $/t, minerai de fer 97,7 $/t, or 4 319 $/oz (M05, M06) ; « environ 3 280 » dans le résumé de M05 | — | Concordant ; une seule table de prix commune, datée | Non |
| X2 | Bauxite et alumine | M05 : bauxite à 67,61 $/t CIF Chine (SMM, 25/05/2026), 63 $/t (Platts, 15/01/2026) ; alumine à 306,91 $/t FOB Australie (moyenne T1 2026) et 346 $/t (septembre 2026). M06 : bauxite à 31 $/t et alumine à 595 $/t (USGS, f.a.s. des importations américaines, 2025). M08 : 78 $/t CIF (DFS) ; 78-86 $/t (CM Group, août 2026) | A (bases de prix différentes : CIF Chine, FOB Australie, f.a.s. États-Unis) | Toujours préciser la base et la date ; ne pas comparer 31 $/t f.a.s. et 67 $/t CIF | Non |
| X3 | Taux de change utilisés | M05 : parité de 655,957 FCFA/€. M08 : 1,15 €/$ (≈ 570 FCFA/$), et « 82 Md FCFA ≈ 140 M USD » (≈ 586 FCFA/$). M06 : aucune conversion | A | Fixer un taux de référence commun, daté et sourcé, ou n'utiliser que les montants des sources | Non |
| X4 | Nachtigal | M03 : dernier groupe le 18/03/2025 (Wikipédia). M05 : groupe 6 le 14/01/2025 (EDF), « pleinement en service depuis environ février-mars 2025 » | A | « 420 MW, pleinement en service au T1 2025 » | Non |

---

## 3. Ruptures de la chaîne pédagogique

### 3.1 01 → 02 (géospatial → prospectivité)

| # | Rupture | Fichiers | Correction proposée |
|---|---|---|---|
| R1 | **Zones différentes.** M01 retient Z1 Tcholliré–Rey Bouba (Nord) comme zone principale, Z2 Bétaré-Oya, Z3 Batouri. M02 propose comme district Bétaré-Oya/Lom **ou Borongo–Mborguéné**, « cohérente avec l'exercice spectral du module 01 » alors que Borongo–Mborguéné n'est pas une zone de M01. Le test phare de M02 (rétro-prédiction de Mbe et Bibemi) se fait hors des zones de M01 | M01 §4 ; M02 §7 | Aligner : district M02 = Z2 Bétaré-Oya (commune aux deux modules), ou Z1 Tcholliré (où M02 cite déjà [L20], [L23]) ; supprimer la mention erronée de Borongo–Mborguéné comme zone du M01 |
| R2 | **Systèmes de coordonnées différents** : EPSG:32633 (M01), EPSG:4326 pour l'échange et UTM 32N/33N pour les calculs (M02), EPSG:32632 (M03) | M01 §6.1 ; M02 §8 ; M03 §7 | Une convention commune : stockage en EPSG:4326, calcul en EPSG:32633 pour l'Est et le Nord (fuseau 33N) |
| R3 | **Classes de confiance incompatibles** : A/B/C/D (M01, « à valider avec le module 02 ») contre High/Medium/Low/Insufficient avec indice de couverture (M02). Aucune table de passage | M01 §6.3 ; M02 §8 | Table de passage (par exemple B → contribue à E6 ; D → couverture de 0) |
| R4 | **Protocoles de validation contradictoires** : M01 met de côté « environ 30 % des occurrences primaires » de façon aléatoire. M02 exige un retrait par **blocs spatiaux ou par districts**, parce qu'un retrait aléatoire gonfle la performance. Le champ `jeu` transmis par M01 sera donc biaisé pour M02 | M01 §5 étape 6 ; M02 C5, §6.5 | Faire appliquer en M01 le découpage par blocs de M02 |
| R5 | Nommage des fichiers différent (`AMI_CM_M01_<zone>_<groupe>_<date>.gpkg` contre GeoTIFF + GeoPackage sans convention) | M01 §6.1 ; M02 §8 | Convention de nommage commune `AMI_CM_Mxx_...` |

### 3.2 01, 02 → 03 (écosystème)

| # | Rupture | Fichiers | Correction proposée |
|---|---|---|---|
| R6 | M01 et M02 envoient à M03 des occurrences corrigées, les polygones de prospectivité et la liste des projets conformes (Mbe, Bibemi). **M03 n'importe ni l'un ni l'autre** : son déroulé (§7) part de l'USGS et de l'ITIE, et la ligne « 01/02 » de sa section Sorties est un **retour** vers 01/02 | M01 §7 ; M02 §9 ; M03 §7, §9 | Ajouter dans M03 une étape « import des couches 01 et 02 » |
| R7 | **Projets or absents de l'inventaire de M03** : Mbe, Bibemi (Oriole/BCM), Wapouzé (calcaire, Oriole) et Kambélé n'apparaissent pas au §5 de M03, alors qu'ils figurent dans M02 et dans M07 (O8, O10, X2) | M03 §5 ; M07 §4 | Ajouter ces 4 lignes dans `projets_2026` |

### 3.3 03 → 04 et 03 → 05

| # | Rupture | Fichiers | Correction proposée |
|---|---|---|---|
| R8 | M03 transmet à M04 la table `titres_2023` (régime de 2001, 2016 ou 2023 ; participation attendue « 10 % gratuite selon le Code 2016 »). M04 ne l'utilise pas : sa matrice est générale, et il garde le cadastre « inconnu » | M03 §9 ; M04 §2 C4, §10 | M04 reprend le constat de M03 sur le cadastre et ajoute un exercice sur 2 ou 3 titres réels de la table 03 |
| R9 | **Dépendance inversée** : la séance 3 de M04 calcule la part de l'État « sur le projet stylisé du module 08 », alors que M08 vient après M04 dans le parcours (le cadrage enseigne 04, 05 et 06 en parallèle, puis 07, 08, 09) | M04 §7 ; cadrage, Dépendances | Fournir à M04 une fiche de paramètres minimale (celle de M08 §5) dans son jeu de secours, ou déplacer l'exercice en M08 |
| R10 | M03 transmet à M05 « Alucam (2018, statut actuel non vérifié) » et « projet d'alumine annoncé pour 2027 (non vérifié) ». M05 établit au contraire 100 kt/an, l'arrêt partiel des cuves en 2025 et une étude de raffinerie attendue au T3 2026 pour plus de 2 Md$. M05 C5 dit lui-même que le livrable 03 est insuffisant | M03 §9 ; M05 §2 C5 | Retour de M05 vers M03 (mise à jour des lignes Alucam, raffinerie et Proalu) |

### 3.4 05 → 06

| # | Rupture | Fichiers | Correction proposée |
|---|---|---|---|
| R11 | **Liste de produits non reprise en entier** : M05 transmet 2606, 2818.20, 7601, 7606, 7614, 2601, 7203, 7207, 7214. M06 bâtit des matrices pour 7601, 7108, 2606, 2601 et 2523, mais **aucune pour les câbles (7614), le DRI/HBI (7203), les billettes (7207), le fer à béton (7214)** ni l'alumine comme produit à vendre. Il traite l'or et le ciment, que M05 ne couvre pas | M05 §7 ; M06 §5, §7 | Ajouter au moins des fiches courtes 7606, 7614 et 7214 (débouchés régionaux de l'aval, cités par M05 et M09) |
| R12 | **Flux d'alumine contradictoires** (voir A4) : Guinée, Irlande, Jamaïque, Pays-Bas (M05) contre Guinée, Irlande, Australie, États-Unis (M06) | M05 §7 ; M06 §4.4 | Une seule table Comtrade, datée et partagée |
| R13 | **M06 C7 et V30 sont obsolètes** : ils affirment que les sections 04 et 05 sont absentes du cadrage. Elles y figurent (lignes 125 à 169 du cadrage actuel) | M06 §2, §10 | Supprimer C7 et V30 |

### 3.5 02 à 06 → 07

| # | Rupture | Fichiers | Correction proposée |
|---|---|---|---|
| R14 | **Les notes « Market » de M07 ne reprennent pas M06.** M06 transmet : bauxite → Chine 3,15 ; fer → Chine 2,85 ; aluminium → UE 4,2 ; ciment local 3,9 (échelle 1-5). M07 note pourtant M = 3 pour O1 bauxite ; M = 3 pour Lobé et Grand Zambi, mais **M = 4 pour Mbalam** (même produit) ; M = 3 pour Alucam (Élevée dans M06) ; M = 5 pour l'or, alors que M06 conclut que le problème de l'or est la formalisation, pas le marché. Aucune règle de conversion n'existe entre l'échelle de M06 (1-5 avec classes) et celle de M07 (0-5) | M06 §9 ; M07 §3.3, §5.1 | Règle de conversion explicite (par exemple note M07 = arrondi de la note M06), et note identique pour un même produit |
| R15 | M06 ne couvre ni le cobalt, ni le nickel, ni le manganèse, ni le rutile (O6, O7 de M07) ; M05 non plus. M07 C8 le reconnaît | M06 ; M07 C8 | Jeu de secours « marché » pour ces substances, ou mention ND assumée |
| R16 | M02 transmet une classe de prospectivité par opportunité pour le critère « Geology » de M07. M07 n'utilise pas de sortie cartographique de M02 et note G à partir des communiqués. M02 transmet aussi la PEA de Bibemi, absente de M07 (P23) | M02 §9 ; M07 O8 | M07 reprend la PEA et cite la classe M02 de Mbe et Bibemi |
| R17 | M03 transmet `projets_access` (distances au port, au rail, à l'électricité) pour le critère « Infrastructure ». Les notes I de M07 ne citent aucune distance | M03 §9 ; M07 §5.1 | Ajouter la distance au port d'export dans chaque fiche |
| R18 | M04 transmet une « note globale investment-ready » et des drapeaux par substance ; M07 note « Regulation » d'après le titre seul et ne cite pas la grille 0-3 de M04 | M04 §8 ; M07 §3 | Mentionner que Reg = statut du titre (M03/M04) + drapeaux M04 |
| R19 | M01 transmet une fiche des cibles de classe B pour « Geology : cible télédétection non vérifiée ». M07 n'a aucune opportunité de ce type, et Tcholliré (Z1) n'apparaît pas dans M07 | M01 §7 ; M07 | Accepter cette rupture (une cible non vérifiée n'a pas à entrer dans un Top 10) et l'écrire dans M01 |

### 3.6 04 et 07 → 08

| # | Rupture | Fichiers | Correction proposée |
|---|---|---|---|
| R20 | **Le lien 07 → 08 fonctionne pour le projet** : M07 recommande un projet stylisé tiré des paramètres d'O1, et M08 construit « Bauxite-Nord (fictif) » à partir de la DFS de Minim-Martap (prix de 78 $/t, fret de 17 $/t, C1, partage de production de 5 %). Il reste deux écarts : (a) M08 n'importe ni l'IOS ni l'IC de M07, contrairement à la règle 3.6 de M07 ; (b) M08 propose en retour un « score de finançabilité à intégrer à l'Investment Opportunity Score », ce que la règle 3.6 de M07 interdit (pas de double comptage, deux scores distincts) | M07 §3.6, §7 ; M08 §10 | M08 : citer l'IOS et l'IC d'O1 dans la fiche projet ; reformuler le retour en « score de finançabilité distinct, affiché à côté de l'IOS » |
| R21 | M08 ne reprend pas les acquis juridiques de M04 : « décrets non lus » (M04 les a lus) ; part payante « non précisée » (M04 : à titre onéreux, art. 47(4)) | M08 C3, C8 ; M04 §3, §4.5 | M08 renvoie à M04 §3 et §4.5 |
| R22 | M08 C7 et M04 C10 demandent d'ajouter des dépendances (08 ← 05, 06 ; 04 ← BEAC, ITIE) : non reportées dans le cadrage | Cadrage, Dépendances | Voir la section 4, n° 17 |

### 3.7 Tous les modules → 09

| # | Rupture | Fichiers | Correction proposée |
|---|---|---|---|
| R23 | M09 écrit ses propres faits **sans reprendre les livrables** : Edéa « non vérifié » (M05 l'a vérifié) ; alumine « inconnue » (M05, M06) ; décrets « inventaire à faire » (M04) ; « 18 000 échantillons non vérifié » (M01, M02) ; ITIE « mars 2024 » (M03, M04 : 29/02/2024) | M09 §1, §2, §8, §10, §11 | Remplacer ces faits par des renvois aux modules sources |
| R24 | M09 §6.2 décrit la sortie de M06 comme « marchés cibles par produit (Cameroun, CEMAC, ZLECAf, export) ». C'est le format du cadrage, que M06 a remplacé par des couples produit × marché (Nigeria, EAU, Turquie…, la ZLECAf devenant une barrière) | M09 §6.2 ; M06 C1-C3 | Aligner M09 sur le format de M06 |
| R25 | **Échelles de notation hétérogènes** d'un module à l'autre : 0-3 (M04), 1-5 (M05, M06, M09), 0-5 (M07), A-D (M01), High-Low (M02). M09 doit agréger des notes non comparables | M04 §7 ; M05 §5 ; M06 §7.1 ; M07 §3.3 ; M09 §6.3 | Fixer une échelle commune, ou une table de conversion publiée dans M09 |
| R26 | Les « 5 projets phares » du gouvernement (15/07/2026, cités par M09 : Bidzar, Colomine, Grand Zambi, Lobé, Minim-Martap) ne coïncident pas avec le Top 10 de M07 (Wapouzé plutôt que Bidzar ; Mbalam, Nkamouna, Akonolinga en plus) | M09 §3.1 ; M07 §5 | Pas une erreur : à exploiter en séance (comparer la liste du gouvernement et le pipeline des analystes) |

---

## 4. Corrections à apporter au cadrage `AFRICA_MINERAL_INSIGHTS.md`

Les numéros de ligne sont ceux de la version lue le 2026-10-08. Chaque source est celle que cite
le module indiqué.

| # | Passage (ligne) | Remplacement proposé | Source (module) |
|---|---|---|---|
| 1 | L.78, ligne USGS : « Année de référence **2018** » | « Année de référence variable selon la couche : installations 2018 ; gisements 2009 et 2017 ; exploration 2004-2018 ; routes et rails OSM au 30/04/2020. Licence CC0 pour la production USGS, mais couches tierces sous leurs propres licences (OSM : ODbL ; GADM : pas de redistribution ni d'usage commercial sans permission). Pour le Cameroun : 9 gisements, 13 sites d'exploration, aucune occurrence d'or, Kribi absent de la couche ports ; coordonnées incohérentes entre couches (Nkamouna, Minim-Martap). » | M01 C1-C3 ; M03 C4-C8 ; ScienceBase DOI 10.5066/P97EQWXP ; gadm.org/license.html |
| 2 | L.79, ligne « Cadastre minier en ligne du MINMIDT (Flexicadastre) … état actuel … à vérifier » | « Portail cadastral Landfolio (ex-Flexicadastre) du MINMIDT/SDCM : **hors service depuis le 03/11/2025** ; avant sa fermeture, republication interdite sans autorisation écrite et aucun export ouvert. Source de titres utilisable : **Rapport ITIE 2023, annexe 30** (situation au 31/12/2023, sans coordonnées), plus une demande formelle à la SDCM. » | M03 C1-C3 ; https://portals.landfolio.com/cameroon/ ; https://eiti.org/document/25589 |
| 3 | L.80, ligne SIGM : « (campagne citée : 18 000 échantillons, 300 sites) » et attribution à Financial Afrik | « Programme PRECASEM (Banque mondiale, P122153 et P160917, clos le 01/12/2021) : campagne géochimique **prévue** d'environ 18 000 échantillons (annonce de janvier 2017) ; 300 nouveaux sites minéralisés annoncés en juin 2019 pour 2014-2019 ; SIGM conçu dans ce cadre (BRGM, 2018) ; **accès public non trouvé**. » Garder l'étude AMDC (Financial Afrik, 10/07/2025), en précisant que l'article ne mentionne ni le SIGM, ni le PRECASEM, ni ces deux chiffres | M01 C4 ; M02 C1-C3 ; BIC 28/01/2017 et 17/06/2019 ; igfmining.org (BRGM 2018) ; M09 §3.1 |
| 4 | L.81, MNT « SRTM / Copernicus DEM » | Ajouter : « Le Copernicus DEM est un modèle de surface (DSM) : en forêt, il représente la canopée. » | M01 C10 |
| 5 | L.82, ligne Code minier : « décrets d'application publiés progressivement depuis 2024 — inventaire à faire » | « Huit décrets signés les 18 et 19/11/2024 : n° 2024/05061/PM, 05062, 05248, 05249, 05250, 05251, 05252, 05253 ; arrêté du 09/06/2025 sur le cadre de négociation des conventions et décrets du 25/06/2025 (rapportés par la presse, textes non consultés). Texte de travail : transcription AMLA, à comparer au Journal officiel. » | M04 C2, C8, §3 ; https://dgb.cm/?p=28315 |
| 6 | L.83, ligne statistiques commerciales | Ajouter : « INS, *Le Commerce extérieur en 2024* (dernière année disponible ; Comtrade déclarant Cameroun s'arrête à 2023). Les statistiques miroirs sont une borne indicative : origine déclarée incertaine (Rwanda, Ouganda), délais de publication, révisions. » | M06 C5-C6 |
| 7 | Socle de données : **aucune ligne ITIE** | Ajouter une ligne : « Rapport ITIE 2023 (publié en décembre 2025) et annexes XLSX : titres, production, exportations d'or. Le Cameroun est **suspendu de l'ITIE** par la décision 2024-17 du 29/02/2024 (score de 53, exigence 1.3) ; prochaine Validation à partir du 01/04/2027. Utilisé en 03, 04, 06, 09. » | M03 §4 ; M04 §4.12 ; https://api.eiti.org/fr/board-decision/2024-17 |
| 8 | L.96-101 (module 01) : « la télédétection optique **ne voit pas** les altérations hydrothermales » ; « les nuages limitent les images exploitables » (sud et est) | « …la télédétection optique est **fortement dégradée** et doit être validée systématiquement sur le terrain (limite forte sous latérite épaisse). Les nuages limitent les images **partout**, y compris au Nord : fenêtre d'acquisition de novembre à février. » | M01 C7, C9 |
| 9 | L.105 (module 02) : flux « … + Occurrences connues → matrice » | « Géologie + Structures + Géochimie + Géophysique + Télédétection (savane) → modèle → carte. Les occurrences servent à entraîner et valider, pas comme couche d'entrée. Validation par **blocs spatiaux ou par districts**. » | M02 C4-C5 |
| 10 | L.120 (module 03) : « Données : couches USGS Afrique + cadastre minier en ligne » ; L.122-123 « le cadastre reflète la date d'extraction » | « Données : couches USGS Afrique (date par couche) + Rapport ITIE 2023, annexe 30 (titres au 31/12/2023) + OSM (Geofabrik). Afficher : "Titres : situation au 31/12/2023 ; portail cadastral hors service depuis le 03/11/2025". » | M03 C1, C3 |
| 11 | L.130 (module 04) : « rôle de l'organisme public mandaté » | « …rôle de **SONAMINES** (Société Nationale des Mines, décret n° 2020/749 du 14/12/2020), organisme public dûment mandaté au sens du Code 2023 (désigné par les décrets 2024/05061 et 05062). » Ne jamais écrire « SOCAMINES » | M03 C9 ; M04 C3 ; https://prc.cm/en/news/the-acts/decrees/4784-decree-no-2020-749-of-14-december-2020-to-set-up-the-national-mining-corporation-2 |
| 12 | L.134-136 (module 04) : benchmark « par exemple … » ; matrice L.140-149 | « Benchmark : Gabon (pair CEMAC), Côte d'Ivoire (1re d'Afrique de l'Ouest, Fraser 2025), Botswana (1er en Afrique, Fraser 2025). » Ajouter les lignes : stabilité ; change et rapatriement ; commercialisation de l'or et du diamant ; gouvernance et transparence (ITIE) ; communautés ; règlement des différends ; et une colonne « Note » | M04 C5-C7 |
| 13 | L.159-163 (module 05) : « Point à documenter : l'existence d'une capacité d'électrolyse d'aluminium dans le pays (Edéa) et son approvisionnement en alumine, à vérifier » | « Le Cameroun dispose d'une capacité d'électrolyse de 100 kt/an nominaux à Edéa (Alucam), très sous-utilisée (34 à 74 kt/an de 2017 à 2022 ; 53 675 t en 2025) et en crise technique et financière depuis 2024. **Aucune raffinerie d'alumine** dans le pays : alumine entièrement importée (Guinée majoritaire en 2023, puis Irlande, Australie, États-Unis ; UN Comtrade). La chaîne nationale est discontinue. » | M05 C1-C2 (USGS MYB 2017-18 ; ASI ; EcoMatin 30/01/2026) ; M06 §4.4 (Comtrade 2023) ; M07 C10 (BIC 14/07/2026) |
| 14 | L.157 : « Bauxite → concassage/lavage → alumine » ; L.166-167 mini-cas DRI | « concassage/criblage (lavage selon le gisement) » ; ajouter : « Le DRI exige un pellet de qualité DR (environ 67,5 % Fe, SiO₂ + Al₂O₃ ≤ 2,5 %) ; les concentrés annoncés titrent environ 60 % Fe ; aucune usine de pellets ni de DRI au Cameroun. » | M05 C3, C6 |
| 15 | L.176-184 (module 06) : matrice à lignes Cameroun / CEMAC / Afrique (ZLECAf) / Europe / Asie | « Une matrice **par produit** (au minimum aluminium brut, or, bauxite, minerai de fer, ciment), avec les marchés en lignes : Cameroun, CEMAC, Nigeria, Europe, Chine, Japon et Corée, EAU, Turquie, États-Unis selon le produit. La ZLECAf relève de la colonne "Barrières". Colonne "Prix" renommée "Prix net réalisable". » | M06 C1-C4 |
| 16 | L.190-192 (module 07) : « ressources connues (avec le code de déclaration ou la mention "non conforme") » | « …statut de la ressource : **conforme actuel / historique / non conforme / non disponible**, en distinguant ressource et réserve. Champs ajoutés : titulaire, statut du titre, litiges, participation de l'État, date de la dernière information. Afficher un indice de confiance à côté du score. » | M07 C1-C4 |
| 17 | L.58-67, tableau des dépendances | Ajouter : 02 ← occurrences et projets de base (USGS, RNS), avec retour vers 01 ; 04 ← sources externes BEAC et ITIE ; 08 ← 05 et 06 (prix, fret, étape de transformation) en plus de 04 et 07 ; 07 ← jeu de secours pour les substances non couvertes par 02, 05 et 06 (Co-Ni-Mn, rutile, calcaire). Signaler que l'exercice 3 de M04 utilise le projet stylisé de M08 (fournir ses paramètres en amont) | M02 C10 ; M04 C10 ; M07 C8 ; M08 C7 ; R9 |
| 18 | L.205-219 (module 08) | Ajouter deux briques à la chaîne de financement : **dette bancaire locale ou régionale en FCFA (refinancement BEAC, guichet B)** et **royalty / streaming**. Ajouter un sous-module « contrôle des changes et architecture des comptes » (taux de 35 % → 50 % en 2027 → 70 % en 2028, à libeller selon l'instruction BEAC 001/GR/2026 ; fonds de restauration en séquestre à la Banque centrale, art. 192). Présenter la DFI comme une cible, pas comme la norme | M08 C1-C5 ; M04 §4.11 |
| 19 | L.237-239 (module 09) : « stratégie nationale de développement, politiques sectorielles » ; horizons L.231-235 | « SND30 (2020-2030) + Code minier 2023 + PDI (texte non consulté) ; aucune politique minière nationale adoptée n'a été trouvée. Les horizons Develop et Transform dépassent tout cadre officiel existant (Vision 2035). Les horizons se chevauchent : des projets "Develop" sont déjà en cours et une capacité "Transform" (Edéa) existe déjà. » | M09 C1-C3 |
| 20 | L.258-259, Point ouvert n° 4 : « les données USGS sont en principe du domaine public ; celles du cadastre et du SIGM doivent être vérifiées » | « USGS : CC0 pour la production USGS, mais licences tierces par couche (OSM ODbL, GADM non commercial). Cadastre : portail fermé ; ancienne interdiction de republier. SIGM : accès non établi. ITIE (rapport et annexes) : licence non précisée. » | M03 C6 ; M03 Inconnue 10 ; M02 C9 |
| 21 | L.268, source « Cameroon Tribune, Flexicadastre » ; L.269, Financial Afrik | Garder Cameroon Tribune avec la mention « annonce de 2017, portail fermé depuis le 03/11/2025 » et ajouter la page Landfolio. Pour Financial Afrik, limiter la citation à l'étude AMDC et ajouter BIC 28/01/2017, BIC 17/06/2019 et la présentation BRGM 2018 pour les chiffres PRECASEM | M02 C1 ; M03 C1, C11 |
| 22 | L.270-271, sources du Code | M04 n'a pas consulté UNEP LEAP ; M09 a lu une copie FAOLEX (https://faolex.fao.org/docs/pdf/cmr223180.pdf). Indiquer **une** copie de référence et signaler les décalages de numérotation de la transcription AMLA (M04 C8 ; « Section 59 » dans la DFS de Canyon, M08) | M04 C8 ; M08 C3 ; M09 §12 |

**Correction à ne pas faire** : M06 (C7, V30) affirme que les sections 04 et 05 manquent dans le
cadrage. C'est faux pour la version actuelle : c'est M06 qu'il faut corriger, pas le cadrage.

---

## 5. Homogénéité

### 5.1 Statuts de vérification

| Module | Système utilisé |
|---|---|
| 01 | [F] / [I] / [H] / [?] dans le texte ; Vérifié / Partiel / Non vérifié dans les tableaux ; « calcul AMI » |
| 02 | [F] / **[F-e]** (extrait de moteur de recherche) / [I] / [H] / [?] |
| 03 | En toutes lettres : Fait vérifié / Inférence / Hypothèse / Inconnue / Non vérifié, plus la balise **[ancien]** (plus de 2 ans) |
| 04 | Fait vérifié / **Fait rapporté** / Inférence / Hypothèse / Non vérifié ; V1-V43 |
| 05 | [F] / **[F-sec]** / [I] / [H] / [?] |
| 06 | [F] / [F-sec] / [I] / [H] / [?] ; « Vérifié (secondaire) » |
| 07 | [F] / [I] / [H] / [?] plus **⚠ > 2 ans** ; [F] couvre aussi la presse, sans distinction primaire/secondaire (précisée seulement dans le tableau de vérification) |
| 08 | Fait vérifié (« source secondaire » précisé) / Inférence / **Hypothèse pédagogique** / Inconnue ; et V / S / NV dans §3 |
| 09 | [F] / **[F-presse]** / [I] / [H] / [?] |

Conséquence : le même fait peut être [F] dans M07, [F-sec] dans M05 et « Fait rapporté » dans
M04 (exemple : la sentence Sundance, l'instruction BEAC). **Proposition** : une convention unique
pour toute l'édition :

- **[F]** : source primaire lue ;
- **[F-sec]** : source secondaire lue (presse, cabinet) ;
- **[F-e]** : extrait de recherche seulement, à relire ;
- **[I]** : inférence ;
- **[H]** : hypothèse ou choix pédagogique ;
- **[?]** : inconnue ou non vérifié ;
- balise **[ancien]** : information de plus de 2 ans, au 08/10/2026.

Le tableau de vérification de chaque module utilise les mêmes libellés.

### 5.2 Format des sources

- Trois formats : identifiants numérotés par type ([S#], [L#], [M#] dans M02 ; [S#] dans M05 ;
  S1-S40 dans M07) ; liste numérotée 1-43 avec trous (M08) ; listes à puces sans identifiant (M01,
  M03, M04, M06, M09).
- **Proposition** : `[Mxx-n] Auteur ou éditeur (date de publication), « titre » — URL — consulté
  le AAAA-MM-JJ — primaire / secondaire`, avec des identifiants préfixés par le module pour pouvoir
  citer entre modules.

### 5.3 Dates

- Formats mélangés : `2026-10-08` (M01, M03, M06), `08/10/2026` (M07, M03), `8 octobre 2026`
  (M04), `08-10-2026` et `02-09-2024` (M05), `1/12/2021` (M09).
- Date d'extraction : 2026-10-08 partout, mais M05 et M08 indiquent « entre le 2026-10-07 et le
  2026-10-08 ». M03 ajoute un seuil « ancien » au 2024-10-08, M07 le même seuil avec ⚠ : seuil
  cohérent, balises différentes.
- **Proposition** : ISO `AAAA-MM-JJ` partout ; une colonne « Date info » dans tous les tableaux de
  projets, comme dans M03 et M07.

### 5.4 Langue et dénominations

- Rédaction en français partout ; citations anglaises entre guillemets ; titres de modules et de
  livrables en anglais, comme dans le cadrage. Titres de modules hétérogènes : « MODULE 08 » en
  capitales, M05 sans le titre de l'étude de cas dans l'en-tête.
- Graphies à harmoniser : Grand Zambi / Grand-Zambi / Bipindi-Grand Zambi ; SONAMINES / Sonamines ;
  Edéa / Édéa ; Mborguéné / Mborguene ; Kribi-Lobé / Lobé ; Minim-Martap / Minim Martap ;
  G-Stones / G-Stones Resources ; Cameroon Mining Company / Corporation.
- **Copie du Code minier** : AMLA (M04, M08) ou FAOLEX (M09). Les numéros d'articles peuvent
  différer (M04 C8 ; « Section 59 », M08). Une seule copie de référence.

### 5.5 Avertissements

- Un avertissement « pas un conseil en investissement / juridique / fiscal » figure dans M02, M04,
  M05, M06, M07, M08 et M09. **Il manque dans M01 et M03.** M01 contient seulement la mention
  cartographique « ne constitue pas une ressource ni une réserve ».
- Mention de limite de recherche (quota web épuisé) : M01, M02, M03, M04 et M06 ; M07 et M08 en
  décrivent d'autres (paywall, pages non lues). Il faut l'harmoniser dans une rubrique « Limites de
  la recherche » commune.
- Taux de change : aucune conversion (M06), parité EUR (M05), 1,15 €/$ (M08). À fixer.

### 5.6 Structure

Tous les modules ont : Résumé, Corrections au cadrage, Sorties, Tableau de vérification,
Inconnues, Sources. C'est un bon socle. La numérotation des sections diffère, et M04, M07 et M08
placent la spécification du livrable à des endroits différents. Gabarit proposé : 1 Résumé ;
2 Corrections ; 3 Données ; 4-6 Contenu ; 7 Déroulé ; 8 Spécification du livrable ; 9 Sorties ;
10 Vérification ; 11 Inconnues ; 12 Sources.

---

## 6. Priorités

**Priorité 1 : contradictions visibles par les participants (à corriger avant toute session)**

1. Minim-Martap : une seule formulation du calendrier (P1) dans M03, M05, M06, M07, M08 et M09 ;
   supprimer « S1 2026 » de M08.
2. Alucam : capacité, origine de l'alumine et série de production (A1, A2, A4) ; aligner M07 et
   M09 sur M05 et M06.
3. Suspension ITIE (G1), cadastre (G7), décrets (G4) et « 18 000 / 300 » (G11) : aligner M02,
   M03, M04, M06, M07, M08 et M09 sur les modules qui ont vérifié.
4. Bibemi : intégrer la PEA dans M07 et recalculer la note E et le rang de O8 (P23).
5. Art. 47 (G5) : aligner M08 sur M04.

**Priorité 2 : arbitrages nécessitant une nouvelle source**

6. Instruction BEAC 001/GR/2026 : terme exact (« rapatriement » ou « rétrocession »), sanction de
   150 %, numéro du règlement de 2021 (G9, G10).
7. Exportations d'or : 1,897 t sur 2021-2025 (gouvernement) face aux séries DGD/ITIE ; production
   industrielle en 2023 (O2, O3).
8. Minim-Martap : ressource (1 102 ou 1 027 Mt), clause de 15 % ou 30 %, montant tiré sur la
   facilité AFG (P2, P3, P6).
9. Grand Zambi, 6 ou 1,3 Mt/an (P14) ; part de l'État dans Alucam (A3) ; clinker de Figuil (P25) ;
   ressources de Nkamouna et date du décret (P17, P18).

**Priorité 3 : chaîne pédagogique**

10. Zone et projection communes 01-02-03, table de passage des classes de confiance, validation
    par blocs dès M01 (R1 à R5).
11. Ajouter Mbe, Bibemi, Wapouzé et Kambélé à l'inventaire de M03 (R7).
12. Règle de conversion entre les notes de M06 et le critère « Market » de M07, et même note pour un
    même produit (R14) ; reformuler le retour de M08 vers M07 (R20).
13. Fiche de paramètres du projet stylisé disponible dès M04 (R9) ; M09 renvoie aux livrables au
    lieu de réécrire les faits (R23, R24).

**Priorité 4 : cadrage et homogénéité**

14. Appliquer les 22 corrections du cadrage (section 4), en commençant par les n° 2, 3, 5, 7, 11
    et 13.
15. Adopter la convention unique de statuts, de sources et de dates (section 5) ; ajouter
    l'avertissement dans M01 et M03 ; choisir une copie de référence du Code minier et un taux de
    change de référence.
