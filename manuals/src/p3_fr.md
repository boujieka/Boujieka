## 1. Objet du modèle {#objet}

Le modèle sert au gestionnaire d'un guichet de subvention ou de financement basé sur les résultats (RBF) pour l'accès à l'énergie. À partir d'un pipeline de projets candidats, il répond à la question suivante : quels projets soutenir, avec quels montants de RBF et de subvention d'investissement, et quel portefeuille de raccordements, d'impact, d'effet de levier et de risque cela permet-il d'obtenir ?

Le classeur couvre l'ensemble du cycle d'un appel à projets :

1. le paramétrage du fonds et de ses règles de soutien ;
2. l'examen d'éligibilité, avec le motif de rejet de chaque projet ;
3. la notation pondérée des projets éligibles ;
4. l'allocation de l'enveloppe par ordre de rang, sous contraintes de concentration ;
5. la projection des décaissements et de la trésorerie du fonds ;
6. le suivi des résultats vérifiés pendant la vie du fonds.

Le modèle est un outil d'aide à la décision. Il ne remplace ni le comité d'investissement, ni la due diligence, ni les règles de passation, ni la documentation juridique du fonds.

## 2. Mise en route {#mise-en-route}

Le classeur est au format .xlsx, sans macro, compatible avec Excel 2010 et les versions ultérieures et avec LibreOffice Calc. Les fonctions utilisées n'exigent pas de version récente d'Excel. Aucune feuille n'est protégée : travaillez sur une copie.

| Apparence | Signification |
|---|---|
| Texte bleu sur fond jaune | Hypothèse à saisir |
| Texte noir | Formule, à ne pas écraser |
| Texte vert | Lien depuis un autre onglet |

Ordre de travail conseillé :

1. Onglet « Paramètres du fonds » : enveloppe, profil, critères, pays, pondérations, taux de réalisation.
2. Onglet « Pipeline de projets » : une ligne par candidat.
3. Lecture de l'onglet « Éligibilité & notation », puis de l'onglet « Allocation ».
4. Lecture du « Tableau de bord portefeuille » et contrôle de l'onglet « Contrôles ».
5. En cours de vie du fonds, mise à jour de l'onglet « Suivi MRV ».

## 3. Architecture du classeur {#architecture}

| Onglet | Contenu | Saisie |
|---|---|---|
| « Commencer ici » | Démarche, méthode, simplifications | Non |
| « Paramètres du fonds » | Enveloppe, profil de soutien, éligibilité, pays, pondérations, taux de réalisation | Oui |
| « Pipeline de projets » | Données des projets candidats, jusqu'à 25 | Oui |
| « Éligibilité & notation » | Tests, soutien maximal, demande, indicateurs, scores, rang | Non |
| « Allocation » | Allocation séquentielle par rang | Non |
| « Décaissements » | RBF, subventions, trésorerie du fonds par année | Non |
| « Suivi MRV » | Raccordements vérifiés, RBF acquis et restant dû | Oui |
| « Tableau de bord portefeuille » | Synthèse, verdicts, graphiques | Non |
| « Contrôles » | Douze contrôles d'intégrité | Non |

Les onglets de projets partagent la même structure : un projet occupe la même ligne dans le pipeline, l'éligibilité, les décaissements et le suivi MRV. Cette correspondance simplifie l'audit des formules.

## 4. Paramétrer le fonds {#parametres}

### 4.1 Enveloppe et limites

| Paramètre | Rôle |
|---|---|
| « Taille totale du fonds » | Ressources totales du guichet |
| « Coûts de gestion du fonds et MRV » | Part de la taille du fonds non allouée aux projets |
| « Guichet d'assistance technique » | Part réservée à l'assistance technique |
| « Taux de surengagement » | Permet d'engager au-delà des fonds disponibles, en anticipant que certains raccordements ne seront pas réalisés |
| « Autoriser le financement partiel du projet marginal ? (1 = oui) » | Si 0, un projet qui ne tient pas dans le reliquat est écarté et le suivant est testé |
| « Part maximale de l'enveloppe par projet » | Plafond de concentration par projet |
| « Part maximale de l'enveloppe par pays » | Plafond de concentration par pays |
| « Tolérance d'additionnalité au-delà du déficit de viabilité » | Marge admise entre la demande et le déficit de viabilité du projet |

