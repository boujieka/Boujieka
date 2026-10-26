# Volume 1 — Fichiers KDP (maquette)

## Contenu

| Fichier | Rôle |
|---|---|
| `sortie/interieur.pdf` (non versionné, trop lourd pour GitHub : relancer `python3 build_kdp.py`) | Intérieur, **67 pages (volume complet)**, broché **8,25 × 6 po paysage**, fond perdu (8,375 × 6,25 po) |
| `sortie/couverture.pdf` | Couverture complète (4ᵉ + dos + 1ʳᵉ), calculée pour le nombre de pages actuel |
| `sortie/apercu_*.jpg` | Aperçus |
| `manifest.txt` | Ordre des pages : ajouter les nouvelles planches ici, puis relancer `python3 build_kdp.py` |
| `sources/` | Planches retenues ; `sources/ecartees/` : versions en double non retenues |

## Ordre retenu et doublons

1. Pages de début (générées) : titre, mentions légales et avertissement, « Comment lire cette BD », sommaire.
2. **Prologue P1** — 4 versions reçues ; retenue : la version avec titre « Prologue » et **étiquettes de
   noms** (elle présente les personnages au lecteur). Écartées : la version portrait (format différent
   des autres planches) et deux versions paysage sans étiquettes.
3. Prologue P2.
4. Épisode 1 : planches 1 à 4, puis **page documentaire** — 2 versions reçues ; retenue : la version au
   plan sombre, dont les légendes sont exactes. Écartée : la version au plan « 3D », qui contient des
   **erreurs** (Livre des Portes placé « paroi nord » au lieu de sud, Amdouat dans le corridor C, salle à
   piliers notée « D » au lieu de F, et une scène de taureau inventée pour le Livre de la Terre).
5. Épisode 2 : planches 1 à 4, page documentaire.
6. Épisode 3 : planches 1 à 3 (**planche 4 et page documentaire manquantes**).
7. Page finale « À suivre » avec la devise de la série.

## Mise à jour — 2ᵉ envoi (19 nouvelles planches)

- **Doublon** : la 1ʳᵉ image de l'envoi est identique, octet pour octet, à l'épisode 3, planche 3, déjà en
  place : non ajoutée.
- **Ajoutées dans l'ordre** : ép. 3 (planche 4, page documentaire), ép. 4 (complet), ép. 5 (planches 1-4),
  ép. 6 (complet), ép. 7 (planches 1-3). Le volume compte maintenant **39 pages** (le minimum KDP de 24
  est atteint).
- **Encore manquants** : page documentaire de l'ép. 5 ; ép. 7 planche 4 et page documentaire ; épisodes
  8 à 12.

### Erreurs relevées dans le 2ᵉ envoi (à corriger avant publication)

