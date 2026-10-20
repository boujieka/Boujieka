# Analyse critique et propositions d'amélioration du plan pour le Cameroun

**20 octobre 2026.** Analyse indépendante, sans mandat officiel. Elle porte sur trois documents soumis :
le **Plan stratégique 2027-2029** (rapport pour la Présidence, 36 mois), le **Programme politique pour le
Cameroun Nouveau** (11 axes) et le livre **« Le Libéralisme solidaire pour un Cameroun Nouveau »**
(plan septennal 2026-2033 et vision 2043). Elle intègre aussi les douze propositions ajoutées par le
commanditaire.

Pièces justificatives : `analyses/verification_plan_strategique.md` (vérification de 14 affirmations),
`analyses/notes/propositions_utilisateur_recherche.md` (recherche sur les propositions ajoutées),
`outputs/coherence_plan.csv` (contrôles chiffrés, script `models/coherence_plan.py`) et le diagnostic
national du 19/10/2026. Les références entre crochets renvoient au registre des sources.

## 1. Synthèse

1. **Le Plan stratégique 2027-2029 est la meilleure base de travail.** Il désigne les bons nœuds :
   trésorerie de l'État, retour vers les bailleurs multilatéraux, subventions aux carburants, arriérés
   intérieurs, entreprises publiques. C'est aussi ce que conclut notre propre diagnostic.
2. **Il contient des erreurs factuelles qui le rendent contestable en l'état.**
   - Les **taux de pauvreté des neuf régions qu'il cite sont tous faux** au regard de l'ECAM5 de l'INS.
   - Le tonnage de riz importé est faux.
   - Les 703,5 Mds FCFA d'arriérés sont une estimation provisoire de fin avril 2026, reprise à fin juin (vérification du 20/10).
   - D'autres chiffres doivent être nuancés.
   Un document destiné au chef de l'État ne peut pas circuler avec ces erreurs.
3. **Son cadrage chiffré n'est pas cohérent.**
   - Le scénario central suppose environ **2 950 Mds FCFA de recettes non pétrolières supplémentaires
     sur trois ans**. Seuls **450 Mds** sont expliqués par des mesures.
   - La croissance de 5,5 % en 2029 attribuée à la bauxite n'est pas crédible : 5 Mt de bauxite
     représentent environ 0,4 % du PIB.
4. **Le Programme politique et le Livre portent une vision et des valeurs utiles :** réconciliation,
   mémoire, unité, diaspora, décentralisation. Mais plusieurs de leurs mesures sont
   **financièrement impossibles ou contradictoires avec le Plan** :
   - un **Fonds souverain de 10 000 Mds FCFA par an**, soit 29 % du PIB et 9,7 fois les recettes
     extractives ;
   - **+30 % sur les salaires publics**, soit environ 488 Mds par an ;
   - une **monnaie nationale** et un **contrôle des capitaux**, qui relèvent de la CEMAC et sont
     incompatibles avec un programme FMI.
5. **Sur les douze propositions ajoutées, huit sont retenues sous une forme rendue exécutable, trois sont
   à reformuler et une est déconseillée** :
   - retenues : audits, recensement, réforme de la santé et de l'éducation, mémoire nationale,
     recouvrement des avoirs, suites des dossiers CAN et Covid, renouvellement des dirigeants
     d'entreprises publiques par application de la loi ;
   - à reformuler : arrêt des importations, financement « centré » sur les matières premières,
     villes nouvelles ;
   - déconseillée : la peine de mort pour les crimes financiers. Elle n'est **pas prévue** par le Code
     pénal pour le détournement, ne réduit pas la corruption de façon démontrée et **bloquerait le
     recouvrement des avoirs à l'étranger**, que vous demandez par ailleurs.
6. **Proposition :** fusionner les trois documents en **un seul programme en 8 chantiers** (section 7).
   Le Plan sert de cadre d'exécution 2027-2029 ; la vision du Programme et du Livre est conservée pour
   2035-2043, mais chaque mesure doit passer un **test de financement**.

## 2. Les trois documents se contredisent sur des points décisifs

