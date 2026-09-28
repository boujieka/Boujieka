import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { enter, fadeUp } from "../anim";
import { Body, Headline, Numeral } from "../components/Type";
import { Well } from "../components/Frame";
import { font, layout, palette, type } from "../theme";
import type { SceneCopy } from "../types";

/** The five costs, only the first of which usually gets counted. */
export const CostList: React.FC<{ copy: Extract<SceneCopy, { kind: "cost-list" }> }> = ({ copy }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const titleIn = enter(frame, fps, 0);
  const noteIn = enter(frame, fps, 16 + copy.items.length * 10 + 16);

  return (
    <Well top={162}>
      <div style={{ ...fadeUp(titleIn), marginBottom: 36 }}>
        <Headline size={type.h2}>{copy.title}</Headline>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
        {copy.items.map((item, i) => {
          const p = enter(frame, fps, 16 + i * 10);
          // The first cost is the one everyone counts — mark it differently.
          const counted = i === 0;
          const accent = counted ? palette.inkFaint : palette.liability;
          return (
            <div
              key={item.name}
              style={{
                ...fadeUp(p, 22),
                display: "flex",
                alignItems: "center",
                gap: 28,
                backgroundColor: palette.panel,
                border: `1px solid ${palette.rule}`,
                borderLeft: `5px solid ${accent}`,
                borderRadius: 14,
                padding: "20px 28px",
              }}
            >
              <Numeral size={38} color={accent} style={{ flex: "0 0 62px" }}>
                {String(i + 1).padStart(2, "0")}
              </Numeral>
              <div style={{ flex: "0 0 460px", fontSize: 30, fontWeight: 800, color: palette.ink, letterSpacing: -0.4 }}>
                {item.name}
              </div>
              <div style={{ flex: 1, borderLeft: `1px solid ${palette.rule}`, paddingLeft: 26 }}>
                <Body size={23} style={{ lineHeight: 1.32 }}>
                  {item.detail}
                </Body>
              </div>
            </div>
          );
        })}
      </div>

      <div
        style={{
          ...fadeUp(noteIn, 18),
          marginTop: 32,
          borderLeft: `5px solid ${palette.trap}`,
          paddingLeft: 28,
        }}
      >
        <Body size={type.small} color={palette.ink} style={{ lineHeight: 1.4 }}>
          {copy.note}
        </Body>
      </div>
    </Well>
  );
};

/** The four remedies, each tied to the chapter that develops it. */
export const RemedyList: React.FC<{ copy: Extract<SceneCopy, { kind: "remedy-list" }> }> = ({ copy }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const titleIn = enter(frame, fps, 0);
  const closeIn = enter(frame, fps, 16 + copy.items.length * 12 + 18);

  return (
    <Well top={158}>
      <div style={{ ...fadeUp(titleIn), marginBottom: 34 }}>
        <Headline size={type.h2} style={{ maxWidth: 1560 }}>
          {copy.title}
        </Headline>
      </div>

      <div style={{ display: "flex", gap: 18 }}>
        {copy.items.map((item, i) => {
          const p = enter(frame, fps, 16 + i * 12);
          return (
            <div
              key={item.n}
              style={{
                ...fadeUp(p, 28),
                flex: 1,
                minWidth: 0,
                backgroundColor: palette.panel,
                border: `1px solid ${palette.rule}`,
                borderTop: `4px solid ${palette.pass}`,
                borderRadius: layout.radius,
                padding: "28px 26px 24px",
                display: "flex",
                flexDirection: "column",
                gap: 16,
              }}
            >
              <Numeral size={52} color={palette.pass}>
                {item.n}
              </Numeral>
              <div style={{ fontSize: 30, fontWeight: 800, color: palette.ink, letterSpacing: -0.4, lineHeight: 1.15, minHeight: 72 }}>
                {item.name}
              </div>
              <Body size={21} style={{ lineHeight: 1.36, flex: 1 }}>
                {item.detail}
              </Body>
              <div
                style={{
                  borderTop: `1px solid ${palette.rule}`,
                  paddingTop: 14,
                  fontFamily: font.mono,
                  fontSize: 18,
                  color: palette.inkFaint,
                  fontWeight: 500,
                }}
              >
                {item.chapter}
              </div>
            </div>
          );
        })}
      </div>

      <div
        style={{
          ...fadeUp(closeIn, 18),
          marginTop: 32,
          borderLeft: `5px solid ${palette.pass}`,
          paddingLeft: 28,
          maxWidth: 1620,
        }}
      >
        <Body size={25} color={palette.ink} style={{ lineHeight: 1.4 }}>
          {copy.closing}
        </Body>
      </div>
    </Well>
  );
};

