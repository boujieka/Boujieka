import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { z } from "zod";
import { colors, fonts, SERIES } from "../brand";
import { Backdrop } from "../components/Backdrop";

export const thumbnailSchema = z.object({
  series: z.enum(["delestage", "bankable", "lumiere", "jamais", "ppa", "facture", "cinqMinutes"]),
  headline: z.string(),
  accent: z.string(),
  image: z.string().optional(),
});

// Miniature YouTube 1280x720 : 3-5 mots max, un mot en accent.
export const Thumbnail: React.FC<z.infer<typeof thumbnailSchema>> = ({ series, headline, accent, image }) => (
  <AbsoluteFill>
    <Backdrop />
    {image && (
      <Img
        src={staticFile(image)}
        style={{ position: "absolute", right: 0, width: "55%", height: "100%", objectFit: "cover", opacity: 0.8 }}
      />
    )}
    <AbsoluteFill
      style={{
        background: `linear-gradient(90deg, ${colors.navyDeep} 45%, transparent 85%)`,
        padding: 60,
        justifyContent: "center",
        gap: 20,
      }}
    >
      <div style={{ fontFamily: fonts.title, fontWeight: 800, fontSize: 30, color: SERIES[series].color, letterSpacing: 3 }}>
        {SERIES[series].label.toUpperCase()}
      </div>
      <div style={{ fontFamily: fonts.title, fontWeight: 900, fontSize: 96, lineHeight: 1, color: colors.white, maxWidth: 760 }}>
        {headline} <span style={{ color: colors.gold }}>{accent}</span>
      </div>
    </AbsoluteFill>
    <Img src={staticFile("logo.png")} style={{ position: "absolute", right: 30, bottom: 30, width: 150, borderRadius: 14 }} />
  </AbsoluteFill>
);