| Sujet | Plan stratégique 2027-2029 | Programme politique | Livre « Libéralisme solidaire » | Arbitrage proposé |
|---|---|---|---|---|
| Relation avec le FMI | Nouveau programme FEC/MEDC/FRD dans les 100 jours | Non traité ; « souveraineté monétaire » | « Partenariats » avec les institutions financières | Programme FMI : c'est le seul financement concessionnel disponible à court terme |
| Monnaie | Franc CFA maintenu (implicite) | Monnaie nationale remplaçant le franc CFA | Non traité | Écarter de l'horizon 2027-2029. Une sortie de la BEAC exige des réserves propres et un accord CEMAC. C'est un débat de long terme, à préparer par une étude indépendante |
| Mouvements de capitaux | Non traité | Non traité | Contrôle des capitaux | La réglementation des changes est communautaire (CEMAC). Retenir plutôt la lutte anti-blanchiment et la sortie de la liste grise du GAFI |
| Salaires publics | Non traité (rappels enseignants) | Non traité | +30 % pour tous les agents | Pas de hausse générale avant l'assainissement. Payer d'abord les arriérés dus et revaloriser de façon ciblée (enseignants et soignants en zone rurale) |
| Fonds souverain | Non | 10 000 Mds/an issus des ressources naturelles | Non | Fonds de stabilisation des recettes extractives, alimenté seulement au-delà d'un prix de référence (section 6.4) |
| Électricité | Contrats de performance, dettes croisées | Non traité | +10 000 MW d'ici 2033 ; 20 000 MW en 2043 | Priorité au réseau, aux pertes et au recouvrement. La capacité actuelle (≈2 280 MW) est sous-utilisée faute de lignes |
| Entreprises publiques | Contrats de performance, triage | Contrôle majoritaire de l'État dans les secteurs stratégiques | Restructuration de 15 entreprises | Application de la loi de 2017, audits, triage au cas par cas (section 6.1) |
| Carburants | Fin progressive des subventions + transferts ciblés | Non traité | Non traité | Retenir le Plan, avec un ciblage renforcé (section 7, chantier 2) |
| Paix (Nord-Ouest et Sud-Ouest) | Conseil ministériel extraordinaire | Forum, Commission Vérité-Justice-Réconciliation, désarmement-démobilisation-réintégration (DDR), réparations | États généraux, dialogue « y compris séparatistes » | Le Programme est le plus complet. Il faut l'intégrer au Plan, qui n'a presque rien sur la paix |

## 3. Erreurs factuelles du Plan stratégique à corriger

Chaque point a été vérifié le 20/10/2026. Le détail figure dans `verification_plan_strategique.md`.

| Affirmation du plan | Verdict | Correction |
|---|---|---|
| Pauvreté par région : Nord 48,5 %, Adamaoua 41,2 %, Est 39,4 %, Centre 17,9 %, Littoral 15,2 %, Sud 22,4 %, Ouest 28,7 %, Nord-Ouest 57,8 %, Sud-Ouest 38,6 % | **Faux (les 9 valeurs)** | ECAM5 2022 (INS, brochure p. 8) : Extrême-Nord 69,2 ; Nord-Ouest 66,8 ; Nord 61,1 ; Adamaoua 45,1 ; Est 41,5 ; Ouest 30,4 ; Littoral hors Douala 23,8 ; Sud-Ouest 20,4 (non représentatif) ; Centre hors Yaoundé 19,1 ; Sud 14,9 ; Yaoundé 10,8 ; Douala 8,3 [VPL-25] |
| Sous-emploi « supérieur à 65 % » | Faux | 56,4 % (EESI3 2021, nouvelle approche) ou 61,4 % (ancienne approche) [VPL-26] |
| Riz importé en 2024 : 648 000 t | Faux | 831 337 t pour 318,6 Mds FCFA. Le chiffre de 648 048 t est la hausse des quantités totales importées [VPL-23] |
| Restes à payer : 703,5 Mds FCFA fin juin 2026 | Partiel (vérification finale) | Estimation provisoire de fin avril 2026, reprise dans la note CAA de fin juin selon la presse. Le stock total de restes à payer était de 1 026,3 Mds fin mars 2026, dont 452,5 Mds de plus de 3 mois [VFF-001, VFF-004] |
| Coût d'importation du gasoil de 975 FCFA/l associé au soutien de septembre | Période erronée | 975 FCFA/l correspond à la structure d'octobre ; septembre : 860,10 FCFA/l. Les 57 Mds de septembre sont confirmés [VPL-03 à 05] |
| « 3 % seulement des subventions retracées » (Chambre des comptes) | Douteux | Ce chiffre ne figure que dans un titre de presse au sens ambigu. Le rendement de 2,92 % est confirmé [VPL-06, 07] |
| Glencore : 7 Mds FCFA (11 M USD), 2007-2018 | Imprécis | Le SFO retient 10,5 M EUR (13,7 M USD) versés entre 2012 et 2015 à des agents de la SNH et de la SONARA. La période 2007-2018 couvre l'ensemble des pays [VPL-13] |
| Le FMI (1er octobre 2026) appelle à un nouveau programme | Non dit | Le communiqué de la mission post-financement ne mentionne ni nouveau programme ni arriérés ; passage au Conseil en décembre 2026 [VPL-09] |
| Dette enseignante « supérieure à 180 Mds » | Revendication | 180 Mds est le chiffre des syndicats OTS. L'État l'évaluait à 140,5 Mds, dont 105 Mds restaient dus en juin 2023 [VPL-22] |
| Permis de Minim-Martap du 16/09/2024 | Date à corriger | Signé le 02/09/2024, remis le 13/09/2024 [VPL-17] |

