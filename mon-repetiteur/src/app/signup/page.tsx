import Link from "next/link";
import { SignupForm } from "./signup-form";

export default function SignupPage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-sm flex-col justify-center gap-6 px-6">
      <div className="flex flex-col gap-1">
        <Link href="/" className="w-fit text-sm font-medium text-indigo-600 dark:text-indigo-400">
          Mon Répétiteur
        </Link>
        <h1 className="text-2xl font-semibold tracking-tight text-zinc-950 dark:text-zinc-50">
          Créer un compte
        </h1>
      </div>
      <SignupForm />
    </main>
  );
}
