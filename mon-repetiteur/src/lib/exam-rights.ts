import { EXPOSABLE_RIGHTS_STATUSES, type Exam, type ExamListItem } from "@/types/exam-archive";

/**
 * Strips source_url unless rights_status permits exposing it (CLAUDE.md
 * §15). Pure — no I/O — so it's directly unit-testable, and applied at
 * the data layer (services/exam-archive.ts) rather than left to page
 * components to remember to check.
 */
export function toExamListItem(exam: Exam): ExamListItem {
  const { source_url, ...rest } = exam;
  const canExpose = EXPOSABLE_RIGHTS_STATUSES.includes(exam.rights_status);
  return { ...rest, accessUrl: canExpose ? source_url : null };
}