**Confirmés :**
- dégradation par Fitch à B- le 16/10/2026 ;
- Eurobond 2033 à 10,65 % le 19/10/2026 ;
- dette de 15 607 Mds FCFA (44,2 % du PIB) fin juin 2026 ;
- loi forestière n° 2024/008 (interdiction des grumes, art. 97) ;
- PAEPYS (300 000 m³/j) ;
- limite de 9 ans pour les mandats des directeurs généraux (lois 2017/010 et 2017/011).

## 4. Incohérences internes et hypothèses trop optimistes du Plan

Calculs reproductibles : `models/coherence_plan.py`.

1. **Recettes non expliquées.** Le scénario central dépasse le scénario de référence de 2 950 Mds FCFA
   de recettes non pétrolières sur 2027-2029. Or le schéma de financement n'attribue que 450 Mds aux
   mesures fiscales. Il manque donc environ **2 500 Mds** de mesures pour justifier la trajectoire.
   En 2029, les recettes non pétrolières atteindraient environ 16,5 % du PIB, contre environ 13 %
   aujourd'hui (estimation).
2. **Croissance de 5,5 % en 2029.** Elle est attribuée à la bauxite, à Nachtigal et au BTP. Or 5 Mt de
   bauxite ne valent qu'environ 135 Mds FCFA (≈0,4 % du PIB, sur une hypothèse de 45 USD/t). Le Plan
   admet lui-même 3 à 5 ans de retard typique sur les projets ferroviaires. **Proposition :** central
   à 4,0-4,5 %, optimiste à 5,5 %.
3. **Eurobond sous 6,5 % en 2029.** Cette cible est très ambitieuse pour un émetteur noté B-. À
   présenter comme scénario favorable, pas comme cible de pilotage.
4. **Riz.** La cible de 400 000 t est présentée comme « plus de 50 % de la consommation ». Or les seules
   importations atteignent 869 039 t en 2025. La cible couvrirait au mieux environ 40 %.
5. **Dotation générale de la décentralisation (DGD).** Le tableau d'arbitrage annonce +120 Mds par an,
   la fiche 6.2 environ +257 Mds dès 2027. Par ailleurs, l'objectif final de 12 % reste **sous le
   plancher légal de 15 % des recettes** (et non « du budget »). Le Plan doit soit atteindre la loi,
   soit proposer de la modifier.
6. **Double compte possible.** Le « redéploiement budgétaire net » de 1 200 Mds est compté comme une
   *source* de financement. Il réduit aussi le déficit dans le tableau macro. Il faut présenter un seul
   tableau emplois-ressources où chaque économie n'apparaît qu'une fois.
7. **Partenariats public-privé « sans garantie souveraine » (720 Mds).** Les passifs conditionnels
   atteignent déjà 14 % du PIB [MAC-009]. Chaque PPP doit chiffrer les loyers futurs, les garanties de
   trafic ou de demande et les clauses de résiliation.
8. **Ciblage des transferts trop étroit.** 300 000 ménages pour compenser la hausse des carburants,
   alors qu'environ 10,1 millions de personnes sont pauvres. Le registre social unifié n'a pas
   d'effectif publié. Le ciblage doit reposer sur le RGPH4 (résultats début 2027) et sur le registre
   des filets sociaux existant (44 500 ménages servis fin 2024) [SOC-015].

## 5. Ce qui manque au Plan

- **Électricité.** Le Plan traite ENEO comme une entreprise publique parmi d'autres. Il n'y a pas de
  fiche sur les pertes (≈30 % [VFF-015]), le recouvrement (72 à 77,5 %), l'écart tarif-coût (le tarif couvre ≈80 % du coût),
  le contrat Nachtigal (paiement garanti même si l'énergie n'est pas utilisée), la ligne Nachtigal–Douala
  ou la protection des petits consommateurs.
- **Paix et sécurité.** Rien de substantiel sur le Nord-Ouest, le Sud-Ouest et l'Extrême-Nord, alors
  qu'ils concentrent la pauvreté la plus forte et 2,9 millions de personnes dans le besoin [GOV-001].
- **Santé.** Le diagnostic sur la couverture santé universelle (CSU) est bon, mais il n'y a pas de fiche
  de financement.
- **Base juridique et autorité compétente.** Plusieurs mesures sont attribuées au « Chef de l'État par
  décret » alors que la loi désigne d'autres autorités :
  - les directeurs généraux d'**établissements publics** sont nommés par décret (loi 2017/010, art. 35). Pour les
    **entreprises publiques**, la loi confie la nomination au **conseil d'administration** (loi 2017/011, art. 70),
    mais la pratique du décret existe (CAMTEL, par exemple) : point à trancher ;
  - les recettes et dépenses nouvelles exigent une **loi de finances** (Parlement) ;
  - la monnaie et les changes relèvent de la **CEMAC**.
