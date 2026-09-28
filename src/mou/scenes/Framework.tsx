import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { enter, fadeUp } from "../anim";
import { Body, Cite, Headline, Numeral } from "../components/Type";
import { Well } from "../components/Frame";
import { useChrome } from "../components/LocaleContext";
import { font, layout, palette, type } from "../theme";
import type { SceneCopy, Stat } from "../types";

const toneColor = (tone: Stat["tone"]): string => {
  switch (tone) {
    case "trap":
      return palette.trap;
    case "liability":
      return palette.liability;
    case "pass":
      return palette.pass;
    case "ink":
      return palette.ink;
    default:
      return palette.signal;
  }
};

/**
 * The spine of the whole book: two tests side by side, the state's one
 * deliberately drawn as the unanswered column.
 */
export const TwoTests: React.FC<{ copy: Extract<SceneCopy, { kind: "two-tests" }> }> = ({ copy }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const titleIn = enter(frame, fps, 0);
  const lenderIn = enter(frame, fps, 14);
  const stateIn = enter(frame, fps, 34);
  const footIn = enter(frame, fps, 62);

  const card = (
    which: "lender" | "state",
    data: { name: string; question: string; asker: string },
    progress: number,
  ) => {
    const isState = which === "state";
    const accent = isState ? palette.liability : palette.pass;
    return (
      <div
        style={{
          ...fadeUp(progress, 34),
          flex: 1,
          backgroundColor: palette.panel,
          border: `1px solid ${isState ? `${palette.liability}55` : palette.rule}`,
          borderRadius: layout.radius,
          padding: "38px 38px 34px",
          display: "flex",
          flexDirection: "column",
          gap: 22,
          position: "relative",
          overflow: "hidden",
        }}
      >
        <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: 4, backgroundColor: accent }} />
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <div
            style={{
              width: 44,
              height: 44,
              borderRadius: 22,
              border: `2.5px solid ${accent}`,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: accent,
              fontSize: 24,
              fontWeight: 800,
              fontFamily: font.mono,
            }}
          >
            {isState ? "?" : "✓"}
          </div>
          <Headline size={type.h3} style={{ letterSpacing: -0.6 }}>
            {data.name}
          </Headline>
        </div>
        <Body size={38} color={palette.ink} style={{ lineHeight: 1.3, fontWeight: 600, minHeight: 148 }}>
          {data.question}
        </Body>
        <div
          style={{
            borderTop: `1px solid ${palette.rule}`,
            paddingTop: 20,
            fontSize: type.caption,
            color: isState ? palette.liability : palette.inkMuted,
            fontWeight: isState ? 700 : 400,
            lineHeight: 1.4,
          }}
        >
          {data.asker}
        </div>
      </div>
    );
  };

  return (
    <Well top={176}>
      <div style={{ ...fadeUp(titleIn), marginBottom: 46 }}>
        <Headline size={type.h2} style={{ maxWidth: 1500 }}>
          {copy.title}
        </Headline>
      </div>
      <div style={{ display: "flex", gap: 30, marginBottom: 46 }}>
        {card("lender", copy.lender, lenderIn)}
        {card("state", copy.state, stateIn)}
      </div>
      <div
        style={{
          ...fadeUp(footIn, 20),
          borderLeft: `5px solid ${palette.trap}`,
          paddingLeft: 28,
          maxWidth: 1560,
        }}
      >
        <Body size={type.body} color={palette.ink} style={{ lineHeight: 1.4 }}>
          {copy.footnote}
        </Body>
      </div>
    </Well>
  );
};

