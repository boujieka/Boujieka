-- Phase 1 (Foundation): profiles table, backing every authenticated user.
--
-- program_id/class_id are added in the Phase 2 migration once the
-- programs/classes tables exist (see PRD.md §8).

create type public.user_role as enum ('student', 'parent', 'teacher', 'admin');

create table public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  role public.user_role not null default 'student',
  full_name text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

comment on table public.profiles is
  'One row per authenticated user. Role-gated columns (role) can only be '
  'changed by service_role, never by the user themself — see '
  'prevent_role_escalation trigger below.';

-- ---------------------------------------------------------------------------
-- updated_at maintenance
-- ---------------------------------------------------------------------------

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger set_profiles_updated_at
  before update on public.profiles
  for each row
  execute function public.set_updated_at();

-- ---------------------------------------------------------------------------
-- Auto-provision a profile row when a new auth user is created.
-- SECURITY DEFINER so it can write to public.profiles despite RLS, since
-- it runs as the (trusted) function owner rather than the new user.
-- ---------------------------------------------------------------------------

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.profiles (id, full_name)
  values (new.id, new.raw_user_meta_data ->> 'full_name');
  return new;
end;
$$;

create trigger on_auth_user_created
  after insert on auth.users
  for each row
  execute function public.handle_new_user();

-- ---------------------------------------------------------------------------
-- Authorization (CLAUDE.md §12/§13): students may read/update their own
-- profile, but must never be able to grant themselves a higher role via
-- that same update. Only service_role (server-side, trusted code) may
-- change `role`.
-- ---------------------------------------------------------------------------

create or replace function public.prevent_role_escalation()
returns trigger
language plpgsql
as $$
begin
  if new.role is distinct from old.role and auth.role() <> 'service_role' then
    new.role := old.role;
  end if;
  return new;
end;
$$;

create trigger profiles_prevent_role_escalation
  before update on public.profiles
  for each row
  execute function public.prevent_role_escalation();

alter table public.profiles enable row level security;

create policy "profiles_select_own"
  on public.profiles for select
  to authenticated
  using (auth.uid() = id);

create policy "profiles_update_own"
  on public.profiles for update
  to authenticated
  using (auth.uid() = id)
  with check (auth.uid() = id);

-- No insert/delete policy for authenticated/anon: rows are created only via
-- the handle_new_user trigger and removed only via auth.users cascade.

-- ---------------------------------------------------------------------------
-- Base table privileges. RLS policies above restrict *which rows* a role
-- can touch, but Postgres also requires a GRANT before a role can attempt
-- an operation on the table at all — without these, every query below
-- fails with "permission denied for table profiles" regardless of RLS.
-- Least privilege: no grants to anon; authenticated gets only what its
-- policies actually allow (select/update, never insert/delete); service_role
-- gets full access since it bypasses RLS by design.
-- ---------------------------------------------------------------------------

grant select, update on public.profiles to authenticated;
grant select, insert, update, delete on public.profiles to service_role;
