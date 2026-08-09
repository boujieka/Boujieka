import type { ReactNode } from "react";
import Link from "next/link";
import { redirect } from "next/navigation";
import { getCurrentProfile } from "@/services/profiles";
import { AppShell } from "@/components/app-shell";
import { cn } from "@/lib/cn";

const TABS = [
  { href: "/admin", label: "Vue d'ensemble" },
  { href: "/admin/lessons", label: "Leçons" },
  { href: "/admin/exercises", label: "Exercices" },
  { href: "/admin/exams", label: "Épreuves" },
];

/**
 * Single server-side authorization gate (CLAUDE.md §13) for every /admin/*
 * route — teacher/admin roles only. RLS is the real backstop on every
 * write (lessons/exercises/exams are staff-only at the database level
 * regardless of this), but without this a plain student hitting /admin
 * directly would still see the all-statuses *listings* these pages
 * render, which "published or own or staff" read policies would happily
 * serve to an actual staff member — this is what keeps a non-staff user
 * out in the first place.
 */
export default async function AdminLayout({ children }: { children: ReactNode }) {
  const profile = await getCurrentProfile();
  if (!profile) {
    redirect("/login");
  }
  if (profile.role !== "teacher" && profile.role !== "admin") {
    redirect("/account");
  }

  return (
    <AppShell>
      <div className="mx-auto flex max-w-3xl flex-col gap-6 px-6 py-8 sm:py-12">
        <nav className="flex gap-2 overflow-x-auto" aria-label="Administration">
          {TABS.map((tab) => (
            <Link
              key={tab.href}
              href={tab.href}
              className={cn(
                "shrink-0 rounded-full bg-zinc-100 px-3 py-1.5 text-xs font-medium text-zinc-600 transition-colors hover:bg-zinc-200",
                "dark:bg-zinc-800 dark:text-zinc-300 dark:hover:bg-zinc-700",
              )}
            >
              {tab.label}
            </Link>
          ))}
        </nav>
        {children}
      </div>
    </AppShell>
  );
}
