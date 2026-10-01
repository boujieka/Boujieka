# Analyse du positionnement : Energy Access Finance Toolkit

Date : 1er octobre 2026. Statut : document de travail.

## 1. Verdict

Le diagnostic de fond tient. La concurrence générique en *renewable project finance* est dense, et l'angle **Energy Access + RBF + VGF + MRV + allocation de fonds** est plus différencié. Mais la recherche initiale contient quatre faiblesses qu'il faut corriger avant d'investir du temps dans les produits 2 et 3.

### Faiblesse 1 : les concurrents gratuits hors marketplace n'ont pas été examinés
- **Vérifié :** CrossBoundary Access a publié gratuitement (open source) un modèle financier de projet mini-grid le 31/10/2023 : https://crossboundary.com/mini-grid-financial-model-open-source/
- Il s'agit d'un acteur reconnu du secteur mini-grid en Afrique. Un acheteur sérieux (développeur, consultant) le trouvera avant notre listing Etsy.
- **Mise à jour :** le fichier a été analysé (voir `docs/COMPARATIF_CROSSBOUNDARY.md`). Il ne contient ni RBF par connexion vérifiée, ni viability gap, ni calibrage de subvention, ni segments, ni affordability, ni MRV/CO₂, ni dette concessionnelle, ni tornado. En revanche, il est plus complet que nous sur la dette (sculptage, refinancement), la fiscalité, le change et les états financiers.
- Il existe d'autres outils, gratuits ou payants, que je n'ai pas vérifiés dans le détail (outils de dimensionnement technique, modèles NREL SAM, etc.).

**Conséquence :** le produit 2 ne peut pas se vendre sur « un modèle financier mini-grid ». Il doit se vendre sur ce qu'un modèle gratuit ne fait pas : la **structuration de la subvention** (viability gap, calibrage du RBF, dossier de financement) et la **pédagogie** (guide, exemple chiffré, version française).

### Faiblesse 2 : « absence dans les résultats » ne veut pas dire « demande non servie »
Ne pas trouver de produit Energy Access + RBF sur Etsy/Gumroad peut signifier deux choses :
- (a) une niche inexploitée ;
- (b) des acheteurs qui n'achètent pas sur Etsy/Gumroad. Les fonds et les DFI passent par des consultants, des appels d'offres ou des outils internes.

Les deux explications sont plausibles. Rien dans la recherche ne permet de trancher.

### Faiblesse 3 : les chiffres de ventes cités ne mesurent pas la demande de la niche
- « Plusieurs centaines de ventes » chez ProfitVision : c'est un chiffre **boutique**, pas produit. On ne peut pas en déduire les ventes du modèle solaire.
- **9 ventes** chez Bank Run (Gumroad) : si le chiffre est exact, c'est plutôt un signal de **faible volume** sur un modèle renouvelable de qualité professionnelle.
- Je n'ai pas revérifié ces prix et volumes en direct. Ils proviennent de la recherche qui m'a été transmise.

### Faiblesse 4 : le produit 3 (Fund Manager, 199–299 $) est le plus risqué sur Etsy
- Inférence : la clientèle d'Etsy est majoritairement grand public et petites entreprises. Un gestionnaire de fonds ou une DFI achète rarement un fichier à 249 $ sur Etsy (achats, conformité, factures).
- Ce produit a plus de chances de se vendre via Gumroad + LinkedIn, ou comme **produit d'appel pour du conseil** (paramétrage du modèle pour un fonds donné). C'est probablement là que se trouve la vraie valeur économique.

### Point juridique et réputationnel à surveiller
Des profils nommés « Mwinda / RDC » ou « Congo Energy Access Fund » dans un produit payant peuvent laisser croire à une affiliation ou à un aval de ces programmes. Ils peuvent aussi exposer des règles internes confidentielles. **Recommandation :** utiliser uniquement des profils génériques (« RBF par connexion, plafond par ménage, décaissement sur vérification »). Ne citer un programme réel que s'il s'appuie sur des documents publics, avec un avertissement de non-affiliation.

