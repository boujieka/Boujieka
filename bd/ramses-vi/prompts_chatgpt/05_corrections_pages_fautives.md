# Prompts ChatGPT — Corrections des pages fautives

Une entrée par page à corriger, **dans l'ordre du livre**. Le nom du fichier est celui de
`kdp/sources/` : la page corrigée doit être enregistrée **sous le même nom**, puis il suffit de relancer
`python3 build_kdp.py`.

## Méthode (à lire d'abord)

1. Ouvre une conversation ChatGPT et **téléverse l'image fautive** (le fichier indiqué).
2. **Si l'outil de sélection est disponible** (pinceau « Sélectionner » sur l'image générée ou
   téléversée), **sélectionne seulement la zone à corriger**, puis colle le prompt. C'est la méthode la
   plus sûre : le reste de la planche ne bouge pas.
3. Sans sélection, ChatGPT redessine toute l'image : vérifie alors que **les autres cases, les bulles et
   les visages n'ont pas changé**. Sinon, recommence ou garde l'ancienne version.
4. **Vérifie toujours le texte** de l'image corrigée, lettre par lettre : ChatGPT peut introduire de
   nouvelles fautes en corrigeant les anciennes.
5. Garde le format **1448 × 1086 px (paysage 4:3)** : demande « même format, même cadrage » si besoin.

Chaque prompt commence par une phrase de cadrage commune :

```
Voici une planche de ma bande dessinée. Modifie UNIQUEMENT ce que je décris ci-dessous. Garde tout le
reste strictement identique : la mise en page, les autres cases, les personnages, les couleurs, les
bulles et tous les autres textes. Même format paysage.
```

> Dans les prompts ci-dessous, « [CADRAGE] » signifie : colle d'abord cette phrase.

---

## A. Correctifs prioritaires (erreurs graves)

### 1. Ép. 3, planche 4 — `16_ep03_P4.png` — référence inventée (case 4)
```
[CADRAGE] Case 4 : sur l'écran du téléphone de Nefertari, la référence bibliographique affichée est
fausse. Remplace tout le texte de l'écran par exactement ceci, en petits caractères lisibles :
« L. Pleuger, « Le Livre de la Terre. À propos du sens de lecture d'une composition funéraire de
l'Égypte ramesside », BABELAO 9 (2020), p. 45-94 »
Garde la citation surlignée et la bulle de Nefertari telles quelles.
```

### 2. Ép. 7, planche 1 — `32_ep07_P1.png` — antichambre attribuée à KV12 (case 5)
```
[CADRAGE] Case 5 : sur le schéma, l'étiquette « Antichambre I (salle arrière de KV12) » est fausse.
L'antichambre I fait partie de KV9 ; c'est une salle du tombeau voisin KV12 qui a été percée.
Corrige ainsi : l'étiquette de la salle de KV9 devient « Antichambre I (KV9) », et ajoute une petite
étiquette « Salle arrière de KV12 » sur la zone orange de KV12, à l'endroit de la brèche. Ne change
rien d'autre.
```

### 3. Ép. 8, planche 2 — `39_ep08_P2.png` — « VOLUME 2 » dans l'en-tête
```
[CADRAGE] Dans le bandeau du haut, au-dessus du titre, remplace « VOLUME 2 » par « VOLUME 1 »,
exactement dans la même police dorée et à la même taille.
```

### 4. Ép. 11, planche 4 — `56_ep11_P4.png` — « ÉPISODE 12 » dans l'en-tête
```
[CADRAGE] Dans le cartouche en haut à droite, remplace « ÉPISODE 12 » par « ÉPISODE 11 » (même
police, même taille). Garde le sous-titre « La nuit avant l'aube ».
```

---

## B. Erreurs historiques ou de vraisemblance

### 5. Couverture — `00_couverture_portrait_source.png`
La couverture doit être **refaite en paysage** (voir `kdp/README_KDP.md`, prompts de couverture). En la
refaisant, ajouter :
```
Pas de léopards ni de félins tachetés : si un double lion apparaît, c'est Aker, deux lions (ou deux
sphinx) à pelage uni, joints dos à dos. Sur la 4e de couverture, n'écris pas « Des liens avec
l'Afrique d'hier et d'aujourd'hui ».
```

