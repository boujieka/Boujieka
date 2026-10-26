# Prompts d'images — Épisodes 10 à 12

> Prompts de mise en page (une planche entière, `--ar 17:22`) et prompts case par case pour
> l'épisode 10 (*Les quatre divisions*), l'épisode 11 (*La nuit avant l'aube*) et l'épisode 12
> (*Le Soleil renaît*), plus une illustration par page documentaire. **Lire d'abord
> [`00_guide_prompts.md`](00_guide_prompts.md)** : avertissements, droits, déclaration IA KDP.

## Conventions propres à ce fichier

- Chaque prompt reprend **mot pour mot** le bloc de style, les fiches (§3-4 du guide) et le négatif
  obligatoire. Pour le **style C**, le bloc du style A est recopié juste avant, puisque le style C
  s'y réfère (« Same comic art as Style A »).
- Les fiches `MAYA` et `MARSAC` restent des **propositions à valider par l'auteur** (guide §3).
- **Aucun texte dans l'image** : les étiquettes du panorama de Maya, les points d'interrogation, les
  légendes d'encadrés, les cartouches et la « bulle dorée » de l'ép. 12 sont posés au lettrage. Les
  prompts demandent des **formes vides** (étiquettes, encadrés) à l'endroit voulu.
- **Panoramas de Maya** : toujours sur ses deux écrans portables ou sa tablette, jamais projetés sur
  les peintures.
- **Conservation** : personne ne touche les parois, ni dans le présent ni dans les reconstitutions.
- **Cases [H]** : le prompt ne sert qu'à poser la composition et la lumière ; la paroi doit être
  **redessinée par un artiste ou générée en image-to-image** à partir de la référence indiquée.
  Les figures égyptiennes des cases [H] sont décrites volontairement de façon sommaire : ne pas
  laisser le générateur « compléter » une paroi réelle.
- Ratios : bandeau `3:1` · grande case `3:2` · case standard `4:3` ou `1:1` · case verticale `2:3`.
- Statut entre crochets : repris du script ; « (implicite) » quand le script ne le note pas pour la
  case et qu'on le déduit de l'épisode (personnages et mission = [F]).

---

## Épisode 10 — Les quatre divisions

Nuit 10 sur 12 · chambre J. Rappel : lettres de sections **système Piankoff** ; aucune lettre n'est dessinée dans l'image.

## Ép. 10 · Planche 1 — Découverte archéologique (7 cases)

### Ép. 10 · Planche 1 — Mise en page : Découverte archéologique

- Ratio : --ar 17:22
- Style : rough de planche (style A ; cases à liseré doré en style B ou C, comme indiqué)
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA, SENSOR, KV9_J
- Grille :
  - Rangée 1 : case 1 (bandeau pleine largeur)
  - Rangée 2 : case 2 (petite, carrée) · case 3 (grande case, deux tiers de la largeur)
  - Rangée 3 : case 4 · case 5
  - Rangée 4 : case 6 · case 7

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[SENSOR] a small grey environmental sensor box on a tripod with a coloured status LED
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Full comic book page layout rough, portrait page, clear white gutters between panels, panels arranged in reading order left to right and top to bottom as follows: Row 1: panel 1, full-width shallow banner, wide view of the burial chamber with two portable screens being unfolded in the centre. Row 2: panel 2, small square close-up of an old open book; panel 3, wide panel taking two thirds of the row, the glowing unrolled panorama on the screens. Row 3: panel 4, zoom on a narrow painted panel on the screen; panel 5, medium shot of Kerbu, overconfident, and Mansour laughing. Row 4: panel 6, Maya holding her tablet with a document open; panel 7, the screens with a second set of dotted label shapes. Setting: the burial chamber described as KV9_J. The panorama is displayed only on the two portable screens or the tablet, never projected onto the wall paintings. Loose but readable thumbnails, consistent characters from panel to panel, empty space left in each panel for speech balloons to be added later.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 1 · Case 1 — Maya déplie les écrans

- Ratio : --ar 3:1
- Style : A
- Personnages : MAYA, SENSOR, KV9_J
- Statut : [F]
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[SENSOR] a small grey environmental sensor box on a tripod with a coloured status LED
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Wide banner shot inside the vaulted burial chamber of KV9 at night. In the centre of the room Maya unfolds two large portable screens on stands, their backs turned to the painted walls, cables neatly coiled and taped along the floor, her tablet resting on her knees as she kneels beside them. The sensor on its tripod glows near the front pillars. The painted walls stay in soft shadow in the background, slightly out of focus. The panorama is displayed only on the two portable screens or the tablet, never projected onto the wall paintings. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 3:1

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 1 · Case 2 — Le Piankoff de Mansour

- Ratio : --ar 1:1
- Style : A
- Personnages : MANSOUR, MAYA
- Statut : [H] (publication 1954, photographies de Husson) / [F] (scan par Maya)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Close-up: Professor Mansour's weathered hands hold his old thick annotated book open on a black-and-white photograph of a tomb wall; the photograph is soft and indistinct, the page not legible. Behind his shoulder, out of focus, Maya smiles and holds up her tablet. Warm headlamp light on the paper, cold LED glow from the screens. Do not reproduce any real page or photograph of the book. --ar 1:1

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 1 · Case 3 — Le panorama s'allume

- Ratio : --ar 3:2
- Style : A
- Personnages : NEFERTARI, MAYA, KERBU, MANSOUR, KV9_J
- Statut : [F] outil ; [H] découpage cité (Piankoff, via Pleuger 2020, TMP, Darnell 2018)
- ⚠ Référence obligatoire : pour l'image affichée à l'écran : Piankoff & Rambova 1954 (photographies de L. F. Husson) et photographies du Theban Mapping Project (fiche KV9) (parois de J), redessinées ; ne pas inventer de scènes
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Large panel: the two portable screens light up in the dark chamber and show the four walls of the burial chamber "unrolled" flat into one long continuous panorama, faded red and yellow ochre scenes in registers, with four blank glowing label tags placed on it (north wall, back wall split into two halves, south wall). The team stands in a half circle facing the screens, faces lit blue-white from below; Nefertari gestures towards the screen without touching it. The real painted walls remain dim behind them. Labels are empty shapes, no letters. The panorama is displayed only on the two portable screens or the tablet, never projected onto the wall paintings. --ar 3:2

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 1 · Case 4 — Le pilastre (partie E)

- Ratio : --ar 4:3
- Style : A
- Personnages : MAYA, NEFERTARI
- Statut : [H] (partie E sur le pilastre ouest, TMP / Hornung)
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) ou photographies du Theban Mapping Project (fiche KV9) : pilastre ouest de J (partie E selon Hornung)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck

Over-the-shoulder shot: Maya pinches to zoom on her tablet; on the screen a narrow vertical painted panel near the back of the chamber fills the frame, faded figures indistinct. Nefertari leans in beside her, glasses catching the screen light. Background dark. The image on screen is a redrawn copy of a real photograph, not an invention. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 1 · Case 5 — Kerbu trop sûr de lui

- Ratio : --ar 4:3
- Style : A
- Personnages : KERBU, MANSOUR
- Statut : [F] (implicite) ; [H] aucun ordre antique connu
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book

Medium shot: Kerbu, arms folded, chin up, a little too sure of himself, headlamp on; next to him Professor Mansour bursts out laughing, leaning on his cane, his old book under his arm. Cold screen light on one side, warm lamp light on the other, dim painted wall behind. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 1 · Case 6 — Le PDF de Darnell

- Ratio : --ar 4:3
- Style : A
- Personnages : MAYA, NEFERTARI
- Statut : [F] (implicite) ; [H] Roberson 2012 / Darnell 2018 : autre découpage
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck

Medium shot: Maya, seated cross-legged, opens a second document on her tablet: a scholarly PDF page shown as soft grey lines of unreadable text and a small diagram. Nefertari, standing, raises an index finger as if asking a precise question. The screen glow lights both faces; the chamber is dark behind. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 1 · Case 7 — Les étiquettes en pointillés

- Ratio : --ar 4:3
- Style : A
- Personnages : MAYA, NEFERTARI, KV9_J
- Statut : [F] outil ; correspondance Roberson/Darnell = inférence N, jamais affirmée
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

The two portable screens show the unrolled panorama of the chamber walls with the first set of solid glowing label tags and, overlaid, a second set of dotted-outline label tags offset and slightly faded, each with an empty small round slot beside it (question marks will be added at lettering). Maya, in the foreground, taps the tablet; Nefertari watches with a cautious look. No letters, no symbols drawn. The panorama is displayed only on the two portable screens or the tablet, never projected onto the wall paintings. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

## Ép. 10 · Planche 2 — Analyse : un débat à quatre voix (8 cases)

### Ép. 10 · Planche 2 — Mise en page : Un débat à quatre voix

- Ratio : --ar 17:22
- Style : rough de planche (style A ; cases à liseré doré en style B ou C, comme indiqué)
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA, KV9_J
- Grille :
  - Rangée 1 : case 1 (grande case pleine largeur)
  - Rangée 2 : case 2 · case 3 · case 4
  - Rangée 3 : case 5 · case 6
  - Rangée 4 : case 7 · case 8 (plus large, encart en bas)

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Full comic book page layout rough, portrait page, clear white gutters between panels, panels arranged in reading order left to right and top to bottom as follows: Row 1: panel 1, full-width large panel, the four researchers spread around the chamber like lawyers at a trial. Row 2: panel 2, Mansour before the north wall; panel 3, Nefertari before the south wall; panel 4, Maya looking at two inset boxes. Row 3: panel 5, Kerbu pointing his lamp at the bottom of the south wall while Nefertari counts on her fingers; panel 6, Maya turned to Mansour. Row 4: panel 7, Nefertari hands the tablet to Kerbu; panel 8, wider panel, a tangle of five coloured paths on the screen with a small inset strip of three tomb plans at the bottom. Setting: the burial chamber described as KV9_J. Leave empty boxes for the scholarly insets in panels 2, 3 and 5. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. Loose but readable thumbnails, consistent characters from panel to panel, empty space left in each panel for speech balloons to be added later.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 2 · Case 1 — Le « procès » à quatre voix

- Ratio : --ar 3:2
- Style : A
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA, KV9_J
- Statut : [F] mise en scène / [H] positions savantes (encadrés)
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) et photographies du Theban Mapping Project (fiche KV9), chambre J ; redessin selon `bible/06_edition_kdp_droits.md` §6
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Large panel, slightly high angle: the four researchers spread out across the burial chamber like lawyers in a courtroom, each one standing about a metre in front of a different wall, facing it; in the centre the two portable screens glow with the unrolled panorama. Mansour by the north wall leaning on his cane, Nefertari by the south wall, Kerbu near the back wall, Maya between the screens with her tablet. Dramatic cross-lighting from four lamps. The panorama is displayed only on the two portable screens or the tablet, never projected onto the wall paintings. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 3:2

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 2 · Case 2 — Mansour, paroi nord

- Ratio : --ar 1:1
- Style : A
- Personnages : MANSOUR
- Statut : [H] école de la paroi nord (Pleuger 2020) ; maître de Mansour [F]
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) et photographies du Theban Mapping Project (fiche KV9), chambre J ; redessin selon `bible/06_edition_kdp_droits.md` §6 (paroi nord)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book

Medium shot: Professor Mansour stands a metre in front of the painted north wall of the burial chamber, one hand on his cane, the other holding his old annotated book closed against his chest, solemn expression. The wall painting behind him is soft-focus, faded ochre registers. Empty rectangular box area left in the lower corner for an inset. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 1:1

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 2 · Case 3 — Nefertari, paroi sud

- Ratio : --ar 1:1
- Style : A
- Personnages : NEFERTARI
- Statut : [H] école de la paroi sud (Pleuger 2020)
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) et photographies du Theban Mapping Project (fiche KV9), chambre J ; redessin selon `bible/06_edition_kdp_droits.md` §6 (paroi sud)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck

Medium shot, mirror composition of the previous panel: Dr Nefertari Hassan stands a metre in front of the painted south wall, arms crossed, calm and precise, her loupe hanging on its cord. The wall painting behind her is soft-focus. Empty rectangular box area left in the lower corner for an inset. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 1:1

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 2 · Case 4 — « Hornung est dans les deux listes ? »

- Ratio : --ar 1:1
- Style : A
- Personnages : MAYA, NEFERTARI
- Statut : [H] Pleuger 2020 p. 48
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck

Close-up: Maya looks from one side to the other, eyebrows raised in surprise, glasses pushed on her head, tablet glowing in her hands; at the edge of the frame Nefertari gives a small amused shrug. Dark chamber background. --ar 1:1

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 2 · Case 5 — Kerbu et la première scène

- Ratio : --ar 4:3
- Style : A
- Personnages : KERBU, NEFERTARI, KV9_J
- Statut : [H] Pleuger 2020 p. 49-50
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) et photographies du Theban Mapping Project (fiche KV9), chambre J ; redessin selon `bible/06_edition_kdp_droits.md` §6 (paroi sud, bas)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Medium-wide shot: Kerbu, impatient, points his handheld lamp at the lower register of the painted south wall, the beam stopping a hand's width from the surface; beside him Nefertari counts on her gloved fingers, deliberately. The lit area of wall is soft and indistinct. Empty box area left at the bottom of the panel for an inset. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 2 · Case 6 — « Et la dernière ? »

- Ratio : --ar 4:3
- Style : A
- Personnages : MAYA, MANSOUR
- Statut : [H] Pleuger 2020 p. 50
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book

Two-shot: Maya turns towards Professor Mansour, tablet lowered; Mansour answers, thoughtful, lifting one finger, his old book open on his forearm, the pages soft and illegible. Warm headlamp light, cold screen glow behind. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 2 · Case 7 — « Tu cites. »

- Ratio : --ar 4:3
- Style : A
- Personnages : KERBU, NEFERTARI
- Statut : [F] (implicite) ; [H] Pleuger 2020 p. 50, 68
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck

Medium shot: Kerbu steps forward full of energy, mouth open, one hand raised as if to propose a grand idea; Nefertari cuts him off by firmly placing her tablet in his hands, its screen showing grey unreadable lines of an article. Kerbu's expression shifts from enthusiasm to concentration as he begins to read. Dark chamber behind. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 2 · Case 8 — Cinq savants, cinq chemins

- Ratio : --ar 3:2
- Style : A
- Personnages : MAYA, MANSOUR, KV9_J
- Statut : [F] outil ; [H] Pleuger 2020 p. 50, catalogue Roberson (Osireion, KV8, KV1)
- ⚠ Référence obligatoire : plans de l'Osireion d'Abydos, de KV8 (Mérenptah) et de KV1 (Ramsès VII) d'après le Theban Mapping Project (et publications pour l'Osireion) — ne pas inventer de plans
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Wide panel: on the two portable screens, Maya's 3D model of the unrolled chamber walls is crossed by five glowing paths in five distinct colours (red, blue, green, orange, violet) that loop and cross like a tangled ball of yarn. Maya stands proudly beside the screens; Mansour watches with gentle irony. At the bottom of the panel, an inset strip with three small simplified white-line silhouettes of tomb floor plans side by side, no labels. The panorama is displayed only on the two portable screens or the tablet, never projected onto the wall paintings. --ar 3:2

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

## Ép. 10 · Planche 3 — Immersion symbolique (6 cases)

Cases 1 à 5 : **image symbolique [S]**, ni scène égyptienne ni reconstitution historique. Elles ne montrent pas une projection sur les vraies parois : c'est une image mentale, dessinée en style B, à partir des registres du panorama. Les petites figures des scènes restent sommaires et indistinctes.

### Ép. 10 · Planche 3 — Mise en page : Immersion symbolique

- Ratio : --ar 17:22
- Style : rough de planche (style A ; cases à liseré doré en style B ou C, comme indiqué)
- Personnages : NEFERTARI, MAYA
- Grille :
  - Rangée 1 : case 1 · case 2 (liseré doré)
  - Rangée 2 : case 3 (pleine largeur, quatre vignettes, liseré doré)
  - Rangée 3 : case 4 · case 5 (liseré doré)
  - Rangée 4 : case 6 (pleine largeur, sans liseré)

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Full comic book page layout rough, portrait page, clear white gutters between panels, panels arranged in reading order left to right and top to bottom as follows: Row 1: panel 1, gold-bordered, a red sun disk gliding along a flat unrolled frieze of Egyptian registers; panel 2, gold-bordered, the same disk climbing the registers from bottom to top. Row 2: panel 3, full-width gold-bordered panel divided into four small sub-panels, four disks on four different routes. Row 3: panel 4, gold-bordered, four disks meeting on the back wall with identical light; panel 5, gold-bordered, a single disk floating at the centre surrounded by small figures. Row 4: panel 6, full width, no gold border, back to the present: the coloured paths on the screens and Nefertari lost in thought. Panels 1 to 5 in flat ancient Egyptian painting style with a thin gold border, panel 6 in the contemporary comic style without border. The panorama is displayed only on the two portable screens or the tablet, never projected onto the wall paintings. Loose but readable thumbnails, consistent characters from panel to panel, empty space left in each panel for speech balloons to be added later.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 3 · Case 1 — Le disque part du nord

- Ratio : --ar 4:3
- Style : B
- Personnages : aucun personnage
- Statut : [S]
- Prompt :

```
[STYLE B] Ancient Egyptian New Kingdom tomb painting style, flat mineral colours (red ochre, yellow
ochre, Egyptian blue, malachite green, carbon black, lime white), bold black outlines, figures in strict
profile with frontal eye and shoulders, Egyptian canon of proportions, horizontal registers, no
perspective, no shading, thin gold border around the panel.

A long flat frieze of Egyptian painted registers, like the north wall of a burial chamber unrolled flat, on a dark background; a glowing red sun disk glides horizontally along the middle register, leaving a faint trail of light. Symbolic image, not an ancient scene and not a historical reconstruction; small figures in the registers are generic, simplified and indistinct, not copies of specific scenes. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 3 · Case 2 — … ou du sud, de bas en haut

- Ratio : --ar 4:3
- Style : B
- Personnages : aucun personnage
- Statut : [S] (lecture de bas en haut de Cauville = [H], sa mise en image = [S])
- Prompt :

```
[STYLE B] Ancient Egyptian New Kingdom tomb painting style, flat mineral colours (red ochre, yellow
ochre, Egyptian blue, malachite green, carbon black, lime white), bold black outlines, figures in strict
profile with frontal eye and shoulders, Egyptian canon of proportions, horizontal registers, no
perspective, no shading, thin gold border around the panel.

The same flat frieze of painted registers, seen as the opposite wall; the red sun disk starts at the lowest register and climbs upward register after register, its light trail rising. Do not depict any specific scholarly route. Symbolic image, not an ancient scene and not a historical reconstruction; small figures in the registers are generic, simplified and indistinct, not copies of specific scenes. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 3 · Case 3 — Quatre disques, quatre trajets

- Ratio : --ar 3:2
- Style : B
- Personnages : aucun personnage
- Statut : [S]
- Prompt :

```
[STYLE B] Ancient Egyptian New Kingdom tomb painting style, flat mineral colours (red ochre, yellow
ochre, Egyptian blue, malachite green, carbon black, lime white), bold black outlines, figures in strict
profile with frontal eye and shoulders, Egyptian canon of proportions, horizontal registers, no
perspective, no shading, thin gold border around the panel.

One panel divided into four equal small sub-panels in a 2 by 2 grid by thin gold lines; in each sub-panel the same red sun disk follows a different route across flat painted registers: left to right, right to left, bottom to top, top to bottom, all at the same moment. Symbolic image, not an ancient scene and not a historical reconstruction; small figures in the registers are generic, simplified and indistinct, not copies of specific scenes. --ar 3:2

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 3 · Case 4 — La même lumière

- Ratio : --ar 4:3
- Style : B
- Personnages : aucun personnage
- Statut : [S] (idée de Kerbu)
- Prompt :

```
[STYLE B] Ancient Egyptian New Kingdom tomb painting style, flat mineral colours (red ochre, yellow
ochre, Egyptian blue, malachite green, carbon black, lime white), bold black outlines, figures in strict
profile with frontal eye and shoulders, Egyptian canon of proportions, horizontal registers, no
perspective, no shading, thin gold border around the panel.

The four red sun disks converge on the painted back wall from four directions and meet; their light is rigorously identical: the same red, the same halo, the same size, perfectly symmetrical composition. Symbolic image, not an ancient scene and not a historical reconstruction; small figures in the registers are generic, simplified and indistinct, not copies of specific scenes. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 3 · Case 5 — Un disque sans début

- Ratio : --ar 1:1
- Style : B
- Personnages : aucun personnage
- Statut : [S]
- Prompt :

