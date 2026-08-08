import Link from "next/link";
import { redirect } from "next/navigation";
import { getCurrentProfile } from "@/services/profiles";
import { LogoutButton } from "./logout-button";
import { AppShell } from "@/components/app-shell";
import { PageHeader } from "@/components/ui/page-header";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { BookIcon, ChartIcon, ArchiveIcon } from "@/components/ui/icons";

const ROLE_LABELS: Record<string, string> = {
  student: "Élève",
  parent: "Parent",
  teacher: "Enseignant",
  admin: "Administrateur",
};

const QUICK_LINKS = [
  { href: "/learn", label: "Voir le programme", description: "Cours et exercices", icon: BookIcon },
  { href: "/progress", label: "Ma progression", description: "Points forts et faibles", icon: ChartIcon },
  { href: "/archive", label: "Archive des épreuves", description: "Sujets des années précédentes", icon: ArchiveIcon },
];

export default async function AccountPage() {
  const profile = await getCurrentProfile();
  if (!profile) {
    redirect("/login");
  }

  return (
    <AppShell>
      <main className="mx-auto flex max-w-2xl flex-col gap-6 px-6 py-8 sm:py-12">
        <PageHeader title="Mon compte" />

        <Card className="flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-indigo-100 text-base font-semibold text-indigo-700 dark:bg-indigo-950 dark:text-indigo-300">
              {(profile.full_name ?? "?").charAt(0).toUpperCase()}
            </div>
            <div>
              <p className="font-medium text-zinc-950 dark:text-zinc-50">
                {profile.full_name ?? "—"}
              </p>
              <Badge tone="info">{ROLE_LABELS[profile.role] ?? profile.role}</Badge>
            </div>
          </div>
          <LogoutButton />
        </Card>

        <ul className="flex flex-col gap-3">
          {QUICK_LINKS.map(({ href, label, description, icon: Icon }) => (
            <li key={href}>
              <Link href={href}>
                <Card className="flex items-center gap-3 transition-colors hover:border-indigo-300 dark:hover:border-indigo-700">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-indigo-50 text-indigo-600 dark:bg-indigo-950 dark:text-indigo-400">
                    <Icon className="h-5 w-5" />
                  </div>
                  <div>
                    <p className="font-medium text-zinc-950 dark:text-zinc-50">{label}</p>
                    <p className="text-sm text-zinc-500 dark:text-zinc-400">{description}</p>
                  </div>
                </Card>
              </Link>
            </li>
          ))}
        </ul>
      </main>
    </AppShell>
  );
}
