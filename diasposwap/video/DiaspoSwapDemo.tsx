import React from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  OffthreadVideo,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  Easing,
} from "remotion";

// Product demo for DiaspoSwap (simulation build): 9:16 (1080x1920) or 16:9 (1920x1080),
// chosen from the composition size.
// Colours come from diasposwap/docs/DESIGN_SYSTEM.md.
const C = {
  petrol: "#082F35",
  emerald: "#087F6D",
  gold: "#C9A44C",
  ivory: "#FAF8F2",
  anthracite: "#182525",
};
const FONT = "Inter, 'Inter Display', sans-serif";

type Timed = { start: number; end: number };
export type DiaspoSwapDemoProps = {
  captions: (Timed & { text: string })[];
  chapters: (Timed & { label: string })[];
  // y0/y1: fractions of the source capture height (780x1688) to outline.
  highlights: (Timed & { y0: number; y1: number })[];
  screenEnd: number;
  duration: number;
};

type Geo = { w: number; h: number; left: number; top: number };
const useWide = () => {
  const { width, height } = useVideoConfig();
  return width > height;
};
const phoneGeo = (wide: boolean): Geo => {
  const h = wide ? 940 : 1400;
  const w = Math.round((h * 780) / 1688);
  return wide ? { w, h, left: 300, top: 70 } : { w, h, left: (1080 - w) / 2, top: 230 };
};

const Phone: React.FC<{ highlights: DiaspoSwapDemoProps["highlights"] }> = ({ highlights }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const { w: PHONE_W, h: PHONE_H, left, top } = phoneGeo(useWide());
  const enter = spring({ frame, fps, config: { damping: 200 }, durationInFrames: 20 });
  return (
    <div
      style={{
        position: "absolute",
        left: left - 14,
        top: top - 14,
        width: PHONE_W + 28,
        height: PHONE_H + 28,
        borderRadius: 64,
        background: C.petrol,
        boxShadow: "0 40px 90px rgba(8,47,53,0.35)",
        opacity: enter,
        transform: `translateY(${(1 - enter) * 40}px)`,
      }}
    >
      <div
        style={{
          position: "absolute",
          left: 14,
          top: 14,
          width: PHONE_W,
          height: PHONE_H,
          borderRadius: 52,
          overflow: "hidden",
          background: C.ivory,
        }}
      >
        <OffthreadVideo
          src={staticFile("diasposwap/screen.mp4")}
          muted
          style={{
            width: PHONE_W,
            height: PHONE_H,
          }}
        />
        {highlights.map((h, i) => {
          const k = interpolate(t, [h.start, h.start + 0.35, h.end - 0.3, h.end], [0, 1, 1, 0], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.inOut(Easing.cubic),
          });
          if (k <= 0) return null;
          return (
            <div
              key={i}
              style={{
                position: "absolute",
                left: PHONE_W * 0.045,
                right: PHONE_W * 0.045,
                top: PHONE_H * h.y0,
                height: PHONE_H * (h.y1 - h.y0),
                border: `5px solid ${C.gold}`,
                borderRadius: 18,
                boxShadow: `0 0 0 ${2000}px rgba(8,47,53,${0.28 * k})`,
                opacity: k,
                transform: `scale(${0.96 + 0.04 * k})`,
              }}
            />
          );
        })}
      </div>
    </div>
  );
};

const Chapter: React.FC<{ label: string; len: number }> = ({ label, len }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const inP = spring({ frame, fps, config: { damping: 18, stiffness: 160 } });
  const out = interpolate(frame, [len - 8, len], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  if (useWide()) {
    return (
      <div
        style={{
          position: "absolute",
          left: 880,
          right: 120,
          top: 250,
          opacity: Math.min(inP, out),
          transform: `translateX(${(1 - inP) * 30}px)`,
          fontFamily: FONT,
          fontWeight: 800,
          fontSize: 62,
          lineHeight: 1.1,
          letterSpacing: -1,
          color: C.petrol,
          borderLeft: `10px solid ${C.gold}`,
          paddingLeft: 32,
        }}
      >
        {label}
      </div>
    );
  }
  return (
    <div
      style={{
        position: "absolute",
        top: 92,
        width: "100%",
        display: "flex",
        justifyContent: "center",
        opacity: Math.min(inP, out),
        transform: `translateY(${(1 - inP) * -20}px)`,
      }}
    >
      <div
        style={{
          background: C.petrol,
          color: C.ivory,
          fontFamily: FONT,
          fontWeight: 700,
          fontSize: 40,
          padding: "16px 34px",
          borderRadius: 999,
          borderLeft: `8px solid ${C.gold}`,
          letterSpacing: -0.3,
        }}
      >
        {label}
      </div>
    </div>
  );
};

const Caption: React.FC<{ text: string; len: number; bottom?: boolean }> = ({ text, len, bottom }) => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [0, 4, len - 3, len], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  if (useWide() && !bottom) {
    return (
      <div
        style={{
          position: "absolute",
          left: 922,
          right: 120,
          top: 560,
          opacity: o,
          fontFamily: FONT,
          fontWeight: 600,
          fontSize: 56,
          lineHeight: 1.22,
          color: C.anthracite,
        }}
      >
        {text}
      </div>
    );
  }
  return (
    <div
      style={{
        position: "absolute",
        bottom: 70,
        left: 60,
        right: 60,
        display: "flex",
        justifyContent: "center",
        opacity: o,
      }}
    >
      <div
        style={{
          fontFamily: FONT,
          fontWeight: 700,
          fontSize: 50,
          lineHeight: 1.18,
          color: C.anthracite,
          background: "rgba(250,248,242,0.96)",
          padding: "14px 28px",
          borderRadius: 22,
          textAlign: "center",
          boxShadow: "0 10px 30px rgba(8,47,53,0.18)",
        }}
      >
        {text}
      </div>
    </div>
  );
};

