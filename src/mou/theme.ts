/**
 * Visual system for the "Bankable Is Not Enough" training films.
 *
 * The look is infographic-led: evidence carries the screen, figures appear only
 * where the story needs an actor. Colour is used semantically, not decoratively —
 * each hue means one thing across all ten compositions.
 */

export const FPS = 30;
export const WIDTH = 1920;
export const HEIGHT = 1080;

export const palette = {
  bg: "#0A1120",
  bgDeep: "#060C17",
  panel: "#111D30",
  panelHi: "#18273E",
  rule: "#243652",

  ink: "#F4F8FD",
  inkMuted: "#93A7C4",
  inkFaint: "#5B7093",

  /** The commitment / the signature — what feels like progress. */
  signal: "#4DA3FF",
  /** The trap itself — cost deferred, risk unpriced. */
  trap: "#F0A93B",
  /** Liability, arrears, the expensive exit. */
  liability: "#E4572E",
  /** A test passed, a remedy, power actually delivered. */
  pass: "#37C08A",
  /** Neutral evidence accent for citations and sources. */
  cite: "#7C8FB0",
} as const;

export type PaletteKey = keyof typeof palette;

/** Semantic colour for each of the four explanations in Table 1.2. */
export const layerColor = {
  sponsor: "#B388FF",
  process: palette.signal,
  system: palette.trap,
  fiscal: palette.liability,
} as const;

export const font = {
  sans: "'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif",
  mono: "'IBM Plex Mono', ui-monospace, 'SFMono-Regular', monospace",
  serif: "'Source Serif 4', Georgia, serif",
} as const;

/** 1920x1080 type scale. Values are px. */
export const type = {
  hero: 148,
  display: 104,
  h1: 76,
  h2: 56,
  h3: 42,
  body: 34,
  small: 28,
  caption: 24,
  micro: 20,
} as const;

export const layout = {
  /** Broadcast-safe gutter. Nothing load-bearing outside this. */
  margin: 132,
  gap: 40,
  radius: 22,
} as const;

/** Standard spring for entrances — settled, no overshoot wobble. */
export const enterSpring = {
  damping: 200,
  mass: 0.7,
  stiffness: 110,
} as const;

/** Slightly livelier spring for numbers and emphasis beats. */
export const popSpring = {
  damping: 18,
  mass: 0.6,
  stiffness: 160,
} as const;
