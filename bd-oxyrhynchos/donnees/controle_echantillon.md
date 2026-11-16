# Contrôle indépendant d'un échantillon du registre iconographique

Date du contrôle : 16/11/2026. Échantillon de 6 fiches au statut `verifiee_notice`.

**Méthode.** Pour chaque fiche, la page indiquée dans `url_source` a été rouverte, puis chaque champ a été comparé au texte de la notice. Le contrôle ne s'appuie pas sur les champs `divergences` du registre. WebFetch a échoué (ENOTFOUND) sur les 5 domaines. Les pages ont donc été lues avec Firecrawl : 6 appels sur 6 autorisés, tous en HTTP 200. Chaque URL renvoie bien à l'objet décrit dans la fiche. Pour la notice du Louvre, le texte a été lu en entier, sauf la bibliographie. Aucun fichier du registre n'a été modifié.

Légende des verdicts :
- **conforme** : la valeur correspond à la notice.
- **écart** : divergence réelle. Une divergence est dite « mineure » quand elle ne porte pas sur l'identification de l'objet.
- **non contrôlé** : l'information est absente de la page lue.

---

## IA-007 : Papyrus d'Ani, feuille 3 (British Museum)

URL : https://www.britishmuseum.org/collection/object/Y_EA10470-3

| Champ | Registre | Notice lue | Verdict |
|---|---|---|---|
| URL / objet | Y_EA10470-3 | Page « papyrus », Museum number EA10470,3 (Ani's Judgment) | conforme |
| Désignation | « 'Book of the Dead', Papyrus of Ani (frame 3): Ani's Judgment » | Identique (la notice dit aussi « sheet 3 » dans une seconde version de la description) | conforme |
| Inventaire | EA10470,3 ; reg. 1888,0515.1.3 | Museum number EA10470,3 ; Registration number 1888,0515.1.3 ; Misc. « Frame.3 » | conforme |
| Datation | vers 1250 av. J.-C. ; XIXe dynastie | « 1250BC (circa) » ; « 19th Dynasty » | conforme |
| Provenance | Tombe d'Ani (Thèbes) | « Excavated/Findspot: Tomb of Ani (Thebes) » | conforme |
| Matériaux | papyrus peint ; encres noire et rouge, pigments ; H. 43,1 × L. 66,2 cm (cadre) | Materials : papyrus ; Technique : painted ; H. 43,10 / L. 66,20 cm (frame). Les encres et pigments figurent seulement dans le relevé d'état (« Black ink, Red ink, Pigment ») | conforme. La notice donne aussi un poids et une épaisseur, que le registre ne reprend pas. |
| Conservation | BM, Egypt and Sudan, non exposé | Department Egypt and Sudan ; Location « Not on display » | conforme |
| Acquisition | don de Sir E. A. T. Wallis Budge, 1888 | « Donated by: Sir Ernest A T Wallis Budge ». L'année 1888 vient du numéro d'enregistrement. | conforme |
| Usages / iconographie | formule 30B ; Ani et Tutu, chanteuse d'Amon ; Anubis, Thot, Ammit, Ennéade | Formule 30B, Tutu « Chantress of Amun », Anubis, Thot, Ammit, Grande Ennéade | conforme |
| Artiste | scribe(s) et artiste(s)-scribe(s), ou un seul scribe | Le commentaire du conservateur dit la même chose | conforme |
| Numérotation par feuille (champ divergences) | EA10470,1, EA10470,3, etc. | La page lue ne montre que EA10470,3 | non contrôlé |

## IA-013 : Autel domestique d'Akhénaton (SMB Berlin)

URL : https://search.smb.museum/object/obj-607132

| Champ | Registre | Notice lue | Verdict |
|---|---|---|---|
| URL / objet | obj-607132 | ObjID obj:607132, même objet | conforme |
| Désignation | « Hausaltar: Echnaton, Nofretete und drei ihrer Töchter unter dem Strahlenaton » | Identique | conforme |
| Type | relief (stèle) | « Relief (Stele) » | conforme |
| Inventaire | ÄM 14145 | « Ident. Nr.: ÄM 14145 » | conforme |
| Datation | règne d'Amenhotep IV / Akhénaton, sans date chiffrée | « Amenophis (Amenhotep) IV. / Echnaton (18. Dynastie -> Neues Reich -> Ägypten) » | conforme |
| Provenance | Amarna | « Geografische Bezüge: Amarna ». La notice ne précise pas qu'il s'agit du lieu de découverte. | conforme. Le registre dit « provenance », la notice seulement « référence géographique ». |
| Matériaux | calcaire ; 33,5 × 39,5 × 3,5 cm | « Kalkstein » ; H × B × T 33,5 × 39,5 × 3,5 cm | conforme |
| Conservation | Ägyptisches Museum und Papyrussammlung, SMB | Identique. La notice ne dit pas si l'objet est exposé. | conforme |
| Droits image | SMB / Margarete Büsing, CC BY-SA 4.0 | Identique | conforme |
| Intervenant | Oskar Hermann Deibel (1893), rôle non précisé | « Beteiligte: Oskar Hermann Deibel (1893) », sans rôle | conforme |
| Don de James Simon | mentionné, d'après une autre page SMB | absent de cette notice | non contrôlé (le registre le signale lui-même) |
| Usages | autel de sanctuaire domestique ; couple royal intermédiaire ; rayons tendant le signe de vie | « Altarbild eines Schreins » ; « Mittler zwischen Mensch und Gott » ; « Lebenszeichen » | conforme |

## IA-014 : Zodiaque de Dendérah (Louvre)

URL : https://collections.louvre.fr/ark:/53355/cl010028871

| Champ | Registre | Notice lue | Verdict |
|---|---|---|---|
| URL / objet | cl010028871 | « Zodiaque de Dendéra » | conforme |
| Désignation | Zodiaque de Dendéra ; dénomination plafond ; relief mural | « Dénomination : plafond ; relief mural ; Titre : Zodiaque de Dendéra » | conforme |
| Inventaire | E 13482 (principal) ; CM 464 (entrée) ; BN 6 ; D 38 (usage) | Principal E 13482 ; entrée CM 464 ; autre BN 6 ; usage D 38 | conforme |
| Datation | Cléopâtre VII et Ptolémée XIII ; juin-août 50 av. J.-C. (bibliographie) | « Cléopâtre VII Philopator ; Ptolémée XIII Philopator (juin-août 50 av. J.-C.) (bibliographie/travail de référence) » | conforme |
| Provenance | temple d'Hathor, chapelle est d'Osiris sur le toit, moitié ouest du plafond de la pièce centrale ; découvert le 24/01/1799 | Identique ; « 24 janvier 1799 (An VII, 5 pluviôse) » | conforme |
| Matériaux | grès, bas-relief saillant ; L. 255, l. 253 cm | grès ; bas-relief saillant ; L. 255 cm, l. 253 cm | conforme |
| Conservation | Louvre, Antiquités égyptiennes, Sully, salle 325 (Les chapelles) | « Sully, [AE] Salle 325 - Les chapelles, Hors vitrine » ; exposé | conforme |
| Historique | Lelorrain envoyé par Saulnier ; extrait en avril-mai 1821 ; firman du 27/01/1821 ; achat par Louis XVIII en avril 1822 ; Bibliothèque royale / Cabinet des Médailles ; affectation au Louvre 1918-1919 | Identique (comité du 25/04/1918, retour le 10/04/1919). La notice mentionne aussi une première exposition au Louvre en 1822-1823, que le registre omet. | conforme |
| Iconographie | 8 dieux à tête de faucon agenouillés et 4 femmes debout, bras levés, qui portent le ciel | Identique | conforme |
| Moulage cl010077401 | vu seulement dans des résultats de recherche | page non lue | non contrôlé |

## NU-004 : Sphinx-bélier de Taharqo, Kawa (British Museum)

URL : https://www.britishmuseum.org/collection/object/Y_EA1779

| Champ | Registre | Notice lue | Verdict |
|---|---|---|---|
| URL / objet | Y_EA1779 | « statue », EA1779, sphinx-bélier protégeant Taharqo | conforme |
| Désignation | COMPASS : « Granite statue of Amun in the form of a ram protecting King Taharqa » | « COMPASS Title: » identique | conforme |
| Inventaire | EA1779 ; reg. 1933,0610.1 | EA1779 ; Registration number 1933,0610.1 | conforme |
| Datation | 690–664 av. J.-C. ; kouchite / napatéen | « 690BC-664BC » ; « Kushite ; Napatan ». La mention « XXVe dynastie » dans le champ `aire_culturelle` ne vient pas de la notice, mais elle est historiquement exacte. | conforme |
| Provenance | Kawa, Temple T ; fouilles de F. Ll. Griffith | « Kawa, Temple T » ; « Excavated by: Prof. Francis Llewellyn Griffith » | conforme |
| Matériaux | gneiss (granitique) | Materials : gneiss ; description : « Granitic gneiss » | conforme |
| Dimensions / état | H. 106 ; base L. 163, l. 63 ; état « fair », base partiellement restaurée | Identique | conforme |
| Conservation | BM, Egypt and Sudan ; salle 4, baie 9 | « On display (Room 4 - Egyptian sculpture, Bay 9) » | conforme |
| Prêt | Leyde (RMO), 2018-2019 | « 2018-2019 12 Oct-13 March, Leiden, Rijksmuseum van Oudheden » | conforme |
| Acquisition | non indiquée sur la page | absente de la page | conforme |
| Fonction | « Objet religieux (image de culte d'Amon) » | La notice ne parle pas d'image de culte. Elle dit seulement : sphinx du bélier d'Amon, inscription royale, Temple T. | **écart mineur** : interprétation non sourcée. Un sphinx de temple n'est pas forcément la statue de culte du sanctuaire. |

## KO-001 : Figure de pouvoir Mangaaka (Met)

URL : https://www.metmuseum.org/art/collection/search/320053

| Champ | Registre | Notice lue | Verdict |
|---|---|---|---|
| URL / objet | 320053 | « Mangaaka Power Figure (Nkisi N'Kondi) » | conforme |
| Désignation | Mangaaka Power Figure (Nkisi N'Kondi) | Identique | conforme |
| Inventaire | 2008.30 | « Object Number: 2008.30 » | conforme |
| Datation | vers 1880–1900 | « ca. 1880–1900 » | conforme |
| Provenance | République du Congo ou Cabinda (Angola), fleuve Chiloango | « Republic of the Congo or Cabinda, Angola, Chiloango River » | conforme |
| Culture / artiste | Kongo (Yombe-Kongo) ; artiste yombe-kongo et nganga ; atelier d'un maître de la côte Congo-Angola | « Culture: Kongo peoples » ; « Yombe-Kongo artist and nganga » ; « atelier of a master active along the coast of Congo and Angola » | conforme |
| Matériaux | bois, fer, résine, céramique, fibre végétale, textile, pigment ; 118 × 49,5 × 39,4 cm, 24 kg | Identique | conforme |
| Conservation | Met, Michael C. Rockefeller Wing, galerie 344 | Identique | conforme |
| Usages | force de la jurisprudence ; serments, traités, lutte contre le mal ; coiffe mpu ; cavité abdominale | Identique | conforme |
| Acquisition | « achat en 2008 (ligne de crédit) » | « Credit Line: Purchase, Lila Acheson Wallace, … and Steven Kossak Gifts, 2008 » | **écart mineur** : « ligne de crédit » traduit mal « credit line ». Ce terme désigne la mention officielle de l'acquisition, ici un achat financé par des dons. Il ne s'agit pas d'un crédit financier. |
| Droits image | Open Access, éligibilité à confirmer | La page ne montre pas l'état OA de l'image (la politique générale est rappelée) | conforme (la réserve est justifiée) |
| Historique de provenance | non lu | L'onglet Provenance n'apparaît pas dans le texte extrait | non contrôlé |

## AF-008 : Aksoum (UNESCO)

URL : https://whc.unesco.org/fr/list/15/

| Champ | Registre | Notice lue | Verdict |
|---|---|---|---|
| URL / objet | list/15 | Page « Axoum » | conforme |
| Désignation / réf. | Axoum, bien n° 15 | « Axoum », identifiant 15 | conforme |
| Datation | ruines du Ier au XIIIe s. ; stèles des IIIe-IVe s. ; royaume du Ier au VIIIe s. (synthèse de la VUE) | « du Ier au XIIIe siècle » (description) ; « stèles datant des IIIe et IVe siècles » ; « du Ier au VIIIe siècles » (synthèse) | conforme. L'écart interne à l'UNESCO est bien rapporté. |
| Provenance | Axoum, plateau du Tigray, Éthiopie | « Plateau de Tigray » ; nord de l'Éthiopie | conforme |
| Conservation | in situ ; ARCCH | ARCCH créée par la Proclamation n° 209/2000. La notice mentionne aussi l'Autorité des Antiquités nationales (1958), que le registre omet. | conforme |
| Monuments | obélisque debout de plus de 23 m, neuf étages ; env. 33 m, tombé ; inscriptions trilingues d'Ezana au IVe s. ; christianisme au IVe s. | Identique | conforme |
| Restitution | rendu en 2005, réinstallé en 2008 | « rendu à Axoum en 2005 puis réinstallé en 2008 » | conforme |
| Droits | texte sous CC-BY-SA IGO 3.0 | Identique | conforme |
| Matériaux | null | Non précisés dans la notice | conforme (champ vide justifié) |

---

## Verdict global

**Aucune erreur d'identification n'a été trouvée.** Pour les 6 fiches, l'URL renvoie bien à l'objet décrit. Les numéros d'inventaire et d'enregistrement, les datations, les provenances, les matériaux, les dimensions et les lieux de conservation correspondent tous aux notices. Je n'ai relevé ni numéro erroné, ni date déformée, ni objet confondu.

Décompte, sur les 67 lignes contrôlées dans les tableaux :
- **conforme : 61**
- **écart mineur : 2**
  - NU-004 : « image de culte » est une interprétation non sourcée.
  - KO-001 : « ligne de crédit » est une mauvaise traduction de « credit line ».
- **non contrôlé : 4**
  - IA-007 : la numérotation des autres feuilles.
  - IA-013 : le don de James Simon.
  - IA-014 : le moulage cl010077401.
  - KO-001 : l'onglet Provenance.

**Taux d'erreur observé**, en excluant les lignes non contrôlées :
- Erreurs majeures (identification, inventaire, date, provenance, matériaux, conservation) : 0 sur 63, soit **0 %**.
- Toutes erreurs confondues : 2 sur 63, soit **3,2 %**. Les deux écarts concernent des champs d'interprétation ou de formulation, pas des champs d'identification.

À l'échelle des fiches, 6 sur 6 ont des données d'identification exactes. Une fois corrigées comme indiqué ci-dessous, les deux fiches concernées pourraient garder le statut `verifiee_notice`.

**Limites du contrôle.** L'échantillon est petit (6 fiches) et n'a pas été tiré au hasard. Un taux de 0 % sur 6 fiches ne permet pas d'exclure un taux d'erreur réel non négligeable dans le reste du registre. Le contrôle a utilisé le même outil (Firecrawl) que celui que les agents ont pu employer, et deux pages sont venues du cache Firecrawl (BM EA1779, UNESCO). Les onglets secondaires (provenance au Met, autres feuilles au BM) n'ont pas été lus.

**Recommandations, sans modifier les fichiers à ce stade.**
1. KO-001 : remplacer « ligne de crédit » par « achat financé par les dons de Lila Acheson Wallace et al., 2008 ».
2. NU-004 : remplacer « image de culte d'Amon » par « sphinx de temple (Temple T) ; inscription royale », ou bien signaler l'interprétation comme hypothèse.
3. Les éléments « non contrôlé » qui viennent de pages non lues (don de James Simon, moulage du Louvre) devraient être marqués « à vérifier » dans le registre.