```
[STYLE B] Ancient Egyptian New Kingdom tomb painting style, flat mineral colours (red ochre, yellow
ochre, Egyptian blue, malachite green, carbon black, lime white), bold black outlines, figures in strict
profile with frontal eye and shoulders, Egyptian canon of proportions, horizontal registers, no
perspective, no shading, thin gold border around the panel.

A single red sun disk floats at the centre of the unrolled chamber, surrounded in a loose circle by the small painted figures of the scenes, all facing it; no arrows, no direction, no starting point, calm and balanced composition on a dark background. Symbolic image, not an ancient scene and not a historical reconstruction; small figures in the registers are generic, simplified and indistinct, not copies of specific scenes. --ar 1:1

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 3 · Case 6 — Retour au présent : Nefertari songeuse

- Ratio : --ar 3:1
- Style : A
- Personnages : NEFERTARI, MAYA, KV9_J
- Statut : [S] (question) ; [F] scène
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Back to the present, no gold border: the LEDs are dimmed; on the two portable screens the coloured reading paths of Maya's model glow in the dark. Nefertari, for the first time, is pensive, chin resting on her hand, gaze lost on the screens; at the side of the frame Maya looks at her with a mischievous grin. Then a soft half-smile on Nefertari's face. The panorama is displayed only on the two portable screens or the tablet, never projected onto the wall paintings. --ar 3:1

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

## Ép. 10 · Planche 4 — Révélation et suspense (7 cases)

### Ép. 10 · Planche 4 — Mise en page : Révélation et suspense

- Ratio : --ar 17:22
- Style : rough de planche (style A ; cases à liseré doré en style B ou C, comme indiqué)
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA, MARSAC, SENSOR, KV9_J
- Grille :
  - Rangée 1 : case 1 · case 2
  - Rangée 2 : case 3 · case 4
  - Rangée 3 : case 5 · case 6
  - Rangée 4 : case 7 (bandeau final, liseré doré fugitif)

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[MARSAC] Julien Marsac, French man about 50, stubble, swept-back greying hair, sunglasses pushed up on head, expensive linen jacket over a black T-shirt, handheld camera or walkie-talkie
[SENSOR] a small grey environmental sensor box on a tripod with a coloured status LED
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Full comic book page layout rough, portrait page, clear white gutters between panels, panels arranged in reading order left to right and top to bottom as follows: Row 1: panel 1, Marsac entering, amazed by the glowing screens; panel 2, Maya shrugging while Mansour rests his hand on his old book. Row 2: panel 3, Nefertari facing Marsac firmly; panel 4, Marsac annoyed, Kerbu gently stepping between them. Row 3: panel 5, Marsac staring at the tangle of five coloured paths; panel 6, Kerbu packing up, his lamp beam falling on a painted scene of the north wall, the sensor blinking. Row 4: panel 7, full-width banner, close-up of the painted barque towed by birds, a flash of thin gold border. Setting: the burial chamber described as KV9_J. The panorama is displayed only on the two portable screens or the tablet, never projected onto the wall paintings. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. Loose but readable thumbnails, consistent characters from panel to panel, empty space left in each panel for speech balloons to be added later.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 4 · Case 1 — Marsac entre

- Ratio : --ar 4:3
- Style : A
- Personnages : MARSAC, MAYA, KV9_J
- Statut : [F]
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MARSAC] Julien Marsac, French man about 50, stubble, swept-back greying hair, sunglasses pushed up on head, expensive linen jacket over a black T-shirt, handheld camera or walkie-talkie
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Julien Marsac steps into the burial chamber, sunglasses pushed up on his head, walkie-talkie in hand, arms spread wide in wonder at the glowing panorama on the two portable screens; their blue light washes over his face. Maya, seated by the screens, glances up at him. The panorama is displayed only on the two portable screens or the tablet, never projected onto the wall paintings. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 4 · Case 2 — Maya hausse les épaules

- Ratio : --ar 4:3
- Style : A
- Personnages : MAYA, MANSOUR
- Statut : [F] (implicite)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book

Two-shot: Maya shrugs with a casual, slightly ironic air, tablet in one hand; Professor Mansour, silent, rests his hand flat on the closed cover of his old thick book lying on his knees, a protective gesture. Dim chamber, screen glow. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 4 · Case 3 — Nefertari, ferme

- Ratio : --ar 1:1
- Style : A
- Personnages : NEFERTARI, MARSAC
- Statut : [F] (implicite)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MARSAC] Julien Marsac, French man about 50, stubble, swept-back greying hair, sunglasses pushed up on head, expensive linen jacket over a black T-shirt, handheld camera or walkie-talkie

Medium close-up: Nefertari stands squarely facing Marsac, firm and composed, looking him straight in the eye; Marsac seen from behind his shoulder in the foreground, out of focus. Cold side light from the screens. --ar 1:1

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 4 · Case 4 — Kerbu s'interpose

- Ratio : --ar 4:3
- Style : A
- Personnages : MARSAC, NEFERTARI, KERBU
- Statut : [F] (implicite) ; [H] débat réel et non résolu
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MARSAC] Julien Marsac, French man about 50, stubble, swept-back greying hair, sunglasses pushed up on head, expensive linen jacket over a black T-shirt, handheld camera or walkie-talkie
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp

Three-shot: Marsac, annoyed, hands on hips; Nefertari calm and unyielding; Kerbu steps gently between them with an open, conciliating gesture of both hands, a warm smile. Headlamp light, dark painted walls behind. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 4 · Case 5 — Marsac regarde les cinq chemins

- Ratio : --ar 4:3
- Style : A
- Personnages : MARSAC, MAYA
- Statut : [F] (étape de l'arc de Marsac)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MARSAC] Julien Marsac, French man about 50, stubble, swept-back greying hair, sunglasses pushed up on head, expensive linen jacket over a black T-shirt, handheld camera or walkie-talkie
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Marsac stands silently in front of the two portable screens, seen in three-quarter back view, studying the five coloured reading paths crossing on the unrolled panorama, the coloured light reflecting on his face; a long moment of reflection. In the corner Maya smiles. The panorama is displayed only on the two portable screens or the tablet, never projected onto the wall paintings. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 4 · Case 6 — Le bip, et la scène des oiseaux

- Ratio : --ar 4:3
- Style : A
- Personnages : KERBU, NEFERTARI, SENSOR, KV9_J
- Statut : [H] scène A12 (système Piankoff) = Darnell §6.38-39 ; [F] le bip
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) : scène A12 de la paroi nord de J (barque halée par les oiseaux-ba, tertre, œil qui pleure, quatre morceaux de chair). L'apparence des oiseaux-ba n'est pas décrite dans la bible : **recopier**, image-to-image ou redessin
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[SENSOR] a small grey environmental sensor box on a tripod with a coloured status LED
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

In the foreground the sensor's status LED blinks red. Kerbu, packing his bag, has let his handheld lamp swing: its beam falls by chance on a painted scene of the north wall, a hand's width from the surface. In the beam: a barque towed on ropes by a row of figures above a mound; the figures and the small motifs around the mound (a weeping eye, four pieces of flesh) are left as soft, simplified placeholder shapes to be redrawn exactly from the reference. Nefertari turns towards the wall, intrigued. Do not invent the appearance of the towing birds. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Planche 4 · Case 7 — Gros plan : la barque halée (bandeau final)

- Ratio : --ar 3:1
- Style : B
- Personnages : aucun personnage
- Statut : [H] scène A12 (système Piankoff) ; liseré doré fugitif
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) (scène A12, paroi nord de J) ; ne rien composer
- Prompt :

```
[STYLE B] Ancient Egyptian New Kingdom tomb painting style, flat mineral colours (red ochre, yellow
ochre, Egyptian blue, malachite green, carbon black, lime white), bold black outlines, figures in strict
profile with frontal eye and shoulders, Egyptian canon of proportions, horizontal registers, no
perspective, no shading, thin gold border around the panel.

Close-up banner on a painted tomb scene: a barque pulled forward on long ropes by a line of towing figures, moving left to right across the register; the scene is a faithful copy of a real wall painting, slightly faded, with the light of a single lamp falling on it, and a thin gold border shimmering around the panel for an instant. Towing figures kept as simplified placeholders to be replaced by an exact redraw from the reference. --ar 3:1

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 10 · Page documentaire — Illustration : deux systèmes de lettres pour la chambre J

- Ratio : --ar 3:2
- Style : A (adapté en schéma documentaire, sans liseré)
- Personnages : aucun personnage
- Statut : [H] (découpages Piankoff / Roberson-Darnell) ; correspondance N « à confirmer »
- ⚠ Référence obligatoire : plan de la chambre J du Theban Mapping Project (proportions, piliers, pilastre ouest) ; les lettres A-E, la mention « correspondance à confirmer » et les noms des savants sont posés à la mise en page
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Clean documentary infographic on a pale parchment background: two identical simplified top-down floor plans of a rectangular rock-cut burial chamber with four pillars at the front and a narrow pilaster at the back, placed side by side. On the left plan, the walls are traced with solid coloured lines in four segments (north wall, back wall split in two halves, south wall) plus a small mark on the back pilaster. On the right plan, the same walls traced with dotted lines in a different colour. Below the two plans, two long coloured arrows side by side, one ochre, one blue. Empty label areas next to each segment and under each arrow for typesetting. Flat vector style, thin lines, no letters, no names drawn. --ar 3:2

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

## Épisode 11 — La nuit avant l'aube

Nuit 11 sur 12 · voûte et parois de J, corridor B, entrée A.

## Ép. 11 · Planche 1 — Découverte archéologique (7 cases)

### Ép. 11 · Planche 1 — Mise en page : Découverte archéologique

- Ratio : --ar 17:22
- Style : rough de planche (style A ; cases à liseré doré en style B ou C, comme indiqué)
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA, SENSOR, KV9_J
- Grille :
  - Rangée 1 : case 1 (bandeau)
  - Rangée 2 : case 2 · case 3
  - Rangée 3 : case 4 (grande case, demi-planche)
  - Rangée 4 : case 5 · case 6 · case 7

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[SENSOR] a small grey environmental sensor box on a tripod with a coloured status LED
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Full comic book page layout rough, portrait page, clear white gutters between panels, panels arranged in reading order left to right and top to bottom as follows: Row 1: panel 1, full-width banner, the team entering the vaulted burial chamber in single file around the restored sarcophagus. Row 2: panel 2, Maya setting the sensor on its tripod near the front pillars; panel 3, Kerbu lying on his back on a mat, lamp pointed at the ceiling, the others lying down one by one. Row 3: panel 4, half-page large panel, low-angle view of the vaulted ceiling with two elongated sky goddesses back to back, four lamp beams crossing. Row 4: panel 5, Maya in profile, lamp on the starry body of the goddess; panel 6, Nefertari's beam moving to one end of the goddess's body; panel 7, close-up of Kerbu, eyes wide open. Setting: the burial chamber described as KV9_J. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. Loose but readable thumbnails, consistent characters from panel to panel, empty space left in each panel for speech balloons to be added later.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 1 · Case 1 — L'équipe entre dans J

- Ratio : --ar 3:1
- Style : A
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA, KV9_J
- Statut : [H] décor / [F] scène
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) et photographies du Theban Mapping Project (fiche KV9), chambre J ; redessin selon `bible/06_edition_kdp_droits.md` §6 : chambre voûtée et sarcophage restauré tel que présenté dans J ; ne pas inventer l'état des parois ni la position des fragments
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Wide banner: the vaulted burial chamber of KV9 at night; in the centre the restored dark green anthropoid sarcophagus; the four researchers enter in single file from the front, lamps held low, moving quietly and carefully on the walkway, respectful silence. Painted walls and vault in soft shadow. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 3:1

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 1 · Case 2 — Le capteur près des piliers

- Ratio : --ar 4:3
- Style : A
- Personnages : MAYA, MANSOUR, SENSOR
- Statut : [F] (courbe et valeurs fictives)
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) et photographies du Theban Mapping Project (fiche KV9), chambre J ; redessin selon `bible/06_edition_kdp_droits.md` §6 (piliers de l'avant)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[SENSOR] a small grey environmental sensor box on a tripod with a coloured status LED

Medium shot: Maya sets the sensor on its tripod near the front pillars of the chamber; on a small handheld screen beside it, a simple line graph curves upward, no numbers, no units. Mansour, behind her, looks up towards the vault and takes a slow breath. The pillar keeps its distance from the tripod. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 1 · Case 3 — On regarde en haut

- Ratio : --ar 4:3
- Style : A
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA
- Statut : [F]
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Kerbu unrolls a simple mat on the floor of the chamber and lies on his back, headlamp and handheld lamp pointed at the ceiling; behind him the others follow one by one, Maya sitting down, Nefertari lying back, Mansour lowering himself carefully with his cane. Calm, almost playful mood. Painted walls dim around them. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 1 · Case 4 — La voûte : deux Nout dos à dos

- Ratio : --ar 3:2
- Style : A
- Personnages : NUT, KV9_J
- Statut : [H]
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) ou photographies du Theban Mapping Project (fiche KV9) : voûte de J (deux Nout dos à dos, Livres du Jour et de la Nuit) ; image-to-image ou redessin obligatoire
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[NUT] elongated woman arched over the scene, body covered with stars, dark blue background
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Large panel, extreme low-angle view from the floor straight up at the vaulted ceiling of the burial chamber: two very elongated painted sky goddesses lie back to back along the whole length of the vault, their bodies spanning it; between and along their bodies run long registers of small painted figures (Books of the Day and of the Night), kept soft and indistinct. Four lamp beams from below cross on the ceiling, revealing patches of deep blue paint and stars, dust floating in the light. Composition to be copied from the reference photographs, do not invent the number or arrangement of figures. --ar 3:2

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 1 · Case 5 — Maya et le ventre étoilé

- Ratio : --ar 4:3
- Style : A
- Personnages : MAYA, NUT
- Statut : [H] (voûte de J ; Nout au plafond de D, ép. 2)
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) ou photographies du Theban Mapping Project (fiche KV9) : voûte de J
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[NUT] elongated woman arched over the scene, body covered with stars, dark blue background

Maya lying on her back, seen in profile in the foreground, her handheld lamp pointed upward; above her, out of reach, the beam lights a section of the starry painted body of the sky goddess on the vault, deep blue with small yellow stars. Wondering expression. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 1 · Case 6 — La douzième heure

- Ratio : --ar 4:3
- Style : A
- Personnages : NEFERTARI, NUT
- Statut : [H] (12ᵉ heure : le soleil sort de Nout)
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) ou photographies du Theban Mapping Project (fiche KV9) : endroit de la voûte de J où le soleil sort du corps de Nout (12ᵉ heure) ; ne pas inventer la scène
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[NUT] elongated woman arched over the scene, body covered with stars, dark blue background

Nefertari, lying on her mat, slowly moves her lamp beam along the vault towards the far end of one of the elongated bodies of the sky goddess; the beam stops on that end, where the painted scene is left soft and indistinct, to be drawn exactly from the reference. Focused, almost reverent expression. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 1 · Case 7 — Kerbu, yeux grands ouverts

