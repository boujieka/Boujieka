import "./index.css";
import React from "react";
import { Composition } from "remotion";
import { Film } from "./mou/Film";
import { ensureFonts } from "./mou/fonts";
import { blueprints, buildFilm, filmDuration, locales } from "./mou/structure";
import { FPS, HEIGHT, WIDTH } from "./mou/theme";
ensureFonts();

/**
 * Ten compositions: one core film plus four audience modules, each in English
 * and French. Both locales share one timing structure, so a voiceover recorded
 * against the cue sheet fits either cut.
 *
 *   npx remotion render MoUTrap-Core-EN out/core.en.mp4
 */
export const RemotionRoot: React.FC = () => (
  <>
    {blueprints.flatMap((blueprint) =>
      locales.map((locale) => (
        <Composition
          key={`${blueprint.id}-${locale}`}
          id={`${blueprint.id}-${locale.toUpperCase()}`}
          component={Film}
          durationInFrames={filmDuration(buildFilm(blueprint, locale))}
          fps={FPS}
          width={WIDTH}
          height={HEIGHT}
          defaultProps={{ filmId: blueprint.id, locale }}
        />
      )),
    )}
  </>
);
