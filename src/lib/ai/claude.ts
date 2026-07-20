/**
 * Client Claude — CÔTÉ SERVEUR UNIQUEMENT.
 *
 * La clé API est lue depuis `ANTHROPIC_API_KEY` et n'est jamais exposée au
 * client. Ce module ne doit être importé que par du code serveur (routes API,
 * server actions). Chaque appel est journalisé dans `ai_interactions`.
 *
 * En l'absence de clé, les fonctions renvoient un repli déterministe (calculé
 * à partir des chiffres déjà produits par les modules d'analyse), de sorte que
 * la plateforme reste fonctionnelle sans dépendance dure à l'API.
 */
import "server-only";
import { prisma } from "@/lib/db";
import { aiModels } from "@/lib/config";

const ANTHROPIC_URL = "https://api.anthropic.com/v1/messages";
const ANTHROPIC_VERSION = "2023-06-01";

export type AiTaskType =
  | "qualification"
  | "extraction_facture"
  | "note_concept"
  | "explication_matching";

interface CallOptions {
  model: string;
  system: string;
  prompt: string;
  maxTokens?: number;
  temperature?: number;
}

interface CallResult {
  text: string;
  tokensUsed: number;
  model: string;
  usedApi: boolean;
}

export function hasApiKey(): boolean {
  return Boolean(process.env.ANTHROPIC_API_KEY);
}

/** Appel bas niveau à l'API Messages de Claude. */
async function callClaude(opts: CallOptions): Promise<CallResult> {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    return { text: "", tokensUsed: 0, model: opts.model, usedApi: false };
  }

  const res = await fetch(ANTHROPIC_URL, {
    method: "POST",
    headers: {
      "x-api-key": apiKey,
      "anthropic-version": ANTHROPIC_VERSION,
      "content-type": "application/json",
    },
    body: JSON.stringify({
      model: opts.model,
      max_tokens: opts.maxTokens ?? 1024,
      temperature: opts.temperature ?? 0.3,
      system: opts.system,
      messages: [{ role: "user", content: opts.prompt }],
    }),
  });

  if (!res.ok) {
    const detail = await res.text().catch(() => "");
    throw new Error(`API Claude ${res.status} : ${detail.slice(0, 300)}`);
  }

  const data = (await res.json()) as {
    content: { type: string; text?: string }[];
    usage?: { input_tokens: number; output_tokens: number };
  };
  const text = data.content
    .filter((b) => b.type === "text")
    .map((b) => b.text ?? "")
    .join("\n")
    .trim();
  const tokensUsed =
    (data.usage?.input_tokens ?? 0) + (data.usage?.output_tokens ?? 0);
  return { text, tokensUsed, model: opts.model, usedApi: true };
}

/** Journalise l'appel dans ai_interactions (traçabilité et maîtrise des coûts). */
async function logInteraction(params: {
  userId?: string | null;
  opportunityId?: string | null;
  taskType: AiTaskType;
  model: string;
  tokensUsed: number;
}): Promise<void> {
  await prisma.aiInteraction.create({
    data: {
      userId: params.userId ?? null,
      opportunityId: params.opportunityId ?? null,
      taskType: params.taskType,
      model: params.model,
      tokensUsed: params.tokensUsed,
    },
  });
}

// ---------------------------------------------------------------------------
// Contextes typés fournis par les modules d'analyse
// ---------------------------------------------------------------------------

export interface QualificationContext {
  siteName: string;
  country: string;
  annualConsumptionKwh?: number | null;
  peakDemandKw?: number | null;
  loadCriticality: string;
  outageCostPerHour?: number | null;
  gridOutageHoursYear?: number | null;
  currentGridTariff?: number | null;
  targetReliabilityRate: number;
}

export interface ConceptNoteContext {
  title: string;
  siteName: string;
  country: string;
  pvSizeKwp: number;
  batterySizeKwh: number;
  backupSizeKw: number;
  coverageRate: number;
  residualDeficitKwh: number;
  annualCo2AvoidedTonnes: number;
  lifetimeCo2AvoidedTonnes: number;
  capex: number;
  ppaTariff: number;
  irr: number | null;
  paybackYears: number | null;
  annualSavings: number;
  currency: string;
  rating?: string | null;
}

export interface MatchExplanationContext {
  opportunityTitle: string;
  developerName: string;
  geographyScore: number;
  technologyScore: number;
  sizeScore: number;
  bankabilityAlignment: number;
  compatibilityScore: number;
  projectSizeKw: number;
  developerRange: { min: number; max: number };
}

// ---------------------------------------------------------------------------
// Fonctions métier
// ---------------------------------------------------------------------------

