@AGENTS.md

# MON RÉPÉTITEUR — CLAUDE CODE PROJECT INSTRUCTIONS

## 1. PROJECT IDENTITY

**Project name:** Mon Répétiteur

**Mission:** Build a mobile-first AI-powered educational platform for students preparing for examinations in Cameroon.

**Initial target:**

- Terminale C — Francophone Cameroon
- GCE A-Level — Anglophone Cameroon

The product combines:

- curriculum-aligned lessons;
- exercises;
- quizzes;
- authorized past examination papers;
- mock examinations;
- personalized progress tracking;
- AI tutoring;
- personalized revision plans.

The authoritative product specification is: **/PRD.md**

Always read and follow `PRD.md` before implementing product functionality.

## 2. CORE PRODUCT PRINCIPLE

Mon Répétiteur is NOT a document repository.

The fundamental product loop is:

```
LEARN
  ↓
PRACTICE
  ↓
TEST
  ↓
DIAGNOSE
  ↓
GET HELP
  ↓
PRACTICE AGAIN
  ↓
IMPROVE
```

All major product decisions should reinforce this loop.

The ultimate objective is improved student mastery.

## 3. PRIORITY ORDER

When making technical or product decisions, prioritize:

1. Correctness
2. Security
3. Pedagogical integrity
4. Maintainability
5. Performance
6. Accessibility
7. Simplicity
8. Scalability
9. Development speed

Do not sacrifice correctness or security for speed.

## 4. SCOPE CONTROL

The MVP is intentionally limited.

**P0**

- Authentication
- Student onboarding
- Curriculum
- Lessons
- Exercises
- Exercise scoring
- Progress tracking
- Exam archive
- AI Tutor
- Dashboard

**P1**

- Quizzes
- Mock exams
- Study plans
- Admin CMS
- Analytics

**P2**

- Photo exercise recognition
- Payments
- Gamification
- Parent dashboard
- Native mobile applications

Do not implement P2 functionality unless explicitly requested.

Do not expand the product scope without a clear requirement.

## 5. SOURCE OF TRUTH

Use this hierarchy:

```
PRD.md
   ↓
CLAUDE.md
   ↓
Existing code architecture
   ↓
Implementation details
```

If the code and PRD conflict:

1. identify the conflict;
2. avoid destructive changes;
3. explain the conflict;
4. follow the latest explicit product instruction.

Do not silently redefine the product.

## 6. DEVELOPMENT PHILOSOPHY

**Prefer:**

- small changes;
- modular architecture;
- reusable components;
- explicit types;
- server-side validation;
- database-driven content;
- testable services;
- clear separation of concerns.

**Avoid:**

- duplicated logic;
- giant React components;
- hard-coded educational content;
- unnecessary dependencies;
- premature abstractions;
- over-engineering.

## 7. ARCHITECTURE

Preferred stack:

**Frontend**

- Next.js
- React
- TypeScript
- Tailwind CSS

**Backend**

- Supabase
- PostgreSQL
- Supabase Auth
- Supabase Storage
- pgvector

**AI**

Provider-independent AI service abstraction.

Do NOT directly call an LLM provider throughout the application.

Use:

```
AIService
├── chat()
├── explain()
├── generateHint()
├── guidedSolution()
├── generateSimilarExercise()
├── diagnoseStudent()
└── generateStudyPlan()
```

The provider should be replaceable.

## 8. CODE ORGANIZATION

Use a structure similar to:

```
src/
├── app/
├── components/
├── lib/
├── services/
├── types/
└── config/
```

Business logic belongs in services.

Database access belongs in dedicated data/service layers.

Do not put complex business logic inside React components.

Components should primarily handle:

- presentation;
- user interaction;
- local UI state.

## 9. TYPESCRIPT

Use strict TypeScript.

Avoid `any` unless there is a documented technical reason.

Prefer explicit interfaces/types.

Database types should be generated or strongly synchronized with the Supabase schema where practical.

Do not duplicate database types manually if generated types can be used.

## 10. DATABASE

The database is the source of truth for educational content.

Never hard-code curriculum content into React components.

Core entities include:

```
profiles
programs
classes
subjects
topics
skills
lessons
exercises
quizzes
quiz_questions
exams
exam_questions
attempts
skill_progress
study_plans
study_sessions
ai_conversations
ai_messages
subscriptions
```

Use migrations for schema changes.

Never manually modify production schema without a migration.

## 11. DATABASE MIGRATIONS

Every schema modification must produce a migration.

Migration naming: `YYYYMMDDHHMMSS_description.sql`

