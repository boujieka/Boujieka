# AP²I — web application

*Every Project. Every Dollar. Every Impact.*

Next.js 15 (App Router) frontend for AP²I — Africa Public Project Intelligence. It renders data from the AP²I API (FastAPI, `ap2i/backend`). It never talks to any other data source.

## Run

```bash
npm ci
AP2I_API_URL=http://127.0.0.1:8000/api/v1 npm run dev      # http://localhost:3000
npm run build && AP2I_API_URL=http://127.0.0.1:8000/api/v1 npm start
```

| Script | What it does |
| --- | --- |
| `dev` / `build` / `start` | Next.js dev server, production build (`output: "standalone"`), production server on port 3000 |
| `lint` | ESLint (`next/core-web-vitals` + `next/typescript`) |
| `typecheck` | `tsc --noEmit` (strict) |
| `test` | Vitest unit tests (i18n key parity, formatting rules, proxy rules) |
| `geo` | Regenerates `public/africa.geojson` (see below) |

Browser smoke test against a running `npm start` and API (uses `playwright-core` with a local Chromium, saves to `screenshots/`):

```bash
AP2I_E2E_EMAIL=... AP2I_E2E_PASSWORD=... node scripts/e2e-smoke.mjs   # CHROMIUM_PATH defaults to /opt/pw-browsers/chromium
```

`AP2I_E2E_CREATE_PLAN=1` also creates a Project Rescue plan, which writes to the database.

### Environment variables (server-side only)

| Variable | Default | Purpose |
| --- | --- | --- |
| `AP2I_API_URL` | `http://127.0.0.1:8000/api/v1` | Backend base URL, used only by server components and route handlers |
| `AP2I_INSECURE_COOKIES` | unset | Set to `1` to drop the `Secure` flag on cookies when running the production build over plain HTTP on a host other than `localhost`. Do not set it in real deployments. |

There are no `NEXT_PUBLIC_*` variables. The browser never receives the API URL or any token.

### Docker

```bash
docker build -t ap2i-web .
docker run -p 3000:3000 -e AP2I_API_URL=http://api:8000/api/v1 ap2i-web
```

The image is multi-stage (`node:22-alpine`), runs `node server.js` from the standalone output, and uses a non-root user (`ap2i`, uid 1001).

## Architecture

```
browser ──► Next.js (this app) ──► AP²I API (/api/v1)
            │ server components: GET with no-store caching (public data, and the user's data via the session cookie)
            │ /api/session/login|mfa|logout|locale   session route handlers
            │ /api/proxy/[...path]                   authenticated generic proxy
```

### Session and proxy

- **Login** (`POST /api/session/login`) calls `POST /auth/login`. The returned access token is stored in the `ap2i_session` cookie. The cookie is `HttpOnly`, `SameSite=Strict`, `Secure` in production, and expires with the token's `expires_in`. The token is never returned to the browser.
- **MFA**: when the API answers `mfa_required`, the challenge is kept in a 5-minute httpOnly cookie (`ap2i_mfa`), and the browser only learns that a code is needed. `POST /api/session/mfa {code}` completes the login through `POST /auth/login/mfa`.
- **Logout** (`POST /api/session/logout`) calls `POST /auth/logout`, which revokes every issued token, and then clears the cookie.
- **Proxy** (`/api/proxy/<path>` → `AP2I_API_URL/<path>`):
  - Adds `Authorization: Bearer <token>` from the cookie.
  - CSRF protection: refuses any non-GET/HEAD/OPTIONS request whose `Origin` header is missing or does not match the app host (`Host` / `X-Forwarded-Host`).
  - Forwards only allowlisted headers. Request: `accept`, `accept-language`, `content-type`, `if-none-match`. Response: `content-type`, `content-disposition`, `content-length`, `x-report-id`, `x-request-id`, `etag`.
  - Rejects path traversal and the token-bearing endpoints (`auth/login*`, `auth/logout`), which must go through the session routes.
  - Streams request bodies (multipart uploads) and response bodies (PDF/XLSX/CSV downloads keep their `Content-Disposition`).
  - Clears the session cookie when the API answers 401.
- Permission checks in the UI only hide features. The API enforces every permission and plan feature.

### Security headers

`next.config.ts` sets the following headers:

- **CSP**: `default-src 'self'`, `connect-src 'self'`, and `worker-src 'self' blob:` plus `img-src 'self' data: blob:` for MapLibre.
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy`
- HSTS in production

### Internationalisation

All UI strings are in `src/i18n/fr.ts` and `src/i18n/en.ts`. French is the default. `src/i18n/i18n.test.ts` checks that both dictionaries have identical keys. The language choice is stored in the `ap2i_locale` cookie (`POST /api/session/locale`).

### Data-presentation rules (enforced in `src/components/value.tsx` and `src/lib/format.ts`)

- A missing value (`null`, `undefined`, `""`) is always rendered as **Non disponible / Not available**, never as 0.
- Amounts are shown per currency and are never summed across currencies. USD equivalents appear only when the API provides them, together with their method or rate source and the `usd_complete` flag.
- Data-nature and verification badges are shown wherever the API returns them.
- Chart elements and dashboard figures link to the underlying records, for example `/projects?country=CMR&sector=ENERGY`, `/projects?…&year_from=Y&year_to=Y`, `/explorer?flow=disbursement&year=Y`, or `/performance?level=…`.
- Every dashboard shows the coverage disclaimer.

### Africa map

`scripts/build-africa-geojson.mjs` converts `world-atlas@2.0.2/countries-110m.json` (Natural Earth, public domain) with `topojson-client`. It keeps only the 54 countries whose `iso_numeric` (zero-padded to 3 digits) is listed by `GET /api/v1/countries`. If the API is unreachable, it falls back to the cached list in `scripts/africa-countries.json`.

Five small island states have no 1:110m polygon: Cabo Verde, Comoros, Mauritius, Seychelles, and São Tomé and Príncipe. They are written as point features at their capitals and drawn as clickable circle markers. The legend says so, and the "Island states" box lists them.

MapLibre GL uses a blank style: a background layer plus fill, line and circle layers, with no tile server. Countries with `has_data=false` are grey and show "no data".

## Layout

```
src/app/                 pages (server components) + api/ route handlers
src/components/ui/       local shadcn-style primitives (button, card, badge, table, form, alert)
src/components/          shared components (value formatting, badges, charts, map, forms)
src/i18n/                fr/en dictionaries
src/lib/                 API client (server), session config, proxy rules, formatting, types
scripts/                 geo build, browser smoke test
public/                  logo, africa.geojson (generated, committed)
```
