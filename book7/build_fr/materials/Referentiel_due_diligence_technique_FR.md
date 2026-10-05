# Référentiel de due diligence technique

Les cinq annexes qui suivent sont un référentiel, pas l'essentiel du livre. La méthode du livre est le cadre de décision des dix-huit chapitres. Ces annexes donnent au membre du comité d'investissement ou du comité de crédit assez de connaissances en ingénierie et en environnement pour contester le dossier technique : savoir à quoi ressemblent une étude hydrologique, un aménagement, un choix d'équipements, un plan de construction ou une évaluation environnementale et sociale solides, et quelles questions révèlent un dossier faible.

Elles s'appuient sur les textes intégraux du guide de l'IFC [DE:S1], du guide de l'ESHA [LIT:S6], du guide de l'investisseur d'Addleshaw Goddard et de l'IHA [LIT:S7] et du rapport de la Banque mondiale et de l'ESMAP sur les solutions privées pour la grande hydroélectricité [HY-06], ainsi que sur la base de sources du livre. Chaque annexe applique son contenu à Kasiri lorsque l'étude de cas définit les valeurs, signale chaque hypothèse illustrative qu'elle ajoute et se termine par des tests de décision. Le tableau indique, pour chaque annexe, les questions du Hydro Readiness Framework et les chapitres qu'elle éclaire.

| Annexe | Thème | Questions du cadre | Chapitres |
|---|---|---|---|
| N | Hydrologie et évaluation du productible | Q1, Q5 | 2, 12, 16 |
| O | Aménagement, génie civil et géotechnique | Q1, Q6 | 3, 9, 10 |
| P | Équipements électromécaniques et raccordement au réseau | Q1, Q3, Q6 | 3, 9, 11 |
| Q | Construction, mise en service, exploitation et maintenance | Q6 | 9, 10, 11 |
| R | Due diligence environnementale, sociale et climatique | Q2, Q5, Q7 | 2, 7, 15, 16 |

# Annexe N. Hydrologie et évaluation du productible

## N.1 Objet et périmètre

Le guide de l'IFC qualifie la production attendue de « l'un des déterminants les plus importants » de la viabilité et classe l'hydrologie comme le premier risque de développement [DE:S1]. L'ESMAP aboutit à la même conclusion pour les grands projets et ajoute que le changement climatique rend une évaluation rigoureuse encore plus nécessaire [HY-06]. Cette annexe suit l'estimation du productible depuis la station de jaugeage jusqu'à l'énergie comptée, avec Kasiri comme exemple d'application. Les valeurs de Kasiri sont des données de l'étude de cas, sauf lorsqu'elles sont signalées comme hypothèses illustratives.

## N.2 Données hydrologiques : sources et qualité

Les autorités de l'eau disposent généralement de débits mesurés pour les cours d'eau principaux, mais pas pour les cours d'eau secondaires ni pour les futurs sites de prise d'eau [DE:S1]. Les services hydrologiques nationaux peuvent publier des débits jaugés, des statistiques de débits et des cartes d'écoulement [LIT:S6]. Dans une grande partie de l'Afrique, la contrainte tient aux données de base elles-mêmes : l'ESMAP cite l'insuffisance des données sur les débits comme un obstacle et recommande de soutenir la surveillance hydrométéorologique [HY-06].

Une station de jaugeage enregistre la hauteur d'eau (cote), pas le débit. Le débit est obtenu à partir d'une courbe de tarage ajustée sur des couples de mesures de hauteur et de débit couvrant toute la plage des niveaux, de préférence sur au moins un an [DE:S1; LIT:S6] :

> Q = a (H + B)<sup>n</sup>

où H est la hauteur d'eau, B une correction du zéro de l'échelle et a, n des constantes ajustées [LIT:S6]. Les hautes eaux sont rarement mesurées directement et sont souvent estimées par la méthode pente-section (Manning), sensible à la rugosité : pour des cours d'eau naturels dont le coefficient n vaut environ 0,035, une erreur de 0,001 sur n modifie le débit d'environ 3 % [LIT:S6].

Le comité doit demander la part de jours reconstitués, le débit le plus élevé effectivement mesuré pour établir la courbe de tarage et l'ampleur de son extrapolation, si un lit mobile déplace la courbe après les crues, et comment la station est protégée contre les crues [DE:S1].

## N.3 Longueur de la série et extension de la série

Le guide de l'IFC demande au moins 15 années de données de débit ou de précipitations, de préférence consécutives [DE:S1]. La série de Kasiri compte 12 ans, constituée à partir des jaugeages de préfaisabilité et d'une corrélation régionale. Elle est plus courte que la référence et en partie synthétique.

Le guide de l'IFC décrit trois méthodes pour transposer les données d'une station au site de prise d'eau [DE:S1] :

1. *Mesures simultanées* sur une section temporaire proche de la prise d'eau et à une station existante, corrélées puis utilisées pour transposer la série longue. Cette méthode exige au moins cinq mesures en période sèche, cinq en période moyenne et cinq en période humide ; c'est la plus précise.
2. *Débit spécifique en fonction de l'altitude* : courbe régionale du débit spécifique (l/s/km²) en fonction de l'altitude moyenne du bassin versant, établie à partir de plusieurs stations.
3. *Rapport des superficies de bassin versant* : méthode qui ignore la végétation, les sols et la géologie, et donne les meilleurs résultats lorsque la station est proche de la prise d'eau :

> Q<sub>intake</sub> = Q<sub>gauge</sub> × (A<sub>intake</sub> / A<sub>gauge</sub>)

L'ESHA ajoute les courbes des débits classés normalisées (débits divisés par la superficie du bassin et la pluviométrie, ou par le débit moyen), qui permettent un transfert depuis des cours d'eau voisins de topographie et de climat semblables, ainsi que l'estimation par modèle pluie-débit en l'absence de série de débits : lame d'eau écoulée moyenne tirée d'un bilan hydrique du bassin versant, convertie selon Q<sub>m</sub> = (lame écoulée en mm × superficie en km²) / 31 536, la forme de la courbe étant choisie à partir d'indices de sol et de débit de base, ou modèle de bassin versant alimenté par la pluviométrie journalière [LIT:S6].

Deux questions de crédit en découlent : la série étendue contient-elle une sécheresse aussi sévère que celle à laquelle la dette doit résister, et la dispersion de la corrélation est-elle reportée dans le P90 ? Le guide de l'IFC recommande de vérifier l'hydrologie pendant la conception et, si possible, d'installer une station de jaugeage permanente à la prise d'eau [DE:S1].

## N.4 Courbe des débits classés et choix du débit d'équipement

Une courbe des débits classés (CDC, en anglais FDC) range les débits du plus élevé au plus faible en fonction du pourcentage de temps pendant lequel chacun est égalé ou dépassé ; Q<sub>95</sub> est souvent retenu comme débit caractéristique d'étiage [DE:S1; LIT:S6]. Une CDC plate traduit un débit régulier sur l'année, une CDC pentue de fortes variations saisonnières [DE:S1]. Le pas de temps compte : les moyennes mensuelles lissent les pointes que les turbines ne peuvent pas exploiter, et le productible calculé sur données mensuelles peut être surestimé de 10 % ou plus par rapport aux données journalières [DE:S1].

Le tableau N.1 classe les douze moyennes mensuelles de Kasiri. Le débit turbinable est le débit de la rivière diminué du débit réservé de 4 m³/s, plafonné au débit d'équipement de 57 m³/s ; la puissance est calculée en N.6.


