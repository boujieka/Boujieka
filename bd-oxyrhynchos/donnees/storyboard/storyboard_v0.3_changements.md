# Changements v0.2 → v0.3

Storyboard du tome 2 « Les mille visages de l'Égypte ancienne » (collection « Images d'Afrique »). Source : `storyboard_t2_complet_v0.2.md` (non modifié). Sortie : `storyboard_t2_complet_v0.3.md`. Données : `registre_egypte_v2.json` (deuxième passe ; `registre_nubie_sahel_v2.json` pour NU-001, inchangé en source secondaire).

**Contrôle de structure (script, sur la v0.3)** : un seul « # Notes générales » ; 46 planches numérotées de 1 à 46 ; 327 cases, avec les mêmes identifiants que la v0.2, dans le même ordre ; chaque planche a une **Intention :**, un **Gabarit :** et un « ### Points de contrôle » ; chaque case a les six champs dans l'ordre ; aucun autre « ## ». Aucune case perdue ni ajoutée.

**Règle appliquée** : un [À VÉRIFIER] n'est levé que si la donnée figure dans une fiche au statut `verifiee_notice` ; elle est alors étiquetée [H : notice <institution>]. Tout ce que la fiche ne dit pas reste [À VÉRIFIER] (crédits photo, statut Open Access objet par objet, conditions du British Museum, détails à lire sur photo, pose de la statuette d'Isis, instruments de musique).

## 1. Cases et sections modifiées (avant → après, en résumé)

**Notes générales**
- Document : « Version harmonisée v0.2 » → « Version v0.3 », mise à jour après la deuxième passe ; renvoi au présent fichier.
- Nouveau paragraphe **Mise à jour v0.3** (fiches vérifiées, règle des étiquettes, Fayoum, écart de datation Nebamon, lieu du chapitre 3, fiches restant non vérifiées).
- Références : `registre_egypte.json` → `registre_egypte_v2.json` (et `registre_nubie_sahel_v2.json`) ; statuts mis à jour (vérifiées sur notice : + IA-006, IA-015, IA-017, IA-018, IA-019, IA-020 ; non vérifiées : IA-004, IA-005, IA-008, IA-009, IA-010, IA-016, IA-021 ; source secondaire : IA-002, NU-001).

**Planche 14 (IA-017, Met 20.3.11)**
- 14.1 : vitrine « des personnages au travail, un bateau » → le modèle de grenier avec porteurs de sacs et scribes. Récitatif : « [À VÉRIFIER : institution selon la fiche IA-017] » → institution connue (Met, salle 105) mais nom du musée **non imprimé** : le lieu du chapitre 3 devient un choix de l'auteur [À VÉRIFIER : choix de l'auteur].
- 14.3 : « modèle précis à choisir, trois variantes de crayonné » → modèle de grenier avec scribes (zones de stockage et de comptabilité, 6 porteurs, 9 hommes dont 4 scribes). Légende modèle → « Modèle de grenier avec scribes. Thèbes, tombe de Meketrê. Moyen Empire, XIIe dynastie, vers 1981–1975 av. J.-C. Bois, plâtre, peinture, lin, grain. New York, The Metropolitan Museum of Art, 20.3.11. » [H : notice Met].
- 14.4 : bulle inchangée ; [À VÉRIFIER : circonstances de découverte] → [H : notice Met] (serdab de TT 280, fouilles du Met en 1920).
- 14.6 : reconstitution « d'autres rament sur un bateau » → portage, mesurage du grain et scribes qui notent (activités du modèle réel) ; palette « Moyen Empire [À VÉRIFIER] » → [H : notice Met]. Bulle inchangée (« textes funéraires » reste [À VÉRIFIER]).
- Points de contrôle : fiche vérifiée ; nouveau point « choix de l'auteur : lieu du chapitre 3 » (Met = voyage à New York, P33–34 au Met, Nebamon au British Museum, papyrus à la NYAM) ; droits Met Open Access à confirmer pour l'objet.

