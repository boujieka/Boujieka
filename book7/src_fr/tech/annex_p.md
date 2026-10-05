## Annexe P. Équipements électromécaniques et raccordement au réseau

### P.1 Objet et champ

Le lot électromécanique transforme la hauteur de chute et le débit en énergie vendable : turbines, alternateurs, régulateurs de vitesse et systèmes d'excitation, transformateurs, poste d'évacuation, protections, SCADA, auxiliaires, ainsi que les vannes et organes hydromécaniques qui commandent l'arrivée d'eau aux groupes. Dans chaque grande centrale, les équipements électromécaniques sont conçus sur mesure [DE:S1]. Dans l'échantillon de référence de l'IFC, les équipements électromécaniques représentent en moyenne 30,3 % du coût total de la centrale (médiane 29,2 %), dans une fourchette de 14,9 à 56,6 % [DE:S1]. Les décisions qu'un comité doit tester sont peu nombreuses : le type de turbine, le nombre et la vitesse des groupes, le calage de la turbine, la protection contre les sédiments, et le régime contractuel et d'essais qui rend les garanties des fournisseurs opposables.

### P.2 Types de turbines et choix selon la hauteur de chute et le débit

Le choix de la turbine repose sur la hauteur de chute et le débit du site, y compris la fréquence à laquelle la turbine fonctionnera à charge partielle parce que le débit disponible est inférieur au débit d'équipement [DE:S1]. Les turbines se répartissent en deux familles [DE:S1] :

- **Turbines à action** (Pelton, Turgo, Banki) : la roue tourne dans l'air sous un ou plusieurs jets. Elles conservent leur rendement lorsque le débit fluctue, évitent les surpressions dans la conduite forcée, maîtrisent facilement la survitesse et sont faciles à entretenir.
- **Turbines à réaction** (Francis, hélice, Kaplan, bulbe) : la roue est noyée dans une enveloppe sous pression et entraînée par la portance ; un aspirateur récupère la chute sous la roue. Leurs roues sont plus petites et plus rapides que celles des Pelton, peuvent fonctionner noyées et offrent un meilleur rendement aux fortes puissances.

Le guide de l'IFC classe les aménagements en haute chute au-dessus de 100 m, moyenne chute de 30 à 100 m et basse chute en dessous de 30 m [DE:S1]. Sa section consacrée aux turbines retient une autre limite pour la basse chute (moins de 10 m) et comporte une coquille sur la plage moyenne (« 50 m < H < 10 m ») ; il faut donc citer les classes d'aménagement [DE:S1]. L'abaque hauteur de chute-débit du guide (figure 4-19, en axes logarithmiques de 1 à 1000 m de chute et de 1 à 1000 m^3^/s de débit) place, autant qu'on puisse le lire, les Pelton et Turgo en haute chute et faible débit, les Kaplan en basse chute et fort débit, les Banki en basse à moyenne chute et faible débit, et les Francis sur le vaste domaine intermédiaire ; les limites dépendent de la conception de chaque constructeur [DE:S1].

Table: Tableau P.1. Types de turbines : principe, domaine d'emploi et comportement à charge partielle
| Type | Principe | Domaine d'emploi selon les sources | Caractéristiques utiles pour un comité |
|---|---|---|---|
| Pelton | Action ; augets à double cuillère, un ou plusieurs injecteurs à pointeau | Haute chute, faible débit ; turbine à action la plus répandue [DE:S1] | Jusqu'à 2 injecteurs (axe horizontal) ou 6 (axe vertical) ; le déflecteur limite la survitesse lors d'un rejet de charge [DE:S1] |
| Turgo | Action ; le jet frappe le plan de la roue sous un angle d'environ 20 degrés | Domaine Pelton, débit plus élevé par roue [DE:S1] | Roue plus petite qu'une Pelton à puissance égale [DE:S1] |
| Banki (cross-flow, Banki-Michell) | Action ; rotor en tambour, l'eau traverse la roue deux fois | Basse à moyenne chute, faible débit (lecture de l'abaque de l'IFC) [DE:S1] | Seuls les 2/3 de la dénivelée entre la roue et le niveau aval comptent dans la chute brute [DE:S1] |
| Francis | Réaction ; entrée radiale, sortie axiale, bâche spirale avec directrices | Turbine la plus répandue ; vaste domaine intermédiaire de chute et de débit [DE:S1] | Le rendement chute fortement en dessous d'environ la moitié du débit d'équipement [DE:S1] |
| Hélice (pales fixes) | Réaction ; écoulement axial, 3 à 6 pales | Basse chute [DE:S1] | Débit technique minimal de 75 % du débit d'équipement [LIT:S6] |
| Kaplan | Hélice à pales et directrices réglables (double réglage) | Basse chute, débit variable [DE:S1] | Coût plus élevé, rendement élevé sur une large plage de débit [DE:S1] |
| Bulbe | Kaplan à axe horizontal dont l'alternateur est logé dans un bulbe étanche | Chutes jusqu'à 30 m, forte puissance [DE:S1] | Excavation plus réduite qu'une Kaplan à axe vertical [DE:S1] |

