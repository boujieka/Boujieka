import { NextRequest, NextResponse } from "next/server";
import { SESSION_COOKIE, verifySession } from "@/lib/auth/session";

/**
 * Middleware d'accès : protège l'espace applicatif (/dashboard, /sites, …).
 * La vérification fine des rôles est faite dans les pages/routes via les
 * garde-fous ; ici on filtre l'authentification de base.
 */
const PROTECTED_PREFIXES = [
  "/dashboard",
  "/sites",
  "/opportunities",
  "/developers",
  "/matching",
  "/messages",
  "/decarbonization",
  "/admin",
];

export async function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;
  const isProtected = PROTECTED_PREFIXES.some((p) => pathname.startsWith(p));
  if (!isProtected) return NextResponse.next();

  const token = req.cookies.get(SESSION_COOKIE)?.value;
  const session = token ? await verifySession(token) : null;
  if (!session) {
    const url = req.nextUrl.clone();
    url.pathname = "/login";
    url.searchParams.set("next", pathname);
    return NextResponse.redirect(url);
  }
  return NextResponse.next();
}

export const config = {
  matcher: [
    "/dashboard/:path*",
    "/sites/:path*",
    "/opportunities/:path*",
    "/developers/:path*",
    "/matching/:path*",
    "/messages/:path*",
    "/decarbonization/:path*",
    "/admin/:path*",
  ],
};
