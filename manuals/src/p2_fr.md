## 1. Objet du modèle {#objet}

Le modèle accompagne un développeur de mini-réseau depuis l'estimation de la demande jusqu'à la demande de financement. Il cherche à savoir si le projet peut devenir bancable, et avec quelle combinaison de subvention d'investissement, de financement basé sur les résultats (RBF), de dette concessionnelle, de dette senior et de fonds propres.

Par rapport au calculateur d'entrée de gamme, l'Édition Développeur ajoute :

* une courbe de charge horaire par segment, qui fixe la part d'énergie consommée la nuit et le ratio de pointe ;
* un inventaire des usages productifs, qui peut déterminer la consommation des usagers productifs ;
* un RBF différencié par segment de clientèle et un test de capacité de paiement ;
* le calibrage exact de la subvention et du RBF nécessaires, sans recours à la valeur cible d'Excel ;
* deux tranches de dette, un compte de réserve du service de la dette (DSRA) et le report des pertes fiscales ;
* trois scénarios prédéfinis et un tornado de sensibilité calculé en continu ;
* des indicateurs d'impact et de MRV, et une note de financement rédigée automatiquement.

Le modèle se concentre sur le dimensionnement des subventions, la capacité de paiement et l'impact. Il ne traite ni le change, ni la TVA, ni le besoin en fonds de roulement, ni les états financiers complets. Si le dossier l'exige, utilisez-le en complément d'un modèle de financement de projet complet.

## 2. Mise en route {#mise-en-route}

Le classeur est au format .xlsx, sans macro, compatible avec Excel 2010 et les versions ultérieures et avec LibreOffice Calc. Aucune feuille n'est protégée. Travaillez sur une copie et conservez l'original intact.

| Apparence | Signification |
|---|---|
| Texte bleu sur fond jaune | Hypothèse à saisir |
| Texte noir | Formule, à ne pas écraser |
| Texte vert | Lien depuis un autre onglet |

Tous les montants sont exprimés dans la devise indiquée dans « Libellé de la devise ». Ce libellé ne fait aucune conversion.

Ordre de travail conseillé :

1. Section 1 de l'onglet « Hypothèses » : projet, taux, fiscalité.
2. Segments de clientèle : effectifs, consommation, tarif, frais de raccordement, RBF, revenu mensuel.
3. Onglets « Courbe de charge » et « Usages productifs ».
4. Dimensionnement, CAPEX, OPEX.
5. Structure de financement.
6. Lecture du « Tableau de bord », puis de l'onglet « Déficit de financement & RBF ».
7. Contrôle de l'onglet « Contrôles », qui doit afficher « TOUT OK ».
8. Tests de scénarios et lecture de l'onglet « Sensibilité ».
9. Reprise des paragraphes de l'onglet « Demande de financement » dans la note conceptuelle.

## 3. Architecture du classeur {#architecture}

| Onglet | Contenu |
|---|---|
| « Commencer ici » | Démarche, méthode, simplifications, avertissement |
| « Hypothèses » | Projet, scénarios, segments, technique, CAPEX, OPEX, financement, impact |
| « Courbe de charge » | Profil horaire par segment, part nocturne, ratio de pointe |
| « Usages productifs » | Inventaire des équipements productifs |
| « Tableau de bord » | Indicateurs, verdicts, capacité de paiement, graphiques |
| « Déficit de financement & RBF » | Déficit de viabilité, subvention et RBF nécessaires, capacité d'endettement, calendrier du RBF |
| « Sensibilité » | Tornado et indicateurs de point mort |
| « Impact & MRV » | Indicateurs annuels et ratios coût-efficacité |
| « Demande de financement » | Paragraphes rédigés, tableau emplois-ressources, indicateurs clés |
| « Flux de trésorerie » | Moteur annuel sur 20 ans |
| « Contrôles » | Seize contrôles d'intégrité |

Le classeur contient aussi quatorze onglets masqués dont le nom commence par S_. Ce sont des copies du moteur de calcul, utilisées par le tornado. Ne les modifiez pas.

## 4. Renseigner les hypothèses {#hypotheses}

### 4.1 Projet, taux et fiscalité

