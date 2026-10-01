# Modèle du gestionnaire de fonds d'accès à l'énergie (Édition RBF & Portefeuille) : guide utilisateur

Fichier : `Modele_Gestionnaire_Fonds_Acces_Energie_v1_FR.xlsx` (version anglaise : `EnergyAccess_Fund_Manager_Model_v1.xlsx`)

## 1. La question traitée
*Quels projets le fonds doit-il soutenir, avec quels montants de RBF et de subvention, et quel portefeuille de raccordements, d'impact, d'effet de levier et de risque cela permet-il d'obtenir ?*

## 2. Démarche
1. **Paramètres du fonds**
   - Taille du fonds, coûts de gestion et d'assistance technique, taux de surengagement, limites de concentration, tolérance d'additionnalité.
   - **Profil du fonds** : taux RBF par type de client, part de subvention CAPEX, plafonds, tranches RBF. Trois profils génériques sont proposés, plus *Personnalisé*.
   - Critères d'éligibilité (seuil + activation), pays éligibles (O/N), pondérations (total = 100 %), taux de réalisation attendu selon le risque.
2. **Pipeline de projets** : une ligne par candidat, jusqu'à 25. Le CAPEX, le déficit de viabilité et le CO2 peuvent être collés depuis l'**Édition Développeur**.
3. **Éligibilité & notation** : tests binaires, soutien maximal, demande, indicateurs, huit scores, score pondéré et rang.
4. **Allocation** : financement par ordre de rang dans la limite de l'enveloppe et de la limite par pays, avec indication de la contrainte limitante.
5. **Décaissements** : la subvention est versée à la mise en service. Le RBF est versé par tranches à la vérification, ajusté du taux de réalisation. L'onglet présente aussi la trésorerie du fonds.
6. **Suivi MRV** : raccordements vérifiés et RBF payé à date, comparés au profil attendu. Statut : Dans les temps, En retard ou Hors trajectoire.
7. **Tableau de bord portefeuille** : engagements, pipeline, impact, effet de levier, coût-efficacité, risque et concentration, verdicts, graphiques.
8. **Contrôles** : doivent afficher **TOUT OK**.

## 3. Méthodes clés
| Élément | Méthode |
|---|---|
| Soutien maximal | MIN(RBF aux taux du profil + subvention CAPEX, part max du CAPEX – autres subventions, max par projet, part max de l'enveloppe) |
| Demande retenue | Montant demandé par le développeur s'il est renseigné (plafonné), sinon le soutien maximal |
| Scores | Relatifs au meilleur projet éligible (coût par raccordement, effet de levier, part productive, CO2 par unité) ; absolus (maturité, expérience, risque) ; additionnalité 100/50/0 |
| Allocation | Séquentielle par rang, sans circularité. Financement partiel : MIN(demande, enveloppe restante, marge pays) ; sinon tout ou rien |
| Décaissement RBF de l'année t | RBF alloué × réalisation × [tranche A × part vérifiée (t – délai) + (1 – A) × part vérifiée (t – délai – 1)] |
| Impact et effet de levier | Au prorata de la part de chaque demande couverte par le fonds |

## 4. Exemple (illustratif, aucun fonds réel)
- Fonds de 3,0 M$. Après gestion et AT, 2,55 M$ sont disponibles. Avec un surengagement de 110 %, l'enveloppe est de **2,805 M$**.
- 14 candidats, dont **8 éligibles**. Les 6 autres sont rejetés avec un motif explicite : pays, part renouvelable, maturité, CAPEX par raccordement, taille, usages productifs.
- Les demandes éligibles totalisent 3,25 M$, soit une **sursouscription de 1,16x**.
- Le projet N est partiellement financé à cause de la **limite pays** (le pays B atteint exactement 50 %). Le projet I est partiellement financé parce que l'**enveloppe est épuisée**.
- Impact financé : environ 8 000 raccordements, 32 400 personnes et 50 800 tCO2. L'effet de levier est de 1,57x en capitaux privés par unité allouée.
- **Le modèle signale une vraie tension :** avec 110 % de surengagement, les décaissements attendus dépassent les fonds disponibles. Les subventions sont versées intégralement et seul le RBF subit la décote, donc la sous-réalisation attendue ne couvre qu'environ **1,02x**. Réduisez le surengagement ou augmentez la part de RBF.

## 5. Comportements testés
- 0 erreur de formule en FR et en EN. Les chiffres sont identiques entre les deux langues (3 032 valeurs comparées).
- Cas testés : financement partiel désactivé (un projet qui ne tient pas est sauté) ; autre profil ; tous critères désactivés (14 éligibles) ; fonds plus grand (chaque projet à son plafond).

## 6. Simplifications
- Pas de temps annuel. Profil de vérification commun à tous les projets. Subventions versées en une fois à la mise en service.
- Pas de change, pas de rendement du fonds (fonds de subvention/RBF), pas de reflux. Les scores aident à la décision ; ils ne remplacent pas le comité d'investissement.

## 7. Avertissement
Outil de sélection et de planification de portefeuille. Ce n'est pas un conseil en investissement, juridique ou fiscal. Les données d'exemple sont fictives.
