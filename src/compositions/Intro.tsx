import React from "react";
import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { colors, fonts, TAGLINE } from "../brand";
import { fadeIn, fadeOut } from "../anim";
import { Backdrop } from "../components/Backdrop";

// Générique d'ouverture (~6 s) : un « courant » traverse l'écran puis allume le logo.
export const Intro: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height, durationInFrames } = useVideoConfig();
  const sweep = interpolate(frame, [0, 30], [-0.2, 1.2], { extrapolateRight: "clamp" });
  const logo = spring({ frame: frame - 25, fps, config: { damping: 12 } });
  const flash = interpolate(frame, [24, 28, 40], [0, 0.8, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ opacity: fadeOut(frame, durationInFrames, 12) }}>
      <Backdrop intensity={fadeIn(frame, 20, 20)} />
      <div
        style={{
          position: "absolute",
          top: height / 2 - 3,
          left: 0,
          width: width * sweep,
          height: 6,
          background: `linear-gradient(90deg, transparent, ${colors.green}, ${colors.gold}, ${colors.goldLight})`,
          boxShadow: `0 0 30px ${colors.gold}`,
          opacity: fadeOut(frame, 36, 10),
        }}
      />
      <AbsoluteFill style={{ background: colors.goldLight, opacity: flash }} />
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", flexDirection: "column", gap: 30 }}>
        <Img
          src={staticFile("logo.png")}
          style={{
            width: Math.min(width, height) * 0.62,
            borderRadius: 28,
            opacity: logo,
            transform: `scale(${0.85 + logo * 0.15})`,
          }}
        />
        <div
          style={{
            fontFamily: fonts.body,
            fontSize: 34,
            color: colors.offWhite,
            opacity: fadeIn(frame, 60, 20),
            textAlign: "center",
            padding: "0 60px",
          }}
        >
          {TAGLINE}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
