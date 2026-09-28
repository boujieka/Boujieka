import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { font, layout, palette, type } from "../theme";

/**
 * The persistent stage every scene sits on: background, a slow drifting grid
 * that keeps flat colour from looking dead, and the running chrome.
 */
export const Frame: React.FC<{
  children: React.ReactNode;
  chapter: string;
  series: string;
  /** Hide chrome on title and key-message cards. */
  bare?: boolean;
  accent?: string;
}> = ({ children, chapter, series, bare = false, accent = palette.signal }) => {
  const frame = useCurrentFrame();
  const drift = (frame * 0.12) % 80;

  return (
    <AbsoluteFill style={{ backgroundColor: palette.bg, fontFamily: font.sans, color: palette.ink }}>
      {/* Engineering grid — the sector's own visual language, kept very quiet. */}
      <AbsoluteFill
        style={{
          backgroundImage: `linear-gradient(${palette.rule}22 1px, transparent 1px), linear-gradient(90deg, ${palette.rule}22 1px, transparent 1px)`,
          backgroundSize: "80px 80px",
          backgroundPosition: `${drift}px ${drift}px`,
          opacity: 0.55,
        }}
      />
      {/* Vignette so the centre of frame always wins. */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse at 50% 42%, transparent 0%, ${palette.bgDeep}CC 78%)`,
        }}
      />

      {!bare ? (
        <>
          <div
            style={{
              position: "absolute",
              top: 58,
              left: layout.margin,
              display: "flex",
              alignItems: "center",
              gap: 18,
              fontSize: type.micro,
              letterSpacing: 2.4,
              textTransform: "uppercase",
              color: palette.inkFaint,
              fontWeight: 600,
            }}
          >
            <span style={{ width: 34, height: 3, backgroundColor: accent, borderRadius: 2 }} />
            {series}
          </div>
          <div
            style={{
              position: "absolute",
              top: 58,
              right: layout.margin,
              fontSize: type.micro,
              letterSpacing: 2.4,
              textTransform: "uppercase",
              color: palette.inkFaint,
              fontWeight: 600,
            }}
          >
            {chapter}
          </div>
        </>
      ) : null}

      <AbsoluteFill>{children}</AbsoluteFill>
    </AbsoluteFill>
  );
};

/** Standard content well: respects the safe gutter, vertically centred. */
export const Well: React.FC<{ children: React.ReactNode; top?: number }> = ({ children, top = 150 }) => (
  <AbsoluteFill
    style={{
      padding: `${top}px ${layout.margin}px 120px`,
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
    }}
  >
    {children}
  </AbsoluteFill>
);
