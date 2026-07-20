import { z } from "zod";

/** Schémas de validation partagés (formulaires & routes API). */

export const roleEnum = z.enum(["offtaker", "developer", "admin"]);

export const registerSchema = z.object({
  organizationName: z.string().min(2, "Raison sociale requise"),
  organizationType: z.enum(["offtaker", "developer"]),
  country: z.string().min(2, "Pays requis (code ISO, ex. CM)").max(3),
  sector: z.string().optional(),
  fullName: z.string().min(2, "Nom complet requis"),
  email: z.string().email("Email invalide"),
  password: z.string().min(8, "Mot de passe : 8 caractères minimum"),
});

export const loginSchema = z.object({
  email: z.string().email("Email invalide"),
  password: z.string().min(1, "Mot de passe requis"),
});

export const siteSchema = z.object({
  name: z.string().min(2),
  latitude: z.coerce.number().min(-90).max(90),
  longitude: z.coerce.number().min(-180).max(180),
  country: z.string().min(2).max(3),
  availableAreaM2: z.coerce.number().min(0).optional(),
  currentGridTariff: z.coerce.number().min(0).optional(),
  annualConsumptionKwh: z.coerce.number().min(0).optional(),
  peakDemandKw: z.coerce.number().min(0).optional(),
  loadCriticality: z.enum(["faible", "moyenne", "elevee", "critique"]),
  outageCostPerHour: z.coerce.number().min(0).optional(),
  gridOutageHoursYear: z.coerce.number().min(0).max(8760).optional(),
  sectorTemplate: z
    .enum([
      "industrie_continue",
      "industrie_2x8",
      "tertiaire_bureaux",
      "commerce",
      "data_center",
      "hopital",
      "telecom",
      "residentiel",
    ])
    .optional(),
});

export const developerProfileSchema = z.object({
  minProjectSizeKw: z.coerce.number().min(0),
  maxProjectSizeKw: z.coerce.number().min(0),
  financingCapacity: z.enum(["equity", "dette", "mixte", "aucune"]),
  trackRecordMw: z.coerce.number().min(0).default(0),
  projectsCompleted: z.coerce.number().int().min(0).default(0),
  countries: z.array(z.string().min(2).max(3)).min(1, "Au moins un pays couvert"),
  technologies: z
    .array(z.enum(["solaire", "stockage", "hybride", "groupe_backup"]))
    .min(1, "Au moins une technologie"),
});

export const opportunitySchema = z.object({
  siteId: z.string().uuid(),
  title: z.string().min(3),
  targetReliabilityRate: z.coerce.number().min(0.1).max(1),
});

export const prefeasibilitySchema = z.object({
  opportunityId: z.string().uuid(),
  performanceRatio: z.coerce.number().min(0.5).max(0.95).optional(),
  batteryRoundTrip: z.coerce.number().min(0.5).max(1).optional(),
  batteryDod: z.coerce.number().min(0.5).max(1).optional(),
  batteryCRate: z.coerce.number().min(0.1).max(2).optional(),
  weatherYear: z.coerce.number().int().min(2000).max(2025).optional(),
});

export const eoiSchema = z.object({
  opportunityId: z.string().uuid(),
  message: z.string().max(2000).optional(),
});

export const messageSchema = z.object({
  opportunityId: z.string().uuid(),
  recipientUserId: z.string().uuid(),
  body: z.string().min(1).max(4000),
});

export type RegisterInput = z.infer<typeof registerSchema>;
export type LoginInput = z.infer<typeof loginSchema>;
