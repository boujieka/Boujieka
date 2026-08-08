-- Phase 3 (Exercises): exercise bank + attempts.
--
-- Exercises reuse content_status (draft/under_review/validated/published/
-- archived) exactly like lessons — they're educational content subject to
-- the same human-validation requirement (CLAUDE.md §14), auto-gradable or
-- not.
--
-- attempts is intentionally polymorphic (attemptable_type/attemptable_id)
-- rather than exercise_attempts/quiz_attempts/exam_attempts, per
-- CLAUDE.md §10's entity list and PRD.md §8's open assumption #3 — only
-- 'exercise' is used for now; 'quiz'/'exam' get added when those phases
-- need them, not preemptively.

create type public.exercise_type as enum (
  'multiple_choice', 'true_false', 'short_answer', 'free_response'
);

create type public.difficulty_level as enum ('easy', 'medium', 'hard');

create type public.attemptable_type as enum ('exercise');

create table public.exercises (
  id uuid primary key default gen_random_uuid(),
  skill_id uuid not null references public.skills (id) on delete cascade,
  type public.exercise_type not null,
  difficulty public.difficulty_level not null default 'medium',
  prompt text not null,
  -- Shape depends on `type`: {choices: string[], correctIndex: number} for
  -- multiple_choice, {answer: boolean} for true_false. short_answer/
  -- free_response aren't auto-graded yet (see scoreExercise).
  content jsonb not null,
  status public.content_status not null default 'draft',
  created_by uuid references public.profiles (id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (skill_id, prompt)
);

create index exercises_skill_id_idx on public.exercises (skill_id);
create index exercises_status_idx on public.exercises (status);

create trigger set_exercises_updated_at
  before update on public.exercises
  for each row
  execute function public.set_updated_at();

create table public.attempts (
  id uuid primary key default gen_random_uuid(),
  profile_id uuid not null references public.profiles (id) on delete cascade,
  attemptable_type public.attemptable_type not null,
  attemptable_id uuid not null,
  answer jsonb not null,
  -- null = not auto-gradable (e.g. free_response), not "ungraded yet".
  is_correct boolean,
  score double precision,
  attempted_at timestamptz not null default now()
);

create index attempts_profile_id_idx on public.attempts (profile_id);
create index attempts_attemptable_idx on public.attempts (attemptable_type, attemptable_id);

comment on table public.attempts is
  'Immutable once written: no update/delete policy for any role below '
  'service_role. is_correct/score are always computed server-side from the '
  'stored exercise content, never trusted from the client (CLAUDE.md §1/§13).';

-- ---------------------------------------------------------------------------
-- RLS
-- ---------------------------------------------------------------------------

alter table public.exercises enable row level security;
alter table public.attempts enable row level security;

create policy "exercises_select_published_or_own_or_staff"
  on public.exercises for select
  to authenticated
  using (status = 'published' or created_by = auth.uid() or public.is_staff());
create policy "exercises_insert_staff" on public.exercises for insert to authenticated with check (public.is_staff());
create policy "exercises_update_staff" on public.exercises for update to authenticated using (public.is_staff()) with check (public.is_staff());
create policy "exercises_delete_staff" on public.exercises for delete to authenticated using (public.is_staff());

create policy "attempts_select_own"
  on public.attempts for select
  to authenticated
  using (profile_id = auth.uid());
create policy "attempts_insert_own"
  on public.attempts for insert
  to authenticated
  with check (profile_id = auth.uid());
-- No update/delete policy for authenticated: attempts are immutable once
-- submitted, by design (integrity of progress history).

grant select, insert, update, delete on public.exercises to authenticated;
grant select, insert on public.attempts to authenticated;

grant select, insert, update, delete on public.exercises to service_role;
grant select, insert, update, delete on public.attempts to service_role;