/** The audience-specific ask. This is the only scene that tells people what to do. */
export const AskCard: React.FC<{ copy: Extract<SceneCopy, { kind: "ask-card" }> }> = ({ copy }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const badgeIn = enter(frame, fps, 0);
  const titleIn = enter(frame, fps, 8);
  const becauseIn = enter(frame, fps, 22 + copy.asks.length * 11 + 14);

  return (
    <Well top={150}>
      <div style={{ ...fadeUp(badgeIn), marginBottom: 18 }}>
        <span
          style={{
            border: `1px solid ${palette.pass}66`,
            backgroundColor: `${palette.pass}14`,
            color: palette.pass,
            borderRadius: 999,
            padding: "10px 24px",
            fontSize: type.micro,
            fontWeight: 800,
            letterSpacing: 2,
            textTransform: "uppercase",
          }}
        >
          {copy.audience}
        </span>
      </div>

      <div style={{ ...fadeUp(titleIn, 24), marginBottom: 34 }}>
        <Headline size={type.h2} style={{ maxWidth: 1520 }}>
          {copy.title}
        </Headline>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
        {copy.asks.map((ask, i) => {
          const p = enter(frame, fps, 22 + i * 11);
          return (
            <div key={ask} style={{ ...fadeUp(p, 22), display: "flex", gap: 24, alignItems: "flex-start" }}>
              <div
                style={{
                  flex: "0 0 46px",
                  height: 46,
                  borderRadius: 23,
                  border: `2.5px solid ${palette.pass}`,
                  color: palette.pass,
                  fontFamily: font.mono,
                  fontSize: 22,
                  fontWeight: 700,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                {i + 1}
              </div>
              <Body size={27} color={palette.ink} style={{ lineHeight: 1.38, maxWidth: 1480, paddingTop: 6 }}>
                {ask}
              </Body>
            </div>
          );
        })}
      </div>

      <div
        style={{
          ...fadeUp(becauseIn, 18),
          marginTop: 34,
          borderLeft: `5px solid ${palette.trap}`,
          paddingLeft: 28,
          maxWidth: 1600,
        }}
      >
        <Body size={25} color={palette.inkMuted} style={{ lineHeight: 1.4, fontStyle: "italic" }}>
          {copy.because}
        </Body>
      </div>
    </Well>
  );
};

/** The closing card. Held long enough to be photographed off a screen. */
export const KeyMessage: React.FC<{ copy: Extract<SceneCopy, { kind: "key-message" }> }> = ({ copy }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const labelIn = enter(frame, fps, 0);
  const textIn = enter(frame, fps, 10);
  const srcIn = enter(frame, fps, 40);

  return (
    // Balanced vertically: this card gets photographed off screens in the room.
    <Well top={120}>
      <div style={{ ...fadeUp(labelIn), display: "flex", alignItems: "center", gap: 20, marginBottom: 34 }}>
        <span style={{ width: 54, height: 4, backgroundColor: palette.trap, borderRadius: 2 }} />
        <span
          style={{
            fontSize: type.small,
            letterSpacing: 3.4,
            textTransform: "uppercase",
            fontWeight: 800,
            color: palette.trap,
          }}
        >
          {copy.label}
        </span>
      </div>

      <div style={{ ...fadeUp(textIn, 30), maxWidth: 1600 }}>
        <div style={{ fontSize: 50, lineHeight: 1.36, fontWeight: 600, color: palette.ink, letterSpacing: -0.8 }}>
          {copy.text}
        </div>
      </div>

      <div style={{ ...fadeUp(srcIn, 16), marginTop: 46 }}>
        <Body size={type.caption} color={palette.inkFaint}>
          {copy.source}
        </Body>
      </div>
    </Well>
  );
};
