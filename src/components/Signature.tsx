import React from "react";
import { AbsoluteFill, Img, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { colors, fonts, TAGLINE } from "../brand";
import { fadeIn } from "../anim";
import { Backdrop } from "./Backdrop";
import { useLayout } from "./layout";

export const Signature: React.FC<{ cta?: string }> = ({ cta = "Abonnez-vous pour la prochaine histoire" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { vertical } = useLayout();
  const pop = spring({ frame, fps, config: { damping: 14 } });
  return (
    <AbsoluteFill>
      <Backdrop />
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", flexDirection: "column", gap: 30 }}>
        <Img
          src={staticFile("logo.png")}
          style={{
            width: vertical ? 700 : 520,
            borderRadius: 32,
            transform: `scale(${0.8 + pop * 0.2})`,
            opacity: pop,
            boxShadow: `0 0 80px ${colors.gold}55`,
          }}
        />
        <div
          style={{
            fontFamily: fonts.body,
            fontSize: vertical ? 40 : 34,
            color: colors.offWhite,
            textAlign: "center",
            maxWidth: vertical ? 900 : 1300,
            opacity: fadeIn(frame, 15, 15),
          }}
        >
          {TAGLINE}
        </div>
        <div
          style={{
            fontFamily: fonts.title,
            fontWeight: 800,
            fontSize: vertical ? 34 : 28,
            color: colors.navyDeep,
            background: colors.gold,
            padding: "14px 34px",
            borderRadius: 999,
            opacity: fadeIn(frame, 30, 15),
          }}
        >
          {cta}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
