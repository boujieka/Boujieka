import { interpolate, spring } from "remotion";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

export const fadeIn = (frame: number, start = 0, len = 15) =>
  interpolate(frame, [start, start + len], [0, 1], clamp);

export const fadeOut = (frame: number, end: number, len = 15) =>
  interpolate(frame, [end - len, end], [1, 0], clamp);

export const rise = (frame: number, fps: number, delay = 0, distance = 40) => {
  const s = spring({ frame: frame - delay, fps, config: { damping: 200 } });
  return { opacity: s, transform: `translateY(${(1 - s) * distance}px)` };
};

export const lerp = (frame: number, input: number[], output: number[]) =>
  interpolate(frame, input, output, clamp);
