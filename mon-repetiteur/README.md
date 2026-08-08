# Mon Répétiteur

A mobile-first, AI-powered exam-prep platform for students preparing for
Cameroon's terminal secondary examinations: **Terminale C** (Francophone,
Baccalauréat) and **GCE A-Level** (Anglophone). See `PRD.md` for the full
product spec and `CLAUDE.md` for engineering/process rules — both are the
source of truth ahead of this README.

## Core loop

```
LEARN → PRACTICE → TEST → DIAGNOSE → GET HELP → PRACTICE AGAIN → IMPROVE
```

## Build phases

Per `CLAUDE.md` §36, each phase has a checks gate (lint + typecheck + test +
build, `CLAUDE.md` §30) before the next one starts. Per the user's explicit
build order, the first vertical (Terminale C → Mathématiques) was taken all
the way through the loop before starting a second program, rather than
building every phase generically first:

```
Phase 0  Repository discovery                                    ✅
Phase 1  Foundation        — Next.js + TS + Tailwind + Supabase, auth   ✅
Phase 2  Curriculum        — programs/classes/subjects/topics/skills/lessons  ✅
         Terminale C / Mathématiques — first-vertical content     ✅
Phase 3  Exercises         — exercise bank, scoring, attempts     ✅
         Progress          — skill_progress tracking              ✅
Phase 6  AI Tutor          — AIService, pedagogical prompt, chat UI  ✅
         Mock Exam         — createMockExam/submitMockExam        ✅
         GCE A-Level       — second program                       ← current
Phase 4  Exam archive      — past papers with rights metadata
Phase 5  Dashboard
Phase 7  Mock exams as a general P1 feature (beyond the first vertical)
Phase 8  Study plans (P1)
Phase 9  Admin CMS (P1)
Phase 10 QA (Playwright E2E suite; so far verified manually per phase)
```

## Stack

- [Next.js](https://nextjs.org) 16 (App Router) + TypeScript + Tailwind CSS
- [Supabase](https://supabase.com): Postgres, Auth, Storage, pgvector — all
  access goes through Row Level Security (`CLAUDE.md` §12)
- [Vitest](https://vitest.dev) + React Testing Library

## Getting started

Requires [Docker](https://docs.docker.com/get-docker/) (the Supabase CLI
runs Postgres/Auth/Storage locally in containers).

```bash
npm install
npm run db:start      # starts the local Supabase stack, applies migrations
npm run db:types      # generate src/lib/supabase/database.types.ts
cp .env.example .env  # fill in from `npx supabase status`
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

`npm run db:start` prints `API_URL` / `ANON_KEY` / `SERVICE_ROLE_KEY` — map
those to `NEXT_PUBLIC_SUPABASE_URL` / `NEXT_PUBLIC_SUPABASE_ANON_KEY` /
`SUPABASE_SERVICE_ROLE_KEY` in `.env`. Local Studio UI is at
`http://127.0.0.1:54323`; local email testing (signup confirmations, if
enabled) is at `http://127.0.0.1:54324`.

## Scripts

| Script                 | Purpose                                              |
| ----------------------- | ------------------------------------------------------ |
| `npm run dev`           | Start the dev server                                    |
| `npm run build`         | Production build                                        |
| `npm run lint`          | ESLint                                                   |
| `npm run typecheck`     | TypeScript, no emit                                      |
| `npm run test`          | Run tests once (Vitest, incl. Supabase/RLS integration)  |
| `npm run test:watch`    | Run tests in watch mode                                  |
| `npm run db:start`      | Start the local Supabase stack                           |
| `npm run db:stop`       | Stop it                                                   |
| `npm run db:reset`      | Recreate the local DB from `supabase/migrations/` + seed |
| `npm run db:migration:new` | Scaffold a new migration file                         |
| `npm run db:diff`       | Diff local schema vs. migrations                         |
| `npm run db:types`      | Regenerate `src/lib/supabase/database.types.ts`          |

## Database

Schema lives in `supabase/migrations/*.sql`. Every table has Row Level
Security enabled — see `CLAUDE.md` §12/§13; `supabase/migrations/*_profiles.sql`
is the reference pattern (RLS policies **and** explicit `GRANT`s — Postgres
requires both, RLS alone isn't enough). Regenerate
`src/lib/supabase/database.types.ts` (committed, not gitignored — CI checks
it isn't stale) after every schema change.

Current tables: `profiles` (role-gated; role changes only via `service_role`,
enforced by a trigger, not just a policy); `programs`/`classes`/`subjects`/
`topics`/`skills`/`lessons` (content-lifecycle-gated: `status` starts at
`draft`, nothing auto-publishes); `exercises`/`attempts` (attempts
immutable once written, scored server-side — see `lib/scoring.ts`);
`skill_progress` (maintained by a trigger on `attempts` insert, not written
directly); `ai_conversations`/`ai_messages` (private to their owner, no
staff bypass — unlike everything else above); `mock_exams`/
`mock_exam_questions`/`mock_exam_answers`. See `PRD.md` §8 for the full
planned entity list (Exam archive, Dashboard, Study plans, Admin CMS still
to come).

## Auth

Supabase Auth, email/password. `src/lib/supabase/{client,server,admin}.ts`
are the three client variants (browser / per-request server / service-role —
see file comments for when to use which). `src/proxy.ts` is this Next.js
version's renamed `middleware.ts` (see `AGENTS.md`); it refreshes the
session cookie on every request. Business logic lives in `src/services/`,
not in components or route files (`CLAUDE.md` §6/§8).

## Checks gate

Required before any phase is considered done (`CLAUDE.md` §30):

```bash
npm run lint && npm run typecheck && npm run test && npm run build
```

CI runs the same checks against a real local Supabase stack on every
push/PR touching `mon-repetiteur/` (`.github/workflows/mon-repetiteur-ci.yml`).

## Known limitations

- Auth is email/password only; local dev has email confirmation disabled
  (`supabase/config.toml`) so signup logs straight in — a deployed project's
  confirmation behavior may differ and isn't tested here.
- No dedicated onboarding flow (program/class selection at signup) — a
  student currently picks a program via `/learn`'s switcher instead.
- No E2E (Playwright) suite committed yet — every phase above was
  smoke-tested manually via a built `next start` server + a throwaway
  script (not committed as test infra); automated E2E is Phase 10 (QA) per
  `CLAUDE.md` §36.
- The AI Tutor's actual model call is unverified in this environment — no
  `ANTHROPIC_API_KEY` was available. Everything up to that call (auth,
  persistence, RLS, prompt construction, exam-mode gating, the "not
  configured" degradation path) is real and tested; the live conversation
  itself isn't.
- Lesson/exercise content across both programs is placeholder text I wrote,
  not sourced against the official OBC / Cameroon GCE Board syllabi — every
  row stays `draft` for exactly this reason (see `PRD.md` §6/§14).
- `/learn` assumes one subject per program (picks `subjects[0]`) and the
  highest-`order` class as the "current" one — stops being safe the moment
  a program gets a second subject or the target class isn't simply
  "highest order".
