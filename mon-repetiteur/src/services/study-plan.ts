import "server-only";
import { createClient } from "@/lib/supabase/server";
import { getStudentProgress } from "@/services/progress";
import { getClasses, getPrograms, getSkills, getSubjects, getTopics } from "@/services/curriculum";
import type { StudyPlan, StudySession } from "@/types/study-plan";

const DEFAULT_PROGRAM_CODE = "terminale_c";
const SESSIONS_PER_PLAN = 6;
const DAYS_BETWEEN_SESSIONS = 2;
const WEAK_THRESHOLD = 0.7;

interface TargetSkill {
  skillId: string;
  skillTitle: string;
  topicTitle: string;
}

export interface StudySessionWithSkill extends StudySession {
  skillTitle: string;
  topicTitle: string;
}

export interface GenerateStudyPlanResult {
  error: string | null;
  studyPlan: StudyPlan | null;
  sessions: StudySessionWithSkill[];
}

/**
 * Weakest-mastery skills first (skill_progress, ascending, < threshold),
 * then — if that isn't enough to fill a plan (e.g. a brand-new student
 * with little/no progress yet) — unattempted skills in curriculum order,
 * mirroring /learn's own defaulting (no persisted program/class
 * selection exists on profiles yet, see the profiles migration's note),
 * so a plan is still generable from day one. Never invents which skills
 * exist — always sourced from real curriculum/progress data (CLAUDE.md
 * §19/§20).
 */
async function selectTargetSkills(limit: number): Promise<TargetSkill[]> {
  const progress = await getStudentProgress();
  const seen = new Set(progress.map((entry) => entry.skillId));
  const weak = progress
    .filter((entry) => entry.masteryScore < WEAK_THRESHOLD)
    .slice(0, limit)
    .map((entry) => ({
      skillId: entry.skillId,
      skillTitle: entry.skillTitle,
      topicTitle: entry.topicTitle,
    }));

  if (weak.length >= limit) return weak;

  const programs = await getPrograms();
  const program = programs.find((p) => p.code === DEFAULT_PROGRAM_CODE) ?? programs[0];
  if (!program) return weak;

  const [classes, subjects] = await Promise.all([
    getClasses(program.id),
    getSubjects(program.id),
  ]);
  const targetClass = [...classes].sort((a, b) => b.order - a.order)[0];
  const subject = subjects[0];
  if (!targetClass || !subject) return weak;

  const topics = await getTopics(subject.id, targetClass.id);
  const fill: TargetSkill[] = [];
  for (const topic of topics) {
    if (weak.length + fill.length >= limit) break;
    const skills = await getSkills(topic.id);
    for (const skill of skills) {
      if (weak.length + fill.length >= limit) break;
      if (seen.has(skill.id)) continue;
      seen.add(skill.id);
      fill.push({ skillId: skill.id, skillTitle: skill.title, topicTitle: topic.title });
    }
  }

  return [...weak, ...fill];
}

/**
 * AIService.generateStudyPlan() (CLAUDE.md §7): starts a fresh active
 * plan for the signed-in student, cancelling any prior active one (one
 * active plan at a time — see the study_plans migration's note),
 * scheduling one session every DAYS_BETWEEN_SESSIONS days for the
 * student's current weakest/unattempted skills.
 */