const pct = (x: number) => `${(x * 100).toFixed(1)} %`;
const fmt = (x: number) => Math.round(x).toLocaleString("fr-FR");

/**
 * Qualifie une opportunité : synthèse concise (forces, risques, adéquation aux
 * deux objectifs — décarbonisation et sécurité d'approvisionnement).
 */
export async function qualifyOpportunity(
  ctx: QualificationContext,
  meta: { userId?: string; opportunityId?: string },
): Promise<{ summary: string; usedApi: boolean }> {
  const system =
    "Tu es analyste d'origination pour ATEN, plateforme de projets solaire+stockage C&I " +
    "en Afrique centrale. Tu qualifies une opportunité en français, de façon concise, " +
    "vérifiable et chiffrée. Tu évalues les deux objectifs d'ATEN : décarbonisation et " +
    "sécurité d'approvisionnement. Ne fabrique aucun chiffre absent du contexte.";
  const prompt = `Qualifie cette opportunité en 4 à 6 phrases (forces, risques, pertinence) :
- Site : ${ctx.siteName} (${ctx.country})
- Consommation annuelle : ${ctx.annualConsumptionKwh ? fmt(ctx.annualConsumptionKwh) + " kWh" : "non renseignée"}
- Pointe : ${ctx.peakDemandKw ? fmt(ctx.peakDemandKw) + " kW" : "non renseignée"}
- Criticité de la charge : ${ctx.loadCriticality}
- Coût d'une heure de coupure : ${ctx.outageCostPerHour ?? "non renseigné"}
- Heures de coupure réseau/an : ${ctx.gridOutageHoursYear ?? "non renseignées"}
- Tarif réseau : ${ctx.currentGridTariff ?? "non renseigné"} /kWh
- Couverture cible imposée : ${pct(ctx.targetReliabilityRate)}`;

  try {
    const r = await callClaude({
      model: aiModels.qualification,
      system,
      prompt,
      maxTokens: 600,
    });
    await logInteraction({ ...meta, taskType: "qualification", model: r.model, tokensUsed: r.tokensUsed });
    if (r.usedApi) return { summary: r.text, usedApi: true };
  } catch (e) {
    console.error("qualifyOpportunity", e);
  }

  // Repli déterministe.
  const summary =
    `Site ${ctx.siteName} (${ctx.country}), charge ${ctx.loadCriticality}. ` +
    `Couverture cible imposée : ${pct(ctx.targetReliabilityRate)}. ` +
    (ctx.gridOutageHoursYear
      ? `Exposition réseau de ${fmt(ctx.gridOutageHoursYear)} h/an — enjeu de sécurité d'approvisionnement marqué. `
      : "") +
    (ctx.currentGridTariff
      ? `Tarif réseau de ${ctx.currentGridTariff}/kWh, propice à un PPA compétitif. `
      : "") +
    "Opportunité à instruire en pré-faisabilité pour chiffrer couverture, CO₂ évité et coût de la fiabilité.";
  return { summary, usedApi: false };
}

/**
 * Génère une note de concept chiffrée (économie + CO₂ évité + fiabilité).
 */
