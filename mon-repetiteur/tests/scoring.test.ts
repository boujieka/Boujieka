import { describe, expect, it } from "vitest";
import { scoreExercise } from "@/lib/scoring";

describe("scoreExercise", () => {
  it("grades multiple_choice by comparing to correctIndex", () => {
    const exercise = {
      type: "multiple_choice" as const,
      content: { choices: ["a", "b", "c"], correctIndex: 1 },
    };
    expect(scoreExercise(exercise, 1)).toBe(true);
    expect(scoreExercise(exercise, 0)).toBe(false);
    expect(scoreExercise(exercise, 2)).toBe(false);
  });

  it("grades true_false by comparing to the stored answer", () => {
    const exercise = { type: "true_false" as const, content: { answer: true } };
    expect(scoreExercise(exercise, true)).toBe(true);
    expect(scoreExercise(exercise, false)).toBe(false);
  });

  it("returns null (not auto-gradable) for short_answer and free_response", () => {
    expect(scoreExercise({ type: "short_answer" as const, content: {} }, "anything")).toBeNull();
    expect(scoreExercise({ type: "free_response" as const, content: {} }, "anything")).toBeNull();
  });

  it("treats a malformed answer as incorrect rather than throwing", () => {
    const exercise = {
      type: "multiple_choice" as const,
      content: { choices: ["a", "b"], correctIndex: 0 },
    };
    expect(scoreExercise(exercise, "not-a-number")).toBe(false);
    expect(scoreExercise(exercise, null)).toBe(false);
  });
});
