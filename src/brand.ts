import "@fontsource/montserrat/600.css";
import "@fontsource/montserrat/800.css";
import "@fontsource/montserrat/900.css";
import "@fontsource/montserrat/600-italic.css";
import "@fontsource/inter/400.css";
import "@fontsource/inter/500.css";
import "@fontsource/inter/700.css";
import { continueRender, delayRender } from "remotion";

// Polices embarquées (pas d'accès réseau requis au rendu).
if (typeof document !== "undefined") {
  const handle = delayRender("Chargement des polices");
  Promise.all(
    ["600 20px Montserrat", "800 20px Montserrat", "900 20px Montserrat", "italic 600 20px Montserrat",
     "400 20px Inter", "500 20px Inter", "700 20px Inter"].map((f) => document.fonts.load(f)),
  ).then(() => continueRender(handle), () => continueRender(handle));
}

// Couleurs relevées sur le logo Courant Continental.
export const colors = {
  navy: "#0B1E4A",
  navyDeep: "#060F28",
  green: "#1E6B2F",
  greenLight: "#2E8B45",
  gold: "#D4A437",
  goldLight: "#F2CF6B",
  white: "#FFFFFF",
  offWhite: "#F4F1EA",
  muted: "#9FB0CC",
  alert: "#E0533D",
};

export const fonts = {
  title: "Montserrat, 'Liberation Sans', Arial, sans-serif",
  body: "Inter, 'Liberation Sans', Arial, sans-serif",
};

export const TAGLINE = "Les histoires vraies qui allument, ou éteignent, l’Afrique.";

export const MANIFESTO = [
  "En Afrique, derrière chaque mégawatt, il y a une histoire.",
  "Derrière chaque projet, il y a des décisions.",
  "Et derrière chaque décision, quelqu’un paie la facture.",
];

export const SERIES = {
  delestage: { label: "Chroniques du Délestage", color: colors.alert },
  bankable: { label: "Bankable ou pas ?", color: colors.gold },
  lumiere: { label: "Quand l’Afrique allume la lumière", color: colors.greenLight },
  jamais: { label: "Le Projet qui n’est jamais arrivé", color: colors.muted },
  ppa: { label: "Dans les coulisses du PPA", color: colors.goldLight },
  facture: { label: "Qui paie la facture ?", color: colors.alert },
  cinqMinutes: { label: "1 Projet, 5 Minutes", color: colors.greenLight },
} as const;

export type SeriesKey = keyof typeof SERIES;
