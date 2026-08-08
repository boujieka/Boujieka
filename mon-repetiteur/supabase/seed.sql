-- Reference data: the two programs this product targets, and their class
-- levels. Idempotent (safe on repeated `supabase db reset`).
--
-- This is real structural/reference data (program & class-level names are
-- established facts about each system), not placeholder — unlike lesson
-- content, which stays in `draft` status until sourced against an official
-- syllabus (see PRD.md §6/§14).

insert into public.programs (code, name, language) values
  ('terminale_c', 'Terminale C', 'fr'),
  ('gce_a_level', 'GCE Advanced Level', 'en')
on conflict (code) do update set name = excluded.name, language = excluded.language;

insert into public.classes (program_id, code, name, "order")
select p.id, c.code, c.name, c."order"
from public.programs p
join (values
  ('terminale_c', 'terminale', 'Terminale', 0)
) as c(program_code, code, name, "order") on c.program_code = p.code
on conflict (program_id, code) do update set name = excluded.name, "order" = excluded."order";

insert into public.classes (program_id, code, name, "order")
select p.id, c.code, c.name, c."order"
from public.programs p
join (values
  ('gce_a_level', 'lower_sixth', 'Lower Sixth', 0),
  ('gce_a_level', 'upper_sixth', 'Upper Sixth', 1)
) as c(program_code, code, name, "order") on c.program_code = p.code
on conflict (program_id, code) do update set name = excluded.name, "order" = excluded."order";