- **Contexte institutionnel.**
  - Le poste de vice-président est créé mais non pourvu, motif explicite de la dégradation par Fitch.
  - Le mandat des députés est prorogé au 20/12/2026, sans date de scrutin connue.
  - Le Plan doit dire quelles réformes exigent le Parlement et comment les sécuriser en cas de
    transition.
- **Indicateurs sociaux.** Le tableau de bord ne suit que des indicateurs financiers et d'infrastructure.
  Il faut ajouter la pauvreté, la scolarisation, la santé maternelle et le délai de paiement des
  enseignants.

## 6. Les propositions ajoutées : analyse et version améliorée

### 6.1 Remplacer tous les dirigeants des entreprises et établissements publics

**Ce qui est établi**
- La loi limite les mandats des directeurs généraux à 3 ans renouvelables deux fois, soit 9 ans au plus.
  Les actes pris au-delà sont « nuls » (loi 2017/011, art. 70 ; loi 2017/010, art. 36) [VPL-27, 28].
- Pour les dirigeants en poste depuis 2017, le plafond a été atteint au plus tard le **12/07/2026**.
- Une étude universitaire (juin 2026, non officielle) recense **36 directeurs généraux et 77 présidents
  de conseil d'administration hors délai** [PRP-44].
- La Chambre des comptes relève un rendement de 2,92 % sur environ 1 911 Mds de participations
  [VPL-06].

**Risques d'un remplacement en bloc**
- Rupture de continuité dans des services vitaux : électricité, eau, ports.
- Remplacement par fidélité plutôt que par compétence.
- Contentieux pour les mandats en cours.

**Version proposée**
- **Jours 1-30.** Constater la caducité de tous les mandats dépassant 9 ans et pourvoir ces postes par
  intérim (application de la loi, aucun texte nouveau requis). Publier la liste nominative des
  mandats et de leurs échéances.
- **Jours 30-120.**
  - Appel public à candidatures pour chaque poste, avec un cabinet de recrutement indépendant et une
    liste restreinte de trois noms transmise au conseil d'administration ou à l'autorité de
    nomination.
  - Déclaration de patrimoine à l'entrée en fonction.
  - Contrat de performance triennal publié.
- **Audit de passation obligatoire** à chaque départ, conduit par la Chambre des comptes ou un cabinet
  agréé. Il protège les sortants honnêtes et sécurise les entrants.
- **Les autres dirigeants** (moins de 9 ans) sont évalués sur l'audit et le contrat de performance. Ils
  ne sont remplacés que sur résultats.
- **Indicateur :** part des entreprises et établissements publics dont le dirigeant est dans les délais
  légaux et a été recruté sur appel public (départ inconnu ; cible 100 % à 12 mois).

### 6.2 Audits

**Retenu.** Audit flash, dans les 100 jours, des **15 entités au risque budgétaire le plus élevé**
(SONARA, SOCADEL/ENEO, SONATREL, CAMWATER, CAMTEL, SNH, CAMAIR-CO, ports…), sous l'autorité de la
Chambre des comptes, appuyée par des cabinets internationaux. S'y ajoutent :
- l'audit de certification des restes à payer, avec rejet des prestations fictives (comme dans le Plan) ;
- l'audit des dettes croisées du secteur électrique.

Tous les rapports sont **publiés**. Sans publication, l'audit ne change pas les comportements :
seuls 12 dossiers Covid ont été transmis à la justice en 2021, et aucune condamnation n'a été
retrouvée à ce jour [PRP-36].

### 6.3 Récupérer les biens mal acquis avec la communauté internationale

**Ce qui est établi**
- Le Cameroun a ratifié la Convention des Nations unies contre la corruption en 2006 [PRP-19].
- Son article 57 prévoit la restitution des fonds publics détournés, mais **sur la base d'un jugement
  définitif dans le pays requérant** [PRP-20].
- Précédent : le Nigeria a récupéré 321 M USD des avoirs Abacha auprès de la Suisse en 2017, près de
  20 ans après les faits, avec un suivi de la Banque mondiale [PRP-21].
- Au Cameroun, le Tribunal criminel spécial (TCS) a fait reverser 9,5 Mds FCFA en 2024 et 10,2 Mds en
  2025 au titre du « corps du délit », selon le Premier ministre [PRP-27, 28].
- Aucune demande camerounaise d'entraide ou de restitution à l'étranger n'a été retrouvée.

**Version proposée**
1. Créer une **cellule nationale de recouvrement des avoirs**, adossée au TCS et à l'agence de
   renseignement financier (ANIF), avec l'appui de l'initiative StAR (Banque mondiale et ONUDC).
