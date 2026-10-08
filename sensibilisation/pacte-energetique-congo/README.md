# Le courant pour tous ? : le Pacte national énergétique en BD

BD citoyenne de 20 pages (plus une page « À propos »), version 3, pour comprendre et suivre le
*Pacte National Énergétique de la République du Congo* (Mission 300, septembre 2025, 37 pages).

Structure en trois actes : I. Nous avons un problème (p. 1-6) · II. Mais comment ? (p. 7-15) ·
III. Et qui va vérifier ? (p. 16-20), avec « Qui fait quoi ? » (p. 15), un tableau de bord
citoyen (p. 16) et une fiche de suivi à photocopier ou découper (p. 19).

Le personnage « PNE » ne dit que ce qui est écrit dans le Pacte ; quand un personnage
lui prête autre chose, il répond « Je n'ai pas dit ça. »

- `index.html` : l'album (dessiné en SVG ; personnages, décors et infographies générés par le script de la page).
- `export/page-XX.png` : chaque page au format A4 (1240 × 1754 px).
- `export/le-courant-pour-tous-bd.pdf` : l'album en A4, une page par feuille.
- `export.mjs` : régénère PNG et PDF (`node export.mjs`, nécessite Playwright).
- `v1/` : la première version (13 planches en silhouettes). La V2 est dans l'historique git.

Règles éditoriales : un chiffre = une source (page du Pacte citée sur chaque page) ; une promesse = une date ;
une date échue = un statut à vérifier ; un résultat = une preuve. Personnages fictifs.
Ce qui n'est pas dans le Pacte porte un tampon bleu. Les répliques en lingala sont à faire relire
par un locuteur natif ; le QR code (dernière page) a été vérifié par décodage, mais le lien reste à tester sur téléphone avant impression.
