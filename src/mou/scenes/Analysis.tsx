import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { enter, fadeUp } from "../anim";
import { Body, Headline } from "../components/Type";
import { Well } from "../components/Frame";
import { useChrome } from "../components/LocaleContext";
import { Figure, type Role } from "../components/Figure";
import { font, layerColor, layout, palette, type } from "../theme";
import type { SceneCopy } from "../types";

/**
 * Table 1.2 — the four explanations, drawn as literal stacked layers so the
 * chapter's "layers, not rivals" argument is carried by the picture.
 */
export const Layers: React.FC<{ copy: Extract<SceneCopy, { kind: "layers" }> }> = ({ copy }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const titleIn = enter(frame, fps, 0);
  const closeIn = enter(frame, fps, 84);

  return (
    <Well top={164}>
      <div style={{ ...fadeUp(titleIn), marginBottom: 34 }}>
        <Headline size={type.h2}>{copy.title}</Headline>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        {copy.layers.map((layer, i) => {
          const p = enter(frame, fps, 14 + i * 14);
          const accent = layerColor[layer.id];
          // Each layer sits slightly inset from the one above it.
          const inset = i * 26;
          return (
            <div
              key={layer.id}
              style={{
                ...fadeUp(p, 26),
                marginLeft: inset,
                marginRight: inset,
                backgroundColor: palette.panel,
                border: `1px solid ${palette.rule}`,
                borderLeft: `6px solid ${accent}`,
                borderRadius: 14,
                padding: "22px 30px",
                display: "flex",
                alignItems: "center",
                gap: 30,
              }}
            >
              <div
                style={{
                  flex: "0 0 240px",
                  display: "flex",
                  alignItems: "center",
                  gap: 16,
                }}
              >
                <span
                  style={{
                    fontFamily: font.mono,
                    fontSize: 20,
                    color: accent,
                    fontWeight: 700,
                  }}
                >
                  {String(i + 1).padStart(2, "0")}
                </span>
                <span style={{ fontSize: 34, fontWeight: 800, color: palette.ink, letterSpacing: -0.5 }}>
                  {layer.name}
                </span>
              </div>
              <div style={{ flex: "0 0 420px" }}>
                <Body size={22} color={palette.inkMuted} style={{ lineHeight: 1.3 }}>
                  {layer.where}
                </Body>
              </div>
              <div style={{ flex: 1, borderLeft: `1px solid ${palette.rule}`, paddingLeft: 26 }}>
                <Body size={22} color={palette.ink} style={{ lineHeight: 1.3 }}>
                  {layer.policy}
                </Body>
              </div>
            </div>
          );
        })}
      </div>

      <div
        style={{
          ...fadeUp(closeIn, 18),
          marginTop: 34,
          borderLeft: `5px solid ${palette.signal}`,
          paddingLeft: 28,
          maxWidth: 1600,
        }}
      >
        <Body size={type.small} color={palette.ink} style={{ lineHeight: 1.4 }}>
          {copy.closing}
        </Body>
      </div>
    </Well>
  );
};

const roleFor = (actor: string, index: number): Role => {
  const key = actor.toLowerCase();
  if (key.includes("develop") && !key.includes("partner")) return "developer";
  if (key.includes("util") || key.includes("compagnie") || key.includes("national")) return "utility";
  if (key.includes("treasur") || key.includes("trésor") || key.includes("finance")) return "treasury";
  if (key.includes("lender") || key.includes("prêteur") || key.includes("preteur")) return "lender";
  if (key.includes("partner") || key.includes("partenaire")) return "partner";
  if (key.includes("govern") || key.includes("gouvern") || key.includes("you") || key.includes("vous"))
    return "government";
  const fallback: Role[] = ["government", "developer", "utility", "lender", "partner"];
  return fallback[index % fallback.length] ?? "government";
};

/**
 * Table 1.3 — who gains at signature and who pays later. The two parties that
 * carry the risk are ringed; everyone else is drawn at full strength, which is
 * exactly the asymmetry the chapter is pointing at.
 */
