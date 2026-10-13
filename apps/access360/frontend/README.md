# ACCESS360 AFRICA: web frontend

Next.js 16 (App Router, TypeScript strict), Tailwind CSS 4, shadcn-style components on Radix primitives,
Recharts, MapLibre GL JS 6, English/French via a small dictionary (`lib/i18n.tsx`).

The browser only calls same-origin `/api/*`; `next.config.ts` rewrites those requests to the FastAPI backend
(`BACKEND_URL`), so the httpOnly `a360_session` cookie stays first party. Every POST/PUT/DELETE sends
`X-Requested-With: access360` (`lib/api.ts`). No tokens are stored in the browser; only the selected
organisation and the language are kept in `localStorage`.

## Requirements

- Node.js 20.9+ (tested with 22), npm 10
- The backend in `../backend` (FastAPI + PostgreSQL 16 on 127.0.0.1:5433), see its own docs

## Environment variables

| Variable | Where | Default | Purpose |
| --- | --- | --- | --- |
| `BACKEND_URL` | server (build and start) | `http://127.0.0.1:8000` | Target of the `/api/*` rewrite |
| `NEXT_PUBLIC_MAP_STYLE_URL` | browser (inlined at build) | `https://demotiles.maplibre.org/style.json` | MapLibre basemap style. If it cannot be loaded the map falls back to a plain background and says so |
| `NEXT_TELEMETRY_DISABLED` | build tooling | unset | Set to `1` to turn off Next.js build telemetry |

Copy `.env.example` to `.env.local` to override. The frontend holds no secrets.

## Commands

```bash
cd apps/access360/frontend
npm install                 # install dependencies
npm run dev                 # dev server on http://localhost:3000 (copies the MapLibre worker first)
npm run build               # production build (copies the MapLibre worker first)
npm run start               # serve the production build on port 3000
npx tsc --noEmit            # type check (also: npm run typecheck)
npm run lint                # ESLint (eslint-config-next)
```

Start the API for development (from `apps/access360/backend`):

```bash
. .venv/bin/activate
A360_JWT_SECRET=dev-secret-0123456789abcdef A360_DEMO_PASSWORD=Demo-password-2027 python -m app.seed demo
A360_JWT_SECRET=dev-secret-0123456789abcdef uvicorn app.main:app --port 8000
```

Demo login: `demo@access360.example` with the `A360_DEMO_PASSWORD` used when seeding.

## End to end tests (Playwright)

The tests run against the real backend and the real Next.js production server. `playwright.config.ts`
starts both if they are not already running (backend: seed demo + uvicorn on :8000; frontend:
`npm run build && npm run start` on :3000) and reuses them if they are.

```bash
export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers   # in the sandbox; elsewhere run `npx playwright install chromium` once
npx playwright test e2e/flow.spec.ts               # register, project, demo inputs, run, sensitivity, teaser PDF, FR, optimizer, explore
SCREENSHOTS=1 npx playwright test e2e/screenshots.spec.ts   # writes ../docs/screenshots/*.png (demo workspace)
```

Optional variables: `E2E_BASE_URL` (default `http://127.0.0.1:3000`), `A360_JWT_SECRET`, `A360_DEMO_PASSWORD`.
`@playwright/test` is pinned to 1.56.1 to match the preinstalled Chromium build 1194.

## Layout

- `app/` routes: `/`, `/login`, `/register`, `/forgot-password`, `/reset-password?token=...`, `/app` (dashboard), `/app/projects`, `/app/projects/new`,
  `/app/projects/[id]?tab=overview|inputs|results|sensitivity|subsidy|milestones|exports`, `/app/optimizer`,
  `/app/explore`, `/app/finance`, `/app/reports`, `/app/admin` (members, MFA, account security: change password, log out everywhere), planned pages `/app/portfolio`,
  `/app/investors`, `/app/delivery`, and `/app/academy`
- `components/ui/` hand-written shadcn-style primitives (button, card, badge, input, tabs, dropdown, table, alert)
- `components/project/` project tabs; `components/charts.tsx` Recharts wrappers; `components/map-view.tsx` MapLibre
- `lib/` API client, session and organisation context, i18n dictionary, formatting, metric definitions

## Conventions enforced in the UI

- Every number comes from the API. Money carries its currency (the LCY code from the project inputs, or USD),
  negatives are in parentheses, percentages have one decimal.
- Model status is always a badge with plain wording; "Validated" only when the API returns `validated`.
- Anything demo (`is_demo` on organisation, project, run or dataset) shows a "Synthetic demo data" badge.
  The dashboard and the Finance page keep real and demo figures in separate panels and never add them.
- Percent inputs are typed as % and sent as fractions. 422 responses are shown next to the field (by `loc`)
  and as a list above the form.
- User and dataset text is rendered as text only (no `dangerouslySetInnerHTML`; map popups use text nodes).

## Known issues and gaps

- MapLibre 6 loads its web worker from a separate file. `scripts/copy-maplibre-worker.mjs` copies it to
  `public/maplibre/` (git ignored) before `dev` and `build`; `map-view.tsx` points the library at it.
- The backend warning `W_REVIEW` is emitted with `label` and `passed` swapped (`label: false`,
  `passed: "Assumptions not yet reviewed..."`). The UI shows the text defensively; the backend should fix the
  positional `Check(...)` call in `engine/checks.py`.
- The dashboard alerts and milestones lists come from the API as one list (they are not figures, so nothing is summed).
- Country boundaries, admin 1 regions, populated places and the country profile come from the bundled public
  reference data (Natural Earth, Our World in Data, World Bank WDI via a mirror; see `../docs/public-data-manifest.md`).
  Run `python -m app.ingest_public` in the backend once, or the Explore page shows "Data unavailable".
- Inputs field labels are bilingual; texts produced by the backend (check labels, warnings, optimizer
  explanation) are shown in English as returned.
- Dark mode is not implemented (light theme only).
