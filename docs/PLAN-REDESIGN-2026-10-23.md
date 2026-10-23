# Plan de redesign — inspiré des plateformes américaines et britanniques

Date : 23/10/2026. Objectif : relooker Africa Bonds Monitor (ABM) pour qu'il soit simple à utiliser et crédible auprès des institutions, sans copier la marque ni l'interface propriétaire de qui que ce soit.

Repères :
- **[S]** : vérifié par une recherche web ce jour (sources en fin de document).
- **[C]** : connaissance générale, non revérifiée aujourd'hui.

## 1. Plateformes comparables

| Plateforme | Pays | Nature | Ce qu'ABM peut en retenir |
|---|---|---|---|
| **Fiscal Data** (fiscaldata.treasury.gov), Trésor américain | US | Portail public de données budgétaires. Lancé en 2020 avec 18 jeux de données, téléchargeables en CSV, JSON et via API [S]. Il propose un jeu de données « auctions » et un autre pour les adjudications à venir [S] | Une page par jeu de données (description, champs, dernière mise à jour, téléchargement, API). Des pages explicatives en langage simple. |
| **TreasuryDirect** | US | Site du Trésor pour l'achat direct de titres par les particuliers, avec résultats et calendrier d'adjudications [C] | Un parcours « comment acheter » officiel et pas à pas. C'est l'équivalent de la page « Accès officiel » d'ABM. |
| **FINRA Fixed Income Data / TRACE** | US | Données gratuites de prix et de transactions obligataires, recherche par identifiant, statistiques de marché quotidiennes ou mensuelles. Il faut accepter une convention d'utilisation, et FINRA ne garantit pas l'exactitude des données [S] | Recherche par code de titre (pour ABM, l'ISIN). Statistiques agrégées séparées des données ligne à ligne. Avertissement clair sur la qualité des données. |
| **EMMA (MSRB)** | US | Site public et gratuit sur le marché municipal : documents d'émission, prix, informations continues, statistiques, alertes gratuites via un compte « MyEMMA » [S] | **C'est le modèle le plus proche d'ABM.** Une page par émetteur, et pour chaque titre un document officiel joint. Le compte sert aux alertes, pas à voir les données. |
| **UK Debt Management Office** (dmo.gov.uk) | UK | Résultats officiels des opérations sur gilts : adjudications, syndications, adjudications à prix unique, facilités de repo [S] | Un tableau des résultats par type d'opération, avec le taux de couverture et le rendement moyen, comme dans les dépêches reprises par MarketScreener [S]. |
| **Bank of England — courbes de taux** | UK | Courbes ajustées publiées (gilts nominaux, réels, inflation implicite, OIS), avec un historique depuis 1979 pour les gilts nominaux [S] | Distinguer clairement **courbe observée** et **courbe ajustée**, avec une note de méthode. ABM ne publie que des points observés. |
| **Calculateurs de gilts pour particuliers** (par exemple tools.incoherency.co.uk) | UK | Tableau des gilts triable, courbe de taux, rendement avant et après impôt, date de dernière mise à jour affichée [S] | Un tableau triable avec des colonnes simples et la date des données toujours visible. |
| **Koyfin** | US | Analyse financière par abonnement : tableaux de bord des rendements mondiaux et des courbes de taux, colonnes personnalisables, export CSV, listes de suivi. Certaines données ne sont pas téléchargeables à cause des contrats avec les fournisseurs [S] | Une table qui alimente un graphique (cocher des lignes pour les comparer). Des listes de suivi. Des restrictions d'export selon la licence, comme pour ABM. |
| **Bloomberg Terminal, LSEG Workspace** | US / UK | Terminaux professionnels payants [C] | Seulement la densité d'information et les raccourcis clavier. **Ni leur marque, ni leurs couleurs, ni leur interface ne doivent être copiées.** |

Références africaines à connaître (ce sont des concurrents ou des partenaires possibles, pas des modèles de design) :
- **Cbonds** : base de données obligataires des marchés émergents, avec des indices de volume pour l'Afrique. L'accès détaillé est payant ; démonstration de 7 jours [S].
- **BAD — African Financial Markets Initiative (AFMI)** : base de données couvrant environ 41 pays, alimentée par des correspondants dans les banques centrales. Elle est liée à l'indice ABABI et à l'African Domestic Bond Fund [S]. **C'est un partenaire de données potentiel**, à approcher.

## 2. Leçons communes (ce qui rend ces sites faciles à utiliser)
1. **Les données publiques sont lisibles sans compte.** EMMA et FINRA demandent au plus une convention d'utilisation. Le compte sert aux alertes et à la personnalisation [S]. ABM fait aujourd'hui l'inverse sur plusieurs pages.
2. **Une page par objet.** Une page par jeu de données (Fiscal Data), par émetteur (EMMA), par titre (FINRA).
3. **Chaque chiffre a sa date et son document.** ABM le fait déjà ; c'est son meilleur atout.
4. **La méthode est séparée de la donnée.** Courbe ajustée ou observée (Bank of England), avertissement sur la qualité (FINRA).
5. **Le téléchargement et l'API sont visibles partout** (Fiscal Data, Koyfin), et ce qui ne peut pas être exporté est signalé.
6. **Des explications en langage simple** à côté des données techniques (Fiscal Data, guide du DMO pour les particuliers).

## 3. Nouvelle structure du site (5 entrées au lieu de 9)

```
Accueil
├── Marchés          → tableau des adjudications (filtres pays / zone / instrument / maturité / date)
│   ├── Pays         → une page par pays : chiffres clés, courbe observée, adjudications, titres, sources
│   └── Titre        → une page par ISIN : conditions connues, historique, documents officiels
├── Comparer         → jusqu'à 5 pays, sur les mêmes conventions uniquement
├── Accès officiel   → comment souscrire, pas à pas, par zone ; intermédiaires agréés
├── Données & méthode→ jeux de données (CSV / JSON / API), conventions, limites, sources, mises à jour
└── Plus             → Rapports, Simulateur, Assistant, Pilote institutionnel, Mentions légales
Compte (en haut à droite) → Suivi (pays / titres), alertes, filtres enregistrés, portefeuille
```

**Règle d'accès :** tout ce qui est publié est public. Le compte sert seulement à enregistrer : suivi, alertes, filtres, portefeuille, assistant.

## 4. Pages clés

| Page | Contenu | Modèle |
|---|---|---|
| **Accueil** | Titre : « Adjudications UEMOA et CEMAC, cote BVMAC — chaque chiffre relié à son document officiel ». Quatre indicateurs calculés en direct depuis le flux, chacun cliquable : adjudications vérifiées, pays, titres BVMAC, date des données. Les 5 dernières adjudications. Trois usages : trésorerie, gestion actif-passif, gestion d'actifs. Deux boutons : « Ouvrir les marchés », « Rejoindre le pilote ». | Fiscal Data, EMMA |
| **Marchés** | Tableau dense et triable. La colonne valeur indique toujours sa nature (rendement, prix ou taux précompté) et sa devise. Cocher des lignes affiche le graphique. Export CSV avec l'URL de la source sur chaque ligne. | Koyfin, DMO |
| **Pays** | En-tête : nom, zone, devise, date de la dernière adjudication. Score de complétude par champ (par exemple « montant offert : 7 % des adjudications »). Courbe des points observés (UEMOA uniquement). Échéances connues. | EMMA (page émetteur) |
| **Titre (ISIN)** | Conditions connues ; tout champ absent est marqué « non publié » et jamais estimé. Historique des adjudications et des cotations, documents. | FINRA, EMMA |
| **Données & méthode** | Une fiche par jeu de données : champs, couverture, fréquence, dernière mise à jour, licence (« publication gratuite, source citée »), liens CSV, JSON et API. | Fiscal Data |
| **Accès officiel** | Étapes numérotées par zone, liste officielle des intermédiaires agréés. | TreasuryDirect, guide du DMO |
| **Pilote institutionnel** | 3 mois gratuits, ce qui est fourni, ce qui est demandé, un seul formulaire. Aucun prix. | — |

## 5. Système visuel
- **Identité :** garder le bleu marine et l'or actuels, qui sont propres à ABM. Ajouter un mode sombre pour les tableaux denses.
- **Typographie :**
  - une police sans empattement lisible pour l'interface ;
  - une police à chiffres de largeur fixe (« tabular ») pour tous les montants et taux ;
  - au minimum 12 px pour le texte et 11 px pour les badges et les sources.
- **Badges de nature**, toujours visibles et de même forme partout : FAIT (publié), CALCUL, NON PUBLIÉ, DÉDUIT / INTERPOLÉ.
- **Couleurs :**
  - aucune couleur ne doit signifier « bon » ou « mauvais » placement ; les hausses et baisses de taux sont neutres, avec une flèche et un signe ;
  - XOF et XAF sont distingués par une étiquette, jamais additionnés.
- **Tableaux :** en-têtes fixes, colonnes masquables, densité réglable (compacte ou confortable), défilement horizontal uniquement dans le tableau.
- **Graphiques :**
  - un seul type par question : ligne pour une évolution, points pour la courbe observée, barres pour les volumes ;
  - source et date sous chaque graphique.
- **Accessibilité :** focus visible en bleu marine, contraste AA, libellés traduits, mise en page de droite à gauche en arabe.

## 6. Phases
| Phase | Contenu | Dépend de |
|---|---|---|
| 1 | Navigation à 5 entrées, données publiques, accueil, page pilote, mentions légales (lots 1 et 2 de `REVUE-CRITIQUE-2026-10-23.md`) | Crédits Lovable ou accès GitHub |
| 2 | Système visuel : badges, typographie, tableaux, mode sombre, accessibilité (lot 3) | Phase 1 |
| 3 | Pages Titre (ISIN) et Données & méthode, export CSV sourcé | Phase 2 |
| 4 | Alertes (nouvelle adjudication, échéance) par e-mail | Service d'envoi et sa clé |
| 5 | Comptes d'équipe et organisations | Phase 3 |

Avant chaque phase, je ferai une maquette cliquable à valider avant toute modification du code.

## Sources (recherche du 23/10/2026)
- Fiscal Data, lancement en 2020 : https://fiscal.treasury.gov/about-us/news/fiscal-service-launches-new-financial-data-website
- Jeu de données des adjudications du Trésor : https://catalog.data.gov/dataset/treasury-securities-auction-results
- FINRA Fixed Income Data : https://www.finra.org/finra-data/fixed-income ; https://www.finra.org/investors/insights/what-is-TRACE
- EMMA (MSRB) : https://msrb.org/sites/default/files/2022-09/MSRB-Reporters-Guide-to-Using-EMMA.pdf
- DMO, résultats des opérations sur gilts : https://www.dmo.gov.uk/data/gilt-market/results-of-gilt-operations
- Exemples de résultats d'adjudication (MarketScreener) : https://www.marketscreener.com/news/u-k-sells-5-billion-pounds-in-may-2029-gilt-ce7f59dad088f620
- Bank of England, courbes de taux (documentation du paquet R `boe`) : https://cran.r-project.org/web/packages/boe/refman/boe.html
- Calculateur de gilts : https://tools.incoherency.co.uk/uk-gilt-yield-calculator
- Koyfin, aide « Global Bonds, Yield Curves & FX » : https://www.koyfin.com/help/global-bonds-yield-curves-fx/amp/
- Cbonds, indices Afrique : https://cbonds.com/indexes/1351/
- BAD, AFMI : https://www.afdb.org/en/topics-and-sectors/initiatives-partnerships/african-financial-markets-initiative-afmi ; https://www.mfw4a.org/news/african-financial-markets-initiative-afmi