Migrations must be:

- deterministic;
- reviewable;
- reversible where practical;
- safe to execute more than once where appropriate.

Never delete production data through a migration unless explicitly authorized.

## 12. SUPABASE SECURITY

Row Level Security is mandatory.

Students must only access their own private data.

Students may access:

- own profile;
- own attempts;
- own progress;
- own study plans;
- own AI conversations.

Students must NOT be able to modify:

- published lessons;
- exercises;
- official exam metadata;
- validated solutions;
- validation status.

Teachers/admins require role-based permissions.

Never expose `SUPABASE_SERVICE_ROLE_KEY` to the client.

## 13. AUTHORIZATION

Never rely solely on UI restrictions.

Every protected operation must also be authorized server-side/database-side.

Example: Hiding an Admin button is NOT sufficient. The API/database must reject unauthorized requests.

## 14. EDUCATIONAL CONTENT

Content lifecycle:

```
Draft
  ↓
Under Review
  ↓
Validated
  ↓
Published
  ↓
Archived
```

AI-generated content must NEVER automatically become published educational content.

AI may assist content creators, but human validation is required for important educational content.

## 15. EXAMINATION PAPERS

Never assume that historical examination papers are free to redistribute.

Every examination document must contain rights metadata, e.g.:

```
rights_status
source
source_url
permission_reference
```

Allowed statuses: `verified`, `permission_required`, `publicly_reusable`, `restricted`, `unknown`.

Do not expose/download documents with unresolved rights unless the product explicitly supports a legally appropriate external-link model.

Never fabricate an official examination paper.

Never label demo content as official.

## 16. DEMO CONTENT

Development seed data must clearly be identifiable as demo content.

Use labels such as `DEMO`, `SAMPLE`.

Never create fake examination documents that look official.

## 17. AI TUTOR

The AI Tutor is a pedagogical assistant. It is NOT simply a chatbot.

Default behavior:

```
Question
  ↓
Understand student's level
  ↓
Ask/check understanding when useful
  ↓
Hint
  ↓
Concept
  ↓
Method
  ↓
Guided solution
  ↓
Full solution
```

The Tutor should promote student autonomy.

## 18. AI CONTEXT

When the Tutor is launched from an educational context, pass:

```
program
class
subject
topic
skill
lesson
exercise
student level
relevant history
```

Example: Terminale C → Mathematics → Probability → Binomial distribution

The AI should know this context without forcing the student to repeat it.

## 19. AI RAG

Curriculum-related questions should use retrieval-augmented generation.

Pipeline:

```
Question
↓
Context
↓
Metadata filtering
↓
Vector search
↓
Published educational content
↓
Prompt construction
↓
LLM
↓
Response
```

Prioritize `validation_status = published`.

The AI must not treat arbitrary retrieved text as authoritative unless it has appropriate validation metadata.

## 20. AI HALLUCINATION CONTROL

The Tutor must:

- avoid inventing curriculum requirements;
- avoid inventing examination rules;
- avoid inventing sources;
- acknowledge uncertainty;
- distinguish official content from generated explanations;
- never claim a solution is official unless validated.

For mathematical/scientific calculations, verify results where practical.

## 21. AI SAFETY

Students may be minors.

The Tutor must remain professional, educational, and age-appropriate.

Never encourage inappropriate relationships or inappropriate interactions.

Do not request unnecessary personal information.

Do not assist cheating during an active examination mode.

## 22. EXAM MODE

When exam mode is active: AI assistance = disabled.

The UI must clearly indicate this.

Do not allow a client-side-only mechanism to enforce this restriction. The server must also enforce exam-mode permissions.

## 23. ERROR HANDLING

Every important feature must have:

- loading state;
- success state;
- empty state;
- validation error;
- authorization error;
- server error;
- network failure state.

Never expose stack traces to users.

Log useful diagnostic information server-side.

## 24. API DESIGN

Keep API/service interfaces clean, e.g.:

```
getPrograms()
getSubjects()
getTopics()
getLesson()

getExercises()
submitExerciseAttempt()

getStudentProgress()
getWeakSkills()

createMockExam()
submitMockExam()

sendTutorMessage()
generateHint()
generateSimilarExercise()

generateStudyPlan()
```

Do not couple components directly to database internals.

## 25. UI/UX

Mobile-first.

Minimum target: 360px

Also support: 390px, 412px, 768px, 1024px+

The interface should be clean, modern, readable, fast, accessible.

Avoid unnecessary animation.

## 26. ACCESSIBILITY

