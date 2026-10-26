# Prompts d'images — Couverture, 4ᵉ de couverture, Prologue

Sources : [`01_couverture.md`](../01_couverture.md), [`02_prologue.md`](../02_prologue.md), règles et fiches
de [`00_guide_prompts.md`](00_guide_prompts.md), bible 01 à 03. Les blocs de style, les fiches personnages /
divinités et le négatif sont **copiés mot pour mot** du guide ; seule la description de la case est propre
à chaque prompt.

> Rappels : aucune case **[H]** générée ne se publie telle quelle (correction par un artiste ou
> image-to-image à partir d'une référence dont les droits sont vérifiés, bible 06 §6) · aucun texte dans
> l'image (titres, cartouches et bulles ajoutés au lettrage) · aucun hiéroglyphe lisible inventé ·
> personne ne touche les parois · déclaration « contenu généré par IA » sur KDP.

**Références d'images à utiliser pour les cases [H]** (redessin, pas d'intégration de photos) :
- **Piankoff & Rambova, *The Tomb of Ramesses VI*, Bollingen Series XL-1, 1954** (photos L. F. Husson) —
  parois des corridors B-C et de la chambre J ; notice [ARCHIVE].
- **Theban Mapping Project**, fiche KV9 (plans, photos des salles, liste des décors par paroi) [TMP].
- Photographies sous licence libre (Wikimedia Commons, CC BY / CC BY-SA : créditer auteur + licence) ou
  photos personnelles de l'auteur, pour l'entrée actuelle de KV9 et le paysage de la Vallée.

---

## 1. Couverture (format portrait)

Format : 8,5 × 11 po → `--ar 17:22`. Le titre, le sous-titre et la mention « Volume 1 » sont posés au
lettrage : **le tiers supérieur (voûte de Nout) doit rester calme et sombre**, sans élément important.

### COUV · Variante 1 — Fidèle au brief (trois plans, contre-plongée légère)
- Ratio : --ar 17:22
- Style : A (scène) — le disque solaire et les parois sont traités en aplats « style mural » (traitement B, sans liseré doré)
- Personnages : KERBU · éléments : KV9_J, AKER, NUT
- Statut : [F] Kerbu · [H] parois, voûte et sarcophage · [S] disque porté par des bras
- ⚠ Référence obligatoire : photos de la chambre funéraire J dans Piankoff & Rambova 1954 (parois nord / ouest / sud du Livre de la Terre, voûte aux deux Nout) et photos du Theban Mapping Project ; pour le double Aker, la scène d'ouverture du Livre de la Terre (§6.1, bible 02). Le disque aux bras levés s'inspire de §6.3 (disque embrassé par des bras sortant du sol) : vision, pas copie de paroi.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Comic book cover, portrait format, three depth planes.
Character: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm
intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small
leather-bound sketchbook, handheld lamp.
Setting: vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in
red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid
sarcophagus.

