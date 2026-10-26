# Prompts d'images — Épisodes 1 à 3

Prompts pour *Les Mystères du tombeau de Ramsès VI*, Volume 1, épisodes 1 (*La porte de KV9*),
2 (*Le plafond des étoiles*) et 3 (*Le livre sans commencement*). Scripts sources :
`03_episode_01_la_porte_de_kv9.md`, `04_episode_02_le_plafond_des_etoiles.md`,
`05_episode_03_le_livre_sans_commencement.md`. Règles et fiches : `00_guide_prompts.md`.

## Mode d'emploi

- **Pour chaque planche** : un prompt de **mise en page** (rough de la planche entière, `--ar 17:22`), puis
  un prompt par **case**, dans l'ordre du script. Chaque épisode se termine par le prompt d'illustration de
  sa **page documentaire**.
- **Chaque prompt est complet** : bloc(s) de style recopiés du guide (Style C est toujours précédé du
  Style A, auquel il renvoie), fiches personnages et éléments recopiées mot pour mot, description de la
  case, consignes de conservation, négatif obligatoire, ratio.
- **Fiches MAYA et MARSAC** : ce sont des propositions **à valider par l'auteur** (guide §3). Une fois
  validées, remplacer le texte partout dans ce fichier à l'identique.
- **Statut** : repris du script. « — (non marqué) » signale une case sans balise dans le script ; la
  parenthèse indique le statut de son contenu.
- **⚠ Référence obligatoire** : toute case qui montre une paroi, un objet ou un lieu réel doit être
  générée en image-to-image à partir de la référence citée, ou redessinée par un artiste. Jamais publiée
  telle quelle (guide §1). Les scènes peintes sont décrites volontairement par la formule
  « painted register with figures, copy from reference » : leur contenu ne doit pas être inventé.
- **Personne ne touche les parois ni les objets** ; aucune lumière forte projetée sur les peintures.
  Seules exceptions voulues par le script : les **artisans antiques** au travail (Ép. 1, planche 3), le
  **trait laser faible** du scanner (Ép. 3, pl. 1, case 7) et le **flash** de l'expédition de 1949-1951
  (Ép. 3, pl. 3, case 4). Elles sont signalées dans les cases.
- **Personnages historiques réels** (Howard Carter, Alexandre Piankoff, L. F. Husson) : de dos ou en
  silhouette, sans ressemblance revendiquée. Natacha Rambova n'apparaît pas sur place.
- **Liseré doré** : il fait partie des blocs B et C ; quand le script le fait « apparaître une seconde »
  sur une case contemporaine, il est ajouté **en mise en page**, l'image ne porte qu'une lueur au bord du
  cadre.
- **Aucun texte** dans les images : bulles, cartouches, SFX, dates, libellés et citations sont posés au
  lettrage.


---

# Épisode 1 — La porte de KV9


## Planche 1 — Découverte archéologique (7 cases)

### Ép. 1 · Planche 1 — Mise en page (rough)
- Ratio : --ar 17:22
- Style : A (contemporain)
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA, SENSOR
- Grille :
  - Rangée 1 : C1 bandeau pleine largeur (≈ 1/4 de la hauteur)
  - Rangée 2 : C2 | C3 | C4 (C4 plus étroite, carrée)
  - Rangée 3 : C5 | C6 | C7