Use semantic HTML.

Support: keyboard navigation, focus states, accessible labels, screen readers, sufficient contrast, readable font sizes.

Do not use color alone to communicate status.

## 27. PERFORMANCE

Optimize for mobile and potentially slow connections.

Use: optimized images, lazy loading, caching, appropriate SSR/SSG, database indexes, pagination, streaming where useful.

Do not load large datasets unnecessarily.

## 28. ANALYTICS

Use a centralized analytics abstraction.

Important events:

```
user_registered
onboarding_completed
lesson_started
lesson_completed
exercise_started
exercise_completed
hint_requested
solution_viewed
quiz_completed
exam_viewed
mock_exam_started
mock_exam_completed
tutor_opened
tutor_message_sent
study_plan_created
recommendation_clicked
subscription_started
```

Do not collect unnecessary sensitive personal data.

## 29. TESTING

Every major feature requires tests: unit, integration, E2E.

Critical flows: Registration, Onboarding, Lesson, Exercise, Exam, Mock exam, AI Tutor, Dashboard.

## 30. REQUIRED CHECKS

Before considering work complete, run:

```
npm run lint
npm run typecheck
npm test
```

If an E2E suite exists: `npm run test:e2e`

If scripts do not exist, create appropriate scripts.

Never claim tests passed if they were not actually run.

## 31. GIT DISCIPLINE

Before major changes: inspect git status; inspect recent commits; understand current branch.

Do not: reset unrelated changes; delete user work; force-push; rewrite history.

Do not commit unless explicitly requested.

## 32. DEPENDENCY POLICY

Before adding a dependency:

1. determine whether it is actually necessary;
2. check whether the existing stack already provides the functionality;
3. prefer mature, maintained packages;
4. avoid adding dependencies for trivial functionality.

Document significant dependencies.

## 33. SECRETS

Never hard-code: API keys, passwords, tokens, service-role keys, payment secrets.

Use environment variables.

Never print secrets in logs.

## 34. FILE MODIFICATION RULE

Before modifying an important file: inspect it; understand its dependencies; preserve existing functionality; make the smallest appropriate change.

Do not rewrite entire files unnecessarily.

## 35. WHEN REQUIREMENTS ARE AMBIGUOUS

Do not invent major product requirements.

Instead:

1. check `PRD.md`;
2. inspect existing implementation;
3. choose the simplest reasonable interpretation;
4. document assumptions;
5. continue when the ambiguity is low-risk.

If the ambiguity could materially change architecture, stop and ask for clarification.

## 36. DEVELOPMENT PHASES

Implement in this order:

```
Phase 0 — Repository discovery
Phase 1 — Foundation
Phase 2 — Curriculum
Phase 3 — Exercises
Phase 4 — Exam archive
Phase 5 — Dashboard
Phase 6 — AI Tutor
Phase 7 — Mock exams
Phase 8 — Study plans
Phase 9 — Admin CMS
Phase 10 — QA
```

Do not jump directly to Phase 6.

## 37. FIRST PRODUCT VERTICAL

The first deeply implemented learning vertical should be:

```
Terminale C
→ Mathematics
→ Probability
→ Functions
→ Complex Numbers
```

The objective is to validate the complete learning loop before populating the entire platform.

## 38. DEFINITION OF DONE

A feature is complete only when UI + Business logic + Database + Authorization + Validation + Error handling + Loading states + Empty states + Responsive design + Tests are addressed appropriately.

## 39. CLAUDE CODE BEHAVIOR

Act as: Senior Software Architect, Senior Full-Stack Engineer, AI Engineer, Database Engineer, QA Engineer.

Do not behave as an autonomous product manager.

Do not make large product decisions without justification.

When implementing:

1. inspect;
2. plan;
3. implement;
4. test;
5. inspect results;
6. fix issues;
7. summarize.

## 40. COMMUNICATION FORMAT

Before significant implementation, provide:

```
PLAN
1.
2.
3.

FILES TO CREATE
-

FILES TO MODIFY
-

RISKS
-

TEST PLAN
-
```

After implementation:

```
IMPLEMENTED
-

TESTS
-

RESULTS
-

KNOWN LIMITATIONS
-

NEXT STEP
-
```

Keep reports concise.

## 41. IMPORTANT

Never state "Done" unless the requested functionality has actually been implemented and tested.

Never state "Tests passed" unless tests were actually executed.

Never state "The content is official" unless the source/validation status confirms it.

Never invent data, sources, examination papers, curriculum requirements or institutional information.

END OF CLAUDE.md