- Ratio : --ar 1:1
- Style : A
- Personnages : KERBU
- Statut : [S] (idée de Kerbu) ; [N] raison de l'absence de la 12ᵉ heure
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp

Close-up of Kerbu lying on his back, eyes wide open, lit from his own lamp held above his chest; the lamp trembles slightly, its beam blurred; a mix of excitement and doubt on his face. Dark background, faint stars of the painted vault reflected in his eyes. --ar 1:1

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

## Ép. 11 · Planche 2 — Analyse d'une inscription : la crise (8 cases)

### Ép. 11 · Planche 2 — Mise en page : La crise

- Ratio : --ar 17:22
- Style : rough de planche (style A ; cases à liseré doré en style B ou C, comme indiqué)
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA, KV9_J
- Grille :
  - Rangée 1 : case 1 · case 2
  - Rangée 2 : case 3 · case 4
  - Rangée 3 : case 5 · case 6
  - Rangée 4 : case 7 · case 8

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Full comic book page layout rough, portrait page, clear white gutters between panels, panels arranged in reading order left to right and top to bottom as follows: Row 1: panel 1, Kerbu springing to his feet and sweeping the walls with his lamp; panel 2, Kerbu stopping before a painted figure while Nefertari reads the legend with her loupe. Row 2: panel 3, Kerbu exalted, arms spread, pointing at wall and vault; panel 4, tight close-up of Nefertari's hand counting on her fingers. Row 3: panel 5, Kerbu destabilised, Mansour sitting on his mat opening his annotated book; panel 6, Maya turning her tablet towards them with the unfolded 3D model. Row 4: panel 7, Nefertari crouching beside Kerbu, gentle; panel 8, Kerbu alone sitting against a pillar, lamp on the floor pointing into emptiness. Setting: the burial chamber described as KV9_J. The panorama is displayed only on the two portable screens or the tablet, never projected onto the wall paintings. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. Loose but readable thumbnails, consistent characters from panel to panel, empty space left in each panel for speech balloons to be added later.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 2 · Case 1 — « Tout va par deux ! »

- Ratio : --ar 4:3
- Style : A
- Personnages : KERBU, KV9_J
- Statut : [F] ; éléments cités [H] (Darnell §6.1, 6.26, 6.11, 6.40) ; « tout se tient » [S]
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) et photographies du Theban Mapping Project (fiche KV9), chambre J ; redessin selon `bible/06_edition_kdp_droits.md` §6 (parois du Livre de la Terre ; garder flou de mouvement)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Dynamic shot: Kerbu springs to his feet, sweeping the painted walls of the burial chamber with his lamp in a wide arc; in the moving beam, faded ochre scenes of the Book of the Earth flash by, blurred by motion and impossible to read in detail. Excited, almost feverish expression. Motion lines. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 2 · Case 2 — La « Mystérieuse »

- Ratio : --ar 4:3
- Style : A
- Personnages : KERBU, NEFERTARI, KV9_J
- Statut : [H] (Darnell §6.2) ; emplacement exact N
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) : scène de la « Mystérieuse » (Shetayt) dans J — emplacement à relever avant dessin ; hiéroglyphes de la légende à copier, jamais inventés
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Kerbu has stopped in front of one painted figure on the wall of the burial chamber; Nefertari approaches and leans in with her epigraphy loupe held a few centimetres from the surface, reading the column of signs beside the figure. The figure and its legend are soft-focus placeholders, to be copied exactly from the reference; no invented hieroglyphs. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 2 · Case 3 — La « grande théorie » de Kerbu

- Ratio : --ar 4:3
- Style : A
- Personnages : KERBU, KV9_J
- Statut : [F]/[S]
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Kerbu, exalted, arms spread wide, one hand pointing at the painted wall, the other up at the vaulted ceiling with its starry goddess, eyes shining, as if he had found the key to everything. Low angle to emphasise his excitement; lamp light flaring. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 2 · Case 4 — Un, deux, trois

- Ratio : --ar 1:1
- Style : A
- Personnages : NEFERTARI
- Statut : [H] sources citées ; lecture de bas en haut = position débattue (C)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck

Tight close-up on Nefertari's gloved hand counting on her fingers: one, two, three; her calm face slightly out of focus behind, glasses catching the lamp light. Simple, quiet composition. --ar 1:1

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 2 · Case 5 — Mansour ouvre son Piankoff

- Ratio : --ar 4:3
- Style : A
- Personnages : KERBU, MANSOUR
- Statut : [F] (annotations) ; [H] Pleuger 2020 p. 48-50
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book

Kerbu, destabilised, hands open in a helpless gesture; Mansour has sat down on his mat and opens his old annotated copy of the 1954 publication, its margins crowded with handwritten notes shown as soft illegible scribbles; no readable page, no reproduced photograph. Warm lamp light on the book. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 2 · Case 6 — Le modèle sait où, pas dans quel ordre

- Ratio : --ar 4:3
- Style : A
- Personnages : MAYA, KERBU, MANSOUR
- Statut : [F] (capacités du modèle)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book

Maya turns her tablet towards the others; on its screen her 3D model unfolds the four walls of the burial chamber flat, like an opened box, faded painted registers in miniature, no labels. Kerbu and Mansour lean towards the screen. The panorama is displayed only on the two portable screens or the tablet, never projected onto the wall paintings. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 2 · Case 7 — « Un livre qui n'a peut-être jamais eu de porte »

- Ratio : --ar 4:3
- Style : A
- Personnages : NEFERTARI, KERBU
- Statut : [H] Darnell 2018 p. 457 ; image de Nefertari [S]
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp

Nefertari crouches beside Kerbu, who sits on the floor; her expression has softened, almost tender, one hand resting on her knee; Kerbu listens, head lowered. Soft warm lamp light, intimate framing. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 2 · Case 8 — Kerbu seul contre un pilier

