# Prompts d'images — Guide commun

Ce dossier contient, pour **chaque planche** du Volume 1, un prompt de **mise en page** (la planche entière,
utile pour un rough) et un prompt par **case** (pour générer les images une à une). Les prompts sont en
**anglais**, la langue où les générateurs d'images sont les plus fiables ; les consignes sont en français.

## 1. Avertissements (à lire avant toute génération)

1. **Les générateurs inventent.** Ils produisent de faux hiéroglyphes, des dieux approximatifs et des
   parois qui n'existent pas. Toute case **[H]** (paroi réelle de KV9) doit être **corrigée par un
   artiste**, ou générée à partir d'une **image de référence** (image-to-image, contrôle de composition)
   tirée de sources dont les droits sont vérifiés (voir `bible/06_edition_kdp_droits.md` §6). Ne jamais
   publier une case [H] générée telle quelle.
2. **Aucun texte dans les images.** Bulles, cartouches et onomatopées sont ajoutés au lettrage. Tous les
   prompts finissent par la consigne « no text, no lettering, no speech bubbles ».
3. **Hiéroglyphes** : soit illisibles et flous (hors focale), soit recopiés exactement d'une publication
   par l'artiste. Jamais de signes « inventés lisibles » au premier plan.
4. **Déclaration KDP** : des illustrations produites par un générateur doivent être **déclarées comme
   contenu généré par IA**, même après retouches (bible 06 §5).
5. **Droits égyptiens** : l'usage commercial d'images d'antiquités pose une question juridique ouverte
   (loi 117/1983, règlement art. 146-147) : avis juridique avant la vente (bible 06 §6).
6. **Conservation** : aucun personnage ne touche les parois ou les objets. Les prompts le précisent
   (« hand held a few centimetres away from the wall, not touching »).

## 2. Les deux styles (à copier en tête de chaque prompt)

**STYLE A — Monde contemporain** (cases sans liseré doré)
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.
```

**STYLE B — Monde mythologique / reconstitution** (cases à liseré doré)
```
[STYLE B] Ancient Egyptian New Kingdom tomb painting style, flat mineral colours (red ochre, yellow
ochre, Egyptian blue, malachite green, carbon black, lime white), bold black outlines, figures in strict
profile with frontal eye and shoulders, Egyptian canon of proportions, horizontal registers, no
perspective, no shading, thin gold border around the panel.
```

**STYLE C — Reconstitution historique d'époque** (Égypte antique « réelle », expédition 1949-51, 1922)
```
[STYLE C] Same comic art as Style A but warmer palette; for antiquity: oil lamps and torchlight, raw
limestone, plain linen clothing; for 20th century scenes: sepia-toned archival look. Thin gold border.
```

**Négatif / fin de prompt (toujours)**
```
no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

## 3. Fiches personnages (descriptions fixes — à copier mot pour mot)

> Les apparences de Maya et de Julien Marsac ne sont pas fixées par la bible : celles-ci sont des
> **propositions à valider par l'auteur**. Une fois validées, ne plus les modifier.

| Code | Description anglaise à coller |
|---|---|
| `KERBU` | Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp |
| `NEFERTARI` | Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck |
| `MANSOUR` | Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book |
| `MAYA` | Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole *(à valider)* |
| `MARSAC` | Julien Marsac, French man about 50, stubble, swept-back greying hair, sunglasses pushed up on head, expensive linen jacket over a black T-shirt, handheld camera or walkie-talkie *(à valider)* |
| `SENSOR` | a small grey environmental sensor box on a tripod with a coloured status LED |

## 4. Divinités et éléments récurrents (Style B)

| Code | Description (d'après bible 03 — à vérifier sur références) |
|---|---|
| `RE_NIGHT` | ram-headed sun god standing in a shrine on a solar barque |
| `KHEPRI` | scarab beetle pushing or emerging from a red sun disk |
| `OSIRIS` | mummiform god with green skin, white atef crown with two plumes, holding crook and flail |
| `AKER` | double sphinx: two lion bodies joined back to back, one head at each end, a barque resting on its back |
| `TATENEN` | bearded man with ram horns, sun disk and two tall plumes, sometimes green skin |
| `NUT` | elongated woman arched over the scene, body covered with stars, dark blue background |
| `NUN` | bearded man with blue-green skin raising a solar barque out of the waters with his arms |
| `APOPHIS` | giant serpent, seized by ram-headed gods |
| `KV9_CORRIDOR` | long straight sloping rock-cut corridor, painted walls with registers of figures, starry astronomical ceiling, modern wooden walkway and handrails |
| `KV9_J` | vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus |

## 5. Formats

- **Planche (rough de mise en page)** : ratio 8,5 × 11 po → `--ar 17:22` (ou 8:10 selon le format retenu).
- **Bandeau pleine largeur** : `--ar 3:1` · **grande case** (½ planche) : `--ar 3:2` · **case standard** :
  `--ar 4:3` ou `1:1` · **case verticale** : `--ar 2:3`.
- La syntaxe `--ar` est celle de Midjourney ; pour d'autres outils, indiquer le ratio en clair.
- Résolution finale : 300 ppp au format d'impression (bible 06).

## 6. Index des fichiers

| Fichier | Contenu |
|---|---|
| `01_prompts_couverture_prologue.md` | Couverture, 4ᵉ de couverture, prologue (2 planches) |
| `02_prompts_ep01-03.md` | Épisodes 1 à 3 |
| `03_prompts_ep04-06.md` | Épisodes 4 à 6 |
| `04_prompts_ep07-09.md` | Épisodes 7 à 9 |
| `05_prompts_ep10-12.md` | Épisodes 10 à 12 |
