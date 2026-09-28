// Renders every composition to out/. Pass a browser path when Remotion cannot
// download its own Chrome Headless Shell:
//   REMOTION_BROWSER=/path/to/chromium npm run render:all
import { execFileSync } from "node:child_process";
import { mkdirSync } from "node:fs";

const films = [
  ["MoUTrap-Core", "core"],
  ["MoUTrap-Ministers", "ministers"],
  ["MoUTrap-Finance", "finance"],
  ["MoUTrap-Regulators", "regulators"],
  ["MoUTrap-Developers", "developers"],
];
const locales = ["EN", "FR"];

mkdirSync("out", { recursive: true });

const extra = process.env.REMOTION_BROWSER
  ? [`--browser-executable=${process.env.REMOTION_BROWSER}`]
  : [];

for (const [id, slug] of films) {
  for (const locale of locales) {
    const composition = `${id}-${locale}`;
    const output = `out/${slug}.${locale.toLowerCase()}.mp4`;
    console.log(`\n=== ${composition} -> ${output} ===`);
    execFileSync("npx", ["remotion", "render", composition, output, ...extra], {
      stdio: "inherit",
    });
  }
}
console.log("\nAll ten films rendered to out/.");
