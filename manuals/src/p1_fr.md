## 1. Objet du calculateur {#objet}

Le calculateur évalue, au stade de la préfaisabilité, l'équilibre économique d'un mini-réseau hybride solaire PV, batterie et groupe diesel destiné à l'électrification rurale. Il répond à trois questions que se posent successivement un développeur, un bailleur et un prêteur :

1. Le projet couvre-t-il ses coûts avec ses seules recettes tarifaires ?
2. Peut-il porter une dette senior dans le respect d'un DSCR minimal ?
3. Quel montant de subvention, sous forme de subvention d'investissement ou de financement basé sur les résultats (RBF), faut-il pour atteindre le taux de rendement minimal retenu ?

La troisième question est la plus utile en pratique. Dans la plupart des projets d'accès à l'énergie, le tarif supportable par les ménages ne couvre pas le coût complet du kWh livré. Le calculateur chiffre cet écart sous la forme d'un déficit de viabilité, puis vérifie si les subventions envisagées suffisent à le combler.

### Ce que l'outil n'est pas

Ce n'est pas un outil de conception technique. Le dimensionnement automatique repose sur des ratios et ne remplace ni une simulation horaire (HOMER Pro ou équivalent) ni une étude de charge sur site. Ce n'est pas non plus un modèle de financement de projet complet : il ne traite ni le change, ni la TVA, ni le besoin en fonds de roulement, ni les états financiers. Ces limites sont détaillées au chapitre 9.

### Public visé

Développeurs de mini-réseaux en phase d'identification ou de préparation d'une candidature, consultants chargés d'une étude de préfaisabilité, équipes de programmes qui veulent tester l'ordre de grandeur d'une subvention, étudiants et analystes en finance de l'énergie.

## 2. Mise en route {#mise-en-route}

### Configuration

Le fichier est un classeur Excel au format .xlsx, sans macro. Il fonctionne avec Excel 2010 et les versions ultérieures, et s'ouvre dans LibreOffice Calc. Aucune feuille n'est protégée : vous pouvez tout modifier, y compris par erreur. Conservez une copie vierge du fichier avant toute saisie.

### Conventions de couleurs

| Apparence | Signification | Règle |
|---|---|---|
| Texte bleu sur fond jaune | Hypothèse saisie par l'utilisateur | À modifier |
| Texte noir | Formule | Ne pas écraser |
| Texte vert | Lien vers un autre onglet | Ne pas écraser |

Les montants sont exprimés dans une devise unique, dont le libellé se saisit dans « Libellé de la devise ». Le libellé ne convertit rien : si vous travaillez en francs CFA, toutes les hypothèses monétaires doivent être saisies en francs CFA.

### Ordre de travail conseillé

