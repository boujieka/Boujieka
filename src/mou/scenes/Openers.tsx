import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { enter, fadeUp, pop } from "../anim";
import { Body, Cite, Headline, Kicker, Numeral } from "../components/Type";
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

export const TitleCard: React.FC<{ copy: Extract<SceneCopy, { kind: "title-card" }> }> = ({ copy }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const a = enter(frame, fps, 0);
  const b = enter(frame, fps, 10);
  const c = enter(frame, fps, 20);
  const rule = interpolate(enter(frame, fps, 6), [0, 1], [0, 420]);

  return (
    <AbsoluteFill
      style={{
        padding: `0 ${layout.margin}px`,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
      }}
    >
      <div style={{ ...fadeUp(a), marginBottom: 26 }}>
        <Kicker color={palette.inkFaint}>{copy.series}</Kicker>
      </div>
      <div style={{ height: 4, width: rule, backgroundColor: palette.trap, borderRadius: 2, marginBottom: 36 }} />
      <div style={fadeUp(b, 34)}>
        <Headline size={type.hero} style={{ maxWidth: 1450 }}>
          {copy.title}
        </Headline>
      </div>
      <div style={{ ...fadeUp(c, 26), marginTop: 34, maxWidth: 1250 }}>
        <Body size={type.h3} color={palette.inkMuted} style={{ lineHeight: 1.32 }}>
          {copy.subtitle}
        </Body>
      </div>
      {copy.audience ? (
        <div
          style={{
            ...fadeUp(c, 20),
            marginTop: 54,
            display: "flex",
            gap: 16,
            alignItems: "center",
          }}
        >
          <span
            style={{
              border: `1px solid ${palette.signal}66`,
              color: palette.signal,
              borderRadius: 999,
              padding: "12px 26px",
              fontSize: type.caption,
              fontWeight: 700,
              letterSpacing: 1.6,
              textTransform: "uppercase",
            }}
          >
            {copy.audience}
          </span>
          {copy.runtime ? (
            <span style={{ color: palette.inkFaint, fontSize: type.caption, fontFamily: font.mono }}>
              {copy.runtime}
            </span>
          ) : null}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

const StatTile: React.FC<{ stat: Stat; progress: number }> = ({ stat, progress }) => {
  const c = toneColor(stat.tone);
  return (
    <div
      style={{
        ...fadeUp(progress, 30),
        flex: 1,
        backgroundColor: palette.panel,
        border: `1px solid ${palette.rule}`,
        borderTop: `4px solid ${c}`,
        borderRadius: layout.radius,
        padding: "32px 30px 30px",
        display: "flex",
        flexDirection: "column",
        gap: 14,
        minWidth: 0,
      }}
    >
      <div style={{ display: "flex", alignItems: "baseline", gap: 12, flexWrap: "wrap" }}>
        <Numeral size={76} color={c} mono={false} style={{ letterSpacing: -1.5 }}>
          {stat.value}
        </Numeral>
        {stat.unit ? (
          <span style={{ color: palette.inkMuted, fontSize: type.small, fontWeight: 600 }}>{stat.unit}</span>
        ) : null}
      </div>
      <Body size={type.caption} style={{ lineHeight: 1.35 }}>
        {stat.label}
      </Body>
    </div>
  );
};

export const ColdOpen: React.FC<{ copy: Extract<SceneCopy, { kind: "cold-open" }> }> = ({ copy }) => {
  const chrome = useChrome();
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const a = enter(frame, fps, 0);
  const b = enter(frame, fps, 12);

  return (
    <Well top={186}>
      <div style={{ ...fadeUp(a), display: "flex", alignItems: "center", gap: 22, marginBottom: 26 }}>
        <Kicker>{copy.kicker}</Kicker>
        <span style={{ width: 8, height: 8, borderRadius: 4, backgroundColor: palette.inkFaint }} />
        <span
          style={{
            fontFamily: font.mono,
            fontSize: type.small,
            color: palette.inkMuted,
            fontWeight: 500,
            letterSpacing: 1,
          }}
        >
          {copy.place} · {copy.date}
        </span>
      </div>

      <div style={{ ...fadeUp(b, 30), marginBottom: 54 }}>
        <Headline size={type.h2} style={{ maxWidth: 1560, lineHeight: 1.16, letterSpacing: -1 }}>
          {copy.headline}
        </Headline>
      </div>

      <div style={{ display: "flex", gap: 22, marginBottom: 44 }}>
        {copy.stats.map((stat, i) => (
          <StatTile key={stat.label} stat={stat} progress={enter(frame, fps, 30 + i * 9)} />
        ))}
      </div>

      {copy.cite ? (
        <div style={{ opacity: enter(frame, fps, 74) }}>
          <Cite label={chrome.sourceLabel}>{copy.cite}</Cite>
        </div>
      ) : null}
    </Well>
  );
};

export const StatFlip: React.FC<{ copy: Extract<SceneCopy, { kind: "stat-flip" }> }> = ({ copy }) => {
  const chrome = useChrome();
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const beforeIn = pop(frame, fps, 4);
  const arrowIn = enter(frame, fps, 30);
  const afterIn = pop(frame, fps, 44);
  const verdictIn = enter(frame, fps, 66);

  // The promised figure dims as the delivered figure lands — the whole point.
  const beforeFade = interpolate(frame, [44, 62], [1, 0.34], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const beforeColor = toneColor(copy.before.tone);
  const afterColor = toneColor(copy.after.tone);

  return (
    <Well top={170}>
      <div style={{ display: "flex", alignItems: "center", gap: 56, marginBottom: 64 }}>
        <div style={{ ...fadeUp(beforeIn, 22), opacity: beforeIn * beforeFade, flex: 1 }}>
          <Numeral size={158} color={beforeColor} mono={false} style={{ letterSpacing: -4 }}>
            {copy.before.value}
            {copy.before.unit ? (
              <span style={{ fontSize: 54, marginLeft: 14, color: palette.inkMuted }}>{copy.before.unit}</span>
            ) : null}
          </Numeral>
          <Body size={type.h3} style={{ marginTop: 16 }}>
            {copy.before.label}
          </Body>
        </div>

        <div
          style={{
            opacity: arrowIn,
            transform: `scaleX(${arrowIn})`,
            transformOrigin: "left center",
            display: "flex",
            alignItems: "center",
            gap: 0,
            flexShrink: 0,
          }}
        >
          <div style={{ width: 110, height: 3, backgroundColor: palette.rule }} />
          <div
            style={{
              width: 0,
              height: 0,
              borderTop: "12px solid transparent",
              borderBottom: "12px solid transparent",
              borderLeft: `18px solid ${palette.rule}`,
            }}
          />
        </div>

        <div style={{ ...fadeUp(afterIn, 22), flex: 1 }}>
          <Numeral size={158} color={afterColor} mono={false} style={{ letterSpacing: -4 }}>
            {copy.after.value}
            {copy.after.unit ? (
              <span style={{ fontSize: 54, marginLeft: 14, color: palette.inkMuted }}>{copy.after.unit}</span>
            ) : null}
          </Numeral>
          <Body size={type.h3} color={afterColor} style={{ marginTop: 16, fontWeight: 700 }}>
            {copy.after.label}
          </Body>
        </div>
      </div>

      <div
        style={{
          ...fadeUp(verdictIn, 22),
          borderLeft: `5px solid ${palette.liability}`,
          paddingLeft: 30,
          maxWidth: 1500,
        }}
      >
        <Body size={type.h3} color={palette.ink} style={{ lineHeight: 1.34, fontWeight: 400 }}>
          {copy.verdict}
        </Body>
      </div>

      {copy.cite ? (
        <div style={{ opacity: enter(frame, fps, 86), marginTop: 36 }}>
          <Cite label={chrome.sourceLabel}>{copy.cite}</Cite>
        </div>
      ) : null}
    </Well>
  );
};
