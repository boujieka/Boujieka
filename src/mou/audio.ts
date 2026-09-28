import type { Locale } from "./types";

/**
 * Narration slots.
 *
 * The films are built to play silent — they carry their argument on screen, which
 * is how most officials watch. When voiceover is recorded, drop the files into
 * `public/audio/` and register them here; nothing else needs to change.
 *
 * Two ways to supply it:
 *
 *   1. ONE TRACK PER FILM (simplest). Record against the cue sheet in
 *      `out/cues/`, which gives the exact start timecode and duration of every
 *      scene. Put the file at e.g. public/audio/core.en.mp3 and add:
 *          "MoUTrap-Core": { en: "audio/core.en.mp3" }
 *
 *   2. ONE CLIP PER SCENE. Register each scene id instead. Each clip starts at
 *      its scene's first frame, so scene timings can be adjusted independently.
 *          "MoUTrap-Core": { en: { "core.nigeria": "audio/core.en.nigeria.mp3" } }
 *
 * A registered file that does not exist will fail the render, so only add an
 * entry once the file is in public/audio/.
 */
export type FilmAudio = Partial<Record<Locale, string | Record<string, string>>>;

export const narrationAudio: Record<string, FilmAudio> = {
  "MoUTrap-Core": {},
  "MoUTrap-Ministers": {},
  "MoUTrap-Finance": {},
  "MoUTrap-Regulators": {},
  "MoUTrap-Developers": {},
};

/** Full-film track for this locale, if one is registered. */
export const fullTrackFor = (filmId: string, locale: Locale): string | null => {
  const entry = narrationAudio[filmId]?.[locale];
  return typeof entry === "string" ? entry : null;
};

/** Per-scene clip for this locale, if one is registered. */
export const sceneClipFor = (filmId: string, locale: Locale, sceneId: string): string | null => {
  const entry = narrationAudio[filmId]?.[locale];
  if (!entry || typeof entry === "string") {
    return null;
  }
  return entry[sceneId] ?? null;
};
