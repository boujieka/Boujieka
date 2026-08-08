import { describe, expect, it } from "vitest";
import { toExamListItem } from "@/lib/exam-rights";
import type { Exam, ExamRightsStatus } from "@/types/exam-archive";

function makeExam(overrides: Partial<Exam>): Exam {
  return {
    id: "exam-1",
    program_id: "program-1",
    subject_id: "subject-1",
    year: 2023,
    session: null,
    title: "Test exam",
    status: "published",
    rights_status: "unknown",
    source: null,
    source_url: "https://example.com/paper.pdf",
    permission_reference: null,
    created_by: null,
    created_at: "2026-01-01T00:00:00Z",
    updated_at: "2026-01-01T00:00:00Z",
    ...overrides,
  };
}

describe("toExamListItem (CLAUDE.md §15 rights gating)", () => {
  it.each<ExamRightsStatus>(["verified", "publicly_reusable"])(
    "exposes source_url as accessUrl when rights_status is %s",
    (rights_status) => {
      const item = toExamListItem(makeExam({ rights_status }));
      expect(item.accessUrl).toBe("https://example.com/paper.pdf");
      expect(item).not.toHaveProperty("source_url");
    },
  );

  it.each<ExamRightsStatus>(["permission_required", "restricted", "unknown"])(
    "strips source_url (accessUrl is null) when rights_status is %s",
    (rights_status) => {
      const item = toExamListItem(makeExam({ rights_status }));
      expect(item.accessUrl).toBeNull();
      expect(item).not.toHaveProperty("source_url");
    },
  );

  it("returns null accessUrl even for an exposable status if there's no source_url", () => {
    const item = toExamListItem(makeExam({ rights_status: "verified", source_url: null }));
    expect(item.accessUrl).toBeNull();
  });
});
