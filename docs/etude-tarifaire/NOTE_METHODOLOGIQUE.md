# Le paradoxe des subventions tarifaires en Afrique — note méthodologique

Cameroun, République du Congo et pays dotés d'un pacte national de l'énergie (Mission 300).
Secteur : électricité. Analyse 2020–2026, réformes 2027–2035.

**Statut au 17 octobre 2026.** Cette note accompagne la version de structure du Livrable 2 :
`modele_tarifaire_electricite.xlsx`, généré par `build_modele.py`.
**Aucune donnée réelle n'est encore saisie.** Seule la feuille `Exemple_fictif` contient des chiffres,
et ils sont inventés : ils servent uniquement à vérifier les formules et ne doivent jamais être cités.

---

## 1. Périmètre : les pays dotés d'un pacte

Selon la page « Compacts » de Mission 300, consultée le 17/10/2026 :

| Cohorte | Pays |
|---|---|
| 1 (janvier 2025) | Côte d'Ivoire, Liberia, Madagascar, Malawi, Mauritanie, Niger, Nigeria, RDC, Sénégal, Tanzanie, Tchad, Zambie |
| 2 (septembre 2025) | Bénin, Botswana, Burundi, **Cameroun**, Comores, **Congo**, Éthiopie, Gambie, Ghana, Guinée, Kenya, Lesotho, Mozambique, Sao Tomé-et-Principe, Sierra Leone, Togo, Zimbabwe |
| 3 | Burkina Faso, Gabon, Ouganda, République centrafricaine, Rwanda |

Sources :
- Mission 300 : <https://mission300africa.org/compacts/>.
- Communiqué Banque mondiale du 24/09/2025, qui liste les 17 pays de la cohorte 2 : <https://www.worldbank.org/en/news/press-release/2025/09/24/17-countries-commit-to-concrete-plans-to-scale-up-electricity-access-as-mission-300-expands>.

**Deux incohérences entre sources restent à lever :**
- La **Namibie** figure dans le communiqué de la Banque mondiale, mais pas sur la page Mission 300.
- Le **Zimbabwe** figure sur la page Mission 300 avec la mention « cohorte 2 », mais pas dans le communiqué.

