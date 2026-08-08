# Mon Répétiteur — Product Requirements Document

**Status:** DRAFT — first pass, derived from `CLAUDE.md`. Needs review before
being treated as final source of truth (see "Open assumptions" at the end).

## 1. Mission

A mobile-first, AI-powered exam-prep platform for students preparing for
Cameroon's terminal secondary examinations:

- **Terminale C** (Francophone system) — leads to the **Baccalauréat**,
  organized by the Office du Baccalauréat du Cameroun (OBC).
- **GCE A-Level** (Anglophone system) — organized by the Cameroon GCE Board.

The product is not a document repository. It is a closed learning loop:

```
LEARN → PRACTICE → TEST → DIAGNOSE → GET HELP → PRACTICE AGAIN → IMPROVE
```

Every P0 feature exists to make that loop work end to end for one exam
series before breadth is added.

## 2. Users

| Persona | Need |
|---|---|
| **Student (Terminale C)** | Master the Bac program: lessons, practice, past papers, mock exams, targeted help on weak topics. |
| **Student (GCE A-Level)** | Same loop, different program/board, different subject list and grading (A–E/O). |
| **Parent** (P2) | Visibility into a child's progress. Not in MVP. |
| **Teacher/Content admin** (P1/P2) | Author and validate lessons/exercises/exam metadata through the content lifecycle. |

## 3. Problem statement

Students preparing for the Bac or GCE A-Level in Cameroon lack a single
tool that combines curriculum-aligned content, practice with real
feedback, authenticated past papers, and personalized help — most
alternatives are static PDF archives (a document repository), not a
learning loop.

## 4. Scope

Mirrors `CLAUDE.md` §4, unchanged:

**P0:** Authentication, student onboarding, curriculum, lessons,
exercises, exercise scoring, progress tracking, exam archive, AI Tutor,
dashboard.

**P1:** Quizzes, mock exams, study plans, admin CMS, analytics.

**P2:** Photo exercise recognition, payments, gamification, parent
dashboard, native mobile apps.

Do not build P2 without an explicit request. Do not expand scope without a
clear requirement — see `CLAUDE.md` §4/§35.

## 5. First vertical (validates the full loop before breadth)

```
Program: Terminale C
Subject: Mathématiques
Topics:  Probabilités, Fonctions (numériques), Nombres complexes
```

Each topic needs, before moving to the next topic or program: at least one
published lesson, a bank of exercises spanning difficulty levels, exercise
scoring, progress tracking against it, exam-archive entries tagged to it
where available, and the AI Tutor able to use it as context.

## 6. Programs & curricula — what's confirmed vs. what needs sourcing

This PRD does **not** assert the following as verified curriculum content;
per `CLAUDE.md` §15/§20/§41 nothing here becomes "official" until sourced
and validated against the actual OBC / Cameroon GCE Board syllabi.

- **Terminale C (OBC, Francophone):** science/math-heavy terminal series in
  the francophone lycée ladder (6ème→Terminale). Known core subjects
  typically include Mathématiques, Physique, Chimie, Sciences de la Vie et
  de la Terre, Français, Anglais, Philosophie, EPS — **exact coefficients,
  syllabus points, and the current official subject list must be sourced
  from OBC material, not assumed.**