1. Renseignez le projet et les paramètres financiers généraux (section 1 de l'onglet « Hypothèses »).
2. Saisissez les segments de clientèle, puis la montée en charge des raccordements.
3. Vérifiez le dimensionnement proposé et forcez vos propres valeurs si vous disposez d'une conception.
4. Saisissez les coûts unitaires d'investissement et d'exploitation.
5. Décrivez la structure de financement : subvention initiale, RBF, dette.
6. Lisez le « Tableau de bord », puis contrôlez que l'onglet « Contrôles » affiche « TOUT OK ».
7. Testez la tenue du résultat avec les leviers de scénario.

## 3. Architecture du classeur {#architecture}

| Onglet | Contenu | Saisie |
|---|---|---|
| « Commencer ici » | Mode d'emploi résumé, simplifications, avertissement | Non |
| « Hypothèses » | Toutes les hypothèses, le dimensionnement et les leviers | Oui |
| « Tableau de bord » | Indicateurs, déficit de viabilité, verdicts, graphiques | Non |
| « Flux de trésorerie » | Moteur annuel sur 20 ans | Non |
| « Contrôles » | Contrôles d'intégrité | Non |

Le moteur de calcul est annuel. L'année 0 correspond à la construction, les années 1 à 20 à l'exploitation. Dans l'onglet « Flux de trésorerie », la colonne B donne soit un total, soit une VAN au taux minimal. Les lignes concernées portent la mention [B = VAN].

## 4. Renseigner les hypothèses {#hypotheses}

### 4.1 Projet et paramètres financiers

| Paramètre | Rôle dans le calcul | Conseil de saisie |
|---|---|---|
| « Durée de vie du projet » | Borne les flux d'exploitation | 20 ans au maximum. Alignez sur la durée de la licence ou de la concession |
| « Taux d'actualisation / taux de rendement minimal (projet) » | Actualise les flux pour la VAN, le LCOE et le déficit de viabilité | Taux nominal, cohérent avec l'indexation. Utilisez le coût moyen pondéré du capital visé ou le taux de référence du programme |
| « TRI cible des fonds propres » | Sert au verdict sur les fonds propres | Rendement attendu par l'actionnaire, en nominal |
| « DSCR minimum exigé par le prêteur » | Seuil du covenant | Reprenez la valeur de la lettre d'intention ou de la term sheet du prêteur |
| « Indexation du tarif » | Fait évoluer le tarif chaque année | Ne dépassez pas ce que le régulateur ou le contrat autorise |
| « Indexation des coûts (OPEX, carburant) » | Fait évoluer les charges et le coût de remplacement des batteries | Inflation locale ou indexation contractuelle |
| « Taux d'impôt sur les sociétés » | Impôt sur le bénéfice positif | Tenez compte des exonérations éventuelles en ajustant le taux |
| « Durée d'amortissement fiscal » | Amortissement linéaire du CAPEX total | Durée admise par l'administration fiscale |

> Le taux minimal et l'indexation doivent être exprimés sur la même base. Un taux nominal de 10 % avec une indexation de 3 % correspond à un taux réel proche de 6,8 %. Mélanger un taux réel et des flux nominaux fausse la VAN et le LCOE.

### 4.2 Leviers de scénario

Les quatre multiplicateurs de la section 2 s'appliquent au tarif, à la consommation, au CAPEX et aux OPEX. La valeur 1,00 reproduit les hypothèses saisies. Une valeur de 0,85 sur la demande simule une consommation inférieure de 15 % à la prévision, à système inchangé. Utilisez-les pour un test de résistance rapide avant de modifier les hypothèses elles-mêmes.

### 4.3 Clients et demande

Le tableau de la section 3 accueille cinq segments : ménages, usagers productifs, commerces, institutions et un segment libre. Pour chacun, saisissez le nombre de clients, la consommation mensuelle par client, le tarif par kWh et les frais de raccordement.

Préférez une consommation issue d'une enquête de demande ou des données de comptage de projets comparables dans la même zone. Une valeur théorique tirée d'une liste d'équipements surestime en général la demande des premières années, parce qu'elle suppose un équipement que les ménages n'ont pas encore acquis.

Trois paramètres complètent la demande :

* la montée en charge des raccordements (part des clients raccordés en années 1, 2 puis 3 et suivantes) ;
* la « Croissance annuelle de la consommation par client », appliquée à tous les segments ;
* le « Taux de recouvrement (part des factures effectivement payées) », qui transforme le chiffre d'affaires facturé en recettes encaissées. Avec des compteurs à prépaiement, l'énergie est payée avant d'être consommée et le taux peut être fixé à 100 %. En facturation à terme échu, retenez le taux observé sur des réseaux comparables.

### 4.4 Conception technique et dimensionnement

Le calculateur dimensionne le système à partir de l'énergie vendue en année 3, une fois tous les clients raccordés :

| Composant | Règle de dimensionnement |
|---|---|
| Champ PV | Production de conception × fraction solaire cible × facteur de pertes de stockage ÷ productible spécifique × facteur de surdimensionnement |
| Stockage batterie | Production journalière × part consommée la nuit ÷ profondeur de décharge utile |
| Groupe diesel | Puissance moyenne × ratio charge de pointe / charge moyenne |

Le « Productible spécifique PV » s'obtient avec PVGIS ou l'étude de conception du site. La « Fraction solaire cible (part max de la production issue du PV) » représente le plafond de couverture solaire que permet le stockage : au-delà, le groupe diesel prend le relais.

Le « Rendement aller-retour de la batterie » mesure le rapport entre l'énergie restituée et l'énergie stockée. L'énergie solaire consommée la nuit transite par la batterie et perd cette différence. Le calculateur en déduit le « Facteur de pertes de stockage sur l'énergie solaire », qui augmente la production PV nécessaire.

Si vous disposez d'une conception, saisissez vos valeurs dans la colonne « Forçage ». La colonne « Retenu » reprend alors votre valeur à la place du dimensionnement automatique.

### 4.5 CAPEX

Les coûts sont saisis en coûts unitaires (par kWc, par kWh de stockage, par kW de groupe, par raccordement) et en forfait pour le local technique, le BOS et le génie civil. Les « Coûts de développement (études, permis, communauté) » et les « Imprévus » s'expriment en pourcentage du CAPEX direct.

Le remplacement des batteries intervient tous les n ans, n étant la « Durée de vie des batteries ». Avec l'option de réserve de maintenance activée, le coût du remplacement est lissé par des dotations annuelles dans le CFADS. Ce traitement, équivalent à un compte de réserve de maintenance, évite qu'une année de remplacement ne fasse chuter le DSCR.

### 4.6 OPEX

Les charges d'exploitation regroupent l'exploitation et la maintenance fixes (en pourcentage du CAPEX direct), le personnel local, l'assurance, les licences et redevances, la maintenance du groupe diesel, le carburant et la gestion clientèle (frais de mobile money inclus, en pourcentage du chiffre d'affaires). Le carburant est calculé à partir de l'énergie diesel, du « Rendement du groupe diesel » et du « Prix du diesel en année 1 », puis indexé.

