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

- **Foundation** — project scaffold (this phase): Next.js + TypeScript,
  Tailwind, ESLint, Prisma (Postgres), Vitest, CI.
- **Database** — schema for users, subjects, curriculum, exercises, exams,
  and AI tutor sessions.
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

```bash
npm install
cp .env.example .env   # then fill in DATABASE_URL
npm run db:generate
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Scripts

| Script               | Purpose                                |
| -------------------- | --------------------------------------- |
| `npm run dev`         | Start the dev server                    |
| `npm run build`       | Production build                        |
| `npm run lint`        | ESLint                                  |
| `npm run typecheck`   | TypeScript, no emit                     |
| `npm run test`        | Run tests once (Vitest)                 |
| `npm run test:watch`  | Run tests in watch mode                 |
| `npm run db:generate` | Regenerate the Prisma client            |
| `npm run db:migrate`  | Apply Prisma migrations (local dev DB)  |

## Audit checklist

Each phase's audit runs, and must pass, before the next phase starts:

```bash
npm run lint && npm run typecheck && npm run test && npm run build
```

CI runs the same checks on every push/PR touching `mon-repetiteur/`
(`.github/workflows/mon-repetiteur-ci.yml`).
