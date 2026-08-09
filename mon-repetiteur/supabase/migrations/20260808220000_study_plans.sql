-- Phase 8 (Study plans, P1): a personalized revision schedule generated
-- from the student's own weak skills (skill_progress), not invented by an
-- LLM — CLAUDE.md §19/§20 require curriculum-grounded, non-hallucinated
-- content, and generating the *schedule* deterministically from real
-- progress data satisfies that without depending on ANTHROPIC_API_KEY
-- being configured. AIService.generateStudyPlan() (CLAUDE.md §7) wraps
-- this generation.
--
-- study_sessions.skill_id isn't in PRD.md §8's first-pass table sketch —
-- added because a session needs to say *what* to review; PRD.md §8
-- explicitly expects that sketch to be refined per phase.
--
-- One active plan per student at a time (a simplifying business-rule
-- assumption, not from PRD.md — documented here and in the service layer):
-- starting a new plan marks any prior 'active' plan 'cancelled'.

create type public.study_plan_status as enum ('active', 'completed', 'cancelled');

create table public.study_plans (
  id uuid primary key default gen_random_uuid(),
  profile_id uuid not null references public.profiles (id) on delete cascade,
  status public.study_plan_status not null default 'active',
  created_at timestamptz not null default now()
);

create table public.study_sessions (
  id uuid primary key default gen_random_uuid(),
  study_plan_id uuid not null references public.study_plans (id) on delete cascade,
  skill_id uuid not null references public.skills (id) on delete cascade,
  "order" integer not null default 0,
  scheduled_for date not null,
  completed_at timestamptz
);

create index study_plans_profile_id_idx on public.study_plans (profile_id);
create index study_sessions_study_plan_id_idx on public.study_sessions (study_plan_id);

-- ---------------------------------------------------------------------------
-- RLS: owner-scoped, plus staff read (same reasoning as skill_progress/
-- mock_exams — staff plausibly want visibility into a student's plan,
-- unlike AI Tutor conversations' privacy-by-default stance).
-- ---------------------------------------------------------------------------

alter table public.study_plans enable row level security;
alter table public.study_sessions enable row level security;

create policy "study_plans_select_own_or_staff"
  on public.study_plans for select
  to authenticated
  using (profile_id = auth.uid() or public.is_staff());
create policy "study_plans_insert_own"
  on public.study_plans for insert
  to authenticated
  with check (profile_id = auth.uid());
create policy "study_plans_update_own"
  on public.study_plans for update
  to authenticated
  using (profile_id = auth.uid())
  with check (profile_id = auth.uid());

create policy "study_sessions_select_own_or_staff"
  on public.study_sessions for select
  to authenticated
  using (
    exists (
      select 1 from public.study_plans p
      where p.id = study_sessions.study_plan_id
        and (p.profile_id = auth.uid() or public.is_staff())
    )
  );
create policy "study_sessions_insert_own"
  on public.study_sessions for insert
  to authenticated
  with check (
    exists (
      select 1 from public.study_plans p
      where p.id = study_sessions.study_plan_id and p.profile_id = auth.uid()
    )
  );
create policy "study_sessions_update_own"
  on public.study_sessions for update
  to authenticated
  using (
    exists (
      select 1 from public.study_plans p
      where p.id = study_sessions.study_plan_id and p.profile_id = auth.uid()
    )
  )
  with check (
    exists (
      select 1 from public.study_plans p
      where p.id = study_sessions.study_plan_id and p.profile_id = auth.uid()
    )
  );

-- Recurring pattern (see e.g. the exercises/mock_exams migrations): RLS
-- policies alone are not sufficient, Postgres also requires explicit
-- GRANTs to the authenticated/service_role roles.
grant select, insert, update on public.study_plans to authenticated;
grant select, insert, update on public.study_sessions to authenticated;

grant select, insert, update, delete on public.study_plans to service_role;
grant select, insert, update, delete on public.study_sessions to service_role;