FOREGROUND (lower third): Dr Kerbu seen from three-quarter back, slightly low angle, raising his handheld
lamp high; his face turned upward, partly visible in profile, expression of wonder and curiosity, not fear.
The cold white beam cuts diagonally through the darkness, full of floating dust. His hand and lamp stay
well away from the wall, not touching.
MIDDLE PLANE (walls): the beam reveals painted registers of the Book of the Earth on pale plaster, red,
ochre and yellow: rows of small figures, serpents, sun disks, and a double sphinx: two lion bodies joined
back to back, one head at each end, a barque resting on its back. Wall details soft and slightly out of
focus, signs blurred and illegible. On the floor, the sarcophagus is only a dark broken mass in deep
shadow.
BACKGROUND (centre-top): a huge red-gold sun disk that seems to emerge from the wall, held up by raised
arms, drawn in flat Egyptian mural style (flat colour, bold black outline, no shading) so it reads as an
image, a vision, glowing gold against the black of the tomb.
TOP EDGE: the beginning of the night-blue vault with the elongated woman arched over the scene, body
covered with stars, dark blue background — kept dark and calm, large empty space reserved for the title.
Palette: night blue ceiling, ochre and red walls, gold disk, cold white lamp light; strong contrast between
the gold disk and the black tomb. Mood: awe, mystery, quiet discovery.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters --ar 17:22
```

### COUV · Variante 2 — Le disque domine (Kerbu plus petit, axe central)
- Ratio : --ar 17:22
- Style : A (scène) — disque et parois en aplats « style mural » (traitement B, sans liseré doré)
- Personnages : KERBU · éléments : KV9_J, AKER, NUT
- Statut : [F] Kerbu · [H] parois, voûte et sarcophage · [S] disque porté par des bras
- ⚠ Référence obligatoire : mêmes sources que la variante 1 (Piankoff & Rambova 1954, chambre J ; Theban Mapping Project ; Livre de la Terre §6.1 pour Aker, §6.3 pour le motif du disque).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Comic book cover, portrait format, symmetrical central composition.
Character: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm
intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small
leather-bound sketchbook, handheld lamp.
Setting: vaulted burial chamber, four pillars at the front, walls covered with Book of the Earth scenes in
red and yellow ochre, ceiling with two back-to-back elongated sky goddesses, restored dark green anthropoid
sarcophagus.

Camera low, behind Dr Kerbu, who stands small in the lower third, seen from three-quarter back between two
dark pillars that frame the image like a doorway. He lifts his handheld lamp at arm's length, face tilted
up toward the light, partly visible, curious and calm. His hand is far from the wall, not touching. A
narrow cone of cold white light rises from the lamp, dust glittering in it.
Straight ahead, filling the centre of the image, an immense red-gold sun disk appears to rise out of the
far wall, supported from below by raised arms, flat Egyptian mural style, bold black outline, no shading,
glowing warm gold — clearly a painted vision, not a real object.
On the side walls, at the edges of the frame, painted registers in red, ochre and yellow fade into
darkness: rows of figures, serpents, small sun disks, and a double sphinx: two lion bodies joined back to
back, one head at each end, a barque resting on its back; all wall signs blurred and illegible. Floor in
deep shadow, with only the dark shape of the broken sarcophagus.
Upper third: the curved night-blue vault with the elongated woman arched over the scene, body covered with
stars, dark blue background, very dark and uncluttered — empty space for the title.
Palette: night blue, ochre, red, gold, cold white. High contrast, cinematic, sense of revelation.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters --ar 17:22
```

---

## 2. Quatrième de couverture

