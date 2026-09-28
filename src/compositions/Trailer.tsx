import React from "react";
import { AbsoluteFill, Series, useCurrentFrame, useVideoConfig } from "remotion";
import { colors, fonts, MANIFESTO, SERIES } from "../brand";
import { fadeIn, fadeOut, rise } from "../anim";
import { Backdrop } from "../components/Backdrop";
import { Signature } from "../components/Signature";
import { useLayout } from "../components/layout";

const Line: React.FC<{ text: string; accent?: boolean }> = ({ text, accent }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const { s } = useLayout();
  return (
    <AbsoluteFill>
      <Backdrop intensity={0.5} />
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", padding: "0 8%" }}>
        <div
          style={{
            fontFamily: fonts.title,
            fontWeight: accent ? 900 : 700,
            fontSize: (accent ? 88 : 72) * s,
            textAlign: "center",
            lineHeight: 1.2,
            color: accent ? colors.gold : colors.white,
            ...rise(frame, fps, 5),
            opacity: Math.min(rise(frame, fps, 5).opacity, fadeOut(frame, durationInFrames, 12)),
          }}
        >
          {text}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const Questions: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { s } = useLayout();
  const qs = [
    "Pourquoi un barrage reste sur le papier ?",
    "Pourquoi un PPA échoue ?",
    "Où passe l’argent ?",
    "Qui paie quand le montage ne fonctionne pas ?",
  ];
  return (
    <AbsoluteFill>
      <Backdrop />
      <AbsoluteFill style={{ justifyContent: "center", padding: "0 10%", gap: 36 * s }}>
        {qs.map((q, i) => (
          <div
            key={i}
            style={{
              fontFamily: fonts.title,
              fontWeight: 800,
              fontSize: 60 * s,
              color: i === qs.length - 1 ? colors.gold : colors.white,
              ...rise(frame, fps, i * 40),
            }}
          >
            {q}
          </div>
        ))}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const SeriesList: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { s } = useLayout();
  const keys = ["delestage", "bankable", "lumiere"] as const;
  return (
    <AbsoluteFill>
      <Backdrop />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 40 * s }}>
        <div style={{ fontFamily: fonts.body, fontSize: 36 * s, color: colors.muted, opacity: fadeIn(frame, 0) }}>
          Trois séries pour commencer
        </div>
        {keys.map((k, i) => (
          <div
            key={k}
            style={{
              fontFamily: fonts.title,
              fontWeight: 900,
              fontSize: 72 * s,
              color: SERIES[k].color,
              textAlign: "center",
              ...rise(frame, fps, 15 + i * 25),
            }}
          >
            {SERIES[k].label}
          </div>
        ))}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// Bande-annonce de la chaîne (~40 s). Aucune donnée factuelle : uniquement le manifeste.
export const Trailer: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ background: colors.navyDeep }}>
      <Series>
        <Series.Sequence durationInFrames={4 * fps}>
          <Line text={MANIFESTO[0]} />
        </Series.Sequence>
        <Series.Sequence durationInFrames={3.5 * fps}>
          <Line text={MANIFESTO[1]} />
        </Series.Sequence>
        <Series.Sequence durationInFrames={4.5 * fps}>
          <Line text={MANIFESTO[2]} accent />
        </Series.Sequence>
        <Series.Sequence durationInFrames={9 * fps}>
          <Questions />
        </Series.Sequence>
        <Series.Sequence durationInFrames={4 * fps}>
          <Line text="On ne vous dit pas ce qu’il faut penser. On vous montre ce qui s’est passé." />
        </Series.Sequence>
        <Series.Sequence durationInFrames={6 * fps}>
          <SeriesList />
        </Series.Sequence>
        <Series.Sequence durationInFrames={6 * fps}>
          <Signature />
        </Series.Sequence>
      </Series>
    </AbsoluteFill>
  );
};
export const TRAILER_SECONDS = 4 + 3.5 + 4.5 + 9 + 4 + 6 + 6;
