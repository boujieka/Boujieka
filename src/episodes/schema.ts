import { z } from "zod";

const sourced = z.object({
  label: z.string(),
  value: z.string(),
  // Toute donnée chiffrée DOIT porter une source. « À VÉRIFIER » s'affiche en rouge.
  source: z.string(),
});

const event = z.object({
  date: z.string(),
  text: z.string(),
  source: z.string().optional(),
});

// Durée de chaque section en secondes (ajuster à la voix off).
const durations = z.object({
  hook: z.number().min(1),
  projet: z.number().min(1),
  promesse: z.number().min(1),
  realite: z.number().min(1),
  rupture: z.number().min(1),
  pourquoi: z.number().min(1),
  lecon: z.number().min(1),
  signature: z.number().min(1),
});

export const episodeSchema = z.object({
  series: z.enum(["delestage", "bankable", "lumiere", "jamais", "ppa", "facture", "cinqMinutes"]),
  episodeNumber: z.number().int().min(0),
  title: z.string(),
  hook: z.array(z.string()).min(1),
  projet: z.object({
    name: z.string(),
    location: z.string(),
    figures: z.array(sourced).max(4),
    image: z.string().optional(),
  }),
  promesse: z.object({
    points: z.array(z.string()).max(4),
    quote: z.object({ text: z.string(), author: z.string(), source: z.string() }).optional(),
  }),
  realite: z.object({ events: z.array(event).max(5) }),
  rupture: z.object({ date: z.string(), text: z.string(), source: z.string().optional() }),
  pourquoi: z.object({ points: z.array(z.string()).max(4) }),
  lecon: z.string(),
  sources: z.array(z.string()),
  voiceover: z.string().optional(), // chemin dans public/, ex. "audio/ep01.mp3"
  music: z.string().optional(),
  durations,
});

export type Episode = z.infer<typeof episodeSchema>;
export type SectionKey = keyof Episode["durations"];
export const SECTION_ORDER: SectionKey[] = [
  "hook",
  "projet",
  "promesse",
  "realite",
  "rupture",
  "pourquoi",
  "lecon",
  "signature",
];
