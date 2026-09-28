import { Episode } from "./schema";

// ÉPISODE MODÈLE — tout le contenu est FICTIF / à remplacer.
// Chaque chiffre, date et citation doit être remplacé par une donnée réelle
// et sourcée (document public, rapport, contrat, presse) avant publication.
export const episodeModele: Episode = {
  series: "delestage",
  episodeNumber: 1,
  title: "[Titre de l’épisode]",
  hook: [
    "En [ANNÉE], ce projet devait électrifier [N] personnes.",
    "[X] ans plus tard, il n’a toujours pas produit un seul kilowattheure.",
    "Que s’est-il passé ?",
  ],
  projet: {
    name: "[Nom du projet]",
    location: "[Pays · Région]",
    figures: [
      { label: "Capacité annoncée", value: "[N] MW", source: "À VÉRIFIER" },
      { label: "Coût estimé", value: "[N] M$", source: "À VÉRIFIER" },
      { label: "Bénéficiaires visés", value: "[N]", source: "À VÉRIFIER" },
    ],
  },
  promesse: {
    points: [
      "[Mise en service prévue en ANNÉE]",
      "[Tarif annoncé / baisse des délestages]",
      "[Emplois / industrialisation promis]",
    ],
    quote: {
      text: "[Citation exacte d’un décideur au lancement]",
      author: "[Nom, fonction]",
      source: "À VÉRIFIER",
    },
  },
  realite: {
    events: [
      { date: "[ANNÉE]", text: "[Signature du protocole d’accord]", source: "À VÉRIFIER" },
      { date: "[ANNÉE]", text: "[Négociation du PPA]", source: "À VÉRIFIER" },
      { date: "[ANNÉE]", text: "[Recherche de financement]", source: "À VÉRIFIER" },
      { date: "[ANNÉE]", text: "[Blocage / renégociation]", source: "À VÉRIFIER" },
    ],
  },
  rupture: {
    date: "[MOIS ANNÉE]",
    text: "[Le moment précis où le projet a commencé à dérailler]",
    source: "À VÉRIFIER",
  },
  pourquoi: {
    points: [
      "[Cause 1 : ex. risque de paiement de l’acheteur unique]",
      "[Cause 2 : ex. garantie souveraine non obtenue]",
      "[Cause 3 : ex. tarif incompatible avec le coût du service]",
    ],
  },
  lecon: "[Le problème n’était pas l’absence de financement. Le projet n’était pas bancable dans ses conditions initiales.]",
  sources: ["[Source 1 — à compléter]", "[Source 2 — à compléter]"],
  durations: {
    hook: 12,
    projet: 30,
    promesse: 45,
    realite: 60,
    rupture: 45,
    pourquoi: 60,
    lecon: 25,
    signature: 10,
  },
};
