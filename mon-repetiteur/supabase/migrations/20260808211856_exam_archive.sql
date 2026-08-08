-- Exam archive (CLAUDE.md §15): index of past examination papers.
--
-- This is an INDEX, not a file host: no storage_path column yet — there
-- are no real files to store. A row can point at an external `source_url`
-- ("a legally appropriate external-link model" per §15) when rights allow
-- it; when they don't, the row is still visible (title/year/subject) but
-- carries no way to reach the actual document. Uploading and hosting real
-- files is future work for whenever the Admin CMS phase gives a content
-- reviewer a place to attach them with real rights metadata attached —
-- not built preemptively here.

create type public.exam_rights_status as enum (
  'verified', 'permission_required', 'publicly_reusable', 'restricted', 'unknown'
);

create table public.exams (
  id uuid primary key default gen_random_uuid(),
  program_id uuid not null references public.programs (id) on delete cascade,
  subject_id uuid not null references public.subjects (id) on delete cascade,
  year integer not null,
  session text,
  title text not null,
  status public.content_status not null default 'draft',
  rights_status public.exam_rights_status not null default 'unknown',
  source text,
  source_url text,
  permission_reference text,
  created_by uuid references public.profiles (id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (subject_id, year, title)
);

comment on table public.exams is
  'rights_status governs whether source_url may ever reach a client — see '
  'src/services/exams.ts, which strips it server-side unless rights_status '
  'is verified or publicly_reusable. Never expose a document (or a link to '
  'one) on any other status. Never set rights_status to anything but the '
  'default (no real source checked yet) without a real, checked source '
  '(CLAUDE.md section 15/41).';

create table public.exam_questions (
  id uuid primary key default gen_random_uuid(),
  exam_id uuid not null references public.exams (id) on delete cascade,
  exercise_id uuid not null references public.exercises (id) on delete cascade,
  "order" integer not null default 0,
  unique (exam_id, exercise_id)
);

create index exams_subject_id_idx on public.exams (subject_id);
create index exams_status_idx on public.exams (status);
create index exam_questions_exam_id_idx on public.exam_questions (exam_id);

create trigger set_exams_updated_at
  before update on public.exams
  for each row
  execute function public.set_updated_at();

-- ---------------------------------------------------------------------------
-- RLS: same publish-gate pattern as lessons/exercises — staff write,
-- authenticated read once published (or own draft, or staff).
-- ---------------------------------------------------------------------------

alter table public.exams enable row level security;
alter table public.exam_questions enable row level security;

create policy "exams_select_published_or_own_or_staff"
  on public.exams for select
  to authenticated
  using (status = 'published' or created_by = auth.uid() or public.is_staff());
create policy "exams_insert_staff" on public.exams for insert to authenticated with check (public.is_staff());
create policy "exams_update_staff" on public.exams for update to authenticated using (public.is_staff()) with check (public.is_staff());
create policy "exams_delete_staff" on public.exams for delete to authenticated using (public.is_staff());

create policy "exam_questions_select_via_exam"
  on public.exam_questions for select
  to authenticated
  using (
    exists (
      select 1 from public.exams e
      where e.id = exam_questions.exam_id
        and (e.status = 'published' or e.created_by = auth.uid() or public.is_staff())
    )
  );
create policy "exam_questions_insert_staff" on public.exam_questions for insert to authenticated with check (public.is_staff());
create policy "exam_questions_update_staff" on public.exam_questions for update to authenticated using (public.is_staff()) with check (public.is_staff());
create policy "exam_questions_delete_staff" on public.exam_questions for delete to authenticated using (public.is_staff());

grant select, insert, update, delete on public.exams to authenticated;
grant select, insert, update, delete on public.exam_questions to authenticated;

grant select, insert, update, delete on public.exams to service_role;
grant select, insert, update, delete on public.exam_questions to service_role;
