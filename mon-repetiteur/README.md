# Mon Répétiteur

An AI-assisted tutoring app for the French national curriculum (Éducation
nationale), covering collège and lycée across the core subjects.

## Build pipeline

The project is built in six gated phases — each one followed by an audit
(lint + typecheck + test + build) before the next phase begins:

```
Foundation → Audit → Database → Audit → Curriculum → Audit →
Exercises → Audit → AI Tutor → Audit → Exams → Audit
```

- **Foundation** — project scaffold: Next.js + TypeScript, Tailwind, ESLint,
  Prisma (Postgres), Vitest, CI.
- **Database** (this phase) — Prisma schema for users, subjects, curriculum
  topics, exercises, exams, and AI tutor sessions; initial migration; seed
  skeleton for the subject taxonomy.
- **Curriculum** — structured content for the French programme scolaire.
- **Exercises** — practice exercise bank tied to curriculum topics.
- **AI Tutor** — conversational tutoring assistant.
- **Exams** — timed assessments and results/analytics.

## Stack

- [Next.js](https://nextjs.org) (App Router) + TypeScript
- [Tailwind CSS](https://tailwindcss.com)
- [Prisma](https://www.prisma.io) + PostgreSQL
- [Vitest](https://vitest.dev) + React Testing Library

## Getting started

Requires a local Postgres instance (used for both dev and the test suite's
DB integration tests).

```bash
npm install
cp .env.example .env      # then point DATABASE_URL at your Postgres
npm run db:generate       # generate the Prisma client
npm run db:migrate        # create the dev DB schema (needs shadow DB privileges)
npm run db:seed           # seed the subject taxonomy
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Scripts

| Script                      | Purpose                                          |
| ---------------------------- | ------------------------------------------------- |
| `npm run dev`                | Start the dev server                              |
| `npm run build`              | Production build                                  |
| `npm run lint`                | ESLint                                            |
| `npm run typecheck`          | TypeScript, no emit                               |
| `npm run test`                | Run tests once (Vitest, incl. DB integration)     |
| `npm run test:watch`         | Run tests in watch mode                           |
| `npm run db:generate`        | Regenerate the Prisma client                      |
| `npm run db:migrate`         | Create/apply migrations in dev (needs shadow DB)  |
| `npm run db:migrate:deploy`  | Apply existing migrations (used by CI/prod)       |
| `npm run db:seed`            | Seed the subject taxonomy                         |
| `npm run db:studio`          | Open Prisma Studio                                |

## Database

Schema lives in `prisma/schema.prisma`. Core entities: `User` (with
`ParentStudentLink` for guardian↔student relationships), `Subject` →
`CurriculumTopic` (self-referencing for sub-topics) → `Exercise`, `Exam` /
`ExamQuestion` / `ExamAttempt` / `ExamAnswer`, `TutorSession` /
`TutorMessage`, and `TopicProgress` for per-student mastery tracking.

`prisma/seed.ts` seeds only the `Subject` taxonomy — full curriculum content
is populated in the Curriculum phase.

## Audit checklist

Each phase's audit runs, and must pass, before the next phase starts:

```bash
npm run db:generate && npm run db:migrate:deploy && \
npm run lint && npm run typecheck && npm run test && npm run build
```

CI runs the same checks (against a Postgres service container) on every
push/PR touching `mon-repetiteur/` (`.github/workflows/mon-repetiteur-ci.yml`).