- Ratio : --ar 2:3
- Style : A
- Personnages : KERBU, KV9_J
- Statut : [F] (sommet de l'arc de Kerbu)
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) et photographies du Theban Mapping Project (fiche KV9), chambre J ; redessin selon `bible/06_edition_kdp_droits.md` §6 (piliers de l'avant)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Kerbu alone in the frame, seated on the floor with his back against one of the front pillars of the burial chamber, keeping his shoulders a few centimetres off the painted surface, knees drawn up; his lamp lies on the floor, its beam pointing into the empty darkness. Silence, melancholy, lots of negative space. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 2:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

## Ép. 11 · Planche 3 — Immersion dans l'Égypte antique (7 cases)

Reconstitution d'époque romaine (style C, liseré doré). Les deux voyageurs sont **fictifs**. Les graffiti ne sont **ni datés ni localisés** : lettres gravées toujours illisibles, aucun grec lisible inventé.

### Ép. 11 · Planche 3 — Mise en page : Immersion dans l'Égypte antique

- Ratio : --ar 17:22
- Style : rough de planche (style A ; cases à liseré doré en style B ou C, comme indiqué)
- Personnages : VOYAGEUR_1 (fictif), VOYAGEUR_2 (fictif), KERBU, NEFERTARI, MARSAC (off)
- Grille :
  - Rangée 1 : case 1 (case charnière, pleine largeur)
  - Rangée 2 : case 2 (grande case)
  - Rangée 3 : case 3 · case 4 · case 5
  - Rangée 4 : case 6 · case 7 (sans liseré)

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck

Full comic book page layout rough, portrait page, clear white gutters between panels, panels arranged in reading order left to right and top to bottom as follows: Row 1: panel 1, full-width hinge panel split in two: left half the engraved graffiti under cold LED light, right half the same wall under orange flame light with a gold border appearing. Row 2: panel 2, full-width large panel, two Roman-era travellers with torches in the painted corridor. Row 3: panel 3, traveller 1 holding his torch near a graffito and smiling; panel 4, silent panel, traveller 1 looking up at a painted god; panel 5, traveller 1 with a metal point poised near the wall. Row 4: panel 6, traveller 2 laughing softly; panel 7, back to the present, same framing, LEDs instead of torches, no gold border. Panels 1 to 6 in the warm historical reconstruction style with thin gold border (Roman-era travellers in plain clothing, torchlight), panel 7 contemporary. All engraved graffiti rendered as illegible scratched marks. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. Loose but readable thumbnails, consistent characters from panel to panel, empty space left in each panel for speech balloons to be added later.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 3 · Case 1 — Case charnière : LED puis flamme

- Ratio : --ar 3:1
- Style : C
- Personnages : aucun personnage
- Statut : [H] graffiti du corridor B (27 av. J.-C. - 191 apr. J.-C., TMP) ; emplacement des graffiti cités N
- ⚠ Référence obligatoire : photographies du Theban Mapping Project (fiche KV9) : corridor B et ses graffiti ; lettres à copier d'après photographie, jamais inventées
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.
[STYLE C] Same comic art as Style A but warmer palette; for antiquity: oil lamps and torchlight, raw
limestone, plain linen clothing; for 20th century scenes: sepia-toned archival look. Thin gold border.

Hinge banner split vertically in two halves: on the left, a cold white LED beam rakes across letters scratched into the painted plaster of a tomb corridor wall, illegible and worn; on the right, the very same stretch of wall lit by a warm orange flickering torch flame, the paint glowing richer, and a thin gold border appears around this half. Scratched letters are illegible marks, no readable Greek or Latin, no invented text. --ar 3:1

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 3 · Case 2 — Deux voyageurs portant une torche

- Ratio : --ar 3:2
- Style : C
- Personnages : VOYAGEUR_1, VOYAGEUR_2 : voyageurs fictifs d'époque romaine, sans fiche dans le guide ; apparence proposée dans le prompt, à valider
- Statut : [F] personnages ; [H] éclairage à la torche, « tombeau de Memnon »
- ⚠ Référence obligatoire : photographies du Theban Mapping Project (fiche KV9) (corridor B, parois et graffiti) ; costumes et torches d'après références d'époque romaine en Égypte
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.
[STYLE C] Same comic art as Style A but warmer palette; for antiquity: oil lamps and torchlight, raw
limestone, plain linen clothing; for 20th century scenes: sepia-toned archival look. Thin gold border.

Two fictional travellers of the Roman period in Egypt: traveller 1, a lean man about 40 in a plain undyed linen tunic and a simple cloak, sandals; traveller 2, a stockier man about 50, short beard, plain linen tunic and cloak; costumes and torches to be copied from Roman-period Egyptian references, not invented. Large panel: the two travellers walk down the long sloping painted corridor of the tomb, each holding a torch at a safe distance from the walls; the painted registers glow and shimmer in the flames; the walls already carry dozens of small scratched graffiti, illegible. Smoke rising to the ceiling, deep shadows ahead. No modern walkway or handrails in this ancient scene. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 3:2

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 3 · Case 3 — « Je ne sais pas lire les hiéroglyphes ! »

- Ratio : --ar 4:3
- Style : C
- Personnages : VOYAGEUR_1, VOYAGEUR_2 : voyageurs fictifs d'époque romaine, sans fiche dans le guide ; apparence proposée dans le prompt, à valider
- Statut : [H] graffito (traduction de presse, SIP) ; personnage [F]
- ⚠ Référence obligatoire : photographies du Theban Mapping Project (fiche KV9) : corridor B et ses graffiti ; lettres à copier d'après photographie, jamais inventées
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.
[STYLE C] Same comic art as Style A but warmer palette; for antiquity: oil lamps and torchlight, raw
limestone, plain linen clothing; for 20th century scenes: sepia-toned archival look. Thin gold border.

Two fictional travellers of the Roman period in Egypt: traveller 1, a lean man about 40 in a plain undyed linen tunic and a simple cloak, sandals; traveller 2, a stockier man about 50, short beard, plain linen tunic and cloak; costumes and torches to be copied from Roman-period Egyptian references, not invented. Medium shot: traveller 1 brings his torch close to (but not touching) a small scratched graffito on the painted wall and reads it aloud with an amused smile; traveller 2 slightly behind. The graffito is an illegible cluster of scratched marks. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 3 · Case 4 — Case muette : le dieu peint

- Ratio : --ar 4:3
- Style : C
- Personnages : VOYAGEUR_1, VOYAGEUR_2 : voyageurs fictifs d'époque romaine, sans fiche dans le guide ; apparence proposée dans le prompt, à valider
- Statut : [F] scène ; divinité [H] à copier (corridor B : Livre des Portes au sud ou Livre des Cavernes au nord)
- ⚠ Référence obligatoire : photographies du Theban Mapping Project (fiche KV9) ou Piankoff & Rambova 1954 (photographies de L. F. Husson) : une divinité réelle du corridor B (Livre des Portes, paroi sud, ou Livre des Cavernes, paroi nord) ; ne pas composer de figure
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.
[STYLE C] Same comic art as Style A but warmer palette; for antiquity: oil lamps and torchlight, raw
limestone, plain linen clothing; for 20th century scenes: sepia-toned archival look. Thin gold border.

Two fictional travellers of the Roman period in Egypt: traveller 1, a lean man about 40 in a plain undyed linen tunic and a simple cloak, sandals; traveller 2, a stockier man about 50, short beard, plain linen tunic and cloak; costumes and torches to be copied from Roman-period Egyptian references, not invented. Silent panel: traveller 1 lifts his eyes from the graffito towards a large painted god right beside it on the wall; the torch flame makes the mineral colours vibrate; he is humbled, unable to read the signs either. The god is a placeholder silhouette to be replaced by an exact copy of a real figure of the corridor; no composed figure, no readable hieroglyphs. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 3 · Case 5 — La réponse gravée

- Ratio : --ar 4:3
- Style : C
- Personnages : VOYAGEUR_1, VOYAGEUR_2 : voyageurs fictifs d'époque romaine, sans fiche dans le guide ; apparence proposée dans le prompt, à valider
- Statut : [H] texte de la réponse (presse, SIP) ; graveur et moment [F]
- ⚠ Référence obligatoire : photographies du Theban Mapping Project (fiche KV9) : corridor B et ses graffiti ; lettres à copier d'après photographie, jamais inventées
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.
[STYLE C] Same comic art as Style A but warmer palette; for antiquity: oil lamps and torchlight, raw
limestone, plain linen clothing; for 20th century scenes: sepia-toned archival look. Thin gold border.

Two fictional travellers of the Roman period in Egypt: traveller 1, a lean man about 40 in a plain undyed linen tunic and a simple cloak, sandals; traveller 2, a stockier man about 50, short beard, plain linen tunic and cloak; costumes and torches to be copied from Roman-period Egyptian references, not invented. Close medium shot: traveller 1 holds a thin metal point raised in front of the wall, just below the first graffito, the tip poised a centimetre from the surface at the instant before engraving, concentration on his face, torch held high by traveller 2 at a safe distance. Above the gesture leave an empty area shaped like a small tablet for the engraved text to be lettered later. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 3 · Case 6 — Le voyageur 2 rit doucement

- Ratio : --ar 4:3
- Style : C
- Personnages : VOYAGEUR_1, VOYAGEUR_2 : voyageurs fictifs d'époque romaine, sans fiche dans le guide ; apparence proposée dans le prompt, à valider
- Statut : [F] (écho au graffito « J'ai admiré ! », sans l'attribuer)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.
[STYLE C] Same comic art as Style A but warmer palette; for antiquity: oil lamps and torchlight, raw
limestone, plain linen clothing; for 20th century scenes: sepia-toned archival look. Thin gold border.

Two fictional travellers of the Roman period in Egypt: traveller 1, a lean man about 40 in a plain undyed linen tunic and a simple cloak, sandals; traveller 2, a stockier man about 50, short beard, plain linen tunic and cloak; costumes and torches to be copied from Roman-period Egyptian references, not invented. Two-shot: traveller 2 laughs softly, shoulders relaxed, torchlight on his bearded face; traveller 1, looking back at the painted walls with quiet admiration. Warm, friendly mood, painted corridor glowing behind them. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 3 · Case 7 — Retour au présent, même cadrage

- Ratio : --ar 4:3
- Style : A
- Personnages : KERBU, NEFERTARI, KV9_CORRIDOR
- Statut : [F]
- ⚠ Référence obligatoire : photographies du Theban Mapping Project (fiche KV9) (corridor B, état actuel)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[KV9_CORRIDOR] long straight sloping rock-cut corridor, painted walls with registers of figures, starry astronomical ceiling, modern wooden walkway and handrails

Back to the present, exactly the same framing as the previous panel, no gold border: modern LED lamps instead of torches, the modern wooden walkway and handrails, the graffiti on the wall faded and worn by the centuries; Kerbu and Nefertari stand where the travellers stood, turning their heads towards the far entrance, where a distant light shines. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

## Ép. 11 · Planche 4 — Révélation et suspense (8 cases)

Le relief de Dendérah n'apparaît **que sur l'écran de la tablette de Marsac**, redessiné d'après une photographie de référence. Aucune image d'« astronautes » n'est inventée.

### Ép. 11 · Planche 4 — Mise en page : Révélation et suspense

- Ratio : --ar 17:22
- Style : rough de planche (style A ; cases à liseré doré en style B ou C, comme indiqué)
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA, MARSAC, SENSOR
- Grille :
  - Rangée 1 : case 1 · case 2
  - Rangée 2 : case 3 · case 4
  - Rangée 3 : case 5 · case 6 · case 7
  - Rangée 4 : case 8 (bandeau final)

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[MARSAC] Julien Marsac, French man about 50, stubble, swept-back greying hair, sunglasses pushed up on head, expensive linen jacket over a black T-shirt, handheld camera or walkie-talkie
[SENSOR] a small grey environmental sensor box on a tripod with a coloured status LED

Full comic book page layout rough, portrait page, clear white gutters between panels, panels arranged in reading order left to right and top to bottom as follows: Row 1: panel 1, at the tomb entrance under work floodlights, Marsac holding out his tablet with three thumbnails; panel 2, close-up of the tablet screen with a redrawn ancient relief, Nefertari barely looking. Row 2: panel 3, Mansour leaning on his cane pointing at graffiti behind him; panel 4, the tablet showing a tomb plan with a dotted room, Maya shrugging. Row 3: panel 5, Marsac less sure of himself, Kerbu answering; panel 6, Marsac switching off his tablet, looking at the dark tomb entrance; panel 7, Kerbu turned to the graffiti, lamp lowered. Row 4: panel 8, full-width banner, close-up of the sensor screen blinking, the line touching the top of the frame. Setting: the rock-cut entrance of tomb KV9 at night under work floodlights. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. Loose but readable thumbnails, consistent characters from panel to panel, empty space left in each panel for speech balloons to be added later.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 4 · Case 1 — Marsac et ses trois vignettes

- Ratio : --ar 4:3
- Style : A
- Personnages : MARSAC, KERBU, NEFERTARI, MANSOUR, MAYA
- Statut : [F]
- ⚠ Référence obligatoire : photographies du Theban Mapping Project (fiche KV9) : entrée A de KV9 (porte taillée, grille) ; redessin
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MARSAC] Julien Marsac, French man about 50, stubble, swept-back greying hair, sunglasses pushed up on head, expensive linen jacket over a black T-shirt, handheld camera or walkie-talkie
[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

At the rock-cut entrance of the tomb, under harsh white work floodlights on stands, Julien Marsac holds out his tablet to the team; its screen shows three small image thumbnails side by side, blurred at this distance, with empty caption strips beneath them (words added at lettering). The team gathered around him, tired. Night sky black above the cliff. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 4 · Case 2 — L'« ampoule » de Dendérah, à l'écran

- Ratio : --ar 4:3
- Style : A
- Personnages : NEFERTARI, MARSAC
- Statut : [F] scène / [H] relief de Dendérah (temple de Dendérah, pas KV9) affiché à l'écran
- ⚠ Référence obligatoire : photographie de référence du relief de la crypte du temple de Dendérah (dit « lampe de Dendérah », Harsomtous) — redessin, uniquement sur l'écran de Marsac ; droits à vérifier (`bible/06` §6)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MARSAC] Julien Marsac, French man about 50, stubble, swept-back greying hair, sunglasses pushed up on head, expensive linen jacket over a black T-shirt, handheld camera or walkie-talkie

Close-up on Marsac's tablet screen held in his hand: it displays a photograph-like image of an ancient Egyptian stone relief from the temple of Dendera (a serpent emerging from a lotus flower inside an elongated form), faithfully redrawn from a reference photograph, nothing invented. The relief exists only on the screen. Behind the tablet, slightly out of focus, Nefertari glances at it only briefly, unimpressed. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 4 · Case 3 — Mansour : torches et miroirs

- Ratio : --ar 4:3
- Style : A
- Personnages : MANSOUR
- Statut : [H] torches et miroirs (`bible/03` §5) ; Dadouchios (V secondaire)
- ⚠ Référence obligatoire : photographies du Theban Mapping Project (fiche KV9) (entrée A / corridor B, graffiti)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book

Medium shot: Professor Mansour, leaning on his cane at the entrance of the tomb corridor, points with his free hand towards the faded scratched graffiti on the wall behind him, keeping his hand well away from the surface; patient, teacherly expression. Graffiti illegible. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 4 · Case 4 — Le plan aux pointillés

- Ratio : --ar 4:3
- Style : A
- Personnages : MAYA, MARSAC
- Statut : [H]/[C] débat KV62 (`bible/03` §5) ; brèche vers KV12 [H]
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[MARSAC] Julien Marsac, French man about 50, stubble, swept-back greying hair, sunglasses pushed up on head, expensive linen jacket over a black T-shirt, handheld camera or walkie-talkie

Over-the-shoulder shot: Marsac's tablet shows a simple white-line tomb floor plan with one extra room drawn in dotted lines, no labels. Maya, beside him, shrugs with sceptical calm, her own tablet tucked under her arm. Floodlight glare. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 4 · Case 5 — « Des visiteurs venus du ciel ? »

- Ratio : --ar 4:3
- Style : A
- Personnages : MARSAC, KERBU
- Statut : [N] aucune publication pour KV9 ; trait d'esprit de Kerbu [S]
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MARSAC] Julien Marsac, French man about 50, stubble, swept-back greying hair, sunglasses pushed up on head, expensive linen jacket over a black T-shirt, handheld camera or walkie-talkie
[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp

Two-shot: Marsac, less sure of himself, half raises his tablet, its screen turned away from the viewer (we do not see the image); Kerbu answers him with a warm, amused smile, one hand gesturing towards the dark tomb behind. No alien or spacecraft imagery anywhere. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 4 · Case 6 — Marsac raye la chambre secrète

- Ratio : --ar 4:3
- Style : A
- Personnages : MARSAC
- Statut : [F] (renoncement de Marsac)
- ⚠ Référence obligatoire : photographies du Theban Mapping Project (fiche KV9) : entrée A de KV9 (porte taillée, grille) ; redessin
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MARSAC] Julien Marsac, French man about 50, stubble, swept-back greying hair, sunglasses pushed up on head, expensive linen jacket over a black T-shirt, handheld camera or walkie-talkie

Marsac switches off his tablet, the screen going black; long silence; he stands still and looks at the black opening of the tomb entrance cut into the rock, his face half in shadow, thoughtful rather than humiliated. Floodlights behind him cast a long shadow towards the entrance. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 4 · Case 7 — Kerbu face aux graffiti

- Ratio : --ar 4:3
- Style : A
- Personnages : KERBU, NEFERTARI
- Statut : [S] (généralisation de Kerbu)
- ⚠ Référence obligatoire : photographies du Theban Mapping Project (fiche KV9) (corridor B, graffiti)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck

Kerbu turned towards the faded graffiti on the corridor wall, lamp held low and pointed at the floor, a peaceful expression; Nefertari beside him with a small smile. Soft, reconciled mood. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Planche 4 · Case 8 — Le record du capteur (bandeau final)