const EndCard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame, fps, config: { damping: 200 }, durationInFrames: 18 });
  const wide = useWide();
  return (
    <AbsoluteFill
      style={{
        background: C.petrol,
        opacity: p,
        alignItems: "center",
        justifyContent: wide ? "flex-start" : "center",
        paddingTop: wide ? 70 : 0,
        fontFamily: FONT,
        color: C.ivory,
        textAlign: "center",
      }}
    >
      <Img src={staticFile("diasposwap/mark-light.svg")} style={{ width: wide ? 160 : 220, height: wide ? 160 : 220, marginBottom: wide ? 24 : 40 }} />
      <div style={{ fontSize: 92, fontWeight: 800, letterSpacing: -2 }}>DiaspoSwap</div>
      <div style={{ fontSize: 44, marginTop: 18, opacity: 0.9 }}>L'argent circule localement.</div>
      <div style={{ fontSize: 44, opacity: 0.9 }}>La valeur voyage.</div>
      <div
        style={{
          marginTop: wide ? 50 : 90,
          border: `3px solid ${C.gold}`,
          color: C.gold,
          borderRadius: 18,
          padding: "18px 30px",
          fontSize: 38,
          fontWeight: 700,
          maxWidth: 860,
        }}
      >
        Démonstration — mode simulation
        <br />
        aucun argent réel n'est transféré
      </div>
      <div style={{ marginTop: wide ? 36 : 60, fontSize: 40, opacity: 0.85 }}>diasposwap.expo.app</div>
    </AbsoluteFill>
  );
};

const WideFrame: React.FC = () => (
  <>
    <div style={{ position: "absolute", left: 922, top: 120, display: "flex", alignItems: "center", gap: 18 }}>
      <Img src={staticFile("diasposwap/mark-light.svg")} style={{ width: 64, height: 64, background: C.petrol, borderRadius: 16, padding: 8 }} />
      <div style={{ fontFamily: FONT, fontWeight: 800, fontSize: 40, color: C.petrol, letterSpacing: -0.5 }}>DiaspoSwap</div>
    </div>
    <div
      style={{
        position: "absolute",
        left: 922,
        bottom: 110,
        fontFamily: FONT,
        fontWeight: 700,
        fontSize: 30,
        color: "#8A6A1F",
        border: `3px solid ${C.gold}`,
        borderRadius: 14,
        padding: "10px 20px",
      }}
    >
      Mode simulation — aucun argent réel
    </div>
  </>
);

export const DiaspoSwapDemo: React.FC<DiaspoSwapDemoProps> = ({ captions, chapters, highlights, screenEnd, duration }) => {
  const { fps } = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);
  const wide = useWide();
  return (
    <AbsoluteFill style={{ background: `linear-gradient(${wide ? 90 : 180}deg, ${C.ivory} 0%, #EFEBDD 100%)` }}>
      <Audio src={staticFile("diasposwap/narration.wav")} />
      <Sequence durationInFrames={f(screenEnd) + 10}>
        <Phone highlights={highlights} />
        {wide && <WideFrame />}
      </Sequence>
      {chapters.map((c) => (
        <Sequence key={c.label} from={f(c.start)} durationInFrames={f(c.end) - f(c.start)}>
          <Chapter label={c.label} len={f(c.end) - f(c.start)} />
        </Sequence>
      ))}
      <Sequence from={f(screenEnd)} durationInFrames={f(duration) - f(screenEnd)}>
        <EndCard />
      </Sequence>
      {captions.map((c, i) => {
        const next = captions[i + 1];
        const end = next ? Math.min(next.start, c.end + 0.35) : c.end + 0.3;
        return (
          <Sequence key={i} from={f(c.start)} durationInFrames={Math.max(1, f(end) - f(c.start))}>
            <Caption text={c.text} len={Math.max(1, f(end) - f(c.start))} bottom={c.start >= screenEnd} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
