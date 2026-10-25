// End-to-end tests of the built portal (npm run build first). Run: npm run e2e
// Uses the real exported snapshot in public/data (copied into dist by the build).
import { after, before, describe, it } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { readFileSync } from "node:fs";
import { chromium } from "playwright-core";

const PORT = 4179;
// E2E_BASE=https://ap2i-africa.netlify.app/ runs the same tests against the deployed site (no local server).
const BASE = process.env.E2E_BASE || `http://localhost:${PORT}/`;
const EXE = process.env.CHROMIUM_PATH || "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";
let server, browser;

async function page(width = 1366) {
  const p = await browser.newPage({ viewport: { width, height: 900 }, acceptDownloads: true });
  p.errors = [];
  p.on("pageerror", (e) => p.errors.push(e.message));
  return p;
}
const ready = (p) => p.waitForSelector("main h1", { timeout: 20000 });
const chartPoint = (p, id, coord) => p.evaluate(([id, coord]) => {
  const el = document.querySelector(`[data-testid="chart-${id}"]`);
  el.scrollIntoView({ block: "center" });
  const v = el.__chart.getOption().series[0].data[coord[1]];
  const pt = el.__chart.convertToPixel({ seriesIndex: 0 }, coord[0] === "mid" ? [v / 2, coord[1]] : coord);
  const r = el.getBoundingClientRect();
  return { x: r.left + pt[0], y: r.top + pt[1] };
}, [id, coord]);

before(async () => {
  if (!process.env.E2E_BASE) server = spawn("npx", ["vite", "preview", "--port", String(PORT), "--strictPort"], { stdio: "ignore" });
  for (let i = 0; i < 60; i++) {
    try { if ((await fetch(BASE)).ok) break; } catch { /* starting */ }
    await new Promise((r) => setTimeout(r, 500));
  }
  browser = await chromium.launch({ executablePath: EXE, args: ["--use-gl=swiftshader", "--enable-unsafe-swiftshader"] });
});
after(async () => {
  await browser?.close();
  server?.kill();
});