Les centrales bulbe et Kaplan de basse chute utilisent des alternateurs lents ; les centrales Francis et Pelton de haute chute, des alternateurs rapides [DE:S1].

### P.3 Vitesse spécifique

La vitesse spécifique condense la hauteur de chute, le débit (ou la puissance) et la vitesse de rotation en un seul nombre qui caractérise la forme de la roue : faible pour les Pelton, intermédiaire pour les Francis, élevée pour les hélices et les Kaplan. À chute et débit égaux, une hélice tourne plus vite qu'une Francis, ce qui explique qu'elle ait supplanté la Francis en basse chute [DE:S1]. L'ESHA fait de la vitesse spécifique son principal critère de sélection [LIT:S6], mais aucun des textes sources disponibles ici ne donne de plages numériques par type de turbine ; l'annexe se limite donc aux définitions, et l'ingénieur doit présenter l'abaque d'expérience du constructeur à l'appui de toute vitesse proposée.

Trois formes sont d'usage courant (n en tr/min, Q en m^3^/s par groupe, H hauteur de chute nette en m, P puissance sur l'arbre par groupe) :

> n~s~ = n × P^0.5^ / H^1.25^ (P en kW ; forme métrique fondée sur la puissance)

> n~q~ = n × Q^0.5^ / H^0.75^ (forme fondée sur le débit)

> n~QE~ = (n / 60) × Q^0.5^ / (g × H)^0.75^ (forme adimensionnelle)

La vitesse de rotation d'un groupe synchrone est fixée par la fréquence du réseau f et le nombre de paires de pôles p :

> n = 60 × f / p

La vitesse varie donc par paliers discrets. À vitesse spécifique constante, la vitesse augmente quand la taille du groupe diminue ; une vitesse spécifique plus élevée réduit la taille de l'alternateur mais impose un calage plus profond pour se prémunir contre la cavitation (P.6).

### P.4 Rendement et comportement à charge partielle

Le choix de la turbine doit comparer les rendements sur toute la plage de débit, et pas seulement au point de dimensionnement [DE:S1]. Les turbines Pelton et Kaplan conservent un rendement élevé en dessous du débit d'équipement ; le rendement des Banki et des Francis baisse plus fortement en dessous de la moitié du débit, ce qui les destine aux débits réguliers [DE:S1]. En dessous d'un débit minimal, le groupe doit être arrêté pour éviter les dommages causés par de fortes vibrations [DE:S1]. Les deux sources indiquent des débits minimaux différents, et l'écart compte pour les mois d'étiage.