2. Adopter une **loi de confiscation sans condamnation pénale préalable** (action civile in rem), avec
   les garanties du contradictoire.
3. Signer des accords d'entraide avec la France, la Suisse, le Royaume-Uni et les Émirats.
4. Prévoir un **mécanisme de restitution transparent**, sur le modèle de la loi française de 2021 :
   les fonds restitués vont à des programmes sociaux suivis publiquement.

**Règle budgétaire : ne jamais inscrire de recettes de recouvrement dans le financement du plan.** Les
délais se comptent en années et les montants sont incertains. Toute somme récupérée réduit la dette.

### 6.4 Centrer le financement de l'économie sur les ressources naturelles

**Constat**
- Les recettes pétrolières ne représentent que **11 %** des recettes internes (567 Mds sur 5 008 Mds
  en 2025) et baissent : −17,6 % en 2025, −34,6 % au premier trimestre 2026 [MAC-009].
- Le pays est devenu **importateur net de pétrole hors gaz en 2024** [ECO-07].
- La bauxite et le fer ne produisent pas encore. Une interdiction d'exporter du minerai brut ne crée de
  la valeur que si l'électricité et le rail suivent.
- Faire reposer le financement de l'État sur des recettes volatiles et en déclin exposerait le budget à
  chaque baisse des cours, comme en 2015-2016.

**Version proposée : mieux capter et mieux gérer la rente, sans la rendre centrale**
- Revoir les conventions minières (Minim-Martap, Mbalam, Lobé) avec des clauses de transparence et de
  transformation locale réalistes.
- Publier les contrats (norme ITIE).
- Faire entrer la production d'or artisanal dans le circuit officiel.
- Contrôler les volumes exportés de la SNH par les statistiques miroir des pays acheteurs.
- **Règle de gestion des recettes extractives :** le budget n'intègre que les recettes calculées à un
  prix de référence prudent. L'excédent alimente un **fonds de stabilisation et d'investissement**
  géré selon les principes de Santiago (gouvernance séparée, publication trimestrielle). C'est la
  version réaliste du « Fonds Ouandié », dont le nom peut être conservé. Taille réaliste : de quelques
  dizaines à quelques centaines de Mds FCFA par an selon les prix, pas 10 000 Mds.
- La base de financement durable reste la **fiscalité non pétrolière** :
  - la réduction des dépenses fiscales (estimées par le Plan à 200-250 Mds par an, chiffre à
    vérifier) ;
  - le cadastre et le foncier ;
  - la numérisation de l'impôt.

### 6.5 Arrêter l'importation de riz, de poisson et de blé

**Constat**
- Importations 2025 [ECO-03] :
  - riz : 869 039 t ;
  - blé : 1 139 403 t ;
  - poisson congelé : 267 259 t.
- Production nationale, selon des chiffres de presse à confirmer :
  - riz : environ 140 000 t d'offre selon la presse, mais 410 000 t de paddy en 2024 selon le MINFI (sources incompatibles, vérification finale) ;
  - poisson : environ 198 000 t sur neuf mois de 2025 ;
  - blé : quasi nulle.
- **Un arrêt immédiat provoquerait pénuries et flambée des prix**, d'abord pour les ménages urbains
  pauvres. Exemple : au Nigeria, la fermeture des frontières en 2019 a fait monter le riz local
  d'environ 9 % en un mois [PRP-67].