export async function generateConceptNote(
  ctx: ConceptNoteContext,
  meta: { userId?: string; opportunityId?: string },
): Promise<{ content: string; usedApi: boolean }> {
  const system =
    "Tu rédiges une note de concept d'investissement pour ATEN, en français, " +
    "structurée et chiffrée. Trois volets obligatoires : (1) économie, (2) CO₂ évité, " +
    "(3) fiabilité / sécurité d'approvisionnement. Utilise EXCLUSIVEMENT les chiffres fournis.";
  const prompt = `Rédige une note de concept pour « ${ctx.title} » (${ctx.siteName}, ${ctx.country}).
Dimensionnement : PV ${fmt(ctx.pvSizeKwp)} kWc, batterie ${fmt(ctx.batterySizeKwh)} kWh, appoint ${fmt(ctx.backupSizeKw)} kW.
Fiabilité : couverture ${pct(ctx.coverageRate)}, déficit résiduel ${fmt(ctx.residualDeficitKwh)} kWh/an.
Économie : CAPEX ${fmt(ctx.capex)} ${ctx.currency}, PPA ${ctx.ppaTariff.toFixed(3)} ${ctx.currency}/kWh, ` +
    `TRI ${ctx.irr !== null ? pct(ctx.irr) : "n/d"}, payback ${ctx.paybackYears !== null ? ctx.paybackYears.toFixed(1) + " ans" : "n/d"}, ` +
    `économie annuelle ${fmt(ctx.annualSavings)} ${ctx.currency}.
CO₂ évité : ${fmt(ctx.annualCo2AvoidedTonnes)} tCO₂/an (${fmt(ctx.lifetimeCo2AvoidedTonnes)} tCO₂ sur la durée de vie).
Bancabilité : ${ctx.rating ?? "n/d"}.`;

  try {
    const r = await callClaude({ model: aiModels.conceptNote, system, prompt, maxTokens: 1400 });
    await logInteraction({ ...meta, taskType: "note_concept", model: r.model, tokensUsed: r.tokensUsed });
    if (r.usedApi) return { content: r.text, usedApi: true };
  } catch (e) {
    console.error("generateConceptNote", e);
  }

  const content = `# Note de concept — ${ctx.title}

## Contexte
Site ${ctx.siteName} (${ctx.country}). Solution solaire + stockage + appoint à fiabilité cible.

## 1. Économie
- CAPEX : ${fmt(ctx.capex)} ${ctx.currency}
- Tarif PPA proposé : ${ctx.ppaTariff.toFixed(3)} ${ctx.currency}/kWh
- TRI : ${ctx.irr !== null ? pct(ctx.irr) : "n/d"} · Payback : ${ctx.paybackYears !== null ? ctx.paybackYears.toFixed(1) + " ans" : "n/d"}
- Économie annuelle contre réseau : ${fmt(ctx.annualSavings)} ${ctx.currency}

## 2. Décarbonisation
- ${fmt(ctx.annualCo2AvoidedTonnes)} tCO₂ évitées par an
- ${fmt(ctx.lifetimeCo2AvoidedTonnes)} tCO₂ sur la durée de vie

## 3. Fiabilité (sécurité d'approvisionnement)
- Dimensionnement : PV ${fmt(ctx.pvSizeKwp)} kWc · Batterie ${fmt(ctx.batterySizeKwh)} kWh · Appoint ${fmt(ctx.backupSizeKw)} kW
- Taux de couverture atteint : ${pct(ctx.coverageRate)}
- Déficit résiduel : ${fmt(ctx.residualDeficitKwh)} kWh/an

## Bancabilité
Notation : ${ctx.rating ?? "n/d"}.`;
  return { content, usedApi: false };
}

/**
 * Explique une recommandation de matching à partir des quatre sous-scores.
 * L'explication commente le score sans jamais l'altérer.
 */
export async function explainMatch(
  ctx: MatchExplanationContext,
  meta: { userId?: string; opportunityId?: string },
): Promise<{ explanation: string; usedApi: boolean }> {
  const system =
    "Tu expliques en français, en 2 à 3 phrases, une recommandation de mise en relation " +
    "entre une opportunité et un développeur, à partir de sous-scores fournis. Sois concret " +
    "et vérifiable. Tu commentes le score, tu ne le modifies pas.";
  const prompt = `Opportunité « ${ctx.opportunityTitle} » ↔ développeur « ${ctx.developerName} ».
Sous-scores : géographie ${ctx.geographyScore.toFixed(2)}, technologie ${ctx.technologyScore.toFixed(2)}, ` +
    `taille ${ctx.sizeScore.toFixed(2)}, bancabilité ${ctx.bankabilityAlignment.toFixed(2)}. ` +
    `Score global ${ctx.compatibilityScore.toFixed(2)}. ` +
    `Projet ${fmt(ctx.projectSizeKw)} kW ; fourchette développeur ${fmt(ctx.developerRange.min)}–${fmt(ctx.developerRange.max)} kW.`;

  try {
    const r = await callClaude({ model: aiModels.matching, system, prompt, maxTokens: 300 });
    await logInteraction({ ...meta, taskType: "explication_matching", model: r.model, tokensUsed: r.tokensUsed });
    if (r.usedApi) return { explanation: r.text, usedApi: true };
  } catch (e) {
    console.error("explainMatch", e);
  }

  const parts: string[] = [];
  if (ctx.geographyScore >= 1) parts.push("forte adéquation géographique");
  else if (ctx.geographyScore > 0) parts.push("couverture nationale (région à confirmer)");
  if (ctx.technologyScore >= 1) parts.push("technologies pleinement couvertes");
  else if (ctx.technologyScore > 0) parts.push("technologies partiellement couvertes");
  if (ctx.sizeScore >= 1) parts.push("taille dans la fourchette du développeur");
  else parts.push("taille de projet à la limite de la fourchette habituelle");
  const explanation =
    `Compatibilité ${ctx.compatibilityScore.toFixed(2)} : ${parts.join(", ")}. ` +
    `Alignement de bancabilité ${ctx.bankabilityAlignment.toFixed(2)}.`;
  return { explanation, usedApi: false };
}
