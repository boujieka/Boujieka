import re, sys, pathlib
root = pathlib.Path(sys.argv[1])
bible = (root/'bible-serie.md').read_text(encoding='utf-8')
edit = (root/'relecture-editoriale.md').read_text(encoding='utf-8')
acts = [(root/'episodes'/f'acte-{i}.md').read_text(encoding='utf-8') for i in range(1,6)]

def section(text, start_pat, stop_pat):
    m = re.search(start_pat, text, re.M)
    if not m: return ''
    rest = text[m.start():]
    nl = rest.find('\n') + 1
    n = re.search(stop_pat, rest[nl:], re.M)
    return rest[: nl + n.start()] if n else rest

troupe = section(bible, r'^## 3\. La troupe', r'^## ').strip()
troupe = troupe.replace('## 3. La troupe (voix et running gags)', '### Fiches personnages : voix et running gags')
garde = section(bible, r'^## 5\. Garde-fous', r'^## ').strip().replace('## 5.', '###')
lexique = section(edit, r'^## \(d\) Lexique consolidé', r'^## Contrôle du format').strip()
lexique = re.sub(r'^## \(d\) ', '## ', lexique, flags=re.M)

# sommaire + points à valider
toc, todo = [], []
for a in acts:
    for line in a.splitlines():
        if line.startswith('# ACTE'):
            toc.append(f"\n**{line[2:].strip()}**\n")
        elif line.startswith('### Épisode'):
            toc.append(f"- {line[4:].strip()}")
    for ep in re.split(r'(?m)^(?=### Épisode)', a):
        h = re.match(r'### (Épisode \d+)[^\n]*', ep)
        if not h: continue
        pv = section(ep, r'^#### Points à valider', r'^#{2,4} ')
        body = '\n'.join(pv.splitlines()[1:]).strip()
        if body:
            todo.append(f"### {h.group(1)}\n{body}\n")

