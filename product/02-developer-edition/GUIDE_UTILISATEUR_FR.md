# Modèle financier de projet d'accès à l'énergie (Édition Développeur) : guide utilisateur

Fichier : `Modele_Financier_Acces_Energie_Developpeur_v1_FR.xlsx`

## 1. La question traitée
*Ce projet d'accès à l'énergie peut-il devenir bancable, et quelle combinaison de subvention, RBF, dette concessionnelle, dette senior et fonds propres lui faut-il ?*

## 2. Démarche (environ 30 minutes pour un premier passage)
1. **Hypothèses**
   - Données du projet, puis choix du scénario actif : Base, Prudent, Optimiste ou Personnalisé.
   - Segments de clientèle avec tarif, frais de raccordement, **RBF par raccordement** et **revenu mensuel**.
   - Technique, CAPEX, OPEX (y compris les coûts MRV), et structure de financement : subvention, dette senior, dette concessionnelle, DSRA.
2. **Courbe de charge** : profil horaire de chaque segment. Il fixe la part nocturne (taille de la batterie) et le ratio de pointe (taille du groupe).
3. **Usages productifs** : inventaire des équipements. Si `UsePUE = 1`, il fixe la consommation des usagers productifs.
4. **Tableau de bord** : indicateurs clés, verdict (OUI/NON) et capacité de paiement par segment.
5. **Déficit de financement & RBF** : ampleur du déficit, subvention ou RBF qui le comble, et dette que le projet peut supporter.
6. **Sensibilité** : tornado dynamique à ±20 % (amplitude réglable).
7. **Impact & MRV** : indicateurs annuels et ratios coût-efficacité.
8. **Demande de financement** : paragraphes rédigés automatiquement et tableau emplois-ressources, prêts pour une note conceptuelle.
9. **Contrôles** : doivent afficher **TOUT OK**.

## 3. Méthodes clés
| Résultat | Méthode |
|---|---|
| Déficit de viabilité | MAX(0, –VAN du flux projet avant subventions au taux minimal) |
| Subvention nécessaire | Déficit de viabilité – VA(RBF prévu) |
| RBF nécessaire pour VAN = 0 | (Déficit – subvention) / VA(raccordements vérifiés, avec délai) |
| RBF nécessaire pour la cible des fonds propres | –(VAN des fonds propres à la cible – VA(RBF) à la cible) / VA(raccordements) à la cible |
| Dette senior maximale | MIN sur les années de (CFADS / DSCR min – service de la dette concessionnelle) / service senior par unité de dette |
| Tornado | Copies masquées du moteur (onglets `S_*`), une par variable et par sens |

**Les résultats RBF sont exacts.** Je l'ai testé en injectant les montants calculés : la VAN du projet tombe à 0 et le TRI des fonds propres à 15,0 %.

## 4. Lire l'exemple (valeurs illustratives)
- 970 clients et un CAPEX de 1,15 M$. Le déficit de viabilité est de 793 k$, soit environ 818 $ par raccordement.
- Une subvention de 600 k$ et un RBF d'environ 260 $ par raccordement comblent le déficit au niveau du projet : VAN de +25 k$.
- Le covenant de dette est respecté, avec un DSCR minimum de 1,37x.
- **Le TRI des fonds propres est de 10,7 %, sous la cible de 15 %.** Le modèle indique qu'un RBF uniforme d'environ **334 $ par raccordement** l'atteindrait.
- **Une demande +20 % réduit la VAN.** Le système est dimensionné pour la demande de base, donc les kWh supplémentaires viennent du diesel, plus cher que le tarif encaissé.

## 5. Simplifications
- Pas de temps annuel, sans dispatch horaire. Le dimensionnement repose sur les hypothèses de base.
- Impôt à taux unique avec report illimité des pertes. Subventions et RBF sont considérés comme non imposables.
- Dette en annuités, sans frais ni profil sculpté. Pas de change, de TVA, de BFR ni de bilan.

Ce modèle se concentre sur le **dimensionnement des subventions, la capacité de paiement et l'impact**. Il peut s'utiliser en complément d'un modèle complet de financement de projet.

## 6. Langue et format
- Calculs identiques à la version anglaise : 32 023 valeurs comparées, aucun écart. Le scénario « Prudent » reproduit exactement « Conservative ».
- Les montants n'ont pas de symbole $ : la devise est un libellé à saisir dans les Hypothèses (USD, XAF, XOF, CDF…).

## 7. Avertissement
Outil de présélection et de préfaisabilité. Ce n'est pas un conseil en investissement, juridique, fiscal ou d'ingénierie. Les valeurs d'exemple ne sont pas des références de marché.
