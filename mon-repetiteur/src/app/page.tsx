import Link from "next/link";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-zinc-50 px-6 text-center font-sans dark:bg-black">
      <h1 className="text-3xl font-semibold tracking-tight text-black dark:text-zinc-50">
        Mon Répétiteur
      </h1>
      <p className="max-w-md text-lg leading-8 text-zinc-600 dark:text-zinc-400">
        Foundation phase — authentication is live. Curriculum, exercises, AI
        tutor, and exams land in later phases.
      </p>
      <div className="flex gap-4 text-sm font-medium">
        <Link href="/login" className="underline">
          Se connecter
        </Link>
        <Link href="/signup" className="underline">
          Créer un compte
        </Link>
      </div>
    </div>
  );
}
