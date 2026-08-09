import { describe, expect, it } from "vitest";
import { nextStatus } from "@/lib/content-status";

describe("nextStatus", () => {
  it("advances one step at a time through the content lifecycle", () => {
    expect(nextStatus("draft")).toBe("under_review");
    expect(nextStatus("under_review")).toBe("validated");
    expect(nextStatus("validated")).toBe("published");
  });

  it("has no next step once published (archiving is a separate action, not part of this chain)", () => {
    expect(nextStatus("published")).toBeNull();
  });

  it("has no next step for archived content", () => {
    expect(nextStatus("archived")).toBeNull();
  });
});