### 4.7 Financement et subventions

| Paramètre | Effet |
|---|---|
| « Subvention d'investissement initiale » | Encaissée en année 0. Réduit l'assiette de la dette et des fonds propres |
| « RBF par nouveau raccordement » | Versé pour chaque nouveau raccordement, l'année de sa réalisation ou l'année suivante selon le délai de vérification |
| « Part de dette dans le CAPEX net de subvention » | Fixe le montant de la dette senior |
| « Taux d'intérêt », « Durée du prêt (différé inclus) », « Différé (intérêts seuls) » | Profil de remboursement : intérêts seuls pendant le différé, puis annuités constantes |

Les fonds propres complètent le plan de financement. Le RBF n'est pas une ressource de construction : il arrive après la mise en service et la vérification des raccordements. Le développeur doit donc préfinancer ce montant.

### 4.8 Impact

Le « Facteur d'émission CO2 du diesel » (2,68 kgCO2 par litre dans l'exemple) sert à estimer les émissions évitées par rapport à une alimentation entièrement au diesel. Vérifiez la valeur exigée par le référentiel de votre bailleur.

## 5. Lire les résultats {#resultats}

### 5.1 Économie du projet

| Indicateur | Lecture |
|---|---|
| « TRI du projet - avant subventions » | Rentabilité intrinsèque du projet, sur la base de ses seules recettes |
| « TRI du projet - après subventions » | Rentabilité une fois la subvention et le RBF intégrés |
| « VAN du projet au taux minimal - avant subventions » | Valeur créée ou détruite au taux minimal. Une valeur négative signale un besoin de subvention |
| « LCOE (coût par kWh vendu) » | Coût actualisé sur le cycle de vie, par kWh vendu |
| « Recette encaissée actualisée par kWh » | Recette réellement encaissée, actualisée sur la même base que le LCOE |

Comparez toujours le LCOE à la recette encaissée actualisée, et non au tarif de l'année 1. Les deux grandeurs sont actualisées de la même façon et tiennent compte de l'indexation et du taux de recouvrement.

### 5.2 Financement et bancabilité

Le DSCR est le rapport entre le CFADS et le service de la dette de l'année. Le tableau de bord affiche le minimum et la moyenne sur la durée du prêt. Le « Délai de récupération des fonds propres (ans) » correspond à la première année où le flux cumulé des fonds propres redevient positif.

### 5.3 Déficit de viabilité et verdicts

Le déficit de viabilité est la subvention initiale, exprimée en valeur actuelle, qui ramène à zéro la VAN du projet avant subventions. Le tableau de bord le compare à la valeur actuelle des subventions prévues (subvention initiale et RBF). Le « Déficit restant après subventions prévues » indique ce qu'il manque encore.

