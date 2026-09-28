# Feuille de route éditoriale — saison 1

Épisodes tirés directement du chapitre 1 de *Bankable Is Not Enough* (matière déjà sourcée) :

| # | Épisode | Série | Angle | Matière dans le chapitre 1 |
|---|---|---|---|---|
| 1 | Nigeria : 14 contrats, zéro électron | Bankable ou pas ? | Le contrat signé qui ne devient jamais finançable | Complète (§ intro, 1.3, 1.5) |
| 2 | Nachtigal : bancable, et après ? | Quand l’Afrique allume la lumière / Bankable ou pas ? | Un succès de financement… puis la garantie de paiement tirée en 2025 | Partielle (§ 1.6) — à compléter |
| 3 | Qua Iboe : de bons sponsors ne suffisent pas | Le Projet qui n’est jamais arrivé | 533 MW, garantie BM de 150 M$, abandonné | Partielle (§ 1.2, 1.3) |
| 4 | Ghana : payer l’électricité qu’on n’utilise pas | Qui paie la facture ? | La « deuxième sortie » : les contrats qui bouclent et deviennent un passif | Partielle (§ 1.5) |

Pour l’épisode 2, le chapitre donne 3 faits sourcés (accord de co-développement État/EDF/IFC/utility ; tranche en monnaie locale d’une maturité sans précédent ; garantie de paiement largement tirée en 2025). C’est insuffisant pour 6–7 minutes : il faut documenter la chronologie (capacité, coût, dates de bouclage et de mise en service) à partir de sources primaires avant d’écrire.

## Méthode de production d’un épisode

1. Dupliquer `src/episodes/modele.ts` → `src/episodes/epXX-nom.ts`, remplir chaque champ avec sa source.
2. Écrire le script de voix off dans `docs/episodes/epXX-nom.md` (même découpage en 8 sections).
3. Enregistrer la voix off, mesurer la durée de chaque section, ajuster `durations`.
4. Placer l’audio dans `public/audio/` et renseigner `voiceover`.
5. Enregistrer la composition dans `src/Root.tsx`, prévisualiser avec `npm run dev`, rendre.