- Il alimenterait la contrebande, surtout à la frontière nigériane.
- Il contreviendrait aux engagements OMC (GATT art. XI ; Accord sur l'agriculture art. 4.2), à l'APE
  avec l'UE et à la ZLECAf [PRP-58 à 62].

**Version proposée : « substitution programmée »**
- **Objectifs de production chiffrés par filière** :
  - riz : réhabilitation des périmètres irrigués SEMRY, semences IRAD ;
  - poisson : aquaculture, avec un objectif officiel de 600 000 t en 2027 à revoir de façon réaliste ;
  - maïs et manioc comme substituts partiels du blé, via l'incorporation de farines locales dans le
    pain.
- **Protection progressive et légale** : droits de douane dans la limite des taux consolidés, clauses
  de sauvegarde de l'APE, achats publics (cantines, armée, hôpitaux) réservés à la production locale.
- **Réduction des importations par paliers** une fois les seuils de production atteints et vérifiés.
- **Stock alimentaire de sécurité.**
- **Indicateur :** part de la production nationale dans la consommation de riz. Départ estimé environ
  14 à 30 % selon les sources (à établir) ; cible à 3 ans de +15 points (proposée, à calibrer).

### 6.6 Réformer l'éducation et la santé

**Retenu et précisé.** Le Livre propose des « états généraux », mais l'urgence est de financer et
d'exécuter ce qui est connu.

**Éducation**
- Solder la dette due aux enseignants (105 Mds restants en 2023, à actualiser) sur un calendrier
  publié.
- Automatiser l'intégration (salaire complet dès la première affectation).
- Adopter le statut particulier.
- Mesurer les apprentissages : PASEC et évaluation nationale, puisque 71,9 % des enfants sont en
  « pauvreté des apprentissages » (2019) [SOC-006].
- Reconstruire les écoles du Nord-Ouest et du Sud-Ouest : environ 45 % sont non fonctionnelles [GOV-001].

**Santé**
- Financer la CSU par des accises dédiées (tabac, alcool, boissons sucrées).
- Payer les formations sanitaires sous 60 jours.
- Assurer la gratuité effective des soins maternels et infantiles.
- Recruter des personnels pour les zones rurales.
- Indicateur de départ : les ménages paient directement 67,7 % de la dépense de santé (2023)
  [SOC-006].

Les « centres d'excellence » et universités « de classe mondiale » du Livre viennent **après** les soins
primaires. La mortalité infantile atteint 133 ‰ dans le Nord [SOC-005].

### 6.7 Exécuter la peine de mort contre les criminels financiers (« modèle chinois »)

C'est votre décision. Voici les faits et les conséquences.

**Faits**
- Le Code pénal de 2016 maintient la peine de mort, mais **l'article 184 (détournement) prévoit au
  maximum la réclusion à vie**, dès 500 000 FCFA détournés. La confiscation est obligatoire [PRP-01].
- Le Cameroun n'a procédé à aucune exécution depuis 1997, ou 1988 selon une autre source. Il est
  « abolitionniste en pratique » selon Amnesty [PRP-02 à 04].
- Il faudrait donc **modifier le Code pénal**, ce qui relève de la loi et donc du Parlement.

**Arguments avancés en faveur**
- Signal de rupture.
- Attente populaire de sanctions exemplaires.
- Effet dissuasif supposé.

**Pourquoi nous déconseillons cette mesure**
1. **Aucune preuve d'efficacité.** La Chine exécute des responsables corrompus (Lai Xiaomin en 2021)
   mais reste à 43/100 à l'indice de perception de la corruption, score inchangé [PRP-16, 17]. Ce qui
   dissuade, c'est la **certitude** d'être poursuivi et de perdre ses biens, pas la sévérité maximale.
2. **Elle bloquerait le recouvrement des avoirs.** La France, la Suisse, le Royaume-Uni et l'UE
   refusent l'extradition, et souvent l'entraide, lorsque la peine de mort est encourue sans garantie
   qu'elle ne sera pas appliquée [PRP-08 à 15]. Les fonds détournés se trouvent précisément dans ces
   pays. La mesure annulerait la proposition 6.3.
3. **L'erreur judiciaire et l'usage politique seraient irréversibles** dans un système judiciaire classé
   134e sur 143 (World Justice Project 2025) [GOV-032].
4. **Coût diplomatique et financier** auprès des partenaires dont dépend le financement concessionnel.

**Alternative proposée, plus efficace pour l'objectif visé**
- Réclusion à perpétuité effective, sans remise pour les détournements les plus graves.
- Confiscation élargie, y compris sans condamnation (6.3).
- Inéligibilité à vie et interdiction de gérer des fonds publics.
- Publication des jugements.
- Délais de jugement tenus.
- Restitution comme condition de toute réduction de peine.

### 6.8 Rendre hommage aux héros nationaux

**Retenu.** Coût faible, effet de cohésion.
- La loi de 1991 a **réhabilité** Um Nyobè, Moumié, Ouandié et Ahidjo, sans créer de statut de héros
  [PRP-53].
- La commission franco-camerounaise a remis son rapport en janvier 2025 et recommande des lieux de
  mémoire [PRP-55].

**Proposition**
- Loi instituant une **Journée nationale des héros**.
- Commission indépendante d'historiens pour établir la liste, de façon inclusive : toutes les régions,
  toutes les périodes, femmes comprises.
- Mémorial ou panthéon.
- Programmes scolaires.
- Réponse officielle au rapport franco-camerounais (accès aux archives).

### 6.9 Villes nouvelles

**À reformuler.** Les villes nouvelles africaines financées de l'extérieur ont souvent été
**sous-occupées**, avec des logements trop chers pour les ménages locaux :
- Kilamba en Angola : 220 appartements vendus sur 2 800 en 2012 ;
- Konza au Kenya : 9 parcelles développées sur 515 fin 2024 ;
- Eko Atlantic au Nigeria [PRP-69 à 71].

Au Cameroun, environ 70 % de l'expansion urbaine est informelle (estimation du Plan, à vérifier). Le
PAEPYS montre le risque d'un investissement sans réseau de distribution.

**Proposition**
- Priorité à **l'aménagement des villes existantes** : drainage, eau, voirie, titres fonciers.
- **Une seule ville nouvelle pilote**, en partenariat public-privé avec captation de la plus-value
  foncière, et seulement après une étude de demande solvable.

### 6.10 Recensement de la population

**Déjà en cours.** Le 4e recensement (RGPH4) a été collecté du 24/04 au 15/09/2026, pour 19 Mds FCFA.
Les résultats sont attendus début 2027 [PRP-49 à 51]. Nous avons corrigé notre diagnostic du 19/10 qui
l'ignorait.

**Proposition**
- Publier les taux de couverture par département. La presse a fait état de moins de 50 % de
  couverture dans le Wouri et le Mfoundi en première phase.
- Réaliser une **enquête post-censitaire indépendante**.
- Publier les résultats sous un calendrier fixe.
- Utiliser ces résultats pour le registre social, la carte scolaire et sanitaire et la répartition
  de la DGD.

### 6.11 « CAN gate »

**Fait établi.** Une sentence du CIRDI du 04/09/2026 condamne l'État dans le litige avec le
constructeur italien du stade d'Olembé. Indemnité principale d'environ 78,5 M€ plus intérêts selon la
presse ; le chiffre de « 250 Mds » n'est pas confirmé [PRP-30, 31].

**Allégations.** Les surfacturations de « 1 200 Mds » ou les coûts de « 3 500 Mds » viennent de la presse
et d'un député. Aucun audit officiel n'a été retrouvé [PRP-33].

**Proposition**
- Audit de la Chambre des comptes sur l'ensemble des marchés de la CAN 2019/2021 : coûts, avenants,
  réceptions, responsabilité de la résiliation ayant conduit à la sentence.
- Publication, puis saisine du TCS si des infractions sont constatées.
- **Négocier ou exécuter la sentence CIRDI** pour éviter des saisies d'actifs à l'étranger.

### 6.12 « Covid gate »

**Faits établis par la Chambre des comptes** [PRP-36 à 38] :
- 21,6 Mds FCFA de surcoûts sur les tests ;
- doubles paiements, travaux payés non achevés, prestations fictives ;
- 14 procédures pour faute de gestion ;
- **12 dossiers transmis à la Justice en 2021.**

**Aucune inculpation ni condamnation n'a été retrouvée** au 20/10/2026.

**Proposition**
- Exiger du ministère de la Justice un **état public des 12 dossiers** dans les 30 jours.
- Saisir le TCS pour les dossiers recevables.
- Recouvrer les surcoûts.
- Publier le rapport de suivi des 48 recommandations, annoncé en 2023 et non publié.

Les personnes visées par la presse ne sont, à ce jour, **ni inculpées ni condamnées**. Elles bénéficient
de la présomption d'innocence.

## 7. Plan amélioré : un portefeuille de 8 chantiers

Les cibles marquées « proposée » sont des propositions de l'équipe, à calibrer après réception des
données manquantes. Les autorités compétentes doivent être vérifiées dans les textes en vigueur.

| # | Chantier | Décision principale | Autorité compétente | Indicateur : départ → cible à 3 ans |
|---|---|---|---|---|
| 1 | **Stabilisation financière** | Négocier un programme FMI (FEC/MEDC/FRD) ; plan de trésorerie ; certification et apurement des arriérés ; visa de la CAA sur tout nouvel emprunt | Président (mandat de négociation), MINFI, Parlement (LFR) | Délai de paiement : > 200 j (2025) → 60 j ; stock d'arriérés certifié : à établir → −70 % (proposée) |
| 2 | **Carburants et SONARA** | Hausses trimestrielles de prix, conditionnées au versement préalable des transferts ; tarif transporteur ; restructuration de la SONARA | Gouvernement (prix administrés), MINFI, MINCOMMERCE | Soutien mensuel : 57 Mds (sept. 2026) → 0 ; ménages compensés : 44 500 → 300 000 (proposée, selon RGPH4) |
| 3 | **Électricité** | Audit des pertes et des dettes croisées ; achèvement de l'évacuation de Nachtigal ; trajectoire tarifaire avec tarif social pour les petites consommations ; contrats de performance SOCADEL/SONATREL | MINEE, ARSEL, CA SOCADEL, MINFI | Pertes de distribution : ≈27 % → 18 % (proposée) ; écart tarif-coût : 18,2 % → < 5 % ; heures de coupure : à mesurer |
| 4 | **Gouvernance publique et redevabilité** | Application de la loi 2017 aux dirigeants ; audits publiés ; cellule de recouvrement des avoirs ; suites CAN et Covid ; sortie de la liste grise du GAFI | Président, CA, Chambre des comptes, Justice, ANIF | Dirigeants dans les délais légaux : à établir → 100 % ; dossiers Covid jugés : 0/12 → 12/12 instruits |
| 5 | **Recettes et ressources naturelles** | Revue des dépenses fiscales ; règle de gestion des recettes extractives et fonds de stabilisation ; renégociation et publication des conventions minières ; traçabilité de l'or | MINFI, MINMIDT, Parlement | Pression fiscale non pétrolière : 12,9 % (2025) → 14,5 % du PIB (proposée) |
| 6 | **Souveraineté alimentaire programmée** | Investissements riz, poisson et maïs ; protection douanière légale ; achats publics locaux ; stock de sécurité | MINADER, MINEPIA, MINCOMMERCE | Part locale du riz : 14 à 30 % selon les sources (à établir) → +15 points (proposée) |
| 7 | **Capital humain** | Apurement de la dette due aux enseignants et statut ; financement de la CSU par accises ; gratuité maternelle et infantile ; évaluation des apprentissages | MINESEC, MINEDUB, MINSANTE, MINFI, Parlement | Paiements directs de santé : 67,7 % → 55 % (proposée) ; délai d'intégration des enseignants : à mesurer → 0 mois |
| 8 | **Paix et territoires** | Processus de paix Nord-Ouest/Sud-Ouest (forum, commission vérité-justice-réconciliation, DDR) ; plan Extrême-Nord ; trajectoire de la DGD vers le plancher légal de 15 %, avec audits ; exploitation du RGPH4 ; mémoire nationale | Président, Parlement, MINDDEVEL, CTD | DGD/recettes : 2,08 % (2024, selon la Chambre des comptes) → 15 % ou modification de la loi ; personnes dans le besoin : 2,9 M → en baisse |

**Les 100 premiers jours (sélection)**
- **J1-J30.** Constat de caducité des mandats échus et intérims ; ordre de mission des audits flash ;
  circulaire sur le visa de la CAA ; demande au ministère de la Justice de l'état des dossiers Covid ;
  saisine du FMI.
- **J31-J60.** Mission FMI, Banque mondiale et BAD ; premiers transferts monétaires dans l'Extrême-Nord,
  le Nord-Ouest et le Sud-Ouest *avant* tout ajustement des prix ; mandat de négociation de la sentence
  CIRDI.
- **J61-J100.** Publication du stock certifié d'arriérés ; premier palier de prix des carburants (si les
  transferts sont versés) ; projet de loi sur la confiscation des avoirs ; lancement des appels à
  candidatures pour les dirigeants ; communication publique du tableau de bord.

