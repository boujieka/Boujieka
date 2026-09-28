import { interpolate, spring } from "remotion";
import { enterSpring, popSpring } from "./theme";

/** 0 → 1 entrance progress for an element that appears `delay` frames into a scene. */
export const enter = (frame: number, fps: number, delay = 0): number =>
  spring({ frame: frame - delay, fps, config: enterSpring, durationInFrames: 26 });

/** Livelier version for numbers and emphasis beats. */
export const pop = (frame: number, fps: number, delay = 0): number =>
  spring({ frame: frame - delay, fps, config: popSpring, durationInFrames: 30 });

/** Fade + rise, the default entrance for text blocks. */
export const fadeUp = (progress: number, distance = 28) => ({
  opacity: progress,
  transform: `translateY(${(1 - progress) * distance}px)`,
});

/**
 * Holds a scene's content on screen and eases it out just before the cut, so
 * scene changes never feel like a hard splice.
 */
export const sceneOpacity = (frame: number, duration: number, fadeFrames = 12): number =>
  interpolate(
    frame,
    [0, fadeFrames, duration - fadeFrames, duration],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

/** Even stagger across n items over `span` frames. */
export const stagger = (index: number, step = 7): number => index * step;

/** Counts a number up, formatted with the caller's own separator rules. */
export const countUp = (progress: number, target: number): number => Math.round(progress * target);
