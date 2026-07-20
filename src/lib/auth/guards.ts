/**
 * Garde-fous d'autorisation réutilisables côté serveur (pages & routes API).
 */
import { redirect } from "next/navigation";
import { getSession, type Role, type SessionPayload } from "./session";

/** Exige une session authentifiée ; redirige vers /login sinon. */
export async function requireUser(): Promise<SessionPayload> {
  const session = await getSession();
  if (!session) redirect("/login");
  return session;
}

/** Exige l'un des rôles ; sinon redirige vers le tableau de bord. */
export async function requireRole(...roles: Role[]): Promise<SessionPayload> {
  const session = await requireUser();
  if (!roles.includes(session.role)) redirect("/dashboard");
  return session;
}

/** Variante API : renvoie la session ou null (l'appelant gère le 401/403). */
export async function getApiSession(...roles: Role[]): Promise<SessionPayload | null> {
  const session = await getSession();
  if (!session) return null;
  if (roles.length > 0 && !roles.includes(session.role)) return null;
  return session;
}