**Tableau N.1. Lecture de la courbe des débits classés mensuels de Kasiri (débits de l'étude de cas)**
{: .cap}

| Rang | Mois | Débit (m³/s) | Fréquence de dépassement m/12 (%) | Fréquence de dépassement m/13 (%) | Débit turbinable (m³/s) | Puissance (MW) |
|---|---|---|---|---|---|---|
| 1 | Mai | 70 | 8,3 | 7,7 | 57 (9 déversés) | 60,5 |
| 2 | Juin | 58 | 16,7 | 15,4 | 54 | 57,3 |
| 3 | Avr. | 52 | 25,0 | 23,1 | 48 | 50,9 |
| 4 | Nov. | 46 | 33,3 | 30,8 | 42 | 44,6 |
| 5 | Juil. | 40 | 41,7 | 38,5 | 36 | 38,2 |
| 6 | Déc. | 36 | 50,0 | 46,2 | 32 | 34,0 |
| 7 | Oct. | 30 | 58,3 | 53,8 | 26 | 27,6 |
| 8 | Mars | 28 | 66,7 | 61,5 | 24 | 25,5 |
| 9 | Août | 28 | 75,0 | 69,2 | 24 | 25,5 |
| 10 | Janv. | 24 | 83,3 | 76,9 | 20 | 21,2 |
| 11 | Sept. | 22 | 91,7 | 84,6 | 18 | 19,1 |
| 12 | Févr. | 20 | 100,0 | 92,3 | 16 | 17,0 |

*Note : Débit moyen (module) 37,8 m³/s ; débit turbinable moyen 33,1 m³/s ; médiane d'environ 33 m³/s. Douze moyennes mensuelles ne permettent pas de déterminer Q<sub>95</sub> ni les pointes de crue. À 57 m³/s, le calcul hydraulique donne 60,5 MW, légèrement au-dessus de la puissance nominale de 60 MW ; plafonner mai à 60 MW retirerait environ 0,3 GWh.*

Premièrement, la pleine charge exige 61 m³/s dans la rivière (57 + 4), débit que seul mai dépasse : sur données mensuelles, la centrale fonctionne donc à pleine puissance environ un mois sur douze ; des données journalières feraient apparaître davantage de jours à pleine charge. Deuxièmement, le taux d'équipement f<sub>a</sub> = Q<sub>d</sub>/Q<sub>av</sub> = 57/37,8 = 1,51 se situe en haut de la fourchette de 1,0 à 1,5 que le guide de l'IFC indique pour les centrales au fil de l'eau, pour lesquelles la règle de première estimation est un débit d'équipement disponible 100 à 120 jours par an, soit environ 30 % du temps [DE:S1]. Troisièmement, l'ESHA observe que l'optimisation conduit normalement à un débit d'équipement « nettement supérieur » au module diminué du débit réservé [LIT:S6], ici 33,8 m³/s. Un débit d'équipement de 57 m³/s n'est défendable que si l'optimisation est démontrée : taux de rendement interne (TRI), valeur actuelle nette (VAN), rapport avantages/coûts ou coût actualisé de l'énergie (LCOE) calculés pour une gamme de débits d'équipement, avec les variations de coût par paliers lorsque la taille des groupes et de la conduite forcée change [DE:S1; LIT:S6]. Cette optimisation doit porter sur des débits journaliers : une CDC mensuelle favorise le surdimensionnement.

En dessous d'un débit minimal technique, la turbine ne peut pas fonctionner [DE:S1]. Le guide de l'IFC indique environ 40 % du débit d'équipement pour une turbine Francis, 20 à 40 % pour une Kaplan et 10 à 20 % pour une Pelton ; l'ESHA indique 50 % pour une Francis, 15 % pour une Kaplan et 10 % pour une Pelton [DE:S1; LIT:S6]. Deux groupes au lieu d'un abaissent le minimum de la centrale [DE:S1]. L'étude de cas ne définit pas les groupes. Hypothèse illustrative : avec un seul groupe Francis à 40 % de minimum (22,8 m³/s), janvier, février et septembre passent en dessous et le modèle mensuel perd environ 14 % du productible ; avec deux groupes identiques, le minimum tombe à 11,4 m³/s et aucun mois n'est perdu.

## N.5 Débit réservé

Le débit réservé (débit résiduel, débit écologique ou débit de compensation) est l'eau qu'une autorisation impose de maintenir dans le tronçon court-circuité. Un débit trop faible nuit à la vie aquatique ; un débit trop élevé réduit la production, surtout en période d'étiage [LIT:S6]. Le guide de l'IFC considère le débit minimal comme la somme des besoins écologiques et des usages en aval, tels que l'irrigation, l'alimentation en eau et la pêche, fixée au cas par cas. Sa démarche est la suivante : comprendre le régime hydrologique, l'écologie et les usages en aval ; consulter les communautés dont les services écosystémiques sont en jeu ; définir les valeurs à préserver ; puis choisir « la méthode la plus appropriée » et surveiller le lâcher [DE:S1]. Sur le plan écologique, le lâcher idéal reproduirait le régime naturel [DE:S1].

Aucun des deux guides ne prescrit de méthode ni de pourcentage. La pratique va des indices hydrologiques (une fraction du module ou un percentile d'étiage) aux méthodes d'habitat, jusqu'aux régimes saisonniers fixés par un panel d'experts ; un lâcher constant est la solution la plus simple et la plus exposée à une révision.

Les 4 m³/s de Kasiri représentent 10,6 % du module et 20 % de la moyenne mensuelle la plus sèche. Chaque m³/s supplémentaire coûte environ 1,06 MW chaque fois que la centrale est en dessous de la pleine charge, soit onze mois sur douze d'après le tableau N.1, ou environ 8 GWh par an (1,06 MW × 8 760 h × 11/12 × 0,95). La liste de contrôle de l'IFC place le débit minimal dans la due diligence de phase 3, car le débit « est le principal déterminant de la production annuelle d'énergie » [DE:S1]. Le comité doit savoir si l'autorisation fixe le lâcher pour toute la durée de la concession.

## N.6 Calcul du productible, étape par étape

La puissance au transformateur est

> P = η<sub>t</sub> × η<sub>g</sub> × η<sub>tr</sub> × ρ × g × Q × H<sub>n</sub> / 10<sup>6</sup> (MW)

avec ρ = 1 000 kg/m³ et g = 9,81 m/s² [DE:S1]. Avec un rendement global type de 87 %, la formule se réduit à P (kW) = 8,5 × Q × H [DE:S1]. Le rendement des alternateurs est de 90 à 98 % et celui des transformateurs de 98 à 99,5 % [DE:S1].

**De la hauteur de chute brute à la hauteur de chute nette.** La hauteur de chute brute se mesure du niveau amont au niveau aval pour les groupes Francis et Kaplan, et du niveau amont au centre de la roue pour les groupes Pelton [DE:S1]. La hauteur de chute nette déduit les pertes de charge singulières (grille, entrée, coudes, vannes) et les pertes de charge linéaires, qui varient avec le carré de la vitesse : la hauteur de chute nette est donc la plus faible au débit maximal ; le niveau aval monte aussi avec le débit [DE:S1; LIT:S6]. L'exemple de l'ESHA (3 m³/s, 85 m de hauteur de chute brute) aboutit à 1,52 m de pertes de charge et à une perte de puissance de 1,8 % [LIT:S6]. Dans les aménagements de moyenne et haute chute, la hauteur de chute peut être considérée comme à peu près constante [LIT:S6], ce qui justifie, en première approximation, la hauteur de chute nette unique de 120 m retenue pour Kasiri.

**Productible et déductions.** Le productible est la somme des puissances multipliées par les durées, par pas journaliers ou par tranches de la CDC, en s'arrêtant là où le débit tombe sous le plus élevé du débit minimal de la turbine et du débit réservé [DE:S1; LIT:S6]. On déduit ensuite :

- la *disponibilité* : environ 95 % la première année (11 jours de maintenance programmée, 7 jours d'arrêts fortuits), puis 97 à 98 % après trois ans [DE:S1] ;
- la *consommation des auxiliaires* : 0,5 à 3,0 % de la production [DE:S1] ;
- les *pertes de transport*, si le point de comptage est éloigné de la centrale [DE:S1].

> E<sub>net</sub> = Σ<sub>i</sub> (ρ g Q<sub>u,i</sub> H<sub>n,i</sub> η<sub>i</sub> t<sub>i</sub>) × A × (1 − a<sub>aux</sub>) × (1 − l<sub>tx</sub>)


**Tableau N.2. Vérification du productible de Kasiri à partir des valeurs de l'étude de cas**
{: .cap}

| Étape | Calcul | Résultat |
|---|---|---|
| Rendement global | 0,92 × 0,98 | 0,9016 |
| Puissance nominale | 9,81 × 57 × 120 × 0,9016 / 1 000 | 60,5 MW |
| Puissance par m³/s | 9,81 × 120 × 0,9016 / 1 000 | 1,061 MW |
| Débit turbinable moyen | Tableau N.1 | 33,1 m³/s |
| Puissance moyenne | 1,061 × 33,1 | 35,1 MW |
| Productible brut | 35,1 × 8 760 h | 307,6 GWh |
| Après disponibilité | × 0,95 | 292,2 GWh |
| Facteur de charge | 292,2 / (60 × 8,76) | 55,6 % |

*Note : Le calcul reproduit le P50 de l'étude de cas (environ 292 GWh) et son facteur de charge (environ 56 %) ; une pondération des mois par leur nombre de jours donne 292,7 GWh. La fourchette de l'IFC pour le facteur de charge des centrales au fil de l'eau est de 40 à 70 % [DE:S1].*

L'arithmétique tient, mais le chiffre de l'étude de cas résulte d'un calcul mensuel à hauteur de chute et rendement constants, sans débit minimal, consommation des auxiliaires ni pertes en ligne. Le tableau N.3 chiffre chacune de ces omissions.


**Tableau N.3. Kasiri : éléments non pris en compte dans le P50 de l'étude de cas (effet sur 292,2 GWh, un élément à la fois)**
{: .cap}

| Élément | Fondement | Résultat |
|---|---|---|
| Consommation des auxiliaires de 0,5 à 3,0 % | [DE:S1] | 290,7 à 283,4 GWh |
| Surestimation de 10 % due aux données mensuelles (292,2 / 1,10) | [DE:S1] | 266 GWh |
| Un seul groupe Francis, débit minimal de 40 % | Hypothèse illustrative | environ 252 GWh |
| Pertes sur la ligne de 35 km en 132 kV | Aucune valeur de source | non chiffré |
| Disponibilité de 97 à 98 % après la troisième année | [DE:S1] | 298 à 301 GWh |
| Tous les débits inférieurs de 10 % | Stress illustratif | 264 GWh |

*Note : Les effets ne s'additionnent pas. L'étude de cas ne précise pas où les 292 GWh sont mesurés ; le point de comptage du contrat d'achat d'électricité (CAE) détermine les pertes supportées par le projet.*

Le calendrier des arrêts compte : une maintenance en février, à environ 17 MW, coûte bien moins que les mêmes jours en mai à 60 MW.

## N.7 Énergie garantie et profil saisonnier

L'ESHA définit l'énergie garantie comme la puissance que l'on peut fournir pendant une période donnée avec une certitude d'au moins 90 à 95 % ; les aménagements au fil de l'eau en offrent peu, une retenue en apporte davantage [LIT:S6]. Dans l'exemple de l'IFC, la puissance garantie à 90 % de l'année est de 11 MW pour une centrale au fil de l'eau et de 23 MW pour une centrale à réservoir sur le même site [DE:S1]. Sur la base des moyennes mensuelles, la puissance garantie de Kasiri est d'environ 17 MW (février) à 19 MW (débit dépassé 11 mois sur 12) avant arrêts, soit environ 16 MW en février après une disponibilité de 95 %, le chiffre utilisé au chapitre 3 ; c'est moins d'un tiers de la puissance installée, et un Q<sub>95</sub> journalier donnerait moins. Le rapport des puissances de mai et de février est de 3,6, plus modéré que l'écart du simple au décuple de l'exemple de l'IFC en Afrique centrale [DE:S1]. Lorsque le CAE rémunère la capacité, c'est le chiffre de puissance garantie qui compte le plus.

## N.8 Variabilité interannuelle : P50, P90, à un an et pluriannuel

Le guide de l'IFC définit le productible d'année sèche (P75) et d'année très sèche (P95) et exige un ratio de couverture du service de la dette (DSCR) supérieur à un dans les pires conditions hydrologiques, comme les années sèches [DE:S1]. Un P90 à un an vérifie si le service de la dette d'une seule année est couvert ; un P90 pluriannuel vérifie la moyenne sur une période de prêt. Avec le coefficient de variation (CV) de 0,15 de l'étude de cas et une loi normale supposée :

> E<sub>Px</sub> = E<sub>P50</sub> × (1 − z<sub>x</sub> × CV / √N)

où N est le nombre d'années moyennées et z = 1,282 pour le P90. La réduction en √N suppose des années indépendantes. Les années sèches ont tendance à se regrouper, ce qui élargit la dispersion réelle ; MODEL 7 ajoute donc une autocorrélation d'ordre un ρ entre les années, fixée à 0,3 pour Kasiri comme hypothèse du modèle :

> E<sub>P90,N</sub> = E<sub>P50</sub> × (1 − 1.2816 × CV × √((1 + ρ) / (1 − ρ) / N))

Une seconde incertitude porte sur la moyenne : 12 années l'estiment avec une erreur type d'environ 0,15/√12 = 4,3 %, avant les erreurs de courbe de tarage et de corrélation, et ce terme ne diminue pas avec la maturité du prêt.


**Tableau N.4. Valeurs de dépassement de Kasiri (CV de 0,15, loi normale supposée)**
{: .cap}

| Mesure | Dispersion | GWh |
|---|---|---|
| P50 | aucune | 292 |
| P75, à un an | 0,674 × 0,15 | 262 |
| P90, à un an | 1,282 × 0,15 | 236 |
| P95, à un an | 1,645 × 0,15 | 220 |
| P99, à un an | 2,326 × 0,15 | 190 |
| P90, moyenne sur dix ans | 1,282 × 0,15/√10 | 274 |
| P90, moyenne sur dix ans, autocorrélation de 0,3 (cas prêteurs de MODEL 7) | 1,282 × 0,15 × √(1,857/10) | 268 |
| P90, moyenne sur 25 ans | 1,282 × 0,15/√25 | 281 |
| P90, moyenne sur dix ans, avec 4,3 % d'incertitude sur la moyenne | 1,282 × √(0,047² + 0,043²) | 268 |

*Note : Calcul de l'analyste, sauf la ligne MODEL 7. Les deux lignes à 268 GWh aboutissent à la même valeur par des voies différentes : l'une élargit la dispersion pour tenir compte de la corrélation entre années, l'autre pour tenir compte de la brièveté de la série. Appliquées ensemble, elles donneraient un chiffre plus bas. Des séries asymétriques donnent des valeurs d'année sèche plus basses encore.*

Le P90 à un an est inférieur de 19 % au P50 ; une vision uniquement pluriannuelle sous-estime ce que le compte de réserve du service de la dette doit couvrir. La réduction d'environ 47 % des allocations de Kariba lors de la sécheresse de 2024 montre jusqu'où peut aller la queue de distribution en cas de sécheresse régionale [CL-04]. En Afrique, les CAE partagent souvent ce risque au moyen de l'énergie réputée livrée ou d'un plancher hydrologique, négocié en fonction de la qualité des données hydrologiques [LIT:S7].

## N.9 Crues de projet

L'étude hydrologique doit aussi couvrir la fréquence et la sévérité des crues, décrites par un hydrogramme et pas seulement par un débit de pointe [LIT:S6]. La crue de projet d'exploitation normale est la plus forte crue évacuée en exploitation normale, définie par une période de retour ; la crue de projet maximale est la plus forte à laquelle les ouvrages doivent résister sans rupture, en général la crue maximale probable (CMP) ou la crue décamillénale [DE:S1; LIT:S6].


**Tableau N.5. Critères types de crue de projet par classe de danger**
{: .cap}

| Classe de danger | Crue de projet |
|---|---|
| Élevée | Crue maximale : CMP ou équivalent, ou crue décamillénale ; exploitation normale : crue millénale |
| Moyenne | Crue centennale à millénale |
| Faible | En général crue centennale ; certains pays ne fixent aucune exigence |

*Note : Source [LIT:S6]. La législation nationale ou les lignes directrices du secteur s'imposent [DE:S1; LIT:S6].*

Le laminage dans la retenue réduit les pointes de débit sortant : la crue entrante et la capacité de l'évacuateur de crues diffèrent donc ; pour les barrages de danger moyen et faible, les règles ignorent souvent le laminage et exigent une capacité d'évacuation supérieure à une pointe de période de retour de 100 à 1 000 ans [LIT:S6]. L'analyse statistique des fréquences convient aux ouvrages moins critiques ; les barrages dangereux exigent une modélisation hydrologique jusqu'à la CMP [LIT:S6]. Le choix de la méthode compte : sur la série de 20 ans de l'ESHA, la crue centennale est de 83 m³/s avec un ajustement log-normal et de 103 m³/s avec une loi log-Pearson III, soit près de 25 % de plus, et l'extrapolation amplifie les erreurs [LIT:S6]. Les lignes directrices de la Banque mondiale sur la sécurité des barrages couvrent le risque hydrologique [HY-15].

Le risque de dépassement d'une crue de période de retour T sur n années est

> R = 1 − (1 − 1/T)<sup>n</sup>

Pour les 3 ans de construction de Kasiri, ce risque est de 14 % pour une crue vicennale et de 3 % pour une crue centennale ; sur 28 ans de construction et d'exploitation, il atteint 25 % pour la crue centennale. Une série de 12 ans ne permet pas de définir statistiquement une crue millénale : il faut des données régionales ou un modèle pluie-débit, et la crue de dérivation doit être cohérente avec l'assurance de l'entrepreneur et la répartition des risques du contrat EPC (clés en main).

## N.10 Sédiments

Le guide de l'IFC range la sédimentation parmi les risques que les investisseurs doivent couvrir et inclut le transport solide dans les études de préfaisabilité [DE:S1]. Les cours d'eau charrient d'importantes quantités de sédiments en crue [DE:S1] ; les sources ne donnent aucune valeur régionale d'apports solides, qui doivent donc être déterminés par des prélèvements sur site incluant les débits de crue.

Dans les centrales de moyenne et haute chute, les matières en suspension usent les turbines et les pièces métalliques, réduisant leur rendement et leur durée de vie ; le quartz et les particules anguleuses sont les plus abrasifs [DE:S1]. Au-delà de 100 m de hauteur de chute, toutes les particules de plus de 0,2 mm doivent être retenues par le dessableur, contre 0,3 mm pour les chutes plus faibles [DE:S1] : avec 120 m, Kasiri relève de la classe 0,2 mm. L'ESHA relie l'efficacité du dessableur aux intervalles de réparation des turbines Francis : environ 6 à 7 ans à 0,2 mm, 3 à 4 ans à 0,3 mm et 1 à 2 ans à 0,5 mm [LIT:S6]. Les revêtements et les groupes à vitesse variable réduisent l'abrasion [DE:S1].

Dans les aménagements au fil de l'eau, un dessableur à chasse est indispensable, car sinon la plupart des sédiments atteignent les turbines [DE:S1; LIT:S6]. Dans les réservoirs, la sédimentation réduit la tranche utile et la production ; les remèdes comprennent la protection du bassin versant, les ouvrages de retenue des sédiments, les chasses, l'enlèvement mécanique et la surélévation du barrage [DE:S1]. À l'échelle mondiale, la capacité de stockage perdue par sédimentation dépasse désormais celle qu'apportent les nouveaux réservoirs [HY-06]. Le modèle de productible doit inclure les pertes dues aux chasses et les arrêts liés aux sédiments, et le budget d'exploitation et maintenance (O&M) l'intervalle de réparation qu'implique le dessableur.

## N.11 Changement climatique et non-stationnarité

Une CDC historique suppose que l'avenir ressemblera au passé. Le guide de l'IFC avertit que les débits peuvent s'écarter des valeurs historiques sous l'effet du changement climatique, avec des modifications régionales importantes du volume et du calendrier des écoulements [DE:S1]. L'ESMAP note que ce risque est souvent transféré en partie ou en totalité à l'État [HY-06]. L'hydroélectricité prévue en Afrique de l'Est et australe concentre la puissance dans quelques bassins et zones pluviométriques, ce qui accroît le risque de sécheresse simultanée [CL-03]. Le guide de l'IHA sur la résilience climatique propose une méthode par étapes de criblage et de tests de résistance [CL-01].

Trois tests en découlent : des tests de tendance et de rupture sur la série ; un cas de stress fondé sur les projections climatiques du bassin ; et la confirmation que les engagements financiers (covenants) sont respectés dans ce cas de stress, et pas seulement au P90 historique. Pour Kasiri, une baisse uniforme de 10 % des débits réduit le productible d'environ 9,7 %, à 264 GWh : le débit réservé fixe prend une part plus importante, tandis que la pointe déversée de mai absorbe une partie de la baisse.

## N.12 Évaluation indépendante du productible par le conseiller technique des prêteurs

Les prêteurs doivent faire recalculer l'estimation du productible par leur conseiller technique, plutôt que d'accepter le chiffre du promoteur. La liste de contrôle de due diligence de l'IFC couvre le bassin versant et les données hydrométéorologiques, la base de données (stations, type de données, longueur des séries), le débit disponible pour la production, les débits de crue, le débit minimal, la puissance installée, la production annuelle et l'analyse probabiliste des années sèches [DE:S1].

Une revue complète contrôle sur site les données de jaugeage et les courbes de tarage ; refait la transposition et en évalue la dispersion ; reconstruit le modèle sur débits journaliers avec une hauteur de chute, un rendement et un débit minimal fonction du débit ; vérifie le débit réservé au regard de l'autorisation et de l'étude d'impact environnemental et social (EIES) ; applique les pertes jusqu'au point de comptage du CAE ; présente le P50 et le P90 à un an et pluriannuel avec toutes les sources d'incertitude ; traite des cas climatiques et sédimentaires ; et rapproche les résultats du partage du risque hydrologique prévu par le CAE [LIT:S7]. Le P50 et le P90 du conseiller doivent servir de base au dimensionnement de la dette.

## N.13 Tests de décision

1. Sur les 12 années de la série de Kasiri, combien ont été mesurées près de la prise d'eau, combien transposées, avec quelle dispersion de corrélation, et pourquoi la série est-elle inférieure aux 15 ans de l'IFC ?
2. Quel est le débit le plus élevé mesuré à l'appui de la courbe de tarage, et quelle part du débit turbinable se situe au-dessus ?
3. Le productible a-t-il été modélisé sur des débits journaliers et, sinon, quelle correction compense la surestimation mensuelle, qui peut atteindre 10 % ou plus ?
4. Où se trouve la courbe du TRI ou du LCOE en fonction du débit d'équipement qui justifie 57 m³/s, compte tenu d'un taux d'équipement de 1,51 ?
5. Combien de groupes, de quel type et avec quel débit minimal, et combien de productible de saison sèche est perdu en dessous de ce minimum ?
6. Le débit réservé de 4 m³/s est-il fixé pour toute la durée de la concession, et qu'advient-il du service de la dette si un lâcher plus élevé ou saisonnier est imposé ?
7. À quel point de comptage les 292 GWh sont-ils mesurés, et la consommation des auxiliaires et les pertes sur la ligne de 35 km sont-elles déduites ?
8. La réserve du service de la dette couvre-t-elle un déficit P90 à un an d'environ 56 GWh au DSCR minimum ?
9. La série montre-t-elle un regroupement des années sèches, et le P90 pluriannuel a-t-il été élargi en conséquence ?
10. Quelles crues de projet ont été retenues pour l'évacuateur de crues, la dérivation et la centrale, comment ont-elles été déduites de 12 années de données, et quelle classe de danger s'applique ?
11. Quelle charge solide a été mesurée et à quels débits, quelle taille de particules le dessableur retient-il, et quel intervalle de réparation des roues le budget d'O&M suppose-t-il ?
12. Quel cas de stress climatique a été simulé, et les engagements financiers (covenants) sont-ils respectés dans ce cas ?

# Annexe O. Schéma d'aménagement, génie civil et géotechnique

## O.1 Objet et champ d'application

Cette annexe donne à un comité de crédit assez de notions de génie civil pour éprouver une étude de faisabilité, un prix EPC et le rapport d'un conseiller technique. Le génie civil est le poste le plus important et le moins prévisible du coût d'investissement d'un aménagement hydroélectrique [DE:S1]. Les chiffres de Kasiri sont des valeurs de l'étude de cas ; chaque dimension de l'aménagement de Kasiri est une hypothèse illustrative, présentée comme telle.

## O.2 Types d'aménagement et conséquences sur les revenus et les risques

Le guide de l'IFC classe les aménagements selon leur mode d'exploitation : au fil de l'eau, à réservoir et de pompage-turbinage (STEP) [DE:S1]. Deux autres catégories comptent pour un financier : l'éclusée (une centrale au fil de l'eau dotée d'une petite retenue journalière ou hebdomadaire) et les aménagements en cascade (plusieurs centrales sur une même rivière dont l'exploitation interagit).


**Tableau O.1. Types d'aménagement, profil de revenus et risque caractéristique**
{: .cap}

| Type d'aménagement | Fonctionnement | Profil de revenus | Risque caractéristique (génie civil et E&S) |
|---|---|---|---|
| Au fil de l'eau | Turbine les apports au fur et à mesure ; peu ou pas de retenue, donc une production de pointe de quelques heures au plus [DE:S1] | Suit l'hydraulicité saisonnière et interannuelle [DE:S1] | Les sédiments atteignent les turbines, un dessableur est donc indispensable [DE:S1] ; risque E&S perçu comme plus faible, apprécié des investisseurs privés [HY-06] |
| Éclusée | Fil de l'eau avec une retenue suffisante pour déplacer le débit au cours de la journée | Même énergie, dont une partie reportée sur les heures de pointe | Seuil plus haut ou petit barrage ; peut franchir les seuils de sécurité des barrages (O.7) |
| À réservoir | Le réservoir stocke l'eau de la saison des pluies ; son volume fixe la durée de pointe [DE:S1] | Énergie et puissance garanties ; moins exposé aux mois secs | Grand barrage ; réinstallation ; fuites en terrain karstique [DE:S1] |
| Pompage-turbinage | Pompe en heures creuses, turbine en heures de pointe ; rendement du cycle jusqu'à environ 80 % [DE:S1] | Écarts de prix et services système tels que l'inertie et le réglage de fréquence [HY-06] | Deux réservoirs ; revenus dépendants de l'organisation du marché |
| Cascade | Plusieurs centrales sur une même rivière | Débit et hauteur de chute dépendent des autres centrales | Les niveaux de retenue ne doivent pas relever le niveau aval de la centrale située en amont ; une retenue amont modifie le débit à l'aval [DE:S1] |

La topographie décide en général du type : une vallée étroite et encaissée permet de créer un réservoir à coût modéré avec un barrage court et haut, alors qu'un relief plat exige un barrage long et coûteux [DE:S1]. Le pompage-turbinage représente plus de 90 % de la capacité mondiale de stockage d'électricité, soit 160 GW en 2021 [HY-06].

## O.3 Ouvrages de l'aménagement dans le sens de l'écoulement

Les deux dispositions de base sont une centrale en pied d'ouvrage de tête ou un aménagement en dérivation avec une centrale à l'aval pour gagner de la chute ; le choix arbitre entre la hauteur de chute et la longueur de l'adduction [DE:S1].

1. **Seuil ou barrage de dérivation.** Relève le plan d'eau jusqu'au niveau de la prise et évacue les crues. Un seuil ne fait que maintenir le niveau amont ; il ne peut pas stocker d'eau [DE:S1]. Les seuils vannés maintiennent un niveau constant, les seuils déversants fixes non [DE:S1].
2. **Évacuateur de crues et vidange de fond.** L'évacuateur de crues fait transiter les débits excédentaires sans endommager le barrage ; la vidange de fond abaisse ou vide la retenue pour la maintenance ou en cas d'urgence [DE:S1].
3. **Prise d'eau.** Grille, dégrilleur et vanne, de préférence sur un tronçon rectiligne au lit stable [DE:S1]. Une submersion d'environ trois diamètres de conduite évite la formation de vortex [DE:S1]. La prise d'eau est en général l'ouvrage qui demande le plus de maintenance [DE:S1].
4. **Grilles.** La vitesse d'approche est typiquement de 0,25 à 1,0 m/s [LIT:S6] ; une grille colmatée provoque une perte de charge et un risque d'arrêt.
5. **Dessableur.** Placé juste à l'aval de la prise. Au-delà de 100 m de chute, les particules de plus de 0,2 mm doivent être retenues ; pour des chutes plus faibles, 0,3 mm est acceptable, et des minéraux durs et anguleux comme le quartz imposent un diamètre de coupure plus petit [DE:S1].
6. **Canal ou galerie d'amenée.** Vitesse dans le canal comprise entre 1,0 et 1,5 m/s, revanche d'environ 10 cm pour un canal revêtu et d'un tiers du tirant d'eau (15 cm au minimum) pour un canal non revêtu [DE:S1]. Vitesse en galerie inférieure à 3 à 4 m/s pour limiter les pertes de charge [DE:S1].
7. **Chambre de mise en charge ou cheminée d'équilibre.** Une chambre de mise en charge contient assez d'eau pour le démarrage, empêche l'entrée d'air dans la conduite forcée et amortit les surpressions lors des déclenchements [DE:S1]. Une cheminée d'équilibre (simple, à orifice étranglé ou différentielle) maîtrise le coup de bélier dans les systèmes en charge [DE:S1].
8. **Conduite forcée.** Dimensionnée pour la charge statique plus le coup de bélier ; tenue par des massifs d'ancrage à chaque changement de direction ou de pente [DE:S1]. L'acier convient aux hautes chutes ; le béton précontraint est limité à environ 15 bar, soit 150 m [DE:S1].
9. **Centrale, en surface ou souterraine.** Le pont roulant doit pouvoir lever la pièce la plus lourde ; une implantation souterraine peut réduire l'impact environnemental [DE:S1]. Les centrales de surface sur terrasses alluviales peuvent nécessiter un traitement spécial des fondations, par exemple par jet grouting [LIT:S6].
10. **Canal de fuite.** Restitue l'eau à la rivière ; son niveau fixe la limite inférieure de la chute utile et, dans une cascade, interagit avec la retenue suivante [DE:S1].

La valeur d'un mètre de chute est un repère utile pour optimiser l'adduction :

> P = ρ g Q H<sub>n</sub> η<sub>t</sub> η<sub>g</sub>

> ΔP par mètre de perte de charge au débit nominal = ρ g Q<sub>d</sub> η<sub>t</sub> η<sub>g</sub>

## O.4 Barrages et seuils : types et critères de choix

Le guide de l'IFC donne les critères de choix du tableau O.2 [DE:S1]. Selon la définition de la CIGB (ICOLD), un grand barrage dépasse 15 m de hauteur, ou mesure de 5 à 15 m avec une retenue de plus de 3 millions de m³ [DE:S1]. L'ESHA cite la définition du « petit » barrage de la CIGB : 15 m de hauteur au plus, crête de moins de 500 m et retenue de moins de 1 million de m³ [LIT:S6].


**Tableau O.2. Types de barrages et critères de choix**
{: .cap}

| Type | Atouts | Limites | Critères de choix |
|---|---|---|---|
| Poids en béton | Évacuateur en crête, centrale en pied, tolère la submersion [LIT:S6] | Exige une fondation saine ; glissement, sous-pressions et fissuration thermique dimensionnent l'ouvrage [LIT:S6] | Vallée étroite en U ; fondation rocheuse ; zones sismiques (comme les remblais) [DE:S1] |
| Béton compacté au rouleau (BCR) | Mise en place continue et très mécanisée, faible coût unitaire [LIT:S6] | Exige un approvisionnement en granulats et en liants à grande échelle | Comme le barrage poids ; la plupart des nouveaux grands barrages sont en BCR ou en CFRD [LIT:S6] |
| Voûte ou coupole | Structurellement efficace, beaucoup moins de béton [LIT:S6] | Vallée étroite et rocher d'appui résistant indispensables [LIT:S6] | Vallée étroite en V [DE:S1] |
| Remblai (terre ou enrochement, à noyau) | S'adapte à de nombreuses fondations ; matériaux locaux [LIT:S6] ; les noyaux argileux conviennent aux zones sismiques [DE:S1] | Sensible à la submersion, aux fuites et à l'érosion interne ; taux de rupture plus élevé que les barrages en béton [LIT:S6] | Vallées larges, plaines, fondations en graviers, limons ou argiles [DE:S1] |
| Enrochement à masque amont en béton (CFRD) | Moins sensible aux fuites et à l'érosion ; pas besoin de matériau de noyau [LIT:S6] | Exige une carrière de roche ; qualité du masque et de la plinthe déterminante | Enrochement disponible, pas d'argile adaptée [LIT:S6] |

Les matériaux doivent être disponibles sur place ou à faible distance de transport [DE:S1] ; un comité doit donc voir les reconnaissances des carrières et des zones d'emprunt, pas seulement les plans du barrage.

## O.5 Galeries et ouvrages souterrains

La qualité du rocher détermine le coût des galeries [DE:S1]. Une galerie peut être non revêtue ou revêtue de béton ou de béton projeté ; ce choix et l'état du rocher fixent les pertes de charge et les fuites [DE:S1]. Une galerie non revêtue exige une section plus grande pour la même perte de charge [DE:S1] : elle échange du revêtement contre de l'excavation et ne se justifie que si le rocher est de bonne qualité et que la pression interne de l'eau ne peut ni ouvrir les joints par vérinage ni s'infiltrer dans des versants instables.

Le forage-minage (drill and blast) est la méthode classique en rocher dur ; les tunneliers (TBM) ont amélioré les rendements et réduit les coûts [DE:S1]. L'arbitrage oppose souplesse et cadence : le forage-minage adapte le soutènement front par front, alors qu'un tunnelier avance vite dans le terrain pour lequel il a été conçu et se rétablit lentement dans un terrain pour lequel il ne l'a pas été. Deux caractéristiques géologiques commandent l'une et l'autre méthode : la variation lithologique le long du tracé et la stabilité structurale du massif rocheux, y compris les failles majeures [LIT:S6]. La galerie de La Rienda citée par l'ESHA a traversé sans incident une faille de chevauchement dans une roche « complètement altérée », uniquement parce que la faille était connue à l'avance [LIT:S6].

Les terrains imprévus sont une source récurrente de litiges sur ce qui est « imprévu » : certains contrats types permettent à l'entrepreneur de réclamer des délais et des coûts, d'autres mettent tout le risque à sa charge, et beaucoup d'entrepreneurs refusent de chiffrer ce risque à un niveau acceptable [LIT:S7]. Les maîtres d'ouvrage prudents font vidanger et inspecter les galeries pendant la période de notification des défauts du contrat EPC (par exemple 24 mois), en conservant jusqu'à son expiration une échéance de paiement importante ou une garantie de crédit [LIT:S7].

## O.6 Phases des reconnaissances géologiques et géotechniques

Sans paramètres précis du rocher et des sols, la conception repose sur des inconnues, « une source de risque importante » [DE:S1]. L'ESHA note que le besoin d'une étude géologique détaillée est « très souvent » sous-estimé, avec pour conséquence des infiltrations sous les seuils et des glissements de canaux [LIT:S6]. Chaque phase doit répondre à la question dont dépend l'engagement suivant.


**Tableau O.3. Phases de reconnaissance et livrables attendus**
{: .cap}

| Phase | Méthodes types | Livrable que le prêteur doit voir |
|---|---|---|
| Identification du site et préfaisabilité | Cartes géologiques nationales (indicatives seulement), photo-interprétation aérienne, visite de terrain [DE:S1; LIT:S6] | Rapport de reconnaissance géologique ; recherche des vices rédhibitoires : failles, glissements de terrain, karst et fondation du barrage |
| Faisabilité | Cartographie géologique et géomorphologique au 1/10 000 à 1/5 000 ; géophysique (électrique ou sismique réfraction) ; puits de reconnaissance ; sondages au barrage, à la prise, aux têtes de galerie et à la centrale ; essais de perméabilité (Lugeon) et de résistance [LIT:S6; DE:S1] | Modèle géologique de l'ingénieur ; classification du massif rocheux le long de l'adduction ; évaluation des fondations et des infiltrations ; évaluation des zones d'emprunt et des carrières ; données d'aléa sismique |
| Appel d'offres et études d'exécution | Sondages complémentaires sur le tracé définitif, essais in situ dans les cavernes et en fondation du barrage | Rapport géotechnique de référence (GBR) intégré au contrat ; base de conception des classes de soutènement et des injections |
| Construction | Levé des fronts, forages de reconnaissance à l'avancement, auscultation | Comparaison du terrain rencontré avec la référence ; base de mesure des réclamations pour conditions de terrain |

Ni l'IFC ni l'ESHA ne fixent un nombre de sondages requis ; le critère est que chaque ouvrage majeur et chaque unité géologique le long de l'adduction soient représentés.

**Rapport géotechnique de référence.** Le FIDIC Emerald Book (2019), élaboré avec l'association des tunnels ITA-AITES, fait du GBR « la seule source ou le seul document contractuel décrivant les conditions souterraines prévues » [DE:S47]. Le maître d'ouvrage supporte les terrains plus défavorables que la référence et bénéficie des terrains meilleurs ; le délai d'achèvement s'ajuste selon les cadences de production de l'entrepreneur, et le paiement varie avec le terrain [DE:S47]. Les développeurs hydroélectriques avertis appliquent le même principe dans les contrats EPC : des données de terrain de référence, plus une formule de partage des coûts au-delà [LIT:S7]. Le GBR transforme un risque géologique illimité en risque mesurable ; l'exposition résiduelle, entre la référence et un terrain défavorable plausible, doit être couverte par les provisions pour aléas ou le soutien des promoteurs.

## O.7 Sécurité des barrages

Les barrages ont été décrits comme « les seules structures construites par l'homme capables de causer le plus de morts », et les petits barrages peuvent eux aussi être dangereux : le seul décès lié à une rupture de barrage en Suède a été causé par un barrage de moins de 4 m de haut [LIT:S6].

**Classement.** La plupart des pays imposent aux propriétaires de classer leurs barrages selon le danger (faible, significatif, élevé), en fonction des conséquences d'une rupture [LIT:S6; DE:S1]. Le classement fixe la crue de projet. Les critères types sont la crue maximale probable, ou à défaut la crue décamillénale, comme crue de projet maximale pour les ouvrages à danger élevé, avec une crue d'exploitation normale millénale ; 100 à 1 000 ans pour un danger moyen ; et en général 100 ans pour un danger faible [LIT:S6]. L'évaluation sommaire du guide de l'IFC retient un débit de projet proche de la crue millénale [DE:S1].

**Revue indépendante.** La norme de performance 4 de l'IFC exige que des professionnels compétents conçoivent et construisent les éléments structurels selon les bonnes pratiques internationales du secteur et, dans les situations à risque élevé, que des experts externes examinent le projet tout au long de ses phases [DE:S1]. La note de bonnes pratiques de la Banque mondiale sur la sécurité des barrages (*Good Practice Note on Dam Safety*, 2021) contient des modèles de termes de référence pour un panel d'experts et des notes techniques sur les risques hydrologique et sismique [HY-15; R4:S1]. Un panel d'experts doit être nommé tôt, examiner les reconnaissances, la conception, la construction et le premier remplissage, et rendre compte aux prêteurs autant qu'au maître d'ouvrage.

**Instrumentation et surveillance.** La sécurité des barrages s'améliore avec des systèmes d'auscultation, des revues et des inspections régulières [LIT:S6]. Les instruments doivent mesurer ce sur quoi repose la conception : sous-pressions et infiltrations (la sous-pression est une charge de calcul [DE:S1]), déformations et tassements, et mouvements forts en zone sismique. Le premier remplissage doit suivre un plan écrit.

**Préparation aux situations d'urgence.** L'EIES et les plans de gestion doivent comprendre des plans d'urgence [DE:S1], fondés sur une étude de rupture de barrage et d'onde de submersion qui cartographie les populations à l'aval, les délais d'alerte et les itinéraires d'évacuation, et testés avec les autorités locales avant la mise en eau.

## O.8 Dérivation provisoire de la rivière pendant les travaux

Les batardeaux sont classés comme des barrages construits pour dériver une rivière [DE:S1]. Les ouvrages de dérivation sont provisoires mais commandent le planning : s'ils sont submergés, la fouille est inondée et le chemin critique s'arrête. Le risque de dépassement sur la durée des travaux découle de la période de retour :

> P<sub>exceed</sub> = 1 − (1 − 1/T)<sup>n</sup>

où T est la période de retour en années et n le nombre d'années d'exposition. L'ESHA tabule cette relation : un événement centennal a 9,6 % de chances de se produire sur 10 ans [LIT:S6]. La crue de projet doit être estimée à partir des débits de pointe, pas des moyennes mensuelles, et le plan de dérivation doit préciser qui supporte le coût d'une crue supérieure à la crue de projet : l'entrepreneur (et ses assureurs) ou le maître d'ouvrage.

## O.9 Le génie civil domine les coûts et le risque de dépassement

Dans l'étude comparative de Fichtner pour le guide de l'IFC, le génie civil représentait de 33,2 à 76,5 % du coût total de la centrale, avec une médiane de 55,2 % et la moitié centrale de l'échantillon entre 47 et 61 % ; les aménagements avec barrage se situent dans le haut de la fourchette [DE:S1]. Comme chaque projet est unique et exposé à la géologie, aux aléas naturels et à la météo, ces coûts sont « imprévisibles et à haut risque » [DE:S1].

Dans cette étude comparative, les provisions pour aléas représentaient en moyenne 9,1 % du coût total de la centrale (médiane 9,8 %), alors que la pratique du secteur est de 15 % pour le génie civil et de 7,5 à 10 % pour les équipements électromécaniques et le raccordement au réseau [DE:S1]. Le guide ajoute que les reconnaissances de sol définitives n'ont souvent pas été faites au stade de la faisabilité, et que le risque de coût est « encore plus élevé s'il faut construire une galerie » [DE:S1]. Les répondants à l'enquête de l'ESMAP ont classé le risque géotechnique et sismique comme le risque technique le plus important pour la grande hydroélectricité [HY-06].

La classe de référence des grands barrages donne à réfléchir : sur 245 barrages, le dépassement de coûts réel avait une médiane de 27 % et une moyenne de 96 %, et le dépassement de délai une médiane de 27 % et une moyenne de 44 % [HY-08]. La distribution est asymétrique à droite. Appliquée à un lot de génie civil au fil de l'eau, elle sert de test de résistance, pas de prévision.

Les estimations de génie civil doivent reposer sur des devis quantitatifs comparés aux prix unitaires nationaux et vérifiés par un ingénieur indépendant ayant l'expérience du pays [DE:S1].

## O.10 Accès au site et logistique

Le choix du site doit vérifier si les routes d'accès existent, doivent être améliorées ou doivent être construites [DE:S1]. Des routes d'accès en terrain difficile peuvent faire échouer le projet (« deal breaker ») en raison de leur coût [DE:S1], et les valeurs de coût aberrantes de l'étude comparative viennent de sites dépourvus d'infrastructures [DE:S1]. Le guide de l'IFC classe les routes d'accès, la construction de la conduite forcée, le creusement des galeries, la fabrication des équipements électromécaniques et le raccordement au réseau parmi les éléments du chemin critique [DE:S1]. Les IFD peuvent appuyer les États en finançant les lignes de transport des projets [HY-06] ; les routes d'accès ont besoin du même financement précoce.

Questions logistiques qui font varier les coûts : le colis le plus lourd au regard de la capacité portante des ponts ; la fiabilité en saison des pluies des itinéraires d'acheminement du ciment, de l'acier et du carburant ; et la distance de transport depuis la carrière.

## O.11 Exemple chiffré de Kasiri

Données du cas : centrale au fil de l'eau de 60 MW, hauteur de chute nette nominale de 120 m, débit d'équipement de 57 m³/s, débit réservé de 4 m³/s, rendement de la turbine de 0,92, rendement alternateur et transformateur de 0,98, P50 d'environ 292 GWh/an, génie civil de 68 millions USD pour un coût de centrale d'environ 157 millions USD, provisions pour aléas de 10 %, construction en 3 ans. Le schéma d'aménagement (seuil de dérivation, dessableur, galerie d'amenée, cheminée d'équilibre, conduite forcée en surface et centrale de surface) est une **hypothèse illustrative**, et non une donnée du cas.

Vérification de la puissance : 1 000 × 9,81 × 57 × 120 × 0,92 × 0,98 ≈ 60,5 MW, cohérent avec 60 MW. Chaque mètre de chute perdu au débit nominal coûte 1 000 × 9,81 × 57 × 0,92 × 0,98 ≈ 0,50 MW. Une mise à l'échelle linéaire du P50 avec la chute donne environ 292 / 120 ≈ 2,4 GWh/an par mètre ; c'est une borne supérieure, car la perte de charge par frottement diminue avec le carré du débit à charge partielle.


**Tableau O.4. Dimensionnement illustratif de Kasiri à partir de règles empiriques sourcées**
{: .cap}

| Élément | Règle | Source | Résultat pour Kasiri (illustratif) |
|---|---|---|---|
| Diamètre de coupure du dessableur | Chute supérieure à 100 m : retenir les particules de plus de 0,2 mm | [DE:S1] | 0,2 mm, moins si les sédiments sont riches en quartz |
| Surface brute des grilles | Vitesse d'approche de 0,25 à 1,0 m/s | [LIT:S6] | 57 / 1,0 à 57 / 0,25 = 57 à 228 m² avant coefficient d'obstruction des barreaux |
| Galerie d'amenée | Vitesse inférieure à 3 à 4 m/s | [DE:S1] | Section de 14,3 à 19,0 m² ; diamètre circulaire équivalent d'environ 4,3 à 4,9 m |
| Canal d'amenée, si retenu | Vitesse de 1,0 à 1,5 m/s | [DE:S1] | Section mouillée de 38 à 57 m² |
| Matériau de la conduite forcée | Béton précontraint limité à environ 15 bar (150 m) | [DE:S1] | Charge statique de plus de 120 m plus une majoration pour coup de bélier de 25 à 50 % pour les turbines à réaction [LIT:S6] : dépasse 150 m ; l'acier est le choix attendu |

Éclusée (illustratif) : en février, le débit moyen est de 20 m³/s, soit 16 m³/s après le débit réservé. Turbiner 57 m³/s pendant 4 heures de pointe exige (57 − 16) × 14 400 s ≈ 0,59 million de m³ de volume utile. C'est moins que le 1 million de m³ de la définition du petit barrage de l'ESHA [LIT:S6], mais un seuil assez haut pour retenir ce volume pourrait tout de même dépasser 15 m ou relever du classement de sécurité des barrages. L'éclusée n'est rentable que si le CAE (PPA) rémunère la production de pointe, ce que le cas ne précise pas.

Dérivation de la rivière : les débits mensuels (20 m³/s en février, 22 m³/s en septembre, 70 m³/s en mai) offrent deux fenêtres d'étiage par an pour les travaux en lit de rivière. Sur les 3 ans de construction, la probabilité que la crue de projet de la dérivation soit dépassée au moins une fois est d'environ 27 % pour une crue décennale, 14 % pour une crue vicennale, 6 % pour une crue cinquantennale et 3 % pour une crue centennale. La série de 12 ans de Kasiri est plus courte que les 15 ans que le guide de l'IFC attend pour l'hydrologie [DE:S1] ; les débits de pointe pour ces périodes de retour sont donc très incertains et doivent être vérifiés par une analyse régionale.

Coût : le génie civil, à 68 millions USD, représente 43 % du coût de la centrale de 157 millions USD et 54 % de la somme de 127 millions USD des six postes de coût de base, proche de la médiane de référence de 55,2 % [DE:S1]. Le coût de la centrale dans le modèle ajoute à ces postes 9,0 millions USD de coûts de développement remboursés au bouclage et une prime de risque de l'entrepreneur de 6,6 millions USD, soit un sous-total de 142,6 millions USD, puis des provisions pour aléas de 10 %, soit 14,3 millions USD. Ces provisions sont proches de ce que donnerait la pratique du secteur sur les seuls travaux (15 % sur le génie civil, 7,5 à 10 % sur les 42 millions USD d'équipements : 13,4 à 14,4 millions USD) [DE:S1], mais uniquement parce qu'elles s'appliquent aussi aux coûts de développement et à la prime, qui ne portent aucun risque physique. Appliqués aux six postes de base seuls, 10 % représenteraient 12,7 millions USD, en dessous de cette fourchette de pratique et en dessous de ce que justifie un aménagement avec galerie. Un dépassement du génie civil égal à la médiane des grands barrages, 27 % [HY-08], ajoute 18,4 millions USD ; à la moyenne de 96 %, 65,3 millions USD. Avec la galerie illustrative, l'écart entre les provisions pour aléas et le cas de stress médian doit être couvert par le partage des risques du GBR, le soutien des promoteurs ou une facilité de réserve.

## O.12 Risques par ouvrage et preuves demandées par les prêteurs


**Tableau O.5. Ouvrage, risque type et preuves pour les prêteurs**
{: .cap}

| Ouvrage | Risque type | Preuves demandées par le prêteur |
|---|---|---|
| Seuil ou barrage | Infiltrations et affouillement sous la fondation ; glissement ; submersion | Sondages de fondation et essais de perméabilité ; stabilité pour tous les cas de charge [DE:S1] ; classe de danger |
| Évacuateur de crues et vidange de fond | Sous-dimensionnement face aux crues ; défaillance des vannes | Étude des crues adaptée à la classe de danger [LIT:S6] ; fiabilité des vannes |
| Prise d'eau et grilles | Colmatage, vortex, entrée de sédiments | Vérification de l'implantation et de la submersion [DE:S1] ; dégrillage |
| Dessableur | Abrasion des turbines ; défaillance des chasses | Échantillonnage et minéralogie des sédiments ; conception de la décantation [DE:S1] |
| Canal d'amenée | Fuites provoquant une rupture de versant | Stabilité des versants, drainage et conception du revêtement [LIT:S6] |
| Galerie d'amenée | Terrain défavorable, failles, venues d'eau, effondrement ; fuites à travers le revêtement | Profil géologique en long ; classes de massif rocheux ; GBR et partage des risques [DE:S47; LIT:S7] ; inspection après vidange [LIT:S7] |
| Chambre de mise en charge ou cheminée d'équilibre | Entraînement d'air ; coup de bélier ; charge sur la fondation | Analyse des régimes transitoires en cas de déclenchement |
| Conduite forcée | Rupture sous coup de bélier ; déplacement des massifs d'ancrage sur les pentes | Classe de pression incluant les surpressions ; géotechnique des massifs d'ancrage [DE:S1] |
| Centrale | Tassement des fondations ; inondation ; stabilité de la caverne si souterraine | Reconnaissance des fondations ; niveaux de crue ; soutènement de la caverne |
| Canal de fuite | Remous dus aux crues ou à la retenue aval | Courbe de tarage du niveau aval ; règles d'exploitation en cascade [DE:S1] |
| Ouvrages de dérivation | Submersion pendant les travaux | Probabilité de dépassement ; répartition des risques |
| Accès et logistique | Retard sur le chemin critique ; transport des colis lourds | Reconnaissance des itinéraires ; plan pour la saison des pluies [DE:S1] |

## O.13 Tests de décision

1. Le type d'aménagement correspond-il au contrat de revenus : si le CAE paie une puissance de pointe ou garantie, existe-t-il une retenue pour la fournir, et sinon, le tarif rémunère-t-il uniquement l'énergie ?
2. L'adduction a-t-elle été optimisée sur la valeur en cycle de vie, en mettant en regard le coût énergétique de chaque mètre de perte de charge (environ 2,4 GWh/an par mètre à Kasiri, en borne supérieure) et le coût d'excavation et de revêtement ?
3. Le type de barrage s'appuie-t-il sur des sondages de fondation et sur une carrière ou une zone d'emprunt reconnue à faible distance de transport ?
4. Chaque ouvrage majeur et chaque unité géologique le long de l'adduction ont-ils fait l'objet de reconnaissances propres au site, ou certaines parties de la conception reposent-elles encore sur des cartes régionales ?
5. Le contrat de génie civil comporte-t-il un GBR, qui supporte les terrains plus défavorables que la référence, et la part du maître d'ouvrage est-elle couverte par les provisions pour aléas ou par un financement engagé des promoteurs ?
6. Quelle classe de danger a été attribuée au barrage ou au seuil, quelles crues de projet et de vérification en découlent, et ont-elles été estimées à partir de données de débits de pointe plutôt que de moyennes mensuelles ?
7. Un panel indépendant a-t-il examiné la conception et la construction, examinera-t-il le premier remplissage, et une étude de rupture de barrage, un plan d'urgence et un plan d'instrumentation sont-ils en place ?
8. Quelle est la probabilité que la crue de projet de la dérivation soit dépassée pendant les travaux, et qui paie si c'est le cas ?
9. Les provisions pour aléas du génie civil atteignent-elles au moins la norme du secteur de 15 %, et le tableau des ressources et emplois résiste-t-il à un dépassement du génie civil égal à la médiane de 27 % de la classe de référence des grands barrages ?
10. Les routes d'accès, les itinéraires des colis lourds et le raccordement au réseau situés sur le chemin critique sont-ils financés et autorisés avant l'ordre de commencer les travaux ?
11. Les galeries seront-elles vidangées et inspectées avant la fin de la période de notification des défauts du contrat EPC, avec une retenue de garantie ou une garantie de crédit encore en place ?

# Annexe P. Équipements électromécaniques et raccordement au réseau

## P.1 Objet et champ

Le lot électromécanique transforme la hauteur de chute et le débit en énergie vendable : turbines, alternateurs, régulateurs de vitesse et systèmes d'excitation, transformateurs, poste d'évacuation, protections, SCADA, auxiliaires, ainsi que les vannes et organes hydromécaniques qui commandent l'arrivée d'eau aux groupes. Dans chaque grande centrale, les équipements électromécaniques sont conçus sur mesure [DE:S1]. Dans l'échantillon de référence de l'IFC, les équipements électromécaniques représentent en moyenne 30,3 % du coût total de la centrale (médiane 29,2 %), dans une fourchette de 14,9 à 56,6 % [DE:S1]. Les décisions qu'un comité doit tester sont peu nombreuses : le type de turbine, le nombre et la vitesse des groupes, le calage de la turbine, la protection contre les sédiments, et le régime contractuel et d'essais qui rend les garanties des fournisseurs opposables.

## P.2 Types de turbines et choix selon la hauteur de chute et le débit

Le choix de la turbine repose sur la hauteur de chute et le débit du site, y compris la fréquence à laquelle la turbine fonctionnera à charge partielle parce que le débit disponible est inférieur au débit d'équipement [DE:S1]. Les turbines se répartissent en deux familles [DE:S1] :

- **Turbines à action** (Pelton, Turgo, Banki) : la roue tourne dans l'air sous un ou plusieurs jets. Elles conservent leur rendement lorsque le débit fluctue, évitent les surpressions dans la conduite forcée, maîtrisent facilement la survitesse et sont faciles à entretenir.
- **Turbines à réaction** (Francis, hélice, Kaplan, bulbe) : la roue est noyée dans une enveloppe sous pression et entraînée par la portance ; un aspirateur récupère la chute sous la roue. Leurs roues sont plus petites et plus rapides que celles des Pelton, peuvent fonctionner noyées et offrent un meilleur rendement aux fortes puissances.

Le guide de l'IFC classe les aménagements en haute chute au-dessus de 100 m, moyenne chute de 30 à 100 m et basse chute en dessous de 30 m [DE:S1]. Sa section consacrée aux turbines retient une autre limite pour la basse chute (moins de 10 m) et comporte une coquille sur la plage moyenne (« 50 m < H < 10 m ») ; il faut donc citer les classes d'aménagement [DE:S1]. L'abaque hauteur de chute-débit du guide (figure 4-19, en axes logarithmiques de 1 à 1000 m de chute et de 1 à 1000 m<sup>3</sup>/s de débit) place, autant qu'on puisse le lire, les Pelton et Turgo en haute chute et faible débit, les Kaplan en basse chute et fort débit, les Banki en basse à moyenne chute et faible débit, et les Francis sur le vaste domaine intermédiaire ; les limites dépendent de la conception de chaque constructeur [DE:S1].


**Tableau P.1. Types de turbines : principe, domaine d'emploi et comportement à charge partielle**
{: .cap}

| Type | Principe | Domaine d'emploi selon les sources | Caractéristiques utiles pour un comité |
|---|---|---|---|
| Pelton | Action ; augets à double cuillère, un ou plusieurs injecteurs à pointeau | Haute chute, faible débit ; turbine à action la plus répandue [DE:S1] | Jusqu'à 2 injecteurs (axe horizontal) ou 6 (axe vertical) ; le déflecteur limite la survitesse lors d'un rejet de charge [DE:S1] |
| Turgo | Action ; le jet frappe le plan de la roue sous un angle d'environ 20 degrés | Domaine Pelton, débit plus élevé par roue [DE:S1] | Roue plus petite qu'une Pelton à puissance égale [DE:S1] |
| Banki (cross-flow, Banki-Michell) | Action ; rotor en tambour, l'eau traverse la roue deux fois | Basse à moyenne chute, faible débit (lecture de l'abaque de l'IFC) [DE:S1] | Seuls les 2/3 de la dénivelée entre la roue et le niveau aval comptent dans la chute brute [DE:S1] |
| Francis | Réaction ; entrée radiale, sortie axiale, bâche spirale avec directrices | Turbine la plus répandue ; vaste domaine intermédiaire de chute et de débit [DE:S1] | Le rendement chute fortement en dessous d'environ la moitié du débit d'équipement [DE:S1] |
| Hélice (pales fixes) | Réaction ; écoulement axial, 3 à 6 pales | Basse chute [DE:S1] | Débit technique minimal de 75 % du débit d'équipement [LIT:S6] |
| Kaplan | Hélice à pales et directrices réglables (double réglage) | Basse chute, débit variable [DE:S1] | Coût plus élevé, rendement élevé sur une large plage de débit [DE:S1] |
| Bulbe | Kaplan à axe horizontal dont l'alternateur est logé dans un bulbe étanche | Chutes jusqu'à 30 m, forte puissance [DE:S1] | Excavation plus réduite qu'une Kaplan à axe vertical [DE:S1] |

Les centrales bulbe et Kaplan de basse chute utilisent des alternateurs lents ; les centrales Francis et Pelton de haute chute, des alternateurs rapides [DE:S1].

## P.3 Vitesse spécifique

La vitesse spécifique condense la hauteur de chute, le débit (ou la puissance) et la vitesse de rotation en un seul nombre qui caractérise la forme de la roue : faible pour les Pelton, intermédiaire pour les Francis, élevée pour les hélices et les Kaplan. À chute et débit égaux, une hélice tourne plus vite qu'une Francis, ce qui explique qu'elle ait supplanté la Francis en basse chute [DE:S1]. L'ESHA fait de la vitesse spécifique son principal critère de sélection [LIT:S6], mais aucun des textes sources disponibles ici ne donne de plages numériques par type de turbine ; l'annexe se limite donc aux définitions, et l'ingénieur doit présenter l'abaque d'expérience du constructeur à l'appui de toute vitesse proposée.

Trois formes sont d'usage courant (n en tr/min, Q en m<sup>3</sup>/s par groupe, H hauteur de chute nette en m, P puissance sur l'arbre par groupe) :

> n<sub>s</sub> = n × P<sup>0.5</sup> / H<sup>1.25</sup> (P en kW ; forme métrique fondée sur la puissance)

> n<sub>q</sub> = n × Q<sup>0.5</sup> / H<sup>0.75</sup> (forme fondée sur le débit)

> n<sub>QE</sub> = (n / 60) × Q<sup>0.5</sup> / (g × H)<sup>0.75</sup> (forme adimensionnelle)

La vitesse de rotation d'un groupe synchrone est fixée par la fréquence du réseau f et le nombre de paires de pôles p :

> n = 60 × f / p

La vitesse varie donc par paliers discrets. À vitesse spécifique constante, la vitesse augmente quand la taille du groupe diminue ; une vitesse spécifique plus élevée réduit la taille de l'alternateur mais impose un calage plus profond pour se prémunir contre la cavitation (P.6).

## P.4 Rendement et comportement à charge partielle

Le choix de la turbine doit comparer les rendements sur toute la plage de débit, et pas seulement au point de dimensionnement [DE:S1]. Les turbines Pelton et Kaplan conservent un rendement élevé en dessous du débit d'équipement ; le rendement des Banki et des Francis baisse plus fortement en dessous de la moitié du débit, ce qui les destine aux débits réguliers [DE:S1]. En dessous d'un débit minimal, le groupe doit être arrêté pour éviter les dommages causés par de fortes vibrations [DE:S1]. Les deux sources indiquent des débits minimaux différents, et l'écart compte pour les mois d'étiage.


**Tableau P.2. Débit technique minimal par type de turbine, en % du débit d'équipement**
{: .cap}

| Turbine | Guide de l'IFC [DE:S1] | Guide de l'ESHA [LIT:S6] |
|---|---|---|
| Pelton | 10 à 20 (selon le nombre d'injecteurs) | 10 |
| Turgo | non indiqué | 20 |
| Francis | 40 | 50 |
| Kaplan (double réglage) | 20 | 15 |
| Semi-Kaplan (simple réglage) | 40 | 30 |
| Hélice (pales fixes) | non indiqué | 75 |

*Note : l'IFC indique pour les Kaplan 20 à 40 %, respectivement pour les machines à double réglage et à simple réglage.*

L'estimation de l'énergie doit appliquer la courbe de rendement tranche par tranche sur la courbe des débits classés, en s'arrêtant au plus élevé du débit technique minimal et du débit réservé [LIT:S6]. La hauteur de chute nette est la plus faible au débit maximal, car les pertes de charge croissent avec le carré de la vitesse et le niveau aval monte avec le débit [DE:S1] ; une hauteur de chute nette nominale doit donc être indiquée avec le débit correspondant.

La production à vitesse variable réduit les variations de rendement hors chute ou débit nominal et diminue l'abrasion [DE:S1].

## P.5 Nombre et taille des groupes

Le nombre de groupes résulte d'un arbitrage entre trois éléments :

1. **Fonctionnement à faible débit.** Exemple tiré du guide de l'IFC : au lieu d'un seul groupe Francis de 60 MW, deux groupes de 30 MW permettent de fonctionner jusqu'à 20 % du débit d'équipement de la centrale au lieu de 40 % [DE:S1]. Chaque aménagement exige d'évaluer si l'énergie supplémentaire paie le surcoût [DE:S1].
2. **Disponibilité.** Avec un seul groupe, tout arrêt du groupe est un arrêt de la centrale. Les grandes révisions reviennent tous les 7 à 12 ans et durent 4 à 6 semaines pour les groupes de plus de 20 MW [DE:S1] ; avec plusieurs groupes, elles peuvent être placées pendant les mois d'étiage.
3. **Coût.** Plus de groupes signifie plus de turbines, d'alternateurs, de vannes, de systèmes de commande et une centrale plus longue ; dans l'exemple d'optimisation de l'IFC, le TRI évolue par paliers avec le coût unitaire des turbines [DE:S1]. Des groupes identiques partagent les pièces de rechange et n'exigent des essais de performance que sur un seul groupe [DE:S1].

Le pont roulant de la centrale est dimensionné pour la pièce la plus lourde, un élément de l'alternateur ou la roue [DE:S1] ; des groupes moins nombreux et plus gros alourdissent donc aussi les charges de levage et de transport.

## P.6 Cavitation et calage de la turbine

La cavitation se produit là où la pression descend sous la pression de vapeur ; les cavités de vapeur implosent dans les zones de pression plus élevée et peuvent causer des dégâts très importants [LIT:S6]. Dans une turbine à réaction, le niveau aval détermine son apparition [LIT:S6]. La cavitation et l'érosion endommagent les roues et réduisent le rendement ; en exploitation et maintenance (O&M), la parade consiste en inspections et en recharges par soudure sur place [DE:S1].

Le calage (cote de la roue par rapport au niveau aval minimal) est régi par le coefficient de cavitation de l'installation (sigma de Thoma) :

> σ<sub>plant</sub> = (H<sub>atm</sub> − H<sub>v</sub> − H<sub>s</sub>) / H

où H<sub>atm</sub> est la hauteur représentative de la pression atmosphérique (qui diminue avec l'altitude), H<sub>v</sub> la hauteur représentative de la pression de vapeur, H<sub>s</sub> la hauteur d'aspiration (positive lorsque la roue est au-dessus du niveau aval) et H la hauteur de chute nette. Le calage doit donner un σ<sub>plant</sub> supérieur au sigma critique de la turbine, avec une marge fixée par le constructeur à partir des essais sur modèle. Les sources ne donnent pas de valeurs de sigma en fonction de la vitesse spécifique ; l'annexe n'en cite donc aucune. Le calcul reste utile : à 120 m de chute nette, chaque 0,01 de sigma représente 1,2 m de profondeur de calage, de sorte qu'un changement de vitesse de la roue ou un niveau aval minimal plus bas peut déplacer le plancher de la centrale de plusieurs mètres et modifier le coût du génie civil.

## P.7 Abrasion par les sédiments et revêtements

Dans les centrales de moyenne et haute chute, les sédiments en suspension usent les ouvrages hydrauliques métalliques et les turbines, ce qui réduit leur rendement et leur durée de vie [DE:S1]. Plus la chute est haute, plus la particule à éliminer est petite : au-dessus de 100 m de chute, toutes les particules de plus de 0,2 mm doivent être retenues dans le dessableur ; 0,3 mm est acceptable pour des chutes plus faibles ; des particules dures (quartz) et anguleuses justifient une limite plus basse [DE:S1]. L'ESHA exprime le pouvoir abrasif des grains sur une roue Francis ainsi :

> P<sub>e</sub> = μ × V<sub>g</sub> × ((ρ<sub>s</sub> − ρ<sub>w</sub>) / R) × v<sup>3</sup>

avec μ un coefficient de frottement, V<sub>g</sub> le volume du grain, ρ<sub>s</sub> et ρ<sub>w</sub> les masses volumiques du grain et de l'eau, R le rayon de l'aube et v la vitesse du grain [LIT:S6]. Comme la vitesse des grains croît avec la chute, l'abrasion augmente fortement avec la hauteur de chute. L'ESHA fait état d'intervalles de réparation des roues Francis d'environ 6 à 7 ans avec un dessableur retenant 0,2 mm, de 3 à 4 ans à 0,3 mm et de 1 à 2 ans à 0,5 mm, et situe l'optimum économique vers 0,2 mm en conditions sévères (haute chute, quartz) et 0,3 mm en conditions normales [LIT:S6].

Les mesures d'atténuation sont un dessableur efficace, des revêtements céramiques durs [DE:S1], la vitesse variable [DE:S1] et, sur les rivières chargées en limons, le suivi des limons pour planifier les réparations [DE:S1]. Les sources ne chiffrent ni la durée de vie ni le coût des revêtements.

## P.8 Alternateurs, excitation et régulateurs de vitesse

Les groupes de grande et moyenne taille ont généralement un arbre vertical ; les petits groupes, un arbre horizontal [DE:S1]. L'excitation est sans balais ou à balais [DE:S1]. Les **alternateurs synchrones** ont une excitation en courant continu ou à aimants permanents et un régulateur de tension ; leur excitation est indépendante du réseau, ce qui leur permet de fonctionner en réseau isolé (îlotage) et de régler la tension [DE:S1]. Les **générateurs asynchrones** ne peuvent pas régler la tension, tournent à une vitesse liée à la fréquence du réseau et ne peuvent pas produire d'énergie lorsqu'ils sont isolés, car leur excitation provient du réseau [DE:S1]. Pour une centrale de 60 MW raccordée au réseau et censée contribuer au réglage de la tension, les machines synchrones sont le choix normal. Le rendement de l'alternateur augmente avec sa puissance nominale et approche 98 % au-dessus de 1 MW [DE:S1].

Le régulateur de vitesse agit sur les directrices ou les pointeaux pour maintenir la vitesse et la charge ; la pratique actuelle est le régulateur numérique PID [DE:S1]. Le temps de fermeture et le circuit hydraulique interagissent : le coup de bélier normal lors d'un arrêt commandé par le régulateur peut élever la pression dans la conduite forcée de 25 à 50 % de la chute brute pour les turbines à réaction, selon les constantes de temps du régulateur [LIT:S6]. Le temps de démarrage de l'eau t<sub>h</sub> de l'ESHA permet de vérifier que le circuit hydraulique est réglable :

> t<sub>h</sub> = V × L / (g × H)

Si t<sub>h</sub> est inférieur à 3 s, une cheminée d'équilibre est inutile ; au-delà de 6 s, une cheminée d'équilibre ou un autre dispositif est nécessaire pour éviter de fortes oscillations du régulateur de la turbine, et un régulateur mal conçu peut interagir avec les oscillations de la cheminée d'équilibre [LIT:S6]. Lorsque les vannes doivent se fermer rapidement, une vanne de décharge montée en parallèle sur la turbine ralentit les variations de débit dans la conduite forcée [LIT:S6].

## P.9 Transformateurs, poste d'évacuation, protections, SCADA et auxiliaires

Les transformateurs élévateurs relèvent la tension pour réduire les pertes en ligne [DE:S1]. Le poste d'évacuation doit être implanté près de la centrale, au-dessus du niveau aval de projet (par exemple le niveau de la crue centennale), et dimensionné selon le nombre et la direction des lignes de départ [DE:S1]. L'entretien des transformateurs repose sur la surveillance de la température de l'huile et des enroulements, l'analyse des gaz dissous et les essais de tangente delta [DE:S1]. Les protections font l'objet d'essais par injection primaire et secondaire, et les relais de l'alternateur sont testés fonctionnellement lors de marches à vide [DE:S1]. Le contrôle-commande logiciel et le SCADA permettent un diagnostic à distance lorsque la présence permanente du fournisseur n'est pas rentable [DE:S1]. Les auxiliaires comprennent les pompes de drainage et d'épuisement, le refroidissement, l'air comprimé, la ventilation, les alimentations en courant alternatif et continu et le groupe diesel de secours [DE:S1].


**Tableau P.3. Durée de vie utile attendue des composants électromécaniques [DE:S1]**
{: .cap}

| Composant | Durée de vie (années) |
|---|---|
| Turbine (hors roue), alternateur, régulateur de vitesse, excitation, vannes de garde principales | 40 |
| Roues de turbine | 10 |
| Transformateurs de puissance ; appareillage HT et poste d'évacuation | 40 |
| Appareillage MT et BT | 30 |
| Contrôle-commande, protections, SCADA, télécommunications, comptage | 20 |
| Équipements auxiliaires mécaniques et électriques | 30 |
| Conduites forcées, vannes, batardeaux, grilles ; lignes de transport | 70 |

*Note : moyennes ; la durée de vie réelle dépend de la qualité de l'eau, de la charge sédimentaire, du climat et du nombre de démarrages et d'arrêts [DE:S1].*

## P.10 Équipements hydromécaniques

Les ouvrages hydrauliques métalliques sont classés selon leur fonction [DE:S1] : les vannes de service règlent le débit ou le niveau (évacuateur de crues, vidange de fond) ; les vannes de garde sont seulement entièrement ouvertes ou fermées (prise d'eau, aspirateur, amont des vannes de tête de conduite forcée) ; les vannes de maintenance, généralement des batardeaux, permettent de mettre à sec les conduits ; les directrices ou les pointeaux règlent le débit de la turbine ; les grilles protègent les prises d'eau. Le type de vanne dépend de la fonction, de la taille de l'ouverture, du climat et du mode d'exploitation [DE:S1]. La mise en service vérifie la vitesse de manœuvre des vannes, l'étanchéité des vannes fermées et des vannes de secours, et le temps de manœuvre des vannes de tête [DE:S1].

## P.11 Raccordement au réseau et code de réseau

Le coût du raccordement au réseau dépend surtout de la distance au réseau [DE:S1]. Dans la pratique du secteur, les provisions pour aléas sont de 7,5 à 10 % pour le raccordement au réseau et les équipements électromécaniques, contre 15 % pour le génie civil [DE:S1]. L'absence de ligne de transport et de renforcements du réseau est un obstacle majeur à la mise en service commerciale, qui génère d'importantes réclamations d'énergie réputée livrée à la charge des acheteurs [HY-06], et la mise en service exige une coordination précoce avec le gestionnaire du réseau [DE:S1].

Les sources ne citent aucune valeur de code de réseau (plages de fréquence et de tension, tenue aux creux de tension, réserve). Son contenu en matière d'essais ressort de la liste de mise en service : synchronisation, essai de capacité de puissance réactive, essai du stabilisateur de puissance (PSS), courbe en V, rejet de charge à 25, 50, 75, 100 et 110 % de la charge nominale, et répartition conjointe des puissances active et réactive pour les centrales à plusieurs groupes, avec comparaison des résultats au contrat de fourniture et au contrat d'achat d'électricité (CAE) [DE:S1]. Le comité doit se procurer le code de réseau national et rattacher chaque clause à un article de la spécification des équipements et à un essai.

## P.12 Contrats de fourniture, essais en usine et sur site

Les développeurs séparent souvent les contrats de génie civil, d'équipements électromécaniques et de raccordement au réseau ; les prêteurs préfèrent en général un contrat EPC clés en main, plus coûteux parce que le risque est transféré à l'entrepreneur [DE:S1]. En lots séparés, on utilise généralement le Livre jaune de la FIDIC pour les équipements électromécaniques et le Livre rouge pour le génie civil, et seule une poignée de fournisseurs de turbines est en concurrence [LIT:S7]. Les paiements des équipements électromécaniques sont généralement de 30 % à l'avance, 50 % à la livraison et 20 % à la réception [DE:S1], et leur fabrication se trouve sur le chemin critique [DE:S1]. Les garanties des fournisseurs dépassent souvent la période de garantie de l'EPC (par exemple 24 mois) ; le maître d'ouvrage doit en bénéficier par cession ou par garantie collatérale (collateral warranty) [LIT:S7].

Le futur personnel d'exploitation et de maintenance doit assister au montage et aux essais en usine [DE:S1]. Les essais sur site se font à sec (alignement, jeux des paliers, temps de manœuvre des vannes, isolement et tenue diélectrique des enroulements, logique du régulateur), à vide (survitesse, vibrations, excitation) et en charge [DE:S1]. Pour les groupes de plus de 5 MW, un essai de réception sur site selon la norme IEC 60041 et un essai par méthode indicielle vérifient le rendement de la turbine sur au moins un groupe, et les pertes de l'alternateur sont mesurées sur au moins un alternateur [DE:S1]. Les grands projets imposent couramment une marche probatoire de 30 jours par groupe ; tout défaut oblige à la recommencer [DE:S1]. Le stock de pièces de rechange représente environ 2,5 à 3,0 % du prix FOB des équipements, et le budget annuel de maintenance électromécanique environ 2,0 à 2,5 % de l'investissement initial, dont environ 60 % constituent une réserve pour les grandes révisions tous les 7 à 12 ans [DE:S1]. La disponibilité est d'environ 95 % la première année et passe à 97 à 98 % après trois ans [DE:S1].

## P.13 Exemple chiffré de Kasiri

**Vérification de la puissance.** Avec les valeurs du cas :

> P = ρ × g × Q × H × η = 1 000 × 9,81 × 57 × 120 × 0,92 × 0,98 = 60,5 MW

La puissance hydraulique est de 67,1 MW, la puissance sur l'arbre de 61,7 MW et la puissance délivrée de 60,5 MW : la puissance nominale de 60 MW est donc cohérente. Deux remarques. D'abord, 0,92 est un rendement au point de dimensionnement ; à charge partielle, la courbe de la Francis baisse (P.4), de sorte que le modèle énergétique a besoin d'une courbe et non d'une constante. Ensuite, 0,98 pour l'alternateur et le transformateur réunis est optimiste : l'IFC situe le rendement du seul alternateur à environ 98 % au maximum au-dessus de 1 MW [DE:S1], et les pertes du transformateur s'y ajoutent. Le P50 d'environ 292 GWh rapporté à 60 MW × 8 760 h donne le facteur de charge du cas, 55,6 % (tableau N.2).

**Type de turbine.** Avec 120 m de chute nette et 57 m<sup>3</sup>/s (19 à 57 m<sup>3</sup>/s par groupe), Kasiri se situe dans la classe haute chute (plus de 100 m) et dans le domaine Francis de l'abaque hauteur de chute-débit de l'IFC, bien au-dessus du plafond de 30 m des bulbes et à des débits supérieurs au domaine Pelton [DE:S1]. Le rapport de dimensionnement Q<sub>d</sub>/Q<sub>av</sub> = 57/38 = 1,5 se situe au sommet de la fourchette de 1,0 à 1,5 des aménagements au fil de l'eau, et le facteur de charge de 56 % se trouve dans la fourchette de 40 à 70 % des aménagements au fil de l'eau [DE:S1].

**Vitesse spécifique.** Le cas retient deux groupes (chapitre 3). Les lignes à un et trois groupes, la fréquence du réseau (50 Hz) et les vitesses ci-dessous sont des hypothèses illustratives, utilisées pour montrer pourquoi deux groupes ont été retenus.


**Tableau P.4. Configurations illustratives des groupes de Kasiri (H = 120 m, η<sub>t</sub> = 0,92, 50 Hz)**
{: .cap}

| Groupes | Q par groupe (m<sup>3</sup>/s) | Puissance sur l'arbre par groupe (MW) | Vitesse (tr/min) | Paires de pôles | n<sub>s</sub> (kW) | n<sub>q</sub> | n<sub>QE</sub> |
|---|---|---|---|---|---|---|---|
| 1 | 57,0 | 61,7 | 214,3 | 14 | 134 | 44,6 | 0,134 |
| 2 | 28,5 | 30,9 | 300,0 | 10 | 133 | 44,2 | 0,133 |
| 2 | 28,5 | 30,9 | 333,3 | 9 | 147 | 49,1 | 0,148 |
| 3 | 19,0 | 20,6 | 375,0 | 8 | 135 | 45,1 | 0,136 |
| 3 | 19,0 | 20,6 | 428,6 | 7 | 155 | 51,5 | 0,155 |

*Note : H<sup>1.25</sup> = 397,2 ; H<sup>0.75</sup> = 36,3 ; (gH)<sup>0.75</sup> = 201,0. Les vitesses sont les paliers synchrones n = 3000/p.*

En maintenant la vitesse spécifique vers 134, passer d'un à trois groupes porte la vitesse de 214 à 375 tr/min et réduit la taille de chaque alternateur ; le palier de vitesse suivant augmente la vitesse spécifique de 11 à 15 %, ce qui économise sur le coût de l'alternateur mais exige un calage plus profond. Le fournisseur doit confirmer ce choix au regard de ses références et de ses essais sur modèle.

**Fonctionnement à faible débit.** Le débit turbinable disponible est le débit de la rivière diminué du débit réservé de 4 m<sup>3</sup>/s, plafonné à 57 m<sup>3</sup>/s.


**Tableau P.5. Mois sous le débit technique minimal, moyennes mensuelles de Kasiri (nombres de groupes illustratifs)**
{: .cap}

| Configuration | Débit d'équipement par groupe (m<sup>3</sup>/s) | Débit minimal, IFC 40 % (m<sup>3</sup>/s) | Mois en dessous (IFC) | Débit minimal, ESHA 50 % (m<sup>3</sup>/s) | Mois en dessous (ESHA) |
|---|---|---|---|---|---|
| 1 × Francis | 57,0 | 22,8 | janv., févr., sept. | 28,5 | janv., févr., mars, août, sept., oct. |
| 2 × Francis | 28,5 | 11,4 | aucun | 14,3 | aucun |
| 3 × Francis | 19,0 | 7,6 | aucun | 9,5 | aucun |

*Note : débits disponibles de janvier à décembre : 20, 16, 24, 48, 57, 54, 36, 24, 18, 26, 42, 32 m<sup>3</sup>/s. Les moyennes mensuelles masquent les étiages journaliers ; la courbe des débits classés journaliers doit donc confirmer le résultat.*

Un groupe unique serait arrêté trois à six mois pendant une année moyenne, ce qui est incompatible avec un facteur de charge de 56 %. Deux groupes éliminent le problème sur les moyennes mensuelles et permettent de placer les révisions en février ou en septembre ; trois groupes ajoutent une marge en année sèche (coefficient de variation de l'énergie de 0,15) moyennant un surcoût. Deux groupes constituent le cas de base naturel à tester.

**Sédiments et coût.** À 120 m de chute, le dessableur doit retenir les particules de plus de 0,2 mm [DE:S1], et la teneur en quartz doit être connue avant de spécifier le revêtement de la roue. Les équipements électromécaniques, à 33 millions USD, représentent 26 % des 127 millions USD de composants de base recensés (33 % avec les équipements hydromécaniques), dans la fourchette de 14,9 à 56,6 % de l'IFC [DE:S1], soit environ 550 USD par kW. La disponibilité de 0,95 correspond au chiffre de première année de l'IFC et reste prudente au regard des 97 à 98 % attendus après la troisième année [DE:S1].

## P.14 Tests de décision

1. L'étude de faisabilité place-t-elle le point hauteur de chute-débit sur un abaque de sélection et justifie-t-elle le type de turbine au regard de toute la courbe des débits classés, et pas seulement du point de dimensionnement ?
2. La hauteur de chute nette nominale est-elle indiquée au débit nominal, avec les pertes de charge et la courbe de tarage du niveau aval utilisées pour la calculer ?
3. Quelle courbe de rendement (du fournisseur ou d'une machine de référence) sous-tend l'estimation de l'énergie, et le rendement à charge partielle est-il appliqué tranche par tranche ?
4. Quel débit technique minimal (IFC 40 % ou ESHA 50 % pour une Francis) est retenu, et combien de jours par année moyenne et par année sèche chaque configuration de groupes serait-elle arrêtée ?
5. Quels nombre et vitesse de groupes sont proposés, et l'optimisation montre-t-elle le coût marginal de chaque groupe supplémentaire au regard de l'énergie et de la disponibilité gagnées ?
6. Quel calage sous le niveau aval minimal est proposé, quelle marge de sigma suppose-t-il, et le fournisseur l'a-t-il confirmé par des essais sur modèle ?
7. Quels sont la concentration en sédiments, la granulométrie et la teneur en quartz mesurées, quelle taille de particule le dessableur retiendra-t-il, et quels revêtement de roue et intervalle de réparation sont supposés dans les OPEX ?
8. L'analyse du régulateur et du circuit hydraulique montre-t-elle que le temps de démarrage de l'eau et la surpression lors d'un rejet de charge restent dans les limites de dimensionnement de la conduite forcée ?
9. Le gestionnaire du réseau a-t-il émis une offre de raccordement pour la ligne de 132 kV, et chaque clause du code de réseau est-elle rattachée à une spécification d'équipement et à un essai de mise en service ?
10. Qui supporte le risque d'énergie réputée livrée si la ligne ou les renforcements du réseau sont en retard ?
11. Les garanties du contrat d'équipements électromécaniques (puissance, rendement, surpression, survitesse) sont-elles assorties de pénalités forfaitaires (liquidated damages), et sont-elles vérifiées par un essai sur site selon la norme IEC 60041 ?
12. Les garanties prolongées des constructeurs sont-elles cédées au maître d'ouvrage, et les pièces de rechange (2,5 à 3,0 % du prix FOB) ainsi que la réserve pour grandes révisions sont-elles prévues au budget ?

# Annexe Q. Construction, mise en service, exploitation et maintenance

## Q.1 Objet et champ

La valeur d'un projet hydroélectrique se gagne ou se perd dans deux fenêtres : la construction, quand la centrale ne fait que consommer du capital, et la première décennie d'exploitation, quand surviennent les arrêts liés à l'apprentissage, les réclamations au titre des garanties et la première grande révision. Aucune recette n'entre avant la mise en service ; une construction plus courte raccourcit donc le délai de récupération [DE:S1]. Cette annexe donne à un comité les références nécessaires pour tester le programme d'un entrepreneur, un plan de mise en service et un budget d'exploitation et de maintenance (O&M). Quand les sources ne donnent pas de chiffre, elle expose la méthode.

## Q.2 Planification des travaux et chemin critique

La construction commence avant le premier coulage de béton. Les sites hydroélectriques sont souvent isolés, l'accès peut être difficile et la météo peut arrêter les travaux en saison des pluies : il faut donc construire les routes d'accès, les bureaux et le logement des ouvriers avant de commencer l'aménagement lui-même [DE:S1]. Le planning doit indiquer les durées, la marge pour aléas de chaque tâche, les jalons, les interdépendances, les responsabilités, le chemin critique et l'avancement par rapport au plan, ventilés par lot : accès ; barrage et dérivation ; canal d'amenée et conduite forcée ; centrale ; fabrication, transport et montage des équipements électromécaniques ; poste d'évacuation et raccordement au réseau ; mise en service [DE:S1].

Le chemin critique type décrit par le guide de l'IFC passe par les routes d'accès, la construction de la conduite forcée, le creusement des galeries, la fabrication des équipements électromécaniques et le raccordement au réseau, même si les éléments critiques varient d'un projet à l'autre [DE:S1]. Le montage électromécanique ne peut suivre que l'achèvement du génie civil de la centrale, et les équipements à long délai de livraison doivent être commandés à temps ; mais un équipement qui arrive trop tôt doit être stocké sur site, ce qui ajoute un risque [DE:S1]. La dérivation de la rivière est la charnière entre ces chaînes : les fondations du barrage et de la centrale ne peuvent être réalisées à sec qu'une fois la rivière dérivée et, sur les projets au fil de l'eau, les essais à sec doivent être achevés avant la mise en eau de la fouille et l'enlèvement des batardeaux (Q.6) [DE:S1]. Un programme qui montre la dérivation glissant au-delà d'une saison sèche sans montrer l'effet en cascade jusqu'à la fenêtre d'étiage suivante est incomplet.

L'absence de lignes de transport et de renforcements du réseau est souvent un obstacle majeur pour atteindre la date de mise en service commerciale (COD), et elle entraîne des réclamations au titre de l'énergie réputée livrée qui pèsent sur les acheteurs [HY-06].


**Tableau Q.1. Références de délais tirées des sources**
{: .cap}

| Poste | Référence | Source |
|---|---|---|
| Conception détaillée | Quelques mois (petite centrale) ; plus d'un an (grande centrale) | [DE:S1] |
| Appel d'offres et passation des contrats EPC, centrales moyennes et grandes | Jusqu'à 18 mois ; jusqu'à deux ans pour un appel d'offres BOO | [DE:S1] |
| Construction, petite centrale | 9 à 18 mois | [DE:S1] |
| Construction, centrales moyennes et grandes | Jusqu'à quatre ans | [DE:S1] |
| Observé : Nyamwamba II, 7,8 MW, Ouganda | Environ 29 mois, du début de la construction à la COD | [DE:S12] |
| Observé : Nachtigal, 420 MW, Cameroun | Construction sur cinq ans | [DE:S13] |
| Grande hydroélectricité, du lancement à la COD | En général 8 à 10 ans ou plus | [HY-06] |
| Dépassement de délai, classe de référence des grands barrages | Médiane 27 %, moyenne 44 % de la durée prévue | [HY-08] |
| Mise en service, une phase d'essais | Environ un mois chacune ; moins pour une petite centrale | [DE:S1] |
| Mise en service, deux groupes de 150 MW (équipements électromécaniques) | Environ sept mois dans le planning type de l'IFC | [DE:S1] |

*Note : Les données de dépassement HY-08 portent sur de grands barrages (245 projets dans 65 pays) ; elles forment une classe de référence, pas une distribution propre à l'Afrique ou aux centrales au fil de l'eau.*

Le profil de paiement fait partie de la planification. Le guide de l'IFC donne un échéancier de paiement EPC type : pour le génie civil, 10 % d'avance, 80 % sur jalons et 10 % à la remise des ouvrages ; pour l'électromécanique, 30 % d'avance, 50 % à la livraison des équipements et 20 % à la réception [DE:S1]. Les entrepreneurs ont tendance à charger les coûts sur les postes de livraison ; la ligne « mise en service » d'un bordereau de prix ne reflète donc pas le coût réel de la mise en service [DE:S1].

## Q.3 Méthodes de construction et risques associés

Le génie civil représente 50 % ou plus du coût du projet et c'est le bloc le moins prévisible, car il dépend de la géologie, des aléas naturels et de la météo [DE:S1]. Les parties prenantes classent les conditions géotechniques et sismiques au premier rang des risques techniques [HY-06].

Travaux souterrains. L'abattage à l'explosif est la méthode classique en roche dure ; les tunneliers (TBM) améliorent le rendement et posent le soutènement au fur et à mesure de l'avancement [DE:S1]. Une roche de mauvaise qualité entraîne des coûts élevés ; un géologue expérimenté doit donc évaluer le risque de chaque galerie au cas par cas [DE:S1]. L'ESHA documente une galerie creusée sous des colluvions hétérogènes, où les tunneliers n'étaient pas utilisables et où l'excavation a progressé mètre par mètre avec de petites charges et des injections, ainsi qu'une zone de faille qui a exigé un système de soutènement entièrement différent ; la lithologie le long du tracé détermine la méthode, et les failles majeures doivent être connues à l'avance [LIT:S6].

Ouvrages de surface et premier remplissage. L'ESHA rapporte le cas d'un canal sur grès altéré où le premier remplissage a saturé le versant et où un glissement de terrain a rompu la digue du réservoir [LIT:S6]. Le premier remplissage est un risque de construction, pas un événement d'exploitation.

Répartition du risque géologique. Les clauses de « conditions imprévues » sont source de litiges, et le transfert intégral du risque géologique est souvent refusé ou facturé cher ; les développeurs expérimentés conviennent d'un référentiel géotechnique (geotechnical baseline), assorti d'une formule de partage des coûts au-delà [LIT:S7]. Le contrat EPC clés en main transfère l'essentiel du risque, mais il coûte cher et peu d'entrepreneurs savent tout faire ; beaucoup de maîtres d'ouvrage divisent donc les travaux entre un contrat électromécanique avec un fournisseur de turbines, un contrat de génie civil (souvent avec des entreprises locales lorsque des règles de contenu local s'appliquent) et un contrat de transport d'électricité [LIT:S7]. Les conditions FIDIC sont la norme du marché : Silver Book (Livre argent) pour l'EPC clés en main, Yellow Book (Livre jaune) pour l'électromécanique et le transport, Red Book (Livre rouge) pour le génie civil [LIT:S7; DE:S1]. La division en lots transfère le risque d'interface au maître d'ouvrage, et le guide de l'IFC qualifie la gestion des interfaces de tâche exigeante, qui demande une ingénierie très expérimentée [DE:S1].

Provisions pour aléas. Dans l'échantillon de l'IFC, les estimations représentent en moyenne 9,1 % du coût total de la centrale, alors que la pratique du secteur retient 15 % sur le génie civil, 7,5 % à 10 % sur l'électromécanique et 7,5 % à 10 % sur le raccordement au réseau [DE:S1]. Les dépassements de coûts réels des grands barrages ont une médiane de 27 % et une moyenne de 96 % [HY-08].

## Q.4 Assurance qualité, supervision et suivi par les prêteurs

Trois intervenants contrôlent l'entrepreneur.

- L'ingénieur du maître d'ouvrage supervise l'entrepreneur EPC pour le compte du maître d'ouvrage et, en cas de passation par lots séparés, gère les interfaces entre lots et les spécifie dans la conception détaillée [DE:S1]. Dans le Silver Book de la FIDIC, le contrat ne prévoit pas d'« Ingénieur » indépendant : le maître d'ouvrage assume lui-même le rôle d'ingénierie [DE:S1].
- Le conseiller technique des prêteurs (ingénieur indépendant) examine l'étude de faisabilité et les projets de contrats pendant la due diligence (audit préalable), puis suit la construction pour le compte des prêteurs [DE:S1]. Le suivi s'appuie sur les rapports d'avancement et les visites de site, avec des revues trimestrielles ; les prêteurs peuvent aussi engager un ingénieur indépendant pour la mise en service [DE:S1].
- L'ingénieur de mise en service reçoit, avant tout essai de mise en service, l'ensemble des certificats de qualité, des procédures d'essai et des résultats des essais de montage [DE:S1].

La qualité de la construction et du montage est un risque technique majeur : les centrales sont des conceptions uniques, et résilier le contrat d'un entrepreneur défaillant coûte cher et prend du temps ; il faut donc une due diligence sur l'entrepreneur, des spécifications complètes, des garanties de performance et une supervision adéquate [HY-06]. Le guide de l'IFC ajoute que la conception doit être conforme aux normes nationales et, lorsque celles-ci sont muettes, aux manuels de l'USACE et aux bulletins de l'ICOLD (CIGB) [DE:S1].

Un rapport de suivi utile (format recommandé, non exigé par les sources) indique la marge sur le chemin critique, le coût restant à engager et les provisions pour aléas consommées, les terrains rencontrés par rapport au référentiel géotechnique, les non-conformités ouvertes, les résultats en matière de sécurité et sur le plan environnemental et social (E&S), ainsi que l'état des équipements à long délai de livraison.

## Q.5 Santé, sécurité et volet E&S pendant la construction

Le guide de l'IFC exige que la santé et la sécurité des personnes soient prises en compte en permanence pendant la construction et signale la santé et la sécurité des travailleurs comme un enjeu particulier en cas de travaux en souterrain, de même que le bruit, la poussière et les vibrations [DE:S1]. Selon les Principes de l'Équateur, les projets situés dans des pays non désignés, ce qui comprend toute l'Afrique subsaharienne, sont évalués au regard des normes de performance de l'IFC et des Directives environnementales, sanitaires et sécuritaires (EHS) du Groupe de la Banque mondiale [DE:S1; DE:S49]. Les règles environnementales imposées à l'entrepreneur, assorties de pénalités en cas de non-respect, doivent couvrir l'implantation des camps, l'extraction de graviers, l'élimination des déchets, la pollution des eaux et le comportement des travailleurs ; les impacts des routes d'accès peuvent dépasser ceux du réservoir [DE:S1].

Les sources ne donnent pas de référence de fréquence des accidents pour la construction hydroélectrique. Un comité doit demander le bilan d'accidents du travail de l'entrepreneur sur des travaux souterrains comparables.

## Q.6 Séquence et essais de mise en service

La mise en service teste la centrale « de l'eau jusqu'au réseau » et exige des compétences en génie civil, en mécanique et en électricité [DE:S1]. La séquence ci-dessous suit le guide de l'IFC.


**Tableau Q.2. Séquence de mise en service et principaux essais**
{: .cap}

| Phase | Conditions préalables | Principaux essais | Source |
|---|---|---|---|
| Essais à sec | Montage achevé ; avant la mise en eau de la retenue, le remplissage des ouvrages d'amenée ou (au fil de l'eau) la mise en eau de la fouille et l'enlèvement des batardeaux | Vitesses de manœuvre des vannes ; alignement et jeux des paliers ; essais d'étanchéité ; temps de manœuvre des directrices et des vannes ; séquences du régulateur avec signaux simulés ; isolement des enroulements et tenue diélectrique haute tension ; vérification des protections | [DE:S1] |
| Essais en eau, hydromécanique | Ouvrages de retenue inspectés ; mise en eau de la retenue et remplissage des ouvrages d'amenée planifiés avec surveillance des eaux souterraines, des fuites et des déformations | Fuites des vannes fermées ; essais de pression des galeries et des conduites forcées ; essais de débit des vannes de réglage (les essais de l'évacuateur de crues peuvent attendre la bonne saison) | [DE:S1] |
| Essais en marche à vide | Ouvrages d'amenée remplis | Séquences de démarrage et d'arrêt avec freinage ; première rotation avec essai de survitesse ; stabilisation de la température des paliers ; faux-rond de l'arbre et vibrations ; essais des protections et de l'excitation ; courbes de court-circuit et à vide ; synchronisation | [DE:S1] |
| Essais en charge | Poste d'évacuation et ligne testés et prêts | Déclenchements à 25, 50, 75, 100 et 110 % de la charge nominale ; capacité en puissance réactive ; stabilisateur de puissance ; courbe en V ; échauffement et puissance ; vibrations | [DE:S1] |
| Essais conjoints (plusieurs groupes) | Tous les groupes mis en service | Déclenchement simultané à pleine charge, avec contrôle des surpressions et des survitesses par rapport aux limites contractuelles ; répartition des puissances active et réactive | [DE:S1] |
| Essais de performance | Groupes de plus de 5 MW | Essai de réception sur site selon la norme CEI 60041 pour le rendement de la turbine et essai indiciel sur au moins une turbine ; pertes de l'alternateur sur au moins un alternateur | [DE:S1] |
| Marche d'essai et essai de fiabilité | Essais à l'achèvement réussis | Fonctionnement normal continu sur une plage de charges : 3 à 10 jours pour les petits projets, environ 30 jours par groupe pour les grands projets ; reprise intégrale si un défaut montre que la fiabilité n'est pas atteinte | [DE:S1] |

Trois points comptent pour un prêteur. D'abord, si les groupes sont identiques, les essais de performance ne portent normalement que sur un seul groupe, mais tout signe que les garanties ne seront pas tenues peut imposer des essais sur tous les groupes afin d'établir la base des pénalités forfaitaires (liquidated damages) [DE:S1]. Ensuite, l'essai indiciel mesure un rendement relatif ; sa valeur tient à son rôle de référence pour les essais indiciels ultérieurs, il faut donc l'enregistrer et le conserver. Enfin, les points de transfert entre entrepreneurs doivent être signés, par exemple la disponibilité de la ligne avant la synchronisation, et le gestionnaire du réseau, qui contrôle en général la ligne, doit être associé tôt [DE:S1].

## Q.7 Réception, garantie des défauts et garanties constructeur

Le certificat de réception libère en général l'entrepreneur EPC et déclenche le paiement final [DE:S1]. Le planning type de l'IFC prévoit un certificat de réception provisoire par groupe après son essai de fiabilité et un certificat de réception définitive après les essais conjoints [DE:S1].

Pendant la période de notification des défauts, par exemple 24 mois, l'entrepreneur doit revenir corriger les défauts constatés après la réception [LIT:S7]. Les maîtres d'ouvrage prudents vident et réinspectent les galeries pendant cette période, lient un jalon de paiement important ou une garantie bancaire à son expiration, et obtiennent le bénéfice des garanties plus longues des fabricants par cession, par garantie collatérale (collateral warranty) ou par un régime de garantie des défauts à plusieurs niveaux [LIT:S7].

## Q.8 Organisation et effectifs d'exploitation et de maintenance

Les sources décrivent trois modèles d'organisation.

- Exploitation par le maître d'ouvrage. Les grandes compagnies d'électricité disposent en général de leur propre division O&M [DE:S1]. Celles qui possèdent de nombreuses centrales les exploitent à distance depuis une salle de commande centrale, avec des « équipes volantes » pour la maintenance programmée et les dépannages [DE:S1].
- Exploitant O&M sous contrat. Les petits producteurs confient souvent ces tâches à des sociétés spécialisées en O&M ou aux fournisseurs d'équipements. Le contrat doit obliger l'exploitant à respecter les obligations du maître d'ouvrage au titre du contrat d'achat d'électricité (CAE), en lui répercutant les responsabilités découlant du CAE et les pénalités de non-performance [DE:S1].
- Appui du fabricant. Présence du fournisseur sur site pendant la période de garantie pour les grands projets ; pour les petits projets, diagnostic et réglage des paramètres à distance grâce à des systèmes de contrôle-commande numériques [DE:S1].

Le futur personnel doit être formé chez le fabricant et participer au montage et à la mise en service [DE:S1]. Pour une centrale de 300 MW à deux groupes dans un pays à revenu intermédiaire, le guide de l'IFC indique un effectif de 40 personnes, dont 14 opérateurs postés ; dans un pays en développement à fort chômage, trois à dix fois plus [DE:S1].

## Q.9 Régime de maintenance, intervalles et durées de vie des composants

La maintenance préventive (programmée) reste le cœur de la plupart des programmes ; la maintenance basée sur la fiabilité ne doit jamais devenir un substitut destiné à réduire les coûts ; la maintenance conditionnelle (prédictive), qui surveille la température, les vibrations et les gaz dissous, ne convient pas comme régime unique. La pratique recommandée combine ces approches, en utilisant les constats relevés à chaque démontage pour ajuster les intervalles [DE:S1]. Il faut limiter le nombre de démarrages et d'arrêts pour prolonger la durée de vie, et caler l'achat des pièces de rechange sur la consommation réelle [DE:S1].

Les tâches courantes comprennent les essais des vannes, l'auscultation du barrage, l'inspection des ouvrages d'amenée, la réparation de la cavitation des roues, le suivi de l'envasement et l'analyse de l'huile des transformateurs [DE:S1].


**Tableau Q.3. Durées de vie des composants et intervalles de maintenance**
{: .cap}

| Poste | Valeur | Source |
|---|---|---|
| Durée de vie économique de la centrale, avec réhabilitation | 70 à 100 ans | [DE:S1] |
| Principaux équipements de production (turbine hors roue, alternateur, régulateur, excitation, vannes d'entrée) | 40 ans | [DE:S1] |
| Roues de turbine | 10 ans | [DE:S1] |
| Transformateurs de puissance ; appareillage HT et poste d'évacuation | 40 ans | [DE:S1] |
| Appareillage MT et BT ; auxiliaires de la centrale | 30 ans | [DE:S1] |
| Contrôle-commande, protections, SCADA, télécommunications, comptage | 20 ans | [DE:S1] |
| Conduites forcées, vannes, batardeaux à poutrelles, grilles ; lignes de transport | 70 ans | [DE:S1] |
| Grande révision des groupes de production | Tous les 7 à 12 ans ; 4 à 6 semaines pour les groupes de plus de 20 MW, 1 à 3 semaines sous 5 MW | [DE:S1] |
| Grande réhabilitation et modernisation de l'électromécanique | En général à 45 à 60 ans d'âge de la centrale | [HY-06] |

*Note : Les durées de vie de l'IFC sont des moyennes en conditions normales ; la charge sédimentaire, la qualité de l'eau, le climat et le nombre de démarrages les modifient [DE:S1].*

Coût d'O&M. Le coût annuel d'O&M est cité entre 1,0 % et 4,0 % de l'investissement ; l'AIE retient 2,2 % pour les grandes centrales et, en incluant le remplacement des gros équipements électromécaniques, l'IFC indique environ 45 USD/kW/an pour les grandes centrales et 52 USD/kW/an pour les petites [DE:S1]. L'échantillon de l'IRENA donne 1 % à 3 % du coût total installé, avec une moyenne légèrement inférieure à 2 % [HY-01]. Le guide de l'IFC détaille ce coût : maintenance électromécanique à 2,0 % à 2,5 % de l'investissement électromécanique initial, dont environ 40 % pour l'entretien courant, les pièces de rechange et les services et environ 60 % pour un fonds de réserve destiné aux gros travaux tous les 7 à 12 ans ; maintenance du génie civil à 0,4 % à 0,6 % du coût du génie civil ; et un stock de pièces de rechange représentant 2,5 % à 3,0 % du prix FOB des équipements [DE:S1]. Les charges d'exploitation (OPEX) comprennent aussi les assurances et, dans certains pays, les redevances de concession et d'eau [DE:S1].

## Q.10 Suivi des performances

La disponibilité se définit sur une période ; les formules ci-dessous sont les définitions usuelles.

> A = (T − SO<sub>h</sub> − FO<sub>h</sub>) / T

> FOR = FO<sub>h</sub> / (FO<sub>h</sub> + S<sub>h</sub>)

> η = P / (ρ g Q H)

où T est le nombre d'heures de la période, SO<sub>h</sub> les heures d'arrêt programmé, FO<sub>h</sub> les heures d'arrêt fortuit, S<sub>h</sub> les heures de fonctionnement, P la puissance électrique ou sur l'arbre, Q le débit et H la hauteur de chute nette. Le guide de l'IFC donne une trajectoire type : environ 95 % de disponibilité la première année (18 jours d'indisponibilité, dont 11 jours d'arrêt programmé et 7 jours d'arrêt fortuit), puis 97 % à 98 % après trois ans (4 à 6 jours d'arrêt programmé, 3 à 5 jours d'arrêt fortuit) [DE:S1]. La disponibilité exigée est en général fixée dans le CAE [DE:S1]. La dégradation du rendement se suit en répétant les essais indiciels par rapport à la référence établie à la mise en service. Les centrales doivent tenir des rapports d'événements et d'incidents pour détecter les faiblesses des équipements et doivent souvent enregistrer les débits et les niveaux chaque jour ou chaque heure en application du permis d'utilisation de l'eau [DE:S1].

## Q.11 Assurances

Le guide de l'IFC distingue les assurances avant achèvement (risques de construction, risques environnementaux et politiques) des assurances après achèvement (défaillances d'exploitation, risques environnementaux, politiques, de non-paiement et de transfert), et note que les assurances de construction obligatoires sont en général exigées [DE:S1]. L'assurance contre le risque politique est généralement accessible aux fonds propres comme à la dette lorsqu'une couverture de bonne qualité de crédit est nécessaire [LIT:S7]. Les assurances météorologiques paramétriques et les couvertures hydrologiques sont encore peu déployées en Afrique ; elles restent difficiles à placer et coûteuses, faute de profondeur des marchés locaux des capitaux et de l'assurance [LIT:S7]. Les sources ne donnent aucun taux de prime ; un comité doit demander les taux cotés, les franchises et le traitement des ouvrages souterrains.

## Q.12 Réhabilitation et fin de concession

Dans une concession BOT, l'installation est transférée à l'autorité publique à la fin de la période sans autre paiement [DE:S1]. Nachtigal est développé en BOT, avec transfert à l'État camerounais après 35 ans [LIT:S7]. Comme les principaux équipements durent environ 40 ans [DE:S1], l'état des ouvrages au transfert est un point de négociation ; les sources ne fixent aucun essai de restitution. La méthode consiste à définir dans la concession des critères minimaux de durée de vie résiduelle ou d'état par classe de composants (tableau Q.3), une inspection conjointe finale incluant la vidange des ouvrages d'amenée, et une réserve de restitution alimentée au cours des dernières années.

En Afrique, la réhabilitation est un marché important en soi : 60 % des installations examinées ont un besoin de réhabilitation élevé ou moyen, pour un total de 6,8 milliards USD et 14,7 GW [HY-06]. La réhabilitation est moins risquée qu'un projet nouveau, mais l'incertitude sur la propriété, la valorisation et les tarifs a limité la participation privée [HY-06].

## Q.13 Illustration Kasiri

Valeurs du cas : 60 MW, construction en trois ans, exploitation sur 25 ans, coût de la centrale d'environ 157 millions USD (génie civil 68, hydromécanique 9, électromécanique 33), provisions pour aléas de 10 %, disponibilité de 0,95, P50 d'environ 292 GWh/an. Vérification : P = 1 000 × 9,81 × 57 × 120 × 0,92 × 0,98 ≈ 60,5 MW, ce qui concorde avec la puissance nominale.


**Tableau Q.4. Contrôles de construction et d'O&M de Kasiri à partir des références des sources**
{: .cap}

| Contrôle | Calcul | Résultat |
|---|---|---|
| Délai par rapport à la classe de référence | 36 mois × 1,27 (médiane) et × 1,44 (moyenne) [HY-08] | Environ 46 et 52 mois |
| Provisions pour aléas selon la pratique du secteur | 15 % × 68 + (7,5 % à 10 %) × (9 + 33) [DE:S1] | 13,4 à 14,4 M USD, soit environ 12 % à 13 % de ces postes ; le cas applique 10 % à un sous-total de 142,6 M USD qui inclut les coûts de développement et la prime de l'entrepreneur (14,3 M USD) |
| Avances EPC | 10 % × 68 génie civil ; 30 % × 42 hydromécanique et électromécanique [DE:S1] | 6,8 M USD et 12,6 M USD |
| Budget de maintenance électromécanique | 2,0 % à 2,5 % × 42 [DE:S1] | 0,84 à 1,05 M USD/an, dont environ 60 % pour la réserve de grande révision |
| Maintenance du génie civil | 0,4 % à 0,6 % × 68 [DE:S1] | 0,27 à 0,41 M USD/an |
| Recoupement du coût total d'O&M | 45 USD/kW/an × 60 000 kW [DE:S1] | 2,7 M USD/an, soit environ 1,7 % du coût de la centrale |
| Grandes révisions sur 25 ans | Cycle de 7 à 12 ans [DE:S1] | Deux à trois par groupe |
| Renouvellement des roues et du contrôle-commande | Durées de vie de 10 et 20 ans [DE:S1] | Roues vers les années 10 et 20 ; contrôle-commande vers l'année 20 |
| Disponibilité | Cas à 0,95 contre 95 % en année 1 et 97 % à 98 % ensuite selon l'IFC [DE:S1] | Prudent après l'année 3 |

*Note : L'application du pourcentage électromécanique de l'IFC au coût hydromécanique comme au coût électromécanique est une hypothèse de l'analyste.*

Chaque point de disponibilité vaut environ 292 / 0,95 × 0,01 ≈ 3,1 GWh/an si les arrêts se répartissaient uniformément sur l'année. Ce n'est pas forcément le cas. Le débit utilisable en février est de 20 moins 4 = 16 m³/s, soit 28 % du débit nominal. Dans le cas de base à deux groupes de l'annexe P (28,5 m³/s chacun, ce qui n'est pas une donnée du cas), un seul groupe peut turbiner tout le débit utilisable de février tout en restant au-dessus de son minimum de 40 %, soit 11,4 m³/s ; une révision de l'autre groupe à ce moment-là ne fait donc perdre presque aucune énergie, sous réserve du rendement à charge partielle. Le plan d'O&M doit donc placer les révisions pendant les mois de plus faible débit (février, septembre et janvier), et le modèle ne doit pas déduire les arrêts programmés au prorata.

## Q.14 Tests de décision

1. Le programme de référence montre-t-il le chemin critique à travers les accès, la dérivation, le creusement des galeries, la centrale, la livraison des équipements électromécaniques et le raccordement au réseau, avec la marge indiquée pour chacun, et résiste-t-il à un dépassement de délai de 27 % dans le dimensionnement de la dette ?
2. La dérivation est-elle calée sur une saison sèche précise, et quel retard entraîne la perte de cette fenêtre ?
3. Comment le risque géologique est-il réparti : référentiel géotechnique avec formule de partage, risque entièrement à la charge de l'entrepreneur ou réclamations pour « conditions imprévues », et que comprend le prix à ce titre ?
4. Les provisions pour aléas sur le génie civil atteignent-elles au moins 15 %, ou un chiffre inférieur est-il justifié par des reconnaissances souterraines achevées ?
5. Qui gère les interfaces entre lots, et combien d'ingénieurs ayant une expérience comparable des travaux souterrains et de l'électromécanique compte l'équipe de l'ingénieur du maître d'ouvrage ?
6. Sur quoi portent les rapports du conseiller technique des prêteurs, à quelle fréquence, et qui les reçoit ?
7. Le plan de mise en service prévoit-il un essai sur site selon la norme CEI 60041 et l'enregistrement d'une référence d'essai indiciel, et des pénalités forfaitaires s'appliquent-elles au rendement et à la puissance mesurés ?
8. L'essai de fiabilité est-il défini en jours par groupe, avec reprise intégrale en cas d'échec, et lié à la réception provisoire ?
9. Une inspection des galeries vidées est-elle prévue pendant la période de notification des défauts, alors qu'un jalon de paiement ou une garantie est encore détenu, et les garanties des fabricants sont-elles cédées au maître d'ouvrage ?
10. Qui exploitera la centrale, quels sont son plan d'effectifs et son programme de formation, et les obligations de disponibilité du CAE sont-elles répercutées sur l'exploitant O&M avec des pénalités ?
11. Existe-t-il une réserve de gros entretien alimentée, dimensionnée pour des grandes révisions tous les 7 à 12 ans et pour le renouvellement des roues et du contrôle-commande ?
12. Dans le cas d'une concession, quels critères d'état et de durée de vie résiduelle s'appliquent à la restitution, et qui paie les travaux nécessaires pour les satisfaire ?

# Annexe R. Due diligence environnementale, sociale et climatique

## R.1 Pourquoi le risque E&S est un risque de crédit

Les prêteurs traitent la performance environnementale et sociale (E&S) comme une condition du prêt. Dans les opérations soumises aux Principes de l'Équateur, l'emprunteur s'engage par covenant à mettre en œuvre des actions E&S déterminées ; tout manquement constitue un cas de défaut qui permet au prêteur d'agir, jusqu'à annuler le prêt et exiger son remboursement [DE:S1]. Les acteurs privés de la grande hydroélectricité placent le risque de réinstallation et le risque lié à la biodiversité parmi les principaux freins à l'investissement, et privilégient les projets qui impliquent peu de réinstallation, bénéficient du soutien des communautés et respectent les normes de l'IFC [HY-06]. Le choix du site est le premier déterminant du risque E&S : sur un site inadapté, aucune mesure d'atténuation ne peut rétablir l'équilibre entre coûts et avantages [DE:S1]. La due diligence (audit préalable) commence donc dès la phase de sélection, et non une fois la conception arrêtée.

## R.2 Le cadre des normes appliquées par les prêteurs

**Droit national.** Le permis environnemental dépend normalement d'une étude d'impact environnemental et social (EIES) approuvée et impose des obligations d'atténuation, de suivi et de rapport pendant toute la durée de vie du projet [DE:S1]. Le permis peut devenir caduc si les travaux ne démarrent pas à temps (un an en Jordanie, dans l'exemple du guide de l'IFC), et des redevances s'appliquent ; au Mozambique, elles s'élevaient à 0,2 % du coût total du projet [DE:S1]. Une autorisation au titre du patrimoine, un permis d'utilisation de l'eau qui couvre aussi les conflits transfrontaliers et la confirmation que le site se trouve hors des aires protégées sont des autorisations connexes typiques [DE:S1].

**Normes de performance de l'IFC (2012).** Les huit normes de performance (NP) constituent de fait la référence E&S du secteur privé, ne comportent aucun seuil de taille et sont reprises de près par la Banque africaine de développement, la Banque européenne pour la reconstruction et le développement (BERD) et d'autres institutions multilatérales [DE:S1]. En Ouganda, le programme GET FiT a fait du respect des NP une condition d'éligibilité pour la petite hydroélectricité [DE:S9].

**Principes de l'Équateur.** La version EP4 est entrée en vigueur le 1er octobre 2020 et s'applique aux financements de projet dont le coût d'investissement total atteint ou dépasse 10 millions USD [DE:S49; DE:S50]. Dans les pays non désignés, qui comprennent toute l'Afrique subsaharienne, l'examen vérifie la conformité aux NP et aux Directives environnementales, sanitaires et sécuritaires (directives EHS) du Groupe de la Banque mondiale [DE:S1; DE:S49; DE:S50]. Le guide de l'IFC énumère les dix principes de la version EP III : catégorisation, évaluation, normes applicables, système de gestion et plan d'action, mobilisation des parties prenantes, mécanisme de gestion des plaintes, examen indépendant, covenants, suivi indépendant et rapports [DE:S1]. Les modifications apportées par EP4 doivent être vérifiées dans son texte ; les sources examinées ne les résument pas.

**Cadre de la Banque mondiale.** Lorsque la Banque mondiale prête ou accorde sa garantie, son propre cadre s'applique, y compris sa note de bonnes pratiques sur la sécurité des barrages [HY-15]. Le projet de Rusumo Falls, financé par l'Association internationale de développement (IDA), a fait l'objet d'une supervision fondée sur une notation des sauvegardes [A2:S16].

**Catégorisation.** FMO a classé Kikagati, en Ouganda, en catégorie A, et Siti et Nyamwamba en catégorie B+ [DE:S51; DE:S52; DE:S40b]. La puissance installée n'indique pas l'ampleur de l'impact [DE:S1] ; ce sont le tronçon court-circuité, l'emprise foncière et les habitats qui déterminent la catégorie.


**Tableau R.1. Normes de performance de l'IFC : enjeux hydroélectriques typiques et preuves demandées par les prêteurs**
{: .cap}

| Norme de performance | Enjeux hydroélectriques typiques | Preuves demandées par les prêteurs |
|---|---|---|
| NP 1 Évaluation et gestion | Zone d'influence ; impacts cumulés des autres centrales ; importance des émissions de gaz à effet de serre ; plans d'urgence [DE:S1] | EIES conforme aux NP et aux directives EHS ; système de gestion ; plan de gestion environnementale et sociale (PGES) et plans spécifiques ; évaluation des impacts cumulés ; plan de mobilisation des parties prenantes et mécanisme de gestion des plaintes [DE:S1] |
| NP 2 Main-d'œuvre | Effectifs importants, sécurité des travaux souterrains, camps, conditions des sous-traitants [DE:S1] | Politique de ressources humaines ; clauses E&S dans les contrats des entrepreneurs ; plan de sécurité des travaux souterrains ; mécanisme de plainte pour les travailleurs |
| NP 3 Prévention de la pollution | Déblais, ruissellement, bruit, poussière, vibrations, tirs de mines [DE:S1] | Plan de gestion des déblais et des déchets [DE:S1] ; état de référence de la qualité de l'eau ; plan de tirs |
| NP 4 Santé et sécurité des communautés | Sécurité du barrage, lâchers d'eau, noyades, maladies à transmission vectorielle, circulation [DE:S1] | Conception conforme aux bonnes pratiques, avec examen externe lorsque le risque est élevé [DE:S1] ; base de calcul de la crue de projet ; plan de préparation aux situations d'urgence ; panel d'experts sur la sécurité du barrage lorsqu'il est exigé [HY-15] |
| NP 5 Terres et réinstallation | Terres pour les ouvrages de tête, les routes, les carrières et la ligne ; régime foncier coutumier ; pertes de pêche, de cultures et de pâturages [DE:S1; LIT:S7] | PAR ou plan de restauration des moyens de subsistance ; recensement et date butoir ; matrice des droits ; budget ; audit d'achèvement |
| NP 6 Biodiversité | Conversion d'habitats, fragmentation de la rivière, migration des poissons, modification des débits, espèces menacées [DE:S1] | État de référence couvrant les saisons ; évaluation des habitats critiques ; étude du débit réservé ; plan de gestion de la biodiversité [DE:S1] ; conception de la compensation des pertes résiduelles |
| NP 7 Peuples autochtones | Groupes à l'identité distincte, utilisant les ressources selon la coutume [DE:S1] | Examen préalable ; compte rendu de consultations adaptées ; plan en faveur des peuples autochtones si la norme s'applique |
| NP 8 Patrimoine culturel | Sites archéologiques et sacrés dans les zones d'inondation ou de travaux [DE:S1] | Inventaire du patrimoine ; autorisation de l'administration compétente [DE:S1] ; procédure en cas de découverte fortuite |

*Note : Les éléments de preuve sans référence sont les produits habituels d'un examen au regard des NP, présentés sous forme de liste de contrôle.*

## R.3 L'EIES : démarche et périmètre

L'EIES commence dès le choix du site, oriente la conception au stade de la faisabilité et aboutit à un plan de gestion environnementale et sociale (PGES) composé de plans spécifiques, tels qu'un plan d'action de réinstallation (PAR), un plan biodiversité, un plan de gestion des déblais et un plan de mobilisation des parties prenantes [DE:S1]. L'étude de faisabilité doit présenter les résultats de l'EIES et les plans de gestion à côté du concept technique [DE:S1]. La logique est celle de la hiérarchie d'atténuation : éviter, réduire, puis indemniser ou compenser [DE:S1].

**Zone d'influence.** La NP 1 exige qu'elle soit définie [DE:S1]. Pour un aménagement en dérivation, elle couvre la retenue, les ouvrages de tête, le tronçon court-circuité, la rivière en aval du canal de fuite, les routes, les carrières, les zones de dépôt des déblais, les camps et le couloir de la ligne. Les routes d'accès peuvent avoir des impacts bien plus importants que le réservoir, les lignes fragmentent la forêt et tuent les grands oiseaux, et les carrières accroissent les surfaces perdues [DE:S1]. La ligne de 35 km et 132 kV de Kasiri se trouve dans la zone d'influence.

**Saisons de l'état de référence.** Les sources ne fixent aucune durée minimale. Le critère est de savoir si les inventaires couvrent les extrêmes de débit qui déterminent les impacts. Le débit moyen mensuel de Kasiri varie de 20 m³/s en février à 70 m³/s en mai (valeurs de l'étude de cas) ; un état de référence limité à une seule saison passerait à côté soit du stress lié aux étiages dans le tronçon court-circuité, soit des conditions de hautes eaux qui commandent les déplacements des poissons.

**Évaluation des impacts cumulés.** L'EIES du premier barrage sur une rivière doit évaluer tous les barrages projetés connus, et les mesures d'atténuation des impacts cumulés doivent être achevées ou bien avancées avant la construction du deuxième barrage [DE:S1]. Dans une cascade, chaque réservoir ne doit pas relever le niveau aval de la centrale située en amont [DE:S1]. Le rapport de la Banque mondiale propose que les institutions de financement du développement (IFD) aident les gouvernements à préparer des études de préfaisabilité comprenant des plans de gestion de bassin versant et des évaluations des impacts cumulés [HY-06].

## R.4 Principaux impacts de l'hydroélectricité

**Modification des débits.** La modification du régime en aval peut détruire les écosystèmes des plaines d'inondation, aggraver la pollution en période d'étiage et réduire les apports de sédiments et de nutriments [DE:S1] ; une dérivation peut laisser un tronçon presque à sec [DE:S1; LIT:S6]. Une exploitation en base reproduit plus facilement les débits naturels qu'une exploitation en pointe [DE:S1]. Les plans de gestion doivent préciser les lâchers environnementaux, y compris pour les barrages privés [DE:S1].

**Débits réservés.** Le débit résiduel, réservé ou de compensation est presque toujours une condition du permis ; trop faible, il nuit à la vie aquatique ; trop élevé, il réduit la production, surtout en période sèche [LIT:S6]. Sa détermination relève de spécialistes : comprendre la rivière, son écologie et les usages en aval, consulter les communautés qui en dépendent, définir les valeurs à protéger, choisir une méthode, puis assurer le suivi [DE:S1]. La courbe des débits classés et les statistiques d'étiage telles que le Q<sub>95</sub> fournissent la référence hydrologique [LIT:S6]. Le coût énergétique découle des données de l'étude de cas :

> E<sub>loss</sub> = ρ × g × H<sub>n</sub> × η<sub>t</sub> × η<sub>gt</sub> × A × Σ (Q<sub>e</sub> × h<sub>m</sub>), sur les mois où Q<sub>m</sub> < Q<sub>d</sub> + Q<sub>e</sub>

Avec H<sub>n</sub> = 120 m, η<sub>t</sub> = 0,92, η<sub>gt</sub> = 0,98 et A = 0,95, chaque m³/s représente environ 1,01 MW. Seul le débit moyen de mai (70 m³/s) dépasse Q<sub>d</sub> + Q<sub>e</sub> = 61 m³/s ; le lâcher coûte donc de l'énergie pendant onze mois, soit environ 8 016 heures.


**Tableau R.2. Débit réservé de Kasiri par mois (débits moyens de l'étude de cas)**
{: .cap}

| Mois | Débit moyen (m³/s) | Débit turbiné après un lâcher de 4 m³/s | Part du lâcher dans le débit |
|---|---|---|---|
| Janv. | 24 | 20 | 17 % |
| Févr. | 20 | 16 | 20 % |
| Mars | 28 | 24 | 14 % |
| Avr. | 52 | 48 | 8 % |
| Mai | 70 | 57 (9 déversés) | 6 % |
| Juin | 58 | 54 | 7 % |
| Juil. | 40 | 36 | 10 % |
| Août | 28 | 24 | 14 % |
| Sept. | 22 | 18 | 18 % |
| Oct. | 30 | 26 | 13 % |
| Nov. | 46 | 42 | 9 % |
| Déc. | 36 | 32 | 11 % |

*Note : Calculé à partir des valeurs de l'étude de cas ; les moyennes mensuelles masquent la variabilité journalière. La même méthode reproduit le P50 de l'étude de cas, d'environ 292 GWh/an.*

Le lâcher coûte environ 32 GWh/an, soit 11 % du P50. Chaque m³/s supplémentaire coûte environ 8 GWh/an (près de 3 % du P50), jusqu'à ce que le lâcher dépasse 13 m³/s et pèse aussi sur le mois de mai. Le lâcher représente 10,6 % du débit moyen, mais 17 à 20 % du débit pendant les mois les plus secs, où les écologues jugeront de son caractère suffisant.

**Passage des poissons.** Les barrages bloquent la migration vers l'amont, la dévalaison par les turbines et les évacuateurs échoue souvent, et les échelles à poissons, ascenseurs et dispositifs de capture et transport sont généralement d'une efficacité limitée [DE:S1]. Des turbines ichtyocompatibles font leur apparition [DE:S1] ; les prises d'eau doivent comporter des dispositifs de déviation des poissons et des passes lorsque c'est exigé [LIT:S6]. L'empoissonnement avec des espèces non indigènes n'est pas souhaitable [DE:S1].

**Sédiments.** La sédimentation réduit la capacité utile ; la gestion du bassin versant, les chasses, les ouvrages de retenue des sédiments et l'enlèvement mécanique sont les réponses possibles [DE:S1]. Les sédiments durs usent les turbines par abrasion [DE:S1]. À Rusumo, les sédiments et les matières organiques présents dans le circuit d'eau de refroidissement ont provoqué l'usure des joints d'arbre et des arrêts [A2:S16].

**Qualité de l'eau.** La mise en eau réduit l'oxygénation et la dilution, la biomasse inondée se décompose, et le manque d'oxygène ou la sursaturation en gaz tue les poissons ; le défrichement sélectif avant la mise en eau est la mesure d'atténuation habituelle [DE:S1].

**Gaz à effet de serre des réservoirs.** La biomasse inondée émet du dioxyde de carbone et du méthane. La plupart des aménagements hydroélectriques compensent largement ces émissions, mais certains réservoirs, comme celui de Balbina au Brésil, semblent émettre pendant de nombreuses années davantage qu'une production au gaz ; la meilleure mesure d'atténuation consiste à inonder peu de terres, surtout forestières [DE:S1]. La NP 1 exige d'évaluer l'importance de ces émissions [DE:S1], et les critères de la Climate Bonds Initiative exigent des infrastructures à faibles émissions de gaz à effet de serre [HY-06]. Les sources ne donnent aucun seuil ; pour un aménagement au fil de l'eau à faible capacité d'éclusée, l'enjeu est généralement mineur, mais l'EIES doit indiquer la surface inondée et la biomasse.

**Biodiversité et habitats critiques.** La forêt riveraine inondée a généralement plus de valeur que l'habitat aquatique créé [DE:S1]. La NP 6 interdit la conversion significative d'habitats naturels et critiques, sauf si des conditions précises sont remplies ; la création d'aires protégées compensatoires de taille et de qualité comparables est la compensation privilégiée, et le sauvetage de la faune réussit rarement [DE:S1].

## R.5 Acquisition de terres et réinstallation

Le déplacement involontaire est considéré comme l'impact social le plus négatif de l'hydroélectricité [DE:S1]. La NP 5 exige d'étudier des variantes de conception qui évitent ou réduisent les déplacements et vise à rétablir ou améliorer les moyens de subsistance ; les pertes économiques liées à la pêche, aux terres agricoles, aux pâturages ou à l'argile appellent des ressources de remplacement ou le rétablissement des revenus [DE:S1]. L'enregistrement foncier peut être incomplet et les terres peuvent relever du domaine de l'État ou du régime coutumier ; l'acquisition est donc négociée ou forcée ; les prêteurs veulent que l'engagement du gouvernement à procéder à l'expropriation, ainsi que la répartition du coût de la réinstallation, soient inscrits dans la convention de mise en œuvre [LIT:S7]. La propriété coutumière est souvent contestée et les droits sont difficiles à établir [HY-06].

La réinstallation est un risque de coût et de calendrier. À Rusumo Falls, les programmes de restauration des moyens de subsistance et de développement local sont passés de 18 millions USD à environ 38 millions USD, soit plus du double ; après des dégâts causés par les tirs de mines, 580 bâtiments en Tanzanie ont dû être réparés ; 80 ménages au Rwanda ont dû être réinstallés, la décision n'ayant été prise qu'en 2023 ; et la date de clôture a été repoussée de décembre 2020 à juin 2025 au fil de trois restructurations [A2:S16]. Ce retard n'était pas entièrement d'origine E&S, mais le cas montre un poste foncier qui double sur le chemin critique. Le PAR doit comporter un recensement et une date butoir, une matrice des droits, un budget doté de ses propres provisions pour aléas et un calendrier lié aux dates de mise à disposition des terrains à l'entrepreneur, car tout retard de mise à disposition se transforme en réclamation.

## R.6 Peuples autochtones et patrimoine culturel

La NP 7 exige le plein respect des droits, des moyens de subsistance et de la culture des peuples autochtones, en tenant compte de leur statut juridique et économique souvent marginal [DE:S1]. Le résumé du guide de l'IFC ne détaille pas les conditions de consentement de la NP 7 ; le comité doit donc demander si l'examen préalable a identifié des peuples autochtones et quelles exigences de la NP 7 s'appliquent. Au titre de la NP 8, les objets patrimoniaux peuvent être sauvegardés, mais les sites sacrés ne peuvent généralement pas être remplacés [DE:S1]. De nombreux pays exigent une autorisation au titre du patrimoine pour les terrains [DE:S1] ; une procédure en cas de découverte fortuite doit figurer dans le contrat de construction.

## R.7 Santé et sécurité des communautés et sécurité des barrages

La NP 4 exige que la conception, la construction et l'exploitation respectent les bonnes pratiques internationales et soient confiées à des professionnels compétents, avec un examen externe dans les cas à risque élevé [DE:S1]. Le guide de l'IFC distingue la crue de projet pour l'exploitation normale, définie par une période de retour, par exemple 100 ans, et fixée par la réglementation nationale selon la classe de danger, de la crue de projet maximale à laquelle les ouvrages doivent résister, à savoir la crue maximale probable ou la crue décamillénale [DE:S1]. La note de la Banque mondiale sur la sécurité des barrages est accompagnée de notes techniques sur les risques hydrologiques et sismiques [HY-15; R4:S1]. Les autres risques sont la noyade, qui impose un contrôle des accès, et les maladies liées à l'eau, comme le paludisme et la schistosomiase autour des réservoirs en climat chaud [DE:S1]. La NP 1 exige des plans d'urgence [DE:S1] ; pour un barrage, cela signifie un plan de préparation aux situations d'urgence testé à l'intention des communautés en aval.

## R.8 Mobilisation des parties prenantes et gestion des plaintes

La NP 1 exige la mobilisation des parties prenantes, la diffusion d'informations et un mécanisme de gestion des plaintes, et les Principes de l'Équateur traitent la mobilisation et la gestion des plaintes comme des principes distincts [DE:S1]. Même les petits projets se heurtent à la méfiance locale, et la communication doit être assurée de la conception à la mise en service [DE:S1]. Le partage des avantages par le contenu local, une contribution sur les recettes telle qu'une redevance sur l'eau, ou un partage des bénéfices peut réduire l'opposition [LIT:S7]. Le comité doit demander le registre des plaintes : nombre, catégories, délai de traitement et dossiers en cours.

## R.9 Cours d'eau transfrontaliers

L'utilisation de l'eau relève de la souveraineté lorsque les cours d'eau franchissent des frontières, comme le montre le différend autour du Grand barrage de la Renaissance éthiopienne ; des traités comme celui qui fonde la Zambezi River Authority organisent la coopération et le règlement des différends [LIT:S7]. Le gouvernement hôte peut devoir adhérer à des accords internationaux [HY-06], et le permis d'utilisation de l'eau couvre les conflits transfrontaliers [DE:S1]. Rusumo, situé sur une rivière frontalière, est détenu à parts égales par trois États [A2:S16]. Les prêteurs multilatéraux appliquent leurs propres procédures relatives aux voies d'eau internationales ; les sources ne les décrivent pas ; il faut donc obtenir l'exigence par écrit et inscrire au calendrier toute notification aux États riverains.

## R.10 Outils de durabilité et labels verts

Les Hydropower Sustainability Tools (outils de durabilité de l'hydroélectricité) comprennent les lignes directrices de bonnes pratiques, le protocole d'évaluation (HSAP) et l'outil d'analyse des écarts ESG (HESG), et couvrent plus de 20 thèmes ; un examen HESG a établi que l'aménagement de Dibwangui, au Gabon, satisfaisait à 11 des 12 critères de bonnes pratiques [LIT:S7]. La Hydropower Sustainability Standard délivre des certifications de niveau Bronze, Argent et Or [HY-03]. Un indice d'obligations vertes n'admet la grande hydroélectricité qu'avec un score HSAP d'au moins 3 ou un engagement à respecter les huit NP [HY-06]. Une analyse des écarts menée par anticipation est un moyen peu coûteux de repérer les faiblesses avant les prêteurs.

## R.11 Résilience climatique et examen préalable

Le changement climatique peut entraîner d'importantes modifications régionales du volume et de la saisonnalité des débits ; cette incertitude échappe au contrôle du développeur mais peut être simulée [DE:S1]. En 2015, une sécheresse à Kariba a provoqué des délestages en Zambie [LIT:S7], et en 2024 l'allocation d'eau pour la production de Kariba a été réduite d'environ 47 %, de 30 à 16 milliards de m³ [CL-04]. Les barrages projetés concentreraient la capacité régionale dans un petit nombre de bassins, ce qui accroît le risque de déficits simultanés [CL-03]. Des méthodes existent : un examen préalable et un test de résistance en six phases [CL-01], des études de revenus à l'échelle des bassins pour les fleuves africains [CL-02] et l'allocation contractuelle des risques hydrologique et de crue [CL-06]. Le risque hydrologique transféré à l'État devient un passif éventuel [HY-06].

Pour Kasiri, appliquer un coefficient de 0,9 à chaque débit moyen mensuel, avec un lâcher maintenu à 4 m³/s, réduit l'énergie modélisée d'environ 10 %, à quelque 264 GWh/an ; en février, le lâcher représenterait alors 22 % du débit. Le scénario à 10 % est une valeur de test choisie par l'analyste, non une projection. La série de 12 ans est plus courte que les 15 ans attendus par le guide de l'IFC [DE:S1], ce qui élargit l'incertitude avant tout ajustement climatique. L'examen préalable doit aussi recalculer les crues de projet pour des précipitations extrêmes plus fortes et indiquer la capacité de l'évacuateur de crues et la revanche.

## R.12 Plan d'action E&S et covenants

L'examen des prêteurs aboutit à un plan d'action environnemental et social (PAES) : pour chaque écart par rapport aux NP, l'action, le responsable, l'échéance et la preuve d'achèvement. Le plan d'action, l'examen indépendant, les covenants et le suivi sont des Principes de l'Équateur distincts [DE:S1]. Le guide de l'IFC recommande des résultats vérifiables, des plans de travail et des budgets annuels, et avertit que les retards peuvent compromettre la capacité d'une société à tenir ses engagements E&S [DE:S1].


**Tableau R.3. Place des exigences E&S dans les documents de financement**
{: .cap}

| Étape | Exigence typique | Points à vérifier |
|---|---|---|
| Conditions suspensives | Permis issu de l'EIES ; PAES convenu ; PAR approuvé ; terrains des travaux préliminaires sécurisés ; personnel E&S en place | Date d'expiration du permis ; état d'avancement du PAES ; dates de mise à disposition des terrains au regard du programme de l'entrepreneur |
| Construction | PGES et PAES respectés dans les délais ; obligations de l'entrepreneur ; suivi indépendant | Clauses des contrats des entrepreneurs ; fréquence des rapports ; budget du conseiller |
| Avant la mise en eau ou la date de mise en service commerciale (COD) | PAR mis en œuvre ; ouvrage de restitution du débit réservé et station de jaugeage installés ; plan d'urgence testé ; examen de la sécurité du barrage | Audit d'achèvement ; enregistrement des données de débit réservé ; compte rendu des exercices |
| Exploitation | Respect du débit réservé ; mécanisme de gestion des plaintes ; rapport E&S annuel ; notification des incidents | Historique de conformité ; statistiques des plaintes |

*Note : La séquence suit les Principes de l'Équateur tels que décrits dans le guide de l'IFC [DE:S1] ; les éléments constituent une liste de contrôle et non des citations d'une convention de prêt.*

Les échéances du PAES qui dépendent d'une action de l'État, comme l'acquisition des terres, doivent avoir pour pendant des engagements de l'État dans la convention de mise en œuvre [LIT:S7].

## R.13 Coûts et calendrier E&S

Kasiri prévoit 5 millions USD pour les mesures E&S dans un coût de centrale d'environ 157 millions USD (valeurs de l'étude de cas), soit environ 3,2 %. Ce poste doit être construit à partir du PGES et du PAR : terres et indemnisation, restauration des moyens de subsistance, ouvrage de restitution du débit réservé et suivi, mesures en faveur des poissons, biodiversité, sécurité des communautés, équipe E&S et conseiller des prêteurs. Les coûts d'études relèvent des coûts de développement ; à titre de points de repère isolés, l'étude de faisabilité et l'EIES du projet Kakono de 53 MW et de sa ligne ont coûté environ 4,8 millions USD [DE:S16], et un don de préparation de 992 000 USD, EIES comprise, a été accordé pour un aménagement hydroélectrique communautaire de 7,8 MW au Kenya [DE:S17].

Si le poste E&S de Kasiri doublait, comme les programmes de subsistance de Rusumo [A2:S16], les 5 millions USD supplémentaires représenteraient environ 3 % du coût de la centrale et absorberaient une partie des provisions pour aléas de 10 %. Le risque de calendrier peut dépasser le risque de coût : une saison d'inventaire manquée, un PAR tardif, une plainte non résolue ou un différend sur le débit réservé peut retarder le bouclage financier ou l'accès au site, et un permis caduc doit être renouvelé [DE:S1]. Le calendrier doit faire apparaître les périodes d'inventaire, les délais de diffusion publique, la délivrance du permis, la mise en œuvre du PAR et l'examen des prêteurs comme des tâches liées, avec leur marge.

## R.14 Questions de décision

1. Quelle catégorie E&S chaque prêteur a-t-il attribuée, et le périmètre de l'EIES y correspond-il ?
2. La zone d'influence inclut-elle le tronçon court-circuité, les routes, les carrières, les camps et la ligne de 35 km, chacun avec des données de référence ?
3. Les inventaires de l'état de référence ont-ils couvert à la fois les mois d'étiage (janvier à mars, septembre) et les mois de hautes eaux (avril à juin) ?
4. Le débit réservé de 4 m³/s est-il fixé dans le permis d'utilisation de l'eau, par quelle méthode a-t-il été déterminé, et le modèle montre-t-il une perte d'environ 8 GWh/an par m³/s supplémentaire ?
5. D'autres centrales existent-elles ou sont-elles prévues sur la rivière, et une évaluation des impacts cumulés a-t-elle été réalisée ?
6. Combien de ménages sont déplacés physiquement ou économiquement, et le budget du PAR est-il construit à partir du recensement, avec ses propres provisions pour aléas ?
7. Le gouvernement s'est-il engagé à recourir à l'expropriation si nécessaire, et qui supporte les dépassements du coût de la réinstallation ?
8. Qu'a révélé l'examen préalable concernant les peuples autochtones, les habitats critiques et le patrimoine culturel ?
9. Quelles crues de projet ont été retenues, un examinateur indépendant les a-t-il acceptées, et existe-t-il un plan de préparation aux situations d'urgence testé ?
10. La rivière est-elle transfrontalière, et les démarches de notification ou au titre des traités figurent-elles au calendrier ?
11. Quels sont l'énergie P50 et le ratio de couverture du service de la dette (DSCR) minimum dans l'hypothèse d'une baisse des débits de 10 % ?
12. Quels éléments du PAES sont des conditions suspensives, lesquels dépendent d'une action de l'État, et leurs échéances sont-elles réalistes ?