Le « Taux de rendement minimal du projet (taux d'actualisation) » sert à la VAN, au LCOE, au déficit de viabilité et au calibrage du RBF. Exprimez-le en nominal, comme les flux. Le « TRI cible des fonds propres » sert au verdict sur les fonds propres et au calcul du RBF nécessaire du point de vue de l'actionnaire. Le « DSCR minimum exigé par les prêteurs » reprend le covenant de la term sheet.

### 4.2 Scénarios

Le « Scénario actif » se choisit dans une liste : Base, Prudent, Optimiste ou Personnalisé. Chaque scénario applique des multiplicateurs au tarif, à la consommation par client, au CAPEX, aux OPEX, au taux de recouvrement et au prix du diesel. Les valeurs fournies sont des exemples. Ajustez-les selon votre analyse de risque.

Les scénarios représentent un risque de réalisation sur un système déjà construit. Le dimensionnement reste celui du cas de base. Une demande inférieure de 15 % ne réduit donc pas la taille du champ PV : elle réduit les ventes.

### 4.3 Segments, tarifs, RBF et capacité de paiement

Pour chaque segment, saisissez :

| Colonne | Commentaire |
|---|---|
| « Clients » | Effectif cible, une fois la montée en charge achevée |
| « kWh/mois (saisi) » | Consommation mensuelle par client. Pour les usagers productifs, la colonne « kWh/mois (utilisé) » peut reprendre l'inventaire des usages productifs |
| « Tarif par kWh » | Tarif de l'année 1, avant indexation |
| « Frais de raccordement » | Payés par le client à son raccordement |
| « RBF par nouveau raccordement » | Montant prévu par le programme pour ce type de client |
| « Revenu ou chiffre d'affaires mensuel » | Revenu du ménage ou chiffre d'affaires de l'activité. Laissez 0 pour les institutions |

Le modèle calcule la facture mensuelle de l'année 1 et la compare au « Seuil de capacité de paiement (facture max en % du revenu) ». Il n'existe pas de seuil universel : utilisez celui de votre programme ou de votre étude de marché.

Le « Taux de recouvrement (part des factures payées) » s'applique à toutes les recettes d'énergie. Avec des compteurs à prépaiement, l'énergie est payée avant d'être consommée et le taux peut être fixé à 100 %.

### 4.4 Courbe de charge

L'onglet « Courbe de charge » contient, pour chaque segment, la part de l'énergie journalière consommée à chaque heure. Chaque colonne doit totaliser 100 %. Le modèle pondère ces profils par l'énergie de chaque segment et en déduit deux grandeurs :

* la part nocturne, c'est-à-dire l'énergie consommée entre le coucher et le lever du soleil, qui dimensionne la batterie ;
* le ratio de pointe, égal à la part de l'heure la plus chargée multipliée par 24, qui dimensionne le groupe diesel.

Les profils livrés sont illustratifs. Remplacez-les par des données de comptage ou d'enquête dès que possible. Un profil de ménages trop concentré en soirée surestime la batterie. Un profil productif trop étalé sous-estime la pointe diurne.

### 4.5 Usages productifs

L'onglet « Usages productifs » recense les équipements attendus : moulins, ateliers de soudure, chambres froides, pompes d'irrigation, machines à coudre, salons de coiffure, outils de menuiserie. Pour chaque ligne, la consommation mensuelle vaut :

unités × puissance (kW) × heures par jour × jours par mois × facteur de charge
{: .formula}

Le facteur de charge traduit le fait qu'un moteur tourne rarement à pleine puissance. Le total, divisé par le nombre d'usagers productifs, donne la consommation par usager. Si l'option correspondante vaut 1 dans les « Hypothèses », cette valeur remplace la saisie directe.

### 4.6 Conception technique et dimensionnement

| Composant | Règle |
|---|---|
| Champ PV | Production de conception × fraction solaire cible × facteur de pertes de stockage ÷ productible spécifique × surdimensionnement |
| Batterie | Production journalière × part nocturne ÷ profondeur de décharge |
| Groupe diesel | Puissance moyenne × ratio de pointe |

Le « Rendement aller-retour de la batterie » entre dans le facteur de pertes de stockage : l'énergie solaire consommée la nuit est stockée puis restituée avec une perte. La colonne « Forçage » permet d'imposer une conception issue d'une étude détaillée.

### 4.7 CAPEX et OPEX

Le CAPEX comprend le PV, la batterie, le groupe, le réseau de distribution, les compteurs et branchements, le local technique et le génie civil, les équipements productifs éventuellement financés par le projet, ainsi que les coûts de développement et les imprévus en pourcentage du CAPEX direct. Les batteries sont remplacées à la fin de leur durée de vie. Avec la réserve de maintenance activée, le coût est lissé dans le CFADS par des dotations annuelles.

Les OPEX comprennent l'exploitation et la maintenance fixes, le personnel, l'assurance, les licences et redevances, les coûts de MRV et de reporting, la gestion clientèle, la maintenance du groupe et le carburant. Les coûts de MRV méritent une ligne propre : un programme RBF impose une vérification tierce et un suivi des données, qui ont un coût annuel.

### 4.8 Structure de financement

| Ressource | Paramètres | Traitement |
|---|---|---|
| Subvention d'investissement | Montant | Encaissée en année 0 |
| RBF | Montant par segment, délai de vérification | Versé par nouveau raccordement vérifié |
| Dette senior | Part du CAPEX net de subvention, taux, durée, différé | Intérêts seuls pendant le différé, puis annuités |
| Dette concessionnelle | Mêmes paramètres | Idem, avec ses propres conditions |
| DSRA | Part du service de la dette de l'année suivante | Doté par les fonds propres, libéré au remboursement |
| Fonds propres | Solde du plan de financement | Supportent aussi la dotation initiale du DSRA |

> Le RBF arrive après la mise en service et la vérification des raccordements. Il ne finance pas la construction. L'onglet « Déficit de financement & RBF » indique le montant reçu les années 1 à 3, que le développeur doit préfinancer.

## 5. Lire les résultats {#resultats}

### 5.1 Tableau de bord

Le tableau de bord présente l'économie du projet (CAPEX, TRI et VAN avant et après subventions, LCOE, recette encaissée actualisée), le plan de financement et la bancabilité (DSCR, TRI et VAN des fonds propres, délai de récupération), la capacité de paiement par segment et six verdicts.

Le verdict sur les fonds propres utilise la VAN des fonds propres au taux cible plutôt que le TRI. Les remplacements de batteries et le DSRA créent des flux de signe variable, pour lesquels le TRI peut être trompeur ou ne pas exister.

### 5.2 Déficit de financement et calibrage du RBF

C'est l'onglet central du modèle. Il répond à quatre questions.

#### Ampleur du déficit

Le déficit de viabilité est la subvention en valeur actuelle qui ramène à zéro la VAN du projet avant subventions. Il est comparé à la valeur actuelle des subventions prévues.

#### Subvention nécessaire

Compte tenu du RBF prévu : subvention nécessaire = déficit de viabilité − VA(RBF prévu).

#### RBF nécessaire

Compte tenu de la subvention prévue, le modèle donne deux réponses. La première ramène la VAN du projet à zéro au taux minimal. La seconde donne aux fonds propres leur rendement cible avec la dette en place : c'est la lecture du développeur. Elles sont exprimées en montant uniforme par raccordement, puis en facteur multiplicatif à appliquer aux montants par segment.

#### Capacité d'endettement

La dette senior maximale est le plus grand prêt dont les annuités maintiennent le DSCR au-dessus du minimum chaque année, compte tenu du CFADS et du service de la dette concessionnelle. Le modèle indique l'année contraignante. Le plus souvent, c'est celle où le RBF s'arrête alors que les deux tranches sont en phase d'amortissement.

### 5.3 Sensibilité

Chaque variable est déplacée de plus ou moins l'amplitude choisie (20 % par défaut), une à la fois, autour du scénario actif. Le tableau donne la VAN après subventions, le déficit de viabilité, le DSCR minimum et le TRI des fonds propres pour chaque cas. Le tornado classe les variables selon leur effet sur la VAN.

Les taux d'intérêt ne modifient pas la VAN du projet, calculée hors dette. Leur effet apparaît sur le DSCR et sur le TRI des fonds propres.

L'onglet donne aussi un tarif moyen d'équilibre sans subvention, obtenu par interpolation linéaire. C'est une approximation, car l'impôt et la répartition entre solaire et diesel rendent la VAN légèrement non linéaire en tarif. Confirmez-la en saisissant ce tarif dans les hypothèses.

### 5.4 Impact et MRV

L'onglet « Impact & MRV » présente, année par année, les nouveaux raccordements vérifiés par segment, les personnes desservies, les usagers productifs, les emplois soutenus, l'énergie livrée, la production renouvelable, le CO2 évité, le RBF acquis et le RBF décaissé. Les ratios coût-efficacité rapportent le financement public non remboursable aux raccordements, aux personnes desservies et aux tonnes de CO2 évitées.

Le CO2 évité suppose qu'en l'absence du projet, l'énergie solaire livrée aurait été produite au diesel avec le même rendement. Le paramètre de référence permet de réduire cette hypothèse si une partie des clients utilisait d'autres sources.

### 5.5 Demande de financement

L'onglet rédige six paragraphes à partir des résultats : résumé du projet, solution technique, investissement et déficit, demande de financement, bancabilité, impact. Il présente aussi le tableau emplois-ressources et les indicateurs clés. Les nombres s'affichent avec les séparateurs de la langue d'Excel de l'utilisateur. Relisez et adaptez la rédaction avant tout envoi.

## 6. Méthode de calcul {#methode}

### 6.1 Formules principales

Solaire livré = MIN(production PV disponible ÷ facteur de pertes de stockage ; production brute × fraction solaire cible)
{: .formula}

CFADS = EBE − dotation à la réserve de maintenance − impôt après intérêts + RBF reçu
{: .formula}

Flux des fonds propres = CFADS − service total de la dette − variation du DSRA
{: .formula}

Déficit de viabilité = MAX(0 ; − VAN du flux du projet avant subventions)
{: .formula}

RBF uniforme pour VAN = 0 = (déficit de viabilité − subvention) ÷ VA(raccordements vérifiés payés)
{: .formula}

RBF uniforme pour la cible des fonds propres = − (VAN des fonds propres au taux cible − VA du RBF prévu au taux cible) ÷ VA(raccordements) au taux cible
{: .formula}

Dette senior maximale = MIN sur les années de (CFADS ÷ DSCR minimum − service de la dette concessionnelle) ÷ service senior par unité de dette
{: .formula}

### 6.2 Pourquoi le calibrage est exact

Le RBF entre de façon linéaire dans les flux du projet et dans les flux des fonds propres. Il n'est pas imposé dans le modèle, et il ne modifie ni la dette ni le DSRA. La VAN est donc une fonction affine du montant de RBF par raccordement, et l'équation VAN = 0 se résout directement. Deux contrôles d'identité de l'onglet « Contrôles » le vérifient à chaque recalcul. En test, l'injection du RBF calculé donne une VAN du projet nulle et un TRI des fonds propres égal à la cible, 15,0 %.

Si le RBF est imposable dans votre juridiction, le calibrage sous-estime le montant nécessaire. Pour un projet bénéficiaire, une première approximation consiste à diviser le résultat par (1 − taux d'impôt). Pour un calcul exact, le RBF doit être intégré au résultat imposable du moteur.

### 6.3 Fiscalité

L'impôt est calculé deux fois. Le calcul hors dette alimente le TRI du projet. Le calcul après intérêts alimente le CFADS. Dans les deux cas, les pertes fiscales sont reportées sans limite de durée et imputées sur les bénéfices ultérieurs.

## 7. Exemple commenté {#exemple}

L'exemple livré est fictif : 970 clients, dont 800 ménages, 60 usagers productifs, 100 commerces et 10 institutions.

| Grandeur | Valeur |
|---|---|
| Part nocturne et ratio de pointe issus de la courbe de charge | 37,1 % et 1,79 |
| Consommation par usager productif issue de l'inventaire | 155 kWh par mois |
| Dimensionnement | 305 kWc PV, 540 kWh de stockage, 87 kW de groupe diesel |
| CAPEX total | 1 162 734 USD, soit 1 199 USD par raccordement |
| Déficit de viabilité | 804 952 USD, soit 830 USD par raccordement |
| Subventions prévues | 600 000 USD de subvention initiale et 252 000 USD de RBF, soit 260 USD par raccordement en moyenne |
| VAN du projet après subventions | positive de 12 968 USD |
| Dette senior et dette concessionnelle | 112 547 USD chacune |
| DSCR minimum | 1,34x pour un seuil de 1,30x, année contraignante 2036 |
| Dette senior maximale au DSCR minimum | 118 010 USD |
| TRI des fonds propres | 10,1 % pour une cible de 15 % |
| RBF uniforme nécessaire pour la cible des fonds propres | 347 USD par raccordement |
| Tarif moyen d'équilibre sans subvention | 0,60 USD par kWh, pour un tarif moyen facturé de 0,38 USD |

Lecture. Le projet ne se finance pas sur ses seules recettes. La subvention et le RBF prévus comblent le déficit au niveau du projet, et la dette respecte le covenant avec une faible marge (la dette senior prévue est inférieure de 5 % environ au maximum supportable). Les fonds propres n'atteignent pas leur cible. Il faudrait porter le RBF de 260 à 347 USD par raccordement en moyenne, soit un budget RBF supérieur d'environ un tiers.

Le tornado apporte un résultat moins intuitif. Une hausse de 20 % de la consommation par client fait baisser la VAN, tout comme une baisse de 20 %. Le système est dimensionné pour la demande de base : les kWh supplémentaires sont produits par le groupe diesel, à un coût de carburant et de maintenance supérieur au tarif encaissé. Une croissance de la demande non accompagnée d'une extension du champ PV détériore donc l'économie du projet.

## 8. Contrôles d'intégrité et diagnostic {#controles}

| Contrôle | Signification d'une alerte | Action |
|---|---|---|
| « Ressources = emplois à la construction » | Plan de financement déséquilibré | Vérifiez les parts de dette et la subvention |
| « Part senior + concessionnelle <= 100 % » | Parts de dette trop élevées | Réduisez l'une des deux parts |
| « Dette senior remboursée à l'échéance » | Différé ou durée incohérents | Le différé doit être plus court que la durée |
| « Courbe de charge : chaque segment totalise 100 % » | Profil horaire incomplet | Corrigez la colonne concernée |
| « Bilan énergétique : solaire + diesel = production » | Formule écrasée | Restaurez le moteur depuis une copie vierge |
| « DSRA entièrement libéré à la fin » | Durée de prêt au-delà de l'horizon | Réduisez la durée du prêt |
| « Identité des subventions : VAN après = VAN avant + grant + VA(RBF) » | Formule modifiée dans le moteur | Restaurez le moteur |
| « Le calibrage du RBF reproduit la cible des fonds propres (contrôle d'identité) » | Formule modifiée | Restaurez le moteur |
| « Les moteurs de sensibilité reproduisent la base (ligne de base = Flux de trésorerie) » | Onglet masqué modifié | Restaurez le fichier |

## 9. Limites d'emploi {#limites}

Ces limites résultent d'une revue critique du modèle. Lisez-les avant de présenter un résultat à un comité d'investissement.

1. Pas de temps annuel, sans dispatch horaire. La répartition entre solaire et diesel résulte d'un plafond de fraction solaire. Pour un dossier d'investissement, confirmez-la par une simulation horaire.
2. Capacités fixes. Sans extension du champ PV, une demande plus forte que prévu est servie au diesel (voir chapitre 7).
3. Dimensionnement sur le cas de base. Les scénarios et le tornado ne redimensionnent pas le système.
4. Groupe diesel dimensionné sur la pointe pondérée, sans marge de réserve ni contrainte de démarrage des moteurs. Ajoutez une marge dans la colonne « Forçage » si nécessaire.
5. Fiscalité simplifiée. Taux unique, amortissement sur le CAPEX total, subventions et RBF non imposables.
6. Dette en annuités, sans commissions ni profil sculpté. La dette senior maximale est calculée sur le CFADS en vigueur, dont l'impôt dépend lui-même des intérêts : c'est une bonne approximation, pas une optimisation.
7. Monnaie unique. Le risque de change entre une dette en devise forte et des recettes en monnaie locale n'est pas représenté.
8. Notions d'impact simplifiées. Les personnes desservies se limitent aux ménages raccordés. Les emplois soutenus reposent sur un ratio saisi par l'utilisateur, à justifier par une enquête.

## 10. Glossaire {#glossaire}

| Terme | Définition |
|---|---|
| CFADS | Flux de trésorerie disponible pour le service de la dette |
| DSCR | CFADS rapporté au service de la dette de l'année |
| DSRA | Compte de réserve du service de la dette |
| Réserve de maintenance | Dotations annuelles destinées à financer le remplacement des batteries |
| Déficit de viabilité | Subvention en valeur actuelle qui ramène à zéro la VAN avant subventions |
| RBF | Financement basé sur les résultats, versé par raccordement vérifié |
| Différé | Période pendant laquelle seuls les intérêts sont payés |
| Dette concessionnelle | Prêt à conditions plus favorables que le marché, souvent accordé par une institution de développement |
| LCOE | Coût actualisé de l'électricité sur le cycle de vie, par kWh vendu |
| Part nocturne | Part de l'énergie journalière consommée entre le coucher et le lever du soleil |
| Ratio de pointe | Puissance appelée à l'heure la plus chargée, rapportée à la puissance moyenne |
| Facteur de charge | Rapport entre la puissance moyenne réellement appelée par un équipement et sa puissance nominale |
| MRV | Mesure, rapportage et vérification des résultats |

## 11. Avertissement et licence {#licence}

Le modèle est un outil de présélection et de préfaisabilité. Il ne constitue pas un conseil en investissement, juridique, fiscal ou d'ingénierie, et ne remplace pas une due diligence indépendante. Les données de l'exemple sont fictives et ne décrivent aucun projet, développeur ou programme existant.

La licence est accordée pour un utilisateur ou une organisation. La revente, la redistribution et la publication du fichier ou du présent manuel sont interdites.
