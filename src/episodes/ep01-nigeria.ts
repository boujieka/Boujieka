import { Episode } from "./schema";

// Épisode 1 — adapté de BANKABLE IS NOT ENOUGH, chapitre 1 « The MoU trap ».
// Chaque fait reprend une référence citée dans le chapitre. Revérifier chaque
// source primaire (liens dans docs/episodes/ep01-nigeria.md) avant publication.
export const ep01Nigeria: Episode = {
  series: "bankable",
  episodeNumber: 1,
  title: "Nigeria : 14 contrats, zéro électron",
  hook: [
    "Juillet 2016. Le Nigeria signe 14 contrats d’achat d’électricité solaire.",
    "1 125 mégawatts promis. Un tarif garanti pendant 20 ans.",
    "En 2020, pas un seul électron n’avait été livré. Que s’est-il passé ?",
  ],
  projet: {
    name: "Les 14 IPP solaires du Nigeria",
    location: "Nigeria · centrales de 50 à 100 MW · acheteur : NBET",
    figures: [
      { label: "PPA signés en juillet 2016", value: "14", source: "Green Street (s.d.) ; pv magazine (2019)" },
      { label: "Capacité cumulée promise", value: "1 125 MW", source: "Green Street (s.d.) ; pv magazine (2019)" },
      { label: "Tarif fixé pour 20 ans", value: "11,5 ¢/kWh", source: "Green Street (s.d.) ; pv magazine (2019)" },
    ],
  },
  promesse: {
    points: [
      "Objectif affiché : première électricité en 18 mois",
      "10 des 14 développeurs versent une caution de développement",
      "Des contrats signés — pas de simples protocoles d’accord",
    ],
  },
  realite: {
    events: [
      { date: "Juillet 2016", text: "Signature des 14 PPA à 11,5 ¢/kWh sur 20 ans", source: "pv magazine (2019)" },
      {
        date: "2018",
        text: "Le ministre : la Banque mondiale hésite à adosser les accords d’option à ce tarif",
        source: "Offgrid Nigeria (2018)",
      },
      { date: "2019", text: "Aucun bouclage financier. L’État veut baisser le tarif vers ~7,5 ¢", source: "pv magazine (2019)" },
      { date: "2020", text: "« 1 125 MW promis, zéro électron livré »", source: "Offgrid Nigeria (2020)" },
      { date: "2023", text: "Des analystes cherchent encore une sortie de l’impasse", source: "Energy for Growth Hub (2023)" },
    ],
  },
  rupture: {
    date: "2019",
    text: "Les prix du solaire ont chuté. L’État veut rouvrir un tarif déjà signé — et sans accords d’option ni garanties, aucun prêteur ne s’engage.",
    source: "pv magazine (2019) ; Energy for Growth Hub (2023)",
  },
  pourquoi: {
    points: [
      "Les promoteurs : des développeurs de solidité inégale",
      "Le processus : un tarif fixé administrativement, sans mise en concurrence",
      "Le système : des distributeurs qui ne paient pas intégralement l’acheteur",
      "L’État : accords d’option et garanties de risque jamais conclus",
    ],
  },
  lecon:
    "Les contrats étaient signés. Les cautions, versées. Mais personne n’avait répondu aux deux questions : le projet peut-il rembourser sa dette ? Et l’État peut-il porter ses engagements pendant 20 ans ?",
  sources: [
    "pv magazine 2019",
    "Offgrid Nigeria 2018, 2020",
    "Energy for Growth Hub 2023",
    "Green Street",
    "Solarplaza 2018",
    "E. Boujieka Kamga, Bankable Is Not Enough, ch. 1",
  ],
  durations: {
    hook: 20,
    projet: 40,
    promesse: 55,
    realite: 90,
    rupture: 65,
    pourquoi: 90,
    lecon: 30,
    signature: 10,
  },
};
