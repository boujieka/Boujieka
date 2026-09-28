import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { bundles } from "../src/mou/content";
import { blueprints, buildFilm, filmDuration, locales, sceneOffsets } from "../src/mou/structure";
import { FPS } from "../src/mou/theme";
import type { Locale } from "../src/mou/types";

/**
 * Generates the voiceover cue sheets.
 *
 *   npm run cues
 *
 * Each sheet gives, per scene, the exact in-point and duration to record
 * against, plus a fit check: narration is timed at NARRATION_WPS words per
 * second and flagged where it would overrun the scene it belongs to. A flagged
 * scene means either the line gets trimmed or the scene's durationInFrames in
 * src/mou/structure.ts gets raised — the sheet is the evidence for which.
 */

/** Measured pace for deliberate, institutional narration: ~150 words/minute. */
const NARRATION_WPS = 2.5;

const timecode = (frames: number): string => {
  const totalSeconds = frames / FPS;
  const m = Math.floor(totalSeconds / 60);
  const s = Math.floor(totalSeconds % 60);
  const ms = Math.round((totalSeconds - Math.floor(totalSeconds)) * 1000);
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}.${String(ms).padStart(3, "0")}`;
};

const wordCount = (text: string): number => text.trim().split(/\s+/).filter(Boolean).length;

type Row = {
  film: string;
  locale: Locale;
  sceneId: string;
  kind: string;
  startFrame: number;
  startTc: string;
  durationFrames: number;
  durationSec: number;
  words: number;
  estSec: number;
  fits: boolean;
  narration: string;
};

const rows: Row[] = [];

for (const blueprint of blueprints) {
  for (const locale of locales) {
    const entry = bundles[locale].films[blueprint.id];
    if (!entry) {
      throw new Error(`No ${locale} copy for ${blueprint.id}`);
    }
    const film = buildFilm(blueprint, locale);
    for (const { spec, from } of sceneOffsets(film)) {
      const narration = entry.narration[spec.id] ?? "";
      const words = wordCount(narration);
      const estSec = words / NARRATION_WPS;
      const durationSec = spec.durationInFrames / FPS;
      rows.push({
        film: blueprint.id,
        locale,
        sceneId: spec.id,
        kind: spec.kind,
        startFrame: from,
        startTc: timecode(from),
        durationFrames: spec.durationInFrames,
        durationSec,
        words,
        estSec,
        fits: estSec <= durationSec,
        narration,
      });
    }
  }
}

mkdirSync(join(process.cwd(), "docs", "cues"), { recursive: true });

// One CSV covering everything, for import into a recording or edit session.
const csv = [
  "film,locale,scene_id,kind,start_frame,start_tc,duration_frames,duration_sec,words,est_vo_sec,fits,narration",
  ...rows.map((r) =>
    [
      r.film,
      r.locale,
      r.sceneId,
      r.kind,
      r.startFrame,
      r.startTc,
      r.durationFrames,
      r.durationSec.toFixed(2),
      r.words,
      r.estSec.toFixed(1),
      r.fits ? "yes" : "NO",
      `"${r.narration.replace(/"/g, '""')}"`,
    ].join(","),
  ),
].join("\n");
writeFileSync(join("docs", "cues", "all-cues.csv"), `${csv}\n`, "utf-8");

// One readable sheet per film per locale, for whoever is at the microphone.
for (const blueprint of blueprints) {
  for (const locale of locales) {
    const entry = bundles[locale].films[blueprint.id];
    if (!entry) {
      continue;
    }
    const mine = rows.filter((r) => r.film === blueprint.id && r.locale === locale);
    const total = filmDuration(buildFilm(blueprint, locale));
    const overruns = mine.filter((r) => !r.fits);

    const lines: string[] = [
      `# ${entry.title} — ${locale.toUpperCase()}`,
      "",
      `**Composition:** \`${blueprint.id}-${locale.toUpperCase()}\`  `,
      `**Audience:** ${entry.audience}  `,
      `**Runtime:** ${timecode(total)} (${total} frames @ ${FPS}fps)  `,
      `**Scenes:** ${mine.length}`,
      "",
      overruns.length > 0
        ? `> **${overruns.length} scene(s) need attention.** The narration below is longer than the scene it sits in, at ${NARRATION_WPS} words/second. Either trim the line or raise that scene's \`durationInFrames\` in \`src/mou/structure.ts\`: ${overruns.map((o) => `\`${o.sceneId}\``).join(", ")}.`
        : `> All narration fits its scene at ${NARRATION_WPS} words/second, with headroom.`,
      "",
      "| In | Scene | Dur | Words | Est. VO | Fits |",
      "| --- | --- | --- | --- | --- | --- |",
      ...mine.map(
        (r) =>
          `| \`${r.startTc}\` | ${r.sceneId} | ${r.durationSec.toFixed(0)}s | ${r.words} | ${r.estSec.toFixed(0)}s | ${r.fits ? "✓" : "**over**"} |`,
      ),
      "",
      "---",
      "",
      "## Script",
      "",
    ];

    for (const r of mine) {
      lines.push(`### \`${r.startTc}\` — ${r.sceneId}`);
      lines.push("");
      lines.push(
        `*${r.kind} · ${r.durationSec.toFixed(0)}s · ${r.words} words · est. ${r.estSec.toFixed(0)}s${r.fits ? "" : " · **OVERRUNS THIS SCENE**"}*`,
      );
      lines.push("");
      lines.push(r.narration || "_(no narration — this scene plays on its visuals)_");
      lines.push("");
    }

    writeFileSync(join("docs", "cues", `${blueprint.slug}.${locale}.md`), `${lines.join("\n")}\n`, "utf-8");
  }
}

const flagged = rows.filter((r) => !r.fits);
// eslint-disable-next-line no-console
console.log(
  `Wrote ${blueprints.length * 2} cue sheets + all-cues.csv to docs/cues/. ` +
    `${flagged.length} of ${rows.length} scenes overrun their narration budget.`,
);
if (flagged.length > 0) {
  for (const r of flagged) {
    // eslint-disable-next-line no-console
    console.log(
      `  over: ${r.film}-${r.locale.toUpperCase()} ${r.sceneId} — ${r.durationSec.toFixed(0)}s allotted, ~${r.estSec.toFixed(0)}s needed`,
    );
  }
}
