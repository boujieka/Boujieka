# Prompts ChatGPT — Mode d'emploi

Ces prompts sont écrits pour la **génération d'images dans ChatGPT**. Il y a **un prompt par planche** :
ChatGPT dessine la planche entière, avec sa grille de cases, en une seule image. Les prompts sont en
**français**, que ChatGPT comprend très bien, pour que tu puisses les modifier facilement.

> Les prompts « case par case » du dossier `prompts/` restent utiles pour régénérer une case ratée, ou
> pour les outils qui fonctionnent mieux image par image (Midjourney, etc.).

## 1. Méthode de travail (important pour la cohérence)

1. **Ouvre une nouvelle conversation par épisode** (ou par groupe de 3 épisodes). ChatGPT garde mieux
   les personnages quand tout se passe dans la même conversation.
2. **Colle d'abord le message n° 1 « Brief de série »** (ci-dessous). Il fixe le style et les
   personnages. Attends la réponse.
3. **Colle ensuite le message n° 2 « Fiches personnages »** et demande la planche de personnages. Garde
   cette image : si ChatGPT dérive plus tard, réimporte-la dans la conversation en disant « garde
   exactement ces personnages ».
4. **Colle ensuite les prompts de planche, un par message, dans l'ordre.**
5. **Si une case est ratée**, ne régénère pas toute la planche : demande par exemple « Refais seulement
   la case 3 : … » ou utilise l'outil de sélection de ChatGPT pour retoucher une zone.
6. **Format** : ChatGPT produit des images de format **portrait 2:3** au maximum (1024 × 1536 px). Une
   planche KDP (8,5 × 11 po) est un peu moins allongée : prévoir un léger recadrage ou une extension du
   fond, puis un agrandissement (*upscale*) pour atteindre 300 ppp à l'impression.

## 2. Message n° 1 — Brief de série (à coller en premier)

```
Nous allons créer ensemble les planches d'une bande dessinée intitulée « Les Mystères du tombeau de
Ramsès VI ». Je vais t'envoyer une planche à la fois. Pour toutes les images de cette conversation,
respecte ces règles :

FORMAT : planche de BD verticale (portrait 2:3), avec une grille de cases séparées par des gouttières
blanches fines, comme une bande dessinée franco-belge.

DEUX STYLES :
- Style A (monde d'aujourd'hui) : bande dessinée réaliste franco-belge, encrage net, couleurs peintes,
  éclairage de lampes frontales LED et de projecteurs froids dans un tombeau égyptien, poussière dans
  les faisceaux, roche calcaire, peintures murales anciennes délavées (ocre rouge, ocre jaune, bleu
  égyptien, noir sur enduit clair).
- Style B (monde mythologique, reconstitution) : style des peintures des tombes égyptiennes du Nouvel
  Empire : aplats de couleurs minérales, contours noirs, personnages de profil avec l'œil et les épaules
  de face, pas de perspective ni d'ombres. Les cases en style B ont un fin liseré doré autour du cadre.
- Style C (reconstitution historique : Égypte antique, 1922, 1949-1951) : comme le style A mais plus
  chaud, lampes à huile et torches pour l'Antiquité, ton sépia pour les scènes du XXᵉ siècle, fin liseré
  doré.

RÈGLES ABSOLUES :
- Aucun texte dans l'image : pas de bulles, pas de mots, pas de lettres, pas de titres. J'ajouterai le
  texte moi-même. Laisse un peu d'espace libre en haut des cases où des personnages parlent.
- Aucun hiéroglyphe lisible inventé : les inscriptions restent floues, lointaines ou hors champ.
- Personne ne touche les parois peintes ni les objets anciens : les mains restent à quelques
  centimètres.
- Pas de sang, pas de violence réaliste : la BD s'adresse aussi aux adolescents.
- Les personnages doivent rester identiques d'une planche à l'autre (je te donne leurs fiches).

Réponds simplement « Compris » ; j'envoie ensuite les fiches des personnages.
```

## 3. Message n° 2 — Fiches personnages (à coller en deuxième)

```
Voici les personnages récurrents. Dessine-moi d'abord une planche de présentation (« model sheet ») en
style A : les cinq personnages en pied, de face et de trois quarts, sur fond neutre, sans aucun texte.

1. Dr KERBU — archéologue africain d'environ 45 ans, peau foncée, barbe courte grisonnante, cheveux
   ras, regard calme et intense ; chemise de terrain couleur sable aux manches retroussées, pantalon
   kaki, lampe frontale, petit carnet de croquis relié de cuir, lampe à main.
2. Dr NEFERTARI HASSAN — égyptologue égyptienne d'environ 38 ans, lunettes rectangulaires, cheveux
   sombres attachés sous un foulard clair, veste de terrain beige, gants en nitrile, loupe d'épigraphiste
   pendue à un cordon autour du cou.
3. Pr ADEL MANSOUR — historien égyptien d'environ 68 ans, moustache grise, visage ridé et bienveillant,
   chapeau de lin crème, veste de lin claire, canne en bois, porte souvent un vieux livre épais annoté.
4. MAYA — ingénieure d'environ 30 ans, carré court brun foncé, lunettes à monture sombre relevées sur
   la tête, veste technique grise imperméable à nombreuses poches, tablette et scanner 3D portatif sur
   perche.
5. JULIEN MARSAC — producteur de documentaires français d'environ 50 ans, barbe de trois jours, cheveux
   grisonnants plaqués en arrière, lunettes de soleil relevées sur la tête, veste en lin coûteuse sur
   un T-shirt noir, caméra à la main ou talkie-walkie.

Accessoire récurrent : un petit boîtier gris de capteur d'humidité posé sur un trépied, avec une diode
de couleur (verte, orange ou rouge selon les épisodes).
```

> Maya et Julien Marsac n'ont pas d'apparence fixée dans la bible : ces descriptions sont des
> **propositions à valider**. Une fois la planche de personnages validée, ne plus changer.

## 4. Limites à connaître (rigueur historique)

- **ChatGPT invente les détails archéologiques.** Les parois réelles de KV9 (cases marquées
  « ⚠ Référence » dans chaque prompt) seront approximatives. Pour la version publiée, il faut soit les
  faire redessiner par un artiste d'après Piankoff & Rambova (1954) et le Theban Mapping Project, soit
  donner à ChatGPT une image de référence dont tu as les droits (« inspire-toi de la composition de
  cette image »).
- **Déclaration KDP** : les images produites par ChatGPT sont du **contenu généré par IA** et doivent
  être déclarées comme tel lors de la publication, même retouchées (bible 06 §5).
- **Droits d'auteur** : vérifier les conditions d'utilisation commerciale des images en vigueur au
  moment de la publication, et la question du droit égyptien sur les images d'antiquités (bible 06 §6).
- **Lettrage** : ajouter bulles et cartouches dans un logiciel de mise en page (Affinity Publisher,
  Canva, Clip Studio, etc.), en reprenant les textes exacts du scénario.

## 5. Index

| Fichier | Planches |
|---|---|
| `01_chatgpt_couverture_prologue_ep01-03.md` | Couverture, 4ᵉ de couverture, prologue (P1-P2), épisodes 1 à 3 |
| `02_chatgpt_ep04-06.md` | Épisodes 4 à 6 |
| `03_chatgpt_ep07-09.md` | Épisodes 7 à 9 |
| `04_chatgpt_ep10-12.md` | Épisodes 10 à 12 |
| `05_corrections_pages_fautives.md` | Prompts pour corriger les 33 pages fautives et la numérotation |