head = f"""# COURANT CONTINENTAL — CAMEROUN
## « Les mégawatts sont arrivés… mais la bière est chaude ! »
### Saison 1 — Scénario complet pour l'illustrateur
**20 épisodes · 5 actes · 80 planches · 400 cases**

*Document de travail confidentiel. Version du scénario après relecture croisée (faits, garde-fous, continuité, humour et langue). Texte à faire valider par un relecteur camerounais (langue) et par un juriste (épisodes 6, 11, 12, 17) avant mise en couleur et impression.*

---

## Sommaire
- Guide de l'illustrateur
- Fiches personnages
- Garde-fous visuels et éditoriaux
{chr(10).join(toc)}
- Annexe A — Lexique de la série
- Annexe B — Points à valider avant impression

---

## Guide de l'illustrateur

### Format
- **4 planches par épisode, 5 cases par planche.** Chaque case du scénario donne une colonne **Image** (ce qu'on dessine) et une colonne **Texte** (bulles, récitatifs, onomatopées).
- Après les planches viennent les **pages documentaires** (carnet de Fifi, chiffres du Pacte, facture cachée de la panne, qui possède quoi, tableau de bord). Elles se mettent en page comme une page de carnet ou un tableau à la craie, **pas** comme un rapport.
- Les rubriques « Mini-lexique » et « Notes pour le dessinateur » s'adressent à l'équipe. Le lexique est imprimé en bas de la dernière planche ; les notes ne sont pas imprimées.
- Les rubriques « Points à valider » **ne sont pas imprimées** ; elles sont regroupées dans l'annexe B.

### Le décor principal : *Le Dernier Kilowatt*, quartier Nkoagne (Douala, fictif)
Bar de quartier : chaises et tables en plastique, comptoir avec une vieille télé, néon d'enseigne à moitié éteint, groupe électrogène qui fume devant la boutique d'à côté, motos-taxis dans la rue. Ce lieu ouvre (épisode 1) et ferme (épisode 20) la saison : garder **les mêmes cadrages** aux deux bouts pour que le lecteur sente la boucle (première gorgée de Boris, dessinée au même cadrage).

### Dispositifs visuels récurrents
| Dispositif | Comment le dessiner | Où |
|---|---|---|
| **Baromètre du courant de Nkoagne** | Grand tableau noir derrière le comptoir. **Craie blanche = chiffre mesuré** ; **craie jaune = objectif** du Pacte. Une ligne nouvelle par épisode. | Tous les épisodes |
| **Chrono de la coordination** | Deux horloges côte à côte : « Centrale prête » et « Ligne prête ». Entre les deux, l'écart en années ou en mois, et parfois un compteur de factures qui tourne. | Ép. 5 à 8, 12, 15, 17, 18 |
| **Tribunal des mégawatts** | Barrages, pylônes et compteurs personnifiés à la barre ; décor de tribunal de quartier. **Personne n'est condamné** : le verdict porte sur la chaîne et les preuves. | Ép. 6, 8, 19 |
| **Bulle « Attention, piège ! »** | Bulle triangulaire jaune de Grâce, pour toute comparaison de coût. | Ép. 5 à 8, 17 |
| **Monsieur Congélateur** | Congélateur du bar avec des yeux, une moustache, des bras. Son humeur suit la tension électrique (givré quand tout va bien, dégoulinant en délestage). | Ép. 1, 3, 12, 20 |
| **La caisse de bières** | Toujours visible quelque part au bar ; elle change de main sans jamais être gagnée, puis finit rangée dans Monsieur Congélateur (ép. 20). | Fil rouge |
| **Le client à la casquette** | Le client du comptoir de l'épisode 1 (blague du Tchad, « Qui va payer les bières chaudes ? »). Même casquette à chacune de ses apparitions. | Ép. 1, 4, 6, 18, 20 |
| **Monsieur 2030** | Costume trois-pièces, cartable débordant de documents. C'est l'allégorie **d'un document** (le Compact), **pas** d'une personne réelle : aucun trait d'un responsable existant. | Actes IV et V |

### Ce qu'on ne dessine jamais
- Le visage, le nom ou la silhouette reconnaissable d'une **personne réelle** (ministre, dirigeant, élu).
- Les **logos réels** d'entreprises (Globeleq, EDF, SOCADEL, etc.) : on écrit leur nom quand le scénario le demande, sans reproduire le logo.
- Une **catastrophe** à Song Loulou ou ailleurs : aucune source n'en signale.
- Des **riverains** ou des **habitants du Nord** présentés comme des obstacles ou de manière caricaturale ; les riverains de Memve'ele sont dessinés avec dignité.
- Toute caricature d'un **accent, d'une région, d'une communauté, du Tchad** ou d'un pays voisin.
- Les photos de presse : elles servent de **référence d'ambiance** seulement, on redessine tout.

---

## Fiches personnages
{troupe}

> **Proposition de silhouettes (à valider avec l'auteur)** : Boris (bleu de travail, masque de soudeur relevé sur le front) ; Pater Glaçon (torchon sur l'épaule, craie à la main) ; Tonton Mballa (crayon de menuisier derrière l'oreille) ; Mami Chantal (peigne et sèche-cheveux, tenues éclatantes) ; Fifi (carnet à spirale, stylo, téléphone) ; Grâce (casque de chantier, multimètre) ; Junior (casquette à l'envers, batterie de moto en bandoulière) ; Papa Tchinda (vieille veste de la SONEL) ; Mami Ngo (pagne, marmite) ; Mola Ndip (sacoche de pièces détachées) ; Adamou (boubou brodé, mètre ruban de tailleur autour du cou) ; le Kilowatt (petite étincelle jaune aux grands yeux).

---

## Garde-fous visuels et éditoriaux
{garde}

---
"""

body = '\n\n---\n\n'.join(a.strip() for a in acts)
tail = f"""

---

# Annexe A — Lexique de la série
*(Consolidé par la relecture éditoriale ; les avis sont ceux du relecteur IA et doivent être confirmés par un relecteur camerounais.)*

{lexique}

---

# Annexe B — Points à valider avant impression
*(Repris des rubriques « Points à valider » de chaque épisode. Rien de cette annexe ne s'imprime.)*

{chr(10).join(todo)}
"""
out = root/'album-saison-1-illustrateur.md'
out.write_text(head + body + tail, encoding='utf-8')
print(out, len((head+body+tail).splitlines()), 'lignes')
