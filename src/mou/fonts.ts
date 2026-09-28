import { loadFont } from "@remotion/fonts";
import { continueRender, delayRender, staticFile } from "remotion";

/**
 * Fonts are vendored in public/fonts rather than fetched from Google at render
 * time, so a render is deterministic and works without outbound network access.
 */
const faces: { family: string; file: string; weight: string; style?: string }[] = [
  { family: "Inter", file: "inter-400.woff2", weight: "400" },
  { family: "Inter", file: "inter-600.woff2", weight: "600" },
  { family: "Inter", file: "inter-700.woff2", weight: "700" },
  { family: "Inter", file: "inter-800.woff2", weight: "800" },
  { family: "IBM Plex Mono", file: "plexmono-500.woff2", weight: "500" },
  { family: "IBM Plex Mono", file: "plexmono-700.woff2", weight: "700" },
  { family: "Source Serif 4", file: "sourceserif-400i.woff2", weight: "400", style: "italic" },
];

let started = false;

/** Call once at module scope of the root. Blocks the render until fonts are ready. */
export const ensureFonts = (): void => {
  if (started) {
    return;
  }
  started = true;
  const handle = delayRender("Loading MoU Trap fonts");
  Promise.all(
    faces.map((face) =>
      loadFont({
        family: face.family,
        url: staticFile(`fonts/${face.file}`),
        weight: face.weight,
        style: face.style ?? "normal",
        format: "woff2",
      }),
    ),
  )
    .then(() => continueRender(handle))
    .catch(() => {
      // A missing font should degrade to the system stack, never fail the render.
      continueRender(handle);
    });
};
