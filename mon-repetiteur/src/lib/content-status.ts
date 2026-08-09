import type { BadgeTone } from "@/components/ui/badge";
import type { ContentStatus } from "@/types/curriculum";

/** French label + Badge tone for CLAUDE.md §14's content lifecycle
 * (draft -> under_review -> validated -> published -> archived). Shared
 * across any page that surfaces a lesson/exercise/exam's status. */
export const CONTENT_STATUS_META: Record<string, { label: string; tone: BadgeTone }> = {
  draft: { label: "Brouillon", tone: "warning" },
  under_review: { label: "En relecture", tone: "warning" },
  validated: { label: "Validé", tone: "info" },
  published: { label: "Publié", tone: "success" },
  archived: { label: "Archivé", tone: "neutral" },
};

/** Lifecycle advance order — the Admin CMS only ever steps forward one
 * stage at a time; archiving is offered separately from any non-archived
 * state, not part of this chain. */
const STATUS_ORDER: ContentStatus[] = ["draft", "under_review", "validated", "published"];

/** Next step in CLAUDE.md §14's content lifecycle, or null if `current`
 * is already at the end of the advance chain (published/archived). Pure
 * — no "server-only" import, unlike services/admin.ts — so it's directly
 * unit-testable, same reasoning as lib/scoring.ts and lib/exam-rights.ts:
 * pure logic lives in lib/, DB-touching code stays in services/. */
export function nextStatus(current: ContentStatus): ContentStatus | null {
  const index = STATUS_ORDER.indexOf(current);
  if (index === -1 || index === STATUS_ORDER.length - 1) return null;
  return STATUS_ORDER[index + 1];
}
