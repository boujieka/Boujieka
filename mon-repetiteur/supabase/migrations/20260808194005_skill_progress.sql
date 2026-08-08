-- Progress: per-student mastery per skill, derived from attempts.
--
-- mastery_score is maintained by a trigger on attempts insert (attempts
-- are immutable — see exercises migration — so insert is the only event
-- that can change it). Not written directly by any client role; the
-- trigger runs SECURITY DEFINER so it doesn't need its own RLS grant.

create table public.skill_progress (
  id uuid primary key default gen_random_uuid(),
  profile_id uuid not null references public.profiles (id) on delete cascade,
  skill_id uuid not null references public.skills (id) on delete cascade,
  -- 0..1 share of graded attempts on this skill that were correct.
  mastery_score double precision not null default 0,
  updated_at timestamptz not null default now(),
  unique (profile_id, skill_id)
);

create index skill_progress_profile_id_idx on public.skill_progress (profile_id);

alter table public.skill_progress enable row level security;

create policy "skill_progress_select_own_or_staff"
  on public.skill_progress for select
  to authenticated
  using (profile_id = auth.uid() or public.is_staff());

grant select on public.skill_progress to authenticated;
grant select, insert, update, delete on public.skill_progress to service_role;

-- ---------------------------------------------------------------------------
-- Recompute mastery_score for (profile, skill) whenever a new exercise
-- attempt comes in. Simple ratio of correct-to-graded attempts on that
-- skill — not a spaced-repetition model, just enough to drive
-- getWeakSkills() meaningfully; can be refined later without a schema
-- change (mastery_score's meaning is owned entirely by this function).
-- ---------------------------------------------------------------------------

create or replace function public.update_skill_progress()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
declare
  target_skill_id uuid;
  correct_count integer;
  graded_count integer;
begin
  if new.attemptable_type <> 'exercise' then
    return new;
  end if;

  select skill_id into target_skill_id
  from public.exercises
  where id = new.attemptable_id;

  if target_skill_id is null then
    return new;
  end if;

  select
    count(*) filter (where a.is_correct),
    count(*) filter (where a.is_correct is not null)
  into correct_count, graded_count
  from public.attempts a
  join public.exercises e
    on e.id = a.attemptable_id and a.attemptable_type = 'exercise'
  where a.profile_id = new.profile_id and e.skill_id = target_skill_id;

  insert into public.skill_progress (profile_id, skill_id, mastery_score, updated_at)
  values (
    new.profile_id,
    target_skill_id,
    case when graded_count > 0 then correct_count::double precision / graded_count else 0 end,
    now()
  )
  on conflict (profile_id, skill_id) do update
    set mastery_score = excluded.mastery_score, updated_at = excluded.updated_at;

  return new;
end;
$$;

create trigger attempts_update_skill_progress
  after insert on public.attempts
  for each row
  execute function public.update_skill_progress();
