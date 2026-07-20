/**
 * Génération de courbes de charge horaires à partir de profils-types sectoriels.
 *
 * Mode de saisie simplifié prévu par le schéma : lorsque la donnée horaire
 * réelle n'est pas disponible, on synthétise un vecteur de 8760 pas à partir
 * d'un gabarit journalier sectoriel, mis à l'échelle de la consommation
 * annuelle du site.
 */

import { HOURS_PER_YEAR } from "../config";

export type SectorTemplate =
  | "industrie_continue"
  | "industrie_2x8"
  | "tertiaire_bureaux"
  | "commerce"
  | "data_center"
  | "hopital"
  | "telecom"
  | "residentiel";

interface SectorShape {
  label: string;
  /** Forme journalière relative sur 24 h (valeurs positives, sans unité). */
  hourly: number[];
  /** Modulation hebdomadaire : facteur appliqué du lundi (0) au dimanche (6). */
  weekly: number[];
  /** Criticité suggérée de la charge. */
  suggestedCriticality: "faible" | "moyenne" | "elevee" | "critique";
}

// Gabarits journaliers relatifs (24 valeurs, heure 0 → 23).
const SHAPES: Record<SectorTemplate, SectorShape> = {
  industrie_continue: {
    label: "Industrie en continu (3x8)",
    hourly: Array(24).fill(1),
    weekly: [1, 1, 1, 1, 1, 0.95, 0.9],
    suggestedCriticality: "critique",
  },
  industrie_2x8: {
    label: "Industrie postée (2x8)",
    hourly: [0.4, 0.4, 0.4, 0.4, 0.5, 0.7, 0.9, 1, 1, 1, 1, 1, 0.95, 1, 1, 1, 1, 0.9, 0.7, 0.55, 0.45, 0.4, 0.4, 0.4],
    weekly: [1, 1, 1, 1, 1, 0.6, 0.4],
    suggestedCriticality: "elevee",
  },
  tertiaire_bureaux: {
    label: "Tertiaire / bureaux",
    hourly: [0.25, 0.22, 0.2, 0.2, 0.2, 0.25, 0.4, 0.65, 0.9, 1, 1, 0.95, 0.85, 0.95, 1, 1, 0.9, 0.7, 0.45, 0.35, 0.3, 0.28, 0.27, 0.26],
    weekly: [1, 1, 1, 1, 1, 0.45, 0.35],
    suggestedCriticality: "moyenne",
  },
  commerce: {
    label: "Commerce / distribution",
    hourly: [0.3, 0.28, 0.27, 0.27, 0.28, 0.3, 0.4, 0.6, 0.8, 0.95, 1, 1, 1, 1, 1, 1, 0.98, 0.95, 0.9, 0.8, 0.6, 0.45, 0.38, 0.33],
    weekly: [0.9, 0.9, 0.95, 0.95, 1, 1, 0.7],
    suggestedCriticality: "moyenne",
  },
  data_center: {
    label: "Data center",
    hourly: Array(24).fill(1),
    weekly: [1, 1, 1, 1, 1, 1, 1],
    suggestedCriticality: "critique",
  },
  hopital: {
    label: "Hôpital / santé",
    hourly: [0.6, 0.58, 0.57, 0.57, 0.58, 0.62, 0.72, 0.85, 0.95, 1, 1, 0.98, 0.95, 0.98, 1, 0.98, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.66, 0.62],
    weekly: [1, 1, 1, 1, 1, 0.95, 0.92],
    suggestedCriticality: "critique",
  },
  telecom: {
    label: "Site télécom / relais",
    hourly: [0.85, 0.82, 0.8, 0.8, 0.82, 0.85, 0.9, 0.95, 1, 1, 0.98, 0.96, 0.95, 0.96, 0.98, 1, 1, 1, 0.98, 0.95, 0.92, 0.9, 0.88, 0.86],
    weekly: [1, 1, 1, 1, 1, 1, 1],
    suggestedCriticality: "critique",
  },
  residentiel: {
    label: "Résidentiel / logement",
    hourly: [0.45, 0.4, 0.38, 0.37, 0.38, 0.45, 0.65, 0.8, 0.7, 0.55, 0.5, 0.5, 0.55, 0.5, 0.48, 0.5, 0.6, 0.8, 1, 1, 0.95, 0.8, 0.65, 0.52],
    weekly: [0.95, 0.95, 0.95, 0.95, 1, 1, 1],
    suggestedCriticality: "faible",
  },
};

export const sectorTemplates = Object.entries(SHAPES).map(([key, s]) => ({
  key: key as SectorTemplate,
  label: s.label,
  suggestedCriticality: s.suggestedCriticality,
}));

export function getSectorMeta(template: SectorTemplate): SectorShape {
  return SHAPES[template];
}

/**
 * Construit un vecteur de charge horaire (kW) de 8760 pas à partir d'un gabarit
 * sectoriel, calibré pour restituer exactement `annualConsumptionKwh` sur l'année.
 *
 * @param template   Gabarit sectoriel.
 * @param annualConsumptionKwh Consommation annuelle cible (kWh).
 * @param peakDemandKw Optionnel : plafonne le profil à la pointe déclarée.
 */
export function generateSectoralProfile(
  template: SectorTemplate,
  annualConsumptionKwh: number,
  peakDemandKw?: number,
): number[] {
  const shape = SHAPES[template];
  const raw = new Array<number>(HOURS_PER_YEAR);

  // Le pas h=0 correspond au 1er janvier 00h. On aligne le jour de semaine :
  // jour 0 = lundi pour rester déterministe et reproductible.
  let sum = 0;
  for (let h = 0; h < HOURS_PER_YEAR; h++) {
    const hourOfDay = h % 24;
    const dayOfYear = Math.floor(h / 24);
    const dayOfWeek = dayOfYear % 7; // 0 = lundi
    const v = shape.hourly[hourOfDay] * shape.weekly[dayOfWeek];
    raw[h] = v;
    sum += v;
  }

  // Mise à l'échelle : Σ profil (kWh) = consommation annuelle.
  // Chaque pas fait 1 h, donc kW == kWh sur le pas.
  const scale = sum > 0 ? annualConsumptionKwh / sum : 0;
  const profile = raw.map((v) => v * scale);

  // Plafonnement optionnel à la pointe déclarée.
  if (peakDemandKw && peakDemandKw > 0) {
    for (let h = 0; h < profile.length; h++) {
      if (profile[h] > peakDemandKw) profile[h] = peakDemandKw;
    }
  }

  return profile;
}
