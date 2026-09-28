# Courant Continental — studio vidéo

*Les histoires vraies qui allument, ou éteignent, l’Afrique.*

Projet [Remotion](https://www.remotion.dev) (vidéo en React) pour produire les vidéos de la chaîne YouTube.

## Démarrer

```bash
npm install
npm run dev          # Remotion Studio : prévisualiser et modifier les props
```

## Compositions

| ID | Format | Contenu |
|---|---|---|
| `Intro` | 16:9, 6 s | Générique d’ouverture |
| `Trailer` / `TrailerVertical` | 16:9 / 9:16, 37 s | Bande-annonce de la chaîne (manifeste, sans données factuelles) |
| `Ep01Nigeria` | 16:9, ~6 min 40 | Épisode 1 — Nigeria : 14 contrats, zéro électron |
| `Ep01NigeriaShort` | 9:16, ~70 s | Version Short / TikTok de l’épisode 1 |
| `Episode` / `Short` | 16:9 / 9:16 | Gabarit vierge (contenu fictif à remplacer) |
| `Ep01Thumbnail`, `Thumbnail` | 1280×720 | Miniatures |

```bash
npx remotion render Ep01Nigeria out/ep01-nigeria.mp4
npx remotion still Ep01Thumbnail out/ep01-thumbnail.png
```

## Structure d’un épisode

Chaque épisode suit 8 sections (`src/episodes/schema.ts`) : Hook → Le projet → La promesse → Ce qui s’est réellement passé → Le point de rupture → Pourquoi ? → La leçon → Signature. Les durées se règlent par section pour caler l’image sur la voix off (`voiceover`, fichier dans `public/audio/`).

**Règle éditoriale :** tout chiffre, date ou citation porte une source affichée à l’écran. Une source marquée `À VÉRIFIER` s’affiche en rouge pour qu’aucun contenu non vérifié ne parte en ligne par erreur.

## Documents

- `docs/episodes/ep01-nigeria.md` — script de voix off, sources, checklist, métadonnées YouTube
- `docs/feuille-de-route.md` — saison 1 et méthode de production
