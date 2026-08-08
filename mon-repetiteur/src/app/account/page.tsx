import Link from "next/link";
import { redirect } from "next/navigation";
import { getCurrentProfile } from "@/services/profiles";
import { LogoutButton } from "./logout-button";

export default async function AccountPage() {
  const profile = await getCurrentProfile();
  if (!profile) {
    redirect("/login");
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-sm flex-col justify-center gap-6 px-6">
      <h1 className="text-2xl font-semibold text-black dark:text-zinc-50">
        Mon compte
      </h1>
      <dl className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-1 text-sm">
        <dt className="text-zinc-500">Nom</dt>
        <dd className="text-black dark:text-zinc-50">{profile.full_name ?? "—"}</dd>
        <dt className="text-zinc-500">Rôle</dt>
        <dd className="text-black dark:text-zinc-50">{profile.role}</dd>
      </dl>
      <Link href="/learn" className="text-sm underline">
        Voir le programme
      </Link>
      <LogoutButton />
    </main>
  );
}
