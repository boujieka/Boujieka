-- Phase 2 (Curriculum): program-agnostic curriculum structure.
--
-- programs -> classes -> (subjects, topics -> skills -> lessons).
-- Content-lifecycle-gated (CLAUDE.md §14) tables (lessons here; exercises/
-- exams in later phases) reuse content_status.

create type public.content_status as enum (
  'draft', 'under_review', 'validated', 'published', 'archived'
);

-- ---------------------------------------------------------------------------
-- Role helper. SECURITY DEFINER so RLS policies on *other* tables can check
-- a caller's role without being blocked by profiles' own "select own row
-- only" policy — this only ever returns a boolean, never row contents.
-- ---------------------------------------------------------------------------

create or replace function public.is_staff()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1 from public.profiles
    where id = auth.uid() and role in ('teacher', 'admin')
  );
$$;

-- ---------------------------------------------------------------------------
-- Tables
-- ---------------------------------------------------------------------------

create table public.programs (
  id uuid primary key default gen_random_uuid(),
  code text not null unique,
  name text not null,
  language text not null check (language in ('fr', 'en')),
  created_at timestamptz not null default now()
);

create table public.classes (
  id uuid primary key default gen_random_uuid(),
  program_id uuid not null references public.programs (id) on delete cascade,
  code text not null,
  name text not null,
  "order" integer not null default 0,
  unique (program_id, code)
);

create table public.subjects (
  id uuid primary key default gen_random_uuid(),
  program_id uuid not null references public.programs (id) on delete cascade,
  slug text not null,
  name text not null,
  unique (program_id, slug)
);

create table public.topics (
  id uuid primary key default gen_random_uuid(),
  subject_id uuid not null references public.subjects (id) on delete cascade,
  class_id uuid not null references public.classes (id) on delete cascade,
  parent_id uuid references public.topics (id) on delete cascade,
  title text not null,
  "order" integer not null default 0
);

create table public.skills (
  id uuid primary key default gen_random_uuid(),
  topic_id uuid not null references public.topics (id) on delete cascade,
  title text not null,
  "order" integer not null default 0
);

create table public.lessons (
  id uuid primary key default gen_random_uuid(),
  skill_id uuid not null references public.skills (id) on delete cascade,
  title text not null,
  content text not null,
  status public.content_status not null default 'draft',
  created_by uuid references public.profiles (id) on delete set null,
  published_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

comment on table public.lessons is
  'status starts at draft and only ever reaches published through explicit '
  'human action (CLAUDE.md §14) — nothing in this schema auto-publishes.';

create index classes_program_id_idx on public.classes (program_id);
create index subjects_program_id_idx on public.subjects (program_id);
create index topics_subject_id_class_id_idx on public.topics (subject_id, class_id);
create index topics_parent_id_idx on public.topics (parent_id);
create index skills_topic_id_idx on public.skills (topic_id);
create index lessons_skill_id_idx on public.lessons (skill_id);
create index lessons_status_idx on public.lessons (status);

create trigger set_lessons_updated_at
  before update on public.lessons
  for each row
  execute function public.set_updated_at();

-- ---------------------------------------------------------------------------
-- RLS: curriculum structure (programs/classes/subjects/topics/skills) is
-- readable by any authenticated user — it's navigational metadata, not
-- gated content. Only staff (teacher/admin) can write it. Lessons add a
-- publish gate on top: authenticated users see published lessons, plus
-- their own drafts if they authored one; staff see and write everything.
-- ---------------------------------------------------------------------------

alter table public.programs enable row level security;
alter table public.classes enable row level security;
alter table public.subjects enable row level security;
alter table public.topics enable row level security;
alter table public.skills enable row level security;
alter table public.lessons enable row level security;

create policy "programs_select_all" on public.programs for select to authenticated using (true);
create policy "programs_insert_staff" on public.programs for insert to authenticated with check (public.is_staff());
create policy "programs_update_staff" on public.programs for update to authenticated using (public.is_staff()) with check (public.is_staff());
create policy "programs_delete_staff" on public.programs for delete to authenticated using (public.is_staff());

create policy "classes_select_all" on public.classes for select to authenticated using (true);
create policy "classes_insert_staff" on public.classes for insert to authenticated with check (public.is_staff());
create policy "classes_update_staff" on public.classes for update to authenticated using (public.is_staff()) with check (public.is_staff());
create policy "classes_delete_staff" on public.classes for delete to authenticated using (public.is_staff());

create policy "subjects_select_all" on public.subjects for select to authenticated using (true);
create policy "subjects_insert_staff" on public.subjects for insert to authenticated with check (public.is_staff());
create policy "subjects_update_staff" on public.subjects for update to authenticated using (public.is_staff()) with check (public.is_staff());
create policy "subjects_delete_staff" on public.subjects for delete to authenticated using (public.is_staff());

create policy "topics_select_all" on public.topics for select to authenticated using (true);
create policy "topics_insert_staff" on public.topics for insert to authenticated with check (public.is_staff());
create policy "topics_update_staff" on public.topics for update to authenticated using (public.is_staff()) with check (public.is_staff());
create policy "topics_delete_staff" on public.topics for delete to authenticated using (public.is_staff());

create policy "skills_select_all" on public.skills for select to authenticated using (true);
create policy "skills_insert_staff" on public.skills for insert to authenticated with check (public.is_staff());
create policy "skills_update_staff" on public.skills for update to authenticated using (public.is_staff()) with check (public.is_staff());
create policy "skills_delete_staff" on public.skills for delete to authenticated using (public.is_staff());

create policy "lessons_select_published_or_own_or_staff"
  on public.lessons for select
  to authenticated
  using (status = 'published' or created_by = auth.uid() or public.is_staff());
create policy "lessons_insert_staff" on public.lessons for insert to authenticated with check (public.is_staff());
create policy "lessons_update_staff" on public.lessons for update to authenticated using (public.is_staff()) with check (public.is_staff());
create policy "lessons_delete_staff" on public.lessons for delete to authenticated using (public.is_staff());

-- ---------------------------------------------------------------------------
-- Base table privileges (see profiles migration comment: RLS alone is not
-- enough, Postgres requires a GRANT too).
-- ---------------------------------------------------------------------------

grant select, insert, update, delete on
  public.programs, public.classes, public.subjects, public.topics,
  public.skills, public.lessons
  to authenticated;

grant select, insert, update, delete on
  public.programs, public.classes, public.subjects, public.topics,
  public.skills, public.lessons
  to service_role;