**Proposition de découpage :**
- **Approfondi** : Cameroun et Congo.
- **Comparatif** : autres pays CEMAC dotés d'un pacte (Tchad, Gabon, RCA), plus deux références de l'UEMOA (Côte d'Ivoire, Sénégal).
- **Indicateurs seulement** : les autres pays.

Analyser une trentaine de pays au même niveau de détail n'est pas réaliste, faute de données de coût par catégorie.

## 2. Faits contextuels relevés (à confirmer auprès de sources primaires)

**Cameroun**
- Le pacte vise l'accès universel en 2030, avec environ 12,5 Md USD à mobiliser. Source : [pacte, Banque mondiale](https://thedocs.worldbank.org/en/doc/230ea6e10398ad291f50a89d2d458c8f-0010012025/original/Cameroon-National-Energy-Compact-Mission-300.pdf).
- L'État a racheté les 51 % d'Actis dans ENEO pour 78 Md FCFA. Les dates ne concordent pas selon les sources :
  - accord du 19/11/2025 selon [Journal du Cameroun](https://fr.journalducameroun.com/?p=448814) ;
  - paiement du 10/02/2026 selon [Business in Cameroon](https://www.businessincameroon.com/energy/2002-15795-cameroon-completes-buyback-of-eneo-in-a-cfa78-billion-deal-with-actis).
- Conséquence pour l'étude : l'opérateur est désormais public. Le risque « l'État ne paie pas ses compensations » devient un risque interne au secteur public, mais il ne disparaît pas.

**Congo**
- Le pacte, appelé « Électricité pour tous », vise l'accès universel, l'alimentation des zones industrielles et minières, et l'exportation. Source : [BAD](https://afdb.africa-newsroom.com/press/17-countries-commit-to-concrete-plans-to-scale-up-electricity-access-as-mission-300-expands?lang=en).
- Les chiffres disponibles sont contradictoires :
  - **Taux d'accès** : 51,3 % en 2023 selon [AllAfrica](https://fr.allafrica.com/stories/202606060216.html), contre 31,66 % selon le pacte cité par [Rio Times](https://www.riotimesonline.com/congo-brazzaville-electricity-e2c-turnaround-2026/).
  - **Capacité installée** : 760 MW ou 748 MW selon les sources, dont environ 600 MW disponibles.
- Le contrat de performance d'E2C est annoncé, mais sa date, ses signataires et ses pénalités ne sont pas publiés.

Aucune grille tarifaire, aucun coût de service par catégorie et aucun montant de compensation versé n'a été trouvé dans ces sources. Ce sont précisément les données qui conditionnent l'étude.

## 3. Points faibles de la proposition, et réponses intégrées au modèle

1. **Périmètre incohérent.** Le secteur annoncé est l'électricité, mais la problématique et la question principale citent aussi l'eau. Le modèle couvre l'électricité seulement. Il faut soit retirer l'eau de la question, soit l'ajouter comme second secteur avec ses propres opérateurs.

2. **H1 à H5 ne peuvent pas être « testées » au sens causal.** Avec deux pays et sept années, aucune identification économétrique n'est possible. L'étude doit l'annoncer clairement. Elle procède par :
   - décomposition comptable : quasi-fiscal deficit (déficit quasi budgétaire) selon Kojima et Trimble, Banque mondiale, 2016 ;
   - simulation de scénarios ;
   - analyse d'incidence sur enquête ménages pour H2 (méthode de Komives et al., Banque mondiale, 2005).

3. **H3 suppose une étude de coût de service par niveau de tension.** Sans elle, on ne peut pas distinguer :
   - une subvention croisée injustifiée (votre cas A) ;
   - une différenciation tarifaire justifiée par les coûts (votre cas B).

   **Hypothèse concurrente à examiner :** une partie de l'industrie pourrait être subventionnée plutôt que surtaxée, par exemple les gros consommateurs sous contrat spécifique. Au Cameroun, les conditions du contrat d'ALUCAM sont à vérifier. Le modèle laisse le signe de l'écart se déterminer à partir des données.

4. **Le CTPT additionne des flux budgétaires (SB, DC) et des coûts économiques (CI, CE).** Ce sont des grandeurs de nature différente. Le modèle les affiche séparément puis agrégés. Deux précautions ont été prises :
   - les pertes excédentaires et le non-recouvrement sont isolés dans une ligne « inefficience opérateur », hors CTPT, pour éviter les doubles comptages ;
   - CI et CE doivent être estimés sur des périmètres disjoints.

5. **H5 se joue sur une variable : la fiabilité des paiements budgétaires.** Dans l'exemple fictif, il suffit d'un taux de versement de 70 % pour qu'un déficit non financé subsiste en 2035, alors même que les tarifs couvrent les coûts. La conclusion principale devrait prendre la forme d'un **seuil de fiabilité à partir duquel le scénario S2 ou S3 domine S0**, plutôt que d'un verdict général.

6. **Ménages non raccordés.** Le modèle les traite de deux façons :
   - une subvention au raccordement, comme ligne budgétaire ;
   - une part de subvention nulle dans l'incidence par quintile.

   Il ne mesure pas encore le gain d'accès que permettrait un opérateur assaini (H4). Cela demande un module d'investissement, absent de cette version.

## 4. Structure du modèle

| Feuille | Contenu |
|---|---|
| `LISEZMOI` | Statut des données, code couleur, limites connues |
| `Synthese` | Comparaison des pays sur le scénario actif de chaque feuille |
| `Cameroun`, `Congo` | Hypothèses (jaune = à renseigner) ; catégories tarifaires ; scénarios S0–S3 ; trajectoire 2027–2035 ; CTPT |
| `Exemple_fictif` | Même structure, valeurs inventées pour tester les formules |
| `Equite_H2` | Incidence de la subvention résidentielle par quintile, tranche progressive ou par volume |

**Conventions :**
- Énergie en GWh ; tarifs en FCFA/kWh ; montants en milliards de FCFA constants (termes réels).
- Les écarts tarif–coût se résorbent de façon linéaire entre la base et 2035.
- Les 1 611 formules ont été recalculées sans erreur sous LibreOffice. Les résultats de l'exemple fictif ont été contrôlés à la main : ventes, recettes, écarts, compensation, résultat d'exploitation, aide et incidence par quintile.

**Limites connues :**
- Pas d'élasticité-prix.
- Coûts constants en termes réels.
- Pas de module d'investissement.
- Un seul scénario actif à la fois par feuille.

## 5. Données à collecter en priorité (par pays, 2020–2026)

1. **Grilles tarifaires officielles** (décisions du régulateur) et tarif moyen effectif par catégorie.
2. **Étude de coût de service** ou, à défaut, revenu requis approuvé et clés d'allocation par tension.
3. **Bilan énergétique** : énergie injectée, pertes techniques et commerciales, pertes admises.
4. **Données financières de l'opérateur** : états financiers audités, recouvrement, créances sur l'État.
5. **Compensations** : montants dus et effectivement versés, d'après les lois de finances et les comptes de l'opérateur.
6. **Enquête ménages** : raccordement et consommation par quintile ; seuil et structure de la tranche sociale.
7. **Enquêtes entreprises** (World Bank Enterprise Surveys, si disponibles) : délestages, autoproduction, part de l'énergie dans les coûts.
8. **Registre social** : capacité de ciblage, coût administratif, erreurs d'inclusion et d'exclusion.
