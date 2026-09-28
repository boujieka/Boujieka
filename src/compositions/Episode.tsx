import React from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  Series,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { colors, fonts } from "../brand";
import { fadeIn, fadeOut, lerp, rise } from "../anim";
import { Backdrop } from "../components/Backdrop";
import { Bullets, SectionHeader, SeriesBadge, SourceNote, Watermark } from "../components/ui";
import { Signature } from "../components/Signature";
import { useLayout } from "../components/layout";
import { Episode as EpisodeData, SECTION_ORDER } from "../episodes/schema";

const Frame: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const { padX, padY } = useLayout();
  return (
    <AbsoluteFill>
      <Backdrop intensity={0.6} />
      <AbsoluteFill
        style={{
          padding: `${padY}px ${padX}px`,
          display: "flex",
          flexDirection: "column",
          gap: 50,
          opacity: Math.min(fadeIn(frame, 0, 10), fadeOut(frame, durationInFrames, 10)),
        }}
      >
        {children}
      </AbsoluteFill>
      <Watermark />
    </AbsoluteFill>
  );
};

const Hook: React.FC<{ ep: EpisodeData }> = ({ ep }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const { s } = useLayout();
  const per = Math.floor((durationInFrames - 20) / ep.hook.length);
  return (
    <AbsoluteFill style={{ background: colors.navyDeep }}>
      <Backdrop intensity={0.4} />
      <AbsoluteFill style={{ justifyContent: "center", padding: "0 10%", gap: 40 * s }}>
        <SeriesBadge series={ep.series} />
        {ep.hook.map((line, i) => {
          const last = i === ep.hook.length - 1;
          return (
            <div
              key={i}
              style={{
                fontFamily: fonts.title,
                fontWeight: last ? 900 : 700,
                fontSize: (last ? 84 : 64) * s,
                lineHeight: 1.15,
                color: last ? colors.gold : colors.white,
                ...rise(frame, fps, 10 + i * per),
              }}
            >
              {line}
            </div>
          );
        })}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const Projet: React.FC<{ ep: EpisodeData }> = ({ ep }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const { s, vertical } = useLayout();
  const { projet } = ep;
  return (
    <AbsoluteFill>
      {projet.image && (
        <Img
          src={staticFile(projet.image)}
          style={{
            position: "absolute",
            width: "100%",
            height: "100%",
            objectFit: "cover",
            opacity: 0.25,
            transform: `scale(${lerp(frame, [0, durationInFrames], [1, 1.12])})`,
          }}
        />
      )}
      <Frame>
        <SectionHeader index={1} title="Le projet" scale={s} />
        <div style={rise(frame, fps, 8)}>
          <div style={{ fontFamily: fonts.title, fontWeight: 900, fontSize: 96 * s, color: colors.white }}>
            {projet.name}
          </div>
          <div style={{ fontFamily: fonts.body, fontSize: 40 * s, color: colors.muted, marginTop: 10 }}>
            {projet.location}
          </div>
        </div>
        <div style={{ display: "flex", flexDirection: vertical ? "column" : "row", gap: 30 }}>
          {projet.figures.map((f, i) => (
            <div
              key={i}
              style={{
                flex: 1,
                padding: 30 * s,
                borderRadius: 20,
                background: "rgba(255,255,255,0.05)",
                borderTop: `4px solid ${colors.gold}`,
                ...rise(frame, fps, 30 + i * 15),
              }}
            >
              <div style={{ fontFamily: fonts.title, fontWeight: 900, fontSize: 64 * s, color: colors.gold }}>
                {f.value}
              </div>
              <div style={{ fontFamily: fonts.body, fontSize: 30 * s, color: colors.offWhite, margin: "8px 0 14px" }}>
                {f.label}
              </div>
              <SourceNote text={f.source} fontSize={18 * s + 2} />
            </div>
          ))}
        </div>
      </Frame>
    </AbsoluteFill>
  );
};

const Promesse: React.FC<{ ep: EpisodeData }> = ({ ep }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const { s } = useLayout();
  const { points, quote } = ep.promesse;
  const quoteAt = Math.floor(durationInFrames * 0.5);
  return (
    <Frame>
      <SectionHeader index={2} title="La promesse" scale={s} />
      <Bullets items={points} stagger={Math.floor(quoteAt / Math.max(points.length, 1))} fontSize={46 * s} />
      {quote && (
        <div
          style={{
            marginTop: "auto",
            paddingLeft: 30,
            borderLeft: `6px solid ${colors.gold}`,
            ...rise(frame, fps, quoteAt),
          }}
        >
          <div style={{ fontFamily: fonts.title, fontStyle: "italic", fontWeight: 600, fontSize: 48 * s, color: colors.white }}>
            « {quote.text} »
          </div>
          <div style={{ fontFamily: fonts.body, fontSize: 28 * s, color: colors.muted, margin: "12px 0 6px" }}>
            — {quote.author}
          </div>
          <SourceNote text={quote.source} fontSize={20 * s} />
        </div>
      )}
    </Frame>
  );
};

const Realite: React.FC<{ ep: EpisodeData }> = ({ ep }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const { s } = useLayout();
  const events = ep.realite.events;
  const per = Math.floor((durationInFrames - 30) / Math.max(events.length, 1));
  const progress = lerp(frame, [10, durationInFrames - 20], [0, 1]);
  return (
    <Frame>
      <SectionHeader index={3} title="Ce qui s’est réellement passé" scale={s} />
      <div style={{ position: "relative", display: "flex", flexDirection: "column", gap: 40 * s, paddingLeft: 60 }}>
        <div style={{ position: "absolute", left: 18, top: 10, bottom: 10, width: 4, background: "rgba(255,255,255,0.12)" }} />
        <div
          style={{
            position: "absolute",
            left: 18,
            top: 10,
            width: 4,
            height: `${progress * 100}%`,
            background: `linear-gradient(${colors.gold}, ${colors.green})`,
          }}
        />
        {events.map((e, i) => (
          <div key={i} style={{ position: "relative", ...rise(frame, fps, 15 + i * per) }}>
            <div
              style={{
                position: "absolute",
                left: -53,
                top: 14,
                width: 18,
                height: 18,
                borderRadius: 9,
                background: colors.gold,
              }}
            />
            <div style={{ fontFamily: fonts.title, fontWeight: 800, fontSize: 34 * s, color: colors.gold }}>{e.date}</div>
            <div style={{ fontFamily: fonts.body, fontSize: 40 * s, color: colors.offWhite }}>{e.text}</div>
            <SourceNote text={e.source} fontSize={18 * s + 2} />
          </div>
        ))}
      </div>
    </Frame>
  );
};

const Rupture: React.FC<{ ep: EpisodeData }> = ({ ep }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { s } = useLayout();
  // Courte coupure « délestage » à l'entrée de la section.
  const blackout = frame > 8 && frame < 22 && frame % 4 < 2 ? 0.85 : 0;
  return (
    <AbsoluteFill>
      <Frame>
        <SectionHeader index={4} title="Le point de rupture" scale={s} />
        <div style={{ marginTop: "auto", marginBottom: "auto" }}>
          <div style={{ fontFamily: fonts.title, fontWeight: 900, fontSize: 120 * s, color: colors.alert, ...rise(frame, fps, 25) }}>
            {ep.rupture.date}
          </div>
          <div style={{ fontFamily: fonts.body, fontWeight: 500, fontSize: 52 * s, color: colors.white, lineHeight: 1.3, ...rise(frame, fps, 40) }}>
            {ep.rupture.text}
          </div>
          <div style={{ marginTop: 20 }}>
            <SourceNote text={ep.rupture.source} fontSize={22 * s} />
          </div>
        </div>
      </Frame>
      <AbsoluteFill style={{ background: "black", opacity: blackout }} />
    </AbsoluteFill>
  );
};

const Pourquoi: React.FC<{ ep: EpisodeData }> = ({ ep }) => {
  const { durationInFrames } = useVideoConfig();
  const { s } = useLayout();
  const pts = ep.pourquoi.points;
  return (
    <Frame>
      <SectionHeader index={5} title="Pourquoi ?" scale={s} />
      <Bullets items={pts} stagger={Math.floor((durationInFrames - 30) / Math.max(pts.length, 1))} fontSize={50 * s} />
    </Frame>
  );
};

const Lecon: React.FC<{ ep: EpisodeData }> = ({ ep }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { s } = useLayout();
  return (
    <Frame>
      <SectionHeader index={6} title="La leçon" scale={s} />
      <div
        style={{
          margin: "auto 0",
          fontFamily: fonts.title,
          fontWeight: 800,
          fontSize: 70 * s,
          lineHeight: 1.2,
          color: colors.white,
          ...rise(frame, fps, 15),
        }}
      >
        {ep.lecon}
      </div>
      <div style={{ fontFamily: fonts.body, fontSize: 22 * s, color: colors.muted, opacity: fadeIn(frame, 40) }}>
        Sources : {ep.sources.join(" · ")}
      </div>
    </Frame>
  );
};

const SECTIONS = {
  hook: Hook,
  projet: Projet,
  promesse: Promesse,
  realite: Realite,
  rupture: Rupture,
  pourquoi: Pourquoi,
  lecon: Lecon,
  signature: () => <Signature />,
} satisfies Record<string, React.FC<{ ep: EpisodeData }>>;

export const Episode: React.FC<EpisodeData> = (ep) => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ background: colors.navyDeep }}>
      <Series>
        {SECTION_ORDER.map((key) => {
          const C = SECTIONS[key];
          return (
            <Series.Sequence key={key} name={key} durationInFrames={Math.round(ep.durations[key] * fps)}>
              <C ep={ep} />
            </Series.Sequence>
          );
        })}
      </Series>
      {ep.voiceover && <Audio src={staticFile(ep.voiceover)} />}
      {ep.music && <Audio src={staticFile(ep.music)} volume={0.12} loop />}
    </AbsoluteFill>
  );
};

export const episodeDuration = (ep: EpisodeData, fps: number) =>
  SECTION_ORDER.reduce((acc, k) => acc + Math.round(ep.durations[k] * fps), 0);