export async function generateStudyPlan(): Promise<GenerateStudyPlanResult> {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) {
    return { error: "Vous devez être connecté.", studyPlan: null, sessions: [] };
  }

  const targets = await selectTargetSkills(SESSIONS_PER_PLAN);
  if (targets.length === 0) {
    return {
      error: "Aucune compétence disponible pour générer un plan de révision.",
      studyPlan: null,
      sessions: [],
    };
  }

  await supabase
    .from("study_plans")
    .update({ status: "cancelled" })
    .eq("profile_id", user.id)
    .eq("status", "active");

  const { data: studyPlan, error: planError } = await supabase
    .from("study_plans")
    .insert({ profile_id: user.id })
    .select()
    .single();
  if (planError || !studyPlan) {
    return {
      error: planError?.message ?? "Échec de la création du plan de révision.",
      studyPlan: null,
      sessions: [],
    };
  }

  const today = new Date();
  const sessionRows = targets.map((target, index) => {
    const scheduledFor = new Date(today);
    scheduledFor.setDate(today.getDate() + index * DAYS_BETWEEN_SESSIONS);
    return {
      study_plan_id: studyPlan.id,
      skill_id: target.skillId,
      order: index,
      scheduled_for: scheduledFor.toISOString().slice(0, 10),
    };
  });

  const { data: insertedSessions, error: sessionsError } = await supabase
    .from("study_sessions")
    .insert(sessionRows)
    .select();
  if (sessionsError) {
    return { error: sessionsError.message, studyPlan, sessions: [] };
  }

  const sessionsWithSkill: StudySessionWithSkill[] = (insertedSessions ?? [])
    .map((session) => {
      const target = targets.find((t) => t.skillId === session.skill_id);
      if (!target) return null;
      return { ...session, skillTitle: target.skillTitle, topicTitle: target.topicTitle };
    })
    .filter((entry): entry is StudySessionWithSkill => entry !== null)
    .sort((a, b) => a.order - b.order);

  return { error: null, studyPlan, sessions: sessionsWithSkill };
}

export interface ActiveStudyPlan {
  studyPlan: StudyPlan;
  sessions: StudySessionWithSkill[];
}

/**
 * The signed-in student's most recent non-cancelled plan (active or just-
 * completed) and its sessions, or null if none exists yet. Deliberately
 * not restricted to status='active' only — otherwise a plan would vanish
 * from the page the instant its last session is marked done, which reads
 * as data loss rather than "you finished it".
 */
export async function getActiveStudyPlan(): Promise<ActiveStudyPlan | null> {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) return null;

  const { data: studyPlan, error: planError } = await supabase
    .from("study_plans")
    .select("*")
    .eq("profile_id", user.id)
    .neq("status", "cancelled")
    .order("created_at", { ascending: false })
    .limit(1)
    .maybeSingle();
  if (planError || !studyPlan) {
    if (planError) console.error("getActiveStudyPlan:", planError.message);
    return null;
  }

  const { data: sessions, error: sessionsError } = await supabase
    .from("study_sessions")
    .select("*, skills(title, topics(title))")
    .eq("study_plan_id", studyPlan.id)
    .order("order");
  if (sessionsError) {
    console.error("getActiveStudyPlan (sessions):", sessionsError.message);
    return { studyPlan, sessions: [] };
  }

  const sessionsWithSkill: StudySessionWithSkill[] = (sessions ?? [])
    .filter((session) => session.skills !== null)
    .map((session) => {
      const { skills, ...rest } = session as unknown as StudySession & {
        skills: { title: string; topics: { title: string } | null } | null;
      };
      return {
        ...rest,
        skillTitle: skills!.title,
        topicTitle: skills!.topics?.title ?? "",
      };
    });

  return { studyPlan, sessions: sessionsWithSkill };
}

export interface CompleteStudySessionResult {
  error: string | null;
  session: StudySession | null;
}

/**
 * Marks a session done, then — if every session in its plan is now
 * complete — marks the plan 'completed' too. Never trusts a client-
 * supplied completion state beyond "this session is done" (CLAUDE.md
 * §1/§13): the plan-level status is always derived server-side from the
 * sessions actually recorded as completed.
 */
export async function completeStudySession(sessionId: string): Promise<CompleteStudySessionResult> {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) {
    return { error: "Vous devez être connecté.", session: null };
  }

  const { data: session, error: updateError } = await supabase
    .from("study_sessions")
    .update({ completed_at: new Date().toISOString() })
    .eq("id", sessionId)
    .select()
    .single();
  if (updateError || !session) {
    return { error: updateError?.message ?? "Séance introuvable.", session: null };
  }

  const { data: siblingSessions } = await supabase
    .from("study_sessions")
    .select("completed_at")
    .eq("study_plan_id", session.study_plan_id);
  const allCompleted = (siblingSessions ?? []).every((s) => s.completed_at !== null);
  if (allCompleted) {
    await supabase
      .from("study_plans")
      .update({ status: "completed" })
      .eq("id", session.study_plan_id)
      .eq("profile_id", user.id);
  }

  return { error: null, session };
}