L'enveloppe d'allocation est égale aux fonds disponibles pour les projets multipliés par le taux de surengagement. Le surengagement n'est prudent que si la sous-réalisation attendue le couvre. Le chapitre 7 montre comment le vérifier.

### 4.2 Profil de soutien

Le « Profil actif » se choisit parmi trois profils génériques et un profil « Personnalisé ». Chaque profil définit :

* un RBF par raccordement pour chaque type de client (ménage, usage productif, commerce, institution) ;
* une subvention d'investissement en part du CAPEX du projet ;
* un plafond de soutien public toutes sources confondues, en part du CAPEX ;
* un plafond de soutien par projet ;
* la tranche de RBF versée à la vérification et le délai de vérification.

La tranche restante est versée un an plus tard, après un contrôle de continuité de service. Une partie du paiement dépend ainsi du maintien du service, en plus du raccordement.

Pour reproduire les règles publiées d'un programme existant, utilisez le profil « Personnalisé ». Les profils génériques ne décrivent aucun programme réel.

Deux paramètres décrivent le rythme de vérification des raccordements : la part vérifiée l'année de mise en service et la part cumulée à la fin de l'année suivante. Le solde est vérifié la troisième année.

### 4.3 Critères d'éligibilité

Huit critères peuvent être activés ou désactivés individuellement :

| Critère | Intention |
|---|---|
| Nombre minimal de raccordements | Écarter les projets trop petits pour justifier les coûts de vérification |
| CAPEX maximal par raccordement | Écarter les projets au coût unitaire excessif |
| Part renouvelable minimale | Garantir le caractère bas carbone du soutien |
| Cofinancement privé minimal | Exiger un engagement du développeur et des prêteurs |
| Stade de maturité minimal | Réserver le soutien aux projets prêts à construire |
| Tarif moyen maximal | Protéger la capacité de paiement des clients |
| Part minimale d'usages productifs | Favoriser les projets qui créent de l'activité économique |
| Pays éligible | Respecter le périmètre géographique du fonds |

La liste des pays se tient dans le tableau dédié, avec O pour éligible et N pour non éligible. Le nom du pays saisi dans le pipeline doit être identique, sans espace superflu.

### 4.4 Pondérations de notation

Huit critères de notation sont pondérés. Le total doit faire 100 %, ce que vérifie un contrôle. Les pondérations livrées sont des exemples : elles doivent refléter la doctrine du fonds et, idéalement, être fixées avant la réception des candidatures.

### 4.5 Taux de réalisation selon le risque

Le tableau associe à chaque note de risque, de 1 à 5, la part des raccordements cibles que le fonds s'attend à voir réalisée. Ce taux réduit les décaissements RBF attendus. Calibrez-le sur l'historique du fonds ou de programmes comparables.

## 5. Renseigner le pipeline {#pipeline}

Chaque ligne décrit un projet : nom, pays, développeur, technologie, maturité, expérience du développeur, note de risque, année de mise en service, raccordements par type, CAPEX, fonds propres du développeur, dette obtenue, autres subventions, tarif moyen, part renouvelable, CO2 évité sur la durée de vie.

Deux colonnes sont facultatives :

* le « Déficit de viabilité (modèle Développeur) », que l'Édition Développeur calcule pour chaque projet. Il sert au test d'additionnalité ;
* le « Montant demandé (optionnel) ». S'il est renseigné, la demande retenue est le plus petit montant entre la demande et le soutien maximal.

La « Mise en service (année du fonds) » doit se situer entre les années 1 et 7, pour que l'ensemble du RBF soit versé avant la fin de l'horizon de dix ans.

## 6. Lire les résultats {#resultats}

### 6.1 Éligibilité et notation

Pour chaque projet, l'onglet affiche le résultat de chaque test (1 si le critère est respecté), puis le « Statut d'éligibilité ». Un projet rejeté indique le premier critère non respecté, par exemple « Pays non éligible » ou « Part renouvelable trop faible ».

Le soutien maximal d'un projet vaut le plus petit des quatre montants suivants :

* RBF aux taux du profil plus subvention d'investissement ;
* plafond de soutien public en part du CAPEX, diminué des autres subventions ;
* plafond par projet ;
* part maximale de l'enveloppe par projet.