**Planche 16 (IA-018, British Museum EA37977)**
- 16.1 : « un homme… femme et enfant (à adapter à l'image réelle) » → Nebamon dans une barque avec son épouse et sa fille, son chat, huit colonnes de hiéroglyphes. Légende modèle → « Nebamon chassant les oiseaux dans les marais. Fragment de peinture murale, plâtre peint. Thèbes, tombe de Nebamon. Nouvel Empire, XVIIIe dynastie, vers 1350 av. J.-C. (datation du musée). Londres, British Museum, EA37977. » [H : notice British Museum].
- 16.2 : MALIK « le petit » → « la petite » (la notice nomme la fille de Nebamon) ; seule retouche de dialogue de la planche.
- 16.3 : bulle inchangée ; rigueur : pêche attestée, position des poissons [À VÉRIFIER].
- 16.4 : bulle inchangée ; présence des oiseaux [H], traitement « plume par plume » [À VÉRIFIER].
- 16.5 : « chat seulement si l'image réelle en montre un » → le chat de Nebamon qui attrape des oiseaux [H : notice British Museum] ; bulle de Malik conservée.
- Points de contrôle : fiche vérifiée ; écart de datation 1350 / 1370 ; « Purchased from: Henry Salt » ; droits BM non lus ; règle « vitrine ou tablette ».

**Planche 17 (IA-019, British Museum EA37984)**
- 17.1 : « femmes jouant d'instruments, danseuses, invités (à adapter) » → deux registres (invités servis par une servante ; quatre musiciennes assises dont deux de face, deux danseuses), quinze colonnes de hiéroglyphes, fragment « l'un des trois ». Légende modèle → « Musiciennes et danseuses du banquet. Fragment de peinture murale, plâtre peint. Thèbes, tombe de Nebamon. Nouvel Empire, XVIIIe dynastie, règne d'Amenhotep III, vers 1370 av. J.-C. (datation du musée). Londres, British Museum, EA37984. » [H : notice British Museum].
- 17.4 : « musiciennes et danseuse » → « musiciennes et danseuses » (deux danseuses) ; rigueur complétée.
- 17.5 : décor + « deux des musiciennes de face » [H] ; bulle inchangée ; interdiction maintenue de parler d'« exception ».
- Points de contrôle : fiche vérifiée ; instruments non identifiés par la fiche ; écart de datation ; droits BM non lus.

**Planche 18 (IA-020, papyrus Edwin Smith, NYAM)**
- 18.1 : « papyrus déroulé » → feuillet du papyrus montré sur la tablette d'Inès (le papyrus est découpé en 10 feuillets et conservé dans une bibliothèque). Légende « Edwin Smith ou Ebers » → « Papyrus chirurgical Edwin Smith. Écriture hiératique, vers 1600 av. J.-C. New York, bibliothèque de la New York Academy of Medicine. » [H : notice NYAM] ; pas de cote (la notice n'en donne pas).
- 18.3 : bulle « descriptions de maux, examens, remèdes… parfois des formules » → « des blessures décrites une à une : ce qu'on voit, ce qu'on en pense, ce qu'on peut espérer, comment soigner… Et au dos, des formules à réciter et des recettes. » [H : notice NYAM] / « Pour eux, tout cela allait ensemble. » [I]. Le schéma en trois colonnes est conservé.
- 18.4 : bulle inchangée ; rigueur : soin d'une blessure cohérent avec le contenu du papyrus.
- Points de contrôle : choix Edwin Smith acté ; historique pour le cahier ; règle « tablette » ; droits à demander à la NYAM ; licences des vignettes 18.5 (Met, BM).

**Planche 19** — 19.5 : champ Œuvre seulement (« IA-006 à venir » → « IA-006, vérifiée : Met 04.2.441, rattachée en P22 ») ; les croquis restent des schémas « date ? source ? ».

