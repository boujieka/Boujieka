import { describe, expect, it } from "vitest";
import { filterHeaders, FORWARD_REQUEST_HEADERS, isSafePath, isSameOrigin } from "./proxy-rules";

describe("proxy rules", () => {
  it("accepts same-origin requests only", () => {
    expect(isSameOrigin("http://localhost:3000", "localhost:3000")).toBe(true);
    expect(isSameOrigin("https://evil.example", "localhost:3000")).toBe(false);
    expect(isSameOrigin(null, "localhost:3000")).toBe(false);
    expect(isSameOrigin("null", "localhost:3000")).toBe(false);
    expect(isSameOrigin("https://app.ap2i.org", "internal:3000", "app.ap2i.org")).toBe(true);
  });
  it("rejects traversal and token-bearing endpoints", () => {
    expect(isSafePath(["projects", "AP2I-CMR-ENERGY-000001"])).toBe(true);
    expect(isSafePath(["projects", "export.csv"])).toBe(true);
    expect(isSafePath(["..", "admin"])).toBe(false);
    expect(isSafePath(["auth", "login"])).toBe(false);
    expect(isSafePath(["auth", "login", "mfa"])).toBe(false);
    expect(isSafePath(["auth", "me"])).toBe(true);
    expect(isSafePath(["a b"])).toBe(false);
    expect(isSafePath([])).toBe(false);
  });
  it("forwards only allowlisted headers", () => {
    const h = new Headers({ cookie: "x=1", authorization: "Bearer evil", "content-type": "application/json", "x-forwarded-for": "1.2.3.4" });
    const out = filterHeaders(h, FORWARD_REQUEST_HEADERS);
    expect(out.get("content-type")).toBe("application/json");
    expect(out.get("cookie")).toBeNull();
    expect(out.get("authorization")).toBeNull();
    expect(out.get("x-forwarded-for")).toBeNull();
  });
});

import { safeNext } from "./safe-next";
describe("safeNext", () => {
  it("rejects open redirects", () => {
    expect(safeNext("/rescue")).toBe("/rescue");
    expect(safeNext("//evil.com")).toBe("/");
    expect(safeNext("https://evil.com")).toBe("/");
    expect(safeNext("/\\evil.com")).toBe("/");
    expect(safeNext(null)).toBe("/");
  });
});