### 6. Prologue, planche 1 — `01_prologue_P1.png` — soleil visible (cases 1 et 5)
```
[CADRAGE] Cases 1 et 5 : le disque du soleil est visible, alors que le soleil ne s'est pas encore
levé. Supprime le disque solaire : garde seulement une lueur orange pâle derrière la crête des
montagnes, le ciel restant bleu-gris d'avant l'aube.
```

### 7. Prologue, planche 2 — `02_prologue_P2.png` — main qui touche la paroi (cases 4 et 6)
```
[CADRAGE] Cases 4 et 6 : la main du Dr Kerbu touche le disque peint sur la paroi. Écarte sa main de
quelques centimètres : il tend la main vers la peinture SANS la toucher, un petit espace visible entre
ses doigts et la paroi. Le faisceau de sa lampe éclaire le disque.
```

### 8. Ép. 1, planche 1 — `03_ep01_P1.png` — graffito grec inventé (cases 3 et 4)
```
[CADRAGE] Cases 3 et 4 : les lettres grecques gravées sur la paroi sont lisibles et inventées.
Rends-les illisibles : des lettres grecques usées, effacées par le temps, à peine distinctes, sans
qu'aucun mot ne puisse être lu. Garde l'effet de gravure à la pointe et l'éclairage.
```

### 9. Ép. 1, planche 3 — `05_ep01_P3.png` — main qui touche le cartouche (case 1)
```
[CADRAGE] Case 1 : la main touche le cartouche peint. Éloigne la main de quelques centimètres : elle
s'approche de la peinture sans la toucher.
```

### 10. Ép. 1, planche 4 — `06_ep01_P4.png` — disque de la porte B (cases 6 et 7)
> Idéalement, téléverser aussi une **photo de référence** du linteau de la porte B de KV9 (Theban
> Mapping Project) dont tu as les droits.
```
[CADRAGE] Cases 6 et 7 : le disque peint au-dessus de la porte doit contenir un SCARABÉE et un DIEU À
TÊTE DE BÉLIER (pas de tête de faucon), le disque étant encadré par deux déesses, Isis et Nephthys,
agenouillées de part et d'autre. Style des peintures murales égyptiennes, couleurs ocre, rouge et
bleu. Ne change pas Kerbu ni les bulles.
```

### 11. Ép. 1, page documentaire — `07_ep01_doc.png` — plan coudé
```
[CADRAGE] Le plan de KV9 montre un axe coudé : il est faux. Redessine le plan en un AXE PARFAITEMENT
RECTILIGNE, de l'entrée (à gauche) jusqu'au fond (à droite) : entrée A, corridors B, C, D, salle E,
salle à piliers F (carrée, avec 4 piliers), corridors G et H, antichambre I, chambre funéraire J
(4 piliers), petite salle K au bout. Garde les mêmes couleurs, la même légende et les mêmes étiquettes.
```

### 12. Ép. 2, planche 4 — `11_ep02_P4.png` — salle du jugement d'Osiris (case 3)
> Cette case doit copier la **vraie paroi** du corridor C : téléverse une photo de référence (Piankoff &
> Rambova 1954, ou Theban Mapping Project) dont tu as les droits.
```
[CADRAGE] Case 3 : remplace la scène peinte générique par une copie fidèle de la scène de la photo de
référence que je joins (la salle du jugement d'Osiris, 5e porte du Livre des Portes, tombe de
Ramsès VI). Garde la composition de la photo, en style peinture murale, sans hiéroglyphes lisibles.
```

### 13. Ép. 2, page documentaire — `12_ep02_doc.png` — horloges stellaires mal placées
```
[CADRAGE] Corrige l'étiquette « Plafond de C : horloge stellaire ». Elle doit devenir « Plafonds de B
et C : constellations et décans ». Si une autre étiquette parle des horloges stellaires, elle doit
indiquer « Plafond de F (côtés) : horloges stellaires ». Ne change rien d'autre.
```

### 14. Ép. 3, planche 1 — `13_ep03_P1.png` — sarcophage rectangulaire (case 3)
```
[CADRAGE] Case 3 : le sarcophage au fond de la chambre est dessiné comme une caisse rectangulaire.
Remplace-le par le sarcophage restauré de Ramsès VI : une cuve EN FORME DE MOMIE (anthropoïde), en
pierre vert sombre presque noire, polie, avec des joints de restauration visibles ; à côté, les deux
moitiés d'une grande cuve extérieure en granit rouge brisée.
```