- Statut : rough de composition uniquement (pas d'image publiable).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
SENSOR: a small grey environmental sensor box on a tripod with a coloured status LED

Panel: Full comic page layout rough, 7 panels in 3 rows with white gutters. Row 1: one wide full-width banner: four explorers pass through the modern metal gate of a rock-cut royal tomb, golden dawn light behind them turning into cold blue LED light ahead. Row 2, three panels: a woman fixing a small sensor box on a tripod near the entrance while an old man with a cane watches; a Black man with a headlamp stopping in front of a painted wall with scratched graffiti; an extreme close-up of scratched marks in painted plaster. Row 3, three panels: a woman with glasses smiling; an old man leaning on his cane, reciting; the Black man pensive, lamp moving from the graffiti to painted gods nearby. Empty space left in each panel for speech balloons.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 17:22
```

### Ép. 1 · Planche 1 · Case 1 — L'équipe franchit la grille
- Ratio : --ar 3:1
- Style : A (contemporain)
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA · éléments : KV9_CORRIDOR
- Statut : [F]
- ⚠ Référence obligatoire : photographies de l'entrée de KV9 (grille, escalier, passerelle) — Theban Mapping Project ; ne pas inventer la forme de l'entrée.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
KV9_CORRIDOR: long straight sloping rock-cut corridor, painted walls with registers of figures, starry astronomical ceiling, modern wooden walkway and handrails

Panel: Wide cinematic banner, eye-level side view. The four team members pass one after another through the modern metal gate at the entrance of the tomb KV9 and step onto the wooden walkway. Behind them (left side of the panel) warm golden dawn light from the valley; ahead of them (right side) the descending corridor lit by cold blue-white LED light: a clear colour-temperature transition from gold to cold blue across the panel. Kerbu leads with his headlamp on, Maya carries equipment cases, Nefertari follows, Mansour walks last with his cane. Dust particles in the light. Mood: quiet, solemn first step.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 3:1
```

### Ép. 1 · Planche 1 · Case 2 — Maya pose le capteur
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : MAYA, MANSOUR, SENSOR
- Statut : [F] (note [H] générale sur la conservation, sans chiffre)
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
SENSOR: a small grey environmental sensor box on a tripod with a coloured status LED

Panel: Medium shot just inside the entrance. Maya kneels on the wooden walkway and fixes the small sensor box on its tripod; the status LED glows green. The tripod stands on the walkway floor, well away from the walls. Mansour stands behind her, both hands on his cane, looking with tender concern at the faded paintings around them. Cold LED light mixed with Maya's warm headlamp. Mood: practical urgency versus reverence.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 1 · Planche 1 · Case 3 — Kerbu découvre des lettres grecques
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : KERBU
- Statut : [H]
- ⚠ Référence obligatoire : graffiti grecs du corridor B : photographies du Theban Mapping Project, mission épigraphique polonaise (PCMA), catalogue J. Baillet (IFAO, 1920-1926). Recopier un graffito réel, ne jamais en inventer.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp

Panel: Medium close shot in the first corridor. Kerbu stops abruptly, headlamp on, and points with his hand held a few centimetres away from the wall: in the middle of the painted scenes, a patch of thin scratched letters incised into the paint. The scratched marks are rendered as an unreadable area of fine incised lines (to be replaced by an exact copy from reference). Expression: surprise and curiosity. Soft raking headlamp light.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 1 · Planche 1 · Case 4 — Gros plan sur les graffiti
- Ratio : --ar 1:1
- Style : A (contemporain)
- Personnages : —
- Statut : [H]
- ⚠ Référence obligatoire : même source que la case 3 (photographie publiée d'un graffito précis de KV9). Case à redessiner à la main : aucun texte lisible généré.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Panel: Extreme close-up of ancient graffiti scratched into painted plaster: the texture of the plaster, the layers of faded red ochre, yellow ochre and blue paint, the fine white scratch lines cutting through the paint. The letter shapes themselves are left deliberately unreadable and slightly out of focus: this area will be replaced by an artist's exact copy from a published photograph. Low raking light from a headlamp, very soft.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 1 · Planche 1 · Case 5 — Nefertari sourit
- Ratio : --ar 1:1
- Style : A (contemporain)
- Personnages : NEFERTARI, MAYA
- Statut : — (non marqué ; scène [F], réplique [H] générale)
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Panel: Close shot. Nefertari, amused and warm, smiles as she explains; her loupe hangs on its cord. Behind her, slightly out of focus, Maya raises her eyebrows in disbelief. Cold LED light, warm headlamp accents. Mood: light humour.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 1 · Planche 1 · Case 6 — Mansour récite
- Ratio : --ar 1:1
- Style : A (contemporain)
- Personnages : MANSOUR
- Statut : — (non marqué ; image [F], réplique [H] sourcée TMP/SIP)
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book

Panel: Medium close-up. Mansour, one hand resting on the top of his cane, the old annotated book under his arm, eyes half-closed as if reciting from memory, a faint knowing smile. Warm headlamp light on his lined face, the cold corridor behind him. Mood: the scholar's quiet authority.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 1 · Planche 1 · Case 7 — Kerbu, pensif, entre graffiti et dieux
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : KERBU
- Statut : — (non marqué ; paroi réelle [H])
- ⚠ Référence obligatoire : même paroi que les cases 3-4 (graffiti + figures divines voisines) d'après photographies TMP / Piankoff & Rambova 1954 ; figures peintes : « painted register with figures, copy from reference ».
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp

Panel: Medium shot, three-quarter profile. Kerbu stands pensive a short distance from the wall, his handheld lamp moving from the scratched graffiti to the painted gods just beside them (suggest the movement with two soft overlapping pools of diffuse light). His face is thoughtful, slightly melancholic. Leave empty dark space at the top of the panel for a thought balloon.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```


## Planche 2 — Analyse d'une inscription (7 cases)

### Ép. 1 · Planche 2 — Mise en page (rough)
- Ratio : --ar 17:22
- Style : A (contemporain)
- Personnages : NEFERTARI, KERBU, MANSOUR, MAYA
- Grille :
  - Rangée 1 : C1 grande case pleine largeur (≈ 1/2 de la hauteur)
  - Rangée 2 : C2 | C3 | C4
  - Rangée 3 : C5 | C6 | C7
- Statut : rough de composition uniquement (pas d'image publiable).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Panel: Full comic page layout rough, 7 panels in 3 rows with white gutters. Row 1: one large full-width panel: a long straight sloping rock-cut corridor in one-point perspective, two different painted programmes on the left and right walls, a dark blue starry ceiling, four small explorers on a wooden walkway. Row 2, three panels: a woman raising a tablet toward the painted ceiling; a woman holding a magnifying loupe near a painted royal cartouche with a Black man looking over her shoulder; an old man with a cane in medium close-up. Row 3, three panels: a perplexed young woman and the old man shrugging; dramatic close-up of the Black man lit from below by a lamp under his chin; the woman with glasses raising a firm finger while the Black man smiles. Empty space for speech balloons.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 17:22
```

### Ép. 1 · Planche 2 · Case 1 — Deux livres se font face
- Ratio : --ar 3:2
- Style : A (contemporain)
- Personnages : NEFERTARI, KERBU, MANSOUR, MAYA · éléments : KV9_CORRIDOR
- Statut : [H]
- ⚠ Référence obligatoire : corridor B de KV9 : Livre des Portes paroi sud (à gauche en entrant), Livre des Cavernes paroi nord (à droite) — photographies TMP et planches de Piankoff & Rambova 1954. Ne pas inventer le contenu des registres.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
KV9_CORRIDOR: long straight sloping rock-cut corridor, painted walls with registers of figures, starry astronomical ceiling, modern wooden walkway and handrails

Panel: Large panel, one-point perspective down the first corridor (corridor B), camera at eye level in the middle of the walkway. Left wall (south) and right wall (north) carry two different painted programmes, both rendered as painted registers with figures, copy from reference; dark blue astronomical ceiling above. The four team members are small figures on the walkway; Nefertari, in front, gestures with open hands toward both walls at once without approaching them. Cold LED light, warm headlamp pools, dust in the air. Mood: wonder, a cathedral of images.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 3:2
```

### Ép. 1 · Planche 2 · Case 2 — Maya lève sa tablette vers le plafond
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : MAYA, NEFERTARI
- Statut : [H] (plafond) / [S] (« modèle du monde »)
- ⚠ Référence obligatoire : plafond du corridor B (constellations circumpolaires et décans) : photographies TMP, Piankoff & Rambova 1954. Disposition des figures non inventée.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck

Panel: Low-angle shot from below. Maya holds her tablet up toward the ceiling, the screen showing a blurred capture of it; Nefertari beside her looks up, calm. The ceiling: dark blue field with rows of painted stars and astronomical figures, rendered as a painted ceiling with figures, copy from reference. Soft light only, no beam aimed at the ceiling.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 1 · Planche 2 · Case 3 — Nefertari et le cartouche royal
- Ratio : --ar 1:1
- Style : A (contemporain)
- Personnages : NEFERTARI, KERBU
- Statut : [H]
- ⚠ Référence obligatoire : cartouches de Ramsès VI regravés sur les montants des portes B à F : photographies TMP / Piankoff & Rambova 1954. Signes recopiés par l'artiste, jamais générés.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp

Panel: Close shot. Nefertari, wearing nitrile gloves, holds her epigraphy loupe a few centimetres in front of a painted royal cartouche on a door jamb, not touching it; the cartouche is seen softly through and around the lens, its signs left blurred and unreadable (to be copied from reference). Kerbu leans in over her shoulder, intent. Warm headlamp light.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 1 · Planche 2 · Case 4 — Mansour explique la reprise du tombeau
- Ratio : --ar 1:1
- Style : A (contemporain)
- Personnages : MANSOUR
- Statut : — (non marqué ; réplique [H] sourcée TMP)
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book

Panel: Medium close-up. Mansour explains, one hand raised in a measured gesture, the other on his cane, his annotated book under his arm. Serious, precise expression. Corridor behind him in soft focus. Warm and cold light mixed.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 1 · Planche 2 · Case 5 — Maya perplexe
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : MAYA, MANSOUR
- Statut : — (non marqué ; débat réel, motif inconnu : C)
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book

Panel: Two-shot. Maya frowns, perplexed, tablet lowered; Mansour answers with a gentle shrug and an open palm, a hint of a smile: nobody knows everything. Neutral corridor background in soft focus.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 1 · Planche 2 · Case 6 — Kerbu, lampe sous le menton
- Ratio : --ar 1:1
- Style : A (contemporain)
- Personnages : KERBU
- Statut : — (non marqué ; réplique poétique [S])
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp

Panel: Close-up of Kerbu's face lit from below by the handheld lamp held under his chin: dramatic up-lighting, deep shadows, intense calm eyes, a slight smile. The background falls into darkness. The lamp lights only his face.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 1 · Planche 2 · Case 7 — Nefertari recadre Kerbu
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : NEFERTARI, KERBU
- Statut : — (non marqué ; case pédagogique [H]/[F]/[S])
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp

Panel: Two-shot. Nefertari, firm but friendly, raises an index finger; Kerbu smiles and raises his sketchbook in a mock gesture of surrender, pencil in hand. Warm light, soft corridor background. Mood: complicity and rigour.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```


## Planche 3 — Immersion dans l'Égypte antique (6 cases)

### Ép. 1 · Planche 3 — Mise en page (rough)
- Ratio : --ar 17:22
- Style : C (reconstitution historique) + A (contemporain)
- Personnages : KERBU
- Grille :
  - Rangée 1 : C1 (1/3 de largeur, case charnière) | C2 grande case (2/3 de largeur)
  - Rangée 2 : C3 | C4
  - Rangée 3 : C5 | C6 (même cadrage, côte à côte : passé / présent)
- Statut : rough de composition uniquement (pas d'image publiable).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[STYLE C] Same comic art as Style A but warmer palette; for antiquity: oil lamps and torchlight, raw
limestone, plain linen clothing; for 20th century scenes: sepia-toned archival look. Thin gold border.

Characters and elements (fixed descriptions):
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp

Panel: Full comic page layout rough, 6 panels in 3 rows with white gutters. Row 1: a narrow panel split in two, a faded painted royal cartouche on the left and the same cartouche fresh and vivid by oil-lamp light on the right; then a large panel of ancient craftsmen working in a sloping rock-cut corridor lit by oil lamps (stonecutter, draughtsman, painter, lamp-bearer). Row 2: a scribe in white linen showing an inscribed limestone flake to a foreman; a painter finishing a red sun disk on the wall, glowing in the lamp light. Row 3: two panels with exactly the same framing side by side: the ancient corridor sloping into darkness with oil lamps, then the same corridor today with LED lights. Thin gold border on the reconstruction panels (row 1 right half, row 2, row 3 left), no border on the last panel.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 17:22
```

### Ép. 1 · Planche 3 · Case 1 — Case charnière : le cartouche, hier et aujourd'hui
- Ratio : --ar 4:3
- Style : C (charnière : moitié gauche en A, moitié droite en C)
- Personnages : KERBU
- Statut : — (non marqué ; cartouche réel [H], reconstitution [F])
- ⚠ Référence obligatoire : cartouche réel de la porte concernée (portes B à F) d'après photographies TMP / Piankoff & Rambova 1954 ; la moitié « fraîche » reprend le même dessin, couleurs ravivées.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[STYLE C] Same comic art as Style A but warmer palette; for antiquity: oil lamps and torchlight, raw
limestone, plain linen clothing; for 20th century scenes: sepia-toned archival look. Thin gold border.

Characters and elements (fixed descriptions):
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp

Panel: Hinge panel split vertically, seamless transition in the middle. Left half (present, Style A, no border): the faded painted cartouche on the tomb wall, Kerbu's hand held a few centimetres away from it, not touching, cold LED light. Right half (antiquity, Style C, thin gold border): the very same cartouche freshly painted, vivid mineral colours on clean white plaster, lit by the warm flickering flame of an oil lamp. Signs inside the cartouche blurred and unreadable (to be copied from reference).

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 1 · Planche 3 · Case 2 — Les artisans au travail
- Ratio : --ar 3:2
- Style : C (Antiquité)
- Personnages : —
- Statut : [F] (individus) ; technique de l'esquisse non vérifiée (N)
- ⚠ Référence obligatoire : architecture du corridor d'après TMP. ⚠ Technique (couleurs de l'esquisse, étapes) à confirmer par D. Laboury et C. A. Keller avant le dessin final ; personnages tous fictifs (aucun ouvrier de KV9 identifié).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[STYLE C] Same comic art as Style A but warmer palette; for antiquity: oil lamps and torchlight, raw
limestone, plain linen clothing; for 20th century scenes: sepia-toned archival look. Thin gold border.

Panel: Large panel, reconstruction of the corridor of the tomb under construction in the 12th century BCE. A long straight sloping rock-cut corridor of raw limestone, lit only by oil lamps. Four craftsmen in plain linen kilts: further down the slope, a stonecutter dressing the rock face with a chisel and mallet; in the middle, a draughtsman tracing a preliminary outline sketch on fresh white plaster (thin neutral lines, colour of the sketch left unspecified); nearer, a painter laying flat colour on a finished section with a brush; in the foreground, a lamp-bearer holding an oil lamp high. Warm palette, smoke and dust in the lamplight. Concentrated, calm work.

Ancient craftsmen at work may touch the fresh plaster with their tools (they are making the tomb); all painted signs stay blurred and unreadable. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 3:2
```

### Ép. 1 · Planche 3 · Case 3 — Le scribe et le chef d'équipe
- Ratio : --ar 4:3
- Style : C (Antiquité)
- Personnages : —
- Statut : [F] (personnages) ; regravure des noms [H]
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[STYLE C] Same comic art as Style A but warmer palette; for antiquity: oil lamps and torchlight, raw
limestone, plain linen clothing; for 20th century scenes: sepia-toned archival look. Thin gold border.

Panel: Medium two-shot in the ancient corridor. A scribe in a white linen kilt, a writing palette tucked under his arm, shows an ostracon (a flat limestone flake with a few ink marks, illegible) to the foreman of the crew, an older muscular man. The scribe looks matter-of-fact, the foreman resolute. Oil-lamp light, warm shadows, raw limestone and fresh plaster behind them.

Ancient craftsmen at work may touch the fresh plaster with their tools (they are making the tomb); all painted signs stay blurred and unreadable. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 1 · Planche 3 · Case 4 — Le peintre et le disque solaire
- Ratio : --ar 4:3
- Style : C (Antiquité)
- Personnages : —
- Statut : [F] (peintre) ; Livre de la Terre en J [H]
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[STYLE C] Same comic art as Style A but warmer palette; for antiquity: oil lamps and torchlight, raw
limestone, plain linen clothing; for 20th century scenes: sepia-toned archival look. Thin gold border.

Panel: Medium shot. A painter in a linen kilt finishes a large red sun disk on the plaster with a brush; the reflection of a nearby oil lamp makes the fresh red paint seem to glow. His face is half lit, absorbed and proud. The surrounding painted figures are only roughed in, blurred.

Ancient craftsmen at work may touch the fresh plaster with their tools (they are making the tomb); all painted signs stay blurred and unreadable. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 1 · Planche 3 · Case 5 — Le corridor antique s'enfonce
- Ratio : --ar 4:3
- Style : C (Antiquité)
- Personnages : —
- Statut : — (non marqué ; reconstitution [F])
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[STYLE C] Same comic art as Style A but warmer palette; for antiquity: oil lamps and torchlight, raw
limestone, plain linen clothing; for 20th century scenes: sepia-toned archival look. Thin gold border.

Panel: Wide shot looking down the axis of the ancient corridor: the long straight slope descending into darkness, small oil lamps placed or carried at intervals, their warm points of light shrinking into the depth. Tiny silhouettes of craftsmen. Strong one-point perspective. Silence and depth.

Ancient craftsmen at work may touch the fresh plaster with their tools (they are making the tomb); all painted signs stay blurred and unreadable. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 1 · Planche 3 · Case 6 — Retour au présent, même pente
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : — · éléments : KV9_CORRIDOR
- Statut : — (non marqué ; [F])
- ⚠ Référence obligatoire : géométrie du corridor (pente, passerelle) d'après photographies TMP — doit correspondre au cadrage de la case 5.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
KV9_CORRIDOR: long straight sloping rock-cut corridor, painted walls with registers of figures, starry astronomical ceiling, modern wooden walkway and handrails

Panel: Exactly the same framing and perspective as the previous panel (ancient corridor), but today: the modern wooden walkway and handrails, the faded paintings, and cold white LED lights of the team in place of the oil lamps, receding down the slope. Kerbu stands small in the middle distance, motionless, as if waking up. No gold border.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```


## Planche 4 — Révélation et suspense (7 cases)

### Ép. 1 · Planche 4 — Mise en page (rough)
- Ratio : --ar 17:22
- Style : A (contemporain) + C (reconstitution historique)
- Personnages : MARSAC, NEFERTARI, KERBU, MANSOUR, MAYA
- Grille :
  - Rangée 1 : C1 | C2
  - Rangée 2 : C3 | C4 (sépia, liseré doré)
  - Rangée 3 : C5 | C6
  - Rangée 4 : C7 bandeau final pleine largeur
- Statut : rough de composition uniquement (pas d'image publiable).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[STYLE C] Same comic art as Style A but warmer palette; for antiquity: oil lamps and torchlight, raw
limestone, plain linen clothing; for 20th century scenes: sepia-toned archival look. Thin gold border.

Characters and elements (fixed descriptions):
MARSAC: Julien Marsac, French man about 50, stubble, swept-back greying hair, sunglasses pushed up on head, expensive linen jacket over a black T-shirt, handheld camera or walkie-talkie
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Panel: Full comic page layout rough, 7 panels in 4 rows with white gutters. Row 1: a man in a linen jacket with a smartphone waiting by the gate of a tomb as dusty explorers come out; the same man pointing down at the entrance of another tomb a few metres below. Row 2: an old man with a cane smiling and holding out an old sepia photograph; a sepia documentary panel of 1922, a man in a hat seen from behind directing workmen clearing rough dry-stone huts at the foot of a tomb entrance. Row 3: a young woman with an incredulous face next to the old man; a Black man alone with a headlamp walking back toward a painted doorway with a sun disk motif above it. Row 4: a wide final banner, close-up of the painted sun disk motif. Empty space for balloons.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 17:22
```

### Ép. 1 · Planche 4 · Case 1 — Marsac attend à la grille
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : MARSAC, NEFERTARI, KERBU, MANSOUR, MAYA
- Statut : [F]
- ⚠ Référence obligatoire : entrée de KV9 et sa grille d'après photographies TMP (décor réel).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MARSAC: Julien Marsac, French man about 50, stubble, swept-back greying hair, sunglasses pushed up on head, expensive linen jacket over a black T-shirt, handheld camera or walkie-talkie
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Panel: Medium-wide shot at the entrance gate of KV9, seen from outside. Julien Marsac waits by the gate; in this panel he holds a smartphone in his hand (instead of the camera), eager grin, sunglasses pushed up on his head. The team comes out through the gate, dusty and tired; Nefertari in front, deadpan. Natural outdoor light on the pale rock of the valley.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 1 · Planche 4 · Case 2 — Marsac montre la tombe de Toutânkhamon
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : MARSAC, MANSOUR, MAYA
- Statut : [H] (décor)
- ⚠ Référence obligatoire : position relative de KV9 et de KV62 et aspect actuel de l'entrée de KV62 : photographies et plan du Theban Mapping Project.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MARSAC: Julien Marsac, French man about 50, stubble, swept-back greying hair, sunglasses pushed up on head, expensive linen jacket over a black T-shirt, handheld camera or walkie-talkie
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Panel: Medium-wide shot. Marsac points excitedly downward at the entrance of the tomb of Tutankhamun (KV62), a few metres below the entrance of KV9; Mansour and Maya look where he points. The layout of the valley floor, paths and the KV62 entrance must follow reference photographs exactly; no invented structures, no signage text.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 1 · Planche 4 · Case 3 — Mansour sort la photo d'archives
- Ratio : --ar 1:1
- Style : A (contemporain)
- Personnages : MANSOUR, MARSAC
- Statut : — (non marqué ; photo réelle [H], sous licence ou redessinée)
- ⚠ Référence obligatoire : photographie d'archives de 1922 sous licence (Griffith Institute, Oxford — fonds Carter/Burton) ou redessin d'après elle. Carter jamais rendu ressemblant.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
MARSAC: Julien Marsac, French man about 50, stubble, swept-back greying hair, sunglasses pushed up on head, expensive linen jacket over a black T-shirt, handheld camera or walkie-talkie

Panel: Close two-shot. Mansour, smiling, holds out an old sepia archival photograph toward Marsac; the photo is seen at an angle, its image soft and indistinct (it will be replaced by a licensed archival photograph or a redrawing). Marsac leans in, curious. Outdoor light. No recognisable historical person in the photo.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 1 · Planche 4 · Case 4 — 4 novembre 1922 : la première hutte
- Ratio : --ar 4:3
- Style : C (1922, sépia)
- Personnages : —
- Statut : [H]
- ⚠ Référence obligatoire : notes de Howard Carter, Griffith Institute TAA i.12.03-04 ; photographies d'époque du secteur KV9/KV62 (Griffith Institute). Personnage historique réel : silhouette de dos uniquement.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[STYLE C] Same comic art as Style A but warmer palette; for antiquity: oil lamps and torchlight, raw
limestone, plain linen clothing; for 20th century scenes: sepia-toned archival look. Thin gold border.

Panel: Sepia documentary panel, archival photographic look, 1922. At the foot of the entrance of KV9, rough dry-stone huts built by the ancient workmen of the tomb; local workmen in period clothing clear the first hut with baskets and hoes; a man in a hat and jacket, seen from behind (silhouette only, no face, no claimed likeness), directs the work; in the cleared ground, the edge of a first rock-cut step begins to appear. Harsh sunlight, pale dust, thin gold border.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 1 · Planche 4 · Case 5 — Maya, incrédule
- Ratio : --ar 1:1
- Style : A (contemporain)
- Personnages : MAYA, MANSOUR
- Statut : — (non marqué ; réplique [H] sourcée GRIFFITH)
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book

Panel: Close two-shot. Maya, incredulous, mouth half open, glasses pushed on her head; Mansour beside her, calm, nodding slowly with a small satisfied smile. Outdoor light, pale rock behind.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 1 · Planche 4 · Case 6 — Kerbu revient vers la porte B
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : KERBU
- Statut : [H]
- ⚠ Référence obligatoire : décor de la porte B (disque solaire, scarabée, dieu à tête de bélier, Isis et Nephthys) : photographies TMP, Piankoff & Rambova 1954.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp

Panel: Medium-wide shot from behind and slightly to the side. Kerbu, alone, walks back to gate B of the tomb and stops about a metre from it. The soft diffuse light of his headlamp reveals the painted motif above the doorway: a sun disk containing a scarab and a ram-headed god, between Isis and Nephthys — painted register with figures, copy the exact composition from reference, do not invent it. Quiet, intimate mood. Empty space for a thought balloon.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 1 · Planche 4 · Case 7 — Gros plan sur le disque (bandeau final)
- Ratio : --ar 3:1
- Style : A (contemporain)
- Personnages : —
- Statut : [H] (image) ; réplique [S]
- ⚠ Référence obligatoire : même décor que la case 6, recadré ; d'après photographie de référence. Le liseré doré « d'une seconde » est un effet de mise en page.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Panel: Wide final banner, tight crop on the painted sun disk motif of gate B (scarab and ram-headed god inside the disk, flanked by two goddesses): painted register with figures, copy from reference. Faded mineral colours on plaster, soft ambient light. At the very edges of the frame only, a faint warm golden glow hints at the mythic world (the gold border is added in the page layout); no light projected on the painting. Mood: revelation, suspense.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 3:1
```


## Page documentaire — Épisode 1 : KV9, un tombeau pour deux rois

### Ép. 1 · Page documentaire — Illustration
- Ratio : --ar 3:1
- Style : A (variante schéma documentaire)
- Personnages : —
- Statut : [H]
- ⚠ Référence obligatoire : plan de KV9 du Theban Mapping Project (salles A à K) ; positions des livres d'après bible/01 §2. Les libellés (noms des salles et des livres) sont posés en mise en page.
- Note : Le générateur ne doit servir qu'à l'ambiance graphique ; le plan lui-même est retracé d'après le TMP (proportions et salles exactes).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Panel: Clean schematic plan of a long straight rock-cut royal tomb seen from above, drawn as a technical illustration on warm off-white paper: entrance, a series of corridors, a square hall with four pillars, further corridors, an antechamber and a vaulted burial chamber with pillars at the far end, all along one straight axis. Thin black ink outlines, light ochre fill, small coloured bands along the walls marking where different painted programmes are (colour-coded, no labels). Generous empty margins for labels. This image is only a draft: the final plan must be traced by hand from the reference plan.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 3:1
```


---

# Épisode 2 — Le plafond des étoiles


## Planche 1 — Découverte archéologique (7 cases)

### Ép. 2 · Planche 1 — Mise en page (rough)
- Ratio : --ar 17:22
- Style : A (contemporain)
- Personnages : MAYA, KERBU, SENSOR, NEFERTARI, MANSOUR
- Grille :
  - Rangée 1 : C1 bandeau pleine largeur
  - Rangée 2 : C2 (2/3 de largeur, contre-plongée) | C3
  - Rangée 3 : C4 | C5
  - Rangée 4 : C6 | C7
- Statut : rough de composition uniquement (pas d'image publiable).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
SENSOR: a small grey environmental sensor box on a tripod with a coloured status LED
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book

Panel: Full comic page layout rough, 7 panels in 4 rows with white gutters. Row 1: a wide night banner inside a painted tomb corridor, a woman adjusting a small sensor on a tripod in the foreground, a painted doorway with a sun disk blurred in the background. Row 2: a low-angle view of four lamps rising toward a dark blue ceiling with rows of painted stars; a close-up of painted stars in rows beside small figures. Row 3: a woman setting up a small projector and a white folding screen, an old man watching; a close-up of the screen showing ceiling figures aligned in rows with coloured digital markers. Row 4: a woman with glasses approaching the screen; a Black man further down the slope lifting his lamp toward the ceiling and beckoning.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 17:22
```

### Ép. 2 · Planche 1 · Case 1 — Nuit 2 : Maya règle le capteur
- Ratio : --ar 3:1
- Style : A (contemporain)
- Personnages : MAYA, KERBU, SENSOR
- Statut : [F]
- ⚠ Référence obligatoire : porte B vue de l'intérieur (décor flou) d'après photographies TMP.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
SENSOR: a small grey environmental sensor box on a tripod with a coloured status LED

Panel: Night. Wide banner inside corridor B looking back toward gate B: the painted sun disk motif of the doorway is in the background, deliberately out of focus. In the foreground, Maya adjusts the sensor on its tripod (LED green), standing on the walkway; Kerbu, a step behind, tilts his head with a puzzled, amused look. Cold LED light, warm headlamps.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 3:1
```

### Ép. 2 · Planche 1 · Case 2 — Les quatre lampes se lèvent
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA
- Statut : [H]
- ⚠ Référence obligatoire : plafond du corridor B (constellations circumpolaires et décans) : Piankoff & Rambova 1954 et photographies TMP. Disposition des figures à recopier, jamais à inventer.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Panel: Dramatic low-angle shot from the walkway floor looking up. The four team members raise their lamps together toward the ceiling of corridor B; soft diffuse light gently reveals a dark blue field with rows of painted stars and astronomical figures: painted ceiling with figures, copy from reference, do not invent the arrangement. Faces lit from below, awe.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 2 · Planche 1 · Case 3 — Étoiles en rangées
- Ratio : --ar 1:1
- Style : A (contemporain)
- Personnages : —
- Statut : [H]
- ⚠ Référence obligatoire : détail du plafond du corridor B d'après photographie publiée (TMP / Piankoff & Rambova 1954).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Panel: Close-up of a section of the painted ceiling: small painted stars aligned in rows on a dark blue ground, next to small figures — copy from reference. Visible plaster texture, cracks, faded pigment. Soft ambient light. No numbers, no labels.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 2 · Planche 1 · Case 4 — Maya installe l'écran, dos à la paroi
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : MAYA, MANSOUR
- Statut : [F]
- Note : Règle de conservation visible : aucune lumière projetée sur les peintures.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book

Panel: Medium shot. Maya sets up a small portable projector and a white folding screen on the walkway; the screen stands with its back to the wall, a clear gap between them, and the projector points at the screen, away from the paintings. On the screen: her photographic survey of the ceiling (soft, blurred image). Mansour watches, leaning on his cane, with an amused, nostalgic smile.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 2 · Planche 1 · Case 5 — L'écran : les figures redressées
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : —
- Statut : [F] (interface) / [H] (figures copiées)
- ⚠ Référence obligatoire : figures du plafond de B d'après photographie publiée ; l'interface est fictive.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Panel: Close-up on the white folding screen: the ceiling figures, digitally straightened, appear in regular rows; thin coloured contemporary digital markers (circles, outlines) surround groups of stars. The figures themselves are copied from reference; no text, no numbers, no interface labels. The edges of the screen frame are visible.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 2 · Planche 1 · Case 6 — Nefertari s'approche de l'écran
- Ratio : --ar 1:1
- Style : A (contemporain)
- Personnages : NEFERTARI, MAYA
- Statut : — (non marqué ; réplique [H] sourcée TMP)
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Panel: Medium close shot. Nefertari, the loupe hanging around her neck, steps closer to the screen with professional interest; Maya, beside her, looks blank and curious. The screen's light on their faces.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 2 · Planche 1 · Case 7 — Kerbu, plus loin dans la pente
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : KERBU, MAYA, NEFERTARI
- Statut : [H]
- ⚠ Référence obligatoire : plafonds astronomiques des corridors C et D : photographies TMP / Piankoff & Rambova 1954.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck

Panel: Medium-wide shot down the slope. Kerbu stands a few metres further down the corridor, lamp raised toward the painted ceiling of corridor C, which continues toward corridor D; he turns back and beckons the others with his free hand. Maya and Nefertari, small, upslope near the screen. Ceiling: painted ceiling with figures, copy from reference.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```


## Planche 2 — Analyse d'une inscription (7 cases)

### Ép. 2 · Planche 2 — Mise en page (rough)
- Ratio : --ar 17:22
- Style : A (contemporain)
- Personnages : NEFERTARI, MAYA, MANSOUR, MARSAC, KERBU
- Grille :
  - Rangée 1 : C1 | C2
  - Rangée 2 : C3 petite case en incrustation (cadre « écran ») | C4
  - Rangée 3 : C5 grande case pleine largeur
  - Rangée 4 : C6 (avec incrustation carnet) | C7
- Statut : rough de composition uniquement (pas d'image publiable).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
MARSAC: Julien Marsac, French man about 50, stubble, swept-back greying hair, sunglasses pushed up on head, expensive linen jacket over a black T-shirt, handheld camera or walkie-talkie
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp

Panel: Full comic page layout rough, 7 panels in 4 rows with white gutters. Row 1: a woman with glasses pointing at a row of stars on a white screen while a younger woman listens; an old man pointing at a small seated figure under a grid of stars on the screen. Row 2: a small inset panel framed like a monitor screen, a man in a linen jacket shouting into a walkie-talkie in front of a field monitor; the woman with glasses holding the walkie-talkie, patient and firm. Row 3: a large full-width panel, lamps revealing on a dark blue ceiling two immense legs of a star-covered female figure, explorers small below. Row 4: a Black man with his head tilted back following the figure, with a small sketchbook-style diagram inset; the woman pointing up at the area under the legs, the Black man intrigued.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 17:22
```

### Ép. 2 · Planche 2 · Case 1 — Nefertari explique les décans
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : NEFERTARI, MAYA
- Statut : [H]
- ⚠ Référence obligatoire : figures projetées = plafond de B d'après photographie publiée (TMP / Piankoff & Rambova 1954).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Panel: Medium two-shot in front of Maya's white screen. Nefertari points at a row of stars on the screen (never at the ceiling itself), in a lively teaching pose, lightly smiling; Maya listens, intrigued. Screen light, warm headlamps. Screen figures copied from reference, no labels.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 2 · Planche 2 · Case 2 — Mansour et l'horloge stellaire
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : MANSOUR, MAYA
- Statut : [H]
- ⚠ Référence obligatoire : horloge stellaire (homme assis sous une grille d'étoiles) de KV9 — corridors B, C ou côtés de F — d'après photographie publiée ; ne pas inventer la grille.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Panel: Medium shot. Mansour points at the screen with his finger: on it, a small seated man under a grid of stars (a star clock), copied from reference, slightly soft. Maya leans in, half amused, half impressed. No explanation drawn, no labels.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 2 · Planche 2 · Case 3 — Marsac au moniteur (incrustation)
- Ratio : --ar 1:1
- Style : A (contemporain)
- Personnages : MARSAC
- Statut : [F]
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MARSAC: Julien Marsac, French man about 50, stubble, swept-back greying hair, sunglasses pushed up on head, expensive linen jacket over a black T-shirt, handheld camera or walkie-talkie

Panel: Small inset panel framed like a screen (rounded corners, faint scanlines). At the tomb entrance at night, Marsac sits in front of a field monitor showing a blurred live feed of the starry ceiling; he holds a walkie-talkie to his mouth, eyes wide, excited, gesturing with his free hand. Cold monitor glow on his face.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 2 · Planche 2 · Case 4 — Nefertari prend le talkie
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : NEFERTARI, MAYA
- Statut : — (non marqué ; théorie de Marsac N, écartée)
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Panel: Medium shot. Nefertari has taken the walkie-talkie and speaks into it, patient but firm, her other hand on her hip; Maya, beside her, suppresses a smile. Background: the screen and the corridor in soft focus.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 2 · Planche 2 · Case 5 — Les jambes de Nout
- Ratio : --ar 3:2
- Style : A (contemporain)
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA · éléments : KV9_CORRIDOR
- Statut : [H]
- ⚠ Référence obligatoire : plafond du corridor D (jambes de Nout au-dessus du début du Livre du Jour et de la fin du Livre de la Nuit) : photographies TMP, Piankoff & Rambova 1954.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
KV9_CORRIDOR: long straight sloping rock-cut corridor, painted walls with registers of figures, starry astronomical ceiling, modern wooden walkway and handrails

Panel: Large panel, low angle in corridor D. The team's soft lamp light reveals on the dark blue ceiling two immense legs: a star-covered female figure that begins here and stretches on toward the depths of the tomb. Painted ceiling with figures, copy from reference: orientation and proportions of the goddess must not be invented. The four team members are small below, heads tilted back; Kerbu raises a hand toward it without touching anything. Mood: awe.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 3:2
```

### Ép. 2 · Planche 2 · Case 6 — Kerbu suit le corps de la déesse
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : KERBU, MANSOUR
- Statut : [H]
- ⚠ Référence obligatoire : répartition D (jambes) → E (Livres du Jour et de la Nuit) → F (tête et bras) d'après TMP.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book

Panel: Medium shot. Kerbu, head thrown back, follows the goddess's body along the ceiling toward the slope; Mansour beside him on his cane. Small inset in a corner drawn in the style of Kerbu's sketchbook (pencil on cream paper): a simple long section of three ceiling zones in a row with a tiny stick figure of the goddess stretched across them — no letters, no words (labels added in lettering).

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 2 · Planche 2 · Case 7 — Sous les jambes de Nout
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : NEFERTARI, KERBU
- Statut : [H]
- ⚠ Référence obligatoire : plafond de D : début du Livre du Jour / fin du Livre de la Nuit sous les jambes de Nout (TMP, Piankoff & Rambova 1954).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp

Panel: Medium two-shot looking up. Nefertari points upward from a distance at the ceiling area beneath the goddess's legs, where painted registers begin (copy from reference); Kerbu, intrigued, follows her finger with his eyes. Soft lamp light, dark blue ceiling.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```


## Planche 3 — Immersion dans l'Égypte antique (7 cases)

### Ép. 2 · Planche 3 — Mise en page (rough)
- Ratio : --ar 17:22
- Style : B (mythologique, liseré doré) + A (contemporain)
- Personnages : KERBU, NEFERTARI
- Grille :
  - Rangée 1 : C1 (1/3 de largeur, case charnière) | C2 grande case (2/3 de largeur, ≈ 1/3 de la planche)
  - Rangée 2 : C3 | C4 | C5
  - Rangée 3 : C6 (2/3 de largeur, plan large) | C7 (1/3, retour au présent)
- Statut : rough de composition uniquement (pas d'image publiable).
- Prompt :
```
[STYLE B] Ancient Egyptian New Kingdom tomb painting style, flat mineral colours (red ochre, yellow
ochre, Egyptian blue, malachite green, carbon black, lime white), bold black outlines, figures in strict
profile with frontal eye and shoulders, Egyptian canon of proportions, horizontal registers, no
perspective, no shading, thin gold border around the panel.

[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck

Panel: Full comic page layout rough, 7 panels in 3 rows with white gutters, mostly in Egyptian mural style with thin gold borders. Row 1: a narrow hinge panel where a painted dark blue ceiling opens into a stylised night sky; a large panel with a horizon line and the sky goddess arched over it, star-covered, a red-gold sun disk descending toward her mouth. Row 2: close-up of the disk entering her mouth; the dark blue starry inside of her body with a small barque gliding; a ram-headed god standing in the barque. Row 3: a wide panel of the goddess's body spanning the whole sky with a faint glow near her hands; then the painted ceiling of the tomb today in LED light, no gold border.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 17:22
```

### Ép. 2 · Planche 3 · Case 1 — Case charnière : le plafond s'ouvre
- Ratio : --ar 4:3
- Style : B (charnière : partie gauche en A)
- Personnages : —
- Statut : [S]
- ⚠ Référence obligatoire : plafond de D d'après photographies TMP / Piankoff & Rambova 1954 (moitié gauche).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[STYLE B] Ancient Egyptian New Kingdom tomb painting style, flat mineral colours (red ochre, yellow
ochre, Egyptian blue, malachite green, carbon black, lime white), bold black outlines, figures in strict
profile with frontal eye and shoulders, Egyptian canon of proportions, horizontal registers, no
perspective, no shading, thin gold border around the panel.

Panel: Hinge panel. Left part (present, Style A): the painted dark blue ceiling of corridor D in dim LED light, painted ceiling with figures, copy from reference. Right part (Style B, thin gold border): the same dark blue opens into a stylised night sky, the painted stars start to twinkle as flat five-pointed Egyptian stars. Seamless transition between the two.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 2 · Planche 3 · Case 2 — Nout et le disque du soir
- Ratio : --ar 3:2
- Style : B (mythologique, liseré doré)
- Personnages : — · éléments : NUT
- Statut : [S]
- ⚠ Référence obligatoire : silhouette de Nout copiée d'après les plafonds publiés (Piankoff & Rambova 1954). Montage symbolique : ne pas présenter comme une paroi précise de KV9.
- Prompt :
```
[STYLE B] Ancient Egyptian New Kingdom tomb painting style, flat mineral colours (red ochre, yellow
ochre, Egyptian blue, malachite green, carbon black, lime white), bold black outlines, figures in strict
profile with frontal eye and shoulders, Egyptian canon of proportions, horizontal registers, no
perspective, no shading, thin gold border around the panel.

Characters and elements (fixed descriptions):
NUT: elongated woman arched over the scene, body covered with stars, dark blue background

Panel: Large panel. A stylised flat landscape: a simple horizon line; above it, the sky goddess Nut arched over the world, resting on her toes and fingertips, her elongated body covered with stars on a dark blue ground. A red-gold sun disk descends toward her mouth. Strict profile, flat colours, black outlines, no perspective. Leave a band free for a caption.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 3:2
```

### Ép. 2 · Planche 3 · Case 3 — Le disque entre dans la bouche de Nout
- Ratio : --ar 1:1
- Style : B (mythologique, liseré doré)
- Personnages : — · éléments : NUT
- Statut : [S]
- ⚠ Référence obligatoire : motif « Nout sur le point d'avaler le disque » (Livres du Jour et de la Nuit) d'après une reproduction publiée ; ne pas le situer dans « ce corridor ».
- Prompt :
```
[STYLE B] Ancient Egyptian New Kingdom tomb painting style, flat mineral colours (red ochre, yellow
ochre, Egyptian blue, malachite green, carbon black, lime white), bold black outlines, figures in strict
profile with frontal eye and shoulders, Egyptian canon of proportions, horizontal registers, no
perspective, no shading, thin gold border around the panel.

Characters and elements (fixed descriptions):
NUT: elongated woman arched over the scene, body covered with stars, dark blue background

Panel: Close-up in mural style: the red sun disk entering the mouth of the goddess Nut in profile; the edge of the disk dissolves into the dark blue of her star-covered body. Flat colours, bold outlines.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 2 · Planche 3 · Case 4 — Dans le corps de Nout
- Ratio : --ar 1:1
- Style : B (mythologique, liseré doré)
- Personnages : —
- Statut : [S]
- Prompt :
```
[STYLE B] Ancient Egyptian New Kingdom tomb painting style, flat mineral colours (red ochre, yellow
ochre, Egyptian blue, malachite green, carbon black, lime white), bold black outlines, figures in strict
profile with frontal eye and shoulders, Egyptian canon of proportions, horizontal registers, no
perspective, no shading, thin gold border around the panel.

Panel: Inside the body of Nut: a deep night-blue space filled with flat painted stars arranged in loose rows; the sun disk has become a small barque in strict profile, gliding between the stars. Flat colours, no perspective, thin gold border.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 2 · Planche 3 · Case 5 — Le dieu à tête de bélier dans la barque
- Ratio : --ar 1:1
- Style : B (mythologique, liseré doré)
- Personnages : — · éléments : RE_NIGHT
- Statut : [S]
- ⚠ Référence obligatoire : figure de Rê nocturne à tête de bélier copiée d'après une figure publiée (bible 03 §1). Montage [S] : Nout et la barque nocturne viennent de livres différents.
- Prompt :
```
[STYLE B] Ancient Egyptian New Kingdom tomb painting style, flat mineral colours (red ochre, yellow
ochre, Egyptian blue, malachite green, carbon black, lime white), bold black outlines, figures in strict
profile with frontal eye and shoulders, Egyptian canon of proportions, horizontal registers, no
perspective, no shading, thin gold border around the panel.

Characters and elements (fixed descriptions):
RE_NIGHT: ram-headed sun god standing in a shrine on a solar barque

Panel: In the barque, standing, the night sun god with a ram's head, in strict Egyptian profile, flat colours, bold black outlines, mural style, against the dark blue starry ground.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 2 · Planche 3 · Case 6 — Le corps de Nout traverse le ciel
- Ratio : --ar 4:3
- Style : B (mythologique, liseré doré)
- Personnages : — · éléments : NUT
- Statut : [S]
- Prompt :
```
[STYLE B] Ancient Egyptian New Kingdom tomb painting style, flat mineral colours (red ochre, yellow
ochre, Egyptian blue, malachite green, carbon black, lime white), bold black outlines, figures in strict
profile with frontal eye and shoulders, Egyptian canon of proportions, horizontal registers, no
perspective, no shading, thin gold border around the panel.

Characters and elements (fixed descriptions):
NUT: elongated woman arched over the scene, body covered with stars, dark blue background

Panel: Wide shot in mural style: the elongated star-covered body of Nut stretches across the whole sky from one edge of the panel to the other; the tiny barque is in the middle of her body; at the far end, near her hands, a barely visible glow of light. Flat colours, horizontal composition.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 2 · Planche 3 · Case 7 — Retour au présent : Nout peinte au plafond de D
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : KERBU, NEFERTARI · éléments : KV9_CORRIDOR
- Statut : — (non marqué ; plafond réel [H])
- ⚠ Référence obligatoire : plafond de D d'après photographies TMP / Piankoff & Rambova 1954.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
KV9_CORRIDOR: long straight sloping rock-cut corridor, painted walls with registers of figures, starry astronomical ceiling, modern wooden walkway and handrails

Panel: Same horizontal composition as the previous panel, but today: the body of Nut painted on the ceiling of corridor D (painted ceiling with figures, copy from reference), in the dim light of the team's LEDs. Kerbu below, lamp relit, looking up with a faint smile; Nefertari a few steps behind, arms crossed. No gold border.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```


## Planche 4 — Révélation et suspense (8 cases)

### Ép. 2 · Planche 4 — Mise en page (rough)
- Ratio : --ar 17:22
- Style : A (contemporain)
- Personnages : NEFERTARI, KERBU, MAYA, MANSOUR, SENSOR
- Grille :
  - Rangée 1 : C1 | C2
  - Rangée 2 : C3 grande case pleine largeur
  - Rangée 3 : C4 | C5
  - Rangée 4 : C6 | C7 (rangée compacte)
  - Rangée 5 : C8 bandeau final pleine largeur (étroit)
- Statut : rough de composition uniquement (pas d'image publiable).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
SENSOR: a small grey environmental sensor box on a tripod with a coloured status LED

Panel: Full comic page layout rough, 8 panels in 5 rows with white gutters. Row 1: explorers' lamps sweeping a painted wall with superposed registers, painted doors and a barque; an old man with a cane pointing toward painted goddesses and a long serpent. Row 2: a large full-width panel, the team in silhouette, back to the viewer, stopped in silence before a painted scene. Row 3: close-up of a Black man's face in cold light; a woman with glasses, arms crossed, wry smile. Row 4: a small sensor on a tripod with an orange light; the Black man turning back while climbing, his lamp beam running far down the axis of the corridor. Row 5: a narrow final banner, a woman's head and starry arms barely visible on a distant ceiling.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 17:22
```

### Ép. 2 · Planche 4 · Case 1 — Corridor C : la paroi sud
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : NEFERTARI, KERBU, MAYA · éléments : KV9_CORRIDOR
- Statut : [H]
- ⚠ Référence obligatoire : paroi sud du corridor C : Livre des Portes, divisions 3-5, 3 registres, barque au registre central — photographies TMP / Piankoff & Rambova 1954.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
KV9_CORRIDOR: long straight sloping rock-cut corridor, painted walls with registers of figures, starry astronomical ceiling, modern wooden walkway and handrails

Panel: Medium-wide shot back in corridor C. The team's soft lamp light sweeps the south wall (on the left when walking down): superposed painted registers, painted doors and a barque in the middle register — painted register with figures, copy from reference. Nefertari, in front, gestures along the wall from a distance; the others follow. Sense of time pressure.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 2 · Planche 4 · Case 2 — Les déesses des heures et le serpent
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : MANSOUR, MAYA
- Statut : [H]
- ⚠ Référence obligatoire : déesses des heures et serpent qui avale les heures (corridor C) : photographies TMP / Piankoff & Rambova 1954.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Panel: Medium shot. Mansour, leaning on his cane, points with his hand (cane on the floor, well away from the wall) toward painted figures of goddesses and a long serpent on the wall: painted register with figures, copy from reference. Maya beside him, wry expression.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 2 · Planche 4 · Case 3 — La salle du jugement d'Osiris
- Ratio : --ar 3:2
- Style : A (contemporain)
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA
- Statut : [H]
- ⚠ Référence obligatoire : salle du jugement d'Osiris (5ᵉ porte du Livre des Portes, corridor C) : EXCLUSIVEMENT d'après Piankoff & Rambova 1954 / photographies TMP. La bible ne décrit pas la scène : rien de mémoire.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Panel: Large panel, the lamps have stopped. In the foreground, the four team members in dark silhouette, backs to the viewer, standing still at a respectful distance. Before them, on the wall, the painted scene of the judgment hall: painted register with figures, copy exclusively from reference — do not add, imagine or arrange any element of the scene. Heavy silence, cold light, dust in the air.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 3:2
```

### Ép. 2 · Planche 4 · Case 4 — Kerbu : faut-il être jugé ?
- Ratio : --ar 1:1
- Style : A (contemporain)
- Personnages : KERBU
- Statut : — (non marqué ; question [S])
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp

Panel: Close-up of Kerbu's face in cold white light, grave, questioning, eyes still fixed on the wall off-panel. Background dark.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 2 · Planche 4 · Case 5 — Nefertari, bras croisés
- Ratio : --ar 1:1
- Style : A (contemporain)
- Personnages : NEFERTARI, MANSOUR
- Statut : — (non marqué ; [F])
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book

Panel: Medium close shot. Nefertari, arms crossed, a wry half-smile; behind her, slightly out of focus, Mansour on his cane, benevolent.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 2 · Planche 4 · Case 6 — Le capteur passe à l'orange
- Ratio : --ar 1:1
- Style : A (contemporain)
- Personnages : SENSOR, MAYA
- Statut : — (non marqué ; [F])
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
SENSOR: a small grey environmental sensor box on a tripod with a coloured status LED
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Panel: Close shot of the sensor on its tripod, standing on the walkway higher up the slope: its status LED has turned from green to orange. Out of focus behind it, Maya glances at her watch. Cold light, small orange glow.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 2 · Planche 4 · Case 7 — Kerbu se retourne une dernière fois
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : KERBU · éléments : KV9_CORRIDOR
- Statut : — (non marqué ; [F])
- ⚠ Référence obligatoire : enfilade D → E → F d'après plan et photographies TMP.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
KV9_CORRIDOR: long straight sloping rock-cut corridor, painted walls with registers of figures, starry astronomical ceiling, modern wooden walkway and handrails

Panel: Medium-wide shot. Kerbu, already climbing back up the walkway, turns round one last time; his lamp beam runs straight down the axis of the tomb, beyond corridors D and E, toward the distant ceiling of the pillared hall far below, the light fading softly with distance (no spotlight on the paintings). Strong one-point perspective.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 2 · Planche 4 · Case 8 — Au bout du faisceau : la tête de Nout
- Ratio : --ar 3:1
- Style : A (contemporain)
- Personnages : —
- Statut : [H]
- ⚠ Référence obligatoire : plafond de la salle à piliers F : tête et bras de Nout — photographies TMP / Piankoff & Rambova 1954.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Panel: Narrow final banner. At the far end of the dim beam, barely visible in the darkness, the ceiling of the four-pillared hall F: a woman's head and star-covered arms painted on dark blue — painted ceiling with figures, copy from reference. Very low light, mysterious. A faint warm golden glow at the frame edges only (the gold border flicker is added in the page layout).

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 3:1
```


## Page documentaire — Épisode 2 : Lire un plafond égyptien

### Ép. 2 · Page documentaire — Illustration
- Ratio : --ar 3:1
- Style : A (variante schéma documentaire)
- Personnages : —
- Statut : [H]
- ⚠ Référence obligatoire : coupe et plan TMP des corridors B à F ; répartition des décors d'après bible/01 §2 et l'épisode. Figures d'étoiles redessinées d'après photographies, jamais inventées.
- Note : Le générateur ne fournit que le fond graphique ; les zones B-C (étoiles, décans), D (jambes de Nout), E (Jour et Nuit), F (tête et bras de Nout, horloges sur les côtés) sont dessinées à la main d'après photographies.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Panel: Clean schematic longitudinal section of a straight sloping rock-cut tomb corridor, from the entrance down to a four-pillared hall, drawn as a technical illustration on warm off-white paper: thin black ink outline of floor and ceiling, five consecutive zones marked by small vertical ticks. Along the ceiling line, five empty rectangular bands in pale dark-blue wash where the decoration will be redrawn by hand (no figures generated). Generous empty margins for labels. Draft look only.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 3:1
```


---

# Épisode 3 — Le livre sans commencement


## Planche 1 — Découverte archéologique (7 cases)

### Ép. 3 · Planche 1 — Mise en page (rough)
- Ratio : --ar 17:22
- Style : A (contemporain)
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA
- Grille :
  - Colonne gauche : C1 bandeau vertical pleine hauteur (1/3 de largeur)
  - Colonne droite, rangée 1 : C2 | C3
  - Colonne droite, rangée 2 : C4 grande case
  - Colonne droite, rangée 3 : C5 | C6
  - Colonne droite, rangée 4 : C7
- Statut : rough de composition uniquement (pas d'image publiable).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Panel: Full comic page layout rough, 7 panels with white gutters. Left column, full page height: a tall vertical panel, plunging perspective down a long straight sloping tomb corridor, four lamps in single file getting smaller. Right column: an old man out of breath with a cane stopping in a painted corridor, a young woman urging him on; the threshold of a vaulted burial chamber with four pillars at the front and a dark sarcophagus mass at the back; a large panel, lamps rising toward a vault with two large back-to-back sky goddesses, walls covered with painted scenes; a woman with glasses with an open hand toward the walls; a woman deploying a scanner on a pole, tablet in hand; the scanner sweeping a painted wall with a faint pale red line.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 17:22
```

### Ép. 3 · Planche 1 · Case 1 — La descente en file indienne
- Ratio : --ar 2:3
- Style : A (contemporain)
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA · éléments : KV9_CORRIDOR
- Statut : [H] (décor)
- ⚠ Référence obligatoire : axe rectiligne de KV9 (env. 290°) : plan, coupe et photographies TMP.
- Note : « Bandeau vertical pleine hauteur » : --ar 2:3 d'après le guide ; pour une colonne très étroite, passer à --ar 1:2 ou 9:22.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
KV9_CORRIDOR: long straight sloping rock-cut corridor, painted walls with registers of figures, starry astronomical ceiling, modern wooden walkway and handrails

Panel: Tall vertical panel (full page height), plunging perspective from the top of the slope down the perfectly straight axis of the tomb, more than a hundred metres long, heading west. The four lamps of the team in single file, getting smaller and smaller toward the depths. Painted walls on both sides out of focus, dark blue ceilings. Vertigo, depth, silence.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 2:3
```

### Ép. 3 · Planche 1 · Case 2 — Mansour, essoufflé
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : MANSOUR, MAYA
- Statut : [F]
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Panel: Medium shot in a corridor. Mansour, out of breath, stops and leans on his cane, casting a regretful glance at the painted walls they are passing (blurred). Maya, a few steps further down, turns back to him, encouraging but impatient, equipment on her shoulder.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 3 · Planche 1 · Case 3 — Le seuil de la chambre J
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : KERBU, MANSOUR · éléments : KV9_J
- Statut : [H]
- ⚠ Référence obligatoire : chambre J (voûte, 4 piliers à l'avant dont le 1ᵉʳ et le 4ᵉ inachevés, sarcophage restauré) : photographies TMP ; sarcophage : ARCE (détails réservés à l'épisode 9).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
KV9_J: vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Panel: Medium-wide shot from the threshold of the burial chamber J. A vaulted chamber with four pillars at the front; the first and fourth pillars are not fully freed from the bedrock (copy from reference). At the back, the dark mass of the restored sarcophagus, without detail. Kerbu and Mansour, seen from behind, stop on the threshold. Soft LED light, awe.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 3 · Planche 1 · Case 4 — Deux Nout sur la voûte
- Ratio : --ar 3:2
- Style : A (contemporain)
- Personnages : MAYA, NEFERTARI, KERBU, MANSOUR · éléments : KV9_J
- Statut : [H]
- ⚠ Référence obligatoire : voûte de J : deux Nout dos à dos encadrant les Livres du Jour et de la Nuit — Piankoff & Rambova 1954, photographies TMP.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
KV9_J: vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Panel: Large panel, low angle inside chamber J. The team's lamps rise slowly toward the vault: two large back-to-back silhouettes of the sky goddess on the vaulted ceiling, then the walls covered with scenes (disks, bodies, figures). Vault and walls rendered as painted ceiling and painted registers with figures, copy from reference: the composition of the vault must not be invented. Maya, whispering, eyes wide; Nefertari calm.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 3:2
```

### Ép. 3 · Planche 1 · Case 5 — Nefertari : le Livre de la Terre
- Ratio : --ar 1:1
- Style : A (contemporain)
- Personnages : NEFERTARI · éléments : KV9_J
- Statut : [H]
- ⚠ Référence obligatoire : parois de J (Livre de la Terre) d'après photographies TMP / Piankoff & Rambova 1954.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
KV9_J: vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Panel: Medium close shot. Nefertari, speaking low, turns her open hand toward the four walls of the chamber from the centre of the room, far from them. Behind her, the painted walls (Book of the Earth) soft and out of focus. Reverent mood.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 3 · Planche 1 · Case 6 — Maya déploie son scanner
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : MAYA, KERBU
- Statut : [F] (appareil)
- ⚠ Référence obligatoire : décor de fond : chambre J (TMP).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp

Panel: Medium shot. Maya extends her portable 3D scanner on its pole; on her tablet, four empty grey rectangles in a row (no words, the labels are added in lettering). Kerbu beside her, eager, notebook open. Cold LED light.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 3 · Planche 1 · Case 7 — Le scan de la paroi nord
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : MAYA
- Statut : [F]
- ⚠ Référence obligatoire : paroi nord de J (partie A du Livre de la Terre) d'après photographies TMP / Piankoff & Rambova 1954.
- Note : Le script prévoit un trait laser « rouge pâle, faible » : le garder à peine visible (exception encadrée à la règle « pas de projection lumineuse »).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Panel: Medium-wide shot. Maya holds the scanner pole at a distance from the north wall; a very faint, thin, pale red laser line runs across the painted scene (low intensity, barely visible). The wall: painted register with figures, copy from reference. Concentration, the hum of machinery suggested by lines of motion only.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```


## Planche 2 — Analyse d'une inscription (7 cases)

### Ép. 3 · Planche 2 — Mise en page (rough)
- Ratio : --ar 17:22
- Style : A (contemporain)
- Personnages : MANSOUR, KERBU, NEFERTARI, MAYA
- Grille :
  - Rangée 1 : C1 | C2
  - Rangée 2 : C3
  - Rangée 3 : C4 case-frise (2/3 de largeur) | C5
  - Rangée 4 : C6 suite de la frise (2/3 de largeur) | C7
- Statut : rough de composition uniquement (pas d'image publiable).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Panel: Full comic page layout rough, 7 panels in 4 rows with white gutters. Row 1: an old man sitting on an equipment crate taking a large bound volume from his satchel; close-up of the open book with pencil scribbles in the margin and his raised finger. Row 2: a Black man leaning over the old man's shoulder as he gently closes the book. Row 3: a documentary frieze on aged paper with three empty vignettes linked by a timeline; a woman with glasses, ironic, half-figure. Row 4: the frieze continued with two smaller empty vignettes; the Black man standing pensive before a painted wall, the woman beside him. Empty bands left for captions.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 17:22
```

### Ép. 3 · Planche 2 · Case 1 — Mansour sort le Piankoff
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : MANSOUR · éléments : KV9_J
- Statut : [F] (exemplaire annoté) / [H] (le livre)
- ⚠ Référence obligatoire : aspect de l'ouvrage réel : A. Piankoff & N. Rambova, The Tomb of Ramesses VI, Bollingen Series XL-1, 1954 (numérisation [ARCHIVE]) — format et reliure.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
KV9_J: vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Panel: Medium shot in chamber J. Mansour sits on a metal equipment crate and takes from his leather satchel a large, heavy bound volume, its pages full of pencil annotations; tender, almost ceremonial gesture. Soft LED light.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 3 · Planche 2 · Case 2 — Le livre ouvert, une note dans la marge
- Ratio : --ar 1:1
- Style : A (contemporain)
- Personnages : MANSOUR
- Statut : [H]
- ⚠ Référence obligatoire : mise en page d'une double page de Piankoff & Rambova 1954 [ARCHIVE] (sans texte lisible).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book

Panel: Close-up on the open book on Mansour's knees: printed text columns and a plate, all blurred and unreadable; in the margin, a handwritten pencil note rendered as illegible scribbles. Mansour's raised index finger enters the frame. Warm light on the paper.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 3 · Planche 2 · Case 3 — Kerbu par-dessus l'épaule
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : KERBU, MANSOUR
- Statut : — (non marqué ; [F])
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book

Panel: Medium two-shot. Kerbu leans over Mansour's shoulder, curious; Mansour gently closes the large book, a mysterious half-smile. Chamber J soft in the background.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 3 · Planche 2 · Case 4 — Case-frise : trois noms
- Ratio : --ar 3:1
- Style : A (variante fiche documentaire)
- Personnages : —
- Statut : [H] (contenu des cartouches)
- ⚠ Référence obligatoire : dates et noms (1946, 1953, 1972) d'après L. Pleuger 2020, p. 45-46 — posés au lettrage.
- Note : Ratio de bandeau retenu pour une case-frise (le script ne précise pas le format).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Panel: Documentary-sheet style panel: aged cream paper background, a thin horizontal timeline in sepia ink linking three empty rounded vignette frames evenly spaced; inside each vignette, a small neutral pictogram of an open book; empty bands under each vignette reserved for captions. No portraits, no words, no dates.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 3:1
```

### Ép. 3 · Planche 2 · Case 5 — Nefertari, ironique
- Ratio : --ar 1:1
- Style : A (contemporain)
- Personnages : NEFERTARI, MAYA
- Statut : — (non marqué ; réplique [H] sourcée DARNELL/PLEUGER)
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Panel: Half-figure of Nefertari, ironic smile, eyebrow raised, standing as if in the middle of the documentary frieze (aged paper background behind her); Maya small at the side, questioning.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 3 · Planche 2 · Case 6 — Suite de la frise : deux vignettes
- Ratio : --ar 3:1
- Style : A (variante fiche documentaire)
- Personnages : —
- Statut : [H] (contenu des cartouches)
- ⚠ Référence obligatoire : Roberson 2012 et Darnell & Darnell 2018 (bible 02) — libellés posés au lettrage.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Panel: Continuation of the documentary frieze on aged cream paper: the same thin sepia timeline, two smaller empty rounded vignettes, each with a small neutral pictogram of a book (one of them a stack of books to suggest a plural title); empty bands for captions. No words, no dates, no portraits.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 3:1
```

### Ép. 3 · Planche 2 · Case 7 — Kerbu devant la paroi nord
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : KERBU, NEFERTARI
- Statut : [S]
- ⚠ Référence obligatoire : paroi nord de J d'après photographies TMP / Piankoff & Rambova 1954.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck

Panel: Medium shot. Kerbu stands pensive about a metre from the north wall of chamber J, hands behind his back; Nefertari next to him, amused and sceptical. The wall: painted register with figures, copy from reference, slightly soft.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```


## Planche 3 — Immersion : l'expédition Piankoff, 1949-1951 (7 cases)

### Ép. 3 · Planche 3 — Mise en page (rough)
- Ratio : --ar 17:22
- Style : C (reconstitution historique) + A (contemporain)
- Personnages : MANSOUR
- Grille :
  - Rangée 1 : C1 (1/3 de largeur, case charnière) | C2 grande case (2/3 de largeur)
  - Rangée 2 : C3 | C4
  - Rangée 3 : C5 | C6 | C7
- Statut : rough de composition uniquement (pas d'image publiable).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[STYLE C] Same comic art as Style A but warmer palette; for antiquity: oil lamps and torchlight, raw
limestone, plain linen clothing; for 20th century scenes: sepia-toned archival look. Thin gold border.

Characters and elements (fixed descriptions):
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book

Panel: Full comic page layout rough, 7 panels in 3 rows with white gutters, sepia tones and thin gold borders except the last panel. Row 1: a black-and-white photograph of a painted wall slipped between book pages turning into the same wall in sepia; a large panel inside a vaulted burial chamber around 1950, a camera on a tripod, period floodlights and cables, two figures seen from behind. Row 2: a man in a jacket walking along the painted wall with an open notebook; a bright flash whitening the wall for an instant. Row 3: the man seen from behind sitting on a crate writing, empty space above him; a large printed book on a table; the same book, older, in the hands of an old man in the chamber today, no border.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 17:22
```

### Ép. 3 · Planche 3 · Case 1 — Case charnière : la photo d'archive
- Ratio : --ar 4:3
- Style : C (1949-1951, sépia)
- Personnages : —
- Statut : — (non marqué ; expédition réelle [H], mise en scène [F])
- ⚠ Référence obligatoire : photographies de L. F. Husson publiées dans Piankoff & Rambova 1954 [ARCHIVE] — vérifier les droits avant toute reprise.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[STYLE C] Same comic art as Style A but warmer palette; for antiquity: oil lamps and torchlight, raw
limestone, plain linen clothing; for 20th century scenes: sepia-toned archival look. Thin gold border.

Panel: Hinge panel. Left: a black-and-white archival photograph of a painted wall of KV9, slipped between two pages of a large book and caught in the beam of a headlamp. Right: the same wall seen 'for real', in sepia, a few decades earlier, lit by period floodlights. The painted wall in both halves: painted register with figures, copy from reference. Seamless transition, thin gold border.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 3 · Planche 3 · Case 2 — L'expédition dans la chambre J
- Ratio : --ar 3:2
- Style : C (1949-1951, sépia)
- Personnages : —
- Statut : [H] (expédition) / [F] (mise en scène)
- ⚠ Référence obligatoire : chambre J d'après photographies TMP ; matériel et portraits non documentés (bible) : figures de dos, aucune ressemblance revendiquée ; ne pas représenter N. Rambova sur place. Fiche KV9_J volontairement omise : son « sarcophage restauré » (2001-2004) serait anachronique.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[STYLE C] Same comic art as Style A but warmer palette; for antiquity: oil lamps and torchlight, raw
limestone, plain linen clothing; for 20th century scenes: sepia-toned archival look. Thin gold border.

Panel: Large sepia panel inside the vaulted burial chamber of the tomb (four pillars at the front, walls covered with painted scenes), around 1950; the broken sarcophagus is not restored yet and stays in deep shadow. A mid-century large-format camera on a wooden tripod, period floodlights on stands, cables on the floor (generic equipment, not a documented model). The photographer, gender-neutral, seen from behind, adjusts the camera; a man in a jacket, notebook in hand, seen from behind in three-quarter back view, observes the painted wall. No faces, no claimed likeness; only these two people in the chamber. Archival sepia atmosphere, thin gold border.

Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 3:2
```

### Ép. 3 · Planche 3 · Case 3 — Piankoff longe la paroi
- Ratio : --ar 4:3
- Style : C (1949-1951, sépia)
- Personnages : —
- Statut : [F]
- ⚠ Référence obligatoire : ennemis ligotés sur toutes les parois de J (TMP) — d'après photographie publiée.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[STYLE C] Same comic art as Style A but warmer palette; for antiquity: oil lamps and torchlight, raw
limestone, plain linen clothing; for 20th century scenes: sepia-toned archival look. Thin gold border.

Panel: Medium shot, sepia. A man in a jacket (Piankoff, fictionalised, seen in three-quarter back view, face in shadow) walks slowly along the painted wall, notebook open, well away from it; in the lower register of the wall, small figures of bound enemies (painted register with figures, copy from reference). The photographer in the background, seen from behind. Thin gold border.

Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 3 · Planche 3 · Case 4 — Le flash
- Ratio : --ar 1:1
- Style : C (1949-1951, sépia)
- Personnages : —
- Statut : [F]
- Note : Type de lumière (magnésium ou projecteur) à vérifier dans la documentation avant le dessin final ; l'éclair est historique et bref, pas un éclairage contemporain.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[STYLE C] Same comic art as Style A but warmer palette; for antiquity: oil lamps and torchlight, raw
limestone, plain linen clothing; for 20th century scenes: sepia-toned archival look. Thin gold border.

Panel: Sepia panel. A burst of white light from beside the camera whitens the painted wall for a fraction of a second; the two figures become dark silhouettes against the overexposed wall; the painting is lost in the glare (no detail). Thin gold border.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 3 · Planche 3 · Case 5 — Piankoff écrit sur une caisse
- Ratio : --ar 4:3
- Style : C (1949-1951, sépia)
- Personnages : —
- Statut : [F]
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[STYLE C] Same comic art as Style A but warmer palette; for antiquity: oil lamps and torchlight, raw
limestone, plain linen clothing; for 20th century scenes: sepia-toned archival look. Thin gold border.

Panel: Medium shot, sepia. The man (Piankoff, fictionalised) sits on a wooden crate, seen from behind and slightly from the side, face hidden, writing in his notebook. A large empty area of dark wall above his head is reserved for a thought balloon (added in lettering). Quiet concentration. Thin gold border.

Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 3 · Planche 3 · Case 6 — Le livre de 1954
- Ratio : --ar 1:1
- Style : C (1954, sépia)
- Personnages : —
- Statut : [H]
- ⚠ Référence obligatoire : couverture réelle de The Tomb of Ramesses VI (Piankoff & Rambova, Bollingen Series XL-1, 1954) d'après [ARCHIVE].
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

[STYLE C] Same comic art as Style A but warmer palette; for antiquity: oil lamps and torchlight, raw
limestone, plain linen clothing; for 20th century scenes: sepia-toned archival look. Thin gold border.

Panel: Sepia still life. A large printed book in folio format lies on a wooden table; its cover is plain and blank (the real cover will be copied from reference or the title set in simple typography at the lettering stage). Soft window light. Thin gold border.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 3 · Planche 3 · Case 7 — Retour au présent : le livre dans les mains de Mansour
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : MANSOUR · éléments : KV9_J
- Statut : — (non marqué ; [F])
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
KV9_J: vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Panel: Medium shot. The same large book, older and worn, open in Mansour's hands inside chamber J today, cold LED light. Mansour looks up from it toward the walls, wistful and humble. No gold border.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```


## Planche 4 — Révélation et suspense (7 cases)

### Ép. 3 · Planche 4 — Mise en page (rough)
- Ratio : --ar 17:22
- Style : A (contemporain)
- Personnages : MAYA, KERBU, NEFERTARI, MANSOUR, MARSAC
- Grille :
  - Rangée 1 : C1 | C2
  - Rangée 2 : C3 | C4
  - Rangée 3 : C5 | C6 (incrustation « écran » de Marsac)
  - Rangée 4 : C7 bandeau final pleine largeur
- Statut : rough de composition uniquement (pas d'image publiable).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
MARSAC: Julien Marsac, French man about 50, stubble, swept-back greying hair, sunglasses pushed up on head, expensive linen jacket over a black T-shirt, handheld camera or walkie-talkie

Panel: Full comic page layout rough, 7 panels in 4 rows with white gutters. Row 1: close-up of a tablet showing four unfolded painted walls, each scene framed; the screen with arrows crossing in all directions and blinking red. Row 2: a young woman stunned, turning the tablet toward the others; a woman with glasses showing a phone with a highlighted line in a PDF. Row 3: a Black man fascinated in front of a painted wall, tight shot; a walkie-talkie in a hand with an inset of a man in a linen jacket before a monitor, eyes shining. Row 4: a wide final banner, two colleagues exchanging a weary look while the Black man stares at the painted wall.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 17:22
```

### Ép. 3 · Planche 4 · Case 1 — La tablette : les quatre parois
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : MAYA
- Statut : [H] (disposition) / [F] (interface)
- ⚠ Référence obligatoire : division A (paroi nord), B-C (paroi ouest), D (paroi sud), E (pilastre ouest) d'après Pleuger 2020 p. 48, TMP, Darnell & Darnell 2018 p. 458 ; images d'après photographies publiées.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Panel: Close-up on Maya's tablet held in her hands: the four walls of the burial chamber unfolded side by side, each painted scene framed by a thin coloured outline (scenes copied from reference, very small and soft). No letters, no numbers, no interface text (added in lettering).

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 3 · Planche 4 · Case 2 — L'écran : aucun point de départ
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : —
- Statut : [F]
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Panel: Close-up of the tablet screen: thin arrows appear between the framed scenes, shoot off in several directions, cross each other, then blink red. Contemporary digital graphics, no words (the message is added in lettering).

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 3 · Planche 4 · Case 3 — Maya, sidérée
- Ratio : --ar 4:3
- Style : A (contemporain)
- Personnages : MAYA, KERBU, NEFERTARI, MANSOUR · éléments : KV9_J
- Statut : — (non marqué ; [F])
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
KV9_J: vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Panel: Medium shot in chamber J. Maya, stunned, turns her tablet (screen blinking red) toward the others; Kerbu leans in, puzzled; Nefertari and Mansour in the background. Cold LED light.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 4:3
```

### Ép. 3 · Planche 4 · Case 4 — Nefertari et l'article de Pleuger
- Ratio : --ar 1:1
- Style : A (contemporain)
- Personnages : NEFERTARI
- Statut : [H]
- ⚠ Référence obligatoire : L. Pleuger, BABELAO 9 (2020), p. 48 — la citation exacte est posée au lettrage, jamais générée.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck

Panel: Close shot. Nefertari, calm, holds up her phone; close-up of the screen: a PDF page with blurred, unreadable lines of text and one line highlighted in yellow (unreadable; the quotation is added in lettering). Screen glow on her glasses.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 3 · Planche 4 · Case 5 — Kerbu fasciné devant la paroi nord
- Ratio : --ar 1:1
- Style : A (contemporain)
- Personnages : KERBU, MANSOUR
- Statut : [S]
- ⚠ Référence obligatoire : paroi nord de J d'après photographies TMP / Piankoff & Rambova 1954.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book

Panel: Tight shot. Kerbu, fascinated, stands before the north wall of chamber J at a respectful distance, his face half lit; behind him, slightly out of focus, Mansour. The wall: painted register with figures, copy from reference.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 3 · Planche 4 · Case 6 — Marsac au talkie (incrustation)
- Ratio : --ar 1:1
- Style : A (contemporain)
- Personnages : MARSAC, MAYA
- Statut : [F]
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
MARSAC: Julien Marsac, French man about 50, stubble, swept-back greying hair, sunglasses pushed up on head, expensive linen jacket over a black T-shirt, handheld camera or walkie-talkie
MAYA: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole

Panel: Close-up of Maya's walkie-talkie in her hand; in an inset framed like a monitor screen (rounded corners, faint scanlines): Marsac at the tomb entrance at night, in front of his field monitor, eyes shining with excitement, walkie-talkie to his mouth.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 1:1
```

### Ép. 3 · Planche 4 · Case 7 — Un regard las (bandeau final)
- Ratio : --ar 3:1
- Style : A (contemporain)
- Personnages : NEFERTARI, MANSOUR, KERBU · éléments : KV9_J
- Statut : [F]
- ⚠ Référence obligatoire : paroi nord de J (décor) d'après photographies TMP.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters and elements (fixed descriptions):
NEFERTARI: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around her neck
MANSOUR: Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light linen jacket, wooden walking cane, carries an old thick annotated book
KERBU: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound sketchbook, handheld lamp
KV9_J: vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid sarcophagus

Panel: Wide final banner in chamber J. On one side, Nefertari and Mansour exchange a weary, knowing look; on the other, Kerbu, a little apart, does not take his eyes off the north wall, as if wondering whether Marsac might be a little right. The wall: painted register with figures, copy from reference, in soft focus. Cold LED light, suspended mood.

Conservation rule: nobody touches the painted walls, ceilings or objects; hands, tools and cane are held a few centimetres away from the wall, not touching. Lamps give soft diffuse light only: no projector, laser or spotlight aimed at the paintings. Any wall paintings in the background are out of focus, soft and unreadable (painted registers with figures, copy from reference).

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 3:1
```


## Page documentaire — Épisode 3 : Un livre aux trois noms

### Ép. 3 · Page documentaire — Illustration
- Ratio : --ar 3:2
- Style : A (variante schéma documentaire)
- Personnages : —
- Statut : [H]
- ⚠ Référence obligatoire : dates d'après bible/02 §1 et l'épisode (Pleuger 2020, Roberson 2012, Darnell & Darnell 2018, [ARCHIVE]) ; plan de la chambre J d'après TMP, lettres A à E de Piankoff (Pleuger 2020 p. 48). Tous les libellés au lettrage.
- Note : Le plan de J et les dates sont retracés/posés à la main ; le générateur ne fournit que l'habillage graphique.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Panel: Documentary illustration on aged cream paper, two parts. Upper part: a long horizontal timeline in sepia ink with eight evenly spaced nodes, each with a small empty rounded vignette containing a neutral pictogram (open book, camera on tripod, stack of books), empty bands for captions. Lower part: a simple schematic floor plan of a vaulted burial chamber with four pillars at the front, thin black outlines, walls highlighted by four pale colour bands (no letters). Clean technical look, generous margins. Draft only.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters

--ar 3:2
```


---

## Récapitulatif

| Épisode | Planches | Prompts de mise en page | Prompts de case | Illustration documentaire |
|---|---|---|---|---|

| 1 — La porte de KV9 | 4 | 4 | 27 | 1 |
| 2 — Le plafond des étoiles | 4 | 4 | 29 | 1 |
| 3 — Le livre sans commencement | 4 | 4 | 28 | 1 |
| **Total** | **12** | **12** | **84** | **3** |