Cinq verdicts résument la situation : viabilité commerciale sans subvention, viabilité après subventions, respect du covenant de dette, TRI des fonds propres, couverture du LCOE par le tarif encaissé. Une réponse OUI apparaît sur fond vert, une réponse NON sur fond rouge, avec la cause.

> Un RBF versé en années 1 à 3 vaut moins qu'une subvention de même montant versée en année 0, puisqu'il est actualisé. Pour combler un déficit donné, le montant nominal de RBF doit donc être supérieur au déficit exprimé en valeur actuelle.

## 6. Méthode de calcul {#methode}

### 6.1 Enchaînement

Raccordements, puis énergie vendue, production nécessaire, répartition solaire et diesel, recettes, charges, EBE, impôt, flux du projet, service de la dette, CFADS, DSCR et flux des fonds propres.

### 6.2 Formules principales

Production brute = énergie vendue ÷ (1 − pertes de distribution et de conversion)
{: .formula}

Solaire livré = MIN(production PV disponible ÷ facteur de pertes de stockage ; production brute × fraction solaire cible). Diesel = production brute − solaire livré
{: .formula}

Facteur de pertes de stockage = 1 + part nocturne × (1 ÷ rendement aller-retour − 1)
{: .formula}

Flux du projet avant subventions = − CAPEX + EBE − remplacements de batteries − impôt hors dette
{: .formula}

CFADS = EBE − dotation à la réserve de maintenance (ou remplacement) − impôt après intérêts + RBF reçu
{: .formula}

LCOE = VA(CAPEX + OPEX hors gestion clientèle + remplacements) ÷ VA(kWh vendus)
{: .formula}

Déficit de viabilité = MAX(0 ; − VAN du flux du projet avant subventions)
{: .formula}

L'impôt est calculé au taux unique sur le bénéfice imposable positif, sans report des pertes. Les subventions et le RBF sont traités comme non imposables. Le LCOE exclut les frais de gestion clientèle, proportionnels au chiffre d'affaires, pour éviter une circularité avec le tarif.

## 7. Exemple commenté {#exemple}

Le classeur est livré avec un exemple fictif : un village de 970 clients (800 ménages, 60 usagers productifs, 100 commerces et 10 institutions). Les valeurs sont illustratives et ne constituent pas des références de marché.

| Grandeur | Valeur |
|---|---|
| Dimensionnement retenu | 367 kWc PV, 780 kWh de stockage, 145 kW de groupe diesel |
| CAPEX total | 1 336 072 USD, soit 1 377 USD par raccordement |
| VAN avant subventions au taux de 10 % | négative de 879 325 USD |
| Déficit de viabilité | 879 325 USD, soit 907 USD par raccordement |
| Subventions prévues | 680 000 USD de subvention initiale et 250 USD de RBF par raccordement, soit 889 705 USD en valeur actuelle |
| VAN après subventions | positive de 10 381 USD |
| TRI du projet après subventions | 10,3 % |
| DSCR minimum | 1,55x pour un seuil de 1,30x |
| TRI des fonds propres | 8,0 % pour une cible de 15 % |
| LCOE et recette encaissée actualisée | 0,632 et 0,438 USD par kWh |

Lecture : sans subvention, le projet détruit de la valeur, ce qui est attendu pour un mini-réseau rural à tarif modéré. Les subventions prévues comblent tout juste le déficit au niveau du projet, et la dette est remboursable avec une marge confortable. En revanche, le TRI des fonds propres reste nettement sous la cible. Pour un actionnaire privé, le projet n'est donc pas encore finançable en l'état. Les leviers possibles sont un RBF plus élevé, une part de dette concessionnelle, ou un tarif plus proche du coût lorsque la capacité de paiement le permet.

## 8. Contrôles d'intégrité et diagnostic {#controles}

