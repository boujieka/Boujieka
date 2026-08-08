-- Natural-key uniqueness for topics/skills/lessons, so seed.sql can use
-- ON CONFLICT and stay idempotent when run without a full db reset (e.g.
-- `supabase db seed` against an already-seeded database).

alter table public.topics
  add constraint topics_subject_class_title_key unique (subject_id, class_id, title);

alter table public.skills
  add constraint skills_topic_title_key unique (topic_id, title);

alter table public.lessons
  add constraint lessons_skill_title_key unique (skill_id, title);
