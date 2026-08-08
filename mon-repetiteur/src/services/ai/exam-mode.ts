import "server-only";

/**
 * Server-side exam-mode check (CLAUDE.md §22): the AI Tutor must refuse
 * to respond while a student is in an active exam. Enforced here, not
 * just hidden in the UI.
 *
 * Currently always returns false: no exam-taking entity exists yet — Mock
 * Exam is a later phase (see TaskList). tutor.ts already calls this on
 * every message, so wiring it to a real "exam attempt in progress" check
 * later is a one-function change, not a new integration point.
 *
 * profileId is kept in the signature (unused for now) for that reason.
 */
// eslint-disable-next-line @typescript-eslint/no-unused-vars
export async function isExamModeActive(profileId: string): Promise<boolean> {
  return false;
}