| Contrôle | Cause probable d'une alerte | Action |
|---|---|---|
| « Ressources = emplois en année 0 (grant + dette + fonds propres = CAPEX) » | Saisie incohérente du financement | Vérifiez la part de dette et la subvention |
| « Dette entièrement remboursée à l'échéance » | Durée ou différé incohérents | Le différé doit être plus court que la durée du prêt |
| « Durée du prêt dans la durée de vie » | Prêt plus long que le projet | Réduisez la durée du prêt |
| « Dotations à la réserve = remplacements (si réserve utilisée) » | Durée de vie des batteries incohérente avec la durée du projet | Vérifiez la durée de vie des batteries |
| « Bilan énergétique : solaire + diesel = production » | Formule écrasée dans le moteur | Restaurez la formule à partir d'une copie vierge |
| « Au moins un client saisi » | Tableau des segments vide | Saisissez au moins un segment |

La mention « TOUT OK » doit figurer dans l'onglet « Contrôles » et en tête du « Tableau de bord » avant toute utilisation des résultats.

## 9. Limites d'emploi {#limites}

Les points suivants résultent d'une revue critique du modèle. Ils ne sont pas des défauts cachés mais des choix de simplification, qu'il faut connaître avant de présenter un résultat à un comité.

1. Pas de temps annuel. La répartition entre solaire et diesel ne résulte pas d'une simulation horaire mais d'un plafond de fraction solaire. Pour un dossier d'investissement, confirmez la répartition par une simulation.
2. Capacités fixes. Le PV et la batterie ne sont pas étendus au fil des années. Si la consommation croît fortement, le groupe diesel couvre l'écart et le coût du carburant augmente. Plafonnez la croissance ou prévoyez une extension par un CAPEX complémentaire.
3. Raccordements fractionnaires. La montée en charge s'applique en pourcentage. Le nombre de raccordements d'une année peut donc être non entier, ce qui est sans effet sur les ordres de grandeur.
4. Fiscalité simplifiée. Pas de report des pertes, amortissement sur le CAPEX total (y compris la part subventionnée), subventions non imposables. Selon la législation locale, l'assiette amortissable peut devoir être réduite des subventions.
5. TRI et flux de signe variable. Les remplacements de batteries peuvent rendre des flux négatifs en cours de vie. Le TRI devient alors peu fiable. Fondez la décision sur la VAN et le déficit de viabilité.
6. Dette unique. Un seul prêt senior en annuités. Pas de compte de réserve du service de la dette, de commissions ni de profil sculpté.
7. Monnaie unique. Pas de risque de change, alors que la dette est souvent libellée en devise forte et les recettes en monnaie locale.

## 10. Glossaire {#glossaire}

| Terme | Définition |
|---|---|
| CAPEX | Dépenses d'investissement initiales |
| OPEX | Charges d'exploitation annuelles |
| EBE | Excédent brut d'exploitation : recettes moins OPEX |
| CFADS | Flux de trésorerie disponible pour le service de la dette |
| DSCR | Ratio de couverture du service de la dette : CFADS divisé par le service de la dette de l'année |
| VAN | Valeur actuelle nette des flux au taux minimal |
| TRI | Taux de rentabilité interne |
| LCOE | Coût actualisé de l'électricité sur le cycle de vie, par kWh vendu |
| RBF | Financement basé sur les résultats, versé après vérification d'un résultat, ici un raccordement |
| Déficit de viabilité | Subvention en valeur actuelle qui ramène la VAN avant subventions à zéro |
| Fraction solaire | Part de la production assurée par le PV |
| Productible spécifique | Énergie produite par kWc installé et par an |
| Profondeur de décharge | Part de la capacité nominale de la batterie effectivement utilisable |
| Rendement aller-retour | Rapport entre l'énergie restituée par la batterie et l'énergie stockée |

## 11. Avertissement et licence {#licence}

Le calculateur est un outil de présélection et de préfaisabilité, à visée pédagogique et de planification. Il ne constitue pas un conseil en investissement, juridique, fiscal ou d'ingénierie. Les résultats dépendent entièrement des hypothèses saisies. Une due diligence technique et financière indépendante reste nécessaire avant toute décision d'investissement.

Les données de l'exemple sont fictives. Elles ne décrivent aucun projet, développeur ou programme existant.

La licence est accordée pour un utilisateur ou une organisation. La revente, la redistribution et la publication du fichier ou du présent manuel sont interdites.
