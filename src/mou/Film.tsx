import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { sceneOpacity } from "./anim";
import { fullTrackFor, sceneClipFor } from "./audio";
import { Frame } from "./components/Frame";
import { ChromeProvider } from "./components/LocaleContext";
import { getBundle } from "./content";
import { SceneRenderer } from "./SceneRenderer";
import { blueprints, buildFilm, sceneOffsets } from "./structure";
import { palette } from "./theme";
import type { Locale } from "./types";

export type FilmProps = {
  filmId: string;
  locale: Locale;
};

/** Thin progress rule along the bottom — orientation without a visible timer. */
const Progress: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const pct = Math.min(1, frame / Math.max(1, durationInFrames - 1));
  return (
    <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 4, backgroundColor: palette.rule }}>
      <div style={{ width: `${pct * 100}%`, height: "100%", backgroundColor: palette.trap }} />
    </div>
  );
};

/** One scene, faded in and out so cuts never hard-splice. */
const SceneShell: React.FC<{ duration: number; children: React.ReactNode }> = ({ duration, children }) => {
  const frame = useCurrentFrame();
  return <AbsoluteFill style={{ opacity: sceneOpacity(frame, duration) }}>{children}</AbsoluteFill>;
};

export const Film: React.FC<FilmProps> = ({ filmId, locale }) => {
  const bundle = getBundle(locale);
  const blueprint = blueprints.find((b) => b.id === filmId);

  if (!blueprint) {
    throw new Error(`Unknown film id "${filmId}". Known: ${blueprints.map((b) => b.id).join(", ")}`);
  }
  const spec = buildFilm(blueprint, locale);
  const film = bundle.films[filmId];
  if (!film) {
    throw new Error(`No ${locale} copy for film "${filmId}".`);
  }

  const fullTrack = fullTrackFor(filmId, locale);

  return (
    <ChromeProvider chrome={bundle.chrome}>
      {fullTrack ? <Audio src={staticFile(fullTrack)} /> : null}
      {sceneOffsets(spec).map(({ spec: scene, from }) => {
        const copy = film.copy[scene.id];
        if (!copy) {
          throw new Error(`Missing ${locale} copy for scene "${scene.id}" in film "${filmId}".`);
        }
        if (copy.kind !== scene.kind) {
          throw new Error(
            `Scene "${scene.id}" is declared as "${scene.kind}" but its ${locale} copy is "${copy.kind}".`,
          );
        }
        const clip = sceneClipFor(filmId, locale, scene.id);
        const bare = copy.kind === "title-card" || copy.kind === "key-message";

        return (
          <Sequence key={scene.id} from={from} durationInFrames={scene.durationInFrames} name={scene.id}>
            <SceneShell duration={scene.durationInFrames}>
              <Frame series={bundle.chrome.series} chapter={bundle.chrome.chapter} bare={bare}>
                <SceneRenderer copy={copy} />
              </Frame>
            </SceneShell>
            {clip ? <Audio src={staticFile(clip)} /> : null}
          </Sequence>
        );
      })}
      <Progress />
    </ChromeProvider>
  );
};