| Page | Gravité | Problème |
|---|---|---|
| Ép. 3, planche 4, case 4 | **Grave** | **Référence inventée** à l'écran : « L. Pleuger (2020), *The Book of the Earth in the Tomb of Ramesses VI*, *Journal of Egyptian Archaeology* 106, p. 37-56 ». Cet article n'existe pas sous ce titre : la vraie référence est L. Pleuger, « Le Livre de la Terre. À propos du sens de lecture… », *BABELAO* 9 (2020), p. 45-94 |
| Ép. 7, planche 1, case 5 | **Grave** | Le schéma nomme l'antichambre « **Antichambre I (salle arrière de KV12)** » : faux. L'antichambre I appartient à KV9 ; c'est la salle arrière de KV12 qui a été percée |
| Ép. 4, planche 4, case 2 | Moyenne | Phrase anglaise attribuée à Darnell à l'écran (« Roberson has suggested that the forward part… ») : **formulation inventée**, non vérifiée dans le livre. Rendre le texte de l'écran illisible |
| Ép. 4, planche 3 | Moyenne | Note interne imprimée dans la BD : « Source : Rê, la nuit, dans la barque : tête de bélier (**bible 03 §1**) » ; et « À suivre — Épisode 5 : *Le cycle des deux horizons* » : mauvais titre, et ce « À suivre » n'a pas sa place en planche 3 (il est déjà en planche 4) |
| Ép. 4, page documentaire | Moyenne | Renvois internes visibles (« bible 03 §1 ») et référence incomplète « Wilkinson, 2003, p. … » |
| Ép. 4, planche 1, cases 2-4 | Moyenne | Aker dessiné en **deux sphinx séparés** ; dans KV9 il s'agit d'un double sphinx (deux corps **joints dos à dos**) |
| Ép. 7, planche 3 | Moyenne | Le scribe écrit sur une **planchette à pince avec un stylo** (anachronique : ostracon ou papyrus et calame) ; fautes : « est passéé », « CARIER » (carrier), « trvers » (travers) |
| Ép. 6, planche 1, case 5 | Faible | Texte déformé sur la feuille déchirée (« CACLE E ? ») |
| Ép. 5, planche 4, case 6 | Faible | Le scan indique « Corridor F » : F est la salle à piliers |
| Ép. 6, page documentaire ; ép. 7, planche 1 | Faible | Plans de KV9 / KV12 **dessinés librement** (formes inventées) : redessiner d'après le Theban Mapping Project |
| Ép. 3, page documentaire | Faible | Plan de la chambre J et vignettes « d'après Piankoff 1946 / Hornung 1972… » **inventés** ; disposition à reprendre de Piankoff & Rambova 1954 |
| Ép. 5, planche 3, case 6 | Faible | La paroi de QV66 dessinée est imaginaire (le cadre l'indique « attestée ailleurs », mais l'image ne copie pas la vraie paroi) |
| Toutes | Faible | « PLANCHE x/7 » au lieu de x/5 ; « KERBU » et « DR KERBU » alternent dans les bulles |

## Mise à jour — 3ᵉ et 4ᵉ envois (volume complet)

**Choix entre doublons**

| Page | Versions reçues | Retenue | Raison |
|---|---|---|---|
| Ép. 7, planche 4 | 2 | Version 2 | Dieux nettement à tête de bélier (case 4), légendes qui situent les scènes (« paroi nord de D, suite en E ») |
| Ép. 7, page documentaire | 2 | Version paysage | L'autre version a un format différent (1536 × 1024) et une mise en page de bandeau |
| Ép. 8, planche 3 | 2 (« 3/6 » et « 3/7 ») | « 3/6 » | L'autre imprime une note interne « (bible 03) » et les balises [S]/[H] dans les cases ; Tatenen debout sur le tertre, conforme au script |
| Ép. 11, planche 4 | 2 | Version sans notes | L'autre imprime des notes de travail dans les cases (« Source : bible/03… », « Intention : renoncement de Marsac… », « Relevé fictif (F) ») |
| Ép. 12, planche 4 | 2 | « FIN DU VOLUME 1 » | La surimpression finale montre le scarabée avec un dieu à tête de bélier, comme le disque de la porte B ; l'autre montre deux têtes de faucon |
| Ép. 12, page documentaire | 2 | Plan lisible A → K | L'autre a des numéros de nuits illisibles (« 3B.10-11 ») ; mais voir l'erreur d'orientation ci-dessous |

**Erreurs relevées (3ᵉ et 4ᵉ envois)**

