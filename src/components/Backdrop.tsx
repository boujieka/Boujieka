import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { colors } from "../brand";

// Fond de marque : dégradé nuit + « courants » animés or/vert.
export const Backdrop: React.FC<{ intensity?: number }> = ({ intensity = 1 }) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  const wave = (offset: number, amp: number, yBase: number) => {
    const pts: string[] = [];
    for (let x = -50; x <= width + 50; x += 40) {
      const y =
        yBase +
        Math.sin(x / 260 + frame / 45 + offset) * amp +
        Math.sin(x / 90 + frame / 30 + offset * 2) * (amp / 6);
      pts.push(`${x},${y.toFixed(1)}`);
    }
    return `M${pts.join(" L")}`;
  };

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at 70% 20%, ${colors.navy} 0%, ${colors.navyDeep} 70%)`,
      }}
    >
      <svg width={width} height={height} style={{ position: "absolute", opacity: 0.07 * intensity }}>
        {Array.from({ length: Math.ceil(width / 80) }).map((_, i) => (
          <line key={`v${i}`} x1={i * 80} y1={0} x2={i * 80} y2={height} stroke={colors.white} />
        ))}
        {Array.from({ length: Math.ceil(height / 80) }).map((_, i) => (
          <line key={`h${i}`} x1={0} y1={i * 80} x2={width} y2={i * 80} stroke={colors.white} />
        ))}
      </svg>
      <svg width={width} height={height} style={{ position: "absolute", opacity: intensity }}>
        <path d={wave(0, 60, height * 0.78)} stroke={colors.gold} strokeWidth={3} fill="none" opacity={0.55} />
        <path d={wave(1.7, 80, height * 0.84)} stroke={colors.green} strokeWidth={5} fill="none" opacity={0.5} />
        <path d={wave(3.1, 40, height * 0.9)} stroke={colors.goldLight} strokeWidth={1.5} fill="none" opacity={0.35} />
      </svg>
    </AbsoluteFill>
  );
};
