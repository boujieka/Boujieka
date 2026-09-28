import React from "react";
import { Composition, Still } from "remotion";
import { Intro } from "./compositions/Intro";
import { Trailer, TRAILER_SECONDS } from "./compositions/Trailer";
import { Episode, episodeDuration } from "./compositions/Episode";
import { Thumbnail, thumbnailSchema } from "./compositions/Thumbnail";
import { Episode as EpisodeData, episodeSchema } from "./episodes/schema";
import { episodeModele } from "./episodes/modele";
import { ep01Nigeria } from "./episodes/ep01-nigeria";

const FPS = 30;

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="Intro" component={Intro} durationInFrames={6 * FPS} fps={FPS} width={1920} height={1080} />
    <Composition
      id="Trailer"
      component={Trailer}
      durationInFrames={TRAILER_SECONDS * FPS}
      fps={FPS}
      width={1920}
      height={1080}
    />
    <Composition
      id="TrailerVertical"
      component={Trailer}
      durationInFrames={TRAILER_SECONDS * FPS}
      fps={FPS}
      width={1080}
      height={1920}
    />
    <Composition
      id="Episode"
      component={Episode}
      schema={episodeSchema}
      defaultProps={episodeModele}
      calculateMetadata={({ props }: { props: EpisodeData }) => ({ durationInFrames: episodeDuration(props, FPS) })}
      durationInFrames={FPS}
      fps={FPS}
      width={1920}
      height={1080}
    />
    <Composition
      id="Short"
      component={Episode}
      schema={episodeSchema}
      defaultProps={{
        ...episodeModele,
        durations: { hook: 6, projet: 8, promesse: 8, realite: 12, rupture: 8, pourquoi: 10, lecon: 6, signature: 4 },
      }}
      calculateMetadata={({ props }: { props: EpisodeData }) => ({ durationInFrames: episodeDuration(props, FPS) })}
      durationInFrames={FPS}
      fps={FPS}
      width={1080}
      height={1920}
    />
    <Composition
      id="Ep01Nigeria"
      component={Episode}
      schema={episodeSchema}
      defaultProps={ep01Nigeria}
      calculateMetadata={({ props }: { props: EpisodeData }) => ({ durationInFrames: episodeDuration(props, FPS) })}
      durationInFrames={FPS}
      fps={FPS}
      width={1920}
      height={1080}
    />
    <Composition
      id="Ep01NigeriaShort"
      component={Episode}
      schema={episodeSchema}
      defaultProps={{
        ...ep01Nigeria,
        durations: { hook: 8, projet: 8, promesse: 8, realite: 14, rupture: 9, pourquoi: 10, lecon: 9, signature: 4 },
      }}
      calculateMetadata={({ props }: { props: EpisodeData }) => ({ durationInFrames: episodeDuration(props, FPS) })}
      durationInFrames={FPS}
      fps={FPS}
      width={1080}
      height={1920}
    />
    <Still
      id="Ep01Thumbnail"
      component={Thumbnail}
      schema={thumbnailSchema}
      defaultProps={{ series: "bankable" as const, headline: "14 contrats. Zéro", accent: "électron." }}
      width={1280}
      height={720}
    />
    <Still
      id="Thumbnail"
      component={Thumbnail}
      schema={thumbnailSchema}
      defaultProps={{ series: "delestage" as const, headline: "Le barrage qui n’a jamais", accent: "tourné" }}
      width={1280}
      height={720}
    />
  </>
);