- **GCE A-Level (Cameroon GCE Board, Anglophone):** Advanced Level
  certificate, structured as Lower Sixth / Upper Sixth, graded A–E/O,
  subject list independent of the francophone track (e.g. Mathematics,
  Further Mathematics, Physics, Chemistry, Biology, Economics, Geography,
  Literature in English, History — **again, must be sourced from the GCE
  Board syllabus, not assumed.**

Action item before Curriculum phase content entry: obtain or link official
syllabus documents per program/subject and record them as the `source` for
each `topics`/`skills` row (see §8).

## 7. Core product loop → features (P0)

1. **Onboarding** — student selects program (Terminale C / GCE A-Level),
   class/level, and subjects of interest.
2. **Curriculum** — browse program → subject → topic → skill → lesson.
3. **Lessons** — structured content per topic/skill.
4. **Exercises** — practice items per topic/skill, scored automatically
   (objective types) with explanations.
5. **Progress tracking** — per-skill mastery derived from exercise (and
   later quiz/exam) attempts.
6. **Exam archive** — past Bac/GCE papers with rights metadata (§15);
   never presented as available unless `rights_status` allows it.
7. **AI Tutor** — pedagogical assistant scoped to the student's current
   program/class/subject/topic/skill context (§17–§22).
8. **Dashboard** — student's current progress, weak skills, recent
   activity, entry points into the loop.

## 8. Data model (Supabase / Postgres)

Table names per `CLAUDE.md` §10. Columns below are a first-pass sketch to
unblock the Foundation-phase migration — expected to be refined per phase
as each feature is actually built, not finalized upfront.

```
profiles            id (=auth.users.id), role, full_name, program_id, class_id, created_at, updated_at
programs             id, code (e.g. "terminale_c", "gce_a_level"), name, language ("fr"|"en")
classes               id, program_id, code (e.g. "terminale", "upper_sixth"), name, "order"
subjects               id, program_id, slug, name
topics                  id, subject_id, class_id, parent_id (self-ref), title, "order"
skills                   id, topic_id, title, "order"
lessons                  id, skill_id, title, content, status (draft|review|validated|published|archived), created_by, published_at
exercises                id, skill_id, type, difficulty, prompt, content (jsonb), status, created_by
quizzes                   id, skill_id|topic_id, title, status                              -- P1
quiz_questions              id, quiz_id, exercise_id, "order"                                -- P1
exams                        id, program_id, subject_id, year, session, title, rights_status, source, source_url, permission_reference
exam_questions                 id, exam_id, exercise_id, "order"
attempts                        id, profile_id, attemptable_type ("exercise"|"quiz"|"exam"), attemptable_id, answer (jsonb), is_correct, score, attempted_at
skill_progress                   id, profile_id, skill_id, mastery_score, updated_at
study_plans                       id, profile_id, status, created_at                          -- P1
study_sessions                      id, study_plan_id, scheduled_for, completed_at             -- P1
ai_conversations                     id, profile_id, context (jsonb: program/class/subject/topic/skill/lesson/exercise), started_at, ended_at
ai_messages                            id, conversation_id, role (user|assistant|system), content, created_at
subscriptions                            id, profile_id, plan, status, ...                      -- P2, deferred
```

Every table gets Row Level Security per `CLAUDE.md` §12: students read/
write only their own `profiles`/`attempts`/`skill_progress`/`study_plans`/
`ai_conversations`/`ai_messages` rows; `lessons`/`exercises`/`exams`
content is writable only by content-admin roles and readable by students
only when `status = 'published'` (or `rights_status` allows it, for exams).

## 9. AI Tutor

Per `CLAUDE.md` §17–§22:

- Default flow: understand level → check understanding → hint → concept →
  method → guided solution → full solution. Promotes autonomy, doesn't
  jump straight to answers.
- Context (`program, class, subject, topic, skill, lesson, exercise,
  student level, relevant history`) is passed automatically from wherever
  the Tutor is launched — the student never re-states it.
- RAG over `published` content only, metadata-filtered before vector
  search; never treats arbitrary retrieved text as authoritative.
- Disabled entirely in exam mode, enforced server-side (§22).
- Implemented behind the `AIService` abstraction (§7) — no direct
  provider calls from application code.

## 10. Content lifecycle & rights

Draft → Under Review → Validated → Published → Archived (§14). AI may
assist drafting; publishing requires human validation. Exam papers carry
`rights_status` (`verified | permission_required | publicly_reusable |
restricted | unknown`) plus `source`/`source_url`/`permission_reference`;
unresolved-rights documents are never exposed for download (§15). Demo/seed
data is always labeled `DEMO`/`SAMPLE` (§16).

## 11. Non-functional requirements

- **Security:** Supabase Auth, RLS-mandatory, service-role key never
  reaches the client, server-side authorization on every protected
  operation (§12–§13).
- **Mobile-first UI:** 360/390/412/768/1024px+ (§25); accessible — semantic
  HTML, keyboard nav, focus states, sufficient contrast (§26).
- **Performance:** optimized images, lazy loading, caching, indexes,
  pagination, streaming where useful (§27).
- **Analytics:** centralized abstraction, event list per §28, no
  unnecessary PII.
- **Testing:** unit + integration + E2E on critical flows — registration,
  onboarding, lesson, exercise, exam, mock exam, AI Tutor, dashboard (§29).

## 12. Success metrics (draft — confirm before relying on them)

- Activation: % of registered students completing onboarding.
- Engagement: exercises attempted per active student per week.
- Learning signal: mastery-score trend per skill over time for returning
  students.
- Loop completion: % of students who go Lesson → Exercise → (weak-skill)
  → AI Tutor → re-Practice within a session.

## 13. Out of scope for MVP

Everything in P2 (§4): photo exercise recognition, payments, gamification,
parent dashboard, native apps. Multi-country expansion beyond Cameroon.
Subjects/programs beyond the first vertical until it's validated.

## 14. Open assumptions to confirm

1. Exact **Terminale C** subject list, coefficients, and current OBC
   syllabus — not sourced yet, needed before Curriculum-phase content for
   that program is marked anything above `draft`.
2. Exact **GCE A-Level** subject list and Cameroon GCE Board syllabus
   structure (Lower/Upper Sixth split, AS vs A2 equivalence) — same
   caveat.
3. `attempts.attemptable_type`/`attemptable_id` polymorphic pattern
   (§8) vs. separate `exercise_attempts`/`quiz_attempts`/`exam_attempts`
   tables — either is workable; polymorphic chosen here for a smaller
   surface, revisit if it fights Supabase RLS ergonomics in practice.
4. Whether Terminale C and GCE A-Level share any `subjects`/`topics` rows
   (e.g. Mathematics content) or are modeled as fully independent trees —
   currently assumed **independent** per program, given differing
   syllabi and language.
