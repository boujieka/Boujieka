import { bundles } from "./content";
import { FPS } from "./theme";
import type { FilmSpec, Locale, SceneKind, SceneSpec } from "./types";

/**
 * Scene durations are derived from the narration, not guessed.
 *
 * Each scene carries a visual minimum — how long its animation needs to land
 * even with nothing said over it — and the timing engine takes whichever is
 * longer: that minimum, or the time the script needs. Timing is computed PER
 * LOCALE, because French runs roughly a fifth longer than English and forcing
 * both cuts onto one timeline would leave the English one padded with dead air.
 *
 * `npm run cues` prints the resulting in-points per locale and flags any scene
 * where the script would still overrun.
 *
 * To shorten every film without touching the copy, lower PACING and PAD_SEC.
 */

/** Measured pace for deliberate, institutional narration: ~150 words/minute. */
const NARRATION_WPS = 2.5;
/** Room for breaths, emphasis and a slower reader than the estimate assumes. */
const PACING = 1.14;
/** Silent head and tail either side of the line, so scenes never feel clipped. */
const PAD_SEC = 1.8;

type SceneBlueprint = {
  id: string;
  kind: SceneKind;
  /** Seconds the animation needs on its own, with no narration. */
  minSeconds: number;
};

export type FilmBlueprint = {
  id: string;
  slug: string;
  scenes: SceneBlueprint[];
};

/** CORE FILM — tracks the chapter's own seven sections. */
export const coreBlueprint: FilmBlueprint = {
  id: "MoUTrap-Core",
  slug: "core",
  scenes: [
    { id: "core.title", kind: "title-card", minSeconds: 9 },
    { id: "core.nigeria", kind: "cold-open", minSeconds: 16 },
    { id: "core.flip", kind: "stat-flip", minSeconds: 14 },
    { id: "core.tests", kind: "two-tests", minSeconds: 15 },
    { id: "core.stages", kind: "stage-ladder", minSeconds: 17 },
    { id: "core.denominator", kind: "funnel", minSeconds: 18 },
    { id: "core.layers", kind: "layers", minSeconds: 18 },
    { id: "core.quaiboe", kind: "case-card", minSeconds: 15 },
    { id: "core.actors", kind: "actor-table", minSeconds: 20 },
    { id: "core.exits", kind: "two-exits", minSeconds: 15 },
    { id: "core.ghana", kind: "case-card", minSeconds: 16 },
    { id: "core.nachtigal", kind: "case-card", minSeconds: 16 },
    { id: "core.costs", kind: "cost-list", minSeconds: 17 },
    { id: "core.remedies", kind: "remedy-list", minSeconds: 17 },
    { id: "core.key", kind: "key-message", minSeconds: 14 },
  ],
};

/** MODULE A — Ministers and Cabinet. The signature moment. */
export const ministersBlueprint: FilmBlueprint = {
  id: "MoUTrap-Ministers",
  slug: "ministers",
  scenes: [
    { id: "min.title", kind: "title-card", minSeconds: 8 },
    { id: "min.flip", kind: "stat-flip", minSeconds: 13 },
    { id: "min.actors", kind: "actor-table", minSeconds: 20 },
    { id: "min.exits", kind: "two-exits", minSeconds: 15 },
    { id: "min.ask", kind: "ask-card", minSeconds: 17 },
    { id: "min.key", kind: "key-message", minSeconds: 12 },
  ],
};

/** MODULE B — Ministry of Finance. The state's test and the contingent liability. */
export const financeBlueprint: FilmBlueprint = {
  id: "MoUTrap-Finance",
  slug: "finance",
  scenes: [
    { id: "fin.title", kind: "title-card", minSeconds: 8 },
    { id: "fin.tests", kind: "two-tests", minSeconds: 15 },
    { id: "fin.ghana", kind: "case-card", minSeconds: 16 },
    { id: "fin.nachtigal", kind: "case-card", minSeconds: 15 },
    { id: "fin.ask", kind: "ask-card", minSeconds: 17 },
    { id: "fin.key", kind: "key-message", minSeconds: 12 },
  ],
};

/** MODULE C — Regulators. Price discovery and the tariff benchmark. */
export const regulatorsBlueprint: FilmBlueprint = {
  id: "MoUTrap-Regulators",
  slug: "regulators",
  scenes: [
    { id: "reg.title", kind: "title-card", minSeconds: 8 },
    { id: "reg.tariff", kind: "cold-open", minSeconds: 16 },
    { id: "reg.layers", kind: "layers", minSeconds: 18 },
    { id: "reg.quote", kind: "quote", minSeconds: 12 },
    { id: "reg.ask", kind: "ask-card", minSeconds: 17 },
    { id: "reg.key", kind: "key-message", minSeconds: 12 },
  ],
};

/** MODULE D — Developers and development partners. */
export const developersBlueprint: FilmBlueprint = {
  id: "MoUTrap-Developers",
  slug: "developers",
  scenes: [
    { id: "dev.title", kind: "title-card", minSeconds: 8 },
    { id: "dev.stages", kind: "stage-ladder", minSeconds: 17 },
    { id: "dev.denominator", kind: "funnel", minSeconds: 18 },
    { id: "dev.nachtigal", kind: "case-card", minSeconds: 15 },
    { id: "dev.ask", kind: "ask-card", minSeconds: 17 },
    { id: "dev.key", kind: "key-message", minSeconds: 12 },
  ],
};

export const blueprints: FilmBlueprint[] = [
  coreBlueprint,
  ministersBlueprint,
  financeBlueprint,
  regulatorsBlueprint,
  developersBlueprint,
];

export const locales: Locale[] = ["en", "fr"];

/** Seconds this locale's narration needs for one scene. Zero if the scene is silent. */
export const narrationSeconds = (filmId: string, sceneId: string, locale: Locale): number => {
  const line = bundles[locale].films[filmId]?.narration[sceneId];
  if (!line) {
    return 0;
  }
  return line.trim().split(/\s+/).filter(Boolean).length / NARRATION_WPS;
};

/** Resolves a blueprint into concrete frame counts for one locale. */
export const buildFilm = (blueprint: FilmBlueprint, locale: Locale): FilmSpec => ({
  id: blueprint.id,
  slug: blueprint.slug,
  scenes: blueprint.scenes.map((s): SceneSpec => {
    const spoken = narrationSeconds(blueprint.id, s.id, locale);
    const needed = spoken > 0 ? spoken * PACING + PAD_SEC : s.minSeconds;
    return {
      id: s.id,
      kind: s.kind,
      durationInFrames: Math.round(Math.max(s.minSeconds, needed) * FPS),
    };
  }),
});

export const filmDuration = (film: FilmSpec): number =>
  film.scenes.reduce((total, s) => total + s.durationInFrames, 0);

/** Absolute start frame of each scene, in order. */
export const sceneOffsets = (film: FilmSpec): { spec: SceneSpec; from: number }[] => {
  let from = 0;
  return film.scenes.map((spec) => {
    const entry = { spec, from };
    from += spec.durationInFrames;
    return entry;
  });
};
