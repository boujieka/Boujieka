import React from "react";
import { font, layout, palette, type } from "../theme";

export const Kicker: React.FC<{ children: React.ReactNode; color?: string; style?: React.CSSProperties }> = ({
  children,
  color = palette.trap,
  style,
}) => (
  <div
    style={{
      fontSize: type.small,
      letterSpacing: 3.2,
      textTransform: "uppercase",
      fontWeight: 700,
      color,
      ...style,
    }}
  >
    {children}
  </div>
);

export const Headline: React.FC<{
  children: React.ReactNode;
  size?: number;
  style?: React.CSSProperties;
}> = ({ children, size = type.h1, style }) => (
  <div
    style={{
      fontSize: size,
      lineHeight: 1.1,
      fontWeight: 800,
      letterSpacing: -1.6,
      color: palette.ink,
      ...style,
    }}
  >
    {children}
  </div>
);

export const Body: React.FC<{
  children: React.ReactNode;
  size?: number;
  color?: string;
  style?: React.CSSProperties;
}> = ({ children, size = type.body, color = palette.inkMuted, style }) => (
  <div style={{ fontSize: size, lineHeight: 1.45, fontWeight: 400, color, ...style }}>{children}</div>
);

export const Numeral: React.FC<{
  children: React.ReactNode;
  size?: number;
  color?: string;
  style?: React.CSSProperties;
  /** Mono suits bare counts; currency strings like "US$8.7bn" read better in sans. */
  mono?: boolean;
}> = ({ children, size = type.display, color = palette.ink, style, mono = true }) => (
  <div
    style={{
      fontFamily: mono ? font.mono : font.sans,
      fontSize: size,
      fontWeight: 700,
      letterSpacing: -2,
      lineHeight: 1,
      color,
      fontVariantNumeric: "tabular-nums",
      ...style,
    }}
  >
    {children}
  </div>
);

/**
 * Source line. Every screen carrying a figure carries one of these — including
 * the chapter's own caveats where a number is press-sourced or unverified.
 */
export const Cite: React.FC<{ children: React.ReactNode; label: string; style?: React.CSSProperties }> = ({
  children,
  label,
  style,
}) => (
  <div
    style={{
      display: "flex",
      gap: 12,
      alignItems: "baseline",
      fontSize: type.micro,
      lineHeight: 1.4,
      color: palette.inkFaint,
      maxWidth: 1500,
      ...style,
    }}
  >
    <span style={{ fontWeight: 700, letterSpacing: 1.6, textTransform: "uppercase", flexShrink: 0 }}>
      {label}
    </span>
    <span style={{ fontWeight: 400 }}>{children}</span>
  </div>
);

export const Panel: React.FC<{
  children: React.ReactNode;
  accent?: string;
  style?: React.CSSProperties;
}> = ({ children, accent, style }) => (
  <div
    style={{
      backgroundColor: palette.panel,
      border: `1px solid ${palette.rule}`,
      borderLeft: accent ? `5px solid ${accent}` : `1px solid ${palette.rule}`,
      borderRadius: layout.radius,
      padding: 34,
      ...style,
    }}
  >
    {children}
  </div>
);
