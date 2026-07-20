/**
 * Authentification par rôles — sessions JWT signées, déposées en cookie
 * httpOnly. Trois rôles applicatifs : offtaker, developer, admin.
 *
 * Le secret de signature est lu côté serveur uniquement (AUTH_SECRET).
 */
import { SignJWT, jwtVerify } from "jose";
import { cookies } from "next/headers";

export type Role = "offtaker" | "developer" | "admin";

export interface SessionPayload {
  userId: string;
  organizationId: string;
  role: Role;
  email: string;
  fullName: string;
  [key: string]: unknown;
}

export const SESSION_COOKIE = "aten_session";
const MAX_AGE_SECONDS = 60 * 60 * 24 * 7; // 7 jours

function secretKey(): Uint8Array {
  const secret = process.env.AUTH_SECRET;
  if (!secret) {
    throw new Error("AUTH_SECRET manquant — définir la variable d'environnement.");
  }
  return new TextEncoder().encode(secret);
}

export async function signSession(payload: SessionPayload): Promise<string> {
  return new SignJWT(payload)
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt()
    .setExpirationTime(`${MAX_AGE_SECONDS}s`)
    .sign(secretKey());
}

export async function verifySession(token: string): Promise<SessionPayload | null> {
  try {
    const { payload } = await jwtVerify(token, secretKey());
    return payload as SessionPayload;
  } catch {
    return null;
  }
}

/** Dépose le cookie de session (Server Action / Route Handler). */
export async function createSessionCookie(payload: SessionPayload): Promise<void> {
  const token = await signSession(payload);
  cookies().set(SESSION_COOKIE, token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    path: "/",
    maxAge: MAX_AGE_SECONDS,
  });
}

export function clearSessionCookie(): void {
  cookies().set(SESSION_COOKIE, "", { httpOnly: true, path: "/", maxAge: 0 });
}

/** Lit et vérifie la session courante depuis le cookie. */
export async function getSession(): Promise<SessionPayload | null> {
  const token = cookies().get(SESSION_COOKIE)?.value;
  if (!token) return null;
  return verifySession(token);
}