Huit scores de 0 à 100 sont ensuite calculés. Le coût-efficacité, l'effet de levier, la part d'usages productifs et le CO2 par unité de soutien sont rapportés au meilleur projet éligible. La maturité, l'expérience et le risque sont notés sur une échelle absolue. L'additionnalité vaut 100 si la demande reste dans le déficit de viabilité augmenté de la tolérance, 0 si elle le dépasse, et 50 en l'absence de donnée.

### 6.2 Allocation

L'onglet « Allocation » classe les projets éligibles par score décroissant. Chaque ligne calcule l'enveloppe restante et la marge restante du pays à partir des seules lignes situées au-dessus. Le modèle évite ainsi toute référence circulaire. La colonne « Contrainte limitante » indique pourquoi un projet n'est financé que partiellement ou pas du tout : « Limite pays » ou « Enveloppe épuisée ».

### 6.3 Décaissements et trésorerie du fonds

La subvention d'investissement est versée l'année de mise en service. Le RBF de l'année t vaut :

RBF alloué × taux de réalisation × [tranche A × part vérifiée en (t − délai) + (1 − A) × part vérifiée en (t − délai − 1)]
{: .formula}

Le bloc de trésorerie suit les décaissements cumulés, les fonds disponibles restants et les engagements non décaissés. Un solde restant négatif signale que le surengagement n'est pas couvert.

### 6.4 Suivi MRV

Pendant la vie du fonds, saisissez dans l'onglet « Suivi MRV » les raccordements vérifiés et le RBF payé à date pour chaque projet. Le modèle compare l'avancement au profil attendu pour l'« Année de reporting du fonds » et attribue un statut :

| Statut | Règle |
|---|---|
| « Dans les temps » | Avancement au moins égal à 90 % de l'attendu |
| « En retard » | Entre 60 % et 90 % de l'attendu |
| « Hors trajectoire » | Moins de 60 % de l'attendu |
| « Non démarré » | Mise en service postérieure à l'année de reporting |

Le « RBF restant dû » correspond au RBF acquis multiplié par la tranche versée à la vérification, diminué des paiements déjà effectués. La seconde tranche devient exigible après le contrôle de continuité de service.

### 6.5 Tableau de bord portefeuille

Le tableau de bord regroupe les engagements, le pipeline, l'impact financé, l'effet de levier, le coût-efficacité, le risque et la concentration, ainsi que quatre verdicts : taux d'engagement de l'enveloppe, couverture des décaissements par les fonds disponibles, concentration par pays, additionnalité.

L'impact et l'effet de levier d'un projet partiellement financé sont attribués au prorata de la part de sa demande couverte par le fonds.

## 7. Exemple commenté {#exemple}

L'exemple est entièrement fictif : fonds, pays et projets. Il est livré sans surengagement (taux de 1,00).

| Grandeur | Valeur |
|---|---|
| Taille du fonds | 3 000 000 USD |
| Disponible après gestion (7 %) et assistance technique (8 %) | 2 550 000 USD |
| Enveloppe, sans surengagement | 2 550 000 USD |
| Candidats et projets éligibles | 14 candidats, 8 éligibles |
| Demandes des projets éligibles | 2 997 500 USD, soit une sursouscription de 1,18 |
| Allocation | 2 550 000 USD, dont 753 311 USD de RBF et 1 796 689 USD de subventions |
| Raccordements financés | environ 7 960, pour 32 100 personnes desservies |
| CO2 évité sur la durée de vie | environ 50 060 tCO2 |
| Capitaux privés mobilisés | 4 322 786 USD, soit 1,70 par unité allouée |
| Allocation par raccordement | 320 USD |
| Décaissements attendus | 2 505 383 USD, pour 2 550 000 USD disponibles |

Six candidats sont rejetés, chacun avec son motif : pays non éligible, part renouvelable insuffisante, maturité insuffisante, CAPEX par raccordement trop élevé, taille insuffisante, usages productifs insuffisants.

Deux projets ne sont que partiellement financés. Le projet N est limité par le plafond pays : le pays B atteint exactement 50 % de l'enveloppe. Le projet B est limité par l'épuisement de l'enveloppe.

