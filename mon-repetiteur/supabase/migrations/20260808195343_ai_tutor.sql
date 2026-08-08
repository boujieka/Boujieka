-- AI Tutor: conversations + messages.
--
-- Private by design: unlike lessons/exercises/skill_progress, no staff
-- bypass policy here. A student's conversation with the tutor is theirs
-- alone (PRD.md §2's persona list: "Students may access: ... own AI
-- conversations" — own, not staff-visible-by-default). Revisit only if a
-- concrete, requested feature needs it (e.g. a teacher escalation flow),
-- not preemptively.

create type public.ai_message_role as enum ('user', 'assistant', 'system');

create table public.ai_conversations (
  id uuid primary key default gen_random_uuid(),
  profile_id uuid not null references public.profiles (id) on delete cascade,
  -- Free-form snapshot of {programId, classId, subjectId, topicId,
  -- skillId, lessonId, exerciseId} at conversation start (CLAUDE.md §18).
  -- jsonb rather than seven nullable FK columns: a conversation can be
  -- anchored at any depth, and this context is a snapshot, not a live
  -- relation the DB needs to enforce referential integrity on.
  context jsonb not null default '{}'::jsonb,
  started_at timestamptz not null default now(),
  ended_at timestamptz
);

create table public.ai_messages (
  id uuid primary key default gen_random_uuid(),
  conversation_id uuid not null references public.ai_conversations (id) on delete cascade,
  role public.ai_message_role not null,
  content text not null,
  created_at timestamptz not null default now()
);

create index ai_conversations_profile_id_idx on public.ai_conversations (profile_id);
create index ai_messages_conversation_id_idx on public.ai_messages (conversation_id);

alter table public.ai_conversations enable row level security;
alter table public.ai_messages enable row level security;

create policy "ai_conversations_select_own"
  on public.ai_conversations for select
  to authenticated
  using (profile_id = auth.uid());
create policy "ai_conversations_insert_own"
  on public.ai_conversations for insert
  to authenticated
  with check (profile_id = auth.uid());
create policy "ai_conversations_update_own"
  on public.ai_conversations for update
  to authenticated
  using (profile_id = auth.uid())
  with check (profile_id = auth.uid());

create policy "ai_messages_select_own"
  on public.ai_messages for select
  to authenticated
  using (
    exists (
      select 1 from public.ai_conversations c
      where c.id = ai_messages.conversation_id and c.profile_id = auth.uid()
    )
  );
create policy "ai_messages_insert_own"
  on public.ai_messages for insert
  to authenticated
  with check (
    exists (
      select 1 from public.ai_conversations c
      where c.id = ai_messages.conversation_id and c.profile_id = auth.uid()
    )
  );

grant select, insert, update on public.ai_conversations to authenticated;
grant select, insert on public.ai_messages to authenticated;

grant select, insert, update, delete on public.ai_conversations to service_role;
grant select, insert, update, delete on public.ai_messages to service_role;