export const ActorTable: React.FC<{ copy: Extract<SceneCopy, { kind: "actor-table" }> }> = ({ copy }) => {
  const chrome = useChrome();
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const titleIn = enter(frame, fps, 0);
  const closeIn = enter(frame, fps, 14 + copy.rows.length * 11 + 22);

  return (
    <Well top={150}>
      <div style={{ ...fadeUp(titleIn), marginBottom: 30 }}>
        <Headline size={type.h2}>{copy.title}</Headline>
      </div>

      <div style={{ display: "flex", gap: 16 }}>
        {copy.rows.map((row, i) => {
          const p = enter(frame, fps, 14 + i * 11);
          const accent = row.bearsRisk ? palette.liability : palette.rule;
          return (
            <div
              key={row.actor}
              style={{
                ...fadeUp(p, 28),
                flex: 1,
                minWidth: 0,
                backgroundColor: row.absent
                  ? "transparent"
                  : row.bearsRisk
                    ? `${palette.liability}12`
                    : palette.panel,
                border: row.absent ? `2px dashed ${palette.liability}88` : `1px solid ${accent}`,
                borderRadius: layout.radius,
                padding: "22px 20px 20px",
                display: "flex",
                flexDirection: "column",
                gap: 14,
              }}
            >
              <div style={{ display: "flex", justifyContent: "center", opacity: row.absent ? 0.42 : 1 }}>
                <Figure
                  role={roleFor(row.actor, i)}
                  size={92}
                  dim={row.absent || !row.bearsRisk}
                  bearsRisk={row.bearsRisk && !row.absent}
                />
              </div>
              <div
                style={{
                  textAlign: "center",
                  fontSize: 25,
                  fontWeight: 800,
                  color: palette.ink,
                  letterSpacing: -0.3,
                  minHeight: 62,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  lineHeight: 1.15,
                }}
              >
                {row.actor}
              </div>
              <div style={{ borderTop: `1px solid ${palette.rule}`, paddingTop: 14 }}>
                <Body size={18} style={{ lineHeight: 1.32, minHeight: 96 }}>
                  {row.offers}
                </Body>
              </div>
              <div
                style={{
                  fontSize: 19,
                  fontWeight: 700,
                  color: row.bearsRisk ? palette.liability : palette.trap,
                  lineHeight: 1.25,
                  minHeight: 48,
                }}
              >
                {row.incentive}
              </div>
              {row.bearsRisk ? (
                <div
                  style={{
                    fontSize: 15,
                    letterSpacing: 1.4,
                    textTransform: "uppercase",
                    fontWeight: 800,
                    color: palette.liability,
                    borderTop: `1px dashed ${palette.liability}66`,
                    paddingTop: 10,
                    textAlign: "center",
                  }}
                >
                  {row.absent ? `${chrome.absentLabel} · ${chrome.bearsRiskLabel}` : chrome.bearsRiskLabel}
                </div>
              ) : null}
            </div>
          );
        })}
      </div>

      <div
        style={{
          ...fadeUp(closeIn, 18),
          marginTop: 32,
          borderLeft: `5px solid ${palette.liability}`,
          paddingLeft: 28,
          maxWidth: 1620,
        }}
      >
        <Body size={26} color={palette.ink} style={{ lineHeight: 1.4 }}>
          {copy.closing}
        </Body>
      </div>
    </Well>
  );
};

/** The branching diagram: stall, or close badly. Both roads priced. */
export const TwoExits: React.FC<{ copy: Extract<SceneCopy, { kind: "two-exits" }> }> = ({ copy }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const titleIn = enter(frame, fps, 0);
  const splitIn = enter(frame, fps, 12);
  const sharedIn = enter(frame, fps, 70);

  const branch = (
    data: { name: string; detail: string; cost: string },
    accent: string,
    progress: number,
  ) => (
    <div
      style={{
        ...fadeUp(progress, 30),
        flex: 1,
        backgroundColor: palette.panel,
        border: `1px solid ${accent}55`,
        borderRadius: layout.radius,
        overflow: "hidden",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <div
        style={{
          backgroundColor: `${accent}1F`,
          borderBottom: `2px solid ${accent}`,
          padding: "20px 30px",
          fontSize: 36,
          fontWeight: 800,
          color: palette.ink,
          letterSpacing: -0.6,
        }}
      >
        {data.name}
      </div>
      <div style={{ padding: "26px 30px", flex: 1 }}>
        <Body size={25} style={{ lineHeight: 1.42 }}>
          {data.detail}
        </Body>
      </div>
      <div
        style={{
          borderTop: `1px solid ${palette.rule}`,
          padding: "20px 30px",
          color: accent,
          fontSize: 27,
          fontWeight: 800,
          letterSpacing: -0.3,
        }}
      >
        {data.cost}
      </div>
    </div>
  );

  const splitWidth = interpolate(splitIn, [0, 1], [0, 1]);

  return (
    <Well top={168}>
      <div style={{ ...fadeUp(titleIn), marginBottom: 26 }}>
        <Headline size={type.h2}>{copy.title}</Headline>
      </div>

      {/* The fork */}
      <div style={{ height: 54, position: "relative", marginBottom: 6 }}>
        <div
          style={{
            position: "absolute",
            left: "50%",
            top: 0,
            width: 3,
            height: 22,
            backgroundColor: palette.rule,
            transform: "translateX(-50%)",
          }}
        />
        <div
          style={{
            position: "absolute",
            left: "50%",
            top: 22,
            height: 3,
            width: `${splitWidth * 50}%`,
            backgroundColor: palette.rule,
            transform: "translateX(-50%)",
          }}
        />
        <div
          style={{
            position: "absolute",
            left: `${50 - splitWidth * 25}%`,
            top: 22,
            width: 3,
            height: 32,
            backgroundColor: palette.trap,
            opacity: splitWidth,
          }}
        />
        <div
          style={{
            position: "absolute",
            left: `${50 + splitWidth * 25}%`,
            top: 22,
            width: 3,
            height: 32,
            backgroundColor: palette.liability,
            opacity: splitWidth,
          }}
        />
      </div>

      <div style={{ display: "flex", gap: 30, marginBottom: 36 }}>
        {branch(copy.stall, palette.trap, enter(frame, fps, 22))}
        {branch(copy.close, palette.liability, enter(frame, fps, 40))}
      </div>

      {/* This is the scene's conclusion, not a footnote — give it the weight. */}
      <div
        style={{
          ...fadeUp(sharedIn, 18),
          borderLeft: `5px solid ${palette.signal}`,
          paddingLeft: 28,
          maxWidth: 1620,
        }}
      >
        <Body size={27} color={palette.ink} style={{ lineHeight: 1.4 }}>
          {copy.shared}
        </Body>
      </div>
    </Well>
  );
};