Les quatre verdicts du tableau de bord sont positifs. Le désengagement attendu, soit 44 617 USD de RBF qui ne seront pas versés faute de raccordements, laisse une marge de trésorerie du même montant.

### Faut-il surengager ?

Le tableau de bord indique que la sous-réalisation attendue couvre un surengagement d'environ 1,02 seulement. La raison tient à la structure du soutien : environ 70 % de l'allocation prend la forme de subventions d'investissement, versées en totalité à la mise en service, et seul le RBF subit la décote de réalisation.

Pour le vérifier, portez le taux de surengagement à 1,10. L'enveloppe passe à 2 805 000 USD, les décaissements attendus atteignent 2 756 447 USD et dépassent les 2 550 000 USD disponibles. Le verdict sur la trésorerie devient alors négatif. Un surengagement n'est donc défendable qu'avec un profil où le RBF pèse davantage.

## 8. Contrôles d'intégrité {#controles}

| Contrôle | Signification d'une alerte |
|---|---|
| « Les pondérations totalisent 100 % » | Pondérations à corriger |
| « Allocation dans la limite de l'enveloppe » | Formule d'allocation modifiée |
| « Aucune allocation à un projet non éligible » | Formule d'éligibilité modifiée |
| « Chaque projet éligible classé une seule fois » | Formule de rang modifiée |
| « Limite par pays respectée » | Formule d'allocation modifiée |
| « Décaissements attendus par année = subventions + RBF x réalisation attendue (tout versé pendant la durée du fonds) » | Mise en service trop tardive ou délai de vérification trop long |
| « Profil de vérification valide (0 <= année 1 <= cumul année 2 <= 100 %) » | Paramètres de vérification incohérents |

En cas d'alerte sur une formule modifiée, restaurez le fichier à partir d'une copie vierge.

## 9. Limites d'emploi {#limites}

Ces limites résultent d'une revue critique du modèle.

1. Normalisation relative. Plusieurs scores sont rapportés au meilleur projet éligible. L'ajout ou le retrait d'un candidat modifie donc les scores des autres et peut, à la marge, inverser deux rangs. Figez le pipeline avant la notation définitive.
2. Allocation gloutonne. Le financement suit l'ordre des scores. Ce n'est pas une optimisation sous contrainte : une autre combinaison de projets pourrait produire davantage de raccordements pour la même enveloppe.
3. Subventions supposées entièrement versées. Le risque de non-achèvement d'un projet n'est pas représenté pour la subvention d'investissement.
4. Profil de vérification commun à tous les projets, sur trois ans.
5. Attribution au prorata. L'impact d'un projet partiellement financé est attribué au fonds en proportion de sa part. D'autres conventions d'attribution existent chez les bailleurs.
6. Pas de change, pas de reflux, pas de rendement financier : le modèle traite un fonds de subvention et de RBF, pas un fonds de prêt.
7. Données déclaratives. Les données du pipeline proviennent des candidats. Leur fiabilité dépend de la due diligence.

## 10. Glossaire {#glossaire}

| Terme | Définition |
|---|---|
| Enveloppe d'allocation | Plafond des engagements, égal aux fonds disponibles multipliés par le taux de surengagement |
| Surengagement | Engagement au-delà des fonds disponibles, en anticipant une sous-réalisation |
| Désengagement | Part des engagements qui ne sera pas décaissée, faute de résultats |
| Additionnalité | Le soutien ne dépasse pas ce dont le projet a besoin pour être viable |
| Effet de levier | Capitaux privés mobilisés par unité de soutien du fonds |
| Taux de réalisation | Part des raccordements cibles effectivement réalisée et vérifiée |
| Tranche à la vérification | Part du RBF versée dès la vérification du raccordement |
| MRV | Mesure, rapportage et vérification des résultats |
| Sursouscription | Rapport entre les demandes éligibles et l'enveloppe |

## 11. Avertissement et licence {#licence}

Le modèle est un outil de sélection et de planification de portefeuille. Il ne constitue pas un conseil en investissement, juridique ou fiscal. Les fonds, pays et projets de l'exemple sont fictifs.

La licence est accordée pour un utilisateur ou une organisation. La revente, la redistribution et la publication du fichier ou du présent manuel sont interdites.