Table: Tableau P.2. Débit technique minimal par type de turbine, en % du débit d'équipement
| Turbine | Guide de l'IFC [DE:S1] | Guide de l'ESHA [LIT:S6] |
|---|---|---|
| Pelton | 10 à 20 (selon le nombre d'injecteurs) | 10 |
| Turgo | non indiqué | 20 |
| Francis | 40 | 50 |
| Kaplan (double réglage) | 20 | 15 |
| Semi-Kaplan (simple réglage) | 40 | 30 |
| Hélice (pales fixes) | non indiqué | 75 |
Note: l'IFC indique pour les Kaplan 20 à 40 %, respectivement pour les machines à double réglage et à simple réglage.

L'estimation de l'énergie doit appliquer la courbe de rendement tranche par tranche sur la courbe des débits classés, en s'arrêtant au plus élevé du débit technique minimal et du débit réservé [LIT:S6]. La hauteur de chute nette est la plus faible au débit maximal, car les pertes de charge croissent avec le carré de la vitesse et le niveau aval monte avec le débit [DE:S1] ; une hauteur de chute nette nominale doit donc être indiquée avec le débit correspondant.

La production à vitesse variable réduit les variations de rendement hors chute ou débit nominal et diminue l'abrasion [DE:S1].

### P.5 Nombre et taille des groupes

Le nombre de groupes résulte d'un arbitrage entre trois éléments :

1. **Fonctionnement à faible débit.** Exemple tiré du guide de l'IFC : au lieu d'un seul groupe Francis de 60 MW, deux groupes de 30 MW permettent de fonctionner jusqu'à 20 % du débit d'équipement de la centrale au lieu de 40 % [DE:S1]. Chaque aménagement exige d'évaluer si l'énergie supplémentaire paie le surcoût [DE:S1].
2. **Disponibilité.** Avec un seul groupe, tout arrêt du groupe est un arrêt de la centrale. Les grandes révisions reviennent tous les 7 à 12 ans et durent 4 à 6 semaines pour les groupes de plus de 20 MW [DE:S1] ; avec plusieurs groupes, elles peuvent être placées pendant les mois d'étiage.
3. **Coût.** Plus de groupes signifie plus de turbines, d'alternateurs, de vannes, de systèmes de commande et une centrale plus longue ; dans l'exemple d'optimisation de l'IFC, le TRI évolue par paliers avec le coût unitaire des turbines [DE:S1]. Des groupes identiques partagent les pièces de rechange et n'exigent des essais de performance que sur un seul groupe [DE:S1].

Le pont roulant de la centrale est dimensionné pour la pièce la plus lourde, un élément de l'alternateur ou la roue [DE:S1] ; des groupes moins nombreux et plus gros alourdissent donc aussi les charges de levage et de transport.

### P.6 Cavitation et calage de la turbine

La cavitation se produit là où la pression descend sous la pression de vapeur ; les cavités de vapeur implosent dans les zones de pression plus élevée et peuvent causer des dégâts très importants [LIT:S6]. Dans une turbine à réaction, le niveau aval détermine son apparition [LIT:S6]. La cavitation et l'érosion endommagent les roues et réduisent le rendement ; en exploitation et maintenance (O&M), la parade consiste en inspections et en recharges par soudure sur place [DE:S1].

Le calage (cote de la roue par rapport au niveau aval minimal) est régi par le coefficient de cavitation de l'installation (sigma de Thoma) :

> σ~plant~ = (H~atm~ − H~v~ − H~s~) / H

où H~atm~ est la hauteur représentative de la pression atmosphérique (qui diminue avec l'altitude), H~v~ la hauteur représentative de la pression de vapeur, H~s~ la hauteur d'aspiration (positive lorsque la roue est au-dessus du niveau aval) et H la hauteur de chute nette. Le calage doit donner un σ~plant~ supérieur au sigma critique de la turbine, avec une marge fixée par le constructeur à partir des essais sur modèle. Les sources ne donnent pas de valeurs de sigma en fonction de la vitesse spécifique ; l'annexe n'en cite donc aucune. Le calcul reste utile : à 120 m de chute nette, chaque 0,01 de sigma représente 1,2 m de profondeur de calage, de sorte qu'un changement de vitesse de la roue ou un niveau aval minimal plus bas peut déplacer le plancher de la centrale de plusieurs mètres et modifier le coût du génie civil.

### P.7 Abrasion par les sédiments et revêtements

Dans les centrales de moyenne et haute chute, les sédiments en suspension usent les ouvrages hydrauliques métalliques et les turbines, ce qui réduit leur rendement et leur durée de vie [DE:S1]. Plus la chute est haute, plus la particule à éliminer est petite : au-dessus de 100 m de chute, toutes les particules de plus de 0,2 mm doivent être retenues dans le dessableur ; 0,3 mm est acceptable pour des chutes plus faibles ; des particules dures (quartz) et anguleuses justifient une limite plus basse [DE:S1]. L'ESHA exprime le pouvoir abrasif des grains sur une roue Francis ainsi :

> P~e~ = μ × V~g~ × ((ρ~s~ − ρ~w~) / R) × v^3^

avec μ un coefficient de frottement, V~g~ le volume du grain, ρ~s~ et ρ~w~ les masses volumiques du grain et de l'eau, R le rayon de l'aube et v la vitesse du grain [LIT:S6]. Comme la vitesse des grains croît avec la chute, l'abrasion augmente fortement avec la hauteur de chute. L'ESHA fait état d'intervalles de réparation des roues Francis d'environ 6 à 7 ans avec un dessableur retenant 0,2 mm, de 3 à 4 ans à 0,3 mm et de 1 à 2 ans à 0,5 mm, et situe l'optimum économique vers 0,2 mm en conditions sévères (haute chute, quartz) et 0,3 mm en conditions normales [LIT:S6].

Les mesures d'atténuation sont un dessableur efficace, des revêtements céramiques durs [DE:S1], la vitesse variable [DE:S1] et, sur les rivières chargées en limons, le suivi des limons pour planifier les réparations [DE:S1]. Les sources ne chiffrent ni la durée de vie ni le coût des revêtements.

### P.8 Alternateurs, excitation et régulateurs de vitesse

Les groupes de grande et moyenne taille ont généralement un arbre vertical ; les petits groupes, un arbre horizontal [DE:S1]. L'excitation est sans balais ou à balais [DE:S1]. Les **alternateurs synchrones** ont une excitation en courant continu ou à aimants permanents et un régulateur de tension ; leur excitation est indépendante du réseau, ce qui leur permet de fonctionner en réseau isolé (îlotage) et de régler la tension [DE:S1]. Les **générateurs asynchrones** ne peuvent pas régler la tension, tournent à une vitesse liée à la fréquence du réseau et ne peuvent pas produire d'énergie lorsqu'ils sont isolés, car leur excitation provient du réseau [DE:S1]. Pour une centrale de 60 MW raccordée au réseau et censée contribuer au réglage de la tension, les machines synchrones sont le choix normal. Le rendement de l'alternateur augmente avec sa puissance nominale et approche 98 % au-dessus de 1 MW [DE:S1].

Le régulateur de vitesse agit sur les directrices ou les pointeaux pour maintenir la vitesse et la charge ; la pratique actuelle est le régulateur numérique PID [DE:S1]. Le temps de fermeture et le circuit hydraulique interagissent : le coup de bélier normal lors d'un arrêt commandé par le régulateur peut élever la pression dans la conduite forcée de 25 à 50 % de la chute brute pour les turbines à réaction, selon les constantes de temps du régulateur [LIT:S6]. Le temps de démarrage de l'eau t~h~ de l'ESHA permet de vérifier que le circuit hydraulique est réglable :

> t~h~ = V × L / (g × H)

Si t~h~ est inférieur à 3 s, une cheminée d'équilibre est inutile ; au-delà de 6 s, une cheminée d'équilibre ou un autre dispositif est nécessaire pour éviter de fortes oscillations du régulateur de la turbine, et un régulateur mal conçu peut interagir avec les oscillations de la cheminée d'équilibre [LIT:S6]. Lorsque les vannes doivent se fermer rapidement, une vanne de décharge montée en parallèle sur la turbine ralentit les variations de débit dans la conduite forcée [LIT:S6].

### P.9 Transformateurs, poste d'évacuation, protections, SCADA et auxiliaires

Les transformateurs élévateurs relèvent la tension pour réduire les pertes en ligne [DE:S1]. Le poste d'évacuation doit être implanté près de la centrale, au-dessus du niveau aval de projet (par exemple le niveau de la crue centennale), et dimensionné selon le nombre et la direction des lignes de départ [DE:S1]. L'entretien des transformateurs repose sur la surveillance de la température de l'huile et des enroulements, l'analyse des gaz dissous et les essais de tangente delta [DE:S1]. Les protections font l'objet d'essais par injection primaire et secondaire, et les relais de l'alternateur sont testés fonctionnellement lors de marches à vide [DE:S1]. Le contrôle-commande logiciel et le SCADA permettent un diagnostic à distance lorsque la présence permanente du fournisseur n'est pas rentable [DE:S1]. Les auxiliaires comprennent les pompes de drainage et d'épuisement, le refroidissement, l'air comprimé, la ventilation, les alimentations en courant alternatif et continu et le groupe diesel de secours [DE:S1].

Table: Tableau P.3. Durée de vie utile attendue des composants électromécaniques [DE:S1]
| Composant | Durée de vie (années) |
|---|---|
| Turbine (hors roue), alternateur, régulateur de vitesse, excitation, vannes de garde principales | 40 |
| Roues de turbine | 10 |
| Transformateurs de puissance ; appareillage HT et poste d'évacuation | 40 |
| Appareillage MT et BT | 30 |
| Contrôle-commande, protections, SCADA, télécommunications, comptage | 20 |
| Équipements auxiliaires mécaniques et électriques | 30 |
| Conduites forcées, vannes, batardeaux, grilles ; lignes de transport | 70 |
Note: moyennes ; la durée de vie réelle dépend de la qualité de l'eau, de la charge sédimentaire, du climat et du nombre de démarrages et d'arrêts [DE:S1].

### P.10 Équipements hydromécaniques

Les ouvrages hydrauliques métalliques sont classés selon leur fonction [DE:S1] : les vannes de service règlent le débit ou le niveau (évacuateur de crues, vidange de fond) ; les vannes de garde sont seulement entièrement ouvertes ou fermées (prise d'eau, aspirateur, amont des vannes de tête de conduite forcée) ; les vannes de maintenance, généralement des batardeaux, permettent de mettre à sec les conduits ; les directrices ou les pointeaux règlent le débit de la turbine ; les grilles protègent les prises d'eau. Le type de vanne dépend de la fonction, de la taille de l'ouverture, du climat et du mode d'exploitation [DE:S1]. La mise en service vérifie la vitesse de manœuvre des vannes, l'étanchéité des vannes fermées et des vannes de secours, et le temps de manœuvre des vannes de tête [DE:S1].

### P.11 Raccordement au réseau et code de réseau

Le coût du raccordement au réseau dépend surtout de la distance au réseau [DE:S1]. Dans la pratique du secteur, les provisions pour aléas sont de 7,5 à 10 % pour le raccordement au réseau et les équipements électromécaniques, contre 15 % pour le génie civil [DE:S1]. L'absence de ligne de transport et de renforcements du réseau est un obstacle majeur à la mise en service commerciale, qui génère d'importantes réclamations d'énergie réputée livrée à la charge des acheteurs [HY-06], et la mise en service exige une coordination précoce avec le gestionnaire du réseau [DE:S1].

Les sources ne citent aucune valeur de code de réseau (plages de fréquence et de tension, tenue aux creux de tension, réserve). Son contenu en matière d'essais ressort de la liste de mise en service : synchronisation, essai de capacité de puissance réactive, essai du stabilisateur de puissance (PSS), courbe en V, rejet de charge à 25, 50, 75, 100 et 110 % de la charge nominale, et répartition conjointe des puissances active et réactive pour les centrales à plusieurs groupes, avec comparaison des résultats au contrat de fourniture et au contrat d'achat d'électricité (CAE) [DE:S1]. Le comité doit se procurer le code de réseau national et rattacher chaque clause à un article de la spécification des équipements et à un essai.

### P.12 Contrats de fourniture, essais en usine et sur site

Les développeurs séparent souvent les contrats de génie civil, d'équipements électromécaniques et de raccordement au réseau ; les prêteurs préfèrent en général un contrat EPC clés en main, plus coûteux parce que le risque est transféré à l'entrepreneur [DE:S1]. En lots séparés, on utilise généralement le Livre jaune de la FIDIC pour les équipements électromécaniques et le Livre rouge pour le génie civil, et seule une poignée de fournisseurs de turbines est en concurrence [LIT:S7]. Les paiements des équipements électromécaniques sont généralement de 30 % à l'avance, 50 % à la livraison et 20 % à la réception [DE:S1], et leur fabrication se trouve sur le chemin critique [DE:S1]. Les garanties des fournisseurs dépassent souvent la période de garantie de l'EPC (par exemple 24 mois) ; le maître d'ouvrage doit en bénéficier par cession ou par garantie collatérale (collateral warranty) [LIT:S7].

Le futur personnel d'exploitation et de maintenance doit assister au montage et aux essais en usine [DE:S1]. Les essais sur site se font à sec (alignement, jeux des paliers, temps de manœuvre des vannes, isolement et tenue diélectrique des enroulements, logique du régulateur), à vide (survitesse, vibrations, excitation) et en charge [DE:S1]. Pour les groupes de plus de 5 MW, un essai de réception sur site selon la norme IEC 60041 et un essai par méthode indicielle vérifient le rendement de la turbine sur au moins un groupe, et les pertes de l'alternateur sont mesurées sur au moins un alternateur [DE:S1]. Les grands projets imposent couramment une marche probatoire de 30 jours par groupe ; tout défaut oblige à la recommencer [DE:S1]. Le stock de pièces de rechange représente environ 2,5 à 3,0 % du prix FOB des équipements, et le budget annuel de maintenance électromécanique environ 2,0 à 2,5 % de l'investissement initial, dont environ 60 % constituent une réserve pour les grandes révisions tous les 7 à 12 ans [DE:S1]. La disponibilité est d'environ 95 % la première année et passe à 97 à 98 % après trois ans [DE:S1].

### P.13 Exemple chiffré de Kasiri

**Vérification de la puissance.** Avec les valeurs du cas :

> P = ρ × g × Q × H × η = 1 000 × 9,81 × 57 × 120 × 0,92 × 0,98 = 60,5 MW

La puissance hydraulique est de 67,1 MW, la puissance sur l'arbre de 61,7 MW et la puissance délivrée de 60,5 MW : la puissance nominale de 60 MW est donc cohérente. Deux remarques. D'abord, 0,92 est un rendement au point de dimensionnement ; à charge partielle, la courbe de la Francis baisse (P.4), de sorte que le modèle énergétique a besoin d'une courbe et non d'une constante. Ensuite, 0,98 pour l'alternateur et le transformateur réunis est optimiste : l'IFC situe le rendement du seul alternateur à environ 98 % au maximum au-dessus de 1 MW [DE:S1], et les pertes du transformateur s'y ajoutent. Le P50 d'environ 292 GWh rapporté à 60 MW × 8 760 h donne le facteur de charge du cas, 55,6 % (tableau N.2).

**Type de turbine.** Avec 120 m de chute nette et 57 m^3^/s (19 à 57 m^3^/s par groupe), Kasiri se situe dans la classe haute chute (plus de 100 m) et dans le domaine Francis de l'abaque hauteur de chute-débit de l'IFC, bien au-dessus du plafond de 30 m des bulbes et à des débits supérieurs au domaine Pelton [DE:S1]. Le rapport de dimensionnement Q~d~/Q~av~ = 57/38 = 1,5 se situe au sommet de la fourchette de 1,0 à 1,5 des aménagements au fil de l'eau, et le facteur de charge de 56 % se trouve dans la fourchette de 40 à 70 % des aménagements au fil de l'eau [DE:S1].

**Vitesse spécifique.** Le cas retient deux groupes (chapitre 3). Les lignes à un et trois groupes, la fréquence du réseau (50 Hz) et les vitesses ci-dessous sont des hypothèses illustratives, utilisées pour montrer pourquoi deux groupes ont été retenus.

Table: Tableau P.4. Configurations illustratives des groupes de Kasiri (H = 120 m, η~t~ = 0,92, 50 Hz)
| Groupes | Q par groupe (m^3^/s) | Puissance sur l'arbre par groupe (MW) | Vitesse (tr/min) | Paires de pôles | n~s~ (kW) | n~q~ | n~QE~ |
|---|---|---|---|---|---|---|---|
| 1 | 57,0 | 61,7 | 214,3 | 14 | 134 | 44,6 | 0,134 |
| 2 | 28,5 | 30,9 | 300,0 | 10 | 133 | 44,2 | 0,133 |
| 2 | 28,5 | 30,9 | 333,3 | 9 | 147 | 49,1 | 0,148 |
| 3 | 19,0 | 20,6 | 375,0 | 8 | 135 | 45,1 | 0,136 |
| 3 | 19,0 | 20,6 | 428,6 | 7 | 155 | 51,5 | 0,155 |
Note: H^1.25^ = 397,2 ; H^0.75^ = 36,3 ; (gH)^0.75^ = 201,0. Les vitesses sont les paliers synchrones n = 3000/p.

En maintenant la vitesse spécifique vers 134, passer d'un à trois groupes porte la vitesse de 214 à 375 tr/min et réduit la taille de chaque alternateur ; le palier de vitesse suivant augmente la vitesse spécifique de 11 à 15 %, ce qui économise sur le coût de l'alternateur mais exige un calage plus profond. Le fournisseur doit confirmer ce choix au regard de ses références et de ses essais sur modèle.

**Fonctionnement à faible débit.** Le débit turbinable disponible est le débit de la rivière diminué du débit réservé de 4 m^3^/s, plafonné à 57 m^3^/s.

Table: Tableau P.5. Mois sous le débit technique minimal, moyennes mensuelles de Kasiri (nombres de groupes illustratifs)
| Configuration | Débit d'équipement par groupe (m^3^/s) | Débit minimal, IFC 40 % (m^3^/s) | Mois en dessous (IFC) | Débit minimal, ESHA 50 % (m^3^/s) | Mois en dessous (ESHA) |
|---|---|---|---|---|---|
| 1 × Francis | 57,0 | 22,8 | janv., févr., sept. | 28,5 | janv., févr., mars, août, sept., oct. |
| 2 × Francis | 28,5 | 11,4 | aucun | 14,3 | aucun |
| 3 × Francis | 19,0 | 7,6 | aucun | 9,5 | aucun |
Note: débits disponibles de janvier à décembre : 20, 16, 24, 48, 57, 54, 36, 24, 18, 26, 42, 32 m^3^/s. Les moyennes mensuelles masquent les étiages journaliers ; la courbe des débits classés journaliers doit donc confirmer le résultat.

Un groupe unique serait arrêté trois à six mois pendant une année moyenne, ce qui est incompatible avec un facteur de charge de 56 %. Deux groupes éliminent le problème sur les moyennes mensuelles et permettent de placer les révisions en février ou en septembre ; trois groupes ajoutent une marge en année sèche (coefficient de variation de l'énergie de 0,15) moyennant un surcoût. Deux groupes constituent le cas de base naturel à tester.

**Sédiments et coût.** À 120 m de chute, le dessableur doit retenir les particules de plus de 0,2 mm [DE:S1], et la teneur en quartz doit être connue avant de spécifier le revêtement de la roue. Les équipements électromécaniques, à 33 millions USD, représentent 26 % des 127 millions USD de composants de base recensés (33 % avec les équipements hydromécaniques), dans la fourchette de 14,9 à 56,6 % de l'IFC [DE:S1], soit environ 550 USD par kW. La disponibilité de 0,95 correspond au chiffre de première année de l'IFC et reste prudente au regard des 97 à 98 % attendus après la troisième année [DE:S1].

### P.14 Tests de décision

1. L'étude de faisabilité place-t-elle le point hauteur de chute-débit sur un abaque de sélection et justifie-t-elle le type de turbine au regard de toute la courbe des débits classés, et pas seulement du point de dimensionnement ?
2. La hauteur de chute nette nominale est-elle indiquée au débit nominal, avec les pertes de charge et la courbe de tarage du niveau aval utilisées pour la calculer ?
3. Quelle courbe de rendement (du fournisseur ou d'une machine de référence) sous-tend l'estimation de l'énergie, et le rendement à charge partielle est-il appliqué tranche par tranche ?
4. Quel débit technique minimal (IFC 40 % ou ESHA 50 % pour une Francis) est retenu, et combien de jours par année moyenne et par année sèche chaque configuration de groupes serait-elle arrêtée ?
5. Quels nombre et vitesse de groupes sont proposés, et l'optimisation montre-t-elle le coût marginal de chaque groupe supplémentaire au regard de l'énergie et de la disponibilité gagnées ?
6. Quel calage sous le niveau aval minimal est proposé, quelle marge de sigma suppose-t-il, et le fournisseur l'a-t-il confirmé par des essais sur modèle ?
7. Quels sont la concentration en sédiments, la granulométrie et la teneur en quartz mesurées, quelle taille de particule le dessableur retiendra-t-il, et quels revêtement de roue et intervalle de réparation sont supposés dans les OPEX ?
8. L'analyse du régulateur et du circuit hydraulique montre-t-elle que le temps de démarrage de l'eau et la surpression lors d'un rejet de charge restent dans les limites de dimensionnement de la conduite forcée ?
9. Le gestionnaire du réseau a-t-il émis une offre de raccordement pour la ligne de 132 kV, et chaque clause du code de réseau est-elle rattachée à une spécification d'équipement et à un essai de mise en service ?
10. Qui supporte le risque d'énergie réputée livrée si la ligne ou les renforcements du réseau sont en retard ?
11. Les garanties du contrat d'équipements électromécaniques (puissance, rendement, surpression, survitesse) sont-elles assorties de pénalités forfaitaires (liquidated damages), et sont-elles vérifiées par un essai sur site selon la norme IEC 60041 ?
12. Les garanties prolongées des constructeurs sont-elles cédées au maître d'ouvrage, et les pièces de rechange (2,5 à 3,0 % du prix FOB) ainsi que la réserve pour grandes révisions sont-elles prévues au budget ?
