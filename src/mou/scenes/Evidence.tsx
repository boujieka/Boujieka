import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { enter, fadeUp } from "../anim";
import { Body, Cite, Headline } from "../components/Type";
import { Well } from "../components/Frame";
import { useChrome } from "../components/LocaleContext";
import { font, palette, type } from "../theme";
import type { SceneCopy } from "../types";

const caseAccent = (tone: "trap" | "liability" | "pass" | undefined): string => {
  switch (tone) {
    case "liability":
      return palette.liability;
    case "pass":
      return palette.pass;
    default:
      return palette.trap;
  }
};

/** A country case, told as a timeline of what is actually on the record. */
export const CaseCard: React.FC<{ copy: Extract<SceneCopy, { kind: "case-card" }> }> = ({ copy }) => {
  const chrome = useChrome();
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const accent = caseAccent(copy.tone);
  const headIn = enter(frame, fps, 0);
  const verdictIn = enter(frame, fps, 18 + copy.beats.length * 10);

  return (
    <Well top={158}>
      <div style={{ ...fadeUp(headIn), display: "flex", alignItems: "baseline", gap: 24, marginBottom: 12 }}>
        <span
          style={{
            fontSize: type.small,
            letterSpacing: 3.2,
            textTransform: "uppercase",
            fontWeight: 800,
            color: accent,
          }}
        >
          {copy.country}
        </span>
        <span style={{ width: 8, height: 8, borderRadius: 4, backgroundColor: palette.inkFaint }} />
        <span style={{ fontSize: type.small, color: palette.inkMuted, fontFamily: font.mono }}>
          {copy.project}
        </span>
      </div>

      <div style={{ ...fadeUp(headIn, 22), marginBottom: 40 }}>
        <Headline size={type.h2} style={{ maxWidth: 1500 }}>
          {copy.verdict}
        </Headline>
      </div>

      {/* Record of what happened, as a vertical spine. */}
      <div style={{ position: "relative", paddingLeft: 38 }}>
        <div
          style={{
            position: "absolute",
            left: 9,
            top: 10,
            bottom: 10,
            width: 2,
            backgroundColor: palette.rule,
          }}
        />
        {copy.beats.map((beat, i) => {
          const p = enter(frame, fps, 18 + i * 10);
          return (
            <div
              key={beat}
              style={{
                ...fadeUp(p, 18),
                position: "relative",
                paddingBottom: i === copy.beats.length - 1 ? 0 : 22,
              }}
            >
              <div
                style={{
                  position: "absolute",
                  left: -38 + 3,
                  top: 10,
                  width: 15,
                  height: 15,
                  borderRadius: 8,
                  backgroundColor: palette.bg,
                  border: `3px solid ${accent}`,
                }}
              />
              <Body size={27} color={palette.ink} style={{ lineHeight: 1.38, maxWidth: 1540 }}>
                {beat}
              </Body>
            </div>
          );
        })}
      </div>

      {copy.cite ? (
        <div style={{ opacity: verdictIn, marginTop: 36 }}>
          <Cite label={chrome.sourceLabel}>{copy.cite}</Cite>
        </div>
      ) : null}
    </Well>
  );
};

/** A pull quote from a primary source. Serif, because it is someone else's voice. */
export const Quote: React.FC<{ copy: Extract<SceneCopy, { kind: "quote" }> }> = ({ copy }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const markIn = enter(frame, fps, 0);
  const textIn = enter(frame, fps, 10);
  const attrIn = enter(frame, fps, 34);

  return (
    <Well top={180}>
      <div
        style={{
          opacity: markIn,
          fontFamily: font.serif,
          fontSize: 200,
          lineHeight: 0.6,
          color: `${palette.trap}55`,
          marginBottom: 24,
          height: 90,
        }}
      >
        &ldquo;
      </div>
      <div style={{ ...fadeUp(textIn, 26), maxWidth: 1560 }}>
        <div
          style={{
            fontFamily: font.serif,
            fontStyle: "italic",
            fontSize: 56,
            lineHeight: 1.36,
            color: palette.ink,
            fontWeight: 400,
          }}
        >
          {copy.text}
        </div>
      </div>
      <div style={{ ...fadeUp(attrIn, 18), marginTop: 44, display: "flex", alignItems: "center", gap: 20 }}>
        <span style={{ width: 54, height: 3, backgroundColor: palette.trap, borderRadius: 2 }} />
        <Body size={type.caption} color={palette.inkMuted} style={{ maxWidth: 1300, lineHeight: 1.36 }}>
          {copy.attribution}
        </Body>
      </div>
    </Well>
  );
};