- Ratio : --ar 3:1
- Style : A
- Personnages : SENSOR, MAYA, MANSOUR
- Statut : [F] (relevé fictif, aucun chiffre)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[SENSOR] a small grey environmental sensor box on a tripod with a coloured status LED
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book

Close-up banner: the sensor on its tripod, its status LED blinking red; on its small screen a line graph climbs until it touches the top edge of the frame, no numbers, no units. In soft focus behind, Maya and Mansour look at it gravely. Tense, suspenseful lighting. --ar 3:1

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 11 · Page documentaire — Illustration : la voûte de la chambre J

- Ratio : --ar 3:2
- Style : A (adapté en schéma documentaire, sans liseré)
- Personnages : aucun personnage
- Statut : [H] (deux Nout dos à dos, Livres du Jour et de la Nuit, 12ᵉ heure)
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) et photographies du Theban Mapping Project (fiche KV9) (voûte de J) — redessin schématique ; la flèche « 12ᵉ heure : le soleil sort de Nout » est lettrée à la mise en page
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Clean documentary diagram on a pale parchment background: a simplified flat schematic of the vaulted ceiling of a burial chamber seen from below, showing two very elongated sky goddess silhouettes lying back to back along the length of the vault, with two long empty bands marking where the Books of the Day and of the Night run, and one curved arrow pointing to the end of one goddess's body where the sun emerges. Flat line drawing, deep blue and ochre accents, empty label areas for typesetting, no letters. --ar 3:2

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

## Épisode 12 — Le Soleil renaît

Nuit 12 sur 12 · descente A → J, salle K, sortie à l'aube. Finale : **lumière de l'aube sur les crêtes**, jamais le disque solaire dans le ciel.

## Ép. 12 · Planche 1 — Découverte archéologique (7 cases)

### Ép. 12 · Planche 1 — Mise en page : Découverte archéologique

- Ratio : --ar 17:22
- Style : rough de planche (style A ; cases à liseré doré en style B ou C, comme indiqué)
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA, SENSOR, KV9_CORRIDOR, KV9_J
- Grille :
  - Rangée 1 : case 1 (bandeau)
  - Rangée 2 : case 2 · case 3 (bande de trois petites cases enchaînées)
  - Rangée 3 : case 4 (étroite) · case 5 (grande case, demi-planche)
  - Rangée 4 : case 6 · case 7

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[SENSOR] a small grey environmental sensor box on a tripod with a coloured status LED
[KV9_CORRIDOR] long straight sloping rock-cut corridor, painted walls with registers of figures, starry astronomical ceiling, modern wooden walkway and handrails
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Full comic book page layout rough, portrait page, clear white gutters between panels, panels arranged in reading order left to right and top to bottom as follows: Row 1: panel 1, full-width banner, the tomb entrance at night, the team passing through the gate. Row 2: panel 2, Maya staring at the sensor screen; panel 3, a strip of three small chained sub-panels from the same angle, corridors, pillared hall, descent. Row 3: panel 4, narrow panel, the burial chamber with the sarcophagus and a smaller opening beyond; panel 5, large panel about half the page, four lamp beams converging on a painted scene in the last room. Row 4: panel 6, Maya raising her lamp and frowning; panel 7, close-up of Kerbu lit by the reflection of the scene. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. Loose but readable thumbnails, consistent characters from panel to panel, empty space left in each panel for speech balloons to be added later.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 1 · Case 1 — Dernière descente

- Ratio : --ar 3:1
- Style : A
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA
- Statut : [F]
- ⚠ Référence obligatoire : photographies du Theban Mapping Project (fiche KV9) : entrée A de KV9 (porte taillée, grille) ; redessin
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Wide banner: the rock-cut entrance of tomb KV9 in pitch-black night, a single work light; the team passes through the metal gate one after another; Professor Mansour, in front, clutches his old thick book tight against his chest. Determined, grave mood, starless black sky above the cliff. --ar 3:1

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 1 · Case 2 — Maya inquiète

- Ratio : --ar 1:1
- Style : A
- Personnages : MAYA, KERBU, SENSOR
- Statut : [F]
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[SENSOR] a small grey environmental sensor box on a tripod with a coloured status LED

Close-up: Maya stares at the sensor's small screen with a worried frown, the status LED orange; behind her, out of focus, Kerbu points down the corridor with resolve. --ar 1:1

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 1 · Case 3 — Cent mètres de roche (trois petites cases)

- Ratio : --ar 3:1
- Style : A
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA, KV9_CORRIDOR
- Statut : [H] décor (axe rectiligne vers l'ouest, TMP)
- ⚠ Référence obligatoire : photographies du Theban Mapping Project (fiche KV9) et Piankoff & Rambova 1954 (photographies de L. F. Husson) : corridors B-D, salle à piliers F, corridors G et H, antichambre I ; redessin selon `bible/06` §6
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[KV9_CORRIDOR] long straight sloping rock-cut corridor, painted walls with registers of figures, starry astronomical ceiling, modern wooden walkway and handrails

A horizontal strip divided into three small chained sub-panels, all from the same angle behind the team: first, the long straight sloping painted corridor with the modern wooden walkway; second, the square pillars of the pillared hall and the start of the descent; third, the further corridors and the small antechamber. The team's lamps get smaller each time, moving deeper. Decor of each room to be redrawn from reference photographs, no composed scenes, wall paintings soft and indistinct. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 3:1

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 1 · Case 4 — K, le bout de l'axe

- Ratio : --ar 2:3
- Style : A
- Personnages : NEFERTARI, KV9_J
- Statut : [H] (salle K jamais achevée, TMP)
- ⚠ Référence obligatoire : photographies du Theban Mapping Project (fiche KV9) : passage J → K et état réel des parois de K (degré d'achèvement) ; ne rien inventer
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Vertical panel: in the burial chamber, the team has passed the restored sarcophagus; beyond it, at the back, a smaller opening leads into a last room. Nefertari points to it with an outstretched arm. The surfaces of the last room, seen through the opening, are left dim and indistinct, to be drawn from photographs. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 2:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 1 · Case 5 — La scène finale du Livre des Portes

- Ratio : --ar 3:2
- Style : A
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA, NUN
- Statut : [H]
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) ou photographies du Theban Mapping Project (fiche KV9) : salle K (scène finale du Livre des Portes : Noun soulève la barque de Rê, roi agenouillé, décans en adoration) ; composition, nombre de figures et couleurs à copier strictement
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[NUN] bearded man with blue-green skin raising a solar barque out of the waters with his arms

Large panel: inside the last small room at the end of the tomb's axis, the four researchers stand in a half circle, their four lamp beams converging on one painted scene: a bearded god with blue-green skin raising a solar barque out of the waters with his arms, a kneeling king, figures in adoration. The painted scene is the focus, faithful to the reference, colours faded; figures and their number must be copied strictly from the reference, no improvisation. The team stays a metre from the wall. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 3:2

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 1 · Case 6 — « On l'a déjà vue »

- Ratio : --ar 4:3
- Style : A
- Personnages : MAYA, NEFERTARI
- Statut : [H] (scène finale des Portes en F et en K, TMP)
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) ou photographies du Theban Mapping Project (fiche KV9) : salle K (scène finale du Livre des Portes : Noun soulève la barque de Rê, roi agenouillé, décans en adoration) ; composition, nombre de figures et couleurs à copier strictement
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck

Maya raises her lamp high and frowns, puzzled, as if recognising something; Nefertari beside her nods, glancing back over her shoulder towards the way they came. The painted wall is softly lit in the background. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 1 · Case 7 — Kerbu : une aube

- Ratio : --ar 1:1
- Style : A
- Personnages : KERBU
- Statut : [H] fait / [S] lecture de Kerbu
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp

Close-up of Kerbu's face, lit by the warm reflected glow of the painted scene before him, blue-green and golden tones on his skin, eyes moist and calm, speaking in a whisper. Dark background. --ar 1:1

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

## Ép. 12 · Planche 2 — Analyse : la 12ᵉ heure (8 cases)

### Ép. 12 · Planche 2 — Mise en page : La 12ᵉ heure

- Ratio : --ar 17:22
- Style : rough de planche (style A ; cases à liseré doré en style B ou C, comme indiqué)
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA
- Grille :
  - Rangée 1 : case 1 · case 2
  - Rangée 2 : case 3 · case 4 · case 5
  - Rangée 3 : case 6 (grande case, encadré en bas)
  - Rangée 4 : case 7 · case 8

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Full comic book page layout rough, portrait page, clear white gutters between panels, panels arranged in reading order left to right and top to bottom as follows: Row 1: panel 1, Kerbu turning to Nefertari; panel 2, Maya's tablet showing the hours lighting up along the corridors with one empty slot. Row 2: panel 3, Kerbu with his hand stretched towards the painted scene without touching it; panel 4, Nefertari, eyebrow raised, arms crossed, Kerbu smiling; panel 5, Nefertari pulling out an annotated printed article. Row 3: panel 6, full-width large panel, Maya's 3D model of the chamber walls and the last room with coloured paths and an empty legend box. Row 4: panel 7, Nefertari looking up at the walls as if for the first time; panel 8, Mansour seated on a crate with his book open on his knees. Setting: the small unfinished last room of the tomb and the burial chamber. The panorama is displayed only on the two portable screens or the tablet, never projected onto the wall paintings. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. Loose but readable thumbnails, consistent characters from panel to panel, empty space left in each panel for speech balloons to be added later.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 2 · Case 1 — « Nuit 6. Tu te souviens ? »

- Ratio : --ar 4:3
- Style : A
- Personnages : KERBU, NEFERTARI
- Statut : [H] (11 heures sur 12, TMP)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck

Two-shot: Kerbu turns towards Nefertari, lamp lowered, an earnest questioning look; Nefertari answers, nodding, in the dim light of the last room. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 2 · Case 2 — La case vide de la 12ᵉ heure

- Ratio : --ar 4:3
- Style : A
- Personnages : MAYA
- Statut : [F] outil ; [H] structure de l'Amdouat (`bible/03` §2)
- ⚠ Référence obligatoire : si la 12ᵉ heure complète est montrée en vignette : redessin d'après photographies de KV34 (Thoutmosis III), uniquement à l'écran, avec la mention « autre tombe » au lettrage
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Over-the-shoulder shot: on Maya's tablet, a schematic 3D model of two long tomb corridors; small rectangular panels light up one after the other along their walls, eleven glowing slots, and in place of the twelfth an empty dark slot with a dotted outline. No labels, no numbers. Optional: a tiny separate inset thumbnail on the screen, marked as another tomb at lettering, redrawn from reference. The panorama is displayed only on the two portable screens or the tablet, never projected onto the wall paintings. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 2 · Case 3 — La main tendue, sans toucher

- Ratio : --ar 4:3
- Style : A
- Personnages : KERBU, NUN
- Statut : [S] rapprochement interprétatif ; [N] raison de l'absence
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) ou photographies du Theban Mapping Project (fiche KV9) : salle K (scène finale du Livre des Portes : Noun soulève la barque de Rê, roi agenouillé, décans en adoration) ; composition, nombre de figures et couleurs à copier strictement
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NUN] bearded man with blue-green skin raising a solar barque out of the waters with his arms

Kerbu stretches his open hand towards the painted scene of the god raising the solar barque, the palm stopping about twenty centimetres from the wall, never touching; his face in profile, contemplative. The painting softly lit, faithful to the reference. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 2 · Case 4 — « Tu sais ce que je vais dire. »

- Ratio : --ar 4:3
- Style : A
- Personnages : NEFERTARI, KERBU
- Statut : [S] annoncé par Kerbu lui-même
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp

Two-shot: Nefertari, one eyebrow raised, arms crossed, a knowing look; Kerbu answers with a disarming, self-aware smile, one hand on his chest. Warm complicity between them. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 2 · Case 5 — La liasse de Pleuger

