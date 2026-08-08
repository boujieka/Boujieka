-- Mock Exam (P1 per CLAUDE.md §4, but pulled forward per the user's
-- explicit build order — see TaskList): a timed set of published
-- exercises the student takes as a personal practice exam, graded
-- server-side like a single exercise attempt but as a batch.
--
-- Distinct from `exams` (the future Exam archive: official past papers
-- with rights metadata, CLAUDE.md §15) — this is generated per student
-- from the exercise bank, not an archived document.

create type public.mock_exam_status as enum ('in_progress', 'submitted');

create table public.mock_exams (
  id uuid primary key default gen_random_uuid(),
  profile_id uuid not null references public.profiles (id) on delete cascade,
  subject_id uuid not null references public.subjects (id) on delete cascade,
  class_id uuid not null references public.classes (id) on delete cascade,
  status public.mock_exam_status not null default 'in_progress',
  score double precision,
  started_at timestamptz not null default now(),
  submitted_at timestamptz
);

create table public.mock_exam_questions (
  id uuid primary key default gen_random_uuid(),
  mock_exam_id uuid not null references public.mock_exams (id) on delete cascade,
  exercise_id uuid not null references public.exercises (id) on delete cascade,
  "order" integer not null default 0,
  unique (mock_exam_id, exercise_id)
);

create table public.mock_exam_answers (
  id uuid primary key default gen_random_uuid(),
  mock_exam_id uuid not null references public.mock_exams (id) on delete cascade,
  mock_exam_question_id uuid not null references public.mock_exam_questions (id) on delete cascade,
  answer jsonb not null,
  is_correct boolean,
  unique (mock_exam_question_id)
);

create index mock_exams_profile_id_idx on public.mock_exams (profile_id);
create index mock_exam_questions_mock_exam_id_idx on public.mock_exam_questions (mock_exam_id);
create index mock_exam_answers_mock_exam_id_idx on public.mock_exam_answers (mock_exam_id);

-- ---------------------------------------------------------------------------
-- RLS: owner-scoped, plus staff (teachers plausibly want to see mock exam
-- performance, unlike AI Tutor conversations — same reasoning as
-- skill_progress, not AI Tutor's privacy-by-default stance).
-- ---------------------------------------------------------------------------

alter table public.mock_exams enable row level security;
alter table public.mock_exam_questions enable row level security;
alter table public.mock_exam_answers enable row level security;

create policy "mock_exams_select_own_or_staff"
  on public.mock_exams for select
  to authenticated
  using (profile_id = auth.uid() or public.is_staff());
create policy "mock_exams_insert_own"
  on public.mock_exams for insert
  to authenticated
  with check (profile_id = auth.uid());
create policy "mock_exams_update_own"
  on public.mock_exams for update
  to authenticated
  using (profile_id = auth.uid())
  with check (profile_id = auth.uid());

create policy "mock_exam_questions_select_own_or_staff"
  on public.mock_exam_questions for select
  to authenticated
  using (
    exists (
      select 1 from public.mock_exams e
      where e.id = mock_exam_questions.mock_exam_id
        and (e.profile_id = auth.uid() or public.is_staff())
    )
  );
create policy "mock_exam_questions_insert_own"
  on public.mock_exam_questions for insert
  to authenticated
  with check (
    exists (
      select 1 from public.mock_exams e
      where e.id = mock_exam_questions.mock_exam_id and e.profile_id = auth.uid()
    )
  );

create policy "mock_exam_answers_select_own_or_staff"
  on public.mock_exam_answers for select
  to authenticated
  using (
    exists (
      select 1 from public.mock_exams e
      where e.id = mock_exam_answers.mock_exam_id
        and (e.profile_id = auth.uid() or public.is_staff())
    )
  );
create policy "mock_exam_answers_insert_own"
  on public.mock_exam_answers for insert
  to authenticated
  with check (
    exists (
      select 1 from public.mock_exams e
      where e.id = mock_exam_answers.mock_exam_id and e.profile_id = auth.uid()
    )
  );

grant select, insert, update on public.mock_exams to authenticated;
grant select, insert on public.mock_exam_questions to authenticated;
grant select, insert on public.mock_exam_answers to authenticated;

grant select, insert, update, delete on public.mock_exams to service_role;
grant select, insert, update, delete on public.mock_exam_questions to service_role;
grant select, insert, update, delete on public.mock_exam_answers to service_role;
