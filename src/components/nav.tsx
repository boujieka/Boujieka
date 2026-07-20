import Link from "next/link";
import { Wordmark } from "@/components/logo";
import { logoutAction } from "@/lib/auth/actions";
import type { SessionPayload } from "@/lib/auth/session";

const ROLE_LABEL: Record<string, string> = {
  offtaker: "Offtaker",
  developer: "Développeur",
  admin: "Administrateur",
};

export function Nav({ session }: { session: SessionPayload }) {
  const links: { href: string; label: string }[] = [
    { href: "/dashboard", label: "Tableau de bord" },
  ];
  if (session.role === "offtaker") {
    links.push({ href: "/sites", label: "Sites" });
    links.push({ href: "/opportunities", label: "Opportunités" });
    links.push({ href: "/decarbonization", label: "Décarbonisation" });
  }
  if (session.role === "developer") {
    links.push({ href: "/developers/profile", label: "Mon profil" });
    links.push({ href: "/opportunities", label: "Opportunités" });
    links.push({ href: "/matching", label: "Mes matchs" });
  }
  if (session.role === "admin") {
    links.push({ href: "/opportunities", label: "Opportunités" });
    links.push({ href: "/admin/matches", label: "Validation matchs" });
    links.push({ href: "/decarbonization", label: "Portefeuille CO₂" });
  }
  links.push({ href: "/messages", label: "Messagerie" });

  return (
    <header className="border-b border-navy-100 bg-white">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-6 py-3">
        <div className="flex items-center gap-8">
          <Link href="/dashboard">
            <Wordmark />
          </Link>
          <nav className="hidden gap-1 md:flex">
            {links.map((l) => (
              <Link
                key={l.href}
                href={l.href}
                className="rounded-lg px-3 py-1.5 text-sm font-medium text-navy-600 hover:bg-navy-50 hover:text-navy-800"
              >
                {l.label}
              </Link>
            ))}
          </nav>
        </div>
        <div className="flex items-center gap-3">
          <div className="hidden text-right sm:block">
            <div className="text-sm font-medium text-navy-800">{session.fullName}</div>
            <div className="text-xs text-navy-400">{ROLE_LABEL[session.role]}</div>
          </div>
          <form action={logoutAction}>
            <button className="btn-ghost text-sm" type="submit">Déconnexion</button>
          </form>
        </div>
      </div>
      <nav className="flex gap-1 overflow-x-auto border-t border-navy-50 px-4 py-2 md:hidden">
        {links.map((l) => (
          <Link key={l.href} href={l.href} className="whitespace-nowrap rounded-lg px-3 py-1 text-xs font-medium text-navy-600 hover:bg-navy-50">
            {l.label}
          </Link>
        ))}
      </nav>
    </header>
  );
}