- Ratio : --ar 4:3
- Style : A
- Personnages : NEFERTARI, KERBU
- Statut : [H] proposition de Pleuger 2020 p. 50, 68 (C : débat non résolu)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp

Nefertari pulls a folded bundle of printed pages from her jacket pocket, the pages covered with highlighter marks and handwritten notes shown as soft illegible scribbles; Kerbu leans in, surprised. Lamp light on the paper. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 2 · Case 6 — Toutes les lectures à la fois

- Ratio : --ar 3:2
- Style : A
- Personnages : MAYA, KERBU, NEFERTARI, MANSOUR
- Statut : [H] positions des savants ; [F] outil ; lettres en système Piankoff uniquement
- ⚠ Référence obligatoire : pour les miniatures de parois à l'écran : Piankoff & Rambova 1954 (photographies de L. F. Husson) / photographies du Theban Mapping Project (fiche KV9) (J et K)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book

Large panel: Maya holds up her tablet and the image fills most of the frame: a 3D model of the four walls of the burial chamber unfolded and, beyond, the small last room; glowing lines in several distinct colours link painted scenes according to each reading, some starting at the north wall, some at the south wall, some ending at the last room. At the bottom of the panel, an empty rectangular legend box for the inset text added at lettering. The team watches in the glow. No letters, no scene codes drawn. The panorama is displayed only on the two portable screens or the tablet, never projected onto the wall paintings. --ar 3:2

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 2 · Case 7 — Nefertari voit les parois autrement

- Ratio : --ar 4:3
- Style : A
- Personnages : NEFERTARI, KV9_J
- Statut : [H] citation Pleuger 2020 p. 67 ; aboutissement de l'arc de Nefertari
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) et photographies du Theban Mapping Project (fiche KV9), chambre J ; redessin selon `bible/06_edition_kdp_droits.md` §6
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Nefertari lowers her printed pages and slowly raises her eyes towards the painted walls around her, as if seeing them for the first time; soft wonder on her face, glasses reflecting the lamplight; the painted walls a gentle blur of ochre and blue around her. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 2 · Case 8 — Mansour sur sa caisse

- Ratio : --ar 4:3
- Style : A
- Personnages : MANSOUR
- Statut : [S] (formulation)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book

Professor Mansour sits on a closed equipment crate, his cane leaning beside him, his old thick annotated book open on his knees, pages soft and illegible; he looks up with a serene, wise smile. Warm lamp light, quiet. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

## Ép. 12 · Planche 3 — Immersion : les formes du soleil (8 cases)

Cases 1 à 6 : **reconstitution symbolique [S]**, style mural, fond noir, ligne de sol ondulée (même code que le prologue, P2 case 6). Chaque figure prise isolément est attestée et doit être dessinée **d'après les model sheets de `bible/03` §1**. Aucune paroi égyptienne ne réunit ces images en une scène.

### Ép. 12 · Planche 3 — Mise en page : Les formes du soleil

- Ratio : --ar 17:22
- Style : rough de planche (style A ; cases à liseré doré en style B ou C, comme indiqué)
- Personnages : NUN, TATENEN, AKER, RE_NIGHT, KHEPRI, NUT, KERBU
- Grille :
  - Rangée 1 : case 1 (case charnière, pleine largeur)
  - Rangée 2 : case 2 (grande case)
  - Rangée 3 : case 3 · case 4 · case 5
  - Rangée 4 : case 6 · case 7 · case 8 (sans liseré)

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[NUN] bearded man with blue-green skin raising a solar barque out of the waters with his arms
[TATENEN] bearded man with ram horns, sun disk and two tall plumes, sometimes green skin
[AKER] double sphinx: two lion bodies joined back to back, one head at each end, a barque resting on its back
[RE_NIGHT] ram-headed sun god standing in a shrine on a solar barque
[KHEPRI] scarab beetle pushing or emerging from a red sun disk
[NUT] elongated woman arched over the scene, body covered with stars, dark blue background
[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp

Full comic book page layout rough, portrait page, clear white gutters between panels, panels arranged in reading order left to right and top to bottom as follows: Row 1: panel 1, full-width hinge panel, painted arms of a god on a wall turning into the same arms rising huge from a black background, gold border appearing. Row 2: panel 2, full-width large gold-bordered panel, below a wavy ground line the night barque gliding on a double sphinx with a ram-headed god in a shrine. Row 3: panel 3, arms rising from the ground embracing a large disk; panel 4, two gods holding two barques entering and leaving the double sphinx; panel 5, a scarab emerging from a disk. Row 4: panel 6, above the ground line, mirrored images of a child and a scarab rising from waters and a disk born on the starry body of the sky goddess; panel 7, an ancient painter with an oil lamp; panel 8, same framing in the present with an LED lamp, no gold border. Panels 1 to 6 in flat ancient Egyptian painting style on a black background with a wavy ground line and a thin gold border; panel 7 warm historical reconstruction with gold border; panel 8 contemporary without border. Loose but readable thumbnails, consistent characters from panel to panel, empty space left in each panel for speech balloons to be added later.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 3 · Case 1 — Case charnière : les bras de Noun

- Ratio : --ar 3:1
- Style : B
- Personnages : NUN
- Statut : [S] (composition de la planche)
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) ou photographies du Theban Mapping Project (fiche KV9) : salle K (scène finale du Livre des Portes : Noun soulève la barque de Rê, roi agenouillé, décans en adoration) ; composition, nombre de figures et couleurs à copier strictement ; model sheets de `bible/03_divinites_iconographie.md` §1, elles-mêmes copiées sur références publiées
- Prompt :

```
[STYLE B] Ancient Egyptian New Kingdom tomb painting style, flat mineral colours (red ochre, yellow
ochre, Egyptian blue, malachite green, carbon black, lime white), bold black outlines, figures in strict
profile with frontal eye and shoulders, Egyptian canon of proportions, horizontal registers, no
perspective, no shading, thin gold border around the panel.

[NUN] bearded man with blue-green skin raising a solar barque out of the waters with his arms

Mural style on a plain black background, a wavy horizontal ground line representing the Earth (same visual code as the prologue). Hinge banner: on the left, the painted arms of the god raising the barque as they appear on a faded tomb wall in lamplight; moving right, the same arms grow immense and rise out of a plain black background, flat mineral colours, as a thin gold border appears around the panel. --ar 3:1

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 3 · Case 2 — La barque de nuit sur Aker

- Ratio : --ar 3:2
- Style : B
- Personnages : AKER, RE_NIGHT
- Statut : [S] composition / figures [H] (Darnell §6.1, 6.26 ; `bible/03` §1-2)
- ⚠ Référence obligatoire : model sheets de `bible/03_divinites_iconographie.md` §1, elles-mêmes copiées sur références publiées
- Prompt :

```
[STYLE B] Ancient Egyptian New Kingdom tomb painting style, flat mineral colours (red ochre, yellow
ochre, Egyptian blue, malachite green, carbon black, lime white), bold black outlines, figures in strict
profile with frontal eye and shoulders, Egyptian canon of proportions, horizontal registers, no
perspective, no shading, thin gold border around the panel.

[AKER] double sphinx: two lion bodies joined back to back, one head at each end, a barque resting on its back
[RE_NIGHT] ram-headed sun god standing in a shrine on a solar barque

Mural style on a plain black background, a wavy horizontal ground line representing the Earth (same visual code as the prologue). Large panel: below the wavy ground line, in the dark underworld, the night barque glides on the back of the double sphinx, one lion head at each end; on board, under a shrine (naos), the ram-headed sun god stands in strict profile. Composition calm and horizontal, deep black space around. --ar 3:2

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 3 · Case 3 — Des bras embrassent le disque

- Ratio : --ar 1:1
- Style : B
- Personnages : aucun personnage
- Statut : [S] composition / [H] Darnell §6.3
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) (Livre de la Terre, KV9, scène du disque embrassé par des bras, §6.3 de Darnell) ; model sheets de `bible/03_divinites_iconographie.md` §1, elles-mêmes copiées sur références publiées
- Prompt :

```
[STYLE B] Ancient Egyptian New Kingdom tomb painting style, flat mineral colours (red ochre, yellow
ochre, Egyptian blue, malachite green, carbon black, lime white), bold black outlines, figures in strict
profile with frontal eye and shoulders, Egyptian canon of proportions, horizontal registers, no
perspective, no shading, thin gold border around the panel.

Mural style on a plain black background, a wavy horizontal ground line representing the Earth (same visual code as the prologue). Two arms rise from beneath the wavy ground line and embrace a large red sun disk, holding it gently above the earth; symmetrical composition. --ar 1:1

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 3 · Case 4 — Noun et Tatenen (case muette)

- Ratio : --ar 4:3
- Style : B
- Personnages : NUN, TATENEN, AKER
- Statut : [S] composition / [H] Darnell §6.40
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) (scène §6.40 de Darnell) ; model sheets de `bible/03_divinites_iconographie.md` §1, elles-mêmes copiées sur références publiées
- Prompt :

```
[STYLE B] Ancient Egyptian New Kingdom tomb painting style, flat mineral colours (red ochre, yellow
ochre, Egyptian blue, malachite green, carbon black, lime white), bold black outlines, figures in strict
profile with frontal eye and shoulders, Egyptian canon of proportions, horizontal registers, no
perspective, no shading, thin gold border around the panel.

[NUN] bearded man with blue-green skin raising a solar barque out of the waters with his arms
[TATENEN] bearded man with ram horns, sun disk and two tall plumes, sometimes green skin
[AKER] double sphinx: two lion bodies joined back to back, one head at each end, a barque resting on its back

Mural style on a plain black background, a wavy horizontal ground line representing the Earth (same visual code as the prologue). Silent panel: two gods face each other across the double sphinx: on one side the bearded god with blue-green skin, on the other the bearded god with ram horns, sun disk and two tall plumes; each one holds up a barque, one barque entering the double sphinx, the other leaving it. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 3 · Case 5 — « Moi-même, je me mets au monde »

- Ratio : --ar 1:1
- Style : B
- Personnages : KHEPRI
- Statut : [S] composition / [H] Darnell §6.16
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) (scène §6.16 de Darnell) ; model sheets de `bible/03_divinites_iconographie.md` §1, elles-mêmes copiées sur références publiées
- Prompt :

```
[STYLE B] Ancient Egyptian New Kingdom tomb painting style, flat mineral colours (red ochre, yellow
ochre, Egyptian blue, malachite green, carbon black, lime white), bold black outlines, figures in strict
profile with frontal eye and shoulders, Egyptian canon of proportions, horizontal registers, no
perspective, no shading, thin gold border around the panel.

[KHEPRI] scarab beetle pushing or emerging from a red sun disk

Mural style on a plain black background, a wavy horizontal ground line representing the Earth (same visual code as the prologue). A scarab beetle emerges from a large red sun disk, wings slightly open, rising upward above the wavy ground line; golden glow around it; empty space at the top of the panel for a golden speech balloon to be added at lettering. --ar 1:1

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 3 · Case 6 — Bélier, disque, scarabée, enfant

- Ratio : --ar 4:3
- Style : B
- Personnages : KHEPRI, NUT
- Statut : [S] (cartouche) / figures [H] (fin du Livre des Cavernes ; 12ᵉ heure, voûte de J)
- ⚠ Référence obligatoire : fin du Livre des Cavernes (paroi nord de F) et voûte de J : Piankoff & Rambova 1954 (photographies de L. F. Husson) / photographies du Theban Mapping Project (fiche KV9) ; model sheets de `bible/03_divinites_iconographie.md` §1, elles-mêmes copiées sur références publiées
- Prompt :

```
[STYLE B] Ancient Egyptian New Kingdom tomb painting style, flat mineral colours (red ochre, yellow
ochre, Egyptian blue, malachite green, carbon black, lime white), bold black outlines, figures in strict
profile with frontal eye and shoulders, Egyptian canon of proportions, horizontal registers, no
perspective, no shading, thin gold border around the panel.