### 15. Ép. 3, planche 3 — `15_ep03_P3.png` — visages de personnes réelles
```
[CADRAGE] Dans cette planche, l'égyptologue Alexandre Piankoff et son photographe sont des personnes
réelles : ne montre pas leur visage. Redessine-les DE DOS ou de trois quarts dos, visages non visibles,
mêmes vêtements et mêmes gestes.
```

### 16. Ép. 3, page documentaire — `17_ep03_doc.png` — plan de la chambre J inventé
```
[CADRAGE] Remplace le plan de la chambre J par un schéma simple vu de dessus : un rectangle avec
quatre piliers à l'avant (côté entrée), et quatre étiquettes : « A — paroi nord », « B et C — paroi du
fond (ouest) », « D — paroi sud », « E — pilastre ouest ». Supprime les vignettes « d'après Piankoff
1946 / Hornung 1972 » si elles montrent des images inventées ; garde la frise chronologique.
```

### 17. Ép. 4, planche 1 — `18_ep04_P1.png` — Aker en deux sphinx séparés (cases 2 à 4)
```
[CADRAGE] Cases 2, 3 et 4 : Aker est dessiné comme deux sphinx séparés. Redessine-le en UN SEUL
double sphinx : deux corps de lion JOINTS par l'arrière-train, dos à dos, formant une seule figure
allongée, avec une tête à chaque extrémité, regardant dans deux directions opposées. Style peinture
murale égyptienne.
```

### 18. Ép. 4, planche 3 — `20_ep04_P3.png` — note interne et faux « À suivre »
```
[CADRAGE] Supprime le cartouche qui contient « Source : … (bible 03 §1) » : remplace la zone par le
décor de la case. Supprime aussi le cartouche « À suivre — Épisode 5 : Le cycle des deux horizons »
(il n'a pas sa place sur cette planche) et remplace la zone par le décor.
```

### 19. Ép. 4, planche 4 — `21_ep04_P4.png` — citation anglaise inventée (case 2)
```
[CADRAGE] Case 2 : le texte anglais affiché sur l'écran du téléphone est inventé. Rends le texte de
l'écran ILLISIBLE (lignes floues, comme une page vue de loin), en gardant une ligne surlignée en jaune.
Ne change pas les bulles.
```

### 20. Ép. 4, page documentaire — `22_ep04_doc.png` — renvois internes
```
[CADRAGE] Supprime toutes les mentions « (bible 03 §1) » et « bible 03 » dans les textes. Remplace la
référence incomplète « Wilkinson, 2003, p. … » par : « R. H. Wilkinson, The Complete Gods and
Goddesses of Ancient Egypt, 2003 ». Ne change rien d'autre.
```

### 21. Ép. 5, planche 3 — `25_ep05_P3.png` — paroi de QV66 imaginaire (case 6)
```
[CADRAGE] Case 6 : dans le cadre pointillé, la paroi peinte est inventée. Remplace-la par un fond
uni couleur papyrus, sans image, afin que seule la citation reste dans le cadre pointillé.
```

### 22. Ép. 5, planche 4 — `26_ep05_P4.png` — « Corridor F » (case 6)
```
[CADRAGE] Case 6 : sur l'écran du scan, l'étiquette « Corridor F » est fausse (F est une salle à
piliers). Remplace-la par « Corridor H ». Ne change rien d'autre.
```

### 23. Ép. 6, planche 1 — `27_ep06_P1.png` — texte déformé (case 5)
```
[CADRAGE] Case 5 : le texte écrit au feutre rouge sur la feuille déchirée est déformé (« CACLE E ? »).
Écris exactement : « SALLE CACHÉE ? », en lettres manuscrites rouges, barré d'un trait.
```

### 24. Ép. 6, page documentaire — `31_ep06_doc.png` — plan KV9 / KV12 inventé
```
[CADRAGE] Simplifie le plan de KV9 et KV12 : KV9 en bleu, un axe rectiligne de l'entrée jusqu'au fond ;
KV12 en orange, à côté des corridors inférieurs de KV9 ; un cercle rouge marque le point de contact,
avec l'étiquette « Brèche (rebouchée) ». Ajoute en petit sous le plan : « Schéma simplifié — d'après
le Theban Mapping Project ». Ne change pas les textes des encadrés.
```

