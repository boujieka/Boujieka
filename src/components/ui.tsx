import React from "react";
import { Img, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { colors, fonts, SERIES, SeriesKey } from "../brand";
import { fadeIn, lerp, rise } from "../anim";

export const Watermark: React.FC = () => (
  <Img
    src={staticFile("logo.png")}
    style={{
      position: "absolute",
      right: 40,
      bottom: 30,
      width: 110,
      borderRadius: 12,
      opacity: 0.85,
    }}
  />
);

export const SeriesBadge: React.FC<{ series: SeriesKey; delay?: number }> = ({ series, delay = 0 }) => {
  const frame = useCurrentFrame();
  const s = SERIES[series];
  return (
    <div
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 14,
        padding: "10px 22px",
        border: `2px solid ${s.color}`,
        borderRadius: 999,
        color: s.color,
        fontFamily: fonts.title,
        fontWeight: 800,
        fontSize: 26,
        letterSpacing: 2,
        textTransform: "uppercase",
        opacity: fadeIn(frame, delay, 12),
      }}
    >
      <span style={{ width: 12, height: 12, borderRadius: 6, background: s.color }} />
      {s.label}
    </div>
  );
};

export const SectionHeader: React.FC<{ index: number; title: string; scale?: number }> = ({
  index,
  title,
  scale = 1,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const bar = lerp(frame, [0, 20], [0, 1]);
  return (
    <div style={{ ...rise(frame, fps, 0, 30) }}>
      <div
        style={{
          fontFamily: fonts.title,
          fontWeight: 800,
          fontSize: 28 * scale,
          color: colors.gold,
          letterSpacing: 6,
        }}
      >
        {String(index).padStart(2, "0")} — {title.toUpperCase()}
      </div>
      <div
        style={{
          marginTop: 14,
          height: 4,
          width: 220 * scale * bar,
          background: `linear-gradient(90deg, ${colors.gold}, ${colors.green})`,
          borderRadius: 2,
        }}
      />
    </div>
  );
};

export const Bullets: React.FC<{ items: string[]; stagger: number; fontSize?: number }> = ({
  items,
  stagger,
  fontSize = 46,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: fontSize * 0.7 }}>
      {items.map((t, i) => (
        <div
          key={i}
          style={{
            display: "flex",
            gap: 24,
            alignItems: "flex-start",
            fontFamily: fonts.body,
            fontWeight: 500,
            fontSize,
            lineHeight: 1.25,
            color: colors.offWhite,
            ...rise(frame, fps, 10 + i * stagger),
          }}
        >
          <span style={{ color: colors.gold, fontFamily: fonts.title, fontWeight: 900 }}>▸</span>
          <span>{t}</span>
        </div>
      ))}
    </div>
  );
};

export const SourceNote: React.FC<{ text?: string; fontSize?: number }> = ({ text, fontSize = 20 }) => {
  const frame = useCurrentFrame();
  if (!text) return null;
  const unverified = text.includes("À VÉRIFIER");
  return (
    <div
      style={{
        fontFamily: fonts.body,
        fontSize,
        color: unverified ? colors.alert : colors.muted,
        opacity: fadeIn(frame, 20, 15),
      }}
    >
      Source : {text}
    </div>
  );
};

export const Highlight: React.FC<{ children: React.ReactNode; color?: string }> = ({
  children,
  color = colors.gold,
}) => <span style={{ color }}>{children}</span>;
