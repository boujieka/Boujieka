import React from "react";
import { palette } from "../theme";

export type Role = "government" | "developer" | "utility" | "treasury" | "lender" | "partner";

const roleAccent: Record<Role, string> = {
  government: palette.signal,
  developer: "#B388FF",
  utility: palette.trap,
  treasury: palette.liability,
  lender: palette.pass,
  partner: palette.cite,
};

/** A small badge that tells you which institution you are looking at. */
const Badge: React.FC<{ role: Role; color: string }> = ({ role, color }) => {
  switch (role) {
    case "utility":
      // Transmission pylon.
      return (
        <g stroke={color} strokeWidth={2.4} fill="none" strokeLinecap="round">
          <path d="M12 26 L18 6 L24 26" />
          <path d="M13.6 20 L22.4 20" />
          <path d="M15 13.5 L21 13.5" />
          <path d="M9 11 L27 11" />
        </g>
      );
    case "treasury":
      // Public purse / treasury seal.
      return (
        <g stroke={color} strokeWidth={2.4} fill="none" strokeLinecap="round">
          <circle cx={18} cy={17} r={8.5} />
          <path d="M18 11.5 L18 22.5" />
          <path d="M21 14 Q15 12.4 15 16 Q15 19 21 19.4" />
        </g>
      );
    case "lender":
      // Bank colonnade.
      return (
        <g stroke={color} strokeWidth={2.4} fill="none" strokeLinecap="round">
          <path d="M8 12 L18 6 L28 12" />
          <path d="M11 13 L11 23 M18 13 L18 23 M25 13 L25 23" />
          <path d="M8 25.5 L28 25.5" />
        </g>
      );
    case "developer":
      // Project case.
      return (
        <g stroke={color} strokeWidth={2.4} fill="none" strokeLinecap="round">
          <rect x={8} y={12} width={20} height={14} rx={2.5} />
          <path d="M14 12 L14 9 Q14 7.5 15.5 7.5 L20.5 7.5 Q22 7.5 22 9 L22 12" />
          <path d="M8 18.5 L28 18.5" />
        </g>
      );
    case "partner":
      // Meridian / partner institution.
      return (
        <g stroke={color} strokeWidth={2.4} fill="none" strokeLinecap="round">
          <circle cx={18} cy={17} r={9} />
          <path d="M9 17 L27 17" />
          <path d="M18 8 Q23 17 18 26 Q13 17 18 8" />
        </g>
      );
    case "government":
    default:
      // Seat of government.
      return (
        <g stroke={color} strokeWidth={2.4} fill="none" strokeLinecap="round">
          <path d="M18 6 L18 10" />
          <path d="M10 12 L26 12" />
          <path d="M12 12 L12 24 M18 12 L18 24 M24 12 L24 24" />
          <path d="M8 26 L28 26" />
        </g>
      );
  }
};

/**
 * Light character: a figure only where the story needs an actor, never as
 * decoration. Dimmed when the actor is present but passive, which is the whole
 * point of the signing-table scene.
 */
export const Figure: React.FC<{
  role: Role;
  size?: number;
  dim?: boolean;
  /** Draws the "carries the risk" ring. */
  bearsRisk?: boolean;
}> = ({ role, size = 120, dim = false, bearsRisk = false }) => {
  const accent = roleAccent[role];
  const bodyFill = dim ? palette.panelHi : palette.panel;
  const stroke = dim ? palette.inkFaint : accent;
  const opacity = dim ? 0.55 : 1;

  return (
    <svg width={size} height={size} viewBox="0 0 120 120" style={{ opacity, display: "block" }}>
      {bearsRisk ? (
        <circle
          cx={60}
          cy={60}
          r={54}
          fill="none"
          stroke={palette.liability}
          strokeWidth={2.5}
          strokeDasharray="7 7"
          opacity={0.85}
        />
      ) : null}
      <circle cx={60} cy={60} r={46} fill={bodyFill} stroke={palette.rule} strokeWidth={1.5} />
      {/* Head */}
      <circle cx={60} cy={44} r={12} fill="none" stroke={stroke} strokeWidth={3} />
      {/* Shoulders */}
      <path
        d="M36 84 Q36 64 60 64 Q84 64 84 84"
        fill="none"
        stroke={stroke}
        strokeWidth={3}
        strokeLinecap="round"
      />
      {/* Institution badge, bottom-right */}
      <g transform="translate(74, 74) scale(1.05)">
        <circle cx={18} cy={17} r={17} fill={palette.bgDeep} stroke={palette.rule} strokeWidth={1.2} />
        <Badge role={role} color={stroke} />
      </g>
    </svg>
  );
};