## 2. Ce que je garde de la stratégie proposée
- L'échelle de produits (entrée → professionnel → institutionnel → bundle). C'est une logique cohérente, illustrée par Bank Run.
- La symétrie commerciale « From Project to Funding / From Funding to Impact ».
- Ne pas cloner ProfitVision.
- La crédibilité liée à l'expérience terrain. À condition qu'elle soit **concrète et vérifiable** : profil LinkedIn, missions réalisées. Une formule vague ne suffit pas.

## 3. Ce que je change
| Sujet | Proposition initiale | Recommandation |
|---|---|---|
| Séquence | Lancer la gamme complète | Lancer **P1** d'abord, mesurer, puis construire **P2** sur le même moteur. P3 seulement après signaux de demande (liste d'attente, demandes entrantes). |
| Canal P3 | Etsy + Gumroad | Gumroad + LinkedIn + offre de paramétrage (service) |
| Différenciation P2 | Liste de fonctionnalités | **Viability gap + calibrage RBF + note de demande de financement** générée par le modèle, et comparatif honnête avec le modèle gratuit CrossBoundary |
| Langue | Anglais | **Anglais + version française**. Inférence : peu de modèles payants en français, et l'Afrique francophone est une cible naturelle vu ton expérience. À vérifier par une recherche Etsy en français. |
| Prix P1 | 19 $ | 19–29 $. Il n'est pas « simple » : il calcule déjà le viability gap et le DSCR. Tester 24 $. |

## 4. Validation avant de construire P2 et P3 (peu coûteux, environ 2 semaines)
1. Publier P1 sur Gumroad (rapide) puis sur Etsy.
2. Publier sur LinkedIn une étude de cas tirée de l'exemple du modèle : « Pourquoi ce mini-grid de 970 clients a besoin de 889 $ de subvention par connexion ». Lien vers P1.
3. Ajouter une liste d'attente « Developer Edition » et « Fund Manager Edition » (formulaire Gumroad gratuit ou à 0 $).
4. Critères de décision, à fixer par toi : par exemple au moins X ventes P1 et Y inscrits en liste d'attente en 30 jours. Je ne connais pas les seuils réalistes pour cette niche. Je ne les invente pas.

## 5. Architecture produit (ce qui est construit et ce qui reste à faire)
**P1, construit** (`product/01-entry-calculator/`) : calculateur de faisabilité mini-grid.
- Segments de clientèle, montée en charge des connexions, auto-dimensionnement PV, batterie et diesel (avec override), CAPEX/OPEX.
- Remplacement batterie avec compte de réserve de maintenance, fiscalité simplifiée, dette en annuité avec différé.
- Indicateurs : CFADS, DSCR, IRR projet avant et après subventions, IRR equity, NPV, LCOE, payback, CO₂.
- **Viability gap** et verdict de finançabilité. Leviers de scénario. Onglet de contrôles d'intégrité.

**P2 Developer Edition, construit** (`product/02-developer-edition/`). Ajouts prévus au départ :
- Courbe de charge mensuelle et productive use détaillé (machines, heures).
- Affordability : facture en % du revenu ménage.
- Calibrage du RBF : montant par connexion nécessaire pour atteindre l'IRR cible.
- Mix grant / RBF / dette concessionnelle.
- Sensibilités en tornado : tarif, CAPEX, demande, taux de recouvrement.
- Scénarios multiples. DSRA.
- Indicateurs MRV : connexions vérifiées, kWh, CO₂, emplois.
- Onglet « Financing Request » prêt à copier dans une note de demande.

**P3 Fund Manager Edition, après validation.** Pipeline de projets, critères d'éligibilité, scoring, allocation sous contrainte d'enveloppe, engagements et décaissements RBF, levier capital privé, coût par connexion, tableau de bord portefeuille.

## 6. Incertitudes ouvertes
- Volume réel de la demande sur Etsy/Gumroad pour ce type de produit : inconnu.
- Contenu du modèle CrossBoundary : vérifié par analyse des libellés, pas par un audit formule par formule.
- Frais et règles actuels d'Etsy et de Gumroad (frais de transaction, TVA sur produits numériques, éligibilité des pays vendeurs) : à vérifier dans tes comptes vendeurs. Je ne les cite pas de mémoire.