### 4ᵉ · Illustration de fond — Nout et le disque, en filigrane
- Ratio : --ar 17:22
- Style : B (atténué, en filigrane ; pas de liseré doré : c'est un fond)
- Personnages : aucun · éléments : NUT
- Statut : [S] (motif inspiré des plafonds de KV9, non copié d'une paroi précise)
- Usage : fond très peu contrasté pour recevoir le texte de 4ᵉ, l'encadré « page documentaire » et la zone
  du code-barres KDP (en bas à droite, à laisser vide).
- Prompt :
```
[STYLE B] Ancient Egyptian New Kingdom tomb painting style, flat mineral colours (red ochre, yellow
ochre, Egyptian blue, malachite green, carbon black, lime white), bold black outlines, figures in strict
profile with frontal eye and shoulders, Egyptian canon of proportions, horizontal registers, no
perspective, no shading, thin gold border around the panel.

Book back cover background illustration, very discreet and low contrast. Elements: elongated woman arched
over the scene, body covered with stars, dark blue background.
The star-covered sky goddess forms a thin arch along the top and the two side edges of the page, faded
like an old ceiling painting, colours muted to deep blue and dull gold. In the lower part, a small red-gold
sun disk sits just above a thin wavy ground line, softly glowing, like the first light before dawn.
The whole centre of the page is an almost empty field of deep night blue with faint scattered stars and a
subtle plaster texture, calm and readable, reserved for overlaid text. Bottom right corner kept completely
plain for a barcode. No gold border on this background (ignore the panel border), edges fade softly into
darkness. Quiet, contemplative mood.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters --ar 17:22
```

---

## 3. Prologue — « Celui qui descend dans la Terre »

### Planche P1 — 6 cases

#### P1 · Mise en page (rough de la planche entière)
- Ratio : --ar 17:22
- Style : A
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA
- Grille proposée (4 bandes) : **bande 1** = case 1 (bandeau pleine largeur) · **bande 2** = case 2 (2/3 de
  largeur) + case 3 (1/3, gros plan) · **bande 3** = case 4 + case 5 (deux moitiés) · **bande 4** = case 6
  (pleine largeur, plus haute : la porte de KV9 clôt la page).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Full comic book page layout, six panels in four horizontal tiers, thin white gutters, black panel borders.
Characters:
Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense
eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound
sketchbook, handheld lamp.
Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a
light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around
her neck.
Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light
linen jacket, wooden walking cane, carries an old thick annotated book.
Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof
technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole.

Tier 1, full-width panoramic panel: Valley of the Kings before dawn, Theban cliffs in silhouette against a
blue-grey sky, a pyramid-shaped peak dominating, four tiny headlamps moving along a desert track.
Tier 2, wide panel: the four team members walking, medium shot; narrow panel: close-up of Dr Kerbu's face
in blue pre-dawn light.
Tier 3, two equal panels: Nefertari in profile with a raised eyebrow; Dr Kerbu looking east toward an
orange glow behind the ridge.
Tier 4, large full-width panel: the rock-cut entrance of a tomb with a metal gate and a blank sign plate,
four headlamp beams converging on the black opening.
Palette: cold blue-grey dawn, small warm headlamp points, first orange glow in tier 3. Mood: quiet,
anticipation. Leave calm areas in each panel for captions added later.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters --ar 17:22
```

### P1 · Case 1 — La Vallée avant l'aube
- Ratio : --ar 3:1
- Style : A
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA (minuscules silhouettes)
- Statut : [H] décor / [F] scène (arrivée à 5 h 42 = accès scientifique fictif)
- ⚠ Référence obligatoire : photographies de la Vallée des Rois et de la cime d'el-Qurn vue depuis la piste de la vallée (photos personnelles ou Wikimedia Commons sous licence libre, créditées) ; vérifier la silhouette réelle des falaises.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters (tiny distant figures, recognisable only by silhouette):
Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense
eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound
sketchbook, handheld lamp.
Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a
light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around
her neck.
Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light
linen jacket, wooden walking cane, carries an old thick annotated book.
Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof
technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole.

Wide panoramic establishing shot, Valley of the Kings, Luxor, before dawn. The Theban limestone cliffs
stand as dark silhouettes against a cold blue-grey sky, the natural pyramid-shaped peak of el-Qurn
dominating the ridge. Below, in the deep shadow of the valley floor, a pale dusty track; four tiny warm
headlamp points move along it in single file, the only warm light in the image. Deserted landscape, no
other people, stillness, the hush before sunrise. Calm empty sky in the upper left for caption boxes.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters --ar 3:1
```

### P1 · Case 2 — L'équipe en marche
- Ratio : --ar 2:1 (2/3 de largeur de bande)
- Style : A
- Personnages : MAYA, MANSOUR, NEFERTARI, KERBU
- Statut : [F]
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters:
Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof
technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole.
Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light
linen jacket, wooden walking cane, carries an old thick annotated book.
Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a
light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around
her neck.
Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense
eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound
sketchbook, handheld lamp.

Medium shot, eye level, the four walk toward the viewer on the dusty track at blue hour, headlamps on.
Left: Maya carrying a hard-shell equipment case for the scanner, focused. Next to her: Professor Mansour
leaning on his wooden cane, steady and unhurried. Centre: Nefertari looking down at a tablet, its screen
casting a faint glow on her glasses (screen content not visible). Slightly ahead on the right: Dr Kerbu,
head raised, gazing up at the cliff above them, thoughtful. Cold blue ambient light, small warm headlamp
glows, long soft shadows, dark cliffs behind. Mood: a focused team, quiet determination.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters --ar 2:1
```

### P1 · Case 3 — Kerbu, lumière bleue
- Ratio : --ar 1:1
- Style : A
- Personnages : KERBU
- Statut : [F]
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Character: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm
intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small
leather-bound sketchbook, handheld lamp.

Close-up of Dr Kerbu's face, three-quarter view, slightly low angle, bathed in cold blue pre-dawn light;
his headlamp is switched off and pushed up on his forehead. Calm, intense, almost solemn expression, eyes
lifted toward the mountains as if speaking about something very old. Soft blue rim light on his beard and
cheekbone, dark blurred cliff behind him. Space on one side of the panel for a speech balloon added later.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters --ar 1:1
```

### P1 · Case 4 — Nefertari, sourcil levé
- Ratio : --ar 4:3
- Style : A
- Personnages : NEFERTARI
- Statut : [F]
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Character: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied
back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on
a cord around her neck.

Medium close-up of Nefertari in strict profile, turning her head slightly from her tablet toward someone
off-panel, one eyebrow raised: amused scepticism, curiosity, a scientist who wants a precise answer. Cold
blue dawn light, small warm reflection of a headlamp on her glasses, dark cliff silhouette and blue-grey
sky behind her. Empty sky area in front of her face for a speech balloon.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters --ar 4:3
```

### P1 · Case 5 — Le regard vers l'est
- Ratio : --ar 4:3
- Style : A
- Personnages : KERBU
- Statut : [F]
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Character: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm
intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small
leather-bound sketchbook, handheld lamp.

Over-the-shoulder medium shot from behind and slightly to the side of Dr Kerbu, who looks east toward the
crest of the hills. Behind the dark ridge line, a thin first orange glow appears in the blue-grey sky, the
sun not yet visible. The faint warm light catches the edge of his face and beard, the rest of him still in
cold blue shadow. Expression: contemplative, a question rather than an answer. Strong colour contrast:
cold blue foreground, thin warm orange horizon. Sky space for a speech balloon.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters --ar 4:3
```

### P1 · Case 6 — L'entrée de KV9
- Ratio : --ar 3:2 (grande case de fin de planche)
- Style : A
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA (de dos, en silhouette)
- Statut : [H]
- ⚠ Référence obligatoire : photographies de l'entrée actuelle de KV9 (porte taillée dans la roche, grille, auvent / aménagements modernes, plaque signalétique) — photos personnelles ou Wikimedia Commons sous licence libre ; plan de l'entrée A du Theban Mapping Project. La plaque « KV9 » est laissée vierge : son texte est ajouté au lettrage, copié d'après photo.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters (seen from behind, partly in silhouette):
Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense
eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound
sketchbook, handheld lamp.
Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a
light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around
her neck.
Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light
linen jacket, wooden walking cane, carries an old thick annotated book.
Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof
technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole.

Wide shot from behind the group, slightly elevated. In front of them, the rock-cut entrance of the tomb:
a rectangular doorway cut into the pale limestone hillside, closed by a modern metal gate, a small blank
sign plate beside it. Beyond the gate, the opening is pure black. The four headlamp beams converge on the
dark doorway, dust drifting in the light. Cold blue dawn ambient light on the rock. Mood: threshold,
gravity, the moment before descending. Composition draws the eye into the black opening.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters --ar 3:2
```

---

### Planche P2 — 6 cases

#### P2 · Mise en page (rough de la planche entière)
- Ratio : --ar 17:22
- Style : A, puis B en bas de planche (bascule progressive)
- Personnages : KERBU, NEFERTARI, MAYA (MANSOUR possible en arrière-plan de la case 1)
- Grille proposée (4 bandes) : **bande 1** = case 1 (pleine largeur, 1/3 de la planche) · **bande 2** =
  cases 2 et 3 (deux moitiés) · **bande 3** = case 4 (moitié) + case 5 (moitié, bord qui se dore) ·
  **bande 4** = case 6 (bandeau final pleine largeur, style mural, liseré doré).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Full comic book page layout, six panels in four horizontal tiers, thin white gutters, black panel borders,
the last tier switching to ancient Egyptian flat mural style with a thin gold border.
Characters:
Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense
eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound
sketchbook, handheld lamp.
Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a
light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around
her neck.
Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof
technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole.
Setting: long straight sloping rock-cut corridor, painted walls with registers of figures, starry
astronomical ceiling, modern wooden walkway and handrails.

Tier 1, large full-width panel (one third of the page): the first corridor seen from the entrance, sloping
down, lamp beams revealing painted walls and the astronomical ceiling.
Tier 2, two panels: Maya pointing her scanner toward a wall, tablet showing a point cloud; Nefertari with a
loupe a few centimetres from a painting, not touching.
Tier 3, two panels: Dr Kerbu's lamp grazing a painted sun disk; extreme close-up of the painted disk with a
halo of light, the panel border starting to turn gold.
Tier 4, full-width strip in flat Egyptian mural style on black: a red sun disk surrounded by raised arms
beneath a wavy ground line, thin gold border.
Colour progression from cold LED white and ochre at the top to black and gold at the bottom. Calm areas for
captions and balloons.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters --ar 17:22
```

### P2 · Case 1 — Le premier corridor
- Ratio : --ar 2:1 (case pleine largeur, 1/3 de planche)
- Style : A
- Personnages : KERBU, NEFERTARI, MANSOUR, MAYA (silhouettes de dos au premier plan, ou seulement leurs faisceaux)
- Statut : [H]
- ⚠ Référence obligatoire : photos du corridor B dans Piankoff & Rambova 1954 et sur le Theban Mapping Project (vue axiale depuis l'entrée). Rappel de décor (bible 01) : paroi sud (gauche en descendant) = Livre des Portes div. 1-2 précédé du roi devant Rê-Horakhty et Osiris ; paroi nord (droite) = Livre des Cavernes div. 1 ; plafond = constellations circumpolaires et décans. **Pas de Livre de la Terre dans ce corridor.** Figures à garder floues / hors focale tant qu'elles ne sont pas redessinées d'après la publication.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Characters (backs only, small, in the lower foreground):
Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm intense
eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small leather-bound
sketchbook, handheld lamp.
Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied back under a
light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on a cord around
her neck.
Professor Adel Mansour, Egyptian man about 68, grey moustache, lined kind face, cream linen hat, light
linen jacket, wooden walking cane, carries an old thick annotated book.
Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey waterproof
technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole.
Setting: long straight sloping rock-cut corridor, painted walls with registers of figures, starry
astronomical ceiling, modern wooden walkway and handrails.

Wide one-point-perspective shot from the entrance looking down the straight sloping corridor, which
recedes into total darkness. The team, seen from behind at the bottom edge, walks on the wooden walkway
between the handrails, keeping to the centre. Their headlamp and lamp beams sweep the walls, revealing
fragments of painted registers on pale plaster: rows of deities, serpents, elongated lying bodies, sun
disks, in red ochre, yellow ochre, Egyptian blue and black; the paintings soft and slightly out of focus,
signs illegible. Overhead, the ceiling shows dark blue astronomical figures and stars caught by the light.
Dust in the beams. Mood: awe, reverence, a first step into another world. Dark area at top left for a
caption.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters --ar 2:1
```

### P2 · Case 2 — Maya scanne la paroi
- Ratio : --ar 4:3
- Style : A
- Personnages : MAYA
- Statut : non marqué dans le script (action [F] ; paroi d'arrière-plan réelle → la garder floue)
- ⚠ Référence obligatoire : si la paroi devient lisible au dessin final, la redessiner d'après le corridor B (Piankoff & Rambova 1954 / Theban Mapping Project).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Character: Maya, woman about 30, short dark bob haircut, dark-framed glasses pushed on her head, grey
waterproof technical jacket with many pockets, carries a tablet and a portable 3D scanner on a pole.
Setting: long straight sloping rock-cut corridor, painted walls with registers of figures, starry
astronomical ceiling, modern wooden walkway and handrails.

Medium shot from slightly behind Maya, standing on the wooden walkway. She holds the portable 3D scanner
on its pole toward the painted wall, the scanner head clearly a good distance from the plaster, not
touching. In her other hand, the tablet screen glows, showing a colourful 3D point cloud of the wall (dots
only, no interface text). Her face lit from below by the screen: concentrated, slightly puzzled. The wall
paintings behind are soft and out of focus, faint red and ochre figures. Cold LED light, dust in the air.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters --ar 4:3
```

### P2 · Case 3 — Nefertari et la loupe
- Ratio : --ar 4:3
- Style : A
- Personnages : NEFERTARI
- Statut : non marqué dans le script (action [F] ; peinture réelle en gros plan)
- ⚠ Référence obligatoire : détail de peinture redessiné d'après le corridor B (Piankoff & Rambova 1954 / Theban Mapping Project), ou laissé flou. Rappel : la réplique parle du Livre de la Terre, qui n'est **pas** dans ce corridor — la paroi montrée ne doit pas être présentée comme le Livre de la Terre.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Character: Dr Nefertari Hassan, Egyptian woman about 38, olive skin, rectangular glasses, dark hair tied
back under a light headscarf, practical beige field jacket, nitrile gloves, epigraphy magnifying loupe on
a cord around her neck.

Close medium shot, side view. Nefertari leans toward the painted wall holding her epigraphy loupe in a
gloved hand, the loupe and her fingers a few centimetres away from the painting, clearly not touching; a
visible gap of air between glove and plaster. Her headlamp makes a soft circle on the faded red ochre and
black paint, which stays blurred and illegible. Expression: absorbed, knowledgeable, about to explain
something complex. Shallow depth of field, warm headlamp light against cold surroundings.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters --ar 4:3
```

### P2 · Case 4 — Kerbu et le disque peint
- Ratio : --ar 4:3
- Style : A
- Personnages : KERBU
- Statut : non marqué dans le script (action [F] ; disque peint réel)
- ⚠ Référence obligatoire : le script ne précise pas **quel** disque : l'auteur choisit un disque solaire réellement présent dans les corridors B-C et le redessine d'après Piankoff & Rambova 1954 / Theban Mapping Project. Le même disque sert à la case 5 (gros plan).
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Character: Dr Kerbu, Black African man about 45, dark skin, short greying beard, close-cropped hair, calm
intense eyes, sand-coloured field shirt with rolled sleeves, khaki trousers, LED headlamp, small
leather-bound sketchbook, handheld lamp.

Medium shot, three-quarter view. Dr Kerbu steps closer to a painted red sun disk on the wall and holds his
handheld lamp low and at an angle so the light grazes the surface, revealing the texture of the plaster;
lamp and hand stay well away from the wall, not touching. His face half lit, eyes narrowed with attention
and quiet respect, as if learning to see. The disk is a simple red circle with a soft edge, surrounding
figures dim and blurred. Raking light, long shadows across the plaster grain, dust in the beam.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters --ar 4:3
```

### P2 · Case 5 — Le disque dans le halo (case charnière)
- Ratio : --ar 1:1
- Style : A, avec le liseré doré B qui **commence** à apparaître sur le bord de la case
- Personnages : aucun (seulement le faisceau de la lampe de KERBU)
- Statut : non marqué dans le script ; peinture réelle en gros plan → traiter comme [H]
- ⚠ Référence obligatoire : le même disque qu'en case 4, redessiné d'après Piankoff & Rambova 1954 / Theban Mapping Project. Ne rien ajouter autour du disque (pas de signes) qui ne soit sur la source.
- Prompt :
```
[STYLE A] Franco-Belgian realistic comic art, cinematic graphic novel, clean ink lines with painted
digital colour, natural cold LED light mixed with warm headlamp light, dust particles in light beams,
detailed limestone rock textures, faded ancient wall paintings in red ochre, yellow ochre, Egyptian blue
and black on pale plaster, expressive faces, high detail.

Extreme close-up of a painted red sun disk on pale plaster, centred in the square panel. The beam of a
lamp forms a circular halo of light around the disk, the plaster grain and tiny cracks visible, the rest
of the wall falling into darkness at the corners. The red of the disk seems to glow faintly in the light,
a hint that the image is coming alive. The panel border is black on one side and gradually turns into a
thin gold line on the other side, as if the frame were transforming. Nothing else legible around the disk;
any surrounding painted detail blurred. Mood: hypnotic, the threshold between reality and myth.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters --ar 1:1
```

### P2 · Case 6 — Le soleil sous la Terre (bandeau final)
- Ratio : --ar 3:1
- Style : B
- Personnages : aucun
- Statut : [S] (motif inspiré du Livre de la Terre §6.3 : disque embrassé par des bras sortant du sol — interprétation, pas copie d'une paroi)
- Prompt :
```
[STYLE B] Ancient Egyptian New Kingdom tomb painting style, flat mineral colours (red ochre, yellow
ochre, Egyptian blue, malachite green, carbon black, lime white), bold black outlines, figures in strict
profile with frontal eye and shoulders, Egyptian canon of proportions, horizontal registers, no
perspective, no shading, thin gold border around the panel.

Wide panoramic strip, solid carbon black background. Across the upper part runs a wavy ground line in
yellow ochre representing the Earth, like a band of hills seen in section. Beneath it, centred, a large
flat red ochre sun disk with a bold black outline, surrounded by pairs of raised arms in red ochre skin
tone rising from below and around it, palms open, holding and lifting the disk upward toward the ground
line. Strictly flat colours, no shading, no perspective, symmetrical and solemn, lots of empty black space
on both sides for captions. Thin gold border around the panel. Mood: the sun waiting in the depths, about
to be reborn.

no text, no lettering, no speech bubbles, no captions, no watermark, no readable hieroglyphs,
no modern objects in ancient scenes, correct anatomy, consistent characters --ar 3:1
```

---

## Récapitulatif

| Bloc | Prompts | Cases [H] / à référence |
|---|---|---|
| Couverture | 2 variantes | 2 (parois, voûte, Aker) |
| 4ᵉ de couverture | 1 | 0 |
| P1 | 1 mise en page + 6 cases | case 1 (décor), case 6 |
| P2 | 1 mise en page + 6 cases | case 1 ; cases 2-5 sur paroi réelle (référence recommandée, obligatoire pour 4-5) |
| **Total** | **17 prompts** | |