/** Table 1.1 — the three stages, drawn as a ladder with the trap bracketed. */
export const StageLadder: React.FC<{ copy: Extract<SceneCopy, { kind: "stage-ladder" }> }> = ({ copy }) => {
  const chrome = useChrome();
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const titleIn = enter(frame, fps, 0);
  const bracketIn = enter(frame, fps, 74);
  const capIn = enter(frame, fps, 88);

  const stageAccent = [palette.trap, palette.signal, palette.liability];

  return (
    <Well top={168}>
      <div style={{ ...fadeUp(titleIn), marginBottom: 40 }}>
        <Headline size={type.h2}>{copy.title}</Headline>
      </div>

      <div style={{ display: "flex", gap: 20, position: "relative" }}>
        {/* Bracket spanning stage 1 to stage 3 — where the trap lives. */}
        <div
          style={{
            position: "absolute",
            left: -42,
            top: 0,
            bottom: 0,
            width: 20,
            opacity: bracketIn,
            borderLeft: `3px solid ${palette.trap}`,
            borderTop: `3px solid ${palette.trap}`,
            borderBottom: `3px solid ${palette.trap}`,
            borderRadius: "8px 0 0 8px",
          }}
        />
        {copy.rows.map((row, i) => {
          const p = enter(frame, fps, 16 + i * 16);
          const accent = stageAccent[i] ?? palette.signal;
          return (
            <div
              key={row.stage}
              style={{
                ...fadeUp(p, 30),
                flex: 1,
                display: "flex",
                flexDirection: "column",
                backgroundColor: palette.panel,
                border: `1px solid ${palette.rule}`,
                borderRadius: layout.radius,
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  backgroundColor: `${accent}1F`,
                  borderBottom: `2px solid ${accent}`,
                  padding: "22px 28px",
                  display: "flex",
                  alignItems: "center",
                  gap: 14,
                }}
              >
                <span
                  style={{
                    fontFamily: font.mono,
                    fontSize: type.micro,
                    color: accent,
                    fontWeight: 700,
                  }}
                >
                  {String(i + 1).padStart(2, "0")}
                </span>
                <span style={{ fontSize: type.h3, fontWeight: 800, color: palette.ink, letterSpacing: -0.6 }}>
                  {row.stage}
                </span>
              </div>
              <div style={{ padding: "26px 28px", display: "flex", flexDirection: "column", gap: 22, flex: 1 }}>
                {(
                  [
                    [chrome.colSigned, row.signed],
                    [chrome.colBinds, row.binds],
                    [chrome.colCommitted, row.committed],
                  ] as const
                ).map(([k, v]) => (
                  <div key={k}>
                    <div
                      style={{
                        fontSize: 17,
                        letterSpacing: 1.8,
                        textTransform: "uppercase",
                        color: palette.inkFaint,
                        fontWeight: 700,
                        marginBottom: 8,
                      }}
                    >
                      {k}
                    </div>
                    <Body size={type.caption} color={palette.ink} style={{ lineHeight: 1.36 }}>
                      {v}
                    </Body>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>

      <div style={{ ...fadeUp(capIn, 16), marginTop: 34 }}>
        <Cite label={chrome.tableLabel}>{copy.caption}</Cite>
      </div>
    </Well>
  );
};

/** The denominator problem, drawn as the funnel nobody can measure the top of. */
export const Funnel: React.FC<{ copy: Extract<SceneCopy, { kind: "funnel" }> }> = ({ copy }) => {
  const chrome = useChrome();
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const titleIn = enter(frame, fps, 0);
  const unknownIn = enter(frame, fps, 78);

  // Funnel bar widths: the first is dashed because the number is unknown.
  const widths = [100, 62, 28];

  return (
    <Well top={162}>
      <div style={{ ...fadeUp(titleIn), marginBottom: 34 }}>
        <Headline size={type.h2}>{copy.title}</Headline>
      </div>

      <div style={{ display: "flex", gap: 44, alignItems: "flex-start" }}>
        {/* Funnel */}
        <div style={{ flex: "0 0 720px", display: "flex", flexDirection: "column", gap: 24 }}>
          {copy.steps.map((step, i) => {
            const p = enter(frame, fps, 12 + i * 14);
            const w = interpolate(p, [0, 1], [0, widths[i] ?? 40]);
            const isUnknown = i === 0;
            return (
              <div key={step.label} style={{ opacity: p }}>
                {/* The bar is a pure graphic; the label sits beneath it so a narrow
                    bar never clips its own text. */}
                <div
                  style={{
                    height: 46,
                    width: `${w}%`,
                    backgroundColor: isUnknown ? "transparent" : `${palette.signal}26`,
                    border: isUnknown
                      ? `2.5px dashed ${palette.inkFaint}`
                      : `1.5px solid ${i === 2 ? palette.liability : palette.signal}`,
                    borderRadius: 8,
                  }}
                />
                <div
                  style={{
                    marginTop: 10,
                    fontSize: type.small,
                    fontWeight: 700,
                    color: palette.ink,
                  }}
                >
                  {step.label}
                </div>
                {step.note ? (
                  <div
                    style={{
                      marginTop: 4,
                      fontSize: type.micro,
                      color: isUnknown ? palette.trap : palette.inkMuted,
                      fontWeight: isUnknown ? 700 : 400,
                      maxWidth: 720,
                      lineHeight: 1.35,
                    }}
                  >
                    {step.note}
                  </div>
                ) : null}
              </div>
            );
          })}
        </div>

        {/* Supporting figures */}
        <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 18 }}>
          {copy.stats.map((stat, i) => {
            const p = enter(frame, fps, 34 + i * 10);
            const c = toneColor(stat.tone);
            return (
              <div
                key={stat.label}
                style={{
                  ...fadeUp(p, 20),
                  display: "flex",
                  gap: 20,
                  alignItems: "baseline",
                  borderBottom: `1px solid ${palette.rule}`,
                  paddingBottom: 14,
                }}
              >
                <Numeral size={42} color={c} mono={false} style={{ flex: "0 0 230px", letterSpacing: -0.8 }}>
                  {stat.value}
                </Numeral>
                <div style={{ flex: 1 }}>
                  <Body size={22} style={{ lineHeight: 1.32 }}>
                    {stat.label}
                  </Body>
                  {stat.unit ? (
                    <div style={{ fontSize: 18, color: palette.inkFaint, fontFamily: font.mono, marginTop: 4 }}>
                      {stat.unit}
                    </div>
                  ) : null}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div
        style={{
          ...fadeUp(unknownIn, 18),
          marginTop: 34,
          borderLeft: `5px solid ${palette.trap}`,
          paddingLeft: 28,
          maxWidth: 1600,
        }}
      >
        <Body size={type.small} color={palette.ink} style={{ lineHeight: 1.4 }}>
          {copy.unknown}
        </Body>
      </div>

      {copy.cite ? (
        <div style={{ opacity: enter(frame, fps, 94), marginTop: 22 }}>
          <Cite label={chrome.sourceLabel}>{copy.cite}</Cite>
        </div>
      ) : null}
    </Well>
  );
};
