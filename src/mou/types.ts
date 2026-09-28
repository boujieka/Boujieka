/**
 * Every film in this project is a list of SceneSpecs.
 *
 * Structure (which scene kinds, in what order, for how long) lives in
 * `structure.ts` and is shared by all locales. Only the words differ per
 * locale, which is what keeps the English and French cuts frame-identical
 * and makes a dropped-in voiceover track valid for both.
 */

export type Locale = "en" | "fr";

export type Citation = string;

/** A single numeric claim pulled from the chapter, with its source. */
export type Stat = {
  value: string;
  unit?: string;
  label: string;
  cite?: Citation;
  /** Colour role. Defaults to "signal". */
  tone?: "signal" | "trap" | "liability" | "pass" | "ink";
};

export type SceneKind =
  | "cold-open"
  | "stat-flip"
  | "two-tests"
  | "stage-ladder"
  | "funnel"
  | "layers"
  | "actor-table"
  | "two-exits"
  | "case-card"
  | "cost-list"
  | "remedy-list"
  | "quote"
  | "title-card"
  | "ask-card"
  | "key-message";

/** Text payloads, one variant per scene kind. */
export type SceneCopy =
  | { kind: "cold-open"; kicker: string; place: string; date: string; headline: string; stats: Stat[]; cite?: Citation }
  | { kind: "stat-flip"; before: Stat; after: Stat; verdict: string; cite?: Citation }
  | { kind: "two-tests"; title: string; lender: { name: string; question: string; asker: string }; state: { name: string; question: string; asker: string }; footnote: string }
  | { kind: "stage-ladder"; title: string; rows: { stage: string; signed: string; binds: string; committed: string }[]; caption: string }
  | { kind: "funnel"; title: string; steps: { label: string; note?: string }[]; stats: Stat[]; unknown: string; cite?: Citation }
  | { kind: "layers"; title: string; layers: { id: "sponsor" | "process" | "system" | "fiscal"; name: string; where: string; policy: string }[]; closing: string }
  | { kind: "actor-table"; title: string; rows: { actor: string; offers: string; costs: string; incentive: string; bearsRisk: boolean; /** Named in the prose as a risk bearer but absent from Table 1.3 itself. */ absent?: boolean }[]; closing: string }
  | { kind: "two-exits"; title: string; stall: { name: string; detail: string; cost: string }; close: { name: string; detail: string; cost: string }; shared: string }
  | { kind: "case-card"; country: string; project: string; verdict: string; beats: string[]; cite?: Citation; tone?: "trap" | "liability" | "pass" }
  | { kind: "cost-list"; title: string; items: { name: string; detail: string }[]; note: string }
  | { kind: "remedy-list"; title: string; items: { n: string; name: string; detail: string; chapter: string }[]; closing: string }
  | { kind: "quote"; text: string; attribution: string }
  | { kind: "title-card"; series: string; title: string; subtitle: string; audience?: string; runtime?: string }
  | { kind: "ask-card"; audience: string; title: string; asks: string[]; because: string }
  | { kind: "key-message"; label: string; text: string; source: string };

/** Timing + identity. Shared across locales. */
export type SceneSpec = {
  id: string;
  kind: SceneKind;
  /** Duration in frames at 30fps. */
  durationInFrames: number;
};

/** One complete film. */
export type FilmSpec = {
  id: string;
  /** Used for the cue sheet and file naming. */
  slug: string;
  scenes: SceneSpec[];
};

/** Per-locale copy for one film: scene id -> copy. */
export type FilmCopy = Record<string, SceneCopy>;

/** Narration line per scene id, for the cue sheet and the audio slot. */
export type FilmNarration = Record<string, string>;

export type LocaleBundle = {
  /** UI chrome that appears across scenes. */
  chrome: {
    series: string;
    chapter: string;
    author: string;
    sourceLabel: string;
    testLender: string;
    testState: string;
    continues: string;
    /** Column headers for the three-stage table (Table 1.1). */
    colSigned: string;
    colBinds: string;
    colCommitted: string;
    tableLabel: string;
    /** Label on the "who carries the risk" marker in the actor table. */
    bearsRiskLabel: string;
    /** Label on an actor who is not at the table at all. */
    absentLabel: string;
  };
  films: Record<string, { copy: FilmCopy; narration: FilmNarration; title: string; audience: string }>;
};
