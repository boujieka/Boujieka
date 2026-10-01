# Calculateur de faisabilité financière de mini-réseau : guide utilisateur

Fichier : `Calculateur_Faisabilite_MiniReseau_v1_FR.xlsx`

## 1. Démarrage rapide
1. Ouvrez l'onglet **Hypothèses**. Ne modifiez que les **cellules jaunes à texte bleu**.
2. Saisissez vos segments de clientèle : nombre de clients, kWh par mois, tarif et frais de raccordement.
3. Vérifiez le dimensionnement automatique du PV, de la batterie et du diesel. Saisissez une valeur dans **Forçage** pour imposer votre propre conception.
4. Saisissez les coûts unitaires, les OPEX et le financement (subvention, RBF par raccordement, conditions de la dette).
5. Lisez le **Tableau de bord**. Vérifiez que l'onglet **Contrôles** affiche **TOUT OK**.

## 2. Lire les résultats
| Indicateur | Signification |
|---|---|
| TRI du projet avant subventions | Rentabilité du projet sur la seule base commerciale |
| TRI du projet après subventions | Rentabilité une fois la subvention et le RBF comptés |
| VAN au taux minimal | Valeur créée à votre taux d'actualisation. Négative = le projet a besoin de soutien |
| LCOE | Coût actualisé sur le cycle de vie par kWh vendu. À comparer à la recette encaissée actualisée par kWh |
| CFADS / DSCR | Trésorerie disponible pour rembourser le prêteur. Covenant non respecté si le DSCR minimum est sous le seuil exigé |
| **Déficit de viabilité** | Subvention initiale, en valeur actuelle, qui ramène à zéro la VAN avant subventions |
| Déficit restant | Déficit de viabilité moins la valeur actuelle de la subvention et du RBF prévus |

## 3. Méthode et simplifications
- Pas de temps annuel : construction en année 0, exploitation années 1 à 20.
- Solaire livré = MIN(PV disponible, production × fraction solaire cible). Le diesel couvre le reste. Il n'y a pas de dispatch horaire.
- Les capacités PV et batterie sont fixes. Une croissance de la demande au-delà de l'année de conception augmente la part du diesel.
- Les batteries sont remplacées tous les *n* ans. L'option de réserve de maintenance lisse ce coût dans le CFADS.
- Impôt : taux unique, sans report des pertes. Subventions et RBF sont considérés comme non imposables. À vérifier localement.
- Dette : annuités après un différé, sans frais ni DSRA.
- Le TRI peut être trompeur quand les flux changent de signe (années de remplacement des batteries). Privilégiez la VAN et le déficit de viabilité.

## 4. Exemple (valeurs illustratives)
- Village de 970 clients, avec 349 kWc de PV, 780 kWh de batterie et 145 kW de diesel. Le CAPEX est d'environ 1,32 M$.
- Sans subvention, la VAN est de –863 k$ à 10 %, soit un déficit d'environ 889 $ par raccordement.
- Avec une subvention de 680 k$ et un RBF de 250 $ par raccordement, la VAN devient positive et le DSCR minimum atteint 1,60x. Le TRI des fonds propres reste sous la cible de 15 %.

## 5. Langue et format
- Version française, avec des calculs identiques à la version anglaise : 1 748 valeurs comparées, aucun écart.
- Les nombres insérés dans les textes utilisent CTXT/FIXED. Ils s'affichent donc avec les séparateurs de votre version d'Excel (par exemple « 4 000 » et « 0,66 »).

## 6. Avertissement
Outil de présélection et de préfaisabilité. Ce n'est pas un conseil en investissement, juridique, fiscal ou d'ingénierie. Les valeurs d'exemple ne sont pas des références de marché.