| Page | Gravité | Problème |
|---|---|---|
| Ép. 11, planche 4 | **Grave** | En-tête « **ÉPISODE 12** » alors que c'est l'épisode 11 (le titre « La nuit avant l'aube » est juste) |
| Ép. 8, planche 2 | **Grave** | En-tête « **VOLUME 2** » au lieu de Volume 1 |
| Ép. 12, page documentaire | Moyenne | Flèche « **Ouest (≈ 290°)** » placée du côté de l'entrée : c'est l'inverse, l'axe s'enfonce **vers l'ouest** depuis une entrée tournée vers l'est |
| Ép. 11, page documentaire | Moyenne | « Tête à l'ouest (le soleil entre) / Pieds à l'est (le soleil sort) » : orientation des Nout de la voûte **non sourcée** (N) |
| Ép. 8, planche 3, case 2 | Moyenne | Faute : « **KEOBU** » au lieu de Kerbu |
| Ép. 9, planche 1, case 7 ; ép. 8, planche 4, case 7 | Moyenne | Sarcophage dessiné en **caisse rectangulaire** ; la cuve restaurée exposée dans J est **anthropoïde** (ép. 9, planche 2 la montre correctement) |
| Ép. 12, planche 3, case 2 | À vérifier | Le cartouche dit « tête de bélier » : vérifier que le dieu dans la barque n'a pas une tête de faucon |
| Ép. 12, planches 1 à 4 | Faible | Numérotation « x/4 » alors que les autres épisodes portent « x/7 » (les deux sont fausses : 4 planches + 1 page doc.) |
| Ép. 7, page documentaire | Faible | Faute « chaudrns » ; plan de KV12 et orientation inventés |
| Ép. 9, page documentaire | Faible | Portraits imaginaires de Belzoni et de Loret dans la frise |

## Pourquoi le format paysage 8,25 × 6 po

Les planches reçues sont en **paysage 4:3** (1448 × 1086 px). KDP propose **un seul format paysage**
broché : **8,25 × 6 po** (page KDP « Trim sizes », consultée le 26/10/2026). Il accueille les planches
sans les tourner ni les réduire à l'excès. Conséquence : la couverture doit elle aussi être **paysage**
(voir plus bas).

## Bloquant avant publication

1. **Volume complet : 67 pages** (4 pages de début, prologue, 12 épisodes × 5 pages, page de fin). Au-dessus
   du minimum KDP (24) ; en dessous des 75 pages (couverture rigide) et des 79 pages (texte sur le dos).
2. **ISBN** : celui de la couverture reçue (978-2-495678-01-5) est **invalide** — son chiffre de contrôle
   devrait être 8, pas 5 — et a été inventé par le générateur d'images. Il a été **effacé**. Utiliser
   l'ISBN gratuit de KDP ou un ISBN AFNIL, et laisser KDP placer le code-barres.
3. **Couverture paysage à créer** : l'illustration reçue est en portrait. La couverture actuelle est une
   **épreuve provisoire** (illustration portrait centrée sur un fond flou). Prompts ChatGPT ci-dessous.
4. **Mentions légales** : compléter ISBN, mois du dépôt légal, et vérifier le nom d'auteur « Emma B. »
   (repris de la couverture).
5. **Déclaration IA sur KDP** : les illustrations sont **générées par IA** ; le texte du scénario a été
   rédigé avec des agents IA puis révisé — selon la règle KDP, il est aussi **à déclarer comme généré
   par IA**, même après modifications.
6. **Droit égyptien** sur les images d'antiquités (loi 117/1983, règlement art. 146-147) : avis
   juridique avant la vente (voir la bible, chapitre 6).

## Erreurs relevées dans les images (à corriger par régénération ou retouche)

| Page | Problème |
|---|---|
| Toutes les planches | En-tête « **PLANCHE x/7** » : chaque épisode compte 4 planches + 1 page documentaire → « x/5 » (ou « x/4 ») |
| Couverture | « Aker » dessiné en **deux léopards tachetés** : ce n'est pas l'iconographie d'Aker (double lion / double sphinx) |
| Couverture (4ᵉ) | « Des liens avec l'Afrique d'hier et d'aujourd'hui » : promesse absente du contenu du Volume 1 |
| Prologue P1 | Le **disque du soleil est visible** alors que le cartouche dit que le soleil n'a pas encore franchi les montagnes |
| Prologue P2, cases 4 et 6 | La main de Kerbu **touche** le disque peint (le script dit « sans la toucher » ; règle de conservation) |
| Ép. 1, P1, cases 3-4 | Graffito grec **lisible inventé** (« ΑΠΟΛΛΩΝΙΟΣ… ») : à remplacer par une copie d'un graffito réel ou par des lettres floues |
| Ép. 1, P3, case 1 | La main touche le cartouche |
| Ép. 1, P4, cases 6-7 | Disque de la porte B : le dieu **à tête de bélier** manque (des figures à tête de faucon à la place), alors que Kerbu parle du « bélier de la nuit » ; référence : Theban Mapping Project |
| Ép. 1, page documentaire | Le plan montre un axe **coudé** ; l'axe de KV9 est **rectiligne** (TMP) |
| Ép. 2, P4, case 3 | Salle du jugement d'Osiris dessinée de façon générique, non d'après la paroi de KV9 |
| Ép. 2, page documentaire | « Plafond de C : horloge stellaire » : selon le TMP, les horloges stellaires sont sur les côtés du plafond de F ; B et C portent constellations et décans |
| Ép. 3, P1, case 3 | Sarcophage dessiné en caisse rectangulaire ; le sarcophage restauré est **anthropoïde** |
| Ép. 3, P3 | Piankoff et Husson dessinés de face : visages imaginaires de personnes réelles (préférer de dos) |
| Personnages | Nefertari (sans foulard, cheveux longs) et Maya (cheveux longs bouclés) diffèrent des fiches : ils sont cohérents d'une planche à l'autre → mettre à jour les fiches plutôt que les images |

## Qualité d'impression

- Résolution réelle des planches : **207 ppp** à la taille imprimée (KDP recommande 300). Le script les
  agrandit à 300 ppp (Lanczos + légère accentuation) pour éviter l'alerte KDP, **mais cela n'ajoute pas
  de détail**. Pour une qualité supérieure : générer les planches en plus haute définition, ou passer un
  agrandisseur IA (ex. Upscayl, Topaz, ou un service en ligne) puis relancer le script.
- Couleurs : fichiers RVB ; KDP convertit à l'impression. Commander une **copie d'épreuve** avant la mise
  en vente pour contrôler les couleurs sombres (les planches de tombeau sont très foncées).

## Réglages KDP

Broché · Format **8,25 × 6 po** · Encre **couleur premium**, papier blanc · **Fond perdu : oui** ·
Couverture brillante (conseillé pour la couleur) · Intérieur : `interieur.pdf` · Couverture :
`couverture.pdf` (à régénérer à chaque changement du nombre de pages : l'épaisseur du dos en dépend).

## Prompts ChatGPT pour la couverture paysage

Coller d'abord le « Brief de série » (`prompts_chatgpt/00_mode_d_emploi_chatgpt.md`), puis :

```
1re de couverture d'une bande dessinée, format PAYSAGE 3:2 (sera imprimée en 8,25 × 6 pouces).
Même style que la couverture précédente : le Dr Kerbu de trois quarts dos, à droite, lève une lampe dont
le faisceau éclaire les parois peintes de la chambre funéraire de Ramsès VI (registres de figures ocre
et rouges) ; au plafond, la voûte bleu nuit étoilée avec le corps arqué de la déesse Nout ; au centre-
gauche, un grand disque solaire rouge-or porté par des bras levés, en style de peinture murale
égyptienne. Pas de léopards : si un double lion apparaît, ce sont deux lions dos à dos (Aker).
Laisse le tiers gauche et le haut plus calmes pour le titre « Les Mystères du tombeau de Ramsès VI »,
le sous-titre « Le Livre de la Terre — Le secret de la renaissance solaire », la mention « Volume 1 »
et « Emma B. présente » : écris ces textes exactement, sans faute, en lettres dorées gravées.
Garde une marge de sécurité : aucun texte à moins de 5 % des bords.
```

```
4e de couverture assortie, format PAYSAGE 3:2. Fond : paroi de tombeau dans la pénombre, plafond étoilé
en haut. À gauche, un encadré sombre et lisible pour un texte de présentation (je l'ajouterai
moi-même : laisse la zone vide). En bas à droite, laisse une zone vide et unie d'environ un quart de la
largeur et un cinquième de la hauteur pour le code-barres : n'y dessine RIEN, et n'invente ni ISBN ni
code-barres. Aucun texte dans l'image.
```

Ensuite : déposer les deux images dans `sources/` sous les noms `couverture_face.png` et
`couverture_dos.png`, puis relancer `python3 build_kdp.py` : le script les utilise automatiquement à la place
de l'épreuve provisoire.
