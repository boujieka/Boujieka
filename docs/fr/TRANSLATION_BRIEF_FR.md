# Brief de traduction : Livre 7 et ses ressources en français professionnel

Ce brief s'applique à toute la traduction française du Livre 7 (*Hydropower Development and Finance*), de MANUAL 7, du classeur MODEL 7 et des ressources associées. Tous les traducteurs l'appliquent à la lettre, pour que le vocabulaire soit le même d'un chapitre à l'autre.

## 1. Public et ton

- Lecteurs : développeurs de projets, banquiers et prêteurs, institutions de financement du développement, investisseurs, ministères des Finances et de l'Énergie, régulateurs et conseillers d'Afrique francophone (Côte d'Ivoire, Sénégal, Cameroun, RDC, Guinée, Madagascar, etc.), ainsi que des lecteurs de France, de Belgique, de Suisse et du Canada.
- Registre : français professionnel de la finance de projet, clair et direct, au présent. Phrases courtes. Pas de calque de l'anglais. Pas de jargon inutile.
- Traduire le sens, pas les mots. Un financier francophone doit pouvoir lire le texte sans deviner qu'il s'agit d'une traduction.
- Ne rien ajouter, ne rien retrancher : mêmes faits, mêmes chiffres, mêmes réserves, mêmes sources. Ne jamais inventer de source, de chiffre ou de nom.
- Pas de formules creuses ni d'emphase (« il convient de noter que », « véritable », « crucial », « incontournable », « au cœur de », « dans un monde en constante évolution »). Le texte anglais n'en contient pas ; la traduction non plus.
- Ne pas utiliser de tiret cadratin (—) ni de tiret demi-cadratin (–) dans le texte courant ; utiliser une virgule, deux-points ou des parenthèses. Le trait d'union normal (-) reste utilisé dans les mots composés.

## 2. Ce qu'il ne faut jamais modifier (balisage technique)

Ces éléments sont lus par des programmes. Les recopier exactement, caractère pour caractère :

1. Les champs de chiffres du modèle : `{{m.capex_real|n0}}`, `{{base_sized.kpi_eirr|pct1}}`, `{{x.debt_total|n0}}`, etc. Les garder intacts ; on peut déplacer le champ dans la phrase française. Le programme les remplacera par des chiffres au format français (virgule décimale, « % » précédé d'une espace). Exemple : `USD {{m.debt_m|n0}} million` devient `{{m.debt_m|n0}} millions USD` ; `{{m.cf|pct0}}` reste `{{m.cf|pct0}}` (ne pas ajouter de « % »).
2. Les références de sources entre crochets : `[HY-08]`, `[DE:S1; A1:S4]`, `[CI]`, `[DE:BENCH]`, `[R2:S3]`, `[LIT:S5]`. Ne jamais les traduire, les déplacer d'une phrase à une autre ni les supprimer.
3. Les marqueurs `%%GATES7`, `%%FRAMEWORK7`, `%%CHECKS7`, `%%CASES7`, `%%SOURCES7` : les laisser seuls sur leur ligne.
4. Les débuts de ligne `Table: ` et `Note: ` (marqueurs de légende de tableau et de note sous un tableau) : garder exactement `Table: ` ou `Note: ` en anglais, puis traduire la suite. Exemple : `Table: Table 18.1. Kasiri at a glance` devient `Table: Tableau 18.1. Kasiri en un coup d'œil`.
5. Les chemins d'images et attributs : `](figures/fig2_1_hydrology.png)`, `{: style="width:32mm"}`. Traduire la légende entre `![` et `]`.
6. La structure Markdown : niveaux de titres (#, ##, ###), numérotation (1.1, N.3…), tableaux (même nombre de colonnes, même ligne `|---|`), listes, gras, italique, blocs de code (ne pas traduire le code, ni les noms de cellules ou de formules Excel dans les blocs de code ; on peut traduire les commentaires en langage naturel).
7. Les noms des feuilles du classeur (`01_CONTROL_PANEL`, `30A_CLOSE_READINESS`, `35_BOOK_CHECK`…), les références de cellules (`C15`), les noms de fichiers et les adresses web : inchangés.
8. Les libellés de sortie du modèle qui restent en anglais dans le classeur : `STOP`, `NOT READY`, `CONDITIONAL GO`, `GO`, `MET`, `PARTIAL`, `NOT MET`, `NO EVIDENCE`, `ALL OK`, `ALL PASS`, `PASS`, `CHECK`, `READY`, `GAP`, `NOT BANKABLE`. Dans le texte, à la première occurrence d'un chapitre, donner le sens en français entre parenthèses, par exemple « NOT READY (non prêt) », « CONDITIONAL GO (feu vert sous conditions) », « MET (franchie) », « PARTIAL (partielle) », « NOT MET (non franchie) », « NO EVIDENCE (sans preuve) ». Ensuite, garder le libellé anglais en capitales.
9. Les noms propres de l'étude de cas : « Kasiri River Hydro » (nom du projet, inchangé), « la rivière Kasiri », « la République de Navaria » (fictive). Les noms d'auteurs, d'institutions et les titres des ouvrages cités restent dans leur langue d'origine (on peut ajouter une traduction du titre entre parenthèses quand c'est utile).

## 3. Titres et numérotation

- `# Chapter 1. ...` devient `# Chapitre 1. ...`
- `## Annex A. ...` devient `## Annexe A. ...` ; `# Annexes` reste `# Annexes`.
- `# About this book` : `# À propos de ce livre` ; `# Preface` : `# Préface` ; `# Introduction: how to read a hydro project` : `# Introduction : comment lire un projet hydroélectrique`.
- `# Technical due-diligence reference` : `# Référentiel de due diligence technique`.
- Les renvois internes suivent : « Chapter 14 » devient « chapitre 14 », « Annex N » devient « annexe N », « Table 18.1 » devient « tableau 18.1 », « Figure 2.1 » devient « figure 2.1 », « section D2 » reste « section D2 ».
- Les deux lignes en italique au début de chaque chapitre : `*Place in the analytical chain: ...*` devient `*Place dans la chaîne d'analyse : ...*` et `*Who must accept the answer: ...*` devient `*Qui doit accepter la réponse : ...*`.
- Le titre du livre cité dans le texte : « *Hydropower Development and Finance* » devient « *Développement et financement de l'hydroélectricité* » quand il s'agit de ce livre-ci ; pour l'édition anglaise, garder le titre anglais.

## 4. Typographie française

- Virgule décimale : 1,53 ; 13,8 % ; 0,689.
- Séparateur de milliers : une espace : 2 614 ; 1 000 ; 292 GWh. (Écrire une espace normale ; un programme la rendra insécable.)
- Espace avant « % », « : », « ; », « ? », « ! » et à l'intérieur des guillemets « ». Écrire une espace normale ; un programme la rendra insécable.
- Guillemets français « … » pour les citations et les termes cités. Les apostrophes droites (') sont acceptées.
- Monnaie : « 145 millions USD », « 1,28 million USD » (singulier sous 2), « 9 millions USD sur six ans ». En abrégé dans les tableaux : « M USD » (par exemple « Dette senior (M USD) »). « USD/kW », « USD/MWh », « c USD/kWh » restent.
- Unités : MW, GWh, MWh, m³/s, km, mm, % : notation internationale, avec une espace entre le nombre et l'unité.
- Dates : « 3 octobre 2026 ». Années : « 2026 ». Ordinaux : « 1er », « 2e ».
- Majuscules : seulement au premier mot des titres et aux noms propres (« Chapitre 3. La rivière et la ressource », pas « La Rivière et la Ressource »). « l'État » avec majuscule quand il s'agit de la puissance publique.
- Sigles : à la première occurrence d'un chapitre, développer le sigle français, puis l'utiliser seul. Quand l'usage international est le sigle anglais (DSCR, LLCR, EPC, O&M, PPA dans un contexte contractuel anglophone), garder le sigle anglais après l'expression française.

## 5. Glossaire obligatoire (anglais : français)

| Anglais | Français |
|---|---|
| financial close | bouclage financier |
| ready for financial close | prêt pour le bouclage financier |
| close readiness | maturité pour le bouclage, préparation au bouclage |
| Hydro Readiness Framework™ | Hydro Readiness Framework™ (nom de marque, non traduit ; décrire au besoin comme « le cadre de maturité hydroélectrique ») |
| gate / evidence gate | porte / porte de preuve (féminin : « une porte critique franchie ») |
| critical gate | porte critique |
| gate met / not met | porte franchie / non franchie |
| 9-gate development screen | filtre de développement à neuf portes |
| financial close decision | décision de bouclage financier |
| question (of the framework) | question (Q1 à Q8) |
| developer | développeur |
| sponsor | promoteur |
| co-developer | co-développeur |
| lender / lenders | prêteur / prêteurs |
| lender group | pool de prêteurs |
| lenders' technical adviser (LTA) | conseiller technique des prêteurs (LTA) |
| government / the state | l'État ; le gouvernement (quand il s'agit de l'exécutif) |
| Ministry of Finance | ministère des Finances |
| offtaker / buyer | acheteur (l'acheteur d'électricité) |
| utility | compagnie d'électricité (société nationale d'électricité) |
| power purchase agreement (PPA) | contrat d'achat d'électricité (CAE) ; on peut écrire « CAE (PPA) » à la première occurrence |
| independent power producer (IPP) | producteur indépendant d'électricité (PIE) |
| implementation agreement / concession agreement | convention de mise en œuvre / convention de concession |
| public-private partnership (PPP) | partenariat public-privé (PPP) |
| development finance institution (DFI) | institution de financement du développement (IFD) |
| blended finance | financement mixte |
| concessional debt | dette concessionnelle |
| project preparation facility | facilité de préparation de projets |
| senior debt | dette senior |
| debt sizing | dimensionnement de la dette |
| sculpted repayment | remboursement sculpté |
| debt service cover ratio (DSCR) | ratio de couverture du service de la dette (DSCR) |
| minimum / average DSCR | DSCR minimum / moyen |
| loan life cover ratio (LLCR) | ratio de couverture sur la durée du prêt (LLCR) |
| debt service reserve account (DSRA) | compte de réserve du service de la dette (DSRA) |
| cash sweep | balayage de trésorerie (cash sweep) |
| gearing | taux d'endettement (gearing) |
| equity | fonds propres |
| private equity IRR | TRI des fonds propres privés |
| project IRR | TRI du projet |
| internal rate of return (IRR) | taux de rendement interne (TRI) |
| net present value (NPV) | valeur actuelle nette (VAN) |
| risk-weighted (expected) NPV | VAN pondérée par le risque (VAN espérée) |
| success path | scénario de succès ; « sur le scénario de succès » |
| development premium | prime de développement |
| break-even | point mort, seuil d'équilibre |
| step-up (in value) | revalorisation |
| financing gap | besoin de financement non couvert (écart de financement) |
| sources and uses | ressources et emplois |
| waterfall | cascade des flux (waterfall) |
| distributions | distributions (aux actionnaires) |
| levelised cost of energy (LCOE) | coût actualisé de l'énergie (LCOE) |
| tariff / blended tariff | tarif / tarif moyen pondéré |
| capacity payment / energy payment | paiement de capacité / paiement d'énergie |
| energy-only tariff | tarif rémunérant uniquement l'énergie |
| take-or-pay | take-or-pay (obligation d'enlever ou de payer) |
| deemed energy | énergie réputée livrée |
| curtailment | écrêtement |
| payment security | garantie de paiement |
| letter of credit | lettre de crédit (crédit documentaire stand-by) |
| sovereign guarantee | garantie souveraine |
| budget backstop | garantie budgétaire (filet de sécurité budgétaire) |
| political risk insurance / cover | assurance contre le risque politique |
| partial risk guarantee | garantie partielle de risque |
| contingent liabilities | passifs éventuels |
| fiscal impact / fiscal exposure | impact budgétaire / exposition budgétaire |
| debt sustainability | viabilité de la dette (cadre de viabilité de la dette, CVD, du FMI et de la Banque mondiale) |
| arrears | arriérés |
| collection rate | taux de recouvrement |
| retail tariff | tarif de détail (tarif aux consommateurs finals) |
| conditions precedent (CPs) | conditions suspensives |
| term sheet | term sheet (feuille de modalités) |
| due diligence | due diligence (audit préalable) |
| investment committee / credit committee | comité d'investissement / comité de crédit |
| bankable / bankability | bancable / bancabilité |
| feasibility study / pre-feasibility | étude de faisabilité / préfaisabilité |
| reconnaissance | reconnaissance (identification du site) |
| permit / licence / consent | permis / licence / autorisation |
| water-use permit | permis d'utilisation de l'eau |
| land rights | droits fonciers |
| environmental and social impact assessment (ESIA) | étude d'impact environnemental et social (EIES) |
| resettlement action plan (RAP) | plan d'action de réinstallation (PAR) |
| environmental flow | débit réservé (débit écologique) |
| IFC Performance Standards | normes de performance de l'IFC |
| Equator Principles | Principes de l'Équateur |
| run-of-river | au fil de l'eau |
| reservoir / storage | réservoir / retenue |
| weir / dam | seuil / barrage |
| headrace / tailrace / penstock | canal d'amenée / canal de fuite / conduite forcée |
| powerhouse | centrale (bâtiment de l'usine) |
| head (gross / net) | hauteur de chute (brute / nette) |
| design flow | débit d'équipement |
| flow duration curve | courbe des débits classés |
| flow record / gauging | série de débits / jaugeage |
| mean annual flow | débit moyen annuel (module) |
| P50 / P90 one-year / P90 ten-year | P50 / P90 à un an / P90 à dix ans |
| capacity factor | facteur de charge |
| installed capacity | puissance installée |
| firm energy | énergie garantie |
| drought / dry year / wet year | sécheresse / année sèche / année humide |
| sediment | sédiments, transport solide |
| turbine / generator | turbine / alternateur |
| electro-mechanical equipment (E&M) | équipements électromécaniques |
| civil works | génie civil |
| EPC contract (turnkey) | contrat EPC (clés en main) |
| split packages / multi-contract | lots séparés / multicontrats |
| owner's engineer | ingénieur du maître d'ouvrage |
| owner | maître d'ouvrage |
| contractor | entrepreneur |
| liquidated damages | pénalités forfaitaires (liquidated damages) |
| cost overrun / delay | dépassement de coûts / retard |
| contingency | provisions pour aléas |
| reference class (forecasting) | classe de référence (prévision par classe de référence) |
| ground conditions / geotechnical | conditions géologiques / géotechnique |
| interface risk | risque d'interface |
| commercial operation date (COD) | date de mise en service commerciale (COD) |
| operation and maintenance (O&M) | exploitation et maintenance (O&M) |
| transmission line / evacuation line | ligne de transport / ligne d'évacuation |
| grid | réseau |
| demand | demande |
| concession | concession |
| standby equity | fonds propres de réserve (standby equity) |
| refinancing | refinancement |
| exit | sortie |
| stress test | test de résistance (stress) ; « stresser » est accepté dans le registre oral |
| sensitivity / tornado chart | sensibilité / diagramme en tornade |
| scenario | scénario |
| base case | cas de base |
| model integrity checks | contrôles d'intégrité du modèle |
| book check | contrôle de cohérence avec le livre |
| dashboard | tableau de bord |
| control panel | panneau de contrôle |
| workbook / sheet | classeur / feuille |
| input / output | donnée d'entrée / résultat |
| decision support, not investment advice | outil d'aide à la décision, pas un conseil en investissement |
| companion materials | ressources d'accompagnement |
| case study | étude de cas |
| work programme | programme de travail |
| verification status | statut de vérification |
| full text read / landing or summary page read / search summary only | texte intégral lu / page d'accueil ou résumé lu / résumé de recherche seulement |

Les termes absents de ce glossaire sont traduits selon l'usage de la finance de projet en Afrique francophone (documents de la Banque mondiale, de l'AFD, de la BAD, de l'IFC et des régulateurs en français).

## 6. Fichiers

- Livre : chaque fichier `book7/src/<nom>.md` est traduit dans `book7/src_fr/<nom>.md` (même nom ; `book7/src/tech/annex_n.md` va dans `book7/src_fr/tech/annex_n.md`).
- Manuel : `manual/fr_work/partN.md` est traduit dans `manual/fr_work/partN_fr.md`.
- Classeur : dans `model/fr_work/strings_N.json`, remplir le champ `"fr"` de chaque entrée (sans modifier `"en"` ni `"sheet"`) et enregistrer sous `model/fr_work/strings_N_fr.json`.

## 7. Contrôle avant remise

Pour chaque fichier traduit, vérifier :
- même nombre de champs `{{...}}`, de références `[...]` de sources, de tableaux (et de colonnes par tableau), de titres, de figures et de marqueurs `%%` que l'original ;
- aucun passage oublié ou résumé ;
- glossaire respecté ; aucune phrase en anglais en dehors des éléments protégés.