describe("AP²I portal", () => {
  it("Africa map: clicking Cameroon opens the Cameroon dashboard", async () => {
    const p = await page();
    await p.goto(BASE + "#/africa");
    await p.waitForSelector('[data-testid="africa-map"][data-ready="1"]', { timeout: 20000 });
    await p.waitForTimeout(800);
    const pt = await p.evaluate(() => {
      const el = document.querySelector('[data-testid="africa-map"]');
      const xy = el.__map.project([12.4, 5.6]); // inside Cameroon
      const r = el.getBoundingClientRect();
      return { x: r.left + xy.x, y: r.top + xy.y };
    });
    await p.mouse.click(pt.x, pt.y);
    await p.waitForFunction(() => location.hash.startsWith("#/country/CMR"));
    await p.waitForSelector("text=Cameroon");
    assert.deepEqual(p.errors, []);
  });

  it("country without data is shown as not available, never zero", async () => {
    const p = await page();
    await p.goto(BASE + "#/country/GAB");
    await ready(p);
    assert.match(await p.innerText("main"), /not available|non disponibles/i);
  });

  it("year, sector and institution filters update counts and the URL", async () => {
    const p = await page();
    await p.goto(BASE + "#/projects");
    await ready(p);
    const count = async () => Number((await p.innerText("main .page-head .sub")).replace(/\D/g, ""));
    const all = await count();
    await p.selectOption('[data-testid="f-y0"]', "2020");
    await p.waitForFunction(() => location.hash.includes("y0=2020"));
    const y = await count();
    assert.ok(y > 0 && y < all, `year filter ${y} / ${all}`);
    await p.selectOption('[data-testid="f-sector"]', "ENERGY");
    await p.waitForFunction(() => location.hash.includes("sector=ENERGY"));
    const ys = await count();
    assert.ok(ys > 0 && ys <= y);
    await p.selectOption('[data-testid="f-partner"]', "WB");
    await p.waitForFunction(() => location.hash.includes("partner=WB"));
    assert.ok((await count()) <= ys);
    // shareable: reloading the URL restores the same selection
    const n = await count();
    await p.reload();
    await ready(p);
    assert.equal(await count(), n);
    await p.click('[data-testid="f-reset"]');
    await p.waitForFunction(() => !location.hash.includes("y0="));
    assert.equal(await count(), all);
  });

  it("dashboard KPIs change when the sector filter changes", async () => {
    const p = await page();
    await p.goto(BASE + "#/country/CMR");
    await ready(p);
    const kpi = () => p.innerText(".kpis .kpi:first-child .kpi-v");
    const before = await kpi();
    await p.selectOption('[data-testid="f-sector"]', "TRANSPORT");
    await p.waitForFunction((b) => document.querySelector(".kpis .kpi:first-child .kpi-v").textContent !== b, before);
    assert.notEqual(await kpi(), before);
  });

  it("chart drill-down: clicking a sector bar filters the dashboard", async () => {
    const p = await page();
    await p.goto(BASE + "#/country/CMR");
    await ready(p);
    await p.waitForTimeout(1500);
    const pt = await chartPoint(p, "c3", ["mid", 0]); // middle of the first sector bar
    await p.mouse.click(pt.x, pt.y);
    await p.waitForFunction(() => /sector=/.test(location.hash));
    assert.match(await p.evaluate(() => location.hash), /^#\/country\/CMR\?.*sector=/);
  });

  it("search, project profile with sources, and CSV export with provenance", async () => {
    const p = await page();
    await p.goto(BASE + "#/projects");
    await ready(p);
    await p.fill('[data-testid="f-q"]', "Social Safety Nets");
    await p.waitForFunction(() => location.hash.includes("q="));
    const [dl] = await Promise.all([p.waitForEvent("download"), p.click('[data-testid="projects-table-csv"]')]);
    const csv = readFileSync(await dl.path(), "utf8");
    assert.match(csv, /^\ufeff"?# Public records only/);
    assert.match(csv, /Social Safety Nets/);
    await p.click('[data-testid="projects-table"] tbody tr:first-child td:nth-child(2) a');
    await p.waitForFunction(() => location.hash.startsWith("#/project/"));
    await p.waitForSelector("text=Provenance");
    assert.match(await p.innerText("main"), /World Bank/);
    assert.deepEqual(p.errors, []);
  });

  it("alerts are interactive and link to the project evidence", async () => {
    const p = await page();
    await p.goto(BASE + "#/performance?alert=critical_attention");
    await ready(p);
    const rows = await p.$$('[data-testid="alerts-table"] tbody tr');
    assert.ok(rows.length >= 1);
    await p.click('[data-testid="alerts-table"] tbody tr:first-child td:nth-child(2) a');
    await p.waitForSelector("#alerts");
    assert.match(await p.innerText("#alerts"), /Evidence|Éléments probants/);
  });

  it("Project Rescue: actions can be added, updated and survive a reload (local draft)", async () => {
    const p = await page();
    await p.goto(BASE + "#/rescue");
    await ready(p);
    await p.click('[data-testid="rescue-top"] >> nth=0'); // ranked list of projects to review first
    await p.waitForSelector('[data-testid="rescue-action"]');
    await p.fill('[data-testid="rescue-action"]', "Verify the disbursement schedule with the executing agency");
    await p.click('[data-testid="rescue-add"]');
    await p.selectOption("table tbody tr:first-child select", "done");
    await p.reload();
    await p.waitForSelector("text=Verify the disbursement schedule");
    assert.match(await p.innerText("main"), /1\/1/);
  });

  it("data explorer distinguishes missing from zero and exports", async () => {
    const p = await page();
    await p.goto(BASE + "#/data?measure=projects&dim=sector&col=status");
    await ready(p);
    assert.match(await p.innerText('[data-testid="dx-table"]'), /—/);
    const [dl] = await Promise.all([p.waitForEvent("download"), p.click('[data-testid="dx-table-csv"]')]);
    assert.match(readFileSync(await dl.path(), "utf8"), /no observation|aucune observation/);
  });

  it("empty selection and unknown project show explicit states", async () => {
    const p = await page();
    await p.goto(BASE + "#/projects?q=zzzz-no-such-project");
    await ready(p);
    assert.match(await p.innerText("main"), /No result|Aucun résultat/);
    await p.goto(BASE + "#/project/NOT-A-PROJECT");
    await p.waitForSelector("text=/not found|introuvable/");
  });

  it("data loading failure shows an error with retry", async () => {
    const p = await page();
    await p.route("**/data/projects.json", (r) => r.fulfill({ status: 500, body: "x" }));
    await p.goto(BASE + "#/");
    await p.waitForSelector("text=/could not be loaded|n'ont pas pu|Connection unavailable|Connexion indisponible/");
    await p.unroute("**/data/projects.json");
    await p.click("text=/Retry|Réessayer/");
    await ready(p);
  });

  it("home leads to the projects in trouble, most severe first", async () => {
    const p = await page();
    await p.goto(BASE + "#/");
    await ready(p);
    await p.click('[data-testid="home-task1"]');
    await p.waitForFunction(() => location.hash.includes("alert=attention"));
    const first = await p.innerText('[data-testid="projects-table"] tbody tr:first-child');
    assert.match(first, /Critical attention|Attention critique/);
  });

  it("skip link focuses the content without leaving the page", async () => {
    const p = await page();
    await p.goto(BASE + "#/finance");
    await ready(p);
    await p.keyboard.press("Tab");
    await p.keyboard.press("Enter");
    await p.waitForTimeout(300);
    assert.equal(await p.evaluate(() => location.hash), "#/finance");
    assert.equal(await p.evaluate(() => document.activeElement?.id), "main");
  });

  it("compare dialog is modal and closes with Escape", async () => {
    const p = await page();
    await p.goto(BASE + "#/projects?view=table");
    await ready(p);
    for (const i of [1, 2]) await p.click(`[data-testid="projects-table"] tbody tr:nth-child(${i}) input[type=checkbox]`);
    await p.click("text=/Compare \\(2\\)|Comparer \\(2\\)/");
    await p.waitForSelector("dialog[open]");
    assert.equal(await p.evaluate(() => !!document.activeElement?.closest("dialog")), true);
    await p.keyboard.press("Escape");
    await p.waitForFunction(() => !document.querySelector("dialog[open]"));
  });

  it("commercial and legal pages render; the contact form stays closed until the publisher is set", async () => {
    const p = await page();
    for (const path of ["plans", "legal/terms", "legal/privacy", "legal/data"]) {
      await p.goto(BASE + "#/" + path);
      await ready(p);
      assert.doesNotMatch(await p.innerText("main"), /\bcom\.[a-z]/); // no untranslated key
    }
    await p.goto(BASE + "#/contact");
    await ready(p);
    assert.equal(await p.$eval("main fieldset", (f) => f.disabled), true);
    assert.deepEqual(p.errors, []);
  });

  it("chart data is available as a table (accessibility)", async () => {
    const p = await page();
    await p.goto(BASE + "#/country/CMR");
    await ready(p);
    await p.click('[id="c3"] summary');
    assert.ok((await p.$$('[id="c3"] .chart-data tbody tr')).length > 3);
  });

  it("global search opens a project; follow and recently viewed appear on the home page", async () => {
    const p = await page();
    await p.goto(BASE + "#/");
    await ready(p);
    await p.fill('[data-testid="hero-search"]', "Nachtigal");
    await p.waitForSelector("#hsearch-list li[role=option]");
    await p.keyboard.press("Enter");
    await p.waitForFunction(() => location.hash.startsWith("#/project/"));
    await p.waitForSelector(".summary-text");
    assert.match(await p.innerText(".summary-text"), /Nachtigal|financ/i);
    await p.click('[data-testid="follow"]');
    await p.goto(BASE + "#/");
    await ready(p);
    await p.waitForSelector(".mine li a");
    assert.ok((await p.$$(".mine li a")).length >= 2); // followed + recently viewed
  });

  it("project page: who finances what, guarantee and unpublished disbursements are labelled, never shown as 0 or 100 %", async () => {
    for (const width of [1366, 375]) {
      const p = await page(width);
      await p.goto(BASE + "#/project/AP2I-CMR-ENERGY-000014");
      await p.waitForSelector(".facts");
      const lenders = await p.innerText("table.lenders");
      assert.match(lenders, /Guarantee|Garantie/);
      assert.match(lenders, /Not published|Non publié/);
      const disb = await p.innerText(".facts .fact:nth-child(2)");
      assert.doesNotMatch(disb, /100\s?%/); // only one lender publishes: no project-wide rate
      assert.ok((await p.$$(".tl-list li")).length >= 3);
      const w = await p.evaluate(() => document.documentElement.scrollWidth);
      assert.ok(w <= width, `scrollWidth ${w}`);
      assert.deepEqual(p.errors, []);
    }
  });

  it("home: search first, key figures, projects to watch with their reason", async () => {
    const p = await page();
    await p.goto(BASE + "#/");
    await ready(p);
    assert.ok(await p.isVisible('[data-testid="hero-search"]'));
    assert.equal(await p.$('[data-testid="global-search"]'), null); // one search box on the home page
    const items = await p.$$(".watch li");
    assert.ok(items.length >= 3);
    assert.match(await items[0].innerText(), /Pourquoi|Why/);
    await p.fill('[data-testid="hero-search"]', "EIB Nachtigal"); // lender names are searchable
    await p.waitForSelector("#hsearch-list li[role=option]");
    assert.match(await p.innerText("#hsearch-list"), /Nachtigal/);
    assert.deepEqual(p.errors, []);
  });

  it("mobile: every module renders without horizontal scrolling", async () => {
    const p = await page(375);
    for (const path of ["", "africa", "country/CMR", "projects", "finance", "performance", "rescue", "data", "about", "plans", "contact", "legal/data"]) {
      await p.goto(BASE + "#/" + path);
      await ready(p);
      await p.waitForTimeout(400);
      const w = await p.evaluate(() => document.documentElement.scrollWidth);
      assert.ok(w <= 375, `${path || "home"} scrollWidth ${w}`);
    }
    assert.deepEqual(p.errors, []);
  });
});