### 25. Ép. 7, planche 3 — `34_ep07_P3.png` — objet anachronique et fautes
```
[CADRAGE] 1) Le scribe antique écrit sur une planchette à pince avec un stylo : c'est anachronique.
Remplace par un éclat de calcaire (ostracon) tenu dans la main et un calame (roseau taillé).
2) Corrige les fautes dans les textes : « est passéé » → « est passée » ; « CARIER » → « CARRIER » ;
« trvers » → « travers ». Ne change rien d'autre.
```

### 26. Ép. 7, page documentaire — `37_ep07_doc.png` — faute
```
[CADRAGE] Corrige la faute « chaudrns » en « chaudrons ». Ne change rien d'autre.
```

### 27. Ép. 8, planche 3 — `40_ep08_P3.png` — « KEOBU » (case 2)
```
[CADRAGE] Case 2 : dans la bulle, le nom « KEOBU » est mal écrit. Remplace par « KERBU », même
couleur verte et même police.
```

### 28. Ép. 8, planche 4 — `41_ep08_P4.png` — sarcophage rectangulaire (case 7)
```
[CADRAGE] Case 7 : le sarcophage au centre de la chambre est une caisse rectangulaire. Remplace-le
par une cuve EN FORME DE MOMIE (anthropoïde), en pierre vert sombre presque noire, polie, avec des
joints de restauration visibles. Garde la lumière, les personnages et les bulles.
```

### 29. Ép. 9, planche 1 — `43_ep09_P1.png` — sarcophage rectangulaire (case 7)
```
[CADRAGE] Case 7 : au fond, dans la chambre funéraire, le sarcophage est une caisse rectangulaire.
Remplace-le par une cuve EN FORME DE MOMIE (anthropoïde), en pierre vert sombre presque noire, comme
à la planche suivante. Garde tout le reste.
```

### 30. Ép. 9, page documentaire — `47_ep09_doc.png` — portraits imaginaires
```
[CADRAGE] Dans la frise chronologique, les vignettes « 9 mars 1898 » (Victor Loret) et « 1823 »
(Belzoni) montrent des visages imaginaires de personnes réelles. Remplace-les : pour 1898, une lampe
éclairant des cercueils dans l'obscurité, sans personnage ; pour 1823, seulement le visage du couvercle
du sarcophage (EA140), sans personnage. Garde les légendes.
```

### 31. Ép. 11, page documentaire — `57_ep11_doc.png` — orientation non sourcée
```
[CADRAGE] Sur le schéma de la voûte, supprime les deux étiquettes « Tête à l'ouest (le soleil entre) »
et « Pieds à l'est (le soleil sort) ». Garde toutes les autres étiquettes.
```

### 32. Ép. 12, planche 3 — `60_ep12_P3.png` — tête du dieu (case 2) — *à vérifier d'abord*
Si le dieu dans la barque a une tête de faucon (bec), corrige :
```
[CADRAGE] Case 2 : le dieu assis dans le naos de la barque doit avoir une TÊTE DE BÉLIER (cornes
recourbées, museau de bélier), surmontée d'un disque rouge, et non une tête de faucon. Ne change
rien d'autre.
```

### 33. Ép. 12, page documentaire — `62_ep12_doc.png` — flèche « Ouest » inversée
```
[CADRAGE] Sur le plan en haut, la flèche « Ouest (≈ 290°) » pointe vers l'entrée : c'est faux.
L'entrée A est à l'EST et le fond K est à l'OUEST. Place « Est (entrée) » à gauche, près de A, et
« Ouest (fin de l'axe) » à droite, près de K, avec la flèche pointant vers K.
```

---

## C. Correction répétée sur presque toutes les planches : la numérotation

Les planches portent « PLANCHE x/7 » (l'épisode 12 : « x/4 »). Un épisode compte **4 planches** et une
page documentaire : la numérotation juste est **« PLANCHE 1/4 » à « PLANCHE 4/4 »**.

```
[CADRAGE] Dans le cartouche en haut à droite, remplace « PLANCHE N/7 » par « PLANCHE N/4 » (même
numéro N, même police, même taille). Ne change pas le sous-titre du cartouche.
```

> Cette correction concerne 44 pages et porte sur un texte placé toujours au même endroit : elle peut
> aussi être faite **automatiquement par script**, sans régénérer les images (demande-le-moi si tu
> préfères ; c'est plus sûr et plus rapide que 44 passages dans ChatGPT).

**Autre incohérence mineure** : les bulles écrivent tantôt « KERBU », tantôt « DR KERBU ». Pas besoin de
tout reprendre : à harmoniser seulement si une page est régénérée pour une autre raison.
