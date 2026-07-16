# FI-06 — Financement mixte et finance climatique pour l'accès à l'énergie

E-learning **auto-rythmé** de l'**Académie de la Transition Énergétique (ATE)**, conçu par **Aigle Group** en partenariat avec **Africa Emergence Group**.

Ce dépôt contient un cours en ligne **autonome** (HTML/CSS/JavaScript, sans dépendance ni étape de build) tiré de la fiche détaillée de formation **FI-06**.

## Contenu du cours

| Étape | Élément |
|-------|---------|
| Accueil | Présentation du parcours et suivi de progression |
| Présentation | Identité de la formation, enjeu, objectifs |
| Section 1 | Pourquoi le marché seul ne suffit pas |
| Section 2 | Instruments concessionnels et rehaussement de crédit |
| Section 3 | La finance climatique |
| Section 4 | Structurer un montage mixte |
| Section 5 | Monter le dossier et le défendre |
| Ressources | Récapitulatif des outils partenaires, dispositif, sources |
| Examen final | 15 questions · seuil de réussite **80 %** |
| Attestation | Attestation de réussite nominative (imprimable / PDF) |

Chaque section comprend le **contenu pédagogique**, une **étude de cas réelle et sourcée** (prioritairement africaine), la liste des **outils partenaires** (GCF, IFC, AfDB, ATIDI, GET.invest, SEforALL, IEA, IRENA…) et un **contrôle des acquis** à valider.

## Fonctionnalités

- **Parcours navigable** avec sommaire latéral et fil de progression.
- **Quiz par section** avec correction immédiate et explications.
- **Examen final** au seuil de 80 % (comme prévu dans la fiche).
- **Suivi de progression** enregistré localement dans le navigateur (`localStorage`).
- **Attestation de réussite** nominative, imprimable ou exportable en PDF.
- **Responsive** (ordinateur, tablette, mobile).

## Lancer le cours

Aucune installation n'est requise.

**Option 1 — ouverture directe**
Ouvrez `index.html` dans un navigateur moderne.

**Option 2 — serveur local** (recommandé)

```bash
python3 -m http.server 8000
# puis ouvrir http://localhost:8000
```

## Structure

```
index.html              Page unique (shell de l'application)
assets/
  css/styles.css        Styles (thème ATE, responsive, impression)
  js/content.js         Données du cours : contenu, cas, outils, quiz
  js/app.js             Logique : routage, progression, moteur de quiz
```

## Réutilisation des ressources partenaires

Les études de cas et données citées proviennent de ressources ouvertes des
partenaires (Green Climate Fund, IFC, AfDB, ATIDI, GET.invest, SEforALL, IEA,
IRENA, ESMAP, Convergence, PIDG…). Leur réutilisation suppose de **vérifier les
licences et de créditer les sources**, conformément à la note de partenariats.
Les données sont indicatives, à réactualiser à la date de la formation.

---

Version 1.0 — 15 juillet 2026 · Document de travail, diffusion restreinte.
Conçu par Emmanuel Boujieka Kamga, fondateur d'Aigle Group.
