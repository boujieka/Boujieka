-- Courant platform: run once in Supabase (SQL editor) to create user profiles with access tiers.
-- Every new account gets tier 'registered'. To grant institutional access, change the tier in Table Editor > profiles.

create table if not exists public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  email text,
  organisation text,
  tier text not null default 'registered' check (tier in ('registered', 'institutional')),
  created_at timestamptz not null default now()
);

alter table public.profiles enable row level security;

-- Each user can read only their own row. Nobody can write from the browser; tiers are changed by the owner in the dashboard.
drop policy if exists "read own profile" on public.profiles;
create policy "read own profile" on public.profiles for select to authenticated using (auth.uid() = id);
revoke insert, update, delete on public.profiles from anon, authenticated;

create or replace function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id, email, organisation)
  values (new.id, new.email, coalesce(new.raw_user_meta_data ->> 'organisation', ''))
  on conflict (id) do nothing;
  return new;
end; $$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users for each row execute function public.handle_new_user();