[KHEPRI] scarab beetle pushing or emerging from a red sun disk
[NUT] elongated woman arched over the scene, body covered with stars, dark blue background

Mural style on a plain black background, a wavy horizontal ground line representing the Earth (same visual code as the prologue). Above the wavy ground line, two images in mirror: on the left, a child and a scarab rising together out of rippling blue waters; on the right, on the starry arched body of the sky goddess, a red sun disk being born at the end of her body. Balanced, luminous composition. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 3 · Case 7 — Le peintre antique s'arrête

- Ratio : --ar 4:3
- Style : C
- Personnages : NUN (+ PEINTRE antique fictif, sans fiche ; même visage que l'ép. 1 s'il a été dessiné)
- Statut : [F] peintre ; [H] K jamais achevée ; raison de l'arrêt N
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) ou photographies du Theban Mapping Project (fiche KV9) : salle K (scène finale du Livre des Portes : Noun soulève la barque de Rê, roi agenouillé, décans en adoration) ; composition, nombre de figures et couleurs à copier strictement (état de K) ; vêtement et lampe à huile d'après références du Nouvel Empire
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.
[STYLE C] Same comic art as Style A but warmer palette; for antiquity: oil lamps and torchlight, raw
limestone, plain linen clothing; for 20th century scenes: sepia-toned archival look. Thin gold border.

[NUN] bearded man with blue-green skin raising a solar barque out of the waters with his arms

Return to antiquity, inside the small unfinished last room of the tomb: a fictional ancient Egyptian painter, a lean man in a plain linen kilt, kneels in front of the painted scene of the god raising the barque; he has just lowered his brush and lets his hands rest on his knees, far from the wall; a small oil lamp on the floor flickers; nobody behind him, the room empty and silent. Painting technique not shown in detail. If the painter of episode 1 was drawn, keep the same face. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 3 · Case 8 — Retour au présent : la LED

- Ratio : --ar 4:3
- Style : A
- Personnages : KERBU, SENSOR
- Statut : [F] (implicite)
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) ou photographies du Theban Mapping Project (fiche KV9) : salle K (scène finale du Livre des Portes : Noun soulève la barque de Rê, roi agenouillé, décans en adoration) ; composition, nombre de figures et couleurs à copier strictement
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[SENSOR] a small grey environmental sensor box on a tripod with a coloured status LED

Back to the present, exactly the same framing as the previous panel, no gold border: Kerbu kneels where the painter knelt, his LED lamp on the floor in place of the oil lamp, the painted scene faded by the centuries; he turns his head as the sensor's LED blinks off-panel. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

## Ép. 12 · Planche 4 — Résolution (8 cases)

### Ép. 12 · Planche 4 — Mise en page : Résolution

- Ratio : --ar 17:22
- Style : rough de planche (style A ; cases à liseré doré en style B ou C, comme indiqué)
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA, MARSAC, KV9_J, KV9_CORRIDOR
- Grille :
  - Rangée 1 : case 1 · case 2
  - Rangée 2 : case 3 (verticale, un tiers) · case 4
  - Rangée 3 : case 5 (grande case pleine largeur)
  - Rangée 4 : case 6 · case 7
  - Rangée 5 : case 8 (bandeau final)

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[MARSAC] Julien Marsac, French man about 50, stubble, swept-back greying hair, sunglasses pushed up on head, expensive linen jacket over a black T-shirt, handheld camera or walkie-talkie
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus
[KV9_CORRIDOR] long straight sloping rock-cut corridor, painted walls with registers of figures, starry astronomical ceiling, modern wooden walkway and handrails

Full comic book page layout rough, portrait page, clear white gutters between panels, panels arranged in reading order left to right and top to bottom as follows: Row 1: panel 1, near the sarcophagus, Mansour handing his old book to Maya; panel 2, Maya opening the book, margins covered with two handwritings, Kerbu and Nefertari in the background. Row 2: panel 3, vertical silent panel taking one third of the width, the team climbing the sloping corridor towards the entrance turning blue-grey; panel 4, at the gate, Marsac waiting by his camera on a tripod. Row 3: panel 5, full-width large panel, the Valley of the Kings at dawn, light on the cliff tops, valley still in shadow, tiny silhouettes at the tomb entrance. Row 4: panel 6, Nefertari beside Kerbu looking towards the light; panel 7, Kerbu facing us, golden light on his face. Row 5: panel 8, full-width final banner, wide view of the tomb entrance in morning light, five figures seen from behind, faint overlay of a painted sun disk motif. Dawn light only on the cliff tops; no sun disk in the sky. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. Loose but readable thumbnails, consistent characters from panel to panel, empty space left in each panel for speech balloons to be added later.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 4 · Case 1 — Mansour tend son livre

- Ratio : --ar 4:3
- Style : A
- Personnages : MANSOUR, MAYA, KV9_J
- Statut : [F] (exemplaire, annotations, maître) ; [H] publication 1954
- ⚠ Référence obligatoire : Piankoff & Rambova 1954 (photographies de L. F. Husson) et photographies du Theban Mapping Project (fiche KV9), chambre J ; redessin selon `bible/06_edition_kdp_droits.md` §6 (sarcophage restauré)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[KV9_J] vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

In the burial chamber, beside the restored dark green sarcophagus (kept at a distance), Professor Mansour holds out his old thick book with both hands to Maya; Maya, moved, raises her hands without yet taking it, shaking her head. Warm lamp light, intimate, the painted walls dim behind. No readable cover title, no reproduced page. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 4 · Case 2 — Les marges aux deux écritures

- Ratio : --ar 4:3
- Style : A
- Personnages : MAYA, MANSOUR, KERBU, NEFERTARI
- Statut : [F]
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck

Maya opens the old book on her forearm: the margins are densely covered with two different handwritings, one older and slanted, one neater, rendered as soft illegible scribbles; Mansour watches her with a gentle smile; in the background, a little apart, Kerbu murmurs to Nefertari, who replies with a dry, amused look. No legible text, no reproduced page. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 4 · Case 3 — La remontée (case muette)

- Ratio : --ar 2:3
- Style : A
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA, KV9_CORRIDOR
- Statut : [F] (implicite) ; décor [H]
- ⚠ Référence obligatoire : photographies du Theban Mapping Project (fiche KV9) (corridors de KV9, vue vers l'entrée)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[KV9_CORRIDOR] long straight sloping rock-cut corridor, painted walls with registers of figures, starry astronomical ceiling, modern wooden walkway and handrails

Vertical silent panel: low angle from the bottom of the long sloping corridor, the team climbs the modern wooden walkway towards the top, small figures with their lamps; at the top, the rectangle of the entrance shifts from black to a pale blue-grey of early dawn. Painted walls soft on both sides. Nobody touches the walls: hands, lamps and tools are held a few centimetres away from the painted surfaces, not touching. --ar 2:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 4 · Case 4 — Marsac à la grille

- Ratio : --ar 4:3
- Style : A
- Personnages : MARSAC, NEFERTARI
- Statut : [F]
- ⚠ Référence obligatoire : photographies du Theban Mapping Project (fiche KV9) : entrée A de KV9 (porte taillée, grille) ; redessin
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[MARSAC] Julien Marsac, French man about 50, stubble, swept-back greying hair, sunglasses pushed up on head, expensive linen jacket over a black T-shirt, handheld camera or walkie-talkie
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck

At the metal gate of the tomb entrance, in the cold blue pre-dawn light, Julien Marsac waits beside his camera on a tripod, but he is not filming, his hands in his pockets; Nefertari emerges first and faces him; then a slow smile appears on Marsac's face. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 4 · Case 5 — La Vallée des Rois à l'aube

- Ratio : --ar 3:2
- Style : A
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA, MARSAC
- Statut : [H] décor
- ⚠ Référence obligatoire : photographies de l'aube sur la Vallée des Rois et sur el-Qurn (lumière sur les crêtes), et photographies du Theban Mapping Project (fiche KV9) pour l'entrée de KV9 ; ce que l'on voit réellement du lever du soleil depuis l'entrée est N
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[MARSAC] Julien Marsac, French man about 50, stubble, swept-back greying hair, sunglasses pushed up on head, expensive linen jacket over a black T-shirt, handheld camera or walkie-talkie

Large panoramic panel: the Valley of the Kings at dawn, the first golden light touching only the tops of the Theban cliffs and the pyramid-shaped peak of el-Qurn, while the valley floor is still in cool blue shadow; tiny silhouettes of five people stand at the rock-cut entrance of the tomb. No sun disk visible in the sky, only light on the crests. Landscape to be drawn after real dawn photographs. --ar 3:2

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 4 · Case 6 — « Ta question. »

- Ratio : --ar 4:3
- Style : A
- Personnages : NEFERTARI, KERBU
- Statut : [F] (écho exact du prologue P1 case 4)
- ⚠ Référence obligatoire : cadrage du prologue, planche P1, case 4 (`02_prologue.md`) pour l'écho visuel
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp

Two-shot: Nefertari stands beside Kerbu outside the tomb entrance, both looking towards the dawn light on the cliffs, Nefertari turning her head to him with a quiet question in her eyes. Framing mirrors the prologue scene. Soft golden reflected light, no sun disk visible. --ar 4:3

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 4 · Case 7 — Kerbu dans la lumière dorée

- Ratio : --ar 1:1
- Style : A
- Personnages : KERBU
- Statut : [S] (réponse de Kerbu, conclusion de la saison)
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp

Close-up of Kerbu facing the viewer, warm golden dawn light on his face coming from the low light on the crests; his LED headlamp has just switched itself off; serene, peaceful expression, slight smile. No sun disk in frame. --ar 1:1

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Planche 4 · Case 8 — L'entrée dans la lumière du matin (bandeau final)

- Ratio : --ar 3:1
- Style : A
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA, MARSAC (+ motif du disque de la porte B, sans fiche : d'après référence)
- Statut : [H] disque de la porte B / [S] surimpression
- ⚠ Référence obligatoire : photographies du Theban Mapping Project (fiche KV9) / Piankoff & Rambova 1954 (photographies de L. F. Husson) : disque de la porte B (scarabée et dieu à tête de bélier dans le même disque) ; entrée de KV9 ; photos de l'aube sur la Vallée des Rois
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[KERBU] Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
[NEFERTARI] Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
[MANSOUR] Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
[MAYA] Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
[MARSAC] Julien Marsac, French man about 50, stubble, swept-back greying hair, sunglasses pushed up on head, expensive linen jacket over a black T-shirt, handheld camera or walkie-talkie

Final wide banner: the rock-cut entrance of tomb KV9 bathed in soft morning light reflected from the cliffs, the five characters seen from behind, standing side by side at the entrance, looking out over the valley. Faintly superimposed in the sky area, as a light translucent overlay, the painted sun disk motif from above the tomb's first door (a disk containing a scarab and a ram-headed god), copied from the reference. No real sun disk in the sky, light on the crests only. --ar 3:1

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

### Ép. 12 · Page documentaire — Illustration : plan de KV9 et les douze nuits

- Ratio : --ar 3:1
- Style : A (adapté en schéma documentaire, sans liseré)
- Personnages : aucun personnage
- Statut : [H] plan (TMP) / [F] numéros des nuits
- ⚠ Référence obligatoire : plan de KV9 du Theban Mapping Project (proportions et ordre des salles A → K) ; lettres des salles et numéros des nuits posés à la mise en page
- Prompt :

```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Clean documentary diagram on a pale parchment background: a long horizontal simplified floor plan of a straight rock-cut royal tomb, from the entrance on the left to the end on the right: entrance ramp, three successive corridors, a small room, a square pillared hall, two more corridors, a small antechamber, a vaulted burial chamber with four pillars, and a small last room at the far end. Next to each zone, a small empty round badge for a night number added at typesetting. In the last room, a small golden sun drawn as a simple circle with short rays. Flat vector line style, thin black outlines, ochre fills, no letters, no numbers drawn. --ar 3:1

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters
```

---

*Total : 12 prompts de mise en page, 89 prompts de case, 3 illustrations documentaires (104 prompts).*
