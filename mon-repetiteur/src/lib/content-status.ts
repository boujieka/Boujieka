import type { BadgeTone } from "@/components/ui/badge";

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