**Planche 21** — 21.1 : rigueur seulement (façade : IA-017 au Met, mais lieu du chapitre 3 = choix de l'auteur).

**Planche 22 (IA-006, Met 04.2.441)**
- 22.4 : silhouette schématique + tampon « OBJET À CHOISIR » → croquis d'après la statuette en bronze (couronne à cornes empruntée à Hathor, Horus le doigt à la bouche). Étiquette → « ④ La mère : Isis allaitant Horus. Statuette, bronze, H. 20,3 cm. Basse Époque (XXVIe–XXXe dynasties, 664–332 av. J.-C.). D'Égypte. New York, Metropolitan Museum, 04.2.441. » [H : notice Met]. Pose assise : [À VÉRIFIER].
- 22.5 : champ Œuvre seulement.
- Points de contrôle : fiche vérifiée ; Open Access de l'objet à confirmer.

**Planche 23** — 23.2 : frise : ajout de « 664–332 av. J.-C. (statuette ④) » [H : notice Met] ; rigueur distingue période du type et date d'objet.

**Planche 41 (IA-015, Met 09.181.6)**
- Intention : « portraits du Fayoum (case grise) » → « portraits funéraires d'époque romaine, dits “portraits du Fayoum” (un exemple attesté, IA-015) ».
- 41.9 : case grise « portrait du Fayoum — objet à choisir » → croquis attesté du « Portrait of a young woman in red ». Bulle « Dans d'autres salles, il y a des visages… : les portraits du Fayoum » → « Il existe aussi des visages peints sur bois… On les appelle souvent “portraits du Fayoum”. » [I : nom usuel du genre] + « Celui-ci est à l'encaustique. » Légende ajoutée : « Portrait d'une jeune femme en rouge. Portrait funéraire d'époque romaine, d'Égypte, 90–120 apr. J.-C. Encaustique sur bois de tilleul, feuille d'or. New York, Metropolitan Museum, 09.181.6. » [H : notice Met]. Aucune mention du Fayoum comme provenance.
- Points de contrôle : fiche vérifiée, « From Egypt » seulement ; Open Access de l'objet à confirmer.

**Planche 43** — 43.2 : champ Œuvre seulement (IA-006 vérifiée).

**Planche 44** — 44.1 : Œuvre et rigueur (visage toujours inventé ; IA-015 citable au cahier comme « portrait funéraire d'époque romaine, d'Égypte » ; « Fayoum » = nom du genre [I]). Points de contrôle : formule du cahier p. 53.

**Planche 45** — 45.8 : cadre « objet à choisir » → croquis ④ repris de 22.4 ; bulle de Malik conservée, « une mère assise » marquée [À VÉRIFIER : pose]. Points de contrôle : droits du croquis ④.

**Planche 46** — 46.1 : la case reste **grise** pour respecter la symétrie stricte avec 46.2 (Vierge allaitante, sans fiche) ; mention « objet à choisir » → « en attente (symétrie avec 46.2) » ; Œuvre « IA-006 (non vérifiée) » → vérifiée ; « les deux sont assises » [À VÉRIFIER]. Points de contrôle mis à jour.

**Non modifié** : toutes les autres cases, en particulier P15 (IA-021 toujours non vérifiée), P4–7 (IA-002, source secondaire), P10–13 (IA-004), P20–22 (IA-005), P28 (IA-008), P30–32, P35 (IA-009, IA-010), P43.3 (IA-016), P46.9 (NU-001), ainsi que le tableau de chronologie des Notes générales (le « musée du chapitre 3 [À VÉRIFIER : institution] » y reste tel quel, en attente du choix de l'auteur).

## 2. [À VÉRIFIER] levés (donnée présente dans la fiche vérifiée)

| Œuvre | Case | [À VÉRIFIER] v0.2 | Remplacé par |
|---|---|---|---|
| IA-017 | 14.1 | institution de conservation | Met, New York, salle 105 [H : notice Met] (rigueur ; nom non imprimé dans le récitatif) |
| IA-017 | 14.3 | type de modèle, datation, conservation, inventaire | grenier avec scribes ; vers 1981–1975 av. J.-C. ; Met 20.3.11 [H : notice Met] |
| IA-017 | 14.3 | objets précis ; matériau « bois peint » | bois, plâtre, peinture, lin, grain ; dimensions [H : notice Met] |
| IA-017 | 14.4 | circonstances de découverte | serdab de TT 280, fouilles du Met 1920 [H : notice Met] |
| IA-017 | 14.6 | période de Meketrê (Moyen Empire) | Moyen Empire, XIIe dynastie [H : notice Met] |
| IA-018 | 16.1 | conservation, datation, inventaire ; fiche IA-018 ; personnages | British Museum EA37977, vers 1350 av. J.-C. ; Nebamon, son épouse, sa fille, le chat [H : notice British Museum] |
| IA-018 | 16.5 | présence d'un chat (texte et rigueur) | chat qui attrape des oiseaux [H : notice British Museum] |
| IA-018 | 16.4 | présence des oiseaux (partiel) | [H : notice British Museum] ; le traitement « plume par plume » reste [À VÉRIFIER] |
| IA-019 | 17.1 | conservation, datation, inventaire ; fiche IA-019 | British Museum EA37984, vers 1370 av. J.-C. [H : notice British Museum] |
| IA-019 | 17.5 | (partiel) représentation des figures | deux musiciennes de face [H : notice British Museum] |
| IA-020 | 18.1 | choix Edwin Smith / Ebers ; conservation, datation ; fiche IA-020 | Edwin Smith, vers 1600 av. J.-C., NYAM [H : notice NYAM] |
| IA-020 | 18.3 | contenu « selon le papyrus choisi » (texte et rigueur) | 48 cas de blessures ; au verso, formules et recettes [H : notice NYAM] |
| IA-006 | 22.4 | objet IA-006 à choisir | statuette en bronze, Met 04.2.441, 664–332 av. J.-C., H. 20,3 cm [H : notice Met] |
| IA-015 | 41.9 | (case grise, pas de [À VÉRIFIER] explicite) | Met 09.181.6, 90–120 apr. J.-C., encaustique sur tilleul, feuille d'or [H : notice Met] |

## 3. [À VÉRIFIER] restants pour les œuvres du registre

**Œuvres vérifiées en passe 2 (ce que la fiche ne dit pas)**
- **IA-017** : choix du lieu du chapitre 3 (14.1, 21.1) ; crédit photo et statut Open Access de l'objet 20.3.11 (14.3) ; lien avec « les textes funéraires » (14.6) ; historique de l'objet au-delà de 1920.
- **IA-018** : crédit photo et conditions de réutilisation du British Museum (16.1) ; position des poissons et espèces (16.3) ; traitement des oiseaux (16.4) ; pose du chat (16.5) ; tenue du chasseur (16.6) ; auteurs des lectures symboliques (16.7) ; harmonisation de la datation 1350 / 1370 avec le conseiller ; date d'achat à Henry Salt.
- **IA-019** : crédit et conditions du British Museum (17.1) ; « la musique, ça ne se peint pas » (17.2) ; identification des instruments (17.3) ; notation musicale (17.4) ; visages et robes, absence d'« exception » (17.5) ; fonction de la chapelle (17.7) ; date d'achat à Henry Salt.
- **IA-020** : feuillet reproduit, crédit et autorisation de la NYAM, rubriques rouges (18.1) ; simplification « diagnostic / pronostic » (18.3) ; accès aux soins (18.4). Pas de cote : ne pas en inventer.
- **IA-006** : pose assise (22.4, 45.8, 46.1) ; statut Open Access de l'objet 04.2.441 ; bornes de la frise 23.2 ; exemple de Vierge allaitante (45.8, 46.2, fiche à créer) ; historique de provenance.
- **IA-015** : statut Open Access de l'objet 09.181.6 ; liant de la détrempe (41.9) ; historique de provenance (crédit Rogers Fund, 1909 ; onglet non lu). Interdiction maintenue : ne pas dire que ce portrait vient du Fayoum.

**Œuvres non vérifiées ou en source secondaire (inchangées)**
- **IA-002**, Palette de Narmer : source secondaire ; lieu d'exposition actuel (Tahrir ou Grand Musée égyptien) non établi (P4–7).
- **IA-004**, tombe de Sennedjem : non vérifiée (10.6, 13.2, 13.4 restent grises).
- **IA-005**, tombe de Néfertari : non vérifiée (20–22).
- **IA-008**, coffre-chapelle d'Anubis : non vérifiée, aucune localisation actuelle (28, 39).
- **IA-009**, Amdouat de KV34, et **IA-010**, chat de Rê (Inherkhâou) : non vérifiées (30–32, 35).
- **IA-016**, Isis ou Sérapis serpentiforme : non vérifiée, aucune recherche en passe 2 (23, 43.3 reste grise).
- **IA-021**, relief agricole : non vérifiée, œuvre toujours à choisir (P15 inchangée).
- **NU-001**, Apédémak (Naqa) : source secondaire (34, 46.9).
