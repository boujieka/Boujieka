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

-- ---------------------------------------------------------------------------
-- First vertical (PRD.md §5/§37): Terminale C -> Mathématiques ->
-- Probabilités / Fonctions / Nombres complexes.
--
-- Lesson content below is a first-pass draft, NOT sourced against the
-- official OBC syllabus (see PRD.md §6's open assumptions) — every lesson
-- stays at status='draft' here. Nothing in this file sets status to
-- 'published'; that's a deliberate human action per CLAUDE.md §14, not
-- something seed data does for itself.
-- ---------------------------------------------------------------------------

with target_subject as (
  insert into public.subjects (program_id, slug, name)
  select p.id, 'mathematiques', 'Mathématiques'
  from public.programs p where p.code = 'terminale_c'
  on conflict (program_id, slug) do update set name = excluded.name
  returning id
),
target_class as (
  select c.id from public.classes c
  join public.programs p on p.id = c.program_id
  where p.code = 'terminale_c' and c.code = 'terminale'
),
topic_seed (title, "order") as (
  values
    ('Probabilités', 1),
    ('Fonctions', 2),
    ('Nombres complexes', 3)
),
inserted_topics as (
  insert into public.topics (subject_id, class_id, title, "order")
  select (select id from target_subject), (select id from target_class), ts.title, ts."order"
  from topic_seed ts
  on conflict (subject_id, class_id, title) do update set "order" = excluded."order"
  returning id, title
),
skill_seed (topic_title, title, "order") as (
  values
    ('Probabilités', 'Vocabulaire des probabilités', 1),
    ('Probabilités', 'Probabilités conditionnelles', 2),
    ('Probabilités', 'Variables aléatoires et loi binomiale', 3),
    ('Fonctions', 'Limites et continuité', 1),
    ('Fonctions', 'Dérivation et étude de fonctions', 2),
    ('Fonctions', 'Fonction exponentielle et logarithme népérien', 3),
    ('Nombres complexes', 'Forme algébrique et opérations', 1),
    ('Nombres complexes', 'Forme trigonométrique et exponentielle', 2),
    ('Nombres complexes', 'Équations dans l''ensemble des nombres complexes', 3)
),
inserted_skills as (
  insert into public.skills (topic_id, title, "order")
  select it.id, ss.title, ss."order"
  from skill_seed ss
  join inserted_topics it on it.title = ss.topic_title
  on conflict (topic_id, title) do update set "order" = excluded."order"
  returning id, title
),
lesson_seed (skill_title, title, content) as (
  values
    ('Vocabulaire des probabilités', 'Introduction au vocabulaire des probabilités',
     'Brouillon (non valide) : univers, issue, evenement, evenement contraire, evenements incompatibles ; calcul de probabilites par denombrement. A valider par rapport au programme officiel de l''OBC avant publication.'),
    ('Probabilités conditionnelles', 'Probabilites conditionnelles et independance',
     'Brouillon (non valide) : probabilite conditionnelle P(A|B), formule des probabilites totales, independance de deux evenements. A valider par rapport au programme officiel de l''OBC avant publication.'),
    ('Variables aléatoires et loi binomiale', 'Variables aleatoires et loi binomiale',
     'Brouillon (non valide) : variable aleatoire discrete, esperance et variance, epreuve de Bernoulli, loi binomiale B(n, p). A valider par rapport au programme officiel de l''OBC avant publication.'),
    ('Limites et continuité', 'Limites et continuite d''une fonction',
     'Brouillon (non valide) : limite d''une fonction en un point ou a l''infini, continuite, theoreme des valeurs intermediaires. A valider par rapport au programme officiel de l''OBC avant publication.'),
    ('Dérivation et étude de fonctions', 'Derivation et etude de fonctions',
     'Brouillon (non valide) : nombre derive, fonction derivee, sens de variation, extremums, construction d''un tableau de variations. A valider par rapport au programme officiel de l''OBC avant publication.'),
    ('Fonction exponentielle et logarithme népérien', 'Fonction exponentielle et logarithme neperien',
     'Brouillon (non valide) : proprietes de la fonction exponentielle, fonction logarithme neperien comme reciproque, resolution d''equations. A valider par rapport au programme officiel de l''OBC avant publication.'),
    ('Forme algébrique et opérations', 'Nombres complexes : forme algebrique et operations',
     'Brouillon (non valide) : nombre complexe sous forme algebrique a + ib, addition, multiplication, conjugue, module. A valider par rapport au programme officiel de l''OBC avant publication.'),
    ('Forme trigonométrique et exponentielle', 'Nombres complexes : forme trigonometrique et exponentielle',
     'Brouillon (non valide) : module et argument, forme trigonometrique, notation exponentielle e^(i*theta), formules de Moivre et d''Euler. A valider par rapport au programme officiel de l''OBC avant publication.'),
    ('Équations dans l''ensemble des nombres complexes', 'Equations dans l''ensemble des nombres complexes',
     'Brouillon (non valide) : resolution d''equations du second degre a coefficients reels dans l''ensemble des nombres complexes, racines carrees d''un nombre complexe. A valider par rapport au programme officiel de l''OBC avant publication.')
)
insert into public.lessons (skill_id, title, content, status)
select isk.id, ls.title, ls.content, 'draft'
from lesson_seed ls
join inserted_skills isk on isk.title = ls.skill_title
on conflict (skill_id, title) do update set content = excluded.content;

-- ---------------------------------------------------------------------------
-- Phase 3: one auto-gradable exercise per skill. Same draft-until-validated
-- rule as lessons — these are ordinary, well-established maths facts (not
-- Cameroon-specific syllabus minutiae), but stay in 'draft' pending human
-- review, per CLAUDE.md §14.
-- ---------------------------------------------------------------------------

with exercise_seed (skill_title, type, difficulty, prompt, content) as (
  values
    ('Vocabulaire des probabilités', 'multiple_choice', 'easy',
     'Comment note-t-on l''evenement contraire de A ?',
     '{"choices": ["A inter B", "non A", "A union B", "P(A)"], "correctIndex": 1}'::jsonb),
    ('Probabilités conditionnelles', 'true_false', 'medium',
     'Si A et B sont independants, alors P(A inter B) = P(A) x P(B).',
     '{"answer": true}'::jsonb),
    ('Variables aléatoires et loi binomiale', 'multiple_choice', 'medium',
     'Pour une loi binomiale B(n, p), l''esperance E(X) est egale a :',
     '{"choices": ["n x p", "n + p", "p / n", "n x p x (1-p)"], "correctIndex": 0}'::jsonb),
    ('Limites et continuité', 'true_false', 'easy',
     'Si une fonction est derivable en un point, alors elle est continue en ce point.',
     '{"answer": true}'::jsonb),
    ('Dérivation et étude de fonctions', 'multiple_choice', 'easy',
     'La derivee de f(x) = x^2 est :',
     '{"choices": ["x", "2x", "x^2", "2"], "correctIndex": 1}'::jsonb),
    ('Fonction exponentielle et logarithme népérien', 'true_false', 'easy',
     'ln(e) = 1.',
     '{"answer": true}'::jsonb),
    ('Forme algébrique et opérations', 'multiple_choice', 'easy',
     'Le conjugue de z = 3 + 2i est :',
     '{"choices": ["3 - 2i", "-3 + 2i", "3 + 2i", "-3 - 2i"], "correctIndex": 0}'::jsonb),
    ('Forme trigonométrique et exponentielle', 'true_false', 'medium',
     'Le module de z = i est egal a 1.',
     '{"answer": true}'::jsonb),
    ('Équations dans l''ensemble des nombres complexes', 'multiple_choice', 'hard',
     'Dans l''ensemble des nombres complexes, l''equation x^2 + 1 = 0 a pour solutions :',
     '{"choices": ["x = 1 et x = -1", "x = i et x = -i", "Aucune solution", "x = 0"], "correctIndex": 1}'::jsonb)
)
insert into public.exercises (skill_id, type, difficulty, prompt, content, status)
select sk.id, es.type::exercise_type, es.difficulty::difficulty_level, es.prompt, es.content, 'draft'
from exercise_seed es
join public.skills sk on sk.title = es.skill_title
on conflict (skill_id, prompt) do update set content = excluded.content;

-- ---------------------------------------------------------------------------
-- Second program (GCE A-Level -> Mathematics, Upper Sixth), proving the
-- schema/RLS is genuinely program-agnostic rather than Terminale-C-only.
-- Same draft-until-validated rule, same honesty caveat as the Terminale C
-- block above: these are standard, internationally-recognized A-Level
-- topic names and textbook facts (not exam-board-specific claims), still
-- explicitly NOT sourced against the actual Cameroon GCE Board syllabus
-- (PRD.md §6's open assumption #2) — hence 'draft', not 'published'.
-- ---------------------------------------------------------------------------

with target_subject as (
  insert into public.subjects (program_id, slug, name)
  select p.id, 'mathematics', 'Mathematics'
  from public.programs p where p.code = 'gce_a_level'
  on conflict (program_id, slug) do update set name = excluded.name
  returning id
),
target_class as (
  select c.id from public.classes c
  join public.programs p on p.id = c.program_id
  where p.code = 'gce_a_level' and c.code = 'upper_sixth'
),
topic_seed (title, "order") as (
  values
    ('Algebra and Functions', 1),
    ('Statistics', 2)
),
inserted_topics as (
  insert into public.topics (subject_id, class_id, title, "order")
  select (select id from target_subject), (select id from target_class), ts.title, ts."order"
  from topic_seed ts
  on conflict (subject_id, class_id, title) do update set "order" = excluded."order"
  returning id, title
),
skill_seed (topic_title, title, "order") as (
  values
    ('Algebra and Functions', 'Quadratic equations', 1),
    ('Algebra and Functions', 'Indices and surds', 2),
    ('Algebra and Functions', 'Functions and graphs', 3),
    ('Statistics', 'Probability', 1),
    ('Statistics', 'Data representation', 2),
    ('Statistics', 'The normal distribution', 3)
),
inserted_skills as (
  insert into public.skills (topic_id, title, "order")
  select it.id, ss.title, ss."order"
  from skill_seed ss
  join inserted_topics it on it.title = ss.topic_title
  on conflict (topic_id, title) do update set "order" = excluded."order"
  returning id, title
),
lesson_seed (skill_title, title, content) as (
  values
    ('Quadratic equations', 'Introduction to quadratic equations',
     'Draft (unvalidated): the quadratic formula, the discriminant, and what its sign tells you about the roots. Pending review against the official GCE Board syllabus before publication.'),
    ('Indices and surds', 'Laws of indices and surds',
     'Draft (unvalidated): index laws (a^m x a^n = a^(m+n), etc.) and simplifying surds. Pending review against the official GCE Board syllabus before publication.'),
    ('Functions and graphs', 'Functions, domain, range and graphs',
     'Draft (unvalidated): function notation, domain/range, and the horizontal-line test for one-to-one functions. Pending review against the official GCE Board syllabus before publication.'),
    ('Probability', 'Introduction to probability',
     'Draft (unvalidated): sample spaces, mutually exclusive events, the addition rule. Pending review against the official GCE Board syllabus before publication.'),
    ('Data representation', 'Representing and summarizing data',
     'Draft (unvalidated): mean, median, mode, and common ways to represent a data set. Pending review against the official GCE Board syllabus before publication.'),
    ('The normal distribution', 'The normal distribution',
     'Draft (unvalidated): the standard normal distribution, its mean and standard deviation. Pending review against the official GCE Board syllabus before publication.')
)
insert into public.lessons (skill_id, title, content, status)
select isk.id, ls.title, ls.content, 'draft'
from lesson_seed ls
join inserted_skills isk on isk.title = ls.skill_title
on conflict (skill_id, title) do update set content = excluded.content;

with exercise_seed (skill_title, type, difficulty, prompt, content) as (
  values
    ('Quadratic equations', 'true_false', 'medium',
     'If the discriminant b^2 - 4ac is negative, the quadratic equation has no real roots.',
     '{"answer": true}'::jsonb),
    ('Indices and surds', 'multiple_choice', 'easy',
     'Simplify: 2^3 x 2^2 =',
     '{"choices": ["2^5", "2^6", "2^1", "4^5"], "correctIndex": 0}'::jsonb),
    ('Functions and graphs', 'true_false', 'medium',
     'A function is one-to-one if it passes the horizontal line test.',
     '{"answer": true}'::jsonb),
    ('Probability', 'multiple_choice', 'easy',
     'For mutually exclusive events A and B, P(A or B) equals:',
     '{"choices": ["P(A) + P(B)", "P(A) x P(B)", "P(A) - P(B)", "P(A) / P(B)"], "correctIndex": 0}'::jsonb),
    ('Data representation', 'true_false', 'easy',
     'The median is the middle value of an ordered data set.',
     '{"answer": true}'::jsonb),
    ('The normal distribution', 'multiple_choice', 'medium',
     'For a standard normal distribution, the mean is:',
     '{"choices": ["0", "1", "100", "undefined"], "correctIndex": 0}'::jsonb)
)
insert into public.exercises (skill_id, type, difficulty, prompt, content, status)
select sk.id, es.type::exercise_type, es.difficulty::difficulty_level, es.prompt, es.content, 'draft'
from exercise_seed es
join public.skills sk on sk.title = es.skill_title
on conflict (skill_id, prompt) do update set content = excluded.content;