## 8. Règles de financement corrigées

1. Un **tableau emplois-ressources unique** pour 2027-2029, dans lequel chaque économie (carburants,
   entreprises publiques) n'est comptée qu'une fois.
2. **Aucune recette hypothétique dans le scénario central** : avoirs recouvrés, monnaie nationale,
   Fonds souverain et bauxite avant la première exportation sont exclus.
3. **Partenariats public-privé** : chiffrage des paiements futurs et des garanties, plafond annuel
   voté par le Parlement.
4. **Trois scénarios** : central (croissance de 4,0-4,5 %), défavorable (pas de programme FMI, baril bas,
   choc politique) et favorable (scénario actuel du Plan).
5. Les mesures coûteuses des documents politiques ne sont admises qu'après un **test de financement**
   montrant leur source :
   - +30 % de salaires : ≈488 Mds par an ;
   - 10 000 MW ;
   - villes nouvelles ;
   - centres d'excellence.

## 9. Risques majeurs

- **Politique.** Le poste de vice-président n'est pas pourvu et le calendrier législatif est incertain.
  Les réformes qui exigent une loi doivent être votées tôt.
- **Social.** Une hausse des carburants sans compensation versée au préalable entraîne un risque de
  contestation et de recul. D'où la règle : le transfert d'abord, la hausse ensuite.
- **Exécution.** L'investissement public n'est exécuté qu'à 73 %. Mieux vaut moins de chantiers,
  pilotés par une unité présidentielle de suivi, comme le propose le Plan.
- **Données.** Plusieurs points de départ restent inconnus (arriérés certifiés, pertes électriques
  officielles, effectif du registre social). Il faut les établir avant de fixer des cibles définitives.

## 10. Ce qui reste à vérifier avant diffusion officielle

- Note CAA n° 06/2026 (restes à payer).
- Rapport de la Chambre des comptes sur les entreprises publiques (2026).
- Rapports ARSEL et SOCADEL.
- Analyse de viabilité de la dette FMI-BM.
- Texte de la sentence CIRDI.
- État judiciaire des dossiers Covid.
- Taux du tarif extérieur commun CEMAC et taux consolidés OMC sur le riz, le blé et le poisson.
- Production nationale officielle de riz et de poisson (MINADER, MINEPIA).
- Textes au Journal officiel : lois de 2017, Code pénal, révision constitutionnelle d'avril 2026.
