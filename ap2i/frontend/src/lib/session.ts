import "server-only";

/** Server-side configuration and session cookie settings. Never import from client components. */
export const API_URL = (process.env.AP2I_API_URL || "http://127.0.0.1:8000/api/v1").replace(/\/$/, "");

export const SESSION_COOKIE = "ap2i_session";
export const MFA_COOKIE = "ap2i_mfa";

export function cookieOptions(maxAgeSeconds: number) {
  return {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production" && process.env.AP2I_INSECURE_COOKIES !== "1",
    sameSite: "strict" as const,
    path: "/",
    maxAge: maxAgeSeconds,
  };
}
